---
title: "[论文解读] Is More Privileged Information Better? From Solution Traces to Problem-Solving Structure in Self-Distilled Reasoning"
description: "[arXiv 2608.01589][LLM Reasoning] 本文把同模型在线策略自蒸馏中的特权上下文设计视为可迁移性问题，并提出以沿验证轨迹提取的问题求解结构取代完整参考解，使教师监督更适合迁移到仅能观察题目的学生模型。"
arxiv_id: "2608.01589"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:03:06.044089+00:00"
source_sha256: "80f8d36bc81595ad84cd46f238eb35f73a175a464ea0588c4c9d60d12178eeef"
tags:
  - "LLM Reasoning"
  - "按策略自蒸馏"
  - "特权信息"
  - "数学推理"
  - "问题空间指导"
  - "状态转移"
  - "逐词监督"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.01589</p>

# Is More Privileged Information Better? From Solution Traces to Problem-Solving Structure in Self-Distilled Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Xuyang Zhao, Liting Zhang, Zichen Xu, Zhihu Wang, Xu Caiyue, Shiwan Zhao, Qicheng Li</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> TMCC, College of Computer Science, Nankai University, Tianjin, China；Huawei Technologies Ltd., Beijing, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01589v1) · [PDF 下载](https://arxiv.org/pdf/2608.01589v1) · **关键词** 按策略自蒸馏, 特权信息, 数学推理, 问题空间指导, 状态转移, 逐词监督<br>


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

本文把同模型在线策略自蒸馏中的特权上下文设计视为可迁移性问题，并提出以沿验证轨迹提取的问题求解结构取代完整参考解，使教师监督更适合迁移到仅能观察题目的学生模型。

**不用术语来说**：训练时，教师模型能看到完整参考答案，学生模型最终却必须只看题目独立作答。完整答案虽然提供的信息更多，却也包含特定答案、推理顺序、措辞和计算细节；教师可能据此给出学生在实际推理时无法复现的提示。因此，关键不只是让教师知道得更多，而是决定应当向教师提供什么形式的信息，才能真正提升学生脱离参考答案后的解题能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将同模型在线策略自蒸馏中的特权上下文设计明确表述为迁移问题，并提出轨迹落地的“问题空间指导”：从验证参考轨迹中保留初始状态、目标条件、约束和选定的状态转移路径，各步进一步描述算子、前置条件、变换及结果状态。
- 作者提出问题空间引导的在线策略自蒸馏（PS-OPSD），仅用上述结构化指导替换教师所见的完整参考解，保持学生的仅题目在线策略采样和逐词元蒸馏目标不变，从而隔离并检验特权信息表示方式本身的作用。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于数学推理模型的知识蒸馏研究。传统知识蒸馏让学生模型模仿教师模型的预测，而在按策略自蒸馏（OPSD）中，学生与教师是同一模型的两种输入视图：学生只读取问题并生成自己的推理轨迹，特权教师额外读取已验证的参考解答，再沿学生实际生成的前缀提供逐词概率监督。这样可使训练时接受监督的状态更接近学生部署时真正访问的状态，并避免长期依赖更强的外部教师；但训练时教师拥有完整解答，推理时学生只有问题，因而形成特权信息不对称。本文据此把研究重点从“如何修改蒸馏损失”转向“教师应看到何种特权信息”，并借用经典问题空间表示，将解题过程描述为初始状态、目标条件、约束以及由算子连接的一条有效状态转移路径。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**按策略自蒸馏（On-Policy Self-Distillation, OPSD）**

学生先依据问题生成当前策略下的推理前缀，教师再对这些学生实际访问的前缀给出下一词分布，学生通过分布匹配接受密集监督。这里的教师不是独立的更强模型，而是额外看到参考解答的同一模型视图。

</div>
<div class="concept-item" markdown="1">

**特权信息（Privileged Information）**

特权信息是训练时可提供、部署推理时不可获得的附加信息，本文中包括完整参考解答或从中抽取的问题空间指导。它只有在学生能从问题本身内化并复现相关知识时才有迁移价值，否则可能产生依赖答案、措辞或特定计算步骤的捷径。

</div>
<div class="concept-item" markdown="1">

**问题空间与状态转移**

