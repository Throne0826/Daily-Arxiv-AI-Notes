---
title: "[论文解读] PROVE-RT: Generating Mechanized Theorem Prover Scripts for Real-Time Systems using LLMs"
description: "[arXiv 2608.12762][LLM Reasoning] PROVE-RT旨在通过依赖感知的非形式化证明草图、PROSA文档检索和分阶段脚本生成，降低将实时系统可调度性分析转化为可由Rocq机械检查的PROSA证明的难度。"
arxiv_id: "2608.12762"
announcement_date: "2026-08-14"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:59:42.270506+00:00"
source_sha256: "ddc0ca8ce53ed4eea0e1749350e0f2ecab8105c353c4b01c742b6a87d92c3469"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "实时系统"
  - "可调度性分析"
  - "机械化验证"
  - "交互式定理证明"
  - "PROSA"
  - "Rocq"
  - "大语言模型"
  - "证明脚本生成"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.12762</p>

# PROVE-RT: Generating Mechanized Theorem Prover Scripts for Real-Time Systems using LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Sadat Shahriyar, Shareef Ahmed, Abdullah Al Arafat</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Florida International University；University of South Florida</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12762v1) · [PDF 下载](https://arxiv.org/pdf/2608.12762v1) · **关键词** 实时系统, 可调度性分析, 机械化验证, 交互式定理证明, PROSA, Rocq, 大语言模型, 证明脚本生成<br>


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

PROVE-RT旨在通过依赖感知的非形式化证明草图、PROSA文档检索和分阶段脚本生成，降低将实时系统可调度性分析转化为可由Rocq机械检查的PROSA证明的难度。

**不用术语来说**：实时系统必须证明每项任务都能按时完成，但这类证明通常由研究者在纸面上推导，细小错误可能影响最终结论及后续研究。PROSA与Rocq可以让计算机逐步检查证明，却需要使用者准确选择领域模型、补齐依赖关系并编写大量形式化代码；例如，文中报告的两个既有工程分别需要18,852行和4,135行Rocq代码。因此，核心现实需求是把论文中的可调度性推导更高效地转成机器可检查的证明，同时保留形式验证带来的可靠性。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出PROVE-RT，这是其所称首个面向实时系统可调度性分析、辅助生成PROSA/Rocq机械化脚本的LLM框架；其针对领域知识不足和论文证明结构不显式的问题，组合了依赖感知草图、文档检索、分阶段骨架生成与证明补全。
- 作者从1,191篇实时系统论文构建面向机械化的语料，包含13,134个带依赖信息的非形式化草图及相应PROSA/Rocq脚本工件，用于缓解该领域专用训练与评测数据不足的问题。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于实时系统可调度性分析与交互式定理证明的交叉领域。可调度性分析用于判断一组实时任务在给定调度策略和系统假设下能否满足截止期限；传统结果多依赖手写数学证明，难以系统检查和长期维护。PROSA 是建立在 Rocq（原 Coq）之上的可调度性分析库：它用 Rocq 的规范语言 Gallina形式化任务、作业、调度、工作量、干扰和响应时间等概念，再把分析结论写成由可信内核逐步检查的引理或定理。本文关注的不是提出新的调度判定公式，而是让大语言模型把实时系统论文中的非形式化分析转换为可编译、可机器检查的 PROSA/Rocq 证明脚本。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**可调度性分析**

它研究实时任务在处理器、调度策略、到达模式和执行时间等约束下，是否都能在截止期限前完成。论文中的分析通常涉及工作量界、干扰界或响应时间保证，最终目标是证明相应的可调度性结论。

</div>
<div class="concept-item" markdown="1">

**机械化证明与 PROSA/Rocq**

机械化证明把定义、假设、引理和定理编码到交互式定理证明器中，并由小型可信内核检查每一步；PROSA 则是面向实时系统可调度性分析的 Rocq 库。一个 PROSA 脚本通常包含模块导入、变量和假设声明、形式化定义、定理陈述以及用于完成证明义务的策略命令。

