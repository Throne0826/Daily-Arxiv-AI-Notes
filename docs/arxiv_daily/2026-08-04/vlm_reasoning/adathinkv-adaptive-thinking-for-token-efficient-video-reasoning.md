---
title: "[论文解读] AdaThinkV: Adaptive Thinking for Token-Efficient Video Reasoning"
description: "[arXiv 2608.01980][VLM Reasoning] AdaThinkV将视频问答中的推理模式选择表述为“显式推理带来的准确率增益是否足以抵偿额外生成成本”，并通过配对采样与方差恢复训练，让模型按问题自适应地决定直接回答还是展开推理。"
arxiv_id: "2608.01980"
announcement_date: "2026-08-04"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:01:06.047517+00:00"
source_sha256: "3e86583dbdef263eacda1443454dffcc1b23c93ec845a9c8a2e317eaea02dd27"
tags:
  - "VLM Reasoning"
  - "VLM Efficiency"
  - "强化学习"
  - "LLM Reasoning"
  - "视频多模态大语言模型"
  - "自适应推理"
  - "显式思维链"
  - "词元效率"
  - "条件净效用"
  - "组相对强化学习"
  - "奖励方差恢复"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.01980</p>

# AdaThinkV: Adaptive Thinking for Token-Efficient Video Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Jingqi Tian, Haoji Zhang, Lin Chen, Hongbo Jin, Haonan Xu, Tianrui Zhu, Xingming Shui, Shilin Ma, Wenjing Yang, Yansong Tang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Tsinghua Shenzhen International Graduate School, Tsinghua University；Alibaba Group；Peking University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01980v1) · [PDF 下载](https://arxiv.org/pdf/2608.01980v1) · **关键词** 视频多模态大语言模型, 自适应推理, 显式思维链, 词元效率, 条件净效用, 组相对强化学习, 奖励方差恢复<br>


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

AdaThinkV将视频问答中的推理模式选择表述为“显式推理带来的准确率增益是否足以抵偿额外生成成本”，并通过配对采样与方差恢复训练，让模型按问题自适应地决定直接回答还是展开推理。

**不用术语来说**：视频问题的难度差异很大：识别画面中的简单事实通常可以立即作答，而事件排序、状态追踪和因果分析往往需要逐步整理跨帧证据。若所有问题都生成很长的思考过程，简单题会浪费计算和输出长度，甚至可能被过度分析；若一律直接回答，复杂题又容易因证据收集不足而出错。因此，模型需要针对当前视频和问题判断“多想一步是否真的值得”。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出以提示级“推理条件净效用”作为模式选择依据，并设计 ThinkGain：对同一输入分别采样显式推理与直接回答结果，用两种模式的经验准确率差衡量收益，同时扣除显式推理增加的响应长度，从而无需离线难度标签、人工置信度阈值或外部路由器即可产生训练监督。
- 作者提出方差恢复策略 VRPO，保留奖励全不成功、低离散度的困难问题采样组，并在同一组上逐步增加样本，以尝试发现成功轨迹和恢复强化学习信号；这针对固定采样探索不足以及只保留非零方差组可能造成的奖励分布偏差。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于视频多模态大语言模型（video MLLM）的自适应推理研究。此类模型需要结合视频中的视觉、时间顺序与文本问题生成答案；显式思维链能够帮助处理事件排序、状态跟踪和因果分析等组合问题，却会增加输出长度，并可能把简单感知问题复杂化。因此，本文关注的核心不是单纯提高推理能力，而是让模型针对每个问题判断显式推理带来的准确率收益是否足以抵偿额外的生成成本。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**显式思维链（Chain-of-Thought, CoT）**

模型在最终答案之前输出可见的中间推理步骤，以分解需要多步判断的问题。它可能提高复杂视频推理的正确率，但会消耗更多解码词元，且不保证对每个问题都有帮助。

</div>
<div class="concept-item" markdown="1">

**自适应推理**

