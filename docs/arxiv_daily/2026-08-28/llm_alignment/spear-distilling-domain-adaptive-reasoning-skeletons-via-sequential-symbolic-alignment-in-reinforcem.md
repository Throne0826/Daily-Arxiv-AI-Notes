---
title: "[论文解读] SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning"
description: "[arXiv 2608.26550][对齐 / RLHF] SPEAR通过将教师和学生的自然语言推理轨迹转换为领域相关的符号里程碑，并用最长公共子序列进行顺序对齐，为强化学习知识蒸馏提供无需训练神经过程奖励模型的稠密过程奖励。"
arxiv_id: "2608.26550"
announcement_date: "2026-08-28"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:31:15.326106+00:00"
source_sha256: "ba0334d310e047146e461a72cd6255f8d971d922e2e473ac2375f95e3a400638"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "强化学习"
  - "知识蒸馏"
  - "在线策略强化学习"
  - "过程奖励"
  - "符号对齐"
  - "最长公共子序列"
  - "多步推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.26550</p>

# SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Zhuochun Li, Yuelyu Ji, Yiming Zeng, Daqing He</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Pittsburgh, Pittsburgh, USA；Affiliation: University of Connecticut, Storrs, USA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26550v1) · [PDF 下载](https://arxiv.org/pdf/2608.26550v1) · **关键词** 知识蒸馏, 在线策略强化学习, 过程奖励, 符号对齐, 最长公共子序列, 多步推理<br>
**代码**: [https://github.com/zhuochunli/SPEAR](https://github.com/zhuochunli/SPEAR)

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

SPEAR通过将教师和学生的自然语言推理轨迹转换为领域相关的符号里程碑，并用最长公共子序列进行顺序对齐，为强化学习知识蒸馏提供无需训练神经过程奖励模型的稠密过程奖励。

**不用术语来说**：教师模型能够给出复杂的多步推理，但学生模型在模仿这些答案时，可能只学到表达方式，而没有学会推理步骤本身。若只根据最终答案是否正确来奖励，学生很难知道中间哪一步出了问题；若逐步使用神经网络评价推理过程，又会带来较高的计算和训练成本。因此，论文试图寻找一种既能指导中间推理、又不依赖昂贵评价模型的方法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出SPEAR，一种无需额外训练、可插入现有序列级在线强化学习知识蒸馏流程的符号过程奖励框架，用教师推理轨迹中的结构信息替代神经过程奖励模型。
- 将数学、科学和常识任务中的自然语言推理转换为领域自适应的符号锚点，并利用最长公共子序列保持推理步骤的先后关系，从而在不要求学生复述教师原文的情况下监督其逻辑骨架。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型推理能力蒸馏与强化学习交叉领域，目标是把大型教师模型的多步推理能力迁移到资源开销较低的小型学生模型。传统监督微调让学生模仿教师预先生成的推理文本，容易学到表达风格而非逻辑转换，并因训练时只接触教师轨迹而产生“暴露偏差”；基于强化学习的在线策略蒸馏则让学生从当前策略生成自己的推理轨迹，再依据奖励更新。其核心困难在于奖励设计：只检查最终答案的结果奖励过于稀疏，难以指出中间逻辑是否正确；神经过程奖励模型虽能提供密集监督，却需要额外训练和推理成本，并可能在特定领域产生错误判断。数学和编程可借助确定性规则验证中间步骤，但科学与常识推理通常以表述多样、边界模糊的自然语言呈现，因此需要一种不拘泥于逐词一致、又能检验推理顺序的通用过程信号。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**在线策略知识蒸馏**

学生模型使用自身当前策略生成推理轨迹，并在教师信息或奖励信号指导下进行强化学习，而不是仅模仿固定的教师数据。这样训练时看到的轨迹更接近学生实际推理时会遇到的状态。

</div>
<div class="concept-item" markdown="1">

**过程奖励**

过程奖励评价最终答案之前的中间推理质量，为多步推理提供比成败式结果奖励更密集的反馈。本文关注的是无需额外神经验证器、可直接接入强化学习流程的过程奖励。

</div>
<div class="concept-item" markdown="1">

**最长公共子序列（LCS）**

LCS是在保持元素先后顺序但允许跳过部分元素的条件下，寻找两个序列共有的最长子序列。它适合衡量学生是否依次覆盖教师的关键推理里程碑，同时不强制双方使用完全相同的自然语言。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一道数学、科学或常识推理题，以及强教师模型产生的详细推理轨迹，系统需要训练较小的学生模型，使其在在线策略强化学习中自主生成推理过程和最终答案。本文假设教师轨迹包含可迁移的中间逻辑，但教师与学生的具体措辞不必一致；因此，评价对象不是逐词相似度，而是从两方自然语言轨迹中抽取出的领域自适应符号里程碑及其顺序一致性。期望输出是一个经蒸馏的学生策略：既能获得正确结果，也能沿合理的逻辑顺序推进，并且不依赖另行训练的神经过程奖励模型。数学任务的符号轨迹可描述计算过程，科学任务可描述因果依赖，常识任务可描述实体状态转移；这些符号表示构成跨语言表达进行过程对齐的中间层。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **GRPO（Group Relative Policy Optimization）**: GRPO及其改进方法是推理强化学习的代表性优化框架，但通常依赖稀疏的二元结果奖励。SPEAR并非替代此类策略优化算法，而是提供可接入标准强化学习流程的密集、顺序感知过程奖励，以缓解仅凭最终答案训练时的逻辑指导不足和冗余推理问题。
- **RePAIR、Logic-RL与既有LCS奖励方法**: RePAIR和Logic-RL表明基于规则的过程奖励可以成为无需训练的可验证替代方案，既有研究也已使用LCS识别较优推理路径。SPEAR在此基础上将不同领域的自然语言推理映射为符号化、有顺序的轨迹，使LCS对齐能够从形式化任务扩展到科学和常识等语言变化更大的推理场景。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

将大型教师语言模型的复杂推理能力迁移到资源受限的小型语言模型，对于降低部署成本和扩大实际应用十分重要。传统离线蒸馏通常让学生学习教师生成的完整推理文本，但这种训练方式容易使学生依赖教师的语言风格；推理时一旦学生走上训练样本未覆盖的错误路径，就缺乏自行纠正的能力。在线强化学习知识蒸馏允许学生探索自己的推理轨迹，因此更适合学习推理过程，但其奖励设计仍是实际应用中的关键瓶颈。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **稀疏结果奖励**：在学生完成整条推理后，只根据最终答案是否正确或是否通过验证来计算奖励。它实现简单、计算开销低，但几乎不说明中间推理步骤的质量。
- **神经过程奖励模型或细粒度分布奖励**：使用专门训练的过程奖励模型逐步评估推理，或在教师与学生的输出之间进行细粒度的概率分布比较，以提供更密集的学习信号。这类方法能提供过程指导，但通常需要额外的模型训练、推理和大规模计算。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 仅依赖最终结果的奖励对多步推理过于稀疏：当答案错误时，学生无法知道是哪个逻辑转折导致失败，强化学习信号也难以有效传回早期步骤。
- 现有过程监督主要适用于数学、编程等中间步骤和答案较易验证的形式化领域；在科学和常识推理中，自然语言表达变化大、步骤边界不清，训练神经过程评价器或进行逐词匹配的成本高，也可能把合理的不同表达错误地视为不一致。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种低成本、无需额外训练神经验证器、又能利用教师详细推理轨迹来监督学生中间逻辑的通用方法，尤其需要适应科学和常识等非形式化任务，并同时允许学生使用不同的语言表达。

</div>
<div markdown="1"><span>核心问题</span>

能否把教师推理轨迹压缩为与任务领域相关的符号里程碑，再通过保持里程碑顺序的匹配，为学生在线探索生成稠密且有效的过程奖励，从而在不进行文本逐词模仿的情况下缩小教师与学生之间的推理能力差距？

</div>
<div markdown="1"><span>作者直觉</span>

完整推理文本包含大量措辞差异和冗余，但其中通常存在更稳定的结构，例如数学中的计算过程、科学中的因果关系、常识任务中的实体状态变化。若先提取这些结构作为学生需要经过的关键检查点，再用最长公共子序列判断学生是否按合理顺序达到这些检查点，就能奖励逻辑进展而不是表面措辞。这样，学生可以用自己的语言完成推理，同时仍受到教师推理骨架的约束；作者在原文中将其概括为“dense and order-aware reward”，并指出该设计旨在“enforces chronological logical consistency while granting SLMs the freedom to formulate their own response”（引言，Figure 2说明）。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SPEAR将教师的自然语言推理轨迹压缩为按顺序排列的“符号里程碑”，再用这些里程碑监督学生的在线强化学习探索。给定问题$q$、教师回答$y_t$、学生回答$y_s$与标准答案$y_{gold}$，系统先检查学生是否按要求输出`<think>`和`<answer>`，然后根据任务类型$\tau$选择数学、科学或常识领域的投影函数$\Phi(\cdot,\tau)$，分别从教师与学生推理中得到符号轨迹$\mathcal{A}_t$和$\mathcal{A}_s$；随后以最长公共子序列衡量两条轨迹中里程碑的覆盖程度及先后顺序，并将该过程分数与答案正确性组合为强化学习奖励。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 教师轨迹准备与学生在线采样

教师为$q$生成包含推理与答案的结构化响应$y^T=(y_{think},y_{ans})$，学生策略则针对同一问题在线采样候选回答$o$。这里不要求学生逐词复现教师，而是允许其采用不同措辞和中间表达。

<div class="method-step__io" markdown="1">

**输入**：问题$q$、教师模型$\mathcal{M}_T$、当前或旧学生策略$\pi_{\theta_{\mathrm{old}}}$。<br>
**输出**：教师参考轨迹$y_t$与一组学生探索轨迹$y_s$。

</div>

**直观理解**：教师提供的是解题路线的参考，而不是要求学生照抄整篇答案；学生可以走自己的语言路径，只要关键推理节点及其顺序合理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 格式门控与答案验证

系统解析`<think>`与`<answer>`区块；若格式不合法，立即返回总奖励$0$，否则从答案区块计算结果正确性奖励$R_{acc}$。

<div class="method-step__io" markdown="1">

**输入**：学生回答$y_s$及标准答案$y_{gold}$。<br>
**输出**：格式指示量$\mathbb{I}_{fmt}$、学生推理文本$y_{think}$、学生答案$y_{ans}$及$R_{acc}$。

</div>

**直观理解**：这一步先确保模型把思考过程和最终答案分开书写；格式不合格时不给奖励，避免后续抽取器面对无法可靠解析的文本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 领域自适应符号投影

系统使用$\mathcal{A}_s=\Phi(y_{think},\tau)$和$\mathcal{A}_t=\Phi(y_t,\tau)$生成符号序列：数学任务抽取LaTeX表达式与显式赋值，科学任务抽取以动词为中心的主客体关系，常识任务抽取名词短语及其支配动作。若任一轨迹为空，则跳过过程对齐并仅返回$R_{acc}$。

<div class="method-step__io" markdown="1">

**输入**：学生推理$y_{think}$、教师轨迹$y_t$与任务类型$\tau\in\{\mathrm{math},\mathrm{sci},\mathrm{com}\}$。<br>
**输出**：学生符号轨迹$\mathcal{A}_s=[a_{s,1},\ldots]$与教师符号轨迹$\mathcal{A}_t=[a_{t,1},\ldots]$。

</div>

**直观理解**：投影函数像一支只标记解题关键帧的荧光笔：数学中关注公式变化，科学中关注“谁对谁做了什么”，常识中关注对象及其状态或动作变化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 顺序对齐与复合奖励计算

动态规划计算两条轨迹的最长公共子序列，并据此得到$R_{reason}$；随后按$R_{spear}=\mathbb{I}_{fmt}(R_{acc}+\lambda R_{reason})$合成奖励，主实验取$\lambda=0.5$。

<div class="method-step__io" markdown="1">

**输入**：符号轨迹$\mathcal{A}_s$、$\mathcal{A}_t$，答案奖励$R_{acc}$及格式指示量$\mathbb{I}_{fmt}$。<br>
**输出**：用于策略优化的标量奖励$R_{spear}$。

</div>

**直观理解**：只有按正确先后顺序出现的共同里程碑才得分；答案对不对决定结果奖励，而推理与教师路线部分一致时还能获得连续的过程反馈。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### LCS-F1过程对齐奖励

$$
R_{\mathrm{reason}}=\frac{2\left|\operatorname{LCS}(\mathcal{A}_s,\mathcal{A}_t)\right|}{|\mathcal{A}_s|+|\mathcal{A}_t|}
$$

**符号说明**

- $R_{\mathrm{reason}}$：学生与教师推理轨迹的过程对齐奖励，取值范围为零到一。
- $\mathcal{A}_s$：从学生推理文本中抽取的有序符号锚点序列。
- $\mathcal{A}_t$：从教师推理轨迹中抽取的有序符号锚点序列。
- $\operatorname{LCS}(\mathcal{A}_s,\mathcal{A}_t)$：两条符号轨迹的最长公共子序列，即保持各自原有顺序的最长共同锚点序列。
- $|\cdot|$：序列长度。

<div class="equation-explanation" markdown="1">

**直观理解**：该式等价于对“学生锚点中有多少得到匹配”和“教师里程碑中有多少被覆盖”取调和平均。分母同时包含两条轨迹的长度，因此重复堆砌锚点或只复现教师路线的短前缀都无法获得满分。<br>
**原文位置**：第3.3节，公式(5)

</div>

</div>

<div class="equation-block" markdown="1">

#### 格式门控的SPEAR总奖励

$$
R_{\mathrm{spear}}=\mathbb{I}_{\mathrm{fmt}}\left(R_{\mathrm{acc}}+\lambda R_{\mathrm{reason}}\right)
$$

**符号说明**

- $R_{\mathrm{spear}}$：提供给强化学习优化器的最终复合奖励。
- $\mathbb{I}_{\mathrm{fmt}}$：格式合规指示量；输出具有合法的思考与答案区块时为一，否则为零。
- $R_{\mathrm{acc}}$：学生最终答案相对于标准答案的正确性奖励。
- $R_{\mathrm{reason}}$：由LCS-F1得到的过程对齐奖励。
- $\lambda$：过程奖励权重，主实验设置为零点五。

<div class="equation-explanation" markdown="1">

**直观理解**：格式门先决定该响应是否有资格得分，再把终局正确性与过程质量相加。即使答案错误，只要格式有效且推理覆盖了部分正确里程碑，模型仍可能获得过程反馈，从而缓解纯二值结果奖励过于稀疏的问题。<br>
**原文位置**：第3.4节，公式(7)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：SPEAR本身不是新的策略优化器，而是可插入现有在线强化学习框架的奖励函数。论文以GRPO类裁剪目标为例：学生从旧策略$\pi_{\theta_{\mathrm{old}}}$对每个问题$q$在线采样回答$o$，由$R_{spear}$形成组相对优势$\hat{A}$，再根据新旧策略概率比更新参数$\theta$；裁剪操作限制概率比落在由$\epsilon$控制的邻域内，以避免单次策略更新过大。与监督微调直接最大化教师文本似然不同，该目标只要求学生探索得到高正确性和高符号顺序一致性的轨迹，因此允许其使用不同于教师的自然语言表达。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 领域自适应符号锚点投影**

投影$\Phi:\mathcal{Y}\rightarrow\mathcal{A}$将高维自然语言推理映射为低维符号轨迹。数学投影以正则表达式提取LaTeX公式和显式变量赋值，并排除孤立数字；科学投影利用依存分析形成“动词词元—宾语”或“主语—动词词元”关系元组并去重；常识投影将名词短语中心词与其支配动词词元配对，若支配项不是动词则仅保留名词中心词。

> 直观理解：不同领域的“关键一步”形式不同，因此不能统一按词语重合打分。该模块舍弃修饰语、时态和表面措辞，尽量只留下公式状态、因果关系或世界状态变化。

**2. LCS-F1顺序对齐器**

对$\mathcal{A}_s$和$\mathcal{A}_t$求最长公共子序列，并以其长度同时归一化到学生和教师轨迹长度。该分数具有顺序敏感性：颠倒里程碑不会被视为完整匹配；学生加入无关或重复锚点会降低精确性，遗漏教师锚点则会降低召回性。

> 直观理解：它类似比较两份步骤清单时寻找最长的同序共同步骤，而非只检查两份清单是否出现过相同词语。这样可以区分“先代入再求变量”和“先求变量再代入”等逻辑次序。

**3. 格式门控的复合奖励**

总奖励由二值格式门$\mathbb{I}_{fmt}$、终局正确性$R_{acc}$和过程对齐$R_{reason}\in[0,1]$组成。格式不合法时奖励归零；轨迹无法抽取时退化为仅使用$R_{acc}$，其余情况下过程奖励以权重$\lambda$加入。

> 直观理解：单靠最终答案只能告诉模型“成或败”，早期训练中容易出现大量同为零分的样本。过程项为部分正确的路线提供梯度，同时格式门保证这些反馈建立在可解析输出之上。

**训练与推理**

训练时，首先用DeepSeek-V3.2为训练问题生成固定教师推理轨迹；每轮强化学习由学生模型在线生成多个候选回答。对每个候选，算法依次执行标签解析、格式检查、答案验证、按任务类型抽取学生与教师锚点、计算LCS-F1和复合奖励，再由GRPO、Dr. GRPO或DAPO完成策略更新；若格式无效则奖励为零，若任一锚点序列为空则只采用答案奖励。符号抽取和LCS匹配均不训练额外神经网络。

**复现信息**

主实验使用DeepSeek-V3.2作为教师，Llama-3-8B-Instruct和Qwen3-4B作为学生；依存锚点通过spaCy的`en_core_web_sm`抽取，数学锚点通过正则表达式抽取。过程奖励权重设为$\lambda=0.5$；训练基于Hugging Face TRL、BF16与LoRA，在四张Nvidia A100-80GB GPU上进行，RL训练为一个epoch、学习率为$1\times10^{-5}$、每个问题生成四个候选、最大生成长度为$2048$。奖励侧的spaCy抽取与LCS-F1在CPU执行，不需要额外神经奖励模型或GPU奖励前向传播；这些设置对于理解其相对神经过程奖励模型的计算优势是必要的。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学推理基准包括GSM8K与MATH。GSM8K按官方划分使用7473个训练样本和1319个测试样本；MATH使用官方训练集中的7500个样本训练，并以覆盖面较高、评测成本较低的MATH-500作为500题测试集。二者用于检验SPEAR对多步算术和竞赛数学推理的作用。
- GPQA用于科学推理评测。由于该数据集没有官方训练/测试划分，作者将$\mathrm{gpqa\_main}$与$\mathrm{gpqa\_extended}$合并为994个训练样本，以198题的$\mathrm{gpqa\_diamond}$作为测试集，用于考察方法在高难度科学知识与推理问题上的效果。
- CommonsenseQA用于常识推理，包含9740个训练样本和1220个测试样本；附录F还使用AlpacaEval 2.0进行跨基准迁移测试。前者检验开放域状态转移提取器在常识选择题上的作用，后者检验同一提取器能否迁移到更开放的指令跟随场景。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**长度控制胜率（LC Win Rate）**

AlpacaEval 2.0的官方指标，在比较模型回答偏好时控制回答长度的影响，用于衡量开放式指令跟随质量。该指标可减少模型仅凭更长回答获得偏好优势的偏差。 （越高越好，因为更高数值表示在控制长度因素后，模型回答更常被评为优于对照回答。）

</div>
<div class="metric-item" markdown="1">

**LCS精确率与教师里程碑召回率**

LCS精确率为学生符号锚点序列中按顺序匹配教师轨迹的比例，用于惩罚无依据或重复锚点；教师里程碑召回率为教师锚点中被学生轨迹按顺序覆盖的比例，用于惩罚遗漏关键步骤。 （两者均越高越好，但单独最大化任一指标都可能产生退化策略：精确率偏好过短的匹配前缀，召回率则可能容忍夹杂大量无依据步骤的冗长轨迹。）

</div>
<div class="metric-item" markdown="1">

**LCS-F1**

LCS精确率与教师里程碑召回率的调和平均，用于同时衡量学生推理是否完整覆盖教师里程碑、是否保持正确顺序，以及是否避免多余的无依据锚点。 （越高越好；只有学生轨迹完整、简洁且顺序一致时才能取得满分。不过，它仍可能低估与教师参考路径不同但实际正确的替代推理。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-4B在AlpacaEval 2.0上采用GRPO优化

<div class="result-value" markdown="1">

GRPO + SPEAR的LC胜率为56.02%，相较原始GRPO提高1.61个百分点；同时高于GRPO + Logic-RL的54.78%。

</div>

作者据此主张SPEAR的开放域符号过程奖励可以改善GRPO训练后的指令跟随表现。分析上，这一对照支持收益来自奖励设计而非仅来自启用GRPO；但单一模型和单一开放式基准的结果不能证明其对所有模型或任务都有效。

<div class="result-source" markdown="1">

来源：附录F，表10

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 10, SPEAR improves the corresponding GRPO, Dr. GRPO, and DAPO baselines by 1.61%, 1.12%, and 1.74%, respectively, and also outperforms the Logic-RL reward under each optimization framework.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-4B在AlpacaEval 2.0上采用Dr. GRPO优化

<div class="result-value" markdown="1">

Dr. GRPO + SPEAR的LC胜率为55.78%，相较Dr. GRPO的54.66%提高1.12个百分点，并高于Dr. GRPO + Logic-RL的54.53%。

</div>

该结果表明SPEAR的增益并不局限于标准GRPO；尤其是Logic-RL在这一设置下未超过原始Dr. GRPO，而SPEAR仍有提升。不过，节选没有给出误差区间或显著性检验，因此1.12个百分点是否稳定仍需重复实验确认。

<div class="result-source" markdown="1">

来源：附录F，表10

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 10, SPEAR improves the corresponding GRPO, Dr. GRPO, and DAPO baselines by 1.61%, 1.12%, and 1.74%, respectively, and also outperforms the Logic-RL reward under each optimization framework.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen3-4B在AlpacaEval 2.0上采用DAPO优化

<div class="result-value" markdown="1">

DAPO + SPEAR取得57.64%的LC胜率，相较DAPO的55.90%提高1.74个百分点，也超过DAPO + Logic-RL的56.27%；这是表10中最高的报告结果。

</div>

三种优化器中DAPO设置的绝对成绩和相对提升均最大，支持SPEAR作为可插拔奖励的主张。由于实验直接复用了常识状态转移提取器，这也构成跨基准迁移证据；但它只能说明该提取器在AlpacaEval 2.0上具有一定复用价值，不能证明提取出的符号必然对应真实或唯一的推理过程。

<div class="result-source" markdown="1">

来源：附录F，表10

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 10, SPEAR improves the corresponding GRPO, Dr. GRPO, and DAPO baselines by 1.61%, 1.12%, and 1.74%, respectively, and also outperforms the Logic-RL reward under each optimization framework.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- SPEAR以单条教师轨迹作为参考，而教师并未穷举所有正确解法。因此，与教师符号里程碑不同但逻辑正确的替代路径可能被低估；这属于基于参考轨迹对齐的结构性限制。
- 所给实验节选没有报告主要数学、科学和常识基准上的具体结果表，也没有给出多次运行方差、置信区间或显著性检验。因而可核验的定量结论主要来自AlpacaEval 2.0，尚不足以独立确认摘要所称的全部跨领域优势。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- GRPO：一种组相对策略优化框架，是SPEAR所附加的基础强化学习优化器之一；比较GRPO与GRPO + SPEAR可判断收益是否来自新增的过程奖励。
- Dr. GRPO：GRPO的修正变体。将SPEAR接入该框架，可检验方法是否依赖单一策略优化算法。
- DAPO：另一种用于推理模型训练的策略优化框架。跨GRPO、Dr. GRPO和DAPO的一致改进用于测试SPEAR的即插即用性。
- Logic-RL奖励：与SPEAR相竞争的奖励设计。相同优化框架下比较Logic-RL与SPEAR，可以较直接地隔离奖励信号设计的差异，而不是把结果归因于优化器不同。

**实验想回答的问题**

- SPEAR提供的顺序感知符号过程奖励，能否在数学、科学与常识推理任务中，为不同强化学习优化框架提供比纯结果奖励或Logic-RL更有效的训练信号？
- 面向常识任务设计的开放域状态转移提取器，能否在不修改提取规则的情况下迁移到开放式指令跟随任务，而非仅适配原有推理基准？

**实验实现**

核心实验覆盖数学、科学和常识推理，并把SPEAR分别接入GRPO、Dr. GRPO与DAPO，以测试其对优化器的兼容性。附录F进一步在Qwen3-4B上使用AlpacaEval 2.0官方长度控制胜率，并保持CommonsenseQA所用的开放域状态转移提取器不变。所给节选未提供随机种子、重复运行次数、方差、显著性检验、训练步数或主要推理基准的具体评分协议，因此不能据此判断结果的统计稳定性。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 仅保留LCS精确率所诱导的短前缀策略 | 当教师轨迹为$[a_1,a_2,a_3]$、学生只输出$[a_1]$时，精确率达到1.00，但召回率仅为0.33，LCS-F1降至0.50。 | 这不是一次训练级消融，而是指标行为诊断。它隔离出“只奖励精确率”的缺陷：学生只复现一个正确开头便可获得满精确率，却没有完成教师推理。LCS-F1通过引入召回率把该不完整轨迹降分，从而减少模型投机地输出短匹配前缀的可能。 | 附录D，表9<br><span class="experiment-evidence">[a₁] \| 1 \| 1.00 \| 0.33 \| 0.50</span> |
| 仅保留教师里程碑召回率所诱导的冗长策略 | 学生轨迹$[a_1,x,a_2,y,a_3,z]$覆盖全部教师里程碑，因此召回率为1.00；但其精确率仅为0.50，LCS-F1为0.67。 | 该诊断隔离出“只奖励召回率”的缺陷：轨迹即使加入$x$、$y$、$z$等无依据锚点，只要包含全部教师节点仍可取得满召回率。LCS-F1利用精确率惩罚这些额外步骤，但该示例本身不等价于证明训练时一定减少幻觉或错误推理。 | 附录D，表9<br><span class="experiment-evidence">[a₁, x, a₂, y, a₃, z] \| 6 \| 0.50 \| 1.00 \| 0.67</span> |

**定性案例**

- 表9的符号轨迹示例说明，完整且简洁的学生序列$[a_1,a_2,a_3]$在精确率、召回率和LCS-F1上均为1.00；不完整前缀或夹杂无依据锚点的轨迹会被LCS-F1降分。该案例直观展示了奖励函数希望学生“按顺序覆盖关键步骤且不过度扩写”，但它是人工构造的指标示例，并非真实问题上的定性推理案例。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出以符号化推理里程碑和序列对齐生成稠密过程奖励的方法，用于强化学习式推理蒸馏与后训练。; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`ba0334d310e047146e461a72cd6255f8d971d922e2e473ac2375f95e3a400638`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
