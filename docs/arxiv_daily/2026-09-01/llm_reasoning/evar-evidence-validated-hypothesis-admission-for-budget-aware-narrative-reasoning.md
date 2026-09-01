---
title: "[论文解读] EVAR: Evidence-Validated Hypothesis Admission for Budget-Aware Narrative Reasoning"
description: "[arXiv 2608.29835][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.29835"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:55:22.257240+00:00"
source_sha256: "b50d46d5c5ed2f08054c3e0ab7a019249fb4023501ed99e804736d042438e780"
tags:
  - "LLM Reasoning"
  - "幻觉检测"
  - "LLM 其他"
  - "证据约束叙事推理"
  - "假设准入"
  - "源链接原子证据"
  - "测试时推理预算"
  - "证据忠实性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.29835</p>

# EVAR: Evidence-Validated Hypothesis Admission for Budget-Aware Narrative Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Peilin Liu, Zhiquan Ji, Jinglong Ping</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29835v1) · [PDF 下载](https://arxiv.org/pdf/2608.29835v1) · **关键词** 证据约束叙事推理, 假设准入, 源链接原子证据, 测试时推理预算, 证据忠实性<br>


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

原文未明确报告。

**不用术语来说**：原文未明确报告。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 原文未明确报告。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的证据约束推理与长篇叙事推理研究。任务要求模型在不可交互、不能依赖外部检索的长文本中整合分散事件，完成多步判断并生成结论与解释；关键难点不只是答案是否正确，还包括解释中的每个原子主张是否能追溯到故事证据，以及推理过程是否在有限推理预算内完成。EVAR将这一问题视为“假设准入”：模型产生的中间假设只有在封闭的叙事证据库中得到支持后，才能影响最终答案。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**源链接原子证据**

原子证据是从故事中拆出的、表达单一事实或关系的最小信息单元；源链接表示该单元保留其在原文中的出处。这样，模型的后续判断可以回溯到具体文本，而不是只依赖模型生成的概括。

</div>
<div class="concept-item" markdown="1">

**中间假设准入**

中间假设是从已知事实进一步推断出的、尚未成为最终答案的判断。假设准入要求先用证据验证它：有支持的假设进入答案支持状态，无法验证的假设被隔离，和证据冲突的假设被丢弃。

</div>
<div class="concept-item" markdown="1">

**测试时推理预算**

测试时推理预算是针对单个输入分配的额外推理资源，例如允许进行的 refinement 或验证次数。EVAR根据未解决的信息缺口和不确定性动态分配预算，使简单实例直接综合答案，困难实例才进行受控的迭代验证。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一篇非交互式长篇叙事文本，以及由任务规定的问题或推理目标，模型需要输出最终判决、所需任务内容和证据化解释。文本中的决定性前提可能分散在相距很远的事件中，模型不能向用户请求澄清，也不使用外部检索；因此，系统必须在故事内部完成证据编译、缺口识别、候选假设生成、验证和答案综合。EVAR的输入是叙事文本与任务指令，输出是最终答案及其原子主张；其核心假设是，答案支持状态中的中间内容必须能够由锁定的叙事证据库支持，不能由未经验证的生成内容继续传播。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D_{\mathrm{task}}$**

任务数据或待处理的任务实例集合；文中通过不同基准数据集评估模型在多种推理任务上的表现。

</div>
<div class="notation-item" markdown="1">

**$D_{\mathrm{NarraCrime}}$**

本文提出的 NarraCrime 数据集，包含 300 个长篇叙事案件，并按 Easy、Medium 和 Complex 划分难度。

</div>
<div class="notation-item" markdown="1">

**$B_i$**

第 $i$ 个实例的推理预算；文中称其由该实例的未解决缺口和不确定性信号估计得到，用于控制后续 refinement 的规模。

</div>
<div class="notation-item" markdown="1">

**$H$**

候选假设；它针对当前未解决的信息缺口提出可能的中间判断，必须经过与证据库条件化的验证挑战后，才可能更新答案支持状态。

</div>

</div>

**直接相关的工作**

