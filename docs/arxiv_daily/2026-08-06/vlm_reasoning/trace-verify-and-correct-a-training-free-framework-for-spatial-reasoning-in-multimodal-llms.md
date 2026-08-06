---
title: "[论文解读] Trace, Verify, and Correct: A Training-Free Framework for Spatial Reasoning in Multimodal LLMs"
description: "[arXiv 2608.04759][VLM Reasoning] 本文针对多模态大语言模型空间推理中“中间判断与图像不一致并沿推理链传播”的问题，提出一种无需训练的证据级追踪、可靠性验证与定点纠错框架。"
arxiv_id: "2608.04759"
announcement_date: "2026-08-06"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:51:04.368343+00:00"
source_sha256: "e3edbb3af95009df60888cd820da25b41c6a81ef8d547e8918eaed8b5b7d5506"
tags:
  - "VLM Reasoning"
  - "LLM 其他"
  - "LLM Reasoning"
  - "多模态 VLM"
  - "多模态大语言模型"
  - "空间推理"
  - "思维链"
  - "感知忠实性"
  - "空间证据核验"
  - "免训练纠错"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.04759</p>

# Trace, Verify, and Correct: A Training-Free Framework for Spatial Reasoning in Multimodal LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Yang Yang, Jiawei Chen, Tairan Chen, Zhaoxia Yin</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Shanghai Key Laboratory of Multidimensional Information Processing；East China Normal University；Zhongguancun Academy；Stevens Institute of Technology</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04759v1) · [PDF 下载](https://arxiv.org/pdf/2608.04759v1) · **关键词** 多模态大语言模型, 空间推理, 思维链, 感知忠实性, 空间证据核验, 免训练纠错<br>


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

本文针对多模态大语言模型空间推理中“中间判断与图像不一致并沿推理链传播”的问题，提出一种无需训练的证据级追踪、可靠性验证与定点纠错框架。

**不用术语来说**：模型回答空间问题时，通常会先写出若干推理步骤，但其中某一步可能看错物体、位置或方向；后续步骤又会把这个错误当作事实继续推导，最终得到错误答案。现有方法多通过重新训练模型或补充深度、三维结构等信息来提高总体表现，却不检查推理过程中的具体空间判断是否真正得到图像支持。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 将改进目标从最终输出转向推理过程，提出模块化、模型无关且无需更新参数的验证与纠错框架：追踪空间证据，定位最早被可靠视觉证据否定的判断，并让原模型从受影响位置重新生成推理与答案。
- 提出空间证据图（SEG）和空间证据可靠性评估（SERA）：前者把自由文本推理中的原子空间判断关联到视觉实体、空间关系及来源步骤，后者从物体存在性、定位置信度和几何测量质量判断视觉证据是否足以支持纠错。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于多模态大语言模型的视觉空间推理研究。任务要求模型结合图像与文本问题，判断物体是否存在、位于何处以及物体之间的方向、距离或拓扑关系，并通过思维链逐步得到答案。这里的关键风险不只是最终答案错误：如果某个中间空间判断与图像不一致，后续步骤可能把它当作已知前提反复使用，使局部感知错误沿推理链传播。在自动驾驶、机器人等需要依据视觉空间关系采取行动的场景中，这类错误会直接影响决策可靠性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多模态大语言模型（MLLM）**

能够联合处理图像和自然语言的生成式模型，例如根据一幅图像回答物体位置关系问题。本文将原始模型视为可调用的推理器，不要求访问或更新其参数。

</div>
<div class="concept-item" markdown="1">

**思维链（Chain-of-Thought, CoT）**

模型在输出最终答案之前生成的一系列中间推理步骤。空间任务中的某一步可能包含“物体 A 位于物体 B 左侧”之类的判断，而错误判断可能成为后续步骤的错误前提。

</div>
<div class="concept-item" markdown="1">

**感知忠实性（perceptual faithfulness）**

