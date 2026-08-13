---
title: "[论文解读] When Self-Consistency Backfires: Majority Vote Hurts the Majority of Hard Science Problems for Small LLMs"
description: "[arXiv 2608.11403][LLM Reasoning] 本文发现，在GPQA Diamond高难度科学题上，对小型指令微调语言模型增加推理采样并进行多数投票，往往会强化模型稳定但错误的答案；同时，基于答案一致率或词元熵的廉价无验证器门控也无法可靠判断何时应采用投票。"
arxiv_id: "2608.11403"
announcement_date: "2026-08-13"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:56:02.641229+00:00"
source_sha256: "94661156e401ce6f35aef79aa7aa182e7946dd6d5e6e940b6c0ca3a6a1fd5e48"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "推理时计算"
  - "自洽性"
  - "多数投票"
  - "逐题准确率"
  - "置信度失准"
  - "GPQA Diamond"
  - "无验证器路由"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.11403</p>

# When Self-Consistency Backfires: Majority Vote Hurts the Majority of Hard Science Problems for Small LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Utkarsh Bahuguna</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Scaler School of Technology</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11403v1) · [PDF 下载](https://arxiv.org/pdf/2608.11403v1) · **关键词** 推理时计算, 自洽性, 多数投票, 逐题准确率, 置信度失准, GPQA Diamond, 无验证器路由<br>


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

本文发现，在GPQA Diamond高难度科学题上，对小型指令微调语言模型增加推理采样并进行多数投票，往往会强化模型稳定但错误的答案；同时，基于答案一致率或词元熵的廉价无验证器门控也无法可靠判断何时应采用投票。

**不用术语来说**：通常，人们让模型对同一道题独立作答多次，再选择出现次数最多的答案，以期用更多计算换取更高准确率。但在困难科学题上，模型可能反复犯同一种错误，此时增加采样只会让错误答案获得更稳定的多数票。实际部署因此面临一个成本与可靠性问题：系统不仅要决定采样多少次，还要在不知道正确答案、也没有外部判题器的情况下，判断某道题是否值得进行多数投票。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将“反噬”明确为单题上$\mathrm{mv\_gain}=\mathrm{MV\_acc}(64)-\mathrm{MV\_acc}(1)<0$，并在完整的198题GPQA Diamond上进行量化：该现象出现在Qwen2.5-7B的56.6%题目和Llama-3-8B的65.7%题目中；其中Qwen是主要证据，接近随机水平的Llama仅用于验证方向。研究还将探索阶段观察到的现象预注册到151题确认集上，四项确认性假设均通过。
- 作者用逐题选择最佳采样数$N\in\{1,2,4,8,16,32,64\}$的网格预言机说明自适应分配推理计算存在理论收益空间，但进一步发现，两个无需外部验证器的廉价信号，即复数答案一致率与平均词元熵，都几乎不能实现这一收益；这把问题定位为“置信信号与正确性脱节”，而不只是固定采样预算选择不当。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型的推理时计算研究：模型参数保持不变，在回答阶段通过增加采样次数来尝试提高准确率。研究聚焦自洽性多数投票，即针对同一道高难度科学题独立生成 $N$ 条思维链，再返回出现次数最多的答案。常见直觉是增加样本并投票至少不会比单次回答更差，但此前已知的模型置信度失准意味着，多次采样也可能稳定地产生同一错误答案；本文据此在完整的 GPQA Diamond 高难度科学问答基准上考察多数投票是否会对单题准确率产生负收益。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**推理时计算（inference-time compute）**

指不重新训练模型，而是在生成答案时投入更多计算，例如对同一问题进行多次采样。其目标是用额外推理成本换取更高的答案准确率。

</div>
<div class="concept-item" markdown="1">

**自洽性与多数投票（self-consistency via majority vote）**

模型对同一问题独立生成 $N$ 个推理过程及答案，再选择出现次数最多的答案作为最终输出。这里实际采用的是复数投票：即使没有答案超过半数，也返回票数最高者。

</div>
<div class="concept-item" markdown="1">

**置信度失准（miscalibration）**

