---
title: "[论文解读] Co-Evolving Structured Knowledge and Reasoning in Language Models"
description: "[arXiv 2608.26386][LLM Reasoning] KBevo将结构化知识库构建与基于知识库的问答推理联合训练，使问答结果的奖励能够反向改善知识的组织方式，从而兼顾知识可控性、可复用性与组合事实推理能力。"
arxiv_id: "2608.26386"
announcement_date: "2026-08-28"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:42:14.976674+00:00"
source_sha256: "437a6d50176dfe6e537e3a829ead961d31ed9332185e958ce6dd277b49bea758"
tags:
  - "LLM Reasoning"
  - "知识密集型问答"
  - "结构化知识库"
  - "检索增强生成"
  - "组合事实推理"
  - "联合优化"
  - "知识可控性"
  - "知识编辑"
  - "结果奖励"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.26386</p>

# Co-Evolving Structured Knowledge and Reasoning in Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Ryan Thomas Noonan, Linxi Zhao, Menghan Xu, Akanksha Sarkar, Mihir Mishra, Dongyoung Go, Kilian Q. Weinberger, Yoav Artzi, Jennifer J. Sun</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Cornell University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26386v1) · [PDF 下载](https://arxiv.org/pdf/2608.26386v1) · **关键词** 知识密集型问答, 结构化知识库, 检索增强生成, 组合事实推理, 联合优化, 知识可控性, 知识编辑, 结果奖励<br>
**代码**: [https://github.com/kilian-group/KBevo](https://github.com/kilian-group/KBevo)

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

KBevo将结构化知识库构建与基于知识库的问答推理联合训练，使问答结果的奖励能够反向改善知识的组织方式，从而兼顾知识可控性、可复用性与组合事实推理能力。

**不用术语来说**：语言模型仅靠训练时记住的事实，容易遗漏、混淆或过时；临时从文档中搜索虽然能补充知识，却常把无关段落一并交给模型。把事实整理成实体—关系形式更便于精确查询和修改，但人工或借助强模型整理的成本很高，而且预先整理出的知识未必正好适合后续问题。本文要解决的是：能否让模型根据实际答题成败，自己学会怎样整理更有用的知识。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出KBevo共演化框架，不再将知识库构建视为固定预处理，而是利用问答结果奖励联合优化结构化知识构建与下游推理，使推理反馈能够直接塑造知识库。
- 建立“离线读取相关文档并构建、索引知识库—在线检索结构化事实并完成问答”的工作方式；作者主张该设计在保持知识可检查、可复用和无需重新训练即可编辑的同时，能够获得有竞争力的知识密集型问答表现。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于知识密集型问答与外部知识增强语言模型的交叉方向。语言模型把事实隐式存入参数时，容易出现记忆不完整、相近事实混淆以及难以检查和更新等问题；检索增强生成（RAG）因此在推理时从外部语料取回信息，但常用的定长文本块并非为组合推理设计，可能带来无关或残缺上下文。结构化知识库将事实表示为可查询的实体与关系，便于精确检索、多跳组合、人工检查和局部编辑，但其覆盖范围受构建模式约束，且通常依赖大量人工标注或昂贵模型生成。本文研究的核心背景是：现有系统往往先独立建立知识存储，再训练或运行推理器，问答失败无法反向改善知识表示。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**检索增强生成（RAG）**

模型回答问题前先从外部语料中检索相关文本，再以检索结果作为生成依据。它能补充模型参数中缺失或过时的事实，但文本块可能包含噪声，也可能只覆盖问题所需证据的一部分。

</div>
<div class="concept-item" markdown="1">

**结构化知识库（KB）**

将事实显式组织为实体及其关系，使系统能够查询单条事实或沿多条关系进行组合推理。与隐式参数记忆相比，这类知识更容易检查、修改和删除，但高质量知识库的构建成本较高。

</div>
<div class="concept-item" markdown="1">

**结果奖励与联合优化**

结果奖励依据最终问答是否成功来提供训练信号，而不要求为每个中间步骤给出人工标签。联合优化意味着知识库构建器与推理模块不再分开训练，最终问答效果可以同时影响二者。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务面向知识密集型问答：系统首先读取一组主题相关文档，将其中可用于回答后续问题的事实整理为结构化知识库，并离线抽取、建立索引以供重复使用；推理阶段接收问题，从该知识库检索事实并进行组合推理，最终输出答案。其关键设定是知识库并非固定的人工预处理产物，而是可学习组件；知识构建与问答推理通过最终问答结果共同优化，使推理失败能够反向提示应补充何种事实、关系或连接。作者同时强调外部结构化存储允许在不重新训练语言模型的情况下直接编辑知识，但所给章节未明确规定知识库的具体形式化模式、问答输入输出符号或训练目标公式。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Retrieval-Augmented Generation（Lewis et al., 2020；Izacard and Grave, 2020）**: 这类方法从外部非结构化文本中检索段落并据此生成答案，是本文的主要比较范式。本文沿用外部知识支撑问答的思路，但转向显式、可编辑的结构化知识，并指出固定文本块可能引入无关信息或仅部分覆盖查询。
- **Search-R1（Jin et al., 2025）**: Search-R1利用结果监督训练模型在逐步推理中发起搜索，说明问答结果奖励可以改善外部知识访问策略；但其知识源仍主要是固定的非结构化内容。KBevo进一步让结果奖励同时训练知识库构建与推理，使被检索的知识表示本身也能随任务共同演化。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

知识密集型应用要求模型准确调用事实，并允许用户检查、纠正和更新这些事实。然而，模型参数中的知识是有损且难以定位的，修正它通常需要昂贵的重新训练；外部知识系统虽然更易更新，但其内容组织方式若不适合推理，模型仍可能无法找到回答多步问题所需的事实链。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于非结构化文本的检索增强生成与搜索代理**：系统在推理时从外部语料中检索固定长度的文本块，再让语言模型结合问题和检索文本生成答案。该路线能够访问较新的外部信息，并减少完全依赖模型参数所导致的事实幻觉。
- **基于结构化知识库的检索与推理**：系统把事实显式表示为可查询的实体及关系，再检索相关事实进行组合推理。与整段文本相比，这种表示便于精确访问单条事实，也更容易检查、编辑和控制模型可使用的外部知识。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 非结构化检索通常以固定长度切分文本，切分目标偏向信息覆盖而非推理需求，因此检索结果可能夹带无关内容，或只覆盖问题所需证据的一部分；这会增加上下文噪声，并削弱多步事实组合的可靠性。
- 结构化知识库受到预设模式和构建流程的约束，高质量构建往往依赖大量人工标注或昂贵的前沿模型推理；更关键的是，现有知识库通常独立于下游推理而建立，答题失败无法反向指出应补充哪些事实、关系或连接。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有路线缺少一种可扩展的闭环机制：知识表示应由下游任务的实际效果来监督，而不是先固定知识存储、再单独训练推理器。具体而言，尚缺少能够把问答成败信号传回知识库构建过程，并同时学习“构造什么结构化知识”与“如何利用这些知识推理”的端到端框架。

</div>
<div markdown="1"><span>核心问题</span>

能否仅借助知识密集型问答的结果奖励，联合优化结构化知识库构建器与推理器，使生成的知识库更适合答案检索和组合事实推理，同时保留结构化知识可检查、可编辑及可跨查询复用的优势？

</div>
<div markdown="1"><span>作者直觉</span>

如果知识库只按通用抽取标准建立，它可能包含大量表面正确却对答题无帮助的事实，也可能缺少连接答案所需的关键关系。让构建器与推理器共同接受问答结果反馈，相当于用真实使用效果检验知识组织：能够帮助检索并完成正确推理的事实结构得到强化，导致失败的缺失连接或不合适表示则有机会在训练中调整。知识库仍可预先离线构建和索引，因此同一批结构化知识能够被多个后续问题重复使用。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

KBevo把知识库构建与基于知识库的问答统一为同一个策略模型$\pi_\theta$的两个阶段。给定支持文档$c$，阶段1生成由$(\text{entity},\text{relation},\text{value})$三元组组成的知识库$G=(V,E)$；给定问题$q$，阶段2通过工具调用查询$G$中的$(\text{entity},\text{relation})$并取得对应值，再组合多条事实生成答案。两个阶段共享参数$\theta$，但知识库只在训练时随策略共同演化；部署时先离线构建并索引知识库，之后将其固定并复用于多个问题。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 支持文档到候选知识库

策略$\pi_\theta$针对每篇文档采样$K$个候选知识库$G_{b,k}$，将实体级原子事实表示为$(\text{entity},\text{relation},\text{value})$三元组。全部三元组形成图$G=(V,E)$，其中$V$包含实体和值，$E$表示带关系标签的连接。

<div class="method-step__io" markdown="1">

**输入**：训练样本$(c_b,q_b,a_b^*)$中的支持文档$c_b$，以及知识库构建提示$p^{\mathrm{kb}}(c_b)$。<br>
**输出**：每个样本对应的候选知识库集合$\{G_{b,k}\}_{k=1}^{K}$。

</div>

**直观理解**：模型不是保留整段文本，而是把“梅西—效力球队—迈阿密国际”之类的事实拆成可单独查询的卡片。多个候选版本让训练过程能够比较哪种事实选择和连接方式最有助于答题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 知识库检索与多次问答

模型可发出针对$(\text{entity},\text{relation})$的数据库查询，系统把命中的值注入当前上下文；在每个$G_{b,k}$上采样$M$条答案轨迹$\hat y_{b,k,m}$，因此每道题共有$K\times M$条问答轨迹。模型可以连续查询并组合多条原子事实，以完成多跳推理。

<div class="method-step__io" markdown="1">

**输入**：问题$q_b$、问答提示$p^{\mathrm{qa}}(q_b)$以及某个候选知识库$G_{b,k}$。<br>
**输出**：预测答案及其检索、推理轨迹$\{\hat y_{b,k,m}\}_{m=1}^{M}$。

</div>

**直观理解**：这类似于只向数据库询问当前需要的字段，而不是把若干长文档全部塞入上下文。多次作答用于判断性能差异究竟来自知识库质量，还是来自回答过程中的随机性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 由答案结果反向评价知识库

每条问答轨迹以预测答案和标准答案之间的F1作为奖励$r_{b,k,m}$；同一知识库对应的$M$个奖励取平均，得到知识库级奖励$\bar r_{b,k}$。问答优势在固定$(b,k)$的$M$次作答内标准化，知识库优势则在同一道题的$K$个候选知识库之间标准化。

<div class="method-step__io" markdown="1">

**输入**：预测答案$\hat y_{b,k,m}$、标准答案$a_b^*$以及每条问答轨迹所属的候选知识库$G_{b,k}$。<br>
**输出**：问答优势$A^{\mathrm{qa}}_{b,k,m}$与知识库优势$A^{\mathrm{kb}}_{b,k}$。

</div>

**直观理解**：系统没有为每个三元组单独提供人工标签，而是看“用这套知识最终能否答对题”。如果某个知识库反复带来更好的答案，它的构建轨迹就获得更强的正向学习信号。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 联合GRPO更新与部署

将知识库构建轨迹和问答轨迹拼接进同一次GRPO更新，采用裁剪代理目标限制策略变化；由于每题有$K$条知识库轨迹而有$K\times M$条问答轨迹，知识库目标权重设为$\lambda=M$。部署时只执行一次阶段1以离线构建和索引知识库，随后固定该知识库，对每个问题仅执行阶段2检索与生成。

<div class="method-step__io" markdown="1">

**输入**：阶段1和阶段2的全部生成轨迹、两类优势，以及旧策略$\pi_{\theta_{\mathrm{old}}}$。<br>
**输出**：能够同时构建任务适配知识库并在其上检索推理的策略$\pi_\theta$，以及可持久化、复用和编辑的知识库。

</div>

**直观理解**：构建者和答题者其实是同一个模型：答题结果既训练“怎样推理”，也训练“应该保存什么事实”。上线后不再为每个问题重复试验$K\times M$次，而是像维护一套可反复查询的数据库那样使用已建知识库。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 双阶段联合GRPO目标

$$
\mathcal{J}(\theta)=\lambda\,\mathcal{J}^{\mathrm{kb}}(\theta)+\mathcal{J}^{\mathrm{qa}}(\theta),\qquad \lambda=M
$$

**符号说明**

- $\mathcal{J}(\theta)$：用于更新共享策略参数的联合优化目标。
- $\theta$：知识库构建阶段与问答阶段共享的模型参数。
- $\mathcal{J}^{\mathrm{kb}}(\theta)$：阶段1知识库构建轨迹的GRPO裁剪代理目标。
- $\mathcal{J}^{\mathrm{qa}}(\theta)$：阶段2检索与回答轨迹的GRPO裁剪代理目标。
- $\lambda$：两个阶段之间的权重系数，文中设为问答采样数M。
- $M$：每个候选知识库上生成的问答轨迹数量。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标要求一次参数更新同时改进“建库”和“用库”。每道题仅产生$K$条建库轨迹，却产生$K\times M$条问答轨迹，因此设置$\lambda=M$，使两个阶段在总梯度权重上大致匹配，避免问答轨迹仅因数量更多而压过知识库构建信号。<br>
**原文位置**：附录A.1，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 知识库级奖励与双层相对优势

$$
\bar r_{b,k}=\frac{1}{M}\sum_{m=1}^{M}r_{b,k,m},\qquad A^{\mathrm{kb}}_{b,k}=\frac{\bar r_{b,k}-\mu^{\mathrm{kb}}_b}{\sigma^{\mathrm{kb}}_b},\quad \mu^{\mathrm{kb}}_b=\frac{1}{K}\sum_{k=1}^{K}\bar r_{b,k};\qquad A^{\mathrm{qa}}_{b,k,m}=\frac{r_{b,k,m}-\mu^{\mathrm{qa}}_{b,k}}{\sigma^{\mathrm{qa}}_{b,k}},\quad \mu^{\mathrm{qa}}_{b,k}=\frac{1}{M}\sum_{m=1}^{M}r_{b,k,m}
$$

**符号说明**

- $b$：小批次中的问题或训练样本索引。
- $k$：同一道题的第k个候选知识库索引。
- $m$：给定候选知识库上的第m条问答轨迹索引。
- $r_{b,k,m}$：预测答案与标准答案之间的F1奖励。
- $\bar r_{b,k}$：候选知识库$G_{b,k}$上M次问答奖励的均值，即该知识库的下游效用奖励。
- $A^{\mathrm{kb}}_{b,k}$：在同一道题的K个候选知识库之间标准化得到的知识库构建优势。
- $A^{\mathrm{qa}}_{b,k,m}$：在固定问题与知识库的M条问答轨迹之间标准化得到的问答优势。
- $\mu^{\mathrm{kb}}_b$：样本b的K个候选知识库的平均奖励。
- $\sigma^{\mathrm{kb}}_b$：样本b的候选知识库奖励标准差。
- $\mu^{\mathrm{qa}}_{b,k}$：固定样本b和知识库k时M条问答轨迹的平均奖励。
- $\sigma^{\mathrm{qa}}_{b,k}$：固定样本b和知识库k时问答奖励的标准差。
- $K$：每篇支持文档采样的候选知识库数量。
- $M$：每个候选知识库对应的问答轨迹数量。

<div class="equation-explanation" markdown="1">

**直观理解**：首先用同一知识库上多次作答的平均成绩评价该知识库，再把它与同题的其他候选库比较；同时，每条答案只与同一知识库条件下的其他答案比较。这样，回答好坏能直接形成建库奖励，而相对标准化使更新更关注同组候选之间的差异。<br>
**原文位置**：算法1第9—12行；附录A.1，公式(6)—(7)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练采用GRPO的裁剪代理目标。阶段2中，每个词元动作的概率比由当前策略$\pi_\theta$与采样时旧策略$\pi_{\theta_{\mathrm{old}}}$之比计算，并乘以问答优势$A^{\mathrm{qa}}_{b,k,m}$；阶段1同理使用知识库优势$A^{\mathrm{kb}}_{b,k}$。概率比被裁剪到$[1-\epsilon,1+\epsilon]$附近，以限制单次更新幅度。关键耦合是阶段1没有独立的抽取奖励：其奖励完全来自阶段2答案F1的均值，因此能提高答案可达性和问答效果的三元组选择、关系表达及图连接方式会被强化。设置$\lambda=M$则平衡数量不对称的两类轨迹。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 无预设模式的原子事实知识库**

KBevo以实体级三元组$(\text{entity},\text{relation},\text{value})$作为基本单元，不依赖固定本体或人工规定的关系集合；训练奖励会推动模型保留并连接对下游问答有用的事实。知识库是持久化且可编辑的结构，推理时可按实体和关系进行定向查找。

> 直观理解：“无预设模式”意味着研究者不必事先列出所有可能关系，模型可按任务需要形成关系名称和事实结构。显式三元组还使单条事实能够被检查或替换，而不必修改模型参数或重新训练整个系统。

**2. 共享参数的双阶段策略**

知识库构建分布$\pi_\theta(\cdot\mid p^{\mathrm{kb}}(c))$与问答分布$\pi_\theta(\cdot\mid p^{\mathrm{qa}}(q),G)$使用同一组参数$\theta$。问答阶段可调用数据库工具，返回值被注入上下文，但这些外部返回的结果词元在损失中被遮蔽，不作为模型自己生成的动作训练。

> 直观理解：共享参数让模型在学习使用知识时，也更清楚应当怎样组织知识；反过来，更适于检索的知识结构又降低了推理难度。屏蔽查询返回值可避免把数据库提供的内容误当成模型自主生成的决策。

**3. 下游耦合的分层奖励**

阶段2直接使用答案F1奖励，阶段1不设置独立的抽取正确率奖励，而是接收其知识库上$M$次问答奖励的均值。两类奖励分别在局部组内转换为相对优势：前者比较同一知识库上的不同答案，后者比较同一道题的不同候选知识库。

> 直观理解：这种设计把“知识是否有用”的判断交给最终任务，而不只奖励抽取出看似正确但无法支持多跳回答的孤立事实。两层比较又分别回答了“哪个回答更好”和“哪个知识库更好”，减少两种随机性的混淆。

**训练与推理**

训练前先进行监督微调热启动，使基础模型学会三元组格式、数据库查询协议和结构化推理轨迹；原文指出直接从基础模型进行RL时，即使加入提示与格式奖励，也会出现奖励和查询使用率坍塌。随后每轮从数据集$\mathcal D$采样$B$个$(c_b,q_b,a_b^*)$，每篇文档生成$K$个候选知识库，每个知识库生成$M$条问答轨迹，以答案F1计算奖励和两级优势，再将两个阶段的轨迹合并进行一次GRPO更新。训练期间两个阶段共享并同步更新参数，所以更好的知识库帮助回答，而回答结果又反向筛选更有效的知识结构。

推理时流程与训练采样分离：对一组输入文档仅执行一次阶段1，离线生成并索引结构化知识库；此后知识库保持固定，可被多个下游问题复用。每个问题只进行一次阶段2生成及所需的嵌入检索和定向数据库查询，不再执行$K\times M$候选采样，也不需要教师模型或额外的模式归纳阶段。若外部事实变化，可直接编辑相应三元组，再由同一推理策略使用更新后的知识。

**复现信息**

知识表示的基本单位是实体级$(\text{entity},\text{relation},\text{value})$三元组，检索接口接受$(\text{entity},\text{relation})$并返回值；查询返回词元在阶段2损失中被遮蔽。监督热启动使用6千条由Gemini 2.5 Flash生成的HotpotQA轨迹并训练3个epoch，附录称约$0.4$个epoch的检查点已经足以启动后续RL。推理侧知识库按文档离线构建并持久化，单次查询只注入较短的查找结果，而非不断追加完整检索段落；原文节选未明确报告$B$、$K$、$M$、学习率或裁剪系数$\epsilon$的具体数值。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HotpotQA：多跳问答基准；训练阶段使用约7,000个样本，评测集含7,405个样本。作者还从HotpotQA生成6,000条两阶段SFT轨迹。由于训练和监督均来自该数据集，它承担域内训练与域内评测的角色。
- MuSiQue：含2,417个样本的多跳问答基准，不参与训练，用于检验模型面对不同问题组合方式时的域外泛化能力。
- 2WikiMultiHopQA：含12,576个样本的多跳问答基准，不参与训练，用于检验跨文档、多跳事实组合能力。原文还评测了单跳事实问答PopQA，但受数据集数量限制，此处优先保留三个多跳基准。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Exact Match（EM）**

主评测指标，检查模型答案在标准规范化后是否与参考答案完全一致；它衡量最终回答正确性，但不会给部分匹配计分。 （越高越好，因为完全匹配的样本比例越高，表示最终答案越准确。）

</div>
<div class="metric-item" markdown="1">

**F1结果奖励**

GRPO训练中使用的问答结果奖励，根据预测答案与参考答案之间的词项精确率和召回率计算。它为不完全匹配提供连续反馈，用于同时优化知识库构建和后续推理；原文未将其明确列为主测试指标。 （越高越好，因为预测与参考答案的重合更充分；但它在本文中主要是训练信号，不能替代EM主结果。）

</div>
<div class="metric-item" markdown="1">

**知识库结构与查询效率诊断**

包括实体数、关系数、三元组数、平均度、连通分量数、最大连通分量占比，以及重复查询率和未知查询率。前几项描述知识覆盖和图连接性，后两项描述推理策略是否反复查询或查询不到匹配项。 （覆盖量、平均度和最大连通分量占比通常越高越好；连通分量数、重复查询率和未知查询率越低越好。不过规模增大本身不等于事实更准确，必须结合三元组质量与问答结果判断。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### HotpotQA上的知识库规模：Qwen3-4B从KBevo-SFT升级到KBevo-GRPO

<div class="result-value" markdown="1">

平均每个样本的三元组数由165.7增至299.1，增加133.4，约为原来的1.81倍。

</div>

作者据此主张，问答结果奖励会促使模型保留或生成更多对后续推理有用的结构化事实。直观地说，系统不再把知识抽取当成固定预处理，而是根据“这些事实最终能否帮助答题”调整知识库。不过，该结果只证明知识库更大；单凭三元组数量不能证明新增事实全部正确，也不能直接证明主问答EM提高。

<div class="result-source" markdown="1">

来源：Table 6, Appendix C.1；列顺序为Qwen3-1.7B SFT、GRPO、Qwen3-4B SFT、GRPO

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

#Triplets 166.2 225.9 165.7 299.1

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### HotpotQA上的知识库连通性：Qwen3-4B从KBevo-SFT升级到KBevo-GRPO

<div class="result-value" markdown="1">

平均连通分量数从13.0降至7.9，同时最大连通分量占比从57.8%升至73.8%。

</div>

这说明GRPO后的知识不只是数量增加，还更集中于相互连接的图结构。对多跳问答而言，更大的连通区域意味着从一个实体沿关系找到另一实体的路径更可能存在。该诊断支持“答案可达性可能改善”的机制解释，但它不是严格因果证明：表6没有单独控制知识库大小，且其检查点与主结果不同。

<div class="result-source" markdown="1">

来源：Table 6, Appendix C.1；列顺序为Qwen3-1.7B SFT、GRPO、Qwen3-4B SFT、GRPO

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

#Components ↓ 13.1 10.3 13.0 7.9
Giant Comp. (%) ↑ 57.2 65.1 57.8 73.8

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### HotpotQA上的查询效率：Qwen3-4B从KBevo-SFT升级到KBevo-GRPO

<div class="result-value" markdown="1">

未知查询率从7.1%降至2.0%，重复查询率从7.2%降至6.3%；Qwen3-1.7B上两项指标也分别从6.6%降至2.3%、从6.3%降至2.3%。

</div>

未知率下降表示推理模型提出的$(实体,关系)$查询更常能在知识库中命中；重复率下降表示它较少反复请求已经查过的信息。作者将此视为知识库与查询策略共同适应的证据。分析上，这比单看图规模更接近“构建与推理共进化”的核心主张，但仍不能排除反向索引、知识库扩张或策略变化各自贡献了多少。

<div class="result-source" markdown="1">

来源：Table 6, Appendix C.1；列顺序为Qwen3-1.7B SFT、GRPO、Qwen3-4B SFT、GRPO

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Redundancy Rate (%) ↓ 6.3 2.3 7.2 6.3
Unknown Rate (%) ↓ 6.6 2.3 7.1 2.0

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前节选省略了知识密集型问答主结果表，因此无法验证主指标EM、各基准上的具体数值以及KBevo相对四类基线的提升。表6只能说明知识库结构和查询行为发生变化，不能替代最终问答性能证据。
- 结构分析采用较早的检索$k=1$检查点，而主问答结果采用最终$k=4$配置；作者明确警告两者的绝对问答结果不可直接比较。此外，节选未提供置信区间、方差或显著性检验，也未给出反向索引和检索参数消融的定量结果。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Direct：不访问任何外部资料，直接由模型生成答案。它用于衡量参数化记忆本身的能力，并判断外部知识访问是否确有增益。
- RAG：从文档文本块中检索相关上下文，再据此生成答案。它是与KBevo最直接的比较，因为两者使用同一批源文档，但RAG检索非结构化文本，KBevo检索抽取出的三元组。
- IRCoT：交替执行思维链推理和BM25迭代检索，并使用与其他检索方法相同的基准语料库。该比较用于判断结构化知识库相对于传统词项匹配式多轮检索是否更适合多跳推理。
- Search-R1：学习在推理过程中进行多轮非结构化文本搜索。作者因没有可用的Qwen3版本而自行复现，并匹配训练数据、训练步数和总体预算；它用于比较“联合学习结构化知识库”与“联合学习文本搜索策略”。

**实验想回答的问题**

- 在使用相同源文档的条件下，KBevo通过“结构化知识库构建—知识库检索—多步推理”的联合训练，能否比无检索、文本块检索和搜索—推理交替方法更有效地完成知识密集型问答，并从HotpotQA泛化到域外数据集？
- 基于问答结果奖励的GRPO共进化，是否会把知识库改善为规模更大、连接更紧密且更容易被推理策略查询的结构，而不只是提高语言模型的最终作答能力？

**实验实现**

作者以Qwen3-1.7B和Qwen3-4B为基础模型，先用Gemini-2.5-Flash生成的6,000条HotpotQA两阶段轨迹进行3轮SFT：第一阶段从支持文本抽取$(实体,关系,值)$三元组，第二阶段通过数据库查询完成问答。随后在7,000个HotpotQA样本上执行500步GRPO，并使用答案F1作为结果奖励。每道问题采样$K=4$个候选知识库，每个知识库生成$M=8$条问答轨迹，因而共有$N=32$条问答轨迹和36次总 rollout；该设计使某个知识库若持续支持正确回答，就能反向获得更高训练信号。

检索时，系统用all-MiniLM-L6-v2编码$(实体,关系)$对，通过余弦相似度返回阈值0.6以上的前$k=4$项，否则返回unknown。数据库还为$(实体,关系,值)$加入反向条目$(值,关系,实体)$。公平性方面，所有检索方法使用同一批基准源文档：文本基线索引文档块，KBevo索引从同一文档抽取的三元组。需要注意，表6及附录C使用的是较早的$k=1$检查点，而主问答结果使用最终$k=4$配置，因此两组绝对结果不可直接横向比较。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 反向索引：为每个$(实体,关系,值)$额外加入$(值,关系,实体)$ | 作者报告该设计改善初始SFT表现、强化学习期间的学习能力以及最终表现，但所给节选没有提供移除反向索引后的具体数值。 | 该设计让原本只能从实体查值的关系也能从值反查实体，理论上可减少多跳推理中的方向性障碍。不过，由于没有成对数值、评价指标或对应表格，这只能视为作者的定性消融结论，无法判断改善幅度及其是否稳定。 | Appendix B.1.2, Database and Retrieval Implementation<br><span class="experiment-evidence">We find that this improves initial SFT performance, the learning ability of the model during reinforcement learning, and the final performance of the model.</span> |
| 检索配置选择：相似度阈值0.6与前$k=4$返回项 | 作者称该组合在SFT训练后取得最高表现，但原文节选未报告与其他阈值或$k$值比较的数值。附录分析使用早期$k=1$检查点，主结果则使用$k=4$。 | 该比较意在确定一次返回多少条三元组以及多相似才算有效命中。较大的$k$可能提高召回率，也可能引入噪声；阈值则在漏检与误检之间折中。由于缺少完整搜索表，而且$k=1$与$k=4$对应不同检查点，不能把附录与主表差异直接解释为$k$的因果效果。 | Appendix B.1.2, Database and Retrieval Implementation<br><span class="experiment-evidence">We found that this combination of threshold and top-k yielded the highest performance after SFT training.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Jointly optimizes structured knowledge-base construction and compositional reasoning for knowledge-intensive question answering.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`437a6d50176dfe6e537e3a829ead961d31ed9332185e958ce6dd277b49bea758`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