</div>
<div class="concept-item" markdown="1">

**证明上下文、依赖顺序与类型类解析**

证明上下文是当前位置可用的变量、假设、既有结论及类型类实例；类型类用于表达任务参数、作业代价、到达信息和调度属性等可复用建模假设。由于 Rocq 要求对象先定义后使用，且所需实例必须能够从当前环境中找到，脚本只有按依赖关系正确排序并建立完整上下文，才可能通过类型检查和编译。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是实时系统文献中的可调度性分析内容，包括自然语言论证、数学定义、假设、引理及其依赖关系；目标输出是对应的 PROSA/Rocq 源代码，其中应包含必要导入、建模上下文、定义、定理陈述和完整证明。运行环境假定已有 Rocq 与 PROSA 提供的形式化接口和既有定理；生成器必须选择正确的 PROSA 抽象，保证每项依赖在使用前出现、所需类型类实例可解析、表达式类型一致，并消解全部证明义务。最终有效性以 Rocq/PROSA 编译检查为准：仅有语法相似或自然语言上合理的脚本并不足够，缺少导入、变量、实例或证明步骤都会导致机械化失败。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **基于 PROSA 的既有实时系统机械化验证工作**: 既有研究已使用 PROSA 验证响应时间分析、CAN 可调度性认证、FIFO 调度、忙窗口推理，以及响应时间分析与网络演算之间的联系，说明该库能够提高实时系统理论结论的可信度。但这些工作仍依赖专家手工构造模型、上下文和证明，因此构成本文试图降低的主要工程成本。
- **学习式证明策略生成、前提选择与大语言模型辅助定理证明**: 先前方法通过学习模型生成证明策略、选择相关前提或引导证明搜索，近期大语言模型也被用于数学和软件验证中的形式化证明生成。作者指出，这些研究主要面向通用定理证明或其他应用领域；据其所知，此前尚无工作专门从实时系统论文自动生成用于机械化可调度性分析的 PROSA 证明。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

安全关键实时系统需要通过离线可调度性分析认证其运行时的时序正确性。传统纸笔证明随着系统和分析模型变复杂而越来越难以验证、扩展与维护，且中间引理或界限中的隐蔽错误会传播到最终结论。机械化证明能够提高可信度，但人工把论文推导编码为PROSA/Rocq脚本需要同时掌握实时调度理论、PROSA建模抽象和证明工程，开发与模型变更后的维护成本都很高。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **人工纸笔可调度性证明**：研究者以数学文字和公式建立任务模型、工作量或干扰界限，再推导足以保证截止期的条件；结论主要依赖同行审查和人工复核，而不是由证明内核逐步检查。
- **人工PROSA/Rocq机械化与通用LLM证明生成**：PROSA在Rocq之上提供任务、调度、工作量、干扰和可调度性结论等可复用定义，专家可据此编写机器可检查的证明；另一方面，已有机器学习和LLM方法尝试自动生成一般数学证明或定理证明器脚本，但并未专门解决PROSA中的实时系统分析机械化。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 纸笔分析缺少定理证明器所要求的显式类型、假设、依赖和逐步证明结构，人工检查容易遗漏细微错误；当后续分析复用错误引理或界限时，影响还会继续传播。
- 纯人工机械化代码量大且维护脆弱，而直接使用先进LLM又缺少PROSA专用语料、建模抽象和证明模式知识，难以把非机械化论文推导可靠地映射为合法脚本；作者报告直接提示不能稳定生成有效PROSA机械化结果。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作分别提供了PROSA这一严格验证基础，以及面向一般定理证明的机器学习自动化，但原文称此前没有研究系统处理“从实时系统文献中的可调度性分析自动生成PROSA机械化证明”这一任务。尚缺少的具体能力包括：识别分析中未显式写出的证明依赖，以PROSA文档约束领域概念和接口，并把复杂结论分解成可逐步生成、可由Rocq检查的脚本；与此同时，PROSA专用数据集的缺乏也使模型训练和客观评测受到限制。

