---
title: "[论文解读] ReflectFact: Self-Reflective Agents for Improving Comprehension and Reasoning in Multi-Hop Fact Verification"
description: "[arXiv 2608.12877][LLM Agent] ReflectFact针对多跳事实核验中局部子任务偏离全局核验目标、模型参数知识压过给定证据这两类问题，引入逐步的自反思事后校验，在错误传递到最终判定前修正中间结果。"
arxiv_id: "2608.12877"
announcement_date: "2026-08-14"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T03:00:21.149288+00:00"
source_sha256: "4275d6c726a3aad7cac9d6e6eedc8b1b3f87572e3fa3786febfbdfa81b06736d"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "Multi-Agent"
  - "多跳事实验证"
  - "大语言模型智能体"
  - "证据落地推理"
  - "参数化知识"
  - "证据漂移"
  - "自反思验证"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.12877</p>

# ReflectFact: Self-Reflective Agents for Improving Comprehension and Reasoning in Multi-Hop Fact Verification

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Runze Zhao, Zixin Tang, Xiaoshuai Hao, Leyuan Chang, Xiaopeng Fu, Boyu Qiao, Dongyang Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Zhongguancun Laboratory；Institute of Information Engineering, Chinese Academy of Sciences</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12877v1) · [PDF 下载](https://arxiv.org/pdf/2608.12877v1) · **关键词** 多跳事实验证, 大语言模型智能体, 证据落地推理, 参数化知识, 证据漂移, 自反思验证<br>


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

ReflectFact针对多跳事实核验中局部子任务偏离全局核验目标、模型参数知识压过给定证据这两类问题，引入逐步的自反思事后校验，在错误传递到最终判定前修正中间结果。

**不用术语来说**：复杂声明通常不能靠一条证据直接判断真假，而要把多个事实连接起来；只要其中一次实体识别、证据理解或逻辑衔接出错，后续步骤就可能在错误基础上继续推理。现有智能体即使能分工完成这些步骤，也可能只顾当前任务是否完成，或凭模型记忆改写证据支持的内容，最终给出看似连贯但依据不足的结论。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者明确归纳了智能体式多跳事实核验的两类关键失效机制：局部子任务与全局核验目标之间的“目标冲突”，以及参数知识与给定证据之间的“知识冲突”。这一划分把错误来源定位到中间推理过程，而不只关注最终标签是否正确。
- 作者提出ReflectFact，将显式推理路径规划、证据漂移校验和推理反思校验结合起来：先形成由证据支撑的分步核验路径，再检查答案是否偏离证据，并从全局目标重新审视各推理步骤，以便在错误累积之前进行重生成和修正。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

多跳事实验证旨在判断一条声明是否真实，但结论不能由单条证据直接得到，而需要联合多段证据进行多步推理。该任务通常要求系统先识别声明涉及的实体和事实关系，再把复杂声明拆成可核查的局部问题，最后依据证据之间的逻辑联系给出判定；它比普通文本分类更强调证据覆盖、推理连贯性与结论的可追溯性。本文关注基于大语言模型智能体的方案：这类方案模仿人工核查流程，将实体解析、语义分解和逻辑推理交给若干连续步骤或专门智能体执行。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多跳事实验证**

系统必须组合多条证据并经过多个推理步骤，才能判断声明是否成立。“跳”表示从一个事实或实体关系转到另一个事实或关系。

</div>
<div class="concept-item" markdown="1">

**参数化知识与证据知识**

参数化知识是大语言模型从训练数据中内化的既有知识，证据知识则是当前任务明确提供的文本依据。当二者冲突时，事实验证系统应以给定证据为准，否则可能出现本文所称的证据漂移。

</div>
<div class="concept-item" markdown="1">

**智能体式事实验证**

智能体式方法把核查过程拆成实体识别、声明分解、证据理解和结论推导等连续子任务，并利用大语言模型逐步执行。其优势是流程接近人工核查且易于解释，但前序错误可能向后累积，局部子任务的目标也可能偏离最终验证目标。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是一条需要核验的复杂声明以及与之相关的多段文本证据，系统需要解决声明中的隐式实体指代，将复合语义拆成可分别核查的原子事实，并跨证据建立完整推理链，最终输出声明真实性的判定。本文假定证据是当前核验的依据，但大语言模型同时携带可能与证据不一致的参数化知识；因此，系统不仅要生成局部答案，还要检查每一步是否忠于证据、是否服务于全局判定。典型失败包括：实体解析虽然局部上找到了对应对象，却替换掉声明中对最终判定关键的矛盾信息；或者模型沿用自身先验而无依据地修改本来受到证据支持的声明。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **HoVer: a dataset for many-hop fact extraction and claim verification（Jiang et al., 2020）**: HoVer建立了多跳事实提取与声明验证的任务场景，也是本文用于评估复杂跨证据推理能力的数据集之一。所给章节未进一步说明其标签体系、证据组织方式或具体跳数构成。
- **EX-FEVER: a dataset for multi-hop explainable fact verification（Ma et al., 2023）**: EX-FEVER面向可解释的多跳事实验证，也是本文的第二个评测数据集，用于考察方法在另一种复杂核验场景下的适应性。所给章节未明确介绍其样本构造、标签定义及解释标注形式。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

社交媒体中的错误信息往往涉及多个实体、事件和关系，自动核验系统必须综合多条证据并完成多步推理。实际应用不仅要求最终结论正确，还要求结论确实建立在所提供的证据上；否则，系统可能把自身记忆或早期步骤中的错误包装成可信判断，削弱事实核验的可靠性与可审查性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **知识图谱与微调自然语言推断模型**：这类方法将声明、实体和关系组织为结构化依赖，或训练自然语言推断模型判断证据是否支持声明，借此捕捉多条事实之间的逻辑联系。它们提供了较明确的推断结构，但论文的研究重点并非改进这类模型，而是处理近期智能体工作流中的中间过程失效。
- **基于大语言模型的智能体式核验**：这类方法模仿人工核查流程，把完整核验任务拆成实体消解、声明分解、证据理解和结论推导等连续子任务，再由一个或多个智能体逐步执行。分工降低了单步任务的复杂度，但标准工作流通常缺少面向全局目标和证据一致性的逐步复核。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 目标冲突：负责某个子任务的智能体可能只优化局部正确性，而没有保留对最终真假判定有用的矛盾。例如，将描述性短语直接替换为实体名称虽然完成了实体消解，却可能掩盖描述中的错误年份。其后果是关键反证在预处理阶段被消除，使后续推理沿错误方向展开。
- 知识冲突：大语言模型的参数知识，即训练过程中记住的信息，可能与当前提供的证据不一致。智能体若优先采用自身记忆，就会出现“证据漂移”，即答案表面上回应了证据，实际却加入无证据支持的修改；这会破坏证据约束，使原本可由材料验证的声明得到错误判定。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有智能体方法能够拆解并顺序执行多跳核验，却缺少一种贯穿中间步骤的事后校验机制：它既要判断当前答案是否真正由给定证据支持，又要判断局部操作是否服务于整体核验目标，并在发现不一致时主动重做，而不是让缺陷继续传播到最终裁决。

</div>
<div markdown="1"><span>核心问题</span>

能否通过在多跳核验的证据理解与推理步骤之后加入自反思复核，使智能体同时抑制证据漂移和局部目标偏移，从而生成更可靠、可追溯的最终真假判定？

</div>
<div markdown="1"><span>作者直觉</span>

作者的出发点是，大语言模型检查一个已有答案是否与证据和任务目标一致，可能比一次性生成完全正确的推理更容易。因此，系统先显式列出实体、子问题和逻辑链，再要求模型引用证据重新回答可疑内容，并从最终核验目标回看每一步；这类似于解题后逐行验算，可把原本隐含且会累积的错误变成可定位、可重生成的中间结果。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ReflectFact面向多跳事实核验：输入待核验声明$c$及数据集提供的黄金证据集合$E=\{e_1,e_2,\ldots,e_n\}$，输出二元标签$y\in\{\mathrm{True},\mathrm{False}\}$。论文刻意不研究证据检索，而把重点放在证据已经给定时的理解与推理。整体流程先显式解析声明中的隐含实体，再把解析后的声明$c'$拆成可由证据逐项回答的子问题，最后整合中间事实得到标签；在此过程中，证据理解类步骤接受“证据漂移核验”，指令推理类步骤接受“推理反思核验”，以阻止局部错误沿多跳链条传播。

技术上，该方法把原本一次完成的判断改造成带有中间检查点的执行链：隐含实体解析负责确定“描述到底指谁”，语义分解负责确定“声明包含哪些必须分别成立的事实”，综合逻辑推理负责确定“这些已核实事实合起来是否支持声明”。通俗地说，它像一名先消除代词和描述歧义、再逐条查账、最后汇总判决的核验员；两个反思机制则分别检查回答是否真正来自眼前证据，以及推理操作是否正确执行了任务指令。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务输入与核验边界确定

将任务限定为基于全部相关证据进行多步推理，并判断声明受到支持还是被反驳；每条$e_i\in E$都参与支持或反驳，因此方法无需在开放语料中自行检索证据。

<div class="method-step__io" markdown="1">

**输入**：待核验声明$c$，以及从Wikipedia等大型文本语料构建、但在本文实验中由数据集直接提供的黄金证据集合$E=\{e_1,e_2,\ldots,e_n\}$。<br>
**输出**：统一的核验实例$(c,E)$，以及目标标签空间$y\in\{\mathrm{True},\mathrm{False}\}$。

</div>

**直观理解**：这一步相当于把核验材料完整交给系统，考查的是它能否读懂并串联材料，而不是能否先把材料找出来。因而实验结果不能直接解释为开放环境下“检索加核验”的整体能力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 隐含实体解析

依次执行定位$\mathcal{L}$、搜索$\mathcal{S}$和替换$\mathcal{R}$：先生成针对隐含描述的查询$Q_l=\mathcal{L}(c)$，再依据证据回答$A_l=\mathcal{S}(Q_l,E)$并识别具体实体$T'$，最后得到$c'=\mathcal{R}(c,A_l)$。搜索属于证据理解任务并接受证据漂移核验，定位与替换属于指令推理任务并接受推理反思核验。

<div class="method-step__io" markdown="1">

**输入**：原始声明$c$及证据$E$，其中可能含有由词序列$T=\{t_1,t_2,\ldots,t_m\}$构成的实体描述，而非明确实体名。<br>
**输出**：将隐含实体描述$T$替换为明确实体$T'$后的精化声明$c'$；若不存在隐含实体，则流程按提示报告该情况。

</div>

**直观理解**：例如，系统先问“录制《Make Them Gold》的乐队是哪一支”，从证据找出乐队名称，再把原声明中的描述换成该名称。这样后续步骤不必一边猜实体一边判断事实，可减少把正确证据接到错误对象上的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 语义分解与逐项证据作答

把$c'$的完整语义组成部分转写为子问题集合$Q_s=\{q_i\}_{i=1}^{n}$，并让LLM针对每个$q_i$仅依据给定证据生成答案$a_i$，汇总为$A_s=\{a_1,a_2,\ldots,a_n\}$。每个答案生成步骤均属于证据理解任务，因此使用无证据答案进行漂移筛查，必要时要求重新回答并逐字引用支撑片段。

<div class="method-step__io" markdown="1">

**输入**：精化声明$c'$及证据$E$。<br>
**输出**：覆盖声明各项关键条件的子问题集合$Q_s$，以及对应的、经过证据约束的中间事实集合$A_s$。

</div>

**直观理解**：若声明称两个对象“都是犬种”，系统会分别询问每个对象是否为犬种，而不是只凭整体印象回答。逐项核验使较长声明中的否定、并列条件或细粒度属性不容易被遗漏。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 综合逻辑推理与最终判决

把$c'$与$A_s$填入人工构造的思维链模板，引导LLM只根据已提供的中间内容逐步整合逻辑关系，并生成$y\in\{\mathrm{True},\mathrm{False}\}$。该整合属于指令驱动的推理任务，系统会验证输出是否与输入及全局事实核验目标一致；发现不一致时，携带错误反馈重新生成。

<div class="method-step__io" markdown="1">

**输入**：精化声明$c'$和已核验的中间答案集合$A_s$。<br>
**输出**：经过反思检查的最终核验标签$y$及其显式中间推理链。

</div>

**直观理解**：这一步不是再次查询外部知识，而是把前面核实过的事实拼成结论。它类似根据已经确认的若干前提完成最后的逻辑验算，并在提交判决前复查是否出现了错位替换、位置偏差或前后矛盾。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 证据漂移筛查与证据重锚定

$$
a^{p}=\mathcal{S}(q,\varnothing),\qquad a\equiv a^{p}\Rightarrow \hat{a}=\mathcal{S}(q,e,e^{*}),\quad e^{*}\subseteq e
$$

**符号说明**

- $q$：当前证据理解子任务的问题。
- $\mathcal{S}$：根据问题及可用上下文生成答案的搜索或作答操作。
- $e$：提供给模型的相关证据。
- $\varnothing$：不向模型提供外部证据，使其只能依赖参数记忆。
- $a$：在证据条件下生成的初始答案，可写作$\mathcal{S}(q,e)$。
- $a^{p}$：不提供证据时由模型参数记忆产生的答案。
- $\equiv$：两个答案在比较中收敛或等价，是触发进一步检查的条件，而非答案必错的充分条件。
- $e^{*}$：从证据e中选出的、必须逐字引用的支撑片段。
- $\hat{a}$：在原证据和明确支撑片段约束下重新推导的答案。

<div class="equation-explanation" markdown="1">

**直观理解**：该关系先用“闭卷回答”作为模型先验的参照。如果“开卷回答”与闭卷回答一致，方法认为存在模型只是复述既有记忆的可能，于是要求它引用证据中的具体文本并重答，以便把结论重新绑定到当前证据；这是一种保守触发规则，原文没有声称答案相同就必然发生了漂移。<br>
**原文位置**：Methodology，Evidence-Drift Verification小节

</div>

</div>

<div class="equation-block" markdown="1">

#### 推理反思后的条件重生成

$$
\hat{o}=\begin{cases}o,&\text{if }\mathcal{V}(x,o)=\text{consistent},\\ \mathcal{F}\!\left(x\mid\mathcal{V}(x,o)\right),&\text{otherwise}.\end{cases}
$$

**符号说明**

- $x$：推理子任务的输入，例如精化声明或中间答案集合。
- $\mathcal{F}$：被检查的推理操作；原文给出的范围包括定位、替换及其他整合操作。
- $o$：推理操作产生的初始输出，即$o=\mathcal{F}(x)$。
- $\mathcal{V}$：检查输入与输出是否一致、输出是否正确遵循指令的验证操作。
- $\mathcal{V}(x,o)$：验证结论，取值为consistent或inconsistent，并在不一致时提供可用于修正的反馈。
- $\mathcal{F}(x\mid\mathcal{V}(x,o))$：以验证器指出的不一致为附加条件，再次执行原推理操作。
- $\hat{o}$：通过验证后保留或经反馈重生成的最终输出。

<div class="equation-explanation" markdown="1">

**直观理解**：若检查器认为初始输出与输入一致，系统直接保留它；否则，系统把发现的问题交回生成操作进行有针对性的重做。核心设计是将生成与验证解耦，并通过明确的事实核验任务框架促使模型主动报告错误。<br>
**原文位置**：Methodology，Reasoning Reflection Verification小节，公式(1)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。所给章节没有提出新的参数训练目标、损失函数或梯度优化过程；ReflectFact是建立在现有LLM之上的推理时代理框架，通过提示、任务分解、证据引用和条件重生成改变执行流程。人工构造的思维链模板及动态示例选择用于组织推理上下文，不能据此视为模型训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 显式推理路径规划**

模块由隐含实体解析、语义分解和综合逻辑推理三个阶段组成，将端到端判断展开为$c\rightarrow c'\rightarrow(Q_s,A_s)\rightarrow y$。其中定位、搜索、替换分别承担描述识别、证据作答和实体回填，人工思维链模板则约束最终阶段只整合$c'$与$A_s$，避免额外引入未经核验的外部知识。

> 直观理解：多跳声明的难点往往不是某一个事实完全未知，而是多个事实必须按正确对象和顺序连接。显式路径让每个连接点都能被查看和复核，也使系统知道当前局部操作服务于哪个全局声明。

**2. 证据漂移核验**

该模块用于搜索与子问题作答等证据理解任务。对同一问题$q$，系统同时获得证据条件下的答案$a=\mathcal{S}(q,e)$和无证据的参数记忆答案$a^p=\mathcal{S}(q,\varnothing)$；若$a\equiv a^p$，系统不直接断言答案错误，而是将其标记为可能未真正使用证据，并要求模型引用支撑片段$e^*\subseteq e$后产生$\hat{a}=\mathcal{S}(q,e,e^*)$。

> 直观理解：有证据答案与模型原本就会给出的答案相同，并不能证明它确实阅读了证据，所以这里采用的是风险筛查而非错误判定。强制逐字指出依据，相当于要求核验员不仅报答案，还必须在材料中划出支持答案的原句。

**3. 推理反思核验**

该模块用于定位$\mathcal{L}$、替换$\mathcal{R}$和最终逻辑整合等指令推理任务。系统把输入$x$和初始输出$o=\mathcal{F}(x)$组成待审查对象，通过验证器$\mathcal{V}(x,o)$判断输出是否正确、一致地遵循输入，并显式提示这是事实核验任务、任何错误都必须报告；若判为不一致，则将验证反馈作为条件交给原操作$\mathcal{F}$重新生成。

> 直观理解：生成者容易顺着自己刚写出的内容继续推理，而检查者更适合寻找不一致，因此论文把“先做”与“再审”分开。反馈并非只给出失败标志，而是进入重生成上下文，使模型能针对已指出的问题修正结果。

**训练与推理**

训练阶段：原文所给方法章节未报告对基础LLM进行微调或额外训练，也未定义可学习参数及优化目标。推理阶段：对每个$(c,E)$实例，先由$\mathcal{L}$识别隐含实体描述并提出查询，再由$\mathcal{S}$基于$E$回答，随后由$\mathcal{R}$把明确实体写回声明形成$c'$；接着把$c'$分解为$Q_s$，逐题依据$E$产生$A_s$，最后将$c'$和$A_s$填入人工思维链模板并输出$y$。

两类检查机制嵌入相应子任务之后，而非只在末尾统一执行：证据理解输出会与无证据参数答案比较，命中风险条件时必须引用$e^*$重新回答；指令推理输出会被$\mathcal{V}$复核，只有一致输出才被保留，否则依据验证反馈重新执行。由此，送入下一跳的是$\hat{a}$或$\hat{o}$等已复核结果，目标是尽早截断错误传播；所给原文未明确报告反思或重生成的最大轮数。

**复现信息**

公平理解与复现时最关键的条件有三点。第一，方法直接使用数据集提供的黄金证据，因此性能主要衡量给定证据下的理解、分解与多跳推理，不包含检索召回错误。第二，隐含实体搜索和语义子问题作答的提示都把证据置于问题之前；最终提示明确要求判断$c'$为真或假，并把$A_s$作为逐步思考内容，限制最终阶段只整合已经得到的信息。第三，替换阶段采用动态样例选择来提供示范，综合阶段采用人工构造的思维链模板，反思提示则预置事实核验任务框架并要求报告任何错误或不一致。

所给章节未明确报告动态样例选择算法、提示示例数量、基础模型调用参数、答案等价$a\equiv a^p$的具体判定器、验证器是否与生成器共享同一LLM、重试次数、温度、随机种子或推理成本。这些因素可能影响漂移触发率和反思收益，完整复现时需要进一步核对论文其余章节或作者代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HOVER：基于英文维基百科构建的多跳事实核查数据集。实验使用包含4,000条声明的验证集；每条声明最多需要联合四篇维基百科文章中的证据，因而可按2-hop、3-hop和4-hop分别检验推理链加长时的性能变化。
- EX-FEVER：声明通过汇总并修改互相超链接的维基百科文档而构造，覆盖2-hop和3-hop推理。实验使用测试集，并为与HOVER的二分类设置一致而删除NEI（证据不足）标签，最终保留4,071条声明；该数据集还提供黄金文本解释，用于评价模型推理链的可解释性。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Macro-F1**

分别计算supported与refuted两类声明的F1后等权平均，兼顾精确率与召回率，并避免样本较多的类别主导总体评价。论文同时报告各跳数和数据集总体Macro-F1，以观察推理深度增加造成的退化。 （越高越好；更高表示模型在支持与反驳两类上的综合判别更均衡。）

</div>
<div class="metric-item" markdown="1">

**ROUGE-1与ROUGE-2**

分别衡量模型构造的思维链与EX-FEVER黄金解释之间的一元词组和二元词组重合程度，用于检验生成解释是否覆盖参考解释中的局部信息。 （越高越好；重合度更高通常说明生成推理链包含更多黄金解释表述，但不直接保证逻辑正确或因果忠实。）

</div>
<div class="metric-item" markdown="1">

**ROUGE-L**

基于最长公共子序列衡量构造思维链与黄金解释在内容及顺序上的匹配程度，比单纯词项重合更关注较长的序列结构。 （越高越好；更高表示解释与参考文本的序列一致性更强，但仍不能单独证明模型确实依据该推理过程作出裁决。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### HOVER与EX-FEVER总体Macro-F1：ReflectFact对比最强智能体基线

<div class="result-value" markdown="1">

作者报告ReflectFact在两个数据集上均取得最佳总体结果；相对最强智能体基线BiDeV，HOVER与EX-FEVER总体Macro-F1分别高3.32和4.10个百分点。

</div>

这说明在统一GPT-4o-mini骨干和禁止联网的条件下，仅依赖多智能体交叉验证仍不如对中间证据使用和推理步骤进行自我复核。该结果支持“后验证工作流有效”的作者主张，但节选没有给出Table 1完整分数、方差或显著性检验，因此不能判断提升的统计稳定性；此外，摘要所称EX-FEVER领先2.78%与实验正文的4.10%不一致，需回查原表。

<div class="result-source" markdown="1">

来源：Comparison with State-of-the-art Methods；Table 1相关正文

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Consequently, even the strongest agent baseline, BiDeV, still trails ReflectFact by 3.32% and 4.10% in overall performance on HOVER and EX-FEVER, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### HOVER 4-hop长链声明：ReflectFact对比智能体与直接调用大模型

<div class="result-value" markdown="1">

在HOVER最困难的4-hop设置中，BiDeV和StepByStepFV的Macro-F1分别为69.95%和69.87%，GPT-4o-mini为68.89%；作者进一步报告ReflectFact比最强智能体基线高3.79个百分点、比最佳直接大模型高4.85个百分点，据此可对应得到ReflectFact约为73.74%，且该值与Table 2完整模型的4-hop结果一致。

</div>

跳数增加意味着结论依赖更多证据和中间步骤，该结果直接测试反思机制能否减缓长链错误累积。ReflectFact在4-hop上的优势比简单设置更明显，支持显式规划与逐步复核适合复杂声明；但这只是在HOVER既定证据条件下的分类表现，不能证明模型能在开放网络中正确检索证据，也不能把收益完全归因于某一个模块。

<div class="result-source" markdown="1">

来源：Comparison with State-of-the-art Methods；Table 1相关正文

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Furthermore, ReflectFact demonstrates even more substantial improvements, outperforming the strongest agent-based baseline and Vanilla LLM by 3.79% and 4.85% on 4-hop claims, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### EX-FEVER黄金解释：构造CoT与参考解释的ROUGE匹配

<div class="result-value" markdown="1">

ReflectFact取得ROUGE-1 56.71、ROUGE-2 39.87和ROUGE-L 52.32；对照模型中MDR分别为54.88、41.34和49.42，BERT-based为46.88、32.80和35.52，GPT为52.28、33.74和48.13。ReflectFact在ROUGE-1与ROUGE-L上最高，但ROUGE-2低于MDR的41.34。

</div>

该实验测试中间CoT是否含有与人工最小充分解释相近的信息。结果表明ReflectFact在单词覆盖和较长序列匹配上更强，但并非所有解释指标都最好；特别是ROUGE-2落后于MDR。因此，更稳妥的结论是其推理链具有一定解释相关性，而不是已经证明解释忠实反映模型内部决策过程。

<div class="result-source" markdown="1">

来源：Table 3，Interpretability Analysis

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Rouge-1 54.88 46.88 52.28 56.71
Rouge-2 41.34 32.80 33.74 39.87
Rouge-L 49.42 35.52 48.13 52.32

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

- Vanilla LLM：包括Flan-T5、GPT-4o-mini和Qwen3。它们将声明与证据直接映射为裁决，不执行显式的智能体工作流，用来判断ReflectFact的收益是否只是来自强语言模型本身。
- NLI微调模型：ScandiNLI与DeBERTaV3-NLI分别基于自然语言推断数据进行专门微调，其中后者还使用FEVER标注。它们代表以监督式文本蕴含分类解决事实核查的路线，用来比较专用微调与大模型多步推理的效果。
- ProgramFC：由大语言模型生成推理程序，再调用共享的专用函数和Flan-T5执行验证。它是程序引导式推理基线，可检验ReflectFact相对于显式程序分解方法的价值。
- 智能体式事实核查：包括HiSS、Factcheck-GPT、BiDeV，以及结果分析中提及的StepByStepFV。HiSS和Factcheck-GPT侧重声明拆分，BiDeV采用多角色智能体交叉验证；所有此类基线统一替换为GPT-4o-mini骨干并禁止联网，用于在较公平的骨干与证据访问条件下比较不同工作流。

**实验想回答的问题**

- ReflectFact能否在HOVER与EX-FEVER的不同推理跳数上，比直接调用大语言模型、推理增强模型和现有智能体式事实核查方法取得更高的Macro-F1，尤其是在长链多跳声明上？
- 性能提升是否确实来自证据漂移验证（EDV）与推理反思验证（RRV），并且能否跨GPT-4o-mini和Qwen3-8B两种骨干模型泛化，同时生成与人工黄金解释相符的推理链？

**实验实现**

主要智能体实验使用GPT-4o-mini作为骨干，并以温度为0的贪心解码稳定输出；T5模块使用3B参数的FLAN-T5-XL。需要微调的模型采用交叉熵损失和AdamW优化器，学习率为$10^{-5}$。智能体基线均改用GPT-4o-mini且禁止访问网络，以控制骨干能力和外部信息来源。主实验在HOVER验证集与清除NEI后的EX-FEVER测试集上按跳数及总体Macro-F1评价；泛化实验另以Qwen3-8B复现实验，并在相同协议下与对应骨干的标准提示基线比较；解释实验则将ReflectFact构造的CoT与EX-FEVER黄金解释计算ROUGE。原文节选未明确报告重复运行次数、随机种子、显著性检验、提示模板及推理成本。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除证据漂移验证（w/o EDV） | 移除EDV后，HOVER的2-hop、3-hop、4-hop Macro-F1由83.33、76.91、73.74降至82.69、76.02、72.57，分别下降0.64、0.89、1.17个百分点；EX-FEVER的2-hop、3-hop由86.68、80.55降至84.21、77.84，分别下降2.47、2.71个百分点。 | 该消融保留整体规划与RRV，只去掉对“有证据回答是否仅复述无证据参数知识”的检查，因此主要隔离证据漂移校准的作用。所有设置均下降，且较深推理通常下降更多，符合早期证据理解错误沿后续步骤传播的解释；不过EX-FEVER的下降明显大于HOVER，原文没有进一步控制数据集差异。 | Table 2，Ablation Study<br><span class="experiment-evidence">w/o EDV 82.69 76.02 72.57 84.21 77.84
ReflectFact 83.33 76.91 73.74 86.68 80.55</span> |
| 移除推理反思验证（w/o RRV） | 移除RRV后，HOVER的2-hop、3-hop、4-hop Macro-F1由83.33、76.91、73.74降至80.68、73.77、69.98，分别下降2.65、3.14、3.76个百分点；EX-FEVER的2-hop、3-hop由86.68、80.55降至84.04、76.68，分别下降2.64、3.87个百分点。各设置的损失均大于移除EDV。 | 该消融使隐式实体定位、子问题推理和最终逻辑链等中间输出不再从全局核查目标重新审查，因而隔离“反思自身推理”的贡献。下降随跳数总体扩大，支持RRV是长链鲁棒性的主要来源；但由于论文只做单模块删除，尚不能判断EDV与RRV之间是否存在互补、冗余或交互效应。 | Table 2，Ablation Study<br><span class="experiment-evidence">w/o RRV 80.68 73.77 69.98 84.04 76.68
ReflectFact 83.33 76.91 73.74 86.68 80.55</span> |

**定性案例**

- 错误类型分析随机抽取了ReflectFact生成的40个样本，将错误归为逻辑错误、事实幻觉和思路遗漏，比例分别为10%、82.5%和7.5%；对语义分解阶段进一步分析时，72.7%的错误集中于大语言模型自身产生的幻觉。作者据此认为当前主要瓶颈已不是显式逻辑步骤，而是模型生成不受证据支持的事实；同时，拆分子信息虽有助于局部推理，却可能丢失文本中的长距离依赖。证据：“We find that the errors corresponding to the three stages are distributed as 10%, 82.5%, and 7.5%, respectively.”；“As shown in Figure 4(b), 72.7% of the errors are concentrated in hallucinations generated by LLM itself.”（Figure 4，Error Type Analysis）。由于样本仅40个且抽样与标注细节未说明，这些比例应视为诊断性观察，不能当作稳定的总体错误分布。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It develops a self-reflective agent that plans, checks evidence grounding, and revises multi-step reasoning for fact verification.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`4275d6c726a3aad7cac9d6e6eedc8b1b3f87572e3fa3786febfbdfa81b06736d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
