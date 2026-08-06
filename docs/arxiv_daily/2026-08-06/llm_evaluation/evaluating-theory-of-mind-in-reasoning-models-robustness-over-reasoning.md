---
title: "[论文解读] Evaluating Theory of Mind in Reasoning Models: Robustness over Reasoning"
description: "[arXiv 2608.04646][LLM 评测] 本文研究推理型大语言模型在心智理论任务中的表现，重点检验其优势究竟来自更强的心智理论能力，还是来自面对提示词和任务变化时更稳定地找到正确答案。"
arxiv_id: "2608.04646"
announcement_date: "2026-08-06"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:52:59.030969+00:00"
source_sha256: "176472b3b9f77aebe6b53b965c9722f5c6a19b840607c416c8560731856ad88a"
tags:
  - "LLM 评测"
  - "LLM 其他"
  - "LLM Reasoning"
  - "大语言模型"
  - "心智理论"
  - "推理模型"
  - "思维链"
  - "可验证奖励强化学习"
  - "提示稳健性"
  - "错误信念测试"
  - "机器心理实验"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.04646</p>

# Evaluating Theory of Mind in Reasoning Models: Robustness over Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Ian B. de Haan, Peter van der Putten, Max van Duijn</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> LIACS, Leiden University, The Netherlands</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04646v1) · [PDF 下载](https://arxiv.org/pdf/2608.04646v1) · **关键词** 大语言模型, 心智理论, 推理模型, 思维链, 可验证奖励强化学习, 提示稳健性, 错误信念测试, 机器心理实验<br>


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

本文研究推理型大语言模型在心智理论任务中的表现，重点检验其优势究竟来自更强的心智理论能力，还是来自面对提示词和任务变化时更稳定地找到正确答案。

**不用术语来说**：语言模型在测试中答对涉及他人信念、意图和愿望的问题，并不一定意味着它真正具备了相应的社会认知能力。尤其是经过强化学习、能够在回答前进行较长推理的模型，可能只是更擅长处理不同的题目表达方式。本文因此试图区分两种解释：模型是否获得了专门的心智理论能力，或者只是提高了在题目变化下保持正确答案的稳定性。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 使用既有的心理学心智理论测试评估近期推理型模型，并比较启用推理与不启用推理时的行为差异。
- 引入保持任务含义不变的提示词变体和任务扰动，考察模型在不同表达和呈现方式下的稳健性，并结合既有基准结果分析性能提升的可能来源。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型社会认知评测与推理模型分析的交叉领域。核心问题是：模型能否根据角色各自获得的信息，追踪其信念、意图和愿望，并据此预测角色的判断或行动，即表现出心智理论（Theory of Mind, ToM）行为。由于仅凭模型结构难以预测实际行为，论文采用类似心理实验的行为评测方法。当前推理模型通常经由可验证奖励强化学习训练，在回答前生成较长的思维链；它们在多类基准上优于普通模型，但已有研究指出，这种优势可能只是更有效地找到基础模型原本就能给出的答案。因此，ToM 得分提高不能直接证明模型获得了新的社会认知能力，还必须考察其在保持任务含义不变的提示改写和任务扰动下是否稳定。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**心智理论（Theory of Mind, ToM）**

指归因并持续追踪自己或他人的信念、意图、愿望等心理状态，再利用这些状态预测行为的能力。有效的 ToM 任务通常要求区分角色的心理状态与客观现实，并排除仅靠表面线索或更简单过程即可答对的情况。

</div>
<div class="concept-item" markdown="1">

**错误信念测试（false-belief test）**

测试中的角色掌握过时或错误的信息，因此其行动应由该角色相信的世界状态决定，而不是由读者已知的真实状态决定。模型只有区分“现实是什么”和“角色认为现实是什么”，才能稳定回答这类问题。

</div>
<div class="concept-item" markdown="1">

**推理模型与思维链（reasoning model and chain of thought）**

