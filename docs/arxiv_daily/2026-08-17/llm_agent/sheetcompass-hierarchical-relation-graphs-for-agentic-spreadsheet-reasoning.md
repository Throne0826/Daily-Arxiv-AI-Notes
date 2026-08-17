---
title: "[论文解读] SheetCompass: Hierarchical Relation Graphs for Agentic Spreadsheet Reasoning"
description: "[arXiv 2608.14452][LLM Agent] SheetCompass旨在以层次化关系图显式恢复复杂电子表格的表内空间拓扑与跨工作表语义依赖，并据此组织多智能体推理，以缓解扁平文本表示造成的结构信息损失。"
arxiv_id: "2608.14452"
announcement_date: "2026-08-17"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-17T02:01:24.459521+00:00"
source_sha256: "d752c1bb6328cbefba10a53a51e882609e5943b4de17bb801dec9e6fb871e69c"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "电子表格自动化"
  - "大语言模型智能体"
  - "多智能体系统"
  - "层次化关系图"
  - "表内空间拓扑"
  - "跨工作表语义依赖"
  - "结构化推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.14452</p>

# SheetCompass: Hierarchical Relation Graphs for Agentic Spreadsheet Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Panjing He, Mingyue Cheng, Yucong Luo, Li Li, Xiaohan Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China , Hefei , China；State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China；Affiliation: State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14452) · [PDF 下载](https://arxiv.org/pdf/2608.14452) · **关键词** 电子表格自动化, 大语言模型智能体, 多智能体系统, 层次化关系图, 表内空间拓扑, 跨工作表语义依赖, 结构化推理<br>


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

SheetCompass旨在以层次化关系图显式恢复复杂电子表格的表内空间拓扑与跨工作表语义依赖，并据此组织多智能体推理，以缓解扁平文本表示造成的结构信息损失。

**不用术语来说**：复杂电子表格并不只是许多单元格文字的集合：行列位置、分区、表头层级以及不同工作表之间的对应关系都承载业务含义。现有系统常把表格转换为Markdown、JSON等长文本交给大语言模型，这就像把一张地图拆成按顺序排列的地名列表；文字仍在，但哪些内容相邻、哪些列属于同一层级、成本表与价格表如何关联会变得难以辨认，因而容易在跨区域或跨工作表任务中定位错误、推理错位。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出SheetCompass，将电子表格从扁平序列重构为层次化上下文图，通过表级节点、列级节点及其关系同时表达表内空间布局和跨工作表语义联系，为后续推理提供结构化依据。
- 作者在该结构表示上结合专家知识记忆、推理经验记忆以及探索者、程序员、反思者组成的多智能体流程，使目标定位、代码执行和闭环校验分别由专门角色承担；原文进一步声称该框架在SCB、SB和SheetRM数据集上优于基线，但所给节选未提供具体数值。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

电子表格自动化旨在根据用户意图理解、查询或修改工作簿中的数据、公式与布局。复杂电子表格并非单纯的二维数值集合，而是以行列位置、表内区域、层级表头以及跨工作表引用共同承载业务语义的半结构化知识载体。大语言模型虽能理解自然语言并调用代码工具，但主流方法通常先把工作表序列化为 Markdown、JSON 等一维文本；这种处理保留了大部分单元格内容，却会削弱两类关键信息：表内层面，原本相邻或具有行列对应关系的单元格可能在文本序列中彼此分离；工作表间层面，成本表、价格表等对象之间隐含的数据依赖和业务逻辑难以显式呈现。因此，本文所处的核心问题是：如何为智能体保留工作簿的多层结构，使其能可靠完成涉及复杂布局、跨表关联和多步工具调用的任务。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**半结构化电子表格**

电子表格既包含规则的行列网格，又允许合并单元格、多级表头、多个数据区域和跨表引用，因此不像关系数据库那样具有完全固定的模式。单元格的意义往往同时取决于内容、位置、周围表头以及所在工作表。

