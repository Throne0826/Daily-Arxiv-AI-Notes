---
title: "[论文解读] SALA: Semantic-Aware Logical Alignment for Complex Reasoning in In-Context Learning"
description: "[arXiv 2609.02336][LLM Reasoning] SALA通过从下游数据中自动归纳任务特定的推理操作，并在连续语义空间中用动态时间规整对齐操作序列，从而为复杂推理的上下文学习选择逻辑上更匹配的示例。"
arxiv_id: "2609.02336"
announcement_date: "2026-09-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:27:48.444045+00:00"
source_sha256: "76b4b3084043d91f8474ab5f3ebd6a5e3562cd53f2e30142327d1d17f4eefe11"
tags:
  - "LLM Reasoning"
  - "上下文学习（ICL）"
  - "复杂推理"
  - "示例选择"
  - "语义逻辑对齐"
  - "动态时间规整（DTW）"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.02336</p>

# SALA: Semantic-Aware Logical Alignment for Complex Reasoning in In-Context Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> Zhao Ji, Wenqing Chen, Zhixuan Chu, Jianxing Yu, Jingping Liu, Shanhe Zhao, Zibin Zheng</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Software Engineering, Sun Yat-sen University, Zhuhai, China；Affiliation: Zhuhai Key Laboratory of Trusted Large Language Models, Zhuhai, China；Affiliation: The State Key Laboratory of Blockchain and Data SecurityZhejiang University, Hangzhou, China；Affiliation: School of Artificial Intelligence, Sun Yat-sen University, Zhuhai, China；Affiliation: Key Laboratory of Sustainable Tourism Smart Assessment TechnologyMinistry of Culture and Tourism, Zhuhai, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.02336v1) · [PDF 下载](https://arxiv.org/pdf/2609.02336v1) · **关键词** 上下文学习（ICL）, 复杂推理, 示例选择, 语义逻辑对齐, 动态时间规整（DTW）<br>


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

SALA通过从下游数据中自动归纳任务特定的推理操作，并在连续语义空间中用动态时间规整对齐操作序列，从而为复杂推理的上下文学习选择逻辑上更匹配的示例。

**不用术语来说**：大语言模型往往需要参考若干已解答的示例来解决新问题，但文字、主题或实体相似的示例不一定采用相同的解题思路；反过来，表述差异很大的问题也可能共享同一种推理过程。因此，关键困难是根据“怎么解题”而不是“题目看起来多像”来选择示例，同时还要容纳不同措辞、步骤数量和拆解方式。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出面向推理示例选择的SALA框架：将问题表示为显式的推理操作序列，再通过语义化的序列对齐度量其解题逻辑相似性，兼顾可解释表示与柔性匹配。
- 提出任务自适应的操作空间：从下游数据自动归纳可复用的任务特定操作，以补充预定义操作集合，并使用动态时间规整处理长度或拆解粒度不同的推理序列。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型（LLM）的上下文学习（ICL）示例选择问题。ICL不更新模型参数，而是在输入问题前提供少量带标签的示例，使模型据此完成新任务；对于复杂推理，示例是否展示了与目标问题相容的解题逻辑，往往比表面词汇或主题相似性更重要。因此，本文关注如何将示例表示为可解释的推理操作序列，并据此检索适合目标问题的示例。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**上下文学习（In-Context Learning, ICL）**

ICL是在不重新训练模型的情况下，把若干输入—输出示例放入提示词，让模型根据这些示例解决新的输入。示例选择会影响模型能否识别任务规则以及采用合适的推理方式。

</div>
<div class="concept-item" markdown="1">

**问题求解逻辑（Problem-Solving Logic, PSL）**

问题求解逻辑是完成一个问题时所经历的中间推理步骤，例如先筛选对象、再进行比较或计算。本文不只比较问题的主题，而是比较这些步骤的组织方式，以判断两个示例是否适合相互指导。

</div>
<div class="concept-item" markdown="1">

**动态时间规整（Dynamic Time Warping, DTW）**

