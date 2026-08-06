---
title: "[论文解读] Monte Carlo Tree Search for Table-to-Multimodal Report Generation"
description: "[arXiv 2608.04071][LLM Reasoning] 本文针对结构化表格到图文报告生成中流程僵化、子任务割裂和评测不可统一验证的问题，将报告构建重述为蒙特卡洛树搜索，并配套提出多维可验证基准 MMRBench。"
arxiv_id: "2608.04071"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T07:04:32.647900+00:00"
source_sha256: "03c585ae10cdd47ca970473b116a29058b3e5dc5bbbc1a69d63e15f8d3e3e442"
tags:
  - "LLM Reasoning"
  - "表格到多模态报告生成"
  - "蒙特卡洛树搜索"
  - "结构化表格"
  - "大语言模型"
  - "数据可视化"
  - "数值事实一致性"
  - "图文对齐"
  - "MMRBench"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.04071</p>

# Monte Carlo Tree Search for Table-to-Multimodal Report Generation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Teng Lin, Zhiyang Zhang, Yuyu Luo, Nan Tang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The Hong Kong University of Science and Technology (Guangzhou)</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04071v1) · [PDF 下载](https://arxiv.org/pdf/2608.04071v1) · **关键词** 表格到多模态报告生成, 蒙特卡洛树搜索, 结构化表格, 大语言模型, 数据可视化, 数值事实一致性, 图文对齐, MMRBench<br>


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

本文针对结构化表格到图文报告生成中流程僵化、子任务割裂和评测不可统一验证的问题，将报告构建重述为蒙特卡洛树搜索，并配套提出多维可验证基准 MMRBench。

**不用术语来说**：给定一张业务或科研表格，系统不仅要正确计算和解释其中的数据，还要选择合适的图表、组织章节，并确保文字结论与图表彼此支持。现有系统通常按预设顺序一次性完成这些步骤，早期产生的错误很难在后续纠正，最终报告可能外观完整，却存在数字错误、图文矛盾、分析浅显或结构缺失。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 MCTS-Report：把尚未完成的报告表示为搜索树中的状态，把章节规划、可视化任务识别、图表生成和叙事改写表示为逐步动作；利用蒙特卡洛树搜索比较候选构建路径，使系统能够回退并联合考虑事实准确性、视觉质量与叙事连贯性。
- 构建 MMRBench：收集六个领域的 185 张真实表格，并配套经专家修订的参考报告结构和可验证关键洞见，用于统一评估结构完整性、数值准确性、图文对齐和洞见新颖性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究“表格到多模态报告生成”：系统需要把结构化表格转化为同时包含数据分析文字与可视化图表的专业报告。该任务不同于只回答单个表格问题或生成一段摘要，因为系统不仅要理解表头、字段关系和数值，还要决定报告结构、选择值得展示的洞见、设计相应图表，并保证文字结论、图中证据与原始表格相互一致。其核心质量要求包括结构完整、数值事实准确、图文对齐和分析洞见具有信息增量；应用背景是企业与研究机构逐渐使用大语言模型智能体执行自动数据分析。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多模态报告生成**

指联合生成自然语言分析和可视化图表，并将二者组织成逻辑连贯的完整报告。这里的“多模态”主要是文本与图表两种表达形式，而不是一般意义上的任意图像生成。

</div>
<div class="concept-item" markdown="1">

**蒙特卡洛树搜索（MCTS）**

一种在巨大决策空间中逐步寻找较优行动序列的搜索方法，通常反复执行选择、扩展、模拟和回传。它通过平衡“尝试尚未充分探索的方案”和“继续改进当前高质量方案”，避免生成过程被单一路径过早锁定。

</div>
<div class="concept-item" markdown="1">

**图文对齐**

