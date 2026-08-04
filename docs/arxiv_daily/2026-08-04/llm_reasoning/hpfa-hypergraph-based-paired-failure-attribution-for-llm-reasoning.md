---
title: "[论文解读] HPFA: Hypergraph-Based Paired Failure Attribution for LLM Reasoning"
description: "[arXiv 2608.02026][LLM Reasoning] HPFA通过对比同一问题的成功与失败推理轨迹，并用依赖超图追踪跨步骤、联合依赖的错误传播，以较低验证成本生成根因标注，进而训练可在测试时辅助反思的轻量归因模型。"
arxiv_id: "2608.02026"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:57:39.951097+00:00"
source_sha256: "e0dac24ec5b36a7587454ba7de002e0d67cc445f165817111ab384dff0aab4d9"
tags:
  - "LLM Reasoning"
  - "大语言模型推理"
  - "失败归因"
  - "反思式推理"
  - "配对轨迹"
  - "依赖超图"
  - "根因定位"
  - "智能体系统"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.02026</p>

# HPFA: Hypergraph-Based Paired Failure Attribution for LLM Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Runchuan Zhu, Hongbin Lai, Bowen Jiang, Junrui Zhang, Zhangheng LI, Ostap Kilbasovych, Junyuan Hong</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02026v1) · [PDF 下载](https://arxiv.org/pdf/2608.02026v1) · **关键词** 大语言模型推理, 失败归因, 反思式推理, 配对轨迹, 依赖超图, 根因定位, 智能体系统<br>


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

HPFA通过对比同一问题的成功与失败推理轨迹，并用依赖超图追踪跨步骤、联合依赖的错误传播，以较低验证成本生成根因标注，进而训练可在测试时辅助反思的轻量归因模型。

**不用术语来说**：大语言模型即使能够在知道错误位置后修正答案，也往往无法自行判断长篇推理究竟从哪一步开始出错；如果逐步替换并重新执行来检查每个候选步骤，轨迹越长，验证成本越高，而且一个错误结论还可能由多处相隔很远的前置推导共同造成。因此，研究需要一种既能找到真正上游错误、又能大规模生成训练标注的归因方法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出HPFA归因数据合成框架：为同一查询收集成功与失败轨迹，将推理拆成原子步骤并构建依赖超图，再把反事实验证集中于两条轨迹的关键分歧及其依赖路径，以改善根因定位的成本与成功率权衡。
- 使用HPFA验证所得的根因标注，通过监督微调和强化学习训练轻量归因模型；该模型只需读取单条失败轨迹即可给出错误步骤、错误类型与错误内容，为后续重新推理提供结构化反馈，而不需要修改底层推理模型。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型推理与智能体系统中的失败归因。此类系统通常先生成包含多个中间步骤的推理轨迹，再依据最终答案、程序测试或环境反馈判断执行是否成功；当轨迹失败时，仅知道最终结果错误并不足以支持有效反思，还需要定位最早引发后续错误的根因步骤。已有研究表明，大语言模型即使在获知错误位置后能够修正答案，也往往不擅长自行定位该位置。问题在智能体任务中更复杂，因为故障不仅可能来自语言推理，还可能来自记忆、工具执行或智能体通信，并沿组件和步骤之间的依赖关系传播。本文因此把失败归因视为连接“检测到失败”与“有针对性地重新推理”之间的关键环节，并关注如何规模化生成可用于训练专用归因模型的根因监督数据。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**反思式推理**

模型在获得答案正确性、测试结果或环境反馈后，重新检查已有推理轨迹，识别问题并生成修订结果。其有效性取决于模型能否把最终失败准确追溯到具体的中间步骤。

</div>
<div class="concept-item" markdown="1">

**失败归因**

失败归因是在一条失败轨迹中找出导致下游错误的起源步骤，而不只是判断整条轨迹是否失败。该任务通常还可输出错误类型与错误内容，以便后续模型执行针对性修正。

</div>
<div class="concept-item" markdown="1">

**依赖超图**

