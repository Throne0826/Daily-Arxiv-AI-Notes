---
title: "[论文解读] MI-Distillation: Selecting from Model-Interpolated Instruct-Reasoning Data Spectrum for Chain-of-Thought Distillation"
description: "[arXiv 2608.29623][LLM Reasoning] 本文从梯度更新特征解释小模型为何难以直接吸收长思维链，并提出通过模型插值构造细粒度推理数据谱、再按信息量与学生可学习性筛选轨迹的 MI-Distillation。"
arxiv_id: "2608.29623"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:54:55.078574+00:00"
source_sha256: "d6f1732a10cb0dfe304c1199ed5066c81ff3413b63a8320f543546ac00ba3917"
tags:
  - "LLM Reasoning"
  - "链式思维蒸馏"
  - "长链式思维"
  - "大型推理模型"
  - "学生模型适配"
  - "梯度谱结构"
  - "监督微调"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.29623</p>

# MI-Distillation: Selecting from Model-Interpolated Instruct-Reasoning Data Spectrum for Chain-of-Thought Distillation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Yangsong Lan, Renkai Hu, HongKai Zheng, Bo Zhang, Renzhi Wang, Hongliang Dai, Piji Li</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: College of Artificial IntelligenceNanjing University of Aeronautics and Astronautics, Nanjing, China；Affiliation: The Key Laboratory of Brain-Machine Intelligence Technology, Ministry of Education, Nanjing, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29623v1) · [PDF 下载](https://arxiv.org/pdf/2608.29623v1) · **关键词** 链式思维蒸馏, 长链式思维, 大型推理模型, 学生模型适配, 梯度谱结构, 监督微调<br>


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

本文从梯度更新特征解释小模型为何难以直接吸收长思维链，并提出通过模型插值构造细粒度推理数据谱、再按信息量与学生可学习性筛选轨迹的 MI-Distillation。

**不用术语来说**：大型推理模型会写出很长、信息丰富的解题过程，但小模型不一定能有效模仿：过长的过程可能包含超出其能力的推理模式，使训练信号虽然丰富，却难以消化，甚至不如简短解法有效。因此，关键并非把教师的完整推理原样交给学生，而是为不同能力的学生找到难度和信息量都合适的推理过程。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者从梯度视角比较长、短思维链监督，发现长思维链通常引起幅度更大且方向更集中的参数更新，并据此将蒸馏困难归结为“推理信息量”与“学生分布匹配程度”之间的失衡。
- 作者提出 MI-Distillation，通过在指令型模型与推理型模型之间插值来生成连续的 Instruct-Reasoning 数据谱，并使用 SeqLSS 优先选择既提供有效新信息、又在学生模型能力范围内的推理轨迹。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型推理能力迁移与链式思维（Chain-of-Thought，CoT）蒸馏领域。大型推理模型（Large Reasoning Models，LRMs）能够通过逐步生成中间推理过程来解决复杂数学、知识推理和代码问题，但其推理过程通常较长、推理成本较高，因此实际部署常需要将能力迁移到参数规模更小的学生模型。CoT蒸馏通常把教师模型生成的“问题—推理依据—最终答案”序列作为监督信号，通过监督微调训练学生模型；本文关注的核心背景问题是：推理信息更多的长CoT是否必然比简短CoT更适合不同规模的学生模型。文章将这一问题与训练梯度联系起来，考察不同推理轨迹如何改变学生模型参数更新的强度与方向结构。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**链式思维蒸馏（CoT distillation）**

教师模型先为输入问题生成中间推理步骤和最终答案，学生模型再以这些完整序列为监督目标进行训练。与只学习最终答案相比，这种方法试图让学生模型学习解决问题的过程，而不仅是结果。

</div>
<div class="concept-item" markdown="1">

**长CoT与短CoT**

长CoT包含更多中间步骤，通常具有更高的推理信息量，但序列更长、训练信号也更复杂；短CoT则以较少步骤表达解题过程。本文不把长度简单视为质量，而是研究推理轨迹的信息密度是否与学生模型的能力和分布相匹配。

</div>
<div class="concept-item" markdown="1">

**梯度的谱结构**

