---
title: "[论文解读] Agentic Graph Token Reasoning"
description: "[arXiv 2608.00542][LLM Agent] 本文提出智能体式图令牌推理（AGT），使语言模型在解题过程中按需选择图视图、调用图编码器生成连续令牌，并依据已获得的证据逐步决定下一次查询或输出答案。"
arxiv_id: "2608.00542"
announcement_date: "2026-08-04"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:04:25.308250+00:00"
source_sha256: "22ccba76d65a9c1bd80a2aac5827a097fa20220dfed135e4b4537050ccc97d8b"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "LLM 其他"
  - "文本属性图"
  - "大语言模型"
  - "图神经网络"
  - "图令牌"
  - "图视图"
  - "智能体推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.00542</p>

# Agentic Graph Token Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Zhuoyi Peng, Yi Yang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The Hong Kong University of Science and Technology</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.00542v1) · [PDF 下载](https://arxiv.org/pdf/2608.00542v1) · **关键词** 文本属性图, 大语言模型, 图神经网络, 图令牌, 图视图, 智能体推理<br>


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

本文提出智能体式图令牌推理（AGT），使语言模型在解题过程中按需选择图视图、调用图编码器生成连续令牌，并依据已获得的证据逐步决定下一次查询或输出答案。

**不用术语来说**：面对论文引用网、商品共购网或蛋白质关系网，回答一个问题所需的信息范围通常无法预先确定：有时只需查看目标节点自身，有时必须继续检查邻居、局部群落或远处的相似节点。现有方法却在看到具体问题之前就固定读取一块图信息，此后不能补充或调整证据，因而可能漏掉关键关系，也可能读入过多无关内容。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出AGT框架，把图令牌化从一次性的输入预处理改造成可反复调用的推理操作：模型每一步选择图视图的范围与粒度，图编码器按需生成固定长度的图令牌块，并将其插入当前上下文，直至模型决定回答。
- 提出针对图令牌智能体的三阶段训练思路，分别训练模型读取不同视图产生的图令牌、通过一致性约束减少对脆弱线索的依赖，并利用图证据与节点文本是否一致构造偏好信号，以缓解模型忽略图令牌的问题。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究文本属性图上的大语言模型推理。此类图同时包含关系结构与节点文本，例如论文及其摘要构成的引文网络、商品及其描述构成的共购网络；任务答案可能取决于目标自身属性、邻居信息和更大范围的拓扑结构。由于大语言模型主要处理语言序列，现有图语言模型通常先用图神经网络把某个图视图压缩为固定长度的连续“图令牌”，再将其与问题一同输入语言模型。论文关注的核心区别不是是否使用图令牌，而是何时以及如何选择图视图：传统方案在看到具体问题前固定选择一次，本文则把图视图选择与令牌生成纳入逐步推理过程。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**文本属性图**

文本属性图同时表示对象之间的边和每个节点携带的文本，其中结构证据与语义证据都可能影响预测。本文将其记为 $\mathcal{G}=(\mathcal{V},\mathcal{E},\mathcal{T})$。

</div>
<div class="concept-item" markdown="1">

**图视图**

图视图 $G^V$ 是从完整图中选出的待处理区域，可以是单个节点、目标的 $k$ 跳邻域、语义相似节点集合、某个簇，或完整图。不同视图对应不同证据范围，范围过小可能遗漏信息，过大则可能稀释有效信号。

</div>
<div class="concept-item" markdown="1">

**图令牌**

图神经网络 $f^{\mathrm{GNN}}$ 将任意大小的图视图压缩为固定长度的连续向量块 $\mathbf{Z}$，并使其位于大语言模型可读取的嵌入空间。通俗地说，它把节点文本与连接结构浓缩成少量非自然语言令牌，使语言模型无需把整张子图展开成文本。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定文本属性图 $\mathcal{G}=(\mathcal{V},\mathcal{E},\mathcal{T})$ 和关于图中对象的问题 $Q$，问题对象可以是节点、节点对或其他由图定义的对象；其真实标签为 $y\in\mathcal{Y}$，模型需要输出答案 $A\in\mathcal{Y}$。推理时允许从完整图中按需取得目标节点文本、邻居文本及周围结构：图编码器依据所选视图 $G^V$ 产生固定长度令牌块 $\mathbf{Z}=f^{\mathrm{GNN}}(G^V)$，大语言模型读取问题与这些令牌后形成答案。论文所对照的传统设置只预先编码一个固定视图，并以 $A=f^{\mathrm{LLM}}(Q,\mathbf{Z})$ 单次作答；本文的目标设置则允许模型在生成过程中多轮选择证据范围与粒度，使实际读取的图令牌依赖此前的推理轨迹，并在证据充分时终止。该设置假定节点带有可用文本、图视图可由图编码器访问，且任务标签属于预先定义的答案空间 $\mathcal{Y}$。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{G}=(\mathcal{V},\mathcal{E},\mathcal{T})$**

