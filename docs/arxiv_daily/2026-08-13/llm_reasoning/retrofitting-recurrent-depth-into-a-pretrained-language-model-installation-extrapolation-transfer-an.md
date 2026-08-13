---
title: "[论文解读] Retrofitting Recurrent Depth into a Pretrained Language Model: Installation, Extrapolation, Transfer, and Retention at Two Parameter Budgets"
description: "[arXiv 2608.11233][LLM Reasoning] 本文研究能否在不从头训练、尽量保留原有通用能力的前提下，把预训练稠密语言模型改造成可反复调用同一组参数、在隐状态中逐步推理的循环深度模型。"
arxiv_id: "2608.11233"
announcement_date: "2026-08-13"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:51:31.653432+00:00"
source_sha256: "a4d74e4e777ba29f2454e685ba9d6ec1ba3fb7524506136ea8821c2fb33be951"
tags:
  - "LLM Reasoning"
  - "循环深度"
  - "预训练语言模型改造"
  - "权重共享"
  - "潜空间迭代计算"
  - "低秩适配"
  - "深度外推"
  - "能力保留"
  - "分布偏移"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.11233</p>

# Retrofitting Recurrent Depth into a Pretrained Language Model: Installation, Extrapolation, Transfer, and Retention at Two Parameter Budgets

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Mark Shapiro</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11233v1) · [PDF 下载](https://arxiv.org/pdf/2608.11233v1) · **关键词** 循环深度, 预训练语言模型改造, 权重共享, 潜空间迭代计算, 低秩适配, 深度外推, 能力保留, 分布偏移<br>


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

本文研究能否在不从头训练、尽量保留原有通用能力的前提下，把预训练稠密语言模型改造成可反复调用同一组参数、在隐状态中逐步推理的循环深度模型。

**不用术语来说**：普通 Transformer 若想增加解题计算量，通常只能预先堆叠更多层，或在回答时生成更多推理文本；前者增加模型参数，后者增加输出长度与推理时间。作者希望给现成的指令微调模型安装一种“内部重复思考”能力：模型反复更新内部表示，每次循环完成一步计算，同时在只运行一次循环时仍尽可能保持原模型行为。但仅把已有网络层重复执行并不可行，因为这些层会接收到偏离预训练分布的中间状态，迭代还可能越过已经正确的答案，并且后续训练可能抹除已学会的循环机制。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出一个需要实证回答的安装问题：同一套保持单循环原模型路径的结构改造，能否分别在冻结基础权重的小型适配器预算和解冻循环区块的较大预算下，形成稳定、可复用的逐循环隐空间状态转移。
- 将研究目标扩展到能力边界而非只验证任务正确率：同时考察循环机制能否超出训练深度继续工作、能否迁移到受控语言表述，以及学习新逆向操作时是否还能保留既有机制与一般能力。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

标准 Transformer 的计算量通常沿两个方向增加：设计时堆叠更多互不共享参数的层，或生成时输出更多推理 token。循环深度模型提供第三条路径：对隐藏状态反复应用同一个权重共享的变换，使测试时计算深度可以随循环次数增加，而独立参数量不必同步增长。既有研究多从头训练这种架构；本文则研究能否对已完成预训练和指令微调的稠密因果语言模型实施结构改造，在尽量保留原有能力的同时安装可逐步迭代的潜空间计算机制。这里的关键困难是分布偏移：预训练模块原本只处理前一层产生的状态，循环后却会反复接收自身输出，隐藏状态可能逐渐偏离其熟悉的表示分布。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**循环深度（recurrent depth）**

将同一个神经网络块按计算深度重复执行，并在各次执行之间共享权重。增加循环次数可以增加有效计算深度，但不会为每一层新增一套完整参数。

</div>
<div class="concept-item" markdown="1">

**潜空间迭代计算（latent iterative computation）**

模型在连续隐藏表示中逐步更新中间状态，而不是把每一步推理写成文本 token。本文关注每次循环是否对应一次稳定、可复用的任务状态转移。

</div>
<div class="concept-item" markdown="1">

**低秩适配（LoRA）**

冻结预训练权重，仅为部分线性映射加入可训练的低秩增量矩阵，从而以较少参数改变模型行为。本文将同一组秩为 $16$ 的适配器用于循环块的每次执行，使其成为权重共享循环算子的一部分。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是预训练且经过指令微调的 Qwen2.5-0.5B。作者将其按深度拆分为前置区（Prelude）、权重共享的循环块（Recurrent Block）和后置区（Coda）：输入序列先由 Prelude 编码，所得表示进入循环块执行指定次数，随后由 Coda 产生最终预测；第一次循环的路径被设计为在新增部件未起作用时严格复现基础模型，而后续循环通过可训练的重入桥再次注入 Prelude 表示，以缓解循环状态的分布漂移。实验设置比较两种相同结构、不同训练预算的改造：一种解冻循环区域，前向有效训练参数约为 $180.6$M；另一种冻结基础权重，仅训练共享的秩 $16$ 适配器与重入桥，前向有效参数约为 $6.01$M。核心问题是：这种改造能否学到“每次循环推进一个任务步骤”的稳定转移，能否在超过训练支持深度时继续工作，并能否在安装与后续训练期间保持基础模型的一般能力。该设置还要求区分循环机制本身与深度选择：本文主要通过强制指定循环次数评估机制，而如何让模型自动决定何时停止仍是开放问题。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$h_0$**

输入经过 Prelude 后得到、供循环计算使用的初始隐藏表示；原文节选未给出统一的正式符号，此处仅用于概括问题流程。

</div>
<div class="notation-item" markdown="1">

**$h_t$**

循环块执行第 $t$ 次后得到的隐藏状态；它应表示任务被继续推进后的潜空间中间结果。

</div>
<div class="notation-item" markdown="1">

**$T$**

推理时指定的总循环次数，即模型使用的有效循环深度。

</div>
<div class="notation-item" markdown="1">

**$F_\theta$**

在各循环之间共享参数 $\theta$ 的循环状态转移算子；具体桥接形式和正式方程未包含在所给章节中。

</div>

</div>

**直接相关的工作**

- **McLeish et al. (2025), pretrained non-recurrent language models converted to recurrent execution**: 这是与本文设置最接近的先例，同样把预训练的非循环语言模型转换为循环执行。本文的区别集中在拆分式重入桥、精确的中间状态监督，以及证明该机制也能在冻结基础权重的低参数适配预算下安装。
- **Universal Transformers (Dehghani et al., 2018)**: 该工作通过反复应用共享的自注意力变换实现深度递归，并加入逐位置动态停止机制，为权重共享的自适应计算提供基础参照。本文处理的是预训练因果语言模型的事后改造，采用显式循环，并把身份保持、重入后的表示分布对齐和能力保留作为核心约束。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现有预训练语言模型的计算深度通常在架构设计时固定；若依靠输出显式思维链来增加计算，则需要生成更多 token。对于需要多步、深度随样例变化的确定性推理任务，需要一种无需增加不同层参数、也无需把每一步都写成文本的额外计算轴，同时还要避免为获得该能力而放弃已有模型及其通用能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **从头训练的循环深度推理模型**：HRM、TRM 等方法从初始化阶段就让网络反复对隐状态应用共享变换，以较少的独立参数执行多轮内部计算；其结果说明迭代式隐空间计算可以解决一些令大模型困难的确定性推理任务。
- **稠密模型的固定深度或显式草稿推理**：固定深度 Transformer 通过预先堆叠不同层获得计算量；需要更多步骤时，另一类方案让模型在输出 token 中串行写出中间逻辑或草稿，再根据这些显式步骤生成答案。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 多数循环深度研究从头训练专用架构，因此不能说明这种能力是否可以安装到已经预训练并完成指令微调的稠密语言模型中，也不能说明安装后能否保留原模型的一般能力。
- 直接重复预训练区块会产生分布错位：后续循环接收的是此前循环生成的状态，而不是该区块在预训练时见过的表示，容易使激活偏离有效表示流形；同时，显式草稿方案把计算转化为输出 token，可能带来更长响应，并可能只在训练覆盖的步骤范围内有效。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

先前工作尚未系统建立一种经过工程与测量验证的“后装式循环深度”方案：既要保证单循环路径与基础模型一致，又要让后续循环真正获得上下文和优化信号，并区分模型学到的是可重复执行的状态转移还是终局答案记忆；此外，还缺少对小型适配器与大规模区块微调两种参数预算之间能力差异、远深度外推和持续训练干扰边界的对照。

</div>
<div markdown="1"><span>核心问题</span>

能否把预训练、指令微调的稠密语言模型以保持单循环恒等路径的方式改造成循环深度系统，使其学会稳定的逐循环隐状态更新，在偏重推理深度的任务上优于已登记的稠密训练方案，同时不损害基础模型的一般能力；实现这些目标最低需要多大的可训练参数预算，其外推、迁移与保留边界在哪里？

</div>
<div markdown="1"><span>作者直觉</span>

如果把模型拆成前置区、共享的循环区块和后置区，那么前置区可以先把输入编码成稳定的上下文表示，循环区块则像重复使用同一个计算步骤一样逐轮推进内部状态。后续循环通过桥接路径重新注入原始上下文，可减轻状态在反复变换中逐渐偏离输入条件的问题；保持单循环路径等同于原模型，则为能力保留提供结构起点。对中间状态按循环索引进行监督，还有望迫使每一轮学习“执行一步”而非直接记住最终答案，随后再用只评价最终结果的训练检验这一过程是否已固化。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把预训练语言模型的中间层改造成可重复执行的递归深度模块。具体而言，模型被划分为前置段、权重共享的循环块和后置段：前置段从输入得到表示 $p$，循环块在每次迭代中执行一次任务步骤，后置段将最终状态映射回语言模型输出空间。循环次数 $T$ 由实验时强制指定，循环过程中序列长度和上下文不增长，因此额外计算主要体现为隐空间中的串行深度。直观地说，模型不是把更多中间步骤写成更长文本，而是反复使用同一组中间层，在内部状态上逐步推进计算。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 模型分段与身份路径保留

在第 $a=6$ 层和第 $b=18$ 层处分割模型，形成 Prelude、12 层 Recurrent Block 和 Coda。循环次数为 $T=1$ 时，每个原始层仍按原顺序执行一次，并关闭递归附加操作，使单循环路径与基础模型计算完全一致。

<div class="method-step__io" markdown="1">

**输入**：预训练的 Qwen2.5-0.5B-Instruct，包括 24 个解码器层及其输入序列。<br>
**输出**：一个在 $T=1$ 时保持基础模型能力、在 $T>1$ 时能够重复执行中间块的包装模型。

</div>

**直观理解**：先把原模型的中间 12 层抽出来作为可反复使用的计算单元，同时保留前后两端负责读入和输出。单次运行时它应当像原模型一样工作，这样后续能力变化才可以归因于递归深度机制，而不是模型被改坏。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 前置表示与循环状态初始化

Prelude 对输入进行一次因果 Transformer 计算，得到输入相关表示 $p$；该表示作为循环状态的初始来源。每次循环内部，Recurrent Block 在固定序列长度 $S$ 上执行标准因果自注意力和前馈计算。

<div class="method-step__io" markdown="1">

**输入**：输入 token 序列、注意力掩码和位置标识。<br>
**输出**：第 $t$ 次循环的状态或块输出 $h_t$，其形状为 $(B,S,896)$，其中 $B$ 为批大小。

</div>

**直观理解**：模型先读懂当前输入，得到一份持续可参考的“原始问题表示”。之后每一轮都处理同样长度的序列，但内部状态会逐轮改变，因此步骤增加不会占用新的文本位置。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 带输入重注入的状态递归

在第 $t$ 轮之后，重入桥分别投影 $p$ 与 $h_t$，并通过偏向恒等映射的门控将两者融合，得到 $u_t$；随后将 $u_t$ 输入共享的 Recurrent Block，计算下一状态 $h_{t+1}$。Prelude 信息只在后续循环重新注入，因此既能保持输入锚定，又不破坏 $T=1$ 的身份路径。

<div class="method-step__io" markdown="1">

**输入**：Prelude 表示 $p$ 和上一轮循环输出 $h_t$。<br>
**输出**：经过 $T$ 轮递归后的最终状态 $h_T$，以及可在每一轮读取的循环 logits。

</div>

**直观理解**：每一轮都把“当前进度”和“最初的问题”重新对照，再继续计算。这样状态不会因反复过多次中间层而迅速偏离预训练模型熟悉的表示范围，同时又能保留已经完成的步骤。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 训练、强制深度读取与输出

安装阶段对每一轮状态施加对应中间步骤监督，例如目标链为 Ben 到 Max 到 Eve 到 Kai 时，循环 1、2、3 分别监督 Max、Eve、Kai；随后进行只监督最终答案的退火阶段。推理和机制评估时强制执行指定的 $T$ 轮，并用同一个经过已知正确链校准的 reader 读取每一轮及最终状态。

<div class="method-step__io" markdown="1">

**输入**：带有最终答案和可选中间答案的规则推理样本，以及指定的循环次数 $T$。<br>
**输出**：最终答案、各循环的中间预测、不同深度下的准确率和深度外推曲线。

</div>

**直观理解**：训练初期要求模型每走一步都答对，帮助它学会“过程”而非只记住终点；后期撤掉中间提示，检查过程是否已经保存在模型内部。测试时先规定模型必须走几轮，再逐轮检查它是否确实完成了相应步骤。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 重入桥与循环状态更新

$$
\begin{aligned}u_t&=\operatorname{Reentry}(p,h_t),\\h_{t+1}&=\operatorname{RecurrentBlock}(u_t),\\\operatorname{Reentry}(p,h_t)&=h_t+g\left(\operatorname{translated}(p,h_t)-h_t\right),\\\operatorname{translated}(p,h_t)&=W_p p+W_s h_t.\end{aligned}
$$

**符号说明**

- $p$：Prelude 对输入序列计算得到的表示。
- $h_t$：第 $t$ 次循环的 Recurrent Block 输出状态。
- $u_t$：重入桥融合输入表示和当前状态后，送入下一次循环块的状态。
- $W_p$：作用于 Prelude 表示的可学习投影矩阵，形状为 $896\times896$。
- $W_s$：作用于持久状态的可学习投影矩阵，形状为 $896\times896$。
- $g$：恒等偏置门控，用于控制新融合表示替换当前状态的幅度。
- $\operatorname{RecurrentBlock}$：共享的 12 层 Transformer 中间块。

<div class="equation-explanation" markdown="1">

**直观理解**：该公式规定每轮如何把旧状态和原始输入重新合并，再交给同一个 Transformer 中间块继续计算。若门控 $g$ 接近零，更新接近恒等映射；若门控增大，模型可以逐步引入输入重注入和新的递归变换。<br>
**原文位置**：第 3.2 节“The re-entry bridge and the corrected loop closure”；Listing 1

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练分为两个阶段。第一阶段对第 $t$ 轮读出的状态使用对应中间目标的交叉熵，使循环 1、2、3 等分别学习规则链中的第 1、2、3 步；第二阶段使用最终答案监督，移除中间标签，以检验步骤机制是否在只有终点奖励时仍然保持。原文说明目标还可以组合任务损失、中间状态损失和趋向中心化几何先验的停机正则项，但本文机制实验均强制循环次数，未给出一个可据此完整复现的统一总损失公式，因此停机选择器不属于本文已解决的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 三段式循环架构**

模型由 Prelude、权重共享的 Recurrent Block 和 Coda 组成，分割点为 $a=6$、$b=18$。Prelude 和 Coda 各执行一次，Recurrent Block 执行 $T$ 次；因此循环深度增加的是中间层重复次数，而不是 token 序列长度。

> 直观理解：前端负责理解输入，中央模块负责重复做步骤，后端负责把内部结果翻译成答案。中央模块共享权重，类似同一个计算程序被反复调用，而不是为每个深度都另存一套参数。

**2. 重入桥与恒等偏置门**

重入桥对 Prelude 表示和持久状态使用独立投影 $$W_p,W_s
e\text{undefined}$$，再通过门 $g$ 将变换结果与原状态混合。该桥是跨循环的唯一信息通道，并在后续循环重新注入输入相关表示。

> 直观理解：状态负责携带已经完成的工作，Prelude 表示负责不断提醒模型当前输入是什么。门控初始偏向“不改变状态”，有助于从原模型行为平稳地开始学习递归。

**3. 中间状态监督与固定 reader**

训练先使用每轮对应的中间目标进行交叉熵监督，再切换为只对最终答案计算损失，以检验步骤机制在撤除监督脚手架后的保持性。评估统一使用一个经过 oracle 链校准的 reader，并强制指定循环数，因而将“执行有效递归”与“自动选择深度”分开。

> 直观理解：同一个阅卷器检查所有系统和所有轮次，避免不同读取方式制造分数差异。本文主要验证模型能不能按要求继续计算，而不是验证它能不能自己决定何时停止。

**训练与推理**

训练时，首先在规则链任务上进行逐步监督，要求每次循环产生当前应到达的符号；随后进行最后 1,000 步的 outcome-only 训练，只根据最终答案优化。模型有两种预算：全块方案解冻 12 层循环块和桥，forward-active 训练参数为 180.6M；Adapter 方案冻结基础模型，在循环块投影上使用 rank-16 LoRA，并训练重入桥，forward-active 参数为 6.01M。对于需要独立学习率的 Prelude 投影，实现将其拆成独立张量并放入单独的 AdamW 参数组；原文指出，在 Adam 类优化器中仅缩放共享矩阵的梯度切片会被逐元素矩归一化抵消，在 Muon 中则会被矩阵正交化削弱，因此必须检查实际参数移动而非只检查代码中的倍率。推理时输入序列经过 Prelude，循环块按强制指定的 $T$ 重复执行，Coda 仅在最后一次状态上产生语言模型 logits；同时可以保存每轮 logits，由同一个 reader 分别检查中间状态和最终答案。本文不依赖学习到的停机头选择深度，且原文报告该选择器在工作机制上的最终测试为预注册的负结果。

**复现信息**

基础模型为 Qwen2.5-0.5B-Instruct，含 24 个解码器层、隐藏宽度 896；切分为前 6 层 Prelude、中间 12 层循环块和后 6 层 Coda。循环跨轮次不增加 KV cache、不扩展上下文，跨轮次唯一的信息通道是重入桥；单轮内部仍使用标准因果注意力，输入形状中的序列长度 $S$ 保持不变。$T=1$ 时递归附加模块被绕过，原始层顺序、注意力掩码、位置标识、归一化、数据类型和因果语义均保持不变。全块方案的 forward-active 参数为 180,556,929，Adapter 方案为 6,007,425；论文同时指出旧版优化器标记数包含一个在 split-mode 中被绕过、因而没有功能梯度的遗留投影。为公平解释结果，应注意循环模型与稠密 scratchpad 对照并非严格的架构因果比较：两者训练历史、token 数量、优化轨迹、FLOPs、延迟和推理计算并不完全相同，本文结论主要适用于所评估的完整系统。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 规则链任务的留出样本：正文片段未给出数据集名称与总规模；对深度1至4的留出行解码循环中间状态，共检查640个“样本—步骤”位置，用于判断模型是否逐步执行规则。
- 强制额外循环测试：对深度3的问题继续运行第4至第8轮，共检查384个超出答案深度的状态，用于区分“继续应用规则”“停在答案”和“产生无关状态”三种行为。
- ARC相关评估：早期参数高效方案使用128行筛选集，并以未改造基座的72/128作为历史参照；退役稳定性阻尼器另在512行ARC-Challenge扫描上评估。原文片段未明确报告这些样本的标准划分、抽样方式及是否与其他评估重叠。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**中间步骤正确率**

将每轮循环后的隐藏状态解码为规则链中的当前符号，并计算深度1至4各中间位置的正确比例。它检验在后期不再直接评分中间步骤后，逐步计算是否仍然存在。 （越高越好；高值表示内部状态仍按正确规则轨迹推进，但单凭该指标不能排除模型只在训练覆盖深度内记忆固定轨迹。）

</div>
<div class="metric-item" markdown="1">

**额外循环正确延续率**

对本应在深度3结束的问题强制继续循环，检查后续状态是否等于再次应用一次规则所得的下一符号。它比最终答案准确率更直接地测试循环块是否表示可重复操作。 （越高越好；高值支持“每轮应用一次规则”的机制解释，同时也说明循环次数过多会越过目标答案。）

</div>
<div class="metric-item" markdown="1">

**额外循环保持率**

统计超过目标深度后，状态是否停留并重复最终答案。该指标针对“模型到达答案后自动停车”的假设。 （在验证持续迭代机制时越低越好；接近零表示循环块不会自行停在答案，但这不是一般意义上的性能优势，因为实际推理仍需外部深度选择。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 仅监督最终答案后的深度1至4中间状态解码

<div class="result-value" markdown="1">

640个中间位置中有625个正确，中间步骤正确率为97.7%。作者据此主张：即使最后训练阶段不再评分中间步骤，模型仍保留逐步求解过程。

</div>

这说明高最终准确率并非完全依赖最后一轮直接猜答案，循环隐藏状态大多对应规则链的真实中间结果。分析上，它支持“机制保留”而非“为中间监督临时表演”的解释；但评估仍来自同一类规则任务，不能单独证明该操作已迁移到任意推理任务。

<div class="result-source" markdown="1">

来源：Result，Active-label diagonal, depths 1-4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The first row reflects decoding the intermediate states on held-out rows, after a final training phase which no longer graded them: 625 of 640 still held the correct intermediate answer, showing that the model solved problems step by step even when only answers were rewarded.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 将深度3问题强制运行第4至第8轮

<div class="result-value" markdown="1">

384个额外循环状态中，357个给出规则链的正确下一步，正确延续率为93.0%；仅1个状态停留在答案，保持率为0.3%。

</div>

两个观察合起来表明，循环块更像“每调用一次就应用一次规则”的状态转移，而不是“查到最终答案后停止”的模块。它也揭示了实际限制：额外循环会继续推进并越过正确答案，因此机制本身没有解决应运行多少轮的问题。

<div class="result-source" markdown="1">

来源：Result，Above-diagonal states that continued iterating / held

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Instead, 93.0% of extra-loop states contained the correct continuation of the chain, the symbol reached by applying the rule once more, and the model essentially never parked (1 of 384).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 修复循环架构后的冻结基座参数高效安装

<div class="result-value" markdown="1">

作者报告，在预训练基座权重完全不更新的条件下，使用6.01M个前向活跃适配器参数可以安装循环规则机制；这使早期“参数高效方案不可行”的结论发生逆转。

</div>

该结果把失败原因从“小参数预算天然不足”缩小到早期实现中的结构问题：循环没有重新注入Prelude上下文，且零门控与零分支的组合锁死了梯度。不过当前节选没有给出正式闭合实验的完整准确率、置信区间或逐深度表，因此只能确认作者报告的可安装性边界，不能据此判断其在所有深度上等同于全块适配。

<div class="result-source" markdown="1">

来源：Appendix A.3, The bounded answer；指向Section 6.2与Section 6.3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The registered closure experiment of Section 6.2 asked the question again on the corrected architecture, and the answer inverted: the mechanism installs at a 6.01M forward-active adapter budget with the base weights untouched, bounded exactly as Section 6.3 states it.

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

- 未改造的预训练基座：早期128行筛选中得到72/128，用于判断冻结基座上的新增循环组件是否至少保持原有能力；由于这些结果早于注册评估框架，作者明确将其视为历史结果，而非正式门控证据。
- “产生答案后停止”的假设基线：若循环块只会到达终点，超过所需深度后隐藏状态应重复答案；额外循环中的保持率直接检验这一行为。
- 捷径或终点查找假设：若模型没有学会逐次应用规则，额外循环状态应与规则链的下一步无稳定对应；正确延续率用于反驳这一解释。
- 修复后的全块适配与冻结基座的适配器方案：前者作为成功安装机制的参考路径，后者用于检验同一机制能否在仅约601万前向活跃训练参数下安装。当前片段未提供二者完整的逐深度结果表。

**实验想回答的问题**

- 循环块学到的是可重复执行一次的规则操作，还是仅在指定深度输出终点答案的查表式捷径？在训练后期只监督最终答案时，逐步计算机制是否仍能保留？
- 在保持预训练基座冻结的参数高效设置下，修复循环闭合与门控初始化后能否成功安装该机制；早期失败究竟来自参数预算不足，还是来自循环结构和优化路径缺陷？

**实验实现**

核心评估在结果退火阶段之后进行：最终训练阶段只按终点答案计分，不再奖励中间状态；随后在留出规则链样本上解码每轮隐藏状态。对深度1至4统计640个中间位置，并把深度3问题强制运行至第8轮，检查384个额外状态。参数高效路线冻结全部预训练权重，修复后的正式方案使用约6.01M个前向活跃适配器参数。早期失败方案则包含秩8 LoRA、恒等初始化的重入桥、零初始化混合门、PonderNet式停止头，以及第二阶段的4个SVGD粒子；作者指出该方案缺少Prelude上下文重注入，且零门控使桥接分支没有有效梯度，因此不能作为参数效率本身失败的有效检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 对早期重入桥的零门控进行只读强制开启 | 原设置下门值、桥输出差值以及门、权重和偏置梯度均为零；把门强制设为1后，投影权重梯度恢复为非零，权重梯度RMS达到9.28e-4。 | 该干预只改变桥接路径是否参与前向传播，因此隔离出“零门控加零分支初始化”造成的梯度自锁，而非优化器整体失效。它解释了早期方案为何从第一步起就无法学习重入组合，但不直接证明修复后的门控是唯一可行设计。 | Appendix A.2, Why it failed, decomposed<br><span class="experiment-evidence">A read-only control forcing the gate to one immediately recovered nonzero projection gradients (weight RMS 9.28e-4), isolating dead initialization rather than any optimizer failure.</span> |
| 在修复前的循环上启用全强度逐轴稳定性阻尼器 | 在512行ARC-Challenge扫描上，循环第8轮的尾部迹比从33.65降至2.91，但答案选择方面仅挽救52例、同时损害67例，因此没有产生清晰净收益并被弃用。 | 该消融表明阻尼器确实压制了循环状态的异常增长，却没有转化为任务性能提升。这支持作者的诊断：数值不稳定是错误循环闭合的症状，外部衰减只能控制症状；修复闭合后，生产路径将其强度设为0。 | Appendix A.4, The retired stability damper<br><span class="experiment-evidence">The damper was an eval-only, covariance-calibrated principal-component tail attenuation: at full strength it reduced the loop-8 tail trace ratio from 33.65 to 2.91 on a 512-row ARC-Challenge sweep without a clean answer-selection gain (52 rescued versus 67 harmed), and it was retired.</span> |

**定性案例**

- 深度3问题被强制多运行五轮可视为机制诊断案例：若模型学的是终点查找，后续状态应保持答案；实际状态通常继续沿规则链推进。该案例把隐藏状态行为与“每轮应用一次规则”的算法语义对应起来，同时直观展示运行过多轮会越过答案。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过为预训练语言模型引入循环深度，研究潜在空间迭代推理的安装、外推、迁移与保持。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`a4d74e4e777ba29f2454e685ba9d6ec1ba3fb7524506136ea8821c2fb33be951`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