推理模型通常通过可验证奖励强化学习进行训练，在输出最终答案前生成一段中间推理文本，这种增加测试时计算量的方式属于推理时扩展。思维链可能帮助模型搜索答案，但不应被直接视为其真实内部推理的完整记录。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是心理学 ToM 测试或既有 ToM 基准中的自然语言情境、问题及其提示变体；情境通常描述多个角色看到或不知道的信息，并要求模型判断某个角色的信念、目标或后续行为。研究比较开启推理能力的模型与相应非推理模型，既考察标准提示下答案是否正确，也考察在不改变任务语义的措辞变化及任务扰动下，正确答案能否保持稳定。输出包括模型答案及跨变体的表现差异；关键假设是，若推理模型主要提高的是稳健性，那么优势应尤其体现在容易因提示变化而失败、或会严厉惩罚不一致回答的评测设置中，而不必解释为一种全新的 ToM 专属能力。本文只分析可观察行为，并采用工具主义立场：模型“像是”具有某种能力与“真正”具有该能力在实验操作上不作区分，也不据此提出模型具有主观心理状态的强结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$k$**

ToM 推理的阶数，即解决任务所需递归嵌套的心理表征层数。

</div>
<div class="notation-item" markdown="1">

**$x$**

一个 ToM 测试实例，包括自然语言情境、角色信息与待回答问题。

</div>
<div class="notation-item" markdown="1">

**$p$**

呈现测试实例时使用的提示版本；不同版本可以改变措辞，但应保持任务语义不变。

</div>
<div class="notation-item" markdown="1">

**$\hat{y}$**

模型针对测试实例输出的预测答案。

</div>

</div>

**直接相关的工作**

- **Ullman（文献 [21]）关于 GPT-3 心智理论测试脆弱性的研究**: 该研究发现，看似微小的提示改动会使原本通过 ToM 测试的 GPT-3 失败，并据此质疑其是否掌握了任务背后的原则。本文沿用这一机器心理实验思路构造保持任务含义的提示变体，但将研究对象扩展到推理模型，并把跨变体稳定性作为区分 ToM 专属能力与一般稳健性提升的关键证据。
- **文献 [7] 在 FANToM、BigToM、MMToM-QA 与 ParaphrasedToMi 上的模型比较**: 该工作直接报告了若干推理模型及非推理模型在既有 ToM 基准上的结果，为本文自建实验之外提供第三方证据。论文特别关注 FANToM：该基准只有在某一问题类型的全部问题均答对时才计分，因此会严厉惩罚不一致；推理模型在此出现较大优势，与“推理训练提高稳定找到正确答案的概率”这一稳健性解释相符，但本身不能证明产生了新的 ToM 机制。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型正越来越多地用于社会互动和代理系统，用户也容易把类似人的意图和推理能力归因于模型。若心智理论测试中的高分会受到提示词形式、任务呈现方式或推理稳定性的影响，那么仅依据平均测试分数判断模型的社会认知能力，可能导致过度解释，并影响后续模型评估和系统部署。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **既有心智理论基准测试**：通过要求模型判断他人的信念、意图或愿望来测量心智理论行为。早期研究曾据此提出语言模型可能出现了某种心智理论能力，随后研究者又建立了更全面的基准，以减少单一测试带来的误判。
- **推理型语言模型与链式思考**：这类模型通过带有可验证奖励的强化学习训练，在给出最终答案前生成较复杂的推理过程；这种在推理时增加计算或步骤的做法，被称为推理时扩展。其目标是提高模型解决问题时的推理表现。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有心智理论评估通常关注任务的平均正确率，却较少系统检验同一任务在提示词改写或任务呈现扰动下是否仍能得到一致答案。因此，模型在某次测试中的失败可能反映的是对表达形式的敏感，而不一定意味着缺少任务相关能力。
- 推理型模型在多种基准上的表现有所提升，但这种提升是否代表更强的、特定于心智理论的推理能力仍不清楚。现有行为结果难以直接区分专门能力增长与更稳定地找到正确解题路径之间的差异，因而也不能仅凭高分或推理过程证明模型真正拥有心智理论。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚未解决的问题是：在控制任务含义基本不变的前提下，推理型模型相较于非推理型模型是否表现出更强的抗提示变化和抗任务扰动能力，以及这种稳定性是否足以解释其在心智理论评估中的进步。该缺口要求把正确率之外的稳健性纳入评估，并将结论限定为关于模型行为的证据，而不是关于模型是否真正拥有心智理论的直接证明。

