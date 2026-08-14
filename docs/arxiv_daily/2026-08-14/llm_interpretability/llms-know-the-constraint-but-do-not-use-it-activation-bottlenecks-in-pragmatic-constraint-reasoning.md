---
title: "[论文解读] LLMs Know the Constraint But Do Not Use It: Activation Bottlenecks in Pragmatic Constraint Reasoning"
description: "[arXiv 2608.12321][LLM 机制与可解释性] 原文未明确报告。"
arxiv_id: "2608.12321"
announcement_date: "2026-08-14"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:54:25.556071+00:00"
source_sha256: "0ceb2c4e75fd9206cf239541d1ec0fdb31e7314d1677bcc968f1b87b0729b339"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "大语言模型"
  - "语用约束推理"
  - "条件约束激活"
  - "启发式覆盖"
  - "线性探针"
  - "激活修补"
  - "保守偏差"
  - "机制可解释性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2608.12321</p>

# LLMs Know the Constraint But Do Not Use It: Activation Bottlenecks in Pragmatic Constraint Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Yubo Li, Ramayya Krishnan, Rema Padman</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Carnegie Mellon University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12321v1) · [PDF 下载](https://arxiv.org/pdf/2608.12321v1) · **关键词** 大语言模型, 语用约束推理, 条件约束激活, 启发式覆盖, 线性探针, 激活修补, 保守偏差, 机制可解释性<br>


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

本文属于大语言模型的语用约束推理与机制可解释性研究。其核心场景是：问题中存在一个显眼、容易套用的表面启发式线索，但正确决策还取决于未被直接说明的可行性前提，例如“去洗车店应步行还是开车”不仅取决于距离，还要求汽车到场。研究重点不是笼统判断模型答对多少，而是区分三种内部过程：模型是否在隐藏状态中表征了约束、该表征是否真正影响最终决策，以及人为移入相关激活后能否修复错误。这一区分对应“知道但未使用”的问题，也避免把始终选择谨慎答案造成的偶然正确误判为真正推理。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**启发式与隐式可行性约束**

启发式是依据距离、常识关联等醒目线索快速作答的规则；隐式可行性约束则是答案成立必须满足、但题面可能没有直说的前提。两者冲突时，模型必须覆盖表面线索，才能得到在现实中可执行的答案。

</div>
<div class="concept-item" markdown="1">

**线性探针**

线性探针是在模型某层隐藏表示上训练的简单分类器，用于检测某项信息能否被线性解码。探针准确率高只能说明表示中含有可读取信号，不能单独证明模型生成答案时因果性地使用了该信号。

</div>
<div class="concept-item" markdown="1">

**激活修补**

激活修补把一个参照输入在特定层或位置产生的内部激活移入目标输入，再观察答案倾向是否改变。若移入约束相关激活能修复目标错误，就为该表示参与决策提供比相关性探针更强的因果证据。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一组围绕同一决策构造的对照提示，其中关键变化是隐式约束是否存在，而醒目的表面启发式线索尽量保持可比；模型输出相应的行动或答案选择。作者以四元组诊断考察“条件约束激活”：首先检验约束信息是否可从内部表示中解码，即知识条件 $K$；其次检查这种可解码性是否在约束存在与不存在的提示间得到对称控制，即对称性条件 $S$；然后判断约束信号是否被路由到最终决策，即路由条件 $R$；最后通过供体激活修补测试错误是否可被因果性修复。该设置尤其要排除保守默认：模型若无论约束是否适用都选择更谨慎的答案，会在约束存在时看似正确，却会伤害约束移除后的最小对，因此不能算作真正的条件推理。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$K$**

Knowledge（知识）条件：约束是否已编码在模型内部表示中。

</div>
<div class="notation-item" markdown="1">

**$S$**

Symmetry（对称性）条件：对约束存在和约束缺失提示进行成对控制，避免把不对称数据线索误当作约束知识。

</div>
<div class="notation-item" markdown="1">

**$R$**

Routing（路由）条件：内部约束信号是否被传递并用于形成最终决策。

</div>
<div class="notation-item" markdown="1">

**$P$**

Repair（修复）条件的简写：从供体输入移入相关激活后，目标错误是否得到因果性修复；原文摘要以单词“Repair”表述，未明确规定该字母记号。

</div>

</div>

