---
title: "[论文解读] The Differential Reasoning Router: Operationalizing Cost-Aware LLM Annotation in E-commerce"
description: "[arXiv 2608.30224][LLM 效率] 本文针对电商规则式标注的冷启动阶段，提出差分推理路由器 DRR，在有限人工标签和审核预算下，根据直接模型与推理模型各自的成功概率，在直接推断、额外推理和人工审核之间进行成本感知路由。"
arxiv_id: "2608.30224"
announcement_date: "2026-09-01"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:51:42.791466+00:00"
source_sha256: "c6e35f04f6648e9fd3e4082d38a16cb5d6dd747dff03c8735a0cb31ba8e80f99"
tags:
  - "LLM 效率"
  - "LLM 其他"
  - "LLM Reasoning"
  - "大语言模型标注"
  - "冷启动"
  - "模型路由"
  - "成本感知推理"
  - "人工升级"
  - "规则级判断"
  - "电商商品数据"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.30224</p>

# The Differential Reasoning Router: Operationalizing Cost-Aware LLM Annotation in E-commerce

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Cheng Lyu, Jingyue Zhang, Vinny DeGenova, Mengwei Li, Yuanli Pei</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30224v1) · [PDF 下载](https://arxiv.org/pdf/2608.30224v1) · **关键词** 大语言模型标注, 冷启动, 模型路由, 成本感知推理, 人工升级, 规则级判断, 电商商品数据<br>


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

本文针对电商规则式标注的冷启动阶段，提出差分推理路由器 DRR，在有限人工标签和审核预算下，根据直接模型与推理模型各自的成功概率，在直接推断、额外推理和人工审核之间进行成本感知路由。

**不用术语来说**：电商平台上线新的商品属性或业务规则时，必须迅速处理海量商品，但此时可供学习和评估的人工标注很少。便宜的模型容易出错，昂贵的推理模型并非总能纠错，而把所有困难样本交给人工又会造成高成本和长延迟。因此，系统需要判断哪些商品可以直接自动处理，哪些值得使用更昂贵的推理，以及哪些因规则含糊或模型均不可靠而必须交给人工。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将冷启动 LLM 标注形式化为联合的路由与标签获取问题：系统不仅要在轻量直接模型、昂贵推理模型和人工审核之间分配流量，还要利用人工审核产生的标签持续支持提示词改进、监督微调、校准和业务规则修订。
- 作者提出 DRR，通过差分监督分别估计直接模型 $M_d$ 与推理模型 $M_r$ 在样本级和业务规则级的成功可能性，从而衡量推理的边际价值，并识别两种模型都可能失败或规则间存在分歧、因而应当拒答并升级人工审核的样本。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型辅助的数据标注与推理路由研究，应用场景是电商结构化商品数据审核。此类任务需要模型结合商品图片、名称、描述、规格和套装信息，逐条判断图片是否违反业务规则，再给出整体资格标签；结果会直接服务于搜索、推荐、商品运营与合规系统。目录规模可达十亿级，完全依赖人工会造成高成本和长延迟，而直接调用轻量模型虽然便宜，却容易在视觉证据含糊、商品文本冲突或规则边界不清时出错；高成本推理模型也并非始终更可靠。因此，论文关注的不是单一模型如何分类，而是在有限且持续变化的启动期标注下，如何把样本分配给直接推理、强化推理或人工审核。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**冷启动标注**

本文的“冷启动”并非完全没有标签，而是上线前只有一个相对于全目录很小、且会随业务规则调整而变化的种子标注集。系统必须在证据尚不充分时开始运行，并通过后续人工审核逐渐补充可靠标签。

</div>
<div class="concept-item" markdown="1">

**模型路由**

模型路由是根据每个样本的预计难度、正确率与成本，动态选择处理路径。本文的候选路径包括低成本直接模型、高成本推理模型和人工审核，而不是让所有样本统一调用同一个模型。

</div>
<div class="concept-item" markdown="1">

**规则级标注**

一个商品样本需要分别接受多条业务规则检查，例如主体是否突出、是否含尺寸图示、是否出现真人以及视角是否合规。整体标签由这些规则级判断汇总而成，因此只看最终对错会掩盖具体的规则分歧与歧义来源。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个商品审核样本，包括候选主图以及商品名称、特征要点、描述、展示销售数量和套装信息等多模态证据；同时给定多条业务规则，每条规则要求输出通过、失败，部分规则还允许“无法验证例外”。系统最终输出主图是否合格的 $\mathrm{True}$、$\mathrm{False}$ 或 $\mathrm{Unsure}$ 标签，并可附带规则级理由、置信度及修改建议。运行环境具有三种处理资源：轻量直接模型 $M_d$、成本更高的推理模型 $M_r$ 和人工审核者；路由器要在有限种子标签、规则仍可能演化且推理词元有成本的条件下，为每个样本选择处理路径。关键假设是昂贵推理只对部分样本具有正向边际价值：简单样本可由 $M_d$ 处理，$M_r$ 适合预期能够纠正直接判断的样本，而两个模型都可能失败、证据冲突或规则含糊的样本应交由人工；人工结果同时构成后续提示词改进、监督微调、校准和规则修订所需的定向真值。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$M_d$**

轻量、低成本的直接模型，负责无需额外复杂推理的样本。

</div>
<div class="notation-item" markdown="1">

**$M_r$**

成本较高的推理模型，仅在预计额外推理能够改善判断时使用。

</div>

</div>

**直接相关的工作**

- **自适应模型路由与测试时计算分配（Wang et al., 2025；Liang et al., 2025；Ding et al., 2025；Damani et al., 2025）**: 这些研究提供了按样本动态分配模型或计算量的背景，但原文指出，常规路由本身没有同时解决冷启动条件下“推理相对直接模型的边际价值估计”和“将人工审核纳入策略”这两个要求。
- **LLM 置信度与校准（Kadavath et al., 2022；Ulmer et al., 2024；Khanmohammadi et al., 2025）**: 置信度方法能够发现不确定预测，却不能直接区分“额外推理能够纠正”的样本与“直接模型和推理模型都会失败”的样本；这一差异正是本文路由决策所需的信息。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

结构化商品数据直接影响搜索、推荐、商品运营和合规，但其维护通常要求模型依据图像、描述等多模态证据逐条执行多项业务规则。新品类、新属性或新规则上线时，平台面对的是一种特殊冷启动：并非完全没有标签，而是只有相对于全量商品目录极小、仍会随规则修改而过时的上线前种子标注集。全量人工审核在十亿级商品规模下成本和延迟过高；然而直接推断较便宜但脆弱，额外推理价格更高且效果未知，因此上线策略必须同时控制错误、推理令牌开销和人工审核量。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于置信度或校准的不确定性路由**：先由模型输出预测及一个标量置信度，再按验证集选定的阈值，把低置信度样本送入更昂贵的模型或人工流程。这类方法擅长筛出模型不确定的样本，但路由依据主要是单个预测的可信程度。
- **自适应计算与测试时推理路由**：根据输入难度或预期表现，在轻量直接推断与具有更多测试时计算的推理模型之间选择，以便把额外计算集中到较困难的样本；许多既有方案依赖规模较大且具有代表性的人工标注数据来训练或校准路由器。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单一置信度只能说明当前预测是否不确定，不能直接估计从 $M_d$ 切换到 $M_r$ 后会增加多少正确概率。因此，它容易把两类样本混在一起：一类确实可由推理纠正，另一类则会被两个模型同时做错；后者即使消耗更多推理令牌，也未必改善最终决策。
- 传统模型路由通常把更强的推理模型当作困难样本的默认后备，却没有把人工审核及其标签获取价值纳入同一策略。推理模型并非可靠的通用兜底方案，而且部分错误来自业务规则边界含糊、证据缺失或真实标签不足，而非模型计算能力不够；若不升级人工，这些问题既无法安全处理，也无法形成用于后续规则修订和系统学习的针对性真值。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一种适用于有限且持续变化的上线前标签集的统一决策机制：它需要分别预测直接推断和额外推理能否成功，显式计算推理相对于直接模型的增益，同时识别自动化路径可能共同失败或业务规则存在分歧的样本，并在给定推理成本与人工审核预算下完成路由。该缺口本质上不是简单的“选择更强模型”，而是把计算分配、可靠拒答和高价值标签获取结合起来。

</div>
<div markdown="1"><span>核心问题</span>

在冷启动电商规则式标注中，能否仅利用有限的强制性上线前标注，学习一个成本感知策略，使系统在直接模型 $M_d$、推理模型 $M_r$ 和人工审核之间自适应分流，在保持准确性的同时减少不必要的推理令牌，并把人工预算集中到自动模型共同不可靠或规则有歧义的样本上？

</div>
<div markdown="1"><span>作者直觉</span>

关键不是问某个样本“难不难”，而是分别问两个模型“各自有多大概率做对”。若 $M_d$ 已很可能正确，额外推理没有购买价值；若 $M_d$ 可能失败而 $M_r$ 更可能成功，推理令牌才值得投入；若二者都可能失败，继续增加模型计算不如请人工判断。进一步在单条业务规则层面观察两种模型的失败和分歧，可以区分一般模型错误与规则边界问题，使人工审核既修正当前结果，也产生最有助于后续校准、训练和规则完善的标签。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

差异推理路由器（Differential Reasoning Router，DRR）把电商商品属性标注建模为一个受成本约束的多模态三路路由问题。输入查询为商品图像与文本元数据的组合 `$q=(x_{\mathrm{img}},x_{\mathrm{txt}})$`，商品必须同时满足业务规则集合 `$\mathcal{R}=\{r_1,\ldots,r_k\}$`。DRR在低成本直接模型 `$M_d$`、高成本推理模型 `$M_r$` 和人工审核之间选择：容易样本交给 `$M_d$`，预期能从额外推理中获益的样本交给 `$M_r$`，而两个自动化路径都可能失败或存在明显不确定性的样本交给人工。技术上，系统使用冻结的预训练多模态编码器提取并缓存特征，再由轻量监督路由器分别估计两个模型在整组规则和单条规则上的正确概率，以及二者同时失败的概率；训练时以监督预测、预期路由误差和推理预算约束共同优化，推理时先执行人工门控，再依据成本调整后的推理边际价值做模型选择。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 商品输入与特征缓存

预训练多模态编码器分别生成图像嵌入 `$e_v$` 和文本嵌入 `$e_t$``，并构造融合特征 `$z=[e_v;e_t;e_v\odot e_t]$`，其中 `$\odot$` 表示逐元素乘法，用于表示图文交互；编码器不参与微调，嵌入在上线前计算并缓存。

<div class="method-step__io" markdown="1">

**输入**：商品图像 `$x_{\mathrm{img}}$`、文本元数据 `$x_{\mathrm{txt}}$`，以及需要检查的业务规则集合 `$\mathcal{R}$`。<br>
**输出**：供路由器使用的融合向量 `$z$`，以及商品需满足的规则列表。

</div>

**直观理解**：先把图片、文字及其匹配关系转换成数字特征，并提前保存下来。这样线上只需运行小型路由模型，不必每次重新运行昂贵的多模态编码器。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 差异可靠性预测

共享多层感知机（MLP）主干处理 `$z$`，随后使用多类预测头估计直接模型和推理模型在完整规则集上的成功概率 `$\hat p_d(q)$` 与 `$\hat p_r(q)$`，在每条规则 `$r_j$` 上的正确概率 `$\hat p_{d,j}(q)$` 与 `$\hat p_{r,j}(q)$`，以及两个自动化模型同时失败的概率 `$\hat p_{\mathrm{amb}}(q)$`。监督标签来自模型输出与人工真值的逐系统、逐规则对照，而不是让直接模型模仿推理模型。

<div class="method-step__io" markdown="1">

**输入**：缓存的融合特征 `$z$`。<br>
**输出**：两个模型的系统级可靠性、规则级可靠性、联合失败风险，以及由此得到的推理边际价值 `$\mathrm{MVOR}(q)=\hat p_r(q)-\hat p_d(q)$`。

</div>

**直观理解**：路由器不是简单相信模型自己的置信度，而是学习“在类似商品上，哪个模型通常会答对”。它还判断两个模型是否可能一起答错，从而识别单纯换一个模型也无法解决的样本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 预算约束下的路由训练

用监督损失训练各预测头，并用可微的软路由概率 `$\pi_r(q)=\sigma((\mathrm{MVOR}(q)-\lambda\Delta C_q)/T)$` 估计选择推理模型的概率；其中 `$\lambda$` 是推理预算的拉格朗日乘子，`$T$` 是温度参数。路由损失估计自动化决策误差，预算项惩罚期望增量推理成本超过目标值。

<div class="method-step__io" markdown="1">

**输入**：预测概率、直接模型与推理模型的成本 `$C_d(q)$` 和 `$C_r(q)$`、增量推理成本 `$\Delta C_q=C_r(q)-C_d(q)$`，以及目标推理预算 `$B_{\mathrm{target}}$`。<br>
**输出**：路由器参数 `$\theta$` 和收敛后的预算价格 `$\lambda^*$`，它们共同决定何时值得调用推理模型。

</div>

**直观理解**：模型会把“推理可能带来的正确率提升”与“这次推理要多花的钱”放在一起比较。预算越紧，预算价格越高，系统就越不愿意为边际收益很小的样本调用昂贵模型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 推理时人工门控与模型选择

首先执行人工门控：若 `$\hat p_{\mathrm{amb}}(q)>\tau_{\mathrm{amb}}$`，或 `$\max(\hat p_d(q),\hat p_r(q))<\tau_{\mathrm{conf}}$`，则转人工。若样本通过人工门控，则当 `$\mathrm{MVOR}(q)>\lambda^*\Delta C_q$` 时选择 `$M_r$`，否则选择 `$M_d$`。

<div class="method-step__io" markdown="1">

**输入**：新商品的预测值 `$\hat p_d(q)$`、`$\hat p_r(q)$`、`$\hat p_{\mathrm{amb}}(q)$`，收敛乘子 `$\lambda^*$`，增量成本 `$\Delta C_q$`，以及验证集调出的阈值 `$\tau_{\mathrm{amb}}$` 和 `$\tau_{\mathrm{conf}}$`。<br>
**输出**：三路动作 `$\pi(q)\in\{M_d,M_r,\mathrm{Human}\}$`，以及由所选路径产生的最终商品标注。

</div>

**直观理解**：先问“两个自动化模型是不是都不可靠”；如果是，就不要继续让模型猜，而交给人。剩下的样本再问“额外推理带来的预期收益是否值得成本”，以决定使用便宜模型还是推理模型。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 预算约束的路由训练目标

$$
\mathcal{J}(\theta,\lambda)=\mathcal{L}_{\mathrm{sup}}(\theta)+\mathcal{L}_{\mathrm{route}}(\theta)+\lambda\left(\bar{C}_{\mathrm{route}}-B_{\mathrm{target}}\right)
$$

**符号说明**

- $\mathcal{J}(\theta,\lambda)$：带预算约束的总体训练目标；`$\theta$` 是路由器参数，`$\lambda$` 是非负预算乘子。
- $\mathcal{L}_{\mathrm{sup}}(\theta)$：监督损失，用二元交叉熵训练系统级、规则级和歧义预测头。
- $\mathcal{L}_{\mathrm{route}}(\theta)$：软路由策略下的期望自动化错误损失。
- $\bar{C}_{\mathrm{route}}$：软路由策略产生的期望增量推理成本。
- $B_{\mathrm{target}}$：允许的平均推理预算。
- $\lambda$：推理预算的影子价格；预算超支时增大，使调用 `$M_r$` 更难。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标同时要求路由器学会预测模型是否正确、降低自动化错误，并遵守平均推理成本限制。最后一项不是直接禁止所有昂贵调用，而是根据超预算程度提高其训练代价，因此系统能在准确率与成本之间进行连续调节。<br>
**原文位置**：第3.2节，公式（2）

</div>

</div>

<div class="equation-block" markdown="1">

#### 成本调整后的软推理路由

$$
\pi_r(q)=\sigma\left(\frac{\mathrm{MVOR}(q)-\lambda\Delta C_q}{T}\right),\qquad \mathrm{MVOR}(q)=\hat p_r(q)-\hat p_d(q)
$$

**符号说明**

- $\pi_r(q)$：训练阶段对查询 `$q$` 选择推理模型 `$M_r$` 的软概率。
- $\sigma(\cdot)$：Sigmoid函数，将输入转换为 `$0$` 到 `$1$` 之间的概率。
- $\mathrm{MVOR}(q)$：推理相对于直接模型预计减少的错误风险，即推理模型成功概率减去直接模型成功概率。
- $\hat p_r(q),\hat p_d(q)$：推理模型和直接模型在完整规则集上预测成功的概率。
- $\Delta C_q$：查询 `$q$` 调用推理模型相对直接模型增加的成本，定义为 `$C_r(q)-C_d(q)$`。
- $T$：温度参数，控制软路由概率从直接模型转向推理模型的平滑程度。

<div class="equation-explanation" markdown="1">

**直观理解**：只有当推理模型预计比直接模型更可靠，而且这种提升足以抵消额外成本时，`$\pi_r(q)$` 才会较高。训练时使用软概率保持可微；部署时则采用硬阈值 `$\mathrm{MVOR}(q)>\lambda^*\Delta C_q$` 做最终选择。<br>
**原文位置**：第3.2节；硬路由规则见第3.4节公式（3）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标由三部分组成：`$\mathcal{L}_{\mathrm{sup}}$` 学习各模型与人工真值之间的差异性可靠性，`$\mathcal{L}_{\mathrm{route}}$` 使软路由倾向于较低的预期错误，拉格朗日项 `$\lambda(\bar C_{\mathrm{route}}-B_{\mathrm{target}})$` 约束平均增量推理成本。系统采用交替原始—对偶更新：路由器参数 `$\theta$` 通过梯度下降更新，预算乘子在对数空间中令 `$\lambda=e^\nu$`，并按 `$\nu\leftarrow\nu+\eta_\lambda(\bar C_{\mathrm{route}}-B_{\mathrm{target}})$` 更新。当期望成本超过预算时，`$\lambda$` 增大并抬高推理门槛；低于预算时，`$\lambda$` 减小并允许更多推理调用。歧义头使用加权二元交叉熵，因为两个自动化模型同时失败的样本较少，但对人工审核决策具有重要价值。该训练方式是“差异监督”而非“蒸馏”：目标不是让 `$M_d$` 模仿 `$M_r$`，而是分别学习两者何时与人工真值一致；这保留了推理模型可能负价值的情况，即 `$M_r$` 失败而 `$M_d$` 正确。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 冻结多模态特征与轻量融合主干**

系统使用预训练多模态编码器得到 `$e_v$` 与 `$e_t$`，再通过 `$z=[e_v;e_t;e_v\odot e_t]$` 同时保留图像证据、文本证据和图文对齐信息。编码器不微调，路由器仅消费缓存特征，并将融合向量输入共享 MLP 主干，以降低在线延迟并保持特征处理稳定。

> 直观理解：该模块相当于先做一次完整的“看图和读文字”，把结果存下来。线上路由只需读取这些结果并进行小规模计算，因此不会因为路由决策再次承担大型模型的全部开销。

**2. 差异可靠性预测头**

系统级头预测 `$P(y_d^{\mathrm{sys}}=1\mid q)$` 和 `$P(y_r^{\mathrm{sys}}=1\mid q)$`，其中 `$y_m^{\mathrm{sys}}=1$` 表示模型 `$M_m$` 在完整规则集上与人工真值一致。规则级头预测 `$P(y_{m,j}=1\mid q)$`，用于定位具体业务规则上的可靠性；歧义头的目标在 `$y_d^{\mathrm{sys}}=0$` 且 `$y_r^{\mathrm{sys}}=0$` 时为正，用于预测联合失败。

> 直观理解：系统级预测回答“这个商品整体能否自动处理”，规则级预测回答“究竟是哪一条规则容易出错”。联合失败预测尤其重要，因为如果两个模型都可能失败，继续在它们之间切换并不能真正提高结果。

**3. MVOR成本感知路由与人工门控**

推理边际价值定义为 `$\mathrm{MVOR}(q)=\hat p_r(q)-\hat p_d(q)$`。自动化选择比较 MVOR 与成本门槛 `$\lambda^*\Delta C_q$`；人工门控则独立使用联合失败阈值和最低置信度阈值，从而将“值得升级到推理模型”和“应退出自动化路径”区分开来。

> 直观理解：这不是把推理模型当作固定的兜底模型，而是估计它相对直接模型的实际增益。人工审核也不是模型选择之后的临时补救，而是一个明确的第三种动作。

**训练与推理**

训练阶段，样本需要包含两个候选模型的输出以及人工真值，以构造完整规则正确标签 `$y_m^{\mathrm{sys}}$`、逐规则正确标签 `$y_{m,j}$` 和联合失败标签。融合特征输入共享 MLP 与各预测头，监督损失学习可靠性，软路由估计直接模型与推理模型的混合错误和增量成本，再通过原始—对偶更新逐步逼近目标推理预算。推理阶段，系统读取缓存多模态特征并输出上述概率；先以 `$\hat p_{\mathrm{amb}}(q)>\tau_{\mathrm{amb}}$` 或 `$\max(\hat p_d(q),\hat p_r(q))<\tau_{\mathrm{conf}}$` 判断是否人工审核。通过人工门控后，再用收敛的 `$\lambda^*$` 和样本成本比较 MVOR：超过成本门槛调用 `$M_r$`，否则调用 `$M_d$`。人工审核产生的标签被纳入后续重训练、校准、提示词或监督微调数据更新，并可帮助修订含义不清的业务规则。

**复现信息**

为保证生产延迟，昂贵的多模态特征只计算一次并缓存，在线决策层仅运行轻量监督模型。人工阈值 `$\tau_{\mathrm{amb}}$` 与 `$\tau_{\mathrm{conf}}$` 在验证集上结合人工转介预算调节；推理预算 `$B_{\mathrm{target}}$` 控制推理模型的平均增量成本，人工门控阈值则独立控制审核量。方法描述了直接模型、推理模型和人工三种动作及其相对成本，但所给章节未明确报告编码器、MLP层数、优化器、学习率、批大小、温度 `$T$` 的具体取值或人工标注协议，因此这些细节不能据此复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 生产环境中的主图合规数据集：每个样本包含一张商品图片及商品元数据，任务是判断该图片能否作为商品主图。人工真值依据$k=11$条合取业务规则确定；任一规则失败，样本即判为不合格。该数据集同时覆盖客观视觉检查和主观视觉判断，用于评估真实部署条件下的路由效果。原文未明确报告数据集规模、训练/验证/测试划分及各划分样本数。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率**

预测的主图合规结论与人工真值一致的样本比例；由于任务是$11$条规则的合取判断，单条规则错误即可导致最终样本错误。 （越高越好，因为它表示最终业务判定更接近人工真值。原文未明确报告具体数值。）

</div>
<div class="metric-item" markdown="1">

**推理令牌成本**

调用推理模型所消耗的推理令牌数量或相对成本，用于衡量高成本推理路径的使用程度。 （越低越好，但必须结合准确率解释；仅降低令牌消耗而损害判定质量并不能说明路由器更优。原文未明确报告成本的精确定义或统计单位。）

</div>
<div class="metric-item" markdown="1">

**人工升级量**

被路由至人工标注员复核的样本数量或比例，反映系统在自动化与人工风险控制之间的权衡。 （通常越低越好，但前提是准确率和风险可接受；原文未明确报告该指标是否被正式统计。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### DRR与最强置信度路由器的准确率比较

<div class="result-value" markdown="1">

作者声称DRR达到了与最强置信度路由器相当的准确率，但供给原文未给出具体准确率、置信区间或显著性检验。

</div>

这表明DRR至少在最终分类质量上没有明显落后于该置信度基线；它支持“节省成本而不牺牲已报告的准确率水平”的主张，但不能据此证明DRR在统计意义上更准确，也不能判断不同规则或不同难度样本上的误差差异。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In a production e-commerce workflow, DRR reaches accuracy parity with the strongest confidence-based router while achieving more than 60\% reasoning-token cost savings.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### DRR的推理令牌成本

<div class="result-value" markdown="1">

相对于最强置信度路由器，DRR的推理令牌成本节省超过$60\%$；供给原文未报告绝对令牌数、成本基准、统计区间或对应准确率数值。

</div>

该结果说明DRR减少了对高成本推理路径的调用，符合其“只在预期有帮助时使用推理”的设计目标。但仅凭摘要无法判断节省来自哪些样本、是否增加了人工审核量，也无法确认成本节省在不同流量或规则子集上是否稳定。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In a production e-commerce workflow, DRR reaches accuracy parity with the strongest confidence-based router while achieving more than 60\% reasoning-token cost savings.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 规则级与样本级联合路由

<div class="result-value" markdown="1">

作者将DRR描述为同时估计直接模型和推理模型在样本层面及业务规则层面的成功概率，并据此把样本分配给直接模型、推理模型或人工；但供给原文未提供各路由分支的准确率、覆盖率、成本或人工升级比例。

</div>

该设计针对合取规则任务的特殊风险：最终标签可能因单条规则失败而失败，因此只看样本整体置信度可能无法定位具体规则的不确定性。现有材料支持这是实验所验证的机制方向，但不足以量化规则级估计究竟带来多少增益。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

DRR estimates separate success probabilities for a direct model and a reasoning model at both the sample and business-rule levels, enabling adaptive routing: easy cases are handled directly, reasoning is reserved for cases where it is expected to improve the decision, and likely double-failure or rule-disagreement cases are escalated to human annotators.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 供给的实验章节仅包含任务设定及规则说明，未提供完整的实验表格、数据规模、数据划分、模型配置、阈值、基线细节和显著性检验；因此多数定量比较只能标注为原文未明确报告。
- 目前材料只涉及单一生产级电商主图合规任务，且摘要中的成本收益来自该工作流；不能据此推断DRR在其他商品类别、规则数量、视觉任务或不同模型成本结构下同样有效。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 基于置信度的路由器：论文摘要称其为最强的置信度路由基线，用于检验DRR是否能在相近准确率下进一步节省推理成本；原文未明确报告该基线的具体模型、路由规则或名称。
- 直接模型：作为无需额外推理的低成本处理路径，用于比较直接预测与DRR自适应调用推理模型之间的效果差异；原文未明确报告其具体模型名称。
- 推理模型：作为较高成本的分析路径，用于比较始终依赖推理能力与DRR选择性调用推理能力的差异；原文未明确报告其具体模型名称。
- 人工升级路径：由人工标注员处理模型可能双重失败或业务规则存在分歧的样本，用于评估DRR的人机协作设计；原文未明确报告人工标注成本、规模或单独的性能结果。

**实验想回答的问题**

- 在生产级电商主图合规任务中，差异化推理路由器（DRR）能否在保持分类准确率的同时降低推理模型的令牌成本？
- DRR是否能比单纯基于置信度的路由策略更有效地区分适合直接处理、适合调用推理模型以及应升级给人工标注的样本？

**实验实现**

评估任务要求模型同时检查商品图片、商品信息和候选主图，并严格执行$11$条业务规则。规则既包括“图片必须满足”的资格条件，也包括“不得违反”的淘汰条件；模型需要逐条评估并给出简短的规则级理由，在规则含义不明确时说明不确定性并反映到置信度中。DRR的核心实验协议是分别估计直接模型和推理模型在样本层面及业务规则层面的成功概率，再据此进行自适应路由：容易样本交给直接模型，预期能从额外推理中获益的样本交给推理模型，而预计两个模型都可能失败或存在规则分歧的样本交给人工。原文未明确报告模型版本、提示词完整内容、阈值、硬件、重复次数、随机种子及成本计算公式。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 任务规则中的示例说明了模型必须处理边界情况，例如展开的沙发床、打开的抽屉或被道具大面积遮挡的商品可能触发不同规则失败。这些例子体现了规则级判断的必要性，但供给原文没有提供DRR对具体样本的路由、模型输出与人工结论对照，因此不能作为正式定量案例研究。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution is cost-aware routing between direct and reasoning LLMs with human escalation to reduce reasoning-token expenditure.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`c6e35f04f6648e9fd3e4082d38a16cb5d6dd747dff03c8735a0cb31ba8e80f99`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
