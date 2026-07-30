---
title: "[论文解读] LLMET: Enabling Cross-Layer Evaluation of Emerging M3D Memories for Energy-Efficient LLM Serving"
description: "[arXiv 2607.26491][LLM 效率] 本文提出跨层仿真框架 LLMET，用于判断单片三维集成（M3D）带来的超大容量片上存储器，能否通过减少片外内存访问来降低大语言模型服务的芯片能耗。"
arxiv_id: "2607.26491"
announcement_date: "2026-07-30"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:04.164474+00:00"
source_sha256: "cc5e9139e938409a5a2a3d60041d0b05ff071f3fc7b23dee33d11629cb818bee"
tags:
  - "LLM 效率"
  - "LLM 其他"
  - "大语言模型推理服务"
  - "单片三维集成"
  - "片上缓存"
  - "高带宽存储器"
  - "键值缓存"
  - "存储层次"
  - "数据移动能耗"
  - "跨层模拟"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2607.26491</p>

# LLMET: Enabling Cross-Layer Evaluation of Emerging M3D Memories for Energy-Efficient LLM Serving

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Ming-Yen Lee, Hanchen Yang, Faaiq Waqar, Harsono Simka, Tushar Krishna, Muhammed Ahosan Ul Karim, Shimeng Yu</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26491v1) · [PDF 下载](https://arxiv.org/pdf/2607.26491v1) · **关键词** 大语言模型推理服务, 单片三维集成, 片上缓存, 高带宽存储器, 键值缓存, 存储层次, 数据移动能耗, 跨层模拟  


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

本文提出跨层仿真框架 LLMET，用于判断单片三维集成（M3D）带来的超大容量片上存储器，能否通过减少片外内存访问来降低大语言模型服务的芯片能耗。

**不用术语来说**：大语言模型推理需要反复搬运体积庞大的模型权重和用于保存上下文的 KV 缓存；当容量有限的片上缓存放不下这些数据时，芯片必须频繁访问片外高带宽内存，而数据搬运本身会消耗大量能量。新型 M3D 存储技术有望显著扩大片上缓存，但缓存越大也会增加自身的访问能耗和芯片面积，因此不能仅凭容量推断其是否真正节能。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出 LLMET，将大语言模型执行轨迹与后端功耗、性能和面积（PPA）模型连接起来，并支持新型 M3D 存储器，从而分析工作负载、缓存层次、硬件映射与器件特性之间的跨层影响。
- 作者利用该框架跨模型、应用和硬件平台评估大容量片上存储器对推理能效的影响，并据此提炼面向未来大语言模型加速器与嵌入式存储器的设计方向。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型（LLM）推理服务中的存储层次与芯片能耗问题。解码器式 Transformer 的推理分为预填充（prefill）和解码（decode）：预填充并行处理全部输入并建立键值缓存，主要执行大规模矩阵乘法，通常受计算能力限制；解码则逐 token 生成输出，每一步都要读取模型权重及不断增长的键值缓存，通常受存储带宽限制。由于现有加速器仅有数十 MB 片上缓存，而模型权重和键值缓存可达数 GB，数据必须频繁往返于片上缓存与高带宽存储器（HBM）；原文指出一次 HBM 访问的能耗约比片上 SRAM 访问高两个数量级，因此减少片外流量是降低 LLM 服务能耗的关键。单片三维集成（M3D）可在逻辑芯片后端互连层中垂直集成高密度、低漏电的嵌入式存储器，有望把片上缓存扩展至数百 MB，但其容量、访问特性、映射策略与实际 LLM 工作负载之间存在跨器件、体系结构和应用层的相互作用，不能仅凭缓存容量或带宽推断最终节能效果。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**预填充与解码（prefill/decode）**

预填充阶段一次性并行处理输入提示，生成首个输出 token，并为各 Transformer 层建立键值缓存，通常偏计算受限。解码阶段自回归地逐个生成 token，每一步都需读取模型权重和已有键值缓存，因此通常偏存储受限。

</div>
<div class="conceptitem" markdown="1">

**键值缓存（KV cache）**

注意力层会保存历史 token 的 key 和 value 张量，后续生成时直接复用，避免重复计算。其容量随批大小和序列长度近似线性增长，长上下文与高吞吐服务因而会显著增加存储压力。

</div>
<div class="conceptitem" markdown="1">

**单片三维集成存储器（M3D memory）**

M3D 将高密度存储单元直接制造在逻辑芯片的后端互连层（BEOL），垂直位于前端逻辑（FEOL）之上；本文关注基于非晶氧化物半导体器件的类 eDRAM 缓冲器。与键合独立 SRAM 裸片的传统 3D 缓存相比，其堆叠结构更薄，有望获得更高密度、更短互连和更好的热特性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务是评估：使用新兴 M3D 存储技术持续扩大 LLM 加速器的片上缓存，能否在不同模型、输入/输出长度、推理阶段和硬件平台上有效降低芯片能耗。输入包括 LLM 结构与精度、工作负载的输入和输出 token 长度、预填充或解码阶段、加速器计算与存储层次配置，以及候选 M3D 存储器的功耗、性能和面积特性；评估过程需要追踪算子执行及模型权重、激活和 KV 缓存在片上缓存与 HBM 之间的实际流量，并考虑缓存容量、数据映射和算子融合。输出是平台的性能、面积与分组件能耗估计，重点判断缓存扩容减少的 HBM 访问能耗是否足以抵消更大片上存储器自身的访问和静态能耗。研究场景同时覆盖服务器和边缘推理，并分别分析计算受限的预填充与存储受限的解码；核心假设是 M3D 可提供远大于传统片上 SRAM 的可用容量，但其系统收益必须通过跨层建模而非仅按容量或带宽估算。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$L_{\mathrm{in}}$**

一次推理请求的输入 token 数，用于描述提示或上下文长度；这是为解释问题设置采用的通用记号，原文节选未给出专门符号。

</div>
<div class="notationitem" markdown="1">

**$L_{\mathrm{out}}$**

一次请求生成的输出 token 数，决定自回归解码步数；这是通用记号，原文节选未明确规定。

</div>
<div class="notationitem" markdown="1">

**$C_{\mathrm{L2}}$**

加速器 L2 片上缓存容量，是本文考察的主要设计变量；原文节选以 MB 或 GB 给出容量，但未定义公式符号。

</div>
<div class="notationitem" markdown="1">

**$E_{\mathrm{chip}}$**

芯片完成目标推理工作负载所消耗的总能量，包含计算、片上存储与片外存储访问等组成；原文节选未给出统一符号。

</div>

</div>

**直接相关的工作**

- **LLMCompass**: 它是与本文最接近的硬件设计探索工具，能够建模存储层次流量以及芯片面积，但采用固定分块策略，主要报告面积和成本，不能充分揭示片上容量增长时片外流量如何变化；同时不支持新兴 M3D 存储、完整的缓存感知映射与分组件能耗分析。
- **LLMServingSim 2.0**: 它面向异构或解耦式 LLM 服务系统，主要通过系统级或基于实测画像的方法模拟调度、吞吐和功耗指标。相较之下，本文需要解析到单芯片存储层次流量与访问能耗，并把新兴存储器的器件级 PPA 特性连接到应用级推理行为。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

随着大语言模型部署规模和上下文长度增长，模型权重与 KV 缓存造成的片上缓存—HBM 数据传输逐渐成为加速器的重要能耗来源；与此同时，硬件功率、散热能力和电费均限制服务系统继续扩展。因此，系统设计者需要知道扩大片上存储是否能减少高代价的片外流量，并在不同推理阶段、模型规模和平台上获得实际能效收益。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **面向 LLM 服务的系统级性能建模与优化工具**：Calculon、Vidur、GenZ、DynamoLLM 和 LLMServingSim 2.0 等工具主要以解析模型、执行配置或已有硬件测量数据估计吞吐率、延迟、平台需求或集群级能耗，并据此优化调度和系统配置。
- **内存层次与大容量片上缓冲设计**：相关研究通过增大片上缓冲区、保存或预取 KV 缓存，减少对 HBM 带宽的需求；LLMCompass 等工具还能描述部分内存层次流量或探索容量扩展及硬件映射，但重点通常是性能、面积或成本。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有系统级或集群级研究往往依赖概要数据，或者只建模容量、带宽、吞吐率和延迟，无法追踪到单芯片缓存与片外内存的具体访问能耗；其后果是难以判断总体节能究竟来自何处，也不能可靠比较缓存扩容的收益与额外开销。
- 既有工具没有同时覆盖新型 M3D 存储器、详细内存层次流量、缓存感知的算子映射或融合，以及完整的功耗—性能—面积分解；因此，器件和电路层提出的高密度存储方案无法直接转化为对真实 LLM 服务工作负载的系统级结论。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一个经过验证的统一评估方法，能够把 M3D 存储器的容量、访问代价和面积特性，与 LLM 的执行轨迹、算子映射、缓存命中及 HBM 流量联系起来，并据此量化不同模型、应用、推理阶段和平台上的净能耗变化。

</div>
<div markdown="1"><span>核心问题</span>

作者要回答的核心问题是：新兴 M3D 存储器支持的持续片上缓存扩容，是否能够在实际 LLM 服务中带来有意义的能效提升，以及这种收益在何种工作负载和硬件条件下成立？

</div>
<div markdown="1"><span>作者直觉</span>

HBM 访问通常比片上访问更耗能；若更大的 M3D 缓存能让模型权重或 KV 缓存更长时间留在芯片内部，就可能用较便宜的片上访问替代昂贵的片外搬运。不过，超大缓存本身也有面积和访问能耗，且预填充与解码阶段的数据复用模式不同，所以需要从器件、缓存流量到完整模型执行进行联合核算，而不能假设缓存越大必然越好。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

LLMET 是一个面向 LLM 推理的跨层仿真框架：输入模型参数与目标硬件配置，前端逐算子生成包含张量形状、分块方案、缓存容量适配映射、各级存储访问字节数和计算周期的执行轨迹；后端再结合具体器件模型，估算面积、性能与能耗（PPA），并细分到 DRAM、L2/L1、寄存器文件、计算单元和片上互连。其关键区别在于，缓存容量变化不仅会改变每次访问的成本，还会触发不同的矩阵映射与注意力融合策略，因此能够评价超大 M3D 片上存储是否真正减少片外流量和系统能耗。
直观而言，LLMET 不把新型存储器简单替换成一个更省电的存储模块，而是先判断“增大的缓存能否装下哪些数据、由此能否少搬几次数据”，再把每一次计算和搬运映射到经过器件级校准的能耗与面积模型。这使器件层的 2T 增益单元、三维堆叠等设计选择可以一路传导到 LLM 服务的系统级结果。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 解析模型与硬件配置

前端将推理过程分解为算子，并记录每个算子的类型与输入、输出张量形状；同时实例化与目标架构对应的硬件资源。

<div class="method-step__io" markdown="1">

**输入**：LLM 模型参数，以及目标平台的计算单元、存储层次、L2 容量、片外存储和互连等硬件配置。  
**输出**：待映射的逐算子工作负载，以及目标硬件模型。

</div>

**直观理解**：这一步先回答“要算什么”和“机器有什么”。只有同时知道张量规模和缓存容量，才能判断哪些数据可以留在芯片内。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 容量感知的分块、映射与算子融合

对矩阵乘法，框架在 L2 能容纳一个输入操作数时将较小矩阵固定在片上，另一矩阵从 DRAM 分块流入，并按剩余容量从四种映射情形中逐算子选择；对注意力，则采用按头调度与跨算子融合，并在容量允许时固定 GQA 中复用的 KV 头。

<div class="method-step__io" markdown="1">

**输入**：逐算子张量形状、可用 L2 容量及目标硬件资源。  
**输出**：每个算子的分块尺寸、容量适配映射情形、融合计划，以及哪些数据驻留片上或从 DRAM 流入的决定。

</div>

**直观理解**：缓存增大并不自动等于节能，关键是它是否跨过了某个“装得下”的门槛。LLMET 会随容量改变执行方案，而不是对所有缓存大小沿用同一套固定分块。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成跨存储层与计算单元的执行轨迹

前端统计每个算子在 RF、L1、L2、DRAM 和芯片间链路上的读写字节数，并计算各功能单元所需周期；融合后的注意力中间结果若能驻留片上，则不计入 DRAM 往返。

<div class="method-step__io" markdown="1">

**输入**：已确定的算子映射、分块和融合计划。  
**输出**：逐算子轨迹，包含算子类型、张量形状、分块尺寸、映射情形、各层读写流量和各功能单元计算周期。

</div>

**直观理解**：这相当于生成一份细粒度账单：每项计算做了多久，每份数据在寄存器、缓存和片外内存之间搬了多少字节。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 器件校准的 PPA 与分组件能耗评估

后端使用技术相关的单位访问能耗、面积和计算代价累加系统 PPA，并将能耗分解到 DRAM、L2/L1/RF、脉动阵列、向量单元和片上互连；M3D 模型还纳入 2T-GC 器件参数与三维层堆叠面积代价。

<div class="method-step__io" markdown="1">

**输入**：逐算子执行轨迹，以及 SRAM、M3D 2T-GC、计算单元、片上互连和 HBM/LPDDR I/O 的器件模型。  
**输出**：目标模型和平台下的系统面积、性能、总能耗及硬件组件级能耗构成。

</div>

**直观理解**：最后把轨迹中的每一次访问和计算乘以对应硬件的实际代价。这样既能看总能耗是否下降，也能判断节省来自减少 DRAM 流量，还是来自某个片上组件。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="equation-block" markdown="1">

#### 单个注意力头的片上工作集条件

$$
W_{\mathrm{head}}=n_{\mathrm{seq}}\,d_{\mathrm{head}}\,b\left(|Q|+|K|+|V|+|A|\right),\qquad W_{\mathrm{head}}\le C_{L2}
$$

**符号说明**

- $W_{\mathrm{head}}$：按头融合执行时需要同时驻留片上的工作集字节数。
- $n_{\mathrm{seq}}$：输入序列长度，即上下文中的 token 数。
- $d_{\mathrm{head}}$：单个注意力头的特征维度。
- $b$：每个张量元素占用的字节数，对应原文中的 bytes。
- $|Q|,|K|,|V|,|A|$：原文对查询、键、值和注意力输出张量所计入份数的记号；四者共同决定该头需要驻留的数据量。
- $C_{L2}$：可用于该执行计划的 L2 缓存容量。

<div class="equation-explanation" markdown="1">

**直观理解**：序列越长、单头维度越大或数据精度越高，一个注意力头所需的片上空间就越大。只有该工作集能放入缓存，QK^T、softmax 与 SV 之间的中间结果才可以一直留在片上，从而避免写入和重新读取 DRAM；其中不等式是对原文“fits in the cache”的显式表达。  
**原文位置**：第 3.2 节 Capacity-Aware Mapping + Operator Fusion，注意力按头融合的工作集描述。

</div>

</div>

<div class="equation-block" markdown="1">

#### GQA 共享 KV 头的 L2 驻留条件

$$
C_{L2}\ge n_{\mathrm{kv}}\,n_{\mathrm{seq}}\,d_{\mathrm{head}}\,b
$$

**符号说明**

- $C_{L2}$：L2 缓存容量。
- $n_{\mathrm{kv}}$：需要共同驻留并被查询头组复用的 KV 头数量。
- $n_{\mathrm{seq}}$：序列长度。
- $d_{\mathrm{head}}$：每个 KV 头的维度。
- $b$：每个元素占用的字节数，对应原文中的 bytes。

<div class="equation-explanation" markdown="1">

**直观理解**：右侧估算共享 KV 数据的容量需求；当 L2 至少达到该大小时，KV 头可以在一个查询头组的整个处理期间固定在片上，不必为每个查询头重复从 DRAM 加载。该门槛在至少 16K token 的长上下文中尤其关键，因为此时 KV 数据可能主导片外流量。  
**原文位置**：第 3.2 节 Capacity-Aware Mapping + Operator Fusion，GQA 的 KV 固定条件。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。LLMET 是用于评估 LLM 推理工作负载的分析与仿真框架，不训练模型，也没有通过梯度优化的学习目标；其“优化”表现为依据缓存容量选择映射、分块和融合方案，再用器件校准模型评估这些离散设计选择的 PPA。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 容量感知映射器**

矩阵乘法映射器根据 L2 是否能容纳一个输入操作数及其剩余容量，在四种算子融合或映射情形中逐算子选择；较小操作数可作为静态操作数固定在片上，另一操作数按块从 DRAM 流式读取。该设计显式建模缓存容量变化引起的片外流量阶跃，而非采用与容量无关的固定分块。

> 直观理解：它解决的是“缓存变大以后程序会不会换一种更省搬运的算法安排”。如果仍固定采用原来的分块方式，就可能低估超大缓存的收益，也可能错误地认为增加容量总能带来同等比例的节省。

**2. 注意力跨算子融合与 GQA 数据驻留**

框架将注意力中的 QK^T 与 SV 阶段按注意力头连续调度，使每个头只需从 DRAM 加载 Q、K、V 并写回注意力输出 A，中间 logits 和 softmax 结果保留在片上。对于分组查询注意力（GQA），若 L2 足以容纳共享的 KV 头，则在同组全部查询头之间固定这些 KV 数据，避免重复加载。

> 直观理解：普通执行可能把前一步的中间结果写到显存，下一步再读回来；融合则让两步紧接着完成，中间数据不离开芯片。GQA 中多个查询头共用 K、V，若缓存装得下，只加载一次即可，长上下文时尤其重要。

**3. 器件校准的跨层 PPA 后端**

计算单元模型来自 ASAP7 RTL 综合；RF、L1、L2 SRAM 使用 NS-Cache，M3D 2T-GC 也采用 NS-Cache 流程，但替换为 2T-GC 器件模型并使用三维层堆叠面积代价；片上互连使用 NeuroSim，HBM/LPDDR I/O 使用代工厂报告的单位比特能耗。后端据此输出组件级而非仅聚合级的能耗与面积结果。

> 直观理解：新型存储尚未必有完整芯片可直接测量，因此需要从晶体管和电路模型推算每比特访问的能耗与面积。组件级拆分还能说明一种存储技术为何有效，而不只是给出一个无法诊断的总功耗数字。

**训练与推理**

该方法仅覆盖推理评估。给定既有 LLM 的参数和张量规模以及目标硬件配置，LLMET 先将推理分解为算子，再逐算子执行容量感知映射：矩阵乘法尝试固定较小输入，注意力按头融合 QK^T、softmax 与 SV，并在满足容量条件时保留共享 KV。随后生成各级存储读写量和功能单元周期轨迹，后端将轨迹与指定 SRAM 或 M3D 2T-GC 等器件模型结合，输出面积、性能、总能耗和组件级能耗分解。原文节选未描述模型权重训练、微调、校准数据集或真实请求调度过程。

**复现信息**

复现或公平解释该方法所需的核心模型来源包括：计算单元采用 ASAP7 RTL 综合结果；RF、L1 和 L2 SRAM 采用 NS-Cache；M3D 存储使用同一 NS-Cache 流程中的 2T-GC 器件模型，并以三维层堆叠面积代替二维 H-tree 面积处理；片上互连采用 NeuroSim；HBM/LPDDR I/O 能耗采用代工厂报告的单位比特数据。框架必须保留逐算子的映射情形、各级存储读写字节数及功能单元周期，否则无法复现容量变化对片外流量和组件能耗的传播。作者还报告后端硬件校准相对公开 A100 芯片面积的误差在 7% 以内（图 4），但本节选未给出四种映射情形的完整算法、具体器件参数、时钟频率或数值配置，相关复现信息需进一步核对原文算法与附录。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- 服务器工作负载：Llama 3.1 70B运行于双NVIDIA A100类7 nm平台，主要评估prefill阶段；序列长度覆盖2K至32K，并在固定2K序列长度时扫描批大小。这里没有传统训练/测试数据集划分，输入长度和批大小构成合成工作负载，用于测试缓存复用、HBM流量与总能耗的关系。
- 技术扩展工作负载：Llama 3.1 405B运行于8张NVIDIA B200-like、3 nm平台，平台参数由公开Blackwell性能指标相对A100外推。实验重点考察更大模型、更多GPU及更先进工艺下，GB级缓存的最佳容量是否向更长序列和更大容量移动。
- 边缘工作负载：INT4量化的Llama 3.2 1B运行于Jetson Orin NX-class类7 nm平台，权重约486 MB，主存为LPDDR5。四种输入/输出长度从256/128到4096/512 token，分别评估prefill与decode；256 MB被视为近期可行的面积上限，512 MB至1 GB仅作为完整片上驻留的敏感性上界。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**片外存储器访问量或相对访问降幅**

统计推理过程中访问HBM或LPDDR5的数据流量，并相对平台基线报告降幅。它直接衡量更大L2是否保留了可复用的权重、中间结果或注意力数据，从而减少昂贵的数据搬运。 （访问量越低或降幅越高越好，因为片外数据搬运的单位比特能耗通常显著高于片上访问；但该指标不能单独保证总能耗下降，因为更大的L2自身也会消耗更多访问能量。）

</div>
<div class="metricitem" markdown="1">

**总推理能耗或相对节能率**

同时计入计算和数据搬运能耗，用于判断减少片外访问后是否获得净能效收益。实验分别分析prefill和decode，并通过分项能耗解释计算、L2访问和DRAM/HBM访问的贡献。 （总能耗越低或节能率越高越好；这是核心系统指标，因为它会扣除超大缓存自身增加的访问开销。）

</div>
<div class="metricitem" markdown="1">

**芯片面积开销**

比较不同缓存容量和实现技术对应的总芯片面积或相对面积增长，并以A100公开数据验证后端PPA模型。该指标检验节能配置是否具有物理实现可行性。 （在达到相同容量和能效目标时越低越好；对于面积严格受限的边缘设备，容量即使节能，也可能因面积不可接受而不能成为近期设计方案。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 双A100服务器上运行Llama 3.1 70B，扫描2K至32K序列长度，并将L2由40 MB基线扩大到最高1 GB。

<div class="result-value" markdown="1">

作者报告，扩大片上缓存最多减少95%的HBM访问并降低44%的总能耗；结合摘要给出的代表配置，44%节能对应16K上下文的prefill。随着上下文变长，可利用的数据复用减少，收益逐渐饱和，且最佳容量会随工作负载变化。

</div>

大缓存让映射和算子融合产生的中间数据更多地留在芯片内，因此长上下文、低批量的prefill能显著减少HBM搬运。不过，这不证明缓存越大越好：当新增容量已不能消除更多HBM访问时，更大缓存自身的访问能耗会抵消收益；结论也依赖LLMET模型而非实芯片上的1 GB缓存测量。

<div class="result-source" markdown="1">

来源：第4.2节，图5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">First, increasing on-chip cache capacity reduces HBM accesses by up to 95% and total energy by 44%, enabled by higher data reuse through cache-aware mapping and operator fusion.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 8×NVIDIA B200-like、3 nm平台上运行Llama 3.1 405B，考察更大模型和先进平台中的GB级L2扩展。

<div class="result-value" markdown="1">

作者报告，在32K输入长度下，HBM访问最高减少95%，prefill能耗最高降低24%；对于16K至64K序列，2 GB至4 GB是最低prefill能耗的推荐区间，而短于16K时256 MB至512 MB通常已足够。

</div>

模型和平台规模扩大后，能够产生净收益的缓存容量及其峰值收益点向更长序列移动，但峰值节能率低于A100案例。结果表明缓存容量必须按模型和上下文选择，而不能直接把A100上的最佳配置等比例复制过去；B200-like平台参数来自外推，因此不等同于对真实B200硬件的测量结论。

<div class="result-source" markdown="1">

来源：第4.3节，图8

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">As illustrated in Figure 8, we observe a maximum HBM access reduction of 95% and peak energy savings of 24% at a 32K input length.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Jetson Orin NX-class类边缘平台运行INT4 Llama 3.2 1B，在四种工作负载上将L2由8 MB扫描至1 GB，并分别评估prefill与decode。

<div class="result-value" markdown="1">

当L2超过约486 MB的量化模型占用、进入约512 MB以上的完整权重驻留区间后，DRAM访问下降超过90%；在1 GB容量时，四种工作负载的decode总能耗降低75%至80%。但论文将512 MB至1 GB视为面积上较激进的上界，而非近期边缘缓存目标。

</div>

decode会反复读取模型权重，因此只要整个模型能留在片上，就能近乎消除权重的片外读取；这解释了容量跨过模型大小时的突跃。该结果不表示1 GB缓存适合现实边缘芯片：论文认为近期较实际的上限约为256 MB，此时只能获得较温和的decode收益，而且短提示prefill还可能因L2访问能耗增加而没有净节能。

<div class="result-source" markdown="1">

来源：第4.4节，图9

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Once the L2 capacity exceeds the quantized model footprint (≈512 MB), the weights become fully resident, DRAM accesses drop by more than 90%, and decode energy is reduced by 75–80% at 1 GB across all workloads.</span>

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

- A100基线：40 MB二维SRAM L2缓存。它对应参考A100平台的原始缓存规模，是判断M3D扩容是否减少HBM流量、能耗以及增加芯片面积的直接比较对象。
- B200-like基线：128 MB二维SRAM L2缓存。该基线适配更先进的3 nm、8 GPU平台，用来区分工艺和平台升级本身与进一步采用GB级M3D缓存带来的收益。
- 边缘基线：8 MB二维SRAM L2缓存。它代表面积受限的边缘加速器配置，所有边缘DRAM访问和总能耗降幅均相对该配置计算。
- 容量与技术对照：在各平台上，从小容量平面SRAM扫描到采用M3D 2T-GC的数百MB或GB级缓存；其中2T-GC按每层128 MB堆叠。该对照不仅测试“容量更大”，也检验平面SRAM在GB级时的布线和面积代价是否使M3D成为更现实的实现方式。

**实验想回答的问题**

- 在服务器、先进工艺和边缘三类部署中，扩大片上L2缓存能否通过减少HBM或LPDDR5访问，降低LLM推理总能耗；其收益如何随上下文长度、批大小、模型规模和推理阶段变化？
- 相较于平面SRAM，单片三维集成的2T增益单元存储器（M3D 2T-GC）能否以可接受的面积与访问能耗实现数百MB至GB级片上缓存，以及不同工作负载对应的能效最优容量是多少？

**实验实现**

LLMET采用跨层评估：前端建立在已验证并针对NVIDIA A100校准的LLM推理框架上，模拟算子映射、分块、融合及缓存复用；后端利用ASAP7 RTL综合、NS-Cache和NeuroSim建立逻辑、SRAM及M3D存储器的功耗—性能—面积模型。7 nm平台通过ASAP7综合评估，3 nm平台使用与2024 IRDS路线图对齐的NeuroSim投影值；B200-like参数则由公开Blackwell指标相对A100外推。各部署分别扫描L2容量，并报告片外流量、包含计算和数据移动的总能耗以及面积开销。表2给出的单位访问能耗显示，例如7 nm下40 MB SRAM、1 GB SRAM和1 GB 2T-GC分别为0.495、2.78和1.08 pJ/bit，而HBM2E为6.6 pJ/bit；这些数值说明扩大缓存既可能节省片外能耗，也可能因片上访问变贵而出现收益饱和。面积模型与公开A100数据比较时，总裸片面积和核心面积估计误差均在7%以内。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 固定2K序列长度，改变服务器prefill的批大小，并比较不同缓存容量。 | 批大小增大时，HBM流量和总能耗收益比随序列长度增长时更快饱和；在2K注意力中，40 MB至128 MB缓存已经能提供较高复用，而更大批量增加计算能耗，使降低内存流量对总能耗的占比变小。 | 该扫描隔离了批量维度，说明“大工作负载”并不必然更需要大缓存。注意力按批次处理时，跨批数据未必产生额外缓存复用；同时计算能耗上升会稀释内存节能。因此，长上下文低批量与短上下文高批量即使token总量相近，也可能需要不同缓存配置。 | 第4.2节，图6<br><span class="experiment-evidence">One reason is that attention at 2K already achieves high reuse with modest cache sizes (e.g., 40MB–128MB), so larger batches provide limited additional memory benefit because attention is processed batch-by-batch.</span> |
| 将A100上的1 GB缓存分别按二维实现与M3D方式实现，并与40 MB二维缓存基线比较面积。 | 二维缓存从40 MB扩展到1 GB会显著增大总芯片面积；采用M3D集成时，1 GB缓存相对40 MB基线的面积开销可控制在23%以内。 | 这一对照主要隔离存储器集成方式，而不只是容量效应：如果1 GB全部铺在逻辑平面上，布线和面积可能使方案失去可行性；垂直堆叠则用第三维承载容量。23%面积开销说明M3D明显改善可实现性，但仍不是零成本，也没有直接证明制造良率、散热或封装问题已经解决。 | 第4.1节，图4<br><span class="experiment-evidence">In contrast, M3D integration keeps the area overhead of a 1GB cache within 23% relative to the 40MB baseline.</span> |

**定性案例**

- 图10的Voice/Cmd边缘案例分解了单层能耗：小缓存decode由DRAM读取主导，缓存增大后权重逐步留在片上，只有进入512 MB至1 GB完整驻留区间时DRAM读取才近乎消失；prefill则不同，增加的L2读写能耗可能抵消DRAM节省。该案例用于解释同一硬件扩容为何对decode明显有利，却可能对短提示prefill无效甚至不利。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work studies large on-chip memory technologies and cross-layer simulation for reducing LLM serving energy.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`cc5e9139e938409a5a2a3d60041d0b05ff071f3fc7b23dee33d11629cb818bee`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
