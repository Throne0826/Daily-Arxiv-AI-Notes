---
title: "[论文解读] RACER: Reinforced Agent Collaboration for Explainable Reasoning on Knowledge Graphs"
description: "[arXiv 2608.29263][Multi-Agent] 原文未明确报告。"
arxiv_id: "2608.29263"
announcement_date: "2026-09-01"
primary_category: "multi_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:58:08.852448+00:00"
source_sha256: "bf2d133651a54f78a2262a04b2d82ffd1bf888ef36173a274a4f7433823eeb7b"
tags:
  - "Multi-Agent"
  - "LLM Reasoning"
  - "强化学习"
  - "LLM 其他"
  - "大语言模型"
  - "知识图谱"
  - "检索增强生成"
  - "多跳推理"
  - "多智能体协作"
  - "可解释推理"
  - "常识问答"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">Multi-Agent · arXiv 2608.29263</p>

# RACER: Reinforced Agent Collaboration for Explainable Reasoning on Knowledge Graphs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Yuwei Lou, Hao Hu, Yuzhou Jiang, Zongfei Zhang, Liang Wang, Jincai Liu, Jidong Ge, Xianping Tao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: State Key Laboratory for Novel Software Technology, Nanjing University, China Independent Researcher Chinaunicom Software Nanjing Branch；Affiliation: State Key Laboratory for Novel Software Technology, Nanjing University, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29263v1) · [PDF 下载](https://arxiv.org/pdf/2608.29263v1) · **关键词** 大语言模型, 知识图谱, 检索增强生成, 多跳推理, 强化学习, 多智能体协作, 可解释推理, 常识问答<br>


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

本文研究知识图谱增强的大语言模型推理：当问题需要跨越多个事实进行常识或领域推断时，仅依赖大语言模型参数中的知识容易产生幻觉；普通检索增强生成又主要从分散的非结构化文本中寻找证据，难以显式表达事实之间的关系。知识图谱将事实组织为“头实体—关系—尾实体”三元组，可把答案依据表示为可核验的多跳路径。由于先进大语言模型通常只能通过 API 访问，本文采用无需修改模型参数的提示增强设定：先从大规模知识图谱中搜索并整理与问题相关的路径，再将其转化为自然语言证据交给大语言模型作答，同时利用多智能体分工完成路径搜索、提示构造、答案生成与结果审查。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**知识图谱与多跳推理**

知识图谱以“头实体—关系—尾实体”三元组保存原子事实，并通过共享实体连接成图。多跳推理是沿若干关系边组合多个事实，例如先确定某对象的类别，再依据该类别的属性回答问题。

</div>
<div class="concept-item" markdown="1">

**检索增强生成**

检索增强生成先从外部知识源取回与问题相关的材料，再把材料作为上下文交给大语言模型生成答案。它能减少仅凭模型内部记忆作答所造成的幻觉，但检索结果会受到语料质量、知识分散程度和搜索空间大小的影响。

</div>
<div class="concept-item" markdown="1">

**多智能体协作**

