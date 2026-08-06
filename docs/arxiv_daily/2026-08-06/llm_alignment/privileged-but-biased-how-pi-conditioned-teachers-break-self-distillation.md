---
title: "[论文解读] Privileged, but Biased: How PI-Conditioned Teachers Break Self-Distillation"
description: "[arXiv 2608.04794][对齐 / RLHF] 本文研究自蒸馏在没有奖励信号时是否真正传递任务正确性，并指出基于特权信息的教师会把学生引向单一参考轨迹，而不是可靠地提升困难推理任务的表现。"
arxiv_id: "2608.04794"
announcement_date: "2026-08-06"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T07:04:24.991967+00:00"
source_sha256: "2ec007c46b11a388e79bc867cdbdd8f219555b248956b958b9605bfe6f7902b7"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM Agent"
  - "大语言模型后训练"
  - "自蒸馏"
  - "特权信息"
  - "逐词元监督"
  - "强化学习与可验证奖励"
  - "PI偏置"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.04794</p>

# Privileged, but Biased: How PI-Conditioned Teachers Break Self-Distillation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Sarthak Harne, Chinmay Karkar, Yash Pandya, Ahmed Awadallah, Akshay Nambi</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Microsoft Research</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04794v1) · [PDF 下载](https://arxiv.org/pdf/2608.04794v1) · **关键词** 大语言模型后训练, 自蒸馏, 特权信息, 逐词元监督, 强化学习与可验证奖励, PI偏置<br>


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

本文研究自蒸馏在没有奖励信号时是否真正传递任务正确性，并指出基于特权信息的教师会把学生引向单一参考轨迹，而不是可靠地提升困难推理任务的表现。

**不用术语来说**：一种看似高效的训练方法让模型先看到答案或参考解法，再用这个信息逐词指导另一个不知答案的模型。问题在于，模型可能只是学会模仿这一个解法的措辞、顺序和停顿，而没有学会判断什么答案是正确的；因此训练损失下降，并不一定意味着模型解决问题的能力提高。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 在问答、数学、代码和多轮工具使用等困难任务上检验自蒸馏，说明当自蒸馏作为唯一训练目标、没有额外奖励项时，训练损失下降并不能稳定转化为正确率提升；这一现象还覆盖不同推理模式、模型规模、特权信息形式以及 $\mathrm{SDPO}$ 和 $\mathrm{OPSD}$ 两种训练方案。
- 提出并实证刻画一条从特权信息偏置到性能失败的因果链：教师偏向单一参考轨迹，使逐词损失难以区分正确与错误，训练压力又集中到低信息量词元和偏离参考路径的探索位置，最终使学生策略变得更平坦、更早做出决定；作者用 $\mathrm{PI\ Bias\ Score}$ 等测量工具对这一机制进行分析。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型的推理后训练。强化学习与可验证奖励（RLVR）让模型根据答案是否正确的可验证信号学习，但通常每条完整回答只有一个标量奖励，因而监督稀疏、信用分配粗糙，并且需要验证器和多次在线采样；传统知识蒸馏能在每个生成位置提供稠密监督，却依赖额外的强教师模型。自蒸馏（SD）试图兼得两者优点：以正在训练的模型同时充当学生和教师，教师额外看到参考解答、提示或执行反馈等特权信息（PI），学生则不可见这些信息；训练时沿学生生成的回答逐词缩小二者输出分布的差异，测试时仅使用学生。本文关注的不是将SD作为奖励学习的辅助项，而是它在没有任何奖励项时，能否单独提升困难任务的正确率。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**强化学习与可验证奖励（RLVR）**

模型对提示生成完整回答，验证器以二元奖励$R(x,y)$判断回答$y$是否正确，再用奖励更新策略$pi_{\theta}$。这种监督直接对应任务成败，但一条回答通常只有一个奖励，难以判断具体哪些词元促成了正确或错误。

</div>
<div class="concept-item" markdown="1">

**特权信息（PI）条件化自蒸馏**

特权信息是训练时提供给教师、测试时不给学生的答案相关信息，例如参考解答、提示、成功轨迹或单元测试反馈。教师和学生可源自同一模型，但教师因额外看到PI而形成不同的下一词元概率分布，学生通过匹配该分布接受稠密监督。

</div>
<div class="concept-item" markdown="1">

**逐词元分布散度**