指模型表现出的置信程度不能可靠反映答案是否正确。在本文场景中，如果模型对错误选项赋予最高生成概率，增加采样次数会让该错误选项更稳定地赢得投票。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是 GPQA Diamond 中的研究生水平科学问题，候选模型为两个不同家族的小型指令微调模型 Qwen2.5-7B 与 Llama-3-8B；对每道题独立采样 $N$ 次，并以复数答案作为最终预测。核心比较是在 $N=1$ 与 $N=64$ 时，多数投票的期望单题准确率是否下降；若 $\mathrm{MV\_acc}(64)-\mathrm{MV\_acc}(1)<0$，该题被定义为发生“反噬”。研究还考虑成本受限的部署情境：不访问标准答案或外部验证器，仅依据少量采样可计算的复数一致率或词元级熵，判断某道题应继续投票还是跳过投票。论文所讨论的结论范围限于上述指令微调模型，原文明确说明未测试推理原生模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N$**

针对同一道问题独立生成的思维链或答案样本数量。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{MV\_acc}(N)$**

使用 $N$ 个独立样本进行多数投票时，该问题的期望准确率。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{mv\_gain}$**

从单次回答增加到 64 次采样投票所带来的准确率变化，即 $\mathrm{MV\_acc}(64)-\mathrm{MV\_acc}(1)$。

</div>
<div class="notation-item" markdown="1">

**$\{1,2,4,8,16,32,64\}$**

论文用于比较不同推理预算并定义逐题网格预言机的候选采样次数集合。

</div>

</div>

**直接相关的工作**

- **Wang et al. (2023)**: 本文将其作为自洽性方法的直接来源：通过采样多条思维链并对答案进行投票，利用推理时计算改善推理结果；当前研究检验这一方法在高难度科学题上是否可能适得其反。
- **Guo et al. (2017); Kadavath et al. (2022)**: 原文用这些工作说明模型置信度失准已有研究基础。本文不是首次指出自洽性可能有害，而是进一步考察这种失准在完整高难度基准上导致逐题投票反噬的频率，以及廉价、无验证器信号能否识别应投票的问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

自洽性多数投票被广泛视为一种低风险的推理时扩展手段：生成$N$条独立思维链，以出现次数最多的答案作为最终输出。对计算预算敏感的使用者真正关心的是，额外采样是否确实提高每道题的正确概率，以及能否只对有收益的题目投入更多推理计算。若困难题上的错误具有系统性，固定增加$N$既浪费算力，也可能主动降低准确率。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **固定预算自洽性多数投票**：对每道题使用相同的采样数$N$生成多条推理轨迹，再返回复数答案。其隐含前提是独立采样中的正确答案更可能占据多数，因此增加样本通常不会比单次回答更差。
- **基于内部置信信号的无验证器门控**：不调用外部判题器，而是利用少量样本即可得到的代理信号决定是否继续投票。本文考察的两类自然信号是复数答案一致率和平均词元熵：前者衡量多个回答是否集中于同一答案，后者衡量模型生成词元时的不确定程度。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定预算投票把“高频答案”近似为“正确答案”，却不能处理模型在困难题上稳定地产生同一错误的情形。当错误答案本身具有最高采样概率时，增大$N$会使错误多数票更加稳定，导致$\mathrm{MV\_acc}(64)<\mathrm{MV\_acc}(1)$。
- 常见廉价置信信号未必经过正确性校准。高答案一致率或低词元熵只能说明模型自身较确定，不能证明其答案正确；因此，用这些信号进行门控可能无法识别应跳过多数投票的题目。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究已经指出自洽性可能降低表现，也已广泛记录神经模型的过度自信，但仍缺少三个相互关联的证据：这种反噬在完整高难度基准上究竟覆盖多少题目，能否跨不同小型指令微调模型家族复现，以及无需真实标签或外部验证器的廉价门控能否把推理预算路由到真正受益的题目。此前的已知失准现象尚未回答这一自洽性部署问题。

</div>
<div markdown="1"><span>核心问题</span>