文本属性图；$\mathcal{V}$ 为节点集合，$\mathcal{E}$ 为边集合，$\mathcal{T}=\{t_v\mid v\in\mathcal{V}\}$ 为节点文本集合。

</div>
<div class="notation-item" markdown="1">

**$G^V$**

从完整图中选择的图视图，即本次交给图编码器处理的节点与结构范围。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{Z}=f^{\mathrm{GNN}}(G^V)$**

图神经网络将图视图编码成位于语言模型嵌入空间中的固定长度连续令牌块。

</div>
<div class="notation-item" markdown="1">

**$Q,\ y,\ A\in\mathcal{Y}$**

$Q$ 是任务问题，$y$ 是真实标签，$A$ 是模型输出，$\mathcal{Y}$ 是答案或标签空间。

</div>

</div>

**直接相关的工作**

- **LLaGA**: 论文将其列为已有图令牌方法的代表：先对目标附近的预定义图视图进行编码，再让语言模型结合问题读取固定令牌块。它代表本文试图突破的静态、单次图令牌范式之一。
- **GOFA**: 论文同样将其归入使用图编码器压缩图视图、供语言模型读取的相关方法。与本文问题设置的关键差异是，既有方案的视图通常在问题驱动的推理开始前确定，之后不会随中间证据动态修订。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大量科学与工业数据同时具有关系结构和丰富文本，例如论文及其摘要构成引用网络、商品及其描述构成共购网络。语言模型擅长处理文本，却不能天然读取图的拓扑关系；实际任务还要求模型针对不同问题定位不同层次的证据，例如目标节点属性、交易伙伴、周边群落或语义相似节点。因此，系统不仅要把图转换成语言模型可处理的表示，还要能根据当前问题和推理进度动态决定接下来查看图的哪一部分。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **静态图令牌方法（如LLaGA、TEA-GLM、GraphGPT、GraphTranslator和GOFA）**：这类方法先用图编码器处理一个预定义图视图，例如目标节点的$k$跳邻域、某个簇或全图，再将其中的节点属性与拓扑压缩为固定长度的连续图令牌块；语言模型随后把该令牌块与问题一起读入，并在单次前向计算中生成答案。
- **通用智能体推理**：语言模型不只依据初始提示直接作答，而是在多轮过程中判断当前缺少什么信息、执行获取信息的动作，并根据新增证据继续推理；其取证轮数和信息量可随样本难度变化。不过，原文指出现有图令牌方法尚未把这种逐步行动机制落实到图令牌空间中。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 静态图令牌方法在语言模型看到问题之前就确定图视图，而且编码后不再修订。预选范围过窄会遗漏答案所需证据，范围过宽则会稀释有效信号；系统却必须把最终表现押在这一次选择上。
- 现有方法通常单次前向即作答，模型无法根据前一步观察结果继续请求邻域、群落或相似节点等证据。即使改为多步训练，模型在同时获得提示文本和图令牌时也容易依赖文本而忽略图令牌，导致表面上存在行动轨迹，实际判断却未扎根于图结构。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

缺失的是一种真正以图令牌为交互媒介的多步推理机制：图视图不能只是固定输入，而应成为模型在推理途中可按需调用的工具；每次调用还应由既有轨迹决定，并返回可继续参与后续决策的图表示。同时，训练方法必须确保模型确实读取这些动态令牌，而不是仅凭节点文本或动作模板完成任务。

</div>
<div markdown="1"><span>核心问题</span>

语言模型如何通过图令牌执行逐步的智能体式推理？更具体地说，模型如何在每一步依据当前上下文选择图视图及其粒度，将该视图编码后纳入持续增长的轨迹，并在证据充分时自适应终止并输出答案？

</div>
<div markdown="1"><span>作者直觉</span>

