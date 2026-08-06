---
title: "[论文解读] SPOT: Sparse Probing and Outcome Calibration for On-Policy Distillation"
description: "[arXiv 2608.04419][LLM Reasoning] SPOT将按需选择探测位置与依据下游结果构造蒸馏目标分开处理，使在策略蒸馏既能利用教师的逐词监督，又能以有限计算发现并保留真正有助于推理成功的候选分支。"
arxiv_id: "2608.04419"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T07:05:36.066323+00:00"
source_sha256: "3ee9cc55d336194ecf6155009640869180c544eff2ce12be1483da86d8e56f81"
tags:
  - "LLM Reasoning"
  - "在策略蒸馏"
  - "知识蒸馏"
  - "反向 KL 散度"
  - "教师熵"
  - "稀疏探测"
  - "结果校准"
  - "推理模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.04419</p>

# SPOT: Sparse Probing and Outcome Calibration for On-Policy Distillation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Zikun Qu, Min Zhang, Mingze Kong, Zhiwei Shang, Yikun Ban, Shuang Qiu, Zhongxiang Dai</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The Chinese University of Hong Kong, Shenzhen；East China Normal University；Beihang University；City University of Hong Kong</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04419v1) · [PDF 下载](https://arxiv.org/pdf/2608.04419v1) · **关键词** 在策略蒸馏, 知识蒸馏, 反向 KL 散度, 教师熵, 稀疏探测, 结果校准, 推理模型<br>


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

SPOT将按需选择探测位置与依据下游结果构造蒸馏目标分开处理，使在策略蒸馏既能利用教师的逐词监督，又能以有限计算发现并保留真正有助于推理成功的候选分支。

**不用术语来说**：小模型沿自己生成的文本继续推理时，教师模型通常会为下一个词提供概率分布，但最高概率的词不一定通向正确答案，其他较低概率候选也可能形成有效解法。逐一尝试所有候选又需要完成后续生成并检查答案，成本很高。因此，关键问题是在有限预算下决定哪些生成位置值得尝试多个分支，以及尝试后应如何根据最终成败调整这些候选的训练权重。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“在哪里探测”与“蒸馏什么”的两决策框架：前者依据教师不确定性、教师前若干候选的概率质量及师生差异分配稀疏探测预算，后者依据候选分支的验证结果构造监督目标。
- 作者提出SPOT的获取—探索—利用流程：从教师的前$k$个候选中建立分支，用学生策略完成后续推理并由验证器评分，再以结果校准教师分布；作者报告该设计旨在提高多次采样时的解法覆盖，同时维持平均正确率。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型推理能力的知识蒸馏研究。传统监督微调和离策略蒸馏使用教师或专家生成的轨迹，训练时所见上下文与学生推理时由自身预测形成的上下文不同，容易产生暴露偏差并累积错误；仅依赖终局验证奖励的在策略强化学习虽然使用学生轨迹，却难以把结果好坏细分到每个生成位置。在策略蒸馏（OPD）结合两者：先由学生生成轨迹，再让教师对学生实际访问的每个前缀提供词元级概率分布，从而同时缓解状态分布失配并获得密集监督。本文关注其中的覆盖问题：标准 OPD 使用反向 KL 散度，倾向集中到教师分布的主导模式，可能低估其他同样合理、且能导向正确答案的后续词元。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**在策略蒸馏（On-Policy Distillation, OPD）**

学生先按当前策略生成完整轨迹，教师再对这些学生实际产生的前缀给出下一词元分布，学生据此学习。它与离策略蒸馏的关键区别是训练上下文来自学生自身，因而更接近部署时遇到的状态。

</div>
<div class="concept-item" markdown="1">

**反向 KL 与前向 KL**

反向 KL $D_{\mathrm{KL}}(\pi_\theta\|\pi_T)$ 更偏向教师的高概率模式，可能忽略次要但合理的候选；前向 KL $D_{\mathrm{KL}}(\pi_T\|\pi_\theta)$ 更强调覆盖教师支持的多种候选。EOPD 只在教师熵较高的位置，以教师 top-$k$ 候选近似前向 KL 来补充覆盖监督。

</div>
<div class="concept-item" markdown="1">

**教师熵与候选概率质量**