在学生回答的每个位置，方法用KL散度等量度比较教师分布与学生分布，并对这些位置的差异进行优化。它比整条回答一个奖励更稠密，但“每个位置都有信号”不等于该信号能区分正确推理与错误推理。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定问题提示$x$，学生策略$\pi_{\theta}$在看不到PI的条件下生成回答$y$；同源教师在额外获得反馈$f$、参考解答$y^{\star}$或其他条件上下文后，对学生轨迹上的每个位置给出下一词元目标分布。SDPO或OPSD据此最小化教师与学生的逐词元散度，并通过停止梯度、固定教师或稳定化教师避免目标随学生同步反向传播；核心设定明确排除独立外部教师和可验证奖励项。论文要检验的是：当训练任务从较容易的短知识题扩展到困难的通用问答、数学、代码和多轮工具使用时，仅优化这种PI条件化蒸馏目标，是否会使验证正确率提高，而不只是使教师—学生散度下降。其关键假设风险在于，教师看到的是某一个具体参考轨迹，而非所有正确解法的总体分布，因此逐词元目标可能主要编码该轨迹的措辞和路径，而非一般意义上的正确性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\pi_{\theta}$**

参数为$\theta$的学生策略，即待训练的大语言模型。

</div>
<div class="notation-item" markdown="1">

**$R(x,y)$**

验证回答$y$对提示$x$是否正确的二元奖励；本文考察的纯SD训练不使用该奖励。

</div>
<div class="notation-item" markdown="1">

**$y^{\star}$**

作为特权信息提供给教师、但不提供给学生的参考解答。

</div>
<div class="notation-item" markdown="1">

**$p_T,\,p_S$**

教师与学生在某个生成位置上的下一词元概率分布，OPSD等方法通过$\mathrm{KL}(p_T\|p_S)$之类的散度训练学生。

</div>

</div>

**直接相关的工作**

- **SDPO（Hübotter et al., 2026）与OPSD（Zhao et al., 2026）**: 二者是本文直接复现和压力测试的PI条件化自蒸馏方案。SDPO可使用成功轨迹或环境反馈$f$并配合EMA或信赖域教师，OPSD则让固定于初始策略的教师读取参考解答$y^{\star}$；它们均沿学生轨迹提供逐词元监督，并曾在相对容易或较窄的任务上报告优于或接近GRPO的效果。
- **RLSD（Yang et al., 2026a）**: RLSD从理论上指出OPSD目标包含条件互信息泄漏项，说明PI条件化教师可能拟合单条参考轨迹而非有效解答的边缘分布；其改进仍以验证器优势为主，仅用教师重加权。本文承接这一理论批评，在困难任务的实际训练过程中测量PI偏置及其后续影响。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

带可验证奖励的强化学习能够训练大语言模型进行推理，但它通常只在一次完整输出后提供一个标量奖励，信用分配粗糙、监督稀疏，并且需要验证器和大量在线采样。自蒸馏试图利用特权信息提供逐词的密集监督，同时避免训练独立的大教师模型，因此具有降低计算和采样成本的实际价值。真正的科学问题是：这种密集监督是否包含可用于学习任务正确性的信号，而不只是包含参考答案的表面轨迹。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **带可验证奖励的强化学习（RLVR）**：模型生成完整轨迹后，由验证器判断答案是否正确，并以奖励训练策略。它直接把优化目标连接到任务结果，但通常每条轨迹只有一个粗粒度信号，且训练过程需要反复生成样本并运行验证器。
- **蒸馏与特权信息条件自蒸馏（包括 SDPO、OPSD）**：普通蒸馏用一个更强的教师指导学生；自蒸馏则从正在训练的模型构造教师，并让教师读取学生不可见的特权信息（$\mathrm{PI}$），例如参考解、提示或执行反馈。教师据此产生逐词分布，学生沿自己的输出轨迹匹配这些分布，从而把一个特权示例转换为密集训练信号。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 已有自蒸馏的正面结果主要来自较容易、较窄的任务环境，例如短的知识选择题；因此这些结果不能说明方法在需要长链推理、探索和多步决策的困难任务中仍能作为唯一目标优化正确性。
- 特权信息条件教师只观察一条具体参考轨迹，教师的逐词预测可能更偏向该轨迹的表达形式而非一般性的正确条件。若学生在所有词元上匹配这一目标，损失就可能主要衡量表面模仿程度，并惩罚有益的偏离和探索，导致损失下降与任务成功脱钩。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未明确回答：在不加入验证奖励或其他任务目标的前提下，特权信息条件自蒸馏的逐词目标是否能够区分正确轨迹与错误轨迹，并在困难推理任务上产生可泛化的能力提升。已有理论工作讨论了信息泄漏，另有研究观察到推理退化，但两者之间缺少由教师偏置、损失分布到学生行为变化的统一实证解释。

