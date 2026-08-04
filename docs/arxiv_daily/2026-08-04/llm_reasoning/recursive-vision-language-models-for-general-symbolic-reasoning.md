---
title: "[论文解读] Recursive Vision Language Models for General Symbolic Reasoning"
description: "[arXiv 2608.01534][LLM Reasoning] 本文研究如何在不改动预训练 Qwen 主干架构的前提下，通过显式递归地修正候选答案，使同一个模型能够处理数独、迷宫、ARC 和填字游戏等异构符号推理任务。"
arxiv_id: "2608.01534"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:04:52.742593+00:00"
source_sha256: "42098cd15f20f258854697edee7af0e9c23d88d18a4db200d6ebbc16c9e45fe0"
tags:
  - "LLM Reasoning"
  - "符号推理"
  - "递归推理"
  - "视觉语言模型"
  - "候选解优化"
  - "约束保持投影"
  - "自回归模型"
  - "Qwen"
  - "ARC-AGI"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.01534</p>

# Recursive Vision Language Models for General Symbolic Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Omid Nejati Manzari, Guillaume Lajoie, Hassan Rivaz</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Concordia University, Montreal, Canada；Mila — Quebec AI Institute</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01534v1) · [PDF 下载](https://arxiv.org/pdf/2608.01534v1) · **关键词** 符号推理, 递归推理, 视觉语言模型, 候选解优化, 约束保持投影, 自回归模型, Qwen, ARC-AGI<br>
**代码**: [https://github.com/IMPACT-L/RQwen](https://github.com/IMPACT-L/RQwen)

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

本文研究如何在不改动预训练 Qwen 主干架构的前提下，通过显式递归地修正候选答案，使同一个模型能够处理数独、迷宫、ARC 和填字游戏等异构符号推理任务。

**不用术语来说**：这类题目通常不能靠一次顺序生成稳定解决：模型若在前面填错一个数字、选择错误路径或误判图形规律，错误可能延续到整个答案，而标准语言模型又缺少反复检查、撤回并修正当前解答的内置过程。研究需要一种能让模型多轮审视同一候选答案、逐步纠错，同时仍可利用大规模预训练知识的通用机制。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 R-Qwen：在预训练 Qwen 主干之外以程序化方式反复调用同一个候选解精炼算子，并通过任务特定的序列化与保约束投影，将统一的递归搜索和修正框架用于数独、迷宫、ARC 与填字游戏，而无须修改主干网络结构。
- 将分层监督加权 HSW 适配到自回归模型，对不同递归步骤的监督损失进行指数加权，使较早、信息量较高的修正步骤获得更强训练信号；同时结合 LoRA、递归深度课程和逐实例提前停止，以参数高效方式学习递归精炼策略。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究通用符号推理：模型需要依据离散规则，通过搜索、回溯和反复修正生成精确的结构化答案，代表任务包括数独、迷宫寻路、ARC-AGI 和填字游戏。标准大语言模型通常以固定深度的 Transformer 自回归生成答案，早期错误容易沿后续序列传播，而且单次前向生成难以稳定执行多轮搜索；递归推理模型则复用同一计算模块，持续更新中间解，以增加有效计算深度而不主要依赖扩大参数量。本文关注如何把这种显式的递归候选解优化机制与预训练视觉语言模型已有的语言、视觉和推理先验结合起来，并在不同符号与空间任务之间复用。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自回归生成**

模型按照从左到右的顺序逐个预测输出符号，每一步都依赖此前已经生成的内容。其局限是早期预测一旦出错，错误会进入后续步骤的条件上下文并可能持续放大。

</div>
<div class="concept-item" markdown="1">

**递归候选解优化**

模型不把第一次生成视为最终答案，而是反复读取原问题和当前候选解，再输出一个改进版本。由于同一优化算子可以执行多次，模型获得了可调的计算深度，并能近似实现检查、修正和回溯。

</div>
<div class="concept-item" markdown="1">

**约束保持投影**

每轮生成后，程序依据具体任务的硬规则整理或修正候选解，使其回到允许的解空间，再交给下一轮递归。例如，它可用于保留题目中不可修改的已知条件，但原文节选未给出各任务投影规则的完整形式。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道来自数独、迷宫、ARC 或填字游戏的题目，以及递归过程中维护的当前序列化候选解；这些任务可能采用文本或视觉语言表示，但都要求满足离散规则并产生精确的结构化输出。每个递归步骤中，预训练 Qwen 主干同时接收原始问题与当前候选解，生成改进候选；随后任务专用的约束保持投影处理该候选，并将结果作为下一步输入。训练采用 LoRA 进行参数高效适配并对多个递归步骤实施深度监督；推理时可执行多轮优化并按实例提前停止。该设置的关键假设是：不同任务虽有不同的序列化和硬约束，却可以共享同一个学习到的候选解优化策略，而无需修改 Qwen 主干架构。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Hierarchical Reasoning Model（HRM）**: 直接相关的递归推理基线：通过迭代更新潜在状态增加计算深度，说明小型递归网络能够处理困难符号任务；与本文相比，它通常采用专门架构、面向较窄任务，并未利用预训练语言模型先验。
- **Tiny Recursive Model（TRM）**: 直接相关的轻量递归模型：以重复优化中间表示或解答的方式替代单次固定深度推理。本文继承其“以递归深度换取推理能力”的思路，但改为在预训练 Qwen 上显式递归当前候选解，并统一处理多类符号与空间任务。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

数独、迷宫寻路和 ARC 等任务要求系统搜索、回溯以及严格满足结构约束，答案往往只有完全正确才有意义。标准大语言模型按顺序一次生成答案，早期错误容易传播，且固定的 Transformer 计算深度限制了模型在单次前向过程中执行长程迭代，因此其在搜索密集型符号谜题上仍不可靠。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **思维链提示与测试时计算扩展**：让模型生成中间推理文本，或在推理阶段投入更多采样与计算，以延长表面上的推理过程并比较候选答案。
- **HRM、TRM 等递归推理模型**：重复更新内部潜在状态或中间表示，用共享的小型网络增加有效计算深度，使模型通过多轮迭代逐渐接近满足约束的解，而不是单纯增加参数量。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 思维链和额外测试时计算在需要大量搜索与回溯的问题上仍较脆弱，而且常依赖较多推理过程监督；一旦中间文本走向错误分支，后续生成未必能可靠恢复。
- 既有递归方法通常在潜在空间中运行、依赖专用架构或面向单一任务族，也可能只递归改写提示而不直接修正显式候选解；这限制了它们复用预训练语言与视觉语言先验并跨异构任务迁移的能力。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚未证明：一个预训练自回归模型能否在保持主干架构不变的情况下，学习可跨任务复用的显式候选解精炼策略，并在每轮递归中利用当前答案、执行受约束的修正，而非仅更新不可解释的潜在状态或重新组织提示。

</div>
<div markdown="1"><span>核心问题</span>

能否把预训练 Qwen 作为共享精炼器，使其反复接收原始问题与当前序列化候选解，在任务硬约束保护下生成更好的下一候选解，并通过跨递归步骤的深度监督稳定地学会这一过程，从而统一解决多类符号和空间推理任务？

</div>
<div markdown="1"><span>作者直觉</span>

预训练模型已经具备语言、语义、视觉表示和一般推理先验，但一次性生成没有给它可靠的纠错机会；递归机制则擅长把复杂求解拆成多次局部改进。把两者结合后，每一轮只需在当前答案基础上发现并修正部分错误，投影步骤负责阻止修正破坏不可违反的规则，而对早期步骤施加更强监督可促使模型尽快取得实质进展。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

R-Qwen把数独、迷宫、ARC 和填字游戏统一为“序列化约束满足”问题：每个样本表示为原始实例 $\bm{x}$、可选上下文 $c$ 和目标解 $\bm{y}^{\ast}$，并以 $\hat{\bm{y}}^{(0)}=\bm{x}$ 初始化候选解。一个冻结主体参数、仅训练 LoRA 适配器的 Qwen3.5-27B 自回归模型反复读取原问题、当前候选解和递归步编号，生成新的完整候选；任务专属投影随后恢复固定线索、过滤非法符号并规范长度，再把结果送入下一轮。不同任务共享模型、训练目标与递归算法，仅序列化格式、合法符号集合和约束投影不同。

训练时，每个递归步都要求模型在当前候选条件下输出完整标准答案，即采用深度监督，而不只监督最后一步。作者进一步用层次监督加权 HSW，使早期、通常改动较大的步骤获得更高损失权重，后期步骤仍保留较小权重；训练初期采用较短监督深度，随后逐渐增加递归步数，并通过候选生成摊销和按样本提前停止降低计算量。直观地说，该方法把同一个语言模型训练成“通用改卷器”：它多次查看题目和上一版答案，每次尝试修正错误，而规则投影充当硬性格式检查器，确保错误生成不会破坏题目给定条件。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 统一序列化与候选初始化

将网格、路径、颜色或字母等结构编码为长度为 $L$ 的字符串，并定义任务字母表 $\Sigma$ 与固定位置集合 $\mathcal{G}(\bm{x})=\{i:x_i\neq\varnothing\}$；初始候选设为 $\hat{\bm{y}}^{(0)}=\bm{x}$。

<div class="method-step__io" markdown="1">

**输入**：任务实例，包括结构化初始状态 $\bm{x}$、可选上下文 $c$ 和训练时可用的目标解 $\bm{y}^{\ast}$。<br>
**输出**：统一表示的实例 $(\bm{x},c,\bm{y}^{\ast})$、合法符号与结构约束，以及首个候选解 $\hat{\bm{y}}^{(0)}$。

</div>

**直观理解**：无论原题是数独、迷宫还是填字游戏，模型看到的都是“题目、当前答案和必要说明”组成的文本。题目已给出的数字、墙或预填字母会被标记为不可修改。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造递归提示

提示构造器 $P(\bm{x},c,\hat{\bm{y}}^{(t-1)},t,N)$ 生成聊天格式输入，明确给出原题、当前候选和递归进度，并要求模型返回遵守固定位置约束的完整序列化答案。

<div class="method-step__io" markdown="1">

**输入**：原始实例 $\bm{x}$、上下文 $c$、上一轮候选 $\hat{\bm{y}}^{(t-1)}$、当前步 $t$ 和总递归深度 $N$。<br>
**输出**：供自回归模型处理的候选条件提示。

</div>

**直观理解**：每一轮不是让模型从空白重新解题，而是把上一版答案交回去并要求继续修正。步编号让模型知道当前处于多轮修改过程的哪个阶段。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自回归生成与约束投影

模型以贪心解码产生原始字符串 $\tilde{\bm{y}}^{(t)}$，再由任务专属投影 $\Pi_{\bm{x}}$ 得到 $\hat{\bm{y}}^{(t)}$：固定位置恢复为题目值，合法的新符号予以采用，非法或缺失位置沿用上一轮值，并将序列截断或填充到长度 $L$。

<div class="method-step__io" markdown="1">

**输入**：当前递归提示和由冻结骨干加 LoRA 适配器组成的条件语言模型 $\pi_{\theta}$。<br>
**输出**：格式正确、保留题目固定条件的下一轮候选解 $\hat{\bm{y}}^{(t)}$。

</div>

**直观理解**：语言模型负责提出修改，投影器负责执行不可违反的规则。即使模型少输出、输出了非法字符或改动了题目线索，投影也能把候选恢复为可继续处理的状态。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 逐步深度监督与 HSW 优化

每一步都以教师强制计算目标答案 token 的平均交叉熵，提示 token 不计入损失；随后按归一化权重 $w_t\propto\lambda^{t-1}$ 加权，并更新 LoRA 参数。候选状态经解码产生后会停止梯度，后续步骤把它视为固定输入，因此不会跨整条递归轨迹反向传播。

<div class="method-step__io" markdown="1">

**输入**：各递归步的候选条件提示、完整目标解 $\bm{y}^{\ast}$、当前有效深度 $N$ 和衰减率 $\lambda$。<br>
**输出**：经过优化的共享 LoRA 适配器，以及能够从不同质量候选恢复到完整解的递归修正算子。

</div>

**直观理解**：模型在每轮都接受“正确完整答案”的批改，而不是等最后一轮才知道对错。HSW 更重视前几轮的大幅纠错，并减轻后期小改动或无效改动带来的噪声。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 递归生成与约束投影

$$
\tilde{\bm{y}}^{(t)}=\mathrm{Decode}_{\theta}\!\left(P(\bm{x},c,\hat{\bm{y}}^{(t-1)},t,N)\right),\qquad \hat{\bm{y}}^{(t)}=\Pi_{\bm{x}}\!\left(\tilde{\bm{y}}^{(t)}\right)
$$

**符号说明**

- $\bm{x}$：序列化原始题目或初始状态。
- $c$：可选辅助上下文，如自然语言线索或示范输入输出对。
- $\hat{\bm{y}}^{(t-1)}$：第 $t-1$ 步经过投影后的候选解。
- $t$：当前递归或精炼步骤编号。
- $N$：当前过程计划执行或监督的总递归步数。
- $P$：把题目、上下文、当前候选和递归进度渲染为聊天提示的构造器。
- $\mathrm{Decode}_{\theta}$：参数为 $\theta$ 的自回归模型及其贪心解码过程。
- $\tilde{\bm{y}}^{(t)}$：模型在第 $t$ 步直接生成、尚未校验的原始候选字符串。
- $\Pi_{\bm{x}}$：依赖原题的确定性约束投影，负责固定线索、合法字符和长度等约束。
- $\hat{\bm{y}}^{(t)}$：第 $t$ 步投影后的候选状态，也是下一步递归的输入。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分让模型根据题目和上一版答案写出改进版，第二部分再用硬规则清理该输出。这个“生成后投影”的闭环是端到端方法的核心，因为它既允许语言模型自由提出修正，又保证递归状态不会因格式错误或改写固定线索而失效。<br>
**原文位置**：Methods，式（2）；投影的逐位置定义见式（3）

</div>

</div>

<div class="equation-block" markdown="1">

#### 层次监督加权目标

$$
\mathcal{L}_{\mathrm{HSW}}(\theta)=\frac{1}{Z_{\lambda}}\sum_{t=1}^{N}\lambda^{t-1}\ell^{(t)}(\theta),\qquad Z_{\lambda}=\sum_{s=1}^{N}\lambda^{s-1}=\frac{1-\lambda^{N}}{1-\lambda},\qquad \lambda\in(0,1]
$$

**符号说明**

- $\mathcal{L}_{\mathrm{HSW}}(\theta)$：用于优化模型参数 $\theta$ 的层次监督加权总损失。
- $\theta$：条件语言模型参数；实际训练时主要指可训练的 LoRA 适配器参数。
- $\ell^{(t)}(\theta)$：第 $t$ 步在完整目标解上计算的平均 token 交叉熵，且提示 token 被掩蔽。
- $\lambda$：监督权重的指数衰减率；$\lambda=1$ 退化为各步均匀加权，$\lambda<1$ 时越早的步骤权重越高。
- $N$：当前有效的监督递归深度。
- $Z_{\lambda}$：权重归一化常数，使当前 $N$ 个步骤的权重之和为 $1$。
- $t$：损失对应的递归步骤索引。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标假设早期候选离答案更远，因此早期修正通常信息量更大；越晚的步骤则按指数规律降低影响，但不完全丢弃。归一化项会随当前课程深度重新计算，因此无论训练到多少步，各步监督权重始终形成可比较的分布；这是作者将 HSW 适配到自回归逐步精炼的关键设计。<br>
**原文位置**：Methods，Hierarchical Supervision Weighting，式（7）至式（8）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：基础逐步损失 $\ell^{(t)}(\theta)$ 是目标完成序列 $\bm{y}^{\ast}$ 上的平均 token 级负对数似然：模型在提示 $P(\bm{x},c,\hat{\bm{y}}^{(t-1)},t,N)$ 和真实目标前缀条件下预测下一个 token，提示部分被掩蔽，只对答案 token 计算梯度。由于每一步监督的都是完整答案，训练目标不是要求第 $t$ 步只修正某个局部，而是学习一个可从任意部分正确候选直接恢复到标准解的共享算子，这与测试时反复调用同一算子的方式一致。

总目标使用 HSW 权重 $w_t=\lambda^{t-1}/Z_{\lambda}$ 聚合各步损失。论文的实际训练循环每个递归步执行一次优化器更新，因此在反向传播前将该步损失缩放为 $w_t\ell^{(t)}$；这会把 $w_t$ 表现为依赖步骤的有效梯度尺度。作者明确说明，若先累积所有加权损失再进行单次参数更新，才与聚合形式的 $\mathcal{L}_{\mathrm{HSW}}$ 完全等价；逐步更新保留了强调早期步骤的意图，但不能简单视为一次聚合更新的严格同一实现。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 显式递归候选状态**

递归状态不是 TRM 一类模型内部携带的隐向量，而是可读的序列化候选 $\hat{\bm{y}}^{(t)}$；同一个自回归算子 $\pi_{\theta}$ 在各步共享参数，并以原题、候选和步编号为条件生成下一状态。解码后的候选在步间被分离梯度，以截断递归方式训练。

> 直观理解：模型不用把解题进度藏在不可见的内部状态中，而是每轮明确写出当前答案，再读取它继续修改。这使不同结构任务可以复用同一套递归循环，也使每轮结果和收敛过程更容易检查。

**2. 任务专属约束投影**

投影 $\Pi_{\bm{x}}$ 由任务的长度 $L$、合法字母表 $\Sigma$、固定集合 $\mathcal{G}(\bm{x})$ 和结构规则确定；它保护固定输入、处理越界或缺失输出，并规范序列形状。论文称数独数字、ARC 颜色、填字字母及网格结构等差异主要封装于序列化和投影中。

> 直观理解：投影器相当于一个不会学习、但严格执行规则的校验层。它把“如何改进答案”交给模型，把“哪些改动绝对不允许”交给确定性程序，从而降低语言模型同时学习推理与格式控制的负担。

**3. LoRA 与层次监督加权**

预训练 Qwen 骨干保持冻结，在注意力块的线性层中注入低秩矩阵 $A$、$B$，仅这些适配器参与训练；同一组适配器跨任务共享。HSW 在有效递归深度内用指数衰减分配每步监督权重，并随课程中的当前深度重新归一化，不增加模型参数或额外前向、反向次数。

> 直观理解：LoRA 保留大模型已有的语言和推理知识，只训练一小组低秩修正参数；HSW 则决定每轮批改对参数更新有多大影响。二者分别解决“如何低成本适配大模型”和“如何减少后期递归监督噪声”两个问题。

**训练与推理**

训练从较浅的监督递归深度开始，并在预设 epoch 边界将有效深度 $N_{\mathrm{sup}}(e)$ 逐级增加，最高不超过 $N_{\max}$。对每个尚未求解的样本，每一步先依据当前候选构造提示并计算完整目标的教师强制交叉熵，再按 HSW 权重缩放损失并更新 LoRA；候选生成是离散贪心解码，生成结果停止梯度后经过投影，作为后续步骤的固定输入。为减少自回归解码成本，训练可只在每隔 $m$ 步及最后一步重新生成候选，其余步骤沿用上一候选，但仍在每一步计算监督损失；一旦某样本候选等于目标解，就从活动集合中移除，全部样本求解后提前结束该批次递归。

推理时不使用教师强制，也不需要目标解。模型从 $\hat{\bm{y}}^{(0)}=\bm{x}$ 出发，以固定测试深度 $K$ 重复执行候选条件提示、贪心解码和同一任务投影，最终返回 $\hat{\bm{y}}^{(K)}$。递归发生在显式任务候选上，而不是让模型递归扩写提示或学习隐式停止深度；因此每一步的含义和总计算预算较清楚，但固定 $K$ 也意味着推理过程本身没有学习式停机机制。

**复现信息**

论文所述实现以预训练 Qwen3.5-27B 为骨干，冻结其原始权重，并在注意力块的线性层中加入 LoRA；实验设置称除非另有说明，LoRA 应用于注意力块的全部线性层。LoRA 将目标矩阵写为 $W=W_0+(\alpha/r)BA$，其中 $W_0$ 冻结，秩 $r$ 远小于原矩阵维度，仅训练 $A$、$B$ 且不训练偏置；正文报告共享适配器的可训练参数为 12M。实现可选用 4-bit NF4 双重量化的 QLoRA 以降低显存，但该选项不改变递归算法。

优化采用 SGD、梯度裁剪、线性预热和余弦学习率调度。公平解释该方法时需要注意三点：其一，跨任务保持相同递归训练框架、超参数和损失，但序列化与投影仍是任务专属程序；其二，生成使用贪心解码，因而改进主要来自递归状态更新而非采样搜索；其三，候选解码在步骤之间停止梯度，训练不是对完整 $N$ 步生成链执行端到端反向传播。摘录未给出 LoRA 秩 $r$、缩放系数 $\alpha$、衰减率 $\lambda$、批大小、具体课程边界、生成间隔 $m$ 或测试深度 $K$ 的最终取值，这些复现参数原文指向附录，当前材料中未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Sudoku：约束满足任务，用于检验模型能否通过反复修正候选解，使数字排列逐步满足行、列和局部区域约束。原文节选未提供数据规模、训练/验证/测试划分及具体题目规格。
- Maze：路径规划任务，用于检验递归细化是否支持多步搜索、错误路径修正与回退。原文节选未提供迷宫尺寸、样本规模和数据划分。
- ARC-AGI-1 与 ARC-AGI-2：抽象视觉变换基准，要求从少量输入输出网格示例中推断变换规则并生成目标网格；二者用于测试跨任务规则归纳与组合推理。原文还报告使用 CrossWordBench 检验语言支撑的网格补全，但受数据集数量限制未单列。原文节选未给出 ARC 数据规模、划分方式或是否采用官方评测服务器。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 八个结构化推理基准上的总体比较

<div class="result-value" markdown="1">

作者声称 R-Qwen 在八个高难度基准上持续优于既有递归推理模型和参数规模大得多的 LLM，同时保持相近的可训练参数量；所给材料没有列出八个基准的完整名称和逐项分数。

</div>

该结果支持“预训练语言模型先验与递归细化可以互补”的作者主张：模型不必只靠扩大参数量，也可通过重复修正候选解提升符号任务表现。不过，仅凭摘要中的总体结论无法判断提升是否覆盖每个数据集、是否具有统计显著性，也无法排除训练数据、评测协议或计算预算差异造成的影响。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across eight challenging benchmarks, R-Qwen consistently outperforms prior recursive reasoning models and substantially larger LLMs while using a comparable number of trainable parameters.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### ARC-AGI 数据集上的基线比较

<div class="result-value" markdown="1">

作者报告 R-Qwen 相对基线提升 27.6%，但所给节选没有说明这是绝对百分点还是相对增幅，也没有明确指出对应 ARC-AGI-1、ARC-AGI-2 或二者汇总，以及具体基线和原始分数。

</div>

这一结果表明递归候选解修正可能特别适合 ARC 所需的规则假设、验证和更新过程。由于缺少分母、基线身份及逐任务成绩，27.6% 不能直接解释为准确率增加 27.6 个百分点，更不能单独证明模型获得了普遍的抽象推理能力。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Notably, on ARC-AGI dataset, our model achieves a 27.6\% improvement over the baseline, highlighting the effectiveness of recursive refinement for general symbolic reasoning.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 分层监督加权对训练稳定性与优化速度的影响

<div class="result-value" markdown="1">

作者声称 HSW 将梯度方差至少降低 50%，提高随机梯度的信噪比并加快收敛；所给节选未报告方差计算方式、对照损失、重复实验数量或具体收敛速度。

</div>

HSW 对不同递归步骤的损失施加指数权重，其目标是让训练信号更稳定，并避免各步监督产生同等但噪声不同的梯度。至少 50% 的方差下降支持其优化层面的作用，但在缺少最终任务分数对照时，这一结果不能证明训练稳定性的改善必然转化为更高的测试准确率。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

HSW reduces gradient variance by at least 50\%, improves the signal-to-noise ratio of stochastic gradients, and accelerates convergence.

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

- HRM（Hierarchical Reasoning Model）：具有分层、迭代潜状态计算的递归推理模型，是判断预训练语言先验是否能在递归计算之外带来额外收益的直接比较对象；表注说明其从头训练。
- TRM（Tiny Recursive Model）：以较少参数进行递归推理的模型，用于比较 R-Qwen 与轻量递归架构的参数效率。表下注明 TRM-MLP 在 Sudoku 上使用 5M 参数，在 Maze 和 ARC-AGI 上使用 19M 参数。
- Loopformer：从头训练的循环式模型，用于检验 R-Qwen 的优势是否来自特定的候选解递归细化与预训练骨干，而非一般意义上的重复计算。
- VARC 与 ARC-AGI 排行榜中的 LLM：VARC 是表中另一种从头训练的比较模型；排行榜 LLM 则代表更大规模的通用语言模型，用于比较预训练规模与显式递归推理机制的相对作用。原文节选未列出具体 LLM 名称、参数量或提示协议。

**实验想回答的问题**

- 递归候选解细化是否能跨越约束满足、路径规划、抽象视觉变换和语言网格补全等不同任务，稳定提升一般符号推理能力，而不是只对单一谜题有效？
- 在可训练参数量相近的条件下，基于预训练 Qwen 的 R-Qwen 能否优于从头训练的递归模型以及规模更大的通用大语言模型？

**实验实现**

作者在 Sudoku、Maze、ARC-AGI-1、ARC-AGI-2 和 CrossWordBench 上评估递归候选解细化框架，并将任务覆盖面设计为约束满足、路径规划、抽象视觉变换和语言支撑网格补全。表 1 比较 Sudoku、Maze、ARC-1 和 ARC-2；其中 LLM 结果取自 ARC-AGI 排行榜，HRM、TRM、Loopformer 和 VARC 从头训练，参数栏中的符号表示可训练参数量。除 TRM-MLP 的部分参数规模外，所给节选没有报告 R-Qwen 具体版本、训练轮数、递归步数、随机种子、解码策略、数据划分、指标定义或显著性检验，因此无法据此完整复现实验，也不能确认排行榜结果与本地训练模型是否使用完全一致的评测协议。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops recursive refinement and supervision mechanisms for improving pretrained language models on symbolic reasoning tasks.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`42098cd15f20f258854697edee7af0e9c23d88d18a4db200d6ebbc16c9e45fe0`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
