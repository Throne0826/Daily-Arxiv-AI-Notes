---
title: "[论文解读] Structured but Fragile: On the Limits of LLMs in Cybersecurity Decision-Making"
description: "[arXiv 2608.20966][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.20966"
announcement_date: "2026-08-24"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-24T02:08:45.905578+00:00"
source_sha256: "3479240b4a2f9c4eb7d000463d9d89468d407cfba5a9c05cbd5708a5a97390ce"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "LLM 其他"
  - "大语言模型"
  - "网络安全决策"
  - "攻击图"
  - "防御组合选择"
  - "Stackelberg 安全博弈"
  - "结构化推理"
  - "预算约束"
  - "提示 framing 敏感性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.20966</p>

# Structured but Fragile: On the Limits of LLMs in Cybersecurity Decision-Making

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Pasquale Malacaria, Yunxiao Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Electronic Engineering and Computer Science, Queen Mary University of London, London, UK；Affiliation: Department of Computer Science, University of Exeter, Exeter, UK</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20966v1) · [PDF 下载](https://arxiv.org/pdf/2608.20966v1) · **关键词** 大语言模型, 网络安全决策, 攻击图, 防御组合选择, Stackelberg 安全博弈, 结构化推理, 预算约束, 提示 framing 敏感性<br>


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

本文位于网络安全决策支持与大语言模型（LLM）交叉领域。网络安全决策的核心是在攻击者具有对抗性、资源有限且信息不完备的条件下，选择安全控制措施以降低组织资产遭受攻击的风险。本文特别关注：当攻击场景被显式表示为攻击图，并且防御者受到预算约束时，LLM 是否能够依据攻击路径和攻击者—防御者相互作用进行结构化决策，而不是仅凭熟悉的安全术语、通用经验或提示语境作答。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**攻击图（attack graph）**

攻击图用节点表示攻击者所处的状态，用有向边表示从一个状态到下一个状态所需执行的攻击步骤。它把可能的攻击路径显式化，因此防御者可以判断哪些节点或边位于关键路径上，并选择能够阻断这些路径的控制措施。

</div>
<div class="concept-item" markdown="1">

**Stackelberg 安全博弈**

这是一种先后行动的对抗模型：防御者先提交防御策略，攻击者观察后选择对自己最有利的攻击响应。本文将其作为规范性优化基线，用明确的攻击者—防御者权衡计算理想防御组合，而不是把某个专家标签直接当作答案。

</div>
<div class="concept-item" markdown="1">

**结构化决策**

结构化决策是指根据明确的对象、约束、目标和关系进行推理；在本文中，具体表现为在给定攻击图和预算下选择一组安全控制，使攻击者成功的风险尽可能低。它不同于只识别威胁或生成一般性安全建议，因为控制选择必须与攻击拓扑及资源约束一致。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

对每个现实威胁场景，输入包括一个攻击图、可选防御控制及其资源或成本信息、预算水平，以及用于评估的攻击者—防御者目标。场景覆盖勒索软件、供应链攻击、云滥用、POS 恶意软件、Kubernetes 攻击和 ICS/OT 入侵等七类情形。LLM 的任务是在预算约束下输出防御组合（defence portfolio），即所选控制措施的集合；随后，LLM 生成的组合及其他候选策略会在受控条件下被评价，并与博弈论优化基线比较。问题的基本假设是攻击图能够描述主要攻击路径，防御控制可以影响攻击者成功概率或路径可达性，而优化基线所使用的目标能够代表结构化决策的规范参照。本文并不假设 LLM 的高分必然意味着其理解了攻击结构，而是进一步检验结果是否会因图复杂度、提示措辞、策略命名、语义信息和抽象程度改变。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$G$**

攻击图，包含表示攻击状态的节点和表示攻击步骤的边。

</div>
<div class="notation-item" markdown="1">

**$D$**

防御组合，即一次决策中被选择部署的安全控制集合。

</div>
<div class="notation-item" markdown="1">

**$B$**

防御预算，限制可选择控制措施的总资源或总成本。

</div>
<div class="notation-item" markdown="1">

**$p_{m succ}$**

攻击者成功到达目标的概率或相应风险量；防御优化的目标是使其尽可能降低。

</div>

</div>

**直接相关的工作**

- **Stackelberg security games 与概率攻击图上的网络安全投资模型**: 相关研究将网络安全投资建模为双层的攻击者—防御者优化问题：防御者先配置资源，攻击者再作最佳响应，并使用攻击图表示潜在攻击路径。本文沿用这种结构化决策思想，但将其作为独立的规范性基线，用来检验 LLM 的防御选择是否接近明确目标下的优化解，而不是只比较通用安全知识。
- **CyberAlly**: CyberAlly 将 LLM 与网络安全知识图谱结合，以支持蓝队事件响应并减少幻觉，代表了通过外部知识增强 LLM 网络安全能力的路线。本文关注的问题不同：即使模型拥有大量网络安全知识，是否仍能在显式攻击图、预算约束和攻击路径权衡下稳定作出结构化决策。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

网络安全防御需要在预算有限时，从多种安全控制中选择组合，以阻断攻击者沿攻击路径推进。大型语言模型已被用于威胁分析和缓解规划，但若将其用于防御决策，必须确认其给出的方案确实依据攻击结构和防御目标，而不是仅凭对多因素认证、网络隔离等常见措施的熟悉程度作出表面上合理的判断。若模型受到提示措辞、策略名称或问题规模的影响，安全决策支持系统就可能产生难以察觉且风险较高的偏差。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于大型语言模型的安全决策**：将威胁场景、攻击步骤和候选防御控制提供给模型，由模型直接提出防御组合，或比较不同组合的优劣。其优势是能够处理自然语言描述，并可能利用已有的网络安全知识；但这种方法通常难以区分模型是否真正理解了攻击路径。
- **基于博弈论和优化的防御选择**：把攻击者与防御者之间的权衡形式化：防御者在预算约束下选择安全控制，优化目标是降低攻击成功风险。该方法提供明确、可计算的评价标准，因此可作为检验大型语言模型是否遵循结构化目标的规范性参照，而不是被视为现实世界中唯一正确的防御方案。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 已有大型语言模型研究往往关注模型能否生成看似合理的安全建议，却没有充分区分结构化推理与通用领域先验之间的作用。其后果是，模型在攻击图发生变化、问题规模增大或输入表述改变时，可能仍给出语言上自信但不符合具体攻击结构的方案。
- 单纯比较模型输出或依赖主观专家判断，难以判断方案是否接近明确的风险最小化目标，也难以系统检测评估过程中的命名和措辞偏差。特别是，若评估者会因策略被标为“最优”而提高评分，评价结果就不能可靠反映防御方案本身的质量。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种受控的研究框架，能够同时检验大型语言模型在攻击图防御选择中的结构化决策能力、对图复杂度和提示表述的鲁棒性，以及其评价判断是否与形式化优化目标一致。具体而言，尚不清楚模型是在小规模且结构明确时真正近似风险优化，还是只是在熟悉的安全控制和表面标签引导下产生合理答案；也不清楚这种能力能否稳定迁移到更复杂的攻击图和不同表达方式。

</div>
<div markdown="1"><span>核心问题</span>

在给定攻击图、预算约束和候选安全控制的条件下，大型语言模型能否依据攻击结构稳定地选择并评价低风险防御组合，使其行为接近博弈论优化参照，而不是被图复杂度、提示框架、策略命名或一般网络安全知识所主导？

</div>
<div markdown="1"><span>作者直觉</span>

攻击图把原本开放式的安全建议转化为显式的结构化决策问题：模型可以沿着攻击者状态和攻击步骤识别关键路径，再把有限预算优先投入能够切断这些路径的控制。因此，在图较小、结构和目标都清楚时，语言模型可能表现出接近优化方案的能力。但这种能力依赖模型是否持续使用给定结构；当图变复杂或提示改变时，熟悉的安全常识和语言线索可能比具体风险关系更容易被模型调用，所以需要用独立的优化参照和受控扰动来检验其可靠性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

方法将网络安全决策建模为基于攻击图的 Stackelberg 安全博弈：输入组织系统的攻击图 $G=(V,E)$、可部署控制集合 $C$、预算 $B$ 以及控制有效性参数 $\theta$，输出满足预算的防御组合 $s$。对每个候选组合，模型计算攻击者在所有源节点到目标节点路径中的最大成功概率，并以最小化该最坏情况风险的优化解 $s^*$ 作为规范性参照，再将 LLM 的防御选择与该参照比较。直观地说，系统先把攻击者可能经过的路线画成图，再在有限经费下选择能够最大程度堵住最危险路线的安全措施；这里的“最优”只表示相对于给定图和参数的模型最优，并不等同于现实世界中已验证的真值。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建威胁场景与攻击图

将攻击阶段表示为节点与边，形成攻击图 $G=(V,E)$；为每个场景列出可用安全控制、控制成本、间接成本、有效性，以及每条边适用的控制集合。

<div class="method-step__io" markdown="1">

**输入**：来自真实事件或官方攻击链分析的威胁场景，包括 ICS/OT 入侵、双重勒索、软件供应链攻击、云基础设施滥用、零售 POS 攻击和 Kubernetes 平台入侵。<br>
**输出**：一个可解释、可人工检查的概率攻击图实例，包含源节点、目标节点、候选控制及其与攻击边的对应关系。

</div>

**直观理解**：这一步类似绘制一张从“入侵入口”到“最终破坏目标”的路线图，并在每条路旁标注可以部署的防火墙、MFA、分段、备份或检测措施。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 定义控制作用与风险函数

若边 $e$ 没有适用控制，则其残余成功概率为 $p_e(s;\theta)=\pi_e$；若有控制，则将基础概率乘以 $s$ 中所有适用控制的有效性值，假设控制独立且以乘法方式作用。对每条源到目标路径计算边概率乘积，并取攻击者最优路径的最大值作为风险。

<div class="method-step__io" markdown="1">

**输入**：攻击图 $G$、防御组合 $s\subseteq C$、控制有效性参数 $\theta$，以及每条边的基础攻击成功概率 $\pi_e$。<br>
**输出**：候选防御组合 $s$ 的风险值 $R(s;\theta)$，表示攻击者在该防御下成功到达目标的最坏情况概率。

</div>

**直观理解**：一条攻击路线只有在每一步都成功时才会成功，因此把各步概率相乘；攻击者会挑选最容易成功的路线，所以防守方必须关注最危险的那一条。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 求解规范性防御组合

求解 $s^*\in\arg\min_{s\in\mathcal{S}(B)}R(s;\theta)$，即在不超过预算的所有控制组合中选择风险最低者。小图可用穷举搜索；大规模实例采用将路径概率乘积取对数、转化为线性和，并通过路径流约束、内层攻击者线性规划对偶化得到混合整数线性规划的方法。

<div class="method-step__io" markdown="1">

**输入**：风险函数 $R(s;\theta)$、可行策略集合 $\mathcal{S}(B)$ 和预算约束 $B$。<br>
**输出**：模型意义下的最优策略 $s^*$ 及其风险，用作比较 LLM 决策是否体现结构化推理的规范性基准。

</div>

**直观理解**：它相当于把所有可负担的防守方案逐一或高效地比较，找出最能压低最危险攻击路线成功率的方案；高效求解器避免在大型图上真的枚举全部组合。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 获得并评估 LLM 防御决策

要求 LLM 在预算限制下选择安全控制，并比较不同 LLM 的策略及其与优化基准的接近程度；进一步通过改变提示措辞或策略标签测试其对 framing 的敏感性，并要求 LLM 为同一优化问题生成求解器以考察其能否实现高层问题 formulation。

<div class="method-step__io" markdown="1">

**输入**：结构化攻击图、控制清单、预算和相应任务提示，以及用于评价候选策略的攻击图实例。<br>
**输出**：LLM 选出的控制组合、对策略的排序或评价，以及 LLM 生成的求解器实现；这些输出用于分析结构化能力、鲁棒性和计算可扩展性。

</div>

**直观理解**：不仅看模型能否给出一个看起来合理的方案，还检查它是否会因换一种说法就改变判断，以及它能否把自己的思路真正写成可运行的算法。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 最坏情况攻击风险

$$
R(s;\theta)=\max_{\pi\in\Pi(G)}\prod_{e\in\pi}p_e(s;\theta)
$$

**符号说明**

- $R(s;\theta)$：防御策略 $s$ 和控制有效性参数 $\theta$ 下的安全风险，即攻击者到达目标的最坏情况成功概率。
- $\Pi(G)$：攻击图 $G$ 中从源节点 Node 0 到指定目标节点的全部路径集合。
- $\pi$：路径集合中的一条具体攻击路径。
- $e$：攻击图中的一条边，表示一个攻击步骤或状态转移。
- $p_e(s;\theta)$：在防御策略 $s$ 下攻击者成功 traversing 边 $e$ 的残余概率。

<div class="equation-explanation" markdown="1">

**直观理解**：先把某条攻击路径上每一步的成功概率相乘，得到攻击者走完该路径的概率；再在所有路径中取最大值，因为攻击者会选择最有利的路线。该式将防御效果归结为降低最危险路径的成功率。<br>
**原文位置**：第 3 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 预算约束下的最优防御目标

$$
s^{*}\in\arg\min_{s\in\mathcal{S}(B)}R(s;\theta)
$$

**符号说明**

- $s^*$：模型下的最优防御控制组合。
- $s$：从可用控制集合 $C$ 中选出的控制子集，满足预算限制。
- $\mathcal{S}(B)$：在预算 $B$ 下所有可行防御策略的集合。
- $B$：防御投资或可选择控制数量等形式的预算约束。
- $\arg\min$：返回使风险函数达到最小值的策略，而不只是返回最小风险数值。

<div class="equation-explanation" markdown="1">

**直观理解**：防御方要在买得起的方案中选择风险最低的组合。这个目标不是声称该组合在现实中绝对正确，而是提供一个统一、可重复的比较标准，用来判断 LLM 的选择离模型最优有多远。<br>
**原文位置**：第 3 节，公式（2）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文不是训练新的 LLM，也未给出模型参数更新、监督标签或梯度训练目标；因此训练目标不适用。研究目标是评估现有 LLM 在给定攻击图和预算下能否进行结构化防御选择，并将其输出与 $\arg\min$ 风险的规范性优化解比较。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 概率攻击图与控制映射**

攻击图 $G=(V,E)$ 的路径集合为 $\Pi(G)$，每条边 $e$ 都关联可作用于该边的控制。控制的残余成功概率在文中按独立乘法组合；未部署适用控制时采用 $\pi_e=1$ 的假设，因此基础边概率不会额外降低。

> 直观理解：该模块把抽象的安全风险拆成一系列可检查的攻击步骤，并明确每项防御措施究竟能阻断哪一步。

**2. 最坏路径风险与 Stackelberg 优化**

防御方先提交满足预算的策略，攻击方随后选择成功概率最大的路径，构成防御方最小化、攻击方最大化的双层决策。原始路径风险是概率乘积，研究采用对数变换、路径流建模和内层线性规划对偶化，将问题重写为可由通用求解器处理的混合整数线性规划。

> 直观理解：防守方不能假设攻击者会走平均路线，而要按攻击者最聪明、最有利的路线来设计防御；线性化则让大型问题能够在合理时间内计算。

**3. LLM 决策与生成求解器评估**

实验把 LLM 输出视为待评估的防御策略，而不是直接视为真实最优解，并以博弈优化结果作为规范性参照。评估还操纵图复杂度、提示 framing、策略标签，并比较 LLM 生成实现与专用求解器的计算表现。

> 直观理解：这一模块区分“模型能读懂并模仿结构”与“模型能稳定地依据结构作出判断”：前者可能在简单、明确的表示下出现，后者还要求对复杂度和措辞变化保持稳定。

**训练与推理**

训练阶段：原文未明确报告对 LLM 进行任何训练或微调。推理阶段以结构化威胁场景、攻击图、控制信息和预算作为输入，要求 LLM 生成防御组合或评价候选策略；研究者改变图复杂度、提示 framing 和策略标签，观察输出稳定性，并另行要求 LLM 生成同一优化问题的求解器。专用博弈求解器则根据攻击图和参数计算规范性解；文中说明其游戏论解通常在数秒内完成，而 LLM 生成的方案通常每个实例需要数分钟，但该比较的完整硬件、软件和调用配置原文未明确报告。

**复现信息**

攻击图实例来自七类威胁场景，规模从 ICS/OT 入侵的 $6$ 个节点、$6$ 条边、$2$ 条路径和 $5$ 个控制，到 Kubernetes 场景的 $30$ 个节点、$38$ 条边、$44$ 条路径和 $17$ 个控制；这些规模是为了保持可解释和可人工检查，而非测试攻击图优化的最大可扩展性。控制可表示预防、限制、检测、响应或影响缓解措施，例如 MFA、分段、EDR、SIEM、备份和数据外泄防护；每个控制的具体数值、成本表、提示模板、LLM 型号、采样设置及完整评估协议在所提供章节中原文未明确报告。为研究计算可扩展性，论文另行使用规模递增的自动生成攻击图，但其生成过程和参数在所提供方法章节中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 七个来自真实威胁场景的攻击图，覆盖勒索软件、供应链入侵、云滥用、Kubernetes 攻击、POS 恶意软件和 ICS/OT 入侵等类型；它们用于测试方法在不同攻击拓扑和复杂度下的决策能力。攻击图 $G_1$ 仅设置三个预算等级，$G_2$ 至 $G_7$ 各设置四个预算等级，共形成 27 个图—预算场景和 216 个防御策略。
- 每个图—预算场景中的防御组合数据，包括控制措施名称、强度等级、direct_cost、indirect_cost 以及以 H/M/L 表示的 effectiveness/confidence；这些信息构成 LLM 防御者和评价者的输入。原文未明确报告各攻击图的节点数、边数和数据集划分比例。
- 由同一批攻击图和防御组合生成的匿名评价样本；四个 LLM 评价者对每个预算下的八类防御方案进行比较，聚合后每个防御者获得 108 次评价。该部分不是独立数据集，而是用于测量评价稳定性和评价—风险一致性的实验样本。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**形式化风险 $R$**

部署控制后所有可行源—目标攻击路径中最大剩余攻击成功概率，即 $R=\max_{p\in\mathcal{P}}\Pr(p)$；它衡量最危险路径仍然有多大风险。 （越低越好，因为防御目标是降低最坏攻击路径的残余概率。）

</div>
<div class="metric-item" markdown="1">

**LLM 平均评价分数**

将评价标签 excellent、very good、good、average、bad、very bad 分别映射为 6、5、4、3、2、1，再对评价取算术平均；它反映匿名 LLM 评价者认为某策略相对安全和有效的程度。 （越高越好，但它是比较性评价信号而非安全风险的真实标签，不能单独证明策略在现实网络中更安全。）

</div>
<div class="metric-item" markdown="1">

**Spearman 秩相关系数 $\rho$**

比较形式化风险排序与 LLM 平均评价排序的一致性；由于低风险应对应高评价，负相关表示更强的一致性。 （在本实验定义下，越负越好；绝对值较大的负值表示 LLM 评价更接近风险最小化排序。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 总体防御策略比较：七个攻击图、不同预算等级及四个 LLM 评价者的聚合评价

<div class="result-value" markdown="1">

Optimal 的平均评价分数最高，为 4.82；Gemini、Grok 和 ChatGPT 紧随其后，分别为 4.63、4.56 和 4.51；Claude 为 4.29。Coverage 和 Greedy 分别为 3.91 和 3.55，Poor 为 1.76。原文还指出，LLM 防御者在较小的图 $G_1$ 至 $G_4$ 上形成接近最优的风险簇，但在较大图上与最优解的差距明显扩大。

</div>

结果支持“条件性能力”而非普遍可靠性：当攻击图较简单且结构显式给出时，LLM 能作出接近形式化优化器的选择；但复杂度增加后，性能差距扩大。该结果只说明在本文的表示方式、预算和风险映射下存在接近性，不能证明 LLM 已经稳定掌握真实网络防御，也不能把 Stackelberg 解视为现实世界的绝对真值。

<div class="result-source" markdown="1">

来源：Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Optimal 43.5% 21.3% 16.7% 11.1% 6.5% 0.9% 4.82

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 形式化风险与 LLM 评价的排序一致性

<div class="result-value" markdown="1">

各攻击图的风险—评价 Spearman 相关均为负，但一致性随图编号和复杂度总体减弱：$G_1$ 为 $-0.867$，$G_2$ 为 $-0.581$，$G_3$ 为 $-0.731$，$G_4$ 为 $-0.558$，$G_5$ 为 $-0.355$，$G_6$ 为 $-0.315$，$G_7$ 为 $-0.266$；表中相应 $p$ 值均小于 0.01。作者据此认为 LLM 评价通常捕捉到风险方向，但复杂图上的排序一致性显著变弱。

</div>

负相关说明评价者并非完全依赖表面名称，通常能把较低形式化风险的方案排得更高；相关绝对值下降则表明复杂结构使这种判断更脆弱。相关性仍不是因果证明，也不能说明每个策略的绝对评价正确，因为评价者本身就是被测对象，且风险值依赖人为设定的效果映射。

<div class="result-source" markdown="1">

来源：Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

1 − 0.867 3.49 × 10−4

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 评价提示的 framing 变化：移除“risk reduction”措辞，并进一步改用数值评分

<div class="result-value" markdown="1">

在 Exp. 2 中，Gemini、Optimal、ChatGPT、Grok、Claude、Greedy、Coverage 和 Poor defender 的平均分依次为 4.65、4.59、4.55、4.31、4.28、3.92、3.70 和 2.17；在 Exp. 3 中依次为 4.81、4.74、4.71、4.58、4.46、4.55、4.25 和 3.32。相较主协议中 Optimal 的最高地位，Exp. 2 和 Exp. 3 中 Gemini 排在 Optimal 之前，且 Greedy 的分数明显升高。

</div>

同一批策略仅因评价任务不再明确要求按风险降低判断，或改用不强制区分度的数值评分，就出现排序变化，说明 LLM 评价对措辞和输出格式敏感。尤其是 Greedy 只看控制效果、忽略拓扑，却可能因“effectiveness、budget efficiency、coverage”这类表述获得偏高评价；因此提示设计本身可能改变实验结论，而不是只改变表达风格。

<div class="result-source" markdown="1">

来源：Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Greedy 3.92 4.55

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- Stackelberg 优化基线依赖准确的控制效果数值和特定的 H/M/L 到风险的映射，而现实中获得这类估计通常困难；因此它是规范性参照而非经过现实验证的最优答案。
- LLM 评价者只提供比较性信号，且匿名面板仍可能受提示措辞、评分标签和模型自偏好影响；实验没有提供独立的人类安全专家真值、真实部署后的攻击结果或跨数据集划分验证，因此不能把评价分数直接解释为现实安全收益。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Optimal（Stackelberg）：在给定形式化模型和数值风险映射下求得的精确解，用作结构化决策的规范性上界或理论下界；它不等同于经过现实验证的最优防御，因为其效果估计可能并不准确。
- Greedy：按控制措施 effectiveness 从高到低选择，直到预算用尽；它测试只依据单项效果、忽略攻击图拓扑的简单启发式。
- Coverage：按控制措施覆盖的攻击图边数从高到低选择；它测试只利用结构覆盖、忽略控制效果的另一种单准则启发式。
- Poor defender：在满足至少消耗 80% direct-cost 预算的可行控制子集中，通过穷举选择会产生显著攻击者风险的组合；它提供一个刻意构造的低质量下界，用于检验评价协议能否识别明显糟糕的策略。

**实验想回答的问题**

- 在给定攻击图、控制措施及双重预算约束时，LLM 能否选择接近 Stackelberg 优化解的防御组合，并且这种能力是否随攻击图复杂度变化？
- LLM 对防御策略的评价是否与形式化风险一致，以及评价结果是否会受到任务措辞、评分方式和策略呈现方式的影响？

**实验实现**

LLM 防御者每个攻击图调用一次提示，输入攻击者起点、目标节点、逐边攻击结构、适用控制及两类成本，并同时要求其在 tight、moderate、comfortable、generous 四个预算等级下输出控制子集和理由。LLM 只能看到 H/M/L 的效果—置信度组合，不能看到优化器使用的数值映射，因此它并未直接求解同一个数值优化问题。定量防御者使用从 H/H 到 L/L 的单点数值映射计算风险。随后，ChatGPT、Claude、Gemini 和 Grok 四个 LLM 评价者看到攻击图及八个匿名防御组合，按风险降低、最危险路径保护、预算利用率和未覆盖路径进行排序并分配唯一标签；作者对部分异常案例进行人工检查，但该检查不是独立的人类真值评估。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 定性表示与定量表示的分离：LLM 仅接收 H/M/L 效果—置信度标签，优化器使用隐藏的数值映射 | 实验刻意不向 LLM 防御者和评价者公开数值映射；优化器使用 H/H = 0.1、H/M = 0.2、H/L = 0.3、M/H = 0.4 直至 L/L = 0.9 的单点映射。作者报告，在这种表示不一致下仍观察到 LLM 策略与优化基线的趋同。 | 该设计隔离了“共享同一个数值目标”这一可能的捷径：LLM 不能直接复现优化器，只能依据定性安全常识和攻击图结构作判断。因此接近最优更能说明表示之间存在决策趋同，但也意味着结论依赖作者指定的定性标签语义和数值映射，不能推出 LLM 真正恢复了隐藏的数学目标。 | Section 5.0.6, Qualitative vs Quantitative Representations<br><span class="experiment-evidence">The numerical mapping is never disclosed to the LLMs (not even to the evaluation panel)and is used by the optimizer to define a precise objective.</span> |
| 预算等级分解：比较 tight、moderate、comfortable 和 generous 下的评价区分能力 | Optimal 在 moderate（B2）预算下平均分最高，为 5.43，Gemini 和 Grok 均为 4.82；在 comfortable（B3）预算下，ChatGPT 为 4.79，高于 Optimal 的 4.75；在 tight（B1）和 generous（B4）预算下，Optimal 分别为 4.71 和 4.29。 | 中等预算提供了较多但仍需权衡的组合选择，因此最能检验结构化优化；预算极紧时多数方案都受到强约束，预算很宽松时多数合理方案都能覆盖主要风险，两种情况下策略差异都更难被评价者辨别。该分析解释了总体分数为何不能简单理解为所有预算条件下的稳定优势。 | Table 4<br><span class="experiment-evidence">Optimal 4.71 5.43 4.75 4.29</span> |

**定性案例**

- Claude 是最能说明评价脆弱性的案例：作为防御者时，它在形式化风险上实际上最接近最优解，但获得的 LLM 评价分数却低于其他 LLM 防御者，差异在最大攻击图上尤其明显。作者的人工检查认为，Claude 选择了单项 effectiveness 标签看似较弱、但整体路径风险接近最优的控制组合；这表明复杂攻击图中评价者可能依赖浅层局部启发式，未能识别跨多条攻击路径的全局收益。该解释由作者的诊断性检查支持，但原文未报告独立人类评审或额外真实网络验证。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：系统评估 LLM 在攻击图防御决策中的结构化推理、脆弱性和提示敏感性，并与优化基线比较。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`3479240b4a2f9c4eb7d000463d9d89468d407cfba5a9c05cbd5708a5a97390ce`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
