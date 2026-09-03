---
title: "[论文解读] Thinking effort aligns between humans and reasoning models in abductive reasoning"
description: "[arXiv 2609.01867][LLM Reasoning] 本文以溯因推理为更难依靠形式线索投机的测试场景，考察人类反应时间与大型推理模型推理轨迹长度是否体现一致的思考成本，并进一步分析允许探索多条推理路径的解码方式是否会增强这种一致性。"
arxiv_id: "2609.01867"
announcement_date: "2026-09-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:29:15.913987+00:00"
source_sha256: "22e2cc2bf7a092ea9c6f148c5c5774bced79e577b782d763d5b1e43599bf3d6d"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "LLM 其他"
  - "大型推理模型"
  - "人类—模型行为对齐"
  - "溯因推理"
  - "链式思维"
  - "反应时"
  - "解码策略"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.01867</p>

# Thinking effort aligns between humans and reasoning models in abductive reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> Henry Arthur</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Center for Mind/Brain Sciences, University of Trento, Italy</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01867v1) · [PDF 下载](https://arxiv.org/pdf/2609.01867v1) · **关键词** 大型推理模型, 人类—模型行为对齐, 溯因推理, 链式思维, 反应时, 解码策略<br>


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

本文以溯因推理为更难依靠形式线索投机的测试场景，考察人类反应时间与大型推理模型推理轨迹长度是否体现一致的思考成本，并进一步分析允许探索多条推理路径的解码方式是否会增强这种一致性。

**不用术语来说**：如果一道题让人思考得更久，推理模型是否也会为它生成更长的推理过程？已有研究发现二者相关，但模型可能只是识别出某些题型在形式上“看起来更难”，继而输出更多文字，并不一定进行了与人类相似的搜索。本文因此改用溯因任务：给定两个观察结果，从两个候选假设中选择更好的解释；题目难度主要取决于比较各假设能解释什么，而不是可直接识别的逻辑形式。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 将人类—模型思考成本对齐的检验从多类推理任务收窄到溯因推理，通过缺少显式形式难度标记的强制选择任务，降低模型依靠题型结构模拟“费力程度”的可能性。
- 把解码策略纳入对齐测量，比较不同推理探索方式，并报告：对多次温度采样得到的推理轨迹进行聚合，会增强三个受测模型的推理成本与人类反应时间之间的相关性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于人类认知建模与大语言模型推理研究的交叉领域，核心问题是：模型在解决问题时所表现出的“思考成本”是否与人类相似。论文特别研究大型推理模型（large reasoning models, LRMs），这类模型通过带可验证奖励的强化学习（RLVR）优化，目标是获得正确的推理答案，而不只是生成符合人类偏好的文本。与普通语言模型相比，LRM通常会生成链式思维（chain-of-thought, CoT）轨迹，并可在困难问题上分配更多生成词元；论文将模型推理轨迹的长度与人的反应时进行比较。研究对象是溯因推理，即从不充分决定结论的观察出发，选择能够提供“最佳解释”的假设。作者选择该任务，是因为其难度主要取决于搜索候选假设及其解释力，而不是可由题目形式直接读出的逻辑结构，因此更适合检验模型与人类是否具有相似的实际推理努力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大型推理模型（LRM）与可验证奖励强化学习（RLVR）**

LRM是专门强化推理能力的大语言模型；RLVR根据答案是否正确等可自动验证的结果给予奖励，而不是主要依赖人类对文本偏好的评价。模型因此倾向于为推理任务生成更长或更充分的中间过程。

</div>
<div class="concept-item" markdown="1">

**溯因推理（abductive reasoning）**

溯因推理是根据观察到的结果，提出并选择最能解释这些结果的假设，也常被称为“最佳解释推理”。由于同一组观察通常可能有多个解释，任务具有不确定性，正确选择不能仅由固定的形式逻辑规则决定。

</div>
<div class="concept-item" markdown="1">

**思考成本与对齐**