问题空间把求解表示为从初始状态出发，在约束下应用算子并逐步达到目标条件的过程；每次转移可分解为算子、前置条件、变换和结果状态。本文不枚举全部可能状态与路径，只提取已验证参考轨迹实际经过的那一部分结构。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定数学问题$q$及其已验证参考解答$r$，标准OPSD让仅观察$q$的学生生成按策略推理轨迹及其前缀，再让额外观察$q$与$r$的同模型特权教师在这些前缀上提供逐词目标分布。核心假设是训练阶段可以使用$r$，但部署阶段只能输入$q$；因此输出必须是无需参考解答、提示、教师或抽取器即可完成的答案与推理。本文研究的变量不是学生轨迹生成方式或蒸馏目标，而是教师上下文的表示：它将完整$r$替换为离线抽取的问题空间指导$g(r)$，其中包含初始状态、目标条件、约束和一条选定的状态转移路径。该设定要检验的是：相较于信息更完整但高度实例化的参考解答，保留有效解题关系而弱化最终答案、表面措辞、固定推理顺序和具体算术细节的结构化指导，是否更容易迁移到仅看问题的学生。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$q$**

输入给学生和教师的数学问题。

</div>
<div class="notation-item" markdown="1">

**$r$**

训练阶段可用的已验证参考解答，部署阶段不可用。

</div>
<div class="notation-item" markdown="1">

**$g(r)$**

由参考解答离线抽取的问题空间指导，包括初始状态、目标条件、约束和选定的状态转移路径。

</div>
<div class="notation-item" markdown="1">

**$y_{<t}$**

学生按当前策略生成的、第$t$个词之前的推理前缀；教师在该前缀处提供下一词监督。

</div>

</div>

**直接相关的工作**

- **OPSD（Zhao et al., 2026a）**: 它确立了本文沿用的基本训练框架：问题侧学生产生按策略前缀，读取已验证解答的同模型教师在这些前缀上提供密集的逐词监督。PS-OPSD保持学生轨迹与分布匹配目标不变，只把教师看到的完整参考解答改为轨迹落地的问题空间指导，因此它是本文最直接的比较起点。
- **AVSD（Nguyen et al., 2026）**: AVSD通过完整解答、部分解答和仅答案等多个教师视图构造共识与门控残差信号，以缓解教师视图依赖。本文处理同一信息不对称问题，但选择在蒸馏前重构单一教师视图，以问题求解关系替代完整解答，而不是融合多个暴露程度不同的教师。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推理模型部署时通常只能获得题目，但在线策略自蒸馏的训练教师可以额外读取验证参考解。若教师的逐词元预测依赖这些部署阶段不存在的信息，学生即使在训练中很好地匹配教师，也可能学到无法在仅题目条件下稳定调用的行为，甚至显式提及并不存在的参考答案、答案键或提示。因此，需要一种既能利用验证解提供可靠监督、又尽量避免学生依赖训练期专属信息的教师上下文。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **同模型在线策略自蒸馏（OPSD）**：学生只根据题目生成自己的推理轨迹；同一模型的特权教师额外读取完整验证参考解，并在学生实际访问的前缀上提供下一词元分布监督。这样可降低训练前缀与仅题目推理时所遇前缀之间的偏差，也不需要长期依赖一个独立且更强的外部教师。
- **完整参考解条件化的特权监督**：该设计把完整解答直接放入教师上下文，使教师能够利用最终答案、完整推导顺序、具体措辞和实例计算来判断学生前缀之后应生成什么。其优势是信息充分且与正确解绑定，但这些信息并不都能从题目本身恢复。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 训练与部署接口不对称：教师看到完整参考解，学生部署时只看到题目。教师给出的逐词元目标可能依赖最终答案、特定推理顺序或局部计算等参考解专属信息，导致监督虽然信息量大，却不一定能迁移到仅题目推理。
- 完整解把可复用的数学关系与某个实例的表面实现绑定在一起；已有研究还观察到经此类训练的模型会提及输入中并不存在的参考解、答案键或提示。作者将其视为潜在依赖的行为迹象，但也明确指出，这类表面现象本身不能证明所有形式的特权信息泄漏。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有讨论已经表明教师选择、信息不对称和词元级可教性会影响自蒸馏，但仍缺少一种经过控制的特权信息表示：它应继续以验证解为依据，保留完成任务所需的关系与有效状态变化，同时削弱对特定答案表述、推理措辞和实例化细节的绑定。尚不清楚，仅改变教师所见信息的表示而保持学生采样与蒸馏目标不变，能否改善仅题目条件下的迁移。