在GPQA Diamond这类研究生水平科学问题上，从单次回答扩展到$64$次采样的多数投票，是否会在多数题目上降低小型指令微调模型的期望准确率；若逐题最优采样数确有明显理论收益，复数答案一致率或平均词元熵能否在不知道正确答案的条件下识别何时投票、何时跳过？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把总体平均准确率拆成逐题的投票收益，因为总体提升可能掩盖大量受损题目。随后用掌握真实标签的网格预言机估计“若能逐题选$N$”的上限，再用一致率和熵测试是否存在可部署的近似路由规则。直观上，如果模型的内部确定性与正确性相关，高一致率或低熵应能指出适合继续采样的题目；如果这种相关性失效，那么更多相似回答只是在重复并放大同一个错误。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是训练新模型，而是对推理阶段的自一致性多数投票进行逐题评估与路由分析。输入是 GPQA Diamond 的多项选择题；对每道题，研究者从同一个指令微调模型以温度 $0.7$ 重复采样推理答案，保存最多用于分析的 $64$ 个样本，再从样本池中无放回抽取大小为 $N$ 的子集，通过多数投票产生答案。核心指标 $\mathrm{MV\_acc}(N)$ 不是单次投票是否正确，而是对许多随机子集重复投票后得到的期望正确率；比较 $N=64$ 与 $N=1$ 的逐题差值，可以判断增加推理计算是否使该题发生“反噬”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成逐题推理样本池

使用锁定且各次运行字节完全相同的提示模板，在温度 $0.7$ 下独立采样回答；主要分析预算上限为每题 $N=64$，并通过五阶段规则从生成文本中提取最终选项。

<div class="method-step__io" markdown="1">

**输入**：GPQA Diamond 的每道研究生水平多项选择题，以及 Qwen2.5-7B-Instruct-Turbo 或 Meta-Llama-3-8B-Instruct-Lite。<br>
**输出**：每个“模型—问题”组合对应一个答案样本池，以及每个样本解析出的多项选择答案。

</div>

**直观理解**：可以把模型看成对同一道题重复作答的学生：温度带来回答差异，样本池记录它在多次尝试中分别选择了什么。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 估计不同采样预算下的多数投票准确率

从该题的 $n$ 个存储样本中无放回抽取 $\min(N,n)$ 个答案，选择出现次数最多的选项；并列时采用与真实答案无关的均匀随机决胜。通过对子集进行蒙特卡洛重复抽样，估计逐题期望多数投票准确率 $\mathrm{MV\_acc}(N)$。

<div class="method-step__io" markdown="1">

**输入**：某道题的全部已存答案、真实答案，以及预算 $N\in\{1,2,4,8,16,32,64\}$。<br>
**输出**：每道题在各个预算 $N$ 下的 $\mathrm{MV\_acc}(N)$ 曲线。

</div>

**直观理解**：这一步不是只偶然抽一次“答题小组”，而是反复组成不同小组并投票，从而估计给定人数时长期平均能答对多少次。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 识别反噬并计算理想路由上界

计算 $\mathrm{mv\_gain}=\mathrm{MV\_acc}(64)-\mathrm{MV\_acc}(1)$，若该值小于 $0$，则把该题标为多数投票反噬。另用真实答案为每道题选择使 $\mathrm{MV\_acc}(N)$ 最大的预算，构造网格预言机；它只表示完美路由可达到的理论上界。

<div class="method-step__io" markdown="1">

**输入**：每道题的 $\mathrm{MV\_acc}(1)$、$\mathrm{MV\_acc}(64)$，以及完整预算网格上的准确率。<br>
**输出**：逐题反噬标签、总体反噬率，以及知道真实答案时可达到的预算路由上界。

</div>

**直观理解**：反噬表示“多问模型并投票”反而不如只问一次；预言机则像事先知道每道题该问几次的裁判，因此不能部署，只用来衡量潜在改进空间。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 测试无需验证器的自适应门控

一致率门控在探测样本的多数选项占比至少为 $\tau$ 时立即返回该选项，否则继续取得并汇总 $N=64$ 个样本；熵门控在 $k=4$ 个探测样本的平均逐 token 熵低于阈值时提前返回，否则执行 $N=64$ 投票。研究者把门控准确率与固定 $N=64$ 投票比较，并用门控恢复的预言机空间衡量路由信号是否有效。

<div class="method-step__io" markdown="1">

**输入**：前 $k$ 个探测样本的答案集中度，或这些样本的逐 token 概率熵，以及预设阈值。<br>
**输出**：每种门控的最终答案、平均样本开销、准确率，以及相对于固定预算和预言机上界的空间恢复比例。