本文用该术语表示中间空间证据是否与输入图像一致。它关注推理过程中的判断有没有视觉依据，而不仅关注最终答案是否碰巧正确。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一幅图像、一个需要空间推理的文本问题，以及原始 MLLM 生成的自由形式 CoT 与初始答案；输出是经视觉证据核验并在必要时修正后的推理链和最终答案。论文采用免训练、模型无关的推理时设置：系统不修改原始 MLLM 参数，而是从 CoT 中抽取原子化空间判断，将其关联到视觉实体、空间关系和来源步骤，再利用物体存在性、定位结果及几何测量进行可靠性评估。若可靠视觉证据与某个判断冲突，系统定位最早出现的冲突证据单元，并要求原始模型从受影响位置重新生成后续推理；这一设置同时假定外部视觉核验本身可能受遮挡、定位误差等因素影响，因此只有被判定为可靠的证据才能触发纠正。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **基于训练的空间推理增强方法**: 这类方法通过空间问答或推理数据、空间指令数据以及区域感知或深度感知表示提升 MLLM，但通常需要访问模型参数，并针对新模型或新任务重新适配。本文转而采用免训练框架，处理已经生成的推理过程。
- **推理时空间信息增强方法**: 这类方法在推理阶段加入深度线索、3D 先验、视觉标记或结构化场景表示，可以补充空间信息，但主要优化输入或整体生成结果，没有显式定位、核验和纠正 CoT 中的中间空间证据。本文的区别是对原子证据单元进行来源追踪与可靠性约束下的过程级修正。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

复杂空间问答依赖一连串中间判断，任何与图像不符的局部判断都可能被后续步骤反复引用并放大。在自动驾驶、机器人等需要依据真实环境采取行动的场景中，这类错误不仅降低答案准确率，还可能造成错误决策，因此模型需要的不只是更强的空间知识，还包括对自身推理依据的可核查性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **训练阶段的空间能力增强**：使用空间问答数据或空间推理数据训练、微调模型，使其在参数层面学习更强的空间关系识别与推导能力。
- **推理阶段的空间信息增强**：不重新训练模型，而是在输入或生成过程中加入深度线索、结构化场景表示或三维先验，为模型提供额外的空间信息。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 训练阶段方法需要访问并更新模型参数，而且换用模型或任务时往往需要重新适配，因而部署成本较高，难以直接用于不可训练或快速迭代的模型。
- 推理阶段增强方法主要面向输入或整体输出，没有显式定位、验证和纠正推理链中的单个空间证据；因此局部错误仍可能未被发现，并继续传播到最终答案。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种过程导向且无需训练的机制，能够把自由形式思维链中的空间判断拆成可追踪的证据单元，判断外部视觉证据是否足够可靠，并只在可靠矛盾出现时定位和修正错误，而不是笼统地重做整个答案。

</div>
<div markdown="1"><span>核心问题</span>

能否在不更新原多模态大语言模型参数的前提下，对其初始思维链进行证据级检查，可靠地找到最早与图像冲突的空间判断，并从该处修订后续推理，从而同时提高感知忠实性和最终答案准确率？

</div>
<div markdown="1"><span>作者直觉</span>

推理链中的早期空间判断类似后续推导的地基：若先把每个判断对应到具体物体、关系和来源步骤，再用足够可信的视觉测量检查它，就能在错误刚出现时截断传播。只从最早被可靠证据否定的位置重新推理，还可以保留此前有效的步骤；对置信度不足的检测或几何结果则不贸然纠错，以减少把正确判断改坏的风险。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法是一个模块化、免训练的推理时纠错框架。给定图像 $I$ 和问题 $q$，原始多模态大语言模型先生成推理链 $C=\{c_1,c_2,\ldots,c_n\}$ 及初始答案；框架随后把推理链中的空间判断拆成可独立核验的原子证据，构建空间证据图（Spatial Evidence Graph, SEG），再利用目标检测、分割和单目深度估计取得外部视觉证据。空间证据可靠性评估模块（Spatial Evidence Reliability Assessment, SERA）先判断这些视觉证据是否足够可信，再将每个空间证据单元标记为 Supported、Contradicted 或 Inconclusive，并按其来源步骤找到最早的可靠矛盾。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成初始推理与答案

