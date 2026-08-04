---
title: "[论文解读] SG-Layout: Structured Scene Graph-Guided Layout Generation with LLMs"
description: "[arXiv 2608.01106][LLM Reasoning] SG-Layout旨在通过将显式场景图对齐并注入大语言模型，使模型能把自然语言中的对象关系转化为更准确、几何一致且可执行的二维或三维布局。"
arxiv_id: "2608.01106"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:01:50.229178+00:00"
source_sha256: "79bdaa1e487a887884873c94f51217741f53d3ad818dff60dd2adb1a3f53662a"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "布局生成"
  - "场景图"
  - "大语言模型"
  - "图—语言特征对齐"
  - "空间推理"
  - "LoRA"
  - "室内场景合成"
  - "对象重排"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.01106</p>

# SG-Layout: Structured Scene Graph-Guided Layout Generation with LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Junsheng Wang, Chao Chen, Mengying Xie, Mingyan Li, Fuqiang Gu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Chongqing University, Chongqing, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01106v1) · [PDF 下载](https://arxiv.org/pdf/2608.01106v1) · **关键词** 布局生成, 场景图, 大语言模型, 图—语言特征对齐, 空间推理, LoRA, 室内场景合成, 对象重排<br>


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

SG-Layout旨在通过将显式场景图对齐并注入大语言模型，使模型能把自然语言中的对象关系转化为更准确、几何一致且可执行的二维或三维布局。

**不用术语来说**：用户可以用语言描述“物体是什么、应放在哪里、彼此有什么关系”，但语言常有歧义，也不会自然给出精确的坐标、尺寸和朝向；当对象增多、关系变密时，大语言模型容易理解大意却排错位置，产生关系冲突、几何不一致或不适合机器人执行的布局。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出两阶段图引导框架SG-Layout：先将场景图中的对象、属性及空间关系编码并对齐到大语言模型的语言潜在空间，再针对指令驱动的布局生成进行适配。
- 设计关系图编码器与投影器完成图—语言特征对齐，并使用LoRA适配器在冻结主干模型的条件下进行参数高效调优，以兼顾结构化空间推理、主干稳定性和训练成本。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

布局生成旨在依据自然语言描述、语义标签或任务指令，输出对象的位置、尺寸与朝向等结构化几何属性。它位于高层语义规划与低层图像合成或机器人执行之间：在二维图像生成中，布局用于约束对象的空间安排并提高图文一致性；在三维室内场景与机器人重排中，布局还必须满足可执行的尺度、位姿和物理约束。大语言模型具有较强的语义理解和指令跟随能力，但其原生输入是文本，难以仅凭含糊的语言稳定表达多对象之间明确且可组合的空间依赖。本文因此引入场景图，将对象及其属性表示为节点、将语义或空间关系表示为边，并把这种结构化信息作为大语言模型生成几何布局的显式条件。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**场景图**

场景图是一种关系图，其中节点表示对象及其属性，边表示对象之间的语义关系或空间关系。它把“椅子在桌子左侧”等自然语言约束拆成明确的对象与关系，便于组合和检查。

</div>
<div class="concept-item" markdown="1">

**图—语言特征对齐**

图编码器先把场景图转换为连续向量，投影器再将这些向量映射到大语言模型能够处理的语言潜在空间或词元空间。通俗地说，这一步相当于为结构化图信息建立一个大语言模型可理解的接口。

</div>
<div class="concept-item" markdown="1">

**LoRA 指令微调**