训练梯度表示模型参数应如何改变；将梯度矩阵进行奇异值分解后，可以用核范数衡量更新信号的总体强度，用有效秩衡量信号分布在多少个有效方向上。直观地说，前者反映“更新有多大”，后者反映“更新是否集中在少数方向”。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定由教师模型产生的蒸馏数据集中的样本 $(x,y)$，其中 $x$ 是输入指令或问题，$y=(y_1,c6,y_T)$ 是由CoT推理依据和最终答案组成的目标序列。学生模型记为 $\mathcal{M}_{\theta}$，其参数为 $\theta$；训练目标是在监督微调中最大化学生模型按照自回归顺序生成目标序列的概率，等价于最小化归一化的逐词负对数似然。本文的设定假定教师模型能够提供有效的推理轨迹，而研究重点不是重新训练教师模型，而是判断哪些不同长度、正确性和推理深度的轨迹最适合学生模型学习。为分析这种匹配关系，文章进一步观察学生注意力模块中查询、键、值和输出投影矩阵的梯度变化，并比较Short CoT与Long CoT所诱导的更新强度及方向集中程度。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入指令或待解决的问题。

</div>
<div class="notation-item" markdown="1">

**$y=(y_1,\ldots,y_T)$**

目标输出序列，包括CoT推理依据和最终答案；$y_t$ 表示第 $t$ 个目标词元，$T$ 表示序列长度。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{M}_{\theta}$**

参数为 $\theta$ 的学生语言模型。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{G}_{X,i}$**

学生模型第 $i$ 层中注意力投影模块 $X$ 的梯度矩阵，其中 $X\in\{Q,K,V,O\}$ 分别表示查询、键、值和输出投影。

</div>

</div>

**直接相关的工作**

- **直接使用Long CoT进行蒸馏**: 本文将其视为主要问题来源：更长的推理轨迹虽然包含更多信息，但已有观察表明，小型学生模型可能无法有效吸收这些信息，甚至可能不如使用Short CoT训练。本文进一步从梯度强度和梯度方向集中性解释这种现象。
- **Long/Short CoT混合与课程式蒸馏**: 相关方法试图通过人工设定混合比例，或按照预定课程逐步调整训练难度，缓解学生模型与推理数据之间的不匹配。本文认为这类方法对监督信号的控制较粗，轨迹多样性也有限，因此转而研究更细粒度的推理数据谱及面向学生模型的轨迹选择。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长思维链使大型推理模型在复杂问题上表现突出，但这类模型推理成本高，不适合资源受限的部署场景。将其推理能力蒸馏到紧凑学生模型本应降低成本，然而直接用长轨迹进行监督微调往往收益有限，小模型有时反而更适合短思维链；这使高质量教师推理数据无法直接转化为可靠的小模型能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **长、短思维链混合蒸馏**：把大型推理模型生成的详细长轨迹与较简洁的短轨迹按预设比例混合，用两类监督共同训练学生，希望兼顾推理信息与学习难度。
- **课程式思维链蒸馏**：按照人工设计的课程顺序或难度日程组织训练数据，让学生逐步接触不同难度的推理轨迹，以减轻直接学习复杂长思维链带来的优化压力。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 混合比例和课程日程通常由人工设定，只能在“长”与“短”或若干离散难度之间进行粗粒度控制，无法针对不同容量的学生连续调节轨迹长度、推理深度与正确性。
- 既有方法产生或使用的轨迹多样性有限，也缺少学生感知的选择准则，因而不能保证被选数据同时具有足够的信息密度和良好的可学习性；结果可能是监督内容丰富，却与学生自身分布不匹配并造成不稳定或低效更新。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一套端到端机制：首先构造覆盖指令式简洁回答到深度推理回答的连续数据谱，而不是只在少量固定数据类型间混合；其次依据具体学生模型的分布，从该数据谱中识别信息充分但不过度超出其能力的轨迹。论文的梯度分析进一步表明，这一缺口具有模型规模依赖性，因此不能仅用统一的教师轨迹或固定课程解决。

</div>
<div markdown="1"><span>核心问题</span>

