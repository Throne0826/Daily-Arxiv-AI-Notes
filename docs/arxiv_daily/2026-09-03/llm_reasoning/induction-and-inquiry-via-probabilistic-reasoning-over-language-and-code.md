---
title: "[论文解读] Induction and Inquiry via Probabilistic Reasoning over Language and Code"
description: "[arXiv 2609.01815][LLM Reasoning] 本文旨在解释人类如何从稀少、连续且带噪的经验中形成和修正抽象概念，并提出用大语言模型引导的贝叶斯推断在自然语言与源代码混合的“心理程序”空间中维持多个不确定假设。"
arxiv_id: "2609.01815"
announcement_date: "2026-09-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:31:49.801677+00:00"
source_sha256: "d45e98d05ea20ce18f4c64a659a8db723ee56b81e4bf02c7aadae83259e529b6"
tags:
  - "LLM Reasoning"
  - "归纳推理"
  - "主动探究"
  - "贝叶斯推理"
  - "心理程序"
  - "大语言模型"
  - "序贯学习"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.01815</p>

# Induction and Inquiry via Probabilistic Reasoning over Language and Code

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> Wasu Top Piriyakulkij, Sam Acquaviva, Cassidy Langenfeld, Joshua Tenenbaum, Kevin Ellis</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Cornell University；Affiliation: Massachusetts Institute of Technology * Equal ContributionCorrespondence to；Affiliation: Massachusetts Institute of Technology</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01815v1) · [PDF 下载](https://arxiv.org/pdf/2609.01815v1) · **关键词** 归纳推理, 主动探究, 贝叶斯推理, 心理程序, 大语言模型, 序贯学习<br>


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

本文旨在解释人类如何从稀少、连续且带噪的经验中形成和修正抽象概念，并提出用大语言模型引导的贝叶斯推断在自然语言与源代码混合的“心理程序”空间中维持多个不确定假设。

**不用术语来说**：人往往只看少量例子，就能猜测背后的规律；面对新证据时，还会修改原先的猜测，并主动提出最有助于辨别不同解释的问题。困难在于，一个认知模型既要容纳近乎无限的可能概念，又不能穷举所有解释；同时还必须保留“哪些解释更可信、目前有多不确定”的信息，才能决定下一步应询问或实验什么。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出一种统一的建模入口：将可学习的符号知识表示为混合自然语言与计算机源代码的“心理程序”，以兼顾语言表达的开放性和代码执行所提供的精确约束。
- 作者将大语言模型的自下而上提议能力与序贯贝叶斯学习结合，用少量持续更新的候选假设近似开放空间中的后验推断，从而把概念归纳与主动询问纳入同一个连续学习循环。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于认知科学与人工智能交叉的归纳推理研究领域。归纳推理关注人在少量、连续到达且可能含噪的经验中学习抽象概念，并在新证据出现后修正已有信念。当数据不足以唯一确定概念时，学习者需要在多个候选假设之间分配不同可信度，并通过提问或实验主动收集信息；因此，本文研究的是随时间展开的“归纳—探究”循环。理想模型需要同时满足三点：以较少数据和计算开销学习，表达从确定到不确定的信念差异，以及覆盖开放且多样的人类概念。本文将知识表示为结合自然语言与源代码的“心理程序”，再借助大语言模型引导的概率推理近似贝叶斯更新。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**归纳推理与主动探究**

归纳推理是从少量例子或观察结果概括出一个可能的概念或规则。主动探究则是在仍有不确定性时选择问题、实验或其他信息获取行动，以区分竞争性假设；二者构成随新数据持续循环的学习过程。

</div>
<div class="concept-item" markdown="1">

**贝叶斯推理**

贝叶斯推理根据先验可信度和新证据重新计算假设的后验可信度，因而能够表达“更可能”而非只有“正确或错误”。在本文中，它主要提供更新信念和选择有价值实验的概率规范，而不单独规定人类能够表示哪些概念。

</div>
<div class="concept-item" markdown="1">

**假设空间与心理程序**

假设空间是模型允许用来解释数据的全部候选假设；空间越开放，越能表达复杂概念，但通常也越难高效搜索。心理程序是本文对假设的表示方式，由自然语言片段和可执行或形式化的源代码组合而成，试图兼顾语言的灵活性与代码的结构化推理能力。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

在连续时间设置中，学习者接收关于某个未知概念或环境的稀疏、可能含噪的观察数据，并维护一组候选心理程序假设。每个假设都需要根据已有观察获得概率权重；当新观察到达时，模型应更新这些权重、修订不再适配证据的程序，并在需要时选择能够最大程度减少不确定性的提问或实验。输入包括历史观察、候选概念及可获得的查询或实验选项；输出包括对候选心理程序的概率信念，以及面向后续信息获取的行动选择。模型假设人类的信念更新近似贝叶斯式，但不要求直接枚举一个固定、封闭的逻辑假设空间；相反，候选假设可以由语言和代码共同表达，并由大语言模型帮助生成或修订。核心约束是在开放表示能力、概率一致性和在线计算效率之间取得平衡。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$h$**

一个候选心理程序假设，即用于解释观察数据的自然语言—源代码表示。

</div>
<div class="notation-item" markdown="1">

**$D_{1:t}$**

截至时间 $t$ 已经获得的全部观察数据；下标表示数据按时间顺序逐步到达。

</div>
<div class="notation-item" markdown="1">

**$p(h\mid D_{1:t})$**

给定截至时间 $t$ 的观察数据后，假设 $h$ 的后验概率，表示模型当前对该假设的相信程度。

</div>
<div class="notation-item" markdown="1">

**$a_t$**

时间 $t$ 的主动探究行动，例如提出问题或进行实验；该行动用于获得新的观察并减少不确定性。

</div>

</div>

**直接相关的工作**

- **Anderson (1990)；Griffiths et al. (2015)；Griffiths et al. (2024)**: 这些研究代表贝叶斯认知建模传统，支持用概率更新刻画人类归纳推理。本文继承其概率规范，但指出传统贝叶斯范式本身并未规定人类可以相信或表示哪些开放式概念，因此进一步研究如何在灵活假设空间中实现高效的在线归纳与探究。
- **Quilty-Dunn et al. (2023)；Piantadosi (2011)**: 这些工作从“思维语言”角度主张人类内部存在形式逻辑、符号图式、贝叶斯网络模板或概率程序等结构化表示，为本文的心理程序表示提供理论背景。本文与其不同之处在于不采用刚性的逻辑形式，而是把自然语言与源代码结合起来，以获得更大的表达弹性和更实际的推理载体。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

认知科学需要一个可计算的模型，说明人类如何在经验稀少、逐步到达且可能含噪时高效增长抽象知识。由于少量观察通常兼容多种规律，模型不仅要学习概念，还要量化不同解释的可信度，并据此选择能够消除歧义的问题或实验；因此，数据效率、计算效率、不确定性表达和概念表示的开放性必须同时满足。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **经典贝叶斯认知模型与形式化“思想语言”模型**：贝叶斯框架用先验与观测似然更新候选假设的后验可信度；相关“思想语言”模型进一步用形式逻辑、符号模式、贝叶斯网络模板或概率程序规定哪些假设可以被表示和学习。它们擅长保持概率一致性，并原则上可依据当前后验选择信息量高的实验。
- **纯大语言模型方法**：大语言模型依靠从大规模语料中学到的语言与代码模式，直接生成、解释或修订候选规律。其优势是能够处理自然语言描述和程序结构等开放表示，并可迅速提出与当前少量证据相符的假设，而无需显式枚举整个假设空间。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 经典贝叶斯方法本身只规定应如何更新信念，并不决定人能够表示哪些开放式概念；一旦采用更灵活的形式化假设空间，竞争解释数量便迅速增加，使在线枚举与更新计算昂贵。以往刚性的逻辑形式又不如自然语言可塑，也未把长期被讨论的自然语言假设表示正式转化为可计算模型。
- 纯大语言模型虽然具有表达和生成能力，却没有显式维护多个假设及其概率权重，因而难以保证新证据到来后信念更新的一致性，也缺少为主动询问计算渐进不确定性和优选实验的明确机制。作者进一步声称，纯大语言模型或经典贝叶斯模型在相关任务中会失败、不能复现人类行为，或只能以极高计算成本成功；但这些比较结论在给定节选中尚无实验细节支持。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种同时可处理开放式语言／程序假设、显式保留概率不确定性，并能在流式证据下以可承受计算量持续更新和选择询问的统一模型。换言之，表达能力强的方法缺少规范化概率推断，而概率推断严谨的方法又受制于预先固定的表示和组合爆炸。

</div>
<div markdown="1"><span>核心问题</span>

能否以自然语言和源代码混合的心理程序作为开放假设空间，并借助大语言模型引导的近似贝叶斯算法，在有限计算预算下统一模拟人类的序贯概念归纳、信念修正与主动询问，包括锚定和“花园路径”等行为特征？

</div>
<div markdown="1"><span>作者直觉</span>

语言适合提出宽泛、可变且接近人类表述的解释，代码则能把解释变成可执行、可检验的预测；大语言模型可利用已学到的模式，把搜索集中到少量看似合理的候选上。随后，贝叶斯机制按照候选解释全部观测的程度重新赋权，保留不确定性，并据此寻找最能区分候选的问题。直观上，这相当于不再穷举所有可能规律，而是让大语言模型负责“提出好猜想”，让概率推断负责“比较、修正并决定下一步问什么”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把人的抽象知识表示为“心理程序”$h$：每个假设同时包含自然语言描述与可执行的 Python 实现。给定按时间到达的证据序列$e_{1:T}$，语言描述的简洁程度决定先验$p(h)$，程序执行结果与观测的一致程度决定似然$p(e_t\mid h)$；二者共同定义随证据递推更新的后验$p(h\mid e_{1:T})$。由于语言与代码构成的假设空间近乎无限，方法不直接枚举全部程序，而是用大语言模型提出少量候选，再以贝叶斯权重抑制不符合证据的候选。

端到端上，模型采用 LLM 增强的序贯蒙特卡洛算法 LLM-SMC-S，在每个时间步维护$K$个候选假设粒子$\{h_t^i\}_{i=1}^K$。新证据到达后，LLM 在看到全部旧粒子和累计证据的条件下提出至多$K$个新候选，随后由先验与似然进行概率校正，得到新的近似后验；该后验既可用于预测新实例，也可通过最大化信息增益选择实验或自然语言问题。直观地说，LLM 负责快速“想点子”，代码负责把点子变成可检验规则，贝叶斯更新负责根据证据决定哪些点子应被保留，而粒子数量则刻画有限的认知或计算预算。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 接收序贯证据并建立当前推断状态

模型不把全部数据视为一次性批处理输入，而是在第$t$步保存对$p(h\mid e_{1:t})$的粒子近似，使证据顺序能够影响后续可被提出和保留的假设。

<div class="method-step__io" markdown="1">

**输入**：按顺序出现的观测$e_1,e_2,\ldots,e_t$；观测可为算法的输入—输出示例、类别正例，或实验及其反馈。<br>
**输出**：累计证据$e_{1:t}$以及当前候选集合$\{h_t^i\}_{i=1}^K$。

</div>

**直观理解**：模型像人一样逐条学习，而不是看完所有答案后重新解题；因此早期形成的解释可能产生锚定或花园路径效应。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 用 LLM 提出语言—代码心理程序

提示词实现提议分布$q(h_{t+1}\mid e_{1:t+1},\{h_t^i\}_{i=1}^K)$，从中生成$s$个候选，其中$s\leq K$；每个一般性候选包含自然语言规则及其 Python 实现。

<div class="method-step__io" markdown="1">

**输入**：新证据$e_{t+1}$、历史证据$e_{1:t}$和全部旧粒子$\{h_t^i\}_{i=1}^K$。<br>
**输出**：一组可能解释新旧证据的新心理程序$\{h_{t+1}^i\}$。

</div>

**直观理解**：LLM 相当于受经验驱动的联想机制，优先提出少量看起来有希望的规则，从而避免在无限多程序中盲目搜索。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 以先验和可执行似然校正候选

短而易描述的语言规则获得更高先验；程序运行结果越符合观测，似然越高。模型据此重加权并更新粒子集合，使其逼近目标后验$p(h\mid e_{1:t+1})$，而不是直接接受 LLM 的输出。

<div class="method-step__io" markdown="1">

**输入**：新提出的心理程序、语言先验$p(h)$以及各条证据对应的似然$p(e_t\mid h)$。<br>
**输出**：带有后验权重的更新后粒子集合，即当前信念分布的有限近似。

</div>

**直观理解**：一个想法即使语言上很流畅，只要代码执行后与数据冲突，就会被降权；这一步把“会生成解释”转化为“会用证据筛选解释”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 产生预测或主动选择查询

归纳任务对各粒子的预测按后验进行汇总；主动探究任务则比较候选实验或问题的预期信息增益，选择最能区分当前竞争假设的查询，并将反馈作为下一条证据继续循环。

<div class="method-step__io" markdown="1">

**输入**：更新后的假设后验，以及待预测对象、可执行实验或候选自然语言问题。<br>
**输出**：类别或函数预测，或者下一项实验$\xi$与自然语言问题。

</div>

**直观理解**：当多个规则都说得通时，模型不只猜答案，还会主动寻找一个能让这些规则给出不同结果的问题，以最快减少不确定性。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 心理程序的序贯贝叶斯更新

$$
p(h\mid e_{1:T})\propto p(e_T\mid h)\,p(h\mid e_{1:T-1})\propto p(h)\prod_{t\leq T}p(e_t\mid h)
$$

**符号说明**

- $h$：候选心理程序；通常同时含自然语言描述与 Python 实现。
- $e_t$：时间步$t$到达的一条观测证据。
- $e_{1:T}$：从第$1$步到第$T$步的完整有序证据序列。
- $p(h)$：心理程序的先验概率，偏好更短的自然语言描述。
- $p(e_t\mid h)$：假设$h$生成或解释证据$e_t$的似然，通常依据程序执行与观测的匹配程度确定。
- $p(h\mid e_{1:T})$：观察全部证据后对假设$h$的后验信念。
- $T$：当前已观察到的证据总数。

<div class="equation-explanation" markdown="1">

**直观理解**：新证据到达时，模型把旧后验乘以该证据在每个假设下的似然；展开后，这等价于用先验乘上所有证据似然。该公式规定了应逼近的理想概率分布，而 LLM-SMC-S 的作用是在无法枚举无限假设时，用少量粒子近似它。<br>
**原文位置**：第2节 Computational Model，公式（1）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该方法没有在论文所述任务上重新训练一个端到端神经网络，也未给出梯度优化损失；核心目标是在推断阶段近似贝叶斯后验$p(h\mid e_{1:T})$。预训练 LLM 仅作为数据驱动的提议机制$q$，其候选再由显式先验与似然重加权，因此 LLM 的生成概率不等同于最终信念。主动探究阶段以预期信息增益作为选择实验或问题的准则，但所给节选仅引用公式（2），未提供其完整数学表达，故不据此补写方程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 语言—代码混合心理程序**

一般情况下，假设$h$由自然语言描述和 Python 实现组成：语言允许开放式表达概念，代码则提供确定、可执行的证据匹配机制。论文也允许领域化退化形式，例如购物问答中假设是有限产品，$p(e\mid h)$由语言模型直接判断产品与问答是否相容，而不强制生成代码。

> 直观理解：自然语言擅长表达“可能是什么规律”，代码擅长检验“这个规律到底会输出什么”；混合表示兼顾表达范围与可验证性，但并不假定每个领域都必须同时使用二者。

**2. LLM 引导的 LLM-SMC-S**

算法在每一步维护$K$个粒子，并让提议分布访问全部旧粒子，而非仅从单个祖先粒子局部变异；每步只生成$s\leq K$个提议，再利用目标后验进行概率校正。它区别于一次性处理全部样本的重要性采样，因为粒子状态会随每条证据演化。

> 直观理解：标准穷举可能需要检查海量程序，而该模块让 LLM 根据当前所有主流解释集中搜索；保留序贯状态也使模型能够描述人类因证据顺序而产生的偏差。

**3. 后验预测与信息增益查询**

同一后验接口支持两类操作：对未知实例做后验预测，以及在候选实验$\xi$或问题中选择预期信息增益最大的项目。Zendo 中实验是由形状组成的构造，购物任务中实验是自然语言问题、证据$e$是问题—回答对。

> 直观理解：这一模块把归纳和探究连成闭环：先根据数据形成多个解释，再挑选最能区分解释的行动，最后用所得反馈修正信念。

**训练与推理**

推断开始时，模型依据最初证据生成有限个心理程序粒子；在第$t+1$条证据到达后，将$e_{1:t+1}$与全部现存粒子放入提示上下文，通过$q(h_{t+1}\mid e_{1:t+1},\{h_t^i\}_{i=1}^K)$提出$s$个候选。随后计算候选的语言先验和证据似然，重加权并更新为$K$粒子的后验近似，再进入下一时间步。该“提议—校正—继续观察”循环使模型既保留早期推断轨迹，又能在新证据下随机修订假设。

任务输出由同一粒子后验派生：列表函数任务执行候选程序并汇总预测；数字概念任务估计各数字属于概念的概率；Zendo 交替选择构造实验、接收二元反馈和更新假设，最后预测留出构造；购物任务则在有限产品假设空间中做精确贝叶斯更新，并让语言模型提供问答似然。后两类主动任务利用信息增益选择查询，使当前假设预计产生尽可能不同的反馈。

**复现信息**

公平理解该方法需要关注三项设置。第一，主要复杂度由粒子数$K$及每步提议数$s$控制，且$s\leq K$；它们既是计算预算，也被作者用作有限认知资源的模型。第二，数字概念的分心条件通过把 LLM-SMC-S 的粒子数从$70$降至$20$来模拟更高认知负荷；这是行为建模假设，而非网络结构变化。第三，LLM-SMC-S 的提议器能够在上下文中看到整个旧后验粒子集合，这是其偏离标准 SMC 的关键设计；作为对照的重要性采样则一次处理全部示例，不能表达相同的逐步路径依赖。作者明确选择普通 LLM 而非经过强监督后训练、倾向输出单一高奖励答案的推理模型，因为该算法需要生成多个彼此竞争且合理的假设。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 所给第4节摘录没有说明行为实验所用数据集、被试规模、任务材料、训练/测试划分或数据收集流程；摘要仅称评估覆盖“一系列行为研究”。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**期望信息增益**

对候选实验 $\xi$ 的可能结果 $e$ 求期望，计算观察该结果前后假设后验分布之间的KL散度；它衡量一次实验预计能使当前信念改变多少。该量在摘录中是实验选择目标，而不是与人类数据比较时的完整评估指标。 （越高越好，因为更高的期望KL散度表示候选实验预计能更大幅度减少关于假设 $h$ 的不确定性。）

</div>
<div class="metric-item" markdown="1">

**人类行为定量特征的复现程度**

摘要称模型复现了锚定、花园路径等人类归纳学习和主动询问现象，但所给材料未说明采用相关系数、似然、准确率还是其他拟合指标。 （原文未明确报告。）

</div>
<div class="metric-item" markdown="1">

**计算成本**

用于区分可处理的LLM引导粒子近似与代价高昂的经典贝叶斯推断；所给材料只作定性比较，没有报告运行时间、调用次数、粒子数或算力消耗。 （通常越低越好，但原文未在所给摘录中规定具体度量。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨多项行为研究的总体评估

<div class="result-value" markdown="1">

作者在摘要中声称，该模型能够复现人类归纳学习和主动询问的定量行为特征，包括锚定效应与花园路径效应；所给材料没有提供各任务的数值结果。

</div>

这意味着模型产生的顺序信念更新或询问选择在若干行为模式上与人类相似。它并不证明模型内部机制就是人类真实认知机制，也不能据此判断拟合幅度、统计显著性或跨任务泛化能力，因为相应表格和实验细节未提供。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across a range of behavioral studies this model successfully reproduces quantitative signatures of human inductive learning and active inquiry, such as anchoring, garden-pathing, and other effects.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 与纯LLM和经典贝叶斯模型的总体比较

<div class="result-value" markdown="1">

作者声称，纯LLM与经典贝叶斯模型至少存在以下一种问题：底层任务失败、不能复现人类行为，或只能以极高计算成本成功。摘录没有把这些问题分别对应到具体基线，也没有给出定量差距。

</div>

这一比较支持混合设计的必要性：LLM缩小搜索范围，贝叶斯更新表达不确定性，粒子近似控制计算量。但由于缺少逐基线结果、统一预算和显著性检验，不能判断优势主要来自语言模型、程序表示、贝叶斯目标还是更多计算资源。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, pure LLMs and classic Bayesian models either fail at the underlying task, or do not reproduce human behavior, or succeed only at exorbitant computational cost.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给第4节摘录主要描述主动实验选择算法，没有提供数据集、被试、具体基线配置、评估指标、数值结果、置信区间或显著性检验，因而无法核验摘要中的定量行为复现与计算成本优势。
- 候选实验由LLM生成，因此最终选择受候选集合覆盖率约束：即使信息增益评分准确，真正最优的实验若未被LLM提出也无法被选中。原文明确指出全实验空间最大化不可处理，但所给材料未报告候选生成质量或相关消融。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 纯大语言模型：用于检验仅依赖神经语言模型、而不显式维护概率假设分布时，能否完成任务并复现人类行为。摘要声称该类方法可能在底层任务上失败或不能复现人类行为，但摘录未给出具体模型、提示方式和结果。
- 经典贝叶斯模型：用于比较传统显式概率推断与本文“语言/代码假设表示、粒子近似、LLM引导搜索”的方案。摘要声称经典模型可能失败、不能复现人类行为，或需要极高计算成本；摘录未报告其假设空间、推断算法及计算预算。
- 精确期望信息增益计算：第4节将其视为原则上的决策标准而非可实际执行的基线，因为对完整假设空间和全部可能实验求期望不可处理；本文改用当前唯一粒子构成的有限假设集合，并让LLM提出有限候选实验。

**实验想回答的问题**

- 在已有观测序列 $e_{1:t}$ 下，模型能否利用粒子近似的概率信念选择预期信息增益最大的实验或问题，从而解释人类如何主动消除对假设 $h$ 的不确定性？
- 以大语言模型提出有限候选实验、再用贝叶斯信息增益评分，是否能在避免穷举无限实验空间的同时复现人类归纳学习与主动询问的行为特征？

**实验实现**

在每个顺序学习时刻，模型先以当前唯一粒子近似后验 $p(h\mid e_{1:t})$。由于无法枚举无限多可能实验，LLM负责提出有限候选集合；对每个候选实验 $\xi$，模型再用粒子近似预测结果分布 $p(e\mid\xi,e_{1:t})$，并估计观察结果后得到的后验 $p(h\mid e_{1:t},e)$。候选实验按预期KL散度评分，最终选择得分最高者。所给摘录未报告LLM型号、提示模板、候选实验数量、粒子数量、重复运行次数、被试设置或统计检验，因此无法复原完整评估协议。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 锚定与花园路径被摘要列为模型能够复现的代表性行为现象。前者通常表示早期信息对后续判断产生持续影响，后者表示早期形成的假设会使学习者在后续证据到来时暂时沿错误解释更新；但摘录没有给出具体刺激、模型轨迹、人类对照曲线或单案例图，因此只能将其视为作者的总体结论。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出结合语言与代码程序表示、LLM引导贝叶斯学习的概率推理模型，核心贡献是模拟归纳学习与主动探究中的推理过程。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`d45e98d05ea20ce18f4c64a659a8db723ee56b81e4bf02c7aadae83259e529b6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
