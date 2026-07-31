---
title: "[论文解读] OSReward: Instituting Standardized Evaluation for Cross-Platform Computer-Use Reward Models"
description: "[arXiv 2607.28609][LLM 评测] 本文围绕“视觉语言模型能否可靠且低成本地判断计算机使用智能体是否真正完成任务”这一问题，建立跨平台标准化评测基准，并据此开发针对主要误判模式的开放奖励模型。"
arxiv_id: "2607.28609"
announcement_date: "2026-07-31"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.522705+00:00"
source_sha256: "d11259b072318a2ac5be07724a2f985b1c2316de4abd38afb308b7320fb04de9"
tags:
  - "LLM 评测"
  - "对齐 / RLHF"
  - "LLM Agent"
  - "多模态 VLM"
  - "计算机使用智能体"
  - "视觉语言模型裁判"
  - "轨迹评估"
  - "奖励模型"
  - "跨平台评测"
  - "人工金标准"
  - "OSReward"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2607.28609</p>

# OSReward: Instituting Standardized Evaluation for Cross-Platform Computer-Use Reward Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Sun, Qiushi, Cheng, Kanzhi, Wang, Yian, Yang, Bowen, Yan, Hang, Chen, Liheng, Xu, Fangzhi, Ding, Zichen, Chen, Nuo, Cao, Jialin, Gong, Xingdong, Li, Zehao, Jin, Kaiming, Yuan, Xinfeng, Liu, Zhoumianze, Gong, Jingyang, Yin, Zhangyue, Gao, Jiahui, Wu, Zhiyong, Xie, Tianbao, Zhang, Jianbing, Kao, Ben, Kong, Lingpeng</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The University of Hong Kong；Xi’an Jiaotong University；Nanjing University；University of Science and Technology of China；National University of Singapore；Fudan University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.28609) · [PDF 下载](https://arxiv.org/pdf/2607.28609) · **关键词** 计算机使用智能体, 视觉语言模型裁判, 轨迹评估, 奖励模型, 跨平台评测, 人工金标准, OSReward<br>
**代码**: [https://os-copilot.github.io/OSReward-Home/](https://os-copilot.github.io/OSReward-Home/) · **项目页**: [https://os-copilot.github.io/OSReward-Home/](https://os-copilot.github.io/OSReward-Home/)

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

本文围绕“视觉语言模型能否可靠且低成本地判断计算机使用智能体是否真正完成任务”这一问题，建立跨平台标准化评测基准，并据此开发针对主要误判模式的开放奖励模型。

**不用术语来说**：计算机使用智能体会在网页、手机和桌面软件中执行一连串操作，但它说“任务完成”并不等于界面中的目标真的已经实现。逐条请人检查成本过高，为每项任务编写自动检查程序又只能覆盖少量预设场景，因此研究者开始让视觉语言模型查看操作过程并作出成败判断。问题在于，这类自动裁判本身可能看错；一旦错误判断被用于评测、筛选训练数据或强化学习，系统就可能奖励实际失败的操作。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建OSReward标准化评测体系：以四个平台上的专门采集环境、经验证的任务指令、不同智能体产生的真实成功与失败轨迹以及多阶段人工金标准标签为基础，形成覆盖一般案例的OSReward、聚焦争议与困难案例的OSReward-Hard，以及附带效率和行为对齐细粒度标签的OSReward-Multi，从而把“评测智能体”转化为“评测负责裁判智能体的视觉语言模型”。
- 将评测发现转化为可扩展的开放解决方案：整理带推理标注和失败类型的OS-Shepherd-100K语料，并训练OS-Shepherd-9B与OS-Shepherd-35B；其两阶段训练先学习一般轨迹判断，再定向抑制把失败轨迹判成成功的宽松偏差，以提供可自托管、面向大规模训练的奖励信号。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

计算机使用智能体（CUA）通过读取屏幕等环境状态，并执行点击、输入文本或命令行操作来完成网页、移动端和桌面软件中的用户指令。一次执行过程形成由环境状态、智能体动作和推理交错组成的轨迹；判断轨迹是否真正实现指令目标，是智能体评测、训练数据筛选和强化学习奖励生成的共同基础。传统的任务专用验证器覆盖范围有限，人工标注又难以扩展到大规模轨迹，因此实践中逐渐使用视觉语言模型（VLM）作为自动裁判或奖励模型，但其跨平台、长轨迹条件下的可靠性此前缺少统一且干净的评测依据。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**计算机使用智能体（CUA）**

能够感知数字环境并采取点击、键盘输入或命令行操作等动作，以完成用户任务的智能体。它不仅生成文字回答，还会实际改变网页、应用程序或操作系统的状态。

</div>
<div class="concept-item" markdown="1">

**轨迹（trajectory）**

智能体执行一项任务时产生的完整交互记录，包括连续的环境状态、动作和推理。裁判需要依据这份记录判断最终环境是否满足指令，而不能只相信智能体声称任务已经完成。

</div>
<div class="concept-item" markdown="1">

**视觉语言模型裁判（VLM judge）**

接收任务指令以及含屏幕图像和文本信息的轨迹，并输出成功或失败等评价的多模态模型。作为奖励模型时，其判断可用于筛选训练数据、评价智能体或为强化学习提供奖励信号。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文研究的对象不是执行任务的智能体本身，而是负责评价执行结果的模型裁判。对每个样本，裁判接收一条用户任务指令和相应的跨平台CUA轨迹；轨迹可能来自网页、移动端、Ubuntu或Windows环境，包含最长约100步的状态、动作与推理，并可能涉及纯GUI或GUI与命令行结合的工作流。裁判的核心输出是轨迹成功或失败的二元判定，即环境最终是否真实满足任务要求；细粒度设置还评价执行效率和行为与指令的对齐程度。评测以经过多阶段人工审核的标签为参照，关键假设是人工金标准能够把裁判错误与原始任务歧义、轨迹缺陷及自动验证器错误区分开来。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **基于任务专用验证器的标准化CUA环境（Chen et al., 2025b；Zhou et al., 2024；Kong et al., 2026）**: 这类环境通过为具体任务编写验证规则来提供可复现评测，但验证器只能覆盖有限的预设任务，也无法直接检查已经脱离在线环境的静态轨迹。OSReward转而用人工金标准轨迹评测可泛化的模型裁判。
- **单平台VLM裁判可靠性研究（Lin et al., 2025；Lù et al., 2025）**: 已有工作开始关注模型奖励的可靠性，但主要局限于单一平台，并复用现成指令或轨迹，因而可能混入原智能体配置、不完善验证器和歧义任务造成的噪声。OSReward使用专门采集、跨平台且经人工严格标注的新轨迹，以更直接地测量裁判自身的可靠性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

计算机使用智能体的评测、数据筛选和强化学习都需要判断一条轨迹是否满足任务指令。这里的轨迹是动作、环境状态与模型推理交错组成的长序列，最长可包含很多步；判断者必须核对环境是否真正达到目标，而不能只相信智能体的文字陈述。随着轨迹数量增长到训练规模，人工标注和逐任务编写验证器均难以承担持续、跨平台的判断需求，因此需要一种可以自动处理大量轨迹的可靠奖励信号。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **人工编写的任务验证器与人工标注**：验证器通过预先设定的规则或环境接口检查任务终态，人工标注则由人员阅读轨迹和界面状态后给出成败结论。两者在覆盖范围内可提供较直接的监督，但前者需要针对具体任务开发并依赖仍可访问的运行环境，后者需要持续投入人工审核。
- **以视觉语言模型作为轨迹裁判或奖励模型**：将任务指令以及轨迹中的屏幕状态、动作和文字推理输入视觉语言模型，由模型输出任务成功或失败等判断；这一结果可作为自动评测分数、数据筛选标签或强化学习奖励。该方案不必为每个任务单独编写规则，因而正在成为事实上的常用做法。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 人工验证方案无法扩展到大规模和开放任务：手写验证器只覆盖少量精心设计的任务，并且无法检查已经失去在线环境的静态语料或历史轨迹；人工标注也无法跟上评测、数据整理和训练所需的海量判断。这会使奖励信号成为计算机使用智能体规模化发展的瓶颈。
- 现有视觉语言模型裁判缺少经过人类金标准校准的跨平台可靠性证据，而且存在系统性的宽松偏差：模型容易受智能体“已经完成”的文字叙述影响，将实际未完成的轨迹误判为成功。作者报告，在OSReward-Hard上最佳裁判准确率低于$70\%$、平均裁判约为$52\%$；少数较可靠的商业模型又过于昂贵，而价格可承受的开放模型明显落后，因此现有方案无法同时满足可靠性与训练规模下的成本要求。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前研究已经使用视觉语言模型充当裁判，却没有一个能够隔离裁判自身错误的标准化跨平台基准：直接复用既有智能体基准的轨迹，会把任务设计、环境验证器和轨迹采集本身的缺陷混入结果，使误差无法明确归因于裁判。与此同时，领域也缺少依据这类诊断结果构建、兼顾困难案例表现与运行成本的开放训练数据和奖励模型。

</div>
<div markdown="1"><span>核心问题</span>

在网页、移动端、Ubuntu和Windows等不同平台上，现有视觉语言模型能否依据长程的屏幕、动作与推理记录，可靠地区分真正完成和实际失败的计算机使用轨迹；若不能，主要偏差由什么信息和案例触发，又能否训练出在准确性、去偏能力、稳定性及成本之间更适合大规模使用的开放裁判？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是先建立一把独立、干净的“尺子”，再针对尺子暴露的具体错误训练模型。专门控制的数据采集环境、经验证的指令、多个能力不同的智能体以及多阶段人工金标准，可以减少任务或原验证器缺陷对裁判评测的干扰；困难子集则集中放大模型之间真正有分歧的案例。随后让开放模型学习带有判断理由和失败类型的多样轨迹，并在第二阶段直接惩罚“把未完成任务当成成功”的行为，有望使模型更多依据可观察的环境状态，而不是顺从智能体自述，从而以较低成本获得更严格、稳定的奖励信号。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本节的方法核心不是训练一个判别模型，而是构建一个能够反过来评测视觉语言模型（VLM）裁判是否可靠的跨平台基准。端到端流程为：先在 Web、Windows、Ubuntu 和 Android 四类真实或高度初始化的环境中编写并交叉审查任务指令；再让由 Claude、Gemini、Kimi、Qwen 等不同骨干驱动的计算机使用智能体执行任务，采集包含指令、截图、思考和动作的完整轨迹；随后过滤由网络故障、反自动化拦截或执行冻结造成的无效样本，并通过三人独立标注、分歧升级复核和质量剔除形成可信的成功/失败金标签；最后将同一金标数据组织为覆盖面完整的 OSReward、强调困难判例的 OSReward-Hard，以及评价成功轨迹对齐性与效率的 OSReward-Multi。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建跨平台环境并编写可信任务

研究者为桌面和移动环境安装日常及专业应用，并注入真实文件、应用记录、用户配置与干扰内容；Web 任务运行于实时网站或需要登录的本地镜像站。标注者先探索环境，再编写与当前状态相符且可执行的指令，随后由非作者进行有效性复核，剔除含糊、脱离环境或无法完成的候选。

<div class="method-step__io" markdown="1">

**输入**：Web、Windows、Ubuntu 和 Android 平台，以及其中可用的网站、应用、账号、文件、数据库和用户状态。<br>
**输出**：约 1500 条候选指令中约 800 条通过人工有效性检查和同伴交叉审查，进入轨迹采集阶段。

</div>

**直观理解**：这一步相当于先搭好一台真正有人使用过的电脑或手机，再出一道确实能在这台设备上完成的题，而不是在空白系统中编造任务。交叉审查用于避免后续把“题目本身有问题”误判为智能体失败。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 使用多类智能体采集完整轨迹

每条指令由一至三个执行智能体完成 rollout，记录任务指令以及逐步的界面截图、智能体思考和动作；轨迹覆盖纯 GUI、GUI 加浏览器原语以及 GUI 加命令行等不同动作空间。不同骨干具有不同的动作习惯、推理详略和失败模式，因此多来源采集可降低基准对单一智能体风格的偏置。

<div class="method-step__io" markdown="1">

**输入**：通过人工审查的任务指令，以及由 Claude、Gemini、Kimi、Qwen 四个模型家族中的骨干驱动的执行智能体。<br>
**输出**：来自四个平台、多种智能体骨干和多种动作空间的原始多模态轨迹，其中同时包含真实成功和真实失败案例。

</div>

**直观理解**：如果只让一种智能体答题，裁判可能只需适应该智能体的表达方式；这里让不同风格的智能体执行同一类任务，检验裁判能否依据实际完成情况而非表面风格下结论。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自动过滤非智能体责任的异常运行

自动预过滤器删除持续遭遇反机器人拦截、网络故障或执行冻结等严重采集问题的运行，避免把环境基础设施失效混入任务失败。过滤后的每条轨迹仍保留完整多模态上下文，供人工逐步审阅。

<div class="method-step__io" markdown="1">

**输入**：采集得到的原始轨迹。<br>
**输出**：可归因于智能体行为、适合进行人工成功判定的候选轨迹。

</div>

**直观理解**：若网页断网导致任务没完成，这不能说明智能体能力差；预过滤就像考试前先排除试卷缺页或设备断电的场次，使“失败”尽量只表示智能体没有完成任务。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 三人标注、分歧复核并生成金标签

每条轨迹由三名标注者独立判断成功或失败；三人一致时直接定案，存在分歧时由两名资深复核者共同审阅并通过讨论给出最终结论，而非简单多数投票。成功轨迹额外标注对齐性和效率，失败轨迹则按推理规划、动作、感知和记忆等类别标记一个或多个致错原因；仍有质量问题的轨迹被剔除。

<div class="method-step__io" markdown="1">

**输入**：通过预过滤的完整轨迹，包括每一步截图、思考和动作。<br>
**输出**：带可信二元金标签、成功质量子标签或失败原因标签的轨迹集合。

</div>

**直观理解**：裁判模型的评测上限取决于参考答案是否可靠，因此作者不依赖单人印象。尤其严格的一点是：即使智能体碰巧给出了正确答案，只要它没有通过环境实际获得或验证该答案，轨迹仍被标为失败。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本节描述的是 OSReward 基准的数据构建、人工标注和子集派生过程，没有提出需要通过梯度优化的中心损失函数或训练目标。原文明确说明 OS-Shepherd 奖励模型在独立语料上训练，且该训练语料与本基准完全不重叠；但所给节选未包含第 6 节，因此不能据此还原其训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 真实且统一的跨平台数据基础设施**

Web 使用隔离的 Chromium 会话、实时网站和部分本地镜像站；Windows、Ubuntu 与 Android 环境预装应用并初始化账号、文件、数据库、使用记录及干扰内容。统一基础设施使四个平台输出一致的轨迹格式，并支持视觉动作、浏览器原语和命令行等不同执行方式。

> 直观理解：裁判必须依据环境是否真的发生了目标变化，而不能只看智能体声称“已经完成”。丰富的初始状态和干扰项让成功需要产生可观察的真实结果，也让失败案例更接近日常使用中的复杂情况。

**2. 多骨干轨迹生成与责任归因过滤**

每条有效指令由一至三个、分属四个主流模型家族的执行智能体运行，以覆盖不同思考长度、动作表达和错误模式；采集后自动排除反自动化拦截、网络失败与冻结运行。该模块有意保留由智能体能力造成的失败，同时删除不能公平归因于智能体的基础设施异常。

> 直观理解：多骨干设计防止基准退化成“识别某一种智能体的写作或操作风格”，而异常过滤保证剩余失败具有评测意义。两者共同决定裁判是在判断任务完成事实，而不是猜测模型身份或网络状态。

**3. 分层人工金标与三视图组织**

三名标注者阅读完整轨迹并独立给出二元判定，分歧样本升级为两名资深人员共同复核；成功样本再获得对齐性与效率等级，失败样本获得多标签错误类别。困难集主要由曾产生人工分歧的案例构成，并额外复核，细粒度集则仅覆盖成功轨迹。

> 直观理解：普通多数票可能把真正模棱两可的案例草率定案，资深复核用于提高参考答案可信度。二元结果回答“有没有完成”，细粒度标签回答“完成得是否合意和高效”，错误类别则帮助分析失败发生在哪个环节。

**训练与推理**

基准构建阶段不进行模型训练。数据生产时，执行智能体接收经人工验证的任务指令，在对应平台环境中逐步观察截图并输出思考与动作，系统保存完整轨迹；随后经过异常运行预过滤、三人独立人工判定、分歧样本资深复核以及残余质量剔除，形成金标签。使用该基准评测裁判模型时，原则上应向裁判提供完整轨迹上下文，让其预测任务成功或失败；在 OSReward-Multi 轨道上，还需对成功轨迹预测对齐性和效率等级。不过，具体裁判提示词、输入序列化方式和指标计算协议位于原文第 4.1 节及附录 C.2，未包含在当前节选中，不能进一步补写。

**复现信息**

公平解释该方法所需的关键实现信息包括：四个平台统一采集轨迹；Web 采用隔离浏览器会话并对不同域名控制访问节奏，桌面和移动环境则初始化真实内容及干扰项；Windows 采集在 2K 与 4K 分辨率间切换，部分轨迹最长可达约 100 步；每条指令由一至三个不同骨干智能体执行；每条通过预过滤的轨迹均由三人独立标注，分歧交由两名资深复核者共同裁决。完整 OSReward 含 1019 条轨迹，成功与失败约占 43% 和 57%；OSReward-Hard 含 284 条轨迹，成功/失败约为 30%/70%；OSReward-Multi 包含 440 条成功轨迹，其中对齐性取 0.5 或 1.0，效率取 0、0.5 或 1.0。作者报告整个三人标注、分歧复核及困难集再验证约耗费 800 人时；更细的软件覆盖、动作空间、标注细则和逐阶段样本数位于附录 A、B，当前节选未完整提供。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- OSReward 是主测试集，包含由不同智能体骨干在多个平台执行、并经多阶段人工标注得到真实成功或失败标签的轨迹；成功与失败约占 43% 和 57%。它用于比较不同判定模型在常规、现实轨迹上的总体可靠性。原文节选未给出轨迹总数和具体划分规模。
- OSReward-Hard 是从 OSReward 中集中筛选困难案例形成的挑战集，成功与失败约占 30% 和 70%，尤其包含代理在结束文本中声称成功、但屏幕证据显示任务未完成的欺骗性失败。它用于放大宽松偏差，并检验模型能否真正读取界面、核验任务完成状态。OSReward-Multi 则在相应轨迹上增加对齐度与效率等级，用于测试细粒度质量评分；原文节选未报告两者的具体样本数。
- 外部分布测试由 AndroidWorld、WebArena 和 OSWorld 组成，分别覆盖移动端、网页端和桌面端任务。模型判定与各基准自己的人工编写验证器比较；这些任务和轨迹均未进入 OS-Shepherd 的训练集或 OSReward，因此该组实验主要测试跨数据集、跨平台迁移，而不是在统一人工金标准上的绝对准确率。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（Acc）或外部验证器一致率**

在 OSReward 上表示成功/失败判定与人工金标签一致的比例；在外部基准上只表示与该基准人工编写验证器一致的比例，因为这些验证器本身可能有假阳性和假阴性。 （越高越好，但类别不平衡时必须结合召回率与平衡准确率解读；外部一致率也不能直接等同于真实准确率。）

</div>
<div class="metric-item" markdown="1">

**成功召回率与失败召回率（sRec/fRec）**

$\mathrm{sRec}$ 是真实成功轨迹中被判为成功的比例，过低表示模型过严；$\mathrm{fRec}$ 是真实失败轨迹中被识别为失败的比例，过低表示模型过宽松。二者的差异直接显示错误偏向。 （二者均越高越好，并且越接近越理想；高 $\mathrm{sRec}$ 配合低 $\mathrm{fRec}$ 往往意味着模型几乎接受所有轨迹，而非真正理解任务是否完成。）

</div>
<div class="metric-item" markdown="1">

**平衡准确率（BalAcc）及细粒度 Macro-recall/AUC**

$\mathrm{BalAcc}=(\mathrm{sRec}+\mathrm{fRec})/2$，用于抵消成功与失败比例不均的影响。OSReward-Multi 的宏召回率衡量模型直接输出的对齐度、效率等级是否校准可用，AUC 则不依赖固定阈值，衡量模型能否正确排序不同质量等级。 （均为越高越好。若 AUC 明显高于宏召回率，说明模型已有一定排序能力，但输出等级的阈值或校准仍不可靠。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### OSReward 主测试集上的判定性能上限

<div class="result-value" markdown="1">

闭源前沿模型占据最高档，但没有模型达到文中作为训练时奖励参考线的约 90% 准确率；Claude-Opus-4-8 的准确率为 89.7%，其 $\mathrm{sRec}$、$\mathrm{fRec}$ 和 $\mathrm{BalAcc}$ 分别为 91.1%、88.9% 和 90.0%。GPT-5.5 与 Claude-Opus-4-6 的准确率均为 89.5%，而按平衡准确率排序时领先者会变化，因此实验只支持“存在一个接近上限的模型群”，不支持认定单一模型在所有错误类型上最优。

</div>

常规测试集上的最好模型已接近可用，但仍没有稳定越过作者采用的训练奖励门槛。准确率接近并不意味着行为相同：有的模型更容易放过失败，有的更容易拒绝成功，所以部署时不能只按一列总分选模型。

<div class="result-source" markdown="1">

来源：Table 1；§4.2 The Accuracy Ceiling

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Claude-Opus-4-8 | closed | 89.7 | 91.1 | 88.9 | 90.0 | 69.7 | 69.8 | 69.7 | 69.7

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### OSReward-Hard 上的困难失败判定

<div class="result-value" markdown="1">

所有判定模型相对 OSReward 均下降 20–43 个百分点；最佳模型 Claude-Opus-4-8 的准确率仅为 69.7%，$\mathrm{sRec}$ 与 $\mathrm{fRec}$ 分别为 69.8% 和 69.7%。由于该集合约有 70% 失败样本，始终预测失败也可获得约 70% 原始准确率，因此 69.7% 不能单独证明模型具有强判别能力；其平衡准确率同为 69.7%，才表明模型在两类上确有一定且较均衡的识别能力。

</div>

困难集专门收集“文字看起来已经完成、屏幕上其实没有完成”的轨迹。结果说明接近 90% 的常规集成绩很乐观，真正需要核验屏幕细节时，前沿模型也只能正确处理约七成案例。类别比例还会让简单的恒定预测看起来很强，因此这里必须查看两类召回率。

<div class="result-source" markdown="1">

来源：§4.4 The Collapse；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Even the best judge loses a full twenty points and lands at 69.7%, level with what a constant always-fail judge scores on this 30/70 split; the mean judge falls to 52%, and the lenient tail lower still.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 开放专用奖励模型 OS-Shepherd 与通用开放模型的比较

<div class="result-value" markdown="1">

OS-Shepherd-9B 在 OSReward 上达到 86.1% 准确率，$\mathrm{sRec}=86.6\%$、$\mathrm{fRec}=86.0\%$、$\mathrm{BalAcc}=86.3\%$；在 OSReward-Hard 上为 60.2% 准确率和 61.9% 平衡准确率。它的总体准确率与 GPT-5-mini 相同，并明显比许多通用小型开放模型更均衡。35B-A3B 版本在困难集达到 62.7% 准确率和 64.3% 平衡准确率，但在普通集准确率为 85.6%，说明扩大模型并未在所有设置中单调提高总准确率。

</div>

专门用轨迹判定数据训练后，小型开放模型可以接近部分商业模型，并避免通用开放模型常见的“几乎都判成功”行为。该结果支持训练配方能够改变模型的判定工作点，但不能证明 OS-Shepherd 已达到最强闭源模型的绝对可靠性，也不能仅凭两个模型尺寸得出完整的规模规律。

<div class="result-source" markdown="1">

来源：Table 1；§4.2、§4.4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

OS-Shepherd-9B (ours) | open weights + data | 86.1 | 86.6 | 86.0 | 86.3 | 60.2 | 66.3 | 57.6 | 61.9

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 外部泛化实验以 AndroidWorld、WebArena 和 OSWorld 的人工编写验证器为参照，而这些验证器本身可能存在假阳性和假阴性；因此实验只能证明与现有验证器的一致程度及相对迁移趋势，不能给出模型在外部基准上的无偏真实准确率。
- 所给节选说明会逐项扰动帧数、点击标记等设置，但未提供相应消融结果，也没有给出各数据集的确切规模、置信区间或显著性检验。因而无法从当前材料判断性能差异的统计稳定性，或准确归因于某个输入组件、解码设置或训练阶段。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 闭源前沿判定模型，包括 Claude-Opus-4-8、GPT-5.5、Claude-Opus-4-6 和 Gemini 系列。它们代表当前性能上界，用于判断 OS-Shepherd 与商业级判定能力之间的差距。
- 大型开放权重通用模型，包括 Kimi-K2.5、Qwen3.5-397B-A17B 和 Intern 系列。它们是判断“专门训练是否优于单纯扩大通用模型规模”的关键对照。
- 小型开放视觉语言模型及 OS-Shepherd 的未调优 Qwen3.5-9B 基座。前者刻画低成本通用模型的能力下界，后者用于区分 OS-Shepherd 的抗宽松偏差究竟来自训练还是模型规模。
- 恒定输出基线，包括始终预测失败或始终预测成功。它们揭示类别不平衡对原始准确率的误导：例如失败占多数时，始终预测失败也可能得到看似较高的准确率，却没有实际判别能力。

**实验想回答的问题**

- 现有视觉语言模型能否在统一协议下可靠判断计算机使用智能体轨迹是否完成任务，并达到可用于训练时奖励的准确性、类别平衡性与跨平台稳定性？
- 针对轨迹判定训练的开放模型 OS-Shepherd，能否缓解通用模型过度接受失败轨迹的宽松偏差，并将这种能力迁移到独立构建的移动端、网页端和桌面端基准？

**实验实现**

所有判定模型采用共同协议：输入轨迹最后 $N=5$ 个状态，以及每一步的推理和动作文本；模型不使用任务专属验证程序、外部工具或逐步监督，最终输出 success/fail。对 OSReward-Multi 还输出对齐度与效率等级。默认帧数、红色点击标记和贪心解码保持一致，以减少提示和推理配置差异造成的混淆。主实验共比较 27 个视觉语言模型，覆盖闭源前沿、闭源高效档、大型开放权重和小型开放视觉语言模型，部分模型另测思考版本；更细配置位于原文附录 §C.1–C.2，但节选未提供。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 代表性失败案例是“假成功”：智能体在最后的文字叙述中宣称任务完成，但截图显示目标状态并未达到。多数判定模型更依赖智能体自己的叙述而非视觉状态，因此会过度接受这类轨迹。该现象把改进方向具体化为：检查最终界面中的可验证完成证据，而不是把措辞自信的结束文本当作成功证明。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces a benchmark for evaluating VLM-based judges of computer-use agent trajectories and trains reward models that provide scalable feedback for agent evaluation and reinforcement learning.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`d11259b072318a2ac5be07724a2f985b1c2316de4abd38afb308b7320fb04de9`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
