更新时间：2026-10-10 13:46 EDT（纽约，UTC−4） / 2026-10-10 17:46 UTC

# Haldane_gap_dotplay

this is for gpt dot play with Haldane gap project

Haldane gap bootstrap 的研究检查点与任务状态。

**当前任务：研究已按用户 2026-10-10 13:14 EDT 的指示恢复。** 从 main 提交 `6be889a30f642bde77fb89af75b3a7379615bed1` 接续，先独立核验已有候选及有限尺寸桥接，再推进低激发带认证。用户确认截止时间为 **2026-10-13 20:00 America/New_York（EDT） / 2026-10-14 00:00 UTC**，届时保存检查点并停止科研计算。

**完成进度：** 已读取 GitHub 的 AGENTS.md、README 与各方向暂停记录，重新通过原检查点 1,149 项文件哈希核验。三组候选已完成独立精确算术核验及所有整数尺寸桥接。完整低激发带方法已在 g=0.03 完成独立认证。下一步推进更大二维种子、完整连续耦合区间及高自旋热迹优化。

**汇报安排：** 每 5 小时更新 GitHub 当前状态、下一步任务并向用户汇报，首次为 10 月 10 日 18:15 EDT，最后一轮常规汇报为 10 月 13 日 16:15 EDT，20:00 EDT 保存最终检查点。最新机器可读状态见 [CURRENT_STATUS.json](CURRENT_STATUS.json)，本轮计划见 [研究续接计划](research_20261010/PLAN.md)。历史 PAUSED 文件和 Release 记录 12:24 EDT 的固定快照，已由本次明确恢复指示接续，原文件保持可审计。

## 本轮新增核验结果（2026-10-10 13:46 EDT）

以下数值是能隙的严格下界，采用各证明指定的单位耦合与周期多重边约定。每一项均有唯一有限体积基态。

| 模型 | 参数 | 已独立核验的能隙下界 | 尺寸范围 |
| --- | --- | --- | --- |
| Spin-1 交替二聚体链 | g=0.1 | 0.118954972866 | 所有整数元胞数 M≥2 |
| 同上 | g=0.125 | 0.068202652189 | 所有整数 M≥2 |
| 同上 | g=0.15，深度 4 | 0.017013326349 | 所有整数 M≥2 |
| 同上 | g=0.16 | 0.004358246531 | 所有整数 M≥2 |
| 同上 | g=0.161 | 0.001952374069 | 所有整数 M≥2 |
| 同上 | g=0.16125 | 0.001075806295 | 所有整数 M≥2 |
| 普通 spin-1/2 方格双层 | g=0.01 | 0.168921021674 | 所有整数正方形边长 L≥2 |
| 同上 | g=0.02 | 0.057308457817 | 所有整数 L≥2 |
| 同上 | g=0.03，完整低激发带与数目扇区谱尾 | 0.009195338283 | 所有整数 L≥2 |
| 完全受挫双层附近 | J=0.3，直连 J+0.005，交叉 J | 0.038983227177 | 所有整数 L≥2 |
| 同上，单一乘积试探态 | 整个区间 0≤ε≤0.00475，直连 J+ε | 0.008090283176 | 所有整数 L≥2 |
| 同上，优化试探态 | ε=0.0085 | 0.001984903734 | 所有整数 L≥2 |