多智能体系统把复杂任务拆给具有不同职责的语言模型角色，并通过信息传递或反馈形成协作流程。本文所需的核心认识是：路径检索、提示组织、答案生成和答案审查可以由不同角色负责，从而避免单一模型同时承担全部环节。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个需要外部常识或多跳知识的问题、可供检索的大规模知识图谱，以及通过接口调用的固定大语言模型；具体实验面向 CommonsenseQA 和 OpenBookQA 所代表的问答场景。系统需要从图中找出与问题语义相关且逻辑连贯的多条推理路径，将图结构证据整理为适合语言模型使用的自然语言知识，并经过多角色协作生成和审查最终答案。输出不仅包括答案，还应提供可追溯至知识图谱路径的解释依据。该设定默认知识图谱中的结构化事实可作为外部证据，并重点解决图搜索空间巨大、人工固定提示缺乏语境适应性以及单智能体执行效率和可靠性有限的问题；所给章节未形式化规定候选答案格式、路径长度或图谱完备性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **KGR**: KGR 使用知识图谱逐步提取和精炼知识，并对大语言模型生成的初始回答进行追溯式验证，与本文同属无需训练闭源大模型的知识图谱提示方法。本文进一步关注可学习的路径搜索、多路径知识精炼以及多智能体协作，而不是主要依靠单一大语言模型完成知识利用。
- **KnowGPT**: KnowGPT 通过机器学习方法或多臂老虎机从知识图谱提取路径，并结合上下文模块和预先设计的模板构造提示，是 RACER 最直接的路径检索与提示增强参照。原文指出其模板仍以预设计和动态选择为主，实践表现受固定模板与检索效率限制；RACER据此引入语义感知动作剪枝、教师引导强化学习和可反馈的多角色流程。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大型语言模型在缺少训练数据或需要整合多跳领域知识时容易产生幻觉，导致答案缺乏事实依据且难以核验。检索增强生成虽然能够引入外部知识，但相关信息可能分散、质量不一，单纯依赖文本检索难以稳定找到支持复杂推理的完整证据链；知识图谱以$(实体，关系，实体)$三元组保存结构化事实，具有可验证、可更新和支持多跳推理的优势，因此有必要研究如何让语言模型更有效地利用知识图谱完成可解释问答。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于检索增强生成与知识图谱增强的语言模型**：这类方法先从外部语料或知识图谱中检索与问题相关的信息，再将其组织到提示词或模型输入中，由语言模型生成答案。代表性方向包括将固定知识注入预训练、利用图结构辅助内部推理，以及使用GraphRAG、CoK等方法增强或核验生成结果。
- **基于知识图谱路径抽取与模板提示的方法**：这类方法在知识图谱中寻找连接问题实体与候选答案的推理路径，将路径转写为自然语言片段或提示模板，再交给语言模型完成推理。KGR尝试逐步抽取和精炼知识，KnowGPT则结合机器学习方法、预设模板和动态选择机制来生成推理提示。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 知识图谱规模庞大，现有路径抽取方法面对巨大的动作和搜索空间时效率有限，往往难以快速筛选出与当前问题真正相关的多跳路径；其直接后果是检索成本上升，并可能把噪声知识传递给语言模型。
- 许多方法依赖人工设计的固定模板或单一语言模型代理，提示内容难以随问题和中间结果自适应调整，也没有充分利用多个角色之间的分工、反馈和复核；因此路径搜索、知识组织与最终答题之间容易脱节，单一路径还可能放大早期检索错误。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未充分解决一个组合性问题：如何在大规模知识图谱中以可控成本学习问题条件下的高质量推理路径，同时保留多条互补证据，并通过能够动态反馈的协作机制把这些证据转化为适合语言模型执行和核验的提示。换言之，仍缺少一个把可学习的路径搜索、跨任务经验复用、多路径知识精炼与端到端多代理协作统一起来的框架。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一种知识图谱增强的推理系统，使其根据问题自适应缩小路径搜索空间、利用历史任务积累的信息选择和精炼多条推理路径，并通过不同代理的协作与批评反馈动态生成可验证的提示，从而同时提高复杂问答的准确性、效率和可解释性？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把推理过程拆成互补的决策环节：先用语义感知的动作剪枝减少明显无关的图搜索，再用教师引导的强化学习学习哪些路径更值得探索；随后用跨任务共享记忆保存边的历史统计，使后续任务不必从零开始，并通过双重注意力整合多条候选路径，降低单一路径失误的影响。最后，GraphAgent、TemplateAgent、AnswerAgent和CriticAgent分别负责知识搜索、提示组织、回答生成和结果复核，形成反馈闭环。直观地说，该设计不是让一个模型一次性猜出答案，而是让系统先找证据、再组织证据、独立作答并检查答案，使检索经验和错误反馈能够反过来改善后续推理。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

RACER 是一个面向知识图谱（Knowledge Graph，KG）可解释推理的强化多智能体框架。给定自然语言问题、候选答案以及知识图谱，系统先用语义感知剪枝压缩图搜索空间，再通过教师引导的强化学习提取连接问题实体与候选答案实体的推理路径；随后利用跨任务共享记忆图记录边的历史表现，并通过双重注意力从多条候选路径中筛选紧凑且互补的知识；最后由 GraphAgent、TemplateAgent、AnswerAgent 和 CriticAgent 协作，把图结构路径转化为语言模型可理解的知识模板，生成并检查答案。直观而言，RACER 不是让单个模型在整张图中盲目寻找一条路，而是先缩小可行道路，再参考过去哪些边有效，综合多条道路，最后由不同角色分别负责找路、组织说明、答题和复核。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问题与图实体表示

