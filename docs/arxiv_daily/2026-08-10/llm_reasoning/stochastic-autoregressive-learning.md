---
title: "[论文解读] Stochastic Autoregressive Learning"
description: "[arXiv 2608.07224][LLM Reasoning] 本文把确定性自回归学习推广到随机生成器，研究在基础单步、完整思维链与仅终点三种监督下，学习最终词元概率所需的样本量能否建立普适比较。"
arxiv_id: "2608.07224"
announcement_date: "2026-08-10"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-11T02:33:04.179667+00:00"
source_sha256: "c148e3dc00b72babf3f1c34e617ae6ddf4d6ede669d76e610421104c9c860b07"
tags:
  - "LLM Reasoning"
  - "随机自回归学习"
  - "PAC学习"
  - "大语言模型"
  - "链式思维监督"
  - "端到端监督"
  - "样本复杂度"
  - "VC维"
  - "脂肪散度"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.07224</p>

# Stochastic Autoregressive Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Ilan Doron-Arad, Idan Mehalel, Elchanan Mossel</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> MIT；The Hebrew University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.07224v1) · [PDF 下载](https://arxiv.org/pdf/2608.07224v1) · **关键词** 随机自回归学习, PAC学习, 大语言模型, 链式思维监督, 端到端监督, 样本复杂度, VC维, 脂肪散度<br>


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

本文把确定性自回归学习推广到随机生成器，研究在基础单步、完整思维链与仅终点三种监督下，学习最终词元概率所需的样本量能否建立普适比较。

**不用术语来说**：语言模型不会在每一步固定输出某个词元，而是先给出概率分布，再从中随机采样；因此，即使训练数据展示了完整生成过程，每个中间词元也只是对应概率的一次随机观测，而不是该概率的准确答案。论文要弄清楚：若生成过程持续 $M$ 步，看到完整轨迹究竟能节省多少训练样本，以及只看到最后一个词元会额外增加多少学习难度。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出二元随机自回归的 PAC 回归模型，用同一生成器 $g$ 在不断扩展的提示上迭代采样，并统一定义基础单步、完整思维链（$\mathsf{CoT}$）和端到端（$\mathsf{e2e}$）三种监督的样本复杂度，使随机生成中的“学习最终词元概率”成为可严格比较的问题。
- 作者指出确定性理论的样本复杂度关系不能直接延伸到随机情形：在相同精度尺度上，基础学习、$\mathsf{CoT}$ 学习与 $\mathsf{e2e}$ 学习之间除显然关系外不存在统一比较，因此需要改变误差尺度，才能建立有意义的普适上界及紧性结论。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究概率自回归学习，即学习一个对每个提示字符串输出下一令牌概率分布的生成器。与确定性自回归模型不同，本文中的生成器对每一步令牌进行随机采样：从初始提示开始，将采样令牌追加到提示中，再对扩展后的字符串重复使用同一个生成器，共进行 $M$ 步。研究目标是在概率近似意义下理解三类监督信息，即单步样本、揭示完整随机轨迹的链式思维样本，以及只揭示最终令牌的端到端样本，分别需要多少训练样本才能学习生成器的相关概率。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**PAC学习**

PAC学习研究如何利用有限随机样本，从假设类中找到一个预测函数，使其在总体分布上的误差以较高概率较小。本文将样本复杂度定义为达到平方损失误差 $4\varepsilon$ 所需的最少样本数。

</div>
<div class="concept-item" markdown="1">

**自回归生成**

自回归生成是指模型根据当前提示预测下一个令牌，并把该令牌追加回提示，再预测下一令牌。本文特别关注这一过程连续运行 $M$ 步后，随机性如何影响学习难度。

</div>
<div class="concept-item" markdown="1">

**VC维与脂肪散度**

VC维衡量二值函数类能够独立实现多少种标记模式；脂肪散度则是其适用于实值函数的、依赖精度尺度 $4\gamma$ 的版本。二者用于刻画函数类的复杂度，从而推导分布无关的学习样本界。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