指报告文字中的结论能够由配套图表支持，同时图表的数据和视觉表达忠实于源表。若文字声称某指标增长而图表未展示该指标或呈现相反趋势，就属于图文不一致。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个真实世界的结构化表格，表格所属领域可以是金融、制造、医疗、教育、零售或 IT 运维；输出是一份由章节化文字分析和可视化图表共同构成的完整报告。系统需要从空报告框架开始，依次或交替执行章节规划、可视化任务识别、图表生成、洞见组织和叙事润色等原子行动，并允许根据中间报告状态重新选择构建路径。任务假设表格是数值事实的主要依据，因此报告中的可验证数值应能回溯到源表，图表应正确呈现相关数据，文字与图表应互相支持；最终质量需要同时考虑结构完整性、数值准确性、图文对齐和洞见新颖性，而不能只优化语言流畅度或图表美观度。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **T2R-Bench（Zhang et al., 2025）与 DDR-Bench（Liu et al., 2026a）**: 二者支持文章级表格报告生成，但原文指出其输出仍局限于文本，没有覆盖商业报告所需的可视化图表，因而不能完整评估表格到多模态报告的生成能力。
- **MMDR-Bench（Huang et al., 2026）**: 该基准面向深度研究报告，采用多阶段评估并检查视觉证据忠实性；本文据此强调仍缺少一个同时整合结构化表格输入、多模态报告输出和可验证多维评价的统一基准。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

企业和研究机构希望让 AI 代理直接从结构化表格生成专业图文报告。这一任务比表格问答或纯文本摘要更复杂：系统必须同时理解数据、形成分析主线、选择并绘制图表、撰写文字，还要保证数值可追溯、图表与论述一致、整篇报告结构完整。因此，需求并非单独生成一段文字或一张图，而是可靠地完成多个相互依赖的决策。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **固定线性生成流水线**：按照预先规定的顺序依次执行表格解析、图表生成、文本写作和润色；每一步主要消费前一步的输出，通常不会重新比较早期决策或探索另一种报告结构。
- **分离式子任务方法与现有专项基准**：生成系统分别处理表格理解、图表制作、文本撰写和质量评估；相应基准也多只考查表格问答、句子级生成、纯文本长报告或孤立的可视化质量，较少把源表、图表和配套论述放在同一可验证框架中。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 线性流水线缺少回溯和全局优化能力：若系统在数据理解尚不充分时先生成了图表，后续文字往往只能迁就该图表，难以撤销早期选择，容易造成作者所称的“insight freezing”，即分析方向过早固化并停留在浅层洞见。
- 子任务独立优化会割裂事实、视觉与叙事目标：图表可能追求美观却不忠实于源表，文字也可能提出无法由图表支持的数值结论；与此同时，依赖大语言模型裁判的评估可能受到奖励投机影响，而孤立的可视化评测又无法检查图表与源表、正文之间的一致性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未提供一种统一方案，既能在生成阶段对部分报告进行可回退的结构化搜索，联合调整章节、洞见、图表和文字，又能在评测阶段把结构化源表、完整图文输出以及可验证的多维指标连接起来。换言之，缺少的是“全局生成决策”与“跨模态可核验评价”相互配套的框架，而不只是更强的单个写作或绘图模块。

</div>
<div markdown="1"><span>核心问题</span>

能否把表格到图文报告的生成建模为对部分报告状态的逐步搜索，让单一大语言模型提出构建动作，并用同时关注数值事实、图表质量、图文一致性、结构完整性和内容多样性的反馈选择路径，从而比固定流水线生成更可靠、更连贯的完整报告？

</div>
<div markdown="1"><span>作者直觉</span>

