# 来源与证据

参考仓库：https://github.com/moneymanagerex/android-money-manager-ex

Commit：866062b4dbecab72e6b922794c82c2f61f4b7c06；许可证：License。冻结记录见 ../../../evidence/sources-03/source-lock.json；实际构建为 money-manager-build-01，APK minSdk29。

已阅读冻结仓库里的 docs/quickstart/start_standalone.md、docs/usermanual/add_transaction.md、docs/usermanual/concept.md：手册定义账户、收入、支出、转账及状态；明确转账不计入收入/支出、交易不能早于开户日期，描述账本文件创建和账户初始化。手册不是本机行为验收。

实际设备 API29 / emulator-5582：money-explore-01 安装成功、冷启动命令超时；02 采集到原版引导；03 关闭引导进入 General；04 返回新建/打开账本页；05 点击新建后进入系统 DocumentsUI，因未声明窗口包而标记错误，不能作为 App 失败；06 显式采集系统保存页；07 点击 SAVE 回到可选密码页；08 留空密码点 OK，进入空账本首页。账本默认名 your_data_20261016_120355.mmb。未声称交易、余额或恢复已验证。

题包状态 DRAFT；尚缺完整设备链路、输入夹具、设计截图、环境生命周期、隐藏测试、3次 Golden、错误实现、多模型及人工独立评分。不创建虚假的合格状态或正式 task.toml。

后续证据：money-explore-09 进入新账户表单，10 输入 Survey Cash，11 点击初始余额进入独立计算器。money-first-account-01 真实点击1、0、0，保存回表单确认 $ 100.00，再保存账户进入首页，五步七断言通过。首页截图已查看：Cash Accounts、Survey Cash、Summary 均显示 $ 100.00，当前月收入/支出/差额均0.00。保存后的重启恢复、数据库同步和多账户业务仍未验证。本次草稿设计图 cash-account-home.png 来自该原始截图，不是完整设计集。

money-explore-12至15完成导航到新账户表单；money-bank-form-01输入Survey Bank并打开类型菜单；money-bank-create-01完成Checking账户创建，初始1000.00。10步通过，首页分别验证Cash=100.00、Bank=1000.00、Summary=1100.00、收入/支出=0。使用相同资源ID时按账户名称所在行匹配，禁止借用另一行数值。截图已查看。LG-02取得更多部分证据，LG-03/04交易与转账仍未执行。

新增LG-04部分证据：money-explore-18至20从Survey Bank交易列表打开新增并选择Transfer。money-transfer-01九步16断言通过，真实转账80后Cash180、Bank920、Summary1100，收入/支出/差额均0；截图已查看。LG-04转账更正仍未完成，普通收支、生命周期恢复和状态口径仍待验证。

首页快捷新增要求默认账户；当前未设置默认，点击后立即返回。该条件由money-explore-16/17现象及CheckingTransactionEditActivity的handleIntent/onCreate代码共同解释。正式任务书将使用账户内新增入口，或显式设置默认账户，不能把未满足前置条件当功能失败。
