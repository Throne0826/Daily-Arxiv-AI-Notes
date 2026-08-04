---
title: "[论文解读] Where Reasoning Diverges: Localized Multi-Agent Debate"
description: "[arXiv 2608.01463][Multi-Agent] 本文提出局部化多智能体辩论（LMAD），将协调对象从整段推理或最终答案缩小为多条推理链中最早出现分歧的局部步骤，并在验证后将修复结果写入共享状态。"
arxiv_id: "2608.01463"
announcement_date: "2026-08-04"
primary_category: "multi_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:57:10.292789+00:00"
source_sha256: "1c6aa253ee528cb783a3337ad9ac9425c728d7bdf3c3bb358dc3c0b3d267eaa7"
tags:
  - "Multi-Agent"
  - "LLM Reasoning"
  - "多智能体辩论"
  - "局部冲突定位"
  - "多跳问答"
  - "类型化推理节点"
  - "共享承诺状态"
  - "推理时协议"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">Multi-Agent · arXiv 2608.01463</p>

# Where Reasoning Diverges: Localized Multi-Agent Debate

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Weijun Gao, Xiang Ding, Tiancheng Xing, Haoyang Liu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The Chinese University of Hong Kong；Nagoya University；Institute of Science Tokyo；University of Illinois Urbana-Champaign</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01463v1) · [PDF 下载](https://arxiv.org/pdf/2608.01463v1) · **关键词** 多智能体辩论, 局部冲突定位, 多跳问答, 类型化推理节点, 共享承诺状态, 推理时协议<br>


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

本文提出局部化多智能体辩论（LMAD），将协调对象从整段推理或最终答案缩小为多条推理链中最早出现分歧的局部步骤，并在验证后将修复结果写入共享状态。

**不用术语来说**：多个语言模型共同解题时，往往只在某个中间判断上发生分歧，但传统辩论会让它们反复交换和重审整段解题过程。这既混入大量已经达成一致的内容，也可能破坏原本正确的步骤；在多跳问答中，一个早期错误还会沿后续推理持续传播，因此仅比较最终答案无法找到真正需要修正的位置。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将多智能体辩论重新表述为“冲突局部化的状态修复”：每轮优先识别并处理跨智能体最早的未解决分歧，同时保留已经确认的共享推理状态。
- 作者提出一套推理时协议，将类型化节点抽取、跨链对齐与定位、局部辩论、受约束提交和提前停止组合起来，使智能体只讨论导致冲突的短片段，并在关系与证据检查通过后继续推理。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于基于大语言模型的多智能体辩论（Multi-Agent Debate, MAD）研究。其基本设置是：多个语言模型实例先独立求解同一问题，再通过交换方案、相互批评和修订来提高最终答案的可靠性。论文关注多跳问答，即答案需要由多个依次依赖的中间事实或推理步骤得到；在这种任务中，某一步选择了错误实体、关系或证据，错误通常会沿后续步骤传播。传统 MAD 往往交换完整答案或整条推理轨迹，但智能体之间真正决定答案差异的部分可能只是最早出现分歧的一个中间步骤，因此本文把协调对象从“完整推理”缩小为“最早冲突及其局部前导片段”。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多智能体辩论（MAD）**

多个语言模型智能体对同一问题分别提出解答，并通过若干轮共享、批评和修订形成最终答案。这里的“智能体”通常可以是同一模型的多个独立实例，也可以来自不同模型。

</div>
<div class="concept-item" markdown="1">

**多跳问答**

不能依靠单一事实直接作答，而要串联多个事实或关系才能得到答案的问答任务。由于后一步依赖前一步，较早的局部错误可能改变整条后续推理。

</div>
<div class="concept-item" markdown="1">

**类型化节点与推理轨迹**

推理轨迹是智能体从问题走向答案的一系列中间陈述；LMAD 将自由文本轨迹转换为保持原有顺序的类型化节点，以便比较不同智能体在对应步骤上的实体、关系或结论。该结构化表示用于定位冲突，但不改写智能体原先给出的答案。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是问题 $q$ 以及任务可用的上下文或证据，系统维护由此前已验证结论构成的共享承诺状态 $P$。多个智能体 $A_i$ 在 $q$、上下文与当前 $P$ 的条件下并行生成自由形式的答案和推理轨迹，随后这些轨迹被映射为有序类型化节点链；当各智能体答案不一致时，系统对齐节点序列并定位最早的跨智能体冲突，只让各智能体交换截至该冲突位置的局部片段 $S_i$。局部辩论产生候选修复 $chat{Z}$，控制器检查它是否符合问题所要求的关系并得到现有证据支持；通过检查后，将其追加到 $P$，智能体再从更新后的状态继续推理。该过程在答案一致时提前停止，否则继续处理下一个最早冲突，最终输出一致答案或协议所确定的最终答案。该设置是纯推理时协议：原文所述操作发生在推理阶段，未声称需要重新训练底层模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$q$**

待回答的问题；智能体推理时还可接收相应上下文或证据。

</div>
<div class="notation-item" markdown="1">

**$A_i$**

第 $i$ 个语言模型智能体。

</div>
<div class="notation-item" markdown="1">

**$P$**

共享承诺状态，保存已经通过关系与证据检查、后续步骤不应随意重新打开的中间结论。

</div>
<div class="notation-item" markdown="1">

**$S_i$**

第 $i$ 个智能体通向当前最早冲突节点的局部推理片段，也是该轮辩论实际交换的内容。

</div>

</div>

**直接相关的工作**

- **Du et al. (2024) 的经典多智能体辩论协议**: 该协议通过多轮交换完整解答并聚合答案来改善推理与事实性，是 LMAD 所比较的常规全轨迹交互范式。LMAD 不主要改变智能体角色或最终聚合方式，而是把通信与修订范围限制在最早冲突对应的局部推理片段。
- **ReConcile（Chen et al., 2024）**: ReConcile 使用置信度加权共识来整合不同模型的回答，重点在答案层面的共识形成。LMAD 处理的是更细粒度的问题：先识别推理链从何处开始分叉，再对导致该分叉的局部内容进行修复。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

多跳问答要求模型连续完成若干相互依赖的推理步骤，前一步确定的事实、实体或关系会约束下一步。当多个智能体在较晚的一跳选择了不同实体或关系时，首次分歧会传导至后续步骤并形成不同答案。实际需要因此不是笼统地增加辩论轮次，而是及时找出最早导致答案分叉的中间判断并进行针对性修复。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **答案级聚合或投票**：各智能体独立生成答案，系统在最终答案层面比较结果，并通过投票或类似共识机制作出决定；这种方法把完整答案视为协调单位。
- **完整推理轨迹辩论**：智能体交换整段答案或推理依据，彼此检查并修改完整解题过程，直到形成共识或满足终止条件；已有协议主要在如何激发分歧和何时停止方面有所不同。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 答案级投票只显示智能体最终结论不同，无法揭示分歧最先出现在哪个中间步骤；因此系统难以区分根因与由根因传播出的后续差异，也无法精确修复决定性错误。
- 完整轨迹辩论的处理粒度过粗：即使真正冲突只涉及少数中间判断，智能体仍需重新审查包含大量正确共识的长推理链。这会引入无关内容，并可能重新打开已经接受的事实，使协调成本和错误风险同时增加。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种面向多跳推理的细粒度协调机制：它既要把自由形式的多条推理轨迹转换为可比较的有序结构，定位最早的跨智能体冲突，又要把讨论限制在产生该冲突的局部片段，并在不推翻既有共识的前提下将修复结果可靠地纳入后续推理。

</div>
<div markdown="1"><span>核心问题</span>

能否在不重新讨论整条推理链的情况下，通过定位多智能体推理中最早的分歧、仅辩论相关局部片段，并对修复结论进行关系与证据检查，持续更新共享状态，从而更有效地解决多跳问答中的分歧？

</div>
<div markdown="1"><span>作者直觉</span>

一条多跳推理链可看作连续依赖的步骤：如果几位解题者前几步一致，只在某一步开始分叉，那么后面的大量差异通常只是该分叉的结果。先修复最早冲突，相当于校正后续推理共同依赖的起点；将已确认步骤保存在共享状态中，则像把正确的阶段性结论锁定下来，使下一轮只处理尚未解决的问题。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

LMAD（Localized Multi-Agent Debate，局部化多智能体辩论）是一种纯推理阶段协议。给定问题 $q$、可选证据上下文 $x$ 和共享同一基础语言模型的 $K$ 个智能体，控制器从空的已提交状态 $P^{(0)}$ 开始；每轮让各智能体在当前状态条件下独立生成自由形式的推理轨迹与答案，再将轨迹抽取为有顺序的类型化节点。若规范化后的答案一致，系统直接停止；否则，定位器从各条节点链的起点向后扫描，找出最早的跨智能体语义冲突，并为每个智能体返回对应的见证节点索引。系统只围绕截至该索引的局部片段交换意见，解析器据此提出替换节点，提交守卫检查这些节点是否得到上下文中逐字引文的支持；通过后将其追加到共享状态，并让所有智能体基于新状态重新推理，未通过则保留旧状态并从当前答案中选择最终结果。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 条件化生成与结构化抽取

第 $\ell$ 轮中，智能体 $i$ 采样自由形式推理 $r_i^{(\ell)}$ 和答案 $a_i^{(\ell)}$；零温度抽取器 $E$ 再把推理映射为有序节点序列 $Z_i^{(\ell)}$，同时单独保留原答案，避免结构化过程改写答案。轻量质量检查识别空节点、重复节点、过长节点和格式错误节点。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、可选证据上下文 $x$、当前已提交状态 $P^{(\ell)}$，以及共享基础模型但采用不同采样温度的 $K$ 个智能体。<br>
**输出**：每个智能体的结构化状态 $(Z_i^{(\ell)},a_i^{(\ell)})$，其中节点表示简洁的中间主张。

</div>

**直观理解**：智能体先按自然方式写完整解题过程，再由稳定的抽取器把它整理成可编号的主张清单。答案被单独保存，因此“整理笔记”不会悄悄改变最终作答。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 一致性检查与最早冲突定位

控制器先比较规范化答案；若答案不一致，定位器 $L$ 从各节点链开头扫描，返回共同冲突描述 $\delta^{(\ell)}$，以及每条轨迹中首次表达或引起该冲突的一基索引 $t_i^{(\ell)}$。它不预测该冲突对最终答案的重要程度，也不要求不同轨迹中的索引数值相同。

<div class="method-step__io" markdown="1">

**输入**：全部智能体状态集合 $\mathcal{U}^{(\ell)}=\{(Z_i^{(\ell)},a_i^{(\ell)})\}_{i=1}^{K}$，以及 $q$、$x$ 和 $P^{(\ell)}$。<br>
**输出**：语义冲突 $\delta^{(\ell)}$、各智能体的见证索引 $t_i^{(\ell)}$，以及可审计的局部片段 $S_i^{(\ell)}=Z_i^{(\ell)}[1:t_i^{(\ell)}]$。

</div>

**直观理解**：系统像逐行对照多份解题草稿一样，停在第一处实质分歧，并记录每份草稿中对应的行号。显式索引能显示系统究竟截取了哪里，降低模糊语义匹配误选较晚分歧的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 局部辩论与修复提议

各智能体只针对已定位的局部冲突交换意见，而不是互传并重审完整推理轨迹；局部交换结束后，解析器提出由一个或多个替换节点组成的修复 $\widehat{Z}^{(\ell)}$。

<div class="method-step__io" markdown="1">

**输入**：问题与上下文 $(q,x)$、共享状态 $P^{(\ell)}$、智能体自身的局部片段 $S_i^{(\ell)}$，以及竞争主张的简短描述。<br>
**输出**：面向当前最早冲突的候选修复节点 $\widehat{Z}^{(\ell)}$。

</div>

**直观理解**：这相当于只开会讨论证明中第一处有争议的步骤，而不是让每个人重新朗读整份解答。讨论结果被整理成可加入公共笔记的新主张。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 守卫提交、重生成与终止

提交守卫 $g_{\mathrm{commit}}$ 要求修复得到所提供上下文中逐字引文的支持；通过时将修复追加为 $P^{(\ell+1)}$，随后所有智能体基于新状态重新生成完整推理，未通过时状态不变并从本轮答案中选取最终结果。流程在规范化答案一致、提交失败或达到最大迭代次数时终止；答案类型感知的粒度守卫仅在抽取节点中已出现兼容的更长实体时允许扩展答案。

<div class="method-step__io" markdown="1">

**输入**：候选修复 $\widehat{Z}^{(\ell)}$、问题 $q$、证据上下文 $x$ 和当前状态 $P^{(\ell)}$。<br>
**输出**：更新后的已提交状态和下一轮输入，或终止时选出的最终答案。

</div>

**直观理解**：公共笔记只接受能从材料中直接找到文字依据的修复；一旦接受，后续推理把它当作已定前提，不再重新争论。这里的“已提交”只表示通过协议检查，并不等于已经由真实标签证明正确。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 带索引的冲突定位

$$
\left(\delta^{(\ell)},t_{1}^{(\ell)},\ldots,t_{K}^{(\ell)}\right)=L\!\left(q,x,P^{(\ell)},\mathcal{U}^{(\ell)}\right)
$$

**符号说明**

- $\ell$：当前迭代轮次。
- $L$：按节点链顺序寻找最早跨智能体不一致的定位器。
- $q$：待回答的问题。
- $x$：可选的证据上下文。
- $P^{(\ell)}$：第 $\ell$ 轮开始时已经通过协议守卫的共享状态。
- $\mathcal{U}^{(\ell)}$：当前轮全部智能体的节点序列与答案集合，即 \{($Z_i^{(\ell)},a_i^{(\ell)})\}_{i=1}^{K}$。
- $\delta^{(\ell)}$：定位器返回的共同语义冲突描述。
- $t_i^{(\ell)}$：智能体 i 的一基见证索引，指向其轨迹中首次表达或导致当前冲突的节点。
- $K$：参与协议的同质智能体数量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把“发现分歧”明确化为一个可审计映射：输入问题、证据、已接受前提和所有当前解答，输出统一的冲突说明以及每份解答中的具体位置。它是局部化的关键，因为后续辩论范围由这些索引确定，而不是依赖一个不可检查的“相关片段”判断。<br>
**原文位置**：第 3.2 节，公式 (3)

</div>

</div>

<div class="equation-block" markdown="1">

#### 守卫控制的共享状态更新

$$
P^{(\ell+1)}=\begin{cases}P^{(\ell)}\mathbin{\|}\widehat{Z}^{(\ell)},&\text{if }G^{(\ell)},\\ P^{(\ell)},&\text{otherwise}.\end{cases}
$$

**符号说明**

- $P^{(\ell+1)}$：提交决策完成后的下一轮共享状态。
- $P^{(\ell)}$：提交决策前的当前共享状态。
- $\widehat{Z}^{(\ell)}$：解析器根据本轮局部辩论提出的一个或多个修复节点。
- $G^{(\ell)}$：本轮提交守卫的布尔决策，其中 $G^{(\ell)}=g_{\mathrm{commit}}(q,x,\widehat{Z}^{(\ell)})$。
- $\mathbin{\|}$：将新修复节点追加到已有共享状态的拼接操作。
- $g_{\mathrm{commit}}$：检查修复是否得到所提供上下文中逐字引文支持的提交守卫。

<div class="equation-explanation" markdown="1">

**直观理解**：只有证据检查通过，候选修复才会进入公共状态；否则系统完全保留原状态。该更新使已接纳内容单调累积，并让下一轮智能体从共同前提重新推理，从而可以继续处理更晚出现的冲突。<br>
**原文位置**：第 3.3 节，公式 (6)；守卫定义见公式 (5)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。LMAD是推理时协议，原文所给方法章节没有引入参数训练、损失函数或梯度优化目标；节点抽取、冲突定位、局部辩论、解析和提交守卫均用于组织现有语言模型在推理阶段的交互。因而公式描述的是采样、定位和状态转移，而不是需要最小化的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 类型化推理节点抽取器**

抽取器 $E$ 以零温度运行，将自由形式推理 $r_i^{(\ell)}$ 转成有序节点序列 $Z_i^{(\ell)}=(z_{it}^{(\ell)})_{t=1}^{T_i^{(\ell)}}$；节点记录简洁主张，原答案 $a_i^{(\ell)}$ 与抽取过程分离。该设计保留自然生成能力，同时提供可索引、可检查的中间表示。

> 直观理解：直接要求较小模型严格按复杂结构输出可能降低推理质量，因此作者让模型先正常解题，再做结构化整理。节点的主要价值不是改变推理内容，而是给每个中间主张一个稳定位置，供后续定位使用。

**2. 带索引的最早冲突定位器**

定位器 $L$ 联合读取 $q$、$x$、$P^{(\ell)}$ 和所有智能体状态，输出冲突描述 $\delta^{(\ell)}$ 与每个智能体的见证索引 $t_i^{(\ell)}$。它按推理顺序寻找第一处跨智能体不一致，由于各智能体每轮都以 $P^{(\ell)}$ 为条件重新生成，辩论片段取从当前轨迹起点到冲突节点的前缀即可。

> 直观理解：同一分歧在不同草稿里可能出现在不同位置，因此每条轨迹需要自己的索引。选择最早冲突是因果上的保守策略：先修正可能导致后续分叉的上游步骤，而不是只修补较晚出现的答案差异。

**3. 解析器、提交守卫与单调状态**

解析器将局部辩论归纳为修复节点 $\widehat{Z}^{(\ell)}$，提交守卫 $g_{\mathrm{commit}}$ 依据上下文逐字引文决定是否接纳；接纳后使用拼接操作将修复追加到 $P^{(\ell)}$。已提交节点在后续轮次不会被重新打开，因此状态以单调方式积累协议已接受的主张，但守卫不承担冲突定位，也不提供真实正确性证明。

> 直观理解：该模块把“大家讨论出了一个说法”与“这个说法可以进入公共前提”分开。证据守卫限制无依据修复，单调状态则避免每轮从头争论，不过其可靠性仍取决于上下文是否充分以及逐字引文能否真正支持该主张。

**训练与推理**

训练过程：原文未报告为LMAD额外训练模型，因而不能据此推断存在微调或专门监督数据。推理过程：初始化 $P^{(0)}=\varnothing$；在第 $\ell$ 轮，各智能体依据 $(q,x,P^{(\ell)})$ 生成新的完整推理与答案，抽取器将推理转成节点序列。若规范化答案一致则返回结果；否则定位最早冲突并截取各自局部片段，执行一次局部辩论，由解析器提出修复并交给提交守卫。修复通过时追加到共享状态并进入下一轮，失败时停止并从当前智能体答案中选取最终结果；达到最大轮数时同样终止。由于每轮轨迹均基于最新共享状态重新生成，局部修复能够影响后续整条推理，而无需把旧轨迹的后缀直接拼接回来。

**复现信息**

参考配置采用同一基础语言模型构成的同质智能体，并用不同采样温度制造候选推理差异；结构抽取器使用零温度，以降低节点划分的随机性。每次迭代只进行一轮局部辩论，最多进行十次迭代。复现时还需实现答案规范化、节点质量检查、逐字引文支持检查和答案类型感知的粒度守卫；其中后者只允许把答案扩展为抽取节点中已经出现的兼容长实体。所给章节未明确报告智能体数量 $K$、各采样温度、具体提示词、解析器与定位器使用的模型、最终答案选择规则的细节或逐字引文匹配的工程实现，因此这些项目不能从当前材料中可靠补全。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HotpotQA：多跳问答基准，用于检验模型能否组合分散在多个证据来源中的信息。原文节选未报告样本规模、具体评测划分及是否向模型提供检索上下文。
- 2WikiMultiHopQA：基于多个维基百科页面进行组合推理的多跳问答基准，用于测试跨证据链推理。原文节选未报告样本规模和具体评测划分。
- MuSiQue：强调组合式、多步骤问题构造的多跳问答基准，可用于检验方法面对较复杂推理链时的迁移能力。原文节选还列出 StrategyQA，但受输出数量限制未单列；各数据集的样本规模与评测划分均未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**宏平均评判器准确率（macro-averaged judge accuracy）**

先在各评测数据集上由评判器判断答案是否正确，再对数据集结果作等权平均，从而避免样本量较大的数据集完全主导总体结论。节选未说明评判器的具体提示、判分规则及其与标准答案的一致性验证。 （越高越好，因为它表示跨数据集平均而言，被评判为正确的回答比例更高。）

</div>
<div class="metric-item" markdown="1">

**骨干模型—数据集组合上的胜、平、负计数**

逐一比较 LMAD 与最强基线在不同骨干模型和数据集组合上的表现，用于衡量改进是否广泛存在，而非仅由少数设置拉高平均值。 （胜出的组合越多、落后的组合越少越好，因为这体现方法跨模型与跨数据集的一致性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 十个骨干模型上的四数据集宏平均评判器准确率

<div class="result-value" markdown="1">

作者报告，使用单一固定配置的 LMAD 在全部十个骨干模型上都取得最高的宏平均评判器准确率。

</div>

这说明 LMAD 的优势并非依赖针对某个骨干单独调参，并支持其跨模型家族和参数规模迁移的主张。不过，节选没有给出各模型的具体分数、方差或显著性检验，因此该结果不能单独证明提升具有统计显著性，也不能说明额外计算成本是否合理。

<div class="result-source" markdown="1">

来源：表 1；第 4 节 Main results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 1 shows that a single fixed LMAD configuration achieves the highest macro-averaged judge accuracy for all ten backbones, outperforming the strongest conventional baseline by up to 7.20 percentage points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### LMAD 与最强常规基线的最大宏平均差距

<div class="result-value" markdown="1">

作者报告，LMAD 相对最强常规基线的最大提升达到 7.20 个百分点。

</div>

该数值展示了 LMAD 在最佳情形下可能带来的收益幅度，但“最高提升”不是平均提升，也不代表所有骨干模型都获得同等收益。由于节选未提供产生该差距的具体骨干模型、绝对准确率和不确定性范围，无法判断其实际难度、相对增幅及稳定性。

<div class="result-source" markdown="1">

来源：表 1；第 4节 Main results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 1 shows that a single fixed LMAD configuration achieves the highest macro-averaged judge accuracy for all ten backbones, outperforming the strongest conventional baseline by up to 7.20 percentage points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 全部骨干模型—数据集组合上的逐项比较

<div class="result-value" markdown="1">

在 40 个骨干模型—数据集组合中，LMAD 相对最强基线取得 36 胜、1 平、3 负。

</div>

逐项胜负分布表明改进覆盖了大多数模型与数据集组合，而不只是由少数高分设置造成。然而，胜负计数忽略了每次差距的大小：微小且可能不显著的领先也会被计作一次胜利，同时三个退化设置的模型、数据集和原因在节选中均未披露。

<div class="result-source" markdown="1">

来源：表 1 汇总结论；第 4 节 Main results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across the 40 backbone–dataset combinations, LMAD improves over the strongest baseline in 36 cases, ties in one, and underperforms in three.

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

- 最强常规基线：主结果以每个骨干模型上的最佳传统方法作为直接参照，用于判断 LMAD 是否优于非局部化的常规多智能体方案；但所给节选没有提供该基线的名称、提示模板、轮数、计算预算或完整推理轨迹交换方式，因此无法核验比较是否严格等预算。

**实验想回答的问题**

- 在保持同一套 LMAD 配置不变的条件下，局部化辩论能否在不同模型家族、参数规模和多跳问答数据集上稳定提高回答正确性？
- 与交换完整推理轨迹的常规多智能体辩论基线相比，LMAD 将讨论限制在最早冲突对应的局部片段，是否能获得更高的宏平均评判器准确率？

**实验实现**

实验覆盖四个问答基准 HotpotQA、2WikiMultiHopQA、MuSiQue 和 StrategyQA，并使用来自 Qwen2.5、Qwen3、Qwen3.5 与 Gemma3 四个模型家族的十个开放权重骨干模型。所有多智能体方法均采用同构智能体，即各智能体使用同一骨干，仅通过采样温度 $0.1$、$0.5$、$0.9$ 形成三种求解行为。对每个骨干，答案生成以及节点抽取、冲突定位、冲突解决等辅助模块都使用同一模型，降低了外部模型能力差异造成的混淆。辅助模块采用温度 $0$ 的确定性解码；控制器每次迭代进行一轮局部辩论，最多迭代十次。推理通过 vLLM 运行，硬件为四张 NVIDIA A100 80GB GPU。节选未报告每个数据集的样本数、评测划分、重复运行次数、随机种子、置信区间、显著性检验、评判器实现，以及 LMAD 与基线的 token 或推理时延预算。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a multi-agent debate protocol that localizes conflicts within reasoning traces to improve multi-hop question answering.; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`1c6aa253ee528cb783a3337ad9ac9425c728d7bdf3c3bb358dc3c0b3d267eaa7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
