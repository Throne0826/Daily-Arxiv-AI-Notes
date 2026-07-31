---
title: "[论文解读] SciDataSailor: Deep Scientific Data Exploring"
description: "[arXiv 2607.28098][LLM Agent] 本文关注如何让大语言模型智能体直接进入真实科学数据仓库，通过可执行工具发现、计算、核验并整合跨文件证据，并进一步解决这类长程交互轨迹难以低成本、可靠构造的问题。"
arxiv_id: "2607.28098"
announcement_date: "2026-07-31"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.434042+00:00"
source_sha256: "f9f2c6e896d37b3ff67397406ff0078d79b0d49cf1ed80c397e79989dd856a83"
tags:
  - "LLM Agent"
  - "LLM 其他"
  - "深度科学数据探索"
  - "科学数据智能体"
  - "异构层级数据仓库"
  - "长时程工具交互"
  - "可执行证据"
  - "蒙特卡洛树搜索"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2607.28098</p>

# SciDataSailor: Deep Scientific Data Exploring

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Rao, Jiyong, Qiu, Yicheng, Zhang, Chi, Song, Chunfeng, Zhao, Runkai</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Shanghai Artificial Intelligence Laboratory；Tongji University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.28098) · [PDF 下载](https://arxiv.org/pdf/2607.28098) · **关键词** 深度科学数据探索, 科学数据智能体, 异构层级数据仓库, 长时程工具交互, 可执行证据, 蒙特卡洛树搜索<br>


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

本文关注如何让大语言模型智能体直接进入真实科学数据仓库，通过可执行工具发现、计算、核验并整合跨文件证据，并进一步解决这类长程交互轨迹难以低成本、可靠构造的问题。

**不用术语来说**：科学数据通常不是一篇篇可直接阅读的文字，而是分散在多层目录中的测量值、元数据、注释、实验记录和派生文件；不同文件还可能采用不同格式、单位、坐标系与标识符。研究者要回答一个问题，往往必须先摸清目录和文件结构，再判断哪些文件彼此相关，运行程序计算统计量，并检查结论是否真正得到数据支持。这个过程耗时、易错，而且当数据规模增大或文档不完整时很难扩展。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“深度科学数据探索”任务范式，将科学数据分析表述为智能体与真实数据仓库之间的长程工具调用过程，要求智能体导航目录、理解异构文件及隐式模式、执行分析、连接跨文件证据，并使结论可追溯到实际工具输出。
- 作者提出 SciDataSailor，用面向证据搜寻的蒙特卡洛树搜索合成工具交互轨迹，并配合执行有效性与幻觉检查筛除错误或缺乏证据的轨迹；由此构建用于监督微调的 SciDataSailor-SFT-2K 和用于评测的 SciDataSailor-Bench。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

科学数据通常以层级目录保存，内部同时包含原始测量、元数据、标注、实验记录和派生结果；不同文件还可能采用不同格式、单位、坐标系与标识符约定，并通过隐含关系相互依赖。因此，科学数据探索不能等同于从文本中检索答案：智能体需要进入可执行环境，逐步查看目录和文件、推断数据模式、对齐跨文件实体、运行统计或验证代码，并确保结论可追溯到真实工具输出。本文将这一场景称为“深度科学数据探索”，关注大语言模型智能体如何在陌生科学数据库上完成长时程、工具调用式的证据发现与整合。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**长时程探索轨迹**

智能体不是通过一次模型调用直接回答问题，而是在多个时间步中反复选择操作、接收执行结果并更新已有信息。完整轨迹保留状态、动作、观察和最终回答，可用于检查结论依据，也可作为监督微调数据。

</div>
<div class="concept-item" markdown="1">

**探索与利用**

“探索”是广泛检查目录、格式、变量和文件关系，以发现有哪些证据；“利用”是围绕已有线索执行精确统计、交叉验证和结论整理。科学数据仓库结构未知且操作预算有限，因此智能体必须在二者之间取舍。

</div>
<div class="concept-item" markdown="1">

**蒙特卡洛树搜索**

蒙特卡洛树搜索（MCTS）把每段部分执行轨迹视为树节点，把可选的下一步工具操作视为分支，并通过选择、扩展、模拟和反向传播逐步寻找高价值路径。其典型选择准则同时偏好估计价值较高的节点和访问较少的节点，以平衡利用与探索。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文把未知科学数据库记为 $D$，把探索种子记为 $\sigma$，一次请求为 $x=(D,\sigma)$；智能体可在代码沙箱 $\mathcal{E}$ 中执行文件系统访问、格式检查和数据分析等操作。在第 $t$ 步，智能体依据上一状态 $s_{t-1}$ 从可行动作集合 $\mathcal{A}(s_{t-1})$ 中选择 $a_t$，环境返回观察 $o_t=\mathcal{E}(s_{t-1},a_t)$，状态转移函数再生成 $s_t=F(s_{t-1},a_t,o_t)$。最终输出是一条可执行轨迹 $\tau$ 及回答 $y$；回答必须以执行观察为依据，而高质量轨迹还应揭示可复用的数据模式、变量分布、文件关系、数值摘要和支持结论的证据。该问题假设数据库起初陌生、证据可能跨文件分散，并允许同一证据状态对应多个合理的后续探查动作，因此可将轨迹空间组织成搜索树。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x=(D,\sigma)$**

探索请求，其中 $D$ 是未知科学数据库，$\sigma$ 是规定初始目标或探索方向的种子。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{E}$**

可执行代码沙箱；它接收当前状态和动作，并返回实际运行产生的观察结果。

</div>
<div class="notation-item" markdown="1">

**$s_t, a_t, o_t$**

第 $t$ 步交互中的状态、智能体动作和环境观察；状态用于累计此前发现的仓库结构、数据语义与执行证据。

</div>
<div class="notation-item" markdown="1">

**$\tau=(s_0,a_1,o_1,s_1,\ldots,a_T,o_T,s_T,y)$**

完成的长时程探索轨迹，其中 $T$ 是交互步数，$s_0$ 编码初始请求与数据库上下文，$y$ 是由执行观察支撑的最终回答。

</div>

</div>

**直接相关的工作**

- **基于网页与文本语料的智能体系统**: 这类系统通常通过结构化查询接口检索文档、阅读文本并综合答案，为智能体规划、推理和工具使用提供了基础；但它们没有充分覆盖直接操作异构科学文件、执行数据分析以及维护跨文件依赖和证据来源的需求。原文在所给节选中仅以参考文献编号 [9–15] 指代相关工作，未提供具体名称。
- **深度网页研究的轨迹合成方法**: 现有流程主要围绕查询改写、文档检索、段落阅读和答案综合生成交互轨迹，而科学数据探索还要求文件操作、模式推断、数值计算和执行有效性检查。本文据此把 MCTS 引入科学数据轨迹合成；同时指出普通 MCTS 偏重任务成功、可能重复探查，且只保留最佳叶节点不足以支持多样化数据生成。原文在所给节选中仅以参考文献编号 [16,17] 指代相关方法，未提供具体名称。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

真实科学仓库中的证据具有异构、分散和相互依赖的特点：一个结论可能同时依赖原始测量、元数据、注释及派生结果，而这些资产在格式、组织方式、标识符、单位和坐标系上并不统一。可靠分析因此需要连续完成目录导航、格式检查、隐式模式推断、跨文件对齐、统计计算和结论验证；依赖人工领域知识执行这些步骤成本高、容易出错，也难以处理大型或文档稀疏的数据集。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于网页文档或文本语料的 LLM 智能体**：智能体通常借助搜索、数据库或其他结构化查询接口定位相关文档，读取自然语言段落，再利用规划与推理能力综合文本信息并生成答案。
- **面向深度网页研究的轨迹合成流水线**：这类方法让智能体反复改写查询、检索文档、阅读段落并汇总答案，以生成搜索和问答过程，主要监督如何从文本资源中逐步收集信息。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 文本或网页智能体通常依赖显式查询接口和可直接阅读的段落，难以覆盖科学仓库所需的文件系统导航、异构格式解析、隐式模式推断、程序执行及跨资产对齐；其后果是答案可能来自文本检索或模型参数知识，而不是对原始科学数据的实际观察。
- 现有网页研究轨迹合成方法没有充分表达科学数据分析的可执行性和来源敏感性，也难以在长程过程中同时兼顾广泛探索与定向验证；人工构造此类多样且可靠的轨迹又代价过高，容易产生执行失败、无信息或缺乏证据支持的训练样本。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种面向真实科学数据资产的专用轨迹合成与评测框架：它既要在仓库结构和数据语义逐步显露时维持连贯的证据获取策略，又要自适应地分配探索广度与验证深度，并保证最终轨迹中的操作可执行、跨文件依赖得到保留、结论能够追溯到实际观测。作者在结论中进一步指出，核心瓶颈并非孤立地调用一次工具，而是在不确定且相互依赖的仓库状态之间持续维持一致的证据获取策略。

</div>
<div markdown="1"><span>核心问题</span>

能否把真实科学仓库探索建模为长程、工具交互式的证据搜索，并用执行反馈驱动的树搜索自动合成可靠轨迹，使模型学会发现数据组织、选择分析操作、验证候选发现和整合跨文件证据，同时提升科学问答的准确性与交互效率？

</div>
<div markdown="1"><span>作者直觉</span>

探索陌生科学仓库类似在尚未绘制的目录树中调查证据：前期需要尝试不同目录、文件和变量以建立全局认识，发现线索后则应把计算集中到最可能回答问题的路径上。蒙特卡洛树搜索适合显式表示这种多步选择，并依据执行反馈不断调整搜索重点；难度分层种子、双反馈、从高层策略到具体工具的分层动作生成以及按不确定性分支，可帮助搜索既不过早锁定错误路径，也不把资源平均浪费在低价值操作上。执行有效性与幻觉检查则充当事后证据门槛，降低不可运行或无数据支持的轨迹进入训练集的风险。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SciDataSailor不是直接训练一个代理回答预先写好的问题，而是先从科学数据集$D$和宽泛的探索种子$\sigma$出发，在可执行代码沙箱$\mathcal{E}$中合成长程探索轨迹。系统把部分轨迹作为蒙特卡洛树搜索节点：先提出具有不同科学意图的候选策略，再将策略具体化为可执行探针；随后结合执行前的预期效用与执行后的证据效用选择和剪枝分支，并根据当前不确定性动态分配分支宽度。搜索得到的轨迹经过执行有效性、逐步证据归因和歧义处理后，被整理为SciDataSailor-SFT-2K中的过程监督数据，以及SciDataSailor-Bench中的元信息总结和科学问答实例。

从直观上看，这一流程相当于让代理在陌生的科学数据仓库中做有记录的调查：探索种子只规定调查方向，代理需要自己查看目录、解析模式、计算统计量、连接跨文件信息并核验结论。树搜索保留多条可能的调查路线，执行反馈用于识别真正产出证据的路线；最终训练材料不仅给出答案，还保存“为何检查这个文件、运行了什么代码、观察到什么结果、结论如何由结果支持”的完整链条。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造分层探索请求

构造请求$x_\sigma=(D,\sigma)$，并依据回答该意图所需的证据范围和推理深度，将$\sigma$划入$\ell(\sigma)\in\{L0,L1,L2,L3\}$之一；最终回答必须保持与原始种子意图一致。

<div class="method-step__io" markdown="1">

**输入**：科学数据集$D$与宽泛探索种子$\sigma$。<br>
**输出**：带难度等级和意图约束的探索请求$x_\sigma$。

</div>

**直观理解**：种子不是一道答案固定的问题，而是一张调查任务单；难度等级说明完成调查大致需要查看多少类证据、进行多深的关联推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成分层策略与可执行探针

先从策略目录$\mathcal{A}_{\mathrm{str}}$提出仓库检查、模式解析、统计分析、跨文件整合、主张验证、可视化或调试等高层策略，再对策略评分和过滤，并将保留策略实例化为候选探针$c_i$；系统按工具身份去重并优先保留互补行动。

<div class="method-step__io" markdown="1">

**输入**：当前已执行轨迹前缀$\tau_v$、状态$s_v$和探索请求$x_\sigma$。<br>
**输出**：候选集合$C_v=\{(c_i,\rho_i)\}$，其中$\rho_i$是执行前效用评分。

</div>

**直观理解**：系统先决定“下一步需要哪一类证据”，再决定“具体运行哪段代码或调用哪个工具”。这种先策略、后工具的层次可减少只因代码写法不同而重复执行的探针。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 以DF-FPU进行树搜索和执行反馈

执行前评审器估计探针产生相关且可复用证据的概率$\rho_w$；DF-FPU利用兄弟节点的预测误差校准未访问节点，并结合访问次数、质量感知探索项和深度奖励选择分支。执行$a_w$得到$o_w=\mathcal{E}(s_v,a_w)$后，执行后评审器给出证据效用$y_w$并反向传播；若$y_w<\theta_{\mathrm{post}}$，节点保留作来源记录但不再扩展。

<div class="method-step__io" markdown="1">

**输入**：候选探针、节点访问统计、已访问兄弟节点的执行结果，以及可执行环境$\mathcal{E}$。<br>
**输出**：含执行观察、经验价值和可扩展标记的更新后轨迹树。

</div>

**直观理解**：执行前评分像检查计划的预审，执行后评分则检验这次操作是否真的拿到了可核查证据。系统还会用同一位置上已经执行过的操作校正评审器的局部乐观或悲观偏差。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 熵引导的动态扩展

系统将候选评分经温度$T_p$归一化并计算先验熵$H_{\mathrm{prior}}(v)$，再与词元熵$H_{\mathrm{tok}}(v)$加权得到步骤熵$H_{\mathrm{step}}(v)$；分支数$k_{\mathrm{dyn}}(v)$在$k_{\min}$与$k_{\max}$之间随不确定性增加，并由多样性过滤器物化对应数量的子节点。

<div class="method-step__io" markdown="1">

**输入**：节点$v$的候选先验评分分布，以及可用时的模型词元预测不确定性。<br>
**输出**：与当前决策不确定性匹配的新增子分支。

</div>

**直观理解**：若多个候选看起来同样合理，系统多试几条路线；若下一步几乎显然，则少开分支，把有限工具预算留给真正难以判断的位置。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### DF-FPU校准价值与分支选择

$$
\Delta_v=\begin{cases}\frac{1}{|S_v|}\sum_{u\in S_v}\left(Q(u)-\rho_u\right),&|S_v|>0\\0,&|S_v|=0\end{cases},\quad \widehat{Q}(w)=\begin{cases}Q(w),&N(w)>0\\\operatorname{clip}_{[0,1]}\left(\rho_w+\Delta_v-\delta_{\mathrm{fpu}}\right),&N(w)=0\end{cases},\quad \operatorname{UCT}_{\mathrm{DF\text{-}FPU}}(v,w)=\widehat{Q}(w)+\lambda\rho_w\sqrt{\frac{\log(1+N(v))}{1+N(w)}}+\beta d_w
$$

**符号说明**

- $v$：当前轨迹树节点。
- $w$：节点$v$的候选子节点。
- $S_v$：节点$v$下访问次数大于零的子节点集合，包括后来被标记为不可扩展的节点。
- $Q(u)$：已访问节点$u$根据执行后回报形成的经验平均价值。
- $\rho_u$：执行前评审器对候选节点$u$的预期证据效用评分。
- $\Delta_v$：当前父节点下，已访问子节点实际价值相对执行前预测的平均残差。
- $\widehat{Q}(w)$：选择阶段使用的价值；已访问节点采用经验值，未访问节点采用经局部残差校准的先验值。
- $N(w)$：子节点$w$的访问次数。
- $\delta_{\mathrm{fpu}}$：非负的首次访问保守折减量，用于反映未测试行动的不确定性。
- $\lambda$：控制质量感知探索强度的系数。
- $\beta$：深度奖励的权重。
- $d_w$：子节点$w$在$[0,1]$范围内的归一化深度。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先比较兄弟节点“执行前预期”与“执行后实际价值”的平均差，并据此修正尚未执行的候选；若评审器在当前位置普遍过于乐观，$\Delta_v$为负，未访问节点的初始价值随之降低。选择分数随后兼顾当前价值、较少访问分支的探索机会和长程证据链的深度，使工具预算优先投入潜在有用但尚未充分验证的路线。<br>
**原文位置**：第4.1节，公式(8)至(11)

</div>

</div>

<div class="equation-block" markdown="1">

#### 熵引导的动态分支宽度

$$
\pi_i=\frac{\exp(\rho_i/T_p)}{\sum_{j=1}^{\bar{M}_v}\exp(\rho_j/T_p)},\quad H_{\mathrm{prior}}(v)=-\frac{1}{\log \bar{M}_v}\sum_{i=1}^{\bar{M}_v}\pi_i\log\pi_i,\quad H_{\mathrm{step}}(v)=\frac{w_pH_{\mathrm{prior}}(v)+w_tH_{\mathrm{tok}}(v)}{w_p+w_t},\quad k_{\mathrm{dyn}}(v)=\min\left\{\bar{M}_v,\operatorname{round}\left(k_{\min}+(k_{\max}-k_{\min})H_{\mathrm{step}}(v)\right)\right\}
$$

**符号说明**

- $\rho_i$：第$i$个候选探针的执行前效用分数。
- $T_p$：将候选分数转换为概率分布时使用的正温度参数。
- $\bar{M}_v$：节点$v$处候选探针的总数。
- $\pi_i$：候选$i$经温度缩放和Softmax归一化后的概率。
- $H_{\mathrm{prior}}(v)$：由候选先验分布计算的归一化熵；候选数不超过一时定义为零。
- $H_{\mathrm{tok}}(v)$：可获得词元对数概率时计算的归一化预测词元熵。
- $w_p,w_t$：先验熵和词元熵的非负组合权重，且二者之和大于零。
- $H_{\mathrm{step}}(v)$：节点$v$处综合后的步骤不确定性。
- $k_{\min},k_{\max}$：允许的最小和最大分支宽度。
- $k_{\mathrm{dyn}}(v)$：节点$v$实际物化的动态分支数。

<div class="equation-explanation" markdown="1">

**直观理解**：若候选分数接近，概率分布较均匀、熵较高，意味着系统无法确信哪条路线最好，于是分支数接近$k_{\max}$；若某个候选明显占优，熵较低，分支数接近$k_{\min}$。当模型词元概率不可获得时，论文规定直接令$H_{\mathrm{step}}(v)=H_{\mathrm{prior}}(v)$，因此机制仍可用于不暴露词元概率的模型。<br>
**原文位置**：第4.1节，公式(12)至(13)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文节选没有给出用于更新基础语言模型参数的独立损失函数，也没有说明在标准词元级交叉熵之外增加专门的树搜索目标。因此不能把DF-FPU的节点价值或执行后评分误解为模型训练损失：它们直接优化的是轨迹合成阶段的搜索决策，即在固定交互预算下优先生成相关、可复用且可执行验证的证据链。搜索和质控得到的`<think>`、`<python>`、`<result>`、`<answer>`序列随后构成SciDataSailor-SFT-2K的过程监督样本，论文所称“token-level supervision”表示模型能够学习完整交互序列，而不仅是最终答案；具体微调损失及其权重在所给章节中原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双反馈首次访问紧迫度（DF-FPU）**

每个候选子节点$w$在首次执行前获得先验分数$\rho_w=r_{\mathrm{pre}}(a_w\mid\tau_v,x_\sigma)$，首次执行后获得证据分数$y_w=r_{\mathrm{post}}(o_w,a_w\mid\tau_v,x_\sigma)$。系统用已访问兄弟节点集合$S_v$上的平均残差$\Delta_v$校准未访问节点的初始价值，再通过带质量感知探索项和深度奖励的$\mathrm{UCT}_{\mathrm{DF-FPU}}$选择边；低于阈值$\theta_{\mathrm{post}}$的分支停止扩展。

> 直观理解：普通MCTS在未尝试动作之间缺少区分，可能把昂贵的工具调用浪费在明显无关的探针上。DF-FPU既参考行动执行前是否值得尝试，也根据执行后是否获得可验证证据修正判断，因此更适合预算有限、单次操作成本较高的科学数据探索。

**2. 分层策略到工具行动生成**

系统不直接从语言模型采样一组代码，而是先在$\mathcal{A}_{\mathrm{str}}$中生成和筛选科学探索策略，再将策略落实为工具探针$c_i$，并按工具身份去重、按意图多样性排序。策略层覆盖仓库与模式检查、统计分析、跨文件整合、主张验证、可视化和调试，也可作为监督微调或强化学习中的中间行动类型信号。

> 直观理解：直接生成代码容易得到多段目的相同的操作，也难以判断遗漏了哪一类证据。显式策略层让不同分支优先回答不同的调查子问题，再为每个子问题生成实际操作。

**3. 熵引导分支与后向质量剪枝**

系统以候选效用分布的归一化熵表示策略间的不确定性，并在可获得词元对数概率时加入归一化词元熵；两者决定动态分支宽度$k_{\mathrm{dyn}}(v)$。该前向扩展机制与执行后基于$y_w$的不可扩展标记共同形成“高不确定处拓宽、低质量处停止”的预算控制器。

> 直观理解：固定分支数会在简单节点浪费调用，又可能在困难节点遗漏关键路线。动态分支负责决定值得同时尝试多少种方案，执行后剪枝负责及时停止没有证据收益的方案。

**训练与推理**

数据合成阶段首先对每个$x_\sigma=(D,\sigma)$建立以初始状态$s_0$为根的轨迹树。每轮搜索在当前前沿节点上生成策略和工具探针，以DF-FPU选择候选，在沙箱$\mathcal{E}$中执行并记录观察，再由执行后评审器评价证据效用、反向传播经验价值并阻止低证据节点继续扩展；熵引导模块同时决定本节点实际创建多少个候选子节点。搜索结束后，系统不只保留单个最高分叶节点，而是选择能够暴露模式、变量分布、文件关系、数值统计或数据质量问题等可复用事实的轨迹，并通过执行有效性和逐步幻觉检查生成监督数据。

监督微调时，模型接收探索请求以及随交互逐步累积的状态，学习预测包含推理、Python工具调用、执行结果承接和最终回答的标记化轨迹。实际推理或基准评测时，代理面对未熟悉的原始数据仓库和任务，在规定的ReAct步骤预算内迭代产生代码、读取真实执行结果并继续推理，最终输出由观察支持的元信息报告或科学问题答案；推理阶段是否继续运行完整MCTS、采用何种解码配置及确切工具接口，在所给章节中原文未明确报告。

**复现信息**

公平复现时最关键的是保留可执行环境和状态一致性：每个行动$a_t$必须在当时状态$s_{t-1}$上由$\mathcal{E}$执行得到$o_t$，并通过状态转移函数$F$形成$s_t$，不能以模型臆造的工具结果替代真实观察。轨迹需包含完整的`<think>`、`<python>`、`<result>`和`<answer>`块，并满足最低探索深度及至少一个实质观察；规则验证应拒绝未解决执行错误、缺失或畸形块、空观察和不一致状态转移。

还需实现两级质量控制：执行后分数低于$\theta_{\mathrm{post}}$的节点保留来源信息但禁止继续扩展；逐步验证器将“行动是否由前文推出”和“后续推理是否由观察支持”分别标记为支持、无支持或矛盾，影响证据链与最终答案的异常分支必须删除。难度等级的八类种子映射、搜索预算、$\lambda$、$\beta$、$\delta_{\mathrm{fpu}}$、$T_p$、$k_{\min}$、$k_{\max}$、熵权重、评审器模型、微调超参数及具体沙箱配置在所给节选中原文未明确报告，不能据此补造数值。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- SciDataSailor-Bench-Meta：包含 627 个元信息总结任务，要求智能体在仓库层面描述文件组织、格式、模式、元数据、来源和使用限制。其作用是检验智能体能否通过实际探索形成覆盖整个数据仓库的结构化认识；回答以轨迹生成的参考答案为依据，由 LLM judge 评分。
- SciDataSailor-Bench-QA：包含 586 个科学问答任务，要求智能体定位相关文件、执行分析并返回由数据支持的答案。它主要检验跨文件检索、代码执行、数值计算和证据整合，而不只是阅读文件名或复述元数据。
- 完整 SciDataSailor-Bench 覆盖生命科学、地球科学和物理科学中的 27 个数据集。所给章节未报告训练集、验证集与测试集的具体划分方式；因此无法据此判断是否按仓库或科学领域进行了严格隔离。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass@1**

单次运行所生成最终答案通过对应评分规则的比例。Meta 任务由 LLM judge 对照轨迹生成的参考答案评分；QA 对数值答案采用容差匹配，对非数值答案检查文本、类别及单位一致性。 （越高越好，因为它直接反映一次智能体运行得到合格答案的概率。）

</div>
<div class="metric-item" markdown="1">

**成功率（SR）**

在给定最大 ReAct 步数预算内生成完整交互轨迹的比例。它衡量智能体能否正常结束探索流程，但完成轨迹不等同于最终答案正确。 （越高越好，因为更高的数值表示较少发生超出预算、执行停滞或未能完成流程的情况。）

</div>
<div class="metric-item" markdown="1">

**平均 ReAct 步数（Avg. Steps）**

智能体平均使用的完整“思考—代码或动作—观察”循环数；每一步可以包含一个或多个并行 Python 工具调用。 （在 Pass@1 和 SR 不下降的前提下越低越好，因为它表示更高的交互效率；若正确率或完成率同时下降，较少步骤也可能只是过早终止，不能单独视为更优。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### SciDataSailor-Bench-Meta，闭源模型 GPT-5.4，最大 ReAct 步数从 12 增至 24。

<div class="result-value" markdown="1">

GPT-5.4 的 Pass@1 从 65.22% 提升至 69.57%，SR 从 98.07% 提升至 100.00%，平均步数仅从 6.03 增至 6.10；它在表中闭源模型组的两个预算设置下均取得最高 Pass@1。

</div>

作者结果表明，GPT-5.4 通常不需要用满预算，并且增加预算主要消除了少量未完成轨迹，同时带来有限的正确率增益。这说明较强模型的主要瓶颈可能不只是允许执行的步数；但该结果仅来自 Meta 任务，不能据此断言它在科学 QA、所有学科或现实开放环境中同样领先。

<div class="result-source" markdown="1">

来源：表 2，SciDataSailor-Bench-Meta

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GPT-5.4 65.22 98.07 6.03 69.57 100.00 6.10

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### SciDataSailor-Bench-Meta，大于 30B 的开放权重模型，最大 ReAct 步数为 12 和 24。

<div class="result-value" markdown="1">

DeepSeek-V4-Pro 的 Pass@1 从 16.43% 增至 52.66%，SR 从 28.99% 增至 79.71%，平均步数从 11.05 增至 15.49；在 24 步设置下，它取得该开放权重大模型组最高的 Pass@1。

</div>

这一行显示 DeepSeek-V4-Pro 对交互预算高度敏感：12 步时平均步数已接近上限且 SR 很低，24 步则正确率和完成率均大幅提高。合理解释是许多仓库探索需要更长的执行链，而非模型完全不会做；不过增加预算同时提高了平均成本，而且 79.71% 的 SR 表明仍有约五分之一运行未形成完整轨迹。

<div class="result-source" markdown="1">

来源：表 2，SciDataSailor-Bench-Meta

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

DeepSeek-V4-Pro 16.43 28.99 11.05 52.66 79.71 15.49

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### SciDataSailor-Bench-Meta，小于 30B 的开放权重模型，在 24 步最大预算下比较完成率与答案正确率。

<div class="result-value" markdown="1">

未经专门微调的 Qwen3-32B 达到 93.72% SR，但 Pass@1 仅为 13.53%，平均使用 5.67 步。

</div>

该结果揭示 SR 与任务正确性不能混用：Qwen3-32B 几乎总能在预算内结束，但大多数最终回答仍未通过评分。较低平均步数也不必然代表高效推理，可能意味着探索不足或过早作答。因此评估智能体时必须联合查看 Pass@1、SR 和步数，而不能只依据流程是否完成。

<div class="result-source" markdown="1">

来源：表 2，SciDataSailor-Bench-Meta

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen3-32B 14.98 86.48 5.69 13.53 93.72 5.67

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验章节在表 3 开始处被截断，未包含 SciDataSailor-Bench-QA 的具体结果，也没有定性案例。因此当前证据只能充分分析 Meta 任务，不能验证模型在数值计算、跨文件科学推理和单位一致性方面的实际表现。
- Meta 回答使用 LLM judge 和轨迹生成参考答案评分，但所给内容未报告人工一致性验证、置信区间、重复运行方差或统计显著性。与此同时，统一脚手架有利于公平比较，却不能排除不同模型对 XML、TIR 或函数调用适配器敏感而造成的接口效应。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 闭源强模型 GPT-5.4、Gemini-3.1-Pro 和 Claude-Opus-4-7-Thinking：代表较强的通用规划与工具使用能力，用于估计当前闭源智能体在科学数据探索上的性能上限。
- 大规模开放权重模型，包括 GLM-5.1、Kimi-K2.6、DeepSeek-V4-Pro、DeepSeek-V4-Flash 和 GPT-OSS-120B：用于判断开放模型在相同工具环境中与闭源模型的差距，并比较不同模型的长程执行和恢复能力。
- 小于 30B 的开放权重模型，包括 Qwen3.5-27B、Qwen3.5-35B-A3B、Qwen3-32B、GPT-OSS-20B 和 Qwen3.5-9B：用于考察较低参数规模或稀疏架构是否仍能完成仓库级探索。
- Qwen3.5-9B-SFT 与未经微调的 Qwen3.5-9B：二者共享基础模型规模，前者使用作者构造的轨迹语料进行监督微调，因此这一对照最直接地测试 SciDataSailor 轨迹训练的作用。

**实验想回答的问题**

- 在统一的 ReAct/CodeAct 智能体框架、Python 沙箱和评分流程下，不同闭源与开放权重模型能否完成科学数据仓库的元信息总结和数据驱动问答？这主要比较模型的规划、可执行分析、观察解释及错误恢复能力。
- 增加最大 ReAct 步数以及使用 SciDataSailor 合成轨迹进行监督微调，能否提高任务正确率和轨迹完成率，并减少完成任务所需的交互步骤？

**实验实现**

所有模型使用统一的 ReAct 风格智能体脚手架，并以 CodeAct 风格协议执行 Python。智能体只能在受控沙箱中使用 Python，网页搜索、外部检索和辅助工具均被禁用；所有模型接收相同任务约定、沙箱和评分流程，从而尽量把差异归因于规划、分析执行、观察解释与错误恢复能力。实验分别设置 12 步和 24 步的最大 ReAct 预算，采样温度为 0.6，$\mathrm{top}\text{-}p=0.95$。不同模型所需的 XML、TIR 和函数调用适配器见附录 B.1。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 以未经微调的 Qwen3.5-9B 为对照，加入 SciDataSailor 轨迹监督微调；在 12 步预算下评估。 | Qwen3.5-9B-SFT 的 Pass@1 为 28.99%，相对基础模型的 14.01% 提高 14.98 个百分点；SR 从 49.76% 提高至 96.14%，平均步数从 10.21 降至 6.24。 | 这一对照主要隔离轨迹监督微调的作用：同规模基础模型经过训练后，不仅更常得到合格答案，也更常在预算内完成，而且平均交互更短。它支持作者关于合成轨迹能教授探索和执行策略的主张；不过这不是严格的单组件消融，因为所给实验没有分别移除 MCTS 中的四个机制，也不能排除训练数据量或一般领域适配带来的影响。 | 表 2，SciDataSailor-Bench-Meta<br><span class="experiment-evidence">Qwen3.5-9B 14.01 49.76 10.21 22.71 70.05 9.42
Qwen3.5-9B-SFT 28.99↑14.98 96.14↑46.38 6.24↓3.97 24.64↑1.93 96.14↑26.09 5.92↓3.50</span> |
| 同一 Qwen3.5-9B 与 Qwen3.5-9B-SFT 对照，但使用 24 步最大预算。 | 监督微调将 Pass@1 从 22.71% 提高至 24.64%，仅增加 1.93 个百分点；SR 从 70.05% 提高至 96.14%，平均步数从 9.42 降至 5.92。 | 在较宽松预算下，微调对“能否完成流程”和交互效率仍有明显作用，但对最终正确率的边际提升远小于 12 步设置。分析上，这意味着训练可能主要改善了终止、规划紧凑性或错误恢复，而未完全解决答案内容质量；由于原文未提供显著性检验，不能判断 1.93 个百分点是否具有统计稳定性。 | 表 2，SciDataSailor-Bench-Meta<br><span class="experiment-evidence">Qwen3.5-9B 14.01 49.76 10.21 22.71 70.05 9.42
Qwen3.5-9B-SFT 28.99↑14.98 96.14↑46.38 6.24↓3.97 24.64↑1.93 96.14↑26.09 5.92↓3.50</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向科学数据仓库探索的工具交互式 LLM Agent 任务，并用 MCTS 合成执行轨迹。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`f9f2c6e896d37b3ff67397406ff0078d79b0d49cf1ed80c397e79989dd856a83`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
