---
title: "[论文解读] Rethinking LLM Verification: Evidence Structure, Uncertainty, and Selective Refinement"
description: "[arXiv 2608.10725][LLM Reasoning] 本文将大模型的弃答视为可利用的不确定性信号，仅对弃答的医学假设引入SNOMED CT本体知识进行二次核验，以兼顾回答覆盖率、准确性与推理成本。"
arxiv_id: "2608.10725"
announcement_date: "2026-08-12"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:07:35.118392+00:00"
source_sha256: "d89ef7b503274891040e1ef23c1502af0ae3a4f2579bfeb5b18946162b4fc8e8"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "医疗推理"
  - "不确定性估计"
  - "弃答"
  - "医学假设验证"
  - "本体 grounding"
  - "SNOMED CT"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.10725</p>

# Rethinking LLM Verification: Evidence Structure, Uncertainty, and Selective Refinement

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Uma Ranjan, Kunal Tilaganji, Aditya Koul, Anurag Mahipal, Dashpreet Singh, Hriday Rana, Manan Jain, Sidharth Gupta, Ajo Babu George, Vineeth Balasubramanian, Nagarajan Natarajan, Amit Sharma</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Indian Institute of Technology Jammu；Microsoft Research；SCB Dental College and Hospital, Cuttack</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.10725v1) · [PDF 下载](https://arxiv.org/pdf/2608.10725v1) · **关键词** 医疗推理, 不确定性估计, 弃答, 医学假设验证, 本体 grounding, SNOMED CT<br>


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

本文将大模型的弃答视为可利用的不确定性信号，仅对弃答的医学假设引入SNOMED CT本体知识进行二次核验，以兼顾回答覆盖率、准确性与推理成本。

**不用术语来说**：在医学选择题或临床决策支持中，大模型即使证据不足也可能自信地给出答案，而错误结论可能带来严重后果。允许模型回答“不确定”可以减少冒险判断，却会留下更多未解决问题；因此，关键困难不是单纯让模型多答或少答，而是识别哪些“不确定”确实值得进一步投入结构化医学知识，并通过有针对性的复核把其中可解决的疑问转化为可靠判断。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者论证弃答并非任意拒绝：在所研究的前沿模型中，标记为$\mathrm{UNKNOWN}$的预测与较低置信度相关，因而可作为触发后续处理的控制信号。
- 作者提出两阶段选择性精炼框架：第一阶段独立核验每个候选假设并允许弃答，第二阶段只对$\mathrm{UNKNOWN}$项进行SNOMED CT本体落地与重新判断，从而避免为每个预测持续调用外部知识；作者进一步声称该方案可接近知识图谱落地方法的表现，但不需要预先构建专用知识图谱。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于面向医疗推理的“大语言模型可靠性”研究。尽管大语言模型在医疗问答基准上表现较强，其推理仍可能受锚定偏差、捷径学习和错误自信影响，因此基准准确率不能直接等同于临床可用性。相关研究通常沿两条路线降低风险：一是允许模型在证据不足时弃答，以减少高置信度错误；二是利用医学知识图谱或本体提供结构化知识依据。本文关注二者的结合：将弃答视为不确定性的控制信号，仅对模型无法判断的候选假设调用 SNOMED CT 医学本体进行定向补充，而不是对所有预测持续检索。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**医学假设验证**

给定一道医学选择题及一个候选选项，模型不直接比较所有选项，而是独立判断该选项所表达的医学命题为真还是为假。逐项验证后，系统再据此确定整道题的答案。

</div>
<div class="concept-item" markdown="1">

**弃答与覆盖率—准确率权衡**

弃答是允许模型在证据不足时输出 UNKNOWN，而不是被迫给出 TRUE 或 FALSE。更频繁地弃答通常能减少错误，却会降低系统实际作答的覆盖范围；弃答过少则可能产生错误但看似确定的结论。

</div>
<div class="concept-item" markdown="1">

**本体 grounding**

本体 grounding 指把题目中的医学概念与标准化医学概念体系及其关系对齐，本文采用 SNOMED CT 提供结构化医学依据。直观上，它让模型在不确定时参考统一的医学术语和概念关系，而不是只依赖参数中记忆的知识。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究设置是多项选择医学问答中的逐候选假设验证：输入为医学问题及其中一个候选选项，验证器独立输出 TRUE、FALSE 或 UNKNOWN，分别表示该候选命题成立、不成立或当前证据不足。第一阶段由大语言模型独立验证；只有输出 UNKNOWN 的候选项进入第二阶段，通过 SNOMED CT 本体 grounding 补充结构化医学证据并重新判断。该设置假定弃答与真实不确定性有关，因此可充当是否启动额外推理的动态信号；最终目标是在避免对每个预测都调用外部知识的同时，提高候选项层面和整题层面的判断可靠性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Su and Wu (2025), MedOnto-RAG**: 该工作将本体 grounding 检索持续集成到医疗问答流程，代表结构化医学知识增强路线。本文与之都利用医学本体，但仅在模型输出 UNKNOWN 时触发 SNOMED CT grounding，研究重点是以弃答控制知识增强的调用范围。
- **Guo and Yan (2026)**: 该工作表明噪声与歧义会降低医疗推理可靠性，而且弃答程度会随任务表述、知识条件和模型架构显著变化。本文进一步检验弃答是否对应较低置信度，并将其由终止性拒绝转化为定向证据增强的触发信号。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

医学推理属于安全关键任务，基准测试上的较高得分并不等同于临床可靠性。原文指出，大模型仍会表现出锚定偏差、依赖推理捷径以及在证据不足时过度自信等问题，甚至已有随机临床试验未观察到大模型决策支持对医生诊断推理的改善。系统因此需要一种机制：既允许模型在不确定时避免强行作答，又不能因频繁弃答而失去实际可用性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **带弃答的选择性预测**：在原有判断之外加入$\mathrm{UNKNOWN}$选项，使模型在证据不足时可以暂不提交$\mathrm{TRUE}$或$\mathrm{FALSE}$结论，以较低覆盖率换取已作答部分更高的可信度。
- **检索增强或知识图谱落地的医学推理**：在推理时持续检索外部医学资料，或把问题映射到经过整理的知识图谱，再依据检索到的概念和关系补充模型自身知识，以约束和支持最终判断。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 弃答机制存在覆盖率与准确性的权衡：弃答过多会使大量问题得不到处理，弃答过少又会制造错误的确定感；更基础的问题是，既有研究尚未充分确定弃答究竟反映真实不确定性，还是模型的任意拒绝，因此不能直接把所有弃答当作可靠安全信号。
- 既有知识增强方法通常采用始终开启的检索，或依赖人工整理、维护的知识图谱。这样会对每个预测引入额外知识获取成本，并要求可用且质量稳定的结构化资源；原文还指出，本体检索效果会随领域和检索质量变化，因而全面依赖外部落地并非总是可行。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种经过验证的选择性机制，将模型自身的弃答行为与后续结构化知识推理连接起来：首先需要判断$\mathrm{UNKNOWN}$是否真的集中于低置信度样本，其次需要确定能否只精炼这些样本，在不为所有预测构建或调用专用知识图谱的情况下，恢复覆盖率并保持较高可靠性。此外，原文强调弃答还受证据表述和落地策略影响，这意味着仅增加一个拒答选项并不足以解决问题。

</div>
<div markdown="1"><span>核心问题</span>

在医学多项选择题中，当每个候选项被独立判为$\mathrm{TRUE}$、$\mathrm{FALSE}$或$\mathrm{UNKNOWN}$时，能否把$\mathrm{UNKNOWN}$验证为真实不确定性的指标，并用它精确触发SNOMED CT本体落地，使二次核验在准确性、覆盖率和外部知识使用成本之间取得更好的平衡？

</div>
<div markdown="1"><span>作者直觉</span>

模型明确弃答相当于指出“自身证据不够”的局部位置，因此无需让所有候选项都经历昂贵的知识增强。框架可以保留第一阶段已经有把握的判断，只把有限资源用于$\mathrm{UNKNOWN}$项；SNOMED CT提供标准化医学概念及其关系，能够为这些模糊项补上更明确的结构化线索。通俗地说，这类似先让模型独立答题，再只查阅术语手册复核它主动圈出的疑难题，而不是从头查证每一道题。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文提出一种“由弃答触发、按需引入本体知识”的两阶段医学假设验证框架。输入是一道多项选择医学问题 $Q$ 及候选项集合 $\mathcal{O}$；模型先基于自身参数知识生成覆盖全部选项、但不直接给出答案的推理轨迹 $R$，再把每个候选项 $O_i$ 当作独立假设，仅依据 $R$ 输出 $\text{TRUE}$、$\text{FALSE}$ 或 $\text{UNKNOWN}$ 及置信度。若没有候选项被判为 $\text{UNKNOWN}$，第一阶段结果直接作为最终输出；若出现弃答，则只为这些不确定选项检索 SNOMED CT 的概念定义与同义词，并用所得本体上下文进行第二阶段复核。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成全选项医学推理轨迹

模型利用参数化医学知识生成逐步推理轨迹 $R$，要求考虑全部选项，但不得选择最终答案。该轨迹并非从外部知识图谱检索，也不是 MedReason 提供的人工验证轨迹。

<div class="method-step__io" markdown="1">

**输入**：问题 $Q$ 与全部候选项集合 $\mathcal{O}$。<br>
**输出**：覆盖问题及全部候选项的自生成结构化推理轨迹 $R$。

</div>

**直观理解**：这一步相当于先写出解题依据，再把“分析过程”和“最终判断”分开，以减少模型看到选项后直接凭表面线索作答的倾向。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 第一阶段独立假设验证

验证器逐项运行 $\mathcal{V}(Q,O_i,R)$，且每次不展示其他候选项，只允许使用 $R$，输出标签 $y_i^{(1)}\in\{\text{TRUE},\text{FALSE},\text{UNKNOWN}\}$ 和置信度 $c_i^{(1)}$。若所有选项均非 $\text{UNKNOWN}$，流程在此结束。

<div class="method-step__io" markdown="1">

**输入**：问题 $Q$、单个候选项 $O_i$ 与固定推理轨迹 $R$。<br>
**输出**：每个候选假设的第一阶段标签与置信度，以及是否触发本体检索的控制信号。

</div>

**直观理解**：把每个选项单独检查，可降低选项之间的相互暗示；$\text{UNKNOWN}$ 不是失败状态，而是告诉系统“这里值得额外查证”的开关。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 面向不确定选项的 SNOMED CT 检索

系统通过 BioPortal API 查询 SNOMED CT，为每个不确定选项检索概念定义和同义词，形成选项相关的本体证据 $E_{\text{SNOMED}}^{(i)}$。确定选项不触发检索，因此外部知识的使用是局部且按需的。

<div class="method-step__io" markdown="1">

**输入**：第一阶段被标为 $\text{UNKNOWN}$ 的候选项及其相关医学概念。<br>
**输出**：仅与初始不确定选项对应的结构化医学概念上下文 $E_{\text{SNOMED}}$。

</div>

**直观理解**：SNOMED CT 可理解为标准化医学术语词典；系统只在模型拿不准时查词，而不是预先为每道题构造完整知识图谱。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 第二阶段本体增强复核

只要任一选项在第一阶段弃答，系统就重新评估整组选项；不确定选项使用 $R\cup E_{\text{SNOMED}}^{(i)}$，其余选项按方法正文的形式仍仅使用 $R$。局部检索与全局复核相结合，使新证据不仅能解除弃答，也可能改变整道题的相对判断。

<div class="method-step__io" markdown="1">

**输入**：问题 $Q$、全部候选项、原推理轨迹 $R$，以及不确定选项对应的 $E_{\text{SNOMED}}^{(i)}$。<br>
**输出**：第二阶段标签 $y_i^{(2)}$、置信度 $c_i^{(2)}$ 及最终题目答案。

</div>

**直观理解**：系统只为疑点补资料，但拿到资料后会重新检查整道题，因为某个选项的新定义也可能间接证明其他选项不成立。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 带置信度的医学假设验证

$$
(y_i,c_i)=\mathcal{V}(Q,O_i,E),\qquad y_i\in\{\mathrm{TRUE},\mathrm{FALSE},\mathrm{UNKNOWN}\},\quad c_i\in[0,1]
$$

**符号说明**

- $\mathcal{V}$：执行候选假设验证的语言模型验证函数。
- $Q$：多项选择医学问题。
- $O_i$：第 i 个候选选项，被视为待验证的医学假设。
- $E$：验证时允许使用的证据；可对应隐式世界知识、知识图谱推理轨迹或本文流水线中的结构化上下文。
- $y_i$：候选假设的判断标签，其中 UNKNOWN 表示根据当前证据无法可靠推断。
- $c_i$：模型对标签 $y_i$ 给出的自报置信度，取值范围为 0 到 1。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把任务从“整道题直接选答案”改写成“逐个核验候选假设”。加入 $\text{UNKNOWN}$ 后，模型可以保留判断，而置信度与弃答共同刻画当前证据是否足以支持结论。<br>
**原文位置**：第 3.1 节 Task formulation

</div>

</div>

<div class="equation-block" markdown="1">

#### 两阶段选择性本体增强验证

$$
(y_i^{(1)},c_i^{(1)})=\mathcal{V}(Q,O_i,R),\qquad (y_i^{(2)},c_i^{(2)})=\mathcal{V}\!\left(Q,O_i,R\cup E_{\mathrm{SNOMED}}^{(i)}\right)
$$

**符号说明**

- $R$：模型在看到问题和全部选项后生成、但不包含最终答案的医学推理轨迹。
- $y_i^{(1)}$：第一阶段仅依据推理轨迹得到的第 i 个选项标签。
- $c_i^{(1)}$：第一阶段标签的自报置信度。
- $E_{\mathrm{SNOMED}}^{(i)}$：针对第 i 个选项检索到的 SNOMED CT 定义与同义词；仅当该选项初始为 UNKNOWN 时非空。
- $y_i^{(2)}$：第二阶段复核后的第 i 个选项标签。
- $c_i^{(2)}$：第二阶段复核标签的自报置信度。
- $\cup$：表示在原推理轨迹上加入可用的 SNOMED CT 上下文，并非严格的数学集合并集运算要求。

<div class="equation-explanation" markdown="1">

**直观理解**：第一式检查自生成推理能否单独支持某一选项；若出现弃答，第二式再为疑点加入标准医学概念证据。核心决策是用 $y_i^{(1)}=\text{UNKNOWN}$ 控制外部检索，而不是对所有样本统一增加检索成本。<br>
**原文位置**：第 3.5 节，公式 (1) 与公式 (2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文没有训练、微调或参数更新过程，也未定义需要梯度优化的损失函数；GPT-5.5 与 DeepSeek-R1 均作为现成模型通过 API 调用。这里的“优化”发生在推理流程层面：利用第一阶段的 $\text{UNKNOWN}$ 选择需要 SNOMED CT 补证的案例，在准确率、覆盖率与外部检索成本之间进行控制，而非学习一个新的模型目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 带弃答能力的假设验证器**

验证器将经典二元判定扩展为三元决策空间 $\{\text{TRUE},\text{FALSE},\text{UNKNOWN}\}$，并为每个候选项返回自报置信度。第一阶段要求逐项、隔离验证，且外部医学知识被明确禁止，使判断可追溯到统一的推理轨迹 $R$。

> 直观理解：该模块的关键不是强迫模型回答，而是允许它明确承认现有证据不足；弃答由此成为资源分配信号，用于决定哪些案例需要额外知识。

**2. 自生成推理轨迹**

模型先观察问题和全部选项，生成不含最终答案的逐步医学推理 $R$；随后验证器把 $R$ 当作完整证据，而不是直接调用未显式化的参数知识。它构成一种内部证据结构化机制，但不能保证事实正确，因为轨迹仍由同一类语言模型生成。

> 直观理解：先把依据写出来，可以让后续判断围绕同一份材料进行；但这份材料可能带有模型原有错误，所以仍需要不确定性检测和外部补证。

**3. 选择性 SNOMED CT 本体接地**

当且仅当第一阶段出现 $\text{UNKNOWN}$ 时，系统才通过 BioPortal 检索 SNOMED CT 的标准概念定义和同义词。检索对象局限于不确定选项，而第二阶段对整组选项复核，从而避免为所有问题预建医学知识图谱或无差别注入外部上下文。

> 直观理解：这一设计把有限的检索成本集中到真正困难的地方，并用标准医学术语减少名称歧义；它主要补充概念性知识，不能天然覆盖缺失图像或治疗指南等信息。

**训练与推理**

完整流程属于零训练推理。对每道题，系统首先用固定提示让模型读取 $Q$ 和 $\mathcal{O}$，输出 JSON 格式的推理轨迹 $R$；随后逐个输入 $Q$、$O_i$ 与 $R$，要求验证器仅依据轨迹产生三元标签和概率。若全部候选项均得到确定标签，则返回第一阶段结果；若至少一个候选项为 $\text{UNKNOWN}$，系统只为这些选项检索 SNOMED CT，并触发第二阶段整题复核，最终输出各选项标签与置信度。论文使用单次推理，即 $k=1$，没有自一致性采样、多数投票或多随机种子重复实验。

**复现信息**

实验调用 Azure OpenAI API 上的 GPT-5.5 和 DeepSeek API 上的 DeepSeek-R1；提示在模型与数据集之间固定，输出约束为可解析的 JSON，默认温度为 $0.1$。SNOMED CT 经 BioPortal API 访问，其定义和同义词仅为第一阶段标记为 $\text{UNKNOWN}$ 的选项检索；MedReason 与 MedQA 各随机抽取 $1000$ 道题，分别形成 $3996$ 和 $4000$ 个候选假设，且不使用训练数据。需要源文复核的一点是：第 3.5 节称每个选项在复核中始终隔离评估，而附录 B.4 的提示模板却要求同时输入全部选项并“Compare all options before deciding”；因此，第二阶段究竟是逐项隔离调用还是一次联合调用，所给文本存在实现描述不一致。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MedReason：医学推理数据集，用于比较世界知识、知识图谱证据、自生成推理轨迹及本体约束重新验证。原文节选未明确报告数据规模、训练/验证/测试划分；消融实验只说明从中使用了 $n=100$ 道题。
- MedQA：医学多项选择问答数据集，用于检验两阶段方法和置信度规律能否迁移到另一医学任务。原文节选未明确报告数据规模及数据划分。
- MedReason 的 100 题消融子集：仅用于 GPT-5.5 的重新评估消融，以区分性能变化来自再次调用模型，还是来自 SNOMED 本体信息。该子集的抽样方式与代表性原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy（Acc）**

全部预测上的准确率；在允许 UNKNOWN 时，弃答不能被视为正确，因此该指标同时反映判断质量与弃答造成的覆盖损失。 （越高越好，因为表示在全部待验证假设中最终判断正确的比例更高。）

</div>
<div class="metric-item" markdown="1">

**Conditional Accuracy（Cond. Acc）**

仅在非 UNKNOWN 预测上计算的准确率，用于衡量模型决定作答时有多可靠；必须结合 Coverage 阅读，否则模型可能通过大量弃答人为抬高该值。 （在覆盖率相近时越高越好；若覆盖率显著下降，单独升高不能证明系统整体更有效。）

</div>
<div class="metric-item" markdown="1">

**Coverage（Cov）**

非 UNKNOWN 预测占全部预测的比例，即系统实际给出 T/F 判断的范围。ROC-AUC 与 ECE 仅在置信度分析中补充报告，但为遵守指标数量限制未单列。 （在准确率和风险可接受的前提下越高越好；覆盖率本身不是单调质量指标，因为强制作答可获得高覆盖率却增加错误。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### MedReason、GPT-5.5：从隐式世界知识基线到两阶段选择性细化

<div class="result-value" markdown="1">

Imp 的准确率为 $87.8\%$；Self 将其提高到 $92.0\%$，增幅为 $4.2$ 个百分点，95% 置信区间为 $[+3.3,+5.1]$；Ont 再提高到 $96.2\%$，相对 Self 增加 $4.2$ 个百分点，95% 置信区间为 $[+3.5,+4.9]$。最终覆盖率为 $99.5\%$，高于 Self 的 $97.6\%$，说明第二阶段不仅纠正部分判断，也解决了多数第一阶段弃答案例。

</div>

作者结果表明，在该模型和数据集上，显式自生成推理与针对弃答样本的本体约束重新验证各自贡献了相近的绝对准确率提升。分析上，这支持“只细化不确定案例”可以兼顾准确率与覆盖率；但单次确定性实验不能说明收益对提示词、采样随机性或其他医学数据分布同样稳定。

<div class="result-source" markdown="1">

来源：表 2，MedReason / GPT-5.5 行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MedReason | GPT-5.5 | Imp (baseline) | 87.8 | 89.7 | 97.9 | — | — | —; Self | 92.0 | 94.2 | 97.6 | +4.2 | [+3.3, +5.1] | <10^-10; Ont | 96.2 | 96.6 | 99.5 | +4.2 | [+3.5, +4.9] | <10^-10; KG-Trace | 92.9 | 96.0 | 96.8 | — | — | —

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨模型、跨数据集的两阶段不确定性细化

<div class="result-value" markdown="1">

DeepSeek-R1 在 MedReason 上由 Imp 的 $84.3\%$ 经 Self 的 $91.1\%$ 提升至 Ont 的 $93.4\%$；在 MedQA 上由 $86.9\%$ 经 $94.2\%$ 提升至 $96.0\%$。GPT-5.5 在 MedQA 上则由 $95.1\%$ 经 $97.4\%$ 提升至 $98.4\%$。各处 Ont 相对 Self 的增幅为 $1.1$ 至 $2.3$ 个百分点，且表中 McNemar 检验均达到统计显著。

</div>

作者结果显示，两阶段收益并非只出现在 GPT-5.5 的 MedReason 设置中：较弱起点的 DeepSeek-R1 在 Self 阶段获得更大提升，而 Ont 阶段仍提供额外增益。分析上，这说明本体细化具有一定跨模型和跨数据集一致性，但只有两个模型和两个数据集，尚不足以推出对所有医学任务或非医学领域都有效。

<div class="result-source" markdown="1">

来源：表 2；同表的 MedReason / DeepSeek-R1、MedQA / GPT-5.5 与 MedQA / DeepSeek-R1 行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MedQA | DeepSeek-R1 | Imp | 86.9 | 86.9 | 100.0 | — | — | —; Self | 94.2 | 94.6 | 99.6 | +7.3 | [+6.1, +8.5] | <10^-10; Ont | 96.0 | 96.0 | 100.0 | +1.8 | [+1.3, +2.2] | <10^-10

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MedReason 世界知识条件下的置信度校准与错误判别

<div class="result-value" markdown="1">

GPT-5.5 的置信度预期校准误差 ECE 为 $0.085$，区分正确与错误预测的 ROC-AUC 为 $0.69$。这表示置信度并非严格校准，但仍提供高于随机排序的错误判别能力；附录还报告 DeepSeek-R1、推理轨迹和 MedQA 条件下均呈现“正确预测置信度更高、UNKNOWN 更集中于低置信区间”的定性趋势。

</div>

作者据此把置信度和 UNKNOWN 解释为可用于触发第二阶段的真实不确定性信号。分析上，$0.69$ 的 AUC 只说明排序具有一定信息量，并不等于置信度概率准确，也不直接证明某个具体触发阈值在临床风险下最优。

<div class="result-source" markdown="1">

来源：图 2及第 4.2 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Left: reliability diagram showing deviation from perfect calibration (ECE = 0.085). Right: ROC curve (AUC = 0.69) indicating that confidence retains meaningful discriminative ability in distinguishing correct from incorrect predictions.

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

- Imp（implicit/world knowledge）：模型主要依赖参数化世界知识直接判断，并允许输出 T/F/U；它衡量不提供显式推理证据时的起点性能。
- T/F forced binary：强制模型在真与假之间选择，不允许 UNKNOWN；与 T/F/U 对比可直接观察弃答对总体准确率、条件准确率和覆盖率的影响。
- Self（Stage 1）：模型先生成自己的推理轨迹，再据此验证选项；它用于判断显式展开推理本身能带来多少收益。
- KG-Trace：使用知识图谱支持的推理轨迹进行验证；它是结构化证据条件下的参照，用于判断选择性本体细化能否达到类似效果，而无需显式构造完整知识图谱。

**实验想回答的问题**

- 允许模型输出 UNKNOWN 后，弃答是否集中在真正不确定的样本上，并形成可解释的覆盖率—准确率权衡，而不是随机拒答？
- 把弃答作为控制信号，仅对不确定假设依次进行自生成推理和 SNOMED 本体约束的重新验证，能否在不同模型与数据集上稳定提升准确率，并接近或超过完整知识图谱推理轨迹的效果？

**实验实现**

实验在 GPT-5.5（通过 Azure OpenAI API）和 DeepSeek-R1 上进行。核心验证采用 $k=1$：每个假设只运行一条独立生成的推理轨迹，不使用自洽采样或多数投票。两阶段流程先以 Self 生成并验证推理；若模型输出 UNKNOWN，再以 SNOMED 本体证据进行 Ont 重新验证。表 2 的结果来自单次确定性运行，95% 置信区间表示配对评估的不确定性而非随机种子方差，阶段差异使用带连续性校正的 McNemar 检验。原文节选未报告提示词、解码参数、具体置信度阈值及数据划分。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| GPT-5.5 在 MedReason 的 $100$ 题子集上：无 SNOMED 的普通重新评估 | Self 准确率为 $91.8\%$，仅再次评估而不加入 SNOMED 后为 $92.0\%$，提升 $0.2$ 个百分点；95% 置信区间为 $[-0.2,+0.7]$，结果不显著。 | 该消融试图区分“再次调用模型”与“加入本体证据”两种因素。几乎为零且不显著的变化说明，主实验中 Ont 的提升不太可能仅由第二次推理机会造成，更可能依赖 SNOMED 提供的结构化医学约束。不过该结论只基于 $100$ 题、单一模型，统计功效和外部有效性有限。 | 表 2标题说明及 Ablation（GPT-5.5, MedR, $n=100q$）行<br><span class="experiment-evidence">Ablation (Reeval) shows re-evaluation without SNOMED on 100 MedReason questions (GPT-5.5) — not significant (n.s.).</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Uses uncertainty-driven abstention and selective ontology grounding to refine LLM verification and reasoning on medical questions.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`d89ef7b503274891040e1ef23c1502af0ae3a4f2579bfeb5b18946162b4fc8e8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
