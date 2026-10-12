更新时间：2026-10-11 23:31:18 EDT（纽约） / 2026-10-12 03:31:18 UTC

# Haldane_gap_dotplay — PAUSED

研究已按用户要求暂停。上传保存当前仍可恢复的最新文件后停止；没有新研究运行，恢复必须有用户新的明确指示。两个研究自动任务均已停用。

## 本次保存范围与限制

本提交是**恢复保存检查点，不是完整 Stage38 源码发布**。原工作区的完整冻结副本现不可用；原计划中6,617个尚未上传的普通文本内容、532个文本批次未能完整恢复。已有部分文件从上传对象精确恢复，因此6,617是原始未上传数量，不能当作当前剩余缺失文件的精确数量。

[恢复目录与文件说明](recovery_20261012/README.md)保存全部700个已确认上传的项目对象，防止孤立对象丢失。其中原最终快照曾核验693个相关对象；另7个是上传的历史或替代对象，当前不能重新确定完整的693子集映射。原对象字节按Git SHA保留，不假称已恢复全部原路径。

- [最新可恢复 README](recovery_20261012/latest_recovered_roots/README.md)、[状态](recovery_20261012/latest_recovered_roots/CURRENT_STATUS.json)、[计划](recovery_20261012/latest_recovered_roots/research_20261010/PLAN.md)逐字节恢复；这些历史文件中的链接可能指向尚未恢复的文件。
- 原main科学文件继续保留在已验证的Stage22提交[`d17eadfb655c35eb325245d8660737b761db6b28`](https://github.com/LaserWong/Haldane_gap_dotplay/commit/d17eadfb655c35eb325245d8660737b761db6b28)所对应路径；本次不以残缺新文件覆盖它们。
- [原Stage22 README](recovery_20261012/baseline_stage22_roots/README.md)保留既有研究说明；[模型与归一化](research_20261010/MODELS_AND_NORMALIZATION.md)继续适用。
- 最新恢复记录包含固定准备H³/Ritz验收，但g=.12 bootstrap replay仍为NOTRUN，**没有新的.12 gap证书**。不宣称完整Stage38复现材料已恢复。
- 大型对象、路径映射、上传回执与精确恢复的materializer源码见恢复目录。其完整配套清单尚未全部恢复，不能直接把源码存在当成完整可运行复现包。

当前暂停与恢复状态以[CURRENT_STATUS.json](CURRENT_STATUS.json)为准，覆盖历史计划中的启动和报告安排。
