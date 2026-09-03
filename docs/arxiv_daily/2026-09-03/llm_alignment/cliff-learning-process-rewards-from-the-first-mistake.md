---
title: "[论文解读] Cliff: Learning Process Rewards from the First Mistake"
description: "[arXiv 2609.02817][对齐 / RLHF] 原文未明确报告。"
arxiv_id: "2609.02817"
announcement_date: "2026-09-03"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:28:19.424364+00:00"
source_sha256: "3d6b3410b2db7ed53b1ee76d8201c16133248db97a949781a6a5b7ea120707be"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "强化学习"
  - "带可验证奖励的强化学习（RLVR）"
  - "大语言模型推理后训练"
  - "过程监督"
  - "首次错误定位"
  - "token 级优势"
  - "奖励塑形"
  - "GRPO"
  - "在线蒸馏"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2609.02817</p>

# Cliff: Learning Process Rewards from the First Mistake

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> Peixuan Han, Runhui Wang, Ketan Ramaneti, Jie Hao, Gerald Friedland, Chris Kong</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Amazon Web Services；Affiliation: University of Illinois Urbana-Champaign</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.02817v1) · [PDF 下载](https://arxiv.org/pdf/2609.02817v1) · **关键词** 带可验证奖励的强化学习（RLVR）, 大语言模型推理后训练, 过程监督, 首次错误定位, token 级优势, 奖励塑形, GRPO, 在线蒸馏<br>


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

原文未明确报告。

**不用术语来说**：原文未明确报告。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 原文未明确报告。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型（LLM）在推理任务上的强化学习后训练，重点是带可验证奖励的强化学习（RLVR）。在 RLVR 中，系统可以自动检查最终答案是否正确，并据此为整条推理轨迹提供奖励；这种设置避免了逐步人工标注，具有较好的规模化能力，但最终结果奖励通常是粗粒度的，无法说明推理过程中哪些步骤正确、又在哪一步首次出错。本文因此关注如何在不训练专用过程奖励模型、也不要求教师与学生采用相同推理模式的前提下，从模型自身生成的推理轨迹中构造更细粒度的学习信号。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**RLVR（带可验证奖励的强化学习）**

模型生成一条推理轨迹和最终答案，外部验证器自动判断答案是否正确，并将判断结果作为强化学习奖励。它的优点是无需逐条人工评价，但通常只评价最终结果，因而难以定位中间推理的错误。

</div>
<div class="concept-item" markdown="1">

**推理轨迹与过程奖励**

推理轨迹是模型从问题到最终答案生成的连续文本或 token 序列。过程奖励不是只评价最终答案，而是评价中间步骤或部分轨迹，从而帮助训练算法把信用分配给具体的推理行为。

</div>
<div class="concept-item" markdown="1">

**GRPO 与优势值**

GRPO（Group Relative Policy Optimization）是一类根据同一问题生成的多条样本相对表现来更新策略的强化学习方法。优势值表示某个动作或 token 相对于参考水平应被鼓励还是抑制；正优势通常提高其概率，负优势通常降低其概率。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定推理任务输入 $x$，学生策略生成一条 token 序列或推理轨迹 $y=(y_1,[0;31my_2,[0m\ldots,y_T)$，其中 $T$ 表示轨迹长度；外部可验证器能够判断最终答案是否正确。本文进一步引入一个现成的教师 LLM，对学生轨迹进行判断并定位首次推理错误的位置 $k$。在失败轨迹中，目标是将轨迹划分为从开头到 $k-1$ 的正确前缀与从 $k$ 开始的错误后缀，再把这一边界信号转换为 token 级优势：正确前缀获得相对正向反馈，首次错误及其后的部分获得负向反馈；完全正确的轨迹则保持为最优结果。该设定假定教师或评估器能够识别“推理在哪一点首次失效”，但不要求其精确评价错误之后的每一个步骤，也不要求教师和学生具有相同的 tokenizer、模型家族或推理模式。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

推理任务的输入问题。

</div>
<div class="notation-item" markdown="1">

**$y=(y_1,\ldots,y_T)$**

学生模型生成的完整推理轨迹；$y_t$ 是第 $t$ 个 token，$T$ 是轨迹长度。

</div>
<div class="notation-item" markdown="1">

**$k$**

教师判断出的首次错误位置；位置 $k$ 之前的内容构成正确前缀，位置 $k$ 及其之后的内容构成错误后缀。

</div>
<div class="notation-item" markdown="1">

**$A_t$**

第 $t$ 个 token 的优势值或训练反馈信号；Cliff 用首次错误边界决定其正负方向，而不是为每个中间步骤单独训练一个过程评分器。

</div>

</div>

**直接相关的工作**

- **Process Reward Models（PRMs）**: PRM 为推理过程中的步骤提供奖励，因此比单一结果奖励更细粒度；但原文指出，PRM 需要额外训练专用奖励模型，可能降低泛化能力并产生 reward hacking（奖励投机），从而增加了 RLVR 的工程和可靠性约束。Cliff 的区别在于只要求教师定位首次错误，不要求建立覆盖所有步骤的连续评分模型。
- **On-Policy Distillation（OPD）**: OPD 让学生在自己的轨迹上学习教师行为，能够提供比结果奖励更丰富的监督；但原文指出，其最佳效果依赖教师与学生具有相近的推理模式，且通常要求 tokenizer 和模型关系更匹配。Cliff 只使用教师对学生轨迹首次错误位置的判断，因此试图避免直接模仿教师完整推理过程。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Cliff 是建立在组相对策略优化（GRPO）之上的奖励塑形方法。给定问题 $q$，当前策略为每个问题生成一组推理轨迹 $a_{1:N}$；自动验证器先判断最终答案是否正确，教师模型再针对可靠的参考解检查学生轨迹，并定位推理首次出错的位置 $p(a_i)$。该位置把错误轨迹分成仍然有效的前缀与由错误开始的后缀，Cliff 据此将原本整条轨迹共享的结果级优势改造成逐词元优势。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 学生策略分组采样与结果验证

旧策略对同一问题采样 $N$ 条推理轨迹 $a_{1:N}$，自动验证器计算每条轨迹的可验证奖励 $R(q,a_i)$。论文主要按二值奖励说明方法，即正确为 $1$、错误为 $0$。

<div class="method-step__io" markdown="1">

**输入**：从训练集 $D$ 采样的问题 $q$，以及旧策略 $\pi_{\theta_{\mathrm{old}}}$。<br>
**输出**：带有结果奖励的一组学生轨迹 $\{(a_i,R(q,a_i))\}_{i=1}^{N}$。

</div>

**直观理解**：普通 GRPO 只知道每份答案最后对不对，就像只给整张试卷一个总分，而不知道错误从哪一步开始。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成并筛选教师参考解

教师独立生成参考解，并由自动验证器检查其最终答案；只有参考解验证正确时，才启用教师的过程判断，否则该问题组退回标准 GRPO。对自动验证器判为全对或全错、因而没有组内奖励方差的问题组，训练实现中跳过教师判断。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、教师模型和自动验证器。<br>
**输出**：经过验证的教师参考解，或表示该组使用标准 GRPO 的回退标记。

</div>

**直观理解**：教师必须先证明自己会做这道题，才能给学生指出第一处错误；这避免把教师自己的错误当成监督信号。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 识别 Pitfall Step

教师先判断学生解答是否正确；对判为错误的轨迹，教师给出首个错误推理步骤 $p(a_i)$，并将 $j<p(a_i)$ 视为有效前缀、将 $j\geq p(a_i)$ 视为错误后缀。若轨迹超过最大长度，则直接设 $p(a_i)=0$，使整条轨迹都被视为有问题。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、验证正确的教师参考解，以及每条学生轨迹 $a_i$。<br>
**输出**：每条错误轨迹的首错边界 $p(a_i)$，以及由该边界确定的前缀—后缀划分。

</div>

**直观理解**：它不反复评价已经建立在错误前提上的后续文字，而是寻找推理“掉下悬崖”的第一步；一旦这一步出现，后面的推导通常已不再提供独立的正确信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造逐词元 Cliff 优势

先由组内正确率计算正确轨迹优势 $A_{\mathrm{cor}}$ 与错误轨迹优势 $A_{\mathrm{inc}}$，再令正确轨迹词元获得 $A_{\mathrm{cor}}-b$，错误轨迹的有效前缀获得 $\lambda A_{\mathrm{cor}}-b$，首错位置及其后缀获得 $A_{\mathrm{inc}}-b$。偏移量 $b$ 将整组逐词元优势重新中心化为零均值；实际训练采用 $\lambda=0$。

<div class="method-step__io" markdown="1">

**输入**：组内二值奖励、GRPO 组统计量、首错边界 $p(a_i)$ 和超参数 $\lambda$。<br>
**输出**：与每个生成词元对应的优势 $A_{i,j}$。

</div>

**直观理解**：最终答错不再意味着此前所有步骤都应受罚：Cliff 保留首错前的推理，集中压低从首错开始的部分；取 $\lambda=0$ 时，前缀主要是不被错误结果连带惩罚，而不是额外鼓励模型写得更长。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 采用逐词元聚合的 GRPO 优化目标

$$
\mathcal{J}_{\mathrm{GRPO}}(\pi_{\theta})=\mathbb{E}\!\left[\frac{1}{\sum_{i=1}^{N}|a_i|}\sum_{i=1}^{N}\sum_{j=0}^{|a_i|-1}\left(\min\!\left\{r_{i,j}A_{i,j},\operatorname{clip}(r_{i,j},1-\epsilon,1+\epsilon)A_{i,j}\right\}-\beta\,\mathbb{D}_{\mathrm{KL}}\!\left[\pi_{\theta}\|\pi_{\mathrm{ref}}\right]_{i,j}\right)\right],\qquad r_{i,j}=\frac{\pi_{\theta}(a_{i,j}\mid q,a_{i,<j})}{\pi_{\theta_{\mathrm{old}}}(a_{i,j}\mid q,a_{i,<j})}
$$

**符号说明**

- $\mathcal{J}_{\mathrm{GRPO}}$：需要最大化的 GRPO 训练目标。
- $\pi_{\theta}$：参数为 θ 的当前学生策略。
- $\pi_{\theta_{\mathrm{old}}}$：生成本轮训练轨迹的旧策略。
- $\pi_{\mathrm{ref}}$：用于衡量策略偏移的参考策略。
- $q$：从训练集采样的问题或提示。
- $N$：同一问题对应的学生轨迹数量。
- $a_i$：第 i 条完整学生推理轨迹。
- $|a_i|$：第 i 条轨迹的词元数量。
- $a_{i,j}$：第 i 条轨迹的第 j 个词元。
- $a_{i,<j}$：第 i 条轨迹在位置 j 之前的词元前缀。
- $r_{i,j}$：当前策略与旧策略生成该词元的条件概率之比，即重要性采样比。
- $A_{i,j}$：第 i 条轨迹第 j 个词元使用的优势；Cliff 用首错边界对其进行细化。
- $\epsilon$：概率比裁剪半径，用于限制单次策略更新幅度。
- $\beta$：KL 正则项权重；论文报告的 GRPO 与 Cliff 配置设为零。
- $\mathbb{D}_{\mathrm{KL}}[\pi_{\theta}\|\pi_{\mathrm{ref}}]_{i,j}$：在对应轨迹和词元位置上，当前策略相对参考策略的 KL 偏离惩罚。
- $\operatorname{clip}$：把重要性比限制在给定区间内的裁剪算子。
- $\mathbb{E}$：对训练问题及采样轨迹分布求期望。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标提升正优势词元的概率、降低负优势词元的概率，同时用裁剪避免新策略相对采样策略变化过猛。Cliff 并未替换优化器，而是通过更细的 $A_{i,j}$ 告诉同一个 GRPO 目标：错误答案中的哪些词元可以保留，哪些词元应被压低。<br>
**原文位置**：第 3.1 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### Cliff 逐词元优势及零均值偏移

$$
\mu=\frac{\sum_{i=1}^{N}R(q,a_i)}{N},\quad \sigma=\sqrt{\mu(1-\mu)},\quad A_{\mathrm{cor}}=\frac{1-\mu}{\sigma},\quad A_{\mathrm{inc}}=\frac{-\mu}{\sigma},\qquad A_{i,j}=\begin{cases}A_{\mathrm{cor}}-b,&R(q,a_i)=1,\\ \lambda A_{\mathrm{cor}}-b,&R(q,a_i)=0\ \text{and}\ j<\mathit{p}(a_i),\\ A_{\mathrm{inc}}-b,&R(q,a_i)=0\ \text{and}\ j\geq\mathit{p}(a_i),\end{cases}\qquad b=\frac{A_{\mathrm{cor}}\sum_{i:\,R(q,a_i)=1}|a_i|+\sum_{i:\,R(q,a_i)=0}\left[\lambda A_{\mathrm{cor}}\mathit{p}(a_i)+A_{\mathrm{inc}}\bigl(|a_i|-\mathit{p}(a_i)\bigr)\right]}{\sum_{i=1}^{N}|a_i|}
$$

**符号说明**

- $R(q,a_i)$：自动验证器给问题 q 与轨迹 $a_i$ 的二值结果奖励，正确为 1、错误为 0。
- $\mu$：同一问题的 N 条轨迹中的平均奖励，即组内正确率。
- $\sigma$：二值组奖励的标准差；当组内全对或全错时为零。
- $A_{\mathrm{cor}}$：由组内奖励标准化得到的正确轨迹基础优势。
- $A_{\mathrm{inc}}$：由组内奖励标准化得到的错误轨迹基础优势。
- $\mathit{p}(a_i)$：教师定位的第 i 条轨迹首个错误步骤边界。
- $j$：轨迹中的词元位置索引。
- $\lambda$：控制错误轨迹有效前缀正向强化强度的非负超参数；实验采用 0。
- $b$：塑形后、重中心化前的全组平均逐词元优势，从所有轨迹总词元数上计算。
- $A_{i,j}$：重中心化后分配给第 i 条轨迹第 j 个词元的最终 Cliff 优势。
- $|a_i|$：第 i 条轨迹包含的词元数。
- $N$：同一问题下参与组相对比较的轨迹总数。

<div class="equation-explanation" markdown="1">

**直观理解**：组内正确率决定基础奖励尺度：某条正确答案在正确答案稀少的组中会获得更大的相对优势，而错误答案获得负优势。Cliff 随后利用 $p(a_i)$ 修改错误轨迹内部的信号；减去 $b$ 可防止塑形整体抬高或压低更新方向，使变化主要来自词元之间的相对责任分配。<br>
**原文位置**：第 3.2.2 节，公式（3）—（5）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练仍最大化 GRPO 的裁剪代理目标，但把标准 GRPO 中一条轨迹共享的结果级优势替换为 Cliff 的逐词元优势 $A_{i,j}$。对于正确轨迹，各词元共享正向基础优势；对于错误轨迹，$p(a_i)$ 之前与之后采用不同信号，并通过 $b$ 重中心化。实际取 $\lambda=0$，意味着有效前缀在减去 $b$ 前不额外获得正奖励，核心作用是避免它与错误后缀一起继承 $A_{\mathrm{inc}}$；首错及其后缀仍承受负反馈。若教师参考解未通过验证，则不使用过程信号，直接按标准 GRPO 更新。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 经验证的教师判断器**

教师先产生自己的参考解，参考解通过自动验证后，教师才结合问题、参考解和学生轨迹判断答案正确性并定位 $p(a)$；若参考解未通过验证，则对应问题组回退到标准 GRPO。判断提示要求教师忽略无害笔误和不同但有效的解法，只寻找真实推理错误。

> 直观理解：教师既是解题者也是审阅者，但系统先检查其解题结果，减少“不会做却硬点评”的风险。

**2. 首错边界分解**

Pitfall Step $p(a)$ 是推理首次变得错误的步骤索引，它将错误轨迹划分为 $j<p(a)$ 的有效前缀和 $j\geq p(a)$ 的错误后缀。对超长轨迹设 $p(a)=0$，既节省判断成本，也避免模型通过生成冗长前缀获得不当收益。

> 直观理解：方法关心的是错误最早在哪里产生，而不是在错误已经发生后继续逐句打分。

**3. Cliff 优势塑形器**

该模块以 GRPO 的组相对优势为基础，把错误轨迹原本统一的负优势拆分到不同区段，并用 $b$ 保持组内逐词元优势零均值。$\lambda$ 控制错误轨迹有效前缀的正向强化强度，论文实际使用 $\lambda=0$ 以抑制长度投机。

> 直观理解：它把“整条答案错了”的粗反馈改成“前面先保留、从第一处错误开始惩罚”的细反馈，同时维持 GRPO 所依赖的相对比较尺度。

**训练与推理**

训练阶段，从 $D$ 中反复采样问题，每题由旧策略以温度 $\tau=1.0$ 生成 $12$ 条轨迹，自动验证器计算结果奖励。教师以温度 $0.6$ 生成参考解；参考解验证正确后，教师检查学生轨迹并给出 $p(a_i)$，系统据此计算 Cliff 优势并执行 GRPO 更新。若参考解错误则回退到标准 GRPO；若组内奖励全同，则因为标准化组优势为零而跳过教师判断。推理阶段不再需要教师、参考解或 Pitfall Step 判断，只使用训练后的学生模型进行贪心解码，因此 Cliff 的额外教师开销仅发生在训练期间。

**复现信息**

论文基于 veRL 实现。GRPO 与 Cliff 使用学习率 $1\mathrm{e}{-6}$、批大小 $64$、每题 $12$ 条 rollout、训练 $200$ 步、最大训练响应长度 $4096$、优势裁剪参数 $\epsilon=0.2$、KL 权重 $\beta=0$；Cliff 专用参数为 $\lambda=0$，教师 rollout 温度为 $0.6$。推理采用贪心解码，最大响应长度为 $8192$。这些设置中最影响方法解释的是 $\lambda=0$：它用于避免模型通过扩展被视为有效的前缀来进行长度投机；对超过长度限制的轨迹设 $p(a)=0$，使其全段接受问题后缀对应的反馈。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学训练集包括 DAPO-math-17k-processed，表 5 报告训练规模为 13,116；数学评测集包括 GSM8K（1,319 个评测样本）、MATH-500（500 个）和 DAPO（1,000 个），另使用 AIME（933 个）评估较高难度的数学推理。训练数据用于 RL，评测数据用于比较最终解题能力。
- 代码训练使用 DeepCoder，表 5 报告其训练规模为 13,485；代码评测包括 CodeContests（400 个）、LiveCodeBench（611 个）和 DeepCoder（500 个）。代码任务采用单轮设置，模型不能预先运行代码，评测时在沙箱中执行并检查测试用例。
- OpenThoughts 用于 Qwen3-4B-Base 的 RL 前监督微调，表 5 报告其规模为 113,957；它不是最终评测集，而是为该学生模型补充指令遵循能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**单任务准确率**

模型在 GSM8K、MATH-500、DAPO 和 AIME 等数据集上得到正确最终答案的比例；数学任务中解析模型输出的最后整数、分数或 boxed 内容并与真值比较。 （越高越好，因为它表示最终解题成功率更高。）

</div>
<div class="metric-item" markdown="1">

**Avg. Acc.**

表中各数学评测集准确率的平均值，用于概括模型在不同难度与分布上的总体推理表现。 （越高越好，但它不能替代对单个数据集的分析，也不能说明所有任务都同步提升。）

</div>
<div class="metric-item" markdown="1">

**Avg. Len.**

生成回答的平均长度，用于观察性能变化是否伴随不必要的推理延长或长度投机。 （不存在单纯的越高或越低；在准确率相近时通常更短更有效，但过短也可能损害推理完整性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-4B 学生模型、SOTA 教师、使用地面真值过滤

<div class="result-value" markdown="1">

相对于标准 GRPO，平均准确率从 61.68 提升到 65.66；GSM8K、MATH-500、DAPO 和 AIME 分别为 93.17、83.20、49.30 和 36.98。作者将此作为 Cliff 的主要性能提升证据。

</div>

在教师参考解经过自动验证器筛选时，首次错误监督比只看最终对错更能帮助学生学习推理过程。该结果证明了在这些数学基准和该训练配置下的有效性，但不能单独证明 Cliff 在所有模型、任务或教师质量下都稳定提升。

<div class="result-source" markdown="1">

来源：Table 3, Comparison of Cliff with and without ground truth

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen3-4B SOTA Yes 93.17 83.20 49.30 36.98 65.66

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-4B 学生模型、SOTA 教师、不使用地面真值过滤

<div class="result-value" markdown="1">

平均准确率为 64.90，仅比使用过滤时的 65.66 低 0.76 个百分点，并仍高于标准 GRPO 的 61.68；四个数据集得分为 93.25、81.20、48.50 和 36.65。

</div>

强教师生成的参考解本身已经足够可靠，因此即使没有外部真值筛选，Cliff 仍能提供有效过程监督。这说明方法可能适用于缺少可验证真值的场景，但结果只覆盖文中该 SOTA 教师和这些数学评测集，不能据此断言所有强教师都不需要过滤。

<div class="result-source" markdown="1">

来源：Table 3, Comparison of Cliff with and without ground truth

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen3-4B SOTA No 93.25 81.20 48.50 36.65 64.90

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen3-4B 学生模型、标准 GRPO 基线

<div class="result-value" markdown="1">

标准 GRPO 的平均准确率为 61.68，GSM8K、MATH-500、DAPO 和 AIME 分别为 92.80、79.00、42.90 和 32.01；平均生成长度为 1,279。

</div>

这是判断 Cliff 是否改善最终推理效果的参照点。它显示标准结果奖励已经能取得较高的简单数学题表现，但在 MATH-500、DAPO 和 AIME 等更具挑战的集合上，仍有空间让过程级信号提供更细致的训练指导。

<div class="result-source" markdown="1">

来源：Table 3, Comparison of Cliff with and without ground truth

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GRPO Yes 92.80 79.00 42.90 32.01 61.68

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 标准 GRPO：使用自动验证器提供的结果反馈，不提供 Cliff 的首次错误位置监督，是判断细粒度过程奖励是否带来增益的直接基线。
- 带地面真值过滤的 Cliff：教师生成的参考解必须先由自动验证器确认正确，否则退回使用 vanilla GRPO；该设置检验 Cliff 在较可靠参考解条件下的效果。
- 不带地面真值过滤的 Cliff：所有过程反馈只依赖教师自生成的参考解及其判断，用于检验方法在缺少可靠外部真值时是否仍然有效。
- 不同能力教师的 Cliff：比较 frontier-model 教师 Qwen3-32B（文中记为 SOTA）、Qwen3-32B 配置和 Gemma3-27B 配置；这些比较主要测试教师能力与参考解质量对 Cliff 的影响，而不是独立的训练算法基线。

**实验想回答的问题**

- 在数学推理与代码生成任务上，Cliff 是否比仅使用结果奖励的标准 GRPO 以及其他教师监督设置更有效？
- Cliff 对地面真值过滤器和超参数 $\lambda$ 的依赖程度如何，移除过滤器或改变正向优势强度会怎样影响性能与生成长度？

**实验实现**

实验使用两个学生模型：Qwen3-4B-Base 与 Phi-4-mini-Instruct；教师模型包括 Qwen3-32B 和 Gemma3-27B，另有文中称为 SOTA 的 frontier-model 教师。Qwen3-4B-Base 在 RL 前先用 OpenThoughts 做监督微调。数学评测不使用 system prompt，只输入原始问题；代码评测将原始问题、一个输入输出示例和编程说明组合为 user prompt。代码答案抽取代码块后在 VolcEngine sandbox 中执行，每道题使用 10 个测试用例、单次时间限制为 5 秒，只有全部通过才记为 1 分。表 3 的主比较报告 GSM8K、MATH-500、DAPO、AIME 及平均准确率；表 4 额外报告平均生成长度。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除地面真值过滤器 | 对于 Qwen3-4B 与 SOTA 教师，平均准确率由 65.66 变为 64.90；对于 Qwen3-4B 与 Qwen、Gemma 教师，平均准确率分别由 64.62 变为 62.69、由 63.70 变为 62.35。对于 Phi-4-Mini，SOTA、Qwen、Gemma 配置分别由 51.73 变为 51.46、由 51.48 变为 49.72、由 50.90 变为 48.30。 | 该消融隔离了外部正确性验证的作用。强教师移除过滤后损失很小，表明其参考解较可靠；较弱教师损失更明显，说明错误参考解会污染对学生 rollout 的判断。它没有证明过滤器在所有任务中都必要，因为强教师仍可在无过滤条件下工作。 | Table 3, Comparison of Cliff with and without ground truth; Section 6.1<br><span class="experiment-evidence">Qwen3-4B SOTA Yes 93.17 83.20 49.30 36.98 65.66; No 93.25 81.20 48.50 36.65 64.90</span> |
| 改变正向优势权重 $\lambda$ | $\lambda=0$ 的平均准确率为 65.66、平均长度为 1,506；$\lambda=0.5$ 为 64.67 和 1,481；$\lambda=1.0$ 为 63.98 和 1,959。标准 GRPO 为 61.68 和 1,279。 | $\lambda$ 控制错误轨迹中正确前缀获得的正向优势强度。增大它并未带来更高准确率，且 $\lambda=1.0$ 明显拉长回答，作者认为这是长度投机：模型可能反复保留并延长已经正确的前缀，而不是继续解决更困难的步骤。因此主实验采用 $\lambda=0$。 | Table 4, Cliff with different λ values; Section 6.2<br><span class="experiment-evidence">λ=1.0 93.252 81.2 47.8 33.655 63.98 1959</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The contribution is a fine-grained reward-shaping method for RLVR post-training that improves intermediate LLM reasoning by identifying the first error.; rule check: matched taxonomy keywords; top rule score=11.0
- 全文指纹：`3d6b3410b2db7ed53b1ee76d8201c16133248db97a949781a6a5b7ea120707be`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