模型根据当前输入，在直接回答与显式推理后回答之间选择响应模式。本文要求这种选择由模型自主完成，而不依赖离线难度标签、人工置信度阈值或外部路由器。

</div>
<div class="concept-item" markdown="1">

**组相对强化学习（Group-relative RL）**

对同一提示采样一组回答，并根据组内奖励的相对差异更新生成策略，从而避免额外训练价值模型。若组内所有回答都失败、准确性奖励几乎没有差异，模型便难以获得有效学习信号。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是视频与对应的文本问题，模型需要先选择 $s(x)\in\{\mathrm{THINK},\mathrm{ANSWER}\}$：前者表示生成显式推理过程后作答，后者表示直接作答；输出则是模式标记及其后可变长度的回答序列。训练处于强化学习设置：对同一提示 $x$ 分别采样匹配的 THINK 与 ANSWER 分支，通过比较两种模式的任务正确性和响应长度，估计显式推理的条件净效用。基本假设是问题难度不能可靠地由置信度直接代表：低置信度不意味着继续推理一定有效，高置信度也可能掩盖遗漏的时间证据；因而模式决策应依据“额外推理实际改善答案多少，以及为此增加多少生成成本”。推理阶段不先生成试探答案，也不调用独立控制器，而是在一个自回归序列中依次生成模式标记和最终响应。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

一个提示实例，即视频及其对应的文本问题。

</div>
<div class="notation-item" markdown="1">

**$s(x)$**

模型针对提示所选择的响应模式，取值为 THINK 或 ANSWER。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{THINK}$**

先输出可见的多步推理过程，再生成答案的模式。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{ANSWER}$**

不输出显式推理过程、直接生成答案的模式。

</div>

</div>

**直接相关的工作**

- **VideoAuto-R1**: 这是与本文最直接相关的视频自适应推理方法：它依据初步答案的置信度选择响应模式。AdaThinkV认为置信度只是间接代理，不能回答额外推理是否真正改善答案并值得其词元成本；同时，AdaThinkV不需要预先生成答案或设置人工置信度阈值。
- **GRPO / DAPO**: GRPO提供无价值模型的组相对策略优化框架；DAPO通过动态采样过滤准确性奖励无变化的组，以保留固定数量的有效提示。本文指出，直接过滤可能丢弃困难但可解的问题并使观测到的奖励离散程度偏高，因此将这类组保留下来并逐步扩充采样，以恢复可用于学习的奖励差异。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

显式思维链能够帮助视频多模态大模型完成时间关系、事件顺序、状态变化和因果关系等组合推理，但其收益并非对每个问题都成立。实际系统既要保证复杂视频问题的正确率，也要控制自回归解码所消耗的输出 token；固定使用长推理或固定使用短回答都无法同时满足这两个目标。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **固定响应模式**：模型对所有输入统一采用显式思维链，或者统一直接给出答案。前者依靠较长的可见推理轨迹处理复杂问题，后者通过缩短响应降低生成成本。
- **基于置信度的自适应路由（如 VideoAuto-R1）**：模型先生成初步答案或估计其置信度，再依据预设阈值决定是否切换到显式推理模式，以不确定性作为问题是否需要继续思考的替代指标。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定模式忽略问题间的推理需求差异：始终推理会在简单感知题上浪费 token，并可能因过度分析而降低表现；始终直接回答则可能在需要跨时间收集证据的组合问题上思考不足。
- 置信度只是不完全的间接指标：低置信度不代表额外推理一定能改善答案，高置信度也可能建立在遗漏关键时间证据的基础上；此外，初步回答、人工阈值或外部路由会引入额外推断步骤与系统设计依赖。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种可直接估计“对同一视频问题展开显式推理后，正确性提升是否超过额外响应成本”的提示级学习信号；同时，对于困难但可解的问题，有限 rollout 可能全部失败并产生近乎零方差的奖励，常规强化学习因而无法获得有效更新，而过滤这些组又可能系统性忽视难题并高估观测到的奖励离散度。

