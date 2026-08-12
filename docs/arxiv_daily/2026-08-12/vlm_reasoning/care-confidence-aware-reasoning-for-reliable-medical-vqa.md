---
title: "[论文解读] CARE: Confidence-Aware Reasoning for Reliable Medical VQA"
description: "[arXiv 2608.10964][VLM Reasoning] CARE面向医疗视觉问答中的置信度失准问题，在两阶段强化微调流程中将诊断正确性与模型自报置信度联合纳入训练，使模型不仅尽可能答对，还能更可信地表达自身不确定性。"
arxiv_id: "2608.10964"
announcement_date: "2026-08-12"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:04:48.768775+00:00"
source_sha256: "2e08fb485f388660597d2613681ab9233a6f7eaa289bf05beaecd01772a4864a"
tags:
  - "VLM Reasoning"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "LLM Reasoning"
  - "医学视觉问答"
  - "医学多模态大语言模型"
  - "强化微调"
  - "思维链"
  - "置信度校准"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.10964</p>

# CARE: Confidence-Aware Reasoning for Reliable Medical VQA

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Yuetian Du, Yucheng Wang, Zhenyuan Chen, Luyuan Chen, Rongyu Zhang, Jinjian Zhang, Wei Zhou, Zhijie Xu, Ming Kong, Zhan Zhou, Jie Liu, Qiang Zhu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Michigan；Affiliation: City University of Hong Kong</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.10964v1) · [PDF 下载](https://arxiv.org/pdf/2608.10964v1) · **关键词** 医学视觉问答, 医学多模态大语言模型, 强化微调, 思维链, 置信度校准<br>
**代码**: [https://github.com/anotherbricki/CARE](https://github.com/anotherbricki/CARE)

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

CARE面向医疗视觉问答中的置信度失准问题，在两阶段强化微调流程中将诊断正确性与模型自报置信度联合纳入训练，使模型不仅尽可能答对，还能更可信地表达自身不确定性。

**不用术语来说**：医疗模型即使给出逐步诊断理由，也可能对错误答案表现得非常肯定，或对正确答案显得没有把握。因此，医生无法仅凭模型表达的确信程度判断答案是否可靠；在错误代价较高的临床场景中，这会削弱模型作为决策支持工具的安全性和可信度。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出置信感知医疗推理框架CARE，在群组相对策略优化（GRPO）中引入置信感知奖励（CAR），把模型表达的置信度作为依赖答案正确性的校准信号，从训练目标层面同时优化诊断正确性与置信度校准。
- 设计可扩展的Medical-CoT自动合成流程，为监督微调构造带有结构化诊断过程和可验证结论的冷启动数据，从而稳定后续强化学习所需的推理格式与答案提取。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

医学视觉问答（Medical VQA）要求多模态大语言模型联合理解医学图像与自然语言问题，并输出诊断或临床问题的答案。传统监督微调通常学习从输入到答案的直接映射，难以呈现可供医生核查的推理依据；强化微调则可利用答案正确性等可验证信号，训练模型生成逐步的思维链。不过，临床可用性不仅取决于答案是否正确，还取决于模型表达的置信度能否真实反映正确概率：若错误诊断仍伴随很高置信度，医生便难以据此判断何时应采纳答案、复核结果或转交专家。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**医学多模态大语言模型（Medical MLLM）**

能够同时处理医学图像和文本的生成模型，例如根据影像及相关问题给出诊断答案。本文关注的模型还需生成可读的推理过程与自身置信度。

</div>
<div class="concept-item" markdown="1">

**思维链（Chain-of-Thought, CoT）**

模型在最终答案之前生成的分步骤推理文本，用于展示其如何从图像证据和医学知识推导结论。思维链提高了过程透明度，但文本看似合理并不保证答案正确或置信度可信。

</div>
<div class="concept-item" markdown="1">

**置信度校准（confidence calibration）**

校准描述模型表达的确定程度与实际正确率是否一致；例如，一批被赋予约 $80\%$ 置信度的回答理想情况下应约有 $80\%$ 正确。置信度失准包括对错误答案过度自信，以及对正确答案不必要地缺乏信心。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文研究带显式推理和置信度表达的医学 VQA：输入是医学图像及其自然语言问题，模型输出结构化临床推理轨迹、最终诊断答案和相应置信度。训练环境包含两阶段设置：先用自动合成并验证的 Medical-CoT 数据进行监督微调，建立稳定的推理格式与答案提取能力；再通过基于可验证结果的强化微调，使答案正确性和置信度校准共同进入优化目标。其核心假设是训练样本具有可核验的标准答案，因而能够判断一次回答是否正确，并据此约束置信度；预期模型不仅提高诊断正确率，还应让高置信度更集中于正确回答、低置信度更合理地对应不确定或错误回答。原文将应用目标定位为临床决策支持，而不是替代医生作出最终诊断。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Med-R1**: 原文将其列为采用强化微调开展医学推理与 Medical VQA 的早期模型。它说明可验证奖励能够促进医学思维链生成，但本文节选未表明其训练目标显式约束置信度与答案正确率之间的对应关系。
- **MedVLM-R1**: 这是与 CARE 直接对照的医学推理多模态模型；引言和图 1 以其说明现有方法可能出现置信度失准，即表达的确定性不能可靠反映实际诊断准确性。CARE 在这一类正确性导向的强化微调框架上进一步引入以正确性为条件的置信度校准信号。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

医疗视觉问答模型可能参与临床决策支持，而诊断错误具有较高风险。临床人员不仅需要看到可解释的逐步推理，还需要判断模型何时值得信任、何时应由医生复核；如果模型表达的把握程度与实际正确率不一致，其置信度就不能作为风险分流或人工复核的可靠依据。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于临床指令数据的监督微调（SFT）**：利用整理好的医疗指令及参考答案训练多模态大模型，使其学习从医学图像和问题到答案的直接映射；部分方法也通过监督数据模仿已有的思维链（CoT），但本质上仍是拟合给定训练样本的输出分布。
- **以答案正确性为核心奖励的强化微调（RFT）**：Med-R1、MedVLM-R1等方法使用GRPO一类强化学习算法，根据可验证的答案结果反馈调整策略，使模型探索并生成较长的逐步医学推理路径；其主要奖励通常关注最终答案是否正确。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统SFT容易形成直接的输入到输出映射，即使加入思维链监督，也主要是被动模仿既有数据，未必能够根据可验证结果动态修正推理路径；这使诊断过程的透明性和可验证性不足，难以满足临床人员审查推理依据的需要。
- 现有医疗RFT虽然提高了推理透明度，却主要奖励答案正确性，没有显式约束置信度与实际正确率的一致性。因此，模型可能对错误诊断给出不应有的高置信度，也可能对正确诊断过度保守，导致其自报置信度无法可靠反映预测风险。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作分别推进了可解释医学推理和基于结果反馈的答案优化，但仍缺少一种统一训练机制：它应把置信度视为与答案正确性相联系的校准信号，而不是单纯诱导模型报告置信度或一概奖励更高置信度，并且还要有稳定、可验证的医学推理冷启动数据支撑后续强化学习。

</div>
<div markdown="1"><span>核心问题</span>

能否在医疗视觉问答的两阶段训练流程中，通过结构化Medical-CoT冷启动和正确性条件化的置信感知奖励，让模型在提高诊断准确率的同时降低置信度失准，而不必在准确性与校准性之间作简单取舍？

</div>
<div markdown="1"><span>作者直觉</span>

只奖励答对会告诉模型“结果好不好”，却不会教它“应该有多大把握”。CARE的切入点是让奖励同时检查答案与置信度：答对时支持与正确性相称的确信，答错时惩罚无根据的高确信，从而使模型逐渐把置信表达与真实诊断能力绑定。此前的Medical-CoT冷启动则先教会模型以稳定格式呈现诊断过程和结论，降低强化学习阶段因输出格式混乱而无法可靠判分的风险。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CARE采用“数据合成、监督冷启动、置信度感知强化学习”的端到端训练路线。首先从医学视觉问答数据集$\mathcal{D}_{\mathrm{VQA}}$中的图像$V$、问题$Q$和标准答案$Y$出发，让基础多模态大语言模型在已知答案的条件下反向生成诊断推理轨迹$\mathcal{T}$，再由辅助验证器筛除结论不一致或逻辑不成立的样本，形成$\mathcal{D}_{\mathrm{CoT}}$。随后，模型先通过监督微调学习规定的临床推理格式，再通过GRPO在同一问题的多条候选回答之间进行相对优化，并以置信度感知奖励CAR同时约束答案格式、诊断正确性及置信度与正确性的匹配程度。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 医学CoT反向合成

基础多模态模型$\pi_\theta$在同时看到$V_i$、$Q_i$和$Y_i$的条件下采样中间推理轨迹$\mathcal{T}_i$，并按照视觉分析、鉴别诊断和结论总结等显式阶段组织输出。

<div class="method-step__io" markdown="1">

**输入**：标准医学视觉问答样本$(V_i,Q_i,Y_i)\in\mathcal{D}_{\mathrm{VQA}}$，其中$V_i$是医学视觉内容，$Q_i$是问题，$Y_i$是标准诊断答案。<br>
**输出**：带有候选结构化推理轨迹的四元组$(V_i,Q_i,\mathcal{T}_i,Y_i)$。

</div>

**直观理解**：这相当于先给模型看正确答案，再要求它补写一条能够从图像证据走到该答案的诊断过程，从而减少逐条邀请临床专家撰写推理标注的成本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 推理轨迹验证与数据筛选

辅助验证器检查轨迹的临床有效性、逻辑连贯性以及最终结论是否与$Y_i$完全一致；仅当推理链能够逻辑推出正确结论时，样本才被接纳。

<div class="method-step__io" markdown="1">

**输入**：合成的推理轨迹$\mathcal{T}_i$及对应标准答案$Y_i$。<br>
**输出**：经过质量过滤的医学推理训练集$\mathcal{D}_{\mathrm{CoT}}$。

</div>

**直观理解**：验证器充当自动质检员，防止模型把“答案碰巧正确但过程错误”的轨迹当作示范学习；不过这种质量保证仍取决于辅助验证器本身的判断可靠性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### SFT结构化推理冷启动

采用教师强制的最大似然监督微调，使模型逐词预测目标推理与答案，并学习规定的结构化临床推理格式。

<div class="method-step__io" markdown="1">

**输入**：训练样本$(V,Q,\mathcal{T},Y)\in\mathcal{D}_{\mathrm{CoT}}$及目标序列$S=[\mathcal{T};Y]$。<br>
**输出**：能够生成基本诊断推理链的参考策略$\pi_{\mathrm{ref}}$，同时作为强化学习策略$\pi_\theta$的初始化与KL约束参照。

</div>

**直观理解**：这一阶段先让模型学会“怎样按要求作答”，避免直接进入强化学习时因输出格式和医学推理能力不足而只能获得稀疏或无意义的奖励。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于CAR的GRPO强化学习

分别计算格式奖励$R_{\mathrm{form}}$、答案正确性奖励$R_{\mathrm{out}}$和校准奖励$R_{\mathrm{calib}}$，将总奖励在同组$K$个候选中标准化为相对优势$A_i$；GRPO利用裁剪策略目标更新$\pi_\theta$，并通过KL惩罚限制其偏离$\pi_{\mathrm{ref}}$。

<div class="method-step__io" markdown="1">

**输入**：每个视觉问题$(V,Q)$、策略生成的$K$个候选输出$\{o_1,\ldots,o_K\}$、标准答案$Y$及参考策略$\pi_{\mathrm{ref}}$。<br>
**输出**：兼顾诊断正确性、输出规范性及置信度校准的最终CARE策略。

</div>

**直观理解**：同一问题的多份候选回答相互比较，优于组内平均水平的回答得到正向更新；CAR进一步规定，答对时高置信度才值得奖励，答错时高置信度反而应受惩罚。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### GRPO策略优化目标

$$
J_{\mathrm{GRPO}}(\theta)=\mathbb{E}\left[\frac{1}{K}\sum_{i=1}^{K}\min\left(\rho_i,\operatorname{clip}(\rho_i,1-\epsilon,1+\epsilon)\right)A_i-\beta\mathbb{D}_{\mathrm{KL}}(\pi_\theta\|\pi_{\mathrm{ref}})\right]
$$

**符号说明**

- $J_{\mathrm{GRPO}}(\theta)$：用于更新参数$\theta$的GRPO期望目标。
- $K$：针对同一个视觉问题采样的候选输出数量。
- $\rho_i$：第$i$个候选的策略概率比，即重要性权重；但所给原文公式将分子和分母都写为$\pi_\theta(o_i\mid V,Q)$，无法形成通常意义上的新旧策略比值，应结合论文排版源或代码核查。
- $\epsilon$：限制策略概率比变化范围的裁剪系数。
- $A_i$：第$i$个候选的组内相对优势，由总奖励$R_i$减去组均值后再除以组标准差得到。
- $\beta$：控制KL散度惩罚强度的系数。
- $\mathbb{D}_{\mathrm{KL}}(\pi_\theta\|\pi_{\mathrm{ref}})$：当前策略$\pi_\theta$相对参考策略$\pi_{\mathrm{ref}}$的KL散度，用于抑制过大的策略偏移。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标根据候选回答相对于同组其他回答的奖励高低调整生成概率，并通过裁剪避免单次更新幅度过大。KL项要求优化后的模型不要为迎合奖励而远离监督微调阶段形成的结构化医学推理策略。<br>
**原文位置**：第2.3节，公式(3)；组内优势定义见公式(4)

</div>

</div>

<div class="equation-block" markdown="1">

#### 答案级置信度与校准奖励

$$
C(a_i)=\frac{1}{|a_i|}\sum_{j=1}^{|a_i|}\pi_\theta(t_j\mid V,Q,t_{<j}),\qquad R_{\mathrm{calib}}(o_i,Y)=R_{\mathrm{out}}\,C(a_i)-\lambda\left(1-R_{\mathrm{out}}\right)C(a_i)
$$

**符号说明**

- $a_i$：第$i$个输出$o_i$中位于`<answer>`区间内的答案词元序列，不包含推理、格式和特殊词元。
- $|a_i|$：答案区间中的词元数量。
- $t_j$：答案序列中的第$j$个词元。
- $\pi_\theta(t_j\mid V,Q,t_{<j})$：给定视觉内容$V$、问题$Q$和先前答案词元$t_{<j}$时，策略对实际生成词元$t_j$赋予的概率。
- $C(a_i)$：答案词元预测概率的算术平均，被用作答案级预测置信度。
- $R_{\mathrm{out}}$：诊断正确性奖励；封闭式任务采用精确匹配指示，开放式任务采用基于召回率的答案覆盖度。
- $\lambda$：错误预测具有高置信度时的惩罚强度。
- $R_{\mathrm{calib}}(o_i,Y)$：候选输出$o_i$相对于标准答案$Y$的置信度校准奖励。

<div class="equation-explanation" markdown="1">

**直观理解**：CARE只平均最终答案区间的词元概率，避免较长的推理文本和格式标记直接干扰诊断置信度。若答案正确，置信度越高奖励越大；若答案错误，同一置信度会按$\lambda$受到惩罚，因此该式优化的是“置信度是否与正确性一致”，而不是无条件鼓励模型更自信。<br>
**原文位置**：第2.4节，公式(5)与公式(6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：SFT阶段最小化目标序列$S=[\mathcal{T};Y]$的负对数似然，使模型获得结构化医学推理能力并产生参考策略$\pi_{\mathrm{ref}}$。强化学习阶段则最大化$J_{\mathrm{GRPO}}(\theta)$：每个候选的总奖励由格式、答案质量和校准三部分相加，随后在同一问题的$K$个候选内标准化为$A_i$；其中CAR使正确且高置信度的答案获得额外收益，使错误且高置信度的答案受到惩罚，而KL正则负责维持策略稳定性。需要注意，开放式任务的$R_{\mathrm{out}}$可能是连续的召回型分数，因此公式中的$1-R_{\mathrm{out}}$表示未覆盖程度，而不一定只是二元错误指示。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 可扩展医学CoT合成与验证模块**

生成模型依据$(V_i,Q_i,Y_i)$反向采样$\mathcal{T}_i$，结构模板要求显式推理阶段和结论总结；辅助验证器将轨迹与$Y_i$核对，只有逻辑结论完全一致的轨迹才能进入$\mathcal{D}_{\mathrm{CoT}}$。

> 直观理解：该模块把已有的图像、问题和答案转化为可用于学习推理过程的数据，同时用自动验证减少低质量合成轨迹造成的错误监督。

**2. 两阶段优化模块**

第一阶段以$S=[\mathcal{T};Y]$为监督目标训练参考策略$\pi_{\mathrm{ref}}$；第二阶段对每个$(V,Q)$采样$K$个候选，以$A_i=(R_i-\mu(R_{1:K}))/\sigma(R_{1:K})$计算组内标准化优势，并采用带裁剪和KL正则的GRPO更新策略。

> 直观理解：监督学习负责建立稳定的医学推理起点，强化学习再根据候选回答的相对质量做定向改进；KL约束用于防止策略为了追逐奖励而过度偏离已学到的合理表达方式。

**3. 置信度感知奖励CAR**

总奖励为$R_i=R_{\mathrm{form}}+R_{\mathrm{out}}+R_{\mathrm{calib}}$。其中$R_{\mathrm{form}}\in\{0,1\}$检查是否使用指定的`<think>`与`<answer>`分隔符；$R_{\mathrm{out}}$对封闭式任务采用答案精确匹配指示，对开放式任务采用基于召回率的标准答案覆盖度；$R_{\mathrm{calib}}$只根据`<answer>`区间内词元的平均预测概率评估答案级置信度，并按答案是否正确给予相反方向的激励。

> 直观理解：普通奖励只判断答案对不对，无法区分“自信地答错”和“谨慎地答错”。CAR把置信度纳入奖惩，使模型不仅追求正确答案，还学习让表达出来的确定程度更接近真实可靠性。

**训练与推理**

训练时，先从$\mathcal{D}_{\mathrm{VQA}}$自动生成并验证医学推理轨迹，构造$\mathcal{D}_{\mathrm{CoT}}$；再以$(V,Q)$为条件、以$[\mathcal{T};Y]$为目标进行SFT，得到$\pi_{\mathrm{ref}}$；最后初始化$\pi_\theta$并对每个问题采样$K$个输出，解析`<think>`和`<answer>`区间，计算$R_{\mathrm{form}}$、$R_{\mathrm{out}}$、$C(a_i)$及$R_{\mathrm{calib}}$，形成组内优势并执行GRPO更新。推理时只需向最终CARE策略提供新的医学视觉内容$V$和问题$Q$，模型生成带结构化推理及最终答案的输出；原文节选未说明推理阶段是否显式展示数值置信度，也未说明是否采用额外采样、集成或后处理。

**复现信息**

复现时最关键的是保持数据与奖励边界一致：CoT轨迹必须遵循显式阶段模板并通过辅助验证器与标准答案的一致性检查；SFT目标连接推理轨迹与答案；强化学习只用`<answer>`区间内的普通答案词元计算$C(a_i)$，排除推理、格式及特殊词元。封闭式与开放式任务分别采用精确匹配和基于召回率的$R_{\mathrm{out}}$，但所给章节未明确报告基础模型、$K$、$\epsilon$、$\beta$、$\lambda$、学习率或具体开放式召回公式；此外，公式(3)中的$\rho_i$定义疑似存在排版错误，这些信息均需通过论文其他章节或公开代码核实。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- VQA-RAD：放射学医学视觉问答数据集，包含315幅由临床人员标注的图像和3,515个问答对。它用于检验模型在规模较小、专业性较强的放射影像场景中回答开放式与封闭式问题的能力；原文未明确报告实验采用的数据划分。
- SLAKE：带语义标签和外部知识的医学视觉问答数据集，包含642幅图像和14,000个双语问答对。它用于检验模型在知识增强且问题形式更丰富的场景中的诊断回答与置信度校准；原文未明确报告使用了哪种语言子集及数据划分。
- PathVQA：病理学视觉问答数据集，包含4,998幅图像和32,799个问答对。它用于检验方法能否从放射学迁移到病理图像，并处理更大规模的开放式与封闭式问答；原文未明确报告实验数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**诊断准确性（Accuracy或Recall）**

封闭式问题报告Accuracy，即答案完全正确的样本比例；开放式问题按照医学视觉问答惯例报告Recall，用来衡量参考答案中的目标信息被模型回答覆盖的程度。表1统一以ACC标示总体结果，而表2分别列出Open与Closed结果。 （越高越好，因为更高数值表示模型给出正确诊断答案或覆盖关键答案信息的能力更强。）

</div>
<div class="metric-item" markdown="1">

**期望校准误差（ECE）**

将预测按置信度划分为$M$个等宽区间$B_m$，计算每个区间的平均置信度与实际准确率之差，再按样本数加权汇总。它衡量模型说自己“有多确定”是否与实际正确概率一致。 （越低越好；$0$表示分箱意义下置信度与经验准确率完全一致。ECE降低说明置信度更可信，但不等价于准确率必然提高。）

</div>
<div class="metric-item" markdown="1">

**幻觉率（HR）**

使用Lingshu-32B作为视觉语言模型裁判，在固定提示、统一评分规则和确定性解码下评价推理轨迹；每个样本的归一化幻觉分数还结合输出token数，并通过全局常数归一化到$[0,1]$。该指标试图衡量推理中缺乏图像或医学依据的内容。 （越低越好，因为更低数值表示裁判识别出的无依据推理更少；但它依赖自动裁判及其评分规则，不能直接等同于临床专家认定的事实错误率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### VQA-RAD总体比较

<div class="result-value" markdown="1">

CARE-7B取得0.767 ACC、0.202 ECE和0.048 HR；在表1所列模型中，这三个指标分别为最高、最低和最低。

</div>

这表明CARE在放射学问答上没有通过牺牲校准或增加幻觉来换取准确率，而是在三个维度上同时领先。相较相近规模基线Lingshu-7B的0.679 ACC、0.375 ECE和0.083 HR，优势不只表现为答案更准确，也表现为置信度与正确率更一致、自动裁判检测到的无依据内容更少。不过该结果不能单独证明CAR造成了全部提升，因为完整CARE还包含医学思维链冷启动和其他训练差异。

<div class="result-source" markdown="1">

来源：表1，CARE-7B（Ours）行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

CARE-7B (Ours) 0.767 0.202 0.048 0.873 0.115 0.070 0.689 0.290 0.059

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### SLAKE总体比较

<div class="result-value" markdown="1">

CARE-7B取得0.873 ACC、0.115 ECE和0.070 HR，三项均为表1最佳；作者进一步声称，0.115 ECE相对第二名Fleming-VL-8B的0.181降低约36%。

</div>

SLAKE结果是CAR有效性的主要证据：准确率提高的同时，ECE反而降低，说明训练后的高置信度总体上更接近真实正确率。按$(0.181-0.115)/0.181$计算，相对降幅约为36.5%，与作者的“36%”表述一致。但ECE是分箱汇总指标，不能说明每个置信度区间、每种疾病或每类问题都同样校准良好。

<div class="result-source" markdown="1">

来源：表1，CARE-7B（Ours）行；第3.3节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

CARE-7B (Ours) 0.767 0.202 0.048 0.873 0.115 0.070 0.689 0.290 0.059

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### PathVQA总体比较

<div class="result-value" markdown="1">

CARE-7B取得0.689 ACC、0.290 ECE和0.059 HR，在表1列出的模型中同样同时达到最高准确率、最低ECE和最低HR。

</div>

该结果说明三目标优势并非只出现在放射影像数据上，也延伸到病理学场景。尤其是CARE相对最高准确率基线MedVLThinker-7B的0.652 ACC有所提高，同时其ECE从0.569降至0.290、HR从0.082降至0.059。不过这仍属于数据集内基准测试，不能推出模型已经具备跨医院、跨设备或真实临床部署中的可靠性。

<div class="result-source" markdown="1">

来源：表1，CARE-7B（Ours）行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

CARE-7B (Ours) 0.767 0.202 0.048 0.873 0.115 0.070 0.689 0.290 0.059

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验只覆盖三个公开医学VQA基准，且原文未明确数据划分、外部医院测试、患者层面去重或分布外评估，因此尚不能判断CARE面对真实临床域偏移、罕见疾病和不同成像设备时是否仍保持校准。
- HR依赖Lingshu-32B自动裁判，ECE则依赖置信度提取方式和分箱设置；原文未报告临床专家复核、裁判一致性、分箱数$M$、置信区间、重复运行或显著性检验。此外，消融没有单独比较“使用CAR”与“使用普通正确性奖励”，因此CAR相对一般RL奖励的独立因果贡献仍未被完全隔离。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- MedVLM-R1-2B：紧凑规模的推理型医学多模态模型，用来判断CARE的收益是否仅来自采用更大参数规模；不过两者参数量并不匹配，因此比较同时包含方法和模型容量差异。
- Lingshu-7B：与CARE同处7B规模，并且在三个数据集上具有较低幻觉率，是检验CARE能否在相近容量下兼顾准确率、校准和幻觉控制的重要基线。
- MedVLThinker-7B：与CARE参数规模相近的医学视觉推理模型，用于比较显式医学推理训练方法；其部分准确率较强，但ECE较高，因此能体现校准目标的必要性。
- Fleming-VL-8B：标准规模的强基线，在多数数据集上具有较有竞争力的ECE和幻觉率，尤其是SLAKE上第二低的ECE，因此适合衡量CAR带来的额外校准收益。

**实验想回答的问题**

- CARE能否在VQA-RAD、SLAKE和PathVQA上同时提高医学视觉问答的诊断准确性、置信度校准质量，并降低推理幻觉，而不是仅在其中一个目标上取得优势？
- 监督微调冷启动（SFT）与采用置信度感知奖励的强化学习（RL）分别适合哪些问题类型，二者组合是否对开放式医学问答更重要？

**实验实现**

CARE以Qwen2.5-VL-7B-Instruct为基础，同一架构既用于合成思维链数据，也作为后续训练的策略模型。训练采用全参数微调并使用6张NVIDIA A100 GPU；SFT冷启动使用AdamW与余弦退火。GRPO阶段每个问题生成$K=4$条 rollout，批大小为2，采用bfloat16混合精度；CAR中的校准惩罚系数为$\lambda=0.5$。原文给出的SFT学习率指数在所提供HTML文本中缺失，因此不能可靠还原。评测中，封闭式和开放式问题分别使用Accuracy与Recall；幻觉评测对所有方法使用相同输入、固定提示及确定性解码。原文未报告随机种子、重复实验次数、误差条或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 仅RL与SFT+RL在封闭式问题上的比较 | RL在三个数据集的封闭式问题上均取得最佳组合：VQA-RAD为0.864准确率和0.096 ECE，SLAKE为0.861和0.119，PathVQA为0.955和0.020；相比之下，SFT+RL对应为0.658和0.323、0.779和0.209、0.863和0.121。 | 该消融隔离了是否先进行SFT冷启动对后续训练的影响。结果表明，当答案来自受限空间时，直接RL可能更高效，SFT初始化甚至可能限制策略探索或引入不适合封闭式作答的生成格式。但表2的“RL”是否使用完整CAR、各配置是否具有完全相同训练预算，所给原文没有进一步说明，因此不能把差异完全归因于SFT本身。 | 表2，RL与SFT+RL行<br><span class="experiment-evidence">RL 0.563 0.407 0.864 0.096 0.819 0.176 0.861 0.119 0.166 0.727 0.955 0.020
SFT+RL 0.620 0.363 0.658 0.323 0.881 0.112 0.779 0.209 0.421 0.561 0.863 0.121</span> |
| 开放式问题中的冷启动作用 | SFT+RL在开放式准确性上均为最佳：VQA-RAD、SLAKE和PathVQA分别达到0.620、0.881和0.421。SFT单独训练已将SLAKE开放式结果从Training-Free的0.513提高到0.803，之后SFT+RL进一步提高到0.881；对应ECE从0.456降至0.188，再降至0.112。 | 该比较说明开放式回答首先需要SFT建立稳定的医学思维链和自由文本输出格式，RL再在此基础上改善答案与校准。它支持两阶段训练的互补性，但也揭示一个重要边界：在PathVQA开放式问题上，SFT+RL的ECE为0.561，高于SFT的0.640之外虽有改善，却仍劣于RL的0.727以外的准确率关系较复杂；因此“两阶段总是改善所有指标”并不成立，更准确的结论是它优先提升开放式回答的任务表现。 | 表2，Training-Free、SFT与SFT+RL行<br><span class="experiment-evidence">Training-Free 0.483 0.485 0.658 0.341 0.513 0.456 0.690 0.287 0.150 0.823 0.664 0.326
SFT 0.520 0.468 0.629 0.359 0.803 0.188 0.767 0.225 0.349 0.640 0.857 0.133
SFT+RL 0.620 0.363 0.658 0.323 0.881 0.112 0.779 0.209 0.421 0.561 0.863 0.121</span> |

**定性案例**

- 图3给出训练前后的归一化置信度分布：训练后分布整体向更高置信度区域移动。结合表1和表2中ECE下降，作者将其解释为置信度与正确率的对齐改善，而非无条件提高自信。该图属于总体分布分析，并非展示具体医学问题、图像和推理轨迹的个案；原文未提供可供核查的定性诊断案例。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper improves medical visual reasoning through supervised chain-of-thought training and confidence-aware reinforcement fine-tuning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`2e08fb485f388660597d2613681ab9233a6f7eaa289bf05beaecd01772a4864a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
