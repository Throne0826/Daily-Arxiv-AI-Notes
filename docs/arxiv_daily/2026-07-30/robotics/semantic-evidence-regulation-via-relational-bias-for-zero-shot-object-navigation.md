---
title: "[论文解读] Semantic Evidence Regulation via Relational Bias for Zero-Shot Object Navigation"
description: "[arXiv 2606.10348][机器人 / 具身智能] SER-Nav将零样本目标导航从“依据语义线索选择搜索位置”改写为“动态调节语义证据可信度”，利用激活与抑制两类关系偏置强化可靠区域、压制误导区域。"
arxiv_id: "2606.10348"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.705258+00:00"
source_sha256: "dc2f4accd514403d3e3153c51597983990b75b3841c5edb35a23641111d9669f"
tags:
  - "机器人 / 具身智能"
  - "具身智能"
  - "零样本目标物体导航"
  - "开放词汇感知"
  - "语义证据调节"
  - "关系偏置"
  - "前沿探索"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2606.10348</p>

# Semantic Evidence Regulation via Relational Bias for Zero-Shot Object Navigation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Weitao An, Chenghao Xu, Xu Yang, Cheng Deng</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2606.10348v3) · [PDF 下载](https://arxiv.org/pdf/2606.10348v3) · **关键词** 具身智能, 零样本目标物体导航, 开放词汇感知, 语义证据调节, 关系偏置, 前沿探索<br>


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

SER-Nav将零样本目标导航从“依据语义线索选择搜索位置”改写为“动态调节语义证据可信度”，利用激活与抑制两类关系偏置强化可靠区域、压制误导区域。

**不用术语来说**：机器人在陌生室内寻找指定物体时，往往依赖视觉模型判断“哪里可能有目标”；但目标可能很小、被遮挡或与其他物体相似，视觉模型也可能误检或漏检。如果机器人把一次错误判断长期当真，就会反复前往没有目标的区域。本文要解决的是：机器人如何在探索过程中根据新观察和行动结果及时修正先前判断，而不是让错误线索持续支配搜索。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出关系偏置视角，将目标导航表述为搜索空间的动态调制问题：正向“激活”传播目标及上下文支持证据，负向“抑制”传播感知混淆与访问失败所产生的反证。
- 提出无需训练的SER-Nav框架：聚合多视角观测形成物体级关系证据，通过动态关系激活—抑制探索图更新前沿价值，并用可靠性感知的承诺门控避免过早追逐尚未充分确认的目标。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究具身智能中的零样本目标物体导航（ObjectNav）：智能体仅凭第一视角视觉观测，在未知室内环境中探索并到达指定类别的物体附近。完成任务不仅需要建立空间表示和规划可行路径，还要利用开放词汇感知识别未限定类别的物体，并借助场景语义关系判断更值得搜索的区域。实际观测中的目标可能较小、被遮挡、距离较远或与干扰物外观相似，因此语义线索并不稳定；本文所处的关键问题是，如何在无需任务专项训练和在线大语言模型推理的条件下，让导航系统在探索过程中动态判断哪些语义证据值得信任。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**零样本目标物体导航**

智能体接收目标类别名称，在此前未见的环境中通过移动和视觉观测寻找该类物体，而不依赖针对当前环境或目标类别重新训练的策略。任务同时考察目标发现、环境探索、路径规划和停止决策。

</div>
<div class="concept-item" markdown="1">

**开放词汇感知**

利用视觉—语言模型或开放词汇检测器，依据文本类别识别不局限于固定训练标签集合的物体。它扩大了可搜索目标的范围，但容易受到误检、漏检和相似类别混淆影响。

</div>
<div class="concept-item" markdown="1">

**前沿选择与语义先验**

