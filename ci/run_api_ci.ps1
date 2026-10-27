$ErrorActionPreference = 'Stop'

$Root   = if ($env:WORKSPACE) { $env:WORKSPACE } else { 'D:\huang\mysoftware\pycode\campus_market_flask' }
$Py     = 'D:\huang\mysoftware\pycode\campus_market_flask\.venv312\Scripts\python.exe'
$Mysql  = 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe'
$Cnf    = if ($env:WORKSPACE) { 'C:\ProgramData\Jenkins\.jenkins\ci.cnf' } else { 'D:\huang\mysoftware\pycode\campus_market_flask\ci.cnf' }
$Sql    = Join-Path $Root 'create_tables.sql'
$Req    = Join-Path $Root 'requirements.txt'
$LogDir = Join-Path $Root 'test_framework\logs'
$Allure = Join-Path $Root 'test_framework\allure-results'

function Test-Port([int]$Port) {
    $c = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    return [bool]$c
}

function Stop-Svc([string]$Pattern, [string]$Label) {
    $procs = @(Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
               Where-Object { $_.CommandLine -like $Pattern })
    if ($procs.Count -eq 0) { Write-Host "[kill] $Label none"; return }
    foreach ($p in $procs) {
        Write-Host "[kill] $Label PID=$($p.ProcessId)"
        & cmd /c "taskkill /PID $($p.ProcessId) /T /F >nul 2>&1"
        if ($LASTEXITCODE -ne 0) { Write-Host "[kill] $Label PID=$($p.ProcessId) already gone" }
    }
}

function Wait-Port([int]$Port, [string]$Label, [int]$Timeout = 20) {
    for ($i = 1; $i -le $Timeout; $i++) {
        if (Test-Port $Port) { Write-Host "[ok] $Label :$Port"; return $true }
        Start-Sleep -Seconds 1
    }
    Write-Host "[fail] $Label :$Port not up in ${Timeout}s"
    return $false
}

function Show-Ports {
    foreach ($pt in 5000, 5001) {
        $free = -not (Test-Port $pt)
        Write-Host "[port] $pt free=$free"
    }
}

$rc = 1
try {
    Set-Location $Root
    $env:PYTHONPATH = $Root
    New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

    # 0 装依赖
    if (Test-Path $Req) {
        & $Py -m pip install -q -r $Req
        Write-Host '[ok] deps installed'
    } else {
        Write-Host '[skip] no requirements.txt'
    }

    # 密码进环境变量
    $line = (Select-String -Path $Cnf -Pattern '^\s*password\s*=' | Select-Object -First 1).Line
    if (-not $line) { throw 'no password= line in ci.cnf' }
    $env:DB_PASSWORD = ($line -split '=', 2)[1].Trim()

    # 1 杀残留
    Stop-Svc '*app.py*' 'flask'
    Stop-Svc '*mock_pay_server*' 'mock'
    Start-Sleep -Seconds 2

    # 2 重置库
    $o = Join-Path $LogDir 'ci_mysql.out'
    $e = Join-Path $LogDir 'ci_mysql.err'
    $m = Start-Process -FilePath $Mysql -ArgumentList "--defaults-extra-file=$Cnf" `
            -RedirectStandardInput $Sql -RedirectStandardOutput $o -RedirectStandardError $e `
            -NoNewWindow -PassThru -Wait
    if ($m.ExitCode -ne 0) { Get-Content $e | Write-Host; throw "mysql exit=$($m.ExitCode)" }
    Write-Host '[ok] reset db done'

    # 3 起服务
    $fl = Join-Path $LogDir 'ci_flask.log'
    $ml = Join-Path $LogDir 'ci_mock.log'
    Start-Process -FilePath $Py -ArgumentList 'app.py' -WorkingDirectory $Root -WindowStyle Hidden `
        -RedirectStandardOutput $fl -RedirectStandardError "$fl.err" | Out-Null
    Start-Process -FilePath $Py -ArgumentList 'test_framework\api\mock_pay_server.py' -WorkingDirectory $Root -WindowStyle Hidden `
        -RedirectStandardOutput $ml -RedirectStandardError "$ml.err" | Out-Null

    if (-not (Wait-Port 5000 'flask')) { throw 'flask not listening' }
    if (-not (Wait-Port 5001 'mock'))  { throw 'mock not listening' }

    # 4 跑测试（只此一处 pytest）
    & $Py -m pytest test_framework\api -v --alluredir=$Allure --clean-alluredir
    $rc = $LASTEXITCODE
    Write-Host "pytest exit=$rc"

    # 5 产物复制进工作区
    if ($env:WORKSPACE) {
        $dst = Join-Path $env:WORKSPACE 'allure-results'
        Remove-Item -Recurse -Force $dst -ErrorAction SilentlyContinue
        New-Item -ItemType Directory -Force -Path $dst | Out-Null
        Copy-Item "$Allure\*" -Destination $dst -Recurse -Force
    }
}
catch {
    Write-Host "[err] $($_.Exception.Message)"
    $rc = 1
}
finally {
    Stop-Svc '*app.py*' 'flask'
    Stop-Svc '*mock_pay_server*' 'mock'
    Start-Sleep -Seconds 2
    Show-Ports
}
exit $rc