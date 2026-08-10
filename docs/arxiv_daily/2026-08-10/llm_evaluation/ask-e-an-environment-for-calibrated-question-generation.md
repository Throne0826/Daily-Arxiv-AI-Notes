---
title: "[论文解读] Ask-E: An Environment for Calibrated Question Generation"
description: "[arXiv 2608.06933][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.06933"
announcement_date: "2026-08-10"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-10T02:38:43.903848+00:00"
source_sha256: "56f7e6a45cfc3c81d6b6ea7a66ce2d2e0b4e4c583730ddba5f5f342606b07572"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "语言模型评测"
  - "校准问题生成"
  - "问题难度"
  - "数学推理"
  - "强化学习"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.06933</p>

# Ask-E: An Environment for Calibrated Question Generation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Sarah Pratt, Jae Sung Park, Scott Geng, Ali Farhadi</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Washington；Allen Institute for AI</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.06933v1) · [PDF 下载](https://arxiv.org/pdf/2608.06933v1) · **关键词** 语言模型评测, 校准问题生成, 问题难度, 数学推理, 强化学习<br>
**代码**: [https://github.com/sarahpratt/aske](https://github.com/sarahpratt/aske)

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

本文位于语言模型评测与训练交叉领域，关注模型能否生成具有精确难度的问题，而不只是回答已有问题。传统方法通常通过问题回答正确率衡量模型能力，但评测和训练需要持续获得处于模型能力前沿的问题：过易的问题无法区分强模型，过难的问题则使所有模型失败。Ask-E将问题生成视为一种能力评测任务：给定两个能力不同的语言模型作为边界求解器，要求被测模型生成一道恰好能被其中一个求解器解决的问题，从而判断其是否理解了两者之间的能力差距。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**语言模型求解器与提问者**

求解器是负责回答问题的语言模型，提问者是负责设计问题的语言模型。本文评估的重点从“能否答对”转向“能否写出能区分两个求解器的问题”。

</div>
<div class="concept-item" markdown="1">

**能力校准**

能力校准指生成的问题难度与预定目标范围相匹配。本文中，若较弱边界模型答错而较强边界模型答对，则问题被视为处于两者能力之间。

</div>
<div class="concept-item" markdown="1">

**边界求解器**

边界求解器是用于定义目标难度范围的一对已有语言模型，通常一个能力较低、一个能力较高。它们的能力差异构成提问者需要命中的目标区间。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

一次 Ask-E 交互的输入包括一个提问者模型、两个能力不同的边界求解器，以及要求生成问题的目标技能范围。提问者先通过与两个求解器对话，探测它们的能力差异；随后输出一道最终问题。分别由两个求解器回答该问题，若恰好一个回答正确，则交互成功，说明问题难度位于两者能力之间；若两个都答对，问题过易，若两个都答错，问题过难。该设定假定求解器的回答表现能够近似反映其相对能力，并且问题具有可判定的正确性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$A$**

提问者模型，负责探测边界求解器并生成最终问题。

</div>
<div class="notation-item" markdown="1">

**$S_\mathrm{low}$**

较低能力的边界求解器。

</div>
<div class="notation-item" markdown="1">

**$S_\mathrm{high}$**

较高能力的边界求解器。

</div>
<div class="notation-item" markdown="1">

**$q$**

提问者生成的最终问题；其难度需要落在两个边界求解器的能力范围之间。

</div>

</div>

**直接相关的工作**

- **传统基于问题回答的语言模型评测与训练**: Ask-E将其作为对照范式。传统方法直接使用模型回答已有问题的正确率作为评测或训练信号，而本文要求模型生成能区分两个求解器的问题，以降低对更强人工或模型监督者的依赖。
- **数学竞赛问题与数学基准评测**: 本文的问题难度校准动机来自数学竞赛和数学基准：简单题无法区分前沿模型，极难题又会使模型共同失败。Ask-E还将问题生成能力与AIME、HMMT及IMO-AnswerBench等数学回答能力联系起来。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

语言模型在数学等高难度领域的训练与评测，依赖一批难度恰好位于当前能力前沿的问题：过易的问题无法区分先进模型，过难的问题又会使所有模型同样失败。随着模型接近高水平人类能力，持续由更强的人类作者设计新颖、可解且难度准确的问题，正成为昂贵且难以扩展的瓶颈。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于既有题库的问答评测与训练**：让模型回答已有数学题，再将正确率作为能力指标或训练信号。评测题通常来自学校、竞赛或人工整理的数据集。
- **由更强人类专家持续出题**：当既有基准趋于饱和时，邀请竞赛冠军、大学教师或研究数学家编写更难的新题，并依靠其学科知识判断题目所需能力与目标难度。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有题库的有效难度区间会随模型进步而迅速失效：原文指出，诸如小学数学的过易题“不做任何区分”，而所有模型都会失败的过难题也“equally uninformative”。因此，正确率饱和或全面失败都不能稳定反映模型间的能力差异。
- 人工出题要求作者既能理解模型当前短板，又具备高于被测模型的数学能力、创造出分布外题目的能力，以及把握解题步骤所需技能的能力。该监督者必须持续强于被测模型的前提，在模型不断进步乃至超过人类时难以维持。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种可随边界模型能力同步升级、且不依赖更强外部监督者的环境，用来直接衡量并训练模型设计“恰好能区分两个能力水平”的问题的能力；这类环境还需要排除题目答案不稳定或含糊所造成的伪区分。

</div>
<div markdown="1"><span>核心问题</span>

能否把“为两个现有语言模型生成难度落在其能力差距内的问题”定义为可评测、可训练的任务，并仅依据这两个求解模型的作答差异，获得对出题模型的有效监督，以及迁移到数学解题能力的训练收益？

</div>
<div markdown="1"><span>作者直觉</span>

写出一道既不让两个模型都答对、也不让两个模型都答错的题，出题者必须估计二者各自会用到哪些知识与推理步骤，并定位其能力分界。作者据此将“恰有一个边界求解器答对”作为校准成功条件：求解器虽然能力可以与出题者相当或更弱，却能通过作答是否分化提供监督信号。为减少随机题或歧义题碰巧造成分化的风险，原文说明只有“三个独立交叉检查样本一致”时会话才可评分；不具稳定唯一答案的题会被拒绝为“bad cross-check”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Ask-E 将提问能力建模为一个可验证的校准任务：输入是两个能力不同的边界语言模型及其隐含能力差距，提问模型通过多轮探测估计该差距，再生成一个最终数学题。两个边界模型和一个独立交叉检查模型分别作答；当恰好一个边界模型的答案与交叉检查答案一致时，该题被判定为校准成功。直观地说，模型不能只生成“很简单”或“难到无人能解”的题，而必须生成一道刚好位于两个解题者能力之间的题。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 选择能力边界

从包含 $n$ 个模型的边界集合中选择一对模型；两者能力差异定义当前会话的目标难度区间。不同模型对最多形成 $\binom{n}{2}$ 个候选区间。

<div class="method-step__io" markdown="1">

**输入**：边界模型集合中的两个不同语言模型。<br>
**输出**：一个由较弱和较强边界模型共同限定的目标技能范围。

</div>

**直观理解**：只用一个模型无法排除极简单或极困难的问题，因此系统用两个模型夹住目标难度。提问模型需要把题目放在这两个能力水平之间。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 探测边界能力

提问模型进行 $k$ 轮探测，每轮向两个边界模型提出问题，并接收它们的答案及简短解题思路；提问模型保留完整会话历史，而边界模型逐题独立作答。

<div class="method-step__io" markdown="1">

**输入**：目标难度区间、提问模型，以及两个无状态边界模型。<br>
**输出**：包含边界模型响应、答案和解题摘要的探测上下文。

</div>

**直观理解**：这相当于先用几道试题观察两名解题者分别能处理什么问题。提问模型通过这些反馈估计最终题目应该落在哪个难度位置。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成校准问题

提问模型综合探测结果，生成带有可解析问题标签的最终数学题；生成结束后，提问模型不再看到边界模型对最终题的回答。

<div class="method-step__io" markdown="1">

**输入**：完整探测上下文和目标技能范围。<br>
**输出**：一条用于区分两个边界模型能力的最终问题。

</div>

**直观理解**：模型必须在没有最终答案反馈的情况下作出难度判断，因此考查的是预测他人解题能力和设计合适问题的能力，而不是事后挑选成功案例。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 独立作答与评分

两个边界模型独立作答；交叉检查模型独立作答三次，只有三次答案一致时会话才可评分。若恰好一个边界模型的答案与交叉检查答案匹配，则记为 calibrated，否则分别记为 too_easy 或 too_hard；无法解析问题或交叉检查答案不一致时记录为对应失败类别。

<div class="method-step__io" markdown="1">

**输入**：最终问题、两个边界模型和交叉检查模型。<br>
**输出**：每个会话的二元校准结果及错误类别统计。

</div>

**直观理解**：交叉检查模型相当于答案核验器，用来提供稳定的参考答案。恰好一个边界模型答对，说明题目确实把两者区分开，而不是两者都能做或两者都不能做。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 嵌入多样性奖励

$$
\alpha\cdot\left(1-\overline{\mathrm{cos\text{-}sim}}_{k\text{-NN}}\right)
$$

**符号说明**

- $\alpha$：多样性奖励的权重，训练设置为 $1.0$。
- $\overline{\mathrm{cos\text{-}sim}}_{k\text{-NN}}$：当前问题与滑动全局问题缓存中 $k$ 个最近邻问题的平均余弦相似度。
- $k$：最近邻数量，训练设置为 $5$。

<div class="equation-explanation" markdown="1">

**直观理解**：问题与历史问题越不相似，多样性奖励越高。但该项奖励受校准奖励门控，只有题目先被判断为校准成功或具有非负校准信号时才会生效，从而避免模型靠生成新奇但无效的问题刷分。<br>
**原文位置**：第 5.1 节 Reward shape；附录 E Embedding-diversity bonus

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练使用 CISPO 对提问策略进行强化学习优化。每次 rollout 的主要奖励为：校准成功 $+1.0$，两个边界模型都答对即 too easy 时 $+0.2$，两个都答错即 too hard 时 $-0.2$；每个缺少必需标签的轮次额外施加 $-0.05$ 格式惩罚，并加入上述经校准奖励门控的多样性项。优化只作用于提问模型自身的 assistant 令牌，边界模型令牌被屏蔽；训练不提供提问模型答案正确性反馈，也不使用新数学数据或更强模型交互。该目标把“能否生成合适难度的问题”直接转化为奖励，同时允许轻微保留过简单问题的信号，因为作者观察到奖励 too easy 比奖励 too hard 更有帮助。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双边界求解器**

两个边界求解器既定义目标难度区间，又参与最终判定。训练时使用不强于提问模型的 $1.5\mathrm{B}$ 至 $8\mathrm{B}$ 开放权重模型，并冻结其参数；边界求解器的响应令牌在训练损失中被屏蔽。

> 直观理解：它们提供的是能力标尺，而不是教师答案。训练阶段限制其能力，避免提问模型通过观察更强模型的推理过程获得隐式蒸馏。

**2. 探测与标签解析模块**

提问模型只能通过规定标签传递结构化内容：向边界求解器发送标签后的问题，向提问模型返回边界模型的摘要和保留的盒装答案；最终问题若没有可解析的问题标签，则会话记为 no question。

> 直观理解：标签把私有思考、实际问题和可用答案分开，防止无关生成内容污染后续角色。摘要机制也限制了提问模型看到的信息规模，使任务更接近根据有限观察估计能力。

**3. 交叉检查与奖励模块**

基准测试使用 Gemini 3.1 Pro 作为交叉检查模型，并要求三次答案一致；训练时使用提问模型当前权重作为独立实例的自交叉检查器，仅产生标量奖励，不把检查文本返回给提问模型。训练奖励包括校准奖励、格式惩罚和经校准奖励门控的嵌入多样性奖励。

> 直观理解：交叉检查模型只负责判断题目答案，不负责生成题目，因此不必比提问模型更强。训练时把检查结果压缩为分数，模型只能从分数中学习哪些提问策略更可能落在目标难度区间。

**训练与推理**

训练时以 Qwen3.5-4B Instruct、no-thinking 版本作为提问策略，使用 11 张 H200 GPU，rollout 与训练异步执行。每次优化步骤采样 256 个 rollout，分组大小为 $G=16$，每个 rollout 包含 3 轮探测和 1 个最终问题；训练共进行 200 个优化步骤并运行 3 个随机种子。边界集合只包含不强于提问模型的 12 个小模型，参数冻结；当前提问模型的独立推理实例负责单次自交叉检查，结果只转换为奖励，不返回交互上下文。推理或基准评测时，输入是边界模型对的目标区间和探测反馈，提问模型输出最终问题；随后两个边界模型及交叉检查模型独立求解，系统抽取最后一个 $\boxed{\cdot}$ 答案并进行等价性判断，最终输出 calibrated、too easy、too hard 或解析失败类别。

**复现信息**

Ask-E 当前只实现数学问题，但作者指出可通过替换提示词和答案等价性库扩展到其他领域。基准测试中，每个边界模型对的交叉检查模型进行三次独立采样并要求答案一致；答案等价性优先使用 math-verify，失败时再使用字符串、集合及 LLM 等价性检查。训练阶段为降低成本，仅使用一次交叉检查采样，不使用三次共识或 LLM 等价性检查；训练 rollout 使用 3 轮探测，基准配置则使用更长的探测和生成预算。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Ask-E 主基准：由不同边界求解器构成的 $190$ 个模型对；每个会话要求 asker 生成一道题，使两台边界模型中恰有一台答案与交叉核对答案一致。其角色是直接测量“按指定能力区间出题”的能力，而非传统答题准确率。
- AIME 系列：AIME 2022--2024 的 AIMO validation pool，共 $90$ 题；AIME 2025 Parts I 和 II 合并，共 $30$ 题。两者均为答案在 $[0,999]$ 的整数数学竞赛题，用于检验训练是否迁移到标准化的高难数学推理。
- HMMT 2025 与 IMO AnswerBench：前者为 2025 年 2 月 HMMT 题集，共 $30$ 题；后者为完整发布集，共 $400$ 题。它们使用自由形式答案，尤其 IMO AnswerBench 用于检验模型对等价数学表达式和更广题型的泛化。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**校准率**

一个 Ask-E 会话被记为 calibrated 的条件是，两台边界求解器中恰有一台的最终答案与三次交叉核对一致答案匹配；两台都匹配为 too_easy，两台都不匹配为 too_hard。 （越高越好，因为更高比例表示生成题目更准确地落在该模型对所界定的能力区间；但它不直接证明题目的客观正确性或教育质量。）

</div>
<div class="metric-item" markdown="1">

**$\mathrm{pass@8}$**

对每道下游题采样 $8$ 次；只要至少一个样本答案正确，该题计为 $1$，再对全数据集平均。它测量模型在多次尝试中能否至少找到一个正确解。 （越高越好，因为它衡量采样预算下的最佳尝试成功率；它会受样本数影响，不能单独代表单次回答的稳定性。）

</div>
<div class="metric-item" markdown="1">

**$\mathrm{avg@8}$**

先计算每题 $8$ 个样本中正确样本的比例，再在数据集上平均，等价于该采样设置下的平均单样本准确率。 （越高越好，因为它同时反映正确率与回答稳定性；相较 $\mathrm{pass@8}$，它不容易被少量偶然成功掩盖。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3.5-4B Instruct 经 Ask-E RL 训练后，在 $550$ 道下游数学题上的汇总表现

<div class="result-value" markdown="1">

三个训练种子在汇总题集上均同时超过未训练基线；$\mathrm{avg@8}$ 的平均提升为 $+1.1$ 个百分点，逐种子增益范围为 $+0.7$ 至 $+1.4$ 个百分点，种子间跨度为 $0.6$ 个百分点。

</div>

结果支持 Ask-E 训练能向数学解题迁移，且汇总增益在三个种子上方向一致。论文特别强调该训练没有加入新数学数据、没有与更强模型交互、也没有直接以答案正确性为奖励；但提升幅度较小，不能据此断言它会普遍优于专门的数学监督或更大规模训练。

<div class="result-source" markdown="1">

来源：Appendix I, Figure 11

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the pooled suite, every seed improves over the baseline on both metrics, and for avg@8 the per-seed spread (0.6pp, with gains ranging from +0.7 to +1.4 pp) is smaller than the mean gain of +1.1 pp.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Ask-E RL 后在不同难度下游数学基准上的迁移

<div class="result-value" markdown="1">

最易的 AIME 2022--2024 上，$\mathrm{pass@8}$ 提升 $+2.2$ 个百分点但 $\mathrm{avg@8}$ 下降 $-0.7$ 个百分点；较难基准的 $\mathrm{avg@8}$ 分别为 AIME 2025 提升 $+3.0$、HMMT 2025 提升 $+1.0$、IMO AnswerBench 提升 $+1.0$ 个百分点。

</div>

这说明训练并非在每个指标、每个基准上都一致改善：较易题集上模型更可能在八次采样中碰到一次正确答案，但平均样本正确率略降。作者的解释是增益模式与基准难度相关；从实验设计看，这一相关性是观察结果，不足以证明“难题必然受益更多”的因果规律。

<div class="result-source" markdown="1">

来源：Appendix I, Figure 11

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On AIME 2022–2024, the easiest benchmark in the suite (baseline avg@8 of 68%), performance is roughly flat, with avg@8 changing by −0.7 pp while pass@8 improves by +2.2 pp.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Ask-E 主基准的交叉核对求解器替换重评分

<div class="result-value" markdown="1">

将标准的 Gemini 3.1 Pro 三次交叉核对改为 Claude Opus 5 后，每个 asker 的校准率变化至多 $0.6$ 个百分点，asker 排名不变。

</div>

这表明在所测试的模型和题目上，基准排序及总体校准测量不太可能只是 Gemini 3.1 Pro 这一特定评分模型的产物。它仍不能排除所有评分偏差，因为两种设置都依赖模型答案分布而不依赖人工标注的题目真值。

<div class="result-source" markdown="1">

来源：Appendix G.2, Figure 8

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The calibration rate of every asker changes by at most 0.6 percentage points, and the ranking of askers is unchanged.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 下游数学迁移只比较同一 $4$B 模型训练前后，并覆盖 $550$ 题、三个训练种子；结果显示的是小幅平均提升，尚未证明对其他规模、模型家族、非数学任务或长期训练同样有效。
- Ask-E 的评分依赖边界模型和交叉核对模型的答案一致性，而不是人工验证的题目真值。尽管替换交叉核对模型后校准率至多变化 $0.6$ 个百分点，仍可能存在多个模型共享系统性错误时被误判为一致的风险。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 未训练的 Qwen3.5-4B Instruct（关闭 thinking）：这是 Ask-E RL 后模型的直接初始化对照；两者采用相同下游采样配置，因此分数变化可主要归因于训练。
- 无 probing 基线：Gemini 3.1 Pro 在不接收任何边界模型反馈时生成 $50$ 道题，随后每题对全部 $190$ 个边界对评分。它检验高校准率是否来自针对具体模型对的探测，而不是泛化地产生困难题。
- 替换交叉核对求解器的重评分：将标准的 Gemini 3.1 Pro 三次一致交叉核对替换为 Claude Opus 5 单次交叉核对。它不是模型能力基线，而是评分机制的稳健性对照。
- 三种独立 Ask-E RL 训练随机种子：报告训练后均值及每个种子结果，用于判断下游增益是否可能只是单次训练随机波动。

**实验想回答的问题**

- Ask-E 能否稳定评测模型针对特定能力边界对生成题目的校准能力，且该测量是否依赖某一个交叉核对求解器？
- 仅用 Ask-E 的强化学习训练、不给模型新增数学题数据和正确性奖励，能否迁移提升 Qwen3.5-4B Instruct 的数学解题能力？

**实验实现**

Ask-E 评分中，asker 最终题目独立交给 Gemini 3.1 Pro 采样三次；只有三次答案一致时该会话可评分。边界模型答案须与这三个一致答案全部匹配才计正确，答案等价性先经 $\texttt{math-verify}$、LaTeX 归一化和若干规则匹配，再由 LLM 等价性检查器复核。下游评测中，训练后模型与未训练 Qwen3.5-4B Instruct 均关闭 thinking，使用相同的 $\texttt{temperature}=1.0$、$\texttt{top\_p}=0.95$、$\texttt{top\_k}=20$、每题 $8$ 次采样和 $32{,}000$ token 上限；AIME/HMMT 采用规则等价匹配，IMO AnswerBench 采用 Gemini 3.1 Flash Lite 的固定是/否提示进行数学等价性裁决。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除 probing：Gemini 3.1 Pro 不获得针对边界对的探测反馈，生成 $50$ 道无条件题目并对全部 $190$ 个边界对评分 | 校准率从有 probing 的 $44.9\%$ 降至无 probing 的 $16.3\%$；$81.7\%$ 的结果为 too easy。 | 该消融隔离了交互式 probing 的价值。大幅下降说明主基准的表现主要依赖根据特定边界对反馈调整题目，而非仅生成普遍高难度题；但该设置只直接报告 Gemini 3.1 Pro asker，不能自动推广到所有 asker。 | Appendix G.3, Figure 9<br><span class="experiment-evidence">The calibration rate drops from 44.9% with probing to 16.3% without, showing that the majority of benchmark performance comes from probing and pair-specific calibration rather than from generating generically difficult questions.</span> |
| 检查校准结果方向：Gemini 3.1 Pro asker 的 $853$ 个 calibrated 会话，以及参数规模明显分离的 $288$ 个会话 | 经验上较弱的求解器单独答对占 $75/853=8.8\%$；限制为一台低于 $4$B 参数、另一台高于 $8$B 参数的模型对后，占 $9/288=3.1\%$。 | 该分析检验对称校准标准是否经常出现“弱模型赢、强模型输”的反常情况。比例较低说明多数已校准题确实在稳定地区分能力，但“较弱”由该模型对十题中的总正确数事后定义，且相近能力模型并不存在可靠的全序强弱关系。 | Appendix G.4, Figure 10<br><span class="experiment-evidence">This occurs in 75 of 853 calibrated sessions (8.8%). Restricting to clearly separated pairs, with one solver under 4B parameters and the other over 8B, it occurs in 9 of 288 calibrated sessions (3.1%).</span> |

**定性案例**

- 无 probing 的成对结果显示，残余校准主要集中在含最弱边界求解器的模型对，而 $81.7\%$ 结果过易。其定性含义是：不观察某一对模型的具体失败模式时，asker 生成的题通常无法精确落入窄能力间隔；较宽的弱模型能力缺口只是更容易被随机覆盖。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces an environment that benchmarks calibrated question generation at model capability frontiers and evaluates downstream mathematical reasoning gains.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`56f7e6a45cfc3c81d6b6ea7a66ce2d2e0b4e4c583730ddba5f5f342606b07572`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