</div>
<div markdown="1"><span>核心问题</span>

推理型语言模型在心智理论任务上的改进，主要反映了新的心智理论特定能力，还是反映了模型在提示词变化和任务变化下更可靠地到达正确答案的稳健性？

</div>
<div markdown="1"><span>作者直觉</span>

如果推理训练主要改善了模型寻找和保持正确解题路径的能力，那么模型的优势应当不仅体现在原始题目的正确率上，也应体现在题意不变但说法改变、任务呈现方式改变时仍能维持正确答案。相反，如果优势来自专门的心智理论能力，则应更直接地表现为对心理状态内容本身的理解，而不只是对输入形式变化的适应。比较这些条件，可以为两种解释提供行为层面的区分证据。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文采用行为评测方法，而不是训练新模型或对强化学习过程进行受控因果实验。研究者把 GPT-5、Claude、DeepSeek R1 和 Grok-3-mini 等推理型大语言模型作为被试，向它们呈现一组改编自人类心理学实验的心智理论（Theory of Mind, ToM）任务，再根据答案与推理解释是否正确进行评分。任务覆盖一阶与二阶 Sally-Anne 错误信念测试、Strange Stories、Imposing Memory，以及专门用于检验提示变化敏感性的简单 ToM 修改任务；这些修改任务依据既有研究中可使 GPT-3 失败的扰动原则重新编写，以降低题目原文进入训练数据所造成的污染风险。最终输出是各模型在不同任务和扰动条件下归一化到 $[0,1]$ 的行为得分，以及对其稳定性和错误模式的比较。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 选择模型并确定可比条件

研究者记录每个模型是否能关闭思考、是否返回完整推理或推理摘要、是否支持温度配置，以及再次提示时能否把先前推理保留在上下文中。Claude 同时在 thinking on 与 thinking off 两种条件下测试，形成论文中最接近同一系统内部对照的比较；其余模型则按接口允许的方式运行。

<div class="method-step__io" markdown="1">

**输入**：GPT-5、Claude、DeepSeek R1 和 Grok-3-mini 的公开模型接口，以及各接口允许控制的思考模式、温度和上下文设置。<br>
**输出**：一组带有明确接口条件的模型配置，以及 Claude 的有思考和无思考两个行为条件。

</div>

**直观理解**：这一步相当于先记录不同被试可使用哪些辅助工具。由于各公司的接口并不一致，比较结果只能说明这些可访问系统表现出了什么行为，不能直接证明某种训练方法导致了差异。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造心理学 ToM 测试与抗扰动任务

研究者复用既有心理学测试框架，并针对每一种已知提示修改原则重新撰写一道任务，而不是直接照搬公开论文中的原题。任务要求模型区分世界的真实状态与角色可获得的信息，并据此推断角色的信念、意图或行动；高阶题还要求递归追踪一个角色对另一个角色心智状态的表征。

<div class="method-step__io" markdown="1">

**输入**：2023 年基准研究中的经典及修改版一阶、二阶 Sally-Anne 测试，Strange Stories、Imposing Memory，以及既有提示扰动研究总结的失败原则。<br>
**输出**：包含经典题、修改题和新编扰动题的 ToM 测试集合。

</div>

**直观理解**：错误信念题的关键不是模型是否知道事实，而是它能否暂时放下自己的全知视角，按照故事角色实际看到或听到的信息回答。重新写题则类似于换掉例题表面的人名和情节，以检查模型学到的是可迁移规则还是训练材料中的固定答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行提示并收集答案与推理

研究者通过各模型接口提交测试，收集最终答案及接口提供的推理内容；当模型支持在后续轮次保留推理时，再提示会继续使用该上下文。Claude 的推理摘要被直接用于解释评分，而 GPT-5 的公开摘要在预试中被认为过滤较多，因此研究者额外询问其给出答案的理由。

<div class="method-step__io" markdown="1">