不同问题像是在同一张图上采用不同的调查路径：欺诈检查可以先看账户自身描述，再看交易伙伴，发现异常后扩展到周边群落，最后检索行为相似的账户。若把图编码器视为模型可调用的取证工具，固定长度的图令牌就能在不把大型子图完整写入上下文的情况下，逐轮提供与当前判断最相关的结构证据；而让后续动作依赖先前返回的令牌，可使简单样本少查、困难样本多查。三阶段训练进一步分别解决“能否读懂令牌”“是否依据令牌形成轨迹”和“图与文本冲突时是否仍以图证据为依据”这三个障碍。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把图分析改写为一个由大语言模型控制的多步决策过程。输入是图 $\mathcal{G}$、问题 $Q$ 与锚点节点 $v$；模型起初只读取问题，不预先注入固定图表示。第 $t$ 步，语言模型根据已有上下文 $\tau_{t-1}$ 选择动作 $a_t$，动作指定本轮应观察的节点、若干跳邻域、相似节点集合或节点所在簇；图神经网络随后把相应子图 $G^{V_t}$ 编码成固定长度的连续向量块 $\mathbf{Z}^{\mathrm{AGT}}_t$，并将其插入上下文。后续动作直接以这些连续图词元为条件，因此模型能依据已收集的证据继续缩小、扩大或转移观察范围，最后执行终止动作并生成答案 $A$。与先选定一个图视图再单次推理的方法相比，这里的图词元内容取决于整条动作轨迹和当前样本难度。

训练分三阶段解决三个递进问题：阶段一通过文本重建和掩码链路预测，让语言模型理解连续图词元分别承载节点语义与局部结构；阶段二用合成的变长轨迹监督动作和答案，并通过干净图表示与扰动图表示之间的分布一致性，提高图词元读取的鲁棒性；阶段三构造“真实文本与图一致”优于“替换锚点文本后与图冲突”的轨迹偏好，用身份偏好优化强化对图证据的依赖。通俗地说，模型不是开考前拿到一张固定范围的图摘要，而是在答题过程中不断决定下一次应查看节点本人、近邻、远邻、相似节点还是群组，再把每次得到的结构化线索累积起来作答。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 图词元语义与结构对齐

阶段一联合训练图编码器 $f^{\mathrm{GNN}}$ 与语言模型 $f^{\mathrm{LLM}}$：文本重建要求从 $v$ 的 `node_token` 恢复标题和摘要，掩码链路预测要求判断候选节点 $w$ 与 $v$ 是否存在边；损失只计算回答词元，注入的连续图词元不作为预测目标。涉及验证或测试节点的边会从链路预测训练图中移除，以避免结构泄漏。

<div class="method-step__io" markdown="1">

**输入**：训练锚点节点 $v$、其节点文本、局部图结构，以及由 $f^{\mathrm{GNN}}$ 产生的图词元块 $\mathbf{Z}^{\mathrm{AGT}}$。<br>
**输出**：得到能够把异构图词元解释为节点内容和局部拓扑证据的初始图编码器与语言模型。

</div>

**直观理解**：连续图向量原本不对应任何自然语言词，阶段一相当于先教模型读懂这种新型证据。重建文本检查它是否读出“节点讲什么”，链路预测检查它是否读出“节点怎样连接”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 变长动作轨迹监督与鲁棒化

阶段二先用加权交叉熵模仿轨迹中的动作调用和答案，再对同一图视图分别生成干净编码与增强编码；增强以概率 $p_{\mathrm{ed}}=0.1$ 丢边、以概率 $p_{\mathrm{tm}}=0.2$ 遮蔽图词元，并用 KL 散度让增强编码下的回答分布接近停止梯度的干净分布。答案词元权重设为 $\omega=20$，一致性权重设为 $\lambda_{\mathrm{KL}}=0.5$。

<div class="method-step__io" markdown="1">

**输入**：阶段一模型，以及由训练锚点、动作序列和正确最终答案组成的合成轨迹；动作来自集合 $\mathcal{A}$。<br>
**输出**：得到既会选择图视图、组合多轮图证据并输出答案，又不易因局部边或词元扰动而失效的轨迹策略。

</div>

**直观理解**：仅会读一块图词元不等于会规划多步查询，因此先让模型照着示范学习“看哪里、何时回答”。随后把同一证据轻微破坏并要求判断基本不变，避免模型只记住脆弱的表面模式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 图文一致性偏好优化

仅保留满足 $A^{\mathrm{c}}=y$、$A^{\mathrm{i}}\neq y$ 且 $A^{\mathrm{c}}\neq A^{\mathrm{i}}$ 的轨迹对，并设置 $\tau^+=\tau^{\mathrm{c}}\succ\tau^-=\tau^{\mathrm{i}}$；随后以阶段二模型为冻结参考策略，通过身份偏好优化拉开两条轨迹的相对得分。该阶段仍联合更新 $f^{\mathrm{GNN}}$ 与 $f^{\mathrm{LLM}}$。

<div class="method-step__io" markdown="1">