设令牌字母表为 $4\Sigma$，提示字符串空间为 $4\Sigma^{\star}$，随机生成器类为 $4\mathcal{F}\subseteq\Delta(\Sigma)^{\Sigma^{\star}}$，其中 $4\Delta(\Sigma)$ 表示令牌集合上的概率分布。给定生成器 $4g\in\mathcal{F}$ 和初始提示，模型在每一步依据当前提示的下一令牌分布采样一个令牌并追加到提示，重复 $M$ 次。本文重点讨论二值令牌情形，此时每个提示对应一个伯努利下一令牌分布。三种监督设置分别是：base仅提供单步采样并要求学习一步概率；CoT提供长度为 $M$ 的完整随机轨迹并要求学习 $M$ 步后的最终令牌概率；e2e仅提供长度为 $M$ 轨迹的最终令牌并完成同样的最终概率学习。对每种设置，$m_{\mathrm{base}}(\varepsilon)$、$m_{\mathsf{CoT}}(\varepsilon)$ 和 $m_{\mathsf{e2e}}(\varepsilon)$ 表示达到平方损失误差 $4\varepsilon$ 所需的最少样本数。论文还通过由 $4\mathcal{F}$ 诱导的一步类 $4\mathcal{F}^{\mathsf{e2e}-1}$ 和 $M$ 步端到端类 $4\mathcal{F}^{\mathsf{e2e}-M}$ 描述这些学习目标的函数复杂度。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{F}\subseteq\Delta(\Sigma)^{\Sigma^{\star}}$**

随机生成器函数类；每个生成器将提示字符串映射为 $4\Sigma$ 上的概率分布。

</div>
<div class="notation-item" markdown="1">

**$\Sigma^{\star}$**

由令牌表 $4\Sigma$ 中有限个令牌组成的全部提示字符串集合。

</div>
<div class="notation-item" markdown="1">

**$M$**

自回归生成链的步数，即从初始提示开始连续采样并追加令牌的次数。

</div>
<div class="notation-item" markdown="1">

**$m_{\mathrm{base}}(\varepsilon),m_{\mathsf{CoT}}(\varepsilon),m_{\mathsf{e2e}}(\varepsilon)$**

在平方损失误差 $4\varepsilon$ 下，base、CoT 和 e2e 三种任务各自所需的最少样本数。

</div>

</div>

**直接相关的工作**

- **Joshi 等人在 COLT 2025 提出的确定性自回归学习框架**: 本文将该确定性框架推广到随机生成器：原框架中的下一令牌行为是确定的，而本文允许生成器为每个提示指定伯努利下一令牌分布，并研究不同监督形式下的样本复杂度。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现代语言模型通过下一词元分布逐步采样，而非反复应用一个确定性标签函数。似然训练直接学习词元概率，采样用于产生多样化续写，自一致性等方法还会汇总同一提示下的多条随机轨迹。因此，理论模型若忽略随机性，就无法说明完整推理轨迹在概率学习中提供了多少有效信息，也无法评估只记录最终输出时的数据需求。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **确定性自回归思维链学习**：既有框架将一个确定性下一词元函数迭代 $M$ 次；$\mathsf{CoT}$ 监督展示全部中间词元，$\mathsf{e2e}$ 监督只展示最终词元，学习目标是预测确定性的最终标签。相关工作以 VC 维等工具比较基础、$\mathsf{CoT}$ 与 $\mathsf{e2e}$ 学习的样本复杂度。
- **普通一步随机回归**：对提示 $X$ 只观测一次伯努利输出 $Y\sim\operatorname{Bern}(p_g(X))$，并在平方损失下估计一步概率 $p_g$。它能够刻画概率标签的噪声，但不包含概率经过多步随机状态转移后如何共同决定最终词元概率的问题。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 确定性模型中，一条完整轨迹会揭示各个已访问状态的精确中间标签；随机模型中，同样的轨迹只为每个中间概率提供一次伯努利样本。因此，确定性结论所依赖的“轨迹直接给出正确中间监督”不再成立，把其样本复杂度比较直接套用于随机语言生成可能严重低估数据需求。
- 既有随机回归只处理一步映射，无法回答局部概率估计误差在 $M$ 步随机迭代中如何传播，也无法量化完整轨迹与仅最终词元之间的信息差距。除 $m_{\mathsf{CoT}}^{\mathcal F,M}(\varepsilon,\delta)\leq m_{\mathsf{e2e}}^{\mathcal F,M}(\varepsilon,\delta)$ 这类由“忽略中间词元”得到的显然关系外，原文指出此前缺少一般性的复杂度比较。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚无适用于任意随机生成器类 $\mathcal F$ 的理论分类，能够说明一步概率的基础学习、完整轨迹监督下的最终概率学习，以及仅终点监督下的最终概率学习之间是否存在统一的样本复杂度换算关系。尤其未知的是，确定性情形中 $\mathsf{CoT}$ 近似把多步任务化为基础学习、而 $\mathsf{e2e}$ 至多随链长显著变难的结构，在平方损失概率回归中是否仍然成立。

