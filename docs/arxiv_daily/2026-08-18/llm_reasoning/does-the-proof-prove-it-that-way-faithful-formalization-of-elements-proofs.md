---
title: "[论文解读] Does the Proof Prove It That Way? Faithful Formalization of Elements Proofs"
description: "[arXiv 2608.15432][LLM Reasoning] 本文研究如何把自然语言证明形式化为不仅能被 Lean 验证、而且忠实保留原论证步骤、结构与引用依赖的形式证明。"
arxiv_id: "2608.15432"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:28:44.791825+00:00"
source_sha256: "d704f4ea2069c3e2f8499a50dd082c11a814cd1816864fcb182d20e5c3734bb1"
tags:
  - "LLM Reasoning"
  - "自动形式化"
  - "形式化验证"
  - "证明忠实性"
  - "Lean"
  - "自然语言证明"
  - "欧几里得几何"
  - "《几何原本》"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.15432</p>

# Does the Proof Prove It That Way? Faithful Formalization of Elements Proofs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Tadd Mao, Tianjun Zhong, Dhruva Arekar, Yuming Feng, One An, Jiani Huang, Xujie Si, Ziyang Li</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.15432) · [PDF 下载](https://arxiv.org/pdf/2608.15432) · **关键词** 自动形式化, 形式化验证, 证明忠实性, Lean, 自然语言证明, 欧几里得几何, 《几何原本》<br>


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

本文研究如何把自然语言证明形式化为不仅能被 Lean 验证、而且忠实保留原论证步骤、结构与引用依赖的形式证明。

**不用术语来说**：证明助手通常只检查最终形式证明是否成立，却不检查它是否沿用了原文的推理方式。因此，自动系统可能绕开自然语言证明中的关键步骤，另找一条更短的证明路径；这样即使代码成功编译，也无法判断原论证本身是否正确，更不能准确指出其中遗漏、错误或不充分的步骤。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出五项形式证明忠实性的必要条件，把过去主要依赖主观语义判断的“是否忠实”问题转化为更明确、可检查的结构要求；作者同时强调这些条件只是必要条件，尚不足以完整刻画证明者的全部意图。
- 作者提出 Pistis：先在 Map Stage 中把自然语言证明映射为保持原结构的分层子目标，再由 OrderDecompose 逐层完成证明，并通过引用依赖约束、顶层结构保护和反驳搜索，避免自动化策略绕过原论证，同时暴露无法填补的推理缺口。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于形式化验证与数学自动形式化领域。自动形式化将自然语言数学转写为 Lean 等证明助理能够机械检查的形式语言；其中，命题形式化负责准确表达待证结论，证明形式化则给出可通过内核检查的推理过程。以往工作通常把“代码能够编译、定理能够闭合”作为主要成功标准，但一个自动搜索得到的形式证明即使结论正确，也可能绕开原自然语言论证。本文因此关注证明的忠实性：形式证明不仅要证明同一命题，还应保留自然语言证明得出结论的推理结构、步骤对应关系和引理引用依赖。研究场景是欧几里得几何，目标材料为《几何原本》前三卷的自然语言命题及证明，形式化平台为 Lean。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**证明助理与形式证明**

证明助理是用严格形式语言表达定义、命题和证明，并由可信内核逐步检查推理是否合法的软件。形式证明能够编译只表示系统接受其逻辑正确性，并不自动保证它复现了原自然语言证明的论证方式。

</div>
<div class="concept-item" markdown="1">

**证明策略（tactic）与证明状态**

在 Lean 中，证明策略是对当前待证目标和已有假设进行变换的操作，连续执行策略可最终关闭目标。自然语言证明按数学句子推进，而形式系统按证明状态变换推进，这种粒度与结构的不一致是忠实形式化的主要困难之一。

</div>
<div class="concept-item" markdown="1">

**证明忠实性**