**输入**：阶段二策略对每个锚点生成的两条贪心轨迹：真实节点文本与真实图一致的 $\tau^{\mathrm{c}}$，以及仅把锚点文本替换为随机节点 $v'$ 的文本、但保留原图不变的 $\tau^{\mathrm{i}}$。<br>
**输出**：得到在节点文本与图结构冲突时更倾向依据图词元证据，而不是依赖锚点文本捷径的最终策略。

</div>

**直观理解**：这里人为制造“节点自述与周围关系说法不一致”的案例，只选择文本替换会把正确答案翻成错误答案的样本。模型因而获得明确反馈：应偏好图文相互印证的推理轨迹，并降低被误导文本带偏的概率。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按需图视图推理

每轮模型从 $\mathcal{A}$ 选择一个动作，并通过映射 $V(a_t)$ 确定图视图；编码器将该视图转为 $\mathbf{Z}^{\mathrm{AGT}}_t$ 后，与动作一起追加到上下文。若动作是 `answer`，模型输出 $A$ 并终止，否则继续依据累计图词元选择下一视图。

<div class="method-step__io" markdown="1">

**输入**：最终策略、待分析图 $\mathcal{G}$、问题 $Q$、锚点 $v$，初始上下文为 $\tau_0=Q$。<br>
**输出**：一条长度和访问范围随问题变化的图词元轨迹，以及最终任务答案 $A$。

</div>

**直观理解**：容易样本可能只需查看节点本身，困难样本可以逐步扩展到近邻、远邻或簇。模型自行决定查询次数和范围，因此不会对简单样本过度编码，也不会让困难样本受限于预先固定的视野。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 多步智能体图词元推理递推

$$
\tau_0=Q,\qquad a_t\sim f^{\mathrm{LLM}}(\cdot\mid\tau_{t-1}),\qquad V_t=V(a_t),\qquad \mathbf{Z}^{\mathrm{AGT}}_t=f^{\mathrm{GNN}}\!\left(G^{V_t}\right),\qquad \tau_t=\left(\tau_{t-1},a_t,\mathbf{Z}^{\mathrm{AGT}}_t\right),\quad t=1,\ldots,T
$$

**符号说明**

- $\mathcal{G}$：待分析的完整图。
- $Q$：输入问题，也是初始上下文的内容。
- $\tau_t$：完成第 t 步后的运行上下文，包含此前问题、动作和图词元块。
- $a_t$：语言模型在第 t 步选择的单个图查询或终止动作。
- $f^{\mathrm{LLM}}$：负责动作决策与最终答案生成的语言模型。
- $V(\cdot)$：把动作映射为节点集合或图视图范围的函数。
- $V_t$：第 t 步动作确定的图视图索引或节点范围。
- $G^{V_t}$：从完整图中按 $V_t$ 取得的节点、邻域、检索结果或簇视图。
- $f^{\mathrm{GNN}}$：把指定图视图编码到语言模型嵌入空间的图神经网络。
- $\mathbf{Z}^{\mathrm{AGT}}_t$：第 t 步按需生成的智能体图词元块。
- $T$：终止前的轨迹步数，由模型按问题动态决定。

<div class="equation-explanation" markdown="1">

**直观理解**：该递推刻画方法的核心闭环：已有图证据决定下一次查询，而查询结果又成为下一轮决策的输入。由于 $V_t$ 每轮重新选择，模型能够放大、缩小或切换观察区域，最终轨迹不是预先固定的单个图摘要。<br>
**原文位置**：第4节，公式(3)至(6)

</div>

</div>

<div class="equation-block" markdown="1">

#### 三阶段训练目标

$$
\begin{aligned}\mathcal{L}_1&=-\sum_{t\in\mathcal{S}}\log f^{\mathrm{LLM}}\!\left(y_t\mid y_{<t},\mathbf{Z}^{\mathrm{AGT}}\right),\\ \mathcal{L}_{\mathrm{CE}}&=\frac{1}{|\mathcal{S}|}\sum_{t\in\mathcal{S}}w_t\,\mathrm{CE}(\ell_t,y_t),\\ \mathcal{L}_2&=\mathcal{L}_{\mathrm{CE}}^{\mathrm{clean}}+\lambda_{\mathrm{KL}}\,\mathrm{KL}\!\left(\mathrm{sg}[p^{\mathrm{clean}}]\,\|\,p^{\mathrm{aug}}\right),\\ \mathcal{L}_3&=\mathbb{E}_{(\tau^+,\tau^-)}\!\left[\left(h(\tau^+)-h(\tau^-)-\frac{1}{2\beta}\right)^2\right],\qquad h(\tau)=\log\frac{f^{\mathrm{LLM}}(\tau\mid Q)}{f^{\mathrm{LLM}}_{\mathrm{ref}}(\tau\mid Q)}.\end{aligned}
$$

