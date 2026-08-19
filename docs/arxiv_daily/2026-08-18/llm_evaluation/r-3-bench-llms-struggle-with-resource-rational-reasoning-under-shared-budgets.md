---
title: "[论文解读] $R^3$-Bench: LLMs Struggle with Resource-Rational Reasoning under Shared Budgets"
description: "[arXiv 2608.16033][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.16033"
announcement_date: "2026-08-18"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:11:27.770580+00:00"
source_sha256: "7322175a7c7cd11c4bbd3a2d783c40317a22297029f58a5f4f7a10726134944d"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "大语言模型"
  - "资源理性推理"
  - "共享预算"
  - "测试时计算"
  - "跨任务资源分配"
  - "机会成本"
  - "单题响应曲线"
  - "离线经验预言机"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.16033</p>

# $R^3$-Bench: LLMs Struggle with Resource-Rational Reasoning under Shared Budgets

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Peisong Wang, Zhiwei Ma, Bowen Liu, Feixue Liu, Aochuan Chen, Chenyi Zi, Hongchuan Zeng, Yuhan Li, Jia Li</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: The University of Hong Kong；Affiliation: Hunyuan Team, Tencent；The Hong Kong University of Science</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.16033) · [PDF 下载](https://arxiv.org/pdf/2608.16033) · **关键词** 大语言模型, 资源理性推理, 共享预算, 测试时计算, 跨任务资源分配, 机会成本, 单题响应曲线, 离线经验预言机<br>


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

原文未明确报告。

**不用术语来说**：原文未明确报告。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 原文未明确报告。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大语言模型的推理能力不仅取决于能否解题，也取决于如何使用推理时的有限计算资源。增加思考长度、工具调用、程序测试或答案验证通常可以提高单题成功率，但会消耗令牌、时间、调用次数及外部服务配额；当多个问题共用一个总预算时，在某题上继续计算会压缩其他题的可用资源，因此模型还必须决定先做哪题、为每题投入多少、何时切换或停止。本文把这种跨问题决策视为“资源理性推理”：目标不是不计成本地逐题求解，而是在机会成本存在时，用有限计算取得尽可能高的整套任务收益。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**资源理性（resource rationality）**

资源理性把计算成本显式纳入理性决策，要求智能体在有限计算资源下最大化预期收益。通俗地说，智能体不仅要判断怎样解题，还要判断继续思考是否值得。

</div>
<div class="concept-item" markdown="1">

**测试时扩展（test-time scaling）**

测试时扩展是在模型参数固定的情况下，通过增加推理令牌、采样、验证或工具交互等测试阶段计算来改善答案。它说明更多计算可能带来更高成功率，但也使预算分配成为必须评估的问题。

</div>
<div class="concept-item" markdown="1">

**共享预算与机会成本**

共享预算指一组任务共同消耗同一有限资源池，而不是每个任务获得互不影响的独立额度。在总预算固定时，一个任务多消耗的资源意味着其他任务少获得资源，这一损失就是跨任务计算的机会成本。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文研究模型能否在共享预算下实现其已经在单题环境中表现出的能力。$R^3$-Bench 在奥林匹克风格数学、竞赛编程和抽象推理三个领域分别构造由六道不同资源需求问题组成的竞赛，每个领域包含 $50$ 场竞赛；同一场内六题竞争一个总预算，并分别在无工具推理和可使用工具的智能体设置下评测。模型的输入是六题组成的任务套件及共享资源约束，模型需要自行决定题目覆盖、计算投入、工具或验证操作、任务切换与停止时机，输出各题答案或解题产物，最终以整套任务的成功情况衡量共享预算表现。为区分“不会解题”与“会解但没有合理分配资源”，研究还对匹配的单题运行建立资源投入与成功结果之间的经验响应曲线，并据此构造等额分配回放和同模型离线经验预言机；后者只在已观察到的单题成功中选择满足总预算约束的组合，是诊断上界而非模型在实际竞赛中可执行的在线策略。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$R^3$**

Resource-Rational Reasoning，即本文评测的“资源理性推理”。

</div>
<div class="notation-item" markdown="1">

**$B$**

一场六题竞赛可共同使用的总资源预算；原文节选未给出其正式符号，此处仅用于说明问题设定。

</div>
<div class="notation-item" markdown="1">

**$b_i$**

分配给第 $i$ 道题的资源量，并受各题资源总和不超过共享预算的约束；原文节选未给出其正式符号。

</div>
<div class="notation-item" markdown="1">

**$i$**

竞赛中的问题索引，一场竞赛共有六个问题槽位。

</div>

</div>

**直接相关的工作**

- **USACOArena**: 该工作在带信用预算的编程竞技场中研究智能体行为，已经涉及多任务共享资源，但覆盖重点是智能体式竞赛编程；本文进一步同时覆盖数学、编程与抽象推理以及无工具和智能体设置，并用匹配的单题表现校准共享预算结果。
- **CLEAR**: 该工作借助外部效用模型和影子价格策略在多个查询之间优化令牌分配，属于直接相关的跨查询资源配置研究；但原文指出，它没有把共享预算分配效果与同一模型逐题展现的推理能力进行比较，而这正是 $R^3$-Bench 要填补的评测缺口。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现代大语言模型在解题时可以通过增加推理步骤、运行工具、测试候选答案或进行验证来提高成功概率，但这些操作都会消耗有限的推理令牌、时间、工具调用次数和接口配额。当多个问题同时运行并共享同一计算预算时，一个问题上投入更多资源，就会减少其他问题可用的资源，因此系统必须同时决定解决什么、投入多少以及何时停止。现有单问题评测无法反映这种跨问题的机会成本，而真实的编程、软件工程和多智能体工作流恰恰经常包含多个并发任务。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **独立任务的推理与智能体基准**：这类方法逐题评估模型能力，通常为每个问题单独设定令牌、时间或工具预算。模型可以在每道题上使用完整额度，评测重点是单个问题能否解决，而不是多个问题之间如何分配总资源。
- **单问题预算控制与跨阶段资源编排**：预算感知方法在单个问题内部调整采样次数、推理令牌或工具使用量；资源编排方法则在不同模型、模块或处理阶段之间分配资源。较接近的工作包括在信用额度约束下评估编程智能体，或利用外部效用模型和影子价格策略在多个查询间分配令牌。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 独立任务评测消除了跨问题的资源竞争：模型可以对每道题都花费完整预算，因而无法检验它是否能根据问题难度、已有进展和剩余总预算进行切换、继续或停止。其结果只能说明模型的单题能力，不能说明这些能力在共享预算下能否被有效实现。
- 已有预算控制或资源分配方法通常缺少与同一模型单题能力的校准。它们可能报告一种分配策略带来的总体表现，却没有回答该表现距离模型在单题响应曲线中已经展示出的潜在成功数有多远，因此难以区分模型本身不会解题与模型不会管理共享资源这两种失败来源。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚未解决的关键缺口是：缺少一种同时具备共享预算、多问题竞争、跨领域覆盖，并能用同一模型的匹配单题表现作为参照的评测框架。具体而言，研究者需要知道模型在单题上已经展示的能力，有多少能够通过自身的在线分配行为转化为共享预算下的实际成功；还需要识别模型是否会根据新证据和剩余预算更新策略，而不是仅仅机械地平均分配或持续投入。

</div>
<div markdown="1"><span>核心问题</span>

当多个问题共同竞争一个有限推理预算时，大语言模型能否把自己在独立单题上已经展示的解题能力有效转化为整组问题上的成功，还是会因无法决定何时继续、何时切换以及应把剩余资源投向何处而产生系统性损失？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把共享预算表现与同一模型的单题响应曲线进行匹配比较。单题响应曲线记录模型在不同资源投入下实际成功过哪些问题；据此构造的离线经验上限可以近似回答“如果资源分配得更合理，模型已有能力最多能实现什么”。若共享预算下的竞赛表现低于这一参照，差距就更可能来自跨题资源管理，而不是单纯缺乏知识或解题能力。这样既能定位模型的分配失误，也能进一步观察它是否会利用运行反馈调整策略。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文提出的不是一种训练模型的新算法，而是一套评估大语言模型“资源理性”的基准协议。核心问题是：当六道题共享同一计算预算时，模型能否根据题目难度、求解进展和剩余资源，合理决定做哪些题、每题投入多少资源以及何时切换或停止。基准覆盖数学、竞赛编程和抽象推理三个领域，并在两种运行方式下使用相同题池与评分规则：无工具推理以输出 token 为资源，智能体设置以实际执行的计数动作作为资源。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建分层题池与六题竞赛

先用 DeepSeek V4 Pro、GLM-5.2 和 GPT-5.5 在单题无预算限制条件下的平均输出长度衡量资源需求，再将每个领域最短的 150 题标为 Easy、接下来的 100 题标为 Medium、最长的 50 题标为 Hard。随后每个领域构造 50 场竞赛，每场随机排列三道 Easy、两道 Medium 和一道 Hard 题。

<div class="method-step__io" markdown="1">

**输入**：每个领域的 300 道题：数学题来自 Omni-MATH 和 MathNet，竞赛编程题来自 LiveCodeBench Pro，抽象推理题来自 Reasoning Gym。<br>
**输出**：三个领域各 50 个组成固定但展示顺序随机的六题竞赛，以及供单题评估和竞赛评估共同使用的分层题池。

</div>

**直观理解**：这里的“难度”不是按模型答对率事后划分，而是按参考模型自然需要写多长来近似资源需求。每场都采用相同的难度配比，使模型之间的差异更可能来自预算分配，而不是某场比赛碰巧更难。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按模型校准共享预算压力

计算模型在该领域正常完成竞赛时的平均自然资源消耗 $R_{m,d}^{\infty}$，再按压力系数 $\rho\in\{0.2,0.8\}$ 设置共享预算 $R_{m,d}^{\rho}=\rho R_{m,d}^{\infty}$。离散资源单位需要取整，其中 $\rho=0.2$ 表示强压力，$\rho=0.8$ 表示中等压力。

<div class="method-step__io" markdown="1">

**输入**：模型 $m$ 在领域 $d$ 的各场无预算限制竞赛，以及其中正常完成的竞赛集合 $\mathcal{C}_{m,d}^{\mathrm{valid}}$。<br>
**输出**：针对每个模型、领域和压力等级分别校准的 token 预算或动作预算。

</div>

**直观理解**：不同模型天生可能偏好长推理或频繁调用工具，直接给所有模型同一个绝对额度并不公平。该步骤相当于把每个模型自己的正常消耗视为 100%，再比较它们只剩 20% 或 80% 资源时如何安排任务。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 运行共享预算竞赛

无工具设置将共享 token 额度作为 API 的 `max_tokens`，模型一次性自由生成六题答案；智能体设置允许执行命令、代码和检查中间结果，并按解析出的可执行解题动作扣减共享动作预算。预算耗尽后，系统阻止新的计数动作，但仍允许题目标记、整理结果和提交最终答案。

<div class="method-step__io" markdown="1">

**输入**：一场包含六道题的竞赛、模型专属共享预算 $R_{m,d}^{\rho}$，以及无工具或智能体运行环境。<br>
**输出**：六题最终答案或提交产物、每题二元正确性、总竞赛分数，以及包含资源消耗和任务切换信息的运行轨迹。

</div>

**直观理解**：六道题使用同一个“钱包”，在一道题上花得越多，留给其他题的资源就越少。模型因此不仅要会解题，还要判断继续深挖当前题是否比转向另一题更值得。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 测量单题能力并构造离线分配参照

对每道题建立“预算等级到经验成功率”的响应曲线；等额分配回放检查每题是否存在资源成本不超过竞赛总预算六分之一的成功尝试。响应曲线 oracle 则把每题的零预算选项及多个预算等级视为候选，在总预算约束下求解多选背包问题，以最大化六题预期正确数。

<div class="method-step__io" markdown="1">

**输入**：与竞赛完全相同的题目、固定预算等级网格，以及每个预算等级五次独立单题运行的结果。<br>
**输出**：每题经验响应曲线、等额分配基线分数，以及具有完整离线单题信息的 oracle 分数。

</div>

**直观理解**：单题实验先回答“如果资源给得合适，模型原本能不能做对”；oracle 再像事后知道每项投资回报的调度员一样选择预算。它不是可在线部署的真实策略，而是用来估计模型已经展示过、却未在共享预算竞赛中兑现的能力。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 模型专属预算校准

$$
R_{m,d}^{\infty}=\frac{1}{|\mathcal{C}_{m,d}^{\mathrm{valid}}|}\sum_{c\in\mathcal{C}_{m,d}^{\mathrm{valid}}}R_{m,d,c}^{\infty},\qquad R_{m,d}^{\rho}=\rho R_{m,d}^{\infty},\quad \rho\in\{0.2,0.8\}
$$

**符号说明**

- $m$：被评估的模型。
- $d$：题目领域，即数学、竞赛编程或抽象推理。
- $c$：某一场六题竞赛。
- $R_{m,d,c}^{\infty}$：模型在领域 d 的竞赛 c 中进行无预算限制基线运行时实际使用的资源；无工具设置中为输出 token，智能体设置中为计数动作。
- $\mathcal{C}_{m,d}^{\mathrm{valid}}$：模型在领域 d 中正常完成、可用于计算基线的竞赛集合。
- $R_{m,d}^{\infty}$：模型在领域 d 上正常完成竞赛时的平均自然资源消耗。
- $\rho$：相对预算系数；0.2 对应强预算压力，0.8 对应中等预算压力。
- $R_{m,d}^{\rho}$：压力系数为 rho 时，模型在领域 d 获得的共享竞赛预算。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分用正常完成的无预算限制竞赛估计模型平时解决整套题会消耗多少资源；第二部分只保留该消耗的一定比例。这样比较的是各模型面对相似相对压力时的调度能力，而不是它们输出风格或工具使用频率造成的绝对消耗差异。<br>
**原文位置**：第 3.1 节 Model-specific budget calibration

</div>

</div>

<div class="equation-block" markdown="1">

#### 资源理性差距

$$
\Delta_{\mathrm{RR}}=\mathrm{Oracle}-\mathrm{Contest},\qquad \mathrm{GapRatio}=\frac{\Delta_{\mathrm{RR}}}{\mathrm{Oracle}},\quad \mathrm{Oracle}>0
$$

**符号说明**

- $\mathrm{Contest}$：模型在真实共享预算竞赛中的平均正确题数。
- $\mathrm{Oracle}$：响应曲线 oracle 在相同总预算约束下得到的平均预期正确题数。
- $\Delta_{\mathrm{RR}}$：oracle 分数减去真实竞赛分数得到的绝对资源理性差距。
- $\mathrm{GapRatio}$：绝对差距相对于 oracle 分数的比例，仅在 oracle 分数大于 0 时定义。

<div class="equation-explanation" markdown="1">

**直观理解**：oracle 表示模型依据单题实验已经展示出来的、经过理想离线分配可实现的能力，Contest 表示模型自己在线分配预算后真正兑现的能力。差距越小，说明模型越能把已有解题能力转化为共享预算下的整体收益；该指标不是一般能力分数，也不证明 oracle 是现实可用的在线策略。<br>
**原文位置**：第 3.4 节 Allocation quality

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。$R^3$-Bench 是评估与诊断协议，不训练或微调被测模型，也没有通过梯度优化学习预算分配策略。响应曲线 oracle 中的“最大化预期正确数”是离线多选背包求解目标，只用于形成经验参照；它利用完整单题响应曲线，不能视为模型在竞赛过程中可获得的信息或训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 匹配的单题响应曲线与共享预算竞赛**

同一批题既被独立评估，也被组合成六题共享预算竞赛。单题侧在多个固定预算等级上各运行五次，以经验成功率描述模型在不同资源投入下的可达能力；竞赛侧则记录模型自主选择任务和预算后的实际表现。

> 直观理解：若只看竞赛失败，无法判断模型是不会解题还是没有合理投入资源。匹配的单题实验提供能力参照，使两类原因能够被分开。

**2. 等额分配回放与响应曲线 oracle**

等额回放为每题隐式保留总预算的六分之一，并依据已有单题成功尝试判断该固定策略可实现的结果。oracle 允许每题从零预算和多个名义预算等级中选择一个，在总预算约束下最大化响应曲线给出的预期正确数，因此对应多选背包分配。

> 直观理解：等额回放检验一个极简单的平均分配规则是否已经优于模型自由调度；oracle 则给出拥有完整事后信息时的经验上界。二者共同说明问题究竟来自明显不均衡，还是来自更细致的任务选择和投入深度。

**3. 智能体动作记账与轨迹诊断**

智能体通过 `focus_problem <id>` 标记当前题目，并在切换前调用 `shelve_problem`；这些记账步骤不扣共享预算。真正执行解题计算的工具动作每次消耗一个预算单位，常规文件操作免费，运行时持续向智能体显示已用和剩余动作数。

> 直观理解：全局预算本身无法说明某个动作服务于哪道题，因此需要显式标记当前任务。免费记账避免因分析行为而额外惩罚模型，同时使研究者能够重建资源在不同难度题目之间的流向。

**训练与推理**

整个流程只有推理与离线评估。首先对每个模型和领域运行无预算限制的六题竞赛，仅使用正常完成的运行计算 $R_{m,d}^{\infty}$，再生成强压力与中等压力预算。随后在相同题目上分别执行单题预算网格实验和共享预算竞赛：单题实验的每个预算等级运行五次以估计经验成功率；竞赛实验把六题同时交给模型，由模型自行决定尝试顺序、每题投入和停止时机。

无工具推理中，模型不访问外部工具或交互反馈，只生成一次自由文本完成，输出 token 总数受共享额度限制。智能体推理中，模型可执行工具动作并观察中间结果，但运行期间得不到官方正确性反馈；系统按可执行解题动作扣费，通过免费记账命令把动作归属到具体题目，并在预算耗尽后只允许记账和最终提交。最后由统一的领域评分器判定答案，离线构造响应曲线、等额回放和 oracle，再计算差距指标并分析轨迹。该协议测量的是固定模型在预算竞争环境中的行为，不涉及参数更新。

**复现信息**

复现时最关键的是保持单题与竞赛评估的题池、答案解析器和评分协议一致，否则 oracle 与 Contest 不再对应同一种能力。每个领域使用冻结的 300 题池并构造 50 场六题竞赛；难度层按三个参考模型的平均单题输出长度固定划分，层级不出现在提示中，竞赛展示顺序独立随机化。每题采用二元满分标准，竞赛主结果是每场答对题数的平均值，分难度和位置分析才使用题级准确率。

预算单位必须按设置区分：无工具环境计输出 token，并通过 API 的 `max_tokens` 强制限制；智能体环境计解析后实际执行的解题动作，而非模型轮数，常规文件操作和任务记账不收费。智能体没有运行时官方正确性反馈，正确性只从最终提交产物判定。计算资源理性差距时必须说明 oracle 拥有完整离线响应曲线，且响应曲线来自每个预算等级五次独立运行；因此它是经验最佳分配参照，并非理论上界，也可能受预算网格、随机运行次数和经验成功率估计误差影响。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- $R^3$-Bench数学部分：用于考查模型在共享输出词元预算下对数学题进行选择、推理并提交最终答案的能力。单题回答采用$\boxed{\cdots}$格式；竞赛设置一次提供六道彼此独立的问题。原文节选未明确报告题目总量、数据来源及训练集、验证集、测试集划分。
- $R^3$-Bench代码部分：要求模型生成完整、可独立编译的C++17程序，并由可执行验证器判定正确性；智能体竞赛中，不同问题的程序写入独立文件。该部分测试共享预算下的代码解题与资源分配。原文节选未明确报告题目总量、来源或数据划分。
- $R^3$-Bench抽象推理部分：答案需置于`<answer>...</answer>`标签中，并由规则验证器检查；竞赛设置同样包含六道独立问题。该部分用于检验模型在较少依赖领域知识的推理任务中能否进行资源理性的选择。原文节选未明确报告题目总量、来源或数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

原文未明确报告，或这里不需要额外前置概念。

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给节选缺少表2及完整八模型结果，也未包含主要指标、数值结果、置信区间或显著性检验。因而无法按来源证据报告三项主要结果或任何消融结论；相关内容均应以论文完整表格和正文为准。
- 节选未明确报告题目来源与总量、数据划分、五档单题预算和两档竞赛预算的具体数值、模型采样参数及重复运行次数。这些信息会影响对模型间比较公平性、结果方差和可复现性的判断。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- DeepSeek-V4系列，包括DeepSeek-V4-Chat、DeepSeek-V4-Reasoner和DeepSeek-V4-Pro：同一模型家族中的对话、推理和增强版本可用于比较专门推理设计是否改善共享预算下的决策与解题表现。
- Qwen3.7-Max与GLM-5.2：作为近期前沿大语言模型，用于检验观察到的资源分配问题是否跨模型家族存在，而非仅属于某一厂商或架构。
- Hy-3：作为另一前沿模型参与八模型横向评测，扩大模型来源的覆盖范围；原文节选没有提供其具体推理模式或上下文配置。
- GPT-5.5与Claude-Opus-4.8：作为闭源前沿模型，与其他模型家族比较工具禁用和智能体设置中的资源理性表现。原文节选未给出版本参数、采样配置或调用日期。

**实验想回答的问题**

- 八个前沿大语言模型在$R^3$-Bench的工具禁用与智能体两种设置下，面对数学、代码和抽象推理任务时，能否在共享预算约束内合理选择题目并分配推理资源，以最大化竞赛总得分？
- 模型的资源理性表现是否会随预算压力变化，即模型能否在更紧张的总输出预算下优先解决把握更高、预计耗费更少的问题，而不是平均分配资源或盲目尝试全部问题？

**实验实现**

实验覆盖两种设置、三个任务领域和两档预算压力，共评测DeepSeek-V4-Chat、DeepSeek-V4-Reasoner、DeepSeek-V4-Pro、Qwen3.7-Max、GLM-5.2、Hy-3、GPT-5.5及Claude-Opus-4.8八个模型。工具禁用设置中，模型只能以自然语言或规定代码格式作答；单题响应曲线使用附录E定义的五档预算上限，且对思考型模型，隐藏推理词元和最终答案词元都计入预算。竞赛设置一次给出六道独立问题，共享一个总响应词元预算，允许模型只提交部分题目，未提交题目计零分；提示明确要求模型扫描全部题目，优先选择预计能可靠且低成本解决的问题。数学答案由基于模型的等价性判定器评估，代码由可执行验证器评估，抽象推理由规则验证器评估。提示模板采用稳定前缀加运行时内容的分层结构，以增加服务商侧前缀缓存复用机会；求解模型看不到预言机决策、参考答案、隐藏测试结果、响应曲线选择或判定器反馈。原文节选未给出温度、采样次数、随机种子、具体预算值以及最终计分指标的正式定义。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces a benchmark for evaluating LLM resource-rational reasoning under shared computational or decision budgets.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`7322175a7c7cd11c4bbd3a2d783c40317a22297029f58a5f4f7a10726134944d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