教师熵衡量下一词元分布整体有多不确定，但相同的高熵既可能来自少数有竞争力的候选，也可能来自很长的低概率尾部。因而还需考察 top-$k$ 候选捕获了多少总概率，以及学生是否已正确表示这些候选，才能判断一次昂贵探测是否值得。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定提示分布 $\mathcal D$、共享词表 $\mathcal V$ 上的学生策略 $\pi_\theta$ 和教师策略 $\pi_T$，对提示 $q\sim\mathcal D$，学生生成轨迹 $x=(x_1,\ldots,x_T)\sim\pi_\theta(\cdot\mid q)$，并在每个位置形成学生诱导的前缀 $c_t=(q,x_{<t})$。标准 OPD 在这些前缀上最小化学生到教师的反向 KL；实际训练可由冻结的旧行为策略 $\pi_{\theta_{\mathrm{old}}}$ 采样，并采用 PPO 风格裁剪。本文进一步考虑预算受限的选择性探测：系统必须先从轨迹位置中决定哪些前缀值得测试，再从教师 top-$k$ 集合逐一接入候选词元、用学生完成后续生成并由验证器评价最终结果；所需输出是经过结果校准的局部监督目标，使学生提高成功候选的概率，同时仍以教师分布为先验。该设定假定师生共享词表，且可查询教师的词元概率、运行学生续写并获得验证器反馈。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal D$**

提示或问题的分布，训练提示满足 $q\sim\mathcal D$。

</div>
<div class="notation-item" markdown="1">

**$\pi_\theta,\ \pi_T$**

分别表示参数为 $\theta$ 的学生策略与教师策略；二者均是在共享词表上的完整下一词元分布。

</div>
<div class="notation-item" markdown="1">

**$c_t=(q,x_{<t})$**

位置 $t$ 的学生诱导前缀，由提示 $q$ 和学生此前生成的词元 $x_{<t}$ 组成。

</div>
<div class="notation-item" markdown="1">

**$S_t^k=\operatorname{TopK}_k(\pi_T(\cdot\mid c_t))$**

教师在前缀 $c_t$ 上概率最高的 $k$ 个下一词元候选集合，用于高效近似覆盖监督及后续候选探测。

</div>

</div>

**直接相关的工作**

- **标准在策略蒸馏（OPD）**: 它在学生生成的前缀上使用教师的密集词元级反馈，缓解离策略训练的暴露偏差；但其反向 KL 目标具有模式寻求倾向，可能不给其他合理延续分配足够概率，是本文要修正的基础方法。
- **EOPD（Entropy-Aware On-Policy Distillation）**: EOPD 以教师高熵为触发条件，并在教师 top-$k$ 候选上加入前向 KL，以改善候选覆盖。本文指出熵无法区分“少数强候选”与“长概率尾部”，也不反映师生候选差异或候选的下游成功率，因此需要把探测位置选择与结果校准目标分开处理。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推理能力蒸馏需要同时解决训练上下文偏移与监督粒度不足。离线蒸馏使用教师生成轨迹，学生推理时却面对由自身错误逐步形成的上下文，容易产生暴露偏差和误差累积；在策略强化学习虽然使用学生自己的轨迹，但通常只有序列级或终局验证奖励，难以判断某个局部词元选择应承担多少责任。在策略蒸馏因此很有吸引力：它在学生生成的前缀上提供教师的稠密逐词反馈。然而，如何在不显著增加分支展开成本的条件下保留多种可能成功的推理路径，仍是实际训练中的核心需求。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **标准反向KL在策略蒸馏**：在学生生成的前缀上，让学生分布通过最小化反向KL散度逼近教师分布。该目标偏向教师概率较高的主导续写，能够提供稠密的词元级训练信号，但具有较强的寻模态倾向。
- **基于教师熵触发的EOPD**：先以教师下一词分布的熵判断当前位置是否不确定；在高熵位置，除反向KL外，再使用教师前$k$个候选近似正向KL，从而鼓励学生为多个局部上合理的候选保留概率。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 反向KL容易将训练质量集中到教师的主导续写，对其他合理候选分配不足概率，其后果是学生可能只覆盖少数解题路径，多次采样时也难以产生具有差异性的成功方案。
- 教师熵只能表示分布总体有多不确定，不能区分概率是集中在少数可探测候选上，还是分散于长尾；它也不反映学生是否已经正确覆盖和排序这些候选。更重要的是，教师的局部概率不等于候选在当前学生策略下的最终成功率。因此，仅靠熵既难以有效分配昂贵的展开验证预算，也不能确定应把额外概率赋给哪个候选。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一个将有限计算预算与结果可靠性统一起来的选择性蒸馏机制：它既要在展开候选之前，利用廉价的局部信息识别最值得获取额外证据的位置；又要在展开之后，把学生续写的实际验证结果转化为局部监督，同时避免完全抛弃教师分布这一有价值的先验。位置选择与目标构造若仅由同一个不确定性指标决定，就无法填补这一缺口。