LoRA 是一种参数高效微调方法，通过训练附加的低秩适配参数来改变模型行为，同时保持预训练主干参数冻结。本文用它让模型学习根据指令和图特征生成布局，以降低完整微调的计算与参数成本，并尽量维持原模型能力。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文研究文本条件下的布局生成，覆盖二维图像布局、三维室内场景合成和机器人对象重排三种设置。输入是描述对象及空间要求的自然语言指令；系统先将指令解析为场景图，其中对象及属性构成节点、对象间的语义与空间关系构成边，再将图特征与语言表示共同提供给大语言模型。输出是可供后续视觉生成或机器人执行使用的结构化布局，包括对象框、位置、尺寸和位姿等具有度量意义的几何属性。问题的核心假设是自然语言能够被解析为足以表达任务约束的场景图；生成结果不仅需要语义上符合指令，还需要在几何上保持空间一致性，并在涉及三维场景时兼顾越界、碰撞等物理可行性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **LayoutGPT**: LayoutGPT 使用大语言模型规划器，把自然语言转换为类似 CSS 的空间描述和层次化布局，并可借助外部布局示例提供上下文。它代表以文本提示或检索文本为主要条件的布局生成路线；本文指出，这类表示在多对象关系复杂时缺少场景图所提供的显式结构约束。
- **GraphGPT**: GraphGPT 将图输入与大语言模型对齐，用于图条件下的指令跟随和推理，说明图结构可以接入语言模型。SG-Layout 借鉴图—语言对齐思路，但任务目标由图理解转为布局合成，输出必须包含对象框、位置与位姿等度量几何属性，并接受空间一致性和物理可行性评价。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

布局生成是连接高层自然语言指令与下游视觉生成或机器人执行的中间环节：文本到图像系统需要对象位置与尺度符合描述，室内场景合成需要合理的三维位置和姿态，机器人重排则需要可直接执行的空间配置。因此，系统不仅要识别指令中的对象语义，还要把多项空间约束落实为准确的位置、尺寸和朝向；复杂场景中的任一关系理解错误，都可能导致生成图像语义失真、室内物体发生物理冲突，或机器人得到不可行的操作目标。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **纯文本驱动的大语言模型布局生成**：利用大语言模型的语义理解、推理和指令遵循能力，直接把自然语言描述转换为对象的位置、尺寸、方向等结构化布局参数。
- **检索增强布局生成**：LayoutGPT、SKE-Layout等方法从外部布局知识库中检索与当前任务相关的示例，并将其作为上下文提供给大语言模型，以缓解布局数据不足和空间推理能力有限的问题。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 自然语言本身具有歧义，缺少场景图那样明确的对象—关系结构；仅依赖文本时，模型难以稳定保留对象之间的组合依赖，场景越复杂、关系越密集，越容易遗漏或错误解释空间约束。
- 检索示例可以提供经验参照，却没有解决结构化空间知识与文本原生大语言模型之间的表示鸿沟；模型仍需从文本上下文中间接推断度量信息，因而难以把语言线索可靠地落到正确的对象尺寸、位置和姿态上。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种同时满足两项要求的机制：一方面把场景图的节点、属性和关系编码成大语言模型能够解释的表示；另一方面在不进行昂贵全参数微调、也不破坏预训练语言主干的前提下，将这些图结构信息有效用于布局生成并支持复杂关系的结构泛化。

</div>
<div markdown="1"><span>核心问题</span>

能否通过图—语言特征对齐和参数高效指令调优，使文本原生的大语言模型显式利用场景图中的对象关系，从而在二维图像布局、三维室内场景和机器人对象重排中生成语义与几何更一致的布局，同时保持预训练主干冻结？

</div>
<div markdown="1"><span>作者直觉</span>

