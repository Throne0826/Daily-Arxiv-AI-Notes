---
title: "[论文解读] Reactivating Test-Time Scaling for Plane Geometry Problem Solving"
description: "[arXiv 2608.30156][VLM Reasoning] 本文研究如何通过增加推理轨迹的异质性、强化图形到符号的显式对齐，并按共识自适应分配采样预算，使测试时扩展在平面几何求解中重新有效。"
arxiv_id: "2608.30156"
announcement_date: "2026-09-01"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:29:34.016688+00:00"
source_sha256: "e22f9021f398d073e999da792a8d81d20db86f659d6a46b187538da39d55ae57"
tags:
  - "VLM Reasoning"
  - "LLM Reasoning"
  - "平面几何问题求解"
  - "多模态推理"
  - "测试时扩展"
  - "自洽性"
  - "符号程序"
  - "视觉落地"
  - "多轨迹推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.30156</p>

# Reactivating Test-Time Scaling for Plane Geometry Problem Solving

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Xiaoqiang Kang, Shengen Wu, Maizhen Ning, Xiaobo Jin, Kaizhu Huang, Yutao Yue, Xiaowei Huang, Qiufeng Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Advanced Technology, Xi’an Jiaotong-Liverpool University；Affiliation: Department of Computer Science, University of Liverpool；Affiliation: The Hong Kong University of Science and Technology (Guangzhou)；Affiliation: Hithink Research；Affiliation: Digital Innovation Research Center, Duke Kunshan University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30156v1) · [PDF 下载](https://arxiv.org/pdf/2608.30156v1) · **关键词** 平面几何问题求解, 多模态推理, 测试时扩展, 自洽性, 符号程序, 视觉落地, 多轨迹推理<br>
**代码**: [https://github.com/Jason8Kang/ReTTS-PGPS](https://github.com/Jason8Kang/ReTTS-PGPS)

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

本文研究如何通过增加推理轨迹的异质性、强化图形到符号的显式对齐，并按共识自适应分配采样预算，使测试时扩展在平面几何求解中重新有效。

**不用术语来说**：平面几何题既要求模型正确看懂图中的角度、点和线之间的关系，也要求它连续完成多步推导。常用的符号程序答案虽然精确，却往往只有一种固定写法；模型反复采样时难以产生真正不同且有价值的解题思路。同时，一旦模型把图中的视觉信息读错，例如把角度数值识别错，后续再严密的符号推理也会建立在错误前提上。因此，简单增加测试时采样次数通常不能像在一般数学题中那样稳定提升正确率。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出多轨迹合成（MTS）与感知增强（PA）训练：以前者把同一符号程序转换为语义一致但形式不同的原始程序、可执行 Python 脚本及带自然语言思维链的版本，以扩展可采样的推理空间；以后者要求模型先把图形解析为结构化语义子句，再进行符号推导，从而减少视觉信息与形式推理之间的脱节。
- 提出共识引导多轨迹集成（CG-MTE）：在较浅的解码阶段检查不同轨迹类型是否达成一致，只对仍存在分歧的题目追加采样，使更多计算集中于不确定样本，以改善准确率与推理成本之间的权衡。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

平面几何问题求解是多模态推理任务：模型需要联合理解题目文本与几何图像，识别点、线、角度及其关系，再通过多步逻辑或符号运算得到答案。现有路线包括先把图文解析为形式语言并调用符号求解器的神经符号方法、直接生成解题程序的神经模型，以及利用多模态大语言模型进行视觉—语言推理的方法。本文关注一个更具体的问题：测试时扩展在一般数学推理中可通过采样多条路径并聚合答案来提升准确率，但在以刚性符号程序表示解法的平面几何任务中，采样路径缺乏多样性，且图像误读会直接污染后续形式推导，因此扩展收益有限。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时扩展（Test-Time Scaling, TTS）**

在模型参数不变的情况下，于推理阶段投入更多计算，例如多次采样不同解题路径并聚合结果，以提高答案可靠性。本文考察这种策略能否从一般数学推理有效迁移到平面几何程序生成。

</div>
<div class="concept-item" markdown="1">

**自洽性（Self-Consistency, SC）**

对同一道题生成多条推理轨迹，再依据答案的一致程度进行选择，通常可理解为对最终答案进行多数投票。它要求采样轨迹既具有足够差异，又能让正确答案形成稳定共识。

</div>
<div class="concept-item" markdown="1">

**符号程序与视觉落地**

符号程序用结构化、可执行或可验证的操作表示几何推导；视觉落地则是把图中的角度、实体和关系准确对应到这些符号。若模型把图中的 $101^{\circ}$ 误读为 $104^{\circ}$，即使后续程序逻辑正确，也会得到错误结果。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是包含自然语言题干和几何图示的平面几何问题，输出是能够导出最终答案的推理结果；原有数据通常以经过验证的符号解题程序作为监督。研究设置以测试时多次生成和聚合为核心：标准自洽性期望不同采样路径汇聚到正确答案，但刚性程序往往使正确程序近乎唯一，重复采样容易产生相同程序或彼此不一致的错误程序。同时，图像中的实体、数值或关系若未先被可靠解析为结构化语义，感知错误会沿多步符号推导持续传播。本文因此把问题界定为：如何在不牺牲既有形式程序严谨性的前提下增加语义一致但表达异质的推理轨迹，并让模型在推导前显式建立图像到符号语义的对应，从而恢复测试时扩展的有效性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Inter-GPS**: 代表神经符号几何求解路线：先把图像和文本解析为形式语言，再由符号求解器完成推导。其结果具有可解释、可验证的优点，但形式推导依赖精确解析，因此对前端感知和解析错误较敏感，这直接对应本文所强调的视觉—符号鸿沟。
- **GeoThought**: 代表面向平面几何的高质量推理轨迹构造方法：使用教师多模态大模型生成带思维链的新问题，并通过拒绝采样和共识验证加强过程监督。与其合成新问题不同，本文以已验证的形式程序为起点派生多种语义对齐轨迹，目标是在保留符号严谨性的同时提升推理多样性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

平面几何求解是多模态推理的重要压力测试，因为系统必须把图像中的实体、数值和空间关系可靠地转化为可推导的条件，再执行精确的多步符号推理。实际错误具有级联性：早期视觉识别出现偏差后，后续推导即使形式上正确也会得到错误答案；而通过大量重复采样弥补错误又会带来较高计算成本。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **符号程序预测与神经符号几何求解**：模型根据题目文本和几何图形生成形式化求解程序，再由预定义算子或执行器完成计算。该范式能提供结构明确、便于执行和核验的推导，但训练数据中的程序通常十分简洁且写法刚性。
- **测试时扩展与自一致性（SC）**：模型在推理阶段对同一道题采样多条候选路径，再依据答案多数投票或一致性聚合选择最终结果。其有效前提是不同采样能够探索具有互补性的推理路径，并使正确答案逐渐形成稳定共识。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 刚性的符号程序压缩了自然语言中的中间思考过程，使多次采样常常只得到相同程序或若干彼此不一致的错误程序，缺乏足够的有效推理多样性；因此，增加采样预算不一定能让正确答案形成多数共识。
- 现有流程没有充分强调在符号推导前显式解析图形。模型可能误读角度数值或几何关系，并把错误视觉信号直接写入后续程序；自一致性只能聚合候选答案，不能从根本上修复所有候选共享的感知错误。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未给出一套面向平面几何的统一机制，同时满足三个条件：从单一形式程序构造语义一致但表达异质的推理路径，在演绎前建立显式且可监督的视觉—符号接口，并根据跨轨迹分歧动态决定是否继续采样。因而，测试时扩展在该任务中的潜力及其准确率—计算成本权衡仍未被充分释放。

</div>
<div markdown="1"><span>核心问题</span>

能否以已有符号程序为可靠推理种子，把它扩展为多种可训练、可采样的推理轨迹，并结合图形语义解析与共识驱动的自适应集成，使平面几何模型随着测试时计算增加而获得稳定收益，同时避免对简单题进行冗余采样？

</div>
<div markdown="1"><span>作者直觉</span>

同一道几何题若只允许一种短小的形式程序，就像要求所有解题者严格照同一份提纲作答，重复询问不会带来多少新信息。把该程序改写成可执行脚本和带自然语言解释的轨迹，相当于在保持结论约束的同时提供不同的推理视角；先把图形整理成结构化条件，则像在计算前先核对题设，降低错误输入污染整条推导链的风险。最后，若不同表达很快得到一致答案即可停止，而出现分歧时再追加样本，便能把计算用于真正困难或不确定的题目。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把平面几何求解建模为“先感知、后推理、再执行与集成”的端到端过程。训练数据中的每个实例写为 $\mathcal{I}=(D,Q,S,P,A)$：$D$ 是几何图像，$Q$ 是问题文本，$S$ 是从图中解析出的结构化语义子句，$P$ 是由几何算子组成的形式化解题程序，$A$ 是数值答案。作者先将单一的符号程序扩展为 Program、PAL、CoT-Program 和 CoT-PAL 等异构轨迹，再训练多模态大语言模型从 $(D,Q)$ 依次生成 $S$ 与推理轨迹 $T$；测试时执行轨迹得到候选答案，并通过自一致性或共识引导的多轨迹集成确定最终答案。

直观地说，原始符号程序像只有机器能读懂的“解题指令”。Multi-Trace Synthesis 将同一道题改写成程序、Python 代码以及带自然语言解释的不同版本，使模型学习多种表达和推导路径；Perception-Augmented Training 要求模型在计算前先把图中的垂直、相等、长度等关系明确写出来；CG-MTE 则让不同轨迹类型共同投票，简单题一旦形成唯一多数意见便提前停止，只有意见不一致的题才继续增加候选。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 形式化实例与程序实例化

每个程序步 $s_t=(\mathsf{op}_t,\mathsf{args}_t)$ 从包含 34 种几何定理或公理的算子集合 $\mathcal{O}$ 中选择算子，并作用于题目变量、过程变量或常量。预处理时将题目变量替换为具体数值，并把常量直接写入程序，使其无需额外变量映射即可执行。

<div class="method-step__io" markdown="1">

**输入**：几何图像 $D$、问题文本 $Q$、语义子句 $S$、形式化程序 $P=\langle s_1,\ldots,s_T\rangle$ 和答案 $A$。<br>
**输出**：自包含的实例化符号程序，以及与其对齐的图像、问题、语义子句和答案。

</div>

**直观理解**：这一步相当于把“对编号为 N1、N4 的边使用勾股定理”改写为对具体长度和未知量执行运算，避免运行程序时还要查另一张变量对照表。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. Multi-Trace Synthesis 多轨迹合成

方法沿格式转换与理由增强两个维度生成异构轨迹：规则系统把程序转换为可执行 PAL Python 脚本，MLLM 再生成含逐步解释的 CoT-PAL 与 CoT-Program。PAL 和 CoT-PAL 必须在沙箱中执行，运行结果与标准答案在相对容差 $\epsilon=0.001$ 内一致才被保留；CoT-PAL 失败时将错误信息反馈给模型，最多修复三轮。

<div class="method-step__io" markdown="1">

**输入**：每道训练题的实例化符号程序及其标准答案。<br>
**输出**：原始 Program、PAL、CoT-Program 和 CoT-PAL 等对齐到同一答案的训练轨迹集合。

</div>

**直观理解**：同一份几何解答被制作成“纯指令”“可运行代码”和“带讲解的指令或代码”等版本。执行验证像单元测试，可过滤虽然文字流畅但实际上算不出正确答案的代码轨迹。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. Perception-Augmented 联合训练

模型按自回归顺序先学习 $P_\theta(S\mid D,Q)$，把图中可见关系解析为显式语义子句；随后学习 $P_\theta(T\mid S,D,Q)$，在图像、题目和已解析子句的共同条件下生成可执行推理轨迹。两个阶段以联合负对数似然训练，使视觉解析错误和后续推理错误都直接受到监督。

<div class="method-step__io" markdown="1">

**输入**：图像与问题 $(D,Q)$，以及监督目标语义子句 $S$ 和某一种推理轨迹 $T$。<br>
**输出**：一个可从 $(D,Q)$ 先生成 $S$、再生成多种格式轨迹 $T$ 的统一多模态模型。

</div>

**直观理解**：模型不能直接看图后立刻“心算”，而要先列出诸如“$AC\perp DB$”和“$AB=3\sqrt{2}$”的已知条件，再据此推导。这类似学生先抄清题目条件，再开始写证明和方程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 执行、渐进集成与答案输出

模型对每种轨迹类型用束搜索生成排序候选并执行为答案 $a_{j,d}(x)$；CG-MTE 从深度 $d=1$ 开始汇集所有类型的前 $d$ 个答案，若出现唯一众数便输出，否则逐层扩展至 $D$。若最大深度仍无唯一众数，则回退到排名第一的 CoT-PAL 答案；该规则也可替换为统一模型多次采样后的标准自一致性投票。

<div class="method-step__io" markdown="1">

**输入**：测试实例 $x=(D,Q)$、轨迹类型数 $V$、每种类型的最大搜索深度 $D$，以及各类型的专用提示。<br>
**输出**：经执行和多轨迹投票确定的最终数值答案 $a^*$，以及由实际终止深度决定的推理采样成本。

</div>

**直观理解**：这相当于让几种不同风格的解法先各给一个答案；如果多数立即一致，就不再花计算量。只有答案打平或互相冲突时，系统才让每种解法继续提交次优候选，因此早停只是节省计算的经验规则，并不保证多数答案必然正确。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 感知增强联合训练目标

$$
\begin{aligned} \mathcal{L} &= -\log P_{\theta}(S,T\mid D,Q) \\ &= -\log\left[P_{\theta}(S\mid D,Q)\cdot P_{\theta}(T\mid S,D,Q)\right] \\ &= \underbrace{-\log P_{\theta}(S\mid D,Q)}_{\mathcal{L}_{\mathrm{perc}}}+\underbrace{-\log P_{\theta}(T\mid S,D,Q)}_{\mathcal{L}_{\mathrm{reason}}}. \end{aligned}
$$

**符号说明**

- $\mathcal{L}$：联合训练的负对数似然损失。
- $\theta$：多模态大语言模型的可训练参数。
- $D$：平面几何题的图像。
- $Q$：题目文本。
- $S=(S_1,\ldots,S_{|S|})$：从图像和题目中解析出的语义子句序列，例如垂直、等长和具体测量关系。
- $T=(T_1,\ldots,T_{|T|})$：目标推理轨迹的 token 或步骤序列。
- $\mathcal{L}_{\mathrm{perc}}$：监督模型从图像与题目生成语义子句的感知损失。
- $\mathcal{L}_{\mathrm{reason}}$：监督模型在语义子句条件下生成推理轨迹的推理损失。

<div class="equation-explanation" markdown="1">

**直观理解**：联合概率按条件概率链式分解为“先读懂图”与“再基于读图结果推理”两项。优化时两项均采用标准自回归交叉熵，因此模型既不能只学会输出几何关系而不求解，也不能完全绕过显式视觉依据直接猜答案。<br>
**原文位置**：第 3.3 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 执行答案的自一致性多数投票

$$
a^{*}=\operatorname{mode}(\{a_i\}_{i=1}^{K})=\arg\max_{v\in\mathcal{V}}\sum_{i=1}^{K}\mathbb{I}(a_i=v),\qquad a_i=\operatorname{Exec}(T_i),\quad \mathcal{V}=\{a_1,\ldots,a_K\}.
$$

**符号说明**

- $T_i$：模型生成的第 i 条候选推理轨迹。
- $\operatorname{Exec}(T_i)$：解析并执行第 i 条轨迹的过程。
- $a_i$：第 i 条轨迹执行后得到的候选答案。
- $K$：参与自一致性投票的候选轨迹数量。
- $\mathcal{V}$：所有已执行候选答案构成的取值集合。
- $\mathbb{I}(a_i=v)$：指示函数；当候选答案等于 v 时取 1，否则取 0。
- $a^*$：出现次数最多的最终答案。

<div class="equation-explanation" markdown="1">

**直观理解**：模型先生成多条可能不同的推理路径，再把每条路径执行成数值，最终选择得票最多的结果。标准自一致性对统一模型的全部候选使用该规则；MTE 与 CG-MTE 也采用相同的投票思想，但候选来自不同轨迹格式，且 CG-MTE 逐层加入候选并在出现唯一众数时提前终止。<br>
**原文位置**：第 3.4.1 节，公式（2）；第 3.4.2 节将其用于多轨迹集成

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是最小化 $\mathcal{L}=\mathcal{L}_{\mathrm{perc}}+\mathcal{L}_{\mathrm{reason}}$。实现上，将目标语义子句 $S$ 与目标轨迹 $T$ 按顺序组织为自回归输出，分别对感知部分和推理部分计算标准 token 级交叉熵；轨迹监督来自原始 Program 与 MTS 合成格式的混合数据。这样，$\mathcal{L}_{\mathrm{perc}}$ 约束视觉信息必须被显式结构化，$\mathcal{L}_{\mathrm{reason}}$ 则要求后续解答真正利用 $S$ 生成可执行轨迹，而非只产生未经验证的自然语言答案。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 程序到 PAL 的可验证转换器**

转换器依次完成运行环境初始化、把每个几何程序步映射为代数方程、附加方程组求解器，以及过滤负长度等无效根。生成脚本在带超时限制的沙箱内执行，仅当预测结果 $\hat{a}$ 与标准答案 $a$ 在相对容差 $\epsilon=0.001$ 内匹配时才通过验证。

> 直观理解：符号程序本身表达的是“用哪个定理”，PAL 则把这些定理落成可实际求值的 Python 方程。沙箱验证防止错误翻译进入训练集，而无效根过滤负责排除代数上成立但几何上不可能的答案。

**2. 理由增强器**

CoT-PAL 在每条方程之前加入对应几何定理及其自然语言理由，同时保留脚本可执行性；CoT-Program 则按照原程序步的严格顺序加入自然语言解释。前者使用执行—报错—修复闭环，后者整体不可执行，因此推理时从生成文本中解析出程序部分再运行。

> 直观理解：该模块不是另造解法，而是为已有可靠程序补上“为什么使用这个定理”的说明。这样既保留符号执行的精确性，又向模型提供比僵硬操作序列更丰富的推理表达。

**3. Consensus-Guided Multi-Trace Ensemble**

对第 $j$ 种轨迹保留按束搜索排序的答案列表 $\mathcal{A}_j(x)=[a_{j,1}(x),\ldots,a_{j,D}(x)]$；在深度 $d$ 汇集所有类型的前 $d$ 个结果并检查是否存在唯一众数。与固定生成全部 $VD$ 个候选的标准 MTE 不同，CG-MTE 的实例 $x$ 只需生成 $Vd_x$ 个候选，其中 $d_x$ 是形成共识或达到上限时的终止深度。

> 直观理解：多种轨迹格式提供的价值在于错误模式不完全相同，集成可利用它们的答案一致性。算法按需增加搜索深度，因此不会让一眼就能形成共识的简单题消耗与困难题相同的预算。

**训练与推理**

训练前，作者先对各数据集的形式化程序进行实例化，并通过 MTS 生成 PAL、CoT-PAL 和 CoT-Program；其中 PAL 类轨迹须通过执行验证。以 PGPS9K 为例，8,021 个训练程序中有 4 个因违反非负线段长度或非退化拓扑等几何约束而未通过 PAL 验证，因此只从 PAL 与 CoT-PAL 分支排除，原始 Program 和 CoT-Program 仍保留；最终得到 8,017 条 PAL、8,017 条 CoT-PAL 和 8,021 条 CoT-Program，并与原始训练集混合。统一模型随后接受图像和问题，先输出语义子句，再输出指定格式或混合格式的推理轨迹。

推理阶段有两种路线。统一模型自一致性对同一输入通过束搜索或温度采样生成 $K$ 条路径，执行后进行多数投票；多轨迹路线则使用轨迹专用提示，分别要求同一微调模型生成不同格式。标准 MTE 固定生成全部 $VD$ 个候选，CG-MTE 则从每种格式的 top-1 开始检查唯一众数，仅在无唯一众数时把深度从 $d$ 增至 $d+1$，达到 $D$ 仍无共识时采用 top-1 CoT-PAL 结果。这里的“唯一众数”只表示当前票数最高者不并列；作者明确指出它是经验性停止规则，不是正确性证明，因为不同轨迹可能产生相关错误。

**复现信息**

模型骨干包括 Qwen2-VL-2B-Instruct、Qwen2.5-VL-3B-Instruct 和 Qwen3-VL-8B-Instruct，使用 Hugging Face TRL 的 SFTTrainer 与 DeepSpeed ZeRO-2，在 8 张 NVIDIA A100 80GB GPU 上微调。2B 与 3B 模型学习率为 $2\times10^{-5}$，8B 模型为 $5\times10^{-6}$；训练 10 个 epoch，采用余弦学习率调度、10% warmup 和 1,024 token 最大序列长度。

主结果默认使用贪心解码，即不采样且束宽为 1；测试时扩展另评估确定性束搜索，以及温度 $T=0.9$、top-$p=0.9$ 的核采样。PAL 脚本必须在带超时约束的沙箱中运行，并以相对容差 $\epsilon=0.001$ 核对答案；这一验证条件是公平理解数据质量与可执行正确性的关键，而具体超时时长原文节选未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- PGPS9K：广泛使用的平面几何问题求解基准；论文在其基础上应用 MTS，将每个符号程序扩展为四类推理轨迹，形成约 32.1K 个训练实例的 PGPS9K-All。它既用于主训练与测试，也用于测试时扩展和误差耦合分析。
- Geometry3K：平面几何问题求解基准；经 MTS 扩展后形成约 33.7K 个训练实例的 Geometry3K-All，用于检验方法在另一数据分布上的泛化表现。
- GeoQA：几何问答基准；由于原数据没有 PA 训练所需的语义子句标注，作者按 PGPS9K 的格式人工补充标注，并形成约 13.9K 个训练实例的 GeoQA-All，用于检验方法在不同任务来源上的有效性。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Answer accuracy（top-1 match）**

预测答案的数值与真实答案匹配的比例；当相对误差不超过 $\epsilon=10^{-3}$ 时视为正确。 （越高越好，因为它直接表示最终几何问题的答对率。）

</div>
<div class="metric-item" markdown="1">

**Absolute gain**

改进方法相对于对应基线的准确率百分点差值，例如 $71.2\%-58.6\%=12.6$ 个百分点。 （越高越好，但它是相对比较量，不能替代跨数据集或跨模型的绝对准确率。）

</div>
<div class="metric-item" markdown="1">

**Sampling budget**

测试时生成并聚合的候选解数量，例如 self-consistency 的 $K=40$；MTE 使用四种轨迹类型，每类保留最多 $D=10$ 个候选，因此最大预算为 $V D=4\times10=40$。 （在准确率相近时越低越好，因为它表示更少的推理采样成本。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### PA Training on MTS-All 对比 Direct Program Prediction

<div class="result-value" markdown="1">

三种模型在三个数据集上均有提升。8B 模型在 PGPS9K、Geometry3K 和 GeoQA 上分别达到 71.2%、74.5% 和 67.2%，相应直接程序预测基线为 58.6%、65.4% 和 60.9%；3B 模型达到 58.3%、64.7% 和 58.7%，2B 模型达到 50.8%、52.0% 和 53.5%。

</div>

这说明把单一符号程序扩展成异构轨迹，并要求模型先生成结构化语义子句再进行符号推理，能够稳定改善最终答题率，而且收益不依赖某一个模型规模或数据集。它支持两种设计共同有效，但不能仅凭该对比断定 PA 与 MTS 各自的独立贡献，因为这里同时改变了训练数据和训练目标。

<div class="result-source" markdown="1">

来源：Table 1；Section 4.1 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Ours: PA Training on MTS-All
Qwen3-VL-8B
71.2
(+12.6)
74.5
(+9.1)
67.2
(+6.3)

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 与通用多模态模型和专用几何求解器比较

<div class="result-value" markdown="1">

Qwen3-VL-8B 的准确率为 PGPS9K 71.2%、Geometry3K 74.5%、GeoQA 67.2%。在前两个数据集上，它高于最强被比较的专用求解器 LANS 的 66.7% 和 72.1%；相对通用 Qwen2.5-VL-72B 的 53.3%、50.5% 和 55.5%，分别高出 17.9、24.0 和 11.7 个百分点。

</div>

结果表明，针对几何任务进行 PA 与 MTS 训练，可以让较小的 8B 模型在这些基准上超过更大的通用模型，并在 PGPS9K 和 Geometry3K 上超过表中专用求解器。由于不同系统的训练数据、感知模块和推理接口可能不同，这一结果证明的是基准上的有效性，不等同于对所有几何任务或所有模型的普遍优越性。

<div class="result-source" markdown="1">

来源：Section 4.1 Main Results；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with general-purpose MLLMs, it substantially outperforms Qwen2.5-VL-72B by 17.9%, 24.0%, and 11.7% on the three benchmarks.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen3-VL-8B 在 MTS-All 上的 self-consistency 测试时扩展

<div class="result-value" markdown="1">

从 top-1 到 SC@40，PGPS9K 的准确率由 71.2% 提升至 76.7%，Geometry3K 由 74.5% 提升至 80.1%，GeoQA 由 67.2% 提升至 76.1%。GeoQA 的绝对提升接近 9 个百分点。

</div>

多候选解码和多数投票确实能从 MTS 产生的多种推理路径中获益，说明该训练框架重新激活了测试时扩展能力。提升并非随预算单调增加，例如部分数据集在 SC@28 或 SC@36 达到更高值后略有回落；因此更大采样预算不保证持续增益，且 self-consistency 使用完整预算时成本较高。

<div class="result-source" markdown="1">

来源：Section D.2；Table 9

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Specifically, answer accuracy improves from 71.2% to 77.2% on PGPS9K, from 74.5% to 80.7% on Geometry3K, and from 67.2% to 76.1% on GeoQA.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- GeoQA 的语义子句标注是作者人工补充的，文段未报告标注规模、标注一致性或公开标注质量，因此 PA 在该数据集上的收益可能受标注流程影响。
- CG-MTE 的跨轨迹错误并非独立：Table 10 报告 pairwise same-wrong 为 34.3%–39.8%，且论文明确指出跨轨迹共识只是经验性的早停信号，不是正确性保证；此外，主文给出的 self-consistency 表格在文字叙述与表格具体 SC@40 数值之间存在不一致，需回查原始论文。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Direct Program Prediction：在原始解答程序上直接训练并预测符号程序，是最直接的内部基线，用于隔离 MTS 数据扩展和 PA 训练带来的收益。
- Qwen2.5-VL-72B：通用多模态大语言模型基线，参数规模明显大于作者微调的模型，用于检验专门训练方法能否超过更大的通用模型。
- LANS：专门的神经几何求解器，用于比较作者方法与现有端到端几何系统在 PGPS9K 和 Geometry3K 上的表现。
- Pi-GPS：神经符号几何求解器，将神经感知与符号几何推理结合，用于比较不同神经符号设计下的解题能力。

**实验想回答的问题**

- 在 PGPS9K、Geometry3K 和 GeoQA 上，PA 训练结合 MTS-All 是否能稳定提升不同规模多模态模型的平面几何解题准确率，并超过直接程序预测及已有通用或专用求解器？
- 在模型已经具备多轨迹训练的情况下，测试时扩展是否能够继续提升准确率；CG-MTE 是否能以较少的采样成本取得接近高预算自洽性解码的效果？

**实验实现**

作者微调 Qwen2-VL-2B-Instruct、Qwen2.5-VL-3B-Instruct 和 Qwen3-VL-8B-Instruct，并以 2B、3B、8B 表示。每个基准分别使用对应的 MTS-All 数据进行 PA 训练；主结果默认采用贪心解码。MTS 为每个符号程序构造四类轨迹：Program、PAL、CoT-Program 和 CoT-PAL，其中 PAL 是可执行的 Python/SymPy 推理脚本，CoT 表示在程序执行前加入逐步自然语言分析。CoT 理由由 Gemini-2.5-Flash 生成。测试时扩展使用 beam search 或温度采样；self-consistency 的预算设为 $K=40$，MTE 的轨迹类型数为 $V=4$，每类最多保留 $D=10$ 个候选。InternVL3.5-2B 和 InternVL3.5-8B 的补充实验采用相同训练与评估协议。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| InternVL3.5 上移除 PA Training 或移除 PGPS9K-MTS | 在 InternVL3.5-2B 上，完整方法为 44.8%，去除 PA 为 38.8%（低 6.0 个百分点），去除 PGPS9K-MTS 为 41.7%（低 3.1 个百分点）；在 8B 上，完整方法为 48.5%，去除 PA 为 42.4%（低 6.1 个百分点），去除 MTS 为 45.2%（低 3.3 个百分点）。 | 该跨骨干网络消融把结论从 Qwen-VL 扩展到 InternVL：PA 和 MTS 都有贡献，且在该实验中 PA 的移除造成更大损失。它仍不能说明两者完全独立，因为消融只给出了整体删除组件后的结果，未报告更细的交叉组合或各轨迹类型单独贡献。 | Table 7；Appendix C.1<br><span class="experiment-evidence">Ours: PA Training on PGPS9K-All
PGPS9K-All
44.8
(+8.1)
48.5
(+8.3)</span> |
| 不同测试时解码策略：beam search 与 temperature sampling | 在 PGPS9K 的 top-40 分析中，beam search 随搜索深度增加会使 CoT-Program 与 CoT-PAL 合计占据超过 85% 的候选；在 $k=4$ 时，可执行的 PAL 与 CoT-PAL 轨迹占 77%。温度采样的轨迹分布在不同 $k$ 下近乎不变，并更倾向集中到单一数值答案。 | 这一分析检验的不是单个最终准确率，而是解码器是否真正探索不同推理模式。作者的解释是 beam search 会逐步激活 CoT 轨迹，因而形成更丰富的候选池；温度采样的重复性更强，所以多数投票可利用的有效多样性较少。该结论来自分布分析，不能单独证明 beam search 在所有预算和数据集上都优于温度采样。 | Appendix D.3；Figure 10<br><span class="experiment-evidence">At low k (k=4), executable traces (PAL and CoT-PAL) dominate, accounting for 77%, reflecting a preference for rigorous code in high-confidence predictions.</span> |

**定性案例**

- PA 的定性案例显示：不使用 PA 时，模型容易直接把图形观察映射为符号操作，产生不完整或缺乏视觉依据的推理；显式预测语义子句后，视觉信息先被转换为结构化事实，再进入演绎过程，从而减少无效定理应用和几何步骤幻觉。不过轨迹质量评估也发现 CoT-PAL 可能虚构弦 $AB$ 与 $CE$ 平行，CoT-Program 可能捏造不存在的“circular balance theorem”，说明自然语言解释的流畅性不等于几何推理忠实性。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作核心是通过视觉 grounding、多轨迹推理和测试时扩展提升多模态平面几何问题求解能力。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`e22f9021f398d073e999da792a8d81d20db86f659d6a46b187538da39d55ae57`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