前沿是地图中已探索自由空间与未知空间的边界，导航系统通常选择某个前沿作为下一探索目标。语义先验利用目标与场景或其他物体的共现关系为前沿排序，例如电视和茶几可能提高附近存在沙发的可能性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括目标物体类别、智能体逐步获得的第一视角视觉观测，以及探索过程中形成的空间和物体级证据；智能体在未知室内环境中反复选择探索区域、规划移动并判断是否对候选目标作出最终追踪或停止承诺。输出是一系列导航动作及最终目标定位结果，目标是在成功到达指定类别物体附近的同时缩短路径。论文假设开放词汇感知和语义关系能够提供搜索线索，但这些线索可能因误检、漏检、类别混淆、局部视角或不可达候选区域而失真；系统因此必须利用后续观测和交互反馈修正既有证据，而不能把已积累的语义分数视为固定事实。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **VLFM: Vision-Language Frontier Maps for Zero-Shot Semantic Navigation（Yokoyama et al., 2024）**: 该工作是零样本语义导航中的视觉—语言前沿地图方法，代表利用视觉语言语义为未知空间的探索前沿赋值并选择搜索方向的路线。SER-Nav关注这类语义引导机制未充分处理的问题：错误或过时的语义证据一旦影响前沿排序，可能持续把智能体引向无效区域。
- **SG-Nav: Online 3D Scene Graph Prompting for LLM-Based Zero-Shot Object Navigation（Yin et al., 2024）**: 该工作通过在线三维场景图组织物体及其关系，并借助大语言模型进行零样本导航推理，说明关系化场景信息可支持目标搜索。SER-Nav同样利用物体关系，但将重点放在正向激活与负向抑制对搜索空间的动态调节，并明确避免依赖在线大语言模型推理。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

开放词汇目标导航需要机器人在未知环境中依靠视觉观测和语义关系寻找目标，但真实室内场景中的遮挡、远距离、小目标和外观相似物会造成误检、漏检及类别混淆。若这些不可靠线索被写入地图或用于前沿选择，机器人可能持续搜索错误区域，浪费路径并降低到达目标的成功率。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **学习式导航策略**：通过大规模训练学习从当前观测和目标类别直接映射到动作或搜索决策，试图把视觉理解、环境探索与行动规划统一在策略模型中。
- **语义引导的地图式或自中心在线方法**：地图式方法把占据、物体或场景语义写入地图，再依据语义先验选择待探索前沿；自中心在线方法则基于第一人称局部观测，借助视觉—语言模型或常识关系推断下一步应搜索的位置。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 学习式策略通常需要大规模训练，并可能对训练环境的特定数据分布敏感；环境或目标分布变化时，其泛化能力和部署便利性受到限制。
- 现有语义引导方法通常把检测结果、静态先验或累积地图证据当作持续有效的正向依据，缺少根据后续观测与行动失败削弱或撤销证据的机制。因此，误检、类别混淆和过时假设一旦影响前沿选择，就可能长期保留并反复把机器人引向无效区域；依赖局部视图或在线视觉—语言推理的方法还会受到提示设计和模型响应不稳定性的影响。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有工作主要回答“根据语义信息去哪里搜索”，但尚未充分解决如何在线判断“哪些语义线索不应继续相信”，以及如何将新出现的反证和具身交互反馈系统地写回搜索空间。缺失的是一种无需额外训练、能够同时利用支持证据与矛盾证据，并随探索过程持续修正前沿价值和目标确认状态的调节机制。

</div>
<div markdown="1"><span>核心问题</span>

在开放词汇感知存在噪声的零样本目标导航中，能否利用物体之间的支持或混淆关系以及访问失败反馈，动态增强可靠语义证据、抑制已被质疑的证据，从而避免过早锁定目标并提高搜索可靠性与路径效率？

</div>
<div markdown="1"><span>作者直觉</span>

语义线索并非彼此独立：寻找沙发时，电视或茶几能提供支持，而外观相近的椅子可能制造歧义；同样，机器人前往某区域后仍无法接近或确认目标，本身就是该假设不可靠的负反馈。因此，可以把搜索区域看成同时受到“吸引力”和“排斥力”作用的场：可信的目标及上下文证据向相关前沿传播激活，混淽物体和失败事件传播抑制，再让门控机制只在证据足够可靠时决定追逐目标。这样既保留语义先验的搜索效率，又能让错误线索随着新证据被及时降权。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SER-Nav 是一个无需任务训练、也无需在线大语言模型推理的零样本三维室内目标导航框架。输入是每个离散时刻的第一视角观测 $o_t$、目标类别 g、当前地图与候选前沿；系统先用开放词汇感知获得物体位置、标签和置信度，再通过跨视角多标签竞争把噪声检测聚合成物体级证据。随后，它依据目标相关、上下文共现和视觉相似关系，分别在局部关系图中传播激活偏置与抑制偏置，用二者和路径代价共同修正前沿分数；只有当候选目标证据超过可靠性阈值时，智能体才从探索切换为目标接近，否则继续访问得分最高的前沿。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造目标中心的类别—动作关系

