---
title: "[论文解读] Social Chain of Thought: A Multi-Agent Architecture Grounded in Medical Differential Diagnosis Methodology"
description: "[arXiv 2608.11420][Multi-Agent] 本文提出社会思维链（SCoT），以动态生成、角色条件化的医学专家智能体开展多轮协商，并检验这种社会化推理结构能否在复杂鉴别诊断中获得单体推理扩展难以复现的召回优势。"
arxiv_id: "2608.11420"
announcement_date: "2026-08-13"
primary_category: "multi_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:52:07.487124+00:00"
source_sha256: "d38084bde70fc536680fd10838736a11947a4db2e97ff4aca59bac80c0977e38"
tags:
  - "Multi-Agent"
  - "LLM Reasoning"
  - "Social Chain of Thought"
  - "医疗鉴别诊断"
  - "多智能体推理"
  - "大语言模型"
  - "角色条件化"
  - "协作式审议"
  - "推理透明性"
  - "Open-XDDx"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">Multi-Agent · arXiv 2608.11420</p>

# Social Chain of Thought: A Multi-Agent Architecture Grounded in Medical Differential Diagnosis Methodology

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Del Coburn, Scott Sanner, Dan Silver</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11420v1) · [PDF 下载](https://arxiv.org/pdf/2608.11420v1) · **关键词** Social Chain of Thought, 医疗鉴别诊断, 多智能体推理, 大语言模型, 角色条件化, 协作式审议, 推理透明性, Open-XDDx<br>


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

本文提出社会思维链（SCoT），以动态生成、角色条件化的医学专家智能体开展多轮协商，并检验这种社会化推理结构能否在复杂鉴别诊断中获得单体推理扩展难以复现的召回优势。

**不用术语来说**：面对症状复杂的病例，模型容易沿着单一思路过早锁定少数疾病，从而漏掉真正诊断；即使让同一个模型思考更久、生成更多答案或自我检查，其判断仍可能重复原有偏差。医疗问答直接关系用户健康，因此研究者需要一种既能扩大候选诊断范围、又能让推理过程更容易追踪的协作机制。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出SCoT多智能体鉴别诊断框架：根据具体病例动态生成五名相关医学专家，通过角色条件化形成不同专业视角，并在七轮流程中协商得到最终鉴别诊断。
- 将SCoT与单智能体基线、单智能体流水线消融及best-of-$n$扩展进行对照，用于区分性能提升究竟来自更多推理计算，还是来自多角色、多轮互动所提供的社会化结构；作者据此主张，SCoT的召回优势不能由单体推理扩展单独复现。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型医疗推理与多智能体协作的交叉领域，研究对象是复杂病例的鉴别诊断：系统不能只给出一个最可能疾病，而应综合症状、体征等病例信息，形成包含多个候选疾病的诊断列表。该任务既要求覆盖真实诊断，也要求推理过程可追踪；尤其在病例涉及多个专科时，单一模型的一次性判断或自我复核可能反复继承同一生成来源的偏差。论文因此把多智能体交互视为一种结构化推理扩展：由具有不同专科角色的智能体多轮讨论，使不同视角能够提出、质疑并修正候选诊断。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**鉴别诊断（Differential Diagnosis）**

医生依据病例信息提出若干可能疾病，并通过证据比较逐步缩小范围的临床推理过程。本文的目标输出是候选诊断列表，因此关键不只是首选诊断是否正确，还包括真实疾病能否被候选集合覆盖。

</div>
<div class="concept-item" markdown="1">

**多智能体推理（Multi-Agent Reasoning）**

多个由大语言模型驱动的智能体分别生成观点，并通过讨论、评议或整合共同完成任务。本文中的智能体被赋予不同医学专科角色，以产生有组织的推理差异，而不是简单重复同一种回答。

</div>
<div class="concept-item" markdown="1">

**内生性与相关偏差（Endogeneity and Correlation Bias）**

同一模型生成答案后再评价自身答案时，评价过程可能继承生成过程中的偏好和错误，使多次推理并不真正独立。本文认为，仅增加思考轮次或计算量未必能消除这种相关性，因此通过角色条件化引入异质视角。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一则具有复杂症状表现的医疗病例；系统使用同一个大语言模型后端，先根据病例动态生成五名相关医学专科角色，再让这些角色在七轮流程中进行协作式讨论，最终输出鉴别诊断。实验场景采用医生整理的 Open-XDDx 基准，并跨多个模型家族运行该流程。论文的核心假设是：即使共享模型后端，专科角色条件化和多轮社会性交互仍能使错误更少相关、增加真实诊断被候选列表召回的机会，并留下比单体推理更容易追踪的讨论记录；不过作者也明确承认，共享后端并不能彻底消除内生性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Zhou et al. (2025) 的医疗鉴别诊断双重 Chain-of-Thought 推理**: SCoT直接扩展这一面向医疗鉴别诊断的双重推理设置，将单体的再次思考改造成由动态生成的专科角色参与的多轮协作流程，并沿用其医生整理的 Open-XDDx 基准。
- **ChatEval（Chan et al., 2024）**: ChatEval同样让具有差异化角色的智能体先独立评价对象，再通过团队机制形成判断；SCoT借鉴这种多角色审议思想，但将应用目标改为复杂医疗病例的鉴别诊断与候选疾病整合。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

全球大量用户已经使用大语言模型处理健康问题，而复杂病例通常需要综合多个专科的知识与判断。若系统只给出一条狭窄的推理路径，就可能遗漏真实疾病；同时，医疗场景的高风险性要求系统不仅提高诊断覆盖率，还应展示不同判断如何被提出、质疑和整合，以便人类理解结论形成过程。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单模型思维链与迭代推理扩展**：让同一个模型生成逐步推理、再次思考或执行多次推理，以增加用于求解病例的计算量；论文所承接的直接工作是Zhou等人用于医学鉴别诊断的双重推理式思维链。
- **多智能体医学诊断**：配置多个智能体，使其分别分析病例并通过讨论、汇总或投票形成诊断。相关研究表明多智能体协作可用于医疗推理，但既有结果尚未充分解释其优势出现的条件及其相对单体推理扩展的独立作用。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 同一模型对自身输出进行评价会继承生成阶段的相关性偏差，即论文所称的内生性问题；单纯增加参数、推理时长或重复采样可能只是反复探索相近路径，因而仍会系统性漏掉某些诊断。
- 既有多智能体工作尚未清楚回答何时需要协作、协作为什么有效，以及它在哪些病例上真正优于单体推理。若缺少单智能体流水线和best-of-$n$等控制比较，就无法判断收益来自交互结构，还是仅来自更多调用次数与计算量。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有证据尚不能把“社会化协商带来的收益”与“增加推理次数带来的收益”明确分离，也缺少对收益分布的条件性分析，尤其是不清楚多轮专家互动是否主要帮助最困难、最容易漏诊的病例，以及角色差异能否在共享同一模型后端时产生足以改善诊断覆盖的推理多样性。

</div>
<div markdown="1"><span>核心问题</span>

在医学鉴别诊断中，将同一大语言模型组织为多个动态生成、角色条件化的专科智能体并进行多轮协商，是否能比单智能体、等流程单智能体消融和best-of-$n$单体扩展更可靠地找回真实诊断；这种优势又是否集中出现在高难度病例中？

</div>
<div markdown="1"><span>作者直觉</span>

不同专科角色会把注意力引向不同症状、病因和候选疾病，相当于主动制造若干不完全相同的推理入口；多轮讨论再让这些角色相互补充和纠错，使早期被忽视的诊断有机会重新进入候选集合。通俗地说，这并非只让一个医生把同一份病历多看几遍，而是让具有不同专业关注点的医生共同会诊。作者同时承认，共享同一模型后端并不能彻底消除内生性，因此这里的异质性主要来自角色提示与互动结构，而非真正独立的模型知识来源。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SCoT（Social Chain of Thought）是一个仅在推理阶段运行的医学鉴别诊断多智能体流水线。输入是一则临床病例描述；后端大语言模型先按病例内容生成五名具有不同专科身份的智能体，再让它们分别完成病例相关性判断、症状分诊和独立鉴别诊断。系统随后合并并去重候选疾病，通过三轮结构化质疑与回应修正各智能体的立场，最后结合响应质量启发式权重与 Borda 排序汇总出有序鉴别诊断，并额外检查是否遗漏危急疾病。输出不是单一诊断，而是一份按可能性排列、兼顾常见病与“不能漏诊”疾病的候选列表。

其核心设计不是简单地对同一提示重复采样，而是有意制造“观点差异，再形成共识”：专科人格使同一病例从不同医学角度被解释，独立提案扩大候选空间，公开质疑迫使智能体说明证据或更新判断，投票则压缩讨论产生的噪声。通俗地说，它模拟一次结构化多学科会诊：先让不同医生各自看病，再把所有怀疑对象写到同一块白板上，互相追问和纠错，最后综合排序，并在结束前专门确认有没有漏掉会造成严重后果的疾病。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 病例条件化的专科团队生成

后端模型根据病例动态生成五名智能体，并为每名智能体分配与病例相关且彼此不同的医学专科人格；默认团队包含两名较高温度的“创新型”专家和三名较低温度的“保守型”专家。该生成过程不依赖 Open-XDDx 的固定专科标签，因此原则上可以接受其他来源的临床文本。

<div class="method-step__io" markdown="1">

**输入**：一条来自 Open-XDDx 的临床病例描述，以及选定的后端大语言模型。<br>
**输出**：一个由五名病例相关专科智能体组成的团队，以及每名智能体的角色条件和采样温度。

</div>

**直观理解**：系统不是预先固定五个科室，而是先读病例，再决定应该请哪些医生会诊。不同人格负责提供知识视角差异，不同温度只是在生成行为上调节探索性与稳定性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 专科评估、症状分诊与独立鉴别诊断

第 1 轮要求每名智能体从本专科角度评估病例，并自评其专科与病例的相关程度；第 2 轮让所有智能体执行症状管理与分诊，优先考虑明显或危及生命、需要先处理的问题；第 3 轮再将任务严格转向诊断，每名智能体独立输出按可能性组织的候选诊断。

<div class="method-step__io" markdown="1">

**输入**：原始病例和已生成的专科团队。<br>
**输出**：各专家的相关性判断、初步处置意见，以及相互独立的专科鉴别诊断列表。

</div>

**直观理解**：这一步把“先处理眼前危险”和“判断病因”分开，避免一开始就只追逐某个诊断。专家先各自作答也能减少过早互相影响，使较少见但合理的候选有机会进入讨论。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选诊断主列表构建

第 4 轮汇总所有专家提出的疾病名称，执行去重，并形成一个暂不排序的主列表；该列表被发送给全部专家，作为后续讨论的共享候选空间。这里的目标是保留团队覆盖到的候选，而不是立即用多数意见淘汰低频诊断。

<div class="method-step__io" markdown="1">

**输入**：五名专家各自给出的鉴别诊断列表。<br>
**输出**：一份无重复、无初始全局排序的候选诊断主列表。

</div>

**直观理解**：可以把它理解为把每位医生写下的疾病贴到同一块白板上，同名疾病只保留一次。先不排序，是为了防止早期多数意见让少数专家发现的重要疾病过早消失。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 三阶段结构化精炼与相互质疑

第 5 轮包含三个子轮：专家先对每个候选标记支持、质疑或中立，并分别给出证据或理由；随后必须质疑他人的某项诊断、补充可能遗漏的诊断、提出针对性问题，或指出相互矛盾的证据；最后，被质疑者逐项回应，依据反证选择维持、辩护或更新立场，并明确说明哪些判断发生了变化。

<div class="method-step__io" markdown="1">

**输入**：候选诊断主列表、原始病例，以及各专家此前的判断和证据。<br>
**输出**：经交叉审查后的候选集合、每名专家的最终立场，以及支持、反对和立场更新记录。

</div>

**直观理解**：普通的多次生成只会得到许多答案，这一步则要求答案彼此发生作用。它类似会诊中的追问环节：医生不能只说“我不同意”，还要指出依据，而原提议者也必须明确说明是否被说服。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 诊断洞察分数

$$
\mathrm{Insight}=3n+2\bar{e}
$$

**符号说明**

- $\mathrm{Insight}$：某名专家的诊断洞察启发式分数，用于 Borda 汇总前的可信度加权。
- $n$：该专家跨全部讨论轮次提出的不同诊断数量。
- $\bar{e}$：该专家对每个所提诊断平均提供的证据条目数量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式同时奖励候选覆盖和证据深度：每多提出一种不同诊断增加 3 分，每个诊断的平均证据条目增加 1 时再增加 2 分。它是人工设计的响应质量启发式，而不是从临床结局学习得到的概率，也不能直接解释为专家正确率。<br>
**原文位置**：附录 F.1，Credibility Weighting Prior to Borda Counting，Component scores

</div>

</div>

<div class="equation-block" markdown="1">

#### 诊断覆盖广度分数

$$
\mathrm{Breadth}=4n
$$

**符号说明**

- $\mathrm{Breadth}$：某名专家考虑不同诊断范围的覆盖广度启发式分数。
- $n$：该专家跨讨论轮次提出的不同诊断数量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式只按不同候选的数量奖励搜索范围，每增加一种不同诊断就增加 4 分，不考虑其证据是否充分。它与洞察分数配合使用，但两者都依赖 $n$，因此可能重复偏好候选较多的回答；原文节选没有给出完整权重归一化过程，不能进一步断言其实际影响大小。<br>
**原文位置**：附录 F.1，Credibility Weighting Prior to Borda Counting，Component scores

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。SCoT 是推理时编排方法，原文没有报告对后端模型进行微调、梯度更新、强化学习或使用病例标签优化参数；Open-XDDx 的医师标注诊断用于评测输出，而不是作为流水线训练目标。附录中的洞察、广度和可行动性分数是投票前的人工启发式可信度信号，不应误称为可微训练损失；由于所给节选未完整展示可行动性公式和最终权重组合，也不能把这些分数重构为未报告的统一目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 动态专科人格与异质性控制**

系统由同一个后端模型实例化病例相关的不同专科人格，以人格条件化产生知识关注点上的异质性；默认五人团队中，两名创新型专家使用温度 $T=0.7$，三名保守型专家使用温度 $T=0.3$。作者还通过固定温度条件下的错误相关性分析区分人格差异与纯采样随机性，但人格并不等同于经过独立医学训练的不同模型。

> 直观理解：该模块试图让团队成员犯不同的错、看到不同的线索，而不是让五个几乎相同的回答简单投票。需要注意的是，所有角色仍可能共享同一后端模型的知识盲点，所以“专科身份”是提示条件，不代表真实执业资质或独立知识库。

**2. Delphi 式结构化讨论**

精炼与共识阶段借鉴临床 Delphi 方法：先独立提出意见，再接收群体层面的候选和反馈，经过迭代回应后形成共识。SCoT 将自由对话约束为支持、质疑、中立、交叉挑战和立场更新等明确动作，使系统能够记录意见如何因证据而变化。

> 直观理解：自由聊天容易重复观点或顺从最先出现的答案；固定讨论动作让每名专家都必须检查候选、提出异议并回应异议。它要解决的不是“生成更多文字”，而是让不同判断经过可追踪的碰撞后再汇总。

**3. 响应质量加权的 Borda 共识与安全复核**

每名专家先给出完整相对排名，系统再以诊断洞察、覆盖广度和可行动性三个启发式分量调整其贡献，最后使用 Borda 计数合成团队排序。该机制之后还保留独立的“Can’t Miss”轮次，使低概率但高危的疾病不完全受总体可能性排序支配。

> 直观理解：Borda 计数利用所有候选的名次信息，比只统计第一名保留了更多会诊意见；质量权重试图降低内容贫乏答案的影响。安全复核则承认“最可能”与“最不能漏掉”是两个不同问题，后者需要单独检查。

**训练与推理**

完整过程属于测试时推理。对每个病例，系统先调用后端模型生成五个专科角色；各角色依次经过专科相关性评估、症状分诊、独立鉴别诊断、共享主列表、三子轮精炼、最终排名和危急疾病复核。前几轮扩大候选诊断空间，中间的辩论轮根据证据纠正或保留意见，后续使用响应派生启发式权重和 Borda 计数压缩为最终排序。系统没有跨病例更新模型参数，也没有像 MACD 那样保存真实临床数据供未来病例自我改进。

实验中的单智能体流水线消融让一个经专科人格条件化的智能体独自走完相同七轮，用于判断收益来自流程结构还是多智能体异质性；标准单智能体基线则只接收病例并直接生成有序鉴别诊断。Best-of-$n$ 对照对同一病例重复调用后端模型：主要计算匹配设置令 Qwen-2.5-32B 执行 $n=35$ 次推理并以多数票聚合，另有使用 Qwen-2.5-32B 充当裁判的 $n=35$ 条件。三智能体消融保留相同流程，但改为一名创新型和两名保守型专家，从而把主要变化限制为团队人数。

**复现信息**

公平解释结果所需的主要设置如下：核心评测使用 Open-XDDx 的 570 条医师标注病例；每例真实诊断数量为 2 至 7 个，任务输出是有序鉴别诊断而非单一类别。默认团队规模为五人，正文第 5.3 节称创新型与保守型温度分别为 $0.7$ 和 $0.3$；但附录表 4 将默认温度组合列为 Qwen-2.5-32B 的 $T=0.20/0.45/0.60$ 和 Gemma-4 MoE 的 $T=0.20/0.60$，两处表述存在需要对照代码或完整附录核验的不一致。

后端覆盖 Qwen-2.5 的 1.5B、3B 和 32B 版本，Gemma-4 MoE 与 dense 版本，以及 GPT-5-4 Nano、Claude Haiku 4.5 和 Claude Sonnet 4.6。多数模型至少在单智能体基线与五智能体 SCoT 条件下完整运行一次 570 例数据；正文声称 Claude 模型各条件只作 100 次探索性比较，但附录表 2 又将 Haiku 基线的样本量列为 570、SCoT 列为 100，因此跨模型比较必须同时检查每一行的样本量。Qwen-2.5-32B 用于团队规模、单智能体流水线和 Best-of-$n$ 消融；温度扫描则在 Qwen-2.5-32B 与 Gemma-4-MoE-26B 上覆盖全部 570 例。原文节选没有提供精确提示模板、候选名称规范化规则、Borda 分值定义、三项可信度分数的完整组合方式或“Can’t Miss”候选如何并入最终列表，这些均是严格复现前需要从完整论文附录或代码确认的关键缺口。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Open-XDDx：医学鉴别诊断评测集，完整评测包含 570 个病例，用于比较单智能体基线、SCoT、多轮单智能体管线以及 best-of-$n$ 重复采样。Claude 与 Gemma-dense 的跨模型探索性实验仅使用其中 100 个病例；原文节选未说明数据划分方式、病例来源及标签构造过程。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**宏平均召回率（macro recall）**

衡量各病例真实诊断项被预测鉴别诊断覆盖的程度，并先按病例计算后汇总，使病例规模差异不至于主导结果。该指标特别对应论文所强调的“不要漏掉正确诊断”。 （越高越好，因为更高的召回率表示真实诊断被遗漏得更少；但它可能通过加入大量候选项换取，因此必须结合精确率判断。）

</div>
<div class="metric-item" markdown="1">

**精确率（precision）**

衡量模型提出的诊断项中有多少属于真实诊断，用于识别模型是否通过无差别扩张鉴别诊断列表来提高召回率。 （越高越好，因为更高的精确率表示错误候选更少；但过度删减候选可能提高精确率并损害召回率。）

</div>
<div class="metric-item" markdown="1">

**F1**

精确率与召回率的调和平均，用于概括“覆盖真实诊断”和“控制错误候选”之间的平衡。难度分层实验以单智能体基线的病例级 F1 定义从最难到最易的四分位组。 （越高越好，因为只有精确率和召回率同时较好时，F1 才会较高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨后端模型的 baseline 与 SCoT $N=5$ 比较

<div class="result-value" markdown="1">

除 Qwen-2.5-1.5B 外，SCoT 在各后端上将召回率提高 4 至 12 个百分点左右；Qwen-2.5-3B 相对其单智能体基线提高 11.8 个百分点，而 Qwen-2.5-1.5B 下降 3.7 个百分点。作者据此把该组模型上的可行性门槛定位在 1.5B 与 3B 参数之间。

</div>

作者结论是，多智能体审议通常能补回单体模型遗漏的真实诊断，但前提是每个智能体已有足够的医学知识和纠错能力。通俗地说，多人讨论只有在参与者能识别并反驳较弱建议时才有帮助。该结果支持“存在能力门槛”，但不能证明参数量本身是因果因素，因为比较还涉及具体模型、训练数据和架构，而且部分后端只评测了 100 例。

<div class="result-source" markdown="1">

来源：第 6.1 节，Figure 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The Qwen-2.5 size tests indicate that the SCoT viability threshold falls between 1.5B and 3B parameters: Qwen-2.5-1.5B degrades under SCoT, while Qwen-2.5-3B gains 11.8 recall points over its single-agent baseline.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen-2.5-32B 上的 SCoT $N=5$ 与单体重复采样比较，570 个病例

<div class="result-value" markdown="1">

SCoT $N=5$ 的召回率、精确率和 F1 分别为 0.607、0.509 和 0.531。Best-of-35 分别为 0.537、0.403 和 0.454；加入 judge 后分别为 0.499、0.447 和 0.465。因而，增加独立采样次数或再加裁判均未复现 SCoT 的召回优势。

</div>

作者将此解释为：关键不只是消耗更多推理计算，而是让不同专科视角先产生互补候选，再通过互动进行修订和筛选。尤其是 judge 虽提高了 best-of-35 的精确率与 F1，却进一步降低召回率，说明后处理选择器不等价于讨论过程。不过，这一对照仍不能单独证明收益来自真实的“社会推理”；它证明的是，在给定模型和协议下，所测试的重复采样方案不足以解释 SCoT 的结果。

<div class="result-source" markdown="1">

来源：第 6.2 节，Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With 35 samples, repeated inference achieved a recall of 0.537, precision of 0.403, and an F1 of 0.454. Adding a judge is negligible, decreasing recall to 0.499, while increasing precision to 0.447, and F1 to 0.465.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 按单智能体基线难度分层的 SCoT 效果

<div class="result-value" markdown="1">

在最难四分位的 146 个病例中，SCoT 相对基线的召回率、精确率和 F1 分别增加 19.1、14.3 和 15.1 个百分点，F1 从 0.212 提高到 0.363，相对提升 71.4%。在最易四分位的 102 个病例中，三项指标反而分别下降 3.1、8.3 和 7.5 个百分点。

</div>

结果表明，SCoT 的价值集中在单体模型不确定、信息整合不完整的病例；对已经容易解决的病例，额外讨论可能引入噪声，形成作者所说的“过度思考”。这支持按病例难度自适应调用 SCoT，而不是对所有病例固定使用昂贵流程。但四分位由同一基线的表现定义，因此该分析描述的是条件相关性，不能独立证明病例难度导致 SCoT 增益。

<div class="result-source" markdown="1">

来源：第 6.3 节，Figure 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Our results show that SCoT has its most significant impact in cases where the baseline performs worst, boosting aggregate F1 score by 15.1 percentage points (0.212 – 0.363), for a relative lift of 71.4% (Figure 4). Conversely, in the upper quartile of easiest cases, defined as those where the single-agent baseline performed best, SCoT shows an 8.3 percentage point decrease in precision.

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

- 单智能体基线：同一后端模型直接完成鉴别诊断，不经过 SCoT 的多专科、多轮讨论流程；它用于测量协作结构相对普通单体推理的净增益。
- SCoT $N=1$：保留 SCoT 的多轮生成、修订和投票管线，但只使用一个智能体；它隔离“多轮结构与额外计算”本身，检验收益是否必须依赖多个异质视角。
- Best-of-5 与 Best-of-35：对单体模型进行多次独立采样，以更多测试时计算扩大候选答案集合；它们用于检验 SCoT 的提升能否由无交互的重复推理复现。
- Best-of-35 + judge：在 35 次重复采样后增加裁判模型进行筛选或整合；它是更强的单体扩展对照，用于区分“有选择器的采样扩展”与“专科智能体相互修订”。

**实验想回答的问题**

- SCoT 是否在不同模型家族与参数规模上稳定优于单智能体诊断，并且这种收益是否取决于模型具备足够的基础能力与“审议余量”？
- SCoT 的收益究竟来自多位专科智能体之间的多轮交互，还是仅来自更多推理轮次与测试时计算；同时，这种收益是否主要集中在单体模型难以解决的病例？

**实验实现**

结果按模型家族汇总，并按照研究问题逐项报告。跨模型实验比较 baseline 与 SCoT $N=5$：除 Qwen-2.5-1.5B 外，文中涉及 Qwen-2.5-3B、Qwen-2.5-32B、GPT-5.4 Nano、Sonnet 4.6、Haiku 4.5、Gemma-4 MoE 和 Gemma-4 dense；Claude 与 Gemma-dense 使用 100 个探索性病例，其余模型使用完整 570 例。结构隔离、best-of-$n$ 和主要难度分析以 Qwen-2.5-32B 为核心。难度实验按单智能体基线 F1 将病例划为四分位，并额外分析基线未找回任何真实诊断的完全失败病例。节选未提供随机种子、采样温度、置信区间、显著性检验、提示词细节及重复运行次数，因此所报告差值应视为该评测协议下的观察结果，而非已完成统计显著性验证的总体效应。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 将多智能体数量从 SCoT $N=5$ 消融为 SCoT $N=1$，同时保留多轮管线；Qwen-2.5-32B，570 个病例 | 单智能体基线的召回率、精确率和 F1 为 0.531、0.472 和 0.493；SCoT $N=1$ 为 0.476、0.580 和 0.509，即召回率下降 5.44 个百分点、精确率提高 10.74 个百分点。SCoT $N=5$ 则达到 0.607、0.509 和 0.531。 | 该消融隔离了“多轮管线”与“多智能体异质性”。保留流程但只让一个智能体反复修订，会删掉较多候选，从而提高精确率却损害召回率；恢复五个智能体后，互补视角扩大候选覆盖并取得最高召回率。因而作者认为，管线本身更像过滤器，而召回提升依赖多个智能体提供不同诊断假设。该实验没有拆分专科角色设定、投票规则和轮次数各自的独立贡献。 | 第 6.2 节，Figure 2<br><span class="experiment-evidence">In this setup, we found that recall degraded relative to its single-agent baseline (no SCoT), losing 5.44 percentage points. The configuration did, however, improve precision by 10.74 percentage points, suggesting that the scaffold of the pipeline functions as a precision-positive filter for a single agent, but as a recall-positive broadening mechanism for multiple agents (Figure 2).</span> |
| 移除最终投票的中间阶段分析，用于观察单智能体在投票前的多轮行为 | 在投票前，单智能体相对基线的精确率下降 11.1 个百分点，而召回率仅提高 4.2 个百分点；经过投票后，完整 SCoT $N=1$ 则表现为精确率提高 10.74 个百分点、召回率下降 5.44 个百分点。 | 这一分析隔离了投票机制的作用：多轮生成在投票前略微扩展候选，却同时引入较多错误项；投票随后强力过滤候选，使最终输出更精确但漏诊更多。作者据此把投票视为“精炼”部件，而不是产生诊断广度的来源。由于节选未给出投票前的绝对分数及独立统计检验，这里只能判断方向和百分点变化。 | 第 6.2 节，Figure 2 后的投票前分析<br><span class="experiment-evidence">Performance before the voting round sees the single-agent trade precision for only a marginal recall gain: precision falls by 11.1 percentage points while recall increases by 4.2 percentage points.</span> |

**定性案例**

- 完全失败病例的聚合案例分析：在 Qwen-2.5-3B、Qwen-2.5-32B、Gemma-4-MoE 和 GPT-5.4 nano 上，单智能体基线平均有 89 例未找回任何真实诊断；对应 SCoT 平均找回 16.3% 的真实诊断项，并在 53.9% 的病例中至少找回一项，即挽救 48/89 个完全失败病例。作者进一步报告，这类病例中 35% 的真实诊断在 refinement 阶段才进入共识，说明后期相互修订可能是困难病例恢复的关键路径。该分析是跨病例与模型的聚合结果，不是对某个具体患者推理过程的定性展示。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出通过多轮专科智能体协作和审议来完成医学鉴别诊断的LLM推理架构。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`d38084bde70fc536680fd10838736a11947a4db2e97ff4aca59bac80c0977e38`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
