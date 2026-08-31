---
title: "[论文解读] SABER: Stability-Aware Early Exit for LLM Reasoning via Adversarial Branch Probing"
description: "[arXiv 2608.27963][LLM 效率] 原文未明确报告。"
arxiv_id: "2608.27963"
announcement_date: "2026-08-31"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:38:24.938013+00:00"
source_sha256: "2cb9803399309ef22b5a5c87ee4c5a702fc58c7be1877527531faf9a92840fd2"
tags:
  - "LLM 效率"
  - "LLM Reasoning"
  - "大型推理模型"
  - "推理时早退"
  - "思维链推理"
  - "对抗分支探测"
  - "推理稳定性"
  - "语义一致性"
  - "置信度稳定性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.27963</p>

# SABER: Stability-Aware Early Exit for LLM Reasoning via Adversarial Branch Probing

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Wanli Cheng, Haiya Xiang, Juntao Li, Hongling Wang, Wenliang Chen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Soochow University, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27963v1) · [PDF 下载](https://arxiv.org/pdf/2608.27963v1) · **关键词** 大型推理模型, 推理时早退, 思维链推理, 对抗分支探测, 推理稳定性, 语义一致性, 置信度稳定性<br>
**代码**: [https://github.com/Bl1nding/SABER](https://github.com/Bl1nding/SABER)

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

本文属于大型语言模型（LLM）推理效率与推理时早退研究。大型推理模型（LRM）通过测试时扩展和长链思维（CoT）处理数学推理、代码生成等复杂任务，但完整生成推理轨迹的计算成本较高，并可能出现“过度思考”：模型在答案已经基本确定后仍继续生成验证或探索步骤。本文关注不修改模型参数的推理时早退，即在生成过程中判断当前中间推理是否已经足够稳定；若稳定则提前停止并输出答案，否则继续推理。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链（Chain-of-Thought，CoT）**

CoT 是模型在给出最终答案前生成的一系列中间推理步骤。它通常能提升复杂任务的解题能力，但步骤越长，推理时间和 token 消耗越高。

</div>
<div class="concept-item" markdown="1">

**推理时早退（inference-time early exit）**

推理时早退是在模型生成完整推理链之前，根据当前状态判断是否可以停止。它不重新训练模型，而是在运行模型时动态地平衡答案质量与计算成本。

</div>
<div class="concept-item" markdown="1">

**语义扰动与稳定性**

语义扰动是在不完全改变问题含义的前提下，对中间推理状态进行局部改写或构造替代分支。若这些分支最终预测相近，说明当前推理状态对局部变化较稳健，可能已经接近可靠答案；若预测差异较大，则表明推理仍不稳定。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个需要多步推理的问题 $x$、一个能够生成长链思维的语言模型，以及生成到某个中间步骤时的推理状态，系统需要在每个候选检查点决定“提前退出”或“继续生成”。SABER 的目标是在不进行完整多步分支展开、也不修改模型参数的条件下，估计当前推理状态是否已经收敛：输入是原始中间状态及其局部语义扰动分支，输出是最终答案预测、稳定性信号和早退决策。其基本假设是，趋向正确答案的推理轨迹在局部语义扰动下会表现出更强的答案一致性和更小的置信度波动，而错误轨迹通常更不稳定。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入问题或待求解任务。

</div>
<div class="notation-item" markdown="1">

**$r_t$**

在推理步骤或检查点 $t$ 时形成的中间推理状态或部分推理轨迹。

</div>
<div class="notation-item" markdown="1">

**$b_i$**

围绕中间状态 $r_t$ 构造的第 $i$ 个分支；分支可以是保持原意的中性分支，也可以是施加语义扰动的对抗分支。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{RSS}$**

Reasoning Stability Score，即综合答案语义一致性与置信度稳定性的推理稳定性分数，用于判断是否早退。

</div>

</div>

**直接相关的工作**

- **DEER 与 EAT 等基于置信度或熵的早退方法**: 这些方法使用中间状态的 token 置信度、答案分布熵或相关不确定性信号决定停止时机，属于与 SABER 直接相关的推理时早退基线。论文指出，LRM 可能在推理错误时仍保持较高置信度，因此单独依赖置信度或熵难以可靠反映推理是否真正稳定。SABER 不只观察单一分支的置信度，而是比较中性分支与扰动分支之间的答案一致性和置信度变化。
- **Dynasor 等基于一致性的早退方法**: 这类方法通过多个中间答案或后续推理轨迹之间的一致性判断模型是否已经收敛，相比单一置信度信号更接近答案稳定性。然而，论文认为它们通常需要连续生成并比较多个后续步骤，因而会延迟早退并增加额外推理开销。SABER 借鉴一致性思想，但使用局部对抗分支的轻量级、答案导向探测，在不完整展开长轨迹的情况下估计稳定性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SABER 是一种无需训练的推理时早停框架，输入为问题 $q$、自回归推理模型 $\mathcal{M}$ 及其当前推理前缀 $\mathcal{P}$。模型正常生成推理内容；当出现代表自我修正或不确定性的触发词 “Wait” 时，SABER 从同一前缀构造中性分支和对抗分支，分别进行轻量级随机探测，收集预测答案与生成置信度，并据此计算语义一致性 $SC$、置信度稳定性 $CS$ 以及综合推理稳定性分数 $RSS$。若 $RSS>\tau$，则注入闭合标记 $</think>$，停止后续长链推理并生成最终答案；否则丢弃探测分支，继续标准推理。直观而言，SABER 不只询问模型“你有多自信”，还故意对当前思路施加一个纠错提示，观察答案是否仍然稳定；若轻微扰动不能改变答案，便认为继续思考的收益可能较低。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 持续生成并定位推理转折点

模型按自回归方式逐 token 生成推理序列 $t_1,t_2,\ldots,t_n$，并持续检查新生成的 token 是否属于 $\mathcal{T}$。完整触发词集合可包括 “Wait”、“Alternatively”、“But”、“So” 和 “Let me double-check”，但实际评估中为降低开销，仅在出现 “Wait” 时执行探测。

<div class="method-step__io" markdown="1">

**输入**：用户问题 $q$、模型 $\mathcal{M}$、当前推理前缀 $\mathcal{P}$、转折触发词集合 $\mathcal{T}$。<br>
**输出**：更新后的推理前缀，以及一个待评估的中间推理状态。

</div>

**直观理解**：模型先像平常一样一步步解题。SABER 把 “Wait” 看作模型可能正在回顾、纠错或转换子目标的时刻，并在这里暂停检查是否还值得继续。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造中性与对抗探测分支

将中性提示 “Wait, let me summarize. The answer is \$\boxed{$” 和对抗提示 “Wait, I think my previous reasoning was incorrect. After correcting it, the answer is \$\boxed{$” 分别追加到 $\mathcal{P}$，得到 $\mathcal{P}_n$ 与 $\mathcal{P}_a$。前者要求总结当前思路，后者注入“先前推理可能错误”的语义扰动。

<div class="method-step__io" markdown="1">

**输入**：同一当前推理前缀 $\mathcal{P}$，以及两个固定探测模板。<br>
**输出**：中性探测前缀 $\mathcal{P}_n$ 和对抗探测前缀 $\mathcal{P}_a$。

</div>

**直观理解**：两个分支从完全相同的解题记录出发，区别只在于提示是否暗示需要纠错。这样可以把“答案是否稳定”与“模型是否恰好受到不同历史内容影响”区分开。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 并行采样并提取答案与置信度

在每个分支上进行 $k$ 次随机解码，形成答案多重集合 $\mathcal{A}_n$ 和 $\mathcal{A}_a$，并为每个生成延续计算基于 token 预测概率的长度归一化几何平均置信度，形成置信度集合 $\mathcal{C}_n$ 和 $\mathcal{C}_a$。探测分支受到长度限制并可在推理引擎中并行执行，因此不需要完整展开两条长推理轨迹。

<div class="method-step__io" markdown="1">

**输入**：两个探测前缀 $\mathcal{P}_n$、$\mathcal{P}_a$，采样数 $k$，以及模型词表 $\mathcal{V}$。<br>
**输出**：两组答案样本 $\mathcal{A}_n,\mathcal{A}_a$，以及两组置信度 $\mathcal{C}_n,\mathcal{C}_a$。

</div>

**直观理解**：每个提示不是只问一次，而是随机问 $k$ 次，避免单次生成的偶然性。系统同时记录“答了什么”和“答得有多确定”，为后面的稳定性判断提供两类证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算稳定性并作早停决策

首先用多重集合 Jaccard 相似度计算语义一致性 $SC$，再比较两个分支的平均置信度并计算 $CS$，最后按 $RSS=\alpha SC+(1-\alpha)CS$ 融合两类信号。若 $RSS>\tau$，将 $</think>$ 追加到原推理前缀并退出推理循环；否则丢弃探测结果，回到正常生成流程。

<div class="method-step__io" markdown="1">

**输入**：答案多重集合 $\mathcal{A}_n,\mathcal{A}_a$、置信度集合 $\mathcal{C}_n,\mathcal{C}_a$、权重 $\alpha$、敏感系数 $\gamma$ 和早停阈值 $\tau$。<br>
**输出**：早停后的最终答案 $y$，或继续生成后的完整推理与最终答案。

</div>

**直观理解**：答案内容一致说明模型在语义上没有被扰动带偏，置信度差异小则说明其把握程度也没有明显变化。两者都足够稳定时就停止；只要仍不稳定，就让模型继续思考。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 语义一致性

$$
SC=\frac{\sum_{a\in\mathcal{A}_{n}\cup\mathcal{A}_{a}}\min(f_{n}(a),f_{a}(a))}{\sum_{a\in\mathcal{A}_{n}\cup\mathcal{A}_{a}}\max(f_{n}(a),f_{a}(a))}
$$

**符号说明**

- $SC$：中性分支与对抗分支之间的语义一致性分数，数值越高表示答案分布越相似。
- $\mathcal{A}_{n}$：中性探测分支经过 $k$ 次随机采样得到的答案多重集合。
- $\mathcal{A}_{a}$：对抗探测分支经过 $k$ 次随机采样得到的答案多重集合。
- $a$：两个分支答案多重集合并集中的某个候选答案。
- $f_n(a)$：答案 $a$ 在中性答案多重集合 $\mathcal{A}_n$ 中出现的次数。
- $f_a(a)$：答案 $a$ 在对抗答案多重集合 $\mathcal{A}_a$ 中出现的次数。
- $\min,\max$：分别取两个分支对同一答案出现次数的较小值和较大值。

<div class="equation-explanation" markdown="1">

**直观理解**：分子统计两个分支对各答案共同支持的部分，分母统计它们的总体支持范围。因此，两个分支越频繁地产生相同答案，$SC$ 越接近高值；答案分布差异越大，$SC$ 越低。该设计比单次答案匹配更能抵抗随机采样噪声。<br>
**原文位置**：第 3.2 节“Semantic Consistency”，公式（3）

</div>

</div>

<div class="equation-block" markdown="1">

#### 推理稳定性分数与早停规则

$$
RSS=\alpha\cdot SC+(1-\alpha)\cdot CS,\quad CS=e^{-\gamma\cdot\left|\bar{P}_{n}-\bar{P}_{a}\right|},\quad \text{early exit if }RSS>\tau
$$

**符号说明**

- $RSS$：综合推理稳定性分数，用于判断当前推理状态是否已经收敛。
- $\alpha$：语义一致性在综合分数中的权重，取值范围为 $[0,1]$。
- $CS$：置信度稳定性分数，数值越高表示两个分支的平均置信度差异越小。
- $\gamma$：置信度差异的敏感系数，控制 $CS$ 对分支间置信度波动的惩罚强度。
- $\bar{P}_{n}$：中性分支 $k$ 次采样置信度的平均值。
- $\bar{P}_{a}$：对抗分支 $k$ 次采样置信度的平均值。
- $\tau$：早停阈值；只有当综合稳定性分数超过该阈值时才终止推理。
- $e$：自然指数的底数，用于将置信度差异映射为 $0$ 到 $1$ 范围内的稳定性分数。

<div class="equation-explanation" markdown="1">

**直观理解**：当两个分支的答案一致且平均置信度接近时，$SC$ 和 $CS$ 都较高，因而 $RSS$ 较高。超过 $\tau$ 后，SABER 认为继续生成的边际收益有限；否则继续推理，以优先避免不可靠的过早停止。<br>
**原文位置**：第 3.2 节公式（6）、第 3.3 节公式（7）及附录 B.2 算法第 22–26 行

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。SABER 被明确设计为 training-free 方法，不引入新的参数训练、监督标签或额外优化目标；模型原有参数保持不变，方法只在解码阶段计算探测分支、稳定性分数并执行早停。因此不存在需要最小化的 SABER 训练损失，$\alpha$、$\gamma$ 和 $\tau$ 是推理决策中的超参数，而不是通过本文所述训练过程学习得到的参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 对抗分支探测**

SABER 在同一中间推理前缀上建立中性分支和对抗分支。中性提示要求模型总结并给出答案，对抗提示明确声称先前推理可能错误并要求纠正；每个分支进行 $k$ 次随机采样，从而以受控语义扰动近似检验中间状态的鲁棒性。

> 直观理解：如果一个解答已经真正接近稳定结论，那么加入“请检查你可能错了”的提示后，答案通常不会大幅改变。若答案经常改变，说明模型还没有形成可靠的结论。

**2. 双信号稳定性估计**

语义一致性 $SC$ 比较两个分支答案多重集合中的出现频率，能够识别答案分布是否一致；置信度稳定性 $CS$ 则比较两个分支的平均置信度差异，并通过指数函数惩罚置信度波动。二者分别覆盖“预测内容是否一致”和“模型确定性是否一致”两个方面。

> 直观理解：只看答案可能漏掉一种情况：两个分支碰巧给出同一答案，但其中一个分支的模型已经明显变得不确定。加入置信度稳定性后，系统要求答案和信心都保持一致，判断更谨慎。

**3. 阈值式自适应早停**

系统将 $SC$ 与 $CS$ 按权重 $\alpha$ 融合为 $RSS$，并在每个可探测的中间节点与阈值 $\tau$ 比较。超过阈值时注入 $</think>$ 终止显式推理并触发最终答案生成；未超过时继续原始自回归解码。

> 直观理解：不同题目需要的思考长度不同，因此不是固定生成若干 token 后统一停止。稳定得早的题目可以早停，不稳定的题目则保留更多推理预算。

**训练与推理**

训练阶段：原文未报告 SABER 的训练过程，因为该方法不进行额外训练。推理阶段首先输入问题 $q$，令模型 $\mathcal{M}$ 正常自回归生成并更新前缀 $\mathcal{P}$；当生成 token 属于触发集合 $\mathcal{T}$ 时，分别追加中性和对抗探测模板，得到 $\mathcal{P}_n$ 与 $\mathcal{P}_a$。随后在两个分支上各采样 $k$ 次，得到答案集合和逐样本置信度，计算 $SC$、$CS$ 和 $RSS$；若 $RSS>\tau$，向原前缀注入 $</think>$ 并生成最终答案 $y$，否则删除探测分支并恢复标准推理，直到触发早停或达到最大长度 $L_{\max}$。

**复现信息**

方法在 vLLM 推理框架中作为标准自回归生成之上的解码时干预实现，探测分支受到严格长度约束并并行执行，以控制额外开销。实验中置信度敏感系数 $\gamma$ 在所有设置中固定为 $3$；$\tau$ 对 DeepSeek-R1-Distilled-Qwen-7B 设为 $0.9$，对 Qwen3 系列模型设为 $0.95$；$\alpha$、采样数 $k$ 和最大长度 $L_{\max}$ 的具体取值原文未明确报告。显式使用推理分隔符的模型通过注入闭合 token $</think>$ 结束推理；触发词设计和额外设置见附录 B.3 与附录 A.1。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：小学数学应用题基准，用于检验相对简单、步骤较短的数学推理；选文给出了不同模型和$\alpha$设置下的准确率与平均令牌数，但未明确报告完整数据规模、划分方式和样本数。
- MATH-500：数学竞赛题子集，用于测试数学推理中的早退决策与采样数影响；选文报告了Qwen3-8B上的采样数消融，并比较了不同停止阈值下的效率—准确率曲线，但未明确报告完整划分与规模。
- OlympiadBench：较困难的奥林匹克数学推理基准，用于检验早退在长链、易出错推理上的可靠性，以及$\alpha$和停止阈值$\tau$的敏感性；选文未明确报告其完整数据规模和划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

任务答案的正确率，衡量早退是否损害最终推理质量。 （越高越好；但应结合令牌数判断是否以更高计算成本换取准确率。）

</div>
<div class="metric-item" markdown="1">

**Average token count**

每个样本平均生成的推理令牌数，反映推理计算量和成本。 （越低越好，但不能脱离准确率单独解释。）

</div>
<div class="metric-item" markdown="1">

**Inference latency**

端到端推理耗时，单位为秒；它衡量令牌减少是否实际转化为墙钟时间加速。 （越低越好；只有在硬件和实现条件相同的比较中，才能直接归因于方法效率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 完整推理与SABER及替代评分函数的比较；DeepSeek-R1-Distill-Qwen-7B，覆盖GSM8K、MATH-500、Olympiad、AIME24/25和GPQA-D。

<div class="result-value" markdown="1">

表5中，SABER的总体准确率为$64.8\%$、总体压缩率为$69.7\%$；Vanilla为$63.2\%$、$100\%$令牌成本。SABER在GSM8K上为$91.0\%/662$个令牌，在MATH-500上为$91.2\%/2,401$个令牌，在AIME24/25上为$50.9\%/9,333$个令牌，在GPQA-D上为$34.8\%/3,326$个令牌。

</div>

这说明在该模型和这些任务上，SABER平均使用约七成的基线令牌，同时总体准确率高于完整推理表中的数值。它支持“早退可以显著节省推理成本”的作者结论，但不等于所有模型、数据集或部署环境都能获得相同收益；表5也没有单独证明每个任务上的准确率都提高。

<div class="result-source" markdown="1">

来源：Appendix C.2, Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

RSS (Ours) 91.0 662 91.2 2,401 56.1 5,560 50.9 9,333 34.8 3,326 64.8 69.7%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 端到端推理延迟比较；在GSM8K、AIME24和GPQA-D上比较Vanilla与SABER。

<div class="result-value" markdown="1">

三种模型的平均延迟均下降：R1-Distill-Qwen-7B从$149.4$秒降至$92.9$秒，Qwen3-4B从$190.1$秒降至$107.0$秒，Qwen3-8B从$243.0$秒降至$98.5$秒；平均降幅为$48.8\%$。

</div>

令牌节省在端到端时间上确实表现为明显加速，尤其是原本推理轨迹较长的模型。该结果支持方法具有实际部署价值，但延迟依赖硬件、并行化和探测实现；选文未提供这些条件，因此不能把降幅直接推广到所有系统。

<div class="result-source" markdown="1">

来源：Section 5.6, Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Average 194.2 99.5 48.8%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 探测开销与早退收益的成本—收益分析；默认配置下比较三种模型的探测令牌与总令牌。

<div class="result-value" markdown="1">

探测令牌占总生成令牌的比例分别为R1-Distill-Qwen-7B的$4.9\%$、Qwen3-4B的$2.8\%$和Qwen3-8B的$3.8\%$，平均为$3.8\%$；对应探测令牌分别为$221$、$147$和$181$，总令牌分别为$4,477$、$5,221$和$4,815$。

</div>

对抗分支不是免费操作，但在默认设置下只占较小的令牌比例，因此作者认为早退节省的主推理成本超过探测成本。该分析说明开销相对可控，却没有单独给出探测所需的实际额外墙钟时间或显存开销。

<div class="result-source" markdown="1">

来源：Section 5.5, Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Average 183 4,838 3.8%

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

- Vanilla：完整长度推理，不使用早退，作为准确率上限附近的效率参照和令牌成本基线。
- SC-only：只使用语义一致性作为停止信号，用于隔离语义稳定性单独判断早退的效果。
- CS-only：只使用置信度稳定性作为停止信号，用于检验单独依赖置信度是否会在错误但稳定的轨迹上过早退出。
- Confidence-only early exit：只根据中性分支的置信度停止，并移除对抗分支，用于直接检验对抗分支探测是否带来额外收益。

**实验想回答的问题**

- 在保持接近完整推理准确率的条件下，SABER能否减少大型推理模型的推理令牌消耗，并改善端到端推理延迟？
- SABER的双分支对抗探测、稳定性评分、采样数、权重$\alpha$和停止阈值$\tau$分别如何影响准确率、令牌成本与效率—准确率权衡？

**实验实现**

实验覆盖多个推理模型，包括R1-Distill-Qwen-7B、Qwen3-4B和Qwen3-8B；选文明确报告了这些模型，但未完整列出所有主实验表及其实现环境。SABER在中间推理状态处构造中性分支与语义扰动的对抗分支，通过轻量探测预测两条分支的最终结果，再根据语义一致性和置信度稳定性联合评分；当稳定性超过停止阈值$\tau$时提前结束，否则继续主推理。采样数$k$在消融中取$\{1,2,4,8,16,32\}$，$\alpha$在敏感性实验中取$0.3$、$0.5$和$0.7$。延迟实验在GSM8K、AIME24和GPQA-D上汇报三种模型的平均耗时；选文未明确报告随机种子、重复次数、硬件、批大小和完整解码参数。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 组件消融：SC-only、CS-only与完整RSS；在两个推理模型和四个基准上比较。 | 完整RSS在所有任务上总体优于两种单信号配置；在GSM8K和MATH-500等简单任务上三者表现接近，而在AIME24和GPQA-D等困难任务上SC-only与CS-only均明显退化。 | 该实验隔离了两个稳定性信号各自的贡献。语义一致但答案错误时，SC-only可能过早退出；轨迹置信度稳定但推理错误时，CS-only也可能失效。因此，联合信号能降低单一判据对“看起来稳定”的误判，但选文未给出图3中各配置的完整数值。 | Section 5.1, Figure 3<br><span class="experiment-evidence">Overall, RSS outperforms both single-signal variants across all tasks, highlighting the importance of jointly modeling semantic consistency and confidence stability.</span> |
| 评分函数消融：固定中性/对抗双分支探测框架，仅将RSS替换为$SC\cdot CS$或Branch-UQ Diff。 | 表5中，RSS总体准确率/压缩率为$64.8\%/69.7\%$，$SC\cdot CS$为$63.8\%/75.1\%$，Branch-UQ Diff为$62.8\%/69.1\%$；RSS准确率最高，而$SC\cdot CS$使用的令牌更少。 | 因为双分支框架保持不变，该实验主要检验收益是否只来自特定的RSS公式。两种替代评分仍然有效，支持“双分支探测是主要来源”的解释；但RSS在准确率与总体权衡上更好，说明加权联合评分比简单乘积或分支不确定性差值更适合作为停止标准。 | Appendix C.2, Table 5<br><span class="experiment-evidence">SC ⋅ CS 91.1 659 91.4 2,509 56.1 5,505 48.4 9,697 31.8 4,576 63.8 75.1%</span> |

**定性案例**

- 扰动提示词分析将探测行为分为Self-Correction、Reflection、Alternative Path和Verification四类。Qwen3-4B上，默认SABER的总体准确率为$76.0\%$、平均令牌数为$4,128$；四种变体中Self-Correction为$75.5\%/3,756$，Verification为$74.1\%/3,519$。这表明不同提示风格改变效率—准确率取舍，但方法不依赖某个精确措辞；它更像是在中间状态施加一次“换个角度检查”的轻量压力测试。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出基于对抗分支探测的训练无关早退机制，以降低长链LLM推理的推理成本并保持准确率。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`2cb9803399309ef22b5a5c87ee4c5a702fc58c7be1877527531faf9a92840fd2`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
