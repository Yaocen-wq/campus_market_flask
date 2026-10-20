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
    ├─ pytest.ini                   关掉中文用例名转义的文件
    ├─ requirements.txt             依赖版本
    ├─ postman/                     postman调试用的存档
    ├─ test-docs/                   手工测试
    │  ├─ 手工用例.xlsx             85 条手工用例
    │  └─ bug-reports/              15 份 bug 报告
    └─ test_framework/
       ├─ config.py                 配置文件
       ├─ conftest.py               确认路径锚 + 记每条用例的结果
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
       │  ├─ pages/                 页面类 + BasePage
       │  └─ test_*_po.py           6 个文件（20条用例）
       ├─ utils/logger.py           写日志
       └─ data/.gitkeep             给以后放数据文件留的位置

日志、报告、截图都是代码自动生成，没放仓库
手工测试的成果在 test-docs/ 85 条用例 + 15 份 bug 报告

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
    $env:DB_PASSWORD="你的 root 密码"   # 密码是 "Campus123!" 时不执行这行
    python app.py                        

窗口3 Mock：

    .\.venv\Scripts\activate
    python test_framework\api\mock_pay_server.py   

4.跑测试：

    python -m pytest test_framework\api -v -s --clean-alluredir --alluredir=test_framework\allure-results
    python -m pytest test_framework\web -v -s --alluredir=test_framework\allure-results

5.看报告（要装 Allure 命令行工具）：

    allure serve test_framework\allure-results

第一次跑不用改任何东西，数据库是新建的，注册用的号都是空的。
第二次跑之前要把 `test_framework\config.py` 里的 `REG_*`
换成没用过的账号，不然注册正例会报“用户名已存在”

## 49 条是什么

| 文件 | 条数 | 测什么 |
|---|---|---|
| api/project_test.py | 20 | 注册、登录、发布、下单、查订单、支付回调 |
| api/negative_test.py | 3 | 反例 |
| api/smoke_test.py | 3 | 冒烟 |
| api/full_chain_test.py | 1 | 注册→登录→发布→取 id→下单，一条走完 |
| api/test_mock_pay.py | 2 | 支付 Mock |
| web/ 下 6 个文件 | 20 | 6 个页面，PO 写法 |

---
2026.10.18 在 Python 3.12.10 + selenium 4.51.0 上跑的结果：

| 跑的哪个 | 结果 | 耗时      |
|---|---|---|
| api/project_test.py | 20 条过 | 0.26 秒  |
| api/test_mock_pay.py | 2 条过 | 0.04 秒  |
| web/ | 20 条过 | 12.10 秒 |
| full_chain / negative / smoke | 7 条过 | 0.11 秒  |

49 条是单独确认过的。跑 web 之前我把自己电脑上的驱动缓存整个挪走了，
所以那次是先下载再跑的，下下来是 155.0.4283.62。
这么做就是想确认一下：别人 clone 下来，是不是也能跑

## 几个纠结过的点

- **地址** 一开始我是直接写在用例文件里的，后来想换个端口得翻好几个文件，
于是后面写到 `config.py` 里统一管理


- **页面元素** 元素最开始写在测试函数里，页面一改就得全找一遍。
后面每个页面单独写成一个类放 `web/pages/`，测试里只剩“打开登录页 →
登录 → 看结果”，一行找元素的代码都没有。改版了就只动 pages 里的类。


- **页面类继承 `BasePage`** 里面写了 6 个动作：打开网页、找元素、
输入、点击、读文字、等文字出现。找元素统一加了 10 秒显式等待，没用 sleep。
`login_page.py` 里定位方法用了id、css、xpath：用户名用 ID、密码用 CSS、
登录按钮用 XPath，想看看是不是都能跑通。


- **失败了怎么查** 接口用例挂了，`api/conftest.py` 会把这条用例发的请求、
收的响应一起贴到 Allure 报告里；网页用例挂了，`web/conftest.py` 会截图贴进去。
这样不用再去翻日志猜


- **三个conftest** 根目录的是为了让子目录里 import config 能找到，
以及统一记每条用例过了还是挂了。api/ 那个管清记录、挂证据，
web/ 那个管开关浏览器和截图。


- **全链路** 从头到尾用一个 Session：注册、登录、发布、取商品 id、下单。
登录用的是刚刚注册的账号，所以注册要是挂了，后面也会挂，不会出现注册失败但整条还是绿的