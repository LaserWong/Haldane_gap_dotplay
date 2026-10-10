# 暂停检查点

2026-10-10 16:25 UTC。按用户要求暂停，不再启动研究或计算。

## 已完成并可打包

- THEORY.md。二维三纯度递推、两个自伴转移结构、全部整数正方形尺寸插值、GNS 极限范围、解析双层及 spin-1 大 D 例子、两个条带推断障碍。
- three_purity_certificate.py。纯 Python 标准库精确有理数指数、递推和能隙验收。
- bilayer_seed_certificate.json、spin_one_seed_certificate.json。保守解析启动证书。
- NONPERTURBATIVE_MODELS.md。全受挫双层 J=3/10 的一维精确试探空间及严格直接 gap，和同一三纯度框架的接入。
- fully_frustrated_bilayer.py、fully_frustrated_one_trial_n2.json、fully_frustrated_one_trial_n4.json。零残差精确 ground trial 与包含全部未保留谱的二项式尾界。
- PRIMARY_LITERATURE.md。已核验的原始 FF 和非 FF 方法对比。
- GENERAL_DIMENSION.md。一般 d 维推导，已提交独立复核。比二维专用常数更保守。打包时需标记一般 d 维部分的独立审计状态，不能继承二维部分的已复核结论。
- toy_checks.py、toy_checks.json。两个解析障碍的小尺寸浮点诊断。这些数值不参与能隙证明。

## 严格结论的必要条件

1. 三纯度证书要求两个空间方向均有精确的实自伴 Hilbert–Schmidt 热转移表示，对该方向所有整数尺寸至少为 2 成立。
2. 长度为 2 的周期方向使用重复周期键，不能去重为简单图。
3. 标准阶梯为 A=Z(2n,m)/Z(n,m)^2、B=Z(2n,2m)/Z(2n,m)^2、C=T(2n,2m)。顺序更新必须使用新缺陷。
4. 二维共同缺陷 u≤1/500 时，全部共同尺度矩形及全部整数正方形可用 gap≥log(1/(32u))/β。一个正方形种子未证明所有任意长宽比矩形。
5. 全受挫双层 H=Q+JΣT_r·T_s 与普通双层是不同 Hamiltonian。前者有同层及交叉层四条同强度边。J=.3 时 L≥3 正方形实际 gap=1，L=2 的实际 gap=.4，所有 L≥2 下确界 .4。三纯度给出的较弱数值下界另列，不能混淆。
6. 全受挫例子的试探维数 1 依赖精确 singlet 产品态及局域守恒。完整激发空间仍然指数大。

## 已推导、尚未实施的优化建议

以下内容仅为后续工作建议，不是本次可执行证书输入。

- 非对易弱键的匹配着色热迹界。通过 logTr exp 的凸性，若各颜色内部为产品元胞图上的匹配，可证明 logZ(H0+ΣV_c)≤χ^−1Σ_c logZ(H0+χV_c)。从而 D≤χβ²Σ_e width(v_e)²/8。双层可进一步使用精确四自旋匹配块的 partition function。尚未写入正式复算脚本或独立审计。
- 全受挫结构破坏测试采用同层 J+ε、交叉层 J。vacuum 的完整残差平方推导为 (3ε²/4)Σ_unique_edges multiplicity²。2×2、4×2、4×4 分别为 12ε²、18ε²、24ε²。等待独立物理矩阵比较，不把它写成已经完成的数值核验。
- SU(2) singlet 的至多两 triplet 试探空间维数为 1+binom(N,2)。普通 Mz=0 枚举会包含更多基向量。完整谱认证仍需要 residual 和尾界。
- 给 low-energy worker 的候选压缩公式未实施和独立核验。使用非归一化 |ij>=Σ_a |t_a(i)t_a(j)>，其 norm²=3，写 trial=c0|vac>+Σcij|ij>。令 r_ij=(ε/2)m_ij、K=J+ε/2，候选投影作用为 (Hc)_vac=3Σr_ijcij，(Hc)_ij=r_ijc0+[2−2K m_ij]cij+Σ_(k≠i,j)(r_ik c_kj+r_jk c_ik)。四 triplet 泄漏的三个配对幅度为 a_(ij)(kl)=r_ijc_kl+r_klc_ij，其 Gram 矩阵候选为对角 9、非对角 3。需在一致的 Cartesian triplet 相位约定下核验符号，再用于验收。

其他数值目录中的低能证书和结构破坏测试由相应工作分支负责，本文件不把它们的进行中结果当作已验收结果。