DTW是一种序列对齐方法，可以比较长度不同、步骤快慢不同的两个序列。直观地说，它允许一个序列中的若干相邻步骤与另一个序列中的一个步骤进行柔性匹配，而不是要求两边逐位置完全相同。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个下游推理任务的示例库，以及一个待求解查询，系统需要从示例库中选择若干带标签示例，并将其放入LLM的提示词中，输出查询的预测答案。本文假设示例包含可用于归纳任务规则的输入—输出信息；核心挑战是从查询与候选示例中识别问题求解逻辑，而不是仅依据词面或主题相似度。SALA的目标是先把查询和候选示例表示为任务相关的推理操作序列，再按照这些序列的语义逻辑相似程度进行检索。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$q$**

待求解的目标查询。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{D}$**

候选示例库，其中包含可供ICL使用的带标签示例。

</div>
<div class="notation-item" markdown="1">

**$o_i$**

推理操作序列中的第$i$个操作；它表示一个较明确的问题求解单元。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{O}(q)$**

查询$q$被解析或诱导得到的推理操作序列。对候选示例也可用相同方式构造对应序列。

</div>

</div>

**直接相关的工作**

- **基于嵌入相似度的示例检索（包括BM25和句子嵌入方法）**: 这类方法根据词汇重叠或整体语义相似度选择示例，适合一般检索，但可能把主题、实体和表面措辞误当作推理相关信号。SALA保留检索需求，同时进一步比较显式的问题求解操作。
- **PSL-guided ICL（Ma et al., 2025）**: 该方法与SALA最直接相关：二者都用操作序列表示问题求解逻辑。区别在于PSL依赖预定义的QDMR风格操作集合和严格的操作级精确匹配，而SALA从下游数据诱导任务自适应操作，并在连续语义空间中用DTW进行柔性对齐。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

上下文学习的效果高度依赖所选演示示例；合适示例能够引导模型完成复杂推理，而不匹配或含噪示例可能引入推理偏差。在把历史推理经验作为记忆反复检索的智能体系统中，这一选择问题更为重要，因为一次错误匹配可能直接影响后续决策。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于表面语义或向量相似度的检索**：将待解决问题与候选示例编码为向量，依据文本语义相似度选择近邻；部分学习型方法进一步训练检索器，使其偏向可能提升模型表现的示例。
- **推理感知表示与符号操作匹配**：先把问题转换为推理路径、推理模式、潜在技能或推理图等中间表示，再执行检索；其中PSL把解题过程表示为预定义推理操作的序列，并按操作层面的符号对应关系匹配示例。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原始问题的向量相似度容易被主题、实体和措辞主导，使真正决定解法的逻辑信号被稀释；自由形式的自然语言推理路径虽然表达力强，但往往含有冗余、措辞波动和不稳定分解，难以可靠比较。
- PSL式符号表示依赖固定的预定义操作空间及精确匹配规则，难以覆盖下游任务中新出现的推理单元，也会把语义等价但名称、序列长度或步骤粒度不同的推理过程误判为不相似。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法尚未同时实现两项目标：一是用显式、可检查的单位表示解题逻辑，二是让这些单位能够随具体任务扩展，并允许语义等价而非仅符号完全一致的序列进行柔性比较。需要一种既可适应下游任务，又能对不同长度和不同拆解粒度的推理过程进行逻辑对齐的表示与检索机制。

</div>
<div markdown="1"><span>核心问题</span>

能否自动学习任务特定的推理操作，并在连续语义空间中对齐由这些操作组成的序列，从而比表面相似度检索和固定操作的精确匹配更有效地选择复杂推理所需的上下文示例？

</div>
<div markdown="1"><span>作者直觉</span>

可以把每道题的解法看成一串“动作”：先识别动作，比直接比较整段题目更接近真正的解题结构；再把动作描述映射到连续语义空间，含义接近但措辞不同的动作就能获得较高匹配度。动态时间规整允许一个较粗的步骤对应多个较细的步骤，因此无需强制两条推理链具有相同长度或完全一致的切分方式；从目标任务数据中补充新动作，则避免预设操作词表遗漏领域特有的解题方式。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SALA面向推理型上下文学习中的示例选择问题：给定示例池 $\mathcal{D}=\{(q_i,y_i)\}_{i=1}^{N}$ 和测试问题 $q^{\ast}$，它不直接依据词面相似度检索示例，而是先从任务训练数据中诱导任务特定的推理操作，构造 $\mathcal{O}_{\mathrm{task}}$；随后用大语言模型将问题解析为有序操作序列，并用预训练文本嵌入模型把操作映射到连续语义空间；最后通过动态时间规整（DTW）对齐测试问题与候选示例的操作序列，按语义逻辑相似度选择前 $k$ 个示例，并按推理序列长度由短到长排列。直观地说，SALA比较的是“解题过程是否相似”，而不是“题目文字是否相似”，同时允许两个过程存在局部插入、删除或不同分解粒度。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务自适应推理操作构造

