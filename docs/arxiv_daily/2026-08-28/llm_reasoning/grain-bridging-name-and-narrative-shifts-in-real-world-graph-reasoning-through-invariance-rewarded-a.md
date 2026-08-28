---
title: "[论文解读] GRAIN: Bridging Name and Narrative Shifts in Real-World Graph Reasoning through Invariance-Rewarded Agentic RL"
description: "[arXiv 2608.27142][LLM Reasoning] 本文关注大语言模型在图结构不变、但节点名称或任务叙述发生变化时推理性能骤降的问题，并探索以结构不变性奖励训练单智能体，使其稳定完成文本到图结构的解析与工具调用。"
arxiv_id: "2608.27142"
announcement_date: "2026-08-28"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:36:10.984368+00:00"
source_sha256: "26e4ffab5d09516abcdeb7b988ba47df4a3ffc453c3283cdd52ecd808b70a15a"
tags:
  - "LLM Reasoning"
  - "LLM Agent"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "大语言模型图推理"
  - "语义解析"
  - "图中间表示"
  - "结构不变性"
  - "节点标签敏感性"
  - "任务形式偏移"
  - "分布外泛化"
  - "工具增强推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.27142</p>

# GRAIN: Bridging Name and Narrative Shifts in Real-World Graph Reasoning through Invariance-Rewarded Agentic RL

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Zike Yuan, Han Zhang, Jianzhi Yan, Le Liu, Cai Ke, Huozhi Zhou, Jian Xie, Jiran Yin, Yukun Cao, Yue Yu, Hui Wang, Ming Liu, Bing Qin</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Harbin Institute of Technology, Shenzhen, China；Affiliation: Peng Cheng Laboratory, Shenzhen, China；Affiliation: Xidian University, Xi’an, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27142v1) · [PDF 下载](https://arxiv.org/pdf/2608.27142v1) · **关键词** 大语言模型图推理, 语义解析, 图中间表示, 结构不变性, 节点标签敏感性, 任务形式偏移, 分布外泛化, 工具增强推理<br>


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

本文关注大语言模型在图结构不变、但节点名称或任务叙述发生变化时推理性能骤降的问题，并探索以结构不变性奖励训练单智能体，使其稳定完成文本到图结构的解析与工具调用。

**不用术语来说**：同一张图可以用编号、人物名或带噪声的现实故事来描述；虽然这些说法不同，节点之间的连接关系和正确答案并未改变，但大语言模型常把表面措辞当成解题线索，因而在换名或换一种叙述后出错。传统图算法不受名称影响，却必须先获得正确的图；如果模型在从文本提取节点和边时就出了错，后续算法再可靠也无法补救。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者在底层图结构与语义保持不变的受控同构设置中，将鲁棒性问题明确拆分为节点标签变化与任务表述变化，并构建覆盖六类图问题、31个现实原型及显式分布外划分的 GRIT，以系统诊断模型对这些表面变化的敏感性。
- 作者提出单智能体强化学习框架 GRAIN，把图推理显式分解为语义解析和算法执行，并以中间图是否匹配真实拓扑为结构不变性奖励，从训练目标上鼓励模型恢复结构、正确调用工具，而非记忆名称和叙述模板。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型在真实文本中的图推理：输入不一定是规整的边列表，而可能是含别名、自然语义和不规则命名的叙事，模型需要先恢复节点及其关系，再完成连通性、路径或更复杂的图计算。传统确定性图算法只依赖拓扑结构，因此对节点改名通常不敏感；真正脆弱的环节是大语言模型将文本转换为图结构的过程。已有基准多采用清洗过的标识符和固定模板，因而可能高估模型面对节点命名变化、任务表述变化、图规模增长及高计算复杂度问题时的可靠性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**图推理**

把对象视为节点、把对象间关系视为边，并依据所得拓扑结构回答问题。它覆盖连通性、路径等基础任务，也可包含计算代价更高的组合优化问题。

</div>
<div class="concept-item" markdown="1">

**语义解析与图中间表示**

语义解析负责从自然语言中识别实体和关系，并将其转换成可由算法处理的结构化图；该结构是语言理解与确定性求解器之间的中间表示。若此处漏边、错认别名或混淆节点，后续算法即使完全正确也会得到错误答案。

</div>
<div class="concept-item" markdown="1">

**同构不变性与分布外泛化**

若两个样例仅改变节点名称、叙述方式或边的描述次序，而保持相同拓扑和任务语义，合理的推理结果应保持不变，这里称为结构不变性。分布外泛化则考察模型能否把这种能力迁移到训练中未见的命名、叙事形式或更大规模图。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是文本化的图任务：输入为描述节点、边及待求问题的自然语言查询，其中节点可能采用随机标识、语义名称或存在别名与噪声，任务也可能由标准模板改写为真实叙事；输出为对应图问题的最终答案。核心设定是对同一底层拓扑构造多种保持同构的命名与叙事视图，用它们区分模型究竟掌握了结构规则，还是依赖表面词形和固定模板。本文将完整推理拆成“语言到结构”与“结构到答案”两段：大语言模型承担语义解析、图中间表示构建和工具选择，确定性求解器承担算法执行；评估重点包括节点标签敏感性、任务形式敏感性，以及面对未见表述和超出训练规模的图时的结构泛化。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Fatemi et al. (2024)**: 该工作研究图的文本编码方式对大语言模型性能的影响，说明标签或序列化形式会显著改变推理结果；本文进一步关注从标准模板迁移到带命名不规则与语义噪声的真实叙事时产生的分布偏移。
- **GraphToken（Perozzi et al., 2024）**: GraphToken通过参数高效的结构编码向模型注入图信号，以减少对原始文本序列化的依赖；但原文指出，其面对多样节点命名约定的稳健性仍未得到解决，这正是本文所研究的表面变化之一。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

社交网络分析、知识图谱推理和软件依赖管理等应用需要从自然语言中恢复图并进行可靠计算。现实输入往往包含不规则命名、别名冲突、语义噪声和非标准故事化表述；即使底层拓扑完全相同，这些变化也会使大语言模型的输出明显波动，因此在干净模板上表现良好并不足以保证实际可用性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **文本化图推理与 CoT／监督微调**：这类方法把图序列化为文本，让模型通过自由形式的思维链直接推理，或使用带答案、推理轨迹及工具调用示例的数据进行监督微调，使模型学习从文本问题到答案或执行步骤的映射。
- **多智能体工具增强图推理**：多个智能体通过多轮协作分别解析问题、检查结构、规划步骤并调用确定性图算法，以外部工具承担拓扑计算，并借助角色分工或相互校验提高正确率。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有文本化研究主要考察序列化或标签方式，却较少同时覆盖从标准模板到带噪现实叙述的分布变化；CoT 将结构提取、逻辑判断和计算混在自由文本中，缺少可验证的中间表示，而监督微调又容易拟合表面模式，导致模型面对同构换名、更大规模图或高计算复杂度问题时泛化下降。
- 多智能体方案可通过工具和交叉检查缓解部分解析错误，但依赖多轮交互，带来较高的令牌成本与延迟，难以满足实时部署；它也没有从根本上保证单个模型学会名称无关、叙述无关的文本到结构映射。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种统一机制：既能在保持底层拓扑不变的条件下系统评估节点命名与任务叙述变化，又能直接监督中间结构是否恢复正确，并将可靠的解析、工具选择和参数构造能力压缩到低延迟的单智能体中。尤其缺少针对“答案可能偶然正确、但所解析图已经错误”这一情况的结构级训练信号。

</div>
<div markdown="1"><span>核心问题</span>

能否把现实图推理建模为可检查的“语言到结构、结构到算法执行”流程，并通过以真实拓扑为参照的强化学习奖励，使单个大语言模型在节点标识、叙述形式和图规模发生分布外变化时仍保持准确，同时避免多智能体系统的交互开销？

</div>
<div markdown="1"><span>作者直觉</span>

确定性图算法只依赖节点和边的关系，不在意节点叫“A”、随机编号还是人物姓名，因此真正脆弱的环节是模型从语言恢复拓扑的过程。若训练时对同一结构反复更换名称和故事，并依据生成的中间图是否与真实图同构来奖励模型，任何只记住词语或模板的策略都难以持续获奖；模型必须抓住“谁与谁相连”等稳定关系。随后把计算交给图工具，便可让语言模型专注于其更适合的语义解析与信息抽取，同时以单次智能体流程替代昂贵的多轮协作。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

GRAIN把图推理拆成“语义解析—结构校验—工具执行—答案生成”的单智能体流程。输入是以自然语言叙述的图问题，其中节点可能采用规范名称、随机编号、语义名称或含别名的混合名称；模型先把文本恢复为结构化图，再调用本地 Python 图算法求解，而不是让大语言模型直接在长文本中完成全部组合计算。训练分为工具使用监督微调与基于 ARPO 的智能体强化学习两阶段，核心监督信号不仅检查最终答案，还依据中间图是否匹配真实拓扑给予 Structure Invariance Reward，从而促使模型忽略命名和叙述表面的变化。

直观地说，GRAIN让语言模型承担它更擅长的“读懂题目并整理数据”，让确定性程序承担“按图计算”。同一张图即使把节点名从城市改成随机数字，或换一种应用故事，其内部连接关系仍应被解析成相同拓扑；训练奖励正是利用这一点约束模型。该设计也避免多智能体之间反复传递图信息所造成的延迟和信息丢失，但所给章节没有展示 Structure Invariance Reward 或 ARPO 的完整数学定义，因此不能据此复原更细的奖励组合与更新公式。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 接收叙事化图问题

模型识别问题属于中心性、最短路径、旅行商、最小图着色、广度优先遍历或顶点覆盖中的哪类任务，并定位构图及求解所需的信息。训练数据会用规范名称、随机编号、语义名称和含别名的混合名称表达相同类型的拓扑。

<div class="method-step__io" markdown="1">

**输入**：一个自然语言图推理问题，包括实体、边或权重、查询条件，以及可能变化的节点命名和现实场景表述。<br>
**输出**：待解析的任务语义、实体关系和求解要求。

</div>

**直观理解**：这一步先判断“题目在问什么”，同时把城市、服务器或人物等故事对象视为图节点，而不把它们的具体名字当作解题规律。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 文本到结构化图的语义解析

单个语言模型生成符合工具接口要求的 JSON 图表示，恢复节点集合、边集合及必要的整数权重，并处理同一节点的别名。监督微调首先训练合法结构化输出和工具调用语法，强化学习随后提高跨命名与跨叙述的一致解析能力。

<div class="method-step__io" markdown="1">

**输入**：已识别的实体、关系、边权、方向性和查询参数。<br>
**输出**：可被程序读取的预测图及任务参数。

</div>

**直观理解**：相当于把一段故事整理成标准表格：谁与谁相连、连接成本是多少、从哪里开始以及要求什么答案。只要故事描述的是同一张图，整理后的结构原则上就应相同。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 中间拓扑校验与强化学习奖励

训练时将预测中间图与真实拓扑比较，并通过 Structure Invariance Reward 奖励正确且不随表面形式变化的结构恢复；ARPO使用基于 GRPO 的组相对估计器，并加入分支感知的搜索与优化机制。所给文本只说明奖励为 Graph Correctness、工具与环境同步以及分支搜索设置，未给出奖励各项的精确计算式。

<div class="method-step__io" markdown="1">

**输入**：模型预测的结构化图、数据生成阶段保留的真实图拓扑，以及同一拓扑的多种命名或叙述变体。<br>
**输出**：轨迹级奖励与用于更新语言模型策略的相对优势信号。

</div>

**直观理解**：系统不只检查最后答案是否碰巧正确，还检查模型是否真正画对了图。这样能惩罚“算对结果但读错部分关系”的脆弱捷径，并让不同名字包装下的同一拓扑得到一致处理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 工具执行与答案返回

模型调用本地 Python 环境中的确定性图算法执行计算，并把工具结果转换为用户要求的答案。训练外推时，即使节点数超过训练范围 $|V|\leq 40$，复杂图计算仍由外部算法承担，语言模型主要负责结构提取和调用协调。

<div class="method-step__io" markdown="1">

**输入**：结构化图、任务类型和查询参数。<br>
**输出**：相应图任务的最终预测，如最短路径、遍历顺序、着色数、覆盖集、关键节点或旅行商回路。

</div>

**直观理解**：语言模型负责把题目翻译成机器可算的图，程序则像计算器一样完成可靠求解。这种分工减少了模型在大图上逐步心算造成的错误，也不需要多个智能体反复交接信息。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标分两层。第一阶段以监督微调让基础模型模仿正确轨迹，获得合法 JSON 图生成、工具调用和答案组织能力；第二阶段从该检查点出发，用 ARPO 对多条智能体 rollout 做组相对优化，主要奖励预测图与真实拓扑的一致性及工具执行正确性。多种节点命名和场景叙述使策略必须在表面变化下恢复同一结构，而不是记忆固定模板；课程学习先在较小图 $N\in[4,14]$ 上稳定格式与调用语法，再扩展到完整训练分布 $N\in[10,40]$。由于原文节选没有给出 Structure Invariance Reward、总奖励或 ARPO 策略损失的显式公式，本分析不补造方程，也无法确定各奖励项权重及优势计算细节。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 结构化语义解析与工具接口**

模型把叙事文本序列化为合法 JSON 图表示，并通过工具调用协议把图、任务类别和查询参数传给本地 Python 环境。第一阶段监督微调专门建立结构化生成和工具调用能力，推理时模型无需自行模拟完整图算法。

> 直观理解：该模块是自然语言与图算法之间的翻译器；如果翻译出的节点、边或权重有误，再精确的算法也会得到错误答案。

**2. Structure Invariance Reward**

该奖励利用训练样本的真实拓扑直接评估预测中间图，并要求同一拓扑在不同节点命名和现实叙述下保持一致。它将监督位置从仅有最终答案前移到图恢复过程，但原文节选未明确给出节点、边、权重及最终答案奖励的组合公式。

> 直观理解：它要求模型学会“认连接关系而不是认名字”。因此，把节点改成随机数字或给同一节点使用多个别名时，模型仍应恢复相同的图。

**3. ARPO 智能体强化学习**

ARPO从工具使用 SFT 检查点热启动，使用 GRPO 估计器进行组相对策略优化，并配置分支搜索：每个提示生成 $G=8$ 条 rollout，beam size 为 2、分支概率为 0.5、熵权重为 0.2。消融描述将其称为 branch-aware optimization，但所给章节没有提供分支优势如何聚合或策略损失如何定义。

> 直观理解：普通强化学习只比较若干完整答案，ARPO还鼓励模型探索不同的解析和工具调用分支，再用结构正确性选择更可靠的行为。其目的不是增加多个智能体，而是在一个智能体内部改进探索。

**训练与推理**

训练阶段一对 Qwen-3-Base 4B 和 Llama-3.2-Base 3B 进行全参数 SFT，使用带结构化图、工具调用与推理轨迹的样本，使模型先学会稳定输出接口格式。阶段二以工具使用 SFT 检查点热启动 ARPO：先在 $N\in[4,14]$ 的小图上进行稳定化训练，再在 $N\in[10,40]$ 的完整分布上优化；主阶段按每种任务和图规模采样两个不同底层图，并通过多种命名与叙述变体提供不变性训练信号。每个提示进行 $G=8$ 次 rollout，模型与本地 Python 环境同步交互，结构正确性和工具执行结果产生组相对奖励，随后更新单智能体策略。

推理时只运行一个经过训练的模型。它读取自然语言问题，生成结构化图和调用参数，与本地 Python 工具进行若干轮交互，取得确定性算法输出后形成最终答案；无需访问训练时的真实拓扑，因为真实拓扑比较仅用于奖励计算。对于超出训练节点规模的大图，外部算法继续承担搜索或组合计算，模型的主要负担仍是从文本中准确提取节点、边、权重和查询条件。

**复现信息**

公平解释结果所需的关键设置如下：SFT采用全参数微调、BF16 精度、15,000 token 上下文、全局 batch size 8、训练 3 个 epoch、学习率 $7\times10^{-6}$，并使用 cosine 调度和 ZeRO-3 Offload。RL采用 actor 学习率 $1\times10^{-6}$、train batch size 16、mini-batch size 4、训练 2 个 epoch；提示与回复上限分别为 24,000 和 12,000 tokens，总上下文为 36,000 tokens。KL 系数设为 0.0，意味着策略不受显式 KL 正则约束，而主要由组相对奖励约束；rollout 由 vLLM 执行。

图数据由 NetworkX 随机模型生成，边概率 $p\in[0.1,0.3]$，加权任务的整数权重均匀采自 $[1,10]$，并通过拒绝采样保证无向图连通或旅行商图满足相应连通要求。确定性评测规定 BFS 邻居按字典序访问，TSP 用动态规划求精确最小 Hamilton 回路，图着色通过带回溯的策略求精确色数；这些规则避免多个同样正确的解造成评测歧义。OOD 划分明确留出 24 个场景模板和命名分布，而非随机拆分，因此主要检验结构解析能否迁移到未见叙述。全部实验使用配备 4 张 NVIDIA A100 80GB GPU 的计算节点，但表中 SFT 配置列为 2 张 A100；两处记录对应的具体资源分配关系在节选中未进一步解释。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GRIT是主要训练与评测基准，包含最短路径、图着色、旅行商问题、顶点覆盖、广度优先搜索和中心性六类任务，并用31种现实场景承载图结构。每个基础实例交叉生成两种题面形式与四种命名方案，共8个视图，用于分别检验任务表述变化和节点标识符变化。训练集含2160张图、17280个问题，节点数为4–40；常规测试集含360张图、2760个问题，节点数为10–40。图由确定性模板注入文本，答案由符号求解器生成，因此该数据集主要测试文本到图结构的稳健解析，而不是开放式语言生成。
- GRIT Large Test包含120张图和960个问题，节点数为40–60，超出主要训练图规模，用于测试长度与规模泛化。GRIT OOD Test包含180张图和1440个问题，节点数为10–40，并显式留出训练阶段未出现的24种场景模板及命名分布，用于区分真正的结构迁移与对领域措辞、模板或别名模式的记忆。
- G-REAL是MA-GTS原工作使用的外部数据集。论文对每个任务随机抽取100道、覆盖不同节点规模的问题进行零样本评测；其作用是检查GRAIN的结果是否仅来自对GRIT生成分布的适配。该摘录只明确报告了图着色、旅行商问题和顶点覆盖的分项成绩，未完整给出所有任务及样本总数。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（Accuracy）**

最终答案与确定性符号求解器产生的标准答案一致的比例，衡量从文本解析、图构建、工具执行到答案输出的端到端正确性；它不能单独区分错误发生在解析还是算法调用阶段。 （越高越好，因为更高比例表示完整推理流水线成功完成并输出正确答案。）

</div>
<div class="metric-item" markdown="1">

**OOD差距（OOD gap）**

模型在分布内评测与分布外评测之间的性能下降，用来衡量模型对未见场景、命名分布或题面变化的敏感程度。 （越低越好，因为较小差距意味着性能较少依赖训练阶段出现过的语言表面形式。）

</div>
<div class="metric-item" markdown="1">

**推理延迟（Latency）**

完成一次端到端解题所需时间，用于衡量单智能体与多智能体流程的实际运行成本。附录还报告平均时间和第90百分位时间，以观察典型成本和长尾延迟。 （越低越好，因为较低延迟意味着更少的智能体轮次、通信和失败重试，更适合实际部署。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### GRAIN与多智能体基线的总体效果和效率比较

<div class="result-value" markdown="1">

作者报告GRAIN的准确率比多智能体基线高16.45%，同时推理延迟约低24%。

</div>

该结果支持单智能体经过针对性强化学习后，可以同时改善正确率和运行效率，而不必依赖多轮智能体协作。需要注意，当前摘录未提供对应主表、绝对准确率、绝对延迟、误差范围或显著性检验；因此它表明作者报告的总体优势，但不足以判断优势是否在每项任务和每种图规模上都一致。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GRAIN outperforms multi-agent baselines by 16.45% in accuracy with approximately 24% lower latency.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 相对于监督微调模型的分布外结构泛化

<div class="result-value" markdown="1">

作者报告SFT模型的OOD差距为15.77%，GRAIN将其降至7.80%，绝对减少7.97个百分点，约缩小一半；同时作者称其在超出训练分布的大图上仍保持稳健。

</div>

OOD差距明显缩小，与“结构不变性奖励促使模型学习文本到图的映射，而不是记忆场景措辞”这一解释一致。它说明GRAIN对分布变化更不敏感，但不能仅凭差距证明模型已经恢复了完全正确的中间图，也不能排除分布内性能变化对该差距的影响；摘录没有给出两端的绝对准确率和逐任务分解。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Furthermore, it demonstrates superior structural generalization, halving the out-of-distribution (OOD) gap of SFT models (from 15.77% to 7.80%) and maintaining robustness on large-scale graphs beyond the training distribution.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 完全未见的G-REAL数据集零样本迁移

<div class="result-value" markdown="1">

GRAIN-4B在覆盖全部节点规模的G-REAL零样本评测中达到86.60%准确率；作者进一步报告图着色为98%、TSP为80%、顶点覆盖为82%。

</div>

外部数据上的较高准确率削弱了“GRAIN只记住GRIT模板”的解释，说明其文本到图结构的解析能力具有一定跨数据集迁移性。不过，该表把GRAIN在G-REAL全规模数据上的86.60%与MA-GTS在GRIT OOD小图子集上的82.79%并列，两者并非相同数据、相同样本难度或相同评测条件，因此不能把这两个数字直接解释为严格的模型胜负差距。

<div class="result-source" markdown="1">

来源：Appendix E, Table 17及其结果分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

First, the single-agent GRAIN achieved a commanding 86.6% accuracy on the entirely unseen G-REAL dataset (with Graph Coloring at 98%, TSP at 80%, and Vertex Cover at 82%).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给摘录缺少完整的主实验表、逐任务结果、随机种子、方差或置信区间，也没有提供结构不变性奖励、语义解析监督和工具执行设计的独立消融。因此无法从当前材料定量判断每个组件各自贡献多少；为避免杜撰，消融列表留空。
- 部分比较并非严格同条件：GRAIN在G-REAL全规模样本上评测，而MA-GTS的补充结果来自GRIT OOD中$|V|\leq20$的小图子集；附录F也明确指出双方训练方式、骨干初始化和智能体组织不同。因此这些结果适合作为迁移与流程可靠性诊断，不足以单独证明单智能体架构在所有公平控制条件下必然优于多智能体架构。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- MA-GTS：推理时采用六智能体分工和工具调用的图任务框架，是检验“复杂多智能体分解是否优于经过强化学习优化的单智能体”的主要比较对象。附录还使用相同的Qwen3-4B-Instruct骨干在GRIT Test与OOD输入上诊断其迁移可靠性。
- SFT模型：仅通过监督微调学习任务映射，不使用论文提出的结构不变性奖励。与它比较OOD性能差距，可判断强化学习目标是否减少了对训练题面和命名表面模式的依赖。
- GRAIN-4B：论文提出的单智能体系统，也是核心被评模型。它将语言模型的职责集中在语义解析和工具调用上；确定性图工具负责后续算法计算。该设置用于验证训练出的单条可执行轨迹能否替代高延迟的多智能体协作。

**实验想回答的问题**

- 面对节点命名变化、标准题面与叙事题面切换，以及训练中未见的场景模板时，GRAIN能否比监督微调模型和多智能体图推理框架更稳定地把文本还原为正确图结构，并得到正确答案？
- 单智能体GRAIN能否在降低推理延迟的同时保持跨数据集、跨图规模的泛化能力；多智能体基线的主要瓶颈究竟是图算法本身，还是前序实体对齐、工具调用与智能体间状态传递？

**实验实现**

GRIT的底层图通过NetworkX随机模型生成；Erdős–Rényi图的边概率为$p\in[0.1,0.3]$，加权任务的边权从$[1,10]$均匀采样，并通过拒绝采样保证无向图连通或TSP图强连通。叙事文本不是由LLM自由生成，而是由严格的模板槽位填充器注入拓扑，从而确保文本与底层图同构。为使评测答案唯一，BFS按节点名称的字典序访问邻居，TSP使用动态规划求精确最小哈密顿回路，图着色通过带回溯的策略求精确色数。外部泛化实验在G-REAL上按任务随机抽取100题；由于多智能体运行成本随图规模增长，MA-GTS在GRIT OOD上的补充评测仅采用$10\leq|V|\leq20$的低难度子集，因此该结果不能被视为完全同规模、同数据条件下的直接排名。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 附录F给出了流程级失败分析：MA-GTS在成功执行原生工具调用的样本子集上可以获得正确结果，但大量输入在到达该阶段前已因任一智能体报错、仅输出文本式调用或算法代理错误而终止。该案例说明多智能体基线的主要障碍是端到端轨迹可靠性，而不是所有图算法都无法求解；不过，成功调用后的条件准确率受到样本选择影响，不能与总体准确率直接比较。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Proposes RL with a structure-invariance reward to train a tool-executing LLM agent for robust semantic parsing and graph reasoning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`26e4ffab5d09516abcdeb7b988ba47df4a3ffc453c3283cdd52ecd808b70a15a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