**符号说明**

- $\mathcal{L}_1$：阶段一的自回归交叉熵，用于图词元的内容与结构对齐。
- $\mathcal{S}$：需要计算损失的模型回答词元位置集合；注入的图词元位置被排除。
- $y_t$：位置 t 的目标回答词元。
- $y_{<t}$：位置 t 之前的目标回答词元序列。
- $\mathbf{Z}^{\mathrm{AGT}}$：作为条件输入的图词元块，而非语言预测目标。
- $\mathcal{L}_{\mathrm{CE}}$：阶段二轨迹监督的加权交叉熵。
- $w_t$：词元权重；答案位置取 $\omega$，其他模型输出位置取 1。
- $\ell_t$：语言模型在位置 t 输出的未归一化预测分数。
- $\mathcal{L}_2$：阶段二的一致性正则化总目标。
- $\lambda_{\mathrm{KL}}$：干净与增强表示分布一致性项的权重。
- $p^{\mathrm{clean}}$：使用未扰动图编码时，回答位置上的 softmax 概率分布。
- $p^{\mathrm{aug}}$：使用丢边和图词元遮蔽后的编码时，回答位置上的 softmax 概率分布。
- $\mathrm{sg}[\cdot]$：停止梯度操作，使干净分布作为固定教师。
- $\mathcal{L}_3$：阶段三的身份偏好优化目标。
- $\tau^+$：图与锚点文本一致且得到正确答案的偏好轨迹。
- $\tau^-$：锚点文本被替换、与原图冲突并得到错误答案的非偏好轨迹。
- $h(\tau)$：当前策略相对参考策略对整条轨迹提高的对数概率。
- $f^{\mathrm{LLM}}_{\mathrm{ref}}$：由阶段二模型初始化并作为比较基准的参考语言模型。
- $\beta$：控制偏好轨迹与非偏好轨迹目标间隔的超参数。

<div class="equation-explanation" markdown="1">

**直观理解**：三个目标依次要求模型“读得懂、读得稳、真正使用”图词元：$\mathcal{L}_1$ 建立图向量与语义及结构的对应，$\mathcal{L}_2$ 在轨迹模仿之外约束扰动前后判断一致，$\mathcal{L}_3$ 则让当前策略相对阶段二参考策略更偏好图文一致的轨迹。IPO 使用平方目标把偏好差控制在有限目标间隔附近，作者据此避免小规模偏好对下 DPO 无界对数比带来的脆弱性。<br>
**原文位置**：第4.1至4.3节，公式(7)至(10)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优化顺序不可互换地对应能力递进。阶段一在文本重建和掩码链路预测样本上最小化 $\mathcal{L}_1$，联合调整 $f^{\mathrm{GNN}}$ 与 $f^{\mathrm{LLM}}$，使连续图词元进入语言模型可解释的表示空间；阶段二先最小化答案加权的 $\mathcal{L}_{\mathrm{CE}}$ 学习动作与答案格式，再最小化 $\mathcal{L}_2$，把干净编码视为教师并约束增强编码产生相近的回答分布。阶段三从策略自身 rollout 中筛选图文一致性偏好对，最小化 $\mathcal{L}_3$；参考模型固定为阶段二策略，$\beta=0.3$。每一阶段从上一阶段初始化，三阶段都联合更新图编码器和语言模型，而预先计算的 mpnet 文本特征及图拓扑不更新。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 开放式图动作接口**

动作空间 $\mathcal{A}$ 包含 `node_token`、`one_hop_token`、`two_hop_token`、`three_hop_token`、`retrieval_token`、`cluster_token`、`anchor_text`、仅用于链路预测的 `cosine_sim`，以及终止用的 `answer`。其中检索动作构造以锚点为中心、连接余弦相似度最高的 $k$ 个节点的星形图；每个动作通过 $V(a_t)$ 映射到待编码范围。

> 直观理解：这些动作相当于一组图查询工具：既可看节点本人和不同半径的邻域，也可看语义相似节点或所在群组。接口不依赖特定任务，后续可以增加新动作而无需改写整体推理循环。

**2. 按需图词元编码器**

图神经网络 $f^{\mathrm{GNN}}$ 接收动作指定的子图 $G^{V_t}$，联合聚合节点属性与拓扑，并输出位于语言模型嵌入空间中的固定长度连续块 $\mathbf{Z}^{\mathrm{AGT}}_t$。该块直接插入上下文，不先转换成自然语言；训练时图编码器和语言模型联合更新，而 mpnet 文本特征与图拓扑保持冻结。