为每个类别 ℓ 分配三维角色向量 $b_g(ℓ)=[c_g(ℓ),a_g(ℓ),i_g(ℓ)]^⊤$：目标及同义词承担承诺与激活角色，上下文类别承担激活角色，视觉相似类别承担抑制角色。

<div class="method-step__io" markdown="1">

**输入**：目标类别 g，以及目标同义词、上下文共现类别和视觉相似干扰类别组成的关系集合。<br>
**输出**：将开放词汇类别标签映射为目标承诺、正向激活和负向抑制三类可执行证据的关系表。

</div>

**直观理解**：系统不只问“检测到了什么”，还问“这个类别应促使我靠近、在附近搜索，还是降低对该区域的信任”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 聚合跨视角检测并形成物体级证据

把不同视角下属于同一实体的检测聚为物体簇，对簇内每个候选标签结合多视角支持度与置信可靠性进行竞争；选出主导标签后，经有界归一化得到证据强度，并乘以该标签的类别—动作角色向量。

<div class="method-step__io" markdown="1">

**输入**：在线检测序列 $d_i=(p_i,s_i,ℓ_i)$，其中 $p_i$ 是投影到二维地图的位置，$s_i$ 是检测置信度，$ℓ_i$ 是预测类别。<br>
**输出**：每个物体 o 的证据向量 $h_o=[h_o^c,h_o^a,h_o^i]^⊤$，分别表示目标承诺、激活和抑制强度。

</div>

**直观理解**：同一物体在不同角度可能被叫成不同名字，因此系统像综合多名观察者的意见一样，不因一次高置信误检就永久确定其身份。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 在局部关系图上传播激活与抑制

构建包含物体证据节点、上下文假设节点、负证据节点和候选前沿的局部图，并使用传播半径 R 内随距离指数衰减的核函数传递证据。目标或上下文证据形成 $A_t(f)$，干扰物与未找到可靠目标的访问失败形成 $I_t(f)$；失败抑制会随时间衰减，并可被新的连续证据覆盖。

<div class="method-step__io" markdown="1">

**输入**：物体级证据、上下文物体、视觉相似干扰物、访问失败记录、二维地图位置及候选前沿集合 $F_t$。<br>
**输出**：每个候选前沿 f 的动态激活值 $A_t(f)$ 与抑制值 $I_t(f)$。

</div>

**直观理解**：激活相当于在可能有目标的区域附近“加亮”，抑制相当于给误导点和已经白跑过的区域“降温”；两种影响只在局部扩散，避免一条线索控制整张地图。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 偏置条件探索与可靠性门控承诺

以激活增强分子，以抑制和路径成本增大分母，计算更新后的前沿分数并选择最高分前沿；同时检查最可靠候选目标的承诺证据是否达到阈值 θ。未达到阈值时继续前沿探索，达到后使用 A* 局部规划器逐步接近候选目标，并在规定成功半径内执行 Stop。

<div class="method-step__io" markdown="1">

**输入**：基础语义响应 $S_t^0(f)$、激活 $A_t(f)$、抑制 $I_t(f)$、归一化路径代价 C̄_t(f)，以及各物体的目标承诺证据 $h_{o,t}^c$。<br>
**输出**：当前时刻的探索目标或目标承诺动作，以及最终的逐步离散导航行为。

</div>

**直观理解**：系统不会看到一个像目标的物体就立刻追过去，而是先权衡支持证据、反证和路程；只有证据足够稳定时才正式“押注”该目标。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 双偏置条件的前沿评分与选择

$$
\widetilde{S}_{t}(f)=\frac{S^{0}_{t}(f)+A_{t}(f)}{1+I_{t}(f)+\bar{C}_{t}(f)},\qquad f_{t}^{\star}=\arg\max_{f\in\mathcal{F}_{t}}\widetilde{S}_{t}(f)
$$

**符号说明**

- $t$：当前离散决策时刻。
- $f$：一个候选探索前沿，即已知可通行区域与未知区域的边界目标。
- $\mathcal{F}_{t}$：时刻 t 的候选前沿集合。
- $S^{0}_{t}(f)$：由 BLIP-2 根据目标类别与检测物体区域的语义对齐计算的基础语义响应。
- $A_{t}(f)$：目标证据和上下文假设传播到前沿 f 的正向激活。
- $I_{t}(f)$：视觉相似干扰物及访问失败传播到前沿 f 的负向抑制。
- $\bar{C}_{t}(f)$：智能体当前位置到前沿 f 的归一化路径成本。
- $\widetilde{S}_{t}(f)$：经激活、抑制和路径成本共同调节后的前沿分数。
- $f_{t}^{\star}$：更新分数最高、下一步将被探索的前沿。

