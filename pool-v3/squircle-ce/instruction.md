# 代码编辑器：多文件编辑、查找替换与安全保存

## 用户目标
在手机上维护一个小型网页项目，同时编辑JavaScript和CSS，使用搜索替换与撤销，并在目录权限失效时避免静默丢稿。

在Android端实现以下可交互工作流。参考应用是设计与功能来源，不要求复刻全部应用。

## 输入与初始状态
input/project包含main.js、styles.css、index.html，都是可编辑的真实文本文件。仅作为编辑器输入，不要求运行JavaScript或内置终端。taskId在main.js出现4次，目录授权通过Android SAF完成；无需网络。

## 需求

### R1
通过系统目录授权打开input/project，文件树可展开；同时打开main.js与styles.css，用标签切换并保持各自光标、滚动位置及未保存内容。

来源：synthetic_extension；对应图：S01, S03。

### R2
JavaScript语法高亮、行号和编辑键盘可用；支持选区、复制粘贴、缩进、撤销重做；高亮不得改变源文件文本。

来源：reference_documented；对应图：S01, S02。

### R3
在main.js查找taskId并逐项替换为itemId，显示匹配数量与当前项；仅替换当前文件，全部替换可一次撤销。

来源：synthetic_extension；对应图：S01。

### R4
编辑器字号、换行、主题可调整，设置返回后不丢草稿或选区；键盘显示时光标不被遮挡。

来源：reference_documented；对应图：S04, S05。

### R5
保存两文件后重新打开内容一致；撤销目录授权后保存明确失败并保留草稿，重新授权可保存。关闭未保存标签必须提供保存/放弃/取消。

来源：synthetic_extension；对应图：S03。

## 交付要求
提交可构建Android源代码、构建说明、APK、输入导入说明；逐条执行operation_taskbook.md并记录截图/录屏、实际结果与失败原因。界面中不得放验收答案或把输入预编码成固定结果。参考图中的宣传外框不属于应用UI。不得把题包文档检查当Android执行验证。

## 边界
- 尚未构建或运行Android应用；操作轨迹是交付验收方案，不是已执行记录。
- 截图未逐一绑定源代码commit；不能据此声称完整设计稿或像素级精确复刻。
- synthetic_extension是本题新增约束，不声称原应用已支持该语义。

## 实现模式
从空工程重建上述限定完整流程。执行模型只获得题面、参考图片和fixture；作者溯源仓库与commit不提供给执行模型，禁止直接修改原App并打包。可使用成熟的通用解析、渲染和媒体库。

## 可执行权限故障入口
调试构建提供“释放当前测试目录授权”命令，调用ContentResolver.releasePersistableUriPermission释放已持久化的SAF读写授权，同时关闭本App持有的该目录流/文件描述符；操作后再次通过DocumentFile/ContentResolver重新访问，禁止复用旧句柄。入口显示目标URI与已释放结果，仅影响用户授权的本题测试目录。恢复入口重新调用ACTION_OPEN_DOCUMENT_TREE并取得持久化授权。运行记录需保留授权释放、失败反馈与重新授权过程；不能仅将UI状态切成无权限来冒充真实失败。
