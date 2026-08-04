---
title: "[论文解读] MechGeo: Autoformalizing and Proving Euclidean Geometry in Lean 4"
description: "[arXiv 2608.02295][LLM Reasoning] MechGeo试图把欧氏几何题从自然语言到可信 Lean 4 定理及其核验后证明的全过程连成统一闭环，并用形式化反例发现那些能够通过编译、却偏离原题含义的陈述。"
arxiv_id: "2608.02295"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:57:38.920781+00:00"
source_sha256: "8b6bd51108d77a9a40ddcf5bf58ec9fffa665c7f9077a22e0d712b7fdf06e46e"
tags:
  - "LLM Reasoning"
  - "LLM Agent"
  - "欧氏几何"
  - "自动形式化"
  - "Lean 4"
  - "Mathlib"
  - "形式化定理证明"
  - "GeoIR"
  - "选择性代数化"
  - "内核检查"
  - "反例引导诊断"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.02295</p>

# MechGeo: Autoformalizing and Proving Euclidean Geometry in Lean 4

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Hao Shen, Junyu Guo, Tian Cui, Yuxuan Xiao, Lihong Zhi</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02295v1) · [PDF 下载](https://arxiv.org/pdf/2608.02295v1) · **关键词** 欧氏几何, 自动形式化, Lean 4, Mathlib, 形式化定理证明, GeoIR, 选择性代数化, 内核检查, 反例引导诊断<br>
**代码**: [https://github.com/MechMath/MechGeoBench](https://github.com/MechMath/MechGeoBench)

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

MechGeo试图把欧氏几何题从自然语言到可信 Lean 4 定理及其核验后证明的全过程连成统一闭环，并用形式化反例发现那些能够通过编译、却偏离原题含义的陈述。

**不用术语来说**：把一道几何题写进 Lean 4，不只是更换数学符号：原题常依赖图形和默认约定，例如“点在边上”究竟表示位于直线、闭线段还是两端点之间，以及相关点是否重合。漏写这些条件时，形式化陈述仍可能通过编译，甚至可能证明成功，但证明的已经不是原题。陈述正确之后，系统还要找到合适的辅助结论，并在保持几何结构与转化为坐标多项式之间作出有效选择。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 Mathlib 原生的 GeoFormalizer：先用中间表示 GeoIR 表达非形式化几何题，再确定性地生成 Lean 4 陈述，并结合编译器的结构诊断与语义评估迭代修复候选形式化，从而同时关注“能否编译”和“是否忠实表达原题”。
- 提出 GeoProver，将几何证明规划、中间引理推导和选择性代数化结合起来；外部计算机代数系统可以生成代数证书，但证书、最终证明以及用于诊断错误陈述的反例均由 Lean 内核检查。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于“数学自动形式化”和“交互式定理证明”交叉领域，具体处理平面欧氏几何。目标不仅是让大语言模型求出几何题，还要把自然语言、示意图惯例与隐含条件转换为精确的 Lean 4 定理，并生成可由 Lean 小型可信内核逐步检查的证明。该任务包含两个相互关联但不同的环节：一是忠实形式化，即形式陈述必须准确表达原题意图；二是认证证明，即证明、外部符号计算产生的证书乃至反例都必须通过内核验证。本文采用 Mathlib 原生表示，使几何对象和结论能够直接使用通用形式化数学库，而不是局限在专用几何语言中。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**Lean 4、Mathlib 与内核检查**

Lean 4 是依赖类型理论驱动的证明助手，Mathlib 是其大型形式化数学库；一个定理只有在相应证明项通过 Lean 内核检查后才被接受。外部计算机代数系统可以帮助寻找结果或生成证书，但不能取代内核的最终验证。

</div>
<div class="concept-item" markdown="1">

**忠实自动形式化**

自动形式化是把自然语言数学题转换成机器可检查的定义、假设和结论；“忠实”进一步要求形式陈述与原题实际意图一致。几何题尤其困难，因为“在线上”“在三角形内”等表述可能依赖图形，并隐含点的次序、严格内部关系或非退化条件。

</div>
<div class="concept-item" markdown="1">

**综合推理与代数化**

综合几何推理直接使用共线、角、凸包和圆心等几何关系来组织证明；代数化则选择坐标，把部分关系转成多项式等式或不等式，再交给 Gröbner 基、Wu 方法等符号过程处理。前者适合暴露结构和拆分子目标，后者适合系统消去变量并验证多项式后果。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是以自然语言给出的二维欧氏几何问题，其中题意可能同时依赖文字、图形习惯以及未明确写出的非退化或位置条件。GeoFormalizer先把问题表示为中间语言 GeoIR，再确定性翻译成 Mathlib 原生的 Lean 4 定理；候选陈述需要通过语法与结构诊断、编译检查和语义评估。这里“能够编译”并不等于“忠实”：例如“点 $D$ 在 $BC$ 上”可能表示位于支撑直线、闭线段或严格处于 $B$ 与 $C$ 之间，而 Mathlib 中的定义即使接受退化输入，也可能仍然具有合法含义。

形式化定理随后作为 GeoProver 的输入。证明器规划几何证明、提出中间引理并把目标拆成子目标：保留适合综合推理的几何结构，仅将适当子目标转换为坐标多项式约束；Singular 或 SymPy 可以参与生成代数证书，但最终证明或反例必须由 Lean 内核检查。输出因而不只是一个“答案”，而是三类可审计形式对象之一：通过验证的 Lean 定理及证明、证明原陈述不成立的 Lean 验证反例，或在发现遗漏条件后得到的修正陈述及其证明。论文默认工作空间为二维实欧氏空间，例如案例中的点属于 $\text{EuclideanSpace}\,\mathbb{R}\,(\mathrm{Fin}\,2)$；典型假设包括仿射无关、凸包成员关系、点不重合和角相等。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\operatorname{EuclideanSpace}\,\mathbb{R}\,(\mathrm{Fin}\,2)$**

以实数为标量的二维欧氏空间，即论文中平面点所在的类型。

</div>
<div class="notation-item" markdown="1">

**$\operatorname{AffineIndependent}_{\mathbb{R}}[A,B,C]$**

点 $A,B,C$ 仿射无关；在二维情形下，它表达三点不共线，从而排除退化三角形。

</div>
<div class="notation-item" markdown="1">

**$K\in\operatorname{convHull}_{\mathbb{R}}\{B,M,C\}$**

点 $K$ 位于 $B,M,C$ 的凸包中；若三点构成非退化三角形，该约束表示 $K$ 位于三角形及其边界内。

</div>
<div class="notation-item" markdown="1">

**$\operatorname{dist}(O,M)=\operatorname{dist}(O,N)$**

点 $O$ 到 $M$ 与 $N$ 的欧氏距离相等，是图 2 的 IMO 2026 第 2 题案例所需证明的最终结论。

</div>

</div>

**直接相关的工作**

- **AlphaGeometry / AlphaGeometry2 / TongGeometry**: 这些系统把学习引导与专用几何语言中的符号演绎结合，用于辅助构造和搜索，展示了高水平竞赛几何能力；但其表达能力取决于专用语言能否表示所需构造和关系。MechGeo采取互补路线，直接处理 Mathlib 陈述，并让最终证明接受 Lean 内核检查。
- **Eucleant**: Eucleant同样面向 Mathlib 原生几何形式化，通过约束显式化、构型锚定、形式化映射和迭代修复处理自然语言到形式陈述的转换。MechGeo在此类形式化问题之上进一步统一语义修复、几何证明规划和经 Lean 验证的代数化证明层。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

当前形式推理系统通常从已经写好的 Lean 定理开始评测，但真实应用首先要求把依赖文字、图形和几何惯例的竞赛题准确转成形式陈述。欧氏几何中的顺序、介于关系和非退化条件经常被省略，而 Mathlib 的许多定义在退化输入上仍有意义，因此漏掉条件未必触发编译错误。实际需求由此包含两个相互依赖的环节：验证形式陈述确实对应原题，以及为该陈述构造可由小型可信内核检查的证明或反例。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **通用 Lean 定理证明器与智能体框架**：这类系统接收已经形式化的定理，利用语言模型、证明搜索和 Mathlib 引理生成 Lean 证明项，再交给 Lean 内核核验；其主要能力集中在证明构造，而非从非形式化几何题恢复完整且忠实的形式语义。
- **专用几何推理与坐标代数化方法**：AlphaGeometry、TongGeometry 等系统用专用几何语言和符号演绎搜索辅助构造与几何关系；另一类方法把几何条件转成多项式方程或不等式，再使用吴方法、Gröbner 基等符号算法验证代数推论。前者强调结构化几何推理，后者通过计算系统化处理代数后果。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 仅依靠 Lean 编译反馈或人工检查，不能可靠判定形式陈述是否忠实：例如“点在某边上”的多种解释都可能合法展开，缺失非退化或顺序条件的错误版本还可能存在有效证明，其后果是系统给出机器核验通过、但并未解决原题的证明。
- 专用几何演绎依赖语言能否表达所需关系以及系统能否提出关键辅助构造，对不等式、非线性关系、三维配置或需要任意多个点的构造仍可能受限；相反，把整个配置一次性代数化会产生庞大的多项式系统和表达式膨胀，其效率又对坐标选择、问题表述和变量顺序敏感。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚缺少一个 Mathlib 原生的统一验证闭环：它既要在陈述层面区分“语法可接受”与“语义忠实”，并通过可核验反例定位遗漏条件；又要在证明层面保留几何结构，只对适合的子目标实施代数化，同时保证外部符号计算产生的结果不会扩大可信计算基础。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一个端到端的 Lean 4 几何智能体框架，使其从非形式化欧氏几何题出发，生成并语义诊断形式陈述，再通过几何证明规划与选择性代数化得到由 Lean 内核完整核验的证明；若陈述错误，则生成同样可核验的反例以支持修复？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是让不同工具各自处理最擅长的部分：GeoIR和确定性翻译减少语言模型直接生成 Lean 代码时的结构漂移，反例把抽象的“陈述可能不忠实”变成具体可检查的失败配置；证明时先用几何推理识别结构并拆分目标，再把适合计算的局部义务转成多项式，可避免全局代数化造成的规模膨胀。外部计算机代数系统只负责寻找证书，Lean 负责复核证书，因此可以利用符号计算能力而不必直接信任外部程序。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MechGeo 是一个面向欧氏几何的 Lean 4 自动形式化与自动证明框架，由 GeoFormalizer 和 GeoProver 串联组成。输入是自然语言几何题；GeoFormalizer 先让语言模型用受限、强类型的中间语言 GeoIR 表达题意，再通过固定规则确定性地生成 Mathlib 原生 Lean 命题，并结合静态检查、Lean 编译检查和语义评分迭代修复。GeoProver 随后仅接收正式 Lean 命题，先生成包含辅助构造和中间引理的几何证明计划，再只把适合计算的局部子目标改写成坐标多项式问题；Lean 内置策略或外部计算机代数系统生成代数推导后，所有证明证书均由 Lean 内核重新检查。若原命题不可证，系统转而构造显式坐标反例并形式化证明其否定。
直观地说，该框架没有要求语言模型一步写出容易出错的 Lean 代码，也没有把整道几何题粗暴地展开为一个庞大的方程组。它先使用 GeoIR 充当自然语言与 Lean 之间的“受控草稿格式”，再让证明器在合成几何推理与坐标代数计算之间切换；外部工具只负责寻找可验证的计算证书，最终可信性仍由 Lean 内核保证。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### GeoIR 生成与结构检查

GeoFormalizer 的构造器生成带类型的 GeoIR 规格，其中包含对象声明、几何构造、几何关系和数值表达；解析器与静态检查器检测未声明对象、参数个数错误、类型不匹配和结构畸形，并将诊断反馈给构造器修复。

<div class="method-step__io" markdown="1">

**输入**：自然语言欧氏几何问题。<br>
**输出**：能够被解析、对象引用完整且类型一致的 GeoIR 抽象语法树。

</div>

**直观理解**：GeoIR 相当于几何题专用的受限语言：模型只需准确描述点、圆、共线等数学关系，不必同时处理复杂的 Lean 接口。先检查这份结构化草稿，可以在进入证明阶段前消除大量语法和类型错误。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定性翻译、评估与迭代修复

无语言模型参与的规则翻译器把 GeoIR 解析为带类型语法树，递归依据固定映射生成 Mathlib 原生 Lean 命题，再由 Lean 的解析器、 elaborator 和内核检查；评估器结合语义一致性分数与点覆盖率计算 $F$，仅在 $F\geq 0.6$ 时接受，否则返回语义或结构反馈并重新生成 GeoIR。

<div class="method-step__io" markdown="1">

**输入**：通过结构检查的 GeoIR 规格及原始自然语言题目。<br>
**输出**：通过 Lean 类型检查且达到接受阈值的正式命题。

</div>

**直观理解**：固定映射使同一份 GeoIR 总能稳定地产生对应的 Lean 表达，避免模型在翻译时随意改变题意。评分环节进一步处理“代码能编译但定理写错了”的问题，例如遗漏关键点、假设矛盾或结论被错误地写成平凡命题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 几何证明规划与选择性代数化

GeoProver 重建命题的几何含义，按顺序规划辅助构造、中间事实、角度追踪和代数恒等式；随后通过 $\mathtt{to\_basic}$ 与 $\mathtt{basic\_to\_poly}$ 或组合策略 $\mathtt{to\_poly}$，只把选定假设或子目标从几何谓词逐层改写为坐标上的多项式等式与不等式。

<div class="method-step__io" markdown="1">

**输入**：已接受的正式 Lean 命题；证明代理只能看到该正式命题。<br>
**输出**：由 Mathlib 层的合成几何步骤和若干规模较小、次数较低的代数子目标构成的证明状态。

</div>

**直观理解**：系统先规划证明，再决定哪些局部步骤值得交给代数计算，因此共线、共圆等整体结构不会过早丢失。每条改写规则本身都是 Lean 已证明的等价引理，所以代数化不会暗中加强假设或削弱结论。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 认证代数求解与独立核验

简单子目标由 Lean 策略处理；较困难的多项式等式可调用 Singular 或 SymPy 寻找余因子证书，再将证书编码为 Lean 推导，非零约束和不等式则通过 Lean 策略、显式符号引理与分类讨论证明。若证明失败且命题为假，系统用显式坐标构造反例并证明命题的否定；独立验证器要求完整文件无 $\mathtt{sorry}$、仅使用允许的公理，并严格匹配输入命题或其否定。

<div class="method-step__io" markdown="1">

**输入**：几何证明计划、Lean 几何子目标及代数化后的多项式约束。<br>
**输出**：由 Lean 内核检查通过的原命题完整证明，或由 Lean 检查通过的形式化反例。

</div>

**直观理解**：Singular 和 SymPy 可以帮助“找到答案”，但不能替 Lean 宣布答案正确；Lean 会逐项验证其代数恒等式和符号论证。证明与反例采用对称的严格标准，从而区分证明搜索能力不足和输入命题本身错误。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 形式化候选的综合评估分数

$$
F = 0.7S_{\mathrm{judge}} + 0.3S_{\mathrm{struct}}
$$

**符号说明**

- $F$：GeoIR 候选的综合接受分数。
- $S_{\mathrm{judge}}$：自然语言题目与生成 Lean 命题之间的语义一致性分数；一致、部分一致和不一致分别映射为 $1$、$0.5$ 和 $0$。
- $S_{\mathrm{struct}}$：点覆盖率，即 GeoIR 中声明的点里，在自然语言题目中被提及的点所占比例。

<div class="equation-explanation" markdown="1">

**直观理解**：该评分以语义判断为主、结构覆盖为辅，候选仅在 $F\geq 0.6$ 时被接受。权重和阈值使结构覆盖率主要在 $S_{\mathrm{judge}}=0.5$ 的语义模糊情形中起决定作用，而不能轻易推翻明确的一致或不一致判断。<br>
**原文位置**：第 3.1.3 节 Evaluation；接受规则见第 3.1.4 节 Iterative Repair

</div>

</div>

<div class="equation-block" markdown="1">

#### 多项式理想成员证书

$$
q = \sum_{i=1}^{n} c_i p_i
$$

**符号说明**

- $p_i$：第 $i$ 个由几何假设代数化得到的多项式；相应假设为 $p_i=0$。
- $n$：参与证书构造的多项式等式假设数量。
- $q$：目标等式左侧对应的目标多项式；待证目标为 $q=0$。
- $c_i$：由 Singular 或 SymPy 计算的第 $i$ 个多项式余因子。

<div class="equation-explanation" markdown="1">

**直观理解**：如果每个假设都给出 $p_i=0$，而外部系统找到余因子使 $q$ 等于这些 $p_i$ 的多项式组合，那么代入后立即得到 $q=0$。外部 CAS 负责搜索 $c_i$，但该恒等式及其推出目标的过程会被转换成 Lean 证明并由内核检查。<br>
**原文位置**：第 3.2.3 节 Certified Algebraic Discharge

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文将 MechGeo 描述为代理式形式化与证明框架，没有报告对语言模型进行参数训练、微调或基于某个损失函数的优化；式 $F=0.7S_{\mathrm{judge}}+0.3S_{\mathrm{struct}}$ 是推理阶段筛选和修复 GeoIR 候选的评分规则，而非训练目标。多项式证书等式同样是证明构造条件，不是机器学习优化目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. GeoFormalizer**

该模块由 GeoIR 构造器、类型化解析与静态检查器、规则式 Lean 翻译器以及语义和结构评估器组成。GeoIR 将几何表达限制为声明、构造、关系和值四类结构；固定映射把大部分结构翻译为 Mathlib 表达，少量结构映射到作者提供并在 Lean 中验证的谓词。

> 直观理解：它解决的是“如何忠实地写出要证明的命题”，而不是直接证明命题。中间表示降低了模型掌握 Lean 语法和 Mathlib 接口的负担，确定性翻译则缩小了可能出错的范围；当 Mathlib 接口变化时，只需更新受影响的映射即可重新翻译已有 GeoIR。

**2. GeoProver**

该模块采用四阶段代理流程：证明规划、选择性代数化、认证代数消解和独立验证。证明过程可在 Mathlib 的合成几何层与坐标多项式层之间交替：前者推导结构性事实，后者处理适合符号计算的精确代数后果。

> 直观理解：它解决的是“如何在不牺牲可信性的前提下完成证明”。先拆分问题再局部代数化，可以避免一次性生成规模过大、次数过高的多项式系统，也能继续利用 Mathlib 已有的几何定理。

**3. 认证代数化与反例验证库**

库中的等价引理支持把共线、共圆、点、圆、距离、向量、范数和内积等对象逐步展开为坐标多项式；外部 CAS 只计算因式分解、代数分解或余因子，而最终恒等式、符号条件及分类讨论均在 Lean 中证明。反例路径要求给出满足全部假设但使结论失败的显式对象，并正式建立原命题的否定。

> 直观理解：该库是几何语义与符号计算之间的可信桥梁。它既允许系统利用成熟计算工具的搜索能力，又防止外部工具的错误、数值近似或接口问题直接进入最终证明。

**训练与推理**

原文未描述专门训练流程，完整过程属于推理时的生成、检查、修复和证明搜索。首先，构造器依据自然语言题目生成 GeoIR，经解析和静态检查后反复修复；规则翻译器确定性地产生 Lean 命题，Lean 检查其良构性与类型，评估器再按综合分数决定接受或返回反馈。随后 GeoProver 仅从正式命题重建几何问题并生成有序证明计划，在 Mathlib 几何推理与局部坐标代数化之间交替，必要时调用 Singular 或 SymPy搜索代数证书。最终系统输出与输入命题精确匹配的无 $\mathtt{sorry}$ 证明；若命题不成立，则输出形式化证明其否定的显式坐标反例。无论走证明还是反例路径，最终文件都必须通过 Lean 内核和独立验证器。

**复现信息**

复现时最关键的接口约束有三项。第一，GeoIR 的四类构造必须具有固定、可维护的 Lean 映射，翻译过程应先生成带类型抽象语法树，再由 Lean 的 parser、elaborator 与 kernel 检查，不能让语言模型自由生成最终 Lean 语法。第二，代数化应实现为经 Lean 验证的等价改写：$\mathtt{to\_basic}$ 先把派生几何对象和谓词化为向量、范数、内积等基础表示，$\mathtt{basic\_to\_poly}$ 再按坐标展开为多项式，$\mathtt{to\_poly}$ 组合这两步并允许作用于指定假设或目标。第三，Singular 或 SymPy 的输出只能作为待核验的证书素材；完整文件必须无 $\mathtt{sorry}$、只使用许可公理，并由独立验证器确认其证明的是原输入命题本身，或在反例路径中确实证明了原命题的否定。原文节选未明确报告提示模板、代理迭代上限、CAS 版本、超时设置或具体许可公理清单。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MG200：共200道非形式化平面几何题，包括43道历史IMO几何题、77道LeanGeo-Bench非IMO题、22条用于考查代数证明能力的CertiGeo经典定理，以及从OMNI-Geometry按难度抽取的58道题。四个子集均用于测试GeoFormalizer；同时，将GeoFormalizer为全部200题生成的Lean命题交给GeoProver，以尽量把证明生成与人工命题形式化分开。实验没有报告训练集、验证集或随机划分，MG200在本文中作为完整评测集使用。
- PutnamBench迁移集：从PutnamBench选取31条基于Lean中$\mathrm{EuclideanSpace}\ \mathbb{R}\ (\mathrm{Fin}\ 2)$表示的平面欧氏几何命题，仅用于测试GeoProver在主基准之外的迁移能力。所给节选未说明具体题目选择标准，也未提供该集合的逐项结果。
- 奥赛级审计集：包括44个经过人工审计、必要时修正的IMO形式化命题，以及LEAP的Lean-IMO-Bench中全部14道几何题。历史IMO部分包含43道旧题，结合IMO 2026第2题形成44题；该设置用于考查系统面对高难度命题时能否证明、形式反驳错误形式化，并在专家修正后证明正确命题。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Lean命题 elaboration rate**

成功通过Lean elaboration的命题比例，即命题能够被解析、补全隐式信息并通过类型检查。该指标检测语法、名称解析和类型层面的可接受性，但不保证形式化命题忠实表达原题。 （越高越好，因为更多生成命题可以进入后续证明阶段；但必须结合语义一致性判断，不能把Lean接受直接解释为形式化正确。）

</div>
<div class="metric-item" markdown="1">

**语义一致性**

由三名专家独立检查生成命题是否保留原题的对象、构造、假设、允许的几何配置和结论，并以多数票决定是否接受，允许逻辑等价的改写。它针对“能够编译但表达错题”的风险。 （越高越好，因为这意味着形式命题更忠实于非形式化题意；所给节选没有给出最终一致性数值，因此不能量化GeoFormalizer在该指标上的优势。）

</div>
<div class="metric-item" markdown="1">

**内核验证的证明或反例成功数**

统计GeoProver是否能让Lean内核接受目标命题的证明，或接受一个确实违反该命题的反例。Singular或SymPy可以生成代数证书，但最终可信性来自Lean内核复核，而不是外部工具本身。 （越高越好，因为它表示系统对给定形式命题给出了机器可检查的结论；不过“找到反例”可能说明输入形式化有误，而不等于原始自然语言定理为假。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RQ1：7个骨干模型在MG200共200题上的全部1400个模型—题目组合

<div class="result-value" markdown="1">

作者报告GeoFormalizer成功 elaboration 1354条命题，即96.7%；Euclean为1159条、82.8%，单次Direct翻译为513条、36.6%。这表明结构化表示和迭代修复显著提高了Lean层面的可接受率。

</div>

直观地说，同一道题不再依赖模型一次性写出完整Lean代码，而是先产生较受约束的中间表示，再根据诊断修补，因此弱骨干模型也较少因语法、类型或结构问题失败。不过该结果只直接证明命题能被Lean elaboration，不能证明它与原题语义一致，也不能证明后续一定存在自动证明。Euclean与GeoFormalizer的调用预算不同，因而这里是实际系统效果比较，而非严格计算成本匹配的算法比较。

<div class="result-source" markdown="1">

来源：第4.2节，表1后的结果分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across all 1,400 model–problem pairs, GeoFormalizer produces 1,354 statements that elaborate successfully (96.7%), compared with 1,159 (82.8%) for Euclean and 513 (36.6%) for direct translation.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### RQ1：按骨干模型汇总的自动形式化表现

<div class="result-value" markdown="1">

相对Euclean，GeoFormalizer将Qwen3.7-Max的总体 elaboration rate 从70.0%提高到93.0%，将MiniMax-M3从45.5%提高到94.5%，将GLM-5.2从67.5%提高到100%；GPT-5.6-Sol和Claude Opus 4.8则均达到100%。主要收益集中在原本直接翻译或基线表现较弱的模型，同时没有牺牲最强模型的上限表现。

</div>

该结果测试方法是否只对某一个供应商或强模型有效。弱模型增幅更大，支持结构化约束和修复机制具有跨模型价值；强模型达到满 elaboration 则说明流水线没有明显引入额外编译失败。但“100%”仍仅指200条生成命题全部通过 elaboration，不代表200条都语义正确，更不代表证明全部成功。

<div class="result-source" markdown="1">

来源：第4.2节，表1后的结果分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The overall elaboration rate rises from 70.0% to 93.0% for Qwen3.7-Max, from 45.5% to 94.5% for MiniMax-M3, and from 67.5% to 100% for GLM-5.2.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### RQ3：43道历史IMO几何题及Lean-IMO-Bench的14道几何题

<div class="result-value" markdown="1">

作者在摘要中报告：43道历史IMO题中，GeoFormalizer生成的命题有29道被GeoProver直接证明；其余14道生成命题被构造出Lean验证的反例，经专家修正后14道均可证明。Lean-IMO-Bench的14题中，系统首次证明12题，并形式反驳剩余2条命题，随后证明两条修正版。

</div>

这个结果展示了“证明失败”之外的诊断路径：系统可以用内核验证的反例指出形式命题可能缺少条件或翻译有误，再由专家修正后重新证明。因而29/43不是系统对原始IMO题的最终覆盖率，而是未经专家修正的自动形式化与自动证明联合成功数；14个修正版以及Lean-IMO-Bench的2个修正版都引入了专家干预。所给实验节选未提供逐题列表、运行预算或与其他证明器的同协议数值比较，因此不能据此判断其相对证明效率。

<div class="result-source" markdown="1">

来源：摘要；对应第4节RQ3的总体结论

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On 43 historical IMO geometry problems, GeoFormalizer generates formal statements that GeoProver proves in 29 cases; for the remaining 14, it constructs counterexamples verified in Lean and proves all repaired statements after expert correction.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- RQ1的主表只统计 elaboration，不等价于忠实自动形式化。人工语义审查仅明确覆盖Claude Opus 4.8生成的200条命题，且所给节选在报告最终数值前截断；因此无法确认96.7%的总体 elaboration rate 对应多高的跨模型语义正确率。
- 系统比较不是严格等资源比较：Euclean获得10分钟并调用模型14至116次，GeoFormalizer最多调用5次；与此同时，所有构造骨干模型共享GPT-5.6-Sol语义裁判。奥赛修复结果还包含专家干预。故现有数据支持实际流水线有效，但不足以单独归因每项收益、比较等成本效率或声称所有奥赛结果均为端到端全自动完成。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Direct：让同一骨干模型只进行一次直接的自然语言到Lean翻译，不使用GeoIR和迭代修复。它衡量模型自身的直接形式化能力，是判断结构化流水线是否真正带来增益的最低控制组。
- Euclean：已有的几何自动形式化系统。它是比单次翻译更强的系统级基线；但本文运行中每题调用模型14至116次并给予10分钟超时，而GeoFormalizer最多调用5次，因此准确率比较能够反映效果，但不能视为严格等预算比较。
- GeoFormalizer组件关闭设置：分别关闭编译器引导修复、语义引导修复或同时关闭两者，用来区分结构与类型错误修复和语义偏差修复的贡献。这些设置属于内部对照，不是独立外部系统。

**实验想回答的问题**

- RQ1：GeoFormalizer能否跨不同大语言模型稳定生成可被Lean接受且语义忠实的几何命题，以及编译器引导修复和语义引导修复分别解决什么问题？
- RQ2/RQ3：给定固定或经人工审计的Lean几何命题，GeoProver能否构造内核检查的证明或反例；这种能力能否迁移到PutnamBench、历史IMO题和Lean-IMO-Bench等高难度场景？

**实验实现**

自动形式化实验覆盖7个骨干模型：GPT-5.6-Sol、Claude Opus 4.8、DeepSeek-V4-Pro、DeepSeek-V4-Flash、Qwen3.7-Max、MiniMax-M3和GLM-5.2。RQ1中所有骨干模型共用GPT-5.6-Sol作为自动语义裁判，因此构造模型的比较较统一，但语义修复并非完全独立于该强模型。GeoFormalizer每题最多进行5次模型调用；Euclean获得10分钟超时，在作者运行中每题调用14至116次。全部实验使用Lean 4.27.0，外部符号计算使用Singular 4.4.1和SymPy 1.13.2；外部系统只提出代数证书，证明与反例仍由Lean内核检查。语义评估仅明确报告对Claude Opus 4.8生成的200条命题进行三专家独立审查并按多数票裁决，所给节选没有提供盲评、专家一致性统计或其他骨干模型的人工语义审查结果。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 同时关闭编译器引导修复和语义引导修复，对比启用两轮编译器引导修复 | 无修复时平均 elaboration rate 为83.1%，加入两轮编译器引导修复后达到96.9%，绝对提高13.8个百分点。 | 该对照主要隔离利用Lean编译诊断反复修正结构、名称和类型错误的作用。大幅提升说明多数可观测失败能够由机器可定位的编译反馈修复；但它没有测量题意是否忠实，因此不能据此认定修复后的命题在数学语义上更正确。 | 第4.2节，表2结果说明<br><span class="experiment-evidence">Two rounds of compiler guided repair increase it to 96.9%, whereas semantic-guided repair alone raises it to 88.7%.</span> |
| 仅启用语义引导修复，对比完全不修复 | 平均 elaboration rate 从83.1%提高到88.7%，绝对提高5.6个百分点，低于编译器引导修复带来的增幅。 | 这一设置考查语义裁判反馈单独作用时是否也会间接修正可编译性。较小的 elaboration 增益符合其设计目标，因为语义修复主要处理对象、假设、配置范围或结论表达不一致，而不是编译错误。由于节选没有给出表2的语义一致性分数，不能从88.7%推断语义修复效果较弱。 | 第4.2节，表2结果说明<br><span class="experiment-evidence">Without repair, the mean elaboration rate is 83.1%.</span> |

**定性案例**

- 历史IMO题形成了一类具有代表性的失败诊断案例：43条自动生成命题中有14条没有被当作单纯的“未证明”处理，而是由GeoProver给出Lean验证的反例；专家据此修正形式命题后，系统证明了全部14条修正版。其意义是反例可以区分“证明搜索不足”和“输入命题本身有问题”，但所给节选没有展示具体题目、反例构造或修正内容，无法判断错误主要来自遗漏退化条件、错误对象关系还是其他语义偏差。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution is an agentic LLM framework for formalizing, planning, repairing, and kernel-verifying Euclidean geometry proofs in Lean.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`8b6bd51108d77a9a40ddcf5bf58ec9fffa665c7f9077a22e0d712b7fdf06e46e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