本文所称忠实性，是形式证明能够反映自然语言论证如何抵达结论，包括保留主要证明结构、逐步对应原文推理，并在原文指定的位置使用相应命题或公理。它比“证明同一个结论”要求更强，因为自动化捷径可能得到正确结论，却掩盖原论证中的缺步或错误。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括自然语言命题及其逐句论证、论证中显式引用的既有命题或共同概念，以及已经给定的 Lean 形式命题；输出是能够通过 Lean 检查、同时忠实对应原论证的形式证明。本文以欧几里得《几何原本》前三卷共 92 个命题为主要设置：自然语言证明可能省略人类认为显然、但 Lean 必须显式说明的步骤，也可能包含引用错误或真正的推理缺口，因此系统既要补全必要细节，又不能用与原证明无关的自动化捷径替代其数学结构。图 1 的 Proposition I-6 展示了区别：直接使用叠合论证或用一次自动化策略合并多个句子，都可关闭给定目标，却没有逐句体现欧几里得的反证、分类、构造和引理引用；忠实版本则要求自然语言中编号的推理步骤与形式步骤明确对应，并在无法证明某一步时暴露该缺口。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$a,b,c$**

Lean 形式命题中的三个几何点，对应三角形的顶点。

</div>
<div class="notation-item" markdown="1">

**$AB,BC,AC$**

连接相应顶点的直线对象，用于表达三角形的边及其几何关系。

</div>
<div class="notation-item" markdown="1">

**$\angle a:b:c$**

以点 $b$ 为顶点、由点 $a$ 与点 $c$ 确定的角。

</div>
<div class="notation-item" markdown="1">

**$|(a-b)|$**

点 $a$ 与点 $b$ 之间线段的长度；示例结论 $|(a-b)|=|(a-c)|$ 表示三角形两边相等。

</div>

</div>

**直接相关的工作**

- **System E（Avigad, Dean, and Mumma, 2009）**: 该工作为欧几里得证明提供忠实形式模型，是本文关于“形式证明应保留原数学论证”的直接理论背景；本文进一步面向自然语言证明到 Lean 证明的自动化流程，并强调可检查的步骤与引用依赖。
- **LeanEuclid（Murphy et al., 2024）**: 这是与本文实验和问题设置最直接相关的既有 Lean 欧几里得形式化工作，并已主张关注忠实性。本文指出其证明中可能由自动化步骤一次关闭多个自然语言推理步骤，因而把它作为比较对象，以研究更细粒度的逐句对应和证明结构保留。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

数学家、学生或 AI 给出的自然语言证明需要被检查的，不只是结论是否为真，还包括“文中写出的理由是否足以推出结论”。若形式化工具只生成任意一个可编译证明，它就可能掩盖原证明的漏洞，无法承担逐步验证、错误定位、教学讲解以及把证明草稿整理为可维护形式成果等任务。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **面向定理闭合的自动证明搜索**：这类方法把形式化后的定理陈述作为整体目标，搜索一串 Lean tactic 或一个证明项，只要最终关闭目标并通过内核检查即可。它保证所得形式证明有效，但通常不要求搜索过程与自然语言证明的句子、构造顺序或引用关系对应。
- **基于粗粒度语义匹配的忠实性评估**：既有工作可让 LLM 充当评审者，比较自然语言证明与形式证明在语义上是否相似；部分形式化成果也保留若干原文构造，但会用强自动化 tactic 一次解决多个步骤。此类方法主要提供整体相似度或主观判断，不能逐项认证每个形式步骤是否确实来自原论证。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 证明助手的 tactic 按“变换证明状态”运行，而自然语言证明按数学句子和论证结构推进；若直接搜索整个定理，系统容易采用与原文不同的捷径，导致“证明可编译”却不能证明原文论证有效。
- 自然语言经常省略人类认为显然、但形式系统必须显式提供的步骤；既有粗粒度评估既难区分合理补全与改变证明结构，也难在子目标失败时判断究竟是搜索能力不足、原文存在缺口，还是引用本身错误。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种端到端机制，能够在补全必要隐含步骤的同时锁定自然语言证明的高层结构、句子顺序和命题引用依赖，并在某一步无法成立时给出可定位的失败或反驳，而不是用其他证明路径掩盖问题。更根本地说，领域中还缺少足够精确、可操作的忠实性标准；论文试图以五项必要条件推进这一问题，但并未声称已经得到充分条件。

