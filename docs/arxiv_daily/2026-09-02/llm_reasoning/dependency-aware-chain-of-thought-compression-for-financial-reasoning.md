---
title: "[论文解读] Dependency-Aware Chain-of-Thought Compression for Financial Reasoning"
description: "[arXiv 2609.00413][LLM Reasoning] 本文旨在通过依赖感知的结构化压缩，在显著缩短金融推理链的同时，尽量保留答案正确性、关键计算依赖与可审计的论证连续性。"
arxiv_id: "2609.00413"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:38:46.106820+00:00"
source_sha256: "75b4b7b44ddf5087b8a41ef076a85391ce6fddeb4e981e05b4ecdf1f0e93c106"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "链式思维压缩"
  - "金融推理"
  - "语义分段"
  - "依赖图"
  - "受约束片段选择"
  - "逻辑连贯性"
  - "可审计推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.00413</p>

# Dependency-Aware Chain-of-Thought Compression for Financial Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Wenjun Wu, Lei Fu, Kejian Tong, Tao Ning, Sichen Zhao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Illinois Urbana-Champaign Urbana USA；University of Illinois Urbana-Champaign；Syracuse University San Jose USA；Syracuse University；Northeastern University Boston USA；Northeastern University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00413v1) · [PDF 下载](https://arxiv.org/pdf/2609.00413v1) · **关键词** 链式思维压缩, 金融推理, 语义分段, 依赖图, 受约束片段选择, 逻辑连贯性, 可审计推理<br>


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

本文旨在通过依赖感知的结构化压缩，在显著缩短金融推理链的同时，尽量保留答案正确性、关键计算依赖与可审计的论证连续性。

**不用术语来说**：金融问题往往需要同时阅读文字证据、完成数值计算并说明判断依据。完整写出所有思考步骤虽然有助于答对和复核，却会增加推理延迟、内存占用与服务成本；直接缩短回答又可能删掉后续计算所依赖的关键步骤，使结果无法验证。论文要解决的是：怎样只保留真正必要的推理内容，而不是简单地把文本截短或改写得更简略。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出分层语义蒸馏框架：先将完整推理链划分为语义片段，再构建有向依赖图并结合问题感知表示评估片段重要性，从而把压缩决策建立在推理结构而非单纯文本相似度上。
- 将全局约束选择与局部边界重写结合：前者在长度预算和依赖约束下选择片段，后者修复删除片段后相邻内容的衔接；冻结的大语言模型仅用于语义特征提取和最终答案生成，使压缩过程保持结构化与可解释。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型多步推理与推理链压缩的交叉方向。链式思维通过显式生成中间步骤，帮助模型组合文本证据、数值计算与规则解释，但较长的推理轨迹也会增加推理延迟、内存占用和服务成本；这一矛盾在强调正确性与可审计性的金融任务中尤其突出。本文关注的不是长上下文本身的高效编码，也不是从头生成更短的答案，而是对一条已经完成的推理链进行结构化压缩：在减少长度的同时，保留后续计算所依赖的关键步骤、数值依据和可追溯的论证关系。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**链式思维（Chain-of-Thought, CoT）**

模型在给出最终答案前显式写出的多步推理过程。它通常能改善复杂任务的求解质量，但过长的中间轨迹会提高计算与部署成本。

</div>
<div class="concept-item" markdown="1">

**语义分段**

把完整推理链划分为若干各自表达相对完整含义的片段，例如证据提取、公式选择、数值计算或结论推导。以片段而非单个词元为压缩单位，更容易保留完整的逻辑步骤。

</div>
<div class="concept-item" markdown="1">

**依赖图**