超图允许一条超边同时连接多个节点，因而可以表达“某个结论由若干分散的前置步骤共同推出”的高阶依赖。本文以原子推理步骤为节点，用超边表示步骤集合之间的逻辑依赖，从而追踪非线性的错误传播。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个查询及其失败推理轨迹，目标是定位造成最终失败的根因步骤，并形成可包含错误步骤、错误类型和错误内容的归因结果。本文采用配对设置：对同一查询收集一条成功轨迹作为有效参考，将失败轨迹与成功轨迹进行语义对齐和原子步骤分解，再重点检查二者依赖结构中的分歧，而不是依次修复并重放失败轨迹中的每个候选步骤。该设置假定能够为同一查询获得至少一条成功参考轨迹，并能根据最终答案、程序测试或执行反馈区分成功与失败；生成的归因轨迹随后用作监督数据，通过监督微调与强化学习训练轻量归因模型，使其在测试时仅根据查询和失败轨迹直接提供定位反馈，支持重新生成推理结果。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Who&When（Zhang et al., 2025b）**: 该工作将多智能体系统中的失败归因定义为无需依赖模型自身内省判断的根因识别任务，并通过基准揭示现有大语言模型定位失败点的能力有限。它为本文的问题定义与评测需求提供直接背景，但没有解决长轨迹归因数据的低成本规模化合成以及复杂步骤依赖的显式建模。
- **AgenTracer（Zhang et al., 2025a）**: 该工作利用反事实重放和程序化故障注入生成标签，并训练轻量归因器执行智能体级与步骤级定位，说明专用归因模型可避免推理时反复重放。本文沿用“合成标注数据后训练归因器”的方向，但针对其逐候选步骤干预与重新执行所带来的高成本，引入成功—失败配对比较和依赖超图来缩小搜索空间并表示非线性依赖。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

反思式推理要求模型根据执行结果回看并修正自己的推理，但修正是否有效取决于能否先定位导致后续失败的中间根因。原文援引既有证据指出，模型在已知错误位置时可能完成纠正，却不擅长自行找到该位置；这会使数学证明、智能体规划和代码生成中的长链失败难以调试，也削弱高风险场景所要求的可解释性、可信度与安全审查能力。本文因而把重点放在可扩展的归因监督构造上，使专门的归因模型经过训练后能直接分析失败轨迹。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于分类体系的回顾式提示**：让大语言模型依据预设错误分类直接阅读失败轨迹，判断关键错误步骤并生成纠正反馈。这类方法使用轨迹本身进行事后分析，实施简单，但定位结果依赖模型的回顾判断能力。
- **逐步骤反事实回放与故障注入**：依次把每个候选步骤修复或替换，再重新执行其后的轨迹，根据最终失败是否消失判断该步骤是否具有决定性；也可通过程序化注入已知故障来构造带标签数据，并用这些数据训练专门的归因器。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 逐步骤反事实标注需要对候选步骤反复修复和重放下游过程，成本随轨迹长度迅速增长；当数学证明或智能体规划包含数十步时，大规模合成归因数据会变得昂贵，限制专门归因模型可获得的训练监督。
- 既有方法通常把推理表示为扁平线性序列，难以表达非局部和高阶依赖。例如，一个后期结论可能同时依赖多条位置相隔较远的早期推导；忽略这种联合依赖会遮蔽错误传播路径，使系统容易停留在下游症状，而不能回溯到真正的上游根因。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未同时解决归因数据的可扩展生成与复杂依赖建模：一方面需要避免对轨迹中的每一步进行穷举式反事实验证，另一方面又必须表示多个前置步骤共同支持后续结论的结构，并据此找到最早且具有因果意义的失败来源。尤其缺少一种能把成功轨迹作为有效参照、把搜索限制在关键分歧附近，并将验证后的根因转化为专门归因器训练数据的统一框架。

</div>
<div markdown="1"><span>核心问题</span>

能否利用同一查询下的成功轨迹作为失败轨迹的反事实参照，并通过依赖超图刻画跨位置、多步骤联合依赖，从而以更少的验证开销可靠定位长链推理的上游根因；这些可扩展生成的归因监督又能否训练出仅凭单条失败轨迹便改善测试时反思与重推理的轻量模型？

