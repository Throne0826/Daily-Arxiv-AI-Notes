---
title: "[论文解读] No Judgment Without a Reason: Counterfactual Receipts for Versioned AI Evaluators"
description: "[arXiv 2608.20938][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.20938"
announcement_date: "2026-08-24"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-24T02:08:53.474457+00:00"
source_sha256: "b80fecd11430fab35feaf77abf470f9ed7f776ab9b602bed035385e59e884f52"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.20938</p>

# No Judgment Without a Reason: Counterfactual Receipts for Versioned AI Evaluators

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Ye Chen, Weining Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Alibaba Group；Affiliation: Cheung Kong Graduate School of Business</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20938v1) · [PDF 下载](https://arxiv.org/pdf/2608.20938v1) · **关键词** LLM 评测<br>


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

本文位于人工智能评估器审计与可验证推理交叉领域。这里的“评估器”是对模型输出进行判定的系统，其标签可能用于放行动作、分流人工复核或生成训练反馈。传统评估主要检查最终标签是否正确，却未必检查评估器是否依据了正确的证据、决策规则以及规则适用的权限。因此，本文把评估器从一个只输出标签的黑盒，扩展为需要对版本间判断变化负责的系统：当评估器从旧版本变为新版本时，审计者不仅要知道新标签是什么，还要验证哪些已声明的来源变化足以导致该标签变化。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**版本化评估器与监督环路**

版本化评估器是具有旧状态和新状态的判断系统；同一案例在两个版本中可能得到不同标签。监督环路指评估结果会影响发布、动作授权、人工复核或后续训练，因此错误判断理由可能造成比单次分类错误更广泛的影响。

</div>
<div class="concept-item" markdown="1">

**反事实替换与判断立方体**

反事实替换是把旧评估器中的某些来源替换为新版本来源，然后观察判断是否改变。本文有三类来源，每类只有“保留旧版本”或“替换为新版本”两种状态，因此形成 $2^3=8$ 个组合，即判断立方体；它完整记录不同来源组合下的输出。

</div>
<div class="concept-item" markdown="1">

**最小充分解释与判断收据**

充分解释是一组来源替换，使系统能够重现修订后的判断；最小充分解释要求删除其中任一替换后都不能再重现该判断。判断收据是所有包含关系最小的这类替换集合，解释的是版本转换，而不是单个输入上的普通理由文本。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

对一个案例，评估器状态由三类具有类型和版本的来源组成：grounds 表示证据，norms 表示决策规则，authority 表示规则适用的权限或管辖条件。设旧状态为 $S^{old}=(G^{old},N^{old},A^{old})$，新状态为 $S^{new}=(G^{new},N^{new},A^{new})$；输入包括该案例以及两组对应的来源，输出包括旧判断、新判断、八种来源保留或替换组合下的判断，以及能够重现新判断的完整最小替换集合，即判断收据。对任意来源子集 $C\subseteq\{G,N,A\}$，反事实状态将 $C$ 中的来源取自新版本，其余来源保留旧版本，并由评估器或参考裁决器重新执行。其基本假设是：来源类型已预先声明，替换操作具有明确语义，参考裁决器能够验证候选收据；黑盒评估器本身只提供输出，因而认证需要实际执行反事实查询，而模型预测的收据不能自动等同于已认证的收据。本文的研究对象不是证明某个来源在哲学或现实世界中是唯一原因，而是在给定旧状态、修订状态和替换语义下，确定哪些最小来源替换足以重放新判断。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G$**

grounds，证据来源；$G^{old}$ 和 $G^{new}$ 分别表示旧版本与新版本的证据。

</div>
<div class="notation-item" markdown="1">

**$N$**

norms，决策规则来源；它规定如何依据案例证据作出判断。

</div>
<div class="notation-item" markdown="1">

**$A$**

authority，规则适用的权限或管辖来源；它规定某项规则是否适用于当前案例。

</div>
<div class="notation-item" markdown="1">

**$C\subseteq\{G,N,A\}$**

被替换为新版本的来源子集；$C$ 中的来源使用新版本，其余来源使用旧版本。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

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

该方法把评估器的判断从单一的最终标签扩展为可审计的“判断收据”（judgment receipt）。输入是一个待评估案例及其三类可替换来源：依据（grounds，案例事实或证据）、规范（norms，规则或政策）和权限（authority，决定规则是否适用于当前情境的授权边界）；系统通过反事实地替换这些来源，观察评估器的修订判断，并输出最终判决、来源替换集合及其对应的八单元判断立方体（judgment cube）。核心目标不是只问“标签是否正确”，而是进一步验证“标签变化是否由正确证据、稳定规则和适当的规则适用性共同造成”。直观地说，普通评估只检查答案，本文要求评估器同时提交一张最小化的因果变更清单，说明答案为什么改变。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造版本化评估案例

将案例拆分为依据、规范和权限三个可独立操纵的来源，并为每个来源设计保持语义或指定规则变化的版本。三类来源的原始或替换状态形成 $2^3=8$ 个组合，即八单元判断立方体。

<div class="method-step__io" markdown="1">

**输入**：政策或逻辑推理任务中的原始案例、依据来源、规范来源、权限来源，以及需要比较的原始版本和修订版本。<br>
**输出**：一组带有明确来源版本、原始判决与修订判决的反事实评估实例。

</div>

**直观理解**：先把一条判断拆成“事实是什么”“采用哪条规则”“这条规则是否有权适用”三部分，再分别开关这些部分。这样可以测试答案变化究竟对应哪一种原因，而不是只比较两个最终标签。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行冻结评估器并预测判决变化

对原始输入和来源替换后的输入进行评估，记录最终判决，并在直接收据任务中直接预测来源替换集合；在判断立方体任务中，同时预测八个来源组合对应的判断格局及其收据。模型输出既包括修订后的判决，也包括解释该变化所需的来源归因。

<div class="method-step__io" markdown="1">

**输入**：每个版本化案例及其反事实来源组合；评估器可以是冻结的语言模型或其他黑箱判断系统。<br>
**输出**：修订判决、直接收据或判断立方体、以及可用于一致性检查的结构化预测。

</div>

**直观理解**：模型不只回答“改成了什么”，还要回答“是哪些输入被改动后导致改判”。判断立方体要求它一次性描述所有来源组合下会怎样判断，因此比只回答一个改判更严格。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成并验证最小判断收据

寻找能够重现修订判决的最小来源替换集合，并将其与金标准收据比较；同时检查收据是否与预测的判断立方体内部一致。收据正确性与最终判决正确性分开计量，以识别“答案正确但理由归因错误”的情况。

<div class="method-step__io" markdown="1">

**输入**：原始判决、修订判决、来源替换集合，以及评估器在相关反事实版本上的输出。<br>
**输出**：经过验证的最小判断收据、收据准确率、修订判决准确率和收据—判决分离诊断。

</div>

**直观理解**：最小收据类似于故障报告中的“真正动过的零件清单”：如果删去其中任何一项就无法重现改判，它才说明了必要原因。即使模型碰巧答对最终标签，收据仍可能暴露它把原因归错了。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 进行鲁棒性与组合泛化测试

比较模型在来源排列、不同来源组合和更深推理结构上的收据恢复能力，并报告标准判决准确率与收据准确率的差距。进一步使用选择性会计设置，在部分覆盖率下集中审查低置信度或高风险收据，并记录覆盖率、理由债务和正确金标准变化召回率。

<div class="method-step__io" markdown="1">

**输入**：语义保持但表面形式改变的来源排列、训练中只出现单来源变化的组合，以及测试中的双来源或三来源变化。<br>
**输出**：变换一致性、未见组合上的判决与收据表现，以及选择性审计的覆盖—错误权衡。

</div>

**直观理解**：如果只把词序或格式改掉，意义没有变，合理系统应保持相同理由；如果训练只教过改一个来源，真正困难的测试则要求它处理多个来源同时变化。该步骤检验模型是否学会了规则，而不是记住了表面模式。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：所给章节未提供可准确复述的训练损失或优化目标。方法的监督对象可以确定为判决、来源变化及其收据或立方体结构，但原文摘录未明确说明这些输出如何组成具体损失函数，也未明确说明是否采用联合优化、序列生成损失或其他目标，因此不能据此补写公式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 三源反事实表示**

方法将判断依据表示为 grounds、norms 和 authority 三类来源，并通过每类来源的替换状态形成八个反事实单元。该表示把“事实变化”“规则变化”和“规则适用性变化”分离，支持对判断更新进行来源级归因。

> 直观理解：同一个错误答案可能来自看错事实、用错规则，或把不适用的规则强行套用。三源表示的作用是把这三种错误拆开检查。

**2. 最小判断收据**

判断收据是能够复现修订判决的最小来源替换集合；其验证不只比较最终标签，还比较预测替换集合与金标准替换集合是否一致。该模块因此定义了“收据准确率”，并支持判决正确性与理由正确性的分离分析。

> 直观理解：收据回答的是“哪些改变足以解释新答案”。最小性避免模型把所有来源都列上，从而掩盖真正造成改判的因素。

**3. 判断立方体与一致性审计**

判断立方体联合预测八种来源组合下的判断和收据，并检查收据是否与其自身单元预测相容。论文将立方体预测与直接收据预测区分开来，因为前者要求模型维护跨反事实单元的一致结构，而不仅是完成一次局部归因。

> 直观理解：直接收据像解释一次改判，判断立方体则像填写一张完整的决策表。后者可以发现模型在不同假设下的判断彼此矛盾，即使每个单独答案看起来都合理。

**训练与推理**

推理时，评估器接收版本化案例及来源信息，分别处理原始版本和反事实替换版本；直接收据设置要求输出修订判决及其来源替换集合，判断立方体设置还要求输出八个来源组合的判断格局。随后将预测收据与可验证金标准比较，并检查其是否能解释修订判决以及是否与立方体内部一致。训练流程方面，所给章节只明确报告了冻结评估、排列鲁棒性训练和“训练于干预基数为零或一、测试于基数为二或三”的真实组合留出实验；未提供完整的训练数据组织、提示模板、损失函数或解码算法，因此不能进一步断言具体优化流程。

**复现信息**

可复现或公平解读结果所必需的信息包括：评估应区分直接收据与判断立方体两种输出形式；主要结果使用冻结评估，并以修订判决准确率和精确收据族准确率分别衡量标签是否正确、理由归因是否正确；收据分析还应在端点均正确的变化案例上单独检查错误归因。所给材料报告了组合留出设置使用三个目标种子，并将单来源训练推广到双来源或三来源变化；但未明确报告完整的输入格式、收据搜索算法、生成约束、训练轮数或硬件配置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ReasonBench：论文提出的政策与逻辑推理基准，包含 19,520 个案例和 7,200 个控制样例；其作用是同时评估判决、收据以及受控变换下的一致性。原文未明确报告完整的训练集、验证集和锁定测试集规模；主实验说明在均衡两个数据层后，每次主运行使用 5,184 个唯一训练样例。
- 锁定测试集：用于比较多数类、字符级 TF-IDF、直接收据、理由收据和判断立方体等方法在固定来源序列化协议下的修订判决与精确收据族表现。它测试的是熟悉呈现形式上的泛化，而不是完整的语义鲁棒性。
- 受控测试集：包括来源顺序置换、未见多来源组合以及组织性条款与逻辑世界等分层控制；其作用是检验模型对含义保持变换、真正组合变化和不同数据子结构的稳定性，而非只记忆来源位置或措辞。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**修订判决准确率**

衡量模型是否正确预测来源更新后的最终判决，即 $widehat{y}^{1}$ 是否等于真实修订判决；它只评价结论，不评价结论变化的理由。 （越高越好，但高分不能证明模型找到了正确的最小来源替换集合，也不能证明其对等价输入保持一致。）

</div>
<div class="metric-item" markdown="1">

**精确收据族准确率**

衡量模型预测的完整收据族是否与真实收据族完全相同。收据是能够重现判决变化的最小来源替换集合，因此该指标同时要求覆盖正确来源并满足最小性。 （越高越好；相比判决准确率，它更直接检验可审计的因果解释，但仍需结合受控变换一致性和可执行证书验证。）

</div>
<div class="metric-item" markdown="1">

**变换一致性**

在保持来源含义不变的顺序置换等变换前后，检查模型预测的判决或收据是否保持应有关系；论文分别报告直接目标和立方体目标的有效收据恢复表现。 （越高越好，因为它检验模型是否依赖语义而非来源位置、格式或措辞等表面线索。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 锁定测试上的表面诊断与学习目标比较

<div class="result-value" markdown="1">

多数目标达到 53.8% 修订判决准确率和 44.2% 精确收据准确率；字符级 TF-IDF 达到 90.0% 和 61.7%。主学习实验中，直接收据是最强的收据目标；Qwen3-1.7B 的直接收据准确率为 98.41%，判断立方体预测为 96.99%，后者低 1.42 个百分点。

</div>

词面特征确实能利用锁定测试中的可见规律，但不能解释接近 98% 的学习结果。直接收据优于立方体，说明输出更多反事实单元格并不会自动带来更好的统计学习目标；立方体的理论可验证性不等于序列模型更容易学会。该结果证明的是固定渲染下的可预测性，不是模型已经掌握了与呈现方式无关的推理机制。

<div class="result-source" markdown="1">

来源：第 7 节结果概述；锁定测试结果表（原文所选章节未完整提供表号）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The 98.41% receipt accuracy and 96.99% cube prediction scores demonstrate that direct receipt supervision slightly outperforms cube supervision.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 等价来源顺序置换控制

<div class="result-value" markdown="1">

保持来源含义不变而仅改变来源顺序后，有效收据恢复率降至直接目标 54.8%、立方体目标 49.2%。这表明锁定测试中的高分无法直接推出呈现独立的推理能力。

</div>

同一组 grounds、norms 和 authority 只是换了排列，语义上应得到相同收据；性能大幅下降说明模型可能利用了来源位置、序列化格式或其他表面相关性。该控制比普通测试更能区分“预测正确”与“依据正确关系预测”，但它仍不能单独证明模型完全没有使用语义信息。

<div class="result-source" markdown="1">

来源：摘要；第 8.2 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Meaning-preserving source permutations reduce valid receipt recovery to 54.8% and 49.2% for direct and cube prediction.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 未见多来源组合与小模型复制

<div class="result-value" markdown="1">

在训练中隐藏干预组合、但不改变渲染协议的组合留出实验中，直接预测通常仍能保持修订判决，却不能识别最小替换来源；Qwen3-0.6B 复制了直接收据优于立方体的排序，但模型深度下降会进一步恶化表现。

</div>

模型可能学会“哪些结论常出现”，却没有学会多个来源共同变化时哪一个最小集合真正造成判决更新，因此判决准确率和收据准确率必须分开报告。较小模型复现总体排序，增强了主要比较并非单一 Qwen3-1.7B 偶然现象的可信度；不过它不能证明结论与模型规模无关。

<div class="result-source" markdown="1">

来源：第 8.2 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The 0.6B replication shows the direct-versus-cube ordering is not an artifact of one backbone; its depth degradation warns against claiming capacity-independence.

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

- 多数目标基线：始终预测训练数据中最常见的目标，用于检验结果是否仅由标签频率造成。
- 字符级 TF-IDF：依据字符词频—逆文档频率特征进行分类，用于检验输入中的词面或序列化线索能否解释性能。
- 直接收据监督：直接输出旧判决、新判决及完整收据族，是最重要的学习比较对象，因为其目标与精确收据指标直接对应。
- 判断立方体监督：输出八个来源组合单元格中的判决，再机械推导端点判决和收据；它检验“更密集的反事实信号”是否比直接预测收据更有利。

**实验想回答的问题**

- 完整判断立方体监督是否比直接收据监督更能提升修订判决准确率与精确收据族准确率，尤其是在多来源更新、收据歧义和等价输入呈现下。
- 高标准判决准确率是否真正对应可审计、稳定的推理：模型能否在来源置换、逆关系和未见多来源组合等控制条件下保持收据正确性与变换一致性。

**实验实现**

主干模型为固定版本的 Qwen3-1.7B，并使用 LoRA 适配；LoRA 秩为 16、alpha 为 32、dropout 为 0.05，作用于注意力和 MLP 投影。主实验使用五个随机种子，并保持数据、优化和解码设置一致。学习目标包括直接判决、直接收据、带确定性一句话理由的理由收据，以及按固定单元格顺序输出八个判决的判断立方体。立方体输出可由构造保证内部形式一致，但这种一致性只是格式属性，不能保证八个单元格预测正确。论文还进行 Qwen3-0.6B 复制实验、来源顺序置换控制、未见多来源组合控制，以及置换增强训练；其中锁定测试评价固定渲染协议下的预测能力，受控测试评价跨呈现和跨组合的推理稳定性。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 简单单来源监督与复杂多来源更新 | 在简单单来源变化上训练的模型仍有 93.75% 判决准确率，但复杂多来源更新的收据恢复率仅为 7.16%。 | 该消融隔离了“能否预测端点判决”和“能否找出最小原因集合”之间的差异。模型可以在结论层面保持很高准确率，却无法组合多个来源的变化并恢复最小收据，因此单一判决指标会严重高估推理能力。 | 摘要；第 8.2 节所述 composition holdout<br><span class="experiment-evidence">Models trained on simple single-source changes retain 93.75% verdict accuracy but recover only 7.16% of receipts for complex multi-source updates.</span> |
| 来源置换增强训练 | 加入置换训练后，直接目标的一致性提升至 96.6%，但立方体预测缺口反而扩大；性能损失主要集中在六条组织性条款，六条组织性条款的改善也弱于逻辑世界。 | 该消融测试增加等价呈现的训练多样性是否能消除位置捷径。它确实显著改善直接目标的一致性，却没有普遍修复立方体目标，说明鲁棒性训练可能改变错误分布而非解决多单元格组合预测困难；因此不能把一致性提升简单解释为完整推理能力提升。 | 摘要；第 8.2 节和第 8.4 节<br><span class="experiment-evidence">Permutation retraining boosts consistency to 96.6% yet worsens cube prediction deficits.</span> |

**定性案例**

- 论文将预测平面与证书平面作为应用层面的案例设计：预测模型输出 $(\widehat{y}^{0},\widehat{y}^{1},\widehat{\mathcal{R}},c)$ 供路由和人工复核分流，可信执行器则计算 $\operatorname{Cert}(x;D,I^{0},I^{1})=(h(x,D,I^{0},I^{1}),Q_x,\mathcal{R}_x)$。这说明模型可以作为收据提议者，但只有绑定案例、裁决器和来源版本的执行证书才能真正承担审计责任；论文未报告该设计在真实部署中的延迟或人工节省。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：核心贡献是通过反事实收据和基准评估语言模型评估器的推理可追责性与变换一致性。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`b80fecd11430fab35feaf77abf470f9ed7f776ab9b602bed035385e59e884f52`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
