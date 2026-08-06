---
title: "[论文解读] Fewer Tokens, Smaller Cache: Reward-Coordinated Efficient Reasoning"
description: "[arXiv 2608.04771][LLM 效率] 本文针对大推理模型中“压缩缓存却可能诱发更长推理”的矛盾，提出以逐步过程奖励统一协调KV缓存压缩、冗余反思抑制和提前停止的ReCo框架。"
arxiv_id: "2608.04771"
announcement_date: "2026-08-06"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:52:38.450008+00:00"
source_sha256: "986ba55448fb025a4818dc3de40ef4bb67f8a04da220ca9b20cbc91586ea9ae7"
tags:
  - "LLM 效率"
  - "LLM Reasoning"
  - "大型推理模型"
  - "思维链推理"
  - "KV 缓存压缩"
  - "过程奖励"
  - "步骤自适应压缩"
  - "生成长度控制"
  - "早停"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.04771</p>

# Fewer Tokens, Smaller Cache: Reward-Coordinated Efficient Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Qiyuan Zhu, Dezhi Li, Pengyu Cheng, Tianle Chen, Jiacheng Wang, Ruijie Shen, Hao Gu, Sida Lin, Zirui Liu, Jiacheng Liu, Sirui Han</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04771v1) · [PDF 下载](https://arxiv.org/pdf/2608.04771v1) · **关键词** 大型推理模型, 思维链推理, KV 缓存压缩, 过程奖励, 步骤自适应压缩, 生成长度控制, 早停<br>


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

本文针对大推理模型中“压缩缓存却可能诱发更长推理”的矛盾，提出以逐步过程奖励统一协调KV缓存压缩、冗余反思抑制和提前停止的ReCo框架。

**不用术语来说**：大推理模型回答问题时，常先写出很长的思考过程；系统还要保存这些历史内容对应的中间状态，供后续生成参考。思考越长，保存和读取这些状态所需的显存、计算与时间就越多。直接丢弃一部分历史状态虽然能减小缓存，却可能让模型因缺少上下文而重复推理，最终生成更多文字，抵消原本希望获得的效率收益。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者指出推理过程不同阶段对上下文丢失的容忍度并不相同，并以逐步过程奖励作为可操作信号：奖励较高表示当前推理路径较稳定，可以更激进地压缩；奖励较低表示模型仍在探索，需要保留更多上下文。
- 作者提出ReCo，以同一个逐步过程奖励协调三类决策：动态调整KV缓存保留比例、惩罚冗余的自我反思词元，并在持续高奖励且答案置信度足够时提前结束推理，从而同时控制缓存规模和后续生成长度。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大型推理模型（LRM）通常先生成较长的思维链，再给出最终答案；这能改善数学、代码与科学问题上的复杂推理，却也会因“过度思考”增加输出 token 数、推理时延和计算成本。在自回归生成中，模型会保存历史 token 的键值缓存（KV cache），供后续注意力计算复用；缓存随思维链持续增长，因此同时构成显存占用和逐 token 计算的主要瓶颈。传统 KV 缓存压缩多面向一次预填充后基本不变的长提示词，而推理模型的缓存主要来自不断增长、且仍需支撑后续推理的中间步骤，因而压缩决策不仅要考虑删去多少缓存，还要考虑删减上下文后是否会诱发更长的后续生成。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链推理（Chain-of-Thought, CoT）**

模型在最终作答前生成一系列中间推理步骤，以分解复杂问题并逐步得到答案。本文关注长思维链带来的冗余生成、时延和计算开销，而不是改变推理任务本身。

</div>
<div class="concept-item" markdown="1">

**键值缓存（KV cache）**

Transformer 自回归解码时会保存历史 token 在注意力层中的键和值，避免每生成一个新 token 都重新计算全部历史表示。压缩该缓存可以降低显存与注意力计算成本，但删除仍有用的上下文可能破坏后续推理。

</div>
<div class="concept-item" markdown="1">

**过程奖励（process reward）**