</div>

**直观理解**：门控试图先用少量回答判断模型是否“足够确定”：若回答很一致或概率分布很尖锐就提前停止，否则投入完整预算；实验检验这种自信能否可靠地区分应该少采样和多采样的问题。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 逐题多数投票增益与反噬判据

$$
\mathrm{mv\_gain}(x)=\mathrm{MV\_acc}_x(64)-\mathrm{MV\_acc}_x(1),\qquad \mathrm{backfire}(x)\iff \mathrm{mv\_gain}(x)<0
$$

**符号说明**

- $x$：一道人为固定的 GPQA Diamond 问题。
- $\mathrm{MV\_acc}_x(N)$：对问题 x 使用 N 个样本进行多数投票时的期望正确率；从该题样本池无放回抽取子集并以蒙特卡洛估计，并列票均匀随机决胜。
- $N$：用于一次多数投票的推理样本预算。
- $\mathrm{mv\_gain}(x)$：问题 x 从单样本推理改为 64 样本多数投票后的准确率变化。
- $\mathrm{backfire}(x)$：多数投票是否降低问题 x 的期望正确率。

<div class="equation-explanation" markdown="1">

**直观理解**：该式直接比较同一道题“只答一次”和“答 $64$ 次后投票”的成功概率。差值为负意味着额外计算把模型更稳定地推向错误答案，因此作者把它定义为反噬。<br>
**原文位置**：第 2 节 Metrics；第 4.1 节 Figure 1 图注

</div>

</div>

<div class="equation-block" markdown="1">

#### 一致率门控决策规则

$$
G_{k,\tau}(x)=\begin{cases}a_k^*(x),&p_k^*(x)\ge \tau,\\a_{64}^*(x),&p_k^*(x)<\tau,\end{cases}\qquad p_k^*(x)=\frac{1}{k}\max_{a}\sum_{i=1}^{k}\mathbf{1}[a_i(x)=a]
$$

**符号说明**

- $G_{k,\tau}(x)$：一致率门控对问题 x 返回的最终答案。
- $k$：门控首先观察的探测样本数；主要报告的门控使用 k=8，参数扫描还包括 k=4。
- $\tau$：允许提前停止的多数选项占比阈值；主要报告设置为 0.75。
- $a_i(x)$：模型对问题 x 的第 i 个样本所给出的选项。
- $a_k^*(x)$：前 k 个探测样本中的多数选项。
- $a_{64}^*(x)$：使用 64 个样本投票得到的多数选项。
- $p_k^*(x)$：前 k 个探测样本中，多数选项所占的比例。
- $\mathbf{1}[\cdot]$：指示函数：条件成立取 1，否则取 0。

<div class="equation-explanation" markdown="1">

**直观理解**：先查看少量回答：若至少有比例 $\tau$ 的回答支持同一选项，就相信这种一致性并提前返回；否则继续使用完整的 $64$ 次采样。该规则把“回答是否集中”当作是否值得继续计算的信号。<br>
**原文位置**：第 2 节 Routing and gates；第 4.3 节

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文没有训练、微调或更新任何模型参数，也没有可反向传播的训练损失；其方法是在冻结的指令微调模型上进行重复采样、蒙特卡洛评估和推理预算路由。熵门控的阈值选择是离散候选值上的样本内 $\arg\max$：在确认集上搜索 $40$ 个阈值，以最大化相对于固定 $\mathrm{MV\_acc}(64)$ 基线、面向二元 $\{N=1,N=64\}$ 预言机的空间恢复比例；这属于超参数选择而非模型训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 逐题多数投票评估器**

评估器在每道题内部从存储样本池无放回抽取子集，以均匀随机方式处理票数并列，并通过蒙特卡洛估计 $\mathrm{MV\_acc}(N)$。逐题估计是必要的，因为汇总准确率可能上升，而多数单题的成功概率仍然下降。

> 直观理解：普通总分会让少数大幅进步的题掩盖许多小幅退步的题；逐题评估器保留这种差异，从而直接回答多数投票对多少道题有害。

**2. 真实答案网格预言机**