</div>
<div markdown="1"><span>核心问题</span>

视频多模态大模型能否在没有离线难度标签、人工置信度阈值和外部路由器的条件下，从训练时同一提示的两种响应模式及其结果中学习：当前问题应直接回答还是显式推理，并在一次自回归生成中完成模式选择与作答？

</div>
<div markdown="1"><span>作者直觉</span>

判断是否需要推理，不应只问模型“有多不确定”，而应做同题对照：比较直接回答和显式推理各自能否答对，以及后者多用了多少 token。若推理显著提高成功率且长度代价可接受，就应学习选择推理；若收益很小，则直接回答更合算。对于首批尝试全部失败的难题，失败并不等于不可解，保留已有轨迹并逐步扩大同一组的探索范围，更可能找到少量成功样本，使组内奖励重新出现差异并形成可学习信号。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

AdaThinkV把视频问答建模为“先选择回答模式，再生成后续内容”的单序列自回归过程。输入是视频与问题组成的提示$x=(v,q)$；模型首先生成模式标记$c\in\{\mathtt{THINK},\mathtt{ANSWER}\}$，随后生成续写$u$：$\THINK$模式包含显式推理轨迹$h$和最终答案$a$，$\ANSWER$模式只包含$a$。训练分为平衡格式数据上的监督微调冷启动和强化学习两个阶段。强化学习时，同一提示被强制分配到两种模式并进行匹配采样；ThinkGain根据两种分支的准确率差和额外长度成本产生提示级模式偏好，VRPO则为“当前全部失败且奖励差异过小”的困难提示逐步增加采样，从而恢复可用于组内相对优化的奖励变化。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 平衡双模式冷启动

在两种格式数量平衡的样本上进行监督微调，使策略$\pi_\theta$学会输出合法标记、显式推理续写或直接回答续写。该阶段同时建立格式遵循能力，避免强化学习初期因某一模式几乎不被生成而无法比较。

<div class="method-step__io" markdown="1">

**输入**：带视频$v$、问题$q$和目标回答的训练样本，以及$\THINK$和$\ANSWER$两种序列化格式。<br>
**输出**：能够条件化生成两种回答格式的初始策略。

</div>

**直观理解**：先教会模型两种基本答题方式：一种写思考过程，一种直接给答案；此时还不要求它准确判断何时应使用哪一种。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提示匹配的双分支采样

对每个提示采样$G$条轨迹，其中$G_{\rm think}=\lfloor\rho G\rfloor$条被强制以$\THINK$标记开头，其余以$\ANSWER$开头；标记由轨迹位置指定，且从策略梯度损失中屏蔽。两分支共享输入与解码配置，因此可以在同一提示内部比较准确率和标记后的续写长度。

<div class="method-step__io" markdown="1">

**输入**：当前策略、同一提示$x$、初始组大小$G_0$和强制思考比例$\rho$。<br>
**输出**：带模式身份、任务准确率奖励$r_i^{\rm acc}$和续写长度$\ell_i$的配对轨迹组。

</div>

**直观理解**：这相当于让同一道题分别采用“先想”和“直接答”多次作答，再比较哪种方式更划算，从而尽量排除不同题目难度造成的干扰。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### ThinkGain模式效用估计

计算显式推理相对直接回答的净收益$\widehat{\Delta}(x)$；当其大于$\tau$时令目标模式$c^*(x)=\mathtt{THINK}$，小于$-\tau$时令$c^*(x)=\mathtt{ANSWER}$，落入死区时不提供模式标签。有效目标通过模式标记的监督似然训练自主选择能力，同时模式一致性奖励调整对应续写轨迹的优势。

<div class="method-step__io" markdown="1">

**输入**：同一提示下两种模式的平均准确率、平均续写长度，以及长度成本系数$\lambda$、归一化常数$B$和死区阈值$\tau$。<br>
**输出**：提示级模式偏好$c^*(x)$及用于续写优化的复合奖励。

</div>