本文用人的反应时和模型生成的推理词元数量近似表示解决题目所需的思考成本。若题目之间这两种成本的变化呈稳定相关，则称模型与人类在推理努力上存在行为对齐；这是一种经验相关性，并不等同于证明二者具有相同的内部机制。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文将溯因推理操作化为二选一任务：输入包括两个观察，即故事状态从 $O_1$ 到 $O_2$ 的变化，以及两个候选解释假设；输出是被试或模型选择的一个假设。候选假设来自基于短篇叙事的数据集，其中一项假设应当比另一项更能解释观察到的状态变化，但两者被设计为较难区分。人类实验记录选择准确率与反应时；模型实验记录最终答案和生成的链式思维轨迹，并以轨迹词元数作为模型思考成本的代理变量。分析重点是题目层面的模型词元数与人类反应时之间的相关性，同时控制题目长度，因为较长题目可能同时增加阅读时间和生成长度。除贪心解码外，论文还比较基于温度的多次采样及其聚合结果，以测试让模型探索多条推理路径是否会增强人类—模型思考成本对齐。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$O_1,O_2$**

故事或情境中的两个观察状态，分别表示状态变化的起点与终点。

</div>
<div class="notation-item" markdown="1">

**$RT$**

人类完成某道题所需的反应时（reaction time）。

</div>
<div class="notation-item" markdown="1">

**$T$**

模型生成的推理轨迹词元数量，用作模型思考成本的近似指标。

</div>
<div class="notation-item" markdown="1">

**$\rho_{T,RT\mid L}$**

在控制题目长度 $L$ 后，模型轨迹长度 $T$ 与人类反应时 $RT$ 之间的偏相关；用于衡量二者在题目难度变化上的对齐程度。

</div>

</div>

**直接相关的工作**

- **de Varda et al. (2025)**: 该研究在七类推理任务上比较模型推理轨迹的词元数与人类反应时，并在 DeepSeek-R1 及其他开放权重推理模型上发现模型能够追踪人类的思考努力。本文沿用这一比较思路，但将任务限定为溯因推理，以减少模型仅凭演绎题的形式结构预测难度的可能性，并进一步考察不同解码策略。
- **Bhagavatula et al. (2020)**: 该工作提供了本文使用的常识溯因数据来源。其数据改编自 ROCStories：参与者根据故事开头和结尾生成解释假设，之后通过最小修改构造竞争假设，并使用 BERT 对候选对进行对抗性筛选，使正确解释更难辨别。本文在此基础上收集新的在线人类数据，并将任务用于人类—模型思考成本比较。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

认知建模需要判断大型语言模型或大型推理模型能否作为人类推理行为的有效模型。大型推理模型经过可验证奖励强化学习训练，能够根据问题难度在推理时分配不同数量的词元；但其思维链只是外显的语言轨迹，未必忠实反映内部计算。因此，仅观察模型是否答对，或是否生成较长解释，都不足以确认其计算负担是否随题目变化而与人类一致。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **跨任务的人类反应时间—模型词元数相关分析**：de Varda 等人的方法以人类完成题目的反应时间表示人类思考成本，以大型推理模型思维链的词元数近似模型计算投入，再检验二者在同一任务内部及不同任务之间的相关性；其研究覆盖七类推理任务，并在 DeepSeek-R1 及另外五个开放权重推理模型上进行验证。
- **基于单次解码的思维链成本测量**：常见测量直接使用一次模型生成所得的思维链长度。解码温度控制候选词元分布的平滑程度：较低温度偏向高概率路径，但可能产生重复的“思考循环”；较高温度则允许模型探索不同推理路径。本文据此把多次温度采样及结果聚合作为更充分刻画模型推理成本的候选方案。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 演绎或三段论任务的难度可部分由形式结构推断。模型可能记住哪些推理格式通常更难，并对这些格式机械地分配更多词元；这样得到的人类反应时间—模型词元数相关性，可能来自表面难度线索，而非双方都进行了更费力的解空间搜索。
- 思维链既可能与模型的内部计算不忠实，也会受到解码策略影响：混合语言、退化轨迹甚至无意义填充词元有时仍能帮助作答，而推理也可能完全发生在潜在表示空间中。若只采用单次或过于确定性的解码，词元数可能混入重复循环和采样偶然性，削弱其作为“思考成本”代理量的效度。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有结果尚未在一个难度无法从固定逻辑形式直接读出、必须比较多个可能解释的任务中，隔离并验证人类与大型推理模型的思考成本对齐；同时也不清楚这种对齐在多大程度上取决于是否允许模型探索并汇总多条推理路径。

