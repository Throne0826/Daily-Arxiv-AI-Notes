---
title: "[论文解读] Think in Latent, Explain in Language: Self-Explainable Latent Reasoning"
description: "[arXiv 2608.13570][LLM Reasoning] SELR通过联合答案监督与思维链监督，使同一个模型既能在连续潜在空间中高效推理，又能将自身的潜在思维还原为人类可读的解释。"
arxiv_id: "2608.13570"
announcement_date: "2026-08-17"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-17T02:04:52.138046+00:00"
source_sha256: "ead7597b3f6c6da0962b663bf2dc6f3c3594e663667f3e8c4a11360c65f9f65e"
tags:
  - "LLM Reasoning"
  - "LLM 机制与可解释性"
  - "潜空间推理"
  - "连续思维"
  - "思维链"
  - "自解释推理"
  - "视觉语言模型"
  - "多任务学习"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.13570</p>

# Think in Latent, Explain in Language: Self-Explainable Latent Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Dayuan Zhao, Shengcao Cao, Yu-Xiong Wang, Liang-Yan Gui</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13570) · [PDF 下载](https://arxiv.org/pdf/2608.13570) · **关键词** 潜空间推理, 连续思维, 思维链, 自解释推理, 视觉语言模型, 多任务学习<br>
**项目页**: [https://jasondayuan.github.io/SELR/](https://jasondayuan.github.io/SELR/)

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

SELR通过联合答案监督与思维链监督，使同一个模型既能在连续潜在空间中高效推理，又能将自身的潜在思维还原为人类可读的解释。

**不用术语来说**：传统思维链要求模型把每一步推理都写成文字，其中不少词只是为了让语句连贯，因而增加生成成本；改用紧凑的内部表示进行推理虽然更省输出，但人无法直接看懂这些表示，也难以判断模型是否依据合理过程得到答案。现有解释方案还可能需要额外模型，使解释与真正参与答题的内部过程并非由同一主体生成。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出自解释潜在推理框架SELR，以多任务学习同时优化答案损失与思维链损失：前者要求潜在推理支持正确作答，后者要求同一模型把自身潜在表示解码为可读推理，从而将推理器和解释器统一在一个模型中。
- 作者声称首次把这种自解释潜在推理范式成功应用于视觉语言模型，并通过从轻量级语言模型到复杂视觉语言模型的实验，归纳可迁移的训练策略；其目标是在保持解释能力的同时兼顾准确率与令牌效率。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型与视觉语言模型的推理研究领域。传统文本思维链（CoT）要求模型逐词生成可读的中间推理，因此便于监督和检查，但大量词元只用于维持语言连贯性，推理成本较高，并受离散词表限制。潜空间推理则跳过中间文本生成，将模型上一轮的隐藏状态直接作为下一轮输入嵌入，使“思考”以连续向量迭代；这种表示能够更紧凑地承载信息，也与视觉模型中的连续图像表示更自然地衔接。然而，连续思维没有可由人直接编写的标准答案，且其内容无法直接阅读，因此该方向同时面临训练监督不足和推理过程不透明两个基础问题。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**文本思维链（Chain-of-Thought, CoT）**

模型在给出最终答案前，以自然语言逐步写出中间推理过程。它能提供人类可读的过程监督，但通常需要生成较多词元。

</div>
<div class="concept-item" markdown="1">

**潜空间推理（Latent-space Reasoning）**

模型不把每一步思考解码成文字，而是将隐藏状态作为“连续思维”反馈给自身，继续执行后续计算。通俗地说，模型直接传递内部向量，而不必先把内部信息翻译成句子。

</div>
<div class="concept-item" markdown="1">

**视觉语言模型（Vision-Language Model, VLM）**

能够联合处理图像与文本并生成文本回答的模型。由于图像通常先被编码为连续向量，潜空间推理可能减少视觉表示与离散文字之间反复转换造成的信息和计算开销。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定文本问题，或由图像与问题组成的多模态输入，模型需要先在连续潜空间中生成若干潜在思维，再输出最终文本答案；在需要审查推理时，还应由同一个模型接收这些潜在思维及解码提示，将其还原为人类可读的思维链。研究设定要求推理器与解释器共享同一模型，不能依赖独立的事后解码器；训练时可利用正确答案和文本思维链作为监督，其中前者约束任务正确性，后者约束潜在表示的语义可解释性。该设定隐含的关键要求是：解释必须来自实际用于作答的潜在轨迹，而不是由另一个模型在答案产生后重新编造一条看似合理的推理。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Coconut（Hao et al., 2025）**: Coconut通过把上一时刻的最后隐藏状态反馈为下一时刻输入，实现连续潜空间中的推理，并以多阶段课程学习逐步将文本思维链内化。它奠定了本文采用的连续思维范式，但潜在轨迹本身不可直接阅读；逐个寻找相似文本词元只能形成零散探测，不能给出连贯、易懂的过程解释。
- **Heima（Shen et al., 2025a）**: Heima通过分别训练用于压缩思维的编码器和用于解释潜在表示的解码器来提升可解释性，直接对应本文所处理的问题。其不足是额外模型带来参数与架构开销，而且解释器和实际推理器彼此分离，使生成的解释可能不能忠实反映真正驱动作答的推理逻辑；本文因此研究由单一模型同时承担潜空间推理与自我解释的设定。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

基于文字的思维链受离散词表约束，且会生成大量用于语言连贯而非实质推理的令牌；潜在推理把上一时刻的隐藏状态直接作为下一时刻的输入嵌入，可以用更少的连续表示承载更密集的信息，对需要衔接连续视觉表示与离散文字的视觉语言模型尤其有吸引力。然而，一旦推理被压缩到潜在空间，人类便失去了按需检查推理路径的直接手段，同时也没有可供人工标注的连续思维“标准答案”来训练这些内部表示。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **黑箱式潜在推理与渐进迁移方法（如Coconut）**：模型跳过中间文字生成，把最后隐藏状态作为“连续思维”反复送回模型；部分方法采用多阶段课程学习，逐步将推理过程从语言空间迁移到潜在空间。推理紧凑且可能更高效，但最终只输出答案，内部连续轨迹本身不可直接阅读。
- **潜在表示探测或事后解释方法（如逐令牌探测、Heima）**：逐令牌探测在语言嵌入空间中寻找与连续思维最相似的文字令牌；事后解释方法则另行训练一个解码器，把推理模型产生的潜在表示转换成自然语言说明。两者都在潜在推理完成后尝试恢复其语义。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 潜在思维没有人类可解释的连续表示真值，普通文字思维链监督无法直接施加到潜在轨迹；多阶段课程学习虽能完成空间迁移，但原文指出尚无公认的有效学习方案，因此潜在表示是否形成稳定、任务相关的推理结构仍缺乏直接约束。
- 逐令牌相似性探测只能孤立解释单个连续思维，难以形成连贯、易读的推理过程；独立事后解码器又增加参数与架构开销，而且解释器不同于实际推理器，存在生成的说明与真正决策逻辑脱节的风险。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未提供一种统一训练机制，使潜在轨迹同时满足三项要求：能够有效支持最终答案、能够从文本推理监督中获得结构性约束，并且无需外部解码器即可由原模型恢复为连贯解释。尤其在视觉语言模型中，原文认为此前还没有成功验证单模型自解释潜在推理的方案。

</div>
<div markdown="1"><span>核心问题</span>

能否用一个联合目标训练同一语言模型或视觉语言模型，使其生成紧凑且有利于正确作答的潜在思维，并在需要审查时自行把这些潜在思维翻译成人类可读的推理步骤，从而避免效率、准确性与可解释性之间的现有取舍？

</div>
<div markdown="1"><span>作者直觉</span>

答案监督只要求内部表示足以导向正确结果，因而可能容许难以理解甚至缺乏清晰语义结构的潜在轨迹；若再要求模型从同一轨迹重建对应的文字推理，文字思维链就会成为一种语义约束，迫使潜在表示保留可解码的推理信息。由于生成与解码共享同一个模型，模型既学习“怎样用内部表示答对”，也学习“怎样读懂自己的内部表示”，理论上可减少独立解释器造成的额外开销与逻辑错位。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SELR（Self-Explainable Latent Reasoning）的输入是图像与问题，输出包括最终答案以及可按需解码的人类可读推理链。模型先用视觉编码器和投影层把图像变成与文本嵌入同维度的序列，再以 <bot> 标记进入潜在推理阶段；此后不把隐藏状态映射为词表中的离散词，而是将每一步最后位置的隐藏状态直接作为下一步输入，形成连续向量序列 $E_{\mathrm{latent}}$。完成潜在推理后，模型附加 <eot>，一方面依据图像、问题和 $E_{\mathrm{latent}}$ 生成答案，另一方面仅依据 $E_{\mathrm{latent}}$ 将内部推理译回文本推理链。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多模态输入编码

视觉编码器 $\mathcal{V}$ 提取图像特征，投影层 $\mathcal{P}$ 将其映射到语言模型维度；嵌入矩阵 $\mathcal{E}$ 编码问题和 <bot>，再按顺序拼接为初始嵌入序列。

<div class="method-step__io" markdown="1">

**输入**：图像 $I$、问题词元序列 $X_q$，以及潜在推理起始标记 <bot>。<br>
**输出**：初始序列 $E=[\mathcal{P}(\mathcal{V}(I));\mathcal{E}(X_q);\mathcal{E}(\texttt{<bot>})]$。

</div>

**直观理解**：这一步把图像、问题和“开始思考”信号翻译成语言模型能够共同处理的一串向量。图像并未转成文字，而是被放进与文字相同的表示空间。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自回归潜在推理

每轮运行同一个语言模型，取最后位置隐藏状态 $h_{\mathrm{last}}$，绕过词表映射和离散采样，直接将其追加到输入序列；重复 $l_{\mathrm{latent}}$ 次并收集所有隐藏状态。

<div class="method-step__io" markdown="1">

**输入**：初始嵌入序列 $E$ 与潜在思考预算 $l_{\mathrm{latent}}$。<br>
**输出**：潜在思考序列 $E_{\mathrm{latent}}\in\mathbb{R}^{l_{\mathrm{latent}}\times d}$。

</div>

**直观理解**：普通生成要求模型每一步“说出一个词”，SELR 则允许模型把尚未语言化的连续向量继续传给自己。这样可以用很短的潜在序列承载较密集的推理信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 答案生成与任务监督

将原始输入、<bot>、潜在思考和 <eot> 拼成答案提示 $E_{\mathrm{ans}}^{\mathrm{prompt}}$，以自回归交叉熵训练模型预测真实答案；推理时则从同一上下文直接生成答案。

<div class="method-step__io" markdown="1">

**输入**：图像表示、问题表示、完整潜在思考 $E_{\mathrm{latent}}$、结束标记 <eot> 和真实答案 $X_a$。<br>
**输出**：答案分布及最终答案，同时得到答案损失 $L_{\mathrm{ans}}$。

</div>

**直观理解**：这一分支检查潜在向量是否真的能解决问题。若内部思考没有保留足够的视觉和问题信息，模型就无法正确预测答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 潜在思考自解释

Full CoT 模式用全部 $E_{\mathrm{latent}}$ 重建完整推理链；Single Step 模式抽取第 $i$ 个潜在思考并重建对应步骤 $X_{\mathrm{CoT}_i}$。生成潜在思考和执行解码的是同一个原始模型，没有额外训练独立解释器。

<div class="method-step__io" markdown="1">

**输入**：解码指令 $X_{\mathrm{dec}}$、潜在思考和标注推理链 $X_{\mathrm{CoT}}$；该分支不接收原图或原问题。<br>
**输出**：可读推理文本，以及全局解码损失 $L_{\mathrm{dec,full}}$ 或逐步解码损失 $L_{\mathrm{dec,step}}$。

</div>

**直观理解**：模型必须仅凭内部向量复述推理，因此不能在解释阶段重新查看题目并事后编造一套理由。该约束把潜在思考变成一个必须同时支持答题和解释的信息瓶颈。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 潜在思考递推

$$
\begin{aligned} E^{(0)}&=[\mathcal{P}(\mathcal{V}(I));\mathcal{E}(X_q);\mathcal{E}(\texttt{<bot>})],\\ H^{(k)}&=\operatorname{LLM}(E^{(k-1)}),\\ e_k&=H^{(k)}[-1,:],\qquad E^{(k)}=[E^{(k-1)};e_k],\\ E_{\mathrm{latent}}&=[e_1;\ldots;e_{l_{\mathrm{latent}}}]. \end{aligned}
$$

**符号说明**

- $I$：输入图像。
- $X_q$：问题的文本词元序列。
- $\mathcal{V},\mathcal{P},\mathcal{E}$：分别表示视觉编码器、视觉到语言空间的投影层和文本嵌入矩阵。
- $E^{(k)}$：完成第 $k$ 个潜在步骤后供下一轮使用的完整嵌入序列。
- $H^{(k)},e_k$：$H^{(k)}$ 是第 $k$ 轮语言模型隐藏状态序列，$e_k$ 是其最后位置状态，也是第 $k$ 个潜在思考。
- $l_{\mathrm{latent}},E_{\mathrm{latent}}$：$l_{\mathrm{latent}}$ 是潜在思考预算，$E_{\mathrm{latent}}$ 是按时间顺序收集的潜在思考序列。

<div class="equation-explanation" markdown="1">

**直观理解**：该递推的关键不是语言模型前向计算本身，而是把 $e_k$ 直接反馈为输入。模型因此在连续表示空间中自回归推理，不必在每个中间步骤生成可读词元。<br>
**原文位置**：第 3.2.1 节，Algorithm 1（Latent Space Reasoning Generation）

</div>

</div>

<div class="equation-block" markdown="1">

#### 答案与自解释联合目标

$$
\begin{aligned} E_{\mathrm{ans}}^{\mathrm{prompt}}&=[\mathcal{P}(\mathcal{V}(I));\mathcal{E}(X_q);\mathcal{E}(\texttt{<bot>});E_{\mathrm{latent}};\mathcal{E}(\texttt{<eot>})],\\ L_{\mathrm{ans}}&=-\frac{1}{|X_a|}\log p(X_a\mid E_{\mathrm{ans}}^{\mathrm{prompt}}),\\ L_{\mathrm{dec,full}}&=-\frac{1}{|X_{\mathrm{CoT}}|}\log p(X_{\mathrm{CoT}}\mid E_{\mathrm{dec,full}}^{\mathrm{prompt}}),\\ L_{\mathrm{dec,step}}&=-\frac{1}{|X_{\mathrm{CoT}_i}|}\log p(X_{\mathrm{CoT}_i}\mid E_{\mathrm{ans,step}}^{\mathrm{prompt}}),\\ L&=L_{\mathrm{ans}}+L_{\mathrm{dec}},\qquad L_{\mathrm{dec}}\in\{L_{\mathrm{dec,full}},L_{\mathrm{dec,step}}\}. \end{aligned}
$$

**符号说明**

- $X_a$：真实答案词元序列，$|X_a|$ 是其词元数。
- $X_{\mathrm{CoT}}$：由全部标注步骤拼接成的完整文本推理链。
- $X_{\mathrm{CoT}_i}$：第 $i$ 个标注推理步骤，$i$ 从样本的 $K$ 个步骤中抽取。
- $E_{\mathrm{dec,full}}^{\mathrm{prompt}}$：由解码指令、<bot>、完整潜在思考和 <eot> 构成的全局解码提示，不含原图与问题。
- $E_{\mathrm{ans,step}}^{\mathrm{prompt}}$：由解码指令、边界标记和单个潜在思考 $E_{\mathrm{latent}_i}$ 构成的逐步解码提示；名称沿用原文公式。
- $L_{\mathrm{ans}},L_{\mathrm{dec}}$：分别为答案负对数似然和所选 CoT 解码负对数似然；单阶段设置中二者权重均为 $1.0$。

<div class="equation-explanation" markdown="1">

**直观理解**：答案损失要求潜在思考对任务有用，解码损失要求它能被同一模型解释。两者联合优化可防止表示只会复述推理却不会答题，或只会输出答案却不携带可恢复的推理内容。<br>
**原文位置**：第 3.2.2 节 Answer Loss、第 3.2.3 节 CoT Loss，以及第 3.3.1 节 Single-Stage Methods

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练样本为 $(I,X_q,\{X_{\mathrm{CoT}_k}\}_{k=1}^{K},X_a)$。单阶段 SELR 使用固定 $l_{\mathrm{latent}}$，联合最小化 $L_{\mathrm{ans}}+L_{\mathrm{dec,full}}$，两个损失的权重均为 $1.0$。多阶段 LLM 在第一阶段设置 $l_{\mathrm{latent}}=K$，最小化 $L_{\mathrm{ans}}+L_{\mathrm{dec,step}}$，随后改用固定长度和 $L_{\mathrm{ans}}+L_{\mathrm{dec,full}}$；第一阶段的步骤索引 $i$ 可均匀采样，也可按 $p(i)=2^i/(2^{K+1}-1)$ 指数采样，使后部、通常更困难的推理步骤获得更高概率。多阶段 VLM 第一阶段相同，第二阶段仍使用答案损失与 Single Step Loss；这是因为 LLaVA-CoT-100k 的每个样本固定包含 summary、caption、reasoning 三步，即 $l_{\mathrm{latent}}=K=3$，位置一一对应仍然成立，而单步文本本身较长且信息密集。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 连续隐藏状态反馈模块**

在第 $k$ 个潜在步骤中，语言模型对当前嵌入序列做前向计算，并把最后隐藏状态直接追加为第 $k+1$ 步的输入嵌入；这一过程跳过语言模型头 $W$、Softmax 和词元采样。<bot> 与 <eot> 分别划定潜在推理的开始和结束。

> 直观理解：词表会迫使每一步都对应某个可读词，而连续反馈允许模型保留尚不适合用一句话表达的中间计算。它是 SELR 区别于普通文本思维链的核心机制。

**2. 共享式自解码模块**

SELR 用产生 $E_{\mathrm{latent}}$ 的同一 VLM 或 LLM 解码这些向量。Full CoT Loss 对齐整段潜在序列与完整推理链，Single Step Loss 则要求 $E_{\mathrm{latent}_i}$ 与 $X_{\mathrm{CoT}_i}$ 一一对应。

> 直观理解：推理者和解释者共享参数，可减少独立解码器对内部状态作错误转述的结构性风险。不过这种共享只提供解释忠实性的归纳偏置，并不等同于对因果忠实性的严格证明。

**3. 思考预算与课程训练模块**

固定长度训练令所有样本采用同一 $l_{\mathrm{latent}}$；可变长度训练令 $l_{\mathrm{latent}}=K$，其中 $K$ 是标注推理步骤数。多阶段训练先以可变长度和逐步对齐建立潜在步骤语义，再切换到固定长度进行精炼；LLM 第二阶段改用 Full CoT Loss，而 VLM 因其数据固定为三个长步骤，继续使用 Single Step Loss。

> 直观理解：第一阶段像逐句教模型每个内部向量应该表达什么，第二阶段再让模型在固定计算预算下压缩和组织这些信息。固定预算也避免测试时必须猜测何时停止思考。

**训练与推理**

训练时，模型先从图像和问题递推产生 $E_{\mathrm{latent}}$，再分别构造答案提示与 CoT 解码提示；梯度同时通过答案分支、解释分支和潜在递推过程更新同一模型。Single Step Loss 每次只监督一个抽样步骤，Full CoT Loss 则一次监督完整推理链；解码分支刻意移除原图和问题，迫使 $E_{\mathrm{latent}}$ 自身携带解决问题所需的上下文。对于纯 LLM，只需删除 $I$、$\mathcal{V}$、$\mathcal{P}$ 和图像嵌入，其余流程不变。

推理时，输入图像与问题后，模型在 <bot> 之后生成预定数量的潜在思考，随后附加 <eot> 并生成答案；若需要解释，再把潜在思考交给同一模型解码。固定长度模型直接使用训练设定的预算；可变长度模型因无法可靠学习自主生成 <eot>，测试时也必须外部指定固定预算。因真实步骤数 $K$ 在测试时未知，所谓“可变长度”只描述训练对齐方式，并不意味着推理时能够真正自适应停止。

**复现信息**

公平复现时最关键的是区分潜在长度的训练策略与测试预算：固定长度训练的模型在达到 $l_{\mathrm{latent}}$ 后停止；可变长度训练的模型仍需在测试时指定预算 $b$，即严格生成 $b$ 个潜在向量后再附加 <eot>。原文在表 7、表 8 的可变长度消融中，对每个基准从预算 $1$ 至 $5$ 中选取最高准确率，因此这些数字属于带有 oracle 预算选择的上界估计，不能视为无需调参的自适应推理结果。另一个必要细节是 Single Step Loss 依赖潜在位置与文本步骤的一一对应，通常只能配合 $l_{\mathrm{latent}}=K$；VLM 第二阶段能够继续使用它，是因为数据恰好固定为 $K=3$。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- VLM训练与解释质量评测使用LLaVA-CoT-100k：该数据集含约10万组图像—文本样本，每个样本提供summary、caption和reasoning三个推理阶段。解释质量实验按95%训练集、5%测试集重新划分；前者训练SELR，后者比较潜在思维解码文本与参考文本的相似性。
- VLM零样本评测覆盖六个互补基准：MMStar、MMBenchV1.1和MMVet主要检查通用视觉问答与推理；MathVista和AI2D检查数学、科学图示理解；HallusionBench检查事实错误或幻觉倾向。该组合用于判断压缩推理是否只在单一任务上有效，以及它是否损害需要长篇、多步输出的能力。
- LLM训练使用GSM8k-Aug，其中包含由GPT-4生成的38.5万道小学数学题；测试包括同分布的GSM8k，以及分布外的SVAMP、GSM-Hard和MultiArith。该设置同时检查训练域内数学推理和题型变化后的迁移能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**最终答案准确率（Accuracy）**

衡量模型给出的最终答案是否正确。VLM中MMVet和MathVista由GPT-4o评分，其余基准采用精确匹配；LLM四个数学基准均报告最终答案准确率。 （越高越好，因为它直接反映压缩后的推理是否仍能支持正确作答；但平均准确率可能掩盖MMVet等特定能力上的退化。）

</div>
<div class="metric-item" markdown="1">

**平均生成标记数（# Token）**

统计模型每次响应实际生成的全部输出标记，包括潜在特殊标记<bot>/<eot>和最终答案，不包括事后解码出的自然语言推理。它近似刻画自回归生成长度与推理预算。 （在准确率相当时越低越好，因为较短序列通常意味着更低的生成开销；但标记数本身不等同于实际延迟，且过度缩短可能损害长篇生成和多步推理。）

</div>
<div class="metric-item" markdown="1">

**解释相似度指标组**

BLEU-4、METEOR和ROUGE-L比较词或片段重合，BERTScore比较语义表示相似度，GPT-4o评分补充判断解码解释与参考summary、caption、reasoning的整体相似性。它们共同检查潜在表示能否恢复成人类可读文本。 （均为越高越好，因为高分表示解码文本更接近参考推理；但与参考文本相似不自动证明解释忠实反映了模型产生答案时的真实因果过程。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### VLM六基准平均准确率与生成长度

<div class="result-value" markdown="1">

作者报告SELR (Single)的平均准确率为63.72，比原始Qwen2.5-VL-3B-Instruct的62.86提高0.86个百分点；平均输出长度为15.72个标记，相对基模型的49.92个标记减少68.51%。多阶段版本进一步把平均长度降至约13个标记，但平均准确率略低于单阶段版本。

</div>

这说明SELR并非仅靠少输出内容换取效率：在该六基准宏观平均下，它可以同时缩短实际生成序列并保持小幅净增益。该结论是跨任务平均结果，不代表每项能力都改善；例如MMVet上SELR仍低于基模型，作者将其归因于多步数学和长篇生成受到压缩限制。

<div class="result-source" markdown="1">

来源：表1，VLM主结果

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

SELR (Single) 57.27 7.56 76.32 7.29 41.88 56.83 65.10 7.51 78.95 8.00 62.78 7.12 63.72 (+0.86) 15.72 (-68.51%)

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### LLM域内与分布外数学推理

<div class="result-value" markdown="1">

SELR (Multi)在GSM8k、SVAMP、GSM-Hard和MultiArith上分别达到42.46、49.67、9.78和81.67，全面高于SELR (Single)的35.03、46.33、8.04和70.00；相对Coconut，它也在四项测试上全部更高。与CoLaR相比则并非全面占优：SELR在GSM8k和GSM-Hard上较高，在SVAMP和MultiArith上较低。

</div>

多阶段训练对域内和域外题目均带来一致改善，支持课程设计有效，而不是只记住GSM8k风格。SELR仍明显落后于生成完整文本思维链的CoT-SFT，因此实验更支持“极短推理预算下具有竞争力”，而非“潜在推理在绝对准确率上优于文本思维链”。

<div class="result-source" markdown="1">

来源：表2，LLM主结果

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

SELR (Multi) 42.46 49.67 9.78 81.67

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 潜在思维的逐阶段自然语言解码质量

<div class="result-value" markdown="1">

以summary解码为例，SELR (Multi, Uniform)的BLEU-4、METEOR、ROUGE-L、BERTScore和GPT-4o得分分别为19.95、45.05、44.60、77.19和4.30，均高于Heima对应的15.9、40.1、41.6、73.4和4.1。表3还显示SELR在caption阶段的五项指标均高于Heima；reasoning阶段总体优势较小，且不同SELR变体并非在每个自动指标上都占优。

</div>

结果支持同一SELR模型能够把内部潜在状态恢复为接近参考推理的文字，且不需要Heima那样为三个阶段分别配置大型解码器。不过，这里主要测量解码文本与标注文本的相似性，只能证明可读性和内容接近程度，不能单独证明解码文本就是模型作答时实际采用的推理路径。

<div class="result-source" markdown="1">

来源：表3，Summary解码质量

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

SELR (Multi, Uniform) 19.95 45.05 44.60 77.19 4.30

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

- 原始骨干与普通监督微调：VLM使用Qwen2.5-VL-3B-Instruct及其LLaVA-CoT-100k微调版本；LLM使用在真实文本思维链和答案上训练15轮的CoT-SFT。它们分别回答“相对未经适配的模型是否有收益”和“潜在推理相对完整文本推理牺牲了多少性能”。
- Heima：基于同一Qwen2.5-VL-3B-Instruct骨干重新实现的VLM潜在推理方法。它还为summary、caption和reasoning分别训练解码器，因此是比较推理压缩、答案性能及潜在表示可解释性的直接基线。
- Coconut：基于同一LLaMA-3.2-1B-Instruct骨干，通过逐步把文本思维链替换为潜在思维进行训练；作者使用其原始代码重新训练15轮。它检验SELR相对于典型纯潜在推理课程学习方法的效果。
- CoLaR：通过辅助预测目标把连续多个推理标记压缩为单个潜在嵌入；实验采用其已报告的最佳结果和测试时压缩因子2。它代表准确率较强但推理序列相对更长的潜在压缩方法，不过其结果来自论文报告而非本文统一重训。

**实验想回答的问题**

- 在相同骨干模型下，SELR能否用少量潜在标记替代显式思维链，在视觉语言与数学推理任务中维持或提高答案准确率，同时显著缩短模型实际生成的序列？
- SELR内部的潜在思维能否由同一模型解码为与参考推理相似的自然语言解释，以及多阶段训练、逐步解码和潜在长度等设计是否确实带来增益？

**实验实现**

VLM以Qwen2.5-VL-3B-Instruct为骨干，SELR各变体训练3轮；LLM以LLaMA-3.2-1B-Instruct为骨干，单阶段训练10轮，多阶段先训练10轮、再训练5轮。模型主要通过LoRA微调，并使用AdamW；VLM统一零样本评测由VLMEvalKit执行。LLM主实验固定使用6个潜在标记，以便与Coconut保持一致。公平性方面，多数比较共享骨干，但CoLaR采用其论文最佳报告值，Heima的训练课程和解码架构也与SELR不同，因此不能把所有差异完全归因于单一组件。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 潜在序列长度设为2、4、6或8 | 在仅训练2轮的SELR (Single)消融中，长度6在GSM8k、SVAMP和GSM-Hard上分别取得31.69、47.67和7.96，为四种长度中的最高值；MultiArith则随长度增加继续改善，长度8达到70.00，高于长度6的61.11。 | 该实验隔离了潜在推理预算：长度2或4容量不足，而从6增加到8没有在多数数据集上继续获益，因此作者选择6作为总体折中并与Coconut对齐。但MultiArith的例外说明“长度6最优”不是普遍规律，较长或步骤更多的题目可能仍受益于额外潜在容量；此外，该消融只训练2轮，不能保证与主实验充分训练后的排序完全一致。 | 表12及附录D，Latent Length Ablation<br><span class="experiment-evidence">Latent Length 2 4 6 8; GSM8k 18.12 22.74 31.69 31.54; SVAMP 36.33 39.67 47.67 47.33; GSM-Hard 4.40 5.84 7.96 7.20; MultiArith 36.67 48.33 61.11 70.00</span> |
| 完整CoT联合解码损失与逐阶段Single Step Loss | 单阶段完整序列解码的BLEU-4、METEOR、ROUGE-L、BERTScore和GPT-4o分别为19.72、38.88、38.04、70.01和3.25；多阶段指数版本对应为20.10、39.32、38.32、69.92和3.46。逐阶段训练改善了BLEU-4、METEOR、ROUGE-L和GPT-4o，但BERTScore略降0.09。 | 该对照主要检验VLM中把summary、caption和reasoning分别对齐、再拼接成完整CoT，是否比一次解码整段推理更容易学习。多数指标的小幅提升支持逐步监督，但增益并不大且BERTScore没有改善，因此更合理的结论是逐阶段损失提供了稳定但有限的解码优势，而不是所有相似度维度上的绝对提升。 | 表4，Full CoT Loss vs. Single Step Loss<br><span class="experiment-evidence">SELR (Single) 19.72 38.88 38.04 70.01 3.25; SELR (Multi, Exponential) 20.10 39.32 38.32 69.92 3.46</span> |

**定性案例**

- 附录B图4展示了一个反例：解码出的CoT本身正确，但模型直接答案错误。作者据此将其视为不忠实解码；分析上，这说明SELR的自解释机制能够产生连贯、甚至正确的事后文字，却不保证该文字与最终答案之间存在真实因果一致性。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：研究潜空间推理及其语言化自解释机制，同时涉及推理能力与过程可解释性。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`ead7597b3f6c6da0962b663bf2dc6f3c3594e663667f3e8c4a11360c65f9f65e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