系统使用预训练语言模型（PLM）将查询、关系和实体编码到统一语义空间，并把当前节点嵌入、查询嵌入和历史路径编码组合成强化学习状态 $s_{t}=[\mathbf{v}_{t};\mathbf{q};\mathbf{h}_{t}]$。在多项选择问答中，由于正确目标事先未知，系统将每个候选答案映射为相应的图实体，并分别评估通向各候选实体的路径。

<div class="method-step__io" markdown="1">

**输入**：输入包括自然语言查询 $q$、知识图谱中的源实体集合 $\mathcal{Q}_{s}$、目标实体或候选答案实体集合 $\mathcal{Q}_{t}$，以及知识图谱中的节点、关系和边。<br>
**输出**：得到查询向量 $\mathbf{q}$、目标节点表示 $\mathbf{g}$、当前节点表示 $\mathbf{v}_{t}$ 以及用于路径搜索的状态 $s_{t}$。

</div>

**直观理解**：这一步相当于先把问题、图中的词和候选答案翻译成同一种“语义坐标”，这样系统才能判断一条关系或一个节点是否与问题相关。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 语义剪枝与教师引导的强化学习搜索

系统按照关系与查询、下一节点与查询、下一节点与目标之间的余弦相似度计算动作分数，只保留得分最高的 Top-$K$ 动作。训练时，先用 BFS 从源节点 $v_{0}$ 到目标节点 $v_{T}$ 求最短教师路径 $P^{*}=[v_{0},v_{1},\ldots,v_{T}]$；以概率 $p_{\mathrm{teacher}}$ 执行教师动作，以概率 $1-p_{\mathrm{teacher}}$ 从强化学习策略 $\pi_{\mathrm{RL}}$ 采样，从而在可靠先验与自主探索之间折中。

<div class="method-step__io" markdown="1">

**输入**：输入是当前节点 $v_{t}$ 的候选动作集合 $A=\{(n_{i},r_{i})\}_{i=1}^{M}$、查询表示 $\mathbf{q}$、目标表示 $\mathbf{g}$ 以及当前路径状态 $s_{t}$。<br>
**输出**：输出连接源实体与目标实体的一个或多个知识图谱推理路径，以及训练后的路径策略 $\pi_{\theta}$。

</div>

**直观理解**：剪枝像是在迷宫入口先挡掉明显无关的岔路；教师路径则像给学习者一条较短的示范路线，但模型仍保留一定概率自己尝试，以免只会机械模仿。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 共享记忆与多路径知识精炼

共享记忆图为每条边 $e=(h,r,t)$ 保存成功、失败和被剪枝拒绝的次数，并据此重新排序候选动作。系统在生成多路径时，前半段使用温度采样提高多样性，后半段使用贪心选择提高路径质量；随后用跨路径多头自注意力建模路径间的互补和冗余，再用查询—路径交叉注意力与可学习重要性评分联合筛选 Top-$k'$ 路径。

<div class="method-step__io" markdown="1">

**输入**：输入是查询 $q$、起始节点集合 $\mathcal{S}$、策略生成的候选路径集合 $\mathcal{P}=\{P_{1},\ldots,P_{N}\}$，以及共享记忆图中各边的历史统计。<br>
**输出**：输出较小的高质量路径子集 $\mathcal{P}^{*}\subseteq\mathcal{P}$，其中 $|\mathcal{P}^{*}|\ll k$，并为后续模板生成提供压缩知识。

</div>

**直观理解**：系统不会只相信第一条找到的路，而是先保留若干不同路线，再比较它们是否重复、是否互相补充、是否真正回答问题；共享记忆则像一份跨任务的“路线经验表”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多智能体模板生成、回答与反馈

GraphAgent 生成并精炼知识三元组序列；TemplateAgent 将其组织为逻辑知识路径，并结合共享记忆图转换为自然语言知识片段模板；AnswerAgent 根据模板回答问题并记录答案正确性；CriticAgent 检查推理过程与最终答案，输出决策 $d\in\{\mathrm{ACCEPT},\mathrm{UNSURE}\}$ 和置信度 $c\in[0,1]$。

<div class="method-step__io" markdown="1">

**输入**：输入是精炼路径 $\mathcal{P}^{*}$、共享记忆图中的统计信息、原始查询以及任务要求。<br>
**输出**：系统输出最终答案、可追溯的知识路径或自然语言知识模板，以及 CriticAgent 的接受或不确定判断；若判断为 UNSURE，则触发新的图搜索分支。

