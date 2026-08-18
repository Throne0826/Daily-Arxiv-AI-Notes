---
title: "[论文解读] More Correct Mass, Worse Answers: Why Power Sampling Can Fail and How to Fix It"
description: "[arXiv 2608.14420][LLM Reasoning] 本文揭示了一个反直觉现象：Power Sampling 即使提高正确推理轨迹的总概率，也可能因破坏答案聚合所需的支持结构而降低最终准确率，并据此提出按题目校准、保留中等概率路径的 Relative-Rank SoftSat。"
arxiv_id: "2608.14420"
announcement_date: "2026-08-17"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-18T02:02:56.379819+00:00"
source_sha256: "fc970d9bfd718ed6044af0ee3b66619600fce0e87f0c62233bf1e5b1ffddc775"
tags:
  - "LLM Reasoning"
  - "测试时计算扩展"
  - "Power Sampling"
  - "完整轨迹分布"
  - "Self-Consistency"
  - "多轨迹聚合"
  - "答案概率质量"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.14420</p>

# More Correct Mass, Worse Answers: Why Power Sampling Can Fail and How to Fix It

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Haohui Yang, Jiaxing Sun, Xiujun Ma</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: [0.4em] State Key Laboratory of General Artificial Intelligence, Peking University, Beijing, China；State Key Laboratory of General Artificial Intelligence, Peking University, Beijing, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14420) · [PDF 下载](https://arxiv.org/pdf/2608.14420) · **关键词** 测试时计算扩展, Power Sampling, 完整轨迹分布, Self-Consistency, 多轨迹聚合, 答案概率质量<br>


</div>

<nav class="paper-jump" aria-label="论文解读章节">
  <a href="#研究背景"><span>01</span>研究背景</a>
  <a href="#研究动机"><span>02</span>研究动机</a>
  <a href="#研究方法"><span>03</span>研究方法</a>
  <a href="#实验"><span>04</span>实验结果</a>
</nav>

<div class="paper-quickread" markdown="1">

<div class="paper-quickread__main" markdown="1">

<span class="paper-mini-label">先用一句话判断</span>

本文揭示了一个反直觉现象：Power Sampling 即使提高正确推理轨迹的总概率，也可能因破坏答案聚合所需的支持结构而降低最终准确率，并据此提出按题目校准、保留中等概率路径的 Relative-Rank SoftSat。

**不用术语来说**：多次采样推理并不是只要找到一条正确思路就够了：自一致性等方法要统计多条思路最终支持哪个答案。如果采样分布被过度“变尖”，某条概率最高但答案错误的思路可能压倒多条各自概率稍低、却共同支持正确答案的思路。因此，增加正确思路的总体概率，不一定能让最终投票更正确。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者发现并系统归因了 Power Sampling 与下游多轨迹决策之间的失配：覆盖失配使概率集中到少数强势轨迹，剂量失配则使同一指数 $\alpha$ 在不同题目上造成程度悬殊的分布变形。
- 作者提出 Relative-Rank SoftSat：用题目内部的相对秩坐标替代原始似然来校准重加权强度，并让高排名轨迹的增益逐渐饱和，以避免少数路径吸收过多概率；同时通过共享基础候选池上的重要性加权聚合实现同预算推理。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的测试时计算扩展研究：模型参数保持不变，在推理阶段生成多条完整推理轨迹，再通过聚合、选择或验证得到最终答案。论文关注这一流程的上游采样分布：基础模型按自回归分布 $p(\tau)$ 生成轨迹；Power Sampling 则在完整轨迹层面构造与 $p(\tau)^\alpha$ 成比例的锐化分布，使模型原本认为更可能的轨迹获得更大权重。下游以自一致性为代表，它不只依赖单条高质量轨迹，还依赖多条轨迹对同一答案形成的集体支持，因此“提高正确轨迹的总概率”与“提高有限样本聚合后的答案准确率”并非同一个目标。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**完整生成轨迹与自回归概率**

完整生成轨迹 $\tau=(\tau_1,\ldots,\tau_T)$ 是模型从第一个 token 到终止位置生成的整个响应或推理过程。其概率 $p(\tau)$ 等于各位置条件概率 $p(\tau_t\mid\tau_{<t})$ 的乘积，因而同时受到每一步生成选择的影响。

</div>
<div class="concept-item" markdown="1">

**Power Sampling（幂采样）**

Power Sampling 将完整轨迹的基础概率提升到幂次 $\alpha>1$，并归一化为目标分布 $q_\alpha(\tau)=p(\tau)^\alpha/Z_\alpha$。直观上，它会放大高概率轨迹与中低概率轨迹之间的差距，但不同于逐 token 调低温度，因为后者会在每个生成前缀处单独归一化。

</div>
<div class="concept-item" markdown="1">

**Self-Consistency（自一致性）**

自一致性从同一提示独立采样 $N$ 条轨迹，提取每条轨迹的答案，并选择出现次数最多的答案。它利用的是答案层面的集体支持，因此多条不同推理路径可以共同支持同一个答案。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个提示和基础语言模型，模型在完整轨迹空间上定义分布 $p(\tau)$；每条轨迹经答案提取函数 $A(\tau)$ 映射为规范化答案，并可由指示量 $R(\tau)\in\{0,1\}$ 标记是否正确。上游可以直接按 $p$ 采样，也可以按理想 Power 目标 $q_\alpha$ 采样；论文明确区分该理想目标与 Power-SMC 使用有限粒子近似时产生的误差。下游获得 $N$ 条独立轨迹后，以自一致性等规则汇总答案支持并输出单个最终答案；其中 $N$ 是下游候选轨迹数，而 Power-SMC 的内部粒子数 $M$ 是近似采样所用计算量，两者不能混淆。核心分析对象是分布变换对两个层面的不同影响：$C_\mu$ 衡量分布 $\mu$ 下正确轨迹的总概率质量，$Q_\mu(a)$ 衡量答案 $a$ 获得的总概率质量，而有限样本聚合的成败还取决于这些质量如何分散在不同答案与推理路径之间。在唯一标准答案 $a^\star$ 的任务中有 $C_\mu=Q_\mu(a^\star)$；代码等任务则可能通过执行结果判定正确性，而不是比较规范答案字符串。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\tau=(\tau_1,\ldots,\tau_T)$**

长度为 $T$ 的完整生成轨迹，其中 $\tau_t$ 是第 $t$ 个生成 token。

</div>
<div class="notation-item" markdown="1">

**$p(\tau)$**

基础语言模型赋予完整轨迹 $\tau$ 的自回归概率。

</div>
<div class="notation-item" markdown="1">

**$q_\alpha(\tau)$**

指数为 $\alpha>1$ 的理想 Power 目标分布，与 $p(\tau)^\alpha$ 成比例。

</div>
<div class="notation-item" markdown="1">

**$Q_\mu(a)$**

从轨迹分布 $\mu$ 采样时，答案提取结果等于 $a$ 的概率，即答案 $a$ 获得的总支持质量。

</div>

</div>

**直接相关的工作**

- **Self-Consistency（SC）**: 本文采用的代表性多轨迹聚合方法：它对独立采样轨迹的规范化答案进行多数表决，用于研究上游分布锐化是否真正改善下游共识决策。
- **Power-SMC**: 使用 $M$ 个粒子近似完整轨迹级 Power 目标的采样方法，使 Power Sampling 可用于大规模语言模型；本文以理想分布 $q_\alpha$ 为理论参照，并将目标分布本身的性质与有限 $M$ 带来的近似误差分开讨论。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

测试时扩展常通过生成多条完整推理轨迹，再用验证、选择或答案聚合获得最终结果。Power Sampling 无需额外验证器或训练，理论上可作为这类方法的通用前端；但实际组合中，固定指数的 Power 重加权在九个模型与基准组合中的七个造成性能下降，最大降幅达到 18.5 个百分点。这说明上游采样分布即使偏向模型认为更可能的轨迹，也未必适合下游的集体决策规则。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **重复采样与自一致性**：从基础语言模型分布独立生成多条推理轨迹，并按最终答案获得的样本支持度进行聚合；Self-Consistency 通常选择获得最多轨迹支持的答案。它利用的是多条路径在答案层面的集体证据，而非单条最优轨迹。
- **Power Sampling**：给定完整轨迹分布 $p$，以与 $p^{\alpha}$ 成比例的目标分布进行采样，其中 $\alpha>1$ 会放大高概率轨迹相对低概率轨迹的优势。Scalable Power Sampling 和 Power-SMC 等方法降低了近似这一序列级目标的成本，使其能够用于大规模测试时推理。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 覆盖失配：Power Sampling 在轨迹层面分别强化高概率路径，而自一致性在答案层面汇总多条路径。若一条高概率错误轨迹与多条中等概率正确轨迹竞争，指数化会放大前者的个体优势、压低后者的联合支持，最终可能翻转聚合答案。即使较高的 $pass@k$ 表明正确轨迹仍可被采到，也不能证明聚合、搜索或选择所需的广泛支持仍被保留。
- 剂量失配：固定指数 $\alpha$ 只保证各题采用相同的代数变换，却不保证分布改变幅度相同。不同题目的轨迹似然间距不同，因此同一个 $\alpha$ 可能对某题仅轻微调整，对另一题却造成近乎坍缩的集中化，使效果跨题目和模型高度不稳定。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究主要解决如何高效逼近序列级 Power 目标，却缺少一种面向下游多轨迹决策的分布整形原则：它既要在不同题目之间提供可比较、可控制的锐化强度，又要避免消除中等概率轨迹在答案层面的集体支持，并且能够在不增加基础候选生成预算的情况下落地。

</div>
<div markdown="1"><span>核心问题</span>

如何设计并实现一种替代全局 $p^{\alpha}$ 锐化的目标分布，使其仍优先考虑较强轨迹，同时控制每道题的分布变形程度、保留多样推理路径对答案聚合的有效支持，从而避免“正确轨迹概率增加但最终答案变差”的悖论？

</div>
<div markdown="1"><span>作者直觉</span>

原始似然的尺度因题而异，而题内相对排名提供统一的 $[0,1]$ 坐标，因此按相对秩分配增益更容易让不同题目承受相近的重加权强度。在此基础上，让增益在顶部逐渐饱和，可以继续提升较强和中等排名轨迹，却不让最强的少数轨迹无限拉开差距。直观上，这相当于提高优质候选的影响力，同时保留多条彼此独立、可能共同支持正确答案的“选票”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把“从完整轨迹分布中进行幂采样”改写成“对同一批基础模型样本加权后再做共识决策”。给定提示词 $x$，首先从基础模型 $p_\theta(\cdot\mid x)$ 一次性生成 $N$ 条完整轨迹，并记录各轨迹的序列对数似然；随后不直接使用跨问题不可比的绝对对数似然，而是在当前问题的样本池内将其转换为相对秩。方法再通过 Relative-Rank SoftSat 为不同秩分配有界、饱和的增益，经过均值归一化和裁剪得到候选权重，最后将这些权重送入加权 Self-Consistency 或加权 ModeX，输出共识答案。

技术上，相对秩解决“剂量不匹配”：同一权重参数不再因不同问题的似然尺度差异而产生悬殊的分布变形；SoftSat 的先提升、后饱和形状解决“覆盖不匹配”：它增强中高似然候选，但避免权重持续随似然上升而被极少数最高似然轨迹垄断。直观地说，该方法不是认定“模型越自信的答案越应无限加分”，而是先看一条回答在本题候选中的名次，再给予封顶的加分，从而兼顾高质量候选与答案覆盖。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成基础轨迹池

独立采样 $\tau_{1:N}\sim p_\theta(\cdot\mid x)$，并计算每条完整轨迹的序列对数似然 $\ell(\tau_i)$；轨迹可以包含推理过程与最终回答。

<div class="method-step__io" markdown="1">

**输入**：提示词 $x$、基础模型 $p_\theta$ 和推理预算 $N$。<br>
**输出**：包含 $N$ 条轨迹、对应对数似然及可提取答案的候选池。

</div>

**直观理解**：先让模型按原分布给出固定数量的完整解答，并保存模型对每个解答整体上有多大把握。后续步骤只重用这批解答，不再调用模型生成额外样本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算问题内相对秩

将每条轨迹的绝对似然替换为经验分位秩 $\widehat{u}_i=N^{-1}\sum_k\mathbf{1}\{\ell(\tau_k)\leq\ell(\tau_i)\}$，使其位于 $[0,1]$。该坐标只保留同一问题内部的似然次序，而不使用不同问题之间不可比的数值间隔。

<div class="method-step__io" markdown="1">

**输入**：当前提示词下候选池的对数似然 $\ell(\tau_{1:N})$。<br>
**输出**：每条候选的相对秩 $\widehat{u}_{1:N}$。

</div>

**直观理解**：不比较不同题目的原始“信心分数”，只判断某个回答在本题候选中排在什么位置。这样，同一组超参数在不同问题上表达的是近似相同的加权强度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### SoftSat 塑形与有界重加权

先用 $\operatorname{SoftSat}_m$ 将秩映射为饱和增益，再指数化并以偏移量 $c$ 调整为均值一，最后裁剪到 $[1-\eta,1+\kappa\eta]$，得到乘子 $\widetilde r_i$；归一化为 $W_i=\widetilde r_i/\sum_j\widetilde r_j$。

<div class="method-step__io" markdown="1">

**输入**：相对秩 $\widehat{u}_{1:N}$ 以及参数 $(m,\beta,\eta,\kappa)$。<br>
**输出**：非负、归一化且影响幅度受控的候选权重 $W_{1:N}$。

</div>

**直观理解**：中等及较高排名的候选会获得额外支持，但排名超过阈值 $m$ 后加分停止增长；裁剪进一步防止单条回答获得过大话语权。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务适配的加权共识

答案字符串可规范化的任务采用加权 Self-Consistency，汇总产生同一答案的轨迹权重；自由形式或可执行输出则把相同权重贯穿 ModeX 的响应相似图读出过程。

<div class="method-step__io" markdown="1">

**输入**：轨迹池 $\tau_{1:N}$、候选权重 $W_{1:N}$ 与共识读出器 $\mathcal D$。<br>
**输出**：最终共识输出 $\widehat y=\mathcal D(\tau_{1:N},W_{1:N})$。

</div>

**直观理解**：普通多数投票把每个候选视为一票，该方法则让问题内排名较高但不过度集中的候选拥有较大票重。若所有权重相同，流程就退化为原始 Self-Consistency 或 ModeX。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 相对秩 SoftSat 目标分布

$$
u_p(\tau)=\Pr_{X\sim p}\!\left[\ell(X)\leq\ell(\tau)\right],\qquad \operatorname{SoftSat}_{m}(u)=1-\left(1-\min\left\{\frac{u}{m},1\right\}\right)^2,\qquad r_{\beta,m}(\tau)=\exp\!\left[\beta\operatorname{SoftSat}_{m}\!\left(u_p(\tau)\right)\right],\qquad q_{\beta,m}(\tau)\propto p(\tau)r_{\beta,m}(\tau)
$$

**符号说明**

- $\tau$：基础模型生成的一条完整轨迹。
- $p$：给定当前提示词时基础模型在完整轨迹上的概率分布。
- $X$：从基础轨迹分布中抽取的随机轨迹，用于定义分位秩。
- $\ell(\tau)$：轨迹的基础模型序列对数似然，即各生成位置条件对数概率之和。
- $u_p(\tau)$：轨迹在当前问题基础分布内的似然分位秩，取值属于区间 $[0,1]$。
- $\operatorname{SoftSat}_{m}(u)$：将相对秩转换为平滑饱和增益的函数，输出位于 $[0,1]$。
- $m$：饱和阈值，满足 $0<m\leq1$；当相对秩达到 $m$ 后增益不再增加。
- $\beta$：SoftSat 增益的指数缩放系数，控制重加权强度。
- $r_{\beta,m}(\tau)$：施加给轨迹的未归一化重要性乘子。
- $q_{\beta,m}(\tau)$：由基础分布和 SoftSat 乘子共同定义的新轨迹目标分布。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先把原始序列似然变成问题内部的百分位位置，再让权重随排名上升但在阈值处封顶。由于 SoftSat 势函数被限制在 $[0,1]$，目标分布相对基础分布的密度比可以保持有界，这既抑制极端权重，也使论文关于加权估计近似率的条件适用于该目标。<br>
**原文位置**：第 5.2 节，公式 (14)–(16)

</div>

</div>

<div class="equation-block" markdown="1">

#### 有限池权重与加权 Self-Consistency

$$
\widehat{u}_{i}=\frac{1}{N}\sum_{k=1}^{N}\mathbf{1}\!\left\{\ell(\tau_k)\leq\ell(\tau_i)\right\},\qquad \widetilde{r}_{i}=\operatorname{clip}_{[1-\eta,\,1+\kappa\eta]}\!\left(\exp\!\left[\beta\operatorname{SoftSat}_{m}(\widehat{u}_{i})+c\right]\right),\qquad W_i=\frac{\widetilde r_i}{\sum_{j=1}^{N}\widetilde r_j},\qquad \mathcal{D}_{\mathrm{SC}}(\tau_{1:N},W_{1:N})=\arg\max_a\sum_{i=1}^{N}W_i\mathbf{1}\!\left\{A(\tau_i)=a\right\}
$$

**符号说明**

- $N$：当前提示词下生成并用于共识的基础轨迹数量。
- $\tau_i$：候选池中的第 $i$ 条完整轨迹。
- $\widehat u_i$：第 $i$ 条轨迹在有限候选池中的经验似然秩。
- $\mathbf{1}\{\cdot\}$：指示函数；条件成立时为 $1$，否则为 $0$。
- $\eta$：控制权重乘子下界偏离 $1$ 的裁剪参数。
- $\kappa$：与 $\eta$ 共同控制权重乘子上界的非对称系数。
- $c$：使裁剪前后所用乘子按论文流程达到均值一尺度的偏移量。
- $\widetilde r_i$：经过 SoftSat、指数映射、均值尺度调整及区间裁剪后的有限池乘子。
- $W_i$：对所有有限池乘子归一化后，第 $i$ 条轨迹的共识权重。
- $A(\tau_i)$：从第 $i$ 条轨迹中抽取并规范化的答案。
- $a$：加权共识所比较的候选答案。
- $\mathcal D_{\mathrm{SC}}$：加权 Self-Consistency 读出器，选择累计权重最大的答案。

<div class="equation-explanation" markdown="1">

**直观理解**：总体分布的真实分位秩通常无法精确计算，因此该式直接用现有 $N$ 条样本的排序估计它。随后，回答不再各计一票，而是按受限权重累计到其答案上；这保留了多样本共识的答案聚合作用，同时避免某条最高似然轨迹凭极端权重单独决定结果。<br>
**原文位置**：第 5.3 节，公式 (17)–(19) 与算法 1

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该方法不是参数训练、微调或奖励优化方法，不更新基础模型参数 $\theta$，也没有需要反向传播的训练损失；$m$、$\beta$、$\eta$ 和 $\kappa$ 是推理阶段重加权规则的参数。其理论目标是用基础分布样本和重要性权重近似所定义的序列级目标答案质量，并通过任务适配的加权共识选择最终输出。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 基础池重要性加权**

理想 Power 目标满足 $q_\alpha(\tau)\propto p(\tau)^\alpha$，因此从基础分布采得的轨迹可使用比率 $r_\alpha(\tau)=p(\tau)^{\alpha-1}$ 估计目标答案质量。论文给出的引理表明，对固定答案，归一化加权质量与直接从 $q_\alpha$ 采样所得的经验质量具有相同的渐近期望；在密度比有界时，两者差异为 $O_p(N^{-1/2})$。

> 直观理解：这一模块说明为何可以只生成一批基础模型回答，再用权重模拟目标分布下的共识，而不必为获得 $N$ 条 Power 轨迹运行 $N$ 次 Power-SMC。该等价是渐近且位于理想目标层面，并不意味着加权旧样本真的变成了相互独立的新目标样本。

**2. Relative-Rank SoftSat**

总体相对秩定义为 $u_p(\tau)=\Pr_{X\sim p}[\ell(X)\leq\ell(\tau)]$，其有限池估计为经验分位秩 $\widehat u_i$。SoftSat 在 $u<m$ 时以平滑凹函数增加增益，并在 $u\geq m$ 时固定为 $1$；$\beta$ 控制指数权重强度，$m$ 控制开始饱和的位置。

> 直观理解：相对秩消除每道题自身似然跨度造成的加权强弱差异，SoftSat 则避免只有最靠前的少量轨迹获得不断扩大的优势。两部分分别针对剂量不匹配和覆盖不匹配。

**3. 有界加权共识读出**

有限样本中，指数乘子经偏移量 $c$ 做均值一缩放，并被裁剪在 $[1-\eta,1+\kappa\eta]$；归一化后的 $W_i$ 可直接替换共识算法中的均匀候选权重。对答案型任务，读出为 $\arg\max_a\sum_iW_i\mathbf 1\{A(\tau_i)=a\}$；对自由形式输出，权重用于 ModeX 的完整读出流程。

> 直观理解：均值一缩放维持整体权重尺度，裁剪限制单个候选相对普通候选最多被削弱或增强多少。读出器仍负责按任务定义“哪些回答一致”，SoftSat 只改变各候选对最终共识的影响力。

**训练与推理**

训练阶段不发生任何模型更新。推理时，对每个提示词 $x$ 仅从 $p_\theta(\cdot\mid x)$ 生成一次包含 $N$ 条完整轨迹的候选池，同时取得每条轨迹的序列对数似然；在该池内排序得到 $\widehat u_{1:N}$，依次应用 SoftSat、指数增益、均值一偏移、区间裁剪和归一化，形成 $W_{1:N}$。最后，根据任务采用加权 Self-Consistency 或加权 ModeX 返回 $\widehat y$。这一过程与均匀共识复用相同的 $N$ 条基础轨迹，因此模型生成成本相同且不增加模型调用；额外工作仅是池内排序、权重计算和加权读出。

**复现信息**

复现时必须区分共识候选数 $N$ 与 Power-SMC 的内部粒子数 $M$：本方法直接使用 $N$ 条基础轨迹，不运行有限 $M$ 的 Power-SMC。对数似然应按完整轨迹计算，即累加各 token 在其前缀条件下的对数概率；相对秩只能在同一提示词的候选池内计算。有限池乘子需使用区间 $[1-\eta,1+\kappa\eta]$ 裁剪，并通过偏移量 $c$ 保持均值一尺度，再归一化为候选权重。答案型任务还需使用论文设定的答案抽取与规范化函数 $A(\tau)$；没有规范答案字符串的自由形式任务则应将同一组候选权重贯穿 ModeX 读出，而不能先将轨迹简化为普通字符串多数投票。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- BigCodeBench：使用 Full-Instruct 划分，共 1,140 道代码生成题。它测试方法在程序响应空间中的效果；八条候选轨迹经过 ModeX 响应级聚合，再由官方执行评测器判断程序正确性。
- LiveAoPSBench：使用 2024 年 4 月切片，共 498 道数学推理题。它测试加权共识能否从多个可能表述不同但数学等价的答案中选出正确答案组，评分采用该基准的官方等价性判定。
- PHYSICS：使用官方测试集中的纯文本 Regular 子集，共 503 道题。它补充检验物理推理响应空间；系统先合并等价的抽取答案，再选择均匀质量或加权质量最大的答案组，并按官方规则评分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**官方基准得分（%）**

分别按照 BigCodeBench 的执行正确性以及 LiveAoPSBench、PHYSICS 的官方答案等价规则，统计最终聚合答案的正确比例。论文不跨基准求平均，以免混合不同任务的评分含义。 （越高越好，因为更高得分表示在固定八轨迹候选池上选出正确最终答案的问题比例更大。）

</div>
<div class="metric-item" markdown="1">

**正确质量与金答案边际 $(C,G)$**

$C$ 表示候选分布赋给正确答案或正确轨迹的总概率质量；$G$ 表示金答案质量相对最强竞争答案的优势。二者联合用于识别 coverage mismatch：总正确质量增加时，最强错误答案可能增加得更多。 （$C$ 通常越高越好，$G$ 则越大越好；尤其是 $G>0$ 表示金答案仍领先最强错误答案。仅提高 $C$ 不能保证共识决策改善。）

</div>
<div class="metric-item" markdown="1">

**加权实现一致率、准确率差及推理加速比**

在 MoreHopQA Case-5 上比较重复 Power-SMC 采样与确定性加权实现：一致率衡量两者最终规范化答案是否相同，准确率差及其配对 bootstrap 置信区间衡量性能差异，加速比衡量平均推理时间下降幅度。 （答案一致率和加速比越高越好；准确率差越接近零且置信区间覆盖零，越支持加权实现在该有限实验设置下近似原采样过程。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Power 相对 Uniform 在不同响应空间和模型上的稳定性

<div class="result-value" markdown="1">

Power 在 LiveAoPSBench 和 PHYSICS 的全部六个模型设置中均低于 Uniform：前者低 1.808 至 18.474 个百分点，后者低 1.934 至 6.999 个百分点；在 BigCodeBench 上则提高 Qwen3.5 与 Ministral 的得分，但降低 Nemotron 的得分。

</div>

这说明更偏向高 Base 似然轨迹并不是可靠的通用共识策略，其效果依赖任务响应空间和模型。结果反驳的是“统一 Power 锐化可稳定替代均匀共识”，但没有证明任何似然加权必然有害，因为 BigCodeBench 的两个模型仍从 Power 中受益。

<div class="result-source" markdown="1">

来源：第 6.2 节，表 1 后的主结果分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

It underperforms Uniform in all six LiveAoPSBench and PHYSICS settings, by 1.808–18.474 points on LiveAoPSBench and 1.934–6.999 points on PHYSICS.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### SoftSat 相对 Uniform 的九个模型—基准组合

<div class="result-value" markdown="1">

SoftSat 在九个设置中五次提高官方得分、一次持平，最大回退为 1.004 个百分点。按表 1，提升包括 BigCodeBench 的三个模型、LiveAoPSBench 的 Ministral，以及 PHYSICS 的 Ministral。

</div>

作者的核心结论不是 SoftSat 始终胜过 Uniform，而是它比 Power 稳定：能保留若干加权收益，同时把最坏损失控制在较小范围。由于只有九个设置且使用固定候选池，这一结果支持跨任务稳健性，但不足以证明对其他模型、采样配置或基准也成立。

<div class="result-source" markdown="1">

来源：第 6.2 节，表 1 后的主结果分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Relative to Uniform, it improves five of the nine settings, ties one, and has a largest regression of 1.004 points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Nemotron 上两个最大的 Power 失败案例

<div class="result-value" markdown="1">

在 Nemotron 的 LiveAoPSBench 设置中，Power 相对 Uniform 的差距为 18.474 个百分点，SoftSat 将其缩小到 1.004 个百分点；在 PHYSICS 中，相应差距从 6.999 缩小到 0.255 个百分点。

</div>

这两个最坏案例直接检验修复方法能否消除全局指数锐化造成的大幅回退。SoftSat 明显接近 Uniform，但在这两项上仍略低于 Uniform，因此证据支持“缓解严重失败”，而不是“全面超越标准共识”。

<div class="result-source" markdown="1">

来源：第 6.2 节，表 1 后的主结果分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the two largest Power failures, both with Nemotron, the gaps to Uniform fall from 18.474 to 1.004 points on LiveAoPSBench and from 6.999 to 0.255 points on PHYSICS.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主实验只覆盖三个 4–9B 模型、三个基准、每题八条 Base 轨迹以及一组固定生成配置。SoftSat 的跨模型稳定性证据因此仍有限，尤其不能外推到更大模型、不同温度、不同 top-$k$ 或分布外任务。
- Power 与 SoftSat 的主表结果来自同一有限 Base 候选池上的确定性加权读出，并非直接从各自目标分布重新采样。MoreHopQA 的 99.55% 一致率支持该实现选择，但作者明确指出这既不是普适等价性结论，也没有检验渐近收敛速度。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Single：直接使用每道题第一条采样轨迹。它提供单样本生成基线，用于判断多样本聚合本身是否有收益。
- Uniform：对同一候选池中的八条轨迹赋予相同权重，再执行任务匹配的共识读出。它是最关键的对照，因为 Power 和 SoftSat 的价值应体现为优于不利用似然信息的标准多样本共识，而不能归因于额外采样。
- Power：以全局指数 $\alpha=4$ 按序列似然进行锐化。它代表论文要诊断的方案，用于检验“增加高似然轨迹权重”是否会因覆盖错配和剂量错配而损害最终答案。
- SoftSat：统一使用 $m=0.75$、$\beta=1$、$\eta=0.25$、$\kappa=64$，对应裁剪范围 $[0.75,17]$。它是待验证的修复方法；与 Uniform 和 Power 共用 Base 候选池，因此比较主要隔离权重读出规则的影响。

**实验想回答的问题**

- 在代码生成、数学推理和物理问答三种不同响应空间中，Power 加权是否能稳定优于均匀共识；若不能，SoftSat 能否在复用同一候选池和生成预算的条件下减少 Power 的严重性能回退？
- SoftSat 的效果是否符合论文对 coverage mismatch 与 dose mismatch 的诊断，包括保留正确答案相对最强错误答案的优势、避免正确轨迹质量过度集中，以及根据候选轨迹预算调整锐化强度？

**实验实现**

实验使用 NVIDIA-Nemotron-3-Nano-4B-BF16、Qwen3.5-9B 和 Ministral-3-8B-Reasoning-2512。每道题均从 Base 模型以温度 1、$\mathrm{top}\text{-}k=50$ 和最大 16,384 token 生成八条轨迹，所有多样本方法复用该候选池。Uniform 等权，Power 固定为 $\alpha=4$，SoftSat 在所有模型与基准组合上使用同一组参数。BigCodeBench 采用 ModeX 后接官方执行评测；另外两个基准先合并等价的抽取答案，再选总权重最大的答案组。该设计固定生成次数和候选内容，使主表主要比较读出规则，但 Power 与 SoftSat 是确定性加权读出，并非分别从其目标分布重新生成样本。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 轨迹预算 $N$ 与 SoftSat 锐化强度 $\beta$ 的联合扫描：Ministral-8B 在 BigCodeBench 上 | 最优 $\beta$ 从 $N=4$ 时的 0.25 上升到 $N=32$ 时的 2，且 SoftSat 在每个已评估预算上都优于相同预算的均匀自洽聚合。 | 该扫描隔离候选池规模对最佳锐化剂量的影响：样本少时过强加权容易过早集中，样本多时则可使用更强权重。它说明固定 $\beta$ 未必适合所有预算，但只展示一个模型—基准的正文代表设置；其他基准仅在附录图 7 中扩展，摘录未给出逐点数值。 | 第 6.3 节，图 3<br><span class="experiment-evidence">The best β rises from 0.25 at N=4 to 2 at N=32, while SoftSat improves over uniform SC at each evaluated budget.</span> |
| 覆盖错配修复诊断：图 2 的代表设置上比较 Base、Power 与 SoftSat | 跨问题中心从 Base 的 $(C,G)=(0.433,0.132)$ 经 Power 变为 $(0.464,-0.072)$，即正确质量增加但金答案边际转负；SoftSat 得到 $(0.439,0.133)$，在保留略高正确质量的同时恢复了接近 Base 的正边际。 | 该诊断不是普通精度消融，而是直接检验方法是否修复 coverage mismatch。Power 的结果表明增加总正确质量仍可能让最强错误答案获得更大优势；SoftSat 则保持覆盖分布和答案竞争关系接近 Base。不过这只是代表设置的分布诊断，不能单独证明所有数据集上的因果机制。 | 第 6.4 节，图 4(a)<br><span class="experiment-evidence">At the answer level, Power moves the across-problem center from (C,G)=(0.433,0.132) to (0.464,-0.072), whereas SoftSat gives (0.439,0.133) and retains a coverage profile close to Base.</span> |

**定性案例**

- 图 4(b) 的代表设置显示：Power 将正确集合内部的条件质量推向 Base 似然最高的一小段轨迹，而 SoftSat 的质量轮廓更接近 Base。其意义是 SoftSat 不仅恢复答案级金答案边际，也避免仅保留狭窄的高似然正确响应；但该图是总体分布可视化，并非单道题的定性案例，也不能据此断言响应众数一定改变。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper studies power sampling failures and corrections for selecting answers from model probability mass, an inference-time reasoning method.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`fc970d9bfd718ed6044af0ee3b66619600fce0e87f0c62233bf1e5b1ffddc775`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