</div>
<div markdown="1"><span>作者直觉</span>

成功轨迹相当于一份已经验证可行的解题参照，因此无需盲目检查失败轨迹的全部步骤，而可优先考察两者发生实质分歧的位置。超图则允许一条依赖关系同时连接多个前提与一个结论，比普通线性顺序更接近“若干前置推导共同支持后续判断”的真实逻辑。把分歧对比与依赖回溯结合后，系统可以从可见的下游错误沿结构向上追踪，再只对少量根因候选进行验证；直观上，这相当于先用正确解缩小排查范围，再沿推理关系图寻找最初断点。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

HPFA包含“离线归因数据构造”和“在线反思推理”两条相连流程。离线阶段先针对同一问题$Q$从目标模型采样一条成功轨迹$T^+$和一条失败轨迹$T^-$，把两条轨迹切分、语义对齐并组织为依赖超图$G=(V,E_h)$；算法随后从成功结论沿依赖反向搜索两条轨迹的会合点，只对会合点之后未对齐的失败步骤做反事实修复测试，从而找出最早能够挽救最终结果的根因步骤。经验证的根因、错误类型和错误描述被整理为监督数据，用于先SFT、再GRPO训练轻量归因器$\pi_\phi$。

在线阶段不再需要成功参考轨迹、超图或答案标签：系统先让基础模型$\pi$生成单条推理轨迹$T$，以语言化置信分数$S(T)$判断是否可能失败；低于阈值$\tau$时，归因器根据$(Q,T)$指出可疑步骤及错误内容，基础模型据此重新生成。直观地说，HPFA在数据生产时用“正确解的结构”缩小排错范围并用实际重跑验证诊断；部署时则把这种排错能力压缩进一个小模型，使其可以仅看当前错误过程给出可执行的修改建议。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 成功—失败轨迹配对

在固定生成协议下重复采样，直到同时得到满足$\mathbf{1}(T^+)=1$的成功轨迹和$\mathbf{1}(T^-)=0$的失败轨迹，或耗尽$K$次预算；若只有一种结果则丢弃该问题，存在多个候选时选择长度最接近的一对。

<div class="method-step__io" markdown="1">

**输入**：问题$Q$、目标LLM或智能体、正确性判定器$\mathbf{1}(\cdot)$以及每题最多$K$次的采样预算。<br>
**输出**：同一问题上的配对轨迹$(T^+,T^-)$，其中每条轨迹都包含中间步骤与最终预测。

</div>

**直观理解**：成功轨迹相当于同一道题的可行路线图，失败轨迹则是待排查路线；两者对照后，算法主要检查真正发生分歧的地方，而不必盲测所有步骤。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 步骤对齐与依赖超图构造

先将两条轨迹切分为原子步骤，再依据语义相似性和聚类建立等价关系$\sim$；仅当两条轨迹明确表达相同推理操作或代码意图时才合并为同一抽象顶点$[s]_\sim$，随后由LLM估计每一步的前置条件，并用超边编码多对一或多对多依赖。

<div class="method-step__io" markdown="1">

**输入**：配对轨迹$(T^+,T^-)$。<br>
**输出**：超图$G=(V,E_h)$、成功与失败轨迹使用的顶点集合$V^+$和$V^-$，以及两个最终预测顶点$v^+_{\mathrm{out}}$与$v^-_{\mathrm{out}}$。

</div>

**直观理解**：普通序列只表示“下一步跟在上一步后面”，超图则能表示某个结论同时依赖几个不相邻的事实、工具结果或子目标，因此更贴近数学推理和智能体执行中的真实因果结构。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 会合点搜索与反事实根因验证

从$v^+_{\mathrm{out}}$开始，沿成功轨迹的有向依赖反向遍历，找到首个属于$V^+\cap V^-$的会合顶点$v^\star$；把失败轨迹中位于该点之后、但无法与成功轨迹对齐的后继作为候选集$C$，逐一替换相应步骤并重新采样下游过程，若修复后的轨迹通过判定就返回该步骤，否则以$v^\star$重新锚定并继续向前搜索。

