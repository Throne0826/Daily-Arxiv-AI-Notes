---
title: "[论文解读] DIVE: Unlocking Self-Improvement in Frozen Language Models Through Diversity-Driven Skill Evolution"
description: "[arXiv 2608.12486][LLM Reasoning] DIVE将冻结语言模型的任务经验与验证器反馈压缩为可持久保存的自然语言技能，并通过维持多条独立、互补的技能演化路径，降低单一路径优化的过拟合与局部收敛风险。"
arxiv_id: "2608.12486"
announcement_date: "2026-08-14"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:59:48.763128+00:00"
source_sha256: "a3423b8a9d913675fd4685dbcb55cff1e11989d17e06bafa6feba6e3b3a6ffe5"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "冻结大语言模型"
  - "自改进"
  - "自然语言技能"
  - "验证器反馈"
  - "部署后适应"
  - "无参数更新"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.12486</p>

# DIVE: Unlocking Self-Improvement in Frozen Language Models Through Diversity-Driven Skill Evolution

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Siheng Xiong, Ali Payani, Oguzhan Gungordu, Faramarz Fekri</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Georgia Institute of Technology；Cisco Research</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12486v1) · [PDF 下载](https://arxiv.org/pdf/2608.12486v1) · **关键词** 冻结大语言模型, 自改进, 自然语言技能, 验证器反馈, 部署后适应, 无参数更新<br>


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

DIVE将冻结语言模型的任务经验与验证器反馈压缩为可持久保存的自然语言技能，并通过维持多条独立、互补的技能演化路径，降低单一路径优化的过拟合与局部收敛风险。

**不用术语来说**：部署后的语言模型即使反复做同类题、收到对错反馈或发现有效解法，也不会自动把这些经验留给后续请求；若不能修改模型参数，它通常只能在每次调用时近似“从头开始”。论文要解决的是：怎样让同一个固定模型自行整理过去的经验，形成以后还能复用和继续修订的解题规则，同时避免经验越积越多而超出上下文容量。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将冻结语言模型的自我改进表述为“持久自然语言技能”的演化：同一模型负责解题、解释验证器反馈和修订技能，无须更新权重，也无须更强的教师模型；技能集中记录可复用的推理步骤、核验策略、常见错误和输出约束。
- 作者提出以多样性控制技能搜索的不稳定性：从自助采样的经验出发独立演化多个技能种群，用异质变换产生候选，并从所有种群中联合选择一组紧凑且互补的技能，使演化阶段保留的不同思路能在推理阶段共同提高可靠性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究冻结大语言模型的部署后自改进问题。常规大语言模型虽然能够进行数学与逻辑推理，但在参数不更新时，一次任务中得到的经验、错误反馈或有效策略不会自动保留到后续请求；微调虽可将经验写入参数，却要求开放模型权重、训练基础设施和较高计算预算，不适用于许多仅能通过 API 使用的模型。本文因此把自然语言上下文视为一种可写入的外部载体：模型将任务经验压缩成持久的自然语言“技能”，以后在该技能条件下作答。研究场景尤其严格，因为同一个冻结模型既负责解题，也负责依据验证器信号修订技能，不依赖更强的教师模型；验证器只判断答案是否正确，并可能返回格式错误、执行失败或超时等结构化诊断，而不提供自然语言批评。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**冻结语言模型**

指推理和适应过程中参数保持不变的语言模型。模型仍可通过提示词或外部文本技能改变当前行为，但这些变化没有写入模型权重。

</div>
<div class="concept-item" markdown="1">

**自然语言技能**

一种紧凑、持久的文本制品，用来记录可复用的推理步骤、核验策略、常见失败模式和输出约束。它类似模型可读取和继续修订的任务手册，而不是参数空间中的新知识。

</div>
<div class="concept-item" markdown="1">

**外部验证器**

一个可访问标准答案的评估组件，用二元得分判断模型回答是否正确，并可附加格式违规或执行失败等结构化信号。本文假设它不直接说明错误原因，因此模型必须自行从作答轨迹和结果中归纳修订方向。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务分布为问题与标准答案对 $(x,y)\sim\mathcal{T}$，冻结模型 $f_{\theta}$ 接收问题 $x$ 并生成回答，外部验证器通过 $r(x,y,f_{\theta}(x))\in\{0,1\}$ 判断回答是否正确。模型的基础任务表现定义为验证得分在分布 $\mathcal{T}$ 上的期望；研究目标是在始终固定参数 $\theta$ 的条件下提高该期望。为实现经验积累，模型使用自然语言技能 $s$ 作为附加条件生成 $f_{\theta}(x;s)$，并在数据集 $\mathcal{D}$ 上收集由问题、技能条件下的回答及验证得分组成的轨迹集合 $\mathcal{E}(\mathcal{D};s)$；随后仍由同一模型根据旧技能和这些轨迹产生修订技能 $s'$。最终输出不是更新后的模型权重，而是可持久保存、复用、编辑、回退并可能跨模型迁移的文本技能；本文进一步关注如何避免单条随机修订路径过拟合有限经验或过早收敛，但具体的多群体演化与联合选择属于方法部分。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$f_{\theta}$**

参数为 $\theta$ 的语言模型；本文优化期间固定 $\theta$，只改变模型读取的自然语言技能。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{T}$**

由问题与标准答案对 $(x,y)$ 构成的任务分布，用于定义模型或技能的期望表现。

</div>
<div class="notation-item" markdown="1">

**$r(x,y,f_{\theta}(x))$**

外部验证器给出的二元正确性得分，取值 $1$ 表示回答正确，取值 $0$ 表示错误。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{E}(\mathcal{D};s)$**

技能 $s$ 在数据集 $\mathcal{D}$ 上产生的验证器标注轨迹集合，每条轨迹包含问题、模型回答和验证得分。

</div>

</div>

**直接相关的工作**

- **GEPA**: 原文将其作为提示优化方法的代表；这类方法主要搜索单个改进提示，而 DIVE 所针对的缺口是保留多种技能假设与演化路径，并在推理时利用它们的互补性。
- **AutoSkill**: 参考文献将其描述为基于经验、通过技能自演化实现终身学习的工作，属于与自然语言技能积累直接相关的方向；给定节选未提供更具体的方法比较或实验关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

许多高能力模型只能通过API使用，开发者无法访问权重，或者只有很有限的适配算力与训练预算。此时，微调所需的权重权限、计算资源和专门训练流程难以满足，但应用仍需要模型从持续到来的任务样例和验证反馈中积累经验。因此，需要一种不改参数、能跨请求保存知识，并能在有限上下文中长期复用的自我改进机制。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **参数更新方法（如SFT与GRPO）**：通过监督微调或基于奖励的优化，把任务经验写入模型参数，使后续推理直接受更新后权重影响。它能够内化经验，但依赖权重访问、训练算力以及经过设计的数据与优化流程。
- **文本反思、记忆与提示优化方法（如GEPA所代表的提示搜索）**：保持模型参数不变，把示例、反馈、反思或规则写入外部文本上下文，或反复搜索和修订提示，从而改变模型之后的解题行为。其基本依据是自然语言上下文本身可以充当一种可写的适配载体。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单候选、贪心式的文本修订容易受自生成反馈噪声影响：一次局部有效的编辑可能删除原有的有用规则、迎合少量失败样例，或放大错误反思；由于自然语言技能优化具有随机性、非凸性和路径依赖，单条轨迹还可能过早丢弃有潜力的替代方案并停在次优解。
- 简单累加演示、推理轨迹和反馈会迅速耗尽上下文预算，而主要寻找一个改进提示的方法也没有充分解决多条演化路径之间的互补利用问题；结果是系统既难以长期压缩经验，也难以抵消不同初始化、经验采样和修订顺序造成的优化方差。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚缺少一种完整机制，能够在权重冻结且没有更强教师的条件下，由同一个模型把验证反馈蒸馏成紧凑、可复用、可继续修订的技能，同时在整个搜索过程中保留多个有差异的候选轨迹，并在最终推理时有原则地利用这些轨迹的互补性。

</div>
<div markdown="1"><span>核心问题</span>

冻结语言模型能否仅依靠自身的任务经验和验证器反馈，把经验转化为持久自然语言技能，并通过多样化的技能演化与联合选择，实现稳定、可持续且无需参数更新的自我改进？

</div>
<div markdown="1"><span>作者直觉</span>

技能修订可以看成在庞大文本空间中寻找更好“解题手册”：只维护一本手册时，某次错误总结就可能把搜索带偏；同时维护多本从不同经验出发、采用不同修订方式的手册，则更可能保住各自擅长的策略。最后不必强行把所有内容合成一个冗长提示，而是选择少量互补技能分别生成答案，再由冻结模型排序候选，从而把搜索阶段的多样性转化为预测阶段的稳健性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

DIVE把冻结语言模型的自我改进表述为自然语言“技能”的搜索与组合，而不是参数训练。输入是带标准答案的开发数据、只能返回正确性及可选结构化错误信号的验证器，以及参数固定的模型$f_{\theta}$；系统先将开发数据划分为演化集$\mathcal{D}_{\mathrm{evo}}$和验证集$\mathcal{D}_{\mathrm{val}}$，再从演化集自助采样出$K$组不同的经验子集与反思子集。每组数据独立初始化并演化一个技能种群：模型从已验证的成功和失败轨迹中归纳技能，通过多种演化算子提出修订，以UCB规则动态分配有限的提案预算，并在演化中生成针对新失败模式的算子。所有种群完成后，候选技能仅在共享验证集上进行最终组合选择；测试时，每个入选技能独立生成答案，再由同一冻结模型排序并输出最佳候选。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 数据划分、自助采样与轨迹采集

为每个种群$k\in[K]$从$\mathcal{D}_{\mathrm{evo}}$独立自助采样经验子集$\mathcal{D}_{\mathrm{exp}}^{(k)}$和反思子集$\mathcal{D}_{\mathrm{ref}}^{(k)}$；运行模型后，用$r(x,y,f_{\theta}(x;s))\in\{0,1\}$标注技能条件轨迹。经验子集用于提炼初始知识，反思子集用于评价技能、定位失败并指导后续修订。

<div class="method-step__io" markdown="1">

**输入**：任务数据中的问题—答案对$(x,y)$、冻结模型$f_{\theta}$、外部验证器$r$，以及演化集$\mathcal{D}_{\mathrm{evo}}$。<br>
**输出**：每个种群各自的已验证经验轨迹$\mathcal{E}(\mathcal{D}_{\mathrm{exp}}^{(k)})$，以及用于演化反馈的反思数据。

</div>

**直观理解**：这相当于让多个研究小组从同一批题目中抽取不同样本，各自总结解题经验，并预留另一批样本检查总结是否真正有效。不同抽样使各组更可能形成互补策略，而不是重复同一条搜索路径。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多种群种子技能初始化

同一模型调用$\operatorname{InitializeSkill}_{f_{\theta}}$，从正确与错误轨迹中蒸馏若干自然语言种子技能$\mathcal{S}_{0}^{(k)}$。技能文本编码可复用的推理步骤、核验策略、常见失败模式和输出格式约束，而不修改参数$\theta$。

<div class="method-step__io" markdown="1">

**输入**：第$k$个种群的零样本验证轨迹$\mathcal{E}(\mathcal{D}_{\mathrm{exp}}^{(k)})$。<br>
**输出**：$K$个彼此独立且内部具有多样性的初始技能种群$\{\mathcal{S}_{0}^{(k)}\}_{k=1}^{K}$。

</div>

**直观理解**：技能不是新模型权重，而是模型随后阅读和执行的一份解题规程。多个种群从不同经历出发，可降低一次随机归纳恰好得到偏置或次优规程的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### UCB驱动的自适应技能演化

每一步先按UCB选择算子$a_t$，再依算子要求选择父技能集合$\mathcal{P}_t$；模型结合父技能及其验证器标注轨迹，从条件分布$p_{f_{\theta}}(\cdot\mid\mathcal{P}_t,\mathcal{E}(\mathcal{D}_{\mathrm{ref}}^{(k)};\mathcal{P}_t),a_t)$采样修订技能$s'_t$。系统以新技能相对最佳父技能的正确率增量更新算子统计和种群，并在$t_{\mathrm{new}}$依据演化历史生成$N_{\mathrm{new}}$个新算子。

<div class="method-step__io" markdown="1">

**输入**：当前技能种群$\mathcal{S}_{t-1}^{(k)}$、反思子集$\mathcal{D}_{\mathrm{ref}}^{(k)}$、演化算子池$\mathcal{A}^{(k)}$和预算$B$。<br>
**输出**：每个种群经过$B$步演化后的候选集合$\mathcal{S}_{B}^{(k)}$，以及记录算子、父技能、提案和收益的演化历史$\mathcal{H}^{(k)}$。

</div>

**直观理解**：不同算子类似不同修改方式，例如强化核验、修补常见错误或重组多份策略；系统会把更多尝试分给历史上有效的修改方式，同时保留对较少尝试方式的探索。若现有修改方式覆盖不了反复出现的问题，模型还会根据历史设计新的修改方式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 验证集上的互补技能联合选择

先按单技能验证表现保留各种群的少量优良候选，再以完整的“多技能生成加模型排序”管线评估技能集合，并按边际验证收益贪心构造$\mathcal{S}_{\mathrm{final}}$。集合大小满足$1\leq|\mathcal{S}_{\mathrm{final}}|\leq M$，且每个种群至多贡献一个技能，以促进跨种群互补。

<div class="method-step__io" markdown="1">

**输入**：所有种群的候选技能并集$\mathcal{C}=\bigcup_{k=1}^{K}\mathcal{S}_{B}^{(k)}$、共享验证集$\mathcal{D}_{\mathrm{val}}$和最大技能数$M$。<br>
**输出**：固定的最终技能集合$\mathcal{S}_{\mathrm{final}}$。

</div>

**直观理解**：这里不是简单挑出分数最高的$M$份规程，因为高分规程可能都擅长同类题、也犯同类错误。联合选择关注“加入这份技能后，整个候选答案系统能否多做对一些题”，因此直接优化组合价值。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 演化算子的UCB分配与相对收益

$$
\operatorname{UCB}_{a}(t)=\widehat{\mu}_{a}(t)+\beta\sqrt{\frac{\log t}{N_{a}(t)}},\quad \widehat{\mu}_{a}(t)=\frac{1}{N_{a}(t)}\sum_{\tau<t:\,a_{\tau}=a}R_{\tau},\quad R_{\tau}=U(s^{\prime}_{\tau})-\max_{s\in\mathcal{P}_{\tau}}U(s),\quad a_t=\arg\max_{a\in\mathcal{A}}\operatorname{UCB}_{a}(t)
$$

**符号说明**

- $\operatorname{UCB}_{a}(t)$：步骤$t$时演化算子$a$的上置信界分数。
- $\widehat{\mu}_{a}(t)$：算子$a$在步骤$t$之前取得的平均父技能相对收益。
- $N_a(t)$：步骤$t$之前算子$a$被选择的次数。
- $\beta$：控制探索强度的UCB系数；越大越偏向尝试使用次数较少的算子。
- $R_\tau$：步骤$\tau$产生的新技能相对其最佳父技能的正确率提升。
- $U(s)$：技能$s$在对应反思子集上的平均正确率。
- $s^{\prime}_{\tau}$：步骤$\tau$提出的新技能。
- $\mathcal{P}_{\tau}$：步骤$\tau$用于产生新技能的父技能集合。
- $\mathcal{A}$：当前可用的演化算子集合。
- $a_t$：步骤$t$实际选择的演化算子。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项衡量某算子过去平均能把父技能提高多少，第二项给尝试次数少的算子额外奖励；两者相加后取最大值，在利用已知有效操作与探索未知操作之间权衡。收益以“新技能减去最佳父技能”定义，可避免仅因父技能本来很强就高估某个算子。<br>
**原文位置**：方法章节“Adaptive Allocation with Upper Confidence Bounds”，公式(11)至(13)；相对收益定义亦见算法1第17行。

</div>

</div>

<div class="equation-block" markdown="1">

#### 最终技能集合的验证效用最大化

$$
\widehat{o}_{\mathcal{S}}(x)=\operatorname{SelectTop}_{f_{\theta}}\left(x,\{f_{\theta}(x;s)\}_{s\in\mathcal{S}}\right),\quad \widehat{V}_{\mathcal{D}_{\mathrm{val}}}(\mathcal{S})=\frac{1}{|\mathcal{D}_{\mathrm{val}}|}\sum_{(x,y)\in\mathcal{D}_{\mathrm{val}}}r\left(x,y,\widehat{o}_{\mathcal{S}}(x)\right),\quad \max_{\mathcal{S}}\widehat{V}_{\mathcal{D}_{\mathrm{val}}}(\mathcal{S})\ \text{s.t.}\ \mathcal{S}\subseteq\bigcup_{k=1}^{K}\mathcal{S}_{B}^{(k)},\ 1\leq|\mathcal{S}|\leq M,\ |\mathcal{S}\cap\mathcal{S}_{B}^{(k)}|\leq1\ \forall k\in[K]
$$

**符号说明**

- $\mathcal{S}$：待评价或待选择的技能集合。
- $f_{\theta}(x;s)$：冻结模型在问题$x$和技能$s$条件下生成的候选答案。
- $\widehat{o}_{\mathcal{S}}(x)$：模型从技能集合$\mathcal{S}$产生的候选中选出的最高排名答案。
- $\operatorname{SelectTop}_{f_{\theta}}$：由同一冻结模型执行的候选答案排序与选择过程。
- $\widehat{V}_{\mathcal{D}_{\mathrm{val}}}(\mathcal{S})$：技能集合$\mathcal{S}$经过生成和排序后在验证集上的经验正确率。
- $\mathcal{D}_{\mathrm{val}}$：只用于最终技能组合构造的共享验证集。
- $r$：依据标准答案判断最终响应是否正确的二元验证器。
- $\mathcal{S}_{B}^{(k)}$：第$k$个种群经过预算$B$步演化后的候选技能集合。
- $K$：独立技能种群的数量。
- $M$：最终技能集合允许包含的最大技能数。

<div class="equation-explanation" markdown="1">

**直观理解**：目标直接衡量整套测试管线：多个技能先生成答案，模型再选一个，最后由验证器判断是否正确。因此，某技能是否值得加入取决于它给现有集合带来的边际增益；每个种群至多选一个技能的约束进一步减少高度相似候选。<br>
**原文位置**：方法章节“Joint Skill Set Selection”，公式(15)至(17)；测试时对应公式(18)。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该方法没有参数训练目标，也不对$\theta$执行梯度更新；更准确地说，它进行两层离散、黑盒优化。种群内部以反思子集上的平均正确率$U(s)$评价自然语言技能，用父技能相对收益$R_t$更新UCB，从而决定后续把演化预算分给哪些算子；种群之间则在独立自助样本和随机修订下并行搜索，以降低单条非凸搜索轨迹的方差。演化结束后，系统在独立的$\mathcal{D}_{\mathrm{val}}$上最大化完整生成—排序管线的经验正确率，并通过集合大小和每种群至多一个技能的约束选择互补组合。因而所谓“自我改进”发生在持久化技能文本、算子策略和技能集合层面，而非模型权重层面；验证器只提供二元正确性及可能的结构化诊断，不提供自然语言教师批评。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 独立技能种群与自助经验**

DIVE维护$K$条独立演化路径；第$k$条路径分别使用$\mathcal{D}_{\mathrm{exp}}^{(k)}$初始化、使用$\mathcal{D}_{\mathrm{ref}}^{(k)}$演化，最终得到$\mathcal{S}_{B}^{(k)}$。种群之间优化相同任务目标，但不同的样本重采样、随机提案和修订轨迹形成不同归纳偏置。

> 直观理解：自然语言技能搜索是随机且非凸的，一条路径可能被偶然样本带偏或停在局部较优解。并行保留多个种群是在解空间中进行多次独立探索，最终利用各自擅长的题型和核验方式。

**2. 异构演化算子及自适应预算分配**

算子$a\in\mathcal{A}$规定父技能如何选择以及模型应执行何种结构化变换，因此定义了不同的技能提案核；算子选择采用“平均相对收益加探索奖励”的UCB分数。到预设步骤$t_{\mathrm{new}}$，模型读取历史$\mathcal{H}_{t_{\mathrm{new}}}$并生成新算子，使搜索操作本身也能针对未解决的失败模式调整。

> 直观理解：单一修订提示会限制可探索的改写方向；异构算子扩大搜索范围，UCB避免把预算平均浪费在低效算子上。动态新增算子则处理事先设计的修改方式没有覆盖到的问题。

**3. 面向完整推理管线的联合技能选择**

候选集合的效用不是各技能分数之和，而是各技能分别生成答案、再由$f_{\theta}$排序后所得最终答案的验证正确率$\widehat{V}_{\mathcal{D}_{\mathrm{val}}}(\mathcal{S})$。约束每个种群至多选择一个技能，并按边际效用贪心加入候选，使选择标准与测试时实际使用方式一致。

> 直观理解：单独最强的技能未必组成最强团队，因为它们可能高度重复；一个单独略弱但能解决其他技能共同失败样例的技能，可能带来更大组合收益。该模块因此选择互补集合，而不只是建立单技能排行榜。

**训练与推理**

开发阶段首先保留$\mathcal{D}_{\mathrm{test}}$仅供最终评价，并把其余开发数据分成$\mathcal{D}_{\mathrm{evo}}$与$\mathcal{D}_{\mathrm{val}}$。对每个$k=1,\ldots,K$并行自助采样$\mathcal{D}_{\mathrm{exp}}^{(k)}$和$\mathcal{D}_{\mathrm{ref}}^{(k)}$，由冻结模型在经验集上产生零样本轨迹，经验证器标注后初始化$\mathcal{S}_{0}^{(k)}$。随后执行$B$轮演化：未尝试算子优先各运行一次，此后按UCB选择$a_t$；算子从当前种群选择$\mathcal{P}_t$，模型读取父技能及其反思轨迹后采样$s'_t$，系统在反思集上计算其正确率和相对收益、更新算子统计与种群，并记录$\mathcal{H}^{(k)}$。在$t=t_{\mathrm{new}}$时，根据历史生成并加入$N_{\mathrm{new}}$个未尝试算子。完成所有种群后，在$\mathcal{D}_{\mathrm{val}}$上评价候选，先缩小各种群候选范围，再按照对$\widehat{V}_{\mathcal{D}_{\mathrm{val}}}$的边际提升贪心选择不超过$M$个技能，得到固定的$\mathcal{S}_{\mathrm{final}}$。

推理阶段不需要标准答案或验证器，也不更新技能。对于每个测试问题$x$，系统以$\mathcal{S}_{\mathrm{final}}$中的各技能分别调用一次冻结模型形成多个候选，再额外调用模型执行$\operatorname{SelectTop}_{f_{\theta}}$，根据推理、答案一致性和任务约束选出最终响应。该设计带来接近技能数的多候选推理开销，因此$M$同时控制潜在互补性和测试成本；$M=1$退化为单技能条件推理，较大的$M$则允许组合多个独立技能并增加排序调用。

**复现信息**

公平解释结果所需的关键设置是：数据必须严格分为演化、验证和测试三部分，$\mathcal{D}_{\mathrm{val}}$只用于演化完成后的集合构造，不反向触发种群内修订，$\mathcal{D}_{\mathrm{test}}$只用于最终报告；经验集与反思集需对每个种群独立自助采样。算法的主要资源参数包括种群数$K$、每个种群的演化预算$B$、UCB探索系数$\beta$、新增算子的时刻$t_{\mathrm{new}}$及数量$N_{\mathrm{new}}$、最终集合上限$M$；所给材料未明确报告初始算子的具体文本、种群保留容量、各数据划分比例、采样温度、贪心选择的精确停止规则或并列处理方式，因此复现时不能自行把这些细节视为原文设定。表1至表4中的主要DIVE多技能结果使用$M=10$；表4还明确给出$K=10$，但不能据此推断所有实验均固定$K=10$。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学竞赛与代数推理：HMMT 和 Equational Theories。原文将每个数据集划分为 evolution、validation 和 test 三部分：演化集的输入与标签用于技能初始化和优化；验证集仅用于评价候选技能并构造最终技能集合；测试集严格留出，只用于最终评价。各部分样本规模在所给章节中未明确报告。
- 数字约束与算术谜题：Sudoku、Cryptarithm 和 Calcudoku，用于检验模型能否形成可复用的约束传播、候选排除、算术一致性检查与输出格式控制策略。它们采用相同的演化集、验证集和测试集划分协议，但具体难度分布及样本规模原文未明确报告。
- 逻辑约束任务：Futoshiki，用于检验演化出的技能能否处理大小关系与行列唯一性等相互耦合的约束。该任务也采用三路数据划分；所给章节未说明数据来源、规模及不同棋盘尺寸的构成。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 多模型家族、六项数学与逻辑推理任务的总体比较

<div class="result-value" markdown="1">

作者报告 DIVE 在不更新参数的情况下跨模型家族和任务取得稳定的强表现，但所给摘录没有提供表 1 的具体分数、逐任务胜负情况或统计不确定性。

</div>

该结果支持自然语言技能可以充当冻结模型的持久化改进载体，而且结论并非只来自单一模型或单一题型。不过，“strong performance”是作者的总体概括；缺少表 1 数值时，不能确认提升幅度、所有设置是否均为最佳，也不能判断差异是否具有统计显著性。

<div class="result-source" markdown="1">

来源：Evaluation，Main Results，Table 1 的正文总结

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across model families and both mathematical and logical reasoning tasks, DIVE consistently achieves strong performance without parameter updates.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### DIVE 对经验记忆方法和提示优化方法

<div class="result-value" markdown="1">

作者称 DIVE 明显优于经验型、记忆型方法和提示优化方法；所给摘录未包含具体基线分数或绝对、相对提升幅度。

</div>

这一比较主要说明，把任务经验反复提炼为可修订技能，并维护多条候选演化轨迹，可能比直接检索旧经验、一次性构造技能或只优化一条提示轨迹更有效。但该结果同时改变了技能表示、搜索方式和候选选择机制，因而仅凭主结果不能把收益唯一归因于某一个组件。

<div class="result-source" markdown="1">

来源：Evaluation，Main Results，Table 1 的正文总结

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

DIVE also substantially outperforms experience- and memory-based methods and prompt optimization, showing the benefit of iterative skill evolution over one-shot skill construction and single-trajectory prompt optimization.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 多样化演化轨迹、异构修订策略与互补技能假设的整体作用

<div class="result-value" markdown="1">

作者认为整体实验结果支持在自我改进过程中同时保留多条演化轨迹、多种修订策略和互补技能候选；所给摘录未报告这些因素各自贡献的定量分解。

</div>

这项结论对应 DIVE 的核心设计假设：自然语言技能优化具有随机性且容易落入次优解，因此并行保留不同候选可以降低单条轨迹偶然失败的风险。它属于作者基于总体结果与消融作出的机制解释，并不等同于已经证明多样性是唯一因果来源。

<div class="result-source" markdown="1">

来源：Evaluation，Main Results，Table 1 后的作者总结

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

These results support the value of maintaining diverse evolution trajectories, heterogeneous revision strategies, and complementary skill hypotheses throughout the self-improvement process.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给评价摘录缺失表 1 和图 3、图 4 的数值内容，也没有明确评价指标、方差、置信区间或显著性检验。因此可以复述作者的定性结论，却无法核验提升幅度、跨随机种子的稳定性及计算成本是否公平匹配。
- 实验只说明技能在若干模型家族和六项结构化推理任务上有效；摘录没有提供开放式任务、分布外测试、技能错误累积、跨任务负迁移或对错误验证器的鲁棒性结果。因而现有证据支持特定数学与逻辑推理设置下的参数冻结自我改进，但不足以证明普遍的部署后持续学习能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 标准提示与推理时方法：ICL、Self-Consistency 和 Tree-of-Thought。它们分别代表从少量示例中学习、对多条推理轨迹进行投票，以及在推理时显式搜索思维分支，用于判断 DIVE 的收益是否超过单纯增加上下文或推理计算。
- 经验与记忆方法：Experience RAG 和 ExpeL。它们利用历史经验或检索记忆辅助新问题，因此是检验“直接保存并调用经验”与“将经验提炼为可修订的自然语言技能”之间差异的关键对照。
- 技能学习与提示优化方法：Direct Skill Generation、SkillOpt、MIPROv2 和 GEPA。前两者检验一次性生成或既有技能优化是否足够，后两者检验 DIVE 的多群体技能演化是否优于把改进过程压缩为提示优化。
- 参数更新方法：在 Qwen3-8B 上比较 SFT 和 GRPO，用于衡量冻结模型的技能演化与监督微调、强化学习式参数适配之间的样本或 rollout 效率差异。所给评价章节未提供训练预算、rollout 数量及具体结果。

**实验想回答的问题**

- 在模型参数完全冻结的条件下，DIVE 通过持续演化自然语言技能，能否在数学与逻辑推理任务上稳定优于标准提示、推理时搜索、经验记忆、技能学习和提示优化方法？
- DIVE 的效果是否确实来自多样化技能演化与互补技能选择，包括增加最终技能集合规模、采用多种演化算子以及自适应分配算子，而不只是单条技能轨迹或单一修订策略？

**实验实现**

实验覆盖 GPT-5-nano、DeepSeek-v4-flash 和 Qwen3.5，并称采用标准化推理设置；另在 Qwen3-8B 上开展参数适配对照及消融。数据隔离协议较严格：优化器可读取演化集的输入和标签；验证集样例不会进入技能生成或修订提示，只用于候选技能评价和最终技能集合构造；测试集仅用于最终评价。这一设计降低了把验证或测试题直接写入技能所造成的数据泄漏风险。DIVE 不更新模型参数，但所给章节没有列出解码参数、每题采样次数、技能演化轮数、计算预算、随机种子、显著性检验或具体评价指标，因此无法仅据该摘录判断不同方法是否使用完全等量的推理计算。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Qwen3-8B 上的 HMMT 与 Sudoku；技能群体数量固定为 $K=10$，改变最终技能集合大小 | 作者报告，纳入更多技能时性能总体提高，随后逐渐饱和；图注未给出各集合大小对应的具体分数。 | 该消融隔离了最终组合阶段的技能数量效应。上升趋势说明多个技能可能覆盖不同解题模式或失败类型，组合后比单一技能更稳健；饱和则表示新增技能的边际信息逐渐减少。由于图注没有数值，也未描述技能选择成本，因此不能确定最佳集合大小或性能与推理开销之间的权衡。 | Figure 3<br><span class="experiment-evidence">Performance generally improves as more skills are included and gradually saturates.</span> |
| Qwen3-8B 上的 HMMT 与 Sudoku；比较最佳单一演化算子、多算子均匀分配、多算子 UCB 分配，以及带算子生成的完整方法 | 图 4 明确列出四种演化策略作为对照，但所给摘录没有报告它们的排序、分数或提升幅度，因此无法给出定量消融结论。 | 这一消融旨在区分三层设计：使用多种变换是否优于单一变换，UCB 式自适应资源分配是否优于平均分配，以及自动生成新算子是否带来额外收益。它能更直接检验“异构且自适应的技能演化”是否必要，但缺少曲线或数值时只能确认实验设计，不能确认哪个组件实际贡献最大。 | Figure 4<br><span class="experiment-evidence">We compare the best single evolution operator, multiple operators with uniform or UCB-based allocation, and the full method with operator generation.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：DIVE enables frozen LLMs to self-improve mathematical and logical reasoning through evolving natural-language skills and verifier feedback.; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`a3423b8a9d913675fd4685dbcb55cff1e11989d17e06bafa6feba6e3b3a6ffe5`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