</div>
<div markdown="1"><span>核心问题</span>

对给定生成长度 $M$、误差 $\varepsilon$ 和生成器类 $\mathcal F$，三个样本复杂度 $m_{\rm base}^{\mathcal F}(\varepsilon)$、$m_{\mathsf{CoT}}^{\mathcal F,M}(\varepsilon)$ 与 $m_{\mathsf{e2e}}^{\mathcal F,M}(\varepsilon)$ 能否在同一精度下普适比较；若不能，必须怎样调整误差尺度，才能给出对所有函数类成立且基本紧致的上界？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把最终词元看成均值为 $q_g^{\mathsf{e2e}-M}(x)$ 的伯努利观测，并用平方损失直接学习这个均值。完整轨迹虽然不能揭示任何中间概率的精确值，却同时留下了沿随机路径访问到的状态及其下一步样本，因而可能帮助恢复局部转移概率；只看终点则把所有中间随机性压缩成一个比特。通过分别形式化这两种信息结构，并允许基础任务与多步任务在不同误差尺度上比较，便可区分“局部概率估得多准”与“这些误差经过 $M$ 步后对最终概率影响多大”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该论文研究随机自回归学习：一个固定生成器 $g$ 为每个提示字符串 $s$ 指定下一令牌为 $1$ 的概率 $p_g(s)$，随后反复采样并把令牌追加到提示中，共生成 $M$ 步。方法论上，论文先把完整轨迹中的每个局部转移视为带标签的二分类样本，再通过轨迹耦合分析局部概率误差如何累积为最终令牌概率误差；对于端到端监督，则利用覆盖数、fat-shattering 维数和信息论论证控制可学习性，并在逻辑函数类上给出具体学习算法。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 定义随机自回归生成过程

从 $X$ 开始，在第 $t$ 步按照 $\operatorname{Bern}(p_g(S_t))$ 采样令牌 $Z_t$，并令 $S_{t+1}=S_tZ_t$；重复该过程直到得到长度为 $M$ 的轨迹。

<div class="method-step__io" markdown="1">

**输入**：初始提示 $X$、生成步数 $M$、生成器 $g$ 及其一步概率函数 $p_g(s)=\Pr_g(Z=1\mid s)$。<br>
**输出**：完整轨迹 $(X,Z_1,\ldots,Z_M)$，以及目标函数 $q_g^{\mathsf{e2e}-M}(X)=\Pr_g(Z_M=1\mid X)$。

</div>

**直观理解**：生成器像一个固定的打字规则：每次只根据当前字符串决定下一个字符出现的概率。新字符加入后，规则再次作用于更长的字符串，因此早期的小误差可能影响后续多步。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 区分三种监督信号

Base 学习直接使用状态—下一令牌对 $(S,Y)$；CoT 学习保留整条 $(X,Z_1,\ldots,Z_M)$ 轨迹；e2e 学习只保留 $(X,Z_M)$，并以最终令牌概率为预测目标。

<div class="method-step__io" markdown="1">

