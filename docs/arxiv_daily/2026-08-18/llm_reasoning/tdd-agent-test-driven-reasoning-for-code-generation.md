---
title: "[论文解读] TDD-Agent: Test-Driven Reasoning for Code Generation"
description: "[arXiv 2608.16742][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.16742"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:17:26.422641+00:00"
source_sha256: "8e438e9d9b422226b1fa75584666337bce02854ca8f8c49ed2492a178d56e439"
tags:
  - "LLM Reasoning"
  - "大语言模型代码生成"
  - "测试驱动开发"
  - "仓库级代码生成"
  - "自生成测试"
  - "执行反馈"
  - "软件工程智能体"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.16742</p>

# TDD-Agent: Test-Driven Reasoning for Code Generation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Hongyue Yu, Kefan Li, Jiakun Li, Hongzheng Chai, Yuan Yuan, Rui He, Junyi Wei</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: National College for Excellent Engineers, Beihang University；Affiliation: School of Computer Science and Engineering, Beihang University；Affiliation: Qingdao Research Institute and Hangzhou Innovation Institute, Beihang University；Affiliation: School of Software, Beihang University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.16742) · [PDF 下载](https://arxiv.org/pdf/2608.16742) · **关键词** 大语言模型代码生成, 测试驱动开发, 仓库级代码生成, 自生成测试, 执行反馈, 软件工程智能体<br>
**代码**: [https://anonymous.4open.science/r/TDD-Agent-Framework-6370/](https://anonymous.4open.science/r/TDD-Agent-Framework-6370/)

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

本文属于大语言模型代码生成与软件工程智能体研究。研究对象不只是根据自然语言补全一个孤立函数，还包括在已有代码仓库中定位目标、理解跨文件依赖并实现符合既有接口与行为约束的代码。软件测试可为生成结果提供可执行反馈，但以往方法通常把测试当作实现完成后的静态验证器；本文关注另一种定位：先生成测试以显式表达任务意图，再让测试与实现依据执行结果共同演化。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试驱动开发（Test-Driven Development, TDD）**

一种先编写描述预期行为的测试、再实现代码并反复运行测试的开发方式。本文将其转化为大语言模型的推理流程，使模型在编码前先明确输入、输出、边界情况和行为约束。

</div>
<div class="concept-item" markdown="1">

**仓库级代码生成**

模型需要在现有软件仓库中完成函数或模块实现，而不是只生成上下文独立的短程序。任务通常要求理解项目结构、调用关系和外部依赖，并可能需要构造模拟对象或运行环境。

</div>
<div class="concept-item" markdown="1">

**自生成测试偏差**

模型生成的测试本身可能不完整或错误，因此通过这些测试并不必然表示实现正确。若把有缺陷的测试固定为唯一反馈来源，模型可能被误导去修改原本合理的代码。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定自然语言任务描述、目标函数信息以及仓库级任务中的现有代码与依赖环境，系统需要输出满足预期行为的实现代码。本文考察两个设置：在 LiveCodeBench 的函数级任务中，用轻量级 TDD-prompt 单独检验“先测试、后实现”的推理作用；在 RepoEval 的仓库级任务中，模型还需浏览仓库、理解依赖并生成可执行测试。核心假设是不在预测阶段依赖预先提供的测试，而由同一智能体先生成测试，再保留对话历史，根据实际执行反馈迭代修改测试和代码，最终输出完整实现；这也意味着系统必须防范自生成测试错误，不能把测试视为不可更改的正确标准。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **AgentCoder**: 该方法通过多智能体分离程序员与测试员角色，说明显式测试生成能够帮助提高代码正确性。TDD-Agent则采用保留统一对话历史的单智能体，使其能够同时修改实现与测试，以减少角色协调开销并维持推理的一致性。
- **TENET**: TENET利用仓库中预先存在的测试进行测试选择、上下文检索和反馈驱动的代码改进。TDD-Agent不假设预测时可访问预定义测试，而是在实现前自行合成可执行测试，并通过执行反馈联合改进测试与代码。

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

TDD-Agent 将测试驱动开发转化为代码生成智能体的推理流程，核心不是训练一个新模型，而是在推理时让现成大语言模型先把自然语言需求和仓库上下文转化为可执行测试，再联合修正测试与实现。给定仓库上下文 $\mathcal{R}$、目标函数 $f_{target}$ 和可用工具集 $\mathcal{T}_{tools}$，智能体 $\mathcal{A}$ 首先检查目录、文件结构和相关代码，生成初始单元测试 $U_0$；随后编写实现 $C_0$，通过 pytest 执行当前测试得到报告 $E_t$，并依据成功、失败、异常及断言信息更新代码 $C_{t+1}$ 和测试 $U_{t+1}$。循环最多进行 10 轮，也可由智能体调用 Early Terminator 提前结束，最终输出直接写入目标文件的实现代码。

其关键区别是测试并非固定不变的外部约束。传统“先生成测试、再让代码通过测试”的做法会把错误断言也当成正确规范，而 TDD-Agent 允许智能体在看到执行反馈后同时修改代码和测试：若代码确有缺陷，就修复实现；若测试误解了接口、预期值或边界条件，就修订测试；若当前实现与测试均较可信，还可扩展测试以覆盖更多行为。通俗地说，智能体先把“题目到底要求什么”写成可运行的检查清单，然后一边执行清单、一边校正答案和清单本身，但最终正确性仍由预测阶段不可见的原仓库测试判定，而不是由智能体自编测试判定。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 仓库上下文检查与需求定位

智能体通过 Directory Viewer、Structure Inspector、File Reader 和 Code Searcher逐步定位目标函数的调用方、相关类型、相邻实现及项目约定；它按需获取局部信息，而不是一次性装入整个仓库。

<div class="method-step__io" markdown="1">

**输入**：仓库上下文 $\mathcal{R}$、待补全函数 $f_{target}$ 以及工具集 $\mathcal{T}_{tools}$。<br>
**输出**：形成用于解释目标行为的仓库证据，包括函数签名、依赖接口、数据结构、调用方式和潜在边界条件。

</div>

**直观理解**：这一步相当于在动手写函数前先查项目目录、接口说明和其他人的调用代码，以免只凭函数名猜需求。结构摘要和定点读取还能减少无关代码占用模型上下文。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 测试优先的可执行规格构造

智能体以测试设计者身份生成初始测试套件 $U_0=\mathcal{A}_{design}(\mathcal{R},f_{target}\mid\mathcal{T}_{tools})$，并通过 Artifact Submitter 将其写入目标文件同目录下的临时测试文件 `test_by_agent.py`。

<div class="method-step__io" markdown="1">

**输入**：检索到的仓库证据、$f_{target}$ 的任务要求以及工具集 $\mathcal{T}_{tools}$。<br>
**输出**：一组可由 pytest 执行的初始单元测试 $U_0$，用于明确正常输入、边界情况和预期输出。

</div>

**直观理解**：先写测试迫使模型把模糊需求变成具体例子，例如“输入什么、应返回什么、异常如何处理”。测试在这里既是检查工具，也是智能体对任务规格的显式表述。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始实现与受控测试执行

智能体生成初始实现 $C_0$ 并原位替换目标代码；Test Runner 只对最新的 `test_by_agent.py` 运行 pytest，在第 $t$ 轮产生执行报告 $E_t=\operatorname{Execute}(C_t,U_t)$。

<div class="method-step__io" markdown="1">

**输入**：初始测试套件 $U_0$、目标函数所在文件及已获取的仓库上下文。<br>
**输出**：当前实现 $C_t$、当前测试 $U_t$ 以及包含通过、失败或运行异常信息的报告 $E_t$。

</div>

**直观理解**：这一步像先交一版答案，再立即运行自己写的检查题。执行结果把抽象的“代码可能有问题”变成具体的失败位置、实际输出和预期输出差异。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 测试与代码双轨反思迭代

智能体执行联合状态更新 $(C_{t+1},U_{t+1})=\mathcal{A}_{reflect}(C_t,U_t,E_t,\mathcal{R})$：失败时分析应修代码、修测试还是补充上下文，成功时考虑增强测试覆盖；随后重新提交制品并执行测试，直至调用 Early Terminator 或达到最多 10 轮。

<div class="method-step__io" markdown="1">

**输入**：当前代码 $C_t$、测试 $U_t$、执行报告 $E_t$ 和仓库上下文 $\mathcal{R}$。<br>
**输出**：最终目标函数实现，以及循环结束时的智能体测试；论文的正式评测另用预测期间不可见的原仓库测试检查实现。

</div>

**直观理解**：测试失败不自动意味着代码错了，因为模型写出的测试也可能误解需求，因此两边都允许修正。测试全部通过也不必立即停止，智能体可以先增加更苛刻的检查，降低“错误代码碰巧通过弱测试”的风险。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 测试优先规格生成

$$
U_{0}=\mathcal{A}_{design}(\mathcal{R},f_{target}\mid\mathcal{T}_{tools})
$$

**符号说明**

- $U_0$：实现代码生成前构造的初始单元测试套件。
- $\mathcal{A}_{design}$：智能体处于测试设计角色时执行的生成过程。
- $\mathcal{R}$：目标仓库中可供检查的代码、目录结构和相关上下文。
- $f_{target}$：需要实现或补全的目标函数。
- $\mathcal{T}_{tools}$：智能体可调用的上下文检查、制品提交和执行工具集合。
- $\mid$：表示测试生成过程以右侧工具集为可用操作条件，而非普通数值运算。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把第一阶段形式化为“先理解、再写可执行规格”：智能体利用工具从仓库中取证，并针对目标函数生成 $U_0$。它的重要性在于明确测试不是实现后的附属物，而是约束后续代码生成的首个显式产物。<br>
**原文位置**：第 2.1 节，公式 (1)，Phase 1: Test-First Specification Setup

</div>

</div>

<div class="equation-block" markdown="1">

#### 执行反馈驱动的代码与测试联合更新

$$
E_t=\operatorname{Execute}(C_t,U_t),\qquad (C_{t+1},U_{t+1})=\mathcal{A}_{reflect}(C_t,U_t,E_t,\mathcal{R})
$$

**符号说明**

- $t$：当前迭代轮次的索引。
- $C_t$：第 $t$ 轮的目标函数实现代码。
- $U_t$：第 $t$ 轮使用的智能体生成测试套件。
- $E_t$：在 $C_t$ 上执行 $U_t$ 得到的 pytest 测试报告或执行反馈。
- $\operatorname{Execute}$：通过 Test Runner 运行当前测试与实现的执行过程。
- $\mathcal{A}_{reflect}$：智能体依据当前代码、测试、执行反馈和仓库证据进行诊断与修订的反思过程。
- $C_{t+1}$：反思后得到的下一轮实现代码。
- $U_{t+1}$：反思后得到的下一轮测试套件。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分先把当前代码与测试送入执行器，得到可观察反馈 $E_t$；第二部分再让智能体联合决定下一版代码和测试。两式合起来表达了方法的核心闭环：失败反馈不是单向要求修改代码，而是用于重新判断实现、测试和需求理解中的哪一部分需要改变。<br>
**原文位置**：第 2.1 节，公式 (2) 与公式 (3)，Phase 2: Dual-Track Test-Code Co-Refinement

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文给出的 TDD-Agent 是基于工具调用和提示控制的推理时智能体框架，没有报告参数训练、微调损失、奖励函数或梯度优化目标；公式 (1) 至 (3) 描述的是制品生成、程序执行和状态更新，而不是可微训练目标。优化发生在任务层面：智能体根据测试反馈反复改进 $C_t$ 与 $U_t$，目标是产生能够通过仓库隐藏测试的函数实现，但隐藏测试不参与预测阶段的反馈循环。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 上下文检查工具组**

Directory Viewer 提供经过排序和数量限制的目录视图；Structure Inspector 返回 Python 类、函数或方法签名及行号而折叠实现；File Reader 按 1 起始的闭区间行号读取、单次最多 200 行；Code Searcher 支持受限的仓库级词法搜索，只允许白名单命令，并拒绝危险元字符、重定向和子 shell。该设计向智能体提供足以理解依赖关系的检索能力，同时控制上下文长度和任意命令执行风险。

> 直观理解：模型不需要阅读整个仓库，而是先看地图、再看骨架、最后打开相关片段。受限搜索保留了查找定义和调用点的能力，又避免让模型获得无限制 shell 权限。

**2. 制品提交与隔离测试执行**

Artifact Submitter 分别处理测试和实现：测试覆盖写入 `test_by_agent.py`，实现则替换原仓库中的目标代码。Test Runner 无参数且只执行最近提交的临时测试文件；pytest 报告被追加到对话上下文，原仓库隐藏测试在预测阶段既不可见，也不能通过该工具执行，只在生成结束后用于正式评价。

> 直观理解：该模块把模型输出真正落到文件并运行，使模型能依据真实执行结果纠错。把自生成测试与隐藏评测测试隔离，防止智能体直接针对最终答案检查器调代码，也说明“通过自编测试”只是中间信号，不等于最终正确。

**3. 双轨反思与提前终止控制**

每次 Test Runner 返回 $E_t$ 后，智能体可修改 $C_t$、修改 $U_t$、继续检查上下文或调用 Early Terminator。执行成功时提示模型考虑加强测试；执行失败时提示其诊断原因，而不预设错误一定属于实现，从而处理错误代码、错误测试和规格理解不足三类可能性。

> 直观理解：固定测试只会要求代码迎合当前断言，哪怕断言本身写错；双轨反思允许模型重新检查自己的判断。不过终止仍由模型置信度或 10 轮上限控制，因此弱测试导致的过早停止仍是该流程的潜在风险。

**训练与推理**

训练流程：原文未描述对基础模型进行额外训练，因此不能把测试通过率解释为训练奖励。框架将各工具以 JSON schema 暴露给模型，规定名称、描述、参数类型及必填字段，并要求每次模型回复至少包含一个有效工具调用；这属于智能体运行协议，而非模型参数学习。

推理流程：对于每个目标函数，智能体先使用目录查看、结构检查、定点文件读取和受限搜索收集 $\mathcal{R}$ 中的相关证据，然后提交 $U_0$；接着生成 $C_0$、替换目标代码，并只运行最新的智能体测试。每轮 pytest 报告 $E_t$ 被加入会话，智能体据此选择继续检索、修改实现、修改测试、扩充测试或终止。主实验将最大迭代数设为 10；每次获得执行结果后均可调用 Early Terminator 提前停止。预测结束后，评测系统才把最终代码集成回原仓库并运行原有隐藏单元测试，因而中间测试负责引导推理，隐藏测试负责衡量真实功能正确性。

**复现信息**

复现该方法需要保留三项会影响结果解释的设置。第一，测试文件固定写为目标文件同目录下的 `test_by_agent.py`，实现直接原位修改目标文件，Test Runner 使用 pytest 且只运行最近提交的该测试文件。第二，上下文访问受到控制：File Reader 单次最多返回 200 行；Code Searcher 对命令做 `shlex` 分词，只允许管道作为组合操作，并将 `find`、`grep`、`egrep`、`fgrep`、`xargs`、`head`、`tail`、`cat`、`less`、`wc`、`sort`、`uniq`、`awk` 和 `cut` 限定为可执行命令；目录工具还排除 `.git`、默认隐藏隐藏文件并限制返回项数。第三，主设置最多进行 10 轮联合修订，但允许提前终止，因此实际调用次数取决于模型判断，而不是固定执行 10 次。

公平理解实验时还需注意，预测期间原仓库测试完全不向智能体开放，也不能由 Test Runner 执行；正式正确性是在生成完成后由这些测试独立判定。这种隔离避免评测泄漏，但也使性能依赖智能体生成测试的有效性以及终止判断：测试可能正确却区分力不足，也可能包含错误断言，而模型还可能在实现未通过自生成测试时提前结束。论文报告的双轨更新正是为缓解前两类问题，但没有提供形式化保证，且迭代上限、基础模型的工具调用能力和自生成测试质量都会影响最终输出。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LiveCodeBench：用于函数级对比实验，作用是隔离“先构造测试、后生成实现”的提示策略本身。每道题为各方法生成10个样本，并以无偏$\mathrm{pass@1}$评价。所给原文未明确报告所用题目规模、时间切分或具体版本，因此不能据此判断是否覆盖完整LiveCodeBench。
- RepoEval：用于仓库级TDD-Agent评测及组件消融。模型在现有Python代码库中为缺失的目标函数生成测试和实现，并利用测试执行结果反复修订。所给原文未明确报告样本规模、划分方式及仓库选择标准。
- 仓库保留测试：作为独立于模型自生成测试的外部判定标准，用于判断最终实现是否真正满足仓库要求，并用于区分“自生成测试通过但保留测试失败”的匹配失败。原文片段未给出该测试集的数量、覆盖范围或构造过程。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**无偏$\mathrm{pass@1}$或通过率**

衡量生成实现通过目标任务外部测试的概率或比例。LiveCodeBench每题采样10次后估计无偏$\mathrm{pass@1}$；RepoEval表4报告通过率百分比。两者都面向代码正确性，但原文片段没有说明二者是否采用完全相同的聚合方式。 （越高越好，因为更高值表示更多生成实现通过用于最终评价的测试。）

</div>
<div class="metric-item" markdown="1">

**测试通过率与目标函数行覆盖率**

测试通过率要求整套生成测试在标准实现上全部成功，主要检查测试是否包含错误假设或幻觉需求；行覆盖率为$\text{Covered Lines}/\text{Total Lines}$，使用pytest-cov计算生成测试执行到目标函数代码行的比例，主要检查测试触及实现逻辑的广度。 （通常越高越好：高测试通过率表示测试与标准实现更一致，高覆盖率表示测试执行了更多目标代码路径；但二者都不能单独证明断言足够敏感或需求理解完整。）

</div>
<div class="metric-item" markdown="1">

**变异分数**

对每题从标准实现生成20个变异体，以$\text{Killed Mutants}/\text{Total Mutants}$计算生成测试识别错误变异体的比例；若测试无法通过标准实现，则该题变异分数置为0。它比单纯覆盖率更关注测试是否能通过断言发现行为错误。 （越高越好，因为生成测试能够杀死更多带有人工扰动的错误实现；但其结论仍受变异算子及每题仅20个变异体的代表性限制。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### LiveCodeBench函数级比较：TDD-prompt对比CoT、SCoT、Self-Planning和ICoT，并分别搭配三种骨干模型。

<div class="result-value" markdown="1">

作者报告TDD-prompt在三个模型上均优于全部提示基线，表明测试优先步骤的收益不局限于某一个模型。所给片段没有包含表1的具体分数、差值或统计不确定性，因此无法量化提升幅度。

</div>

这一结果检验的是：在不引入仓库工具循环时，把具体测试用例作为实现前的推理产物是否比自然语言推理、结构化推理、任务规划或意图提炼更有效。它支持“测试可作为推理框架”的作者主张，但仅凭现有信息不能证明收益来自测试的可执行性，因为函数级提示只要求设计测试和推导输出，片段未说明这些测试是否实际运行；也不能证明对未评测模型、语言或任务分布同样有效。

<div class="result-source" markdown="1">

来源：第3.1节，表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 1, TDD-prompt outperforms all baselines on three LLMs.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### RepoEval逐轮分析：比较三种模型在TDD-Agent执行反馈循环中的代码通过率变化。

<div class="result-value" markdown="1">

三种模型均从迭代修订中获益，其中DeepSeek累计提升最大；改进曲线在约第6至7轮趋于平台。原文片段没有给出图3各轮的具体通过率，因此这里只能报告趋势，不能报告绝对增益。

</div>

共同上升说明执行失败信息能够帮助仍在运行的任务修正代码。DeepSeek较少在首次自测成功后立即停止，因此更充分利用后续轮次；GPT前期增长较快后趋稳；Qwen虽然有时在尚未通过自生成测试时提前结束，仍获得较小的正收益。第6至7轮附近的平台意味着中等迭代预算可能具有较好的性能与计算成本折中，但这只是三种模型和当前任务设置下的经验现象，不是通用的最优停止轮数。

<div class="result-source" markdown="1">

来源：第4.2节，图3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across all three models, the improvement curves gradually converge and reach a near-plateau around iterations 6–7.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 生成测试质量分析：每轮将自生成测试运行在标准实现及其变异体上，跟踪通过率、行覆盖率和变异分数。

<div class="result-value" markdown="1">

作者报告三项测试质量指标随迭代总体提高；DeepSeek在三项指标上持续保持较高水平，GPT稳定改善，Qwen起点相对较低但仍呈正向趋势。原文片段未提供图5的坐标数值，无法量化每项指标的变化。

</div>

测试通过率上升表示模型逐渐删除错误断言或修正不匹配预期，覆盖率上升表示测试触达更多实现逻辑，变异分数上升表示测试更可能识别被扰动的错误实现。三项指标共同改善，比只观察代码通过率更直接地支持“测试也是被迭代优化的推理产物”。不过相关趋势不能单独建立因果关系，也不保证测试覆盖了仓库真正要求的全部行为，失败分析仍发现大量内部一致但外部错误的情况。

<div class="result-source" markdown="1">

来源：第4.3节，图5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The results show that all three metrics generally improve as the number of iterations increases.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 证据完整性有限：所给材料缺少表1、图3至图6的具体坐标或完整统计，且未报告置信区间、显著性检验、LiveCodeBench与RepoEval的样本规模和切分。因此可以确认作者报告的方向性趋势及表4消融数值，但不能充分判断提升的统计稳定性、难度分层表现或数据污染风险。
- 自生成测试仍可能形成错误的闭环验证。多数失败中代码已通过自生成测试却未通过仓库保留测试，说明联合修订可以提高测试覆盖和变异检测能力，却不能保证测试规格与真实需求对齐；此外，实验仅覆盖三种模型、Python仓库场景和给定迭代预算，对其他语言、模型规模、代理工具链及成本约束的外推仍需额外验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- CoT：先生成自然语言推理再编写代码，用于比较测试优先推理与一般链式思维提示的差异。
- SCoT：用程序结构组织推理步骤后再生成代码，用于检验收益是否仅来自更结构化的推理过程。
- Self-Planning：先制定子任务计划，再依据计划生成代码，用于比较“规划后实现”与“测试后实现”两种前置推理载体。
- ICoT：先提炼任务意图，再据此生成代码，用于判断显式测试是否比抽象的意图识别更能约束最终实现。仓库级消融中的Vanilla、Reflect、Single-track和TDD-Agent-iter1属于组件变体，另在消融字段说明。

**实验想回答的问题**

- 测试优先推理是否具有跨任务层级和跨模型的一致收益：在函数级任务中，仅要求模型先设计测试再实现代码，能否优于其他提示式推理方法；在仓库级任务中，加入可执行测试与迭代反馈后，能否进一步提高实现通过率？
- TDD-Agent的收益来自哪些机制：测试优先生成、执行反馈、代码迭代和测试迭代是否都不可替代；随着迭代推进，模型何时停止、生成测试的有效性如何变化，以及失败主要由错误归因还是不完整测试导致？

**实验实现**

实验覆盖GPT-5-mini、DeepSeek-V3.2和Qwen3-Coder-30B-A3B-Instruct三种模型。GPT与DeepSeek通过API调用，Qwen以vLLM部署在单张NVIDIA H20 GPU上；具体生成参数仅指向附录A，所给片段未展开。函数级TDD-prompt要求模型依次完成任务概述、设计3至5个含预期输出推导的测试、给出算法及复杂度、输出最终Python实现；每题生成10个样本，以减轻随机性影响。仓库级TDD-Agent可读取和搜索代码库、提交测试与实现、执行测试，并根据执行结果同时修订测试和代码，直至模型主动结束或达到迭代预算。分析还逐轮记录Match Rate与End Rate：前者表示当前代码通过当前自生成测试的任务比例，后者表示模型在该轮主动终止的任务比例。测试质量分析则把生成测试运行在标准实现上，测量通过率、目标函数行覆盖率和变异分数。原文指出性能约在第6至7轮接近平台，但片段未给出统一最大轮数、温度、仓库执行超时或重复试验置信区间。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 完整TDD-Agent与Vanilla、Reflect、Single-track和TDD-Agent-iter1在RepoEval上的总体比较。 | 完整TDD-Agent在GPT、DeepSeek和Qwen上的通过率分别为78.24%、90.77%和59.34%，均为各模型最佳。相较Vanilla的68.35%、73.63%和52.97%，绝对提升分别为9.89、17.14和6.37个百分点。 | Vanilla同时移除测试生成和迭代，Reflect只保留代码自反思，TDD-Agent-iter1只执行一轮测试优先生成，Single-track则固定首轮测试、只更新代码。完整方法同时超过这些变体，支持测试优先、执行反馈以及测试与代码双轨修订具有互补作用。尤其是完整方法相对Single-track的优势说明，初始测试可能错误或不完整，冻结测试会让代码被不可靠规格牵引。不过多个组件同时变化的比较不能单独精确分配每个组件的因果贡献。 | 表4，TDD-Agent行<br><span class="experiment-evidence">TDD-Agent 78.24 90.77 59.34</span> |
| Single-track与完整TDD-Agent的对照，用于隔离迭代过程中是否允许修订生成测试。 | Single-track在GPT、DeepSeek和Qwen上的通过率分别为70.11%、79.56%和57.36%；完整TDD-Agent分别达到78.24%、90.77%和59.34%，即允许测试随代码共同演化后绝对提高8.13、11.21和1.98个百分点。 | 两种设置都采用测试优先并利用可执行测试反馈，关键差异是Single-track冻结初始测试，而完整方法可以同时改测试与代码。因此该差距是支持“双轨修订”最直接的消融证据：模型可以修复幻觉断言、补充遗漏路径，再用更可靠的反馈指导代码。但三种模型的增益差异较大，尤其Qwen提升较小，说明该机制的效果依赖模型能否正确诊断测试和实现各自的问题。 | 表4，Single-track行；完整方法数值见同表TDD-Agent行<br><span class="experiment-evidence">Single-track 70.11 79.56 57.36</span> |

**定性案例**

- 失败类型分析显示，多数失败属于matched failures：终止时实现能够通过模型自己生成的测试，却无法通过仓库保留测试。作者将其解释为“假阳性验证”，即测试与实现共同演化成内部一致状态，但测试没有表达完整或正确的仓库需求。换言之，反馈循环只能修复当前测试能暴露的缺陷；若需求理解一开始就遗漏关键行为，代码和测试可能互相确认同一个错误。原文还称错误信用分配情形少于失败案例的10%，但所给片段未提供各模型精确比例或图6数值，因此该定量结论仍需核对附录C。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：论文以测试驱动的方法增强代码生成中的推理与验证过程，核心贡献属于 LLM 代码推理。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`8e438e9d9b422226b1fa75584666337bce02854ca8f8c49ed2492a178d56e439`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