对每道题在 $\{1,2,4,8,16,32,64\}$ 中选择使 $\mathrm{MV\_acc}(N)$ 最大的 $N$，再汇总所选预算对应的准确率。由于选择过程访问真实答案，它只能作为可恢复性能空间的上界，不能被当作实际算法。

> 直观理解：该模块回答“如果能完美判断每道题需要多少次采样，最多能提升多少”，从而区分“没有改进空间”和“有空间但现有信号找不到”的情况。

**3. 一致率门控与 token 熵门控**

一致率门控使用探测样本中多数选项的占比作为置信度；熵门控使用模型输出分布的平均逐 token 熵作为不确定性。两者都不借助外部验证器，真实答案只参与最终评分；熵门控阈值在确认集上的 $40$ 个候选值中通过最大化相对二元 $\{N=1,N=64\}$ 预言机的恢复比例选取，因此其结果属于同集选阈值后的样本内估计。

> 直观理解：两种门控分别观察“多次答案是否一致”和“模型生成每个词时是否犹豫”。它们测试仅凭模型自身表现出来的信心，能否决定何时提前停止，而无需另一个模型判断答案对错。

**训练与推理**

完整过程均发生在推理与离线评估阶段。研究者首先用两个冻结的小型非推理指令模型对每道题重复生成答案，再解析最终选项并形成逐题样本池；随后在预算网格 $N\in\{1,2,4,8,16,32,64\}$ 上对子集进行蒙特卡洛抽样，估计逐题 $\mathrm{MV\_acc}(N)$。根据 $\mathrm{MV\_acc}(64)-\mathrm{MV\_acc}(1)$ 判断反噬，并分别汇总探索集、确认集与完整数据集；预注册假设只在 $151$ 道确认题上作通过或失败的决策。

路由分析包含一个不可部署的真实答案预言机和两个可部署形式的无验证器门控。预言机查看真实答案后为每题选择最优 $N$，只提供理论上界；一致率门控先生成 $k$ 个样本，根据多数占比决定立即返回还是继续到 $64$ 个样本；熵门控对 $k=4$ 个探测样本计算平均逐 token 熵，低于阈值则提前返回，否则进行完整投票。真实答案不参与门控决策，只用于评分；因此门控是否接近预言机，检验的是模型内部置信度能否承担逐题计算分配。

**复现信息**

数据为完整 GPQA Diamond，共 $198$ 道生物、化学和物理多项选择题，其中 $47$ 道用于探索并提出假设，剩余 $151$ 道用于预注册确认；阈值在确认分析前锁定并以仓库标签 `backfire-prereg-v1.0` 固化。模型为 Qwen2.5-7B-Instruct-Turbo 和 Meta-Llama-3-8B-Instruct-Lite，均由 Together AI 提供；采样温度为 $0.7$，提示模板固定且用 SHA-256 验证各次运行字节一致。五阶段答案提取的解析率分别为 Qwen 的 $99.5\%$ 和 Llama 的 $98.6\%$。

Llama 每题恰有 $64$ 个存储样本；Qwen 的 $151$ 道确认题每题恰有 $64$ 个，而 $47$ 道探索题因保留早期采样而有 $65$ 至 $72$ 个。计算 $\mathrm{MV\_acc}(N)$ 时从全部已存样本中无放回抽取 $\min(N,n)$ 个，因此 Qwen 探索题的 $N=64$ 估计使用了略大的候选池；作者另将所有问题截为前 $64$ 个样本复算，反噬计数仍为 $198$ 题中的 $112$ 题，且没有题目跨越反噬边界。置信区间采用问题级 bootstrap，共 $1000$ 次迭代、随机种子 $42$。逐 token 对数概率只覆盖 $151$ 道确认题，故熵门控只能在该子集评估；它与基于完整 $198$ 题的一致率门控不能直接横向比较。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GPQA Diamond：共 198 道研究生水平科学题，是本文唯一明确报告的评测基准。作者先在 47 道探索题上观察现象，再在彼此独立的 151 道确认题上检验预注册假设；最后汇总全部 198 题报告总体结果。探索集用于形成假设，确认集用于降低事后挑选结论的风险，全集结果用于提高估计精度。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**回火率（backfire rate）**

