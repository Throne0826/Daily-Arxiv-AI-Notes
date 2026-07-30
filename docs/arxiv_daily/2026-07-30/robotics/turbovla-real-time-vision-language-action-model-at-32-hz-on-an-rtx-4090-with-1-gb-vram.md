---
title: "[论文解读] TurboVLA: Real-Time Vision-Language-Action Model at 32 Hz on an RTX 4090 with <1 GB VRAM"
description: "[arXiv 2607.27205][机器人 / 具身智能] TurboVLA质疑以大语言模型为执行核心的主流VLA架构，提出让视觉与语言特征直接交互并一次性预测连续动作块，以较小的计算和显存代价实现实时、语言条件化的机器人操控。"
arxiv_id: "2607.27205"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:25.455170+00:00"
source_sha256: "0f1fb0e160e037c8809a5fd5583d34bacafc4dae0264222fe80e604c2462428d"
tags:
  - "机器人 / 具身智能"
  - "VLM Efficiency"
  - "LLM 其他"
  - "视觉—语言—动作模型"
  - "语言条件机器人操作"
  - "直接视觉—语言交互"
  - "双向交叉注意力"
  - "连续动作分块"
  - "实时推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.27205</p>

# TurboVLA: Real-Time Vision-Language-Action Model at 32 Hz on an RTX 4090 with <1 GB VRAM

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Hengyi Xie, Chenfei Yao, Xianjin Wu, Xuanyang Xi, Yiping Tang, Di Xu, Yingying Zhu, Dingkang Liang, Xiang Bai, Han Ding</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27205v1) · [PDF 下载](https://arxiv.org/pdf/2607.27205v1) · **关键词** 视觉—语言—动作模型, 语言条件机器人操作, 直接视觉—语言交互, 双向交叉注意力, 连续动作分块, 实时推理  
**代码**: [https://github.com/H-EmbodVis/TurboVLA](https://github.com/H-EmbodVis/TurboVLA)  

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

TurboVLA质疑以大语言模型为执行核心的主流VLA架构，提出让视觉与语言特征直接交互并一次性预测连续动作块，以较小的计算和显存代价实现实时、语言条件化的机器人操控。

**不用术语来说**：机器人需要根据摄像头画面和人类指令迅速决定下一步动作，但许多现有系统每次决策都要调用一个拥有数十亿参数的大语言模型，好比让机器人在执行每个简单动作前都先运行一套庞大的通用推理程序。这会增加等待时间和显存需求，降低控制频率，也使系统难以部署到计算资源有限的机器人上。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 在概念上将传统的间接 V→L→A 路径改写为直接的 V+L→A 路径：语言仍用于规定任务，但通用大语言模型不再充当视觉感知与动作控制之间的必经接口。
- 提出面向执行级操控的轻量方案TurboVLA，通过独立的视觉与文本编码、双向跨模态交互、机器人状态条件化以及非自回归连续动作块预测，兼顾任务条件理解与低延迟执行。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

视觉—语言—动作模型（Vision-Language-Action, VLA）面向语言条件机器人操作：策略依据当前视觉观测和自然语言指令生成机器人动作。主流方案采用以大语言模型（LLM）为核心的间接路径 V\rightarrow\mathbf{L}\rightarrow A：先把视觉特征投影到语言模型的表示空间，再由语言模型融合图像与指令，最后生成动作或将融合表示交给连续动作解码器。这种结构可利用大规模预训练得到的语义知识，但机器人每次调用策略都要经过参数量庞大的语言模型，因而带来显著的计算、显存和时延开销。本文关注的不是开放式对话或自主任务分解，而是指令已经给定后的执行级连续控制，并考察是否能通过视觉与语言特征直接交互来取代LLM中心接口。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**视觉—语言—动作模型（VLA）**

一种把视觉观测、自然语言任务描述和机器人控制统一起来的策略模型。其目标是让机器人根据“看见什么”和“被要求做什么”决定下一步动作。

</div>
<div class="conceptitem" markdown="1">

**交叉注意力（cross-attention）**

一种让一个模态的特征主动查询另一个模态信息的机制，例如让图像区域查询指令中与其相关的词语。双向交叉注意力同时进行“语言指导视觉”和“视觉修正语言”，从而建立细粒度对应关系。

</div>
<div class="conceptitem" markdown="1">

**连续动作分块（continuous action chunk）**

模型一次前向计算直接预测未来一段连续数值动作，而非把动作离散成符号后逐个生成。这样可以减少自回归解码次数，并提高策略执行频率。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

在第 n 次策略调用时，模型接收视觉观测 \mathcal{O}_n、自然语言任务指令 x，并可结合当前机器人状态 s_n；输出为连续动作序列块 \hat{\mathbf{A}}_n，用于执行语言条件操作。传统设定先计算 \widetilde{Z}_n^v=P_v(E_v(\mathcal{O}_n))，再通过 H_n^L=F_L([\widetilde{Z}_n^v;\operatorname{Tok}(x)]) 获得LLM中心的多模态表示，动作预测依赖该表示。本文所针对的设置假定指令已明确操作意图，因此执行策略主要需要判断当前视觉证据应如何转化为动作，而不必承担开放式语言生成或自主任务分解；由此可将问题改写为直接的 \mathbf{V}+\mathbf{L}\rightarrow A 映射。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$\mathcal{O}_n$**

第 n 次策略调用时的视觉观测。

</div>
<div class="notationitem" markdown="1">

**$x$**

描述目标操作任务的自然语言指令。

</div>
<div class="notationitem" markdown="1">

**$s_n$**

第 n 次调用时的机器人自身状态，供动作解码器进行状态条件化。

</div>
<div class="notationitem" markdown="1">

**$\hat{\mathbf{A}}_n$**

模型预测的连续动作块，即一次输出的未来若干步机器人动作。

</div>

</div>

**直接相关的工作**

- **OpenVLA / RT-2**: 二者代表LLM中心的自回归VLA：将机器人动作表示为离散词元，并基于语言模型表示按顺序生成。它们既保留大型语言模型的计算开销，又承担逐词元动作解码的串行成本，是本文所对比的传统 V\rightarrow\mathbf{L}\rightarrow A 路径。
- **Grounding DINO**: 该视觉定位模型利用直接的跨模态交互建立文本概念与图像内容之间的细粒度对应。TurboVLA借鉴其高效视觉—语言交互思路，但将交互后的特征用于连续机器人动作预测，而非目标定位。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

语言条件化机器人不仅要理解“做什么”，还必须根据不断变化的视觉观察及时决定“怎么做”。在响应式交互、高吞吐操控和资源受限平台上，策略调用的延迟、显存占用与控制频率都是实际部署条件；若每次动作决策都经过大型语言模型，即使任务成功率较高，也可能无法满足实时控制要求。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **自回归、LLM中心的VLA**：先把视觉观察投影到大语言模型的表示空间，与语言指令共同处理，再把机器人动作离散为类似词元的序列，按照先后顺序逐个生成；代表性方法包括OpenVLA和RT-2。
- **带并行动作头或动作专家的LLM中心VLA**：保留大型语言模型作为多模态处理核心，但用并行解码、连续动作头或专门的动作专家替代逐词元动作生成，从而一次或并行地产生动作，减少动作解码阶段的串行开销。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 自回归方法把动作当作词元逐步生成，继承了语言生成的串行解码成本；其直接后果是单次策略调用延迟较高，难以提升在线控制频率。
- 并行动作头和动作专家虽然消除了逐动作词元生成，但视觉与指令仍需先经过数十亿参数的语言模型；因此主要计算与显存瓶颈并未消失，仍会限制消费级硬件和资源受限机器人的部署。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作主要优化“大语言模型之后如何生成动作”，却较少检验一个更基础的架构假设：对于指令已经明确、重点是根据当前画面执行具体技能的任务，视觉与语言是否必须先统一到通用大语言模型的潜在空间。因而仍缺少一种不以LLM为执行核心、同时能保留语言条件化能力与强操控性能的直接控制范式。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一个简单而高效的VLA，使视觉观察和语言指令直接形成面向控制的联合表示并输出连续动作，在移除执行路径中的大型语言模型后，仍满足实时机器人操控所需的任务成功率、低延迟和低显存要求？

</div>
<div markdown="1"><span>作者直觉</span>

具体执行指令通常已经说明目标技能，底层策略的主要职责不是开放式生成语言或自主分解复杂任务，而是让指令筛选当前画面中与动作有关的信息。例如，“拿起杯子”只需使视觉编码器重点关注杯子及其可抓取位置。轻量文本编码器可以提供这种任务语义，紧凑的双向视觉—语言交互则可直接生成控制导向特征，因此无需在每一步都调用具备广泛知识和复杂推理能力的通用LLM。作者同时承认，这一直觉主要适用于执行级指令，不能据此推断该架构足以承担高层规划。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TurboVLA将传统的“视觉先进入大语言模型、再生成动作”的 V→L→A 路径改为直接的 V+L→A 路径。系统输入当前时刻的多相机图像、自然语言任务指令和机器人本体状态；视觉编码器与轻量文本编码器分别提取特征，堆叠的双向交叉注意力让视觉和语言直接交换信息，随后轻量 Transformer 解码器一次并行预测未来 H 步连续动作。其关键取舍是：执行级操作指令通常只需表达对象、属性和空间关系，因此不再让大型生成式语言模型充当感知到动作的必经接口。

直观而言，该方法把“大语言模型先统一理解一切”的重型流程，改成“视觉模块看场景、文本模块读指令、二者直接对照后交给动作模块执行”。机器人状态不参与前面的视觉—语言对齐，而是在动作解码阶段加入：前半段回答“场景中与任务相关的是什么”，后半段结合机械臂当前姿态回答“接下来具体怎样运动”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多模态输入与独立编码

轻量文本编码器保留完整的逐词元特征；图像编码器提取各视角的空间特征，并加入位置嵌入和相机视角嵌入；机器人状态由独立的小型投影网络编码。各类特征均被投影到共享隐藏维度 d。

<div class="method-step__io" markdown="1">

**输入**：任务指令 x、当前时刻 n 的 K 路相机图像 I_n^{(1)},\ldots,I_n^{(K)}，以及机器人状态 s_n。  
**输出**：语言序列 Z^l、拼接后的多视角视觉序列 Z_n^v，以及状态序列 Z_n^s。

</div>

**直观理解**：文本不被压缩成单个向量，以免丢失“哪个物体、什么属性、位于哪里”等细节；位置和视角标记则告诉模型每个视觉特征来自图像何处及哪台相机。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双向视觉—语言交互

连续通过 N 个融合层，每层包含层归一化、两个方向的交叉注意力、模态专属前馈网络和残差连接；语言查询视觉以形成场景感知的指令特征，视觉查询语言以形成指令条件化的视觉特征。

<div class="method-step__io" markdown="1">

**输入**：视觉特征 V_n^0=Z_n^v 与语言特征 L_n^0=Z^l。  
**输出**：最终视觉流 V_n^N 和语言流 L_n^N，并拼接为动作就绪表示 Z_n^{vl}=[V_n^N;L_n^N]。

</div>

**直观理解**：两个方向分别让指令确认“场景里这句话具体指什么”，并让图像突出“当前任务真正需要关注什么”。相比只做单向注意力，双方都更新可保留互补信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 融合机器人状态并并行动作解码

ACT 风格的轻量 Transformer 解码器以 [Z_n^{vl};Z_n^s] 为上下文，同时解码全部 H 个动作查询，不进行动作离散化或逐词元自回归生成。

<div class="method-step__io" markdown="1">

**输入**：跨模态表示 Z_n^{vl}、机器人状态特征 Z_n^s，以及 H 个可学习动作查询 Q_a=[q_1,\ldots,q_H]。  
**输出**：连续动作块 \hat{\mathbf A}_n\in\mathbb R^{H\times d_a}，其中每一行对应一个未来时间步的 d_a 维机器人动作。

</div>

**直观理解**：模型像一次写出一小段未来控制计划，而不是每生成一步就重新运行完整策略；当前关节或末端状态在此阶段加入，使场景理解能够转化为机械臂实际可执行的运动。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 行为克隆训练与闭环执行

训练时以预测动作块和专家动作块之间的 L1 损失优化全部策略参数，不加入辅助语言建模目标；推理时每次策略调用直接产生一个连续动作块。

<div class="method-step__io" markdown="1">

**输入**：专家示范中的观测、指令、机器人状态及对应的 H 步专家动作块 \mathbf A_n^*。  
**输出**：学习得到参数化策略 D_\theta，并在部署时输出可执行的未来动作序列。

</div>

**直观理解**：训练目标只要求模型模仿专家怎样控制机器人，无需同时学习续写文本。并行动作块减少了顺序生成带来的等待，但实际闭环中的动作块执行与重规划细节在所给原文中未明确报告。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 双向交互的逐层更新与最终融合

$$
\left(V_{n}^{\ell},L_{n}^{\ell}\right)=\operatorname{FusionLayer}_{\ell}\left(V_{n}^{\ell-1},L_{n}^{\ell-1}\right),\quad \ell=1,\ldots,N,\qquad Z_{n}^{vl}=\left[V_{n}^{N};L_{n}^{N}\right]
$$

**符号说明**

- $n$：当前策略调用或观测时刻的索引。
- $V_n^0=Z_n^v$：进入交互模块前的多视角视觉特征序列。
- $L_n^0=Z^l$：进入交互模块前的逐词元指令特征序列。
- $\ell$：融合层索引。
- $N$：双向视觉—语言融合层的总数。
- $\operatorname{FusionLayer}_{\ell}$：第 \ell 个融合层，包含层归一化、双向交叉注意力、模态专属前馈网络、残差连接。
- $V_n^\ell,L_n^\ell$：经过第 \ell 层后更新的视觉流和语言流。
- $Z_n^{vl}$：将最终视觉流与语言流沿序列维拼接得到的动作就绪多模态表示。
- $[\,;\,]$：特征序列拼接操作。

<div class="equation-explanation" markdown="1">

**直观理解**：每一层都让视觉与语言互相读取对方的信息，而不是把两个独立特征直接交给动作模块。多层迭代完成任务词语与场景区域的逐步对齐，最终保留两条流供动作解码器使用。  
**原文位置**：第4.2节，公式(7)与公式(8)

</div>

</div>

<div class="equation-block" markdown="1">

#### 连续动作块并行预测

$$
\hat{\mathbf{A}}_{n}=D_{\theta}\!\left(Q_{a},\left[Z_{n}^{\mathrm{vl}};Z_{n}^{s}\right]\right)\in\mathbb{R}^{H\times d_{a}},\qquad Q_{a}=\left[q_{1},\ldots,q_{H}\right]
$$

**符号说明**

- $\hat{\mathbf A}_n$：模型在时刻 n 预测的完整连续动作块。
- $D_\theta$：参数为 \theta 的轻量 ACT 风格 Transformer 动作解码器。
- $Q_a$：由 H 个可学习动作查询构成的查询序列。
- $q_h$：用于预测动作块中第 h 个时间位置的可学习查询。
- $Z_n^{vl}$：双向视觉—语言交互后得到的任务条件化多模态特征。
- $Z_n^s$：当前机器人状态 s_n 经轻量状态编码器产生的特征。
- $H$：一次预测覆盖的动作步数，即动作视界或动作块长度。
- $d_a$：单步连续机器人动作的维度。
- $\mathbb R^{H\times d_a}$：输出包含 H 个 d_a 维实值动作。

<div class="equation-explanation" markdown="1">

**直观理解**：H 个查询同时从任务相关场景特征和当前机器人状态中提取控制信息，因此一次前向传播即可得到整段连续动作。它直接消除了动作离散化和逐步生成的计算链路，是低延迟设计的重要组成部分。  
**原文位置**：第4.3节，公式(9)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：TurboVLA使用专家示范进行行为克隆。对时刻 n 的专家动作块 \mathbf A_n^*=[a_{n,1}^*,\ldots,a_{n,H}^*]，以预测动作块 \hat{\mathbf A}_n 与专家动作块之间的 L1 损失训练策略；该损失按元素惩罚连续动作的绝对误差，并通过反向传播优化编码器、交互模块和动作解码器参数。原文明确说明“不需要辅助语言建模目标”，但所给章节没有展示L1目标的完整公式或归约方式，因此不额外构造方程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 紧凑的模态专属编码器**

文本侧采用 BERT 等轻量编码器并保留 N_l 个词元表示；视觉侧对 K 路相机分别编码，投影到维度 d 后加入视图内位置嵌入 E_{pos}^{(i)} 和相机标识 e_{view}^{(i)}，再沿序列维拼接。状态编码器 f_{state} 独立产生 N_s 个状态特征，不进入视觉—语言交互模块。

> 直观理解：该设计只保留执行级操作所需的信息，不承担开放式文本生成或高层任务规划，从而避免大型语言模型产生的参数、激活显存和注意力计算开销。把状态推迟到动作解码阶段，也让跨模态模块专注于寻找与指令相关的场景内容。

**2. 堆叠式双向交叉注意力模块**

模块以视觉和语言两条序列为输入，在每一层分别执行视觉到语言、语言到视觉的交叉注意力，并通过残差连接和模态专属前馈网络更新两条流；经过 N 层后拼接二者。它替代了传统 VLA 中由大语言模型承担的多模态表示桥梁。

> 直观理解：交叉注意力可以理解为一组内容相关的检索：文本词元从图像中寻找对应对象，图像区域也从文本中寻找任务条件。双向更新使“指令如何落到当前场景”和“场景如何消除指令歧义”同时发生。

**3. 连续动作块解码器**

ACT 风格 Transformer 解码器使用 H 个可学习查询，每个查询对应动作块中的一个时间位置，并共同关注视觉—语言表示与机器人状态；输出维度为 H\times d_a。所有动作位置并行预测，因此无需将连续控制量量化成动作词元，也无需自回归解码。

> 直观理解：该模块直接回答未来若干步“怎么动”，避免逐个动作生成造成的串行延迟。动作块长度 H 控制时间覆盖范围：过短难以表达连续技能，过长则增加一次预测整段轨迹的难度。

**训练与推理**

训练阶段，从专家轨迹截取当前多相机观测、任务指令、当前机器人状态和随后 H 步连续动作。文本、图像与状态分别编码；视觉和语言通过 N 层双向交叉注意力形成任务条件化表示；动作解码器以 H 个动作查询并行预测动作块，随后用L1行为克隆损失与专家动作块比较并更新参数。由于训练目标直接监督连续控制量，系统不需要动作词表、动作标记化或语言生成监督。

推理阶段，对每次策略调用执行同一前向路径：编码当前图像与固定任务指令，进行双向视觉—语言融合，再结合当前机器人状态一次输出 H 步动作。主实验采用 H=12、N=6；这种并行预测避免自回归动作生成。所给原文没有明确说明动作块是否全部执行、采用时间集成，还是在执行若干步后重新规划，因此这些部署行为不能从摘录中确定。

**复现信息**

公平理解方法所需的关键设置是：视觉、语言和状态特征统一到隐藏维度 d；文本侧保留完整词元序列，视觉侧保留空间特征并显式加入位置与相机视角嵌入；跨模态模块只处理视觉和语言，机器人状态仅在动作解码阶段加入。主要配置使用 BERT 文本编码器、N=6 个双向交互层和 H=12 的动作块长度；文中也说明文本编码器可替换为 T5-small 或 SigLIP-Base，表明核心方法并不绑定单一文本骨干。除这些设计外，优化器、学习率、批量大小、图像分辨率、视觉编码器训练或冻结策略等复现细节在所给原文中未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- LIBERO：包含LIBERO-Object、LIBERO-Spatial、LIBERO-Goal和LIBERO-Long四个套件，每套10个语言条件操作任务，共40个任务。实验使用OpenVLA发布的修改版no_noops RLDS数据，将四套数据混合训练为一个模型；每个任务进行50次 rollout，共计2000次试验。其作用是同时检验单臂策略的物体识别、空间关系理解、目标条件执行和长时序操作能力。
- RoboTwin 2.0：包含50个需要双臂协调的语言条件操作任务。受计算预算限制，训练只采用官方clean demonstrations，不使用随机场景数据；每个任务在clean setting下评估100次，并汇报50个任务的平均成功率。该基准用于检验架构能否扩展到14维双臂绝对关节位置控制和多任务联合学习，但不能充分衡量对场景随机化的鲁棒性。
- 真实机器人数据：使用AgileX Piper平台，覆盖grab roller、move playing card away、press stapler和stack three bowls四项任务。每项任务采集65条遥操作示范，共4×65条；策略从LIBERO预训练检查点初始化，再微调12.5k步。每项任务测试40次，用于考察真实视觉噪声、视角变化、物体定位及闭环执行能力。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**任务成功率**

成功完成指定语言条件操作任务的试验比例，是所有仿真与真实场景的主要任务性能指标。它直接衡量最终任务是否完成，但不能单独说明动作轨迹质量、失败类型或安全性。 （越高越好，因为更高比例表示策略在更多独立试验中完成了任务。）

</div>
<div class="metricitem" markdown="1">

**推理延迟**

从输入多模态观测到生成一个动作块，或生成等价数量的自回归动作token所需的时间；在RTX 4090、batch size为1下测量。它近似反映在线策略的控制响应速度。 （越低越好，因为更短延迟通常允许更高控制频率和更及时的闭环反馈。）

</div>
<div class="metricitem" markdown="1">

**推理显存**

完整在线策略推理期间的峰值GPU显存占用，用来衡量部署资源需求。论文还报告总参数量，但参数量与运行时峰值显存并不等价。 （越低越好，因为较低峰值显存使模型更容易部署在消费级GPU上，并为其他感知或控制模块保留资源。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### LIBERO四套件联合评估

<div class="result-value" markdown="1">

作者报告TurboVLA在LIBERO上的平均成功率为97.7%。

</div>

作者主张，直接采用V+L→A而非以大语言模型为中心的V→L→A路径，仍能获得很高的语言条件单臂操作成功率。该结果说明轻量架构没有明显牺牲该基准上的最终任务完成率；但当前节选没有给出四个套件的分项成绩、方差或逐基线差值，因此不能据此判断优势集中在哪类任务，也不能验证统计显著性。

<div class="result-source" markdown="1">

来源：Abstract；表1在节选中仅出现标题，未提供完整数据行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">On LIBERO, TurboVLA achieves 97.7% average success with only 0.2B parameters, 31.2 ms inference latency, and 0.9 GB inference VRAM on a consumer-grade RTX 4090, matching or outperforming substantially larger VLA policies.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 单张消费级RTX 4090上的在线推理效率

<div class="result-value" markdown="1">

作者报告推理延迟为31.2 ms，对应理论上约32 Hz的策略调用频率。

</div>

31.2 ms表示模型可在约三十分之一秒内从多模态输入生成一个动作块，支持较高频率的闭环控制。这里的约32 Hz是由单次延迟换算出的调用频率，不等同于整套机器人系统的实际控制频率；摄像头采集、通信、机器人执行和其他软件开销可能进一步降低端到端频率。

<div class="result-source" markdown="1">

来源：Abstract；表1说明延迟在单张RTX 4090、batch size为1下测量

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">On LIBERO, TurboVLA achieves 97.7% average success with only 0.2B parameters, 31.2 ms inference latency, and 0.9 GB inference VRAM on a consumer-grade RTX 4090, matching or outperforming substantially larger VLA policies.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 模型规模与部署显存

<div class="result-value" markdown="1">

作者报告TurboVLA仅有0.2B参数，推理峰值显存为0.9 GB。

</div>

这一结果表明模型可在消费级GPU上以较小资源占用运行，支持论文关于轻量部署的核心主张。参数量和显存是两个不同维度：前者描述模型规模，后者还受激活、数据类型和实现方式影响。当前节选未给出所有对照模型的完整参数与显存数据，也没有跨GPU或不同精度设置的结果，因此尚不能判断该效率优势在其他硬件环境中是否保持。

<div class="result-source" markdown="1">

来源：Abstract；表1说明TurboVLA参数量对应DINOv3 ViT-B配置

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">On LIBERO, TurboVLA achieves 97.7% average success with only 0.2B parameters, 31.2 ms inference latency, and 0.9 GB inference VRAM on a consumer-grade RTX 4090, matching or outperforming substantially larger VLA policies.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前提供的实验节选在表1标题处结束，缺少LIBERO完整对照表、RoboTwin 2.0结果、真实机器人结果和组件消融数据。因此除摘要中的97.7%、0.2B、31.2 ms和0.9 GB外，其余数值结论均不能核验；也无法按要求报告有证据支持的消融结果。
- 实验范围本身存在外推限制：RoboTwin 2.0仅训练和评估clean setting，真实实验也只有单一AgileX Piper平台、四项任务及每项40次试验。现有证据不足以证明模型对随机场景、不同机器人本体、长期运行、安全约束或分布外语言指令具有同等效果。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- π0.5：真实机器人实验中的直接对照方法；它与TurboVLA使用相同机器人平台、训练数据和评估协议，因此比较主要反映策略架构差异，而不是数据量或硬件条件差异。
- 其他可运行的VLA方法：原文说明使用各方法的官方架构、实现和检查点，在同一RTX 4090、batch size为1的条件下重新测量效率。当前节选没有给出这些方法的具体名称及结果，因而无法逐一判断其模型规模和预训练数据是否与TurboVLA严格可比。
- VLA-Adapter：本文沿用其LIBERO rollout协议，保证LIBERO成功率的评估流程具有可比性；当前节选未明确说明它是否作为表1中的直接数值基线。
- StarVLA：本文沿用其RoboTwin 2.0训练与评估框架，用于统一双臂任务的实验协议；当前节选未提供其对照成绩，也未明确说明是否在完全相同训练数据下比较。

**实验想回答的问题**

- TurboVLA在不以大语言模型作为视觉到动作中介的情况下，能否保持较强的语言条件机器人操作成功率，同时显著降低参数量、推理延迟和显存占用？
- 这种直接视觉—语言交互架构能否从LIBERO单臂仿真任务扩展到RoboTwin 2.0双臂多任务控制和真实机器人部署，并且哪些核心组件对性能起主要作用？

**实验实现**

TurboVLA采用DINOv3作为视觉骨干、BERT作为轻量指令编码器，将视觉和文本特征投影到256维共享空间，再经过6层双向视觉—语言交互层；这些交互层由grounding预训练的特征增强权重初始化。ACT风格Transformer解码器结合多模态特征与机器人状态，输出连续动作块。所有基准均使用行为克隆和L1损失训练，学习率为5×10^-5，训练使用4张RTX 4090。LIBERO配置使用DINOv3 ViT-B，预测12步、7自由度连续动作块，训练80k步，其中10k步warm-up，有效batch size为256。RoboTwin 2.0使用DINOv3 ViT-L，预测50步、14维绝对关节位置动作块，训练55k步，其中1k步warm-up，有效batch size为192。效率测试统一在单张RTX 4090、batch size为1下进行；延迟覆盖完整多模态输入至动作输出过程，显存取完整在线策略的峰值。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 真实平台选择抓取滚轮、移走扑克牌、按压订书机和堆叠三个碗，分别涉及目标定位、平面物体操作、接触式执行和较长序列堆叠，可用于观察视角鲁棒性与闭环稳定性；但当前节选未提供成功率、失败案例或定性轨迹，故无法判断TurboVLA具体在哪类现实扰动下更稳健。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Proposes a compact, low-latency vision-language-action architecture for efficient real-time robotic manipulation.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`0f1fb0e160e037c8809a5fd5583d34bacafc4dae0264222fe80e604c2462428d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