</div>
<div markdown="1"><span>核心问题</span>

能否构造一种受明确忠实性条件约束的 Lean 证明搜索方法，使生成证明逐步对应给定自然语言论证、只补充形式系统必需的缺失步骤、正确使用原文引用，并能在原论证有漏洞或错误时定位乃至反驳相关步骤？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是先分段、后搜索：不让自动化系统直接寻找关闭整个定理的任意路径，而是先把每个自然语言推理单元固定为有顺序、有层级且带引用依赖的形式子目标，再逐个填充。直观上，这相当于先规定必须经过哪些检查点，再允许系统寻找检查点之间的局部推导；局部失败因而会暴露在对应原句附近，自动化也更难跳过原作者真正依赖的论证。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Pistis 将“忠实形式化”定义为一个带结构对应关系的证明生成问题。输入为四元组 $\langle P_{\mathrm{NL}},\operatorname{formal}(P_{\mathrm{NL}}),F_{\mathrm{NL}},\Delta\rangle$：自然语言命题、已写成 Lean 的命题、自然语言证明，以及 System E 几何公理集。与只寻找任意可编译证明不同，系统输出 $\langle\bar\phi,\bar s,\operatorname{assumps}(\cdot),\operatorname{assert}(\cdot),\operatorname{formal}(\cdot)\rangle$，其中 $\bar s$ 是自然语言证明的句段划分，$\bar\phi$ 是按推理顺序排列的形式步骤，另外三个映射分别记录每个句段使用的前提、作出的断言及其形式对应。输出需满足覆盖性、原子性、原子忠实性、顺序性和引用约束；可靠性则由 Lean 编译单独保证。作者强调，这些条件只是忠实性的必要条件，因为形式证明必须补出原文省略的推理，无法与原文完全逐字同构。

端到端流程分为 map 和 fill 两阶段。map 阶段让大语言模型代理把自然语言证明逐句映射成含 `sorry` 的 Lean 模板，并由脚本或人工 oracle 反复检查结构性条件；fill 阶段调用 OrderDecompose，严格按模板中的步骤顺序证明各个占位目标。若短时 SMT 无法直接解决某个目标，算法让模型提出中间引理，先验证这些引理是否足以推出当前目标、其前提是否能由当前上下文提供，再递归证明引理。通俗地说，map 阶段先制作一份不能随意改动的“逐句施工图”，fill 阶段只负责补齐施工图中缺失的论证，因此系统较难用另一条更方便但不忠于原文的证明路线替代作者路线。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 问题规范化与忠实证明表示

系统把前提公式视为 $\alpha=\alpha_1\land\cdots\land\alpha_m$，记录其中的自由变量 $v_1,\ldots,v_k$，并把目标从“生成一个证明项”细化为“生成形式步骤、自然语言句段及二者映射”。最终形式步骤必须按顺序构成从 $\Delta\cup\{\alpha\}$ 推出 $\beta$ 的证明。

<div class="method-step__io" markdown="1">

**输入**：自然语言命题 $P_{\mathrm{NL}}$、其 Lean 形式化 $\operatorname{formal}(P_{\mathrm{NL}})=\alpha\to\beta$、自然语言证明 $F_{\mathrm{NL}}$ 和 System E 公理集 $\Delta$。<br>
**输出**：待构造的结构化对象 $\langle\bar\phi,\bar s,\operatorname{assumps}(\cdot),\operatorname{assert}(\cdot),\operatorname{formal}(\cdot)\rangle$ 及其忠实性检查规范。

</div>

**直观理解**：普通自动证明只关心终点是否正确；这里还要保存沿途每一步，并说明它对应原文哪一句、使用了哪些原文前提。这样才能区分“证明了同一个定理”和“按原文所述方式证明了定理”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. Map 阶段：生成逐句形式模板