对每个训练问题提示大语言模型：仅当 $\mathcal{O}_{\mathrm{pre}}$ 无法覆盖其解题逻辑时，生成一个或多个补充操作，形成候选池 $\mathcal{O}_{\mathrm{cand}}$。随后先按操作名称小写化并去除空格、下划线后进行包含关系去重，再由大语言模型判断候选操作是否与当前操作集合在功能上重复；只有不重复的操作才被递归加入 $\mathcal{O}_{\mathrm{task}}$。

<div class="method-step__io" markdown="1">

**输入**：下游任务训练集中的问题，以及预定义的 $13$ 个 QDMR 推理操作集合 $\mathcal{O}_{\mathrm{pre}}$。<br>
**输出**：最终任务自适应操作集合 $\mathcal{O}_{\mathrm{task}}$，其中包含预定义操作和经筛选的任务特定操作。

</div>

**直观理解**：先给模型一套通用“解题动作词典”，遇到词典表达不了的任务模式时再补充新动作。两轮去重分别处理名称相近和功能相同的问题，避免操作集合膨胀。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 推理操作嵌入库建立

使用预训练文本嵌入模型 $f_{\mathrm{emb}}$ 对每个操作描述进行编码，并通过隐藏状态平均池化获得初始向量 $u_o^{\mathrm{init}}$；之后进行 $\ell_2$ 归一化，得到单位语义向量 $v_o$，并保存操作到向量的映射关系。

<div class="method-step__io" markdown="1">

**输入**：任务自适应操作集合 $\mathcal{O}_{\mathrm{task}}$ 中每个操作的核心功能描述 $\mathrm{desc}(o)$。<br>
**输出**：推理操作嵌入库 $L_{\mathrm{emb}}=\{(o,v_o)\mid o\in\mathcal{O}_{\mathrm{task}}\}$。

</div>

**直观理解**：把离散的动作名称转换成可计算距离的向量；功能相近的动作可以在向量空间中接近，因此不必要求两个操作名称完全一致。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问题解析与语义序列生成

使用大语言模型将每个问题解析为有序操作序列：测试问题得到 $Q^{\ast}=\pi(q^{\ast};\mathcal{O}_{\mathrm{task}})$，候选示例得到 $E_i=\pi(q_i;\mathcal{O}_{\mathrm{task}})$；再从 $L_{\mathrm{emb}}$ 中查找每个操作的向量，将其转换为语义序列 $\mathbf{Q}^{\ast}$ 和 $\mathbf{E}$。

<div class="method-step__io" markdown="1">

**输入**：测试问题 $q^{\ast}$、候选示例问题 $q_i$ 和 $\mathcal{O}_{\mathrm{task}}$。<br>
**输出**：测试问题和每个候选示例对应的连续操作嵌入序列。

</div>

**直观理解**：模型先把一道题概括成按先后排列的“解题动作清单”，再把清单中的每个动作替换成向量，供后续比较。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### DTW逻辑对齐与示例选择

计算两条语义序列之间的成对欧氏距离，使用满足边界、单调性和连续性约束的DTW路径求最小累计代价；将平均路径代价截断到 $1$，再转换为相似度 $\mathrm{Sim}(Q^{\ast},E_i)$。所有候选按相似度降序排列，选择前 $k$ 个示例，并按其操作序列长度升序重排后送入目标大语言模型。

<div class="method-step__io" markdown="1">

**输入**：测试序列 $\mathbf{Q}^{\ast}$ 以及每个候选序列 $\mathbf{E}$。<br>
**输出**：供目标大语言模型进行上下文学习的 $k$ 个示例及其由易到难的排列。

</div>

**直观理解**：DTW像在两条长度不同的动作清单之间拉一条允许弯曲的连线：一个过程可以多一步或少一步，但整体先后逻辑仍需对应，因此比逐位置或最长前缀匹配更灵活。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### DTW累计对齐代价递推

