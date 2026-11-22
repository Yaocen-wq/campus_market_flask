# 校园二手平台—自动化测试框架

这是我自己做的一个项目。被测的网站是我自己写的（Flask）
测试代码也是我自己写的，一共 49 条用例

网页用 Selenium 测，接口用 Requests 测，用 pytest 统一跑
`app.py` 和 `templates/` 是被测对象，`test_framework/` 是测试代码

## 环境

Windows11，Python 3.12.10，用 Edge 浏览器，驱动由 selenium 自己去下对应的驱动
数据库用 MySQL8.0，库名 campus_flea_market

## 目录
    campus_market_flask/
    ├─ app.py                       被测的 Flask 后端
    ├─ templates/                   被测的网页
    ├─ create_tables.sql            建库、建表、插固定账号
    ├─ pytest.ini                   标记项目根目录
    ├─ requirements.txt             依赖版本
    ├─ postman/                     postman调试用的存档
    ├─ Jenkinsfile                  CI 流水线定义
    ├─ test-docs/                   手工测试
    │  ├─ 手工用例.xlsx              85 条手工用例
    │  └─ bug-reports/              15 份 bug 报告
    ├─ ci/
    │  └─ run_api_ci.ps1            Jenkins 用的 CI 脚本
    └─ test_framework/
       ├─ config.py                 环境配置：路径、地址、等待时间
       ├─ conftest.py               确认路径锚 + 记每条用例的结果
       ├─ dashboard.py              Streamlit 看板
       ├─ fail_report.py            失败分类
       ├─ data/                     测试数据
       │  ├─ fixtures.yaml          前置账号、固定商品（对应 create_tables.sql）
       │  ├─ api/                   接口用例数据
       │  │  ├─ smoke.yaml
       │  │  ├─ negative.yaml
       │  │  ├─ project.yaml
       │  │  ├─ chain.yaml
       │  │  └─ mock_pay.yaml
       │  └─ web/                   网页用例数据
       │     ├─ login.yaml
       │     ├─ register.yaml
       │     ├─ publish.yaml
       │     ├─ order_submit.yaml
       │     ├─ order.yaml
       │     └─ home.yaml
       ├─ api/                      接口
       │  ├─ api_log.py             发请求的封装，并记录请求和响应
       │  ├─ conftest.py            每条用例前清记录；挂了把记录贴进报告
       │  ├─ project_test.py        20 条，参数化
       │  ├─ negative_test.py       3 条，反例
       │  ├─ smoke_test.py          3 条，冒烟
       │  ├─ full_chain_test.py     1 条，全链路
       │  ├─ test_mock_pay.py       2 条，测支付 Mock
       │  └─ mock_pay_server.py     自己写的 Mock（5001）
       ├─ web/                      网页
       │  ├─ conftest.py            开关浏览器 + 自动截图
       │  ├─ pages/                 页面类 + BasePage（定位器留在页面类里）
       │  └─ test_*_po.py           6 个文件（20条用例）
       └─ utils/
          ├─ logger.py             写日志
          └─ data_loader.py        读 data/ 下的 YAML

日志、报告、截图都是代码自动生成，没放仓库
手工测试的成果在 test-docs/ 85 条用例 + 15 份 bug 报告

---

## 怎么跑

- 下面所有命令需要用Windows PowerShell在项目根目录执行
- 步骤 1、4、5 在窗口1执行
- 跑完全部之前不要关掉窗口1、2、3

1.打开一个窗口（窗口1）建虚拟环境、装依赖：

    python -m venv .venv
    .\.venv\Scripts\activate 
    pip install -r requirements.txt

2.建库。create_tables.sql 会删同名旧库。

    用 MySQL Workbench 打开：File → Open SQL Script → 选 create_tables.sql
    → 点闪电图标执行

3.打开两个新窗口起服务

窗口2 flask：

    .\.venv\Scripts\activate
    $env:DB_PASSWORD="你的 root 密码"
    python app.py                        

窗口3 Mock：

    .\.venv\Scripts\activate
    python test_framework\api\mock_pay_server.py   

4.跑测试：

    python -m pytest test_framework\api test_framework\web -v -s --clean-alluredir --alluredir=test_framework\allure-results

5.看报告（要装 Allure 命令行工具）：

    allure serve test_framework\allure-results                                 # 打开临时报告
    allure generate test_framework\allure-results -o allure-report --clean     # 生成静态报告
    allure open allure-report                                                  # 打开静态报告

