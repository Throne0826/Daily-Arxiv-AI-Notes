---
title: "[论文解读] A Model with No Head and Many Thoughts"
description: "[arXiv 2608.31069][LLM Reasoning] 本文提出软潜在思考（Soft Latent Thinking，SLT），在内部推理阶段用小型可学习潜在投影器替代完整词表头，使语言模型直接在连续嵌入空间中展开推理，以降低单步计算成本并提升多次采样时的答案覆盖率。"
arxiv_id: "2608.31069"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:42:02.409055+00:00"
source_sha256: "fa56cf85853ca7901526c3964f92b63a3bc2ad2ad9f9ba2d94e6f7775b0985b6"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "LLM 其他"
  - "大语言模型"
  - "思维链推理"
  - "软思考"
  - "连续潜在推理"
  - "Gumbel-Softmax"
  - "强化学习"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.31069</p>

# A Model with No Head and Many Thoughts

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Nikita Koriagin, Yaroslav Aksenov, George Bredis, Gleb Gerasimov, Nikita Balagansky, Daniil Gavrilov</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.31069v1) · [PDF 下载](https://arxiv.org/pdf/2608.31069v1) · **关键词** 大语言模型, 思维链推理, 软思考, 连续潜在推理, Gumbel-Softmax, 强化学习<br>


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

本文提出软潜在思考（Soft Latent Thinking，SLT），在内部推理阶段用小型可学习潜在投影器替代完整词表头，使语言模型直接在连续嵌入空间中展开推理，以降低单步计算成本并提升多次采样时的答案覆盖率。

**不用术语来说**：语言模型通常在每一步思考时都要从整个词表中计算下一个词，即使这些中间内容只服务于内部推理，也要反复执行昂贵的词表投影，并把思路强制写成词或词的混合。论文要解决的问题是：能否让模型用更小、更便宜的内部表示继续思考，直到需要输出最终答案时才恢复普通文本生成。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出SLT：仅在推理阶段将完整词表投影替换为规模为$K$的紧凑潜在投影器，其中$K\ll V$；模型根据隐藏状态生成潜在基的系数，并直接合成下一步连续推理状态，而最终回答仍采用标准离散词元解码。
- 为连续潜在动作构造可用于强化学习的逐步似然，并允许只训练投影器与潜在基，或配合LoRA进行轻量适配；作者还将高$k$下的收益归因于压缩潜在算子带来的推理路径多样性，而不只是单次答案精度。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型的推理阶段。标准自回归模型先把上下文编码为隐藏状态 $h_t$，再通过覆盖完整词表的语言模型头 $W_{\mathrm{head}}$ 得到下一个离散词元的概率；思维链（CoT）通过生成中间词元增加测试时计算，以提升复杂数学任务的求解能力。软思考进一步将中间步骤表示为连续嵌入：它不选取单个词元，而按词表概率混合所有词元嵌入，并把所得向量送入下一步。这样可以在连续空间传递信息，但每一步仍需执行规模为 $V$ 的词表投影与归一化，而且中间状态仍被限制为词元嵌入的加权组合。本文所处的核心问题因此是：能否在内部推理时绕过完整语言模型头，直接生成连续推理状态，同时保留最终答案的标准离散词元解码能力，并使这种连续决策能够接受强化学习训练。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自回归解码与语言模型头**

自回归模型根据已有上下文逐步预测下一项；在第 $t$ 步，语言模型头把 $d$ 维隐藏状态投影为 $V$ 个词元的分数，再经 softmax 得到概率。由于通常 $V$ 很大，这个完整词表投影在长推理轨迹中会反复产生计算开销。

</div>
<div class="concept-item" markdown="1">

**软思考（Soft Thinking）**

软思考不把中间推理步骤离散化为某个词元，而是用概率 $p_{t,i}$ 对全部词元嵌入 $e_i$ 加权，形成连续向量 $s_t=\sum_{i=1}^{V}p_{t,i}e_i$。直观上，它把“必须选一个词”改成“按不同程度混合许多词”，但仍依赖完整词表概率。

</div>
<div class="concept-item" markdown="1">

**Gumbel-Softmax 与策略梯度**

Gumbel-Softmax 向概率分数加入随机噪声，并通过温度控制的连续 softmax 产生可探索、可微的近似选择。SofT-GRPO 不直接给连续软词元定义类别概率，而给生成它的 Gumbel 随变量计算逐步似然，从而构造强化学习所需的重要性比率。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定问题文本 $\boldsymbol{Q}$ 和一个预训练自回归语言模型，模型需要先产生若干内部推理状态，再输出离散答案 $\boldsymbol{A}$。标准解码在每一步计算 $p(x_t\mid x_{<t})=\operatorname{softmax}(W_{\mathrm{head}}h_t)$；已有软思考则由该词表分布合成 $s_t$ 并将其反馈到下一步。本文关注仅替换“内部推理”算子的设定：推理阶段应从 $h_t$ 直接得到连续状态，避免每步执行 $V$ 维完整词表投影；进入最终回答阶段后仍使用原有语言模型头生成普通词元。其基本假设是潜在基底规模 $K$ 显著小于词表规模 $V$，即 $K\ll V$，且连续推理动作必须具有可计算的逐步似然，才能用 GRPO/PPO 风格的策略梯度稳定优化。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$h_t\in\mathbb{R}^{d}$**

第 $t$ 个解码步骤的隐藏状态，其中 $d$ 是模型隐藏维度。

</div>
<div class="notation-item" markdown="1">

**$W_{\mathrm{head}}\in\mathbb{R}^{V\times d}$**

标准语言模型头，将隐藏状态投影到含 $V$ 个词元的完整词表空间。

</div>
<div class="notation-item" markdown="1">

**$s_t=\sum_{i=1}^{V}p_{t,i}e_i$**

已有软思考方法生成的连续软词元；$p_{t,i}$ 是第 $i$ 个词元的概率，$e_i$ 是其嵌入。

</div>
<div class="notation-item" markdown="1">

**$B\in\mathbb{R}^{d\times K}$**

本文采用的可学习潜在基底；其 $K$ 个方向用于合成连续推理状态，并满足 $K\ll V$。

</div>

</div>

**直接相关的工作**

- **Soft Thinking（Zhang et al., 2025）**: 该工作将中间推理从离散词元扩展为概率加权的连续词元嵌入，是本文直接采用的问题起点。其无需额外训练即可运行，但每一步仍通过完整语言模型头计算 $V$ 维分布，且生成状态只能位于词元嵌入所张成的空间内。
- **SofT-GRPO（Zheng et al., 2025）**: 该工作通过 Gumbel-Softmax 增加软推理轨迹的随机探索，并以底层 Gumbel 变量的似然构造 GRPO/PPO 风格的重要性比率，使连续中间状态可由强化学习优化。本文沿用“为潜在动作定义可处理似然”的思路，但把选择空间从完整词表的 $V$ 个方向缩小为可学习潜在基底的 $K$ 个方向。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

思维链通过增加中间推理步骤来改善复杂任务表现，但长推理轨迹会反复调用维度为$V$的完整词表头，完成大规模投影与归一化。随着推理步数增长，这一操作成为明显的计算瓶颈；同时，中间状态必须借助离散词元语义表达，也限制了模型在连续表示空间中进行更灵活状态转移的可能性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **离散词元思维链**：模型在每个中间步骤把隐藏状态送入语言模型词表头，得到覆盖$V$个词元的概率分布，再采样或选择一个离散词元作为下一步输入。它能通过延长推理过程分配更多计算，但所有中间思路都必须显式词元化。
- **基于完整词表的软思考及其强化学习版本**：软思考不必选出单个词元，而是先经完整词表头计算$V$维概率，再对全部词元嵌入加权求和，将所得连续向量送入下一步；SofT-GRPO等方法进一步用强化学习优化这种连续推理过程。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有软思考仍在每一步计算完整的$V$维词表分布，因此保留了大规模词表投影与归一化的主要成本；在长推理轨迹中，这会削弱连续推理本应具有的计算效率优势。
- 软状态由词元嵌入的加权混合构成，因而仍被绑定到离散词元语义及词元嵌入张成的表示范围；它虽然不是单个词元，却没有真正摆脱以完整词表为中介的内部推理机制。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究表明连续软状态和强化学习可以改善推理，但尚未解决如何同时去除每步完整词表计算、摆脱对词元混合的结构性依赖，并为新的连续潜在动作保留可处理的强化学习策略似然。换言之，缺少一种只改变内部推理算子、仍能轻量训练且不破坏最终标准文本输出的端到端方案。

</div>
<div markdown="1"><span>核心问题</span>

能否在推理阶段把$V$维词表头替换为$K\ll V$的可学习潜在投影器，直接自回归生成连续嵌入状态，并在降低单步计算量的同时维持或改善数学推理表现，尤其是多次采样条件下的$\mathrm{pass}@k$？

</div>
<div markdown="1"><span>作者直觉</span>

中间推理状态并不一定需要对应可读词语；只要它能携带下一步计算所需的信息，就可以由少量可学习的潜在方向组合表示。用较小的潜在基代替整个词表，好比让模型先用内部速记推演，最后再翻译成正常文本：这既缩短了每一步的投影路径，也可能通过受控随机性探索更多不同的解题路线。不过作者也指出，这种基于领域词元初始化的内部速记具有领域依赖性，数学初始化的投影器在代码任务HumanEval上会退化。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Soft Latent Thinking 在推理阶段暂时绕过参数量和计算量都较大的词表输出头，不再把每一步思考强制转换成离散词元。给定当前上下文，基础语言模型先产生末层隐藏状态 $h_t$；一个由编码器、Gumbel-Softmax 采样器和解码器组成的潜在投影器，将 $h_t$ 压缩为 $K$ 个潜在类别上的分布，再还原成连续软嵌入 $s_t$。该嵌入直接作为下一步输入，因而形成自回归的连续推理轨迹。潜在空间满足 $K\ll V$：原文采用约 $12\text{k}$–$24\text{k}$ 个潜在类别，而完整词表约为 $150\text{k}$，所以推理步骤无须反复执行完整词表投影。

训练沿用 SofT-GRPO 的强化学习框架，但把原先覆盖完整词表的随机变量改为覆盖潜在类别。旧策略负责采样并保存 Gumbel 扰动和软嵌入；当前策略在相同软上下文上重算这些已保存随机变量的似然，由新旧似然之比构造 GRPO 更新。潜在推理结束后，模型重新启用标准语言模型头生成可读答案。直观地说，该方法让模型先在一个较小、可学习的“连续草稿空间”中思考，只有最终作答时才把内容翻译成普通词元。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 隐藏状态提取与潜在编码

将当前上下文 $c_t=[Q;(s_1,\ldots,s_{t-1})]$ 输入基础语言模型得到末层隐藏状态 $h_t\in\mathbb{R}^d$，再通过线性编码器计算 $K$ 维潜在 logits，即 $z_t=W_{\mathrm{enc}}h_t$。

<div class="method-step__io" markdown="1">

**输入**：题目提示 $Q$、此前生成的软嵌入序列 $(s_1,\ldots,s_{t-1})$，以及基础模型参数。<br>
**输出**：隐藏状态 $h_t$ 和潜在类别 logits $z_t\in\mathbb{R}^K$。

</div>

**直观理解**：这一步没有在整个词表中挑选下一个词，而是先把模型的内部状态压缩成较小的“思维代码”候选集合。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 随机潜在采样与软嵌入解码

先对 $z_t$ 做 softmax 得到 $p_t$，加入独立 Gumbel 噪声后以温度 $\tau_g$ 计算混合权重 $y_t$，最后通过 $s_t=W_{\mathrm{dec}}^\top y_t$ 映射回模型的 $d$ 维输入嵌入空间。

<div class="method-step__io" markdown="1">

**输入**：潜在 logits $z_t$、Gumbel 温度 $\tau_g$、编码器和解码器参数。<br>
**输出**：连续软嵌入 $s_t\in\mathbb{R}^d$，以及训练时保存的扰动量 $g_t$ 和噪声 $\epsilon_t$。

</div>

**直观理解**：模型不是硬选一个代码，而是随机形成多个潜在代码的加权组合；随机性使训练能探索不同推理路径，解码器则把组合转换成语言模型能够继续处理的向量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 连续自回归推理与阶段切换

若尚未满足停止条件，就令 $c_{t+1}=[c_t;s_t]$ 并重复潜在推理；当 $s_t$ 与 $\texttt{</think>}$ 嵌入的余弦相似度超过阈值 $\delta$ 时终止，对没有显式思考边界的模型则检测其与 $\texttt{\backslash boxed}$ 嵌入的相似度是否超过 $\gamma$。

<div class="method-step__io" markdown="1">

**输入**：当前软嵌入 $s_t$、当前上下文 $c_t$ 和边界词元的嵌入。<br>
**输出**：一条长度可变的连续潜在推理轨迹，以及切换到答案生成阶段的信号。

</div>

**直观理解**：软嵌入既是下一步的“思考内容”，也可逐渐靠近“开始作答”的边界方向；检测到该方向后，系统停止内部草稿并进入正常输出。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 答案解码与强化学习更新

模型用标准词表头自回归生成最终答案并获得奖励 $R$；更新时固定已采样的 $g_t$ 和软上下文，在当前策略下重算其 Gumbel 似然，以新旧策略似然比和答案词元的分类似然比共同优化带裁剪与 KL 正则的 GRPO 代理目标。

<div class="method-step__io" markdown="1">

**输入**：潜在推理后的上下文、标准语言模型头、最终答案奖励 $R$，以及 rollout 中保存的 $(c_t,g_t,\epsilon_t,s_t)$。<br>
**输出**：更新后的基础模型、潜在编码器 $W_{\mathrm{enc}}$ 和潜在解码器 $W_{\mathrm{dec}}$。

</div>

**直观理解**：如果最终答案得分高，训练会提高产生整条已采样潜在思路的概率；如果得分低，则降低其概率，而答案部分仍按普通词元策略学习。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 潜在投影器的编码、采样与解码

$$
z_t=W_{\mathrm{enc}}h_t,\qquad p_{t,i}=\frac{\exp(z_{t,i})}{\sum_{j=1}^{K}\exp(z_{t,j})},\qquad g_{t,i}=\log p_{t,i}+\epsilon_{t,i},\ \epsilon_{t,i}\sim\mathrm{Gumbel}(0,1),\qquad y_{t,i}=\frac{\exp(g_{t,i}/\tau_g)}{\sum_{j=1}^{K}\exp(g_{t,j}/\tau_g)},\qquad s_t=W_{\mathrm{dec}}^{\top}y_t
$$

**符号说明**

- $h_t$：第 $t$ 个潜在推理步骤中，基础模型产生的 $d$ 维末层隐藏状态。
- $W_{\mathrm{enc}}$：把隐藏状态投影到 $K$ 个潜在类别的编码器矩阵。
- $z_t$：编码器产生的 $K$ 维未归一化潜在 logits。
- $p_{t,i}$：第 $t$ 步选择第 $i$ 个潜在类别的归一化概率。
- $\epsilon_{t,i}$：为第 $i$ 个潜在类别独立采样的标准 Gumbel 噪声。
- $g_{t,i}$：对数概率与 Gumbel 噪声之和，也是 rollout 后保存并用于似然评估的随机量。
- $\tau_g$：Gumbel-Softmax 温度；控制混合权重的尖锐或平滑程度。
- $y_t$：覆盖 $K$ 个潜在类别的可微混合权重向量。
- $W_{\mathrm{dec}}$：把潜在混合权重映射回 $d$ 维模型嵌入空间的解码器矩阵。
- $s_t$：作为下一推理步骤输入的连续软嵌入。
- $K$：独立潜在空间的类别数，显著小于完整词表大小。

<div class="equation-explanation" markdown="1">

**直观理解**：该组公式完整描述了“隐藏状态—潜在分布—随机软组合—输入嵌入”的转换。关键区别是 softmax 只在 $K$ 个潜在类别上执行，而且输出 $s_t$ 不必等于任何真实词元嵌入，因此既降低投影规模，也不把中间推理限制在离散语言语义中。<br>
**原文位置**：第 4 节，式 (5)–(6)；Gumbel-Softmax 定义引用第 3.2 节式 (1)–(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 潜在步骤的 Gumbel 似然与重要性比

$$
\log p_{\theta}(g_t\mid c_t)=\sum_{i=1}^{K}\left[-\left(g_{t,i}-\log p_{t,i}^{\theta}\right)-\exp\!\left(-\left(g_{t,i}-\log p_{t,i}^{\theta}\right)\right)\right],\qquad \log r_t=\log p_{\theta}(g_t\mid c_t)-\log p_{\theta_{\mathrm{old}}}(g_t\mid c_t)
$$

**符号说明**

- $c_t$：由题目和此前软嵌入组成的第 $t$ 步上下文。
- $\theta$：正在优化的当前策略参数，包括参与当前概率计算的模型与投影器参数。
- $\theta_{\mathrm{old}}$：生成 rollout 轨迹的旧策略参数。
- $p_{t,i}^{\theta}$：当前策略在上下文 $c_t$ 下赋给潜在类别 $i$ 的概率。
- $g_t$：由旧策略 rollout 采样并保存的整组 Gumbel 扰动后对数概率；更新时按常量处理。
- $p_{\theta}(g_t\mid c_t)$：保存的随机向量 $g_t$ 在当前策略所诱导移位 Gumbel 分布下的似然。
- $r_t$：当前策略与旧策略对同一潜在随机结果的逐步重要性比。

<div class="equation-explanation" markdown="1">

**直观理解**：连续软嵌入本身没有普通分类词元那样直接可用的概率，因此方法转而给生成它的底层 Gumbel 随机量计算似然。固定 rollout 中的 $g_t$ 后，梯度只通过当前概率 $p_{t,i}^{\theta}$ 传播；若某条轨迹得到高奖励，GRPO 就可借助 $r_t$ 提高当前策略复现该轨迹的相对可能性。<br>
**原文位置**：第 4.2 节式 (9)，其似然定义来自第 3.2 节式 (3)，并将词表大小 $V$ 替换为潜在类别数 $K$

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：方法没有另行提出新的总体强化学习目标，而是采用 SofT-GRPO 的带裁剪 GRPO/PPO 风格代理目标。对潜在推理前缀，优化器使用保存的 Gumbel 随机量构造逐步重要性比 $r_t$；对最终答案词元，则继续使用标准语言模型头提供的分类对数概率比。最终答案奖励 $R$ 为整条轨迹提供学习信号，裁剪限制新旧策略变化幅度，参考策略 KL 惩罚用于抑制训练漂移。

必须区分采样与更新：rollout 由 $\theta_{\mathrm{old}}$ 生成，保存的 $g_t$、$\epsilon_t$ 和 $s_t$ 在更新阶段不重新采样；当前策略 $\theta$ 只在同一上下文上重算 $p_t^{\theta}$。这种处理避免错误地让梯度穿过旧轨迹的随机采样过程，并使连续潜在步骤能够嵌入通常要求动作对数概率的策略梯度框架。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 低基数潜在编码器**

编码器是线性映射 $W_{\mathrm{enc}}\in\mathbb{R}^{K\times d}$，将 $d$ 维隐藏状态投影到 $K$ 个潜在类别。它以目标领域中最常见的 $K$ 个词元对应的预训练语言模型头行初始化，随后独立训练，不再与原语言模型头绑定。

> 直观理解：它相当于用较小的候选面板替换完整词表面板，从而减少每个思考步骤的投影开销；独立训练又允许这些类别逐渐脱离原词义，成为更适合推理的内部代码。

**2. Gumbel-Softmax 潜在采样器**

采样器对潜在概率 $p_{t,i}$ 加入独立 Gumbel 噪声 $\epsilon_{t,i}$，再以温度 $\tau_g$ 形成可微的混合权重 $y_t\in\mathbb{R}^K$。训练把扰动后的 $g_t$ 视为 rollout 中已经发生的随机结果，并计算其在当前策略下的似然。

> 直观理解：单纯使用概率均值容易反复依赖最高概率选项；加入噪声可探索不同潜在思路，同时软化后的权重仍能参与梯度训练。

**3. 潜在解码器与边界检测器**

解码器参数 $W_{\mathrm{dec}}\in\mathbb{R}^{K\times d}$ 将混合权重映射为 $s_t=W_{\mathrm{dec}}^\top y_t$，其初始化来自相同高频词元的输入嵌入行，之后与原嵌入表解耦。推理阶段通过 $s_t$ 与边界词元嵌入的余弦相似度判断何时恢复标准词元解码。

> 直观理解：解码器把内部代码翻译成模型下一层可读的输入向量；边界检测器则承担“什么时候停止想、开始说”的控制功能。

**训练与推理**

训练时，先以旧策略从题目 $Q$ 开始 rollout。每一步计算 $h_t$ 和潜在概率 $p_t$，采样 $\epsilon_t$，形成 $g_t$、$y_t$ 与 $s_t$，并把 $s_t$ 追加到上下文；同时保存 $(c_t,g_t,\epsilon_t,s_t)$。达到软停止条件或最大推理长度后，系统启用标准语言模型头生成最终答案并根据答案正确性获得奖励 $R$。随后当前策略重放已保存的软嵌入以保持上下文一致，重新计算潜在概率和 Gumbel 似然比，再结合答案词元比率、奖励、裁剪项及 KL 项更新基础模型和投影器。

推理时无需计算策略更新所需的似然，只重复潜在编码、Gumbel-Softmax 采样和软嵌入反馈。若模型具有显式 $\texttt{</think>}$ 边界，就检测 $\cos(s_t,e_{\texttt{</think>}})>\delta$；缺少该边界的检查点则检测 $\cos(s_t,e_{\texttt{\backslash boxed}})>\gamma$。一旦满足条件，系统停止连续推理并恢复完整词表头，以普通自回归方式生成用户可读的最终答案。

**复现信息**

为保留预训练模型已有语义结构，作者从目标领域最常见的 $K$ 个词元集合 $\mathcal{K}=\{k_1,\ldots,k_K\}$ 初始化投影器：$W_{\mathrm{enc}}[i,:]$ 复制语言模型头中词元 $k_i$ 的行，$W_{\mathrm{dec}}[i,:]$ 复制输入嵌入表中同一词元的行。初始化后两者均可训练，并与原语言模型头和输入嵌入表解除绑定；因此高频词元只提供合理起点，而不是对潜在类别语义的永久约束。

原文以 OpenThoughts-114k 的数学子集统计初始化词频，并指出最高频的 $5000$ 个词元覆盖接近 $99\%$ 的出现次数，但其消融结论认为约 $12\text{k}$ 个潜在类别效果最佳，说明仅覆盖绝大多数表面词频并不必然足够。停止阈值的初步检查显示，中间推理阶段与边界嵌入的余弦相似度通常低于 $0.2$，临近答案时才明显上升；作者据此称规则对适度阈值变化相对不敏感，但同时明确承认尚需完整阈值扫描，因此复现时不应把该稳健性视为已经充分验证。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学推理数据与评测：训练使用 DeepScaleR；评测使用 AIME2024、AIME2025、AMC23、MATH-500 和 GSM8K，用于检验模型在竞赛数学、标准数学题及小学数学文字题上的推理能力。原文未明确报告 DeepScaleR 的规模、划分及各评测集的具体样本数。
- 跨领域评测：GPQA Diamond 用于科学推理，HumanEval 用于代码生成；二者检验数学推理数据上训练的投影器是否会损害非数学任务。原文未明确报告这两个数据集的规模、划分及具体评测协议。
- 模型规模检查：在 Qwen3.5-9B 上进行一次未调参的 AIME2024 实验，用于观察方法能否从 1.5B–3B 模型迁移到更大模型；该实验不是完整的规模扩展研究。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**pass@$k$**

从同一题生成 $k$ 个样本，只要其中一个答案正确就计为成功；它衡量多次采样下找到正确推理路径的概率。 （越高越好；$k=1$ 更接近单次推理准确率，而较大的 $k$ 更能反映推理路径多样性和覆盖率。）

</div>
<div class="metric-item" markdown="1">

**平均推理 token 数（#Token 或 Avg. tokens）**

生成推理过程所使用的 token 数，用于衡量推理链长度和生成成本。 （在准确率相当时越低越好；但单独减少 token 不等于推理质量提高，因此必须结合 pass@$k$ 解读。）

</div>
<div class="metric-item" markdown="1">

**TPS 与 speedup**

TPS 是每秒生成 token 数，speedup 是方法相对于 vanilla 基线的吞吐比值，用于衡量实际服务效率。 （越高越好；它反映端到端服务吞吐，不完全等同于单个 LM head 解码步骤的理论 FLOPs 降低。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 数学推理主结果：DeepSeek-R1-Distill-Qwen-1.5B 与 LLaMA-3.2-3B-Instruct 在五个数学基准上的平均 pass@32

<div class="result-value" markdown="1">

DeepSeek-Qwen-1.5B 的 Soft Latent Thinking 平均 pass@32 为 86.22，高于基础模型的 83.23 和 SofT-GRPO 的 85.18；LLaMA-3.2-3B-Instruct 上为 60.70，高于基础模型的 56.26 和 SofT-GRPO 的 57.06。作者同时指出，方法主要改善多次采样时的准确率—效率权衡，而不是在每个采样预算上都全面领先。

</div>

这说明投影器与 Gumbel-Softmax 采样可能让不同 rollout 产生更有差异的推理路径，因此在允许采样 32 次时更容易覆盖正确路径。它支持方法在多样本推理和 RL 训练场景中的价值，但不能推出单次采样必然更准，也不能证明所有数据集、模型或采样预算都优于基线。

<div class="result-source" markdown="1">

来源：第 5.1 节 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On DeepSeek-R1-Distill-Qwen-1.5B, we achieve 86.22 average pass@32 compared to 83.23 for the base model and 85.18 for SofT-GRPO. On LLaMA-3.2-3B-Instruct, we achieve 60.70 average pass@32 compared to 56.26 for the base model and 57.06 for SofT-GRPO.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 较大模型的初步迁移：Qwen3.5-9B 在 AIME2024 上的单次与多次采样表现及 token 使用

<div class="result-value" markdown="1">

投影器模型的 Avg. tokens 为 9288.1、Correct tokens 为 7378.2、pass@1 为 68.4、pass@16 为 92.8、pass@32 为 93.3；基础 Qwen3.5-9B 分别为 23292.1、21778.6、76.4、93.2 和 93.3。

</div>

在这个未调参检查中，投影器模型单次准确率较低，但在 pass@32 上达到与基础模型相同的结果，同时平均 token 数显著更少。这表明效率—多次采样权衡可能迁移到更大模型，但由于只有一个未调参配置、没有完整基线扫描，不能视为确定的规模扩展结论。

<div class="result-source" markdown="1">

来源：第 5.2 节 Preliminary Larger-Model Check，表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This check is not intended as a full-scale evaluation, because we did not perform scale-specific hyperparameter tuning or a complete baseline sweep.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 计算与服务效率：替换词表 LM head 后的理论投影成本和 mini-SGLang 吞吐

<div class="result-value" markdown="1">

标准词表投影的每步 FLOPs 为 $2dV$，投影器的每步 FLOPs 为 $4dK$；在 $d=1536$、$V=150k$、$K=16k$ 的示例中，词表投影步骤理论上约减少 5 倍。mini-SGLang 原型中，Llama-3.2-1B 的 speedup 为 1.062–1.071 倍，Llama-3.2-3B 为 1.051 倍，Llama-3.1-8B 在 batch size 1、4、8 时分别为 1.032、1.256、1.137 倍。

</div>

理论计算量显示，压缩投影器的矩阵乘法规模远小于完整词表投影；端到端吞吐提升则较为温和，因为服务系统还包含主干网络、调度和其他开销。因而该结果支持“降低解码步骤成本”和“原型服务吞吐提升”两个较弱但互补的结论，不能把理论 5 倍直接等同于整体生成速度提升 5 倍。

<div class="result-source" markdown="1">

来源：第 5.5 节 Computational Efficiency，表 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The latter shows an approximately 1.05× decode speedup across tested models and is the cleaner measurement of the algorithmic gain from replacing the LM-head reasoning step.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验规模与完整性有限：Qwen3.5-9B 只进行了一个未调参配置，作者明确未做针对规模的超参数调优和完整基线扫描，因此不能据此建立可靠的规模扩展规律。
- 跨领域结论仍受任务、初始化词汇和训练分布影响。数学初始化投影器在 HumanEval 上退化，说明连续瓶颈并非天然任务无关；此外，摘录未报告所有主结果表、各数据集规模与完整统计显著性，具体数值和可重复性需要回查原文。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Base model：未微调的基础模型，用于衡量方法相对于原始模型的净增益。
- Base model + standard GRPO：使用标准 GRPO 微调的模型，用于比较连续潜在推理是否优于只改变训练目标而保留标准解码的方案。
- Soft-Thinking：不使用投影器、直接在完整词表上进行软推理；同时比较未微调和 GRPO 版本，用于区分“软推理本身”和“词表压缩投影器”的作用。
- SofT-GRPO：已有的基于完整词表软推理的 GRPO 方法，是最直接的强基线，用于检验 Soft Latent Thinking 的改进是否来自将推理空间压缩到 $K$ 维候选表示。

**实验想回答的问题**

- Soft Latent Thinking 是否能在数学推理任务中，相比标准离散解码、标准 Soft-Thinking 和 SofT-GRPO，提高多次采样下的推理覆盖率，即高 $k$ 时的 pass@$k$，同时减少推理 token 与语言模型词表投影的计算？
- 连续潜在推理是否具有迁移性与可部署性：它能否迁移到科学问答和代码生成，并在不同模型规模、投影器大小、训练配置及推理温度下保持有效？

**实验实现**

实验基于 DeepSeek-R1-Distill-Qwen-1.5B 和 LLaMA-3.2-3B-Instruct。投影器由编码矩阵 $W_{\mathrm{enc}}\in\mathbb{R}^{K\times d}$ 和解码矩阵 $W_{\mathrm{dec}}\in\mathbb{R}^{K\times d}$ 构成，设置 $K=8d$；因此 Qwen 的 $d=1536$、$K=12288$，LLaMA 的 $d=3072$、$K=24576$。训练使用 DeepScaleR、Soft-GRPO 和基于结果的奖励；冻结主干模型，同时训练所有注意力与 MLP 模块上的秩为 64 的 LoRA，以及投影器。主结果覆盖五个数学基准，并报告不同采样预算的 pass@$k$；跨领域实验比较基础模型、启用投影器的 LoRA，以及关闭投影器后使用完整词表的标准 Soft-Thinking。计算效率部分还在 mini-SGLang 原型中测试不同模型和 batch size 的 TPS。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 投影器训练与软推理形式：训练后的投影器、初始化投影器、以及固定 LoRA 下的完整词表 Soft-Thinking | 在 AIME2024 上，训练后的投影器为 pass@1=28.7、pass@16=74.3、pass@32=80.0、#Token=10280；初始化投影器为 28.3、70.1、76.7、11383；完整词表 Soft-Thinking 为 29.5、72.3、80.0、11242。 | 相对于初始化投影器，训练后的投影器在 pass@16 和 pass@32 更好且 token 更少，说明瓶颈并非仅靠裁剪词表就能使用，而需要学习连续表示。完整词表版本的 pass@1 更高，但 pass@16 更低且 pass@32 相同，支持作者关于压缩词表增加有益随机性、牺牲部分单样本精确度以换取多样路径的解释。 | 第 5.6 节 Effect of projector training，表 5<br><span class="experiment-evidence">Full vocabulary soft thinking achieves higher pass@1 but lower pass@16, with similar pass@32.</span> |
| 投影器大小与训练配置：不同 $K$，以及训练投影器配合 LoRA、冻结主干或初始化投影器 | 不同投影器大小的结果为：$K=1\times1536$ 时 pass@1/16/32=20.4/58.2/66.7、#Token=18694；$K=4\times1536$ 时为 29.7/62.0/66.7、14881；$K=8\times1536$ 时为 28.7/74.3/80.0、10280。训练配置中，训练投影器并训练 LoRA 为 28.7/74.3/80.0、10280；训练投影器但冻结主干为 26.0/65.4/70.0、12256；初始化投影器且冻结主干为 11.3/56.3/63.3、6370。 | 更小的 $K$ 容量不足，导致准确率和推理长度都变差；较大的投影器在多次采样指标上更有利，但实验只覆盖三种尺寸，不能确定最优规模的普遍规律。训练配置表明，主干需要通过 LoRA 适配连续软嵌入；只训练投影器不足，而投影器和 LoRA 联合训练能取得最佳结果。需要注意，不同 $K$ 的结果来自表 7，不应与表 8 的训练配置变化混为单一因果比较。 | 第 5.6 节 Projector size 与 Projector and backbone training，表 7、表 8<br><span class="experiment-evidence">Joint training of projector and LoRA achieves the best results, allowing both components to co-adapt.</span> |

**定性案例**

- 跨领域评测显示了一个具有部署意义的任务切换策略：GPQA Diamond 上，关闭投影器的 SLT† 达到 97.0，而 SofT-GRPO 为 95.5；HumanEval 上对应为 92.7 和 94.5。作者将差异归因于表示匹配：科学推理与数学共享数字、符号和形式化记号，而代码依赖 Python 关键字、标识符、语法及缩进标记。由此可将投影器用于数学等域内任务以追求效率，并在代码等域外任务中绕过投影器；不过这些数值来自表 9，所给摘录未提供完整表格行，具体评测统计仍需核对原文。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Soft Latent Thinking performs continuous-space autoregressive reasoning without the vocabulary head, improving reasoning performance while reducing per-step computation.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`fa56cf85853ca7901526c3964f92b63a3bc2ad2ad9f9ba2d94e6f7775b0985b6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