过程奖励为当前已完成的推理步骤给出一个标量分数，用来估计推理路径是否正确、可靠且仍在正轨上。本文将该分数视为步骤级控制信号：高分状态更能承受上下文删减，低分状态仍可能处于探索阶段，需要保留更多信息。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个需要大型推理模型通过自回归思维链求解的问题，以及生成过程中逐步增长的 KV 缓存；每完成步骤 $c_i$，轻量级过程奖励估计器产生分数 $v_i$。目标是在不重新训练推理模型、也不依赖逐任务提示工程的设置下，依据步骤状态动态决定缓存保留程度，并联合限制冗余反思与判断何时停止推理，最终输出答案，同时减少缓存规模、生成 token 数和端到端时延，并尽量保持原有准确率。该问题区别于静态长上下文压缩：这里被压缩的主要是模型刚生成的推理轨迹，而这些内容仍会影响尚未生成的步骤；此外，压缩后的上下文可能使模型生成更多 token，因此缓存节省与生成长度不能被视为彼此独立的目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$c_i$**

思维链中的第 $i$ 个已完成推理步骤。

</div>
<div class="notation-item" markdown="1">

**$v_i$**

步骤 $c_i$ 完成后由过程奖励估计器给出的标量奖励，反映当前推理路径是否可靠且在正轨上。

</div>
<div class="notation-item" markdown="1">

**$\beta_i$**

由奖励 $v_i$ 映射得到的反思 token 对数几率惩罚强度，用于抑制冗余的自我反思式生成。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{PPL}(a)\leq\tau_p$**

答案候选 $a$ 的困惑度不高于阈值 $\tau_p$ 的停止条件，表示答案置信度足以支持结束推理。

</div>

</div>

**直接相关的工作**

- **R-KV**: 面向推理过程的 KV 缓存压缩方法，但原文称其采用启发式淘汰与统一策略，未按推理步骤的重要性调整压缩程度，并且只处理缓存、不控制压缩后可能出现的生成长度膨胀。
- **RPC**: 同样将 KV 缓存压缩用于持续增长的推理轨迹；与本文问题最直接的差异是，RPC 被作者归为忽略步骤重要性且仅作用于缓存的方法，而本文试图用统一的过程奖励联合协调缓存保留与生成控制。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长链式思维使大推理模型能够处理数学、代码和科学问题，但也容易产生“过度思考”：即使问题并不需要很长推导，模型仍可能生成大量中间步骤。自回归解码必须为这些历史词元保存键值缓存，即KV cache；缓存随推理持续增长，会同时增加显存占用、每个新词元的注意力计算量以及端到端延迟，因此实际部署需要在尽量保持答案正确率的前提下降低这部分成本。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **经典长上下文KV缓存压缩**：SnapKV、PyramidKV等方法依据注意力分数淘汰不重要的缓存项；其他方法通过合并相似缓存项或采用低比特量化来减少占用。这类方法主要面向由静态长提示主导的场景，通常可在预填充后集中压缩一次。
- **面向推理过程的统一KV缓存压缩**：近期方法把缓存压缩扩展到链式思维生成过程中，但通常沿整条推理轨迹使用统一压缩策略，即不同步骤采用相同或固定的压缩强度，关注的主要是从缓存中删除了多少内容。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 统一压缩忽略了推理状态的阶段差异：已经处于正确、稳定路径的高奖励状态更能承受上下文裁剪，而仍在探索的低奖励状态较脆弱。对二者施加相同压缩强度，会在可安全压缩时保留过多缓存，或在需要上下文时错误删除信息，从而损害效率或准确率。
- 现有方法主要核算缓存侧的减少，没有同时考察压缩对后续生成行为的影响。作者观察到，缓存变小后模型可能因上下文缺失而重复检查、反思或重新推导，使输出反而变长；因此仅压缩KV缓存并不等价于降低完整推理成本，新增词元可能抵消显存和注意力计算方面的收益。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种面向动态推理轨迹的联合控制机制：它既要逐步判断当前状态能承受多强的上下文压缩，又要把压缩导致的生成长度变化纳入同一决策过程。换言之，已有工作没有提供一个共享信号，使缓存保留、冗余推理抑制和推理终止能够随当前推理状态协同调整。

</div>
<div markdown="1"><span>核心问题</span>

能否利用轻量级过程奖励估计器在每个推理步骤结束后评估路径的可靠程度，并以该信号联合决定KV缓存压缩强度、反思词元抑制程度和提前停止时机，从而在尽量保持答案准确率的同时减少生成词元、延迟和缓存占用？

</div>
<div markdown="1"><span>作者直觉</span>