</div>
<div markdown="1"><span>核心问题</span>

在PROSA专用训练材料有限、论文证明结构不显式且可调度性定理依赖复杂的条件下，能否利用LLM配合依赖提取、领域文档检索和分阶段生成，将实时系统论文中的可调度性分析转化为能够通过Rocq机械检查的PROSA脚本，并比直接提示通用先进LLM更可靠？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把一次性生成完整证明改造成受约束的逐步翻译：先从论文中整理出人可读的证明草图及其前置依赖，再检索与当前步骤相关的PROSA定义和既有证明模式，随后先生成结构骨架，最后补全证明。直观上，这相当于先给模型列出“要证明什么、依赖什么”，再提供“PROSA里应当如何表达”的参考资料，从而缩小每一步的搜索空间，并减少模型凭一般Rocq经验猜测领域接口的机会。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PROVE-RT把论文中的实时系统可调度性分析，而非一个已经写好的形式定理，转换为能够由PROSA/ROCQ编译检查的机械化证明脚本。输入是自然语言与数学公式混合的分析$A$以及处理后的PROSA文档库$P$；系统先抽取待形式化的系统不变量集合$I$，为每个不变量$i_j$生成非形式化草图$K_j$，并构造依赖有向无环图$G_D$。之后，它按依赖顺序为每个$i_j$检索库内相关上下文$R_j$，增量生成代码块$s_j$的结构骨架，将暂时不能完成的证明写成`Admitted.`，再生成证明片段$\pi_j$替换占位符，并利用ROCQ编译器反馈迭代修复。最终输出是按依赖排序且能够通过编译检查的脚本$S$。

该方法的关键不在于让大模型直接“猜下一条证明策略”，而在于先恢复一篇论文在证明助理中必须显式提供的形式结构。通俗地说，PROVE-RT先把论文拆成一张“哪些定义和结论必须先出现”的施工图，再从PROSA代码库中寻找可复用的零件，先搭出完整框架，最后逐项补齐证明并交给编译器验收。成功输出同时要满足三项要求：$s_j$表达的内容与$i_j$一致，脚本顺序服从$G_D$，且完整脚本能在PROSA/ROCQ环境中编译；其中语义忠实性主要依赖抽取、草图和生成过程，编译只能验证形式合法性与证明义务是否成立，不能单独保证脚本准确复现原论文意图。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 系统不变量、草图与依赖抽取

使用带示例和约束规则的LLM提示识别机械化所需的系统不变量$I=\{i_1,\ldots,i_n\}$，并为每个$i_j$生成包含命题陈述、直觉和预期证明步骤的草图$K_j$。同时识别每个不变量依赖的前置不变量，构造$G_D=(I,D)$并据此排列处理顺序。

<div class="method-step__io" markdown="1">

**输入**：实时系统文献中的可调度性分析$A$，其中可能混合定义、公式、假设、引理、定理、推论和自然语言证明。<br>
**输出**：依赖有序的不变量集合$I$、一一对应的草图集合$\{K_j\}$以及依赖有向无环图$G_D$。

</div>

**直观理解**：这一步把面向人类写作的论文变成形式化任务清单，并标出每项任务的先修关系。例如某个结论使用了先前定义的时间开销函数，那么该定义必须排在结论之前。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### PROSA文档语料处理

将文档加工成可检索语料库$P$：对Analysis和Results采用面向证明的切块，将形式代码块与对应说明文字配对；对其余模块采用章节级切块，以保留较自包含的概念、假设和辅助构件。Results主要提供完整的已验证证明范例，其他模块提供模型、定义、类型类假设、可复用引理和辅助证明上下文。

<div class="method-step__io" markdown="1">

**输入**：PROSA库中按Analysis、Behavior、Implementation、Model、Results和Util组织的文档、ROCQ代码与证明。<br>
**输出**：由文档片段、形式定义、假设、可复用引理和示例证明结构组成的检索语料库$P$。