</div>
<div class="concept-item" markdown="1">

**信息扁平化（序列化）**

信息扁平化是把二维工作表转换成 Markdown、JSON或连续文本，以便大语言模型按词元序列读取。转换后文本值可能仍在，但二维邻接关系、行列层级和跨工作表依赖可能被隐藏或打散。

</div>
<div class="concept-item" markdown="1">

**大语言模型智能体与多智能体系统**

大语言模型智能体是在语言模型推理之外加入环境观察、工具调用和反馈修正的系统；多智能体系统则让多个具有不同职责的智能体协作完成任务。本文背景下，角色分工用于分别承担结构导航、代码执行和结果验证，以降低长推理链中的错误累积。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个可能包含多个工作表、复杂表头与跨表依赖的工作簿，以及描述查询、计算或编辑目标的用户任务。系统需要先识别表内的空间拓扑和表间的语义联系，再通过智能体规划与代码工具执行操作，最终输出与用户意图及原工作簿结构对齐的处理结果。该设置隐含两个关键假设：单元格位置与布局本身携带语义；任务可能需要跨越多个数据区域或工作表进行长程推理，因而仅依赖扁平文本和单一智能体的连续推理不足以保证可靠性。原文节选没有给出形式化的问题定义、输入输出类型或统一数学符号。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **SpreadsheetLLM**: 该方法使用倒排索引转换来压缩电子表格的布局表示，说明大语言模型处理工作簿时需要控制表示长度；但按本文的归纳，这类序列化路线仍未充分显式保留非线性的表内拓扑与跨表语义依赖。
- **SheetAgent / SheetCopilot**: 两者通过多智能体流程拆分电子表格任务，并调用代码解释器执行操作，是本文最直接的智能体式自动化前序工作。SheetCompass在此基础上强调层次化关系图和结构感知导航，以弥补仅靠任务分解与工具调用时对复杂工作簿结构建模不足的问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

电子表格广泛承载异构数据、业务规则和领域知识，而大量重复操作使自动化成为影响工业生产效率的瓶颈。实际任务往往需要系统同时理解一个工作表内部的行列布局、表头和数据区域，并追踪多个工作表之间的数据依赖；若结构理解不可靠，即使模型能够读懂单元格文本，也难以稳定完成跨表定位、计算和修改。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于扁平文本表示的大语言模型方法**：这类方法先将多维电子表格线性化为Markdown、JSON或其他顺序字符串，再让大语言模型依据文本序列理解内容并规划操作。其优点是能够直接复用语言模型的语义理解能力和文本接口，同时通常可以保留单元格中的文字或数值内容。
- **基于线性序列的结构近似推理**：在缺少显式二维拓扑和跨工作表关系的情况下，模型依靠序列中的统计线索，间接推测哪些单元格、列、区域或工作表彼此相关。换言之，模型需要从展平后的上下文中自行重建原始表格结构，而不是在输入表示中直接获得这些关系。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 在单个工作表内部，线性化会打散行列构成的正交定位体系，使原本相邻的单元格、列层级和独立数据区域在词元序列中失去清晰的空间邻接关系。其后果是模型难以准确恢复网格布局，容易在目标区域识别和结构对齐时出错。
- 在多个工作表之间，扁平化会隐藏隐式数据依赖和业务逻辑，例如成本表与价格表之间的直接对应可能被拆成彼此孤立的文本片段。缺少显式跨表语义依赖后，模型难以重建工作簿中的动态数据流，尤其容易在跨表推理中发生结构错配。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法尚缺少一种能直接面向大语言模型或智能体、同时保留两个结构层次的表示与推理框架：一方面需要编码工作表内部的二维空间拓扑，另一方面需要连接不同工作表之间的语义依赖；此外，这种结构表示还必须能够被后续定位、执行和校验流程实际利用，而不能只作为静态描述存在。

</div>
<div markdown="1"><span>核心问题</span>