- **Self-Refine 与 Reflexion**: 这类方法通过多轮自我反馈和修订改善输出，但没有可靠外部反馈时，模型未必能纠正事实错误，并会增加额外推理成本。EVAR的差异在于，它不把模型自己的批评直接当作可信反馈，而是要求每个候选假设先与不可变的叙事证据库核验。
- **SABA**: SABA在最终综合前评估前提是否充分，并通过事件—属性对齐状态和查询生成假设；EVAR则强调在实例级预算控制下，对每个候选假设执行假设条件化验证，再决定其是否进入答案支持状态。两者都关注前提充分性，但EVAR进一步区分支持、不可验证和矛盾三种验证结果，并保留源链接原子证据。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在非交互式长篇叙事推理中，关键前提往往分散在相距较远的事件或段落中，模型必须仅依据静态文本整合证据并作出结论。现有大语言模型即使生成了流畅、连贯的答案，也可能把没有文本支持的中间判断带入后续推理，最终产生表面合理但证据不忠实的结论；这会同时损害任务答案的正确性与解释的可信度。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单次提示与局部多步推理**：模型直接读取叙事文本，通过若干局部推理步骤生成中间判断和最终答案，通常依赖自身上下文整合能力来发现分散证据。该类方法适合前提明确、推理链较短的任务，但在长篇叙事中容易过早形成结论。
- **统一深度的自我修订或迭代推理**：模型对初始答案反复检查、重写或扩展推理链，试图通过增加推理步骤来纠正错误。其基本假设是更多修订通常带来更好的结果，但修订过程本身未必受到独立、可靠的文本证据约束。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单次或局部推理可能出现“过早承诺”：模型依据不完整前提形成初始判断，随后围绕该判断进行合理化解释；一旦无支持的中间假设进入推理轨迹，后续推断便可能被其污染，导致答案虽连贯却缺乏来源证据支持。
- 统一深度的自我修订没有根据实例难度分配推理成本，也没有保证每个新假设经过证据验证；在缺少可靠反馈时，额外推理可能不能提升准确率，甚至增加成本或放大原有错误。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法尚未充分解决这样一个具体缺口：如何在长篇叙事中，把分散文本整理为可追溯的原子证据，并让每个会影响最终答案的中间假设先通过来源证据验证，同时依据当前实例的不确定性控制推理预算。换言之，仍缺少一种将证据溯源、假设准入和按难度分配推理成本统一起来的测试时推理机制。

</div>
<div markdown="1"><span>核心问题</span>

对于非交互式长篇叙事，能否建立一种证据约束的测试时推理流程，使模型只允许有文本支持的中间假设进入答案合成状态，将无法验证或与证据矛盾的假设隔离或丢弃，并依据未解决缺口与不确定性决定是否继续推理，从而同时提高任务表现、证据忠实度并控制推理成本？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把中间假设视为需要“准入”的候选状态，而不是默认可信的思维步骤。首先将叙事编译成带来源位置的原子证据存储，并保持其不可修改；随后针对未解决缺口提出候选假设，再构造专门检验该假设的验证问题。只有能够在锁定证据中找到支持的假设才会影响后续答案，无法验证的假设被隔离，与证据冲突的假设被删除。直观上，这相当于为推理链设置证据闸门：模型仍可提出大胆的候选解释，但不能让未经证实的解释继续传播；同时，当已有证据足以回答问题时提前停止，可避免对简单实例进行不必要的反复推理。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

EVAR把长篇叙事推理设计成“先锁定证据，再有限推理，最后受控作答”的流程。输入是固定叙事$X=\{x_i\}_{i=1}^{n}$与目标$G$；系统先把原文拆成带来源位置的原子主张，标记局部不确定性与冲突，并形成不可在后续推理中改写的证据库$\mathcal{B}$。随后，它根据未解决缺口、异常证据数量及冲突严重度计算实例难度$\Gamma$和推理预算$K$：$K=0$时直接从证据库合成答案，$K>0$时进入迭代验证。
在迭代路径中，系统围绕阻碍结论的缺口提出候选假设，并为每个假设分别检查支持证据、反证和仍缺失的必要前提。验证器只能对照锁定的$\mathcal{B}$作出Support、Unknown或Contradict判断；仅Support假设进入可支持答案的历史集合$\mathcal{H}^{+}_{\mathrm{HIST}}$，Unknown被隔离，Contradict被丢弃。循环在缺口消失、状态达到充分性阈值或预算耗尽时停止，最终答案只使用$\mathcal{B}$和已准入假设。直观地说，EVAR不是让模型自由续写一条看似合理的推理链，而是像案件审查一样：先封存卷宗，再给每个推测做证据核验，只有核验通过的内容才能写入结论。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造并锁定来源可追溯的证据库