用有向图表示推理片段之间的前置关系：若一个片段的结论被另一个片段使用，就建立相应的依赖边。压缩时考虑这种结构，可避免保留后续结论却删除其必要依据。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道需要多步金融推理的问题及其已生成的完整推理链；任务是选择并保留其中对回答问题、维持数值正确性和支持后续步骤必要的语义片段，再对删除片段造成的局部衔接断裂进行轻量改写，输出更短但逻辑连贯的推理链，并据此生成最终答案。本文假定完整链可以先被划分为语义单元，单元之间能够构造成有向依赖关系，而且压缩受到长度预算与依赖约束：不能仅依据局部词元显著性删除内容，因为金融计算中的一个看似次要步骤可能是后续计算或审计说明的必要前提。冻结的 Qwen3 4B 仅用于提取语义特征和生成最终答案，压缩决策本身由可解释的分段、建图、重要性评分与受约束选择流程完成。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **TR-BERT 与 PoWER-BERT**: 两者通过任务相关的动态词元删减或逐层淘汰低影响词向量来降低推理成本，说明自适应压缩具有可行性；但其决策主要基于局部词元重要性，没有显式建模多步推理片段之间的逻辑依赖，因此可能删除金融推理中被后续计算使用的前置步骤。
- **HeterSumGraph**: 该工作利用图表示捕捉文档级关系，为用结构信息进行内容选择提供了直接背景。本文将类似的图结构思想用于推理链压缩，重点不再是一般文档摘要，而是保留与最终答案、数值计算及论证连续性有关的推理依赖。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在高风险金融应用中，模型既要整合文本证据、数值计算和合规解释，又要满足严格的正确性与审计要求。长推理链能够展示较完整的判断过程，但会提高延迟、内存使用和在线服务成本，限制其在真实系统中的部署；如果为了效率粗暴删减，又可能破坏计算依据或审计所需的证据链。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **直接答案生成**：模型不展开或只展开很少的中间推理步骤，直接根据问题生成最终答案，因此输出短、推理成本较低。
- **完整思维链与审慎式推理**：完整思维链显式保留多步推导；更高级的审慎式策略则搜索或比较不同推理路径，以提高复杂任务中的推理质量。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 直接生成虽然高效，但容易省略关键逻辑步骤；在金融计算中，被省略的步骤可能正是后续数值结果的依据，因而降低答案可靠性和可审计性。
- 完整思维链过于冗长，而审慎式推理主要改善推理路径搜索，并未明确解决如何压缩一条已经完成的推理链，同时保存步骤之间的依赖结构与数值忠实性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种面向已生成金融推理链的结构化压缩机制：它不仅要判断哪些片段重要，还要识别“后一步依赖前一步”的关系，并在给定长度预算下避免删除被保留结论所必需的前提。与此同时，压缩结果还需保持语言连贯，并提供可检查的选择过程。

</div>
<div markdown="1"><span>核心问题</span>

能否把完整金融推理链表示为语义片段及其有向依赖关系，再在长度和依赖约束下进行全局片段选择，从而减少中间推理文本与推理成本，同时尽量维持最终答案准确性、数值依据和逻辑连贯性？

</div>
<div markdown="1"><span>作者直觉</span>

推理链中的句子并非彼此独立：某个中间数值、条件判断或证据引用，可能是后续结论的必要前提。若把推理看成依赖图，压缩就类似于在预算有限时保留支撑最终结论的关键路径，而非逐句判断是否“看起来重要”。删除非关键分支后，只需在新相邻片段的边界进行轻量改写，便可能以较小改动恢复可读性，同时避免让生成模型自由重写整条推理而引入新的数值或逻辑偏差。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

HSDN将输入问题与原始长推理链视为“需要在长度预算下保留关键证据的结构化压缩”问题。完整流程先用BiLSTM-CRF把连续推理文本切成语义片段，再以片段为节点预测有向无环依赖图；随后，双编码器结合问题相关性、片段内容和图中心性得到重要度，并通过带前置依赖约束的动态规划选择片段；最后，仅在因删除片段而形成的断裂边界处进行受复制机制约束的局部改写，得到压缩推理链。冻结的Qwen3-4B不直接决定删留，而只负责提供语义特征及依据压缩链生成最终答案，因此压缩依据可追溯到片段分数、依赖边和预算约束。
直观地说，该方法不是逐词删除看似冗余的内容，而是先把一份财务推导拆成若干完整步骤，再画出“哪个步骤依赖哪个步骤”的流程图，最后在字数限制内保留得分高且前提齐全的步骤。这样可以避免只留下结论却删掉计算依据；局部改写只负责把相邻保留步骤接顺，不承担重新推理，从而降低引入新数字或新事实的风险。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 语义片段切分

BiLSTM同时编码每个位置的前后文，前馈层产生“边界/非边界”发射分数，线性链CRF再联合解码全局一致的边界序列。数值跨度检测器禁止在连续金额、百分比或多词数值表达内部设置边界，表格单元边界辅助任务则帮助模型识别结构化数据引用。

<div class="method-step__io" markdown="1">