场景图把一句可能含糊的描述拆成对象节点和关系边，相当于先把“有哪些东西、谁相对谁处于什么位置”整理成可检查的关系清单；关系图编码器负责汇总这张清单，投影器再把图表示翻译到大语言模型熟悉的表示空间。完成这种对齐后，模型可同时利用图结构的明确约束和语言模型的语义、指令遵循能力；LoRA只调整少量适配参数，则使模型学会在生成布局时使用这些信息，而无需改写整个主干模型。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SG-Layout把自然语言布局生成改写为“文本语义与显式空间图共同条件化的序列生成”问题。输入是描述对象及其相互位置的用户指令$u$；系统先借助GPT-4o按预设规则将其解析为场景图$\hat{G}=(V,E)$，其中节点保存对象身份与属性，有向边保存left_of、right_of、front_of、behind、above、below等空间关系。关系图Transformer将图编码为结构表示$Z_G$，投影器再把$Z_G$映射为与语言模型词元同维、同空间的图词元$T_G$；图词元与指令词元$T_u$拼接后送入冻结的Qwen3-8B，并通过可训练LoRA适配器生成序列化布局，最后解析为对象类别、坐标和尺寸组成的二维或三维布局$\hat{L}$。

方法的关键不是让语言模型仅凭文字“记住”空间关系，而是先把“哪些对象通过什么关系连接”整理成机器容易操作的图，再把这张图翻译成语言模型能读取的连续向量。训练分成两个阶段：第一阶段只训练图编码器和投影器，使图词元进入语言模型后能够支持场景描述，从而完成图空间到语言空间的对齐；第二阶段冻结图侧模块，训练LoRA，使模型依据指令和已对齐的图词元输出具体几何布局。这样把表示对齐与任务适配分开，减少小规模可训练参数同时承担“理解图”和“学习布局格式”两项工作的难度。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 指令解析与场景图构建

在规则约束下调用GPT-4o，把$u$解析为有向场景图$\hat{G}=(V,E)$；节点$v_i=(id_i,p_i)$记录对象身份$id_i$及属性$p_i$，边$e_{ij}=r_{ij}$以多热向量表示对象$i$指向对象$j$的一种或多种空间关系。

<div class="method-step__io" markdown="1">

**输入**：自然语言用户指令$u\in U$，其中描述需要出现的对象及对象间的定性空间关系。<br>
**输出**：结构化场景图$\hat{G}$，包含对象集合$V$和带方向、带类型的关系集合$E$。

</div>

**直观理解**：这一步把“椅子在桌子左边”从一句话改写成“椅子节点$\rightarrow$桌子节点，边类型为left_of”。方向不能忽略，因为$e_{ij}\neq e_{ji}$，交换两个对象通常会改变关系含义。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 关系图编码与跨模态投影

默认使用关系图Transformer $f_{\mathrm{RGT}}$聚合节点及类型化关系，得到节点与关系感知表示$Z_G=f_{\mathrm{RGT}}(\hat{G})$；随后通过投影器$f_{\mathrm{proj}}$得到图词元$T_G=f_{\mathrm{proj}}(Z_G)$，使其维度和潜在表示空间与LLM输入词元兼容。

<div class="method-step__io" markdown="1">

**输入**：场景图$\hat{G}$及其中的对象属性、边方向和关系类型。<br>
**输出**：可直接注入语言模型输入序列的连续图词元$T_G$。

</div>

**直观理解**：图编码器负责读懂连接结构，投影器则像一个接口转换器，把“图模型使用的表达方式”转换成“语言模型能接收的表达方式”。没有这一层对齐，即使图中关系正确，LLM也无法直接解释图嵌入。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 图文融合与LoRA条件生成

按$T=[T_G;T_u]$拼接图词元和文本词元，并输入带LoRA适配器的Qwen3-8B；主干参数$\theta$保持冻结，仅低秩更新$\Delta\theta_{\mathrm{LoRA}}$在第二训练阶段被优化，模型自回归地产生布局文本序列。

<div class="method-step__io" markdown="1">

**输入**：投影后的图词元$T_G$和由分词器生成的指令词元$T_u=f_{\mathrm{Tokenizer}}(u)$。<br>
**输出**：隐藏状态$H$以及由其逐词元预测的序列化布局，包括对象类别与几何属性。

</div>

**直观理解**：模型同时看到原始要求和一份结构化“关系提纲”：文本保留自然语言语义，图词元强调必须满足的对象依赖。LoRA只给冻结模型增加少量可训练低秩参数，因此无需全面改写80亿参数主干。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 布局解码与结构恢复