通过结构化接口$M_{\pi_{\mathrm{ATOM}}}$抽取原文明确表达的原子主张$c_j$及其来源标识$\rho_j$，再附加可由对应片段直接观察到的实体、时间和极性元数据$\eta_j$。系统将证据单元$u_j=(c_j,\rho_j,\eta_j)$与局部一致性标签$\kappa_j$组合为不可变证据库$\mathcal{B}$。

<div class="method-step__io" markdown="1">

**输入**：固定叙事$X=\{x_i\}_{i=1}^{n}$，其中$x_i$是句子或来源片段。<br>
**输出**：锁定证据库$\mathcal{B}=\{(u_j,\kappa_j)\}_{j=1}^{m}$；每项均保留至少一个有效来源标识，并带有OK、Uncertain或Conflict状态及严重度。

</div>

**直观理解**：这一步相当于把长故事拆成一张张带页码的证据卡，后续只能引用这些卡，不能偷偷改写原文。跨片段的因果桥接或人物动机若不是原文明确陈述，就不会在此阶段被当成事实。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 探测推理缺口并分配实例级预算

轻量缺口探测器$M_{\pi_{\mathrm{GAP}}}$生成阻碍可靠结论的前提缺口集合$Z_0$，系统综合缺口数、非OK证据数和严重度得到复杂度$\Gamma$。再由全局上限$B_{\max}$、快速路径阈值$\tau_{\mathrm{fast}}$和预算步长$\tau_{\mathrm{step}}$计算$K$，据此选择FAST或ITER路径。

<div class="method-step__io" markdown="1">

**输入**：锁定证据库$\mathcal{B}$与推理目标$G$。<br>
**输出**：初始缺口集合$Z_0$、复杂度分数$\Gamma$、最大迭代预算$K$及路由$r\in\{\mathrm{FAST},\mathrm{ITER}\}$。

</div>

**直观理解**：证据完整、冲突少的样本无需反复思考；缺口多或材料互相矛盾的样本才获得更多验证轮次。这样把计算量集中在真正困难的故事上，而不是让所有输入都使用固定长度的推理链。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提出假设并构造针对性验证挑战

系统重新识别当前缺口$Z_t$，为所选缺口$z$直接生成候选集合$H_{z,t}$；对每个候选$h$构造支持、反证和必要前提三类验证挑战$V_{h,t}=\{v^{\mathrm{sup}}_{h,t},v^{\mathrm{ctr}}_{h,t},v^{\mathrm{req}}_{h,t}\}$。挑战仅用于规定“该查什么”，被保存在审计历史中，但不作为证据或答案依据。

<div class="method-step__io" markdown="1">

**输入**：迭代状态$S_t=(\mathcal{B},V_{\mathrm{HIST},t},\mathcal{H}^{+}_{\mathrm{HIST},t})$、目标$G$及剩余预算。<br>
**输出**：本轮候选假设集合$H_t$与验证挑战集合$V_t$。

</div>

**直观理解**：模型不是漫无目的地扩写故事，而是针对一个卡住结论的问题提出少量可检验猜测。随后像交叉询问一样同时寻找赞成材料、反对材料以及尚未满足的前提，避免只挑支持自身猜测的内容。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 验证准入、停止判断与答案合成