</div>
<div markdown="1"><span>核心问题</span>

在溯因式“最佳解释推断”任务中，控制题目长度后，人类逐题反应时间是否与大型推理模型的推理轨迹长度稳定相关，模型与人类是否呈现相似错误，以及采用多次温度采样等非贪心解码策略是否能提高这种成本对齐？

</div>
<div markdown="1"><span>作者直觉</span>

溯因推理中的观察通常不足以唯一确定结论，两个候选假设在表面长度或固定逻辑格式上也没有必然的难度标签；要选出更好的解释，解题者必须实际考察每个假设如何连接并解释观察。因而，如果某些题目同时让人类反应更慢、让模型投入更多推理词元，这种对应关系比演绎题中的结构性相关更难用题型记忆解释。进一步地，多次较高温度采样让模型尝试不同解释路径，再聚合其成本，可以减少单条轨迹的偶然性及低温循环，更接近人类在不确定条件下搜索和权衡备选解释的过程。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本研究不是训练新模型，而是构建一个用于比较人类与大语言推理模型（LRM）推理努力的统一评估流程。输入是包含两条观察和两个候选假设的溯因推理题；输出包括人类反应时、模型推理轨迹长度、答案正确性，以及二者在题目层面的相关性。核心做法是先让人类和模型解决相同的自然语言任务，再用每道题的平均人类反应时与模型生成的推理词元数衡量“思考成本”，并控制题目长度后计算偏相关。直观地说，研究者检查的是：哪些题目让人类花费更久，是否也让模型生成更长的推理过程，而不是只比较最终答对率。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造溯因推理测试集

保留假设长度相差不超过一个词、删除重复观察上下文，并以随机种子 $42$ 抽取 $162$ 道题，其中 $160$ 道为正式题、$2$ 道为练习题；正式题全部来自经过对抗性筛选的测试集。每道题要求选择能够最好解释两条观察之间发生过程的假设。

<div class="method-step__io" markdown="1">

**输入**：AllenAI 的 Abductive Natural Language Inference Dataset（ART）中的训练集和测试集候选题目；每题包含观察 $O_1$、$O_2$ 以及假设 $A$、$B$。<br>
**输出**：包含 $160$ 道正式溯因选择题的共同测试项目集，以及每题的标准答案和总提示长度。

</div>

**直观理解**：这类题不是从前提必然推出唯一结论，而是在两个可能解释中选出最合理者，因此题目难度不能仅由形式逻辑结构直接读出。研究者还尽量匹配两个选项的长度，避免参与者或模型仅凭较长选项作答。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 采集人类行为数据

参与者在线完成强制选择任务，使用键盘上的 Q、P 键选择假设；答案位置随机化，并设置理解检查、练习题、注意力试题和试题间 $200$ 毫秒注视十字。记录每题选择结果与反应时，并剔除反应异常快或疑似离开电脑的参与者。

<div class="method-step__io" markdown="1">

**输入**：最终 $N=120$ 名居住在美国的英语母语者，以及 $160$ 道正式题。<br>
**输出**：每道题的平均人类反应时、参与者层面的选择正确性，以及总体人类准确率。分析中还按四个不重叠区块分配题目和参与者。

</div>

**直观理解**：参与者被要求“尽量快但保持准确”，所以反应时被当作人类思考努力的行为指标。对每道题汇总多人反应，可以减少某个参与者偶然分心、迟疑或操作速度差异带来的噪声。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 获得模型答案与推理成本