**输入**：由真实生成器产生的样本，可分别观察一步样本、完整轨迹或仅最终令牌。<br>
**输出**：三类不同的学习任务：估计一步概率 $p_g$，或估计长度为 $M$ 的最终概率 $q_g^{\mathsf{e2e}-M}$。

</div>

**直观理解**：三种设置相当于观察过程的不同程度：Base 看到局部答案，CoT 看到完整推理路径，e2e 只看到最后答案。论文比较的是这些信息形式对样本数量的影响。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 把完整轨迹还原为一步样本并进行上界归约

从每条轨迹中随机选择 $T\sim\operatorname{Unif}([M])$，构造 $S=S_T=XZ_1\cdots Z_{T-1}$ 和 $Y=Z_T$，得到合法的一步样本。用真实生成器与估计生成器的逐步耦合、Jensen 不等式和 Cauchy–Schwarz 不等式，将一步平方损失控制为最终概率平方损失。

<div class="method-step__io" markdown="1">

**输入**：CoT 轨迹 $(X,Z_1,\ldots,Z_M)$ 以及一个能够学习 $p_g$ 的 Base 学习器。<br>
**输出**：若 Base 学习器在随机状态分布上的平方损失达到 $\varepsilon/M^2$，则构造出的生成器在 CoT 目标上的平方损失达到 $\varepsilon$，即 CoT 学习可由更高精度的 Base 学习完成。

</div>

**直观理解**：一条完整轨迹包含 $M$ 个局部训练例子；随机抽一个就能模拟 Base 数据。由于误差最多在 $M$ 个位置逐步累积，局部精度需要提高到原目标的约 $1/M^2$。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分析端到端学习及逻辑函数实例

一般情形下，用 e2e 预测函数的分离性、覆盖数和 fat-shattering 维数刻画样本复杂度，并用 Fano 不等式证明 e2e 相比 CoT 的额外代价。逻辑函数情形下，CoT 将每个轨迹中的 $M$ 个状态—令牌转移作为逻辑回归样本，最小化经验逻辑损失；e2e 则直接学习由多步马尔可夫过程诱导的最终概率函数。

<div class="method-step__io" markdown="1">

**输入**：仅含最终令牌的 e2e 样本、生成器类 $\mathcal F$，以及在逻辑函数类中受限维度的参数向量 $w$。<br>
**输出**：一般上界形式为 e2e 学习复杂度至多为 $\widetilde O((M/\varepsilon)m_{\mathsf{CoT}}(\Theta(\varepsilon)))$；逻辑函数的 CoT 学习是有效且 proper 的，而 e2e 学习的证明给出 improper、通常不高效的回归器。

</div>

**直观理解**：CoT 暴露中间状态，所以可以把一次长生成拆成许多普通监督样本。e2e 隐藏了这些中间信息，只能从最终结果反推大量潜在符号，因此通常需要更多数据。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### CoT 轨迹到 Base 样本的误差传播界

$$
\left(q_{g_{\star}}^{\mathsf{e2e}-M}(x)-q_{\widehat{g}}^{\mathsf{e2e}-M}(x)\right)^{2}\leq M\cdot\mathbb{E}\left[\sum_{t=1}^{M}\left(p_{g_{\star}}(S_{t})-\widehat{p}(S_{t})\right)^{2}\,\middle|\,X=x\right]
$$

**符号说明**

- $g_{\star}$：真实生成器。
- $\widehat{g}$：由学习器估计得到的生成器。
- $q_{g}^{\mathsf{e2e}-M}(x)$：从提示 $x$ 出发生成 $M$ 步后，最终令牌为 $1$ 的概率。
- $p_g(S_t)$：第 $t$ 步状态 $S_t$ 下，下一令牌为 $1$ 的一步概率。
- $M$：自回归生成的步数。

<div class="equation-explanation" markdown="1">

**直观理解**：最终预测的平方误差由整条轨迹上各步的一步概率误差共同决定。对时间步求和并乘以 $M$ 表明误差可能随生成长度累积，因此要达到最终精度 $\varepsilon$，一步学习通常需要达到约 $\varepsilon/M^2$ 的精度。<br>
**原文位置**：第 5.1 节证明草图，Theorem 5.1

