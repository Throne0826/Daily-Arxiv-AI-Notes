---
title: "[论文解读] PromptResponse: Optimizing Prompts for LLM Coding Tasks"
description: "[arXiv 2608.21074][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.21074"
announcement_date: "2026-08-24"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-25T01:58:08.330783+00:00"
source_sha256: "771a9ba1235ff57e53f3b7597ce8c84e11b1db5bca665a91584a4dee1b8b809e"
tags:
  - "LLM Reasoning"
  - "大语言模型"
  - "代码生成"
  - "提示工程"
  - "提示格式"
  - "提示调优"
  - "提示稳定性"
  - "HumanEval"
  - "可复现性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.21074</p>

# PromptResponse: Optimizing Prompts for LLM Coding Tasks

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Erik Thureck, Robert Kühnen, Tim Jacobowitz</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.21074) · [PDF 下载](https://arxiv.org/pdf/2608.21074) · **关键词** 大语言模型, 代码生成, 提示工程, 提示格式, 提示调优, 提示稳定性, HumanEval, 可复现性<br>


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

本文位于大语言模型代码生成与提示工程的交叉领域。大语言模型能够把自然语言任务说明转换为可执行代码，但生成结果会随提示的措辞、结构和格式变化；即使任务语义相同，输出的正确性、执行效率和稳定性也可能不同。这种敏感性不仅影响软件开发效果，也会削弱采用大语言模型的研究流程之可复现性。既有提示优化研究主要考察问答、文本标注等自然语言任务，本文则聚焦代码生成，研究统一重排提示格式以及让另一大语言模型自动改写提示，是否会改变 GPT-4o 生成代码的任务表现、效率与稳定性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**提示工程（Prompt Engineering）**

在不修改模型参数的情况下，通过设计任务说明、示例和输出约束来影响模型行为。本文特别区分只改变信息组织形式的“重格式化”和由大语言模型按照策略改写内容表达的“提示调优”。

</div>
<div class="concept-item" markdown="1">

**HumanEval**

OpenAI 提出的代码生成基准，包含 164 个编程问题，通常要求模型依据函数签名、自然语言说明和示例补全程序。本文以原始版本为基线，并构造语义等价而句法形式不同的 JSON、Markdown、YAML 和大语言模型调优版本。

</div>
<div class="concept-item" markdown="1">

**提示稳定性（Prompt Stability）**

指模型面对语义相同但表述或格式不同的提示时，能否保持一致或近似一致的输出表现。稳定性越高，提示的偶然写法对实验结论影响越小，因而更有利于结果复现。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究输入是 HumanEval 的 164 个代码任务，每个任务分别表示为五种版本：未经修改的基线版本、JSON、Markdown、YAML，以及由另一大语言模型逐提示调优的版本。前三种重格式化版本旨在改善字段和示例的内部一致性，同时保持任务语义不变；调优版本则用于检验大语言模型能否依据预定义策略自动优化提示。所有版本交给 GPT-4o 生成代码，受控实验共执行 8200 次 API 请求，并从任务表现、生成或执行效率以及提示稳定性三个维度比较结果。该设置的关键假设是各版本表达相同的编程要求，因此观察到的系统性差异主要可归因于提示的句法组织或调优方式，而不是任务内容变化。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D$**

由 164 个 HumanEval 编程任务组成的基准任务集合。

</div>
<div class="notation-item" markdown="1">

**$V=\{v_{base},v_{JSON},v_{MD},v_{YAML},v_{tuned}\}$**

五种提示版本的集合，依次表示原始基线、JSON、Markdown、YAML 和大语言模型调优版本。

</div>
<div class="notation-item" markdown="1">

**$x_{i,v}$**

第 $i$ 个 HumanEval 任务在提示版本 $v$ 下的输入文本。

</div>
<div class="notation-item" markdown="1">

**$y_{i,v,r}$**

GPT-4o 对输入 $x_{i,v}$ 在第 $r$ 次执行中生成的代码输出。

</div>

</div>

**直接相关的工作**

- **Prompt Stability Score（Barrie et al., 2025）**: 该工作提出用于量化提示敏感性的稳定性指标，为本文从提示稳定性角度评估代码生成提供直接背景；所给章节未说明本文是否原样采用其具体计算公式。
- **PromptSET（Razavi et al., 2025）与 E-Bench（Zhang et al., 2024）**: 这些基准用于考察大语言模型对提示变化的敏感性，说明语义相同的提示仍可能产生不同输出；本文将问题进一步限定到代码生成，并比较结构化重格式化与自动提示调优。

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

本文采用受控实验，而不是提出或训练新的代码生成模型。核心自变量是同一组 HumanEval Python 编程任务的五种提示版本：原始的 $\mathrm{vanilla}$、结构化重排的 $\mathrm{json}$、$\mathrm{markdown}$ 与 $\mathrm{yaml}$，以及由 Mistral-7B-Instruct-v0.2 改写文档字符串的 $\mathrm{tuned}$。前三种重排版本尽量保留原始任务的函数签名、描述、示例和约束等语义内容，只改变外部语法结构；$\mathrm{tuned}$ 则保留函数签名与实现要求，但允许模型改写和扩展文档字符串，因此同时涉及措辞与格式标准化。研究者随后让固定版本的 GPT-4o 在默认设置下独立回答每个提示，并比较正确性、生成效率、生成代码的执行效率以及重复回答的稳定性。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造五种语义对应的 HumanEval 提示集

保留原始提示形成 $\mathrm{vanilla}$ 基线，并解析原始内容以构造 $\mathrm{json}$、$\mathrm{markdown}$ 和 $\mathrm{yaml}$ 三种统一模板；原文缺失的字段保留为空或使用模板占位符，不主动补写任务信息，也不修正原始语法和拼写问题。另以 Mistral-7B-Instruct-v0.2 改写原始提示的文档字符串，形成 $\mathrm{tuned}$ 版本，同时明确要求改写模型不得修改函数签名或生成实现代码。

<div class="method-step__io" markdown="1">

**输入**：HumanEval 的 $164$ 个原始 Python 编程任务；每个任务可能包含导入、辅助函数、函数签名、描述、注释、示例、变量说明和约束等字段。<br>
**输出**：五个各含 $164$ 个任务的提示集，即总计 $820$ 个“任务—提示版本”组合。

</div>

**直观理解**：这一步相当于把同一道题分别写在原始文本、JSON 表单、Markdown 文档、YAML 配置和经过语言润色的题面中。前三种主要检验“排版方式”是否影响模型，最后一种检验“让另一个大模型先润色题面”是否有额外作用。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 以隔离上下文的方式重复生成代码

每次请求都创建全新的 ChatGPT completion 上下文，不携带历史对话；统一要求模型仅输出指定签名的函数及必要导入。每个提示独立请求 $10$ 次，五种版本按顺序执行，且关闭流式输出；若回复包含多个答案，仅保留第一个答案。

<div class="method-step__io" markdown="1">

**输入**：五种提示集中每个任务的具体提示，以及统一的系统消息和用户前缀；目标代码生成模型为 $\texttt{gpt-4o-2024-08-06}$。<br>
**输出**：共 $5\times164\times10=8200$ 次代码生成结果，以及每次请求从发送到完整响应抵达主机的生成时长 $\mathrm{GenDuration}$。

</div>

**直观理解**：每次都像让同一位答题者在“失忆”状态下重新做题，避免上一轮回答影响下一轮。对同一题重复十次，既能估计一次生成是否正确，也能观察模型面对完全相同提示时是否稳定。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 清洗、组装并执行生成代码

第二个 Python 脚本移除模型偶尔附加的 Markdown 代码围栏，将生成代码与原始 HumanEval 中相应的辅助函数拼接，并通过 Python 的 $\texttt{exec()}$ 动态执行；随后运行任务配套测试，记录是否通过全部测试、响应字符数和评测耗时。语法错误、运行错误或测试失败均计为未通过，而 $\mathrm{PassDuration}$ 只在完全通过的回答上统计。

<div class="method-step__io" markdown="1">

**输入**：GPT-4o 返回的函数代码、HumanEval 原始任务中可能存在的辅助函数，以及对应的官方测试用例。<br>
**输出**：逐次执行的成功或失败标记、$\mathrm{ResponseLen}$、$\mathrm{EvalDuration}$，以及通过样本对应的 $\mathrm{PassDuration}$。

</div>

**直观理解**：这一步不是判断代码“看起来是否合理”，而是真正运行代码并用标准测试验收。只在正确代码上比较运行时间，可以避免把立即报错或提前退出的错误程序误判成高效程序。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 聚合指标并进行非参数统计检验

对每个任务的十次重复结果计算通过比例 $\mathrm{PassRate}$，并计算所有回答对之间 ROUGE-L 的平均值以表示句法稳定性；同时聚合各项效率指标。由于 Shapiro–Wilk 正态性检验在所有因变量上均显著，研究者使用 Kruskal–Wallis 检验比较五种提示版本的总体差异；出现显著主效应时，再进行带 Bonferroni 校正的两两 Mann–Whitney U 检验。

<div class="method-step__io" markdown="1">

**输入**：每个任务—提示版本下的 $10$ 次正确性记录、生成与执行时长、响应长度，以及十份文本回答。<br>
**输出**：五种提示版本在任务表现、生成效率、代码执行效率和回答稳定性上的统计比较，以及 Kruskal–Wallis 的 $\varepsilon^2$ 和两两比较的秩二列相关 $r$ 等效应量。

</div>

**直观理解**：先判断五组整体上是否存在可靠差异，再定位究竟是哪两种格式不同；Bonferroni 校正用于降低多次比较造成偶然显著的风险。效应量则补充说明差异有多大，避免只凭显著性判断实际价值。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文没有训练、微调或通过损失函数优化 GPT-4o，也没有以实验反馈更新提示；所谓 $\mathrm{tuned}$ 是一次离线数据构造过程，即让 Mistral-7B-Instruct-v0.2 按固定指令改写 HumanEval 文档字符串。后续 GPT-4o 仅执行代码生成推理，统计检验用于比较既定提示版本，而非反向优化模型参数或自动搜索最优提示。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 受控提示变体构造模块**

该模块把 $\mathrm{dataset}$ 作为五水平自变量。$\mathrm{json}$、$\mathrm{markdown}$ 和 $\mathrm{yaml}$ 使用统一字段组织函数、导入、辅助函数、签名、描述、注释、示例、变量和约束；其内容尽量从 $\mathrm{vanilla}$ 原样解析，缺失部分不依靠人工语义推断补齐。$\mathrm{tuned}$ 使用 Mistral-7B-Instruct-v0.2 改写整个文档字符串，系统指令限定其只提高文档字符串的清晰度与帮助性，不得改变函数签名或写出实现。

> 直观理解：这一设计试图把“题目要求是什么”和“题目怎样呈现”分开。不过，结构化版本不仅改变符号，还统一了字段顺序并显式加入空字段；$\mathrm{tuned}$ 更会改变措辞和篇幅。因此实验能比较完整提示方案，却不能把观察到的差异严格归因于某一个孤立的标点或单一排版因素。

**2. 隔离式重复代码生成模块**

所有变体使用同一 GPT-4o 发布版本、相同系统角色和用户任务前缀，并采用模型默认参数。每个提示的 $10$ 次生成均位于独立的新会话中，不共享上下文；研究者没有自行设定低温度等参数，因为已有工作表明所谓确定性设置仍不能保证稳定输出，同时默认设置更接近日常用户使用情形。

> 直观理解：固定模型和外层指令，使主要变化来自题面版本；新会话则排除聊天历史干扰。重复十次不是传统的 $\mathrm{pass@10}$——研究并非允许从十份答案中挑一份，而是把每次都视为独立的一次回答，再统计单次成功率和回答一致性。

**3. 多维评测与统计模块**

$\mathrm{PassRate}$ 表示同一提示的十次回答中通过全部 HumanEval 测试的比例，用于联合反映单次任务表现及其跨重复波动；$\mathrm{GenDuration}$ 测量 API 请求到完整响应抵达的时间，$\mathrm{EvalDuration}$ 测量主机执行评测的时间，$\mathrm{PassDuration}$ 仅保留正确答案的评测时间，$\mathrm{ResponseLen}$ 为回答字符数。稳定性使用十次回答之间所有两两 ROUGE-L 的均值，取值从 $0$ 到 $1$；值越高表示最长公共子序列越相似，但不等同于程序语义或算法完全相同。

> 直观理解：这些指标分别回答四类问题：能否做对、模型多久给出答案、生成的正确程序运行是否高效，以及同一提示反复询问时是否给出相似文本。生成时长会受到远端服务器负载影响，字符长度也不直接等于代码质量，因此它们应作为辅助效率证据，而不能单独解释为模型推理能力。

**训练与推理**

离线准备阶段从 Hugging Face 获取 $\mathrm{vanilla}$ HumanEval，将其解析成三个结构化版本，并用默认温度的 Mistral-7B-Instruct-v0.2 生成 $\mathrm{tuned}$ 文档字符串。正式推理阶段使用固定的 $\texttt{gpt-4o-2024-08-06}$：系统消息设为 Python 编程专家，用户消息要求仅返回指定签名的函数和必要导入；五种数据集的每道题各在无历史上下文的新会话中请求 $10$ 次。生成后不进行模型训练，而是清洗代码、补回 HumanEval 原有辅助函数、动态执行官方测试，并据此计算正确性、时长、长度和文本稳定性指标。最后以非参数检验判断提示版本是否与这些结果存在统计关联。

**复现信息**

复现时需要固定五类提示的具体模板、Mistral 改写指令、GPT-4o 的外层消息以及模型发布版本，否则“格式效应”可能与模板措辞或模型版本变化混杂。原实验使用 GPT-4o 默认设置，关闭响应流，全部 $8200$ 次请求顺序执行且不使用多进程；实验于 $2025$ 年 $7$ 月 $10$ 日晚完成，总耗时约 $205$ 分钟，因此 $\mathrm{GenDuration}$ 主要适合当次实验中的同期相对比较，不宜视为可跨日期复现的绝对延迟。评测端需要移除偶发的代码围栏，若模型给出多个答案仅采用第一个，并使用 HumanEval 配套测试执行代码；由于 $\texttt{exec()}$ 会运行模型生成内容，实际复现应在隔离沙箱、受限权限和超时机制下进行。统计分析以每种提示版本的 $164$ 个任务为聚合比较单位：先做 Shapiro–Wilk 检验，再使用 Kruskal–Wallis 检验；显著后采用经 Bonferroni 校正的 Mann–Whitney U 两两比较，并分别报告 $\varepsilon^2$ 与 $r$，以同时呈现显著性和差异规模。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HumanEval：用于评估LLM生成Python代码是否通过题目所提供的全部测试用例；实验覆盖5种提示词格式、820个提示词，每个提示词执行10次，共8200个数据点。原文未明确报告训练集、验证集或测试集划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$\mathrm{PassRate}$**

对每个提示词，统计10次执行中通过HumanEval全部测试用例的比例；它同时反映任务性能和语义稳定性。 （越高越好，因为更高比例表示代码更经常正确通过全部测试。）

</div>
<div class="metric-item" markdown="1">

**$\mathrm{GenDuration}$、$\mathrm{EvalDuration}$和$\mathrm{PassDuration}$**

$\mathrm{GenDuration}$是模型形成代码解答所需时间；$\mathrm{EvalDuration}$是运行生成代码并执行测试用例所需时间；$\mathrm{PassDuration}$只在通过测试的执行中统计代码通过全部测试所需时间。 （越低越好，因为较短时间意味着生成或代码执行效率更高；但$\mathrm{PassDuration}$排除了失败执行，不能单独代表整体任务效率。）

</div>
<div class="metric-item" markdown="1">

**$\mathrm{ResponseLen}$和$\mathrm{Rouge\mbox{-}L}$**

$\mathrm{ResponseLen}$统计生成代码片段的字符数；$\mathrm{Rouge\mbox{-}L}$计算同一提示词10次响应之间的两两文本相似度平均值，用于衡量句法或表面形式稳定性。 （$\mathrm{ResponseLen}$通常越低表示响应更短，但短并不自动意味着代码正确；$\mathrm{Rouge\mbox{-}L}$越高表示重复执行产生的文本形式更一致。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 提示词格式对通过率的影响

<div class="result-value" markdown="1">

$\mathrm{json}$、$\mathrm{markdown}$、$\mathrm{vanilla}$和$\mathrm{yaml}$的平均$\mathrm{PassRate}$分别为$0.901$、$0.890$、$0.886$和$0.873$，$\mathrm{tuned}$最低，为$0.748$。数据集格式的主效应显著，$\chi^2(4)=19.177$，$p=0.0007253633$，$\varepsilon^2=0.0186$；$\mathrm{tuned}$相较于$\mathrm{json}$、$\mathrm{markdown}$和$\mathrm{vanilla}$的通过率显著更低。

</div>

在本实验中，JSON格式取得最高平均通过率，而调整后的$tuned$格式明显落后，说明提示词外观或组织方式可能影响代码任务的正确性。不过效应量较小，结果只能说明这些格式在当前模型、任务和实验协议下存在统计差异，不能证明JSON在所有编程任务或模型上都必然最好，也不能据此判断$tuned$具体哪一项设计导致性能下降。

<div class="result-source" markdown="1">

来源：Section 4.1, Pass Rate

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The total average PassRates of ‹json› (0.901), ‹markdown› (0.890), ‹vanilla› (0.886), and ‹yaml› (0.873) were similarly high, with ‹tuned› (0.748) significantly behind.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 提示词格式对模型生成耗时的影响

<div class="result-value" markdown="1">

$\mathrm{yaml}$的平均$\mathrm{GenDuration}$最低，为$1.37\,\mathrm{s}$，其次是$\mathrm{markdown}$的$1.44\,\mathrm{s}$和$\mathrm{json}$的$1.49\,\mathrm{s}$；$\mathrm{vanilla}$与$tuned$均为$1.61\,\mathrm{s}$。格式因素的主效应显著，$\chi^2(4)=35.046$，$p=0.0000004544938$，$\varepsilon^2=0.0381$；$\mathrm{vanilla}$和$tuned$相对$\mathrm{json}$、$\mathrm{markdown}$及$\mathrm{yaml}$均显著更慢。

</div>

YAML、Markdown和JSON在模型生成阶段略快于原始格式和$tuned$格式，但差异量级约为十分之几秒，且效应量仍较小。这表明格式可能影响生成效率，却不能说明总体系统效率一定提高，因为代码测试执行时间、响应长度和正确率还需要分别考察。

<div class="result-source" markdown="1">

来源：Section 4.2, Generation Duration

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On average, prompts in the ‹yaml› format were generated the fastest (x̄ = 1.37 s, sintra = 0.36 s, s = 0.68 s), followed closely by ‹markdown› (x̄ = 1.44 s, sintra = 0.46 s, s = 0.91 s) and ‹json› (x̄ = 1.49 s, sintra = 0.65 s, s = 2.51 s), with ‹vanilla› (x̄ = 1.61 s, sintra = 0.55 s, s = 0.85 s) and ‹tuned› (x̄ = 1.61 s, sintra = 0.57 s, s = 1.04 s) taking significantly longer.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 提示词格式对跨次文本稳定性的影响

<div class="result-value" markdown="1">

$\mathrm{json}$、$\mathrm{markdown}$和$\mathrm{yaml}$的平均$\mathrm{Rouge\mbox{-}L}$分别为$0.842$、$0.837$和$0.821$，高于$tuned$的$0.798$和$\mathrm{vanilla}$的$0.787$。格式因素的主效应显著，$\chi^2(4)=14.950$，$p=0.004805055$，$\varepsilon^2=0.0134$；$\mathrm{vanilla}$相对$\mathrm{json}$和$\mathrm{yaml}$的差异显著，但效应量较小。

</div>

结构化输出格式，尤其是JSON，在同一提示词重复执行时产生的文本形式更一致；原始格式的表面形式稳定性最低。该指标衡量的是代码文本的相似程度，不是功能正确性，因此较高的$\mathrm{Rouge\mbox{-}L}$不能保证代码通过测试，也不代表模型探索不同但同样正确的实现是坏事。

<div class="result-source" markdown="1">

来源：Section 4.6, ROUGE-L Scores

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On average, reformatted prompts resulted in higher Rouge-L scores, with ‹json› (x̄ = 0.842, sintra = 0.136) in first, followed by ‹markdown› (x̄ = 0.837, sintra = 0.138) and ‹yaml› (x̄ = 0.821, sintra = 0.148).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验章节只报告HumanEval、820个提示词和每个提示词10次执行；原文未明确报告其他数据集、模型、模型版本或数据划分，因此结论的跨任务和跨模型泛化能力有限。
- 效率指标存在明显异常值，且$\mathrm{PassDuration}$排除了失败执行、$\mathrm{EvalDuration}$还受到特定题目和内存错误影响；因此不同格式的平均耗时不应脱离异常值处理方式和通过率单独比较。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- $\mathrm{vanilla}$：未采用结构化输出格式的原始提示词，作为不改变提示词格式的基准。
- $\mathrm{json}$：要求模型以JSON格式组织响应，用于检验结构化格式对正确性、稳定性和效率的影响。
- $\mathrm{markdown}$：要求模型以Markdown格式组织响应，用于与JSON等结构化格式比较。
- $\mathrm{yaml}$：要求模型以YAML格式组织响应，用于检验另一种结构化文本格式的效果；$\mathrm{tuned}$为经过调整的提示词格式，但其具体调整方式在所给章节中未明确说明。

**实验想回答的问题**

- 不同提示词格式（$\mathrm{vanilla}$、$\mathrm{json}$、$\mathrm{markdown}$、$\mathrm{yaml}$和$\mathrm{tuned}$）是否会影响LLM在HumanEval编程任务上的通过率与跨次执行稳定性？
- 不同提示词格式是否会改变代码生成效率，包括生成耗时、测试执行耗时、通过测试耗时和响应长度？

**实验实现**

每个提示词执行10次，并以提示词为单位聚合结果；对于$\mathrm{GenDuration}$、$\mathrm{EvalDuration}$、$\mathrm{PassDuration}$和$\mathrm{ResponseLen}$，作者同时报告提示词内部执行的标准差$s_{\mathrm{intra}}$与全局标准差$s$。统计显著性分析在R中完成，采用卡方检验报告数据集因素的主效应、$p$值和效应量$\varepsilon^2$，并进行事后两两比较。对于$\mathrm{PassDuration}$，不通过测试的执行被排除；对于代码评估，还特别记录异常耗时和内存错误案例。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- HumanEval第129题（$\mathrm{minPath(grid,k)}$）是一个具有代表性的困难案例：题目描述超过200个单词，整体$\mathrm{PassRate}$为$0.54$，正确代码通常需要更长评估时间；这说明格式平均值可能掩盖特定题目难度和正确实现复杂度的影响。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper optimizes prompts specifically to improve LLM performance on code-generation or coding-reasoning tasks.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`771a9ba1235ff57e53f3b7597ce8c84e11b1db5bca665a91584a4dee1b8b809e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