通过 OpenRouter API 调用模型，贪心条件使用温度 $0$；LRM 的 `<think>...</think>` 内容作为推理轨迹，并统计生成词元数。对不原生输出推理轨迹的 DeepSeek-V3，在提示末尾加入“Let’s think step by step”；另外对 R1、GPT-OSS-20B 和 Qwen3-32B 使用模型提供者建议的非贪心温度，并进行多次独立采样后取每题平均词元数和多数投票答案。

<div class="method-step__io" markdown="1">

**输入**：相同的题目提示、七个 LRM 和一个非推理基线 DeepSeek-V3；模型包括 DeepSeek-R1、Qwen3-235B（Thinking）、Qwen3-32B（Thinking）、GPT-OSS-20B、GPT-OSS-120B、GLM-4.5-Air 和 Kimi-K2（Thinking）。<br>
**输出**：每个模型、每道题的答案标签、正确性和推理词元成本；随机解码条件下还得到多次运行的均值、方差和收敛所需运行次数。

</div>

**直观理解**：模型“想了多久”用生成了多少推理词元近似表示，而不是用墙钟时间，因为不同模型的服务延迟不可直接比较。随机解码会让同一道题产生多条思路，取平均相当于用多次观察估计模型在该题上的典型思考成本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 控制长度并检验人机对齐

对反应时和推理词元数取对数，并分别对数化题目词元长度做残差化，再计算题目层面的 Pearson 偏相关；同时用模型共识准确率或单模型正确性与人类题目准确率计算错误对齐。对随机采样，通过重复抽取不同数量的运行子集进行 bootstrap，判断偏相关是否稳定。

<div class="method-step__io" markdown="1">

**输入**：每题的平均人类反应时、模型平均推理词元数、题目提示长度和模型答案正确性。<br>
**输出**：人类反应时与模型推理成本的偏相关、模型与人类错误模式的相关性、温度条件差异以及随机运行的收敛诊断。

</div>

**直观理解**：题目越长通常越耗时，也可能让模型生成更多词；长度控制后，相关性更接近“题目本身的推理难度”而非文本长度。错误对齐则回答另一问题：人和模型是否会在相似的困难题上共同失败。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 对数推理词元的标准误

$$
\mathrm{SE}=\frac{\bar{\sigma}}{\sqrt{k}}
$$

**符号说明**

- $\mathrm{SE}$：对每道题取 $k$ 次随机运行平均后的对数推理词元估计的标准误。
- $\bar{\sigma}$：已有随机运行中估计的每题对数推理词元标准差的中位数。
- $k$：用于聚合的独立随机运行次数。

<div class="equation-explanation" markdown="1">

**直观理解**：独立运行越多，平均推理长度的不确定性按 $1/\sqrt{k}$ 下降。该式把“需要运行多少次”转化为可量化的稳定性问题，而不是凭经验决定采样次数。<br>
**原文位置**：附录 F，Chain-of-Thought Convergence

</div>

</div>

<div class="equation-block" markdown="1">

#### 达到目标标准误所需的运行次数

$$
k^{*}=\left(\frac{\bar{\sigma}}{\theta}\right)^{2}
$$

**符号说明**

- $k^{*}$：使标准误达到目标阈值所需的理论运行次数。
- $\bar{\sigma}$：每题对数推理词元标准差的中位数。
- $\theta$：预先设定的标准误目标阈值。

<div class="equation-explanation" markdown="1">

**直观理解**：当模型在不同随机运行间波动更大时，所需运行次数按平方增加。研究用它交叉验证 bootstrap 收敛结果；例如高温度下 GPT-OSS-20B 的理论需求超过可用运行池，支持其未收敛的判断。<br>
**原文位置**：附录 F，Chain-of-Thought Convergence；由该节的标准误公式推导

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文没有提出或训练新的模型，也没有在 ART 数据集上优化参数；模型沿用各提供者已经训练完成的检查点。研究中的“推理努力对齐”是评估目标而非训练损失，具体通过人类反应时与模型推理词元数之间的长度控制偏相关，以及双方题目级错误相关性来衡量。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 溯因强制选择任务**