</div>

**直观理解**：预训练模型通常不知道PROSA中特定名称和使用规则，因此系统先把代码库整理成可搜索的参考手册。不同模块采用不同粒度，是为了让完整证明保留代码与解释的联系，同时避免把简单概念切得过碎。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按不变量检索并恢复库内依赖

分别以$K_j$中的命题陈述、直觉和结论构造查询，各自取得排名前$k$的候选片段，再合并候选并选择最高分片段形成$R_j\subseteq P$。对于来自Analysis或Results的面向证明片段，框架还补入相关依赖，使检索到的定理或定义连同其所需支撑构件一起进入生成上下文；节选未给出具体排名算法、$k$值及依赖恢复细则。

<div class="method-step__io" markdown="1">

**输入**：当前不变量$i_j$的草图$K_j$、处理后的语料库$P$以及依赖顺序$G_D$。<br>
**输出**：当前不变量的PROSA专用上下文$R_j$，包含相关定义、假设、引理、证明范例及可恢复的前置依赖。

</div>

**直观理解**：系统不是只用命题中的关键词搜索，而是从“要证明什么、为什么成立、最后得到什么”三个角度查资料。把候选引理的依赖一起取回，可避免模型看到一个可用结论，却缺少调用该结论所需的定义或前提。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 依赖有序的证明骨架生成与验证

骨架模块$M_{\mathrm{skel}}$按$G_D$规定的顺序增量生成对应代码块$s_j$，显式组织变量、假设、类型类实例、章节上下文、定义和证明声明。对引理、定理或推论中尚未完成的证明体暂时使用`Admitted.`，形成可继续处理的结构骨架；原文称该阶段会生成并验证结构正确的骨架，但所给节选未明确报告具体验证循环。

<div class="method-step__io" markdown="1">

**输入**：当前草图$K_j$、检索上下文$R_j$、依赖图$G_D$以及此前已生成的部分脚本$S_{<j}$。<br>
**输出**：与$i_j$对应的PROSA/ROCQ代码块$s_j$及其中可能存在的延迟证明义务，连续处理后形成部分脚本。

</div>

**直观理解**：这相当于先保证程序文件的导入、声明和接口都按正确顺序搭好，再处理最困难的证明内容。占位符把“形式环境搭建”和“证明搜索”分开，降低一次生成数百行完整上下文与证明的难度。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 总体机械化映射

$$
M:(A,P)\rightarrow S,\qquad S=\{s_1,s_2,\ldots,s_n\}
$$

**符号说明**

- $M$：PROVE-RT的整体生成流水线。
- $A$：待机械化的实时系统可调度性分析。
- $P$：经过切块和加工的PROSA文档语料库。
- $S$：最终生成的、按依赖排序的PROSA/ROCQ脚本。
- $s_j$：脚本中用于形式化第$j$个系统不变量$i_j$的代码块。
- $n$：从输入分析中抽取的系统不变量数量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式定义了论文要解决的整体问题：系统接收一篇尚未形式化的分析和一个库专用知识源，输出完整机械化脚本。它不是可训练损失函数；其约束由语义对应、依赖顺序和最终编译通过共同构成。<br>
**原文位置**：第IV-B节，Problem Statement

</div>

</div>

<div class="equation-block" markdown="1">

#### 分阶段代码与证明生成

$$
M_{\mathrm{skel}}:(K_j,R_j,G_D,S_{<j})\rightarrow s_j,\qquad M_{\mathrm{proof}}:(S_{<j},s_j,K_j,R_j)\rightarrow\pi_j
$$

**符号说明**