<div class="equation-explanation" markdown="1">

**直观理解**：目标或上下文证据提高前沿吸引力，干扰证据、失败记忆和较长路程降低其优先级。采用除法意味着抑制与成本不仅是固定扣分，而会按当前证据强度共同压低不可信或代价高的候选。<br>
**原文位置**：式 (11)–(12)，Bias-conditioned Exploration and Target Commitment

</div>

</div>

<div class="equation-block" markdown="1">

#### 可靠性门控的探索—承诺决策

$$
o_{t}^{\star}=\arg\max_{o\in\mathcal{O}_{t}}h^{c}_{o,t},\qquad \Gamma_{t}=\mathbb{I}\!\left[h^{c}_{o_{t}^{\star},t}\geq\theta\right],\qquad \pi_{t}=\begin{cases}\pi_{\mathrm{commit}}(o_{t}^{\star}),&\Gamma_{t}=1,\\ \pi_{\mathrm{explore}}(f_{t}^{\star}),&\Gamma_{t}=0.\end{cases}
$$

**符号说明**

- $\mathcal{O}_{t}$：时刻 t 已聚合得到的物体证据节点集合。
- $h^{c}_{o,t}$：物体 o 在时刻 t 的目标承诺证据强度。
- $o_{t}^{\star}$：当前目标承诺证据最强的物体候选。
- $\theta$：触发目标承诺的可靠性阈值。
- $\mathbb{I}[\cdot]$：条件成立时为 1、否则为 0 的指示函数。
- $\Gamma_t$：探索与目标承诺之间的二值门控变量。
- $\pi_{\mathrm{commit}}$：接近已验证目标候选的策略。
- $\pi_{\mathrm{explore}}$：前往最高分候选前沿的探索策略。
- $\pi_t$：时刻 t 最终执行的导航决策。

<div class="equation-explanation" markdown="1">

**直观理解**：系统先找出最像真实目标的物体，但不立即追踪；只有其累计证据越过阈值才切换到接近策略。这一硬门控将弱线索用于引导探索、将强证据用于行动承诺，从而减少误检导致的过早追逐。<br>
**原文位置**：式 (13)–(14)，Bias-conditioned Exploration and Target Commitment

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。SER-Nav 是 training-free 框架，原文没有给出可学习参数、损失函数或反向传播过程；其决策来自预定义类别关系、开放词汇感知、跨视角证据聚合、显式关系传播、前沿评分和阈值门控，而不是通过导航数据优化策略网络。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 多标签物体—角色竞争**

对物体簇 o 的每个候选标签 ℓ 计算 $ρ_o(ℓ)=m_o(ℓ)r_o(ℓ)$，其中 $m_o$ 表示跨视角累计支持，$r_o$ 表示聚合置信可靠性；选取 $ℓ_o^*=argmax_ℓρ_o(ℓ)$，再将归一化强度映射为 $h_o=r_o b_g(ℓ_o^*)$。

> 直观理解：该模块把“单帧标签”改成“经多次观察后胜出的身份”，从源头降低开放词汇检测的标签抖动和一次性误判。

**2. 双关系偏置传播**

激活通道汇总直接目标证据及由上下文物体生成的假设节点；抑制通道汇总视觉相似干扰证据和访问失败产生的负节点。二者都通过有限半径的距离衰减核投影到前沿决策空间，负证据还具有时间衰减和可覆盖性。

> 直观理解：单纯使用正向语义先验只能告诉智能体“哪里可能值得去”，该模块额外保存“哪里目前不应再相信”，从而避免持续追逐同一误检或反复访问无结果区域。

**3. 可靠性感知承诺门**

从当前物体集合中选择 $h_{o,t}^c$ 最大的候选，仅当其值不低于阈值 θ 时启用目标接近策略，否则继续执行偏置条件的前沿探索。

> 直观理解：它把“值得继续搜”与“已经确认到可以直接接近”分开，防止上下文线索或不稳定检测过早触发追踪与停止。

**训练与推理**