将 $I$ 与 $q$ 输入待改进的原始 MLLM，生成由步骤 $c_k$ 组成的推理链 $C=\{c_1,c_2,\ldots,c_n\}$，以及对应的初始答案。

<div class="method-step__io" markdown="1">

**输入**：原始图像 $I$ 和问题 $q$。<br>
**输出**：未经验证的推理链 $C$ 和初始答案。

</div>

**直观理解**：先让模型按照原有能力完整作答，框架不改变其网络参数或解码函数，而是在答案生成后检查推理过程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 抽取空间证据并构建 SEG

通过提示 MLLM，从各推理步骤抽取目标存在性、图像绝对位置、二维相对关系和相对深度四类空间证据单元；每个单元记录涉及的实体、空间关系、证据类型及来源步骤，并被组织为空间证据图 $\mathcal{G}=(\mathcal{V},\mathcal{E},\mathcal{A})$。

<div class="method-step__io" markdown="1">

**输入**：初始推理链 $C$。<br>
**输出**：包含实体节点、空间关系边、证据属性和来源步骤的 SEG。

</div>

**直观理解**：这一步把散落在自然语言中的“杯子在盘子左边”等判断整理成结构化检查清单，同时保留每条判断在原推理链中的位置。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 获取视觉证据并评估可靠性

Grounding DINO 为实体提供候选框、定位分数和存在性分数；绝对位置及二维关系由边界框坐标支持，相对深度则结合 SAM2 的目标掩码与单目深度估计结果。SERA 根据存在确定性 $R_E(o)$、定位清晰度 $R_L(o)$ 和几何测量稳定性 $R_M(o)$ 计算实体证据可靠性 $g(o)$，并划分 HIGH、MEDIUM、LOW 三档。

<div class="method-step__io" markdown="1">

**输入**：SEG 中的实体与空间证据类型，以及原始图像 $I$。<br>
**输出**：与各实体和证据单元关联的视觉观测、可靠性分数及可靠性等级。

</div>

**直观理解**：外部视觉工具相当于核查员，但核查员本身也可能看错，因此框架会先检查检测框是否明确、目标是否确实存在，以及深度测量是否稳定。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 验证、定位最早矛盾并定向再生成

框架依照证据类型的验证规则，将空间证据标记为 Supported、Contradicted 或 Inconclusive；随后按来源步骤排序，选择最早一个被可靠视觉证据否定的单元，并把其位置、判定结果及视觉证据组成验证报告，交给同一 MLLM 重写受影响的后续推理和答案。

<div class="method-step__io" markdown="1">

**输入**：带来源步骤的空间证据单元、视觉证据及其可靠性等级。<br>
**输出**：纠正后的推理链与最终答案；若没有发现可靠矛盾，则保留原推理和原答案。

</div>

**直观理解**：框架不是要求模型从头随意反思，而是指出第一处有可信证据支持的错误，让模型只从该处开始修正后续推导，从而减少早期错误继续传播。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 空间证据单元与空间证据图表示

$$
\mathcal{G}=(\mathcal{V},\mathcal{E},\mathcal{A}),\qquad s_m=\left\langle o_i,r_m,o_j,t_m,k_m\right\rangle
$$

**符号说明**

- $\mathcal{G}$：空间证据图。
- $\mathcal{V}$：视觉实体节点与图像参考节点的集合。
- $\mathcal{E}$：有向空间关系边的集合。
- $\mathcal{A}$：证据类型、来源步骤及关联视觉证据等属性。
- $s_m$：从推理链中抽取的第 $m$ 个原子空间证据单元。
- $o_i$：证据单元中的主体视觉实体。
- $r_m$：第 $m$ 个证据单元编码的空间关系。
- $o_j$：关系涉及的客体实体或图像参考节点。
- $t_m$：证据类型，即目标存在性、绝对位置、二维相对关系或相对深度。
- $k_m$：该证据单元在原始推理链中的来源步骤编号。