</div>
<div markdown="1"><span>核心问题</span>

在同模型在线策略自蒸馏中，特权教师究竟应观察完整参考解，还是观察由验证轨迹提取的、以初始状态、目标、约束和连贯状态转移为核心的问题求解结构，才能为仅看题目的学生提供更可迁移的监督？

</div>
<div markdown="1"><span>作者直觉</span>

完整参考解像是把某一道题已经走完的全部脚印交给教师，其中既有通用路线，也有只适用于该答案的措辞和计算。问题空间指导则把脚印改写成“从什么状态出发、要达到什么目标、必须遵守什么约束、每一步通过什么操作改变状态”。这种关系结构仍由正确轨迹支撑，却更接近学生从题目中能够重建的解题规则；因此，教师的预测较少依赖不可见的答案细节，更可能转化为学生部署时可独立使用的推理能力。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PS-OPSD（Problem-Space-Guided On-Policy Self-Distillation，问题空间引导的同策略自蒸馏）保留原始 OPSD 的学生采样方式与蒸馏目标，只改变教师可见的特权信息。给定训练集中的问题—验证解答对 $(q,r)$，离线提取器不把完整解答 $r$ 直接交给教师，而是生成结构化指导 $g_{\mathrm{PS}}(q,r)=\langle s_0,G,C,\pi\rangle$：初始状态 $s_0$ 描述已知量与关系，目标条件 $G$ 规定何时算解题成功，约束 $C$ 记录定义域、不变量和合法性要求，路径 $\pi$ 则把参考解答压缩为一串状态转移。训练时，学生仅根据问题 $q$ 生成自己的推理轨迹 $\hat y$；固定教师在相同的学生前缀 $\hat y_{<t}$ 上额外读取结构化指导，产生逐词概率目标，学生通过坐标裁剪的温度化 KL 形式损失逼近该目标。最终只更新学生参数 $\theta$，推理时仍使用 $p_\theta(\cdot\mid q)$，不需要参考解答、指导、提取器、教师或规划模块。

技术上的关键不是增加一个新的推理器，而是重新编码训练期特权信息：完整参考解答可能含有依赖特定答案和后续步骤的词级线索，这些线索在测试时不可获得；问题空间指导则突出“当前有什么、要达到什么、必须遵守什么、可以怎样逐步变化”。通俗地说，普通 OPSD 像让教师拿着完整标准答案逐字纠正学生，PS-OPSD 则让教师拿着一张由标准答案提炼出的路线图纠正学生；学生练习和考试时看到的仍然都只有题目，因此没有改变部署接口。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造训练实例并离线提取问题空间指导

对每个 $(q_i,r_i)$ 调用离线提取器，生成并缓存 $g_i=g_{\mathrm{PS}}(q_i,r_i)=\langle s_0,G,C,\pi\rangle$；概念上的完整问题空间 $\mathfrak P(q)=\langle S,s_0,O,G,C\rangle$ 不被显式枚举。

<div class="method-step__io" markdown="1">

**输入**：数据集 $\mathcal D=\{(q_i,r_i)\}_{i=1}^{N}$，其中 $q_i$ 是数学问题，$r_i$ 是经过验证的参考解答。<br>
**输出**：训练可复用的缓存数据对 $(q_i,g_i)$。

</div>

**直观理解**：提取器把一份完整标准答案整理成“已知条件、目标、规则和步骤路线”，避免训练过程中反复处理原解答。它只抽取参考解答实际走过的一条路径，不声称列出所有可能状态和操作。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 由问题专用学生进行同策略采样

学生在不读取 $g$ 或 $r$ 的条件下采样完整轨迹 $\hat y\sim p_\theta(\cdot\mid q)$，并将每个位置之前的内容记为前缀 $\hat y_{<t}$。

<div class="method-step__io" markdown="1">

**输入**：小批量中的问题 $q$ 与当前学生模型 $p_\theta$。<br>
**输出**：当前学生真实会生成的推理轨迹 $\hat y$ 及其所有逐词前缀。

</div>