如何为容量不同的学生模型构造更细粒度、可控的推理轨迹，并从中选择既能带来有效推理信息、又与该学生内在能力和输出分布相匹配的监督数据？

</div>
<div markdown="1"><span>作者直觉</span>

指令型模型倾向于给出简洁、易模仿的回答，推理型模型倾向于生成更长、更深入的过程；在二者参数之间以系数 $\lambda$ 插值，相当于连续调节生成器的“指令—推理倾向”，从而得到不同长度、深度和难度的候选轨迹。随后让学生自身参与评分：轨迹若完全符合学生当前预期，新增信息可能不足；若令学生极度意外，又可能难以学习。SeqLSS 因而寻找两者之间的平衡点，使蒸馏数据既有教学价值，又不至于超出学生的吸收能力。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MI-Distillation 是一种面向小型学生模型的链式思维（Chain-of-Thought，CoT）蒸馏框架。它先将指令型教师与推理型教师进行参数插值，构造具有不同推理深度和表达紧凑度的连续教师谱；随后为每道题生成多条候选推理轨迹，先按最终答案正确性过滤，再用学生模型条件化的 SeqLSS 对候选进行排序，选择同时具有信息量和可学习性的轨迹，最后以标准监督微调目标训练学生模型。

技术上，方法试图解决推理信息密度与学生分布对齐之间的冲突：过短的 CoT 可能提供不足的推理监督，过长的 CoT 虽然梯度信号更强，却可能超出小模型的学习能力。直观地说，MI-Distillation 不让学生只能在“极短”或“极长”两种教材中二选一，而是先制作一套难度连续变化的教材，再根据学生实际能学会什么进行选材。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造插值教师谱

对两类教师的参数进行线性插值，得到一组中间教师 $M_{\lambda}$，其参数为 $\Theta^{\mathrm{MI}}_{\lambda}$。改变 $\lambda$ 会连续调节推理深度、回答紧凑度和指令行为。

<div class="method-step__io" markdown="1">

**输入**：一个推理导向教师 $\Theta^{\mathrm{Thi}}$、一个指令导向教师 $\Theta^{\mathrm{Ins}}$，以及插值系数集合 $\Lambda=\{0.2,0.4,0.6,0.8,1.0\}$。<br>
**输出**：插值教师集合 $\{M_{\lambda}\}_{\lambda\in\Lambda}$。

</div>

**直观理解**：这相当于把“擅长简洁回答”的教师和“擅长深入推理”的教师按不同比例混合，制作出从短推理到长推理的一系列教材。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成候选推理轨迹

对每个问题 $q_i$，让每个 $M_{\lambda}$ 生成一条推理轨迹 $\mathbf{R}_{i,\lambda}\sim M_{\lambda}(\cdot\mid q_i)$，并将问题、答案、插值系数和轨迹汇总为候选集合 $\mathcal{D}$。

<div class="method-step__io" markdown="1">

**输入**：带有问题和标准答案的训练集 $\mathcal{S}=\{(q_i,a_i)\}_{i=1}^{N}$，以及每个插值教师 $M_{\lambda}$。<br>
**输出**：包含多个推理风格候选的 Instruct-Reasoning 数据谱 $\mathcal{D}$。

</div>

**直观理解**：同一道题由不同风格的教师分别作答，因此学生面对的不是一份固定答案，而是一组长短和难度不同的候选解题过程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 正确性过滤与 SeqLSS 选择

首先保留最终预测与 $a_i$ 一致的轨迹；然后计算每个候选轨迹的 SeqLSS，选择每道题中得分最高的正确轨迹。SeqLSS 用学生对轨迹 token 的惊讶度衡量信息量，并用学生对该 token 的概率排序位置衡量可学习性。

<div class="method-step__io" markdown="1">

**输入**：候选轨迹集合 $\mathcal{D}$、每条轨迹对应的标准答案 $a_i$，以及待训练学生模型 $\theta_s$。<br>
**输出**：最终蒸馏集合 $\mathcal{D}_{\mathrm{select}}=\{(q_i,R_i)\}$。

</div>

**直观理解**：先把答案错误的解题过程剔除，再从正确答案中挑选“有新东西但学生又不至于完全看不懂”的那一条。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 监督微调与下游评估

