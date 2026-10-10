# 非微扰、小试探空间的二维例子

2026-10-10。这里选择全受挫 spin-1/2 双层模型作为可立即复算的主例。结论依赖精确的梯级总自旋守恒，全程不作耦合展开。试探空间保持一维的原因是精确结构，不能据此推断一般强耦合模型也需要同样小的空间。

## 1. 与普通双层的参数区别

每个正方晶格元胞含两个 spin-1/2。定义

\[
P_r=\mathbf S_{r,1}\cdot\mathbf S_{r,2}+\frac34 I,
\quad \mathbf T_r=\mathbf S_{r,1}+\mathbf S_{r,2},
\quad Q=\sum_rP_r.
\]

P_r 为 triplet 投影，T_r²=2P_r。取

\[
H_J=Q+J\sum_{\langle r,s\rangle}\mathbf T_r\cdot\mathbf T_s.
\]

每条元胞间边包含四条系数均为 J 的 Heisenberg 耦合，包括两条同层键和两条交叉层键。普通双层只有同层键。因此这里的 J=0.3 与普通双层热迹证书中的 g=0.01 或 0.02 属于不同 Hamiltonian，不能当作同一模型参数区间的直接扩大。

该全受挫双层及其局域总自旋守恒是已有模型结构。可核验的原始文献为 J. Stapmanns et al., Physical Review Letters 121, 127201 (2018), Eq. (2)，[作者存档全文](https://perso.u-cergy.fr/~ahonecker/papers/ffb-final.pdf)，[arXiv:1805.11017](https://arxiv.org/abs/1805.11017)。下面的简短不等式和小尺寸约定在此独立推导，不把文献中的数值相变点当作严格能隙证明。

## 2. 精确一维试探空间

每个 P_r 都与 H_J 对易。所有梯级 singlet 的乘积 |Ω⟩ 满足

\[
P_r|\Omega\rangle=0,
\quad \mathbf T_r|\Omega\rangle=0,
\quad H_J|\Omega\rangle=0.
\]

因此采用 span{|Ω⟩} 的一维试探空间，能量及完整残差分别精确为 0 和 0，不随体积增长。物理自旋的 S^z 张量积基中，这一个向量有 2^N 个非零系数，但在梯级 singlet–triplet 基中恰为一个基向量。表示复杂度、试探向量数和完整激发空间维数需要分别报告。

在含 q 个 triplet 的扇区中，Hamiltonian 是被占据元胞图上的相互作用 spin-1 模型，维数为 3^q。同一占据图内的相邻 Heisenberg 项一般不对易。因此完整激发谱没有缩成一维。

## 3. 星形算符给出的统一界

先考虑每个空间方向长度至少为 3 的周期矩形，每个元胞有四个不同邻居。在 P_r=1 扇区，中央总自旋为 1，四个邻居的总自旋 S 至多为 4。角动量相加给

\[
\mathbf T_r\cdot\sum_{s\sim r}\mathbf T_s\ge-5P_r.
\]

邻居总自旋为 S≥1 时最小值为 −(S+1)，S=0 时为 0。将星形不等式求和，每条边被计数两次，得到

\[
H_J\ge\left(1-\frac52J\right)Q.
\]

因此 0≤J<2/5 时，全部这类有限体积都具有唯一 singlet 乘积基态，统一正隙至少为 1−5J/2。这个区间来自精确角动量界，没有使用微扰级数。它是充分区间，不是物理相边界。

### J=3/10 时的精确 gap

在 q≥4 的扇区中，上式给 E≥q/4≥1。q=1 时能量精确为 1。q=2 时至多有一条被占据边，故 E≥2−2J=1.4。q=3 时简单图至多有三条边，每条 T_r·T_s≥−2，故 E≥3−6J=1.2。

因此在每个边长至少为 3 的周期矩形上，尤其在每个整数正方形 L≥3 上，

\[
\Delta=1\quad\text{at }J=3/10.
\]

孤立 triplet 态达到该能量，所以这不只是下界。同一个证明覆盖 0≤J≤3/10。

## 4. 长度 2 的多重边必须单独检查

为保持精确热转移表示，长度为 2 的周期方向保留两个邻接项。2×2 元胞图因此是带双重边的四环。把相对顶点分为 A、B 两组，则

\[
H_J=Q+2J\mathbf T_A\cdot\mathbf T_B.
\]

若两组各有 q_A、q_B 个 triplet，总自旋分别至多为 q_A、q_B。最大反铁磁能量降低为

\[
2J\min(q_A,q_B)\,[\max(q_A,q_B)+1].
\]

对 q_A,q_B∈{0,1,2} 枚举，全部非空扇区的最小能量为

\[
\Delta_{2,2}
=\min\{1,\,2-4J,\,3-6J,\,4-12J\},
\quad 0\le J<1/3.
\]

在 J=3/10 时它等于 2/5。结合前节，全部整数正方形 L≥2 的能隙下确界恰为 2/5，而 L≥3 的实际有限体积隙均为 1。

J=1/3 时，2×2 全 triplet 扇区中的一个 singlet 与 |Ω⟩ 简并。因此若要求把该多重边 L=2 也纳入“唯一 singlet 基态”的模型族，其允许 J 区间确实必须在 1/3 前终止。这个有限体积限制不同于无限平面物理相变。

## 5. 所有种子几何上的谱尾界

简单而统一的矩形界来自 plaquette。四环的相对顶点总自旋记为 T_A、T_B，环上四条边之和 K=T_A·T_B。对所有 singlet/triplet 占据，角动量枚举给

\[
K\ge-\frac32\sum_{r\in\square}P_r.
\]

把所有周期 plaquette 相加，每条边出现两次，每个元胞出现四次，得到

\[
H_J\ge(1-3J)Q.
\]

该不等式包含长度为 2 的重复边约定。因此 J=3/10 的所有启动矩形均可使用 γ=1/10。若各边至少为 3，可改用星形界 γ=1/4。

q-triplet 扇区的总维数为 binom(N,q)3^q，且能量至少为 γq。因此全部未保留谱都有明确的二项式尾界

\[
1\le Z_N(\beta)\le\sum_{q=0}^N\binom Nq3^qe^{-\beta\gamma q}
=(1+3e^{-\beta\gamma})^N.
\]

这里没有计算任何完整多体谱，也没有丢弃非零残差或未计数的简并态。

## 6. 接入同一个三纯度框架

梯级联合时间反演平方为 +1，所以可选取 T_r=iA_r 的实结构。跨元胞 −J T_r·T_s 的同因子实张量展开满足 THEORY.md 的两个方向自伴热转移条件。

记 z=1+3e^{-βγ}、N=nm，则

\[
A\ge z^{-2N},\quad B\ge z^{-4N},\quad C\ge z^{-8N}.
\]

用 n=m=2、β=120、γ=1/10，全部有理数下界直接进入三纯度的小缺陷区域，给出每个整数正方形 L≥2 的 bootstrap 能隙下界

\[
\Delta_L\ge0.033085166891.
\]

最大启动几何含 16 个梯级、32 个物理自旋，完整 Hilbert 空间维数为 4,294,967,296。实际保留的试探空间仍只有一个精确向量。

改用 n=m=4、β=80、γ=1/4，得到 L≥4 上的 bootstrap 下界 0.132295274293。最大启动几何虽有 128 个物理自旋，其尾界仍只是二项式表达式。

该模型的直接局域不等式已经给出更强的 gap。这里接入三纯度的价值是严格验证同一热迹框架可以处理没有耦合展开的非对易模型，并展示如何把精确结构压缩成极小的谱输入。它不意味着 thermal bootstrap 在这个特殊模型上优于直接角动量证明。

代码 fully_frustrated_bilayer.py 和两个 fully_frustrated_one_trial_n*.json 提供全有理数复算。

## 7. 破坏精确结构后的灵敏度测试

当前数值测试约定为同层耦合 J+ε、交叉耦合 J。设 D_r=S_(r,1)−S_(r,2)，则边相互作用为

\[
\left(J+\frac\epsilon2\right)\mathbf T_r\cdot\mathbf T_s
+\frac\epsilon2\mathbf D_r\cdot\mathbf D_s.
\]

第二项可以从两个 singlet 产生一对 triplet，局域 P_r 守恒随之破坏。ε≠0 后原先的一维基态试探空间一般有非零残差。测试应报告完整残差、热迹认证区间和所需支持数如何随 ε 增长，而不是把 ε=0 的一维精确空间沿用为一般结论。

两个方向的热转移结构仍可检查。层指标耦合矩阵的本征值为 2J+ε 和 ε。ε≥0 时，它可用 T、D 的正系数同因子分解，所以目前选择的小正 ε 测试保持转移条件。

## 8. 其他候选及其用途

AKLT/MPS 父 Hamiltonian 具有有限维虚拟表示，但固定 bond dimension 不等于其 S^z 基中的有限支持，更不等于用一两个普通向量就能认证整个正激发谱。其 frustration-free 有限尺寸或局域正算符分解证书往往比纯度路线更合适。

Shastry–Sutherland 型正交二聚体也有精确 singlet 乘积基态区间，可作为下一类结构压缩候选。但必须分别证明热谱尾和两个方向自伴转移。本次已经完成的非微扰主例是上面明确定义的全受挫双层，不把这些其他模型列成已完成证书。

可进一步核验的两项原始来源为 B. S. Shastry and B. Sutherland, “Exact ground state of a quantum mechanical antiferromagnet,” Physica B+C 108, 1069–1070 (1981)，[作者论文存档](https://physics.ucsc.edu/~sriram/papers/paper_19.pdf)，以及 V. Karimipour and L. Memarzadeh, “Matrix product representations for all valence bond states,” Physical Review B 77, 094416 (2008)，[期刊论文](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.77.094416)。前者的完整 PDF 当前获取失败，搜索中可核验其三角形分解与精确二聚体基态内容，因此本报告未用它的未读细节建立新的 SS 数值证书。

## 9. 独立小尺寸诊断

独立数值检查已在 J=0.3 的 2×2 梯级环面确认唯一基态、精确乘积态零残差及浮点能隙 0.4。在 4×2 梯级矩形上，完整占据数及 S^z 分块计算得到能隙 0.8，物理空间维数为 65,536，最大稠密分块维数为 1,107。另在 2×2 上检查 J=1/3 时基态简并数变为 2，J=0.35 时原 singlet 乘积态已不是基态。

相关浮点谱和局域星形、plaquette 矩阵检查由独立数值目录保存。它们作为解析构造的诊断，不替代本报告角动量不等式及有理数热迹尾的证明。没有对 4×4 梯级体系运行完整物理谱对角化。