- $M_{\mathrm{skel}}$：为当前不变量生成结构化PROSA/ROCQ代码骨架的模块。
- $M_{\mathrm{proof}}$：补全当前代码块中延迟证明义务的模块。
- $K_j$：第$j$个不变量的非形式化草图，包含陈述、直觉和证明提纲。
- $R_j$：从PROSA语料库中为第$j$个不变量检索出的相关上下文。
- $G_D$：系统不变量的依赖有向无环图。
- $S_{<j}$：处理第$j$个不变量前已经生成的脚本部分。
- $s_j$：当前不变量对应的代码块，其中可暂含延迟证明占位符。
- $\pi_j$：用于替换当前延迟证明占位符的ROCQ证明片段。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项映射负责把当前目标放进正确的形式环境，第二项映射才负责填入证明。两者都利用此前脚本和检索资料，但证明补全额外读取当前代码块$s_j$，因为具体证明目标与局部上下文只有在骨架建立后才完全显现。<br>
**原文位置**：第IV-B节，Skeleton Generation与Proof Completion

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文将PROVE-RT描述为LLM辅助的生成与编译修复流水线，没有在所给章节中提出新的参数化模型、监督训练损失或强化学习目标，因此不存在可据此复现的训练目标。这里的“目标”是系统级验收条件而非梯度优化函数：每个$s_j$应忠实表示$i_j$，脚本顺序必须符合$G_D$，且替换所有待完成证明后的$S$必须由PROSA/ROCQ环境成功检查。编译成功提供确定性的形式验证信号，但它只证明脚本在给定形式化陈述和假设下成立；原论文到形式陈述之间是否发生语义偏移，还需检查不变量抽取和草图是否忠实。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 依赖感知的中间表示**

中间表示由$I$、$\{K_j\}$和$G_D=(I,D)$组成；边$(i_p,i_j)\in D$表示$i_j$依赖$i_p$，因此$i_p$对应代码必须先于$i_j$出现。$K_j$既保存目标陈述，也保存推理直觉和证明提纲，从而连接原论文表达与PROSA代码生成。

> 直观理解：ROCQ不能引用尚未声明的对象，而可调度性定理又常建立在多层任务模型、到达约束、工作量和干扰界之上。这一模块把隐含在论文叙述中的先后关系显式化，防止模型生成内容正确但排列后无法编译的脚本。

**2. PROSA专用检索模块**

该模块从$P$中为每个$i_j$选择$R_j$，并针对证明密集模块保留代码与说明的配对关系、恢复所检索构件的依赖。查询由$K_j$的statement、intuition和conclusion三个部分独立发起，再合并各自的前$k$名候选。

> 直观理解：通用LLM缺少PROSA特有的抽象、类型类条件和证明惯例，仅凭论文内容容易使用不存在的定义或漏掉前提。检索模块为当前步骤提供可核对的库内范例与接口，但检索相关不等于一定可复用，生成模块仍须满足被检索引理的全部前置条件。

**3. 骨架生成、证明补全与编译器闭环**

框架把代码生成分解为$M_{\mathrm{skel}}$和$M_{\mathrm{proof}}$：前者依据$K_j$、$R_j$、$G_D$和$S_{<j}$生成$s_j$的整体结构，后者依据当前证明环境生成$\pi_j$。证明片段只有在替换`Admitted.`后通过ROCQ编译检查才被接受，失败时以编译反馈或证明状态驱动修复。

> 直观理解：分阶段设计避免模型同时解决环境声明、依赖排序和策略搜索三个问题。它先确保“题目和上下文写对”，再集中完成“如何证明”，并用证明助理本身过滤语法正确但类型或逻辑不成立的候选。

**训练与推理**

所给方法属于推理时编排。离线准备阶段将PROSA六类模块加工为语料库$P$：Analysis与Results按证明单元切块并绑定说明文字，其余模块按章节切块；所给节选未说明是否微调底层LLM。在线阶段对输入分析$A$运行受提示约束的不变量抽取，得到$I$、$\{K_j\}$和$G_D$，再按$G_D$逐个处理$i_j$：使用$K_j$的陈述、直觉和结论检索并合并候选，构造$R_j$；将$K_j$、$R_j$、$G_D$和$S_{<j}$交给骨架模块生成$s_j$；对其中的`Admitted.`调用证明模块生成$\pi_j$，替换后交由ROCQ检查，并依据错误或证明状态修复。当前代码块被接受后才继续扩展脚本，最终得到$S$。