验证器$M_{\pi_{\mathrm{VER}}}$仅依据$\mathcal{B}$为每个$h$输出标签$\ell(h)$及支持证据$E_h$；Support进入$\mathcal{H}^{+}$，Unknown进入隔离区，Contradict被丢弃。状态更新后，若$Z_t=\varnothing$、充分性分数$\sigma_{t+1}\geq\tau_{\mathrm{SUF}}$或预算耗尽，则从终态$S^{\mathrm{ans}}_{t^\star}=(\mathcal{B},\mathcal{H}^{+}_{\mathrm{HIST},t^\star})$合成答案。

<div class="method-step__io" markdown="1">

**输入**：候选假设$H_t$、挑战$V_t$、锁定证据库$\mathcal{B}$和当前状态$S_t$。<br>
**输出**：NarraCrime任务输出答案$\hat{y}$及来源信息$p$；公共基准只请求并评估文本答案$\hat{y}$。

</div>

**直观理解**：只有能指向封存证据的猜测才会获得“进入结论”的通行证；暂时无法证明的猜测即使听起来合理，也只能隔离。最终写答案时不向模型展示验证问题、被隔离假设或矛盾假设，从结构上减少这些内容泄漏进结论。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 复杂度驱动的实例级推理预算

$$
\Gamma=\alpha_1|Z_0|+\alpha_2\sum_{j=1}^{m}\mathbb{I}\{\mathrm{status}_j\neq\mathrm{OK}\}+\alpha_3\sum_{j=1}^{m}\mathrm{sev}_j,\qquad K=\min\!\left(B_{\max},\max\!\left(0,\left\lceil\frac{\Gamma-\tau_{\mathrm{fast}}}{\tau_{\mathrm{step}}}\right\rceil\right)\right)
$$

**符号说明**

- $\Gamma$：当前实例的综合复杂度分数。
- $Z_0$：第一次缺口探测得到的未解决前提集合，绝对值表示缺口数量。
- $\alpha_1,\alpha_2,\alpha_3$：分别控制缺口数、异常证据数和异常严重度贡献的权重。
- $m$：证据单元总数。
- $\mathbb{I}\{\mathrm{status}_j\neq\mathrm{OK}\}$：指示函数；第j个证据单元为Uncertain或Conflict时取1，否则取0。
- $\mathrm{sev}_j$：第j个证据单元的一致性问题严重度，取值为0、1、2或3。
- $K$：分配给该实例的细化迭代预算；为0时走快速路径。
- $B_{\max}$：所有实例共同遵守的预算上限。
- $\tau_{\mathrm{fast}}$：决定实例是否可绕过细化的复杂度阈值。
- $\tau_{\mathrm{step}}$：复杂度每增加多少就增加一个预算单位的步长参数。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分把三类困难信号相加：还缺多少关键前提、有多少证据带风险标签、这些风险有多严重。第二部分将超过快速阈值的复杂度按步长换算成整数轮次，并限制在$0$到$B_{\max}$之间，因此简单样本可不迭代，困难样本也不会无限推理。<br>
**原文位置**：第3.3节，公式(8)–(10)

</div>

</div>

<div class="equation-block" markdown="1">

#### 证据验证与严格假设准入

$$
(\ell(h),E_h)\leftarrow M_{\pi_{\mathrm{VER}}}(h,V_{h,t},\mathcal{B}),\quad \ell(h)\in\{\mathrm{Support},\mathrm{Unknown},\mathrm{Contradict}\};\qquad \mathcal{H}^{+}_{t}=\{(h,E_h)\mid h\in H_t,\ell(h)=\mathrm{Support}\},\quad E_h\subseteq\mathcal{B}
$$

**符号说明**

- $h$：针对某个未解决缺口提出的候选假设。
- $V_{h,t}$：第t轮围绕假设h构造的支持、反证与必要前提验证挑战。
- $\mathcal{B}$：不可变且保留来源链接的基础证据库。
- $M_{\pi_{\mathrm{VER}}}$：采用结构化验证接口的语言模型操作符。
- $\ell(h)$：假设的验证标签：有证据支持、证据不足或与证据矛盾。
- $E_h$：验证器为假设h定位的支持证据单元集合，必须是证据库的子集。
- $H_t$：第t轮产生的全部候选假设集合。
- $\mathcal{H}^{+}_{t}$：第t轮通过验证、可加入答案支持状态的假设及其证据。

