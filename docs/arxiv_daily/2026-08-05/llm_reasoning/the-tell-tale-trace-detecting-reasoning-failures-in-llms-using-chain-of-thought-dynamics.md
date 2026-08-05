---
title: "[论文解读] The Tell-Tale Trace: Detecting Reasoning Failures in LLMs Using Chain-of-Thought Dynamics"
description: "[arXiv 2608.03291][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.03291"
announcement_date: "2026-08-05"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:38:45.978046+00:00"
source_sha256: "3a992ba2737b2521a53e243402db4fa01bba651aa2082a7a43278b624c84b610"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "思维链"
  - "推理动态"
  - "推理失败检测"
  - "布尔可满足性"
  - "能力前沿"
  - "过程监测"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.03291</p>

# The Tell-Tale Trace: Detecting Reasoning Failures in LLMs Using Chain-of-Thought Dynamics

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Shashwat Sourav, Aishwarya Balwani</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Department of Physics, Washington University in St. Louis；Department of Developmental Neurobiology, St. Jude Children’s Research Hospital</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03291v1) · [PDF 下载](https://arxiv.org/pdf/2608.03291v1) · **关键词** 大语言模型, 思维链, 推理动态, 推理失败检测, 布尔可满足性, 能力前沿, 过程监测<br>


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

大语言模型可通过思维链（Chain-of-Thought，CoT）在回答前生成自然语言形式的多步推理，这既是一种增加测试时计算的方法，也为监测推理过程提供了可见接口。传统过程监督和逐步验证通常判断单个中间步骤在语义上是否正确或一致，但一条推理链的失败也可能分散在整个轨迹中，表现为某类操作出现得过早、反复循环或过早结束；同时，可见CoT未必忠实记录模型内部计算，因此不能直接当作机制解释。本文据此研究“可见推理动态”：不要求每句话忠实对应内部过程，而是考察不同推理功能在整条轨迹中的次序、重复、转移与时机是否能揭示能力边界附近的推理失败。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链（CoT）**

模型在给出最终答案前生成的自然语言中间推理序列，可表示为“推理轨迹加最终输出”。本文把它视为可观察的行为证据，而非必然忠实的内部计算记录。

</div>
<div class="concept-item" markdown="1">

**布尔可满足性（SAT/UNSAT）**

给定由布尔变量和子句组成的逻辑公式，若存在一组变量赋值使所有子句同时为真，则为SAT；若任何赋值都不能满足公式，则为UNSAT。SAT通常可用一个候选赋值直接验证，而UNSAT往往需要系统枚举情形并推出矛盾。

</div>
<div class="concept-item" markdown="1">

**能力前沿与能力匹配**

能力前沿指某模型从大多能解到经常失败的任务难度区域。能力匹配是在各模型各自的这一难度区域比较相近实例，使正确与错误轨迹并存，避免把失败简单归因于任务过难或把成功归因于任务过易。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是复杂度可系统调节、且具有外部可验证真值的布尔可满足性问题；模型生成一条可见CoT及最终SAT或UNSAT判断。研究者按句切分CoT，并依据每句话承担的推理功能加标签，再比较正确与错误轨迹的角色密度、功能转移、循环、熵和结束时机，目标是识别分布于整条轨迹的失败模式、在最终答案输出前提供预警，并据诊断设计针对性的提示干预。核心假设不是“CoT忠实描述内部计算”，而是即使缺乏这种忠实性，其可见组织结构仍可能携带与推理成败相关的行为信号；实验比较集中于五种LLM配置各自能力前沿附近的可比问题。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\langle \mathrm{CoT}, y \rangle$**

模型的完整可见响应，其中CoT是自然语言推理轨迹，$y$是最终输出或SAT/UNSAT判断。

</div>
<div class="notation-item" markdown="1">

**$F$**

待判断的布尔公式，由变量及其子句构成。

</div>
<div class="notation-item" markdown="1">

**$a$**

对公式中布尔变量的一组候选真值赋值；若该赋值满足$F$的全部子句，则可证明$F$为SAT。

</div>
<div class="notation-item" markdown="1">

**$r_{1:T}$**

切分并标注后的推理功能序列，$r_t$表示第$t$个句子的推理角色，$T$表示轨迹中的句子数。该符号是为概括问题设置而采用的记法，原文节选未明确给出统一符号。

</div>

</div>

**直接相关的工作**

- **Uesato et al. (2022); Lightman et al. (2024) 的过程监督与逐步验证研究**: 这些方法主要评估单个中间步骤的语义有效性或一致性，用于发现错误或塑造推理过程；本文转而分析错误是否以跨步骤、分布式的轨迹结构变化出现。
- **Lee et al. (2026), ReasonOps: operator segmentation for LLM reasoning traces**: 该工作从可见CoT中归纳反复出现的推理算子，并用于轨迹完成前的正确性预测；本文进一步关注任务依赖的推理功能次序、复现与时间结构，以及这些信号能否指导特定推理程序的纠正。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大语言模型即使写出了看似连贯的思维链，也可能在多步推理中逐渐偏离正确程序并最终给出错误答案。若监控系统只能检查最终答案或寻找某个局部错误步骤，就难以及时发现分散在整条推理轨迹中的失败模式，更无法据此选择有针对性的纠正策略。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **过程监督与逐步验证器**：把思维链拆成若干中间步骤，逐一判断每一步在语义上是否正确、前后一致，并将判断用于错误定位、训练监督或推理时筛选。
- **推理轨迹与内部状态分析**：不只检查孤立语句，而是研究推理随时间的变化；已有工作利用隐藏状态的轨迹差异、认知阶段转换、重复出现的推理操作或答案不确定性的演化来预测错误并触发干预。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 逐步语义检查通常把可见思维链视为模型真实推理的可靠记录，但模型可能省略真正影响答案的因素，或在结论形成后生成貌似合理的解释。因此，语句层面的正确性既不一定反映内部计算，也可能因直接优化中间文本而变得更具迷惑性。
- 现有轨迹研究虽表明推理的位置、演化和组织方式具有预测价值，却尚未充分刻画特定任务中的能力失败如何体现为可见推理功能的先后顺序、重复结构与发生时机，也未明确这些动态信号能否在答案输出前识别失败，并进一步导出与错误程序相匹配的纠正方案。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

缺少一种不要求思维链忠实呈现内部计算、同时又能在模型自身能力边界附近进行受控比较的分析框架，用来识别成功与失败轨迹之间分布式、任务依赖的结构差异，并把诊断结果转化为程序层面的定向干预。

</div>
<div markdown="1"><span>核心问题</span>

在不假设可见思维链具有语义忠实性的前提下，推理功能的排序、转移、循环、密度与结束时机能否揭示任务依赖的能力失败；这些迹象能否在最终答案产生前被检测，并用于设计针对具体推理程序缺陷的纠正策略？

</div>
<div markdown="1"><span>作者直觉</span>

即使模型说出的每句话都不是内部计算的逐字记录，整条思维链仍可能留下稳定的行为痕迹。例如，模型可能过早从探索转入验证、反复执行相似操作，或在本应构造反证时执着于检验候选解。把句子按推理功能归类并观察这些功能如何随轨迹展开，就像不必相信一个人的全部自述，也能从其行动顺序和反复模式判断其解题策略是否失衡；一旦识别出这种程序错配，提示词便可直接要求模型采用更合适的证明步骤。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文提出的不是一个需要训练的新神经网络，而是一套基于可见思维链动态的诊断与干预流程。输入是经外部求解器认证的合取范式布尔可满足性公式，以及多个大语言模型在三种提示框架下生成的逐步推理和最终答案；流程先按模型能力选择成功与失败并存的难度区间，再把每条思维链切分为句子并映射为粗粒度推理角色，随后从角色序列提取密度、转移、循环、熵和结束时机等轨迹特征。研究者在同一公式、同一提示条件下配对比较正确与错误回答，用这些特征诊断 SAT 与 UNSAT 的不同失败程序，并进一步评估前缀预警及针对 UNSAT 错误的证明搜索提示修复。
直观地说，该方法不逐句裁判模型“说得是否在语义上正确”，也不假定模型写出的思维链忠实呈现内部计算；它把整条推理看成一条行为轨迹，观察模型在“规划、尝试赋值、检查、回退、寻找矛盾、作答”等活动之间怎样移动。这样可以识别分散在全过程中的异常组织方式，例如过早陷入重复检查，或在本应证明不存在解时仍持续搜索候选解。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造并认证 SAT/UNSAT 任务

使用外部 SAT 求解器独立确定每个实例的 SAT 或 UNSAT 标签。SAT 回答只有在模型报告 SAT、给出可解析赋值且该赋值通过全部子句检查时才算正确；对 UNSAT 实例则依据求解器标签评价模型报告的结论，但不把模型的自然语言论证当作形式证明。

<div class="method-step__io" markdown="1">

**输入**：复杂度可控的合取范式公式；每个公式由若干子句组成，模型需要判断是否存在一个布尔变量赋值使全部子句同时为真。<br>
**输出**：带有求解器真值标签、复杂度等级和可验证评价规则的任务集合，以及区分完整正确、完整错误、截断或循环、格式失败等情形的结果标签。

</div>

**直观理解**：求解器相当于独立裁判，因此模型不能靠一段听起来合理的解释被判正确。SAT 需要拿出一个确实有效的解，UNSAT 则要求结论与求解器认定的“无解”一致。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 采样推理并匹配模型能力前沿

对同一公式在三种提示条件下收集可见思维链和最终答案，并分别估计模型 $m$ 在复杂度等级 $\ell$ 上的经验准确率 $\widehat{p}_{m,\ell}$。只把准确率位于预设混合成功区间的模型—难度组合视为能力前沿，以避免用对强模型过易、对弱模型过难的固定等级进行失衡比较。

<div class="method-step__io" markdown="1">

**输入**：固定公式、五个被评估模型，以及基线求解提示 $T0$、监督者关注谨慎性的框架 $D1$、强调子句跟踪与假设检查的框架 $D2$。<br>
**输出**：位于各模型能力边界附近、同时含有成功与失败样本的推理轨迹，以及保持公式和提示条件不变的分歧配对案例。

</div>

**直观理解**：这相当于给每位考生选择“会做一部分、也会错一部分”的题，而不是让所有人做同一难度。只有在这种区间里，正确轨迹和失败轨迹的差异才具有可比性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 句子级角色标注与动态特征提取

先将思维链切为句子，再用基于正则规则的分类器为每句赋予粗粒度功能角色。SAT 角色包括规划、赋值、验证、回溯、结束和其他；UNSAT 分析还加入矛盾搜索、显式 UNSAT 证明构造、SAT 承诺和子句检查等角色，随后由角色序列计算角色密度、转移矩阵、循环率、加权自转移、转移熵与归一化结束时机。

<div class="method-step__io" markdown="1">

**输入**：一条由 $T$ 个句子组成的可见思维链及其句子序列。<br>
**输出**：每条思维链的角色序列 $r_1,\ldots,r_T$ 及固定维度的轨迹动态特征。

</div>

**直观理解**：方法把每句话压缩成“这一步在做什么”，而不是判断这句话是否忠实揭示模型内部。之后统计模型是否长期停在同一种活动、是否反复走相似路径，以及多早开始宣布答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 配对诊断与前缀预警

在同一公式和同一提示条件下，将一个模型的完整错误回答与另一模型的正确回答配对，并用配对 Wilcoxon 符号秩检验和配对 bootstrap 置信区间比较动态特征；同时补充同模型族及同模型分析，以检查模型写作风格的混杂。预警实验按不断增长的思维链前缀重算特征，使用每个模型自身的基线正确轨迹完成尺度变换和阈值校准，并按问题划分校准集与评估集，使同一公式不会进入两部分。

<div class="method-step__io" markdown="1">

**输入**：正确和完整错误轨迹的动态特征、匹配的公式—提示条件，以及模型自身在基线提示下的正确轨迹。<br>
**输出**：SAT 与 UNSAT 的失败动态诊断、仅由前缀触发的错误警报、检测性能及从首次警报到最终答案的句子级提前量。

</div>

**直观理解**：配对设计相当于让两条轨迹回答完全相同的问题，从而尽量把差异归因于推理过程而不是题目。前缀实验则模拟在线监控：模型还没有说出最终答案时，系统逐步观察其行为是否已偏离该模型通常的正确轨迹。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 模型能力前沿判据

$$
0.30 \leq \widehat{p}_{m,\ell} \leq 0.90
$$

**符号说明**

- $\widehat{p}_{m,\ell}$：模型 $m$ 在复杂度等级 $\ell$ 上的经验准确率
- $m$：被评估的大语言模型索引
- $\ell$：SAT 公式的复杂度等级

<div class="equation-explanation" markdown="1">

**直观理解**：只有当某个模型在某个难度上的经验准确率介于 $30\%$ 与 $90\%$ 时，该模型—等级组合才被纳入混合成功的能力前沿。下界保证有足够正确轨迹，上界保留足够失败轨迹；作者明确说明这只是本研究采用的临时规则，并非普适的能力边界定义。<br>
**原文位置**：Methodology，Capability frontiers and capability matching

</div>

</div>

<div class="equation-block" markdown="1">

#### 推理角色转移矩阵

$$
P_{ij}=\Pr\!\left(r_{t+1}=j\mid r_t=i\right)
$$

**符号说明**

- $P_{ij}$：当前角色为 $i$ 时，下一句角色转移到 $j$ 的条件概率，即行归一化转移矩阵的元素
- $r_t$：思维链第 $t$ 个句子的功能角色
- $r_{t+1}$：思维链第 $t+1$ 个句子的功能角色
- $i$：当前句子的角色类别
- $j$：下一句的角色类别
- $t$：句子在思维链中的位置索引

<div class="equation-explanation" markdown="1">

**直观理解**：该式把整条思维链表示为角色之间的移动规律：对每种当前角色，统计下一句落入各角色的比例。这个矩阵是循环、自转移和转移多样性等动态指标的基础，使分析关注推理活动如何演化，而非只计算某类句子出现了多少次。<br>
**原文位置**：Methodology，Reasoning dynamics and analysis protocols

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文没有训练或微调语言模型，也没有提出通过梯度下降优化的损失函数；句子角色由规则正则分类器赋值，动态特征用于统计比较、阈值检测和诊断。定向证明搜索属于推理时提示干预，其作用是改变模型被诱导执行的推理程序，而不是更新模型参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 求解器认证与结果分类模块**

外部 SAT 求解器提供与模型文本独立的真值标准。推理结果被划分为 $\text{correct\_complete}$、$\text{wrong\_complete}$、$\text{truncated\_or\_looping}$ 和 $\text{format\_failure}$；UNSAT 的核心错误子类为 $\text{wrong\_sat\_complete}$，即对求解器认证的 UNSAT 公式给出完整但错误的 SAT 结论。

> 直观理解：该模块把“推理逻辑错了”和“文本没生成完或格式无法读取”分开，避免把生成故障混入完整推理失败。它也保证正确性来自外部检查，而不是从思维链自己的说法反推。

**2. 功能角色轨迹模块**

规则分类器将句子映射为少量功能角色，再从 $r_1,\ldots,r_T$ 计算各角色出现比例及相邻角色转移。循环率描述近期角色模式的重复，加权自转移描述停留在同一角色的持续性，转移熵描述下一角色选择的多样性，结束时机则记录开始输出答案的位置在整条轨迹中的归一化比例。

> 直观理解：这些量共同描述推理的“节奏和路线”，而不是某一个句子的真假。低多样性、高重复和过早结束可表示模型尚未充分探索就陷入固定检查模式，但具体含义仍需结合 SAT 或 UNSAT 的任务要求解释。

**3. 能力匹配、校准与干预模块**

跨模型分析以相同实例和提示为配对单位，并在每个模型自己的混合成功难度附近取样；在线分数的尺度和阈值仅由该模型在基线提示下的正确轨迹确定。UNSAT 修复则对同一批原始错误案例比较通用重试与指定证明程序的定向提示，从而区分随机重采样效应和程序引导效应。

> 直观理解：不同模型的典型长度和表达习惯不同，不能共享一个未经校准的异常阈值。修复实验设置通用重试作为对照，是为了判断改进究竟来自“再抽一次答案”，还是来自补上诊断所指出的证明步骤。

**训练与推理**

完整流程全部发生在任务生成、模型推理和离线分析阶段。首先生成并由求解器认证不同复杂度的 CNF 公式；随后让 Qwen3-8B、Qwen3-14B、Llama3-8B、Llama3-70B 和 OLMo2-13B 在 $T0$、$D1$、$D2$ 三种提示下对固定公式生成思维链。依据求解器核验和可解析性标注结果，再按每个模型的经验准确率选择能力前沿等级并建立同题同提示的正确—错误配对。
分析时，系统对可见思维链做句子切分、规则角色标注和动态特征汇总，然后进行配对统计检验。早期预警将问题集合一分为二：一半只用于从模型自身的 $T0$ 正确轨迹确定重缩放方式与检测阈值，另一半专门评估；系统随着前缀增长重复计算得分，首次越过阈值即报警。UNSAT 干预不自动触发，而是在已知的 Llama3-70B 错误 SAT 案例上事后重跑；分别使用通用重试和定向证明搜索提示，并以求解器重新核验输出。

**复现信息**

公平解释结果所需的关键设置有四点。第一，三种提示保持公式和答案要求不变，$D1$ 与 $D2$ 被视为受控的措辞框架扰动，而不是预设会诱发欺骗或隐藏信念与报告分离。第二，完整错误与截断、循环、不可解析输出分开处理，主要推理动态比较针对可完整评价的回答。第三，跨模型主要配对包括 Llama3-8B 错误对 Qwen3-14B 正确、OLMo2-13B 错误对 Qwen3-14B 正确，以及为减轻模型族风格混杂而设置的 Llama3-8B 错误对 Llama3-70B 正确；另用同模型比较作为更严格的风格控制。第四，UNSAT 稳健性分析同时采用删除最终答案与承诺句、排除全部答案相关特征两种处理，避免检测器仅靠结论词识别错误。
统计上，匹配案例使用配对 Wilcoxon 符号秩检验，并通过配对 bootstrap 给出置信区间；修复实验在相同错误案例上比较干预前后，并采用 McNemar 检验。角色标注器是规则正则系统而非学习分类器，因此结果可能受角色词典和句子切分规则影响；源文将完整提示、结果定义、角色分类法、特征细节、预警校准和干预协议分别放在补充材料 A–H 节，复现时应以这些细则为准。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 实验数据不是现成基准，而是自动生成并由外部求解器认证的合取范式布尔公式，难度分为 L2–L6 五个序数等级。SAT 样例要求模型报告 SAT 并给出满足全部子句的完整赋值；UNSAT 样例的真实标签由求解器证明。该设计使答案正确性不依赖自然语言推理是否看似可信，同时允许按难度定位各模型正确与错误并存的能力前沿。
- SAT 动态比较集由同一“公式—提示条件”上的完整回答构成，只比较 $correct\_complete$ 与 $wrong\_complete$，不把截断、循环未作答或格式失败混入推理错误。跨模型匹配包括 105 个 Llama3-8B 错误而 Qwen3-14B 正确的配对；另报告 91 个至少有一个模型正确且至少有一个模型错误的分歧单元，以及 97 个 Llama3-8B 模型内错误—正确配对。
- UNSAT 诊断集重点考察 $wrong\_sat\_complete$：求解器认定公式不可满足，但模型完整地声称 SAT。Llama3-70B 提示干预使用同一批 UNSAT 样例，其中原始条件下共有 52 个错误 SAT 回答；早期预警则按唯一公式 ID 划分 50% 校准集和 50% 测试集，同一公式的全部生成轨迹只能进入一侧，以避免公式泄漏。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**求解器验证准确率与错误纠正率**

准确率衡量最终答案经外部求解器检查后正确的比例；对 SAT，必须同时给出可解析且满足所有子句的完整赋值。纠正率则是在原先错误声称 SAT 的样例中，干预后改为正确答案的比例。 （越高越好，因为它直接反映可验证任务是否被正确解决；但它本身不能说明模型采用了什么推理过程，也不能证明模型内部原先已经知道答案。）

</div>
<div class="metric-item" markdown="1">

**思维链动态指标**

包括轨迹字符数、句子数、验证与回溯密度、完整轨迹循环率、功能标签之间的转移熵及开始最终作答的位置。循环率刻画重复相似操作的程度；转移熵刻画推理功能切换的多样性；密度指标刻画某类推理句子所占比例。 （不存在统一的越高越好方向。本文将更高循环率、更低转移熵和更早最终化解释为推理过早收缩的迹象，但长度和验证密度受模型家族及回答风格影响，不能单独当作质量分数。）

</div>
<div class="metric-item" markdown="1">

**AUROC 与提前量**

AUROC 衡量动态检测分数在不同阈值下区分正确与错误完整轨迹的排序能力，0.5 附近相当于随机排序；提前量以句子数表示错误被标记到最终答案之间的距离，同时报告最终答案前被成功标记的错误比例。 （AUROC、预先标记比例和正的提前句数越高越有用，因为检测器能够更可靠、更早地发出警告；但这些数值依赖具体模型、难度区间、校准划分和阈值，不能直接视为跨模型通用性能。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### SAT 同题同提示的匹配比较，重点为 105 个 Llama3-8B 错误、Qwen3-14B 正确的跨家族配对，并以模型家族内比较检查稳健性。

<div class="result-value" markdown="1">

跨家族比较中，错误轨迹平均字符数为 3293.60，而正确轨迹为 7936.14；验证密度为 0.61 对 0.49，循环率为 0.56 对 0.45，转移熵为 0.58 对 0.85，且均达到 $p<.001$。错误轨迹从全程 77.1% 的位置开始最终化，正确轨迹则为 89.8%。不过，家族内比较并不支持错误轨迹必然更短或验证更多；较稳定的共同特征是循环增多和转移熵降低。

</div>

作者将该模式称为“过早验证坍缩”：失败回答没有简单地漏看更多子句，因为子句覆盖率差异不显著，而是过早进入狭窄、重复的检查模式，并更早承诺最终答案。通俗地说，问题不一定是“没读题”，而更像是“很快选定一种检查套路并反复执行，缺少继续探索和修正”。这是一种轨迹层面的关联证据；由于长度和验证密度受到模型家族影响，不能把“短”或“验证多”单独当作通用失败判据。

<div class="result-source" markdown="1">

来源：Results，SAT failures show a recurring collapse in reasoning dynamics；Table 1、Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across 105 matched Llama3-8B-wrong/Qwen3-14B-correct pairs, wrong traces are roughly half as long, more verification-heavy and more cyclic, and markedly lower in transition entropy (Table 1), beginning finalization at 77.1% of the trace rather than 89.8%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 在按公式 ID 隔离的 50% 校准集与 50% 测试集上，对逐渐展开的部分思维链进行动态失败检测。

<div class="result-value" markdown="1">

在校准集确定的阈值下，Llama3-8B 有 80.2% 的完整错误轨迹在最终答案前被标记，中位提前量为 23 句；OLMo2-13B 为 78.2% 和 17.5 句；Llama3-70B 仅为 35.7%，中位提前量为 0 句。部分轨迹的检测分数仅在接近结尾时才高于随机水平，而且效果随模型及其所处能力区间变化。

</div>

可见思维链动态对某些模型确实能形成提前预警，说明失败结构不总是到最终标签出现时才可观察。然而，Llama3-70B 的零句中位提前量意味着许多警报直到答案附近才出现，实际干预价值有限。该实验验证的是“按模型校准后，在特定能力前沿上是否能预警”，并未得到可直接迁移到任意模型、难度或阈值的通用检测器。

<div class="result-source" markdown="1">

来源：Results，Reasoning dynamics provide model-dependent early warnings；Figure 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At the threshold set on the calibration half, 80.2% of Llama3-8B wrong-complete traces are flagged before the final answer with a median lead time of 23 sentences, and 78.2% of OLMo2-13B traces with 17.5 sentences, whereas Llama3-70B reaches only 35.7% with zero median lead time (Figure 5, right).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### UNSAT 能力前沿上的错误类型和轨迹结构分析，比较错误声称 SAT 的完整轨迹与正确判断 UNSAT 的轨迹。

<div class="result-value" markdown="1">

Llama3-70B 的能力前沿准确率从 SAT 上的 0.526 降至 UNSAT 上的 0.159，其全部完成回答中有 0.800 是错误 SAT 声称。错误轨迹较少进行矛盾搜索或构造 UNSAT 证明，反而更多检查候选赋值并循环，表现得像在用寻找单个满足赋值的程序解决本应证明不存在满足赋值的问题。

</div>

SAT 与 UNSAT 虽使用同一公式语言，却要求不同程序：SAT 只需找到一个成功赋值，UNSAT 则必须排除所有可能性或构造矛盾。结果表明，许多 UNSAT 失败不是模型停止作答，而是它带着“应该存在解”的预设不断验证候选赋值，最后错误宣布 SAT。作者据此提出过程错配解释，但可见轨迹仍只是外显行为，不能证明这些文字忠实记录了模型内部计算。

<div class="result-source" markdown="1">

来源：Results，UNSAT failures substitute assignment search for contradiction proof；Figure 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Llama3-70B is most affected, its frontier accuracy falling from 0.526 on SAT to 0.159 on UNSAT, with false SAT claims accounting for 0.800 of its completions.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 失败检测明显依赖模型、难度区间和校准分布：Llama3-70B 的提前检测较弱，UNSAT 的作答前 AUROC 接近随机。因此当前方法不是跨模型通用检测器，且在几乎全对或普遍失败的能力区间中难以稳定评估。
- 研究分析的是可见思维链结构，并未证明外显文字忠实对应模型内部计算；证明搜索提示的成功也不能推出模型原先“知道”正确答案。修复实验还是事后针对已知 UNSAT 错误进行，原文未展示在缺少真实标签时可靠触发干预的方法。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 同题同提示的正确轨迹：例如将 Llama3-8B 或 OLMo2-13B 的错误轨迹与 Qwen3-14B 的正确轨迹配对。固定公式和提示框架后，差异更可能来自回答过程与模型行为，而不是题目难度。
- 模型家族内比较：Llama3-8B 错误轨迹对 Llama3-70B 正确轨迹，用来检验“过早验证坍缩”是否只是不同模型家族的语言风格或回答长度造成。结果显示循环增多和转移熵降低较稳定，但长度与验证密度并不稳定。
- 原始提示与通用重试：在 Llama3-70B 的 UNSAT 错误上，原始条件给出未经修复的参照，通用重试检验单纯增加一次采样或要求重做是否足够，而不明确改变求解程序。
- 定向证明搜索提示：明确要求分类讨论和矛盾搜索，与通用重试形成机制性对照。若它显著改善 UNSAT 表现，并同步改变轨迹中的矛盾搜索与 SAT 承诺密度，则更支持“错误过程可被提示纠正”的解释。

**实验想回答的问题**

- 在外部求解器可验证的布尔可满足性任务中，正确与错误回答的可见思维链是否呈现系统性的轨迹差异，尤其是这些差异能否在控制同一公式和提示条件后仍然成立，并在最终答案产生前提供失败预警？
- SAT 与 UNSAT 错误是否对应不同的过程性失效机制；若 UNSAT 错误源于模型采用了错误的搜索程序，而不只是输出了错误标签，那么针对矛盾证明与分类讨论的提示能否定向修复这些错误？

**实验实现**

实验评估 Qwen3-8B、Qwen3-14B、Llama3-8B、Llama3-70B 与 OLMo2-13B。每个固定公式在三种提示框架下采样：真实基线 T0、监督压力 D1 和注意力压力 D2；公式与要求输出的 SAT/UNSAT 判断不变。作者按模型选择正确和错误都足够多的混合成功难度，而不是强迫不同能力模型使用同一等级。完整且错误的推理与 $truncated\_or\_looping$、$format\_failure$ 分开统计；SAT 主分析只比较完整正确和完整错误轨迹。早期预警在校准集上确定阈值，再于按公式隔离的留出测试集上逐步截取思维链并评分。轨迹句子按推理功能标注，以计算验证、回溯、矛盾搜索、SAT 承诺、循环和状态转移等结构指标。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 从 UNSAT 错误分类特征中移除与最终答案或标签直接相关的特征，并进一步只使用最终答案之前的句子。 | 移除答案相关特征后，完整轨迹 AUROC 仍分别达到 Llama3-8B 的 0.800、Llama3-70B 的 0.795 和 OLMo2-13B 的 0.905；但只看作答前句子时，AUROC 分别降至 0.507、0.570 和 0.569。 | 第一步排除了分类器只是读取“SAT”或“UNSAT”等最终标签的简单解释，说明完整轨迹的组织方式本身具有区分力。第二步则隔离时间因素：接近随机的作答前 AUROC 表明 UNSAT 动态主要适合事后解释，尚不足以在模型推理过程中可靠预警。这两个结果共同限制了“动态信号可实时检测所有失败”的强结论。 | Results，UNSAT failures substitute assignment search for contradiction proof；Figure 6<br><span class="experiment-evidence">Discrimination from the sentences preceding the answer alone is nonetheless modest (AUROC 0.507, 0.570, and 0.569): the separation emerges only once the full trace is available, so these features explain UNSAT failures after the fact but cannot flag them while the model is still reasoning.</span> |
| 对 Llama3-70B 的同一批 UNSAT 样例比较原始提示、通用重试和定向证明搜索提示；纠正率以原始条件下 52 个错误 SAT 完成为分母。 | 原始准确率为 13.3%，通用重试后为 10.0%，仅纠正 6/52 个错误，即 11.5%；证明搜索提示将准确率提高到 85.0%，纠正 44/52 个错误，即 84.6%。相对原始条件的配对增益为 73.1 个百分点，bootstrap 95% 置信区间为 61.5–84.6，并通过 McNemar 检验。与此同时，SAT 承诺密度从 0.0263 降至 0.0105，矛盾搜索密度从 0.0658 升至 0.1097。 | 通用重试没有改善准确率，因此增益不能简单归因于“再生成一次”；定向提示明确替换了解题程序，并使可见轨迹向矛盾搜索移动，较有力地连接了诊断与修复。不过，这仍不能证明模型内部原本知道答案，也未展示在没有真实标签时如何自动决定何时触发修复。 | Results，Prompting for proof search rescuers most UNSAT failures；Table 2<br><span class="experiment-evidence">Table 2 shows that a generic retry does not, whereas the targeted proof-search prompt raises accuracy from 13.3% to 85.0%, correcting 44 of 52 original wrong-SAT completions, a paired improvement of 73.1 percentage points (bootstrap 95% CI: 61.5–84.6) that is significant under McNemar’s test.</span> |

**定性案例**

- Figure 3 对同一 SAT 公式和提示条件下的 Llama3-8B 错误轨迹与 Qwen3-14B 正确轨迹进行匹配展示：失败轨迹更短、更偏向验证、更循环、转移熵更低且更早最终化。该个案把聚合统计中的“过早验证坍缩”具体化为一种可读模式——模型并非完全不接触公式内容，而是在有限操作之间反复切换不足，过早停止探索；个案本身只用于说明机制，不替代 Table 1 的总体检验。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过分析思维链轨迹的动态结构来诊断并纠正LLM逻辑推理失败。; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`3a992ba2737b2521a53e243402db4fa01bba651aa2082a7a43278b624c84b610`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