**直接相关的工作**

- **Heuristic Override Benchmark（Li et al., 2026）**: 该基准已在四类启发式和五类约束上展示语用推理失败，但仅凭行为正确率无法判断正确答案来自真实约束推断还是保守默认。本文在其问题基础上加入四元组最小对诊断及机制实验，以消除这一识别歧义。
- **线性探针与激活修补研究（Alain and Bengio, 2017；Meng et al., 2022；Wang et al., 2023a 等）**: 既有探针工作用于判断特征是否存在于隐藏状态，既有激活修补工作主要定位事实回忆或单步符号计算的因果回路。本文将二者结合用于条件性语用推理：探针回答模型是否“知道”，修补回答该知识是否能够被路由并改变决策。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型在回答日常问题时，可能被显眼的表面线索吸引，却忽略行动成立所需的隐含前提。例如，在“去附近洗车店应步行还是开车”的问题中，模型可能因距离近而建议步行，却没有把“洗车必须把车带到现场”纳入决策。这类回答语言流畅且表面合理，因此仅观察最终答案不容易判断模型究竟没有理解约束，还是理解了却没有使用。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于最终答案的行为准确率评估**：在包含不同启发式线索和隐含约束的题目上统计模型是否给出正确答案，并以总体或严格聚合准确率衡量其约束推理能力。这种方法能够显示错误是否普遍存在，但主要观察外部行为结果。
- **提示式务实推理干预**：通过修改提示，引导模型检查前提、解释推理过程或关注潜在约束，希望模型在生成答案前显式考虑行动的可行性。论文考察的四类提示策略覆盖了已有务实推理干预的主要类型。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 总体准确率会混淆真正的约束推断与保守默认：模型即使没有识别当前题目中的具体约束，也可能习惯性选择更谨慎的答案而碰巧正确。因此，行为得分无法区分“内部没有约束知识”和“已有知识未被路由到决策”这两种机制。
- 提示式干预可能只是提高模型提及前提或采取保守答案的倾向，而非修复约束信息进入最终决策的路径。作者报告所测提示干预均增加保守偏差，且尚未检验强化学习或微调式缓解方法，所以现有证据既没有展示真正的路由修复，也不能覆盖所有潜在干预。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种能把约束知识的内部表征、该表征在有无约束条件下的对称性、信息是否实际进入决策，以及通过因果干预能否修复答案区分开的诊断框架。因而，模型的隐含约束失败究竟源于“不知道”，还是源于“知道但没有调用”，仍未被行为准确率和普通提示实验可靠识别。

</div>
<div markdown="1"><span>核心问题</span>

当显眼的表面启发式线索与隐含可行性约束冲突时，大语言模型是否已经在隐藏状态中编码了该约束，却因激活路由瓶颈而未将其用于决策；进一步说，这种失败能否通过移植包含约束信息的内部激活得到因果性修复，而不是仅靠提示诱发更保守的回答？

</div>
<div markdown="1"><span>作者直觉</span>

如果约束信息能够从隐藏状态中稳定解码，但模型最终仍忽略它，那么问题更可能出在信息从内部表征流向答案的过程，而不是知识缺失。比较约束存在与不存在的配对情形，可以排除模型一概保守作答造成的假象；再把正确样本中的内部激活移植到失败样本中，观察决策是否随之改善，就能把“状态中含有信息”推进为“该信息对答案具有因果作用”的检验。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文把“模型是否知道隐藏约束”与“模型是否在恰当情境中使用该约束”拆开测量。输入是 HOB 基准中包含目标、显著表面线索和隐藏可行性约束 $C$ 的场景；每个场景被改写成 Active、Removed、Explicit 和 Salience Control 四联条件，并进一步构造五级提示阶梯。方法先用四联行为指标区分约束过度激活、激活不足与相对平衡的模型，再用提示干预、推理预算扫描和中介分析判断表面改进是否只是提高了“提及前置条件”的总体概率，最后在开放权重模型上以线性探针和激活修补依次检验 Knowledge、Symmetry、Routing、Repair，即 $K/S/R/P$ 四项条件。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造场景配对与显著性控制

按场景编号生成四联条件：Active 保留隐含且有效的 $C$；Removed 移除 $C$ 但保留表面线索；Explicit 在 Active 后明确写出 $C$；Salience Control 则在相同位置加入长度和句式匹配的中性陈述。中性填充句按实例编号确定性分配，以减少人工选择带来的混杂。

