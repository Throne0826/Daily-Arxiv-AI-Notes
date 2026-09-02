---
title: "[论文解读] Escaping Redundant Reasoning: Structure-Aware Search for Inference-Time LLMs"
description: "[arXiv 2609.00738][LLM Reasoning] 本文将推理时搜索反复探索同类思路的现象形式化为“推理盆地坍缩”，并提出无需训练的 BASIN 与质量感知版本 QA-BASIN，通过识别并抑制对已过度访问策略的重复选择，在固定推理预算下改善探索与利用的平衡。"
arxiv_id: "2609.00738"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:43:38.991819+00:00"
source_sha256: "360aa3b53cf88eea5116f69480aaa87f92208bdc436c4695f15c6321c8af7fe5"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "推理时搜索"
  - "Tree of Thoughts"
  - "推理盆地"
  - "推理盆地坍缩"
  - "结构感知搜索"
  - "策略级多样性"
  - "冗余差距"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.00738</p>

# Escaping Redundant Reasoning: Structure-Aware Search for Inference-Time LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Lu Cheng</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Department of Computer Science；Affiliation: University of Illinois Chicago</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00738v1) · [PDF 下载](https://arxiv.org/pdf/2609.00738v1) · **关键词** 大语言模型, 推理时搜索, Tree of Thoughts, 推理盆地, 推理盆地坍缩, 结构感知搜索, 策略级多样性, 冗余差距<br>
**代码**: [https://github.com/GitHubLuCheng/basin](https://github.com/GitHubLuCheng/basin)

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

本文将推理时搜索反复探索同类思路的现象形式化为“推理盆地坍缩”，并提出无需训练的 BASIN 与质量感知版本 QA-BASIN，通过识别并抑制对已过度访问策略的重复选择，在固定推理预算下改善探索与利用的平衡。

**不用术语来说**：让大语言模型生成更多推理过程，并不等于它真正尝试了更多解题办法：许多候选过程可能只是用不同措辞重复同一条路线。如果搜索预算大量消耗在这种重复上，模型就可能一直围绕一个错误思路打转，而没有机会尝试真正不同的方案；但若一味追求差异，又可能放弃已经找到的优质路线。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“推理盆地”概念，把采用同一底层策略的推理状态归为一个等价类，并据此识别“推理盆地坍缩”：搜索表面上生成了许多状态，实际却集中于少数结构或语义相近的策略；同时引入冗余差距 $\Delta$，用于刻画正确预测与错误预测之间的搜索集中程度差异。
- 作者提出训练无关的 BASIN，在候选选择阶段依据盆地历史访问次数施加对数惩罚，将预算重新分配给较少探索的策略；进一步提出 QA-BASIN，对高质量盆地减弱惩罚，以缓解无条件多样化导致的过度探索。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型的推理时搜索领域：模型在测试阶段生成多个包含中间推理步骤的候选轨迹，并通过搜索或评分选择最终答案，以额外计算量换取更好的复杂推理能力。论文关注一个比“生成多少条轨迹”更细的问题：这些轨迹是否真正采用了不同策略。作者指出，Tree of Thoughts（ToT）等常规方法通常依据候选状态的质量分数进行扩展，却不识别多个状态是否属于同一策略，因而可能反复消耗预算于结构或语义等价的路径；本文将这种搜索集中于少数策略的现象称为“推理盆地坍缩”。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**推理时搜索（inference-time search）**

模型参数保持不变，在回答问题时生成、评估并扩展多条候选推理路径。其计算预算通常限制候选生成、状态扩展或模型调用的总量，因此关键问题是如何把固定预算分配给更有价值的路径。

</div>
<div class="concept-item" markdown="1">

**Tree of Thoughts（ToT）**

ToT把推理过程表示为由中间状态构成的搜索树：节点是部分解答或当前思路，边表示继续推理的一步操作，搜索程序反复生成并选择候选节点。与只生成一条思维链不同，它允许比较、保留和扩展多条路径。

</div>
<div class="concept-item" markdown="1">

**推理盆地（reasoning basin）与盆地坍缩**

推理盆地是采用同一底层策略的一组等价推理状态；有明确任务结构时可按符号或结构特征划分，开放式任务中则可抽取中心假设并借助自然语言推断判断语义等价。若大量搜索访问集中在少数盆地，即使表面措辞不同也没有探索新策略，便形成推理盆地坍缩。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个需要多步推理的问题、能够从当前状态生成后继状态的LLM、候选质量评分机制以及固定推理预算，搜索程序需要在每轮从候选状态中选择一部分继续扩展，最终输出答案或完整推理轨迹。论文假设候选状态可依据任务相关结构或中心假设映射到某个推理盆地；核心问题是在不训练模型、不修改底层生成器且不增加预算的条件下，利用盆地归属与历史访问情况减少对同一策略的重复扩展，同时避免为了多样性而放弃已经发现的高质量策略。作者还用有效盆地数 $N_{\mathrm{eff}}$ 描述访问在不同策略间的实际分散程度，并以冗余差距 $\Delta$ 比较正确与错误预测对应搜索的集中程度。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N_{\mathrm{eff}}$**

按各盆地访问频率加权得到的有效盆地数量，用于衡量搜索实际覆盖了多少种不同推理策略；它不同于简单统计出现过的盆地总数。

</div>
<div class="notation-item" markdown="1">

**$n_{\mathrm{basins}}$**

搜索过程中被识别出的盆地总数；论文图示以 $N_{\mathrm{eff}}<n_{\mathrm{basins}}$ 表示访问频率集中于部分已探索盆地。

</div>
<div class="notation-item" markdown="1">

**$\Delta$**

冗余差距（redundancy gap），衡量正确预测与错误预测对应搜索的集中程度之差；正值表示两类结果呈现不同的冗余结构。

</div>

</div>

**直接相关的工作**

- **Tree of Thoughts（Yao et al., 2023）**: ToT将LLM推理建模为中间状态上的树搜索，是本文最直接的基础搜索框架。本文认为其常规候选选择主要关注状态质量而缺少策略级结构意识，因此可能反复扩展属于同一盆地的候选；BASIN针对选择环节加入盆地访问约束，而非替换底层生成器。
- **Diverse Beam Search（Vijayakumar et al., 2016）**: 该方法通过候选组之间的多样性惩罚减少近似重复，是与BASIN思路接近的多样化搜索方法。区别在于BASIN并非一般性地最大化文本差异，而是依据符号结构或语义等价关系形成策略级盆地，并惩罚对同一底层策略的重复访问。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推理时计算扩展通常依靠生成并筛选多条候选轨迹来提高复杂任务的成功率，但固定预算下真正稀缺的是“不同策略的尝试次数”，而不是文本轨迹总数。论文在 MuSR 的示例分析中指出，标准 Tree of Thoughts 搜索平均只有 38% 的预算到达真正新的推理策略；因此，新增计算可能主要制造同类轨迹，错误路线也可能持续吸收预算，使搜索成本增加却未带来相应的策略覆盖。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **多轨迹生成与选择或聚合**：通过思维链采样、自一致性等方式生成多条完整推理轨迹，再依据投票、评分或其他聚合规则确定答案。其基本假设是增加样本数量能够提高覆盖正确推理的概率，但通常不显式判断多条轨迹是否采用了同一底层策略。
- **Tree of Thoughts（ToT）等状态搜索**：把中间推理步骤表示为搜索状态，反复扩展候选并依据质量评分选择后续节点。它比只生成完整答案更有组织性，但标准选择规则主要关注候选自身的分数，不记录同类策略已经被访问多少次。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有搜索通常对推理结构或语义等价关系不敏感，因而可能把措辞不同但策略相同的状态误当作独立探索。其后果是有效盆地数 $N_{\mathrm{eff}}$ 显著低于已生成状态或已识别盆地数量，固定推理预算被重复路线消耗。
- 单纯的搜索集中并不能代表答案可靠：正确搜索可能集中在有效策略上，错误搜索也可能集中在错误策略上。反过来，无条件鼓励多样性同样存在风险，因为搜索已经进入高质量区域后，持续排斥该区域会把预算转向较弱候选。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前方法缺少一种可直接嵌入现有推理搜索、无需重新训练生成模型的选择原则：它既要按任务结构或语义识别“真正相同的策略”，又要利用访问历史减少有害重复，同时还要根据候选质量避免机械地追求多样性。相应地，也缺少能够区分正确与错误搜索中冗余模式的诊断量，而不仅是统计总体多样性。

</div>
<div markdown="1"><span>核心问题</span>

在生成器、推理预算和基本搜索框架保持不变时，能否仅修改候选选择机制，依据推理盆地的访问频率与质量，在不同策略之间更合理地分配计算，从而提高复杂推理的准确性与跨任务稳健性？

</div>
<div markdown="1"><span>作者直觉</span>

可把搜索想象成在若干“解题思路区域”之间移动：若某一区域已被反复访问，再从中选择相似候选所带来的新信息通常较少，因此应施加随访问次数增长的惩罚，促使搜索尝试尚未充分探索的区域。不过，访问频繁也可能是因为该区域确实优质，所以 QA-BASIN 会对高质量盆地减弱惩罚。这样既避免在错误思路中反复打转，也不轻易丢弃已经显现价值的路线。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

BASIN 是对推理时搜索“候选选择”环节的结构感知改造，不训练或微调语言模型，也不改变候选生成方式。给定搜索产生的推理状态，方法先用任务相关的盆地映射 $\mathcal{B}$ 将采用同一核心策略的状态归为一个“推理盆地”，再统计各盆地此前进入活跃搜索集的次数。候选的原始分数 $f(s)$ 随所属盆地的访问次数受到对数惩罚，搜索据此重新排序并保留候选；若有可靠的质量信号，QA-BASIN 还用盆地质量 $q_z$ 减弱高质量盆地的惩罚，以避免为了多样性而放弃有希望的策略。最终输出仍是底层 ToT、MCTS 或 GoT 搜索程序产生的答案，BASIN 只重新分配固定推理预算。

技术上，盆地不是按字面相似度简单聚类，而是近似表示“继续搜索后会沿同一种解题策略发展”的等价类。Game of 24 等结构明确的任务使用运算序列与剩余数值构成确定性键；MuSR 等开放式任务则先抽取一句话主假设，再要求两个状态答案一致、假设具有足够高的自然语言推断蕴含概率且矛盾概率足够低。直观地说，普通搜索可能让多个措辞不同但思路相同的候选同时占满搜索束；BASIN 把它们视为对同一条路线的重复投资，并把部分预算转给尚未充分尝试的路线，而 QA-BASIN 会继续保护已经显示出较高质量的路线。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 生成并基础评分候选状态

按照原有 ToT、GoT 或 MCTS 规则扩展当前状态，得到候选延续 $s$，并由底层搜索程序计算基础分数 $f(s)$；该分数可以是模型似然、价值估计或启发式分数。

<div class="method-step__io" markdown="1">

**输入**：当前轮活跃状态集合 $\mathcal{A}_t$、底层推理模型、搜索控制器及固定推理预算。<br>
**输出**：带有基础分数 $f(s)$ 的候选推理状态集合。

</div>

**直观理解**：这一步仍由原搜索算法提出下一批可能的思路并初步判断其前景，BASIN 不改变模型写出什么，只改变随后优先保留什么。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 构造任务相关的推理盆地

通过盆地映射 $\mathcal{B}:\mathcal{S}\rightarrow\mathcal{Z}$ 为每个状态分配离散标识；结构化任务使用确定性键，开放式任务使用答案一致性、主假设抽取和 NLI 兼容性近似策略等价。

<div class="method-step__io" markdown="1">

**输入**：候选状态 $s$ 的推理轨迹、当前答案及任务可利用的结构信息。<br>
**输出**：每个候选的盆地标识 $z=\mathcal{B}(s)$，以及语义任务中相应的聚类关系。

</div>

**直观理解**：它相当于给不同表述的推理路线贴上“实际采用哪种策略”的标签，从而识别看似丰富、实则重复的候选。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 计算盆地感知选择分数

BASIN 从 $f(s)$ 中减去随同一盆地访问次数对数增长的惩罚；QA-BASIN 再用 $1-q_z$ 调节惩罚，使高质量盆地受到更弱抑制。

<div class="method-step__io" markdown="1">

**输入**：基础分数 $f(s)$、盆地标识 $\mathcal{B}(s)$、历史访问计数 $\mathrm{visits}[z]$，以及 QA-BASIN 可选的盆地质量 $q_z$。<br>
**输出**：每个候选的盆地感知分数 $\tilde{f}(s)$。

</div>

**直观理解**：常被选择的路线会逐渐“涨价”，但惩罚增长是次线性的，因此不会永久封死旧路线；若旧路线确实优质，QA-BASIN 会降低其涨价幅度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 选择、更新并完成搜索

ToT 保留分数最高的 $k$ 个状态形成下一轮 $\mathcal{A}_{t+1}$；MCTS 则只在 UCT 子节点选择中加入盆地项。完成选择后更新被选盆地的访问次数，并在 QA-BASIN 中更新其运行平均质量，随后重复扩展与选择直至预算耗尽或搜索终止。

<div class="method-step__io" markdown="1">

**输入**：按 $\tilde{f}(s)$ 排序的候选、搜索束宽或 MCTS 选择规则，以及当前访问与质量统计。<br>
**输出**：底层搜索程序的最终候选、聚合结果或经验证的答案，以及搜索过程中形成的盆地访问统计。

</div>

**直观理解**：方法并不增加搜索预算，而是在每轮重新安排预算去向：减少对弱且重复路线的投入，同时允许基础分数足够高的旧路线再次胜出。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 结构盆地与语义盆地的任务相关定义

$$
\begin{aligned}
\mathcal{B}(s)&=\bigl(\mathrm{ops}(s),\mathrm{sort}(\mathrm{remaining}(s))\bigr),\\
\mathrm{same\_basin}(s,s')&\Longleftrightarrow \mathrm{ans}(s)=\mathrm{ans}(s')\;\wedge\;\mathrm{NLI}_{\mathrm{ent}}(h_s,h_{s'})\geq\tau_e\;\wedge\;\mathrm{NLI}_{\mathrm{con}}(h_s,h_{s'})\leq\tau_c.
\end{aligned}
$$

**符号说明**

- $s,s'$：两个候选推理状态。
- $\mathcal{B}:\mathcal{S}\rightarrow\mathcal{Z}$：把状态空间映射到离散盆地标识空间的函数。
- $\mathrm{ops}(s)$：状态截至当前时刻按顺序执行的运算符序列。
- $\mathrm{remaining}(s)$：执行已有算术步骤后尚未合并的数值集合。
- $\mathrm{sort}(\cdot)$：对剩余数值排序，以消除无关的排列差异。
- $\mathrm{ans}(s)$：状态所预测或支持的答案。
- $h_s$：从状态推理轨迹中抽取的一句话主假设。
- $\mathrm{NLI}_{\mathrm{ent}}$：自然语言推断模型给出的假设间蕴含或相容分数。
- $\mathrm{NLI}_{\mathrm{con}}$：自然语言推断模型给出的假设间矛盾分数。
- $\tau_e,\tau_c$：分别控制最低蕴含程度和最高矛盾程度的阈值，决定语义聚类粒度。

<div class="equation-explanation" markdown="1">

**直观理解**：第一行是结构化算术任务的精确键：只有已用运算顺序和剩余数字都一致时才视为同一策略。第二行是开放式任务的近似等价条件：两个状态不仅要选择同一答案，其核心假设还必须足够相容且不能明显矛盾；这避免仅因共享大量故事文字就把不同推理路线合并。<br>
**原文位置**：第 3.1 节，公式（1）与公式（2）

</div>

</div>

<div class="equation-block" markdown="1">

#### BASIN 与 QA-BASIN 的盆地感知评分

$$
\begin{aligned}
\tilde{f}_{\mathrm{BASIN}}(s)&=f(s)-\lambda\log\!\left(1+\mathrm{visits}[\mathcal{B}(s)]\right),\\
\tilde{f}_{\mathrm{QA\text{-}BASIN}}(s)&=f(s)-\lambda\log\!\left(1+\mathrm{visits}[\mathcal{B}(s)]\right)\bigl(1-q_{\mathcal{B}(s)}\bigr).
\end{aligned}
$$

**符号说明**

- $s$：当前待选择的候选推理状态。
- $f(s)$：底层搜索程序原本用于选择状态的基础分数。
- $\tilde{f}(s)$：加入盆地访问历史后用于实际排序或选择的分数。
- $\mathcal{B}(s)$：状态所属的推理盆地。
- $\mathrm{visits}[\mathcal{B}(s)]$：该盆地此前被选入活跃搜索集的累计次数。
- $\lambda$：非负惩罚强度；值越大，搜索越偏向尚未充分访问的盆地。
- $q_{\mathcal{B}(s)}$：状态所属盆地的运行平均质量分数，范围为零到一。

<div class="equation-explanation" markdown="1">

**直观理解**：BASIN 用历史访问次数给重复路线扣分：第一次访问时惩罚为零，之后惩罚增加，但对数函数使增长逐渐变慢。QA-BASIN 将该惩罚再乘以质量缺口；当盆地质量接近一时几乎不受重复惩罚，当质量接近零时则退化为原始 BASIN，从而在探索新策略与保留优质策略之间折中。<br>
**原文位置**：第 3.2 节公式（3）与第 3.3 节公式（4）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：BASIN 与 QA-BASIN 均为 training-free 的推理时选择规则，没有参数训练损失、梯度更新或额外微调目标。其计算目的不是直接优化盆地数量，而是在固定推理预算内改变候选排序，使预算较少浪费在结构或语义上重复的策略上；QA-BASIN 进一步利用外部质量信号控制探索—利用折中。$\lambda$、语义阈值 $\tau_e$ 与 $\tau_c$ 属于推理控制参数，不应被解释为通过论文所述训练目标学习得到的模型参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 任务相关的盆地构造器**

在 Game of 24 中，盆地键由截至当前状态的有序运算符序列 $\mathrm{ops}(s)$ 与排序后的剩余数值 $\mathrm{sort}(\mathrm{remaining}(s))$ 组成；运算次序不同的状态不会被错误合并。在 MuSR 中，系统从轨迹抽取一句话主假设 $h_s$，仅在预测答案相同、NLI 蕴含分数不低于 $\tau_e$ 且矛盾分数不高于 $\tau_c$ 时合并状态。

> 直观理解：结构明确时使用可精确复现的规则最可靠；没有显式结构时才借助语义模型判断两段推理是否真正支持兼容的核心主张。作者选择 NLI 而非嵌入相似度，是因为共享故事背景的轨迹可能词汇很像，却支持互相冲突的结论。

**2. 历史依赖的重复访问惩罚器**

所有属于同一盆地 $z$ 的状态共享 $\mathrm{visits}[z]$，计数表示该盆地此前被选入活跃搜索集的次数，而不是候选被生成的次数。惩罚为对数形式，因此未访问盆地不受惩罚，重复访问的边际惩罚逐步减小；超参数 $\lambda\geq 0$ 控制结构多样性相对于基础评分的影响。

> 直观理解：若分别惩罚每个文本候选，模型可以用换一种措辞绕过限制；共享盆地计数才能集体识别同一策略的重复。对数惩罚则保留“回头路”：一个旧盆地只要基础优势足够大，仍然可以被选中。

**3. 质量感知调节器**

QA-BASIN 为每个盆地维护归一化运行平均质量 $q_z\in[0,1]$，并以 $1-q_z$ 缩放重复访问惩罚。它要求验证器或质量估计与正确性具有实际相关性；质量信号不可靠时可能错误保护弱盆地或压制有用探索，因此平坦 BASIN 是不依赖该信号的备选方案。

> 直观理解：单纯追求新路线可能把预算从正确思路上赶走；质量调节器相当于允许“表现好的老路线”获得折扣。不过折扣依据若不可信，系统反而会固守错误路线，所以该模块不是无条件适用。

**训练与推理**

训练阶段无需对基础 LLM、NLI 模型或搜索控制器进行专门训练。推理开始时初始化活跃集合以及各盆地的访问计数；每一轮由原搜索算法扩展候选并计算 $f(s)$，再构造 $\mathcal{B}(s)$、计算 $\tilde{f}(s)$、选出下一轮状态并更新访问计数。QA-BASIN 还根据已获得的验证器或 LLM 质量分数更新盆地运行平均 $q_z$。搜索达到轮数、模拟次数等预算，或满足原控制器的终止条件后，仍由原有验证或聚合机制给出答案。

在 ToT 中，标准算法每轮从候选中保留前 $k$ 个状态，BASIN 仅用 $\tilde{f}(s)$ 替代 $f(s)$ 执行该排名，其余生成、束宽、终止和验证组件保持不变。在 UCT-MCTS 中，盆地项只加入子节点选择，不改树展开及模拟框架；在 GoT 中，盆地感知机制决定哪些策略在搜索中存活，原有图聚合随后组合轨迹。因而方法的接口要求很低：搜索器只需能枚举候选、提供基础分数、维护选择历史，并能为任务定义盆地映射；只有 QA-BASIN 额外要求可信的质量估计。

**复现信息**

复现时最关键的是保持搜索预算与基础搜索一致，并明确“访问”指盆地中的状态被选入活跃搜索集，而非仅被生成；计数应在每次选择完成后更新，同一盆地的所有状态共享计数。Game of 24 应保存有序运算序列并排序剩余数值，不能把运算顺序不同的状态合并。MuSR 需要从每条轨迹抽取一句话 $\mathrm{main\_hypothesis}$，随后同时检查答案一致、NLI 蕴含阈值和矛盾阈值；原文说明语义盆地比确定性结构键更噪声化，因此跨实现比较时必须报告抽取器、NLI 模型及阈值。

QA-BASIN 中 $q_z$ 必须归一化到 $[0,1]$ 并作为盆地运行平均质量使用，不能直接把未经校准、量纲任意的启发式分数代入。论文的 MuSR 主设置在表 3 中报告九轮搜索及 $\lambda=3.0$；惩罚消融考察 $\lambda\in\{0.5,1.0,1.5,2.0,3.0,4.0,5.0\}$，说明实现时需验证中等惩罚区间，而不能默认越强越好。MCTS 泛化实验使用每题 50 次模拟并仅修改 UCT 子节点选择。除此之外，候选生成、基础评分、束宽、答案验证与终止条件应保持和对应基线相同，才能把差异归因于盆地感知选择。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Game of 24：采用 Yao et al.（2023）的标准 100 题集合。每题要求用加、减、乘、除组合四个整数得到 24，表达式可通过计算结果与数字使用情况进行精确验证。它主要测试 BASIN 在离散、可明确定义结构盆地的符号搜索中，能否避免反复访问同类算术状态。
- MuSR：从谋杀谜题、物体放置和团队分配三个子任务中均匀抽取 300 题；附录分项结果实际包含谋杀谜题 94 题、团队分配 96 题和物体放置 110 题。该数据集测试自然语言多步推理；实验从每条轨迹抽取 $main\_hypothesis$，再按语义关系形成盆地，因此也检验方法在盆地边界不能由规则直接确定时是否有效。
- HumanEval：程序合成基准，文中将其用于更广泛的泛化评估，并指出代码轨迹可采用确定性的结构盆地定义。所给章节没有报告其样本规模、具体划分或对应数值结果；此外，作者还评估了 GSM-Hard 与 BIG-Bench Hard 的 Logical Deduction，但受数据集数量限制不再展开。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（Accuracy）**

最终选中答案正确的题目比例；Game of 24 可精确执行验证，MuSR 则按任务答案判断。它同时受候选集合是否包含正确答案以及最终候选选择是否成功影响。 （越高越好，因为直接表示完整搜索和答案选择流程解决了更多问题。）

</div>
<div class="metric-item" markdown="1">

**$Pass@k$**

至少一个最终候选正确的题目比例，其中 $k$ 是保留的候选数。它衡量搜索是否发现过正确答案，而不是最终选择器能否把正确候选排在首位。 （越高越好；较高的 $Pass@k$ 配合较低准确率，通常表明主要瓶颈在候选选择而非策略覆盖。）

</div>
<div class="metric-item" markdown="1">

**有效盆地数 $N_{\mathrm{eff}}$**

概括搜索实际覆盖多少个具有实质权重的结构或语义盆地；比原始盆地数量更关注分布是否集中。它是搜索多样性诊断量，不是任务正确性指标。 （不存在普遍的越高或越低越好：较低值可能表示错误策略上的有害坍缩，也可能表示多个轨迹围绕正确策略形成了有用共识。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 匹配推理预算下的总体结果：Game of 24 与 MuSR

<div class="result-value" markdown="1">

作者报告，相比标准 ToT，BASIN 在 Game of 24 上最高提高 22 个百分点，在 MuSR 上最高提高 6.7 个百分点。

</div>

这一结果支持“只改变候选选择即可提高推理搜索效率”的核心主张，因为计算预算和其他搜索环节受到控制。它表明收益可以跨越符号算术与自然语言推理，但“最高提升”是最佳设置的结果，不代表每个模型、子任务或样本都获得同等改善，也不能单独证明提升必然来自更高的盆地数量。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under matched inference budgets, BASIN improves over Tree of Thoughts (ToT) by up to $+22$pp on Game of 24 and $+6.7$pp on MuSR.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### MuSR 物体放置：gpt-oss-120b

<div class="result-value" markdown="1">

标准 ToT 的准确率为 0.564，BASIN 为 0.645，增加 0.082；标准 ToT 的 $Pass@k$ 为 0.755、$N_{\mathrm{eff}}=4.18$。作者进一步报告该差异的 $p=0.032$，配对比较中有 14 个 BASIN 胜例和 5 个败例。

</div>

这里标准搜索约有四分之一题目完全没有正确最终候选，而 BASIN 的显著正收益与“扩大策略级覆盖可以找回原先遗漏答案”的解释一致。该结果仍是特定模型与子任务上的关联证据；表中没有给出 BASIN 的 $N_{\mathrm{eff}}$，所以不能仅凭这一行量化多样性增加了多少。

<div class="result-source" markdown="1">

来源：附录 A，Table 6，Object placement 分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

BASIN improves accuracy by +0.082 ($p=0.032$, 14 wins vs. 5 losses), consistent with additional strategy-level exploration recovering answers that standard search misses.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MuSR 物体放置：gpt-4o-mini

<div class="result-value" markdown="1">

标准 ToT 的准确率为 0.609，BASIN 降至 0.573，即下降 0.036；标准 ToT 已有 $Pass@k=0.827$，尽管其有效盆地数仅为 $N_{\mathrm{eff}}=3.84$。

</div>

这是对方法边界最关键的反例：低盆地数不必然表示搜索失败。此时正确候选覆盖率已经较高，无条件惩罚重复策略可能移走围绕优质解形成的有效共识。该结果说明 BASIN 不是稳定支配 ToT 的替代品，也构成引入 QA-BASIN 或自适应路由的直接动机。

<div class="result-source" markdown="1">

来源：附录 A，Table 6，Object placement 分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For gpt-4o-mini, standard ToT has an even lower $N_{\mathrm{eff}}=3.84$, yet Pass@$k$ is already $0.827$ and BASIN reduces final accuracy by $0.036$.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给章节未提供完整主结果表、QA-BASIN 的独立量化结果，以及 HumanEval、GSM-Hard 和 Logical Deduction 的具体分数；因此无法核验所有模型和数据集上的一致性，也不能量化质量感知修正相对原始 BASIN 的贡献。
- MuSR 的盆地依赖模型抽取 $main\_hypothesis$ 及语义聚类，可能受抽取错误、蕴含模型和阈值影响。作者声称附录结果对替代设置稳健，但当前材料没有给出对应数值；此外，多项子任务差异不显著，路由分析也仅覆盖六个实验设置，统计结论仍需更大规模复验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 标准 ToT：主要受控基线。它以树搜索保留候选推理状态，但不惩罚重复进入同一结构或语义盆地。BASIN 只替换其候选选择规则，其他生成与评测环节保持不变，因此差异可较直接归因于结构感知选择。
- BASIN：在分析质量感知版本或自适应路由时，原始 BASIN 构成固定的“增加探索”策略。它对重复访问盆地施加与质量无关的惩罚，适合检验单纯扩大策略多样性是否会因过度探索而损害已有的正确共识。
- QA-BASIN：质量感知变体，对高质量盆地减弱重复访问惩罚。所给材料主要说明其设计动机，未提供可核验的独立结果表，因此不能据此量化其相对 ToT 或 BASIN 的收益。
- 固定策略与路由策略：诊断实验把始终使用标准 ToT、始终使用 BASIN，与根据冗余及搜索状态信号逐题选择策略的 routed 方法比较，用于检验“哪种题应增加探索”能否自适应决定。

**实验想回答的问题**

- 在生成次数、搜索预算和最终答案选择方式均相同的条件下，仅将标准思维树（Tree of Thoughts, ToT）的候选选择改为结构感知的 BASIN，能否减少对重复推理策略的集中，并提高不同模型在符号推理与自然语言多步推理任务上的正确率？
- 推理轨迹集中是否一定意味着有害的“推理盆地坍缩”，以及有效盆地数、候选覆盖率和冗余差等搜索状态信号，能否判断应当继续利用当前高质量策略还是扩大探索？

**实验实现**

主要 Game of 24 实验使用 gpt-4o-mini 与 Qwen3-27B；MuSR 使用 gpt-4o-mini 与 gpt-oss-120b，扩展评估还覆盖 Qwen2.5-7B-Instruct 和 Llama-3.3-70B-Instruct。BASIN 与 QA-BASIN 分别只按原文公式（3）和公式（4）改变 ToT 的候选选择，生成过程、搜索预算及最终答案选择保持固定。Game of 24 使用束宽 $k=5$、分支因子 $b=5$、深度 $T=3$、采样温度 0.7；MuSR 使用束宽 $k=2$、九轮推理和温度 0.8。在 MuSR 中，标准方法和盆地感知方法每题都使用 18 次生成调用及 18 次假设抽取调用，以避免把额外模型调用误当成算法收益。语义聚类采用蕴含阈值 $\tau_e=0.45$ 和矛盾上限 $\tau_c=0.3$；除另有说明外，盆地重复惩罚系数为 $\lambda=3.0$。作者称附录研究了抽取器、自然语言推断聚类及阈值敏感性，但所给材料没有相应完整数值。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 策略路由信号消融：只使用冗余差 $\Delta_\rho$，对比再加入节点数 $n_{nodes}$ | 仅凭 $\Delta_\rho$，六个实验设置中只在 2 个设置选中经验上更好的固定策略，决策准确率为 33.3%；加入已有的 $n_{nodes}$ 信号后提高到 5/6，即 83.3%。 | 该比较隔离了额外搜索状态信号的作用：冗余差可以描述正确与错误预测的搜索集中差异，却不能独立决定应利用还是探索；节点数补充了问题级搜索进展信息。由于这里只有六个设置，83.3% 的比例对单个设置非常敏感，不能视为稳定的泛化估计。 | 路由诊断实验，所给无编号表格之后<br><span class="experiment-evidence">Incorporating the already-available $n_nodes$ signal raises the routing decision accuracy to 5/6 settings (83.3%).</span> |
| 固定选择策略对比逐题路由：Game24/gpt-4o-mini | 逐题路由准确率为 0.760，高于固定使用标准 ToT 的 0.660，也高于固定使用 BASIN 的 0.720。 | 这一比较检验收益是否只来自全局偏向 BASIN。路由结果超过两种固定策略，说明不同题目可能分别适合维持当前盆地或增加探索，逐题决策能够利用这种异质性。不过所给材料未说明路由阈值是否在独立验证集上确定，因此仍需排除针对这些实验设置调参带来的乐观偏差。 | 路由诊断实验，所给无编号表格及其后正文<br><span class="experiment-evidence">On Game24/gpt-4o-mini, routed accuracy reaches 0.760, compared with 0.660 for standard ToT and 0.720 for BASIN.</span> |

**定性案例**

- MuSR 物体放置构成一组有解释力的对照案例：gpt-oss-120b 在标准 ToT 下的 $N_{\mathrm{eff}}=4.18$、$Pass@k=0.755$，BASIN 提高 0.082；gpt-4o-mini 的 $N_{\mathrm{eff}}$ 更低，仅 3.84，但 $Pass@k$ 已达 0.827，BASIN 反而下降 0.036。两者共同表明，低盆地覆盖只有在正确候选确实缺失时才更可能意味着有害坍缩；若正确候选已被发现，额外探索可能破坏有效共识。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper improves inference-time LLM reasoning through structure-aware search and diversification across distinct reasoning trajectories.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`360aa3b53cf88eea5116f69480aaa87f92208bdc436c4695f15c6321c8af7fe5`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