> 直观理解：它把大小和形状不同的图视图压缩成语言模型可读取的短向量块，同时尽量保留“节点是什么”和“节点怎样连接”。直接保留连续结构表示，可避免把邻域逐项写成文本所造成的上下文膨胀和拓扑信息弱化。

**3. 轨迹控制语言模型**

语言模型 $f^{\mathrm{LLM}}$ 同时充当策略与答案生成器：中间步骤只输出单个动作，不输出自然语言推理；下一步以此前的动作和图词元块为条件，终止时才生成答案 $A$。阶段二训练动作选择和答案生成，阶段三进一步校准整条轨迹相对于参考策略的概率。

> 直观理解：同一个模型既负责决定下一步查什么，也负责整合查到的证据。中间只传动作和紧凑图词元，可减少冗长文字推理对结构信号的干扰。

**训练与推理**

训练时，先为各锚点构建阶段一的文本重建与无泄漏链路预测任务；再构建包含不同动作组合和正确答案的变长合成轨迹，完成普通监督预热及图扰动一致性训练；最后分别在真实图文输入和仅替换锚点文本的冲突输入上执行贪心 rollout。只有一致轨迹答对、冲突轨迹答错且两者答案不同的样本才形成偏好对，原文称每次运行约得到 $300$ 对，然后以阶段二模型为参考执行 IPO。

推理时不需要针对目标节点微调，也不先生成固定图词元。上下文从 $Q$ 开始，模型每轮只输出动作；运行环境解析动作、抽取相应 $G^{V_t}$，调用 $f^{\mathrm{GNN}}$ 生成固定长度的 $\mathbf{Z}^{\mathrm{AGT}}_t$ 并插回上下文。模型可连续调用不同粒度的结构动作，也可读取锚点原文；链路预测还可调用端点余弦相似度。执行 `answer` 后才生成最终答案，因此访问视图和步数 $T$ 均由当前问题决定。

**复现信息**

公平理解该方法需要保留四点。第一，图词元是固定长度连续向量块，并直接位于语言模型嵌入空间，不是图视图的文字序列化。第二，阶段二将答案词元权重设为 $\omega=20$；一致性增强采用 $p_{\mathrm{ed}}=0.1$ 的丢边概率和 $p_{\mathrm{tm}}=0.2$ 的图词元遮蔽概率，且 $\lambda_{\mathrm{KL}}=0.5$。第三，阶段三设置 $\beta=0.3$，偏好对只替换锚点输入文本，原节点的图结构、邻居及邻居文本保持不变，从而尽量隔离“依赖文本还是依赖图”的因素。第四，所有训练阶段都联合更新图编码器与语言模型，但 mpnet 文本特征和拓扑冻结；具体图编码器层数、图词元块长度、优化器、学习率、批大小及最大推理步数在所给节选中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ogbn-arxiv：以论文为节点、引用为边的文本属性图，节点文本为标题和摘要，标签为 $40$ 个计算机科学主题。它是主要域内基准，也是所有零样本迁移实验的源域。节点分类从官方训练划分抽取 $3000$ 个训练节点，并在独立的 $1000$ 个节点上测试；链接预测使用 $1500$ 个正边和 $1500$ 个负样本训练，在 $500$ 个正边与 $500$ 个负样本上测试。
- ogbn-products：Amazon 商品共购图，节点文本为商品描述，标签为 $42$ 个商品类别。它用于检验方法能否处理与论文引用不同的关系语义。节点分类和链接预测沿用统一的 $3000/1000$ 节点及 $3000/1000$ 节点对采样协议。
- STRING-db：人类蛋白质相互作用图，节点文本描述蛋白质，标签为 $21$ 个 COG 蛋白质功能类别。该数据集用于检验文本线索较弱、分类更依赖图结构时的方法表现；节点分类同样采用 $3000$ 个训练节点和 $1000$ 个测试节点。实验整体覆盖十个文本属性图，其中七个用于域内训练和评测，零样本研究则把 ogbn-arxiv 上训练的策略迁移到七个未见目标图。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**节点分类准确率**

在固定的 $1000$ 个测试节点中，预测类别与真实类别一致的比例；它直接衡量多类别节点分类能力，但不能单独说明模型是否真正使用了图结构。 （越高越好，因为正确分类的测试节点比例更大。）

</div>
<div class="metric-item" markdown="1">

**AUC**