<div class="method-step__io" markdown="1">

**输入**：HOB 的 core100：100 个基础场景，覆盖 $4$ 类启发式与 $5$ 类约束形成的 $20$ 个组合；每个场景含目标、显著表面线索及隐藏约束 $C$。<br>
**输出**：每个基础场景对应一组可直接配对比较的 Active、Removed、Explicit 和 Salience Control 提示。

</div>

**直观理解**：四联设计相当于给同一道题做四个只改变关键因素的版本，因此能判断模型是识别了约束，还是只因提示更醒目、更长或更保守而改变答案。Removed 尤其重要，因为它能揭示模型在约束不存在时是否仍机械地选择“约束较重”的答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 行为诊断与提示特异性测量

计算各条件准确率、条件偏置指数 $\mathrm{CBI}$、显著性校正增益 $\mathrm{SalAdjGain}$、配对一致准确率 $\mathrm{PCA}$ 和条件激活分数 $\mathrm{CAS}$；提示阶梯的每一级 $L_i$ 还配有词汇、长度和启发式匹配的三个负对照。以 $\mathrm{CBI}>0.10$ 标记过度激活，以 $\mathrm{CBI}<-0.10$ 标记激活不足，并用提示准确率超过最佳匹配对照的差值判断增益是否真正来自约束信息。

<div class="method-step__io" markdown="1">

**输入**：14 个模型在四联条件上的重复作答，以及从 $L_0$ 到 $L_4$、由隐含 Active 逐步接近 Explicit 的五级提示阶梯。<br>
**输出**：模型级失败类型、对 Active 与 Removed 的配对表现，以及显式程度提升是否具有约束特异性的行为证据。

</div>

**直观理解**：只看 Active 正确率会把“真的理解约束”和“凡事保守”混为一谈；四联指标要求模型在有约束时使用它、无约束时放下它。提示阶梯及负对照则回答：模型变好究竟因为提示说中了约束，还是因为任何醒目的附加文字都会让它更谨慎。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 评估提示缓解与推理预算机制

对每个模型与策略计算二维缓解前沿：横轴为 ActiveGain，纵轴为 PairHarm；理想“修复角”要求 ActiveGain 为正且 PairHarm 非正。随后检测回答是否提及规范化隐藏约束的内容词，估计干预 $\to$ 前置条件提及 $\to$ 正确性的中介链及 mediated correctness share。

<div class="method-step__io" markdown="1">

**输入**：零前缀基线、思维链、前置条件列举、目标分解和反事实检查四种单提示前缀，以及四个思考型模型在 $256$、$1024$、$4096$、$16384$ 个思考 token 预算下的输出。<br>
**输出**：每种提示策略或推理预算是否选择性修复 Active、是否伤害 Removed，以及其效果有多大比例经由“提及前置条件”这一表面行为实现。

</div>

**直观理解**：真正的修复应只在约束适用时提高正确率，而不能让模型在 Removed 中也变得更保守。中介分析用于检查不同推理提示是否只是用不同说法触发了同一个动作，即不分情境地谈论前置条件。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 线性探针与因果激活修补

在每个 Transformer 层训练逻辑回归探针区分 Active 与 Removed，以分场景五折交叉验证测试 $K$；比较两类平衡子集上的准确率差测试 $S$；计算探针投影与正确答案相对捷径答案的 logit 差之间的 Spearman 相关测试 $R$。再在最佳探针层 $\ell^\star$ 用 Explicit 的最终 token 隐藏状态覆盖受体对应状态，重算正确答案与捷径答案的对数概率差，以 Active 上的改善和 Removed 上的副作用共同测试 $P$。

<div class="method-step__io" markdown="1">

**输入**：Qwen3-14B 与 GPT-OSS-20B 对 core100 四联提示逐层产生的最终输入 token 残差隐藏状态，以及 Explicit 供体与 Active 或 Removed 受体提示。<br>
**输出**：约束信息是否可解码、是否在配对条件中对称存在、是否被决策过程读取，以及直接注入该表示能否选择性修复答案的 $K/S/R/P$ 证据。

</div>