**输入**：模型配置和逐项 ToM 测试提示。<br>
**输出**：每个模型在每道题上的最终回答、可获得的推理或解释，以及相应运行条件。

</div>

**直观理解**：评分不只看模型是否碰巧选中正确选项，还检查它为什么这样回答。需要注意，公开接口返回的“思考摘要”不一定等同于模型内部完整计算过程，因此这些文本只能作为可观察解释，而不能被视为内部机制的直接记录。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分级评分与归一化

沿用参考研究的三级规则：推理错误计 $0$ 分；推理接近正确，或模型随后承认先前错误并给出适当解释，计 $1$ 分；答案与推理均正确计 $2$ 分。研究者对任务得分取平均后除以 $2$，将报告尺度统一映射到 $[0,1]$。

<div class="method-step__io" markdown="1">

**输入**：每道测试的标准答案、模型最终答案，以及模型给出的推理或后续解释。<br>
**输出**：可跨模型、任务及思考条件比较的归一化表现分数。

</div>

**直观理解**：该规则把“完全错误”“部分理解或成功纠错”和“答案及理由都正确”区分开来。除以 $2$ 只是在不改变模型排序的前提下，把满分从 $2$ 改写为更直观的 $1$。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 归一化 ToM 评分

$$
S_{m,T}=\frac{1}{2N_T}\sum_{i=1}^{N_T} r_{m,i},\qquad r_{m,i}\in\{0,1,2\}
$$

**符号说明**

- $S_{m,T}$：模型 $m$ 在任务集合 $T$ 上归一化后的平均得分，取值范围为 $[0,1]$。
- $N_T$：任务集合 $T$ 中被计分的测试项目数量。
- $r_{m,i}$：模型 $m$ 在第 $i$ 个项目上的原始等级分：推理错误为 $0$，接近正确或适当自我纠错为 $1$，答案与推理均正确为 $2$。
- $m$：接受测试的模型或模型运行条件，例如 Claude thinking on 或 thinking off。
- $T$：某一心理测试、修改任务或其汇总集合。
- $i$：任务集合中的测试项目索引。

<div class="equation-explanation" markdown="1">

**直观理解**：论文原文用文字规定“平均原始分除以 $2$”，这里将其忠实写成求和形式：先把各题的 $0$ 至 $2$ 分求平均，再除以 $2$。该变换只统一报告尺度，不会训练模型，也不会改变同一任务内由原始平均分确定的相对高低。<br>
**原文位置**：第 3.3 节 Scoring；原文未给出编号公式，而是文字说明所有结果通过将平均得分除以 2 归一化到 [0,1]。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文没有训练、微调或优化任何模型，也没有提出新的损失函数；RLVR 只是被研究模型的背景属性，而不是本文实施的训练阶段。研究目标是进行行为评测：观察推理型模型在 ToM 题目及其提示、任务扰动下是否表现得更稳定。由于研究没有同时控制基础模型、RLVR 训练、供应商接口和推理预算，所得证据不能识别 RLVR 的独立因果效应。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 多类型 ToM 心理测试套件**

测试套件同时覆盖错误信念推断、较复杂社会故事理解、记忆负荷与递归心智状态追踪。Sally-Anne 类题要求区分真实世界状态与角色信念；高阶任务要求追踪嵌套表征，例如某角色认为另一角色相信什么，从而检验不同层次的心智状态归因。

> 直观理解：单一题型可能被关键词或固定模板破解，因此需要从多个角度检查同一种能力。不同测试共同判断模型是否能持续区分“事实是什么”和“故事人物以为什么”。

**2. 提示与任务扰动模块**

该模块依据既有研究中导致 GPT-3 在简单 ToM 任务上失败的修改原则生成新任务，用表面形式或情境条件的变化测试行为稳定性。新编题避免直接复用公开原题，但论文也承认，语义结构与模型关于 ToM 测试的元知识之间仍可能存在伪相关。

> 直观理解：标准题答对可能只是因为模型熟悉题型；扰动后的题更像压力测试。如果内容本质相同但措辞或情境稍变就失败，模型的成功便不够稳健。