<div class="method-step__io" markdown="1">

**输入**：超图$G$、配对轨迹$(T^+,T^-)$、反事实重采样协议$R$和正确性判定器$\mathbf{1}(\cdot)$。<br>
**输出**：失败轨迹$T^-$上的已验证根因索引$k$，或在没有可用配对、共享区域耗尽等情况下返回FAIL。

</div>

**直观理解**：算法像从正确答案倒着追溯：先找到正确与错误路线最近一次共享的可靠节点，再检查错误路线随后独有的分支。候选步骤只有在“改掉它并重跑后真的成功”时才被接受，因此归因不是单纯依靠文本判断。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 归因器的SFT与GRPO训练

第一阶段用标准因果语言模型目标进行监督微调，使$\pi_\phi$模仿固定格式的诊断；第二阶段在目标模型在线产生的失败样本上进行GRPO，对同一$(Q,T_{\mathrm{fail}})$采样一组诊断，以组内标准化奖励形成优势，并结合裁剪策略比率与相对参考策略$\pi_{\mathrm{ref}}$的KL正则更新。

<div class="method-step__io" markdown="1">

**输入**：由HPFA生成的训练元组，包括$Q$、失败轨迹$T^-$、根因索引$k$、简短理由，以及可选的成功反事实替换片段$s'$。<br>
**输出**：轻量归因器$\pi_\phi$，其输出包含错误步骤、错误类型和对错误内容的简洁描述。

</div>

**直观理解**：SFT先教模型“诊断报告应该怎么写”，GRPO再用实际修复结果检查报告是否有用。这样模型不仅要指出一个看似合理的问题，还要给出能帮助基础模型改对答案的诊断。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 最早可恢复步骤的根因定义

$$
k=\min\left\{j:\exists s'_j\ \mathrm{s.t.}\ \mathbf{1}\!\left(R(T_{\mathrm{fail}},j,s'_j)\right)=1\right\}
$$

**符号说明**