**直观理解**：探针像一个旁观者，检查模型内部是否已经保存“约束适用”的信号；相关性再检查模型自己的答案模块是否读取了这个信号。激活修补则把明确提示中的内部状态移植到失败样本中：若答案随之改善且 Removed 不被误伤，才说明该状态对决策具有选择性的因果作用。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 条件行为诊断指标

$$
\mathrm{CBI}=\mathrm{Acc}_{\textsc{A}}-\mathrm{Acc}_{\textsc{R}},\qquad \mathrm{SalAdjGain}=\mathrm{Acc}_{\textsc{E}}-\mathrm{Acc}_{\textsc{SC}},\qquad \mathrm{PCA}=\frac{1}{|S|}\sum_{s\in S}\widehat{\mathrm{Acc}}_{\textsc{A}}(s)\widehat{\mathrm{Acc}}_{\textsc{R}}(s),\qquad \mathrm{CAS}=\mathrm{PCA}(1-|\mathrm{CBI}|)
$$

**符号说明**

- $\mathrm{Acc}_{\textsc{A}}$：Active 条件的总体准确率。
- $\mathrm{Acc}_{\textsc{R}}$：Removed 条件的总体准确率。
- $\mathrm{Acc}_{\textsc{E}}$：Explicit 条件的总体准确率。
- $\mathrm{Acc}_{\textsc{SC}}$：Salience Control 条件的总体准确率。
- $S$：全部基础场景的集合。
- $s$：一个基础场景。
- $\widehat{\mathrm{Acc}}_{\textsc{A}}(s)$：场景 $s$ 在 Active 条件下由重复试验估计的准确率。
- $\widehat{\mathrm{Acc}}_{\textsc{R}}(s)$：场景 $s$ 在 Removed 条件下由重复试验估计的准确率。
- $\mathrm{CBI}$：Conditional Bias Index；正值表示相对偏向约束型答案，负值表示约束需要启用时反而表现较差。
- $\mathrm{SalAdjGain}$：显式约束相对长度和句式匹配中性填充句带来的特异性准确率增益。
- $\mathrm{PCA}$：Pair-Consistent Accuracy；要求同一场景在 Active 与 Removed 两个条件中都表现正确的配对指标。
- $\mathrm{CAS}$：Conditional Activation Score；在配对一致性基础上惩罚绝对条件偏置。

<div class="equation-explanation" markdown="1">

**直观理解**：$\mathrm{CBI}$ 判断模型的错误偏向哪一侧，但单独使用它可能掩盖“两边都很差”的情况；$\mathrm{PCA}$ 要求同一场景的两个反事实版本都答对，$\mathrm{CAS}$ 再惩罚过度激活或激活不足。$\mathrm{SalAdjGain}$ 则从 Explicit 增益中扣除单纯增加醒目文本所能带来的效果。<br>
**原文位置**：第 3.3 节 Behavioral Metrics

</div>

</div>

<div class="equation-block" markdown="1">

#### 缓解前沿与激活修补判据

$$
\textsc{ActiveGain}=\mathrm{Acc}^{\mathrm{strat}}_{\textsc{A}}-\mathrm{Acc}^{\mathrm{zero}}_{\textsc{A}},\qquad \textsc{PairHarm}=\mathrm{CBI}^{\mathrm{strat}}-\mathrm{CBI}^{\mathrm{zero}};\qquad \Delta^{c}=g^{c}_{\mathrm{patched}}-g^{c}_{\mathrm{baseline}},\quad g=\log p(y_{\mathrm{gold}}\mid x)-\log p(y_{\mathrm{shortcut}}\mid x)
$$

**符号说明**

- $\mathrm{Acc}^{\mathrm{strat}}_{\textsc{A}}$：采用某一提示策略时的 Active 准确率。
- $\mathrm{Acc}^{\mathrm{zero}}_{\textsc{A}}$：不添加策略前缀时的 Active 基线准确率。
- $\mathrm{CBI}^{\mathrm{strat}}$：采用提示策略时的条件偏置指数。
- $\mathrm{CBI}^{\mathrm{zero}}$：零前缀基线的条件偏置指数。
- $x$：输入提示，即某一场景的 Active 或 Removed 版本。
- $y_{\mathrm{gold}}$：当前条件下的正确答案。
- $y_{\mathrm{shortcut}}$：由显著表面线索直接诱导的捷径答案。
- $g$：正确答案相对捷径答案的对数概率差；越大表示决策越支持正确答案。
- $\Delta^{c}$：条件 $c$ 中修补后与基线之间的决策差变化，$c$ 可为 Active 或 Removed。