**复现信息**

公平解释该方法时，需要保留三项实现选择：第一，文档切块区分证明密集的Analysis/Results与其余模块，因为前者需要保存代码、文字说明和依赖，Results还承担完整证明示例来源；第二，检索以单个$K_j$为单位，并将statement、intuition和conclusion拆成三个查询后合并前$k$候选；第三，生成必须按$G_D$增量进行，并将骨架中的未完成证明显式延后，再以ROCQ编译器反馈形成修复闭环。所给节选没有明确报告底层LLM名称及版本、嵌入或排序模型、相似度函数、$k$值、提示全文、采样参数、上下文长度、依赖恢复算法、编译环境版本、修复轮数上限与终止条件；这些信息不能从当前材料中补造，且会显著影响复现结果。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- PROVE-RT System Invariant Dataset：源论文首先来自 RTSS、RTAS、ECRTS、EMSOFT、RTCSA、RTNS、RSS 和 IROS 等会议。IEEE Xplore API 返回 1,991 条论文记录，下载、去重后约有 1,870 篇唯一论文；经依赖解析和结构验证，最终保留 1,191 篇论文及 13,134 个带依赖信息的非形式化草图。该语料既为框架提供输入，也用于研究从可调度性分析到 PROSA/ROCQ 脚本的自动机械化。原文未明确报告训练集、验证集和测试集的划分。
- 人工整理的评测集：论文摘要说明最终成功率是在一个 curated evaluation set 上测得，但所给章节未说明其样本数、抽样方式、所含论文范围以及它与 13,134 个草图语料之间是否重叠。因此，该评测集的作用可以确定为比较 PROVE-RT 与直接生成基线，但无法从当前材料判断其代表性或数据泄漏风险。
- PROSA 检索语料：由 PROSA 的 CoqDoc HTML 文档加工而成，共包含 356 个源文件中的 5,097 个文档片段。Analysis 和 Results 模块采用面向证明的切分，并为检索结果补充相关依赖；其他模块采用章节级切分。该语料不是待证明样本集，而是在骨架生成阶段向模型提供 PROSA 定义、假设、引理和证明范式的外部知识库。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Success Rate**

成功率定义为 $N_S/N_T$，其中 $N_S$ 是成功机械化且生成了有效证明脚本的草图数，$N_T$ 是被评测草图总数。一个脚本只有在 ROCQ 检查器无错误接受、不含遗留的延迟证明义务、通过证明完整性检查并以 Qed 完成时才计为成功。 （越高越好，因为它表示完整通过形式证明检查的样本比例更大；该指标衡量端到端机械化是否成功，而不是代码表面相似度或自然语言答案质量。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 完整 PROVE-RT 在人工整理评测集上的端到端机械化

<div class="result-value" markdown="1">

PROVE-RT 的成功率为 44.7%，即约四成半被评测草图最终产生了通过 ROCQ 检查与完整性要求的证明脚本。

</div>

作者据此主张，依赖感知草图、PROSA 文档检索、分阶段骨架生成和证明补全的组合能够支持一部分真实可调度性分析的自动机械化。分析上，这个结果表明任务并非完全超出当前 LLM 能力，但超过半数样本仍未成功。由于当前材料未给出评测集规模、成功样本数及不确定性区间，不能据此估计该比例在更广泛实时系统文献中的稳定性。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On a curated evaluation set, direct prompting of state-of-the-art LLMs fails to reliably generate valid PROSA mechanizations, whereas PROVE-RT achieves a success rate of 44.7%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 系统不变量语料构建与结构过滤

<div class="result-value" markdown="1">

经过下载去重、LLM 抽取和确定性依赖验证后，最终语料保留 1,191 篇论文和 13,134 个非形式化草图。

</div>

