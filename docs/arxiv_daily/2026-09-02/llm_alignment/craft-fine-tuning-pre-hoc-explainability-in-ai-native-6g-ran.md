---
title: "[论文解读] CRAFT: Fine-Tuning Pre-hoc Explainability in AI-native 6G RAN"
description: "[arXiv 2609.00590][对齐 / RLHF] 原文未明确报告。"
arxiv_id: "2609.00590"
announcement_date: "2026-09-02"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:49:09.774904+00:00"
source_sha256: "1861112c25abd92118f66a999819aa2e534ef2deff9f7aed78ea207945d9bb9b"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "AI-RAN"
  - "O-RAN"
  - "小语言模型"
  - "预先推理"
  - "思维链"
  - "低秩适配"
  - "组相对策略优化"
  - "可审计决策"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2609.00590</p>

# CRAFT: Fine-Tuning Pre-hoc Explainability in AI-native 6G RAN

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Pranshav Gajjar, Vijay K Shah</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: NextG Wireless Lab NCSU Raleigh USA；Affiliation: NextG Wireless Lab</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00590v1) · [PDF 下载](https://arxiv.org/pdf/2609.00590v1) · **关键词** AI-RAN, O-RAN, 小语言模型, 预先推理, 思维链, 低秩适配, 组相对策略优化, 可审计决策<br>


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

本文位于面向第六代移动通信的 AI 原生无线接入网（AI-RAN）场景。O-RAN 的解耦架构通过 RAN 智能控制器承载 xApps 与 rApps，使模型能够根据实时关键性能指标（KPI）遥测执行资源分配、网络切片和干扰缓解等任务；部署在边缘侧的小语言模型（SLM，文中指约 1 亿至 50 亿参数）因此既要给出正确决策，也要提供运营人员可审计的依据。本文关注“预先推理”：模型先生成推理轨迹 $t$，再依据输入 $x$ 与轨迹预测标签 $y$，其联合生成可写为 $p_{\theta}(t,y\mid x)=p_{\theta}(t\mid x)p_{\theta}(y\mid x,t)$。这种顺序不同于在预测完成后附加解释的事后合理化；但电信 SLM 缺乏合格推理轨迹的先验，直接采用强化学习时往往难以同时学会输出格式、有效推理和正确标签，构成本文所称的冷启动障碍。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**预先推理与思维链**

思维链（CoT）要求模型在最终答案前生成中间推理步骤；预先推理进一步强调标签 $y$ 应在生成机制上依赖先产生的轨迹 $t$，而不是先决定答案再补写理由。本文采用的可检验标准是：结合输入 $x$ 和轨迹 $t$ 时，模型应能恢复真实标签。

</div>
<div class="concept-item" markdown="1">

**低秩适配**

低秩适配（LoRA）冻结预训练权重 $W_0$，只训练较小的低秩矩阵 $A$ 与 $B$，使层输出成为 $h=W_0x+\frac{\alpha}{r}BAx$。直观上，它以较少的可训练参数把通用模型适配到电信任务，适合算力和存储受限的边缘部署。

</div>
<div class="concept-item" markdown="1">

**组相对策略优化**

组相对策略优化（GRPO）对同一输入采样一组候选输出，以组内奖励的均值和标准差构造相对优势，无需像 PPO 那样额外训练价值网络。其奖励通常同时评价模板合规、推理是否非空以及标签正确性，而这些目标在缺乏初始推理能力的小模型上可能相互竞争。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定来自电信 xApp 数据集的一条结构化 KPI 遥测输入 $x$ 及其真实类别，目标是在 AI-RAN 的边缘计算约束下训练紧凑 SLM，使其按指定格式先输出人类可读且非退化的推理轨迹 $t$，再输出任务标签 $y$。模型不仅应保持分类正确和输出可解析，还应让标签由输入与先前轨迹共同导出；这排除了仅在决策后生成解释的设置。本文讨论的关键前提是：未经推理对齐的 SLM 对电信任务中的有效轨迹缺乏先验，因而直接用 GRPO 同时优化格式、内容与正确性可能无法有效探索。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

模型接收的电信任务输入，例如实时 KPI 遥测特征。

</div>
<div class="notation-item" markdown="1">

**$t$**

在最终标签之前生成的人类可读推理轨迹。

</div>
<div class="notation-item" markdown="1">

**$y$**

任务的真实标签或模型最终输出的类别。

</div>
<div class="notation-item" markdown="1">

**$p_{\theta}(t,y\mid x)$**

参数为 θ 的模型在给定输入后联合生成推理轨迹与标签的条件概率；预先推理将其分解为先生成轨迹、再依据输入和轨迹生成标签。

</div>

</div>

**直接相关的工作**

- **RANSTRUCT**: 代表电信语言模型的监督微调路线，并通过 LoRA 适配模型；其训练重点是直接生成正确答案，原文指出它没有提供可审计推理轨迹的机制，因此不能满足本文的预先解释要求。
- **Group Relative Policy Optimization (GRPO)**: 代表推理导向的强化学习路线，通过同一输入的一组采样输出计算相对优势并优化策略。本文以其作为重要技术背景，但指出将其直接迁移到电信 SLM 时会遭遇冷启动障碍。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CRAFT（Cold-start Reasoning Alignment via Fine-Tuning）的核心不是直接用强化学习逼迫小语言模型同时学会“正确分类”和“按格式推理”，而是先构造一个经过验证的监督数据集，再进行参数高效微调。给定带标签的电信 KPI 样本 $(x_i,y_i)$，同一个基础模型以两种不同提示分别扮演 Oracle Reasoner 和 Predictor：前者已知真实标签并生成候选推理轨迹 $t_i$，后者看不到真实标签，只根据 KPI 输入与该轨迹恢复预测标签 $\hat y_i$。只有格式有效、长度足够且满足 $\hat y_i=y_i$ 的轨迹才进入验证集 $\mathcal D'$；随后目标 SLM 通过 LoRA 学习依次输出推理轨迹和标签。

技术上，这一设计把困难的联合冷启动问题分解为“生成候选解释—检验解释是否携带决策信息—监督学习稳定复现”三个较容易控制的环节。直观地说，Oracle 像一名拿着参考答案写解题过程的教师，Predictor 像一名只看题目和解题过程、必须自行交卷的学生；如果学生能据此得到正确答案，才认为该过程具有可用于决策的信息。不过，这种检验支持的是操作层面的因果信息性：轨迹在标签恢复中有用，并不严格证明每个自然语言步骤都忠实对应模型内部的真实计算机制。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### KPI 样本序列化与角色提示构造

利用 $\textsc{FormatKPIs}(x_i)$ 将数值窗口转换为文本表示，并构造同时包含格式化输入 $x$ 与真实标签 $y$ 的 Oracle 提示 $P_R$。论文动机实验中还将 KPI 窗口表示为逐特征摘要统计量，但摘录未给出完整字段模板。

<div class="method-step__io" markdown="1">

**输入**：原始有标签数据集 $\mathcal D=\{(x_i,y_i)\}_{i=1}^{N}$，其中 $x_i$ 是一个 KPI 时间窗口，$y_i$ 是对应类别标签。<br>
**输出**：适合语言模型读取的 KPI 文本 $x$、标签 $y$ 及 Oracle 提示 $P_R$。

</div>

**直观理解**：语言模型不能直接按普通表格算法处理整段无线网络遥测，因此先把 KPI 整理成文字化的问题描述。Oracle 同时看到题目和答案，以便集中生成与该标签相关的推理过程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Oracle 候选推理生成与结构过滤

Oracle 生成响应 $r=\textsc{Generate}(\mathcal M_{\theta_R},P_R)$，系统从中抽取思考轨迹 $t=\textsc{ExtractThinking}(r)$。若抽取结果为 $\bot$、轨迹长度 $|t|<\tau_{\min}$，或完整响应未通过 $\textsc{FormatOk}(r)$，该样本立即丢弃。

<div class="method-step__io" markdown="1">

**输入**：Oracle 提示 $P_R$、Oracle Reasoner $\mathcal M_{\theta_R}$ 和最小轨迹长度阈值 $\tau_{\min}$。<br>
**输出**：结构合法、可成功抽取且不短于阈值的候选推理轨迹 $t$。

</div>

**直观理解**：这一层先排除空白、过短、标签破损或模板失控的输出。它只检查轨迹“像不像一份完整解答”，尚不能判断解答是否真的足以推出正确类别。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Predictor 标签恢复验证

构造 $P_P=\textsc{PredictorPrompt}(x,t)$，其中轨迹被置于指定的思考标签内；Predictor 生成响应 $p$，再由 $\textsc{ParseLabel}(p)$ 得到 $\hat y$。仅当 $\hat y\neq\bot$ 且 $\hat y=y$ 时，将三元组 $(x,t,y)$ 加入 $\mathcal D'$。

<div class="method-step__io" markdown="1">

**输入**：原始格式化 KPI 输入 $x$、候选轨迹 $t$，以及看不到真实标签的 Predictor $\mathcal M_{\theta_P}$。<br>
**输出**：验证数据集 $\mathcal D'=\{(x,t,y):\hat y=y\}$，其中每条保留轨迹均通过标签恢复测试。

</div>

**直观理解**：Predictor 相当于闭卷复核者：它不知道标准答案，必须借助题目和 Oracle 的过程作答。答对说明轨迹至少包含了足以支持该标签的可利用信息，从而比仅仅语言流畅的事后解释更适合作为监督目标。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### LoRA 监督微调与顺序生成

冻结基础权重 $W_0$，只训练低秩矩阵 $A$ 与 $B$；标准语言模型损失施加在推理轨迹和标签的串接序列上，使模型学习条件分布 $p_\theta(t,y\mid x)$。训练后模型面对新 KPI 输入时先生成 $t$，再在该轨迹条件下生成并解析标签 $y$。

<div class="method-step__io" markdown="1">

**输入**：验证三元组数据集 $\mathcal D'$、预训练目标 SLM，以及固定的“推理轨迹在前、最终标签在后”输出模板。<br>
**输出**：能够稳定产生可解析的思考块与最终类别标签的 CRAFT 策略；该策略也可作为后续 GRPO 的初始化。

</div>

**直观理解**：不是让模型通过昂贵的试错奖励从零摸索格式与答案，而是让它模仿已经过筛的完整示范。LoRA 只调整少量附加参数，因此保留基础模型主体并降低训练成本。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### LoRA 参数化

$$
h=W_{0}x+\frac{\alpha}{r}BAx
$$

**符号说明**

- $x$：当前层的输入表示。
- $h$：加入低秩适配更新后的层输出。
- $W_0\in\mathbb R^{d\times k}$：冻结的预训练权重矩阵。
- $A\in\mathbb R^{r\times k}$：可训练的低秩下投影矩阵。
- $B\in\mathbb R^{d\times r}$：可训练的低秩上投影矩阵。
- $r$：适配更新的秩，满足远小于原权重矩阵的输入和输出维度。
- $\alpha$：控制低秩更新幅度的缩放因子。
- $d,k$：原权重矩阵的输出维度与输入维度。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项保留基础模型已有能力，第二项用两个小矩阵表达任务相关改动；因为只优化 $A$ 和 $B$，需要更新的参数远少于全参数微调。CRAFT 使用这一参数化学习验证后的轨迹—标签序列，而 LoRA 本身并不负责判断轨迹是否可靠。<br>
**原文位置**：式（1），Section II-A；Section III-B 指明 CRAFT 训练复用该式

</div>

</div>

<div class="equation-block" markdown="1">

#### 预解释式轨迹—标签联合生成分解

$$
p_{\theta}(t,y\mid x)=p_{\theta}(t\mid x)\,p_{\theta}(y\mid x,t)
$$

**符号说明**

- $x$：格式化后的 KPI 输入窗口。
- $t$：在最终标签之前生成的自然语言推理轨迹。
- $y$：任务的最终类别标签。
- $\theta$：目标语言模型的参数；在 CRAFT 微调中主要对应可训练的 LoRA 参数。
- $p_\theta(t\mid x)$：模型根据 KPI 输入生成推理轨迹的条件概率。
- $p_\theta(y\mid x,t)$：模型在输入与已生成轨迹条件下输出标签的条件概率。

<div class="equation-explanation" markdown="1">

**直观理解**：该分解明确规定生成顺序：先由输入产生轨迹，再利用输入和轨迹决定标签。与先固定预测再补写说明的事后解释不同，标签生成在计算顺序上位于轨迹之后；CRAFT 的验证步骤进一步要求保留轨迹能够支持正确标签恢复。<br>
**原文位置**：Section II-B；Section III-B 的轨迹与标签串接监督将该分解落实到 CRAFT

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文采用标准自回归语言建模损失，对每个验证三元组 $(x,t,y)\in\mathcal D'$ 中“推理轨迹 $t$ 后接标签 $y$”的目标序列进行监督微调。其优化含义是最大化条件联合似然 $p_\theta(t,y\mid x)$，等价地最小化目标 token 的逐步负对数似然；由于标签 token 位于轨迹之后，其预测上下文包含 $x$ 与 $t$。原文摘录没有给出单独编号的损失公式，也未明确说明是否屏蔽输入提示 token、是否对轨迹与标签采用不同权重，因此不应补造更具体的目标。与 GRPO 不同，CRAFT 主训练阶段不需要组采样、奖励归一化、裁剪策略目标或 KL 奖励项；可靠性主要由训练前的数据验证承担。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Oracle Reasoner**

Oracle Reasoner $\mathcal M_{\theta_R}$ 接收 KPI 输入 $x$ 与真实标签 $y$，生成面向该标签的候选轨迹。它与 Predictor 可由同一个底层基础模型实例化，但通过不同提示承担不同角色；其输出仍可能是事后合理化，因此不能未经验证直接作为训练数据。

> 直观理解：Oracle 的职责是高召回率地提出可能有用的解题过程，而不是独立证明过程可靠。给它答案可以绕过小模型不知道从哪里开始推理的冷启动困难，但也正因如此，后面必须安排盲测。

**2. Predictor 与因果信息性过滤器**

Predictor $\mathcal M_{\theta_P}$ 只接收 $(x,t)$，不接收真实标签 $y$，其输出经标签解析后得到 $\hat y$。结构过滤负责可抽取性、最小长度和模板合法性，标签恢复过滤负责条件 $\hat y=y$；两者联合决定三元组是否进入 $\mathcal D'$。

> 直观理解：格式检查防止模型只学到乱码或不完整模板，盲标签恢复则检查轨迹是否真的能帮助完成任务。需要注意，Predictor 同时看到 $x$ 和 $t$，因此若它仅凭 $x$ 就能答对，过滤器可能高估轨迹本身的贡献；摘录未报告反事实删除轨迹或扰动轨迹的额外验证。

**3. LoRA 轨迹—标签联合微调器**

目标 SLM 冻结原始矩阵 $W_0\in\mathbb R^{d\times k}$，插入秩为 $r$ 的可训练矩阵 $B\in\mathbb R^{d\times r}$ 与 $A\in\mathbb R^{r\times k}$，且 $r\ll\min(d,k)$。监督序列将轨迹放在标签之前，使标签 token 的预测能够条件化于已生成轨迹，而不是先给出决策再追加解释。

> 直观理解：该模块同时解决两个问题：用少量参数适配电信任务，并把“先想、后答”的顺序写入训练目标。真正决定预解释性质的是序列顺序和联合监督，而不仅是输出中出现了一个思考标签。

**训练与推理**

训练阶段首先遍历 $N$ 个标注样本：格式化 KPI，调用已知标签的 Oracle 生成轨迹，执行抽取、长度和格式过滤，再调用不知道标签的 Predictor 进行恢复验证。通过验证的 $(x,t,y)$ 构成 $\mathcal D'$，随后在目标 SLM 上冻结基础权重并用 LoRA 进行监督微调。Oracle 与 Predictor 是同一基础模型在不同提示下的两个逻辑角色，并非论文要求训练两个额外网络；数据准备完成后，部署只需要微调后的目标 SLM。

推理阶段输入新的 KPI 窗口，经与训练一致的序列化和指令模板送入 CRAFT 模型。模型先生成规定结构中的轨迹 $t$，再生成最终标签 $y$，系统从响应中解析标签；因此部署时不需要真实标签、Oracle 或 Predictor。论文还允许把所得 CRAFT 策略作为后续 GRPO 的暖启动策略，但这是可选延伸而非 CRAFT 获得基本能力所必需的步骤。

**复现信息**

复现时不可省略的设计包括：Oracle 必须同时接收 $x$ 和 $y$，Predictor 必须只能接收 $x$ 与 $t$；候选轨迹必须同时通过成功抽取、$|t|\geq\tau_{\min}$ 和完整格式检查；只有可解析预测满足 $\hat y=y$ 才能入库；监督输出必须把轨迹置于标签之前；参数更新采用 LoRA 而非全参数微调。论文在 TRACTOR 动机实验中使用 Qwen 3.5 2B，并以逐特征摘要统计量序列化 KPI；其他实验还涉及 Qwen 3.5 4B 与 Nemotron-3-Nano 4B，但这些模型选择不改变算法流程。

当前摘录未明确报告 $\tau_{\min}$ 的具体数值、Oracle 与 Predictor 的完整提示文本、解码温度或采样次数、LoRA 的秩 $r$ 与缩放系数 $\alpha$、学习率、批大小、训练轮数及验证集保留比例。因而这些参数不能从所给章节中推断；公平复现还应固定 KPI 序列化、输出标签集合和解析器，因为格式变化会直接影响样本过滤及解析失败率。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- TRACTOR：面向O-RAN近实时RIC网络切片流量分类。数据由非重叠的基站KPI窗口构成，每个窗口包含64个、采样间隔为250毫秒的样本，即16秒时间跨度；使用17个KPI的统计摘要表示，共1,575个窗口，标签为四类：eMBB、mMTC、URLLC和ctrl。它主要测试多分类网络切片场景中的前置推理能力。
- IC xApp：面向近实时RIC射频干扰检测。每个窗口由四个上行KPI（ul_snr、ul_mcs、ul_bitrate和ul_bler）的15个样本组成，共389个窗口，标签为clean或interference。它在KPI组成、时间粒度和类别数上不同于TRACTOR，用于检验方法是否只适用于特定的多分类任务。
- 两个数据集都采用固定的70%/15%/15%训练集、验证集和测试集划分，并对所有方法使用相同划分；因此方法间差异主要归因于训练范式，而不是数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

测试集中预测标签正确的样本比例，反映总体分类正确性。 （越高越好；但在类别分布不均衡时，单独使用可能掩盖少数类性能。）

</div>
<div class="metric-item" markdown="1">

**Macro-F1**

先分别计算每个类别的F1，再对类别做等权平均；F1综合精确率和召回率。 （越高越好；比Accuracy更能反映模型是否同时照顾所有类别。）

</div>
<div class="metric-item" markdown="1">

**Parse-failure rate（PF%）**

测试输出中无法提取有效标签的比例，衡量输出是否符合预先规定的机器可读格式。 （越低越好；PF%高时，即使文字中包含合理推理，也无法被网络控制系统可靠使用。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### TRACTOR上Qwen 3.5 4B的主要方法比较

<div class="result-value" markdown="1">

在该模型上，Zero Shot达到32.9% Accuracy和26.3% Macro-F1；SFT达到54.0% Accuracy和51.1% Macro-F1；直接GRPO达到35.0% Accuracy和28.0% Macro-F1；SFT+GRPO达到56.5% Accuracy和53.5% Macro-F1；CRAFT达到83.1% Accuracy和86.5% Macro-F1，且CRAFT的PF%为0%。

</div>

CRAFT相对于四种比较方法都明显提高了分类质量，同时保持完全可解析的输出。尤其是直接GRPO并未因优化组合奖励而获得可靠的分类性能，SFT+GRPO虽优于直接GRPO，却仍显著落后于CRAFT。这说明在该设置中，先构造可信的输入—推理轨迹—标签数据，再进行LoRA监督微调，比直接让强化学习同时学会格式、推理和分类更有效。但该结果只证明了所测数据集、模型和预算下的优势，不能单独证明CRAFT在所有电信任务或更大模型上都优于GRPO。

<div class="result-source" markdown="1">

来源：Section V, Main results；Table I

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

CRAFT itself, fine-tuned on the verified reasoning dataset for five epochs, reaches 83.1% accuracy and 86.5% macro-F1 with 0% parse failures and a 100% Think rate, training in maximum 5.8 hours when shared dataset-preparation time is included comfortably within the 12-hour budget.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### TRACTOR上三个目标SLM的跨模型表现

<div class="result-value" markdown="1">

CRAFT在三个目标模型上平均达到约81% Accuracy，并且PF%为0%；原文进一步指出，即使Qwen 3.5 2B和Nemotron-3-Nano 4B在其他训练范式下完全失效，CRAFT仍能在这两个模型上工作。

</div>

该结果主要检验CRAFT是否依赖某一个较强的目标模型。平均结果和小模型上的成功表明，验证后的推理数据可能为模型提供了较明确的格式、推理和标签联合监督，从而缓解冷启动。不过，原文在所给章节中没有提供三个模型各自的完整数值表，因此不能据此判断不同模型之间的精确差距，也不能排除模型规模、初始化或提示设计的影响。

<div class="result-source" markdown="1">

来源：Section V, Main results；Table I

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Averaged across all three SLMs, CRAFT attains approximately 81% accuracy with 0% parse failures, a result that holds even for Qwen 3.5 2B and Nemotron-3-Nano 4B, both of which collapse entirely under every other training paradigm.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### TRACTOR上的零样本与格式冷启动现象

<div class="result-value" markdown="1">

Qwen 3.5 4B的Zero Shot没有解析失败，但只有32.9% Accuracy和26.3% Macro-F1；Qwen 3.5 2B和Nemotron-3-Nano 4B则达到0% Accuracy和100% PF%。这表明无微调时，较小模型无法稳定遵循规定输出格式并完成分类。

</div>

该对照建立了后续训练方法的必要性：问题不仅是标签预测不准，还包括输出无法被解析。Qwen 3.5 4B的无解析失败并不等于其推理可靠，因为其分类分数仍然较低；相反，小模型的完全失败说明仅依靠提示不能解决格式和任务决策的同时学习。该观察支持论文关于冷启动障碍的解释，但它只描述所测三个模型，不能推出所有小语言模型都会出现相同程度的崩溃。

<div class="result-source" markdown="1">

来源：Section V, Main results；Table I

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Zero-shot prompting is weak and uneven across models: Qwen 3.5 4B reaches 32.9% accuracy and 26.3% macro-F1 with no parse failures, but Qwen 3.5 2B and Nemotron-3-Nano collapse entirely, with 0% accuracy and a 100% parse-failure rate, indicating that smaller models cannot reliably follow the required output format without any fine-tuning at all.

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

- Zero Shot：只使用带链式思维提示的基础模型，不进行微调，用来衡量模型原本的格式遵循和任务分类能力。
- SFT：仅在输入—标签对上进行普通监督微调，不监督推理轨迹，用来检验标签学习是否足以产生可审计的前置解释。
- GRPO：从基础模型直接进行Group Relative Policy Optimization，以等权组合奖励同时鼓励输出格式、推理存在性和标签准确率，用来直接测试强化学习式推理对电信任务的适应性。
- SFT+GRPO：先使用标签监督SFT，再用同一组合奖励进行GRPO，用来检验标签预训练是否能缓解GRPO的冷启动问题。

**实验想回答的问题**

- CRAFT能否在TRACTOR和IC xApp上同时提升分类质量与可解析的前置推理能力，克服直接GRPO、标签监督SFT及SFT+GRPO的冷启动问题？
- CRAFT初始化的模型在继续进行不同奖励函数的GRPO训练时是否保持稳定，并且是否比强化学习基线更节省训练时间与GPU能耗？

**实验实现**

实验比较三个目标小语言模型：Qwen 3.5 2B、Qwen 3.5 4B和Nemotron-3-Nano 4B；CRAFT离线数据生成阶段使用Gemma 4 31B作为Oracle Reasoner和Predictor，但该大模型不参与部署。所有LoRA适配器的秩为16、α为32、dropout为0，使用AdamW，学习率为$5\times10^{-6}$，线性预热比例为10%并随后线性衰减。GRPO每个提示采样4个候选输出，梯度累积步数为1。所有运行均在单张24GB显存的RTX 4090上进行，固定计算预算为12小时，并通过Unsloth完成训练和推理。TRACTOR主结果中的CRAFT训练五个epoch，并将共享的数据准备时间计入训练时间。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 从最佳CRAFT模型继续进行不同奖励函数的GRPO | 以TRACTOR上Qwen 3.5 4B的最佳CRAFT模型为起点，在剩余12小时预算内继续进行GRPO，比较三种奖励设置：平衡静态权重$w_{\mathrm{fmt}}=w_{\mathrm{think}}=w_{\mathrm{acc}}=0.5$；准确率优先权重$w_{\mathrm{acc}}=0.9$且$w_{\mathrm{fmt}}=w_{\mathrm{think}}=0.3$；以及每一步从$[0.2,1.0]$独立随机采样三个权重的动态设置。原文在所给章节中未明确报告三种设置下的具体Macro-F1和PF%数值。 | 该消融隔离的是CRAFT初始化的稳健性，而不是CRAFT与GRPO从零开始的差异。若三种奖励都保持高Macro-F1和低PF%，说明验证数据提供了较强的格式与决策先验，使后续奖励变化不容易破坏模型；尤其动态奖励是对稳定性的压力测试。但由于当前材料没有具体结果，不能把作者预期的稳定性表述为已由数值证实。 | Section IV-A, Ablation Studies<br><span class="experiment-evidence">We report macro-F1 and PF% for each, expecting CRAFT’s initialization to sustain high performance across all three schemes in a way that GRPO trained from scratch cannot.</span> |
| 迁移到IC xApp并比较能耗 | IC xApp消融在不同KPI、时间窗口和二分类标签上重复比较所有基线与CRAFT，并使用TRACTOR中表现最佳的SLM；能耗消融通过NVIDIA Management Library测量SFT、GRPO、SFT+GRPO和CRAFT训练期间的总GPU能耗，Zero Shot因不训练而排除。所给章节未明确报告IC xApp各方法的具体Macro-F1、PF%或各方法的具体焦耳数。 | IC xApp部分检验CRAFT的优势是否只是TRACTOR四分类任务的偶然现象；若CRAFT仍保持较高F1和较低PF%，则支持跨任务泛化。能耗部分则把训练时长优势转化为实际GPU电力成本比较，直接检验部署可持续性。由于当前摘录缺少图表数值，不能从设计描述本身推出方法在IC xApp上的胜负或确切节能比例。 | Section IV-A, Ablation Studies<br><span class="experiment-evidence">This lets us contextualize CRAFT’s wall-time advantage in terms of actual energy cost, which is directly relevant to the sustainability of deploying auditable reasoning models at scale in AI-RAN.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作提出通过数据构造和参数高效微调使语言模型先生成可验证推理轨迹再输出决策，核心涉及推理训练与对齐。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`1861112c25abd92118f66a999819aa2e534ef2deff9f7aed78ea207945d9bb9b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