解码函数$f_{\mathrm{Decode}}$把文本序列解析为$\hat{L}=\{o_i\}_{i=1}^{n}$，其中三维对象$o_i=(id_i,x_i,y_i,z_i,w_i,h_i,d_i)$包含类别、位置和尺寸；二维任务沿用同一模式，但省略不使用的深度维度。

<div class="method-step__io" markdown="1">

**输入**：LLM生成的序列化布局及其隐藏状态$H$。<br>
**输出**：可用于渲染和几何评估的二维或三维结构化预测布局$\hat{L}$。

</div>

**直观理解**：语言模型输出的不是最终图像或三维网格，而是一份可解析的对象清单及数值参数。后处理程序据此恢复边界框或三维包围盒，从而检查位置关系、重叠和越界等几何性质。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 图文融合的条件布局生成

$$
Z_G=f_{\mathrm{RGT}}(\hat{G}),\quad T_G=f_{\mathrm{proj}}(Z_G),\quad T_u=f_{\mathrm{Tokenizer}}(u),\quad H=f_{\mathrm{LLM}}([T_G;T_u];\theta,\Delta\theta_{\mathrm{LoRA}}),\quad \hat{L}=f_{\mathrm{Decode}}(H)
$$

**符号说明**

- $\hat{G}$：从用户指令解析得到的有向场景图。
- $f_{\mathrm{RGT}}$：关系图Transformer编码函数。
- $Z_G$：包含节点语义和类型化关系信息的图表示。
- $f_{\mathrm{proj}}$：将图表示映射到LLM词元空间的投影器。
- $T_G$：投影后可供LLM读取的图词元序列。
- $u$：自然语言用户指令。
- $T_u$：用户指令经过分词和嵌入后形成的文本词元序列。
- $[T_G;T_u]$：沿序列维度拼接图词元与文本词元得到的联合输入。
- $\theta$：训练期间保持冻结的Qwen3-8B主干参数。
- $\Delta\theta_{\mathrm{LoRA}}$：第二阶段可训练的低秩参数增量。
- $H$：LLM在图文联合条件下产生的隐藏表示。
- $f_{\mathrm{Decode}}$：把生成序列解析成对象级结构化布局的解码函数。
- $\hat{L}$：模型预测的二维或三维布局。

<div class="equation-explanation" markdown="1">

**直观理解**：该组合式公式概括了完整前向路径：先读取图结构，再把图表示转换成图词元，与指令词元共同输入LLM，最后把语言模型序列恢复为几何布局。它体现了SG-Layout的核心设计，即空间图不是额外的文字提示，而是经过专门编码和对齐后直接参与每一步条件生成。<br>
**原文位置**：第3.3节，公式(6)至(11)

</div>

</div>

<div class="equation-block" markdown="1">

#### 序列化布局生成损失

$$
\mathcal{L}_{\mathrm{gen}}=-\sum_{t=1}^{|L|}\log P(l_t\mid l_{<t},u,\hat{G})
$$

**符号说明**

- $\mathcal{L}_{\mathrm{gen}}$：布局序列的词元级交叉熵损失。
- $L$：序列化的真实布局目标。
- $|L|$：真实布局序列包含的词元数量。
- $t$：自回归生成过程中的词元位置。
- $l_t$：真实布局序列在位置$t$的目标词元。
- $l_{<t}$：位置$t$之前的真实布局词元；教师强制训练时将其作为历史条件。
- $u$：提供对象和空间要求的自然语言指令。
- $\hat{G}$：提供对象节点及成对空间关系的场景图。
- $P(l_t\mid l_{<t},u,\hat{G})$：给定先前布局词元、用户指令和场景图时，模型赋予正确下一词元的条件概率。

<div class="equation-explanation" markdown="1">

