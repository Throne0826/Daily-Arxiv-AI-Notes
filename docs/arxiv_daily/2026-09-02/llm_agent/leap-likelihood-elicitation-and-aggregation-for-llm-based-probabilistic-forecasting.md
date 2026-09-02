---
title: "[论文解读] LEAP: Likelihood Elicitation and Aggregation for LLM-based Probabilistic Forecasting"
description: "[arXiv 2609.01337][LLM Agent] 原文未明确报告。"
arxiv_id: "2609.01337"
announcement_date: "2026-09-02"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:54:41.765446+00:00"
source_sha256: "00acb2bae8b0f2afae23d09d47276996012fcbcfd4ea9dd0c4c9f4c0aa43abbe"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "大语言模型预测"
  - "概率预测"
  - "贝叶斯更新"
  - "证据级聚合"
  - "可审计性"
  - "概率校准"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2609.01337</p>

# LEAP: Likelihood Elicitation and Aggregation for LLM-based Probabilistic Forecasting

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Yufei Chen, Yiran Zhao, Xiaogang Xu, Qipeng Xie, Jiafei Wu, Zhe Liu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Shandong University Nanjing University of Aeronautics and Astronautics；Affiliation: School of Software Technology, Zhejiang University；Affiliation: Ningbo Global Innovation Center, Zhejiang University；Affiliation: The Hong Kong University of Science and Technology (Guangzhou)</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01337v1) · [PDF 下载](https://arxiv.org/pdf/2609.01337v1) · **关键词** 大语言模型预测, 概率预测, 贝叶斯更新, 证据级聚合, 可审计性, 概率校准<br>
**代码**: [https://github.com/layingfish/LEAP](https://github.com/layingfish/LEAP)

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

本文研究的是基于大语言模型（LLM）的概率预测：系统先通过搜索、检索或浏览收集与问题相关的证据，再根据这些证据预测经济、体育、地缘政治或其他现实事件的结果。传统系统通常让模型一次性阅读全部证据并直接生成答案，即“整体式预测”（Monolithic Prediction）；LEAP关注的是证据已经固定之后，如何把每条证据转换为可解释、可复现且经过概率校准的最终预测。其核心思想是让LLM分别解释单条证据，再由显式概率模型统一聚合，而不是让LLM在长上下文中隐式完成全部证据融合。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**概率预测与校准**

概率预测不仅给出最可能的答案，还为每个候选结果给出概率分布，例如某事件发生的概率。校准要求这些概率与长期实际频率相符：被赋予约$0.7$概率的事件应大致在$70\%$的情况下发生。

</div>
<div class="concept-item" markdown="1">

**贝叶斯更新**

贝叶斯更新以先验分布表示观察证据前对各结果的初始相信程度，再利用证据的似然逐步得到后验分布。直观地说，先验提供基础发生率，似然表示某条证据在不同结果下有多合理，后验则是结合证据后的信念。

</div>
<div class="concept-item" markdown="1">

**证据级可审计性**

证据级可审计性要求能够追踪每条证据如何影响最终预测，而不只是查看模型事后生成的解释。若移除某一证据并重新计算后验，用户应能观察到该证据对结果和不确定性的具体影响。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个预测任务、上游搜索或浏览代理收集的固定证据集合，以及由任务决定的输出类型，系统需要生成目标答案的概率分布。目标可以是连续数值、单选结果或多选结果；输出分别是相应的连续预测分布、候选类别上的概率分布，或多个候选事件的联合/边际概率表示。LEAP假设证据收集阶段已经完成，并在比较时向不同预测方法提供同一证据集合，从而隔离“如何利用证据进行最终预测”这一问题。它不要求LLM直接完成可靠的整体推理，而是令LLM逐条解释证据、产生似然参数，再由确定性的概率更新过程计算后验。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D$**

固定的证据集合；其中每个元素是一条由上游搜索、检索或浏览过程获得的证据。

</div>
<div class="notation-item" markdown="1">

**$d_i$**

证据集合$D$中的第$i$条证据，LEAP会单独分析它对目标结果的含义。

</div>
<div class="notation-item" markdown="1">

**$Y$**

预测目标或随机变量，表示需要预测的事件、类别或连续数值。

</div>
<div class="notation-item" markdown="1">

**$P(Y\mid D)$**

给定全部证据$D$后的后验预测分布，即系统最终输出的概率性预测。

</div>

</div>

**直接相关的工作**

- **LLM-based forecasting systems（包括AutoCast、ForecastBench和Prophet Arena等）**: 这些工作研究LLM结合搜索、检索、推理、集成或校准完成现实世界预测，但最终预测通常仍由读取全部已收集材料的LLM调用整体生成。LEAP不改变证据收集过程，而是将研究重点限定为固定证据如何被转换为最终概率分布。
- **BIRD、Nafar等人的LLM辅助贝叶斯推断，以及Bayesian Linguistic Forecaster**: 这些工作证明可以让LLM提供因素、条件概率或结构化信念，并将其放入概率模型中。LEAP的区别在于：它针对单个预测任务的固定检索证据，为每条证据 elicitation 一个似然参数，并在证据集合固定后统一计算后验，从而强调证据级贡献的可追踪性。

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

LEAP（Likelihood Elicitation and Aggregation for Probabilistic Forecasting）将预测阶段拆为两个相互分离的环节：首先，LLM分别阅读任务$T$与单个证据项$e_i$，为显式概率模型估计先验参数和似然参数；随后，确定性的共轭贝叶斯更新将这些局部参数与先验结合，输出任务要求格式的后验预测$f$。系统还通过依赖聚类、可靠性采样和连续值异常值剔除来降低重复证据、局部估计噪声及单位错误的影响，并使用留一法计算每项证据的可复现贡献$\Delta_j$。直观地说，传统方法让LLM把所有材料混在一起直接给答案，而LEAP让LLM逐条说明证据支持什么，再由一个固定的概率计算器统一汇总，因此每条证据如何改变结论更加透明。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 证据收集与表示

在ReAct式循环中，LLM根据当前消息生成推理文本和搜索或页面抓取调用；工具返回的页面或摘要被加入证据集$\mathcal{E}$，并记录时间戳及候选依赖键。循环在满足停止信号、证据数量要求、连续无新增证据或预算耗尽时终止。

<div class="method-step__io" markdown="1">

**输入**：任务描述$T$、工具注册表$\mathcal{T}$、轮数预算$B$、最少证据数$m$和停滞阈值$s$。<br>
**输出**：结构化证据集合$\mathcal{E}=\{e_1,\ldots,e_n\}$，每个证据项带有来源相关元数据。

</div>

**直观理解**：这一阶段相当于先做资料搜集：LLM决定查什么，工具负责取得材料，但此时还不要求LLM给最终概率。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 先验与局部似然 elicitation

一次无证据可见的调用估计先验$P_0(\theta)$的参数；随后对每个$e_i$单独调用LLM，依据任务输出类型产生似然参数和依赖键。连续目标提取证据暗示的目标值$\mu_i$并估计不确定性$\sigma_i$；单选目标产生各选项的未归一化似然$L_i(k)$；多选目标产生支持或反对各选项的对数似然比。

<div class="method-step__io" markdown="1">

**输入**：任务$T$以及先验调用所需的背景信息，或单个证据对$(T,e_i)$；局部调用不能看到其他证据、累计证据或部分后验。<br>
**输出**：先验参数、每个证据的似然参数及依赖键。

</div>

**直观理解**：LLM只回答“这一条材料分别支持哪些结果、支持有多强”，而不是直接把这一条材料当成完整答案；先验则表示看证据前的基准概率。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 安全筛选与证据去重

按共同来源或报告对证据进行依赖聚类，每组保留一个代表项，得到保留集合$\mathcal{R}\subseteq\{1,\ldots,n\}$；可对同一证据重复查询$R$次，并依据输出一致性缩小或保持局部似然强度。对于具有历史数据先验的连续任务，若$\mu_i$距离先验均值超过四个先验标准差，则剔除该项。

<div class="method-step__io" markdown="1">

**输入**：证据项的依赖键、重复采样结果、先验参数和连续目标的局部观测。<br>
**输出**：经过筛选的代表证据集合$\mathcal{R}$及调整后的局部似然参数。

</div>

**直观理解**：这一阶段防止把同一新闻的多次转载误算成多条独立证据，也防止一次不稳定或明显单位错误的LLM解读过度影响结果。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定性贝叶斯聚合与贡献分析

针对连续、单选和多选任务分别使用高斯、分类—多项式和独立伯努利共轭模型，执行闭式后验更新；从后验读取连续目标分位数、单选选项概率或多选伯努利边际概率。对每个$j\in\mathcal{R}$重新计算排除$j$后的后验，并将预测变化记为留一贡献$\Delta_j$。

<div class="method-step__io" markdown="1">

**输入**：先验参数、保留证据集合$\mathcal{R}$、各项似然参数、温度或全局似然强度$\eta$以及任务输出类型$\tau$。<br>
**输出**：最终预测$f$、后验分布及每项证据的可复现贡献$\Delta_j$。

</div>

**直观理解**：最后一步像一个固定的电子表格：它按同一套概率规则合并所有局部判断，不再调用LLM作最后裁决，因此相同输入应产生相同结果，并能检查删除某条证据后答案改变多少。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 先验—似然生成模型

$$
\theta\sim P_{0}(\theta),\qquad e_{i}\mid\theta\;\overset{\text{indep}}{\sim}\;P_{i}(e_{i}\mid\theta),\qquad i=1,\ldots,n
$$

**符号说明**

- $\theta$：预测目标的未知答案变量，例如连续数值、单选类别或多选中各项的真实状态。
- $P_0(\theta)$：在查看任何证据前对目标的先验分布，编码历史基准率或背景知识。
- $e_i$：第$i$条证据项。
- $P_i(e_i\mid\theta)$：在目标为$\theta$时观察到第$i$条证据的条件分布，即该证据对应的似然模型。
- $n$：原始证据项数量。
- $\overset{\text{indep}}{\sim}$：表示在给定$\theta$后，各证据项被假设为条件独立。

<div class="equation-explanation" markdown="1">

**直观理解**：该模型把预测拆成“一个看证据前的基准”与“每条证据在不同答案下有多可能”。条件独立假设使证据可以逐项组合，但共同来源证据可能违反它，所以LEAP先做依赖聚类。<br>
**原文位置**：第4.1节，公式(3)

</div>

</div>

<div class="equation-block" markdown="1">

#### 保留证据的贝叶斯后验更新

$$
P(\theta\mid\mathcal{E})\;\propto\;P_{0}(\theta)\prod_{i\in\mathcal{R}}P_{i}(e_{i}\mid\theta)
$$

**符号说明**

- $P(\theta\mid\mathcal{E})$：观察证据集合后的目标后验分布。
- $\mathcal{E}$：收集到的全部证据集合。
- $\mathcal{R}$：经过依赖聚类、可靠性调整和必要异常值剔除后实际参与聚合的证据索引集合。
- $\propto$：表示右侧给出未归一化后验，之后需通过归一化得到合法概率分布。

<div class="equation-explanation" markdown="1">

**直观理解**：后验等于基准先验乘以所有保留证据的支持程度。LEAP采用共轭分布，因此这个乘法更新有闭式结果，不需要额外的LLM调用或迭代优化。<br>
**原文位置**：第4.1节，公式(4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未报告LEAP进行参数训练或针对该方法优化的训练目标。该方法在推理时提示LLM估计先验和逐条证据的似然参数，随后由确定性的共轭贝叶斯更新生成预测；因此这里不适用基于损失函数的端到端训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 按证据项隔离的参数估计**

LEAP要求每次证据级调用仅接收$(T,e_i)$，输出适配任务类型的结构化似然模式，而不是对$\theta$的后验预测。连续任务把显式数值或定性判断映射为似然均值和标准差；单选任务把支持标签映射为$L_i(k)=P(e_i\mid\theta=k)$；多选任务把支持与反对标签映射为对数似然比。

> 直观理解：隔离输入可以保留证据的局部含义：模型不会因为先看了其他材料而把不同来源的判断混在一起，也不会在每一条证据上重复使用已经形成的结论。

**2. 共轭概率模型与闭式聚合**

LEAP假设先验为$P_0(\theta)$，且在给定目标$\theta$后各证据条件独立；为三类输出分别选择高斯、分类—多项式和独立伯努利共轭对，使后验可以闭式计算。实验中还使用温度和角色权重的 tempered update；当温度与权重均为单位值时退化为基本贝叶斯更新。

> 直观理解：LLM只负责把自然语言证据翻译成概率模型所需的局部参数，最终组合由可检查的数学规则完成，避免让LLM凭整体印象直接压缩不确定性。

**3. 稳健性保护与可解释输出**

依赖聚类根据证据返回的依赖键保留共同来源的代表项；可靠性采样对同一局部查询重复$R$次，并依据一致性调整似然幅度；连续任务可用先验作为数值锚点进行异常值剔除。聚合后通过留一法计算$\Delta_j$，从而分解单项证据对最终预测的影响。

> 直观理解：这些机制分别回答“重复报道是否被重复计数”“LLM这次解读是否稳定”和“哪条材料真正改变了答案”三个实际问题。

**训练与推理**

方法不需要重新训练基础模型。推理时，证据收集循环先从任务$T$构造$\mathcal{E}$；先验调用在无具体证据条件下生成$P_0$参数，证据级调用分别处理$(T,e_i)$并生成$P_i$参数；系统再进行依赖聚类、可靠性调整和连续值异常筛除，使用保留集合$\mathcal{R}$执行闭式后验更新，最后按$\tau$读取预测$f$。对于连续目标，输出后验分位数；对于单选目标，输出归一化选项概率；对于多选目标，输出各选项的伯努利边际概率。为解释结果，系统逐项排除证据并重新更新，得到$\Delta_j$；外部CLI框架场景则直接把框架完成的轨迹规范化为同一种证据表示，再运行完全相同的elicitation与聚合流程。

**复现信息**

复现或公平解读结果所需的关键设置包括：证据级调用必须严格隔离为任务与单项证据，并使用结构化JSON模式；先验不得读取具体证据，否则会在后验乘法中重复计算同一信息；三类预测分别使用高斯、分类—多项式和独立伯努利共轭对。依赖键用于共同来源聚类，可靠性采样可将同一局部查询重复$R$次，连续任务的四个先验标准差异常值规则仅适用于由历史数据得到的先验；全局似然强度默认设为$\eta=1.0$。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- FutureX：初始选取 160 个任务，移除不支持的排序题后保留 157 个；包含原生单选、多选和连续预测任务，用于真实预测场景评测。冻结时间 $t_{\mathrm{freeze}}$ 使用原始问题时间。
- GAIA：从 103 个信息寻求任务候选中，经结构化改写和人工审核保留 99 个；开放式问题被改写为单选、多选或连续目标，用于测试在信息寻求场景中将答案转化为概率预测的能力。其 $t_{\mathrm{freeze}}$ 来自构建时的基准快照，表示检索截止时间而非真实预测截止时间。
- BrowseComp：从 100 个浏览任务候选中抽样，经审核保留 91 个；短答案浏览题被改写为带合理干扰项的单选题，用于测试浏览辅助问答中的概率化预测。三者合计形成 347 个任务，包括 266 个单选、29 个多选和 52 个连续任务；原文未提供传统训练集、验证集和测试集划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**FutureX composite score**

FutureX 定义的综合评分，用作覆盖所有输出类型的主指标；原文摘录未给出其具体公式。 （越高越好，因为它是论文报告的主综合性能指标；具体分值含义应以 FutureX 的评分规则为准。）

</div>
<div class="metric-item" markdown="1">

**Brier score 与 Spherical score**

用于离散任务的概率预测评价：Brier score 衡量预测概率与真实结果之间的平方误差，Spherical score 衡量预测概率向量与真实结果之间的方向性匹配；原文摘录未给出本文采用的完整公式。 （Brier score 越低越好；Spherical score 通常越高越好。二者分别从误差和概率分布匹配角度检验离散概率预测。）

</div>
<div class="metric-item" markdown="1">

**NCRPS**

连续任务使用的长度归一化连续排序概率得分，是连续排序概率得分的归一化变体，用于评价连续预测分布；原文摘录未给出归一化公式。 （越低越好，因为它衡量预测分布与真实连续结果之间的距离。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Monolithic Prediction：将全部收集到的证据一次性提供给语言模型，并要求其直接产生最终预测；它是 LEAP 的核心基线，因为两种方法共享同一证据集，主要差别是证据如何进入预测阶段。
- 不同基础模型上的 Monolithic 与 LEAP 对照：DeepSeek-V3.2、Gemini-3.1-Flash-Lite、Claude-Haiku-4.5、GPT-5.4-mini 和 Grok-4.20-Fast；该设置检验结论是否依赖某一个模型。
- 外部智能体框架中的原始轨迹与 LEAP 概率技能：DeerFlow、Hermes、OpenClaw 和 MiroFlow；该比较检验 LEAP 能否附加到未经修改的外部智能体轨迹，而不只是适用于作者自建的 ReAct 式循环。
- 受控比较中的先验访问、推理预算和聚合方式：原文摘录说明这些因素被单独控制，但未提供具体基线名称、设置定义或数值结果。

**实验想回答的问题**

- 在为每种方法提供完全相同的证据集 $\mathcal{E}$、相同时间截断和相同基础模型的条件下，LEAP 是否比 Monolithic Prediction 更能提升预测准确性与概率校准？
- LEAP 的优势是否能够跨不同基础模型、外部智能体框架、输出类型以及先验访问、推理预算和聚合方式等受控条件保持稳定？

**实验实现**

所有方法对每个任务使用同一证据集 $\mathcal{E}$。为避免证据泄漏，检索材料不得晚于任务的 $t_{\mathrm{freeze}}$，且基础模型的知识截止时间早于被评测时间。作者在自建 ReAct 式循环中评测五个基础模型，并在四个外部 CLI 智能体框架的未修改轨迹上应用 LEAP。固定设置包括证据收集预算 $B=10$ 轮、研究预算 6、每轮最多 4 次工具调用、一次思考样本、LEAP 温度 $\eta=1.0$、最多 6 条证据进入似然阶段、每个任务最多 60 次似然调用，以及每条证据 10 次可靠性采样。未进行超参数搜索；这些值和映射常数在最终评测前固定。每个模型—方法单元格在 $N=5$ 个随机种子下独立运行并取均值。作者还在固定的 60 任务分层诊断子集上分析校准、不同提前期的稳健性和组件消融，使用 GPT-5.4-mini 作为基础模型。原文摘录说明时间泄漏审计未发现截止时间违规或疑似泄漏，但未提供完整主结果表、数值表或各受控比较的具体配置。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向搜索与浏览型 LLM Agent 的逐证据似然提取和确定性概率聚合方法，以改善预测与校准。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`00acb2bae8b0f2afae23d09d47276996012fcbcfd4ea9dd0c4c9f4c0aa43abbe`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
