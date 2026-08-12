---
title: "[论文解读] ThinkRetrieve: Retrieval-Augmented Reasoning Traces for Test-Time Scaling"
description: "[arXiv 2608.10928][LLM Reasoning] 本文针对大推理模型单纯延长思维链容易累积错误的问题，提出在每个推理步骤中动态检索并插入带有完整解法的相似例题，以外部过程性指导改善测试时扩展。"
arxiv_id: "2608.10928"
announcement_date: "2026-08-12"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:05:08.366151+00:00"
source_sha256: "3c0490a9fb69ea93ae50ef78000622b55f2e627d0ebdba097e97c5e006751310"
tags:
  - "LLM Reasoning"
  - "大推理模型"
  - "测试时扩展"
  - "思维链"
  - "检索增强推理"
  - "动态样例检索"
  - "上下文示例"
  - "程序性支架"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.10928</p>

# ThinkRetrieve: Retrieval-Augmented Reasoning Traces for Test-Time Scaling

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Vaibhav Singh, Soumya Suvra Ghosal, Sarvesh Gharat, Soumyabrata Pal, Ramasuri Narayanam, Dinesh Manocha</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Maryland, College Park；Adobe Research</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.10928v1) · [PDF 下载](https://arxiv.org/pdf/2608.10928v1) · **关键词** 大推理模型, 测试时扩展, 思维链, 检索增强推理, 动态样例检索, 上下文示例, 程序性支架<br>
**代码**: [https://github.com/itsvaibhav01/ThinkRetrieve](https://github.com/itsvaibhav01/ThinkRetrieve) · **项目页**: [https://itsvaibhav01.github.io/ThinkRetrieve/](https://itsvaibhav01.github.io/ThinkRetrieve/)

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

本文针对大推理模型单纯延长思维链容易累积错误的问题，提出在每个推理步骤中动态检索并插入带有完整解法的相似例题，以外部过程性指导改善测试时扩展。

**不用术语来说**：面对难题，让模型继续“多想一会儿”并不一定有用：如果它早期走错方向，后续推理可能只是在错误路径上反复延伸，最终变得更不确定或更偏离题意。本文要解决的问题是，如何在不重新训练模型的情况下，让模型在推理途中及时参考相似题目的正确解题过程，从而发现错误并调整方向。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出 ThinkRetrieve，将相似已解问题及其逐步解答动态插入大推理模型的思维轨迹；检索查询随中间答案更新，使测试时计算从无外部指导的连续自省转变为逐步的例题引导。
- 作者将方法效果归因于过程性脚手架，并通过答案熵与不确定性分析、逐题 help/hurt 分解、计算量匹配的自洽性比较以及答案差异检索控制，检验收益是否来自检索机制，而非额外生成计算或答案层面的重合。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大推理模型的测试时扩展研究。大推理模型通过在推理阶段投入更多计算、生成更长的思维链来处理数学和科学等多步任务，这种无需增加模型参数或重新训练的做法称为测试时扩展。然而，单纯延长推理轨迹可能使模型反复尝试、累积早期错误、提高答案不确定性，甚至偏离原问题。本文关注的关键背景是：如何在推理过程中动态引入外部指导，使新增的推理计算用于纠错和调整解题路径，而不只是延续模型自身已有的思路。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大推理模型（Large Reasoning Model, LRM）**

能够显式生成多步思维链，并通过增加推理阶段计算来改善复杂任务表现的语言模型。本文不改变这类模型的训练过程，而是在测试时干预其推理轨迹。

</div>
<div class="concept-item" markdown="1">

**测试时扩展（Test-Time Scaling, TTS）**

在模型参数保持不变的情况下，增加单个问题在推理阶段使用的计算量，例如生成更长的推理轨迹。顺序式测试时扩展通常依靠模型自我反思继续推理，但缺少外部信息时可能放大已有错误。

</div>
<div class="concept-item" markdown="1">

**检索增强与上下文示例**

检索增强是从外部语料库选取与当前输入相关的内容，并将其加入模型上下文；上下文示例则是供模型模仿或参考的示范。本文检索的不是孤立事实，而是包含题目及逐步解答的完整已解样例，用作程序性解题支架。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个待解的多步推理问题、一个能够生成显式推理轨迹的大推理模型，以及由“问题—逐步解答”对构成的外部样例库，目标是在不额外训练模型的测试时设置中生成正确的最终答案。标准顺序式测试时扩展只让模型在已有轨迹后继续自我反思；本文所研究的设置则允许模型在每个推理阶段产生中间答案，以该中间答案查询样例库，再将检索到的完整已解问题作为上下文示例插入当前思维轨迹。其基本假设是：与当前中间推理状态相关的已解样例能够提供可迁移的解题步骤，帮助模型发现已有错误、提炼关键做法并修正后续推理方向。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Sequential Test-Time Scaling / Budget Forcing（Muennighoff et al., 2025）**: 该方法通过控制或延长模型的推理轨迹来增加测试时计算，是本文的直接问题背景与比较对象。它主要改变模型“思考多久”，但不会在推理期间增加新的外部内容；本文则在延续推理时动态注入已解样例，改变模型“依据什么继续思考”。
- **Search-o1（Li et al., 2025）与 RAT（Wang et al., 2024c）**: 二者都把检索与推理过程交错执行，因此与本文同属动态检索增强推理。区别在于它们主要检索事实知识或利用检索信息修订思维步骤，而本文检索包含完整逐步推理轨迹的已解问题，目标是提供解题程序和类比示范，而非仅补充模型缺少的事实。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大推理模型通常通过增加推理时计算、生成更长的思维链来处理多步任务，但较长轨迹会出现不确定性上升、重复循环、偏离原问题和错误累积。其直接后果是：额外计算可能放大早期错误而不是纠正它，因此“思考预算更大”不能稳定转化为更高的答案准确率。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **顺序式测试时扩展**：模型先生成一段推理，再借助“重新想一遍”之类的自我反思提示继续扩展同一条思维轨迹，以更多生成长度换取潜在的推理改进；整个过程主要依赖模型自身已有状态，没有引入外部解题参照。
- **检索增强生成与动态知识检索**：传统检索增强生成和上下文学习通常在推理开始前检索一次文档或示例，随后使用固定上下文完成生成；Search-o1、RAT 等动态方法虽然会在思考过程中多次检索，但主要补充与当前问题相关的事实知识。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 顺序式测试时扩展缺少外部纠偏信号。当模型早期采用错误假设或解题路线时，后续自我反思仍可能沿用该路线，导致错误复合、思维漂移和性能随推理长度增加而下降。
- 已有检索方法未同时满足“推理过程中动态更新”和“提供完整解题程序”两个条件：一次性检索的内容不会随中间推理状态变化，而动态知识检索回答的是应使用什么事实，并未示范应如何逐步推导，因而难以充当过程性脚手架。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种面向大推理模型的测试时机制：它能够根据不断变化的中间推理状态反复检索结构上相关的已解问题，并把问题及逐步解法直接放入当前思维轨迹，使模型在推理途中获得可用于比较、诊断和纠偏的过程级参照。与此同时，还需区分这种机制的真实收益与单纯增加令牌、重复采样或检索到相同答案所带来的表面收益。

</div>
<div markdown="1"><span>核心问题</span>

在不更新模型参数的条件下，能否把由中间答案触发的相似已解例题检索嵌入每个思考步骤，使不同规模的大推理模型随着测试时思考预算增加而更稳定地提高准确率并降低答案不确定性；若能，这一改进是否确实来自动态的过程性示例引导？

</div>
<div markdown="1"><span>作者直觉</span>

人遇到卡住的难题时，通常不会只把原思路重复得更长，而会回忆一道相似题，比较两者的结构与步骤。完整例题同时提供“怎样分解问题、采用什么操作、如何得到结果”的轨迹；将它放入模型当前上下文，相当于给模型一个临时解题模板。由于检索查询来自最新中间答案，后续取回的例题还能随模型当前困惑而变化，从而帮助模型提炼可迁移步骤、识别自身推导中的冲突并改换路线。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ThinkRetrieve 是一种无需更新模型参数的检索增强测试时扩展方法。输入测试问题 $x_{\text{test}}$、带逐步解答的外部样例库 $\mathcal{E}$、大推理模型 $\pi_\theta$ 和思考预算 $B$ 后，系统让模型分段推理；每当一个推理步骤结束，就要求模型输出反映当前判断的中间答案 $y_t$，再将原问题与该答案共同编码为检索向量，从样例库中选出最相似的已解问题。检索到的问题及完整解法作为示例 $e_t$ 被直接插入思考轨迹，模型据此继续下一步，直至预算耗尽并生成最终答案 $y$。

技术上的关键不是给模型补充孤立事实，而是动态提供与当前解题状态相近的“解法示范”。普通顺序测试时扩展只是反复提示模型继续思考，已有错误可能在后续自我反思中被放大；ThinkRetrieve 则在每轮推理后引入外部参照，使模型有机会比较解题结构、发现中间结论与示例策略之间的冲突，并修正后续推理。整个过程形成交错轨迹 $\tau_k=(z_1,e_1,\ldots,z_k,e_k)$，其中模型推理与检索示例轮流进入上下文。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建并索引已解样例库

将每个问题与解答联合编码为稠密向量 $\mathbf{e}_j=\mathrm{Enc}(q_j,a_j)$，并建立支持最近邻搜索的向量索引。该步骤在处理测试问题之前完成，样例库与评测基准被声明为零重叠。

<div class="method-step__io" markdown="1">

**输入**：外部语料库 $\mathcal{E}=\{(q_j,a_j)\}_{j=1}^{N}$，其中 $q_j$ 是问题，$a_j$ 是对应的逐步解答；另给定预训练句子编码器 $\mathrm{Enc}$。<br>
**输出**：包含 $N$ 个预计算向量及其原始问题、解答文本的可检索样例索引。

</div>

**直观理解**：这相当于预先整理一本带完整解题过程的例题册，并为每道例题制作便于快速查找的语义标签。运行时不必逐条阅读整个例题库，只需搜索向量索引。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成当前推理步骤与中间答案

模型先生成第 $t$ 段推理 $z_t$；到达步骤边界后，框架关闭当前思考块并追加“Final Answer:”提示，使同一模型根据当前上下文生成中间答案 $y_t$。边界通常由模型提前产生的 `</think>` 停止标记触发；若模型持续生成而不自行停止，框架按固定词元间隔强制插入边界。

<div class="method-step__io" markdown="1">

**输入**：测试问题 $x_{\text{test}}$、此前形成的轨迹前缀 $\tau_{<t}$，以及尚未用完的思考预算 $B$。<br>
**输出**：当前推理片段 $z_t$ 和概括模型当前解题判断的中间答案 $y_t$。

</div>

**直观理解**：系统不会直接拿冗长且反复修改的草稿去搜索，而是先让模型说出“目前认为答案是什么”。这个短结论与原题一起更集中地表达了模型当前走到哪一步。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按当前判断检索结构相近的示例

系统计算查询向量 $\mathbf{q}_t=\mathrm{Enc}(x_{\text{test}},y_t)$，再以余弦相似度搜索全部样例向量，选择得分最高的条目 $j_t^*$。检索同时使用原题和中间答案，以兼顾问题结构与模型当前的求解状态。

<div class="method-step__io" markdown="1">

**输入**：原测试问题 $x_{\text{test}}$、中间答案 $y_t$，以及预先建立的样例向量索引。<br>
**输出**：最相似样例的编号 $j_t^*$，以及格式化后的示例 $e_t=[\text{Example: }q_{j_t^*}\ \text{Solution: }a_{j_t^*}]$。

</div>

**直观理解**：可以把它理解为根据“原题是什么”和“现在算到什么结果”共同查例题。这样找到的内容不仅主题相似，还可能针对模型正在采用或误用的解题路线。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 注入示例并继续推理

框架把 $(z_t,e_t)$ 追加到上下文，并插入固定的继续推理提示 $c$；模型随后在增强后的上下文上采样下一段推理 $z_{t+1}$。提示与示例均由外部框架插入，不要求模型自行生成触发短语或遵循额外输出格式。

<div class="method-step__io" markdown="1">

**输入**：已有轨迹 $\tau_{<t}$、当前推理 $z_t$、检索示例 $e_t$，以及要求利用示例继续思考的提示 $c$。<br>
**输出**：更新后的交错轨迹 $\tau_t=(z_1,e_1,\ldots,z_t,e_t)$，以及下一轮推理所需的上下文。

</div>

**直观理解**：模型每写完一段草稿，就在旁边看到一道相关例题及其完整解法，然后带着这个参照继续作答。示例提供的是推理路径，而不只是某个知识点。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 基于当前中间答案的示例选择

$$
\mathbf{q}_{t}=\mathrm{Enc}(x_{\mathrm{test}},y_t),\qquad j_{t}^{*}=\operatorname*{arg\,max}_{j\in\{1,\ldots,N\}}\mathrm{sim}(\mathbf{q}_{t},\mathbf{e}_{j}),\qquad \mathbf{e}_{j}=\mathrm{Enc}(q_j,a_j)
$$

**符号说明**

- $\mathbf{q}_t$：第 $t$ 步用于检索的稠密查询向量。
- $\mathrm{Enc}$：将文本对映射为稠密向量的预训练句子编码器。
- $x_{\mathrm{test}}$：当前待求解的测试问题。
- $y_t$：模型在第 $t$ 段推理后生成的中间答案，表示其当前解题判断。
- $j_t^*$：第 $t$ 步检索到的最高相似度样例编号。
- $N$：外部已解样例库中的条目总数。
- $\mathrm{sim}$：查询向量与样例向量之间的余弦相似度函数。
- $\mathbf{e}_j$：第 $j$ 个样例的问题 $q_j$ 与逐步解答 $a_j$ 的预计算联合向量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先把“原问题加当前暂定答案”压缩成一个语义向量，然后从例题库中挑选余弦相似度最高的条目。它体现了论文最关键的检索设计：检索目标会随模型的中间判断动态变化，而不是在开始推理前只根据原题检索一次。<br>
**原文位置**：第 3.2.1 节，公式（5）和公式（6）

</div>

</div>

<div class="equation-block" markdown="1">

#### 检索增强的递推推理与最终生成

$$
z_{t+1}\sim\pi_{\theta}\!\left(\cdot\mid x_{\mathrm{test}},\tau_{<t},z_t,e_t,c\right),\qquad y\sim\pi_{\theta}\!\left(\cdot\mid x_{\mathrm{test}},\tau_k\right)
$$

**符号说明**

- $z_{t+1}$：模型吸收第 $t$ 步检索示例后生成的下一段推理。
- $\pi_\theta$：参数为 $\theta$ 的大推理语言模型；本文推理过程中不更新这些参数。
- $\tau_{<t}$：第 $t$ 步之前由推理片段和检索示例交错组成的轨迹前缀。
- $z_t$：模型在第 $t$ 步生成的当前推理片段。
- $e_t$：第 $t$ 步检索并格式化后注入上下文的已解示例。
- $c$：由框架插入、要求模型利用检索示例继续推理的提示。
- $\tau_k$：预算结束时包含 $k$ 个推理片段和 $k$ 个检索示例的完整增强轨迹。
- $y$：根据测试问题和完整增强轨迹生成的最终答案。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分说明下一段推理不仅依赖原题和旧草稿，还明确依赖刚检索到的示例与继续推理提示；第二部分说明最终答案以整条增强轨迹为条件生成。换言之，检索结果不是独立的旁路信息，而是直接进入模型后续推理上下文。<br>
**原文位置**：第 3.2.1 节，公式（8）和公式（9）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。ThinkRetrieve 是纯测试时框架，原文没有提出新的训练损失、微调过程或参数优化目标；大推理模型 $\pi_\theta$ 与句子编码器 $\mathrm{Enc}$ 均作为已有模型使用，样例向量只进行离线计算和索引。方法改进来自推理时对上下文、检索时机和计算预算的组织，而非更新参数 $\theta$。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 中间答案驱动的查询构造**

原始推理片段 $z_t$ 可能包含试探、回溯和自我纠正，直接编码会引入语义噪声。因此，框架额外调用同一模型产生中间答案 $y_t$，再联合编码 $(x_{\text{test}},y_t)$，用较紧凑的当前判断表示检索意图。

> 直观理解：草稿中的很多句子只是尝试，不一定代表模型真正相信的结论。先提炼一个暂定答案，能让检索器更清楚地判断应该找哪类例题。

**2. 稠密最近邻样例检索**

预训练编码器把测试查询和样例的问题—解答对映射到同一向量空间，并以余弦相似度选择单个最高分样例。由于样例向量 $\mathbf{e}_j$ 已离线计算，在线阶段主要承担中间答案编码和最近邻查询。

> 直观理解：该模块按照整体语义和解题结构找相似内容，而不是只匹配相同关键词。它负责从大量例题中快速挑出当前最可能有帮助的一道。

**3. 交错式轨迹与步骤边界控制**

增强上下文以 $z_1,e_1,z_2,e_2,\ldots$ 的顺序增长；每个边界处由框架插入示例和提示 $c$。模型自然输出 `</think>` 时触发边界，连续生成型模型则使用固定词元间隔，因此该方法不依赖特定模型主动输出“Wait”或“Think more”等触发语。

> 直观理解：边界控制决定何时暂停模型、查一次例题并把结果放回上下文。框架主动管理这些操作，使不同模型都能采用同一套循环。

**训练与推理**

训练阶段：本文方法本身不训练大推理模型或检索编码器。部署前仅准备带逐步解答的样例库 $\mathcal{E}$，使用预训练编码器计算每个 $(q_j,a_j)$ 的向量 $\mathbf{e}_j$，并建立最近邻索引。

推理阶段：初始化空轨迹 $\tau$，让模型针对 $x_{\text{test}}$ 生成一段推理 $z_t$；在自然或强制步骤边界处，提示同一模型输出中间答案 $y_t$。系统编码 $(x_{\text{test}},y_t)$，检索余弦相似度最高的已解示例，将其问题和完整解法格式化为 $e_t$，再把 $(z_t,e_t)$ 追加到轨迹并提示模型继续。循环持续到预算 $B$ 耗尽，最后根据完整轨迹 $\tau_k$ 生成答案 $y$。这一过程只增加推理时的模型调用、上下文词元和检索开销，不发生梯度反向传播。

**复现信息**

公平解释或复现时需要注意四点。第一，样例库条目必须同时包含问题与逐步解答，且论文声明所用合成语料与评测基准零重叠；否则结果可能混入测试泄漏。第二，样例的问题—解答对与在线的原题—中间答案对必须由同一预训练句子编码器映射到可比较的向量空间，检索采用余弦相似度的稠密最近邻搜索。

第三，步骤边界优先使用模型自然产生的 `</think>` 标记；对于不会自行终止思考的模型，需要设定固定词元插入间隔，以保证周期性检索。第四，总预算 $B$ 同时覆盖模型生成内容和注入的示例词元，因此示例会占用上下文预算；步骤数 $k$ 并非预先固定，而由预算、自然终止频率和强制间隔共同决定。继续提示 $c$ 的精确模板位于原文附录 K，完整控制流程见附录 L 的算法 1；所给节选未提供固定插入间隔、样例库规模 $N$ 或编码器索引参数的具体取值。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学评测组包括 GSM-8K、MATH-500 和 AIME 2025。GSM-8K 含 8,788 道需要多步算术推理的小学数学应用题；MATH-500 是覆盖代数、几何、数论和组合数学的 500 道竞赛题子集；AIME 2025 含当年 30 道邀请赛题，代表奥赛级难度。三者分别测试从基础多步计算到高难竞赛推理的扩展行为，检索样例均来自经过去污染处理的 NuminaMath 样例库。
- SciQ 是选择题形式的科学问答基准，用于检验方法能否从数学推理迁移到不同领域和答案形式。实验以 SciQ 训练集作为检索样例库，并在同样五个模型、五种方法的设置下评测；原文未明确报告测试集在本实验中的具体样本数。
- 外部数学样例库取自 NuminaMath-1.5 的合成部分。作者先按合成标记、题目与解答长度及题型筛选约 60 万个候选，再进行精确匹配删除和 E5-Large 余弦相似度去污染，删除与任一测试题相似度大于 $0.90$ 的条目，最终保留 $N=309{,}609$ 个题目及逐步解答。该语料不是评测集，而是 ThinkRetrieve、静态输入级 ICL 和相关随机检索对照所使用的外部知识来源。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**最终答案准确率**

检查每个测试问题的模型最终答案 $y$ 是否与标准答案 $y^{*}$ 匹配，并计算正确样本比例。主表报告各思考预算中的最佳准确率，并对三个随机种子取平均。 （越高越好，因为它直接反映完整推理流程最终解决问题的比例；但只检查最终答案，不能单独证明中间推理过程完全正确。）

</div>
<div class="metric-item" markdown="1">

**预算下的准确率曲线**

考察准确率随思考预算 $B$ 增长的变化，用于识别额外测试时计算带来的增益、平台期或性能退化。图中结果对三个随机种子平均，并以最小值至最大值阴影表示波动。 （在更大 $B$ 下保持稳定或上升更好，因为这意味着方法能够有效利用新增预算，而不是因错误累积或过度反思而退化。）

</div>
<div class="metric-item" markdown="1">

**推理成本**

通过模型生成 token 数、检索与编码带来的墙钟时间开销衡量效率。样例 token 与模型生成 token 一样计入总预算 $B$，因此同预算比较不会把检索文本当作免费上下文。 （在准确率相当时，生成 token 和墙钟时间越少越好；在成本相近时，准确率越高越好。该指标用于判断提升是否来自额外计算，而非检索质量。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 五个模型在 GSM-8K、MATH-500 与 AIME 2025 上的最佳预算准确率

<div class="result-value" markdown="1">

作者报告 ThinkRetrieve 在表 1 的全部 15 个“模型—数学基准”组合中取得最高准确率。提升在接近饱和的 GSM-8K 上通常较小，而在 AIME 2025 上最大达到 $13.4$ 个绝对百分点；例如 Qwen3-1.7B 的 TTS 为 $22.2\%$，ThinkRetrieve 为 $35.6\%$。

</div>

该结果表明逐步相关样例检索在不同模型规模和数学难度下具有较一致的收益，且难题上的收益更明显。由于表 1 选择各方法跨预算的最佳准确率，它证明的是“可达到的最佳表现”占优，不能单独说明 ThinkRetrieve 在每一个固定预算点都以同样幅度领先，也不能证明所有未测试模型或任务都会受益。

<div class="result-source" markdown="1">

来源：第 4 节 Evaluation results，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ThinkRetrieve wins on every cell, with gains ranging from modest improvements on near-saturated benchmarks to over 13 absolute points on AIME 2025.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 随思考预算增长的测试时扩展行为

<div class="result-value" markdown="1">

在 AIME 2025 的 Qwen3-1.7B 设置中，顺序 TTS 在 $B=8\mathrm{K}$ 左右停留于约 $22\%$，增加到 $B=32\mathrm{K}$ 仍无明显改善，而 ThinkRetrieve 上升到 $35.6\%$，绝对领先 $13.4$ 个百分点。在 GSM-8K 的 DeepSeek-R1-Distill-Qwen-1.5B 设置中，顺序 TTS 在约 $B=22\mathrm{K}$ 时从 $83\%$ 降到 $52\%$，ThinkRetrieve 则维持约 $84\%$。

</div>

预算曲线比单个最佳分数更直接地检验测试时扩展是否稳定：顺序自我反思可能累积错误或偏离原题，而检索样例可作为推理参照，使额外预算更可能转化为有效计算。这里的“稳定或上升”是所测试预算、模型与随机种子下的经验现象，并不能证明单调性在任意更长预算下必然成立。

<div class="result-source" markdown="1">

来源：第 4 节 Evaluation results，图 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On GSM-8K, the effect is equally striking for DeepSeek-R1-Distill-Qwen-1.5B, where sequential TTS collapses from 83% to 52% at B=22K tokens while ThinkRetrieve remains stable at 84%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### SciQ 科学选择题上的跨领域验证与推理成本

<div class="result-value" markdown="1">

ThinkRetrieve 在 SciQ 的五个模型上均取得最高准确率：例如 DeepSeek-R1-Qwen-1.5B 从 TTS 的 $88.4\%$ 提升到 $90.5\%$，Qwen3-8B 从 $96.2\%$ 提升到 $96.8\%$。作者同时报告，在相同预算比较中 ThinkRetrieve 平均生成 $12{,}913$ 个模型 token，而顺序 TTS 生成 $15{,}847$ 个，仅增加约 $6\%$ 的墙钟时间。

</div>

SciQ 结果说明收益不限于 NuminaMath 支持的数学题，在改用 SciQ 训练集作为样例库后仍然存在；大模型接近任务饱和时，绝对提升相应缩小。成本结果削弱了“准确率只是因为生成更多 token”的解释，因为检索文本占用相同预算且实际模型生成量更少；不过墙钟开销来自特定模型、硬件与索引设置，不能直接外推到所有部署环境。

<div class="result-source" markdown="1">

来源：第 4 节 Key result；SciQ 准确率见表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Because injected exemplar tokens count against the budget but are not generated, ThinkRetrieve produces fewer model tokens than sequential TTS at the same budget (12,913 vs. 15,847), adding only ∼6% wall-clock overhead.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主表报告跨思考预算的最佳准确率，而非统一固定预算下的单一结果；这种汇总适合比较方法上限，但可能掩盖预算选择成本。AIME 2025 仅有 30 题，即使采用三个随机种子，单题变化也会造成较明显的百分比波动，原文摘录未提供置信区间或显著性检验。
- 作者通过相似度阈值、实际检索审计和答案不同过滤较充分地排查直接泄漏，但数学实验仍依赖大型合成 NuminaMath 语料，SciQ 则使用同任务训练集。现有实验尚不能确定在缺少高质量同领域逐步解答库、跨语言任务或开放式非结构化推理中是否保持同等收益；编码器和查询消融也主要集中于 MATH-500 的 Qwen3-1.7B 设置。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- ST（standard thinking，标准思考）：模型仅进行一次常规思维链生成，不执行顺序式扩展或样例注入。它给出模型原始推理能力的参照，用来判断增加测试时计算是否真正有益。
- TTS（sequential test-time scaling，顺序测试时扩展）：在更大思考预算下依靠模型继续生成和自我反思，不使用外部样例。这是最关键的比较对象，因为它控制了测试时预算，直接检验检索引导是否比单纯延长推理更有效。
- S-ICL（static input-level ICL，静态输入级上下文学习）：在推理开始前一次性向输入加入 $k=3$ 个语义检索样例，之后不再按步骤更新。它保留语义检索，但移除推理过程中的动态注入，用于检验检索时机与推理状态适配的作用。
- Rand（random per-step retrieval，随机逐步检索）：保留与 ThinkRetrieve 相同的逐步注入流程，但从语料库均匀随机选择样例。它控制注入位置和频率，同时移除语义相关性，用于判断收益是否只是额外上下文带来的。

**实验想回答的问题**

- 在相同推理预算下，逐步检索并注入已解样例的 ThinkRetrieve，能否比标准思考、顺序测试时扩展以及输入级检索更稳定地提升不同规模推理模型在数学与科学问答上的最终答案准确率，尤其能否缓解长推理导致的性能平台期或下降？
- 性能增益究竟来自哪些设计：推理过程中按步骤注入、与当前推理状态相关的语义检索，还是特定检索编码器、随机样例、答案泄漏等替代解释？

**实验实现**

实验覆盖五个处于思考模式的推理模型：DeepSeek-R1-Distill-Qwen-1.5B、Qwen3-1.7B、Qwen3.5-2B、Qwen3-4B 和 Qwen3-8B，参数规模为 1.5B 至 8B。除非另有说明，生成采用温度 $0.6$ 和各模型默认的 top-$p$ 采样；主表准确率使用相同的三个随机种子，以减少方法间随机解码差异。主要思考预算为 $B=22{,}528$ token，图中还比较多个预算点；检索样例本身也占用 $B$，所以 ThinkRetrieve 在相同预算下可用于模型生成的 token 更少。数学检索采用 E5-Large 编码与 FAISS 近邻索引；作者还通过精确匹配、相似度阈值和答案不同过滤控制数据泄漏。主表取每个模型与基准组合在所有预算中的最佳准确率，因此它适合比较各方法可达到的峰值，但不能替代固定预算下的逐点比较。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 静态输入级检索与随机逐步检索对照 | S-ICL 保留语义检索但只在开始前注入一次，Rand 保留逐步注入但移除语义相关性；两者在每个“模型—基准”组合上都低于完整 ThinkRetrieve。表 1 中，例如 Qwen3-1.7B 在 AIME 2025 上，S-ICL、Rand 和 ThinkRetrieve 分别为 $23.3\%$、$27.8\%$ 和 $35.6\%$。 | 这组对照分别隔离“动态注入”和“语义相关性”。S-ICL 较弱说明仅在输入端提供相关例题不能充分适配推理过程中不断变化的错误与子目标；Rand 较弱说明逐步插入任意长文本本身不足以解释收益。两项因素同时存在时效果最好，但该对照仍不是严格的因果析因实验，因为不同样例内容可能改变上下文长度和生成轨迹。 | 表 1，Qwen3-1.7B 行；第 4 节 Baseline ablations<br><span class="experiment-evidence">Qwen3-1.7B 91.2 90.3 90.3 90.7 92.1 90.2 91.0 89.8 90.2 92.5 24.4 22.2 23.3 27.8 35.6</span> |
| 检索查询构造：Q–Q 对比 QA–QA | 在 MATH-500、Qwen3-1.7B 设置中，默认 QA–QA 查询达到 $91.0\%$，只编码题目的 Q–Q 查询为 $90.2\%$。QA–QA 在检索端联合编码测试题和当前中间答案，并在语料端联合编码题目和解答。 | 该消融检验检索是否需要感知模型当前的推理状态。$0.8$ 个百分点的差异支持中间答案与样例解答有助于检索结构相似的解题策略，而不仅是表面相似题目；但实验只报告一个模型与一个基准，差距也较小，因此不足以证明这种查询构造在所有任务上都显著更优。 | 附录 J，图 7<br><span class="experiment-evidence">QA–QA achieves the highest accuracy (91.0% vs. 90.2% for Q–Q on MATH-500 with Qwen3-1.7B).</span> |

**定性案例**

- MATH-500 的概率题案例中，两种方法起初都得到错误中间答案 $1/6$。顺序 TTS 的重复自我反思未发现计数错误，最终仍确认 $1/6$；ThinkRetrieve 检索到结构相似的已解题后注意到遗漏的计数区别，将结果修正为 $2/6=1/3$。该案例直观展示检索样例如何提供模型自身轨迹中缺失的推理参照，但单个成功案例只能解释一种可能机制，不能估计这种纠错行为在整个测试集中的发生频率。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper improves LLM test-time reasoning by dynamically retrieving solved reasoning exemplars at intermediate chain-of-thought steps.; rule check: matched taxonomy keywords; top rule score=14.0
- 全文指纹：`3c0490a9fb69ea93ae50ef78000622b55f2e627d0ebdba097e97c5e006751310`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
