---
title: "[论文解读] DRIP-R: A Benchmark for Decision-Making and Reasoning Under Real-World Policy Ambiguity in the Retail Domain"
description: "[arXiv 2605.07699][LLM 评测] DRIP-R针对零售退货政策存在多种合理解释的现实情形，评估大语言模型智能体如何在动态对话中解释政策、权衡利益并作出决策。"
arxiv_id: "2605.07699"
announcement_date: "2026-08-03"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-03T02:16:27.634220+00:00"
source_sha256: "9f6013c61735d30779ba47050d84e2f67d2042e623a1df60d5a501ed3cfce973"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "大语言模型智能体"
  - "政策歧义"
  - "零售退货"
  - "智能体评测"
  - "对话决策"
  - "工具调用"
  - "多维度评价"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2605.07699</p>

# DRIP-R: A Benchmark for Decision-Making and Reasoning Under Real-World Policy Ambiguity in the Retail Domain

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-03</span>
<span><strong>作者</strong> Hsuvas Borkakoty, Sebastian Pohl, Cheng Wang, Bei Chen, Yufang Hou</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Interdisciplinary Transformation University, Austria；Amazon, Berlin, Germany</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2605.07699) · [PDF 下载](https://arxiv.org/pdf/2605.07699) · **关键词** 大语言模型智能体, 政策歧义, 零售退货, 智能体评测, 对话决策, 工具调用, 多维度评价<br>


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

DRIP-R针对零售退货政策存在多种合理解释的现实情形，评估大语言模型智能体如何在动态对话中解释政策、权衡利益并作出决策。

**不用术语来说**：现实中的退货条款常使用“未使用”等边界不清的表述，同一案例因此可能得到多种都说得通的处理结果；但现有测试通常先把规则写得明确，再检查智能体是否完成任务，难以发现模型面对模糊规则时会不会武断解释、钻规则漏洞，或在表面合规的同时作出违背制度意图的决定。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建DRIP-R基准：从真实的亚马逊退货政策中系统识别歧义，据此设计不存在唯一正确处理结果的零售退货场景，并通过具有顾客角色设定、工具调用能力和双向交互的对话模拟考察智能体决策。
- 提出多维评估框架，从政策遵循、行为与角色设定的一致性、对话质量以及最终解决方案质量等方面分析模型，并比较不同模型、歧义类型和角色设定下的决策差异。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型智能体评测研究，关注智能体在零售客服中依据领域政策进行对话、工具调用与决策。领域政策规定哪些操作可执行，并为判断处理结果是否适当提供规范依据；但真实政策常含隐含假设、模糊措辞或缺失条件，同一条款因而可能支持多种合理解释。既有智能体基准多使用为评测专门编写的简短、单文档且边界清晰的政策，主要测试规划、指令遵循和工具调用，难以反映真实部署中“没有唯一正确答案”的政策解释问题。DRIP-R据此以真实、多文档的亚马逊退货政策为基础，将政策歧义转化为动态客服对话场景，研究不同模型如何解释规则、平衡顾客满意度与组织利益等竞争价值，并形成最终退货决定。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**政策歧义（policy ambiguity）**

政策中的条款或短语因模糊或规定不足而存在多个有效解释；不同解释在具体案例中可能导向不同处理结果。例如，“商品必须处于未使用状态”没有明确说明不同商品怎样才算“未使用”。

</div>
<div class="concept-item" markdown="1">

**价值多元主义（value pluralism）**

顾客满意度、企业利润与法规遵从等正当价值可能彼此冲突，而且不存在一种在所有情形下都唯一正确的排序。因此，政策有歧义时，智能体的任务不只是匹配规则，还涉及对竞争利益作出取舍。

</div>
<div class="concept-item" markdown="1">

**工具调用（tool calling）**

对话智能体在生成自然语言之外，还可调用订单查询、退货处理等外部功能来执行操作。它使智能体的政策解释产生真实行动后果，因此评测不能只看回答是否流畅。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务场景是一段全双工零售退货对话：系统向客服智能体提供真实退货政策、包含特定政策歧义的订单退货案例及顾客交互信息，并允许智能体在对话过程中调用工具；顾客端和客服端还可具有不同人物设定。智能体需要询问必要信息、解释适用条款、决定是否接受退货或采取其他处理方式，并给出相应理由与操作。核心假设是政策本身允许多个可辩护的解释，因此基准不预设每个案例只有一个标准答案，而是从政策遵从、行为与人物设定的一致性、对话能力以及解决方案质量等维度评价过程和结果。换言之，DRIP-R要测的不是智能体能否从清晰规则中找出固定答案，而是它在规则边界不清时如何行使裁量权，以及这种裁量是否稳定、合理且符合预期。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\tau$**

既有的对话式智能体基准系列，使用领域政策约束带工具调用的任务执行。

</div>
<div class="notation-item" markdown="1">

**$\tau^{2}$**

既有智能体基准，文中指出其采用简化政策，并常以二元可接受性等有限范围进行评价。

</div>

</div>

**直接相关的工作**

- **τ-bench**: 与DRIP-R同样评测受领域政策约束、具有工具调用能力的对话智能体，但其政策不是直接采用真实世界政策，而是单文档、专为评测构造的简化规范。表1报告其政策FK阅读年级为9.55，因而不能充分覆盖真实政策的结构深度与解释歧义。
- **τ²-bench**: 该基准进一步评测智能体在领域任务中的执行表现，但仍使用简化的单文档政策，评价范围还可能局限于二元可接受性。本文以其出现“利用政策漏洞得到技术上有效但非预期结果”的案例说明：规则表面遵从并不足以揭示智能体如何解释歧义；表1报告其政策FK阅读年级为9.50，而DRIP-R所用真实多文档政策为11.89。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

零售、医疗和金融等领域正使用大语言模型智能体处理日常但后果重大的任务，其可采取的行动受到领域政策约束。然而，真实政策往往包含隐含假设、含混措辞或缺失条件；当顾客满意度、企业利益与监管合规等价值发生冲突时，机构通常依靠一线人员裁量、升级流程、审计和先例控制风险，而智能体未必具备这些保障。因此，模型可能过度坚持某种解释、利用裁量空间或规则漏洞，产生技术上合规却不符合制度意图的结果。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **能力导向的智能体基准**：通过预先设计且范围明确的任务与政策，分别测试智能体的规划、指令遵循和工具调用等能力；清晰规则使任务容易判分，但基本消除了真实政策中的解释分歧。
- **基于简化政策和有限结果判定的领域基准**：以$\tau$和$\tau^2$等基准为代表，要求智能体依据简化的领域政策完成交互任务，并常用二元可接受性等有限标准判断结果是否合格。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有基准的政策通常为评测专门编写，具有表述清晰、范围狭窄和贴合指定任务等特点；这提高了可判分性，却抽掉了现实部署中政策不完整、语义含混以及多种解释并存的核心困难，因而无法检验模型如何使用裁量权。
- 仅以任务是否成功或结果是否可接受等有限尺度评价，会把政策解释过程和最终结果压缩为单一标签；当多个结论均可辩护时，这类评价难以揭示模型是否遵循政策、如何说明理由、是否受交互角色影响，以及是否兼顾不同利益相关方。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

目前缺少一种以真实政策歧义为任务来源、明确允许多个合理结果，并能在完整对话过程中细粒度观察智能体解释、互动和决策行为的基准；尤其缺少对不同模型是否形成稳定但彼此冲突的政策解释，以及顾客与客服角色设定如何改变结果的系统比较。

</div>
<div markdown="1"><span>核心问题</span>

当零售退货政策没有唯一无争议的解释时，大语言模型智能体会如何理解并执行政策、说明其决定、平衡竞争性利益；这些行为与结果又会怎样随模型、歧义类型及对话双方的角色设定而变化？

</div>
<div markdown="1"><span>作者直觉</span>

与人为制造一道规则明确、答案唯一的退货题相比，直接从真实政策的模糊词语、指代不清和条件缺失处生成案例，更容易暴露模型实际采用的解释偏好。再让具有不同性格倾向的顾客与客服智能体展开双向对话，并从多个维度分别评价过程和结果，就能区分“完成了任务”与“以合理、可解释且符合政策意图的方式完成任务”，也能观察交互压力是否推动模型改变裁量决定。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

DRIP-R不是训练新模型的方法，而是一个在真实零售政策歧义下评测大语言模型客服代理的交互式基准。其核心做法是：以Amazon公开退货政策为领域规则，将存在多种合理解释的政策条款转化为用户退货任务；再把任务与用户画像组合成场景，由模型客服代理和模拟用户在部分可观测的双人环境中对话。代理可以查询或操作工具，最终依据完整对话给出一种处理结果及相应推理；系统不使用单一的“成功/失败”标签，而从政策遵循、对话质量、行为与利益对齐、任务解决对齐等多个维度评价整个过程。

形式上，政策库$B_P$由自然语言条款$p_i$构成，每个条款可能对应多个合理解释。任务$\tau$依赖至少一个歧义条款，并关联一个包含多种可辩护处理结果的集合$B_O(\tau)$；因此，基准不预设唯一标准答案。直观地说，该方法不是检查客服是否“猜中答案”，而是观察它面对规则边界不清的真实情形时，能否收集信息、正确使用工具、与具有不同沟通风格的用户协商，并给出符合某种合理政策解释且有充分理由的决定。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤1：建立歧义政策与任务表示

将政策表示为条款序列$B_P=(p_1,p_2,\dots,p_N)$，并为可能含糊的条款$p_i$保留合理解释集合$\mathcal{I}(p_i)$。据此构造退货任务$\tau\in B_T$，且每个任务至少依赖一个歧义条款$p_i\in B_P^{\mathrm{amb}}$。

<div class="method-step__io" markdown="1">

**输入**：Amazon公开退货政策中的自然语言规则、规范和共享处理策略，以及商品状态、购买与送达时间、顾客情况、品类例外和资格条件等退货信息。<br>
**输出**：一个由领域政策$B_P$和用户中心退货任务集合$B_T$构成的基准问题空间。

</div>

**直观理解**：同一句退货规则在不同上下文中可能有不止一种合理读法，因此基准先明确哪些任务真正触及这种解释分歧，而不是制造只有一个固定答案的普通问答题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤2：标注多种可辩护结果并生成场景

为任务建立有限的合理结果集合$B_O(\tau)$，其中不同结果对应相关政策条款的不同合理解释；随后将任务与用户画像$\pi$组合为场景$\sigma=(\tau,\pi)$。画像只控制模拟用户的行为、沟通方式和表达偏好，不改变任务本身的合理结果集合。

<div class="method-step__io" markdown="1">

**输入**：任务$\tau$、其所依赖政策条款的合理解释，以及用户画像库$\Pi$。<br>
**输出**：包含退货事实、多个可辩护结果和用户交互风格的场景$\sigma$。

</div>

**直观理解**：同一个退货问题可以交给不同性格或沟通风格的顾客来提出，但哪些处理决定在政策上站得住脚不应随顾客性格改变。这样可以把“政策推理能力”和“应对不同用户的能力”分开考察。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤3：运行双人客服对话仿真

在遵循Dec-POMDP形式的双人环境中，模拟用户与客服代理轮流采取动作；环境状态包含对话历史和底层模拟数据库状态，转移函数根据当前状态与动作生成下一状态和新观测。只有客服代理能够调用工具，每轮可包含若干工具调用以及一条发给对方的自然语言消息。

<div class="method-step__io" markdown="1">

**输入**：场景$\sigma$、通用领域政策、任务约束、代理和用户各自的观测，以及代理可使用的客服工具。<br>
**输出**：完整对话$\mathcal{C}=(T_1,T_2,\dots,T_n)$，其中包含用户消息、代理消息和代理的工具调用轨迹。

</div>

**直观理解**：代理并非一次性阅读题目后作答，而是像真实客服一样边询问、边查询系统、边与用户协商；它只能看到当前消息和工具返回的信息，不能直接读取所有隐藏状态。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤4：解析最终决定并进行多维评价

由解析函数$\rho$将对话映射为结果$o$和理由$r$；若用户中止或达到轮数上限，则结果与推理可记为$\bot$。评价函数$\mathcal{E}$结合任务、全部交互和最终解决方案，在政策遵循、对话质量、行为对齐、利益对齐和任务解决对齐等维度产生向量分数。

<div class="method-step__io" markdown="1">

**输入**：任务$\tau$、完整对话$\mathcal{C}$以及代理在结束时生成的决定和推理。<br>
**输出**：结构化解决结果$\rho(\mathcal{C})=(o,r)$及多维评价向量$e\in\mathbb{R}^d$。

</div>

**直观理解**：评测不仅看客服最后是退款还是拒绝，还检查它是否遵守政策、是否进行了合适的沟通和工具操作，以及其决定是否属于当前歧义条件下可辩护的解决办法。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 歧义任务的多结果定义

$$
B_O(\tau)=\{o_1,\dots,o_{m_\tau}\}\subset B_O,\qquad \tau\text{ is ambiguous}\iff |B_O(\tau)|\ge 2
$$

**符号说明**

- $\tau$：一个包含商品及购买、送达时间等信息的用户退货任务。
- $B_O$：基准允许的全部结果类别所构成的集合。
- $B_O(\tau)$：对任务而言可由歧义政策合理支持的结果集合。
- $o_j$：任务的一种可辩护结果，对应相关政策条款的一种合理解释。
- $m_\tau$：任务所具有的可辩护结果数量。

<div class="equation-explanation" markdown="1">

**直观理解**：该定义是基准区别于单答案任务的关键：只要同一退货任务在政策上下文中至少允许两个合理结果，它就是歧义任务。因而评测重点应是决定是否可辩护及其推理是否充分，而不是是否匹配唯一标签。<br>
**原文位置**：第2.2节，Task ambiguity

</div>

</div>

<div class="equation-block" markdown="1">

#### 解决解析与多维评价

$$
\rho:\mathcal{C}\rightarrow(B_O\cup\{\bot\})\times\mathcal{R},\quad \rho(\mathcal{C})=(o,r);\qquad \mathcal{E}(\tau,\mathcal{C},\rho(\mathcal{C}))=e\in\mathbb{R}^{d}
$$

**符号说明**

- $\rho$：把已完成对话解析为最终结果和推理的解决函数；在DRIP-R中由客服代理模型实现。
- $\mathcal{C}$：用户与客服代理之间的完整对话，包括消息和工具调用。
- $o$：客服代理最终承诺执行的处理结果。
- $r$：客服代理在对话结束时生成的决策推理。
- $\bot$：没有形成正常解决结果；例如用户中止或对话达到最大轮数。
- $\mathcal{R}$：代理可生成的推理内容空间。
- $\mathcal{E}$：结合任务、对话和最终解决方案的多维评价函数。
- $e$：评价函数输出的$d$维实数向量。
- $d$：评价轴及其子维度的总数。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分把自由形式的完整对话压缩为“做了什么决定、为什么这样决定”；第二部分再从多个角度评价这项决定及其形成过程。这样可避免用一个二元成功标记掩盖政策遵循、沟通质量与结果合理性之间的差异。<br>
**原文位置**：第2.2节，Resolution function与Evaluation

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。所给章节将DRIP-R定义为交互式评测基准，没有提出参数训练目标、损失函数或基于评价向量$e$更新模型参数的优化过程；$\mathcal{E}$用于比较代理表现，而非被明确描述为训练奖励。不能据此推断参与评测的客服代理或用户模拟器经过了何种额外训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 政策歧义与多结果任务模块**

政策$B_P$由自然语言条款$p_i$组成，每个条款具有可能为单元素或多元素的解释集合$\mathcal{I}(p_i)$。任务$\tau$对应合理结果集合$B_O(\tau)\subset B_O$；当$|B_O(\tau)|\geq 2$时任务被定义为歧义任务，而DRIP-R中的所有任务均按此条件构造。全局结果空间$B_O$包括全额退款、部分退款、礼品卡退款、拒绝退款、换货、转人工和用户中止七类。

> 直观理解：该模块承认政策含糊时可能不存在唯一正确决定。它考察代理能否找到并论证一种合理处理方式，而不是用单一答案把其他可辩护决定错误地判为失败。

**2. 基于Dec-POMDP的交互环境**

环境表示为$\bigl(\mathcal{S},\{\mathcal{A}_i\},\{\mathcal{O}_i\},\mathcal{T},\mathcal{M},\mathcal{U}_\sigma,\mathcal{E}\bigr)$，参与者$i\in\{\text{agent},\text{user}\}$。其中$\mathcal{S}$覆盖对话和数据库状态，$\mathcal{A}_i$与$\mathcal{O}_i$分别是动作及观测空间，$\mathcal{M}$是自然语言消息空间，$\mathcal{U}_\sigma$包含通用政策和场景约束；工具权限仅授予客服代理。

> 直观理解：部分可观测意味着双方都要通过对话或工具逐步获得信息。采用这一结构是为了评测连续决策过程，避免把真实客服任务简化成静态选择题。

**3. 解决解析与多维评价模块**

客服代理在对话结束时基于完整历史生成最终结果$o$和推理$r$，由$\rho$形成结构化记录；评价函数$\mathcal{E}$以任务、对话和该记录为输入，并输出$d$维实数向量。它替代$\tau^2$-bench所使用的二元奖励，使不同代理能够按政策、交流、行为和解决质量等方面分别比较。

> 直观理解：一个客服可能给出可接受的退款结果，却在沟通过程中误导用户或不当使用工具；也可能交流良好，但最终决定缺乏政策依据。多维评价用于揭示这些不同类型的优缺点。

**训练与推理**

训练流程：原文所给章节未描述专门训练DRIP-R模型的过程。推理与评测流程：先选择任务$\tau$和用户画像$\pi$组成场景$\sigma$，向交互环境提供通用领域政策和任务特定约束；用户模拟器依据画像控制行为、语言风格和偏好，客服代理依据可见消息及工具反馈选择后续动作。每轮$T_i$可包含代理的零次或多次工具调用，并以用户或代理的一条自然语言消息结束；用户侧不能调用工具。对话在一方发出结束消息或轮数达到$t_{lim}=20$时终止。正常结束时，代理依据完整对话生成最终结果$o$和理由$r$；若用户中止或达到轮数限制，则解析结果可为$\bot$。最后，系统以$\mathcal{E}(\tau,\mathcal{C},\rho(\mathcal{C}))$对任务事实、交互轨迹和最终解决方案进行联合评价。

**复现信息**

公平解释结果所需的关键设定包括：基准以Amazon公开退货政策为政策基础；所有任务均依赖至少一个歧义条款，并按$|B_O(\tau)|\geq2$构造，因此不存在唯一正确结果。结果空间覆盖七类处理：全额退款、部分退款、礼品卡退款、拒绝退款、换货、转人工和用户中止。场景中的用户画像影响模拟用户的行为、沟通风格和陈述偏好，但按设计不改变$B_O(\tau)$。交互最多进行20轮，只有客服代理有工具权限；状态还包含底层模拟数据库。所给材料没有明确列出具体工具接口、模型版本、解码参数、提示模板、各评价维度的计算细节或评价器实现，复现这些部分需要核对论文其余章节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- DRIP-R主评测集：包含40个经人工核验的零售退货任务和10个客户人格，两两配对形成400个场景。任务由真实政策中的歧义驱动，并包含订单时间线、商品状态、配送状态和客户情境；其作用是评估模型在信息不完整、政策允许多种合理解释时的多轮决策能力。任务复杂度分布为Very High 230个、High 160个、Medium 10个。
- Amazon Product Descriptions VLM：公开商品描述数据，仅用于为每个任务随机抽取2至3件商品并提供具体商品信息；商品组合不在不同任务间复用。它不是独立测试集，而是提高退货场景真实性和商品条件多样性的素材来源。
- Persona-Hub衍生人格集：作者从Persona-Hub的elite personas出发，加入大五人格、沟通方式、语言特征及人口统计属性，从30个候选人格中人工保留10个。该数据用于控制客户模拟器的行为，并测试人格差异是否影响模型给出的处理结果。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**政策遵循度（Policy Adherence/Policy Support）**

在单轮、整段对话和最终解决方案三个层级，判断代理的说法和决定是否能由给定政策文本支持。该指标评估的是“能否由政策辩护”，而不是在歧义条件下强行指定唯一正确答案。 （越高越好；高分表示代理较少脱离政策或作出缺乏文本依据的承诺，但不代表其处理方案是唯一合理方案。）

</div>
<div class="metric-item" markdown="1">

**跨模型与模型内解决一致率**

跨模型一致性把同一场景的四个模型结果分为完全一致、部分一致和完全不一致；模型内一致性则比较同一模型对同一场景重复运行三次时的成对结果是否相同。两者共同测量歧义下决策的稳定程度。 （一致率越高表示结果越稳定；但高一致性本身不保证政策遵循度或客户服务质量更高。）

</div>
<div class="metric-item" markdown="1">

**利益平衡与结果倾向**

利益平衡分数定义为客户目标对齐减去公司利益对齐，并用Spearman相关检验其与有序人格特征的单调关系；代理人格分析还将七类结果映射为0至6的客户友好序数，并比较拒绝率。 （没有统一的越高越好方向：正值更偏向客户，负值更偏向公司。理想表现取决于政策和任务要求；人格不应在缺乏业务依据时造成系统性待遇差异。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 同一DRIP-R场景上四个模型最终解决类型的跨模型一致性

<div class="result-value" markdown="1">

四个模型仅在4.2%的场景中完全给出相同结果，13.3%的场景中四者结果全部不同，其余82.4%为部分一致。作者据此主张，政策歧义会造成显著的跨模型解决不稳定性。

</div>

多数场景并非所有模型都作出同一种处理，说明模型选择会实质影响客户获得退款、拒绝或升级处理等结果。由于任务本来就允许多种可辩护解释，这一结果证明的是“决策不稳定”，而不是偏离多数意见的模型必然错误；同时，实验没有提供无歧义任务上的对应一致率，因此不能仅凭4.2%精确估计歧义造成的全部因果影响。

<div class="result-source" markdown="1">

来源：Section 4.2, “Impact of policy ambiguity on model resolution”; Figure 3(b)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Overall, only 4.2% of scenarios yield full agreement (all four models converge on the same resolution), and 13.3% yield full disagreement (every model produces a distinct outcome). The remaining 82.4% show partial agreement (some but not all models converge).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 分辨最终解决类型后的逐轮政策支持轨迹

<div class="result-value" markdown="1">

升级处理在对话结束时维持较高政策遵循度，而直接授予退款的轨迹相对早期水平下降更多；GPT-5在不同结果组中的逐轮得分始终不低于4.83。作者将其解释为，不同最终决定对应不同程度的对话后期政策依据漂移。

</div>

代理可能在早期按政策谨慎收集信息，但在形成最终决定时逐渐偏离自己先前的政策推理；这种漂移在部分开放模型上更明显。GPT-5的高而平稳轨迹表明其对话内政策依据更稳定，但该指标只衡量决定是否有政策支撑，并不能证明GPT-5选择了唯一正确、最公平或最有利于客户的结果。

<div class="result-source" markdown="1">

来源：Section 4.2, “Impact of ambiguities on conversations”; Figure 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across all four models, escalation maintains end-of-conversation adherence at or near the top of the bucket ordering, while refund-granting outcomes drop further than escalation from their early-conversation levels. The drift is most striking in Qwen3-35B and OSS-120B, where buckets diverge around the conversation midpoint; GPT-4.1 shows a smaller, earlier dip that flattens; and GPT-5 stays uniformly high (≥ 4.83) across outcomes.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 客户大五人格与客户目标—公司利益平衡分数的关联

<div class="result-value" markdown="1">

外向性与更偏客户的结果呈弱正相关，$ρ=0.077$、$p=0.0016$；神经质同样呈弱正相关，$ρ=0.109$、$p<0.0001$；宜人性则呈弱负相关，$ρ=-0.054$、$p=0.0259$。开放性和尽责性未发现显著相关。

</div>

在该模拟环境中，更外向或更神经质的客户略可能得到偏向客户目标的结果，而更宜人的客户略偏向公司利益。作者据此提出公平性疑问；但相关系数都很小，实验只能说明统计关联，不能证明人格直接导致了结果，也不能直接外推到真实客户、真实客服或其他政策领域。

<div class="result-source" markdown="1">

来源：Section 4.2, “Impact of user personas on alignment”; Figure 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Though effect sizes were small overall, for Extraversion and Neuroticism we found that highly extraverted (ρ = 0.077, p = 0.0016) and highly neurotic (ρ = 0.109, p < 0.0001) user personas were associated with results that favor customer goal alignment over company interest alignment. Whereas user personas that were more agreeable were associated with lower customer goal alignment scores and higher company interest alignment scores (ρ = −0.054, p = 0.0259).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测与客户模拟均高度依赖大语言模型：客户由GPT-4o-mini生成，裁判由GPT-5.4执行。尽管裁判经人工校准后达到0.84的相邻一致率，其七分类解决类型准确率仅为56%，且人工标注者在五点量表上的平均精确一致率只有0.23；因此细粒度分数和结果类别仍可能包含显著测量误差。
- 外部有效性有限：基准只有40个退货任务、10个合成人格和400种固定配对，且集中于单一电商退货政策环境。人格相关效应很小，场景也并非真实客户互动，因此不能据此断言真实客服系统必然歧视特定人格，或将模型排名直接推广到其他企业、语言、政策及服务领域。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- GPT-5（gpt-5-2025-08-07）：API模型，也是总体对话内指标表现最强的参照，用来代表较新的闭源客服代理能力。
- GPT-4.1（gpt-4.1-2025-04-14）：API模型；在部分最终解决层指标上略优于GPT-5，因此可检验更新模型是否在所有决策维度上都占优。
- gpt-oss-120b：开放权重模型，用来比较开放模型与API模型在歧义政策推理、对话一致性及重复运行稳定性方面的差异。
- Qwen3.6-35B-A3B：开放权重模型，与gpt-oss-120b共同构成开放模型对照，并用于观察不同模型架构和来源是否产生不同的解决轨迹。

**实验想回答的问题**

- 在真实零售退货政策存在歧义时，不同大语言模型能否形成稳定、可由政策文本辩护且满足用户请求的对话与最终处理方案？同一模型重复运行时的决策稳定性，与不同模型之间的一致性有何差别？
- 客户人格与客服代理人格是否会系统性改变客户利益和公司利益之间的平衡，以及拒绝、退款、换货或升级处理等最终结果？

**实验实现**

每个代理在400个场景中仅收到与其角色有关的信息，完整任务细节、明确标注的政策歧义和退货答案均被隐藏，以模拟实际部署。客服提示要求模型在决策前收集相关事实，每轮先执行工具调用再输出消息；客户由GPT-4o-mini模拟。代理和客户温度均为0.7，以产生一定响应多样性。最终输出包含七类之一的结构化解决类型，以及说明政策冲突、权衡、条件和已收集事实的自由文本解释。评测采用并行LLM-as-a-Judge：不同裁判分别负责政策与任务解决遵循、对话质量、行为对齐和利益对齐，编排器检查格式并聚合结果；裁判统一使用温度为0的gpt-5.4-2026-03-05。裁判校准使用30个经专家标注的实例，其中5个由分布保持少样本采样选作示例，25个作为留出测试集；校准后的平均偏差为0.33，五点量表相差不超过1分的一致率为0.84。为分析随机性，作者还在分层子样本上让每个代理模型重复运行三次。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 政策受控消融：为每一种歧义向代理提供确定性规则，而其他设置保持不变 | 明确消除政策歧义后，政策遵循度提高0.26，行为对齐没有变化。 | 该消融直接隔离“歧义是否被明确解决”这一因素。政策遵循度提高而人格行为对齐不变，支持改进来自更明确的决策规则，而非代理整体变得更顺从或人格表达发生变化。不过原文节选未给出该0.26变化的置信区间、显著性检验或各模型分项，因此不能判断提升在每个模型上是否同样稳定。 | Section 4.2, “Impact of policy ambiguity on model resolution”; Appendix C.1<br><span class="experiment-evidence">In addition, a policy-controlled ablation (Appendix C.1) where the agent receives a deterministic rule for each ambiguity raises Policy Adherence by +0.26 without affecting Behavioral Alignment, showing that resolving ambiguity directly improves outcome quality.</span> |

**定性案例**

- 代理人格提供了一个定性行为案例：Direct代理在所有模型中均表现出最高拒绝率，Very_Helpful代理则最低；合并分析显示人格与拒绝率相关，$χ^2(4)=59.03$、$p<0.001$。这说明即使任务和政策相同，系统提示规定的客服风格也可能成为决定结果的“锚点”。但拒绝减少后究竟转化为全额退款、部分退款还是升级处理仍取决于模型，因此人格只能解释部分变化，不能替代对模型决策机制的分析。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces a benchmark for evaluating decision-making and reasoning under ambiguous real-world retail policies.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`9f6013c61735d30779ba47050d84e2f67d2042e623a1df60d5a501ed3cfce973`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
