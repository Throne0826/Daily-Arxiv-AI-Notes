---
title: "[论文解读] Compared to What? A Human-Anchored Security Benchmark for LLM-Generated Infrastructure-as-Code"
description: "[arXiv 2608.28021][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.28021"
announcement_date: "2026-08-31"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:38:37.251522+00:00"
source_sha256: "a6a1e4ea2e6f2f5f8f881cc1f27c65329bee7babcf04aaa8a2ea0ee70e741586"
tags:
  - "LLM 评测"
  - "LLM 安全"
  - "LLM 其他"
  - "LLM Reasoning"
  - "基础设施即代码"
  - "大型语言模型"
  - "云安全"
  - "静态分析"
  - "安全基准"
  - "人类基线"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.28021</p>

# Compared to What? A Human-Anchored Security Benchmark for LLM-Generated Infrastructure-as-Code

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Animesh Shaw</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28021v1) · [PDF 下载](https://arxiv.org/pdf/2608.28021v1) · **关键词** 基础设施即代码, 大型语言模型, 云安全, 静态分析, 安全基准, 人类基线<br>
**代码**: [https://github.com/AnimeshShaw/GenIaC-SecBench](https://github.com/AnimeshShaw/GenIaC-SecBench) · **项目页**: [https://huggingface.co/datasets/AnimeshShaw/GenIaC-SecBench](https://huggingface.co/datasets/AnimeshShaw/GenIaC-SecBench)

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

基础设施即代码（Infrastructure-as-Code，IaC）用 Terraform、AWS CloudFormation、Azure Resource Manager 或 Kubernetes 清单等声明式文件描述云基础设施，并将其作为可版本控制的部署工件。与普通应用代码不同，IaC 中的安全错误通常不是潜在缺陷：错误配置会按原样创建存储桶、安全组或 IAM 角色，从而直接暴露云资源。本文关注大型语言模型（LLM）生成 IaC 的安全性评估，核心问题不是模型产生了多少漏洞，而是在使用相同扫描工具并控制工件规模后，模型生成结果相对于人类工程师编写的 IaC 究竟有多不安全。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**声明式 IaC 与资源图**

声明式 IaC 只描述需要哪些云资源及其属性、依赖关系，而不是逐步编写创建资源的程序。因而其安全性主要取决于资源默认配置和资源之间的连接关系，而非传统代码中的控制流。

</div>
<div class="concept-item" markdown="1">

**IaC 安全扫描器与安全策略**

Checkov、Trivy 和 KICS 是通过预定义规则检查 IaC 配置的静态分析工具，例如发现公开存储桶、过度开放的网络规则或不安全的身份权限。扫描器报告的是违反策略的发现项，因此结果既反映配置风险，也可能受到规则覆盖范围和工件规模的影响。

</div>
<div class="concept-item" markdown="1">

**漏洞密度与规模匹配**

漏洞密度是把扫描发现数量按工件中的声明资源数等规模指标进行归一化，用于比较大小不同的 IaC。本文强调，漏洞密度与工件大小呈反向关系；若不在相近资源数范围内比较，差异可能主要来自生成文件大小，而不是真实安全水平。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文构建一个人类锚定的 IaC 安全基准。输入包括分层设计的部署场景、不同厂商和权重开放状态的 LLM 配置，以及人类编写的 IaC 模板；模型根据场景生成 IaC 工件，随后模型工件和人类工件都由相同的 Checkov、Trivy、KICS 工具链扫描。输出是按声明资源数等规模因素匹配后的安全指标，尤其是漏洞发现数量及漏洞密度，并进一步比较标准生成、提示式链式思考和厂商扩展思考三种生成方式。该设定假定静态策略引擎能够以一致方式评估两类工件，同时承认其结果是策略违反项而非对所有真实运行时风险的完整测量。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D_{\mathrm{task}}$**

任务或部署场景数据集；本文中的场景总数为 100，并按架构复杂度分层。

</div>
<div class="notation-item" markdown="1">

**$D_{\mathrm{human}}$**

人类编写的 IaC 模板语料库；本文用它提供与模型工件可比较的人类安全基线。

</div>
<div class="notation-item" markdown="1">

**$N_{\mathrm{res}}$**

IaC 工件中声明的资源数量，是本文进行规模匹配和计算漏洞密度的主要规模指标。

</div>
<div class="notation-item" markdown="1">

**$\rho$**

Spearman 秩相关系数，用于衡量工件大小与漏洞密度之间的单调关联，而不要求变量满足线性关系。

</div>

</div>

**直接相关的工作**

- **SecurityEval 与 EvalPlus**: SecurityEval 面向应用代码中的安全性，EvalPlus 面向应用代码正确性；它们通常以函数为分析单位。本文指出，IaC 的分析单位是声明式资源图，正确性更接近模式或架构有效性，安全问题则集中在资源默认配置，因此不能直接用应用代码基准替代 IaC 基准。
- **Vargas 等人关于生成式 IaC 的评估**: 该工作评估文本到 Terraform 的生成，是本文最接近的先前研究。本文将范围扩展到四种 IaC 格式、按架构复杂度分层的场景、三个独立策略引擎和多评审者人工验证，最关键的区别是加入了 634 个与模型结果使用相同工具链扫描的人类 IaC 模板，因而能够回答“模型相对于谁更不安全”。

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

GenIaC-SecBench是一套用于比较模型生成基础设施即代码（Infrastructure-as-Code，简称IaC）安全性的基准。方法从仅包含功能要求的部署场景出发，让不同模型配置在不被提示安全控制的条件下生成IaC；随后进行语法或模式验证，并使用Checkov、Trivy和KICS三个独立策略引擎扫描漏洞。研究还以相同工具链扫描634份人类编写的IaC模板，按照声明资源数量进行规模匹配，使用每资源漏洞密度而非绝对漏洞数比较模型与人工基线，并通过不完整区组统计、配对检验及带资源数暴露量偏置的负二项广义估计方程分析模型差异与推理模式效果。直观地说，方法不仅问“模型发现了多少问题”，还问“在写出同等规模基础设施时，模型相对于工程师多产生多少问题”，从而避免把代码长短误判为安全性。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造分层部署场景

场景只规定功能需求，不提及安全、加固、合规或具体安全控制；因此模型生成结果主要反映其默认配置，而非对安全提示的服从能力。

<div class="method-step__io" markdown="1">

**输入**：100条自然语言部署场景，其中60条为单服务简单任务，40条为涵盖网络、身份、数据和可观测性的多组件复杂任务；目标云平台包括AWS、Azure、GCP和供应商无关的Kubernetes，目标格式包括Terraform HCL、CloudFormation、ARM和Kubernetes清单。<br>
**输出**：按架构复杂度分层、并带有目标平台和代码格式要求的部署任务记录。

</div>

**直观理解**：相当于给工程师一张“把服务部署起来”的需求单，却不提醒他检查哪些安全选项。这样可以观察模型在没有额外安全提醒时会自然采用什么默认配置。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 按统一协议生成IaC

每次请求均为无状态单次API调用，使用固定系统提示，要求模型以“高级云基础设施工程师”身份输出生产可用IaC，并只输出一个代码块；不使用对话历史、少样本示例、检索或共享记忆。标准生成和提示式思维链的温度为$0.2$，扩展思考使用供应商默认值$1.0$；达到输出上限而被截断的结果被丢弃，无法在128k输出令牌上限内完成的4个复杂场景记为缺失。

<div class="method-step__io" markdown="1">

**输入**：每条场景记录、目标格式指令，以及12种模型配置；其中固定基础模型的三种Anthropic配置分别为标准生成、提示式思维链和供应商扩展思考。<br>
**输出**：最多1200份模型生成IaC制品，实际得到1196份；同时记录每次请求的普通输出令牌和推理令牌使用量。

</div>

**直观理解**：所有模型都在尽量相同的考试规则下答题，唯一刻意改变的变量之一是“是否使用推理模式”。截断代码不纳入分析，是为了避免不完整模板偶然减少漏洞数量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 验证并扫描安全发现

先根据目标格式执行$terraform\ validate$、$cfn-lint$、ARM解析或$kubeconform$验证，再以完全相同的配置交给Checkov、Trivy和KICS扫描。三种引擎的发现数合并为总漏洞发现数，同时从每个制品的抽象语法树（AST）解析声明资源数，而不采用扫描器可能退化的资源计数。

<div class="method-step__io" markdown="1">

**输入**：生成的IaC制品，以及634份来自三个公开仓库的人类编写IaC模板；人工模板通过根键等结构启发式筛选，以排除非IaC文件。<br>
**输出**：每个制品的模式有效性、三引擎安全发现、AST资源数量及覆盖记录；1196份生成制品均由三个引擎扫描。

</div>

**直观理解**：先检查代码是否像对应格式的合法文件，再让三个不同的“安全检查员”独立找问题。人工模板使用同一套检查员和规则，因此规则偏差会同时作用于两边。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 规模匹配并进行统计比较

计算漏洞密度$\text{findings}/\text{declared\ resources}$，在资源数量分层内比较模型与人工制品；模型间使用适合缺失单元的不完整区组Skillings–Mack检验，显著后采用带Holm校正的成对Wilcoxon符号秩检验。发现数另外用带$\log(\text{resource\_count})$暴露量偏置的负二项GEE建模，以获得按资源计算的发生率比；模型与人工分布使用Mann–Whitney $U$检验，结构分布使用两样本Kolmogorov–Smirnov检验。

<div class="method-step__io" markdown="1">

**输入**：每个制品的总发现数、声明资源数、复杂度分层、模型配置和人工来源标签。<br>
**输出**：规模匹配后的模型—人工安全差距、模型间显著性比较、复杂度交互效应，以及推理模式对漏洞密度的影响估计。

</div>

**直观理解**：不能直接拿一个两资源模板和一个五十资源架构比漏洞总数，因为后者天然有更多被检查的地方。该步骤先把“代码有多大”控制住，再判断同等规模下谁更容易产生安全问题。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 漏洞密度

$$
\mathrm{vulnerability\ density}_i=\frac{F_i}{R_i}
$$

**符号说明**

- $F_i$：第$i$个IaC制品由Checkov、Trivy和KICS报告的漏洞发现总数。
- $R_i$：第$i$个IaC制品通过AST解析得到的声明资源数量。
- $i$：IaC制品的索引。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把发现数除以资源数，得到每个声明资源对应的平均发现数。它不能消除所有规则或解析偏差，但能避免大模板仅因资源更多而在绝对数量上占劣势。<br>
**原文位置**：III-F Metrics

</div>

</div>

<div class="equation-block" markdown="1">

#### 带资源暴露量偏置的负二项计数模型

$$
\log\!\left(\mathbb{E}[Y_i\mid X_i]\right)=X_i\beta+\log(R_i)
$$

**符号说明**

- $Y_i$：第$i$个IaC制品的漏洞发现计数。
- $X_i$：第$i$个制品的解释变量设计矩阵，包含模型配置、复杂度及其交互项等因素。
- $\beta$：待估计的回归系数；系数指数化后可解释为发生率比。
- $R_i$：第$i$个制品的声明资源数量，作为暴露量。

<div class="equation-explanation" markdown="1">

**直观理解**：模型先预测漏洞发现的期望数量，再显式考虑一个制品包含多少资源。这样，配置系数表示在资源机会量相近时的漏洞发生率差异，而不是单纯表示谁生成了更多代码；负二项分布用于处理发现数明显过度离散的情况。<br>
**原文位置**：III-G Statistical procedure；IV-I Rate model；V-D Absolute counts mislead

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文不是训练新模型的方法论文，而是对现有模型进行受控生成和安全评估；因此没有需要优化的模型参数、损失函数或训练目标。研究中的“推理模式”是推理阶段的API配置，提示式思维链是系统提示后缀，均不构成本文训练过程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 功能优先、无安全提示的生成协议**

系统提示固定角色和输出格式，用户提示仅包含目标格式与功能场景；不加入安全术语、硬化要求、合规要求或具体控制。模型配置覆盖四家供应商、开放与闭源模型，以及标准生成、提示式链式思考和供应商扩展思考。

> 直观理解：该模块把安全要求从题目中拿掉，测试模型自身的基础设施默认习惯，而不是测试模型能否照着安全清单执行。

**2. 多引擎扫描与人工锚定语料库**

生成制品和634份人类模板均经过相同的格式验证和Checkov、Trivy、KICS扫描；安全结果以三引擎发现总数表示，资源分母由AST解析得到。人工语料库提供规模匹配的参考分布，而不是仅报告模型的原始漏洞计数。

> 直观理解：人工基线像一把现实中的尺子：只有知道工程师写同类代码通常有多少问题，才能判断模型是更差、相近还是更好。多个扫描器则降低单一工具规则遗漏造成的结论依赖。

**3. 暴露量校正与不完整区组统计**

主要比较量为按声明资源数归一化的漏洞密度；计数模型使用负二项GEE并以$\log(\text{resource\_count})$作为暴露量偏置，以处理观测到的方差均值比为130.0的过度离散。由于12种配置并非每个场景都有完整结果，模型总体差异采用Skillings–Mack，而不是要求完整区组的Friedman检验。

> 直观理解：资源数是漏洞机会的粗略计数器，暴露量偏置让模型比较关注“每个资源的风险率”。Skillings–Mack允许某些模型在某些场景缺席，避免为了使用传统检验而把所有有缺失的场景全部删除。

**训练与推理**

本文仅执行推理。对每个场景，系统生成一条固定系统提示，加入目标格式和功能需求的用户提示，并分别调用12种模型配置；请求保持无状态，不使用少样本示例、检索或会话历史。标准生成与提示式思维链使用温度$0.2$，扩展思考使用供应商强制的默认温度$1.0$；记录输出及推理令牌，丢弃达到上限的截断结果，临时失败则指数退避重试。生成后进行格式验证和三引擎扫描，再将结果与人工模板的同工具链结果按资源数量分层比较。扩展思考与标准生成的对照属于固定基础模型内的配对推理实验，提示式思维链用于区分“要求模型逐步思考”和真正调用供应商扩展推理机制的效果。

**复现信息**

复现实验所必需的设计包括：100个场景按简单任务60个、复杂任务40个分层；覆盖四个平台和四类IaC格式；模型请求要求单个代码块且不提安全；四个复杂场景因128k输出上限无法完成并作为缺失处理；1196份生成制品全部由Checkov、Trivy和KICS扫描；人工参考库包含634份模板，且使用相同扫描器、配置和覆盖核验。统计解释时必须保留资源数分母的定义，因为简单生成约声明3个资源、复杂生成约50个资源，而人工模板平均约5.31个资源；直接比较绝对发现数或未匹配密度会混入规模效应。扩展思考的令牌预算还与温度同时变化，这是无法消除的混杂因素，论文将其列为限制。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GenIaC-SecBench模型生成集：包含100个按架构复杂度分层的部署场景，评估12种模型配置；理论规模为1,200个制品，实际生成1,196个，用于比较模型配置、任务复杂度和推理方式。
- 人类基线集：634个由人类编写的IaC模板，使用与模型制品相同的扫描工具链，并按声明资源数量提供规模匹配基线，用于回答模型是否确实劣于工程师。
- 三引擎扫描结果集：对模型和人类IaC进行Checkov、KICS和Trivy独立扫描；模型制品共产生38,803条发现，用于计算漏洞密度及进行稳健性比较。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**漏洞密度**

将扫描发现按IaC制品规模归一化，核心比较同时考虑漏洞数量和声明资源数量；论文还按资源数量进行匹配。 （越低越好，因为表示每单位IaC规模对应的安全问题更少；未匹配规模时，低密度也可能只是制品更大。）

</div>
<div class="metric-item" markdown="1">

**Spearman秩相关系数**

衡量制品大小与漏洞密度之间的单调关系，不要求变量服从正态分布。 （不存在普遍的高低优劣；绝对值越大表示关系越强，负值表示一个变量增大时另一个通常减小。）

</div>
<div class="metric-item" markdown="1">

**Skillings-Mack统计量**

用于不完整区组或存在缺失观测时的秩检验，论文以它替代现实基准设计中不可行的完整案例Friedman检验。 （它不是安全质量分数，不能按高低直接解释为更安全；应结合显著性检验判断配置间差异。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 模型制品覆盖率与扫描规模

<div class="result-value" markdown="1">

100个场景中实际获得1,196个模型IaC制品，覆盖理论规模的99.7%；三种扫描器共报告38,803条发现，其中Checkov报告14,017条、KICS报告14,033条、Trivy报告10,753条。

</div>

该结果说明基准的大多数模型—场景组合都能被评估，扫描结果规模足以支持分布和配置比较。但它不表示这些发现都是彼此独立的漏洞，也不表示扫描器报告的每一项都已人工确认；四个无法生成的复杂场景可能造成选择性缺失。

<div class="result-source" markdown="1">

来源：IV-A Corpus

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Generation yielded 1,196 of a possible 1,200 artifacts (99.7%). Scanning produced 38,803 findings (Checkov 14,017; KICS 14,033; Trivy 10,753).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 按资源规模匹配的人类基线比较

<div class="result-value" markdown="1">

按声明资源数量匹配后，所有模型配置的漏洞密度约为人类基线的3.21至3.87倍；在单资源任务中差距为4.9倍，而在至少20个资源的任务中缩小到1.4倍。论文还报告漏洞密度与制品大小呈显著负相关，Spearman $ρ=-0.55$、$p<10^{-77}$。

</div>

作者的核心解释是：模型制品相对人类模板仍更不安全，但差距会随任务规模增大而缩小；如果直接比较未匹配的原始漏洞数，较大的制品可能因单位规模漏洞更少而看起来更安全。因此该结果支持“规模匹配是必要的”，但不能证明模型在所有架构或真实部署条件下都只差固定倍数。

<div class="result-source" markdown="1">

来源：Abstract；资源规模匹配结果

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

When matched on declared-resource count, all model configurations fall within 3.21x--3.87x the human vulnerability density, with the gap widening for simpler tasks (4.9x at one resource, 1.4x at twenty or more).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 复杂度分层下的模型配置表现

<div class="result-value" markdown="1">

表II显示各配置在简单场景的漏洞密度均值通常高于复杂场景；例如claude-opus-4-6为简单场景12.12、复杂场景4.38，gpt-5-thinking为8.44和5.65，mistral为10.98和8.49。中位数普遍低于均值，表明发现分布明显右偏且含大量零值。

</div>

这说明简单任务并不自动更安全：较小的配置可能更容易暴露高密度问题，或其漏洞被规模归一化后更突出。均值高于中位数意味着少数异常高漏洞制品会显著拉高平均值，所以只看均值可能夸大典型制品的风险；表II描述的是扫描发现密度，不等于经过人工验证的真实漏洞率。

<div class="result-source" markdown="1">

来源：IV-B Descriptive statistics；Table II

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Medians are markedly lower than means throughout—the distribution is heavily right-skewed and zero-inflated, which is why all inferential tests below are rank-based or explicitly negative-binomial.

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

- 人类编写的IaC模板：最关键的外部基线，因为仅与其他模型比较只能说明模型之间的相对差异，不能判断模型是否达到工程师水平。
- 标准生成：不额外要求显式推理，作为评估链式思考和扩展思考的生成基准。
- 提示工程链式思考：通过提示要求模型展示或执行链式思考，用于检验普通提示是否能改善安全性。
- 厂商扩展思考API：调用模型供应商提供的扩展推理机制，用于与提示工程链式思考区分真正的额外推理预算或专用推理机制。

**实验想回答的问题**

- 在按声明资源数量匹配后，模型生成的基础设施即代码（IaC）相对于人类模板的漏洞密度有多大差异；若不匹配规模，比较是否会把制品大小误判为安全性差异？
- 标准生成、提示工程链式思考和厂商扩展思考是否会产生不同的安全结果；可部署性与漏洞数量是否相关？

**实验实现**

每个场景要求模型生成可部署的IaC，再由Checkov、KICS和Trivy独立扫描并汇总发现；论文按简单与复杂场景报告均值和中位数，并指出分布右偏且含大量零值，因此推断检验采用秩方法或显式负二项模型。模型结果与634个人类模板使用相同扫描工具链，关键比较按声明资源数量匹配，以避免制品大小造成混淆。实验还区分标准生成、提示工程链式思考和厂商扩展思考，并记录输出预算中的思考令牌占比。四个复杂场景未能在模型最大输出窗口内生成，即使窗口达到128k令牌；这既是数据缺失，也反映复杂架构提示可能诱发超长输出。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 标准生成、提示工程链式思考与厂商扩展思考 | 厂商扩展思考相较提示工程链式思考使漏洞结果下降12.0%，且差异显著（$p=0.0013$）；提示工程链式思考相较标准生成仅下降1.3%，统计上不显著。 | 该对照隔离了“仅在提示中要求思考”和“使用供应商专门扩展推理机制”的差异。结果支持扩展思考可能带来有限但可检测的安全改善，却不支持普通链式思考提示本身能稳定降低漏洞；它也没有证明扩展思考能达到人类基线。 | Abstract；推理方式比较<br><span class="experiment-evidence">Vendor extended thinking significantly outperforms prompted chain-of-thought ($-12.0\%$, $p = 0.0013$), while prompted chain-of-thought is indistinguishable from standard generation ($-1.3\%$, n.s.).</span> |
| 扩展思考的令牌预算消融 | 令牌记录显示，扩展思考使用的令牌少于输出预算的1%。 | 这为扩展思考改善幅度有限提供了机制解释：额外思考并未占用很大的可见输出预算，因此其效果可能受推理规模约束。该观察是资源使用与效果的关联证据，不足以单独证明“令牌占比低”就是性能提升受限的唯一原因。 | Abstract；Token instrumentation<br><span class="experiment-evidence">Token instrumentation shows extended thinking uses under 1\% of the output budget, explaining its bounded effect.</span> |

**定性案例**

- 可部署性与漏洞并不相关：论文报告$r=0.158$、$p=0.625$。这意味着“能够部署”不能作为“更安全”的替代指标；一个制品可以语法正确、能够部署，却仍包含大量扫描器发现。该结果也提醒评估应将部署成功和安全性作为两个不同维度，而不能用前者推断后者。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：核心贡献是建立带有人类安全基线的LLM生成基础设施代码安全评测基准，同时评估并分析生成代码的漏洞风险。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`a6a1e4ea2e6f2f5f8f881cc1f27c65329bee7babcf04aaa8a2ea0ee70e741586`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