**直观理解**：训练在每个位置要求模型提高正确布局词元的概率，再把整段序列的负对数概率相加。由于预测同时以$u$和$\hat{G}$为条件，该目标不仅教授输出格式和坐标数值，也迫使可训练模块利用文本语义与图中成对关系；不过它本身没有单独加入碰撞、越界或关系违反的几何损失。<br>
**原文位置**：第3.4节，公式(12)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：监督数据被组织为三元组数据集$\mathcal{D}=\{(u_i,\hat{G}_i,L_i)\}_{i=1}^{N}$，其中$u_i$是指令，$\hat{G}_i$是对应场景图，$L_i$是真实结构化布局。目标布局先被序列化；训练采用教师强制，即预测位置$t$时输入真实前缀$l_{<t}$，并最小化词元级交叉熵$\mathcal{L}_{\mathrm{gen}}$。该损失通过下一词元预测间接学习对象类别、坐标和尺寸以及它们与指令、场景图之间的对应关系，原文没有报告额外的显式关系满足损失、碰撞惩罚或边界惩罚。

两个训练阶段使用交叉熵监督，但优化对象不同。阶段一以简短提示（如“Describe the room.”）和场景图为输入，以精炼场景描述为目标，冻结Qwen3-8B及LoRA，仅更新RGT和投影器，使$T_G$对冻结LLM具有可解释语义；阶段二改用指令到布局的监督，冻结主干、RGT和投影器，仅更新$\Delta\theta_{\mathrm{LoRA}}$，使模型学会在联合条件$[T_G;T_u]$下生成目标布局$L$。因此第一阶段解决“图向量怎样被语言模型理解”，第二阶段解决“怎样把已理解的图文条件转化为规定格式的布局”。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 关系图Transformer（RGT）**

RGT是默认场景图编码器，通过注意力机制建模带类型、带方向的关系，使$Z_G$同时包含节点语义和关系结构。论文还以R-GCN和加入关系类型嵌入的GAT作为替代编码器进行消融，但主方法采用RGT。

> 直观理解：普通文本模型容易把多个关系混在一起；RGT显式沿图边传播信息，使一个对象的表示能够结合它与其他对象之间的具体关系。它尤其服务于对象多、关系密集时的组合约束保持。

**2. 图语言投影器**

投影器$f_{\mathrm{proj}}$把图编码器输出$Z_G$映射为图词元$T_G$，目标是使图表示与LLM文本词元处于兼容的潜在空间。第一阶段在冻结LLM和LoRA的条件下，通过场景描述监督联合训练关系图编码器与投影器。

> 直观理解：图编码结果与单词嵌入原本属于不同表示体系，直接拼接没有可靠语义。投影器通过第一阶段训练学会让某种图结构产生可被冻结语言模型利用的向量。

**3. 冻结Qwen3-8B与LoRA适配器**

Qwen3-8B承担自回归布局序列建模，其原始参数$\theta$在两个阶段均冻结；第二阶段仅训练低秩增量$\Delta\theta_{\mathrm{LoRA}}$，而已经对齐的图编码器和投影器保持冻结。模型以$[T_G;T_u]$为联合条件预测目标布局序列。

> 直观理解：冻结主干保留预训练语言能力，LoRA则以较少参数教会模型遵循布局输出格式并利用空间条件。分阶段冻结还能避免布局微调反过来破坏已经学到的图语言对应关系。

**训练与推理**

训练前，作者分别为三类任务构造“指令—场景图—布局”三元组。二维图像布局来自筛选后的MSCOCO：去除过小或任务无关对象，按对象数量分组，由视觉语言模型提取候选场景图和适用性判断，再人工核验对象列表及成对关系；三维室内场景来自3D-FRONT/3D-FUTURE的卧室和客厅，读取家具类别、三维位置、尺寸、旋转及房间尺寸，并结合布局摘要与渲染图查询视觉语言模型生成有向场景图；物体重排采用SK-Dataset中带定性空间指令的关系子集。第一阶段对每个$\hat{G}$计算$Z_G$和$T_G$，与简短提示词元拼接后输入冻结LLM，通过场景描述目标反向传播，仅优化图编码器和投影器。第二阶段预先取得已对齐的$T_G$，与真实用户指令的$T_u$拼接，通过目标布局序列计算$\mathcal{L}_{\mathrm{gen}}$，仅更新LoRA参数。

