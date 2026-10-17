# 来源与状态

参考：https://github.com/gsantner/markor

Commit：aff9492c55a1d0a09e3b11e603a0487678bb4f27。许可证文件为 LICENSE.txt，完整哈希记录见 ../../../evidence/sources-03/source-lock.json。

状态为 DRAFT，不是 Harbor Task 1.3 已验收包。尚未创建声称兼容的 task.toml；需要正式字段验证及完整环境、参考制品、评测器后再发布。

已验证：原版构建；单文档创建、保存、预览；force-stop 后重开与文件字节一致；文内搜索命中/不命中/清空且不改变正文。证据位于 ../../../evidence/markor-explore-03 至 23，以及 ../../../evidence/markor-search-workflow-01。

NB-03/04/06/09 只有部分证据，不能据此声称整个要求通过。其余全部待设备核验。此处的原版资源 ID 只用于探索，公开契约不要求它们。

后续设备证据补充：

- `markor-north-preview-01` 实际进入 survey-v03-01/north 并打开 observations.md。首次切换后的截图为空，报告中的控件 PASS 不证明渲染；见该目录 REVIEW.md。原始导入夹具另存 fixture-original。
- `markor-explore-26` 实际显示 North ridge、表格、强调、列表、任务项和 project index 链接。截图已查看，对应 NB-04 部分证据；代码区尚未滚动核验。
- `markor-relative-links-01` 揭示原版链接打开目标编辑器而非预览；错误等待条件导致 INVALID，失败记录保留。
- `markor-explore-27` 从 README 编辑器 BACK 实际返回 north 预览。
- `markor-relative-links-02` 四步、七条断言通过：north 的 ../README.md 链接进入 README 编辑器，切换首页预览，链接进入 south 的同名文件，再预览确认 Limestone / S-017 / S-018 文档。对应 NB-01、NB-05 部分证据，尚未验证修改后的同名文件隔离。

等待正文的 runner 负向检查：`workflow-control-missing-device-02` 为 INVALID，`workflow-control-false-assertion-01` 为 FAIL，均退出1。它们不是 App 错误变体，不计入至少3个错误实现的要求。

## 替换、历史与文件隔离

`markor-explore-28` 从 south 预览进入编辑器，正文与原始夹具一致。`markor-replace-history-01` 实际完成九步：打开搜索、清空旧查询、查询 S-017、打开替换、输入 S-117、全部替换、撤销、重做、保存。11条断言通过。

替换/撤销/重做每次均比较编辑器完整正文与独立期望文本，保留换行；最终用 adb 读取用户目录里的三个真实文件逐字节比较。south 的两个 S-017 均变为 S-117，撤销恢复全部原文，重做恢复修改；north 同名文件及 README 未改变。期望文件快照、哈希和实际读回文件均保存在 run 下。对应 NB-01、NB-07、NB-08 的部分业务证据；单次替换、正则边界、撤销分支及复杂进程恢复仍未验证。

`markor-post-replace-check-01` 使用新增整条工作流设备锁，复核编辑器及三份文件一致性通过。`workflow-control-device-lock-01` 在锁已占用时返回 INVALID，未执行动作。`workflow-control-document-mismatch-01` 故意与修改前文件比较，正确返回 FAIL。这些是 runner 自检，不是模型试跑或错误 App 变体。

`markor-render-after-edit-01` 两步5断言通过：关闭搜索不改变完整正文，切换预览后实际段落与表格均显示 S-117，数值4未改变，磁盘仍与完整期望文件一致。step-002/after.png 已实际查看，证明本次变更从编辑器、保存文件传播到预览。未据此推断所有 Markdown 元素或生命周期场景均正确。

复杂度假设：文件身份、编辑缓存、渲染、路径导航、查找替换历史、持久化共享同一组状态，局部实现正确仍可能在组合链路中失败。该假设尚无模型试跑或人工难度结论支撑。

夹具为本次新编写的调查样例，不来自公开 benchmark 测试。参考 App 源码、隐藏材料和上述管理员证据不能随 instruction.md 一起交给模型；当前目录本身不是沙箱隔离措施。
