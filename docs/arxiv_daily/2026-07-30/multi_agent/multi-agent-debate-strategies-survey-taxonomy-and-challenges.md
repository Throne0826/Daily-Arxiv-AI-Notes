---
title: "[论文解读] Multi-Agent Debate Strategies: Survey, Taxonomy, and Challenges"
description: "[arXiv 2607.26212][Multi-Agent] 本文通过对141项主要研究进行系统文献综述，建立覆盖辩论参与者、交互机制与共识协议的三维分类体系，以统一多智能体辩论的描述方式并揭示其尚未被充分比较的设计空间。"
arxiv_id: "2607.26212"
announcement_date: "2026-07-30"
primary_category: "multi_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:24.773712+00:00"
source_sha256: "5948204419712f527aaf6a9ac2b5a384548e88e3ef39ad7bcdbcbd4b85d71376"
tags:
  - "Multi-Agent"
  - "LLM 其他"
  - "多智能体辩论"
  - "大语言模型智能体"
  - "多智能体系统"
  - "系统文献综述"
  - "分类体系"
  - "交互机制"
  - "一致性协议"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">Multi-Agent · arXiv 2607.26212</p>

# Multi-Agent Debate Strategies: Survey, Taxonomy, and Challenges

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Quim Motger, Marc Oriol, Jordi Marco, Xavier Franch</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26212v1) · [PDF 下载](https://arxiv.org/pdf/2607.26212v1) · **关键词** 多智能体辩论, 大语言模型智能体, 多智能体系统, 系统文献综述, 分类体系, 交互机制, 一致性协议  


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

本文通过对141项主要研究进行系统文献综述，建立覆盖辩论参与者、交互机制与共识协议的三维分类体系，以统一多智能体辩论的描述方式并揭示其尚未被充分比较的设计空间。

**不用术语来说**：让多个大语言模型相互提出答案、指出错误并共同作出决定，有望在不增加领域专用训练数据的情况下提高结果的准确性与稳定性；但不同研究对“辩论”的含义、参与角色、交流过程和最终决策方式描述不一，导致研究者难以判断某种方法究竟为何有效，也难以公平复现和比较不同方案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 按照系统综述规范整理并分析141项多智能体辩论主要研究，结构化呈现其应用领域、任务类型与设计实践。
- 提出由参与者、交互和共识三个维度构成的分类体系，统一描述智能体角色与能力、信息交换过程以及最终结果的确定机制，并据此归纳开放挑战和研究机会。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型智能体与多智能体协作研究的交叉领域。单个LLM智能体通常通过“观察—推理—行动”循环，结合规划、记忆和工具使用来完成目标；多个智能体则可借助自然语言通信、角色分工与协同推理解决共享任务。多智能体辩论（Multi-Agent Debate，MAD）进一步要求智能体交换论点、相互批评并迭代修正答案，以期在不额外依赖领域语料、知识库或人类偏好标注的情况下提高准确性与鲁棒性。该研究关注的不是提出一种新的辩论算法，而是系统整理MAD系统中参与者、交互过程和最终决议的可配置设计要素。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**LLM智能体**

以大语言模型为核心的自主系统，能够读取上下文，并利用推理、规划、记忆或工具调用产生面向目标的行动。它通常在循环中持续观察环境反馈、更新判断并采取下一步行动。

</div>
<div class="conceptitem" markdown="1">

**LLM驱动的多智能体系统**

由多个LLM智能体组成的协作或竞争系统，各智能体可具有不同角色、能力和局部信息，并通过自然语言交流共同处理任务。其效果不仅取决于单个模型，也取决于通信拓扑、信息共享方式和协调协议。

</div>
<div class="conceptitem" markdown="1">

**多智能体辩论（MAD）**

多个LLM智能体提出答案或立场、交换论据、批评彼此输出，并经过若干轮交互形成最终结果的推理范式。这里的“辩论”既包括参与者如何配置，也包括信息如何传播以及最终如何达成一致。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文将跨应用领域的MAD研究作为系统文献综述对象：输入是按照系统综述流程识别并纳入的141项主要研究，分析单位是每项研究所采用的辩论配置及其应用任务；处理过程是提取并统一不同论文中分散或不一致的术语与设计属性；输出包括MAD研究版图，以及由“参与者—交互—协议”构成的三维分类体系，其中协议维度具体描述如何形成最终一致结果。研究假定MAD可被拆解为一组可比较的设计决策，并围绕四个问题考察应用领域与任务、参与者的角色和决策行为、通信与影响机制，以及最终结果的决议方式；它不直接以新的任务性能模型或训练目标为研究对象。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Smit et al. (2024)**: 该工作是较早的MAD综述，仅识别8项研究并提取6个设计特征，例如辩论轮数以及是否设置裁判或总结者。本文在其基础上扩大研究规模，并试图以系统化、跨领域的方式整合完整设计维度。
- **Oriol et al. (2025)**: 这是作者此前面向需求工程价值开展的初步系统映射，基于25项主要研究提出暂定分类体系与统一词汇。本文通过前向和后向滚雪球检索及改进的数据提取协议，对该基础进行扩展、细化与验证。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现有的大语言模型智能体仍会产生推理错误、不一致答案和不可靠决策。继续预训练、检索增强生成或基于人类偏好的对齐可以改善这些问题，但往往需要领域语料、知识库或人工偏好标注等额外资源。因此，研究界需要一种尽量不依赖新增领域数据、而能借助多个智能体相互批评和修正来提高准确性与鲁棒性的方案。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单体模型增强与适配方法**：提示方法通过少样本上下文学习、思维链、自一致性或树搜索激发模型已有能力；训练与知识增强方法则通过对齐、微调、持续预训练或检索增强生成，提高模型的目标遵循、领域适应和事实依据。
- **既有多智能体辩论综述与分类**：已有工作通常把辩论视为某类智能体交互机制，进行定性汇总或按少数通信模式分类；例如早期综述仅分析8项研究并提取6个设计特征，另有工作提出基于三种通信模式的扁平分类。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 模型适配、持续预训练、检索增强和偏好对齐通常依赖额外领域语料、人工整理的知识库或人类偏好标注，增加数据、维护和计算成本，因而不能直接解决“无新增领域数据时如何提升智能体可靠性”的需求。
- 已有MAD综述覆盖规模有限，或缺少清晰的系统综述协议；其分类通常只涉及轮数、特殊角色或通信模式等局部特征，没有完整刻画参与者、交互过程和结果裁决之间相互关联的设计决策，因而难以支持跨研究复现、受控比较和统一术语。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

在本文之前，尚无一项大规模、方法学严谨且跨应用领域的综合研究，能够系统整合MAD的核心设计维度与架构模式，并用统一框架描述不同方案。尤其缺少同时覆盖“谁参与并如何独立决策”“智能体之间如何通信和相互影响”以及“最终如何形成共识”三个环节的系统分类。

</div>
<div markdown="1"><span>核心问题</span>

本文集中回答四个相互衔接的问题：MAD研究应用于哪些领域和任务；辩论参与者的角色、能力与个体决策行为如何设计；通信、信息交换与影响关系如何组织；以及系统通过何种解决机制形成最终结果。

</div>
<div markdown="1"><span>作者直觉</span>

一次多智能体辩论并非单一算法，而是由参与角色、连接与交流方式、信息保留方式以及投票或裁判等多项选择共同构成。先把这些选择拆成统一、可组合的维度，再将141项研究映射到同一坐标系，就能区分哪些做法只是惯例、哪些替代方案尚未探索，并为后续逐项控制变量的基准测试提供基础。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文采用系统性文献综述（Systematic Literature Review, SLR），目标不是训练或提出一个新的多智能体辩论模型，而是从既有研究中归纳可复用的设计分类。方法遵循 Kitchenham 与 Charters 的 SLR 指南，并以 Wohlin 的前向、后向滚雪球法补充数据库检索。研究首先操作化定义多智能体辩论（MAD）的边界：至少两个 AI 智能体围绕同一自然语言任务进行多轮、可出现对立论点的实质讨论；单智能体自省、单向反馈、仅分工传递信息以及人类作为辩论参与者的情形均不纳入。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 界定研究对象与范围

作者将 MAD 操作化为两个或更多 AI 智能体针对同一自然语言任务开展多轮讨论，并允许提出相互对立的论点；同时明确排除单智能体反思、无双向讨论的反馈、仅进行子任务信息传递、非自然语言任务和人类参与辩论的系统。

<div class="method-step__io" markdown="1">

**输入**：文献中关于多智能体辩论的不一致定义，以及传统辩论和多智能体系统的相关概念。  
**输出**：可直接用于筛选文献的 MAD 定义、研究边界与纳入/排除标准。

</div>

**直观理解**：这一步相当于先规定什么才算“辩论”，避免把普通协作、流水线分工或自我检查误计为 MAD。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造精确检索并获得种子文献

作者使用检索式“(LLM OR ‘Large Language Model’ OR LLMS OR ‘Large Language Models’ OR ‘AI Agent’ OR ‘AI Agents’) AND (MAD OR ‘Multi-Agent Debate’)”，不限制领域和发表日期；检索有意强调精确率，而未加入噪声较大的宽泛词“debate”或“discussion”。

<div class="method-step__io" markdown="1">

**输入**：PICO 框架中的研究对象 Population（LLM 或 AI agent）和干预 Intervention（MAD），以及 Scopus 的题名、摘要和关键词索引。  
**输出**：29 篇候选文献，经纳入和排除标准筛选后形成11篇种子文献。

</div>

**直观理解**：数据库检索只负责找到一批可信的起点，而不是一次覆盖全部研究；遗漏的相关论文随后通过引用关系继续扩展。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 独立筛选与版本控制

筛选依次经过题名、摘要和全文三个层级，候选论文原则上由两位作者独立判断，分歧通过讨论达成共识；同一论文存在多个版本时选择最新 arXiv 版本，但若已有会议或期刊正式版本则优先选择正式版本。

<div class="method-step__io" markdown="1">

**输入**：数据库检索和后续滚雪球得到的候选论文，以及预先规定的 IC1、EC1—EC6 标准。  
**输出**：满足 MAD 定义、信息充分、英文全文可访问且没有重复或被取代版本的研究集合。

</div>

**直观理解**：双人独立判断用于降低个人偏差，版本规则则防止同一工作被重复计数或依据过时内容编码。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 前向与后向滚雪球扩展

作者各执行一轮后向滚雪球和前向滚雪球：前者沿参考文献寻找更早工作，后者沿引用关系寻找后续工作；所有候选项继续依据同一套纳入和排除标准筛选。

<div class="method-step__io" markdown="1">

**输入**：11篇种子论文及其参考文献、引用这些论文的后续研究。  
**输出**：后向滚雪球后得到23篇研究，前向滚雪球后最终得到141篇主要研究；作者报告所有筛选轮次的平均 Cohen’s kappa 为0.70。

</div>

**直观理解**：这类似从一组核心论文沿引用网络向前后各走一层，既补回检索词没有覆盖的研究，也纳入尚未被 Scopus 完整收录的及时 arXiv 工作。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文是系统性文献综述与分类研究，没有可训练模型、损失函数或参数优化目标；其方法学目标是依据明确协议最大化文献选择的可追踪性，并通过结构化特征抽取形成描述性分类，而非优化预测性能。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 研究边界与资格判定模块**

纳入标准 IC1 要求研究提出或使用至少一种满足操作化定义的 MAD 策略；排除标准覆盖策略细节不足、辩论并非完全发生于 AI 智能体之间、任务不是自然语言任务、非英文、全文不可访问以及重复或被取代版本。

> 直观理解：该模块保证综述比较的是同一种基本研究对象，否则把人机讨论、视觉分类或普通多智能体分工混入后，统计结果将失去统一含义。

**2. 检索—滚雪球互补模块**

Scopus 精确检索用于建立高质量种子集，一轮后向和一轮前向滚雪球则利用参考关系扩大召回范围。初检与后向滚雪球于2025年3月执行，前向滚雪球于2025年7月执行。

> 直观理解：精确检索减少人工筛选噪声，引用扩展弥补术语不统一造成的漏检；两者结合比单独依赖关键词更适合快速发展且命名尚未稳定的 MAD 领域。

**3. 分类编码模块**

作者从入选研究中抽取可描述 MAD 方法的代码，并按研究应用、参与者设计、辩论交互和协议达成方式组织。参与者进一步涉及 persona、功能角色和基础模型，协议达成则区分最终决定权 authority 与生成最终响应的 resolution 机制。

> 直观理解：这一模块把一套复杂辩论系统拆成可比较的设计选择；例如，最终答案由全体智能体共同决定还是由裁判决定，与具体采用投票、评分或论证评价是两个不同问题。

**训练与推理**

不适用传统机器学习中的训练与推理流程。本文的对应执行过程是：先确定 MAD 定义和范围，再在 Scopus 中检索并筛选种子论文，随后沿引用网络实施一轮双向滚雪球，最后对入选研究进行数据抽取和归纳编码。分类体系由文献中的实际设计反复归纳而成，并用于统计151种 MAD 配置的设计分布；原文节选未报告自动编码模型或自动分类器。

**复现信息**

公平解释该方法需要注意四点：第一，初始检索只覆盖 Scopus 的题名、摘要和关键词，并刻意以精确率优先，因此完整性依赖后续滚雪球；第二，滚雪球前向和后向均只执行一轮，时间截点分别为2025年3月和7月；第三，筛选通常由两位作者独立完成并协商分歧，但前向滚雪球的889篇去重候选先由一位作者初筛，排除367篇明显越界论文，余下522篇再接受双人评审；第四，统计单位并不始终等于论文数量，因为141篇主要研究对应151种不同 MAD 方法配置。完整的数据抽取数据据称位于复现包中，但所给原文节选未提供其具体 URL、编码表结构或编码一致性细节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- 系统性文献综述语料库：包含141项MAD主要研究。该语料库不是传统机器学习训练集，也没有训练、验证或测试划分；其作用是支持设计特征编码、分类体系归纳和研究趋势统计。当前节选未说明文献检索数据库、筛选流程、时间范围及各类别的完整计数。
- 协议形式化子集：在分析最终答案的解决机制时，仅统计实际形式化并实现了该过程的97种MAD方法，因此Resolution类别的百分比以n=97为分母，而不是以全部141项研究为分母。
- 应用与任务分类语料：作者按一般推理、数学、医学、软件工程、网络安全、社会科学、语言等领域整理纳入研究，并区分客观任务与开放式任务。该分类用于判断不同MAD设计和评价方式适用于什么任务，而非用于训练或直接比较某个模型的准确率。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**设计类别占比**

某一MAD设计选择在编码研究中出现的比例，例如最终决策权由集体或裁判掌握的比例。它衡量研究实践的普及程度，不衡量任务准确率或方法优越性。 （无统一的越高越好方向；较高只表示采用更普遍，也可能反映研究惯例或设计趋同。）

</div>
<div class="metricitem" markdown="1">

**任务准确率**

在GSM8K等具有明确标准答案的算术、数学或逻辑基准上，最终答案正确的样本比例。本文将其作为既有MAD研究常用的客观评价方式，但当前节选没有报告统一汇总分数。 （越高越好，因为表示更多问题被正确解决；但跨研究比较仍会受到模型、提示、智能体数量和交互协议差异的影响。）

</div>
<div class="metricitem" markdown="1">

**LLM-as-a-judge多维评分**

由语言模型充当评审，对开放式输出的连贯性、忠实性和对齐程度等维度进行评分。它使缺少唯一标准答案的任务可以被量化，但可能受到评审模型偏差、智能体迎合和偏见强化的影响。 （通常越高越好，但分数有效性取决于评审提示、评审模型及评分标尺；不能直接等同于人工认可或事实正确性。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 系统性综述的覆盖规模与分析框架

<div class="result-value" markdown="1">

作者分析了141项MAD主要研究，并据此提出由参与者、交互机制和共识协议构成的三维分类体系。

</div>

这一结果说明本文的主要产物是对MAD设计空间的结构化整理，而不是一个在标准基准上取得更高准确率的新算法。141项研究提供了较广的观察基础，但语料规模本身不能证明分类体系完整、互斥或具有因果解释力。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">We present a systematic literature review characterizing 141 primary studies on MAD.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨研究的MAD设计模式归纳

<div class="result-value" markdown="1">

作者发现，现有研究集中采用静态、全连接拓扑，逐字传递消息，使用短期记忆，并通过投票决定最终结果；其他可能的设计仍处于边缘位置。

</div>

这表明许多论文并未充分探索MAD的组合设计空间，主流配置可能更多来自惯例而非受控比较。因此，某一论文报告的收益不能自动归因于“辩论”本身，也可能来自拓扑、记忆、信息压缩或决策规则。该结论是对文献分布的描述，不证明主流配置性能更差，也不证明边缘配置一定更优。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Our analysis reveals that the field has implicitly converged on a narrow design pattern — static, fully connected topologies, verbatim exchange, short-term memory and voting resolution strategies — adopted by convention rather than systematic comparison, while promising alternatives remain marginal.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 辩论结束后的最终决策权配置

<div class="result-value" markdown="1">

集体决策是最常见的权威模式，占52.3%；裁判式决策占39.1%；混合模式和其他模式分别占4.0%与4.6%。

</div>

大多数系统要么聚合全体智能体的立场，要么交由专门裁判阅读辩论记录并作出最终判断。集体模式略占多数，尤其适合答案较客观的推理任务；裁判模式则便于综合开放式论证。占比仅反映文献采用频率，不能说明集体决策比裁判决策更准确。当前节选也未给出在相同任务、模型和成本下对四种模式的统一性能比较。

<div class="result-source" markdown="1">

来源：Section 6.1, Authority

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Collective (52.3%): This is the most frequent approach, where the final answer is an aggregation of the agents’ positions.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 本文报告的是跨论文的描述性频率，而非在统一模型、数据集、提示、智能体数量、轮数和预算下进行的受控基准测试。因此，类别占比只能说明研究惯例，不能证明某种拓扑、记忆或解决协议更有效。
- 当前节选未明确报告检索数据库、纳入与排除流程、编码者一致性、类别完整计数及开放式任务的统一质量标准；同时，依赖LLM-as-a-judge的原研究可能存在迎合与偏见强化风险。因而本文结论仍需结合完整论文及141项原始研究进行来源核查。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未设置统一的单智能体基线。作为系统性综述，本文比较的是既有研究的设计配置，而不是在同一数据集和模型条件下重跑单智能体与多智能体系统。
- 不同MAD配置可被视为描述性比较组，例如集体决策、裁判决策、混合决策和其他权威模式；但这些组来自不同论文与任务，不能当作受控实验中的性能基线。
- 任务评价方式形成另一组概念性对照：数学、逻辑和代码等任务通常有客观正确答案，而文本评价、法律推理、谈判和创意生成更多依赖LLM-as-a-judge或定性综合。该对照用于说明评价证据强弱，而非证明某类任务更适合MAD。

**实验想回答的问题**

- 141项主要研究中的多智能体辩论（MAD）被应用于哪些领域与任务，以及不同任务的可评价性有何差异？
- 现有MAD系统在参与者、交互机制与共识协议上采用了哪些设计，哪些配置已成为主流，哪些替代设计仍缺乏系统比较？

**实验实现**

本文是系统性文献综述与分类研究，而非统一重跑模型的基准实验。作者对141项主要研究进行特征提取，并从参与者、交互机制和共识协议三个维度构建MAD分类体系，再统计各设计选择的出现情况并按领域、任务和评价方式进行归纳。当前节选明确给出了部分权威模式占比，并说明解决机制的比例仅以实际形式化和实现该过程的97种方法为分母；但未提供检索式、文献筛选者人数、编码一致性、复核程序、完整统计表或可复现实验脚本，因此不能从节选重建完整综述流程。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 领域对照显示，MAD设计应随任务改变：知识密集或主观任务常利用异质人格扩大观点覆盖，医学场景借此缓解单一认知偏差；漏洞评估、钓鱼检测等安全关键任务则采用对抗式或红队协议主动寻找系统弱点。该观察说明分类体系可用于解释“为什么选择某种智能体配置”，但由于这些案例来自不同研究，不能据此建立异质人格或对抗协议提升性能的统一因果结论。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Surveys and systematizes LLM-based multi-agent debate participants, interaction mechanisms, and agreement protocols.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`5948204419712f527aaf6a9ac2b5a384548e88e3ef39ad7bcdbcbd4b85d71376`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