推理时，系统接收新的自然语言指令$u$，先由GPT-4o在规则指导下生成$\hat{G}$，再由冻结的RGT和投影器产生$T_G$；分词器产生$T_u$，二者拼成$[T_G;T_u]$并输入带已训练LoRA的冻结Qwen3-8B。模型不再使用真实布局前缀，而是把自己先前生成的词元作为历史，自回归输出完整布局文本；解析器随后将其转换为$\hat{L}$。三维输出中每个对象含类别$id_i$、位置$(x_i,y_i,z_i)$和尺寸$(w_i,h_i,d_i)$；二维输出省略不用的深度相关维度。该流程依赖上游场景图解析质量：若GPT-4o遗漏对象或给出错误边，后续模块会把错误结构作为显式条件继续传播。

**复现信息**

主干语言模型为Qwen3-8B。默认图编码器为RGT，图编码器输出必须经投影器映射到与文本词元兼容的潜在空间；图词元位于文本词元之前，联合序列顺序为$[T_G;T_u]$。两个阶段均冻结LLM主干：第一阶段训练图编码器和投影器并冻结LoRA，第二阶段冻结图编码器和投影器并训练LoRA。布局以文本词元序列生成，再解析为对象级数值结构，这是复现输入输出协议和参数冻结策略所必需的信息。

原文节选未明确报告RGT层数、隐藏维度、投影器具体结构、LoRA秩及其插入层、优化器、学习率、批大小、训练轮数、坐标归一化或离散化方式、数值序列格式、解码温度和约束解析规则，因此不能据此完成逐参数复现。还需注意，训练数据中的场景图并非完全由同一流程自动得到：二维数据包含人工核验，三维数据结合结构化标注、渲染图和视觉语言模型，而在线推理描述为由GPT-4o按规则解析指令；这些数据来源与上游图构建差异会影响对方法增益及公平性的解释。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- NSR-1K：用于数值推理与空间推理，表 2 报告数据规模为 39,436。该数据集用于检验模型能否理解显式数量信息和对象间空间关系；当前节选未给出训练、验证和测试划分，也未说明 39,436 对应样本、指令还是场景的数量。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 二维图像布局生成

<div class="result-value" markdown="1">

作者概括称，SG-Layout 在包括二维图像布局生成在内的代表性空间推理任务上总体改善了空间理解与推理能力，并在复杂、关系密集的设置中优势最清楚；当前节选没有提供该任务的具体分数或逐基线排名。

</div>

这表明显式场景图可能帮助模型同时处理多个对象关系，而不只依赖文本序列中的隐式关系表示。由于缺少二维任务的结果表、指标定义和误差范围，该结论只能视为作者的总体实验陈述，不能据此判断提升幅度，也不能确认 SG-Layout 是否优于每一个参考基线。

<div class="result-source" markdown="1">

来源：第 4 节 Experiment

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across representative tasks involving spatial reasoning, including image layout generation, indoor scene synthesis and robotic object rearrangement, our proposed SG-Layout generally improves spatial understanding and reasoning ability, with the clearest advantages in complex and relation-dense settings.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 三维室内场景合成

<div class="result-value" markdown="1">

作者报告 SG-Layout 的总体优势覆盖三维室内场景合成，并强调复杂、关系密集场景中的改进最明显；当前节选未报告其相对 DiffuScene、InstructScene、GPT-4 或 SKE-Layout 的数值差异。

</div>

