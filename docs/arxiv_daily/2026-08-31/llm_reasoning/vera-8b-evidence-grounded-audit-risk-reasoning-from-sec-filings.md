---
title: "[论文解读] VERA-8B: Evidence-Grounded Audit Risk Reasoning from SEC Filings"
description: "[arXiv 2608.28402][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.28402"
announcement_date: "2026-08-31"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:45:17.427076+00:00"
source_sha256: "0faf44a1afdd4fef9cb135f7226374dd038a831c927d9ff41d3f84bacae60a3c"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "审计推理"
  - "SEC申报文件"
  - "金融语言模型"
  - "证据 grounding"
  - "可执行规则书"
  - "GRPO"
  - "选择性弃权"
  - "不确定性限定"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.28402</p>

# VERA-8B: Evidence-Grounded Audit Risk Reasoning from SEC Filings

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Menghan Liu, Elynn Chen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: New York University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28402v1) · [PDF 下载](https://arxiv.org/pdf/2608.28402v1) · **关键词** 审计推理, SEC申报文件, 金融语言模型, 证据 grounding, 可执行规则书, GRPO, 选择性弃权, 不确定性限定<br>


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

本文位于审计风险预测、金融语言模型和证据约束推理的交叉领域。传统错报风险模型通常利用财务比率、公司治理、市场信息、审计特征或$10$-$K$文本，在公司层面预测某一发行人是否存在错报风险；金融语言模型则进一步处理财务文本、表格和数值推理。然而，审计判断不能只依赖一个准确但缺乏依据的预测：模型必须说明具体风险、引用申报文件中的准确原文，并证明该引文在时间、语境和审计机制上确实支持结论。本文将任务设定为一种事前、文件级的审计推理：模型只使用执法行动发生前可获得的$SEC$申报文件，识别一个或多个可能的审计风险，给出与风险对应的原文证据和解释；当证据不足或不确定时，模型应选择弃权或进行不确定性限定，而不是强行生成结论。其核心背景问题是，执法结果可以帮助确定“哪个发行人—期间”值得调查，却不能直接充当申报文件中可见证据的标签；同时，没有执法行动也不能证明不存在审计风险。因此，可靠系统需要同时处理时间对齐、风险多标签、证据溯源、结构化输出和选择性预测。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**证据 grounding 与证据验证**

证据 grounding 指模型的结论必须连接到输入文件中的具体支持材料，而不是仅凭看似相关的词语生成解释。证据验证进一步检查引文是否真实存在、是否属于正确语境、是否具有正确时间关系，并且是否足以支持所声称的审计机制。

</div>
<div class="concept-item" markdown="1">

**事前审计风险预测**

该任务要求模型在执法行动或其他后续结果发生之前，仅根据当时已经公开的申报文件预测潜在审计风险。后来的执法结果可作为监督信号或样本筛选依据，但不能被当作当时申报文件中已经出现的直接证据。

</div>
<div class="concept-item" markdown="1">

**选择性弃权**

选择性弃权允许模型在证据不充分、冲突或置信度不足时不作确定判断，而把案例交给人工复核。对审计而言，这比输出一个流畅但无依据的风险结论更安全，因为系统的目标不仅是提高覆盖率，也要控制无法验证的主张。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是按发行人和期间组织的$SEC$申报文件及其中的审计相关披露，研究重点是执法行动发生前可获得的文本信息。输出不是单一的风险概率，而是完整的审计发现，包括二元风险判断、一个或多个审计风险类别、与每个判断对应的精确文件引文、基于引文的理由，以及在证据不足时的弃权或不确定性说明。任务允许同一观察同时具有多个非互斥风险类别，因此属于证据约束的多标签推理。基本假设是：模型不得把关键词出现本身视为证据；引文必须真实存在，并且其时间、上下文和审计机制能够支持结论。最终结果还应以结构化、可验证且便于审阅的形式交付，而不是只返回自由文本。文中给出的系统目标是把原始申报文件转换为已验证记录，再转换为审计人员可以直接检查的报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D$**

一个发行人—期间对应的申报文件或文件集合，是模型进行事前审计推理的主要输入。

</div>
<div class="notation-item" markdown="1">

**$r$**

审计风险判断，可表示存在或不存在整体风险，也可进一步表示某一风险类别。

</div>
<div class="notation-item" markdown="1">

**$e$**

从申报文件中抽取的精确证据引文；它必须实际出现在输入文本中，并能支持对应的风险判断。

</div>
<div class="notation-item" markdown="1">

**$a$**

模型生成的结构化审计发现，通常包含风险判断、风险类别、证据、理由以及弃权或不确定性状态。

</div>

</div>

**直接相关的工作**

- **错报风险检测模型（包括Dechow F-score及后续机器学习和文本方法）**: 这些方法从财务比率、公司治理、市场、审计特征或$10$-$K$语言中预测公司层面的错报风险，并强调类别稀少、按时间划分数据和延迟发现等现实评估问题。它们能够进行风险预测，但通常不能把预测连接到具体申报文件证据，也不能解释某一引文如何支持特定审计机制；本文在此基础上转向文件级、证据可核验的事前推理。
- **AuditAgent**: AuditAgent使用执法文件和财务报告寻找欺诈证据，代表了专家引导的跨文件证据发现方向。本文的设定不同：VERA-8B只从执法行动发生前的申报文件预测未来审计风险，并试图用统一证据标准同时约束风险决策、证据来源、推理理由和弃权行为。

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

VERA-8B将单条SEC申报文件建模为证据约束的审计风险推理任务：输入为执行行动发生之前的公司—申报文件—财务期间观测$x_i$，输出风险类别、文件中的支持证据、证据到风险的机制解释以及是否弃答。方法分为两个阶段：第一阶段把后续执法结果与申报文件对齐，并将SEC文件、PCAOB准则和历史AAER知识编译为可执行的证据规则，生成只有在当期文件证据充分时才允许出现的监督目标；第二阶段先用结构化QLoRA监督微调学习统一输出契约，再用带审计约束的GRPO修正残余错误，最后通过校准、保序预测集和证据验证器决定自动阳性、自动阴性或人工复核。直观地说，后续执法事件只用于提示哪些文件值得调查，不能直接充当模型作出风险判断的证据；模型只有在文件中找到经过验证的原文依据时才能自动提出风险，否则必须弃答或转人工审核。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造结果对齐的数据集

将每个申报观测表示为$x_i$，仅当发行人身份匹配、受影响财务期间匹配且申报日期早于执法日期时，才令结果指示变量$Y_i=1$；不确定的身份或期间匹配保留给人工复核或敏感性分析。控制样本来自相同的SEC文件总体，并排除已链接期间、已知涉执法发行人、污染窗口内文件以及跨数据划分的重复或近重复文本。

<div class="method-step__io" markdown="1">

**输入**：SEC EDGAR中的公司申报文件及其公司身份、财务期间和申报日期信息；SEC Accounting and Auditing Enforcement Releases中的事后执法事件。<br>
**输出**：结果对齐数据集$\mathcal{D}_{\mathrm{out}}=\{(x_i,Y_i)\}_{i=1}^{N}$，其中$Y_i$表示文件是否与后续执法结果满足严格时序和实体条件，但不表示文件中一定存在可采纳的审计证据。

</div>

**直观理解**：这一步像把“后来发生了问题”的案件与更早的申报文件配对，用于发现值得学习的风险线索。作者刻意把案件标签和文件证据分开，避免模型把事后执法公告直接当成当时审计人员能够看到的证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 编译审计证据规则并生成监督目标

通过编译器生成版本化JSON规则书；每条规则规定知识来源、生效日期、适用文件章节、风险类别、检索触发条件、验证条件、排除条件和最低证据强度。对候选文件片段$e$和风险类别$k$执行证据门控：必须有精确引文、章节和上下文一致性、机制层面的支持，并排除仅历史性陈述及已完成整改；通过门控的证据才可进入目标，失败者成为困难负例，冲突则转人工审核。

<div class="method-step__io" markdown="1">

**输入**：SEC文件中的审计相关章节$K_{\mathrm{filing}}$、PCAOB审计准则知识$K_{\mathrm{PCAOB}}$、历史执法行动中的风险机制$K_{\mathrm{AAER}}$，以及可选的外部专家规则接口$I_{\mathrm{external}}$。<br>
**输出**：结构化目标$o_i=(\mathbf{y}_i,E_i,r_i,a_i)$：$\mathbf{y}_i$为九类非互斥审计风险的多热向量，$E_i$为支持证据，$r_i$为证据到风险的机制解释，$a_i$为弃答指示。如果没有任何可采纳的类别—证据配对，则设置$a_i=1$并保持风险标记为空。

</div>

**直观理解**：规则书相当于一份可执行的审计检查表，不只是告诉模型“这个文件后来出过问题”，而是规定“文件中的哪句话、位于什么章节、通过什么审计机制，才足以支持某个风险”。因此，模型可以少报，但不能用没有出处的合理猜测冒充审计结论。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 证据闭合的结构化监督微调

使用结构化QLoRA进行答案部分的因果语言模型监督微调，联合学习风险类别选择、证据归因、机制解释和弃答。损失只在答案token上计算，并按答案长度归一化，使包含多个风险标记的较长输出不会仅因token更多而主导训练；所有正类必须满足至少一个当期文件片段通过对应证据门控。

<div class="method-step__io" markdown="1">

**输入**：原始文件观测$x_i$以及序列化后的金标准契约$u_i^{\star}=\operatorname{Serialize}(o_i^{\star})$；契约中的每个风险标记包含风险类别、证据标识符、精确支持短语和机制解释，并附带置信度与弃答状态。<br>
**输出**：得到VERA-SFT模型，它输出统一的结构化JSON契约，而不是只有类别或自由文本解释的预测结果。

</div>

**直观理解**：这一步先教会模型遵守审计报告格式和证据规则。类似先让实习生按统一模板写报告：每个结论都要附原文依据和解释；如果依据不足，正确答案是暂不下结论。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 共享验证器约束的GRPO残差优化

共享可执行验证器检查JSON语法、风险分类体系、证据标识符是否存在、支持短语是否经过规范化后逐字包含于输入，以及弃答与风险标记集合是否一致。GRPO根据六类奖励优化结构、二元正例/弃答决策、多标签恢复、精确证据依据、经验证的类别—证据配对和审计代价不对称性；通过组内奖励方差自适应调节各奖励权重，并用指数平滑、上下界裁剪和相对于冻结VERA-SFT策略的KL惩罚限制策略漂移。

<div class="method-step__io" markdown="1">

**输入**：VERA-SFT产生的候选序列、输入文件中的证据片段、解析后的结构化输出，以及每组候选之间的奖励差异。<br>
**输出**：得到经过证据约束的最终推理策略；只有验证通过的类别—证据配对能获得正向奖励，检查点还必须通过验证集门槛，不能以增加无支持阳性为代价换取召回率。

</div>

**直观理解**：监督微调之后，模型可能仍漏掉次要风险，或偶尔提出没有依据的阳性。GRPO像让多个候选报告相互竞争，但评分不仅看答对没有，还看引文是否真实存在、推理是否通过审计检查；因此优化重点会自动转向当前最薄弱的错误类型，而不是盲目改变已经学会的行为。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 审计风险任务的结构化输出

$$
f_{\theta}(x_i)=o_i=(\mathbf{y}_i,E_i,r_i,a_i)
$$

**符号说明**

- $x_i$：第$i$个执行行动发生前的公司—SEC申报文件—财务期间观测；其中$i$为样本索引。
- $f_{\theta}$：参数为$\theta$的模型映射，从申报文件观测生成审计输出。
- $o_i$：第$i$个样本的完整结构化输出。
- $\mathbf{y}_i\in\{0,1\}^{9}$：九类非互斥审计风险的多热向量；每一维表示相应类别是否被识别。
- $E_i$：支持所识别风险的申报文件证据，包括证据标识和精确原文片段。
- $r_i$：解释文件证据如何通过审计机制支持相应风险的理由。
- $a_i\in\{0,1\}$：弃答指示；$a_i=1$表示可采纳证据不足而应弃答。

<div class="equation-explanation" markdown="1">

**直观理解**：模型不是只输出一个风险类别，而是同时输出“有哪些风险、哪句话支持、为什么支持、是否应该弃答”。这种联合输出把审计判断的结论、依据和不确定性放在同一个可检查对象中。<br>
**原文位置**：第3.1节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### GRPO的审计约束奖励与策略目标

$$
\mathcal{L}_{\mathrm{GRPO}}=-\mathbb{E}\!\left[\rho_{ijt}\widehat{A}_{ij}-\beta D_{ijt}^{\mathrm{KL}}\right],\qquad R_{ij}=\lambda_sR_{ij}^{\mathrm{schema}}+\lambda_bR_{ij}^{\mathrm{binary}}+\lambda_cR_{ij}^{\mathrm{category}}+\lambda_eR_{ij}^{\mathrm{evidence}}+\lambda_vR_{ij}^{\mathrm{verified}}+\lambda_aR_{ij}^{\mathrm{asymmetry}}
$$

**符号说明**

- $\mathcal{L}_{\mathrm{GRPO}}$：GRPO阶段优化的策略损失。
- $i,j,t$：分别表示输入提示、同组候选完成结果和候选序列中的token位置。
- $\rho_{ijt}$：当前策略相对于参考策略在位置$t$上的概率比率。
- $\widehat{A}_{ij}$：候选$j$相对于同组其他候选的估计优势，表示其奖励相对高低。
- $\beta$：KL惩罚系数，用于限制新策略偏离冻结的VERA-SFT策略。
- $D_{ijt}^{\mathrm{KL}}$：当前策略与参考策略在相应位置上的KL散度。
- $R_{ij}$：提示$i$的候选$j$的总奖励。
- $\lambda_s,\lambda_b,\lambda_c,\lambda_e,\lambda_v,\lambda_a$：六项奖励的权重，依次对应结构有效性、二元正例/弃答、类别恢复、证据依据、验证通过和审计代价不对称性。
- $R_{ij}^{\mathrm{schema}},R_{ij}^{\mathrm{binary}},R_{ij}^{\mathrm{category}},R_{ij}^{\mathrm{evidence}},R_{ij}^{\mathrm{verified}},R_{ij}^{\mathrm{asymmetry}}$：六项审计专用奖励，分别评价输出结构、正例/弃答决策、多标签恢复、精确证据、类别—证据验证以及无支持阳性和漏报支持风险的不同代价。

<div class="equation-explanation" markdown="1">

**直观理解**：总奖励同时评价“答得对不对”和“有没有可核验依据”，策略目标则要求模型提高相对优质候选的概率，同时不要远离已经学会证据契约的VERA-SFT。这样GRPO的改进被限制在审计规则允许的范围内，而不是为了提高召回率随意增加阳性判断。<br>
**原文位置**：第4.2节“Mechanism 2: Audit-Constrained Adaptive GRPO Refinement”，公式(12)和(14)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练分为监督契约学习和证据约束的策略优化。第一阶段将目标契约序列化为$u_i^{\star}$，采用仅对答案token计算的归一化因果语言模型损失$\mathcal{L}_{\mathrm{SFT}}(\theta)$，使模型学习风险选择、证据引用、机制解释和弃答；答案token集合记为$A_i$，其长度归一化避免多风险样本因输出较长而过度影响训练。第二阶段以VERA-SFT为参考策略，使用GRPO在同一提示的候选组内比较奖励差异，奖励覆盖结构、二元决策、多标签恢复、证据精确性、验证通过和审计代价不对称性；自适应权重将训练压力转向仍能区分候选的未解决目标，KL惩罚与验证集门槛共同防止策略漂移和无支持阳性增加。重要约束是：没有通过类别特定证据门的当期文件片段，就不能形成正类SFT目标，也不能成为自动阳性结果。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 可执行审计证据规则书与证据门**

规则编译器将$K_{\mathrm{filing}}$、$K_{\mathrm{PCAOB}}$、$K_{\mathrm{AAER}}$和$I_{\mathrm{external}}$整合为版本化JSON规则。对候选片段$e$和类别$k$，证据分数由精确引文条件$q(e)$、章节与上下文一致性$s_k(e)$、机制支持$v_k(e)$以及排除函数$z(e)$共同决定；只有$G_k(e)=1$的证据才能进入正类目标或自动阳性输出。

> 直观理解：它把审计知识变成机器可以逐项执行的准入标准，防止模型用语义上“听起来相关”的句子支持风险。尤其重要的是，事后执法标签只能帮助构造训练对象，不能绕过文件证据门。

**2. 共享可执行验证器**

验证器将生成序列解析为$\hat{o}_i$，并要求解析、语法、类别体系、证据标识符、原文短语包含关系和弃答—标记集合一致性全部通过。该验证器在监督学习后的生成检查、GRPO奖励计算、模型细化和最终路由中保持相同，从而避免训练阶段与部署阶段使用不同的证据标准。

> 直观理解：验证器像自动审稿员：它不仅检查JSON能否读取，还逐字确认引文确实来自输入文件，并检查“说自己弃答”是否真的没有风险标记。这样模型不能靠漂亮的解释掩盖缺失证据。

**3. 自适应GRPO与选择性不确定性路由**

GRPO以VERA-SFT为锚点，使用六项审计奖励和组内相对优势更新策略；各奖励权重依据当前组内方差自适应调整，并经平滑和裁剪。推理阶段以正例—弃答对数似然比进行校准，再将分割保序预测集与验证器、逐类别证据门共同用于三路路由；自动阳性和自动阴性分别需要证据充分的正集合与格式有效且空标记的负集合。

> 直观理解：该模块解决两个不同问题：GRPO负责修正模型还会犯的细节错误，路由负责决定哪些结果可以直接进入审计流程。前者提高受约束的推理质量，后者把无法可靠判断的案例保留给人工，而不是强行输出一个看似确定的答案。

**训练与推理**

训练时，先从SEC文件与后续AAER建立严格的发行人、财务期间和时序链接，同时从PCAOB准则、文件知识和历史执法机制编译规则书；再对每个候选片段实施证据门，生成结构化目标并进行QLoRA监督微调。随后，VERA-SFT为每个输入生成候选输出，解析器和共享验证器计算结构与证据约束，GRPO依据组内相对奖励进行残差优化；奖励权重根据组内方差调整，并通过KL惩罚和验证集条件筛选检查点。推理时，模型先对输入文件生成结构化输出，验证器检查JSON、类别、证据标识符、原文短语和弃答一致性；模型再用正例—弃答的对数似然比进行校准，并在独立校准集上构造分割保序预测集。若预测集为单一正类且输出和每个类别的证据均合格，则路由为$\mathrm{Auto+}$；若预测集为单一负类、验证通过且没有风险标记，则路由为$\mathrm{Auto-}$；其他情况包括歧义、格式错误、证据不足或验证失败，均路由为$\mathrm{Review}$。路由规则在测试前固定，形式化认证还需满足有限样本错误接纳界；若不满足，只报告路由诊断而不宣称正式认证。

**复现信息**

复现或公平解释结果时，必须保持三类数据源的角色分离：SEC文件提供可见的事前证据，AAER提供事后结果对齐信息，PCAOB及相关公共审计知识提供规则依据。数据划分应按发行人进行，排除事后执法叙述、污染窗口中的文件，以及跨划分的精确和近重复段落；不确定的实体或期间匹配不能直接视为确认链接。输出契约应支持多标签风险、每类风险对应的精确证据和机制解释，并规定弃答时风险标记为空；验证阶段必须使用输入中实际存在的证据标识符和原文短语。校准必须使用与训练和测试不相交的校准划分，且部署自动化必须同时满足统计决策条件与证据验证条件。原文未明确报告训练集规模、QLoRA秩、学习率、候选组大小、奖励权重初值、校准方法的具体参数、分割保序置信水平、验证集门槛数值或正式认证界限。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 实验使用1,960份经过验证的SEC申报文件。数据按发行人划分为训练集1,352份、验证集298份和冻结测试集310份，任何发行人均不跨集合；验证集再按发行人拆成199份模型选择数据和99份不确定性校准数据。输入仅保留执法前可获得的申报文本，并排除跨集合完全或近似重复段落、特定执法事件的AAER叙述、整改披露及其他执法后信息。该设计测试的是前瞻性审计风险识别，而非利用事后线索回推风险。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**二元F1**

综合风险阳性识别的精确率与召回率，衡量模型能否判断申报文件是否存在目标审计风险；无效或不完整输出按失败计入，因此它也受输出可解析性的影响。 （越高越好，因为更高值表示风险判断对阳性遗漏与误报取得了更好的综合平衡。）

</div>
<div class="metric-item" markdown="1">

**证据验证微平均F1（EV-Micro-F1）**

对多标签风险类别计算微平均F1，但某个预测类别只有在其随附证据通过统一的证据可采性门槛时才获得分数。它比普通类别F1更接近完整审计合同：不仅要求类别正确，还要求该类别能由申报文本中的合格证据支撑。 （越高越好，因为更高值意味着更多类别判断同时满足预测正确和证据合格，而不是只生成听起来合理的结论。）

</div>
<div class="metric-item" markdown="1">

**未验证声明率（UCR）**

实质性风险类别声明中缺乏可采证据的比例，用于直接衡量模型产生无依据审计断言的频率；格式错误的预测不会被静默删除或事后修补。 （越低越好，理想值为零，因为审计场景不能把缺乏合格证据的风险声明当作可靠结论。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 冻结测试集上的端到端审计合同表现

<div class="result-value" markdown="1">

VERA-8B在310份冻结测试文件上取得95.3%的二元F1和87.1%的EV-Micro-F1，并为全部310份样本生成有效JSON。

</div>

作者据此主张，模型的优势不限于风险二分类，还覆盖带证据的多标签判断和结构化输出。分析上，较高EV-Micro-F1说明许多类别结论确实通过了既定证据门槛；但它仍是单一内部协议下的测试结果，不能单独证明模型可跨年份、跨监管制度或跨文件类型泛化。

<div class="result-source" markdown="1">

来源：第5.2节；图4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the frozen test set, VERA-8B achieves 95.3% binary F1 and 87.1% EV-Micro-F1, with valid JSON for all 310 observations.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 与通用模型及金融专用模型的比较

<div class="result-value" markdown="1">

相对最强金融专用基线，VERA-8B把类别micro-F1从0.648提高到0.878；相对DeepSeek-V4-Pro，二元F1提高45%，验证阳性召回率提高83%，UCR从16.0%降至3.1%。

</div>

作者将该结果解释为：金融知识或通用推理能力本身不足以满足审计证据纪律，审计判断还需要每个风险类别都绑定可采证据。分析上，这组比较支持专门训练与统一证据验证的价值，但节选没有给出各基线的完整绝对分数、模型规模和推理预算，因此不能仅凭相对增幅确定优势来自训练目标、模型容量还是计算配置。

<div class="result-source" markdown="1">

来源：第5.2节；图4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with DeepSeek-V4-Pro, VERA-8B improves binary F1 by 45% and verified-positive recall by 83%, while reducing the unverified claim rate from 16.0% to 3.1%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 不确定性路由形成的人机协作策略

<div class="result-value" markdown="1">

系统自动处理258/310份文件，即83.2%的测试集，并将52份、即16.8%的案例转交人工复核；182个自动阴性案例的阴性预测值为100.0%，自动阳性声明的UCR为0.0%，选择性风险为1.94%。

</div>

这表明路由层没有强迫模型自动处理所有案例，而是把低置信度或证据不完整的案例留给审计人员。100.0%的自动阴性预测值和0.0%的自动阳性UCR只适用于该冻结样本及既定阈值；尤其是校准认证界限未通过、系统没有签发部署证书，因此这些结果不能被解释为真实部署中的统计保证。

<div class="result-source" markdown="1">

来源：第5.4节；表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

VERA-8B automatically handles 83.2% of the frozen test set, while all 182 automatic negatives achieve 100% negative predictive value and automatically routed positive claims have zero UCR.

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

- 通用指令微调模型：用于检验一般语言理解与推理能力是否足以满足审计任务的严格证据要求；节选明确点名DeepSeek-V4-Pro，但未列出该组其他模型。
- 金融专用推理模型：用于区分“掌握金融知识”与“能按审计证据标准给出可核验结论”这两种能力；节选未给出最强金融基线的具体模型名称。
- 基础Llama-3.1-8B：与VERA模型共享骨干，用于衡量审计专用后训练相对于原始基础模型的整体增益。
- VERA-SFT：只经过结构化监督微调的同骨干模型，用于隔离后续适应性GRPO带来的边际作用。

**实验想回答的问题**

- 在严格、不可事后修复且发行人互斥的冻结测试协议下，VERA-8B能否同时做好审计风险识别、多标签风险分类和证据落地，并优于通用指令模型与金融专用推理模型？
- 结构化监督微调、适应性GRPO和不确定性路由分别带来什么作用：前两者是否提高有合格证据支撑的风险识别，后者是否能在保持证据约束的同时把不确定案例可靠地转交人工复核？

**实验实现**

所有模型接收相同的申报文本和输出模式，并由同一个解析器及确定性证据验证器评分；生成结果不进行事后修复，无效和不完整输出直接计为失败。测试集只在模型和不确定性程序锁定后开启并评估一次。VERA-SFT与VERA-8B的比较采用10,000次观测级配对bootstrap重采样及双侧精确McNemar检验。除核心指标外，原文还报告类别micro-F1、支持类别macro-F1、精确集合匹配、验证阳性召回率、JSON有效率、证据定位和证据词元F1等诊断指标。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 基础Llama-3.1-8B与结构化监督微调后的VERA-SFT比较 | 结构化SFT把二元F1从13.0%提高到94.7%，把EV-Micro-F1从34.3%提高到86.4%，并将UCR从65.2%降至3.2%；冻结测试集全部输出均为有效JSON。 | 该对照共享同一Llama-3.1-8B骨干，因而主要隔离审计专用结构化监督的作用。结果表明SFT不仅改善风险预测，还显著改善证据绑定和格式遵从。不过它把结构化标签、证据监督与输出模式联合加入，不能进一步区分三者各自贡献。 | 第5.3节；图4<br><span class="experiment-evidence">Starting from the same Llama-3.1-8B backbone, structured SFT raises binary F1 from 13.0% to 94.7% and EV-Micro-F1 from 34.3% to 86.4%.</span> |
| VERA-SFT与加入适应性GRPO后的VERA-8B比较 | 适应性GRPO将验证阳性召回率从91.5%提高到93.6%，假阴性由5例降至3例；JSON有效率保持100%，UCR没有上升。配对95% bootstrap区间包含零，精确McNemar检验得到$p=1.0$。 | 该消融隔离GRPO在SFT之后的边际效果：它主要多找回少量有证据支持的风险，同时未放松格式和证据标准。由于置信区间包含零且McNemar检验不显著，原文更合理的解释是GRPO针对少数具体错误进行细化，而不是已经证明其带来稳定、广泛的总体性能提升。 | 第5.3节<br><span class="experiment-evidence">Verified-positive recall rises from 91.5% to 93.6%, while false negatives fall from five to three.</span> |

**定性案例**

- 图5展示一个冻结测试集阳性案例：AuditBridge把同一份已验证决策同时保存为机器可读JSON和审计人员可读报告，报告汇集申报元数据、风险发现、精确支持证据、经验证的推理、路由决定与不确定性。该案例说明输出如何保持从结论到申报原文的可追溯性，但节选未提供案例正文或审计人员使用研究，因此只能证明展示形式可实现，不能证明其实际节省复核时间或提高审计质量。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该论文训练具备证据 grounding、拒答和不确定性表达能力的审计推理LLM，并以SFT与GRPO后训练为关键方法。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`0faf44a1afdd4fef9cb135f7226374dd038a831c927d9ff41d3f84bacae60a3c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