</div>

**直观理解**：四个角色像一个小型协作团队：一个负责查资料，一个负责把资料写成说明，一个负责作答，最后一个负责质检；答案不确定时，团队回到查资料环节重找证据。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 语义感知动作评分

$$
\operatorname{score}(n_i,r_i)=\alpha\cdot\operatorname{sim}(r_i,\mathbf{q})+\beta\cdot\operatorname{sim}(n_i,\mathbf{q})+\gamma\cdot\operatorname{sim}(n_i,\mathbf{g}),\qquad \alpha+\beta+\gamma=1
$$

**符号说明**

- $A=\{(n_i,r_i)\}_{i=1}^{M}$：当前节点可执行的 $M$ 个候选动作，每个动作包括下一节点 $n_i$ 和关系 $r_i$。
- $\mathbf{q}$：自然语言查询的稠密嵌入表示。
- $\mathbf{g}$：目标节点或候选答案实体的嵌入表示。
- $\operatorname{sim}(\cdot,\cdot)$：余弦相似度，用于衡量两个表示的语义相关性。
- $\alpha,\beta,\gamma$：三个相似度项的权重，且总和为 $1$。
- $K$：保留的最高分动作数量。

<div class="equation-explanation" markdown="1">

**直观理解**：这个公式把一条候选边的三个问题合并起来判断：关系是否贴合问题、下一节点是否贴合问题、下一节点是否接近目标。只保留最高分的 $K$ 条动作，可以在搜索前显著缩小分支数量，同时尽量保留语义相关路线。<br>
**原文位置**：第 3.1 节“Semantic Action Space Pruning”，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 强化学习总奖励

$$
\mathcal{R}=r_{\mathrm{step}}+r_{\mathrm{rel}}+r_{\mathrm{goal}}+r_{\mathrm{reach}},\qquad r_{\mathrm{rel}}=\lambda_{\mathrm{rel}}\cdot\operatorname{sim}(r_t,\mathbf{q}),\qquad r_{\mathrm{goal}}=\lambda_{\mathrm{goal}}\cdot\left(\operatorname{sim}(v_{t+1},\mathbf{g})-\operatorname{sim}(v_t,\mathbf{g})\right)
$$

**符号说明**

- $\mathcal{R}$：每一步行动获得的总奖励。
- $r_{\mathrm{step}}$：步长惩罚，用于抑制不必要的长路径探索。
- $r_{\mathrm{rel}}$：关系相似度奖励，鼓励选择与查询语义相关的关系。
- $r_{\mathrm{goal}}$：目标导向的稠密奖励，衡量下一节点相对于当前节点是否更接近目标。
- $r_{\mathrm{reach}}$：到达目标节点时给出的额外正奖励；原文将其定义为到达时为 $\lambda_{\mathrm{reach}}$，否则为 $0$。
- $\lambda_{\mathrm{rel}},\lambda_{\mathrm{goal}},\lambda_{\mathrm{reach}}$：分别控制关系奖励、目标接近奖励和到达目标奖励强度的超参数。
- $r_t,v_t,v_{t+1}$：第 $t$ 步 traversed relation、当前节点和执行动作后的下一节点。

<div class="equation-explanation" markdown="1">

**直观理解**：奖励函数同时惩罚绕远路、奖励选择相关关系、奖励在语义上靠近目标，并在真正到达目标时给予较大回报。这样策略优化的方向不是单纯追求某一种相似度，而是综合考虑效率、相关性和任务成功。<br>
**原文位置**：第 3.1 节“Reward Function Design”，公式（3）—（5）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：RACER 的路径策略通过强化学习最大化由总奖励 $\mathcal{R}$ 诱导的长期回报。每个状态包含当前节点、查询和历史路径，动作是在剪枝后的候选边中选择下一步；BFS 教师轨迹以概率 $p_{\mathrm{teacher}}$ 提供动作先验，教师动作获得固定正奖励 $R_{\mathrm{teacher}}=1.0$，其余步骤由策略网络探索。总奖励中的步长惩罚、关系相似度、目标接近度和到达目标项分别塑造效率、语义相关性、目标导向性和最终成功信号。需要注意的是，所给方法章节没有明确给出完整的策略梯度损失、折扣因子、优化器或联合训练目标，因此不能据此断言路径策略、注意力精炼器和语言模型是否以统一端到端损失共同优化。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 语义剪枝知识图谱强化学习**