<div class="equation-explanation" markdown="1">

**直观理解**：该表示把一句空间判断压缩成“哪个实体、与谁、具有什么关系、属于哪类证据、来自哪一步”。其中 $k_m$ 建立了验证结果与原推理链之间的直接索引，是定位最早错误并从该处继续生成的基础。<br>
**原文位置**：第 3.1 节 Spatial Evidence Graph Construction

</div>

</div>

<div class="equation-block" markdown="1">

#### SERA 实体级视觉证据可靠性

$$
\begin{aligned}R_E(o)&=2\left|p_{\mathrm{yes}}(o)-0.5\right|,\\R_L(o)&=\min\left(\sigma(s_1),\sigma(s_1-s_2)\right),\\R_M(o)&=\begin{cases}1,&\text{for non-depth evidence units},\\a_{\mathrm{mask}}(o)d_{\mathrm{stable}}(o),&\text{for relative-depth evidence units},\end{cases}\\a_{\mathrm{mask}}(o)&=\sigma\left(\log_{10}\left(\max(|M_o|,1)\right)-\theta_m\right),\\d_{\mathrm{stable}}(o)&=\sigma\left(\theta_d-\operatorname{Std}(D_o)\right),\\g(o)&=R_E(o)^\alpha R_L(o)^\beta R_M(o)^\gamma,\qquad \alpha+\beta+\gamma=1,\\\operatorname{tier}(o)&=\begin{cases}\mathrm{HIGH},&g(o)\geq\tau_h,\\\mathrm{MEDIUM},&\tau_l\leq g(o)<\tau_h,\\\mathrm{LOW},&g(o)<\tau_l.\end{cases}\end{aligned}
$$

**符号说明**

- $o$：待评估的视觉实体。
- $p_{\mathrm{yes}}(o)$：实体 $o$ 出现在图像中的概率，取值范围为 $[0,1]$。
- $R_E(o)$：存在可靠性；存在概率越远离不确定点 $0.5$，其值越高。
- $s_1$：Grounding DINO 对实体 $o$ 给出的最高原始定位分数。
- $s_2$：Grounding DINO 对实体 $o$ 给出的第二高原始定位分数。
- $\sigma(\cdot)$：Sigmoid 函数，用于将输入平滑映射到 $0$ 与 $1$ 之间。
- $R_L(o)$：定位可靠性，取最高候选置信度与前两名候选分数间隔所对应可靠度的较小值。
- $R_M(o)$：几何测量可靠性；非深度证据不需要额外测量，故设为 $1$。
- $M_o$：SAM2 为实体 $o$ 生成的分割掩码，$|M_o|$ 表示有效掩码面积。
- $D_o$：实体 $o$ 的掩码区域内的深度值集合。
- $a_{\mathrm{mask}}(o)$：掩码面积充分性；有效区域越大，该项通常越高。
- $d_{\mathrm{stable}}(o)$：深度一致性；区域内深度标准差越小，该项通常越高。
- $\theta_m$：控制掩码面积充分性映射的阈值参数。
- $\theta_d$：控制深度稳定性映射的阈值参数。
- $\operatorname{Std}(D_o)$：实体掩码区域内深度值的标准差。
- $g(o)$：实体 $o$ 的综合视觉证据可靠性分数。
- $\alpha,\beta,\gamma$：存在、定位和测量可靠性的非负权重，其和为 $1$。
- $\tau_h$：HIGH 与 MEDIUM 可靠性之间的阈值，文中设为 $0.75$。
- $\tau_l$：MEDIUM 与 LOW 可靠性之间的阈值，文中设为 $0.45$。
- $\operatorname{tier}(o)$：实体证据所属的 HIGH、MEDIUM 或 LOW 可靠性等级。