- $k$：被定义为根因的最早步骤索引。
- $j$：失败轨迹中的候选步骤索引。
- $T_{\mathrm{fail}}$：最终结果错误的原始推理轨迹。
- $s'_j$：与原步骤粒度一致、用于替换第$j$步的修复内容。
- $R(T_{\mathrm{fail}},j,s'_j)$：保持第$j$步之前的前缀不变，以$s'_j$替换原步骤，并按固定协议重新采样全部下游步骤后得到的新轨迹。
- $\mathbf{1}(T)$：轨迹正确性指示函数；正确取1，错误取0。

<div class="equation-explanation" markdown="1">

**直观理解**：该定义不把所有可修复步骤都算作并列根因，而是选择最早能通过替换并重新生成后续过程来恢复正确答案的位置。于是后续错误被视为第一次可恢复分歧造成的后果，这为训练标签提供了明确且可验证的标准。<br>
**原文位置**：第3节 Problem Formulation

</div>

</div>

<div class="equation-block" markdown="1">

#### GRPO归因奖励

$$
R_i=R_i^{\mathrm{fmt}}+\lambda R_i^{\mathrm{rollout}},\qquad \lambda>0,\qquad R_i^{\mathrm{rollout}}=\mathbf{1}(\widetilde{T}_i)
$$

**符号说明**

- $R_i$：第$i$个采样诊断获得的序列级总奖励。
- $R_i^{\mathrm{fmt}}$：格式奖励，检查诊断能否解析、步骤索引是否合法、必需字段与分隔符是否完整。
- $R_i^{\mathrm{rollout}}$：重跑奖励，表示使用该诊断后生成的新轨迹是否正确。
- $\lambda$：正的权重系数，用于调节重跑成功奖励对总奖励的贡献。
- $\widetilde{T}_i$：基础模型或智能体以问题、失败轨迹和第$i$个诊断为条件重新生成的轨迹。
- $\mathbf{1}(\widetilde{T}_i)$：新轨迹正确时为1，否则为0的指示值。

<div class="equation-explanation" markdown="1">

**直观理解**：奖励同时要求诊断“机器可读”和“确实能帮助改对”。仅满足格式只能获得格式部分，只有诊断推动基础模型重跑成功时才得到行动有效性奖励。<br>
**原文位置**：第3.2节，公式(1)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练分为模仿与策略优化两阶段。SFT阶段使用标准因果语言建模目标，给定任务指令、问题$Q$和带索引的失败轨迹，最大化模板化诊断目标的条件似然，使归因器掌握步骤索引、错误类型和错误内容的输出规范；原文未给出该标准目标的展开公式。GRPO阶段从$\pi_\phi$为每个$(Q,T_{\mathrm{fail}})$采样一组归因，用$R_i=R_i^{\mathrm{fmt}}+\lambda R_i^{\mathrm{rollout}}$评分，再将组内奖励标准化为零均值、单位方差的优势值，并通过裁剪策略比率更新，同时以相对$\pi_{\mathrm{ref}}$的KL正则限制策略漂移。其关键连接是：HPFA产生经反事实验证的离线标签供SFT学习，而在线失败上的重跑奖励让GRPO直接优化部署时真正关心的“诊断能否促成正确重生成”。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 配对依赖超图**

顶点$V$不是原始文本位置，而是由两条轨迹中语义等价的原子步骤形成的抽象类$[s]_\sim$；超边$E_h$编码步骤$s_j$所依赖的前置步骤集合$\{s_i\}_{i\in P(j)}$。对齐规则偏保守：只有显式相同的推理操作或代码意图才合并，否则保留为不同顶点。

> 直观理解：该模块同时解决两个问题：成功轨迹提供对照，超图保留非连续依赖。保守合并可以减少把表面措辞相近、实际逻辑不同的步骤误当成同一步的风险。

**2. 迭代会合点定位器**

定位器沿成功轨迹的有向依赖和反向步骤顺序搜索$v^\star\in V^+\cap V^-$，分支采用固定的打破平局规则；$v^\star$不一定是无向图意义下两个输出顶点的最低公共祖先，因为搜索方向和参照路径均由$T^+$限定。候选集由失败轨迹中从$v^\star$出发且未与成功轨迹对齐的后继构成。

> 直观理解：会合点是两条路线共享的参照锚点，不是简单寻找文本第一次不同的位置。沿正确依赖倒查能把测试集中在影响最终答案的分歧分支上，从而减少昂贵的反事实重跑。

**3. 可执行诊断归因器**

归因器$\pi_\phi$将$(Q,T_{\mathrm{fail}})$映射为结构化诊断，字段包括有效步骤索引、错误类型和错误内容；格式奖励检查输出能否按模板解析，重跑奖励则把诊断交给基础模型或智能体生成新轨迹$\widetilde{T}_i$，并依据$\mathbf{1}(\widetilde{T}_i)$评价诊断是否促成成功。

> 直观理解：结构化输出保证修复程序能稳定读取，重跑检验保证诊断具有行动价值。二者结合避免模型只写出流畅但无法指导修复的泛泛批评。

**训练与推理**

数据与训练流程为：对每个$Q$在预算$K$内采样并选择长度接近的$(T^+,T^-)$，构建对齐超图，利用会合点候选搜索和反事实重跑得到经验证索引$k$，再保存$T^-$、$k$、简短理由及可选修复片段$s'$；随后先对这些结构化样本进行SFT，再以最终SFT模型初始化GRPO，并使用目标模型在线生成的失败轨迹做策略精炼。数学任务的配对与仅负例根因提示采用与格式奖励一致的$\texttt{root\_cause}$标签模式。

推理流程为：基础模型$\pi$先对新问题生成单条轨迹，系统计算语言化置信分数$S(T)$；若达到$\tau$则直接接受，否则归因器仅根据$(Q,T)$生成诊断，基础模型利用该诊断执行修复重生成。系统在新分数达到阈值、分数变化可忽略或完成$B$轮修复时停止。这里需要区分两个场景：HPFA离线定位依赖成功参考、超图和正确性判定器，而测试时归因器不可见真实答案、成功路径及超图，其能力来自训练阶段对HPFA归因数据的压缩学习。

**复现信息**

公平复现需要固定四类协议：轨迹生成协议、每题采样上限$K$、反事实替换后重采样下游步骤的协议$R$，以及正确性判定器$\mathbf{1}(\cdot)$；否则“可恢复”与搜索成本不可直接比较。原子步骤可以是一项算术操作、一次工具调用或一个子目标；超图由LLM按照附录D模板构建，其可靠性检查位于附录A。多条合格轨迹存在时按长度最接近原则配对，只有成功或只有失败的题目会被删除。

测试时还必须指定语言化置信函数$S$、触发阈值$\tau$、修复预算$B$以及“分数变化可忽略”的停止规则。节选未明确报告具体$K$、$\lambda$、$\tau$、$B$数值，也未给出语义聚类模型、相似度阈值、GRPO裁剪系数、KL系数、组大小或稳定常数，因此不能从当前章节补造这些设置；编码任务的轨迹采样提示、超图构建提示和修复相关模板需查阅附录D。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学推理：MATH 与 GSM8K 用于生成成功—失败轨迹和训练归因器。MATH 使用官方训练集训练，并在 MATH500 上评测；GSM8K 使用官方训练集与测试集。归因迁移分析还使用 AIME 2024 和 LogiQA 2.0，其中失败样本数分别为 22 和 441，但它们不参与归因器训练。
- 智能体编程：KodCode 使用官方训练集和测试集；MBPP 随机划分为 $3{:}1$ 的训练—评测集。收集到的成功—失败轨迹对数量分别为 KodCode 853、MBPP 479，可用于归因定位；其中成功修复轨迹分别为 473、112，用于归因器训练。
- 隐私场景：使用 PrivateAI 对基于 CoQA 的输入进行去标识化，以检验隐私信息缺失所致推理失败的定位能力。该设置要求修复后的轨迹既成功完成任务，又满足无泄漏约束；原文节选未报告样本规模与具体划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Rollout-verified success rate（反事实展开验证成功率）**

在失败轨迹中，将方法定位的步骤 $k$ 替换为修复片段 $s'$ 后，共享判定器是否将新轨迹 $R(T^-,k,s')$ 判为成功；隐私场景还必须满足无泄漏约束。该指标直接检查被定位步骤是否具有可操作的因果修复价值，而不只是与人工标签表面一致。 （越高越好，因为更高比例表示修改被归因的步骤确实能够翻转失败结果。）