<div class="equation-explanation" markdown="1">

**直观理解**：前两项把提示策略的收益与副作用放在同一坐标系中：理想方法应满足 $\textsc{ActiveGain}>0$ 且 $\textsc{PairHarm}\leq 0$。修补量 $\Delta^c$ 则比较移植 Explicit 隐藏状态前后，模型对正确答案相对捷径答案的支持变化；论文规定 $\Delta^{\mathrm{Active}}>1.0$ nat 且 $|\Delta^{\mathrm{Removed}}|\leq1.0$ nat 才算具有选择性的 Repair。<br>
**原文位置**：第 3.4 节 Mitigation Frontier 与第 3.8 节 Activation Patching；$g$ 的展开依据该节所述 gold–shortcut log-probability gap

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文不训练新的生成模型，也没有端到端任务损失。唯一的监督优化是逐层逻辑回归探针：以隐藏状态为输入、Active 与 Removed 标签为目标，使用 liblinear、正则参数 $C=1$ 和逐特征标准化进行拟合；其用途是测量约束信息是否线性可解码，而不是提升基础模型能力。激活修补属于推理期因果干预，不通过梯度更新模型权重；提示策略和推理预算扫描同样只改变输入或推理配置。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 四联条件诊断与显著性控制**

核心实验单位不是孤立样本，而是按同一场景编号配对的 Active、Removed、Explicit、Salience Control。Removed 隔离“约束是否适用”，Explicit 提供明确约束信号，Salience Control 用长度桶和句式匹配的中性句隔离非特异性的显著性效应；五级提示阶梯又在每级加入 $\mathrm{ctrl}_{\mathrm{lex}}$、$\mathrm{ctrl}_{\mathrm{len}}$、$\mathrm{ctrl}_{\mathrm{heur}}$ 三种负对照。

> 直观理解：该模块建立了论文最关键的反事实：同一模型不能只在“需要约束”的版本上答对，还必须在“不需要约束”的版本上恢复使用表面线索。这样才能把条件推理能力与普遍保守倾向区分开。

**2. 二维缓解前沿与中介分析**

缓解前沿同时报告 $\textsc{ActiveGain}$ 和 $\textsc{PairHarm}$，避免把 Active 的局部增益误判为整体修复。中介变量 $m$ 表示输出是否通过与规范化隐藏约束的内容词重叠而提及前置条件，并比较 $\Pr(c\mid m)$、$\Pr(c\mid\neg m)$、$\Pr(m)$ 及正确答案中可归因于提及轨迹的比例。

> 直观理解：某种提示即使让 Active 更准确，也可能只是把所有回答都推向保守选项；二维前沿会把这种代价显示出来。中介分析进一步说明提示为何有效，而不仅仅说明它是否有效。

**3. 探针与激活修补的表示到决策检验**

探针读取每层最终输入 token 的 post-block residual state，并以场景分组五折交叉验证避免同一场景的四个版本跨训练集与测试集泄漏。最佳层随后用于测量探针方向与决策 logit 差的相关性，并执行 Explicit 到 Active 或 Removed 的单层、单位置状态覆盖；阈值分别为 $\theta_K=0.80$、$\theta_S=0.05$、$\theta_R=0.30$ 和 $\theta_P=1.0$ nat。

> 直观理解：可解码不等于被模型使用，所以方法分成“读得出来”“与答案联动”和“移植后能改变答案”三个强度递增的检验。场景分组交叉验证也防止探针仅靠记住同一题的措辞差异取得虚高成绩。

**训练与推理**

行为推理阶段，对 core100 的每个四联条件独立调用模型并判定答案正确性；API 模型每个“模型、条件”单元运行 $T=10$ 次，本地 GPU 模型运行 $T=8$ 次，预算扫描运行 $T=4$ 次。随后聚合条件准确率与配对指标，并在提示阶梯中把每个真实提示级别同三个匹配负对照比较。缓解实验只添加一个策略前缀，其余条件保持不变；预算实验仅改变思考 token 上限。中介分析从生成轨迹中检测约束内容词是否出现，再估计提及与正确性的条件概率。