</div>
<div markdown="1"><span>核心问题</span>

在学生生成前缀上的在策略蒸馏中，如何结合教师不确定性、教师前$k$个候选所覆盖的概率质量以及师生分布差异，把有限探测预算分配给最有信息价值的位置；并在获得验证器评分的学生续写后，如何构造一个既偏向下游结果更好的候选、又受教师分布约束的局部训练目标？

</div>
<div markdown="1"><span>作者直觉</span>

可以把教师看成“候选提出者”，而不是最终裁判。若教师在某处给多个候选显著概率、这些概率主要集中于一个很小的候选集合，并且学生尚未充分表示或正确排序它们，那么在这里尝试分支最可能带来新信息。随后让学生从每个候选继续生成，并用最终答案验证结果检验整条分支，相当于用实际成败纠正教师的局部判断；同时保留对教师分布的KL约束，则可防止少量、有噪声的验证结果使训练目标发生过度偏移。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SPOT是在标准同策略蒸馏（OPD）之上增加稀疏分支监督的方法，核心解决两个相互关联的问题：在哪些生成位置值得花费额外计算进行探测，以及在这些位置应向学生蒸馏哪些候选词。每轮训练先由冻结的旧学生策略$\pi_{\theta_{\mathrm{old}}}$生成轨迹，并在所有学生访问到的前缀$c_t$上查询教师$\pi_T$；随后用归一化教师熵、教师top-$k_s$概率质量和师生差异构成采集分数$s_t$，仅选择得分最高的$M$个位置。对每个入选位置，方法从教师top-$k_p$候选词分别出发，让旧学生继续生成，并用验证器$R$评估最终结果；这些回报用于指数倾斜教师先验，形成结果校准目标$\tilde{\pi}_T$。最终训练同时最小化整条原轨迹上的反向KL蒸馏损失和入选分支上的交叉熵损失，输出更新后的学生策略$\pi_\theta$。

直观地说，SPOT不在每个词位都穷举后续路径，而是先寻找“教师有少数几个合理选择、学生又没有学好”的关键岔路口，再实际尝试各条岔路能否通向正确答案。教师概率提供初始偏好，验证器给出结果证据，二者共同决定学生在该岔路口应重新分配多少概率；因此它既保留教师知识，又避免把教师局部最偏好的词误当成必然具有最好长期结果的选择。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 同策略轨迹采集与教师查询

在每轮开始固定行为策略$\pi_{\theta_{\mathrm{old}}}\leftarrow\pi_\theta$，采样学生轨迹$x\sim\pi_{\theta_{\mathrm{old}}}(\cdot\mid q)$；对每个前缀$c_t=(q,x_{<t})$查询教师的全词表分布$\pi_T(\cdot\mid c_t)$。

<div class="method-step__io" markdown="1">

**输入**：提示$q\sim\mathcal{D}$、当前学生$\pi_\theta$和教师$\pi_T$。<br>
**输出**：包含学生轨迹、各位置师生概率分布及前缀$c_t$的训练样本。

</div>

**直观理解**：学生先按自己当前会走的路线解题，教师再对这条路线上的每一步给出建议。这样监督覆盖的是学生实际会遇到的状态，而不是教师单独生成时才会访问的状态。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 位置采集与稀疏预算分配

计算归一化教师熵$\bar H_T(c_t)$、教师top-$k_s$质量$C_t^{k_s}$以及由质量不足和Jensen–Shannon形状差异组成的师生差距$G_t^{k_s}$，令$s_t=\bar H_T(c_t)C_t^{k_s}G_t^{k_s}$。屏蔽特殊、填充、纯空白和纯标点词位后，选择$\mathcal B=\operatorname{Top\text{-}}M(\{s_t\})$。

<div class="method-step__io" markdown="1">

**输入**：每个有效位置的教师分布、旧学生分布、评分候选数$k_s$和位置预算$M$。<br>
**输出**：最多包含$M$个待探测位置的集合$\mathcal B$。

</div>

**直观理解**：高熵只表示教师犹豫，却不能说明犹豫是否集中在少数可操作的选择上；乘积评分要求三个条件同时较强。它把有限预算留给“有几个明确备选，而且学生对这些备选覆盖不足或排序不同”的位置。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选分支探测与可行性筛选

