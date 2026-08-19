---
title: "[论文解读] CEDAR-GRPO: Process-Aware Reinforcement Learning for General Abductive Reasoning in LLMs"
description: "[arXiv 2608.14791][LLM Reasoning] 本文研究如何通过兼顾答案正确性与推理过程质量的强化学习后训练，使大语言模型学到可跨任务迁移的溯因推理能力，而非仅适应某个特定基准。"
arxiv_id: "2608.14791"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:16:49.465597+00:00"
source_sha256: "ea213b1c96c1f51c21024c7a6c706f527691e68795b3dc82cfcb0a7b2cd0ebe8"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "归纳推理"
  - "大型语言模型"
  - "强化学习后训练"
  - "GRPO"
  - "过程感知奖励"
  - "跨任务迁移"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.14791</p>

# CEDAR-GRPO: Process-Aware Reinforcement Learning for General Abductive Reasoning in LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Moein Salimi, Danial Parnian, Shaygan Adim, Amirmohammad Ebrahiminasab, Nima Alighardashi, Parsa Gholami, Sahand Akramipour, Mahdi Jafari Siavoshani, Mohammad Hossein Rohban</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Sharif University of Technology；University of Tehran</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14791) · [PDF 下载](https://arxiv.org/pdf/2608.14791) · **关键词** 归纳推理, 大型语言模型, 强化学习后训练, GRPO, 过程感知奖励, 跨任务迁移<br>
**代码**: [https://github.com/cedar-grpo/cedar-grpo](https://github.com/cedar-grpo/cedar-grpo)

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

本文研究如何通过兼顾答案正确性与推理过程质量的强化学习后训练，使大语言模型学到可跨任务迁移的溯因推理能力，而非仅适应某个特定基准。

**不用术语来说**：许多现实任务都要求模型根据不完整线索反推出最合理的隐藏原因，例如医生从症状推测疾病、工程师从故障现象定位原因，或程序员从报错寻找缺失条件。然而，一个模型在某套固定题型上答得更准，并不意味着它真正掌握了这种“由结果追溯解释”的能力；它可能只是记住了题型规律，甚至通过添加缺乏证据的假设凑出答案。因此，关键问题是如何训练模型，使其既给出正确结论，又能覆盖已有证据、比较竞争解释，并保持从观察到解释的合理推断方向。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 CEDAR-GRPO，在答案正确性奖励之外加入证据覆盖与“证据到解释”方向性奖励，用过程信号约束模型生成能够解释观察、且不过度依赖无依据假设的推理。
- 建立受控的跨任务迁移研究设置：使用兼含假设生成与假设选择的领域中立训练混合，并在四个开放权重模型和十一项未见任务上检验迁移，同时借助过程指标与消融实验区分强化学习、奖励设计和训练任务多样性的作用。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

归纳推理（abductive reasoning）是从不完整、分散或不确定的观察出发，寻找能够最好解释这些证据的隐藏原因、缺失事实或假设。本文关注大型语言模型（LLM）是否能通过强化学习后训练，将这种能力从训练任务迁移到未见过的任务，而不是只在某一个固定基准或输出格式上取得更高分。研究覆盖假设选择、缺失事实生成、可撤销推理、长文本调查、临床推理和代码调试等场景，并同时设置非归纳推理任务作为控制。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**归纳推理（abduction）**

给定观察结果，模型需要反向提出一个最能解释这些结果的假设。例如，看到某人注视喷泉后愉快离开，比起无依据地假设他看到了倒映的流星，更应考虑“他向喷泉投入硬币并许愿”。

</div>
<div class="concept-item" markdown="1">

**假设生成与假设选择**

假设生成要求模型直接提出能够解释观察的答案；假设选择则要求模型在多个候选解释中选出最佳者。两者分别检验模型能否构造解释，以及能否比较解释与证据之间的匹配程度。

</div>
<div class="concept-item" markdown="1">

**GRPO与过程感知奖励**

GRPO（Group Relative Policy Optimization）是一种通过比较同一输入下多个输出的相对奖励来更新语言模型的强化学习方法。过程感知奖励除了检查最终答案是否正确，还检查推理是否覆盖观察证据，以及是否保持“由证据推向解释”的方向。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文将归纳推理建模为从观察证据和任务指令到解释性输出的映射。输入可以是自然语言观察、前提、候选假设、规则或长文档；输出可以是候选标签、缺失事实、解释性假设或经过规定格式包装的答案。训练阶段使用知识量较少、与具体领域无关的混合任务，包含假设生成和假设选择；模型通过可验证的最终答案正确性，以及证据覆盖和证据到解释方向性奖励进行后训练。评估阶段使用训练中未出现的任务和数据集，以检验能力是否跨任务格式、领域和推理类型迁移；同时以基础模型和仅使用正确性奖励的GRPO作为比较对象。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入实例，例如观察证据、任务提示、候选假设或规则。

</div>
<div class="notation-item" markdown="1">

**$h$**

模型生成或评估的解释性假设，即对观察结果的潜在原因、缺失事实或机制的说明。

</div>
<div class="notation-item" markdown="1">

**$r$**

强化学习奖励，用于评价模型输出；本文的奖励由最终答案正确性、证据覆盖和证据到解释方向性等部分组成。

</div>
<div class="notation-item" markdown="1">

**$\pi_\theta(y\mid x)$**

参数为$\theta$的语言模型策略，在输入$x$下生成输出$y$的概率分布。

</div>

</div>

**直接相关的工作**

- **ART**: ART是 commonsense hypothesis selection 基准，要求模型根据观察在候选解释中选择更合理者。本文将其作为归纳推理示例和评估对象之一，同时指出仅在单一基准家族上的提升不足以证明可迁移的归纳能力。
- **ProofWriter与AbductionRules**: 这类数据集研究根据规则和观察生成能够补足推理链的缺失事实，代表假设生成形式的归纳任务。本文在训练混合数据中纳入缺失事实生成，并在未见任务上测试模型能否把这种能力迁移到其他领域和任务格式。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

临床诊断、科学假设形成、证据解释、代码调试和长上下文调查都需要从零散且不完整的观察中推断潜在原因。此类任务通常存在多个看似合理的解释，模型不仅要输出一个候选答案，还要判断哪些解释真正覆盖现有证据、哪些依赖额外假设，以及新证据是否足以排除竞争解释；因此，稳定而可迁移的溯因推理直接关系到大语言模型在不确定环境中的可靠性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **任务或基准特定的溯因建模**：既有研究通常围绕单一任务族训练或评估模型，例如在 ART、e-CARE 中从候选项选择最佳解释，在 ProofWriter、AbductionRules 中生成缺失事实，或在知识图谱中寻找能够解释关系结构的假设。这些方法可以衡量模型对特定输入输出格式和领域规则的适应程度。
- **仅以最终答案正确性为目标的 GRPO 后训练**：该类方法使用精确匹配、标签匹配或执行结果等可验证信号奖励最终答案，并通过组相对策略优化更新模型。它能够直接提高任务得分，但奖励通常不检查中间解释是否覆盖观察，也不检查模型是否按照从证据推向隐藏原因的溯因方向进行推断。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单一基准族、任务格式或结构化领域内的提升难以区分“掌握了可复用的溯因能力”与“适应了训练题型”；尤其是假设生成和假设选择具有不同输出结构，只在其中一种形式上有效不能证明能力能够跨形式迁移。
- 只奖励最终正确答案会留下过程层面的欠约束：模型可能忽略部分证据、编造未经观察支持的前提，或先假定结论再反向拼接理由。原文图 1 的示例中，correctness-only GRPO 为“喷泉中看到流星倒影”添加了额外设定并选错答案，说明单一结果信号不足以稳定引导证据约束下的解释。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有工作尚未在受控设置中证明：仅用规模较小、领域中立且知识需求较低的训练数据进行后训练，能否同时跨越假设生成与假设选择两种形式，并迁移到未见的临床推理、代码调试、长上下文调查等领域；同时也缺少证据表明，任务得分提升确实伴随替代假设探索、竞争解释排除、回溯和不确定性标记等溯因行为变化，而不只是输出格式或领域知识适配。

</div>
<div markdown="1"><span>核心问题</span>

在最终答案正确性之外显式奖励证据覆盖和证据到解释的方向性，能否使四个开放权重大语言模型通过 GRPO 后训练获得可跨未见任务与领域迁移的溯因推理能力，并且优于基础模型及仅奖励正确性的 Cor-GRPO？

</div>
<div markdown="1"><span>作者直觉</span>

一个好的溯因解释不仅应当碰巧得到正确答案，还应尽可能解释全部观察，并让推断从已知证据指向潜在原因。证据覆盖奖励促使模型逐项核对线索，方向性奖励则抑制先假定结论、再补造证据的推理；再将假设生成与假设选择共同纳入训练，模型更可能学习两类任务共享的“比较解释与证据支持关系”，而不是记忆某一种答案模板。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CEDAR-GRPO把一般溯因推理表述为：给定不完整观察或证据，从可能原因、缺失事实或潜在变换规则中选择或生成最能解释观察的答案。模型接收用户提示$x$，输出结构化文本，其中$b2(y)$是位于`<think>`标签内的推理轨迹，$b1(y)$是位于`<answer>`标签内的最终答案；训练时，最终答案由数据集专用验证器判断是否正确，推理轨迹则由外部评判模型检查是否覆盖关键证据，以及推理方向是否确实从证据走向解释。三个信号等权平均成奖励$R(x,y,g,d)$，再用于GRPO强化学习更新模型。

该方法的关键不是单纯要求“答对”，而是把溯因过程中的两个结构性要求加入优化：一是候选解释应说明尽可能多的已知细节，二是模型不能先假定答案成立再反向拼接证据。训练数据同时包含假设生成型来源和假设选择或评价型来源，使模型学习从开放地产生解释到比较候选解释的完整能力。通俗地说，系统不仅给最终答案打分，还检查模型有没有把题目中的线索逐项解释清楚，以及论证是否按“看到线索，再推出原因”的顺序展开。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造一般溯因训练实例

将任务统一为依据不完整观察生成或选择最佳解释；训练池覆盖假设生成和假设选择或评价两类任务。前者包括AbductionRules、Crypto和List Function，后者包括UniADILR-HGc、Balanced COPA cause、CauseLogics和CLIMATE-FEVER。

<div class="method-step__io" markdown="1">

**输入**：来自多个训练来源的用户提示$x$、标准答案或目标解释$g$，以及数据集标识$d$。<br>
**输出**：统一表示的训练四元组$(x,g,d)$及其任务专用验证方式。

</div>

**直观理解**：不同数据集可能要求找原因、补事实或猜规则，但都被整理成同一个问题：什么解释最能说明已经看到的现象。两类训练来源分别练习“提出候选”和“比较候选”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 采样结构化推理与答案

模型按`<think>`$b2$`</think><answer>`$b1$`</answer>`格式生成完成文本$y$，再通过$b2(y)=\operatorname{ExtractThink}(y)$和$b1(y)=\operatorname{ExtractAnswer}(y)$分离推理与答案。任务正确性只读取$b1(y)$，过程评价只读取提示$x$和推理轨迹$b2(y)$。

<div class="method-step__io" markdown="1">

**输入**：训练实例中的提示$x$以及当前策略模型。<br>
**输出**：可独立验证的最终答案$b1(y)$和可独立评价的推理轨迹$b2(y)$。

</div>

**直观理解**：标签相当于把草稿区和答题区分开，避免因推理文字冗长而干扰答案匹配，也避免过程评判者直接依据标准答案给推理打分。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算正确性与过程奖励

数据集专用验证器$V_d$对$b1(y)$执行精确匹配、集合匹配或执行式验证，得到二值正确性$r_{\mathrm{cor}}$；gpt-oss-120b根据$x$与$b2(y)$评估证据覆盖$r_{\mathrm{cov}}$和证据到解释的方向性$r_{\mathrm{dir}}$。覆盖率是已被推理处理的观察细节比例；方向性按反向论证、混合或含糊、正向论证分别取$0$、$0.5$、$1$。

<div class="method-step__io" markdown="1">

**输入**：提示$x$、生成文本$y$、标准答案$g$和数据集标识$d$。<br>
**输出**：三个分量$r_{\mathrm{cor}}$、$r_{\mathrm{cov}}$、$r_{\mathrm{dir}}$及其等权复合奖励$R(x,y,g,d)$。

</div>

**直观理解**：答案验证器检查“结论对不对”，过程评判者检查“线索有没有讲全”和“是不是由线索推出结论”。这样，即使两个回答都答对，论证更完整、更符合溯因方向的回答也能获得更有信息量的训练信号。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 使用复合奖励进行GRPO更新

以复合奖励作为GRPO的优化信号更新开放权重骨干模型，使高正确性、高覆盖率且方向合理的生成行为更可能出现。原文节选未给出GRPO策略损失、组内优势计算、正则项或每个提示的采样数量，因此不能进一步还原其参数更新公式。

<div class="method-step__io" markdown="1">

**输入**：当前策略对训练提示生成的回答及其复合奖励$R(x,y,g,d)$。<br>
**输出**：经过溯因推理后训练的CEDAR-GRPO模型；推理时仅需输入新提示并生成结构化推理和最终答案。

</div>

**直观理解**：模型通过比较受奖励程度来调整生成倾向，不需要逐字模仿一条固定的人工推理链。复合奖励把“答对”和“推得像一个合格解释”同时变成学习目标。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### CEDAR-GRPO复合奖励

$$
R(x,y,g,d)=\frac{r_{\mathrm{cor}}+r_{\mathrm{cov}}+r_{\mathrm{dir}}}{3}
$$

**符号说明**

- $R(x,y,g,d)$：提示、生成结果、标准答案和数据集共同确定的总奖励
- $x$：包含观察或证据的用户提示
- $y$：模型生成的完整结构化文本
- $g$：标准答案或目标解释
- $d$：数据集标识，用于选择相应的答案验证器
- $r_{\mathrm{cor}}$：最终答案正确性奖励
- $r_{\mathrm{cov}}$：推理轨迹对观察细节的覆盖奖励
- $r_{\mathrm{dir}}$：从证据走向解释的方向性奖励

<div class="equation-explanation" markdown="1">

**直观理解**：总奖励对结果正确、证据覆盖和推理方向给予相同权重。它使模型不能只依靠偶然猜中答案获得全部训练收益，也不能仅写出形式良好但答案错误的推理。<br>
**原文位置**：第4.3节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 证据覆盖奖励

$$
r_{\mathrm{cov}}=\frac{1}{m}\sum_{j=1}^{m}z_j
$$

**符号说明**

- $r_{\mathrm{cov}}$：推理轨迹覆盖观察细节的比例
- $m$：过程评判器从提示中识别出的观察细节总数
- $j$：观察细节的索引
- $z_j$：第j项细节是否被推理处理的二值标记，已处理为1，未处理为0

<div class="equation-explanation" markdown="1">

**直观理解**：该式把每条证据是否得到解释转化为平均覆盖率。例如识别出五项观察而推理只解释四项时，覆盖奖励为$0.8$；若评判器无法给出有效细节列表，论文规定该奖励直接置为$0$。<br>
**原文位置**：第4.3节，公式(3)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练以$R(x,y,g,d)$作为GRPO的奖励信号。正确性项由$r_{\mathrm{cor}}=V_d(\alpha(y),g)$给出，其中$V_d(\alpha(y),g)\in\{0,1\}$；覆盖项按已处理观察细节的比例计算；方向性项要求推理从证据走向解释。主方法对三项等权平均，而消融中的Cor-GRPO仅保留正确性，Cor+Cov-GRPO与Cor+Dir-GRPO分别保留正确性和一个过程项，两个保留项各占$0.5$。从优化意图看，正确性保证答案可用，覆盖率迫使假设解释更多事实，方向性抑制先假定结论再反向合理化；三者联合把一般溯因推理的结果质量和过程结构同时纳入策略学习。需要注意，所给节选没有提供GRPO本身的策略梯度目标、组相对优势估计或KL约束，因而这些部分只能视为采用标准GRPO框架，不能据此声称具体公式或超参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 结构化CoT生成与解析**

模型生成$y=\langle\texttt{think}\rangle\,b2\,\langle\texttt{/think}\rangle\langle\texttt{answer}\rangle\,b1\,\langle\texttt{/answer}\rangle$。解析器分别提取$b2(y)$与$b1(y)$，使过程奖励不依赖最终答案文本，而任务验证也不受推理轨迹影响。

> 直观理解：这一模块建立清晰的评分边界：机器验证器只看正式答案，过程评判者只看题目和思考过程。它是把结果监督与过程监督组合起来的接口。

**2. 数据集专用正确性验证器**

$V_d(\alpha(y),g)$根据数据集$d$选择精确匹配、集合匹配或执行式验证，并输出$r_{\mathrm{cor}}\in\{0,1\}$。这种设计允许答案形态不同的任务共享强化学习框架，同时保留各任务原有的可验证标准。

> 直观理解：选择题、集合答案和可执行规则不能用同一种字符串比较方式判断，因此系统为每类任务使用合适的判分器。它提供相对客观的最终结果信号。

**3. 覆盖率与方向性过程评判器**

gpt-oss-120b在温度$0.0$下读取$x$与$b2(y)$：先从$x$返回$m$个观察细节并判断每项是否被处理，形成$z_j\in\{0,1\}$；再将方向性评为$0$、$0.5$或$1$。若评判器未返回有效细节列表，则$r_{\mathrm{cov}}$被设为$0$。

> 直观理解：覆盖率防止模型只抓住一条显眼线索，方向性则防止模型先猜答案、再倒推貌似合理的理由。两者共同约束“解释是否充分”和“论证路径是否合格”，但由于它们来自模型评判而非确定性程序，仍可能受到评判偏差影响。

**训练与推理**

训练阶段首先从同时包含假设生成和假设选择或评价任务的混合池中抽取$(x,g,d)$，当前骨干模型为每个提示生成带`<think>`和`<answer>`标签的$y$。系统分离$b2(y)$与$b1(y)$：$V_d$依据任务类型验证$b1(y)$，gpt-oss-120b则在温度$0.0$下仅依据$x$和$b2(y)$计算覆盖率与方向性；随后将三项奖励平均，并用所得标量执行GRPO更新。论文在问题设定中使用Qwen3-4B、Qwen3-8B、DeepSeek-R1-Distill-Qwen-7B和Llama-3.1-8B-Instruct四个开放权重骨干，以检验该训练方法能否跨模型规模与家族工作。

推理阶段不再需要标准答案$g$、验证器$V_d$或过程评判模型参与生成；经过训练的策略接收未见提示$x$，产生推理轨迹$b2(y)$和最终答案$b1(y)$，下游任务读取$b1(y)$作为预测。结构化推理仍可保留以供分析，但节选没有说明部署时是否强制标签格式、是否使用特定解码温度、是否进行多样本投票或验证器重排，因此不能把这些做法归入其推理流程。

**复现信息**

为公平理解方法，需要保留四点。第一，输出格式固定区分推理和答案，生成器完整提示位于附录B，但当前节选未提供其内容。第二，正确性验证随数据集变化，可采用精确匹配、集合匹配或执行式验证；详细验证规则、失败处理和数据集说明在原文后续材料中，当前节选未完整给出。第三，两个过程奖励均由gpt-oss-120b在温度$0.0$下评判，且只向它提供$x$与$b2(y)$；无有效观察细节列表时，覆盖奖励置零。第四，主奖励三项等权，而奖励消融中的两项组合各以$0.5$加权。

训练骨干覆盖$4$B到$8$B参数规模，包括通用指令模型与推理导向模型。消融说明SFT与RL使用相同训练池和相同`<think>`、`<answer>`响应格式，并尽量匹配PEFT配置、优化预算与检查点选择协议，但节选未报告学习率、批量大小、LoRA或其他PEFT参数、GRPO组大小、采样温度、训练步数、硬件和随机种子。因而这些信息不足以从当前材料完整复现实验；尤其不能自行补全标准GRPO超参数或假定过程评判器完全可靠。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 持出评测套件：用于检验跨任务泛化，涵盖闭式选择、形式化缺失事实、规则学习和机器学习调试等不同任务形态。所给节选仅明确提到 ART、COPA-effect 和 DefasibleNLI 的评测提示模板，未提供完整数据集清单、样本规模或具体划分。
- ART：叙事溯因选择任务。输入两条前后观察及两个候选假设，模型选择最能解释状态转变的假设；它主要测试常识、因果关系和叙事连贯性。原文节选未明确报告规模与划分。
- COPA-effect：给定一个原因和两个候选结果，选择最可能的直接结果；它测试从原因到结果的常识因果推断。该方向与训练提示中出现的 COPA-cause 相反，因此可用于观察模型是否学到较一般的因果推理能力。原文节选未明确报告规模与划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率**

用于闭式选择任务，计算最终答案选择正确的样本比例；它衡量任务结果是否正确，不直接评价推理文本是否可靠。 （越高越好，因为正确完成选择任务的样本占比更大。）

</div>
<div class="metric-item" markdown="1">

**精确匹配或验证器判定的正确性**

用于形式化缺失事实与规则学习任务：能够规范化比较的答案采用精确匹配，程序或形式规则输出则由验证器检查是否满足任务条件。 （正确率或通过率越高越好，因为更多输出与标准答案完全一致或通过形式验证。）

</div>
<div class="metric-item" markdown="1">

**通过或修复成功率**

用于机器学习调试任务，衡量模型给出的修改是否使目标检查通过或成功修复故障。 （越高越好，因为更多调试实例被实际修复；该指标不等同于代码可维护性或对故障原因的正确解释。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给来源在表格位置仅保留了“Model”和“Ablation”等标题，未包含任何完整结果行、分数或比较结论。因此无法可靠返回三项主结果或两项关键消融；填入具体数值、胜负关系或增益幅度都会超出证据。
- 实验协议说明任务分数只取决于最终答案字段，这能清晰衡量可验证正确性，却不能单独证明生成的推理轨迹忠实反映模型内部推断，也不能证明方法已获得领域外的一般溯因能力；后者还取决于完整评测套件与训练数据之间是否真正隔离。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原始基础模型：未经过本文后训练的起点，用于判断任何性能变化是否确实来自后训练。
- Cor-GRPO：仅使用正确性奖励训练的 GRPO 检查点。它与 CEDAR-GRPO 共享强化学习范式，因此可较直接地检验复合奖励是否比“只奖励最终答案正确”更有效。
- 匹配的通用推理后训练对照：用于排除增益仅来自额外推理训练或额外计算，而非溯因导向训练设计的可能性。所给节选未报告该对照的具体模型名称、训练数据或结果。
- 训练池与奖励相关的消融版本：分别移除或改变强化学习、奖励设计及两阶段训练池构造，用于定位完整方法中真正产生作用的组成部分。所给节选未给出各版本名称。

**实验想回答的问题**

- 采用复合奖励进行后训练的 CEDAR-GRPO，能否在未用于训练的任务上提升一般溯因推理能力，而非仅提高训练任务上的表现？
- 若性能发生变化，它是否伴随推理过程质量的改善，以及这种变化分别来自强化学习、复合奖励设计、两阶段训练池构造中的哪些因素？

**实验实现**

实验分为三层证据：持出任务表现、推理轨迹的过程级测量，以及针对强化学习、奖励设计、两阶段训练池和通用推理后训练对照的消融。主比较对象是基础模型、仅正确性奖励的 Cor-GRPO 和复合奖励的 CEDAR-GRPO。任务得分一律只根据最终答案字段计算，过程指标则单独从推理轨迹计算，从而避免把冗长解释本身误计为任务正确性。评测提示要求模型分别输出 `<think>` 推理区和格式严格受限的 `<answer>` 最终答案区。所给节选未报告基础模型名称、解码参数、采样次数、随机种子、训练预算、完整评测集规模、统计显著性检验或结果表中的具体数值。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces a process-aware GRPO reinforcement-learning method to improve abductive reasoning in LLMs.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`ea213b1c96c1f51c21024c7a6c706f527691e68795b3dc82cfcb0a7b2cd0ebe8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
