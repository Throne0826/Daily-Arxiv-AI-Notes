---
title: "[论文解读] PL-Guard: Probabilistic Logic Reasoning for LLM Guardrails"
description: "[arXiv 2608.15673][LLM 安全] 本文提出 PL-Guard，将大语言模型护栏中的语义事实识别与政策推理分离，先由本地语言模型估计政策谓词成立的概率，再由 ProbLog 按显式规则推断风险，以提高决策的可检查性并更清楚地呈现安全性与有用性之间的权衡。"
arxiv_id: "2608.15673"
announcement_date: "2026-08-18"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:18:03.410659+00:00"
source_sha256: "9efd7dfd99a47c661b64fda2a8cfa44a4e0b0b2e3fa31525f2bd3dca8532b099"
tags:
  - "LLM 安全"
  - "LLM Reasoning"
  - "大语言模型护栏"
  - "政策一致性"
  - "神经符号推理"
  - "概率逻辑"
  - "ProbLog"
  - "语义落地"
  - "不安全服从"
  - "过度拒答"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2608.15673</p>

# PL-Guard: Probabilistic Logic Reasoning for LLM Guardrails

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Satchit Chatterji, Shihan Wang, Giovanni Sileno, Erman Acar</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Amsterdam and Utrecht University and University of Amsterdam and University of Amsterdam；Affiliation: University of Amsterdam；Utrecht University；University of Amsterdam</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.15673) · [PDF 下载](https://arxiv.org/pdf/2608.15673) · **关键词** 大语言模型护栏, 政策一致性, 神经符号推理, 概率逻辑, ProbLog, 语义落地, 不安全服从, 过度拒答<br>


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

本文提出 PL-Guard，将大语言模型护栏中的语义事实识别与政策推理分离，先由本地语言模型估计政策谓词成立的概率，再由 ProbLog 按显式规则推断风险，以提高决策的可检查性并更清楚地呈现安全性与有用性之间的权衡。

**不用术语来说**：用户请求即使提到暴力、违法等敏感内容，也可能只是教育、历史、虚构或比喻性讨论；真正有害的请求则可能使用礼貌、含蓄的表达。因此，安全系统不能只看关键词，而要结合请求与回答的实际含义判断是否构成有害协助。判断过松会让模型提供危险信息，判断过严又会拒绝正常问题。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 将大语言模型护栏具体表述为概率逻辑的政策一致性检查：神经模型负责把提示词与回答映射为带概率的政策谓词，符号程序负责根据明确规则推导政策风险，从架构上拆分语义落地与政策推理。
- 提出以归一化的 True/False 词元概率作为谓词概率、以 ProbLog 计算规则级风险概率的可审计接口；作者还通过政策粒度消融研究谓词与规则结构如何影响安全性和有用性的权衡。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型（LLM）护栏，即在模型生成内容前后，通过外部控制机制检查或修改响应，使其符合预先规定的安全政策。本文将护栏形式化为政策一致性判断：系统首先从用户请求与模型响应中识别政策相关事实，再依据由规则组成的政策推断这些事实是否构成违规。核心困难在于，表面上涉及暴力、违法或其他敏感主题的请求可能属于教育、历史、虚构或比喻语境，而真正有害的请求也可能采用礼貌或间接表达。因此，系统需要同时控制两类错误：对有害请求提供帮助的“不安全服从”，以及拒绝正常请求的“过度拒答”。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**语义落地（semantic grounding）**

语义落地是把自然语言中的具体请求和响应，转换为政策可以处理的结构化事实。例如，系统可以判断某个请求是否要求提供有害操作步骤。本文中，LLM负责从文本得到这些事实对应的概率，而不是直接决定最终政策结论。

</div>
<div class="concept-item" markdown="1">

**神经符号方法（neurosymbolic method）**

神经符号方法把神经网络的语言理解能力与符号系统的规则推理能力结合起来。本文让LLM负责理解文本，让概率逻辑程序负责依据明确规则进行推断，从而把“看懂文本”和“执行政策”分开。

</div>
<div class="concept-item" markdown="1">

**ProbLog概率逻辑**

ProbLog是一种能够同时表示概率事实、逻辑规则和查询结果的概率逻辑系统。它可以在事实存在不确定性的情况下继续推理，因此适合处理LLM对政策事实判断并非完全可靠的情形。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定用户请求 $P_{in}$、基础LLM $L_{base}$ 生成的初始响应 $O_{base}$，以及由自然语言政策预先转换得到的谓词集合和ProbLog规则，系统需要判断该请求—响应对是否符合政策，并输出行动建议与最终响应 $O_{final}$。其中，谓词是可被判断为真或假的政策相关事实，例如某响应是否提供了有害帮助；每个谓词不必被硬性判为真或假，而是由评估LLM根据归一化的 True/False 词元分数赋予概率。随后，ProbLog依据这些概率事实和政策规则计算规则层面的风险概率，行动建议再用于指导基础LLM生成最终输出。该设定假定政策能够被表达为谓词和逻辑规则，且本地评估LLM能够对这些谓词进行相对稳定的文本判断。本文主要关注开放式用户交互中的安全—有用性权衡：不安全服从属于更严重的安全失败，过度拒答则主要损害正常使用体验。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$P_{in}$**

用户输入或请求。

</div>
<div class="notation-item" markdown="1">

**$O_{base}$**

基础LLM在护栏处理前生成的初始响应。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{KB}_{preds}$**

政策谓词知识库，即需要由评估LLM判断的政策相关谓词集合。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{KB}_{policy}$**

政策规则知识库，由ProbLog谓词、概率事实及其逻辑规则组成，用于计算政策风险或行动条件。

</div>

</div>

**直接相关的工作**

- **Policy prompting与政策或宪法引导的无害化方法**: 这类方法把自然语言政策直接提供给LLM，要求同一个模型理解请求、解释政策并生成符合政策的响应。PL-Guard保留自然语言政策作为来源，但先将其转换为谓词和ProbLog规则，把文本语义判断与政策推理分离。
- **LLM-as-a-judge护栏流程**: 这类方法使用一个LLM判断响应是否违反政策，并可能生成理由或修订建议；其优点是灵活，但判断过程通常以自由文本结论为主要接口，容易受到模型偏差和推理可靠性的影响。PL-Guard改为输出谓词概率，并由ProbLog显式计算规则层面的概率，使中间判断和政策推理过程更容易检查。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

面向开放用户的大语言模型需要在两个代价不对称的错误之间取得平衡：一是“unsafe compliance”，即没有识别出危险行为而提供有害协助，相当于以检测不安全行为为正类时的假阴性；二是“over-refusal”，即把无害请求误判为危险并拒绝回答，相当于假阳性。前者可能直接助长伤害，通常比主要损害可用性的后者更严重，但单纯扩大拒绝范围也会显著削弱系统对正常用户的帮助。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **政策提示（policy prompting）**：把自然语言安全政策直接提供给生成模型，要求模型在生成回答时自行理解政策、判断当前语境并遵守相应约束。
- **LLM-as-a-judge**：使用一个语言模型充当裁判，阅读用户请求、候选回答和政策，直接判断回答是否违规，并可能生成理由或修改建议来指导后续回答。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 两类方法通常让同一个语言模型同时判断“请求与回答中哪些政策相关事实成立”和“这些事实依据政策意味着什么”，使语义落地与政策推理相互纠缠。发生误判时，很难确定错误来自事实识别还是规则应用，因而不易检查、调试和修订。
- 自由形式的模型裁决可能受评估偏差和有限推理可靠性的影响；面对表面敏感但实际无害的语境，系统可能过度拒绝，而面对措辞礼貌或间接的有害请求，又可能错误放行。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有护栏缺少一种能够接收神经模型对语义事实的不确定判断、再依据可显式检查的政策规则独立完成推理的统一接口。尤其尚不清楚，概率化谓词与符号规则的组合能否在不把语义判断过早离散化的情况下有效降低危险放行，并通过中间结果揭示具体风险来源及安全性与有用性的取舍。

</div>
<div markdown="1"><span>核心问题</span>

将护栏分解为“语言模型估计政策谓词概率”和“ProbLog 根据显式政策规则推断风险”两个阶段，是否能比基础生成、政策提示和自由形式的 LLM 裁判更可靠地阻止有害协助，同时提供可审计的中间推理；政策谓词与规则的粒度又会如何改变过度拒绝与危险放行之间的平衡？

</div>
<div markdown="1"><span>作者直觉</span>

语言模型擅长理解自然语言，却未必能稳定地同时执行复杂政策；逻辑程序擅长一致地应用规则，却不能直接理解文本。PL-Guard 让两者各做其所长：语言模型只回答诸如“是否存在有害意图”“回答是否提供实质协助”等事实成立的可能性，ProbLog 再把这些概率代入固定规则。保留概率而不是立即作硬性的真假判断，可以让边界语境中的不确定性继续参与推理；同时，谓词概率和规则概率分别显示系统“看到了什么”以及“为何据此判为风险”，便于定位错误和调整政策。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PL-Guard 将自然语言安全政策转换为可执行、可审计的 ProbLog 符号政策，并在推理阶段对基础大语言模型生成的回答进行概率化检查与修复。系统不是直接输出一个二元的“安全/不安全”标签，而是分别估计不安全服从和过度拒答等政策规则的成立概率，再依据安全优先的动作阈值决定保留、拒答或重写回答。整体输入是自然语言政策 $R_{NL}$、用户请求 $P_{in}$ 和基础模型 $L_{base}$；整体输出是符合政策的最终回答 $O_{final}$，同时保留谓词概率、规则概率和动作推荐等中间轨迹。直观地说，PL-Guard 先把政策写成一组可检查的规则，再让模型提供带不确定性的事实，最后由符号推理器检查这些事实是否触发风险或过度拒答。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 离线政策符号化

$L_{setup}$ 分析政策中的安全条件、风险类型和允许的响应行为，生成谓词知识库 $\mathcal{KB}_{preds}$ 与政策规则知识库 $\mathcal{KB}_{policy}$。前者规定需要从请求—回答对中判断哪些事实，后者用 ProbLog 规则定义不安全服从、过度拒答及其更细粒度的原因。

<div class="method-step__io" markdown="1">

**输入**：自然语言政策 $R_{NL}$，以及用于政策配置的设置模型 $L_{setup}$。<br>
**输出**：一组可由请求和回答实例化的政策谓词，以及建立在这些谓词之上的 ProbLog 程序。

</div>

**直观理解**：这一步相当于把“遇到危险请求应拒绝、遇到安全但敏感的问题不应无故拒答”这样的文字规范，整理成检查清单和判断规则。它只需离线完成一次，之后可以通过修改谓词或规则来更新政策，而不必重新训练基础模型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基础回答生成

系统先计算 $L_{base}(P_{in})$，得到未经 PL-Guard 检查的初始回答 $O_{base}$。该回答既可能安全且有帮助，也可能执行有害请求，或者对本来可以回答的请求进行拒答。

<div class="method-step__io" markdown="1">

**输入**：用户请求 $P_{in}$ 和基础大语言模型 $L_{base}$。<br>
**输出**：初始模型回答 $O_{base}$。

</div>

**直观理解**：PL-Guard 先观察模型通常会怎么回答，再判断这个回答是否符合政策；这样它既能发现“答得太危险”，也能发现“拒绝得太多”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 谓词概率化接地

对每个谓词 $p_i$，$L_{judge}$ 根据请求、回答和谓词描述，读取继续生成 `True` 与 `False` 的概率，并按 $\hat{p}_i=q_i^T/(q_i^T+q_i^F)$ 重新归一化。由此形成向量 $\mathcal{I}_{preds}\in[0,1]^{|\mathcal{KB}_{preds}|}$，其中每个分量表示相应事实成立的概率，而不是强制作出不透明的二元判断。

<div class="method-step__io" markdown="1">

**输入**：请求 $P_{in}$、初始回答 $O_{base}$、谓词集合 $\mathcal{KB}_{preds}$ 和判断模型 $L_{judge}$。<br>
**输出**：谓词概率向量 $\mathcal{I}_{preds}$，例如“请求有害”“回答有害”“模型拒答”和“敏感语境中但请求本身无害”等事实的概率。

</div>

**直观理解**：判断模型不必写一段理由，只需比较“真”和“假”两个候选词的概率。这样既保留了模型对边界案例的犹豫程度，也便于批量处理和复查。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### ProbLog 政策推理与动作选择

求解器将谓词概率作为概率事实，按政策规则推导规则结果，得到 $\mathcal{I}_{policy}\in[0,1]^{|\mathcal{KB}_{policy}|}$。系统分别寻找不安全服从规则和过度拒答规则中概率最高的结果：若任一不安全规则超过阈值，则推荐 `refuse_or_rewrite`；否则若过度拒答规则超过阈值，则推荐 `answer_helpfully`；两者均未超过阈值时推荐 `preserve_or_answer`。

<div class="method-step__io" markdown="1">

**输入**：谓词概率向量 $\mathcal{I}_{preds}$、政策规则库 $\mathcal{KB}_{policy}$、ProbLog 求解器 $\mathcal{S}$ 和可调动作阈值。<br>
**输出**：政策规则概率向量 $\mathcal{I}_{policy}$ 以及一个动作推荐。

</div>

**直观理解**：符号层像一名按照明确规章办事的审查员：先优先处理可能造成伤害的情况，再处理不必要拒答，最后才保留原回答。系统关注最有力的具体违规理由，避免规则越写越细后，大量很弱的风险路径被简单累加成虚高的总风险。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 谓词概率归一化

$$
\hat{p}_{i}=\frac{q_{i}^{T}}{q_{i}^{T}+q_{i}^{F}}
$$

**符号说明**

- $\hat{p}_{i}$：谓词 $p_i$ 成立，即取值为 True 的最终概率。
- $p_i$：第 $i$ 个政策谓词，例如请求是否有害或回答是否造成伤害。
- $q_i^T$：判断模型在给定请求、初始回答和谓词描述后，为 token `True` 分配的概率。
- $q_i^F$：相同条件下，判断模型为 token `False` 分配的概率。
- $L_{judge}$：用于谓词判断的语言模型。
- $P_{in}$：用户输入的请求。
- $O_{base}$：基础模型未经检查生成的初始回答。

<div class="equation-explanation" markdown="1">

**直观理解**：模型原始词表中的概率可能还包含其他 token，因此系统只比较 `True` 和 `False`，再把二者归一化为总和为 $1$ 的二元概率。结果越接近 $1$，表示判断模型越支持谓词成立；接近 $0.5$ 则表示案例存在明显不确定性。<br>
**原文位置**：第 2.2 节，公式 (3)

</div>

</div>

<div class="equation-block" markdown="1">

#### 符号政策推理

$$
\mathcal{S}(\mathcal{I}_{preds},\mathcal{KB}_{policy})\rightarrow\mathcal{I}_{policy}
$$

**符号说明**

- $\mathcal{S}$：ProbLog 求解器，负责依据规则从概率事实推导政策结论。
- $\mathcal{I}_{preds}$：由谓词接地阶段产生的概率事实向量，属于 $[0,1]^{|\mathcal{KB}_{preds}|}$。
- $\mathcal{KB}_{policy}$：由 ProbLog 编写的政策规则集合，包括不安全服从和过度拒答等规则。
- $\mathcal{I}_{policy}$：各政策规则结论的概率向量，属于 $[0,1]^{|\mathcal{KB}_{policy}|}$。

<div class="equation-explanation" markdown="1">

**直观理解**：该式表示从“若干带概率的事实”到“若干带概率的政策结论”的推理过程。它把神经模型负责的事实识别与符号系统负责的规则一致性检查分开，使人可以定位错误究竟来自谓词判断、政策覆盖不足还是动作阈值。<br>
**原文位置**：第 2.2 节，公式 (5)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告 PL-Guard 的端到端训练目标，也未描述通过梯度优化联合训练 $L_{setup}$、$L_{judge}$ 或 $L_{base}$。方法主要依赖离线政策配置、判断模型的概率输出、固定的 ProbLog 规则推理和推理阶段的政策引导生成；因此这里不应虚构交叉熵、强化学习或其他训练损失。政策规则和谓词由人工编写并在实验中借助 GPT-5.5，随后进行人工检查，但这属于政策构建流程，不等同于 PL-Guard 的参数训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 自然语言到 ProbLog 的政策接口**

该模块由 $L_{setup}$ 根据 $R_{NL}$ 产生 $\mathcal{KB}_{preds}$ 和 $\mathcal{KB}_{policy}$。谓词可以描述请求或响应的政策相关事实，例如 $harmful\_request$、$harmful\_response$、$refused\_response$ 和 $benign\_sensitive\_context$；规则则将这些事实组合为具体的风险或过度拒答结论。政策还可以进一步区分教育性、虚构性、可执行伤害、安全重定向和一般良性回答等语境。

> 直观理解：该接口决定系统究竟检查什么、哪些事实会触发什么后果，是政策可解释性的主要来源。政策改变时，优先编辑这里的谓词和规则，而不是把所有安全行为重新压缩进模型参数。

**2. 概率谓词接地器**

$L_{judge}$ 接收同一个请求—回答上下文以及单个谓词描述，通过 `True` 和 `False` 的续写概率估计谓词成立程度。由于各谓词共享前缀上下文，该设计支持 KV 缓存和批处理，并且每个谓词只需生成极少量候选 token；输出的是连续概率而非自由文本判断。

> 直观理解：这一模块负责把自然语言实例翻译成符号规则能使用的“带置信度事实”。它降低了传统 LLM-as-a-judge 中自由文本解析的不确定性，但仍可能因模型误判谓词而把错误事实传给后续推理。

**3. ProbLog 推理与安全优先决策器**

ProbLog 将 $\mathcal{I}_{preds}$ 作为概率事实，依据 $\mathcal{KB}_{policy}$ 计算规则级概率 $\mathcal{I}_{policy}$。决策器分别处理不安全服从和过度拒答两类规则，并采用安全优先的阈值策略，而不是把所有规则路径合成为单一违规分数；最终结果还被回传给 $L_{base}$ 以指导重写。

> 直观理解：该模块把模型的模糊判断放进明确的政策逻辑中，并给出可以追溯的“哪条规则被触发”信息。分开比较具体规则还能避免详细政策因为包含更多弱规则而看起来不合理地更危险。

**训练与推理**

训练方面，原文仅明确说明离线阶段使用 $L_{setup}$ 将自然语言政策 $R_{NL}$ 转换成谓词集合和 ProbLog 规则，并指出实验中的政策由人工编写、借助 GPT-5.5 完成后人工核查。原文未明确报告基础模型或判断模型是否在 PL-Guard 框架内进行额外微调，因此应将二者视为提供生成与概率判断的现成模型组件，不能据此推断存在联合训练。

**复现信息**

复现时需要固定自然语言政策、谓词清单、ProbLog 程序、动作阈值、基础模型和判断模型，并明确判断模型如何读取 `True` 与 `False` 的 continuation token 概率。谓词判断可以对共享的请求—回答上下文进行 KV 缓存并批量计算；完整前向流程还包括基础回答生成、逐谓词概率接地、ProbLog 推理和必要的最终重生成。运行时间会受到批处理方式、序列长度和 GPU 利用率影响，因而原文将其视为实现相关测量而非硬件无关常数。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- XSTest 完整基准，共 450 个提示，其中 250 个为安全提示、200 个为不安全提示。安全子集用于检验模型是否因敏感表面词汇或语境而过度拒绝；不安全子集用于检验模型是否输出可操作的有害指导。原文未说明额外的训练集、验证集或随机划分，实验角色是统一的安全护栏评测集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**过度拒绝率（over-refusal）**

在安全提示中，最终回答拒绝请求或无必要地限制正常回答的比例。它衡量护栏对良性请求造成的有用性损失。 （越低越好，因为较低值表示系统更能识别良性语境，不会仅因敏感词汇而拒答。）

</div>
<div class="metric-item" markdown="1">

**不安全服从率（unsafe compliance）**

在不安全提示中，最终回答提供可操作有害指导的比例。它衡量危险请求绕过护栏并获得实用伤害信息的频率。 （越低越好，因为较低值表示护栏更少输出能够直接促成伤害的步骤、材料或操作细节。）

</div>
<div class="metric-item" markdown="1">

**每样本时间（Time/ex.）**

结果表标题显示论文报告每个样本的处理时间，用于比较不同护栏机制引入的推理开销；所给节选没有提供具体计算口径或数值。 （通常越低越好，因为它意味着部署吞吐量更高，但必须结合安全性和过度拒绝率判断，不能单独据此认定方法更优。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前分析严格受所给论文节选限制，缺失的表格数据与结果段落必须回查原始论文后才能补充三项核心结果及消融结论。
- 这是需要结合原文表格、附录和实验代码进一步核验的 AI 分析草稿。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 无防护的 base LLM：直接使用与其他方法相同的 Phi-3-medium 生成回答，用于测量不加入任何护栏机制时的原始安全性与有用性。
- Policy prompting：先把自然语言安全策略加入提示，再附上用户请求。该基线检验仅通过上下文指令表达策略是否足以替代 PL-Guard 的显式谓词判定与概率逻辑推理。
- LLM-as-a-judge：由 Phi-3-medium 充当循环内评审模型，对基础回答作出判断，再由基础模型依据评审信号修复输出。它代表一种常见的生成后审查与重写方案，可用于判断 PL-Guard 的结构化逻辑推理是否优于纯 LLM 自我评审。
- PL-Guard：论文提出的方法，也是被评估系统。它将谓词概率写入 ProbLog，并按照概率逻辑规则和安全优先的动作选择生成最终回答；与三个基线共用同一生成骨干，以尽量把差异归因于护栏机制。

**实验想回答的问题**

- 在相同的 Phi-3-medium 生成骨干和确定性解码条件下，PL-Guard 能否同时减少安全请求上的过度拒绝与不安全请求上的有害服从？
- 相较于无防护模型、自然语言策略提示和 LLM-as-a-judge，PL-Guard 的安全性与有用性权衡及每样本推理开销如何？

**实验实现**

四种方法均使用本地 HuggingFace Phi-3 14B 后端，即 Phi-3-medium，并以温度 $0.0$ 进行确定性解码；XSTest 每次生成最多 512 个新 token。LLM-as-a-judge 基线的循环内评审同样使用 Phi-3-medium。PL-Guard 通过候选标签 True 与 False 的下一 token 延续分数获得谓词概率，并在两个标签上重新归一化；随后把这些概率作为概率事实输入 ProbLog，以阈值 $0.5$ 将规则概率映射为建议动作，并采用安全优先的规则级动作选择。最终保存的回答会清除泄漏的提示词或模板续写，原始生成则保留以便追溯。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：研究使用概率逻辑推理构建LLM护栏，核心同时涉及安全防护与逻辑推理机制。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`9efd7dfd99a47c661b64fda2a8cfa44a4e0b0b2e3fa31525f2bd3dca8532b099`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
