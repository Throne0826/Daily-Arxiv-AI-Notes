---
title: "[论文解读] TrAC: Trace-Conditioned Answer Consistency for Efficient Uncertainty Quantification in LLMs"
description: "[arXiv 2608.00422][LLM Reasoning] TrAC通过从一条已完成的推理轨迹中低成本地重新引出短答案，并结合原生成过程中的词元置信度信息，估计该回答正确的可能性。"
arxiv_id: "2608.00422"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:04:39.051669+00:00"
source_sha256: "8065879538b751d3e5683b9fe4548c57f9f06974b81e615414f1308de642d14c"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "不确定性量化"
  - "数学推理"
  - "推理轨迹"
  - "答案重引出"
  - "选择性预测"
  - "自洽性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.00422</p>

# TrAC: Trace-Conditioned Answer Consistency for Efficient Uncertainty Quantification in LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Dahai Yu, Lin Jiang, Rongchao Xu, Guang Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Florida State University Tallahassee, Florida USA；Florida State University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.00422v1) · [PDF 下载](https://arxiv.org/pdf/2608.00422v1) · **关键词** 大语言模型, 不确定性量化, 数学推理, 推理轨迹, 答案重引出, 选择性预测, 自洽性<br>
**代码**: [https://anonymous.4open.science/r/TrAC](https://anonymous.4open.science/r/TrAC)

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

TrAC通过从一条已完成的推理轨迹中低成本地重新引出短答案，并结合原生成过程中的词元置信度信息，估计该回答正确的可能性。

**不用术语来说**：大语言模型即使写出流畅、看似合理的推理过程，最终答案仍可能错误，因此部署系统需要判断哪些回答可信、哪些应当拒答、交由人工复核或追加计算。困难在于，这种判断最好只利用当前的一次完整回答完成，不能依赖标准答案、额外裁判模型或多次昂贵的完整推理。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出“轨迹条件答案一致性”这一主动不确定性信号：在模型完成推理后附加固定提示，让同一冻结模型依据完整轨迹重新生成一个短答案，以检验原轨迹是否仍稳定支持原答案。
- 提出正确性监督的TrAC框架，将主动的前缀条件引出表示PCE与被动的轨迹不确定性剖面TUP结合，输出回答正确性分数；前者描述重新引出答案与原答案的一致程度及概率支持，后者概括原始生成过程中词元级不确定性的变化。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的响应级不确定性量化研究，关注模型完成一条数学推理响应后，如何估计该响应最终答案正确的可能性。数学推理虽然可以通过确定性的答案核验获得离线正确性标签，但语言流畅、推导完整并不保证结论正确，因此部署系统需要用置信分数对响应排序，以支持选择性预测，即在低置信度时拒答、转交人工复核或追加计算。现有证据主要来自三类途径：读取单条响应已有的词元概率等被动信号；生成多条完整推理并比较答案共识；从未完成的推理前缀反复引出答案。本文研究的特定设置是只依赖一条已经完成的推理轨迹，在不调用独立裁判模型、不使用参考答案且不再生成完整推理轨迹的条件下，判断原响应是否可靠。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**响应级不确定性量化**

为模型生成的整个响应计算一个反映其可能正确或错误程度的分数，而不是只判断某个词元是否可信。该分数主要用于排序和决策，例如优先接受高置信响应并复核低置信响应。

</div>
<div class="concept-item" markdown="1">

**推理轨迹**

模型从题目出发生成的中间推导过程及最终答案序列。本文强调，即使轨迹表面连贯，其中的错误仍可能传播到最终答案。

</div>
<div class="concept-item" markdown="1">

**答案重引出**

在完整推理轨迹后附加固定提示，让同一冻结模型仅再次生成一个简短答案。它不要求模型直接评价自己是否正确，而是检验原轨迹在被重新读取后能否稳定支持原答案。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道可验证的数学推理题，以及同一大语言模型已生成的一条完整响应，其中包含推理轨迹和返回答案；推理完成时可取得原生成过程中的词元级概率信号。系统需要输出一个响应正确性分数，使正确响应在总体上排在错误响应之前，并可据此决定接受、拒答、人工复核或追加采样。研究假设最终答案可通过确定性规则在离线阶段核验，从而为轻量预测头提供正确或错误的监督标签；但推理时不允许访问参考答案，也不调用额外裁判模型。TrAC所处的计算约束是仅保留一条完整推理轨迹，随后通过缓存该轨迹并生成一个短答案探针获得主动证据，同时复用原轨迹的词元不确定性获得被动证据；它要估计的是单个已完成响应的正确性，而不是寻找提前终止推理的位置。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Self-consistency（Wang et al., 2023）**: 该方法从多条独立生成的完整推理轨迹中提取最终答案，以最高频答案的票数占比表示置信度，因而能够反映跨轨迹分歧。它需要多次完整生成，而且当所有样本答案一致时会失去进一步区分能力，无法区分稳定正确与被模型反复生成的系统性错误；TrAC则用一次短答案重引出来测量单条完整轨迹内部对原答案的支持。
- **P(True)（Kadavath et al., 2022）**: P(True)让模型显式判断某个候选答案是否正确，属于自我验证式置信度信号。TrAC不要求模型作正确性判断，而是让模型在相同完整轨迹条件下重新给出答案，再利用答案是否一致及其概率支持估计可靠性，因此作者将其视为与显式自我验证不同的证据来源。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在可验证的数学推理任务中，答案可在离线阶段确定对错，但推理文本的流畅和自信并不能保证结论正确。实际系统因而需要一个回答级不确定性分数，将较可靠的输出排在可能错误的输出之前，以支持选择性预测、拒答、人工复核以及决定何时投入额外采样计算。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单轨迹置信度方法**：被动方法直接汇总一次完整回答生成时已有的词元概率或置信度；主动前缀方法则从尚未完成的推理前缀引出答案，观察答案何时稳定或偏好如何转变，主要用于提前停止。
- **多轨迹采样与投票方法**：从同一问题独立生成多条完整推理轨迹，再依据最终答案之间的共识或投票比例估计可靠性，例如八样本自一致性通过答案出现频率衡量置信度。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单轨迹被动信号没有主动检验已完成的推理上下文是否继续支持其最终答案，而既有主动前缀方法关注部分轨迹上的答案稳定或提前停止，并未直接评估一条完整回答的正确性；因此，词元置信度或早期稳定并不等价于完整轨迹对结论的稳健支持。
- 多轨迹投票需要生成若干条完整推理，增加推理延迟和计算成本；当所有样本答案一致时，共识分数还会饱和，难以继续区分这些表面上同样一致、实际错误风险不同的回答。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种面向已完成推理轨迹的主动答案级探测机制：它应当在不调用独立裁判、不使用参考答案、也不再生成另一条完整推理的条件下，重新询问模型结论，并把开放形式、长度可变的答案转换为同时保留答案身份与概率支持强度的固定表示。

</div>
<div markdown="1"><span>核心问题</span>

仅依据一条已完成的推理轨迹及一次很短的条件答案探测，能否构造有效的回答正确性评分；并且，这种重新引出信号是否提供了超出原始词元置信度、显式自我验证概率和跨样本共识的独立信息？

</div>
<div markdown="1"><span>作者直觉</span>

一条真正支持其结论的推理轨迹，在模型重新阅读后应当像一份结论明确的解题记录：模型会高概率地再次给出同一答案。若原结论只是偶然产生或推理内部不稳，重新引出的答案更可能改变，或者即使相同也只获得较弱的概率支持。因此，“是否复现”与“多强地复现”可以揭示单看流畅文本或原答案置信度时不易发现的错误风险。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TrAC把一次已完成的推理响应视为待评估对象：冻结语言模型先对问题$x$生成推理正文$r$和原始答案$a$，即$y=(r,a)$；随后，一条主动分支PCE在完全相同的$x,r$上下文后追加固定提示，仅重新生成一个短答案$\tilde{a}$，提取它与$a$的一致性及生成概率；一条被动分支TUP直接汇总原始响应各位置的词元对数概率和熵。两类特征经训练折内标准化后输入带$L_2$正则的逻辑回归头，输出响应正确性分数$u_{\mathrm{TrAC}}\in[0,1]$。该分数用于跨响应排序，而不是改写答案；部署时不需要参考答案、验证器、过程标签、隐藏状态编码器或LLM裁判。
直观地说，TUP检查模型在“说出整段推理时是否一路犹豫”，PCE则在模型已经看完自己的推理后追问一次“所以最终答案是什么”。如果短答案仍与原答案一致且概率支持强，同时原推理的词元不确定性轨迹稳定，则预测头倾向于给出更高可靠性分数。默认方案只付出一条完整推理加一个可复用缓存的短答案后缀；若系统本来已有$K$条完整轨迹，还可用CF把TrAC的单轨迹证据与跨轨迹投票统计结合。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成并记录主响应

模型生成完整响应$y=(r,a)=(y_1,\ldots,y_T)$，同时保存每个已选词元的对数概率及预测分布的top-$k$信息；训练阶段再用确定性验证器$V(a,a^*)$构造标签$z\in\{0,1\}$。

<div class="method-step__io" markdown="1">

**输入**：推理问题$x$与冻结语言模型$p_\theta$。<br>
**输出**：推理正文$r$、原始答案$a$、原始生成的逐词元统计，以及仅在离线校准时使用的正确性标签$z$。

</div>

**直观理解**：先保留模型实际作答及其生成过程中的置信信号，再判断这一次回答是否可靠。标准答案只负责制作训练标签，不会成为部署输入。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行PCE短答案重引出

在$x,r$后追加模型兼容的思考结束标记与固定提示“<The final answer is>”，利用前缀缓存进行贪心的答案后缀解码，得到$\tilde{a}=(v_1,\ldots,v_L)$及各答案词元的对数概率。随后确定性归一化$a$与$\tilde{a}$，计算一致性$e=\mathbb{I}[\tilde{a}\equiv a]$、平均对数似然、最小词元对数似然、前至多两个词元的平均对数似然和首词元置信度。

<div class="method-step__io" markdown="1">

**输入**：原问题$x$、已完成的推理正文$r$和原始答案$a$。<br>
**输出**：五维主动特征$\phi_A=[e,\ell,\ell_{\min},\ell_{\mathrm{head}},c_1]$及可审计的重引出记录。

</div>

**直观理解**：这不是重新做一道题，而是让模型依据刚才那段既定推理再报一次答案。答案是否改变反映结论稳定性，答案概率则区分“勉强一致”和“有力一致”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造TUP不确定性轨迹

对每个位置$t$计算已选词元对数概率$\lambda_t$和在top-$k$候选上重归一化的熵$\eta_t$；把不同长度的序列按相对位置划入$J$个区间并分别求均值，再加入全局均值、极值、标准差、线性趋势、拟合优度、尾部均值和低概率词元比例。

<div class="method-step__io" markdown="1">

**输入**：主响应$y$及生成时已保存的逐词元概率统计。<br>
**输出**：固定维度的被动特征$\phi_P=[\mathbf{b}(\lambda);\mathbf{b}(\eta);\mathbf{s}]$。

</div>

**直观理解**：分箱相当于把长短不同的推理都压缩成“开头、中段、结尾”的置信曲线；附加统计量则保留最低谷、整体波动和结尾是否失稳等信息。该分支完全复用主生成数据，不增加解码。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 标准化并融合评分

仅用当前训练折估计标准化参数和缺失值规则，再以正则化二元交叉熵拟合逻辑回归参数$\mathbf{w},b$；推理时将保存的预处理应用于$[\phi_A;\phi_P]$并计算$u_{\mathrm{TrAC}}$。

<div class="method-step__io" markdown="1">

**输入**：主动特征$\phi_A$、被动特征$\phi_P$以及训练阶段的标签$z$。<br>
**输出**：单个响应的正确性或可靠性分数$u_{\mathrm{TrAC}}\in[0,1]$。

</div>

**直观理解**：轻量预测头学习哪些迹象更常出现在正确回答中，并把它们合成一个可排序分数。限制分类器容量有助于把效果归因于PCE和TUP信号，而不是复杂分类网络。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### TrAC统一正确性评分

$$
u_{\mathrm{TrAC}}=\sigma\!\left(\mathbf{w}^{\top}[\phi_A;\phi_P]+b\right)
$$

**符号说明**

- $u_{\mathrm{TrAC}}$：TrAC对当前响应正确性或可靠性的标量估计，取值在零到一之间
- $\sigma$：Sigmoid函数，把线性得分映射到零到一
- $\mathbf{w}$：由带正确性标签的校准数据学习得到的特征权重向量
- $\phi_A$：PCE主动表示，包含答案一致性和重引出答案的概率支持
- $\phi_P$：TUP被动表示，包含主响应的分箱不确定性轨迹和辅助统计
- $b$：逻辑回归的偏置项
- $[\phi_A;\phi_P]$：主动与被动特征的向量拼接

<div class="equation-explanation" markdown="1">

**直观理解**：该式是方法的最终融合接口：预测头为不同不确定性证据分配权重，再输出一个响应级分数。分数主要服务于正确与错误响应的排序、拒答和资源分配；它并不重新生成或修改原答案。<br>
**原文位置**：式（18），第3.3.1节 Representation Fusion

</div>

</div>

<div class="equation-block" markdown="1">

#### 正确性监督的正则化校准目标

$$
\min_{\mathbf{w},b}\frac{1}{N}\sum_{i=1}^{N}\left[-z_i\log u_i-(1-z_i)\log(1-u_i)\right]+\lambda\lVert\mathbf{w}\rVert_2^2
$$

**符号说明**

- $N$：校准训练集中的响应数量
- $z_i$：第i个主响应的二元正确性标签，由确定性验证器离线产生
- $u_i$：预测头对第i个响应输出的正确性分数
- $\mathbf{w}$：待优化的逻辑回归权重
- $b$：待优化的偏置
- $\lambda$：控制L2权重惩罚强度的正则化系数
- $\lVert\mathbf{w}\rVert_2^2$：权重向量的平方L2范数，用于限制模型复杂度

<div class="equation-explanation" markdown="1">

**直观理解**：二元交叉熵要求正确响应获得较高$u_i$、错误响应获得较低$u_i$；$L_2$项抑制过大的权重以减少过拟合。参考答案只用于生成$z_i$并拟合该头，部署时计算$u_i$不再需要参考答案。<br>
**原文位置**：式（19），第3.3.2节 Correctness-Supervised Calibration

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练对象不是语言模型$p_\theta$，而是响应级校准器。对校准集$\mathcal{D}=\{(\phi_i,z_i)\}_{i=1}^N$，先从冻结模型的主响应和PCE记录构造$\phi_i$，再仅用训练折计算连续特征的均值与尺度、设置显式缺失指示，并最小化带$L_2$惩罚的二元交叉熵；主动PCE、被动TUP、统一TrAC及CF变体使用相同拟合流程。这样，训练直接优化“预测当前响应是否正确”，而AUROC所关心的正确响应高于错误响应的排序能力则由连续输出$u_i$体现。
确定性验证器$V$和参考答案$a^*$只在离线阶段把原始答案$a$映射为$z=V(a,a^*)$，不参与特征计算或在线评分。逻辑回归容量受限，使实验中的性能差异主要反映不同不确定性观察是否有效；但这里的$u_i$仍是监督校准所得的可靠性分数，不能理解为语言模型自身未经校准的真实正确概率。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Prefix-Conditioned Elicitation（PCE）**

PCE定义固定重引出算子$(\tilde{a},\mathbf{c})=Q_\theta(x,r)$，其中$\mathbf{c}$保存$\tilde{a}$各词元的对数概率。它将答案等价指示量$e$与四个概率支持统计拼成$\phi_A$：$\ell$按长度平均，$\ell_{\min}$捕捉最弱词元，$\ell_{\mathrm{head}}$关注答案开头至多两个词元，$c_1$在完整答案解析失败时仍可使用。

> 直观理解：仅看原答案概率可能出现“模型很自信地给出另一个答案”，仅看一致性又无法区分强支持与弱支持。PCE同时记录答案身份和支持强度，专门探测已完成推理对其结论的内部支持，而不是要求模型直接评价自己是否正确。

**2. Trace Uncertainty Profile（TUP）**

TUP从主生成中提取$\lambda_t=\log p_\theta(y_t\mid x,y_{<t})$与top-$k$重归一化熵$\eta_t$。相对位置分箱保留粗粒度的时间形状，辅助向量$\mathbf{s}$补充全局、趋势、尾部和低置信词元统计，从而把任意长度响应映射为固定维度$\phi_P\in\mathbb{R}^{d_P}$。

> 直观理解：两个回答可能具有相同平均置信度，但一个始终稳定，另一个在关键中段或结尾突然犹豫；单一均值无法区分它们。TUP保留这种随推理位置变化的模式，并且不需要第二次完整生成。

**3. 轻量校准头与Consensus Fusion（CF）**

默认头对拼接表示$[\phi_A;\phi_P]$进行正则化逻辑回归；可选CF头再加入$q_K$和$h_K$。所有变体共享训练折内标准化、缺失指示和拟合流程，语言模型参数$p_\theta$始终冻结。

> 直观理解：统一的简单预测头使主动、被动和共识特征能够公平比较，也减少数据泄漏及高容量分类器掩盖信号质量的风险。CF的目的不是用投票替代TrAC，而是检验重引出是否能提供投票中没有的信息。

**训练与推理**

离线准备与训练：每个问题只需生成并保存一次主响应，同时保留逐词元对数概率和top-$k$熵所需信息；PCE利用主推理缓存生成短答案，并保存不可变的$\tilde{a}$、逐词元概率及一致性所需原始字段，而不只保存最终特征。主答案存储后，验证器才依据$a^*$产生$z$。每个训练折独立确定答案归一化后的特征、缺失值约定和标准化参数，拟合正则化逻辑回归，并将缺失规则、标准化器与预测头共同保存；测试折统计不得进入预处理。
在线推理：冻结模型先输出$x$对应的$r,a$及词元统计，TUP无需额外解码即可生成$\phi_P$；PCE复用$x,r$的缓存，仅贪心生成短答案$\tilde{a}$，再通过确定性答案归一化和等价检查构造$\phi_A$。保存的预处理器和头输出$u_{\mathrm{TrAC}}$，全程不访问$a^*$、$V$或$z$。分数可用于低分拒答、人工复核排序或为低分响应分配额外采样；若已有$K$条完整轨迹，则额外计算$q_K,h_K$并输出$u_{\mathrm{CF}}$。

**复现信息**

公平解释成本时，应把默认TrAC计为“一次完整主生成加一次短的缓存答案探测”，而不能计为两条完整推理；TUP本身没有额外解码。PCE使用固定且跨样本不变的提示、模型兼容的思考结束标记和贪心解码，主推理正文与冻结模型参数均不修改。答案一致性使用确定性归一化与等价规则，但不接触参考答案；保存PCE原始记录使研究者可以调整解析、归一化或特征定义而不重新生成昂贵主轨迹。
复现时还需固定TUP的相对位置区间数$J$、熵候选数$k$、尾部窗口$W$和低概率阈值$\tau$，因为它们决定$\phi_P$的维度与统计口径；本节仅说明这些值在所有样本间固定，具体数值位于原文附录C.2，当前节选未提供。缺失答案字段必须带显式缺失指示，连续特征只能按训练折标准化。CF使用与SC@$K$相同的$K$次完整生成，另加一个短缓存探测，因此其结论应解释为“在已有多轨迹预算上增加轨迹内证据”，不能与默认单轨迹TrAC混为同一部署设置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 五个数学推理基准：GSM8K、MATH500、Minerva、OlympiadBench 和 AIME。论文将六种模型与五个数据集组成的全部 $30$ 个“模型—数据集”对纳入数学任务宏平均；摘录未给出各数据集的样本规模及具体训练、验证、测试数量。
- BIG-Bench Hard：用于检验 TrAC 能否从数学推理推广到更广泛的高难度组合推理任务。摘录仅报告该数据集被纳入非数学评估，未明确给出样本规模、子任务选择或划分。
- GPQA-Diamond：面向高难度、专家级科学问答，用来检验方法在非数学知识推理上的适用性。摘录未明确报告样本规模与划分；附录只给出定性结论，即数学到非数学的迁移未胜过最佳迁移基线。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**AUROC**

衡量评分将正确回答排在错误回答之前的概率，并将同分情况按一半计入。它评价整体的两两正确性排序能力，但不直接表示某个固定阈值下的准确率或概率校准质量。 （越高越好；较高值表示正确回答通常获得更高的置信评分。）

</div>
<div class="metric-item" markdown="1">

**AURC**

先按置信评分从高到低排列回答，再计算各覆盖率下保留回答的错误率，最后对风险—覆盖率曲线求面积。它检验系统在逐步拒答或转交人工时，能否优先剔除错误回答。 （越低越好；较低值表示错误回答更早被拒绝，在不同覆盖率下保留下来的错误更少。）

</div>
<div class="metric-item" markdown="1">

**风险@覆盖率及 excess AURC**

风险@覆盖率是在指定覆盖比例下最有信心的一组回答中的错误率；excess AURC 则按基础错误率归一化选择性风险，便于比较原始准确率不同的模型—数据集对。摘录说明这些指标出现在总体结果表中，但没有提供相应数值。 （均越低越好，因为目标是在保留给定比例回答时减少错误，并降低相对于基础错误率的额外选择性风险。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### TrAC 与八样本自洽性 SC@8 在五个数学推理基准、三个模型家族上的宏平均比较

<div class="result-value" markdown="1">

作者报告：TrAC 相对 SC@8 的宏平均 AUROC 提高 $1.8\%$，AURC 降低 $3.4\%$；同时，TrAC 只生成一条完整推理轨迹，并基于缓存执行一次短答案探测，而 SC@8 需要八条独立完整轨迹。

</div>

这说明在该实验协议下，完成轨迹后的短答案重引导可以用明显少于八次完整生成的解码量，取得更好的正确性排序和选择性拒答表现。该结果支持“信号效率更高”，但摘录没有给出绝对 AUROC、绝对 AURC、统计显著性或精确延迟，因此不能仅据这些相对百分比判断实际部署收益大小。

<div class="result-source" markdown="1">

来源：摘要；总体实验对应第 4 节与表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across five mathematical reasoning benchmarks and three LLM families, TrAC improves macro AUROC by 1.8% and reduces AURC by 3.4% relative to eight-sample self-consistency, while using one complete reasoning trace and a short cached answer probe.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 已有八个完整采样回答时，将共识统计与答案重引导融合

<div class="result-value" markdown="1">

作者报告：在八个样本已经可用的条件下，将重引导信号加入样本共识，使宏平均 AUROC 进一步提高 $4.3\%$、AURC 降低 $8.3\%$，且无需再生成完整推理轨迹。按附录表 11 的 AUROC 统计，融合方法相对 SC@8 在全部 $30$ 个数学模型—数据集对上的宏差值为 $+0.038$。

</div>

这表明重引导与跨样本投票不是完全重复的信息：即便已经支付八次完整采样的成本，回到某条完成轨迹再询问短答案仍可能改善错误识别。该结果不意味着每个数据集和模型都获益；表 11 明确包含少数负差值，例如 MATH500 上的 Phi-4-r 和 Qwen3-4B。

<div class="result-source" markdown="1">

来源：摘要；逐模型—数据集 AUROC 结果见附录表 11

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

When eight samples are already available, augmenting sample consensus with re-elicitation further improves macro AUROC by 4.3% and reduces AURC by 8.3%, without additional full-trace generation.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 仅考察 SC@8 八次采样答案完全一致的高共识子集

<div class="result-value" markdown="1">

在投票一致率为 $1.000$ 的子集中，共有 $7485$ 个样本，其中仍有 $243$ 个错误；SC 的 AUROC 为 $0.500$，而 PCE 的 AUROC 为 $0.839$。

</div>

完全一致时，所有样本的投票比例相同，SC 无法继续区分哪些共识答案是错的，所以 AUROC 退化到随机排序水平；PCE 仍可利用完成轨迹条件下的短答案及其概率支持来排序这些错误。这直接展示了“多数一致不等于正确”的共识盲区，但它只证明 PCE 在该筛选子集上有额外分辨率，不证明其评分已经良好校准。

<div class="result-source" markdown="1">

来源：附录表 10，列依次为 Vote≥、Pairs、n、Wrong、SC、PCE

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

1.000 30 7,485 243 .500 .839

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

- 单轨迹概率基线，包括平均 token 对数概率、Self-certainty 和 DeepConf-bottom。它们只读取原始生成中的 token 置信度，不执行额外完整采样，因此用于判断 TrAC 的收益是否超出常规被动置信度汇总。
- P(True) 与 SelfDoubt：前者通过自我验证询问答案为真的概率，后者使用模型口头表达的不确定性。它们同样主动询问模型，但没有以“完成后的推理轨迹支持原答案到何种程度”为核心表示，因此是检验轨迹条件化重引导是否必要的对照。
- SelfCheckGPT@8 与八样本自洽性 SC@8：从八个独立完整回答之间的一致程度估计不确定性。该组基线代表高生成成本的采样式方法，也是判断 TrAC 能否用“一条完整轨迹加一次短答案探测”替代多轨迹采样的关键参照。
- Supervised Consensus@8：汇总投票比例、答案熵、投票间隔、轨迹对数概率、TUP 特征和答案似然，并使用与 TrAC 相同的逻辑回归头和正确性监督。它控制了监督方式与分类器容量，用来判断融合收益是否仅来自更丰富的投票统计，而非答案重引导信号。

**实验想回答的问题**

- 在正确性排序与选择性预测中，TrAC 相比单轨迹置信度方法和需要八次完整采样的方法是否更有效，并且能否以更低的生成成本取得这种优势？
- 答案重引导信号是否真正依赖已完成的推理轨迹、能否弥补采样共识在高一致性样本上的盲区，以及该信号对随机种子、轨迹长度、答案泄漏和跨数据集迁移是否稳健？

**实验实现**

实验覆盖 Qwen3-4B、Qwen3-8B、Qwen3-14B、Qwen3.5-9B、Phi-4-reasoning 和 Ministral-3-14B-Reasoning，共三个模型家族、六种配置。正确性标签由确定性验证器离线生成。所有学习型估计器采用五次随机打乱的五折划分，按问题隔离以避免同一问题跨折泄漏；域内分数全部来自折外预测。各方法共享逻辑回归头、数据折、特征标准化、缓存生成结果和标签，从而尽量把差异限定在不确定性表示本身。总体结果对模型—数据集对等权平均，置信区间使用 $2000$ 次“模型—数据集对等权”的分层 bootstrap。相对延迟在 Qwen3-8B 上测量，但所给摘录没有列出具体延迟数值。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 控制轨迹长度和粗粒度难度代理：在对数概率、熵和长度特征上加入 active stability | 在表 13 汇总的 $12$ 个模型—数据集组合上，宏平均 AUROC 从 $0.844$ 提高到 $0.903$，差值为 $+0.059$；长度分层后的 AUROC 为 $0.737$，稳定性与长度的相关系数为 $-0.473$。 | 该控制检验 active stability 是否只是“较短轨迹通常更容易、更可能正确”的替代指标。加入 stability 后仍有 $0.059$ 的宏平均 AUROC 增益，说明它包含超出这些粗粒度长度与概率特征的信息；但作者明确承认，这不能排除所有潜在的题目难度因素。 | 附录表 13，列依次为 LP+entropy+length、+stability、Δ、Within-length、r(stability,length)<br><span class="experiment-evidence">Macro .844 .903 +.059 .737 −.473</span> |
| 答案泄漏控制：仅保留推理正文中没有出现字符串或数值等价最终答案的轨迹 | 在答案未写入轨迹正文的子集上，覆盖 $30$ 个模型—数据集对，PCE 的 AUROC 为 $0.804$，完整 TrAC 的 AUROC 为 $0.859$；相比之下，答案已出现时二者分别为 $0.851$ 和 $0.912$。 | 该消融隔离了重引导是否仅在复制轨迹中已经出现的最终答案。答案未出现时两种方法仍明显高于随机排序的 $0.5$，说明信号不能完全归因于字符串复制；但性能低于“答案已出现”子集，表明显式答案痕迹确实会增强信号，而且两个子集可能还存在难度差异。 | 附录表 14，列依次为 Subset、Pairs、PCE、TrAC<br><span class="experiment-evidence">Answer not stated in trace 30 .804 .859</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过对完整推理轨迹重新引出答案并融合轨迹不确定性，估计数学推理回答的正确性。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`8065879538b751d3e5683b9fe4548c57f9f06974b81e615414f1308de642d14c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