对每个$t\in\mathcal B$及$v\in S_t^{k_p}$，把$v$接到前缀$c_t$后，从$\pi_{\theta_{\mathrm{old}}}(\cdot\mid c_t,v)$独立采样$N_p$条续写，并以验证器回报的均值估计候选的学生可执行价值$\hat V_t(v)$。仅保留至少存在一个正价值候选的位置，得到$\mathcal B^+\subseteq\mathcal B$，每条原轨迹至多需要$M k_p N_p$次候选续写。

<div class="method-step__io" markdown="1">

**输入**：位置集合$\mathcal B$、每个位置的教师top-$k_p$候选集$S_t^{k_p}$、每候选采样数$N_p$、旧学生$\pi_{\theta_{\mathrm{old}}}$和验证器$R$。<br>
**输出**：保留位置$\mathcal B^+$及其各候选的价值估计$\hat V_t(v)$。

</div>

**直观理解**：这里评估的不是候选词看起来是否合理，而是当前学生接过这个词以后，是否真能把答案完成好。若一个位置的所有尝试都没有正回报，方法就不额外强化该位置，避免从无效探索中制造监督。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结果校准与联合优化

对$t\in\mathcal B^+$，以$\exp(\gamma\hat V_t(v))$倾斜教师先验并归一化，得到结果校准目标$\tilde\pi_T(v\mid c_t)$；随后用该目标对学生候选概率计算分支交叉熵。优化器将此分支损失与全轨迹OPD反向KL损失相加并更新$\theta$。

<div class="method-step__io" markdown="1">

**输入**：教师在$S_t^{k_p}$上的重归一化先验$\bar\pi_T^{k_p}$、候选价值$\hat V_t(v)$、逆温度$\gamma$及分支权重$\beta$。<br>
**输出**：既匹配教师整体分布、又提高高价值候选概率的更新后学生策略$\pi_\theta$。

</div>

**直观理解**：教师相当于给候选设定初始票数，验证器根据完整解题结果追加票数；$\gamma$控制结果证据能在多大程度上改变教师排序。训练仍以普通OPD为主体，稀疏分支信号只负责校正关键决策。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 位置采集分数

$$
\begin{aligned} C_t^{k_s}&=\sum_{v\in S_t^{k_s}}\pi_T(v\mid c_t),\\ A_t^{k_s}&=\sum_{v\in S_t^{k_s}}\pi_{\theta_{\mathrm{old}}}(v\mid c_t),\\ G_t^{k_s}&=\lambda_{\mathrm{mass}}(1-A_t^{k_s})+\lambda_{\mathrm{shape}}D_{\mathrm{JS}}\!\left(\bar\pi_T^{k_s}\,\|\,\bar\pi_{\theta_{\mathrm{old}}}^{k_s}\right),\\ s_t&=\bar H_T(c_t)\,C_t^{k_s}\,G_t^{k_s},\qquad \lambda_{\mathrm{mass}}+\lambda_{\mathrm{shape}}=1. \end{aligned}
$$

**符号说明**

- $t$：学生轨迹中的词位索引。
- $c_t$：位置$t$之前的上下文前缀，即$c_t=(q,x_{<t})$。
- $k_s$：计算位置评分时采用的教师候选数量。
- $S_t^{k_s}$：教师在前缀$c_t$上的top-$k_s$候选词集合。
- $v$：候选集合中的一个词元。
- $\pi_T$：教师策略的全词表条件概率分布。
- $\pi_{\theta_{\mathrm{old}}}$：本轮采样和探测使用的冻结旧学生策略。
- $C_t^{k_s}$：教师top-$k_s$集合捕获的教师总概率质量。
- $A_t^{k_s}$：旧学生分配给同一教师候选集合的总概率质量。
- $\bar\pi_T^{k_s}$：教师分布限制在$S_t^{k_s}$后重新归一化得到的相对形状。
- $\bar\pi_{\theta_{\mathrm{old}}}^{k_s}$：旧学生分布限制在$S_t^{k_s}$后重新归一化得到的相对形状。
- $D_{\mathrm{JS}}$：归一化到$[0,1]$的Jensen–Shannon散度，用于衡量两个候选分布形状的差异。
- $\lambda_{\mathrm{mass}}$：质量覆盖不足项的权重。
- $\lambda_{\mathrm{shape}}$：候选相对形状差异项的权重，且与$\lambda_{\mathrm{mass}}$之和为$1$。
- $G_t^{k_s}$：教师候选集合上的师生差距。
- $\bar H_T(c_t)$：除以$\log|\mathcal V|$后的教师熵，取值位于$[0,1]$。
- $s_t$：位置$t$的最终采集优先级分数。