<div class="equation-explanation" markdown="1">

**直观理解**：验证器不能因为假设语义连贯就放行，而必须返回锁定证据库中的具体支持项。集合构造式把Support作为唯一准入条件；Unknown假设进入隔离区，Contradict假设被丢弃，因此二者均不能成为最终答案的前提。<br>
**原文位置**：第3.3节，公式(15)–(18)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。所给方法章节没有提出参数训练、监督损失或奖励函数；$M_\pi(\cdot)$表示同一类LLM在不同提示和约束输出接口$\pi$下执行原子化、标签、缺口探测、假设生成、验证、充分性判断与答案合成。因而公式中的复杂度、预算和准入规则属于推理时控制机制，不应解释为通过梯度优化学习的目标；原文也未明确报告是否对底层模型进行额外微调。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 不可变证据库**

证据库以$\mathcal{B}=\{(u_j,\kappa_j)\}_{j=1}^{m}$保存原子主张、来源集合、可观察元数据和局部一致性标签。非连续片段不会被预先合并成重构事件，后续假设验证与答案生成均以同一锁定版本为参照。

> 直观理解：它解决的是“推理过程中把模型自己的补充误当成原文事实”的问题。保留来源位置还能追查每个结论究竟依赖故事中的哪一段，但一致性标签本身只提示风险，不会自动裁定整个故事真假。

**2. 预算感知路由器**

路由器先以$Z_0$描述尚未满足的关键前提，再把缺口、不确定或冲突证据的数量及严重度压缩为$\Gamma$，最后映射为有上限的整数预算$K$。$K=0$直接执行快速答案合成，$K>0$才启用验证门控的迭代细化。

> 直观理解：这一模块控制“值得再想几轮”，而不是判断答案内容本身。其价值在于使推理成本可预测，并通过充分性提前停止避免已经有足够证据后继续生成新猜测。

**3. 验证门控的假设准入器**

准入器将候选的验证结果分成Support、Unknown和Contradict，并要求Support假设携带$E_h\subseteq\mathcal{B}$。挑战历史$V_{\mathrm{HIST},t}$可用于审计和避免重复，但答案支持状态只包含$\mathcal{B}$与此前获准的$\mathcal{H}^{+}_{\mathrm{HIST},t}$。

> 直观理解：普通链式推理一旦在中间步骤猜错，错误就可能被下一步当作前提；这里在状态入口设置闸门。Unknown与Contradict分开处理也很重要：前者表示证据不足，不能误判成已证伪；后者才表示与锁定材料相冲突。

**训练与推理**

训练过程：原文未明确报告独立训练阶段，也没有给出可优化损失。推理过程：首先对$X$进行一次证据原子化和来源绑定，只保留原文明确表达的主张；随后附加实体、时间、极性元数据以及局部一致性状态，得到锁定的$\mathcal{B}$。系统针对$G$探测$Z_0$，计算$\Gamma$和$K$；若$K=0$，直接用$\mathcal{B}$快速合成答案。若$K>0$，则在每轮$t$重新探测阻塞缺口、选择缺口、生成候选、构造三类验证挑战，并仅对照$\mathcal{B}$验证。通过者累积进$\mathcal{H}^{+}_{\mathrm{HIST},t}$，无法验证者和矛盾者分别隔离或丢弃；系统持续检查缺口、充分性和预算。终止后，答案接口只能接收$S^{\mathrm{ans}}_{t^\star}=(\mathcal{B},\mathcal{H}^{+}_{\mathrm{HIST},t^\star})$，不能使用挑战历史或未获准假设。

**复现信息**

