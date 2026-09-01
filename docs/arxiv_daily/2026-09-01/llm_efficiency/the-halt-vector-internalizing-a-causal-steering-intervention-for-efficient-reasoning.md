---
title: "[论文解读] The Halt Vector: Internalizing a Causal Steering Intervention for Efficient Reasoning"
description: "[arXiv 2608.28859][LLM 效率] 原文未明确报告。"
arxiv_id: "2608.28859"
announcement_date: "2026-09-01"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:35:30.474353+00:00"
source_sha256: "defe37aa1535e7c241f1896620c7459cfb5073f047698f0db12bc4630b33a7ad"
tags:
  - "LLM 效率"
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "高效推理"
  - "过度思考"
  - "思维链"
  - "强制作答点"
  - "停止向量"
  - "均值差方向"
  - "激活引导"
  - "因果可解释性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.28859</p>

# The Halt Vector: Internalizing a Causal Steering Intervention for Efficient Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Dylan Jayabahu, Tinuade Adeleke</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Waterloo</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28859v1) · [PDF 下载](https://arxiv.org/pdf/2608.28859v1) · **关键词** 高效推理, 过度思考, 思维链, 强制作答点, 停止向量, 均值差方向, 激活引导, 因果可解释性<br>
**代码**: [https://github.com/dylanjayabahu/halt-vector](https://github.com/dylanjayabahu/halt-vector)

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

本文研究大语言模型的高效推理与因果表征干预。以 DeepSeek-R1-Distill-Qwen-7B 为代表的推理模型通常先在 `<think>` 与 `</think>` 之间生成长篇思维链，再给出最终答案；思维链虽能提高数学解题准确率，但模型可能在已经具备正确作答能力后继续复核、重推，甚至把正确结论改错。本文关注的不是统一压缩所有回答，而是识别每道题各自“已经会答但尚未停止”的可删减区间，并研究能否把控制停止行为的内部方向写入模型权重，使模型在不依赖推理时外部监控信号的情况下自适应地缩短思考。研究对象固定为具有 28 层、约 70 亿参数的 DeepSeek-R1-Distill-Qwen-7B，核心分析发生在其残差流激活空间。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**强制作答点（forced-answer point）**

在思维链的某个前缀后人工补上结束思考和最终答案提示，让模型以贪心解码立即作答；最早能够答对的位置记为 $B_{\text{end}}$。它用于离线衡量模型何时已经具备正确作答能力，而不是部署时可直接获得的停止信号。

</div>
<div class="concept-item" markdown="1">

**均值差方向（difference-of-means direction）**

分别计算某层中“之前”与“之后”两组 token 激活的平均值，再以两者之差构造一个向量方向。若该方向确实编码某种状态，激活在其上的投影可用于读取该状态，沿该方向施加干预则可检验其是否具有因果作用。

</div>
<div class="concept-item" markdown="1">

**激活引导（activation steering）**

在模型前向计算时沿特定内部方向修改隐藏激活，观察生成行为是否随干预强度系统变化。与仅凭相关性训练分类探针不同，引导实验可测试某个内部特征是否能够直接控制停止、置信度或文本长度。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道数学题，模型先自由生成思维链，再输出最终答案；目标是在准确率和正常终止能力不劣于基础模型训练噪声范围的前提下，减少已经没有必要的思考 token。为得到离线监督依据，作者在推理轨迹的不同前缀处强制模型作答并用 `math_verify` 判分，以最早正确前缀 $B_{\text{end}}$ 界定可删减余量；若 $B_{\text{end}}$ 后仍有大量思考，该题称为可压缩问题，否则称为锚点问题。作者进一步在每层残差流中比较回答锁定前后的 token 位置，构造停止向量，并以 Jiang 等人的价值轴作为近正交控制方向。这里必须区分“何时可以安全停止”与“什么内部变量能够驱动停止”：$B_{\text{end}}$ 回答前者，但依赖标准答案且只能离线计算；停止向量旨在提供后者，其有效性最终需要通过因果引导而非方向分类 AUROC 来判断。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$B_{\text{end}}$**

强制作答已经正确的最早思维链前缀位置；其后的 token 在原则上构成可删减余量。

</div>
<div class="notation-item" markdown="1">

**$h^{(\ell)}_{c,t}$**

对比项 $c$ 在 token 位置 $t$、网络第 $\ell$ 层的残差流激活向量。

</div>
<div class="notation-item" markdown="1">

**$a^{(\ell)}$**

第 $\ell$ 层中，“之后”位置平均激活减去“之前”位置平均激活所得的未归一化均值差方向。

</div>
<div class="notation-item" markdown="1">

**$\hat{u}^{(\ell)}$**

将 $a^{(\ell)}$ 除以其范数后得到的单位方向，用于计算投影和实施激活引导。

</div>

</div>

**直接相关的工作**

- **Jiang et al. (2026) 的 value axis**: 该工作从上下文强化学习猜测游戏中构造线性价值轴，并报告其引导可调节置信度、自我纠正和冗长度。本文复现这一均值差构造，将价值轴作为控制方向，并另行从数学推理中回答锁定前后的激活构造停止向量；两者近乎正交，且价值轴在本文模型上不能控制数学推理的停止。
- **DeepSeek-R1-Distill-Qwen-7B（Guo et al., 2025）**: 它是本文唯一使用的基础推理模型，具有约 70 亿参数和编号为 0 至 27 的 28 层。本文在该模型的思维链、强制作答行为及残差流激活上定义问题和构造停止方向，因此结论首先适用于这一具体模型，而非所有推理模型。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法将一个原本只能在推理时施加的因果干预，内化为模型参数中的自适应停止能力。首先在 DeepSeek-R1-Distill-Qwen-7B 的第 18 层残差流中，用模型答案概率锁定前后的推理位置构造 halt vector；随后不直接最大化激活在该方向上的标量投影，而是训练一个注意力层 LoRA 适配器，使整个位于第 18 层的激活接近“自然的非目标维度 + 受控的 halt-vector 分量”。推理时，模型根据每道题的内部状态逐渐达到停止条件，适配器在答案已经可被可靠推出的位置促使模型提交答案，从而在不增加服务时开销的情况下减少可删除的思考尾部。直观地说，作者不是给模型装一个按固定长度剪枝的计时器，而是把“我已经想够了”的内部开关写进模型，同时尽量不改变读出答案所需的其他神经表示。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造可验证的停止位置

对推理前缀逐点截断，在末尾加入答案格式提示，让模型贪心生成最终答案，并用 math_verify 判断其是否正确；定义 $B_{\mathrm{end}}$ 为最早能被强制得到正确答案的前缀位置。该位置将推理划分为答案尚不可验证的部分与原则上可删除的 slack 部分。

<div class="method-step__io" markdown="1">

**输入**：基础模型在数学题上的完整自由运行推理轨迹、每个位置的隐藏状态，以及题目的标准答案。<br>
**输出**：每道题的 $B_{\mathrm{end}}$、可压缩样本与无明显 slack 的 anchor 样本，以及用于构造方向的 before/after 位置集合。

</div>

**直观理解**：作者不把“模型对答案的信心”直接当作停止信号，而是实际把模型强制要求回答，再检查答案是否正确。这样得到的是一个离线的安全参照点：在这里之后的思考理论上可以删掉，但它不能直接作为部署时的传感器。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 学习 halt vector 并选择干预层

对每个候选层计算 after 与 before 激活均值之差并归一化，得到 halt vector；用余弦投影评估它能否区分锁定后的晚期推理位置。作者在第 6、12、18、24 层比较干预效果，并以第 18 层作为主要控制位置；同时用来自 guessing-game 对比的 value axis、随机方向和幅度匹配方向作特异性控制。

<div class="method-step__io" markdown="1">

**输入**：训练题上的第 $\ell$ 层残差流激活，以及 $B_{\mathrm{end}}$ 前后的 think-token 位置。<br>
**输出**：第 18 层的单位方向 $\hat{u}^{(18)}$、方向幅度参考 $\lVert\bar{h}\rVert$，以及用于训练的按位置 steering schedule $s(t)$。

</div>

**直观理解**：可以把 halt vector 看成“模型从继续推理转向提交答案时，内部状态共同改变的方向”。重要的不是它单独能否识别状态，而是沿这个方向推动模型后，模型是否真的会更早停止；因此作者用因果 steering 而不是只看分类准确率来确认它。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 重构完整受控激活并训练适配器

为每个 think-token 构造目标激活 $h^*(t)$：保留基础激活作为非 halt 方向的自然值，只加入按 schedule 控制的 halt-vector 分量；以语言模型损失加归一化激活重构损失训练注意力-only LoRA，主要配置为层 0 至 18、$\alpha=25$、损失权重 $\lambda=1$、24 道题、12 个 epoch。该重构目标避免仅约束一个标量投影所造成的 off-axis 漂移。

<div class="method-step__io" markdown="1">

**输入**：基础模型激活 $h_{\mathrm{base}}(t)$、halt vector $\hat{u}$、停止位置 $B_{\mathrm{end}}$、目标 steering 强度 $\alpha$，以及完整推理轨迹。<br>
**输出**：一个内化 halt vector 的模型适配器，使模型在不同题目接近各自可停止位置时改变其后续生成行为。

</div>

**直观理解**：如果只要求某个坐标变大，模型可能为了达到这个数值而随意扭曲其他坐标，冻结的下游模块就会读错信息。作者因此要求整个隐藏向量都像一次安全的 steering 结果：只改变停止方向，其余部分尽量保持原样。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 部署时自适应生成与评估

正常逐 token 生成，不使用 serving-time hook、额外置信度探针或强化学习；适配器依据当前推理状态逐渐施加内化的停止倾向，使模型在题目自身的可删除 slack 处提交答案。对比基础模型、长度惩罚、截断、DEER 等方法，报告答案正确率、think-token 数量、终止率，并检查跨 benchmark、随机种子和难度的稳定性。

<div class="method-step__io" markdown="1">

**输入**：未见过的数学题、内化后的模型，以及可选的常规贪心解码。<br>
**输出**：每题的最终答案、思考长度与是否生成结束标记，以及压缩—准确率折衷和每题 slack-to-cut 适应性指标。

</div>

**直观理解**：部署时不需要另一个程序持续监视模型，也不需要为每道题预先设定同一个长度。模型像原来一样生成，但参数中已经包含了停止机制，因此节省的是推理过程本身，而不是事后把文本硬截短。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 差分均值 halt vector

$$
a^{(\ell)}=\frac{1}{|C|}\sum_{c\in C}\left(\frac{1}{|T^{c}_{\mathrm{post}}|}\sum_{t\in T^{c}_{\mathrm{post}}}h^{(\ell)}_{c,t}-\frac{1}{|T^{c}_{\mathrm{pre}}|}\sum_{t\in T^{c}_{\mathrm{pre}}}h^{(\ell)}_{c,t}\right),\qquad \hat{u}^{(\ell)}=\frac{a^{(\ell)}}{\lVert a^{(\ell)}\rVert}
$$

**符号说明**

- $C$：用于构造对比方向的样本集合。
- $\ell$：模型层编号。
- $h^{(\ell)}_{c,t}$：样本 $c$ 在 token 位置 $t$、第 $\ell$ 层的残差流激活。
- $T^{c}_{\mathrm{pre}}$：样本 $c$ 中锁定点之前的推理位置集合。
- $T^{c}_{\mathrm{post}}$：样本 $c$ 中锁定点之后的推理位置集合。
- $a^{(\ell)}$：未归一化的 after-minus-before 均值差方向。
- $\hat{u}^{(\ell)}$：归一化后的方向，用于读取投影或施加 steering。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把每道题锁定点前后的隐藏状态分别求平均，再跨题求差，得到从“继续想”到“准备结束”的共同变化方向。归一化后，方向长度不再影响比较，后续只需由 steering 强度决定推动多少。<br>
**原文位置**：第 3 节 Background，Equation (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 全激活重构训练目标

$$
h^{*}(t)=h_{\mathrm{base}}(t)+s(t)\,\frac{\alpha}{100}\,\lVert\bar{h}\rVert\,\hat{u},\qquad \mathcal{L}=\mathcal{L}_{\mathrm{LM}}+\lambda\cdot\frac{1}{|T_{\mathrm{think}}|}\sum_{t\in T_{\mathrm{think}}}\frac{\lVert h(t)-h^{*}(t)\rVert^{2}}{\left(\frac{\alpha}{100}\lVert\bar{h}\rVert\right)^{2}}
$$

**符号说明**

- $h^{*}(t)$：位置 $t$ 的目标第 18 层激活。
- $h_{\mathrm{base}}(t)$：关闭适配器时基础模型在位置 $t$ 的激活，负责保留自然的非 halt 方向信息。
- $s(t)$：按位置变化的 steering schedule，在 $B_{\mathrm{end}}$ 附近达到峰值。
- $\alpha$：steering 强度百分比，例如主要实验使用 25。
- $\lVert\bar{h}\rVert$：基础模型第 18 层 think-token 激活范数的均值，用作固定尺度参考。
- $h(t)$：启用适配器后模型在位置 $t$ 的实际激活。
- $\mathcal{L}_{\mathrm{LM}}$：完整推理轨迹上的普通语言模型损失。
- $T_{\mathrm{think}}$：参与激活重构损失的 think-token 位置集合。
- $\lambda$：激活重构损失相对于语言模型损失的权重。

<div class="equation-explanation" markdown="1">

**直观理解**：第一式只沿 halt vector 添加受控分量，并把其他维度固定为基础模型原值；第二式要求训练后的激活接近这个完整目标，同时保持正常语言建模能力。这样优化的不是一个容易被投机达到的标量，而是一个下游读出器可以安全使用的完整隐藏状态。<br>
**原文位置**：第 5 节 Reconstructing the whole steered activation，Equations (4)–(5)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优化目标由两部分组成：普通语言模型损失 $\mathcal{L}_{\mathrm{LM}}$ 保持推理与答案生成能力，激活重构损失约束启用适配器后的第 18 层隐藏状态接近目标 $h^*(t)$。重构项在 think-token 上按 steering 幅度归一化，并由 $\lambda$ 加权；其核心作用是同时实现指定的 halt-axis 位移与 off-axis 保真，而不是单独追求余弦投影或某个停止 token 的概率。训练不使用强化学习，主要模型从 24 道题拟合；作者另以更大数据量研究单次训练的 erosion 与 burst-merge，但主要结论依赖 24-problem adapter。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 强制答案测量器**

对前缀加入 "$\n</think>\n\n**Final$ answer:** $\boxed{" 等答案 scaffold，贪心生成后通过 math_verify 判定正确性，最早正确前缀定义为 $$B_{\mathrm{end}}$$。该测量只用于离线构造训练目标与评估可压缩 slack，不作为推理时的直接预测信号。

> 直观理解：它像一个离线裁判：把模型在不同思考时刻叫停并要求交卷，找出最早已经能答对的时刻。这样可以避免仅凭首个答案 token 的概率误判，因为格式先验可能让概率很高，但模型实际上还没有形成正确答案。

**2. 第 18 层 halt-vector 干预**

halt vector 是锁定后与锁定前残差流均值的差分方向，记为 $\hat{u}^{(18)}$；在该层的 steering 强度控制停止倾向。value axis 与随机方向的幅度匹配实验不产生相同长度效应，说明效果依赖于方向语义而非一般性的残差扰动。

> 直观理解：这是一个方向性开关，而不是简单地把所有神经元激活放大或缩小。沿正确方向推动会让模型进入更接近“已经准备提交”的状态，沿无关方向则不会稳定地缩短推理。

**3. 全向量重构 LoRA**

适配器以第 18 层完整激活为训练对象，而不是只优化 $\hat{u}^{(18)}\cdot h$；目标复制基础模型的 off-axis 分量，并只注入 schedule 控制的 on-axis 分量。采用注意力-only LoRA，覆盖层 0 至 18，以限制写入激活时对冻结下游读出器的破坏。

> 直观理解：下游网络需要隐藏状态中的全部信息来继续推理和写答案，所以训练时既要告诉模型“停止方向要变”，也要告诉它“其他信息不要乱动”。这解释了为什么看似更简单的标量投影目标反而会导致更长、循环或完全不结束的生成。

**训练与推理**

训练阶段先在基础模型上获得正确 rollout 与 $B_{\mathrm{end}}$，再用锁定点前后位置构造第 18 层 halt vector；为每个训练 token 生成受 schedule 控制的完整激活目标，并训练层 0 至 18 的 attention-only LoRA，使语言模型损失与重构损失共同下降。主要配置为 steering strength $\alpha=25$、$\lambda=1$、12 个 epoch、seed 17 和 24 道题，同时用 seed 0、42 检查稳定性；训练时的 $B_{\mathrm{end}}$ 是离线、依赖标准答案的教师信号。

**复现信息**

基础模型为 7B、28 层的 DeepSeek-R1-Distill-Qwen-7B，主要干预第 18 层；训练问题与离线池来自 DeepScaleR，评估使用 MATH500、AMC、AIME 2024 和 AIME 2025 等未见 benchmark。推理不需要 serving-time hook、外部 probe 或强化学习流程；应将结果理解为把 steering 机制写入权重，而不是声称在原始压缩—准确率前沿上超过精调长度惩罚或 DEER。评估时需同时关注 think-token 数、math_verify 准确率、生成闭合率及每题自适应性，因为单纯减少长度可能来自错误答案、截断或非终止行为。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 训练集由 24 个可压缩问题组成，用于拟合 halt adapter；原文未明确报告这些问题来自哪个数据集、如何筛选及是否设置独立验证集。
- 泛化评测覆盖五个训练时未见的基准，用于检验推理压缩能否迁移到新问题；所给章节未列出五个基准的名称、规模和逐基准结果。
- 难度分层的非终止评测用于观察模型无法结束推理的病理现象是否随问题难度加重，以及 halt 方法能否缓解该现象；具体数据集和分层规则原文摘录未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率**

模型最终答案正确的比例，用于检查减少思维过程后是否保留任务能力。 （越高越好；但本文主要比较在准确率基本持平时能减少多少推理计算。）

</div>
<div class="metric-item" markdown="1">

**think-tokens**

生成链式思维所消耗的 token 数，是推理长度与生成计算成本的代理指标。 （在准确率不下降或仅有可接受变化的前提下越低越好。）

</div>
<div class="metric-item" markdown="1">

**终止率**

生成能够在预算内正常结束的比例，用于识别模型持续推理而不停止的病理行为。 （越高越好，因为更高的终止率表示较少出现超长生成或无法结束。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 在 24 个可压缩训练问题上，以未修改模型作为参照。

<div class="result-value" markdown="1">

基础模型准确率为 0.812，平均使用 6,516 个 think-tokens，终止率为 0.95。

</div>

这些数值建立了训练问题上的成本与能力基线，说明即使答案准确率较高，模型仍会生成较长的推理过程，而且并非每次都能正常终止。该结果本身不证明 halt 方法有效，只规定了后续压缩必须比较的起点。

<div class="result-source" markdown="1">

来源：第 6.1 节；附录表 11

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We fit 24 compressible problems with a LoRA adapter and no reinforcement learning; the base model scores 0.812 accuracy at 6,516 think-tokens with 0.95 termination (Table 11, in the appendix).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 仅用 24 个问题拟合 halt，并在五个训练时未见的基准上评测。

<div class="result-value" markdown="1">

作者报告，在准确率保持不变的条件下，halt 大约减少四分之一的思维过程。

</div>

这表明权重内化后的干预并非只记住 24 个训练问题，而能在多个未见基准上减少冗余推理。这里的“held accuracy”支持的是总体准确率与基础模型相近，而不是保证每个数据集、每类难度或每个样本都完全无损；所给材料也未提供逐基准分数与不确定性。

<div class="result-source" markdown="1">

来源：摘要；五个未见基准的汇总结果

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Fit from 24 problems and no reinforcement learning, the halt removes about a quarter of the thinking at held accuracy across five unseen benchmarks, and the cut tracks each problem's own removable slack at 0.70.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 比较每个问题实际减少的推理量与该问题自身可移除的冗余空间。

<div class="result-value" markdown="1">

二者的相关程度报告为 0.70。

</div>

这一结果支持 halt 的压缩幅度具有样本自适应性：冗余更多的问题通常被削减得更多，而不是对所有问题施加同一个长度上限。这比单纯报告平均 token 降幅更能回应论文动机，但相关性不等于因果证明，也不能说明所有问题都被精确压缩到最优长度。

<div class="result-source" markdown="1">

来源：摘要；按问题分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Fit from 24 problems and no reinforcement learning, the halt removes about a quarter of the thinking at held accuracy across five unseen benchmarks, and the cut tracks each problem's own removable slack at 0.70.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 作者明确不主张该方法在原始准确率—推理长度权衡上优于经过充分调参的长度惩罚或解码时早停；贡献主要是把因果可解释性干预稳定地内化到模型权重，因此不能据此认定它是所有效率方案中的最佳选择。
- 现有证据集中于 DeepSeek-R1-Distill-Qwen-7B、第 18 层方向、24 个拟合问题和五个未见基准。所给章节未明确列出各基准名称、逐任务结果、方差或显著性，也未证明该方向和重构目标能直接迁移到其他模型规模、架构或更广泛任务。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 未修改的 DeepSeek-R1-Distill-Qwen-7B，提供准确率、思维 token 数和终止率的参照，用于判断压缩是否以损害任务能力为代价。
- 最大化激活在 halt direction 上标量投影的训练目标，用于检验只增强目标方向是否足以把因果 steering 内化进权重。
- 复制实验得到的 value axis steering，用作方向特异性对照：如果该轴不改变推理长度，而 halt vector 可以，则效果不太可能只是任意激活扰动造成的。
- 全局长度惩罚与解码时置信度钩子，分别代表统一压缩生成长度和依据当前置信度提前退出的替代方案；论文明确表示其重点不是在原始准确率—长度权衡上击败经过良好调参的替代方法。

**实验想回答的问题**

- 将因果干预得到的 halt vector 通过 LoRA 内化到模型权重后，能否在基本保持推理准确率的同时，按样本自适应地减少不必要的思维 token，并改善正常终止率？
- 完整重构被 steering 后的激活，是否比仅最大化 halt 方向投影、使用无效的 value axis 或采用解码时置信度钩子更可靠？

**实验实现**

实验对象为 DeepSeek-R1-Distill-Qwen-7B。作者在第 18 层使用 difference-of-means 得到的 halt vector，并以 24 个可压缩问题拟合 LoRA adapter，不使用强化学习。核心训练目标不是只增大激活沿 halt direction 的投影，而是重构完整的 steering 后激活，同时把与该方向正交的维度约束在其自然取值附近，避免破坏冻结下游网络依赖的信息。评测同时报告答案准确率、思维 token 数与正常终止情况，并在五个未见基准上测试迁移；所给原文未明确报告采样次数、解码参数、LoRA 超参数、统计显著性检验或置信区间。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 将完整 steered-activation 重构目标替换为仅最大化激活在 halt direction 上的标量投影。 | 投影目标破坏了下游读取器依赖的非目标方向信息，生成不但没有缩短，反而变长；完整重构则是作者报告唯一能够在保持准确率时实现压缩的目标。 | 该对照隔离了“增强 halt 分量”和“保持其余表示结构”之间的差别。结果说明一个方向在推理时具有因果 steering 效果，并不意味着训练时只增大该方向的投影就能安全复现效果；权重更新还必须保护正交维度中承载的任务信息。 | 摘要；第 6.1 节提及目标函数比较，详细结果位于附录 A<br><span class="experiment-evidence">Maximizing the scalar projection onto the direction corrupts the off-axis dimensions a frozen downstream reader depends on, and generation gets longer instead of shorter; what works is reconstructing the whole steered activation with those dimensions pinned to their natural values.</span> |
| 以复制得到的 value axis 代替第 18 层 halt vector 进行 steering。 | halt vector 的 steering 强度能够控制模型思考时长，而复制的 value axis 对推理长度没有作用。 | 该方向对照检验效果是否来自任意激活扰动。value axis 无效而 halt vector 有效，支持长度控制与所发现方向的语义或因果作用有关；但所给材料没有报告该消融的具体数值、误差范围或跨层结果。 | 摘要；第 18 层方向干预实验<br><span class="experiment-evidence">The mechanism is a halt vector: a difference-of-means direction at layer 18 of this model whose steering strength controls how long it thinks, while a replicated value axis does nothing.</span> |

**定性案例**

- 在难度增加时，基础推理模型更容易出现持续生成而无法正常终止的行为；作者称权重内化的 halt 能消除这一病理趋势，而解码时置信度钩子会使其恶化。该案例说明“当前答案概率已经稳定”不一定能直接转化为可靠的解码时停止规则，但所给原文未展示具体样本、难度分组数值或完整生成轨迹。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work uses a causally identified internal activation direction to shorten LLM reasoning while preserving accuracy, combining mechanistic interpretability with reasoning-efficiency optimization.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`defe37aa1535e7c241f1896620c7459cfb5073f047698f0db12bc4630b33a7ad`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