对于当前节点的候选动作 $(n_{i},r_{i})$，RACER 综合关系—查询、节点—查询和节点—目标三类语义相似度计算分数，并保留 Top-$K$ 动作。状态 $s_{t}$ 融合当前节点、查询和历史路径；教师轨迹由 BFS 最短路径产生，训练策略在教师动作和强化学习策略之间按 $p_{\mathrm{teacher}}$ 混合。奖励由步长惩罚、关系相似度奖励、目标接近度奖励和到达目标奖励组成，使策略既减少无效探索，又逐步靠近目标。

> 直观理解：该模块解决的是“图太大、岔路太多”的问题。它用问题语义提前筛掉不相关动作，用示范路径帮助训练，再用奖励告诉模型短路、相关边和成功抵达目标分别有什么价值。

**2. 共享记忆图与双重注意力路径精炼**

对于边 $e$，共享记忆记录 $\mathrm{succ}(e)$、$\mathrm{fail}(e)$ 和 $\mathrm{reject}(e)$，并按历史成功率与拒绝率计算边质量分数。多路径生成采用温度采样和贪心策略的前后分段组合；路径向量由 PLM 编码后，经 $L$ 层跨路径自注意力获得表示，再分别计算查询相关性权重和可学习的重要性权重，使用 $s_{i}=\lambda\alpha_{i}+(1-\lambda)\beta_{i}$ 选择 Top-$k'$ 路径。

> 直观理解：该模块解决的是“单条路径可能走入局部最优、信息不足或重复”的问题。它一方面记住过去哪些边经常成功，另一方面让多条路线互相比较，最后只把最有用的少数证据交给语言模型。

**3. 四角色多智能体协作**

GraphAgent 负责图搜索和三元组精炼，TemplateAgent 负责将结构化路径转为逻辑路径及自然语言模板，AnswerAgent 负责依据模板生成答案，CriticAgent 负责过程与答案检查。若 CriticAgent 输出 UNSURE，则触发 GraphAgent 探索替代语义分支，并将失败轨迹写入共享记忆图，使后续搜索降低重复失败路线的优先级。

> 直观理解：该模块把复杂流程拆成职责清晰的环节，减少一个模型同时搜索、解释、作答和自我检查时的混乱。反馈回路使系统能够在证据不足时重新检索，而不是直接输出未经核验的答案。

**训练与推理**

训练阶段，系统首先使用 PLM 获得查询、关系和实体表示，并针对训练查询用 BFS 计算源节点到目标节点的教师最短路径；在语义剪枝后的动作空间中，策略按教师概率和自主策略概率混合执行，依据总奖励更新强化学习策略，同时使用 $R_{\mathrm{teacher}}=1.0$ 加速收敛。路径搜索过程中可将成功、失败和被拒绝的边统计写入共享记忆图；原文未明确报告共享记忆图的初始化、清空周期或是否在训练集之外持续累积。推理阶段，系统将问题及每个候选答案映射到图实体，分别搜索通向候选目标的路径；每条路径生成的前半阶段采用温度采样，后半阶段采用贪心策略，形成多条候选路线。随后，双重注意力精炼器通过路径间自注意力、查询—路径交叉注意力和可学习重要性评分选择 Top-$k'$ 路径；GraphAgent 将结果交给 TemplateAgent 生成自然语言知识模板，AnswerAgent 生成答案，CriticAgent 输出 $\mathrm{ACCEPT}$ 或 $\mathrm{UNSURE}$。若为 $\mathrm{UNSURE}$，系统触发 GraphAgent 探索替代分支，并将失败轨迹用于惩罚共享记忆图中的相关路线。

**复现信息**