多数投票使逐题正确率相对单次采样下降的问题比例。该指标按问题比较采样分布下的正确概率，而不只是比较整个数据集的平均准确率。 （越低越好；较高意味着增加采样并投票在更多问题上系统性放大了错误答案。）

</div>
<div class="metric-item" markdown="1">

**门控收益捕获率（gate capture）**

门控策略相对固定 $N=64$ 多数投票获得的改进，占二元预言机可获得改进的比例。它检验无验证器信号能否识别不同问题适合的推理预算。 （越高越好；接近零表示门控几乎没有利用预言机所揭示的逐题预算差异，负值则表示门控比固定预算更差。）

</div>
<div class="metric-item" markdown="1">

**最高一致度分箱准确率（top-agreement-bin accuracy）**

将问题按多数答案的一致程度分箱后，最高一致度一箱中多数答案的正确率。它检验“采样答案越一致就越可能正确”这一门控前提。 （越高越好；若高一致度下准确率仍低，说明模型可能稳定地产生同一个错误答案，一致度不能可靠代表正确性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 全部 198 道 GPQA Diamond 题上的逐题回火现象

<div class="result-value" markdown="1">

汇总评估中，Qwen2.5-7B 的回火率为 56.6%，95% 置信区间为 [49.5, 63.6]；Llama-3-8B 为 65.7%，区间为 [59.1, 71.7]。两个点估计及其区间均高于 50%，表明多数投票降低逐题正确率的问题占多数。

</div>

作者的结果支持：对这两个小型指令微调模型，增加采样并采用多数票并非普遍稳健，错误答案可能比正确答案更容易在重复采样中占据多数。该结果针对“受损问题的比例”，不等同于证明数据集整体平均准确率必然下降，也不能外推到论文未测试的推理原生模型。

<div class="result-source" markdown="1">

来源：第 4.1 节，图 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Majority voting reduces per-problem accuracy on most problems for both models (Figure 1): the pooled backfire rate is 56.6% (95% CI [49.5, 63.6]) for Qwen and 65.7% ([59.1, 71.7]) for Llama.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 151 道确认题上的预注册回火率检验 PH1

<div class="result-value" markdown="1">

预注册标准要求两个模型的回火率均不低于 33%；确认集上 Qwen2.5-7B 为 60.3%，区间为 [53.0, 68.2]，Llama-3-8B 为 65.6%，区间为 [58.3, 73.5]，因此 PH1 通过。

</div>

这一结果的关键价值在于复现顺序：现象先在 47 道探索题上出现，阈值随后被锁定，再用 151 道未参与探索的题确认，从而减少围绕同一批数据事后制定假设的偏差。不过，33% 是作者预先设置的判定阈值；通过该阈值本身并不证明所有模型或所有科学推理基准都会回火。

<div class="result-source" markdown="1">

来源：表 1，第 3 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

PH1 | backfire rate ≥ 33% | 60.3% [53.0, 68.2] | 65.6% [58.3, 73.5] | PASS

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 151 道确认题上的最高一致度分箱检验 PH3

<div class="result-value" markdown="1">

预注册上限为 70%；最高一致度分箱中，Qwen2.5-7B 的准确率只有 51.2%（$n=43$），Llama-3-8B 只有 14.3%（$n=21$），PH3 通过；这两个统计量未报告置信区间。

</div>

高一致度并未对应高正确率，尤其 Llama 的结果说明模型可以非常一致地重复错误答案。这直接削弱了“票数越集中，答案越可信”的门控依据。不过，不同模型分箱内样本量较小，且原文未为该统计量计算区间，因此精确数值及模型间差距需要谨慎解释。

<div class="result-source" markdown="1">

来源：表 1，第 3 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