以问题 $q_i$ 为条件，让学生通过标准下一 token 预测学习完整选定轨迹 $R_i$，包括推理过程和最终答案；训练完成后，在下游推理基准上评估学生模型。

<div class="method-step__io" markdown="1">

**输入**：最终数据集 $\mathcal{D}_{\mathrm{select}}$ 和学生模型参数 $\theta_S$。<br>
**输出**：经过 CoT 蒸馏的学生模型及其基准测试结果。

</div>

**直观理解**：学生模仿筛选后的完整解题示范，而不是只学习最终答案，因此训练目标同时覆盖推理步骤和答案生成。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 模型插值

$$
\Theta^{\mathrm{MI}}_{\lambda}=\lambda\,\Theta^{\mathrm{Ins}}+(1-\lambda)\,\Theta^{\mathrm{Thi}},\quad\lambda\in[0,1]
$$

**符号说明**

- $\Theta^{\mathrm{MI}}_{\lambda}$：插值系数为 $\lambda$ 时的中间教师参数。
- $\Theta^{\mathrm{Ins}}$：指令导向教师的参数，通常对应更紧凑、更易遵循指令的回答行为。
- $\Theta^{\mathrm{Thi}}$：推理导向教师的参数，通常对应更深入或更长的推理行为。
- $\lambda$：插值系数；$\lambda$ 越接近 $1$，插值结果越偏向指令型教师，越接近 $0$ 则越偏向推理型教师。

<div class="equation-explanation" markdown="1">

**直观理解**：该式在参数空间中连接两个教师端点，生成中间教师。它的意义不是简单拼接两段文本，而是改变生成模型本身，使生成的 CoT 风格随 $\lambda$ 平滑变化。<br>
**原文位置**：第 4.1 节，式（3）

</div>

</div>

<div class="equation-block" markdown="1">

#### SeqLSS 序列选择分数

$$
\mathrm{SeqLSS}(\mathbf{R})=\frac{\sum_{i=1}^{T}S_i\,(1-U_i)^{\alpha}}{\sum_{i=1}^{T}S_i}
$$

**符号说明**

- $\mathbf{R}=(r_1,\ldots,r_T)$：由 $T$ 个 token 组成的候选推理轨迹。
- $S_i=-\log p_{\theta_s}(r_i\mid x,r_{<i})$：学生模型对第 $i$ 个 token 的 surprisal（惊讶度）；概率越低，$S_i$ 越大，表示该 token 对学生而言包含更多新信息。
- $U_i$：学生分配给所有概率高于目标 token $r_i$ 的词表 token 的累计概率质量；$U_i$ 越小，说明目标 token 越接近学生的高概率区域。
- $\alpha\geq0$：可学习性惩罚的强度，控制 $(1-U_i)^\alpha$ 对偏离学生分布 token 的降权程度。
- $x$：输入问题及其上下文。
- $\theta_s$：学生模型参数。

<div class="equation-explanation" markdown="1">

**直观理解**：分子把每个 token 的信息量 $S_i$ 与可学习性因子 $(1-U_i)^\alpha$ 相乘，分母用总惊讶度归一化。因此该分数近似表示：整条推理中，有多少重要信息落在学生能够学习的概率区域内；每道题选择分数最高的正确轨迹。<br>
**原文位置**：第 5.2 节，式（7）—（10）；序列级定义为式（10）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：选定数据后，学生使用标准下一 token 预测进行监督微调：最大化学生在问题 $q_i$ 条件下生成轨迹 $R_i$ 的对数概率，即最小化负对数似然。该优化使学生逐 token 模仿筛选后的推理过程；不过，所给章节未要求将该目标作为单独的中心公式展开，原文对应目标见第 5.2 节式（11）。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 模型插值的 Instruct-Reasoning 谱**

方法将指令型参数 $\Theta^{\mathrm{Ins}}$ 与推理型参数 $\Theta^{\mathrm{Thi}}$ 线性组合，形成 $\Theta^{\mathrm{MI}}_{\lambda}$。论文将该过程解释为对指令任务向量和推理任务向量进行任务算术；不同 $\lambda$ 产生不同的推理长度、深度和紧凑度。

