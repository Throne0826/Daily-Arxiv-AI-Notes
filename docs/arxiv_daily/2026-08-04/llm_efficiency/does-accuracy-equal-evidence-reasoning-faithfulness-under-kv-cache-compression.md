---
title: "[论文解读] Does Accuracy Equal Evidence? Reasoning Faithfulness under KV Cache Compression"
description: "[arXiv 2608.01631][LLM 效率] 本文指出，KV 缓存压缩后的最终答案正确率并不能充分证明其推理依据仍被保留，并将正确答案与证据支持不同步的现象定义为“答案—证据鸿沟”。"
arxiv_id: "2608.01631"
announcement_date: "2026-08-04"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:01:07.783423+00:00"
source_sha256: "8e88fd2fb30382cf4dd29a74897a30062f30883274071cab01d1a420fff95b5e"
tags:
  - "LLM 效率"
  - "LLM Reasoning"
  - "KV 缓存压缩"
  - "大型推理模型"
  - "推理忠实性"
  - "固定轨迹重放"
  - "答案—证据差距"
  - "思维链"
  - "词元淘汰"
  - "KV 量化"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2608.01631</p>

# Does Accuracy Equal Evidence? Reasoning Faithfulness under KV Cache Compression

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Mengting Ai, Jingrui He, Yue Guo</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Illinois Urbana-Champaign</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01631v1) · [PDF 下载](https://arxiv.org/pdf/2608.01631v1) · **关键词** KV 缓存压缩, 大型推理模型, 推理忠实性, 固定轨迹重放, 答案—证据差距, 思维链, 词元淘汰, KV 量化<br>
**代码**: [https://github.com/famous-blue-raincoat/Safe_KV_Compress](https://github.com/famous-blue-raincoat/Safe_KV_Compress)

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

本文指出，KV 缓存压缩后的最终答案正确率并不能充分证明其推理依据仍被保留，并将正确答案与证据支持不同步的现象定义为“答案—证据鸿沟”。

**不用术语来说**：大型推理模型会保存先前文本的内部计算结果，以便生成后续内容时直接使用；长推理会使这部分缓存占用大量显存，因此通常需要压缩。问题在于，现有评估往往只检查压缩后答案是否正确：模型可能仍然给出正确答案，但展示的推导已经包含无依据的步骤、缺失关键证据，或很容易被错误的中间陈述带偏。在数学证明、科学问答和临床计算等需要审核推理过程的场景中，这种表面正确会使人高估压缩方案的可靠性。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“答案—证据鸿沟”这一可观察的行为失效模式：KV 缓存压缩可能以不同速率保留最终答案和支持该答案的推理证据，因此准确率保持并不等价于推理可信度保持。
- 作者提出受控的固定轨迹重放评估思路，并联合考察最终答案准确率、答案—推理链一致性和扰动忠实度，使压缩方案是否仍能利用既有推理证据成为可测量问题。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

自回归大语言模型在生成每个新词元时，需要让注意力机制访问此前词元的表示。KV 缓存保存这些历史词元的键和值状态，从而避免重复计算完整前缀，但其显存占用会随上下文长度和生成长度增长；大型推理模型往往先生成数千个中间推理词元，因此这一开销尤其突出。KV 缓存压缩通过淘汰、合并或量化缓存状态降低推理期内存，现有研究通常用最终答案准确率判断压缩是否成功。本文关注这一评价标准的隐含假设：答案仍然正确，是否就意味着可见推理链仍拥有足以支持该答案的有效证据。作者将二者不一致的现象称为“答案—证据差距”，并强调它是可观察的行为差异，而不表示缓存内部必然存在彼此独立的“答案模块”和“论证模块”。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**KV 缓存**

Transformer 在自回归生成中保存历史词元的键向量和值向量，使后续词元可以直接关注已有前缀，而不必重新计算全部历史状态。它能加速解码，但缓存大小会随序列变长，可能成为推理期显存瓶颈。

</div>
<div class="concept-item" markdown="1">

**KV 缓存压缩**

缓存压缩旨在减少历史键值状态所占内存；本文涉及的主要路线包括删除部分词元状态的“词元淘汰”和降低每个状态数值精度的“量化”。前者可能使模型完全无法访问被删除的推理片段，后者通常保留所有位置但以较低精度表示。

</div>
<div class="concept-item" markdown="1">

**推理忠实性**

推理忠实性要求模型展示的推理过程确实与答案形成有关，并能提供有效、可检验的支持，而不只是事后编造的合理化文字。因而，一条看似流畅的思维链即使导向正确答案，也可能遗漏证据、使用错误前提或对误导性中间陈述异常敏感。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是在数学推理、科学问答、临床计算和长上下文检索任务上运行的大型推理模型。实验先让未压缩模型生成完整推理轨迹，再使用固定轨迹重放协议，让不同缓存压缩方法在相同推理内容上重放该轨迹；这样可尽量排除自由生成时路径分叉造成的混杂，集中检验压缩后的 KV 状态是否仍保存了原轨迹中的可用信息。评价输出不只包括最终答案是否正确，还包括答案是否受到推理链支持，以及面对误导性中间陈述时表现出的扰动忠实性。核心判定问题是：在压缩预算下，某方法能否同时保留答案性能和证据支持；若准确率保持而推理有效性或忠实性明显下降，则出现答案—证据差距。相反，在依赖精确证据保留的检索任务中，信息损失可能直接表现为准确率下降，因此准确率崩溃可以揭示压缩损害，但准确率保持不能充分证明证据也被保留。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **KV 缓存压缩研究**: 既有方法通过保留高注意力词元、注意力汇聚位置或最近窗口，或采用分层预算、头级分配、语义分块、冗余感知选择和 KV 量化等策略减少内存。本文不提出另一种压缩器，而是质疑该方向主要依赖最终答案准确率的评价惯例，并比较多种词元淘汰方法与一种覆盖保留型量化方法在证据保留方面的差异。
- **思维链忠实性研究**: 既有研究表明，可读且貌似合理的思维链可能掩盖偏置线索的使用、遗漏真正影响答案的提示，或对既有结论进行事后合理化；相关工作采用因果、反事实、符号验证和证据核验等方式测量忠实性。本文把这一问题引入 KV 缓存压缩场景，考察压缩是否会在最终答案仍正确时破坏可见推理链的支持作用。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

自回归模型通过 KV 缓存保存先前 token 的键和值状态，从而避免每一步都重新计算完整前缀；但大型推理模型常生成数千个中间推理 token，使 KV 缓存成为推理阶段的重要显存瓶颈。压缩虽然能降低资源开销，却可能删除后续验证答案所需的推理信息。由于中间推理正被用于解释、审计和信任模型输出，压缩方案不仅要保住答案，还应保住让答案可核查的证据结构。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于最终答案准确率的 KV 压缩评估**：对 KV 缓存应用压缩后运行任务，只比较模型最终答案与标准答案是否一致；若准确率接近未压缩模型，通常便认为压缩较好地保留了模型能力。
- **思维链忠实度评估**：不只判断推理文本是否看起来合理，而是检查可见推理是否真正支持答案，以及模型在中间证据被误导性修改时是否表现出符合证据依赖关系的变化；既有研究已表明，合理流畅的解释也可能遗漏、歪曲或事后合理化真实依据。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 准确率是一种非对称诊断：准确率下降能够暴露压缩损害，但准确率保持只能说明答案仍可恢复，不能证明完整、有效的推理依据仍可访问。其后果是把“答案碰巧正确但证据已受损”的情况计为压缩成功，形成假阳性并高估方案质量。
- 既有思维链忠实度研究揭示了解释与真实依据可能脱节，但尚未专门隔离 KV 缓存压缩的影响；若直接比较压缩前后的自由生成结果，推理轨迹、长度和解码过程会同时改变，因而难以判断差异究竟来自缓存信息丢失，还是来自模型走上了另一条推理路径。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种面向大型推理模型的受控评估框架，用来区分“压缩后仍能输出正确答案”与“压缩后仍保有可用于支持、核查该答案的推理证据”。尤其尚不清楚，在固定模型、提示、文本前缀与解码配置，并保持既有推理轨迹不变时，不同 KV 缓存变换是否会让答案保持率、推理链有效性和对误导性证据的敏感性发生分离，以及这种分离是否随任务、模型和压缩预算而变化。

</div>
<div markdown="1"><span>核心问题</span>

当同一条由未压缩模型生成的推理轨迹在压缩 KV 状态下被重放时，压缩方法是否能够同时保留最终答案、答案与推理链之间的一致性以及对中间证据的忠实依赖，还是会出现答案仍正确而证据支持已经失效的“答案—证据鸿沟”？

</div>
<div markdown="1"><span>作者直觉</span>

固定轨迹重放先让未压缩模型生成一条完整推理，再要求各压缩方案在同一文本轨迹上重放，因此被比较的方法看到相同的显式推理内容；主要变化来自它们如何保留或变换对应的 KV 状态。这样可以把“缓存中原本可用的信息是否仍能被访问”与“模型是否生成了另一条推理路径”区分开。再将答案正确性与推理链一致性、扰动忠实度并列观察，就能识别仅检查答案时不可见的证据损失；覆盖范围保持较完整的量化压缩还可作为对照，帮助判断问题更可能源于推理轨迹局部访问权的丢失，而非缓存变小本身。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文提出“受控固定轨迹重放”（controlled fixed-trace replay），用于诊断 KV 缓存压缩是否仍能让模型利用一条已经存在的推理轨迹。给定问题 $q$、标准答案 $y$ 和未压缩模型生成的完整思维轨迹 $r$，实验先固定文本前缀 $q\,\|\,\texttt{<think>}r\texttt{</think>}$，再让每种压缩方法分别建立自己的 KV 缓存；其中问题对应的缓存受到保护，只有推理轨迹 $r$ 对应的缓存被压缩。随后，模型从 $\texttt{</think>}$ 后重新解码，生成可见解释与最终答案。因为各方法读到的文本完全相同，输出差异可主要归因于压缩后的 KV 表示是否保留了可用信息，而不是各次生成采用了不同推理路径。

该方法把“答案线索”和“证据支持”作为两种行为功能加以区分：前者是足以恢复答案的结论、摘要或临近最终回答的提示，后者则包括中间方程、前提检查、分情况讨论、检索事实和验证步骤。论文并不假设 KV 状态在机制上被明确拆成这两部分，而是通过最终答案准确率、答案与推理链的一致性以及扰动忠实度，观察压缩是否以不同速率损害二者。直观地说，该实验相当于把同一份解题草稿交给不同的“压缩记忆系统”，再检查它们能否不仅记住答案，还能利用草稿中的步骤给出真正支持答案的解释。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成并固定未压缩推理轨迹

先运行 Full-KV 模型，使其生成完整的 $\texttt{<think>}r\texttt{</think>}$ 推理轨迹及其后续回答；之后抽取并固定文本轨迹 $r$，作为所有压缩方法共享的重放内容。固定轨迹在压缩实验开始前生成，避免压缩方法改变前期推理文本。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、标准答案 $y$，以及使用完整 KV 缓存的基础模型。<br>
**输出**：共享的固定文本前缀 $q\,\|\,\texttt{<think>}r\texttt{</think>}$，以及用于评分的标准答案 $y$。

</div>

**直观理解**：先由未压缩模型写出一份统一的解题草稿，之后每种压缩方法都使用同一份草稿。这样不会把“草稿本来就不同”误判成“记忆压缩效果不同”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 重放前缀并构建方法专属 KV 状态

对固定前缀执行预填充（prefill），即一次性计算各层、各注意力头的键和值状态 $K_{1:t}^{(\ell,h)}$ 与 $V_{1:t}^{(\ell,h)}$。每种方法独立构建自己的压缩缓存，因此共享的是文本内容，而不是同一份缓存状态。

<div class="method-step__io" markdown="1">

**输入**：固定前缀 $q\,\|\,\texttt{<think>}r\texttt{</think>}$，以及待评估的 KV 压缩方法。<br>
**输出**：与相同文本前缀对应、但由不同压缩算法处理的候选 KV 表示。

</div>

**直观理解**：所有方法读的是同一段文字，但各自决定如何把它存进有限记忆。比较的重点由此变成“同样的信息被压缩后还能否取用”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 保护问题并仅压缩推理缓存

问题部分的 KV 缓存始终受到保护，只对 $r$ 对应的缓存执行保留、合并、量化或逐 token 驱逐；主要诊断采用激进的 256-token 驱逐预算，并以 KIVI-2bit 作为保留 token 覆盖范围的量化对照。该设计防止压缩问题文本本身成为混杂因素。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$ 与推理轨迹 $r$ 对应的分段 KV 状态，以及指定的保留预算。<br>
**输出**：保留完整问题信息、但推理轨迹表示已经缩减的压缩 KV 缓存。

</div>

**直观理解**：实验只“压缩草稿”，不删题目，以便确认失败是否来自推理证据丢失。量化对照则像保留整份草稿但降低字迹精度，用来区别“精度降低”和“整段内容被删除”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 从固定边界恢复解码

模型不重新生成 $r$，而是从 $\texttt{</think>}$ 后立即恢复自回归解码，为每种压缩缓存重新生成可见理由和最终答案。由于重放文本与恢复位置一致，压缩可以改变后续解释和答案，却不能改变已经提供的推理文本。

<div class="method-step__io" markdown="1">

**输入**：压缩后的 KV 缓存，以及紧接在 $\texttt{</think>}$ 之后的统一解码位置。<br>
**输出**：每种压缩方法对应的新生成可见解释与最终答案。

</div>

**直观理解**：这相当于让模型读完同一份草稿后重新作答。若答案仍正确但新解释无法由草稿中的步骤推出，就暴露了“答案保住了、证据却没保住”的差距。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该工作提出的是推理阶段的诊断与评估协议，不训练新的模型，也没有通过损失函数优化压缩器；被比较的压缩方法按照各自已有规则选择、驱逐、合并或量化 KV 状态。标准答案 $y$ 只用于输出评分，不作为梯度监督。固定轨迹重放的目标是控制变量并测量信息可用性，而不是学习一个新的参数化映射。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 固定轨迹控制器**

控制器先保存 Full-KV 模型产生的 $r$，再强制所有方法预填充相同的 $q\,\|\,\texttt{<think>}r\texttt{</think>}$，并在同一边界恢复解码。它将“推理内容是否曾出现”保持不变，从而把主要自变量限制为压缩后的 KV 表示。

> 直观理解：若每种方法都自由生成草稿，就无法判断差异来自压缩还是来自不同解题过程；该控制器相当于给所有方法发同一份试卷和草稿。

**2. 分段缓存保护与压缩器接口**

系统按文本区间区分问题缓存和推理缓存，保护前者并对后者施加精确目标预算。接口覆盖十种 token 驱逐方法，并加入 KIVI-2bit 量化控制：驱逐方法减少可访问的轨迹位置，量化方法则降低状态精度但保留轨迹覆盖范围。

> 直观理解：这一模块把“删掉若干草稿步骤”与“所有步骤都在但记录较粗糙”分开比较，因此能检验问题究竟来自内存减少本身，还是来自证据位置消失。

**3. 证据敏感性诊断器**

诊断器结合答案评分、答案—推理链一致性检查和扰动测试；扰动包括插入错误答案以及用另一随机种子的域内错误推理块替换原轨迹中段。位置条件分析进一步检测不同压缩器是否偏向保留开头锚点、末尾结论或局部显著内容。

> 直观理解：它不只问“最后答得对不对”，还问“解释真的支持答案吗”以及“证据被改坏后模型会不会察觉”。后两项用于识别看似正确、实际依赖错误线索或缺失验证步骤的输出。

**训练与推理**

完整流程属于推理时评估。首先用 Full-KV 模型在问题 $q$ 上生成教师轨迹 $r$；随后针对每个压缩器重新预填充相同的 $q\,\|\,\texttt{<think>}r\texttt{</think>}$，保护问题缓存，仅压缩 $r$ 的缓存，并从结束标签后恢复采样解码。对原始轨迹和受控扰动轨迹重复该过程，再比较答案、可见推理链和扰动响应。主要固定轨迹实验隔离“已生成证据经过压缩后是否仍可用”，而补充的端到端实验让压缩在生成过程中持续生效，因而同时改变未来轨迹、推理长度、中间错误和最终答案，只用于验证部署场景下的相关性。

**复现信息**

实验基于 HuggingFace Transformers，模型权重和 KV 缓存均使用 bfloat16，并在 NVIDIA H100 80GB GPU 上运行。主要思考模式解码采用温度 $0.6$、top-$p$ 为 $0.95$、top-$k$ 为 $20$、min-$p$ 为 $0.0$、重复惩罚为 $1.0$；固定教师轨迹的生成上限分别为 AIME 的 32,000 tokens、GPQA-Diamond 的 12,000 tokens 和 MedCalc 的 4,096 tokens。

SnapKV、StreamingLLM、TOVA、KNorm、LagKV、ChunkKV、AdaKV 和 PyramidKV 通过 kvpress 0.5.1 实现，并添加包装逻辑以保护提示词和后缀、严格满足目标预算；R-KV 与 HeadKV 按其公开方法设计实现。主要诊断使用 256-token 驱逐预算，这是刻意设置的高压缩条件；端到端范围检查使用 2,048-token 预算。该预算主要换取 KV 内存缩减，而不是解码加速，因为缓存选择与模型计算仍位于推理关键路径。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- AIME24、AIME25、AIME26：多步符号数学推理基准，每年各 30 题，分别使用官方竞赛题，并汇总报告 AIME24–26 结果。答案是整数，主要检验压缩后模型能否保留完整推导，而非仅凭局部线索恢复最终答案。
- GPQA-Diamond：研究生水平的多项选择科学问答，使用 Diamond 子集，共 198 个样本，采用 CC BY 4.0 许可。它检验模型在需要专业知识与多步科学推理时，答案正确性和推理链支持是否同步保持。
- MedCalc-Bench 与 RULER QA 分别代表证据依赖更强的临床计算和长上下文检索：前者使用 1,100 个评估集样本，要求从病例中提取患者变量并应用计算公式；后者使用 500 个 32K-token QA 样本，在干扰信息中进行多跳检索。二者用于测试关键变量或特定证据被驱逐后，正确答案和证据忠实性是否以不同速度下降。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**最终答案准确率**

衡量模型输出的最终答案是否正确。该指标反映任务完成情况，但不能单独证明可见推理链确实支持该答案。 （越高越好，因为它表示更多样本得到正确最终答案。）

</div>
<div class="metric-item" markdown="1">

**答案—推理链一致性**

采用任务特定的严格二元标准，将推理判为“完全正确”或“并非完全正确”，检验可见推理链能否有效推出并支持最终答案。论文使用 Claude-Sonnet-4.0 作为裁判，并以人工标注审计其一致性。 （越高越好，因为它表示答案与支撑答案的推导同时成立，而不是只碰巧得到正确答案。）

</div>
<div class="metric-item" markdown="1">

**扰动忠实性**

通过对推理轨迹不同位置实施干预，观察模型是否按照被改变的证据作出相应反应，从而衡量输出是否真正依赖其声称使用的推理信息，而非依靠残余线索恢复答案。 （越高越好，因为对证据扰动作出符合预期的响应，说明模型对可见推理轨迹存在更真实、可检验的依赖。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 固定轨迹重放下，比较完整 KV 与十种 token 驱逐压缩方法在推理和检索任务上的表现

<div class="result-value" markdown="1">

作者报告，token 驱逐方法可能维持有竞争力的最终答案准确率，却明显损害推理链支持或扰动忠实性，即答案和证据并不以相同速度退化。节选没有提供相应分数，因而无法判断各方法差距的具体幅度。

</div>

这说明“答对”不能自动推出“推理仍有效”：压缩后模型可能凭剩余局部线索恢复答案，但已经无法访问完整推导或关键证据。该结果证明的是评估指标之间可能分离，并不证明所有正确答案都是猜测，也不证明所有驱逐方法在所有任务上都会同等退化。

<div class="result-source" markdown="1">

来源：第 4 节 Experimental Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Our main finding is an answer–evidence gap: compressed models can preserve final-answer accuracy while degrading the derivation, verification, or robustness needed to support the answer.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 以覆盖保持型量化作为内存压缩控制，与删除 token 的驱逐方法比较

<div class="result-value" markdown="1">

作者称量化控制受到的答案—证据缺口影响明显较小，支持问题主要与丢失对部分推理轨迹的访问有关，而不是任何形式的 KV 内存缩减都会造成同等损害。节选未报告量化位宽、压缩率或具体指标数值。

</div>

量化保留所有位置但降低表示精度，而驱逐直接移除位置；两者的差异使实验能够更接近因果地定位故障来源。结果支持“覆盖范围比单纯容量更关键”的解释，但尚不能排除量化误差、实际内存节省比例或方法实现差异等其他因素。

<div class="result-source" markdown="1">

来源：论文摘要；第 4.1 节将 quantization-based controls 列为比较方法

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A coverage-preserving quantization control is substantially less affected, suggesting that the failure is tied less to KV memory reduction itself than to losing access to parts of the reasoning trace.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 答案—推理链一致性的裁判可靠性检查，覆盖 AIME、GPQA-Diamond、MedCalc-Bench 和 RULER QA-2

<div class="result-value" markdown="1">

一名研究生水平专家独立标注 400 个输出，LLM 裁判与人工标注的总体 Cohen's $\kappa$ 为 0.89；各任务分别审计 100 个样本，说明主要一致性指标并非完全依赖未经验证的自动裁判。

</div>

较高的 Cohen's $\kappa$ 表明在扣除随机一致后，LLM 与人工对“推理完全正确”这一严格二元标签具有较强一致性，为答案—推理链结果提供测量可信度。但这不是模型任务性能，也不能证明裁判在未审计样本、边界案例或其他模型输出上没有系统偏差。

<div class="result-source" markdown="1">

来源：附录 B，表 13

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Overall | 400 | 0.89

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

- Full-KV：不压缩的完整 KV 缓存参照，用于确定模型在完整访问既有推理轨迹时的答案、推理链和鲁棒性上限，也是判断压缩损失的共同基准。
- 基于新近性、attention sink 与注意力分数的 token 驱逐方法：分别偏向保留最近 token、序列中的稳定注意力锚点或高注意力 token，用于检验常见局部重要性规则能否同时保存答案和支持答案的证据。
- 采用头级或层级分配、语义片段保留、局部效用、冗余感知及推理感知策略的驱逐方法：这些方法利用更精细的结构或语义信号选择保留内容，用于判断答案—证据缺口能否通过更有针对性的 token 选择得到缓解。原文节选未给出十种驱逐方法各自的名称。
- 覆盖保持型量化方法：不直接删除推理轨迹中的 token，而是降低 KV 表示精度以节省内存。它是关键控制组，用于区分“内存缩减”与“失去部分轨迹访问权”两种可能原因。

**实验想回答的问题**

- 在固定推理轨迹内容不变时，KV 缓存压缩是否会出现“答案仍正确，但可见推理链已不足以支持答案”的答案—证据缺口？
- 该缺口主要源于缓存容量减少本身，还是源于逐 token 驱逐造成的推理轨迹覆盖丢失；它是否跨数学、科学、临床计算和长上下文检索任务存在？

**实验实现**

主要实验采用固定轨迹重放：先固定一条已经存在的推理轨迹，再在压缩条件下重放，使各方法面对相同推理内容，从而把“生成了不同推理路线”这一混杂因素排除，集中测量压缩后缓存中是否仍有可用信息。默认情况下，token 驱逐方法只保留 256 个 token；作者说明这一激进预算是为了拉开方法差异，并在 512 至 8,192 token 范围内做预算消融。主模型为 Qwen3-8B，另在 DeepSeek-R1-Distill-Llama-8B 和 Qwen3-30B-A3B 上验证总体模式。为补充部署场景，作者还在 AIME26 和 GPQA-Diamond 上进行端到端检查；端到端压缩会同时改变推理轨迹的形成和 KV 保留，因此它是适用范围检查，不能像固定轨迹重放一样单独归因于缓存保留。所有数据集仅用于评估，没有用于训练或微调。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 将 token 驱逐方法的保留预算从 512 调整到 8,192 token，并与默认 256-token 设置联系起来考察 | 作者说明，更大的预算常使各方法结果聚集到 Full-KV 附近，因此默认采用 256-token 激进预算以增强诊断区分度；预算消融覆盖 512 至 8,192 token。节选没有给出每个预算下准确率、链一致性或扰动忠实性的具体变化。 | 该消融隔离“保留容量”对现象的影响：如果预算增大后缺口缩小，说明关键证据被驱逐是重要机制。但默认的极低预算也可能放大部署中较温和压缩设置下的差异，因此不能把 256-token 条件下的严重程度直接外推到所有预算。 | 第 4.1 节 Compression budget；预算结果见第 4.5 节<br><span class="experiment-evidence">This aggressive setting provides diagnostic separation among methods: larger budgets often made results cluster near Full-KV, making it harder to observe the difference; we further ablate budgets from 512 to 8,192 tokens in Section 4.5.</span> |
| 固定轨迹重放与 AIME26、GPQA-Diamond 端到端压缩检查的协议对照 | 固定轨迹重放只考察既有推理轨迹在压缩后是否仍可用；端到端检查则同时允许压缩改变轨迹生成和缓存保留。作者在 AIME26 表 2 及 GPQA-Diamond 附录表 11 中进行部署式检查，但所给节选未包含具体结果数值。 | 该对照隔离实验协议的影响。固定重放具有更清晰的归因能力，端到端设置更接近实际部署；若二者呈现相同总体模式，现象的外部有效性更强，但端到端结果本身不能判断退化究竟来自生成路线变化还是缓存证据丢失。 | 第 4.1 节 End-to-end scope check；AIME26 见表 2，GPQA-Diamond 见附录表 11<br><span class="experiment-evidence">These experiments serve as deployment-style scope checks: online compression jointly changes trajectory construction and KV retention, whereas fixed-trace replay isolates the retention question.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work studies how KV-cache compression affects both answer accuracy and the faithfulness of preserved reasoning traces.; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`8e88fd2fb30382cf4dd29a74897a30062f30883274071cab01d1a420fff95b5e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