<div class="equation-explanation" markdown="1">

**直观理解**：SERA 先分别询问三个问题：目标是否明确存在或不存在、检测位置是否唯一清楚、用于空间关系判断的几何量是否稳定。加权几何平均具有“短板效应”，例如检测框很确定但深度区域极不稳定时，综合分数仍会降低；分档结果随后决定视觉证据能否支持明确的 Supported 或 Contradicted 判定。<br>
**原文位置**：第 3.2 节 Reliability-Aware Spatial Verification

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该框架不训练或微调 MLLM、Grounding DINO、SAM2 或单目深度估计器，也没有通过损失函数更新参数；SEG 抽取、SERA 评分、规则验证和定向再生成均发生在推理阶段。因此，上述可靠性公式是证据筛选与决策规则，而不是需要梯度优化的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 空间证据图（SEG）**

SEG 写为 $\mathcal{G}=(\mathcal{V},\mathcal{E},\mathcal{A})$：$\mathcal{V}$ 包含视觉实体节点和图像参考节点，$\mathcal{E}$ 是有向空间关系边，$\mathcal{A}$ 保存证据类型、来源步骤和视觉证据。目标存在性作为实体节点属性，绝对位置及实体间关系表示为有向边，因此自然语言判断可以被单独验证并追溯至原始步骤。

> 直观理解：SEG 的作用是把长篇推理转换成带出处的“实体—关系—实体”记录；发现错误后，系统能够知道错的是哪条空间判断以及它来自第几步。

**2. 空间证据可靠性评估（SERA）**

SERA 从三个方面评估实体 $o$ 的视觉证据：$R_E(o)$ 衡量存在概率距离不确定点 $0.5$ 有多远，$R_L(o)$ 同时考虑最佳检测候选的置信度及其相对次佳候选的分数间隔，$R_M(o)$ 衡量几何测量是否稳定。三者通过加权几何平均得到 $g(o)$，使任何关键分量过低都会明显压低总可靠性，避免以模糊检测或不稳定深度结果作出过度肯定的纠错。

> 直观理解：即使某个工具给出答案，也要判断它是否“看得清”：候选位置相互竞争、目标区域太小或区域内深度波动过大时，系统宁可判为无法确定，也不据此改写原推理。

**3. 最早矛盾定位与定向再生成**

验证结果按照证据单元的来源步骤 $k_m$ 排序，系统只在存在可靠 Contradicted 判定时选取最早矛盾，并将该步骤、判定和视觉证据写入验证报告。报告连同原图和问题输入同一 MLLM，用于重新生成受该错误影响的后续推理与最终答案；没有可靠矛盾时不触发修改。

> 直观理解：早期错误往往会使后面的推理连续偏离，因此优先修正第一处确定错误，比笼统要求模型全面反思更有针对性；保留无可靠矛盾的答案也可降低误改风险。

**训练与推理**

完整过程仅包含推理：首先由原始 MLLM 根据图像 $I$ 和问题 $q$ 生成初始推理链与答案；随后再次利用提示抽取四类空间证据单元并建立 SEG。框架按证据类型调用外部视觉工具：Grounding DINO 提供实体候选框、定位分数及存在性信息，SAM2 为深度关系涉及的实体生成掩码，单目深度估计器计算掩码内深度统计；SERA 据此评估证据可靠性并执行空间验证。最后，若存在被可靠视觉证据否定的单元，则把最早矛盾的来源步骤、判定和视觉证据交给同一 MLLM，只重写受影响的后续推理和最终答案；否则直接返回初始结果。

**复现信息**