> 直观理解：离散地混合 Short CoT 和 Long CoT 只能提供少数几种风格，而参数插值提供了更细的中间档位，使后续选择有更丰富的候选。

**2. 正确性过滤**

对每个候选 $\mathbf{R}_{i,\lambda}$ 检查其最终预测是否匹配标准答案 $a_i$，仅将答案正确的轨迹交给后续 SeqLSS 排序。

> 直观理解：这一模块防止学生把错误的推理模式当成监督信号；SeqLSS 只负责在正确候选中选择，而不是纠正错误答案。

**3. SeqLSS 学生感知选择**

对轨迹 $R=(r_1,\ldots,r_T)$，先计算 token 惊讶度 $S_i$ 和高于目标 token 的累计概率质量 $U_i$，再以惊讶度加权聚合可学习性修正后的 token 分数。最终每道题选择 SeqLSS 最高的正确轨迹；其中 $\alpha\geq0$ 控制可学习性惩罚强度。

> 直观理解：高惊讶度通常意味着内容新颖，但也可能意味着学生几乎不会预测；SeqLSS 试图保留有信息的部分，同时降低明显偏离学生概率分布的部分。

**训练与推理**

训练阶段，先固定或准备指令型与推理型教师，按照 $\Lambda=\{0.2,0.4,0.6,0.8,1.0\}$ 构造插值教师；每个教师对训练问题生成候选 CoT，按最终答案正确性过滤，再使用学生模型计算候选轨迹的 token 概率、$S_i$、$U_i$ 和 SeqLSS，并为每道题保留最高分正确轨迹。随后用 $\mathcal{D}_{\mathrm{select}}$ 对学生进行监督微调。

推理阶段，论文所给方法章节未规定额外的 MI-Distillation 推理算法；蒸馏完成后，学生作为普通语言模型在下游推理基准上生成答案并接受评估。训练时的候选排序依赖学生分布，因此不同学生模型或模型容量原则上可以选择不同的最优轨迹。

**复现信息**

论文明确给出的关键复现实例是使用五个插值系数 $0.2$、$0.4$、$0.6$、$0.8$ 和 $1.0$ 生成教师谱；候选轨迹均需经过相同的答案正确性过滤，之后才进行 SeqLSS 排序。SeqLSS 的惩罚强度由 $\alpha$ 控制，但所给章节未明确报告其具体取值、候选生成解码参数、每题保留轨迹数量或学生模型在训练期间是否周期性更新。

为公平解释该方法，需区分两类作用：模型插值扩大了可选监督的范围，SeqLSS 则利用具体学生的预测分布完成选择。论文还报告了与 SeqLSS-min 的对照，其中候选池和正确性过滤保持一致，仅改变排序方向；这用于检验提升是否来自 SeqLSS 的“信息量—可学习性”联合标准，而非来自候选数据本身。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 训练数据为MATH训练集中的7,500道随机抽样题目；每道题由Short-CoT教师、Long-CoT教师及插值教师生成候选推理轨迹，经答案正确性过滤后用于蒸馏。其作用是提供统一的问题集合，并构造可比较的Instruct–Reasoning数据谱。
- 主要数学评测覆盖GSM8K、MATH-500和AMC23：GSM8K测试多步小学数学文字题推理，MATH-500是涵盖竞赛数学不同主题与难度的500题子集，AMC23测试较高难度的高中数学解题能力。三者共同检验从基础多步计算到竞赛数学推理的迁移效果。
- 扩展评测包括AIME24、GPQA-Diamond、Minerva和OlympiadBench，分别覆盖高难度竞赛数学、研究生水平生物/物理/化学选择题、数学与STEM定量推理及奥林匹克数学。原文未明确报告这些数据集在实验中的具体样本规模或划分细节。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass@1 accuracy**

对每道题独立生成答案时，至少一次采样得到正确答案的比例；本文按规定的独立运行次数计算平均准确率，并同时报告标准差。 （越高越好，因为它直接表示学生模型解决评测题的成功率；标准差越小通常表示多次采样结果更稳定，但它不是主要性能指标。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 两种3B学生模型上的总体比较

