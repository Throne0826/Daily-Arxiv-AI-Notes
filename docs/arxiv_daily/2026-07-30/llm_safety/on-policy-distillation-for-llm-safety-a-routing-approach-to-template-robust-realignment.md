---
title: "[论文解读] On-Policy Distillation for LLM Safety: A Routing Approach to Template-Robust Realignment"
description: "[arXiv 2607.27081][LLM 安全] 本文针对微调供应链中的安全失准，提出基于路由的在线策略蒸馏 ROPD，通过分别继承原始对齐模型的拒答能力与受攻击微调模型的专业能力，降低安全修复对攻击提示模板的依赖。"
arxiv_id: "2607.27081"
announcement_date: "2026-07-30"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.578266+00:00"
source_sha256: "c80de25044bc417c0305004250c2b5d1dd32ba691459d8b695ff08c8e9b07960"
tags:
  - "LLM 安全"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "大语言模型安全"
  - "安全再对齐"
  - "微调供应链攻击"
  - "提示模板不匹配"
  - "知识蒸馏"
  - "下游能力保持"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2607.27081</p>

# On-Policy Distillation for LLM Safety: A Routing Approach to Template-Robust Realignment

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Yongjian Guo, Wanlun Ma, Lingyu Shen, Xi Xiao, Sheng Wen</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27081v1) · [PDF 下载](https://arxiv.org/pdf/2607.27081v1) · **关键词** 大语言模型安全, 安全再对齐, 微调供应链攻击, 提示模板不匹配, 知识蒸馏, 下游能力保持<br>


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

本文针对微调供应链中的安全失准，提出基于路由的在线策略蒸馏 ROPD，通过分别继承原始对齐模型的拒答能力与受攻击微调模型的专业能力，降低安全修复对攻击提示模板的依赖。

**不用术语来说**：用户可能从第三方获得训练数据或模型适配器，以便让大语言模型掌握代码生成等专业技能，但提供者也可能暗中加入诱导模型回答危险问题的数据。修复这种模型很困难：修得太强会连专业技能一起抹掉；只按防御者选定的提示格式修复，又可能挡不住攻击者换一种系统提示重新触发有害行为。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者识别并系统化评估了安全重对齐中的“模板不匹配”漏洞：防御者通常不知道攻击者使用的提示模板，因此论文分别考察攻击模板、防御模板及跨模板通道中的攻击成功率，以衡量修复是否仅对特定提示格式有效。
- 作者提出 ROPD 双教师蒸馏框架：从原始对齐模型蒸馏较少依赖表面模板的拒答分布，从受攻击微调模型蒸馏下游任务能力，并按样本来源路由教师，以缓解安全恢复与能力保留之间的冲突。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型通常先经过指令微调或基于人类反馈的训练，以形成遵循指令且拒绝危险请求的安全行为，随后再通过下游微调获得代码生成等专业能力。本文关注这种二次微调带来的供应链安全问题：恶意数据提供者可在训练语料或参数高效适配器中夹带有害样本，使模型保留目标任务能力，却在特定提示模板下响应危险请求。防御方拿到已受损模型后，需要进行“安全再对齐”，即在不从头训练、通常也不知道攻击者提示模板的条件下恢复拒答能力，同时避免遗忘下游技能；因此，评价不能只看某一种提示格式下是否安全，还要考察攻击模板、修复模板及其交叉切换下的攻击成功率与任务能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**安全对齐与安全再对齐**

安全对齐是让模型遵循人类意图并拒绝有害请求；安全再对齐则是在后续微调破坏这种行为后，对受损模型进行修复。本文的核心约束是修复安全性的同时保留受损模型已经获得的专业技能。

</div>
<div class="concept-item" markdown="1">

**提示模板不匹配**

提示模板指组织系统提示、用户请求及角色标记的具体格式；同一危险问题放入不同模板后，模型行为可能明显变化。攻击者与防御者使用不同模板时，在防御模板下看似成功的修复可能仍会在攻击模板或新系统提示下失效。

</div>
<div class="concept-item" markdown="1">

**知识蒸馏与输出概率分布**

知识蒸馏让学生模型模仿教师模型对下一词的概率分配，而不只是学习一条固定的参考回答。本文据此区分两类行为来源：原始对齐模型提供拒答倾向，受攻击的微调模型提供下游任务能力。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括三个要素：攻击前且已安全对齐的原始模型、经下游数据或适配器微调后同时具有专业能力与有害行为的受损模型，以及由有害探针和正常任务样本组成的再对齐数据。攻击者可通过未知提示模板触发有害响应；防御者只能选择自己的修复模板，不能假设它与攻击模板一致。目标是输出一个再对齐后的单一模型，使其在攻击者模板、防御者模板以及模板切换形成的交叉通道中都尽量拒绝危险请求，同时维持受损模型的下游任务能力。该设置还要求防御效果写入模型行为，而不是仅在验收所用的系统提示下暂时成立；原文以攻击成功率衡量危险请求是否仍可诱导模型服从，但所给章节未进一步给出其计算公式。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$K$**

top-K KL 蒸馏中保留并比较的候选词数量；所给章节未明确报告 K 的具体取值。

</div>
<div class="notation-item" markdown="1">

**$p_{\mathrm{safe}}$**

便于描述问题而采用的记号，表示原始对齐模型对下一输出词的概率分布，即安全教师所携带的拒答先验；原文节选未给出这一符号。

</div>
<div class="notation-item" markdown="1">

**$p_{\mathrm{task}}$**

便于描述问题而采用的记号，表示受攻击微调模型的下一词概率分布，其中保留下游技能，但也可能包含有害服从行为；原文节选未给出这一符号。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{ASR}$**

攻击成功率（Attack Success Rate），用于衡量危险请求成功诱导模型输出有害内容的比例；数值越低通常表示防御越有效。

</div>

</div>

**直接相关的工作**

- **RESTA（Bhardwaj et al., 2024）**: 通过任务算术向受损模型参数加入预先计算的“安全向量”以恢复对齐，是本文比较的代表性参数修复方法。本文指出，这类方法的有效性可能依赖修复监督与攻击提示模板保持一致，并可能以损害下游任务能力为代价。
- **soft-SFT（Qi et al., 2025）**: 针对安全行为集中在生成开头、因而较为浅层的问题，采用按词元加权的微调目标强化后续词元的安全约束。本文将其视为模板格式化拒答监督的一类代表，并考察模板不匹配时其安全恢复与技能保持是否同时退化。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

微调是赋予大语言模型专业能力的常用方式，却形成了现实的供应链攻击面：恶意数据集或参数高效适配器可以让模型在保持目标任务能力、因而看似正常可用的同时，学会在特定提示下响应危险请求。模型接收者需要在不从头训练、且不知道攻击者触发模板的情况下恢复安全性，同时保住所购买或训练得到的专业技能。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **参数恢复与模型算术方法**：将部分微调后的权重拉回原始对齐模型，或向受损模型参数加入表示安全行为的“安全向量”，试图在权重空间撤销微调造成的失准。
- **基于安全样本再训练或表征修正的方法**：使用带有特定提示格式的拒答数据继续微调，例如对安全相关 token 加权；或者在隐藏表征空间中校正模型，使其在已观察到的危险请求上恢复拒答。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 安全修复与专业能力通常在同一组权重上直接竞争。把模型强行推回原始对齐状态虽然可能降低有害回答，却会造成灾难性遗忘，使代码生成等下游任务能力显著下降，因而安全性常以实用性为代价。
- 现有防御往往从某个特定模板触发出的拒答样本、安全方向或表征进行修复，隐含假设防御模板与攻击模板一致。当两者不一致时，修复可能只在防御者测试的通道中有效，而攻击者原有通道仍可产生有害回答；即使验收测试通过，简单改写系统提示也可能重新越狱。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一种能够同时满足三项要求的权重级重对齐方案：无需预先知道攻击者的提示模板，能够把安全行为推广到不同模板通道，并在恢复拒答能力时保留受攻击微调所获得的专业技能。更根本地说，已有方法主要拟合模板化拒答或模板诱导出的参数方向，尚未充分利用原始对齐模型与受损模型在输出概率分布上的稳定差异。

</div>
<div markdown="1"><span>核心问题</span>

能否将安全恢复与任务能力保留分别交给原始对齐模型和受攻击微调模型，并通过按样本来源路由的输出分布蒸馏，把二者合并到一个学生模型中，从而在未知攻击模板时仍降低多个模板通道的攻击成功率，同时不牺牲下游任务能力？

</div>
<div markdown="1"><span>作者直觉</span>

提示模板只是输入的表面包装，而模型面对有害请求时“倾向拒绝哪些词、倾向继续生成哪些词”体现在完整的下一 token 概率分布中。原始对齐模型通常把较高概率分配给拒答表达，受损模型则更倾向顺从；这种分布差异可能比某一句固定拒答文本更能跨模板保留安全信号。因此，对有害探针让学生模仿原始模型的分布，对任务样本让其模仿微调模型的分布，相当于分别向两位专长不同的教师学习，可减少安全目标与任务目标在训练中的直接冲突。不过作者明确指出，这只能显著缓解而不能彻底消除提示改写带来的条件性漏洞。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ROPD（Routing-based On-Policy Distillation，基于路由的在策略蒸馏）以遭攻击模型为学生初始值，并冻结两个教师：原始安全对齐模型负责恢复拒答行为，遭攻击模型自身负责保留下游技能。训练数据由任务样本与有害提示组成，全部用防御者可选的模板渲染；系统根据样本来源逐例选择教师，再以 top-K KL 散度对齐学生与对应教师的逐词输出概率分布，最终得到兼顾安全性和任务能力的重对齐模型。
直观地说，该方法不试图从参数变化中猜测攻击者使用了哪种提示模板，而是让学生在危险问题上模仿“安全模型会如何分配下一词概率”，在专业任务上模仿“已学会该技能的模型会如何回答”。这种分工将安全修复与能力保持分开，但不能完全消除模板风险：部署时若切换到与重对齐阶段差异很大的系统提示，仍可能重新暴露有害行为。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造双教师与初始化学生

冻结安全教师 $\pi_{\mathrm{safe}}=M_0$ 和任务教师 $\pi_{\mathrm{task}}=M_a$，并用 $M_a$ 的参数初始化可训练学生 $\pi_\theta$。

<div class="method-step__io" markdown="1">

**输入**：原始安全对齐模型 $M_0$，以及由任务语料和有害语料联合微调得到的失配模型 $M_a$。<br>
**输出**：两个固定的概率分布参照源，以及一个已经具备下游技能、等待安全修复的学生模型。

</div>

**直观理解**：安全教师知道何时拒绝，任务教师保留攻击后模型学到的专业能力；从 $M_a$ 出发可避免重新学习整个任务。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 混合数据并统一渲染

形成 $D=D_{\mathrm{task}}\cup D_{\mathrm{harm}}$，为每个样本保留来源标签 $s(x)\in\{\mathrm{task},\mathrm{harm}\}$，并在使用时统一按 $T_d$ 渲染；防御者无需观察攻击模板 $T_a$。

<div class="method-step__io" markdown="1">

**输入**：任务数据 $D_{\mathrm{task}}$、含有害提示的安全数据 $D_{\mathrm{harm}}$，以及防御模板 $T_d\in\{\textsc{raw},\textsc{self}\}$。<br>
**输出**：带来源标签、采用同一防御模板表示的训练批次。

</div>

**直观理解**：模型看到的文本格式可以统一，但系统仍记得每条数据属于专业任务还是安全测试，以便决定该听哪位教师。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按来源路由蒸馏目标

任务样本路由至 $\pi_{\mathrm{task}}$，有害样本路由至 $\pi_{\mathrm{safe}}$，从而为每个词位置 t 生成教师目标分布 $q_t$。

<div class="method-step__io" markdown="1">

**输入**：渲染后的样本 x、其来源标签 s(x)，以及两个教师在每个位置给出的下一词分布。<br>
**输出**：与样本目标相匹配的逐词教师概率分布。

</div>

**直观理解**：遇到危险问题就向安全模型学习拒答，遇到专业问题则向已经掌握技能的模型学习，避免用单一训练信号同时破坏两类行为。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### top-K 概率匹配与参数更新

保留 $q_t$ 中概率最大的 K 个词，将其余词合并为一个尾部概率桶，计算压缩后的 KL 损失；对样本内词位置和数据集取平均，并以梯度下降更新学生参数。

<div class="method-step__io" markdown="1">

**输入**：教师分布 $q_t$、学生分布 $p_t=\pi_\theta(\cdot\mid x_{<t})$、超参数 K、学习率 $\eta$ 和训练轮数 E。<br>
**输出**：经若干轮训练后得到重对齐模型 $\pi_\theta$。

</div>

**直观理解**：算法重点匹配教师最可能选择的少数词，同时只校准剩余词的总概率，因此无须逐一处理整个大词表。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 按样本来源选择教师分布

$$
q_t(\cdot)=\begin{cases}\pi_{\mathrm{task}}(\cdot\mid x_{<t}),&s(x)=\mathrm{task},\\[2pt]\pi_{\mathrm{safe}}(\cdot\mid x_{<t}),&s(x)=\mathrm{harm}.\end{cases}
$$

**符号说明**

- $q_t(\cdot)$：位置 t 上用于监督学生的教师下一词概率分布。
- $\pi_{\mathrm{task}}$：冻结的任务教师，默认取遭攻击但保留下游技能的模型 $M_a$。
- $\pi_{\mathrm{safe}}$：冻结的安全教师，即原始安全对齐模型 $M_0$。
- $x_{<t}$：生成位置 t 之前的全部上下文词元。
- $s(x)$：样本 x 的来源标签，取 task 或 harm。

<div class="equation-explanation" markdown="1">

**直观理解**：该式是 ROPD 的核心路由规则：专业数据保持遭攻击模型已有的技能分布，有害数据则改向原始模型的安全分布靠拢。由于监督对象是输出概率分布而非某个固定模板下的硬答案，作者认为安全信号对攻击模板的依赖更弱。<br>
**原文位置**：第 3.2 节，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### top-K KL 蒸馏损失与总体目标

$$
\ell_t=\sum_{v\in\mathcal{K}_t}q_t(v)\log\frac{q_t(v)}{p_t(v)}+\bar q_t\log\frac{\bar q_t}{\bar p_t},\qquad \mathcal{L}(\theta)=\mathbb{E}_{x\sim D}\frac{1}{|x|}\sum_{t=1}^{|x|}\ell_t,\quad \bar q_t=1-\sum_{v\in\mathcal{K}_t}q_t(v),\quad \bar p_t=1-\sum_{v\in\mathcal{K}_t}p_t(v)
$$

**符号说明**

- $\ell_t$：位置 t 上的 top-K KL 蒸馏损失。
- $\mathcal{K}_t$：教师分布 $q_t$ 中概率最大的 K 个词元的索引集合。
- $v$：词表中的一个候选词元。
- $q_t(v)$：所选教师在位置 t 对词元 v 分配的概率。
- $p_t(v)=\pi_\theta(v\mid x_{<t})$：学生模型在相同上下文下对词元 v 分配的概率。
- $\bar q_t,\bar p_t$：教师和学生在 top-K 集合之外的聚合尾部概率质量。
- $\mathcal{L}(\theta)$：对混合数据中的样本及其全部词位置平均后的训练目标。
- $D$：任务数据与有害数据组成的混合训练集。
- $|x|$：样本 x 的词元长度，用于按长度归一化。
- $\theta$：待优化的学生模型参数。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项要求学生在教师最看好的 K 个词上复制其相对概率，第二项要求学生为所有其他词保留相近的总概率；总体目标再对每条序列的词位置以及整个数据集取平均。最小化该目标，就是同时在有害输入上缩小学生与安全模型的分布差异、在任务输入上缩小学生与技能模型的分布差异。<br>
**原文位置**：第 3.2 节，公式 (2) 与公式 (3)；此处合并呈现同一优化目标

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练时，根据公式 (1) 为每个样本选择冻结教师，再计算公式 (2) 所定义的逐词 top-K KL 损失，并按公式 (3) 聚合。学生从 $M_a$ 初始化，使用更新式 $\theta\leftarrow\theta-\eta\nabla_\theta\mathcal{L}(\theta)$ 迭代 E 轮；任务样本的损失将参数锚定在原有专业能力附近，有害样本的损失则把预测拉向 $M_0$ 的拒答分布。这里的“on-policy”体现在学生持续以自身当前分布 $p_t$ 参与蒸馏比较，但原文所示算法仍在给定混合语料及其上下文上计算目标，并未描述额外的在线采样或强化学习步骤。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双教师职责分离**

安全教师是未经攻击的 $M_0$，仅为有害样本提供拒答概率分布；任务教师默认直接复用 $M_a$，仅为任务样本提供专业技能分布。教师均冻结，只有从 $M_a$ 初始化的学生参数 $\theta$ 被更新。

> 直观理解：单靠安全教师可能在消除伤害时遗忘技能，而单靠遭攻击模型又无法恢复安全；两位教师分别约束两种行为，使安全修复不必通过大幅扰动全部能力来实现。

**2. 来源条件路由器**

路由器不学习复杂门控，而是读取已知的样本来源标签 s(x)：若为 task，则选任务教师；若为 harm，则选安全教师。路由发生在样本级，所选教师为该样本所有词位置产生蒸馏目标。

> 直观理解：它相当于一个明确的分诊规则，而非让模型自行猜测训练目标，因此安全信号和任务信号不会在同一条样本上相互冲突。

**3. top-K KL 分布蒸馏**

对每个位置仅显式匹配教师概率最高的 K 个词，并把词表其余部分聚合为一个尾部事件；该压缩分布上的 KL 散度既约束高概率决策，又保留对尾部总质量的校准。

> 直观理解：真正影响下一个词选择的通常是概率头部；把大量低概率词打包处理，可降低大词表蒸馏的计算负担，又不会完全忽略剩余概率。

**训练与推理**

训练阶段：准备 $D_{\mathrm{task}}$ 与 $D_{\mathrm{harm}}$，选择防御模板 $T_d$，将两类数据按该模板渲染；冻结 $M_0$ 与 $M_a$ 两个教师，用 $M_a$ 初始化学生；逐批读取样本来源，路由到对应教师，计算所有位置的 top-K KL 损失并仅更新学生。推理阶段：丢弃两个教师和训练路由，只部署最终学生 $\pi_\theta$，按选定的部署模板自回归生成；因此推理不需要判断输入属于 task 还是 harm，也不增加双教师前向开销。需要注意，重对齐和验收模板一致时的安全性不能保证跨系统提示不变，部署模板被切换仍可能导致攻击成功率回升。

**复现信息**

复现方法所必需的设置包括：教师均冻结；学生由失配模型 $M_a$ 初始化；训练混合任务数据和安全数据；防御模板只能由防御者选择，无需知道攻击模板；使用教师分布的 top-K 词元及一个聚合尾部桶计算 KL。算法 1 将 K、训练轮数 E 和学习率 $\eta$ 作为显式超参数；所给消融实验采用 2 轮、学习率 $2\times10^{-5}$、top-50 KL，但节选未说明这是否是全部主实验的统一配置。默认任务教师直接复用 $M_a$，以避免额外训练；干净任务教师可作为效果更强但成本更高的替代方案。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- SQL文本到查询任务：采用Gao et al. (2024)所述SQL数据，用于检验模型在安全重对齐后能否保留结构化查询生成能力；任务指标为完全匹配。原文节选未给出该数据集的正式名称、训练/验证/测试规模或具体划分。
- SAMSum：对话摘要数据集，用于检验安全修复是否损害长对话信息压缩与摘要能力；以ROUGE类文本重叠分数评估。原文节选未报告本实验采用的具体训练、验证和测试样本数。
- NL2Bash与BeaverTails共同构成能力—安全评测：NL2Bash检验自然语言到Shell命令的合成能力；攻击者将每个任务语料与1,500条BeaverTails有害样本混合微调，并使用另外700条留出的BeaverTails提示计算攻击成功率。任务数据和有害数据均先保存为原始输入—输出对，再在加载时分别套用raw、self或attack模板，以独立控制攻击、修复和评测模板。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**下游任务分数**

衡量安全修复后专业技能的保留程度；SQL采用完全匹配，SAMSum采用ROUGE类文本重叠，NL2Bash采用命令准确率。各任务分数含义不同，不能直接跨数据集比较绝对值。 （越高越好，因为更高分表示修复后仍能正确完成对应专业任务。）

</div>
<div class="metric-item" markdown="1">

**ASR（Attack Success Rate，攻击成功率）**

700条留出BeaverTails有害提示中，被模型作出有害回答的比例；回答是否有害由Qwen2.5-32B-Instruct判定。攻击的真实ASR应从与其攻击模板一致的评测通道读取。 （越低越好，因为更低的ASR表示恶意微调所植入的有害行为更少被触发。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 现有防御在攻击模板与防御模板不一致的条件下

<div class="result-value" markdown="1">

作者报告，基线防御在模板不匹配时经常失效，而且这种失效常伴随严重的下游任务性能下降；当前节选未提供表1及后续结果表的具体数值，因此无法核验各基线、模型和任务上的降幅。

</div>

这一结果针对防御者不知道攻击者提示格式的现实条件，说明仅在与修复数据相同的模板下有效并不足够。它同时强调安全与能力必须联合考察：ASR下降若以专业技能大幅退化为代价，并不能视为理想修复。但摘要中的概括不能证明所有基线在所有模型和任务上均失败，具体适用范围仍需核对完整表格。

<div class="result-source" markdown="1">

来源：摘要；对应实验设计见第4.2节，具体数值表在所给节选中缺失

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Our results demonstrate that when baseline defenses face template mismatches, often accompanied by severe degradation in downstream task performance.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### ROPD在模板不匹配条件下的防御有效性与能力保持

<div class="result-value" markdown="1">

作者声称ROPD显著缓解模板不匹配风险，并在降低有害行为与保存下游能力两方面表现出更强鲁棒性；原文节选没有给出可逐项引用的任务分数、ASR或相对提升数值。

</div>

关键含义不是ROPD只在某个固定提示外壳上学会拒答，而是其修复效果据称更能跨模板维持，同时利用被污染模型保留任务知识、利用原始模型提供安全倾向。不过，这只是作者在摘要中的总体结论；缺少表格数值、方差和统计检验时，不能判断优势的绝对幅度或稳定性。

<div class="result-source" markdown="1">

来源：摘要；实验设置见第4.1节，完整定量结果未包含在所给节选中

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, ROPD substantially mitigates template-mismatch risks, maintaining superior robustness in both defense effectiveness and capability preservation.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### ROPD面对进一步模板切换或重新越狱

<div class="result-value" markdown="1">

作者明确承认ROPD并非对模板变化完全免疫，但声称其性能退化相较现有方法可忽略不计；节选未报告该退化的数值、置信区间或具体发生在哪些模型和任务上。

</div>

这表明论文结论是“相对更鲁棒”，而不是“彻底解决模板攻击”。所谓退化可忽略需要结合完整表格中的任务分数和ASR变化判断；它也不等价于对未见过的任意系统提示、编码攻击或自适应攻击都安全。

<div class="result-source" markdown="1">

来源：摘要；所给第4节节选未包含相应定量表格

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

While our analysis indicates ROPD is not entirely immune to template shifts, its performance degradation is negligible compared to existing methods, establishing a new standard for robust LLM realignment.

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

- rollback：回滚式安全恢复方法，代表通过撤销或逆转恶意微调影响来恢复原模型行为的路线；它是有意义的比较对象，因为实验关注的正是后训练污染后的模型修复。
- RESTA：已有安全重对齐方法，按其原论文设置运行；用于比较ROPD与现有参数层面安全恢复方案在模板不匹配时的能力保持和有害行为抑制效果。
- soft-SFT：基于软监督微调的重对齐基线，代表继续使用监督信号修复模型的路线；该比较用于判断ROPD对输出分布进行在线蒸馏是否比直接拟合特定修复数据或模板更稳健。
- SSRD：表征空间防御方法，代表不直接依赖普通输出监督、而在内部表示层面实施安全修复的路线；它可检验ROPD的优势是否仅来自与传统SFT类方法不同。

**实验想回答的问题**

- 当攻击者使用的提示模板未知，且防御模板与攻击模板不匹配时，ROPD能否比现有安全重对齐方法更稳定地降低有害回答的攻击成功率，同时保留文本到SQL、对话摘要和自然语言到Shell命令等专业能力？
- 在不同初始对齐强度的指令模型、不同下游任务以及raw、self、attack三类提示模板之间切换时，ROPD的安全性与任务能力权衡是否具有一致的鲁棒性？

**实验实现**

实验覆盖Llama-2-7B-Chat、Qwen2.5-7B-Instruct和Gemma-2-9B-it三种对齐强度不同的指令模型。攻击者使用4-bit LoRA，将各下游任务语料与1,500条BeaverTails有害样本混合微调。ROPD采用双教师配置：被污染模型充当任务教师，以保存专业技能；原始模型充当安全教师，以恢复安全输出倾向。由于现实中的防御者不知道攻击模板，所有方法都只能使用合法防御模板Td∈{raw,self}；仅当攻击使用attack模板时，额外报告Td=attack作为不可供现实防御者使用的预言机上界。技能保持实验令评测模板与修复模板一致，即Teval=Td，并按“任务分数/ASR”同时报告能力与安全。所有实验运行于NVIDIA H20D GPU；节选未给出学习率、批量大小、训练轮数和随机种子，称详细配置位于补充材料。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It proposes an on-policy distillation defense for robustly realigning compromised LLMs while preserving downstream capabilities.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`c80de25044bc417c0305004250c2b5d1dd32ba691459d8b695ff08c8e9b07960`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
