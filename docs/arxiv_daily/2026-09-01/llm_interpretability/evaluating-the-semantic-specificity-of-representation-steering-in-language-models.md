---
title: "[论文解读] Evaluating the Semantic Specificity of Representation Steering in Language Models"
description: "[arXiv 2608.29431][LLM 机制与可解释性] 原文未明确报告。"
arxiv_id: "2608.29431"
announcement_date: "2026-09-01"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:56:59.642126+00:00"
source_sha256: "41a4eb8969d0fb54dd2169c63b1924974d18f3cb662e3c03665ed76c6c55c69a"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "机制可解释性"
  - "表示操控"
  - "激活操控"
  - "逻辑推理"
  - "矛盾盲视"
  - "跨规则迁移"
  - "标签偏置"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2608.29431</p>

# Evaluating the Semantic Specificity of Representation Steering in Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Zhangdie Yuan, Andreas Vlachos</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Cambridge</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29431v1) · [PDF 下载](https://arxiv.org/pdf/2608.29431v1) · **关键词** 大语言模型, 机制可解释性, 表示操控, 激活操控, 逻辑推理, 矛盾盲视, 跨规则迁移, 标签偏置<br>
**项目页**: [https://huggingface.co/datasets/MoyYuan/Asymmetricity-2.0](https://huggingface.co/datasets/MoyYuan/Asymmetricity-2.0)

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

本文位于大语言模型的机制可解释性与表示操控研究交叉领域。表示操控通过在模型中间层激活上注入向量来改变生成行为，通常无需修改模型参数；本文关注其是否真正修复了逻辑推理机制，而不是仅通过改变最终输出标签来提高基准准确率。具体而言，研究对象是用于纠正“矛盾盲视”的后层局部表示操控（Localized Representation Steering，LRS）：模型原本擅长正向蕴含，却难以识别矛盾。论文提出跨规则迁移（Cross-Rule Transfer，CRT），把操控向量同时施加到模型原本已经解决的同一逻辑领域规则上，以检验原有能力是否保持不变。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**表示操控与操控向量**

表示操控是在模型生成过程中修改中间层隐藏状态；操控向量通常由不同条件下的激活差异构造，并在指定层加入隐藏状态。直观地说，它像是在模型内部施加一个方向性的“提示”，促使模型倾向于某种行为，而不必更新模型权重。

</div>
<div class="concept-item" markdown="1">

**矛盾盲视与规则推理**

给定前提 $P$ 和假设 $H$，模型需要判断 $H$ 是否由 $P$ 蕴含，或是否与 $P$ 矛盾。本文所说的矛盾盲视，是模型能够处理正向蕴含，却系统性地无法识别矛盾关系。

</div>
<div class="concept-item" markdown="1">

**标签偏置与机制修复**

标签偏置是直接提高某个输出标签的得分，使模型看起来更常预测该标签，但不代表其内部重新执行了正确推理。真正的机制修复应当改善目标失败规则，同时保留模型在其他同领域规则上的原有能力；若后者显著下降，则更可能是全局标签覆盖。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是由前提与假设组成的逻辑样本 $x=(P,H)$，输出是词汇表 $V$ 中对应逻辑标签的预测，例如蕴含或矛盾。模型先在早期和中间层提取语义，再在指定的后层 $L_d$ 注入操控向量，最后通过层归一化和非嵌入矩阵得到输出词元的 logits。论文的核心假设是：如果 LRS 修复了矛盾推理电路，那么它在目标失败规则上应提升性能，并在模型原本熟练的结构不同规则上保持性能；如果它只是注入与标签相关的全局偏置，则会把熟练规则中的正确预测也推向目标标签。CRT 因而要求在共享同一标签空间、但规则结构彼此分离的规则族之间进行测试，而不能只依赖目标基准上的总体准确率。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x=(P,H)$**

一个逻辑推理输入，其中 $P$ 表示前提集合，$H$ 表示待判断的假设。

</div>
<div class="notation-item" markdown="1">

**$L_d$**

进行表示操控的指定层，本文重点考察后层操控。

</div>
<div class="notation-item" markdown="1">

**$h_{L_d}$**

输入 $x$ 在操控层 $L_d$ 的隐藏状态表示。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{v}$**

学习得到的表示操控向量，被加入 $h_{L_d}$ 以改变模型行为。

</div>

</div>

**直接相关的工作**

- **Zou et al. (2023)；Turner et al. (2023) 的表示工程与激活操控**: 这些工作奠定了通过向中间层激活注入向量来改变大语言模型行为的方法基础。本文继承这一范式，但进一步审计操控向量究竟编码了语义推理方向，还是仅编码了与输出标签相关的偏置。
- **McCoy et al. (2019) 关于自然语言推理中的表面捷径**: 该工作说明高基准准确率可能来自词汇或模板线索，而非真正的结构推理。本文将这一评价风险扩展到表示操控场景，并用同一逻辑领域中模型原本熟练的规则族检验所谓的推理修复。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

机制可解释性研究不仅要让大语言模型在基准测试中得分提高，还要确认干预确实修复了内部推理机制。局部表征引导（Localized Representation Steering，LRS）通过在生成过程中注入学习到的激活差分向量，已被用于处理模型的逻辑推理缺陷；但如果它只是把输出强行推向某个标签，那么表面上的准确率提升会错误地被解释为推理回路修复。该问题直接影响模型编辑和机制解释结论的可信度。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **局部表征引导（LRS）**：从对比样本的内部激活中学习 steering vector，并在指定层注入该向量，使模型在目标任务上改变后续表示和输出。本文关注的是晚层 LRS：由于晚层表示距离词表输出较近，注入向量可能直接改变标签词的 logits，而不必改变前面的逻辑计算。
- **基准测试与模型编辑审计**：通过目标任务准确率或下游任务表现判断干预是否成功；相关模型编辑审计则进一步考察更新是否仅表现为局部的 logit 开关。此类方法通常围绕被修复的失败样例评估干预，较少检验它在模型原本已经擅长、且结构上不同的规则上的行为。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 仅在目标失败规则上观察准确率，无法区分真正的推理回路修复与全局标签偏置。本文所述矛盾检测案例中，晚层 LRS 可将目标基准准确率恢复到 100%，但在模型原本擅长的蕴含规则上，准确率由 99.6% 降至 40.4%；原文将这一现象概括为“degrades performance to 40.4% by forcing false contradiction predictions”（Abstract）。其后果是，模型可能只是被强制输出“矛盾”标签，却被误判为获得了逻辑能力。
- 现有评估缺少对干预语义特异性的系统性反事实检查：如果一个向量只编码标签方向，它应当能够迁移到不相关规则并破坏原有能力；如果它修复的是特定推理机制，则应保留这些规则上的原生能力。没有这种跨规则检验，也难以排除直接 logit 偏置、标签翻转方向或模型间可迁移的表面效应。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚未解决的缺口是：缺少一种与具体模型和目标任务相对独立的诊断协议，能够利用模型在结构上不相关、但原本已具备能力的规则族，检验表征干预究竟改变了规则推理过程，还是仅注入了与标签相关的输出偏置。本文以 Cross-Rule Transfer（CRT）填补这一缺口：将学得的干预向量转移到模型原生擅长的规则上，要求真实修复保留原有能力；若出现系统性的错误标签预测，则说明干预更可能是表面覆盖。

</div>
<div markdown="1"><span>核心问题</span>

对于用于修复矛盾盲视的晚层 LRS，其性能提升是否来自对逻辑推理回路的真实修复，还是来自能够跨规则强制改变输出标签的全局 logit 偏置？

</div>
<div markdown="1"><span>作者直觉</span>

关键直觉是把干预带到它“不该需要帮助”的地方。若向量修复了特定的矛盾判断机制，那么在模型已经正确处理的蕴含规则上，它应当基本不影响原有判断；反之，若向量主要编码“输出矛盾”这一标签方向，那么无论输入规则的真实关系是什么，它都会推动模型选择矛盾标签，从而显著损害原生能力。CRT 正是把这种预期差异转化为可观测的跨规则反事实测试；原文称其目标是检验干预是否“corrected a logical circuit or merely injected a global output bias”（Introduction）。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文的方法不是提出一种新的表示干预，而是审计标准局部表示引导（Localized Representation Steering, LRS）究竟修复了逻辑推理，还是仅在输出端强迫模型选择目标标签。完整流程先用跨层线性探针定位与“矛盾盲视”相关的晚层表示变化，再以成功样本和失败样本在目标层的平均激活差构造引导向量；随后分别在源任务和模型原本擅长的其他规则族上注入该向量，并通过 Cross-Rule Transfer（CRT）观察原生能力是否受损。若干预能恢复矛盾识别且保持原本正确的蕴含判断，才支持“推理回路修复”；若大量正确蕴含被改成“contradiction”，则判为表面标签偏置。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 定位候选干预层

在早层激活上训练二元线性探针，再将其跨层应用到晚层，通过跨层错误率识别读出几何发生显著漂移的区域；层区间按归一化深度划分为前 $20\%$ 的早层、中间 $40\%$ 和最后 $40\%$ 的晚层。探针预测的是行为成功与否而非真正的逻辑语义，因此作者明确将其视为代理定位信号。

<div class="method-step__io" markdown="1">

**输入**：各模型在逻辑规则样本上的中间层激活，以及每次预测的行为结果标签“正确/错误”。<br>
**输出**：每个模型的候选目标层：Llama 为第 $13/16$ 层、Gemma 为第 $21/26$ 层、Qwen 为第 $32/40$ 层、DeepSeek 为第 $26/32$ 层。

</div>

**直观理解**：这一步类似先寻找“正确与错误案例在哪里开始分道扬镳”，但不能据此断言找到了推理回路，因为探针也可能只读到了模型准备输出哪个标签。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造并注入 LRS 向量

分别计算成功与失败样本的平均隐藏激活并取差，得到方向 $\mathbf{v}$；生成时将归一化后的 $\mathbf{v}$ 以强度 $\alpha$ 加到最终预测 token 在目标层的隐藏状态。主要设置使用 $\alpha=1.5$，源任务上还采用仅对矛盾规则族触发干预的 oracle 门控作为理想化上界。

<div class="method-step__io" markdown="1">

**输入**：目标层 $L$ 上行为成功集合 $S_{\text{success}}$ 与失败集合 $S_{\text{fail}}$ 的上下文序列激活。<br>
**输出**：经过干预的隐藏状态及其最终生成标签，并得到门控和无条件注入两种运行模式。

</div>

**直观理解**：平均差向量相当于从大量案例中寻找一条“从失败走向成功”的方向，再把模型当前状态沿该方向推一下；问题在于成功与失败几乎也分别对应不同输出标签，所以这条方向可能只是“更想输出 contradiction”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行 Cross-Rule Transfer 审计

先从 $D$ 中选出基线准确率至少为 $95\%$ 的原生胜任子集 $F_{\text{comp}}$，再取消 oracle 门控，将 $\mathbf{v}$ 无条件注入这些样本。比较干预前后准确率、被错误注入的目标标签数量，并对成对预测差异使用 McNemar 检验。

<div class="method-step__io" markdown="1">

**输入**：未干预模型 $M$、评价规则族集合 $D$、引导向量 $\mathbf{v}$，以及模型原本高准确率处理的规则族。<br>
**输出**：干预后的原生能力保持率、错误目标标签注入数及诊断分类：保持高准确率支持广义推理修复，显著退化且错误由目标标签主导则支持标签偏置覆盖。

</div>

**直观理解**：CRT 不问干预能否在原来的错题上“把答案改对”，而是把它放到模型本来会做的相关题目上；真正修好的推理能力不应把这些正确答案系统性改错。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 用机制对照检验诊断

将 LRS 与直接给目标标签增加常数 logit 的 DLB 对比，并分别限制注入发生在最终标签 token 或此前的思维链 token；同时测试早层注入、随机或正交扰动、成功/失败标签打乱，以及通过线性映射完成的跨模型向量移植。若 LRS 与 DLB 输出一致、仅最终 token 注入有效且标签方向可跨模型移植，则其作用更符合输出承诺覆盖而非推理轨迹改变。

<div class="method-step__io" markdown="1">

**输入**：LRS 的预测结果，以及直接 logit 偏置、早层向量、打乱对比标签所得向量和跨模型投影后的向量。<br>
**输出**：关于向量语义特异性的互补证据，包括功能等价性、token 位置依赖、层位置依赖、方向特异性和跨架构可迁移性。

</div>

**直观理解**：这些对照相当于从不同角度追问“模型是真的重新推理了吗”：若只在写最终答案时推一下就能达到全部效果，而且直接给某个答案加分也完全一样，那么更可能只是改了答题按钮。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 成功—失败均值差引导向量

$$
\mathbf{v}=\frac{1}{|S_{\text{success}}|}\sum_{i\in S_{\text{success}}}\mathbf{h}_{i}^{(L)}-\frac{1}{|S_{\text{fail}}|}\sum_{j\in S_{\text{fail}}}\mathbf{h}_{j}^{(L)}
$$

**符号说明**

- $\mathbf{v}$：用于表示引导的方向向量。
- $S_{\text{success}}$：模型行为预测正确的上下文序列集合。
- $S_{\text{fail}}$：模型行为预测错误的上下文序列集合。
- $\mathbf{h}_{i}^{(L)}$：成功样本 i 在目标层 L 的隐藏激活。
- $\mathbf{h}_{j}^{(L)}$：失败样本 j 在目标层 L 的隐藏激活。
- $|S|$：集合 S 中的样本数量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把所有成功案例的平均表示减去所有失败案例的平均表示，期望获得与成功行为相关的方向。但本文设置中成功/失败与 entailment/contradiction 标签高度混淆，因此该差向量在数学上容易同时编码输出标签偏好，而不是纯粹的推理特征。<br>
**原文位置**：式 (1)，第 4.2 节 Steering Vector Construction

</div>

</div>

<div class="equation-block" markdown="1">

#### 推理时归一化表示注入

$$
\mathbf{h}_{t}^{(L)}\leftarrow\mathbf{h}_{t}^{(L)}+\alpha\frac{\mathbf{v}}{\|\mathbf{v}\|_{2}}
$$

**符号说明**

- $\mathbf{h}_{t}^{(L)}$：生成位置 t 在目标层 L 的隐藏状态。
- $\alpha$：控制干预幅度的缩放系数，主要实验设置为 1.5。
- $\mathbf{v}$：由成功与失败样本均值差得到的引导向量。
- $\|\mathbf{v}\|_{2}$：引导向量的欧氏范数，用于消除向量原始长度对干预强度的影响。
- $t$：自回归生成中的 token 位置。
- $L$：实施表示干预的目标 Transformer 层。

<div class="equation-explanation" markdown="1">

**直观理解**：先把方向向量标准化，再按 $\alpha$ 指定的固定步长加到隐藏状态中，使不同模型或数据所得向量的长度不会直接决定干预强弱。作者进一步比较不同 $\alpha$，并检查只干预最终标签 token 与只干预此前推理 token 的差异，以判断作用发生在推理过程还是输出提交阶段。<br>
**原文位置**：式 (2)，第 4.2 节 Steering Vector Construction

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文没有对基础语言模型进行参数训练，也没有提出需要梯度优化的新损失函数。线性探针仅以中间激活为输入、行为正确/错误为监督信号进行二分类拟合；标准 LRS 向量则直接由两组激活的样本均值差计算，不通过反向传播优化。跨模型移植对照额外使用带 $L_2$ 正则的普通最小二乘拟合线性投影 $W$，其目的只是把 Llama 的 $2048$ 维方向映射到 Qwen 的 $3584$ 维空间，而非训练模型的推理能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 跨层代理定位**

探针在早层表示上训练、在晚层表示上测试。二分类错误率显著高于 $50\%$ 被解释为跨层转移下的系统性反相关或读出几何失配，但潜在空间协变量偏移和晚层表示压缩也可能导致探针退化，因此该模块只确定候选干预区域，不将可解码性直接等同于因果推理机制。

> 直观理解：探针像一把在早层校准的尺子；到晚层后它若不仅失准而且经常给出相反判断，说明表示组织方式发生了一致变化，但不能仅凭这把尺子证明那里保存着真正的逻辑规则。

**2. Cross-Rule Transfer 判别器**

CRT 以原生胜任规则族 $F_{\text{comp}}$ 作为反事实保护集，而不是只考察目标失败分布上的恢复率。论文建议以干预后准确率仍至少为 $95\%$ 作为广义修复的操作性标准；若准确率显著下降且新增错误集中为目标标签，则分类为 superficial label bias override。

> 直观理解：普通分布外测试主要检查修复能否推广到同类新题，CRT 则专门尝试证伪：它检查修复工具会不会在不该动手的地方，把模型原来会做的题强行改成同一个答案。

**3. 标签偏置等价与因果对照**

最终预测由隐藏状态经 unembedding 矩阵 $\mathbf{W}_{U}$ 映射到词表 logits；注入 $\mathbf{v}$ 会产生固定的 logit 位移 $\Delta\mathbf{y}=\alpha\mathbf{v}\mathbf{W}_{U}$。当 $\mathbf{v}$ 与“contradiction”和“entailment”的 unembedding 方向差近似共线时，LRS 在几何上退化为对目标标签增加常数偏置，因此作者用 DLB、最终 token 注入和跨模型移植检验这种解释。

> 直观理解：隐藏向量最终必须经过输出层变成每个词的分数；如果引导方向主要连接两个标签的输出方向，那么它做的不是修改推理过程，而是直接给其中一个标签加固定分数。

**训练与推理**

准备阶段先运行未干预模型，收集各层隐藏激活、最终预测及其正确性；用早层激活训练行为结果探针并跨层评估，选定晚层候选位置。随后从成功和失败上下文的目标层激活计算 $\mathbf{v}$，通过强度网格选择主要设置 $\alpha=1.5$。推理时采用自回归生成，在指定 token 位置执行隐藏状态加法：源任务恢复实验可使用只对矛盾规则族触发的 oracle 门控，而 CRT 必须取消该门控，在原生胜任规则族上无条件注入。
评价时先记录未干预基线并选取准确率至少为 $95\%$ 的 $F_{\text{comp}}$，再比较干预后的准确率、预测翻转方向和错误目标标签数，并用 McNemar 检验分析成对变化。机制核验还包括：将 LRS 替换为直接标签 logit 偏置；分别只在最终标签 token 或思维链 token 注入；将目标层改为早层；使用打乱标签向量、随机高斯扰动和等范数正交向量；以及学习线性投影后执行跨架构向量移植。整个方法的核心输出不是单一恢复分数，而是对干预作出“保持语义特异性的推理修复”或“全局标签偏置覆盖”的诊断。

**复现信息**

主要模型的目标层分别为 Llama 第 $13/16$ 层、Gemma 第 $21/26$ 层、Qwen 第 $32/40$ 层和 DeepSeek 第 $26/32$ 层；主要注入强度为 $\alpha=1.5$。CRT 的原生胜任阈值设为准确率至少 $95\%$，核心跨规则评价每次包含 $N=500$ 个蕴含规则样本。DLB 对照与下游比较采用贪心解码，论文另以温度 $T=0.7$、nucleus 参数 $p=0.9$ 检查采样鲁棒性。
跨模型移植使用 $1000$ 对最终提示 token 的晚层激活拟合投影，采用 $90/10$ 训练—验证划分和正则系数 $\lambda=0.1$；还以非 NLI 的 WikiText 上下文拟合投影，并以随机正交投影作为负对照。公平解释结果时必须区分 oracle 门控与无条件部署：门控需要预先知道样本属于目标规则族，只是隔离向量因果性质的合成控制，不能视为无需任务分类器即可部署的方法。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Asymmetricity-2.0：大规模二分类自然语言推理数据集，超过 $72$ 百万条、约 $25.5$ GB；由 Wikidata 关系三元组和自然语言模板构造，包含对称、传递、非自反等规则族，用于测试蕴含与矛盾判断。数据包含 iid、实体不相交、长度分布外、实体—关系对不相交和属性不相交等划分，并提供词汇化和去词汇化版本。其核心作用是把“目标矛盾规则”和“模型原本擅长的规则”放在同一诊断框架中进行跨规则比较。
- 目标矛盾划分：用于训练或应用预先学习的 LRS，并检验模型在“矛盾盲视”规则上的目标性能。Appendix M 的结果采用 oracle-gated LRS，即只在已知目标样本上施加操控，因此主要测试干预在目标类别上的纠错能力，而不是实际门控器的识别能力。
- 下游任务 CLUTRR、SpartQA 和 ProntoQA：每个任务 $N=100$，并采用平衡的 $50/50$ 划分，用于检验从 Asymmetricity-2.0 学到的 steering vector 能否迁移到不同推理任务。这里不施加门控，因而可以观察操控是否会在非目标任务上产生系统性副作用。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

预测标签正确的样本比例；目标规则上越高越好，但单独使用时可能被类别比例或系统性标签偏置误导。 （越高越好；不过必须结合规则族、类别分布和标签模式解释。）

</div>
<div class="metric-item" markdown="1">

**Recoveries 与 Side Effects**

Recoveries 是由错误变正确的预测数，Side Effects 是由正确变错误的预测数；二者直接衡量干预的净纠错与副作用。 （Recoveries 越高越好，Side Effects 越低越好；若二者同时很高，说明模型可能是在系统性翻转标签，而非进行条件化推理。）

</div>
<div class="metric-item" markdown="1">

**Cohen’s kappa**

衡量两个系统在生成序列上的一致性，本文用于比较 LRS 与 DLB 在随机采样下的输出行为。 （越高表示行为越一致；高一致性支持 LRS 与直接标签偏置具有功能等价性，但本身不证明二者内部机制完全相同。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Cross-Rule Transfer：将针对目标矛盾盲视学习的晚层 LRS 应用于模型原本已经掌握的规则族。

<div class="result-value" markdown="1">

原文摘要报告，非目标规则的基线准确率为 $99.6\%$，施加 steering vector 后下降至 $40.4\%$，并被迫产生错误的矛盾预测。

</div>

这说明 LRS 的目标性能提升不能直接解释为推理电路被修复：如果同一个向量让原本正确的规则大量失效，更符合“全局标签偏置”的解释。该结果强烈支持 CRT 的诊断，但单凭行为结果还不能严格证明向量在参数几何上完全等同于某个固定的 logit bias。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

applying the steering vector to rules the model already handles correctly (99.6% baseline) degrades performance to 40.4% by forcing false contradiction predictions.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 目标矛盾划分上的 oracle-gated LRS。

<div class="result-value" markdown="1">

Llama-3.2-1B-Instruct 的准确率由 $0.1503$ 升至 $1.0000$，Qwen-3.5-9B-Instruct 由 $0.4108$ 升至 $1.0000$，DeepSeek-R1-Distill-Qwen3-8B 由 $0.0349$ 升至 $1.0000$；Gemma-4-E4B-It 由 $0.5430$ 升至 $1.0000$，但其评估仅包含 $256$ 个样本的 bounded retry。

</div>

在预先知道哪些样本属于目标规则的理想条件下，LRS 可以把目标准确率推到完美，因此它确实能改变目标标签预测。然而，这一设置只证明目标行为可被操控，不证明模型学会了识别矛盾；真正的诊断来自同时观察非目标规则上的崩溃和下游迁移失败。

<div class="result-source" markdown="1">

来源：Appendix M, Table 20

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

All models achieve perfect recovery with zero side effects on non-target rule families.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 下游迁移与 DLB 等价性测试。

<div class="result-value" markdown="1">

作者报告，在无门控的下游任务上，LRS 与 DLB 在贪婪解码下具有 identical accuracy profiles；随机采样时二者序列一致性达到 $\kappa\geq0.94$，且 Llama 的 CRT 准确率为 $38.6\%\pm1.2\%$。Table 21 中，Llama-1B-It 在 SpartQA 上由 $0.710$ 降至 $0.290$，而 DeepSeek-Q-8B-It 在 CLUTRR 和 SpartQA 上分别由 $0.000$ 升至 $1.000$。

</div>

LRS 在不同任务上有时提高、有时降低准确率，但标签模式同步发生系统性翻转，例如从 all-entailment 变为 all-contradiction；因此这些变化不应被解释为稳定的跨任务推理能力。LRS 与 DLB 的高度一致性进一步表明主要作用点可能是最终标签 token 的输出竞争，而不是中间推理过程。

<div class="result-source" markdown="1">

来源：Appendix N, Functional Equivalence and Decoding Robustness

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

When evaluated on downstream tasks (where no gating is applied), LRS and DLB display identical accuracy profiles across all models and tasks (as reported in Table 8).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 现有摘录主要提供行为、迁移和 DLB 等价性证据；作者明确表示尚未完成直接的逐层 logit lens 归因以及 steering vector 与 unembedding 差分的余弦相似度审计，因此“表示空间中完全等价于静态标签偏置”的参数级机制仍需进一步验证。
- 目标结果使用 oracle-gated LRS，意味着实验预先知道哪些样本应施加干预；这不能代表实际系统能可靠识别目标规则。另有 Gemma 的完整规模 mechanistic manifest 缺失，仅进行 $256$ 个实例的 bounded retry，结果的可比性和统计稳定性有限。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原始模型（Pre）：不施加 LRS 的模型表现，用于衡量模型的初始矛盾判断能力以及下游任务的原始准确率。
- LRS（Post）：在目标位置注入 steering vector 后的模型表现，用于检验目标矛盾规则上的表面恢复效果及其跨规则副作用。
- Direct Logit Biasing（DLB）：直接在输出层对标签 token 添加偏置的比较方法。它不改变中间推理表示，却可模拟“强制输出某个标签”，因此是判断 LRS 是否等价于标签级偏置的关键基线。
- 控制向量、跨模型 grafting 和早层 steering 控制：这些控制分别检验标签翻转是否可由任意方向实现、向量是否依赖特定模型、以及晚层操控是否只是最终输出阶段的覆盖。所给摘录未报告这些控制的完整数值表。

**实验想回答的问题**

- 在目标矛盾规则上表现良好的局部表征操控（LRS）是否真正修复了模型的推理缺陷，还是仅仅把输出标签从“蕴含”偏置为“矛盾”？
- 通过跨规则迁移、直接对数几率偏置、跨模型迁移、不同解码方式和下游任务测试，能否区分真实的推理修复与表面标签覆盖？

**实验实现**

实验比较模型在施加 LRS 前后的标签预测，并在目标矛盾规则与非目标规则之间进行 Cross-Rule Transfer（CRT）。目标结果采用 oracle-gated LRS；下游测试不使用门控。输出主要通过贪婪解码（temperature $=0.0$）产生，另以 temperature $T=0.7$、nucleus sampling $p=0.9$ 检验解码鲁棒性。每个下游任务使用 $100$ 个样本。作者还检查了生成轨迹，以判断模型是否先完成了正确的逐步推理、再输出错误标签；摘录指出，操控施加在最终标签承诺位置，并未改变此前的自回归推理过程。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 解码鲁棒性：比较贪婪解码与 temperature $T=0.7$、nucleus sampling $p=0.9$。 | 在随机采样下，LRS 与 DLB 的生成序列 Cohen’s kappa 满足 $\kappa\geq0.94$；Llama 的 CRT 准确率为 $38.6\%\pm1.2\%$。 | 该控制排除了“LRS 与 DLB 只是在 temperature $=0$ 时恰好选出同一 top-1 token”的解释。高序列一致性和持续的 CRT 崩溃说明标签偏置行为对解码参数具有鲁棒性，而不是单纯的贪婪解码伪象。 | Appendix N, Functional Equivalence and Decoding Robustness<br><span class="experiment-evidence">In these sampling runs, the functional equivalence between late-layer LRS and DLB remains extremely tight (exhibiting a Cohen’s kappa coefficient of κ ≥ 0.94 between their generated output sequences), and the Cross-Rule Transfer competence collapse on Llama remains catastrophic (38.6% ± 1.2% accuracy).</span> |
| 标签模式与生成轨迹检查：比较干预前后的标签分布，并人工检查 rationale 是否先完成正确推理。 | Table 21 显示 Llama-1B-It 在 CLUTRR 上准确率保持 $0.500$，但标签模式从 All-entailment 变为 All-contradiction；在 SpartQA 上准确率从 $0.710$ 降至 $0.290$，标签模式同样转为 All-contradiction。作者还报告未观察到“正确逐步 rationale 与错误标签不匹配”的生成轨迹。 | 该检查把准确率变化与输出分布联系起来：相同或更低的准确率伴随整体标签翻转，说明模型并非根据每个样本重新判断规则，而是在最终输出位置强制选择某一标签。由于这是人工轨迹检查而非完整的层级因果分析，它支持但不能单独证明所有内部表示都未被改变。 | Appendix N, Functional Equivalence and Decoding Robustness<br><span class="experiment-evidence">instead, they immediately emit the steered label formatting.</span> |

**定性案例**

- Llama-1B-It 的下游结果展示了最直观的失败模式：CLUTRR 的准确率仍为 $0.500$，但输出由全为蕴含变为全为矛盾；SpartQA 则从 $0.710$ 降到 $0.290$。这表明表面上的“修复”可以只是把模型的默认标签偏好整体反转，而没有针对输入内容进行新的逻辑判断。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops a diagnostic framework for determining whether representation steering genuinely repairs logical reasoning mechanisms or merely induces output-label bias.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`41a4eb8969d0fb54dd2169c63b1924974d18f3cb662e3c03665ed76c6c55c69a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