</div>
<div markdown="1"><span>核心问题</span>

当自蒸馏作为唯一训练目标、学生看不到特权信息且不存在奖励项时，它优化的究竟是任务正确性，还是仅仅是对单一参考解法及其表面形式的模仿信号？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是比较教师目标与任务结果之间的关系，而不是只观察总损失是否下降。如果教师真正传递的是正确性，那么正确和错误轨迹应受到不同的训练压力，决定答案的内容词元也应比停用词、标点等承担更多信息；相反，如果教师被一条参考解法牵引，学生会被要求在所有位置贴近这条路径，正确但采取不同探索路线的输出也会受到惩罚。由此可以沿着“教师看到了什么、损失强调什么、学生因此改变什么”的链条定位失败原因，并判断问题究竟来自监督的稀疏性，还是来自特权目标本身没有编码一般性的正确条件。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文研究的不是一种新的蒸馏算法，而是把 SDPO 与 OPSD 共有的“特权信息条件化自蒸馏”抽象为统一目标，并追踪该目标为何可能与任务正确性脱钩。给定问题 $x$ 和仅教师可见的特权信息 $r$，学生策略 $p_S$ 先自行采样回答 $\hat{y}$；同一模型或其慢速副本作为教师，在额外看到 $r$ 后，对回答每个位置给出下一词元分布 $p_T$。训练逐位置缩小 $p_S$ 与 $p_T$ 的散度，但不加入可验证奖励，因此模型实际优化的是“模仿看过参考信息的教师”，而不是直接提高答案正确率。

为解释这种训练信号，作者进一步提出 PI Bias Score：在学生生成到某一前缀后，分别让含有 $r$ 的教师上下文和不含 $r$ 的学生上下文评价若干候选后续，包括上下文中的参考解、另一条正确解、错误解和无关解。两种上下文对同一后续的平均对数概率之差，衡量特权信息把模型推向该后续的程度。直观地说，该方法先检查学生是否能通过逐词模仿教师学会推理，再用反事实式对比判断教师究竟在传递普遍的正确性知识，还是偏向它已经看到的那一条具体答案轨迹。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造学生与特权信息教师

