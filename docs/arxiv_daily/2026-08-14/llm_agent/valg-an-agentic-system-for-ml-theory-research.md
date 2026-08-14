---
title: "[论文解读] VALG: An Agentic System for ML Theory Research"
description: "[arXiv 2608.13060][LLM Agent] 本文关注机器学习理论研究中的“前形式化”阶段，提出用智能体系统显式协调问题设定、定理目标与证明结构的共同演化，并持续记录所得定理相对原始开放问题的范围变化。"
arxiv_id: "2608.13060"
announcement_date: "2026-08-14"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:54:31.046519+00:00"
source_sha256: "403ac3014b836edc73045941ee4c1fa9920cf68ef013c480e53717cd4206ca61"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "机器学习理论"
  - "自主智能体"
  - "定理开发"
  - "证明依赖图"
  - "自适应问题表述"
  - "多层验证"
  - "开放问题"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.13060</p>

# VALG: An Agentic System for ML Theory Research

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Dechen Zhang, Xuan Tang, Xinxiang Yin, Xingwu Chen, Jian Qian, Difan Zou</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The University of Hong Kong；Shenzhen Loop Area Institute；Northwestern Polytechnical University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13060v1) · [PDF 下载](https://arxiv.org/pdf/2608.13060v1) · **关键词** 机器学习理论, 自主智能体, 定理开发, 证明依赖图, 自适应问题表述, 多层验证, 开放问题<br>
**代码**: [https://github.com/DechenZhang/VALG-ML-Theory-Agent/tree/main/skills](https://github.com/DechenZhang/VALG-ML-Theory-Agent/tree/main/skills) · **项目页**: [https://github.com/DechenZhang/VALG-ML-Theory-Agent](https://github.com/DechenZhang/VALG-ML-Theory-Agent)

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

本文关注机器学习理论研究中的“前形式化”阶段，提出用智能体系统显式协调问题设定、定理目标与证明结构的共同演化，并持续记录所得定理相对原始开放问题的范围变化。

**不用术语来说**：解决机器学习理论开放问题并不只是为一个固定命题寻找证明：研究者往往会在推导过程中修改假设、算法能力、数据条件或结论强度。修改可能产生有价值的特例或条件性结论，也可能让最终定理悄然偏离原问题。因此，真正困难的是让智能体在长期探索中既能灵活修正研究方向，又能明确说明“现在证明的究竟是什么、它与原问题还有什么关系”。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将非形式化机器学习理论研究表述为一个受来源问题约束的智能体定理开发任务，要求系统联合维护学习设定、附加假设、定理目标、证明依赖和结果相对原问题的范围，而不是只判断一段证明是否看似成立。
- 作者提出分层诊断与修订思路：把失败区分为局部推导、整体证明结构和定理表述三个层级，并规定只有表述层障碍才启动与原问题显式关联的新变体或放宽版本，从流程上防止系统未经说明地替换证明目标。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于机器学习理论与自主智能体交叉领域。机器学习理论不是只证明一个孤立命题，而是先用数据生成方式、算法可获得的信息、训练协议、损失或风险、随机性以及性能随问题参数变化的规律，精确定义需要解释的学习现象；因此，改变假设、协议或评价对象，可能使证明得到的定理偏离原始问题。VALG关注形式化证明之前的非形式化定理研究阶段：智能体需要同时形成问题设定、定理目标和证明机制，并持续记录修订后的结论与源开放问题之间的数学关系。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**机器学习理论问题设定**

它是一组共同界定研究对象的数学条件，通常包括数据模型、假设类、训练或查询协议、损失函数、成功概率及复杂度参数。定理是否解决原问题，取决于这些条件和目标结论是否与源问题保持一致。

</div>
<div class="concept-item" markdown="1">

**定理契约**

本文用固定的数学规格约束一条证明分支，明确该分支采用的假设、学习设置和目标结论。其作用类似接口：在局部证明过程中不能悄然增加假设或更换目标，确需改变时必须建立新的变体或放松分支。

</div>
<div class="concept-item" markdown="1">

**有类型的证明依赖图**

它把原始假设、中间引理和目标定理表示为带有依赖关系及角色类型的图，并要求每个结论由其前置节点支持。直观地说，系统先检查整条证明链能否接合并闭合，再按依赖顺序完成和审查各个局部证明。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个尚未解决的机器学习理论子问题及其源文献所规定的数学范围，包括学习模型、可用信息、协议、假设和目标结论。系统需要在相对于源问题的一条定理分支中确定固定规格，构造从基本假设经中间引理到目标定理的证明依赖图，依次生成并审查局部推导；失败时还要判断障碍来自局部推导、整体证明结构还是定理表述。输出不是无条件宣称“解决问题”，而是带有问题设定、定理陈述、证明状态及源问题关系标签的候选结果，例如与源范围匹配的候选定理、受限方法结果、特殊情形、条件定理、显式放松或受阻分支。本文处理的是自然语言和数学文本驱动的预形式化研究，内部“最终定稿”仅表示通过系统内部流程，不等同于外部同行评审或机器验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **通用科学研究智能体与机器学习研究智能体**: 这类系统通常把文献检索、假设生成、实验、批评和写作组织为长程工作流，也有基准评测扩展的机器学习任务；VALG进一步聚焦机器学习理论中问题表述与证明共同变化的情形，要求显式追踪每次假设和定理范围修订。
- **数学研究智能体与形式化定理证明智能体**: 前者已研究猜想生成、长程证明搜索、批评和修订，后者借助证明助手、检索与修复循环证明或形式化固定命题。VALG处理二者之间的预形式化缺口：目标命题尚未完全固定时，如何区分局部推导失败、证明结构失败和问题表述失败，并避免把修改后的较弱命题误报为原问题的解答。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

机器学习理论中的定理依赖完整的数学设定，包括数据生成方式、训练协议、算法可访问的信息、损失或风险、随机性及渐近范围。研究开放问题时，这些要素常与证明技术一起被反复调整；系统既要允许这种探索，又要审计每项新增假设和目标变化，否则一个形式上合理的结果可能已经不再回答来源论文提出的问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **通用科学研究与数学推理智能体**：这类系统通过语言模型协调文献检索、假设生成、工具调用、长程证明搜索、批评和迭代修订，适合把研究活动组织成多步骤工作流；部分数学研究智能体还会在自然语言中协同生成猜想和修改证明。
- **形式化定理证明智能体**：这类系统通常接收一个已经固定的形式命题，借助证明助手、定理检索和错误修复循环构造可由形式系统检查的证明；其优势是局部推导和最终证明能够接受严格的机器验证。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 通用研究或数学推理智能体可以不断生成、批评和修订内容，但原文指出，机器学习理论还要求同步跟踪问题设定、定理表述和证明机制；若缺少这种来源相对的记录，系统可能在采用自适应协议、近似表示、分布依赖结论或额外目标性质后，仍把较弱或不同的问题当作原问题处理。
- 形式化证明智能体主要面向固定陈述的证明或形式化，因而没有直接解决证明前阶段的关键决策：当现有命题证明受阻时，应修复某一步推导、重构全局证明依赖，还是承认原表述需要增加假设或降低结论。其后果是形式检查即使成功，也不能单独保证被证明的命题仍与来源开放问题范围一致。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有进展留下了一个面向机器学习理论的前形式化空缺：尚缺少一种智能体工作机制，能够在命题和证明都可能变化的情况下，为每条研究分支固定当前数学规格，检查中间引理能否组合为目标定理，定位失败属于哪个层级，并把放宽、特例、条件性结果和原范围结果明确区分。

</div>
<div markdown="1"><span>核心问题</span>

能否把机器学习理论开放问题的探索组织为自主智能体工作流，使系统在共同发展问题表述、定理目标和证明机制时，仍可验证证明依赖、诊断失败原因，并忠实维护每个候选定理与来源问题之间的数学关系？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把开放探索和受约束证明分开管理：一条分支先固定当前要证明的数学“合同”，再把证明表示成从原始假设、经中间引理到目标定理的有类型依赖图。这样，失败便可以沿依赖关系追溯：某个推导错误就局部修补，引理接口不兼容就重构证明图，只有现有设定本身不足时才另开变体。直观上，这相当于给会变化的研究过程加入版本控制和分层审计，使探索保持灵活，同时避免目标在迭代中被无声替换。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

VALG 将机器学习理论研究建模为“问题形成、证明构造、独立审查、故障定位与定向修订”的闭环，而不是从自然语言问题直接生成一篇完整证明。系统输入研究方向、源问题及可选研究简报，先调查相关理论与经验文献，再以“视角—想法”两级结构建立至多 $M\leq 3$ 个并行分支；每个分支随后固定数学对象、假设、量词、研究范围和唯一目标，形成不可由证明阶段随意修改的定理契约。通过这一设计，不同分支对应不同但有文献依据的研究解释，而同一分支内的证明始终针对一个明确命题。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 文献调查与研究视角选择

文献工作器分别整理直接相关的理论结果、基础理论框架和经验现象，并记录已有设定、证明工具、结论及有证据支持的缺口。视角选择器据此提出至多 $M\leq 3$ 个彼此不同的研究视角，每个视角由“分析目标、模型类别、数据假设、学习制度、算法”五个字段规范表示。

<div class="method-step__io" markdown="1">

**输入**：研究方向、源问题，以及可选的研究简报。<br>
**输出**：经过覆盖性与重复性检查的并行视角分支，以及每个分支对应的文献依据、范围约束和待解释缺口。

</div>

**直观理解**：这一步先确定“应当从哪几个角度研究”，避免系统一开始就押注单一证明路线。五字段表示相当于给每条路线划定边界，但暂时不把定理细节定死。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 机制想法生成与定理形式化

独立的想法生成器在视角范围内提出具体机制和候选结果；想法必须逐字段特化上游视角，不能扩大或冲突于其模型、数据、制度或算法范围。形式化器随后固定记号、基本假设、量词、参数制度和恰好一个数学目标，构成该分支的定理契约。

<div class="method-step__io" markdown="1">

**输入**：一个已选研究视角、该视角的文献依据，以及源问题的范围约束。<br>
**输出**：可供证明阶段使用的形式化设定与唯一目标；缺乏文献支持、跨越视角边界或与其他分支重复的想法被拒绝。

</div>

**直观理解**：研究视角只是大方向，这一步把它变成真正可以判断真假的命题。所谓定理契约，就是先写清楚“允许假设什么、必须证明什么”，防止证明困难时偷偷增加条件或降低结论。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 证明图、全局诊断与局部证明

草图工作器把论证表示为有向无环依赖图：源节点是基本假设，内部节点是引理级命题，唯一汇点是目标定理；每个节点还记录精确结论、依赖、允许假设、拟用工具和输出接口。草图通过审查后，全局证明工作器检查跨节点的定量依赖、对象兼容性、概率或收敛模式、闭合论证与边界情形，再由局部工作器按依赖顺序证明 $S_1,\ldots,S_k$。

<div class="method-step__io" markdown="1">

**输入**：固定的定理契约，包括形式化设定、允许的基本假设和目标定理。<br>
**输出**：通过独立审查的证明依赖图、全定理可行性诊断，以及逐项验收的局部证明证据。

</div>

**直观理解**：依赖图说明“整篇证明需要哪些积木以及先后关系”，全局诊断则检查这些积木是否真的能拼成目标，而不只是箭头连接得漂亮。之后每个工作器只负责一块可核查的数学任务，使隐藏引理、条件缺失和结论强度不足更容易暴露。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 证明组装与多角度终审

组装器统一记号并将局部结论连接为自包含的 LaTeX 定理稿件，但不得在组装阶段引入未经证明的新数学内容。结构、严谨性、引用和对抗性四类审查器分别检查依赖闭合、实际推导、外部结果适用性及极端或退化情形，聚合审查器再产生唯一的控制器判定。

<div class="method-step__io" markdown="1">

**输入**：固定定理契约、已接受的依赖图、全局诊断和全部已接受局部证明。<br>
**输出**：满足接收门槛的最终定理候选及审查记录，或者带有明确故障类别和最小修复对象的拒绝结果。

</div>

**直观理解**：组装不是简单拼接文本，而是确认所有已验收部件共同推出原定目标。四类终审像从不同专业角度检查同一份证明，最后只由聚合审查给控制器一个统一结论，避免多个审查意见相互冲突。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文描述的是由多个生产工作器、独立审查器和控制器组成的自主研究工作流，没有提出用于训练参数模型的损失函数，也没有说明对底层语言模型进行微调或梯度优化；系统所优化的是流程层面的产物质量与修订范围，即在固定定理契约下通过阶段门控、独立审查和最小有效返工获得可接受的定理候选。由于这不是一个数值优化目标，不能把最终审查分数或接收条件解释为可微训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 视角—想法分层形式化模块**

视角使用规范化五元组“分析目标、模型类别、数据假设、制度、算法”描述宽范围搜索区域；下游想法必须是该五元组的逐字段特化，只能收紧或具体化，不能扩大范围或与上游冲突。形式化器再把可行想法转换为包含固定对象、原始假设、量词、参数制度和唯一目标的定理契约，并且只有通过检查点的契约才能进入证明流程。

> 直观理解：这一模块把“探索多个方向”和“对一个明确命题负责”分开处理。前半段保持研究搜索的广度，后半段锁定证明边界，从而可以判断最终结果究竟回答了源问题、只回答了特殊情形，还是修改了原问题。

**2. 类型化证明依赖图与全局诊断模块**

证明草图不是自由文本提纲，而是有唯一目标汇点的有向无环图；每个节点都带有精确命题、合法依赖、允许假设、证明工具和下游所需接口。全局诊断位于草图与局部推导之间，逐节点验证输入是否足够、候选机制是否可导出指定结论，并在定理层面检查常数和速率依赖、概率或收敛模式、对象转换、闭合条件及边界行为。

> 直观理解：图结构只能证明“计划没有循环且看似完整”，不能证明每一步真的做得到，也不能保证上一步给出的结论足够强。全局诊断专门寻找这种跨步骤不匹配，例如上游只控制了替代对象，而下游却需要原始目标的保证。

**3. 契约化独立审查与故障路由模块**

证明阶段的生产者与审查者相互分离，草图、全局证明、局部步骤和最终稿分别按照阶段特定标准接受检查。最终稿由结构、严谨性、引用和对抗性审查器并行评估，再由聚合审查器给出控制器可执行的单一判定；控制器依据故障类型将任务路由到组装、局部步骤、全局证明、草图或新想法层级。

> 直观理解：固定定理契约后，审查者可以依据清楚的目标检查生产者，而不必自行决定什么问题值得研究。故障路由的价值在于把“证明错了”细分成可操作原因，使系统既避免无谓的全量重写，也避免用局部补丁掩盖定理设定本身的问题。

**训练与推理**

VALG 不包含论文所述意义上的模型训练阶段，其运行过程相当于多智能体推理与编排。运行时，系统先读取源问题和可选简报，执行文献调查、视角选择、机制想法生成及形式化；交互模式在预证明阶段的各节点暂停，由人类专家批准、编辑或要求重做，自动模式则默认继续，但仍执行来源范围一致性、分支覆盖和产物有效性检查。只有已检查且形式化完成的分支进入证明阶段。

对每个活动分支，系统依次生成证明依赖图、执行草图审查、生成全局证明诊断、执行全局审查、按拓扑依赖顺序生成并独立审查局部步骤、组装完整证明，并进行四类专门终审与聚合审查。若审查失败，控制器读取标准化诊断，选择最小可修复层级并在预算内重试；修订必须使用已接受的上游上下文，且需要新的独立审查。一个分支最终化不会终止其他分支；因此单次运行可以返回零个、一个或多个已接受定理候选，并保留未接受分支的限制、条件或阻塞状态。

**复现信息**

公平理解和复现该系统需要保留四项流程约束。第一，活动视角分支数满足 $M\leq 3$，并通过文献支持检查和跨分支去重门控控制搜索宽度。第二，证明图包含源假设节点、引理级内部节点和唯一目标汇点，局部步骤 $S_1,\ldots,S_k$ 必须按依赖顺序处理；论文图示给出的工作器规模为每次运行共享 $2$ 个工作器、每个分支使用 $12+2k$ 个工作器，其中 $k$ 是局部证明步骤数。第三，生产者不能自我验收，各阶段产物只有在对应独立审查或人工检查点通过后才能被下游使用；最终图示门槛为分数至少 $7$ 且不存在阻塞项。第四，系统同时支持交互和自动运行模式，但两种模式均执行产物验证、重试预算、分支覆盖及最终接收副本核验；所给章节没有明确报告底层语言模型、采样参数、检索后端、具体重试次数配置或硬件环境，因此这些内容不能由节选推断。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 评测对象不是传统训练或测试数据集，而是从五个COLT 2026开放问题中选出的九个理论子问题，覆盖张量分解、学习复杂度、单比特均值估计、差分隐私和在线优化。每个子问题构成一次理论研究运行，用于检验VALG能否形成可审查的定理候选及证明记录；原文未报告随机划分、训练集或测试集。
- 九个子问题的源问题说明及其数学设定充当外部参照。评估时比较候选定理与源说明在数据模型、交互协议、假设、结论和渐近范围上的一致性，而不是在隐藏测试样本上计算预测性能。
- 单比特均值估计案例使用分布类$\mathcal{D}(k,\lambda,\sigma)$作为理论问题域，其中均值位于$[-\lambda,\lambda]$，中心$k$阶矩不超过$\sigma^k$。该案例用于检验系统能否在查询必须预先固定、每个独立样本只返回一比特的约束下，得到覆盖完整分布类的最优阶样本复杂度结论。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**源范围匹配**

检查最终定理候选是否保持源问题规定的数据模型、协议、假设、输出和目标范围。它是逐案例的数学判定，而非连续数值分数。 （达到完整匹配优于受限方法、特殊情形或条件结果，因为前者直接处理原始子问题；但这不等同于外部同行确认定理正确。）

</div>
<div class="metric-item" markdown="1">

**内部最终定理候选数**

统计九次运行中有多少分支通过系统内部的依赖、严谨性、引用和对抗性审查，并形成最终候选。 （在同等问题难度和审查标准下越高越好，因为它表示更多运行完成了内部证明流程；该指标不能替代独立专家复核。）

</div>
<div class="metric-item" markdown="1">

**理论速率阶**

在单比特均值估计案例中，以样本数$n$相对于目标复杂度$r_k(\lambda,\sigma,\epsilon,\delta)$的渐近阶衡量效率，同时要求最坏情况下绝对误差超过$\epsilon$的概率不超过$\delta$。 （样本复杂度上界越低越好；与已知极小极大下界同阶时称为阶最优，但常数$C_k$仍可能影响有限样本表现。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 九个子问题的总体结果

<div class="result-value" markdown="1">

九次运行中有两次形成与源问题说明范围匹配、并处理原始子问题的内部最终定理候选；其余七次只得到受限方法结果、特殊情形或条件定理。

</div>

作者据此主张VALG能够在少数开放问题分支上把定理表述与证明推进到内部完成状态，并能对未完全解决的分支作范围标注。分析上，这个结果更直接支持“研究过程可被结构化记录和分类”，而不足以建立普遍的问题解决成功率：样本只有九个子问题，问题并非随机抽取，也没有外部专家在统一标准下确认两项候选定理的正确性与新颖性。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Two runs produce internally finalized theorem candidates that match the scope of their source briefs and address the original subproblems; the remaining seven yield restricted-method results, special cases, or conditional theorems.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 非交互式单比特均值估计案例

<div class="result-value" markdown="1">

在$\mathcal{D}(k,\lambda,\sigma)$上，候选协议对每个独立样本恰好使用一比特，查询库在第一次响应前固定，并给出$n\leq C_k r_k(\lambda,\sigma,\epsilon,\delta)$及最坏情况下失败概率不超过$\delta$的保证；作者称其覆盖源问题完整范围，并与已知下界同阶。

</div>

该案例表明系统生成的候选方案没有通过自适应查询规避原问题：定位与细化查询均预先承诺，解码器再利用定位结果完成平移、中心化和重要性加权。若证明和所引用下界均正确，它给出了三个矩条件区间下的阶最优样本复杂度。不过，“阶最优”只比较渐近数量级，不说明常数较小、实际实现高效，也不构成机器检验或外部同行验证。

<div class="result-source" markdown="1">

来源：第4节，Theorem 4.5后的Discussion

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This theorem matches the source problem’s full scope over the unrestricted central-$k$-moment class. Together with the known one-bit minimax lower bound, its rate is order-optimal. Both query banks are precommitted, and localization is a decoder-side operation.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 七个未达到源问题完整范围的运行

<div class="result-value" markdown="1">

七次运行没有被合并报告为“解决原问题”，而是保留为受限方法结果、特殊情形或条件定理。

</div>

这一结果主要检验系统的范围治理能力：当证明依赖新增条件、只适用于较窄设定或仅覆盖特定方法时，VALG应避免把它包装成原开放问题的完整答案。作者的结论支持这种分类机制在案例记录中得到执行，但摘录没有逐项给出七个分支各自的最终状态、失败原因和独立正确性审查，因此无法进一步比较不同障碍类型的频率。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Two runs produce internally finalized theorem candidates that match the scope of their source briefs; the remaining seven yield restricted-method results, special cases, or conditional theorems.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测仅含五个COLT 2026开放问题中的九个子问题，且所给材料未说明随机抽样、预注册选择标准或难度校准；两次源范围匹配不能直接外推为一般开放问题上的成功率。
- “internally finalized”表示通过VALG内部审查流程，不等同于形式化证明助手验证、独立专家复核或同行评议确认。所给摘录也未报告重复运行、替代代理基线、组件消融、计算成本及人工介入程度，因此无法隔离多层验证、依赖图和自适应表述机制各自的因果贡献。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 源问题本身是最关键的参照基线：候选结果必须与源说明逐项比较，以判断它解决的是原问题、受限方法版本、特殊情形还是附加假设下的条件版本。
- 单比特均值估计中的已知单比特极小极大下界是理论速率基线。若VALG所得上界与该下界同阶，才能称为阶最优；所给摘录未提供该下界的完整公式或证明。
- Danus是相关系统层面的概念比较对象：它使用共享事实图和无状态验证器积累局部证明，而VALG进一步区分全局证明架构、定理级可行性与局部推导，并在表述受阻时新建与源问题关系明确的分支。原文未报告两者在同一组问题上的定量对照实验。
- 形式化定理证明代理构成另一类概念基线，其通常从已经固定并编码的命题开始；VALG评测的重点则是形式化之前、定理目标与假设仍可能修订的研究过程。原文未报告与具体形式化证明器的成功率或资源消耗对比。

**实验想回答的问题**

- VALG能否在机器学习理论开放问题中自主完成从问题形式化、证明结构设计、局部推导到多层审查的完整流程，并产出与源问题范围一致的定理候选？
- 当原始目标无法证明时，VALG能否识别障碍属于局部推导、证明结构还是定理表述，并将原范围结果、受限方法结果、特殊情形、条件定理与失败分支明确区分？

**实验实现**

评测采用九个理论子问题的案例研究协议。每个源相对分支固定一份数学规格，将证明表示为从原始假设、经中间引理到目标定理的有类型依赖图；系统先做机制感知的全局可行性与接口检查，再按依赖顺序构造和审查局部证明，最后分别执行结构、严谨性、引用和对抗性审查，并由聚合审查器给出控制器可见的最终判定。失败会被路由至证明步骤、证明草图、全局结构或问题表述层；若必须修改假设或目标，系统建立新分支并记录其与源问题的关系。论文报告问题设定、候选定理及相对源问题的进展，但所给材料未报告统一的运行预算、模型版本、重复运行次数、人工介入程度、墙钟时间或外部盲审协议。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 单比特均值估计案例把样本预先分成定位块和细化块：定位器以预先固定的Borel查询粗略确定均值区域，细化阶段同样预先抽取查询层级、参数和阈值，每个样本仅返回一个指示比特；解码时构造经重要性加权的$Z_i(c)$，再以分块均值的中位数输出$\widehat{\mu}$。其关键意义在于区分“查询自适应”与“解码器使用先前结果”：协议的查询库始终预先承诺，只有解码计算利用定位中心$c$，因而候选定理仍符合非交互式源问题。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：VALG is an autonomous research agent whose core workflow coordinates theorem formulation, proof-graph construction, verification, and iterative mathematical reasoning.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`403ac3014b836edc73045941ee4c1fa9920cf68ef013c480e53717cd4206ca61`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