**输入**：长度为$T$的原始推理词元序列$\mathbf{c}=(c_1,\ldots,c_T)$。<br>
**输出**：按原顺序排列的$K$个语义片段$\mathbf{S}=(s_1,\ldots,s_K)$，每个片段成为后续图建模与选择的原子单位。

</div>

**直观理解**：这一步类似先把一份解题草稿切成“读取表格、计算变化率、核对法规、得出结论”等完整步骤，而不是机械地按句号切开。尤其不能把“增长$12.5\%$”之类的数值表达拆成两段，否则后续删除会破坏计算含义。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 依赖图构建

对每个片段内的词元表示做均值池化并经残差投影得到节点向量；双仿射打分器预测有向边$s_i\rightarrow s_j$，表示$s_j$的推理需要$s_i$提供的信息。路径增强项补偿远距离依赖，训练时用可微无环正则抑制环，推理时删除检测到的环中概率最低的边。

<div class="method-step__io" markdown="1">

**输入**：语义片段集合$\mathbf{S}$及冻结语言模型为各词元提供的中间层表示。<br>
**输出**：有向无环依赖图$\mathcal{G}=(\mathcal{V},\mathcal{E})$及每条候选依赖边的概率。

</div>

**直观理解**：图中的箭头表示“后一步离不开前一步”，例如最终利润率依赖先前得到的利润和收入。将这些关系显式化后，系统若保留最终结论，就必须连同其必要前提一起保留，而不能只凭局部措辞判断。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问题条件化的重要度评分

问题编码器先产生上下文化表示；每个片段通过跨注意力定位问题中与自身相关的词元，再将片段表示、问题相关表示、二者逐元素交互以及长度、位置、数值指示和图中心性等特征融合为重要度$I_k\in(0,1)$。图特征包含PageRank，用于提高被多个后续步骤依赖的基础片段的保留优先级。

<div class="method-step__io" markdown="1">

**输入**：问题$\mathbf{x}$、各片段节点表示以及依赖图$\mathcal{G}$。<br>
**输出**：每个片段$s_k$对应的问答相关重要度$I_k$。

</div>

**直观理解**：同一段推理是否重要取决于当前问题：若问题询问合规性，法规核对比中间修辞重要；若问题询问收益率，数值计算链更重要。PageRank还会提醒模型，有些看似不直接回答问题的步骤其实是许多后续结论的共同地基。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 依赖约束下的片段选择

先对有向无环图做拓扑排序，再用动态规划求解带前置依赖的背包式优化：最大化保留片段的重要度总和，同时限制总长度，并要求选择任一片段时也选择其所有依赖片段。论文给出的时间复杂度为$O(KL_{\mathrm{budget}})$，依赖检查通过预处理父节点位掩码实现。

<div class="method-step__io" markdown="1">

**输入**：片段长度$|s_k|$、重要度$I_k$、依赖边集合$\mathcal{E}$和长度预算$L_{\mathrm{budget}}$。<br>
**输出**：二元选择向量$\mathbf{z}\in\{0,1\}^K$及按原始顺序排列的保留片段。

</div>

**直观理解**：这不是按分数从高到低贪心删除，而是在固定字数中整体寻找最有价值且逻辑闭合的一组步骤。某个高分结论如果需要两个前置计算，算法会把三者的联合成本纳入预算，而不会留下没有依据的孤立结论。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 依赖约束下的预算选择目标

$$
\begin{aligned}\max_{\mathbf{z}\in\{0,1\}^{K}}\quad &\sum_{k=1}^{K}z_k I_k\\\text{s.t.}\quad &\sum_{k=1}^{K}z_k|s_k|\le L_{\mathrm{budget}},\\&z_j=1\implies z_i=1,\quad \forall(s_i,s_j)\in\mathcal{E}.\end{aligned}
$$

**符号说明**

- $\mathbf{z}$：片段选择向量，其中每个分量为二元变量。
- $z_k$：片段$s_k$是否保留的指示变量，取$1$表示保留。
- $K$：语义片段总数。
- $I_k$：双编码器为片段$s_k$预测的重要度。
- $|s_k|$：片段$s_k$的词元长度。
- $L_{\mathrm{budget}}$：允许压缩链占用的最大长度预算。
- $\mathcal{E}$：依赖图中的有向边集合；边$(s_i,s_j)$表示$s_j$依赖$s_i$。