一份报告可以看成逐步搭建的对象：当前已写内容决定下一步适合补充哪个章节、洞见或图表。把不同的下一步选择展开为搜索树后，蒙特卡洛树搜索可以在“尝试新结构”和“继续完善高质量结构”之间取舍，并在发现某条路径导致重复图表、事实冲突或结构死角时转向其他分支。这样，图表不再是必须被后文迁就的固定中间产物，而能与文字和整体结构一起接受反馈并被重新选择。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MCTS-Report将多模态表格报告生成建模为结构化树搜索。输入是一个或多个结构化表格$T=\{T_1,T_2,\ldots,T_n\}$及分析查询$q$，输出是由文本报告$R_{\mathrm{text}}$和图表集合$R_{\mathrm{vis}}$组成的多模态报告$\mathcal{R}=(R_{\mathrm{text}},R_{\mathrm{vis}})$。算法把章节规划、可视化任务识别、图表生成、洞察组织和叙事润色拆成原子动作，并通过蒙特卡洛树搜索反复探索不同动作序列；每条候选路径都由自动化事实、结构、视觉和洞察新颖性评价得到奖励，再将奖励回传以影响后续搜索。直观地说，系统不是一次性按固定流水线写完报告，而是像在多个可能的写作方案中逐步试写、评分并保留更有潜力的方案。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务建模与初始状态构造

系统将根节点$v_0$初始化为包含输入表格、查询和空报告骨架的状态，并把完整报告表示为从$v_0$到终止节点$v_t$的一条动作路径。每个中间节点保存已完成章节、图表、洞察、当前章节索引和历史动作及其输出。

<div class="method-step__io" markdown="1">

**输入**：一个或多个结构化表格$T$、自然语言查询$q$以及表结构摘要。<br>
**输出**：搜索树$\Psi=(V,E)$中的根节点和部分报告状态。

</div>

**直观理解**：先把“要分析什么”和“手头有哪些数据”放进一个空报告框架中。之后每个节点都代表报告写到某一步时的完整草稿状态，因此系统能够根据已有内容决定下一步。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 合法动作搜索与扩展

选择阶段优先访问未访问动作；当所有动作均被访问后，依据UCT分数选择子节点。扩展阶段使用动作专属提示模板，将查询、表结构、历史动作、图表元数据和洞察元数据交给同一LLM，生成候选动作输出并创建新的部分报告节点；动作转移矩阵用于禁止不符合报告逻辑的动作序列。

<div class="method-step__io" markdown="1">

**输入**：当前节点$v$、其尚未探索的合法动作集合$\mathcal{A}_{\mathrm{valid}}(v)$、查询$q$、表结构和当前路径上的推理轨迹。<br>
**输出**：若干新的子节点，每个子节点对应一个更新后的部分报告状态。

</div>

**直观理解**：搜索会优先尝试还没有试过的写作动作，之后在“目前看起来好”和“还值得探索”之间权衡。转移约束类似写作规则，例如先识别图表任务再生成图表，以免系统产生无法执行的步骤。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 模拟补全候选报告

模拟阶段从当前状态出发，依据动作转移规则和轻量随机策略继续选择动作，调用LLM补全章节、图表、洞察和叙事内容，直到执行终止动作$a_{10}$。模拟使用较低采样温度$T_{\mathrm{sim}}=0.3$和较短提示，所得路径只用于评估，不永久加入搜索树。

<div class="method-step__io" markdown="1">

**输入**：扩展得到的部分报告节点及其当前动作历史。<br>
**输出**：完整候选报告$\mathcal{R}_{\mathrm{draft}}$。

</div>

**直观理解**：系统从一个尚未写完的方案快速“草拟到结尾”，用来估计这条路径最终可能得到的报告质量。快速草拟结果不必全部保存，因为它的作用主要是帮助判断当前方案是否值得继续探索。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自监督评价与树统计回传

评价器计算事实准确性、结构完整性、视觉质量和洞察新颖性四项得分，并合成为奖励$r$。随后沿模拟路径从终止节点回溯到根节点，更新每个动作的访问次数$N(u,a_u)$、累计奖励$Q(u,a_u)$和节点访问次数$N(u)$，供下一轮UCT选择使用。

<div class="method-step__io" markdown="1">

**输入**：候选报告$\mathcal{R}_{\mathrm{draft}}$、源表格$T$、报告中的图表和数值洞察。<br>
**输出**：候选报告的奖励$r$以及更新后的搜索树统计量；搜索结束后选出高奖励报告作为最终输出。

