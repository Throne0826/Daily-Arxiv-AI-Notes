---
title: "[论文解读] Answer Probing-Guided Search for Diverse Solution Exploration of LLMs"
description: "[arXiv 2608.30345][LLM Reasoning] 本文针对大语言模型在重复推理时容易收敛到同一解法、现有语义嵌入又难以识别真正不同推理路径的问题，提出以中间路径所导向的潜在答案作为探针，并据此兼顾解法多样性与质量的树搜索方法 APTS。"
arxiv_id: "2608.30345"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:31:47.618244+00:00"
source_sha256: "b908dec8926c6722323d927a2941d9a131bc0ec0ce2e941164f5d4507ac14069"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "多样化解答生成"
  - "测试时搜索"
  - "答案探测"
  - "树搜索"
  - "隐藏状态"
  - "困惑度"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.30345</p>

# Answer Probing-Guided Search for Diverse Solution Exploration of LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Yi Fang, Que Shen, Chengpeng Li, Boyi Deng, Wei Shi, Wenjie Wang, Fuli Feng, Fengli Xu, Dayiheng Liu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Science and Technology of China；Affiliation: Zhongguancun Academy；Affiliation: Alibaba Group；Affiliation: Shanghai Jiao Tong University；Affiliation: Tsinghua University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30345v1) · [PDF 下载](https://arxiv.org/pdf/2608.30345v1) · **关键词** 大语言模型, 多样化解答生成, 测试时搜索, 答案探测, 树搜索, 隐藏状态, 困惑度<br>


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

本文针对大语言模型在重复推理时容易收敛到同一解法、现有语义嵌入又难以识别真正不同推理路径的问题，提出以中间路径所导向的潜在答案作为探针，并据此兼顾解法多样性与质量的树搜索方法 APTS。

**不用术语来说**：许多任务需要的不是把同一个答案换几种说法，而是得到多条真正不同且可行的解决路线；例如，多样的代码测试可覆盖不同缺陷，多样的候选化合物可扩大药物发现的探索范围。然而，大语言模型即使被多次采样，也常反复采用最有把握的同一思路。现有方法还可能把措辞不同的同一路线误当成多样，或因写作结构相似而把实际不同的路线误判为重复，因此搜索过程难以保留真正有价值的备选解法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 Answer Probing：从每条中间推理路径继续探测模型可能得出的答案，并以探测答案的平均池化隐藏状态表征其潜在解题倾向，同时以探测答案的困惑度作为路径质量的代理信号。
- 提出 Answer Probing-Guided Tree Search（APTS）：在树搜索中联合使用探测答案之间的隐藏状态相似度与困惑度，优先扩展质量较高且彼此不冗余的节点，以提升解法层面的多样性并尽量维持正确性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型在推理阶段的多样化解答生成：对于同一问题，目标不是只得到一个高置信答案，而是探索多条彼此实质不同且仍然有效的推理路径，从而形成一组高质量候选解。这类能力适用于代码测试生成、药物发现等需要覆盖多种可能性的任务。现有生成侧方法主要包括两类：温度采样、核采样等解码方法通过扰动词元概率增加表面变化；树搜索方法则同时保留多个中间推理分支，并借助语义嵌入删除相似分支。本文关注后者，并指出回复级语义嵌入容易受到措辞、结构和写作风格的干扰，未必能识别推理路径最终会导向哪个答案。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时多样化生成**

在不重新训练模型的情况下，通过改变推理阶段的解码或搜索过程，使同一输入产生多个候选结果。本文要求候选之间不仅文本不同，而且采用不同的解题思路或导向不同的有效答案。

</div>
<div class="concept-item" markdown="1">

**树搜索**

把尚未完成的推理前缀视为树节点，对选中的节点继续生成若干后续步骤，并周期性剪除价值较低或彼此冗余的分支。它能够显式维护多条候选路径，但效果取决于节点质量与多样性的判断信号。