$$
\gamma(i,j)=D(i,j)+\min\{\gamma(i-1,j),\gamma(i,j-1),\gamma(i-1,j-1)\}
$$

**符号说明**

- $\gamma(i,j)$：从两条序列起点到测试序列第 $i$ 个操作与候选序列第 $j$ 个操作之间的最小累计对齐代价。
- $D(i,j)$：测试序列第 $i$ 个操作向量与候选序列第 $j$ 个操作向量之间的欧氏距离。
- $i,j$：分别表示测试序列和候选序列中的位置索引。

<div class="equation-explanation" markdown="1">

**直观理解**：到达位置 $(i,j)$ 时，算法选择三种合法前一步中累计代价最小的一种，再加上当前两个操作的不匹配代价。该递推使序列可以局部拉伸或压缩，同时保持解题步骤的先后顺序。<br>
**原文位置**：第3.4.3节，公式(7)

</div>

</div>

<div class="equation-block" markdown="1">

#### DTW序列相似度

$$
\mathrm{Sim}(Q^{\ast},E_i)=\frac{1}{1+\min\left(\frac{\gamma(m,n)}{k},1\right)}
$$

**符号说明**

- $\mathrm{Sim}(Q^{\ast},E_i)$：测试问题序列 $Q^{\ast}$ 与候选示例序列 $E_i$ 的最终语义相似度。
- $\gamma(m,n)$：到达两条完整序列末端时的最小DTW累计代价。
- $k$：最优DTW路径的长度，用于把累计代价转换为每一步的平均代价。
- $m,n$：测试序列和候选序列的长度。

<div class="equation-explanation" markdown="1">

**直观理解**：先用路径长度消除序列长短差异，再把平均距离转换为相似度；平均距离越小，分数越高。论文指出由于向量归一化且距离被截断，分数范围为 $[0.5,1]$，但该分数是排序信号而非概率。<br>
**原文位置**：第3.4.3节，公式(8)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：SALA的核心不是训练一个新的端到端参数模型，而是一个基于提示的大语言模型操作诱导、问题解析和示例检索框架。论文所给方法章节未定义用于优化SALА参数的损失函数；预训练嵌入模型也被作为固定编码器使用，操作向量在检索前预计算。因此，训练阶段主要是利用下游训练数据构造 $\mathcal{O}_{\mathrm{task}}$ 和 $L_{\mathrm{emb}}$，而不是对SALА进行梯度优化；原文未明确报告操作诱导或解析提示是否进行额外参数训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 任务特定操作诱导与两阶段去重**

SALA以QDMR的 $13$ 个预定义操作为基础，从训练问题中让大语言模型仅在覆盖不足时诱导新操作。候选操作先经过基于归一化名称和包含关系的启发式去重，再经过大语言模型的功能重叠二元判断 $J(\bar{o}_i,\mathcal{O}_{\mathrm{task}}^{(i-1)})\in\{0,1\}$；判断为无功能重叠时才加入集合。

> 直观理解：固定词典对不同任务的解题方式覆盖不全，因此SALА允许词典按任务扩展；先用便宜的名字规则过滤明显重复项，再用模型判断真正的功能是否重复。

**2. 连续语义操作表示**

每个操作的功能描述经嵌入模型编码为 $u_o^{\mathrm{init}}\in\mathbb{R}^{d}$，并归一化为 $v_o$。由于所有向量位于同一固定维度空间且为单位向量，欧氏距离可以作为操作语义差异的成本。

> 直观理解：操作不再被当作只能完全相等或完全不同的标签，而是具有程度差异的语义表示；这使“相近但名称不同”的推理动作能够匹配。

**3. DTW语义序列对齐**

DTW在操作嵌入序列之间寻找从 $(1,1)$ 到 $(m,n)$ 的单调、连续路径，并允许水平、垂直或对角移动，以适配不同序列长度和不同分解粒度。最终相似度使用平均对齐距离的有界变换，距离越小则相似度越接近 $1$。

> 直观理解：两个解题过程不必逐步严格对齐：一个过程把某一步拆成多步，另一个过程可能合并表达，DTW仍能寻找合理的整体对应关系。

**训练与推理**