能否把复杂电子表格表示为显式的层次化关系图，并让具有探索、编程和反思分工的智能体在该图及双层记忆支持下协同工作，从而减少扁平序列导致的结构信息损失，提高跨区域、跨工作表任务的执行可靠性？

</div>
<div markdown="1"><span>作者直觉</span>

人类查看电子表格时会先凭视觉布局识别表头层级、数据区域和相邻关系，再追踪不同工作表之间的对应项，而不是逐字读取一条被拉直的长文本。SheetCompass的切入点是把这种可见但在线性输入中丢失的关系显式画成“导航图”：探索者先沿图确定目标及相关区域，程序员据此生成结构化操作，反思者再检查执行结果；专家知识记忆提供较稳定的工具使用规则，推理经验记忆则帮助后续轨迹根据既往执行反馈进行调整。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SheetCompass 将电子表格自动化拆成“空间重建”和“协同推理”两部分。输入是包含多个工作表和表格的集合 $\mathcal{T}$ 以及用户指令 $q$；系统先把原始二维网格重建为层次关系图 $\mathcal{G}=(\mathcal{V},\mathcal{E})$，以表节点和列节点表示数据实体，用结构边保存包含、相邻等版式关系，再结合向量相似度与大语言模型判断补充跨表语义边。随后，探索者把指令分解为原子步骤，从图中检索种子节点并扩展相关子图；程序员在图约束下生成并执行脚本；反思者依据从指令提取的检查清单核验执行后的表格状态，并在发现不一致时触发有限次数的修正。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 层次图初始化

系统依据表格边界、列标题、列顺序和代表性数据样本建立两级节点：表节点表示一个结构化表格，列节点由列标题及部分原始数据共同表征。确定性解析规则生成表到列的包含边，以及按水平顺序连接相邻列的邻接边，二者构成结构边集合 $E_{\mathrm{str}}$。

<div class="method-step__io" markdown="1">

**输入**：原始电子表格集合 $\mathcal{T}=\{T_1,T_2,\ldots,T_M\}$，其中每个工作表可以包含多个表格。<br>
**输出**：包含表节点、列节点及稳定结构边的初始层次图。

</div>

**直观理解**：这一步把电子表格从一串容易丢失位置的信息，恢复成一张“表格包含哪些列、哪些列彼此相邻”的地图。系统按列而非按单元格建模，以较小规模保留完成任务所需的布局和数据语境。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 跨表语义对齐

预训练 Transformer $\Phi$ 将每个列特征编码为向量 $\mathbf{h}_i=\Phi(\mathbf{x}_i)$，系统计算列向量的余弦相似度，并让大语言模型函数 $\mathcal{F}_{\mathrm{LLM}}(v_i,v_j)$ 判断主键、外键或其他逻辑联系。两类分数按权重 $\beta$ 融合，超过阈值 $\alpha$ 时加入语义边 $E_{\mathrm{sem}}$。

<div class="method-step__io" markdown="1">

**输入**：初始层次图中的列节点 $v_i$、列标题与代表性数据组成的特征 $\mathbf{x}_i$。<br>
**输出**：统一层次关系图 $\mathcal{G}=(\mathcal{V},\mathcal{E})$，其中 $\mathcal{E}$ 同时包含结构边与跨表语义边。

</div>

**直观理解**：即使两个相关列位于不同工作表、名称也不完全一致，系统仍尝试把它们连接起来。向量匹配负责发现“看起来相似”，大语言模型判断负责检查“逻辑上是否确实相关”，阈值则过滤置信度不足的连接。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 指令分解与相关子图检索

探索者将 $q$ 分解为具有依赖关系的原子步骤 $\{t_1,t_2,\ldots,t_n\}$，再按步骤向量 $\mathbf{t}_i$ 与节点表示 $\mathbf{h}_j$ 的余弦相似度筛选种子集合 $\mathcal{S}_i$。系统从种子节点执行广度优先搜索得到各步骤子图 $\mathcal{G}_i$，并以 $\mathcal{G}_{\mathrm{shared}}=\bigcap_{i=1}^{n}\mathcal{G}_i$ 提取多个步骤共同依赖的图结构。