过程奖励可以理解为当前解题路线的“进展与可靠性指示器”。当奖励高时，模型大概率已经沿着有效路径前进，对完整历史的依赖较弱，因此可以更大胆地裁剪缓存，并抑制“等等、再检查一下”等可能引出重复推导的反思表达；若高奖励持续出现且答案探针显示置信度足够，就可直接结束推理。相反，低奖励意味着路线尚不稳定，此时保留更多上下文和探索空间更稳妥。让三种操作读取同一信号，有助于避免一边激进压缩、一边因信息不足生成更多补偿性推理。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ReCo 是一个仅在推理阶段工作的、以“推理步骤”为控制粒度的联合压缩框架。给定问题 $q$，大推理模型 $\mathcal{M}$ 自回归生成思维链 $\mathcal{C}=\{c_1,\ldots,c_T\}$，并以换行符划分步骤；每完成一步 $c_i$，轻量过程奖励估计器 Pilot 根据当前轨迹 $c_{\leq i}$ 输出奖励 $v_i\in[0,1]$。同一个 $v_i$ 同时控制三件事：调整整个已累积 KV 缓存的保留比例、抑制下一步中可能重新开启无效分支的反思词元，以及在轨迹持续可靠时触发答案置信度探测。最终输出是模型提交的答案，同时获得更短的生成序列、更小的 KV 缓存和更低的端到端延迟。

技术上的关键不是单独提高某种缓存淘汰算法，而是协调“每个生成词元有多贵”和“模型还要生成多少词元”这两个成本来源。直观地说，Pilot 像一名随行检查员：当前推理已经比较稳妥时，系统可以少保留一些历史笔记，并阻止模型反复说“等等、换个思路”；当前推理仍不稳定时，则保留更多上下文并允许继续探索。只有在连续高奖励且候选答案本身也具有低困惑度时，系统才提前结束，避免仅凭语言流畅度过早提交错误答案。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤化生成与在线奖励评估

模型按 $c_i\sim\mathcal{M}(\cdot\mid q,c_{<i})$ 生成下一段内容，并在换行词元处将其记为一个完整推理步骤；随后用 30M 参数的 Pilot 对 $c_{\leq i}$ 打分，得到 $v_i=\mathrm{Pilot}(c_{\leq i})\in[0,1]$。该分数估计当前状态最终导向正确答案的可能性，而不是直接度量某个历史词元是否重要。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、推理模型 $\mathcal{M}$，以及已经生成的部分轨迹 $c_{<i}$。<br>
**输出**：完成的步骤 $c_i$、更新后的部分轨迹 $c_{\leq i}$ 和统一控制信号 $v_i$。

</div>

**直观理解**：系统不会在每个词元后都作复杂决策，而是在一段相对完整的推理写完后检查方向是否可靠。奖励越高，表示当前路线越像一条能够得到正确答案的路线。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 奖励自适应缓存预算分配

当缓存自上次压缩后至少增长 $S$ 个词元，即 $L-L_{i-1}\geq S$ 时，根据最新奖励相对本轨迹平均奖励的位置计算保留比例 $\lambda_i$，并把目标缓存预算设为 $m_i=\lambda_iL$。高于轨迹平均水平的奖励会减小 $\lambda_i$，低于平均水平的奖励会增大 $\lambda_i$。

<div class="method-step__io" markdown="1">

**输入**：最新奖励 $v_i$、当前轨迹的奖励统计量、当前 KV 缓存长度 $L$、基础保留比例 $\lambda$、调节幅度 $\delta$ 和压缩间隔 $S$。<br>
**输出**：本轮允许保留的缓存规模 $m_i$，以及用于整个累积缓存的动态保留比例 $\lambda_i$。

</div>

**直观理解**：系统先决定“这次能留下多少历史”。推理已经稳定时可以更大胆地压缩；推理仍在摸索时则多留一些上下文，降低思路因信息缺失而中断的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 注意力引导的 KV 词元选择

对每个历史词元 $j$，汇总最近 $w$ 个查询对其键向量的注意力，得到相关性分数 $s_j$；保留得分最高的 $m_i$ 个词元，并强制保留最近的 $w$ 个词元。每次压缩都会重新计算分数，因此已经不再被近期推理关注的旧词元可被后续淘汰。

<div class="method-step__io" markdown="1">

**输入**：目标预算 $m_i$、长度为 $L$ 的累积 KV 缓存，以及最近 $w$ 个词元形成的查询窗口。<br>
**输出**：规模受 $m_i$ 限制、但优先保留当前推理相关信息的压缩 KV 缓存。

</div>

**直观理解**：奖励只回答“留多少”，注意力则回答“具体留哪些”。这类似先确定笔记页数，再留下最近推理真正引用的内容，而不是机械地删除最早或随机的记录。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 反思抑制与置信度早停