- [Spin-1 链完整证明与审计](research_20261010/chain_audit/CHAIN_CERTIFICATE_PROOF.md)：补齐 g=0.15 曾缺少的短尺寸范围，独立重建完整残差、局域正性、全谱尾及递推。
- [普通双层完整证明与审计](research_20261010/bilayer_audit/PROOF.md)：核验六组基态输入、24 个优化热迹节点与六条递推路径，补齐 g=0.02 的 L<16 范围。
- [非微扰参考点扰动完整证明与审计](research_20261010/nonperturbative_audit/BASELINE_PROOF.md)：核验占据数计数、加权星形界、局域正性、完整残差、热迹与所有短尺寸。
- [完整低激发带的独立核验](research_20261010/low_band_review/README.md)：普通双层 g=0.03 已通过。最大 32-spin 种子完整 Hilbert 维数为 2^32，认证保留基态及 48 个单 triplet 低态。基态采用 11 维对称试探空间，激发态使用分扇区稀疏表示。所有遗漏态由 triplet 数目压缩的精确 Jacobi 矩阵界计数，未求多体全谱。
- [更强链耦合及方法边界](research_20261010/chain_frontier_review/FRONTIER_PROOF.md)：g=0.16125 成功。g=0.1615 的特定 ground-only/dimer-tail 方法即使继续提高基态精度仍受阻，该结论不表示物理无隙。
- [非微扰参考点的连续扰动区间](research_20261010/nonperturbative_audit/EPSILON_FRONTIER.md)：一个乘积试探向量、完整非零残差与完整谱尾即可认证整个 ε 区间。[后续有限尺寸桥接](research_20261010/root_review/FF_FRONTIER_BRIDGE.md) 还补齐 ε=0.008 与 0.0085 的所有整数尺寸。
- [更强有限窗口插值](research_20261010/root_review/FINITE_WINDOW_INTERPOLATION.md)：用精确主谱权重界补齐递推到达小缺陷区之前的整数尺寸，已独立复核并用于上述 g=0.03 证明。
- [二维全部整数插值域扩展](research_20261010/root_review/INTERPOLATION_DOMAIN.md)：共同缺陷允许到 1/200，常数 32 保持不变，已获第二份独立复核。

这些结果不依赖最大种子的完整谱对角化。它们是指定模型与参数上的充分证书，不表示最大可认证耦合或实际能隙。后续扫描、低激发带及压缩基底结果在完成各自核验前保持候选状态。

## 直接浏览与继续工作

通常直接在 `main` 中阅读和使用本项目，无需先下载 ZIP。

- [检查点说明](README_先读.md)：完整科学状态、已核验结果与候选工作的边界
- [后续工作约定](AGENTS.md)：继续工作前先阅读，并结合本页任务队列与各目录暂停记录
- [独立审计](audit/)、[热迹计算](heat_trace/)、[低能试探空间](low_energy/)
- [二维理论](two_d_theory/)、[二维数值](two_d_numerics/)、[seed 分析](seed_size/)、[额外复核](root_review/)
- [暂停状态](PAUSED.json)、[原始文件哈希清单](MANIFEST_SHA256.json)、[运行环境记录](COMPUTE_ENVIRONMENT.json)

## 固定检查点备份

Release ZIP 保存本次暂停时的固定快照，便于归档与按 SHA-256 核对。本仓库中的展开文件是日常浏览和继续开发的主要入口。