<div class="method-step__io" markdown="1">

**输入**：用户指令 $q$、统一层次图 $\mathcal{G}$，以及专家知识记忆和当前任务的推理经验记忆。<br>
**输出**：可执行的原子任务序列，以及供后续代码生成使用的紧凑共享子图 $\mathcal{G}_{\mathrm{shared}}$。

</div>

**直观理解**：探索者先把复杂请求拆成小任务，再只取地图中与这些任务密切相关的区域。这样既能定位跨表数据，也能减少送入模型的无关内容，降低上下文过长和错误引用实体的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 图约束脚本生成与沙箱执行

程序员把每个步骤转换为可执行脚本，并执行实体对齐检查，要求代码中的工作表、表格、列和变量均锚定到已验证的图节点。脚本在配有 Python 解释器和 Excel 引擎的安全沙箱中运行，执行结果、报错和动作轨迹写入当前任务的推理经验记忆。

<div class="method-step__io" markdown="1">

**输入**：原子步骤、共享子图 $\mathcal{G}_{\mathrm{shared}}$、专家知识记忆中的公式或工具规则，以及当前任务的历史执行记录。<br>
**输出**：经过沙箱执行的候选电子表格结果、代码执行状态和可供诊断的运行轨迹。

</div>

**直观理解**：程序员不能凭空猜测列名或表格位置，而必须从关系图中选择真实存在的实体。沙箱相当于隔离的试运行环境，既执行修改，也保留失败原因供下一轮修正。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 跨列语义边判定

$$
\epsilon_{ij}=\begin{cases}1,&\text{if }\left[\beta\cdot sim_{ij}+(1-\beta)\cdot\mathcal{F}_{\mathrm{LLM}}(v_i,v_j)\right]>\alpha,\\0,&\text{otherwise.}\end{cases}
$$

**符号说明**