公平解释该方法时需要注意三点。第一，框架依赖现成的 Grounding DINO、SAM2 和单目深度估计器提供独立视觉证据，但不改变原 MLLM 的生成函数或解码程序。第二，存在性单元只有在 $R_E(o)\geq\tau_h$ 时才作明确判断：对于正向存在声明，若 $p_{\mathrm{yes}}(o)>0.5$ 则为 Supported，若 $p_{\mathrm{yes}}(o)<0.5$ 则为 Contradicted；负向声明反转标签，低于阈值则为 Inconclusive。第三，文中设定 $\tau_h=0.75$、$\tau_l=0.45$；具体抽取提示、各空间关系的验证规则及再生成提示位于附录 B、附录 C，所给节选未完整列出这些内容，因此仅凭当前材料不能复现全部规则和提示模板。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- RealWorldQA：使用765个样本，考查真实世界场景理解；它是主消融、阈值敏感性、空间证据忠实度和人工验证实验的核心数据集，适合检验方法在复杂自然图像中的实际有效性。
- GQA：使用balanced test-dev划分的12,578个样本，重点考查对象属性与空间关系推理；同时在固定子集上测量推理过程中空间证据忠实度的变化，用于判断最终准确率提升是否伴随中间推理质量改善。
- POPE：使用其3,000个样本划分，专门考查图像中对象是否存在及对象幻觉；它补充了RealWorldQA和GQA，使总体评测不仅覆盖空间关系，也覆盖错误感知对象所导致的推理失败。另有LLaVA-Bench-in-the-Wild的60个样本和MMHal-Bench的96个样本参与完整的15种模型—数据集组合评测，但受列表数量限制不在此逐项展开。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**最终答案准确率（Accuracy）**

衡量模型最终回答与标准答案是否一致。RealWorldQA、GQA和POPE优先采用确定性的答案抽取与规范化规则，仅在规则无法判断时调用GPT-4o进行文本语义等价判定；LLaVA-Bench-in-the-Wild和MMHal-Bench则对有效样本统一采用GPT-4o二元语义正确性判断。后者可写为$\mathrm{Acc}_{\mathrm{GPT\text{-}4o}}=N_{\mathrm{correct}}/N_{\mathrm{scored}}$，其中$N_{\mathrm{correct}}$是被判为正确的样本数，$N_{\mathrm{scored}}$是成功获得有效判断的样本数。 （越高越好，因为它直接反映任务回答正确的样本比例；但它只评价最终输出，不能单独说明推理链是否忠实。）

</div>
<div class="metric-item" markdown="1">

**空间证据忠实度（SEF）**

对样本$i$，定义$\mathrm{SEF}_i=S_i/(S_i+C_i)$，其中$S_i$与$C_i$分别是被视觉证据支持和反驳的空间证据单元数量；被判为无法确定的单元不进入该比值。实验同时使用人工评价和自动评价，以检查中间推理中的空间判断是否与图像一致。 （越高越好，因为更高比例的可判定空间证据得到图像支持；但该指标不直接衡量答案是否正确，也可能受到证据抽取和验证器误差影响。）

</div>
<div class="metric-item" markdown="1">

**中间组件质量指标**

抽取器采用严格字段及来源步骤完全匹配下的Precision、Recall和F1；验证器采用三分类准确率、Macro-F1、可判定单元准确率（Dec. Acc.）与覆盖率（Coverage）。这些指标分别检验空间证据是否被完整抽取、Supported／Contradicted／Inconclusive三类是否判断正确，以及高置信判定覆盖了多少单元。 （总体上越高越好；其中Macro-F1强调三类的均衡识别，Dec. Acc.与Coverage必须联合解读，因为只对少量容易样本作出决定也可能得到较高准确率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三种骨干模型、五个基准组成的15种模型—数据集设置，与Vanilla及其他推理时增强或验证方法比较

<div class="result-value" markdown="1">

本文方法在15种设置中的11种取得最佳结果；作者还在摘要中报告总体平均准确率为68.94%，相对所比较基线平均高8.55个百分点。

</div>

