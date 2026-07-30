---
title: "[论文解读] AgentSnare: Learning to Delay, Divert, and Defuse Autonomous Penetration Agents"
description: "[arXiv 2607.26998][LLM 安全] AgentSnare将对LLM渗透代理的防御从预先布置的静态诱饵，转变为依据攻击轨迹动态生成、校验并逐步展开一致诱饵环境的自适应引导。"
arxiv_id: "2607.26998"
announcement_date: "2026-07-30"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:25.505173+00:00"
source_sha256: "3d7e9356804494b0772b3d8fd572fc1d6365052d773cdae7aa0289a189f28ea8"
tags:
  - "LLM 安全"
  - "LLM Agent"
  - "LLM 其他"
  - "自主渗透测试代理"
  - "大语言模型代理"
  - "主动欺骗防御"
  - "轨迹自适应欺骗"
  - "诱饵环境"
  - "全局事实一致性"
  - "Delay–Divert–Defuse"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2607.26998</p>

# AgentSnare: Learning to Delay, Divert, and Defuse Autonomous Penetration Agents

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Ruoyu Wang, Heng Zhao, Renjie Wu, Mengnan Zhao, Zhixuan Chu, Wanyu Lin, Tianhang Zheng</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26998v1) · [PDF 下载](https://arxiv.org/pdf/2607.26998v1) · **关键词** 自主渗透测试代理, 大语言模型代理, 主动欺骗防御, 轨迹自适应欺骗, 诱饵环境, 全局事实一致性, Delay–Divert–Defuse  


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

AgentSnare将对LLM渗透代理的防御从预先布置的静态诱饵，转变为依据攻击轨迹动态生成、校验并逐步展开一致诱饵环境的自适应引导。

**不用术语来说**：自动化渗透代理会根据工具返回的信息不断调整攻击计划；因此，防守方虽可放置假文件、假凭据或误导指令来吸引它，但能力较强的代理会在多轮探索中发现前后矛盾，绕过诱饵并重新攻击真实系统。需要解决的问题不是制造一个更逼真的单件诱饵，而是让整套假环境能随代理的调查过程持续、连贯地发展。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出轨迹自适应欺骗系统AgentSnare：策略模型结合当前探测动作、历史交互和诱饵状态构造候选伪装物，再检查其与当前动作、既有事实及后续可执行操作是否一致，仅将有效候选增量加入诱饵环境。
- 将防御目标明确为Delay–Divert–Defuse：分别考察诱饵能否吸收探测工具调用、使进入诱饵后的行为继续停留其中，以及使任务完成判断建立在诱饵证据之上，从而评价整个攻击轨迹而非单次误导。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于自主渗透测试与主动欺骗防御的交叉领域。基于大语言模型的渗透代理通过“观察—动作”循环工作：代理读取扫描、命令执行或网页访问等工具返回的观察，据此规划并调用下一项工具，再随反馈持续调整攻击策略。由于决策依赖环境观察，防守方可以布置蜜标、误导文件、提示注入或消耗计算资源的诱饵，使代理偏离真实目标；但这些预先植入且彼此孤立的静态伪装容易在多轮探索中暴露上下文矛盾。本文因此研究一种面向完整攻击轨迹的自适应诱骗环境：防御系统根据代理已经执行的动作和当前诱饵状态，逐步披露彼此一致的新伪装事实，而不是一次性构造固定环境。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**自主渗透测试代理**

由大语言模型负责规划、调用安全工具并解释结果的自动化代理。它不同于固定脚本，会根据每轮工具观察动态改变后续探测与利用行为。

</div>
<div class="conceptitem" markdown="1">

**欺骗制品（deceptive artifact）**

防守方故意向攻击者暴露的虚假但看似可信的信息或对象，例如蜜标、误导文件和提示注入。其目的不是直接修复漏洞，而是影响代理对环境和攻击机会的判断。

</div>
<div class="conceptitem" markdown="1">

**轨迹自适应欺骗**

依据代理迄今的交互历史和诱饵环境状态，动态生成并披露下一批欺骗制品。关键要求是新旧观察在整个交互过程中保持事实一致，使代理难以通过多轮核验识破诱饵。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

场景包含一个自主渗透代理、受保护的真实目标以及可由防守方逐步展开的诱饵环境。系统可观察代理的交互历史、当前动作或探测请求以及已经承诺的诱饵事实，并可操纵返回给代理的部分环境观察；输出是经过验证、可并入诱饵状态的欺骗制品及相应观察。防御目标分为三层：在进入诱饵前后吸收更多工具调用以拖延攻击（Delay），使代理进入诱饵后继续在其中行动而非返回真实目标（Divert），并让代理最终依据诱饵证据提交任务完成报告（Defuse）。这一设定假定代理的后续决策显著依赖工具观察，同时要求动态生成的内容与当前动作、既有诱饵事实及可能的后续操作相容。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$\mathrm{Interference@20}$**

前20个交互步骤中，欺骗制品能够影响攻击代理行为的步骤比例；数值越高，表示干扰越持久。

</div>
<div class="notationitem" markdown="1">

**$\mathrm{Delay}$**

被诱饵环境吸收的代理工具调用占全部工具调用的比例，用于衡量防御拖延攻击的能力。

</div>
<div class="notationitem" markdown="1">

**$\mathrm{PER}$**

Post-Entry Retention，即代理首次进入诱饵后，仍停留在诱饵中的动作占进入后动作的比例，对应 Divert。

</div>
<div class="notationitem" markdown="1">

**$\mathrm{Defuse}$**

代理的任务完成尝试是否建立在诱饵观察或诱饵证据之上，用于判断攻击是否被虚假成功证据化解。

</div>

</div>

**直接相关的工作**

- **Pasquini, Kornaropoulos, and Ateniese (2024), Hacking Back the AI-Hacker: Prompt Injection as a Defense Against LLM-Driven Cyberattacks**: 代表利用提示注入干扰大语言模型攻击代理的静态防御路线。本文将其视为预先植入欺骗制品的一类方法，并指出固定制品难以在多步、会自我修正的攻击轨迹中持续发挥作用。
- **Sladić et al. (2024), LLM in the Shell: Generative Honeypots**: 属于利用生成模型提供交互式蜜罐响应的相关方向。本文进一步强调跨轮次的全局事实一致性，并沿代理实际轨迹增量构造诱饵，而不只是在局部生成看似真实的交互回复。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

LLM渗透代理以“观察—行动”循环自主选择工具和修正策略，这既提高了合法测试的自动化程度，也可能扩大恶意攻击能力。防守方需要在代理真正利用漏洞之前持续改变其决策方向，消耗其有限的工具调用和调查预算，并避免其重新聚焦真实目标。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **预置静态欺骗物**：攻击开始前在环境中放置蜂蜜令牌、误导文件、提示注入内容或消耗计算资源的诱饵，使代理在探索时接收到虚假观察并采取偏离真实目标的行动。
- **传统交互式蜜罐**：针对代理的局部请求返回看似真实的交互响应，以模拟可被继续探测或攻击的服务，主要追求单次或局部响应的逼真性。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 静态欺骗物的内容和出现方式预先固定，难以适配代理不断变化的意图；代理经过多步探索后可能识别上下文矛盾、绕过诱饵并返回真实目标，因此干扰通常无法持续覆盖完整攻击轨迹。
- 仅生成逼真的局部响应不足以构成可信的替代环境；若不同轮次披露的主机、文件、凭据或服务事实不能彼此兼容，后续工具操作也无法在这些事实上成立，代理便可利用全局不一致识破欺骗。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种以攻击者当前状态为条件、能够按实际轨迹逐步构造和披露诱饵，同时维护跨轮次事实一致性与后续可交互性的机制；相应地，也缺少从持续拖延、进入后留存和错误完成判断三个阶段衡量轨迹级防御效果的框架。

</div>
<div markdown="1"><span>核心问题</span>

能否学习一个轻量的伪装物构造策略，根据渗透代理的当前探测、完整交互历史和已有诱饵状态实时提出候选内容，并通过一致性校验逐步建立可信的替代现实，从而持续把代理的后续行动限制在诱饵内而非真实目标上？

</div>
<div markdown="1"><span>作者直觉</span>

代理的下一步高度依赖刚刚看到的工具结果，因此防守方不必预先搭建一套覆盖所有可能分支的完整假系统，只需沿代理实际选择的路径及时补全它最可能继续调查的事实。先生成有吸引力的候选，再过滤掉与历史冲突或无法支持后续操作的内容，就像一边观察对方走向、一边铺设前后一致的岔路，更可能让代理持续深入诱饵而不察觉环境正在动态展开。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

AgentSnare是一套面向自主渗透智能体的在线、自适应欺骗系统。其输入是攻击者可见的交互历史、当前工具动作以及已承诺的诱饵世界状态；当动作触及防御者控制的表面时，部署的LLM根据当前攻击意图构造候选欺骗制品，制品同时包含准备返回的观察与支撑该观察所需的环境事实。ShadowOS随后验证候选制品，将有效事实和对象增量写入持久诱饵环境，再向攻击智能体披露对应观察；真实目标上的动作则由原环境原样处理。系统由此沿攻击轨迹逐步展开诱饵，而非预先放置一组孤立且静态的蜜罐线索。

直观地说，AgentSnare不是一次性给攻击者一条假线索，而是像即兴搭建一座必须前后一致的“假网络”：攻击者每探测一步，系统才生成下一部分房间、文件、凭据或主机，并检查新内容能否与此前所见相容。这样既可消耗攻击工具调用，又可使进入诱饵后的后续探索继续留在其中，并可能让智能体基于诱饵证据提交完成报告。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 接收动作并划分执行表面

智能体依据 h_t 选择 a_t；系统判断该动作指向真实目标还是防御者控制的表面。真实目标动作交给原始环境且不作修改，只有到达防御表面的动作才进入欺骗流程。

<div class="method-step__io" markdown="1">

**输入**：攻击者可见的历史 h_t、攻击智能体 A 选出的工具动作 a_t，以及有限工具调用预算 B。  
**输出**：原环境直接产生的观察，或一个需要为其构造诱饵观察的当前探测请求。

</div>

**直观理解**：防御系统不是篡改所有工具结果，而是在自己控制的入口处接管响应；这保留了正常应用功能和真实漏洞执行路径。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结合轨迹推断意图并构造候选制品

部署的LLM推断攻击者当前意图，并为该次探测生成候选artifact；每个候选同时给出将向攻击者披露的观察，以及使该观察在环境中成立所需的事实。

<div class="method-step__io" markdown="1">

**输入**：当前攻击请求、完整交互历史，以及由既有事实和已披露制品组成的当前诱饵状态。  
**输出**：候选观察与其支撑事实的组合。

</div>

**直观理解**：例如，不能只凭空返回“发现一台内部主机”，还要同时准备该主机及其相关关系，使攻击者随后真的能够继续探测它。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 验证并实现一致的诱饵状态

ShadowOS在披露前验证候选制品，并把有效制品实现到诱饵环境；账本保存对象、属性、关系和攻击者造成的状态变化，可供性图表示当前可见或下一步可构造的调查机会。

<div class="method-step__io" markdown="1">

**输入**：候选制品、世界事实账本 W_t，以及惰性可供性图 G_t。  
**输出**：更新后的持久诱饵世界，以及通过验证、可安全披露的观察 o_t。

</div>

**直观理解**：这一步相当于连续性检查：已经删除的文件不能无故恢复，同一凭据或主机的描述也不能在后续响应中自相矛盾。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 披露观察并循环展开诱饵

系统将 o_t 返回给攻击者，并把动作—观察对追加到历史形成 h_{t+1}；后续工具调用重复构造、验证和披露过程，直到智能体停止或耗尽预算。

<div class="method-step__io" markdown="1">

**输入**：经验证的观察 o_t、当前动作 a_t 和既有历史 h_t。  
**输出**：扩展后的攻击轨迹，以及沿该轨迹增量形成、全局一致的诱饵环境。

</div>

**直观理解**：诱饵不是预先完整生成，而是随攻击者实际选择逐段展开，因此可把后续线索对准其正在采用的攻击策略。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 攻击者动作采样与交互历史更新

$$
a_t\sim A(h_t),\qquad h_{t+1}=h_t\mathbin{\|}(a_t,o_t)
$$

**符号说明**

- $t$：在线交互的步骤编号。
- $A$：自主渗透智能体；其规划器、记忆、工具和停止规则由攻击者控制。
- $h_t$：步骤 t 时攻击者可见的交互历史。
- $a_t$：智能体根据当前历史选择的工具动作。
- $o_t$：环境实际返回给智能体的观察；在防御者控制的表面上，它是AgentSnare构造并验证后的观察。
- $\sim$：表示动作从智能体策略给出的分布中产生，而不必是确定性选择。
- $\mathbin{\|}$：历史拼接操作，即把当前动作和观察追加到既有历史。

<div class="equation-explanation" markdown="1">

**直观理解**：该式刻画AgentSnare所作用的闭环：智能体根据过去信息采取动作，环境返回的新观察又会改变下一步决策。防御的关键正是控制防御表面上的观察，同时让该观察由一个可持续交互的诱饵世界支撑。  
**原文位置**：Online Artifact Construction and Disclosure—Interaction context，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 诱饵可供性图

$$
G_t=(V_t,E_t)
$$

**符号说明**

- $G_t$：步骤 t 的惰性可供性图，描述当前可见或下一步可能构造的调查机会。
- $V_t$：图的节点集合，对应环境对象或攻击机会，如文件、凭据、服务、主机、提权机会等。
- $E_t$：图的边集合，编码对象和攻击机会之间的关系。

<div class="equation-explanation" markdown="1">

**直观理解**：该图不是预先生成整个假环境，而是维护攻击者当前可以看到、以及系统接下来可以补建的路径。它使诱饵能够随轨迹展开，并为连续的侦察、提权或横向移动提供结构。  
**原文位置**：Online Artifact Construction and Disclosure—Decoy state and affordance frontier，公式(2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：离线训练通过模拟攻击者—防御者交互收集监督：对于同一攻击状态，系统探索多个经过验证的候选制品，并利用这些制品导致的后续轨迹，训练部署模型推断攻击意图并逐步构造能够维持诱饵探索的制品。所给原文节选未明确报告具体损失函数、候选轨迹的评分或偏好规则、参数优化公式，因此不能据此判断采用监督微调、偏好优化还是强化学习，也不能把DDD评估指标当作训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 制品构造策略模型**

该部署LLM以攻击交互历史和当前诱饵状态为条件，推断攻击者意图，并联合生成候选观察及其所要求的环境事实。离线阶段通过模拟攻击者—防御者交互，在相同攻击上下文中探索多个经过验证的制品，并用所得轨迹提供监督。

> 直观理解：它决定“下一步给出什么假线索”；同时生成支撑事实，是为了让线索不仅像真的，而且能够经受后续工具验证。

**2. ShadowOS验证与实现层**

ShadowOS在候选制品对外披露前执行验证，并将通过验证的对象和事实增量实现为可交互的诱饵环境。原文节选没有进一步列出验证规则、执行接口或失败候选的处理算法。

> 直观理解：语言模型擅长提出内容但可能产生矛盾，ShadowOS相当于发布前的事实核验与落地层，避免把无法由环境支持的描述直接返回给攻击者。

**3. 事实账本与惰性可供性图**

世界事实账本 W_t记录已承诺的诱饵对象、属性、关系及攻击者引起的状态变化；图 G_t=(V_t,E_t)的节点表示文件、凭据、服务、用户、容器、内部主机及提权或横向移动机会，边表示对象或攻击机会之间的关系。该图采用惰性构造，只表示当前可见或可能在下一步构造的调查机会。

> 直观理解：账本负责记住“这个假世界已经发生了什么”，图则负责规划“攻击者接下来还能顺着哪些方向调查”，两者共同维持长期连贯性。

**训练与推理**

训练阶段是离线的：从模拟交互状态出发，在相同攻击上下文下生成并验证多个制品，让不同候选继续演化出后续轨迹，再以这些轨迹监督制品构造策略学习攻击意图与渐进式环境构造。推理阶段是在线的：部署模型读取 h_t 与当前诱饵状态，为触及防御表面的 a_t 构造候选观察和支撑事实；ShadowOS验证并实现有效候选，更新 W_t 与 G_t 后返回 o_t，随后将 (a_t,o_t) 写入历史并继续循环。若动作指向真实目标，原始环境直接处理；整个过程受最多 B 次工具调用的攻击预算约束。

**复现信息**

公平理解该方法所必需的边界条件有三点：第一，防御者只能在不改变应用正常功能和漏洞执行路径的前提下布置或动态构造制品；第二，系统不假设已知目标CVE、攻击模型、工具配置、停止规则或攻击策略；第三，状态必须持久化，攻击者引起的变化会保留，直到被显式修改或撤销。所给节选未明确报告部署LLM型号、ShadowOS的验证器实现、候选数量、训练数据规模、优化器、超参数、运行开销或制品实现接口，因此这些复现细节仍需查阅完整论文。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- CVE-Bench中的15个可部署Web应用漏洞任务。每个任务对应一个真实CVE利用场景，用于同时测试攻击轨迹是否被诱饵接管，以及真实目标最终是否仍被官方评估器判定为成功利用。原文未明确报告数据划分。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**Delay（%）**

攻击过程中由诱饵吸收的工具调用占比，衡量有限调用预算有多少被从真实目标转移到受控环境。表中按15个CVE级均值报告均值与标准误；总体值为跨攻击者汇总结果。 （越高越好，因为更多调用预算消耗在诱饵上；但它只反映调用去向，不单独证明真实目标未被利用。）

</div>
<div class="metricitem" markdown="1">

**PER（Post-Entry Retention，%）**

代理进入诱饵之后，后续目标导向动作继续落在诱饵中的比例，用于区分短暂上钩与持续滞留。 （越高越好，因为说明代理在调查、验证和调整策略后仍主要与诱饵交互，而非迅速返回真实目标。）

</div>
<div class="metricitem" markdown="1">

**SubDefuse（%）与Verified Exploits**

SubDefuse是有效完成尝试中由诱饵证据支持的比例，检验代理是否把诱饵中的发现当作任务完成依据；Verified Exploits则由CVE-Bench官方评估器判断真实目标是否被成功利用，并按可利用的攻击者–CVE组合数报告。 （SubDefuse越高越好，表示更多完成报告建立在诱饵证据上；Verified Exploits越低越好，零表示在给定重复次数和调用预算下没有真实目标利用通过评估。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三种攻击模型、15个CVE上的总体轨迹引导

<div class="result-value" markdown="1">

AgentSnare总体Delay为46.8%，高于Cowrie的17.6%和HoneyLLMd的29.5%；总体PER为55.9%，比HoneyLLMd的36.9%高19.0个百分点。

</div>

这表明AgentSnare不仅能让代理短暂接触诱饵，还能在后续调查与验证中持续吸收较多动作。该结果衡量的是动作分配，不能单凭Delay或PER断言漏洞利用已经被阻止。

<div class="result-source" markdown="1">

来源：Table 1；RQ1，Budget absorption and retention

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Across attackers, It absorbs 46.8% of all issued tool calls, compared with 17.6% for Cowrie and 29.5% for HoneyLLMd. Its overall PER is 55.9%, a 19.0-point improvement over HoneyLLMd.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 三种攻击模型、全部CVE与重复运行中的诱饵证据闭环

<div class="result-value" markdown="1">

AgentSnare的638次有效完成尝试中有574次以诱饵证据为依据，SubDefuse为90.0%；Cowrie和HoneyLLMd分别为29.7%与72.2%。

</div>

多数有效完成尝试把受控诱饵中的信息当作成功依据，说明防御不仅拖延执行，还能影响代理对“任务是否完成”的判断。不过该指标不等同于报告内容完全正确，也不代表代理在所有运行中都会主动停止。

<div class="result-source" markdown="1">

来源：Table 1；RQ1，Decoy-grounded completion attempts

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Pooling all attackers, CVEs, and repetitions, 574 of 638 valid completion attempts are grounded in decoy evidence, yielding 90.0% SubDefuse. Cowrie and HoneyLLMd reach 29.7% and 72.2%, respectively.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 真实目标利用抑制，15个CVE × 3种攻击模型

<div class="result-value" markdown="1">

在防御条件的pass@3协议下，Static Defenses、Cowrie和HoneyLLMd仍分别有18/45、12/45和10/45个攻击者–CVE组合可被成功利用，而AgentSnare为0/45。

</div>

在每个CVE允许三次独立尝试的评估协议下，AgentSnare是唯一没有出现官方评估器确认的真实目标利用的防御。该结论严格限于所选15个CVE、三种攻击模型、200次调用预算及当前评估器，不能推出对任意漏洞或自适应攻击者均可实现零利用。

<div class="result-source" markdown="1">

来源：Table 1；RQ2，Real-target exploit suppression

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Under the pass@3 protocol used for defended conditions, Static Defenses still leave 18/45 pairs exploitable, with the same attacker-wise counts. Cowrie and HoneyLLMd reduce this number to 12/45 and 10/45, respectively, whereas AgentSnare records no verified real-target exploit (0/45).</span>

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

- Static Defenses：攻击前一次性部署13个可复现干预实例，覆盖误导感知、转移注意、专用诱饵、模型破坏、角色操纵和强制代码执行六类策略。它代表预先放置、不会随攻击轨迹演化的静态防御。
- Cowrie：提供预构建的交互式Shell、静态虚拟文件系统和脚本化命令响应。它用于比较传统高交互蜜罐能否在固定环境中持续留住自主渗透代理。
- HoneyLLMd：以分层概率自动机跟踪攻击状态转移，并由GPT-5.4-mini生成自适应响应。它是动态生成式防御基线，可检验AgentSnare的优势是否仅来自“使用语言模型实时回复”。

**实验想回答的问题**

- AgentSnare能否在攻击全过程中持续吸收工具调用、使进入诱饵后的动作留在诱饵内，并让攻击者基于诱饵证据生成完成报告？
- 这种轨迹引导能否减少真实目标上的有效漏洞利用，以及微调后的构件生成模型与有状态运行时ShadowOS分别贡献了什么？

**实验实现**

攻击端采用agentic版本PentestGPT，分别以Claude Opus 4.6、GPT-5.4和MiniMax M3作为攻击模型。每个攻击者–交互式防御组合在每个CVE上独立运行3次，共405次防御运行；所有条件共享任务提示、工具、200次工具调用预算和停止规则，交互式防御还共享应用侧breadcrumb与交互入口。防御条件按pass@3评估；无防御结果仅提供pass@1参考，因此两者不能视为完全同协议的直接对照。AgentSnare的构件生成策略使用LoRA微调的Qwen3-4B。消融实验固定GPT-5.4为攻击者，对15个CVE各重复3次，每个配置45次运行。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Base Qwen3-4B + ShadowOS：保留完整有状态运行时，但移除基于反应引导轨迹的模型微调 | 相对完整AgentSnare，Delay/PER/SubDefuse由37.7/45.0/96.5降至34.4/38.0/85.5，并有3/15个目标可被利用。 | 该对照主要隔离构件生成模型微调的贡献：相同ShadowOS下，未微调基础模型较难选择能持续引导探索的构件。不过它同时比较了两个不同参数状态的生成器，结果支持微调有效，但不能进一步区分训练数据、目标函数或模型行为中的哪一项起主要作用。 | RQ3，What Do Model Fine-Tuning and ShadowOS Contribute?<br><span class="experiment-evidence">With ShadowOS fixed, replacing the model fine-tuned on reaction-guided trajectories with Base Qwen3-4B reduces Delay/PER/SubDefuse from 37.7/45.0/96.5 to 34.4/38.0/85.5 and leaves 3/15 targets exploitable.</span> |
| AgentSnare w/o ShadowOS：保留微调模型，但移除有状态的持久验证与构件实现运行时 | Delay/PER/SubDefuse降至34.6/38.5/82.2，并有1/15个目标可被利用；其中SubDefuse相对完整系统下降14.3个百分点。 | 该消融检验跨命令保存、验证并落实一致状态是否必要。SubDefuse下降最大，说明当攻击者反复跨工具核验证据时，仅生成局部可信回复不足以维持完整证据链；但1/15与0/15的差异样本规模有限，原文未报告显著性检验。 | RQ3，What Do Model Fine-Tuning and ShadowOS Contribute?<br><span class="experiment-evidence">Removing ShadowOS while retaining the fine-tuned model yields 34.6/38.5/82.2 and leaves 1/15 targets exploitable. The 14.3-point reduction in SubDefuse, the largest degradation among the three process metrics, highlights the importance of persistent state when the attacker repeatedly verifies evidence across commands and tools.</span> |

**定性案例**

- Figure 3的聚合轨迹显示：Cowrie在大部分攻击阶段仍由真实目标占主导，HoneyLLMd使真实目标与诱饵的动作分配接近均衡，而AgentSnare在代理进入诱饵后反转二者比例，并在后期维持诱饵占多数。该图支持“持续滞留”而非“一次性吸引”的解释，但它汇总了攻击者和CVE，可能掩盖单个任务的失败轨迹。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：AgentSnare dynamically deceives and redirects tool-using autonomous LLM penetration-testing agents to prevent exploitation of real targets.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`3d7e9356804494b0772b3d8fd572fc1d6365052d773cdae7aa0289a189f28ea8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