</div>

</div>

<div class="equation-block" markdown="1">

#### 逻辑函数类的经验训练目标

$$
\widehat{L}_{n}(w)=\frac{1}{nM}\sum_{i=1}^{n}\sum_{t=1}^{M}\left[\log\left(1+\exp(\langle w,Y_{i,t}\rangle)\right)-Z_{i,t}\langle w,Y_{i,t}\rangle\right]
$$

**符号说明**

- $\widehat{L}_n(w)$：参数向量 $w$ 的经验逻辑损失。
- $n$：完整 CoT 轨迹的数量。
- $M$：每条轨迹包含的转移数量。
- $Y_{i,t}$：第 $i$ 条轨迹第 $t$ 步的状态，即当前提示的末尾 $d$ 个比特。
- $Z_{i,t}$：第 $i$ 条轨迹第 $t$ 步实际生成的二值令牌。
- $w$：逻辑函数生成器的 $d$ 维权重向量。

<div class="equation-explanation" markdown="1">

**直观理解**：训练时把每条完整轨迹拆成 $nM$ 个逻辑回归样本，并选择使预测令牌概率最符合观测令牌的权重 $w$。该目标是凸函数，所以在参数范围受限时可以用多项式时间优化方法求解。<br>
**原文位置**：第 8.2 节证明草图，Theorem 8.2

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：一般生成器类的核心目标是在提示分布 $P$ 下最小化目标概率函数的平方损失，例如估计一步概率时最小化 $\mathbb{E}_{S\sim P}[(p_g(S)-\widehat p(S))^2]$，估计端到端输出时最小化 $\mathbb{E}_{X\sim P}[(q_g^{\mathsf{e2e}-M}(X)-\widehat q(X))^2]$。对于维度为 $d$ 的逻辑函数类，CoT 训练具体实现为最小化经验逻辑损失 $\widehat L_n(w)$；由于该损失对 $w$ 凸，优化结果可输出类内生成器 $g_{\widehat w}$。e2e 的一般上界主要是存在性和覆盖数论证，论文明确指出该学习器是 improper 且不保证计算高效。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 随机自回归生成器**

生成器由一步概率函数 $p_g(s)$ 定义，并通过 $M$ 次 Bernoulli 采样诱导最终概率 $q_g^{\mathsf{e2e}-M}(x)$。在维度为 $d$ 的逻辑函数类中，$p_w(s)=\sigma(\langle w,\operatorname{tail}_d(s)\rangle)$，因此过程可视为定义在最近 $d$ 个比特状态上的有限马尔可夫链。

> 直观理解：模型只规定“当前提示后生成 $1$ 的概率”，完整输出不是一次计算出来的，而是反复随机走 $M$ 步得到的。逻辑函数特例进一步限制了模型只关注提示末尾的 $d$ 个比特。

**2. CoT 到 Base 的随机抽样归约**

对每条完整轨迹随机选择时间 $T$，使用 $(S_T,Z_T)$ 作为一步监督样本；轨迹耦合显示，若一步预测误差的平方平均值为 $\delta$，则最终概率平方误差至多为 $M^2\delta$。

> 直观理解：完整轨迹不仅提供最后答案，还提供沿途每一步的训练信号。归约把这些沿途记录整理成普通的一步预测数据，从而复用 Base 学习器。

**3. 覆盖数与统计学习分析**

对 e2e 诱导函数类 $\mathcal F^{\mathsf{e2e}-M}$，若生成器在有限自回归树上逐点接近，则通过逐步耦合得到最终概率接近；随后用覆盖数和 fat-shattering 维数上界控制回归样本复杂度。逻辑函数类中，最终概率经变量替换 $u_j=e^{w_j}$ 后成为有理函数，可用伪维数分析。

> 直观理解：该模块不直接枚举所有随机轨迹，而是先问：需要多少个代表函数才能近似整个函数类。代表函数越多，区分真实模型所需的样本通常越多。

**训练与推理**

