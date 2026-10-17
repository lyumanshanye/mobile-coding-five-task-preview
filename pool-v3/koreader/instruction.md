# MCP-013 重排版后的阅读锚点、批注与同名书籍隔离

## 目标与来源

用两本实际EPUB实现目录跳转、文本选择高亮、批注列表和稳定阅读位置；改变字号/方向造成重新分页后，同一语义锚点仍可恢复，不能只保存页码。

参考真实开源Android应用 KOReader：https://github.com/koreader/koreader，固定源码版本 `f3f88f7ca774b626ba4bdf8d6341e8b895b8ff3c`。交付可安装debug APK、完整源码、构建说明和人工自测记录。从空工程实现本题范围即可，不要求完整克隆原App。可以使用成熟开源组件，不以源码规模计分。

## 视觉参考

input/design中是实际从官方来源下载、解析并人工审视过的Android页面。保留原图，不将图标或自造界面当截图。参考其信息层级、列表密度、操作位置与状态表达；商店宣传外框/文字不属于App UI，不需实现。截图不是本机运行证据，也不保证与固定commit同版；数据、颜色和名称可按本题素材调整。看不到的异常/恢复状态按下列合同实现，不能从截图推断隐藏业务规则。

- S01 `input/design/official-01.png`：阅读上层目录/书签菜单与下层字体排版设置；对应 R02, R04, R08, R09
- S02 `input/design/official-02.png`：正文选中后的词典/高亮操作弹层；不要求在线查词；对应 R03, R06, R10
- S03 `input/design/official-03.png`：实际EPUB连续阅读正文与底部进度；对应 R01, R04, R05, R11
- S04 `input/design/official-04.png`：Android文件浏览库与书籍条目进度；对应 R01, R05, R12

## 冻结业务契约

标为reference_documented的是官方页面明确展示的真实能力；synthetic_extension冻结测试数据、精确数值和恢复边界，不冒充原版内部协议或完整算法。

### R01 (synthetic_extension)

导入north和south两个同名field-guide.epub，按EPUB identifier与内容哈希区分，不按basename合并。显示内部title，目录含3章。使用成熟EPUB解析/排版库，必须加载文件内实际XHTML文字，不能用图片或硬编码段落代替。

### R02 (synthetic_extension)

支持目录跳转章节、翻页或滚动、书签与恢复阅读。稳定锚点至少包含book identifier、spine href、段落id和段内字符偏移；页码仅显示，不是唯一持久化地址。本题XHTML段落ID明确提供，允许采用库等价CFI。

### R03 (synthetic_extension)

长按正文选择连续文本并高亮，能调整选区边界、添加批注和从批注列表跳回。对于本题重复句，以章节/段落/偏移区分；高亮对象拥有稳定annotation_id，批注内容不改变引用文本。

### R04 (synthetic_extension)

字号18→26sp及横竖屏切换会重新排版；顶部阅读锚点或选中的高亮应保持在视区，允许行位置改变但不得跳到同页码的其他段。显示当前章节与进度；返回目录或批注页后可回原阅读上下文。

### R05 (synthetic_extension)

每本书独立保存位置、字号、书签和批注。切换到同名另一书不能继承第一书批注或进度；关闭书再打开按该书最后已保存锚点恢复。已导入文件保留私有副本，源URI失效不丢书。

### R06 (synthetic_extension)

创建/编辑批注成功后持久化；编辑取消保留旧批注；删除高亮仅删除目标，其他批注不动。force-stop后恢复书籍身份、锚点与批注，选区拖动未确认可丢弃。

### R07 (synthetic_extension)

导出annotations.json：每项book_id,annotation_id,href,paragraph_id,start_offset,end_offset,quote,note；offset为Unicode codepoint半开区间，在原段落文本中对应quote。书签另含book_id与同类锚点。排序book_id/href/paragraph_id/start_offset，重复导出不生成新批注。

### R08 (synthetic_extension)

离线工作，不要求在线词典/Wikipedia。截图的词典面板仅参考选区操作和弹层信息结构，实际提供高亮/批注/复制即可；目录、书签与阅读设置需有完整返回路径。

### R09 (reference_documented)

保留官方页面中可见的主要能力与信息层级：阅读上层目录/书签菜单与下层字体排版设置。截图只证明页面设计，不证明本题新增边界已实测。

### R10 (reference_documented)

保留官方页面中可见的主要能力与信息层级：正文选中后的词典/高亮操作弹层；不要求在线查词。截图只证明页面设计，不证明本题新增边界已实测。

### R11 (reference_documented)

保留官方页面中可见的主要能力与信息层级：实际EPUB连续阅读正文与底部进度。截图只证明页面设计，不证明本题新增边界已实测。

### R12 (reference_documented)

保留官方页面中可见的主要能力与信息层级：Android文件浏览库与书籍条目进度。截图只证明页面设计，不证明本题新增边界已实测。

## 输入与交付边界

两本EPUB均为本题原创英文文本，3章×20段，mimetype/OPF/nav/XHTML真实可解包；input/reading-plan.json指定阅读位置。原图是官方Android商店资料，含电子墨水风格界面，不要求模拟桌面应用。

作答模式固定为从空工程重建限定流程。repo/commit仅为构题侧来源；模型公开输入是Spec、截图和fixture，不提供原版源码或Git历史，不得直接打包或修改原版App作为答案。允许成熟通用组件与领域库。

操作控件必须有可访问名称，列表身份/计数/状态有可读语义。横竖屏与1.3字体不能遮挡核心按钮；旋转不得重复提交。禁止要求商业账号或生产数据；不将下载依赖失败或设备限制计为业务难度。导出文件通过系统选择器取得，不依赖候选包名、数据库或内部类名。

运行时功能需按任务书验证，不能只展示截图或硬编码终态；视觉评估看页面层次、主要组件和状态反馈，不要求复制商标或第三方版权媒体。所有输入夹具为本题原创或官方截图参考；原App截图中的电影、书籍、卡片内容不属于要求复制的训练素材。

当前仅完成题面、输入与静态来源核对。Android运行、参考实现、隐藏评测、模型试做和人工验收仍PENDING，不提供虚假的已通过比例。
