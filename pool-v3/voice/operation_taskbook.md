# 操作链草稿

1. 通过系统选择器分别授权多书目录、单书目录、作者目录；比对实际书籍与章节分组。
2. 播放书A第一章并记录真实音频，跳至另一章中部，建书签；切换书B同名章节。
3. 回到书A核对独立进度；从书签跳转，核对实际发声内容，不只看时间标签。
4. 暂停、继续、变速、章节边界连播，比较媒体推进与墙钟时间；容差实测后冻结。
5. 设置睡眠定时，等待真实暂停；恢复播放、前后台和系统媒体控制，验证没有双重音频。
6. 终止进程后重开，重新扫描，再验证书籍身份、进度与书签；处理权限取消和损坏媒体。

以上完整链路仍待设备核验。音频采集能力尚未证明，不得用无音频的屏幕录像代替。系统事件、UiAutomation、原始音频及时间戳应共同留证。

## 已观察的书库与章节状态

前置条件：通过系统文件选择器授权 input/audio-v01/library 对应目录，以 Top-Level Book Mode 导入。以下为参考 App 的局部观察，不是完整链路验收；初次授权流程尚未封装为可重复执行的完整轨迹。

| 状态ID | 动作 | 目标 | 预期状态 | 证据点 |
| --- | --- | --- | --- | --- |
| AB-L01 | 导入完成后查看书库 | 五个 MP3 的书籍分组 | 显示 Field Journal、Weather Notes、Station Log 三本书；初始位于 Not started Yet 分组 | library-imported.png、书库语义树 |
| AB-L02 | 核对书籍时长 | 三本书的列表行 | Field Journal 与 Weather Notes 显示 01:05，Station Log 显示 00:30 | library-imported.png；实际媒体时长另见夹具清单 |
| AB-L03 | 打开 Field Journal | 第一章播放器 | 书名 Field Journal，章节 Arrival，位置 0:00，章节时长 0:32，显示 Play 控件 | arrival-paused.png、播放器语义树 |
| AB-L04 | 打开章节选择器 | Field Journal 的章节 | 提供 Arrival、Return 两章，标识当前章节 | 章节选择器语义树 |
| AB-L05 | 选择 Return | 第二章播放器 | 章节切换到 Return，显示 0:33 与 Play 控件 | return-paused.png、播放器语义树 |
| AB-L06 | 停止进程后重开并进入 Field Journal | 已选章节状态 | 书库保留三本书；Field Journal 位于 Current 分组，重开为 Return、0:33、Play | 重启后的书库及播放器语义树 |

L06 的既有观察发生于 AOT 编译和一次启动超时后的独立检查，不能作为干净启动耗时或稳定性通过证据。L03/L05 的 Play 图标仅说明界面处于待播放状态，不能推出真实音频输出、独立播放进度或章节连播正确。

上述观察的维护侧来源：references/voice-exploration.md、voice-library-check.json、voice-chapter-selection.json、voice-restart-state-check.json。公开截图映射见 input/design/README.md。书签、速度、睡眠、系统媒体控制、损坏媒体和跨书进度仍需单独验证。
