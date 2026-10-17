# 本地发现与媒体服务

工作目录为本task，运行 `python3 input/mock_server.py --host 0.0.0.0 --port 8765`，不需要pip包或外网。
模拟器内base URL通常为http://10.0.2.2:8765；真机填写可达的主机局域网IP。App提供设置base URL字段，不硬编码候选包名。服务仅监听测试网络，不含凭据。

GET /search?q=slow&page=1 延迟1200ms返回v-a；GET /search?q=fast&page=1 延迟50ms返回v-a/v-b与next_page=2；page2返回v-b/v-c和null。客户端按video id稳定去重，后返回旧查询不得覆盖当前查询。
GET /media/video-a.mp4等返回实际24秒H264/AAC视频，支持单区间Range；GET /media/missing.mp4固定404。无在线YouTube抓取/登录/订阅API。应用本地维护收藏/队列。所有时延为模拟服务规则，不是原NewPipe行为声明。
服务重启没有业务持久状态，重复轨迹可用相同输入。图中Blender影片只是官方页面参考，任务播放的是本题原创色板/时间标记/音轨。