生成下一步时，按奖励所在区间对 $\mathcal{R}$ 中词元的 logit 施加 $0$、$\beta/2$ 或 $\beta$ 的惩罚；若连续两个步骤满足 $v_i\geq\tau_h$，则插入结束思考提示并生成候选答案 $a$，仅当 $\mathrm{PPL}(a)\leq\tau_p$ 时提交，否则丢弃探测结果并继续推理。

<div class="method-step__io" markdown="1">

**输入**：最新奖励 $v_i$、阈值 $\tau_\ell<\tau_h$、最大惩罚 $\beta$、反思词元集合 $\mathcal{R}$、连续奖励历史和答案困惑度阈值 $\tau_p$。<br>
**输出**：受到反思词元约束的后续推理；或者在轨迹可靠且答案置信度足够高时得到最终答案 $a$。

</div>

**直观理解**：高奖励时，模型不太需要再用“等等”或“换一种方法”等表达重新开辟分支；但系统也不会只因路线看起来正确就停止，还要检查模型是否能自信地给出具体答案。探测失败后恢复推理，使早停成为可撤销的尝试。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 奖励驱动的动态缓存保留比例

$$
\lambda_i=\underbrace{\lambda}_{\text{base ratio}}-\underbrace{\delta\frac{v_i-\bar{v}}{v_{\max}-v_{\min}}}_{\text{reward adjustment}},\qquad m_i=\lambda_iL,\qquad \lambda_i\in[\lambda-\delta,\lambda+\delta]
$$

**符号说明**

- $\lambda_i$：第 $i$ 个已完成步骤所决定的本轮 KV 缓存保留比例。
- $\lambda$：不考虑奖励调节时的基础缓存保留比例。
- $\delta$：奖励调节幅度，用于限制动态比例偏离基础比例的程度。
- $v_i$：Pilot 对部分轨迹 $c_{\leq i}$ 给出的最新步骤奖励。
- $\bar{v}$：当前轨迹截至该时刻所有步骤奖励的平均值。
- $v_{\min},v_{\max}$：当前轨迹截至该时刻观察到的最小和最大奖励。
- $L$：压缩发生前累积 KV 缓存中的词元数。
- $m_i$：第 $i$ 次决策后允许保留的 KV 词元数量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先把最新奖励与本轨迹平均奖励比较，再用轨迹内部的奖励范围归一化。若 $v_i>\bar{v}$，调整项为正，$\lambda_i$ 下降并触发更强压缩；若 $v_i<\bar{v}$，则保留更多缓存。作者据此把“当前状态对上下文损失的容忍度”转化为实际缓存预算；需要注意，给定节选未说明当 $v_{\max}=v_{\min}$ 时如何处理分母为零的边界情况。<br>
**原文位置**：公式 (1)，第 3.2 节 Reward-driven retention

</div>

</div>

<div class="equation-block" markdown="1">

#### 奖励分段反思惩罚与双条件早停

$$
\begin{aligned}\beta_i&=\begin{cases}0,&v_i\leq\tau_{\ell},\\ \beta/2,&\tau_{\ell}<v_i<\tau_h,\\ \beta,&v_i\geq\tau_h,\end{cases}\quad \beta>0,\\ \tilde z_t(u)&=\begin{cases}z_t(u)-\beta_i,&u\in\mathcal R,\\ z_t(u),&u\notin\mathcal R,\end{cases}\\ \mathrm{PPL}(a)&=\exp\!\left(-\frac{1}{n}\sum_{t=1}^{n}\log p(x_t\mid x_{<t})\right),\qquad \mathrm{stop}\iff \mathrm{PPL}(a)\leq\tau_p\ \text{ after two consecutive steps with }v_i\geq\tau_h.\end{aligned}
$$

**符号说明**