</div>
<div class="concept-item" markdown="1">

**隐藏状态、语义嵌入与困惑度**

隐藏状态是模型处理词元时形成的内部向量表示，语义嵌入则通常把一段完整文本压缩为用于比较语义相似性的向量；困惑度衡量模型对一段生成文本的不确定程度，越低通常表示该文本在模型看来越自然或越可信。本文使用探测答案的隐藏状态表示潜在解答倾向，并把其困惑度作为路径质量的近似信号，但困惑度并不等同于事实正确性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个需要推理的问题以及一个可在推理阶段继续生成文本并读取内部隐藏状态的大语言模型；搜索过程从同一问题出发，维护若干未完成的中间推理路径。对于每条候选路径，系统临时探测模型可能到达的答案，以探测答案隐藏状态之间的相似度判断不同路径是否可能收敛到同一解，并以探测答案的困惑度近似判断路径质量；随后保留既有潜力又不冗余的节点继续扩展。最终输出是同一问题的一组完整候选解答，核心要求是在尽量维持正确性的同时提高解答路径或最终解的实质多样性。该设置属于固定提示下的生成侧、测试时方法，不依赖额外训练；原文摘要与引言未给出输入输出变量的正式符号化定义。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Tree of Thoughts（Yao et al., 2023）**: 它代表以树结构探索多个中间思考分支的搜索式推理框架，为本文的多分支测试时搜索提供直接背景；本文的区别不在于首次采用树搜索，而在于使用答案探测产生的质量与多样性信号来选择节点。
- **Certaindex（Fu et al., 2025）**: 该工作同样在推理中途提取潜在答案，但主要用于估计确定性和提前停止；本文把中途答案进一步用于两种目的，即以隐藏状态相似度刻画不同路径的潜在解答倾向，并以答案困惑度近似评估路径质量。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

代码测试生成、药物发现等应用需要一组高质量且覆盖不同可能性的候选结果，而非单个标准答案。大语言模型在推理阶段却倾向于沿单一高置信轨迹收敛；即使执行多次采样，也可能反复产生本质相同的解法，缩小候选集合的覆盖范围，并降低后续测试、筛选或专家决策的价值。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于解码的随机采样**：温度采样、核采样等方法调整下一个词元的采样分布，通过增加生成随机性获得不同文本序列。其干预发生在词元选择层面，实施简单且无需额外训练。
- **基于语义嵌入的搜索**：束搜索、Tree of Thoughts 等方法在每个推理步骤生成多条候选分支，再利用完整响应或推理文本的语义嵌入计算相似度，剪除被判定为相近的分支，保留看起来更不相似的节点继续扩展。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 随机解码主要制造词元和表述层面的变化，却不能保证底层推理策略发生变化；结果可能是文本看似不同，实际仍沿用同一条解题路线，因而无法可靠提高真正的解法多样性。
- 响应级语义嵌入容易受到共同的推理提示语、篇章结构和写作风格干扰：真正不同的路径可能因表面形式相似而在嵌入空间中过近，导致搜索错误剪枝；相反，仅措辞不同的同一路径也可能被保留，从而浪费有限的搜索预算。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有测试时方法缺少一种能够在中间推理阶段直接表征“该路径最终倾向于导向什么答案”的信号，并且还需要在同一评估机制中判断路径是否值得继续扩展。换言之，尚缺少一种较少受语言风格噪声影响、同时提供解法差异与潜在正确性信息的路径表示，以支持有效剪枝。

</div>
<div markdown="1"><span>核心问题</span>

能否从每条尚未完成的推理路径中探测模型当前可能到达的答案，再利用该答案的内部隐藏状态衡量不同路径的解法差异、利用其困惑度估计路径质量，从而引导树搜索保留既有希望又不重复的分支？

</div>
<div markdown="1"><span>作者直觉</span>

