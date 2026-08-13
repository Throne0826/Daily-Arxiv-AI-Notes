---
title: "[论文解读] OEIS Open: How many conjectures can language models turn into theorems?"
description: "[arXiv 2608.11941][LLM 评测] 本文提出以 Lean 形式化证明为判定标准的 OEIS Open 基准，用统一、可复现且较难受答案泄漏影响的评测，衡量通用语言模型能否自主证明或否证尚未解决的数学猜想。"
arxiv_id: "2608.11941"
announcement_date: "2026-08-13"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:51:20.687226+00:00"
source_sha256: "668cbcda6269d3d94f934ec4791313cf3403bd46468bd06d39a612dcc827d01d"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "开放数学猜想"
  - "语言模型"
  - "形式化定理证明"
  - "Lean"
  - "OEIS"
  - "整数序列"
  - "数学推理基准"
  - "机器核验"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.11941</p>

# OEIS Open: How many conjectures can language models turn into theorems?

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Tom Adamczewski</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11941v1) · [PDF 下载](https://arxiv.org/pdf/2608.11941v1) · **关键词** 开放数学猜想, 语言模型, 形式化定理证明, Lean, OEIS, 整数序列, 数学推理基准, 机器核验<br>
**代码**: [https://github.com/epoch-research/LeanOpenProblems](https://github.com/epoch-research/LeanOpenProblems) · **项目页**: [https://github.com/epoch-research/LeanOpenProblems-results](https://github.com/epoch-research/LeanOpenProblems-results)

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

本文提出以 Lean 形式化证明为判定标准的 OEIS Open 基准，用统一、可复现且较难受答案泄漏影响的评测，衡量通用语言模型能否自主证明或否证尚未解决的数学猜想。

**不用术语来说**：已有报道表明 AI 偶尔能解决开放数学问题，但这些案例通常没有公开全部尝试过的问题、人与模型的完整交互和失败成本，因此无法判断成功究竟来自模型本身、专家引导还是问题筛选。本文要把这种零散展示转化为受控评测：给不同模型同一批尚无已知答案的猜想，限制预算和工具，并要求提交可由证明助手机械检查的完整证明。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者构建 OEIS Open：从 OEIS 整数序列猜想中选取 492 个已在 Lean 中形式化的开放猜想，并允许模型证明原命题或其否定，从而覆盖真假尚不确定的任务。
- 作者发布可用于通用语言模型的开源评测框架，以 Lean 内核统一验证结果，并据此比较模型、预算和代理配置，而不依赖每道题单独编写的验证程序。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于语言模型数学推理与形式化定理证明的交叉研究，目标不是展示少数成功案例，而是系统测量模型独立解决开放数学猜想的能力。开放问题尚无已知答案，因而较少受到训练语料答案泄漏的影响，但其评测必须同时解决“答案是否正确”和“真伪未知时如何验收”两个难点。本文采用已在 Lean 中形式化的 OEIS 整数序列猜想：模型可以证明猜想，也可以证明其否定；提交结果由 Lean 内核检查，从而把验收标准从数值证据或人工判断提升为机器可核验的形式证明。不过，该设置测到的是数学推理与 Lean 形式化能力的综合表现，并且只覆盖能够借助 Mathlib 现有定义或少量辅助定义准确表述的问题。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**开放数学猜想**

尚未获得公认证明或反例的数学命题。因为预先不知道命题为真还是为假，评测系统需要同时允许证明原命题与证明其否定。

</div>
<div class="concept-item" markdown="1">

**Lean 形式化证明与证明内核**

Lean 是证明助手，要求把命题、定义和推理步骤写成可由计算机检查的形式语言；其小型可信内核负责验证最终证明项是否符合逻辑规则。通过内核检查意味着提交的是演绎证明，而不只是实验或数值证据。

</div>
<div class="concept-item" markdown="1">

**生成器—验证器差距**

某些问题的答案对象很难找到，但给定候选对象后可以低成本地用程序检查，例如验证一个图、一个多项式或一种构造是否满足条件。该范式不适用于大量要求证明一般命题的问题，而且验证成功有时只能提供强证据，未必构成完整证明。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

基准 OEIS Open 的输入是 492 个来自 OEIS、此前仍属开放且已由 Tsoukalas 等人形式化为 Lean 陈述的整数序列猜想；OEIS Open Lite 则是其中随机抽取的 100 题低成本子集。对每个问题，通用语言模型在给定工具和计算预算下生成 Lean 证明，合法输出可以是原猜想的证明，也可以是其否定的证明，最终由 Lean 内核验收。该任务假设形式化陈述忠实反映原始猜想，并依赖 Lean 的公理基础、Mathlib 中可用的定义与定理；若命题独立于该公理基础，则原命题及其否定都可能不可证明。评测因此能够统计固定问题集合上的成功率与求解成本，但结果不能被直接解释为纯粹的非形式化数学能力，也不能代表所有研究数学问题。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N=492$**

OEIS Open 中形式化开放猜想的总数。

</div>
<div class="notation-item" markdown="1">

**$N_{\mathrm{Lite}}=100$**

OEIS Open Lite 随机子集中的猜想数。

</div>
<div class="notation-item" markdown="1">

**$C$**

某一道以 Lean 形式语言陈述的 OEIS 猜想。

</div>
<div class="notation-item" markdown="1">

**$\neg C$**

猜想 $C$ 的否定；模型证明它即可形式化地表明原猜想为假。

</div>

</div>

**直接相关的工作**

- **HorizonMath**: 包含 101 个开放问题，利用生成器—验证器差距检查闭式表达、优化结果或对象构造。本文将其作为对照：该方案覆盖不了多数要求一般性证明的问题，部分验收结果也只是数值证据，并依赖额外过滤规则避免硬编码等取巧行为。
- **FrontierMath: Open Problems（FM:OP）**: 包含 50 个由研究数学家提供的问题，并为每题编写专用验证程序。本文指出这种逐题验证器成本较高、可能出现误判，而且只能确认给出的对象有效；OEIS Open 改以统一的 Lean 内核检查证明，并允许通过证明否定来解决错误猜想。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

研究者需要判断语言模型是否已经具备推进数学研究前沿的能力，而不是只会解决训练语料中可能出现过、答案已知的难题。要作出这一判断，评测必须同时记录模型面对的完整问题集合、成功率、计算成本和人类介入程度，并确保所谓“解答”是严格成立的证明。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **开放问题个案展示**：研究团队挑选开放数学问题，让 AI 在可能包含专家提示与多轮交互的流程中寻找证明或反例，再公布少数成功案例。这类工作能展示能力上限，却通常没有公开所有尝试、失败记录和完整交互。
- **基于生成器—验证器差距的开放问题基准**：HorizonMath 和 FrontierMath: Open Problems 要求模型生成图、算法、多项式或闭式等具体对象，再由数值检查或专门编写的程序低成本验证。其核心条件是答案虽然难找，但候选对象容易通过计算检查。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 个案展示没有披露尝试问题的总体范围，也未充分公开专家提示与交互，因此无法可靠估计成功率、平均成本、人类贡献或不同模型之间的相对能力。
- 生成器—验证器方法只适用于能提交可计算对象的少数问题，难以覆盖要求证明一般命题的大部分研究数学；而且通过检查有时只构成数值证据，正确性还依赖人工验证代码与过滤器。若目标对象根本不存在，只允许提交正向对象的任务还可能天然无解。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种能够面向一般命题、接受证明与否证、以统一可信的机制判定严格正确性，并可在相同问题、预算和工具条件下复现比较通用语言模型的开放数学问题基准。

</div>
<div markdown="1"><span>核心问题</span>

在限制人类指导并统一评测条件后，当前通用语言模型能够以多高的成功率和成本，自主把一批此前未解决且已在 Lean 中形式化的 OEIS 猜想转化为可由内核验证的定理或反定理？

</div>
<div markdown="1"><span>作者直觉</span>

形式化证明把模型输出变成可机械核验的证明项：Lean 内核只接受类型正确且逻辑成立的推导，因此无需为每道题设计容易出错的专用验证器。允许模型证明猜想或其否定，又使错误猜想仍然可以通过严格反证得到解决；选择整数序列猜想则让自然语言含义与形式化陈述相对直接，有助于降低形式化偏离原意的风险。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文的方法不是训练新的定理证明模型，而是构建一套可让通用语言模型直接接受评测的开放式自动定理证明流程。输入是从 OEIS 开放猜想中筛选并用 Lean 4 形式化的 492 个目标；模型在隔离的工作环境中读取目标、编写和反复编译证明，可以选择证明猜想或证明其否定；最终提交物经过独立编译与内核级安全检查，只有确实证明指定命题且未引入非法公理的提交才计为解决。作者还用随机抽取的 100 题子集 OEIS Open Lite 支持较低成本的模型和代理配置比较。

从直观上看，这一方法把每道尚未解决的数学猜想变成一项“带自动裁判的编程任务”：语言模型可以自由试错，但不能修改正式题目，也不能用 `sorry`、额外公理或环境漏洞伪造成功。其主要研究对象是现成语言模型在固定工具、成本和时间约束下自主完成研究级证明搜索的能力，而不是某种专门证明算法的训练效果。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建并整理形式化猜想集

作者因技术原因排除 8 个目标，形成包含 492 个猜想、涉及 444 个不同 OEIS 序列的 OEIS Open，并随机抽取 100 个猜想构成 OEIS Open Lite。整数序列题主要使用整数与初等运算，其形式陈述通常较少依赖复杂的 Mathlib 定义链。

<div class="method-step__io" markdown="1">

**输入**：Tsoukalas 等人从 OEIS 的 2649 个开放猜想中筛选并自动形式化的 500 个 Lean 目标。<br>
**输出**：可由 Lean 4 检查的 492 题完整基准和 100 题低成本子集。

</div>

**直观理解**：这一步把自然语言猜想转换为计算机能够逐字核验的命题，并移除无法稳定运行的题目。Lite 子集相当于完整考试的随机缩略卷，用来降低多模型、多配置实验的成本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 补充来源与关注度元数据

作者用 GPT-5.5 将 Lean 命题匹配到对应的 OEIS 猜想文本，并识别提出者和首次出现日期；又合并 OEIS 条目中的外部链接与参考文献，以及三类 OpenAlex 全文检索结果，估计相关序列受到的文献关注。该关注度只描述序列被引用的程度，不能直接证明具体猜想曾被研究。

<div class="method-step__io" markdown="1">

**输入**：每个 Lean 猜想、对应序列的完整 OEIS 记录及修订历史，以及 OpenAlex 全文索引。<br>
**输出**：猜想的提出者、提出日期、匹配置信度及序列层面的文献关注度代理变量。

</div>

**直观理解**：这些信息不参与证明判定，而是帮助判断题目是否可能早已受到广泛关注，以及模型解决的是否大多是冷门问题。作者特别避免把“某篇论文提到该序列”误解成“该论文研究过这一猜想”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 语言模型迭代搜索证明或反例

基础代理采用 ReAct 式工具循环：模型分析当前目标，编辑 Lean 文件，通过命令行编译并读取错误或剩余子目标，再据此继续修改。目标被写成可编辑真值与猜想之间的等价关系，因此代理既可把真值设为 `True` 后证明原猜想，也可设为 `False` 后证明其否定，直至成功或耗尽费用、时间等限制。

<div class="method-step__io" markdown="1">

**输入**：单个 Lean 形式化目标、Lean 4 与 Mathlib 环境、命令行和文本编辑器，以及剩余预算信息。<br>
**输出**：候选 Lean 源文件，内容是对目标猜想或其否定的完整形式证明。

</div>

**直观理解**：模型像程序员一样反复“写证明、运行编译器、根据报错修正”，而不是一次生成最终答案。允许证明否定意味着找到严格验证的反例方向也算解决问题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 隔离编译与安全核验

每次尝试被分到互不联网的代理、编译和评分三个 Docker 容器：代理容器只输出源码，编译容器用干净工具链生成 `olean`，评分容器编译可信陈述并用 SafeVerify 比较两者。检查器要求目标声明的名称、种类和内核类型一致，依赖定义的主体一致，并从头通过 Lean 内核重放全部声明；除 `propext`、`Quot.sound` 和 `Classical.choice` 外不得依赖其他公理。

<div class="method-step__io" markdown="1">

**输入**：代理提交的 Lean 源文件，以及评分端保存的可信目标陈述副本。<br>
**输出**：“通过”或“拒绝”的可审计验证结论；通过者计为解决该猜想。

</div>

**直观理解**：模型所在环境即使被修改，也不能影响独立裁判使用的题目和工具链。裁判不仅检查代码能否编译，还确认它证明的正是原题，并排除 `sorry`、额外公理、恶意编译期代码和绕过内核等作弊方式。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文没有训练或微调语言模型，也没有提出需要优化的损失函数；它把现成通用语言模型视为黑箱推理器，在固定工具和资源限制下进行测试。代理运行中的直接成功条件是生成一个无未完成占位符、可编译且能通过 SafeVerify 或交叉检查器的 Lean 证明，评测层面再以已解决猜想数除以题目总数得到解决率。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 基础 ReAct 证明代理**

代理基于 Inspect 实现，仅提供 `bash`、文本编辑器和预算查询三种工具；运行环境包含 Lean 4、Mathlib、SageMath，以及带 `sympy`、`mpmath`、`numpy` 和 `pantograph` 的 Python。循环控制不预先规定证明策略，而是让模型根据 Lean 编译反馈自主选择演算、搜索和文件修改操作。

> 直观理解：该模块刻意保持简单，用最少的通用工具检验语言模型本身能否组织证明过程。数学软件可辅助探索规律或计算实例，但最终成果仍必须是 Lean 内核能够验证的证明。

**2. 三容器安全验证系统**

代理、编译和评分分别运行于无网络的 Docker 容器，只有代理生成的 Lean 源码进入干净编译环境，随后只有编译产物进入评分环境。SafeVerify 将提交与评分端自行编译的可信陈述比较，并在新内核中重放声明、核对目标类型和依赖定义、执行公理白名单检查；作者另用 Comparator 交叉检查 Claude Opus 4.8 的完整集提交。

> 直观理解：三层隔离把“寻找证明”和“决定证明是否有效”分开，使模型无法通过篡改本地 Mathlib、替换题目或攻击编译过程获得分数。它解决的是开放式智能体评测中最关键的可信计分问题。

**3. 文献访问与 DeepAgent 对照变体**

文献变体向代理提供截至 2022 年的 476000 篇纯数学 arXiv 论文的离线 LaTeX 源码；DeepAgent 变体则以 Inspect 的 `deepagent` 替换基础 ReAct 循环，加入子代理委派、持久记忆、待办事项工具和更长的指导性系统提示。两者保持形式目标和最终验证标准不变，用于单独检验知识访问与代理复杂度。

> 直观理解：这两个模块不是核心评分器，而是方法对照：前者测试“查阅大量数学论文是否有帮助”，后者测试“更复杂的任务管理和多代理协作是否有帮助”。保持同一裁判可以避免把验证宽松误当成能力提升。

**训练与推理**

仅涉及推理。对每个猜想独立启动无网络的代理容器，将形式化目标和工具接口交给待测模型；模型在 ReAct 循环中检查命题、编辑文件、调用 Lean 编译器或辅助数学软件，并依据错误信息继续修改。循环在产生完整证明、触及每题费用上限或达到最长 72 小时工作时间时终止；完整 OEIS Open 的主要设置为每题 50 美元，OEIS Open Lite 的高预算设置为每题 200 美元。成功提交随后在干净编译容器中生成 `olean`，再由独立评分容器对可信题目副本执行安全核验。完整集通常对每个模型运行一次；Lite 用于比较基础代理、文献代理和 DeepAgent 等配置。整个流程不把某题的中间状态共享给其他题，也不基于评测结果更新模型参数。

**复现信息**

复现时最关键的是固定 Lean 4、Mathlib、题目文件和验证器版本，并严格保留代理、编译、评分三容器边界；否则模型可能因环境差异或篡改评分依赖而获得不可比较的结果。每个容器均应禁用网络，评分端必须持有自己的可信陈述副本，不能直接信任代理提交的目标；只允许填补原陈述中的 `sorry`，目标声明与依赖定义必须保持内核级一致。资源控制需要同时记录每题货币支出和最长工作时间，并在不同模型间采用相同的成功定义。SafeVerify 是论文实验采用的主要检查器，但原文报告它在少数异常形式化和资源耗尽情形下与 Comparator 存在差异，因此后续复现应记录具体检查器及其裁决，并优先考虑作者计划采用的 Comparator。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- OEIS Open：包含 492 个来自 OEIS、由 Tsoukalas 等人形式化为 Lean 命题的开放猜想。它是完整评测集，用于比较通用语言模型与 AlphaProof Nexus；每个模型在每道猜想上运行一次，单题支出上限为 50 美元。
- OEIS Open Lite：从完整集合随机抽取的 100 个猜想，作用是降低多模型、多智能体变体和更高预算实验的成本。主要 Lite 实验将单题预算上限提高到 200 美元。
- arXiv 数学文献库：包含 476,000 篇论文，作为智能体可检索的外部知识源；它不是独立测试集，而是用于检验文献访问是否能提高 OEIS Open Lite 上的解决率。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**猜想解决率（accuracy / solve rate）**

被成功解决的猜想占评测集的比例。只有当模型提交原猜想或其否定命题的 Lean 证明，并通过验证时，才计为解决；因此该指标同时包含证明和证伪。 （越高越好，因为它表示在相同数据集与预算条件下，有更多形式化开放猜想获得了可验证的结论。）

</div>
<div class="metric-item" markdown="1">

**单题支出上限**

智能体在每个猜想上最多可调用模型和工具的美元预算；完整集使用 50 美元上限，Lite 主要实验使用 200 美元上限。它界定了比较模型时可使用的计算资源。 （它不是单向优劣指标；在解决率相同时越低越经济，而比较解决率时必须控制或明确预算。）

</div>
<div class="metric-item" markdown="1">

**解决时支出曲线**

对给定支出阈值，统计在达到该支出之前已经解决的猜想比例，用来估计不同预算上限可能对应的解决率。 （在相同支出阈值下曲线越高越好，表示模型以较少费用解决了更多猜想；但该曲线只是预算效果的近似，因为智能体预先知道总预算，行为可能随预算改变。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 完整 OEIS Open，492 个猜想，每题预算上限 50 美元

<div class="result-value" markdown="1">

作者报告 Claude Opus 4.8、GPT-5.5 和 Gemini 3.5 Flash 的解决率分别为 30%、26% 和 22%。其中 Claude Opus 4.8 解决约三成，是该设置下文中列出的最佳通用模型。

</div>

这说明通用语言模型在有限预算和形式验证约束下，能够自主完成相当数量的开放猜想证明或证伪，而不只是生成貌似合理的数学文字。它不表示模型解决了具有代表性的重大数学难题，也不能据此判断这些猜想的数学重要性或模型在其他研究问题上的成功率。

<div class="result-source" markdown="1">

来源：Section 3.1, Figure 1（右）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Claude Opus 4.8 resolved 30% of the 492 conjectures, GPT-5.5 resolved 26%, and Gemini 3.5 Flash 22% (Figure 1, right).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 完整 OEIS Open 上与专用系统 AlphaProof Nexus 比较

<div class="result-value" markdown="1">

AlphaProof Nexus 的论文报告结果为 44/492，即 9%；本文列出的三个通用语言模型均达到 22% 至 30%，因此按论文报告口径明显高于该专用系统。

</div>

该比较支持作者关于通用模型超过既有专用系统的主张，因为双方处理的是同一组 492 个形式化猜想，而且成本被描述为大致同量级。不过，这不是严格的同一基础设施下复跑：AlphaProof Nexus 的数字来自既有论文，其公开仓库仅发布 38 个 OEIS 证明，成本信息也部分来自私人通信，因此比较仍需核查评测与成本口径。

<div class="result-source" markdown="1">

来源：Section 3.1, Figure 1（右）及脚注 8–9

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

By comparison, Tsoukalas et al. 2026 report that their system, AlphaProof Nexus, resolved 44 of the same 492 conjectures (9%), at a similar cost to our result.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### OEIS Open Lite，100 个猜想，每题预算上限 200 美元

<div class="result-value" markdown="1">

不同语言模型解决 29% 至 44% 的猜想，其中 Claude Fable 5 达到最高的 44%，Gemini 3.5 Flash 为区间下端的 29%。

</div>

在较小测试集和更高单题预算下，当前最佳模型可解决接近一半的猜想，显示增加可用推理资源后仍有进一步成功空间。但 Lite 只是随机抽取的 100 题，而且 Claude Fable 5 仅在 Lite 的基础智能体上评测，所以该结果不能直接证明它在完整 492 题上也会达到 44%，也不能把它与所有模型、所有智能体配置作完全对称的比较。

<div class="result-source" markdown="1">

来源：Section 3.1, Figure 1（左）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On OEIS Open Lite, with the cap raised to $200 per conjecture, language models resolved 29% (Gemini 3.5 Flash) to 44% (Claude Fable 5) of the 100 conjectures (Figure 1, left).

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

- AlphaProof Nexus：Tsoukalas 等人针对同一批 492 个猜想使用的专用智能体系统。它处理相同形式化命题，且作者称其单个已解决猜想的成本量级与本文实验相近，因此是完整 OEIS Open 上最直接的既有系统基线；但其论文报告 44 个解，而配套仓库仅公开 38 个 OEIS 证明，复现口径存在差异。
- Base agent：仅提供完成 Lean 证明所需的最小工具集，是 OEIS Open Lite 上比较不同语言模型能力的默认智能体，也是判断额外检索或复杂控制流程是否真正有增益的参照。
- 带数学文献访问的智能体：在基础流程上增加对 476,000 篇 arXiv 论文的访问，用于隔离外部文献知识是否帮助解决这些可能很少被研究的猜想。
- DeepAgent：比基础智能体使用更复杂的智能体循环，用于检验增加规划和迭代机制是否比简单流程带来更高准确率。

**实验想回答的问题**

- 通用语言模型配合最小工具集，能否在固定推理预算下自主证明或证伪 OEIS 中已形式化的开放猜想，并取得高于专用系统 AlphaProof Nexus 的解决率？
- 提高单题预算、接入数学文献检索或采用更复杂的智能体循环，是否能稳定提高猜想解决率？

**实验实现**

判定规则是形式验证而非自然语言判断：模型提交猜想本身或其否定命题的证明，且证明通过 Lean 验证，才算解决。Figure 1 将解进一步分成证明与证伪，并报告正负一个标准误差。完整 OEIS Open 上，各模型对每个猜想只运行一次，单题支出封顶 50 美元；OEIS Open Lite 将上限提高到 200 美元，并在可用时比较基础智能体、文献访问和 DeepAgent 三种变体。Figure 2 按猜想被解决时已经发生的支出绘制累计解决率；Lite 曲线在有数据时对三种智能体变体取平均。Claude Fable 5 和 GPT-5.6 Sol 只在 Lite 上以基础智能体评测，因而不能用于完整集或智能体变体间的全面比较。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| OEIS Open Lite：基础智能体与增加数学文献访问的变体比较 | 作者报告，接入数学文献没有影响 Lite 上的准确率；原文所给摘录未明确报告各变体的具体分数或差值。 | 该实验隔离了外部文献检索的作用：在其余流程相近时，允许智能体访问论文并未形成可观察的解决率增益。这说明这些题目的主要障碍可能不是无法找到相关论文，也可能是模型不能有效检索、吸收或转化文献内容；由于缺少具体分数、误差和逐题变化，不能进一步断言两种设置严格等价。 | Section 3.1, Figure 3, Appendix A.2<br><span class="experiment-evidence">Neither giving models access to the mathematics literature, nor using the more complex DeepAgent (Sections 2.4.1 and 2.4.2) affected the accuracy on Lite (Figure 3, Appendix A.2).</span> |
| OEIS Open Lite：基础智能体与更复杂的 DeepAgent 循环比较 | 作者报告，DeepAgent 没有影响 Lite 上的准确率；原文所给摘录未明确报告具体分数、差值或统计检验。 | 该对照旨在判断更复杂的规划与迭代控制是否是性能提升来源。没有观察到准确率变化，意味着在这些模型和预算下，增加智能体流程复杂度并未转化为更多可验证证明；这不等于所有复杂智能体设计都无效，因为结论只覆盖本文实现、Lite 子集和相应预算。 | Section 3.1, Figure 3, Appendix A.2<br><span class="experiment-evidence">Neither giving models access to the mathematics literature, nor using the more complex DeepAgent (Sections 2.4.1 and 2.4.2) affected the accuracy on Lite (Figure 3, Appendix A.2).</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces and applies a benchmark for evaluating language models on autonomous Lean-based theorem proving and mathematical reasoning.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`668cbcda6269d3d94f934ec4791313cf3403bd46468bd06d39a612dcc827d01d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