- $\beta_i$：完成第 $i$ 步后，在生成下一步时采用的反思词元惩罚强度。
- $\beta$：最高奖励区间使用的完整 logit 惩罚，且为正数。
- $\tau_{\ell},\tau_h$：满足 $\tau_{\ell}<\tau_h$ 的低、高奖励阈值，用于把奖励划成三个区间。
- $z_t(u),\tilde z_t(u)$：位置 $t$ 上词元 $u$ 的原始 logit 与施加反思惩罚后的 logit。
- $\mathcal R$：人工整理的反思词元及其分词器变体集合，例如表示“Wait”“Hmm”和“Alternatively”的词元。
- $a=(x_1,\ldots,x_n)$：早停探测阶段生成的、由 $n$ 个词元组成的候选答案。
- $p(x_t\mid x_{<t})$：模型在答案前缀 $x_{<t}$ 条件下赋予第 $t$ 个答案词元的概率。
- $\mathrm{PPL}(a)$：候选答案的困惑度；数值越低，表示模型对该答案序列越有把握。
- $\tau_p$：允许提交候选答案的最大困惑度阈值。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分把奖励映射成三级反思抑制：低奖励时保留探索能力，中等奖励时温和抑制，高奖励时强烈阻止重新开辟分支；惩罚通过降低相关词元的 logit 改变采样概率。第二部分要求“连续高奖励”和“答案低困惑度”同时成立：前者检查推理路线，后者检查具体答案，因此比单独使用困惑度更不容易因一个流畅但错误的答案而提前停止。<br>
**原文位置**：公式 (3)–(6)，第 3.3 节 Reward-banded reflection penalty 与 Early stopping via answer confidence

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：ReCo 本身没有需要在目标任务上优化的新训练目标，核心算法是在推理时根据奖励和解码统计执行确定性的控制规则。基础大推理模型 $\mathcal{M}$ 保持不变；Pilot 在本文方法之外已从 Skywork-o1-Open-PRM-7B 蒸馏，其训练目标被描述为匹配教师过程奖励，但给定章节没有提供具体蒸馏损失、训练数据或优化过程。因此不能把缓存保留式、反思惩罚或困惑度阈值解释为通过端到端反向传播学习的目标，它们是推理阶段的决策机制。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 轻量过程奖励估计器 Pilot**

Pilot 是从 Skywork-o1-Open-PRM-7B 蒸馏得到的 30M 参数步骤级估计器，在每个完整步骤后计算 $v_i=\mathrm{Pilot}(c_{\leq i})$。它评价部分轨迹继续导向正确答案的可能性，并作为缓存预算、反思惩罚和早停触发条件的共同信号；原文没有说明在 ReCo 实验中继续联合训练 Pilot 或基础推理模型。

> 直观理解：若三个控制器各用一套互不相关的判断标准，可能出现一边认为应该压缩、一边认为应该继续探索的冲突。共享奖励使缓存和生成控制围绕同一个“当前路线是否可靠”的判断协同行动。

**2. 奖励分配预算、注意力选择内容的 KV 压缩器**

压缩器以固定增长间隔 $S$ 触发，但每次目标比例 $\lambda_i$ 都由当前奖励相对本轨迹奖励均值、最小值和最大值的位置决定，范围受 $[\lambda-\delta,\lambda+\delta]$ 约束。得到预算 $m_i$ 后，系统汇总最近 $w$ 个查询对历史键的注意力并选择高分词元，同时始终保留查询窗口；这是一种动态全缓存重选，而不是给每一步永久分配互不变化的局部预算。

> 直观理解：相对归一化让决策适应不同题目和轨迹的打分尺度：重要的是某一步在“这条轨迹内部”属于高分还是低分，而不要求所有问题共享完全一致的绝对奖励标尺。预算决策与内容选择分工后，奖励无需精确判断每个词元的重要性。

**3. 奖励自适应生成控制器**

该模块包括解码期反思词元惩罚和两阶段早停。前者直接修改指定词元的 logit，不增加额外前向传播；后者先用连续两步高奖励筛选可靠轨迹，再通过临时生成答案并计算 $\mathrm{PPL}(a)$ 检查答案置信度，因此探测本身有额外生成成本，但只对已进入高奖励区间的轨迹执行。

> 直观理解：仅缩小缓存可能让模型因上下文受损而生成更多补偿性推理，抵消节省，所以必须同时约束输出长度。反思惩罚减少无谓分支，早停删除已经得到结论后的尾部推理，两者分别处理“少绕路”和“及时结束”。

**训练与推理**

训练方面，给定节选只说明使用已经蒸馏完成的 Pilot，未报告 ReCo 对 Pilot 或推理模型进行额外微调，也未说明基础比例 $\lambda$、调节幅度 $\delta$、阈值 $\tau_\ell$、$\tau_h$、$\tau_p$、压缩间隔 $S$、窗口 $w$ 和惩罚 $\beta$ 是否通过验证集搜索确定。因而可复现时应把 ReCo 视为外接于冻结模型的推理解码框架，而不能假定这些参数由联合训练自动获得。