<div class="equation-explanation" markdown="1">

**直观理解**：目标函数希望保留片段的重要度总和尽可能大；第一条约束控制压缩后的总长度，第二条约束保证任何被保留的后续步骤都不会失去必要前提。它形式化了论文最核心的决策：不是单独判断每段删不删，而是在预算与逻辑完整性之间进行全局组合优化。<br>
**原文位置**：第4.3.2节，公式(17)–(19)

</div>

</div>

<div class="equation-block" markdown="1">

#### 端到端准确性—压缩率奖励

$$
R=\mathbb{1}[\mathrm{correct}]\left(1+\beta\frac{|\mathbf{c}|-|\mathbf{c}^{*}|}{|\mathbf{c}|}\right)-\mathbb{1}[\neg\mathrm{correct}]\rho
$$

**符号说明**

- $R$：端到端强化学习奖励。
- $\mathbb{1}[\cdot]$：条件成立时取$1$、否则取$0$的指示函数。
- $\mathrm{correct}$：冻结语言模型依据压缩链生成的最终答案是否正确。
- $\mathbf{c}$：原始未压缩推理链。
- $\mathbf{c}^{*}$：经过选择和边界改写后的压缩推理链。
- $\beta$：正确答案条件下压缩收益的权重。
- $\rho$：答案错误时施加的惩罚强度。

<div class="equation-explanation" markdown="1">

**直观理解**：只有答案正确时，缩短推理链才会带来额外奖励；一旦压缩导致错误，模型直接受到惩罚。这一设计避免优化器仅追求极端短文本，并使片段选择最终对下游答案负责，而不仅是拟合人工或合成的重要度标签。<br>
**原文位置**：第4.5.3节，公式(29)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练分三阶段。第一阶段分别预训练基础组件：分段器最小化CRF负对数似然$\mathcal{L}_{\mathrm{seg}}=-\log P(\mathbf{y}^{*}|\mathbf{c})$，其中$\mathbf{y}^{*}$是人工标注边界；依赖图预测器使用由大语言模型标注得到的合成依赖数据预训练；边界改写器则从正确推理链中随机移除片段，构造合成断裂边界进行训练，使其学习修复局部衔接而不依赖完整压缩流水线的潜在错误。
第二阶段联合训练重要度评分器和图预测器，目标为$\mathcal{L}_{\mathrm{joint}}=\mathcal{L}_{\mathrm{score}}+\lambda_1\mathcal{L}_{\mathrm{edge}}+\lambda_2\mathcal{L}_{\mathrm{DAG}}$。其中$\mathcal{L}_{\mathrm{score}}$用“仍能产生正确答案的最小片段子集”所导出的oracle标签监督$I_k$，$\mathcal{L}_{\mathrm{edge}}$监督依赖边概率，$\mathcal{L}_{\mathrm{DAG}}$惩罚环路；第三阶段使用REINFORCE优化片段选择策略$\pi_\theta(\mathbf{z}\mid\mathbf{x},\mathbf{c})$，并以近期奖励的指数移动平均$b$作为基线降低梯度方差。整体上，监督学习先教会模型识别边界、依赖和重要片段，强化学习再按最终答案正确性与实际压缩收益校准选择行为。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 金融感知的BiLSTM-CRF分段器**

双向LSTM为每个词元编码左右上下文，CRF利用标签转移分数联合确定边界，而非独立判断每个位置。解码时，若位置位于仍在延续的数值跨度内，则将转入边界标签的分数置为负无穷；分段器还通过表格单元边界检测辅助任务进行预训练，以适应表格引用和结构化数据描述。

> 直观理解：后续图的节点就是这些片段，所以错误切分会贯穿整个系统：片段过碎会使依赖图复杂，片段过长又会把关键内容与冗余内容绑在一起。数值保护尤其重要，因为金融推理中的金额、百分比和计算式必须作为完整证据保留或删除。

**2. 依赖图与双编码重要度模块**

冻结Qwen3-4B的中间层词元表示经片段内均值池化和可训练残差投影后形成节点表示；头节点与依赖节点分别通过MLP变换，再由双仿射函数预测边概率。片段重要度同时融合问题跨注意力、片段自身语义、逐元素交互、数值和位置特征以及PageRank等图中心性，使“直接相关性”和“作为其他步骤前提的结构价值”进入同一评分。