LLM 代理将 $F_{\mathrm{NL}}$ 顺序切分为 $\bar s=\{s_1,\ldots,s_n\}$，从每个 $s_i$ 中抽取前提子串 $\operatorname{assumps}(s_i)$ 和唯一断言 $\operatorname{assert}(s_i)$，再把它们映射到含 `sorry` 的 Lean 步骤序列 $\bar\phi'$。脚本检查覆盖、顺序等可机械验证条件，人工 oracle 检查原子性和局部语义忠实性；不通过时由 oracle 要求模型修订并重复检查。

<div class="method-step__io" markdown="1">

**输入**：完整输入四元组，以及自然语言证明中的句子和引文信息。<br>
**输出**：映射模板 $M=\langle\bar\phi',\bar s,\operatorname{assumps}(\cdot),\operatorname{assert}(\cdot),\operatorname{formal}(\cdot)\rangle$，其中 $\bar\phi'$ 预期成为最终证明 $\bar\phi$ 的子序列。

</div>

**直观理解**：这一阶段像给原文逐句加编号并搭出证明骨架：每句话只能表达一个主要断言，而且不能调换句序或漏掉句子。骨架暂时允许有空洞，但后续填洞时不能偷偷改写这份逐句对应关系。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. Fill 阶段：按序递归填充证明

