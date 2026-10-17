# MCP-012 兄弟卡片、撤销评分与笔记编辑的复习队列

## 目标与来源

围绕牌组列表、问答翻面、评分按钮、笔记编辑和统计页实现可恢复的复习会话；同一笔记双向卡片共享文本但独立排期，评分撤销恢复队列和统计。

参考真实开源Android应用 AnkiDroid：https://github.com/ankidroid/Anki-Android，固定源码版本 `e331d34f62b619d36b0e5d53ee04078855dc7e0a`。交付可安装debug APK、完整源码、构建说明和人工自测记录。从空工程实现本题范围即可，不要求完整克隆原App。可以使用成熟开源组件，不以源码规模计分。

## 视觉参考

input/design中是实际从官方来源下载、解析并人工审视过的Android页面。保留原图，不将图标或自造界面当截图。参考其信息层级、列表密度、操作位置与状态表达；商店宣传外框/文字不属于App UI，不需实现。截图不是本机运行证据，也不保证与固定commit同版；数据、颜色和名称可按本题素材调整。看不到的异常/恢复状态按下列合同实现，不能从截图推断隐藏业务规则。

- S01 `input/design/official-01.png`：问面提示和输入区域，参考问答阶段区分；对应 R03, R07, R09
- S02 `input/design/official-02.png`：答案揭示与Again/Good/Easy评分操作区；对应 R03, R04, R05, R10
- S03 `input/design/official-03.png`：牌组列表与到期卡计数；对应 R01, R02, R11
- S06 `input/design/official-06.png`：复习统计页面的分类与趋势信息；对应 R04, R08, R12
- S07 `input/design/official-07.png`：笔记字段编辑页与保存入口；对应 R01, R06, R13

## 冻结业务契约

标为reference_documented的是官方页面明确展示的真实能力；synthetic_extension冻结测试数据、精确数值和恢复边界，不冒充原版内部协议或完整算法。

### R01 (synthetic_extension)

导入collection.json和TSV更新。note_id与card_id必须独立；每note生成f/r两卡共享内容而排期独立。TSV按note_id更新原note，空白字段保留原值，不创建重复卡，不重置due或review日志。未知ID拒绝整份更新。

### R02 (synthetic_extension)

牌组显示当前可复习数量，条件due<=当前业务时钟、未suspended、未临时bury。按due再card_id升序。业务时钟初值来自fixture，提供测试工具入口推进60秒/1天，禁止用真实系统钟造成不可复现。

### R03 (synthetic_extension)

问面只显示当前方向的提示；翻面后显示答案和Again/Good/Easy，未翻面不能评分。反向卡r交换front/back。评分提交一次生成唯一review_id，界面未完成提交前再次点按不得重复记数。

### R04 (synthetic_extension)

本题调度明确不是FSRS/SM2：评分后due=评分时钟+60/86400/345600秒，分别对应Again/Good/Easy，interval_seconds同步。统计按review日志计算各评分次数；同note另一张卡在当前会话临时bury，不改原due。点击结束会话解除全部bury。

### R05 (synthetic_extension)

撤销最近一次评分必须同时删除该review、恢复旧due/interval、恢复被该评分bury的兄弟卡和原当前问面；其他日志不动。只支持最近一次，后续评分替代撤销栈顶。取消编辑不影响排期。

### R06 (synthetic_extension)

从复习页进入编辑note并保存后，两方向内容立即更新，当前卡回问面，due和历史不变；回牌组再进入按同一队列规则，不把同标题当ID。

### R07 (synthetic_extension)

成功评分/撤销/编辑持久化；force-stop恢复会话当前card_id、问/答面、bury集合及业务时钟，未保存编辑草稿丢弃。旋转不翻面、不评分、不重新抽卡。

### R08 (synthetic_extension)

导出UTF-8 JSON，包含notes/cards/reviews/current_card_id/face/clock/buried_ids；reviews含review_id,card_id,rating,at,previous_due,new_due，按at再review_id排序。统计与牌组计数必须能由导出重建。无需AnkiWeb登录、同步或实现.apkg兼容。

### R09 (reference_documented)

保留官方页面中可见的主要能力与信息层级：问面提示和输入区域，参考问答阶段区分。截图只证明页面设计，不证明本题新增边界已实测。

### R10 (reference_documented)

保留官方页面中可见的主要能力与信息层级：答案揭示与Again/Good/Easy评分操作区。截图只证明页面设计，不证明本题新增边界已实测。

### R11 (reference_documented)

保留官方页面中可见的主要能力与信息层级：牌组列表与到期卡计数。截图只证明页面设计，不证明本题新增边界已实测。

### R12 (reference_documented)

保留官方页面中可见的主要能力与信息层级：复习统计页面的分类与趋势信息。截图只证明页面设计，不证明本题新增边界已实测。

### R13 (reference_documented)

保留官方页面中可见的主要能力与信息层级：笔记字段编辑页与保存入口。截图只证明页面设计，不证明本题新增边界已实测。

## 输入与交付边界

collection.json是本题交换格式，不是Anki原生数据库；updates.tsv真实制表符分隔。rating-contract.json公开调度规则，故意不假称复刻原版FSRS。截图年代较早，仅用页面结构作参考。

作答模式固定为从空工程重建限定流程。repo/commit仅为构题侧来源；模型公开输入是Spec、截图和fixture，不提供原版源码或Git历史，不得直接打包或修改原版App作为答案。允许成熟通用组件与领域库。

操作控件必须有可访问名称，列表身份/计数/状态有可读语义。横竖屏与1.3字体不能遮挡核心按钮；旋转不得重复提交。禁止要求商业账号或生产数据；不将下载依赖失败或设备限制计为业务难度。导出文件通过系统选择器取得，不依赖候选包名、数据库或内部类名。

运行时功能需按任务书验证，不能只展示截图或硬编码终态；视觉评估看页面层次、主要组件和状态反馈，不要求复制商标或第三方版权媒体。所有输入夹具为本题原创或官方截图参考；原App截图中的电影、书籍、卡片内容不属于要求复制的训练素材。

当前仅完成题面、输入与静态来源核对。Android运行、参考实现、隐藏评测、模型试做和人工验收仍PENDING，不提供虚假的已通过比例。