<div class="equation-explanation" markdown="1">

**直观理解**：高$\bar H_T(c_t)$寻找存在多种选择的位置，高$C_t^{k_s}$排除不确定性散落在长尾中的位置，高$G_t^{k_s}$排除学生已经充分掌握教师候选的情况。三者相乘后，只有同时满足“教师确有紧凑备选”和“学生确需纠正”的位置才会优先进入top-$M$探测集合。<br>
**原文位置**：第3.2节，公式（5）至（7）

</div>

</div>

<div class="equation-block" markdown="1">

#### 结果校准目标与联合训练目标

$$
\begin{aligned} \tilde\pi_T(v\mid c_t)&=\frac{\bar\pi_T^{k_p}(v\mid c_t)\exp\!\left(\gamma\hat V_t(v)\right)}{\sum_{u\in S_t^{k_p}}\bar\pi_T^{k_p}(u\mid c_t)\exp\!\left(\gamma\hat V_t(u)\right)},\\ \mathcal L_t^{\mathrm{Branch}}&=-\sum_{v\in S_t^{k_p}}\tilde\pi_T(v\mid c_t)\log\pi_\theta(v\mid c_t),\\ \mathcal L&=\frac{1}{T}\sum_{t=1}^{T}\mathcal L_t^{\mathrm{OPD}}+\frac{\beta}{\max\{1,|\mathcal B^+|\}}\sum_{t\in\mathcal B^+}\mathcal L_t^{\mathrm{Branch}}. \end{aligned}
$$

**符号说明**

- $\tilde\pi_T$：结合教师先验和候选后续回报得到的结果校准目标分布。
- $v$：当前被校准的教师候选词。
- $u$：归一化求和中遍历的教师候选词。
- $c_t$：学生轨迹在位置$t$之前的前缀。
- $k_p$：每个入选位置实际探测的教师候选数量。
- $S_t^{k_p}$：教师在$c_t$上的top-$k_p$探测候选集合。
- $\bar\pi_T^{k_p}$：教师概率限制在$S_t^{k_p}$并重新归一化后的提议先验。
- $\hat V_t(v)$：旧学生在强制选择$v$后继续生成所得验证器回报的期望估计。
- $\gamma$：正的逆温度参数，控制结果价值改变教师先验的强度。
- $\mathcal L_t^{\mathrm{Branch}}$：位置$t$上以结果校准分布为软标签的分支交叉熵损失。
- $\pi_\theta$：待优化的当前学生策略。
- $\mathcal L$：SPOT的总训练损失。
- $T$：原始学生轨迹的长度。
- $\mathcal L_t^{\mathrm{OPD}}$：位置$t$的标准OPD反向KL损失，即学生分布到教师分布的KL散度。
- $\beta$：分支蒸馏相对于全轨迹OPD的损失权重。
- $\mathcal B^+$：探测后至少有一个正价值候选的位置集合。
- $|\mathcal B^+|$：保留位置的数量，用于平均分支损失。

<div class="equation-explanation" markdown="1">

**直观理解**：第一式把每个候选的教师概率乘以其结果权重：价值差每增加一单位，候选间赔率就按$\exp(\gamma)$的比例调整；当$\gamma\to0$时目标退化为教师先验。后两式让学生拟合该校准分布，并与覆盖整条轨迹的OPD损失联合训练；若$\mathcal B^+=\varnothing$，分支项为零，方法自动退化为标准OPD。<br>
**原文位置**：第3.2节，公式（10）与（12）；校准目标来源于公式（9）的KL约束优化

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：标准部分在学生实际访问的每个前缀上最小化$\mathcal L_t^{\mathrm{OPD}}=D_{\mathrm{KL}}(\pi_\theta(\cdot\mid c_t)\|\pi_T(\cdot\mid c_t))$，使学生在整条轨迹上接近教师；新增部分只在$\mathcal B^+$上，以$\tilde\pi_T$为软标签最小化分支交叉熵。分支损失除以$\max\{1,|\mathcal B^+|\}$，避免保留位置数量改变其整体尺度，$\beta$控制局部校正与全轨迹蒸馏的权衡。训练数据由冻结行为策略$\pi_{\theta_{\mathrm{old}}}$采集，实际优化采用PPO风格裁剪以控制新旧学生策略之间的更新幅度；每轮完成梯度更新后，再把新学生复制为下一轮行为策略。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 乘积式位置采集器**