训练数据阶段：从下游任务训练集形成示例池 $\mathcal{D}$，以 $\mathcal{O}_{\mathrm{pre}}$ 为起点诱导候选操作，执行名称去重和功能去重，得到 $\mathcal{O}_{\mathrm{task}}$；为每个操作生成核心功能描述，利用固定的嵌入模型计算并归一化 $v_o$，建立可复用的 $L_{\mathrm{emb}}$。检索推理阶段：对测试问题 $q^{\ast}$ 和示例池中每个候选问题 $q_i$ 进行操作序列解析，从嵌入库取出序列向量，计算成对距离和DTW最优路径，得到 $\mathrm{Sim}(Q^{\ast},E_i)$；按分数降序取前 $k$ 个示例，再按推理操作序列长度升序排列，最后将这些示例与测试问题一起输入目标大语言模型完成答案生成。论文没有在所给章节中明确说明操作解析、示例选择和答案生成是否使用不同的大语言模型或具体提示轮数。

**复现信息**

为公平解释结果，应注意三点：第一，候选操作诱导和序列解析依赖大语言模型提示，功能去重也依赖大语言模型的二元判断，因此这些环节可能引入模型判断误差；第二，嵌入模型对操作的功能描述进行编码，而不是直接对完整问题编码，向量采用均值池化并做 $\ell_2$ 归一化；第三，DTW使用欧氏距离、边界为 $(1,1)$ 到 $(m,n)$，路径允许三种相邻转移，并将平均路径代价截断到 $1$。检索后采用由易到难的序列长度排序。所给章节未明确报告嵌入模型的具体名称、向量维度 $d$、候选池规模、检索的 $k$ 值、提示模板细节、DTW窗口限制或运行时间，因此不能据此补充这些复现参数。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：包含$8{,}792$道小学数学题，训练集$7{,}473$道、测试集$1{,}319$道；用于检验多步数学推理中的示例选择。原文表3报告："GSM8K 7,473 1,319"。
- SVAMP：包含$1{,}000$道算术文字题，训练集$700$道、测试集$300$道；用于检验算术文字推理。原文表3报告："SVAMP 700 300"。
- CommonsenseQA与StrategyQA：前者是包含五个选项的常识多项选择题基准，共$10{,}881$题，训练集$9{,}741$道、测试集$1{,}140$道；后者是开放域问答基准，共$2{,}290$题，训练集$1{,}603$道、测试集$687$道。二者共同检验方法从数学推理迁移到常识和开放域推理的能力。原文表3报告："CommonsenseQA 9,741 1,140"和"StrategyQA 1,603 687"。由于列表上限为三个条目，此处将两个非数学基准合并说明。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务准确率**

原文将各基准上的最终任务正确率作为性能比较依据；它衡量选中的示例是否帮助目标模型得到正确答案，而非直接衡量检索序列本身的相似度。 （越高越好；但仅凭准确率不能单独证明模型真正学习了正确推理过程，也可能受到目标模型能力和提示格式影响。）

</div>
<div class="metric-item" markdown="1">

**五次运行的平均结果**

所有实验结果在五次运行后取平均，用于减小随机抽样、生成和推理波动。 （平均准确率越高越好；原文未明确报告标准差或置信区间，因此无法判断小幅差异的统计显著性。）

</div>
<div class="metric-item" markdown="1">

**案例正确性**

消融案例中将模型输出与明确给出的Ground Truth比较，用来诊断示例选择是否保留了关键推理操作，例如取模、代数求解或百分比计算。 （正确答案表示更好；该指标只适用于定性案例，不能替代四个基准上的总体统计结果。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所提供章节未给出主结果表或图，因此无法核验摘要中“SALA优于现有方法”的具体幅度、各基准上的一致性以及统计显著性；原文未明确报告标准差、置信区间或显著性检验。
- 实验依赖Seed-OSS-36B-Instruct归纳操作、BERT编码操作，并按PSL设定示例数量；因此结果可能受操作归纳质量、编码器选择和示例预算影响。当前节选没有报告不同归纳模型、编码器或示例数量下的敏感性分析。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Random：随机抽取示例，提供无检索能力的下界，用于判断收益是否来自有针对性的示例选择。
- BM25与EPR：BM25依据词项匹配，EPR使用对比学习检索器；二者代表基于表面或语义文本相似度的传统检索方法，可检验SALA是否超越“题面相似”这一选择信号。
- TopK-BERT与DPP-BERT：TopK-BERT使用BERT表示检索最相似示例，DPP-BERT进一步用行列式点过程平衡相关性与多样性；二者检验单纯语义相关性及相关性—多样性权衡是否足够。
- PSL与LMS3：PSL依据解题逻辑指导选择示例，LMS3结合语义相似度与推理稳定性；二者是最直接的推理感知对照，用于检验SALA的软逻辑对齐是否优于既有逻辑规则或稳定性信号。