</div>
<div class="metric-item" markdown="1">

**Pass@1 任务准确率**

归因器引导一次反思修复后，模型首次生成即答对的题目比例，用于评价归因是否最终转化为数学或编程任务收益。AIME 2024 的专项修复分析例外地使用 Pass@16。 （越高越好，因为它表示端到端推理成功率更高；但它同时受骨干模型执行修复能力影响，不能单独证明根因定位完全正确。）

</div>
<div class="metric-item" markdown="1">

**Correction success rate（修正成功率）**

仅在模型第一次作答失败的样本上，经过一次归因器引导修复后成功解决问题的比例；默认按 Pass@1 判断，AIME 2024 按 Pass@16 判断。该指标比总体准确率更集中地测试归因信号能否促成有效修复。 （越高越好，因为更高比例说明归因器能将初始失败转化为成功；不过它仍混合了定位质量与骨干模型重写推理的能力。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 第 5 轮失败定位：五个数学、隐私和编程基准

<div class="result-value" markdown="1">

HPFA 在 MATH500、GSM8K、CoQA、KodCode、MBPP 上的反事实展开验证成功率依次为 64.6%、76.9%、53.7%、53.4% 和 23.0%，并在五个基准上均超过 AgentDebug 与 AgenTracer。相对每个数据集上较强的基线，作者报告前四个基准提升超过 30%，MBPP 提升超过 17.2%。