PH3 | top-agree-bin acc. ≤ 70% | 51.2% (n=43)† | 14.3% (n=21)† | PASS

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 模型覆盖范围有限：论文只测试 Qwen2.5-7B 和 Llama-3-8B 两个小型指令微调模型，明确未测试推理原生模型；因此结论不能直接推广到更大模型、专门训练的推理模型或其他解码范式。
- 任务覆盖范围与统计精度有限：评测集中于 GPQA Diamond 的 198 道高难度科学题，部分确认统计量没有置信区间，一致度门的 bootstrap 区间尤其宽；预言机结果又依赖真实标签，仅表示理论上界而非可部署性能。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 单次采样 $N=1$：不进行自洽性聚合，是判断增加推理时计算量究竟改善还是损害准确率的直接参照。
- 固定预算多数投票 $N=64$：从同一问题采样 64 条推理链，并输出出现次数最多的答案；它代表高推理预算下的标准自洽性方法，也是门控策略的固定预算参照。
- 二元预言机 $\{N=1,N=64\}$：利用真实标签为每道题选择两个预算中表现更好的一个。它不是可部署方法，而是衡量一致度门和熵门最多捕获多少潜在收益的上界；预注册的 PH2、PH4 使用该上界。
- 网格预言机 $N\in\{1,2,4,8,16,32,64\}$：利用真实标签逐题选择最佳采样数，是比二元预言机更宽松的事后理论上界。它用于说明逐题预算选择的潜力，不能作为现实系统能够达到的性能。

**实验想回答的问题**

- 在 GPQA Diamond 的高难度科学问题上，小型指令微调语言模型采用自洽性多数投票后，逐题正确率是否经常低于单次采样，即多数投票是否会在多数问题上“适得其反”？
- 无需外部验证器、只依据答案一致度或词元熵进行预算选择的门控方法，能否识别应使用单次采样还是多数投票的问题，并获得接近预言机路由的收益？

**实验实现**

实验评估 Qwen2.5-7B 与 Llama-3-8B 两个不同模型家族的指令微调小模型。标准自洽性对每题采样 $N$ 条思维链并返回复数票答案，预算网格为 $N\in\{1,2,4,8,16,32,64\}$。四项确认性假设及阈值在分析 151 道确认题之前锁定并以 Git 标签记录；PH1 检验回火率，PH2 与 PH4 分别检验一致度门和词元熵门相对二元预言机的收益捕获率，PH3 检验最高一致度分箱准确率。回火率和部分门控结果采用问题级 bootstrap 的 95% 区间，共 1000 次迭代、随机种子 42；带匕首标记的统计量未计算区间。原文还说明 PH2 的区间很宽，预注册判定依据点估计，因此“通过”不等于门控收益已被高精度地限定在阈值以下。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 一致度门相对固定 $N=64$ 与二元预言机的收益捕获率 | 在确认集上，一致度门的预注册要求是捕获率不高于 10%；Qwen2.5-7B 的点估计为 0.8%，95% 区间为 [-89.1, 68.1]，Llama-3-8B 为 -1.6%，区间为 [-92.9, 74.2]，PH2 按预注册的点估计规则通过。 | 该对照隔离了“多数票集中程度能否充当预算路由信号”。点估计接近零或为负，说明它几乎没有捕获二元预言机相对固定 $N=64$ 的潜在收益；但区间极宽，作者也明确承认其与超过 10% 的捕获率相容，所以证据支持“本次实现未显示有效收益”，而不是精确证明所有一致度门都无效。 | 表 1，第 3 节<br><span class="experiment-evidence">PH2 \| agree gate capture ≤ 10% \| 0.8% [-89.1, 68.1] \| -1.6% [-92.9, 74.2] \| PASS</span> |
| 词元熵门相对固定 $N=64$ 与二元预言机的收益捕获率 | 词元熵门采用与 PH2 相同的 10% 捕获率上限；Qwen2.5-7B 的捕获率为 0.5%，Llama-3-8B 为 0.9%，PH4 通过，但原文未为这两个数值计算置信区间。 | 该对照把门控信号从答案票数集中度换成模型输出分布的不确定性，检验失败是否只是因为一致度指标过于粗糙。两模型点估计仍接近零，说明词元熵也未形成有效路由器；由于探索阶段没有收集对数概率且确认结果没有区间，这一消融只能支持当前设定下的负面结果，不能排除其他熵定义或训练式门控方法。 | 表 1，第 3 节<br><span class="experiment-evidence">PH4 \| entropy gate capture ≤ 10% \| 0.5%† \| 0.9%† \| PASS</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文系统评测小型 LLM 在科学推理中自一致性多数投票的失效，并分析推理时扩展与置信度机制。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`94661156e401ce6f35aef79aa7aa182e7946dd6d5e6e940b6c0ca3a6a1fd5e48`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