每个项目由两条观察和两个候选假设组成，参与者或模型选择能够最好连接 $O_1$ 与 $O_2$ 的假设。测试集采用对抗性筛选后的项目，以保留更难区分的候选解释；同时删除重复上下文并限制选项长度差异。

> 直观理解：题目要求补出故事中间最合理的事件，而不是机械地证明一个必然结论。这样可以更直接地观察内容和常识如何改变推理难度。

**2. 推理努力测量与长度控制**

模型努力定义为推理轨迹生成的词元数；DeepSeek-V3 则将提示诱导出的链式思考词元作为对应指标。由于提示长度与反应时的相关为 $r=0.669$，分析对 $\\log(\\mathrm{RT})$ 和 $\\log(\\mathrm{tokens})$ 分别在 $\\log(\\mathrm{prompt\ length})$ 上残差化，再计算偏相关。

> 直观理解：研究者并不把更长的文字自动当作更难，而是先扣除题目文字长度造成的共同影响。剩下的关系才用于判断人类和模型是否对同一道题表现出相似的额外思考需求。

**3. 随机解码聚合与收敛检验**

在推荐温度下，R1 运行 $10$ 次，GPT-OSS-20B 和 Qwen3-32B 各运行 $25$ 次；对每个项目取平均推理词元数和多数投票答案。对运行数 $k$ 的每个候选值进行 $500$ 次随机子集抽样，并以 $95\%$ 置信区间宽度低于 $0.03$ 且偏相关均值相邻变化小于 $0.01$ 判定收敛。

> 直观理解：一次随机生成可能恰好走出特别长或特别短的思路，不能代表模型通常的行为。多次采样并平均就像让多名参与者完成同一道题，可以减少偶然性；收敛规则用于确认样本次数已经足够。

**训练与推理**

训练阶段不属于本文流程。推理阶段首先用与人类任务说明相匹配的模板向模型提供两条观察和两个假设；在贪心条件下设置温度 $0$，直接记录模型答案与推理轨迹长度。对 DeepSeek-V3，追加“Let’s think step by step”以诱导链式思考；对 R1、GPT-OSS-20B 和 Qwen3-32B，分别在推荐温度（$0.6$、$1$、$0.6$）以及温度 $2$ 下进行多次独立调用。每次调用提取最终答案标签和生成词元数，按题目聚合得到平均成本与多数答案；随后将人类和模型的题目级指标对数化，并控制提示长度后计算 Pearson 偏相关。错误分析使用人类每题准确率与模型正确或错误标签，随机解码分析则在不同运行数下重复子集抽样并检查相关估计是否收敛。

**复现信息**

为便于复现，正式测试集有 $160$ 道题，候选池经长度匹配、重复上下文删除后以随机种子 $42$ 抽样；其中 $87$ 道标准答案为 A、$73$ 道为 B，题目总词数均值为 $33.5$、标准差为 $7.0$，范围为 $19$ 至 $70$。人类样本从 Prolific 招募，最终样本平均年龄为 $33.0$ 岁，标准差为 $6.6$；模型调用采用各模型默认推理努力设置，除文中明确改变的温度外，其他解码参数保持默认。分析同时以提示词元数和词数作为长度控制变量进行稳健性检查；Spearman 偏相关也用于检验结果是否依赖线性或分布假设。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 核心评测集包含 160 道溯因推理题；每题同时具有人类作答数据和模型回答。人类侧记录逐题平均反应时与正确率，模型侧记录推理 token 数、答案标签与正确性。原文节选未报告训练集、验证集或测试集划分，因而这里应理解为行为评测集，而非用于训练模型的数据集。
- 贪心解码评测覆盖 DeepSeek-R1、GPT-OSS-120B、GPT-OSS-20B、Qwen3-235B-Thinking、Kimi-K2-Thinking、GLM-4.5-Air、Qwen3-32B-Thinking，以及非推理模型 DeepSeek-V3。其作用是比较不同模型逐题推理长度与人类反应时的对应关系，并计算跨模型的逐题共识正确率。
- 随机解码评测选取 DeepSeek-R1、GPT-OSS-20B 和 Qwen3-32B-Thinking，在模型提供方推荐温度及高温设置下重复采样。每题的多次运行被汇总为平均推理 token 数和答案标签，用来检验多路径采样是否提高与人类行为的对齐程度。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**控制题目长度后的 Pearson 偏相关系数**