<div class="result-value" markdown="1">

MI-Distillation在Qwen2.5-3B-Instruct和Llama3.2-3B-Instruct上都取得最佳平均性能，分别比最强基线高1.12和1.40个百分点；在AMC23、MATH-500和OlympiadBench等较具挑战性的任务上也有一致收益。

</div>

这说明方法并非只适配某一个学生模型家族，也不仅改善基础难度题目。结果支持“从教师数据谱中选择更适合学生的轨迹”有助于蒸馏，但不能单独证明提升完全来自SeqLSS，因为MI-Distillation同时包含模型插值和轨迹选择两个设计。

<div class="result-source" markdown="1">

来源：第6.1节“Main Results”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MI-Distillation achieves the best average performance on both Qwen2.5-3B-Instruct and Llama3.2-3B-Instruct, outperforming the strongest baseline by 1.12 and 1.40 points, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 与固定插值系数$\lambda$的直接蒸馏比较（Qwen2.5-3B-Instruct）

<div class="result-value" markdown="1">

在GSM8K、MATH-500和AMC23上，MI-Distillation分别比最强固定$\lambda$变体高0.19、2.70和1.09个百分点。固定系数之间不存在跨任务通用的最优值：$\lambda=0.8$在GSM8K最好，而$\lambda=0.4$和$\lambda=0.6$分别在MATH-500与AMC23更强。

</div>

该对照隔离了“自适应选轨迹”相对于“固定使用一种插值教师分布”的价值。它表明不同题目或任务可能需要不同的信息密度与可学习性平衡；但实验只报告了三个任务上的固定系数比较，不能据此断言该规律适用于所有推理领域。

<div class="result-source" markdown="1">

来源：第6.1节“Comparison with Fixed Interpolation Coefficients”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MI-Distillation consistently achieves the best performance across GSM8K, MATH-500, and AMC23, outperforming the strongest fixed-λ baseline by 0.19, 2.70, and 1.09 points, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### SeqLSS与候选轨迹选择基线的比较

<div class="result-value" markdown="1">

在相同的模型插值候选轨迹池上，SeqLSS取得最佳平均性能，并在五个基准中的四个上超过PPL、IFD和随机选择；反向选择最低SeqLSS分数的SeqLSS-min整体最差。

</div>

这个实验直接检验排序标准，而不是重新比较不同教师或不同训练预算。SeqLSS优于随机选择说明候选轨迹的质量并非均匀；SeqLSS-min最差则支持作者关于“高分轨迹更有用”的排序方向。不过原文未明确报告该段对应表格中各基准的具体分数，因此不能从这里判断每个任务的提升幅度。

<div class="result-source" markdown="1">

来源：第6.1节“Ablation on the SeqLSS Selection Criterion”，Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 3, SeqLSS achieves the best average performance and outperforms all baselines on four of the five benchmarks.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验训练语料仅来自MATH训练集的7,500道随机抽样题目，评测虽包含GPQA-Diamond等科学推理任务，但原文未明确报告跨领域训练数据或去污染处理，因此跨领域收益的来源仍不清楚。
- 主要结果强调平均性能和部分任务上的提升，但所给章节未提供Table 2、Table 3的完整数值、所有基线的逐任务结果及统计显著性检验；此外，$\alpha$的敏感性分析被放在附录D.5，而当前材料未给出其具体数值，故对稳定性和最优超参数的判断仍需核查原文表格。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Short-CoT和Long-CoT直接蒸馏：分别使用指令型教师和推理型教师生成的轨迹，构成最直接的对照，用于检验“推理越长是否越适合小学生”这一核心问题。
- Mix Long：按4:1比例随机混合Short-CoT与Long-CoT轨迹，测试简单的数据级混合能否同时获得简洁性与详细推理的信息。
- Mix Large：沿用4:1混合比例，并引入不同规模教师生成的轨迹，测试教师规模多样性是否足以替代按学生可学习性进行筛选。
- Curriculum Learning：采用两阶段手工课程，从“Instruct + NoThink”过渡到“NoThink + NoRethink”，测试预先规定的推理格式转变能否改善学生适应过程。所有基线使用相同问题、答案过滤、提示格式、学生架构和优化超参数，因此主要差异在轨迹的选择、混合或调度策略。