**实验想回答的问题**

- 在四类推理基准、三种目标大语言模型上，SALA是否比随机采样、文本相似度检索和已有推理感知选择方法更有效地选择上下文示例？
- SALA的任务特定操作归纳与基于动态时间规整的逻辑语义对齐是否分别带来可识别的收益？

**实验实现**

评估使用Llama3-8B-Instruct、Qwen2.5-7B-Instruct和通过API调用的DeepSeek-V4-Pro三种目标模型。每个基准的候选示例来自训练集，操作归纳使用独立的Seed-OSS-36B-Instruct在相应训练集上构造，以避免操作空间由被评估目标模型决定；推理操作的语义编码使用$bert\text{-}base\text{-}uncased$。所有基线与SALA选择的示例数量遵循PSL针对不同基准的设置，结果平均五次运行。原文明确说明了数据划分、模型和平均方式，但所给章节没有提供总体结果表、准确率数值、标准差或每个基准的完整提示配置。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 去除新操作，仅保留$13$种QDMR操作 | 案例1中，加入新操作后模型正确完成取模问题；去除新操作后，序列被扩展为“除法→乘法→减法”，从而匹配到比例问题。案例2中，加入$DEFINE$和$ALGEBRA$后答案为$80$，而仅使用QDMR时答案为$90$。 | 该消融隔离操作归纳模块。结果表明，固定且较粗的QDMR操作难以表达取模和未知量求解等高层结构，模型可能依据连续$ARITHMETIC$或重复$SELECT$—$PROJECT$模式选择逻辑不相关的示例；新操作提供了更短、更有语义的推理表示。案例结果支持“操作粒度影响示例选择”，但只是少量定性案例，不能推出总体准确率必然提升。 | 附录F.1.2，表8；案例1对应表7<br><span class="experiment-evidence">w/ new OPs
80 ✓
(with Algebra)
w/o new OPs
90
×
(QDMR only)</span> |
| DTW语义对齐与Prefix Subsequence Matching对比，仅使用$13$种QDMR操作 | 案例3中，DTW选择的示例得到$1{,}430$，Prefix方法得到$1{,}170$；案例4中，DTW得到$86.40$，Prefix方法得到$80$。 | 该消融隔离逻辑对齐模块。Prefix方法要求示例操作序列严格匹配查询前缀，容易排除步骤粒度不同但逻辑相同的示例，或选择一个只覆盖前面步骤、遗漏百分比计算的示例。DTW允许序列在时间步上发生弹性错位，因此能匹配“基数→百分比→总计”等结构；案例支持软对齐优于严格前缀约束，但仍不能替代跨数据集的统计消融。 | 附录F.2.1，表9<br><span class="experiment-evidence">Ground Truth
$1,430
DTW
$1,430 ✓
Prefix
$1,170
×</span> |

**定性案例**

- 百分比计算案例：查询要求先合计$50$美元的裙子和$30$美元的包，再加$8\%$销售税，正确答案为$86.40$。DTW选择了包含“提取基础价格→应用百分比→求总和”的示例并答对；Prefix选择了只演示两项求和的示例，输出$80$，漏掉税费。该案例直观说明，严格前缀匹配的“形式有效”不等于覆盖完整推理，而DTW更关注操作关系和推理步骤的功能相似性。原文证据为："DTW
$86.40 ✓
Prefix
$80
×"，位置为附录F.2.2、表10。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：核心贡献是依据语义化推理操作和逻辑序列对齐来选择示例，从而改善 LLM 的上下文复杂推理。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`76b4b3084043d91f8474ab5f3ebd6a5e3562cd53f2e30142327d1d17f4eefe11`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