复现或公平解读方法时，必须明确以下已报告设计：动作评分使用三项余弦相似度并满足 $\alpha+\beta+\gamma=1$；教师路径使用 BFS 最短路径；教师动作概率为 $p_{\mathrm{teacher}}$，教师监督奖励固定为 $R_{\mathrm{teacher}}=1.0$；状态为 $s_t=[\mathbf{v}_t;\mathbf{q};\mathbf{h}_t]$；共享记忆边统计包括成功、失败和拒绝次数；多路径生成前半段使用温度参数 $\tau$ 的采样、后半段使用贪心策略；路径精炼由 $L$ 层多头自注意力、查询—路径交叉注意力和可学习的混合权重 $\lambda$ 构成，并通过验证集确定 $k'$。原文未明确报告 $K$、$N$、$L$、$k'$、$\tau$、$p_{\mathrm{teacher}}$、奖励权重、PLM 的具体型号、强化学习算法名称、训练轮数、批大小、学习率、终止条件和 CriticAgent 的具体提示模板；这些因素可能影响效率、路径多样性与最终答案质量，因此不能从给定章节补充推断。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- CommonsenseQA：包含12,102道需要常识知识的多项选择题，以ConceptNet作为背景知识图谱。它主要检验系统能否从大规模常识图谱中检索并组合与问题相关的多跳知识；原文未明确报告本实验采用的数据划分。
- OpenBookQA：包含5,957道需要基础科学事实的多项选择题，同样以ConceptNet作为背景知识图谱。它用于检验方法能否把图谱知识用于科学常识推理，而非仅适配CommonsenseQA；原文未明确报告本实验采用的数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Performance（百分比；具体指标名称原文未明确报告）**

表2和表3以百分数汇报多项选择问答性能。结合任务形式，这些数值通常对应答案正确率，但所给实验章节没有显式定义指标名称、计算公式或统计方式，因此不应把它进一步解释为宏平均、微平均或其他指标。 （越高越好，因为更高的百分比表示系统在测试问题上产生正确选项的比例或总体性能更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 同一GPT-4骨干下，RACER与零样本GPT-4及现有KG提示方法比较

<div class="result-value" markdown="1">

RACER（GPT-4）在CommonsenseQA和OpenBookQA上分别达到$84.7\%$和$93.2\%$；相对零样本GPT-4的$77.2\%$和$84.6\%$，分别提高$7.5$和$8.6$个百分点。在CommonsenseQA上，它也超过该表中最强的已有KG提示基线KnowGPT（$81.8\%$）$2.9$个百分点。

</div>

同骨干比较是最有解释力的结果：在不更换GPT-4的情况下加入RACER后，两个数据集均明显改善，说明收益不只是来自更强的底座模型。作者据此主张结构化知识注入和协作推理有效；但实验未把提示长度、调用次数和计算预算控制情况完整列出，因此不能断言增益完全由某一个模块造成，也不能据此证明成本更低。

<div class="result-source" markdown="1">

来源：表2（Performance comparison on CommonsenseQA and OpenBookQA）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

RACER (GPT-4) | 84.7 | 93.2

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 以GPT-5为骨干的RACER与零样本GPT-5比较

<div class="result-value" markdown="1">

RACER（GPT-5）在CommonsenseQA和OpenBookQA上分别取得$88.2\%$和$98.0\%$，相对零样本GPT-5的$82.0\%$和$91.0\%$分别提升$6.2$和$7.0$个百分点；这也是表2中两个数据集的最高报告值。

</div>

结果表明RACER在较强骨干上仍有增益，没有因底座能力提高而失去作用；OpenBookQA的$98.0\%$尤其显示该组合在所用评测上的高正确率。作者称其接近人类专家水平，但所给章节没有提供人类专家对照行、置信区间或显著性检验，因此该说法不能由表2独立验证，也不能外推为一般科学推理能力接近人类。

<div class="result-source" markdown="1">

来源：表2（Performance comparison on CommonsenseQA and OpenBookQA）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

RACER (GPT-5) | 88.2 | 98.0

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨Qwen3、GLM4.7和Gemini 3骨干检验框架通用性

<div class="result-value" markdown="1">

RACER相对相应零样本骨干均有提升：Qwen3从$75.0\%/86.0\%$升至$85.4\%/92.6\%$，GLM4.7从$74.0\%/87.2\%$升至$86.5\%/94.5\%$，Gemini 3从$80.0\%/90.8\%$升至$87.0\%/97.5\%$；两项数字依次对应CommonsenseQA与OpenBookQA。

</div>

多个不同骨干上方向一致的提升，是RACER具有一定模型可迁移性的证据，比只在单一闭源模型上报告结果更有说服力。作者将其解释为多智能体结构化知识注入具有普遍效果；更谨慎的结论是该框架在所测三个额外骨干和两个数据集上稳定有效，尚不能推广到未测试的模型、开放式生成任务或其他知识图谱。

<div class="result-source" markdown="1">

