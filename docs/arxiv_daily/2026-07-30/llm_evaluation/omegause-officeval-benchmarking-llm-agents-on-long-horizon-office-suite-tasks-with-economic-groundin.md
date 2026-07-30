---
title: "[论文解读] OmegaUse-OfficeVal: Benchmarking LLM Agents on Long-Horizon Office-Suite Tasks with Economic Grounding"
description: "[arXiv 2607.27155][LLM 评测] OmegaUse-OfficeVal旨在检验大语言模型智能体能否以合理成本完成真实、长流程的办公套件任务，并通过任务级经济信号与代码验证器同时衡量最终交付物的质量和经济价值。"
arxiv_id: "2607.27155"
announcement_date: "2026-07-30"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:24.793711+00:00"
source_sha256: "d4d40157724313ae46ee70e372d8fa1fe19f270f039d36934ed5393605a25e77"
tags:
  - "LLM 评测"
  - "LLM Agent"
  - "LLM 其他"
  - "大语言模型智能体"
  - "办公套件任务"
  - "长周期工作流"
  - "智能体评测"
  - "任务级经济锚定"
  - "代码验证器"
  - "最终交付物"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2607.27155</p>

# OmegaUse-OfficeVal: Benchmarking LLM Agents on Long-Horizon Office-Suite Tasks with Economic Grounding

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Jingbo Zhou, Yusai Zhao, Qi Bao, Jingjia Cao, Zhenghai Chen, Chang Gao, Kaiqi Guo, Muxin Guo, Mingxuan Li, Xinjiang Lu, Yanru Ma, Yixiong Xiao, Zenghui Zhang, Le Zhang, Hua Wu</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27155v1) · [PDF 下载](https://arxiv.org/pdf/2607.27155v1) · **关键词** 大语言模型智能体, 办公套件任务, 长周期工作流, 智能体评测, 任务级经济锚定, 代码验证器, 最终交付物  
**项目页**: [https://omegause-officeval.github.io](https://omegause-officeval.github.io)  

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

OmegaUse-OfficeVal旨在检验大语言模型智能体能否以合理成本完成真实、长流程的办公套件任务，并通过任务级经济信号与代码验证器同时衡量最终交付物的质量和经济价值。

**不用术语来说**：现实中的办公请求往往不是一次点击或填写一个单元格，而是需要综合处理文档、表格、演示文稿和PDF，持续执行多个相互依赖的步骤，最后交付可直接使用的文件。现有测试通常只能说明智能体是否完成了某个短操作或到达预设界面状态，却难以回答企业和用户更关心的问题：智能体做出的成品是否正确、是否需要大量人工返工，以及相对于人工完成同一任务是否真正节省时间和成本。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建并开放OmegaUse-OfficeVal：包含100个源于从业者真实办公请求、经隐私保护改编的长流程任务；每项任务提供高层用户指令、输入文件和明确交付物，并附带人工劳动时间与任务价格代理两类任务级经济信号。
- 建立面向最终交付物的稳定评测机制：把细粒度评分规则转化为代码验证器，同时奖励已满足的要求并惩罚增加用户修复负担的意外破坏，从而避免人工评分和“用大模型充当裁判”带来的成本、波动与可复现性问题。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型智能体评测与办公自动化交叉领域。研究对象不是只回答问题或执行少量界面操作的模型，而是能够接收自然语言委托和办公文件、持续规划并产出文档、表格、演示文稿或 PDF 等可交付成果的智能体。此类任务的关键评价对象是最终成果是否正确、完整且可直接使用；同时，由于智能体的实际价值取决于它替代了多少人工劳动以及推理成本是否合理，评测还需要在单个任务层面关联人工耗时和市场价格。现有生产力评测通常覆盖较宽泛的职业工作，却未必完整开放材料或提供逐任务经济标注；办公与 GUI 基准则多侧重短流程、标准化操作或是否到达预设环境状态，难以回答长周期办公成果的质量与经济价值问题。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**大语言模型智能体（LLM agent）**

以大语言模型为核心、能够规划步骤并调用 GUI、脚本或办公软件等工具完成任务的系统。本文不限定智能体必须采用哪种操作路径，而主要检查其最终交付物。

</div>
<div class="conceptitem" markdown="1">

**长周期办公套件任务（long-horizon office-suite task）**

需要持续执行多个相互依赖的步骤，最终生成文档、电子表格、演示文稿或 PDF 等成果的办公工作。这里的“长周期”以实际人工劳动时间体现，而不只是用点击次数、应用数量或对话轮数衡量。

</div>
<div class="conceptitem" markdown="1">

**任务级经济锚定（task-level economic grounding）**

为每个任务分别记录人工完成时间和任务价格代理值，使模型推理成本能够与被替代的人工成本或市场价值直接比较。它还支持按任务价值加权评价，避免把高价值与低价值任务等同处理。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

OmegaUse-OfficeVal将评测单元定义为真实工作场景改编而来的高层办公请求：每个任务输入一条自然语言用户指令及一个或多个文件，智能体可通过 GUI、脚本或混合方式处理，输出可供用户使用的办公交付物。基准包含100个经隐私保护流程改编的任务，任务面向通常可由初级办公室职员、助理或实习生完成的工作，但刻意保留长周期和复杂性；原文报告其平均人工完成时间为2.32小时。评测不要求复现指定操作轨迹，而是依据细粒度规则对应的代码验证器检查最终成果是否满足要求，并对增加用户修复负担的非预期破坏予以惩罚。每项任务同时附带人工劳动时间与任务价格代理值：前者来自无LLM辅助条件下的人工完成记录，后者优先采用从业者给出的明确价格信号，否则聚合专家估价；因此该设置既能评价成果质量，也能比较人工成本、模型推理成本和任务经济价值。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **GDPVal**: 同样以现实或接近现实的专业工作流评价智能体，并将任务与经济价值联系起来；但据本文所述，GDPVal只公开部分任务或限制参考输出访问，经济锚定也不像OmegaUse-OfficeVal那样完整落实到每个办公任务。
- **OSWorld 2.0**: 它是与本文最接近的长周期计算机使用基准之一，包含108项任务，熟练人工完成任务的中位主动操作时间约为1.6小时；但其核心是GUI操作及预期环境状态，经济覆盖分析主要依赖职业层级映射，而OmegaUse-OfficeVal检查最终办公交付物，并为每项任务提供人工耗时和价格代理值。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

LLM智能体正从自然语言问答和编程辅助走向“vibe working”，即代替用户完成日常办公工作。然而，长流程办公任务包含多文件理解、连续编辑、格式维护和成品检查等环节；中间某一步的错误还可能在后续累积。要判断这类智能体是否具有实际生产力，不能只检查操作是否执行，还必须评估最终文件能否使用，并把推理成本、完成时间和交付价值与人工工作进行可比的量化。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **通用职业与生产力基准**：GDPVal、Remote Labor Index和Agents' Last Exam等基准以广泛、复杂的专业工作流测试智能体，并尝试用职业类别等信息体现任务的经济意义，适合观察模型在跨职业知识工作上的总体能力。
- **办公自动化与GUI智能体基准**：OfficeBench、OdysseyBench、SpreadsheetBench和PPT-Eval等侧重文档操作、电子表格处理、演示文稿编辑或标准化办公技能；GUI基准则通常让智能体在软件界面中执行操作，并依据是否到达预定义环境状态或是否完成规定过程进行评分。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 通用职业基准往往只开放部分任务或限制参考输出访问，而且通常把经济价值绑定到宽泛的职业类别，而非单个任务；因此难以对具体办公请求进行人工成本与模型推理成本的直接比较，也难以开展可靠的价值加权评估。
- 既有办公与GUI基准多聚焦边界明确的短操作、合成流程、标准化技能或界面过程状态，即使部分近期基准覆盖长流程，也主要评估交互过程而非最终成品的质量与可用性；其结果因而不能充分反映交付物是否正确、是否可直接使用以及会给用户带来多少返工负担。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

该领域缺少一个同时满足四项条件的评测载体：任务源于真实职业办公需求、具有足够长的执行链、以最终办公文件而非操作过程为评价对象，并为每个任务提供可与模型成本对照的经济标注。缺少这种联合设计，使“能力得分高”无法自然推导为“能创造更高实际价值”。

</div>
<div markdown="1"><span>核心问题</span>

面对一个由自然语言描述、附带输入文件且需要多步执行的长流程办公套件任务，LLM智能体能否以低于人工的时间和成本，产出正确、可用且具有实际经济价值的最终交付物；其质量与人类基线相比仍存在多大差距？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把评测单位从零散操作提升为完整工作委托：真实高层指令保留了工作场景中的规划难度，最终文件验证直接对应用户真正收到的结果，人工耗时和任务价格代理则把不同任务放入经济尺度。再用细粒度规则编写确定性的代码检查，可以分别识别“完成了哪些要求”和“造成了哪些需要返修的破坏”，使能力、可用性与价值能够在同一框架下比较。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本节方法并非训练智能体，而是为每个办公任务构造可靠的人类劳动时间基准。给定任务 t 和标注员池 \mathcal{A}，系统先随机安排两名标注员独立完成任务，记录包含返工在内的总耗时，并由资深专家进行质量门控；只有最终通过检查的交付物才产生有效时间。若两人的耗时相差超过 30%，则引入第三名标注员补充测量。最终，人类劳动时间 H_t 定义为全部有效耗时中最短两个值的平均数，同时根据初次质量和相对速度给标注员计分，并按日汇总分数发放效率奖金。

这一设计试图同时控制“赶工造成低质量”和“个别人员异常缓慢”两类偏差：返工时间不会被隐去，初次失败者也不能凭最终合格获得效率分；而取两个较快且质量合格的时间求均值，意在估计熟练人员在合理质量约束下完成任务所需的劳动，而非普通人员耗时的总体均值。该时间测量随后可作为基准中的任务级经济信号，但所给章节没有展开任务价格代理、模型推理成本或智能体执行流程的计算方法。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双人随机分配与独立计时

从 \mathcal{A} 中随机选择两名标注员 a_1、a_2，令其分别完成同一任务，并独立记录完成时间 \tau_1、\tau_2。

<div class="method-step__io" markdown="1">

**输入**：办公任务 t 与标注员池 \mathcal{A}  
**输出**：两份候选交付物及其初始完成时间记录

</div>

**直观理解**：相当于让两个人独立做同一道实际工作题，避免仅凭一个人的速度判断任务难度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 专家质量门控与返工计时

资深专家检查交付物是否满足任务要求；若不合格，则要求持续修改直至通过，并把全部修改时间计入 \tau_i。最终通过者的时间被视为有效，但只要发生过返工，其任务分数就设为 0。

<div class="method-step__io" markdown="1">

**输入**：每名标注员提交的交付物及当前累计耗时  
**输出**：质量合格的交付物、有效总耗时、是否返工的状态与初步任务分数

</div>

**直观理解**：完成得快但不合格不能算真正完成；返工所花时间也属于劳动成本，因此不能从计时中删除。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于质量与相对速度的计分

若仅一人返工，则返工者得 0 分、未返工者得 1.5 分；若两人均返工，则均得 0 分。若均未返工且较慢耗时超过较快耗时的 1.3 倍，则快者得 2 分、慢者得 1 分，否则两人均得 1.5 分。

<div class="method-step__io" markdown="1">

**输入**：a_1、a_2 的有效耗时及返工状态  
**输出**：前两名标注员的任务级效率分数，以及是否需要第三次测量的判定

</div>

**直观理解**：分数先奖励一次做对，再区分明显的速度差异；它用于激励和奖金排序，并不直接等同于任务质量分。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 异常差异下的第三人复测

将同一任务交给第三名标注员 a_3，并执行相同质量门控；若其返工则得 0 分，否则当 \tau_3 小于原较短时间的 70% 时得 2 分，大于原较长时间的 1.3 倍时得 1 分，其余情况得 1.5 分。

<div class="method-step__io" markdown="1">

**输入**：满足 \max(\tau_1,\tau_2)>1.3\min(\tau_1,\tau_2) 的两次有效计时  
**输出**：第三个有效完成时间及第三名标注员的任务分数

</div>

**直观理解**：两个人速度差得太大时，很难知道谁更具代表性，因此再找一人复测，降低偶然状态或个人熟练度造成的误判。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 第三人复测触发条件

$$
\max(\tau_1,\tau_2)>1.3\cdot\min(\tau_1,\tau_2)
$$

**符号说明**

- $\tau_1$：第一名标注员完成任务并通过质量门控的总耗时，包含返工时间
- $\tau_2$：第二名标注员完成任务并通过质量门控的总耗时，包含返工时间
- $\max(\tau_1,\tau_2)$：两次有效测量中较慢的耗时
- $\min(\tau_1,\tau_2)$：两次有效测量中较快的耗时
- $1.3$：判定两次耗时存在显著差异的固定倍率阈值

<div class="equation-explanation" markdown="1">

**直观理解**：若较慢者比较快者至少慢 30%，仅靠这两次测量不足以稳定估计任务耗时，因此系统要求第三人独立复测。30% 阈值是该流程预设的规则，所给原文未报告其统计估计过程或敏感性分析。  
**原文位置**：Appendix C，Algorithm 1，Lines 25、30–32

</div>

</div>

<div class="equation-block" markdown="1">

#### 任务级人类劳动时间

$$
H_t=\frac{\tau_{t,(1)}+\tau_{t,(2)}}{2},\quad \tau_{t,(1)}\leq\tau_{t,(2)}\leq\cdots,\;\tau_{t,(j)}\in\mathcal{T}_{\mathrm{valid}}
$$

**符号说明**

- $t$：待测量的人类办公任务
- $\mathcal{T}_{\mathrm{valid}}$：任务 t 的全部质量合格完成时间集合
- $\tau_{t,(1)}$：集合 \mathcal{T}_{\mathrm{valid}} 中最短的有效完成时间
- $\tau_{t,(2)}$：集合 \mathcal{T}_{\mathrm{valid}} 中第二短的有效完成时间
- $H_t$：任务 t 的最终人类劳动时间估计

<div class="equation-explanation" markdown="1">

**直观理解**：该式不对所有参与者耗时求平均，而只平均两个最快且质量合格的记录。这样更接近熟练执行者的合理劳动时间，并减少异常缓慢记录的影响，但也可能低于一般工作人员的典型耗时。  
**原文位置**：Appendix C，Algorithm 1，Lines 44–46；原文以文字规定“average of the two shortest values”，此处按其数学含义形式化

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本节描述的是人类劳动时间的测量、质量控制与激励算法，没有模型参数、损失函数或梯度优化目标；任务分数用于标注员日度奖金排名，而不是用于训练 LLM。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 质量门控与返工机制**

资深专家判断交付物是否满足要求；未通过者必须修改至合格，修改耗时并入总时间，且发生返工者的任务效率分数设为 0。原文明确指出，该阶段无法人工核验文件的每个细节，因此质量判断包含一定程度的专家判断。

> 直观理解：它确保测到的是“完成合格成果所需时间”，而不是“第一次提交文件所需时间”；代价是测量仍可能受到专家主观判断影响。

**2. 相对耗时异常检测与第三人复测**

当两次有效耗时之比超过 1.3 时，方法将其视为显著差异并增加第三次独立测量。第三人的计分同时参考原两次时间的较短值和较长值，以识别特别快、正常或特别慢的完成情况。

> 直观理解：第三次测量类似在两个温度计读数冲突时加入第三个温度计，目的是判断差异来自任务本身还是个人异常。

**3. 质量约束下的效率激励**

任务分数由是否返工及相对完成速度共同决定，并按日聚合；只有质量有效的标注员参与奖金排名，前 25% 和随后 25% 分别获得 1.5 倍和 1.25 倍基础日薪。

> 直观理解：如果没有效率奖励，标注员可能拖延而抬高人类成本；如果只奖励速度，又可能诱发粗糙提交，因此该模块把奖金与质量门槛绑定。

**训练与推理**

不涉及模型训练或模型推理。完整执行过程是：对每个任务随机安排两名标注员，记录包含返工在内的质量合格耗时；根据返工状态与相对速度计分；当两次耗时相差超过 30% 时增加第三名标注员并执行同样的质量流程；最后从全部有效时间中取最短两个值的平均数作为 H_t。标注员任务分数按日汇总并映射为奖金倍率，以在质量约束下鼓励高效完成。

**复现信息**

复现该测量协议所需的关键规则包括：每项任务初始随机分给两人；专家检查失败后必须返工，返工时间计入总耗时；发生返工即记 0 分；双人时间差阈值为 1.3 倍，超过后引入第三人；第三人未返工时，以原较短时间的 0.7 倍和原较长时间的 1.3 倍作为计分边界；H_t 取所有有效记录中最短两次的平均值。奖金按日汇总，仅在质量有效者中排序，前 25% 和第 25%–50% 分别获得 1.5 倍与 1.25 倍基础日薪；专家人数、检查清单、标注员池规模及随机分配实现细节在所给原文中未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- OmegaUse-OfficeVal：包含100个真实办公请求改编任务，以高层用户指令和多模态输入文件为输入，以最终办公文档为评测对象。数据共含220个输入文件和115个目标交付物；输入可包含图像、视频、DOCX、PPTX、XLSX和PDF，输出主要为DOCX、PPTX、XLSX及少量PDF。每个任务同时提供人类劳动时间、任务价格代理和由细粒度评分规则生成的代码验证器。原文未明确报告训练集、验证集和测试集划分；该数据集在实验中整体作为代理能力与经济效率评测集使用。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**Score**

汇总全部任务由代码验证器给出的任务得分，用于衡量最终交付物对指令与细粒度评分规则的总体满足程度；评分还会惩罚非预期修改或对文档造成的可避免损坏。 （越高越好，因为更高得分表示交付物完成了更多要求且引入了更少错误。）

</div>
<div class="metricitem" markdown="1">

**Time-Weighted Score**

以每项任务记录的人类劳动时间作为权重，对任务得分加权求和。它让耗费更多人工时间的任务对总结果产生更大影响，可近似理解为代理覆盖了多少高人工投入工作的完成价值。 （越高越好，因为更高值表示模型在需要更多人类劳动时间的任务上完成得更好；但它不是模型自身运行时间指标。）

</div>
<div class="metricitem" markdown="1">

**Price-Weighted Score**

以任务价格代理作为权重，对任务得分加权求和，用于衡量模型在估计市场价值更高的任务上取得的完成质量。 （越高越好，因为更高值表示模型捕获了更多价格加权的任务价值；该指标依赖价格代理的合理性，并不等同于真实商业收入。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 人类最佳交付物与全部LLM代理的总体质量比较

<div class="result-value" markdown="1">

人类基线的Score为27.79，高于表现最好的LLM GLM-5.2的17.91；即使采用每项任务的较优人类提交，人类得分也远未达到满分。

</div>

作者据此认为，当前模型在长时程办公交付质量上仍明显落后于初级人类工作者。更直白地说，模型虽然能生成文件，但仍容易遗漏需求、破坏原有内容或在多步编辑中累积结构错误。该结果不证明所有人类都稳定优于模型，因为人类基线特意选取了每项任务得分最高的提交，也不代表人类表现接近理想上限。

<div class="result-source" markdown="1">

来源：第5.2节 Main Results；数值汇总见表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">The human achieves a score of 27.79, substantially outperforming all evaluated LLMs, but remains far from perfect.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 平均质量排序与经济价值加权排序比较

<div class="result-value" markdown="1">

GLM-5.2以17.91取得最高LLM平均Score，但Qwen3.7-Plus以34.73的Time-Weighted Score和106.50的Price-Weighted Score取得两项加权指标的LLM最佳结果。

</div>

平均交付质量最好的模型并不一定最擅长高人工投入或高价格任务。Qwen3.7-Plus的结果说明，它虽然平均分略低于GLM-5.2，却在经济权重较大的任务上相对更强。因此，模型选择应取决于目标：若重视一般任务平均质量可偏向GLM-5.2，若更重视高劳动量或高价值任务则Qwen3.7-Plus更有优势。不过，加权得分只反映该基准任务分布及其价格代理，不能直接证明真实部署中的利润更高。

<div class="result-source" markdown="1">

来源：第5.2节 Main Results；具体数值见表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Qwen3.7-Plus obtains the highest time-weighted and price-weighted scores among the evaluated models, suggesting that it performs relatively better on tasks associated with greater human labor time or higher task price.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 质量、单任务成本与运行时间的综合效率比较

<div class="result-value" markdown="1">

Qwen3.7-Plus的平均成本最低，为每任务0.2152美元，平均用时0.193小时，同时取得17.51的Score；DeepSeek-V4-Pro平均用时最短，为0.184小时，但Score仅为14.48。相比之下，人类基线每任务成本为6.8560美元、用时2.324小时、Score为27.79。

</div>

当前LLM已经显示出显著的时间和货币成本优势，但这种效率尚未转化为人类水平的交付质量。Qwen3.7-Plus呈现较均衡的低成本、低时延和质量组合，而DeepSeek-V4-Pro说明“更快”本身不意味着“完成得更好”。这些结果适合用于比较本实验脚手架下的相对取舍，但模型运行时间会受到API延迟、系统负载和框架实现影响，不能被视为稳定的生产环境时延估计。

<div class="result-source" markdown="1">

来源：表3 Overall performance and efficiency on OmegaUse-OfficeVal

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Human | 27.79 | 54.45 | 144.61 | $6.8560 | 2.324
Qwen3.7-Plus | 17.51 | 34.73 | 106.50 | $0.2152 | 0.193
DeepSeek-V4-Pro | 14.48 | 27.14 | 79.33 | $0.6111 | 0.184</span>

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

- 人类基线：每项任务至少由两名人类标注者完成，实验选取其中得分最高的交付物，作为“较优初级工作者”参考。该基线适合衡量当前代理与实际办公交付质量之间的能力差距，但并不代表普通人类的平均水平。
- GLM-5.2、Qwen3.7-Plus与Kimi K2.6：三者构成表现较强的前沿模型比较组，用于检验平均质量最优模型是否也能在劳动时间加权、价格加权和成本效率上保持领先。
- DeepSeek-V4-Pro：作为运行速度突出的模型，用于观察较低延迟是否会自然转化为更高的长时程任务完成质量。
- MiniMax M3：作为另一前沿模型家族的代表，用于扩大跨模型比较范围，并检查不同模型在领域、文件类型和操作意图上的能力差异。

**实验想回答的问题**

- 在统一的程序化办公代理框架下，前沿大语言模型能否完成需要持续规划、跨文件处理和格式保持的长时程办公套件任务，其最终交付物质量与初级人类工作者相比还有多大差距？
- 当任务按人类劳动时间或市场价格代理加权，并同时考虑推理成本与运行时间时，不同模型的质量—经济价值—效率排序是否会发生变化？

**实验实现**

所有模型使用同一套内部代理框架、相同系统提示与任务提示模板。代理接收用户指令和关联输入文件，通过程序化工具、Shell、脚本及文件级API检查、创建或修改办公文件，并按指定格式在当前目录输出最终交付物；当前框架不提供GUI级电脑操作。实验在Ubuntu 24.04.1 LTS、Python 3.10的CPU-only Docker容器中运行，模型推理由远程API完成；容器最多分配108个CPU核等价资源和300 GiB内存，并配备LibreOffice 24.2。每项任务墙钟超时为14400秒，同时运行10个任务环境，每个模型最多有两个并发推理线程。所有产物均由代码验证器评分；模型成本按对应API的token价格计算。人类成本以任务价格代理表示，因此人与模型的成本口径并不完全相同。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces an economically grounded benchmark with code-based verifiers for evaluating LLM agents on long-horizon office workflows.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`d4d40157724313ae46ee70e372d8fa1fe19f270f039d36934ed5393605a25e77`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