采集器把$\bar H_T(c_t)$、$C_t^{k_s}$与$G_t^{k_s}$相乘。$G_t^{k_s}$进一步结合学生赋给教师候选集的总质量不足$1-A_t^{k_s}$，以及师生在该集合内重归一化分布的Jensen–Shannon散度；前者检查学生是否整体低估这些候选，后者检查学生是否错误排列候选间的相对概率。

> 直观理解：该模块不是寻找所有不确定位置，而是寻找最值得纠正的不确定位置。乘法形成一种“软与门”：任一因素接近零时，位置就不会因其他单一因素很高而大量消耗探测预算。

**2. 验证器引导的稀疏分支探测器**

探测器强制采用教师提出的局部候选$v$，但后续由旧学生策略完成，因此$\hat V_t(v)$衡量的是候选对当前学生是否可执行，而非教师自己能否沿该分支成功。位置预算$M$、候选预算$k_p$与每候选采样预算$N_p$共同显式限制额外生成开销。

> 直观理解：一个候选词即使对强教师有用，也可能让弱学生无法继续；让学生亲自完成后续生成，可以检验这条分支是否适合当前能力。稀疏预算则避免在每个词位进行昂贵的完整解题试验。

**3. KL约束的结果校准器**

校准器在教师top-$k_p$候选集的概率单纯形上最大化期望价值，同时约束新目标与教师先验之间的KL散度不超过$\epsilon$；其闭式解是教师概率与价值指数权重的乘积。候选$v$相对候选$u$的目标对数优势等于教师先验对数优势加$\gamma(\hat V_t(v)-\hat V_t(u))$，因此统一平移全部回报不会改变候选间排序。

> 直观理解：直接选择样本回报最高的候选容易受少量随机续写影响，完全沿用教师概率又忽略真实结果。KL约束在两者之间折中：结果较好的候选获得更多概率，但教师原有知识仍是稳定锚点。

**训练与推理**

训练时，对每批$q\sim\mathcal D$执行“旧学生生成原轨迹、教师逐前缀打分、top-$M$位置采集、top-$k_p$候选分支续写、验证器评分、正回报门控、构造$\tilde\pi_T$、联合损失更新”这一闭环。探测分支仅用于产生训练目标，不要求把分支续写直接并入最终答案；其价值明确依赖当前旧学生的续写能力，因此随着学生更新，候选价值和入选位置也会重新估计。

原文方法章节未提出专用推理算法。训练完成后可直接使用更新后的学生策略$\pi_\theta$按常规解码生成答案，不再需要教师、位置采集器、额外分支续写或验证器；因此额外探测成本发生在训练阶段，而部署接口与普通自回归学生模型一致。

**复现信息**

公平理解该方法所需的关键设置是：评分候选数$k_s$与实际探测候选数$k_p$彼此独立，前者用于低成本判断位置是否值得探测，后者决定昂贵分支探索的宽度；总探测上界为每条轨迹$M k_p N_p$次续写。主实验中的OPD、EOPD、GRPO与SPOT使用verl实现，并由SGLang异步生成轨迹；OPD、EOPD和SPOT使用每提示$1$个样本，而GRPO使用每提示$8$个样本。共同的主要训练设置包括学习率$3\times10^{-6}$、AdamW、余弦学习率调度、训练批大小$128$、小批大小$32$和采样温度$1.0$；主实验使用$4$张A800、FSDP2及bfloat16。所给节选未完整报告$M$、$k_s$、$k_p$、$N_p$、$\gamma$、$\lambda_{\mathrm{mass}}$和$\lambda_{\mathrm{shape}}$的具体取值，复现时仍需核对论文其余实现表格或代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 训练数据：Qwen3-0.6B-Base 与 Qwen3-1.7B-Base 学生在 MATH 上训练；Qwen3-4B-Base 使用难度更高的 DAPO 数据集。跨模型家族实验中，Llama-3.2-3B-Instruct 学生同样在 MATH 上训练三个 epoch。原文节选未明确报告训练样本数、具体划分及 DAPO 子集规模。
- 主要数学评测套件：MATH-500、AIME 2024、AIME 2025、AMC 2023、Minerva Math 和 HMMT 2025，共覆盖一般竞赛数学、较高难度竞赛题及不同来源的数学推理问题。六个基准均用于零样本评测，并计算不加权宏平均，以检验收益是否只来自某一个数据集。
- 域外评测套件：GPQA-Diamond 检验高难度科学推理，MMLU-Pro 检验跨学科知识与推理，AlpacaEval 2.0 检验开放式指令跟随和偏好胜率。它们用于判断仅在 MATH 上训练的 Qwen3-1.7B-Base 是否能把分支校准能力迁移到非数学任务。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Avg@8**