训练阶段首先根据监督形式整理数据：Base 直接使用状态—下一令牌样本，CoT 将每条长度为 $M$ 的轨迹展开为 $M$ 个逻辑回归样本，e2e 则只用初始提示和最终令牌。对 CoT，优化经验损失得到 $\widehat w$ 或对应生成器；对一般 e2e 学习，先用有限覆盖或代表预测函数近似候选的最终概率函数，再根据最终令牌样本进行有界回归。

**复现信息**

复现理论方法所需的关键设定是二值令牌、固定生成器、长度为 $M$ 的重复采样，以及明确的初始提示分布。逻辑函数模型只使用提示末尾 $d$ 个比特作为状态特征；CoT 优化在一个多项式有界的参数盒上进行，并通过有限精度参数网格控制轨迹分布误差。论文给出的 e2e 学习器主要是统计存在性构造，不能据此推断有可直接实现的高效训练算法；所给章节未报告具体优化器、学习率、批大小或软件实现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 本文是理论 PAC 学习研究，没有使用真实或合成基准数据集，也没有报告训练集、验证集或测试集划分。其“样本”由未知提示分布与固定随机生成器共同产生：基础样本只观察一次伯努利下一令牌，CoT 样本观察长度为 $M$ 的完整随机轨迹，e2e 样本只观察该轨迹的最终令牌。
- 一般类分析覆盖任意随机生成器类 $\mathcal{F}$，并通过专门构造的有限类给出下界或紧致性实例。这些构造不是经验数据集，其作用是检验统一上界的尺度、倍率及适用边界。
- 逻辑斯蒂案例使用类 $\mathcal{F}_{\sigma}(d)$：同一个参数向量 $w\in\mathbb{R}^d$ 在每一步重复使用，根据当前字符串最后 $d$ 个二进制令牌计算下一令牌概率。该案例用于检验一般理论在一个典型、有限记忆且基础样本复杂度已知的函数类上能否得到统计与计算结论。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**平方损失下的 PAC 样本复杂度**

$m_{\rm base}$、$m_{\mathsf{CoT}}$ 或 $m_{\mathsf{e2e}}$ 表示以规定置信度把相应目标概率的期望平方误差控制到 $\varepsilon$ 所需的最少样本数；基础任务预测单步概率，CoT 与 e2e 任务预测第 $M$ 步最终令牌概率。 （越低越好，因为达到相同误差与置信度时需要的监督样本更少。）

</div>
<div class="metric-item" markdown="1">

**样本复杂度比率及渐近依赖**

比较 $m_{\mathsf{CoT}}/m_{\rm base}$、$m_{\mathsf{e2e}}/m_{\mathsf{CoT}}$，以及复杂度对 $M$、$d$、$1/\varepsilon$ 的增长，用于判断监督形式改变带来的统计代价。 （对学习器而言增长越慢越好；对下界而言，比率越大表示两种监督之间的分离越强。）

</div>
<div class="metric-item" markdown="1">

**计算效率与正常学习性**

检查算法是否为随机多项式时间，以及输出是否仍属于目标生成器类；对 $\mathcal{F}_{\sigma}(d)$，正常学习器必须输出具有多项式位数的有理向量 $\widehat{w}$。 （能够同时实现多项式时间和正常输出更强；仅有信息论样本上界并不代表存在可计算的高效学习器。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 任意随机生成器类 $\mathcal{F}$ 的基础监督到 CoT 监督比较，$M\geq 1$ 且 $0<\varepsilon<1$。

<div class="result-value" markdown="1">

定理 5.1 给出 $m_{\mathsf{CoT}}^{\mathcal{F},M}(\varepsilon)\leq m_{\rm base}^{\mathcal{F}}(\varepsilon/M^2)$。作者还构造有限类，使两者在相应尺度上都达到 $\Theta(LM^2/\varepsilon)$；并证明若把基础任务的精度放宽到 $\varepsilon^{1-\beta}/M^2$，基础复杂度可为 $0$，而 CoT 复杂度仍可达 $\Omega(K/\varepsilon)$。

