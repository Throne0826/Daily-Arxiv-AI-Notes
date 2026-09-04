---
title: "[论文解读] What Else Needs Fixing? Exploring Cost-Effective Test-Time Compute for Revision Propagation in Artifacts Generated Through Conversation"
description: "[arXiv 2609.03254][LLM 评测] 原文未明确报告。"
arxiv_id: "2609.03254"
announcement_date: "2026-09-04"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:39:27.810361+00:00"
source_sha256: "732e68e45d9e9399cac71d2ad72963fea5c81269f5a0eacac0bfe82be30b2e16"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大型语言模型"
  - "修订传播"
  - "对话式生成产物"
  - "隐式依赖"
  - "JSON"
  - "测试时计算"
  - "RevPropBench"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2609.03254</p>

# What Else Needs Fixing? Exploring Cost-Effective Test-Time Compute for Revision Propagation in Artifacts Generated Through Conversation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Daisuke Kikuta</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: NTT, Inc</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03254v1) · [PDF 下载](https://arxiv.org/pdf/2609.03254v1) · **关键词** 大型语言模型, 修订传播, 对话式生成产物, 隐式依赖, JSON, 测试时计算, RevPropBench<br>
**代码**: [https://github.com/ntt-dkiku/llm-revision-propagation](https://github.com/ntt-dkiku/llm-revision-propagation) · **项目页**: [https://github.com/ntt-dkiku/llm-revision-propagation](https://github.com/ntt-dkiku/llm-revision-propagation)

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

本文研究大型语言模型（LLM）在对话式生成产物中的修订传播（revision propagation）能力。用户通常先通过多轮对话生成文档、代码、计划或配置等结构化产物，再提出局部修改请求；模型不仅要修改被直接指出的部分，还要识别由该修改影响的其他部分，并同步更新它们以维持整体一致性。既有研究主要面向依赖关系较明确的代码仓库、知识图谱或文档结构，而本文关注依赖关系可能隐含在生成产物之外的对话历史中的场景，并进一步研究如何用测试时计算以较低成本提升修订质量。为便于系统处理和自动评估，本文将产物限定为 JSON 格式。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**修订传播**

修订传播是指对产物中的一个局部元素进行修改后，继续更新所有依赖该元素的其他元素，以保持全局一致性。例如，改变计划中的日期可能同时需要修改相关任务的时间、顺序或状态。

</div>
<div class="concept-item" markdown="1">

**隐式依赖**

隐式依赖是指两个元素之间存在影响关系，但这种关系没有以调用图、引用、字段约束或知识图谱边等明确形式预先给出。在本文中，依赖关系可能只存在于此前生成产物的多轮对话语境中，因此模型需要从对话和产物共同推断影响范围。

</div>
<div class="concept-item" markdown="1">

**测试时计算**

测试时计算是模型生成答案时额外使用的推理、采样、反思或候选搜索过程，而不是重新训练模型。本文比较顺序反思和并行采样等方法，目标是在增加推理成本的同时获得更好的准确率与成本性能权衡。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一段包含产物生成过程的多轮对话、当前 JSON 产物以及用户提出的局部修订请求，模型需要输出完成修订后的 JSON 产物。任务要求模型识别请求直接涉及的元素，推断由该变化产生的隐式依赖，并更新所有受影响元素，同时保持不相关元素不被错误修改。本文假设依赖信息可能嵌入对话历史而非显式依附于 JSON 结构本身；研究范围限定为 JSON 产物，覆盖规划、记录保存和配置等领域，并考察包含 10、50 或 100 个 JSON 元素的不同规模。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

当前需要修订的 JSON 产物及其相关输入语境；具体可包含产物内容、对话历史和用户修订请求。

</div>
<div class="notation-item" markdown="1">

**$x'$**

模型根据局部修订请求生成的修订后 JSON 产物，即任务的输出。

</div>
<div class="notation-item" markdown="1">

**$D$**

修订传播评测数据集；本文具体使用新建的 RevPropBench。

</div>
<div class="notation-item" markdown="1">

**$N$**

并行采样得到的候选修订数量；测试时计算方法从这些候选中选择最终输出。

</div>

</div>

**直接相关的工作**

- **代码仓库级编辑（Jimenez et al., 2024；Bairi et al., 2024；Du et al., 2025）**: 这些工作同样要求模型在局部任务之后定位相关文件并传播跨文件修改，但通常可以利用调用图、导入关系和变量引用等较明确或可静态分析的依赖信息。本文将问题扩展到对话式生成的 JSON 产物，其中依赖关系可能没有预先构建的图结构，并可能只在对话历史中隐式建立。
- **RippleEdits（Cohen et al., 2024）与 ChainEdit（Dong et al., 2025）**: 知识编辑研究把修订传播视为事实修改后的连锁影响：模型需要更新相关事实，并保留不应变化的事实。RippleEdits 通过相关事实查询评估这种影响，ChainEdit 借助知识图谱中的逻辑规则增强传播；相比之下，本文处理的是对话生成的 JSON 产物，通常缺少预先存在的知识图谱或显式依赖来源。

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

RevPropBench把“对话中生成的结构化产物能否正确传播局部修改”形式化为一个受控评测任务。每个样本包含预先生成的多轮用户—LLM对话、由各轮补丁逐步构成的最终 JSON 产物、一条只明确提出局部变化的修订请求，以及人工审核后的金标准 JSON Patch。被测模型读取完整上下文并输出符合 RFC 6902 的有序补丁序列；评测程序执行补丁后，将所得产物与执行金标准补丁后的产物比较，以判断所有直接和间接受影响元素是否都被正确修改，同时避免无关编辑。

基准构建采用“强模型生成、另一强模型预标注、人工复核”的流程：先设计覆盖不同应用领域与依赖传播模式的场景，再合成对话和修订请求，随后由辅助模型提出候选金标准补丁并由标注者校正。通俗地说，任务不是检查模型是否会改用户点名的一个字段，而是检查它能否像维护电子表格公式或项目计划一样，沿着隐藏在对话历史和产物内容中的依赖关系，把所有连带变化改全、改对，并且不碰无关部分。需要注意，所给章节主要描述基准与评测流程，并未给出论文所比较的顺序反思、并行采样和候选选择方法的具体算法，因此这里不补写其未提供的推理细节。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 场景设计与受控采样

研究者借助强 LLM 进行场景构思，并以领域多样性、传播模式多样性和金标准可确定性为约束；随后控制最大对话轮数与目标元素数量，为每个场景生成小、中、大三个规模的样本。

<div class="method-step__io" markdown="1">

**输入**：应用领域、期望的对话流程、修订传播模式，以及目标产物规模。<br>
**输出**：覆盖九个实际领域和多种传播结构的场景集合，以及每个场景对应的合成任务实例。

</div>

**直观理解**：这一步相当于先设计一组可判卷的连锁修改题，并有意识地改变题目行业、依赖形态和规模，而不是从开放网络中随机收集难以确定唯一答案的案例。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多轮对话与 JSON 产物生成

生成模型合成用户—LLM对话；每个 LLM 回合至少输出一个向 JSON 产物添加元素的补丁，按对话顺序执行各轮补丁，直到达到目标元素数或最大轮数，从而形成最终产物。

<div class="method-step__io" markdown="1">

**输入**：一个已设计场景及其对话流程、目标元素数量和最大轮数。<br>
**输出**：完整对话历史、逐轮生成补丁和一个最终 JSON 产物。

</div>

**直观理解**：产物不是一次写成，而是像用户与助手逐轮完善行程、项目计划或配置文件那样累积形成，因此后续修订所需的依赖信息可能散落在较早的对话中。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 局部修订请求与金标准标注

另一强 LLM 先生成候选金标准补丁，人工标注者再通过图形界面检查并纠正每个补丁的操作、路径和值；对允许多种措辞的自由文本配置关键词匹配器，对“修改或保持均合理”的元素设置可选标志。

<div class="method-step__io" markdown="1">

**输入**：合成的对话历史、最终 JSON 产物，以及针对其中局部内容的修订请求。<br>
**输出**：经过人工审核的有序金标准 JSON Patch，以及关键词匹配和可选元素等判定规则。

</div>

**直观理解**：辅助模型负责提供初稿，但最终答案由人核查；宽松匹配规则用于避免把语义正确的不同表述误判为错误，而可选标记则处理上下文中确实不存在唯一编辑选择的情况。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 模型修订推理

被测 LLM需要从对话与产物中识别直接及间接受影响的元素，并输出由 $\textit{op}$、$\textit{path}$ 和 $\textit{value}$ 组成的 RFC 6902 补丁序列；其中操作类型限于替换、添加和删除。

<div class="method-step__io" markdown="1">

**输入**：预先准备的生成阶段对话、最终 JSON 产物和用户的局部修订请求。<br>
**输出**：可按顺序执行的预测 JSON Patch，以及应用该补丁后得到的修订产物。

</div>

**直观理解**：模型既要找到用户明确点出的修改位置，也要追踪所有连带依赖；输出补丁而不是整份重写结果，可以清楚记录它改了哪里、怎样改以及是否误改。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该章节提出的是评测基准及其数据构建、标注和计分方法，不是需要训练的新模型，也未定义损失函数或参数优化目标。合成数据时调用强 LLM 生成场景、对话和候选标注，但这属于离线数据生产而非对被测模型进行训练；论文标题和摘要提到的测试时计算方法也属于推理阶段策略，而非训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 对话式修订传播任务表示**

一个实例将生成阶段对话、由逐轮补丁累积得到的 JSON 产物和局部修订请求共同作为条件，目标输出是有序的 RFC 6902 JSON Patch。每个补丁操作可表示为三元组 $(\textit{op},\textit{path},\textit{value})$，其中 $\textit{op}\in\{\texttt{replace},\texttt{add},\texttt{remove}\}$，$\textit{path}$ 定位目标元素，$\textit{value}$ 给出新内容；删除操作在 RFC 6902 中不需要新值，但原文以统一三元组说明其标注表示。

> 直观理解：该表示把复杂的整份产物修订拆成一组可检查的原子动作。它尤其适合研究“修改传播”，因为评测者可以区分模型是否找到了正确路径、选择了正确操作，并填入了正确内容。

**2. LLM 辅助的人机协同金标准构建**

数据生成与答案标注由不同的强 LLM 辅助：一个模型合成对话和局部修订请求，另一个模型生成候选金标准补丁，随后由人工标注者借助 GUI 逐项复核和修正。场景必须使正确补丁能够确定，以降低开放式修订带来的答案歧义；对于仍然存在的合理语言变体和编辑可选性，则通过关键词匹配器与可选标志显式编码。

> 直观理解：完全人工编写成本高，完全依赖模型又可能把模型错误当成答案，因此论文让模型承担批量起草工作，让人负责最终质量控制。额外的匹配规则不是放宽任务本身，而是避免把措辞差异或真正合理的多解情况算作失败。

**3. 产物级完成判定与错误分解**

主要指标完成率按样本统计：只有预测补丁执行后的 JSON 产物与金标准补丁执行后的产物完全一致，样本才记为完成。诊断指标进一步区分 $\text{miss}$、$\text{over edit}$ 和 $\text{wrong value}$，分别对应遗漏必要修改、修改了不应修改的元素，以及必要修改位置上的值不正确；可选元素在保持不变或正确编辑时均可接受，只有被改成错误值时才计错。

> 直观理解：严格的产物级判定直接对应真实使用需求：一份行程、账单或部署配置只要漏掉一个关键连带修改，就可能仍然不可用。错误分解则能判断增加测试时计算究竟改善了依赖召回、抑制了过度修改，还是仅提高了具体值的生成质量。

**训练与推理**

训练方面，所给章节未报告利用 RevPropBench 微调模型；生成阶段对话已提前准备，正式任务只执行修订阶段。推理时，被测模型接收完整的生成阶段上下文、最终 JSON 产物和局部修订请求，需自行恢复显式或隐式依赖，并输出 RFC 6902 补丁。随后评测器按顺序执行补丁，将预测修订产物与金标准修订产物比较。

从摘要可知，完整论文比较了九种修订方法，包括顺序反思和并行采样变体，并探索基于 LLM 或中心样本的候选选择；然而当前所给第 2 节没有描述这些方法的提示流程、反思轮次、采样参数、中心样本距离定义或最终选择算法。为避免臆造，本分析只能完整还原基准侧的端到端推理接口，不能进一步声称某一测试时计算方法如何生成或筛选候选。

**复现信息**

基准实例包含 $50$ 个场景，每个场景生成含 $10$、$50$、$100$ 个元素的小、中、大样本各一个，共 $50\times3=150$ 个样本；领域覆盖旅行行程、发票、购物车、项目进度、课程计划、数据流水线、软件部署配置、组织访问计划和制造业物料清单。产物规模通过目标元素数量和最大对话轮数共同控制：对话最多运行到轮数上限，但达到目标元素数后可提前结束；每个 LLM 回合至少添加一个元素。

复现评测时应使用有序 RFC 6902 补丁并实际应用到同一个原始 JSON 产物，而不能仅比较补丁文本，因为不同但等效的操作表达可能得到同一最终状态。对自由文本值应使用标注时定义的必需关键词匹配器；对带可选标志的元素，保持不变与正确修改都视为正确，但错误修改仍需计错。当前节提到合成与预标注可分别使用 GPT-5.5、Claude-Opus-4.8 等强模型作为示例，但未明确给出固定模型版本、提示模板、解码参数、标注者数量、一致性统计或完整数据划分，相关复现信息需进一步核对附录和代码仓库。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 论文新建的修订传播基准包含 50 个场景、9 个领域和 6 种传播模式；每个场景有 3 种工件规模，共 150 个样本。按场景划分数据，保证同一场景的三个规模版本不会跨集合：10 个场景、30 个样本用于提示词调优，剩余 40 个场景、120 个样本构成测试集，全部报告指标均在测试集上计算。每个样本包含对话历史、最终 JSON 工件、用户修订请求和人工核验的标准 JSON patch，用于检验模型能否同时完成直接修改与依赖驱动的级联修改。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**完成率（completion rate）**

衡量一个样本的修订是否被完整完成，是论文比较方法正确性的主指标；结果对测试集样本及五个随机种子取平均。所给节选未进一步明确其形式化判定公式，因此不应将其自行解释为普通的逐字段准确率。 （越高越好，因为更高的完成率表示更多修订请求及其必要传播被整体正确处理。）

</div>
<div class="metric-item" markdown="1">

**API 成本与成本效率**

API 成本衡量生成与选择所消耗的货币成本；本地模型按 OpenRouter 价格表估算。论文还用相对基线 $j+h$ 的性能增益除以额外成本比例，即 $\mathrm{gain}/(\mathrm{cost}/\mathrm{cost}_{j+h}-1)$，比较每单位新增成本带来的收益。 （在相同完成率下成本越低越好；成本效率则越高越好，因为它表示额外预算转化为更多正确样本的效率更高。）

</div>
<div class="metric-item" markdown="1">

**延迟与延迟效率**

延迟是每个样本从推理开始到取得答案的时间；延迟效率以 $\mathrm{gain}/(\mathrm{latency}/\mathrm{latency}_{j+h}-1)$ 衡量单位新增等待时间对应的性能收益。它区分了可并行执行的 med 与必须串行反思或再选择的方案。 （延迟越低越好，延迟效率越高越好；这反映交互式应用中响应速度与准确率的实际权衡。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 六个模型使用信息最完整的单次推理基线 $j+h$。

<div class="result-value" markdown="1">

完成率介于 68.3% 和 93.0% 之间，并整体呈现同一家族中更大模型表现更好的趋势。作者据此认为，仅扩大模型规模能够改善修订传播，但不同模型间仍有显著能力差异。

</div>

这说明即使把对话历史和最终工件都交给模型，任务仍未解决：最弱与最强系统之间相差较大，最强系统也没有达到满分。该比较支持“模型能力重要”，但由于模型架构、训练数据和推理实现并未被严格控制，不能把差异完全归因于参数量。

<div class="result-source" markdown="1">

来源：Section 4.1, Model comparison；Figure 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With the strongest baseline (j+h), for example, completion rates span 68.3–93.0%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 五次 LLM 调用下，将 Select、med、Reflect 及规则合并方法与单次 $j+h$ 基线比较。

<div class="result-value" markdown="1">

Select 相对 $j+h$ 提升 3.3–12.5 个百分点，在六个模型中的四个取得最高完成率、另外两个取得第二名；med 提升 1.8–7.7 个百分点，是次稳定的方法。作者的结论是，生成多个完整候选后再选一个候选，比逐叶节点进行简单规则合并更可靠。

</div>

Select 的优势表明多个样本通常各自发现了不同依赖，而额外的模型判断能够偏向修改更完整的候选；med 不需要额外的语义判断，也能通过避开离群候选获得稳定收益。不过这些数字对应固定调用数而非严格固定成本，尤其 Qwen 上 Select 会生成更多推理 token，因此不能仅凭该结果断言 Select 在所有预算下都最优。

<div class="result-source" markdown="1">

来源：Section 4.1, Method comparison；Figure 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Among the test-time compute methods, Select yields the most consistent improvement over j+h (+3.3–12.5%), achieving the highest completion rate on four of the six models and the second-highest on the remaining two.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 在五次调用下比较测试时计算方法的成本，并进一步对齐 Select 与其他方法的成本。

<div class="result-value" markdown="1">

GPT 模型中各方法的成本大致随调用数成比例增长；Qwen 模型上的 Select 成本达到 $j+h$ 的 5.7–7.5 倍，主要因为选择阶段产生更多推理 token。即便把其他方法的调用数增加到相近或更高成本，方法间的相对性能排序仍大体不变。

</div>

作者据此主张 Select 的准确率优势并非单纯来自花费更多预算，但也承认其绝对成本可能很高。成本对齐是比固定调用数更公平的比较，不过结果仍依赖论文采用的供应商价格与 token 计费方式；本地部署时的真实硬件成本不一定保持相同排序。

<div class="result-source" markdown="1">

来源：Section 4.2, Cost comparison under fixed LLM calls；Figure 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, for Qwen models, Select tends to incur higher costs than the other methods, increasing the cost by 5.7–7.5× over j+h.

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

- 单次推理基线 $j$、$h$ 与 $j+h$：模型分别只获得最终 JSON 工件、只获得对话历史，或同时获得两者。三者的控制变量清楚，可直接检验依赖信息是否隐藏在历史中，以及显式提供最终工件是否能减少 JSON 路径错误和漏改。
- 顺序反思 Reflect：从 $j+h$ 生成的 patch 开始，多轮检查并改写同一个答案。它代表把额外计算用于串行自我纠错，可与一次生成以及并行探索进行比较。
- 并行采样加规则选择：or、and、maj 分别在任一候选修改、全部候选一致、严格多数候选一致时采纳叶节点修改；med 则选择与其余候选在叶节点层面平均分歧最小的完整候选。该组方法检验不依赖额外 LLM 判断的候选聚合是否足以提高可靠性。
- 并行采样加 LLM 选择 Select：先使用 $j+h$ 并行生成多个 patch，再让同一 LLM 从候选中选出最终 patch。它与 med 的核心区别是使用模型推理判断候选完整性，而不是按候选间的形式相似度选择。

**实验想回答的问题**

- 在对话生成的 JSON 工件中，最终工件与对话历史分别提供了多少修订传播所需的信息；模型能否发现用户未直接点明、但因依赖关系必须同步修改的元素？
- 在增加推理时计算的条件下，顺序反思、并行候选的规则合并、中位样本选择和 LLM 选择，哪一种能在完成率、API 成本与推理延迟之间取得更好的权衡？

**实验实现**

共评估六个模型：gpt-oss-20b/120b、gpt-5.4-mini 和 qwen3.5-9b/27b/122b-a10b，均启用推理，GPT 模型的推理强度设为 medium。支持温度设置的模型使用 0.6，但 gpt-5.4-mini 除外；最大输出上下文为 32K tokens，本地模型通过 vLLM 部署在四张 NVIDIA A100 80GB GPU 上。每个测试样本以种子 $s\in\{0,42,84,126,168\}$ 重复五次。标准五调用配置中，Reflect 串行执行五次生成；并行方法使用种子 $s$ 至 $s+4$ 生成五个候选，而 Select 生成四个候选并额外进行一次 LLM 选择。成本曲线还扩展了调用数，以观察收益是否饱和；LiteLLM 缓存保证相同输入和种子产生相同输出。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 输入上下文消融：单次推理分别使用最终工件 $j$、对话历史 $h$ 和二者结合的 $j+h$。 | 所有模型均满足 $j<h<j+h$。例如，gpt-5.4-mini 的完成率依次为 90.7%、92.7%、93.0%，qwen3.5-122b 则为 81.7%、86.7%、90.3%。 | 从 $j$ 到 $h$ 的提升隔离出对话历史中依赖描述的价值：仅看最终状态无法可靠判断哪些字段应随局部请求变化。从 $h$ 到 $j+h$ 的进一步提升说明，历史虽原则上可重建最终工件，但显式给出当前 JSON 能降低重建负担及路径错误。该消融证明两类上下文具有互补性，但没有分别测量历史长度、无关轮次或依赖陈述位置的影响。 | Section 4.1, Importance of conversation history；Figure 4<br><span class="experiment-evidence">Across every model, the baselines follow a consistent performance ordering, j < h < j+h (e.g., 90.7% < 92.7% < 93.0% for gpt-5.4-mini and 81.7% < 86.7% < 90.3% for qwen3.5-122b).</span> |
| 测试时调用数消融：沿成本曲线增加并行样本数或反思轮数，并比较不同调用规模下的收益。 | 多数方法和模型在约四至五次调用时性能基本饱和；跨模型平均的最高成本效率由三次或四次调用的 Select，或三次调用的 med 获得。 | 这一分析隔离了“继续增加采样预算”本身的边际价值：初始少量候选可提高覆盖率，但超过四至五次后新增候选很少转化为更多完整修订。它支持采用少量并行采样，而不是无限扩大测试时计算；但论文没有在所给节选中报告每个曲线点的完整数值和置信检验。 | Section 4.2, Cost-performance scaling；Figure 6<br><span class="experiment-evidence">Figure 6 shows that performance largely saturates around four to five LLM calls for most methods and models.</span> |

**定性案例**

- 旅行日程场景展示了为何必须阅读对话：若用户把旅行开始日向后移动，仅看最终 JSON，无法知道后续活动日期应整体平移还是保持固定；只有历史中的“旅行开始后三天”等相对表述明确建立了依赖。该案例说明基准测试的不是机械字符串替换，而是从会话中恢复依赖并把局部修改传播到相关字段。它是任务合理性的定性示例，不构成方法优越性的统计证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces a benchmark and compares test-time sampling and reflection methods for evaluating dependency-aware revision propagation by LLMs.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`732e68e45d9e9399cac71d2ad72963fea5c81269f5a0eacac0bfe82be30b2e16`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
