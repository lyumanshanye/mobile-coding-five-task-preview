# MCP-011 操作任务书

每条独立轨迹从清数据/导入原始夹具开始，除非明确写同链。固定业务日期/时钟见input，不取设备真实今日。控件定位从新鲜UI树获取，不用截图中的固定像素。

## T01 继承标签与移动撤销

初态：导入mission.org，Work due初始battery/sensors两项。

动作与中间态：展开Work，长按sensors移到Personal；搜索中sensors消失，仅battery；同名home-sensors不能被误动；撤销移动。

终态：sensors回Work，查询恢复两项且正文一致。

恢复/重置：退出重启，折叠/层级按保存状态恢复；独立测试清数据重导。

视觉证据：S02树、S04结果和S03详情各截图一次，展示ID/面包屑。

## T02 重复完成与撤销

初态：固定今日1月15日，battery计划15日。

动作与中间态：在Agenda完成battery，日期变16日且仍TODO，历史1条；撤销，回15日历史0；再完成一次。

终态：battery16日、历史恰1条、查询仍两项。

恢复/重置：force-stop重启后日期与历史不重复。

视觉证据：S05完成前/后分组、S03日期与history.json。

## T03 跨页编辑和取消

初态：sensors仍在Work。

动作与中间态：从Work due进入sensors详情，把局部tag改lab并保存；再编辑标题为Discard但取消。

终态：原标题Pack sensors；有效标签work/lab；field已移除；home-sensors不变。

恢复/重置：返回保持Work due上下文，再重启检查。

视觉证据：S03保存/取消、S02同名节点和S04面包屑。

## T04 结构拒绝与文件往返

初态：从原始输入开始。

动作与中间态：尝试把Work移到其后代battery，应拒绝且树不变；导出Org并清数据后重新导入。

终态：ID集合6个、层级/正文/日期保持；Work due仍battery/sensors。

恢复/重置：恢复以导出文件为唯一输入，不能缓存旧数据库。

视觉证据：S01导入入口、S02树、导出文本及S05日程。