</div>

技术上，这说明只要能把每一步概率学到更严格的 $\varepsilon/M^2$ 平方误差尺度，就足以控制长度为 $M$ 的最终概率误差；$M^2$ 来自多步误差传播。紧致性构造表明该精度尺度不能普遍地显著放宽。它不表示同一精度 $\varepsilon$ 下 CoT 总比基础学习容易，也不表示所有自然模型都会达到最坏的 $M^2$ 代价。

<div class="result-source" markdown="1">

来源：定理 5.1（informal）；表 1 总结

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For every class $\mathcal{F}$, every $M\geq 1$, and every $0<\varepsilon<1$, $m_{\mathsf{CoT}}^{\mathcal{F},M}(\varepsilon)\leq m_{\rm base}^{\mathcal{F}}\left(\frac{\varepsilon}{M^{2}}\right)$.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 任意随机生成器类 $\mathcal{F}$ 的 CoT 到 e2e 比较，$M\geq 2$ 且 $0<\varepsilon<1$。

<div class="result-value" markdown="1">

定理 6.3 证明 $m_{\mathsf{e2e}}^{\mathcal{F},M}(\varepsilon)\leq\widetilde{O}(M(1\vee m_{\mathsf{CoT}}^{\mathcal{F},M}(c\varepsilon))/\varepsilon)$。相应有限类满足 $m_{\mathsf{e2e}}=\Theta((M/\varepsilon)m_{\mathsf{CoT}}(\rho\varepsilon))=\Theta(NM/\varepsilon)$，说明除对数因子与常数精度变化外，$M/\varepsilon$ 倍代价可被实现。

</div>

完整轨迹可在一个样本中暴露多个中间条件，而 e2e 样本只给最终二进制结果，因此最坏情况下需要额外约 $M/\varepsilon$ 倍样本。该结论是在 CoT 精度改为常数倍 $c\varepsilon$ 后成立，并包含 $1\vee m_{\mathsf{CoT}}$ 以处理 CoT 复杂度为零的退化情况。它是样本复杂度上界，不保证相应 e2e 学习器高效，也不表示每个具体类都遭受这一倍率。

<div class="result-source" markdown="1">

来源：定理 6.3（informal）；表 1 总结

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

There is a constant $c$ such that, for every class $\mathcal{F}$, $M\geq 2$, and $0<\varepsilon<1$, $m_{\mathsf{e2e}}^{\mathcal{F},M}(\varepsilon)\leq\widetilde{O}\left(\frac{M\left(1\vee m_{\mathsf{CoT}}^{\mathcal{F},M}(c\varepsilon)\right)}{\varepsilon}\right)$.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### $d$ 维逻辑斯蒂自回归类 $\mathcal{F}_{\sigma}(d)$，比较 CoT 与 e2e 的统计样本量及计算效率。

<div class="result-value" markdown="1">

e2e 存在非高效、非正常学习器，其样本复杂度至多为 $\widetilde{O}((d^2\log M+\log(1/\delta))/\varepsilon)$；CoT 则以相同阶样本量实现随机多项式时间正常学习。另一方面，在 LPN 预测假设下，当 $M\leq d$ 时，不存在对所有该类实例都有效的 e2e 随机多项式时间正常学习器。

</div>

统计上，两种监督都只需关于记忆维数 $d$ 的多项式样本和关于轨迹长度 $M$ 的对数依赖；计算上，完整中间轨迹使参数类内的高效学习成为可能，而只看最终令牌会隐藏可归约为带噪奇偶校验的困难结构。该结论没有排除高效的非正常 e2e 学习器，也不是无条件复杂性下界；其困难性依赖 LPN 假设且针对正常学习。

<div class="result-source" markdown="1">