**3. 答案与解释联合评分器**

评分器以最终答案和解释质量为共同依据，采用 $0$、$1$、$2$ 三级分值，并允许正确的自我纠错获得部分分。对会展示推理的模型，直接使用可获得的推理文本；对推理摘要不足的 GPT-5，则通过后续提示索取理由。

> 直观理解：只看答案无法区分真正跟踪角色信念与偶然猜中，因此还要核对理由。部分分则保留模型接近正确或能够发现并修正错误的信息。

**训练与推理**

整个流程仅发生在推理与离线评估阶段。推理时，研究者把每个心理测试提示提交给模型，并按接口能力收集最终答案和推理内容；Claude 分别以思考开启和关闭运行，支持温度设置的模型使用温度 $0$，支持保留推理上下文的模型在再次提示时保留该上下文。对于仅返回摘要的系统，Claude 的摘要用于评分，而 GPT-5 因摘要信息不足被额外询问答案理由。离线评估时，人工或配套评分工具依据统一的 $0/1/2$ 规则判断答案和解释，再汇总并归一化。论文公开了提示类、原始与已评分数据、实验脚本、命令行评分工具和分析笔记本，但所给节选没有提供仓库的文字 URL。

**复现信息**

公平解释结果所必需的设置包括：支持温度控制的 DeepSeek R1 与 Grok-3-mini 将温度设为 $0$，以减少重复运行的随机差异；GPT-5、DeepSeek R1 与 Grok-3-mini 的思考模式始终开启，只有 Claude 可以完全关闭思考；GPT-5 和 Claude 主要返回可能经过接口过滤的推理摘要，而 R1 与 Grok-3-mini 返回完整推理；GPT-5 与 Claude 可在再次提示时接收先前推理作为上下文，R1 与 Grok-3-mini 不支持该方式。以上差异会同时影响可复现性、解释文本质量和模型表现，因此不能把跨模型分数差异简单归因于架构或 RLVR。另一个关键限制是 Claude thinking off 并非 Claude 推理模型对应的基础模型，只是同一公开系统关闭思考后的运行状态；它能提供有价值的内部行为对照，却不能替代 RLVR 模型与其 base model 的严格比较。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Sally-Anne错误信念测试：包括一阶版本SA-1和二阶版本SA-2，每个推理阶次包含3个故事，其中2个由经典任务改写而来。它主要检验模型能否区分现实状态与角色的错误信念，并在二阶任务中追踪“一个角色如何理解另一个角色的信念”。原文未明确报告数据划分，也未完整报告总样本数。
- Strange Stories与Imposing Memories心理实验：前者覆盖谎言、假装、笑话、善意谎言、误解、讽刺和双重诈唬7类社会情境，测试模型能否从话语和情境推断非字面意图；后者同时设置意图性问题与记忆问题，并包含不同阶次的心理状态嵌套，用于区分心理状态推断困难和单纯事实回忆困难。原文未明确报告训练、验证或测试划分及完整样本规模。
- 简单提示修改任务：由既有心理理论任务的多种扰动版本组成，表6列出1A.1至2C.2共14种设置。其作用不是测试模型能否识别熟悉模板，而是检查任务表述、场景结构或干扰因素改变后，正确推理路径是否仍然稳定；其中2A和2B被作者视为尤其依赖场景表征的困难修改。各修改的精确定义位于补充材料，当前节选未提供。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**样本平均任务得分**

表3至表6按模型和任务类别报告样本平均分，用于概括答案及其相关推理是否满足任务判定。表中出现0.00、0.50和1.00等值，但当前节选没有完整说明部分得分的评分规则、评审者或一致性检验。 （越高越好，因为高分表示模型在更多样本中给出被判定为正确的答案及适当理由。）

</div>
<div class="metric-item" markdown="1">

**意图性问题与记忆问题的错误对比**

比较Imposing Memories中需要心理状态推断的问题和主要依赖事实恢复的问题，以分析错误是否集中在心理状态嵌套，而非笼统归因于阅读或记忆失败。 （两类问题均是错误越少越好；二者差距本身是诊断信号，不能直接当作独立性能分数。）