**直观理解**：“同策略”表示训练样本来自学生当前自己的行为，而不是只模仿一条固定标准答案。教师因此要面对学生实际可能写出的正确、绕路或错误前缀，并从这些位置提供纠正信号。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在相同前缀上计算教师与学生分布

教师计算 $p_{T,t}^{\mathrm{PS}}=p_T(\cdot\mid q,g,\hat y_{<t})$，学生计算 $p_{\theta,t}=p_\theta(\cdot\mid q,\hat y_{<t})$；两者观察同一问题和前缀，但只有教师额外获得 $g$。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、缓存指导 $g$、学生前缀 $\hat y_{<t}$、固定教师 $p_T$ 和学生 $p_\theta$。<br>
**输出**：每个位置 $t$ 上覆盖完整词表 $\mathcal V$ 的教师目标分布与学生预测分布。

</div>

**直观理解**：这相当于让教师和学生都读到学生已经写出的同一段答案，但教师手边多一张结构化路线图。比较的是“下一词应如何分配概率”，而不只是检查最终答案对错。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算坐标裁剪的温度化蒸馏损失

先用温度 $T$ 软化教师和学生的 logits，再对词表中每个词元的 KL 形式贡献分别取不超过 $c$ 的值，随后在完整词表、非填充序列位置和小批量上求平均。

<div class="method-step__io" markdown="1">