机制分析阶段，先冻结 Qwen3-14B 与 GPT-OSS-20B，在全部 Transformer 层缓存每个四联输入最终 token 的 post-block residual hidden state。每层各训练一个 Active/Removed 逻辑回归探针，按场景编号做五折划分，使同一场景的四个版本始终位于同一折；选择交叉验证准确率最高的层 $\ell^\star$。在该层依次检查探针准确率是否超过 $0.80$、条件子集准确率差是否不超过 $0.05$、探针投影与 gold–shortcut 决策差的 Spearman 相关是否超过 $0.30$。最后对每个场景先运行 Explicit 供体并缓存 $h^{\mathrm{donor}}_{\ell^\star}$，再运行 Active 或 Removed 受体，通过 forward hook 覆盖该层最终 token 的输出，比较修补前后的决策差；只有 Active 明显改善且 Removed 基本不变，才满足 Repair。

**复现信息**

数据覆盖 core100 的 $100$ 个场景和全部 $20$ 个“启发式×约束”组合。14 个模型用于行为评估；隐藏状态实验集中在 Qwen3-14B 与 GPT-OSS-20B，因为二者是开放权重模型且代表不同的行为失败类型。四联条件必须按场景配对统计，探针交叉验证也必须按场景分组，否则同一场景的近似改写可能同时进入训练折与测试折并造成泄漏。Salience Control 的中性句需按长度桶和句式匹配，并按实例编号确定性分配；提示阶梯每级需保留词汇、长度和启发式三个负对照。激活修补使用最佳探针层、最终输入 token 和 Explicit 供体；供体打乱、层扫描及位置扫描被列为附录控制，公平复现时应保留这些检验。论文同时说明 API 数据采集于 2026 年 5 月，闭源模型可能在之后被供应商更新，因此模型标识与采集时间是解释复现差异所必需的信息。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 四元组行为诊断任务：通过成对的“约束存在”与“约束不存在”提示区分约束知识、跨条件对称性和决策路由；覆盖的具体样本来源、任务规模及数据划分在所给节选中未明确报告。
- 开放权重模型的内部表征探测任务：用于检验模型激活中能否解码出隐含约束；所给材料仅说明涉及两个开放权重模型，具体模型名称、层级样本规模和训练测试划分未明确报告。
- 提示干预与激活修补评测：分别测试外部提示能否实现无偏的行为修复，以及供体激活能否因果性地恢复约束使用；具体干预集合、样本规模和划分未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**四元组诊断条件**

分别检查知识存在（Knowledge）、约束存在与不存在条件之间的对称性（Symmetry）、约束是否进入最终决策（Routing），以及供体激活能否完成修复（Repair）。它用于拆分聚合准确率中混杂的真实约束推理与保守默认。 （同时满足四项条件更好；仅提高表面准确率不足以证明模型真正进行了条件性约束推理。）

</div>
<div class="metric-item" markdown="1">

**探针解码准确率**

衡量从模型内部激活中预测隐含约束是否存在的能力，用于检验约束信息是否已经被内部编码。 （越高越好，因为更高准确率表示内部表征包含更多可线性或由指定探针读取的约束信息；但它本身不证明模型在生成答案时使用了该信息。）

</div>
<div class="metric-item" markdown="1">

**激活修补效应（nats）**

衡量注入供体激活后，目标决策相关对数概率或对数优势发生的变化；所给材料没有给出其完整计算公式。 （朝正确约束决策方向的正向变化越大越好；接近零或负值表示修补没有实现预期的因果性恢复。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 14个模型上的四元组行为诊断

<div class="result-value" markdown="1">

作者报告该诊断揭示了两类失败模式，但所给材料未提供各模型的分类、分项得分或统计不确定性。

</div>

这说明表面上相似的错误可能来自不同机制，不能只用总体正确率概括。不过，“存在两类失败模式”仍是作者基于其诊断框架作出的归类；当前证据不足以判断两类模式在不同模型中的普遍程度。

<div class="result-source" markdown="1">

来源：Abstract；第4节节选说明行为结果位于§4.1，知识、对称性与路由结果位于§4.5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A quartet diagnostic over 14 models reveals two failure modes; probes on two open weights decode the constraint above $88\%$, yet activation patching repairs one ($+6.4$ nats) and not the other ($-0.07$).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 两个开放权重模型的约束探测与激活修补