每道题采样八个回答后，对单次回答正确率取平均，近似衡量随机生成一次答案时的平均质量。 （越高越好，因为它表示单个生成样本更可能正确；但它不能单独反映八次尝试是否覆盖到至少一条正确但低概率的推理路径。）

</div>
<div class="metric-item" markdown="1">

**Pass@8**

八个采样回答中至少有一个正确的问题比例，主要衡量多样采样对可行解路径的覆盖能力。 （越高越好，因为它表示有限次数搜索更可能命中正确解；不过较高的 Pass@8 不必然意味着每次回答都更可靠，因此需要与 Avg@8 联合判断。）

</div>
<div class="metric-item" markdown="1">

**宏平均**

先分别计算各基准得分，再对六个数学基准作不加权平均；每个基准权重相同，不因题目数量不同而改变。 （越高越好，因为它表示跨基准的总体表现更强；但不加权平均可能掩盖某些单独任务上的退化。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个 Qwen3 学生规模、MATH 与 DAPO 训练设置下的六项数学基准宏平均

<div class="result-value" markdown="1">

作者报告，SPOT 在全部三个学生规模上取得最高的宏平均 Pass@8，并取得最高或第二高的宏平均 Avg@8。相对标准 OPD，宏平均 Avg@8 提升 $0.47$ 至 $1.48$ 个百分点，宏平均 Pass@8 提升 $4.55$ 至 $5.28$ 个百分点；相对最接近的 EOPD，前者提升 $0.29$ 至 $0.68$ 个百分点，后者提升 $2.49$ 至 $3.19$ 个百分点。

</div>

较大的 Pass@8 增益说明 SPOT 更容易让八次采样覆盖至少一条正确推理路径，而 Avg@8 没有随之下降，说明这种覆盖扩张并非简单地用大量低质量回答换取偶然命中。由于收益同时出现在 $0.6$B、$1.7$B 和 $4$B 学生以及两种训练数据设置中，它不像是单一容量或单一数据集造成的现象。不过，该结果只能支持受测模型和数学基准内的一致性，不能证明对所有规模、教师或任务都成立；节选也没有提供方差和显著性检验。

<div class="result-source" markdown="1">

来源：第 4.2 节 Main Results，Table 1 的文字分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Relative to standard OPD, SPOT improves macro Avg@8 by 0.47–1.48 points and macro Pass@8 by 4.55–5.28 points. Relative to EOPD, the closest uncertainty-aware OPD baseline, SPOT improves macro Avg@8 by 0.29–0.68 points and macro Pass@8 by 2.49–3.19 points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-1.7B-Base 仅在 MATH 上训练后的域外迁移

<div class="result-value" markdown="1">

在 GPQA-Diamond 上，SPOT 的 Avg@8 为 $29.42\%$、Pass@8 为 $80.81\%$，相对该任务最强基线分别提高 $2.21$ 和 $11.62$ 个百分点；在 AlpacaEval 2.0 上，原始 WR 为 $34.63\%$，领先最强基线 $1.40$ 个百分点。MMLU-Pro Pass@1 为 $42.26\%$，低于 EOPD 的 $42.90\%$；AlpacaEval 的 LC-WR 为 $27.59\%$，也低于 EOPD 的 $28.13\%$。

</div>

域外收益呈现任务结构差异：结果校准对需要展开多步推理的 GPQA-Diamond 最明显，但在广域知识问答上没有全面超过熵驱动的 EOPD。AlpacaEval 中原始 WR 最优而长度控制后次于 EOPD，说明部分偏好优势可能与回答长度相关，不能全部归因于指令质量提升。因此，这组实验支持“能迁移但并非统一占优”，而不是普遍的域外优势。

<div class="result-source" markdown="1">

来源：Appendix C.1，Table 9 及其后文字分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Relative to the strongest baseline on GPQA-Diamond, SPOT improves Avg@8 by 2.21 points and Pass@8 by 11.62 points, and it leads AlpacaEval WR by 1.40 points. On MMLU-Pro, SPOT ranks second at 42.26: it trails EOPD by only 0.64 points, while exceeding GRPO and OPD by 0.40 and 1.03 points, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Llama-3.2-3B-Instruct 学生与 Llama-3.1-8B-Instruct 教师的跨模型家族实验