**实验想回答的问题**

- 在相同学生模型、问题集合、提示格式和优化设置下，MI-Distillation能否相较于Short-CoT、Long-CoT及混合或课程式基线，稳定提升小模型的数学与科学推理能力？
- 性能提升究竟来自模型插值所形成的教师数据谱，还是来自SeqLSS对候选轨迹的自适应筛选与可学习性控制？

**实验实现**

实验使用Qwen2.5-3B-Instruct和Llama3.2-3B-Instruct两个不同模型家族的学生模型；32B教师端点为QwQ-32B（Long CoT）和Qwen2.5-32B-Instruct（Short CoT），附录还给出14B端点为DeepSeek-R1-Distill-Qwen-14B与Qwen2.5-14B-Instruct。候选轨迹以温度$T=0.6$、核采样$p=0.95$生成，最大长度为8,192 tokens。学生使用LLaMA-Factory和AdamW训练3个epoch，学习率为$1\times10^{-5}$，有效全局batch size为32，最大上下文长度为8,192，并采用bfloat16与DeepSpeed ZeRO-3 Offloading。评测沿用教师生成时的采样设置；AIME24和AMC23各进行16次独立评测，其余GSM8K、MATH-500、GPQA-Diamond、Minerva和OlympiadBench进行4次，报告均值及标准差。SeqLSS的可学习性惩罚系数默认设为$\alpha=4$；硬件为一台8张NVIDIA L20的服务器和一台8张NVIDIA RTX A5000的服务器。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| SeqLSS、PPL、IFD、随机选择与SeqLSS-min的选择标准消融 | SeqLSS在五个基准中的四个上超过其他选择基线并取得最佳平均性能；SeqLSS-min整体表现最差。 | 候选轨迹池和训练条件保持一致，因此该实验主要隔离SeqLSS排序方向与评分准则的作用。SeqLSS-min的反向结果削弱了“只要下采样就能提升”的解释，但由于原文未明确给出每项分数，无法分析该标准在具体任务上的收益大小。 | 第6.1节“Ablation on the SeqLSS Selection Criterion”，Table 3<br><span class="experiment-evidence">In contrast, SeqLSS-min performs worst overall, confirming that the improvement is attributable to the proposed ranking criterion rather than merely to subsampling the candidate pool.</span> |
| 可学习性惩罚系数$\alpha$对训练动态的影响 | 在Qwen2.5-3B-Instruct和Llama-3.2-3B-Instruct上，MI-Distillation的训练损失比Long-CoT和Mix Long更低且更稳定；增大$\alpha$通常带来更平滑的优化和更低的损失，且在Llama-3.2-3B-Instruct上更明显。Short-CoT训练损失最低。 | 该分析检验SeqLSS中的可学习性控制是否缓解复杂Long-CoT带来的优化困难。它支持较强的可学习性约束有助于训练过程稳定，但训练损失不是最终推理准确率，因而不能把更低损失直接等同于更强的泛化；原文还指出Short-CoT虽损失最低，却提供较少的丰富推理监督。 | 第6.1节“Training Dynamics under Different Learnability Penalties”，Figure 4<br><span class="experiment-evidence">Across both student backbones, MI-Distillation exhibits substantially lower and more stable training loss than Long CoT and Mix Long, indicating that selecting trajectories with explicit learnability control alleviates the optimization difficulty introduced by overly complex reasoning traces.</span> |

**定性案例**

- 原文未提供具体题目的定性案例、逐步推理轨迹或错误分析；因此无法据此说明MI-Distillation在某类题目上具体如何改变推理过程，只能依据整体指标和训练曲线讨论其统计效果。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work proposes a method for distilling chain-of-thought reasoning trajectories into smaller language models through learnability- and information-aware data selection.; rule check: matched taxonomy keywords; top rule score=10.0
- 全文指纹：`d6f1732a10cb0dfe304c1199ed5066c81ff3413b63a8320f543546ac00ba3917`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