6.看板（可选）：

    python -m streamlit run test_framework\dashboard.py
    # 需要跑完测试再执行


第二次跑之前，需要改「期望注册成功」的账号和邮箱（换成没用过的）。
用 Jenkins 时不改，CI 每次会重建库：

- `test_framework\data\api\project.yaml` 的 `register_cases` 第一条（`id: 正例`）
- `test_framework\data\api\chain.yaml` 的 `user` 
- `test_framework\data\web\register.yaml` 的 `reg-1`

不想改账号就执行 `create_tables.sql` 重置数据库，改了就不要重置


## CI（Jenkins）

1.建 ci.cnf 把 password 换成自己的 MySQL root 密码

    [client]
    user=root
    password=你的密码
    default-character-set=utf8mb4

放在 Jenkins 主目录（JENKINS_HOME）路径默认是 C:\ProgramData\Jenkins\.jenkins\
如果 Jenkins 主目录（JENKINS_HOME）路径有变动或者想放在其他地方就需要改 run_api_ci.ps1 里 $Cnf 指定路径那一行


2.把 ci\run_api_ci.ps1 第 4 行 $Py，改成本机 venv 里 python.exe 的绝对路径

3.打开 Jenkins 网页
    
    New Item → 随便起名 → 选 Pipeline → Definition 选 Pipeline script from SCM → 
    SCM 选 Git → 填自己需要提交的 gitHub 仓库 URL → Branch 填 */main → 
    Script Path 填 Jenkinsfile → 保存

之后可以手动点 Build Now 也可以让 poll SCM 定时检查代码(1.每五分钟检查 2.需要先手动构建一次之后就不用管了有新提交自动构建）
产物 allure-results 和构建一起归档，在构建页可以下载

---

## 49 条是什么

| 文件 | 条数 | 测什么 |
|---|---|---|
| api/project_test.py | 20 | 注册、登录、发布、下单、查订单、支付回调 |
| api/negative_test.py | 3 | 反例 |
| api/smoke_test.py | 3 | 冒烟 |
| api/full_chain_test.py | 1 | 注册→登录→发布→取 id→下单 |
| api/test_mock_pay.py | 2 | 支付 Mock |
| web/ 下 6 个文件 | 20 | 6 个页面，PO 写法 |

2026.11.21 跑的结果：

| 跑的哪个 | 结果    | 耗时      |
|------|-------|---------|
| api  | 29 条过 | 0.87 秒  |
| web/ | 20 条过 | 17.79 秒 |
api 的 0.87 秒不含建库和起停服务

## 跑完后的产物

| 产物          | 位置 | 是否进仓库 |
|-------------|---|-|
| Allure 原始结果 | test_framework/allure-results/ | 否 |
| 日志文件        | test_framework/logs/test.log | 否 |
| web 失败后截图   | test_framework/web/screenshots/ | 否 |
| 失败汇总 md     | test_framework/logs/fail_summary.md | 否 |
| 失败汇总 json   | test_framework/logs/fail_summary.json | 否 |

日志文件和失败截图文件夹，不自动清空；
失败汇总的两个文件每次跑完重写，全部通过时会写成 total=0。

---

## 备注

- **地址** 一开始我是直接写在用例文件里的，后来想换个端口得翻好几个文件，
于是后面写到 `config.py` 里统一管理


- **数据和代码** 代码通过 `utils/data_loader.py` 去读取 `data/` 里的数据


- **页面元素** 元素最开始写在测试函数里，页面一改就得全找一遍。
后面每个页面单独写成一个类放 `web/pages/`，测试里只剩“打开登录页 →
登录 → 看结果”，如果页面改版就只动 pages 里的类


- **失败了怎么查** 接口用例挂了，`api/conftest.py` 会把这条用例发的请求、
收的响应一起贴到 Allure 报告里；网页用例挂了，`web/conftest.py` 会截图保存到 `web/screenshots`


- **三个conftest** 根目录的是为了让子目录里 import config 能找到，
以及记每条用例过了还是挂了。api 那个管清记录、挂证据到 Allure 报告，
web 那个管开关浏览器和截图


- **全链路** 从头到尾用一个 Session：注册、登录、发布、取商品 id、下单。
登录用的是刚刚注册的账号，所以注册要是挂了，后面也会挂，不会出现注册失败但整条还是绿的


- **失败汇总** 每次跑完 `fail_report.py` 把失败分类，
分类的东西写到 `logs/fail_summary.md` 和 `logs/fail_summary.json`