先对数变换人类平均反应时、模型推理 token 数和提示 token 数，再从前两者中回归掉提示长度影响，最后计算逐题相关。它主要衡量模型推理成本能否预测人类思考时间，而不是仅仅反映长题同时导致更多阅读时间和更多模型输出。 （绝对值越大表示控制题长后关联越强；本文关注正相关，因此 $r$ 越高代表模型认为更费力的题通常也更耗费人类时间。显著性 $p$ 值用于评估该关联是否足以排除随机波动。）

</div>
<div class="metric-item" markdown="1">

**模型—人类错误对齐相关**

将模型逐题正确或错误与人类逐题正确率关联；跨模型分析还使用模型共识正确率，即每题答对模型所占的无权重比例。该指标测试双方是否在相同题目上成功或失败，而不仅是总体准确率是否接近。 （正相关越高，表示模型和人类对题目难度的排序越一致；但它不能单独证明两者采用了相同的内部推理机制。）

</div>
<div class="metric-item" markdown="1">

**Steiger–Williams 相关差异检验与采样收敛**

Steiger–Williams 检验比较同一批题目上共享人类反应时变量的两个相关系数，例如贪心解码与随机解码的偏相关。收敛分析则反复抽取 $k$ 次运行，观察偏相关 bootstrap 区间宽度及增加一次运行后的均值变化。 （相关提升的检验 $p$ 值越小，越支持解码设置确实改变对齐程度；达到稳定所需的 $k$ 越小，说明多次采样的汇总估计越快稳定。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 八个模型在贪心解码下的推理成本对齐

<div class="result-value" markdown="1">

控制提示长度后，所有模型的推理 token 数都与人类平均反应时显著正相关。GPT-OSS-120B 的对齐最强，为 $r=0.552$、$p<.001$；唯一的非推理模型 DeepSeek-V3 最弱，为 $r=0.197$、$p=.012$。不过，DeepSeek-R1 与 DeepSeek-V3 的相关差异未达到显著水平，Fisher $z=1.23$、$p=.217$。

</div>

作者结果表明，模型在某题上生成更长推理过程时，人类通常也需要更长时间，而且该现象不能简单归因于题目文本更长。分析上，这支持“逐题思考成本存在行为对齐”。但推理模型与非推理模型之间的优势没有在直接统计比较中可靠成立，因此不能据此断言强化推理训练必然造成更人类化的思考机制。

<div class="result-source" markdown="1">

来源：第 3.1 节 Greedy Decoding Correlations；图 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

After controlling for prompt length, all models are significantly correlated with human reasoning effort. The strongest alignment was observed for GPT-OSS-120B (r = 0.552, p < .001) and GPT-OSS-20B (r = 0.41, p < .001), followed by Qwen3-235B-Thinking (r = 0.359, p < .001), DeepSeek-R1 (r = 0.327, p < .001), Kimi-K2-Thinking (r = 0.303, p < .001), GLM-4.5-Air (r = 0.263, p < .001), and Qwen3-32B-Thinking (r = 0.229, p = .002). The only non-reasoning model, DeepSeek-V3, was also significantly correlated (r = 0.197, p = .012), though it showed the weakest alignment of all models tested. Notably, the difference between DeepSeek-R1 and its non-reasoning counterpart DeepSeek-V3 did not reach significance (Fisher z = 1.23, p = .217), suggesting that while reasoning models tend to show numerically stronger alignment, the advantage over a capable non-reasoning model was not reliably detected at this sample size.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 贪心解码下模型与人类的逐题错误对齐