完整推理过程如下：输入问题 $q$ 后，模型持续生成至换行并形成步骤 $c_i$；Pilot 对 $c_{\leq i}$ 计算 $v_i$。当缓存增量达到 $S$ 时，系统计算动态比例 $\lambda_i$ 和预算 $m_i$，再依据最近 $w$ 个查询产生的注意力保留高分 KV 词元。生成 $c_{i+1}$ 时，系统依据 $v_i$ 所在奖励区间降低集合 $\mathcal R$ 中词元的 logit。若连续两个步骤处于最高奖励区间，则插入原文给出的结束思考提示“Okay, I think I have finished thinking.”并生成候选答案；候选答案满足 $\mathrm{PPL}(a)\leq\tau_p$ 时提交，否则丢弃该探测答案、恢复思考并继续上述循环，直至正常结束或后续探测成功。

**复现信息**

公平解释结果所需的实现信息包括：步骤边界由换行词元定义；奖励器是 30M 参数的 Pilot，教师为 Skywork-o1-Open-PRM-7B；缓存不是每一步必然压缩，而是在距上次压缩新增至少 $S$ 个词元时压缩；奖励决定整个累积缓存的单一预算，注意力选择具体保留词元，最近 $w$ 个词元始终保留；反思集合 $\mathcal R$ 包含目标表达及其分词器变体，惩罚直接作用于 logit；早停探测只在连续两步满足 $v_i\geq\tau_h$ 后执行，失败后继续原推理。

结果中的端到端延迟包含 Pilot 在线评分和置信度探测开销，并在单张 NVIDIA H20 GPU 上按每题墙钟时间测量；主表数字是三次独立运行的平均值。这一点很重要，因为 ReCo 的速度收益不是忽略奖励器后的理论缓存收益。给定节选没有报告 $S$、$w$、$\lambda$、$\delta$、$\beta$、三个阈值的具体取值，也没有说明注意力分数如何跨层、跨头聚合，以及奖励范围退化时的数值处理；这些均属于当前材料中的复现缺口，需回查论文完整版本或代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学推理数据集组：GSM8K、MATH-500 和 AMC2023，覆盖从小学算术到竞赛数学的不同难度，用于检验方法在常规及中等难度数学推理上的准确率与效率。原文未明确报告各数据集的规模、划分方式和具体测试样本数。
- 高难度竞赛数学数据集组：AIME24 和 AIME25，用于检验模型在信息密集、长链式推理任务上的鲁棒性，尤其适合观察缓存压缩是否破坏关键中间状态。原文未明确报告各数据集的规模、划分方式和具体测试样本数。
- 科学推理数据集：GPQA，用于检验方法是否能从数学任务推广到科学知识与推理任务。原文未明确报告该数据集的规模、划分方式和具体测试样本数。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率**

衡量模型在各数据集上最终答案正确的比例，用于评估压缩和生成控制是否损害推理质量。 （越高越好；但实验重点是接近 Full CoT，而不是脱离效率成本单独追求最高准确率。）

</div>
<div class="metric-item" markdown="1">

**平均生成 token 数**

衡量模型为完成任务生成的平均文本长度，反映解码工作量以及过度思考程度。 （越低越好，但必须结合准确率解释；单纯减少 token 可能意味着提前截断或推理失败。）

</div>
<div class="metric-item" markdown="1">

**端到端延迟与相对加速比**

端到端延迟衡量完整推理所需时间；相对加速比以 Full CoT 为参照，表示完整推理速度提升倍数，综合反映缓存压缩、生成长度和额外控制开销。 （延迟越低、加速比越高越好；该指标检验 token 减少是否真正转化为实际系统收益。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三种模型上的准确率保持能力

<div class="result-value" markdown="1">

作者报告 ReCo 在三个模型上的平均准确率分别为 Llama-8B 的 $60.2\%$、Qwen-7B 的 $60.0\%$ 和 Qwen3-8B 的 $69.6\%$，对应 Full CoT 的 $62.8\%$、$61.9\%$ 和 $72.3\%$，是所有压缩方法中与 Full CoT 差距最小的方案。在 Llama-8B 的 AIME25 上，ReCo 保持 $33.3\%$，而所有 KV-cache 压缩基线均不超过 $20\%$。

</div>

这说明奖励引导的缓存保留能够减少对脆弱推理状态的破坏，尤其在高难度任务上比统一压缩策略更稳健。该结果支持 ReCo 的准确率保持优势，但不等于 ReCo 完全没有准确率损失，也不能仅凭平均准确率证明其在所有任务或模型上都优于 Full CoT。

<div class="result-source" markdown="1">