这说明方法的优势并非局限于单个骨干或单一任务类型，且总体排名优于比较方法。分析上，它支持“核验并纠正中间空间证据具有较好的跨设置适用性”，但仍有4种设置未获最佳，因此不能证明其在所有模型和数据分布上都占优；摘要中的68.94%与正文按骨干报告的均值采用了不同聚合视角，复核时应结合完整表2确认计算口径。

<div class="result-source" markdown="1">

来源：第4.2节，表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Tab. 2, our method achieves the best performance in 11 of the 15 model–dataset settings.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 按骨干模型汇总五个基准上的Vanilla与完整框架准确率

<div class="result-value" markdown="1">

Qwen平均准确率由64.33%升至70.59%，增加6.26个百分点；InternVL由56.11%升至68.55%，增加12.44个百分点；Llama由63.55%升至67.68%，增加4.13个百分点。

</div>

三个骨干均有正向变化，且InternVL增益最大，表明框架能帮助不同初始能力的模型，但收益幅度明显依赖骨干模型。该结果没有隔离SEG、SERA和纠错提示各自的贡献，也不能排除不同模型生成的CoT质量对增益大小的影响。

<div class="result-source" markdown="1">

来源：第4.2节，表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Specifically, the average accuracy increases from 64.33% to 70.59% for Qwen, from 56.11% to 68.55% for InternVL, and from 63.55% to 67.68% for Llama.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### RealWorldQA与GQA各200个固定样本上的Vanilla和完整框架比较，同时进行人工与自动SEF评价

<div class="result-value" markdown="1">

RealWorldQA的人工SEF由82.12%升至92.47%，自动SEF由81.79%升至91.40%，准确率由45.00%升至57.00%；GQA的人工SEF由90.94%升至96.70%，自动SEF由90.03%升至95.60%，准确率由62.00%升至69.00%。

</div>

中间空间证据忠实度与最终准确率同步上升，支持作者关于框架不仅改变答案、也改善推理链视觉一致性的主张。人工和自动SEF趋势接近，也为自动验证结果提供一定可信度。不过这是相关性证据而非严格因果证明，且只覆盖两个固定子集；不能据此断言每个被纠正的证据单元都会直接导致正确答案。

<div class="result-source" markdown="1">

来源：表3，第4.3节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

RealWorldQA | 82.12 → 92.47 (+10.35) | 81.79 → 91.40 (+9.61) | 45.00 → 57.00 (+12.00); GQA | 90.94 → 96.70 (+5.76) | 90.03 → 95.60 (+5.57) | 62.00 → 69.00 (+7.00)

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 若干关键诊断实验使用较小固定子集：表3每个数据集200例、图5每个数据集500例、阈值实验100例、人工组件验证共100条CoT回答。原文未明确报告重复抽样、置信区间或统计显著性，因此这些差异的抽样稳定性尚不清楚。
- 最终答案评价部分依赖GPT-4o：两个开放式基准全部由其二元判分，另外三个基准在规则无法判断时也调用它；未成功判分的样本还会被排除出分母。虽然温度设为0且提示词统一，这仍可能引入外部判分器偏差。与此同时，表6中Contradicted类F1为58.82%，说明自动验证器对关键反例证据的识别仍可能限制纠错可靠性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Vanilla：直接使用骨干多模态模型进行原始推理，不增加空间信息、验证或纠错模块；它给出各骨干模型自身的性能基准，并用于测量完整框架的净增益。
- SpatialPIN：代表推理时空间信息增强方法；该比较用于区分“补充初始空间线索”与本文“核验并纠正中间空间证据”两种路线的效果。
- SoM（Set-of-Mark）：通过视觉标记帮助模型指认和区分图像实体，代表显式视觉提示增强；它检验仅改善实体定位提示是否足以替代推理链核验。
- FaithAct：代表针对模型推理或回答进行事实忠实性检查的验证方法；与之比较可判断面向原子空间证据、视觉可靠性及最早错误定位的专门设计是否更有效。完整实验还包含ByDeWay与GoM，但受基线数量限制不在此逐项展开。

**实验想回答的问题**

