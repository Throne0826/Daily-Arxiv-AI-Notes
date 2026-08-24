---
title: "[论文解读] Self-Speculation for Faster Reasoning Models"
description: "[arXiv 2608.20359][LLM 效率] 原文未明确报告。"
arxiv_id: "2608.20359"
announcement_date: "2026-08-24"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-24T02:10:28.939909+00:00"
source_sha256: "43c82e3328183f1061187faeb49af9ed5c652274ddde6a9a867a009eacc7d6c2"
tags:
  - "LLM 效率"
  - "LLM Reasoning"
  - "LLM 其他"
  - "推理型大语言模型"
  - "思维链（CoT）"
  - "推测解码"
  - "自推测"
  - "后缀解码"
  - "生成延迟"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.20359</p>

# Self-Speculation for Faster Reasoning Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Ravisri Valluri, Tung Nguyen, Aditya Grover</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of California, Los Angeles</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20359v1) · [PDF 下载](https://arxiv.org/pdf/2608.20359v1) · **关键词** 推理型大语言模型, 思维链（CoT）, 推测解码, 自推测, 后缀解码, 生成延迟<br>
**代码**: [https://github.com/Ravi-VK/SSR/](https://github.com/Ravi-VK/SSR/)

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

本文位于推理型大语言模型与推测解码的交叉领域。推理型模型先生成较长的思维链（Chain-of-Thought，CoT），再依据该推理过程生成最终答案；这种设计有助于规划、编程和多步决策，但会增加端到端生成延迟。推测解码则让一个较廉价的草稿分布先提出多个候选词元，再由目标分布并行验证，从而减少逐词串行解码的次数。本文关注的特殊场景是：同一个推理模型在不同推理预算下产生的答案分布可以分别充当草稿器和验证器，因而无需额外草稿模型或训练新的模型组件。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**推理型语言模型与思维链（CoT）**

模型先根据用户输入生成推理轨迹 $r$，直到结束思考标记，再生成最终答案 $a$。推理预算越大，通常意味着允许模型生成更多思维链词元；部分思维链虽然尚未完成，但已经能够诱导出有意义的中间答案分布。

</div>
<div class="concept-item" markdown="1">

**自回归生成与推测解码**

自回归模型按从左到右的顺序生成词元，每一步都依赖此前已经生成的内容。推测解码先由草稿分布提出一段候选序列，再由目标分布一次性验证；若候选与目标分布足够一致，就能批量接受多个词元，减少串行步骤。

</div>
<div class="concept-item" markdown="1">

**后缀解码**

后缀解码把提示词或历史生成内容中的后缀存入缓存，并查找与当前上下文匹配的后续文本作为候选。它不要求候选带有完整的草稿概率，因此通常采用近似的贪心验证，特别适合代码编辑或其他具有较高词法重复度的任务。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定用户输入 $q$ 和一个带有推理过程的语言模型，模型先生成推理轨迹 $r$，再生成最终答案序列 $a=(a_1,ots,a_l)$。若指定推理预算 $b$，则以 $p_{\theta}(a\mid q,b)$ 表示模型在仅使用前 $b$ 个推理词元 $r_{\leq b}$ 后生成答案的分布；完整推理过程对应较大的或完整的预算，并作为更可靠的目标分布。本文的目标是在不改变最终输出分布或答案质量的前提下，降低答案生成的总延迟：较低预算的部分-CoT分布提出草稿，完整-CoT分布验证草稿。系统还假设部分推理越接近完成，其答案与完整预算答案在语义和词面上越可能重叠；对于连续前缀未能完全匹配但后续仍有重叠的情形，后缀缓存可恢复被标准前缀验证丢弃的文本片段。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$q$**

用户输入或问题。

</div>
<div class="notation-item" markdown="1">

**$r$**

模型生成的推理轨迹，即思维链；$r_{\leq b}$ 表示其前 $b$ 个词元。

</div>
<div class="notation-item" markdown="1">

**$a$**

最终答案序列；$a_t$ 表示答案中的第 $t$ 个词元，$a_{<t}$ 表示其之前的词元。

</div>
<div class="notation-item" markdown="1">

**$p_{\theta}(a\mid q,b)$**

参数为 $\theta$ 的模型在输入 $q$ 和推理预算 $b$ 条件下生成答案 $a$ 的概率分布；预算省略了对部分推理轨迹 $r_{\leq b}$ 的显式书写。

</div>

</div>

**直接相关的工作**

- **标准推测解码（Leviathan et al., 2023；Chen et al., 2023）**: 标准方法使用独立草稿模型分布 $d$ 提出多个未来词元，再由目标模型分布 $p$ 验证。它建立了本文的基本加速框架，但独立草稿模型需要额外训练、显存和推理开销；SSR改为使用同一模型在较低推理预算下诱导出的部分-CoT答案分布作为草稿器。
- **后缀解码（Oliaro et al., 2024）**: 后缀解码从提示词和历史生成文本建立后缀缓存，并利用匹配后缀提出候选，适用于具有词法重复的任务。SSR将这一思想接到部分-CoT草稿之后：在连续前缀首次不匹配后，继续从草稿中寻找可能匹配的后续片段，以弥补标准前缀验证过早停止的损失。

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

SSR（Self-Speculation for Reasoning Models）是一种无需训练的自推测解码方法。给定用户问题 $q$、同一个推理模型 $p_{\theta}$、较小的草稿推理预算 $b_d$ 和较大的验证推理预算 $b_v$（满足 $b_d<b_v$），方法先在部分思维链 $r_{\leq b_d}$ 条件下生成答案草稿，再在更充分的思维链 $r_{\leq b_v}$ 条件下验证草稿；被验证接受的草稿前缀直接保留，其余答案由高预算分布继续生成。由于草稿生成与后续推理并行，草稿延迟可以被较长的思维链计算部分隐藏；随后，方法还把草稿放入后缀缓存，用于找回接受前缀之外仍然匹配的答案片段。

技术上，SSR把同一个模型在两个推理预算下得到的条件分布分别充当草稿分布和目标分布，而不是额外训练一个小型草稿模型。直观地说，模型先用“想了一部分”的状态猜答案，同时继续“想得更充分”；当完整推理完成后，用后者检查前者，正确且一致的部分无需重新逐词生成。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 生成并记录部分与完整推理状态

模型逐词采样思维链 $r$，达到 $b_d$ 时保存部分推理 $r_d=r_{\leq b_d}$，继续采样直到达到 $b_v$，得到验证推理 $r_v=r_{\leq b_v}$。实际提示中会追加模型所需的结束思考标记，以及某些模型需要的预算强制前缀。

<div class="method-step__io" markdown="1">

**输入**：用户问题 $q$、模型 $p_{\theta}$、草稿预算 $b_d$、验证预算 $b_v$。<br>
**输出**：部分推理状态 $r_d$ 和较高预算的验证状态 $r_v$。

</div>

**直观理解**：这相当于在同一场思考中设置两个检查点：较早的检查点用于先猜答案，较晚的检查点用于形成更可靠的最终判断。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 并行生成答案草稿

在推理达到 $b_d$ 后，启动草稿请求，从 $p_{\theta}(a\mid q,b_d)$ 中逐词采样草稿 $\hat{a}=(\hat{a}_1,\ldots,\hat{a}_m)$；与此同时，父请求继续从 $r_d$ 推进至 $r_v$。为了让草稿在验证前完成，需要总推理长度满足 $|r|>b_d+m$；否则草稿生成可能延迟验证。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、部分推理 $r_d$ 和模型 $p_{\theta}$。<br>
**输出**：答案草稿 $\hat{a}$，并由其构建后缀缓存 $C$。

</div>

**直观理解**：模型不是等全部思考结束后才开始写答案，而是在继续思考时先写一份草稿；只要思考足够长，写草稿的时间就能隐藏在思考时间里。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 用高预算分布验证草稿前缀

将 $p_{\theta}(\cdot\mid q,r_d)$ 作为提议分布，将 $p_{\theta}(\cdot\mid q,r_v)$ 作为目标分布，执行标准推测解码验证。草稿词元按顺序接受，直到首次拒绝；接受长度记为 $k_{\mathrm{acc}}$，拒绝时按照目标分布相对于提议分布的残余分布采样，以保持目标模型的输出分布。

<div class="method-step__io" markdown="1">

**输入**：草稿 $\hat{a}$、问题 $q$、草稿推理 $r_d$、验证推理 $r_v$。<br>
**输出**：最长接受前缀 $\hat{a}_{1:k_{\mathrm{acc}}}$，以及从该前缀继续生成的起点。

</div>

**直观理解**：高预算状态像校对者逐项检查早期草稿；连续正确的开头可以整段通过，而不是重新一个词一个词写。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 继续生成并利用后缀缓存

首先在验证分布 $p_{\theta}(\cdot\mid q,r_v,\hat{a}_{1:k_{\mathrm{acc}}})$ 下生成剩余答案；同时以草稿词元的所有后缀更新缓存，并在当前上下文中查找匹配后缀。候选片段由验证模型贪婪检查，匹配的片段可一次前进多个词元，直到答案结束。

<div class="method-step__io" markdown="1">

**输入**：验证推理 $r_v$、已接受前缀 $\hat{a}_{1:k_{\mathrm{acc}}}$ 和后缀缓存 $C$。<br>
**输出**：最终输出 $\mathrm{concat}(r_v,\hat{a}_{1:k_{\mathrm{acc}}},a_{\mathrm{cont}})$，其中 $a_{\mathrm{cont}}$ 是接受前缀后的连续答案。

</div>

**直观理解**：即使草稿开头有小差异，后面较长的句子仍可能相同；后缀缓存像“可复用短语库”，能把这些后来重新出现的片段整段取出并检查。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 自回归输出概率

$$
p_{\theta}(o\mid q)=\prod_{t=1}^{l}p_{\theta}(o_t\mid x,o_{<t})
$$

**符号说明**

- $p_{\theta}(o\mid q)$：参数为 $\theta$ 的语言模型在用户输入 $q$ 下生成输出序列 $o$ 的概率。
- $o=(o_1,\ldots,o_l)$：长度为 $l$ 的输出词元序列。
- $o_t$：序列在位置 $t$ 的当前词元。
- $o_{<t}$：位置 $t$ 之前已经生成的全部词元。
- $x$：模型在该位置可见的条件输入；在本文推理模型中包括问题及相应推理上下文。
- $\theta$：语言模型的参数。

<div class="equation-explanation" markdown="1">

**直观理解**：模型把整段答案的概率拆成每一步在已有上下文下生成下一个词元的概率乘积。SSR正是利用同一乘积式模型在不同思考前缀下产生两个不同的条件分布。<br>
**原文位置**：第3.1节“Autoregressive reasoning language models”

</div>

</div>

<div class="equation-block" markdown="1">

#### 推测解码的接受概率与残余采样

$$
\alpha_t=\min\left(1,\frac{p(\hat{a}_t\mid q,r,a_{<t})}{d(\hat{a}_t\mid q,r,a_{<t})}\right),\qquad a_t\sim\frac{\max(p-d,0)}{\sum_v\max(p(v)-d(v),0)}
$$

**符号说明**

- $\alpha_t$：第 $t$ 个草稿词元被接受的概率。
- $\hat{a}_t$：草稿在第 $t$ 个位置提出的词元。
- $p(\cdot\mid q,r,a_{<t})$：目标模型在问题 $q$、推理上下文 $r$ 和已接受答案前缀 $a_{<t}$ 下的词元分布。
- $d(\cdot\mid q,r,a_{<t})$：草稿模型或草稿分支在相同上下文下的提议分布；在SSR中由低预算分布提供。
- $a_t$：验证拒绝后重新采样得到的第 $t$ 个答案词元。
- $v$：词元词表中的遍历变量。

<div class="equation-explanation" markdown="1">

**直观理解**：如果目标模型认为草稿词元至少同样可信，它就以概率 $1$ 接受；若目标模型认为它不够可信，接受概率会下降。拒绝后使用 $p-d$ 的正部分进行补采样，可以补回草稿分布没有覆盖、但目标模型更支持的选择，从而使精确版本的最终分布与目标模型一致。<br>
**原文位置**：第3.2节“Speculative decoding”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文方法是训练无关的推理加速方法，不提出新的参数优化目标、损失函数或微调阶段。模型参数 $\theta$ 保持不变，SSR只在推理时改变条件上下文和调度方式：低预算分布提出草稿，高预算分布进行验证；因此不能把接受率或延迟改善理解为训练目标直接优化的结果。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双预算自推测模块**

SSR不引入独立草稿模型，而是使用同一模型在两个思维链预算下的分布：$d(a)=p_{\theta}(a\mid q,b_d)$ 负责提出草稿，$p(a)=p_{\theta}(a\mid q,b_v)$ 负责验证，其中 $b_d<b_v$。该设计依赖一个经验性结构假设：部分推理达到较充分阶段后，草稿答案与高预算答案在语义和词面上具有较高重合度；但若 $b_d$ 过小，部分推理可能尚未收敛，草稿在高不确定性任务上会偏离最终答案。

> 直观理解：它不是训练一个更小、更快的模型，而是让同一个模型用较少思考先预测、用较多思考再核验，因此省下的是串行等待时间，而不是模型总计算量。

**2. 标准推测验证模块**

草稿先提出多个词元，目标分布逐位置计算接受概率。接受后保留最长连续前缀；若出现拒绝，则从目标分布与草稿分布之差形成的残余分布采样替代词元，从而在理论上保证最终样本仍服从目标分布。论文同时指出，工程实践中简单地在拒绝处直接从目标分布重采样，是常见但近似的实现。

> 直观理解：草稿只负责提高一次检查能跳过的词数，最终决定权仍在高预算模型手中；草稿质量越好，单次检查通常能接受越长的连续文本。

**3. 后缀解码与服务调度模块**

后缀解码不需要草稿概率，而是把草稿及已有上下文的后缀索引到缓存 $C$ 中，在继续生成时检索匹配上下文的候选片段，并与验证模型的贪婪预测逐词比较。服务端通过调度器复制原请求：父请求继续高预算推理，子请求从共享前缀开始草稿生成；vLLM 前缀缓存复用已计算的提示和部分思维链。该过程会增加重叠窗口内的瞬时批量和额外计算，因此加速来自隐藏草稿延迟，而非降低总 FLOPs。

> 直观理解：父请求像主线工作，子请求像并行助手；两者共享已经读过的内容。后缀缓存则进一步利用草稿中后来仍可能有用的句段，避免只依赖从开头开始的连续匹配。

**训练与推理**

训练阶段：原文未报告SSR需要额外训练、蒸馏或参数更新；方法直接使用已有推理模型 $p_{\theta}$。推理阶段先从问题 $q$ 生成思维链至 $b_d$，保存 $r_d$；随后并行生成草稿 $\hat{a}$ 和继续思考至 $b_v$ 的父请求，收集完整的 $r_v$ 后执行标准推测验证，保留接受前缀并在验证分布下继续生成；最后可使用由草稿构建的后缀缓存 $C$ 加速剩余答案。

论文还描述了多阶段变体：给定 $b_1<b_2<\cdots<b_T$，在各阶段用较低预算输出作为草稿、用下一预算验证和扩展，逐步复用中间结果。该变体的目的不是改变模型分布，而是降低单次选择草稿预算的脆弱性；当早期草稿较短或不充分时，后续阶段仍可更新草稿。

**复现信息**

服务端实现把达到草稿预算的原请求复制为子请求。子请求复用父请求已有的提示和部分思维链前缀，通过 vLLM 前缀缓存避免重复计算，然后追加模型特定的结束思考标记并生成草稿；父请求继续较高预算的思维链。草稿完成后，调度器更新后缀缓存并发起验证请求，验证请求在最终推理前缀后接入草稿词元，比较目标模型和草稿的对数概率，按标准规则确定接受前缀；随后由连续生成请求完成答案。

复现或公平解读时需要注意三点：第一，SSR的收益依赖草稿生成能否在验证推理结束前完成，即总推理长度应覆盖草稿预算与草稿长度；第二，草稿预算过小会降低答案重合度，过大则减少可隐藏的并行时间，因此需要按任务或采用多阶段策略选择；第三，后缀解码是基于贪婪匹配的近似加速，不具备带概率草稿分布的精确拒绝采样保证。服务期间父、子请求会并行运行并造成额外瞬时计算，所以应以端到端延迟而非总 FLOPs 单独判断实际收益。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LongProc 2K：包含多种长结构化生成子任务，实验聚焦于 countdown、html_to_tsv、path_traversal、pseudo_to_code 和 tom_tracking；2K 版本目标输出约为 2K tokens，用于测试长答案和复杂结构下的加速效果。表 1 报告样本数为 $n=989$，但原文未明确报告训练集、验证集或测试集划分。
- ClassEval：面向类级代码生成，程序通常比函数级补全更长，因此用于测试较长、结构化代码答案中的草稿复用。表 1 报告样本数为 $n=100$，但原文未明确报告数据划分。
- HumanEval：面向函数级代码补全，答案相对较短，用于检验当回答阶段较短、CoT 生成占主要延迟时 SSR 是否仍然有效。表 1 报告样本数为 $n=164$，但原文未明确报告数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**端到端加速比（speedup）**

定义为基线总延迟除以 SSR 总延迟，即衡量同一请求完成生成的整体加速程度。 （越高越好，因为表示 SSR 相对于基线需要的时间更少。）

</div>
<div class="metric-item" markdown="1">

**延迟降低比例（Improvement）**

根据平均样本加速比计算为 $100\cdot(1-1/\mathrm{speedup})$，表示相对基线减少的总生成延迟百分比。 （越高越好；它是延迟节省比例，不等同于生成质量提升。）

</div>
<div class="metric-item" markdown="1">

**接受 token 数（Prefix tok. 与 Suffix tok.）**

Prefix tok. 衡量前缀验证接受的连续草稿 token 数，Suffix tok. 衡量后缀解码复用的草稿 token 数，用于判断加速来自哪一种复用路径。 （通常越高越有利于降低延迟，但数量本身不保证端到端加速，因为草稿、验证和缓存操作仍有开销。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Gemma-4-E4B-it 在 ClassEval 上使用前缀验证与后缀解码

<div class="result-value" markdown="1">

SSR 总延迟为 59.9 秒，Base 为 79.2 秒，延迟降低 24.1%；平均接受前缀为 238.9 tokens，接受后缀为 637.8 tokens。

</div>

这是表中最强的端到端结果，说明在较长的类级代码答案中，草稿与最终答案有足够重叠，后缀复用能够显著减少继续生成的工作。它只证明延迟优势，不证明生成质量、代码正确率或所有任务上的普适优势；原文未报告这些延迟结果对应的质量指标。

<div class="result-source" markdown="1">

来源：表 1，Main latency results across benchmarks and 4B-class models

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Gemma-4-E4B-it | ClassEval | 100 | 24.1% | 59.9 | 79.2 | 238.9 | 637.8

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3.5-4B 在 LongProc 2K、ClassEval 与 HumanEval 上使用完整 SSR

<div class="result-value" markdown="1">

LongProc 2K 的 SSR/Base 延迟为 68.9/72.8 秒，延迟降低 9.1%；ClassEval 为 72.8/85.3 秒，降低 18.5%；HumanEval 为 25.2/26.4 秒，降低 2.9%。

</div>

同一模型在 ClassEval 上收益明显高于 HumanEval，符合方法依赖长答案和词法重叠的预期；HumanEval 的短函数补全中，CoT 生成占比较大，能够被复用的答案 continuation 较少，因此端到端收益受限。该结果支持任务长度影响加速幅度，但不能单独证明长度是唯一原因，因为不同基准的结构和内容也不同。

<div class="result-source" markdown="1">

来源：表 1；第 5.2 节 Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen3.5-4B | LongProc 2K | 989 | 9.1% | 68.9 | 72.8 | 97.2 | 529.6
Qwen3.5-4B | ClassEval | 100 | 18.5% | 72.8 | 85.3 | 275.1 | 674.4
Qwen3.5-4B | HumanEval | 164 | 2.9% | 25.2 | 26.4 | 56.8 | 88.6

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 阶段性延迟与并发草稿开销的分析

<div class="result-value" markdown="1">

在 ClassEval 上，Qwen3.5-4B 的 CoT、Draft、Verify、Continuation 分别为 38.8、11.7、0.24、33.8 秒，SSR 总延迟为 72.8 秒，Base 为 85.3 秒；Gemma-4-E4B-it 的对应 SSR/Base 总延迟为 59.9/79.2 秒。并发草稿期间，Qwen3.5-4B 在 ClassEval 的 CoT throughput 变化为 -5.4%，草稿活跃时间占比为 29.5%；Gemma-4-E4B-it 的变化为 -0.0%，占比为 30.9%。

</div>

草稿生成本身需要约 8--12 秒，但与 CoT 生成并发，因此不会简单地全部加到总延迟上；验证阶段仅约 0.07--0.24 秒，主要剩余成本在继续生成。结果说明 SSR 的关键成立条件是并发能够隐藏草稿成本，且接受或复用的 token 足以抵消额外资源占用；它也显示硬件调度和模型实现会影响收益。

<div class="result-source" markdown="1">

来源：表 3、表 4；第 5.2 节 Stagewise latency breakdown

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen3.5-4B | ClassEval | 38.8 | 11.7 | 0.24 | 33.8 | 72.8 | 85.3
Qwen3.5-4B | ClassEval | 100 | 40.20 | 38.03 | -5.4% | 29.5%

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验范围较窄：只评估两个 4B 级开源推理模型和三个基准，且主要集中于代码与长结构化生成；原文未报告更大模型、其他任务类型、不同硬件或不同 batch size 下的结果，因此不能据此断言 SSR 对一般生成任务都有效。
- 收益依赖草稿与最终答案的重叠程度以及答案 continuation 长度。原文未报告 token 接受率分布、输出质量或统计显著性，也未明确报告重复实验和置信区间；因此延迟结果的稳定性、质量是否完全保持，以及低重叠样本上的失败比例仍需进一步验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 朴素自回归生成（Base）：使用与 SSR 相同的模型和采样设置，直接逐 token 生成完整 CoT 与答案，是端到端延迟的主要比较基线。
- 同 token 重放基线（same-token replay）：在表 2 中作为速度比参照，用于衡量前缀验证或后缀解码相对于简单重放相同数量 token 的收益；原文未进一步说明其具体实现。
- 仅前缀验证（Prefix-only）：只保留草稿与最终答案连续匹配的前缀，不使用后缀缓存复用，用于隔离前缀验证机制的贡献。
- 仅后缀解码（Suffix-only）：不接受连续前缀，而使用草稿建立后缀缓存并复用匹配片段，用于检验非连续词法重叠是否能独立带来收益。

**实验想回答的问题**

- 在长程、结构化生成任务中，SSR 是否能相较于同模型的朴素自回归生成降低端到端延迟，并且这种收益是否因答案长度和结构而变化？
- 前缀验证、后缀解码以及并发草稿等机制分别贡献多少收益，其额外计算开销是否会抵消延迟降低？

**实验实现**

实验采用端到端生成协议：请求先生成不超过最大推理预算的 CoT；推理过程中，SSR 从较低预算前缀启动答案草稿，在较高预算上下文下验证草稿，随后从接受的前缀继续生成，并可把草稿作为额外后缀缓存源执行后缀解码。所有延迟比较均使用相同模型和采样设置，并以朴素自回归生成作为主要基线。模型为可在单 GPU 部署的 Qwen3.5-4B 与 Gemma-4-E4B-it。延迟实验运行于一台含 10 张 NVIDIA RTX A6000 的机器，每张 GPU 使用一个 vLLM worker，batch size 为 1；4B 模型不使用张量并行。原文未明确报告随机种子、重复运行次数、置信区间以及各数据集的训练/验证/测试划分。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Gemma-4-E4B-it 在 ClassEval 上比较仅前缀、仅后缀和两者结合 | 仅前缀的速度比为 1.086，接受前缀 235.7 tokens、后缀 0.0 tokens；仅后缀的速度比为 1.318，接受前缀 0.0 tokens、后缀 867.8 tokens；两者结合的速度比为 1.318，接受前缀 238.9 tokens、后缀 637.8 tokens。 | 该消融分别关闭两种复用路径，直接测试各组件是否必要。仅前缀对应约 7.9% 延迟降低，而仅后缀达到约 24.1%，表明非连续后缀重叠在该任务上比连续前缀更有价值；结合方案没有超过仅后缀的速度比，说明组件的 token 接受量不能简单相加，二者可能复用相同内容或受缓存和继续生成开销限制。 | 表 2，Ablation of prefix verification and suffix decoding on ClassEval<br><span class="experiment-evidence">Gemma-4-E4B-it \| ClassEval \| ✓ \| – \| 100 \| 1.086 \| 235.7 \| 0.0
Gemma-4-E4B-it \| ClassEval \| – \| ✓ \| 100 \| 1.318 \| 0.0 \| 867.8
Gemma-4-E4B-it \| ClassEval \| ✓ \| ✓ \| 100 \| 1.318 \| 238.9 \| 637.8</span> |
| Gemma-4-E4B-it 在 ClassEval 上比较多次草稿生成与迭代式 SSR | 当 $i=750,m=500$ 时，多次草稿的 draft wall time 为 18.58 秒，迭代式 SSR 为 16.37 秒，降低 11.9%；当 $i=500,m=250$ 时，两者分别为 17.75 秒和 17.16 秒，降低 3.3%。 | 这里隔离的是草稿调度策略，而不是最终答案质量：$i$ 表示草稿间隔，$m$ 表示最大草稿长度。迭代式 SSR 在较长间隔下减少草稿子请求的墙钟生命周期更多，说明较晚生成的草稿更可能贴近最终答案，从而更快完成；但这只报告草稿请求时间，没有给出对应端到端总延迟或质量变化。 | 表 5；第 5.2 节 Iterative SSR overhead<br><span class="experiment-evidence">Gemma-4-E4B-it \| ClassEval \| i=750, m=500 \| 18.58 s \| 16.37 s \| 11.9%
Gemma-4-E4B-it \| ClassEval \| i=500, m=250 \| 17.75 s \| 17.16 s \| 3.3%</span> |

**定性案例**

- 图 2 展示了一个代码生成示例：草稿与最终输出的连续前缀先被验证接受，首次不匹配后的部分继续常规生成，同时草稿中与最终代码相同的后缀片段被重新利用。图中以 CalendarUtil 类和事件字典为例，直观说明 SSR 不只复用开头，还能找回前缀验证失败位置之后的有用代码片段；但该图是机制示意，不是定量质量比较。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work proposes a speculative-decoding method that accelerates long chain-of-thought generation by exploiting partial reasoning traces as drafts and full reasoning as verification.; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`43c82e3328183f1061187faeb49af9ed5c652274ddde6a9a867a009eacc7d6c2`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