OrderDecompose 依次处理 $\phi'_1$ 到 $\phi'_{N'}$；对每个目标先构造适用的上下文假设，再调用 Decomp 尝试在 30 秒 SMT 预算内直接关闭。若直接搜索失败，模型提出中间引理 $h^{(j)}\to\omega^{(j)}$；算法只保留能共同推出当前目标且前提可由上下文供应的引理，并递归证明各 $\omega^{(j)}$。

<div class="method-step__io" markdown="1">

**输入**：假设 $\alpha$、映射阶段留下的有序子目标 $\phi'_1,\ldots,\phi'_{N'}$、结论 $\beta$、公理集 $\Delta$ 和 LLM $\mathcal M$。<br>
**输出**：若全部目标均闭合则返回 `True`，并将生成的中间步骤 $\kappa_1,\ldots,\kappa_t$ 插入对应模板位置，形成可由 Lean 检查的完整证明；模型决定放弃时返回 `False`。

</div>

**直观理解**：算法不是把整个难题一次交给模型，而是按原文顺序逐格填空；一格太难时，再拆成更小的辅助结论。每次拆分都要先证明“这些小结论确实够用”以及“它们没有凭空要求当前上下文中不存在的条件”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 验证、缺口识别与反驳

系统检查 Lean 可编译性、每个形式步骤的引用是否合法，以及除允许填充的部分外映射模板是否未被改变；可选阶段还会把每个形式前提具体化为 `have` 并用自动策略尝试证明。若证明失败，系统区分模型能力、映射错误、实现限制与原文问题；对原文问题，可报告未闭合的假设缺口，或通过导出断言为假、构造满足原前提但违反断言的对象配置来反驳证明。

<div class="method-step__io" markdown="1">

**输入**：填充后的 Lean 脚本、固定的 map 对象、句段引用关系，以及可选的假设缺口检测结果。<br>
**输出**：被接受的忠实形式证明，或带位置的 gap 标记，或证明原论证错误的形式反例；无法判定具体原因时则得到失败状态供 oracle 检查。

</div>

**直观理解**：最后不只是问“代码能不能运行”，还要问它有没有改施工图、有没有提前引用后文、原文省略的条件能否真正推出。缺一步但尚未造成矛盾被记为缺口；若能证明某一步错误或找到满足题设却使该步失败的几何配置，则构成反驳。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 结构化忠实形式化输出

$$
\left\langle \bar\phi,\bar s,\operatorname{assumps}(\cdot),\operatorname{assert}(\cdot),\operatorname{formal}(\cdot)\right\rangle,\qquad \Delta\cup\{\alpha\}\vdash\beta
$$

**符号说明**

- $\bar\phi=\{\phi_i\}_{i=1}^{N}$：最终形式证明的有序步骤序列，每一步可由公理、题设和此前步骤推出
- $\bar s=\{s_i\}_{i=1}^{n}$：自然语言证明按原顺序切分得到的句段序列
- $\operatorname{assumps}(s_i)$：句段中被当前推理使用的自然语言前提子串集合
- $\operatorname{assert}(s_i)$：句段作出的唯一主要断言子串
- $\operatorname{formal}(\cdot)$：把自然语言前提或断言映射到对应形式公式的函数
- $\Delta$：System E 的形式几何公理集合
- $\alpha$：待证命题的形式假设，可分解为若干假设公式
- $\beta$：待证命题的形式结论
- $\vdash$：右侧公式可在左侧公理和假设下被形式推导

<div class="equation-explanation" markdown="1">

**直观理解**：该表达式把论文的关键目标从“得到一个类型为定理的 Lean 项”提升为“得到一个能逐句对齐的证明包”。其中 $\Delta\cup\{\alpha\}\vdash\beta$ 保证数学结论可证，其余组成部分则保存自然语言与形式推理之间的结构关系。<br>
**原文位置**：第 3.1 节 Problem Definition，Output

</div>

</div>

<div class="equation-block" markdown="1">

#### 单个模板步骤的填充条件

$$
\Delta\cup\left\{\alpha,\phi'_1,\ldots,\phi'_{i-1},\kappa_1,\ldots,\kappa_t\right\}\vdash\phi'_i
$$

**符号说明**

- $\phi'_i$：map 阶段产生、当前需要证明的第 i 个模板步骤
- $\phi'_1,\ldots,\phi'_{i-1}$：按照原文顺序已经处理的先前模板步骤
- $\kappa_1,\ldots,\kappa_t$：fill 阶段为关闭当前目标而生成并插入的中间形式步骤
- $i$：当前模板步骤的顺序索引
- $t$：为当前步骤生成的中间步骤数量

<div class="equation-explanation" markdown="1">

**直观理解**：填充阶段不能跳过原文步骤直接证明最终结论，而要让每个 $\phi'_i$ 都能由公理、题设、此前原文步骤和新补出的局部推理推出。证明成功后，$\kappa_1,\ldots,\kappa_t$ 被插到 $\phi'_i$ 前面，这既补齐隐含推理，又保留 map 阶段确定的原文主干顺序。<br>
**原文位置**：第 3.2 节 Approach Overview，Fill stage

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文描述的是基于 LLM 代理、Lean、SMT、脚本检查和人工 oracle 的推理时证明构造流程，没有提出用于训练或微调模型的损失函数，也没有报告通过梯度下降优化 Pistis 的过程。算法中的“充分性”“可供应性”“引用合法性”和“可编译性”属于候选证明的离散验收条件，而不是可微训练目标；因此不能把上述逻辑公式解释为机器学习优化目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 忠实性条件与混合检查器**

五项结构性条件为：Coverage 要求 $s_1,\ldots,s_n$ 按原顺序拼接回 $F_{\mathrm{NL}}$；Atomicity 要求每个 $s_i$ 只有一个断言；Atomic Faithfulness 要求句段的每个前提和断言都被忠实形式化；Order 要求各断言对应的形式式在 $\bar\phi$ 中保持子序列关系；Citation 要求句段引用的命题对应于当前断言之前的形式步骤。Coverage、Order 和 Citation 由脚本检查，Atomicity 与 Atomic Faithfulness 由人工 oracle 检查，Soundness 则由 Lean 内核检查。

> 直观理解：单靠 Lean 只能排除逻辑上无效的代码，不能判断代码是否照着原文走；单靠人工又难以稳定核对长证明的顺序和引用。因此系统把字符串覆盖、步骤先后等明确规则交给脚本，把“这句话究竟表达什么”留给专家，并把最终逻辑可靠性留给 Lean。

**2. OrderDecompose 与递归 Decomp**

OrderDecompose 固定按 $\bar\phi'$ 的顺序处理目标，并在每个目标通过可供应性、可靠性、引用约束和模板不变性检查前持续重试。核心 Decomp 先运行受限 SMT；失败后由 CreateLemmas 生成若干条件引理，计算充分性 $S_F$ 与可供应性 $S_P$，再对每个辅助结论递归调用 Decomp，从而把开放式 LLM 搜索约束为可即时机器检验的分治搜索。

> 直观理解：LLM 擅长猜测可能有用的中间结论，却不保证猜测正确。该模块让模型只负责提出候选，再立即用证明器检查“够不够”和“能不能用”，因此错误候选不会直接进入最终证明。

**3. Gap 与 Refutation 分析器**

假设缺口检测器把 $\operatorname{assumps}(s_i)$ 对应的形式前提逐一放入 Lean `have` 语句并尝试自动关闭，未关闭者以 `sorry` 标出并加入后续子目标。反驳器寻找两类证据：在 $\Delta\cup\{\alpha\}$ 下可推出某句断言的否定，或存在自由变量 $v_1,\ldots,v_k$ 的实例使 $\alpha$ 成立而该断言不成立；前者直接否定所述步骤，后者给出反模型。

> 直观理解：原文没写出的内容不一定是错误：它可能只是作者默认读者会补出的步骤，所以系统把这种情况记为 gap。只有当系统能正式证明某句不可能成立，或展示满足题设却破坏该句的具体配置时，才把证明判为被反驳。

**训练与推理**

原文只明确描述推理流程。首先，LLM 代理在 map 阶段切分自然语言证明，抽取每句的前提和断言，并生成带 `sorry` 的 Lean 模板；脚本与人工 oracle 检查各自负责的忠实性条件，不合格时把问题反馈给代理修订。其次，可选的 gap 检测阶段尝试自动证明每个形式假设，并把未闭合假设显式加入模板。然后，fill 阶段执行 OrderDecompose：按顺序取出一个模板目标，构造当前可用假设，先进行最多 30 秒的 SMT 直接搜索；失败时由 LLM 借助代理工具提出中间引理，算法检查这些引理是否足以关闭目标以及前提是否可从当前上下文获得，再递归处理辅助结论。每个模板目标还必须通过 Citation、Lean 可靠性和模板未被篡改等检查。全部目标成功时输出完整证明；返回 `False` 时，由 oracle 判断是模型能力、映射错误、System E 实现限制，还是原证明或译文存在问题，并可在修正映射后恢复搜索。

**复现信息**

公平复现所必需的实现约束有四点。第一，形式环境采用 Lean，并以 System E 公理集 $\Delta$ 作为几何推理基础；最终 Soundness 由 Lean 编译且不得含 `sorry` 来确认。第二，Decomp 的每次直接 SMT 尝试使用 30 秒预算，目的是维持快速的生成—验证反馈循环；原文节选未给出 SMT 求解器名称或硬件配置。第三，LLM 通过 skill files 接收通用算法指令，通过 agentic hooks 防止“cheating”，并可调用代理工具辅助 CreateHypothesis 与 CreateLemmas；具体模型、提示模板和工具细节被指向附录，但本节选未完整提供，故不能进一步确定。第四，检查责任必须保持一致：Coverage、Order、Citation 等确定性结构条件由脚本检查，Atomicity 与 Atomic Faithfulness 由人工 oracle 判断，Lean 负责逻辑可靠性；若 oracle 误标映射，应允许修正后从原位置继续 OrderDecompose。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 评测对象为欧几里得《几何原本》第 I–III 卷，共包含 92 个命题；原文明确指出第 I 卷有 48 个命题、第 II 卷有 14 个命题，但所给节选没有完整报告第 III 卷的数量、样本筛选条件或训练/验证/测试划分。该集合用于评价形式化证明的忠实性、证明补全、Lean 编译速度以及证明缺口识别能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**形式化证明忠实性**

衡量生成的 Lean 证明是否沿用了教材证明中的关键依赖关系和推理路线，而不只是借助更强或更晚出现的结果得到同一结论。节选中出现的“Major dependency mismatch”说明评价会关注重要依赖缺失、被后续更强结果替代，或引用方式与教材不一致等问题。 （忠实程度越高越好，因为论文目标不仅是让证明通过 Lean 检查，还要求形式化证明准确反映教材的证明方式；所给节选未给出该指标的具体量表或聚合公式。）

</div>
<div class="metric-item" markdown="1">

**fill 阶段完成能力**

衡量系统能否补全分解后留下的形式化证明缺口，用于比较完整 Pistis 与不含 OrderDecompose 的裸大语言模型。 （成功完成的命题或证明缺口越多越好；但所给节选未明确报告成功率的定义、统计单位或数值。）

</div>
<div class="metric-item" markdown="1">

**Lean 证明编译速度**

比较 Pistis 生成的证明与 LeanEuclid 证明通过 Lean 编译或检查所需的时间，以考察生成证明的计算开销。 （编译时间越短越好，因为这表示证明检查成本更低；所给节选未说明计时口径、硬件环境、重复次数或统计方法。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给节选缺失第 4 节的大部分实验内容，包括完整数据构成、指标定义、主结果表、消融数值、速度测量协议及案例全文。因此无法返回三个有证据支持的主结果，也不能验证作者是否充分回答四个研究问题。
- 即使完整论文报告了忠实性得分，该评价仍可能依赖人工判断或特定依赖匹配规则；当前节选没有说明标注者数量、一致性、盲评方式及对等价证明路线的处理，因此该指标的客观性与可复现性尚无法判断。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- LeanEuclid（Murphy et al., 2024）：已有的《几何原本》Lean 形式化版本，是回答忠实性比较和编译速度比较问题的主要基线。它具有可比性，因为 Pistis 与 LeanEuclid 面向相同的几何命题；但所给节选未说明二者是否使用相同的公理库、辅助引理和编译环境。
- 不使用 OrderDecompose 的裸大语言模型：用于检验 fill 阶段的成功是否来自 OrderDecompose，而非语言模型本身的证明生成能力。所给节选未提供模型名称、提示词、采样参数或该基线的具体得分。

**实验想回答的问题**

- RQ1：与 LeanEuclid 相比，Pistis 生成的形式化证明在多大程度上忠实于《几何原本》中的原始证明思路？
- RQ2：OrderDecompose 是否是完成 fill 阶段的必要组件，还是不使用该组件的裸大语言模型也能独立完成这一阶段？

**实验实现**

作者围绕四类问题组织系统评测：与 LeanEuclid 比较证明忠实性；移除 OrderDecompose，测试裸大语言模型能否完成 fill 阶段；比较两类证明的编译速度；通过定性案例观察 Pistis 如何反驳证明并发现证明缺口，包括教材翻译中的缺口。评测覆盖《几何原本》第 I–III 卷的 92 个命题。由于所给来源节选在“4.1 Evaluation Setups”开头即被截断，模型版本、Lean 版本、公理与引理环境、运行硬件、重复次数、人工标注流程及统计显著性检验均无法从当前材料确认。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除 OrderDecompose，仅使用裸大语言模型执行 fill 阶段。 | 原文未明确报告 | 该消融隔离 OrderDecompose 的作用：若移除后完成能力明显下降，才能支持该组件负责把顺序或结构约束转化为语言模型更容易补全的子问题。当前节选只提出了比较问题，没有给出结果，因此不能断言该组件是必要的，也不能量化其贡献。 | 第 4 节 Evaluation，RQ2<br><span class="experiment-evidence">RQ2. Is OrderDecompose necessary, or can a bare LLM complete the fill stage on its own?</span> |

**定性案例**

- 作者计划定性分析 Pistis 如何反驳证明并识别证明缺口，包括教材翻译中的问题。节选还展示了一类“Major dependency mismatch”：最重要的引用依赖缺失，被更强的后续结果替代，或依赖的使用方式与教材不一致。这说明案例分析关注的是形式化证明与原文推理结构之间的实质偏差，而非语句表面的差异；但节选没有提供完整案例及最终判定，因而无法评估诊断是否准确。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work focuses on faithful formalization of mathematical proofs, directly targeting reliable structured reasoning and proof generation.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`d704f4ea2069c3e2f8499a50dd082c11a814cd1816864fcb182d20e5c3734bb1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
