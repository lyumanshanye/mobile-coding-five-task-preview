# 来源与缺口

仓库 https://github.com/iSoron/uhabits；commit 7e993e17b2b674d4b5b1291ebd18677b74810df2；许可证 LICENSE.txt。实际构建证据 loop-build-02，离线批量构建证据 batch-offline-01。

已阅读 README.md 的 flexible schedules、habit score、CSV/SQLite export，以及 CHANGELOG.md 的 numeric habits、at most、skips、exported notes 条目。这些证明来源具有对应功能，不证明本机任务链路或算法已通过。

状态 DRAFT。缺少原版设备探索、精确统计公式与算例、完整状态转换、设计图、输入历史、环境生命周期、隐藏评测、Golden三次、错误变体、多模型和独立人工评分。公式缺失前禁止冻结题面，否则会成为要求模型猜测算法的题。

设备探索已开始：loop-explore-01 在API28安装并启动，真实进入Welcome；loop-explore-02 点击SKIP进入空习惯列表。尚未验证任何历史或统计链路。Score.kt、ScoreList.kt、Entry.kt 的源码规则调查见 statistics-investigation.md，不冒充设备验证或独立评测。

loop-explore-03 实际出现Yes or No/Measurable类型选择，04进入数值习惯表单，默认Every day/At least/Reminder Off。当前没有保存新习惯。
