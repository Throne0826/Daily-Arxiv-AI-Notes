---
title: "[论文解读] GPT-Red: Automated Red Teaming via Self-Play at Scale"
description: "[arXiv 2607.26115][LLM 安全] 本文提出GPT-Red：通过大规模自博弈、代理式交互搜索和多样化安全环境训练自动红队模型，使其持续发现针对前沿大语言模型的新型提示注入攻击，并为防御模型的对抗训练提供更强数据。"
arxiv_id: "2607.26115"
announcement_date: "2026-07-30"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.895544+00:00"
source_sha256: "11ce03c2593bea4c70903b7a3335a88caea47b58bcc3d436c391892e3df95532"
tags:
  - "LLM 安全"
  - "Multi-Agent"
  - "强化学习"
  - "大语言模型安全"
  - "自动化红队"
  - "提示注入"
  - "内容政策越狱"
  - "指令层级"
  - "对抗训练"
  - "对抗鲁棒性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2607.26115</p>

# GPT-Red: Automated Red Teaming via Self-Play at Scale

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Eric Wallace, Christopher A. Choquette-Choo, Nikhil Kandpal, Sam Toyer, Dylan Hunn, Stephanie Lin, Yuxin Wen, Xiangyu Qi, Christopher Wolff, Zizhao Wang, Milad Nasr, Sicheng Zhu, Chuan Guo, Juan Felipe Cerón Uribe, Kaiwen Wang, Aiden Low, Kai Xiao, Kai Chen</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26115v1) · [PDF 下载](https://arxiv.org/pdf/2607.26115v1) · **关键词** 大语言模型安全, 自动化红队, 提示注入, 内容政策越狱, 指令层级, 对抗训练, 强化学习, 对抗鲁棒性<br>


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

本文提出GPT-Red：通过大规模自博弈、代理式交互搜索和多样化安全环境训练自动红队模型，使其持续发现针对前沿大语言模型的新型提示注入攻击，并为防御模型的对抗训练提供更强数据。

**不用术语来说**：当大语言模型能够浏览网页、读取文件或调用工具时，外部内容可能夹带恶意指令，诱使模型偏离用户任务，甚至泄露数据或执行危险操作。要提前发现并修补这些漏洞，需要大量能够随模型升级而变化的攻击样本；但人工测试速度有限，固定攻击集又容易被模型记住，因此难以长期检验真实的安全性。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出可扩展的攻击者—防御者自博弈训练框架：攻击者因诱发有效失败而获得奖励，防御者因抵抗攻击并完成原任务而获得奖励；随着双方共同增强，系统能够自动产生逐步变难的攻击与防御训练信号。
- 将红队能力沿三个维度联合扩展：用带状态的defender_model工具支持测试时反复试探，用多种真实任务构造提示注入环境，并以大规模强化学习让攻击者面对一组同时训练的强防御者，从而减少对单一模型特性的依赖。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型安全与对抗鲁棒性研究，核心问题是：模型在面对恶意输入时，能否仍按系统或开发者设定的规则行动。论文聚焦两类风险：一是提示注入，即低权限或不可信内容试图覆盖高权限指令；二是内容政策越狱，即攻击者通过改写、角色扮演或间接表达，诱使模型回答本应拒绝或安全处理的有害请求。为发现这些风险，红队测试让攻击者主动寻找模型弱点；自动化红队则用模型生成攻击，以降低人工测试成本并扩大攻击场景与尝试次数。本文进一步将自动攻击生成与对抗训练连接起来：红队模型产生困难样本，防御模型再通过强化学习学习保持安全和正确行为。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**提示注入（Prompt Injection）**

攻击者提供与可信指令冲突的文本，试图让模型忽略系统或开发者意图。直接注入来自用户消息；间接注入则藏在网页、检索文档或工具输出等第三方内容中。

</div>
<div class="concept-item" markdown="1">

**指令层级（Instruction Hierarchy, IH）**

模型输入被划分为系统、开发者、用户和工具响应等不同权限级别；发生冲突时，模型应优先遵循更高权限指令。该机制是同时防御直接与间接提示注入的基本行为规范。

</div>
<div class="concept-item" markdown="1">

**自动化红队与对抗训练**

自动化红队使用模型或优化算法批量生成能够暴露目标模型缺陷的攻击。对抗训练再把这些困难攻击作为训练任务，通过监督微调或强化学习增强防御模型的稳健性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究设定包含攻击者与防御者两类代理。攻击者接收现实化的红队环境与攻击目标，生成提示注入或内容政策越狱攻击；防御者是通用大语言模型，需要在恶意输入下仍遵守指令层级、维持预期任务行为，或对有害请求作出拒绝和安全回应。本文讨论直接聊天式提示注入与经工具输出、检索文档或网页进入代理上下文的间接提示注入，并覆盖自残、非法建议以及生物、化学和网络风险等越狱主题。基本假设是攻击可通过与目标模型交互来检验，而自动红队生成的高难度任务能够用于后续强化学习式对抗训练；本节未给出形式化输入空间、输出空间或成功判据。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Zou et al. (2023) 等基于离散优化的自动攻击方法**: 这类方法通过优化对抗后缀攻击目标模型，但通常需要白盒访问、大量防御者查询，并且较难迁移到新模型或新场景。作者将其视为与本文基于大语言模型的自动红队方法不同但互补的路线。
- **Ma et al. (2023)；Liu et al. (2025)；Deng et al. (2025)**: 作者认为这些工作与本文最接近，但前两者使用的目标和环境规模较小，本文试图通过更广泛的环境与更多对抗目标显著扩展训练；Deng et al. (2025) 只研究防御分类器，而本文面向通用大语言模型。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

面向代理式应用部署的大语言模型会接触不可信网页、工具返回值和本地文件等内容，攻击者可借此实施间接提示注入，操纵模型行为。随着模型能力、工具权限和应用领域扩大，可被攻击的入口也随之增加；生产系统因而需要一种能够持续发现新攻击、评估当前防线并生成高质量对抗训练数据的自动化机制。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于既有攻击数据的强化学习对抗训练**：收集人类红队员、经过提示的通用大模型或生产环境真实事件产生的恶意输入，再奖励防御模型拒绝这些输入并维持原任务行为，以提升其对已知攻击模式的抵抗力。
- **单次生成或提示驱动的自动红队**：让通用大模型根据攻击目标直接生成候选恶意提示；更强的版本可把模型放入交互式工具框架，使其查询目标防御者并多轮修改攻击，但模型本身未必经过专门训练以有效利用这种交互过程。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有对抗数据集规模和攻击形态有限，防御模型可能很快拟合其中的固定模式，却仍会被能够观察防御行为并调整策略的自适应攻击者突破；模型能力和使用场景扩大后，这种覆盖不足会更加严重。
- 人工红队难以按生产模型迭代速度持续扩充攻击，而普通提示式模型或只针对单一防御者训练的攻击器，可能无法充分利用多轮试探，也容易依赖特定目标模型的偶然弱点，因而难以迁移到未见模型、环境和攻击框架。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种可按训练计算量扩展的专用红队智能体：它既能通过反复交互学习如何搜索攻击，又能覆盖多种现实任务和攻击面，并在多个强防御者上训练以发现可迁移的新漏洞；同时，其生成的攻击还应足够有效，可直接用于后续生产模型的鲁棒性训练。

</div>
<div markdown="1"><span>核心问题</span>

能否通过攻击者与一组持续增强的防御者进行大规模自博弈，并联合扩展测试时搜索、训练环境多样性和强化学习计算量，训练出一个在未见攻击目标、环境、交互框架及目标模型上仍能发现有效提示注入的自动红队智能体？

</div>
<div markdown="1"><span>作者直觉</span>

固定题库式防御只能教模型应对已经见过的招数，而自博弈会让攻防双方互相抬高难度：防御者堵住旧漏洞后，攻击者必须借助多轮查询寻找新路径；攻击者变强后，又会暴露更隐蔽的失败供防御者学习。让攻击者同时面对多种任务和多个防御者，相当于要求它学习可复用的攻击原则，而不是背诵某个模型的单一漏洞，由此可能形成持续改进的安全训练循环。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

GPT-Red 是一个以大语言模型为核心的智能体式红队攻击器，目标是在给定安全场景中自动搜索能够使防御模型违反高优先级指令或安全策略的输入。其端到端流程是：从真实能力任务改造出攻击环境，指定攻击可插入的位置和恶意目标；攻击器通过终端构造攻击，并借助 defender_model 工具反复查询防御模型、观察轨迹与评判反馈、逐步修改候选攻击；只保留最终攻击，将其插入预定位置后重新运行防御模型；环境验证攻击是否合法并分别计算攻击者与防御者奖励，最后用强化学习同时更新攻击器和多个防御器。GPT-Red 以 GPT-5.5 权重初始化，并在直接提示注入、间接提示注入、多模态攻击及内容策略越狱等多类环境上训练，同时混入常规强化学习后训练任务以维持通用能力。

直观地说，这不是让模型一次性“猜”一个恶意提示，而是给它一个可反复试验的沙盒：先写攻击，观察目标模型如何反应，再像调试程序一样局部修改。训练中，防御模型也持续学习抵抗当前攻击，因此攻击器必须不断寻找更强或更有针对性的策略；同时面对多个弱点不同的防御器，可降低攻击策略退化为单一模板的风险。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造并采样红队强化学习环境

系统采样对话、文件状态和一个防御模型，选择与上下文匹配的攻击插入点，通常是工具调用结果中的指定区域，并设定可验证的攻击目标；同时向攻击器提供完成该任务所必需的对抗信息，例如最终用户消息。多数环境由现有能力任务改造而来，即在防御器正常执行任务时暂停其轨迹，并开放一小段工具响应、文件内容或低优先级消息供攻击器编辑。

<div class="method-step__io" markdown="1">

**输入**：一个能力任务对应的对话、初始虚拟文件系统、防御模型，以及可被攻击者控制的消息或工具返回区域。<br>
**输出**：一个包含正常任务、高优先级约束、攻击位置、攻击目标和目标防御模型的可执行红队实例。

</div>

**直观理解**：系统先搭好一个“正常工作被恶意内容插入”的现场，并明确攻击者可以改哪里、希望诱导模型做什么。这样攻击发生在邮件、网页、文件或工具调用等实际任务上下文中，而不是脱离场景地生成一句越狱口令。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 通过 defender_model 工具进行顺序式攻击搜索

攻击器在虚拟文件系统中创建候选攻击文件，并把文件路径提交给 defender_model；系统将文件内容放入预定攻击位置，采样防御器轨迹，再返回该轨迹、token 对数似然及评判模型反馈。攻击器可在同一上下文内依据反馈编辑文件、运行代码生成模板化或组合式攻击，并继续查询，也可在支持的环境中构造有状态的多轮攻击。

<div class="method-step__io" markdown="1">

**输入**：红队实例、攻击目标、可用的终端工具，以及对当前防御模型的查询接口。<br>
**输出**：经过多次交互式测试和修改后选定的最终攻击消息或消息序列。

</div>

**直观理解**：这类似程序员根据测试结果不断调试同一份代码，而不是彼此独立地随机写很多版本。前一次失败透露了防御器如何理解输入，攻击器便能有方向地修改措辞、结构或伪装方式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 验证攻击并执行正式防御轨迹

系统先检查攻击与环境是否合法；若攻击无效，则攻击者奖励置为 0。合法攻击被插入预定位置，防御器从该攻击点恢复执行，而搜索阶段产生的所有中间 defender_model 调用均被丢弃，不作为正式攻击轨迹。

<div class="method-step__io" markdown="1">

**输入**：攻击器提交的最终攻击、原始环境状态、预定插入位置和防御器尚未完成的正常任务。<br>
**输出**：一条用于判定攻击成败、任务完成情况并进行强化学习的正式防御器 rollout。

</div>

**直观理解**：练习时可以反复试错，但最终计分只看攻击器选出的那一次正式提交。合法性检查防止攻击器靠破坏环境格式或利用无意义的评测漏洞获得奖励。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算非对称奖励并进行多防御器自博弈更新

环境分别检查攻击器是否诱发了有效失败，以及防御器是否抵抗攻击并完成原始任务，据此产生通常不对称的双方奖励；随后使用各自的 rollout-reward 对通过强化学习更新攻击器和防御器。训练迭代持续重复上述过程，使改进后的防御器提供更困难的攻击目标，同时从多个防御器采样对手以鼓励针对不同弱点的策略。

<div class="method-step__io" markdown="1">

**输入**：攻击器 rollout、正式防御器 rollout、环境专用成功判据，以及由多个不同防御模型构成的训练群体。<br>
**输出**：不断增强且策略更具多样性的 GPT-Red，以及对提示注入更稳健的防御模型检查点。

</div>

**直观理解**：双方并非简单共享一个正负相反的分数：攻击者要真正造成指定失败，防御者还要在不受骗的同时把原任务做好。多个对手相当于让攻击者面对不同风格的守门员，迫使它先判断对手弱点，而不是永远重复同一招。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文节选没有给出统一的显式损失函数或带编号的数学目标，因此不应补造公式。其优化目标以环境奖励实现：攻击器因诱发经验证的有效失败而获得奖励，无效攻击的奖励为 0；防御器因抵抗攻击并完成原始能力任务而获得奖励。二者的奖励通常是非对称的，因为“攻击未成功”不自动等于“防御任务完成”，防御器若通过过度拒绝来避开攻击，仍可能无法得到任务完成奖励。每轮收集双方的 rollout 与相应奖励后，用强化学习分别更新攻击器和防御器；随着防御器修补当前策略，攻击器必须探索新的攻击，从而形成动态课程。训练 GPT-Red 时还混入标准强化学习后训练环境，以减少专攻红队任务导致的指令遵循、Codex 交互能力和诚实性退化。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 智能体式攻击 harness 与 defender_model 查询接口**

攻击器拥有通用终端和 defender_model 两类工具：前者用于创建、编辑和执行生成攻击所需的文件或代码，后者读取指定文件，将攻击嵌入环境并返回防御器轨迹、token 对数似然和评判反馈。该接口支持在单次攻击器 rollout 内顺序查询与局部修改，因此不同于把相同预算用于相互独立候选的 best-of-N 采样；某些场景还支持保持防御器会话状态的多轮攻击。

> 直观理解：该模块把攻击生成从“一次作答”变成“观察—修改—再测试”的搜索过程，并让模型能用代码批量填充模板、重复字符串或组合策略。其核心价值不是单纯增加样本数，而是让后续尝试利用前面尝试获得的信息。

**2. 多防御器同步自博弈**

攻击器和一组多样化防御 LLM 均由强链式思维推理模型初始化，并在每轮中同时接受强化学习更新。论文指出，单一防御器训练容易使攻击器模式坍塌到少数策略；引入多个对不同攻击类型具有不同鲁棒性的防御器，会促使攻击器根据对手反馈探测特定弱点，而非只学习一种普遍模板。

> 直观理解：如果训练中永远只有一个对手，攻击者可能只记住对付它的一套固定招数。让它轮流面对多个防御者，就更像综合训练：必须先辨认对手特点，再选择或创造合适的攻击。

**3. 由能力任务改造的多类别红队环境**

训练环境覆盖直接与间接提示注入、多模态场景和内容策略越狱；主要构造原则是复用已有能力任务，在防御器执行工具调用或处理外部内容时，开放指定消息、工具响应或文件区域给攻击器编辑。这样可以继承原任务的真实上下文、工具链和完成标准，并通过环境专用验证器分别判断攻击目标是否实现及合法任务是否完成。

> 直观理解：系统不是凭空设计大量人工谜题，而是把模型原本需要完成的邮件、搜索、函数调用或软件任务改造成带恶意内容的版本。因而防御者必须同时做到“不听攻击者的假指令”和“继续完成用户真正交代的工作”。

**训练与推理**

训练阶段首先用 GPT-5.5 初始化 GPT-Red，并用强推理模型初始化自博弈参与者；训练覆盖第 6 节所述全部红队环境，对手包括多个历史防御模型，最高包含 GPT-5.5。每次迭代依次完成环境采样、攻击位置与目标设定、攻击器交互式搜索、最终攻击合法性验证、攻击插入与防御器续跑、环境专用奖励计算，以及基于 rollout-reward 对的双方强化学习更新。攻击器搜索过程中的中间防御查询仅用于改进最终候选，正式训练样本采用最终提交后的防御轨迹。论文还将常规 RL 后训练环境混入训练，以保持非安全专项能力；训练计算量被描述为与近期生产 GPT-5 系列模型的 RL 后训练大致相当，但节选未明确报告优化器、学习率、批大小、查询上限或具体更新算法。

推理或评测阶段不再更新 GPT-Red，而是为其提供目标系统描述、可控制的攻击位置、终端和 defender_model 工具。模型在查询或 token 预算内顺序提出、测试并修改攻击，满意或耗尽时间后提交最终文件路径；评测系统将其内容插入目标轨迹，并以环境判据计算攻击成功率等结果。对真实智能体系统，可先在模拟环境中迭代，再把选定攻击提交到生产系统；对防御训练，则可持续用 GPT-Red 生成对抗提示并加入目标模型的 RL 数据。需要区分两种扩展：推理扩展增加单次任务中的顺序查询与思考计算，训练扩展则通过自博弈让攻击器学会更有效地利用这些查询。

**复现信息**

公平理解和复现该方法所需的关键设置包括：第一，攻击位置由环境预先指定，攻击器只能编辑开放区域，不能任意篡改系统状态；否则攻击成功率不能代表提示注入能力。第二，攻击搜索采用文件路径提交协议，defender_model 在后台嵌入文件内容并返回完整反馈；评测 best-of-N 时应在相同防御器调用预算下比较独立采样与顺序式搜索。第三，正式计分只使用最终攻击，中间查询轨迹被丢弃；ASR 的具体定义在相关推理扩展实验中是“至少一次攻击成功的评测实例比例”。第四，自博弈需要多样化防御器群体，并同时检查攻击成功与正常任务完成，以避免单一对手导致策略模式坍塌，也避免防御器靠一概拒绝取得表面安全。

环境方面，应保留直接提示注入、间接提示注入、多模态和内容策略场景的不同交互结构及其专用验证器；部分环境允许有状态多轮攻击，不能与单轮环境混为一谈。GPT-Red 使用 GPT-5.5 初始化，并与标准 RL 后训练环境混合训练，但原文节选未明确报告模型架构改动、各数据类别配比、训练步数、强化学习算法、采样温度、每个 rollout 的最大查询次数、奖励尺度或评判模型配置。因此，仅凭所给章节可以复现算法框架和评测协议，不能精确复现训练运行。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 2025 Q4 Indirect Prompt Injection（IPI）Challenge场景：包含多种对抗目标与环境，且与GPT-Red的训练环境不同；论文使用内部镜像开展自动化红队评测，并允许GPT-Red访问defender_model工具和完整智能体工具。其作用是测试对未见场景、对抗目标和工具框架的迁移能力。原文未明确报告场景数量、样本规模及精确划分。
- IPI 2025 Challenge人类攻击数据集：由基于函数调用的人类提示注入攻击组成，用于比较GPT-Red与人类红队攻击，并检验GPT-5.6对真实人类攻击的防御能力。原文未明确报告数据规模；对GPT-5.6的复测属于完全留出的人类攻击评估。
- IH-Challenge指令层级数据集：用于受控自博弈实验，初始攻击者为内部helpful-only模型，防御者为较小的GPT-5系列模型。实验跟踪攻击成功率和留出防御鲁棒性，用来研究训练动态、攻击者是否遗忘旧能力，以及可训练攻击者相对冻结攻击者的作用。原文未明确报告任务数和数据划分规模。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**攻击成功率（Attack Success Rate, ASR）**

成功诱导防御模型违反原任务或提示注入约束的攻击尝试占比；在训练动态中，它反映当前攻击者相对当前或历史防御者的有效性。 （评价攻击者时越高越好，因为表示更多尝试成功；评价防御者时越低越好，因为表示更少攻击能够突破。）

</div>
<div class="metric-item" markdown="1">

**防御成功率／提示注入鲁棒性**

防御者抵抗注入并继续完成原始任务的比例；论文对若干留出攻击、数据集和领域报告平均防御成功率。 （越高越好，因为模型既需忽略恶意指令，也需维持原任务执行。该指标可能受标签噪声、任务歧义和奖励噪声影响。）

</div>
<div class="metric-item" markdown="1">

**过度拒绝（overrefusal）倾向**

模型面对本应允许的请求时是否因安全训练而不必要地拒绝，用于检查鲁棒性提升是否以通用可用性下降为代价。 （越低越好，但所给节选未提供其具体计算方式或数值，因此无法判断GPT-5.6在该指标上的变化幅度。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### GPT-Red与人类红队员及GPT-5.5在2025 Q4 IPI Challenge未见场景上的比较

<div class="result-value" markdown="1">

作者报告：单次生成攻击时GPT-5.5约与人类红队员相当；加入可查询防御者的工具框架后攻击更有效；直接针对该框架训练的GPT-Red成功覆盖的场景明显更多，并且增加测试时计算后仍继续改善。

</div>

这说明GPT-Red的优势不仅是底座模型会写攻击，还来自其学习了如何在交互式工具中试探目标、根据反馈修改策略。由于节选没有给出Figure 1的坐标值、样本数或统计区间，无法量化其相对提升，也不能由此证明它在所有真实系统上都优于专业人类。

<div class="result-source" markdown="1">

来源：Figure 1及Introduction

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

When prompted to generate a single attack, GPT-5.5 roughly matches human red-teamers, while placing it in a harness with query access to the defender enables even more effective attacks.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GPT-5.6在留出的强攻击、数据集和领域上的提示注入鲁棒性

<div class="result-value" markdown="1">

面对专门构造的强留出集合，GPT-5.6的平均防御成功率超过50%，部分评测最高达到89%；作者称它在所有所列鲁棒性评测中均优于先前OpenAI模型。

</div>

该结果测试对未用于训练的攻击强度、任务分布和完整领域的泛化，而非只记住训练攻击模板。超过50%到最高89%的跨度表明不同评测难度差异很大；节选没有逐数据集成绩、误差范围和通用能力对照数值，因此不能断言所有分布外场景都已得到可靠解决。

<div class="result-source" markdown="1">

来源：Section 8.2, Robustness Evaluation（文中指向Section 7.2的结果图）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Despite these attacks representing a very strong hold-out set, robustness climbs to greater than 50% and reaches as high at 89%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### GPT-5.6抵抗自动GPT-Red攻击与IPI 2025人类攻击

<div class="result-value" markdown="1">

在不使用系统级缓解、因而对攻击者更有利的自动IPI红队协议中，GPT-5.6的ASR低于4%；在人类IPI 2025 Challenge攻击复测上，作者报告100%鲁棒性。

</div>

两项结果分别检验自适应自动攻击和固定人类攻击：前者表明GPT-Red仍能找到少量突破，但成功率已较低；后者表明该特定人类攻击集合未能复现突破。100%仅针对有限数据集和当前复测协议，不等于不存在未知提示注入；原文也提醒标签噪声、歧义、奖励噪声及缺少系统级缓解会影响指标解释。

<div class="result-source" markdown="1">

来源：Section 8.2, Held-out red-teaming exercise

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We see clear monotonic gains in robustness over time, with ASR below 4% for GPT-5.6.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 证据披露不完整：所给节选缺少Figure 1、5、6及Section 7.2的完整数值、样本量、误差条和统计检验；攻击者单独训练对照明确标为not shown。因此“远多于人类”“最佳最终鲁棒性”等主要是作者的定性主张，尚不能独立核算效应大小或计算效率。
- 外部有效性有限：多数训练和评测依赖内部模型、内部红队环境及IPI内部镜像；自动评测还刻意不使用系统级缓解，作者承认这会抬高ASR。与此同时，人类攻击集上的100%鲁棒性只覆盖一个有限的既有数据集，不能证明对未知自适应攻击、不同供应商模型或真实部署链路具有普遍安全性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- GPT-5.5单次攻击生成：不给模型交互式查询防御者的机会，用于区分通用模型一次性写攻击的能力与GPT-Red经专门训练后的智能体红队能力。
- 带defender_model工具的冻结提示LLM：可反复查询目标防御者并迭代攻击，但自身参数不训练；它控制了测试时交互和额外推理计算，从而判断收益是否只是来自工具框架。
- 不带defender_model工具的冻结提示LLM：以固定模型一次性或非交互地产生攻击，作为传统自动攻击数据生成方式，并与可交互及自博弈攻击者比较。
- 人类红队员：来自IPI Challenge的人类攻击，为实际人工发现攻击的参照；该比较检验GPT-Red能否扩大成功攻击的覆盖范围，但不直接比较人工成本、专家资历或攻击质量。

**实验想回答的问题**

- GPT-Red是否能比未专门训练的模型和人类红队员更有效地发现提示注入攻击，并将能力迁移到训练中未见的环境、目标模型与红队工具框架？
- 将自博弈攻击者生成的攻击用于防御者训练，是否能持续提升GPT系列模型对分布内、分布外及人类提示注入攻击的鲁棒性；这种提升是否来自可训练攻击者、多防御者种群等关键设计？

**实验实现**

自动红队评测中，GPT-Red可通过有状态的defender_model工具多轮查询选定防御者、观察结果并迭代攻击；IPI内部镜像评测还开放完整智能体工具。对GPT-5.3及后续模型按攻击尝试数计算ASR，且不启用系统级缓解措施，因此作者明确指出该协议会高估现实攻击成功率。鲁棒性训练方面，GPT-5.6在能力与安全任务的RL训练中加入GPT-Red生成的提示注入样本。强IID攻击按其对防御模型多次试验的平均成功率排序，较弱的下半部分用于训练，较强的上半部分用于评测；每个高级领域另留出一个数据集，并整体留出智能体编程领域。各模型以大致相当于high reasoning的配置评测。所给节选未明确报告采样次数、置信区间、显著性检验、解码参数、训练算力数值及完整分项成绩。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 攻击者类型消融：冻结提示LLM、带defender_model查询工具的冻结提示LLM、自博弈训练攻击者 | 在相同目标——提升留出直接提示注入鲁棒性——下，自博弈训练攻击者使防御者提升最快且最终鲁棒性最好；仅给冻结攻击者增加目标查询能力虽更强，但仍不及训练攻击者。原文未明确报告各组数值。 | 该对照隔离了两个因素：交互式查询提供的测试时计算，以及攻击者参数通过自博弈更新所带来的学习。结论表明工具访问本身不足以解释全部收益；训练后的攻击者能持续产生更适合当前防御者的困难样本。不过没有数值、方差和算力匹配信息，无法判断单位计算成本下的优势。 | Figure 5及Self-play training is healthy and stable<br><span class="experiment-evidence">Trained attackers lead to defenders with the fastest improving and best final robustness, demonstrating the efficacy of self-play.</span> |
| 自博弈与攻击者单独训练的对照 | 作者称，攻击者单独训练时对其训练所针对的防御者更强，但在留出防御者上更差，也更容易出现攻击策略模式坍塌；完整结果未展示，且原文未明确报告数值。 | 该对照考察联合演化是否比固定对手上的单方优化更能保持迁移性与策略多样性。结果支持自博弈的价值在于不断改变对手和学习信号，而非仅提高某一固定目标上的ASR；但由于实验标为not shown，证据强度低于有图示的主要实验。 | Self-play leads to better attackers（正文讨论，结果not shown）<br><span class="experiment-evidence">We also experimented with attacker-only training (not shown) and found they were better narrowly, i.e., mainly against the defender they trained against and worse on held-out ones.</span> |

**定性案例**

- 定性训练轨迹显示，简单的“覆盖系统消息”策略较早出现，而伪造chain-of-thought等更复杂策略在训练后期才出现；作者还称GPT-Red成功提示注入了现实中的AI自动售货机。前者与自博弈逐步提高难度的解释一致，后者展示跨系统迁移的可能性，但单个案例不能估计现实世界总体攻击成功率。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过攻击者与防御者群体的强化学习自博弈训练自动红队模型，以发现提示注入攻击并提升 LLM 鲁棒性。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`11ce03c2593bea4c70903b7a3335a88caea47b58bcc3d436c391892e3df95532`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
