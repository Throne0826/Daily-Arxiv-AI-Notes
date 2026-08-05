---
title: "[论文解读] Balancing Efficiency and Efficacy: Training-Free Attention-Guided Switching Between Explicit and Latent Thoughts for MLLMs"
description: "[arXiv 2608.03450][VLM Reasoning] 本文针对多模态大语言模型中感知与推理混杂导致的模式切换失准，提出无需训练的注意力引导切换方法 AGS，依据视觉—文本注意力比在连续潜在思考与显式文本推理之间动态路由。"
arxiv_id: "2608.03450"
announcement_date: "2026-08-05"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:38:05.179099+00:00"
source_sha256: "e90c0cd685a89f2cfd753f1726e2d7a8c7b06290f234b97f29107a43b26bbf0c"
tags:
  - "VLM Reasoning"
  - "VLM Efficiency"
  - "LLM 其他"
  - "LLM Reasoning"
  - "多模态大语言模型"
  - "多模态推理"
  - "显式思维链"
  - "潜在推理"
  - "感知—推理解耦"
  - "视觉—文本注意力比率"
  - "免训练推理"
  - "动态模式切换"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.03450</p>

# Balancing Efficiency and Efficacy: Training-Free Attention-Guided Switching Between Explicit and Latent Thoughts for MLLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Haoqian Kang, Liupeng Li, Kuofeng Gao, Jinpeng Wang, Zhenyu Lu, Bin Chen, Ke Chen, Yaowei Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Harbin Institute of Technology, Shenzhen Shenzhen China；Harbin Institute of Technology, Shenzhen；Tsinghua Shenzhen International Graduate School, Tsinghua University Shenzhen China；Tsinghua Shenzhen International Graduate School, Tsinghua University；Peng Cheng Laboratory Shenzhen China；Peng Cheng Laboratory；Shenzhen Institutes of Advanced Technology, Chinese Academy of Sciences Shenzhen China；Shenzhen Institutes of Advanced Technology, Chinese Academy of Sciences</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03450v1) · [PDF 下载](https://arxiv.org/pdf/2608.03450v1) · **关键词** 多模态大语言模型, 多模态推理, 显式思维链, 潜在推理, 感知—推理解耦, 视觉—文本注意力比率, 免训练推理, 动态模式切换<br>
**代码**: [https://github.com/swordAndSnow/MM26-AGS](https://github.com/swordAndSnow/MM26-AGS)

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

本文针对多模态大语言模型中感知与推理混杂导致的模式切换失准，提出无需训练的注意力引导切换方法 AGS，依据视觉—文本注意力比在连续潜在思考与显式文本推理之间动态路由。

**不用术语来说**：多模态模型解题时既要看清图像细节，也要按步骤进行逻辑推导。若把全部思考都写成文字，不仅生成速度慢，还可能在将视觉内容转述为语言时丢失信息并产生幻觉；若直接沿用文本模型中基于输出不确定度的隐式思考切换规则，又无法判断模型究竟是“没看清”还是“没想明白”，因而可能在错误的阶段采用错误的思考方式。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者识别出多模态潜在推理中的“熵纠缠”问题：词元级熵同时反映感知歧义与逻辑不确定性，不能可靠地充当显式—潜在模式切换依据；为此提出可解释的视觉—文本注意力比 $R_A$，用模型当前对视觉词元和文本词元的相对注意程度判断解码阶段的功能。
- 作者据此设计无需重新训练或修改架构的 AGS：将感知主导的步骤路由到连续潜在空间，以保留高保真视觉信息；将逻辑主导的步骤保留为显式文本生成，以维持顺序结构和推导锚点。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

多模态大语言模型（MLLM）需要在同一条生成轨迹中完成两类互相依赖的工作：从图像中识别对象、属性与空间关系，以及依据这些视觉事实进行逻辑推导。主流的显式思维链（CoT）把中间步骤逐词生成为离散文本，便于维持推理结构，但自回归生成带来较高延迟，并可能在把细粒度视觉信息转写为语言时丢失信息、诱发视觉幻觉。潜在推理则在连续表示空间中传递中间状态，可减少不必要的文本生成；然而，现有多模态潜在推理通常需要额外数据、教师监督或重新训练，而从纯文本模型直接移植的免训练切换方法又难以区分视觉感知困难与逻辑推理困难。本文由此研究一种白盒、免训练的推理时路由问题：利用模型内部的跨模态注意力判断当前解码步骤更偏重感知还是逻辑，并在潜在表示与显式文本之间动态切换。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**显式思维链（Explicit Chain-of-Thought, CoT）**

模型先以可读文本逐步写出中间推导，再生成最终答案。其优势是逻辑步骤有明确的顺序锚点，代价是每个中间词元都要自回归解码，增加计算量与延迟。

</div>
<div class="concept-item" markdown="1">

**潜在推理（Latent Reasoning）**

模型不把所有中间思考都转换成离散词元，而是在连续向量空间中传递隐藏状态或词嵌入混合。直观上，它允许模型“内部思考”而不逐字写出过程，但多模态场景中的潜在轨迹通常需要专门训练才能稳定工作。

</div>
<div class="concept-item" markdown="1">

**视觉—文本注意力比率**

该指标比较当前解码步骤分配给视觉词元和文本词元的注意力，用于刻画模型此刻更依赖图像还是已有文本上下文。较高的比率被解释为感知占主导，较低的比率被解释为逻辑推导占主导。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一幅图像及其文本问题，基础MLLM已完成常规预训练且参数在推理时保持冻结；输出是模型对该多模态问题的回答。模型沿单条自回归轨迹逐步处理上下文，在第$t$步读取内部注意力并计算视觉—文本注意力比率$R_{A,t}$：若视觉注意占比较高，则把该步骤视为感知主导并转入连续潜在空间，以概率加权的词嵌入混合作为后续输入；若该比率较低，则把步骤视为逻辑主导并恢复显式词元生成。问题的核心不是训练一个新模型，而是在不修改参数、无需额外监督数据的设定下，决定每一步应采用哪种推理模式，从而兼顾视觉信息保真、逻辑结构、答案准确率与推理效率。该设定要求能够访问模型内部注意力，因此属于白盒推理方法，而非仅调用输出接口的黑盒策略。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$t$**

自回归推理轨迹中的当前解码步骤。

</div>
<div class="notation-item" markdown="1">

**$R_{A,t}$**

第$t$个解码步骤的视觉—文本注意力比率，即视觉词元所获注意力相对于文本词元所获注意力的比值。

</div>

</div>

**直接相关的工作**

- **SwiReasoning（Shi et al., 2025）**: 这是面向纯文本LLM的免训练显式—潜在推理切换方法，依据词元级概率或熵决定模式。本文指出，直接改造成SwiR-MLLM后表现不稳定，因为高输出熵既可能来自图像细节不清，也可能来自复杂逻辑步骤，单一熵信号无法给出可靠的多模态路由决策。
- **Qiao et al. (2024) 与 Jia et al. (2025) 的感知—推理解耦方法**: 这些工作通过两阶段流程或LLM—MLLM协作在模块层面分离视觉感知与符号推理，有助于降低幻觉，但会引入额外模块和延迟，也难以描述两类过程在单条生成轨迹中的交替。本文转而在词元级进行动态解耦，并以跨模态注意力比率替代额外监督或专门训练。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

科学图表分析、几何题和多模态数学问题要求模型同时完成细粒度视觉感知与严谨逻辑推导。主流显式思维链需要逐词自回归生成中间过程，带来较多解码步骤和推理时延；更关键的是，把稠密、连续的视觉信息过早压缩成离散文字可能造成信息损失和视觉幻觉。因此，实际需求不是单纯缩短思维链，而是在不牺牲逻辑可靠性的前提下减少不必要的文字化过程。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **显式文本思维链（CoT）**：模型先在离散词元空间逐步写出中间推理，再生成最终答案。文字步骤能够为逻辑推导提供清晰的顺序结构，但视觉观察也必须被转换成语言并通过自回归方式逐词生成。
- **潜在推理及基于熵的训练自由切换方法**：已有多模态潜在推理在连续表示空间中交织文本与图像嵌入，以模拟“用图像思考”，但通常依赖外部高质量数据或强教师监督进行训练。为避免训练成本，SwiReasoning 一类源自纯文本模型的方法依据词元概率或词元级熵，在显式文本生成与隐式连续表示之间动态切换；其直接移植版本在文中称为 SwiR-MLLM。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 显式 CoT 对感知和推理一律采用离散文字表达：这增加自回归计算开销，并形成“语言瓶颈”，使细粒度视觉信息在文字化时可能丢失，从而加剧视觉幻觉。已有多模态潜在推理虽可绕开部分文字化过程，却通常需要昂贵的专门训练、外部数据或教师监督。
- 训练自由的熵切换机制把高熵统一视为应切换模式的信号，但多模态场景中的高熵可能来自两种性质不同的困难：看不清微小目标的感知歧义，或无法确定下一步推导的逻辑不确定性。二者需要不同处理，单一熵指标却无法区分，作者的初步评估因此观察到直接移植后的性能不稳定，有时甚至低于普通显式 CoT；具体数值在所给章节中未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一种同时满足三项条件的机制：无需额外训练，能够在单个解码步骤上判断模型当前主要是在读取图像还是进行逻辑推演，并据此选择适合该阶段的表示空间。换言之，缺口不只是新的潜在推理形式，而是一个不受“熵纠缠”影响、可解释且可直接用于多模态模式路由的状态信号。

</div>
<div markdown="1"><span>核心问题</span>

能否仅利用多模态模型推理时已有的内部注意力，在不修改架构、无需任务监督或重新训练的条件下，可靠区分感知主导与逻辑主导的解码步骤，并分别将其路由到连续潜在空间和显式文本空间，从而兼顾准确性、视觉忠实度与推理效率？

</div>
<div markdown="1"><span>作者直觉</span>

输出概率只告诉我们模型对“下一个词是什么”有多不确定，却没有说明不确定性的来源；内部注意力则显示当前步骤主要从哪里取信息。若模型显著关注视觉词元，该步骤更可能承担识别角度、空间关系或局部目标等感知功能，适合保留为概率加权的连续嵌入，避免先翻译成文字再处理；若模型更多依赖已有文本上下文，该步骤更可能是在组织顺序化逻辑，显式生成词元可以提供稳定的结构约束。因此，视觉—文本注意力比 $R_A$ 有望成为比熵更贴近当前认知功能的路由依据。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

AGS（Attention-Guided Switching）是一种无需训练的多模态推理策略。给定图像 $\mathbf{I}$ 与问题 $Q$，模型先把视觉特征和文本嵌入拼接成统一上下文；在每个生成步 $t$，它读取各层、各注意力头对视觉与文本位置的注意力，计算视觉—文本注意力比 $R_{A,t}$，以判断当前步骤更偏向视觉感知还是逻辑推理。感知占主导时，不立即选取离散词，而将词表分布加权成软嵌入 $\tilde{\mathbf e}_t$ 并在连续空间中传播；文本推理占主导时，则贪心解码出离散词 $\hat y_t$，以显式语言维持逻辑结构。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造多模态上下文

视觉编码器和跨模态投影器将图像转换为 $N$ 个视觉嵌入 $\mathbf E_v\in\mathbb R^{N\times d}$，分词与嵌入层将问题转换为 $M$ 个文本嵌入 $\mathbf E_t\in\mathbb R^{M\times d}$；二者按序列维拼接为 $\mathbf E=[\mathbf E_v;\mathbf E_t]$。

<div class="method-step__io" markdown="1">

**输入**：图像 $\mathbf I$ 与文本问题 $Q$。<br>
**输出**：长度为 $L=N+M$ 的联合上下文 $\mathbf E\in\mathbb R^{L\times d}$。

</div>

**直观理解**：模型把图像切换成一组可由语言模型读取的向量，再与问题文字排在同一条上下文序列中。后续推理因此可以同时回看图像证据和已有文字。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 预测下一步并测量认知焦点

模型得到词表概率分布 $\mathbf p_t$，并分别统计当前查询对视觉位置集合 $\mathcal I_v$ 和文本位置集合 $\mathcal I_t$ 的平均注意力 $A_{V,t}$、$A_{T,t}$；随后计算 $R_{A,t}=A_{V,t}/A_{T,t}$。

<div class="method-step__io" markdown="1">

**输入**：初始上下文 $\mathbf E$、此前追加的嵌入序列以及当前步各层各头的注意力权重。<br>
**输出**：下一词概率 $\mathbf p_t$ 与表示视觉相对关注程度的标量 $R_{A,t}$。

</div>

**直观理解**：该比值回答的不是“模型有多不确定”，而是“模型此刻主要在看图，还是主要在沿文字继续推导”。按视觉和文本位置数分别取平均，可减轻两类上下文长度不同造成的偏差。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按阶段阈值判定推理模式

通常在 $R_{A,t}\geq\tau_k$ 时选择潜在感知，在 $R_{A,t}<\tau_k$ 时选择显式推理；若已进入显式模式但持续不足 $W$ 步，则强制保持显式模式。达到最大切换预算 $C$ 后终止思考阶段，防止模式循环。

<div class="method-step__io" markdown="1">

**输入**：当前注意力比 $R_{A,t}$、本阶段首步参考值 $\tau_k=R_{A,t_k}$、上一状态 $S_{t-1}$、显式模式起点 $t_{\mathrm{exp}}$、最小维持窗口 $W$ 与累计切换次数 $c_{t-1}$。<br>
**输出**：二值状态 $S_t\in\{0,1\}$ 及更新后的切换计数 $c_t$，其中 $0$ 表示潜在模式、$1$ 表示显式模式。

</div>

**直观理解**：AGS不使用跨样本固定阈值，而把每个推理阶段的起点当作局部标尺，因此适应不同图像和不同推理阶段的注意力量级。窗口约束防止刚开始一句推理就被打断，预算约束则给整个思考过程设置硬上限。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 路由嵌入并继续生成

潜在模式计算软嵌入 $\tilde{\mathbf e}_t=\mathbf W^\top\mathbf p_t$；显式模式使用 $\hat y_t=\arg\max\mathbf p_t$ 对应的 $\operatorname{Emb}(\hat y_t)$。预算首次达到 $C$ 时只注入一次终止标识嵌入 $\mathbf e_{\mathrm{stop}}$，此后采用标准显式生成直至答案结束。

<div class="method-step__io" markdown="1">

**输入**：状态 $S_t$、词表分布 $\mathbf p_t$、词表嵌入矩阵 $\mathbf W$ 与切换计数。<br>
**输出**：追加到上下文的最终嵌入 $\mathbf e_t^*$，以及最终可读的显式答案。

</div>

**直观理解**：看图阶段保留整个候选词分布的连续信息，避免过早把细腻视觉证据压成一个词；逻辑阶段则落到明确文字上，使推导具有可追踪的语义锚点。最终答案仍通过普通离散词输出。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 视觉—文本注意力比

$$
\begin{aligned} A_{V,t}&=\frac{1}{|\mathcal I_v|N_lN_h}\sum_{l=1}^{N_l}\sum_{h=1}^{N_h}\sum_{j\in\mathcal I_v}\alpha_{t,j}^{(l,h)},\\ A_{T,t}&=\frac{1}{|\mathcal I_t|N_lN_h}\sum_{l=1}^{N_l}\sum_{h=1}^{N_h}\sum_{k\in\mathcal I_t}\alpha_{t,k}^{(l,h)},\\ R_{A,t}&=\frac{A_{V,t}}{A_{T,t}}. \end{aligned}
$$

**符号说明**

- $t$：当前自回归生成步。
- $\mathcal I_v$：当前上下文中视觉词元的位置集合，其大小在生成期间保持不变。
- $\mathcal I_t$：当前上下文中文本词元的位置集合，会随生成逐步扩展。
- $N_l$：语言模型的注意力层数。
- $N_h$：每层纳入统计的注意力头数。
- $\alpha_{t,j}^{(l,h)}$：第 $l$ 层第 $h$ 个头中，当前步查询对位置 $j$ 的注意力权重。
- $A_{V,t}$：跨位置、层和头平均后的视觉注意力。
- $A_{T,t}$：跨位置、层和头平均后的文本注意力。
- $R_{A,t}$：视觉平均注意力与文本平均注意力之比。

<div class="equation-explanation" markdown="1">

**直观理解**：先分别计算模型平均分配给一个视觉位置和一个文本位置的注意力，再取二者之比；这避免了视觉词元通常较多时，仅因数量而得到较大总注意力。$R_{A,t}$ 越高，当前步骤越像在提取图像信息；越低，则越像依赖已有文字进行推导。<br>
**原文位置**：第3.2节，公式（5）—（6）

</div>

</div>

<div class="equation-block" markdown="1">

#### 受约束的状态判定与嵌入路由

$$
\begin{aligned} S_t&=\mathbb I\!\left(R_{A,t}<\tau_k\lor(S_{t-1}=1\land t-t_{\mathrm{exp}}<W)\lor c_{t-1}\ge C\right),\\ c_t&=c_{t-1}+\mathbb I(S_t\ne S_{t-1}),\\ \mathbf e_t^*&=\begin{cases}\mathbf e_{\mathrm{stop}},&c_t=C\ \text{and}\ c_{t-1}<C,\\ \tilde{\mathbf e}_t=\mathbf W^\top\mathbf p_t,&c_t<C\ \text{and}\ S_t=0,\\ \operatorname{Emb}(\hat y_t),&\text{otherwise},\end{cases}\quad \hat y_t=\arg\max_{y\in\mathcal V}p_t(y). \end{aligned}
$$

**符号说明**

- $S_t$：当前模式指示量；$0$ 为潜在推理，$1$ 为显式推理。
- $\mathbb I(\cdot)$：条件成立时取 $1$、否则取 $0$ 的指示函数。
- $\tau_k$：第 $k$ 个推理阶段的动态阈值，取该阶段首步的注意力比 $R_{A,t_k}$。
- $t_{\mathrm{exp}}$：最近一次进入显式推理模式的步骤。
- $W$：显式模式必须连续维持的最少步数。
- $c_t$：截至步骤 $t$ 的累计模式切换次数。
- $C$：允许的最大模式切换预算。
- $\mathbf p_t$：当前步在词表 $\mathcal V$ 上的预测概率分布。
- $\mathbf W$：尺寸为 $|\mathcal V|\times d$ 的词表嵌入矩阵。
- $\tilde{\mathbf e}_t$：由词表概率加权得到的连续软嵌入。
- $\hat y_t$：当前分布中概率最大的贪心解码词元。
- $\mathbf e_{\mathrm{stop}}$：终止思考标识（如 $\texttt{</think>}$）的预定义嵌入。
- $\mathbf e_t^*$：最终选中并追加到下一步上下文的嵌入。

<div class="equation-explanation" markdown="1">

**直观理解**：第一行决定当前是否必须显式化：视觉相对注意力下降、显式窗口尚未结束，或切换预算已耗尽，都会令 $S_t=1$。后续分段路由在预算内允许连续软嵌入传播；预算首次用尽时只插入一次结束思考标识，之后回到普通离散生成，从而避免无限循环。<br>
**原文位置**：第3.3节，公式（7）—（8）；软嵌入定义来自第3.1节公式（4）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。AGS是训练自由的推理时算法，不引入损失函数、梯度更新或额外参数优化；它直接复用预训练MLLM的词表分布、嵌入矩阵和内部注意力权重，在每个生成步执行状态判断与表示路由。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 视觉—文本注意力比**

模块对所有 $N_l$ 层、$N_h$ 个注意力头求平均，并分别除以视觉位置数 $|\mathcal I_v|$ 与文本位置数 $|\mathcal I_t|$，再形成比值 $R_{A,t}$。高比值被解释为视觉感知占主导，低比值被解释为文本语义和逻辑推进占主导。

> 直观理解：词级熵只能说明输出分布是否分散，无法区分“图像细节看不清”与“逻辑步骤很困难”。注意力比直接观察信息来源，因而为两种情况选择不同传播方式。

**2. 阶段式动态状态控制器**

每次模式切换后的首步 $t_k$ 建立新阈值 $\tau_k=R_{A,t_k}$，控制器结合该相对阈值、显式模式最小维持窗口 $W$ 和最大切换预算 $C$ 决定 $S_t$。计数器按 $c_t=c_{t-1}+\mathbb I(S_t\neq S_{t-1})$ 更新。

> 直观理解：不同样本的绝对视觉注意力不可直接比较，因此控制器比较同一阶段内的相对变化。两个约束分别抑制频繁抖动和无休止切换，使动态路由可控。

**3. 潜在—显式双路由器**

潜在分支用 $\mathbf W^\top\mathbf p_t$ 将所有词嵌入按概率加权，显式分支则选择贪心词 $\hat y_t$ 的离散嵌入。路由器只改变当前步追加到上下文的表示，不修改预训练MLLM参数。

> 直观理解：潜在分支像保留多个候选含义的混合表示，适合承载尚未文字化的视觉证据；显式分支像把关键推理写在纸上，适合稳定多步逻辑。

**训练与推理**

训练阶段无需任何额外处理。推理时，先按原模型流程编码图像和问题；随后循环执行前向预测、计算 $R_{A,t}$、依据阶段阈值与约束确定 $S_t$，并在软嵌入 $\tilde{\mathbf e}_t$ 与离散嵌入 $\operatorname{Emb}(\hat y_t)$ 之间选择。每次状态改变都更新 $c_t$；当预算首次达到 $C$ 时插入一次 $\texttt{</think>}$ 对应嵌入，此后完全采用显式自回归生成，直到模型输出最终答案或常规停止条件触发。

**复现信息**

公平复现需要从模型内部取得当前查询对视觉和文本位置的逐层、逐头注意力，并按位置数归一化，而不能用两类位置的注意力总和直接相除。文中消融后采用最小显式维持窗口 $W=512$ 与最大切换预算 $C=4$；显式分支使用贪心词 $\hat y_t=\arg\max\mathbf p_t$，潜在分支使用完整词表分布计算 $\mathbf W^\top\mathbf p_t$。终止标识必须仅在预算首次达到时注入一次，否则可能重复结束标记或形成路由循环；摘录未明确报告其他采样参数、缓存处理方式或硬件相关设置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 视觉数学组：MathVista 检验多技能视觉数学能力，MathVision 包含竞赛级题目，MathVerse 通过减少文本偏置强化对视觉推理的考察，WeMath 聚焦多步数学推理。原文未明确报告各数据集的样本规模、所用划分或是否使用完整测试集；这组数据主要检验 AGS 能否在既需读取图像细节、又需连续演绎的任务中保留视觉信息。
- 科学与通用推理组：ScienceQA 检验结合背景知识的多模态科学推理，$M^3$CoT 覆盖多种场景下的通用多模态多步推理。前者侧重知识与逻辑结合，后者用于观察方法是否超越视觉数学这一特定领域。原文未明确报告样本规模与评测划分。
- 视觉感知与幻觉组：POPE 用于评估物体幻觉鲁棒性，补充验证效率提升是否会削弱视觉依据；实验设置还提到用于细粒度视觉感知的 $V^*$，但所给章节未提供其量化结果、规模或划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Task Accuracy（Acc，%）**

最终答案正确率，用于衡量推理有效性。它能说明答案是否正确，但单独不能揭示推理过程是否忠实、是否依赖错误但碰巧得到正确答案的中间步骤。 （越高越好，因为更高数值表示更多样本得到正确答案。）

</div>
<div class="metric-item" markdown="1">

**Inference Efficiency（Eff）**

每个样本平均经历的自回归生成步数；除可见文本词元外，也计入仅在连续嵌入空间中前向传播、不输出离散词元的潜在推理步，因此比只统计可见输出长度更接近本文方法的实际推理计算量。 （越低越好，因为更少生成步通常意味着更低推理成本；但它不是硬件无关的延迟或能耗测量，不能单独证明真实部署速度按同比例提升。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 六个推理基准上的 Qwen3-VL-8B-Thinking 总体结果

<div class="result-value" markdown="1">

加入 AGS 后，六个任务的平均准确率由 $51.7\%$ 提升至 $58.8\%$，平均生成步数由 $2214$ 降至 $953$，即作者概括的约 $57\%$ 成本下降。该结果同时改善有效性与步数效率，是长推理链模型上最具代表性的总体收益。

</div>

通俗地说，AGS 不只是把答案过程缩短：在这组平均结果中，它用不到原先一半的生成步数得到更高正确率，说明部分显式文字化可能既冗余又会损失视觉信息。不过这是六个数据集的宏平均，不能说明每个任务都同幅改善；也不能把生成步减少直接等同于真实延迟、显存或能耗按 $57\%$ 下降。

<div class="result-source" markdown="1">

来源：Section 4.2 Main Result；Table 1，Qwen3-VL-8B-Thinking 与其 +AGS 行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the 8B model, AGS reduces the average generation cost from 2214 to 953 steps (∼57%) while improving accuracy from 51.7% to 58.8%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 视觉数学任务上的 Qwen3-VL-4B-Thinking

<div class="result-value" markdown="1">

在 WeMath 上，AGS 将准确率从 $43.1\%$ 提升至 $69.4\%$，绝对增加 $26.3$ 个百分点；Table 1 同时显示平均生成步数从 $3217$ 降至 $1114$。这表明收益在要求多步数学推理的视觉任务上尤其明显。

</div>

这一结果支持作者关于“潜在路由可避免重复文字化并保留视觉信息”的解释：模型在更少步骤下答对更多题。但实验只展示任务层面的最终准确率，没有直接测量被保留的视觉信息，也未把增益分解为视觉读取、数学运算和答案格式等因素，因此其机制解释仍属于由结果支持的推断，而非因果证明。

<div class="result-source" markdown="1">

来源：Section 4.2 Main Result；Table 1，Qwen3-VL-4B-Thinking 的 WeMath 列

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On WeMath, AGS raises Qwen3-VL-4B-Thinking accuracy from 43.1% to 69.4%; on MathVerse, the 4B and 8B models gain 15.9 and 8.8 percentage points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### POPE 物体幻觉评测中的跨模型表现

<div class="result-value" markdown="1">

作者报告六个模型变体的准确率均提高 $0.1$ 至 $1.1$ 个百分点，并在五个设置中减少生成步数。代表性地，InternVL3.5-8B 从 $82.8\%/79$ 步改善为 $83.9\%/76$ 步；Qwen3-VL-2B-Thinking 从 $86.8\%/112$ 步改善为 $87.2\%/104$ 步。

</div>

POPE 结果说明切换到潜在推理没有系统性破坏物体层面的视觉落地，且可能略微缓解物体幻觉。需要谨慎的是，准确率提升幅度较小，摘录没有误差条或显著性检验；此外 InternVL3.5-2B 的步数还从 $78$ 增至 $79$，所以不能声称 AGS 在所有模型上都严格提高效率。

<div class="result-source" markdown="1">

来源：Section 4.2 Main Result；Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On POPE, AGS improves accuracy for all six model variants by 0.1–1.1 percentage points and reduces generation steps in five settings. InternVL3.5-8B improves from 82.8% to 83.9% while reducing steps from 79 to 76, and Qwen3-VL-2B-Thinking improves from 86.8% to 87.2% while reducing steps from 112 to 104.

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

- Explicit CoT：所有中间推理均生成为离散文本，是最直接的基线。它用于判断 AGS 在显式文本推理与连续潜在推理之间切换后，能否同时保持逻辑结构、降低冗长生成成本并改善正确率。
- Token Entropy 路由：采用 SwiReasoning 使用的词元熵作为模式切换依据。该对照与 AGS 的路由框架目标相近，但依据预测分布的不确定性进行切换，因此可较直接地检验视觉—文本注意力比是否比词元熵更适合区分感知过程与逻辑过程。
- LEAD：多模态潜在推理方法；论文称其与 AGS 均使用同一个 Qwen3-VL-4B-Thinking 检查点，从而尽量控制基础模型差异、比较潜在推理策略本身。不过所给摘录仅出现表题，未包含 Table 5 的数值，不能据此判断二者优劣。

**实验想回答的问题**

- 在不额外训练模型的条件下，AGS 能否跨不同模型家族、参数规模与多模态推理领域，同时提高答案准确率并减少包括显式与潜在推理在内的自回归生成步数？
- AGS 的收益是否确实来自基于视觉—文本注意力比的路由，而非任意的显式/潜在模式切换；显式推理维持窗口 $W$ 又如何影响准确率与计算成本的平衡？

**实验实现**

实验覆盖 Qwen3-VL-Thinking 与 InternVL3.5 两个模型家族，各含 2B、4B、8B 三种规模。前者通常生成较长的审慎推理链，后者推理较简洁，因而可分别检验 AGS 在计算密集和紧凑推理场景中的适用性。实现基于 PyTorch，在 NVIDIA RTX A6000 GPU 上遵循两个模型的官方 HuggingFace 推理流程；最大序列长度为 $4096$，默认显式推理最小维持窗口为 $W=512$，最大切换预算为 $C=4$。显式词元使用多项式采样，设置 `do_sample=True`、温度为 $0.6$。所有实验均称无需额外训练或针对模型调参，但摘录未说明随机种子、重复运行次数、置信区间、显著性检验、批大小及端到端延迟测量协议。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Qwen3-VL-8B-Thinking 上比较无路由、词元熵路由与注意力比路由 | 在 MathVerse、WeMath、$M^3$CoT、ScienceQA 四项平均上，无路由 Explicit CoT 为 $67.3\%$、$1961$ 步；词元熵路由为 $70.7\%$、$864$ 步；本文注意力比路由达到 $74.7\%$、$815$ 步。相对词元熵，注意力比提高 $4.0$ 个百分点并再减少 $49$ 步；WeMath 上的差距最突出，为 $76.8\%$ 对 $68.9\%$。 | 该消融隔离的是“用什么信号决定显式/潜在模式切换”。两种路由都远少于全显式 CoT 的步数，说明模式切换本身能压缩推理；注意力比进一步提高平均正确率，支持作者关于词元熵会混合感知歧义与逻辑不确定性的主张。不过各路由是否使用完全匹配的阈值或切换预算，摘录没有展开，因此仍需结合全文核查控制变量。 | Table 3；列顺序为 MathVerse、WeMath、M³CoT、ScienceQA、Avg，每项依次为 Acc 与 Eff<br><span class="experiment-evidence">Explicit CoT (No Routing) \| 55.9 \| 2574 \| 62.9 \| 2489 \| 62.7 \| 1881 \| 87.5 \| 898 \| 67.3 \| 1961
Token Entropy \| 58.8 \| 1068 \| 68.9 \| 1001 \| 66.4 \| 850 \| 88.8 \| 535 \| 70.7 \| 864
Attention Ratio (Ours) \| 64.7 \| 1002 \| 76.8 \| 867 \| 67.4 \| 861 \| 89.8 \| 529 \| 74.7 \| 815</span> |
| $M^3$CoT 上显式推理维持窗口 $W$ 的敏感性 | 随着 $W$ 从 $64$ 增至 $512$，准确率由 $52.2\%$ 逐步升至最高的 $67.4\%$，生成步数则由 $209$ 增至 $861$；继续增至 $W=1024$ 后，步数升至 $1766$，准确率反而降至 $62.9\%$。因此默认值 $W=512$ 在所测候选中取得最高准确率，但不是最低成本点。 | 窗口 $W$ 规定切换后至少维持多长的显式推理。窗口过短时，模型可能缺少足够的离散文本来固定逻辑结构；窗口过长则接近冗长的显式 CoT，既增加成本，也可能重新引入重复文字化或误差累积。该实验只在一个基准和给定候选网格上进行，因而不能证明 $W=512$ 对所有模型与任务都最优。 | Table 4；列为 Window Size、M³CoT Acc、M³CoT Eff<br><span class="experiment-evidence">64 \| 52.2 \| 209
128 \| 58.9 \| 412
256 \| 63.6 \| 609
512 \| 67.4 \| 861
1024 \| 62.9 \| 1766</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces an attention-guided inference method that switches between explicit and latent multimodal reasoning to improve both accuracy and inference efficiency.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`e90c0cd685a89f2cfd753f1726e2d7a8c7b06290f234b97f29107a43b26bbf0c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