**直观理解**：模型不是把“难题”等同于“必须思考”，而是直接估计思考带来的正确率提升是否值得额外生成成本；证据不明显时暂不下结论，以减少噪声标签。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### VRPO方差恢复与策略更新

若组内已有成功与失败对比，或连续准确率奖励的离散度超过$\delta_{\rm acc}$，则保留该组；若所有轨迹均失败、离散度不足且$G_x<G_{\max}$，则保留旧轨迹并按两种模式平衡追加采样，否则丢弃。对最终保留组计算组内标准化优势，使用带非对称裁剪和过长掩码的DAPO式策略目标更新续写，并联合优化模式选择损失。

<div class="method-step__io" markdown="1">

**输入**：当前轨迹组的成功指示$s_i$、准确率奖励离散度$\sigma_{\rm acc}(x)$、最大组大小$G_{\max}$及各轨迹的复合奖励。<br>
**输出**：同时改善条件续写质量和自主模式选择的更新策略$\pi_\theta$。

</div>

**直观理解**：普通固定采样遇到“所有答案都错”时无法知道哪个答案相对更好；VRPO只给这类可能仍可解决的题追加尝试，直到出现有区分度的反馈或达到预算上限。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### ThinkGain净推理效用与模式目标

$$
\widehat{\Delta}(x)=\overline{r}^{\rm acc}_{\rm think}-\overline{r}^{\rm acc}_{\rm answer}-\lambda\frac{\overline{\ell}_{\rm think}-\overline{\ell}_{\rm answer}}{B},\qquad c^{*}(x)=\begin{cases}\mathtt{THINK},&\widehat{\Delta}(x)>\tau,\\ \mathtt{ANSWER},&\widehat{\Delta}(x)<-\tau,\\ \emptyset,&|\widehat{\Delta}(x)|\leq\tau.\end{cases}
$$

**符号说明**

- $x=(v,q)$：由视频$v$和问题$q$组成的输入提示
- $\overline{r}^{\rm acc}_{\rm think},\overline{r}^{\rm acc}_{\rm answer}$：同一提示下思考分支与直接回答分支的平均归一化任务准确率奖励
- $\overline{\ell}_{\rm think},\overline{\ell}_{\rm answer}$：两种模式在开头标记之后的平均续写token数
- $\lambda$：额外解码长度的成本权重
- $B$：把长度差归一化到适当尺度的常数
- $\widehat{\Delta}(x)$：提示$x$上显式推理相对直接回答的蒙特卡洛净效用估计
- $\tau$：抑制小幅、噪声性效用差异的非负死区阈值
- $c^*(x)$：提示级模式监督目标；空集表示该提示不参与模式似然监督

<div class="equation-explanation" markdown="1">

