---
title: "[论文解读] Change2Task: From Repository Changes to Executable Coding Agent Tasks and Environments"
description: "[arXiv 2607.28591][LLM Agent] Change2Task研究如何把历史合并请求中由开发者真实意图支撑的软件变更，迁移到同一仓库健康、现代的后继版本上，并将其构造成可执行、可验证且可复用环境的编码智能体任务。"
arxiv_id: "2607.28591"
announcement_date: "2026-07-31"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.313593+00:00"
source_sha256: "1b86d4050945ca38e35d7a0ffe1427f47a586effee3d65f74de66b6c74cb7b27"
tags:
  - "LLM Agent"
  - "LLM 评测"
  - "编码智能体"
  - "可执行任务"
  - "仓库历史"
  - "拉取请求"
  - "环境工程"
  - "任务重建"
  - "现代仓库修订"
  - "可执行验证"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2607.28591</p>

# Change2Task: From Repository Changes to Executable Coding Agent Tasks and Environments

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Qi, Haomin, Wang, Xingliang, Gao, Xuanqi, Sang, Baihui, Zhang, Xin, Ma, Minghua, Gao, Pengfei, Kang, Yu, Lin, Qingwei, Rajmohan, Saravan, Zhang, Dongmei, Zhang, Qi</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.28591) · [PDF 下载](https://arxiv.org/pdf/2607.28591) · **关键词** 编码智能体, 可执行任务, 仓库历史, 拉取请求, 环境工程, 任务重建, 现代仓库修订, 可执行验证<br>


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

Change2Task研究如何把历史合并请求中由开发者真实意图支撑的软件变更，迁移到同一仓库健康、现代的后继版本上，并将其构造成可执行、可验证且可复用环境的编码智能体任务。

**不用术语来说**：训练和评测编码智能体不能只有自然语言题目，还需要一套真正能安装依赖、编辑代码、运行工具并自动判断答案是否正确的软件环境；但为每道题单独准备和保存环境成本很高，而旧合并请求虽然包含真实需求、补丁和测试，通常只能在当时的旧代码版本上直接使用。本文要解决的是：怎样利用已经维护好的现代仓库环境，把这些真实历史变更重新变成今天仍能运行和验证的任务。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出并实现Change2Task：以历史合并请求及其健康后继版本为输入，按“补丁逆转、代码映射、智能体重建”三级路径逐步处理代码演化造成的不一致，并通过健康态、任务态和恢复态的生命周期检查，构造带恢复补丁的可执行任务。
- 建立面向多类维护任务的统一适配与复用思路：从开发者描述、实现补丁和行为证据中定义任务目标、预期输出、可执行判定器与编辑范围，使同一现代基础环境能够承载多个轻量任务变体，兼顾真实维护意图与环境工程成本。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

仓库级编码智能体不只生成代码，还会在真实软件仓库中检索文件、修改实现、调用构建与测试工具，并依据执行反馈反复修正。因此，一个可执行任务必须同时包含可运行的仓库状态、依赖与开发工具、任务规格以及能够判断成功与否的验证器；论文将构造这一执行基础的工作称为“环境工程”。现有历史基准通常把任务固定在旧版本，现代环境构建系统则主要解决仓库能否运行的问题，尚未充分回答如何从一个已维护、可运行的现代仓库版本中低成本地产生多个具有真实开发依据的任务。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**仓库级编码智能体**

能够在完整软件仓库中查看代码、编辑多个文件、运行命令和测试，并根据反馈迭代求解的自动化系统。其能力评估依赖真实的仓库状态和可执行验证，而不能只比较生成文本。

</div>
<div class="concept-item" markdown="1">

**可执行编码任务**

将任务说明、特定仓库状态、依赖与工具以及成功判据绑定在一起的评测或训练单元。智能体提交修改后，系统通过构建、测试或其他行为检查判断任务是否完成。

</div>
<div class="concept-item" markdown="1">

**合并拉取请求**

拉取请求（PR）记录开发者提出并已合入仓库的维护变更，通常包含自然语言描述、代码补丁和测试等行为证据。Change2Task把它视为真实维护意图的来源，而不是凭空合成任务目标。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一项已经合并的历史PR，以及同一仓库中位于其后的、固定且可正常运行的现代修订版本。历史PR提供任务描述、开发者实现补丁与行为证据，现代修订提供共享的健康执行环境；系统假设二者具有共同仓库血缘，但代码结构、接口和依赖可能已经演化。目标是在现代基础版本上重建一个尚未完成该维护目标的“任务状态”，同时生成可将其恢复到正确状态的补丁，并验证健康基础状态、任务状态和恢复状态之间的完整生命周期。最终产物是可供编码智能体训练或评测的成对任务，其任务目标、预期输出、可执行判定器和允许编辑范围由适配器定义，可覆盖缺陷修复、功能添加、测试生成、API迁移与安全修复等不同任务族。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **SWE-bench**: 代表基于真实开发者问题、补丁和测试的历史任务基准，但任务通常绑定于原始历史修订。Change2Task保留这种开发者证据，同时把维护事件迁移到同一仓库的健康现代后继版本。
- **SWE-smith PR Mirror**: 与本文最接近：它让模型在当前仓库中撤销历史PR，并保留能够破坏目标测试的候选任务。论文指出该方法侧重单一构造操作与修复目标，而Change2Task通过补丁反转、代码映射和智能体重建三级策略适应代码演化，并以统一验证核心支持多种任务目标。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

编码智能体通过搜索仓库、修改文件、调用工具和根据测试反馈反复修正来完成任务，因此每个训练或评测样本都必须同时提供可运行的仓库状态、依赖与开发工具、任务说明以及可靠的自动验证机制。可执行环境的供给由此成为数据规模与多样性的瓶颈；若继续为每个任务制作独立快照，还会重复消耗镜像构建、存储、注册表传输、冷启动和批量运行资源。实际需求不是单纯增加题目文本，而是提高每个已维护、可运行仓库环境能够产出的可靠任务数量。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **绑定原始版本的历史任务或基准**：从真实问题单、合并请求、开发者补丁和测试中提取任务，并保留任务发生时的仓库版本。其优势是需求和正确修改都有真实开发历史作为依据，但执行环境通常停留在旧修订上。
- **在预先准备仓库中的新鲜任务合成**：以已经能够构建和测试的仓库为基础，自动注入故障或生成可验证任务，从同一环境批量制造训练与评测实例；文中以面向修复任务的SWE-smith为代表。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 历史任务与原始旧修订绑定，难以直接利用持续维护的现代代码和统一环境；若为每项历史任务继续保留专用快照，就会放大环境搭建、镜像存储和运行调度成本，也使任务随依赖及工具链演化而逐渐陈旧。
- 新鲜合成能够扩大实例数量，却未必对应开发者曾经处理过的真实维护意图；人工注入的失败与真实缺陷、功能新增、接口迁移或安全修复之间可能存在分布差异，因而不能同时保证规模、现实性和历史证据的可追溯性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有路线尚未提供一种通用机制，将历史合并请求中的描述、补丁与行为证据和同一仓库的健康现代后继版本对齐，在代码结构、测试和接口已经演化的情况下重建任务，同时验证任务确实能从健康态进入待解决状态、再经正确修改恢复，并支持多种维护任务共享现代基础环境。该空缺位于“真实历史依据”和“现代环境复用”之间，而不是单纯缺少更多历史样本或更多合成样本。

</div>
<div markdown="1"><span>核心问题</span>

在要求来源可追溯、行为可执行验证、修改范围受控且结果可恢复的前提下，能否把合并请求代表的历史维护变化可靠地迁移到健康的现代仓库修订上，从每个现代基础环境构造更多编码智能体任务，并减少重复环境工程开销？

</div>
<div markdown="1"><span>作者直觉</span>

合并请求已经提供了任务构造所需的三类关键线索：开发者描述说明“要做什么”，实现补丁说明“曾经怎样做”，测试或其他行为证据说明“怎样判断完成”；现代后继版本则提供较健康、较易维护的执行底座。若旧改动仍与现代代码直接对应，就可以逆转补丁制造待解决状态；若位置或结构改变，则先映射相关代码；只有直接对应失效时才让智能体依据历史证据重建。由易到难逐级升级，比对所有任务一律重新合成更能保留真实意图，也比把任务永久冻结在旧版本上更利于共享环境。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Change2Task把已合并拉取请求（PR）视为开发者留下的任务证据，但不直接复用其容易失效的历史环境。系统先从PR中提取修改意图、实现补丁和可执行检查，再在同一仓库谱系中冻结一个健康的现代后继版本$H$；随后通过补丁反转、代码映射和智能体重构三级策略生成任务补丁$D$，得到待修复状态$C$，并构造恢复补丁$G$。候选任务只有在健康态、任务态和恢复态组成的完整生命周期中，同时通过目标检查、回归检查、作用域约束和历史忠实度验证，才会被固化为可执行任务。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 从历史PR派生任务证据

系统识别PR改变的条件及其可观察方式，划分目标检查与回归检查，并建立源变更画像，记录受影响组件、文件、代码块、行、符号和检查范围。若修改意图含混、检查无法执行，或目标修改不能与无关改动分离，则直接排除候选。

<div class="method-step__io" markdown="1">

**输入**：同一仓库历史中已合并PR的描述、合并前后版本$V_{\mathrm{pre}}$与$V_{\mathrm{post}}$、源补丁$P_s$以及可执行检查。<br>
**输出**：带有PR来源信息的任务证据，包括目标检查、回归检查和源变更画像。

</div>

**直观理解**：这一步相当于从一次真实开发活动中整理出三件事：究竟要改变什么、怎样证明改变成功，以及哪些邻近功能不能被破坏。它防止系统仅凭补丁表面差异猜测任务。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 建立并对齐健康现代基座

系统按固定优先级选取同一谱系中的后继提交作为健康现代基座$H$，在构造前冻结其提交哈希，并验证检出、依赖、服务及检查均可运行。随后进行PR对齐，在重构、文件移动、API变化或测试重组后定位历史行为在现代代码中的对应实现；映射后的目标检查与回归检查必须都在$H$上通过。

<div class="method-step__io" markdown="1">

**输入**：任务证据、仓库版本谱系，以及声明的健康版本、目标版本或可访问的上游默认分支。<br>
**输出**：可复现且可执行的现代基座$H$、历史到现代代码及检查的对齐关系，以及任务目标、输出契约、验证预言机和允许编辑范围组成的任务规格。

</div>

**直观理解**：系统不是回到旧版本搭建一次性环境，而是在仍受维护的新版本中寻找同一功能的现代落点。只有确认新版本当前是健康的，而且旧PR讨论的行为仍然存在，后续制造出的失败才可归因于任务补丁。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 逐级构造任务状态与恢复补丁

系统按从保守到自适应的三级策略构造任务补丁$D$：先尝试直接反转源补丁；失败后尝试结构引导的代码映射；仍失败时由构造智能体在最多四轮内提出受限候选，并经应用、语法、构建和作用域检查筛选。对通过初筛的$D$，系统生成逆变换或等价现代修复$G$，使$C=\mathrm{apply}(H,D)$能够恢复为$H^{\prime}$。

<div class="method-step__io" markdown="1">

**输入**：健康基座$H$、PR证据、源补丁$P_s$、源变更画像、现代对齐关系和任务规格。<br>
**输出**：现代任务状态$C$、任务补丁$D$、恢复补丁$G$及候选构造轨迹；无可辩护的现代行为宿主或耗尽预算的候选被拒绝。

</div>

**直观理解**：三级策略像是先尝试原样撤销旧修复，再尝试把旧代码块搬到新位置，最后才让智能体按证据重建同一种缺陷或缺失能力。升级顺序优先保留开发者原始修改的结构，同时为代码长期演化留下适应空间。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 验证三状态生命周期并冻结任务

系统要求目标检查在$H\rightarrow C\rightarrow H^{\prime}$上呈现“通过、暴露任务条件、再次通过”，而回归检查始终通过；重复执行用于排除不稳定案例。作用域门禁止修改受保护检查或元数据来伪造有效性，忠实度门则比较现代实现与源PR的受影响组件、编辑规模和检查表面，拒绝任务范围坍缩或无关膨胀。

<div class="method-step__io" markdown="1">

**输入**：候选$H$、$D$、$C$、$G$、$H^{\prime}$、两类检查、任务规格和源变更画像。<br>
**输出**：冻结的可执行任务变体，包含$H$、$D$、$G$、目标与回归检查、任务规格及源PR来源；只有通过生命周期、作用域和忠实度验证的变体进入评测。

</div>

**直观理解**：一个合格任务必须证明三点：原系统本来正常，制造任务后只出现预期问题，应用标准恢复后问题消失。这样可以避免把环境故障、测试篡改或大范围无关改动误包装成编码任务。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 历史变更与现代任务的双分支生命周期

$$
V_{\mathrm{pre}}\xrightarrow{P_s}V_{\mathrm{post}},\qquad H\xrightarrow{D}C\xrightarrow{G}H^{\prime}
$$

**符号说明**

- $V_{\mathrm{pre}}$：历史PR合并前的仓库状态。
- $P_s$：历史PR的源补丁，把合并前状态变为合并后状态。
- $V_{\mathrm{post}}$：应用源补丁后的历史仓库状态。
- $H$：从同一仓库谱系选择并冻结的健康现代基座。
- $D$：Change2Task构造的任务补丁，用于在现代基座上形成待处理条件。
- $C$：应用任务补丁后的现代任务状态，即编码智能体实际接收的仓库状态。
- $G$：恢复补丁，用于从任务状态恢复预期健康行为。
- $H^{\prime}$：应用恢复补丁后的状态；要求在相关行为上等价于健康基座，但不要求文本完全一致。

<div class="equation-explanation" markdown="1">

**直观理解**：左侧记录开发者当年如何从旧问题状态走到旧修复状态，右侧则把同一维护意图迁移到现代代码：先从健康版本制造任务，再证明它可以被修复。该式明确区分“历史证据链”和“现代可执行任务链”，也是整个系统的核心问题设定。<br>
**原文位置**：Methodology开头，四阶段生命周期记号。

</div>

</div>

<div class="equation-block" markdown="1">

#### 现代任务状态构造

$$
C=\operatorname{apply}(H,D)
$$

**符号说明**

- $C$：呈现指定维护条件的现代任务状态。
- $\operatorname{apply}$：把补丁应用到仓库状态的操作。
- $H$：已验证健康且固定提交哈希的现代基座。
- $D$：由三级构造过程产生并受作用域约束的任务补丁。

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定任务不是一份自然语言描述，而是由明确基座和补丁决定的可执行仓库状态。因而同一任务可以被复现、验证和恢复，也能把环境问题与任务本身区分开。<br>
**原文位置**：Methodology，Constructing the Task State小节。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。Change2Task是任务与环境构造系统，原文没有定义模型训练损失或通过梯度更新参数；Level 3调用现成构造智能体生成候选补丁，但任务最终是否接受由确定性的应用、语法、构建、作用域、生命周期和忠实度门决定，而不是用下游编码智能体的求解结果优化任务。原文还明确说明，下游智能体结果不会用于选择或修改任务，以避免评测数据对被测智能体产生结果导向的偏置。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. PR证据对齐与任务适配器**

对齐模块把历史PR中的行为、实现和检查映射到现代后继版本，并要求对应目标及回归检查在健康基座$H$上成立。其上方的任务适配器共享同一构造核心，但按任务族改变目标和预言机：Bug Fix制造未修复行为，Feature Addition移除能力，Test Generation形成可观察失败，API Migration恢复旧API用法，Security Repair引入沙箱化漏洞。

> 直观理解：对齐模块回答“旧PR在新代码里对应哪里”，适配器回答“要把这段历史证据包装成哪一种任务”。两者分离后，系统可以复用同一套可靠性验证，而不必为每种任务类型重新设计完整流水线。

**2. 三级渐进式任务状态构造器**

Level 1仅在现代上下文兼容时反转$P_s$，因而与开发者修改保持最直接的结构联系。Level 2寻找现代文件中唯一对应的历史修改后代码块，允许规范化缩进，并以重新缩进的修改前代码块替换它；Level 3接收PR证据、现代上下文、任务规格及先前失败反馈，最多尝试四次受限补丁，再按源变更画像忠实度和编辑复杂度排序候选。

> 直观理解：直接反转最可信但覆盖面有限，结构映射可以处理文件移动和局部重构，智能体重构则用于代码形态已显著变化但行为仍存在的情况。智能体不是自由改写仓库，其候选始终受任务范围、可执行检查和历史画像约束。

**3. 生命周期、作用域与忠实度验证器**

生命周期验证器在$H$、$C$和$H^{\prime}$三个状态执行目标检查与回归检查，并验证$G$确实恢复相关健康行为，而非要求$H^{\prime}$与$H$文本完全相同。作用域门限制可编辑工件并保护检查与元数据；忠实度门依据文件、代码块、变更行、符号、目标检查和回归检查六个维度比较历史源补丁与现代恢复补丁，防止现代任务明显变简单或扩大为无关重构。

> 直观理解：只检查“任务状态会失败”不足以证明任务有效，因为失败可能来自环境损坏或测试作弊。这个模块把行为可恢复性、邻近功能稳定性和修改规模合理性同时纳入准入条件。

**训练与推理**

系统运行时先离线处理历史PR：提取可执行证据，选择并冻结健康现代基座$H$，完成历史行为到现代代码的对齐，并实例化任务规格。构造阶段按Level 1到Level 3顺序执行，只有当前一级无法产生有效候选时才升级；Level 3在最多四次尝试中利用结构化失败反馈继续提议补丁，反馈可指出目标条件未满足、回归检查损坏、恢复失败或忠实度偏离。候选通过全部验证后，系统输出供训练或评测使用的任务状态$C$及其环境、规格和验证预言机；编码智能体随后只需在$C$中按规格编辑允许范围内的工件，其输出由冻结的目标检查与回归检查判定。

**复现信息**

公平复现所必需的约束包括：现代基座必须来自同一仓库谱系，版本解析在任务构造前完成并冻结提交哈希；历史基座回退需要单独记录，不能计为现代基座。基座必须支持干净检出、运行时依赖与服务，并能执行目标和回归检查；Change2Task假设原生配置或外部准备工具已使基座可运行。Level 2只进行一次结构引导尝试，要求源代码块到现代代码块的对应关系唯一，替换后重新解析并接受与其他候选相同的作用域和可执行门；Level 3最多四轮。重复运行用于拒绝不稳定任务，最终产物必须同时保存$H$、$D$、$G$、两类检查、任务规格和源PR来源，以支持复现、审计和统一评测。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 构造候选集：来自 12 个公开基准集合及其发布版本的 1,130 个“可构造源变更”。纳入条件是同时具有源 PR 证据、可执行检查，以及同一仓库中满足前置条件的基础版本。它用于测量 Change2Task 从候选变更到最终已验证任务的构造成功率。
- 配对任务语料：构造流程得到 900 个配对集合，包括 500 个 Bug Fix，以及各 100 个 Feature Addition、Test Generation、API Migration 和 Security Repair。每个集合含两个来源关联的分支：历史修订上的官方基准 Original Branch，以及在同仓库健康现代修订上重构的 Change2Task Branch；这种一一配对用于控制任务意图与来源差异，并比较迁移前后的可解性。
- 五类任务族：Bug Fix 要修复错误行为；Feature Addition 要实现缺失行为；Test Generation 要添加一个在任务态失败、恢复态通过且仅改测试范围的测试；API Migration 要把过时 API 调用替换成指定目标 API；Security Repair 要消除由确定性沙箱预言机暴露的漏洞。五类任务用于检验系统是否能覆盖不同产物和验证契约，而不只是传统缺陷修复。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**已验证任务恢复率**

在 1,130 个可构造源变更中，最终通过生命周期、修改范围、保真度和语义资格检查并进入成品语料的比例。该指标同时衡量任务能否被构造，以及构造结果是否满足论文定义的可执行质量门槛。 （越高越好，因为更高比例表示同样数量的真实历史变更能转化为更多经过完整验证的任务。）

</div>
<div class="metric-item" markdown="1">

**匹配结果一致率**

在相同代理和受控评测条件下，历史 Original Branch 与现代 Change2Task Branch 是否得到一致求解结果的比例。它用于检查任务迁移后是否大体保留原任务的经验难度与可解性。 （越高越好，因为更高一致率意味着现代重构任务更可能保留历史任务的评测行为；但它不等同于逐文件、逐轨迹或语义上的完全等价。）

</div>
<div class="metric-item" markdown="1">

**完整流水线测量开销**

任务构造与评测完整流程中的总体资源支出，用于检验复用健康现代基础环境是否减少重复环境安装、存储和任务准备成本。 （越低越好，因为开销下降表示在维持任务供给和验证要求时，系统运行更经济。原文节选未给出开销的具体计量单位与分项定义。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RQ1：在全部 1,130 个可构造源变更及五类任务上进行端到端任务构造与验证。

<div class="result-value" markdown="1">

作者报告 Change2Task 的已验证任务构造成功率为 79.6%，对应流程最终形成 900 个配对任务集合。

</div>

这表示约五分之四的合格输入变更能够经过重构及多重质量门后成为可执行任务，说明该方法并非只在少量人工挑选案例上有效。该数字以已经满足证据、检查和同仓库基础版本条件的 1,130 个变更为分母，因此不能解释为任意 PR 或任意仓库都有 79.6% 的转化率，也不能单独证明五个任务族的成功率完全均衡。

<div class="result-source" markdown="1">

来源：摘要；RQ1 的指标定义见 Experiments > RQ1，构造路线与终止拒绝原因见 Figure 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Starting from 1,130 source changes eligible for construction, Change2Task achieves 79.6% verified task construction success across these task families.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 在匹配候选集上，将 Change2Task 与基于拉取请求的任务构造基线比较。

<div class="result-value" markdown="1">

作者报告 Change2Task 恢复的已验证任务数量比该基线多 29.2%。

</div>

这个相对增幅表明，历史证据对齐、现代版本上的状态重构和验证流程能够挽回一部分传统 PR 构造流程无法产出的任务，因而直接支持“扩大可执行任务供给”的主张。由于所给节选未报告两种方法的绝对任务数、置信区间及逐任务族增幅，该结果不能说明收益来自哪一种重构路线，也不能据此判断所有仓库都能获得相同比例的提升。

<div class="result-source" markdown="1">

来源：摘要；相关构造路线与终止拒绝原因见 Figure 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On a matched candidate set, it recovers 29.2% more verified tasks than a construction baseline based on pull requests.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 对来源匹配的 Original Branch 与 Change2Task Branch 进行受控多代理评测，并测量现代基础版本复用带来的完整流水线开销变化。

<div class="result-value" markdown="1">

作者报告历史案例与重构案例的匹配结果一致率最高达到 98.0%，同时现代基础版本复用使完整流水线的测量开销降低 10.8%。

</div>

最高 98.0% 表明在至少一个已报告评测条件下，现代重构分支与历史分支通常给出相同的解决或未解决结论；10.8% 的下降则说明共享或复用现代健康环境可能减少重复准备成本。这里的“最高”不是所有任务族、代理或设置的总体一致率，而且结果一致只比较最终评测结论，不证明代理轨迹、代码补丁或运行时行为完全相同。节选也未给出开销单位和统计不确定性，因此成本收益仍需结合完整论文核查。

<div class="result-source" markdown="1">

来源：摘要；评测控制条件见 Experiments > Experiment Setup > Construction and evaluation agents

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Historical and reconstructed cases achieve up to 98.0% matched outcome agreement under agent evaluation, while reuse of modern bases reduces measured expenditure across the complete pipeline by 10.8%.

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

- 基于拉取请求的任务构造基线：在匹配候选集上与 Change2Task 比较已验证任务数量。该基线有意义，因为两者都从真实开发变更出发，而 Change2Task 额外利用历史证据对齐、现代基础版本复用及多种状态重构路线；因此比较直接检验这些设计是否扩大可用任务供给。
- Original Branch：官方基准任务在历史修订上的原始环境。它不是任务构造算法基线，而是配对代理评测中的参照条件，用来判断 Change2Task Branch 迁移到现代修订后是否保持相近的求解结果。
- Change2Task Branch：同一任务在同仓库健康现代修订上的重构版本。它与 Original Branch 在任务意图、模型、接口、可见证据、权限、上下文策略、预算和验证器强度方面保持一致，从而把结果差异主要归因于任务状态与基础版本的变化。

**实验想回答的问题**

- RQ1：Change2Task 能否从具备拉取请求证据、可执行检查和同仓库基础环境的历史变更中，可靠地构造通过生命周期、范围、保真度与语义资格验证的可执行任务？
- 在候选变更和评测条件匹配时，Change2Task 相比基于拉取请求的构造基线能否恢复更多已验证任务；将历史任务迁移到现代健康版本后，任务结果是否仍与原始历史版本一致，并能否降低完整流水线开销？

**实验实现**

Agent Reconstruction 使用 Claude Code 与 Opus 4.8，在有界循环中生成、执行并迭代候选重构。代理评测使用四种配置：Codex CLI/GPT-5.5、Claude Code/Sonnet 5、Gemini CLI/Gemini 3.1 Pro，以及 GitHub Copilot/GPT-5.6 Terra；每个代理在每个分支上只运行一次干净试验。配对内部固定任务意图、模型、交互接口、可见证据、权限、上下文策略、预算和验证器强度，且评测代理不能访问构造轨迹、任务补丁、恢复补丁或隐藏目标检查。任务只有在任务族专用预言机、回归检查和修改范围门全部通过时才计为解决。该协议的核心是使历史分支与现代重构分支尽量只在代码状态和环境年代上不同；不过单次运行仍可能受到代理随机性的影响。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：构建将代码仓库历史变更转换为可执行、可验证编码Agent任务和环境的系统，服务于训练与持续评测。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`1b86d4050945ca38e35d7a0ffe1427f47a586effee3d65f74de66b6c74cb7b27`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