链接预测中，根据分数 $\mathrm{logit}(\texttt{yes})-\mathrm{logit}(\texttt{no})$ 对正边和负边排序，衡量随机正边得分高于随机负边的概率。测试集由 $500$ 个正样本和 $500$ 个负样本组成。 （越高越好，因为模型区分存在边与不存在边的排序能力更强。）

</div>
<div class="metric-item" markdown="1">

**按节点度数估计的错误比例密度**

对误分类节点的度数做高斯核密度估计，并把曲线面积缩放为该模型的总错误质量。曲线高度反映错误集中在哪些度数区间，面积则反映错误总量；它是错误结构分析，不是独立的任务性能指标。 （整体越低越好，因为表示总错误质量更少；还需比较曲线形状，判断收益是否只来自高连接度节点。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨七个图领域的总体比较

<div class="result-value" markdown="1">

作者声称，该方法在覆盖七个图领域的评测中以较大幅度超过广泛的基线集合；所给摘录未提供各数据集的准确率、AUC、绝对提升或方差，因而无法判断“large margin”的具体大小及其跨任务一致性。

</div>

这一结论支持动态、轨迹相关的图令牌机制具有总体优势，但目前证据只是一句作者汇总陈述。由于缺少主结果表，不能确认优势主要来自动态视图选择、三阶段训练、额外训练数据，还是这些因素的组合，也不能据此断言每个数据集都显著领先。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across evaluations spanning seven graph domains, our models outperform a broad set of baselines by a large margin and transfer zero-shot to unseen domains without any per-target fine-tuning.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 从 ogbn-arxiv 向未见目标图的零样本迁移

<div class="result-value" markdown="1">

作者报告将 ogbn-arxiv 上训练的策略直接迁移到七个从未见过的目标图，目标域不进行任何进一步训练；所给摘录未包含表 3 的具体目标列表和分数。

</div>

该设置检验策略是否学习到可跨图复用的图令牌操作，而不只是记住源数据集标签模式。无需目标域微调具有实际价值，但“零样本”并不等于完全没有先验：模型仍继承语言模型预训练知识、MPNet 文本表示以及源域策略训练。缺少表 3 还意味着无法核实迁移到跨家族图时是否始终有效。

<div class="result-source" markdown="1">

来源：Section 5.1, Datasets；结果指向 Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Seven are used for in-domain training and evaluation (ogbn-arxiv, ogbn-products, PubMed, Reddit, arXiv-2023, CiteSeer, STRING-db), and a zero-shot study transfers the ogbn-arxiv-trained policy, without any further training, to seven targets it has never seen (Table 3).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 相对 AgentGL 的节点度数分层错误结构

<div class="result-value" markdown="1">

在 ogbn-arxiv、ogbn-products、PubMed 和 Reddit 共四个数据集的同一批 $1000$ 个测试节点上，作者观察到本文方法的错误质量曲线均低于 AgentGL；两种方法的错误都更多集中于低度节点，但本文方法的优势贯穿整个度数范围。

</div>

配对测试减少了因测试节点不同造成的混淆。结果表明收益并非只来自容易利用邻域信息的高连接度枢纽节点，而是在低度到高度节点上都减少了错误。不过这是描述性核密度分析，没有给出置信区间或逐度数显著性检验，也不能证明动态选图视图是误差减少的唯一原因。

<div class="result-source" markdown="1">

来源：Appendix E；Figure 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The errors of both methods concentrate on lower-degree nodes, where the graph signal is scarcest, but our density stays below AgentGL’s across the whole degree range, not merely at the well-connected end.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验章节缺少主要性能表，未提供逐数据集准确率、AUC、绝对或相对提升、方差、随机种子数量和统计显著性检验；因此“large margin”和零样本迁移优势只能作为作者声明，仍需核对 Table 3 及其他主结果表。
- 敏感性分析只覆盖四个数据集、$3$B 骨干和节点分类，尚不能证明令牌预算及 GNN 骨干结论可推广到链接预测、更大语言模型或全部十个图；错误结构分析也只与 AgentGL 比较，未覆盖静态图令牌基线。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen（zero-shot/CoT）：冻结 Qwen2.5-3B-Instruct，仅输入目标节点文本和候选类别；CoT 版本额外要求逐步推理。它们检验提升是否只是来自语言模型的文本知识或显式思维链，而非图结构。
- Graph2Text-SFT：把中心节点及其一跳邻居序列化成文本，再监督微调同一 Qwen 骨干。它与本文方法都使用邻域信息，但前者通过自然语言传递图结构，因此可检验连续图令牌是否优于文本化邻域。
- LLM-GNN：先由 Qwen 根据文本产生伪标签，再训练 GraphSAGE 图分类器。它代表语言模型与传统图神经网络的级联组合，用于判断端到端图令牌推理是否优于把语言模型仅当作标注器。
- 静态图令牌方法 TEA-GLM、GraphGPT 与 GraphTranslator：三者均把基于 MPNet 特征和 GraphSAGE 编码的一跳邻域投影成 $128$ 个连续图令牌，但在模型看到并推理目标问题前就固定图视图。TEA-GLM 冻结语言模型，GraphGPT 联合微调语言模型和编码器，GraphTranslator 使用两阶段令牌翻译器；这一组是检验“轨迹相关、按需调用图编码器”是否优于静态单次令牌化的关键对照。