**直观理解**：第一项衡量“先思考”多带来多少正确率，第二项扣除它多生成的token成本。只有净收益明显为正或明显为负时才给出模式标签，因此该标签是有限采样下的效用偏好，并非作者声称的真实难度标签或统计显著性结论。<br>
**原文位置**：Method，ThinkGain: Prompt-Matched Estimation of Reasoning Gain，式(1)与式(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 联合训练目标

$$
\mathcal{L}_{\rm total}=\mathcal{L}_{\rm RL}+\gamma\mathcal{L}_{\rm mode},\qquad \mathcal{L}_{\rm mode}=-\frac{1}{N_{\rm mode}}\sum_{\substack{x\in\mathcal{B}_{\rm RL}\\c^*(x)\neq\emptyset}}\log\pi_\theta\!\left(m(c^*(x))\mid x\right)
$$

**符号说明**

- $\mathcal{L}_{\rm total}$：最终最小化的总训练损失
- $\mathcal{L}_{\rm RL}$：作用于模式标记之后续写token的裁剪策略优化损失
- $\mathcal{L}_{\rm mode}$：使模型在看到提示后提高目标模式标记似然的监督损失
- $\gamma$：模式监督相对强化学习目标的权重
- $\mathcal{B}_{\rm RL}$：经VRPO筛选后保留、用于策略更新的提示组缓冲区
- $N_{\rm mode}$：当前缓冲区中具有非空模式目标的提示数量
- $m(c^*(x))$：目标模式对应的完整序列化开头标记
- $\pi_\theta$：参数为$\theta$的自回归视频多模态策略

<div class="equation-explanation" markdown="1">

**直观理解**：总目标把两个问题拆开处理：强化学习提高“进入某种模式后怎样继续生成”的质量，模式似然损失学习“面对当前问题先选哪种模式”。强制标记本身被屏蔽于策略梯度，因此模式选择不会被错误地当作旧策略自然采样的动作。<br>
**原文位置**：Method，Mode selection learning，式(3)；Optimization relative to each group，式(7)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：每条轨迹的复合奖励为$r_i=r_i^{\rm acc}+r_i^{\rm fmt}+r_i^{\rm ol}+g_i$：$r_i^{\rm acc}$评价任务正确性，$r_i^{\rm fmt}$评价是否符合被分配的序列格式，$r_i^{\rm ol}$是在长度上限附近的软惩罚，$g_i$则奖励轨迹模式与ThinkGain目标一致。VRPO是否扩展或保留一个组只依据任务成功和$r_i^{\rm acc}$的离散度，不依赖格式、长度或模式奖金，因此这些辅助奖励不会取代任务正确性标准。

对每个保留组，系统在全部$G_x$条轨迹内标准化复合奖励，得到轨迹优势$\widehat A_i$，并把同一优势赋给该轨迹的全部续写token。$\mathcal{L}_{\rm RL}$采用新旧策略续写概率之比和非对称裁剪，其中较紧的下降边界限制破坏性概率下降，较宽的上升边界允许有利但原本低概率的token更快增大；被生成上限截断的响应由硬掩码移除。每个提示内部按未屏蔽token总数归一化，避免先逐响应平均产生隐含的$1/|u_i|$权重，也避免VRPO扩展后的大组支配小批量。最终以$\mathcal{L}_{\rm total}=\mathcal{L}_{\rm RL}+\gamma\mathcal{L}_{\rm mode}$联合更新；作者不使用KL惩罚或独立参考模型，旧策略$\pi_{\theta_{\rm old}}$仅用于重要性比。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. ThinkGain**

ThinkGain在同一提示的受控双模式轨迹上估计条件准确率差，并扣除$\THINK$相对$\ANSWER$增加的归一化长度成本。估计值经死区映射为噪声模式目标$c^*(x)$：该目标一方面通过模式似然直接监督开头标记，另一方面通过$g_i=\alpha\mathbf{1}[c_i=c^*(x)]$影响续写轨迹的相对优势。

> 直观理解：它解决的是“是否值得思考”，而不是简单预测题目是否困难；即使一道题较难，只要显式推理没有稳定提高正确率，系统也不会把长推理当作默认选择。

**2. Variance Recovery Policy Optimization**

VRPO把任务成功与奖励离散度分开判断。二元任务直接以准确率奖励定义成功；连续任务以固定任务标准$\eta_{\rm task}$转成成功指示，同时保留原始连续奖励的离散度。它仅扩展满足$\max_i s_i=0$、$\sigma_{\rm acc}(x)\leq\delta_{\rm acc}$且$G_x<G_{\max}$的组，每次保留已有轨迹并维持两模式平衡；最终只有具有成功对比或足够奖励离散度的组进入强化学习缓冲区$\mathcal{B}_{\rm RL}$。

> 直观理解：该模块把额外算力集中到“目前全错、反馈又没有差别，但增加尝试后可能找到突破口”的提示上；全对但反馈无差别的简单组不会被无意义扩展。

**3. 双因素联合优化**

完整响应概率被分解为模式标记概率$\pi_\theta(m(c)\mid x)$和给定模式后的续写概率。训练中强制标记不接受策略梯度，而由$\mathcal{L}_{\rm mode}$直接学习自主模式选择；续写token由$\mathcal{L}_{\rm RL}$优化，使用组内标准化复合奖励、旧策略重要性比、非对称裁剪及DAPO过长掩码。

> 直观理解：“选择哪种答题方式”和“选定方式后怎样答好”由共享模型联合学习，但各自有清晰的监督入口，避免把训练时人为指定的模式误当成模型自己采样的动作。

**训练与推理**

训练首先在两种格式平衡的数据上进行一个阶段的SFT冷启动。强化学习阶段对每个提示从$G_0=8$开始，以$\rho=0.5$平衡强制两种模式；若组内已有成功与失败对比，或准确率奖励标准差超过$\delta_{\rm acc}$，直接保留。若所有响应均失败且离散度不足，则每轮为每种模式各增加4条轨迹，保留此前样本并重新计算ThinkGain，直至获得有效信号或达到$G_{\max}=32$；仍无有效差异的组被丢弃。该可选停止与轨迹复用可能引入选择偏差，原文明确将其作为风险，并称在补充材料中通过分阶段诊断和独立重采样更新组进行量化。

测试时不再强制模式，也不运行外部路由模型。策略依据$x$自回归生成完整开头标记；若生成$<think>$，则继续产生显式推理$h$、闭合标记和答案$a$，若生成$<answer>$则直接产生$a$。因此模式决定与答案生成只需一次连续解码，但二者共享参数意味着续写训练仍可能间接改变模式概率；直接作用于模式概率的信号来自$\mathcal{L}_{\rm mode}$。

**复现信息**

策略骨干为Qwen3-VL-8B，视觉编码器冻结；SFT与RL各训练一个epoch，全局批量为32。与方法解释直接相关的参数为ThinkGain的$\rho=0.5$、$\lambda=0.1$、$B=512$、$\tau=0.05$，模式一致性奖励权重$\alpha=0.3$及联合损失权重$\gamma=0.1$；VRPO采用$G_0=8$、$G_{\max}=32$，连续奖励任务使用$\eta_{\rm task}=0.5$和$\delta_{\rm acc}=0.05$，作者说明后二者未在下游测试集上调参。训练采样最多生成4096个token，策略裁剪边界为$\epsilon_{\rm low}=0.20$和$\epsilon_{\rm high}=0.28$。

在Qwen3-VL分词器下，$<think>$是1个token而$<answer>$是3个token，因此模式损失使用完整标记序列的似然，不做逐token长度归一化；所有强制标记token均从续写损失中屏蔽。训练使用16张NVIDIA H100 GPU；这些资源信息对解释VRPO的自适应采样成本是必要的，但具体分布式软件配置不影响核心算法。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 通用视频理解评测组：Video-MME、MVBench、LongVideoBench、MMVU和Video-MMMU，用于检验模型对多类视频问答及长视频内容的综合理解能力。原文给出各基准得分，但所供章节未说明测试集规模、划分方式和具体采样协议。
- 时序定位评测组：Charades-STA与ActivityNet检验模型能否从视频中定位与文本查询对应的时间区间；NExT-GQA同时检验答案准确率与证据片段定位质量。原文未明确报告这些评测所用划分和样本规模。
- 流式视频理解评测组：StreamingBench用于实时视频理解，报告RTVU准确率；OVO-Bench综合Real-Time与Backward两个轨道，考察模型在视频持续到达时的在线理解以及对既有内容的回溯能力。原文未明确报告评测规模与划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（Acc.）**

衡量回答正确的样本比例；表2中的各通用视频基准、NExT-GQA、StreamingBench及OVO-Bench均以准确率或准确率聚合值反映任务完成质量。表5的Acc.则是在表1所定义的六种评测设置上汇总，但所供章节未包含这六种设置的具体构成。 （越高越好，因为更高数值表示正确回答更多；但不同表中的准确率可能来自不同基准或聚合协议，不能直接跨表比较。）

</div>
<div class="metric-item" markdown="1">

**R@0.5与mIoU**

二者衡量时序定位质量。$R@0.5$表示预测时间区间与真实区间的交并比至少达到$0.5$的样本比例；mIoU表示预测区间与真实区间交并比的平均值。 （均为越高越好：$R@0.5$越高说明更多样本达到可接受的定位重合度，mIoU越高说明预测片段整体上与真实证据区间重合得更准确。）

</div>
<div class="metric-item" markdown="1">

**平均输出令牌数（Tok.）及格式正确率（Fmt.）**

Tok.衡量生成响应所消耗的平均输出长度，是推理成本的代理指标；Fmt.衡量输出遵守目标格式的样本比例。表5还报告Think比例，即选择显式推理模式的样本百分比，用于观察策略偏好，而不是单独的性能指标。 （在准确率相近时Tok.越低越好，因为生成成本更小；Fmt.越高越好，因为输出更稳定可解析。Tok.不能脱离准确率判断，Think比例也不存在统一的越高或越低越好。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 通用视频理解：Video-MME、MVBench、LongVideoBench、MMVU和Video-MMMU

<div class="result-value" markdown="1">

AdaThinkV依次取得72.1、72.5、68.1、71.4和65.3。相较同表最强的VideoAuto-R1-Q3，五项分别变化$+0.4$、$+0.5$、$+0.7$、$+0.3$和$+0.3$个百分点，并在五项上均为表内最高值。

</div>

作者结果支持AdaThinkV在多种通用视频基准上具有一致而非局部的优势。分析上，这些提升幅度较小，说明主要证据是跨基准的稳定领先，而不是单项大幅跃升；由于没有方差和显著性检验，也不能据此断言每个零点几分的差距都具有统计显著性。

<div class="result-source" markdown="1">

来源：表2，General video understanding benchmarks

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

AdaThinkV | 72.1 | 72.5 | 68.1 | 71.4 | 65.3

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 时序定位：Charades-STA、ActivityNet与NExT-GQA

<div class="result-value" markdown="1">

AdaThinkV在Charades-STA上达到75.2的$R@0.5$和64.0的mIoU，在ActivityNet上达到54.9和52.2，在NExT-GQA上达到81.4准确率和44.5 mIoU。相较VideoAuto-R1-Q3，对应六项分别提高$0.3$、$0.3$、$0.6$、$0.3$、$0.3$和$0.3$个百分点；但ActivityNet的$R@0.5$仍低于Time-R1的55.6。

</div>

结果表明AdaThinkV不仅能答题，也能较准确地指出视频中的相关时间区间，并在多数指标上取得表内最佳结果。它并未全面支配所有专用定位方法：ActivityNet的召回指标仍由Time-R1领先，因此更合理的结论是综合表现强且稳定，而不是每项定位能力都最优。

<div class="result-source" markdown="1">

来源：表3，Temporal grounding benchmarks

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

AdaThinkV | 75.2 | 64.0 | 54.9 | 52.2 | 81.4 | 44.5

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 流式视频理解：StreamingBench与OVO-Bench

<div class="result-value" markdown="1">

AdaThinkV在StreamingBench和OVO-Bench上分别取得79.79与64.02，超过表中次优结果HERMES-7B的79.44和Qwen3-VL-8B的63.51，领先幅度分别为$0.35$和$0.51$个百分点。

</div>

这说明AdaThinkV在视频逐步到达的在线场景中仍保持竞争力，其收益并不限于可一次读取完整视频的离线问答。不过差距不足一个百分点，且表中没有令牌成本、延迟或吞吐量，因此该结果只证明准确率领先，不能证明真实流式部署速度或计算效率更高。

<div class="result-source" markdown="1">

来源：表4，Streaming video understanding

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

AdaThinkV | 79.79 | 64.02

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

- Qwen2.5-VL-7B与Qwen3-VL-8B：通用视觉语言骨干基线，用于判断提升是否来自AdaThinkV的训练框架，而非仅来自基础模型本身；表2还表明VideoAuto-R1分别使用Qwen2.5和Qwen3骨干，因此可辅助进行近似的同骨干比较。
- VideoAuto-R1-Q2.5与VideoAuto-R1-Q3：最直接的自适应视频推理对照，检验AdaThinkV所学习的自主模式选择和推理预算分配是否优于已有自适应方案；其中Q2.5和Q3分别表示Qwen系列骨干。
- Temporal-RLT、Time-R1与VITAL：面向视频时序推理或时序定位的强化学习方法，用于检验AdaThinkV在定位指标上的收益是否能够超过专门面向时间信息建模的方法。
- TimeChat-Online-7B、StreamForest-7B与HERMES-7B：流式视频理解对照，用于判断AdaThinkV在实时输入场景中是否仍具有竞争力，而非只适用于离线完整视频。

**实验想回答的问题**

- AdaThinkV能否在通用视频理解、时序定位和流式视频理解等不同任务上，稳定超过同骨干模型及已有视频推理方法，而不是只对某一种题型有效？
- 由监督微调（SFT）形成模式与格式基础、再由强化学习（RL）学习自适应推理策略的两阶段训练，能否同时提高准确率、控制输出长度，并保持有效的输出格式？

**实验实现**

训练包含一个由10186条轨迹组成的SFT冷启动集合，以及一个含30495个仅提示输入的RL集合，覆盖图像推理、时序定位、文本推理和视频问答。每个任务族的SFT数据在直接回答与显式推理轨迹之间保持平衡；RL数据不预制特定模式的回答，而是在在线采样时控制THINK与ANSWER两类rollout的分配。评测分为通用视频理解、时序定位和流式视频理解三组，并通过表5在同一组六设置样本上比较RL only、SFT only及SFT后接RL。所供章节未明确报告视频帧采样、解码参数、随机种子、重复实验次数、方差或显著性检验，因此表中差值应视为单次报告结果。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 完整两阶段训练SFT→RL与SFT only比较 | SFT→RL将Acc.从36.80提高到40.79，即增加3.99个百分点；Fmt.从99.1%增至99.3%，Tok.从260.48降至257.20，Think比例则从33.9%升至49.1%。 | 该对照主要隔离SFT之后继续进行RL的作用：RL在几乎不增加平均输出长度、也不破坏格式稳定性的情况下提高了准确率，同时让模型更频繁但并非一律采用显式推理。由于没有“普通RL与VRPO”的直接对照，这一行只能证明追加RL阶段有效，不能单独证明收益来自VRPO。 | 表5，SFT and RL stage ablation<br><span class="experiment-evidence">SFT only \| 36.80 \| 99.1 \| 260.48 \| 33.9
SFT → RL \| 40.79 \| 99.3 \| 257.20 \| 49.1</span> |
| 完整两阶段训练SFT→RL与RL only比较 | SFT→RL相较RL only将Acc.从35.59提高到40.79，即增加5.20个百分点；Fmt.从92.4%提高到99.3%，Tok.从660.20降至257.20，减少403.00个、约61.0%；Think比例从87.5%降至49.1%。 | 该对照表明SFT冷启动为模式控制和输出格式提供了关键基础。仅用RL时，模型倾向于对绝大多数问题显式思考，产生很长的回答，但准确率和格式正确率反而较低；加入SFT后再做RL，更接近按需推理。该消融同时改变训练初始化与训练流程，因而不能把全部差异归因于某一个具体模块。 | 表5，SFT and RL stage ablation<br><span class="experiment-evidence">RL only \| 35.59 \| 92.4 \| 660.20 \| 87.5
SFT → RL \| 40.79 \| 99.3 \| 257.20 \| 49.1</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过强化学习和 VRPO 训练视频 VLM 自适应选择显式推理或直接回答，以提高视频推理的 token 效率。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`3e86583dbdef263eacda1443454dffcc1b23c93ec845a9c8a2e317eaea02dd27`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
