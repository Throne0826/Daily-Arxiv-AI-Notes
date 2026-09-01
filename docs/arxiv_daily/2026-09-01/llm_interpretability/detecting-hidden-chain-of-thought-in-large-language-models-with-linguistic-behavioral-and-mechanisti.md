---
title: "[论文解读] Detecting Hidden Chain-of-Thought in Large Language Models with Linguistic, Behavioral, and Mechanistic Indicators"
description: "[arXiv 2608.29956][LLM 机制与可解释性] 原文未明确报告。"
arxiv_id: "2608.29956"
announcement_date: "2026-09-01"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:44:32.810786+00:00"
source_sha256: "c3586d678e9255239e2c8cd1059f540317e4f0644c991e270d3723b429b13b24"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "隐藏思维链"
  - "潜在推理"
  - "可解释性"
  - "行为分析"
  - "机制分析"
  - "思维链提示"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2608.29956</p>

# Detecting Hidden Chain-of-Thought in Large Language Models with Linguistic, Behavioral, and Mechanistic Indicators

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Armaan Singh, Ryan Trinh Le, Jasmine Kaur, Abdullah Sultan, Edward Lue Chee Lip, Kiran Nijjer, Adnan Ahmed, Vasu Sharma</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29956v1) · [PDF 下载](https://arxiv.org/pdf/2608.29956v1) · **关键词** 大语言模型, 隐藏思维链, 潜在推理, 可解释性, 行为分析, 机制分析, 思维链提示<br>
**代码**: [https://github.com/a4maan/detecting-hct](https://github.com/a4maan/detecting-hct)

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

本文属于大语言模型推理行为与可解释性研究。研究重点不是判断模型是否能够生成显式思维链（Chain-of-Thought，CoT），而是在模型未被要求展示推理步骤的中性提示下，利用行为信号与机制信号判断其行为是否更接近显式 CoT 条件。该问题源于两个事实：显式思维链可能提升复杂推理任务的表现，但模型生成的解释不一定忠实反映真正产生答案的内部计算；反过来，模型也可能在没有输出中间步骤的情况下进行内部的多步计算。因此，本文把“隐藏 CoT”限定为一种可测量的操作性现象，即中性提示下的行为与显式 CoT 行为更相似，而不是直接观测或证明模型存在未公开的推理轨迹。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**显式思维链（CoT）提示**

CoT 提示要求模型在给出最终答案前写出中间推理步骤，常用于复杂数学或逻辑任务。本文将其作为一种比较参照，而不把生成的文字步骤自动视为真实内部推理的忠实记录。

</div>
<div class="concept-item" markdown="1">

**中性提示与无 CoT 提示**

中性提示不明确要求模型展示或抑制推理步骤，用于观察模型在通常交互条件下的行为。无 CoT 提示要求模型直接给出答案；对于不服从该指令的推理型模型，本文还通过强制关闭推理块构造可比较的答案型参照。

</div>
<div class="concept-item" markdown="1">

**行为与机制指标**

行为指标从模型输出及其生成过程观察现象，例如输出熵、生成延迟、释义一致性和扰动敏感性。机制指标进一步利用梯度与激活归因定位可能影响输出的内部计算，并测试抑制这些计算后准确率是否下降。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定模型、数据集中的问题以及三种提示条件——显式 CoT、显式无 CoT 和中性提示——本文比较中性条件的多维行为与机制特征更接近哪一个参照条件。具体研究对象是 Qwen3-4B Instruct 与 Qwen3-4B Thinking，在 GSM8K 上进行主要分析，并将 StrategyQA 作为单独报告的数据集。模型输出包括最终答案、生成过程及其相关统计特征；研究假设是，如果中性行为在控制输出长度后更接近显式 CoT，则可将其解释为与隐藏推理一致的证据，但这一比较不能证明模型确实执行了某条不可见的内部推理链。由于 Thinking 版本可能忽略无 CoT 指令，主要分析中通过强制关闭其推理块获得答案型无 CoT 比较条件。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$HCDS$**

Hidden CoT Detection Score，即隐藏思维链检测分数；它衡量中性提示行为相对于显式 CoT 和显式无 CoT 两个参照点的相对接近程度。

</div>
<div class="notation-item" markdown="1">

**$x$**

单个模型输入或数据样本，通常对应一个待回答的问题及其提示条件。

</div>
<div class="notation-item" markdown="1">

**$f_i(x)$**

输入 $x$ 在第 $i$ 个指标上的特征值；本文使用六类特征，包括平均 token 熵、熵斜率、每个输出 token 的延迟、释义一致性、扰动敏感性，以及抑制归因计算后的准确率代价。

</div>
<div class="notation-item" markdown="1">

**$d(\mathrm{neutral},\mathrm{CoT})$**

中性提示特征向量与显式 CoT 参照特征向量之间的欧氏距离；类似地，$d(\mathrm{neutral},\mathrm{no\text{-}CoT})$ 表示中性提示与显式无 CoT 参照之间的距离。

</div>

</div>

**直接相关的工作**

- **Turpin et al. (2023)**: 该工作指出思维链解释可能不忠实于模型实际产生答案的计算。本文沿用这一警示，不把模型自报的推理文本当作内部推理的直接证据，而改用行为相似性和机制干预来研究隐藏推理。
- **Chen et al. (2025)**: 该工作同样关注显式思维链不能充分揭示内部计算的问题。本文与其区别在于，研究目标是检测中性提示下推理型行为是否出现，而不是评估显式理由本身的忠实性。

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

该方法把“隐藏思维链”定义为一种可检验但非直接可观测的行为假设：在同一个模型回答同一个问题时，中性提示的行为特征是否更接近显式思维链条件，而不是显式不展示思维链条件。具体而言，方法分别生成显式 CoT、显式 no-CoT 和 neutral-strict 三种条件的回答，提取六类语言、行为与机制特征，经长度残差化和标准化后计算欧氏距离，并以中性条件到 no-CoT 的距离减去到 CoT 的距离，得到每道题的 $\mathrm{HCDS}_q$；正值表示中性行为更接近显式 CoT。直观地说，方法不试图读取模型“脑中的文字草稿”，而是比较三种外部实验条件下模型行为的相似性；因此正的 HCDS 只能支持“更像隐式推理”的解释，不能证明模型确实存在未暴露的推理轨迹。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造三种提示条件

分别要求模型逐步推理、直接给出答案，或仅执行任务而不规定是否展示推理。对 Thinking 模型，显式 no-CoT 与 neutral-strict 都使用相同的 force-closure 前缀关闭自动打开的思维块。

<div class="method-step__io" markdown="1">

**输入**：模型 $m$、问题 $q$，以及显式 CoT、显式 no-CoT 和 neutral-strict 三种提示条件。<br>
**输出**：每个模型—问题—提示条件组合对应的一条生成序列及其最终答案。

</div>

**直观理解**：这是一个三组对照实验：一组明确要求写出步骤，一组明确要求不要写步骤，另一组不告诉模型该怎么展示推理。对会自动进入思维模式的模型，研究者用统一的前缀让它从答案阶段开始，避免“提示不同”和“输出格式不同”混在一起。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提取并校正六维特征

为每个条件计算输出 token 延迟、平均 token 熵、熵斜率、释义一致性、扰动敏感性和机制干预敏感性，形成六维向量 $f_{m,q,p}$。在每个后端及模型—数据集组内，将每个原始特征对生成长度 $\log n^{\mathrm{gen}}_{m,q,p}$ 做单独 OLS 回归，保留残差并进行 z-score；未调整分数则直接对原始特征 z-score。

<div class="method-step__io" markdown="1">

**输入**：三种条件下的生成序列、输出长度、答案正确性，以及可解析的多步骤推理轨迹。<br>
**输出**：长度调整后的标准化特征向量，以及部分样本中定义的机制干预特征。

</div>

**直观理解**：模型写得长，天然会增加延迟和改变 token 统计，因此方法先把“仅仅因为回答更长”能解释的部分去掉。剩余特征才用于判断回答风格和内部状态是否更像 CoT；机制特征在没有足够推理步骤或答案跨度时可能无法定义。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算问题级 HCDS

在两两比较可用特征的交集上计算欧氏距离，并按完整六维特征数对缺失机制特征的距离进行 rescale；随后用中性条件到 no-CoT 的距离减去中性条件到 CoT 的距离。对每个模型和数据集，再对 $N$ 道题的分数求平均。

<div class="method-step__io" markdown="1">

**输入**：同一模型和问题下 neutral、explicit-no-CoT 与 explicit-CoT 的特征向量。<br>
**输出**：每道题的 $\mathrm{HCDS}_q$ 和模型—数据集层面的平均分 $\overline{\mathrm{HCDS}}$。

</div>

**直观理解**：把三种条件想成特征空间中的三个点：如果中性点离 CoT 点更近，分数就为正；如果离 no-CoT 点更近，分数就为负。这个分数测量的是“相似性方向”，不是从模型内部恢复出一段真实思维链。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 机制锚点干预与稳健性处理

以答案跨度 token 的对数概率为目标，计算各层各步骤的 gradient × activation 归因，选出归因最高的两个步骤作为候选锚点；在第 18 个解码器层的 residual stream 上，将锚点 token 位置的激活置零，并与同轨迹、同位置附近的控制步骤干预比较，得到 $\Delta A^{\mathrm{mech}}$。由于不同后端的机制特征定义略有差异，研究同时检查不同距离策略、后端、量化设置及去除机制特征后的结论。

<div class="method-step__io" markdown="1">

**输入**：具有可解析答案跨度且至少包含三个分段步骤的生成轨迹，以及梯度和激活值。<br>
**输出**：候选推理状态的机制干预敏感性，并纳入 HCDS 的第六维特征或作为稳健性分析。

</div>

**直观理解**：归因只是用来找“可能重要的步骤”，并不等于已经证明因果关系；真正的检验是把这些步骤对应的内部表示抹掉，看答案正确率是否比控制位置下降更多。若没有足够长的轨迹，方法不强行补数据，而是把该机制特征视为未定义。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 问题级隐藏思维链检测分数

$$
\mathrm{HCDS}_{q}=D\!\left(f_{m,q,\mathrm{neutral}},f_{m,q,\mathrm{no\text{-}cot}}\right)-D\!\left(f_{m,q,\mathrm{neutral}},f_{m,q,\mathrm{cot}}\right)
$$

**符号说明**

- $\mathrm{HCDS}_{q}$：问题 $q$ 的隐藏思维链检测分数。
- $f_{m,q,p}$：模型 $m$ 在问题 $q$ 和提示条件 $p$ 下的六维标准化特征向量。
- $D(\cdot,\cdot)$：两个条件特征向量之间的欧氏距离，必要时包含缺失特征的重标度。
- $\mathrm{neutral}$：不指定是否展示推理的中性提示条件。
- $\mathrm{no\text{-}cot}$：要求直接回答、不展示思维链的显式条件。
- $\mathrm{cot}$：要求逐步展示推理的显式条件。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项衡量中性行为离显式 no-CoT 有多远，第二项衡量它离显式 CoT 有多远。若前者更大、后者更小，则 $\mathrm{HCDS}_{q}>0$，表示中性行为更接近 CoT；这支持但不证明模型在中性提示下进行了潜在中间推理。<br>
**原文位置**：第 3.1 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 模型—数据集平均 HCDS

$$
\overline{\mathrm{HCDS}}=\frac{1}{N}\sum_{q=1}^{N}\mathrm{HCDS}_{q}
$$

**符号说明**

- $\overline{\mathrm{HCDS}}$：某模型在某数据集上的平均 HCDS。
- $N$：该模型—数据集组中纳入聚合的题目数。
- $\mathrm{HCDS}_{q}$：第 $q$ 道题的问题级 HCDS。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把每道题的相似性证据取平均，得到模型和数据集层面的总体方向。它反映平均行为模式，但不能说明每一道题都表现出相同的潜在推理信号。<br>
**原文位置**：第 3.1 节，公式（2）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未报告为 HCDS 训练新的模型，也未定义用于优化模型参数的损失函数。Qwen3-4B Instruct 与 Thinking 被作为已有模型检查点进行推理、特征提取和内部干预；因此该方法的核心是推理时测量与比较，而不是训练目标优化。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 比较式 HCDS 表征**

HCDS 使用六维特征：每个输出 token 的延迟 $\ell_{m,q,p}$、平均熵 $\bar{H}_{m,q,p}$、熵斜率 $s^H_{m,q,p}$、释义一致性 $C^{\mathrm{para}}_{m,q,p}$、扰动敏感性 $\Delta A^{\mathrm{pert}}_{m,q,p}$ 和机制干预敏感性 $\Delta A^{\mathrm{mech}}_{m,q,p}$。特征先按后端及模型—数据集组处理，再通过欧氏距离比较中性条件与两个极端条件的接近程度。

> 直观理解：单一指标可能把长度、随机性或提示服从性误判成推理，所以研究者把多个行为和内部干预信号合成一个比较分数。核心不是某个特征绝对值多大，而是中性回答在整体上更像哪一个对照条件。

**2. 长度残差化与缺失特征距离**

原始特征分别回归到生成长度的对数 $\log n^{\mathrm{gen}}$ 上，使用残差进行主分析。若机制特征在某一对条件中未定义，则先在可用特征交集 $\mathcal{J}_q$ 上计算距离，再用 $\sqrt{|\mathcal{F}|/|\mathcal{J}_q|}$ 重标度，其中 $\mathcal{F}$ 是完整六维特征集合；另有不校正的 pairwise 策略和使用三条件共同交集的 complete 策略。

> 直观理解：这一步相当于先扣除“答案写得长”带来的共同影响，再尽量避免某个条件缺少机制测量时因为维度较少而距离天然偏小。研究者也承认，长度校正可能同时删掉部分真正与推理有关的变化。

**3. 基于归因的残差流干预**

每个轨迹按句号、问号、感叹号后的空格或换行切分为步骤；以最后一个 $\boxed{\cdots}$ 匹配结果作为答案跨度。对答案跨度 token 的观测 next-token log probability 求梯度，并与内部激活逐元素相乘，按步骤和层聚合后选取 top-2 锚点，在第 18 层 residual stream 位置执行 $\mathrm{residual\_zero}$。

> 直观理解：研究者先找出哪些推理片段对最终答案分数最敏感，再把这些片段在模型内部对应的表示清零。控制步骤只按轨迹位置和长度近似匹配，没有匹配步骤承担的具体功能，因此该模块仍不能完全排除控制不充分的问题。

**训练与推理**

整个流程在推理阶段完成：对每个模型—问题组合运行三种提示条件，收集生成文本、token 统计、答案正确性、释义一致性、扰动结果及可用的机制干预结果；然后按后端和模型—数据集组做长度残差化、z-score 标准化，计算条件间距离并聚合 HCDS。机制分析额外要求生成结果具有可解析的最后一个 $\boxed{\cdots}$ 答案跨度和至少三个分段步骤，随后进行一次梯度 × 激活归因、top-2 锚点选择、第 18 层 residual stream 清零、控制步骤干预和答案重解析。

**复现信息**

为使 Thinking 模型的 no-CoT 极点有效，研究者在 assistant 前缀中加入伪造的已完成思维内容并关闭 $\langle\mathrm{think}\rangle$ 区块，同时对 no-CoT 和 neutral 使用相同的 force-closure；显式 CoT 则自然生成。机制特征在 CUDA 后端分别干预两个锚点并平均正确性，MLX 后端使用一次联合锚点—控制比较；CUDA 中 $\Delta A^{\mathrm{mech}}$ 的取值支持为 $\{-1,-\tfrac{1}{2},0,+\tfrac{1}{2},+1\}$，MLX 中为 $\{-1,0,+1\}$。控制步骤按相对轨迹位置优先、token 长度弱优先的确定性距离选择，并在相同层和位置执行干预；原文特别指出控制未按步骤功能匹配，这是解释机制结果时需要保留的限制。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：小学数学文字题，需要多步算术推理，是主要评测基准。每个模型—后端实验单元使用 $n=50$ 个问题；同一问题分别采用 explicit CoT、explicit no-CoT 和 neutral 三种提示。由于开放式数值答案的随机命中概率接近零，基于准确率差异的行为与干预特征具有较大的可用动态范围。
- StrategyQA：答案为二元值的隐式多跳常识问答，作为次要基准而非共同主基准。每个模型—后端单元同样使用 $n=50$；其随机准确率为 $0.50$，使 explicit no-CoT 条件已经接近机会水平，从而压缩准确率型特征的动态范围，并降低机械干预的有效覆盖率。
- 校准控制任务：单步算术与数值事实查询，设计上不需要多步推理，用于检验 HCDS 会不会把冗长输出误判为隐藏 CoT。图 1 报告每个实验单元 $n=50$，并比较长度校正前后的分数；原文未给出这些控制集的正式数据集名称与划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**长度校正 HCDS**

先将各特征对数输出长度的可预测部分残差化，再衡量中性提示的特征向量相对 explicit CoT 与 explicit no-CoT 两个极点的位置。正值表示中性行为更接近显式 CoT，接近零表示与两极距离相近；该指标只是操作性“CoT-like alignment”，不直接观测或证明存在未展示的推理轨迹。 （研究目标是检测 CoT-like 对齐，因此显著大于零才构成支持证据；数值越大通常表示相对更接近 explicit CoT，但论文明确指出其尺度依赖标准化特征空间，不能赋予跨设置通用的绝对含义。）

</div>
<div class="metric-item" markdown="1">

**不确定性与显著性**

以问题级 HCDS 检验零假设 $\mathbb{E}[\mathrm{HCDS}_q]=0$，报告双侧检验的 $p$ 值和基于 $1000$ 次问题重采样得到的 $95\%$ bootstrap 置信区间。确定性解码下，不确定性来自问题之间的差异，而非同一问题的多次生成。 （置信区间不跨零且双侧 $p<0.05$ 时，说明平均 HCDS 与零存在统计差异；这衡量统计稳定性，不等同于因果证明或实际效应的重要程度。）

</div>
<div class="metric-item" markdown="1">

**机械干预敏感性**

定义为 $\Delta A^{\mathrm{mech}}=A_{\mathrm{control}}-A_{\mathrm{anchor}}$：比较抑制归因方法选出的候选推理锚点与抑制位置匹配控制点后的准确率。它检验被选内部状态是否对最终答案具有额外的因果贡献，并作为 HCDS 六个组成测量之一。 （值越大，表示抑制候选锚点比抑制匹配控制位置造成更大的准确率损失，因果证据越强；负值或稀疏结果说明该干预信号不稳定，不能仅凭它断言存在隐藏推理。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### GSM8K，PyTorch/CUDA bf16 后端，长度校正 HCDS

<div class="result-value" markdown="1">

Thinking 的 HCDS 为 $+1.872$，$95\%$ 置信区间为 $[1.32,2.45]$，$p=1.2\times10^{-7}$；Instruct 为 $+1.410$，区间为 $[0.75,2.16]$，$p=1.9\times10^{-4}$。两种模型的中性提示行为均显著偏向 explicit CoT，其中 Thinking 的点估计更高。

</div>

作者结果支持：在需要多步算术的 GSM8K 上，即使不明确要求展示推理，两种模型的综合行为和敏感性仍更像显式 CoT 条件。分析上，Thinking 的更高点估计与其推理后训练相符，但论文没有给出两模型 HCDS 差值的直接显著性检验，因此不能仅凭点估计断言 Thinking 显著强于 Instruct；正 HCDS 也不等于直接发现了内部文字化思维链。

<div class="result-source" markdown="1">

来源：表 2；第 5.1 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

PyTorch/CUDA | Thinking | +2.372 | +1.872 [1.32, 2.45], p = 1.2 × 10−7
PyTorch/CUDA | Instruct | +1.765 | +1.410 [0.75, 2.16], p = 1.9 × 10−4

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### GSM8K，MLX 8-bit 独立推理栈复现

<div class="result-value" markdown="1">

MLX 上 Thinking 的长度校正 HCDS 为 $+1.799$，Instruct 为 $+1.449$，均显著为正；与 CUDA 对应结果的差异不超过 $0.08$，而长度校正前的最大后端差异达到 $0.65$。

</div>

这项复现检验的是结果是否依赖某一种硬件、运行时或数值精度。长度校正后两套推理栈高度一致，削弱了“正信号只是后端实现或量化误差”的解释，也显示长度残差化提高了跨环境稳定性；但两个后端仍使用同一模型家族和同一批任务，不能据此推断信号可普遍推广到其他架构。

<div class="result-source" markdown="1">

来源：表 2 标题说明；第 5.1 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The length-adjusted scores agree across backends to within 0.08, compared with a 0.65 maximum difference before adjustment.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### StrategyQA 次要基准，长度校正后的跨后端结果

<div class="result-value" markdown="1">

Thinking 在 CUDA 与 MLX 上分别得到 $+0.724$（$p=3.8\times10^{-4}$）和 $+0.738$（$p=1.2\times10^{-3}$）；Instruct 分别为 $+0.291$（$p=0.28$）和 $-0.149$（$p=0.54$），均不显著。因而只有 Thinking 的正结果跨后端保留，但后续特征分析表明该信号主要由熵斜率单项承载。

</div>

该结果说明 HCDS 并非在所有模型—数据集组合上都稳定显著。作者把 Instruct 的阴性结果解释为 StrategyQA 测量能力较弱：二元答案的机会水平较高，准确率型特征可变化空间有限。分析上，这是一种合理但尚未由更合适第二数据集验证的解释；结果既不能证明 Instruct 在常识问题上没有隐藏推理，也不能把 Thinking 的单特征驱动信号视为与 GSM8K 多特征结果同等强的证据。

<div class="result-source" markdown="1">

来源：表 8；附录 F

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The negative result is plain (Table 8): Instruct StrategyQA HCDS does not survive length adjustment, on either backend.

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

- explicit CoT 提示条件：明确要求模型展示逐步推理，构成 HCDS 的“CoT 极点”；中性提示若更接近该条件，HCDS 为正。
- explicit no-CoT 提示条件：明确要求模型不展示推理过程，构成比较中的“无 CoT 极点”。它不是外部模型基线，而是同一模型、同一问题和同一解码配置下的配对行为参照。
- 未校正的六特征 HCDS：直接在标准化特征空间中计算，用来显示输出长度可能造成的混淆；长度残差化后的 HCDS 是论文的主要指标。
- 跨后端复现：PyTorch/CUDA bf16 与 MLX 8-bit 在不同硬件、数值精度和运行时下独立评测，用于排除特定推理栈造成的伪信号，而不是比较后端性能优劣。

**实验想回答的问题**

- 在中性提示下，模型的行为与内部敏感性是否系统性地更接近“显式要求逐步推理”的条件，而不是“显式禁止逐步推理”的条件；这种经长度校正后的 HCDS 信号能否在不同模型变体与推理后端上复现？
- 观察到的正 HCDS 是否只是输出更长、运行环境差异或单一特征造成的假象；在不需要多步推理的校准任务、第二基准 StrategyQA、特征移除以及内部干预下，信号是否仍然成立？

**实验实现**

实验对象为 Qwen3-4B-Instruct-2507 与 Qwen3-4B-Thinking-2507：前者针对指令遵循优化，后者经过生成显式推理块的后训练。每个 $(m,q,p)$ 组合记录准确率、生成时间、输出长度、每输出 token 延迟、token 熵、释义一致性、无关扰动敏感性，以及可定义时的机械干预敏感性；准确率和输出长度仅作辅助诊断，不直接进入 HCDS，其余六项构成特征向量。三种提示在同一模型—数据集单元内使用相同的确定性解码配置和 token 上限，但上限可随模型及数据集变化。主分析把每项特征对对数输出长度做残差化；释义一致性衡量保持数量、结构、实体和金答案不变的 $K$ 个释义中复现原答案的比例，无关扰动则统一在问题前加入句子“The neighbor’s dog barked seven times that afternoon.”。两套后端独立运行；bootstrap 固定为 $1000$ 次、随机种子为 $17$，且重采样时不重新拟合 pooled preprocessing。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 长度校正消融：比较原始六特征 HCDS 与将每项特征对对数输出长度残差化后的 HCDS | 未校正分数在单步算术和事实查询控制任务上出现可超过 GSM8K 的大正值；长度校正后控制分数趋近零且几乎全部不显著。图 1 进一步指出，未校正分数在八个控制单元中的五个为大正值。 | 该对照隔离了“推理迹象”与“只是生成得更长”之间的混淆。如果一个指标在无需多步推理的任务上也强烈为正，它就不能可靠区分推理与冗长。校正后控制信号消失而 GSM8K 信号保留，是选择长度校正 HCDS 作为主指标的核心依据；不过残差化只能控制与输出长度相关的线性统计关系，不能排除全部潜在混淆。 | 图 1；第 5.2 节<br><span class="experiment-evidence">On single-step arithmetic and factual lookup, where multi-step reasoning is unnecessary, it produces large positive values that can exceed those on GSM8K.</span> |
| 特征贡献消融：StrategyQA 与 GSM8K 的 leave-one-feature-out 分析 | StrategyQA 在长度校正后几乎由熵斜率单独驱动：移除熵斜率使 HCDS 改变 $-0.60$，移除其他任一特征的变化均满足 $\|\Delta\|<0.21$；相比之下，GSM8K 仍由平均熵、熵斜率、释义一致性和扰动敏感性共同贡献。 | 该消融检验正 HCDS 是多个相互补充的指标共同形成，还是单一统计量造成。StrategyQA 对熵斜率高度依赖，意味着其 Thinking 正结果更脆弱，也可能反映该数据集的二元答案结构，而非广泛一致的隐藏推理信号；GSM8K 的多特征贡献则提供更强的聚合稳健性，但仍不是对潜在推理轨迹的直接观测。 | 附录 F，表 7 后的特征分析<br><span class="experiment-evidence">Second, and more importantly, once output length is adjusted for (Section 3) the StrategyQA signal is carried almost entirely by a single feature, entropy slope: in a leave-one-feature-out analysis, removing entropy slope costs −0.60 HCDS while every other feature contributes \|Δ\| < 0.21.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces behavioral and mechanistic indicators for detecting latent chain-of-thought-like reasoning in LLMs.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`c3586d678e9255239e2c8cd1059f540317e4f0644c991e270d3723b429b13b24`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