训练阶段：SER-Nav 本身不进行任务训练。默认关系集合由 DeepSeek 在评测前一次性生成，未依据验证集选择，也未人工修改；在线导航时不调用 LLM。推理阶段：智能体持续接收 RGB-D 等第一视角观测并更新定位与地图，开放词汇检测结果被投影到二维地图、跨视角聚类并竞争出物体主导标签；系统据此更新上下文假设、干扰证据和访问失败负节点，在局部图上传播激活与抑制，重排候选前沿。若最佳物体的承诺证据低于 θ，则前往最高分前沿继续观测；若达到 θ，则以 A* 局部规划逐步接近该物体，并在满足任务成功半径时执行 Stop。失败区域的抑制会随时间减弱，也可被后续一致证据推翻，因此系统能够从暂时的感知错误中恢复。

**复现信息**

基础前沿语义响应由 BLIP-2 衡量目标类别与检测物体区域的语义一致性；感知实验涉及 GroundingDINO（G-DINO）以及更强的 YOLO+G-DINO 组合。局部传播采用半径 R 内的指数距离衰减核，实验默认 R=2.3；承诺阈值默认 θ=0.45，这两个值在 HM3Dv2 验证集敏感性分析中取得最佳总体表现。目标承诺后使用 A* 局部规划器和逐步离散动作。真实机器人验证使用 Wheeltec R550、Astra Pro Plus RGB-D 相机和 Jetson Orin NX Super 16GB；开放词汇感知在配备 RTX A6000 的远程工作站运行，定位、建图与运动控制在机器人端运行，并通过局域网 ROS 2 通信。原文节选未明确给出物体聚类阈值、归一化函数 σ 的具体形式、负证据衰减系数及上下文假设节点生成细节，复现时需查阅补充材料 Section A.4。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HM3Dv1：Habitat 中的标准 ObjectNav 基准，包含20个场景、2,000个导航回合和6类目标。它用于检验方法在较少场景但较多回合设置下的成功率与路径效率。
- HM3Dv2：包含36个场景、1,000个导航回合和6类目标；正文还明确将其验证集用于消融实验。相较 HM3Dv1，其场景更多，是本文主要的组件分析与总体性能评估平台。
- MP3D：包含11个场景、2,195个导航回合和21类目标。其目标类别数量明显更多，用于检验 SER-Nav 面对更丰富目标语义时的泛化性与竞争力。原文节选未明确说明三个基准的具体数据划分细节。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**SR（Success Rate，成功率）**

衡量导航回合最终被 Habitat 判定为成功的比例；本文采用距离目标满足0.2米有效范围并执行 Stop 的成功判据。SR主要回答“是否找到并正确停止”，不体现成功路径是否绕远。 （越高越好，因为表示更多回合能够成功到达目标并正确停止。）

</div>
<div class="metric-item" markdown="1">

**SPL（Success weighted by Path Length，路径长度加权成功率）**

在成功与否的基础上进一步考虑实际路径相对有效路径的长度，用于同时评价任务完成率和路径效率。仅提高SR但产生大量绕行时，SPL未必同步提高。 （越高越好，因为高值通常意味着既能成功，又能以更高效的路径完成导航。）

</div>
<div class="metric-item" markdown="1">

**SoftSPL**

消融分析中的补充指标，用于在回合失败时仍度量智能体朝目标取得的部分进展，从而区分“完全走错”与“接近目标但未满足停止条件”等失败。具体数学定义位于补充材料，当前节选未提供。 （越高越好，因为表示即使未最终成功，智能体总体上也更接近目标或取得了更多有效进展。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### HM3Dv2 标准 ObjectNav 评测

<div class="result-value" markdown="1">

SER-Nav 获得74.5%的SR和36.8%的SPL；相较同为免训练、零样本且无在线LLM推理的VLFM，SR提高10.9个百分点、SPL提高4.3个百分点。由此可反推出该比较中VLFM约为63.6% SR和32.5% SPL，但这是根据文中差值计算，而非节选直接列出的表格行。

</div>

两项指标同时提升，说明 SER-Nav 不只是增加了到达目标的次数，也减少了部分无效搜索或绕行；这与抑制持续误导区域、强化可靠语义方向的设计目标一致。由于节选没有提供方差、置信区间或多次随机运行结果，不能仅据该差值判断统计显著性；同时，共享感知栈只能支持“执行决策机制带来收益”的解释，不能证明对所有感知模型均同样有效。

<div class="result-source" markdown="1">

来源：Main Results，Comparison with representative ObjectNav methods；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with VLFM, which is also training-free, zero-shot, and does not rely on online LLM reasoning, SER-Nav improves SR by 10.9 points and SPL by 4.3 points on HM3Dv2.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### HM3Dv1 标准 ObjectNav 评测

