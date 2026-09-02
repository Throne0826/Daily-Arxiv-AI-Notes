---
title: "[论文解读] Replacing Training with Memory: Listwise Selection for Text-to-SQL"
description: "[arXiv 2609.00834][LLM Reasoning] MaP-SQL用从标注数据中提炼的结构化记忆代替选择器微调，并通过多种候选排列的排序聚合缓解位置偏差，从而实现无需更新模型参数的Text-to-SQL列表式候选选择。"
arxiv_id: "2609.00834"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:48:11.824972+00:00"
source_sha256: "0289cd0be0a54ce0898541f69a8cec7bc623080a25e3f92efc6c5419dd300c05"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "Text-to-SQL"
  - "列表式选择"
  - "免微调选择器"
  - "结构化记忆检索"
  - "排列聚合"
  - "位置偏差"
  - "执行结果反馈"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.00834</p>

# Replacing Training with Memory: Listwise Selection for Text-to-SQL

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Yeonseok Jeong, Soyoung Yoon, Seongjun Lee, Seung-won Hwang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Seoul National University；KAIST</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00834v1) · [PDF 下载](https://arxiv.org/pdf/2609.00834v1) · **关键词** Text-to-SQL, 列表式选择, 免微调选择器, 结构化记忆检索, 排列聚合, 位置偏差, 执行结果反馈<br>
**代码**: [https://github.com/ldilab/MAP-SQL](https://github.com/ldilab/MAP-SQL)

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

MaP-SQL用从标注数据中提炼的结构化记忆代替选择器微调，并通过多种候选排列的排序聚合缓解位置偏差，从而实现无需更新模型参数的Text-to-SQL列表式候选选择。

**不用术语来说**：面对同一个自然语言问题，Text-to-SQL系统通常会生成多条看起来都合理的SQL，但最终只能提交一条。困难在于，候选之间可能只差一个表连接、筛选条件或聚合操作，却产生完全不同的答案；让大模型一次比较多条SQL通常更容易发现这些细微差别，但专门训练这种比较器需要处理很长的数据库模式、SQL和执行结果，成本较高，而且候选放置顺序还可能改变模型判断。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出无需微调选择器参数的列表式选择框架MaP-SQL：将训练数据中的问题—SQL知识整理为可复用的结构化记忆，按测试问题检索相关记忆，并将其作为比较候选SQL的显式判据。
- 提出成本感知的排列聚合机制：改变候选SQL的输入顺序并汇总多次排序，以降低“中间位置候选容易被忽略”的偏差，同时利用执行结果和选择性逐点评分减少不必要的模型调用与上下文开销。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

Text-to-SQL旨在把自然语言问题转换为可在给定数据库上执行的SQL查询。本文关注现代系统中的“生成—执行—选择”设置：系统先生成多个候选SQL并获得其执行结果，再由选择器挑出最可能正确的候选。按每次联合评估的候选数量，选择器可分为逐点式、成对式和列表式；列表式选择器能在同一上下文中比较多个候选的结构与结果差异，同时避免全量成对比较的$O(n^2)$开销，但长候选列表会增加训练成本，并使语言模型容易受到候选排列位置的影响。本文因此研究：在不更新选择器参数的前提下，如何利用训练数据构造的外部记忆和推理时的排列聚合，保留列表式联合比较的优势。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**列表式选择（listwise selection）**

选择器一次读取并联合比较多个候选SQL，而不是独立评分或逐对比较。其价值在于能直接识别候选之间细微但决定性的差异，例如连接条件、聚合操作或过滤范围不同。

</div>
<div class="concept-item" markdown="1">

**执行结果反馈（execution feedback）**

候选SQL在数据库上运行后得到的输出、错误或结果等价关系，可作为判断候选行为的信号。多个SQL即使文本不同，也可能产生相同执行结果，因而可以被归入同一执行结果组以减少重复比较。

</div>
<div class="concept-item" markdown="1">

**位置偏差与排列聚合**

位置偏差指语言模型的选择会受到候选在输入列表中位置的影响，其中“迷失在中间”表现为模型较难充分利用长上下文中部的信息。排列聚合通过改变候选顺序并综合多次排序，降低单一输入顺序对最终选择的支配作用。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括自然语言问题、对应数据库模式、由上游生成器产生的$n$个候选SQL及其执行结果；系统还可访问由带标注问题—SQL训练对提炼而成的外部结构化记忆。输出是候选集合中排名最高、预计能正确回答问题的一条SQL。本文假设候选池已经给定，重点不是重新生成SQL，而是在使用现成预训练语言模型且不更新选择器参数的条件下完成重排序；这里“免微调”不等于完全不使用训练数据，而是将训练数据中的自然语言—模式元素—SQL操作—预期输出映射存入可检索记忆，并在测试时作为显式选择标准。为控制排列聚合成本，候选按执行结果分组，使理论排列空间由$O(n!)$缩减为$O(g!)$，其中通常有$g\ll n$。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$n$**

待选择的SQL候选总数。

</div>
<div class="notation-item" markdown="1">

**$g$**

按照相同执行结果划分后得到的候选组数量，通常远小于$n$。

</div>
<div class="notation-item" markdown="1">

**$O(n^2)$**

对$n$个候选进行全量成对比较时的比较复杂度。

</div>
<div class="notation-item" markdown="1">

**$O(g!)$**

利用执行结果分组后，论文所讨论的组级排列空间上界。

</div>

</div>

**直接相关的工作**

- **$R^3-SQL$**: 与本文最直接相关的既有选择器方法。原文称其在训练中处理位置偏差，并在无法可靠区分候选时使用逐点选择器作为决胜机制；MaP-SQL则把选择准则与偏差缓解都转移到推理阶段，分别采用记忆检索和排列聚合。
- **MCS-SQL**: 同样是不微调选择器的多项选择式SQL选择方法，并在把候选交给选择器前进行排序；但原文指出，该工作没有系统研究列表式选择面临的位置偏差及相应优化，而这些正是MaP-SQL的目标问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现代Text-to-SQL系统常采用“生成—执行—选择”流程：生成器给出多个候选SQL，执行器获得运行结果，选择器再决定最终答案。实际部署需要选择器既能联合比较候选的SQL结构、数据库模式使用方式和执行结果，又不能因长上下文训练、频繁模型调用或更换底层大模型而产生过高成本；否则，多候选生成带来的潜在正确答案也可能在最后一步被错误淘汰。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **逐点与成对选择**：逐点方法独立为每条候选SQL打分，再按分数选择；成对方法每次比较两条候选，以直接判断哪一条更好。前者计算简单但缺少候选间的相对参照，后者能够显式对比差异，却在候选数为$n$时通常需要接近$O(n^2)$次比较。
- **经过微调的列表式选择**：列表式方法在一次上下文中同时查看多条候选SQL并给出整体排序，可以横向检查表连接、过滤条件、SQL操作及执行结果。已有做法通过包含多条SQL及其执行信息的训练样本微调选择器，使模型学习排序判据，并尝试降低候选输入位置对结果的影响。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 逐点评分无法充分利用候选之间的细微差异，可能把各自看来合理、但相互对照后明显有错的SQL赋予相近分数；成对比较虽然更直接，却具有$O(n^2)$级比较开销，候选池扩大后会显著增加调用次数和输入Token。
- 微调列表式选择器需要在每个训练样本中同时放入多条SQL、数据库模式和执行结果，造成长上下文与较高计算成本；即使采用列表式输入，大模型仍可能出现“lost-in-the-middle”位置偏差，即对列表中间候选关注不足，使排序随候选排列发生变化。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一种同时满足三项要求的SQL候选选择方案：保留列表式联合比较的辨别能力，不通过参数更新学习选择规则，并在推理阶段以可控成本处理位置偏差。这里的“无需微调”并不等于完全不使用监督信息；论文仍允许利用标注的问题—SQL对构造可检索记忆，缺口在于如何把监督知识从模型参数迁移到外部、可复用且可解释的决策依据中。

</div>
<div markdown="1"><span>核心问题</span>

能否把列表式选择器通常通过微调获得的两种能力——形成可靠的SQL选择判据与减轻输入顺序偏差——改写为推理时的记忆检索和多排列排序聚合，从而在不更新选择器参数的条件下，提高同一候选池上的选择准确性、稳定性与效率？

</div>
<div markdown="1"><span>作者直觉</span>

如果模型只凭通用语言能力判断SQL，它可能不知道当前问题中的措辞应对应哪个模式元素、操作符或预期输出；检索相似训练实例提炼出的结构化记忆，相当于在考试时提供针对当前题型的检查清单，使模型能依据明确线索横向核对候选。另一方面，单次列表排序可能受候选位置干扰；让候选换几个位置后重复判断并汇总排名，类似由多个不同座次下的评审结果投票，可以让真正由SQL内容支持的偏好保留下来，而偶然的位置效应相互抵消。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MaP-SQL是一个无需微调的Text-to-SQL列表式选择框架。输入包括自然语言问题$x$、数据库模式$S$、候选生成器给出的SQL集合$C=\{q_i\}_{i=1}^{n}$，以及每条查询执行后缓存的结果$e_i$；输出是单条预测查询$\hat q\in C$。其核心是把通常通过微调学到的两类能力改为推理时机制：从训练样本预先提炼并检索结构化记忆，为候选比较提供显式判断标准；再对候选采用基于执行结果分组的多次排列与排名聚合，降低列表式大模型对输入位置的依赖。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 离线生成结构化记忆库

使用与选择器相同的大语言模型$f_{\mathrm{mem}}$，把每个训练样本提炼为记忆$m_j$。记忆按Encoding、Translating和Decoding三组组织，分别记录语言到模式元素的对应关系、语义到SQL操作的转换规则，以及输出形态与查询约束。

<div class="method-step__io" markdown="1">

**输入**：训练集$\mathcal D$中的问题$x_j$、数据库模式$S_j$和正确SQL查询$q_j^*$。<br>
**输出**：可复用的结构化记忆库$M=\{m_j\}_{j=1}^{|\mathcal D|}$。

</div>

**直观理解**：这里不让模型通过训练把经验藏进参数，而是把正确样例整理成可检索的“检查清单”。面对新问题时，选择器可以直接参照相似问题中哪些列、操作和输出形式通常是正确的。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 检索与当前问题相关的记忆

稠密检索器比较$x$与各训练问题$x_j$的向量相似度，选出最相关的记忆集合$\mathcal M(x)$并置于选择提示词前部。实际并非机械固定$k$，而是在选择器上下文长度允许时尽可能装入更多相关记忆，以提供多种验证视角。

<div class="method-step__io" markdown="1">

**输入**：测试问题$x$、记忆库$M$以及训练问题的稠密向量表示。<br>
**输出**：面向当前问题的结构化判断标准集合$\mathcal M(x)$。

</div>

**直观理解**：这类似于开卷考试时先找出几道与当前题意最接近的例题，但只取其中可迁移的判题规则，而不是复制旧SQL。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行候选、分组并进行滑动窗口列表排序

系统先执行每个$q_i$一次，并按照相同执行结果把候选归组，以结果出现频率较高者优先形成初始顺序；随后用窗口大小$w=8$、步长$s=4$从后向前滑动。每次调用列表式选择器，同时比较窗口内至多八个$(q_i,e_i)$，并依据同一组记忆更新该窗口的局部排名。

<div class="method-step__io" markdown="1">

**输入**：问题$x$、模式$S$、候选集合$C$、缓存的执行结果$\{e_i\}$和检索记忆$\mathcal M(x)$。<br>
**输出**：覆盖全部候选的初步全局排序$R$。

</div>

**直观理解**：多数候选得到同一执行结果时，该结果可作为较可靠的先验；滑动窗口则像分批复审，使候选数达到$32$时也不必一次把所有SQL塞进模型。执行结果只计算一次并缓存，后续窗口和排列重复使用。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 组内置换、排名聚合与可选决胜

系统保持按组大小确定的组间顺序，只随机改变每个组内部的候选顺序，并进行$K$次列表排序；随后以候选的平均名次$\mu_i$升序聚合结果。若基于成对名次差计算的置信度$P(a>b)$低于阈值$\tau=0.95$，则把前两名视为并列，并可用点式奖励模型分别打分决胜。

<div class="method-step__io" markdown="1">

**输入**：按执行结果划分的候选组、初步顺序$R$以及列表式选择器。<br>
**输出**：最终选择的单条SQL查询$\hat q$。

</div>

**直观理解**：普通全局打乱会破坏“多数执行结果更可信”的有用线索，因此这里只在同结果候选之间换位置。多次观察后取平均名次可削弱模型偏爱列表开头或结尾的现象；只有前两名难分高下时才额外逐条评分，以控制推理成本。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 结构化记忆生成

$$
M=\{m_j\}_{j=1}^{|\mathcal D|},\qquad m_j=f_{\mathrm{mem}}(x_j,S_j,q_j^*)
$$

**符号说明**

- $\mathcal D$：用于构建记忆的训练数据集。
- $M$：由全部训练样本提炼得到的结构化记忆库。
- $m_j$：第$j$个训练样本对应的结构化记忆。
- $f_{\mathrm{mem}}$：根据提示词提炼记忆的大语言模型函数；原文采用与选择器相同的模型。
- $x_j$：第$j$个训练样本的自然语言问题。
- $S_j$：第$j$个样本对应的数据库模式，包括表、列及其关系。
- $q_j^*$：第$j$个样本的正确SQL查询。

<div class="equation-explanation" markdown="1">

**直观理解**：该式表示把每个带正确答案的训练样本压缩成一份显式规范，再汇总为记忆库。它是“用记忆替代训练”的关键：知识不通过梯度更新写入选择器参数，而是在推理时按需检索并放进提示词。<br>
**原文位置**：公式(1)，第4.1节Step 1: Memory Generation

</div>

</div>

<div class="equation-block" markdown="1">

#### 基于成对名次差的前两名置信度

$$
P(a>b)=T_{K-1}\!\left(\frac{\bar d_{a,b}}{s_{a,b}/\sqrt K}\right),\qquad d_{a,b}^{(k)}=r_b^{(k)}-r_a^{(k)}
$$

**符号说明**

- $a$：按平均名次排序后的第一名候选。
- $b$：按平均名次排序后的第二名候选。
- $K$：采用不同组内排列进行列表排序的运行次数。
- $r_a^{(k)}$：候选$a$在第$k$次运行中的名次。
- $r_b^{(k)}$：候选$b$在第$k$次运行中的名次。
- $d_{a,b}^{(k)}$：第$k$次运行中$b$与$a$的成对名次差；正值表示$a$排在$b$之前。
- $\bar d_{a,b}$：全部运行中成对名次差的均值。
- $s_{a,b}$：全部成对名次差的样本标准差。
- $T_{K-1}$：自由度为$K-1$的Student $t$分布累积分布函数。
- $P(a>b)$：用于判断$a$是否稳定优于$b$的轻量级排名置信分数，不被作者视为正式假设检验。

<div class="equation-explanation" markdown="1">

**直观理解**：该式检查第一名是否在多次换序后仍稳定领先第二名：平均领先越大、波动越小，置信分数越高。当$P(a>b)<\tau$时，系统不强行相信列表排名，而是声明并列并可触发点式模型决胜。<br>
**原文位置**：公式(5)，第4.2节Group-Based Permutation

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：MaP-SQL不对列表式选择器进行参数微调，也没有需要反向传播优化的训练损失。训练集仅作为离线记忆来源，由$f_{\mathrm{mem}}$把$(x_j,S_j,q_j^*)$转成$m_j$；推理阶段的平均排名和$P(a>b)$是选择与置信启发式，而非训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Encoding–Translating–Decoding结构化记忆**

Encoding包含模式落地、连接路径和过滤语义，用来检查问题短语是否对应正确表、列、连接及条件；Translating包含聚合、排序与范围、条件及空值处理，用来检查SQL操作；Decoding包含输出形式、元级查询约束和额外SQL构造，用来检查返回列、结果形状及是否存在多余连接或错误聚合。各记忆是短小的规范集合，而非完整历史轨迹。

> 直观理解：这三个部分依次回答“问题说的是数据库里的什么”“应采用什么SQL操作”“最终应返回什么”。结构化形式让选择器能够逐项核对外观相似的候选，而不是仅凭整体语感猜测。

**2. 带执行反馈的滑动窗口列表选择器**

选择器$f_{\mathrm{list}}$同时接收$x$、$S$、$\mathcal M(x)$及窗口内多个$(q_i,e_i)$，输出完整局部排序而非仅判断单条查询。窗口从后向前更新$R$，使较优候选逐步移向前部；相同记忆在一次提示中统一约束所有候选，从而支持直接横向比较。

> 直观理解：点式方法分别看每条SQL，难以发现两个候选之间的细小差别；列表式方法把它们摆在一起比较。执行结果还能暴露报错、空结果或结果形态不符等问题，但它只是证据，不能单独保证语义正确。

**3. 分组置换与置信决胜**

候选按执行结果分成$g$组，通常$g\ll n$；算法保留基于组频率的组间优先级，只在组内置换，以减少无信息排列。聚合阶段使用跨$K$次运行的平均排名，并根据同一次运行中前两名的成对名次差估计置信度；点式决胜仅在低置信并列时触发。

> 直观理解：该模块同时保留多数投票先验并测试模型是否因位置变化而改判。成对差值比单独比较两位候选各自的排名波动更合适，因为同一轮中的名次彼此制约。

**训练与推理**

离线阶段遍历训练集，为每个正确Text-to-SQL样本生成Encoding–Translating–Decoding记忆，并保存训练问题的稠密向量以支持检索。在线阶段先接收$x$和$S$，由外部候选生成器产生$C$；每个$q_i$执行一次得到$e_i$并缓存。系统检索$\mathcal M(x)$，按执行结果频率建立初始顺序，以滑动窗口完成列表式重排，再进行多次组内置换并按平均名次聚合。若前两名的置信分数低于$\tau$，可调用点式奖励模型只比较并列候选，最终返回$\hat q$。因此主体完全发生在推理时，点式决胜是可选而非必要路径。

**复现信息**

公平解释方法所需的关键设置为：候选规模实验采用$n=8$或$n=32$；滑动窗口大小$w=8$、步长$s=4$，故单次列表选择最多比较八个候选；所有执行结果只计算一次，并在窗口和置换间缓存复用；候选按执行结果分组，组间顺序由组大小确定，置换仅发生在组内；并列阈值固定为$\tau=0.95$。记忆检索使用问题的稠密表示，原文说明在上下文限制内尽可能加入相关记忆，而非始终使用固定数量；附录的扰动实验明确提到检索器为bge-m3。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- BIRD-dev：主要评测集，包含 1,534 条开发集查询，覆盖大规模、较真实的数据库。它用于比较不同选择策略的准确率与推理成本，并用于附录中的并列消歧消融。记忆库由 BIRD 训练集构建。
- Spider-test：跨领域 Text-to-SQL 测试集，包含 2,147 条查询，用于检验方法能否从主要基准推广到不同数据库领域。记忆库由 Spider 训练集构建。
- EHRSQL：电子健康记录领域数据集，包含 1,008 个问题，用于测试专业领域中的泛化。由于该数据集没有训练划分，实验使用 BIRD 与 Spider 训练集共同构建的外部记忆库，这同时检验了跨数据集记忆迁移能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**执行准确率（Acc.）**

预测 SQL 与标准 SQL 在数据库上产生相同执行结果的查询比例；它衡量最终答案是否等价，而不是 SQL 字符串是否完全相同。 （越高越好，因为相同执行结果通常表示预测查询正确回答了问题。）

</div>
<div class="metric-item" markdown="1">

**平均 LLM 调用次数（Calls）**

每个问题在选择阶段平均触发的大模型调用数，用于衡量推理交互成本；成对比较通常会产生较多调用。 （越低越好，因为在准确率相近时，更少调用意味着更低延迟与服务开销。）

</div>
<div class="metric-item" markdown="1">

**平均输入 token 数（Tokens）**

每个问题在选择阶段消耗的平均输入 token 数，用于近似衡量上下文处理量和推理计算成本。 （越低越好，因为较少 token 通常意味着更低计算量与推理费用，但必须结合准确率判断。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### BIRD-dev，Agentar-Scale-SQL-Generation-32B 生成器，$n=32$ 个固定候选。

<div class="result-value" markdown="1">

完整 MaP-SQL 的执行准确率为 73.08%，比复现的 R³-SQL 高 1.11 个百分点，比成对选择高 2.02 个百分点；这是该主要基准与较大候选池设置下的最高准确率。

</div>

该结果说明，在完全相同的候选池中，结构化记忆和多排列聚合能够帮助选择器更可靠地挑出正确 SQL；因此提升来自选择阶段，而不是生成器额外产生了更好的候选。不过，这一单项比较不能证明方法在所有模型、数据库或候选分布上都必然占优，且 R³-SQL 是在原模型未公开条件下按相同组件复现的算法版本。

<div class="result-source" markdown="1">

来源：Section 5.3, Accuracy；Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On BIRD-dev with Agentar-32B and n=32, it reaches 73.08%, outperforming R³-SQL by 1.11 points and pairwise by 2.02 points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### BIRD-dev，Arctic-Text2SQL-R1-7B 生成器，$n=32$ 个固定候选，比较单个记忆增强列表式选择器与成对选择器。

<div class="result-value" markdown="1">

成对选择平均需要 184.59 次调用和 443,713 个输入 token，而记忆增强列表式选择仅需 5.91 次调用和 27,440 个 token；对应准确率分别为 68.12% 与 72.10%。

</div>

列表式方法一次联合检查多个候选，并利用执行结果分组及预筛分避免大量无意义比较，因此不仅成本显著下降，准确率也没有因减少调用而受损。这里的 token 和调用次数反映该实验协议下的推理负担，不等同于端到端运行时间、货币成本或能耗；原文也未报告这些系统指标。

<div class="result-source" markdown="1">

来源：Section 5.3, Efficiency；Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On BIRD-dev with n=32, pairwise requires on average 184.59 calls and 443,713 tokens per query with Arctic-R1-7B, whereas our listwise selector uses only 5.91 calls and 27,440 tokens.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨数据集泛化，Arctic-Text2SQL-R1-7B 生成器，$n=32$ 个固定候选。

<div class="result-value" markdown="1">

完整 MaP-SQL 在 Spider-test 上达到 87.59% 执行准确率，比 R³-SQL 高 0.77 个百分点，并将调用数减少到后者的约 $1/8.43$；在 EHRSQL 上达到 44.71%，比 R³-SQL 高 0.68 个百分点，调用数减少到约 $1/11.09$。

</div>

在跨领域 Spider 和医疗领域 EHRSQL 上同时出现小幅准确率提升与大幅调用节省，说明优势不局限于 BIRD。EHRSQL 没有训练集，仍可借助 BIRD 与 Spider 的记忆库获得提升，也提供了跨数据集迁移证据；但其绝对准确率仍只有 44.71%，表明专业医疗数据库上的 Text-to-SQL 问题远未解决。

<div class="result-source" markdown="1">

来源：Section 5.3, Generalization；Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

With n=32 on Spider-test, our full method achieves 87.59% accuracy, surpassing R³-SQL by 0.77 points using 8.43× fewer calls. On EHRSQL with n=32, our method reaches 44.71%, improving over R³-SQL by 0.68 points while requiring 11.09× fewer calls.

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

- greedy 与 majority voting：前者直接使用单次或默认生成结果，后者选择候选中占多数的执行答案；二者是不调用学习式选择器的低成本参照，可判断复杂选择流程是否真正带来收益。
- pointwise：使用 Contextual-RM-32B 独立评价每个候选。该模型是由 Qwen2.5-Coder-32B-Instruct 训练得到的强奖励模型，用来检验联合比较多个候选是否优于逐个打分。
- pairwise：复现 CHASE-SQL 的成对比较方式；先把执行结果相同的候选分组，仅比较跨组候选，再汇总比较结果形成排序。它是列表式方法的重要对照，因为比较更细致但理论上会随候选数量快速增加成本。
- R³-SQL（not trained）：组合逐点与成对选择器的多选择器基线。由于原模型未公开，作者采用与 MaP-SQL 相同的生成器和选择器复现其选择算法，以尽量隔离选择算法本身的影响。

**实验想回答的问题**

- 在固定候选 SQL 集合下，无需微调的 MaP-SQL 是否能比贪心、多数投票、逐点、成对及多选择器方法更准确地选出执行结果正确的 SQL，并且这种优势能否跨生成器、候选规模和数据集保持稳定？
- 以结构化记忆支持的列表式选择能否减少选择阶段的 LLM 调用次数与输入 token 数；完整方法的效果是否依赖额外的逐点奖励模型进行并列候选消歧？

**实验实现**

实验使用 Agentar-Scale-SQL-Generation-32B 与 Arctic-Text2SQL-R1-7B 两个 SQL 生成器；每个问题预先生成固定的 $n=8$ 或 $n=32$ 个候选，所有选择策略在相同候选池上评测，以避免把生成质量差异误归因于选择器。列表式与成对组件统一使用 Qwen3-Coder-30B-A3B-Instruct；MaP-SQL 仅在可选的并列消歧阶段使用 Contextual-RM-32B。推理时用 bge-m3 按问题语义相似度检索记忆，不固定检索条数，而是在选择器上下文长度允许范围内尽量加入相关记忆。全部实验在单节点、单张 NVIDIA RTX PRO 6000 GPU 上完成。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| BIRD-dev，Agentar-Scale-SQL-Generation-32B，$n=8$；比较无并列消歧、复用 Qwen3-Coder 消歧及使用独立 Contextual-RM-32B 消歧。 | 不进行并列消歧时，MaP-SQL 的执行准确率为 72.23%，仍高于 R³-SQL 的 71.51%；复用同一个 Qwen3-Coder 后提高到 72.42%，使用独立 Contextual-RM-32B 后进一步提高到 72.62%。 | 该消融隔离了逐点奖励模型的作用：核心列表式记忆机制在没有额外奖励模型时已经超过对照，而独立奖励模型只提供 0.39 个百分点的额外提升；因此它是可选增强，不是方法成立的必要条件。与此同时，该实验只覆盖 BIRD-dev、一个生成器和 $n=8$，尚不能确认相同增量会在其他候选规模或数据集上重现。 | Appendix A.1, Effect of Pointwise Tie-Breaking；Table 8<br><span class="experiment-evidence">Without tie-breaking, MaP-SQL achieves 72.23% execution accuracy. This result is higher than the 71.51% of R³-SQL in the same setting. Using Qwen3-Coder for tie-breaking improves the accuracy to 72.42%. Using Contextual-RM-32B further improves the accuracy to 72.62%.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper improves LLM-based Text-to-SQL reasoning by using retrieved structured memories and permutation-aggregated listwise candidate selection.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`0289cd0be0a54ce0898541f69a8cec7bc623080a25e3f92efc6c5419dd300c05`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
