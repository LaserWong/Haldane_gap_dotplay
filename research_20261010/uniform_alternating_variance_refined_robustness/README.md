# Variance-refined alternating-chain robustness

Refined variance bounds produce the four candidate intervals below. They require independent H², scalar, and interval review. Earlier accepted results remain unchanged.

For the periodic spin-one Hamiltonian H_M(g)=sum_j[h_(2j−1,2j)+g h_(2j,2j+1)] with designated exchange one, the new rows claim a unique ground state and the listed gap bounds for every integer M>=2 (physical L=2M).

| Gap | Closed g interval | eta radius |
|---|---|---|
| .020 | [4999249/5000751,5000751/4999249] | 751/5000000 |
| .015 | [9997911/10002089,10002089/9997911] | 2089/10000000 |
| .010 | [399901/400099,400099/399901] | 99/400000 |
| .005 | [399891/400109,400109/399891] | 109/400000 |

The widest interval is approximately [.9994551484720414,1.0005451485529806]. The only changed seed inputs are the variance-refined Gibbs effect bounds kappa32<=.0969 and kappa64<=.119. The same cell-16 initialization, original uniform thermal data and accepted length-specific finite bridge are retained.

All 37 integer-cell windows, four infinite tails and 56 finite bridges pass 400-place directed checks. The 36 exact candidate checkpoints retain 19 rejections. No floating-tail shortcut is used. This separately authorized scalar gate cost 24.955691278 CPU seconds including its parent, below 30. There was no retry or physical computation.