</div>
<div class="metric-item" markdown="1">

**扰动鲁棒性**

观察模型在14种修改任务上是否仍能保持正确表现，并重点检查提示或场景变化是否导致推理路径失稳。论文主要通过逐设置得分及与早期GPT-3结果的比较来判断鲁棒性，没有在当前节选中定义单一汇总鲁棒性指标。 （跨越更多修改仍保持高分时更好，因为这意味着结果较少依赖固定措辞、熟悉模板或脆弱启发式。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 一阶与二阶Sally-Anne错误信念测试

<div class="result-value" markdown="1">

SA-1上5种模型的平均得分均为1.00；SA-2上Claude、R1、Claude关闭thinking和GPT-5-high均为1.00，Grok-3-mini为0.67。唯一明确描述的失败是Grok-3-mini合并两个角色的知识，忽略了角色之间不同的心理状态。

</div>

这说明当前模型在结构清晰的经典错误信念题上通常能追踪一阶和二阶信念。然而，该结果不能证明模型形成了通用心理理论：三个故事仍共享Sally-Anne测试的基本语义结构，模型可能利用训练中见过的经典模板或表面相关性。接近满分也形成天花板效应，使该任务难以区分显式推理的贡献。

<div class="result-source" markdown="1">

来源：表3及第4.1节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

SA-2 1.00 1.00 1.00 1.00 0.67

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Strange Stories七类社会意图理解

<div class="result-value" markdown="1">

所有模型在谎言、假装、笑话、善意谎言和误解前5类上均为1.00；GPT-5-high在讽刺和双重诈唬上也均为1.00。其他模型的少量失分集中在讽刺和双重诈唬，最低类别得分为Claude关闭thinking在双重诈唬上的0.67。

</div>

结果表明，显式线索充分的非字面意图任务对这些模型总体较容易，GPT-5-high在本实验中覆盖了全部题型。困难案例并非完全不知道讽刺或双重诈唬概念，而是模型在多个合理解释之间选择了错误路径。由于整体表现接近饱和，实验不足以证明高分来自专门的心理理论机制，也不支持仅凭小幅分差给模型能力作稳定排序。

<div class="result-source" markdown="1">

来源：表4及第4.2节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The performance of the models in the first five strange stories categories, which involves understanding of, respectively, lies, pretend play, jokes, white lies, and misunderstanding, was flawless (Table 4).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 14种简单提示和任务修改

<div class="result-value" markdown="1">

新模型整体被作者判断为比文献[21]中的GPT-3更能应对修改任务，但2A和2B仍是共同失败点：Claude、R1、Grok-3-mini及Claude关闭thinking在2A.1、2A.2、2B.1和2B.2上均为0.00，GPT-5-high只在2A.1和2A.2上各得0.50，而在2B两项仍为0.00。

</div>

该实验比经典模板更有区分力：模型可以在许多措辞或结构变化后保持正确，却在可能需要形成空间或视觉场景表征的修改上系统失败。这支持“改进主要来自推理路径更稳定”的解释，但只是作者基于行为模式提出的说明；由于缺少GPT-3逐项结果、视觉表征的直接操控及统一鲁棒性统计量，实验不能单独确认失败的根因，也不能证明模型真正进行了人类式心理模拟。

<div class="result-source" markdown="1">

来源：表6及第4.4节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Two of these tasks, 2A and 2B, are nonetheless still particularly difficult for them (see Table 6).

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

- Claude关闭thinking：与同一模型的推理版本形成最直接的对照，用来考察显式推理或推理时计算是否改善心理状态追踪及抗干扰能力；由于两种模式仍可能存在解码和系统配置差异，该比较不能自动等同于严格的单变量因果消融。
- GPT-3既有研究结果：作者将修改任务上的表现与文献[21]中的GPT-3比较，以判断新模型相对早期通用语言模型是否更能承受任务扰动；当前节选没有给出GPT-3的逐项分数和完全一致的复现实验条件。
- Claude、R1、GPT-5-high与Grok-3-mini之间的横向比较：这些模型共同覆盖不同推理型系统，用于判断观察到的鲁棒性是否只属于单一模型系列。原文没有在当前节选中提供参数规模、推理预算或版本配置，因此横向排名需要谨慎解释。
- 记忆问题作为任务内参照：在Imposing Memories中，记忆问题主要要求恢复故事事实，而意图性问题要求追踪角色心理状态。两类错误的差异可帮助判断失败更接近事实读取问题还是心理状态推断问题，但题目难度并未严格配平。

