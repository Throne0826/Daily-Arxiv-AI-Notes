---
title: "[论文解读] ThreatForest: Multi-Agent Attack Tree Generation with Pluggable TTP Framework Mapping"
description: "[arXiv 2607.27528][Multi-Agent] ThreatForest研究如何把云原生应用的源代码仓库自动转化为具有应用上下文、标准化TTP映射和针对性缓解措施的结构化攻击树，并通过可插拔映射组件与人工验证关口兼顾覆盖范围、可审查性和实际可用性。"
arxiv_id: "2607.27528"
announcement_date: "2026-07-31"
primary_category: "multi_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.258332+00:00"
source_sha256: "66045161892a31239b8ee8aeae9963cca20362f3ce64818ab55208941400ac54"
tags:
  - "Multi-Agent"
  - "LLM Agent"
  - "威胁建模"
  - "攻击树"
  - "MITRE ATT&CK"
  - "多智能体系统"
  - "大语言模型"
  - "云安全"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">Multi-Agent · arXiv 2607.27528</p>

# ThreatForest: Multi-Agent Attack Tree Generation with Pluggable TTP Framework Mapping

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Leo, Cristian, Dykyi, Anton, Cortegaca, Danny, Begimher, Daniel, Jha, Prakash</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27528) · [PDF 下载](https://arxiv.org/pdf/2607.27528) · **关键词** 威胁建模, 攻击树, MITRE ATT&CK, 多智能体系统, 大语言模型, 云安全<br>


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

ThreatForest研究如何把云原生应用的源代码仓库自动转化为具有应用上下文、标准化TTP映射和针对性缓解措施的结构化攻击树，并通过可插拔映射组件与人工验证关口兼顾覆盖范围、可审查性和实际可用性。

**不用术语来说**：安全人员需要从代码、配置和系统数据流中推断攻击者可能如何逐步入侵，再为每条攻击路径找到合适的防御措施；但云原生系统往往包含大量服务、权限关系和网络边界，完全依靠专家逐项分析既慢又昂贵。现有自动化工具通常只能帮助画图、填写威胁描述或列出可能风险，尚不能稳定地给出从威胁目标、攻击步骤、标准攻击行为分类到应用级缓解建议的一整套结果。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出端到端多智能体威胁建模流水线：以代码仓库为输入，分阶段生成高层威胁、AND/OR攻击树、叶节点的TTP候选映射以及引用具体应用组件的缓解措施；流水线采用有向图编排、确定性验证、有限重试和三个人工参与验证点，使中间产物可检查、可修正并可恢复执行。
- 把TTP映射设计为可替换的独立组件，并建立覆盖威胁陈述、攻击树、TTP映射和缓解措施的评测协议；作者据此将主要准确性瓶颈定位到基于句向量相似度的映射编码器，而不是笼统归因于多智能体架构，为后续优化明确了优先对象。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

威胁建模是在软件设计与开发阶段系统识别攻击目标、攻击路径和缓解措施的安全分析活动。云原生应用通常横跨多种托管服务、访问控制模型、加密配置与网络边界，人工分析不仅耗时，而且依赖同时理解目标系统和攻击知识的安全专家。现有图形化或引导式工具主要帮助人工记录威胁，已有大语言模型方法也多停留在威胁枚举；本文关注更完整的链路，即从代码仓库出发，生成结构化攻击树，将具体攻击步骤对齐到标准化的攻击者战术、技术与过程框架，并给出与应用组件相关的防御建议。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**攻击树（Attack Tree）**

攻击树以攻击者的高层目标为根节点，逐层分解为子目标和可执行的叶节点，并用 AND/OR 关系表达“必须同时满足”或“任选一种即可”的攻击条件。它把零散威胁组织成可检查的攻击路径，但本文不声称生成结果具有形式化完备性或可靠性。

</div>
<div class="concept-item" markdown="1">

**战术、技术与过程（TTP）映射**

TTP 框架用标准条目描述攻击者的目标和行为，例如 MITRE ATT&CK、CAPEC 及云环境威胁矩阵。将攻击树叶节点映射到这些条目，可以复用框架中已有的检测与缓解知识，并使不同项目的威胁描述具有统一参照。

</div>
<div class="concept-item" markdown="1">

**多智能体流水线与人在回路（HITL）**

多智能体流水线把仓库分析、上下文修正、威胁生成、攻击树构造、TTP 映射和缓解建议等职责交给不同阶段，并通过有向图、确定性校验和有限重试协调执行。人在回路表示系统可在三个中间检查点暂停，由领域专家确认或纠正产物，避免错误继续向后传播。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是用户拥有且系统可读取的、能够部署为应用的源代码仓库；系统还假定用户信任所调用的大语言模型服务商，但不要求用户本人具备安全专业知识。目标输出包括四类设计期产物：与具体技术栈和数据流有依据关联的高层威胁；每个威胁对应、含 AND/OR 子目标和具体叶节点技术的攻击树；每个叶节点到可配置攻击者框架中已知 TTP 的映射；以及引用应用自身组件、而非仅给出通用原则的定制缓解措施。系统支持自主运行后交由安全领域专家复核的咨询模式，以及在三个节点接受人工修正的交互模式；所分析的攻击者是针对目标应用的外部对手。运行时检测与响应、自动修补、自主渗透测试等进攻操作均不在范围内，输出只服务于安全审查和安全开发生命周期，不能替代专家审查，也不是运行时防御控制。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$K$**

TTP 检索阶段为每个攻击步骤保留的候选技术数量，即 top-$K$ 中的候选数。

</div>
<div class="notation-item" markdown="1">

**$F_1$**

综合精确率与召回率的调和平均指标；引言用它概述 TTP 映射判定模型的试验结果。

</div>
<div class="notation-item" markdown="1">

**$\kappa$**

Cohen's kappa，一种扣除随机一致性后衡量评审者分类一致程度的统计量。

</div>

</div>

**直接相关的工作**

- **OWASP Threat Dragon**: 属于以图表为中心的威胁建模工具，能够提供结构化绘图支持，但核心安全推理仍主要依赖人工；它体现了现有工具在自动生成攻击路径、标准 TTP 映射和定制缓解方面的不足。
- **AWS Threat Composer**: 通过引导式界面帮助用户编写威胁陈述，但每项威胁仍需人工输入；相比之下，本文设定的是从源代码仓库自动产生威胁、攻击树、TTP 映射及缓解建议的端到端任务。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

云原生应用可能跨越数十种托管服务，每种服务又具有不同的访问控制、加密配置和网络边界。安全团队若要人工识别与具体技术栈、组件及数据流相关的威胁，还需进一步拆解攻击路径、对照MITRE ATT&CK或CAPEC等框架并制定缓解措施，工作量大且依赖稀缺的安全专家。因此，许多组织只能跳过威胁建模，或仅分析最关键的系统，导致其余攻击面在设计和发布阶段缺乏系统审查。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **图表驱动或引导式威胁建模工具**：OWASP Threat Dragon等工具为数据流图和威胁模型提供结构化编辑环境，AWS Threat Composer则引导用户逐条编写威胁陈述；它们主要规范人工建模过程，核心安全推理和内容录入仍由使用者完成。
- **基于大语言模型的威胁识别**：这类方法让大语言模型读取系统描述或相关上下文并枚举潜在威胁，以降低初步分析成本；论文指出，已有工作通常把输出终点设在威胁列表，而未继续形成分层攻击路径、标准化TTP映射和面向具体组件的防御建议。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统建模工具自动化程度有限，仍要求专家逐个系统、逐条威胁完成分析；当应用频繁发布且服务数量增加时，严谨性与覆盖范围之间形成直接冲突，难以对每个系统和每次版本迭代实施完整建模。
- 已有大语言模型方案通常只回答“可能有什么威胁”，没有连通“攻击者如何逐步实现目标、这些步骤对应何种已知行为、应在本应用何处采取措施”；结果因而难以直接接入安全评审和安全开发生命周期，也缺乏可验证的结构化中间产物。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种面向云原生代码仓库的完整且可审查的自动化机制，能够在同一流程中把应用证据转化为高层威胁，再将威胁分解为带AND/OR关系的攻击树，把叶节点映射到可配置对手框架中的TTP，并生成引用应用自身组件的缓解措施。同时，这种机制还需要显式暴露各阶段质量，使研究者能够判断错误究竟来自威胁生成、树构造、TTP检索还是缓解合成，而不是只评估最终文本的整体观感。

</div>
<div markdown="1"><span>核心问题</span>

给定一个用户有权读取的可部署应用代码仓库，能否通过带确定性检查、有限重试和人工验证点的多阶段智能体系统，自动产生具有足够覆盖范围与结构一致性的威胁陈述、攻击树、跨框架TTP映射和应用级缓解建议，并通过分能力评测准确定位端到端系统中的主导质量瓶颈？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把原本需要专家一次性完成的复杂推理拆成边界清楚的阶段：先理解仓库和数据流，再提出威胁，随后并行构造攻击树、检索标准攻击技术并生成缓解措施。这样，每个智能体只处理较窄的任务，确定性验证器可检查格式和必要字段，专家也能在错误继续传播前修正中间结果。将TTP框架表示为可检索的技术条目，并以语义相似度为每个攻击步骤召回候选项，则允许更换MITRE ATT&CK、CAPEC或云专用矩阵；更重要的是，映射器作为独立模块可以单独测量和替换，从而把系统改进集中到证据显示最薄弱的环节。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ThreatForest 是一个由有向图编排的多智能体威胁建模系统：输入源代码仓库，先提取云平台、服务、认证、数据流和部署方式等项目上下文，再生成结构化威胁；随后针对每个威胁并行构造攻击树，将攻击步骤检索映射到可插拔对手知识框架中的战术、技术与过程（TTP），并为每个映射技术生成有证据关联的缓解措施。并行结果经过确定性的概率标注后，被汇总为 Markdown 报告和交互式 HTML 仪表板。共享目录中的结构化 JSON 状态使中间结果可检查、可恢复，并支持不同威胁分支安全并行。

系统的关键设计不是提出新的单一模型，而是组合 LLM 智能体、句子嵌入检索、确定性验证器和三个人工审核点。LLM 负责需要语义判断的仓库理解、威胁分析、攻击树分解与缓解建议；纯函数验证器负责字段完整性、引用一致性和树结构合法性，并在失败时触发有界重试；安全专家则可在错误传播到下游前修正上下文与威胁。直观地说，它把一次大型、难以审计的提示调用拆成一条安全分析流水线，每一步都有明确输入、结构化输出和质量检查。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 仓库扫描与项目上下文校正

扫描智能体调用结构分析器和受沙箱限制的文件读取器，提取文件树、依赖、云提供商、技术栈、服务、认证机制、数据流及部署模型；确定性验证器检查必填字段，Scanner Review 与 Interviewer 再通过结构化编辑和追问补充上下文及置信度。

<div class="method-step__io" markdown="1">

**输入**：源代码仓库路径，以及仓库内可访问的源码、依赖清单和基础设施即代码文件。<br>
**输出**：经过验证和人工校正的项目上下文 JSON，例如 $\mathcal{C}$，保存于共享状态目录。

</div>

**直观理解**：这一步相当于先绘制系统地图，并请熟悉项目的人确认地图是否正确。后续判断只基于这份上下文，从而减少把仓库中不存在的组件或技术误当成攻击面。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 威胁生成与人工筛选

威胁智能体按“参与者—所需访问或知识—攻击动作—直接影响—最终后果”的模板生成威胁，并记录标题、描述、优先级和受影响组件；验证器检查 JSON 结构及组件引用，Threat Review 支持调整优先级、删除、重排、补充遗漏或重新调用智能体。

<div class="method-step__io" markdown="1">

**输入**：项目上下文 $\mathcal{C}$。<br>
**输出**：经过筛选的结构化威胁集合，其中每个威胁记为 $\theta_i$。

</div>

**直观理解**：系统先回答“可能发生哪些坏事”，而不是立即罗列攻击技术。人工审核在这里清除不合理或重复威胁，可避免错误继续扩展成整棵攻击树。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 并行攻击树构造

系统为每个威胁启动独立并行分支，树智能体将攻击目标分解为带 AND/OR 关系的子目标和具体步骤，形成根树 $\mathcal{T}_{\theta_i}=(S,E,r)$；验证器检查父子引用、根节点及步骤关系是否合法。

<div class="method-step__io" markdown="1">

**输入**：项目上下文 $\mathcal{C}$ 与单个威胁 $\theta_i$。<br>
**输出**：每个威胁对应一棵层次化攻击树，以及由根到叶节点构成的完整攻击路径。

</div>

**直观理解**：攻击树像把“达成攻击目标”拆成多条操作路线：OR 表示任选一条即可，AND 表示多个条件都要满足。不同威胁互不依赖，因此可同时处理，而不必逐棵等待。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. TTP 检索映射与缓解措施生成

ATTACK-BERT 将每个步骤与所有技术描述编码为 $768$ 维向量并计算余弦相似度，保留相似度不低于阈值 $\tau$ 的前 $K$ 个候选并以 top-1 作为最终映射；缓解智能体再根据上下文、完整攻击链和映射集合 $\mathcal{M}_{\theta_i}$，为每个唯一技术生成结构化缓解记录。

<div class="method-step__io" markdown="1">

**输入**：攻击树步骤描述、目标 TTP 框架中的技术描述、项目上下文 $\mathcal{C}$ 和攻击树 $\mathcal{T}_{\theta_i}$。<br>
**输出**：步骤到 TTP 技术的映射、候选技术及相似度，以及包含技术编号、实施指导、优先级、证据和处置周期类型的缓解措施。

</div>

**直观理解**：检索阶段先按语义相似性给每个攻击步骤查找最接近的标准技术标签，低于门槛时宁可不映射，也不强行贴标签。缓解阶段再把标准技术、实际技术栈和攻击路径合并考虑，使建议能说明“针对哪一步、为何需要以及应多快处理”。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 攻击步骤与 TTP 技术的余弦相似度

$$
\operatorname{sim}(d_i,t_j)=\frac{\mathbf{e}(d_i)\cdot\mathbf{e}(t_j)}{\lVert\mathbf{e}(d_i)\rVert\,\lVert\mathbf{e}(t_j)\rVert}
$$

**符号说明**

- $d_i$：攻击树中第 i 个步骤的文本描述
- $t_j$：目标 TTP 框架中第 j 个技术的文本描述
- $\mathbf{e}(\cdot)$：ATTACK-BERT 文本编码函数，输出 768 维实向量
- $\operatorname{sim}(d_i,t_j)$：步骤描述与技术描述之间的余弦相似度
- $\lVert\cdot\rVert$：向量的欧几里得范数

<div class="equation-explanation" markdown="1">

**直观理解**：该式比较两个文本向量的方向而非绝对长度；方向越接近，系统认为攻击步骤与标准技术的语义越相似。系统对每个步骤检索满足 $\operatorname{sim}\geq\tau$ 的前 $K$ 项，并默认选择相似度最高者，因此编码器的语义表示能力直接限制映射准确性。<br>
**原文位置**：第 3.5 节，公式 (2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 基于上下文、攻击树与 TTP 映射的缓解生成

$$
\operatorname{mitigate}(\theta_i)=f_{\mathrm{LLM}}\!\left(\mathcal{C},\mathcal{T}_{\theta_i},\mathcal{M}_{\theta_i}\right)\to\{m_1,\ldots,m_p\}
$$

**符号说明**

- $\theta_i$：第 i 个结构化威胁
- $\mathcal{C}$：从仓库提取并经审核的项目上下文
- $\mathcal{T}_{\theta_i}$：威胁 $θ_i$ 对应的攻击树
- $\mathcal{M}_{\theta_i}=\{(s_j,t_j)\}$：该威胁下攻击步骤 $s_j$ 到技术 $t_j$ 的映射集合
- $f_{\mathrm{LLM}}$：生成结构化缓解措施的语言模型智能体
- $m_k$：第 k 条缓解记录，包含技术编号、指导、优先级、证据和类型
- $p$：为该威胁生成的缓解记录数量

<div class="equation-explanation" markdown="1">

**直观理解**：该式强调缓解建议不是只看一个技术标签生成，而是同时读取实际项目环境、完整攻击链和技术映射。上下文约束建议适配现有基础设施，攻击树提供多步因果关系，映射集合则允许验证每个已识别技术是否得到处置。<br>
**原文位置**：第 3.6 节，Mitigation Agent

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文描述的是推理期多智能体系统，没有报告对 LLM 或 ATTACK-BERT 进行端到端训练、微调或基于损失函数的联合优化；ATTACK-BERT 作为既有句子编码器用于检索，LLM 通过结构化提示、工具调用和验证反馈工作。参数 $K=3$ 与阈值 $\tau=0.3$ 为经验设定，而不是通过本文所述训练目标学习得到。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 有向图编排、共享状态与有界重试**

各智能体和验证器是 Strands Graph 的节点，条件边控制正常前进或失败回退；每个节点从 $\texttt{.threatforest/state/}$ 读取前序 JSON 并写入新状态。正常路径节点数为 $|V|=12$，最多重试次数为 $k=2$，四个阶段带重试边，理论预算下界为 $20$，运行时总节点执行上限设为 $B=32$，耗尽后返回部分结果而非无限循环。

> 直观理解：共享状态像流水线上的检查单，使失败后可以从中间继续，也能看到错误在哪一步产生。重试预算则是保险丝：模型输出不合格时允许返工，但不会因反复失败而永久运行。

**2. 确定性验证与三个人工参与门**

扫描、威胁、并行子流水线和报告阶段均由不调用 LLM 的纯函数验证字段、JSON 模式、树关系及跨对象引用；结构错误硬失败并触发重试，少量缓解覆盖缺口仅产生软警告。Scanner Review、Interviewer 和 Threat Review 允许专家直接合并结构化编辑，或以自由文本反馈重新调用上游智能体。

> 直观理解：验证器擅长检查“格式和引用是否正确”，专家擅长判断“安全含义是否合理”，两者职责分离。这样既避免用另一个随机模型检查格式，也使关键领域知识能在错误扩散前进入系统。

**3. 嵌入式 TTP 检索与证据关联缓解**

系统使用 ATTACK-BERT 对攻击步骤和技术描述进行统一向量编码，设 $K=3$、$\tau=0.3$，保存三个候选但默认采用最高相似度技术；若没有候选达到阈值，则该步骤保持未映射。缓解生成以 $\mathcal{C}$、$\mathcal{T}_{\theta_i}$ 和 $\mathcal{M}_{\theta_i}$ 为联合条件，并由 Pydantic 模式约束输出；覆盖验证器检查每个已映射技术是否至少有一条缓解措施。

> 直观理解：候选列表保留了机器判断的不确定性，方便后续由 LLM 或专家改选，而阈值能降低明显牵强的标签。证据字段把建议反向连接到攻击步骤和标准技术，使缓解措施可以追溯，而不是一组与项目无关的通用安全清单。

**训练与推理**

完整流程属于推理：用户提供仓库路径后，扫描智能体生成 $\mathcal{C}$，验证器与 Scanner Review/Interviewer 校正上下文；威胁智能体产生 $\theta_i$，Threat Review 完成筛选；系统按威胁并行生成 $\mathcal{T}_{\theta_i}$，使用 ATTACK-BERT 对步骤和框架技术做全量相似度检索，形成 $\mathcal{M}_{\theta_i}$，再生成并验证缓解记录。最后，确定性概率模块更新步骤成功概率并沿 AND/OR 树传播到达概率，报告生成器输出 Markdown 与 HTML；任一可重试阶段若未通过结构验证，则在执行预算 $B=32$ 内回到其生产智能体，预算耗尽时终止并保留部分结果。

**复现信息**

复现或公平解释方法所需的关键设置包括：智能体以 Strands Graph 编排，中间状态写入 $\texttt{.threatforest/state/}$；文件读取器只能访问目标仓库；TTP 编码器为 ATTACK-BERT，嵌入维度为 $768$，候选数为 $K=3$，最低余弦相似度为 $\tau=0.3$，top-1 用作最终映射。攻击树—TTP—缓解子流水线按威胁并行；结构化记录使用 JSON 和 Pydantic 模式验证；概率标注与最终报告均为确定性实现。原文称系统支持可插拔 TTP 框架，但所给方法细节具体展开的是 MITRE ATT&CK 映射，其他框架的适配接口和索引构建细节在本节选中未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 七个云原生应用领域：IoT制造、身份联合、生成式AI、医疗分析、IAM治理、会议转录和旅行预订。它们代表不同架构原型，用于检验跨领域外部有效性，而非构成具有固定训练集、验证集和测试集划分的标准数据集；原文未明确报告各领域的仓库数量、样本规模或数据划分。
- 流水线生成的四类评测对象：威胁陈述、攻击树、逐攻击步骤的TTP映射以及缓解措施。每类对象依据相应评分维度接受评审；单条TTP映射还被写入数据项，以便后续构建人工真值语料、计算$\mathrm{precision}@K$并进行微调，但本节未报告该语料规模或$K$值。
- 用于跨模型校准的分层样本：由不同LLM家族的独立评审模型在不知道原面板结论的条件下重新评分，用来检查自动评审面板的可靠性；原文未明确报告样本量及抽样比例。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**16维质量评分**

覆盖四类能力：威胁陈述5维、攻击树6维、TTP映射1维、缓解措施4维。除TTP映射外，各维采用excellent、good、acceptable、poor、unacceptable五档，并映射为$1.0$、$0.75$、$0.5$、$0.25$、$0$；TTP映射则由评审者判断为good（1）或bad（0）。跨应用报告各维均值与标准差，用于衡量内容质量及领域间稳定性。 （越高越好；高分表示生成内容更相关、完整、准确、现实且可执行，或TTP技术与攻击步骤之间更可辩护。）

</div>
<div class="metric-item" markdown="1">

**技术多样性$\delta$与阶段覆盖率$\gamma$**

$\delta$是不同ATT&CK技术数量占全部映射数量的比例，用来识别是否反复套用少数技术；$\gamma$是映射结果覆盖的ATT&CK战术数占14个战术总数的比例，用来衡量从侦察到影响等攻击阶段的覆盖广度。这两项是结构覆盖指标，不直接判断映射是否正确。 （通常越高表示覆盖越广、重复越少，但并非无条件越高越好；若为了增加多样性而加入不相关技术，高覆盖率仍可能伴随较低映射准确率。）

</div>
<div class="metric-item" markdown="1">

**攻击树平均深度$\bar{D}$**

对一个应用生成的$N$棵攻击树分别计算深度后取均值，用于描述攻击路径的层级复杂度和展开程度。它只衡量结构，不评估攻击逻辑是否真实或技术步骤是否正确。 （不存在简单的单调优劣关系；过浅可能遗漏中间攻击步骤，过深则可能引入冗余或臆造路径，应结合结构质量、技术现实性和攻击路径逻辑评分解释。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 七个应用领域上的威胁陈述、攻击树和缓解措施质量

<div class="result-value" markdown="1">

作者报告，三类核心生成产物的面板质量分数处于$0.63$至$0.68$之间，量表范围为$0$至$1$。

</div>

这表明系统在内容生成和结构化分析方面总体达到中等偏上的自动评审水平，且攻击树之外的威胁描述与防御建议也没有出现明显断层。不过，这些分数来自LLM面板，并由专家进行确认性复核，不能等同于大规模、完全独立的人类专家标注，也不能直接证明生成内容在真实攻防环境中有效。

<div class="result-source" markdown="1">

来源：摘要；所给节选未包含第5节对应结果表

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Panel-measured quality reaches 0.63-0.68 (on a 0-1 scale) for threat statements, attack trees, and mitigations, but only 0.29 for embedding-only TTP mapping -- a gap stable across all seven domains that isolates the binding constraint.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 仅使用嵌入相似度完成的TTP映射

<div class="result-value" markdown="1">

嵌入式TTP映射的面板准确性仅为$0.29$，明显低于威胁陈述、攻击树和缓解措施的$0.63$至$0.68$质量区间；这一差距在全部七个领域中保持稳定。

</div>

结果说明系统能够生成看似合理的攻击步骤，却经常无法把这些步骤可靠地对齐到正确的ATT&CK等框架技术。跨领域一致的低分降低了“只是某个应用领域特别困难”的可能性，并支持嵌入检索是共同瓶颈的判断。但TTP指标采用二元可辩护性判断，而其他能力采用五档质量评分，两者数值不能被视为完全同构的准确率。

<div class="result-source" markdown="1">

来源：摘要；评分定义见第4.1节，跨领域结果表未包含在所给节选中

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Panel-measured quality reaches 0.63-0.68 (on a 0-1 scale) for threat statements, attack trees, and mitigations, but only 0.29 for embedding-only TTP mapping -- a gap stable across all seven domains that isolates the binding constraint.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 同一模型的受控单次调用与嵌入映射方案比较

<div class="result-value" markdown="1">

作者报告，受控单次调用基线使映射的可辩护性提高到嵌入方案的两倍以上。

</div>

由于比较使用同一基础模型，显著改善更符合“嵌入编码器或相似度检索方式限制了映射质量”的解释，而不是把失败归因于多智能体设计本身。原文摘要没有给出基线的绝对分数、置信区间或显著性检验，因此“锁定瓶颈”是作者基于受控比较提出的因果性较强主张，仍需结合完整实验表核验。

<div class="result-source" markdown="1">

来源：摘要；所给节选未包含第5节基线结果表

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A controlled single-call baseline on the same model more than doubles mapping defensibility, pinning the limitation on the embedding encoder rather than the multi-agent design.

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

- 同一基础模型的受控单次调用基线：绕过或替代多智能体周边流程，直接完成映射任务。该比较控制了基础模型差异，因此适合判断TTP映射问题主要来自嵌入编码器，还是来自多智能体编排。
- 三名独立LLM评审者的原始评分：在对抗验证器介入前保留，用于计算序数维度的平均两两一致率，以及二元TTP判断的Cohen's $\kappa$和百分比一致率，从而检验自动评分是否稳定。
- 不同LLM家族的独立校准评审者：对分层样本进行盲评，用于判断主评审面板的结论是否只是特定模型家族的评分偏好。

**实验想回答的问题**

- ThreatForest在不同云原生应用领域中，能否稳定生成高质量、贴合上下文且可供防御者执行的威胁陈述、攻击树与缓解措施？
- TTP映射的低准确率究竟来自多智能体流水线本身，还是来自以句向量余弦相似度检索候选技术的嵌入编码器？

**实验实现**

所有产物均由三名具有不同审查重点的LLM评审代理独立评分，并获得与生成流水线相同的扫描器上下文。对抗验证代理以逐维中位数为起点，只能维持或降低评分；降分必须引用模板化内容、技术错误、虚构组件或覆盖缺失等具体缺陷。之后，人类安全领域专家通过Langfuse标注队列确认或纠正面板判断，但论文主要定量结果仍是自动面板测量，而非完全由人类独立标注所得。系统同时记录Strands SDK自动产生的OTEL调用轨迹，以及各子图边界的结构化输入输出标注轨迹。可靠性检查包括原始评审者间一致性和跨模型盲评校准；本节未给出具体模型版本、运行次数、推理参数、成本或完整专家复核比例。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 以同一基础模型的单次调用替换嵌入式TTP映射 | 单次调用基线使映射可辩护性提高到两倍以上；原文未明确报告两种设置的绝对分数、样本量、误差范围及统计显著性。 | 该控制实验尽量保持基础模型不变，主要改变映射机制，因此隔离出句向量编码和余弦相似度候选匹配这一组件的影响。性能大幅回升支持嵌入编码器是主导瓶颈，但若单次调用获得了不同提示、更多上下文或不同候选集合，仍可能存在未完全控制的因素；所给节选不足以核验这些细节。 | 摘要；所给节选未包含第5节消融或基线表<br><span class="experiment-evidence">A controlled single-call baseline on the same model more than doubles mapping defensibility, pinning the limitation on the embedding encoder rather than the multi-agent design.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces an orchestrated multi-agent pipeline with verification, retries, and human validation for repository-based threat modeling.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`66045161892a31239b8ee8aeae9963cca20362f3ce64818ab55208941400ac54`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
