pipeline {
    agent any
    triggers { pollSCM('H/5 * * * *') }
    stages {
        stage('跑接口测试') {
            steps {
                powershell '& ./ci/run_api_ci.ps1'
            }
        }
    }
    post {
        always { archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true }
    }
}