---
title: "[论文解读] PertMind: Eliciting Emergent Biological Reasoning in LLM via Reinforcement Learning on Cellular Perturbation Data"
description: "[arXiv 2608.16419][LLM Reasoning] PertMind将公共细胞扰动图谱中的实验终点转化为可自动验证的强化学习奖励，以较少人工推理标注训练大语言模型，并检验由此学到的生物学推理策略能否迁移到训练目标之外的任务。"
arxiv_id: "2608.16419"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:17:35.704138+00:00"
source_sha256: "30e1bcc3dcb5d4a084c3e1008288511b38c6a43de18f73863f8e886119fdaca4"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "细胞扰动图谱"
  - "差异基因表达"
  - "大语言模型"
  - "可验证结果强化学习"
  - "生物学推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.16419</p>

# PertMind: Eliciting Emergent Biological Reasoning in LLM via Reinforcement Learning on Cellular Perturbation Data

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Zhenchao Tang, Xiaogang Xu, Tianxu Lv, Jiahui Guan, Jiale Zhou, Haohuai He, Zhi Song, Hanbo Huang, Jiehui Huang, Jiafei Wu, Zhe Liu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.16419) · [PDF 下载](https://arxiv.org/pdf/2608.16419) · **关键词** 细胞扰动图谱, 差异基因表达, 大语言模型, 可验证结果强化学习, 生物学推理<br>
**项目页**: [https://shapsider.github.io/PertMind/](https://shapsider.github.io/PertMind/)

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

PertMind将公共细胞扰动图谱中的实验终点转化为可自动验证的强化学习奖励，以较少人工推理标注训练大语言模型，并检验由此学到的生物学推理策略能否迁移到训练目标之外的任务。

**不用术语来说**：给定一种药物、一个细胞环境和一个目标基因，模型不仅要判断该基因会升高、降低还是基本不变，还应理解药物作用如何经过通路和调控网络传递到最终反应。这类能力对药物机制研究、靶点筛选和功能基因组学有价值，但目前若要训练模型给出可靠的机制推理，通常需要专家逐步撰写或审核大量推理过程；面对数量庞大的药物、基因与细胞组合，这种监督方式难以扩展。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出一种“扰动实验即训练环境”的监督接口：把细胞扰动图谱中实测的基因上调、下调或无可靠变化作为可计算的终点奖励，使训练规模能够随实验图谱扩展，而不必为每个样本人工编写完整机制推理链。
- 提出PertMind训练框架，以可信轨迹监督初始化模型，再联合基因终点、通路方向和输出格式三类强化信号；作者进一步用未参与后训练的任务考察其是否形成可复用的生物学推理策略，而非只记住正向扰动预测的标签规律。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

细胞扰动研究关注药物等干预如何改变细胞状态，是机制导向药物发现、靶点优先级排序和功能基因组学的重要基础。一次响应通常由药物作用机制、通路传播、基因调控和细胞背景共同决定；公共扰动图谱通过大规模单细胞实验记录这些干预及其终端基因表达变化。大语言模型虽已从预训练中获得广泛生物医学知识，并能生成自然语言机制解释，但通用预训练不能直接判断某条看似合理的解释是否符合特定药物、基因和细胞系组合的实验结果。本文因此把实验测得的扰动终点转化为可自动验证的强化学习反馈，使模型在不依赖逐步人工机制标注的条件下学习扰动响应推理。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**细胞扰动图谱**

将药物、基因编辑等干预施加于不同细胞背景，并系统测量干预后细胞状态的数据集合。本文使用其差异表达统计，把大量“药物—细胞系—目标基因”组合自动转换为可训练、可评分的查询。

</div>
<div class="concept-item" markdown="1">

**差异基因表达**

比较扰动组与对照组后，判断某个基因的表达量是否显著升高、降低或没有可靠变化。本文将这种实验统计压缩为 Up、Down 或 No 三类终端标签，而不是要求模型精确预测连续表达量。

</div>
<div class="concept-item" markdown="1">

**基于可验证结果的强化学习**

模型生成推理和答案后，由能够自动核验的最终结果计算奖励，再据此更新生成策略，无须为每个中间推理步骤提供标准答案。本文的可验证结果来自实验测量，而非人工编写的问答标签。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

基本样本可表示为扰动药物 $d$、细胞系 $c$ 与目标基因 $g$ 的组合；模型接收围绕该组合构造的基因中心自然语言查询，需要结合药物机制、通路传播、基因调控及细胞背景进行推理，并输出目标基因响应 $y_{d,c,g}$，其类别为 Up、Down 或 No，分别表示上调、下调或无可靠变化。监督终点来自 Tahoe-100M 图谱预先计算的差异表达统计，具体查询结果在生成时不向模型泄露，只用于训练后的自动评分。该设置只直接训练正向扰动响应预测，即由干预条件推断基因响应；论文随后以未参与该后训练目标的任务检验所得策略能否迁移，但这些迁移任务不属于本节基本问题定义。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$d$**

施加于细胞的化合物或药物扰动。

</div>
<div class="notation-item" markdown="1">

**$c$**

接受扰动的细胞系或具体细胞背景。

</div>
<div class="notation-item" markdown="1">

**$g$**

需要预测表达响应的目标基因。

</div>
<div class="notation-item" markdown="1">

**$y_{d,c,g}\in\{\mathrm{Up},\mathrm{Down},\mathrm{No}\}$**

药物扰动、细胞背景与目标基因三元组对应的实验终端标签，依次表示上调、下调或无可靠变化；该符号是依据引言中的任务描述作出的统一记号，原文未正式定义符号。

</div>

</div>

**直接相关的工作**

- **BioReason**: 该工作通过人工整理的生物学任务训练多模态逐步推理，说明生物推理能力可以通过后训练塑造；与本文相比，其专家轨迹和目标理由成本较高，也会预先规定哪些中间步骤属于正确推理。
- **OwkinZero**: 该工作已将可验证奖励强化学习用于面向生物发现的整理式问答，但训练目标仍需人工决定和编写；PertMind改用扰动实验直接测得的终端响应作为奖励接口，使训练环境可随公共实验图谱扩展。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

细胞对化学扰动的反应由药物机制、通路传播、基因调控和细胞背景共同决定。实际研究希望模型能把干预与这些跨尺度因素联系起来，从而支持机制导向的药物发现、靶点优先级判断和功能基因组学分析；然而，公共扰动图谱虽然积累了大量实验测量，却尚未被充分转化为训练自然语言生物学推理的可扩展监督。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **端点或结构化预测模型**：扰动响应系统，包括基于大语言模型的推理框架和非大语言模型的深度学习方法，通常以明确的实验终点或结构化标签为训练目标，例如预测某个基因在特定扰动和细胞环境下的响应类别。这类方法能够学习输入到结果的映射，但通常不会直接评价模型生成的机制性自然语言是否真正导向实验一致的结论。
- **人工策划的生物学推理后训练**：BioReason、Bio-KCoT以及面向可验证问答的强化学习方法，通过专家编写的任务、逐步推理轨迹、目标解释或知识图谱事实来塑造模型推理；其共同思路是先由人规定值得训练的问题或合理的中间步骤，再据此实施监督学习或可验证奖励优化。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 专家撰写的推理轨迹和目标依据成本高，难以覆盖扰动图谱中大量药物、基因与细胞背景组合；结果是训练数据规模受人工策划能力限制，而不是随持续增长的实验数据同步扩展。
- 人工轨迹会预先规定哪些中间步骤属于“正确机制”，策划式问答也需要人决定哪些问题值得作为训练目标。这既把机制假设写入监督信号，也可能使模型适应固定任务形式，而不能证明其从实验结果中提炼了可迁移的生物学策略。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种同时满足三项要求的训练接口：直接利用公共扰动实验而非逐条人工策划样本；只凭可测量的终点结果自动判分而无需完整标注潜在机制链；并能促使模型联合利用药物、通路、基因和细胞背景，而非依赖实体身份或类别先验。更关键的是，仍需通过未出现在后训练中的任务验证这种终点监督是否产生了可复用推理能力。

</div>
<div markdown="1"><span>核心问题</span>

当模型只能依据隐藏于查询之外的实验终点获得奖励，并仅在正向的“扰动条件到目标基因响应”任务上接受后训练时，强化学习能否从预训练模型原本分散的候选答案与知识中集中出更有效的生物学推理策略，并使这些策略零任务特定后训练地迁移到反向条件识别、组合扰动、表型筛选、过程解释及多尺度表征任务？

</div>
<div markdown="1"><span>作者直觉</span>

一次扰动实验可以看作复杂生物级联过程的压缩结果：模型看不到完整的中间机制，但最终基因响应同时受药物作用、通路传递、基因调控和细胞环境影响。若训练覆盖许多不同组合，依靠单一药物身份、基因身份或总体类别频率的捷径就难以持续得分；终点奖励会反复筛选那些能够综合多种因素的生成策略。作者还指出，基础模型的采样分布中已经存在正确答案，只是贪心解码或简单多数投票不能稳定选中，因此强化学习的作用更像是提高有效策略被采用的概率，而不是从零注入全部生物知识。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PertMind将细胞扰动下的基因响应预测建模为一个知识增强的推理策略学习问题。输入是查询三元组$x=(c,d,g)$，其中$c$为细胞系，$d$为小分子扰动，$g$为目标基因；模型输出目标基因的三分类方向$\hat{y}_g\text{，即}$Up、Down或No，并同时生成可审计的自然语言机制解释和候选通路方向。整体流程以Qwen3-4B Base为起点，先从Tahoe-100M构造细胞系严格隔离的监督数据，再用知识检索和可信轨迹进行一次监督微调，最后以路径响应代理信号辅助GRPO强化学习。直观地说，模型不仅要猜基因最终向上、向下还是没有可靠变化，还要先对扰动可能经过的通路作结构化判断；通路信号为最终答案之间的中间步骤提供额外反馈，但当前样本的真实表达结果始终只用于训练评分，不展示给模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 扰动数据清洗与标签构造

将共享药物身份的剂量和实验板记录按附录规则合并，删除缺失统计量及统计功效不足的记录，并依据预先固定的显著性、效应量和基线表达阈值赋予Up、Down、No或ambiguous标签；ambiguous样本被排除。随后按细胞系划分训练/开发域与测试域，保证$\C_{train}\cap C_{test}=\emptyset$。

<div class="method-step__io" markdown="1">

**输入**：Tahoe-100M提供的细胞系、药物、剂量、实验板和基因的伪批量差异表达统计，包括$\Delta_{c,d,g}$、$\q_{c,d,g}$和$\mu_{c,d,g}$。<br>
**输出**：训练查询集合$\D_{train}$及其标签和置信度权重$\w^{conf}_{c,d,g}$；测试细胞系为C32、HepG2C3A、HOP62、Hs 766T和PANC-1。

</div>

**直观理解**：先把实验统计结果转换成模型可以学习的三种方向，同时把不够可靠的记录剔除。按细胞系而不是按单条样本切分，检验模型能否迁移到完全未见过的细胞背景。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 知识增强与可信轨迹初始化

从PubChem、DrugBank、UniProt、Gene Ontology、Reactome、STRING和CORUM组装上下文$\K(x)$，Qwen3-4B Base针对每个查询采样$M$条候选推理轨迹；仅保留最终标签正确、格式唯一、没有声称访问隐藏表达值、实体关系有证据支持且包含“扰动靶点—通路—目标基因”完整链条的轨迹。

<div class="method-step__io" markdown="1">

**输入**：训练查询$x$、仅来自训练分区的生物知识图谱和按Up、Down、No分层检索的历史支持案例$\S(x)$。<br>
**输出**：可信轨迹语料$\D^{traj}$，并用其进行一轮带Balanced Fine-Tuning加权的SFT，得到$\pi_{theta}^{SFT}$，该策略同时作为GRPO初始策略和KL正则的冻结参考策略。

</div>

**直观理解**：强化学习初期如果模型很少给出合乎格式的答案，只有最终对错的反馈会很稀疏。因此先挑出“答案对、理由有依据、格式完整”的模型回答进行示范训练，让后续强化学习从一个会按要求推理的起点开始。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选通路与奖励侧代理构造

为部分查询选择至多三个包含$g$的候选通路，并在训练评分阶段使用通路中除目标基因外的成员$P\setminus\{g\}$计算转录响应代理标签$\y^P_{c,d,g}\in\{Up,Down,No,uncertain\}$；代理标签依据同一剂量和实验板条件下的显著性加权效应、方向一致性、活跃成员比例及跨条件共识得到。候选通路、名称、药物/基因关系和代表性非目标成员可放入提示，但代理方向、表达统计量和哪些通路有确定标签不得放入提示。

<div class="method-step__io" markdown="1">

**输入**：药物$d$、目标基因$g$、Reactome通路注释及与药物机制和目标基因相关的、与当前表达结果无关的证据。<br>
**输出**：奖励侧的确定通路集合$\P_{det}(c,d,g)$及其代理标签；无法可靠判断的通路保留为uncertain并不获得通路奖励。

</div>

**直观理解**：模型可以看到“哪些通路可能相关”以及通路中的代表成员，但看不到这些成员这次实验究竟升了还是降了。这样通路标签可以作为教师在后台检查中间判断，又不会把正确答案直接泄露给模型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 路径监督GRPO优化

分别计算最终基因正确性奖励、确定通路方向平均正确率和格式奖励，并按查询内响应组进行奖励标准化；将标准化优势输入带裁剪重要性权重的策略目标，同时施加相对于冻结$\pi_{theta}^{SFT}$的采样词元KL惩罚，并在完整样本目标上乘以$\w^{conf}_{c,d,g}$。

<div class="method-step__io" markdown="1">

**输入**：当前策略针对每个查询采样的$G$个结构化回答，每个回答包含候选通路方向、机制解释和最终基因标签。<br>
**输出**：经过置信度加权、KL约束和路径辅助奖励优化的PertMind策略。

</div>

**直观理解**：同一个问题生成多个答案后，模型主要学习“这一组里哪个答案更好”，而不是依赖不同任务之间不可比的奖励尺度。最终答案仍是最高优先级，通路和格式只提供有限的辅助分数；实验依据较弱的样本对参数更新影响更小。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 三分类响应标签规则

$$
y_g=\begin{cases}\mathrm{Up},&q_{c,d,g}\le 0.05\land\Delta_{c,d,g}\ge 0.585,\\\mathrm{Down},&q_{c,d,g}\le 0.05\land\Delta_{c,d,g}\le -0.585,\\\mathrm{No},&|\Delta_{c,d,g}|<0.20\land q_{c,d,g}\ge 0.50\land \mu_{c,d,g}\ge 10,\\\mathrm{ambiguous},&\mathrm{otherwise}.\end{cases}
$$

**符号说明**

- $y_g$：目标基因的离散响应标签，取Up、Down、No或ambiguous。
- $\Delta_{c,d,g}$：细胞系$c$在药物扰动$d$下目标基因$g$的log2FoldChange。
- $q_{c,d,g}$：经多重检验校正的显著性值padj。
- $\mu_{c,d,g}$：目标基因的baseMean表达水平。

<div class="equation-explanation" markdown="1">

**直观理解**：只有同时满足显著性和足够大的效应量时，才判定基因明确上调或下调；只有变化很小、显著性证据弱且基线表达足够高时，才判为No。其余情况不强行归类，以减少噪声标签。<br>
**原文位置**：式(4)，第2.2节

</div>

</div>

<div class="equation-block" markdown="1">

#### 复合响应奖励

$$
R(o_i)=R_{gene}(o_i)+\lambda_{pw}m_{pw}R_{pw}(o_i)+\lambda_{fmt}R_{fmt}(o_i)
$$

**符号说明**

- $R(o_i)$：第$i$个响应$o_i$的总奖励。
- $R_{gene}(o_i)$：最终基因标签奖励，若模型标签与实验标签$y_g$一致则为1，否则为0。
- $R_{pw}(o_i)$：确定候选通路方向的平均正确率；没有确定通路时规定为0。
- $m_{pw}$：通路奖励掩码，当确定通路数量大于0时为1，否则为0。
- $R_{fmt}(o_i)$：格式奖励；所有必需字段、合法标签和唯一终止答案均满足时为1，否则为0。
- $\lambda_{pw},\lambda_{fmt}$：通路奖励和格式奖励的权重，均为正，且两者之和小于1。

<div class="equation-explanation" markdown="1">

**直观理解**：最终基因方向是核心评分，通路方向和输出格式只提供受限的辅助奖励。因为辅助权重之和小于1，即使一个错误的基因答案在通路和格式上都完美，也不可能超过一个正确的基因答案。<br>
**原文位置**：式(11)及第2.4节

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：PertMind的优化分为初始化和主优化两部分。初始化阶段在可信轨迹集合$\D^{traj}$上进行一轮BFT加权SFT，得到结构化且有证据依据的$\pi_{theta}^{SFT}$；主阶段从该策略开始执行路径监督GRPO。对每个查询，当前策略采样$G$个响应，使用复合奖励计算组内标准化优势$\hat{A}_i=(R(o_i)-\mathrm{mean}_jR(o_j))/(\mathrm{std}_jR(o_j)+\epsilon)$，再优化带裁剪重要性权重的策略代理目标和相对于冻结$\pi_{theta}^{SFT}$的采样词元KL惩罚。每个查询的完整样本目标统一乘以其置信度权重$\w^{conf}_{c,d,g}$；该权重不改变同一响应组内的相对排序，只调节该查询对整体更新的影响。若一组响应的总奖励完全相同，则组内方差为零并不产生梯度。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 知识检索上下文模块**

模块从开放世界生物知识图谱和训练分区支持案例构造$\K(x)$，支持案例按Up、Down、No分层检索，以避免多数类证据压制少数类。检索池排除当前查询及其重复测量，并不访问验证或测试细胞系的结果。

> 直观理解：它为模型提供药物、基因和通路之间的已知关系及训练历史，类似先查阅资料再回答；严格限制检索范围是为了防止模型间接看到测试答案。

**2. 可信轨迹SFT初始化模块**

Qwen3-4B Base对知识增强提示采样候选轨迹，经过五项可信度过滤后形成$\D^{traj}$，再进行一轮BFT加权SFT。BFT改变标准SFT中样本和词元的权重，不构成独立训练阶段；所得$\pi_{theta}^{SFT}$还固定为RL的KL参考。

> 直观理解：强化学习前先用高质量示范教会模型遵守输出格式、引用证据和组织机制链条。它解决的是“模型是否会按规则推理”，而不是直接替代后续的强化学习目标。

**3. 路径监督GRPO奖励模块**

GRPO不使用学习得到的价值网络，而对同一查询的$G$个响应按总奖励计算组内标准化优势。总奖励由基因终端奖励、带掩码的通路奖励和格式奖励组成；通路奖励只检查结构化方向字段，不检查自由文本机制解释的逐句蕴含，也不提供词元级因果信用。

> 直观理解：除了检查最终基因方向是否正确，模块还检查模型对若干中间通路方向的判断，从而提供更密集的学习信号；但它不会假装能够验证整段自然语言解释的所有因果细节。

**训练与推理**

训练时，先将Tahoe-100M伪批量差异表达记录转为细胞系、药物、目标基因查询，并按固定阈值生成标签和置信度；随后只利用训练分区检索知识和历史案例，生成并过滤可信轨迹，执行一轮SFT。对有候选通路的训练查询，在不查看当前查询表达结果的前提下构造通路响应代理标签；当前策略对知识增强提示采样多条回答，后台依据最终基因标签、通路方向和格式计算奖励，再通过置信度加权、组内优势标准化、裁剪策略更新和对SFT参考策略的KL约束进行GRPO训练。推理时，给定未见细胞系、药物和目标基因，检索允许使用的外部知识及训练分区证据，将其与查询和候选通路信息组成提示；模型生成通路方向、机制解释和唯一的最终Up、Down或No标签。推理提示不包含当前查询的差异表达统计、基因标签、通路代理方向或测试结果，因此模型需要根据知识和已见案例作条件化判断。

**复现信息**

可复现和公平解释结果所必需的设置包括：训练与测试按细胞系隔离，五个测试细胞系在最终评估前保持封闭；所有阈值、通路参数、检索规则和模型选择决策仅由开发域确定；Tahoe-100M的主标签直接使用预计算的DESeq2-style伪批量统计，不重新从单细胞表达矩阵估计。每个查询最多选择三个Reactome候选通路，通路代理计算时排除目标基因，并在同一剂量和实验板条件内汇总后进行保守的跨条件共识；uncertain通路不进入奖励分母。格式要求包括完整的通路方向字段、机制解释字段和唯一终止答案。文中未给出BFT闭式目标、完整裁剪策略公式、KL估计式以及具体超参数；这些内容被放在附录A中，当前节选不足以补全。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Tahoe-100M 扰动图谱用于正向扰动响应训练和评测。作者先按细胞系划分样本，将 C32、HepG2C3A、HOP62、Hs 766T 和 PANC-1 的全部样本保留为最终测试域，其余细胞系构成开发域；开发域中的合格细胞系、药物、基因三元组按 90:10 划分训练集与验证集，并保证相同三元组不会跨分区。该设计允许药物和基因在训练域与测试域重复，但测试时的细胞环境从未参与训练，主要检验跨细胞环境泛化。
- Schmidt 原代人 T 细胞 CRISPRa/CRISPRi 数据集用于逆向扰动条件预测。模型接收源细胞与目标细胞之间的上调、下调差异表达基因，并在每个查询的 69 个候选扰动中排序真实干预；该数据集检验从“扰动预测响应”向“响应反推扰动”的迁移能力。
- Norman Perturb-seq 数据集用于组合扰动评测，包含 131 个双扰动组合，候选池由 105 个单基因扰动组成。评测分别记录两个真实基因的排名，不因只找回其中较容易的一个而给予完整成功判定；PertMind 未使用双扰动样本进行任务适配，因此该设置重点检验组合推理与零样本迁移。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

衡量分类预测中标签完全正确的样本比例；本文将其用于差异表达检测、调控方向预测及 Top-1 等正确识别场景。该指标直观，但在类别不均衡时可能被高频类别主导。 （越高越好，因为更高值表示更多样本被正确分类。）

</div>
<div class="metric-item" markdown="1">

**Macro-F1 / F1**

F1 综合精确率与召回率；Macro-F1 先分别计算各类别 F1，再进行不按类别频率加权的平均，因此能检查模型是否兼顾少数类别。逆向任务中的 F1 则用于概括候选扰动识别质量。 （越高越好，因为高值要求精确率与召回率同时较好；Macro-F1 还要求不同类别上的表现较均衡。）

</div>
<div class="metric-item" markdown="1">

**候选排名与 Top-k 准确率**

Top-1 或 Top-5 准确率衡量真实扰动是否出现在排名首位或前五位；Norman 评测进一步保留两个真实扰动基因各自的完整排名，以观察模型能否同时找回组合中的两个成分。 （Top-k 准确率越高越好，而真实扰动的名次数值越低越好，因为更小名次代表候选被排在更靠前的位置。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 五个未见细胞系上的 VCWorld 正向扰动响应评测

<div class="result-value" markdown="1">

作者报告，PertMind 在差异表达检测与调控方向预测的 Accuracy 和 Macro-F1 上，平均达到或略微超过基于 Gemini-2.5-Flash 的 VCWorld 参照，并在多数细胞系设置中领先。

</div>

这表明在参数规模较小的 Qwen3-4B 上加入细胞扰动监督，能够明显改善跨细胞环境的正向响应预测。分析上，由于药物和基因可以跨域重复，该实验主要支持“对新细胞环境的泛化”，并不等同于对全新药物或全新基因的零样本泛化；作者也明确说明，该结果本身不能证明能力必然是涌现的，更不能证明模型学到了真实生物因果机制。

<div class="result-source" markdown="1">

来源：第 4.1 节，Figure 3a

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

PertMind matched or modestly exceeded this Gemini-based reference on average across both tasks and evaluation metrics, and it outperformed the reference in a majority of the held-out cell-line settings.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Schmidt 原代 T 细胞数据集上的逆向扰动条件预测

<div class="result-value" markdown="1">

作者报告，只接受过正向扰动响应后训练的 PertMind，在 Top-1、Top-5 和 F1 上接近任务专用 CellNavi，并明显优于同源 Base 与 SFT 模型；该迁移不包含逆向任务的额外微调。

</div>

正向任务要求从干预推断表达变化，逆向任务则从表达变化反推干预，两者并非相同的输入输出映射。因此，超过 Base 和 SFT 说明收益不能仅归因于原始语言知识或监督适配。它与跨任务能力一致，但“接近专用模型”仍不是超过专用模型，也不能单凭一次迁移实验确定该能力在严格定义下属于涌现。

<div class="result-source" markdown="1">

来源：第 4.2 节，Figure 4b

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Although PertMind had been post-trained only for forward perturbation-response prediction, it approached the performance of the task-specialized CellNavi model across Top-1 accuracy, Top-5 accuracy, and F1 score (Figure 4b).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Norman Perturb-seq 双基因组合扰动排名

<div class="result-value" markdown="1">

作者报告，CellNavi 更擅长将组合中较容易识别的第一个真实基因排到前列，而 PertMind 改善了第二个真实基因的排名，并减小两个目标之间的排名失衡。

</div>

该结果关注的是能否同时恢复组合中的两个扰动成分，而不是只命中一个显著目标。PertMind 的优势更像是组合恢复的均衡性，而非对所有真实基因排名的全面领先。作者提出语言模型的组合推理先验可能解释这一现象，但这只是解释性假设；实验没有直接隔离预训练组合能力，也没有证明其机制。

<div class="result-source" markdown="1">

来源：第 4.2 节，Figure 4d

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

CellNavi ranked the easier first perturbation more highly, whereas PertMind improved the rank of the second perturbation and reduced the imbalance between the two targets.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 给定节选主要提供定性比较而没有 Figure 3 和 Figure 4 的具体数值或完整表格，因此无法核验优势幅度、不同细胞系上的实际波动以及逆向任务与 CellNavi 的精确差距；Figure 3b 还明确缺少运行级误差条。论文报告的标准差也不是置信区间或显著性检验。
- 测试集隔离的是细胞系而非药物和基因，因而正向实验支持未见细胞环境泛化，却不能直接推出对全新分子实体的泛化。逆向及组合结果与跨任务涌现相一致，但尚未通过机制实验排除训练统计关联、预训练知识或提示敏感性等替代解释。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- VCWorld（Gemini-2.5-Flash）是正向扰动响应任务的主要大语言模型参照。它使用闭源且规模明显更大的模型，因而可用于判断 4B 参数 PertMind 是否能凭借领域后训练进入强通用模型的性能区间。
- Qwen3-4B Base 与 BFT 加权 SFT 构成同源模型对照：Base 衡量原始预训练知识，SFT 衡量可信轨迹监督微调本身的收益，由此可区分强化学习带来的增量是否超出普通监督适配。
- CellNavi 是逆向细胞状态转移任务的专用基线，其驱动基因预测器在 CRISPR 筛选数据上经过微调。它与无需逆向任务微调的 PertMind 对比，可检验通用提示式迁移和任务专用训练之间的差异。
- GEARS 是基于扰动表达建模的基线，被用于 Schmidt 单扰动和 Norman 组合扰动评测；它提供了非大语言模型方法的参照，帮助判断 PertMind 的结果是否仅来自语言模型已有的文本知识。

**实验想回答的问题**

- 在严格按细胞系隔离训练与测试数据的条件下，基于细胞扰动监督进行后训练，能否提高大语言模型对未见细胞环境中差异表达与调控方向的预测，同时避免通用语言能力发生灾难性遗忘？
- 只针对正向扰动响应训练的 PertMind，能否在无任务特定微调的情况下迁移到逆向扰动条件识别及双基因组合扰动推断，从而表现出跨任务生物学推理能力？

**实验实现**

PertMind 从 Qwen3-4B Base 初始化。可信轨迹阶段每个训练查询生成 8 个候选回答，仅保留通过全部验证器的轨迹；随后进行一轮 BFT 加权 SFT 和三轮 GRPO。最终比较 Base、SFT、打乱通路标签、仅基因终局奖励、仅在提示中加入通路上下文，以及完整 PertMind 六种同源变体。所有阈值、通路候选和超参数只在训练与验证域选择，并在最终测试前冻结；检索也只使用训练记录，测试细胞系的结果不进入轨迹生成、SFT、GRPO 或模型选择。正向响应与通用能力、Schmidt 逆向预测均报告五次独立运行的标准差；作者明确指出误差条不是置信区间，也不构成显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 基因终局奖励与完整基因、通路、格式联合奖励对比 | 作者报告，SFT 首先带来显著提升，基因层面的终局奖励继续提供较小增益；加入与生物学一致的通路监督后，完整 PertMind 成为表现最好的变体。 | 这组消融将最终基因响应监督与中间通路监督分开：基因奖励约束“最后预测是否正确”，通路奖励约束“中间生物过程是否合理”。完整模型最佳支持两种监督互补，但 Figure 3b 不展示运行级误差条，因此无法仅凭图中差距判断增益的统计稳定性或显著性。 | 第 4.1 节，Figure 3b<br><span class="experiment-evidence">By contrast, combining the gene-level outcome reward with biologically aligned pathway supervision produced the best-performing PertMind variant, while shuffling the pathway labels reduced performance below the SFT model.</span> |
| 提示中加入通路上下文、正确通路奖励与打乱通路标签的对照 | 作者报告，仅提供通路文本但不施加通路奖励，并未优于仅基因奖励；打乱通路标签后，性能降至 SFT 以下。 | 提示对照表明性能提升不是因为模型单纯看到了更多通路词汇；打乱标签对照进一步检验监督中的生物结构是否重要，因为它保留通路出现频率和提示格式，只破坏通路与样本的对应关系。下降支持“正确结构化通路监督有用”，但也可能部分来自错误标签引入的训练噪声，不能单独证明模型形成了忠实的通路级推理链。 | 第 4.1 节，Figure 3b<br><span class="experiment-evidence">Adding pathway context to the prompt without a corresponding pathway reward did not improve over gene-only RL.</span> |

**定性案例**

- 在训练模式之外的自由文本案例中，模型被询问 Vemurafenib 处理 C32 细胞对 MKI67 的影响。PertMind 预测 MKI67 下调，并给出“抑制 BRAF V600E，降低 MAPK/ERK 信号和增殖活性，进而降低 MKI67”的机制链；附录文献审计为主要环节找到了公开来源。该案例只能说明模型能够生成连贯且可由文献支持的解释，不能作为定量泛化证据，也不能证明生成的推理过程忠实反映了模型作出预测的内部原因。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Applies reinforcement-learning post-training to elicit biological reasoning from an LLM using cellular perturbation data.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`30e1bcc3dcb5d4a084c3e1008288511b38c6a43de18f73863f8e886119fdaca4`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
