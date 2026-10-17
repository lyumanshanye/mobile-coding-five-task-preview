# 公开离线邮件服务

执行 python3 mock_server.py --db mock-mail.sqlite3；仅监听127.0.0.1:8765，不连接任何真实邮件系统。模拟器使用 adb reverse tcp:8765 tcp:8765，App端点设置为 http://127.0.0.1:8765；仅为此本地测试端点允许明文HTTP。服务由验收侧启动，模型不需要实现或修改服务。

POST /send JSON: {"account_id":"work","request_id":"UUID","payload":{"from":"worker@example.test","to":["team@example.test"],"subject":"test","body":"text","in_reply_to":"<meeting@example.test>","attachments":[{"name":"agenda.txt","mime":"text/plain","base64":"..."}]}}。payload内容在首次入队后冻结。200返回server_id；409为相同键不同内容；503为公开模拟离线。

POST /mode 使用 {"mode":"normal"}、{"mode":"offline"} 或 {"mode":"accept_then_timeout"}。最后一个模式首次接受请求并提交SQLite后直接断开连接，不返回响应；客户端应按结果未知处理，重试相同ID返回200。每个新的请求都可触发一次，不是全局仅一次。

GET /state 返回mode和accepted数组；POST /reset 使用 {} 清除本题服务记录并恢复normal。重置客户端数据另由App演示重置命令完成。测试前先重置两侧。服务重启保留相同--db文件中的接受记录和模式。不得将服务记录或故障开关视为真实邮件服务器功能。
