---
title: "[论文解读] MemTxn: A Transaction Boundary for Source-Supported Updates and Complete-State Recovery in Agent Memory"
description: "[arXiv 2607.27834][LLM Agent] MemTxn将可写智能体记忆的更新与故障恢复视为应用级事务，通过来源支持校验、冲突版本选择和完整状态恢复，防止错误事实被持久化、错误版本对回答可见以及多键故障留下混合状态。"
arxiv_id: "2607.27834"
announcement_date: "2026-07-31"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.225151+00:00"
source_sha256: "0f79840a31e0a21a2817120af0ec36de7b68268d29ef17dba318f512af348ebb"
tags:
  - "LLM Agent"
  - "智能体持久记忆"
  - "可写记忆"
  - "应用级事务"
  - "来源支持"
  - "时间冲突解析"
  - "完整状态恢复"
  - "快照日志"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2607.27834</p>

# MemTxn: A Transaction Boundary for Source-Supported Updates and Complete-State Recovery in Agent Memory

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Cui, Hanshuai, Tang, Zhiqing, Yao, Zhi, Meng, Fanshuai, Ma, Qianli, Jia, Weijia</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27834) · [PDF 下载](https://arxiv.org/pdf/2607.27834) · **关键词** 智能体持久记忆, 可写记忆, 应用级事务, 来源支持, 时间冲突解析, 完整状态恢复, 快照日志<br>


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

MemTxn将可写智能体记忆的更新与故障恢复视为应用级事务，通过来源支持校验、冲突版本选择和完整状态恢复，防止错误事实被持久化、错误版本对回答可见以及多键故障留下混合状态。

**不用术语来说**：长期运行的智能体会把对话事实、用户偏好和任务状态保存下来，但一次错误提取可能长期影响后续回答：新事实可能没有被原文真正支持，多个互相冲突的版本可能选错，更新中断还可能只改成功一部分数据。现有记忆系统主要解决“保存什么、取回什么”，数据库的原子写入也只保证底层写操作的完整性，不能判断一条记忆在语义上是否应当写入，更不能自动确定故障后应恢复的完整业务状态。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者指出可写智能体记忆缺少明确的“事务边界”，并将其拆分为三个相互独立且可审计的契约：候选更新必须得到来源支持、冲突事实必须按预先声明的规则确定可见版本、故障后必须恢复完整的应用可见状态。
- 作者提出位于回答模型之外的 MemTxn 治理层：Ordered PatchTest 在提交前检查候选值与引用文本的有序词汇支持，Temporal Resolver 按时间契约处理版本冲突，持久化快照日志则在不掌握实际物理写集合的情况下恢复经审计的活动状态映射。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究长期运行的大语言模型智能体的可写持久记忆。此类系统会把对话事实、用户偏好和任务状态保存到模型外部，并在后续会话中检索和更新；因此，错误提取、事实冲突或部分写入不仅影响当前回答，还可能成为持久状态并持续污染未来行为。既有工作主要优化记忆的存储、检索、压缩、组织及时间关系建模，而本文关注更基础的状态治理问题：一次候选更新是否有来源支持、多个冲突版本中哪一个应对回答模型可见，以及发生持久化故障后应恢复哪一份完整的应用可见状态。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**可写持久记忆**

指智能体能够跨会话保存并修改的模型外部状态，例如用户偏好、事件和任务事实。它不同于当前提示中的临时上下文，因为错误一旦写入，可能在数据库重开后仍然存在。

</div>
<div class="concept-item" markdown="1">

**应用级事务边界**

事务边界规定一组状态变更何时可以提交、提交后哪个版本可见，以及失败时应恢复到什么状态。本文强调，底层存储的原子写入只能保证物理操作整体成功或失败，不能自动判断更新在语义上是否受到原始证据支持。

</div>
<div class="concept-item" markdown="1">

**状态前像**

状态前像是一次更新或故障发生前，应用原本可见的完整状态快照。保存此前像使系统能够整体恢复，而不是只撤销某一个已知键并留下新旧状态混合的结果。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

系统处于长期运行、记忆可被持续写入且回答模型与记忆治理层分离的设置。输入包括候选记忆更新及其引用的来源片段、可能彼此冲突的事实版本，以及故障前持久化的应用状态；治理层不能借助金标准答案、基准标签或未来查询来决定是否提交。它需要输出三类决定：仅允许满足预先声明的来源支持条件的更新提交；在发生版本冲突时，依据明确的时间顺序契约选择对回答模型可见的版本；当数据库重开后仍存在不变量违例或持久多键故障时，恢复完整的、经审计声明为活跃的应用可见映射。关键假设是一次逻辑更新可能同时改动版本、指针、事实键和事件记录等多个物理键，而且恢复阶段未必知道实际被写坏的物理键集合。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **MemGPT（Packer et al., 2023）**: MemGPT管理短期与长期记忆层，代表面向容量和层级管理的智能体记忆系统；本文则补充其未明确提供的语义提交契约、冲突版本可见性规则与完整状态恢复边界。
- **检索增强生成与稠密段落检索（Lewis et al., 2020；Karpukhin et al., 2020）**: 这些方法根据相关性从外部证据中选择内容以支持下游生成，但检索相关性并不能证明候选写入受到来源支持，也不能规定冲突后的持久版本或故障恢复目标。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

持久记忆会跨会话影响智能体决策，因此写入错误具有累积性和长期性。候选事实即使与来源共享大量词语，也可能因词序或否定极性变化而表达相反含义；一次逻辑更新还可能同时修改版本、指针、事实键和事件记录等多个物理键。若系统错误接纳前一种更新，或在后一种更新失败后只撤销单个键，错误或自相矛盾的状态会在数据库重新打开后继续污染未来任务。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **检索、反思与自主记忆管理方法**：这类方法从情景经历或外部语料中检索相关内容，并通过反思、记忆分层、结构化存储、压缩、时间关系建模或学习到的记忆操作来决定保留和调用哪些信息。其主要目标是提高记忆的相关性、组织效率与回答可用性。
- **数据库原子写入与局部撤销机制**：这类机制在存储层约束物理写入，使一组已知操作全部完成或全部失败，或在异常后撤销某个已记录的键。它们关注底层数据操作的一致性，而不负责解释候选事实是否受来源支持，也不定义智能体业务层面哪个事实版本应当可见。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 相关性、时间新近性和学习到的记忆动作都不能构成提交契约：它们不要求候选值由所引用的来源片段支持，也没有把“回答时找不到证据而临时回退”与“拒绝把不可信事实永久写入”区分开。若改用标准答案、基准标签或未来查询监督写入，又会把评测信号泄漏进持久状态。
- 存储原子性只能约束物理操作，不能识别应用层应恢复的完整前像；单键撤销尤其无法覆盖一次逻辑更新涉及的所有版本、指针、事实和事件键。因此，持久化多键故障可能留下新旧数据并存的混合状态，并在重新打开存储后继续违反系统不变量。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一个位于回答模型与存储系统之间、同时覆盖“写入准入、冲突可见性和完整恢复”的应用级治理边界。这个边界还必须在不访问答案监督的条件下判断来源支持，并在不知道故障实际改写了哪些物理键时，仍能恢复故障前完整的应用可见状态。

</div>
<div markdown="1"><span>核心问题</span>

如何在无答案监督的条件下，仅依据候选更新及其引用来源决定该状态能否提交，并按明确的时间冲突契约选择对回答模型可见的版本；同时，如何在持久化多键故障发生且实际物理写集合未知时，恢复完整、预期的应用状态？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把记忆更新类比为应用级事务，而不是把它仅当作一次检索或数据库写入。提交前先检查候选事实是否能由来源文本按声明的顺序直接支撑，可以拦截那些表面词汇高度重合、实际却改变词序或否定含义的错误；冲突出现时使用固定的时间规则，可避免回答模型临时猜测版本；更新前持久化完整活动映射的前像，则让恢复过程以“恢复整个可见状态”为目标，而不必事后猜测究竟哪些底层键写坏了。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MemTxn 是部署在回答模型之外的持久记忆治理层，目标不是训练一个更会回答问题的模型，而是在记忆写入、冲突读取和故障恢复三个边界上提供可审计的确定性规则。系统把逻辑时刻 $t$ 的状态表示为 $S_t=(\mathcal{V}_t,A_t,\mathcal{J}_t)$：$\mathcal{V}_t$ 是只追加的版本集合，$A_t$ 是从规范化事实键 $\kappa$ 到当前版本标识的活动指针映射，$\mathcal{J}_t$ 保存持久化状态事件与恢复意图；应用实际看到的状态为 $\Pi_{\rm app}(S_t)=A_t$。上游抽取器提出包含键、值、证据、来源及时间信息的更新 $q$，MemTxn 先验证该值是否按原顺序受到所引来源文本支持，通过后才创建新版本并原子切换活动指针。查询时仅在检测到跨来源、异值冲突后调用 Temporal Resolver，按声明的时间规则选择可见版本；没有冲突时沿用 Dense 原始文本块。发生持久故障时，系统依据事务开始前保存的完整活动映射 $A_0$ 做补偿恢复，而不是猜测故障影响了哪些物理行。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造更新提案并限定信任边界

系统检查规范化键 $\kappa$、候选值 $v$、证据片段 $e$、来源标识 $s$ 和时间元数据 $\nu$ 是否齐全，并只允许 Ordered PatchTest 读取提案字段和 $D_s$。候选值、提案器和可写子系统均不可信，基准答案、故障标签及安全标签不参与运行时决策。

<div class="method-step__io" markdown="1">

**输入**：上游抽取器给出的 $q=(\mathrm{id},\kappa,u,r,v,e,s,\nu)$，以及不透明来源标识 $s$ 指向的原始来源文本 $D_s$。<br>
**输出**：字段完备、来源可定位且可送入支持性验证的提案，或一个不改变持久状态的拒绝结果。

</div>

**直观理解**：这一步像先核对报销单是否填全、附件是否确实来自所声明的文件；测试集答案不能被拿来帮助系统“猜对”是否应写入。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 验证来源支持并原子激活版本

Ordered PatchTest 要求证据确实是来源文本的规范化子串，并要求候选值的内容词元序列 $T(v)$ 是证据词元序列 $T(e)$ 的有序子序列。若验证通过，系统创建带版本标识、父指针、生命周期状态和提交时间的版本 $z$，以当前 $A_t(\kappa)$ 为父版本并原子更新指针；否则保持持久状态不变。

<div class="method-step__io" markdown="1">

**输入**：提案 $q$、证据 $e$、来源文本 $D_s$，以及当前活动映射 $A_t$。<br>
**输出**：状态为 Active 的新版本及审计记录，或状态为 Rejected 的提案；每次决定记录规范化证据、谓词分量、父版本和最终状态。

</div>

**直观理解**：规则不只检查新值中的词是否“出现过”，还检查出现顺序，因此能拦截部分否定词插入、来源外替换和词序篡改。写入是否成立在此处已经决定，后续回答模型不能靠一次看似正确的回答挽救不受支持的更新。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 检测冲突并选择回答上下文

系统按时间顺序贪心规范化键：键完全相同或主语—关系 Jaccard 相似度至少为 $0.60$ 时视为同类候选；不同来源的值既不完全相同、其 Jaccard 相似度又未达到 $0.80$ 时触发冲突路由。对每个冲突键，Temporal Resolver 选择 $\nu(q)$ 最大的候选，时间并列时依来源顺序和提案标识确定性打破平局；无合格冲突则使用 Dense 原始块。

<div class="method-step__io" markdown="1">

**输入**：查询相关候选、规范化的主语—关系表示、来源标识、候选值及时间元数据 $\nu$。<br>
**输出**：提供给回答模型的受治理版本上下文，或常规 Dense 检索上下文；该输出只影响本次回答，不授权任何写入。

</div>

**直观理解**：系统先判断“这些记录是否在谈同一件事且互相矛盾”，再按应用预先声明的最新版本优先规则选材料。它只决定回答时看哪个版本，并不声称最新记录在现实世界中一定为真。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 持久化恢复意图并审计故障

控制器先持久化 $A_0$ 和 pending 恢复意图，再执行待审计更新，关闭写入进程并重新打开数据库得到 $S_1$。它同时检查活动映射是否仍等于 $A_0$，以及指针所指版本存在、事实键一致、生命周期状态正确和事件可重放等不变量 $I(S_1)$。

<div class="method-step__io" markdown="1">

**输入**：受控事务 $\tau=(q,S_0,K_\tau,\sigma_\tau)$、故障前状态 $S_0$ 及完整应用可见快照 $A_0=\Pi_{\rm app}(S_0)$。<br>
**输出**：经重新打开仍有效的正常状态，或需要补偿恢复的持久故障判定。

</div>

**直观理解**：只有错误在关闭并重开数据库后仍存在，才算真正的持久故障；这避免把尚未落盘的瞬时异常误报成恢复成功或失败。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Ordered PatchTest 来源支持谓词

$$
\operatorname{Support}_{\rm ord}(q)=F(q)\land Q(e,D_s)\land[T(v)\preceq T(e)]
$$

**符号说明**

- $q$：上游提出的记忆更新，其中包含键、值、证据、来源和时间信息。
- $F(q)$：字段完备性指示量：键、值、来源标识、时间信息和证据均存在，且值的内容词元序列非空。
- $e$：提案引用的证据片段。
- $D_s$：不透明来源标识所引用的原始来源文本。
- $Q(e,D_s)$：证据规范化后是来源文本规范化结果之子串的谓词。
- $T(x)$：文本经规范化后得到的内容词元序列。
- $v$：提议写入的事实值。
- $\preceq$：有序子序列关系，即左侧所有词元必须按原顺序出现在右侧序列中。

<div class="equation-explanation" markdown="1">

**直观理解**：只有元数据齐全、证据确实位于所声明来源中，而且候选值的每个内容词元按顺序出现在证据里，提案才获准写入。该式提供的是可审计的“引文支持”下界，而不是自然语言蕴含或来源真实性证明。<br>
**原文位置**：Method，Source-supported update admission，Equation 1

</div>

</div>

<div class="equation-block" markdown="1">

#### 持久回滚成立条件

$$
\operatorname{RB}(\tau)\iff \operatorname{PersistIntent}(A_0)\land\operatorname{Reopen}(S_1)\land\bigl([\Pi_{\rm app}(S_1)\neq A_0]\lor\neg I(S_1)\bigr)\land\operatorname{Restore}(A_0)\land\operatorname{Reopen}(S_2)\land I(S_2)\land\Pi_{\rm app}(S_2)=A_0
$$

**符号说明**

- $\tau$：受治理的应用级事务，包含提案、更新前状态、声明的逻辑范围和事务状态。
- $A_0$：故障前状态的完整应用可见活动指针映射，即恢复前像。
- $S_1$：执行待审计更新并关闭、重新打开数据库后得到的故障检查状态。
- $S_2$：执行补偿恢复后再次重新打开数据库得到的状态。
- $\Pi_{\rm app}(S)$：从持久状态投影出的应用可见活动映射。
- $I(S)$：指针与版本存在、事实键一致、活动状态正确及事件可重放等完整性条件的合取。
- $\operatorname{PersistIntent}(A_0)$：完整活动映射前像及恢复意图已经持久化。
- $\operatorname{Restore}(A_0)$：控制器已执行恢复完整活动映射的补偿事务。
- $\operatorname{Reopen}(S_i)$：数据库经过关闭和重新打开后得到状态 $S_i$，用于验证结果确已持久化。

<div class="equation-explanation" markdown="1">

**直观理解**：回滚不能只以“调用过恢复函数”为准：必须先有持久化意图，故障必须在第一次重开后仍可观察，恢复后还要第二次重开，并同时满足结构不变量和完整活动映射相等。该条件因此排除了只修一个键、只恢复内存态或留下悬空指针却宣称成功的情况。<br>
**原文位置**：Method，Durable audit and complete-state recovery，Equation 3

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。MemTxn 不是通过梯度优化训练出的回答模型，也没有可学习损失函数；Ordered PatchTest、冲突触发、时间解析和恢复条件均为冻结的确定性合同。回答模型可以替换，治理层的写入许可与恢复决定不依赖其答案；文中提到的固定或校准覆盖率规则仅作为 Ordered PatchTest 的显式消融对照，而非 MemTxn 的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Ordered PatchTest**

该模块是冻结的、无需模型调用的词法验证器。它组合字段完备性 $F(q)$、证据是否源内可定位的 $Q(e,D_s)$，以及值词元在证据中的有序子序列约束；复杂度对所检查来源和词元长度为线性。

> 直观理解：普通覆盖率只问“词有没有出现”，可能放过改变词序或插入否定后的错误。Ordered PatchTest 使用较窄但容易复现和审计的支持合同，保证所有被激活提案都满足同一条来源一致性规则；它不保证来源本身真实，也不处理深层语义角色绑定。

**2. Temporal Resolver**

模块只处理冲突触发器筛出的候选集合 $C_\kappa$，在“时间顺序定义可见真值”的受控协议下返回时间元数据 $\nu(q)$ 最大的版本，并采用确定性平局规则。构造两两冲突触发器需要 $O(n^2)$，分组后的解析需要 $O(n)$，其中 $n$ 为候选数。

> 直观理解：它解决的是“按照既定版本政策应展示哪条”，而不是判断哪条在现实中更可信。将冲突路由与写入分离，可避免回答阶段临时选了某条记录，就把该选择偷偷变成永久记忆更新。

**3. 持久快照日志与补偿恢复控制器**

恢复可信基包括 SQLite、已持久化的恢复意图和活动映射快照 $A_0$；版本、活动指针、状态事件和恢复意图存放在独立持久表中。系统保存应用可见前像而非整个物理数据库，恢复和快照成本为 $O(|A_t|)$ 个键，以空间与时间开销换取对真实物理写集合的独立性。

> 直观理解：数据库原子性只能保证一笔物理写入如何提交，不能自动知道应用原本想让哪些版本可见。该模块保存“故障前完整目录”，因此能恢复应用语义上的整体状态；但它依赖快照和意图完好、外部检测器调用控制器，且不承诺并发、反复故障或物理介质丢失下的恢复。

**训练与推理**

运行前需确定文本规范化、来源查找、冲突阈值、时间元数据含义以及“最新时间即当前可见版本”的应用合同，并建立版本、活动指针、状态事件和恢复意图表。在线写入时，上游抽取器生成 $q$，Ordered PatchTest 独立验证来源支持；通过者被扩展为版本 $z=(\mathrm{vid},q,\rho,\sigma,t_c)$，其中 $\rho$ 为父指针、$\sigma$ 为生命周期状态、$t_c$ 为提交时间，随后原子激活。在线回答时，系统不重新决定写入是否合法，而是根据无监督的冲突触发器在 Dense 原始块与受治理版本之间路由；冲突集合由 Temporal Resolver 按 $\nu(q)$ 选择。故障恢复由外部异常检测器启动：控制器读取预先持久化的 $A_0$，在一次补偿事务中恢复全部活动指针、更新受影响版本状态并记录修复，再通过重新打开数据库和不变量检查确认恢复持久化。该流程明确不覆盖异常检测本身、并发控制、连续重复故障、来源真实性验证或物理存储丢失。

**复现信息**

持久层采用 SQLite WAL，并设置 $\texttt{synchronous=FULL}$；SQLite 负责物理写入的原子性，MemTxn 负责语义写入许可、版本可见性和补偿恢复。恢复接口故意不接收物理写集合；每笔受控事务保存完整活动映射 $A_0$，所以快照和恢复开销随活动键数 $|A_t|$ 线性增长。冲突检测的固定阈值为：同键或规范化主语—关系 Jaccard 相似度至少 $0.60$ 时归并候选；仅当来源不同且值既不完全相同、Jaccard 相似度又低于 $0.80$ 时触发治理路由。公平解释结果时还应注意：无冲突情形使用 Dense 原始块；恢复评测从外部检测器调用控制器之后开始；Ordered PatchTest 不调用额外验证模型，因而其行为主要由规范化和来源定位实现决定。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 端到端 API 受控案例：对 GPT-5.3-Codex-Spark、GPT-5.4-mini 和 GPT-5.4 三个端点分别评测有效写入、无支持写入与旧任务保留；每个端点每类有 100 个受控案例，对应每个端点 300 条方法评测记录。其作用是检验完整的“写入—拒绝—保留”工作流，而不是单独测试某一组件。
- LongMemEval-S 派生的来源支持审计集：从抽取输出构造，开发集条目 ID 与测试条目完全分离；测试包含 12 个未见来源条目、60 个有支持的原始提案和 179 个契约内困难负例。负例由插入否定、词元重排和来源外替换生成，用于检验写入门能否判断提议值是否得到所引用来源的直接支持。
- MemoryAgentBench FactConsolidation：任务规定时间上最新的冲突断言为正确答案，与 Temporal Resolver 的时间顺序契约一致。表 2 在五个代表性答案模型上比较七种方法，每个模型评测 800 个问题；所有方法共享提示词且只调用一次答案模型，因此主要测试“改变哪个版本对答案模型可见”是否有效。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率及组件正确率**

端到端实验分别计算有效写入被接纳、错误写入被拒绝、旧任务被保留的比例；来源审计中的准确率则统计所有正负提案被正确分类的比例。 （越高越好，因为它表示事务边界更少误拒合法更新、误收错误更新或丢失既有状态。）

</div>
<div class="metric-item" markdown="1">

**F1**

综合精确率与召回率的调和平均。在来源审计中，它衡量接纳有支持写入时对误接纳和误拒绝的平衡；在 FactConsolidation 中，它衡量最终问答结果与标准答案的综合匹配质量。 （越高越好，因为它要求系统不能仅靠偏向接纳或拒绝某一类样本获得表面优势。）

</div>
<div class="metric-item" markdown="1">

**条件陈旧率**

在具备相关冲突信息的条件下，答案仍采用旧版本事实的比例，用来直接检查 Temporal Resolver 是否减少陈旧事实泄漏到最终答案。 （越低越好，因为较低数值表示系统更常把时间上应当生效的最新版本暴露给答案模型。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个 API 端点上的端到端写入—拒绝—保留工作流

<div class="result-value" markdown="1">

作者报告，MemTxn 在有效写入和错误写入拒绝上平均正确率均为 1.0，旧任务保留率为 0.992；相比之下，Retrieval 的旧任务保留率仅为 0.225，Versioned 未保留任何旧任务。端点调用错误率低于 0.007。

</div>

这说明同一个外部治理层可以同时允许合法更新、拦截无支持更新并维持此前仍应可见的任务状态，而不是通过“一律拒绝写入”换取安全性。由于案例是受控构造的，并且精确端点检查点版本未被独立验证，该结果不能直接证明开放环境中的长期可靠性，也不能排除端点版本漂移的影响。

<div class="result-source" markdown="1">

来源：Figure 3；End-to-End API-Endpoint Governance，Workflow and component accuracy

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across these three API-endpoint configurations, each with 300 method rows, MemTxn averages 1.0 1.0 on valid writes and wrong-write rejection and .992 .992 on old-task retention. Retrieval retains only .225 .225 of old tasks, while Versioned retains none. Endpoint call-error rates remain below .007 .007; exact checkpoint revisions were not independently verified.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 条目不重叠的 LongMemEval-S 来源支持审计

<div class="result-value" markdown="1">

Ordered PatchTest 正确接纳全部 60 个有支持原始提案，并拒绝全部 179 个困难负例，准确率、平衡准确率、精确率和 F1 均为 100.00，误接纳与误拒绝均为 0。最强替代门 Hybrid 仍误接纳 49 个负例并误拒绝 3 个正例。

</div>

该结果表明，冻结后的有序词汇支持规则可以泛化到未参与阈值选择的来源条目，而且收益并非测试集上重新调阈值得到。它证明的是提案是否满足论文声明的“有序词汇来源支持契约”，并不证明来源本身真实，也不保证系统正确理解语义角色。

<div class="result-source" markdown="1">

来源：Table 1；Source-Support Admission，Admission quality

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Ordered – 100.00 100.00 100.00 100.00 0 0

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MemoryAgentBench FactConsolidation 的时间冲突解析

<div class="result-value" markdown="1">

在五个代表性答案模型上，MemTxn 均取得所在模型区块的最高结果；相对 Dense，F1 提升 17.06–24.07 个点，条件陈旧率下降 15.97–37.6 个点。论文同时指出，单跳问题的提升大于多跳问题。

</div>

由于所有方法共享同一提示词且只进行一次答案调用，这一差异主要支持如下判断：在冲突事实中只暴露时间上应生效的版本，能够明显提高答案质量并减少旧事实干扰。单跳收益更大则提示版本选择并未解决全部问题，多跳场景仍受答案模型组合推理能力限制。

<div class="result-source" markdown="1">

来源：Table 2；Temporal Resolution on FactConsolidation，Main FactConsolidation results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MemTxn leads every model block, improving over Dense by 17.06–24.07 F1 points and reducing conditional stale rate by 15.97–37.6 points. Larger single-hop than multi-hop gains indicate remaining answer-reasoning limits.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 来源支持审计只验证声明的有序词汇支持契约。作者明确说明，该受控结果不能建立语义角色忠实性或事实真实性；因此即使提案能在来源中按顺序找到，也不代表来源可信或更新语义必然正确。
- 当前节选未给出持久化多键故障审计、LoCoMo 状态恢复、最终消融与压力测试的具体表格和数值，也未提供 FactConsolidation 表 2 的逐模型分数。端到端 API 实验的精确检查点修订亦未独立验证，且整体 API 配置数量的叙述存在需核对的口径差异。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Retrieval：代表仅依赖检索来访问记忆的方案。它是端到端比较中的关键参照，用于判断普通检索是否能够在写入后继续保留旧任务所需的信息。
- Versioned：代表保存版本但缺少 MemTxn 完整治理边界的方案。该比较用于区分“记录多个版本”与“正确决定应用可见版本并维持旧任务状态”之间的差异。
- Dense：FactConsolidation 的主要下游问答基线。由于各方法使用相同提示词和单次答案调用，与 Dense 的差异主要反映记忆可见性和冲突版本选择，而非额外推理调用。
- 来源支持写入门对照组：包括 Lexical、Calibrated、Qwen 和 Hybrid。它们分别代表固定词汇阈值、校准阈值、模型判定及混合判定，用于检验 Ordered PatchTest 的收益是否只是阈值调整或引入验证模型所致。

**实验想回答的问题**

- MemTxn 能否作为统一的事务治理边界，在不依赖运行时标签的情况下同时完成三类操作：接纳有来源支持的更新、拒绝无来源支持的更新，以及保留更新前仍应可见的旧任务状态？
- 将写入验证与时间版本解析分别隔离后，它们是否能在未见来源条目和冲突事实问答中稳定工作，并进一步改善下游答案质量、减少旧版本事实被错误使用？

**实验实现**

实验按 API 案例、来源条目、固定基准历史和持久化历史分别统计，不把不同统计单位混合汇总。运行时决策不读取标准答案或评测标签：PatchTest 仅接收更新提案字段及其引用来源，Temporal Resolver 仅接收候选键、值、来源 ID 和时间顺序；标准答案、基准类别、不安全标签及故障类别均在决策完成后才关联。校准始终先于正式验证，来源审计尤其先在条目不重叠的数据上确定阈值，再冻结 Ordered PatchTest 规则并评测未见条目。论文称整体覆盖十个本地模型配置和两个 API 配置，但端到端小节另列出三个 API 端点；该口径差异需结合完整论文核对。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Figure 5 被描述为跟踪一个预算匹配的 FactConsolidation 示例，用于直观展示版本可见性如何影响回答；但所给节选没有提供该示例的具体历史、候选版本、模型回答或错误路径，因此无法据此作进一步定性归因。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces a transactional governance and recovery layer for reliable persistent memory updates in long-running LLM agents.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`0f79840a31e0a21a2817120af0ec36de7b68268d29ef17dba318f512af348ebb`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