> 直观理解：只比较片段与问题的文字相似度，可能删掉“先算出分母”这类不直接复述问题、却是答案必需的中间步骤。依赖图负责说明逻辑前提，问题注意力负责说明任务相关性，二者结合才适合多步财务计算与合规核验。

**3. 受约束选择与保守边界重写模块**

动态规划在长度预算内优化片段集合，并用依赖闭包约束保证被选节点的父依赖均被选中。对选择后出现的非原始相邻片段，仅处理固定窗口边界；指针式复制分布限制生成偏离输入，语义相似度验证失败时采用安全回退，因此文本流畅性优化与事实选择相互分离。

> 直观理解：选择器决定“哪些推理事实必须留下”，改写器只决定“留下的事实怎样接得自然”，职责分离提高了可解释性。若改写结果看起来可能改变原意，系统宁可使用普通连接词，也不让流畅性凌驾于事实可靠性。

**训练与推理**

训练时，冻结Qwen3-4B，不对其参数反向传播；可训练部分包括BiLSTM-CRF分段器、片段残差投影、双仿射依赖预测器、问题编码与重要度评分器，以及轻量边界改写器。先完成组件预训练，再联合优化重要度、边预测和无环约束，最后在完整问答回路中根据答案正确性与压缩比例进行强化学习微调。依赖图训练阶段使用合成边标注，重要度监督来自oracle最小正确子集，因此这些监督信号并非都由人工直接验证，解释结果时应注意其潜在标注偏差。
推理时，输入问题$\mathbf{x}$与完整推理链$\mathbf{c}$。系统依次完成语义切分、冻结Qwen3-4B特征抽取、依赖边预测和去环、问题条件化重要度评分、拓扑排序及预算动态规划；随后按原始顺序恢复所选片段，只改写被删除区间两侧的边界，并执行嵌入相似度检查。得到$\mathbf{c}^{*}$后，将其与问题共同输入同一个冻结Qwen3-4B生成答案；因此最终输出包括可检查的片段选择与依赖依据、压缩推理文本以及答案。

**复现信息**

论文使用冻结的Qwen3-4B承担两项功能：从其$32$层中的第$16$层提取词元表示，以及在压缩结束后生成最终答案。作者称中间层在语义抽象与表层细节之间取得经验性平衡；冻结模型则减少训练显存并避免灾难性遗忘，但这也意味着报告的压缩效果与该固定特征空间及生成器能力相关。
边界改写仅查看相邻保留片段两侧各$15$个词元，避免让改写器重新生成整条推理；答案解码采用温度$\tau=0.7$、核采样$p=0.9$，并用于best-of-5评估。复杂度方面，分段为$O(T)$，全片段对的依赖预测为$O(K^2)$，预算选择为$O(KL_{\mathrm{budget}})$；由于通常$K\ll T$，结构化模块的主要新增成本来自片段图构建和动态规划，而总体计算仍主要由冻结语言模型的特征提取与答案生成占据。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- $AFAC2025$ 基准：论文将其作为金融推理评测数据集，用于比较答案正确性、推理链压缩率和逻辑依赖保持情况。原文未明确报告数据规模、训练集、验证集或测试集划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Best-of-5 accuracy（最佳五次准确率）**

对每个问题生成五个输出；只要其中一个输出与参考答案匹配，该问题即计为正确。其形式为 $\text{Acc}=\frac{1}{N}\sum_{i=1}^{N}\mathbb{1}\left[\bigvee_{j=1}^{5}\text{Match}(o_{i}^{(j)},\mathcal{R}_{i})\right]$，其中 $N$ 是样本数，$o_i^{(j)}$ 是第 $i$ 个样本的第 $j$ 个输出，$\mathcal{R}_i$ 是参考答案。 （越高越好，因为它衡量模型最终答案是否正确；但最佳五次设置允许从五个样本中挑出正确答案，不能等同于单次生成准确率。）

</div>
<div class="metric-item" markdown="1">

**Compression ratio（压缩率，$CR$）**

衡量压缩后推理链相对于原始推理链减少了多少长度，定义为 $\text{CR}=1-\frac{\sum_{i=1}^{N}|\mathbf{c}_{i}^{*}|}{\sum_{i=1}^{N}|\mathbf{c}_{i}|}$，其中 $\mathbf{c}_i$ 是原始推理链，$\mathbf{c}_i^{*}$ 是压缩后的推理链，$|\cdot|$ 表示长度。 （越高表示节省的推理链长度越多，通常有利于降低推理成本；但单独追求高 $CR$ 可能损害答案正确性或逻辑完整性，因此应与准确率和连贯性一起观察。）