<div class="result-value" markdown="1">

在四个数学基准的家族内宏平均上，SPOT 的 Avg@8 为 $17.53\%$、Pass@8 为 $34.05\%$；对应 OPD 为 $12.57\%$ 和 $29.65\%$，EOPD 为 $14.62\%$ 和 $31.51\%$，GRPO 为 $17.45\%$ 和 $31.44\%$。SPOT 因而同时取得该设置下最高的宏平均 Avg@8 与 Pass@8。

</div>

这一结果表明 SPOT 相对基线的排序模式不只出现在 Qwen3 上：更换教师、学生架构、检查点类型和师生规模后，覆盖率优势仍然存在。SPOT 的宏平均 Avg@8 只略高于 GRPO，因此平均单样本质量方面的跨家族优势较小，主要差异体现在 Pass@8。该实验只能作 Llama 家族内部的方法比较，不能将其绝对分数与 Qwen 实验直接比较，也不足以证明对更多模型家族均有效。

<div class="result-source" markdown="1">

来源：Appendix C.2，Table 10，列顺序为 GRPO、OPD、EOPD、SPOT

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Macro avg. Avg@8 17.45 12.57 14.62 17.53 Pass@8 31.44 29.65 31.51 34.05

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给章节没有提供真正隔离单个组件的消融结果，例如分别移除归一化教师熵、top-$k_s$ 候选质量、师生失配项、验证器结果或 KL 正则。因此，主结果只能证明完整 SPOT 流程有效，不能确定哪一组件是收益的必要条件，也不能排除组件之间的交互作用。
- 实验未在节选中报告多随机种子均值、标准差、置信区间或统计显著性；主要比较还依赖同一套提示、答案验证器及八次随机采样。尤其对题量较小的 AIME 类基准和基于偏好判断的 AlpacaEval，数值差异可能受采样波动、验证器误差、回答长度以及有效判断数不完全一致的影响。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- KD：在教师生成的数据上，以前向 KL 散度和交叉熵进行离策略蒸馏。它代表传统的教师轨迹模仿，用于判断学生自生成轨迹和稀疏探测是否确有额外价值。
- OPD：在学生 rollout 上施加逐 token 的反向 KL 监督，是 SPOT 的直接基础方法。与它比较可衡量稀疏候选探测及结果校准目标带来的整体增益。
- GRPO：根据可验证奖励计算组相对优势，不使用教师监督。它用于区分 SPOT 的收益究竟来自结果反馈本身，还是来自结果反馈与教师分布约束的结合。
- EOPD：在固定教师熵阈值选中的位置加入 top-$k$ 前向 KL 项，是最接近 SPOT 的不确定性感知 OPD 基线。该比较主要检验仅依据教师熵选择位置，是否不如同时考虑归一化熵、候选概率质量、师生失配和后续结果。

**实验想回答的问题**

- 在教师、训练数据和评测协议受控的条件下，SPOT 是否比标准知识蒸馏 KD、标准在策略蒸馏 OPD、结果奖励强化学习 GRPO，以及基于教师熵选点的 EOPD，取得更好的数学推理准确率与多次采样覆盖率？
- SPOT 的收益能否跨学生规模、训练数据难度和模型家族保持，并从数学训练迁移到科学推理、广域知识与指令跟随任务？

**实验实现**

主要 Qwen 实验统一采用关闭 thinking mode 的 Qwen3-8B 作为蒸馏教师，并以 Qwen3-0.6B-Base、Qwen3-1.7B-Base 和 Qwen3-4B-Base 作为学生。所有模型使用相同提示模板和答案验证器进行零样本评测；每题采样八个回答，温度为 $1.0$，采用参数 $p=0.8$ 的 top-$p$ 采样，最大回答长度为 $8192$ 个 token。Llama 扩展实验使用 Llama-3.1-8B-Instruct 教师和 Llama-3.2-3B-Instruct 学生，在相同的八次采样解码条件下作家族内比较。域外实验中，GPQA-Diamond 每题采样八次，MMLU-Pro 使用类别匹配的五样本思维链示例并报告 Pass@1，AlpacaEval 2.0 同时报告原始胜率 WR 和长度控制胜率 LC-WR。原文节选未明确报告随机种子、重复训练次数、置信区间或显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向在策略蒸馏的稀疏探测与结果校准方法，以提升语言模型推理性能。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`3ee9cc55d336194ecf6155009640869180c544eff2ce12be1483da86d8e56f81`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