**实验想回答的问题**

- 推理型大语言模型在一阶与高阶错误信念、复杂意图理解及受扰动任务上，是否能稳定识别角色的知识、信念和意图，而不是把客观事实误当作角色所知？
- 推理过程带来的优势是否主要体现为对提示变化、干扰信息和任务改写的鲁棒性提升，而非出现一种新的、专属于心理理论的能力？

**实验实现**

评测覆盖Claude推理模式、Claude关闭thinking、R1、GPT-5-high和Grok-3-mini；各表报告跨样本平均结果，并结合推理响应的人工定性检查分析成功与失败路径。Sally-Anne每个阶次使用3个故事；Strange Stories按7类社会情境汇总；Imposing Memories分别考察意图性与记忆问题；修改任务按14种设置逐项报告。定性分析关注模型是否先重组事实、主动区分角色视角、识别经典任务模板，以及是否出现多种解释间摇摆、答非所问或经重新提示后自我纠正。当前节选未明确报告采样次数、温度、最大生成长度、随机种子、推理预算、评分者数量、显著性检验方法及完整评分标准，因此表中均值的方差和复现稳定性无法判断。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Claude开启thinking与关闭thinking在Imposing Memories上的比较 | Claude推理版本正确率为100%，关闭thinking版本为92%，相差8个百分点；作者认为推理时扩展可能帮助模型仔细解析故事细节并将其与待判断陈述进行比较。 | 这是最直接检验显式推理价值的对照，结果说明额外推理在事实较多、需要嵌套追踪心理状态的故事中可能有帮助。但它只比较一个模型的两种运行模式，当前节选没有置信区间、重复运行或推理预算控制，因此不能确定8个百分点差距的统计稳定性，也不能将全部变化严格归因于某个单独组件。 | 第4.3节，Imposing Memories结果分析<br><span class="experiment-evidence">The thinking version of Claude performed slightly better than its non-thinking counterpart (100% vs 92%).</span> |
| Claude开启thinking与关闭thinking在14种修改任务上的比较 | 根据表6逐项结果，Claude推理版本在14项中的平均得分为0.71，关闭thinking版本为0.50；优势主要出现在多个1A、1B、1D和2C修改上，而两种模式在2A和2B四项中均为0.00。 | 该对照隔离的是推理模式与抗提示干扰表现之间的关联：推理模式改善了部分可通过整理文本和选择正确推理路径解决的修改，却没有解决2A、2B这类共同难点。因此，显式推理提高的是有限范围内的鲁棒性，而不是消除所有任务表征缺陷。0.71和0.50是依据表6的14项得分计算出的简单平均值，并非作者在原文中直接报告的汇总指标。 | 表6及第4.4节；平均值依据表6逐项结果计算<br><span class="experiment-evidence">Additionally, it’s possible to verify that the reasoning version of Claude performed significantly better in these tests than its non-thinking counterpart.</span> |

**定性案例**

- 讽刺故事中，父亲看到儿子打扫厨房时面粉落下并弄乱现场，却说“Wow, everything is so clean now!”。Claude和Grok-3-mini都在推理中考虑过讽刺解释，最后却假设父亲只看见已清洁区域、尚未发现混乱。该案例说明模型拥有相关概念，也能生成正确候选解释，但缺乏稳定的场景约束来排除不太可能的替代解释；这更符合“推理路径选择不稳”而非“完全没有心理状态知识”。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作通过 Theory of Mind 任务和心理学实验评估推理模型的鲁棒性及能力解释。; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`176472b3b9f77aebe6b53b965c9722f5c6a19b840607c416c8560731856ad88a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