公平复现至少需要固定各结构化接口$\pi_{\mathrm{ATOM}}$、$\pi_{\mathrm{TAG}}$、$\pi_{\mathrm{GAP}}$、$\pi_{\mathrm{HYP}}$、$\pi_{\mathrm{CHAL}}$、$\pi_{\mathrm{VER}}$、$\pi_{\mathrm{SUF}}$和$\pi_{\mathrm{ANS}}$的提示模板及输出字段，并强制每个$c_j$至少保留一个有效$\rho_j$。还需报告或固定预算参数$\alpha_1$、$\alpha_2$、$\alpha_3$、$B_{\max}$、$\tau_{\mathrm{fast}}$、$\tau_{\mathrm{step}}$和充分性阈值$\tau_{\mathrm{SUF}}$；但所给章节未提供这些参数的具体数值。实现时必须保持$\mathcal{B}$不可变，禁止把验证挑战、Unknown假设或Contradict假设送入答案合成；NarraCrime接口返回$\hat{y}$与来源$p$，公共基准仅返回$\hat{y}$。底层模型版本、采样参数、每个缺口的候选数量及具体停止时的预算计数方式在所给原文中未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- NarraCrime：非交互长篇叙事基准，共 $300$ 个案例，分为 Easy、Medium、Complex 三个各含 $100$ 个案例的难度划分；平均故事长度分别为 $863.5$、$1065.2$ 和 $1413.4$ 个词，平均证据线索为 $8.7$、$10.9$ 和 $13.4$ 条。每个案例含一个主要罪犯以及零个或多个已确认共犯，用于测试跨事件叙事推理、角色区分和证据覆盖。
- HotpotQA（HQA）：公共多跳问答基准，使用 Answer exact match（Ans）和 Supporting-Fact F1（SF），用于测试答案正确性及支持事实恢复；原文未明确报告本次评测所使用的样本规模或划分。
- StrategyQA（SQA）与 BBH：SQA 使用官方数据集全部 $2,780$ 个例子，测试需要多步常识推理的问题；BBH 在全部 $23$ 个任务上报告宏平均准确率，用于检验方法是否能从叙事任务推广到多种公共推理任务。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Role-Aware Verdict Score（RVS）**

