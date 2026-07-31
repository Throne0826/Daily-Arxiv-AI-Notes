---
title: "[论文解读] Do LLMs Know What They Know? Measuring Metacognitive Efficiency with Signal Detection Theory"
description: "[arXiv 2603.25112][LLM 评测] 本文提出一套面向开放式事实问答的元认知评估框架，用信号检测论刻画置信度区分正确与错误答案的能力，并以归一化互信息衡量这种能力相对于答案正确性不确定度的效率。"
arxiv_id: "2603.25112"
announcement_date: "2026-07-30"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.738142+00:00"
source_sha256: "27091ea85be10d8634db524cc8a2a3be6c18d1e6d748ee5a37bb472d67249054"
tags:
  - "LLM 评测"
  - "大语言模型置信度"
  - "元认知效率"
  - "信号检测论"
  - "Type-2 ROC"
  - "归一化元认知信息"
  - "开放式事实问答"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2603.25112</p>

# Do LLMs Know What They Know? Measuring Metacognitive Efficiency with Signal Detection Theory

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Jon-Paul Cacioli</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2603.25112v3) · [PDF 下载](https://arxiv.org/pdf/2603.25112v3) · **关键词** 大语言模型置信度, 元认知效率, 信号检测论, Type-2 ROC, 归一化元认知信息, 开放式事实问答<br>
**代码**: [https://github.com/synthiumjp/metacognition-audit](https://github.com/synthiumjp/metacognition-audit)  

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

本文提出一套面向开放式事实问答的元认知评估框架，用信号检测论刻画置信度区分正确与错误答案的能力，并以归一化互信息衡量这种能力相对于答案正确性不确定度的效率。

**不用术语来说**：语言模型不仅要尽可能答对，还应当知道哪些回答更可能答对：如果置信度无法区分具体答案的对错，即使模型的平均置信度与总体准确率一致，用户也不能据此决定何时信任、复核或拒绝回答。本文关注的正是这种“能否可靠监控自身回答”的能力，而不是单纯比较谁答对得更多。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将大语言模型置信度作为连续信号、将回答正确与否作为待区分状态，构建了Type-2信号检测论分析，包括AUROC2、z-ROC斜率和非等方差敏感度，从而把置信信号的排序能力与其整体高估或低估倾向分开考察。
- 作者针对开放式问答缺少二选一Type-1决策、因而不适合直接使用meta-d′效率比的问题，引入归一化元认知信息meta-I2r，以正确性与离散化置信度之间的互信息除以正确性熵，并配合置换零分布和自助法置信区间进行有限样本校正与不确定性估计。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型（LLM）置信度评估与元认知测量研究。事实问答系统的可靠性至少包含两个不同能力：一是生成正确答案的能力，即 Type-1 准确性；二是模型内部置信度能否区分自身答案的正确与错误，即 Type-2 元认知敏感性。常用的期望校准误差（ECE）和 Brier 分数主要考察置信度数值与总体正确率是否匹配，可能把置信度的整体偏高或偏低与其逐题识别错误的能力混在一起。本文因此引入信号检测论，将答案正确性视为待判别状态，将答案的 token 级归一化对数概率视为连续置信信号，通过 Type-2 ROC、z-ROC 与信息论指标分析该信号。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**置信度校准**

校准考察模型声称的置信概率是否与实际正确频率一致，例如置信度约为 80% 的答案是否约有 80% 正确。良好校准不等于置信度能区分具体哪道题答对或答错：一个始终报告相同置信度的模型也可能在总体上完美校准。

</div>
<div class="concept-item" markdown="1">

**Type-2 信号检测论**

传统 Type-1 分析关注模型能否完成外部任务，Type-2 分析则关注其置信信号能否判别自己刚才的回答是否正确。改变置信阈值可形成 Type-2 ROC；AUROC₂衡量排序能力，z-ROC 的斜率则反映正确与错误答案的置信分布是否具有不同方差。

</div>
<div class="concept-item" markdown="1">

**互信息与归一化元认知信息**

互信息衡量知道置信度后，能够减少多少关于答案正确性的未知量。本文用 meta-I₂r 将正确性与离散化置信度之间的互信息除以正确性的熵，从而按任务正确率所提供的信息上限进行归一化。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是在开放式事实问答中由 LLM 生成的答案。每次试验输入一个事实问题，模型输出自由文本答案；研究者依据参考答案及别名将其标注为正确或错误，并从生成 token 的对数概率构造长度归一化的连续置信度。核心问题不是仅比较模型答对多少题，而是判断该置信信号能在多大程度上把正确答案与错误答案分开，以及在控制正确率所决定的信息上限后，其元认知效率有多高。该设定没有二选一的 Type-1 决策，因此论文认为依赖二选一检测结构的 meta-d′/M-ratio 并不适用，改用不假定高斯证据分布、也不要求 Type-1 二元选择的 meta-I₂r；有限样本下的互信息估计通过置换零分布校正，并使用 bootstrap 置信区间表达不确定性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$I(\mathrm{correct};\mathrm{confidence})$**

二元答案正确性与离散化置信度之间的互信息，即置信度传递了多少关于正确与错误的信息。

</div>
<div class="notation-item" markdown="1">

**$H(\mathrm{correct})$**

答案正确性变量的熵，表示在观察置信度之前，正确与错误状态所含的不确定性。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{meta\text{-}}I_{2r}=\frac{I(\mathrm{correct};\mathrm{confidence})}{H(\mathrm{correct})}$**

本文采用的归一化元认知信息指标；值为 0 表示置信度不提供正确性信息，越接近其上限表示置信度越能解析正确与错误的区别。来源：第 1 节，式（1）。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{AUROC}_2$**

Type-2 ROC 曲线下面积，衡量置信度把正确答案排在错误答案之前的能力；它关注排序，而不是置信概率的绝对数值是否校准。

</div>

</div>

**直接相关的工作**

- **Dayan (2023)**: 提出选择准确性与置信度之间的 meta-I 及其归一化形式；本文采用其中按正确性熵归一化的思想，并将所用比率记为 meta-I₂r，以适配开放式问答。
- **Cacioli (2026)**: 表明参数化信号检测论中的 ROC、非等方差模型拟合和判定标准估计能够揭示校准指标不可见的 LLM 置信度结构；本文进一步把该框架应用到区分自身答案正误的 Type-2 层面。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在事实问答系统中，准确率不足通常需要改进训练数据或模型能力，而置信度不能跟踪自身对错则需要校准或监控机制；若评估工具不能区分这两类故障，开发者就可能采取错误干预。部署中的置信拒答也依赖逐题置信度是否真正携带正确性信息，而非只要求平均置信度接近总体准确率。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **校准误差与概率评分（ECE、Brier score）**：ECE将预测按置信度分组，比较各组平均置信度与实际准确率；Brier score衡量概率预测与二元结果之间的平方误差，并可分解为可靠性、分辨率和不确定性。这类方法主要判断概率数值是否与经验频率相符。
- **Type-2排序与参数化元认知指标（AUROC2、meta-d′/M-ratio）**：AUROC2考察置信度能否把正确回答排在错误回答之前。meta-d′及其效率比则源自信号检测论，通常根据二选一Type-1判断及其置信度，反推出产生观察到的Type-2表现所需的元认知敏感度。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- ECE会把置信度的整体偏高或偏低与其区分正确、错误答案的能力混在一起，因此可能偏爱“所有回答都给相同置信度、但平均值恰好匹配准确率”的模型；Brier score虽包含分辨率项，也没有控制模型本身的Type-1正确率后单独给出元认知效率。
- AUROC2衡量排序质量，但不按正确答案基率所包含的不确定度进行归一化；meta-d′/M-ratio则要求可定义的二选一Type-1检测决策，开放式事实问答不具备这一结构。强行套用会使d′与meta-d′由同一张“正确性×置信度”表决定，令M-ratio接近由构造固定为1，并把非等方差偏离误当成效率差异。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有评估缺少一种同时满足三项要求的方法：适用于开放式生成任务，不依赖高斯证据分布或二选一决策假设，并能把置信信号携带的正确性信息相对于任务自身的正确性不确定度进行量化；与此同时，还需要显式检查不同模型置信信号可能具有的非等方差结构。

</div>
<div markdown="1"><span>核心问题</span>

在控制“模型答对多少”这一Type-1能力后，如何可靠测量大语言模型的连续置信信号究竟包含多少关于自身回答正确与否的信息，并判断这种元认知信息是否随模型、知识领域和采样温度变化，以及是否能预测置信拒答的实际收益？

</div>
<div markdown="1"><span>作者直觉</span>

把每次回答的正确性看成需要识别的隐藏状态，把长度归一化的token对数概率看成模型内部给出的线索，就可以通过移动置信阈值观察正确与错误回答如何被分开；ROC及z-ROC描述线索的区分能力和分布形状，而互信息直接计算知道置信度后能减少多少关于答案对错的不确定性。再除以原有的正确性熵，便可在不同准确率的模型之间比较“可用正确性信息被置信信号传出了多少”，而无需假定开放式回答等同于二选一判断。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把开放式事实问答中的“模型是否答对”视为待识别状态，把生成答案的逐词元归一化对数概率（NLP）视为连续置信信号，并用二阶信号检测论（Type-2 SDT）衡量该信号区分模型自身正确与错误回答的能力。端到端流程是：让四个模型在两个问答数据集和多个温度下生成答案，记录答案及其NLP，用自动评分器标注正确性，再构造Type-2 ROC、拟合z-ROC方差结构，并计算经置换偏差校正的归一化元认知信息$meta-I_{2r}$；最后用试次级bootstrap给出不确定性，并通过领域、温度和置信度拒答分析检验其行为意义。
直观地说，论文不只问“模型答对多少”，而是问“模型给出的内部高低置信度能否可靠地区分自己何时答对”。这不是对模型进行训练或增加一个元认知网络，而是一套事后测量流程；其中ROC面积描述排序能力，z-ROC斜率描述正确与错误答案的置信分布形状差异，$meta-I_{2r}$描述置信信号消除了多少关于正确性的未知。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成事实问答试次并记录内部置信信号

模型自由生成答案，同时记录每个答案词元的条件概率，并取答案级平均对数概率NLP。每个模型—数据集—温度组合均独立形成试次，共得到224000个试次。

<div class="method-step__io" markdown="1">

**输入**：TriviaQA的5000个问题、NQ-Open的3000个短答案问题，以及四个开放权重LLM；每个模型在T∈{0.1,0.3,0.5,0.7,1.0,1.5,2.0}下回答每个问题。<br>
**输出**：每个试次的生成答案、答案长度、NLP、模型标识、数据集、温度及问题领域。

</div>

**直观理解**：NLP相当于把模型生成整段答案时的“顺畅程度”压缩成一个连续分数；分数越高，操作上视为模型越有信心。它只是功能性的置信代理，不证明模型具有人类式自我意识。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 标注回答正确性并离散化置信度

先以已验证别名进行精确匹配，并以difflib.SequenceMatcher≥0.85作为后备规则，得到二元正确性标签；随后在每个模型×数据集条件内，以T=1.0的NLP分布的12.5%至87.5%分位点为边界，将NLP划为2K=8个有序类别，K=4，且边界在其他温度下保持不变。

<div class="method-step__io" markdown="1">

**输入**：模型生成答案、数据集的已验证答案别名，以及各试次的连续NLP。<br>
**输出**：每个试次的正确/错误标签，以及可跨温度比较的八级置信类别。

</div>

**直观理解**：正确性是要被置信信号识别的真实状态，分箱则把连续置信度变成稳定的等级。固定T=1.0得到的边界，可避免每个温度都重新定义“高置信”，从而使温度比较更公平。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 估计Type-2 ROC及不等方差结构

扫过置信阈值，以“正确答案高于阈值”为命中、以“错误答案高于阈值”为虚警，构造Type-2 ROC并计算AUROC_2；再对命中率和虚警率作probit变换并线性回归，估计z-ROC斜率s、截距及不等方差敏感度$d_a$。

<div class="method-step__io" markdown="1">

**输入**：二元正确性标签、连续或有序NLP置信信号。<br>
**输出**：置信排序能力AUROC_2，以及描述正确与错误答案置信分布相对方差的s和敏感度$d_a$。

</div>

**直观理解**：AUROC_2回答“随机取一个正确答案和一个错误答案，模型是否倾向给前者更高置信度”。z-ROC进一步检查两类答案的置信分布是否具有不同宽窄，这是ECE或单一ROC面积看不到的结构。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算元认知信息并进行统计推断

计算归一化元认知信息$meta-I_{2r}$，即置信信号对正确性不确定性的削减量占正确性总不确定性的比例；用2000次随机打乱置信度—正确性配对所得的置换零基线校正插件互信息的向上偏差，并用2000次试次级bootstrap重算完整流程获得95%百分位置信区间。

<div class="method-step__io" markdown="1">

**输入**：置信类别与正确性标签的联合频数，以及模型、数据集、领域和温度条件。<br>
**输出**：偏差校正后的$meta-I_{2r}$、置换显著性及95%置信区间，可用于跨模型、跨领域和跨温度比较。

</div>

**直观理解**：如果打乱后仍能得到少量正信息，那通常是有限样本造成的假象，因此需要减去置换零基线。bootstrap则反复重抽问题，检验结论是否依赖某一小批试次。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 答案级归一化对数概率

$$
\mathrm{NLP}=\frac{1}{L}\sum_{i=1}^{L}\log p(t_i\mid t_{<i})
$$

**符号说明**

- $\mathrm{NLP}$：生成答案的平均词元对数概率，作为连续置信证据；数值越高表示操作意义上的置信度越高。
- $L$：生成答案包含的词元数量。
- $t_i$：答案中的第i个生成词元。
- $t_{<i}$：生成第i个词元之前已有的词元序列。
- $p(t_i\mid t_{<i})$：模型在既有前缀条件下为实际生成词元$t_i$赋予的条件概率。

<div class="equation-explanation" markdown="1">

**直观理解**：先对每个实际生成词元的概率取对数，再在整段答案上求平均，以降低答案长度对总对数概率的直接影响。该量来自模型的生成分布，比离散且容易集中在整数档位的口头置信评分更适合作为连续排序信号，但仍应理解为流畅度与分布属性的综合代理。<br>
**原文位置**：§2.1，The confidence signal as a Type-2 detector

</div>

</div>

<div class="equation-block" markdown="1">

#### 不等方差敏感度指数

$$
d_a=\sqrt{\frac{2}{1+s^2}}\,(\text{z-intercept})
$$

**符号说明**

- $d_a$：考虑正确与错误证据分布方差不等后的Type-2敏感度摘要。
- $s$：经验z-ROC线性回归斜率，按论文定义为错误答案证据标准差与正确答案证据标准差之比。
- $\text{z-intercept}$：命中率与虚警率经probit变换后，z-ROC回归直线的截距。

<div class="equation-explanation" markdown="1">

**直观理解**：仅用ROC截距概括可分性会忽略两类置信分布宽度不同的问题；该式利用斜率对截距进行缩放，从而在不等方差条件下给出更合适的敏感度。论文的$meta-I_{2r}$完整公式在所提供节选中未展示，因此这里不依据描述补写该公式。<br>
**原文位置**：§2.2，Unequal-variance structure via z-ROC

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文提出的是评估与统计测量方法，不训练、微调或优化任何LLM，也没有反向传播损失；模型参数保持固定，仅改变采样温度并分析生成输出。$meta-I_{2r}$、AUROC_2、z-ROC斜率和$d_a$均为生成后的估计量，而不是训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Type-2信号检测模块**

把正确性作为二元状态、NLP作为连续证据，构造Type-2 ROC；AUROC_2不依赖高斯分布，而z-ROC回归在高斯SDT解释下用斜率s刻画错误答案与正确答案证据分布的标准差之比。s=1表示等方差，s<1表示正确答案证据分布更分散，s>1表示错误答案证据分布更分散。

> 直观理解：该模块把“知道多少”和“置信度是否跟得上所知”分开：准确率测前者，正确与错误答案的置信可分性测后者；z-ROC还指出两类置信分布为何可能具有不同形状。

**2. 模型无关的$meta-I_{2r}$效率模块**

$meta-I_{2r}$以正确性熵为归一化分母，衡量置信变量与正确性之间的信息量占正确性总不确定性的比例，并通过置信—正确性置换零分布进行有限样本偏差校正。论文没有强行使用meta-d′/d′，因为开放式问答不存在标准meta-d′所需的S1/S2二选一Type-1决策和相应d′分母。

> 直观理解：它衡量“看到模型置信度后，对其是否答对能少猜多少”。选择信息量指标避免把开放问答硬套成二选一任务，否则所谓效率比会主要反映ROC的不等方差，而不是真正的置信信息效率。

**3. 稳健推断与外部效用检验模块**

所有核心估计均配有2000次置信—正确性置换和2000次试次级bootstrap；NLP还需通过各模型×数据集条件下准确率随NLP分位严格递增的单调性检查。选择性预测按NLP排序拒答低置信试次，以覆盖率—准确率关系检验指标是否预测置信筛选增益。

> 直观理解：置换检验排除随机配对产生的虚假信息，bootstrap显示估计的抽样波动；拒答实验则把抽象指标转化为实际问题——模型是否能用自己的置信度挑出更可靠的回答。

**训练与推理**

推理阶段，四个固定模型分别回答TriviaQA与NQ-Open问题，在七个温度下生成自由文本答案并输出逐词元概率；系统据此计算答案级NLP，并以答案别名匹配和SequenceMatcher后备规则产生二元正确性标签。分析阶段按模型×数据集建立T=1.0的固定置信分箱，随后在所需的模型、领域和温度单元内重算Type-2 ROC、AUROC_2、z-ROC斜率、$d_a$及偏差校正$meta-I_{2r}$；每个bootstrap样本都重跑完整流程，而不是只对最终统计量做近似误差传播。最后按NLP排序进行低置信拒答，比较不同覆盖率下的准确率及相对基础准确率的增益。

**复现信息**

评估模型为Llama-3-8B-Instruct、Llama-3-8B-Base、Mistral-7B-Instruct-v0.3和Gemma-2-9B-Instruct，均使用Q5_K_M GGUF量化，通过llama-cpp-python 0.3.16运行；前三个模型属于预注册分析，Gemma-2按相同协议作为注册后的泛化检验。数据包括TriviaQA 5000题和NQ-Open 3000题，每题在四模型、七温度下作答，合计224000试次。置信分箱在每个模型×数据集内由T=1.0的{12.5,…,87.5}百分位确定并跨温度固定；置换和bootstrap均为2000次、试次级重采样，随机种子为42。结果解释必须考虑自动正确性评分的残余模型相关误差：作者说明修正后的评分器仍可能漏判正确答案，因此细粒度跨模型排序不宜视为最终结论。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- TriviaQA：事实问答数据集，是主要分析场景；用于比较四个模型在总体元认知、z-ROC结构、六类知识领域、温度干预及选择性预测上的表现。原文摘要称全部实验合计224,000次事实问答试验，但所给章节未明确报告TriviaQA的单独样本量、数据划分或具体子集。
- Natural Questions（NQ）：第二个事实问答数据集，用于检验跨模型结论能否跨数据集复现，重点考察z-ROC斜率排序以及准确率与$meta-I_2r$的关系。原文未明确报告其单独样本量、划分和预处理方式。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$meta-I_2r$（归一化元认知信息）**

模型无关的二阶效率指标，衡量连续置信信号包含多少关于答案正确与否的信息，并进行了置换零基线偏差校正。它适用于开放式问答，因为该任务缺少计算传统meta-d′效率比所需的二选一一阶决策。 （越高越好；数值越高表示模型自身的置信信号越能区分正确与错误回答，但不等同于模型回答得更准确。）

</div>
<div class="metric-item" markdown="1">

**AUROC_2与z-ROC斜率s**

AUROC_2衡量置信信号把正确回答排在错误回答之前的总体区分能力；z-ROC斜率刻画正确与错误证据分布的方差关系，文中定义s为错误分布标准差与正确分布标准差之比，s<1表示正确回答的证据分布更分散。 （AUROC_2越高通常表示区分能力越强；z-ROC斜率没有统一的越高越好，其相对1的偏离用于识别不等方差结构，而不是直接评定性能优劣。）

</div>
<div class="metric-item" markdown="1">

**Accuracy与50%覆盖率下的选择性预测增益**

Accuracy是一阶事实问答正确率；选择性预测增益是在仅接受置信度最高的一半回答时，筛选后准确率相对原始准确率的百分点提升，用于衡量置信度拒答的部署价值。 （两者均越高越好，但含义不同：准确率衡量模型知道多少，选择性预测增益衡量模型利用自身置信信号筛掉错误回答的能力。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### T=1.0下跨四个模型比较TriviaQA与Natural Questions的总体元认知信息

<div class="result-value" markdown="1">

TriviaQA上的$meta-I_2r$从Gemma-2-Instruct的0.151到Llama-3-Base的0.300，相差1.98倍，且四个估计均显著高于置换零基线（p<0.001）。模型准确率不能稳定预测元认知信息排序：与准确率的Spearman相关在TriviaQA为ρ=-0.80，在NQ为ρ=+0.00。

</div>

不同模型不但“知道多少”不同，也在“能否识别自己答对”方面存在显著差异；准确率较高的模型不一定拥有更有信息的置信信号。由于仅比较四个模型，相关系数主要描述这组系统的排序，不足以证明准确率与元认知能力在更广泛模型总体中独立或存在因果关系。作者同时明确撤回旧版本中“准确率与元认知效率反向耦合”的结论。

<div class="result-source" markdown="1">

来源：第4.3节，表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Metacognitive information varies by a factor of 1.98 across models (meta-I₂r 0.151–0.300 on TriviaQA; Table 3). All four estimates exceed their permutation null (p<0.001).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### T=1.0下TriviaQA六个知识领域的分层分析

<div class="result-value" markdown="1">

Science & Technology是四个模型共同最弱的元认知领域；最强领域则因模型而异，三个模型为Pop Culture & Entertainment，Llama-3-Instruct为Sports。领域跨度也具有模型差异，例如Gemma-2为0.079–0.275，Llama-3-Base为0.256–0.331。

</div>

总体指标会掩盖领域风险：模型可能在流行文化问题上能较好地判断自己是否答对，却在科技问题上难以识别错误。因此，面向特定领域部署时不能仅依赖全数据集平均分。不过该结果来自TriviaQA的领域分类，不能直接推出所有科技问答数据或真实专业场景都会呈现相同排序。

<div class="result-source" markdown="1">

来源：图3及第4.4节，具体数值见表4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Science & Technology is the weakest domain for every model. The strongest is Pop Culture & Entertainment for three models and Sports for Llama-3-Instruct; v2 reported Arts & Literature as strongest, which holds only among the four domains it tabulated.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### TriviaQA上按置信度进行选择性预测，在50%覆盖率下仅接受置信度最高的一半回答

<div class="result-value" markdown="1">

Llama-3-Base准确率由47.8%升至74.0%，增加26.3个百分点；Llama-3-Instruct由58.4%升至82.8%，增加24.4个百分点；Gemma-2由62.7%升至80.1%，仅增加17.4个百分点。四模型中$meta-I_2r$与筛选增益的Spearman相关为ρ=+1.00，而与筛选后的绝对准确率相关为ρ=-0.40。

</div>

$meta-I_2r$预测的是“利用自身置信度拒答能额外获得多少收益”，而不是拒答后最终能达到多高准确率；后者仍主要受原始准确率影响。这给指标提供了直接部署解释，但ρ=+1.00只基于四个模型和一个50%覆盖率工作点，不能保证换模型、换数据集或换覆盖率后仍为完美相关。

<div class="result-source" markdown="1">

来源：第4.6节；完整准确率—覆盖率曲线位于附录B

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At 50% coverage (accepting the top half of responses ranked by NLP), Llama-3-Base improves from 47.8% to 74.0% (+26.3 points) and Llama-3-Instruct from 58.4% to 82.8% (+24.4), while Gemma-2, with the least informative confidence, gains least (62.7% to 80.1%, +17.4).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 跨模型秩相关仅基于四个模型；ρ=-0.80、0.00或+1.00对单个排序变化十分敏感，不应视为对更大模型总体关系的精确估计。
- 正确性状态依赖自动评分标签。尽管v3据摘要称已用1,830条人工裁决验证修正，但旧版结论被长度偏差显著改变，说明任何数值与排序仍需结合人工标注覆盖范围、领域误差和完整评分协议复核。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Llama-3-Instruct：指令微调模型，与其基础版本对照，可观察指令微调后准确率、置信信号结构和元认知信息量是否同步变化。
- Llama-3-Base：基础语言模型；其较高的$meta-I_2r$及随温度显著变化的行为，使其成为检验“准确率与元认知效率可分离”的关键比较对象。
- Mistral-Instruct：另一模型家族的指令微调系统，用于判断结论是否只属于Llama系列；标签修正对它的准确率和$meta-I_2r$排序影响尤其明显。
- Gemma-2-Instruct：总体准确率最高、但两个数据集上置信信息均较弱的比较系统，用于检验高准确率是否必然意味着高元认知信息量。

**实验想回答的问题**

- 在控制模型问答准确率这一一阶能力后，基于答案归一化对数概率的置信信号，能否有效区分正确与错误回答；不同模型、数据集和知识领域的元认知信息量及其信号检测结构是否一致？
- 温度变化和置信度拒答能否将一阶准确率与二阶元认知能力区分开来，以及元认知信息量能否预测选择性预测带来的实际收益？

**实验实现**

实验将答案的token级归一化对数概率作为连续置信变量，将自动评定的答案正确性作为待区分状态。在T=1.0下，对四个模型分别构造二阶ROC，并在probit坐标中拟合z-ROC；八个“模型×数据集”条件均通过置信度四分位上的准确率严格单调性检查，拟合R²均不低于0.98。$meta-I_2r$先减去置换零分布以校正有限样本偏差，显著性由置换检验给出，95%置信区间来自2,000次按试验重采样的bootstrap。温度实验使用T∈{0.3,0.5,0.7,1.0}；选择性预测按归一化对数概率排序，在50%覆盖率下接受置信度最高的一半回答。v3使用修正后的自动正确性标签，并据摘要所述以1,830条人工裁决验证评分修正；所给章节未进一步说明生成参数、提示模板或各数据集拆分。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 温度干预：在TriviaQA上将采样温度设为T∈{0.3,0.5,0.7,1.0} | 四个模型的准确率均随温度升高而下降：Llama-3-Base和Llama-3-Instruct的ρ(acc,T)=-1.00，Gemma-2为-0.93，Mistral为-0.82。与此同时，Mistral、Llama-3-Instruct和Gemma-2的$meta-I_2r$跨温度范围分别仅为0.009、0.016和0.027；Llama-3-Base是例外，范围达到0.103。 | 温度是对生成随机性的干预，可在不更换模型的情况下观察正确率与置信信号信息量是否同步变化。多数模型出现“准确率下降而$meta-I_2r$近乎不变”，支持一阶能力和二阶跟踪能力可被经验区分；Llama-3-Base则表明该分离并非所有模型都相同。该实验没有证明温度只影响单一机制，因为它也可能改变答案类型和错误难度。 | 图4及第4.5节<br><span class="experiment-evidence">Metacognitive information is near-flat for three of four (meta-I₂r range 0.009 for Mistral, 0.016 for Llama-3-Instruct and 0.027 for Gemma-2 across T∈{0.3,0.5,0.7,1.0}), moving in a different direction from accuracy.</span> |
| 自动正确性评分标签修正：比较v2未修正标签与v3修正标签 | 修正后，Mistral的准确率被确认在旧标签中低估13.3个百分点，其$meta-I_2r$由旧标签下的0.328降至0.206，排序从第一降至四模型中的第三；准确率与$meta-I_2r$的旧版完全负相关ρ=-1.00不再成立，修正后TriviaQA为ρ=-0.80、NQ为ρ=+0.00。 | 这一对照隔离了自动评分器的差异化长度偏差：更啰嗦的回答曾被系统性惩罚，从而同时扭曲准确率和元认知排序。结果说明旧版“准确率越高、元认知效率越低”的结论主要是标签伪影，也显示元认知评估对正确性标注质量高度敏感；这不是模型组件消融，而是决定结论有效性的测量消融。 | 第4.3节；版本修正说明见论文第1页<br><span class="experiment-evidence">Mistral’s accuracy was understated by 13.3 points, and on corrected labels it falls from the highest meta-I₂r (0.328) to the third of four (0.206).</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出基于信号检测理论和信息度量的 LLM 元认知置信度评测方法。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`27091ea85be10d8634db524cc8a2a3be6c18d1e6d748ee5a37bb472d67249054`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