该结果主要证明作者建立了一个规模较大的、面向机械化且带依赖关系的实时系统语料资源，为检索、生成和后续研究提供输入。它不是证明生成准确率，也不能说明 13,134 个草图均已由专家确认语义正确；当前节选仅明确报告了结构验证和过滤。

<div class="result-source" markdown="1">

来源：Section VII-A, System Invariant Dataset Construction

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

After this filtering step, the retained corpus contained 1,191 papers and 13,134 informal sketches.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 保留语料中形式构造类别的分布

<div class="result-value" markdown="1">

13,134 个规范化不变量中，定义有 6,817 个，占 51.9%；引理有 4,144 个，占 31.6%；定理有 1,822 个，占 13.9%，其余为推论、递归定义和假设。

</div>

分布显示评测对象以定义和引理为主，而不是只包含最终定理。这与 PROVE-RT 先恢复依赖、再按顺序生成形式构造的设计相符，也说明总体成功率会同时受到建模声明和证明步骤的影响。不过，该类别统计只描述语料组成，不能直接证明模型在哪一类构造上更强；当前材料没有报告分类别成功率。

<div class="result-source" markdown="1">

来源：Table I, Distribution of extracted elements by category

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

TOTAL 13134 100.0% 73

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

- 原始论文文本直接生成：LLM 只接收目标不变量在原始可调度性分析论文中的对应文本，不获得 PROSA 外部文档，也不经过骨架代码生成。它检验通用模型能否直接跨越自然语言论证与 PROSA 形式化接口之间的差距。
- 非形式化草图直接生成：LLM 接收经过抽取的目标不变量草图，但不使用检索支持和骨架生成阶段。与第一种基线相比，它控制了输入结构化程度；与完整 PROVE-RT 相比，它用于检验仅有草图是否足以完成机械化。
- BM25 检索：采用基于词项匹配的稀疏检索，从 PROSA 文档中为每个查询选取前 $K=5$ 个片段。它适合匹配精确的库名、定义名和调度术语，是评估词法检索是否足够的参照。
- 稠密检索与混合检索：稠密检索使用 nomic-embed-code-7b 生成向量并存入 FAISS，以语义相似度选择前 $K=5$ 个片段；混合检索结合稀疏与稠密信号。三种策略的比较旨在隔离检索方式对最终证明成功率的影响，但当前节选没有给出各策略的结果。

**实验想回答的问题**

- RQ1：PROVE-RT 能在多大程度上把实时系统文献中的可调度性测试形式化为可被 PROSA/ROCQ 接受的证明脚本？
- RQ3：BM25、稠密检索与混合检索等不同文档检索方法，会如何影响 PROVE-RT 的机械化成功率？

**实验实现**

系统不变量抽取使用 Gemini-2.5-Flash，并通过带少样本示例和约束条件的提示处理 GROBID 生成的结构化 XML。依赖验证器依次执行精确、规范化和模糊匹配；模糊匹配仅在字符级相似度超过 $0.88$ 时连接最高分候选。存在依赖环或未解析依赖比例高于 $0.15$ 的论文被拒绝。证明阶段使用 Claude-Opus-4.6：第一阶段生成含 Admitted. 的骨架，用于先检查声明、类型和类型类解析；第二阶段逐个消除证明义务，并可使用线性整数算术自动化策略。系统通过自动脚本与 ROCQ 9.1.0 交互。检索时分别以不变量的陈述、直觉和结论构造查询，每个查询选取前 $K=5$ 个文档片段。实验运行环境为 Python 3.10、Ubuntu 24.04 LTS、12 核 24 线程 Intel Xeon w5-3423 和 64GB 内存；原文未明确报告模型温度、随机种子、重复运行次数、置信区间或统计显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：核心贡献是通过检索与分阶段生成提升 LLM 构造形式化定理证明脚本的代码和逻辑推理能力。; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`ddc0ca8ce53ed4eea0e1749350e0f2ecab8105c353c4b01c742b6a87d92c3469`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