学生分布定义为 $p_S(\cdot\mid x,y_{<t})=\pi_\theta(\cdot\mid x,y_{<t})$，教师分布定义为 $p_T(\cdot\mid x,r,y_{<t})=\pi_{\theta'}(\cdot\mid x,r,y_{<t})$，其中 $\theta'$ 可取学生参数或跟踪学生的慢速副本。

<div class="method-step__io" markdown="1">

**输入**：训练样本 $(x,r)$，其中 $x$ 是问题提示，$r$ 是参考解、正确答案或提示式特权信息；基础策略参数为 $\theta$。<br>
**输出**：一对共享模型能力但信息条件不同的下一词元预测器 $p_S$ 与 $p_T$。

</div>

**直观理解**：学生只能看题，教师还能偷看参考信息；因此两者对同一生成前缀可能给出不同的下一词建议。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 采集学生在策略回答

从学生自身分布采样完整回答 $\hat{y}\sim\mathrm{sg}(p_S)$，并将该回答的每个前缀 $\hat{y}_{<t}$ 同时送入学生和教师；采样路径使用停止梯度，不通过离散采样过程反向传播。

<div class="method-step__io" markdown="1">

**输入**：问题 $x$、当前学生策略 $p_S$ 及其自回归生成历史。<br>
**输出**：学生实际可能访问的回答轨迹 $\hat{y}$，以及轨迹上各位置的学生、教师条件分布。

</div>

**直观理解**：训练沿着学生自己走出的路线进行，而不是只在标准答案上教学；教师在学生走到每一步时告诉它下一步应更像什么。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行密集逐词元自蒸馏

在所有回答位置计算散度 $D(p_T\|p_S)$，按回答长度取平均并更新 $\theta$；教师目标停止梯度，主实验采用对称 Jensen-Shannon 散度，而 OPSD 复现实验改变散度方向、教师计划、采样数和裁剪设置。

<div class="method-step__io" markdown="1">

**输入**：轨迹上每个位置的 $p_T(\cdot\mid x,r,\hat{y}_{<t})$ 与 $p_S(\cdot\mid x,\hat{y}_{<t})$。<br>
**输出**：在教师条件分布下逐词元散度更低的学生策略。

</div>

**直观理解**：每个词都获得训练信号，信号很密集；但标点、停用词和措辞风格也会与决定答案的关键推理词一起被模仿。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 测量特权信息偏置

分别计算教师上下文和学生上下文对完整后续 $w$ 的逐词元平均对数概率 $s_t^T(w)$ 与 $s_t^S(w)$，再取差 $\mathrm{PS}_t(w)=s_t^T(w)-s_t^S(w)$；正值表示加入 $r$ 后模型更倾向沿 $w$ 继续。

<div class="method-step__io" markdown="1">

**输入**：学生前缀 $\mathrm{prefix}_{<t}$、含或不含特权信息的上下文，以及四类目标后续 $w\in\{y^\star,y',y^-,\tilde{y}\}$。<br>
**输出**：不同位置、不同后续类型上的 PI Bias Score，可用于比较教师对原参考解、替代正确解和错误解的偏向。

</div>

**直观理解**：这相当于只改变模型是否看到参考信息，再观察它对同一候选续写的偏好变化；若参考解获得特殊提升，就说明教师可能在教“复现这条解法”，而非一般正确性。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 特权信息条件化自蒸馏目标

$$
\mathcal{L}_{\mathrm{SD}}(\theta)=\mathbb{E}_{(x,r)}\,\mathbb{E}_{\hat{y}\sim\mathrm{sg}(p_S)}\!\left[\frac{1}{|\hat{y}|}\sum_{t=1}^{|\hat{y}|}D\!\left(\mathrm{sg}\!\left(p_T(\cdot\mid x,r,\hat{y}_{<t})\right)\,\middle\|\,p_S(\cdot\mid x,\hat{y}_{<t})\right)\right]
$$

**符号说明**

- $\mathcal{L}_{\mathrm{SD}}(\theta)$：关于学生参数的自蒸馏训练损失。
- $(x,r)$：训练问题与教师专有的特权信息组成的样本。
- $\hat{y}\sim\mathrm{sg}(p_S)$：由学生策略采样、且采样过程不参与反向传播的回答轨迹。
- $\hat{y}_{<t}$：回答在位置 t 之前的词元前缀。
- $p_S$：只观察问题和回答前缀的学生下一词元分布。
- $p_T$：额外观察特权信息的教师下一词元分布。
- $D$：教师分布与学生分布之间的散度；不同训练配方采用不同实例。
- $\mathrm{sg}$：停止梯度算子，使梯度只通过学生分布流向参数。
- $|\hat{y}|$：学生回答的词元长度，用于对逐位置损失归一化。

<div class="equation-explanation" markdown="1">

**直观理解**：该式要求学生在自己生成轨迹的每一步都匹配看过 PI 的教师。它的关键不是散度具体选哪一种，而是教师目标既逐词元密集出现、又受某条参考信息影响；在没有奖励项时，降低该损失并不在数学上保证提高答案正确率。<br>
**原文位置**：第 3 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 目标后续评分与 PI Bias Score

$$
s_t(w)=\frac{1}{|w|}\sum_{k=0}^{|w|-1}\log P_{\mathrm{model}}\!\left(w_k\mid c,\mathrm{prefix}_{<t},w_{<k}\right),\qquad \mathrm{PS}_t(w)=s_t^{\mathrm{T}}(w)-s_t^{\mathrm{S}}(w)
$$

**符号说明**

- $w$：待评价的目标后续序列，可以是原参考解、替代正确解、错误解或无关正确解。
- $s_t(w)$：模型从学生位置 t 的前缀出发，对目标后续全部词元给出的平均对数概率。
- $w_k$：目标后续 w 的第 k 个词元。
- $c$：评分上下文；取含 PI 的教师提示或不含 PI 的学生提示。
- $\mathrm{prefix}_{<t}$：学生回答在被评价位置 t 之前的词元。
- $w_{<k}$：目标后续中位于第 k 个词元之前的部分。
- $s_t^{\mathrm{T}}(w)$：使用含 PI 的教师上下文得到的目标后续分数。
- $s_t^{\mathrm{S}}(w)$：使用不含 PI 的学生上下文得到的目标后续分数。
- $\mathrm{PS}_t(w)$：位置 t 上目标 w 的 PI Bias Score，表示加入 PI 导致的平均对数概率增量。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分不是只检查目标后续的第一个词，而是把整个后续接在学生前缀后逐词计分；第二部分消去模型在两种上下文中共有的偏好，只保留 PI 带来的变化。分数为正表示 PI 推动模型朝该目标继续，但是否属于有益知识，要结合原参考解与其他正确解的相对变化判断。<br>
**原文位置**：附录 E，公式（3）和公式（4）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练仅最小化 $\mathcal{L}_{\mathrm{SD}}(\theta)$，不叠加可验证奖励、序列级正确性奖励或其他直接任务成功信号。每次更新先由当前学生产生在策略轨迹，再将各位置的教师软分布作为停止梯度目标，通过散度对学生参数求梯度；因此优化成功的直接含义只是平均逐词元分布差异下降。论文的因果分析强调，PI 可能使教师目标偏向特定参考轨迹，而密集目标又把这种偏向施加到所有词元，于是损失对整条回答是否正确近乎不敏感，并可能主要由低信息词元或探索性表达贡献。

主 SDPO 配置用混合系数 $\alpha=0.5$ 的对称 Jensen-Shannon 散度，并以更新率 $0.001$ 的指数移动平均教师提供较慢变化的目标；OPSD 对照则采用单次采样、固定正确答案和初始策略教师。两套配方的差异用于检验失败是否源自某个实现选择，而共同的训练约束仍是：学生在自己的前缀上逐位置逼近 PI 条件教师，且没有奖励项纠正“像参考轨迹”与“答案正确”之间的偏差。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 信息不对称的自教师—学生模块**

学生和教师基于同一策略族 $\pi$，但学生只条件化于 $x$ 与当前前缀，教师还条件化于 $r$。教师参数 $\theta'$ 可以等于当前学生参数，也可以通过指数移动平均缓慢跟踪 $\theta$，从而形成较稳定的软目标。

> 直观理解：教师并非独立训练的更大模型，它的主要优势来自多看到一份答案相关信息；该设计节省额外教师成本，却也使监督信号天然依赖特定参考信息。

**2. 密集词元级散度模块**

模块在学生采样轨迹的每个位置比较完整词表上的教师与学生分布，再对位置求平均。SDPO 与 OPSD 对散度 $D$、教师更新和裁剪的具体实例化不同，但都保留“PI 条件教师、学生在策略轨迹、逐词元匹配”这一共同结构。

> 直观理解：密集监督比只给整段答案一个分数更容易优化，但它不知道哪些词真正决定正确性，因此大量梯度可能花在措辞、标点和犹豫表达上。

**3. PI Bias Score 诊断模块**

在每个被评估的助手词元位置，模块以最长 $K=2000$ 个词元的前瞻对目标序列完整计分；目标包括特权信息中的正确解 $y^\star$、另一正确解 $y'$、错误解 $y^-$ 和同批其他问题的无关正确解 $\tilde{y}$。提示式 PI 不含完整解时，$y^\star$ 使用同题正确解并移除其推理轨迹。

> 直观理解：多种候选后续使诊断能够区分“看到 PI 后更懂这道题”和“看到 PI 后只偏爱其中一条固定写法”；只有比较替代正确解与原参考解，才能暴露这种轨迹偏置。

**训练与推理**

训练时，对每个问题及其 PI 构造学生提示和教师提示；学生以温度采样一个或多个回答，教师在同一学生前缀上计算软词元分布。系统以停止梯度固定采样轨迹和教师目标，对每个位置计算散度、按回答长度平均，再用 AdamW 更新学生；慢速教师配置随后用指数移动平均跟踪学生。主实验分别训练 thinking 模式与 instruct 模式：前者允许长推理链，后者生成更短、更直接的回答，用来检验逐词元偏置是否随推理长度和探索需求增强。

评测或实际推断时不再向学生提供 $r$，模型只根据 $x$ 自回归生成回答；验证采用独立采样并根据各基准的任务规则计算正确率，BFCL 则报告其验证分数。PI Bias Score 属于离线诊断而非部署时模块：固定学生前缀，分别在有 PI 和无 PI 的上下文中对四类完整候选后续计分，从而定位教师条件化对生成方向的影响。

**复现信息**

主要实验使用 Qwen3-8B，并在四个领域共享核心配置：问题批大小与小批大小均为 $32$，每题生成 $8$ 条训练 rollout，主损失采用 top-$K$ 蒸馏且 $K=100$，Jensen-Shannon 混合系数为 $\alpha=0.5$，教师 EMA 更新率为 $0.001$，逐词元损失裁剪阈值为 $\tau=0.001$。优化器为 AdamW，主要学习率为 $1\times10^{-5}$；代码和多轮智能体实验改用 $1\times10^{-6}$。训练共 $3$ 个 epoch，每个 epoch 使用 $2000$ 个问题，主实验最大提示长度为 $2048$、最大回答长度为 $16384$；这些长度信息对解释长推理轨迹上的密集监督尤其重要。

验证每个问题采样 $4$ 条回答，温度为 $0.6$、top-$p$ 为 $0.95$；所有报告值按四次独立 rollout 平均。PI 偏置诊断仅在助手词元位置执行，前瞻上限设为 $K=2000$，原文说明该值超过所有目标长度，因而候选后续不会被截断。计算资源为单节点 $8$ 张 NVIDIA B200；Qwen3-32B 规模实验把最大回答长度改为 $10240$、最大上下文改为 $12288$，并采用张量并行度 $4$。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 通用问答使用 MMLU-Pro，抽取 $2{,}000$ 个训练样本，并在 MMLU-Pro 上进行域内评测；迁移评测使用 GPQA-Diamond 和 SciKnowEval。该设置测试自蒸馏是否只适应训练数据，还是能够泛化到不同来源的知识与推理问题。原文还说明 SciKnowEval 包含生物、化学、材料和物理四个学科，并采用九比一的训练测试划分。
- 数学使用去重后的 DAPO-Math，抽取 $2{,}000$ 个训练样本，在 DAPO-Math 上进行域内评测，并在 AIME24、AIME25 和 OlympiadBench 上进行迁移评测。该数据组合主要测试模型面对不同题目来源、解答长度和数学难度时的推理能力，而不是仅测试短答案记忆。
- 代码使用 CodeForces 的 $2{,}000$ 个题目训练并进行域内评测，迁移评测使用 MBPP+、HumanEval+、CodeElo 和 LiveCodeBench v6；多轮智能体任务另使用 BFCL v3 多轮基础类别训练与域内评测，并在 BFCL v4 的基础、缺失函数、缺失参数和长上下文类别上迁移评测。代码任务要求生成算法，智能体任务要求跨轮次维护状态并组合工具调用。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务成功率或准确率**

数学和问答使用任务准确率，代码使用测试用例通过比例，BFCL 智能体任务使用其 success 指标；每个验证步骤对每项任务采样 $4$ 条验证轨迹后取平均。 （越高越好，因为它直接衡量答案是否正确、代码是否通过测试，或工具调用流程是否成功。）

</div>
<div class="metric-item" markdown="1">

**逐词自蒸馏损失**

衡量学生在各生成位置上的输出分布与教师目标分布之间的差异；实验将散度实例化为对称 Jensen–Shannon 散度。该指标反映学生是否在拟合教师，不等价于任务正确率。 （越低表示学生更接近教师目标，但只有在该目标与任务正确性一致时，下降才具有能力提升含义。）

</div>
<div class="metric-item" markdown="1">

**学生熵**

记录学生分布 $p_S(\cdot\mid x,\hat{y}_{<t})$ 的不确定性，并结合平均回答长度、教师与学生之间的 KL 散度及教师困惑度分析模型行为变化。 （不存在脱离任务的统一高低标准；熵降低可能表示决策更确定，也可能表示模型过早变得僵化，因此必须结合任务成功率和生成行为解释。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 在原始简单设置上复现 SDPO：Qwen3-8B、完整解答 PI、SciKnowEval 生物和物理任务。

<div class="result-value" markdown="1">

研究者报告，使用完整解答 PI 和 SDPO 代码库及原始超参数时，逐词损失下降，同时验证准确率上升、回答变短，因而在定性上复现了 SDPO 的结果。

</div>

该结果说明实现没有因为代码或训练流程错误而无法学习，也说明自蒸馏在原论文所强调的简单、知识回忆型场景中确实可能表现出收益。但它只证明该特定设置可以复现，不能推出自蒸馏在困难推理任务上普遍有效。

<div class="result-source" markdown="1">

来源：第 4 节“Reproducing SD in its original regime”及 Figure 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Using whole-solution PI, we train Qwen3-8B with Eq. (1) on SciKnowEval with SDPO’s codebase (Hübotter et al., 2026) and reported hyperparameters, and recover the qualitative SDPO result: on Biology and Physics the loss decreases while validation accuracy rises and responses shorten (Figure 1), confirming that implementation is faithful.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 困难任务上的统一自蒸馏：问答、数学、代码和多轮智能体工具调用，覆盖不同推理模式、模型规模和 PI 形式。

<div class="result-value" markdown="1">

摘要报告，在上述四类任务、不同推理模式、模型规模和 PI 形式下，逐词损失持续下降，但验证准确率没有提升且通常下降；该现象在 SDPO 和 OPSD 两种配方下都出现。

</div>

损失下降仅表示学生越来越像带有 PI 的教师目标，并不表示学生越来越会答题、做数学、写代码或调用工具。结果支持作者的核心判断：当自蒸馏是唯一目标时，优化信号可能与任务成功脱钩；但所给章节没有提供各数据集的具体数值、置信区间或统计显著性，因此只能确认报告的总体趋势。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across question answering, mathematics, coding, and multi-turn agentic tool use, across reasoning modes, model sizes, and forms of PI, and under both the SDPO and OPSD recipes, the per-token loss falls steadily while validation accuracy does not improve and typically degrades.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨来源迁移评测：MMLU-Pro、DAPO-Math、CodeForces 和 BFCL 训练后，分别迁移到不同来源的问答、数学、代码和 BFCL v4 任务。

<div class="result-value" markdown="1">

实验设计同时包含域内评测和来自不同来源的 held-out transfer benchmarks，研究目标是检验收益是否来自训练分布拟合；所给章节未报告这些迁移评测的具体分数或逐数据集结果。

</div>

迁移集能够区分“记住训练样式”与“获得可泛化能力”。如果只在域内变好而迁移不变好，不能认为模型学到了稳定推理能力；但由于当前材料没有数值结果，不能据此断言迁移性能具体下降或改善。

<div class="result-source" markdown="1">

来源：第 4 节“Domains and data”；数据汇总见 Appendix A Table 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We train on 2,000 examples for general QA, math, and coding, and on the BFCL multiturn split, evaluating every domain in-domain and on held-out transfer benchmarks from different sources, so a gain cannot come from fitting the training distribution.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验材料主要提供总体趋势和实验设计，未提供困难任务及迁移基准的逐数据集分数、误差范围或显著性检验，因此不能判断退化幅度、不同任务间差异或结论的统计稳健性。
- 实验重点考察“无奖励或验证器的单独自蒸馏目标”，不能直接推出将自蒸馏与奖励、验证器或其他任务监督结合后仍然失败；同时，所给章节未完整呈现第 5.2 节、Section 6.1 和 Section 6.3 的结果，关于 OPSD、不同 PI 形式及损失集中位置的细节需要回查原文。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- SDPO 原始配方及其报告的超参数构成主要复现实验基线，用于确认实现是否能够在其原先的简单任务设置中重现已发表的定性收益。
- OPSD 配方用于检验结论是否依赖 SDPO 的具体自蒸馏实现；原文说明 OPSD 结果见第 5.2 节，但所给章节未提供其具体数值。
- 无奖励或验证器的单独自蒸馏目标是核心比较条件，研究者将其与任务验证指标的变化对照，以判断下降的逐词损失是否真正对应任务能力提升。
- 不同 PI 形式之间的比较包括完整参考解、短提示和约 $500$ 个词元的结构化技能指南；该比较用于检验结论是否只是完整参考解这一种 PI 形式造成的。

**实验想回答的问题**

- 在没有奖励函数或验证器参与损失的情况下，单独使用由特权信息（PI）条件化教师产生的自蒸馏目标，能否在困难的问答、数学、代码和多轮工具调用任务上提升任务成功率？
- 自蒸馏在不同任务难度、推理模式、模型规模、PI形式及训练配方下的表现是否稳定，并且能否迁移到训练分布之外的评测集？

**实验实现**

实验以 Qwen3-8B 为主要模型，同时覆盖 think（长思维链）和 instruct 两种推理模式；通用问答还比较 Qwen3-32B，以检验模型规模影响。默认 PI 是从模型自身成功尝试中随机选取的一条正确完整解答，教师可以看到该解答，而学生训练时不直接看到 PI。训练只使用 Eq. (1) 的自蒸馏目标，不把奖励或验证器加入损失。默认散度为对称 Jensen–Shannon 散度，定义为 $\mathrm{JSD}(p\,\|\,q)=\tfrac{1}{2}\mathrm{KL}(p\,\|\,m)+\tfrac{1}{2}\mathrm{KL}(q\,\|\,m)$，其中 $m=\tfrac{1}{2}(p+q)$；$p$ 和 $q$ 分别表示教师与学生在一个词元位置上的输出分布，$m$ 是两者的平均分布，$\mathrm{KL}$ 是 Kullback–Leibler 散度。为适应困难数据，训练使用逐词元散度裁剪、慢速指数移动平均教师 $\theta^{\prime}\leftarrow(1-\alpha)\theta^{\prime}+\alpha\theta$，其中 $\theta$ 是当前学生参数，$\theta^{\prime}$ 是教师参数，$\alpha=0.001$；其他报告的设置包括裁剪阈值 $\tau=0.001$、学习率 $1\mathrm{e}{-5}$、批大小 $32$ 和训练 $3$ 个周期。域内训练集使用分层验证子集，通常包含 $300$ 个样本；迁移数据集的验证集使用完整数据集。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 改变 PI 形式：完整参考解、短提示以及约 $500$ 个词元的结构化技能指南。 | 原文说明第 6.1 节额外研究了短提示和技能两种 PI，并将它们作为完整参考解的替代形式；所给章节未报告各形式对应的准确率、损失或消融数值。 | 该消融隔离的是“教师是否必须看到完整的一条解答”。若不同 PI 形式都出现损失下降而任务性能不升，说明失败不能简单归因于参考解过长；但没有具体结果时，只能确认实验覆盖了这些条件，不能判断哪种 PI 最差或是否存在显著差异。 | 第 4 节“Models and privileged information”<br><span class="experiment-evidence">Section 6.1 additionally studies short hints (one to two sentences) and skills (≈500-token structured guides of relevant techniques).</span> |
| 训练配方与稳定化组件：比较 SDPO 与 OPSD，并使用逐词元散度裁剪和慢速 EMA 教师。 | 原文报告 OPSD 变体见第 5.2 节；困难数据训练采用逐词元裁剪和 $\alpha=0.001$ 的慢速 EMA 教师，作者称这消除了早期观察到的后期训练不稳定性，但所给章节未报告移除任一组件后的独立消融数值。 | 这一组设计区分两类问题：配方差异是否决定结论，以及训练是否只是数值不稳定。EMA 和裁剪可以让优化更平稳，却不能自动使教师目标与正确答案一致；因此即使稳定化成功，也不能把损失下降解释为能力提升。缺少逐组件对照时，不能量化每个组件对最终任务指标的贡献。 | 第 4 节“Objective, divergence, and training”<br><span class="experiment-evidence">Two ingredients stabilize training on harder data, both motivated by the loss concentration of Section 6.3: aggressive per-token clipping of the divergence (Zhao et al., 2026), preventing a few high-divergence stylistic tokens from dominating the gradient, and a slow EMA teacher θ′←(1−α)θ′+αθ with α=0.001 (vs. 0.01 in SDPO and 0.05 in Kim et al. (2026)), which removed the late-training instabilities we first observed.</span> |

**定性案例**

- 作者将失败机制概括为从 PI 偏差到行为退化的因果链：教师看过一条特定参考轨迹后，其逐词目标会偏向该轨迹，而不是一般意义上的正确性；学生在所有位置拟合这一目标后，损失主要集中在停用词、标点和不确定性标记等低信息词元，反而惩罚正确推理轨迹中的探索性词元。直观上，学生学会了更确定、更像参考解的表达方式，却没有获得判断答案正确与否的可靠信号。所给实验章节没有提供具体案例文本或对应图表，因此该解释应视为作者的机制性分析，而不是当前材料中可独立核验的定性样例。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：分析以特权信息为条件的逐token自蒸馏后训练目标为何无法提升并可能损害LLM推理能力。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`2ec007c46b11a388e79bc867cdbdd8f219555b248956b958b9605bfe6f7902b7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
