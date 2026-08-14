---
title: "[论文解读] From Caveman to Expert Analyst: Energy Consumption of Variable LLM Tasks"
description: "[arXiv 2608.12350][LLM 效率] 本文从需求侧管理视角研究普通用户能否通过选择推理或非推理模型、限定回答长度及采用可复用提示策略，在基本保持回答质量的同时降低商业大语言模型推理阶段的用电量。"
arxiv_id: "2608.12350"
announcement_date: "2026-08-14"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T03:03:25.480590+00:00"
source_sha256: "99f0a7cd9ed111f02d22f8e400aeb8ef1755d73822869a06375076dc55234381"
tags:
  - "LLM 效率"
  - "LLM Reasoning"
  - "能源"
  - "气候减缓"
  - "大语言模型"
  - "人工智能"
  - "需求侧管理"
  - "提示行为"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.12350</p>

# From Caveman to Expert Analyst: Energy Consumption of Variable LLM Tasks

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Diego Manya, Ethan I. Thorpe, Ji Zhang, Myranda Shirk, Jiamian He, Angel Hsu, Michael P. Vandenbergh</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Data-Driven EnviroLab, Institute for Environment, UNC Chapel Hill；Climate Governance Lab, Vanderbilt Law School, Nashville, Tennessee, USA；Vanderbilt University, Nashville, Tennessee, USA；Department of Public Policy, UNC Chapel Hill；Vanderbilt Law School, Nashville, Tennessee, USA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12350v1) · [PDF 下载](https://arxiv.org/pdf/2608.12350v1) · **关键词** 能源, 气候减缓, 大语言模型, 人工智能, 需求侧管理, 提示行为<br>


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

本文从需求侧管理视角研究普通用户能否通过选择推理或非推理模型、限定回答长度及采用可复用提示策略，在基本保持回答质量的同时降低商业大语言模型推理阶段的用电量。

**不用术语来说**：生成式人工智能的普及使数据中心用电需求持续增长，但现有讨论主要关注如何为数据中心增加低成本、低环境影响的电力供应，较少研究普通用户能否通过改变日常使用方式减少需求。由于一次提示的节电幅度只有在大量用户愿意采用且回答仍然可用时才有现实意义，关键问题不是寻找复杂的模型优化技术，而是识别无需专业知识、容易推广且不会明显损害结果质量的用户行为。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 将人工智能用电治理的研究对象从供电侧和数据中心运营扩展到普通商业大语言模型用户，系统考察四类具有较高行为可塑性的使用方式，即模型类型选择、角色式提示、最简回答要求以及高效或截断式提示。
- 按布鲁姆认知分类法刻画任务复杂度，并在主要供应商的较新商业模型上使用基准数据集提示，分析同一节电行为是否会因任务难度不同而产生不同的能耗与质量效果。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于生成式人工智能用电需求与需求侧管理的交叉领域。大语言模型聊天机器人的普及使模型推理，即用户每次提交提示并获得回答的过程，成为数据中心新增电力需求的重要来源；智能体式人工智能还会通过多轮、反复推理进一步增加耗电。现有研究与政策较多关注如何为数据中心供应低成本或低环境影响的电力，而较少考察普通用户能否通过改变模型选择和提示行为减少需求。本文因此将商业大语言模型的单次使用视为可干预的用电行为，研究无需技术专长、可广泛复用的操作是否具有显著的技术减排潜力。研究只评估电力消耗，不直接估算用水量或碳排放，因为后两者还明显取决于数据中心所在地温度和供电电网结构等用户无法控制的条件。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大语言模型推理**

推理是已训练模型接收用户提示并生成回答的运行过程，不是本文所说的模型训练。回答生成所需的计算越多、过程越长或迭代次数越多，通常就可能消耗更多电力。

</div>
<div class="concept-item" markdown="1">

**推理模型与非推理模型**

推理模型会投入更多计算步骤处理复杂问题，非推理模型则通常直接生成答案；这里的分类是用户可选择的模型运行方式。本文比较二者，是为了判断日常任务是否需要承担推理模型额外的能源成本。

</div>
<div class="concept-item" markdown="1">

**技术减排潜力与行为可塑性**

技术减排潜力指采用某种行为后理论上能够减少的能源使用量，行为可塑性指用户改变到该行为的难易程度。有效的需求侧措施不仅要节电幅度可观，还要足够简单，才能被大量普通用户采用。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是使用 ChatGPT、Claude 等通用商业大语言模型的普通个人用户，而不是仅面向开源模型或编程、技术写作等专业场景。输入包括按 Bloom 认知分类法划分任务复杂度、并从大语言模型基准数据集中选取的提示，以及四类用户可执行的提示或模型选择行为：选择推理或非推理模型、赋予不同“角色”、要求最简回答，以及采用高效或截断式提示。系统在主要供应商的较新商业模型上生成回答，输出并比较不同策略下的电力需求，同时需要考察回答质量是否仍足以完成任务，以及节电效果是否随任务复杂度变化。其基本假设是用户能够控制模型类型与提示文本，但无法控制数据中心位置、环境温度和供电结构；本文首先估计这些行为的技术潜力，并不直接证明大规模用户一定会采纳。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Podder et al. (2026)、Adamska et al. (2026) 与 Rubei et al. (2025)**: 这些研究已考察提示工程与能源消耗或碳排放之间的关系，但据本文作者概括，其重点主要是 Llama 等开源模型或技术写作、内容创作、编程和数据分析等专门任务。本文转而研究普通用户使用通用商业大语言模型时可直接复用的简单行为，并按任务复杂度分析其效果。
- **Dietz et al. (2009)、Swim and Baker (2025) 与 Nielsen et al. (2026)**: 这些工作提供了评估行为干预的概念框架，即同时考虑技术潜力与行为可塑性。本文借用该框架，将提示修改和模型选择理解为可能由平台、雇主、学校或其他组织推广的需求侧行为。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型聊天机器人及智能体式人工智能需要执行一次或多次推理，广泛采用后会增加数据中心的电力需求，并对电力系统可靠性、可负担性和环境目标形成压力。作者特别关注推理阶段，因为该阶段由持续增长的日常提示直接驱动；与此同时，许多普通用户并不了解人工智能服务的用电和环境影响，组织也缺少可直接纳入员工政策或使用建议的低门槛节电做法。本文只评估电力使用，而不把用水量或碳排放作为主要结果，因为后两者还强烈依赖数据中心所在地温度、电网电源结构等用户无法控制的外部条件。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **供给侧与数据中心侧治理**：相关研究和政策主要通过增加低成本电力供应、接入环境影响较低的电源，或利用人工智能企业、数据中心与公用事业之间的合同调整负荷时段，来缓解人工智能增长带来的电力压力。这类方法主要改变电力从何处获得或何时使用，而不是改变终端用户一次请求所产生的计算需求。
- **面向模型或专业任务的提示节能研究**：既有工作已经比较提示工程与能耗或碳排放之间的关系，但研究对象主要是开放源代码模型，或技术写作、内容创作、编程和数据分析等专门场景。其基本思路是改变提示的表达和约束，观察输出计算量、能源消耗或排放是否随之下降。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 供给侧措施即使能够降低供电成本或调整负荷时段，也没有回答普通用户是否能直接减少人工智能服务的用电总量；因此，面向大规模终端用户的需求侧减排潜力仍缺乏证据。
- 既有提示节能研究偏重开放源代码模型和专业任务，其结论未必适用于使用 ChatGPT、Claude 等通用商业产品的普通用户；同时，较少研究按任务复杂度比较节能策略，因而无法判断简单问题与高认知难度问题是否应采用相同建议。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一项以普通商业大语言模型用户为对象的系统评估：同时检验无需技术知识、能够复制到不同提示中的通用行为，测量其技术减排潜力，并考察节电效果与回答质量之间的权衡是否随任务复杂度变化。这个缺口使企业、学校和其他组织难以判断哪些用户建议既容易采用，又足以产生可观的需求侧效果。

</div>
<div markdown="1"><span>核心问题</span>

在个人使用主流商业大语言模型的情境下，选择推理或非推理模型、加入不同角色指令、要求最简回答以及采用高效或截断式提示，能否在不同复杂度任务上显著降低电力消耗而不显著损害回答质量？

</div>
<div markdown="1"><span>作者直觉</span>

一次大语言模型请求所需的计算量并非完全固定：模型是否展开额外推理、回答生成多少内容，以及提示是否明确限制输出，都可能改变推理过程和输出长度。普通用户虽然不能控制服务器、电网结构或模型内部实现，却能控制这些请求条件；若某种简短指令能减少不必要的推理或冗余文本，同时保留完成任务所需的信息，那么单次节省经过大规模、高频使用累积后就可能形成有意义的需求侧节电效果。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该研究采用受控的重复查询实验，评估普通用户能否仅通过选择模型或修改提示词来降低商业大语言模型的推理能耗。输入是从 ChatBot Arena、Natural Questions 和 MMLU 等基准中选出的 $300$ 个真实或接近真实用户问题，并按布鲁姆分类法划分为知识、理解、应用、分析、综合和评价六类，每类 $50$ 个。研究将这些问题提交给五家供应商的十种模型配置，比较非推理基线、高推理模型以及三种节能提示策略；每次请求记录输出、输出 token 数和从请求到最后一个 token 的客户端响应时间，再以模型对应的功率系数估算单次查询电耗。

方法的核心不是直接测量数据中心电表，而是做相对行为比较：在相同问题集合上改变用户可控制的选项，观察响应时间、估算电耗和语义保持程度如何变化。能耗以 $E_m=P_m t/3600$ 计算，其中模型相关系数 $P_m$综合了理论 GPU、非 GPU 功耗及电能使用效率（PUE）假设；回答质量则以句向量余弦相似度近似衡量。直观而言，研究把每个模型视为一台具有特定“每小时耗电率”的机器，用回答所需时间估计本次运行的电量，同时检查节能后的回答是否仍与原回答表达相近。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建并分层问题集

研究者在布鲁姆分类法的知识、理解、应用、分析、综合和评价六类中各选取 $50$ 个提示，共得到 $300$ 个查询，用任务类别表示认知要求的递增层次。

<div class="method-step__io" markdown="1">

**输入**：来自 ChatBot Arena、Natural Questions 和 MMLU 等现有基准的用户查询候选。<br>
**输出**：带有六类认知标签的固定问题集，可用于总体比较以及按任务复杂度分层比较。

</div>

**直观理解**：这一步相当于准备一份覆盖“记忆事实”到“作出评价”的分级试卷，避免节能策略只在某一种简单任务上看起来有效。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成基线与行为干预条件

基线使用最新的非推理或低强度模型和未经修改的提示；四种比较条件分别为高推理模型，以及在基线模型上加入 energy-efficient persona、minimal answer 或 caveman 指令。除高推理条件改变模型外，三种提示干预均保持模型与基线一致，以尽量隔离提示措辞的影响。

<div class="method-step__io" markdown="1">

**输入**：每个原始提示以及五家供应商提供的推理、非推理或低推理强度模型配置。<br>
**输出**：同一问题对应的基线回答、高推理回答和三类提示干预回答。

</div>

**直观理解**：研究先保留一个普通使用方式作为参照，再一次只改变一个用户决策：要么换成更强推理模式，要么要求模型以不同方式缩短回答。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 调用商业模型并记录查询级观测

研究从美国在夜间执行请求，以减弱地理位置和排队对客户端到最后一个 token 时间（TTLT）的影响，并为每次查询记录 token 使用量、完整回答和响应时间。非推理模型的能耗假设采用 $32$ 路并发批处理，推理模型采用 $16$ 路并发批处理。

<div class="method-step__io" markdown="1">

**输入**：各实验条件下的提示与相应商业模型 API 配置。<br>
**输出**：逐查询的模型、任务类别、实验条件、响应文本、token 数和推理时间记录。

</div>

**直观理解**：由于研究者看不到供应商服务器内部的电表，只能记录用户端可观察的回答时长和 token，并尽量在相似网络负载条件下收集数据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 估算电耗并评估语义保持

研究将响应时间乘以模型特定的理论功率系数并换算为 Wh，得到单次查询的估算能耗；同时使用 all-MiniLM-L6-v2 将回答映射为句向量，再通过 scikit-learn 计算成对回答的余弦相似度。

<div class="method-step__io" markdown="1">

**输入**：逐查询响应时间、模型功率系数，以及基线和比较条件下的回答文本。<br>
**输出**：每个模型、问题和干预条件的估算能耗，以及相对于比较回答的语义相似度。

</div>

**直观理解**：前一项回答“省了多少电”，后一项检查“省电后是否还在说大致相同的内容”；两者必须结合，才能避免把单纯删掉答案误判为有效节能。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 单次查询能耗估算

$$
E_m(\mathrm{Wh})=P_m\left(\frac{t_m}{3600}\right)
$$

**符号说明**

- $E_m$：模型 $m$ 完成一次查询的估算电能消耗，单位为 Wh。
- $P_m$：模型 $m$ 的理论总功率系数，单位为 W；该系数包含 GPU、非 GPU 功耗和 PUE 等假设，并已按文中批处理设定折算。
- $t_m$：模型 $m$ 对该查询的客户端到最后一个 token 时间，即 TTLT，单位为秒。
- $3600$：将秒换算为小时的常数。

<div class="equation-explanation" markdown="1">

**直观理解**：公式按“功率乘以时间”估算电量。文中对每个模型给出不同的 $P_m$，例如 gpt-5.5-pro 对应 $4872.0$，gpt-5.4-mini 对应 $410.4$；因此即使响应时间相同，不同模型的估算耗电也可能显著不同。<br>
**原文位置**：第 2.1 节，表 3“​​Simplified energy consumption calculation for each model”

</div>

</div>

<div class="equation-block" markdown="1">

#### 回答向量余弦相似度

$$
\operatorname{sim}(\mathbf{u},\mathbf{v})=\frac{\mathbf{u}^{\top}\mathbf{v}}{\lVert\mathbf{u}\rVert_2\lVert\mathbf{v}\rVert_2}
$$

**符号说明**

- $\mathbf{u}$：由 all-MiniLM-L6-v2 编码得到的一个回答的句向量。
- $\mathbf{v}$：由同一编码器得到的另一个待比较回答的句向量。
- $\mathbf{u}^{\top}\mathbf{v}$：两个回答向量的内积。
- $\lVert\mathbf{u}\rVert_2$：向量 $\mathbf{u}$ 的二范数，即其欧氏长度。
- $\operatorname{sim}(\mathbf{u},\mathbf{v})$：两个回答在句向量空间中的余弦相似度。

<div class="equation-explanation" markdown="1">

**直观理解**：该计算关注两个向量的夹角而非长度：方向越接近，回答的整体语义越相似。原文明确说明使用余弦相似度，但未在节选中印出公式，因此这里给出的是该函数的标准数学定义，而不是论文另行提出的新目标。<br>
**原文位置**：第 2.1 节“Testing Methodology and Data Analysis”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。研究没有训练或微调新的语言模型，也没有通过损失函数优化提示词；all-MiniLM-L6-v2 仅作为现成的句向量编码器使用。能耗和余弦相似度是实验测量与比较指标，不构成反向传播目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 用户侧行为干预模块**

实验设置包含一个非推理或低推理强度基线、一个高推理模型条件和三个提示改写条件。energy-efficient persona 提供柔性的节能角色指令，minimal answer 明确要求用最少 token 完整准确作答，caveman 则要求删除冠词、填充语和寒暄并允许片段式表达。

> 直观理解：这些干预都能由普通用户直接实施，不要求修改模型权重、推理服务器或解码程序，因此测试的是现实中的需求侧节能空间。三种提示的约束强度不同，也使研究能够观察缩短输出与保留内容之间的权衡。

**2. 商业模型查询能耗估算模块**

研究沿用 Jegham 等人的方法并采用 Bao 等人针对单次查询的修改，将客户端 TTLT 与模型特定功率系数结合。功率系数基于模型参数规模、硬件功率规格、GPU 与非 GPU 消耗、PUE 和批处理假设推导，而不是来自供应商服务器的实时功率遥测。

> 直观理解：该模块把不可直接观察的数据中心耗电转化为“估计功率乘以运行时间”。它适合比较同一套假设下哪些行为更耗电，但绝对 Wh 数值会受模型参数估计、真实硬件、批量大小、排队时间和数据中心运行方式影响。

**3. 回答语义相似度模块**

all-MiniLM-L6-v2 句子 Transformer 将每个回答编码为稠密向量，scikit-learn 的余弦相似度函数再衡量模型回答向量之间的方向接近程度。该指标用于判断切换模型或压缩提示后，回答是否仍保留与参照回答相近的语义。

> 直观理解：这类似于把两段文字转换成语义坐标，再看它们指向是否接近。它能低成本检查内容是否大体一致，但不等于事实正确率，也未必能识别关键细节遗漏、推理错误或格式是否满足用户要求。

**训练与推理**

整个研究仅涉及推理。对每个带布鲁姆类别的问题，研究先调用非推理或低推理强度模型生成未修改提示下的基线回答；随后在供应商对应的高推理配置上运行原提示，并在基线模型上分别运行三种附加指令。模型以自回归方式逐 token 生成答案，实验端记录到最后一个 token 的时间、token 使用量和回答文本。之后依据模型专属系数把 TTLT 换算为估算 Wh，并将回答送入 all-MiniLM-L6-v2 得到向量，计算回答对的余弦相似度。最终按实验条件、模型供应商及布鲁姆类别汇总比较，不存在参数更新或训练阶段。

**复现信息**

模型范围为 OpenAI、Google、Anthropic、DeepSeek 和 xAI 的十种推理或非推理配置。表 1 所列关键配置包括温度、reasoning effort、thinking level 或 token budget；多数模型温度设为 $0$，Anthropic 两种模型温度为 $1$。商业供应商未公开的参数规模来自 Li（2026）的估计，Gemini 3.1 Pro 和 Flash 的规模使用对应 Gemini 2.5 型号作下界，因此模型功率系数并非完全基于厂商披露数据。

为解释能耗估计，必须保留三项复现条件：请求从美国在夜间执行；非推理模型假定 $32$ 路并发批处理，推理模型假定 $16$ 路；能耗只依据主动响应阶段的客户端 TTLT 估算。原文未明确报告每个问题是否重复调用、请求执行顺序、网络延迟校正、异常值处理和统计显著性检验，也没有给出真实服务器、GPU 型号或实时利用率；因此该方法更可靠地支持相同假设下的相对比较，不能视为商业数据中心端到端实际耗电的直接测量。问题数据可用性位置为 DOI：https://doi.org/10.15139/S3/RMU1TU。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 按布鲁姆认知分类法组织的通用提示集合，覆盖 Knowledge、Comprehension、Apply、Analyze、Evaluate 和 Create 六类认知任务，用于检验任务复杂度与能耗的关系。当前摘录未报告提示总数、具体来源及训练集、验证集或测试集划分；它在实验中属于评测问题集，而不是模型训练数据。
- 同一批问题的非推理模型与同提供商推理模型回答配对，用于比较两类模型的能耗，并计算成对回答的余弦相似度。当前摘录未明确列出全部推理模型名称、每类样本数或重复运行次数。
- 非推理模型在基线提示及三种改写提示下生成的配对回答，用于评估提示实践的节能效果与语义保真度。摘录提及五个基线模型，并点名 Grok 4.3-low、DeepSeek V4 Flash、Gemini 3.1 Flash、GPT 5.4-mini 和 Haiku 4.5，但未报告完整提示模板、数据规模或缺失样本处理方式。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**单次回答估算能耗（Wh）**

估计模型完成一个提示所消耗的电能，并按任务类型、模型类型和提示实践比较其分布或中位数。该指标衡量推理服务侧的用电负担；当前摘录未交代估算仪器、系统边界或不确定性计算方法。 （越低越好，因为在回答质量仍可接受的前提下，更低的 $\mathrm{Wh}$ 表示更小的电力需求和潜在环境负担。）

</div>
<div class="metric-item" markdown="1">

**相对能耗变化**

将某个推理模型或提示实践的能耗与非推理原始提示基线比较，以倍数或百分比表示增加和降低。它适合回答行为改变带来的相对节能潜力，但不能独立给出整个数据中心的绝对节电量。 （对节能实践而言，降幅越大越好；对推理模型比较而言，能耗倍数越接近 $1$ 越节能，但仍需结合回答质量判断。）

</div>
<div class="metric-item" markdown="1">

**回答余弦相似度**

比较两份回答语义表示向量方向的一致程度，用于估计改用推理模型或提示实践后，回答内容相对基线保留了多少。它衡量语义接近程度，不直接衡量事实正确性、逻辑严谨性或任务完成质量。 （通常越高越好，因为更高值表示与基线回答的语义内容更接近；但基线本身未必正确，因此高相似度不能等同于高质量。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 按布鲁姆认知类别评估五个非推理模型的基线能耗

<div class="result-value" markdown="1">

基线中位能耗随任务复杂度总体上升：Knowledge 类最低，为 $0.16\,\mathrm{Wh}$；Create 类最高，为 $0.68\,\mathrm{Wh}$。Wilcoxon 秩检验还表明，较低认知任务与 Evaluate、Create 等较高认知任务的能耗分布存在统计差异。

</div>

作者据此主张，布鲁姆分类能帮助识别通用提示的能耗层级。直观地说，要求模型创造或综合内容通常比检索知识消耗更多电力。不过，该结果说明的是类别间关联，并不能证明认知复杂度是能耗变化的唯一原因；输出长度、模型路由和回答格式也可能共同影响能耗。

<div class="result-source" markdown="1">

来源：第 3.1 节，图 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The results of our baseline estimations (non-reasoning models) in Figure 1 show a gradient in the required energy following the complexity of the prompts with the lowest median estimates (0.16 Wh) for knowledge type prompts and highest median estimates (0.68 Wh) for create type of prompts.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 同一提供商的推理模型与非推理模型配对比较

<div class="result-value" markdown="1">

推理模型在所有任务类别上耗能更高：最低复杂度任务约为基线的 $20$ 倍，较高复杂度任务约为 $15$ 倍；作者进一步概括，使用推理模型会使能耗至少增加 $19$ 倍，而回答语义差异从 Knowledge 类约 $10\%$ 增至 Create 类约 $20\%$。

</div>

作者的结论是，多数普通任务使用非推理模型即可获得语义内容接近的回答，启用推理模式的额外电力成本可能不划算。分析上，这一结果只表明两类回答彼此相似，不能证明非推理回答在事实正确性、复杂推导或高精度任务中同样可靠；“多数使用场景无需推理模型”仍依赖任务风险和质量要求。

<div class="result-source" markdown="1">

来源：第 3.1 节，图 2 至图 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Therefore, for most use cases except those that are exceptionally complex or demand exceptional precision, switching from a non-reasoning to a reasoning model will not see a significantly better response but will increase their energy footprint by at least 19 times.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 三种提示实践相对非推理原始提示基线的节能与语义保真度比较

<div class="result-value" markdown="1">

提示改写的最大节能幅度达到 $65\%$。其中，最小输出提示在各任务类型上的降幅最大，约为 $38\%$ 至 $63\%$；穴居人式提示通常次之，但在 Knowledge 类任务上平均增加 $5\%$ 能耗；节能人格提示的降幅为 $4\%$ 至 $35\%$，同时维持最高的基线语义相似度，中位数约为 $0.8$ 至 $0.9$。

</div>

结果展示了明确的节能与内容保留权衡：直接压缩输出最省电，但回答相对基线变化也更大；节能人格提示节电较少，却更能保持原回答含义。对普通用户而言，若首要目标是保留回答内容，节能人格更稳妥；若可接受更短、更不完整的回答，最小输出更节能。这些比较没有证明任一策略在所有模型或任务上始终最优。

<div class="result-source" markdown="1">

来源：第 3.2 节，图 4 和图 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

By contrast the energy efficient persona prompt maintained substantially higher semantic similarity to the baseline, with median cosine similarity between 0.8 and 0.9, while still reducing energy consumption across all task categories.

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

- 非推理模型加原始提示的基线：它代表用户不采用额外节能提示实践时的常规使用方式，也是推理模型和三种提示改写共同参照的能耗与回答内容基准。
- 同一提供商的高推理模型：与其非推理对应模型进行配对比较，尽量减少提供商或模型家族差异，用于隔离启用较强推理能力所伴随的能耗变化。
- 最小输出提示（minimal output）：要求模型尽量缩短输出，用于测试直接限制回答长度能否最大化节能；它也揭示能耗下降可能以损失回答内容为代价。
- 穴居人式提示（caveman）与节能人格提示（energy efficient persona）：前者以极简表达约束回答，后者通过人格或行为指令鼓励节能。两者分别代表较强的输出形式干预和较温和的行为引导，用于与原始提示及最小输出策略比较。

**实验想回答的问题**

- 在按布鲁姆认知分类法划分的不同任务复杂度上，推理模型相较同一提供商的非推理模型会增加多少能耗，这种额外能耗是否对应明显更高的回答语义内容相似度？
- 三种可由普通用户直接采用的提示实践，即“穴居人式”简化表达、节能人格提示和最小输出提示，能否降低非推理模型的能耗，以及节能幅度与回答语义保真度之间存在什么权衡？

**实验实现**

评测先依据布鲁姆认知分类法把问题分成六种复杂度，再在五个非推理模型上估算基线回答能耗，并用 Wilcoxon 秩检验比较不同认知层级的能耗分布。随后，将每个非推理模型与同一提供商的推理对应模型比较能耗，并计算两类回答的成对余弦相似度。提示实验固定使用非推理模型，分别施加穴居人式、节能人格和最小输出三种提示改写，以原始提示回答为共同基线，比较中位能耗和语义相似度，并进一步按模型与任务类型分解结果。当前摘录未明确报告硬件、功耗估算工具、采样参数、运行次数、置信区间、多重检验校正和显著性阈值，因此这些结果更适合作为相对技术减排潜力的证据，而非可直接复现的绝对能耗测量。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 隔离输出压缩强度：比较最小输出、穴居人式和节能人格三种提示实践 | 最小输出提示在所有任务类型中实现最大节能，降幅从 Knowledge 类的 $38\%$ 到 Create 类的 $63\%$；但其余弦相似度仅为 $0.55$ 至 $0.73$，低于穴居人式提示的 $0.64$ 至 $0.75$ 和节能人格提示约 $0.8$ 至 $0.9$ 的中位水平。 | 这一对照主要隔离“要求回答更短”与“以较温和方式引导模型节能”的效果。更强的输出压缩带来更大节电，同时也删除或改写更多基线语义内容，说明节能并非没有质量代价。不过余弦相似度只反映内容接近度，不能确定被删除的信息是否真正影响任务完成。 | 第 3.2 节，图 4 和图 6<br><span class="experiment-evidence">Although the minimum output and caveman prompts produced the largest reductions in energy consumption, they were also associated with lower cosine similarity to the baseline responses (0.64 to 0.75 for caveman and 0.55 to 0.73 for minimum).</span> |
| 按具体模型拆分提示实践效果 | 不同模型上的最佳策略并不一致：节能人格在 Grok 4.3-low 的 Comprehension 类问题上最有效，却在 DeepSeek V4 Flash、Gemini 3.1 Flash 和 GPT 5.4-mini 的同类问题上最不有效；穴居人式提示在 Haiku 4.5 的多数任务上反而提高能耗。 | 该分解检验总体平均节能是否由少数模型驱动，并揭示提示策略与模型实现之间存在交互。它意味着用户建议不能只依据跨模型平均值制定，也不能把某一模型上的节能幅度直接迁移到其他模型。摘录没有提供这些模型级差异的具体数值和显著性检验，因此只能确认方向性异质性。 | 第 3.2 节，图 5<br><span class="experiment-evidence">For example, the energy efficient persona was the most effective modification for comprehension type questions on Grok 4.3-low but was the least effective for comprehension type questions on DeepSeek V4 Flash, Gemini 3.1 Flash, and GPT 5.4-mini.</span> |

**定性案例**

- Gemini 3.1 Flash 在所有任务类型和提示实践下的估算能耗均显著低于其他受测模型，说明模型选择本身可能比提示微调带来更大的节能差异。不过摘录未给出其绝对能耗、质量比较或统计检验，不能据此认定该模型在能效与质量综合意义上普遍最优。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper centrally measures and reduces LLM inference energy consumption across model and prompting choices.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`99f0a7cd9ed111f02d22f8e400aeb8ef1755d73822869a06375076dc55234381`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