来源：第4.2节 Observations，第(3)点；具体数值见表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The substantial gains observed across diverse models (Qwen, GLM, Gemini 3, etc.) demonstrate that our multi-agent collaboration framework provides a universally effective strategy for structured knowledge injection.

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

- LM + Fine-tuning：BERT-base、BERT-large和RoBERTa-large。该组代表仅依靠任务数据微调的预训练语言模型，用于判断显式知识图谱与智能体推理是否比常规监督微调更有效。
- KG-enhanced LM：MHGRN、QA-GNN、JointLK和GreaseLM。该组将知识图谱结构直接融入较传统的语言模型或图神经网络，是检验RACER相对于既有图谱推理架构价值的核心对照。
- LLM + Zero-shot：GPT-3.5、GPT-4、GPT-5、Qwen3、GLM4.7和Gemini 3。尤其是同一骨干的零样本结果，可用于隔离RACER框架带来的增益，避免把改进简单归因于更强的大语言模型。
- LLM + KG Prompting：KnowGPT、CoK、RoG和Mindmap。该组同样通过知识图谱辅助大语言模型，因而最直接检验强化路径搜索、共享记忆及多智能体协作是否优于已有图谱提示方法。

**实验想回答的问题**

- RQ1：与近期知识图谱增强大语言模型方法及相同骨干模型的零样本版本相比，RACER能带来多大性能提升？
- RQ2：语义剪枝、教师引导、共享记忆、注意力精炼和多智能体协作分别是否对RACER的性能有关键贡献？

**实验实现**

RACER分别采用GPT-5、Qwen、GLM和Gemini 3等骨干，以特定系统提示驱动各角色，并使用少样本上下文示例稳定输出解析。CriticAgent反馈阶段最多协作$3$轮；若仍未达成一致，AnswerAgent输出初始置信度最高的候选答案。策略网络使用Adam优化，学习率为$5\times10^{-4}$；关系相似度权重和目标相似度权重依据验证集分别设为$0.25$和$0.35$；选择前$k'=24$条路径，最大路径长度为$4$。TemplateAgent把图谱三元组改写为简短背景知识，AnswerAgent只输出选项字母，CriticAgent根据问题、三元组、文本知识和候选答案给出判断及置信度。原文未明确报告随机种子、重复运行次数、方差、显著性检验、各骨干的完整版本配置或推理成本，因此表中结果主要支持点估计层面的比较。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除语义剪枝（w/o Semantic Pruning） | 性能从完整RACER（GPT-4）的$84.7\%/93.2\%$下降到$80.1\%/89.5\%$，即CommonsenseQA和OpenBookQA分别下降$4.6$和$3.7$个百分点，是表3中最大的退化。 | 该消融主要隔离在图谱搜索时依据语义相关性缩小候选动作空间的作用。最大降幅说明，先过滤与问题或目标无关的关系和节点，对避免路径搜索被巨大图谱空间淹没十分重要。它支持语义剪枝的必要性，但由于一次仅删除完整模块，不能区分收益究竟来自更高路径质量、更短上下文还是更低搜索噪声。 | 第4.3节 Observations；对应数值见表3<br><span class="experiment-evidence">Removing semantic pruning drops performance the most (-4.6% / -3.7%), followed by teacher guidance (-3.2% / -2.4%).</span> |
| 移除教师引导（w/o Teacher Guidance） | 性能由完整模型的$84.7\%/93.2\%$下降到$81.5\%/90.8\%$，在CommonsenseQA和OpenBookQA上分别下降$3.2$和$2.4$个百分点，降幅仅次于移除语义剪枝。 | 该对照检验教师信号对强化学习路径策略的训练价值。稳定下降表明，仅靠环境探索不足以获得同等质量的推理路径，教师引导有助于策略更快地偏向有效路径。不过，原文未提供无教师版本的收敛曲线、训练方差或等训练预算比较，因此尚不能判断它主要改善样本效率、最终上限，还是两者兼有。 | 表3（Ablation study on RACER (GPT-4) components）<br><span class="experiment-evidence">w/o Teacher Guidance \| 81.5 \| 90.8</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Proposes a multi-role LLM agent collaboration framework with reinforcement-learned knowledge-graph path extraction for explainable multi-hop reasoning.; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`bf2d133651a54f78a2262a04b2d82ffd1bf888ef36173a274a4f7433823eeb7b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