**输入**：各位置的 $p_{T,t}^{\mathrm{PS}}$、$p_{\theta,t}$，温度 $T$ 与裁剪阈值 $c$。<br>
**输出**：轨迹级损失 $\ell(q,g)$ 及小批量训练目标 $\mathcal L_{\mathrm{PS\text{-}OPSD}$。

</div>

**直观理解**：温度让模型之间的比较包含候选词的相对偏好，而不只看概率最大的词；逐坐标裁剪限制少数极端概率差异主导更新。由于裁剪发生在求和之前，该量是工程化的 KL 形式目标，而不是原始数学 KL 散度。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 问题空间指导序列化

$$
g_{\mathrm{PS}}(q,r)=\langle s_{0},G,C,\pi\rangle,\qquad \pi=(\tau_{1},\ldots,\tau_{k}),\qquad \tau_i=(o_i,\mathrm{pre}_i,\mathrm{transform}_i,s_i)
$$

**符号说明**

- $g_{\mathrm{PS}}(q,r)$：从问题与验证参考解答中离线提取的问题空间指导
- $q$：输入数学问题
- $r$：经过验证的参考解答
- $s_0$：初始状态，包括变量、实体、已知量及其关系
- $G$：目标条件，即待求目标和可验证的成功条件
- $C$：全局约束，包括定义域、不变量和合法性条件
- $\pi$：由参考解答导出的有序状态转移路径
- $\tau_i$：路径中的第 i 个状态转移记录
- $k$：选定路径包含的转移数量
- $o_i$：第 i 步采用的操作符
- $\mathrm{pre}_i$：第 i 步在前一状态中必须满足的局部前置条件
- $\mathrm{transform}_i$：第 i 步操作引起的状态变化
- $s_i$：执行第 i 步后得到的结果状态

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定教师指导中究竟保留什么信息：不是复制整篇答案，而是记录问题的起点、终点、规则以及一条连贯的参考路径。路径内部进一步拆成“做什么、何时能做、怎样改变、得到什么”，因此教师可用结构化的过程信息判断学生前缀下一步应如何发展。<br>
**原文位置**：第 3 节“Explicit Problem-Space Guidance”，公式（3）与公式（4）

</div>

</div>

<div class="equation-block" markdown="1">

#### 坐标裁剪的温度化 PS-OPSD 目标

$$
p^{(T)}=\operatorname{softmax}(z_p/T),\quad q^{(T)}=\operatorname{softmax}(z_q/T),\quad d_T(p,q;v)=p^{(T)}(v)\log\frac{p^{(T)}(v)}{q^{(T)}(v)},\quad \widetilde D_{c,T}(p\|q)=\sum_{v\in\mathcal V}\min\{d_T(p,q;v),c\},\quad \mathcal L_{\mathrm{PS\text{-}OPSD}}=\mathbb E_{\substack{(q,r)\sim\mathcal D\\\hat y\sim p_\theta(\cdot\mid q)}}\left[\frac{1}{|\hat y|}\sum_t\widetilde D_{c,T}\left(p_{T,t}^{\mathrm{PS}}\|p_{\theta,t}\right)\right]
$$

**符号说明**

- $z_p$：作为第一参数的教师分布在 softmax 前的 logits
- $z_q$：作为第二参数的学生分布在 softmax 前的 logits
- $T$：控制概率分布软化程度的温度
- $p^{(T)}$：教师 logits 经温度缩放后得到的概率分布
- $q^{(T)}$：学生 logits 经温度缩放后得到的概率分布
- $v$：词表中的一个词元
- $\mathcal V$：模型的完整词表
- $d_T(p,q;v)$：词元 v 对温度化 KL 形式距离的单坐标贡献
- $c$：施加于每个词元贡献的裁剪上限
- $\widetilde D_{c,T}(p\|q)$：先逐词元裁剪、再对完整词表求和的实现型距离
- $\mathcal L_{\mathrm{PS\text{-}OPSD}$：PS-OPSD 的期望训练损失
- $\mathcal D$：由问题与验证参考解答组成的训练分布
- $\hat y$：学生依据问题同策略采样的完整推理轨迹
- $|\hat y|$：学生轨迹的有效序列长度
- $t$：轨迹中的词元位置
- $p_\theta$：参数为 theta 的问题专用学生模型
- $\theta$：训练中唯一被更新的学生参数
- $p_{T,t}^{\mathrm{PS}}$：教师读取问题、问题空间指导和学生前缀后在位置 t 给出的目标分布
- $p_{\theta,t}$：学生仅读取问题和自身前缀后在位置 t 给出的预测分布

<div class="equation-explanation" markdown="1">

**直观理解**：目标先在学生自己生成的轨迹上逐位置比较教师和学生。每个词元的概率差异超过阈值后不再线性增大，因此单个极端坐标较难支配整个梯度；再对轨迹长度归一化，使不同长度回答具有可比较的损失尺度。该目标把结构化指导的作用限制在教师目标分布中，梯度只推动学生在仅见问题和自身前缀时复现这种预测偏好。<br>
**原文位置**：第 3 节“Training and Question-Only Inference”，公式（6）与公式（7）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是在 $(q,r)\sim\mathcal D$ 且 $\hat y\sim p_\theta(\cdot\mid q)$ 的联合采样下，最小化教师分布 $p_{T,t}^{\mathrm{PS}}$ 到学生分布 $p_{\theta,t}$ 的平均坐标裁剪距离。教师以 $q$、$g_{\mathrm{PS}}(q,r)$ 和学生前缀 $\hat y_{<t}$ 为条件，学生只以 $q$ 和 $\hat y_{<t}$ 为条件；因此优化要求学生吸收教师借助问题结构形成的逐词偏好，同时不能直接依赖训练期指导。实际计算覆盖完整词表，先对每个词元贡献应用阈值 $c$，再对非填充位置、轨迹和小批量平均；固定 $p_T$，仅通过反向传播更新 $\theta$。

这一目标与标准监督微调的区别在于，监督信号不是参考解答中的唯一目标词序列，而是教师针对学生当前轨迹给出的完整概率分布；与原始 OPSD 的目标形式则基本相同，核心替换是教师读取结构化 $g_{\mathrm{PS}}(q,r)$ 而非完整 $r$。因此，论文的方法变量可以明确归因于特权信息表示，但坐标裁剪意味着损失值不能按未经修改的 KL 散度解释。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 问题空间指导表示**

指导 $g_{\mathrm{PS}}(q,r)$ 包含四个顶层字段：初始状态 $s_0$、目标条件 $G$、约束 $C$ 和选定路径 $\pi$。路径写成 $\pi=(\tau_1,\ldots,\tau_k)$，每个转移 $\tau_i=(o_i,\mathrm{pre}_i,\mathrm{transform}_i,s_i)$ 依次记录操作符、局部前置条件、状态变化及结果状态；预期所有 $s_0,\ldots,s_k$ 都满足 $C$，末状态 $s_k$ 满足 $G$。

> 直观理解：该表示同时保留全局解题要求和局部步骤之间的因果顺序，使教师知道每一步为什么合法、执行后改变了什么。它省略难以穷举的完整状态空间 $S$ 和操作集合 $O$，也刻意不把实例化的最终答案作为顶层输出。

**2. 非对称特权教师—问题专用学生**

教师目标为 $p_T(\cdot\mid q,g_{\mathrm{PS}}(q,r),\hat y_{<t})$，学生预测为 $p_\theta(\cdot\mid q,\hat y_{<t})$；教师固定，且指导只进入教师上下文。与原始 OPSD 的差别仅是用 $g_{\mathrm{PS}}(q,r)$ 替换教师上下文中的完整解答 $r$，学生采样和学生输入均不改变。

> 直观理解：非对称设计允许教师在训练时知道更多，却强制学生始终按考试条件练习。这样可以检验性能差异是否来自“特权信息怎样表示”，而不是来自给学生增加提示、规划器或另一套生成流程。

**3. 坐标裁剪的全词表蒸馏器**

在每个非填充位置，方法对完整词表 $\mathcal V$ 计算温度化分布，并将每个词元贡献 $d_T(p,q;v)$ 单独截断到上限 $c$ 后再求和。训练清单需绑定每次运行的温度 $T$ 和阈值 $c$，因为原文指出不同模型规模和运行的裁剪配置可能不同。

> 直观理解：教师不是只告诉学生唯一的下一词，而是传递对整个词表的偏好；裁剪则降低极端分歧造成不稳定更新的风险。解释复现实验时必须把它视为特定实现的蒸馏距离，不能直接等同于标准 KL 散度。

**训练与推理**

训练前，对全部 $(q_i,r_i)$ 一次性执行指导抽取并缓存 $g_i$。每轮训练从 $\{(q_i,g_i)\}_{i=1}^{N}$ 采样小批量；学生先仅凭 $q$ 采样 $\hat y$，随后对每个位置 $t$，固定教师读取 $(q,g,\hat y_{<t})$，学生读取 $(q,\hat y_{<t})$，二者分别输出全词表分布。系统计算轨迹平均的温度化、逐坐标裁剪损失，对小批量求均值后更新 $\theta$；教师权重和缓存指导始终不变，循环直至训练预算耗尽。

推理时完全移除训练期特权通道，直接按 $p_\theta(\cdot\mid q)$ 生成推理与答案。既不把 $g_{\mathrm{PS}}$ 附加到学生提示中，也不调用参考解答、离线提取器、教师或额外规划模块；所以方法改善若能迁移到测试阶段，必须已经编码进学生参数，而不能来自测试时的信息泄漏或额外计算组件。

**复现信息**

公平复现最关键的细节有四项。第一，指导必须在训练前离线提取并缓存，且只供教师使用；若把它加入学生提示，就改变了问题设定。第二，教师与学生必须在同一个学生生成前缀 $\hat y_{<t}$ 上评分，才能保持同策略训练。第三，距离计算必须覆盖完整词表，并在词表求和之前对每个坐标贡献裁剪，然后只在非填充位置上平均；把总 KL 求和后再裁剪并不等价。第四，温度 $T$ 和阈值 $c$ 应随运行清单保存，因为原文明确说明不同规模和运行的裁剪配置存在差异，但所给章节未列出其具体取值。

提取器输出需保持四个顶层字段及路径内的转移结构，并保证转移来自验证解答 $r$；概念表示中的完整状态空间 $S$ 和可用操作集合 $O$ 不需要构造。原文还说明指导省略实例化最终答案，但所给章节没有明确报告提取器的模型、提示模板、抽取失败处理、教师与学生是否共享初始化权重，以及各规模对应的具体 $T$、$c$，这些内容仍需结合论文其余章节和运行清单核验。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- OpenThoughts的数学推理子集：作为训练数据。离线提取器根据每个问题及其经过验证的参考解答生成Problem-Space Guidance，并在训练前缓存；原文节选未明确报告训练样本数、具体划分规模及过滤规则。
- AIME24与AIME25：两个竞赛数学测试基准，用于分别检验模型对不同年度AIME题目的仅问题推理能力。各基准准确率还参与三基准非加权平均值的计算；原文节选未明确报告评测题数。
- HMMT25：另一项竞赛数学测试基准，用来检验结论能否从AIME迁移到不同来源的数学题；它与AIME24、AIME25共同构成跨基准汇总评测。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Question-only accuracy**

模型在推理时只能观察问题的情况下，最终答案正确的题目比例。该指标直接检验学生是否把训练所得能力转化为不依赖参考解答的独立解题能力。 （越高越好，因为更高准确率表示在相同仅问题输入条件下解决了更多测试题。）

</div>
<div class="metric-item" markdown="1">

**Avg**

AIME24、AIME25与HMMT25三个准确率的非加权算术平均，用于概括跨基准表现。主表采用oracle envelope：每个基准报告在该基准上选择出的最佳检查点，因此它反映训练期间可达到的最好结果，而不等同于统一检查点的部署性能。 （越高越好，因为它表示三个基准上的总体准确率更高；但必须结合单项结果与检查点选择方式解释。）

</div>
<div class="metric-item" markdown="1">

**Explicit PI-invocation rate**

生成结果中显式提及不可用的参考解答、答案键、提示或指导的比例，用于测量特权信息泄漏的一种可观察行为表现。 （越低越好，因为较低比例意味着模型较少在仅问题推理时诉诸实际不可见的信息；该指标只覆盖显式提及，不能排除隐性的依赖。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三种Qwen3规模上的跨基准oracle-envelope汇总结果

<div class="result-value" markdown="1">

PS-OPSD在1.7B、4B和8B上的三基准平均准确率分别为43.12%、64.32%和65.40%，每个规模均超过最强对照，领先幅度为1.54至2.04个百分点。

</div>

作者据此主张PS-OPSD具有跨模型规模的一致汇总优势。更准确地说，这证明其在按各基准分别选择最佳检查点的评测协议下，平均表现优于所比较方法；它不证明PS-OPSD在每一道题、每个基准或任意固定训练检查点上都占优，也未单独证明增益具有统计显著性。

<div class="result-source" markdown="1">

来源：第5节“Main Question-Only Performance”，Table 1相关正文

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The observed oracle-envelope Avg scores are 43.12, 64.32, and 65.40 for PS-OPSD at 1.7B, 4B, and 8B, exceeding the strongest baseline at every scale by 1.54–2.04 percentage points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 九个“模型规模—数学基准”单元格的逐项比较

<div class="result-value" markdown="1">

PS-OPSD在九个单元格中有六个严格最高；三个例外分别是1.7B的AIME25、4B的HMMT25和8B的AIME24，对照方法领先PS-OPSD的幅度依次为0.19、0.37和0.65个百分点。

</div>

这一结果把论文的核心结论限定为“跨基准总体更稳定”，而非“每个单项都最好”。三个反例的差距较小，但仍说明更合适的特权信息表示不会自动保证所有数据集和规模上的逐项统治；由于节选没有误差条或重复实验，不能判断这些小差距是否稳定。

<div class="result-source" markdown="1">

来源：第5节“Main Question-Only Performance”，Table 1相关正文

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The three exceptions are OPSD on AIME25 at 1.7B and AVSD on HMMT25 at 4B and AIME24 at 8B, where the respective gaps over PS-OPSD are 0.19, 0.37, and 0.65 points; the headline result is therefore cross-benchmark consistency, not uniform per-benchmark dominance.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 最终检查点上的显式特权信息调用行为

<div class="result-value" markdown="1">

在训练题上，OPSD与PS-OPSD的显式调用率分别为3.0%和0.5%；在留出验证题上分别为2.2%和0.4%。

</div>

作者将较低调用率解释为PS-OPSD较少依赖推理时不可见的、与参考解答绑定的信息，而且验证集结果表明该现象并非只出现在训练题上。分析上，这只是对显式措辞的行为测量：模型不提“参考解答”并不等于其内部表征完全没有吸收参考特有模式，因此不能把该结果直接等同于彻底消除信息泄漏。

<div class="result-source" markdown="1">

来源：第5节“Main Question-Only Performance”，Figure 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the training problems, the invocation rate at the final checkpoint is 3.0% for OPSD and 0.5% for PS-OPSD; on held-out validation problems, it is 2.2% and 0.4%, respectively.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主表的每个基准成绩由同一基准上的oracle-best检查点选出，这适合描述训练期间的性能上界，却可能产生选择乐观性，也不等同于使用统一验证规则选出一个可部署检查点。Figure 3的最终检查点结果缓解了这一问题，但所给节选没有提供其完整数值。
- 所给实验节选未明确报告随机种子、重复训练次数、置信区间或显著性检验，也未给出OpenThoughts训练规模及各评测集样本数。因此，对0.19至0.71个百分点等较小差异，应视为观察到的趋势，而不能据此断言其统计稳定性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Base：未经所述后训练的初始模型，用于衡量自蒸馏后训练带来的总体收益。节选只说明其比较目的，没有给出Base的具体结果。
- OPSD：标准在线策略自蒸馏方法，教师看到完整参考解答，学生只看到问题。它与PS-OPSD使用相同目标函数，二者主要差异是教师所见的特权信息表示，因此是判断“完整解答”与“问题空间指导”孰优的核心对照。
- AVSD：论文在主结果和训练轨迹中比较的另一种自蒸馏基线。它用于判断PS-OPSD的优势是否只相对于标准OPSD成立；但所给节选未解释AVSD的具体训练机制。
- Flattened PS：将问题空间指导的显式字段或边界扁平化的受控变体，用于检验结构化呈现本身是否有增益；它更接近消融条件，而非独立方法。

**实验想回答的问题**

- 在仅向学生提供问题、不给参考解答或问题空间指导的推理条件下，PS-OPSD能否在不同模型规模和数学推理基准上，比标准OPSD及其他自蒸馏方法取得更稳定的准确率提升？
- PS-OPSD的效果究竟来自哪些指导属性：显式字段结构、与当前题目的相关性，还是状态转移路径的全局连贯性；它是否同时减少模型在推理时显式依赖不可见特权信息的行为？

**实验实现**

实验覆盖Qwen3-1.7B、Qwen3-4B和Qwen3-8B。同一条件内教师与学生采用相同模型家族及初始化；所有OPSD变体中的教师均为初始Qwen3检查点，关闭LoRA适配器且不进行梯度跟踪，训练只更新学生的LoRA参数。PS-OPSD使用Qwen3.6-35B-A3B作为离线提取器，把问题与经验证的参考解答转换为Problem-Space Guidance；提取结果在训练前缓存，提取器不参与优化，也不用于仅问题推理。主表对每个“模型规模—基准”组合报告该基准上的oracle-best检查点，并对三个基准作非加权平均；Qwen3-4B另比较检查点20至100的匹配训练轨迹及最终检查点表现。该协议有助于区分“训练过程中可达到的最好成绩”和“同一最终检查点的实际表现”。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 目标相关性消融：PS-OPSD对比Mismatched PS，Qwen3-4B | PS-OPSD的平均准确率为64.32%，Mismatched PS为61.76%，相差2.56个百分点；下降出现在AIME24、AIME25和HMMT25三个基准上。 | Mismatched PS破坏指导与当前目标问题之间的匹配关系，同时保留“存在问题空间指导”这一大体形式，因此主要检验内容相关性。三个基准方向一致，支持相关指导是增益来源之一；不过该比较仍不能判定哪些字段最关键，也不能排除错配文本带来的额外干扰。 | 第5节“What Matters in Problem-Space Guidance”，Table 2<br><span class="experiment-evidence">The 2.56-point gap over Mismatched PS appears on all three benchmarks and is consistent with the importance of target-relevant guidance.</span> |
| 路径连贯性消融：PS-OPSD对比Path-Corrupted PS，Qwen3-4B | PS-OPSD的平均准确率为64.32%，Path-Corrupted PS为62.19%，相差2.13个百分点；三个基准上的结果都下降。 | Path-Corrupted PS破坏状态转移的全局顺序，用来隔离“解题路径是否连贯”这一属性。结果说明仅提供相关状态或步骤集合还不够，步骤之间合理的演进次序也会影响教师监督质量；但节选没有说明具体破坏操作及其强度，因此无法判断模型对哪类顺序错误最敏感。 | 第5节“What Matters in Problem-Space Guidance”，Table 2<br><span class="experiment-evidence">The 2.13-point gap over Path-Corrupted PS also appears on all three benchmarks and is consistent with sensitivity to globally coherent transition order.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper improves mathematical reasoning through problem-structure-guided on-policy self-distillation.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`80f8d36bc81595ad84cd46f238eb35f73a175a464ea0588c4c9d60d12178eeef`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
