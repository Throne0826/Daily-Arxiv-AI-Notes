---
title: "[论文解读] CRAFT: LLM-Based Iterative Refinement for Temporal Reasoning over Clinical Narratives"
description: "[arXiv 2608.12779][LLM Reasoning] 本文针对缺少明确时间锚点的单份临床叙事，研究如何利用大语言模型的生成器与基于约束的验证器，通过定向反馈和迭代修正，重建分阶段的症状发展轨迹。"
arxiv_id: "2608.12779"
announcement_date: "2026-08-14"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:58:57.030399+00:00"
source_sha256: "3b74e358fdade780171954851e166fd65710472ce47361ecfd94e8366f64226f"
tags:
  - "LLM Reasoning"
  - "临床时间推理"
  - "症状轨迹重建"
  - "弱时间锚定"
  - "阶段式排序"
  - "临床叙事"
  - "迭代细化"
  - "大语言模型"
  - "MedTempo"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.12779</p>

# CRAFT: LLM-Based Iterative Refinement for Temporal Reasoning over Clinical Narratives

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Chengyang He, Tahreem Arif, Marko Zivkovic, Lijing Wang, Yue Ning, Ping Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Thanks: Stevens Institute of Technology, Hoboken, NJ, 07030, USA；Thanks: Genesis Research Group, Hoboken, NJ, 07030,USA；Thanks: New Jersey Institute of Technology, Newark, NJ, 07102, USA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12779v1) · [PDF 下载](https://arxiv.org/pdf/2608.12779v1) · **关键词** 临床时间推理, 症状轨迹重建, 弱时间锚定, 阶段式排序, 临床叙事, 迭代细化, 大语言模型, MedTempo<br>


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

本文针对缺少明确时间锚点的单份临床叙事，研究如何利用大语言模型的生成器与基于约束的验证器，通过定向反馈和迭代修正，重建分阶段的症状发展轨迹。

**不用术语来说**：疫苗不良事件等临床报告通常把多个症状写在一段自由文本中，却不一定注明每个症状发生的准确日期；同一症状还可能被重复提及、描述为持续或好转。因此，系统不能简单按照症状在文本中的出现顺序判断真实发生顺序，而人工逐份整理又成本很高。本文要解决的是：给定一份报告及其中的症状列表，自动判断哪些症状属于同一阶段，并恢复各阶段的先后次序。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 CRAFT，将弱时间锚定条件下的症状轨迹重建建模为迭代结构化预测：生成器提出分阶段轨迹，验证器依据多项时间约束检查候选结果并提供定向反馈，生成器据此重新生成；同时设置受控基线和消融配置，以区分生成与验证机制的作用。
- 构建 MedTempo 基准，收录 5,347 份覆盖三种新冠疫苗的不良事件叙事，其中 3,166 份具有不同症状进展的时间证据并配有专家验证的阶段式顺序标注，从而补足单报告、缺少绝对时间锚点场景的标准化评测资源。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

临床时间推理旨在从病历叙述中恢复症状或其他临床事件的先后关系，以支持疾病进展建模、治疗效果监测和安全信号检测。传统时间信息抽取通常先识别事件与时间表达，再判断事件对之间的时间关系并据此构造全局顺序；但本文关注的场景更困难：每位患者只有一份自由文本报告，缺少日期等绝对时间锚点，先后关系往往隐含在“随后”“持续”“再次出现”等相对描述以及症状状态变化中，同时共现、复述和更新也可能造成误判。研究目标因此不是孤立地判定若干事件对，而是把报告中的给定症状组织成按阶段分组的完整进展轨迹。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**时间锚点**

能够把事件定位到时间轴上的明确线索，例如日期、时间戳或“接种后第三天”。“弱时间锚定”表示文本主要依赖隐含或相对线索，缺少稳定的绝对时间信息。

</div>
<div class="concept-item" markdown="1">

**成对时间关系分类**

对两个事件判断先于、后于或同时等关系，再由多组局部判断推导整体顺序。它侧重事件对是否判断正确，不一定直接产生可供使用的分阶段患者轨迹。

</div>
<div class="concept-item" markdown="1">

**阶段式症状轨迹**

把症状按照临床叙述所支持的发生阶段排序，同一阶段可包含同时发生或无法进一步区分先后的多个症状。与简单线性列表相比，这种表示同时保留阶段顺序和阶段内分组信息。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文研究单报告、弱时间锚定条件下的临床症状进展重建。每个样本的输入是一篇疫苗不良事件自由文本叙述及其配套症状列表；系统需要利用显式或隐式时间证据，将这些症状组织为有序的阶段式轨迹，输出哪些症状处于同一阶段以及各阶段的先后次序。MedTempo共含5347篇来自Pfizer、Moderna和Janssen三类疫苗的报告，每位患者仅对应一篇报告且没有显式绝对时间锚点；当前基准只评估其中具有不同症状阶段之时间证据并获得专家验证标注的3166篇报告，其余不含时间进展的报告保留用于未来的时间证据识别研究。该设定假定症状列表已经提供，因此核心问题是排序与分组，而不是从原文中重新发现全部症状。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **TimeML、TempEval及其后续成对时间关系分类范式**: 这些工作建立了事件、时间表达和时间关系的标准化表示与评测方式，通常先预测局部事件对关系，再诱导全局一致顺序。CRAFT所研究的问题不同：它要求在时间锚点稀疏的单篇临床报告中端到端恢复有序且分组的症状轨迹，而非仅评价局部关系是否正确。
- **Self-Refine**: Self-Refine通过模型生成的反馈反复修改模型输出，为CRAFT的迭代细化思路提供了直接先例。CRAFT将这一范式专门化为临床时间排序任务，采用结构化轨迹表示和面向时间约束的验证机制；与依赖人工复核的临床迭代抽取方案相比，其目标是实现全自动、可跨不同模型能力层级比较的基准评测。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

恢复症状随时间的进展对于疾病进程建模、治疗结果监测和安全信号检测具有实际价值，但临床自由文本中的时间线索往往是隐含的，或只表达某事件相对另一事件的先后关系，而不是固定日期；共现、重复叙述和症状状态更新又会进一步混淆真实顺序。依赖人工将这些描述整理成阶段式轨迹既耗时，也难以支撑大规模监测。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **事件抽取与成对时间关系分类**：先识别文本中的事件和时间表达，再为事件对预测先于、晚于或重叠等关系，最后由这些局部关系推导全局排序；近期工作还扩展到更完整的关系覆盖和复杂时间事实抽取。
- **基于大语言模型的临床时间推理**：利用大语言模型理解临床文本并推断事件顺序，但现有方法通常建立在多次就诊记录、与时间戳关联的监督信号或其他受约束的数据条件之上。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 成对关系分类主要优化局部事件关系，并多在少数语料库和固定关系集合上研究，不能直接满足从一份报告中输出完整、分阶段症状轨迹的要求；局部预测还需要额外机制才能形成结构一致的全局结果。
- 现有临床大语言模型方法依赖多次就诊时间线、时间戳监督或特定数据条件，而单份报告常没有绝对时间锚点，因此这些前提在目标场景中并不成立；同时，相关基准缺乏多样性，难以标准化比较该场景下的方法。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未充分覆盖一种明确的任务设置：输入是每位患者的一份临床叙事及给定症状列表，文本缺少明确绝对时间锚点，但含有隐式相对时间证据；输出则不是若干孤立的事件对关系，而是经结构化分组和排序的阶段式症状进展轨迹。该设置同时缺少专门方法与专家标注的标准化评测基准。

</div>
<div markdown="1"><span>核心问题</span>

在单报告、弱时间锚定的条件下，能否让大语言模型先生成候选症状轨迹，再由任务专用的约束验证器识别时间排序问题并提供反馈，通过多轮修正稳定提高阶段划分与全局排序的准确性；并且这种提升能否在不同能力层级的大语言模型上成立，且可分别归因于生成器和验证器？

</div>
<div markdown="1"><span>作者直觉</span>

隐式时间信息往往分散在“随后”“持续”“再次出现”以及症状状态变化等局部描述中，一次生成容易漏掉线索或产生彼此冲突的排序。CRAFT 的切入点是把复杂任务拆成“提出完整答案、按明确标准检查、针对问题重写”的循环：生成器负责综合上下文形成全局轨迹，验证器则像校对者一样把结构或时间约束违规转化为定向反馈。这样既保留大语言模型理解含蓄叙述的能力，又用外部检查限制其不一致输出。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CRAFT把单份临床叙事中的症状时间推理建模为“分阶段排序”任务。对报告$r$，输入包括自由文本叙事$x_r$以及VAERS已提供的临床发现集合$\mathcal{F}(r)=\{f_1,\dots,f_n\}$；系统不负责从文本中识别症状实体，而是把每个给定发现恰好分配到一个非空时间桶，输出按最早到最晚排列的序列$\mathcal{B}(r)=(B_1,\dots,B_K)$。同一时间桶中的发现被视为处于患者病程的同一阶段，评测只考察桶之间的顺序和桶内分组，不评价可选的证据片段。任务要求叙事明确表达至少一种新发现晚于先前发现；仅有同时发生、严重程度变化、症状消退，或只能通过持续时长猜测先后关系的情况不算时间进展。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造结构化任务输入

系统直接采用$\mathcal{F}(r)$作为待排序项目，不执行实体抽取或医学编码；提示同时规定何为时间进展，以及哪些现象不能据此推断新的时间阶段。

<div class="method-step__io" markdown="1">

**输入**：一份报告$r$的自由文本临床叙事$x_r$，以及VAERS的SYMPTOM字段所提供的MedDRA首选术语集合$\mathcal{F}(r)$。<br>
**输出**：由叙事、闭集症状清单和任务约束组成的生成器输入。

</div>

**直观理解**：系统拿到的是“病历文字”和“必须摆放的症状卡片”。它只判断这些卡片的先后与同期关系，不再从病历中寻找新的卡片。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成候选阶段时间线

第$i$轮由生成器$g$重新生成完整候选$\hat{\mathcal{B}}^{(i)}(r)$，将给定发现组织为从最早到最晚的JSON时间桶。CRAFT-Full每轮使用完整任务说明，并在后续轮次把验证器反馈追加到上下文中。

<div class="method-step__io" markdown="1">

**输入**：症状集合$\mathcal{F}(r)$、叙事$x_r$，以及上一轮反馈$\text{feedback}^{(i-1)}$；首轮反馈为空。<br>
**输出**：候选JSON桶序列$\hat{\mathcal{B}}^{(i)}(r)$。

</div>

**直观理解**：生成器先提交一份完整的症状时间表；收到批改意见后，它不是只改一个局部字段，而是结合原文和意见重新交一份完整答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 规范化并验证候选

验证器先调用确定性的FormatTool，把原始输出规范为统一JSON桶结构但不改变时间内容；随后按五项加法量表检查格式与方向、未提及症状的处理、症状唯一覆盖、同期分组和基于叙事线索的跨组排序，每项一分。

<div class="method-step__io" markdown="1">

**输入**：原始候选$\hat{\mathcal{B}}^{(i)}(r)$、症状集合$\mathcal{F}(r)$和临床叙事$x_r$。<br>
**输出**：分数$\text{score}^{(i)}\in\{0,\dots,5\}$、决策$\text{decision}^{(i)}\in\{\text{ACCEPT},\text{REVISE}\}$，以及指出具体问题的$\text{feedback}^{(i)}$。

</div>

**直观理解**：FormatTool像格式整理器，只把答案整理成可检查的表格；验证器再像阅卷者，分别检查是否漏项、重复、错误合并或颠倒顺序，并给出可执行的修改意见。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 反馈迭代与停止

当$\text{score}^{(i)}\geq\theta$时返回ACCEPT并停止；否则将定向反馈送回生成器进入下一轮。若经过$T_{\max}$轮仍没有候选被接受，系统终止并返回最后一轮候选。

<div class="method-step__io" markdown="1">

**输入**：当前轮决策、分数、反馈、接受阈值$\theta$和最大迭代次数$T_{\max}$。<br>
**输出**：最终阶段式症状时间线，即被接受的候选，或达到预算上限时的最后候选。

</div>

**直观理解**：流程相当于“作答、检查、按意见重做”，直到答案达到验收线；迭代上限保证系统不会无限修改，但达到上限并不等于最后答案已经通过验证。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 阶段式时间线表示

$$
\mathcal{B}(r)=(B_1,B_2,\dots,B_K),\qquad \bigcup_{k=1}^{K}B_k=\mathcal{F}(r),\quad B_k\neq\varnothing,\quad B_j\cap B_k=\varnothing\ (j\neq k)
$$

**符号说明**

- $r$：一份接种后不良事件报告。
- $\mathcal{F}(r)$：报告$r$中由VAERS SYMPTOM字段给出的全部临床发现集合。
- $\mathcal{B}(r)$：报告$r$的阶段式时间线，即按时间排序的桶序列。
- $B_k$：第$k$个非空时间桶，包含被判断为处于同一病程阶段的发现。
- $K$：预测时间线中的阶段总数。
- $k$：时间桶索引，数值越小表示阶段越早。

<div class="equation-explanation" markdown="1">

**直观理解**：该表示把所有给定症状划分成互不重叠的若干组，并要求每个症状恰好出现一次；组内表示同期，组间索引表示先后。原文直接给出有序非空桶序列及“每个发现恰好分配到一个桶”的约束，这里用并集、非空和两两不交把该文字约束显式写出，并未增加新的学习目标。<br>
**原文位置**：第4.1节 Problem Formulation and Temporal Representation

</div>

</div>

<div class="equation-block" markdown="1">

#### 生成器与验证器的迭代映射

$$
\hat{\mathcal{B}}^{(i)}(r)=g\!\left(\mathcal{F}(r),x_r,\operatorname{feedback}^{(i-1)}\right),\qquad \left(\operatorname{decision}^{(i)},\operatorname{feedback}^{(i)},\operatorname{score}^{(i)}\right)=v\!\left(\mathcal{F}(r),x_r,\hat{\mathcal{B}}^{(i)}(r)\right)
$$

**符号说明**

- $i$：当前迭代轮次；首轮$i=1$时上一轮反馈为空。
- $x_r$：报告$r$的自由文本临床叙事。
- $g$：根据症状、叙事和上一轮反馈生成完整候选时间线的生成器。
- $\hat{\mathcal{B}}^{(i)}(r)$：生成器在第$i$轮提出的候选时间线。
- $v$：检查候选结构与时间约束并产生决策、反馈和分数的验证器。
- $\operatorname{feedback}^{(i)}$：验证器在第$i$轮给出的定向修正意见。
- $\operatorname{decision}^{(i)}$：第$i$轮的ACCEPT或REVISE决策。
- $\operatorname{score}^{(i)}$：第$i$轮五项加法量表的总分，取值为0至5。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分描述生成器如何结合原始输入和历史反馈提出候选，第二部分描述验证器如何对同一候选进行评分和诊断。两式通过反馈变量首尾相接，构成CRAFT的核心闭环；验证器不是直接生成最终时间线，而是以约束检查结果引导下一轮生成。<br>
**原文位置**：第4.2.1节 Generator Agent 与第4.2.2节 Verifier Agent

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文所给方法不是通过一个新的可微损失函数训练生成器或验证器，也未描述对四种大语言模型骨干进行参数微调；因此这里没有可报告的训练目标。五项加法量表是推理阶段的候选验收与反馈机制：验证器计算$\text{score}^{(i)}$，并以$\text{score}^{(i)}\geq\theta$决定是否提前停止，但该分数不应被误解为用于反向传播的优化损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 生成器代理**

生成器是一个大语言模型代理，实现映射$g:(\mathcal{F}(r),x_r,\text{feedback}^{(i-1)})\rightarrow\hat{\mathcal{B}}^{(i)}(r)$。它必须只使用$\mathcal{F}(r)$中的原始发现名称，以JSON桶序列表达同期分组和阶段先后，并避免叙事未支持的时间推断。

> 直观理解：该模块负责把非结构化病历转成结构化时间线。把症状清单设为封闭集合，可以把主要难点集中在时间推理上，并减少模型自行添加、改写或遗漏医学概念的空间。

**2. FormatTool**

FormatTool是验证前调用的确定性辅助模块，只把生成器原始输出规范到统一JSON桶模式，不修改症状之间的时间关系。其作用是将表示错误与推理错误分开，避免验证器因代码围栏、字段包装或其他表面格式差异而无法检查候选。

> 直观理解：它只负责“排版和装订”，不替生成器改答案。因此，格式被修好后仍然保留原候选的时间判断，后续评分更能反映真正的结构与顺序问题。

**3. 约束验证器代理**

验证器实现$v:(\mathcal{F}(r),x_r,\hat{\mathcal{B}}^{(i)}(r))\rightarrow(\text{decision}^{(i)},\text{feedback}^{(i)},\text{score}^{(i)})$。五项量表分别要求：JSON有效且按最早到最晚排列；文本未提及的症状置于最终的“none”组；每个症状恰好使用一次；时间相近的症状正确合组；各组顺序符合叙事中的时间线索。

> 直观理解：验证器把“这份时间线是否可信”拆成五个可定位的条件，而不是只给笼统的对错判断。反馈能够告诉生成器下一轮应修复漏项、重复、分组还是顺序，从而让迭代具有明确方向。

**训练与推理**

就所给章节而言，CRAFT是一个完全自动化的推理时迭代框架。每份报告独立处理：首轮将$\mathcal{F}(r)$、$x_r$和完整任务定义交给生成器；候选经FormatTool规范化后，由验证器按照五项约束产生分数、ACCEPT/REVISE决策和定向反馈。若未达到阈值$\theta$，下一轮生成器读取相同原始输入及上一轮反馈，完整重建候选；达到阈值则提前返回，超过$T_{\max}$仍未通过则返回最后候选。数据集标注阶段曾用GPT-4o mini生成初始时间线，再由两名具有医学NLP背景的标注者独立审核并协商裁决，但这是MedTempo金标准的构建过程，不是CRAFT的模型训练过程。

**复现信息**

公平解释或复现所必需的设计包括：输入症状必须直接取自VAERS的MedDRA首选术语列表，不能把实体抽取误差计入排序方法；输出采用从最早到最晚的JSON非空桶序列，每个给定症状只出现一次，同期症状位于同一桶；FormatTool只能规范格式，不能修改时间内容；CRAFT-Full在每轮执行完整再生成，并追加上一轮反馈；验证器采用五项各一分的加法量表，并通过阈值$\theta$和上限$T_{\max}$控制停止。所给原文未明确报告$\theta$、$T_{\max}$的具体数值、提示词全文、解码参数、四种骨干模型名称及不同CRAFT配置的具体差异，因此不能据此补造这些设置；这些缺失项会影响严格复现，需回查算法、附录或实验章节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MedTempo：包含 5,347 条 COVID-19 疫苗不良事件叙事，每条叙事附带给定症状列表，覆盖 Janssen、Moderna 和 Pfizer 三种疫苗。实验的主要作用是检验模型能否从缺少明确时间锚点的单份临床叙事中，将全部症状恢复为按阶段排列的时间线。
- MedTempo-T：从 MedTempo 中选取具有明确症状进展证据的 3,166 条报告作为主要评测集，其中 Janssen、Moderna、Pfizer 分别为 1,164、983、1,019 条。其余报告不包含时间进展，因而不进入主基准；原文未明确报告训练集、验证集和测试集的进一步划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Strict Exact Match（EM）**

只有预测与金标准具有完全相同的阶段数、阶段顺序以及各阶段症状集合时才记为正确；阶段内部的症状顺序不计。它衡量整条结构化时间线是否一次性完全恢复，因此最严格。 （越高越好；更高表示更多报告的阶段划分和跨阶段顺序均与专家标注完全一致。）

</div>
<div class="metric-item" markdown="1">

**Group-Aware LCCS**

把每个症状阶段视作一个整体标记，计算预测与金标准之间最长的连续相同阶段片段。它奖励未被打断的正确阶段序列，并会受到局部分组错误的明显影响。 （越高越好；更高表示模型恢复了更长的连续正确时间片段，但不要求整条时间线完全正确。）

</div>
<div class="metric-item" markdown="1">

**Kendall's $\tau_b$**

比较共同症状两两之间的先后关系，并显式处理同一阶段形成的并列关系；取值范围为 $[-1,1]$，其中 $1$ 表示完全一致，$-1$ 表示完全反转。 （越高越好；更高表示症状对的相对时间顺序更接近金标准，但它可能在阶段边界仍不完全正确时保持较高数值。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### GPT-4.1：CRAFT-Full 与 PIVOT、GUIDE 的总体比较

<div class="result-value" markdown="1">

CRAFT-Full 的总体 EM、LCCS、$\tau_b$ 分别为 35.61%、61.46%、57.77%；PIVOT 为 34.60%、59.24%、57.20%，GUIDE 为 33.97%、59.80%、58.24%。因此 CRAFT-Full 在严格完全匹配和连续阶段恢复上最好，但其 $\tau_b$ 略低于 GUIDE。

</div>

作者数据支持 CRAFT-Full 更容易恢复完整阶段结构和较长的连续正确阶段，但不支持其在所有排序指标上全面领先。分析上，这种差异说明 LCCS、EM 与 $\tau_b$ 检查的是不同错误：CRAFT-Full 可能改善阶段边界和整体结构，同时未增加所有症状对的排序一致性。

<div class="result-source" markdown="1">

来源：表 5.1，GPT-4.1 模型块；数值依次按 Janssen、Moderna、Pfizer、Total 报告 EM、LCCS、$\tau_b$

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GPT-4.1 PIVOT 33.65 59.56 58.89 38.53 60.73 55.43 31.89 57.44 57.00 34.60 59.24 57.20
GPT-4.1 GUIDE 33.99 61.02 60.07 36.70 60.68 56.48 31.30 57.57 57.85 33.97 59.80 58.24
GPT-4.1 CRAFT-Full† 34.43 61.68 59.58 40.06 63.84 56.45 32.68 58.93 56.97 35.61 61.46 57.77

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Llama-3.3-70B：CRAFT-Full 与锚点式基线的总体比较

<div class="result-value" markdown="1">

CRAFT-Full 的总体 EM、LCCS、$\tau_b$ 为 28.04%、52.45%、52.43%，均高于 PIVOT 的 27.22%、51.04%、51.27%和 GUIDE 的 26.08%、49.25%、49.58%。

</div>

这是较清晰的跨指标改进：在 Llama-3.3-70B 上，加性验证与完整重生成的组合同时改善整条时间线、连续阶段片段和成对顺序。然而，这只是同一数据集上的配置比较，不能单独证明改进可迁移到其他临床事件类型。

<div class="result-source" markdown="1">

来源：表 5.1，Llama-70B 模型块

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Llama-70B PIVOT 24.76 50.18 51.98 30.58 52.81 49.53 26.77 50.33 52.13 27.22 51.04 51.27
Llama-70B GUIDE 23.73 48.59 50.81 30.28 51.40 48.53 24.70 47.94 49.17 26.08 49.25 49.58
Llama-70B CRAFT-Full† 25.88 52.06 53.47 31.90 53.89 50.69 26.77 51.49 52.93 28.04 52.45 52.43

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Claude Sonnet 4.5：方法排名随指标变化

<div class="result-value" markdown="1">

Claude-4.5 上，CRAFT-Full 的总体 EM、LCCS、$\tau_b$ 为 37.14%、61.60%、54.94%。其 LCCS 是该模型块最高值，但 EM 低于 CRAFT w/o V 的 37.83%，$\tau_b$ 低于 CRAFT-G 的 55.47%，说明 CRAFT-Full 并非在强模型上统一占优。

</div>

该结果限制了“验证迭代必然提升强模型”的结论。分析上，Claude 的单次生成已经较强，验证反馈可能改善连续阶段结构，却也可能引入局部重排或阶段改写，从而降低严格完全匹配或成对排序；表格只能显示这种权衡，不能确定具体错误机制。

<div class="result-source" markdown="1">

来源：表 5.1，Claude-4.5 模型块

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Claude-4.5 CRAFT w/o V 37.19 57.73 56.03 40.88 59.85 54.20 35.63 55.23 53.06 37.83 57.58 54.51
Claude-4.5 CRAFT-G 33.74 61.04 57.58 40.67 63.39 53.99 34.06 59.57 54.50 35.99 61.30 55.47
Claude-4.5 CRAFT-Full† 35.89 61.82 56.68 41.18 64.51 54.98 34.65 58.54 52.92 37.14 61.60 54.94

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

- PIVOT：使用与 CRAFT-Full 相同的完整重生成器，但将验证器替换为基于锚点的验证器。该验证器把接种日期视为中心时间锚点，从 5 分开始，遇到锚点顺序矛盾、阶段合并或拆分错误、整体时间线与文本线索不一致时扣分。它用于检验加性规则验证是否优于传统的固定锚点式判断。
- GUIDE：采用局部编辑生成器和基于锚点的验证器；后续迭代直接修改上一版候选时间线，而非从叙事重新生成。它是有意义的比较对象，因为它同时代表“局部修补”生成策略和传统锚点验证策略。
- CRAFT-G：保留 CRAFT 的加性规则验证器，但把完整重生成器替换成局部编辑生成器。该配置控制验证器不变，用于隔离完整重生成策略的贡献。
- CRAFT w/o V：仅运行一次生成，不执行验证和反馈迭代。该配置用于衡量验证闭环相对于单次提示生成的实际作用。

**实验想回答的问题**

- 方法有效性与组件贡献：CRAFT-Full 在不同能力层级的大语言模型上，是否优于采用时间锚点验证器的 PIVOT、GUIDE，以及性能变化主要来自完整重生成器还是加性规则验证器？
- 模型与数据条件的稳健性：四种大语言模型在 MedTempo 上的能力排序是否稳定，且不同疫苗类型是否会改变模型表现、错误模式或方法排名？

**实验实现**

实验使用 GPT-4.1、Claude Sonnet 4.5、MedGemma-27B 和 Llama-3.3-70B 四种骨干模型。专有模型通过官方 API 以确定性解码运行；开放权重模型通过 Hugging Face Transformers、本地双 NVIDIA RTX A5000 GPU 和 NF4 4-bit 量化运行。所有配置使用固定提示模板和严格 JSON 输出模式，要求给定症状列表中的每个症状恰好出现一次；若文本无法支持阶段内部顺序，则将相关症状放入同一阶段。生成长度上限为 512 个新 token。带生成器—验证器闭环的配置最多迭代 $T_{\max}=4$ 次，验证分数达到阈值 $\theta=3$ 时提前停止；FormatTool 负责格式规范化及跨阶段重复项的检查与修复。表 5.1 报告按疫苗类型分层及总体结果，表 6.1 进一步报告不同迭代上限下的指标和平均执行迭代数。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除验证闭环：GPT-4.1 的 CRAFT-Full 对比 CRAFT w/o V | 加入验证与反馈迭代后，总体 EM 从 26.30%升至 35.61%，LCCS 从 42.19%升至 61.46%，$\tau_b$ 从 44.02%升至 57.77%。 | 该对比隔离了“是否使用验证闭环”，表明 GPT-4.1 的单次生成仍会产生大量阶段划分或排序错误，而约束反馈能显著修正它们。不过 CRAFT-Full 同时允许多次重新生成，因此这些增益应解释为整个验证驱动迭代过程的贡献，而不是验证器打分本身的独立因果效果。 | 表 5.1，GPT-4.1 模型块<br><span class="experiment-evidence">GPT-4.1 CRAFT w/o V 26.49 42.94 45.79 27.93 43.51 43.65 24.51 40.06 42.37 26.30 42.19 44.02
GPT-4.1 CRAFT-Full† 34.43 61.68 59.58 40.06 63.84 56.45 32.68 58.93 56.97 35.61 61.46 57.77</span> |
| 生成器消融：GPT-4.1 的完整重生成 CRAFT-Full 对比局部编辑 CRAFT-G | 在相同加性规则验证器下，CRAFT-Full 的总体 EM、LCCS、$\tau_b$ 为 35.61%、61.46%、57.77%，高于 CRAFT-G 的 31.08%、55.69%、53.88%。表 6.1 还显示 CRAFT-G 的 EM 从第 1 次迭代的 34.89%持续降至第 4 次的 31.08%，而 CRAFT-Full 从 26.90%升至 35.61%。 | 该消融隔离的是后续反馈应通过“局部修改旧答案”还是“依据原叙事重新生成完整答案”来执行。结果说明 GPT-4.1 的局部编辑会累积或固化错误，而完整重生成更能利用验证反馈重新组织全局阶段；但这一结论具有模型依赖性，因为其他骨干的迭代轨迹并不完全相同。 | 表 6.1，GPT-4.1 模型块；各指标按第 1 至第 4 次迭代报告<br><span class="experiment-evidence">GPT-4.1 CRAFT-G 2.9407 34.89 32.79 31.78 31.08 60.90 58.16 56.61 55.69 58.33 55.87 54.40 53.88
GPT-4.1 CRAFT-Full† 2.9864 26.90 34.89 35.61 35.61 47.10 60.94 61.45 61.46 45.71 58.19 58.16 57.77</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution is an iterative generator-verifier framework for constrained temporal reasoning with LLMs.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`3b74e358fdade780171954851e166fd65710472ce47361ecfd94e8366f64226f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