- 该训练自由框架能否在不同多模态大语言模型与不同视觉问答任务上稳定提高最终答案准确率，并优于仅补充空间信息或进行一般性事实核验的推理时方法？
- 性能提升是否确实来自中间空间证据忠实度的改善，以及空间证据图（SEG）与空间证据可靠性评估（SERA）是否分别提供了不可替代的作用？

**实验实现**

实验使用Qwen3-VL-8B-Instruct、InternVL3.5-8B和Llama-3.2-11B-Vision-Instruct三种骨干模型，并在五个基准上形成15种模型—数据集设置；所有方法使用相同样本与评价流程。RealWorldQA、GQA和POPE先执行确定性答案抽取与规范化，仅在结果不确定时调用温度为0、最大输出8个token的GPT-4o文本判分器，而且只保留模型回答末尾4,500个字符用于评价。LLaVA-Bench-in-the-Wild与MMHal-Bench直接使用GPT-4o作YES／NO语义正确性判断，未成功判分的样本从分母中排除。忠实度实验使用RealWorldQA与GQA各200个样本进行表3评价，图5则使用各500个固定样本；人工组件验证从两个数据集各随机抽取50条CoT回答，并对所得291个证据单元标注Supported、Contradicted或Inconclusive。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| RealWorldQA上分别移除SEG或SERA，并跨Qwen3-VL-8B、InternVL3.5-8B和Llama-3.2-11B比较 | 完整模型在三个骨干上的准确率分别为66.93%、66.14%和61.18%；移除SEG后分别降至63.92%、63.01%和58.56%，平均下降2.92个百分点；移除SERA后分别降至62.88%、61.96%和57.65%，平均下降3.92个百分点。 | 移除SEG把证据退化为扁平列表，因而隔离了实体、关系、视觉证据与来源步骤之间结构化连接的价值；移除SERA则保留证据收集但取消可靠性估计和门控，检验是否需要过滤不可靠视觉证据。两者均下降说明两个模块都有贡献，而SERA下降更大，表明防止噪声证据触发错误纠正尤其重要。由于实验只在RealWorldQA上进行，模块贡献能否以相同幅度迁移到其他四个基准仍未得到证明。 | 表4，第4.4节“Component ablation”<br><span class="experiment-evidence">Qwen3-VL-8B \| 66.93 \| 63.92 (-3.01) \| 62.88 (-4.05); InternVL3.5-8B \| 66.14 \| 63.01 (-3.13) \| 61.96 (-4.18); Llama-3.2-11B \| 61.18 \| 58.56 (-2.62) \| 57.65 (-3.53)</span> |
| Qwen3-VL-8B-Instruct在RealWorldQA固定100样本子集上的SERA可靠性阈值敏感性 | 宽松阈值$\tau_l=0.35,\tau_h=0.65$时SEF为84.04%、准确率为51%；默认阈值$\tau_l=0.45,\tau_h=0.75$时SEF为89.36%、准确率为55%；严格阈值$\tau_l=0.55,\tau_h=0.85$时SEF为86.17%、准确率为52%。 | 默认阈值同时取得最高SEF和准确率，体现可靠性门控存在覆盖范围与证据质量之间的折中：阈值过低会让噪声证据触发纠错，过高则使更多证据被判为无法确定。默认设置只比宽松和严格设置高4与3个准确样本，且样本量仅100；原文未报告方差或显著性检验，因此不能断言该阈值在其他模型和数据集上普遍最优。 | 表5，第4.4节“Threshold sensitivity”<br><span class="experiment-evidence">Loose \| 0.35 \| 0.65 \| 84.04 \| 51; Default \| 0.45 \| 0.75 \| 89.36 \| 55; Strict \| 0.55 \| 0.85 \| 86.17 \| 52</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出训练免费的视觉证据验证与纠错框架，以提升多模态模型的空间链式推理。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`e3edbb3af95009df60888cd820da25b41c6a81ef8d547e8918eaed8b5b7d5506`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