来源：第 4.2 节“ReCo best preserves accuracy under compression”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ReCo stays closest to Full CoT: its average accuracy is 60.2% vs. 62.8% on Llama-8B, 60.0% vs. 61.9% on Qwen-7B, and 69.6% vs. 72.3% on Qwen3-8B, the smallest gap among all compressed methods.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 生成长度与长度膨胀

<div class="result-value" markdown="1">

相较于 Full CoT，ReCo 在 Llama-8B、Qwen-7B 和 Qwen3-8B 上分别减少 $37\%$、$65\%$ 和 $46\%$ 的生成 token。相反，缓存专用方法可能增加生成长度；例如 Llama-8B 上 SnapKV 将平均生成长度从 $7{,}078$ 增至 $11{,}266$ token。Dynasor 在 Llama-8B 的 GSM8K 上将准确率降至 $82.3\%$，低于 Full CoT 的 $89.8\%$。

</div>

缓存变小虽然降低了单个 token 的注意力成本，却可能使模型因上下文信息不足而反复推理，从而抵消节省。ReCo 同时控制缓存和反思生成，因此减少 token 的同时避免了这一长度膨胀现象。该结果表明联合控制更适合效率优化，但不能说明所有缓存压缩方法在所有任务上都会增加生成长度。

<div class="result-source" markdown="1">

来源：第 4.2 节“ReCo reduces tokens without inflation, unlike cache-only compression”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In sharp contrast, the cache-only methods SnapKV, R-KV, and RPC all increase token count (e.g. 7,078 → 11,266 under SnapKV on Llama-8B), directly corroborating the length-inflation effect of Sec. 2.2.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 端到端延迟与准确率的联合权衡

<div class="result-value" markdown="1">

ReCo 相对 Full CoT 在 Llama-8B、Qwen-7B 和 Qwen3-8B 上分别达到 $2.08\times$、$2.35\times$ 和 $2.18\times$ 加速。Llama-8B 上缓存专用基线仅达到 $1.09\times$ 至 $1.33\times$ 加速；长度控制方法虽可达到相近延迟，但 SAT 的准确率为 $58.1\%$，低于 ReCo 的 $60.2\%$。

</div>

该结果说明减少每个 token 的计算量还不够，必须同时减少生成 token，才能把缓存压缩转化为明显的端到端收益。ReCo 的优势在于同时降低两类成本，并在相近速度下较好保持准确率。由于实验只使用单张 H20 GPU，结果对其他硬件、批处理规模和服务负载的可迁移性仍未得到验证。

<div class="result-source" markdown="1">

来源：第 4.2 节“ReCo delivers strong speedups without trading away accuracy”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Reducing both the per-token attention cost and the generation length, ReCo reaches 2.08×, 2.35×, and 2.18× speedup over Full CoT on Llama-8B, Qwen-7B, and Qwen3-8B.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 数据集虽覆盖五个数学数据集和一个科学推理数据集，但实验章节未明确报告数据规模、划分方式、解码随机性、统计显著性或各模型的逐任务完整结果，因此无法判断结果的方差与稳定性，也不能排除某些任务或设置上的性能退化。
- 所有实验在单张 NVIDIA H20 GPU 上进行，且超参数敏感性主要在 DeepSeek-R1-Distill-Llama-8B 上分析。由此得到的端到端延迟和统一配置结论，尚不足以证明在不同硬件、批处理负载、模型规模或更广泛任务上的通用性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Full CoT：不压缩 KV-cache 且不限制推理长度的完整链式思考，作为准确率参考上限和效率比较基准。
- KV-cache 压缩方法：SnapKV、R-KV 和 RPC，通过移除缓存条目降低每个生成 token 的注意力成本，但不控制生成长度，用于测试单独压缩缓存的效果及其可能引起的生成长度膨胀。
- SAT：通过提示词控制缩短推理过程，同时保留完整 KV-cache，用于比较只控制生成长度的方案。
- Dynasor：通过提前停止解码减少生成 token，同时保留完整 KV-cache，用于比较另一类只控制生成过程的方案，并检验在相近加速水平下是否需要牺牲准确率。

**实验想回答的问题**

- 在保持推理准确率的前提下，ReCo 能否同时减少生成 token 数与端到端延迟，并优于只压缩 KV-cache 或只控制生成长度的方法？
- ReCo 的奖励协调 KV-cache 压缩、反思 token 控制和提前停止三个组件是否互补，以及关键超参数是否存在稳定的有效区间？