中间推理文本记录的是“怎么说、走到了哪里”，其中包含大量共享模板和行文习惯；探测答案则更接近“沿这条路最终会得到什么”。因此，两条路径即使写法相似，只要趋向不同答案，其探测答案的隐藏状态仍可能显现差异；反之，表述不同但最终倾向一致的路径会更容易被识别为冗余。与此同时，若模型能以较低困惑度生成某个探测答案，说明它对该路径导向的结果相对更有把握，因而可作为筛选路径的实用质量线索，但这种自我置信并不等同于真实正确性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

APTS（Answer Probing-Guided Tree Search）是一种无需训练、在推理阶段运行的广度优先树搜索方法。输入是问题 $p$ 和期望生成的答案数量 $M$；搜索树中的每个节点保存一条尚未完成的中间推理路径 $r$。对每个候选节点，方法临时追加答案诱导提示 $[0m$$π_{\text{ans}}$$[0m$，用贪心解码得到“如果现在必须作答，模型会给出什么答案”。该探测答案的平均隐藏状态 $H(r)$ 用来判断候选路径是否通向不同解法，而探测答案的困惑度 $\mathrm{PPL}$ 用来估计路径质量。随后，算法以加权节点价值在正确性与多样性之间折中，每层保留 $M$ 个候选，直至达到最大深度 $D$ 或所有路径均已完成。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始化推理树

从问题 $p$ 独立采样 $M$ 个初始推理步骤，构成第零层节点集 $\mathcal{N}^{(0)}=\{n_1^{(0)},\ldots,n_M^{(0)}\}$；每个节点对应一条部分生成的响应。

<div class="method-step__io" markdown="1">

**输入**：问题 $p$、目标响应数 $M$，以及待解码的语言模型。<br>
**输出**：包含 $M$ 条初始中间推理路径的节点集合 $\mathcal{N}^{(0)}$。

</div>

**直观理解**：可以把它理解为先让模型提出 $M$ 个不同的解题开头，而不是一开始就押注于单一路线。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按推理步骤扩展候选节点

每个节点继续采样 $W$ 个子节点，得到包含 $MW$ 个元素的候选集 $\mathcal{C}^{(d+1)}$；节点以两个换行符分隔推理步骤。

<div class="method-step__io" markdown="1">

**输入**：当前深度 $d$ 的保留节点集 $\mathcal{N}^{(d)}$ 和扩展宽度 $W$。<br>
**输出**：下一层尚未筛选的候选推理路径集合 $\mathcal{C}^{(d+1)}$。

</div>

**直观理解**：每条现有路线都向前试走 $W$ 种可能的下一步，因此算法有机会发现后续才开始分化的解法。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 对候选路径执行答案探测

构造上下文 $c=p\oplus r\oplus\pi_{\text{ans}}$，再以贪心解码生成短探测答案 $PA$；对其词元隐藏状态取平均得到 $H(r)$，并计算该答案在上下文中的 $\mathrm{PPL}$。

<div class="method-step__io" markdown="1">

**输入**：候选路径 $r$、原问题 $p$ 和答案诱导提示 $\pi_{\text{ans}}$。<br>
**输出**：每个候选节点的路径表示 $H(r)$ 与质量信号 $1/\mathrm{PPL}$。

</div>

**直观理解**：算法像是在解题中途追问模型“照这条路走，你最终会答什么”。答案内容所对应的内部状态揭示路线终点，而回答是否自信则粗略反映当前路线是否可靠。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 质量—多样性联合选择与终止

执行 $M$ 轮贪心选择：每轮计算剩余候选的节点价值，用逆困惑度奖励高质量路径，并用其与 $\mathcal{S}$ 中最相似节点的负余弦相似度奖励差异；选取得分最高者加入 $\mathcal{S}$。令 $\mathcal{N}^{(d+1)}=\mathcal{S}$ 并继续扩展，直到深度达到 $D$ 或当前所有节点均已给出最终答案。

<div class="method-step__io" markdown="1">

**输入**：全部候选的 $H_i$、$\mathrm{PPL}_i$、折中系数 $\alpha$，以及初始为空的已选集合 $\mathcal{S}$。<br>
**输出**：至多 $M$ 条经过质量约束且彼此具有差异的完整响应。

</div>

**直观理解**：这相当于组建一个候选解法队伍：既不能只选看起来新奇但不可信的路线，也不能选一批高度可信却几乎相同的路线。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 答案探测的路径表示与质量信号

$$
\begin{aligned} c&=p\oplus r\oplus\pi_{\mathrm{ans}},\\ PA&=\operatorname{LLM}(c)=(a_1,a_2,\dots,a_L),\\ H(r)&=\frac{1}{L}\sum_{i=1}^{L}h_i,\\ \mathrm{PPL}(PA)&=\exp\!\left(-\frac{1}{L}\sum_{i=1}^{L}\log p_{\theta}(a_i\mid c,a_{<i})\right). \end{aligned}
$$

**符号说明**

- $p$：待求解的原始问题。
- $r$：某个搜索节点所保存的部分响应，即中间推理路径。
- $\pi_{\mathrm{ans}}$：促使模型立即给出最终答案的提示，例如“The final answer is”。
- $\oplus$：文本序列拼接操作。
- $c$：由问题、中间路径和答案诱导提示拼接得到的探测上下文。
- $PA$：模型基于探测上下文贪心生成的探测答案。
- $a_i$：探测答案中的第 i 个词元。
- $L$：探测答案的词元长度。
- $h_i$：模型生成词元 $a_i$ 时对应的隐藏状态。
- $H(r)$：探测答案隐藏状态的均值，用作中间推理路径 r 的表示。
- $p_{\theta}$：参数为 θ 的语言模型给出的条件词元概率。
- $a_{<i}$：探测答案中位于第 i 个词元之前的全部词元。
- $\mathrm{PPL}(PA)$：探测答案在当前路径条件下的困惑度；数值越低表示模型越有把握。

<div class="equation-explanation" markdown="1">

**直观理解**：该组公式先让模型从半成品推理直接预测终点，再从同一次探测中提取两个互补信息：$H(r)$ 描述路径可能通向哪类答案，$\mathrm{PPL}$ 描述模型对该终点有多确定。作者将低困惑度视为推理质量的代理信号，而不是经过外部验证的正确性证明。<br>
**原文位置**：第3.1节 Answer Probing

</div>

</div>

<div class="equation-block" markdown="1">

#### 质量与多样性联合节点价值

$$
\begin{aligned} V(c_i^{(d+1)})&=(1-\alpha)\cdot\frac{1}{\mathrm{PPL}_i}+\alpha\cdot DS_i,\\ DS_i&=\begin{cases}0,&\text{if }\mathcal{S}=\emptyset,\\-\max\limits_{c_j\in\mathcal{S}}\cos(H_i,H_j),&\text{otherwise}.\end{cases}\end{aligned}
$$

**符号说明**

- $c_i^{(d+1)}$：搜索深度 d+1 上的第 i 个候选节点。
- $V(c_i^{(d+1)})$：候选节点的联合选择价值，越大越优先被保留。
- $\mathrm{PPL}_i$：候选节点 i 的探测答案困惑度。
- $\alpha$：质量与多样性的折中系数，取值范围为 [0,1]。
- $DS_i$：候选节点 i 相对于当前已选集合的多样性得分。
- $\mathcal{S}$：当前选择阶段已经贪心选中的节点集合。
- $c_j$：已选集合中的一个节点。
- $H_i$：候选节点 i 的探测答案平均隐藏状态。
- $H_j$：已选节点 j 的探测答案平均隐藏状态。
- $\cos(H_i,H_j)$：两个探测答案隐藏状态表示之间的余弦相似度。
- $d$：当前树搜索深度。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项偏爱低困惑度、即模型更有信心的路径；第二项取候选与已选路线中“最像的那一条”的相似度并加负号，因此越不相似得分越高。首次选择时 $\mathcal{S}$ 为空，多样性项为零，所以先选质量较高的锚点；之后再围绕它补充不同路线。<br>
**原文位置**：第3.2节 Answer Probing-Guided Tree Search

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。APTS不是通过梯度下降学习的新模型，也没有额外训练损失；它冻结并调用现有LLM，在测试时根据探测答案的隐藏状态和困惑度重排搜索节点。公式中的 $V$ 是逐层贪心选择准则，而非用于反向传播的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 答案探测器**

它不直接用部分响应的表面语义表示路径，而是追加 $\pi_{\text{ans}}$ 并强制模型从当前路径生成探测答案。路径表示由探测答案各词元的隐藏状态均值构成；生成采用贪心解码，以避免采样随机性污染表示和困惑度。

> 直观理解：两段中间推理可能措辞相近，却最终导向不同答案；直接观察它们“准备给出的答案”比比较当前文字更容易识别这种实质差异。

**2. 双信号节点评估器**

质量信号为 $1/\mathrm{PPL}_i$，表示模型从当前路径生成探测答案的置信程度；多样性信号 $DS_i$ 是候选与已选节点中最高余弦相似度的相反数。系数 $\alpha\in[0,1]$ 控制二者权重：$\alpha=0$ 时仅按质量选择，$\alpha$ 增大时更强调路径差异。

> 直观理解：困惑度负责排除模型自己也拿不准的分支，隐藏状态相似度负责避免重复探索同一种解法；两者分别回答“是否可能正确”和“是否足够不同”。

**3. 多样性感知的广度优先搜索**

搜索在每一深度同时维护 $M$ 条路径，每个父节点产生 $W$ 个子节点，再从 $MW$ 个候选中逐个贪心选回 $M$ 个。逐个选择而非一次独立排序很关键，因为候选的多样性得分取决于此前已经选入 $\mathcal{S}$ 的节点。

> 直观理解：普通束搜索容易让多条分支集中到同一高概率答案；这里每选入一条路线，后续与它相似的路线都会受到惩罚，从而把有限搜索预算分配给不同方向。

**训练与推理**

完整过程仅发生在推理阶段。给定 $p$ 后，先采样 $M$ 个初始节点；每一层将保留节点各扩展 $W$ 次，对所有 $MW$ 个候选执行答案探测并计算 $H_i$ 与 $\mathrm{PPL}_i$，再按联合价值执行 $M$ 轮贪心选择。所选集合成为下一层节点集，循环直至达到最大深度 $D$ 或所有保留节点已经输出最终答案，最终返回这些完成响应。答案探测本身采用贪心解码，但树节点扩展仍使用采样，因此前者提供稳定评估信号，后者负责产生可供探索的不同分支。

**复现信息**

论文主要设置为每题返回 $M=16$ 个响应；对Diverse Beam Search、SemDiD和APTS统一使用采样温度 $T=1.0$，APTS采用扩展宽度 $W=4$、最大深度 $D=15$ 和折中系数 $\alpha=0.7$。推理步骤以“$\n\n$”分隔。由于每个候选都需要额外生成探测答案，APTS存在计算开销；实现利用共享树前缀的KV缓存，并将大量短扩展与短探测批处理，以避免为相同前缀重复计算。隐藏状态信号要求能够访问模型内部表示，因此标准版本面向开放权重模型；论文对闭源模型的适配改用语义嵌入和语义熵，但这不是核心APTS配置。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 多解 Game of 24 数据集：来自 4nums.com，共 204 道题，每道题至少包含 4 个解法类别；解法类别按底层数学逻辑划分，表面形式不同但逻辑等价的表达式会合并。该数据集用于表示空间的诊断分析，并评估数学解答的正确性与解法覆盖率。原文报告每道题从 Qwen3-8B 采样 $N=512$ 个响应。
- TestCaseGen：代码单元测试生成任务，目标是为给定代码生成可执行且断言正确的测试，从而覆盖不同程序行为和边界情况。原文摘录未明确报告该数据集的规模、训练验证测试划分或具体样本构造；其作用是检验 APTS 在代码领域的正确性、行覆盖和分支覆盖。
- Forward Synthesis 与 LiveIdeaBench：Forward Synthesis 要求根据反应物和试剂生成多个可能产物，用于检验化学有效性与化学空间探索；LiveIdeaBench 要求根据精心设计的关键词生成科学想法，用于检验 APTS 在没有明确“解法类别”的开放式生成中的泛化。原文摘录未明确报告 Forward Synthesis 的规模与划分；LiveIdeaBench 每个关键词生成 16 个想法，但其完整规模未报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**解法可分性 AUROC**

将同一解法类别的响应对视为正例、不同类别的响应对视为负例，以表示之间的余弦相似度区分二者；AUROC 越高，表示越能识别解法层面的差异。 （越高越好，因为高值意味着同类与异类解法的相似度排序更容易被正确区分。）

</div>
<div class="metric-item" markdown="1">

**数学与代码质量—多样性指标组**

$Acc@16$ 衡量 16 个响应的平均正确性；$Cov@16$ 衡量覆盖的全部数学解法类别；代码任务中的 $L$-$Cov@16$ 和 $B$-$Cov@16$ 分别衡量所有正确测试达到的行覆盖率与分支覆盖率。 （$Acc@16$、$Cov@16$、$L$-$Cov@16$ 和 $B$-$Cov@16$ 均越高越好，但正确性指标与多样性指标应联合解释，不能仅凭覆盖率判断答案质量。）

</div>
<div class="metric-item" markdown="1">

**化学质量—多样性指标组**

$Conf@16$ 使用 RXNMapper 置信度评价生成产物质量；$NCircle@16$ 计算生成分子中任意两者 Tanimoto 相似度不超过 0.75 的最大子集规模，以衡量探索到的化学空间范围。 （两者均越高越好：前者表示产物映射或化学有效性更可信，后者表示在去除高度相似分子后仍保留更多不同产物。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Game of 24 表示可分性：Qwen3-8B，四种响应/答案表示比较

<div class="result-value" markdown="1">

答案级表示整体显著优于响应级表示：附录 B 报告答案级表示相对响应级表示的平均优势为 0.36，平均 AUROC 为 0.94 对 0.58；表 2 的具体结果为 $RespSem=0.57$、$RespHid=0.58$、$AnsSem=0.95$、$AnsHid=0.92$。这说明完整响应的语言和格式相似性会掩盖解法差异，而截取最终答案区域更容易暴露解法类别信息。

</div>

作者的证据支持“答案级表示更适合区分最终解法类别”，但不能据此断言答案级语义表示在所有推理过程判别任务中都优于隐藏状态。表 2 中 $AnsSem$ 的类别 AUROC 高于 $AnsHid$，而论文进一步主张 APTS 中 $AnsHid$ 更适合区分中间推理差异；这两个结论针对的判别对象不同，不能混为一个指标上的全面优胜。

<div class="result-source" markdown="1">

来源：第 2.2 节；附录 B 表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

using pairwise AUROC to measure solution separability, answer-level representations outperform response-level representations by 0.36 on average (0.94 vs. 0.58).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Game of 24 推理轨迹：语义空间与隐藏状态空间的累积前缀比较

<div class="result-value" markdown="1">

将每条响应截取为 10% 至 100% 的十个累积前缀后，隐藏状态轨迹显示不同解法从相近区域出发、随生成推进逐渐分离并最终到达不同终点；语义空间中的轨迹在大部分生成阶段高度重叠。层选择分析还指出第 32 层具有较强的类间分离和较高的聚类质量，因此主实验使用第 32 层。

</div>

该结果支持 APTS 在中间节点上使用隐藏状态答案探测，而不是只比较整段文本的语义向量：隐藏状态似乎更早保留了“将走向哪类答案”的信号。不过这是可视化和层间诊断得到的表示相关性证据，并未单独证明这些轨迹差异必然导致搜索质量提升。

<div class="result-source" markdown="1">

来源：第 2.3 节；图 3；附录 A 图 9

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Trajectories associated with different solutions originate from nearby regions and progressively diverge as generation proceeds, eventually reaching distinct endpoints.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 多任务与开放式生成：Game of 24、TestCaseGen、Forward Synthesis，以及 LiveIdeaBench

<div class="result-value" markdown="1">

论文摘要声称在两个 LLM、三个推理任务上，APTS 一致提升解答多样性；在 LiveIdeaBench 上，作者声称 APTS 在两个模型上持续提升多样性，同时质量达到最好或接近最好。可见摘录没有给出主实验表、模型名称、具体分数或基线间差值，因此不能从当前材料核验提升幅度，也不能判断每个任务上的质量—多样性权衡。

</div>

这组结果的实验设计覆盖数学、代码、化学和开放式科学创意，说明作者试图检验方法的跨领域稳健性；但所给章节只保留了结论性文字，缺少数值表格，故结论应视为作者报告而非已由当前证据完整复核的定量事实。开放式任务中质量和多样性由多个 LLM 评审以 1—10 分评分，也意味着结果可能受评审模型和主观评分协议影响。

<div class="result-source" markdown="1">

来源：附录 G；表 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 5, APTS achieves the best or near-best quality while consistently improving diversity on both models, suggesting that it is also effective for open-ended generation tasks beyond explicit multi-solution settings.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前所给实验摘录缺少主实验结果表、模型与基线的完整数值，因此无法核验“在两个 LLM 和三个任务上一致提升多样性”的提升幅度、统计稳定性以及质量是否有显著代价。
- APTS 的探索能力受候选生成覆盖范围限制；失败案例显示，当模型被平凡模式吸引或当前 $\alpha$ 不足以鼓励更广搜索时，许多有效解法仍不会被发现。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Repeated Sampling：在相同目标输出数量和解码设置下重复采样，是检验搜索方法是否比独立随机采样更能发现多样解的直接基线；原文摘录未提供其完整实现细节或数值结果。
- RespSem：对完整响应使用 Qwen3-Embedding-0.6B 得到的响应级语义嵌入，用于检验传统响应语义相似度是否足以识别不同解法路径。
- AnsSem：仅对最终答案片段使用 Qwen3-Embedding-0.6B 得到的答案级语义嵌入，用于区分“只看答案表面语义”和“利用模型答案隐藏状态”的作用。
- RespHid 与 AnsHid：分别对完整响应和最终答案片段的隐藏状态进行平均池化，用于构成表示层面的对照；其中 AnsHid 是 APTS 答案探测所采用的核心表示。原文摘录未明确报告主实验中所有搜索基线的完整列表。

**实验想回答的问题**

- 与完整响应的语义嵌入相比，答案片段的语义表示和隐藏状态是否更能区分具有不同数学逻辑的解法类别，并揭示推理轨迹的分化过程？
- 在数学、代码和化学的多解生成任务，以及开放式科学创意生成任务中，APTS 能否在保持解答质量的同时提升解的多样性；其隐藏状态、答案探测和搜索权衡机制是否确实发挥作用？

**实验实现**

预分析在 Game of 24 上对每题从 Qwen3-8B 采样 512 个响应。每个响应表示为 token 序列 $r_i=(t_{i,1},\dots,t_{i,T_i})$，并定位最终答案片段 $a_i=(t_{i,s_i},\dots,t_{i,e_i})$。研究比较四类表示：响应级语义嵌入 $RespSem_i$、答案级语义嵌入 $AnsSem_i$、响应级隐藏状态均值 $RespHid_i$ 和答案级隐藏状态均值 $AnsHid_i$；语义编码器是 Qwen3-Embedding-0.6B，隐藏状态取 Qwen3-8B 第 32 层。可视化先用二维 PCA 投影；轨迹分析则将响应按长度取 10% 至 100% 的十个累积前缀，并按解法类别求平均表示。可见的 APTS 算法以问题 $p$、目标响应数 $M$、扩展宽度 $W$、最大深度 $D$ 和权衡系数 $\alpha$ 为输入：先生成初始节点，再逐层为每个节点生成 $W$ 个下一步候选；对每个候选执行 Answer Probing，得到答案隐藏状态 $H_i$ 与答案困惑度 $PPL_i$；随后依据与已选候选的最大余弦相似度计算多样性分数，并用 $V(c_i)=(1-\alpha)/\mathrm{PPL}_i+\alpha DS_i$ 选择 $M$ 个节点，直到节点完成或达到最大深度，最后补全响应。原文明确报告 inverse-PPL 在实践中作为质量项使用，并在 Qwen3-8B 的三项任务上检查其分布；主实验完整解码配置、硬件设置和各基线参数在所给摘录中未全部报告。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 答案探测中的 inverse-PPL 质量项：三项任务上的数值分布检查 | Qwen3-8B 上 inverse-PPL 在 Game of 24、TestCaseGen 和 Forward Synthesis 的均值分别为 0.95、0.96 和 0.94，最小值分别为 0.87、0.88 和 0.85，最大值均为 1.00；原文据此认为该质量项在实践中集中且不会跨数量级变化。 | 这不是严格意义上移除组件的性能消融，而是对目标函数尺度和稳定性的敏感性检查。它说明固定的 $\alpha$ 可能在三个任务间具有可用的数值尺度，但没有证明 inverse-PPL 比其他质量指标更有效，也没有展示去掉该项后的多样性或正确性变化。 | 附录 D；表 4<br><span class="experiment-evidence">the actual inverse-PPL values used by APTS are tightly concentrated within roughly [0.85,1.00] across tasks, and do not vary by orders of magnitude.</span> |
| 失败案例中的搜索权衡与采样局限：$\alpha=0.7$ 的 Game of 24 | 对题目 [2, 6, 10, 12]，共有 9 个解法类别，APTS 只覆盖 3 类；对题目 [2, 2, 4, 6]，共有 5 类，但 16 个输出全部为同一表达式，因此只覆盖 1 类。作者将前者归因于当前 $\alpha$ 下多样性激励不足，并指出后者受到重复数字导致的平凡消去模式吸引，改变 $\alpha$ 也未必能引导模型探索其他解法。 | 这组案例揭示了 APTS 的边界：搜索器只能在模型实际生成的候选分支中选择，若候选本身没有包含稀有解法，答案探测无法凭空创造新路径；同时，单一强吸引模式可能压过隐藏状态相似度提供的多样性信号。因此提高搜索权重并不保证覆盖率必然上升。 | 附录 K；表 9；表 10<br><span class="experiment-evidence">For the problem [2, 6, 10, 12], there are 9 solution categories. As shown in Table 9, APTS covers only 3 of them, with the remaining 6 categories unexplored.</span> |

**定性案例**

- 题目 [2, 2, 4, 6] 有 5 个解法类别，但 APTS 的 16 个答案全部是 $6\times4+2-2$，利用了平凡的 $a\times b+c-c$ 消去模式。该案例说明 APTS 能重排和筛选候选，却受基础模型采样分布限制：当模型反复提出同一高概率模式时，隐藏状态多样性奖励不足以产生未被提出的替代解法。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper proposes a test-time tree-search method guided by answer probing to explore diverse LLM reasoning paths.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`b908dec8926c6722323d927a2941d9a131bc0ec0ce2e941164f5d4507ac14069`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
