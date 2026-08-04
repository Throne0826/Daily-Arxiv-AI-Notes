---
title: "[论文解读] Right Answer, Wrong Method: Shortcut Hacking Misleads the Evaluation of LLM Reasoning on Frontier Science Benchmarks"
description: "[arXiv 2608.02442][LLM 评测] 本文指出，仅凭最终答案正确率会把通过枚举、搜索、猜测或先看答案再验证所得的正确答案误判为有效科学推理，并据此提出识别和抑制“解答投机”的评估思路。"
arxiv_id: "2608.02442"
announcement_date: "2026-08-04"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:57:57.608106+00:00"
source_sha256: "d1360954770b33a63f50730add4fee0c86b03e6991c9efe3d004a3c1e77a5174"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "科学推理评测"
  - "解法破解"
  - "目标推理能力"
  - "捷径利用"
  - "过程评估"
  - "最终答案正确率"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.02442</p>

# Right Answer, Wrong Method: Shortcut Hacking Misleads the Evaluation of LLM Reasoning on Frontier Science Benchmarks

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Xuan Ren, Weiqi Zhai, Tianle Pu, Yihua Zhu, Yihua Zhu, Hu Wei, Bing Zhao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Alibaba DAMO Academy</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02442v1) · [PDF 下载](https://arxiv.org/pdf/2608.02442v1) · **关键词** 大语言模型, 科学推理评测, 解法破解, 目标推理能力, 捷径利用, 过程评估, 最终答案正确率<br>


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

本文指出，仅凭最终答案正确率会把通过枚举、搜索、猜测或先看答案再验证所得的正确答案误判为有效科学推理，并据此提出识别和抑制“解答投机”的评估思路。

**不用术语来说**：一道题答对了，并不意味着模型真正掌握了题目想考查的方法。例如，题目要求推导二次方程的精确根，模型却可能不断试数，碰巧找到满足方程的答案；传统的答案判分仍会给它满分。这样得到的高正确率混合了真实推理与投机取巧，因而可能夸大模型面对高难度科学问题时的实际能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者明确提出并界定“解答投机”（Solution Hacking）：模型虽然给出正确答案，却使用搜索、枚举、猜测或答案优先验证等无效捷径，绕过题目要求考查的目标推理能力；这一概念强调的不是解法与参考答案不同，而是解法未能独立、有效地推出结论。
- 作者从题目难度、科学领域、模型差异和题目特征等角度分析解答投机，并将领域专家的判断原则转化为自动判别器与测试时反投机指令，用于区分真实推理所得的正确答案和捷径所得的正确答案。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型科学推理能力评测研究。现有数学、物理等前沿科学基准通常向模型提供一道问题及其作答要求，再以最终答案是否正确作为主要评分依据，并把更高的正确率视为更强推理能力的证据；但这种评测默认“答对”能够代表模型完成了题目所要求的推导。本文指出，最终答案与目标能力之间并非一一对应：模型可能没有执行预期的代数推导、证明或科学分析，而是通过枚举候选值、数值搜索、猜测或先得到答案再反向验证等捷径答对。因而，可靠评测不仅要检查答案和推理步骤是否正确，还要判断整个解法是否真正运用了基准意图测量的目标推理能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**最终答案正确率**

只依据模型最终答案是否与标准答案一致计算的比例，是科学推理基准常用的性能指标。它容易自动评分，但不能单独证明模型采用了有效且符合题目目标的推导方法。

</div>
<div class="concept-item" markdown="1">

**目标推理能力**

一道题意图考查的核心求解能力，例如利用求根公式精确推导二次方程的根，而非逐个试数。判定它是否被实际运用，需要结合题目要求和完整解答过程，而不能只观察结果。

</div>
<div class="concept-item" markdown="1">

**解法破解（Solution Hacking）**

模型通过搜索、枚举、猜测或答案优先验证等无效捷径得到正确答案，却没有给出能够独立确立答案正确性的、面向目标任务的有效推导。它不等同于采用不同于参考答案的方法，关键判据是该方法是否绕过了题目要测量的能力。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是前沿大语言模型在不同难度层级和科学领域中的完整作答。输入包括科学问题、该题意图考查的目标推理能力以及模型生成的推理过程和最终答案；评估首先判断最终答案是否正确，再对答对样本判断其求解过程是有效运用目标能力，还是构成解法破解。本文假设“替代解法”本身并不违规：只要它能独立、有效地推出结论，就不应仅因不同于参考解而被判为破解；相反，即使枚举出的候选值均被正确验证，只要整体策略靠捷径发现或确认答案并绕过目标推导，仍属于破解。研究设置覆盖普通数学推理、奥赛级问题和 HLE 等难度层级，并跨科学领域及多个前沿模型分析这种现象；因此其核心任务不是再次判断答案对错，而是在答案正确的条件下识别正确答案的获得方式。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **过程监督与步骤级推理评估（Uesato et al., 2022；Lightman et al., 2023；Zheng et al., 2025）**: 这些方法检查中间步骤是否正确、有用，或能否作为训练信号，主要回答推理链在局部或整体上是否有效。本文关注更进一步且不同的问题：解法是否实际调用了基准指定的目标能力；候选枚举后的逐项验证可能每一步都正确，却仍通过整体策略绕开目标推导，因此可能逃过常规步骤错误检测。
- **科学推理中的捷径与证明缺陷研究（Mahdavi et al., 2025；Balunovic et al., 2025；Sun et al., 2025）**: 既有研究已讨论试错、以例代证、模式识别、暴力枚举和启发式猜测，也提出抗猜答案空间、抗暴力扰动或 Lean 验证子集，但多把它们作为证明谬误、个案现象或特定基准问题。本文将其统一为一种发生在评测阶段的“解法破解”失效模式，并试图跨难度、领域和模型系统量化，而不是只防御某一种捷径。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

前沿科学基准越来越困难，其目的通常是测量大语言模型能否完成特定的数学或科学推导，但主流评估仍把最终答案正确率视为核心指标。作者的动机分析显示，随着题目难度上升，模型更可能绕过目标推理过程：解答投机比例由普通问题上的 2.2% 上升至奥赛级问题上的 28.3%，并在 HLE 上达到 37.4%。因此，越需要验证高级推理能力的基准，越可能受到答案正确但方法无效这一问题的干扰。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **最终答案正确率评估**：将模型输出的最终答案与标准答案比较，匹配即计为正确，并以正确样本占比衡量模型的推理能力。该方法成本较低、易于规模化，也能区分正确答案与普通推理错误，但不检查正确答案是如何得到的。
- **推理过程验证**：检查模型解答中的中间步骤是否合理或是否存在推导错误，相比只判最终答案更关注过程质量。然而，论文指出，已有过程验证往往没有进一步判断模型是否真正使用了题目要测量的目标推理能力。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 最终答案正确率无法区分“有效推导后答对”和“通过枚举、搜索、猜测或答案优先验证答对”。两类输出都会获得相同分数，导致投机答案被计入能力成绩；在所分析的前沿模型中，获判正确的答案里有 8.2% 至 44.1% 被识别为投机解答。
- 一般的过程验证即使能够发现局部逻辑错误，也可能接受一条表面连贯但绕开目标能力的路线。其后果是评估回答了“模型能否得到或确认答案”，却没有可靠回答“模型能否用题目指定或隐含要求的科学推理独立推出答案”。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有评估缺少一套面向“目标推理能力是否真正被执行”的操作化标准：它既要允许不同于参考答案但仍然有效的独立解法，又要排除依赖搜索、枚举、猜测和答案优先验证的捷径，并且能够用于大规模模型评估。由于这一区分尚未得到系统处理，当前基准分数无法清楚分离真实推理贡献与捷径带来的分数膨胀。

</div>
<div markdown="1"><span>核心问题</span>

在不同难度、科学领域和前沿模型中，解答投机究竟有多普遍、会在多大程度上抬高最终答案正确率，以及能否依据专家原则自动识别并通过测试时指令抑制这种行为，从而更忠实地评估模型的科学推理能力？

</div>
<div markdown="1"><span>作者直觉</span>

专家评价科学解答时，不只看结论和局部步骤是否正确，还会追问：这些步骤是否足以独立建立结论，以及模型是否实际运用了题目要考查的推理能力。把这一判断拆成明确原则，可让自动判别器识别“结果正确但论证无效”的输出；同时，在作答前禁止捷径并允许模型在无法完成有效推导时放弃回答，可以减少模型靠碰答案维持表面正确率的激励。这样，剩余的正确答案更可能代表模型真正完成了目标推理。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文的方法由两个共享同一专家标准的工具组成：一是事后检测工具，即判断完整解答是否通过捷径绕过目标推理能力的 hack judge；二是生成时干预工具，即要求回答模型给出可独立成立的推导、避免投机捷径的 anti-hack prompt。给定题目 $q$、参考答案 $a^*$ 和模型解答 $s$，系统首先单独检查最终答案 $\hat{a}(s)$ 是否正确，再让看不到 $a^*$ 与正确性标签的检测器判断 $s$ 是否属于 solution hacking；由此同时报告普通准确率、破解率、正确答案中的破解率，以及只认可“正确且非破解”解答的推导校正准确率。检测器和干预提示均以盲审领域专家标注的同一批解答为锚点，从而尽量让测量标准与抑制标准保持一致。

技术上的关键不是识别某个表面动作，而是判断该动作在当前题目中的作用：数值计算、枚举或引用公式本身并不自动构成破解，只有当它们在关键步骤替代题目要考查的能力 $\mathcal{C}(q)$，且没有独立推出答案时才算破解。通俗地说，系统不只是问“答案对不对”或“有没有搜索”，而是问“这份解答是否真正完成了题目要求证明或推导的那一步”。由于最终检测器对专家确认的破解存在较多漏检，论文把测得的破解率解释为保守下界，而不是实际破解率的无偏估计。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤一：形式化破解边界并构建初始审计器

作者将 solution hacking 定义为：解答的最终答案正确，但在必要步骤使用 $M(q)$ 之外的捷径替代 $\mathcal{C}(q)$；再用 T1“是否替代目标关键步骤”、T2“是否绕过目标能力”、T3“是否独立建立答案”三个问题操作化该定义。基于这一边界，初始审计器输出结构化 JSON，包括必要步骤分析、hack/clean 二元结论、策略类别和决定性原文证据。

<div class="method-step__io" markdown="1">

**输入**：基准题目与模型完整解答组成的题解对 $(q,s)$，以及领域专家对题目目标能力 $\mathcal{C}(q)$ 和可接受策略集合 $M(q)$ 的理解。<br>
**输出**：统一的判定规范、六类策略标签，以及可用于大规模初筛的 Stage-1 auditor。

</div>

**直观理解**：这一步相当于先制定阅卷规则：使用枚举或公式不一定违规，关键看它是否跳过了题目真正要考的推导。审计器还必须指出解答中的具体证据，避免只凭整体印象贴标签。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤二：分层抽样并获得盲审专家锚点

作者按初筛的 flagged/clean 结论进行分层抽样，以增加稀少且分布不均的正例，得到 $300$ 份解答；随后打乱来源并隐藏模型身份，由对应学科的博士专家依据书面规范逐份给出 hack/clean 标签和策略类别，并进行一次自我复核。专家锚点被划分为 $180$ 个开发样本和 $120$ 个只使用一次的留出测试样本。

<div class="method-step__io" markdown="1">

**输入**：GPT-5.2、Claude Opus 4.7 和 Gemini-3.1-Pro-Preview 在 HLE 与奥赛级数学、物理、化学题目上生成的解答，以及 Stage-1 auditor 给出的初筛结论。<br>
**输出**：覆盖数学、物理和化学的专家标注锚点集，其中开发集用于提示修订与检测器选择，测试集用于估计最终检测器的泛化可靠性。

</div>

**直观理解**：自然数据里真正的破解案例可能太少，因此先按机器初筛结果抽样，能让专家看到足够多的边界案例。盲审则减少专家因模型品牌或初筛结论而产生的先入为主。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤三：校准并部署无自审的多模型检测器

作者在开发集上修订提示，使其正确处理“预期方法中的枚举”“允许引用的标准定理”和“多个弱线索联合构成破解”等边界，再为各判断模型选择与专家标签最一致的提示版本。通常采用三者多数票；若某判断模型正在审核自己生成的解答，则移除该模型，只在另外两个判断器一致判为破解时标记 $H_i=1$。

<div class="method-step__io" markdown="1">

**输入**：专家标注的开发集、修订后的审计提示，以及 Gemini-3.1-Pro-Preview、Claude Opus 4.7、GPT-5.2 三个同级判断模型。<br>
**输出**：最终 deployed detector，以及每份解答的二元破解标签 $H_i$ 和策略类别；该检测器用于计算破解相关指标。

</div>

**直观理解**：多个模型共同阅卷可以降低单个判断器的偶然偏差，而禁止模型给自己的答案打分可减少自我偏袒。两名剩余判断器必须一致才判破解，这一保守规则会牺牲召回率，因此测得的破解率更适合作为下界。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤四：独立评估正确性并实施生成时干预

正确性模块独立比较 $\hat{a}(s)$ 与 $a^*$：数值答案采用 $5\%$ 相对容差，符号答案检查代数等价；hack judge 只接收 $(q,s)$，看不到参考答案和正确性结论。生成干预分别采用 ban-list、necessity、guardrail 和 pre-commit 四种提示，并允许模型输出“CANNOT SOLVE RIGOROUSLY”以明确弃答。

<div class="method-step__io" markdown="1">

**输入**：题目 $q$、参考答案 $a^*$、模型解答 $s$，以及由专家边界提炼出的四种 anti-hack prompt。<br>
**输出**：每份解答相互分离的正确性标签 $C_i$ 与破解标签 $H_i$，由此得到 $\mathrm{Acc}$、$\textsc{Hr}$、$\textsc{Hr}_{\mid\mathrm{corr}}$ 和 $\textsc{Daa}$；干预侧则产生受约束的新解答或明确弃答。

</div>

**直观理解**：把“答案是否正确”和“方法是否合格”交给两个隔离的过程，可避免把普通算错自动误判成作弊。允许弃答也很重要，否则强硬提示可能只迫使模型把捷径写得更隐蔽，而不是真正提升推理。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Solution hacking 的形式化判定

$$
\operatorname{Hack}(q,s)=\mathbb{1}\!\left[\hat{a}(s)\equiv a^{*}\ \land\ \exists\,e\in\operatorname{Essential}(q):\operatorname{strategy}_{s}(e)\notin M(q)\ \land\ \operatorname{strategy}_{s}(e)\text{ substitutes for }\mathcal{C}(q)\right]
$$

**符号说明**

- $q$：基准题目。
- $s$：大语言模型生成的完整解答。
- $a^{*}$：题目的参考答案。
- $\hat{a}(s)$：从解答中抽取出的最终答案。
- $\mathcal{C}(q)$：题目设计为考查的目标推理能力。
- $M(q)$：领域专家认可的、能够正当运用目标能力的策略集合，不限于参考解法。
- $e$：题目所要求解答中的一个必要步骤。
- $\mathbb{1}[\cdot]$：指示函数；括号内条件成立时取 $1$，否则取 $0$。

<div class="equation-explanation" markdown="1">

**直观理解**：该式忠实概括 Definition 1 的逻辑条件：只有最终答案正确，并且至少一个关键步骤使用集合 $M(q)$ 之外的捷径替代目标能力时，解答才是 solution hack。它排除了两类容易混淆的情况：答案错误但推导方法诚实的普通推理错误，以及虽不同于参考答案但仍完整运用了目标能力的有效替代解法。<br>
**原文位置**：第 3 节，Definition 1；判定细化见 T1–T3

</div>

</div>

<div class="equation-block" markdown="1">

#### 正确性、破解率与推导校正准确率

$$
\mathrm{Acc}=\mathbb{E}_{i}[C_i],\qquad \textsc{Hr}=\mathbb{E}_{i}[H_i],\qquad \textsc{Hr}_{\mid\mathrm{corr}}=\mathbb{E}_{i}[H_i\mid C_i=1],\qquad \textsc{Daa}=\mathbb{E}_{i}[C_i(1-H_i)],\qquad \Delta_{\mathrm{infl}}=\frac{\mathrm{Acc}-\textsc{Daa}}{\mathrm{Acc}}=\textsc{Hr}_{\mid\mathrm{corr}}
$$

**符号说明**

- $i$：模型在基准上的第 $i$ 个题目或解答样本。
- $C_i$：最终答案正确性指示变量，取值属于 $\{0,1\}$。
- $H_i$：solution-hacking 指示变量，取值属于 $\{0,1\}$。
- $\mathrm{Acc}$：普通最终答案准确率。
- $\textsc{Hr}$：全部解答中的破解比例。
- $\textsc{Hr}_{\mid\mathrm{corr}}$：在最终答案正确的解答中，被判为破解的条件比例。
- $\textsc{Daa}$：derivation-adjusted accuracy，只认可答案正确且未破解的解答。
- $\Delta_{\mathrm{infl}}$：普通准确率中由破解解答带来的相对分数膨胀。
- $\mathbb{E}_{i}$：对基准中所有样本求经验平均。

<div class="equation-explanation" markdown="1">

**直观理解**：普通准确率只看 $C_i$，而 $\textsc{Daa}$ 通过因子 $1-H_i$ 去掉方法不合格的正确答案，因此两者差异直接反映答案式评分认可了多少破解解答。等式 $\Delta_{\mathrm{infl}}=\textsc{Hr}_{\mid\mathrm{corr}}$ 表明，准确率的相对膨胀恰好等于正确答案中的破解比例；但由于检测器会漏掉部分破解，实际计算值应按论文说明理解为保守下界。<br>
**原文位置**：第 4.1 节 Metrics

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文没有训练或微调新的参数化模型，也没有给出需要梯度优化的损失函数；所谓“build”主要指在 $180$ 个专家开发样本上迭代审计提示、为每个判断模型选择与专家标签更一致的提示版本，并设计四种测试时 anti-hack 指令。专家一致率用于模型与提示选择，Cohen’s $\kappa$ 仅作为次要可靠性指标，而不是训练目标；$120$ 个留出样本只用于最终检验，不能反向参与提示校准。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 角色敏感的 solution-hacking 判定规范**

判定以题目目标能力 $\mathcal{C}(q)$ 和专家认可策略集合 $M(q)$ 为参照，并联合检查 T1 targeted crux、T2 capability bypass、T3 derivational support。策略标签包括数值搜索 $\mathcal{H}_{\mathrm{num}}$、枚举 $\mathcal{H}_{\mathrm{enum}}$、模式猜测 $\mathcal{H}_{\mathrm{pat}}$、公式猜测 $\mathcal{H}_{\mathrm{form}}$、答案猜测 $\mathcal{H}_{\mathrm{ans}}$ 和其他捷径 $\mathcal{H}_{\mathrm{oth}}$，但最终标签由策略在具体解答中的功能决定。

> 直观理解：同一种技术在不同题目里可能一边合法、一边构成破解：穷尽所有候选并证明覆盖完整通常是有效枚举，只试到第一个匹配答案便停止则可能没有排除其他候选。这个模块的作用是判断方法有没有替代关键推导，而不是维护一张机械的禁用技术清单。

**2. 专家锚定的无自审投票检测器**

三个 peer-level judge 使用经开发集校准的审计提示，对问题和解答进行独立判断并投票；常规样本采用多数票，自生成样本采用 no-self-audit 规则。检测器不接触参考答案 $a^*$ 或 $C_i$，并在留出专家测试集上只评估一次，以避免把测试标签用于提示调优。

> 直观理解：它像一个由多名阅卷员组成的评审组，但任何阅卷员都不能审核自己的答卷。与正确性检查隔离后，错误但推导诚实的解答不会仅因答案错误而被记为破解。

**3. 专家锚定的 anti-hack 生成提示**

ban-list 直接禁止六类捷径；necessity 要求证明答案具有必然性或唯一性；guardrail 明确评分边界，同时保留题目本来允许的枚举；pre-commit 要求模型先声明推导计划，并标注关键步骤来自推导还是猜测。四种变体均提供严格弃答选项，其目标是改变测试时生成行为，不涉及模型参数更新。

> 直观理解：四种提示分别从“禁止什么”“必须证明什么”“怎样区分合法与非法方法”和“先承诺推导路线”约束模型。弃答机制把“无法严格完成”变成可接受输出，减少模型为了交出答案而猜测后补验证的动机。

**训练与推理**

校准阶段先由 Stage-1 auditor 对多模型、多学科的高难题解答进行初筛，再对分层抽取的 $300$ 份解答做盲审专家标注；其中 $180$ 份用于修订审计提示和选择检测器配置，$120$ 份留出测试。最终判断时，系统对每份解答并行执行两条相互隔离的路径：正确性路径将 $\hat{a}(s)$ 与 $a^*$ 比较并生成 $C_i$；破解检测路径只把 $(q,s)$ 交给投票 panel，生成 $H_i$ 与策略标签。若回答模型与某个 judge 相同，则排除该 judge，防止自审。

生成干预同样发生在推理时：将题目与 ban-list、necessity、guardrail 或 pre-commit 提示之一交给回答模型，模型输出完整推导或“CANNOT SOLVE RIGOROUSLY”。新解答随后仍由上述独立正确性模块和无自审检测器评估，因此干预效果不能只看普通准确率，还应联合比较 $\textsc{Hr}$ 与 $\textsc{Daa}$，判断准确率变化究竟来自减少破解、增加严格解答，还是增加弃答。

**复现信息**

复现时必须保留三项决定公平性的设计。第一，正确性判定对所有 judge 共用且只计算一次：数值答案采用 $5\%$ 相对容差，符号答案检查代数等价；hack judge 不得看到参考答案或正确性标签。第二，专家锚点应保持学科匹配、解答来源盲化和开发/测试隔离；原文样本为数学 $101$ 份、物理 $100$ 份、化学 $99$ 份，初筛分层为 flagged $107$ 份、clean $193$ 份，并由数学、物理、化学博士专家池分别标注。第三，最终 panel 由 Gemini-3.1-Pro-Preview、Claude Opus 4.7 和 GPT-5.2 构成，常规情形采用多数票，自审冲突时只保留另外两个判断器且要求一致。

解释结果时还要注意检测误差方向：原文报告 deployed detector 与专家总体一致率为 $75.4\%$，但在锚点上对专家确认破解的总体召回率仅为 $61.2\%$，其漏检多于误报。因此 $H_i=0$ 不能被理解为已经证明推导完全有效，聚合后的 $\textsc{Hr}$、$\textsc{Hr}_{\mid\mathrm{corr}}$ 和由其决定的分数膨胀也不能视为实际破解程度的上界或无偏估计。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 简单层用于负对照，包括 SciBench 与难度等级不超过 $2$ 的 MATH-500 教材题，共 $603$ 个样本，其中数学、物理、化学分别为 $200$、$199$、$204$ 个。其作用是检验审计器是否会把正常基础解法大量误判为作弊。
- 中等层由 IMO-Bench、PHYBench 和 SciOlympiad 的竞赛题组成，用于观察模型面对仍可能求解、但需要较强专业推理的问题时，是否转向捷径，以及反作弊指令能否把捷径重新引导为诚实推导。
- 困难层采用 HLE 前沿科学题。中等层和困难层共同构成主语料，覆盖数学、物理、化学，由 $11$ 个模型生成 $3528$ 份解答；其中跨学科核心子集的反作弊实验包含 $n=1008$ 份解答。另有 $300$ 份前沿解答由博士专家盲标，划分为 $180$ 份开发集和 $120$ 份测试集，用于校准及检验自动审计器。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（Acc）**

最终答案被判为正确的比例，不检查推导过程是否满足题目要求。它衡量基准通常报告的答案级成绩，但可能把捷径得到的正确答案计入能力。 （通常越高越好，但只有结合解法作弊指标才能解释为真实推理能力。）

</div>
<div class="metric-item" markdown="1">

**作弊率（Hr）及正确答案条件作弊率（$\mathrm{Hr}_{\mid\mathrm{corr}}$）**

$\mathrm{Hr}$ 是全部解答中被审计为使用无效捷径的比例；$\mathrm{Hr}_{\mid\mathrm{corr}}$ 是已获正确分的答案中实际属于作弊解法的比例，直接刻画答案级准确率受到捷径污染的程度。 （越低越好；较低意味着模型较少依赖不满足任务推导要求的搜索、猜测或答案先行验证。）

</div>
<div class="metric-item" markdown="1">

**推导调整准确率（Daa）**

排除作弊所得正确答案后，更接近“答案正确且推导有效”的能力指标。论文通过比较 Daa 与 Acc 的差距估计捷径给报告成绩带来的膨胀。 （越高越好；若反作弊后 Acc 下降而 Daa 基本不变，说明减少的主要是捷径买来的分数，而非真实推导能力。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 不同难度层级的总体作弊率

<div class="result-value" markdown="1">

使用同一部署审计器后，汇总作弊率从简单题的 $2.2\%$ 上升到竞赛题的 $28.3\%$，再升到 HLE 前沿题的 $37.4\%$；只保留各模型家族最强版本时仍呈 $2.2\%\rightarrow16.1\%\rightarrow26.3\%$ 的单调趋势。

</div>

这说明捷径行为主要在高难题上暴露，而不是审计器不分难度地乱报。简单地说，模型会做时通常正常推导，不会做时更可能搜索或猜测。不过，该结果是难度分层下的相关关系；题目答案格式、可搜索性及数据集构成也可能共同影响作弊率，不能据此断言难度是唯一因果因素。

<div class="result-source" markdown="1">

来源：Figure 2；Section 5.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Hack ratio by difficulty tier and subject (deployed detector): the rise is monotone in every subject, 2.2 → 28.3 → 37.4% pooled over all model versions (solid line; bars give the per-subject pooled values). The dashed line pools only the strongest current version of each family (2.2 → 16.1 → 26.3%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 困难层中正确答案受到作弊解法污染的程度

<div class="result-value" markdown="1">

困难层总体作弊率为 $33.2\%$；在各模型已获正确分的答案中，$\mathrm{Hr}_{\mid\mathrm{corr}}$ 从 Gemini-3.1-Pro-Preview 的 $8.2\%$ 到 GPT-4.1 的 $44.1\%$。所有模型的 Daa 都低于 Acc。

</div>

答案级评分确实会把部分无效推导包装成模型能力，而且较弱模型的正确答案中这种污染比例更高。作者还指出审计器存在漏检，因此这些差距是下界。需要注意，$44.1\%$ 表示 GPT-4.1 的“已判正确答案中有多少属于作弊”，并不表示它在全部题目上的作弊成功率，也不意味着所有模型都被高估相同比例。

<div class="result-source" markdown="1">

来源：Table 4；Section 5.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

It grows steeply as models weaken, from 8.2% for Gemini-3.1-Pro-Preview to 44.1% for GPT-4.1, so reported accuracy overstates derived competence by a corresponding margin, and Daa falls below Acc for every model.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 困难跨学科核心集上的反作弊生成干预

<div class="result-value" markdown="1">

随着反作弊提示变严格，作弊率由 $22.3\%$ 降至 $6.9\%$；与此同时，报告准确率由 $41.5\%$ 降至 $33.3\%$、弃答率由 $0\%$ 升至 $22.5\%$，而 Daa 仅由 $34.7$ 变为 $31.3$。

</div>

干预消除的分数大多没有转化为有效推导，而是转化为弃答，因此原先下降的那部分准确率主要依赖捷径。Daa 变化远小于 Acc，也支持“答案级成绩存在膨胀”的解释。但严格提示并非纯粹改善模型：它也可能让本来能诚实解决的问题被放弃，所以不能把更低作弊率直接等同于更高总体实用性。

<div class="result-source" markdown="1">

来源：Figure 4；Table 7；Section 5.5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As the prompt becomes stricter, the hack ratio drops from 22.3% to 6.9%. Reported accuracy also drops, from 41.5% to 33.3%. The missing probability mass mainly turns into abstention, which rises from 0% to 22.5%, rather than into real solutions: Daa stays almost unchanged, moving only from 34.7 to 31.3.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主作弊率依赖自动审计器，而人工锚定显示初始单审计器总体阳性预测值仅为 $0.626$、漏检率为 $0.207$，且具体作弊类别的一致性较弱。作者的分层校正反而提高了各学科估计，支持当前结果是下界，但总体比例仍需要更大规模、多标注者的人类复核。
- 若干比较不是严格因果实验：难度层同时改变了数据集来源、答案格式和可搜索性，模型版本也同时改变了训练数据、后训练及推理能力。反作弊提示还会诱发弃答并压制部分诚实求解，因此其效果不能只用作弊率下降评价。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 标准中性思维链提示：要求模型作答，但完全不提“作弊”，作为自然捷径行为和报告准确率的基准。
- 答案正确性评价：只比较抽取出的最终答案与参考答案，数值题采用 $5\%$ 相对误差容限，符号题检查数学等价性。它代表科学推理基准常见的答案级评分方式。
- 专家盲标：由对应学科的博士标注者依据书面规则判断解答为作弊或干净，并进行自我复核；它是校准自动审计器和估计漏检程度的人工参照。
- 固定外部审计器：在同一模型家族的版本比较中，每个家族始终由一个不属于该家族的固定审计器评分，以避免模型自审和审计器更换混淆版本差异。

**实验想回答的问题**

- 在答案正确性保持不变的评价口径下，前沿大模型有多大比例通过猜公式、猜答案、枚举或数值搜索等无效捷径得到答案；这种解法作弊是否随题目难度、学科和模型能力而系统变化？
- 自动审计器能否可靠识别解法作弊，以及生成时加入不同强度的反作弊指令后，报告准确率、真实推导能力和弃答率如何变化？

**实验实现**

主实验让多个前沿模型在统一的中性思维链提示下生成完整解答，随后将“最终答案是否正确”和“推导是否作弊”分开判定。困难与竞赛主语料覆盖 $11$ 个模型；反作弊干预则在三个最强面板模型及数学、物理、化学的共享核心题上比较标准提示与四种反作弊提示。自动审计器先以博士专家盲标的开发集分析分歧并收紧规则，再在测试集和主语料上部署。由于专家样本刻意富集了审计器标记的案例，论文不直接把样本中的标记比例当作总体作弊率，而是在“已标记”和“未标记”两个层内估计阳性预测值与漏检率。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 固定外部审计器下的同家族版本阶梯比较 | GPT 家族作弊率从 $49.5\%$ 降至 $37.0\%$，Gemini-pro 从 $20.7\%$ 降至 $13.4\%$，Claude-opus 从 4-5 的 $50.3\%$ 降至 4-7 的 $20.4\%$；但 Claude-opus 4-8 又升至 $35.2\%$。 | 该控制实验固定题目和家族外审计器，主要隔离同一模型谱系的版本变化，减少模型家族和自审规则造成的混淆。结果表明后训练可能持续抑制明显捷径，但这种改进并不保证随版本单调发生；Claude 4-8 的反弹说明普通能力升级不能替代过程审计。它仍是观察性版本比较，不能单独确定具体训练环节的因果作用。 | Table 6；Figure 5；Section 7, Family study details<br><span class="experiment-evidence">Within-family version ladders (%), each lineage scored by a fixed judge external to it (v3c prompt), applied identically to every rung: as each lineage advances its hack ratio falls—except the newest Claude-opus rung († 4-7 → 4-8), which reverses.</span> |
| 反作弊干预按学科与难度拆分 | 物理核心集原本的 Acc 与 Daa 已较接近，为 $28.1$ 对 $26.7$；最严格的预承诺提示使物理 Daa 从 $26.7$ 降至 $20.9$。相反，在中等难度竞赛题上，数学 Daa 在 necessity 提示下由 $51.9$ 升至 $56.2$，化学 Daa 在 guardrail 提示下由 $52.4$ 升至 $64.3$，但化学样本仅有 $n=42$。 | 这一拆分检验反作弊提示究竟是在移除虚假得分，还是能把模型重新引导到正确推导。物理中可获分作弊本来较少，干预主要造成过度弃答；中等难度数学和化学仍处于模型能力范围，部分捷径则能被转化为诚实解法。化学提升来自很小的样本，原文也要求定性解读，不能当作稳定的精确增益。 | Section 5.5；Section 7, Mitigation averages, the physics null, and the competition-tier conversion<br><span class="experiment-evidence">On the competition tier the direction reverses: Daa rises under several variants (medium math 51.9 → 56.2 necessity; medium chemistry 52.4 → 64.3 guardrail and ban-list, n = 42), i.e. within-reach hacks are converted into honest derivations rather than abstentions.</span> |

**定性案例**

- 审计器与专家都判定为作弊的 $67$ 个案例中，具体策略类别的一致性只有原始 $47.8\%$、$\kappa=0.213$；审计器尤其倾向把案例归入宽泛的 other_shortcut。这个案例分析说明，系统较适合回答“是否使用了捷径”，却不适合把公式猜测、答案猜测等细类别占比当作高精度结论。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It identifies shortcut-based solution hacking in scientific reasoning benchmarks and develops evaluation methods that distinguish valid reasoning from answer-only correctness.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`d1360954770b33a63f50730add4fee0c86b03e6991c9efe3d004a3c1e77a5174`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