<div class="result-value" markdown="1">

两个模型的探针约束解码准确率均超过$88\%$；但激活修补对其中一个模型产生$+6.4$ nats的修复效应，对另一个模型为$-0.07$ nats。

</div>

高探针准确率支持“模型内部含有可读出的约束信息”，而截然不同的修补效果表明，可解码性不等于该信息能被因果地接入决策。正向$+6.4$ nats支持一个模型存在可修复的路由瓶颈；$-0.07$ nats则表示同一修补思路在另一模型上没有奏效，但不能据此证明后者完全没有约束知识，因为修补位置、供体选择或表征格式不匹配也可能导致失败。

<div class="result-source" markdown="1">

来源：Abstract；激活修补结果位于§4.6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A quartet diagnostic over 14 models reveals two failure modes; probes on two open weights decode the constraint above $88\%$, yet activation patching repairs one ($+6.4$ nats) and not the other ($-0.07$).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 提示干预的缓解前沿

<div class="result-value" markdown="1">

作者报告没有任何提示干预到达理想的“修复角点”；所有提示干预都通过“提及先决条件”这一中介路径增加了保守偏差。

</div>

理想干预应当只在约束确实存在时纠正答案，并在约束不存在时保持正常决策。结果表明，提示可能主要让模型更频繁地谈论或假定先决条件，而非学会按条件调用约束，因此表面改善可能伴随更多误拒绝或过度谨慎。该结论依赖论文对“修复角点”、保守偏差和中介效应的具体定义，所给材料未提供数值效应量。

<div class="result-source" markdown="1">

来源：Abstract；所给第4节节选未标明提示干预结果的具体小节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On a mitigation frontier, no prompted intervention reaches the repair corner: all inflate conservative bias through a single mediation pathway -- prerequisite mention.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给来源仅包含摘要和第4节开头的截断片段，未提供完整数据集、模型名单、样本规模、误差条、显著性检验及表格内容；因此实验结果只能按摘要陈述，无法独立核验稳健性与可重复性。
- 机制证据仅明确涉及两个开放权重模型，而且其中一个激活修补失败；这既限制了“路由瓶颈”结论的跨模型外推，也留下修补位置、供体激活或表征不匹配等替代解释。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 未干预的原始模型行为：作为提示干预和激活修补的参照，用于判断性能变化是否来自干预。
- 约束不存在的配对条件：与约束存在条件共同检验对称性，并识别模型是否只是无条件采用保守答案。
- 提示式干预：与内部激活修补形成比较，用于检验仅靠自然语言提醒能否达到“正确修复且不增加保守偏差”的目标。
- 两个开放权重模型之间的修补结果比较：用于判断“约束可被探针解码”是否足以保证该表征能够通过激活替换被路由到决策。具体模型名称未明确报告。

**实验想回答的问题**

- 当显著的表面线索与隐含的可行性约束冲突时，模型失败究竟源于没有表征约束知识，还是虽已表征却未将其路由到最终决策？
- 激活修补和提示干预能否恢复约束的条件性使用，同时避免把模型推向不区分约束是否存在的保守默认行为？

**实验实现**

实验按知识、对称性、路由和修补四个条件组织。行为层面在14个模型上运行四元组诊断；机制层面选择两个开放权重模型训练或评估约束探针，并使用供体激活进行激活修补；干预层面比较多种提示方案在“修复约束存在条件”和“避免约束不存在条件中的保守偏差”之间的位置。所给节选未报告具体模型名称、提示模板、采样参数、探针结构、修补层与位置、重复次数、置信区间或显著性检验，因此这些实现细节仍需对照论文完整第4节核验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 最关键的对照案例是两个均能以超过$88\%$准确率解码约束的开放权重模型：一个可通过激活修补获得$+6.4$ nats改善，另一个为$-0.07$ nats。该对照把“内部存在信息”与“信息可被路由并因果影响答案”分开，但所给材料未提供具体输入、输出和逐例轨迹。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper uses probing and activation patching to identify an internal routing bottleneck responsible for LLM constraint-reasoning failures.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`0ceb2c4e75fd9206cf239541d1ec0fdb31e7314d1677bcc968f1b87b0729b339`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