- $\epsilon_{ij}$：列节点 $v_i$ 与 $v_j$ 之间是否建立语义边的二值变量；取 $1$ 表示建立连接，取 $0$ 表示不连接。
- $v_i,v_j$：待判断关系的两个列节点。
- $sim_{ij}$：两个列表示向量的余弦相似度，即 $sim_{ij}=(\mathbf{h}_i\cdot\mathbf{h}_j)/(\|\mathbf{h}_i\|\|\mathbf{h}_j\|)$。
- $\mathcal{F}_{\mathrm{LLM}}(v_i,v_j)$：大语言模型对两个列节点逻辑关系的评分，用于检查主键、外键等关系。
- $\beta$：向量相似度在融合分数中的权重，$1-\beta$ 是大语言模型关系评分的权重。
- $\alpha$：建立语义边所需超过的置信度阈值。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把“数据和标题是否相似”与“逻辑上是否有关联”合并成一个置信度。只有融合分数超过 $\alpha$ 才连边，因此其作用不仅是发现跨表关系，也是在图构建阶段阻止低置信度关系污染后续推理。<br>
**原文位置**：第 3.3.2 节，公式 (2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 任务相关种子节点筛选

$$
\mathcal{S}_i=\{v_j\in V\mid\cos(\mathbf{t}_i,\mathbf{h}_j)\geq\lambda\}
$$

**符号说明**

- $\mathcal{S}_i$：与第 $i$ 个原子步骤相关、用于启动子图扩展的种子节点集合。
- $v_j$：层次图顶点集合 $V$ 中的第 $j$ 个候选节点。
- $\mathbf{t}_i$：第 $i$ 个原子步骤 $t_i$ 的向量表示。
- $\mathbf{h}_j$：候选节点 $v_j$ 的向量表示。
- $\cos(\mathbf{t}_i,\mathbf{h}_j)$：任务步骤表示与节点表示之间的余弦相似度。
- $\lambda$：种子筛选阈值；节点相似度达到该阈值才会被保留。

<div class="equation-explanation" markdown="1">

**直观理解**：该式为每个子任务选出一小批语义最相关的图节点，作为广度优先搜索的起点。$\lambda$ 控制召回范围：阈值较高会使上下文更紧凑，但可能漏掉间接相关实体；阈值较低会保留更多候选，也会增加上下文和错误匹配风险。<br>
**原文位置**：第 3.5 节，公式 (3)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文将总体任务形式化为在输入表格集合 $\mathcal{T}$ 和指令 $q$ 条件下寻找概率最大的输出表格序列，即 $\hat{\mathcal{A}}=\arg\max_{\mathcal{A}'}p(\mathcal{A}'\mid q,\mathcal{T};\theta)$。但所给章节没有说明对 SheetCompass 的图构建器、多智能体角色或记忆模块进行端到端参数训练，也没有报告损失函数、梯度优化过程或训练数据构造方法；因此该式应理解为任务目标的概率化定义，而不能据此断言系统使用该目标进行了监督训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 层次关系图**

图 $\mathcal{G}$ 采用表节点和列节点两级表示，避免成本较高的单元格级建图；$E_{\mathrm{str}}$ 编码表列包含和水平邻接关系，$E_{\mathrm{sem}}$ 则编码由向量相似度与大语言模型联合确认的跨表逻辑联系。该设计同时保存局部版式几何与全局语义依赖，并为后续检索和代码实体对齐提供统一坐标系。

> 直观理解：普通文本序列很难表达“某列属于哪个表、旁边是哪一列、另一张表中哪一列与它对应”。关系图把这些联系显式化，使智能体能够沿着可靠路径找到数据，而不是仅凭列名猜测。

**2. 双层记忆**

专家知识记忆是跨任务的长期知识库，保存常用公式、图表操作等领域规则，以及从历史代码执行中提炼的错误根因和修复模板；推理经验记忆是当前任务内的短期记录，保存图上移动、沙箱报错和检查器发现的不一致。当前任务中的成功轨迹和高价值经验可被提炼后迁移到长期记忆，但原文未给出具体的写入筛选算法或检索公式。

> 直观理解：长期记忆提供经过验证的操作常识，减少模型临时猜测；短期记忆则让下一轮知道上一轮走过哪些路径、为什么失败。二者结合，使修正能够继承已有结果，而不是每轮重新开始。

**3. 探索者—程序员—反思者协作**

探索者负责任务分解、图检索和目标定位；程序员依据共享子图生成受实体约束的脚本并在沙箱执行；反思者把用户约束转成检查清单，验证 $\Delta(\mathcal{M})$ 并触发最多 $\tau$ 轮修正。三个角色形成“定位—执行—核验”的闭环，角色之间通过图上下文、执行轨迹、错误诊断和记忆进行信息传递。

> 直观理解：将一个模型同时承担理解、写代码和验收容易混淆职责。这里让三个角色分别负责找对位置、做出修改和检查结果，使错误能被定位到具体阶段并反馈修复。

**训练与推理**

训练阶段：原文未明确报告专门的模型训练流程。语义表示由预训练 Transformer $\Phi$ 产生，逻辑关系判断和多智能体推理由大语言模型支持；长期专家知识主要来自预先整理的领域规则、工具使用知识，以及运行历史中提炼的修复经验，但经验提炼是否自动完成、如何审核和更新均未在所给章节中说明。

推理阶段：给定 $\mathcal{T}$ 与 $q$，系统先解析表格边界、标题、列顺序和代表性数据，建立表—列层次节点及结构边；再编码列特征，融合余弦相似度与大语言模型评分建立跨表语义边。探索者将 $q$ 分解为原子步骤，基于阈值 $\lambda$ 选取种子节点，通过广度优先搜索形成步骤子图并提取共享子图；程序员结合图上下文和记忆生成脚本，完成实体对齐后在沙箱中执行；反思者根据检查清单核验结果状态。若未满足约束，诊断信息和执行历史进入下一轮，直至检查通过或达到最大修正轮数 $\tau$，最终输出目标表格序列 $\hat{\mathcal{A}}$。

**复现信息**

公平复现该方法至少需要实现四项关键机制：一是能够识别一个工作表中多个表格边界的确定性解析器，并为列节点保留标题及代表性数据样本；二是预训练 Transformer 编码、余弦相似度、大语言模型关系评分以及由 $\alpha$ 和 $\beta$ 控制的语义连边规则；三是按 $\lambda$ 筛选种子节点、执行广度优先搜索并计算共享子图的检索过程；四是带 Python 解释器和 Excel 引擎的隔离执行环境、图实体对齐检查、状态清单核验及最多 $\tau$ 轮的反馈循环。所给章节未明确报告 $\Phi$ 的具体型号，列数据采样数量，$\alpha$、$\beta$、$\lambda$、$\tau$ 的取值，提示模板，广度优先搜索深度，共享子图为空时的处理方式，以及长期记忆的检索和更新实现；这些缺失信息会影响严格复现，也不应根据结果表自行推测。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- SCB：包含复杂工作表结构的电子表格任务基准。实验以$\mathrm{exec@1}$检验首次生成方案能否运行，以$\mathrm{pass@1}$检验其功能结果是否与标准答案一致。原文节选未给出样本规模、数据划分及单表与多表子集的具体数量。
- SB（SpreadsheetBench）：面向真实且复杂的电子表格操作；每个任务附带三个独立测试用例，适合检验方案在多个输入条件下的稳健性。实验同时报告软约束与硬约束结果，并进一步区分单表和多表场景来测试跨工作表依赖推理。
- SheetRM：同样以复杂工作表结构为特征，用于补充验证方法在另一类电子表格任务上的可执行性与功能正确性，指标为$\mathrm{exec@1}$和$\mathrm{pass@1}$。原文节选未说明其规模、划分和任务类型细节。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**exec@1与pass@1**

$\mathrm{exec@1}$衡量第一次生成的方案能否成功运行，主要反映语法、接口调用和运行时有效性；$\mathrm{pass@1}$要求第一次方案的功能输出通过标准答案验证，因此比“能运行”更接近任务是否真正完成。 （越高越好；前者表示运行失败更少，后者表示首次生成方案的功能正确率更高。）

</div>
<div class="metric-item" markdown="1">

**Soft restriction**

对SB每项任务的三个独立测试用例计算平均成功率；它允许方案只通过部分测试，因此衡量一般性能力而不会因少量边缘情况失败而将整项任务记为零。 （越高越好，因为表示平均而言通过了更大比例的测试用例。）

</div>
<div class="metric-item" markdown="1">

**Hard restriction**

只有一个任务的全部测试用例均通过时才计为成功，因而更严格地衡量方案在不同输入条件下的一致正确性和稳健性。 （越高越好，因为表示更多任务能够无遗漏地通过所有测试用例。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 较小骨干模型下的跨数据集总体比较

<div class="result-value" markdown="1">

作者报告，在所谓“GPT-4 backbone”设置下，SheetCompass在SCB上的$\mathrm{pass@1}$达到63.2%，在SB上的硬约束达到18.3%，在SheetRM上的$\mathrm{pass@1}$达到43.5%，并称三项均超过最强基线。

</div>

三种基准同时改善，说明该框架的收益可能不局限于某一种任务或某一种判分方式，尤其是功能正确性和严格多用例通过能力均有提升。不过节选缺少Table 1的完整基线分数，无法据此复算各项提升，也无法判断差异是否具有统计显著性；此外，“GPT-4”与设置中的GPT-4o-mini命名并不一致。

<div class="result-source" markdown="1">

来源：第4.2节，Table 1的文字总结；所给节选未包含Table 1表体

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under the GPT-4 backbone, SheetCompass advances the state-of-the-art by improving pass@1 on SCB to 63.2%, hard restriction on SB to 18.3% and pass@1 on SheetRM to 43.5% ,which noticeably surpass the strongest baseline.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GPT-5骨干模型上的高难度SB基准

<div class="result-value" markdown="1">

作者报告，换用GPT-5后，SheetCompass在SB软约束和硬约束上相对基线分别取得6.4和6.9个百分点的绝对提升。

</div>

硬约束的提升意味着框架不仅增加了平均通过的测试用例数量，也提高了整项任务三个测试用例全部通过的概率；这与执行反馈和纠错机制的设计目标一致。但该比较本身不能区分收益究竟来自层次关系图、记忆还是多智能体协作，也未说明计算成本是否同步增加。

<div class="result-source" markdown="1">

来源：第4.2节，Table 1的文字总结；所给节选未包含Table 1表体

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Notably, on the challenging SB dataset, SheetCompass achieves absolute improvements of 6.4% on soft restriction and 6.9% on hard restriction.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 单表与多表复杂度分析

<div class="result-value" markdown="1">

在SCB多表场景中，SheetCompass取得最高的65.2%得分且性能下降更小；在SB多表场景中，其软约束指标比基线高7.7个百分点。作为参照，SheetAgent在SCB中从单表的74.4%降至多表的58.1%。

</div>

该结果直接测试跨表依赖：传统智能体在工作表增多后更容易丢失列与表之间的对应关系，而显式的表—列层次图可提供定位锚点。它支持“结构建模有助于多表推理”的解释，但Figure 3节选没有给出SheetCompass的单表分数和完整基线明细，因此无法精确比较所有方法的下降幅度。

<div class="result-source" markdown="1">

来源：第4.4.1节，Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On SCB, the pass@1 of SheetAgent drops from 74.4% to 58.1% when moving from a single table to multiple tables. This drop indicates that linear spreadsheet inputs make it difficult for traditional methods to track columns across different worksheets. In contrast, SheetCompass is less affected by this layout change, achieving the highest score of 65.2% in the multi-table setting with a much smaller performance drop. A similar trend is observed on the SB dataset, where SheetCompass outperforms the baseline by 7.7% under the soft restriction metric.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 证据完整性有限：所给节选缺少Table 1的完整分数、Figure 3与Figure 4的全部数据，也未报告样本规模、数据划分、方差、置信区间或显著性检验。因此可以复述作者报告的优势，但不能独立验证提升是否稳定，也无法排除不同运行预算或提示设置造成的影响。
- 实验可复现性和成本比较不足：节选未说明提示词、工具接口、最大步骤数、失败重试预算、令牌与时间成本，也没有澄清结果段的“GPT-4 backbone”是否就是设置段的GPT-4o-mini。多智能体与多轮推理通常会增加调用成本，现有结果尚不能证明其在同等计算预算下仍优于基线。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Binder：代表静态表格问答路线，将自然语言一次性翻译为SQL或Python。它用于判断SheetCompass的优势是否来自交互执行与纠错，而不只是更强的代码生成。
- 传统VBA脚本生成方案：让大语言模型一次性生成可在Excel原生接口中执行的宏代码，代表静态电子表格自动化；其局限是执行中无法主动感知并修正错误。
- SheetCopilot与SheetAgent：代表面向电子表格的交互式智能体，采用“规划—行动—观察”闭环逐步操作。二者比静态方法更强，因此可用于检验层次关系图、记忆和角色协作是否带来额外收益。
- OS-Copilot：代表更通用的基于大语言模型的交互式计算机智能体，也使用环境反馈调整行动；该对比用于判断SheetCompass针对电子表格结构的专门建模是否优于通用界面操作框架。

**实验想回答的问题**

- SheetCompass相较于静态代码生成方法和采用“规划—行动—观察”闭环的表格智能体，能否在不同电子表格基准、不同模型容量以及多测试用例约束下，更可靠地完成可执行且功能正确的操作？
- 层次关系图、双层记忆和多智能体工作流分别贡献了什么，以及系统面对跨表依赖时，结构边、语义边、迭代推理和图构建超参数如何影响结果？

**实验实现**

实验以GPT-5作为主要闭源骨干模型，并以成本较低、容量更受限的GPT-4o-mini检查框架能否跨模型规模工作；但结果段使用了“GPT-4 backbone”这一表述，节选没有澄清它是否指GPT-4o-mini。评测在SCB、SB和SheetRM上进行，SB每项任务运行三个独立测试用例；主实验比较静态生成与动态交互基线，消融实验则分别移除层次关系图、双层记忆、多智能体工作流及其内部模块。超参数分析考察推理轮数$\tau$、图节点置信阈值$\alpha$和子图种子阈值$\lambda$。节选未报告数据划分、重复运行次数、随机种子、置信区间、显著性检验、提示模板、运行预算或各方法是否使用完全一致的工具权限。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 完整移除层次关系图 | 相对完整模型，移除层次关系图后，SCB的$\mathrm{pass@1}$下降14.9个百分点，SheetRM的$\mathrm{pass@1}$下降10.9个百分点，SB硬约束下降7.5个百分点；作者将其描述为主要组件中最明显的退化。 | 该消融隔离了显式表格拓扑对系统的整体作用。三个数据集均下降，说明图结构不是只针对某一基准的附加特征，而是为后续搜索、代码生成和验证提供共同的结构依据。不过一次移除整张图也同时删除了结构边与语义边，不能单独确定哪类关系造成了主要收益。 | 第4.3.1节，Table 2<br><span class="experiment-evidence">Completely removing the hierarchical graph causes the sharpest performance drop, lowering the pass@1 on SCB and SheetRM by 14.9% and 10.9% respectively, while reducing the hard restriction on SB by 7.5%.</span> |
| 分别移除多智能体工作流中的Explorer与Reflector | 移除Explorer后，SCB的$\mathrm{pass@1}$降至64.8%；移除Reflector后，SheetRM的$\mathrm{pass@1}$降至45.1%。 | 两个细粒度消融检验角色是否只是重复调用模型。Explorer缺失主要削弱候选执行路径的启发式搜索，Reflector缺失则削弱对运行结果和结构约束的独立核验，因而结果支持“探索”和“纠错”承担不同职责。不同数据集上的受影响指标不同，也提示角色价值与任务类型相关，不能把单个分数下降直接解释为普遍的因果效应。 | 第4.3.4节，Table 2<br><span class="experiment-evidence">Removing the explorer decreases the SCB pass@1 to 64.8%, as the system loses the heuristic exploration needed to discover plausible execution paths. Meanwhile, removing the reflector primarily harms performance on the SheetRM pass@1, driving it down to 45.1%.</span> |

**定性案例**

- Figure 6展示跨表收入计算：系统最初把介于0和1之间的折扣值0.15误当作绝对金额，生成$\mathrm{revenue}=\mathrm{quantity}\times\mathrm{retail\ price}-\mathrm{discount}$。该公式语法正确且可执行，所以仅靠运行成功无法发现语义错误；Reflector结合数值尺度和商业规则识别冲突，将反馈传回下一轮，随后系统把该节点重新解释为折扣率，改为$\mathrm{revenue}=\mathrm{quantity}\times\mathrm{retail\ price}\times(1-\mathrm{discount})$并通过验证。该案例说明闭环验证能够利用领域常识修复“可运行但含义错误”的程序，但单个成功案例不能量化这类纠错在整个测试集中的发生频率。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work develops hierarchical relation graphs to support agentic reasoning over spreadsheets.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`d752c1bb6328cbefba10a53a51e882609e5943b4de17bb801dec9e6fb871e69c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
