---
title: "[论文解读] FiRE: Enhancing MLLMs with Fine-Grained Context Learning for Complex Image Retrieval"
description: "[arXiv 2607.27959][多模态 VLM] FiRE通过自动构建细粒度多模态五元组数据集，并将上下文推理与检索对齐拆分为两个微调阶段，使多模态大语言模型更好地处理组合图像、长文本和视觉对话等复杂图像检索任务。"
arxiv_id: "2607.27959"
announcement_date: "2026-07-31"
primary_category: "multimodal_vlm"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.290750+00:00"
source_sha256: "f4507013400f243b0bb14008a01def44d02907860ab5715cc9a2e11b1143f0fb"
tags:
  - "多模态 VLM"
  - "LLM 其他"
  - "复杂图像检索"
  - "多模态大语言模型"
  - "组合图像检索"
  - "细粒度上下文学习"
  - "查询—目标对齐"
  - "零样本检索"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">多模态 VLM · arXiv 2607.27959</p>

# FiRE: Enhancing MLLMs with Fine-Grained Context Learning for Complex Image Retrieval

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Hou, Bohan, Lin, Haoqiang, Song, Xuemeng, Wen, Haokun, Liu, Meng, Hu, Yupeng, Zhao, Xiangyu</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27959) · [PDF 下载](https://arxiv.org/pdf/2607.27959) · **关键词** 复杂图像检索, 多模态大语言模型, 组合图像检索, 细粒度上下文学习, 查询—目标对齐, 零样本检索<br>


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

FiRE通过自动构建细粒度多模态五元组数据集，并将上下文推理与检索对齐拆分为两个微调阶段，使多模态大语言模型更好地处理组合图像、长文本和视觉对话等复杂图像检索任务。

**不用术语来说**：复杂图像检索不只是按几个关键词找图：用户可能给出一张参考图并描述希望修改之处，也可能使用长篇描述或多轮对话表达目标。模型既要准确理解其中的对象、属性、关系和变化，又要从大量候选图像中识别最匹配的目标；只擅长理解语言或只擅长计算整体相似度，都不足以可靠完成这一过程。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出自动化的细粒度多模态五元组数据构建流程，并据此建立大规模数据集FiGMaQ；其中包含细粒度图像描述与修改文本，用于训练模型理解组合检索中的具体视觉内容和变化要求。
- 提出两阶段细粒度微调策略：先进行面向上下文推理的微调，再进行面向检索的微调，分别强化复杂查询理解与查询—目标对齐，避免将两种学习目标混在同一阶段。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究统一的复杂图像检索：系统需要在同一框架内处理长文本查询、视觉对话以及组合图像检索等不同输入形式，并从候选图像库中找出最符合用户意图的目标图像。传统视觉—语言预训练模型擅长把图像和短文本映射到可比较的表示空间，但面对包含大量细节、上下文依赖或推理关系的查询时理解能力不足；多模态大语言模型具有更强的上下文理解与推理能力，却原生面向生成任务，缺少检索所需的判别式查询—目标对齐能力。因此，该方向的核心问题是如何通过合适的数据与微调目标，使一个多模态大语言模型既能精细理解复杂查询，又能生成适合相似度匹配的检索表示。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多模态大语言模型（MLLM）**

能够联合处理图像与文本，并借助大语言模型进行上下文理解和推理的模型。它通常由视觉编码器、连接视觉与语言表示的适配模块以及大语言模型组成，但必须经过专门训练才能有效用于判别式检索。

</div>
<div class="concept-item" markdown="1">

**组合图像检索（CIR）**

查询由参考图像与修改文本共同构成，例如给定一张参考服装图并要求“改成红色且去掉袖子”，系统需检索满足修改要求的目标图像。其难点是同时保留参考图像中未被修改的内容，并准确落实文本指定的变化。

</div>
<div class="concept-item" markdown="1">

**查询—目标对齐**

将查询和候选目标编码为可比较的表示，使正确目标比无关目标具有更高相似度。生成式语言模型即使能解释查询，也不一定天然具备这种区分候选图像并排序的能力。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

设图像库为候选集合，系统接收复杂查询并输出按相关性排序的图像，其中查询可以是长文本、多轮视觉对话，或由参考图像与修改文本组成的组合输入。训练阶段重点利用组合式多模态数据；基础样本可表示为“参考图像、修改文本、目标图像”三元组，本文进一步构造包含参考图像与目标图像细粒度描述信息的五元组，以显式建模两幅图像之间的属性、对象和关系变化。论文关注统一模型及零样本迁移设置，即经过该训练后，不针对每个下游复杂检索数据集分别训练专用模型，而是直接评估其查询理解和目标排序能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$I_r$**

组合图像检索查询中的参考图像。

</div>
<div class="notation-item" markdown="1">

**$T_m$**

描述期望变化的修改文本。

</div>
<div class="notation-item" markdown="1">

**$I_t$**

应被检索到的目标图像。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{G}$**

检索时包含目标图像及其他候选图像的图像库。

</div>

</div>

**直接相关的工作**

- **MCL**: MCL将配有CLIP视觉编码器和适配器的语言模型同时用于多模态上下文描述与检索，并通过自动生成的MMC组合数据进行微调，说明组合式数据能够增强多模态输入理解。其生成流程依据参考图像及其描述产生修改描述和目标描述，却没有真实目标图像；原文据此指出所得三元组质量受限，且其上下文理解与检索目标处于既有微调范式中，构成本文进一步细化数据和拆分训练阶段的直接参照。
- **MagicLens**: MagicLens通过同一网页中的图像分组、自动元数据标注以及视觉和文本相似度筛选，自动发现真实的参考—目标图像对，再由语言模型生成修改文本，代表可扩展的全自动组合数据构造路线。本文指出其图像元数据较粗，只覆盖主体的一般和共性属性，因而难以支持复杂检索所需的细粒度差异理解；FiRE的数据管线正针对这一限制构造更细致的多模态组合样本。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现实检索需求具有多种输入形态：短文本可直接表达简单意图，但长文本检索、视觉对话检索和组合图像检索需要处理更长、更细致或同时包含图像与文本的查询。若为每一种任务单独开发模型，会带来较高训练成本和彼此割裂的解决方案，因此需要一个能够统一接收不同查询类型、并充分理解复杂搜索意图的图像检索模型。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于视觉—语言预训练模型的统一检索方法**：此类方法利用CLIP等视觉—语言预训练模型的多模态嵌入能力，把查询与候选图像编码到共享表示空间，再依据表示相似度完成排序。其优势是天然适合判别式匹配，并可在同一框架中支持多种检索任务。
- **基于LLM或MLLM微调的检索方法**：此类方法借助大语言模型的语言理解和推理能力，再通过微调补足生成式模型原本欠缺的查询—目标判别能力。例如，MCL联合训练多模态上下文描述生成与多模态上下文检索；E5-V则使用纯句子对微调预训练MLLM中的核心LLM，以增强查询和目标之间的对齐。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 视觉—语言预训练模型虽然具有较强的跨模态嵌入能力，但模型规模及推理能力相对有限，难以充分解析包含长描述、关系推断或多模态修改条件的复杂查询；其后果是模型可能只捕捉整体语义，而遗漏决定检索结果的细微属性与关系。
- 现有LLM或MLLM检索方法尚未充分利用细粒度上下文建模，并常将上下文理解与检索对齐目标纠缠在同一微调过程中。前者使训练监督不足以明确刻画对象、属性和修改要求，后者则可能让“理解查询”和“学会排序”相互干扰，从而限制复杂检索性能。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作证明了MLLM可以作为较通用的图像检索器，但仍缺少一套相互配合的数据与训练机制：训练数据需要显式提供细粒度图像描述和修改信息，优化过程则需要把复杂上下文推理与判别式查询—目标对齐分开学习。这个缺口在组合图像检索、长文本检索和视觉对话检索中尤其突出。

</div>
<div markdown="1"><span>核心问题</span>

能否通过自动构建具有细粒度语义监督的多模态组合数据，并采用“先理解与推理、后检索与对齐”的两阶段微调方式，在不为各类任务分别训练专用模型的情况下，提高MLLM对多种复杂图像检索任务的统一零样本迁移能力？

</div>
<div markdown="1"><span>作者直觉</span>

复杂检索可以类比为先读懂需求清单，再按清单筛选商品：第一阶段让模型逐项理解参考图像、文本描述及其要求的变化，减少对关键细节的遗漏；第二阶段再专门训练模型把理解后的查询表示与正确目标拉近、与不匹配图像区分开。细粒度五元组数据为前一步提供明确线索，目标解耦则使两个阶段各自解决更单一的问题，因此有望得到更稳定的复杂查询表示和更准确的候选排序。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

FiRE由“自动构造细粒度五元组数据”和“分阶段微调统一检索模型”两部分组成。首先，系统从图像集合中识别语义相关但在局部属性、对象数量或空间关系等方面存在差异的图像对，为每幅图像生成细粒度描述，再据此生成贴近用户表达习惯、不会直接泄露目标图像全部内容的修改文本，最终形成包含参考图像、目标图像及相关文本信息的FiGMaQ五元组。随后，以BLIP-3-4B为骨干，先训练模型根据参考图像和修改文本推理目标内容，再训练其把复合查询与目标图像映射到相近的嵌入位置，并用召回代理损失直接强化排序能力。
直观地说，第一阶段先教模型“看懂改动后应该得到什么图像”，第二阶段再教它“从图库里把这幅图找出来”。这种先理解、后检索的解耦设计避免模型同时学习语言生成与排序时相互干扰；训练完成后，同一个检查点可在组合图像检索、长文本检索、视觉对话检索和普通文本到图像检索中直接进行零样本评测。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 相关图像对识别与细粒度语义过滤

先将模型训练为图像编码器，再依据图文对比相似度筛选语义相关的候选图像对；过滤使用下、上阈值$\theta_l=0.6$与$\theta_h=0.83$，排除无关图像以及几乎相同、缺少有效修改空间的图像。

<div class="method-step__io" markdown="1">

**输入**：候选图像集合，以及用于数据构造的BLIP-3-4B多模态模型。<br>
**输出**：语义主题相近但仍具有可描述细粒度差异的参考图像—目标图像对。

</div>

**直观理解**：这一步不是随意配对图片，而是在“完全不同”和“几乎一样”之间寻找难度适中的样本，使后续修改既合理又确实需要细致观察。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 细粒度描述与人类式修改文本生成

模型为两幅图像生成覆盖对象、属性、数量、布局与局部细节的长描述，再由LLM比较两份描述并生成相对简短、带一定模糊性的修改文本；专门的提示约束修改文本聚焦关键变化，而非完整复述目标图像。

<div class="method-step__io" markdown="1">

**输入**：筛选后的参考图像和目标图像，以及两幅图像各自的细粒度描述。<br>
**输出**：FiGMaQ细粒度多模态五元组，其中包含参考端、目标端及支持组合查询和目标内容推理的文本信息。

</div>

**直观理解**：细描述相当于给数据生成器一份完整的“找不同”清单，而最终修改文本只保留用户通常会说出的关键要求，避免把检索任务变成直接照抄答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 第一阶段：细粒度上下文推理微调

以参考图像和修改文本构成复合查询，训练MLLM生成或表征目标图像应具有的细粒度语义，使模型先学习从当前视觉内容与语言改动推断目标内容。

<div class="method-step__io" markdown="1">

**输入**：参考图像、修改文本和目标图像的细粒度描述。<br>
**输出**：具备细粒度多模态组合推理能力的中间模型。

</div>

**直观理解**：模型先回答“按这些要求修改后，目标应该长什么样”，而不是立刻面对整个图库做排序，因此更容易建立对象、属性和关系变化之间的联系。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 第二阶段：细粒度检索微调

继续优化查询—目标对比学习目标，并加入面向$\mathrm{Recall@1}$和$\mathrm{Recall@5}$的可微召回代理损失，使正确目标的相似度超过负样本；该阶段采用温度$\tau'=0.01$，召回代理温度$\tau_1=1$、$\tau_2=0.01$，权重$\beta_1=0.4$、$\beta_2=0.15$。

<div class="method-step__io" markdown="1">

**输入**：第一阶段模型、由参考图像与修改文本组成的查询，以及对应目标图像和批内负样本。<br>
**输出**：可将复杂多模态查询与候选图像编码到统一检索空间的最终FiRE模型。

</div>

**直观理解**：第一阶段保证模型大体理解要求，第二阶段进一步要求正确图片排在前几名，尤其直接关注第一名和前五名是否命中。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文将优化过程分为两个连续目标：第一阶段面向目标内容生成或细粒度上下文推理，第二阶段面向查询—目标嵌入对齐，并把图像—文本对比损失与召回代理损失联合起来。第二阶段的召回项覆盖$\mathrm{Recall@1}$和$\mathrm{Recall@5}$，以$\beta_1=0.4$和$\beta_2=0.15$控制相应贡献；优化器为AdamW。所给节选只列出了式(1)至式(7)的超参数及用途，没有提供这些公式的完整表达式，因此无法忠实抄录中央方程，`equations`保持为空，避免根据公式编号反向臆造目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. FiGMaQ自动细粒度五元组构造模块**

该模块将相关图像对识别、细粒度图像描述、语义过滤和受约束的修改文本生成串联起来。与仅生成三元组的方法相比，它保留参考与目标两端的细粒度语义，可同时支持目标内容推理和查询—目标检索训练；最终数据规模为$87\mathrm{K}$。

> 直观理解：它不仅告诉模型“哪两张图有关”，还说明两张图各自包含什么以及用户会如何表达变化，从而用更少但更精细的数据训练复杂检索能力。

**2. 两阶段解耦微调模块**

第一阶段优化细粒度上下文推理，使模型从参考图像和修改文本恢复目标语义；第二阶段优化查询—目标对齐和排序。该设计不同于把推理与检索目标在单一阶段同时训练的纠缠式方案。

> 直观理解：这类似先学习读懂题目并形成答案，再练习从大量选项中选出答案；若两件事从一开始混在一起，模型可能只学到表面相似性。

**3. 召回导向的判别式检索模块**

在常规图文对比目标之外，第二阶段加入针对排名指标的召回代理损失，并联合$\mathcal{R}_s=[1,5]$两个截断位置进行训练。其作用是缩小复合查询与正确目标的距离，同时提高正确目标相对于困难负样本的排序优势。

> 直观理解：普通对比学习只要求正确配对总体更相似，而召回代理损失进一步关心它是否真的进入第一名或前五名，因此训练信号更贴近实际检索评价。

**训练与推理**

数据构造阶段先用BLIP-3-4B生成细粒度图像描述，并训练用于相关图像对识别的编码器；通过相似度阈值过滤候选对后，利用成对细描述生成关键但不泄露全部目标内容的修改文本，得到FiGMaQ。模型训练阶段冻结视觉编码器和投影层，只通过LoRA更新LLM：先进行一个训练周期的上下文推理微调，再从该模型继续进行两个训练周期的检索微调。技术上，两阶段使用相同骨干但承担不同学习职责，不是分别部署两个模型。
推理时保留第二阶段所得的唯一检查点。对于组合图像检索，输入是参考图像与修改文本；对于长文本、视觉对话或短文本检索，输入相应文本上下文；候选图库图像被编码为可比较表示，系统依据查询—图像相似度排序。作者在所有评测任务上复用同一检查点并采用零样本设置，即不在各测试数据集上继续微调。

**复现信息**

骨干为BLIP-3-4B，共约$4\mathrm{B}$参数，视觉编码器采用与对比基线一致的ViT-L/14。所有数据生成与模型微调阶段均冻结视觉编码器和投影层，仅对LLM施加LoRA：秩为$64$、`lora_alpha`为$128$、`lora_dropout`为$0.1$。相关图像对识别模型使用批大小$16$、学习率$1\mathrm{e}{-4}$训练两个周期；第一阶段以学习率$1\mathrm{e}{-4}$训练一个周期，第二阶段使用批大小$16$、学习率$1\mathrm{e}{-4}$训练两个周期。
数据生成中EOS标记数设为$M=5$，图文对比温度$\tau=0.01$，过滤阈值为$\theta_l=0.6$和$\theta_h=0.83$；检索微调使用$\tau'=0.01$以及召回代理温度$\tau_1=1$、$\tau_2=0.01$。训练采用AdamW和DeepSpeed ZeRO-2，在$4$张NVIDIA A100-40G GPU上完成。这些设置说明FiRE的比较建立在较轻量的$4\mathrm{B}$骨干和参数高效微调之上，但节选未给出随机种子、完整提示模板及全部损失公式，严格复现仍需核对论文正文或代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 组合图像检索：CIRR与CIRCO是开放域数据集，FashionIQ是时尚领域数据集，并含Dresses、Shirts和Tops&Tees三个子集。它们共同测试模型能否结合参考图像与修改文本找到目标图像；所给章节未报告数据规模、评测划分及候选库大小。
- 复杂文本交互检索：Urban1K包含1000张细微差异明显的城市景观图像，每张图像配有细粒度长描述，用于长文本到图像检索；Visual Dialog用于对话式图像检索，考察模型利用多轮语言上下文定位图像的能力。所给章节未说明Visual Dialog采用的具体划分与候选设置。
- 短文本到图像检索：COCO与Flickr30K作为经典数据集，用于检查FiRE在较简单、标准的图文检索任务上是否仍具通用性。所给章节未报告具体测试划分、图像数量、文本数量及是否采用统一候选库。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$R@k$**

Recall at $k$，表示正确目标是否出现在排序前$k$个结果中；文中用于CIRR。不同$k$反映用户查看较少或较多候选时的命中能力。 （越高越好，因为数值越高表示更多查询能在前$k$个候选中找到正确目标。）

</div>
<div class="metric-item" markdown="1">

**$R_{\mathrm{subset}}@k$**

在CIRR特定子集候选范围内计算的Recall at $k$，用于衡量模型在语义相近、区分更困难的局部候选集合中的排序能力。 （越高越好，因为它表示在更具迷惑性的候选子集中，正确目标进入前$k$名的比例更高。）

</div>
<div class="metric-item" markdown="1">

**$\mathrm{mAP}@k$**

截断到前$k$项的平均精度均值，文中用于CIRCO。它不仅检查相关图像是否被找回，还考虑多个相关目标在前$k$名中的排序位置。 （越高越好，因为相关目标越多且排序越靠前，平均精度通常越高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- FiRE在零样本设置下，能否跨越组合图像检索、长文本到图像检索、视觉对话检索和短文本到图像检索等不同任务，稳定提升复杂查询与目标图像的匹配能力？
- 自动构造的细粒度多模态数据，以及将“上下文推理”和“检索对齐”解耦的两阶段微调，是否分别构成性能提升的关键来源？

**实验实现**

作者将评测覆盖四类任务：组合图像检索、长文本到图像检索、对话式图像检索和短文本到图像检索，并在摘要中将总体协议称为零样本检索。所给实验节选只明确了数据集选择，以及CIRR采用$R@k$和$R_{\mathrm{subset}}@k$、CIRCO采用$\mathrm{mAP}@k$；没有提供模型检查点、图像分辨率、候选向量计算方式、相似度函数、批大小、硬件、随机种子或完整测试协议，因此无法据此复现实验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces multimodal data construction and staged fine-tuning methods to improve MLLM-based complex image retrieval.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`f4507013400f243b0bb14008a01def44d02907860ab5715cc9a2e11b1143f0fb`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