三维场景通常要求模型同时满足对象类别、几何位置和多条空间关系，因此这一结果与图编码器的设计目标相符。但“跨任务总体改善”不等于在所有场景、所有指标和所有基线上都占优；缺少逐项结果时，也无法排除改进主要集中于特定难度子集。

<div class="result-source" markdown="1">

来源：第 4 节 Experiment

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across representative tasks involving spatial reasoning, including image layout generation, indoor scene synthesis and robotic object rearrangement, our proposed SG-Layout generally improves spatial understanding and reasoning ability, with the clearest advantages in complex and relation-dense settings.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 机器人对象重排及与原始 Qwen3 骨干的总体比较

<div class="result-value" markdown="1">

作者称 SG-Layout 在对象重排任务上总体提升空间推理能力，并相对原始语言模型骨干取得明显更高的任务成功率；原文节选未给出成功率数值、统计波动或失败类型。

</div>

相对原始骨干的提高支持“结构化空间知识对任务有帮助”这一作者主张，因为两者至少共享 Qwen3-8B 骨干。不过，该比较本身仍不能区分提升来自图语言对齐、LoRA 指令微调还是二者共同作用；这一因果归因需要 Qwen3+LoRA 与 SG-Layout 的受控消融结果，而当前节选没有给出相应数值。

<div class="result-source" markdown="1">

来源：第 4 节 Experiment

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared to the original LLM backbone, SG-Layout achieves notably higher task success rates, confirming the effectiveness of incorporating graph-structured spatial knowledge.

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

- Qwen3：与 SG-Layout 使用相同的 Qwen3-8B 骨干和任务数据，是判断图结构增强相对于原始语言模型是否有效的核心受控基线。
- Qwen3+LoRA：在相同 Qwen3-8B 骨干和任务数据上进行 LoRA 微调，用于区分性能提升究竟来自一般性的任务微调，还是来自 SG-Layout 的场景图编码与图语言特征对齐。
- SKE-Layout：被用于二维图像布局、三维室内场景和对象重排三类任务，是覆盖范围最接近 SG-Layout 的参考方法；但节选未解释其模型规模、输入信息和训练数据是否与 SG-Layout 一致，因此它不是严格受控比较。
- GPT-4：作为二维布局中的 LayoutGPT 骨干之一，并在三维室内场景任务中直接作为参考基线，用于比较 SG-Layout 与较强闭源通用模型的空间生成能力；由于模型规模和标准设置不同，该比较主要反映任务表现，而不能单独归因于场景图设计。

**实验想回答的问题**

- 与原始 Qwen3-8B 以及仅进行 LoRA 指令微调的受控基线相比，引入场景图编码与图语言特征对齐后，SG-Layout 是否能提升布局生成中的空间理解、关系推理和任务成功率？
- 这种改进能否跨越二维图像布局、三维室内场景合成和机器人对象重排三类任务，并且在关系密集、组合结构复杂的场景中表现得更明显？

**实验实现**

作者采用 Qwen3-8B 作为骨干语言模型，并使用关系图 Transformer（RGT）作为图编码器，从场景图中提取对象的语义、几何特征以及“位于左侧”“位于前方”等空间关系。表 1 将比较分为两类：Qwen3、Qwen3+LoRA 和 SG-Layout 使用相同骨干与任务数据，构成可用于组件归因的受控比较；LayoutGPT、SKE-Layout、DiffuScene、InstructScene、GPT-4 和 LLM-GROP 则遵循各自标准设置，仅作为任务级参考。当前节选未提供数据划分、解码策略、随机种子、重复实验次数、统计显著性、硬件配置或具体评价指标，因而无法核验评测是否完全可复现，也不能把文中的“任务成功率”进一步对应到明确的计算公式。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The core contribution injects scene-graph structure into an LLM to improve explicit spatial and compositional reasoning for layout generation.; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`79bdaa1e487a887884873c94f51217741f53d3ad818dff60dd2adb1a3f53662a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
