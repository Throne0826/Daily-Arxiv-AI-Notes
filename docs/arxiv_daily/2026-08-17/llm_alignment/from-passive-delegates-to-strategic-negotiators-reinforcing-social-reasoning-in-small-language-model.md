---
title: "[论文解读] From Passive Delegates to Strategic Negotiators: Reinforcing Social Reasoning in Small Language Models with SocialRL"
description: "[arXiv 2608.13787][对齐 / RLHF] 本文将利益冲突场景中的代理行为视为需要专门后训练的社会推理问题，并研究能否通过 SocialRL 使小型语言模型从顺从的通用助手转变为维护委托人利益的策略型代表。"
arxiv_id: "2608.13787"
announcement_date: "2026-08-17"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-17T02:07:04.886393+00:00"
source_sha256: "3da3769f1d7acae994d3eeb0b89f293e6314034b96fe6ab574c71266de066350"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "战略委托"
  - "社会推理"
  - "语言模型智能体"
  - "多轮谈判"
  - "效用优化"
  - "私有信息"
  - "跨环境迁移"
  - "理论心智"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.13787</p>

# From Passive Delegates to Strategic Negotiators: Reinforcing Social Reasoning in Small Language Models with SocialRL

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Wenyue Hua, Zachary Huang, Tyler Payne, Safoora Yousefi, Saleema Amershi, Asli Celikyilmaz</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Microsoft Research, AI Frontiers</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13787) · [PDF 下载](https://arxiv.org/pdf/2608.13787) · **关键词** 战略委托, 社会推理, 语言模型智能体, 多轮谈判, 效用优化, 私有信息, 跨环境迁移, 理论心智<br>


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

本文将利益冲突场景中的代理行为视为需要专门后训练的社会推理问题，并研究能否通过 SocialRL 使小型语言模型从顺从的通用助手转变为维护委托人利益的策略型代表。

**不用术语来说**：当 AI 代表用户议价、求职谈判或协调日程时，对话顺利结束并不等于任务完成得好：代理还必须守住用户不应公开的信息，判断对方想要什么，并在接受、让步、拒绝和继续争取之间作出有利于用户的选择。现有通用助手通常被训练得友好、坦诚且乐于达成共识，这些特点在合作任务中有益，却可能使其在利益冲突中主动泄露底线、过早退让，最终牺牲委托人的收益。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者把策略性委托明确表述为社会推理后训练问题，并建立覆盖物品分配、多议题谈判、价格议价和偏好协调的六环境套件；每个领域分别训练专家策略，再进行完整的跨环境评估，以检验能力是否随互动结构迁移。
- 作者提出 SocialRL 训练框架，并以领域强化学习、迁移感知的级联强化学习、多教师在线策略蒸馏及显式心智理论轨迹监督为切入点，研究单领域策略能否被整合为一个统一的 4B 委托代理。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究语言模型智能体的“战略委托”：智能体不只是完成用户指令，而是作为委托人的代表，在会议协调、商品议价、资源分配等多轮互动中维护委托人的利益。此类互动通常包含目标冲突和信息不对称，因此成功标准不能仅是对话流畅或最终达成协议；智能体还需保护私有偏好，推断对手的潜在目标与后续行为，并根据委托人的效用判断应当坚持、让步、延长谈判还是拒绝交易。论文将这些能力统称为社会推理，并以分配谈判、多议题协商、价格谈判和偏好协调等六种环境作为研究场景。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**战略委托（strategic delegation）**

委托人向智能体提供自己的偏好、约束或利益目标，并授权智能体与其他参与方进行有后果的互动。智能体的任务不是笼统地促成合作，而是使结果尽可能符合委托人的利益，同时遵守私有信息和可接受结果的边界。

</div>
<div class="concept-item" markdown="1">

**社会推理（social reasoning）**

社会推理是根据对话和行动推断另一方未直接公开的偏好、激励及可能行为，再据此选择策略性行动的能力。本文关注的典型行为包括选择性披露信息、预测对手下一步行动，以及决定何时坚持或让步。

</div>
<div class="concept-item" markdown="1">

**效用（utility）**

效用是将谈判或协调结果对某一参与方的价值表示为可比较分数的评价方式，例如资源组合的偏好价值或成交价格带来的收益。本文以委托人的效用而非是否达成协议作为核心结果导向，因此低价值协议可能不如拒绝交易。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个带状态的多轮互动环境、委托人的私有偏好或约束，以及来自对手方的消息和行动，语言模型策略需要持续产生自然语言回复或环境动作。对手可能是另一用户的智能体、卖家、招聘者，或异构乃至黑盒模型；双方目标可能部分一致，也可能直接冲突。环境通过私有观察、通知和动作构成的事件式接口与智能体通信，并根据最终分配、价格、录用条件或日程安排计算结果。研究覆盖 Deal-or-No-Deal、CaSiNo、Craigslist、Job Interview、Calendar 和 Marketplace 六个领域，假设智能体能够观察授权给它的信息，但不应无条件披露委托人的私有偏好；其输出目标是在多轮交互中采取能够提高委托人效用的策略，同时允许在不利条件下拒绝或延长互动。论文进一步把每个领域训练出的策略放到全部六个环境中评估，以区分领域内能力与跨领域迁移能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Deal-or-No-Deal、CaSiNo 与 Craigslist 等语言谈判环境**: 这些既有环境分别提供多物品分配、多议题资源协商和价格谈判任务，是本文构建六环境战略委托评测套件的直接基础。本文并非只检查模型能否生成连贯谈判文本，而是以委托人效用衡量策略质量，并系统评估在一个环境中训练后向其他环境迁移的效果。
- **SocialReasoning-Bench**: 本文采用其中的 Calendar 和 Marketplace 环境，将偏好驱动的时间协调与市场交互纳入测试范围。它们补充了传统谈判环境，使研究能够比较不同互动结构下的社会推理能力；所给章节未提供该基准的更多技术细节。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现实中的 AI 代理正被授权处理价格比较、购买谈判、求职沟通和会议协调等直接关系用户利益的任务。此时，对手方可能拥有不同甚至冲突的目标，而代理掌握委托人的偏好、约束或底线；代理若不能选择性披露信息、推断对方激励并设置合理的保留边界，就可能在表面友好的交互中达成对委托人不利的协议。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **通用助手式后训练**：指令微调和基于人类反馈的强化学习通常依据合作式对话中的人类偏好，将模型塑造成有帮助、诚实、无害且服从指令的助手，重点是给出合适回答并顺利完成互动。
- **通用大模型的直接谈判与聚合结果评测**：已有研究让通用语言模型直接参与物品分配、资源划分和价格议价，并以是否达成协议或最终总体收益衡量其策略能力；较大的前沿模型通常能够保持连贯对话并完成谈判。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 通用助手的透明、随和与追求共识倾向和策略性委托的目标并不一致；在存在私有信息和利益冲突时，这些行为先验会表现为未经要求披露信息、遭遇有限阻力便放弃立场以及为了成交而过度让步，使代理变得可预测且容易被利用。
- 连贯对话、较高成交率或良好的聚合结果不能证明模型忠实代表了委托人，也不能说明其学会了推断对手偏好、预测下一步行为和控制让步节奏；同时，原有研究尚未系统揭示在一个互动领域中学到的策略能否迁移到结构相似或不同的领域，并进一步整合进单一小模型。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

仍缺少一种面向小型语言模型的统一训练与评测方案，能够直接优化委托人的效用和策略性社会推理，支持多轮、异构或黑盒对手交互，并系统回答领域专家之间的迁移规律、专家能力的统一整合方式，以及显式心智理论监督究竟应训练哪些推理成分。

</div>
<div markdown="1"><span>核心问题</span>

针对六类具有利益冲突或偏好差异的多轮互动，能否通过直接的社会推理后训练，使一个 4B 模型学会保护委托人利益并达到大型前沿模型的策略水平；这些能力如何随博弈结构跨领域迁移，又能否借助级联强化学习、多教师在线策略蒸馏和心智理论轨迹监督汇聚到一个统一策略中？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把“友好地完成对话”与“有效地代表用户”拆开：若训练奖励直接反映委托人的结果，模型就会为守住底线、延迟让步或拒绝坏交易获得正向信号；若不同任务共享相似的议题结构、报价机制或约束关系，其中学到的策略便可能相互迁移。进一步让模型按照“推断对方状态、选择行动、预测对方下一步”的顺序学习，可将隐含的对手建模过程显式化，而从多个领域专家蒸馏则有望把分散策略压缩进同一个小模型。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SocialRL采用“先分域学习、再统一能力”的两阶段训练框架，基础策略统一为Qwen3-4B-Instruct-2507。第一阶段分别在Deal-or-No-Deal、CaSiNo、Craigslist、Job Interview、Calendar和Marketplace六种社会交互环境中训练专家策略：前四个环境直接从基础模型执行近端策略优化（PPO），两个价格谈判环境先用监督微调（SFT）建立基本议价行为，再用PPO根据终局效用优化。随后把每个专家放到全部六个环境中评测，以基础模型为参照构造跨环境迁移矩阵；矩阵的非对角元素刻画某个供体环境的训练对其他受体环境造成的促进或干扰。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分环境训练专家策略

对Deal-or-No-Deal、CaSiNo、Job Interview和Calendar直接运行PPO；对Craigslist和Marketplace先进行SFT，使议价所需的锚定等行为进入策略可探索的支持集，再运行PPO优化终局效用。交互由原有环境与智能体框架执行，独立的rollout代理记录模型输入、输出、旧策略对数概率和终局奖励。

<div class="method-step__io" markdown="1">

**输入**：基础策略Qwen3-4B-Instruct-2507、六个社会交互环境、各环境定义的终局效用奖励；Craigslist和Marketplace另有SFT初始化数据或检查点。<br>
**输出**：六个针对各自训练环境优化的4B专家策略，以及训练过程中用于策略和价值函数更新的轨迹数据。

</div>

**直观理解**：先让六个模型分别专攻一种谈判或协调任务。价格谈判若直接依靠奖励探索，很难偶然学会有效开价，因此先示范基本动作，再让奖励决定这些动作应如何改进。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 测量跨环境迁移结构

将每个专家分别部署到六个环境，形成以训练环境为行、测试环境为列的迁移矩阵；对角项衡量域内专门化效果，非对角项衡量训练一个供体环境后在另一受体环境上的变化。每个供体的$out-transfer$定义为其在其余五个环境中相对基础策略变化的平均值。

<div class="method-step__io" markdown="1">

**输入**：六个领域专家、未经领域训练的基础4B策略，以及全部六个评测环境。<br>
**输出**：一个有方向的跨环境迁移矩阵，以及每个环境作为训练供体时的平均外迁移信号。

</div>

**直观理解**：该步骤不是只问“哪个专家最强”，而是问“学会哪种任务会帮助或破坏哪些其他任务”。由于从环境$A$到$B$的帮助不保证反向成立，迁移关系必须按方向分别测量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 通过迁移感知级联强化学习统一能力

用同一个策略依次经过六个PPO阶段，每一阶段只在当前环境上优化，并把选定检查点作为下一阶段的初始化。训练期间周期性评估当前及此前纳入的环境，选择这些已见环境平均效用最高的检查点，以兼顾当前学习和旧能力保留。

<div class="method-step__io" markdown="1">

**输入**：Craigslist-SFT共享初始化、迁移矩阵、六个环境的终局奖励，以及由迁移结构确定的环境顺序。<br>
**输出**：一个同时服务六种交互结构的统一4B策略；该路线直接继续优化环境奖励，目标侧重最终多域性能。

</div>

**直观理解**：这相当于让同一名谈判者按精心安排的课程依次练习六类任务。容易破坏其他能力的课程被提前，互相促进的课程相邻，而容易遗忘的能力最后补回。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 通过多教师在策略蒸馏高效统一能力

每次rollout先采样环境$e$，再选取该环境对应的专家；学生在环境中生成响应，教师对这些已生成响应提供逐词元logits，学生通过反向KL蒸馏向教师分布靠近。CaSiNo教师因相对初始化几乎没有额外优势而不进入训练混合，只保留用于最终评测；原文还提出按尚未吸收的教师优势分配预算的gap-closed curriculum，但所给节选未包含其完整计算规则。

<div class="method-step__io" markdown="1">

**输入**：Craigslist-SFT学生初始化、第一阶段的领域专家教师、环境采样结果，以及学生在对应环境中自行生成的在策略轨迹。<br>
**输出**：一个由多个专家直接蒸馏得到的统一学生策略，旨在用少于完整六阶段级联RL的追加训练恢复大部分专家优势。

</div>

**直观理解**：级联RL让学生重新在每门课里试错，蒸馏则让六位专家直接批改学生自己写出的回答。训练预算优先投向学生与教师仍有明显差距的任务，已基本学会的任务不再重复占用同等预算。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 迁移感知级联课程

$$
\text{Calendar}\rightarrow\text{CaSiNo}\rightarrow\text{DnD}\rightarrow\text{Craigslist}\rightarrow\text{Marketplace}\rightarrow\text{Job Interview}
$$

**符号说明**

- $\rightarrow$：表示前一环境的PPO阶段结束并选定检查点后，将该检查点作为后一环境PPO阶段的初始化。
- $\text{DnD}$：Deal-or-No-Deal资源分配环境的缩写。
- $\text{Calendar}$：日程协调环境，被安排在最前，以免其负迁移覆盖后续获得的议价和面试能力。
- $\text{Craigslist}$：价格谈判环境，与Marketplace构成最强的正迁移环境对，并按较强的迁移方向排在Marketplace之前。
- $\text{Job Interview}$：工作面试环境，因其能力在其他环境训练后不易保留而被安排在最后恢复。

<div class="equation-explanation" markdown="1">

**直观理解**：该式不是数值损失函数，而是级联RL的关键训练路径。它把迁移矩阵转化为课程：先处理可能破坏其他技能的Calendar，再连接互相帮助的任务，最后训练容易被遗忘的Job Interview。<br>
**原文位置**：第5.3.1节，公式(11)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：第一阶段与级联RL的直接目标都是最大化各环境在交互终局给出的效用奖励。PPO使用演员策略生成的轨迹和独立价值模型给出的基线估计进行稳定更新；每个级联阶段仍优化当前环境奖励，但模型选择依据已见环境的平均效用，因此实际选择准则同时考虑新任务进展与旧任务保留。所给节选未列出PPO裁剪目标的具体公式，因而不补写未提供的数学表达。

MOPD不继续直接优化终局奖励，而是最小化学生与对应领域教师之间的反向KL差异：学生先在当前策略下生成轨迹，教师再对这些响应提供逐词元概率信息。这样，优化信号由“回合结束后得到一个效用分数”变成“每个生成位置都得到教师分布”，可减少追加训练成本；但其上限更依赖教师已有能力，并且需要通过教师筛选和gap-closed课程避免将预算浪费在学生已经接近教师的领域。节选只说明采用reverse-KL objective，未给出其论文内完整公式，因此不将通用反向KL公式冒充原文方程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 解耦式环境交互与rollout采集**

环境和智能体harness保持不变，rollout代理统一截获演员模型的输入、生成输出、rollout对数概率及终局奖励，使交互结构不同的六个环境能够复用同一套PPO实现。在MOPD中，该代理还针对学生生成的轨迹查询相应教师的逐词元logits。

> 直观理解：环境只负责把谈判或协调过程跑完，训练器只负责从过程记录中学习；二者之间的代理像统一的数据记录接口，因此换任务或换教师时不必重写环境。

**2. 迁移感知课程与检查点选择**

课程依据迁移矩阵的方向性安排：Calendar对Craigslist和Job Interview具有明显破坏性，因此置于开头；Craigslist到Marketplace的正迁移强于反方向，因此二者相邻且Craigslist在前；Job Interview容易被后续训练破坏，因此置于最后。每个阶段在已见环境上联合选择平均效用最高的检查点，而不是只依据当前环境得分。

> 直观理解：课程顺序承担两项工作：让后一门课复用前一门课的技能，并避免最后才学习会覆盖旧技能的任务。跨任务检查点选择则像阶段性综合考试，防止模型只顾当前科目。

**3. 多教师在策略蒸馏**

学生在真实环境中自行采样轨迹，领域专家仅对学生实际生成的响应提供目标分布，并以反向KL进行逐词元蒸馏；教师分布截断至概率最高的32个logits，温度为$1.0$，所有响应词元等权。教师选择考虑其相对当前学生的剩余优势，以免把预算用于几乎已被学生匹配的教师。

> 直观理解：教师不替学生生成整段标准答案，而是评价学生当前真的会说出的词。这使训练数据贴近学生部署时会访问的状态，同时减少离线示范与学生实际行为之间的偏差。

**训练与推理**

训练从同一个4B指令模型开始。阶段1中，四个环境直接执行PPO；Craigslist和Marketplace使用SFT暖启动后再执行PPO。所有专家训练完成后，对每个专家进行全环境交叉评测，以基础策略为参照计算迁移方向与强度。阶段2的级联路线从Craigslist-SFT检查点开始，按公式(11)逐环境运行PPO；每个阶段周期性在小型验证集上评估当前及此前环境，并把平均效用最高的检查点传给下一阶段。作为顺序有效性的控制，论文还保持初始化和预算不变，设置随机顺序及故意违背主要迁移规律的anti-transfer顺序。

MOPD路线同样从Craigslist-SFT检查点开始。每轮采样一个环境和相应专家，学生在策略生成完整交互轨迹，教师为学生响应返回逐词元logits，随后用反向KL更新学生；没有明显剩余提升空间的CaSiNo教师被排除出训练混合。推理时，两条路线都只保留统一的4B演员策略：输入是当前环境通过标准接口提供的对话上下文，输出是下一条自然语言行动；不使用教师、critic或额外领域路由器。

**复现信息**

所有PPO实验默认使用独立的Qwen3-1.7B critic。训练开始时冻结4B演员并预热critic 30个优化步，之后联合更新演员和critic；演员学习率为$2\times10^{-6}$，批大小为$144$、mini-batch大小为$36$、最大梯度范数为$5$，critic学习率为$1\times10^{-5}$，单次PPO最多训练$200$步。作者报告critic在演员开始训练前通常达到约$0.8$的explained variance，用于说明其已能解释大部分回合回报变化；这是价值基线可靠性的诊断量，不是最终任务指标。

级联RL的每个环境阶段最多执行$200$步，并每$20$步在小型验证集上评测检查点；所有级联和MOPD比较共享Craigslist-SFT初始化，以控制初始化差异。MOPD使用恒定学习率$10^{-5}$且不预热，教师分布只保留top-$32$ logits，蒸馏温度为$1.0$，响应中的全部词元等权。节选称MOPD可在少于$100$个额外优化步内恢复大部分专家优势，但gap-closed curriculum的完整采样概率、更新公式及后续结果未包含在当前材料中，复现时需要回查第5.3.2节余下内容。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Craigslist 双边买卖议价环境：买方围绕标价、私有目标价格与卖方多轮出价。分析将报价按“标价减目标价”的差值归一化，其中 $0$ 表示买方目标价，$1$ 表示标价，负值表示报价低于目标价；该环境用于检验初始锚定、逐轮让步、私有信息泄露及承诺性语言。原文节选未明确报告样本规模、训练/测试划分或评测回合数。
- Deal-or-No-Deal 多物品分配环境：谈判双方对帽子、球和书等物品具有不同的私有价值，需要协商分配方案；该环境主要检验模型在首个方案被拒绝后，能否继续保留高价值物品并避免零收益或谈判破裂。原文节选未明确报告样本规模与数据划分。
- CaSiNo 资源分配谈判环境：参与者对食物等资源具有高、中、低优先级，需要在保护高优先级资源的同时用低优先级资源交换；该环境用于检验保留底线和选择性让步。原文节选未明确报告样本规模与数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**归一化报价与低于目标价开局比例**

归一化报价衡量买方报价相对其目标价和卖方标价的位置；低于目标价开局比例衡量模型是否主动留出议价空间。该指标需要结合后续成交效用判断，因为过低报价本身不保证成交。 （在买方任务中，较低的初始归一化报价及较高的低于目标价开局比例通常表示锚定更强、议价空间更大；但并非无条件越低越好。）

</div>
<div class="metric-item" markdown="1">

**零收益率与未成交率**

零收益率统计代理最终没有为委托人保留价值的回合比例；未成交率统计谈判未形成协议的比例，用于观察强硬策略是否造成失败尾部。 （越低越好，因为这表示模型较少完全放弃自身价值，也较少因僵局失去交易。）

</div>
<div class="metric-item" markdown="1">

**过度让步率与强价值保留率**

过度让步率衡量代理是否交出过多高优先级资源；强价值保留率衡量代理是否显著保护自身高价值资源，直接检验选择性让步。 （过度让步率越低越好，强价值保留率越高越好；两者合看可避免把单纯拒绝或不成交误判为有效价值保护。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Craigslist 买方的锚定与逐轮让步

<div class="result-value" markdown="1">

基础模型的平均开局归一化报价为 $+0.04$，仅 $3\%$ 的开局低于目标价；SFT+PPO 将开局降至 $-1.48$，低于目标价开局比例升至 $78\%$，且平均到第三次报价仍低于目标价。作者据此认为，后训练形成了更低的初始锚点和更缓慢的让步路径。

</div>

最终策略不再一开始就报出接近自身底线的价格，而是先留下谈判空间，并在受到压力时逐步而非立即抬价。这支持“训练提高战略耐心”的解释，但不能单独证明整体收益必然提高，因为极低报价也可能降低成交概率；仍需结合效用和成交结果。

<div class="result-source" markdown="1">

来源：第 6.1 节，Craigslist: anchor low and concede gradually；表 9

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The SFT+PPO policy opens at −1.48, remains below target through its third proposal on average, and raises the below-target opening rate to 78%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Deal-or-No-Deal 中遭遇拒绝后的收益保护

<div class="result-value" markdown="1">

相对于 SFT-only 检查点，PPO 将零收益回合比例从 $4.7\%$ 降至 $2.5\%$，并将未成交比例从 $4.5\%$ 降至 $0.5\%$。作者将变化归因于策略在首选分配受到挑战后更愿意反提方案或接受有利方案，而不是突然投降或机械重复。

</div>

PPO 的改善并非只表现为更强硬：它同时减少了完全失去价值和谈判失败，说明模型更可能在保护高价值物品与达成协议之间进行调整。不过当前节选没有提供置信区间或显著性检验，无法判断这些比例差异的统计稳定性。

<div class="result-source" markdown="1">

来源：第 6.1 节，Deal-or-No-Deal: resist capitulation after rejection

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Relative to the SFT diagnostic checkpoint, PPO also reduces the zero-reward and no-deal tail: zero-reward episodes fall from 4.7% to 2.5%, and no-deals from 4.5% to 0.5%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### CaSiNo 中高优先级资源的底线保护

<div class="result-value" markdown="1">

PPO 后，过度让步回合比例从 $17.3\%$ 降至 $13.6\%$，强力保留自身价值的回合比例从 $17.3\%$ 升至 $24.2\%$。轨迹分析显示，最终策略会明确设置高优先级资源的最低保留量，并主要在低优先级资源上让步。

</div>

结果表明模型学到的不是对所有议题一律强硬，而是按照私有优先级分配让步成本：守住重要资源，用不重要资源换取协议。这更接近有效的多议题谈判，但这些行为标签如何定义和标注在当前节选中没有说明，因而仍需核查完整论文。

<div class="result-source" markdown="1">

来源：第 6.1 节，CaSiNo: maintain a floor on high-priority resources

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At the distribution level, the fraction of over-conceding games falls from 17.3% to 13.6%, while the fraction of games in which the agent strongly preserves its own value rises from 17.3% to 24.2%.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- Craigslist 环境没有提供外部可比价格信息，但训练后模型会引用所谓市场价或类似商品价格；作者明确将其视为学习到的虚构或诈唬，而非事实依据更充分。这意味着效用提升可能伴随真实性与可信度风险。
- 当前节选主要是第 6 节的定性和行为分析，未报告评测样本量、随机种子、置信区间、显著性检验及行为标签的标注一致性；因此数值可描述观察到的变化，却不足以单独判断泛化范围、统计可靠性或训练方法的因果贡献。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Untrained/Base model：未经该领域后训练的基础小语言模型，用于确定模型原有的谈判能力及其快速让步、泄露目标价格等缺陷。
- SFT-only checkpoint：仅用监督示范进行微调的诊断性基线，用于识别模仿学习能否引入低价锚定、市场比较等行为，以及它是否会因偏好友好回答而导致过度让步。
- SFT+PPO/final domain-trained policy：先经监督微调、再以 PPO 强化学习得到的最终策略；它是论文的主要方法，并与基础模型和 SFT-only 检查点比较，以判断奖励优化是否会进一步筛选有利的谈判行为。

**实验想回答的问题**

- 后训练是否会改变小语言模型的战略决策，使其在遭遇拒绝或阻力时减少无条件让步，并更好地保护委托人的高价值利益？
- 监督微调（SFT）与近端策略优化（PPO）分别带来什么行为变化，即哪些策略主要来自示范模仿，哪些策略经过强化学习后才被稳定选择？

**实验实现**

定性分析覆盖六个谈判环境，并在每个环境中比较基础模型与最终领域策略；存在 SFT-only 检查点时，再用它区分模仿学习与强化学习的作用。分析对象包括聚合行为分布和配对交互轨迹，重点检查开局锚点、让步路径、拒绝后的响应、为委托人保留的价值、语言风格及动作选择。原文节选没有给出模型规模、PPO 超参数、采样温度、随机种子、统计显著性检验、评测回合数或人工标注流程，因此这些实现细节不能从当前材料确认。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Craigslist 中 Untrained、SFT 与 SFT+PPO 的阶段比较 | 平均初始归一化报价依次为 $+0.04$、$-1.21$ 和 $-1.48$，低于目标价开局比例依次为 $3\%$、$71\%$ 和 $78\%$；SFT 已产生主要的低价锚定变化，PPO 又将锚点下移并减慢后续让步。 | 该比较隔离了两阶段训练的相对作用：从基础模型到 SFT 的大幅变化说明锚定行为主要可由示范引入；从 SFT 到 SFT+PPO 的进一步变化说明奖励优化会强化并维持该策略。它不是严格的单因素消融，因为当前节选未说明训练数据量、优化步数等是否完全匹配。 | 第 6.1 节，Craigslist: anchor low and concede gradually；表 9<br><span class="experiment-evidence">SFT introduces the missing anchoring behavior: the mean opening moves to −1.21, and 71% of games begin below the buyer’s target.</span> |
| CaSiNo 中 SFT-only 对过度让步的诊断 | 基础模型的过度让步率为 $17.3\%$，SFT-only 将其提高到 $29.4\%$；相比之下，最终 PPO 策略将该比例降至 $13.6\%$。作者据此提出，模仿学习可能强化友好、顺从的表达，却没有校准应让出多少价值。 | 该诊断表明，学会看似合作的回复不等于学会有利的谈判策略；PPO 的奖励信号可能负责纠正 SFT 的过度迎合倾向。不过它只能显示相关的训练阶段差异，不能排除检查点选择或训练配置造成的影响。 | 第 6.1 节，CaSiNo: maintain a floor on high-priority resources<br><span class="experiment-evidence">The SFT diagnostic moves in the opposite direction, raising over-concession to 29.4%, suggesting that imitation alone can favor agreeable behavior without calibrating how much value to surrender.</span> |

**定性案例**

- Craigslist 的配对轨迹中，标价为 $275$、买方目标价为 $209$：基础模型从 $209$ 开始并最终接受 $275$，得到零效用；训练后策略按 $150\rightarrow165$ 的路径报价，拒绝 $250$，最终以 $190$ 成交并获得最大效用。该案例直观展示了低价锚定和承压坚持如何共同改善单局结果，但它只是示例轨迹，不能替代总体分布或显著性检验。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：SocialRL is a reinforcement-based post-training method for improving strategic social reasoning and negotiation in small language models.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`3da3769f1d7acae994d3eeb0b89f293e6314034b96fe6ab574c71266de066350`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
