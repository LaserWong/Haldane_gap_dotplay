# 2026-10-14 有界证书复算

本目录保存本次实际运行的证据，原始日志与 JSON 保留原样。不是新的能隙发现，也不是全项目复现或完整 Stage38 发布。

## 复算命令

在仓库根目录运行（需要已安装 Python 3 与 NumPy，不会自动安装软件）：

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261014/readme_audit/replay/run_fresh_certificate_audit.py
```

脚本从自身位置推导仓库根目录，不依赖执行时的当前目录。每次创建新的 `rerun_时间戳/`，不覆盖 `fresh_results/` 或仓库历史审计输出。也可传入 `--repo-root 路径` 和新的 `--output-dir 路径`。不得使用 `python -O`，因为原核验程序使用断言。预计本环境约 9 秒，其他机器时间可能不同。无网络、安装、远端发布、删除操作。

## 输入与可移植性

[input_hashes.json](input_hashes.json) 列出全部 65 个输入文件的仓库相对路径、SHA-256 和 Git blob SHA。运行前逐一检查 SHA-256；缺失或变化则明确停止。

[current_main_input_identity.json](current_main_input_identity.json) 记录 2026-10-14 检查时 main 上这 65 个文件的 Git blob SHA，全数与实际复算的归档输入一致。包括两个独立核验器、扩展包的校验表及其 59 项、spin-1 证书及两个 Ritz NPZ。此证据不是整个 main 树的认证；后续 main 变化需重新核对。

便携入口已在字节相同的检查点输入上测试，见 [portable_wrapper_test.log](portable_wrapper_test.log)。未声称另建完整 main 工作副本并运行全部测试。

## 这次实际通过的内容

- spin-1 交替二聚体周期链，强键 1、弱键 1/20：M=2、4 的精确 Hamiltonian 作用、残差、全空间 Weyl/Temple 界、完整谱尾和六组温度递推；完整 Hilbert 维数分别 81、6561，每个输入保留一个试探向量。最佳已存证书下界 0.116303868802。
- 基线 625 维 Casimir 谱枚举、0 至 200 阶整数矩、惯性计数、β=1、2 热迹包络，以及通用标量下界 0.055688426272。
- 两份输入 ZIP 的 CRC、检查点清单 1,149 项及扩展包校验表 59 项全部匹配。ZIP 字节本目录不重复附带。

这是重新执行历史独立核验器。物理转移假设、全整数尺寸插值与短尺寸桥接未在这次重新人工审计；普通双层、大 D、完全受挫双层、均匀 spin-1 Appendix A、Stage38 和 g=.12 未在这次重算。准确边界见 [AUDIT_SCOPE.json](AUDIT_SCOPE.json)。

## 证据文件

- [archive_integrity.json](archive_integrity.json)：ZIP SHA-256、CRC 和条目数。
- [manifest_integrity.json](manifest_integrity.json)：每个清单条目的实际与期望 SHA-256。
- [fresh_results/baseline_verification.json](fresh_results/baseline_verification.json)、[spin-1 复算](fresh_results/certificate_s1_W1_g1d20_k0_audit.json)。
- [fresh_results/reproducible_replay.log](fresh_results/reproducible_replay.log)：原始成功日志。
- [fresh_results/run_environment.json](fresh_results/run_environment.json)：原始运行环境、源码哈希与耗时。

历史 JSON 和日志中的 `/workspace/...` 绝对路径是当时的来源与输出位置，不是仓库内可点击链接，也不是便携复算的依赖。它们按原样保留以便溯源；便携入口仅使用相对清单和自动推导的仓库根目录。