来源：定理 8.1、定理 8.2、定理 8.3（informal）；表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Assume the LPN prediction assumption holds. Then no proper randomized polynomial-time algorithm can learn $\mathcal{F}_{\sigma}(d)$ with $\mathsf{e2e}$ supervision for all horizons $M\leq d$.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 论文结果主要是分布无关、可实现条件下的最坏情形样本复杂度定理，没有真实语言数据、有限样本曲线或算法运行时间实验；专门构造的有限类证明边界可达，却不能说明自然数据或现代大模型通常会达到这些最坏情况。
- 逻辑斯蒂 e2e 的计算分离只排除 LPN 假设下的高效正常学习器，未排除高效非正常算法；此外，文中关于 $L_1$ 损失的对应结果明确属于作者预期而非已证明定理，KL 上界还可能要求单步概率远离 $0$ 和 $1$，因此不能把平方损失结论直接视为其他目标下的既成结果。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 基础单步学习 $m_{\rm base}^{\mathcal{F}}(\varepsilon)$：直接学习每个提示下的伯努利条件均值，是衡量完整 CoT 监督是否因误差沿 $M$ 步传播而需要更细精度的自然参照。
- 完整轨迹 CoT 学习 $m_{\mathsf{CoT}}^{\mathcal{F},M}(\varepsilon)$：训练时可见所有中间令牌，既是 e2e 学习的监督信息更强的参照，也是判断中间轨迹能否带来计算优势的核心比较对象。
- 仅最终令牌的 e2e 学习 $m_{\mathsf{e2e}}^{\mathcal{F},M}(\varepsilon)$：训练时隐藏中间状态，用于量化丢失轨迹信息造成的统计代价，并与 CoT 的高效正常学习能力比较。
- 胖打散维数 $\operatorname{fat}_{\mathcal{F}}(\gamma)$ 上界：这是随尺度 $\gamma$ 变化的实值函数类复杂度基线，用来检验基础类的尺度敏感容量是否足以控制 e2e 样本复杂度；论文明确指出不依赖精度的伪维数类指标在随机情形下可能失效。

**实验想回答的问题**

- 在平方损失精度为 $\varepsilon$、生成长度为 $M$ 时，基础单步监督、完整思维链（CoT）监督和仅观察最终令牌的端到端（e2e）监督，其样本复杂度之间是否存在对所有随机自回归生成器类都成立的比较关系？这些关系对精度尺度的调整是否必要且近乎最优？
- 对有限记忆的 $d$ 维逻辑斯蒂随机自回归生成器，CoT 与 e2e 监督能否同时获得关于 $d$ 和 $M$ 的多项式样本复杂度；进一步地，两种监督在高效且正常（proper）学习方面是否存在计算复杂性分离？

**实验实现**

论文没有执行常规经验实验，也未报告优化器、硬件、随机种子或数据划分。评估协议是可实现的分布无关 PAC 分析：固定生成器类 $\mathcal{F}$ 与轨迹长度 $M$，分别向学习器提供基础、CoT 或 e2e 样本，以目标概率的期望平方损失和失败概率 $\delta$ 定义样本复杂度。一般结论通过统一上界与专门有限类下界相互校验；$\widetilde{O}$ 隐去对数因子。逻辑斯蒂案例另外区分正常/非正常与高效/非高效算法，并以标准 LPN 预测假设给出条件计算下界。因此，下述“结果”应理解为定理保证和最坏情形构造，而不是基准数据上的平均测试分数。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 逻辑斯蒂有限记忆案例把抽象生成器具体化为 $p_{g_w}(s)=\sigma(\langle w,\operatorname{tail}_d(s)\rangle)$：每一步复用同一 $w$，只读取最近 $d$ 位。表 2 的关键对照是，CoT 可由高效正常算法以 $\widetilde{O}(d^2\log M/\varepsilon)$ 量级学习，而 e2e 的同阶保证仅由非高效、非正常算法取得，且高效正常版本在 LPN 假设下被排除。这一案例支持“中间轨迹主要可能带来计算信息，而不一定改善样本阶数”的解释，但不能外推为所有神经语言模型的经验结论。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Develops a theoretical sample-complexity framework comparing chain-of-thought, end-to-end, and next-token supervision in stochastic autoregressive learning.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`c148e3dc00b72babf3f1c34e617ae6ddf4d6ede669d76e610421104c9c860b07`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