</div>

**直观理解**：报告会被自动检查：数字能否由表格验证、必需章节是否齐全、图表是否正确、洞察是否只是常识性改写。评分会传回之前做过的决定，使后续搜索更倾向于产生事实可靠、结构完整且图文相互支持的报告。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### UCT选择函数

$$
\mathrm{UCT}(v,a)=\frac{Q(v,a)}{N(v,a)}+c\cdot\sqrt{\frac{\ln N(v)}{N(v,a)}}
$$

**符号说明**

- $v$：当前搜索树节点，表示一个部分报告状态。
- $a$：从节点$v$执行的报告构造动作。
- $Q(v,a)$：从节点$v$执行动作$a$的所有搜索路径获得的累计奖励。
- $N(v,a)$：从节点$v$选择动作$a$的访问次数。
- $N(v)$：节点$v$被访问的总次数。
- $c$：探索系数，原文设为$1.414$。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项表示动作过去平均表现，第二项鼓励尝试访问次数较少的动作。这样搜索不会只重复当前最优方案，也会保留发现更好报告结构的机会。<br>
**原文位置**：MCTS-Driven Report Generation；Phase 1: Selection (UCT-Based)，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 多维自监督奖励

$$
r=r_{\mathrm{fact}}+r_{\mathrm{struct}}+r_{\mathrm{vis}}+r_{\mathrm{novel}}
$$

**符号说明**

- $r$：候选完整报告的总奖励。
- $r_{\mathrm{fact}}$：数值事实准确性得分，即经SQL验证正确的数值陈述占全部数值陈述的比例。
- $r_{\mathrm{struct}}$：结构完整性得分；必需章节均存在且每章至少有一段时为$1$，否则为$0$。
- $r_{\mathrm{vis}}$：视觉质量得分，即通过技术正确性和数据保真检查的图表比例。
- $r_{\mathrm{novel}}$：洞察新颖性得分，即与常见或平凡洞察模板相似度低于阈值的洞察比例。

<div class="equation-explanation" markdown="1">