<div class="result-value" markdown="1">

DeepSeek-R1 答对的题上，人类正确率为 $82.5\%$；在其答错的题上，人类正确率降至 $47.8\%$，点二列相关为 $r=0.53$、$p<.001$。进一步汇总全部模型后，控制提示长度的模型共识正确率与人类正确率相关达到 $r=0.668$、$p<.001$。

</div>

双方不仅总体上会做错题，而且倾向于被同一批题难住，说明模型的逐题难度敏感性与人类相似。作者据此反对简单记忆解释；更谨慎的分析是，共享错误确实不符合对全部题目的近乎完美记忆，但仍不足以单独排除训练数据污染，也不能证明模型与人类使用完全相同的认知步骤。

<div class="result-source" markdown="1">

来源：第 3.2 节 Greedy Error Alignment；图 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Looking at DeepSeek-R1, human accuracy on items R1 answered correctly was 82.5%, compared to 47.8% – below chance – on items R1 got wrong (point-biserial r = 0.53, p < .001; see Figure 3). This pattern generalized across all models: the correlation between model consensus accuracy and human accuracy, computed as the Pearson partial correlation across the 160 items between per-item model-consensus accuracy and per-item human accuracy, controlling for prompt length, was r = 0.668 (p < .001).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 推荐温度下多次随机采样并平均推理成本

<div class="result-value" markdown="1">

相较贪心解码，推荐温度随机采样使三个模型的偏相关都提高：GPT-OSS-20B 从 $r=0.41$ 升至 $r=0.55$，且 $p<.001$；Qwen3-32B 从约 $r=0.23$ 升至 $r=0.32$，且 $p<.05$；DeepSeek-R1 从约 $r=0.32$ 升至 $r=0.37$，但差异不显著。

</div>

对同一题探索多条生成路径再取平均，通常比单次确定性输出更接近人类平均思考时间，且其中两个模型的提升具有统计显著性。直观上，单次输出可能受偶然生成路径影响，而多次采样更接近模型对该题所需计算量的期望值。不过，DeepSeek-R1 的提升未显著，故不能把该效果视为对任意模型都已可靠成立。

<div class="result-source" markdown="1">

来源：第 3.3 节 Stochastic Decoding Correlations；图 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In GPT-OSS-20B, the partial went from r = 0.41 to r = 0.55, (Steiger–Williams test, p < .001), and the model converged to a stable partial at k = 19 runs. For Qwen3-32B, greedy r = 0.23 and at temp = 0.6, r = 0.32 (p < 0.05), and converged at 18 runs. R1 also improved from greedy decoding at r = 0.32 and r = 0.37 for temp = 0.6, but the difference was not significant, and this model converged after 8 runs.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 推理成本以生成 token 数代理，人类成本以反应时代理。两者都可能受到与核心推理无关的因素影响，例如模型表述冗长度、人类阅读速度或作答策略；控制提示长度只能减少其中一部分混杂，行为相关也不能直接证明共享内部机制。
- 随机解码实验只覆盖三个模型，且 DeepSeek-R1 的提升未显著；同时，DeepSeek-R1 与非推理模型 DeepSeek-V3 的贪心相关差异也未显著。因此，“推理模型普遍优于非推理模型”以及“随机采样对所有模型都可靠有效”均超出了现有证据。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 贪心解码（$T=0$）：每题仅沿单一路径生成，是判断随机多路径采样是否真正改善行为对齐的直接基线。
- DeepSeek-V3：实验中唯一的非推理模型，并与 DeepSeek-R1 形成有意义的同系列对照，用于判断经推理优化的模型是否比能力较强的普通模型更接近人类思考成本。
- 推荐温度随机解码：DeepSeek-R1 与 Qwen3-32B-Thinking 使用 $T=0.6$，GPT-OSS-20B 使用 $T=1$；该设置检验适度探索多条推理路径并取均值的效果。
- 高温随机解码（$T=2$）：作为过度随机化对照，用于区分“多路径探索有益”和“温度越高越有益”这两个不同命题。

