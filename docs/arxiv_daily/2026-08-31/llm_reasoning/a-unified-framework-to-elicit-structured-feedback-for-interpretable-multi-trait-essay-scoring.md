---
title: "[论文解读] A Unified Framework to Elicit Structured Feedback for Interpretable Multi-Trait Essay Scoring"
description: "[arXiv 2608.28407][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.28407"
announcement_date: "2026-08-31"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:39:29.560165+00:00"
source_sha256: "afd5a0fc0bd7ca50762ba3e05e00dfa6ae0a56a3c59b3166b8e29c14f22ee16e"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "多特质自动作文评分"
  - "结构化反馈生成"
  - "层级化链式思考"
  - "大语言模型后训练"
  - "可解释评分"
  - "评分量规对齐"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.28407</p>

# A Unified Framework to Elicit Structured Feedback for Interpretable Multi-Trait Essay Scoring

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Shihang Yang, Sanwoo Lee, Ningning Zhao, Yunfang Wu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: National Key Laboratory for Multimedia Information Processing, Peking University；Affiliation: School of Computer Science, Peking University；Affiliation: School of Chinese Language and Literature, Beijing Normal University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28407v1) · [PDF 下载](https://arxiv.org/pdf/2608.28407v1) · **关键词** 多特质自动作文评分, 结构化反馈生成, 层级化链式思考, 大语言模型后训练, 可解释评分, 评分量规对齐<br>
**代码**: [https://github.com/Atiyahsama/HiFTS](https://github.com/Atiyahsama/HiFTS) · **项目页**: [https://github.com/Atiyahsama/HiFTS](https://github.com/Atiyahsama/HiFTS)

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

自动作文评分（Automated Essay Scoring，AES）利用计算模型依据评分标准评价作文，输出整体分数；多特质自动作文评分（multi-trait AES）进一步把写作质量拆分为内容、结构、表达、格式规范等评分维度，并同时预测各维度分数与整体分数。与只判断作文优劣的整体评分相比，多特质评分能够提供更细粒度的诊断信息，但各特质通常相互依赖：例如段落结构会影响论证表达，材料选择也会影响内容深度。因此，该任务不仅要求模型预测分数，还要求其依据评分量规生成与分数一致、可解释的反馈。本文关注中文和英文作文上的多特质评分，并将结构化反馈生成与分数预测放入同一个自回归过程。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**整体评分与多特质评分**

整体评分是对作文总体质量给出一个分数；多特质评分则按照评分量规分别评价内容、结构、表达和格式规范等维度。各特质分数提供更细的诊断，但它们并非完全独立。

</div>
<div class="concept-item" markdown="1">

**评分量规与结构化反馈**

评分量规是规定“什么样的作文应得什么分”的评价标准，例如内容是否充实、段落是否连贯、语句是否准确。结构化反馈把模型的判断组织成有层次的文字说明，使读者能够理解分数对应的优缺点，而不是只看到一个黑箱分数。

</div>
<div class="concept-item" markdown="1">

**自回归生成与链式思考反馈**

自回归模型按顺序生成文本，后面生成的内容可以利用前面已经生成的内容。本文先生成从整体到局部的层级化链式思考（CoT）反馈，再生成特质分数和整体分数，以便让分数建立在前面的量规分析之上。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一篇作文及其适用的评分标准，模型需要输出两类结果：一是围绕多个评分特质生成层级化、量规对齐的反馈，二是预测各特质分数和整体分数。CFMS-34 将任务具体化为对 951 篇中文作文进行整体评分和 34 项细粒度特质评分，特质覆盖 Content、Structure、Expression 和 Conventions 四个维度；实验还在英文多特质基准 ASAP++ 上进行。任务的核心假设是，特质之间存在需要显式建模的依赖关系，且反馈内容应当与随后生成的数值分数保持一致。与只生成分数、由外部模型提供反馈，或使用独立回归头产生分数的设置不同，本文要求一个统一的自回归模型先进行全局到局部的量规推理，再生成特质级和整体分数。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入作文文本。

</div>
<div class="notation-item" markdown="1">

**$s_i$**

第 $i$ 个评分特质的预测分数，其中特质可属于内容、结构、表达或格式规范维度。

</div>
<div class="notation-item" markdown="1">

**$s_h$**

作文的整体（holistic）预测分数。

</div>
<div class="notation-item" markdown="1">

**$D_{\mathrm{task}}$**

作文评分任务数据集；本文主要包括中文数据集 CFMS-34 和英文基准 ASAP++。

</div>

</div>

**直接相关的工作**

- **Chu et al. (2025)**: 该类方法使用外部大语言模型生成反馈，并将反馈作为输入来训练主要负责预测分数的模型。它说明反馈能够帮助评分，但反馈与评分并未在同一个生成过程中联合产生，因此可能存在分数—反馈脱节；HiFTS 则把层级反馈生成和分数生成统一为一个自回归流程。
- **Li and Pan (2025)**: 该方法原生生成反馈，但数值评分由独立的回归头产生。本文认为这种架构削弱了反馈推理与最终分数之间的直接联系；HiFTS 改为先生成量规对齐的反馈，再在同一生成链中输出特质分数和整体分数。

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

HiFTS 将多特质自动作文评分建模为统一的自回归生成过程：输入作文 $X$ 及其评分量规，模型先按“全文理解—高层维度—细粒度子特质”的层级生成可检查的思维链反馈 $Y_{\mathrm{CoT}}$，再生成各子特质分数与整体分数 $S$。训练采用先监督微调、后强化学习的两阶段方案；监督微调使模型学习量规化反馈到分数的生成顺序，GRPO 则利用评分一致性、反馈语义质量和结构合法性等奖励进行联合优化。推理时，BERT 回归器提供作文整体质量的粗粒度先验 $S_{\mathrm{prior}}$，作为软锚点输入语言模型，以减少长反馈生成中的语义漂移。直观地说，HiFTS 不是先“猜一个分数”再补解释，而是先沿着评分标准逐层检查作文，再让分数从检查结果中自然产生。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 层级反馈构造

使用教师模型 Gemini-3 按照“全文理解 $\rightarrow$ 高层维度分析 $\rightarrow$ 子特质评价”的自上而下结构生成量规化思维链反馈，并将反馈与标注分数拼接为目标序列 $Y=[Y_{\mathrm{CoT}};Y_{\mathrm{Score}}]$。

<div class="method-step__io" markdown="1">

**输入**：作文 $X$、评分量规定义和人工标注的子特质及整体分数。<br>
**输出**：包含层级反馈、34 个子特质分数和整体分数的统一目标序列。

</div>

**直观理解**：教师模型先示范一份完整的评分过程：先说明文章整体情况，再分别检查内容、结构、表达和规范等维度，最后给出细项与总分。这样学生模型学习到的不只是答案，还包括答案应如何由量规逐步支撑。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 监督微调预热

将反馈到分数的目标序列作为指令提示后的自然续写，使用标准 token 级交叉熵训练学生语言模型参数 $\theta$。

<div class="method-step__io" markdown="1">

**输入**：作文输入 $X$ 与教师构造的统一目标序列 $Y$。<br>
**输出**：能够生成层级反馈并随后输出特质分数和整体分数的初始模型 HiFTS-SFT。

</div>

**直观理解**：先用示范数据进行模仿学习，避免模型在尚未掌握层级推理格式时直接接受稀疏的最终分数奖励。反馈必须先出现、分数随后出现，有助于把评分决定锚定在前面的量规分析上。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### GRPO 多目标强化学习

对候选回答计算整体与特质 QWK、负 MSE、反馈与教师反馈的语义余弦相似度及结构规则奖励，形成复合奖励 $R$；再使用 Group Relative Policy Optimization 根据同组候选的相对奖励更新策略。

<div class="method-step__io" markdown="1">

**输入**：HiFTS-SFT、作文提示、人工金标准分数、教师反馈，以及每个提示采样得到的一组候选回答。<br>
**输出**：在评分准确性、反馈质量和输出结构之间取得平衡的 HiFTS 策略模型。

</div>

**直观理解**：模型一次提出多份可能的评分报告，系统比较它们谁更接近人工分数、反馈更像高质量教师反馈且格式更完整，再提高较好回答的生成概率。这样优化目标不再只关心“总分对不对”，也关心“理由是否有用、是否遵守层级结构”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 带全局先验的推理

BERT 回归器先估计粗略整体质量，并将该分数写入系统提示；语言模型在条件 $X,S_{\mathrm{prior}}$ 下自回归生成层级反馈 $Y_C$，再根据反馈生成特质分数和整体分数 $S$。

<div class="method-step__io" markdown="1">

**输入**：待评分作文 $X$、训练完成的 GRPO 语言模型，以及 BERT 回归器预测的整体质量先验 $S_{\mathrm{prior}}$。<br>
**输出**：包含量规对齐反馈、特质分数和整体分数的最终评分报告；$S_{\mathrm{prior}}$ 不作为最终预测。

</div>

**直观理解**：全局先验像导航中的大致目的地：它先告诉模型文章总体可能处于哪个质量区间，但不替模型完成评分。模型仍需逐项分析量规，只是较不容易在长篇推理过程中从“文章一般”漂移到“文章优秀”或相反结论。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 监督微调交叉熵目标

$$
\mathcal{L}_{\mathrm{SFT}}=-\sum_{t=1}^{T}\log P_{\theta}(y_t\mid y_{<t},X)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{SFT}}$：监督微调阶段的训练损失。
- $T$：目标序列的 token 总长度。
- $y_t$：第 $t$ 个目标 token，属于反馈或分数序列。
- $y_{<t}$：第 $t$ 步之前已经出现的目标 token。
- $X$：输入作文。
- $P_{\theta}$：参数为 $\theta$ 的学生语言模型对下一个 token 的条件概率。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标要求模型在每个位置都提高正确下一个 token 的概率。由于目标序列先包含层级反馈、后包含分数，优化会同时教会模型如何组织反馈以及如何从反馈继续生成评分结果。<br>
**原文位置**：第 4.1 节，式（2）

</div>

</div>

<div class="equation-block" markdown="1">

#### 强化学习复合奖励

$$
R=\alpha\left(R_{\mathrm{QWK}}+R_{\mathrm{MSE}}\right)+(1-\alpha)R_{\mathrm{CoT}}+\delta
$$

**符号说明**

- $R$：候选回答的总奖励。
- $\alpha\in[0,1]$：评分对齐与反馈对齐之间的平衡系数；论文在开发集上选择 $\alpha=0.8$。
- $R_{\mathrm{QWK}}$：整体分数与特质分数和人工标注之间的 QWK 对齐奖励；整体部分在最近 $h=64$ 个生成样本的滑动窗口上计算。
- $R_{\mathrm{MSE}}$：预测分数与金标准分数之间均方误差的负值，较大的数值偏差会降低奖励。
- $R_{\mathrm{CoT}}$：生成反馈与教师反馈的语义对齐奖励，通过句向量余弦相似度计算。
- $\delta$：基于规则的结构合法性固定奖励或惩罚。

<div class="equation-explanation" markdown="1">

**直观理解**：这个目标把三个问题合并考虑：分数是否接近人工标注、反馈是否在语义上接近教师示范、输出是否满足规定结构。$\alpha$ 越大，训练越偏向分数；$\alpha$ 越小，训练越偏向反馈质量。<br>
**原文位置**：第 4.2 节，式（3）；$R_{\mathrm{QWK}}$ 与 $R_{\mathrm{CoT}}$ 的具体定义见式（4）和式（5）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练分为两个优化阶段。第一阶段以 $\mathcal{L}_{\mathrm{SFT}}$ 最小化 token 级预测误差，使学生模型学习教师提供的层级反馈到分数的生成轨迹；第二阶段冻结这一结构化能力的初始化基础，使用 GRPO 最大化组内相对的复合奖励 $R$，同时优化分数一致性、数值误差、反馈语义质量和结构合法性。论文报告开发集上选择 $\alpha=0.8$，并在主实验中使用整体 QWK 奖励的滑动窗口 $h=64$；作者同时指出 $h=128$ 略优，但 $h=64$ 接近且被用于主实验。直观而言，SFT 先教模型“按什么步骤写评分报告”，强化学习再教模型“怎样让这份报告更准确、更可靠”。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 层级反馈到分数的统一自回归生成**

模型将 $Y_{\mathrm{CoT}}$ 与 $Y_{\mathrm{Score}}$ 放在同一目标序列中，按照先反馈、后分数的顺序生成。反馈层级对应全文理解、高层维度和子特质评价，覆盖内容、结构、表达和规范等量规组织的评价层次。

> 直观理解：评分报告被设计成一条连续的推理链，而不是彼此独立的分数预测器和解释器。因此读者可以沿着具体子特质检查模型为什么得到某个分数。

**2. 复合奖励与 GRPO**

奖励由评分对齐项、反馈对齐项和结构规则项组成：评分部分结合整体滑动窗口 QWK、特质级 QWK 与负 MSE，反馈部分使用生成反馈和教师反馈句向量的余弦相似度，结构项 $\delta$ 对格式进行固定规则奖励或惩罚。GRPO 对同一提示的候选回答使用组内相对奖励更新策略，避免为每个奖励目标引入大量独立权重；系数 $\alpha$ 控制评分对齐与反馈对齐的相对侧重。

> 直观理解：一个回答即使分数接近人工答案，若反馈空泛、层级错乱，也不应被视为完整成功。复合奖励把“分数准确”“解释相似且有质量”“格式合规”放进同一评价框架，再由组内比较帮助模型选择更好的回答。

**3. BERT 全局先验引导**

BERT 回归器根据作文 $X$ 输出粗粒度整体先验 $S_{\mathrm{prior}}$，该先验仅作为语言模型提示中的条件信息。生成分解为 $P(Y_C,S\mid X,S_{\mathrm{prior}})=P(Y_C\mid X,S_{\mathrm{prior}})P(S\mid Y_C,X,S_{\mathrm{prior}})$，体现先生成反馈、再基于反馈生成分数的条件依赖。

> 直观理解：该模块不是另加一个最终投票器，而是在生成开始时提供总体方向。论文中的随机先验和常数先验实验表明，只有与当前作文相关的先验才有助于稳定推理。

**训练与推理**

训练时，首先为每篇作文准备量规、人工分数和教师生成的层级反馈，将反馈与分数组成统一序列进行 SFT；随后针对每个提示采样一组候选回答，计算 QWK、负 MSE、反馈嵌入余弦相似度和结构奖励，并用 GRPO 更新语言模型。推理时，BERT 回归器先对作文输出 $S_{\mathrm{prior}}$，系统提示将作文和该先验共同提供给 GRPO 对齐后的语言模型；模型先生成 $Y_C$，再生成特质分数与整体分数 $S$，其中最终结果来自语言模型的反馈到分数过程，而不是直接采用 BERT 先验。论文给出的概率分解为先生成 $Y_C$、再条件于 $Y_C$ 生成 $S$，因此方法的核心输出是一个可追踪的完整评分报告。

**复现信息**

数据方面，CFMS-34 包含 951 篇中国小学生课堂作文，每篇由两名专家按照 34 个细粒度子特质和整体分数标注，分数范围为 $0$ 到 $5$，并按 $8:1:1$ 划分训练、开发和测试集；该数据集主要用于训练和评估中文多特质评分。强化学习中的反馈语义奖励在 CFMS-34 使用 bge-small-zh-v1.5，在 ASAP++ 使用 all-MiniLM-L6-v2；这些选择来自原文第 4.2 节。模型骨干在主表中分别报告 Qwen2.5 与 Qwen3，推理先验使用 BERT 回归器；原文节选未明确报告 BERT 架构、GRPO 的候选组大小、优化器、学习率或完整提示模板，因此不应据此补充复现细节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- CFMS-34：中文多特质作文数据集，包含 951 篇作文、34 个量规特质及整体分数；实验使用量规分析确定的 20 个核心特质，两个评分者给出的 0–5 分相加为 0–10 分，用于训练和评测。该数据集主要检验中文、多维量规和层级反馈场景下的评分能力。原文未明确报告训练集、开发集和测试集的具体规模。
- ASAP++：在 ASAP 基准上扩展而来的英文多特质作文数据集，覆盖 8 个题目并提供人工标注的特质分数，用于同时评估整体评分和特质级评分，也用于检验方法对英文及不同题目分布的泛化能力。原文未明确报告各划分的具体规模。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**二次加权 Kappa（QWK）**

衡量模型评分与人工评分之间的一致性，并对不同程度的分歧赋予不同权重；Overall 表示 CFMS-34 的整体 QWK，Prompts 表示 ASAP++ 八个题目的平均整体 QWK，Traits 表示平均特质级 QWK。 （越高越好，因为高值表示模型与人工评分在等级判断上更加一致。）

</div>
<div class="metric-item" markdown="1">

**均方误差（MSE）**

衡量预测分数与人工分数之间的平方误差，用于补充 QWK 对数值校准的评估。 （越低越好，因为低值表示预测分数在数值上更接近人工分数。）

</div>
<div class="metric-item" markdown="1">

**WinRate**

由 DeepSeek-V3.2 对成对反馈进行比较所得的胜率，仅比较同一数据集上每个 SFT 模型与其 GRPO 对齐版本，用于评价反馈的相对质量。 （越高越好，表示模型反馈在成对比较中更常被判定为较优；但它依赖大语言模型评审，不能等同于人工金标准质量。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### CFMS-34 与 ASAP++ 的整体及特质评分

<div class="result-value" markdown="1">

作者报告 HiFTS 在两个数据集上均保持较强且一致的表现；Qwen3-4B 加 GRPO 的模型达到整体 QWK 0.677，并将 MSE 降至 0.741。原文没有在所提供摘录中给出其他模型或所有指标的完整数值表，因此不能据此计算相对提升幅度。

</div>

该结果说明方法不仅适用于中文作文，也能迁移到英文多题目多特质评分；同时，较低的 MSE 表明预测分数的数值校准也得到改善。但由于摘录缺少完整表格、数据划分规模和多次运行统计，不能判断提升是否具有统计显著性，也不能单独归因于某一个模块。

<div class="result-source" markdown="1">

来源：第 6.1 节 Scoring Performance，Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The Qwen3-based model with GRPO achieves the best results, reaching 0.677 Overall QWK and reducing MSE to 0.741.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### CFMS-34 的 20 个特质级评分

<div class="result-value" markdown="1">

GRPO 对齐模型总体上优于对应的 SFT 模型，Qwen3 版本取得最高平均特质 QWK，并在大多数特质维度上获得提升。

</div>

这表明奖励对齐可能改善模型对细粒度量规维度的判断，而不仅仅是改善整体分数。由于特质之间可能存在难度差异，平均提升并不意味着每一个特质都提升；原文也未在摘录中提供各特质的具体分数或提升幅度。

<div class="result-source" markdown="1">

来源：第 6.2 节 Fine-grained Trait Analysis，Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GRPO-aligned models generally outperform their SFT counterparts, with the Qwen3-based variant achieving the highest average trait QWK and consistent gains on most dimensions.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 反馈质量与量规依据

<div class="result-value" markdown="1">

作者报告 GRPO 对齐版本相较于 SFT 版本具有更高的 WinRate，且在 CFMS-34 上差异尤其明显；进一步的规则型 grounding 指标显示，对齐版本分数更高，完整 HiFTS 表现最佳。

</div>

结果支持 GRPO 不仅影响分数预测，也可能改善反馈的连贯性、量规对齐和逻辑一致性。WinRate 只是在 SFT 与 GRPO 版本之间的相对比较，并由大语言模型评审；规则型 grounding 指标由特质覆盖率、特质级论证和推理密度构成，因此二者都不能完全替代人工评价。

<div class="result-source" markdown="1">

来源：第 6.3 节 Feedback Assessment，Table 8

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 8 shows that reward-aligned variants obtain higher grounding scores than SFT, and full HiFTS performs best.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验结果来自一次固定随机种子运行，原文未报告多次运行的方差或显著性检验，因此结果稳定性仍需进一步验证。
- 反馈质量的 WinRate 依赖 DeepSeek-V3.2 的大语言模型评审，grounding 指标则依赖规则设计；摘录未提供充分的人类专家评价或跨评审者验证，因此反馈质量结论仍可能受到自动评审偏差影响。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- HISK：代表性作文评分模型，用于与传统神经作文评分方法比较其整体评分能力。
- STL-LSTM：单任务长短期记忆网络模型，用于检验多任务、反馈和奖励对齐设计相对于单一评分任务建模的增益。
- MTL-BiLSTM：多任务双向长短期记忆网络，用于比较显式联合建模多个评分目标的效果。
- RMTS：使用外部大语言模型生成特质级理由的多特质评分模型，是最直接的反馈增强型比较对象，可检验 HiFTS 的联合反馈—评分建模是否优于将理由作为外部输入或独立增强信号。

**实验想回答的问题**

- HiFTS 能否在中文 CFMS-34 和英文 ASAP++ 上同时提升整体评分与多特质评分，并保持跨语言、跨数据集的稳定性？
- 分层 CoT 监督、GRPO 奖励对齐和全局先验分别能否改善评分一致性、数值校准以及反馈的量规依据与结构有效性？

**实验实现**

模型采用两阶段流程：先在分层 CoT 数据上对 Qwen2.5-7B 和 Qwen3-4B 进行监督微调，再使用 GRPO 进行奖励对齐。分层 CoT 反馈由教师大语言模型依据量规蒸馏得到，学生模型学习先生成结构化反馈，再预测特质分数和整体分数。GRPO 每个输入采样 $G=4$ 个回答，KL 系数为 $\beta=0.02$，学习率为 $1\times10^{-6}$；复合奖励中的权重设为 $\alpha=0.8$，结构奖励或惩罚为 $\delta=0.1$。整体 QWK 奖励在最近 $h=64$ 次生成的滑动窗口上计算。全局先验由中文的 bert-base-chinese 或英文的 bert-base 初始化的 BERT 回归器产生，用于提供整体质量指导。推理时模型接收作文、量规提示以及可选的整体分数先验，输出 [Analysis]、[Trait Scores] 和 [Overall Score] 三个字段，解码温度为 0.6，$top\text{-}p=0.9$。结果来自一次固定随机种子运行，检查点依据开发集整体 QWK 选择。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| SFT 与 GRPO 对齐版本比较 | 在 CFMS-34 上，GRPO 进一步改善 Overall QWK、Traits QWK 和 MSE；在 ASAP++ 上，GRPO 进一步改善题目平均整体 QWK 和特质级 QWK，并提高反馈 WinRate 或 grounding 表现。 | 这一比较主要隔离奖励对齐阶段的作用：在相同分层 CoT 监督基础上加入 GRPO 后，模型同时在评分和反馈指标上改善，因此支持 GRPO 有助于缓解反馈与分数不一致。不过摘录未提供每个版本的具体数值，不能估计各模块的增益大小。 | 第 6.1 节 Scoring Performance，Table 5<br><span class="experiment-evidence">In contrast, HiFTS performs consistently across both datasets, with GRPO further improving CFMS-34 Overall QWK, Traits QWK, and MSE, as well as ASAP++ prompt-averaged and trait-level QWK.</span> |
| 加入全局先验的变体比较 | 在 ASAP++ 的 Qwen2.5 实验中，PPO 和 GRPO 改善了多数特质，相比之下加入 prior guidance 后进一步提升，完整 HiFTS 获得最佳平均 QWK。 | 该比较检验轻量级整体质量先验能否为长篇层级推理提供全局约束。结果说明先验可能减少推理过程中逐步偏离整体质量的风险，但因为摘录没有分别列出无先验与有先验的数值，也没有呈现 CFMS-34 上该组件的独立结果，所以不能断言其收益在所有数据集和所有特质上都成立。 | 第 6.2 节 Fine-grained Trait Analysis，Table 6<br><span class="experiment-evidence">PPO and GRPO improve most traits over the neural baselines, and prior guidance helps further; HiFTS attains the best mean QWK, indicating that the alignment strategy also generalizes to English multi-dimensional scoring.</span> |

**定性案例**

- 原文摘录未提供具体作文、反馈文本或逐案例对照，因此无法给出可核验的定性案例；仅能确认推理输出被结构化为 [Analysis]、[Trait Scores] 和 [Overall Score] 三个字段。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The method uses hierarchical rubric-grounded chain-of-thought generation and group-relative policy optimization to jointly produce feedback and essay scores.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`afd5a0fc0bd7ca50762ba3e05e00dfa6ae0a56a3c59b3166b8e29c14f22ee16e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
