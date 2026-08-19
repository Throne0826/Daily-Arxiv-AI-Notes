---
title: "[论文解读] Admission Without Answers: Label-Free Certification and Experience Learning for LLM-Based Optimization Modeling"
description: "[arXiv 2608.15565][LLM Reasoning] 本文研究在没有标准答案的真实优化任务流中，如何用外部生成、统计校准的行为证据判断大语言模型生成的优化模型是否值得写入经验库，并允许系统在证据不足时拒绝自动决策或转交人工。"
arxiv_id: "2608.15565"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:24:43.825054+00:00"
source_sha256: "a0d1c08bc156551178a625515091241b290e300cd447367f2a4c5cf9a722a317"
tags:
  - "LLM Reasoning"
  - "大语言模型优化建模"
  - "无标签接纳"
  - "经验学习"
  - "行为验证"
  - "错误发现率校准"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.15565</p>

# Admission Without Answers: Label-Free Certification and Experience Learning for LLM-Based Optimization Modeling

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Junbo Jacob Lian, Huiling Chen, Hanzhang Qin, Chung-Piaw Teo</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Institute of Operations Research and Analytics；Affiliation: National University of Singapore, Singapore；Affiliation: College of Computer Science and Artificial Intelligence；Affiliation: Wenzhou University, Wenzhou, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.15565) · [PDF 下载](https://arxiv.org/pdf/2608.15565) · **关键词** 大语言模型优化建模, 无标签接纳, 经验学习, 行为验证, 错误发现率校准<br>
**代码**: [https://github.com/junbolian/AdmitOR](https://github.com/junbolian/AdmitOR)

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

本文研究在没有标准答案的真实优化任务流中，如何用外部生成、统计校准的行为证据判断大语言模型生成的优化模型是否值得写入经验库，并允许系统在证据不足时拒绝自动决策或转交人工。

**不用术语来说**：基于大语言模型的优化建模智能体会把过去生成的模型总结成可复用经验，但错误经验一旦进入长期记忆，可能在后续任务中被反复检索并传播。现有系统通常依靠已知最优答案判断经验是否正确，而真实业务工单往往没有答案；仅检查代码能否运行或让模型评价自己，也无法确认模型是否真正表达了题意。因此，系统需要一种不看标准答案、又能控制错误经验混入比例的准入办法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出 AdmitOR：从题目中提取参数域，对候选优化模型进行实例重采样，比较来自三个模型家族、不同提示策略和求解器栈的价值函数轨迹，再以跨家族一致性团概括证据，并通过校准阈值输出“接纳、弃权或升级人工处理”。其关键区别是把无标签准入明确表述为具有错误发现率目标的统计决策，而不是把一次运行成功或简单多数一致当作正确性证明。
- 作者不仅比较不同准入判据对经验库精度和下游性能的影响，还完整报告校准保证向真实任务流迁移失败的负面结果：当基准题目文本不能忠实描述其带标签实例，或不同模型家族共享同一错误的基础规格提取时，跨模型一致仍可能共同确认错误。这一审计明确了方法成立所依赖的观测与分布迁移条件。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究的是利用大语言模型将自然语言运营问题转化为可执行优化模型，并通过经验学习把已验证的模型、技能或示例存入可复用知识库。优化模型通常包含决策变量、目标函数和约束条件，求解器据此返回一个或多个可行解及其目标值；经验学习的关键不只是生成模型，还包括判断哪些生成结果足够可靠、可以进入持久化库。本文聚焦于无答案场景：真实工单流没有现成最优值或人工标签可供核验，因此需要依据模型在外部测试实例上的行为来决定是否接纳。该接纳过程还必须控制错误接纳的比例，否则错误模型会污染知识库，并在后续检索中反复传播。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**优化建模与价值函数**

优化建模是把自然语言中的资源、决策和规则写成决策变量、目标函数与约束条件组成的数学模型。给定输入实例后，模型由求解器执行并产生目标值；在本文中，跨多个测试实例得到的目标值序列被视为可比较的行为证据。

</div>
<div class="concept-item" markdown="1">

**经验学习与知识库污染**

经验学习会把过去问题中提炼出的技能或模型保存起来，在新问题上检索和复用。若错误模型被接纳，它会成为“污染”记忆，导致后续系统更频繁地检索并使用错误经验，从而降低整体建模准确率。

</div>
<div class="concept-item" markdown="1">

**选择性接纳与错误发现率**

选择性接纳允许系统在证据不足时拒绝接纳或暂缓决定，而不是对所有候选模型二选一地放行。错误发现率（$\mathrm{FDR}$）表示被接纳候选中错误候选所占的期望比例，本文用校准阈值控制这一风险，并将输出划分为接纳、弃权和升级处理三种状态。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一批由大语言模型生成的候选优化模型，以及从候选文本中提取出的参数域和可执行实例；系统假设候选模型能够被相应求解器运行，但不拥有这些实例的真实答案或最优值。对每个候选模型，接纳门从三个模型家族、不同提示策略和求解器栈中产生或执行模型，并在参数域内重采样多个测试实例，记录各实例上的目标值或价值函数轨迹。系统随后比较不同家族的行为一致性，以跨家族团的结构汇总证据，再使用在校准数据上确定的阈值输出接纳、弃权或升级。最终输出不仅是单个候选模型的决定，还包括进入经验库的模型集合；研究目标是在无标签流中提高接纳精度、减少错误记忆，同时维持可量化的错误发现率控制。该设定的关键边界是校准分布与部署流之间需要满足传递假设；文中报告的野外流实验表明该假设可能失败。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D_{\mathrm{task}}$**

待处理的任务或工单分布，表示自然语言运营问题及其对应参数实例的来源。

</div>
<div class="notation-item" markdown="1">

**$x$**

一个具体优化实例，例如由参数域重采样得到的容量、利润或需求参数组合。

</div>
<div class="notation-item" markdown="1">

**$V_m(x)$**

候选模型 $m$ 在实例 $x$ 上经求解器执行后产生的价值函数或目标值，用于描述模型的外部行为。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{FDR}$**

错误发现率，即所有被接纳候选中实际错误候选的比例；本文将其作为接纳门需要校准和控制的风险指标。

</div>

</div>

**直接相关的工作**

- **带标签的经验学习系统：基于已知最优值、真实标签轨迹或专家示例的经验库方法**: 这些方法能够利用答案判断哪些模型或技能应进入知识库，但依赖真实答案书。在本文的无标签场景中，真实工单不提供该监督信号，AdmitOR因此以跨模型家族、跨重采样实例的执行行为作为替代证据，并在同一经验学习系统中用原有真实标签裁判作为参考比较。
- **自验证、投票与评审式接纳方法**: 执行成功、自我评估和多数投票可以在没有答案键的情况下运行，但它们可能只检查可执行性、在单个实例上比较结果，或受到共同错误和候选答案锚定影响，因而不能可靠控制被接纳错误的比例。AdmitOR通过让多个模型家族先独立生成并执行模型，再比较其跨实例价值函数轨迹，并配合校准的错误发现率预算，针对这些不足设计接纳机制。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

优化建模智能体需要从持续到来的自然语言工单中积累技能，但这些工单通常只有问题描述，没有可用于核验候选模型的标准最优值。准入错误的代价具有长期性：错误模型被总结并存入经验库后，会在未来检索中影响多个任务。原文以其无标签任务流说明风险并非边缘现象：只按执行成功接纳了 $878$ 个候选模型，其中 $241$ 个与暂时隐藏、仅供事后审计的答案不一致。因此，实际需求不是让系统尽量多存经验，而是在缺少答案时优先控制被接纳经验中的错误比例，并把不确定样本留给弃权或人工升级。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **依赖答案或专家的监督式准入**：既有经验学习器通过比较候选模型的最优值与已知答案、使用真实标签评价生成轨迹，或者由专家预先筛选高质量示例，只有通过核验的内容才进入经验库。这类方式能直接检查结果，却把答案键、人工标注或专家策展作为运行前提。
- **无标签的内部检查与单实例共识**：在没有答案时，系统可检查生成代码是否成功执行、采信模型的自我评价，或让多个候选模型在原始实例上求解并以多数票或数值一致作为准入依据。此类方法使用成本较低，但证据主要来自候选系统自身，且通常只观察一个参数点。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 监督式准入遭遇作者所称的“标签墙”：真实工单流没有答案簿，持续获得最优答案或专家标注的成本也会抵消自动经验学习的价值。因此，这些方法适合有标注基准，却不能直接支持开放、持续到达的生产任务。
- 执行成功、自我评价或原始实例上的一致都不是语义正确性的充分证据。一个错误模型可能语法合法且可求解；多个不同模型也可能只在当前参数值上偶然得到同一目标值，却在参数变化后表现不同。反过来，如果所有候选都以同一种方式误读文本，它们甚至会在多个重采样实例上持续一致，说明简单共识无法识别共享偏差。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种面向持续经验库的无标签准入机制：它需要利用不依赖标准答案的外部行为证据区分稳定一致与单点巧合，将证据强度映射到明确校准的错误发现率目标，并在证据不足时允许弃权或升级；同时还应清楚说明该统计目标从校准数据迁移到真实任务流所需的假设及其失效方式。这里的错误发现率指被系统接纳的候选中错误候选所占比例的总体控制目标，而不是对每个单独候选作绝对正确保证。

</div>
<div markdown="1"><span>核心问题</span>

在看不到任务标准答案的条件下，能否通过独立生成的候选模型在重采样参数实例上的行为轨迹及跨家族一致性，构造一个经过统计校准的准入门，并使其建立的经验库比执行成功或多数投票产生更少的错误记忆、更高的下游建模效果；这种校准保证又在什么迁移条件下成立或失败？

</div>
<div markdown="1"><span>作者直觉</span>

若两个候选模型只是在原始实例上碰巧给出相同最优值，改变需求量、容量或收益等参数后，它们的最优值变化轨迹通常会分开；真正表达同一优化关系的模型则更可能在一组重采样实例上持续一致。再要求一致集合跨越不同模型家族、提示方式和求解技术栈，可以减少同源生成错误造成的虚假共识。最后用已审计数据校准一致性门槛，而不是凭经验设阈值，便可把“证据看起来很强”转化为可检验的准入风险目标；但该直觉仍以不同证据源不会共享同一文本理解错误、校准分布与部署流具有适当可迁移性为条件。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

AdmitOR 是一个面向大语言模型优化建模的“无标签准入门”。输入是一道自然语言优化题及其题面给定参数，同时由多个模型家族生成可执行候选模型；系统不依赖该题的标准答案，而是在题面参数附近重采样多个实例，比较候选模型的目标值函数轨迹。若来自至少两个模型家族的候选在所有有效实例上形成足够强的最大团共识，且共识分数超过由独立合成数据校准得到的阈值，系统就输出 accept 和认证目标值；证据不足时输出 abstain，数据提取冲突或需要追加证据时输出 escalate。只有 accept 对应的求解轨迹会进入经验库。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造去相关候选面板

使用三个模型家族、不同提示策略和不同求解器栈生成候选集合 $\mathcal{C}=\{M_1,\ldots,M_k\}$，并记录每个候选的家族标签 $f(M_i)$。每个候选 $M_i$ 都必须是可执行程序，能够在任意允许参数 $\theta$ 下建模、求解并返回目标值 $V_{M_i}(\theta)$。

<div class="method-step__io" markdown="1">

**输入**：自然语言优化题票据 $x$，其中包含参数向量 $\theta\in\Theta$ 及题面参数值 $\theta_0$。<br>
**输出**：带模型家族标签的可执行候选面板 $\mathcal{C}$。

</div>

**直观理解**：这相当于让使用不同工具、具有不同训练背景的建模者独立作答。跨家族设计旨在降低所有候选因共享训练数据、提示模板或求解器接口而犯同一种错误的概率，但不能消除所有成员共同误读题意的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 提取参数域并重采样实例

提取器大语言模型从题面识别参数键、基准值及各参数的相对或绝对扰动范围，构造以 $\theta_0$ 为锚点的参数域；结构尺寸参数保持固定，并通过规则检查冲突范围和退化区间。随后独立采样 $\theta_1,\ldots,\theta_m$，在每个实例上执行所有候选并记录目标值与求解状态；因不可行或执行失败而缺少足够可比结果的实例被标为 uninformative。

<div class="method-step__io" markdown="1">

**输入**：题票据 $x$、题面基准参数 $\theta_0$ 和候选面板 $\mathcal{C}$。<br>
**输出**：包含基准实例和多个有效扰动实例的执行日志，即各候选的采样值函数轨迹 $\{V_{M_i}(\theta_j)\}$。

</div>

**直观理解**：系统不只检查候选在原题数字上是否碰巧得到同一答案，而是轻微改变价格、容量等参数，观察其输出曲线是否仍一致。原题实例始终被保留，因此认证结果仍对应用户实际提交的问题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 建立值函数共识

若两个候选在某实例上的目标值在相对容差内一致，则视为该实例上一致；只有它们在全部有效实例及基准实例上均一致时，才在候选一致性图中连边。系统寻找覆盖至少两个模型家族的最大团，将该团在 $\theta_0$ 上的公共值作为候选认证答案，并为团外候选给出一个发生分歧的具体重采样实例。

<div class="method-step__io" markdown="1">

**输入**：所有候选在基准实例与有效扰动实例上的目标值和求解状态。<br>
**输出**：跨家族最大团、候选认证值 $\hat z=V(\theta_0)$、团覆盖家族数、团大小、有效实例数以及局部分歧诊断。

</div>

**直观理解**：图中的团是一组彼此在整段测试轨迹上都相符的候选，而不只是原题答案相同的候选。改变参数后，遗漏约束等结构错误通常会被激活，系统也能指出错误候选在哪个实例开始偏离。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 校准阈值并作三态决策

将词典序三元组编码为有限标量分数，并在可达阈值网格 $T$ 上计算经验错误率 $\hat p_\tau$ 和 Clopper–Pearson 上置信界 $U_\tau$；选择同时满足名义目标 $\alpha$ 与有限样本预算 $2\alpha$ 的最低阈值 $\tau^*$。部署时，证据达到阈值则 accept，证据不足则 abstain，参数提取冲突、有效实例过少或需追加候选与实例时则 escalate。

<div class="method-step__io" markdown="1">

**输入**：由家族覆盖数、最大团大小和有效实例数构成的词典序证据分数，以及带有构造性真值的独立合成校准集。<br>
**输出**：accept、abstain 或 escalate；accept 同时携带认证值、最大团证据和统计证书，其他状态携带证据不足或数据层冲突的诊断。

</div>

**直观理解**：最大团并不自动等于正确答案，因此还要用已知真假的合成题估计“多强的共识才值得放行”。阈值关注的是被放行集合中错误认证所占比例，而不是承诺每一道被放行的题都绝对正确。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 校准阈值选择规则

$$
\tau^{\ast}=\min\left\{\tau\in T:\widehat{p}_{\tau}\leq\alpha,\ U_{\tau}\leq 2\alpha\right\}
$$

**符号说明**

- $\tau^{\ast}$：最终选定的最低准入分数阈值。
- $T$：部署分数能够取得的有限阈值网格；试点中共有四个可达值。
- $\widehat{p}_{\tau}$：校准集中分数不低于阈值 $\tau$ 的已接受认证之经验错误比例。
- $\alpha$：名义错误认证比例选择目标，论文设为 5%。
- $U_{\tau}$：根据校准错误计数计算的水平为 $1-\delta$ 的 Clopper–Pearson 精确上置信界。
- $2\alpha$：有限样本证书所允许的错误认证概率上界；论文设置下为 10%，与名义选择目标不同。

<div class="equation-explanation" markdown="1">

**直观理解**：系统从较宽松到较严格的候选阈值中，选择第一个同时满足两项条件的阈值：观测错误率不超过名义目标，且考虑有限校准样本的不确定性后，上置信界仍不超过认证预算。第二项防止系统仅因校准样本太少、碰巧没观察到错误就过度放行。<br>
**原文位置**：第 3 节 Step 4，Proposition 2（Calibrated admission）

</div>

</div>

<div class="equation-block" markdown="1">

#### 固定阈值与数据依赖阈值的有限样本保证

$$
\Pr\!\left(p_{\tau}\leq U_{\tau}\right)\geq 1-\delta,\qquad \Pr\!\left(p_{\tau^{\ast}}\leq 2\alpha\right)\geq 1-|T|\delta
$$

**符号说明**

- $p_{\tau}$：分数至少为 $\tau$ 的已接受认证中，错误认证的真实概率。
- $U_{\tau}$：固定阈值 $\tau$ 下由校准数据得到的 Clopper–Pearson 上置信界。
- $\delta$：每个固定阈值的置信失败概率。
- $p_{\tau^{\ast}}$：采用校准数据选择出的阈值 $\tau^{\ast}$ 后，被接受认证的真实错误概率。
- $|T|$：被同时考察的可达阈值数量。
- $\alpha$：名义错误认证比例目标；有限样本结论控制到 $2\alpha$。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分说明，对预先固定的任一阈值，其真实错误认证概率以至少 $1-\delta$ 的概率不超过计算出的上界。第二部分考虑阈值本身由校准数据选择所带来的多重比较代价：所有阈值同时成立的置信度降为至少 $1-|T|\delta$；在 Assumption 1 的交换性条件下，该结论才能从合成校准集迁移到真实部署准入流。<br>
**原文位置**：第 3 节 Step 4，Proposition 2（i）至（iii）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：AdmitOR 本身不是通过梯度训练一个新的优化模型，因此没有常规意义上的损失函数。它优化的是准入策略：在经验错误率满足 $\widehat p_\tau\leq\alpha$、有限样本上界满足 $U_\tau\leq2\alpha$ 的阈值中选择最小的 $\tau$，以尽量保留可接受经验，同时控制已接纳集合中的错误认证比例；更严格的阈值通常提高准入精度，但增加 abstain 并降低准入召回。宿主学习器的蒸馏目标保持不变，只是训练数据由“标准答案标注的轨迹”替换为“经 AdmitOR 认证并以 $\hat z$ 重标注的轨迹”。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 跨家族候选面板**

候选由三个模型家族在不同提示策略和求解器后端下独立产生，系统显式保留 $f(M_i)$，并要求形成正证据的最大团至少覆盖两个家族。该约束降低同一家族共享训练数据、建模习惯或接口错误所造成的相关失败，但作者明确指出，所有家族共同误读题面时该模块无法发现错误。

> 直观理解：单一家族内部的多数票可能只是多个相似模型重复同一种错误；跨家族共识要求不同来源的建模程序表现一致，因此证据更强。它证明的是独立行为之间的一致性，而不是直接证明这些行为符合出题者的真实意图。

**2. 基准锚定的值函数轨迹检验**

候选 $M$ 由值函数 $V_M(\theta)$ 表示，两个候选仅在整个参数域 $\Theta$ 上值函数相同才称为等价。对于线性与混合整数模型，作者依据 Proposition 1 说明：在满维扰动域中，若两个候选不等价，其分歧区域包含开集；连续独立重采样遗漏该区域的概率会随样本数 $m$ 几何下降，下降速度取决于分歧区域的概率质量。

> 直观理解：两个错误程度不同的模型可能在一个参数点上恰好给出相同最优值，所以只检查原题答案无法识别结构差异。把参数改变多次，相当于从多个角度给模型做压力测试；分歧区域越大、采样次数越多，持续漏检的可能性越低。

**3. 有限样本校准准入器**

部署分数按家族覆盖数、最大团大小和有效实例数进行词典序排序并编码为有限标量；试点中的可达网格满足 $|T|=4$，成对数值裕量仅记录而不参与分数。阈值通过求解器可验证的合成校准题选择，保证依赖证书可交换性假设：分数至少为 $\tau$ 的部署认证，在真假标签方面须与相同分数的校准认证可交换；若采用自适应升级策略，校准与部署还必须使用同一升级策略。

> 直观理解：该模块把“看起来共识很强”变成可审计的放行标准，并为放行集合的错误比例提供有限样本上界。保证是有条件的：如果真实数据与合成校准题的错误规律不同，或部署时改变了追加证据的策略，原证书就可能失效。

**训练与推理**

离线校准阶段，系统在按构造即可验证真值、且经过分层抽样的合成优化问题上运行完全相同的准入门。对每个可达分数阈值 $\tau\in T$，统计接受证书的真假，计算 $\widehat p_\tau$ 与 Clopper–Pearson 上界 $U_\tau$，再按 Proposition 2 选择 $\tau^*$；若线上会对边界案例追加实例或候选，离线校准也必须复现同一升级阶梯。论文还指出，当校准的零假设计数充分增长时，可用基于 split-conformal 的 $p$ 值和 Benjamini–Hochberg 程序替代有限阈值网格证书，以在相应交换性条件下控制实现的错误发现率。

部署推理阶段，对每张无标签票据只需题面 $x$，无需答案键。系统依次生成跨家族候选、提取并校验以 $\theta_0$ 为锚点的扰动域、采样并执行多实例、构造一致性图和跨家族最大团，再用已冻结的 $\tau^*$ 作出三态决策；accept 返回 $\hat z$ 及证书并进入蒸馏，abstain 不进入经验库，escalate 则触发人工处理或与校准策略一致的追加证据流程。该推理过程控制的是长期被接纳流的错误发现率，而不是逐题的确定性正确。

**复现信息**

公平复现需要保留以下关键设置：候选来自三个模型家族并使用不同提示和求解器后端；参数域必须包含原题基准点 $\theta_0$，结构尺寸参数固定，冲突范围回退到相对扰动，退化范围需扩宽并记录警告；所有候选在同一批独立采样参数上运行，目标值按相对容差比较，执行失败、不可行或可比候选过少的实例不得计入一致性证据，且判决前必须达到最低有效实例数。正共识必须是覆盖至少两个家族的最大团，部署分数只使用家族覆盖、团大小和有效实例数，不能事后把成对裕量加入分数而继续沿用原校准证书。

试点的数据层提取器数量为 $E=1$，但完整设计要求多个提取器家族就参数键集合与基准值达成容差内一致，否则转入 escalate；这一简化会留下参数提取的单点故障。校准使用 $\alpha=0.05$、每阈值 $\delta=0.05$ 和四点网格，因此作者给出的有限样本预算为 $2\alpha=0.10$，数据依赖阈值的同时置信度为 $1-|T|\delta=0.80$；若要求 $95\%$ 的四阈值同时解释，应以 $\delta=0.0125$ 重新计算。以上证书还依赖题面能忠实确定待评分实例，以及校准认证与部署认证在相同分数下具有真假标签交换性。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 下游评测由五个公开优化建模基准组成：ComplexOR、IndustryOR、Mamo.C、OptMATH 和 OptiBench，共 $1100$ 个题目。它们用于评估不同准入判断器所构建技能库对宿主经验学习系统的实际帮助；Macro 对五个基准等权平均，Micro 则按题目数加权。原文未明确报告各基准的完整划分方式；已知 OptiBench 含 $605$ 个题目，ComplexOR 中单个题目可影响 $1.11$ 个宏平均百分点。
- 标签盲经验收集流包含 $300$ 个优化问题。系统对每个问题使用 DeepSeek-V3.2、GPT-5.4 和 Claude Sonnet 4.6 三个模型家族各生成一个候选，再由四种准入判断器重放同一批候选与求解日志。该数据流用于控制候选生成差异，使各实验组只在准入判断器上不同。
- 密封答案库（sealed vault）仅用于实验后评价判断器，而不参与 AdmitOR 的候选认证。它用于计算候选级准入精度和召回率，并检验标签无关认证在未知样本上的错误发现控制；当前节选未给出答案库规模及其构造细节。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**下游准确率（Macro 与 Micro）**

使用 round-aware scorer 衡量宿主系统装备某一技能库后，在五个公开基准上的正确率。Macro 将五个基准等权平均，避免大数据集完全主导结论；Micro 在全部 $1100$ 个题目上按样本数加权，更接近总体逐题成功率。 （越高越好，因为它直接表示准入策略形成的技能库能否帮助宿主系统正确完成新的优化建模任务。）

</div>
<div class="metric-item" markdown="1">

**准入精度（admission precision）**

在判断器准入的候选模型中，经密封答案库确认正确的比例。它衡量技能库准入内容的纯净度，并对应论文关于错误发现控制的核心目标。 （越高越好，因为较高精度表示错误候选更少进入技能库；但该指标不能单独反映因过度保守而漏掉多少正确经验。）

</div>
<div class="metric-item" markdown="1">

**准入召回率（admission recall）**

所有正确且可执行的候选中，被判断器成功准入的比例。执行成功基线按定义达到 $1.0$；该指标与准入精度共同描述宽松准入和选择性认证之间的取舍。 （通常越高越好，因为它表示保留了更多正确经验；但若提高召回率同时引入大量错误经验，未必会改善下游性能。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 五个公开基准上的下游性能：AdmitOR 与 Ground truth、Execution success、Majority vote 使用同一批收集日志，仅替换准入判断器。

<div class="result-value" markdown="1">

AdmitOR 在 ComplexOR、IndustryOR、Mamo.C、OptMATH、OptiBench 上分别取得 $66.67\%$、$39.00\%$、$57.82\%$、$56.02\%$、$72.23\%$，Macro 为 $58.35\%$，Micro 为 $63.91\%$。其 Macro 高于 Ground truth 的 $53.89\%$、Execution success 的 $56.51\%$ 和 Majority vote 的 $54.82\%$；同时其技能库只有 $101$ 个文件，小于执行成功的 $163$ 个、多数投票的 $145$ 个和 Ground truth 的 $130$ 个。

</div>

作者据此主张，无标签认证没有给下游经验学习造成明显的性能上限，而且更高选择性的认证可以用更小的技能库获得更高准确率。分析上，这一结果较有说服力，因为所有组重放同一批日志，主要差异确实集中在准入政策；但它不能证明任何规模、任何宿主或任何优化领域中，选择性认证都必然优于宽松准入。

<div class="result-source" markdown="1">

来源：表 2，AdmitOR 行；第 4.2 节另报告各技能库文件数

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

AdmitOR 66.67 39.00 57.82 56.02 72.23 58.35 63.91

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### AdmitOR 与 Majority vote 的配对统计比较，以五个基准等权的 Macro 为统计量。

<div class="result-value" markdown="1">

AdmitOR 相对 Majority vote 提升 $3.53$ 个宏平均百分点，$95\%$ bootstrap 区间为 $[+0.87,+6.75]$。两者逐基准比较时，AdmitOR 在五个基准上均不低于多数投票，并满足作者预注册的 K2 判据。

</div>

区间下界仍高于 $0$，说明在本文配对评测样本和重采样方案下，该优势不只是一个点估计波动。它隔离的是“认证规则相对简单多数共识”的增益，而不是候选模型或生成次数的增益；不过 bootstrap 区间只反映当前基准项目的采样不确定性，不自动覆盖模型版本、提示词或数据分布变化。

<div class="result-source" markdown="1">

来源：第 4.2 节；图 4 位于附录 C

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Against majority vote, the gain is +3.53 points, with a 95% interval of [+0.87,+6.75].

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 候选认证覆盖范围与失败原因分析，对 $300$ 个标签盲问题执行基础实例和重采样实例认证。

<div class="result-value" markdown="1">

认证得到 $174$ 个 accept、$114$ 个 uninformative、$10$ 个 abstain 和 $2$ 个 error。$114$ 个 uninformative 中，$65$ 个主要由重采样实例不可行导致，$45$ 个是至少两个候选始终不返回数值，另有 $4$ 个来自执行失败；这些案例并非候选证据相互冲突。

</div>

这表明认证覆盖率的主要瓶颈不仅是严格的一致性标准，也包括重采样实例质量、候选执行稳定性和求解工具链。换言之，uninformative 不应直接解释为模型意见冲突或方法拒绝正确答案；它更多表示现有执行框架未产生足够证据。该分析揭示了系统工程改进可能带来的额外覆盖率，但没有报告修复这些问题后的下游增益。

<div class="result-source" markdown="1">

来源：第 4.2 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Of these cases, 65 are dominated by infeasible resampled instances, 45 contain at least two candidates that never return a value, and 4 result from execution failure.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测标签和宿主基础设施都存在已确认的噪声：ComplexOR 至少有一个错误最优值标签，OptiBench 有 $85$ 个题目在技能选择阶段失败，OptMATH 复现还存在已知的 $3$ 至 $5$ 个百分点缺口。虽然作者固定协议并进行了敏感性分析，但五个基准的绝对分数，尤其是 Ground truth 组与 OptMATH 的分数，仍需谨慎解释。
- 实验固定使用三个特定模型家族、两类求解栈、每个家族一个温度 $0$ 候选以及 $m=5$ 个重采样实例。现有证据能够支持这一配置下 AdmitOR 优于多数投票，却不足以证明其对其他模型组合、随机采样温度、求解器、重采样数量或更广泛优化问题分布具有同等优势；此外，$114$ 个 uninformative 案例显示当前认证覆盖率明显受执行框架限制。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Ground truth：使用真实答案标签决定经验是否准入，代表有监督判断器。它是检验“无标签是否形成下游性能上限”的直接参照，但其结果仍会受到错误标签和宿主技能选择异常的影响。
- Execution success：只要候选能够执行并返回结果便准入，是最宽松的无标签基线。它检验大量但可能受污染的经验，能否依靠技能库规模弥补较低准入精度。
- Majority vote：依据三个候选模型的多数一致意见准入，是无需真实标签的共识基线。它能检验 AdmitOR 的认证规则是否比简单的模型间投票更可靠。
- AdmitOR：论文提出的无标签认证判断器，也是主要实验方法。它综合三个模型家族的输出、求解日志、基础实例及 $m=5$ 个重采样实例，允许返回 accept、uninformative、abstain 或 error，并为准入决定保留可审计证据。

**实验想回答的问题**

- 在完全不使用答案标签的情况下，基于多候选一致性与求解验证的 AdmitOR 准入机制，能否产生足以支持后续经验学习的技能库，并达到或超过使用真实标签、仅检查执行成功、或多数投票所产生技能库的下游优化建模准确率？
- 提高候选经验的准入精度是否能稳定改善下游性能；这种优势在配对统计检验、异常样本敏感性分析以及不同模型家族的失败模式下是否仍然成立？

**实验实现**

宿主经验学习器使用发布的完整流程，固定骨干模型为非思考模式的 DeepSeek-V3.2，温度为 $0$；除失败处理和调用日志外不修改宿主。候选面板包含 DeepSeek-V3.2、GPT-5.4 和 Claude Sonnet 4.6，每个家族在温度 $0$ 下生成一个候选；第一、第三个家族采用直接建模，第二个采用结构化策略。求解栈分为 Pyomo 搭配 HiGHS 与 gurobipy。每次认证使用必需的基础实例和固定随机种子生成的 $m=5$ 个重采样实例。模型版本、提示词、容差和求解器版本均固定，认证运行与宿主生成运行彼此独立。

四种判断器重放完全相同的候选生成结果和求解日志，再将各自准入的轨迹交给未经修改的宿主蒸馏过程，因此技能库之间的设计变量只有判断器。认证共返回 $174$ 个 accept、$114$ 个 uninformative、$10$ 个 abstain 和 $2$ 个 error；候选级评价分别覆盖执行成功的 $878$ 个候选、多数投票的 $721$ 个候选和 AdmitOR 的 $413$ 个候选。下游区间采用按基准分层的配对 bootstrap，在每个基准内部重采样 $10000$ 次，并在宏平均尺度上报告 $95\%$ 区间。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| OptiBench 技能选择异常的敏感性分析：从所有实验组中同时移除受影响的 $85$ 个题目，以保持配对比较。 | 移除异常题目后，AdmitOR 相对 Majority vote 的 Macro 增益为 $3.49$ 个百分点，$95\%$ 区间为 $[+0.82,+6.69]$，与原始分析的 $3.53$ 点基本一致；相对 Ground truth 的增益则从 $4.46$ 点缩小为 $2.14$ 点，区间为 $[+0.05,+4.29]$。 | 该分析隔离了宿主技能选择器反复生成不存在标识符这一非建模故障。AdmitOR 对 Majority vote 的优势几乎不变，说明论文的预注册核心比较不依赖这批异常；相对 Ground truth 的领先明显收窄，则表明原始的部分优势确实来自 Ground truth 技能库触发了更多选择阶段故障，而不能全部归因于准入内容质量。 | 第 4.2 节，OptiBench 异常敏感性分析<br><span class="experiment-evidence">The gain over majority vote is unchanged at +3.49 points, [+0.82,+6.69]. The gain over the ground-truth arm narrows to +2.14 points, [+0.05,+4.29].</span> |

**定性案例**

- ComplexOR 中有一个实例的公开标签为 $200$，但复现管线返回 $250$，人工验证确认 $250$ 才是真正最优值。因此正确输出在公开评分中被惩罚：按原标签复现得分为 $66.7\%$，修正标签后为 $72.2\%$，恰好匹配已报告结果。作者仍在主结果中保留公开标签，并让该错误同等影响所有方法。这个案例说明 Ground truth 组和绝对准确率并非无噪声标准，也解释了为何论文更重视同日志、同评分协议下的配对比较。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Develops label-free certification and experience learning for LLM generation of optimization models, centering on structured problem-solving reliability.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`a0d1c08bc156551178a625515091241b290e300cd447367f2a4c5cf9a722a317`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