**实验想回答的问题**

- 在节点分类与链接预测中，按推理轨迹动态选择图视图并生成图令牌，是否比纯文本推理、图结构文本化、传统图神经网络以及静态单次图令牌方法更有效？
- 该策略能否在不针对目标图继续训练的条件下迁移到未见领域，以及其收益是否对节点度数、每次动作的令牌预算和池化器中的图神经网络骨干保持稳定？

**实验实现**

同骨干基线统一使用 Qwen2.5-3B-Instruct、相同的数据划分、相同的测试节点或候选边，以及由原始节点文本计算的 MPNet 特征，方法之间主要改变图信息进入模型的机制。节点分类训练语料最多为 $20000$ 个样本，链接预测训练语料最多为 $6000$ 个样本；编码器和投影器训练一个 epoch，图模块学习率为 $5\times10^{-4}$，梯度累积为 $4$，最大序列长度为 $2048$。链接预测会从两个端点的邻域中遮蔽待预测边，避免直接泄漏答案。作者还说明测试节点和候选节点对均未进入任何训练或对齐语料。不过，所给章节没有列出主结果表中的逐数据集分数、方差、随机种子数量或显著性检验，因此只能核实实验协议和作者的汇总结论，不能从摘录中复算性能差距。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 每次图令牌动作的令牌预算：$16$、$32$、约 $64$、$128$ 与 $256$ 个令牌 | 四个数据集上的准确率从 $16$ 增至 $32$ 个令牌时快速上升，超过 $64$ 个令牌后仅变化零点几个百分点；$128$ 个令牌在各数据集上达到最佳或处于噪声范围内，只有 ogbn-arxiv 在 $256$ 个令牌时仍有轻微提升。 | 该实验隔离每次调用图编码器所提供的表示容量。结果说明令牌过少会压缩掉重要图信息，而约 $64$ 至 $128$ 个令牌后边际收益趋于饱和。选择 $128$ 而非 $256$ 可把单次动作占用的推理上下文减半，同时只牺牲可忽略的准确率；但摘录没有报告具体分数、误差条或统计噪声的定义。 | Appendix H；Figure 10<br><span class="experiment-evidence">Accuracy rises steeply from 16 to 32 tokens and then flattens: beyond 64 tokens the four datasets move by only a few tenths of a point, and 128 is at or within noise of the best setting everywhere while ogbn-arxiv still gains slightly at 256.</span> |
| 池化器图神经网络骨干选择：GraphSAGE 与另外两种图卷积 | 在默认每次动作 $128$ 个令牌时，三种图卷积在每个数据集上的差距均约不超过 $1.5$ 个百分点；GraphSAGE 在四个数据集中的三个上最优或并列最优，并且计算成本最低。 | 该实验检验主结果是否依赖某一种特别强的图神经网络。较小的性能范围表明完整流程对池化器骨干相对稳健，GraphSAGE 的选择主要体现性能与成本的折中。不过摘录没有给出另外两种卷积的名称和逐数据集分数，因此不能判断它们在哪类图上各有优势。 | Appendix H；Figure 11<br><span class="experiment-evidence">The pooler is robust to this choice, with the three convolutions within about a point and a half on every dataset.</span> |

**定性案例**

- Figure 5 的配对错误分析可视为定性案例：在 ogbn-arxiv、ogbn-products、PubMed 和 Reddit 上，本文方法与 AgentGL 对同一批节点作答，前者的错误密度在整个节点度数范围内更低。其含义是图视图编码相较于邻居文本检索留下了更少的残余错误；但这只是总体错误分布，不展示具体节点、所选图视图或推理轨迹，因而不能直接解释单个预测为何被纠正。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：让LLM在推理轨迹中按需选择图视图并调用图编码器生成动态token，是面向图分析的工具调用式智能体推理方法。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`22ccba76d65a9c1bd80a2aac5827a097fa20220dfed135e4b4537050ccc97d8b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
