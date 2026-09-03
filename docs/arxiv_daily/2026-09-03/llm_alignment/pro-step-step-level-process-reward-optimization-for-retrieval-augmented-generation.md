---
title: "[论文解读] PRO-Step: Step-level Process Reward Optimization for Retrieval-Augmented Generation"
description: "[arXiv 2609.01658][对齐 / RLHF] 原文未明确报告。"
arxiv_id: "2609.01658"
announcement_date: "2026-09-03"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:29:23.623137+00:00"
source_sha256: "480730467d542b95078f74ddf50d8d231c99053d4147f10e0f9f86ffad9443ec"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "检索增强生成"
  - "多跳问答"
  - "过程奖励模型"
  - "证据支撑"
  - "直接偏好优化"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2609.01658</p>

# PRO-Step: Step-level Process Reward Optimization for Retrieval-Augmented Generation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> MinKeon Kim, Namjun Lee, Jaekwang Kim</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Applied Artificial Intelligence；Affiliation: Sungkyunkwan University, Seoul, South Korea</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01658v1) · [PDF 下载](https://arxiv.org/pdf/2609.01658v1) · **关键词** 检索增强生成, 多跳问答, 过程奖励模型, 证据支撑, 直接偏好优化<br>
**代码**: [https://github.com/keemminnke/PRO-Step](https://github.com/keemminnke/PRO-Step) · **项目页**: [https://github.com/keemminnke/PRO-Step](https://github.com/keemminnke/PRO-Step)

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

本文位于检索增强生成（Retrieval-Augmented Generation，RAG）与大语言模型推理优化的交叉领域。RAG通过从外部知识源检索文本并将其提供给大语言模型，以减少幻觉并补充时效性知识；但面对需要多次检索和推理的多跳问答时，系统必须交替执行查询改写、文档检索和中间推理，早期检索错误可能沿推理链传播。本文关注如何用过程级监督评价每一步的逻辑正确性与证据支撑，而不是只根据最终答案是否正确来训练系统。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**检索增强生成（RAG）**

RAG先根据问题从外部文档中检索相关信息，再把这些信息交给大语言模型生成答案。这样做的目标是让答案有外部证据支撑，而不完全依赖模型参数中的记忆。

</div>
<div class="concept-item" markdown="1">

**多跳问答与过程奖励模型（PRM）**

多跳问答需要连续完成多个检索和推理步骤，后一步往往依赖前一步的结果。过程奖励模型（PRM）不只检查最终答案，而是为推理链中的中间步骤提供评价；本文进一步要求它同时检查逻辑有效性和检索证据是否真正支持该步骤。

</div>
<div class="concept-item" markdown="1">

**直接偏好优化（DPO）**

DPO通过成对的偏好样本训练模型：给定同一上下文，模型应提高对较好步骤的概率并降低对较差步骤的概率。本文中的偏好对由PRM和价值树搜索构造，用于直接优化每一个推理步骤。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文研究具有交错检索—推理过程的单跳和多跳问答。给定用户问题以及可访问的外部检索环境，策略模型需要逐步决定何时检索、如何改写查询、如何利用返回文档进行推理，并最终输出答案；每个中间步骤都应在逻辑上有效，且其事实主张应由当前检索到的证据支持。核心困难是：最终答案正确并不保证中间步骤正确，因为错误检索可能偶然导向正确答案；而只使用最终答案奖励又会产生稀疏反馈，难以及时识别和纠正早期错误。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$RAG$**

检索增强生成系统；通过外部知识检索辅助大语言模型生成答案。

</div>
<div class="notation-item" markdown="1">

**$LLM$**

大语言模型，负责生成查询、推理步骤和最终答案。

</div>
<div class="notation-item" markdown="1">

**$PRM$**

过程奖励模型，用于逐步评价推理过程，而非只评价最终结果。

</div>
<div class="notation-item" markdown="1">

**$DPO$**

直接偏好优化方法，根据优选步骤与劣选步骤的成对数据优化策略模型。

</div>

</div>

**直接相关的工作**

- **Search-R1、R1-Searcher**: 这些方法把搜索引擎接入大语言模型环境，并使用最终答案正确性作为强化学习奖励，证明了端到端结果监督可以提升智能体式RAG能力。但这种结果级奖励只在完整推理链结束后反馈，不能明确惩罚中间检索或推理错误。
- **GenPRM**: GenPRM将过程奖励模型从单纯输出标量扩展为先生成错误分析理由、再给出正确性标签，从而提供更丰富的步骤级监督。PRO-Step借鉴这种生成式评价思想，但针对RAG增加了对检索证据支撑性的检查，因为RAG步骤同时包含内部逻辑推理和外部事实依据。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

检索增强生成（RAG）需要先从外部知识源检索证据，再由大语言模型进行推理和作答；在多跳问答中，模型往往要交替执行查询改写、文档检索与中间推理。若早期检索到无关文档或提出不准确的查询，错误就可能传递到后续步骤，最终产生看似合理但缺乏依据的答案。因此，实际需求不仅是判断最终答案是否正确，还要及时识别每个中间步骤是否合乎逻辑、是否得到检索证据支持。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **结果监督的强化学习与端到端优化**：这类方法让模型在检索环境中完成完整的推理链，并主要依据最终答案是否正确来提供奖励，从整体结果优化检索、推理和生成策略。
- **过程奖励模型（PRM）与过程级优化**：这类方法为推理链中的各个步骤提供反馈，通常检查步骤之间的逻辑一致性，并据此引导模型学习更可靠的推理轨迹。本文将其扩展到检索增强场景，关注中间步骤的逻辑正确性和证据依据。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 结果监督方法只在完整推理链结束后依据最终答案给出反馈，无法定位或惩罚早期的查询和检索错误；奖励因此较为稀疏，错误可能在后续步骤中持续传播，并增加训练收敛所需的数据和优化难度。
- 现有过程级方法在迁移到 RAG 时通常偏重逻辑一致性，不能核验中间主张是否真正得到检索文档支持；即使某一步的检索或推理存在缺陷，也可能因偶然得到正确最终答案而被视为有效，形成“虚假成功”。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种面向 RAG 的细粒度监督机制，能够在每个交替的检索—推理步骤上同时判断逻辑有效性与证据支撑，并将这些判断转化为可用于策略优化的、具有区分度的训练信号。具体而言，已有方法尚未充分解决如何系统构造“有效步骤”与“有缺陷步骤”的偏好对，从而避免仅凭最终答案选择训练样本的问题。

</div>
<div markdown="1"><span>核心问题</span>

能否训练一个具有生成式解释能力的过程奖励模型，在每个 RAG 步骤上同时评估逻辑正确性和证据依据，并利用其筛选出的步骤级偏好对，通过价值树搜索与直接偏好优化，使模型减少中间检索和推理错误，而不只是提高最终答案的表面正确率？

</div>
<div markdown="1"><span>作者直觉</span>

如果训练信号在错误发生的步骤就出现，模型便不必等到整条推理链结束后才知道哪里出了问题。具体地说，生成式过程奖励模型先为步骤给出正确性判断及理由，再用这些判断引导价值树搜索，保留有依据的步骤、排除依靠偶然路径得到正确答案的步骤，最后通过步骤级直接偏好优化让策略偏向更可靠的局部决策。其直观效果是把“最终答错后的事后惩罚”转化为“每一步都检查依据的过程纠偏”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PRO-Step 是一个面向检索增强生成（RAG）的两阶段训练框架。第一阶段让策略模型 $\pi_{\theta}$ 与外部搜索引擎 $\mathcal{E}$ 交互，生成包含检索、推理和答案的多步轨迹，并由 QwQ-32B 为每个步骤标注局部正确性；随后训练生成式过程奖励模型（PRM）$\pi_{\psi}$，使其同时判断步骤是否逻辑正确以及是否受到检索证据支持。第二阶段利用 PRM 引导价值树搜索（VTS）构造同一推理前缀下的优劣步骤对，再通过步骤级直接偏好优化（DPO）更新策略模型，使模型偏好过程可靠的步骤，而不只是偏好最终答案正确的轨迹。

直观地说，普通 RAG 主要检查“最后答对没有”，PRO-Step 则像逐步审阅解题过程：每次检索和推理都要通过“这一步是否合理、证据是否足够”的检查；树搜索负责寻找更可靠的后续路径，DPO 再把这些偏好写回生成模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 交错生成检索轨迹

策略模型在 `<think>...</think>` 中生成推理；当生成 `<search>...</search>` 时暂停，将查询发送给 $\mathcal{E}$，并把返回内容以 `<documents>...</documents>` 追加到上下文。该交互循环持续到模型生成 `<answer>...</answer>` 或达到最大交互步数。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、策略模型 $\pi_{\theta}$、外部搜索引擎 $\mathcal{E}$ 以及系统提示。<br>
**输出**：包含推理步骤、搜索动作、检索文档和最终答案的完整轨迹 $\tau$；从 HotpotQA 和 MuSiQue 的 2,000 个问题中每题采样 16 条轨迹，过滤后保留 31,728 条。

</div>

**直观理解**：模型不是一次性写完答案，而是可以在推理过程中主动查资料。检索结果会成为后续推理的上下文，因此模型能够通过改写查询来修正早期检索错误。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤标注与生成式 PRM 训练

使用 QwQ-32B 根据标注提示为每一步生成理由 $v_t$ 和二元正确性标签 $r_t\in\{0,1\}$，并保留错误步骤之后的后续步骤。以全部标注轨迹构成 $\mathcal{D}_{\mathrm{PRM}}$，训练初始化于 DeepSeek-R1-Distill-8B 的生成式 PRM $\pi_{\psi}$。

<div class="method-step__io" markdown="1">

**输入**：轨迹中的问题 $q$、截至第 $t$ 步的上下文 $s_{\leq t}$，以及每个步骤 $s_t$。<br>
**输出**：能够先生成步骤评价理由、再预测步骤标签的 PRM；推理时以 $\hat r(s_t)=\arg\max_{r\in\{0,1\}}\pi_{\psi}(r\mid q,s_{\leq t},v_t)$ 作为步骤可靠性信号。

</div>

**直观理解**：PRM 像一个逐步阅卷人，不只看最终答案，还检查当前推理是否成立。即使某一步出错，后续步骤仍会被保留，因为模型可能通过新的检索查询恢复。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### PRM 引导的价值树搜索与偏好对构造

把节点定义为 $s_t=(q,s_{\leq t})$，把策略模型生成的下一步骤视为动作；通过 UCB 选择、扩展、PRM 评价和回传建立搜索树。终止节点使用带深度折扣的最终 F1 作为奖励，非终止节点使用 PRM 的二元预测，并以 $V(s)=\bar Q(s)+\alpha\hat r(s)$ 综合后代轨迹质量与当前步骤正确性；同一父节点下若两个子节点的价值差超过阈值 $\delta$，高价值步骤作为 chosen，低价值步骤作为 rejected。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、策略模型 $\pi_{\theta}$、PRM $\pi_{\psi}$、搜索引擎 $\mathcal{E}$ 和每个节点的推理前缀。<br>
**输出**：步骤级偏好数据集 $\mathcal{D}_{\mathrm{dpo}}$，其中优劣步骤共享问题和前缀，但 chosen 步骤具有更高的过程—结果综合价值。

</div>

**直观理解**：树搜索会尝试多条可能的解题路线，而不是只相信一次随机生成。它特别防止“中间过程错误、但碰巧答对”的轨迹被误选为好样本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤级 DPO 策略优化与推理

使用步骤级 DPO 最大化 chosen 步骤相对于 rejected 步骤的隐式效用差，并屏蔽 `<documents>` 内容，不让模型直接学习复制检索文档。训练后，给定新问题，策略模型重复执行推理—检索交互，直到生成最终答案。

<div class="method-step__io" markdown="1">

**输入**：偏好元组 $(x,y_{<t},y_t^w,y_t^l)$、当前策略 $\pi_{\theta}$、参考策略 $\pi_{\mathrm{ref}}$。<br>
**输出**：优化后的 RAG 策略模型，其生成概率更偏向逻辑有效且有证据支撑的中间步骤，并输出最终答案。

</div>

**直观理解**：DPO 不要求为每个步骤指定精确分数，只需要告诉模型“这一步比另一条候选步骤好”。因此训练目标直接塑造模型在相同上下文中选择可靠行动的倾向。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 生成式过程奖励模型训练目标

$$
\mathcal{L}_{\mathrm{PRM}}=-\mathbb{E}_{(q,\tau,v_t,r_t)\sim\mathcal{D}_{\mathrm{PRM}}}\left[\log\pi_{\psi}(v_t\mid q,s_{\leq t})+\log\pi_{\psi}(r_t\mid q,s_{\leq t},v_t)\right]
$$

**符号说明**

- $\mathcal{L}_{\mathrm{PRM}}$：PRM 的训练损失。
- $\mathcal{D}_{\mathrm{PRM}}$：由问题、生成轨迹、步骤评价理由和二元标签组成的过程监督数据集。
- $q$：输入问题。
- $\tau$：一条完整的推理—检索—答案轨迹。
- $s_{\leq t}$：截至第 $t$ 步的上下文和步骤前缀。
- $v_t$：PRM 对第 $t$ 步生成的评价理由。
- $r_t$：第 $t$ 步的二元正确性标签，取值为 0 或 1。
- $\pi_{\psi}$：参数为 $\psi$ 的生成式过程奖励模型。

<div class="equation-explanation" markdown="1">

**直观理解**：损失要求 PRM 同时学会两件事：根据上下文生成可读的评价理由，以及结合该理由预测步骤是否正确。这样得到的模型不仅输出分数，还能为树搜索提供可解释的局部可靠性信号。<br>
**原文位置**：第 3.1 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 步骤级直接偏好优化目标

$$
\mathcal{L}_{\mathrm{DPO}}(\theta)=-\mathbb{E}_{\mathcal{D}_{\mathrm{dpo}}}\left[\log\sigma\left(u_{\theta}(x,y_t^w)-u_{\theta}(x,y_t^l)\right)\right],\quad u_{\theta}(x,y_t)=\beta\log\frac{\pi_{\theta}(y_t\mid x,y_{<t})}{\pi_{\mathrm{ref}}(y_t\mid x,y_{<t})}
$$

**符号说明**

- $\mathcal{L}_{\mathrm{DPO}}(\theta)$：用于更新策略模型参数 $\theta$ 的 DPO 损失。
- $\mathcal{D}_{\mathrm{dpo}}$：步骤级偏好数据集，包含共享前缀、chosen 步骤和 rejected 步骤。
- $x$：带系统提示的问题输入。
- $y_{<t}$：第 $t$ 步之前的共享生成前缀。
- $y_t^w,y_t^l$：同一前缀下的优选步骤和拒绝步骤。
- $u_{\theta}$：当前策略相对参考策略对某一步骤的隐式效用。
- $\pi_{\theta},\pi_{\mathrm{ref}}$：待优化的策略模型和固定参考模型。
- $\beta$：控制策略偏离参考模型程度的超参数。
- $\sigma$：将效用差映射为偏好概率的 logistic 函数。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标让 chosen 步骤相对于 rejected 步骤获得更高的相对概率，同时限制模型不要偏离参考模型过远。由于训练对象是共享前缀下的单步选择，监督重点从“最终答案对错”转移到了“下一步该怎么做”。<br>
**原文位置**：第 3.2 节，公式（5）—（6）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练包含两个相互衔接的目标。首先，PRM 最小化 $\mathcal{L}_{\mathrm{PRM}}$，学习从问题和步骤前缀生成评价理由并预测局部正确性；其次，策略模型最小化步骤级 DPO 损失，使优选步骤的隐式效用高于拒绝步骤。VTS 本身不是独立的梯度训练目标，而是利用 PRM 信号和终止节点 F1 进行搜索，从而构造 $\mathcal{D}_{\mathrm{dpo}}$；其中综合价值使用 $V(s)=\bar Q(s)+\alpha\hat r(s)$，但该公式属于数据构造规则而非直接优化损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 面向 RAG 的生成式过程奖励模型**

PRM $\pi_{\psi}$ 根据问题 $q$ 和前缀 $s_{\leq t}$ 先生成评价理由 $v_t$，再预测 $r_t\in\{0,1\}$。与只依据最终答案评价过程的方法不同，它为每个检索或推理步骤提供局部监督，并将逻辑正确性与外部证据 grounding 纳入评价。

> 直观理解：该模块解决的是“最后答对但过程不可信”的问题：模型必须说明当前步骤为什么成立，而不是仅凭最终答案反推过程正确。

**2. PRM 引导的价值树搜索**

搜索节点是 $s_t=(q,s_{\leq t})$，下一步由 $\pi_{\theta}$ 采样；UCB 在探索未充分访问的分支和利用高价值分支之间折中。终止奖励为深度折扣后的 F1，非终止节点使用 $\hat r(s_t)\gamma^{d(s_t)}$，并通过回传更新节点的平均价值 $\bar Q(s)$。

> 直观理解：搜索同时考虑“最终能否答对”和“当前步骤是否可靠”。深度折扣还会抑制不必要的长轨迹，避免模型通过无关的额外步骤提高偶然答对的机会。

**3. 步骤级 DPO**

对共享前缀下的 chosen 步骤 $y_t^w$ 与 rejected 步骤 $y_t^l$，定义相对于参考策略的隐式效用 $u_{\theta}$，并最小化二者效用差的 logistic 损失；超参数 $\beta$ 控制策略相对参考模型的 KL 约束，检索文档块在损失中被屏蔽。

> 直观理解：该模块把搜索得到的局部偏好转化为模型参数更新，让模型在以后遇到类似前缀时更常选择可靠的检索或推理动作，而不是只学习答案字符串。

**训练与推理**

训练时，先从 HotpotQA 和 MuSiQue 采样并生成 31,728 条轨迹，使用 QwQ-32B 对所有步骤标注，训练 PRM $\pi_{\psi}$。随后从 5,000 个多跳问题构成策略训练混合数据，使用 PRM 引导 VTS；每个问题的搜索设置为分支因子 $K=3$、最大深度 7、每题 64 次迭代，并用价值差阈值 $\delta$ 筛选步骤偏好对。最后用步骤级 DPO 更新 $\pi_{\theta}$，训练时屏蔽检索文档块。

推理时，优化后的策略从问题开始生成推理；生成 `<search>` 后调用外部搜索引擎，将返回的 `<documents>` 放回上下文，再继续生成。模型重复该过程，直到输出 `<answer>` 或达到交互上限；PRM 主要用于训练阶段的过程评价和搜索引导，最终答案由优化后的策略生成。

**复现信息**

主要骨干模型为 Qwen2.5-7B-Instruct；PRM 初始化于 DeepSeek-R1-Distill-8B。所有方法使用 2018 年 Wikipedia 的 5.9M 文档集合、BGE-base-en-v1.5 检索器和 $k=3$ 个检索段，以保持比较一致；PRO-Step 的策略训练数据为 HotpotQA 2,000 题、MuSiQue 2,000 题和 2WikiMultiHopQA 1,000 题。VTS 使用深度折扣 $\gamma=0.9$ 和 PRM 权重 $\alpha=0.3$；文中说明 $\alpha=0.3$ 用于在不覆盖显著 F1 差异的情况下打破结果相近步骤之间的平局。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HotpotQA：多跳问答基准，用于测试系统是否需要从多个证据来源逐步检索和推理；附录报告其测试集规模为 $7{,}405$。
- 2WikiMultiHopQA：多跳问答基准，用于检验跨文档、多步检索中的错误传播与恢复能力；附录报告其测试集规模为 $12{,}576$。
- MuSiQue：较复杂的多跳问答基准，用于测试更长推理链上的检索、证据利用和最终回答质量；附录报告其测试集规模为 $2{,}417$。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**EM**

Exact Match，预测答案与标准答案完全匹配的比例，主要反映严格的最终答案正确率。 （越高越好，因为更高表示完全正确的答案更多。）

</div>
<div class="metric-item" markdown="1">

**F1**

答案词级精确率与召回率的调和平均，允许预测答案与标准答案存在部分词汇重叠，因此比 EM 更能反映部分正确程度。 （越高越好，因为更高表示答案与标准答案的内容重合度更高。）

</div>
<div class="metric-item" markdown="1">

**IFBC**

Intermediate-Flawed-But-Correct，定义为在最终答案正确的轨迹中，至少包含一个有缺陷中间步骤的条件概率：$\mathrm{IFBC}=P(\text{flaw}\geq 1\mid\text{correct})$。 （越低越好，因为较低表示正确答案更少依赖错误的中间检索或推理步骤。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 五个基准上的宏平均显著性比较

<div class="result-value" markdown="1">

相对于 Search-R1，PRO-Step 的宏平均 EM 提升 $2.51$ 个百分点，$95\%$ 置信区间为 $[1.01,4.06]$；宏平均 F1 提升 $3.37$ 个百分点，区间为 $[1.94,4.82]$。相对于 ReasonRAG，EM 和 F1 分别提升 $1.93$ 和 $3.14$ 个百分点，两个区间均不包含 $0$。相对于 StepSearch，F1 提升 $2.10$ 个百分点且显著，但 EM 提升 $1.36$ 个百分点的区间 $[-0.29,3.00]$ 包含 $0$。

</div>

作者的统计结果支持 PRO-Step 相比 Search-R1 和 ReasonRAG 在整体 EM、F1 上具有稳健优势，也支持其相对 StepSearch 的 F1 优势；但不能据此断言它在所有数据集和所有指标上都显著优于 StepSearch。宏平均显著性也不等于每个数据集都显著，具体数据集差异仍需单独检查。

<div class="result-source" markdown="1">

来源：Appendix F, Findings；Table 15

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

PRO-Step significantly outperforms Search-R1 and ReasonRAG in macro-AVG EM and F1 (95% CI). Against StepSearch, F1 improvements are significant; while the EM CI marginally includes 0, PRO-Step leads significantly on PopQA and 2WikiMultiHopQA.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 检索失败后恢复的轨迹

<div class="result-value" markdown="1">

在由各模型自身搜索行为定义的恢复子集上，PRO-Step 的 token-level F1 在 HotpotQA、PopQA、2WikiMulti 和 MuSiQue 上分别为 $69.0$、$57.6$、$66.1$ 和 $51.1$，相对 Search-R1 分别为 $+2.5$、$+3.4$、$+7.8$ 和 $+2.1$；在 Bamboogle 上则低 $3.6$ 个百分点。

</div>

该分析专门考察初始检索不理想、系统后来成功恢复的轨迹，因此结果表明 PRO-Step 的优势不仅来自一开始就检索到金标准证据，也可能来自更好的后续步骤选择和推理修正。不过恢复子集由各模型自己的搜索行为产生，模型之间并非完全相同的样本集合；Bamboogle 的结果还不支持普遍优势，因为该数据集上 PRO-Step 反而落后。

<div class="result-source" markdown="1">

来源：Appendix I, Section I；Table 19

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

PRO-Step leads on four of five datasets, with the largest margin on 2WikiMulti (+7.8). The exception is Bamboogle, whose recovered subset contains only 25 questions.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 不同恢复深度下的 2WikiMultiHopQA 表现

<div class="result-value" markdown="1">

在 2WikiMultiHopQA 上，按第一次成功检索步骤 $k$ 分组后，作者报告 PRO-Step 在 $k=1$ 至 $k=3$ 的恢复深度上均保持收益；$k\geq4$ 的分组中优势更大，但两个子集都较小，因此该比较不够可靠。

</div>

这一结果测试的是 PRO-Step 是否只在较早恢复时有效，还是在多次检索失败后仍能利用过程信号进行修正。结果支持其收益在多个恢复阶段都存在，但不能把 $k\geq4$ 的较大差距视为稳定结论，因为样本量有限且作者明确提示该比较不可靠。

<div class="result-source" markdown="1">

来源：Appendix I, Section I；Table 20

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Gains are consistent at k=1 through k=3. The k≥4 bucket favors PRO-Step by a wide margin, but both subsets are small and the comparison is not reliable.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 现有片段没有提供五个基准的完整主结果表、所有优化策略消融结果、Table 18 的 IFBC 数值以及 Table 20 的具体分数，因此无法完整核验“最佳平均 EM 和 F1”或量化错误中间轨迹的减少幅度。
- 恢复子集由每个模型自身的搜索行为定义，模型间样本集合可能不同；此外 Bamboogle 恢复子集只有 $25$ 个问题，$k\geq4$ 的 2WikiMultiHopQA 子集也被作者指出样本较小。因此这些细分结果更适合作为机制证据，而不是对所有检索场景的确定性结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Search-R1：搜索与推理基线，用于比较标准搜索增强推理流程与 PRO-Step 的差异。
- ReasonRAG：既有检索增强生成方法，用于比较不同检索—推理协同机制的最终问答效果。
- StepSearch：步骤级搜索或过程优化方法，用于检验 PRO-Step 的步骤级奖励与偏好优化是否优于已有步骤搜索策略。
- Without PRM：去除过程奖励模型的 PRO-Step 变体，用于隔离 PRM 对最终性能的贡献，而不是比较完整系统。

**实验想回答的问题**

- PRO-Step 是否能在单跳与多跳问答基准上，相对于既有搜索、推理和过程优化方法提升最终答案质量，并且这种提升是否具有统计显著性？
- 同时评估中间步骤的逻辑有效性与证据支撑，尤其通过过程奖励模型（PRM）和步骤级优化，是否能改善检索失败后的恢复能力并减少“中间步骤有误但最终答案正确”的轨迹？

**实验实现**

主要实验采用温度为 $0$ 的贪心解码，因此每个问题的输出是确定性的；显著性分析在逐问题得分分布上进行，而不是依赖多个随机种子。附录使用自助法计算宏平均差异的 $95\%$ 置信区间，并进行逐数据集配对 $t$ 检验。恢复分析中，若金标准段落出现在前 $3$ 个检索文档中，则认为检索成功；恢复深度 $k$ 表示第一次成功检索发生的步骤，初始检索记为步骤 $0$。IFBC 分析使用每个系统在 HotpotQA、2WikiMultiHopQA 和 MuSiQue 上各 $500$ 个配对问题的轨迹，并由对系统身份不知情的 QwQ-32B 按与 PRM 监督相同的 R1–R6 标准进行标注。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 去除过程奖励模型（Without PRM） | 完整 PRO-Step 的五个数据集宏平均为 EM $34.5$、F1 $44.1$；去除 PRM 后为 EM $32.7$、F1 $41.9$，分别下降 $1.8$ 和 $2.2$ 个百分点。完整模型在 PopQA、HotpotQA、2WikiMulti 和 Bamboogle 的 EM、F1 均高于去除 PRM 版本；MuSiQue 的 F1 持平为 $22.4$。 | 该消融隔离了 PRM，而不是整个搜索或偏好优化流程。性能下降说明同时评价步骤逻辑有效性和证据支撑的 PRM 对整体效果有实质贡献，但它不能单独证明 PRM 的每个设计细节都必要，也不能排除其与搜索和优化模块的交互效应。 | Table 2, Component ablation study<br><span class="experiment-evidence">Without PRM 38.5 45.0 36.8 49.3 41.4 48.4 34.4 44.2 12.3 22.4 32.7 41.9</span> |

**定性案例**

- 恢复深度分析是最接近案例层面的证据：作者把 2WikiMultiHopQA 的恢复轨迹按第一次成功检索的步骤 $k$ 划分，发现 PRO-Step 在 $k=1$ 至 $k=3$ 均有一致收益。这说明该方法并非只依赖一次成功的初始检索，而是可能通过步骤级价值评估改善后续搜索决策；但原文摘录未提供各深度分组的具体分数，因而只能作方向性解释。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向多跳 RAG 的生成式过程奖励模型、价值树搜索和步骤级 DPO，以优化中间检索与推理过程。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`480730467d542b95078f74ddf50d8d231c99053d4147f10e0f9f86ffad9443ec`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
