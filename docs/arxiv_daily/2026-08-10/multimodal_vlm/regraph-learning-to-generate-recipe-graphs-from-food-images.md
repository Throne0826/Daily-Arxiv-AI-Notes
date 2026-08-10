---
title: "[论文解读] ReGraph: Learning to Generate Recipe Graphs from Food Images"
description: "[arXiv 2608.06917][多模态 VLM] 本文针对从单张食物图像生成可验证烹饪流程的问题，指出文本流畅性不能代表程序结构正确性，并以显式食谱图和两阶段训练框架提升模型对实体、状态变化及步骤关系的建模能力。"
arxiv_id: "2608.06917"
announcement_date: "2026-08-10"
primary_category: "multimodal_vlm"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-10T02:43:17.863638+00:00"
source_sha256: "c094a514e779fc24ffb3a0c3b54ccc8e648dd0e40488e71be85e105a63701550"
tags:
  - "多模态 VLM"
  - "LLM Reasoning"
  - "食物图像到食谱生成"
  - "大语言多模态模型"
  - "食谱图"
  - "结构化生成"
  - "食材状态转化"
  - "程序关系"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">多模态 VLM · arXiv 2608.06917</p>

# ReGraph: Learning to Generate Recipe Graphs from Food Images

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Guoshan Liu, Bin Zhu, Pengkun Jiao, Jingjing Chen, Chong-Wah Ngo, Yu-Gang Jiang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Institute of Trustworthy Embodied AI, Fudan University Shanghai China；Institute of Trustworthy Embodied AI, Fudan University；Shanghai Key Laboratory of Multimodal Embodied AI Shanghai China；Shanghai Key Laboratory of Multimodal Embodied AI；Singapore Management University Singapore Singapore；Singapore Management University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.06917v1) · [PDF 下载](https://arxiv.org/pdf/2608.06917v1) · **关键词** 食物图像到食谱生成, 大语言多模态模型, 食谱图, 结构化生成, 食材状态转化, 程序关系<br>


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

本文针对从单张食物图像生成可验证烹饪流程的问题，指出文本流畅性不能代表程序结构正确性，并以显式食谱图和两阶段训练框架提升模型对实体、状态变化及步骤关系的建模能力。

**不用术语来说**：现有模型能够根据成品图像写出看似合理的食谱，但文字通常没有明确说明每种食材如何变化、每个动作具体作用于什么对象，以及哪些步骤必须先后执行。因此，模型可能只是生成符合常识的描述，却没有真正表达完整的烹饪过程。本文要解决的是：如何把图像中难以直接观察的烹饪流程组织成结构化表示，并据此检验和提升模型的过程推理能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 ReGraph 食谱图数据集，将食材、动作和工具表示为实体，用实体属性记录食材状态变化，并用类型关系 `$targ$`、`$dest$` 和 `$followed\ by$` 表示操作对象、动作目的地或产物以及步骤顺序；同时提供 Recipe Reasoning Chain-of-Thought（RR-CoT）作为程序分解的辅助监督。
- 提出 Recipe Graph Learning（RGL）两阶段框架：先通过监督微调联合生成 RR-CoT 和食谱图，再通过图级强化微调优化实体与关系生成，从而直接提升模型恢复细粒度烹饪结构的能力。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于食品计算、视觉语言学习与结构化生成的交叉领域。任务是根据食物图像推断其可能对应的烹饪流程：输入只有最终或中间食物外观，模型需要利用视觉信息和已学习的烹饪知识，生成不仅语言流畅，而且能够显式表达食材、动作、工具、食材状态变化及动作顺序的结构化食谱图。与传统食谱生成主要依靠文本相似度不同，本文关注模型是否恢复了可分析、可比较的过程级知识。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大语言多模态模型（LMM）**

LMM同时处理图像和文本，并利用语言模型生成文本或结构化结果。在本文中，LMM接收食物图像，推断不可直接观察的食材、烹饪动作及其先后关系。

</div>
<div class="concept-item" markdown="1">

**食谱图**

食谱图是一种将烹饪流程表示为节点和有类型边的图结构。节点包括食材、动作和工具，节点属性记录食材状态，边则表示动作作用于什么对象、动作产生或传递到什么对象，以及动作之间的先后顺序。

</div>
<div class="concept-item" markdown="1">

**结构化生成**

结构化生成要求模型输出符合预先定义模式的机器可读对象，而不是任意自由文本。模型必须同时满足内容正确、实体和关系相互一致、输出格式可解析等要求，因此比生成通顺句子更严格。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一张食物图像，模型需要生成一个细粒度食谱图，输出包括食材实体、烹饪动作实体、工具实体、食材状态或中间产物属性，以及三类过程关系：$targ$、$dest$和$followedy$。其中，$targ$表示某个食材或其他被直接操作的实体是动作的作用对象，$dest$表示动作对应的目的地或输出实体，$followedy$表示动作之间的时间或程序顺序。任务的核心假设是：最终图像通常不能直接显示完整烹饪流程，因此模型必须根据视觉线索和一般烹饪知识恢复潜在的状态转化与程序依赖；生成结果随后按照预定义模式与参考食谱图进行确定性、模式感知的匹配。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$I$**

输入的食物图像。

</div>
<div class="notation-item" markdown="1">

**$G$**

目标或生成的食谱图，由实体、实体属性和有类型关系组成。

</div>
<div class="notation-item" markdown="1">

**$V$**

食谱图中的实体集合，包括食材、烹饪动作和工具。

</div>
<div class="notation-item" markdown="1">

**$E$**

食谱图中的关系集合，包括$targ$、$dest$和$followed\ by$等有类型边。

</div>

</div>

**直接相关的工作**

- **FoodLMM**: FoodLMM通过多模态指令调优增强细粒度食物识别与食谱理解，代表了从食物图像生成详细食谱的LMM路线。但其主要输出仍是自由形式文本，未显式编码动作与食材的作用关系、状态演化和程序顺序。
- **FoodKG**: FoodKG是大规模食品领域知识图谱，主要描述食材属性、营养信息和跨食谱关联，规模超过一百万份食谱和六千七百万条三元组。它缺少完整的烹饪工作流、显式食材状态转化和动作依赖，因此不能直接作为本文所需的细粒度视觉食谱图生成与评测资源。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

从食物图像推断食谱具有实际价值，但成品图像通常只显示最终外观，无法直接呈现清洗、腌制、溶解等准备操作。因而，模型不仅要生成语言上合理的食谱，还要推断食材状态如何沿动作序列演化，并明确动作、对象、工具和中间产物之间的依赖关系。这个问题本质上是从不完整视觉证据中生成一个合理且能够与参考流程对齐的烹饪工作流，而不是唯一地复原真实发生过的过程。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于自由文本的食谱生成**：模型直接根据食物图像生成步骤化或段落式食谱，通常使用 SacreBLEU、ROUGE-L 等文本指标，将生成文本与参考食谱进行词汇或序列层面的比较。这类方法擅长衡量文字是否流畅、是否包含相似表述，但没有把食材状态、操作对象和步骤依赖作为独立结构进行预测。
- **既有食物知识图或流程图资源**：已有资源以节点和边表示食材、营养信息、配方关联或部分烹饪流程，例如静态食物知识图、视觉标注图和烹饪程序数据。它们为结构化表示提供了基础，但部分数据规模较小，部分只记录静态关联或局部流程，且许多资源没有细粒度表示中间状态，也缺少面向多模态模型的程序推理监督。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 文本指标只能反映表述层面的相似性，不能可靠判断模型是否恢复了过程结构。生成文本即使流畅且与参考文本词汇相近，也可能没有明确指出某个动作操作哪种食材、食材在动作后变成什么状态，或哪些动作必须按顺序执行；其后果是模型的程序知识无法被直接分析、比较和验证。
- 既有食物图资源在规模、流程完整性和状态表达方面不足：有的主要描述静态食材或跨食谱关系，有的只包含部分烹饪流程，有的将中间状态隐含在文本中，且通常没有显式的程序分解监督。因此，它们难以同时支持大规模训练和对图像到细粒度食谱流程的系统评估。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种能够把烹饪视为连续状态变换过程的统一基准：该基准需要同时显式表示食材、动作、工具、中间产物、食材状态和步骤依赖，并为模型提供程序分解监督；同时还需要一种不依赖模型主观判断、能够按实体和类型关系确定性比较生成图与参考图的评估协议。缺少这一表示和评估层，文本生成分数与模型实际掌握的程序结构之间的差距就难以量化，针对结构生成的训练改进也缺乏明确目标。

</div>
<div markdown="1"><span>核心问题</span>

给定一张成品食物图像，如何训练多模态大模型生成一个与参考流程对齐、可解析且包含细粒度实体、食材状态变化和程序关系的食谱图，并以结构级指标判断模型是否真正恢复了烹饪过程知识？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把原本混在自然语言中的流程信息拆成模型可以逐项学习和检查的结构。先让模型生成 RR-CoT，相当于要求它在输出图之前整理动作及其顺序；再生成食谱图，把食材状态变化和动作关系固定到预定义模式中；最后使用相对改进奖励和格式奖励，分别推动结构预测质量提升并减少不可解析输出。直观地说，这种设计把“写出像食谱的话”转化为“列出谁在何时对什么做了什么，以及对象随后变成什么”，因此更适合学习和评估过程级知识。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ReGraph 的 Recipe Graph Learning（RGL）以食物图像 $x$ 和固定文本查询 $q$ 为输入，采用两阶段训练生成结构化菜谱图。第一阶段 RGL-SFT 使用带有 Recipe Reasoning Chain-of-Thought（RR-CoT）的标注进行监督微调，使模型先分解可能的烹饪流程，再输出实体与关系图；第二阶段 RGL-RFT 使用 Group Relative Policy Optimization（GRPO）按照图结构质量和格式合规性进行强化微调。推理时模型仍生成 RR-CoT 与菜谱图，但评估只解析并评分图部分，RR-CoT 仅在训练中作为辅助监督。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多模态输入与任务指令

模型接收图像和文本指令，利用视觉信息推断成品背后的可能烹饪过程。由于静态图像通常不直接显示中间状态和动作，模型需要结合烹饪常识补全隐含流程。

<div class="method-step__io" markdown="1">

**输入**：食物图像 $x$ 与固定文本查询 $q$。查询要求模型推断一个合理的烹饪流程，提取 ingredient、tool、action 三类实体，预测 $targ$、$dest$ 和 $followed\ by$ 三类有向关系，并按预定义模式输出菜谱图。<br>
**输出**：供自回归生成使用的多模态条件 $(x,q)$。

</div>

**直观理解**：输入只有菜品的最终视觉结果和任务说明，类似于根据一张成品照片倒推食材如何被处理、使用了什么工具以及各步骤的先后关系。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### RGL-SFT：程序分解与图生成

使用监督微调让模型先组织合理的步骤序列、依赖关系、食材状态变化和中间产物，再生成实体及其类型、属性和有类型关系。训练对 RR-CoT 与图的完整目标序列计算自回归负对数似然，使图输出与前面的流程分解保持一致。

<div class="method-step__io" markdown="1">

**输入**：训练样本 $(x,q,o)$，其中目标序列 $o=[o_{\mathrm{reason}},o_{\mathrm{graph}}]$ 包含 RR-CoT 推理轨迹和对应的参考菜谱图。<br>
**输出**：初始化策略 $pi_\theta$，能够按照指定模式生成 RR-CoT 和结构化菜谱图。

</div>

**直观理解**：模型不是直接从照片跳到答案，而是先写出一份步骤草稿，再把草稿整理成可计算的图。这份草稿不在测试分数中单独评价，但帮助模型学习如何安排隐含的烹饪过程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### RGL-RFT：图级强化优化

对每个候选图计算实体和关系的严格匹配 F1，并以相对于 SFT 基线的 RIR 作为语义结构奖励；同时用二值 FR 检查 RR-CoT、实体段、关系段、字段完整性和模式顺序。GRPO 在候选组内标准化奖励得到相对优势，采用裁剪策略比率并加入相对于参考策略 $pi_{\mathrm{ref}}$ 的 KL 正则，以更新模型。

<div class="method-step__io" markdown="1">

**输入**：经过 SFT 初始化的策略、训练图像和查询，以及同一输入下由旧策略 $pi_{\theta_{\mathrm{old}}}$ 采样的 $G$ 个候选输出。<br>
**输出**：RGL-RFT 策略，倾向于生成实体更完整、关系更准确且可解析的菜谱图。

</div>

**直观理解**：同一张图让模型提出多个答案，再比较哪一个更接近参考图、格式也更正确，并提高相对较好的答案概率。KL 约束防止强化训练破坏 SFT 阶段已经获得的基本生成能力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 推理、解析与图评估

解析输出中的实体段和关系段，排除 RR-CoT，不使用测试集信息构建词表。对食材名称、状态属性、动作和工具进行规范化，再依据类型、名称、状态和端点匹配规则计算实体与关系的 Precision、Recall 和 F1；未匹配项可在补充实验中接受受限的语义等价判断。

<div class="method-step__io" markdown="1">

**输入**：测试食物图像 $x$ 与固定查询 $q$，以及模型生成的 RR-CoT 和图文本。<br>
**输出**：可评分的预测图及实体、关系层面的宏平均指标。

</div>

**直观理解**：评估器先把不同写法统一成标准标签，再检查模型是否找对了节点及节点之间的边。主评估强调可复现的精确匹配，补充语义评估只处理规范化仍无法解决的局部表达差异。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### RGL-SFT 监督微调目标

$$
\mathcal{L}_{\mathrm{SFT}}(\theta)=-\mathbb{E}_{(x,q,o)\sim\mathcal{D}}\left[\frac{1}{|o|}\sum_{t=1}^{|o|}\log\pi_{\theta}(o_{t}\mid x,q,o_{<t})\right]
$$

**符号说明**

- $\mathcal{L}_{\mathrm{SFT}}(\theta)$：参数为 $\theta$ 的监督微调损失，越小表示模型越接近参考输出。
- $\mathcal{D}$：ReGraph 训练集，样本包含图像、查询和目标序列。
- $x$：输入食物图像。
- $q$：固定文本任务查询。
- $o$：由 RR-CoT 和最终菜谱图组成的目标序列。
- $o_t$：目标序列在位置 $t$ 的 token。
- $o_{<t}$：位置 $t$ 之前已经生成的 token。
- $\pi_{\theta}$：当前多模态自回归策略生成 token 的条件概率。
- $|o|$：目标序列长度，用于对 token 损失做平均。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标要求模型在给定图像、查询和已生成前缀时，提高正确下一个 token 的概率。因为 $o$ 同时包含 RR-CoT 和图，所以模型会同时学习流程分解与结构化输出。<br>
**原文位置**：第 4.1 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### GRPO 强化微调目标

$$
\mathcal{J}_{\mathrm{GRPO}}(\theta)=\mathbb{E}_{(x,q)\sim\mathcal{D},\,\{o_i\}\sim\pi_{\theta_{\mathrm{old}}}}\left[\frac{1}{G}\sum_{i=1}^{G}\min\left(\rho_i\hat{A}_i,\,\mathrm{clip}(\rho_i,1-\epsilon,1+\epsilon)\hat{A}_i\right)-\beta D_{\mathrm{KL}}(\pi_{\theta}\|\pi_{\mathrm{ref}})\right],\quad \rho_i=\frac{\pi_{\theta}(o_i\mid x,q)}{\pi_{\theta_{\mathrm{old}}}(o_i\mid x,q)},\quad \hat{A}_i=\frac{R_i-\mathrm{mean}(\{R_1,\ldots,R_G\})}{\mathrm{std}(\{R_1,\ldots,R_G\})}
$$

**符号说明**

- $\mathcal{J}_{\mathrm{GRPO}}(\theta)$：GRPO 要最大化的策略目标。
- $G$：同一输入下采样的候选输出数量。
- $o_i$：第 $i$ 个候选 RR-CoT 与菜谱图输出。
- $R_i$：候选输出的总奖励，由 RIR 和 FR 加权得到。
- $\hat{A}_i$：候选在同组中的标准化相对优势，表示其奖励高于或低于组内平均水平的程度。
- $\rho_i$：候选输出在当前策略与旧策略下的概率比。
- $\epsilon$：策略比率的裁剪阈值，限制单次更新幅度。
- $\beta$：KL 正则项权重，控制当前策略偏离参考策略的程度。
- $D_{\mathrm{KL}}(\pi_{\theta}\|\pi_{\mathrm{ref}})$：当前策略与参考策略之间的 KL 散度。

<div class="equation-explanation" markdown="1">

**直观理解**：GRPO 不要求额外训练价值网络，而是比较同一输入产生的多个候选答案。奖励更高的候选提高生成概率，但裁剪和 KL 正则共同限制更新过猛或偏离原有能力过远的情况。<br>
**原文位置**：第 4.2 节，公式（2）和公式（3）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标分为两层。RGL-SFT 最小化覆盖 RR-CoT 与图序列的平均 token 级负对数似然，使模型学习预定义模式、程序分解和图生成；RGL-RFT 最大化 GRPO 目标，使模型在同一输入的候选组中偏向实体 F1、关系 F1 和格式奖励更高的输出。RIR 对实体和关系分别计算严格匹配 F1，并以 SFT 的任务级基线为参照：超过基线的候选获得归一化正奖励，低于基线的候选获得经 $lambda=0.5$ 软化的负奖励；FR 只检查结构存在性、顺序和字段完整性，不判断 RR-CoT 的语义质量。需要区分的是，RIR 不直接评分食材状态属性，状态改进主要通过实体识别和最终状态感知评估间接体现。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. ReGraph 结构化监督与 RR-CoT**

ReGraph 将 ingredient、action 和 tool 作为实体，并用食材属性表示烹饪状态变化；$targ$ 表示动作作用的目标，$dest$ 表示动作结果或对象的目的地，$followed\ by$ 表示程序顺序。每个样本同时提供参考图和 RR-CoT，后者描述步骤组织、依赖、状态变化、中间产物及动作与食材的交互。

> 直观理解：普通菜谱文字容易把“谁被怎样处理、处理后变成什么、下一步接什么”混在句子里；图把这些信息拆成节点和边，而 RR-CoT 提供从步骤到图的中间整理过程。

**2. RGL-SFT 自回归监督微调**

模型对目标序列 $o=[o_{\mathrm{reason}},o_{\mathrm{graph}}]$ 逐 token 建模，先生成 RR-CoT，再生成图。监督信号同时覆盖程序分解和模式化图输出，弥补仅监督最终图时中间程序组织指导不足的问题。

> 直观理解：这一阶段负责教会模型“应该如何思考和按什么格式表达”，重点是获得从图像到流程图的基本能力，而不是直接针对单个图的最终 F1 做优化。

**3. RGL-RFT 的 RIR、FR 与 GRPO**

RIR 分别对实体和关系计算严格 exact-match F1，并相对于收敛 SFT 模型在训练集上的任务基线 $b_{\mathrm{entity}}$ 和 $b_{\mathrm{relation}}$ 计算相对改进奖励；低于基线时使用 $lambda=0.5$ 的软化惩罚，最终奖励裁剪到 $[-0.5,1.0]$。FR 对结构合法性给出全满足为 $1$、否则为 $0$ 的奖励；总奖励按实体、关系和格式三项加权，其中原文给出 $alpha=1$、$beta'=1$、$gamma=0.1$。

> 直观理解：RIR 关心图的内容是否正确，FR 关心输出能否被程序可靠读取。两者结合后，模型既不会只生成看似合理但结构错误的文字，也不会只追求格式而忽略实体和关系。

**训练与推理**

训练时，首先用 ReGraph 样本和固定查询构造目标 $o=[o_{\mathrm{reason}},o_{\mathrm{graph}}]$，通过 SFT 获得具备基本流程分解和图生成能力的策略。随后，旧策略对每个训练输入采样 $G$ 个候选，解析候选图并依据严格实体、关系匹配计算 RIR，再依据 Table 7 的结构约束计算 FR；将组内标准化优势代入带裁剪比率和 KL 正则的 GRPO 目标，迭代更新策略。推理时输入一张未见过的食物图像和同一固定查询，模型生成 RR-CoT 及结构化图；评估器仅解析实体和关系部分，RR-CoT 不计入指标。

**复现信息**

为保证评估可复现，所有训练词表和映射只由 8,500 个训练样本构建，并在测试前冻结。食材名称使用 Inverse Cooking 的词表和同义词映射；状态属性保留明确的烹饪操作及结果状态，区分如 $boiling$ 与 $boiled$，保留多状态原始顺序，并移除数量、单位、时间、温度等非状态修饰。训练集规范化后，12,626 个原始食材属性字符串归并为 246 个动作或状态标签，3,080 个原始动作表达归并为 277 个规范动作，4,171 个工具表达归并为 137 个规范工具；频次低于 10 的规范动作和工具标签被移除。RIR 采用实体类型与名称、关系类型及两端实体的严格匹配，食材端点还必须匹配状态；实体 ID 被忽略。补充语义匹配使用 Gemini 3.1 Pro 和 Qwen3-32B，仅对规范化后仍未匹配的候选对进行受限等价判断，且不能消除食材状态差异。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ReGraph：实验唯一明确使用的数据集。作者以其中 8,500 个样本训练 RGL-SFT 和 RGL-RFT，保留 1,500 个样本评测。其角色是为“食物图像→配方图”任务提供图像、RR-CoT 推理轨迹和人工核验的结构化图真值，并按确定性的规范化匹配协议评价输出。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**实体 Precision、Recall 与 F1**

衡量预测实体与参考图实体的规范化匹配程度。食材实体必须同时匹配规范名称及保留的动作/状态属性；动作和工具实体仅匹配规范名称。Precision 反映预测实体中有多少正确，Recall 反映真值实体被找回多少，F1 综合二者。 （越高越好，因为更高值表示模型既少产生不对应的节点，也少遗漏参考过程中的节点；但它不单独证明生成的烹饪流程在现实中可执行。）

</div>
<div class="metric-item" markdown="1">

**关系 Precision、Recall 与 F1**

衡量预测的类型化关系与参考图关系的一致性，用于检验食材/工具与动作之间的操作对象、目标位置及过程顺序等依赖是否被正确恢复。 （越高越好，因为配方图的程序语义主要由边表达；但严格参考匹配较低也可能部分来自图像无法观察到的配料或中间步骤，而不必然等价于菜谱完全错误。）

</div>
<div class="metric-item" markdown="1">

**格式奖励**

RGL-RFT 中的训练奖励项，用于约束输出保持图的预定结构格式，防止强化学习后结构化输出退化；它不是表 8 中的主报告质量指标。 （训练时越高越好，但作者刻意赋予较小权重，以避免模型为了格式合规而牺牲实体和关系的语义探索。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 现有方法生成的菜谱文本与 ReGraph 参考图之间的结构可恢复性对比。

<div class="result-value" markdown="1">

作者报告：既有方法虽然在文本生成质量上具有竞争力，但在 ReGraph 模式下可严格对齐的实体和关系结构有限。原文节选没有提供表 8 的具体数值行，因此无法据此比较各模型的精确 F1 差距。

</div>

该结果支持“流畅、看似合理的菜谱”不等于“明确表示了食材状态和步骤依赖”。不过，这是基于作者定义的规范化图匹配得到的结论，不能直接推出文本菜谱对人类读者毫无实用性。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under a deterministic, schema-aware matching protocol, our experiments reveal a substantial gap between text-generation quality and recoverable procedural structure: recipes produced by existing approaches achieve competitive text-generation scores yet yield limited reference-aligned entity and relation structure under the ReGraph schema.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### RGL 在 Qwen3-VL-8B 与 InternVL3-8B 两个代表性视觉语言模型骨干上的跨骨干比较。

<div class="result-value" markdown="1">

作者声称 RGL 在两个骨干上均持续改善烹饪实体与程序关系的生成；但当前节选未包含表 8 的完整结果行，原文未明确报告每个骨干、训练阶段和指标的具体数值。

</div>

两个不同骨干均有改进，说明收益不应完全归因于单一模型的偶然特性。由于没有给出置信区间、重复实验或完整表中差值，不能由此判断改进幅度是否在统计意义上稳定。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, across two representative LMM backbones, RGL consistently improves the generation of cooking entities and procedural relations, while our analysis further shows that fine-grained ingredient-state capture remains the most challenging dimension.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 细粒度食材状态的恢复难度分析。

<div class="result-value" markdown="1">

作者将细粒度食材状态捕获确定为最具挑战性的维度。当前节选未说明该分析使用的具体分组、指标值或错误类型比例，原文未明确报告。

</div>

这与任务本身相符：同一食材在“生的、煮熟的、冷却的、混合后”等阶段名称可能不变，但状态属性决定其能否作为后续动作的正确输入。该发现指出后续方法应重点建模中间状态，而不只识别食材名和动作词。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, across two representative LMM backbones, RGL consistently improves the generation of cooking entities and procedural relations, while our analysis further shows that fine-grained ingredient-state capture remains the most challenging dimension.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 提供的实验节选只给出表 8 标题与评测协议，未包含表中完整数值；因此具体模型排名、F1 值、shot 数影响和 RGL-SFT/RFT 的差值均无法从当前材料核验。
- 以单个参考配方图进行确定性规范化匹配能严格评估参考对齐，但对同一道菜存在多种合理做法、图像不可见的配料或步骤时，可能低估语义上可行但不同表述的输出。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- InternVL3-8B：不进行参数更新的开源视觉语言模型，用零样本及 1/2/3-shot 上下文学习评估原生程序图生成能力；同时也是 RGL 的一个基础骨干，因此可区分框架训练收益与骨干本身能力。
- Qwen3-VL-8B：与 InternVL3-8B 相同，既作为免训练的上下文学习基线，也作为 RGL-SFT/RFT 的基础骨干；用于检验方法是否跨两个同规模模型泛化。
- Qwen3-VL-32B：更大规模的开源免训练模型，在零样本及 1/2/3-shot 设置下测试；它检验“仅增大模型并给示例”能否替代面向图结构的训练。
- GPT-5.2 与 Gemini 3.1 Pro：专有通用模型，仅在零样本和 3-shot 下评估；它们代表不依赖 ReGraph 参数微调的强闭源模型参照，但原文节选未给出二者的具体分数。

**实验想回答的问题**

- 通用大模型即使能生成流畅菜谱文本，能否从食物图像中恢复与参考答案严格对齐的食材、动作、工具及其过程关系？
- 在两种视觉语言模型骨干上，分阶段的 Recipe Graph Learning（RGL）监督微调与强化微调是否能稳定提高配方图中的实体和关系生成能力，以及最难恢复的是哪类过程信息？

**实验实现**

评测采用确定性的 canonical matching protocol，并报告实体与关系的 Precision、Recall、F1（百分比）。开源模型使用 zero-shot、1-shot、2-shot、3-shot；每个示例包含食物图像、对应 RR-CoT 和目标配方图。专有模型仅测 zero-shot 与 3-shot。RGL 使用 Qwen3-VL-8B、InternVL3-8B 两个骨干；LoRA 秩为 128，最大序列长度为 8,192，SFT 训练 1 个 epoch。RFT 用 GRPO，对每个查询采样 $G=8$ 个候选，且实体、关系、格式奖励权重分别为 $\alpha=1$、$\beta^{\prime}=1$、$\gamma=0.1$；其中实体/关系参考基线取相应 SFT 模型的 Entity F1/Relation F1。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| RGL-SFT 与 RGL-RFT 的两阶段训练，以及 RFT 相对 SFT 的奖励基线设计。 | RGL-RFT 的实体和关系参考基线分别初始化为对应 RGL-SFT 的 Entity F1 和 Relation F1，使奖励显式度量相对监督模型的改进；原文节选未提供移除 RFT、移除某项奖励或改变权重后的定量消融表。 | 这一设计隔离的是“在已有结构格式能力的 SFT 模型上，强化学习是否继续优化语义图匹配”。它使奖励关注超过 SFT 的增益，但仅凭该设定描述不能证明每个奖励项各自带来多少提升。 | Section 5.1, Dataset and Baselines<br><span class="experiment-evidence">For RGL-RFT, the RIR reference baselines $b_{\mathrm{entity}}$ and $b_{\mathrm{relation}}$ are initialized using the Entity F1 and Relation F1 scores achieved by the corresponding RGL-SFT model.</span> |
| RGL-RFT 中格式奖励的低权重设置，$\gamma=0.1$。 | 作者将格式奖励设为较小权重，理由是 SFT 已建立较强的结构合规性；较大格式权重可能过度约束策略并降低语义探索能力。没有报告不同 $\gamma$ 取值的指标变化，原文未明确报告定量消融结果。 | 该分析考察格式约束与语义优化之间的权衡：格式奖励负责避免输出格式崩坏，而实体、关系奖励应主导优化。它是作者的机制解释，不是已由权重扫描实验直接验证的因果结论。 | Section 5.1, Implementation Settings<br><span class="experiment-evidence">A substantially larger format-reward weight could over-constrain the policy and reduce its capacity for semantic exploration.</span> |

**定性案例**

- 附录以“cheese stuffed shells”展示 ReGraph 标注流程：先由 Claude-Sonnet 4.5 生成步骤、依赖、RR-CoT 和初始图，再由 GPT-4o 做模式规范化并经人工复核为最终真值。例子把 shell pasta 区分为初始、boiled、cooled 等实体状态，并用如“煮→取出→冷却→填馅→烘烤”的依赖边表达过程。它说明数据标注的目标是显式记录中间状态与先后条件，而非仅从最终成品图判断菜谱是否合理；该附录是数据案例，未构成模型性能的定量证明。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces dataset supervision and a structured generation framework for multimodal models to infer recipe graphs from food images.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`c094a514e779fc24ffb3a0c3b54ccc8e648dd0e40488e71be85e105a63701550`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
