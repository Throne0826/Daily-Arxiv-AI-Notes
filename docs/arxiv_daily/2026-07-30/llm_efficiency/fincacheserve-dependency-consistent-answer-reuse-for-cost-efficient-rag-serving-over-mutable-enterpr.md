---
title: "[论文解读] FinCacheServe: Dependency-Consistent Answer Reuse for Cost-Efficient RAG Serving over Mutable Enterprise Documents"
description: "[arXiv 2607.26076][LLM 效率] FinCacheServe通过把生成答案与文档版本、证据、工具输出及模型配置等依赖共同绑定，在企业文档持续更新的条件下安全复用答案，从而减少RAG服务中的GPU推理调用。"
arxiv_id: "2607.26076"
announcement_date: "2026-07-30"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:25.812170+00:00"
source_sha256: "13ef891662e64af5c7944f460592deb782f284b3f86a87771421a56939cb7389"
tags:
  - "LLM 效率"
  - "检索增强生成"
  - "大语言模型服务"
  - "答案缓存"
  - "可变企业文档"
  - "依赖一致性"
  - "缓存失效"
  - "GPU 成本"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2607.26076</p>

# FinCacheServe: Dependency-Consistent Answer Reuse for Cost-Efficient RAG Serving over Mutable Enterprise Documents

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Lingteng Zeng, Yifan Jin</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26076v1) · [PDF 下载](https://arxiv.org/pdf/2607.26076v1) · **关键词** 检索增强生成, 大语言模型服务, 答案缓存, 可变企业文档, 依赖一致性, 缓存失效, GPU 成本  


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

FinCacheServe通过把生成答案与文档版本、证据、工具输出及模型配置等依赖共同绑定，在企业文档持续更新的条件下安全复用答案，从而减少RAG服务中的GPU推理调用。

**不用术语来说**：企业分析系统经常反复回答含义相同的问题；直接返回旧答案可以节省昂贵的大模型计算，但公司公告、财务表格或计算结果可能已经更新，旧答案因而可能过时。关键困难不是简单判断两个问题是否相似，而是确认旧答案所依据的全部信息仍然有效。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出依赖一致的答案复用契约：缓存项不仅记录规范化的企业分析意图，还记录源文档版本、证据指纹、工具输出指纹、模型身份和解码配置；只有任务身份匹配且全部依赖兼容时才允许复用。
- 将该契约实现为面向RAG服务的缓存与元数据机制，包括文档到答案的反向依赖索引和更新驱动的失效流程，使文档更新能够在后续读取前传播到相关缓存项。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究面向可变企业文档的检索增强生成（RAG）在线服务。典型请求先从公司报告、监管申报、政策或日志中检索证据，再把问题与证据组成提示交给大语言模型生成带依据的回答；即使多个请求表达相同分析意图，传统流程仍会重复消耗 GPU 显存、预填充时间和解码计算。答案缓存可以在命中时直接返回既有回答，完全跳过模型调用，但企业文档及其派生数据会更新，因此缓存是否可复用不能只由问题文本相似度或固定有效期决定，还必须检查生成该回答所依赖的文档版本、证据片段、工具结果以及模型配置是否仍然一致。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**检索增强生成（RAG）**

RAG 在生成回答前先从外部文档库检索相关证据，并将证据连同问题输入大语言模型。它能让回答依据企业私有或持续更新的资料，但也使回答正确性依赖于检索结果及源文档版本。

</div>
<div class="conceptitem" markdown="1">

**答案缓存（answer cache）**

答案缓存保存已经生成的最终自然语言回答；后续请求若满足复用条件，可直接返回该回答并省去模型的预填充和解码。它不同于 KV 缓存或前缀缓存，后两者只加速模型内部执行，通常不能完全取消模型调用。

</div>
<div class="conceptitem" markdown="1">

**依赖一致性与失效传播**

依赖一致性要求缓存回答所依赖的源文档、证据、工具输出和服务配置仍与生成时兼容。失效传播是指底层文档更新后，通过文档到答案的反向依赖关系定位并使相关缓存项失效，避免返回基于旧证据的答案。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是针对公司、报告期或申报文件等企业对象的分析请求，以及当前文档库、检索证据、工具计算结果和模型服务配置；系统输出自然语言回答，并尽可能复用历史答案以减少 GPU 上的大模型调用。场景假设请求意图会重复，但源文件、证据抽取结果、数值计算工具或模型与解码配置可能变化。因而核心任务是在识别语义等价或业务意图一致请求的同时，仅当金融实体与期间、文档范围、源文档版本、证据指纹、工具输出指纹、模型身份和解码配置均满足兼容条件时允许缓存命中；否则重新检索或生成。金融申报材料被用作可复现设置，因为回答通常明确依赖公司、期间、申报范围和版本，且修订申报或证据管线刷新会改变答案依据。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **vLLM / PagedAttention**: vLLM 通过 PagedAttention 改善 KV 缓存的显存管理和大模型服务吞吐，属于模型执行阶段的缓存优化。FinCacheServe 在其上实现 RAG 服务，但把复用提升到最终答案层：有效命中时不是加速一次模型运行，而是直接取消该次模型调用。
- **GroundedCache-style routing**: 该类语义响应缓存通过证据重叠和来源有效性门控提高 RAG 回答复用的可靠性。FinCacheServe 进一步把复用条件定义为面向可变企业文档的细粒度依赖契约，同时约束金融身份与期间、文档版本、证据和工具指纹、模型身份及生成参数。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

面向公司报告、监管申报、政策、工单和日志的RAG服务会在仪表盘、合规流程及金融分析助手中重复处理相同或语义等价的分析请求。常规执行仍需检索证据、构造增强提示并调用LLM，重复消耗GPU显存、预填充时间和解码计算；若直接缓存最终答案，又必须应对申报修订、证据切分刷新、工具计算变化以及模型或推理配置切换带来的答案失效。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **模型执行阶段复用**：通过KV缓存、前缀复用、预填充复用或上下文调度，减少请求进入模型后的重复计算；这类机制仍会执行模型调用，只是加速其中部分步骤。
- **基于查询匹配或时间窗口的答案缓存**：依据文本或语义相似度命中历史答案，或使用固定生存时间（TTL）限制缓存有效期；部分版本化方法还会检查较粗粒度的文档版本，但并未完整刻画答案对具体证据、工具结果和服务配置的依赖。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 模型执行阶段的缓存不能像有效的答案级命中那样完全绕过LLM，因此仍保留预填充或解码成本，无法最大程度消除重复分析请求造成的GPU负担。
- 仅凭语义相似度、固定TTL或粗粒度版本信息无法判断旧答案的依据是否仍然成立：源表修订、证据块刷新、比率计算变化或模型配置切换都可能在问题措辞近似时产生过时答案，并将失效证据暴露给用户。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方案缺少一种可落地的答案级复用机制，能够同时获得绕过整个LLM调用的收益，并以细粒度、可检查的依赖契约约束复用资格；该机制还需要在文档更新与缓存读取并发发生时，及时定位并失效所有受影响答案。

</div>
<div markdown="1"><span>核心问题</span>

能否把RAG生成答案表示为带显式依赖的服务对象，并利用任务身份匹配、全依赖兼容检查和更新驱动失效，在可变企业文档上显著跳过LLM调用，同时避免观察到由依赖变化造成的陈旧输出？

</div>
<div markdown="1"><span>作者直觉</span>

一个历史答案是否可复用，取决于“问题所指的任务”和“产生答案时使用的条件”是否都未改变。FinCacheServe因此不把相似问题直接等同于相同答案，而是给答案附上一张依赖清单；查询到来时逐项核验，文档更新时再通过反向索引找到相关答案并使其失效。这样，语义匹配负责发现候选答案，依赖检查负责决定候选答案是否仍然安全。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

FinCacheServe将RAG生成的答案视为带有完整依赖关系的“服务对象”，而不是仅由问题文本索引的普通缓存项。输入请求为r=(q,m,θ)，其中q是用户问题，m是模型标识，θ是解码配置；系统先完成检索并得到证据块，再按公司、报告期、分析意图、文档范围和工具需求构造金融请求签名。候选缓存答案只有在请求签名兼容、源文档版本仍一致、检索证据指纹相同、工具输出指纹相同且模型与解码配置一致时才能返回；否则执行检索、工具调用和LLM生成，并把新答案及其依赖写入缓存。

其核心设计是把“能否安全复用”与“有限容量下缓存什么”分开：依赖一致性门负责正确性，效用策略只负责收益和空间。文档更新时，元数据平面先增加版本号，再通过文档到答案的反向索引使所有相关答案失效，从而让更新和缓存读取具有统一的线性化顺序。直观地说，每个答案都附带一张记录其材料、计算工具和生成配置的保修单；只有保修单上的所有状态与当前请求完全相符，系统才跳过昂贵的LLM调用。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 请求规范化与金融签名构造

请求规范化器生成签名s(r)，其字段包括公司身份、报告期、查询族、文档范围、工具需求、模型身份和解码配置；查询族用于归并措辞不同但分析意图相同的问题。

<div class="method-step__io" markdown="1">

**输入**：用户查询q、模型标识m、解码配置θ，以及可解析出的公司、报告期、问题类型、文档范围和工具需求。  
**输出**：可用于精确索引或签名桶检索的规范化请求签名。

</div>

**直观理解**：系统不只比较句子是否相似，而是先判断两次请求是否在问同一家公司、同一时期和同一种财务问题，避免把跨季度或跨公司问题错误合并。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 检索解析与候选答案查找

系统解析检索结果E_r及来源文档D_r，并在精确索引和金融签名桶中查找候选答案；每个候选项携带引用文档、证据块、版本和其他依赖记录。

<div class="method-step__io" markdown="1">

**输入**：规范化请求、检索缓存、FAISS向量索引、当前文档集合及其版本元数据。  
**输出**：当前请求的证据依赖，以及一个较小的候选缓存答案集合。

</div>

**直观理解**：签名桶先把搜索范围限制到业务含义相同的答案，再做严格核验；这类似先从正确的档案柜抽出少量文件，而不是扫描全部缓存。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 依赖一致性复用判定

在统一线性化点τ检查签名兼容性、所有依赖文档的版本相等、证据指纹相等、工具指纹相等，以及模型与解码配置完全一致；任一条件失败即拒绝该候选。

<div class="method-step__io" markdown="1">

**输入**：候选缓存项c、请求签名s(r)、当前文档版本、当前证据指纹、工具指纹、模型标识和解码配置。  
**输出**：通过门控时直接输出缓存答案；未通过时输出缓存未命中及拒绝原因，并进入生成路径。

</div>

**直观理解**：语义相似只是入口条件，不是复用许可；即使问题相同，只要底层财报、引用段落、计算结果或模型配置发生变化，旧答案就不能直接使用。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 回退生成、依赖封装与缓存准入

系统执行工具计算和vLLM托管的Qwen2.5-Instruct生成，随后记录答案文本、引用文档与块、块哈希、文档版本、证据与工具指纹及请求签名；容量受限时依据效用U(c)决定准入，并按最低效用密度U(c)/M(c)淘汰。

<div class="method-step__io" markdown="1">

**输入**：未命中的请求、检索证据、必要的工具输出，以及指定的模型和解码配置。  
**输出**：新生成的答案，以及一个与全部生成依赖绑定的答案缓存项。

</div>

**直观理解**：一次昂贵生成完成后，系统不仅保存答案，还保存答案所依据的材料清单。空间不足时优先保留预计会重复使用、生成成本高、占用较小且不易因更新失效的答案。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 缓存答案的依赖一致性复用条件

$$
\operatorname{Serve}(c,r,\tau) \iff \bigl[s(r)\simeq s(c)\bigr] \land \bigl[\forall d\in D_c,\ v_{\tau}(d)=V(c,d)\bigr] \land \bigl[h_E(r)=h_E(c)\bigr] \land \bigl[h_T(r)=h_T(c)\bigr] \land \bigl[m=m(c)\bigr] \land \bigl[\theta=\theta(c)\bigr]
$$

**符号说明**

- $r=(q,m,\theta)$：当前服务请求；q为用户查询，m为模型标识，θ为解码配置。
- $c$：候选答案缓存项，包含答案及其生成依赖。
- $\tau$：复用判定的线性化点，即读取版本状态并决定是否返回缓存答案的逻辑时刻。
- $s(r),\ s(c)$：当前请求与缓存项的规范化金融签名；符号≃表示二者满足系统定义的签名兼容关系。
- $D_c$：缓存答案c所依赖的源文档集合。
- $v_{\tau}(d)$：在线性化点τ读取到的文档d当前版本。
- $V(c,d)$：生成缓存答案c时记录的文档d版本。
- $h_E(r),\ h_E(c)$：当前请求证据与缓存项记录证据的指纹。
- $h_T(r),\ h_T(c)$：当前工具执行状态与缓存项记录工具状态的指纹。
- $m(c),\ \theta(c)$：生成缓存答案c时使用的模型身份和解码配置。

<div class="equation-explanation" markdown="1">

**直观理解**：该式合并了原文式(2)至式(6)：所有条件是逻辑“且”关系，因此任何一个依赖不一致都必须回退到重新生成。它规定的是可审计的依赖新鲜度合同，而不是答案真实性判据；即使全部条件通过，答案质量仍需另行审计。  
**原文位置**：第3节，式(2)–(6)

</div>

</div>

<div class="equation-block" markdown="1">

#### 容量受限缓存的条目效用

$$
U(c)=\hat{H}(s(c))\,C(c)-\lambda_m M(c)-\lambda_f F(c)-\lambda_u R(c)
$$

**符号说明**

- $U(c)$：缓存项c的综合效用分数；正效用条目才被准入。
- $\hat{H}(s(c))$：对签名s(c)未来复用需求的估计。
- $C(c)$：复用该答案可避免的生成成本估计。
- $M(c)$：缓存项占用的存储空间。
- $F(c)$：答案依赖的文档扇出，即其关联文档规模或范围。
- $R(c)$：依赖文档发生更新、进而使答案失效的风险。
- $\lambda_m,\lambda_f,\lambda_u$：分别控制空间、文档扇出和更新风险惩罚强度的权重。

<div class="equation-explanation" markdown="1">

**直观理解**：收益项把预计复用频率与可节省的生成成本相乘，三个惩罚项分别对应空间占用、依赖范围和失效风险。容量耗尽时淘汰U(c)/M(c)最低的条目，即优先移除“单位空间价值”最小的答案；该策略只决定保存什么，不会让未通过一致性门的答案获得复用资格。  
**原文位置**：第4.5节，式(7)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。FinCacheServe是RAG服务与缓存管理方法，原文没有提出模型训练损失，也不通过梯度优化Qwen2.5或检索器；式(7)是在线/离线缓存策略的启发式效用函数，而非神经网络训练目标。离线CacheOpt从完整回放轨迹估计复用需求、文档扇出和更新风险，用于给出非Belady式的策略上界；在线CacheOpt则从近期请求和财报更新的滑动历史中估计这些量，以模拟可部署的自适应策略。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 金融请求签名与多级答案索引**

签名包含公司、期间、查询族、文档范围、工具要求、模型和解码配置。答案缓存同时维护重复请求的精确索引、面向同类金融意图的签名桶索引，以及供更新失效使用的文档到答案反向索引。

> 直观理解：普通语义缓存可能把语言相近但财务语境不同的问题混在一起；结构化签名把公司、时期和任务种类变成硬边界，同时仍允许同义改写复用同一答案。

**2. 依赖一致性复用门**

门控依次约束请求签名、证据指纹、文档版本、工具指纹和模型配置。证据指纹是引用块标识、块哈希及文档版本的顺序稳定摘要；工具指纹覆盖工具名称、工具版本、规范化输入和结构化返回值。

> 直观理解：它验证的不只是“问题像不像”，而是“答案的所有依据现在是否仍然一样”。哈希指纹把大量证据和工具状态压缩为可快速比较的摘要，但其目标是依赖新鲜度，并不直接证明答案事实正确。

**3. 版本化元数据平面与容量管理**

元数据平面管理版本存储、答案条目、反向依赖和门控日志，并以服务级元数据锁为读取和更新提供单一线性化顺序；托管LLM调用在锁外执行。正确性门与准入淘汰策略相互独立，后者可采用离线CacheOpt估计策略上界，或用近期请求与更新的滑动窗口实现在线估计。

> 直观理解：版本和失效操作必须有明确先后次序，否则查询可能在更新过程中读到旧答案；另一方面，换用不同淘汰算法不会放松一致性检查，因此性能优化不应破坏正确性边界。

**训练与推理**

训练阶段：原文方法章节未设置模型训练或微调流程，直接使用托管的Qwen2.5-Instruct模型、缓存嵌入和FAISS检索。离线轨迹统计只服务于缓存管理策略评估，不应解释为训练生成模型。

推理/服务阶段：请求先被规范化并解析金融身份，检索层得到当前证据，答案路由器从精确索引或签名桶提取候选；随后在元数据线性化点逐项验证签名、版本、证据、工具及模型配置。命中则直接返回答案并标记跳过LLM调用；未命中则执行检索补全、必要工具计算和托管模型生成，再将答案及完整依赖记录封装为缓存项，经效用策略决定是否准入。文档更新进入元数据平面后，系统先修改版本存储并通过反向索引失效依赖答案，因而后续门控读取不会把更新前条目视为有效。

**复现信息**

实现由请求规范化器、检索缓存、答案缓存、元数据平面和托管生成连接器五部分组成。检索采用缓存嵌入与FAISS搜索，生成采用vLLM托管的Qwen2.5-Instruct；答案缓存维护精确索引、金融签名桶和文档到答案的反向索引。系统按请求记录路由结果、LLM是否调用、证据与工具哈希、版本检查、陈旧来源类别及服务调用闭合状态，以支持一致性审计。

并发方面，版本存储更新和答案条目变更由服务级元数据锁保护，而耗时的托管LLM调用在临界区外执行；这使缓存读取与财报更新具有单一线性化顺序，同时避免长时间占锁。原文给出的复杂度为：精确或分桶候选查找近似O(1)，之后只检查小型候选集合；更新一份被k个答案依赖的文档时失效成本为O(k)；N个答案条目和E条文档—答案依赖边的元数据空间为O(N+E)。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- SEC 衍生财务文档工作负载：请求覆盖流动性、收入、利润率、债务、风险、现金流、申报变化和比率分析等类别，并带有公司、期间、文档范围及来源版本信息。主要托管轨迹含 2,230 个请求，使用 Qwen2.5-7B，用于完整统计提供商侧 LLM 调用及依赖过期输出；另有 208 请求的释义/更新压力集，用来显式制造相同意图、改写请求和申报文件更新。
- 32B operator suite：三次托管种子运行共 544 个请求，使用 Qwen2.5-32B，主要用于与较强安全缓存基线进行比较。其归档轨迹还用于容量与 SLO 重放：容量实验预热 120 个请求，并在五条归档轨迹上重放 895 个测量请求和 110 次文件更新。
- 受控安全与元数据压力集：金融近碰撞套件含 2,376 个探针，覆盖发行人、期间、申报范围、查询族、工具与证据漂移、模型和生成参数变化以及文档版本更新；交错查询/更新压力测试在每个设置中执行 4,096 次查询和 512 次更新，并扩展到 100k 缓存条目，用于检验缓存契约边界、并发一致性及后端可扩展性。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**LLM skip rate（LLM 调用跳过率）**

无需再次执行生成模型的请求比例，直接反映答案复用减少 GPU 密集型生成工作的能力。 （在依赖新鲜度相同的前提下越高越好；若高跳过率伴随过期输出，则不能视为可部署收益。）

</div>
<div class="metricitem" markdown="1">

**Dependency-stale outputs（依赖过期输出数或比例）**

答案命中时，其文档版本、检索证据、工具输出、模型身份或生成配置已不再满足原缓存契约的请求数量或占比。 （越低越好，理想值为零；论文报告的是实验中“观测到的”过期输出，零观测不等于对所有真实输入的形式化正确性证明。）

</div>
<div class="metricitem" markdown="1">

**SLO-constrained goodput 与每千次 fresh SLO success 的 GPU-sec/Wh**

Goodput 只计入无错误、依赖新鲜且在时延预算内完成的请求；GPU 秒和 Wh 则衡量每 1,000 次此类有效成功所需的计算或估算电能。 （Goodput 越高越好，单位有效成功的 GPU 秒或 Wh 越低越好；该组合避免把快速但过期的响应误计为服务收益。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 主要托管 Qwen2.5-7B 全轨迹，共 2,230 个请求

<div class="result-value" markdown="1">

FinCacheServe 跳过 1,188 次 LLM 调用，即 53.27%，同时观测到 0 个依赖过期输出；相比之下，无新鲜度保护的 TTL 与语义缓存各跳过 1,173 次，但各产生 1 个过期输出。

</div>

该结果表明，答案级复用在完整提供商调用核算下可以消除超过一半的生成调用，而且本轨迹中没有观察到因依赖变化而失效的缓存答案。它还说明过期来源不只存在于答案缓存：检索缓存基线即使不跳过 LLM，也可能把旧证据送入生成路径。不过，这只是单条 7B 财务轨迹上的经验结果，不能证明所有文档更新模式下都绝不会出现过期答案。

<div class="result-source" markdown="1">

来源：第 7.1 节，表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">FinCacheServe skips 1,188 of 2,230 LLM calls (53.27%) with zero observed dependency-stale outputs.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 三个托管 Qwen2.5-32B operator-suite 种子，共 544 个请求

<div class="result-value" markdown="1">

FinCacheServe 的跳过率为 53.31%，95% 置信区间为 [49.11%, 57.46%]，依赖过期数为 0；版本化语义缓存为 38.97%，grounded-style reuse 为 22.43%，两者同样没有观测到过期输出。FinCacheServe 相对最强安全语义基线提高 14.34 个百分点。

</div>

在更大模型和多种子条件下，FinCacheServe 不只是超过不安全基线，而是在同样满足实验中新鲜度要求的安全策略之间取得更高复用率。因此，主要收益可归因于更细的金融意图索引与依赖契约，而不是简单放松安全门。置信区间反映这三次运行中的统计不确定性，但样本仍限于论文构造的 operator suite。

<div class="result-source" markdown="1">

来源：第 7.3 节，表 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">FinCacheServe skips 290 of 544 requests (53.31%, 95% CI [49.11, 57.46]) with zero observed dependency-stale outputs.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 归档托管 32B 指标上的 2 秒 SLO 与 450 W 能耗重放

<div class="result-value" markdown="1">

FinCacheServe 达到 53.31% 的依赖新鲜 goodput，单位 1,000 次依赖新鲜 SLO 成功需要 22.40 GPU 秒；按 450 W 换算为 2.80 Wh，而版本化语义缓存为 5.03 Wh，故降低 44.30%。无新鲜度签名缓存虽然估算为 1.41 Wh，但有 23.16% 的请求依赖过期。

</div>

缓存命中能在生成路径约需 3 秒时满足 2 秒预算，因此调用跳过确实转化为有效服务成功，而不只是账面上的命中率。与最强安全语义基线相比，FinCacheServe 每次有效成功所需资源更少；不安全缓存的更低能耗不能直接比较为可部署优势。Wh 来自 GPU 秒和板卡功率假设，未包含 CPU、存储、网络及整机功耗，也不是现场电能测量。

<div class="result-source" markdown="1">

来源：第 7.7 节，图 9；相关 goodput 与 GPU 秒见表 8

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">At 450 W, FinCacheServe uses 2.80 Wh per 1,000 fresh SLO successes, compared with 5.03 Wh for versioned semantic caching and 11.15 Wh for grounded-style reuse.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所有主要工作负载均为 SEC 衍生财务文档和 Qwen2.5/vLLM 路径；未报告其他企业领域、其他模型家族、跨语言请求或长期真实生产流量，因此复用率、更新分布与安全表现的外部有效性仍需验证。零 dependency-stale 是“零观测”，不是形式化证明。
- SLO 与能耗结论来自归档逐请求指标重放和板卡功率假设，而容量实验部分属于确定性元数据平面重放；它们没有完整测量端到端整机功耗、网络与检索开销，也不能完全反映线上负载突发、分布漂移和多节点缓存协调成本。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Versioned semantic cache（版本化语义缓存）：语义匹配之外检查文档版本，是最强的安全语义基线；它用于判断 FinCacheServe 的金融意图和多依赖契约是否能在同样保持零观测过期输出时增加复用。
- Grounded-style reuse（基于证据的安全复用）：依赖检索证据或文档落地信息来约束命中，但没有完整的金融身份、模型和配置契约；它检验仅保证“证据相似或一致”是否足够。
- Semantic/signature cache without freshness（无新鲜度检查的语义或签名缓存）：允许积极命中但不随依赖更新失效，是不安全负对照；它揭示高跳过率是否只是以返回过期答案为代价。
- LRU、LFU、TinyLFU 与 Belady-style oracle：前三者代表常见容量受限缓存管理，离线 Belady 式策略提供知道未来访问序列时的性能上界；它们用于评估 CacheOpt 的准入与淘汰决策，而非答案语义质量。

**实验想回答的问题**

- 在企业财务文档会持续更新的 RAG 服务中，FinCacheServe 能否在不返回依赖过期答案的前提下，比现有安全缓存策略跳过更多 LLM 调用，并将这种调用节省转化为吞吐量、SLO 有效吞吐和能耗收益？
- 系统的安全性与效率分别来自哪些机制：金融意图签名和依赖失效是否缺一不可，容量受限时的准入与淘汰策略能否接近离线最优，同时在并发更新及持久化元数据后端上保持一致性？

**实验实现**

托管实验在 vLLM 上运行 Qwen2.5-7B、14B 和 32B，并按请求统计是否实际调用模型、依赖是否过期及延迟。32B 强基线比较采用三个托管种子；置信区间按论文表格报告。容量实验固定依赖一致性门，仅改变缓存容量和准入/淘汰策略，并以五条归档轨迹的标准差作为误差条。2 秒 SLO 重放使用归档的逐请求托管指标，能耗由 GPU 秒和明确的 450 W 板卡功率假设换算，因此属于估算而非直接电表测量。元数据路径同时在内存实现和 SQLite/WAL 事务实现上验证；安全性还通过字段级边界探针、2,376 个近碰撞探针以及交错查询/更新压力测试检查。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 32B operator suite：移除金融签名门或移除新鲜度失效 | 完整 FinCacheServe 跳过率为 53.31%、过期数为 0；移除 signature gate 后，安全跳过率降至 10.48%、过期数仍为 0；保留签名但移除 freshness invalidation 后，跳过率保持 53.31%，却产生 126 个依赖过期输出。 | 这一对消融分别隔离“找到可复用的同类金融请求”和“依赖变化后撤销复用资格”两个机制。签名门负责把安全复用从粗粒度实体—期间匹配提升到更高覆盖率；失效机制本身不提高命中率，却决定这些命中在更新后是否仍可信。因此完整收益来自二者组合，而非单一组件。 | 第 7.3 节，表 5<br><span class="experiment-evidence">Removing the financial-signature layer reduces safe reuse to 10.48%, matching the entity-period semantic baseline. Removing freshness invalidation preserves skip rate but exposes 126 dependency-stale outputs.</span> |
| 字段级复用门边界探针 | 完整门接受 1 个安全释义且接受 0 个不安全案例；分别删除 query family、period key、tool hash、model identity、generation parameters 或 evidence fingerprint 时，每种设置都额外接受 1 个对应的不安全边界案例。 | 该消融不是衡量总体吞吐，而是验证缓存键中每个字段是否有独立安全作用：查询族与期间防止财务意图近碰撞，工具和证据指纹防止支撑信息变化，模型及生成参数身份防止把不同生成契约视为同一对象。公司、范围、工具或来源字段单独删除未暴露当前探针，是因为其他重叠门仍能拒绝案例，不能据此断言这些字段在真实流量中多余。 | 第 7.8 节，表 9<br><span class="experiment-evidence">Removing query family, period, tool hash, model identity, generation parameters, or evidence fingerprint exposes at least one unsafe reuse case.</span> |

**定性案例**

- 受控金融近碰撞套件可视为缓存契约案例研究：2,376 个请求都与已缓存请求语义相似，但只有良性释义应被复用。全局语义缓存接受 100% 的不安全案例，版本化语义缓存仍接受 87.18%，grounded-style reuse 接受 35.90%，FinCacheServe 接受 0% 且良性释义接受率为 100%。这说明“语义相似”“文档版本一致”或“证据一致”任一单独条件都不足以刻画可安全复用的财务答案；但该结论严格限于受控覆盖的碰撞类型。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出具备依赖一致性的答案缓存与复用机制，以减少可变文档 RAG 服务中的 LLM 调用、能耗和延迟。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`13ef891662e64af5c7944f460592deb782f284b3f86a87771421a56939cb7389`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