</div>

作者主张，配对比较与结构化候选搜索能更常找到“修复后确实使结果翻转”的步骤。由于所有方法共享同一结果判定器，该比较主要反映定位策略差异；但它是在已获得一对成功—失败轨迹且允许反事实展开的受控条件下完成，不能直接等同于部署时仅有单条失败轨迹的性能。

<div class="result-source" markdown="1">

来源：Section 4.1, Main results；数值见 Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At the fifth refinement step, Ours outperforms both AgentDebug and AgenTracer on all five benchmarks.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 测试时反思：MATH500、GSM8K、KodCode 与 MBPP

<div class="result-value" markdown="1">

SFT+GRPO 归因器的 Pass@1 分别为 84.8%、93.0%、46.3% 和 48.4%；相较 Vanilla prompting 的 79.4%、92.6%、43.9% 和 46.5%，对应提高 5.4、0.4、2.4 和 1.9 个百分点。它在 MATH500 与两个编程任务上取得表中最高值，但 GSM8K 的最高值是仅 SFT 的 93.4%。

</div>

HPFA 监督带来的收益不局限于离线定位，而能改善最终答题或编程正确率，其中 MATH500 和编程任务的证据最明确。GSM8K 已处于约 93% 的高准确率区间，提升空间较小，且加入 GRPO 后略低于仅 SFT；因此实验支持“整体有用”，不支持“GRPO 在所有任务上都单调改善”。

<div class="result-source" markdown="1">

来源：Section 4.2, Main results；完整四任务数值见 Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Ours (SFT + GRPO) achieves a score of 84.8% on MATH500, outperforming vanilla prompting, Self-reflection, and AgenTracer.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 失败样本修复与跨域归因：MATH500、GSM8K、AIME 2024、LogiQA 2.0

<div class="result-value" markdown="1">

在分别包含 83、84、22、441 个初始失败样本的四个数据集上，SFT+GRPO 的修正成功率为 19.3%、14.3%、22.7%、6.6%，Self-reflection 为 11.9%、7.1%、9.1%、1.2%。绝对提升分别为 7.4、7.2、13.6 和 5.4 个百分点；其中 LogiQA 2.0 表明数学任务训练的归因器在非数学逻辑推理上仍有有限但可测的迁移。

</div>

这项分析只考察首次失败的样本，因而更直接测试归因是否能促成针对性修复。结果支持 HPFA 监督比无监督自我反思产生更可操作的错误信号，也提供了跨域迁移证据；不过 LogiQA 2.0 的绝对成功率仍只有 6.6%，AIME 又使用 Pass@16 而非 Pass@1，不能据此声称已经获得强泛化或直接横向比较各数据集难度。

<div class="result-source" markdown="1">

来源：Section 4.2, Attribution analysis；Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We can see that Ours (SFT + GRPO) consistently outperforms Self-reflection: 19.3% vs. 11.9% on MATH500, 14.3% vs. 7.1% on GSM8K, 22.7% vs. 9.1% on AIME 2024, and 6.6% vs. 1.2% on LogiQA 2.0.

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

- AgentDebug：通过预定义错误分类体系识别根因，并进行反事实测试。它代表依赖错误类型而非配对超图结构的归因方法，用于比较根因定位准确率和计算代价。
- AgenTracer：训练轻量归因器识别根因。在定位实验中，它是学习式归因基线；在测试时推理实验中，作者在相同数据集上采用其数据生成和训练方案，因此用于检验 HPFA 生成的监督信号是否更有效。
- Ours w/o graph：保留成功—失败配对轨迹和反事实验证，仅移除超图引导的候选步骤提取。它是隔离超图结构贡献的关键消融，而非完全独立的方法。
- Vanilla prompting 与 Self-reflection：前者进行无显式失败归因的单次生成，衡量骨干模型的原始任务能力；后者由模型自行指出错误步骤并反思，但不使用 HPFA 监督，用于判断结构化、经反事实验证的归因是否优于模型自我诊断。

**实验想回答的问题**