**直观理解**：总奖励把报告质量拆成四个可自动检查的方面，并将它们相加作为搜索反馈。其核心思想是避免只优化文字流畅度，而同时要求数字可信、结构完整、图表可用且洞察不重复。<br>
**原文位置**：MCTS-Driven Report Generation；Phase 4: Backpropagation，Reward Function，公式(2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未描述独立的模型参数训练目标，也未报告通过梯度下降更新LLM参数。该方法的优化对象是搜索树中的动作路径：每次模拟得到候选报告奖励$r$后，将其累积到路径上的$Q(u,a_u)$并增加访问次数$N(u,a_u)$，再通过UCT改变后续动作选择；因此更准确地说，这是推理阶段的搜索优化，而不是LLM的参数训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 搜索树与动作空间**

搜索树$\Psi=(V,E)$的节点表示部分报告，边表示报告构造动作。动作空间覆盖章节规划$a_1$、可视化任务识别$a_2$、图表生成$a_3$、图表修改$a_4$、洞察组织$a_5$、章节总结$a_6$、标题优化$a_7$、叙事流优化$a_8$、过渡设计$a_9$和终止$a_{10}$；合法后继由转移约束矩阵决定。

> 直观理解：报告被拆成许多可单独执行的小步骤，而不是让模型一次生成全部内容。约束矩阵规定这些步骤何时可以出现，从源头上减少逻辑不通或前置条件未满足的方案。

**2. MCTS搜索引擎与LLM执行引擎**

MCTS包含Selection、Expansion、Simulation和Backpropagation四个阶段；Selection使用UCT，Expansion为每个尚未扩展的合法动作调用LLM生成候选状态，Simulation使用轻量策略快速补全，Backpropagation更新搜索统计。系统使用同一个LLM，通过不同的动作提示模板完成数据解析、图表代码生成、洞察写作和报告润色，而非部署多个具有独立身份的智能体。

> 直观理解：LLM负责具体写作和推理，MCTS负责决定先做什么、保留哪条路线。单一模型通过不同提示承担不同工作，因此报告中的数据分析、图表和文字能够共享当前状态与历史轨迹。

**3. 自监督多维奖励与有效性检查**

事实准确性通过从数值陈述生成SQL查询并对照源表执行结果计算；视觉质量检查图表代码、坐标轴、图例、标题及渲染数据点；结构完整性检查必需章节和段落；洞察新颖性通过与常见模式模板的余弦相似度判断。系统还利用动作前置条件、重复分支去重和可选的低奖励提前终止来压缩无效搜索。

> 直观理解：评价主要依靠表格和规则本身，而不是额外人工逐篇打分。这样搜索可以获得明确反馈：错误数字、缺章节、坏图表和重复洞察都会降低候选方案的吸引力。

**训练与推理**

方法在推理阶段接收表格集合$T$和查询$q$，建立空报告根节点，并重复执行MCTS的Selection、Expansion、Simulation和Backpropagation。扩展阶段对尚未探索的合法动作调用LLM，原文报告每个动作采样$k=3$次、扩展温度为$T_{\mathrm{expansion}}=0.8$；模拟阶段使用$T_{\mathrm{sim}}=0.3$，随机选择合法后继并朝终止动作推进，直至得到$\mathcal{R}_{\mathrm{draft}}$。候选报告由内部自监督奖励评价，统计量回传后继续搜索，最终从搜索结果中选择高奖励的完整报告；原文未明确报告完整报告的最终选取规则、$N_{\mathrm{rollout}}$具体数值以及四项奖励是否使用额外权重。

**复现信息**

可复现所需的关键设置包括：LLM通过动作专属提示模板接收查询、表结构摘要、累计推理轨迹及已生成图表和洞察的元数据；图表代码使用Vega-Lite或Matplotlib生成。事实陈述通过SQL对照源表验证，正确性容差为$1\%$；图表数据保真检查也使用不超过$1\%$的容差；洞察新颖性使用模板库余弦相似度，低于$0.7$视为新颖。原文还提到扩展去重、非法动作剪枝和基于动态阈值的可选提前终止，但未明确去重标准、动态阈值公式、各奖励项权重、LLM具体型号及最终候选排序细节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MMRBench：论文构建的多模态表格到报告基准，包含来自六个领域的真实表格，并配有专家修订的报告结构和可验证的关键洞察。它用于统一评测报告结构、数值事实、图表文本关系和洞察新颖性。数据集的具体样本总量、训练集与测试集划分，原文未明确报告。
- 分层抽样的50个任务：由六名专业商业分析师独立生成参考报告，用于建立人工基线。该样本承担人类专家对照的作用，而不是另一个模型训练或测试集；其余任务规模和划分原文未明确报告。
- 200份随机抽样的MCTS-Report生成报告：用于人工错误分析，统计数值幻觉、陈述平凡或改写、多表混淆等主要错误类型。该样本用于诊断系统弱点，不是用于主结果打分的数据集；抽样来源和具体划分原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Overall**

总体分数，是结构完整性、数值准确性、图表与文本对齐以及洞察新颖性四个维度的平均值，用于概括报告的综合质量。 （越高越好，因为它表示四个评价维度的平均表现更强。）

</div>
<div class="metric-item" markdown="1">

**Numerical**

数值准确性，衡量报告中的数字是否与表格事实一致。论文说明其评价通过SQL进行验证或由评价协议进行判断，重点是减少数值幻觉。 （越高越好，因为更高分表示报告中的数值事实更可靠。）

</div>
<div class="metric-item" markdown="1">

**Chart-Text**

图表与文本对齐，衡量叙述是否正确解释和支持所生成的图表，以及图表是否与文本表达的分析结论相匹配。 （越高越好，因为更高分表示视觉证据与文字叙述之间的跨模态协调更充分。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### MMRBench上的总体比较：MCTS-Report使用DeepSeek-R1作为底层模型，与直接使用DeepSeek-R1及其他模型比较。

<div class="result-value" markdown="1">

MCTS-Report（DeepSeek-R1）取得77.9的Overall、88.6的Structural、73.1的Numerical、88.7的Chart-Text和61.3的Novelty；直接DeepSeek-R1的Overall为62.7，因此总体提高15.2分，并且超过表中其他自动化基线。

</div>

该结果表明，在底层模型相同的情况下，搜索式规划和逐步构建能够显著改善综合报告质量，尤其改善数值可靠性和图文协调。它只能证明在本文给定的MMRBench、提示模板和评审设置下具有优势，不能单独证明该方法在其他数据集、其他评审模型或不同计算预算下同样优越。

<div class="result-source" markdown="1">

来源：Main Results，Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Overall score is 77.9, far exceeding the best baseline of DeepSeek-R1 (62.7, +15.2).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 不同底层大语言模型上的迁移比较：分别以DeepSeek-R1、GPT-4o和Gemini-3.5-Flash驱动MCTS-Report。

<div class="result-value" markdown="1">

三种底层模型下的Overall分别为77.9、74.1和71.8；对应的Chart-Text分数分别为88.7、85.5和82.1。三种配置均高于其可直接比较的底层模型分数，说明搜索框架并非只对单一底层模型有效。

</div>

这说明MCTS-Report更像是作用于报告构建过程的通用控制框架，而不是只依赖某个特定模型的偶然能力。不同底层模型之间仍有明显差距，因此框架不能完全消除底层模型在推理、代码执行或表达方面的差异；原文没有提供每个配置的统计显著性或多次运行方差。

<div class="result-source" markdown="1">

来源：Main Results，Finding 1；Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MCTS-Report consistently improves every base model it is applied to.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 与人工专家的质量差距及错误诊断：比较MCTS-Report（DeepSeek-R1）和Human Expert，并检查200份生成报告。

<div class="result-value" markdown="1">

MCTS-Report（DeepSeek-R1）的Chart-Text为88.7，人工专家为89.5；但MCTS-Report的Novelty为61.3、Numerical为73.1，人工专家分别为88.5和91.2。错误分析中，数值幻觉占24.6%，平凡或改写式洞察占31.0%，多表混淆占9.8%。

</div>

系统已接近人工报告的图文对齐水平，但在洞察新颖性和数值准确性上仍有较大差距。错误分布提示，进一步增加搜索并不必然解决深层分析不足：模型可能探索了不同报告结构，却仍生成普通洞察；多表混淆则显示复杂模式和连接关系仍是薄弱环节。错误比例来自可包含多个错误的报告，因此不能直接相加为100%。

<div class="result-source" markdown="1">

来源：Main Results，Finding 3；Error Analysis，Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Although all models’ novelty scores are far below the human baseline (MCTS-Report’s 61.3 vs. human 88.5), MCTS-Report achieves relative superiority through the exploration mechanism inherent in MCTS, which encourages the search to try less obvious analytical angles.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评估主要依赖温度为0.2的单一GPT-4o评审模型，且原文未报告人工复核、评审一致性、置信区间或多次运行方差；因此分数可能受到自动评审偏差和随机性的影响。
- MMRBench的总体规模、训练测试划分、任务分布和各领域样本量原文未明确报告；同时实验没有量化MCTS相较于直接生成的推理时间、token消耗或模型调用成本，因而难以判断77.9的质量收益是否适合资源受限场景。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原生图表生成的视觉语言模型，包括GPT-4o、GPT-4.1、Gemini-2.5-Pro、Gemini-3.5-Flash、Claude-4.5-Sonnet和Qwen3-VL-235B。它们代表能够直接生成文本及图表的通用多模态模型，可检验MCTS是否超越单次直接生成。
- 代码增强的多模态系统，包括带代码解释器的DeepSeek-R1、Qwen3-Coder-32B和TableGPT2-7B。它们能够借助代码处理表格或生成图表，是数值计算能力较强的比较对象。
- 深度研究代理，包括Gemini Deep Research、ChatGPT Deep Research和Perplexity Sonar Deep Research。它们代表具有多步检索或分析流程的代理系统，用于比较MCTS式报告构建与现有研究型代理的差异。
- 人工专家基线：六名专业商业分析师在50个分层抽样任务上按照相同协议独立生成参考报告。它用于衡量模型与专业人工报告之间的差距，但不是自动化模型基线。

**实验想回答的问题**

- 在相同输入、提示模板和输出限制下，$MCTS$引导的渐进式报告构建是否能相较于直接生成、代码增强系统和深度研究代理，提高报告的结构完整性、数值准确性、图表与文本对齐以及整体质量？
- MCTS-Report中的搜索规划、自监督奖励和更多rollout分别是否对报告质量有实质贡献，且当前系统的主要失败模式是什么？

**实验实现**

每个模型接收一个任务实例，任务包含一个或多个表格以及分析指令$q$，并生成同时含有文本和嵌入式可视化的多模态报告。所有模型使用相同提示模板，文本报告最多4096个token，最多生成8个可视化结果。评价使用GPT-4o作为单一评审模型，温度设为0.2；Overall为四个评价维度的平均值。实验比较三类外部模型、三种MCTS-Report底层模型以及人工专家。消融实验统一使用DeepSeek-R1。错误分析人工检查200份随机报告；由于一份报告可能包含多个错误，错误比例不应被解释为互斥类别概率。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Variant A（w/o MCTS）：保留相同动作空间，但去除MCTS搜索，直接让底层LLM进行单次rollout；与完整MCTS-Report比较。 | 该变体的Overall比完整MCTS-Report低13.4分，Numerical低13.7分，Novelty低23.8分。 | 该消融隔离的是树搜索、反复评估和回传机制的整体作用。大幅下降说明单次线性生成难以同时规划报告结构、验证数字并寻找非平凡洞察；但由于一次去除了多个相互关联的搜索操作，结果不能把下降精确归因于某一个MCTS子步骤。 | Ablation Studies，Figure 2<br><span class="experiment-evidence">Variant A underperforms full MCTS-Report by 13.4 points overall, with the largest drops in numerical accuracy (-13.7) and novelty (-23.8).</span> |
| Variant B（w/o Self-Supervised Reward）与Variant C（Reduced Rollouts）：Variant B在搜索中随机选择且不回传奖励；Variant C将rollout数量从10减为5，均与完整方法比较。 | Variant B的Overall比完整方法低10.6分；Variant C在5次rollout下取得70.4，而完整MCTS-Report取得77.9。 | Variant B检验奖励信号能否帮助搜索区分有希望和较差的路径，结果支持奖励引导的重要性。Variant C检验搜索预算，5次rollout明显低于10次，说明更充分的探索通常有益；不过原文只报告这两个预算点，无法据此确定最优rollout数量或证明收益曲线已经出现边际递减。 | Ablation Studies，Figure 2<br><span class="experiment-evidence">Variant C (5 rollouts) achieves 70.4 overall, while full MCTS-Report reaches 77.9.</span> |

**定性案例**

- 错误分析提供了一个定性诊断：多表混淆在金融和医疗报告中尤其常见，因为这些任务的模式复杂且表连接并不简单。该现象说明当前搜索虽然能优化候选报告路径，却仍可能在跨表模式对应和连接关系理解上出错；原文未提供具体报告样例或逐步搜索轨迹，因此不能进一步判断错误发生在表选择、连接、图表生成还是叙述阶段。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The core method uses LLM-driven stepwise planning and reasoning within Monte Carlo Tree Search to construct coherent multimodal reports.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`03c585ae10cdd47ca970473b116a29058b3e5dc5bbbc1a69d63e15f8d3e3e442`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