**实验实现**

实验使用 DeepSeek-R1-Distill-Qwen-7B、DeepSeek-R1-Distill-Llama-8B 和 Qwen3-8B 三个推理模型，覆盖两个模型系列与不同规模；所有实验在单张 NVIDIA H20 GPU 上进行。ReCo 的基础缓存保留比例设为 $\lambda=0.25$，奖励调整范围设为 $\delta=0.1$，注意力窗口设为 $w=32$；KV-cache 基线使用可比的 $0.25$ 保留比例。生成控制的状态阈值为 $\tau_{\ell}=0.4$ 和 $\tau_{h}=0.8$，提前停止的困惑度阈值为 $\tau_p=1.1$。SAT 与 Dynasor 被调节到相近的加速水平，以便比较准确率与效率的权衡。原文未明确报告统一的样本解码参数、随机种子、每个数据集的样本数量及显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Llama-8B 的组件消融：分别只保留 KV Comp.、Refl. Ctrl. 或 Early Stop | 只使用 KV Comp. 时，AIME25 平均生成长度为 $12.8$k token，而完整 ReCo 为 $8.6$k token。作者还报告完整 ReCo 在 AIME25、AMC 和 MATH500 上的准确率分别为 $33.3\%$、$80.0\%$ 和 $80.6\%$，并称其在三者上均优于单组件变体。 | 该消融分别测试“保留什么上下文”和“推理多久”两个控制方向是否可以独立替代。KV Comp. 单独使用会留下生成长度膨胀问题；反思控制或提前停止虽然减少 token，却缺少奖励引导的缓存保留，因此在困难任务上损失准确率。结果支持三个组件互补，而非简单重复。 | 第 4.3 节“ The three components are complementary ”，图 4<br><span class="experiment-evidence">“KV Comp.” alone leaves generation unconstrained and is the most expensive on hard problems (12.8k tokens on AIME25 vs. ReCo’s 8.6k), echoing the length inflation of Sec. 2.2.</span> |
| 超参数敏感性：基础保留比例、奖励调整范围与提前停止阈值 | 基础保留比例从 $15\%$ 到 $35\%$ 扫描时，$15\%$ 在 AIME25 和 AMC 上的准确率分别为 $20.0\%$ 和 $65.0\%$，且 AIME25 token 数从 $35\%$ 时的 $7.8$k 增至 $15\%$ 时的 $9.2$k。奖励调整范围为 $\delta=0$ 时 AMC 准确率为 $65.0\%$；$\delta=0.10$ 时达到 AMC 的 $80.0\%$、MATH500 的 $80.6\%$ 和 AIME25 的 $33.3\%$。提前停止阈值从 $1.10$ 调至 $1.20$ 时，MATH500 准确率由 $80.6\%$ 降至 $68.4\%$。 | 该分析测试配置是否存在合理稳定区间，而不是只报告一个经过选择的点。过度压缩会破坏关键信息，并可能诱发更长的补偿性推理；完全不使用奖励调整则退化为统一策略；提前停止过于宽松会过早结束并损害准确率。作者因此采用 $\lambda=0.25$、$\delta=0.10$ 和 $\tau_p=1.10$，但敏感性实验仍主要基于 Llama-8B，不能证明这些阈值对所有模型均最优。 | 第 4.3 节“Sensitivity to the reward-adjustment range”，图 5<br><span class="experiment-evidence">At δ = 0.00 the policy is uniform and reward-agnostic, and is consistently among the weakest (65.0% on AMC), direct support for our motivation that reward-guided allocation beats treating all steps alike.</span> |

**定性案例**

- AIME25 是最能体现方法差异的困难案例：Llama-8B 上 ReCo 保持 $33.3\%$ 准确率，而所有 KV-cache 压缩基线均降至不超过 $20\%$；同时，组件消融显示只使用 KV Comp. 时平均生成长度达到 $12.8$k，而完整 ReCo 为 $8.6$k。该案例表明困难推理既需要在信息密集状态保留更多有效上下文，也需要抑制缓存压缩导致的冗余继续生成；但原文未提供具体推理轨迹或 token 级可视化，因此这里只能作聚合指标层面的解释。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The method jointly compresses KV caches, suppresses redundant reasoning tokens, and stops reasoning early to accelerate chain-of-thought inference.; rule check: matched taxonomy keywords; top rule score=11.0
- 全文指纹：`986ba55448fb025a4818dc3de40ef4bb67f8a04da220ca9b20cbc91586ea9ae7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