**实验想回答的问题**

- 在排除题目长度这一混杂因素后，模型每题生成的推理 token 数是否与人类平均反应时一致，即模型和人类是否在相同溯因推理题上付出较多思考成本？
- 模型与人类是否会在相似题目上犯错，以及允许模型随机探索并汇总多条推理路径，能否比贪心解码更好地预测人类推理成本？

**实验实现**

所有思考成本分析均按题进行：人类侧使用平均反应时，模型侧使用推理 token 数；两者均取对数，并控制由各模型原生 API tokenizer 得到的对数提示 token 数。作者同时以对数词数替代 token 数、以 Spearman 偏相关替代 Pearson 偏相关，并分别限制为人类答对或人类与模型均答对的响应进行稳健性检查。随机解码中，DeepSeek-R1 最终运行 10 次，GPT-OSS-20B 与 Qwen3-32B-Thinking各运行 25 次；每题汇总平均 token 响应和答案标签，并通过 Monte Carlo 子采样确定相关估计何时收敛。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 将推荐温度提高到统一高温 $T=2$ | GPT-OSS-20B 的偏相关降至 $0.22$，相对贪心解码变化为 $\Delta=-0.19$，且 25 次运行后仍未收敛。Qwen3-32B 相对贪心增加 $\Delta=+0.063$，但仍低于 $T=0.6$，并需 24 次运行才收敛，比 $T=0.6$ 多 6 次；DeepSeek-R1 相对贪心仅增加 $\Delta=+0.028$，并在 6 次运行后收敛。 | 该对照隔离了“多路径采样”与“极高随机性”的区别。结果不支持温度越高越好：过强随机性可降低相关、拖慢稳定，甚至使估计在既定运行预算内不收敛。因此推荐温度的收益更可能来自有限度地覆盖合理路径，而不是制造任意多样性。 | 第 3.3 节 Stochastic Decoding Correlations；图 6<br><span class="experiment-evidence">GPT-OSS-20B partial r decreased to 0.22 (Δ = −.19), and the partial did not converge after 25 runs (Figure 6). Qwen3-32B partial increased by Δ = +.063, but was still lower than the results with temp = 0.6 and converged at 24 runs, 6 runs more than temp 0.6. R1 Temp = 2 increased from T=0 by Δ = +.028 and converged after 6 runs.</span> |
| 检验跨随机运行的 token 方差是否提供独立预测信息 | 在控制每题平均 token 数后，跨运行 token 方差与人类反应时的偏相关介于 $-0.12$ 至 $+0.08$，所有检验均为 $p>.12$。 | 该分析隔离了随机采样收益究竟来自“平均推理长度”还是“模型在该题上的不稳定程度”。方差没有额外解释力，说明取每题多次运行的均值已经足够；观察到的提升不太可能仅由少数波动极大的异常运行驱动。 | 第 3.3 节 Stochastic Decoding Correlations<br><span class="experiment-evidence">Token variance across stochastic runs did not predict human RT beyond what mean token count already explained (partial rs = −.12 to +.08, all ps > .12), confirming that a simple per-item mean is sufficient and that results are not driven by a small number of high-variance outlier runs.</span> |

**定性案例**

- DeepSeek-R1 提供了直观的逐题案例：将题目按模型答对或答错分组后，人类在前一组明显更准确，而在后一组甚至低于机会水平。图 3 因而把抽象相关系数转化为易理解的现象——模型失误集中于人类也普遍觉得困难的题；但这是集合层面的行为对应，并未展示单道题的具体推理轨迹是否与人类相同。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper empirically evaluates whether reasoning-model search effort and errors align with human abductive reasoning behavior.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`22e2cc2bf7a092ea9c6f148c5c5774bced79e577b782d763d5b1e43599bf3d6d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
