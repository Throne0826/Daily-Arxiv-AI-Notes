---
title: "[论文解读] A Task-Centric Ontology and Deterministic Domain Rules as a Verifiable Core for AI-Assisted Chemistry Problem Solving"
description: "[arXiv 2608.26164][LLM 其他] 本文探索以面向限定题集的任务中心本体和确定性化学规则构成可检查、可约束的符号推理核心，使未来的大语言模型主要负责自然语言与规范化任务表示之间的转换，而非独自承担化学推理。"
arxiv_id: "2608.26164"
announcement_date: "2026-08-28"
primary_category: "llm_nlp"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:38:54.142994+00:00"
source_sha256: "95ca47956efa27fafb496098d1d4a622ab52d54fe26756395acc3bcd8c245b01"
tags:
  - "LLM 其他"
  - "LLM Reasoning"
  - "任务中心本体"
  - "神经—符号人工智能"
  - "化学问题求解"
  - "确定性规则"
  - "知识表示"
  - "可解释人工智能"
  - "大语言模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 其他 · arXiv 2608.26164</p>

# A Task-Centric Ontology and Deterministic Domain Rules as a Verifiable Core for AI-Assisted Chemistry Problem Solving

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Ibrokhimsho Abduchaborov</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26164v1) · [PDF 下载](https://arxiv.org/pdf/2608.26164v1) · **关键词** 任务中心本体, 神经—符号人工智能, 化学问题求解, 确定性规则, 知识表示, 可解释人工智能, 大语言模型<br>


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

本文探索以面向限定题集的任务中心本体和确定性化学规则构成可检查、可约束的符号推理核心，使未来的大语言模型主要负责自然语言与规范化任务表示之间的转换，而非独自承担化学推理。

**不用术语来说**：大语言模型能够读懂化学题并生成答案，但其推理过程往往难以逐步检查：系统可能在看似简单的问题上给出不一致或过度自信的回答，也难以说明用了哪条化学规则。学校化学等要求答案和中间步骤可核验的场景，因此需要一种把题目所需知识、适用条件和求解步骤明确写出并稳定执行的核心，而不是把全部判断隐藏在语言模型内部。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出任务中心本体工程方法：不追求建立覆盖整个化学领域的通用本体，而是从一个边界明确的问题集合所要求的概念、属性、关系和可执行过程反向确定本体内容。
- 构建并审计一个轻量本体与确定性 Python 规则结合的概念验证系统，同时明确区分可复用的本体驱动规则与尚不能一般化的专家编码回退方案，并将语言模型翻译层和令牌效率留作后续验证。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于化学知识表示与神经—符号人工智能的交叉领域。大语言模型能够理解自然语言化学题并生成回答，但其推理过程可能不一致、过度自信，且难以检查某条规则为何适用；符号系统则把领域概念、事实、约束和求解步骤显式表示，使中间过程与答案能够复核。ChemOntoRule研究的不是通用化学智能，而是面向有限的中学化学问题族，构建由任务中心本体和确定性规则组成的可验证推理核心；未来的大语言模型仅负责把用户问题翻译成受约束的任务表示，并将符号结果表述为自然语言，该语言接口在当前论文中尚未接受评测。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**任务中心本体**

本体是对领域中的类别、属性、个体及其关系进行机器可读表示的知识结构。所谓“任务中心”，是指只依据目标题集的能力需求纳入必要知识，而不追求建立覆盖全部化学的通用本体。

</div>
<div class="concept-item" markdown="1">

**确定性规则引擎**

规则引擎读取结构化事实，并按预先编写的条件和程序执行计算或分类；相同输入与相同规则会产生相同输出。本文使用外部 Python 规则处理电子结构、周期趋势、氧化态以及氧化物和氢化物性质等问题。

</div>
<div class="concept-item" markdown="1">

**神经—符号架构**

该架构把神经模型灵活的语言理解能力与符号系统透明、可约束的推理能力结合起来。本文设想大语言模型承担自然语言与规范化任务框架之间的翻译，而把可规则化的化学推理交给本体关联程序。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究问题是：对于边界明确的一组学校层级化学题，任务中心本体与确定性领域规则能否构成一个可检查、可约束并可验证的求解核心。系统的概念性输入是由自然语言题目转换而来的规范化任务框架，其中包含题型、相关化学实体、已知属性及所求目标；当前研究实际评测的是该结构化表示之后的符号核心，而非自然语言翻译层。核心利用 JSON 与 RDF/Turtle 中的本体事实以及确定性 Python 规则生成答案；尚未被一般规则覆盖的题型由独立的专家编码回退程序处理。输出包括求解答案以及可供检查的规则执行依据。其关键假设是目标问题空间已经限定，并可通过检查题目族来识别所需实体、属性和程序；由于同一题集既参与本体构建又用于评测，论文结果只反映已实现范围内的覆盖度与内部一致性，不能视为对新题的独立泛化能力。结构约束验证也不等同于化学答案正确：前者检查知识图是否符合显式模式，后者仍需依据参考答案和错误分析判断。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **KnowTD**: KnowTD将热力学本体与推理器结合，用于选择方程并生成可解释的入门热力学解答，是本文最直接的本体驱动科学求解先例；ChemOntoRule则转向多个学校化学问题族，并强调任务中心建模、确定性外部规则和专家回退之间的边界。
- **ChemBench**: ChemBench通过大规模化学问答评测显示语言模型虽有较强平均表现，仍会出现基础错误和过度自信，从而说明仅依赖生成模型难以满足可验证推理需求。本文不再以比较大语言模型能力为主要目标，而是评测未来语言接口背后的确定性符号核心。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在辅助化学解题中，用户输入通常是自由形式的自然语言，而可靠求解又要求系统明确识别题型、调用适用的领域规则并输出可复核结果。若让大语言模型同时承担语言理解和化学推理，其内部步骤、规则适用性及最终答案都难以检查和约束，这使它不适合作为需要可解释性与可靠性的唯一推理来源。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **端到端大语言模型化学问答**：模型直接读取自然语言题目，依靠参数中学习到的化学知识生成推理文本和答案；其优势是语言适应性强，但知识调用和推理过程主要位于不可直接审计的模型内部。
- **本体、外部规则引擎与神经符号系统**：本体以机器可读形式表示类别、属性、个体和公理，外部规则引擎依据与本体关联的事实执行计算或分类；神经符号架构进一步让神经模型处理灵活语言，让符号模块负责透明、可控的领域推理。文中以 KnowTD 为例说明本体可与推理器结合，用于选择热力学方程并生成可解释解答。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单独依赖大语言模型会带来不一致、过度自信以及基础题失误；更关键的是，中间步骤和规则适用条件难以检查，因此即使答案看似合理，也缺少可验证的推理依据。
- 通用本体或已有领域本体方案并未直接回答一个更实际的工程问题：对于边界明确的学校化学题集，应该收录哪些知识、如何把知识连接到可执行程序，以及如何诚实地区分可复用规则与针对个别题型硬编码的处理。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有思路表明语言模型适合处理自然语言、本体与规则适合提供透明推理，但两者之间仍缺少一个经过实际题集审计的、范围受控的化学符号核心：它应由任务能力需求驱动，能够把规范化题目映射到明确规则，并分别报告一般规则的覆盖范围与专家回退的作用。本文只填补这一概念验证层面的空缺，并不解决独立泛化、完整开放式化学推理或受控语言模型比较。

</div>
<div markdown="1"><span>核心问题</span>

一个依据限定学校化学问题集合构建的任务中心本体，配合确定性领域规则，能否形成未来 AI 辅助化学解题所需的可验证核心，并在明确区分通用规则与任务特定回退的前提下表现出足够的内部覆盖和一致性？

</div>
<div markdown="1"><span>作者直觉</span>

自然语言的表达方式很多，但同类化学题通常可归约为少量结构化要素，例如所问属性、涉及对象和需要执行的规则。若先把题目翻译为受约束的任务框架，再由显式程序完成电子结构、周期趋势、氧化态或化合物性质等判断，系统就能记录调用了什么知识以及怎样得到结果。任务中心设计还避免一开始构建“完整化学世界模型”：只实现当前题集真正需要的概念与过程，因此更容易审计；暂时不能抽象为通用规则的题型则单独回退，而不伪装成本体推理。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ChemOntoRule 是一个“任务中心 ontology（本体）+ 外部确定性规则引擎”的符号求解核心。系统先把题目整理为规范化任务框架，识别任务家族、化学实体、约束或目标属性及输出格式；随后查询轻量本体提供的元素与关系信息，并把任务路由到可复用的 Python 规则或尚未泛化的专家编码回退程序；最后输出答案、可检查的推理轨迹、方法标签与结构验证状态。当前实验使用受约束的确定性解析器处理既定题目格式，论文设想的语言模型翻译器尚未实现或评测。
技术上，本体负责陈述“有哪些对象、属性和关系”，规则引擎负责执行电子结构、周期趋势、氧化态、氧化物与氢化物等计算，而验证器只检查答案是否满足格式约束。通俗地说，本体类似一本结构化化学资料册，规则引擎像按明确步骤工作的解题程序，专家回退则像尚未整理成通用公式的专题答案；这种分工使规则来源和执行过程可追踪，但不能把格式通过等同于化学结论正确。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 题目接收与条件规范化

当前实现通过确定性条件解析，将题目整理为包含任务家族、已识别实体、约束或请求属性、输出模式的规范化任务框架；论文设想未来由参数化翻译器 $T_{\theta}$ 将自然语言查询 $q$ 映射到该框架，但本研究未评测这一层。

<div class="method-step__io" markdown="1">

**输入**：学校化学题目及其受约束的任务格式。<br>
**输出**：规范化任务框架 $z=(f,E,K,o)$，其中 $f$ 是任务家族，$E$ 是实体集合，$K$ 是约束或目标属性，$o$ 是输出模式。

</div>

**直观理解**：这一步把自然语言题目改写成程序能稳定读取的“表单”。当前系统主要读取格式较固定的表单，而不是证明语言模型能够可靠理解任意问法。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 求解器路由与适用性判断

系统根据任务家族与规则适用条件选择求解路径：已被一般化表示的问题进入 $\text{ontology\_rule}$ 路径，规则库未覆盖的问题进入 $\text{manual\_expert}$ 专家编码回退路径。两类路径使用不同方法标签，避免把针对特定任务的代码误称为本体推理。

<div class="method-step__io" markdown="1">

**输入**：规范化任务框架 $z$ 以及已注册的任务模板和规则。<br>
**输出**：选定的通用规则或专家回退程序，以及对应的方法标签。

</div>

**直观理解**：它相当于先判断题型，再把题目交给合适的解题模块。若还没有通用解法，就明确标为专门处理，而不是假装系统已经学会了一条普适化学规律。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 本体查询与确定性规则执行

规则引擎查询元素的周期、族、区块、外层电子结构、氧化态、成氧化物或挥发性氢化物能力及趋势分数，再执行电子排布、价电子、未成对电子、稳定离子电子数、氧化态范围、化学式可行性或趋势排序等显式程序。每条适用规则产生结果 $y_j$ 和解释片段 $\tau_j$。

<div class="method-step__io" markdown="1">

**输入**：任务框架、所选规则，以及本体 $\mathcal{O}$ 中的类别、属性、个体和属性值。<br>
**输出**：候选答案、所关联的本体概念及可追踪的中间解释。

</div>

**直观理解**：资料由本体提供，计算由 Python 规则完成；例如系统先查某元素的结构信息，再按写明的步骤计算或排序。因此结论不是来自不可见的自由生成过程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 答案生成与分层验证

系统生成最终答案 $a$、推理轨迹 $\tau$ 和验证状态 $v$，并记录关联概念、简短解答及方法标签。内置验证仅检查答案是否存在、选择是否非空、选择数量是否合理以及选项索引是否越界；化学正确性另以规范化输出是否匹配人工验证参考答案来衡量。

<div class="method-step__io" markdown="1">

**输入**：规则执行结果、目标输出模式与选项约束。<br>
**输出**：结构化答案记录，包括答案、轨迹、验证状态、方法标签和关联概念。

</div>

**直观理解**：格式验证只能发现“没填答案”或“选项编号越界”一类错误，不能证明化学推理正确。真正的结果评估仍需把答案与人工参考答案对照。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 本体结构与可执行规则

$$
\mathcal{O}=(\mathcal{C},\mathcal{P},\mathcal{I},\mathcal{A}),\qquad r_j:\phi_j(z,\mathcal{O})\rightarrow(y_j,\tau_j)
$$

**符号说明**

- $\mathcal{O}$：任务中心化学本体。
- $\mathcal{C}$：本体中的类别集合。
- $\mathcal{P}$：属性与关系集合。
- $\mathcal{I}$：元素等个体的集合。
- $\mathcal{A}$：显式断言或由规则推导出的属性值集合。
- $r_j$：第 j 条可执行领域规则。
- $\phi_j$：第 j 条规则的适用性谓词，用于判断该规则能否处理当前任务。
- $z$：规范化任务框架。
- $y_j$：第 j 条规则计算出的结果。
- $\tau_j$：第 j 条规则生成的推理轨迹或解释片段。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分规定知识库由类别、关系、个体和属性值组成；第二部分规定规则只有在适用条件成立时，才依据任务框架和本体产生结果及解释。它表达了论文的核心分工：本体提供结构化上下文，外部规则提供可执行推理。<br>
**原文位置**：第 5.2 节，公式（1）和公式（2）

</div>

</div>

<div class="equation-block" markdown="1">

#### 任务翻译与符号核心求解接口

$$
z=T_{\theta}(q)=(f,E,K,o),\qquad S(z,\mathcal{O},\mathcal{R})\rightarrow(a,\tau,v)
$$

**符号说明**

- $q$：用户提交的自然语言化学问题。
- $T_{\theta}$：论文设想的参数化 AI 翻译器；当前研究未对其进行评测。
- $z$：供符号核心使用的规范化任务框架。
- $f$：任务家族或路由类别。
- $E$：从问题中识别出的化学实体。
- $K$：题目给出的约束或要求计算、分类、比较的属性。
- $o$：期望的答案输出模式。
- $S$：确定性符号求解核心。
- $\mathcal{O}$：任务中心本体。
- $\mathcal{R}$：可用的确定性领域规则集合。
- $a$：最终答案。
- $\tau$：完整或汇总后的求解轨迹。
- $v$：输出验证状态。

<div class="equation-explanation" markdown="1">

**直观理解**：理想架构先让翻译器把用户问题变成严格字段，再让确定性核心查本体、选规则并返回答案、轨迹和验证结果。当前论文只检验后半段的符号核心，并以受约束的确定性解析替代 $T_{\theta}$，所以这些公式定义的是未来接口，不构成语言模型理解能力的实验结果。<br>
**原文位置**：第 5.2 节，公式（3）和公式（4）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文没有训练神经模型，也没有给出损失函数、参数优化或梯度学习过程；本体和规则由任务需求驱动地人工设计，专家回退同样由人工编码。符号核心 $S$ 的行为来自显式知识与确定性程序，而不是从 300 道题上拟合参数。虽然未来翻译器记为 $T_{\theta}$，原文没有说明其训练目标或训练数据，并明确指出当前研究未评测该翻译层。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 任务中心轻量本体**

本体不是试图完整表示化学，而是从限定题集的能力问题出发，只建模解题所需的实体、属性、关系、适用条件和输出模式。实现包含 Element、PeriodicTrend、OxidationStateRule 和 ManualReactionPattern 四个声明类，覆盖 52 个元素及八组任务相关关系，并以 JSON 和 RDF/Turtle 序列化；可执行逻辑主要不在 OWL 公理中。

> 直观理解：这种设计优先保证“当前题目需要什么就明确表示什么”，因此规模较小且便于检查。但它的覆盖边界由既定任务空间决定，不能据此认为系统拥有完整的化学知识。

**2. 外部确定性领域规则引擎**

Python 引擎实现电子排布与亚层计数、外层和价电子计算、未成对电子计算、稳定离子电子数、最高与最低氧化态、常见氧化物化学式可行性、周期趋势启发式评分及模板化排序。规则以适用性谓词连接任务框架和本体上下文，并返回结果与解释轨迹，因此该系统应称为“本体支撑的外部规则引擎”，而非纯 OWL 推理器。

> 直观理解：本体保存事实，程序负责按确定步骤算答案。优点是同样输入通常得到同样输出，且可以检查用了哪条规则；局限是程序未编码的题型不会自动获得解法。

**3. 专家编码回退与验证记录**

当一般规则库不能覆盖某个任务家族时，系统调用与特定任务或题型绑定的专家代码，并标记为 $\text{manual\_expert}$；只有独立表示其实体、适用条件、变换和验证规则后，才能升级为通用规则。每个任务记录六个逻辑阶段，并将结构有效性与参考答案匹配分开。

> 直观理解：回退机制让原型系统能处理更多已知题目，但它也揭示了尚未一般化的覆盖缺口。单独标记回退结果，可避免把“为这道题写过代码”错误解释为“系统掌握了可迁移规则”。

**训练与推理**

本方法没有传统意义上的训练阶段。开发阶段以 300 道人工编写并人工验证的题目同时提取需求和检查实现：开发者按反复出现的题型确定所需实体、目标关系、化学属性、规则适用条件、输出格式及结构检查，再建立轻量本体、编写通用 Python 规则，并为未覆盖家族加入专家回退。由于同一题集参与了本体构建与评估，这一过程更接近范围限定的知识工程，而非独立训练集上的统计学习。
运行时，题目依次经过接收、条件解析、求解器路由、本体上下文查询、答案生成和结果验证。当前解析器面向给定任务格式；若通用规则适用，则输出 $\text{ontology\_rule}$，否则调用 $\text{manual\_expert}$。系统保存答案、关联概念、简短轨迹、方法标签和验证状态；未来才计划让语言模型把开放式自然语言转换为同一任务框架。

**复现信息**

公平解释结果所需的实现事实包括：知识层提供 JSON 与 RDF/Turtle 两种序列化，工作本体含 4 个声明类、8 组任务相关关系、52 个元素个体、约 1,029 个 RDF 三元组和 17 个数据类型属性；主要推理逻辑位于外部 Python 引擎，而非 OWL、SWRL 或 SHACL 内部。系统为每题记录 6 个逻辑阶段及事件日志，但仪表板中的阶段时长是为可视化生成的数值，不是实际墙钟时间，因此不能用于推断延迟、吞吐量或推理成本。
此外，结构验证只覆盖答案存在性、非空选择、合理选择长度及选项索引范围，不能独立确认化学正确性。实现中的趋势判断包含启发式分数，专家回退则是明确隔离的任务特定代码；复现时必须保留这两者与一般本体规则的边界，否则会高估符号规则的实际覆盖范围。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 一个包含300道人类编写并经人工验证的学校层次化学问题集合。该集合同时用于本体与规则开发和最终评估，没有独立训练集、验证集或冻结测试集；因此它适合检查已实现题型的覆盖率与内部一致性，不适合估计对未见题目、不同表述或新实体的泛化能力。题目按实现层面的任务族统计，包括原子结构、周期趋势、氧化态、专家反应、有机化学、扩展方程和计算题。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**规则覆盖率（Rule Coverage）**

定义为$\mathrm{Coverage}_{\mathrm{rules}}=N_{\mathrm{ontology\_rule}}/N_{\mathrm{all}}$，其中$N_{\mathrm{ontology\_rule}}$是由本体驱动规则引擎处理的题数，$N_{\mathrm{all}}$是全部题数。它衡量多少任务无需进入专家编码回退即可由可复用规则层处理，不直接衡量答案正确性。 （越高越好，因为更高的覆盖率意味着更多题型已被统一的本体概念和确定性规则吸收；但若通过过度宽泛或错误的规则提高覆盖率，并不代表化学推理质量提高。）

</div>
<div class="metric-item" markdown="1">

**归一化精确匹配率（Match Rate）**

定义为$\mathrm{MatchRate}=N_{\mathrm{matched}}/N_{\mathrm{evaluated}}$，其中$N_{\mathrm{matched}}$为归一化后与参考答案完全相同的输出数，$N_{\mathrm{evaluated}}$为被评估题数。该指标用于完整系统、规则子集、回退子集及各任务族。 （越高越好，因为它表示更多最终答案与人工参考答案一致；但精确匹配不能单独证明推理链正确，也可能把数值容差、等价表达和参考答案本身的问题混在一起。）

</div>
<div class="metric-item" markdown="1">

**Wilson 95%置信区间**

论文为观察到的匹配比例报告Wilson 95%区间，用于描述有限样本下比例估计的不确定性。由于评估集合参与过开发，这些区间没有校正设计集依赖。 （不以单纯更高或更低判断优劣；在中心比例相近时，更窄的区间通常表示描述性估计更稳定，但这里不能将其解释为对独立总体或未见任务泛化率的置信界。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 本体驱动规则层的任务覆盖

<div class="result-value" markdown="1">

规则引擎处理了300题中的269题，规则覆盖率为89.67%；其余31题由任务特定的专家编码回退处理。

</div>

这说明多数已收录问题能够映射到统一的本体与可执行规则，而约一成题目仍依赖专门代码。覆盖率反映的是系统已实现哪些题型，不等同于答对率；又因为这批题参与了本体构建，该结果不能证明规则层对新题型也能达到相同覆盖。

<div class="result-source" markdown="1">

来源：第9.1节“Coverage and reference matching”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The ontology-driven rule engine covered 269 of 300 problems, corresponding to 89.67% rule coverage. The remaining 31 problems were processed by task-specific expert-coded fallbacks.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 完整系统及两条内部路由的参考答案匹配

<div class="result-value" markdown="1">

完整系统在300题中匹配296题，匹配率为98.67%；规则子集在269题中匹配266题，匹配率为98.88%；专家回退在31题中匹配30题，匹配率为96.77%。

</div>

作者据此主张该原型在当前开发集合上具有较高的实现一致性。规则子集和回退子集面对的是不同题目，而非同一批题上的公平对照，因此二者的匹配率差异不能直接归因于规则设计优于专家代码；这些数字更不能被解释为独立泛化性能。

<div class="result-source" markdown="1">

来源：第9.1节及表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The complete system matched 296 of 300 reference answers (98.67%). The ontology-rule subset matched 266 of 269 references (98.88%), while the fallback subset matched 30 of 31 (96.77%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 不同实现级任务族的匹配情况

<div class="result-value" markdown="1">

氧化态、专家反应、有机化学和扩展方程任务均达到100%参考匹配；原子结构为100/102，周期趋势为100/101，而计算题仅为3/4。四个错误中，三个发生在一般本体规则任务族，一个发生在专家编码计算题。

</div>

分任务族结果用于定位系统薄弱环节：当前错误并非平均分布，而是集中在电子结构或周期性质规则的语义边界，以及一个专门计算过程。不过若只看计算题的75.00%会产生较大不确定性，因为该任务族仅有4题；若干任务族的100%也只能说明当前少量已知题全部匹配，不能证明相应化学领域已经被完整建模。

<div class="result-source" markdown="1">

来源：第9.2节“Results by task family”及表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

All oxidation-state, expert-reaction, organic, and extended-equation tasks matched the references. Three of the four mismatches occurred in general ontology-rule families, and one occurred in an expert-coded calculation.

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

- 一份预先存在的LLM生成答案文件仅用于描述性参照。该文件与全部参考答案匹配，但由于确切模型版本、完整提示词、解码参数、token数量、重复运行方案及潜在后处理历史均未保存，论文明确不把它视为受控基线，也不据此进行优越性或统计显著性比较。
- 专家编码回退路径可视为系统内部的对照路由：它处理尚未被通用本体规则表示的题型，用于区分可复用规则层的覆盖范围与针对特定任务直接编码的能力；但它不是独立外部方法，也不是随机化消融实验。

**实验想回答的问题**

- 在这组参与系统开发的校内化学题上，任务中心本体与确定性规则能够覆盖多少题目，并且完整系统、通用规则路径和专家回退路径分别能与人工参考答案匹配到什么程度？
- 未匹配案例集中暴露了哪些可复用表示或推理缺陷，从而说明后续应优先改进语义作用域、规则适用条件、领域启发式还是计算过程？

**实验实现**

系统依次运行全部300道题，并为每题保存路由、任务族、答案类型、概念数量、最终答案和解题轨迹。输出与人工参考答案经过归一化后做精确比较；系统首先尝试本体驱动的确定性规则，未被通用规则覆盖的题目转入任务特定的专家编码回退。论文按完整系统、两类路由和任务族报告匹配情况，并对四个不匹配案例逐一诊断。实验没有冻结独立测试集，也没有保留足以复现LLM比较的配置。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 四个不匹配案例揭示了四类工程缺陷：任务3129把“最外层有三个电子”误当成“失去三个电子后得到八电子稳定外层”，属于适用条件不完整；任务3149把所有已占据$s$、$p$亚层的电子总数与题目要求的最外层计数混淆，属于语义作用域缺失；任务3485用一般金属性趋势排序过渡金属还原性，说明粗粒度启发式不足，应引入电化学或课程级专门次序；任务314的专家计算给出与参考不一致的质量分数，说明逐题硬编码算术应替换为带方程检查和容差规则的通用化学计量程序。整体上，这些案例表明“数值属性存在”并不保证查询语义正确，属性还必须绑定到正确能级、条件和适用领域。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The contribution is a deterministic ontology-and-rule symbolic chemistry system, with an LLM mentioned only as a prospective interface.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`95ca47956efa27fafb496098d1d4a622ab52d54fe26756395acc3bcd8c245b01`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