</div>
<div class="metric-item" markdown="1">

**Reasoning coherence score（推理连贯性分数，$RCS$）**

比较原始推理图与压缩推理图所保留的依赖边，定义为 $\text{RCS}=\frac{1}{N}\sum_{i=1}^{N}\frac{|\mathcal{E}(\mathcal{G}_{i})\cap\mathcal{E}(\mathcal{G}_{i}^{*})|}{|\mathcal{E}(\mathcal{G}_{i}^{*})|}$，其中 $\mathcal{G}_i$ 和 $\mathcal{G}_i^{*}$ 分别表示原始与压缩推理图，$\mathcal{E}(\cdot)$ 表示图中的依赖边集合。 （越高越好，表示压缩后保留了更多被评估为关键的逻辑依赖；它衡量结构保持情况，不直接保证最终答案正确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### $HSDN$ 在 $AFAC2025$ 上的整体性能

<div class="result-value" markdown="1">

作者报告 $HSDN$ 的最佳五次准确率为 $91.0\%$，压缩率为 $68.4\%$。

</div>

这表明该方法在论文所用基准上同时实现了较高的答案正确性和较大幅度的推理链缩短。它支持“压缩并不必然破坏任务性能”的作者主张，但不能单凭该结果证明方法在其他金融数据集、单次采样设置或不同基础模型上同样有效。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the AFAC2025 benchmark, HSDN achieves 91.0% accuracy with 68.4% compression, outperforming strong compression baselines in overall score and reasoning coherence.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### $HSDN$ 与强推理链压缩基线的综合比较

<div class="result-value" markdown="1">

作者称 $HSDN$ 在综合竞赛分数和推理连贯性方面优于强压缩基线，但所给材料没有列出基线名称、各方法的具体分数或差值。

</div>

该结果若得到完整表格支持，说明 $HSDN$ 不只是提高压缩率，而是在错误惩罚和依赖保持同时存在的评测协议下取得更好的折中。不过当前材料缺少逐项数值，因此无法判断优势大小、统计稳定性或是否对所有基线都成立。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the AFAC2025 benchmark, HSDN achieves 91.0% accuracy with 68.4% compression, outperforming strong compression baselines in overall score and reasoning coherence.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 表 1 的主比较与消融研究

<div class="result-value" markdown="1">

原文明确说明表 1 同时呈现 $AFAC2025$ 上的主比较和消融研究，但所提供摘录未包含表 1 的具体行、数值或消融设置。

</div>

因此可以确认作者设计了统一表格来检验整体方法和各组件作用，但无法从当前材料判断哪些组件被移除、性能如何变化，也不能据此作出关于组件必要性的定量结论。

<div class="result-source" markdown="1">

来源：Section 6, Experiment Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 1 presents the main comparison and ablation study on the AFAC2025 benchmark.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 已有推理链压缩方法：这是最直接的比较对象，用于检验 $HSDN$ 的改进是否来自其依赖图建模、重要性评分和结构化选择，而不只是来自使用语言模型。具体基线名称及其实现细节，原文未明确报告。

**实验想回答的问题**

- 在 $AFAC2025$ 金融推理基准上，$HSDN$ 能否在显著压缩推理链的同时保持答案准确性与推理连贯性？
- 与已有推理链压缩方法相比，图依赖引导的分段选择与边界重写是否能改善综合性能？

**实验实现**

论文摘要说明，冻结的 $Qwen3$ 4B 模型仅用于特征提取和最终答案生成，压缩过程本身不更新该模型，而是由结构化流程完成。该流程包括语义分段、依赖图构建、双编码器重要性评分、受约束的片段选择和局部边界重写。评测遵循挑战赛协议，并使用最佳五次准确率、压缩率、竞赛分数和推理连贯性分数；但原文所给章节未明确报告采样温度、提示模板、硬件、随机种子、训练规模及具体基线配置。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It develops dependency-aware chain-of-thought compression that preserves financial reasoning accuracy while reducing inference-token cost.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`75b4b7b44ddf5087b8a41ef076a85391ce6fddeb4e981e05b4ecdf1f0e93c106`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
