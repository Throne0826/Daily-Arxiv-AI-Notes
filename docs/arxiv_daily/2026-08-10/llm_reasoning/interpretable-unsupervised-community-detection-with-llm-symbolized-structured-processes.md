---
title: "[论文解读] Interpretable Unsupervised Community Detection with LLM-Symbolized Structured Processes"
description: "[arXiv 2608.06402][LLM Reasoning] 本文提出 LUCID，一种利用大语言模型诱导可解释规则、无需训练和标签的社区检测方法。"
arxiv_id: "2608.06402"
announcement_date: "2026-08-10"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-10T02:38:44.815862+00:00"
source_sha256: "7427f1f31f4b0846d6eb48533b09e1c5d86b44863da6084d6b207c084fa938f4"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.06402</p>

# Interpretable Unsupervised Community Detection with LLM-Symbolized Structured Processes

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Aoting Zeng, Kai Wang, Jianwei Wang, Yuxiang Sun, Yizhang He, Wenjie Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Shanghai Jiao Tong University Shanghai China；Shanghai Jiao Tong University；University of New South Wales Sydney Australia；University of New South Wales</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.06402v1) · [PDF 下载](https://arxiv.org/pdf/2608.06402v1) · **关键词** LLM Reasoning<br>


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

本文提出 LUCID，一种利用大语言模型诱导可解释规则、无需训练和标签的社区检测方法。

**不用术语来说**：给定一个由节点和连接组成的网络，研究目标是把联系紧密、行为相似的节点分成若干社区，同时说明每个节点为何被归入某个社区。现实网络的结构通常复杂，现有方法虽然可能获得较好的划分结果，却往往难以解释决策过程，且常需要针对新数据重新训练或依赖人工标注。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 LUCID 四阶段社区检测框架：从局部结构初始化社区，经多因素合并和多粒度细化，最后依据全局拓扑质量选择社区。
- 将大语言模型定位为规则诱导器而非端到端预测器，把隐含的结构判断转化为可检查的逻辑规则，从而同时支持无监督、免训练和可解释的社区检测。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

社区发现是图分析中的基础任务，目标是在由节点和边构成的图中识别内部连接紧密、行为或兴趣相似的节点群。该任务应用于金融系统、社交网络、生物医学和信息系统等场景；现有方法包括基于目标函数优化、矩阵分解、生成模型以及深度学习的方法，但复杂真实图结构、决策透明性和跨数据集适应性仍是关键问题。本文将大语言模型用于无监督社区发现，并通过显式规则表达其分析过程。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**图与社区**

图由节点和边组成，节点表示实体，边表示实体之间的关系。社区是图中内部连接较密集、因而可能具有相似行为或兴趣的节点集合。

</div>
<div class="concept-item" markdown="1">

**无监督与半监督学习**

无监督方法不依赖人工标注的社区，而是仅根据图结构发现群组。半监督方法则使用部分已标注社区进行训练或提示，因此在标注稀缺时成本更高。

</div>
<div class="concept-item" markdown="1">

**大语言模型驱动的图分析**

这类方法把图结构或其描述提供给大语言模型，使模型利用推理能力处理图任务。本文特别关注将模型的隐含判断转化为可检查的显式逻辑规则，而不是只使用不可解释的输出。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一张现实世界图，包含节点及其关系；在无监督、免训练的设定下，方法需要输出若干社区，即节点集合，并判断这些社区是否具有较高的内部拓扑紧凑性和较清晰的边界。论文关注的不是仅优化固定目标函数，而是让方法能够适应复杂图结构，同时解释节点为何被归入同一社区；原文未明确给出统一的形式化图记号、节点属性假设或社区是否必须构成完整划分的约束。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G$**

图；原文以 graph 表述输入对象，但未在所给章节中明确给出形式化定义。

</div>
<div class="notation-item" markdown="1">

**$V$**

节点集合；该符号未在所给章节中显式定义，此处仅按图论常用记法标注。

</div>
<div class="notation-item" markdown="1">

**$E$**

边集合；该符号未在所给章节中显式定义，此处仅按图论常用记法标注。

</div>
<div class="notation-item" markdown="1">

**$k$**

局部视图中的邻域阶数；摘要提到 k-ego contexts，但所给章节未进一步说明其具体取值或构造方式。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

社区检测被用于金融系统、社交网络和生物医学等图分析场景，用于发现联系紧密的实体群体并支持后续分析和决策。实际应用中的网络结构往往具有复杂的边界、不同尺度的群体以及不规则的连接模式，因此方法不仅需要识别合理社区，还需要能够解释节点归属，并能在缺少标注和新图数据上直接使用。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **经典目标驱动方法**：这类方法直接优化预设的图结构目标，例如连接密度或模块度，以寻找内部连接较密集的节点集合。其优点是流程相对明确，但固定目标对复杂、非规则的真实社区结构适应性有限。
- **深度学习社区检测方法**：这类方法使用节点表示、生成模型、深度强化学习或预训练与提示策略，学习图中的复杂结构模式并预测社区。例如 ComE 使用节点嵌入表示社区特征，SEAL 使用生成对抗网络推断社区结构，CLARE 使用定位器和重写器进行强化学习式检测，PROCOM 结合预训练和提示策略。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 深度学习方法通常以神经网络内部表示或端到端预测作出决定，难以明确说明某个节点为何与其他节点归入同一社区，结果因此缺乏可审查性。
- 许多方法需要针对数据集训练或适配；半监督方法还依赖社区标签进行训练或提示，而真实应用中的标注成本高且经常不可获得，导致方法难以直接迁移到新的无标签图。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未充分解决这样一个结合性缺口：如何在不依赖社区标签和数据集特定训练的前提下，处理复杂图结构，同时把社区合并、边界修正和结果筛选过程表达为人能够检查的结构化规则。关键困难在于，单一的局部相似性或固定优化目标不足以覆盖社区形成过程中的多种判断因素，而纯神经网络方案又难以提供清晰的决策依据。

</div>
<div markdown="1"><span>核心问题</span>

能否让大语言模型利用其推理能力和一般知识，针对图中的局部结构、社区合并因素、不同粒度的边界噪声以及全局拓扑质量诱导出显式规则，从而构建一种免训练、无标签且可解释的社区检测流程？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把大语言模型从直接给出社区划分的预测器改造成规则设计者：先用 $k$-ego 上下文和无监督节点角色描述局部结构，再让模型把多种结构线索组织成合并与细化规则，最后用拓扑紧致性和边界清晰度筛选结果。直观上，这相当于先生成候选群体，再逐步合并相容群体、清理边界噪声并进行全局审查；规则化中间过程使最终划分不仅有结果，也能追溯其判断依据。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

LUCID 将无标签图 $G=(V,E)$ 的社区发现拆成“局部初始化、合并、细化、全局筛选”四个阶段。它不让大语言模型直接读完整图并输出社区，而是先用确定性的图算法把图压缩为可放入提示词的局部 $k$-ego 子图，再让大语言模型从样例结构中归纳可执行的符号规则；这些规则随后在全图上重复执行。因此，最终结果既是允许重叠的社区集合，也能给出合并或删除节点所依据的决策树/规则轨迹。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 局部视图社区初始化

以每个节点 $u$ 为中心构造包含 $k$ 跳内节点的重叠子图 $G_u^{(k)}$。再根据节点与其邻居的邻域 Jaccard 相似度分布提取五个分位数特征，并以 $K=4$ 的 K-means 聚类赋予无监督角色标签 $l_u$。

<div class="method-step__io" markdown="1">

**输入**：无属性或仅含拓扑信息的图 $G=(V,E)$，以及 $k$-ego 半径 $k$。<br>
**输出**：带角色标签的局部 $k$-ego 子图集合 $\{G_u^{(k)}\}_{u\in V}$，作为初始社区单元和后续提示词的结构化输入。

</div>

**直观理解**：完整图可能太大，无法一次交给大语言模型；该步骤把每个节点周围的小范围关系单独展开。角色标签用“邻居之间有多像”概括节点在局部中的位置，使模型不必只依赖冗长的边列表理解结构。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多因素社区合并

大语言模型依据样例归纳 JSON 格式的多因素决策树，并将其编译为可执行谓词，用重叠、密度和角色标签等条件判断中心—邻居子图对是否合并。执行时按 ego 密度从高到低调度中心节点，并只对 Jaccard 相似度最高的 top-$b$ 邻居运行规则；若接受合并，则将相应 ego 节点从可用中心集合中移除。

<div class="method-step__io" markdown="1">

**输入**：局部子图、角色标签、数据集统计概要，以及中心节点及其相邻 $k$-ego 子图构成的样例块。<br>
**输出**：经局部子图聚合得到的候选社区骨架集合 $\mathcal{C}_M$，以及可审计的合并决策规则和轨迹。

</div>

**直观理解**：大语言模型只负责先写出“什么情况下可以并”的规则，不逐对实时替作者做黑箱判断。算法优先处理连接紧密的核心区域，并跳过结构上不相近的大量邻居，以控制上下文长度和计算量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多粒度社区细化

大语言模型归纳由粗到细的节点删除规则：粗规则先剔除明显不一致节点，中粒度规则检查局部邻居及角色一致性，细规则再使用局部聚类系数和介数中心性等精细拓扑量。规则在不同社区之间并行执行，并在单个社区内批量处理节点，输出应从各候选社区删除的边界噪声节点。

<div class="method-step__io" markdown="1">

**输入**：合并阶段得到的候选社区 $\mathcal{C}_M$、数据集统计概要和候选社区样例。<br>
**输出**：经成员修正后的候选社区集合 $\mathcal{C}_R$。

</div>

**直观理解**：合并能找回社区主体，但边界处容易混入桥接节点或偶然相连的节点。先做便宜的粗筛，再把计算较重的检查留给少数可疑节点，目标是保留社区内部模式一致的成员。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 全局社区筛选

对每个候选社区计算 RDC，即以跨社区割边数衡量外部边界、以内边数量衡量内部凝聚，并对接近树状的稀疏连通子图施加惩罚。按 RDC 从小到大排序，选择前 $N$ 个候选社区作为最终结果。

<div class="method-step__io" markdown="1">

**输入**：细化后的候选社区集合 $\mathcal{C}_R$、目标输出数量 $N$，以及密度正则参数 $\epsilon$。<br>
**输出**：最终高质量社区集合；社区的 RDC 分数同时构成可解释的全局排序依据。

</div>

**直观理解**：低分社区应当内部连接较多、与外部连接较少。额外惩罚避免把仅靠少量链式边维持连通、但并不紧密的节点集合误认为优质社区。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Ego 网络 Jaccard 相似度

$$
J(v,u)=\frac{|V_{\mathrm{ego}}(v)\cap V_{\mathrm{ego}}(u)|}{|V_{\mathrm{ego}}(v)\cup V_{\mathrm{ego}}(u)|}.
$$

**符号说明**

- $J(v,u)$：节点 $v$ 与节点 $u$ 的 ego 网络节点集之间的 Jaccard 相似度。
- $V_{\mathrm{ego}}(v)$：以节点 $v$ 为中心的 ego 网络中的节点集合。
- $V_{\mathrm{ego}}(u)$：以节点 $u$ 为中心的 ego 网络中的节点集合。

<div class="equation-explanation" markdown="1">

**直观理解**：分子是两个局部网络共有的节点数，分母是它们出现过的全部节点数。分数越高，说明两个中心附近的局部结构越重叠；论文用它筛选提示词样例和实际合并时值得比较的邻居。<br>
**原文位置**：第 4.3.2 节，Similarity-based sampling

</div>

</div>

<div class="equation-block" markdown="1">

#### RDC：密度正则化导通排序分数

$$
RDC(\mathcal{C}_R)=\frac{Cut(\mathcal{C}_R,\bar{\mathcal{C}_R})}{|E(\mathcal{C}_R)|-\epsilon(|\mathcal{C}_R|-1)}.
$$

**符号说明**

- $RDC(\mathcal{C}_R)$：候选社区 $\mathcal{C}_R$ 的密度正则化导通排序分数，越小越优。
- $\mathcal{C}_R$：经过细化后的候选社区。
- $\bar{\mathcal{C}_R$：图中不属于 $\mathcal{C}_R$ 的节点集合。
- $Cut(\mathcal{C}_R,\bar{\mathcal{C}_R)$：从 $\mathcal{C}_R$ 连接到其补集的跨边数量。
- $E(\mathcal{C}_R)$：候选社区内部边的集合。
- $\epsilon$：控制对链状、接近树结构社区惩罚强度的正则参数。

<div class="equation-explanation" markdown="1">

**直观理解**：分子越小表示社区边界越清晰，分母越大表示内部越紧密。减去与节点数相关的项会使内部边数接近连通所需最低值的树状社区得到很大分数，因而不会被优先选中。<br>
**原文位置**：第 4.5 节，式 (1)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。LUCID 不训练图神经网络、嵌入模型或任务分类器，也没有可学习参数上的损失函数优化；大语言模型在合并和细化前根据提示词生成一次可执行规则，后续通过确定性图处理执行。论文将其描述为“training-free”和“label-free”，但未在所给章节说明所调用模型是否完全固定、温度等生成配置，故这些细节为“原文未明确报告”。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. LLM 符号化规则归纳器**

合并模块的提示词由数据画像、中心节点 $v_c$ 的 $k$-ego 网络及其 $z$ 个直接邻居的 ego 网络组成；模型输出决策树 $\mathcal{T}$ 的 JSON 规则，再被编译为内部节点谓词 $\phi_n$ 与叶节点动作。细化模块使用数据画像和候选社区样例，生成粗、中、细三级的成员删除规则，而不是对每个节点重新调用模型作自由文本判断。

> 直观理解：该设计把大语言模型的作用限定为一次性归纳明确规则，图算法负责大规模执行。可解释性来自可查看的条件判断和决策轨迹，而非仅从最终社区反推模型理由。

**2. 动态合并编排器**

候选邻居由 $J(v,u)$ 排序后截取 top-$b$，而中心节点按 $\mathrm{EgoDensity}(v)$ 降序处理。对接受的合并 $M(v,u)=1$，更新 $\mathcal{A}\leftarrow\mathcal{A}\setminus V_{\mathrm{ego}}(u)$，避免已被吸收子图反复作为中心，但其节点仍可参与其他社区，因而支持重叠社区。

> 直观理解：它分别回答“比较谁”和“先处理谁”。前者减少无关比较，后者优先建立更可靠的稠密核心，再处理较稀疏的外围结构。

**3. RDC 全局质量选择器**

RDC 在标准割边/内边比的分母中减去 $\epsilon(|\mathcal{C}_R|-1)$。论文证明，在 $e$ 接近该惩罚项时，新分数趋于无穷大，且其对内边数 $e$ 的变化比标准分数更敏感，从而更强地排斥接近最低连通边数的树状候选。

> 直观理解：仅看边界与内部边的比例，可能无法充分区分紧密团块和细长树枝。RDC 把“刚好连通但不够稠密”的结构排到后面。

**训练与推理**

该方法只有推理式处理流程：输入图后构造 $k$-ego 子图和角色标签；向大语言模型提供数据画像与结构样例，分别获得合并决策树和细化规则；在整张图上执行相似度受限、密度排序的合并，再并行细化候选成员，最后以 RDC 排序选出 top-$N$ 社区。模型生成不是端到端社区预测，且表 2 注明“with a fixed prompt, LUCID reports mean ± std over three independent LLM generations”，说明结果会报告独立规则生成带来的波动。

**复现信息**

为复现实验解释所必需的公开设定包括：初始化阶段使用每个节点的 $k$-ego 网络；节点角色特征由邻域 Jaccard 相似度的 $(Q_0,Q_{25},Q_{50},Q_{75},Q_{100})$ 五个分位数构成，并以 $K=4$ 的 K-means 离散化；合并阶段在规则构造时取 top-$z$ 邻居、执行时取 top-$b$ 邻居，并按 ego 密度降序调度；细化规则按粗到细顺序、跨社区并行且社区内批量运行；最终按 RDC 升序保留 top-$N$。$k$、$z$、$b$、$N$、$\epsilon$ 的具体数值、LLM 型号、提示词全文、编译规则的完整语法和并行硬件配置在所给章节中均为“原文未明确报告”，不能据此摘录自行补全。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Facebook：社会网络，包含 $3{,}622$ 个节点、$72{,}964$ 条边和 $130$ 个社区，平均社区大小为 $15.6$，平均度为 $40.3$；用于检验方法在社区边界相对清晰的小型网络上的表现。
- Amazon：电子商务网络，包含 $13{,}178$ 个节点、$33{,}767$ 条边和 $4{,}517$ 个社区，平均社区大小为 $9.3$，平均度为 $5.1$；用于检验方法在大量、小规模且较稀疏社区上的表现。
- Livejournal：社会网络，包含 $69{,}860$ 个节点、$911{,}179$ 条边和 $1{,}000$ 个社区，平均社区大小为 $13.0$，平均度为 $26.1$；用于检验方法在大规模且社区重叠明显的网络上的表现。原文还报告了 DBLP 和 Twitter，但受任务限制此处不展开。五个数据集均含有重叠社区和部分标签，作者按照 ProCom、CLARE 和 SEAL 使用的预处理协议移除异常值，以保证比较公平。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**F1**

在双向匹配下，分别让每个预测社区匹配最相似的真实社区、让每个真实社区匹配最相似的预测社区，再对两个方向取平均。单个匹配中的 $delta$ 使用 F1，综合考察社区成员的准确性与覆盖率。 （越高越好，因为高分表示预测社区与真实社区在成员重合和完整性方面更好。）

</div>
<div class="metric-item" markdown="1">

**Jaccard**

与 F1 使用相同的双向匹配框架，但单个社区匹配相似度 $delta$ 改为 Jaccard 相似度，即交集大小除以并集大小。 （越高越好，因为高分表示预测社区与真实社区的成员集合更一致。）

</div>
<div class="metric-item" markdown="1">

**Pair F1**

在合并阶段评估候选社区对是否应当合并，综合衡量正确合并的精确率与召回率。严格版本 Strict Pair F1 还要求合并后社区至少有 $\tau=0.8$ 的成员属于其最匹配真实社区。 （越高越好，因为高分表示合并决策既少误合并，也能覆盖更多应合并的候选对。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 总体性能：$LUCID$ 与无监督基线比较

<div class="result-value" markdown="1">

作者报告 $LUCID$ 在所有五个数据集上均显著优于现有无监督方法；相对于每个数据集上最强的无监督基线，F1 平均相对提升 $20.7\%$，Jaccard 平均相对提升 $31.9\%$。

</div>

该结果说明，将局部结构编码、规则驱动的社区合并、细粒度修正和全局筛选组合起来，能够明显改善传统无监督方法的社区成员识别。它支持的是在本文数据集和评测协议下的有效性，并不单独证明提升完全来自大语言模型，也不证明对所有图类型都成立。

<div class="result-source" markdown="1">

来源：第 5.2 节 Overall performance (RQ1)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with the best unsupervised baseline on each dataset, our method achieves average improvements of 20.7% in F1 score and 31.9% in Jaccard score.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 总体性能：$LUCID$ 与半监督基线比较

<div class="result-value" markdown="1">

作者报告 $LUCID$ 在五个数据集上都取得最佳结果；相对于每个数据集上最强的半监督基线，F1 平均相对提升 $10.1\%$，Jaccard 平均相对提升 $16.6\%$。

</div>

这是一个更强的比较，因为半监督方法可以使用 $10$ 个标注社区进行训练或提示，而 $LUCID$ 不使用标签。结果表明，本文方法在给定实验设置下能够利用网络拓扑和规则化推理获得具有竞争力的检测结果，但由于半监督方法的训练、提示和数据使用方式不同，比较仍不能完全排除协议差异的影响。

<div class="result-source" markdown="1">

来源：第 5.2 节 Overall performance (RQ1)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As an unsupervised method, LUCID consistently outperforms state-of-the-art semi-supervised baselines.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### LLM 规则的过程级质量：合并决策

<div class="result-value" markdown="1">

在五个数据集平均的候选社区对评估中，LLM Rules 的 Pair F1 为 $39.64\%$，高于 Modularity 的 $32.30\%$；严格合并条件下，Strict Pair F1 为 $23.57\%$，高于 Modularity 的 $16.62\%$。严格条件采用合并后社区至少有 $80\%$ 成员属于最匹配真实社区的要求。

</div>

该结果直接检验合并动作本身，而不是只看最终社区分数。LLM 规则在普通和严格合并判定下都更准确，说明其诱导出的结构一致性、密度兼容性、标签对齐和规模平衡等条件可能有助于减少错误合并。不过这些过程级标签使用了真实社区进行事后评估，因此只能作为评测工具，不能作为无监督推理时可获得的信息。

<div class="result-source" markdown="1">

来源：附录 E.1 Merge quality，表 9

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with the strongest heuristic, they increase Pair F1 from 32.30% to 39.64% and Strict Pair F1 from 16.62% to 23.57%.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 数据集均来自 SNAP，且都含有重叠社区和部分标签；因此实验结论主要适用于具有此类标注和结构特征的网络，不能据此断言方法在无重叠社区、动态图、异质图或其他领域图上的表现。
- 主实验依赖 GPT-5.2 官方 API，虽然附录报告了 DeepSeek-V4-Pro 结果，但所提供摘录没有给出完整的 API 成本、运行时间、提示内容和随机性控制细节；因此 $LUCID$ 的可复现性、成本优势及对不同 LLM 的稳健性仍需进一步核查。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- BigClam：无监督矩阵分解方法，用于检测重叠社区；它是传统目标驱动无监督方法的代表。
- ComE：无监督地联合学习节点嵌入与社区结构；它代表将表示学习用于社区检测的方法。
- PROCOM：半监督方法，采用“预训练、提示”范式和双层级预训练；它是与基于大语言模型的半监督方法比较的重要对象，但需要标注数据和训练或提示示例。
- CLARE：半监督方法，使用定位器和重写器从标签中学习社区；它代表依赖标注信息的生成式或重写式检测方法。

**实验想回答的问题**

- RQ1：作为完全无监督方法，$LUCID$ 相比无监督方法和代表性半监督方法的社区检测性能如何？
- RQ2：$LUCID$ 的四个阶段及其关键规则分别对总体性能贡献多大？

**实验实现**

实验在 NVIDIA A100 上进行，主实验使用 GPT-5.2 作为大语言模型骨干，并通过官方 API 调用；默认温度为 $1.0$。预测社区数 $N$ 按数据集设置：Facebook 为 $200$，Amazon 为 $1{,}500$，Livejournal 为 $1{,}000$，DBLP 和 Twitter 为 $5{,}000$。对于无监督基线，按照既有工作直接报告其结果；对于半监督方法，随机选择 $10$ 个社区用于训练或提示，将其余社区用于测试。总体性能中的 F1 和 Jaccard 采用真实社区与预测社区之间的双向最大相似度平均值。效率实验还考察运行时间和 API token 成本，原文说明每次实验限制为两次 API 调用，但详细运行时间与 token 分解位于附录表 12 和表 13。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 排名指标消融：Density、Modularity、Local Conductance 与 RDC | 表 4 的 F1 结果显示，RDC 在 Amazon 和 Livejournal 上取得最高分，在 Facebook 上与 LC 接近；相对 Density 的平均相对提升为 $161.44\%$，相对 Modularity 的平均相对提升为 $83.40\%$，相对 LC 的提升较小。RDC 同时考虑密度和局部传导率，用于衡量社区内部凝聚性与边界清晰度。 | 该消融隔离的是全局社区选择阶段的排名标准，而不是 LLM 是否参与规则生成。结果支持 RDC 比单独使用密度或模块度更能兼顾内部连接和外部边界，但其相对 LC 的优势有限，说明传导率类指标本身已经很有效，RDC 的收益主要来自联合考虑多个结构信号。 | 第 5.3 节 Ranking metric ablation study，表 4<br><span class="experiment-evidence">Our proposed RDC consistently outperforms baselines on most datasets, achieving substantial average gains over Density (+161.44%) and Modularity (+83.40%).</span> |
| LLM 必要性消融：用 Density 或 Modularity 替换 LLM-induced rules | 表 5 中，LLM Rules 在五个数据集上的 F1 平均相对优于 Density $13.4\%$、优于 Modularity $5.0\%$。例如 Amazon 上，LLM Rules 为 $92.11\%$，Density 为 $71.66\%$，Modularity 为 $85.54\%$；这些数值均为 F1 百分比。 | 该实验检验性能是否只是来自简单结构启发式。替换方案在合并阶段仅在指标增加时合并，在修正阶段仅在指标增加时删除节点，因此比较了相近的操作框架。结果支持 LLM 诱导规则能提供比单一密度或模块度更细致的判断，但不能区分具体是哪一条规则、提示设计还是模型本身导致收益，因为没有提供逐规则的独立消融。 | 第 5.3 节 LLM necessity ablation study，表 5<br><span class="experiment-evidence">As shown in Table 5, LLM-induced rules outperform Density and Modularity by 13.4% and 5.0% on average across the five datasets, respectively.</span> |

**定性案例**

- DBLP 与 Amazon 的可解释性案例展示了从输入局部子图到输出社区的决策链。在 DBLP 示例中，$LUCID$ 因顶部邻居具有较高重叠率、标签一致性和密度相似性而将其合并；底部邻居因共享上下文不足而被拒绝。随后修正阶段移除内部度较低且三角闭包较弱的节点，得到与真实社区一致的 $5$-clique。Amazon 示例同样通过聚合稠密邻居并剪除离群点得到与真实社区对齐的预测。该案例说明规则具有可追踪性和可读性，但属于少量定性示例，不能替代大规模统计验证。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The method centrally uses LLM-induced logical rules and structured multi-stage reasoning for unsupervised community detection.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`7427f1f31f4b0846d6eb48533b09e1c5d86b44863da6084d6b207c084fa938f4`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