- 在给定同一问题的一条成功轨迹 $T^+$ 和一条失败轨迹 $T^-$ 时，HPFA 能否比错误分类法、轻量归因器以及无超图的配对方法更准确且更高效地定位真正导致失败的推理步骤？这种优势是否随轨迹长度和依赖复杂度增加而增强？
- 由 HPFA 自动合成的根因归因数据能否训练出可用于测试时反思的归因器 $[0m\pi_\phi$，从而提高数学推理和智能体编程的任务正确率，并迁移到不同推理任务与不同骨干模型？

**实验实现**

失败定位阶段先对每个查询展开目标模型，直到同时得到一条成功轨迹 $T^+$ 和失败轨迹 $T^-$，或达到每题预算 $K=8$；随后建立依赖超图、迭代提炼候选根因，并用统一判定器执行反事实修复展开。数学和编程场景以 Qwen3-8B 生成轨迹及构图，温度为 0.7，最大长度为 8192 tokens；隐私场景的所有大模型组件使用 GPT-4o。定位曲线在第 5 轮后基本稳定，因此表 2 以第 5 轮为代表点，并在图 3 中结合累计墙钟时间比较成本。

测试时推理阶段以 HPFA 从训练集生成包含失败轨迹、根因步骤、解释以及可用反事实片段的样本。数学与编程实验采用 Qwen3-8B，温度为 0、no-think 模式、最大长度 8192 tokens；先用 SFT 训练归因器，再可选用 GRPO 优化。SFT 使用 4 张 NVIDIA A100 80GB、批量 16、AdamW、学习率 $5\times10^{-5}$、5 个 epoch；GRPO 的组大小为 4、每批 4 组、学习率 $2\times10^{-6}$。跨模型实验固定归因器检查点和提示模板，只替换执行反思推理的骨干模型。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除超图候选提取：Ours 对比 Ours w/o graph | 加入超图后，MATH、MBPP、KodCode 的反事实展开验证成功率分别提高 9.7、11.1、18.6 个百分点；对应平均轨迹长度为 $12.4\pm5.8$、$14.0\pm3.2$、$18.2\pm5.5$ 个原子节点。GSM8K 平均仅 $8.2\pm3.2$ 步，超图使结果下降 4.5 个百分点。 | 该消融固定配对轨迹与反事实验证，仅改变是否使用超图，因此较干净地隔离了结构化依赖搜索的贡献。结果表明超图主要服务于候选步骤多、依赖复杂的长轨迹；它不是无条件增益，在短轨迹上构图或裁剪误差可能超过搜索收益。轨迹长度与增益的相关趋势仍不是因果证明，因为四个数据集的任务类型和难度也同时不同。 | Table 3；Section 4.1, When does the hypergraph help?<br><span class="experiment-evidence">Metric GSM8K MATH MBPP KodCode
Traj. Length ± SD 8.2 ± 3.2 12.4 ± 5.8 14.0 ± 3.2 18.2 ± 5.5
∆ gain (%) −4.5 +9.7 +11.1 +18.6</span> |
| 训练目标消融：Ours (SFT) 对比 Ours (SFT + GRPO) | 加入 GRPO 后，MATH500 从 84.2% 升至 84.8%，KodCode 从 46.1% 升至 46.3%，MBPP 从 47.8% 升至 48.4%；GSM8K 则从 93.4% 降至 93.0%。 | 该比较隔离了 SFT 之后强化学习阶段的边际作用。GRPO 在 MATH500 和编程任务上仅增加 0.2 至 0.6 个百分点，并未改善 GSM8K，说明大部分收益已经由 HPFA 合成数据上的监督微调获得；现有数值不足以证明小幅差异具有统计显著性。 | Section 4.2, Main results；数值见 Table 4<br><span class="experiment-evidence">Building upon the SFT stage, GRPO further improves performance on MATH500, KodCode and MBPP.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出基于超图配对分析的推理失败步骤归因方法，并用归因训练提升数学与代码推理准确率。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`e0dac24ec5b36a7587454ba7de002e0d67cc445f165817111ab384dff0aab4d9`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