对每个候选对象输出的概率分布进行评分；主要罪犯获得完整信用，已确认共犯获得 $[1;31m\lambda=0.5[0m$ 的部分信用，其他候选人不获得信用。其核心形式为 $s_i(p_i)=\sum_{e\in R_i^{\mathrm{cul}}}p_i(e)+\lambda\sum_{e\in R_i^{\mathrm{acc}}}p_i(e)$，并对 $N$ 个实例取平均，即 $\mathrm{RVS}=\frac{1}{N}\sum_{i=1}^{N}s_i(p_i)$；它衡量角色感知的最终判决质量。 （越高越好，因为更多概率质量被分配给真实罪犯或共犯。）

</div>
<div class="metric-item" markdown="1">

**Evidence Coverage（EC）**

将预测出的证据命题集合与参考证据命题集合进行语义匹配，再用匹配到的参考命题数除以参考命题总数，即 $\mathrm{EC}=\mathrm{Recall}(\hat{P}_E,P_E)$；它衡量答案覆盖了多少标注支持证据。 （越高越好，表示恢复了更多参考证据；它不等同于所有生成内容都真实，因为覆盖率不直接惩罚额外的无依据陈述。）

</div>
<div class="metric-item" markdown="1">

**Unsupported Claim Rate（UCR）**

先把最终答案拆成原子陈述，并将每条陈述标记为 Support、Unknown 或 Contradict；UCR 统计 Unknown 与 Contradict 陈述在全部陈述中的比例，即 $\mathrm{UCR}=\frac{\sum_i|\{c\in\hat{C}_i:\ell(c)\in\{\mathrm{Unknown},\mathrm{Contradict}\}\}|}{\sum_i|\hat{C}_i|}$。它衡量最终答案中未被证据支持的内容比例。 （越低越好；矛盾陈述同时计入 UCR，因此 UCR 与 Contradiction Rate 不是互斥指标。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### NarraCrime 三个难度划分及统一 DeepSeek-V3.2 骨干模型

<div class="result-value" markdown="1">

EVAR 在所有 NarraCrime 划分上取得最高的 RVS 和 EC。Complex 上 EVAR 的 RVS 为 $78.6$、EC 为 $83.3$；GoT 分别为 $69.6$ 和 $77.6$。Easy 上 EVAR 达到 RVS $85.9$、EC $93.5$。

</div>

这说明在故事更长、证据更分散且跨事件推理更复杂时，EVAR 的角色判决和证据恢复仍然较强；相对 GoT，Complex 上的提升表明锁定证据并验证中间假设可能比单纯扩大搜索更有效。但这些结果只证明在所选数据集、骨干模型和自动评测协议下的优势，不能单独证明每条中间推理都被人工核验。

<div class="result-source" markdown="1">

来源：Section 4.4 Main Results；Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On NarraCrime, EV AR improves both role-aware verdict quality and task-content recovery metrics across all splits, with the largest gains on NarraCrime-Complex: compared with GoT and SELF-DISC., RVS increases to78.6 from 69.6 and 68.0, respectively, while EC increases to83.3 from 77.6 and 76.3.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### HotpotQA、StrategyQA 和 BBH 的公共推理任务泛化

<div class="result-value" markdown="1">

EVAR 在 HQA 上取得 Ans $78.2$、SF $74.1$，高于最强基线 GoT 的 $76.6$ 和 $72.7$；在 SQA 和 BBH 上分别达到准确率 $94.1$ 和 $93.6$。

</div>

这表明 EVAR 的证据验证与预算控制并不只适用于罪犯识别，也能迁移到多跳问答、常识推理和多任务推理。不过，不同公共基准的任务定义和指标不同，不能把这些分数直接与 NarraCrime 的 RVS 或 EC 比较；同时，原文未在该段报告各公共基准的完整方差或所有基线细节。

<div class="result-source" markdown="1">

来源：Section 4.4 Main Results；Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On public reasoning benchmarks, EV AR also generalizes well. On HQA, it achieves 78.2 Ans and 74.1 SF, compared with76.6 and 72.7 from the strongest baseline (GoT), corresponding to relative gains of 2.1% and 1.9%, respectively. On SQA and BBH, EV AR reaches94.1 and 93.6, corresponding to relative gains of 1.3% and 3.2%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### NarraCrime-Complex 上的推理成本与性能联合比较

<div class="result-value" markdown="1">

EVAR 在 NarraCrime-Complex 上的平均 LLM 调用次数为 $T=15.8$，GoT 为 $T=35.5$；相较 GoT，原文报告成本下降 $55.5\%$。EVAR 同时在该划分取得 RVS $78.6$ 和 EC $83.3$。

</div>

该结果支持“性能提升并非单纯依靠更多调用”的解释：EVAR 通过实例级预算路由和充分性停止，把更多计算留给困难实例，并在达到足够证据后停止。然而，$T$ 是平均调用次数而非真实金钱、延迟或能耗；因此它证明的是调用级成本可控，不是完整部署成本一定更低。

<div class="result-source" markdown="1">

来源：Section 4.4 Main Results；Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Moreover, on NarraCrime-Complex, compared with GoT (T= 35.5), EV AR reduces inference cost toT= 15.8 ,a55.5%reduction.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- NarraCrime 的 IR、ASR、EC、UCR 和 CR 依赖 GPT-5.5 自动执行命题抽取、原子分解和证据状态标注，且“没有人工裁决”；因此对证据忠实性的结论受评判模型、提示词和证据标注质量影响。
- 实验主要以 DeepSeek-V3.2 为骨干模型，虽然原文称附录报告了额外骨干模型的鲁棒性结果，但所给章节未提供这些结果的具体数值；同时，成本 $T$ 只统计平均 LLM 调用次数，未覆盖真实价格、延迟、上下文长度或硬件资源。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Direct：直接回答，不显式展开推理，用来提供最低复杂度的性能参照。
- CoT：链式思维提示，代表顺序生成中间推理的常见方法，用于检验 EVAR 是否超越基础推理提示。
- Self-Refine 与 SELF-DISC.：基于自反馈或自我反思的迭代方法，用来比较一般性的自我修正是否足以解决证据污染问题。
- GoT：图式或轨迹搜索式推理方法，是主要的强推理基线，用于比较结构化搜索在性能和成本上的差异。

**实验想回答的问题**

- 在长篇、非交互叙事中，EVAR 是否能同时提高角色判断、证据覆盖与公共推理任务性能，并降低最终答案中的无依据陈述？
- 证据存储、验证门控、预算路由和基于充分性的提前停止，分别是否改善性能、证据忠实性与推理成本？

**实验实现**

主实验统一使用 DeepSeek-V3.2 作为骨干模型，所有方法接收相同输入并遵循统一协议。NarraCrime 的最终输出必须包含文本答案和覆盖固定候选集的候选人概率映射，概率非负且总和为 $1$；不使用供应商特定的 token 对数概率。确定性方法使用贪心解码、temperature=$0$、top-p=$1.0$、最大输出长度 $512$ 个 token；随机基线使用非零温度和随机种子 $42$、$44$、$46$。结果通常为三次独立运行的均值；表 2 的任务指标报告均值±标准差，而 $T$ 表示每个 NarraCrime-Complex 实例平均调用 LLM 的次数。EVAR 的全局预算上限在成本实验中取 $B_{\max}\in\{0,1,2,3,4\}$，并通过提前停止避免不必要的 refinement。NarraCrime 的命题抽取、原子分解和证据状态标注由 GPT-5.5 自动完成，且没有人工裁决。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| NarraCrime-Complex 与 StrategyQA 的组件消融：完整 EVAR、w/o Admission、w/o Evidence Store、w/o Budget Routing 和 CoT | 完整 EVAR 的 RVS、EC、UCR 和 SQA 准确率为 $78.6$、$83.3$、$8.6$ 和 $94.1$。去除 Admission 后为 $71.5$、$74.4$、$17.8$ 和 $90.5$；去除 Evidence Store 后为 $70.3$、$72.5$、$19.4$ 和 $83.2$；去除 Budget Routing 后为 $62.9$、$64.7$、$21.7$ 和 $77.5$。 | Admission 消融测试验证器是否真正阻止无支持假设进入活动状态；UCR 从 $8.6$ 升至 $17.8$，支持其对抑制无依据陈述的作用。Evidence Store 消融测试固定、结构化证据基础的重要性；Budget Routing 消融的下降最大，说明统一或不区分实例难度地分配计算会损害性能。CoT 的 RVS 为 $46.0$、UCR 为 $28.4$，提供了基础提示参照，但单次消融不能区分提示格式、调用次数和搜索结构的所有潜在影响。 | Section 5.1 Ablation Study；Table 3<br><span class="experiment-evidence">Variant RVS EC UCR↓SQA
EV AR 78.6 83.3 8.6 94.1
w/o Admission 71.5 74.4 17.8 90.5
w/o Evidence Store 70.3 72.5 19.4 83.2
w/o Budget Routing 62.9 64.7 21.7 77.5
CoT 46.0 61.6 28.4 86.9</span> |
| NarraCrime-Complex 的证据忠实性比较：Direct、CoT、Self-Refine、GoT 与 EVAR | EVAR 的 RVS 为 $78.6$、EC 为 $83.3$、UCR 为 $8.6$、CR 为 $3.8$；GoT 为 $69.6$、$77.6$、$15.9$、$7.4$，Direct 为 $40.1$、$59.4$、$31.6$、$14.2$。 | EVAR 不仅恢复更多目标证据，还减少最终答案中未知或矛盾的原子陈述；这与“先验证、再允许中间假设影响后续推理”的设计一致。由于这些标签由 GPT-5.5 自动生成且没有人工裁决，结果支持自动评测意义下的证据忠实性改善，但不能排除评判模型或证据标注带来的误差。 | Section 5.2 Hypothesis Admission and Evidence Faithfulness；Table 4<br><span class="experiment-evidence">EV AR 78.6 83.3 8.6 3.8</span> |

**定性案例**

- 原文未提供具体实例级定性案例；其补充分析仅报告“EV AR assigns iterative refinement more frequently to harder instances”，因此不能据此编造某个故事中的推理过程或错误修正案例。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出通过证据验证和隔离不支持假设来提升长文本推理可靠性的框架，核心涉及推理过程控制与幻觉抑制。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`b50d46d5c5ed2f08054c3e0ab7a019249fb4023501ed99e804736d042438e780`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
