---
title: "[论文解读] Predicting Program Exit Code with LLMs and Programming Language Semantics"
description: "[arXiv 2609.00579][LLM Reasoning] 本文提出程序可执行性预测任务 PrEx，以简短的执行成功或语义错误判定，检验大语言模型究竟能否应用显式给出的编程语言语义，还是主要依赖预训练形成的代码模式先验。"
arxiv_id: "2609.00579"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:44:14.232551+00:00"
source_sha256: "f1fde37a6fd96068bb90cd098d2c3794ff75d99409fd6904ae820bcb3a71378d"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "LLM 其他"
  - "程序可执行性预测"
  - "大语言模型"
  - "程序语言语义"
  - "小步操作语义"
  - "K 框架"
  - "语义偏移"
  - "代码推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.00579</p>

# Predicting Program Exit Code with LLMs and Programming Language Semantics

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Lara Marinov, Aditya Thimmaiah, Jayanth Srinivasa, Junyi Jessy Li, Milos Gligoric</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: The University of Texas at Austin , Austin , USA；The University of Texas at Austin；Affiliation: Cisco Research , San Francisco , USA；Cisco Research</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00579v1) · [PDF 下载](https://arxiv.org/pdf/2609.00579v1) · **关键词** 程序可执行性预测, 大语言模型, 程序语言语义, 小步操作语义, K 框架, 语义偏移, 代码推理<br>
**代码**: [https://github.com/EngineeringSoftware/prex](https://github.com/EngineeringSoftware/prex)

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

本文提出程序可执行性预测任务 PrEx，以简短的执行成功或语义错误判定，检验大语言模型究竟能否应用显式给出的编程语言语义，还是主要依赖预训练形成的代码模式先验。

**不用术语来说**：大语言模型可能见过大量常见代码，因此能根据熟悉的形式猜出程序作用，却未必会像解释器一样逐步按照规则判断程序能否运行；当运算符含义被调换、关键词被陌生符号替代或程序结构变复杂时，这种“凭经验猜测”尤其容易失效。本文要区分模型是真的会遵循给定规则，还是只是在复现训练中学到的常规代码模式。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 PrEx，将语义理解压缩为基础的离散判断：给定程序及其形式语义，预测程序执行成功还是因语义错误停止，并在失败时指出被违反的规则；该设计避免长执行轨迹本身造成的输出负担，从而更直接地测量语义判断能力。
- 构造配对的有效与无效程序，并通过两种形式语义、两种语义偏移以及三类不同来源和复杂度的程序进行控制性评估，以区分模型遵循显式规则的能力与其对熟悉符号、代码形态和预训练先验的依赖。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于程序语言语义与大语言模型代码推理的交叉领域。既有代码执行预测通常要求模型在不真正运行程序的情况下推断输出、状态或执行轨迹，但这类结果可能来自训练语料中的代码模式，而非对语言规则的系统应用。本文因此研究一个更基础且可控的问题：当提示中明确给出形式语义时，模型能否据此判断程序是否可执行，尤其能否在运算符含义被交换或替换后抑制预训练形成的符号先验。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**操作语义**

操作语义用形式规则描述程序如何一步步改变执行状态，以及何时正常结束或因规则不适用而出错。本文同时采用细粒度的小步操作语义与粒度较粗的 K 框架重写语义，以检验模型能力是否依赖规则表达方式。

</div>
<div class="concept-item" markdown="1">

**程序可执行性预测（PrEx）**

PrEx 要求模型根据程序及其给定语义，判断执行会成功还是因语义错误而停止；若无效，还要指出被违反的规则。它只要求离散判定而非完整执行轨迹，从而减少长程轨迹生成对语义能力测量的干扰。

</div>
<div class="concept-item" markdown="1">

**语义偏移**

语义偏移刻意改变熟悉符号的含义，以区分模型是在使用提示中的规则还是依赖预训练先验。KeywordSwap 交换已有运算符的意义，KeywordObf 则用新颖的单 token 符号替换标准运算符和关键字。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入由一个 $C^*$ 程序和一套显式提供的形式语义组成，语义采用小步系统 $\mathbb{S}$ 或 K 框架 $\mathbb{K}$；测试还可施加 KeywordSwap 或 KeywordObf 语义偏移。模型输出程序能否成功执行的离散结论；若程序无效，还需识别其违反的语义规则。数据以有效程序为基础，通过语义感知变换构造配对的无效程序，错误类别包括循环外使用 break、循环外使用 continue、除零、模零和变量先使用后声明；程序来源分为 Human-Written、LLM-Translated 与 Fuzzer-Generated，三者平均长度和结构复杂度依次增加。该设置假定判断依据应是当前提示给出的规则，而不是模型对常规语言符号和常见代码结构的既有记忆。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$C^*$**

本文实验所使用的程序语言及其程序集合；有效程序继承自 PLSemanticsBench。

</div>
<div class="notation-item" markdown="1">

**$\mathbb{S}$**

小步操作语义形式化系统，每条推理规则表示一个原子计算步骤。

</div>
<div class="notation-item" markdown="1">

**$\mathbb{K}$**

K 框架语义形式化系统，以较粗粒度的重写规则变换程序配置。

</div>

</div>

**直接相关的工作**

- **PLSemanticsBench（Thimmaiah et al., 2026）**: 该基准通过 PredState、PredRule 和 PredTrace 分别测试最终变量状态预测、执行规则识别与完整轨迹生成，但任务包含复杂的多步输出，因而难以判断低性能究竟来自轨迹生成负担还是基础语义判断缺陷。PrEx 继承其有效 $C^*$ 程序，并把目标缩减为可执行性及违规规则判定，以建立更基础的能力基线。
- **REval（Chen et al., 2025a）**: REval 测量代码覆盖、程序状态、执行路径和最终输出等相互依赖的运行时行为，但使用熟悉的语言语义。PrEx 的输出更简单，却额外提供显式的 $\mathbb{S}$ 与 $\mathbb{K}$ 规则、配对的有效与无效程序以及两类语义偏移，因此更适合诊断模型究竟遵循给定规则还是预训练先验。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

代码生成、翻译和修复等软件工程应用要求模型理解代码在语言规则下会如何执行，而不只是识别表面模式。若模型遇到轻微的控制流变化、陌生程序结构或重新定义的运算符后仍按常规含义猜测，它就可能错误判断程序是否合法或能否执行；这意味着其表面上的编码能力不足以支撑需要可靠语义推理的场景。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于常规软件工程任务的代码能力评估**：通过代码生成、代码翻译、缺陷修复或代码总结等任务衡量模型表现。这些任务能够反映实用能力，但模型可能凭借训练中记忆的代码模板和统计关联完成任务，因而难以单独证明其掌握了编程语言语义。
- **PLSemanticsBench 的语义理解评估**：该基准通过预测最终变量状态 PredState、识别执行中使用的形式规则 PredRule，以及生成逐步执行轨迹 PredTrace 来考查语义理解，要求模型处理程序执行的中间过程和规则应用。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 常规代码任务把模式识别、训练数据记忆和语义推理混合在一起：模型即使给出正确答案，也可能只是识别了熟悉算法或符号，无法据此判断它是否真正应用了显式规则。
- PLSemanticsBench 的任务包含多步推导、规则说明和较长执行轨迹，而模型在这些复杂任务上普遍表现较低；因此，失败可能来自长输出与多步执行负担，也可能来自更根本的语义判断缺陷，现有结果无法清楚定位能力边界。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚缺少一个低输出负担、同时又能控制预训练先验的基础测试：它应将“能否作出语义判定”与“能否生成完整执行轨迹”分离，并通过改变熟悉符号的含义或移除其表面线索，直接观察模型是否服从题目给出的形式语义。与此同时，该测试还需覆盖不同语义形式、程序来源和结构复杂度，以判断这种能力是否能够泛化。

</div>
<div markdown="1"><span>核心问题</span>

当模型同时获得程序及其显式形式语义时，它能否系统地依据这些规则判断执行是否成功、失败时违反哪条规则；尤其在运算符含义被交换或关键词被陌生符号替代后，它是否仍能覆盖预训练先验，并在更复杂、不同来源的程序上保持这种能力？

</div>
<div markdown="1"><span>作者直觉</span>

把答案限制为可执行性与错误类型的离散判定，可以减少长轨迹生成带来的干扰，使错误更可能反映语义判断本身。再将每个有效程序与按特定语义错误生成的无效版本配对，并设置 KeywordSwap 和 KeywordObf：如果模型确实读取并应用规则，符号是否熟悉不应决定结论；如果性能随符号改义、线索消失或结构复杂度增加而明显下降，则更支持模型依赖预训练关联而非系统执行规则的解释。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PrEx（Program Executability Prediction）把“语言模型是否真正遵循给定编程语言语义”转化为一个可判定任务：输入包括小型命令式语言 C∗ 的 EBNF 语法、两种形式语义之一（小步操作语义 $\mathbb{S}$ 或 K-framework 语义 $\mathbb{K}$）以及待分析程序；模型输出程序能否执行。若程序有效，输出 `##success##`；若存在语义错误，输出 `##error##` 并指出被违反的规则。任务不要求生成代码，而要求模型将规则应用到具体程序状态，例如识别未声明变量、除零或循环外的 `break`。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建有效 C∗ 程序集合

将程序统一为 C∗ 语法，并组成 Human-Written、LLM-Translated 与 Fuzzer-Generated 三个数据划分；其中翻译程序通过 K-framework 成功执行测试进行过滤，模糊生成程序则采用深度受控、语义感知的文法生成。

<div class="method-step__io" markdown="1">

**输入**：人工题解、由 C++ 翻译得到的程序，以及语法制导模糊测试器生成的程序。<br>
**输出**：共 491 个语义有效的 C∗ 程序，三个划分分别含 162、165 和 164 个程序。

</div>

**直观理解**：三类程序分别测试模型面对人写代码、模型改写代码和长而结构化的自动生成代码时能否稳定使用语义规则，而不是只适应某一种代码风格。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成配对的语义无效程序

使用基于 ANTLR 的 parser-visitor 对每个有效程序分别施加五类语义感知变换：循环外插入 `break`、循环外插入 `continue`、制造除零、制造模零，以及使用未声明变量；每个变体只违反一个预定错误规则。

<div class="method-step__io" markdown="1">

**输入**：每个有效 C∗ 程序及其抽象语法结构。<br>
**输出**：每个有效程序对应五个错误类别的无效变体，共得到 2,455 个无效程序；连同有效程序，完整数据集含 2,946 个样本。

</div>

**直观理解**：这相当于从同一道“正确题”制作五个只改动一种错误的“错题”。有效与无效程序在来源、风格和复杂度上保持匹配，因此模型不能简单利用表面风格判断标签。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 配置形式语义与语义迁移条件

分别在原始语义、KeywordSwap 和 KeywordObf 条件下构造任务：KeywordSwap 交换已有运算符的语义，例如令 `+` 表示减法；KeywordObf 用模型可单 token 化的新符号替换常见关键字或运算符，并在规则中明确其含义。

<div class="method-step__io" markdown="1">

**输入**：C∗ 程序、完整语法，以及 $\mathbb{S}$ 或 $\mathbb{K}$ 形式化规则。<br>
**输出**：同一程序在不同形式语义表示和语义映射下的测试条件。

</div>

**直观理解**：如果模型只是凭预训练记忆认为 `+` 永远是加法，它会在语义迁移中失败；只有读取并执行当前提示中的规则，才能给出正确判断。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提示推理与结构化预测

让模型判断程序是否可执行；有效程序返回 `##success##`，无效程序返回 `##error##` 并报告对应的违规规则。对非推理模型同时测试直接回答和思维链（CoT）提示，后者仅额外要求模型给出推理过程。

<div class="method-step__io" markdown="1">

**输入**：一条由 C∗ EBNF 语法、选定形式语义规则和目标程序组成的完整提示。<br>
**输出**：二分类执行性预测，以及无效样本的错误规则归因。

</div>

**直观理解**：模型既要回答“程序会不会因语义错误而停止”，又要指出“是哪条正式规则说明它错了”，从而区分猜标签与按规则分析。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 小步语义中的除零错误规则

$$
\frac{\texttt{v2}=\texttt{0}}{\langle\texttt{v1 / v2},\sigma,\chi\rangle\to\langle\texttt{ERROR},\sigma,\chi\rangle}
$$

**符号说明**

- $\texttt{v1}$：除法表达式已经求值完成的左操作数。
- $\texttt{v2}$：除法表达式已经求值完成的右操作数。
- $\sigma$：当前程序状态，即变量到值的映射。
- $\chi$：执行所需的附加控制上下文；该规则中保持不变。
- $\to$：小步操作语义中的一次状态转移。
- $\texttt{ERROR}$：语义错误状态，进入后程序立即停止执行。

<div class="equation-explanation" markdown="1">

**直观理解**：当前除法的右操作数为零时，表达式不能产生普通整数结果，而是转移到错误状态。这是 PrEx 中“除零”无效样本对应的 $\mathbb{S}$ 规则，也说明模型必须结合运行时值而非只搜索 `/ 0` 的固定文本模式。<br>
**原文位置**：Section 3.2, Table 1, Rule 19

</div>

</div>

<div class="equation-block" markdown="1">

#### 小步语义中的未声明变量错误规则

$$
\frac{\sigma(\texttt{x})=\bot}{\langle\texttt{x},\sigma,\chi\rangle\to\langle\texttt{ERROR},\sigma,\chi\rangle}
$$

**符号说明**

- $\texttt{x}$：当前被求值的变量标识符。
- $\sigma(\texttt{x})$：在当前程序状态中查询变量的结果。
- $\bot$：变量在当前状态中没有绑定值，即尚未声明或不可用。
- $\sigma$：当前变量状态映射。
- $\chi$：执行的附加控制上下文。
- $\texttt{ERROR}$：导致程序停止的语义错误状态。

<div class="equation-explanation" markdown="1">

**直观理解**：若状态表中找不到变量 $x$ 的绑定，读取该变量便直接产生错误。该规则体现了任务所考察的状态跟踪能力：模型必须按语句顺序判断变量何时进入状态，而不能只检查变量名是否在程序任意位置出现过。<br>
**原文位置**：Section 3.2, Table 1, Rule 2

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该方法没有在 PrEx 数据上训练或微调被评估模型，也没有定义新的损失函数；它通过提示式推理评估现有开源代码语言模型。预测目标包含两个层次：首先判断执行性标签，其次在预测为错误时识别被违反的形式规则，因此规则归因是对语义理解的附加检验，而不是独立的梯度优化目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双形式语义表示**

$\mathbb{S}$ 使用 Gentzen 风格推理规则，将执行拆成细粒度原子转移；$\mathbb{K}$ 使用基于重写的较粗粒度规则，并隐式处理部分操作数归约。两者覆盖相同类型的正常执行与错误状态，但规则粒度和表述风格不同。

> 直观理解：同一个程序错误可以用“逐小步演算”或“较大块重写”描述。并列测试二者可判断模型的困难来自程序语义本身，还是来自某一种形式化写法。

**2. 语义迁移控制**

KeywordSwap 保留熟悉的表面符号，却重新分配其含义；KeywordObf 则去除熟悉的符号线索，并保证替代符号各自被分词为一个 token，以避免因多 token 符号额外增加提示长度或句法复杂度。

> 直观理解：前者测试模型能否压过“旧习惯”，后者测试没有熟悉外观时能否只靠规则办事。二者共同隔离预训练先验与提示内语义的影响。

**3. 语义感知的配对错误注入**

ANTLR parser-visitor 在程序结构上定位合法插入或替换位置，并为每个有效程序生成五个分别对应单一错误规则的变体。数据集中有效类占 491 个样本，每一错误类别也各占 491 个样本，即六种类别各占 16.7%。

> 直观理解：单错误设计使失败原因可追踪：若模型答错，可明确归因到某类语义规则，而不必处理一个程序同时含多个错误时的歧义。

**训练与推理**

数据准备阶段先保留 491 个可执行程序，再由五种确定错误类型的变换为每个程序生成五个单错误变体。推理时，每条样本独立与完整 C∗ 语法及一套语义规则共同放入上下文；实验分别切换 $\mathbb{S}$ 与 $\mathbb{K}$，并切换原始语义、KeywordSwap 和 KeywordObf。模型不执行参数更新，而是直接生成结构化标签；非推理模型还分别使用直接回答提示和要求解释过程的 CoT 提示，以检验显式推理要求是否改善规则应用。

**复现信息**

C∗ 是具有声明、赋值、算术与布尔表达式、`if-else`、`while`、`loop`、`halt`、`continue` 和 `break` 的小型 C 风格命令式语言。错误变换由 ANTLR parser-visitor 完成，以保证操作针对语法结构并使每个无效程序只触发一个目标错误；LLM-Translated 样本由 Qwen2.5-Coder 32B 从 C++ 翻译，并用 K-framework 执行公共测试过滤。程序规模在三个划分间差异显著：中位行数分别为 19、106 和 786，中位 token 数分别为 81、538 和 9,081；因此跨划分比较同时考察代码来源与复杂度，不能仅解释为风格变化。原始集合中的一个 Fuzzer-Generated 程序因完整提示约 37K token、超过所用 Qwen2.5-Coder 模型的 32K 上下文而被移除。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Human-Written：人工编写的程序划分，主要检验模型处理较短、较自然程序时的 PrEx 能力。表 6 报告该划分在两种语义形式体系与三种语义设置下的准确率；原文节选未明确报告独立程序数量，但称跨 6 种配置共评估 5,832 个程序实例。
- LLM-Translated：由大模型翻译得到的类 C 程序划分，用于检验模型能否处理表面上熟悉、但可能不满足所给 $C^*$ 语义的代码。它尤其能暴露模型是否因代码外观类似标准 C 而过度预测为可执行；结果见表 7。
- Fuzzer-Generated：由模糊测试器生成的程序划分，用于检验模型面对更不规则、更复杂或训练分布外程序时能否稳定执行形式规则。该划分在表 8 中整体最困难，并用于与 Human-Written 对照分析程序来源和复杂度造成的退化。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**PrEx accuracy**

预测与真实标签完全一致的比例：有效程序必须输出成功标签，无效程序不仅要判断为错误，还必须指出对应的被违反规则。因此它同时考查可执行性判断和规则级定位。 （越高越好，因为更高值表示模型更经常依据给定语义得到完整正确的结论。）

</div>
<div class="metric-item" markdown="1">

**相对 Standard 的准确率变化（pp）**

同一模型和语义形式体系下，KeywordSwap 或 KeywordObf 准确率相对 Standard 的百分点增减，用于隔离语义变换带来的稳健性损失。 （降幅越小越好；较大负值表示模型难以摆脱标准关键字或运算符含义的预训练先验。）

</div>
<div class="metric-item" markdown="1">

**按错误类型的规则级准确率**

在无效程序上，分别统计除零、模零、变量先使用后声明、循环外使用 break 或 continue 等错误的正确规则识别率，用于定位模型对哪类语义规则最不稳定。 （越高越好，因为它表示模型能够可靠地识别具体错误规则，而非只笼统判断程序有错。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 不同程序来源之间的泛化：Human-Written 对比 LLM-Translated 与 Fuzzer-Generated

<div class="result-value" markdown="1">

最强的三种 Human-Written 配置在 LLM-Translated 上的六列平均准确率分别下降 2.9、8.7 和 8.6 个百分点，在 Fuzzer-Generated 上分别下降 19、24.8 和 33.3 个百分点；其中 Qwen2.5-Coder 14B-CoT 在 $\mathbb{K}$/KeywordObf 下从 78% 降至 23%，单配置下降 55 个百分点。

</div>

作者据此认为，模型在人工短程序上取得的高分不能直接视为稳定掌握了形式语义；程序来源变化后，尤其面对模糊测试生成的复杂或不规则代码，性能显著恶化。该结果证明的是跨划分稳健性不足，但不能单独确定下降究竟来自程序长度、控制流复杂度、表面分布变化还是这些因素的组合。

<div class="result-source" markdown="1">

来源：第 5.1 节，表 6 与表 8

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Fuzzer-Generated programs (Table 8) the decline is even sharper, with mean drops of 19pp, 24.8pp, and 33.3pp computed the same way across Tables 8 and 6.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Standard 对比 KeywordSwap 与 KeywordObf 的语义迁移

<div class="result-value" markdown="1">

在 Human-Written 划分上，所有模型从 Standard 转到 KeywordSwap 时的准确率降幅中位数为 19 个百分点，转到 KeywordObf 时为 32 个百分点；最大降幅出现在 Ministral 3 14B 的 $\mathbb{K}$/KeywordObf，从 90% 降至 32%，文中按百分点记为 59pp。

</div>

关键字含义交换已经明显削弱模型，而引入新符号的混淆更困难，支持模型依赖标准语言符号—含义关联的解释。如果模型能系统执行提示中的规则，符号改名原则上不应造成如此普遍的下降。不过，该比较仍不能证明模型完全没有规则推理能力，因为部分模型与配置在变换后仍保持较高准确率。

<div class="result-source" markdown="1">

来源：第 5.2 节，表 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Human-Written programs (Table 6), KeywordObf is consistently harder than KeywordSwap: across all models, median accuracy falls by 19pp under KeywordSwap versus 32pp under KeywordObf (each median is the drop from Standard to KeywordSwap or KeywordObf, taken over all model rows and 𝕂/𝕊 formalisms in Table 6).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 错误类型与失败模式分析

<div class="result-value" markdown="1">

在 LLM-Translated 上，DeepSeek-Qwen 32B 的 822 次失败中有 695 次是假成功；在 Fuzzer-Generated 上，各模型跨配置出现 372–1,484 次假成功、597–1,003 次错误规则预测和 341–453 次假错误。KeywordObf 对循环外 break/continue 等依赖关键字的错误影响尤其明显。

</div>

主要问题不只是输出错误的规则编号：模型经常把违反所给 $C^*$ 语义的程序直接判为可执行。这与模型按熟悉的标准 C 外观作答、而未逐步应用给定规则的解释一致。错误类型图还显示，关键字依赖规则比算术和作用域规则更易受符号混淆影响；但这些错误统计是行为证据，不能直接揭示模型内部推理机制。

<div class="result-source" markdown="1">

来源：第 5.5 节；图 5；表 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For example, DeepSeek-Qwen 32B produces 695 false-success errors out of 822 total failures across configurations, suggesting that models often treat translated C-like code as executable even when it violates the supplied C∗ semantics.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验仅覆盖 Qwen、DeepSeek-Qwen 与 Ministral 等开源代码或推理模型；原文节选未报告闭源前沿模型，因此结论不能无条件推广到所有 LLM。
- 语义变换、程序来源与复杂度同时影响难度。现有跨划分结果清楚表明稳健性下降，但没有完全分离长度、控制流结构、翻译风格、模糊测试分布及符号陌生度各自的因果贡献；同时，推理模型缺少独立的非 CoT 对照。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Random：随机预测基线，用于给出多类别 PrEx 任务的机会水平；其准确率约为 16%–18%，说明仅猜测很难同时正确区分成功与具体错误规则。
- Qwen2.5-Coder 系列：面向代码任务训练的开源模型，覆盖 3B、7B、14B 和 32B 参数规模，用于观察代码专用预训练、模型规模及显式 CoT 提示是否提升形式语义应用能力。
- Ministral 3 系列：覆盖 3B、8B 和 14B 的开源模型，并比较 CoT 与非 CoT 条件；它提供不同模型家族下对规模效应和提示策略的交叉验证。
- DeepSeek-Qwen 14B/32B：默认生成推理轨迹的推理模型，用于检验增强推理能力是否足以克服标准语言先验，并与显式 CoT 的非推理模型进行对照。

**实验想回答的问题**

- 在明确提供程序语法与操作语义后，代码大模型能否据此判断程序是否可执行，并在无效时准确指出被违反的语义规则，而不是依赖预训练阶段形成的常规语言先验？
- 模型的规则应用能力是否能跨语义变换与程序来源保持稳定，尤其是在关键字含义被交换或混淆、程序由翻译或模糊测试生成、结构复杂度上升时？

**实验实现**

实验组合为两种语义形式体系 $\mathbb{S}$ 与 $\mathbb{K}$、三种语义设置 Standard、KeywordSwap 与 KeywordObf，以及非推理模型的 CoT/非 CoT 提示。Standard 使用原程序和标准语义；KeywordSwap 交换已有符号的语义并同步变换程序；KeywordObf 使用新符号混淆关键字，使模型更难直接调用标准语言记忆。有效程序标为 ##success##，无效变体标为 ##error## 并附被违反规则，真值由系统化变换过程产生。每个非推理模型配置运行 3 次并报告平均准确率；默认生成推理轨迹的推理模型只测试一种提示条件，不另设 CoT 与非 CoT 版本。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 语义变换强度消融：Standard、KeywordSwap 与 KeywordObf | Human-Written 上，从 Standard 到 KeywordSwap 的跨模型降幅中位数为 19pp，到 KeywordObf 为 32pp；最强三种 Human-Written 模型的平均语义迁移降幅仍分别达到 15.2pp、14.8pp 和 23.3pp。 | 该对照保持任务目标与程序有效性标签不变，改变符号和语义的对应关系，从而尽量隔离模型对标准编程语言先验的依赖。KeywordObf 降幅更大，说明完全陌生的新符号比交换熟悉符号更难；但符号变换也可能增加提示解析负担，因此下降不能全部归因于语义知识缺失。 | 第 5.2 节，表 6<br><span class="experiment-evidence">The top three Human-Written models (DeepSeek-Qwen 32B, Ministral 3 14B-CoT, and Qwen2.5-Coder 32B-CoT) incur mean semantic-shift drops of 15.2pp, 14.8pp, and 23.3pp, respectively (each averaged over {𝕂,𝕊} × {KeywordSwap, KeywordObf} in Table 6).</span> |
| CoT 提示消融：同一非推理模型的 CoT 与非 CoT 版本 | CoT 的效果依赖模型和规模。例如 Human-Written 的 Ministral 3 14B 在 $\mathbb{K}$ 三种设置下由 90%/75%/32% 变为 99%/79%/91%，但 Qwen2.5-Coder 3B 在同一组设置下由 44%/23%/7% 变为 32%/25%/16%；因此 CoT 并非一致有效。 | 该比较检验显式推理提示是否促使模型逐步应用规则。较强 Ministral 的 KeywordObf 大幅改善，说明推理轨迹在部分模型上有帮助；小型 Qwen 的 Standard 反而下降，说明要求输出思维链不等于获得可靠的形式推导能力。由于默认推理模型没有非 CoT 对照，此消融只能解释非推理模型，不能把所有模型家族放在完全相同的提示条件下比较。 | 第 5 节实验协议；数值见表 6<br><span class="experiment-evidence">Because reasoning models generate chain-of-thought traces by default, we evaluate them under one prompting condition only and do not run separate CoT and non-CoT variants.</span> |

**定性案例**

- Figure 5 的规则级雷达图显示，在 KeywordObf 下，continue-outside-loop 与 break-outside-loop 的多模型多边形比除零、模零和变量先使用后声明明显向内收缩；在 KeywordSwap 下，divide-by-zero 也相对 Standard 下降。作者将其解释为关键字和标准除法符号的预训练含义干扰了新语义。直观地说，模型往往知道“break 通常与循环有关”或“/ 通常表示除法”，但当论文临时重定义符号后，未能稳定地按新规则重新解释程序。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a program-semantics benchmark testing whether coding LLMs apply supplied formal rules rather than pretrained priors.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`f1fde37a6fd96068bb90cd098d2c3794ff75d99409fd6904ae820bcb3a71378d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
