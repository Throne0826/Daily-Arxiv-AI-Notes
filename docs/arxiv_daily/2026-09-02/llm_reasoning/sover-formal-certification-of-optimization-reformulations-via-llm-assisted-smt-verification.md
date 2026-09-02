---
title: "[论文解读] SOVER: Formal Certification of Optimization Reformulations via LLM-Assisted SMT Verification"
description: "[arXiv 2609.00728][LLM Reasoning] 本文针对优化模型重写后难以可靠判定语义等价的问题，提出将大语言模型负责的符号映射与SMT求解器负责的形式认证分离，以验证可行域对应关系及全局目标排序是否保持。"
arxiv_id: "2609.00728"
announcement_date: "2026-09-02"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:46:36.019827+00:00"
source_sha256: "ad702cb0234e02a27e7baac0f68e6114eae6e8aaa6e60628ae5f804eb221641e"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "优化重构等价性"
  - "大语言模型辅助建模"
  - "SMT形式化验证"
  - "混合整数线性优化"
  - "连续非线性优化"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.00728</p>

# SOVER: Formal Certification of Optimization Reformulations via LLM-Assisted SMT Verification

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Swapnil Bhattacharyya, Mayank Baranwal</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: TCS Research, Mumbai；Affiliation: Indian Institute of Technology Bombay</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00728v1) · [PDF 下载](https://arxiv.org/pdf/2609.00728v1) · **关键词** 优化重构等价性, 大语言模型辅助建模, SMT形式化验证, 混合整数线性优化, 连续非线性优化<br>


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

本文针对优化模型重写后难以可靠判定语义等价的问题，提出将大语言模型负责的符号映射与SMT求解器负责的形式认证分离，以验证可行域对应关系及全局目标排序是否保持。

**不用术语来说**：同一个优化任务可以用不同变量、约束或目标函数来表达，但两份模型在少量测试中得到相同答案，并不代表它们始终等价：错误约束可能在测试实例上恰好不起作用，而目标函数经过正比例缩放后，最优解不变、最优值却会改变。因此，在采用大语言模型自动生成或改写优化模型时，需要一种不依赖有限次试算、能够从逻辑上判断改写是否保持原问题最优决策的方法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出SOVER混合验证框架：大语言模型解析优化陈述并提出变量、参数及变换之间的符号对应，随后由Z3或dReal检查形式化验证条件，从而把可能出错的语义理解环节与确定性的逻辑认证环节分开。
- 将等价判定从“最优值是否相同”提升为对可行域交叉可行性和全局目标次序保持性的验证，可覆盖混合整数线性模型、连续非线性模型、符号参数以及变量变换造成的异构表示；同时发布含100个等价对和50个困难非等价对的NLEquiv-150基准。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于数学优化、形式化验证与大语言模型辅助建模的交叉领域。数学优化通过在可行域上最小化目标函数来支持资源配置与决策；优化重构则将同一问题改写为另一种变量、约束或目标表达。本文关注的核心不是两个模型是否在若干实例上得到相同最优值，而是给定变量与参数之间的语义映射后，一个模型的可行解和最优解是否能够系统地对应到另一个模型。为此，SOVER让大语言模型负责从自然语言或数学表达中提取对应关系，再由满足性模理论（SMT）求解器对实数、整数等背景理论中的逻辑条件进行形式检查，从而减少局部最优、超时、数值误差和有限样本测试造成的误判。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**可行域与最优解集**

约束满足的所有变量取值构成可行域，记为$\mathcal{X}$；在最小化问题中，使目标函数达到最低值的全部取值构成最优解集$\arg\min$。只比较最优目标值可能遗漏解集结构，因此本文把解的对应关系作为等价性的重要依据。

</div>
<div class="concept-item" markdown="1">

**优化重构等价性**

两个表达式即使变量名称、约束形式或目标数值不同，也可能描述同一个优化问题。若映射$\Sigma$能把一个模型的可行解和最小化解对应到另一个模型的相应解，并保持目标的相对优劣顺序，本文将其视为$\arg\min$等价；因此目标函数乘以正数或施加严格递增变换不必导致非等价。

</div>
<div class="concept-item" markdown="1">

**SMT形式化验证**

SMT把关于整数、实数等理论的逻辑公式交给求解器判断可满足性。验证某个性质$\varphi$时，通常检查其否定$\neg\varphi$是否可满足：若不可满足，则不存在违反性质的赋值；若可满足，则求解器可提供反例。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是两个待比较的优化问题及其变量、参数、目标函数、约束和变量域，另有由大语言模型提取或提出的变量—参数映射$\Sigma$。源问题可写为$\min_{\mathbf{x}\in\mathcal{X}} f(\mathbf{x})$，其中$f$为目标函数、$\mathcal{X}$为约束诱导的可行域；目标是输出两个重构是否等价，而不是仅输出一次求解得到的最优值。本文假设映射能够表达两个模型之间的语义对应，并针对混合整数线性问题以及连续非线性问题分别构造可验证条件：前者检查域交叉可行性与全局目标次序保持，后者在容差语义下检查可行性、值域及$\epsilon$-argmin条件。验证结果应能说明是否存在违反等价性条件的赋值；若存在，则该赋值可作为反例。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathbf{x}$**

优化决策变量向量，通常属于$n$维实数空间或包含整数限制的变量空间。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{X}\subseteq\mathbb{R}^{n}$**

可行域，即同时满足模型约束和变量域限制的所有决策变量取值。

</div>
<div class="notation-item" markdown="1">

**$f:\mathbb{R}^{n}\to\mathbb{R}$**

源优化问题的目标函数；最小化时，目标值越小通常表示方案越优。

</div>
<div class="notation-item" markdown="1">

**$\Sigma$**

两个优化表述之间的变量、参数或表示形式映射，用于把一个模型中的赋值解释为另一个模型中的赋值。

</div>

</div>

**直接相关的工作**

- **EquivaMap（Zhai et al., 2025）**: EquivaMap同样使用大语言模型推断决策变量映射，再检查可行性和最优性，因此是本文最直接的相关工作。本文认为其轻量验证仍不足以覆盖约束不活跃、目标缩放或严格递增变换、符号参数以及线性到非线性表示变化等边界，并进一步以共享逻辑表示和SMT条件进行形式化检查。
- **OptiMUS（AhmadiTeshnizi et al., 2024）**: OptiMUS将自然语言描述翻译为混合整数线性规划，并通过自动测试调试求解代码，代表了大语言模型辅助优化建模路线。与其主要依赖测试和求解执行不同，本文关注已生成或已重构模型之间的语义等价性，并把结构解释与逻辑证明分离。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

优化模型广泛用于能源成本、供应链和利润决策，大语言模型也开始把自然语言需求翻译成正式模型或在不同建模语言之间进行重写。然而，这类自动生成结果可能遗漏假设、混淆变量、误写约束或改变问题结构。在高风险决策中，若仅凭求解器在若干实例上的输出接受重写模型，局部极小值、超时、数值误差或尚未激活的错误约束都可能掩盖语义偏差，因此需要可审查、可证明的改写正确性认证。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于求解结果或表面相似性的经验比较**：分别求解原模型与重写模型，比较有限实例上的最优解或最优值，或者依据公式文本、符号结构和采样结果的相似程度判断两者是否等价。
- **EquivaMap式大语言模型辅助映射验证**：先让大语言模型推断两份模型决策变量之间的变换，再检查映射后的模型是否保持可行性与最优性，以减少仅靠公式字面匹配造成的误判。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 有限次求解与最优值比较不能刻画全局语义：两个不同模型可能因错误约束在测试点不活跃而得到相同最优解和最优值；反之，正比例缩放或其他保持排序的目标变换会改变最优值，却不改变$\arg\min$。这会同时产生假阳性和假阴性。
- 现有检查尚不足以统一处理符号参数、混合整数变量、非凸连续模型以及由变量变换引起的线性模型到非线性模型等异构表示；若仍把生成式模型的判断直接当作结论，还会继承其映射遗漏与歧义，缺少独立的逻辑证书。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

仍缺少一种统一机制，能够在给定候选变量与参数映射后，不依赖大量独立求解或固定参数采样，而是在整个符号定义域上认证双向可行性，并确认目标函数对任意候选解的全局优劣次序得到保持；同时，该机制还应分别适配离散线性模型与带数值容差的连续非线性模型。

</div>
<div markdown="1"><span>核心问题</span>

能否把大语言模型仅用于提出跨模型的语义对应关系，再由SMT求解器独立验证这些对应关系，从而对混合整数线性重写给出精确的$\arg\min$等价认证，并对连续非线性重写给出容差感知的$\epsilon$-$\arg\min$保证？

</div>
<div markdown="1"><span>作者直觉</span>

判断两个优化问题是否保留相同最优决策，关键不是要求目标函数数值逐点相等，而是保证两件事：一份模型中的可行决策经映射后在另一份模型中仍然可行，以及任意两项可行决策的“谁更优”关系不会被颠倒。大语言模型擅长从不同写法中猜出变量、参数和变换的对应关系，却不适合充当正确性的最终裁判；SMT求解器则可以系统搜索违反上述性质的反例。二者分工后，只要找不到违反可行性或目标排序的反例，就能获得比有限试算更强的认证；对非线性情形再引入$\delta$与$\epsilon$容差，可使这一思路适应数值求解现实。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SOVER 的核心思想是把“理解两种建模写法之间的对应关系”与“证明它们确实等价”分开处理。输入是源优化问题 $P_A$、目标优化问题 $P_B$ 及其程序化模型文本；大语言模型只负责提出决策变量映射 $\mathcal{M}_V$ 和参数映射 $\mathcal{M}_P$，并通过一次定向修正减少重复或矛盾映射。随后，系统解析约束与目标函数，用映射 $\Sigma$ 将 $P_B$ 改写到 $P_A$ 的符号坐标系中，再由 SMT 求解器主动搜索“不等价”的反例。对于线性、混合整数和分段线性模型，Z3 依次检查可行域是否一致以及任意两个可行点的目标弱序是否一致；两类反例查询均为 UNSAT 时，依据命题 1 认证两 formulation 具有相同的全局最优解集合。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 模型解析与符号化

系统去除 addConstr、setObjective 等求解器 API 外壳，提取代数表达式，并按布尔、整数或实数等原生类型声明 SMT 符号。基准中的索引变量和矩阵表达式会在固定代理维度上展开。

<div class="method-step__io" markdown="1">

**输入**：源问题 $P_A$ 和目标问题 $P_B$ 的程序化 gurobipy 字符串，包括变量、参数、约束和目标表达式。<br>
**输出**：源模型的可行性谓词 $C_A$ 与目标 $O_A$，以及目标模型的可行性谓词 $C_B$ 与目标 $O_B$。

</div>

**直观理解**：这一步把“可执行的建模代码”翻译成逻辑求解器能够推理的数学句子。它不是运行优化算法，而是抽取模型究竟允许哪些解、如何评价这些解。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 变量与参数映射生成

沿用 EquivaMap 式的 LLM 语义匹配，生成决策变量映射 $\mathcal{M}_V$，并扩展生成目标系数、容量、边界和缩放常数等参数映射 $\mathcal{M}_P$。系统再执行一次定向提示修正，要求映射唯一，并删除缺乏显式聚合规则的多对一冲突。

<div class="method-step__io" markdown="1">

**输入**：$P_A$、$P_B$ 中决策变量和实例参数的名称、结构及语义信息。<br>
**输出**：经修正的候选映射集合 $\mathcal{M}_V\cup\mathcal{M}_P$，以及由此构造的符号替换 $\Sigma$。

</div>

**直观理解**：LLM 在这里相当于识别两份模型中“谁对应谁”的翻译员，例如判断一个新变量是否等于旧变量的线性变换。它只提出候选翻译，不拥有最终裁决权，因此语义猜测本身不会被直接当作等价证明。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 公共坐标系构造与投影

将 $\Sigma$ 代入目标模型，得到以源变量表示的 $\widetilde{C}_B$ 和 $\widetilde{O}_B$。若 $P_B$ 含有不进入目标函数的松弛变量或辅助变量，则对这些变量作存在量化投影，使比较对象是原变量上的可行集合，而不是维数更高的表示空间。

<div class="method-step__io" markdown="1">

**输入**：$C_B$、$O_B$ 以及候选替换 $\Sigma$。<br>
**输出**：同一符号坐标系中的两组表示 $(C_A,O_A)$ 与 $(\widetilde{C}_B,\widetilde{O}_B)$。

</div>

**直观理解**：只有把两种写法放到同一套坐标中，才能逐点比较。辅助变量类似中间计算栏：只要存在合适的中间值即可，不应因为两份模型的中间栏数量不同就判定它们不等价。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. Z3 两阶段反例验证

第一阶段求解 $\neg(C_A\leftrightarrow\widetilde{C}_B)$，寻找只被一侧判为可行的点；第二阶段创建源变量的影子副本以表示另一可行点，并寻找两目标对这两个点给出不同弱序的反例。查询为 SAT 时分别返回 Feasibility Mismatch 或 Ordering Mismatch，为 UNKNOWN 时返回 Inconclusive，两次均为 UNSAT 才返回 Pass。

<div class="method-step__io" markdown="1">

**输入**：公共坐标系中的 $C_A$、$O_A$、$\widetilde{C}_B$ 和 $\widetilde{O}_B$。<br>
**输出**：状态 Pass、Feasibility Mismatch、Ordering Mismatch 或 Inconclusive；若存在不一致，还可输出具体反例。

</div>

**直观理解**：验证器并不尝试枚举所有解，而是让逻辑求解器寻找一个足以推翻等价性的见证。找不到任何可行域反例，也找不到任何排序反例，才说明两种写法始终选择同一批全局最优点。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 可行域一致与目标弱序保持所蕴含的 argmin 等价

$$
\left[\forall \mathbf{x},\ C_A(\mathbf{x})\leftrightarrow\widetilde{C}_B(\mathbf{x})\right]\ \land\ \left[\forall \mathbf{x},\mathbf{y},\ C_A(\mathbf{x})\land C_A(\mathbf{y})\Rightarrow\left(O_A(\mathbf{x})\le O_A(\mathbf{y})\leftrightarrow\widetilde{O}_B(\mathbf{x})\le\widetilde{O}_B(\mathbf{y})\right)\right]\ \Rightarrow\ \arg\min_{\mathbf{x}:C_A(\mathbf{x})}O_A(\mathbf{x})=\arg\min_{\mathbf{x}:\widetilde{C}_B(\mathbf{x})}\widetilde{O}_B(\mathbf{x})
$$

**符号说明**

- $\mathbf{x},\mathbf{y}$：公共坐标系中的任意两个候选决策点。
- $C_A$：源问题的可行区域谓词；其值为真表示该点满足源问题全部约束。
- $\widetilde{C}_B$：经候选映射代入并在必要时投影辅助变量后的目标问题可行性谓词。
- $O_A$：源问题在公共坐标系中的目标函数。
- $\widetilde{O}_B$：经替换后以源坐标表达的目标问题目标函数。
- $\Sigma$：由变量与参数对应关系构造的候选坐标替换；该符号虽未显式出现在合并公式中，但决定带波浪号的谓词和目标。
- $\arg\min$：使目标达到全局最小值的全部可行点构成的集合，而不是单个求解器返回解。

<div class="equation-explanation" markdown="1">

**直观理解**：第一个条件要求两种模型允许的方案完全相同；第二个条件要求它们对任意两个可行方案的“谁不比谁差”判断完全一致。二者共同保证全局最优点集合一致，同时又不强求目标函数数值相同，这正是 SOVER 的线性与混合整数认证依据。<br>
**原文位置**：第 4.3.1 节，命题 1，公式 (1)–(3)；对应 Algorithm 1 第 15–35 行

</div>

</div>

<div class="equation-block" markdown="1">

#### 非线性问题的 $\epsilon$-最优集合及双向保持

$$
\Omega_{\epsilon}(P)=\left\{\mathbf{x}\in\mathcal{X}\ \middle|\ O(\mathbf{x})\le\inf_{\mathbf{y}\in\mathcal{X}}O(\mathbf{y})+\epsilon\right\},\qquad \Sigma\!\left(\Omega_0(P_B)\right)\subseteq\Omega_{\epsilon}(P_A),\quad \Sigma^{-1}\!\left(\Omega_0(P_A)\right)\subseteq\Omega_{\epsilon}(P_B)
$$

**符号说明**

- $P$：一个连续非线性最小化问题。
- $\mathcal{X}$：问题 $P$ 的可行集合。
- $O$：问题 $P$ 的目标函数。
- $\Omega_{\epsilon}(P)$：目标值距离全局下确界至多 $\epsilon$ 的全部可行点，即 $\epsilon$-最优区域。
- $\Omega_0(P)$：当全局最小值可达到时，问题 $P$ 的精确全局最优解集合。
- $\epsilon$：允许的目标次优误差，文中用于降低非线性边界点或平坦区域上的脆弱性。
- $\Sigma$：从 $P_B$ 可行集合到 $P_A$ 可行集合的双射坐标变换。
- $\delta$：dReal 的数值判定容差；命题要求相关失配查询返回 UNSAT，而不能用 $\delta$-SAT 作为等价证书。

<div class="equation-explanation" markdown="1">

**直观理解**：该式不要求一个问题的精确最优点映射后仍在另一问题中逐数值精确最优，而要求它至多比另一侧最佳目标差 $\epsilon$，且两个方向都成立。根据命题 2，在全局最小值可达到、$\Sigma$ 为可行集上的双射，并且双向可行性及裕量分离的优化失配查询均为 UNSAT 时，可获得这种容差化保证。<br>
**原文位置**：第 4.4.2 节，$\epsilon$-Argmin Equivalence 定义与命题 2

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。SOVER 不是通过数据训练一个等价分类器，也没有论文所定义的学习损失函数；LLM 被用作现成的映射提议器，最终判定来自 Z3 或 dReal 对反例公式的可满足性检查。这里真正被“优化”的对象仍是输入的数学规划问题，而 SOVER 自身执行的是逻辑认证：Z3 路径要求不存在可行域和目标弱序反例，dReal 路径要求相关容差化失配公式为 UNSAT。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. LLM 辅助语义映射模块**

该模块分别抽取决策变量映射 $\mathcal{M}_V$ 和参数映射 $\mathcal{M}_P$，可表达重命名、二元变量替换、线性或非线性坐标变换、参数缩放等关系。一次修正提示约束映射唯一性，并过滤没有显式聚合含义的多对一对应；但文中保证是相对于“给定候选映射”的条件性保证，不证明 LLM 必然找出正确或完整映射。

> 直观理解：两种数学模型可能使用完全不同的变量名、单位和坐标，因此不能直接逐字符串比较。LLM 擅长猜测这种结构对应，而后续形式验证负责发现猜错、漏映射或映射不满射等问题。

**2. Z3 精确弱序认证模块**

该模块面向线性、混合整数和分段线性算术，先验证 $C_A$ 与 $\widetilde{C}_B$ 的逻辑等价，再用两个任意可行点验证 $O_A$ 与 $\widetilde{O}_B$ 是否诱导相同弱序。它比较的是全局排序轮廓而不是目标表达式的代数恒等性，因此允许正比例缩放或其他严格单调变换；若目标模型含不参与目标的辅助变量，则在投影后的可行域上应用命题 1。

> 直观理解：最优解只取决于哪些点比哪些点更好，而不要求两边给出相同分数。例如把所有成本乘以正数会改变最优值，却不会改变最优方案；弱序检查能接受这种有效改写。

**3. dReal 容差感知非线性模块**

该模块使用 $\delta$-完备判定处理超越函数、非凸连续约束和非线性坐标变换。可行性检查采用大于 $\delta$ 的分离裕量，并把 $P_A\to P_B$ 方向表述为前向映射的值域覆盖：只有当某个 $P_A$ 可行点附近不存在任何可映射的 $P_B$ 可行点时才构成反例；优化部分则采用双向 $\epsilon$-argmin 检查，辅助变量通过量化可行性处理。

> 直观理解：非线性映射可能没有简单、全局单值的逆函数，仅检查一个代入公式容易错误接受非满射变换。值域覆盖直接询问每个目标点能否由另一侧实现，而 $\epsilon$-最优区域则允许平坦区域和边界附近不可避免的小误差。

**训练与推理**

系统没有单独的训练阶段。推理时，先输入一对优化 formulation，由 LLM 分别抽取变量和参数对应关系，并各进行一次修正；随后解析两侧模型、声明符号并将目标 formulation 代入源坐标。对于线性、混合整数或分段线性问题，Z3 先运行可行域反例查询，再运行双点目标排序反例查询：第一项 SAT 表示可行性失配，第二项 SAT 表示排序失配，UNKNOWN 表示无法下结论，只有二者均 UNSAT 才输出 Pass。对于连续非线性问题，系统改用 dReal 执行带分离裕量的双向可行性或值域覆盖检查，以及双向 $\epsilon$-argmin 失配检查；UNSAT 才构成认证，$\delta$-SAT 不作为等价结论。因而输出不仅是二分类，还包括失配类型、可能的反例以及不确定状态。

**复现信息**

输入采用程序化 gurobipy 字符串；系统去除求解器 API 语法，抽取代数约束与目标，并依据变量原生类型声明 Boolean、Integer 和 Real SMT 符号。索引变量及矩阵表达式在固定代理维度上展开，因此证书只覆盖该实例化维度，而不是自动覆盖任意维度；若要得到维度参数化结论，还需归纳证明或量化数组论证。线性路径使用 Z3，适用于线性、混合整数和分段线性算术；含超越函数、非凸连续约束或非线性坐标变换时使用 dReal。系统为每个问题对保存验证状态、生成的 SMT 公式、求解器输出、可用反例和诊断元数据到结构化 CSV，以便复查。需要特别注意，形式保证以解析正确和候选映射正确表达预期语义为前提；若 LLM 映射遗漏关键变量，系统可能无法验证真正的预期对应关系。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- EquivaFormulation：由NLP4LP优化问题经语义或代数变换构造。清洗元数据并排除添加有效不等式的变体“_e”后，实验保留九类变换，共2178对MILP重构，其中1449对等价、729对不等价。它主要测试线性替换、目标缩放、目标转约束、删除非活跃约束等结构变化下的等价判定。
- NLP4LP：EquivaFormulation的原始问题来源，本实验并未将其作为独立测试集报告结果；其作用是提供由自然语言描述及相应优化模型构成的基础问题。
- NLEquiv-150：作者新建的150对应用背景连续非线性重构，包括100对等价样本和50对故意设计的困难非等价样本。正例覆盖指数/对数、softplus、倒数、平方/平方根、logistic/odds、双曲函数、平移指数和三次变换；负例覆盖目标函数、约束、等式、方向、系数及值域不匹配等11类机制，用于检验容差感知的非线性验证能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**正确分类数与准确率**

衡量系统将每对模型判为等价或不等价时，与基准标签一致的数量及比例；表2按变换子类型报告正确数，正文报告总体准确率。 （越高越好，因为这表示系统同时减少了将非等价模型误判为等价和将等价模型误判为不等价的情况。）

</div>
<div class="metric-item" markdown="1">

**等价类与非等价类分别正确数**

分别统计正例和负例上的正确分类，用来检查总体准确率是否由某一占多数的类别主导，并特别观察困难负例能否被拒绝。 （两类数值均越高越好；只在等价正例上表现好并不足以证明系统能够发现细微语义偏差。）

</div>
<div class="metric-item" markdown="1">

**端到端时间**

从LLM映射抽取到最终判定的整体运行时间。所给片段的时间表只完整展示了端到端时间行，未提供硬件、统计方式以及完整的形式验证器单独耗时。 （越低通常越好，但必须在相近准确率和相同运行条件下比较；仅凭当前片段不能进行严格的效率结论。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### EquivaFormulation上的总体端到端MILP等价判定

<div class="result-value" markdown="1">

SOVER正确分类2173/2178对，准确率为99.77%；其中等价样本正确1446/1449，不等价样本正确727/729。相比之下，作者复现的EquivaMap为1935/2178，即88.84%。

</div>

作者结果表明，在LLM抽取映射可能不完美的端到端条件下，显式检查可行域与目标次序比已有映射检查流程更稳定，而且性能并非只来自某一类别。然而，这一结果只覆盖所选九类MILP变换，不能直接证明对任意混合整数模型或分布外重构都同样有效。

<div class="result-source" markdown="1">

来源：第5.4节 Results and Analysis；分类子类型明细见表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On EquivaFormulation, SOVER correctly classifies 2173/2178 MILP pairs (99.77%): 1446/1449 equivalent and 727/729 non-equivalent.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### NLEquiv-150连续非线性重构，包括困难负例

<div class="result-value" markdown="1">

SOVER正确分类149/150对，即99.33%，并正确识别全部50/50个困难非等价样本；100个等价样本中正确99个，唯一错误由变量映射抽取不完整导致。

</div>

该结果支持dReal容差验证能够发现多类细微非线性语义不匹配，并表明至少在此基准上没有把困难负例误认证为等价。唯一错误发生在验证前的LLM映射阶段，说明整体系统的瓶颈可能是语义对齐而非形式检查。不过，基线并未在这些新样本上评估，因此不能据此量化SOVER相对其他方法的非线性优势；数据集由作者构造且规模仅150对，也不足以代表所有非线性优化形式。

<div class="result-source" markdown="1">

来源：表2及其表注；_m+行为99/100，_m-行为50/50

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Counts are end-to-end with LLM-extracted mappings; the sole _m+ miss is an incomplete map.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 对表面差异大或单一最优解观察容易误导的变换子类型

<div class="result-value" markdown="1">

在目标缩放“_i”上，SOVER为242/243，而字符级规范匹配为0/243；在目标转约束“_f”和线性替换“_h”上，SOVER均为243/243；在删除非活跃约束的困难非等价“_l”上为241/243。

</div>

这些子类型说明形式验证的价值来自语义而非文本相似度：目标缩放或变量替换可以显著改变表达形式，却仍保持优化次序；反过来，删除当前解处看似不起作用的约束，可能改变全局可行域，不能通过比较一次求解所得最优点来认证。不过，这是不同测试子类型之间的对比，而不是严格控制其他因素的组件消融。

<div class="result-source" markdown="1">

来源：第5.4节 Results and Analysis；各子类型计数见表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

It obtains 242/243 on objective rescaling (_i), where canonical matching obtains 0/243, and perfect accuracy on objective-to-constraint (_f) and linear-substitution (_h) variants.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 非线性实验缺少同表基线：表2明确说明原有基线面向EquivaFormulation设置，因而未在NLEquiv-150上报告。由此可以评价SOVER在该新数据集上的绝对正确率，却不能严格判断其相对现有非线性等价检查方法的提升幅度。
- 端到端系统依赖LLM抽取变量映射，NLEquiv-150唯一错误即来自不完整映射；此外，所给片段未报告多次LLM采样的方差、不同模型后端的逐项结果、硬件与超时设置，也未给出错误样本的完整分析，因此稳定性、可复现成本和规模扩展能力仍需源文及代码核验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- EquivaMap：与SOVER最直接的基线，同样先由LLM生成变量映射，再检查可行性和最优性。比较它可以判断SOVER的形式验证义务是否比已有的映射后检查流程更可靠。
- Naive LLM Prompting：零样本地要求LLM直接输出二元等价判断，不显式生成变量映射，也不调用求解器。它用于检验仅依赖语言模型表面推理是否足够。
- Weisfeiler-Lehman Graph Test（WLT）：把优化模型表示为二部图，并通过迭代颜色细化比较结构。它代表不执行数值或逻辑语义验证的结构匹配方法。
- Canonical Accuracy：对规范化后的声明进行逐字符精确匹配。它是严格的表面形式基线，用来说明语义等价模型可能具有完全不同的文本或代数表达。

**实验想回答的问题**

- SOVER能否在端到端条件下，即变量映射由LLM自动抽取而非人工提供时，准确判定线性与连续非线性优化重构是否保持可行域及最优性语义？
- 相较于LLM直接分类、已有映射检查方法、图结构匹配和字符串规范匹配，基于SMT的可行域与目标次序验证是否对表面形式变化及隐蔽语义错误更稳健？

**实验实现**

每个实例由一个原始优化模型和一个变换后的模型组成，系统使用LLM抽取二者之间的变量映射，再执行形式验证。EquivaFormulation先清理会破坏SMT声明的元数据：用正则表达式删除“positive”“continuous”“non-negative”等定性维度描述；没有显式索引时，将空形状或非索引形状视为标量。实验评估每个原模型的九种变换，并排除添加有效不等式的“_e”，因为作者关注结构等价性而非特定实例或求解器行为。连续非线性验证以前向映射为主：使用dReal检查映射后的可行性及反向值域覆盖，并设置$\delta=10^{-5}$、分离裕量$10^{-3}$和$\epsilon=10^{-3}$。全部2328对样本均按端到端流程计数，其中映射由LLM抽取；原文片段未明确报告训练/验证/测试划分，基准更接近固定测试集上的确定性验证评估。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 删除非活跃约束的“_l”子类型可视为代表性困难案例：某约束在一次求解得到的最优点处可能不活跃，删除后观察到的最优值也可能暂时不变，但全局可行域已经扩大，因此模型未必等价。SOVER通过显式可行域检查取得241/243，而不是把单一最优解的一致性当作证明；原文片段未提供某个具体实例的公式级追踪。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The core contribution uses LLM-extracted mathematical mappings and formal SMT verification to certify optimization reformulations.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`ad702cb0234e02a27e7baac0f68e6114eae6e8aaa6e60628ae5f804eb221641e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