- 文件：`Haldane_bootstrap_checkpoint_20261010.zip`
- 大小：6,073,351 字节
- SHA-256：`c4cced00e75e1f778ad1ff43e32d58c383aa1a821725794039ce2bdae61c1ea5`
- Release 标签：`checkpoint-2026-10-10`
- [Release 页面](https://github.com/LaserWong/Haldane_gap_dotplay/releases/tag/checkpoint-2026-10-10)
- [下载检查点 ZIP](https://github.com/LaserWong/Haldane_gap_dotplay/releases/download/checkpoint-2026-10-10/Haldane_bootstrap_checkpoint_20261010.zip)
- 发布于 2026-10-10 12:49:18 EDT / 16:49:18 UTC。私有仓库下载需使用已获授权的 GitHub 账号。

本页是该检查点的状态索引。以下技术结果和核验状态均依据 [README_先读.md](README_先读.md)，未因归档发布、源码导入或启动配置整理新增或升级结论。下文路径相对于仓库根目录，也对应 ZIP 解压后的检查点根目录。

## 固定检查点中的已完成结果

### 1. Spin-1 交替二聚体链：低能 seed

强键为 1，弱键为 0.05。仅保留一个最低态，结合精确残差与完整谱尾界，得到所有周期元胞数 **M≥2** 的能隙下界 **0.116303868802**。

证据入口：[low_energy/](low_energy/)、[audit/independent/certificate_s1_W1_g1d20_k0_audit.json](audit/independent/certificate_s1_W1_g1d20_k0_audit.json)。

### 2. 普通 spin-1/2 方格双层：真正二维的例子

竖直耦合为 1，两个面内方向的耦合均为 0.01。所有周期正方形边长 **L≥2** 的能隙下界为 **0.072950533962**。最大 seed 含 32 个自旋，完整 Hilbert 空间维数为 4,294,967,296，试探空间为 377 维。

证据入口：[audit/independent/bilayer_g001_audit.json](audit/independent/bilayer_g001_audit.json)。

### 3. 二维 spin-1 大 D 模型

D=1，两个方向的 Heisenberg 耦合均为 0.01。所有整数 **L≥2** 的正方形环面能隙下界为 **0.086452285325**。最大 seed 含 16 个 spin-1，完整 Hilbert 空间维数为 43,046,721，试探空间为 241 维。

证据入口：[audit/independent/largeD_g001_audit.json](audit/independent/largeD_g001_audit.json)。

### 4. 完全受挫双层：非微扰的一态例子

竖直耦合为 1，直连与交叉耦合均为 J。精确 singlet 乘积态只需一个试探态，残差为零。对全部周期矩形 **nx,ny≥2**，在 **0≤J<1/3** 时，最优族统一能隙为 **min(1,4−12J)**。

J=0.3 时，该族统一值为 **0.4**。正方形 **L≥3** 的实际能隙为 **1**。解析论证与独立小尺寸检验已完成，同一三纯度 bootstrap 也保存了可复算证书。

本模型含交叉耦合。其参数区间与能隙结论不可直接移用于第 2 项普通双层模型。

证据入口：[two_d_theory/NONPERTURBATIVE_MODELS.md](two_d_theory/NONPERTURBATIVE_MODELS.md)、[two_d_numerics/results/fully_frustrated_checks.json](two_d_numerics/results/fully_frustrated_checks.json)。

### 5. 原始均匀 spin-1 路线：复现与计算优化

已补齐并重新认证 Appendix A 的九个有限热迹输入，重建 D=26 MPS 的精确整数收缩，并复核矩、滤波、降温与 bootstrap 链。对周期链每个整数 **L≥1920**，得到能隙下界 **0.005908566393**。

标准计算 replay 保留原有偶数尺寸表述，覆盖全部整数尺寸的插值由独立审计文档补齐。此处复现的是已有档案中的路线及相应扩展，没有声称直接阅读缺失的原始 PDF。

证据入口：[heat_trace/appendix_a_replay.json](heat_trace/appendix_a_replay.json)、[heat_trace/PROOF.md](heat_trace/PROOF.md)、[audit/APPENDIX_A_BRIDGE.md](audit/APPENDIX_A_BRIDGE.md)。

### 6. 普通双层 g=0.03：当前认证方法的限制

在 g=0.03 时，当前指定的 **ground-only numerator 与独立二聚体谱尾界组合**，对所有温度与局域比较参数均无法通过现用递推。进一步收紧现有基态区间也不能解除这一障碍。

该结论限定上述认证方法的组合与递推，不能解释为物理相变边界。

证据入口：[audit/independent/majorant_g003_audit.json](audit/independent/majorant_g003_audit.json)。

## 三个新增问题的进展

1. **可认证耦合上限。** 已区分物理相变、试探态精度、完整谱尾估计与 seed 的空间纯度。完全受挫双层给出了可精确回答的非微扰区间，普通双层 g=0.03 的结果则定位了当前谱尾认证的限制。
2. **试探空间大小。** 完整激发壳层的线性维数为 Σ(j=0…q) C(M,j)[(2s+1)²−1]ʲ。已保存自适应支撑深度、残差与认证精度的比较。[root_review/trial_dimension_toy.json](root_review/trial_dimension_toy.json) 中的精确二项分布截断示例只说明可解模型的表示复杂度，不作为相互作用模型的证据。
3. **紧凑表示与完整认证。** 小线性空间、MPS 虚拟键维数与完整 Hilbert 空间维数分别计量不同对象。均匀 spin-1 路线中的 D=26 MPS 是紧凑变分态，其能量证书仍需与完整热迹认证结合。

## 已保存、待全面独立核验或继续研究

本轮核验已完成的条目在上方列明。以下区分已升级条目和仍在进行的工作。

- **Spin-1 二聚体链：** g=0.1 至 0.16125 的已列参数点已完成独立核验与所有整数尺寸桥接。方法边界与试探空间需求见新报告。
- **普通双层：** 优化后的 g=0.01、g=0.02 已完成独立核验与所有整数尺寸桥接。g=0.03 已通过完整低激发带及改进谱尾认证。g=0.04、0.05 当前小种子的有限温度网格未通过，保持诊断状态。
- **完全受挫双层附近的鲁棒性：** J=0.3、ε=0.005 及若干更大参数点已完成独立核验，整个 0≤ε≤0.00475 区间也已认证。连续区间与离散成功点分别记录。
- **其他方法工作：** 一般 d 维原推广已独立复核，二维常数 K=26 另有精确证明与第二次复核。更强一般 d 维常数、较大种子的压缩基底与 spin-2 Chebyshev 优化分别保留其具体核验状态。
- **Spin-2 计算：** 单列基准在暂停时中断，没有启动整夜或完整大系统计算。

各目录的 `PAUSE` / `PAUSED` 文件记录更细的完成状态、未核验部分与恢复入口。

## 仓库与任务状态

默认分支为 `main`。完整检查点已按原路径导入，原检查点文件与 `MANIFEST_SHA256.json` 保留。仓库另提供 `README.md`、`AGENTS.md`、`.gitignore` 与 `requirements.txt` 作为导航和继续工作的配置。检查点 Release 已发布，附件状态为 uploaded，大小和 GitHub 返回的 SHA-256 均与本地归档一致。

- [x] 保存截至暂停时的结果、源代码、检查点与所需参考依赖
- [x] 在归档说明中区分已独立核验结果、候选证书与未完成工作
- [x] 保存运行环境、文件哈希清单与可移植性修改记录
- [x] 发布仓库首页与 Release 说明
- [x] 将完整 ZIP 按原路径展开至 `main`，保留检查点文件与原始哈希清单
- [x] 提供 `AGENTS.md` 连续工作入口与最小 Python 启动配置
- [x] 发布 `checkpoint-2026-10-10` Release，上传 ZIP 并核验远端大小与 SHA-256
- [x] 完成上述三组已保存候选的独立核验及短尺寸桥接
- [ ] 扩大耦合、改进低激发带或谱尾认证，进行中
- [ ] spin-2 误差证明与成本评估后决定是否启动长计算，尚未启动

用户已明确恢复研究，授权持续计算与 GitHub 更新，截止 10 月 13 日纽约时间 20:00。任何后续暂停指示优先。

## 下一步任务记录（按优先级）

以下队列已恢复。优先完成已有候选的独立核验，再扩大计算范围。

1. **归档发布与源码导入已完成。** 完整检查点已展开至 `main`。Release ZIP 保留为固定快照，远端附件大小与 SHA-256 核验通过。继续工作时先阅读 `AGENTS.md`、本页任务队列与对应目录暂停记录。
2. **已有主要候选核验完成，后续改进继续逐项复核。** 较强 spin-1 链、普通双层至 g=0.03 与非微扰扰动证书已分别通过。优先审计更深标量递推、较大种子及连续参数区间，不重复已通过的物理输入。
3. **确定可认证耦合范围。** 分别诊断试探态残差、完整谱尾界和 seed 纯度的限制。普通双层 g=0.03 已通过完整低激发带与数目扇区谱尾。下一步针对 g=0.04、0.05 的小种子空间纯度瓶颈构造更大种子，避免仅增加小种子基态小数位。
4. **估计试探空间需求。** 小种子基态已实现 377→121→6 的对称性压缩与 11 向量改进。下一步为 4×8、8×8 种子计算更深精确矩与平移低激发带，记录完整残差、尾界、内存和运行时间。
5. **扩展非微扰参考点的连续区间。** 单一乘积试探态已认证 0≤ε≤0.00475；更宽区间需参数依赖的优化试探态及区间算术，不能由若干离散成功点插值推出。
6. **优化原始高自旋热迹计算。** 完成 spin-2 Chebyshev 误差证明与单列基准，在评估总耗时和内存后再决定长计算。保留流式检查点和独立核验入口。

扩展项目：独立核验一般 d 维定理与改进常数。它们不作为上述候选证书已完成的前提。

## 仓库文件结构

| 路径 | 内容 |
| --- | --- |
| [audit/](audit/) | 独立复核、物理假设、完整证明衔接与精确核验输出 |
| [heat_trace/](heat_trace/) | 流式整数热迹代码、检查点、九项热迹输入与原始路线 replay |
| [low_energy/](low_energy/) | 稀疏试探态、精确残差、局域比较、谱尾与候选证书 |
| [two_d_theory/](two_d_theory/) | 二维定理、整数尺寸插值、非微扰模型与文献 |
| [two_d_numerics/](two_d_numerics/) | 独立 Hamiltonian、精确交叉检查与浮点基准 |
| [seed_size/](seed_size/) | seed 排除、温度窗口、参数优化与谱尾上限 |
| [root_review/](root_review/) | 额外独立局域矩阵验证与试探空间复杂度示例 |
| [original/](original/)、[input/](input/) | 最初上传的扩展包与原样解压内容 |
| [upstream/extracted/](upstream/extracted/) | 复算所需的原始参考代码、标量程序与 spin-2 局域证书依赖 |

本检查点及其仓库展开内容没有再次复制约 196 MB 的完整历史档案 `HaldaneConjecture.zip`，也未复制其中无关的历史服务器日志。当前新计算结果、源代码、检查点与所需参考依赖均已保存。原始 ZIP 的 SHA-256 为 `f55ab851502759d863673f627bce28de1d040750f18f747a7814e866153425c8`。

## 环境准备

归档运行环境是 **Python 3.12.14**，详见 [COMPUTE_ENVIRONMENT.json](COMPUTE_ENVIRONMENT.json)。新增的 [requirements.txt](requirements.txt) 固定了该环境记录中的 NumPy 2.3.5、SciPy 1.17.0 和 SymPy 1.14.0，可在 Python 3.12 环境中作为最小启动配置使用：

```bash
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

`.gitignore` 仅排除常见缓存、虚拟环境和临时工作目录，不排除科学数据、结果或检查点。此处新增的是环境准备入口，原有科学审计状态保持不变。

整数 C++ 程序还需要 **C++ 编译器与 GMP**，它们不由 `requirements.txt` 安装。随包 Linux 二进制仅记录归档时环境，换平台时应从源代码编译，并参照对应目录 README。

## 完整性检查与复算入口

在仓库根目录或 ZIP 解压后的检查点根目录执行：

```bash
python verify_archive.py
```

该命令检查原始 `MANIFEST_SHA256.json` 中列出的归档文件哈希。仓库新增的首页、工作约定与启动配置未加入或改写这份原始清单。哈希一致只验证文件完整性，数学结论的依据见对应证明与审计文件。

已有原始路线证书的重放入口为：

```bash
python heat_trace/replay_appendix_a.py
```

部分审计脚本中的原执行环境绝对路径已改为包内相对路径，清单见 [PORTABILITY_PATCHES.json](PORTABILITY_PATCHES.json)。归档说明记录这些修改没有改变数学逻辑。各目录 README 提供重新计算与单项核验命令。本轮恢复后的新增材料放在 research_20261010/，固定检查点文件保留以便核对。

## 仍在推进的方向

- 更大二维种子的解析低阶矩与平移对称低激发带，控制内存和完整泄漏残差
- 已认证种子的更深标量递推及更好常数，后续数值须单独复核后升级
- spin-2 严格 Chebyshev 误差界、单列基准及整轮成本估计，尚未启动完整大规模热迹计算
- 将离散成功参数点扩展为完整连续区间，清楚区分方法充分条件与物理相边界