<div class="result-value" markdown="1">

SER-Nav 达到60.5%的SR和32.1%的SPL；作者称其优于近期零样本与基于LLM的方法，但当前节选没有提供这些方法的名称、数值及领先幅度。

</div>

HM3Dv1上的结果表明，该方法的收益并非只出现在主要消融所用的HM3Dv2上。SR与SPL之间仍存在较大数值间隔，意味着成功之外的路径效率仍有改进空间。由于缺失完整Table 1，无法核验它是否在HM3Dv1的每一项指标上都排名第一，也无法区分相对不同基线的具体优势。

<div class="result-source" markdown="1">

来源：Main Results，Comparison with representative ObjectNav methods；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

SER-Nav achieves the better performance on HM3Dv2 and HM3Dv1, obtaining 74.5 SR and 36.8 SPL on HM3Dv2, and 60.5 SR and 32.1 SPL on HM3Dv1.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MP3D 标准 ObjectNav 评测

<div class="result-value" markdown="1">

作者报告 SER-Nav 在不进行在线LLM推理的条件下取得有竞争力的表现，但所给节选未报告MP3D上的SR、SPL、排名或相对提升。

</div>

MP3D包含21类目标，因此该结论意在说明关系决策层可扩展到目标类别更丰富的环境。可是“competitive”只是作者的定性判断；在缺少完整数值和对应基线的情况下，不能据此断言 SER-Nav 在MP3D上最优，也无法量化其准确率—成本权衡。

<div class="result-source" markdown="1">

来源：Main Results，Comparison with representative ObjectNav methods；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On MP3D, SER-Nav achieves competitive performance without online LLM reasoning.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前节选缺少Table 1的完整方法行、MP3D数值以及不确定性统计，因而无法全面核验排名、统计显著性和不同基线间的公平性；“更优”或“有竞争力”主要是作者陈述。
- Table 2只有标题而无具体消融结果，无法量化关系激活、关系抑制和可靠性感知承诺门控的独立作用，也无法判断组件之间是否存在互补或冗余。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- VLFM：与 SER-Nav 同为免训练、零样本且不依赖在线 LLM 推理的方法，因此可较直接地比较两者在类似部署约束下利用语义线索进行搜索的能力。节选仅给出了它在 HM3Dv2 上与 SER-Nav 的明确数值差异。
- 其他代表性 ObjectNav 方法：Table 1 据称还比较了近期零样本方法和基于 LLM 的方法，但所给节选没有列出其名称、配置或完整成绩，因而无法逐项分析。

**实验想回答的问题**

- 在保持相同感知—建图—规划栈的条件下，SER-Nav 的关系激活、关系抑制与可靠性感知决策机制，能否在噪声开放词汇感知下提高零样本目标导航的成功率和路径效率？
- SER-Nav 能否在不同场景规模与目标类别数量的标准 ObjectNav 基准上保持稳定收益，并在不使用在线大语言模型推理的情况下兼顾导航性能、鲁棒性与推理成本？

**实验实现**

智能体在 Habitat 模拟器中使用离散动作：前进0.25米、左转30度、右转30度和停止；每回合最多500步，感知范围为0至5米，并依据 Habitat 的0.2米有效 Stop 标准判定成功。为隔离执行决策层的作用，所有变体共享同一套感知—建图—规划栈，使用 YOLO、GroundingDINO、MobileSAM 和 BLIP-2，因此变体间差异原则上主要反映语义证据调节与决策机制，而不是感知模型更换。实验在单张 NVIDIA RTX A6000 GPU 上运行，约使用8GB显存；SR、SPL及消融中的SoftSPL均以百分比报告。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Figure 4与Figure 5比较了噪声开放词汇感知下的导航行为。作者观察到，基线可能被高置信度误检持续吸引，或因不可靠观测漏掉目标；SER-Nav则利用抑制证据降低假阳性区域的优先级，并通过上下文激活和动作级验证恢复较弱的目标证据，因而产生更可靠、冗余更少的轨迹。该案例直观展示了机制如何改变搜索方向，但没有给出案例数量、筛选原则或总体发生频率，不能单独证明普遍优势。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出通过动态调节语义证据可靠性来改善零样本目标导航探索与决策的具身导航框架。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`dc2f4accd514403d3e3153c51597983990b75b3841c5edb35a23641111d9669f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
