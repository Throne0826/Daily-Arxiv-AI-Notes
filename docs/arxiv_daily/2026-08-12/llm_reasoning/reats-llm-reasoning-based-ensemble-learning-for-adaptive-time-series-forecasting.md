---
title: "[论文解读] REATS: LLM Reasoning-based Ensemble Learning for Adaptive Time Series Forecasting"
description: "[arXiv 2608.10149][LLM Reasoning] REATS将大语言模型用作时间序列预测的智能集成路由器，根据每个样本的文本化时序模式与数值特征，推理并生成可解释的自适应候选模型权重。"
arxiv_id: "2608.10149"
announcement_date: "2026-08-12"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:09:55.945347+00:00"
source_sha256: "6d8f99c480ef630a8679882eeb11e3faf9c5041c4da3e02844043fd1367c9f93"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "时间序列预测"
  - "集成学习"
  - "动态加权"
  - "大语言模型"
  - "集成路由"
  - "文本—数值表示"
  - "可解释预测"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.10149</p>

# REATS: LLM Reasoning-based Ensemble Learning for Adaptive Time Series Forecasting

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Xu Zhang, Chang Xu, Hui Sun, Nan Ma, Zijian Zhang, Peng Wang, Wei Wang, Li Zhao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Fudan University；Microsoft Research；Nankai University；Jilin University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.10149v1) · [PDF 下载](https://arxiv.org/pdf/2608.10149v1) · **关键词** 时间序列预测, 集成学习, 动态加权, 大语言模型, 集成路由, 文本—数值表示, 可解释预测<br>


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

REATS将大语言模型用作时间序列预测的智能集成路由器，根据每个样本的文本化时序模式与数值特征，推理并生成可解释的自适应候选模型权重。

**不用术语来说**：不同预测模型擅长处理不同类型的时间序列，例如某些模型更适合趋势明显的样本，另一些模型可能更善于捕捉周期或局部变化，因此不存在始终最优的单一模型。实际需要解决的不是再训练一个统一预测器，而是针对当前样本判断各候选模型应占多大比重，并且让这一判断能随样本变化、能够解释，也能在候选模型发生变化时保持可用。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出以大语言模型为核心的样本级集成范式：把原始时间序列转换为固定令牌成本的文本—数值混合表示，并加入相似样本先验，使模型能够通过思维链分析时序模式，输出自适应集成权重及自然语言解释。
- 围绕大语言模型学习连续集成权重的困难，设计多行多样化权重监督、节省令牌的百分比表格输出，以及由监督微调到群体相对策略优化的两阶段训练；其中倒数型奖励映射旨在限制无界误差信号，并增强接近最优权重区域的区分能力。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

时间序列预测旨在依据一段按时间排列的历史观测，预测未来连续数值轨迹，常见于能源管理、金融分析和交通规划。Transformer、线性模型和卷积网络等预测器采用不同归纳偏置，分别擅长捕捉不同类型的趋势、周期性或局部变化；由于真实序列的模式及预测场景具有多样性，论文据此采用“多个候选预测模型加一个集成路由器”的设定：候选模型生成各自的预测，路由器再针对当前样本分配权重并形成组合预测。该设定的核心不再是设计一个统一预测器，而是判断每个候选模型对当前样本应贡献多少。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**时间序列预测**

给定按时间顺序排列的历史数值，估计未来一个或多个时间点的连续值。不同序列可能表现出趋势、周期性或不规则波动，因此同一模型未必适合所有样本。

</div>
<div class="concept-item" markdown="1">

**集成学习与动态加权**

集成学习把多个候选模型的输出组合为最终预测；加权集成通常让表现更可靠的模型占更大比例。动态加权进一步按输入样本调整权重，而不是对所有样本使用同一组固定权重。

</div>
<div class="concept-item" markdown="1">

**大语言模型推理式路由**

这里的大语言模型并非直接生成未来数值，而是充当集成路由器，联合读取时间模式的文字描述和数值特征，推理候选模型应如何组合。论文期望它同时输出样本自适应权重和自然语言解释，使权重决策比纯数值黑箱更易检查。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括某个时间序列样本的历史信息、由该样本构造的文本化时间模式描述与数值特征，以及多个候选预测模型对该样本产生的连续数值预测。系统假设候选模型具有互补能力，且不存在一个模型在所有数据集、样本和预测场景上始终最优；其输出是一组随样本变化的候选模型权重、相应的组合预测，以及解释权重选择的自然语言推理。与固定平均或依据整体验证误差设置静态权重不同，REATS研究的是如何让大语言模型依据当前样本的混合文本—数值表示进行动态路由；候选模型输出的是数值轨迹而非文本回答，因此面向自然语言回答排序或融合的既有大语言模型集成方法不能直接套用。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **基于训练或验证误差的传统静态集成方法（Bertsimas et al.; Chen et al.; Gruber et al.）**: 这类方法采用均匀平均、逆误差加权或其他固定规则，简单且高效，但权重主要由整体训练或验证表现确定，不能随当前输入的时间模式充分变化；它们构成REATS所比较和试图改进的静态集成范式。
- **基于神经网络与强化学习的动态集成方法（Fu et al.）**: 这类方法从数值时间序列中提取特征，并依据预测奖励学习样本级权重，已经具备动态适应能力；但原文指出其只能利用数值输入，不能借助文本语义与大语言模型推理解释决策，而且候选模型变化时通常需要重新训练，因此在表达能力和候选模型迁移灵活性上仍有缺口。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现实时间序列在趋势、周期性、波动强度和局部动态等方面具有显著差异，而采用不同架构与建模假设的预测器各有适用范围。因而，固定选用一个模型会把同一种建模策略强加给所有样本，难以充分利用候选模型之间的互补性。应用层面的关键需求是进行样本级路由：对每条输入序列动态分配合适的候选模型权重，以提高预测准确性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **固定或静态集成**：依据预先设定的规则或验证集误差，为候选预测模型确定固定权重或静态组合策略；部署后，同一组权重通常被用于具有不同模式的时间序列样本。
- **数值驱动的神经网络动态路由**：训练小型神经网络读取时间序列的数值输入，并针对当前样本预测候选模型的组合权重，从而实现比固定加权更细粒度的动态分配。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 固定权重或基于验证误差的静态策略不能随单个样本的复杂、动态时序模式调整权重，导致集成器无法充分匹配不同候选模型与不同样本之间的适配关系。
- 小型神经路由器主要依赖数值输入，缺少对文本化模式语义的利用，其权重决策通常是难以解释的黑箱；当候选模型发生变化时还需要重新训练，限制了跨候选集合使用的灵活性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚未建立一种面向时间序列预测的推理式集成机制，能够联合理解时序模式的语义描述与数值证据，在样本级生成可解释权重，并适应候选模型变化。与此同时，直接让大语言模型学习集成权重还面临输入令牌成本、连续数值输出、监督信号稀疏或单一，以及回归奖励无界且易被异常值主导等训练障碍。

</div>
<div markdown="1"><span>核心问题</span>

能否把轻量级大语言模型训练成时间序列集成路由器，使其依据每个样本的文本—数值混合信息进行结构化推理，稳定地产生接近优良组合的候选模型权重，并在跨数据集迁移或遇到未见候选模型时仍保持有效且可解释的决策？

</div>
<div markdown="1"><span>作者直觉</span>

候选预测器的优劣往往与可描述的时序特征有关；如果先把冗长的原始序列压缩成趋势、周期和变化等模式描述，同时保留必要的数值证据，大语言模型就可以像分析案例一样比较当前样本与各模型的长处，而不只是拟合一组难以理解的数字映射。再以相似样本的既有表现作为参考，并通过结构化推理约束其输出，模型便可能把“识别模式—判断适配性—分配权重”的过程显式化，从而兼顾自适应性与可解释性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

REATS把时间序列集成建模为一个由大语言模型执行的“样本级路由”问题。对每个待预测样本，系统接收历史序列、候选预测模型及其预测结果，先把长度可变的原始序列压缩成固定令牌开销的文本—数值混合表示，其中既包含趋势、周期性、波动性和自相关等可读模式描述，也保留用于区分模型表现的数值特征；随后检索少量相似历史样本作为先验，并让语言模型按“序列模式分析→候选模型与模式匹配→参考相似案例→形成权重结论”的顺序推理，最终输出多组整数百分比权重。将权重与各候选模型预测加权求和，即得到集成预测。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 固定预算的时间序列表征

从原始序列提取趋势、季节性、波动性和自相关等时间特征，并将其组织为文本描述与数值特征并存的混合输入；该表示被设计为固定令牌成本，使输入开销不随原始序列长度线性增长。原文节选未给出全部特征的计算公式、归一化方式和最终提示模板。

<div class="method-step__io" markdown="1">

**输入**：单个预测样本的历史时间序列、候选模型信息以及各候选模型的预测结果。<br>
**输出**：可直接输入语言模型、长度受控且保留主要时间语义的文本—数值表示。

</div>

**直观理解**：它不是把每一个时间点都写进提示词，而是先制作一份定长的“序列体检报告”。文字让模型理解模式含义，数字则提供更精确的强弱程度和预测依据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 相似样本检索与先验注入

执行检索增强生成，即为当前样本寻找 $k$ 个相似参考案例，并把这些案例作为路由决策的上下文先验。消融结果表明默认采用少量高相似邻居更合适：$k=3$ 的平均MSE为 $0.1210$，低于 $k=25$ 的 $0.1262$；作者将其解释为大量较弱相关案例会向推理过程引入噪声。

<div class="method-step__io" markdown="1">

**输入**：当前样本的混合表示，以及由历史训练样本及其模型配置或权重信息组成的检索库。<br>
**输出**：包含当前序列描述、候选模型信息和少量相似案例先验的增强提示。

</div>

**直观理解**：这相当于在决定如何分配模型权重前，先翻看几份最相似的历史病例。参考案例太多时，边缘相关的样本反而可能干扰当前判断。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 规则化推理与多行权重监督构造

按固定逻辑自动构造规则链式思维，使文本依次说明序列模式、模型适配关系、检索案例和分配结论，无需调用外部大模型API生成推理文本；同时为一个样本构造多行具有差异的候选权重，而非只提供单个最优向量。权重采用整数百分比表表达，以降低小数生成难度、输出令牌数和数值幻觉风险。

<div class="method-step__io" markdown="1">

**输入**：增强提示、候选模型信息，以及训练阶段可获得的近似最优权重或其监督信号。<br>
**输出**：由结构化推理文本和多组百分比权重组成的监督样本。

</div>

**直观理解**：训练答案不仅给出“各模型占多少”，还给出一条格式稳定的判断过程；多行权重则像给学生多个质量不同、但都可评分的方案，使后续训练获得更密集的比较信号。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 两阶段微调与回归奖励优化

先用监督微调学习结构化推理格式和合理的初始权重策略，再以SFT模型初始化GRPO；GRPO计算生成权重相对oracle权重的预测MSE差距 $\delta$，通过有界倒数映射获得奖励，并在同一提示的生成组内标准化为优势。默认奖励还组合逐行MSE奖励与oracle引导，节选报告默认系数为 $\lambda_1=0.8$、$\lambda_3=0.2$。

<div class="method-step__io" markdown="1">

**输入**：第一阶段的规则推理—权重监督数据，以及第二阶段针对同一提示采样得到的多条推理和权重输出。<br>
**输出**：能够针对每个样本生成自然语言理由和自适应集成权重的REATS策略模型。

</div>

**直观理解**：SFT先教会模型按规定格式思考和答题，GRPO再让它一次提出多个方案，并依据实际集成误差比较这些方案。倒数奖励会突出已经接近最优方案之间的细微差别，同时限制极差方案对整组评分尺度的破坏。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 倒数MSE差距奖励

$$
\delta=\mathcal{L}(\mathbf{w})-\mathcal{L}(\mathbf{w}^{*}),\qquad r(\delta)=\frac{1}{1+k\delta}
$$

**符号说明**

- $\mathbf{w}$：语言模型生成的一行候选模型集成权重。
- $\mathbf{w}^{*}$：以预测MSE为准得到的oracle集成权重，即用于比较的近似最优权重。
- $\mathcal{L}(\mathbf{w})$：使用权重向量进行候选预测加权后得到的预测均方误差。
- $\delta$：生成权重相对oracle权重的MSE差距；越接近零表示生成方案越接近oracle。
- $k$：控制奖励曲线敏感度和衰减速度的正缩放因子，论文推荐值为20。
- $r(\delta)$：提供给GRPO的有界非线性奖励；误差差距越小，奖励越接近1。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先用oracle方案作为参照，计算生成权重多造成了多少MSE，再把差距映射为倒数奖励。其导数绝对值为 $k/(1+k\delta)^2$，在所有有限的 $\delta\geq0$ 上都为正，因而没有线性截断函数那样的硬“无信号区”；同时奖励有界，极差样本不能无限增大组内方差。<br>
**原文位置**：附录A.5.1给出差距定义与映射比较；附录A.5.2式(8)、附录A.5.3式(14)讨论倒数映射的敏感度。

</div>

</div>

<div class="equation-block" markdown="1">

#### GRPO组内标准化优势

$$
\hat{A}_{i}=\frac{r_{i}-\mu_{r}}{\sigma_{r}},\qquad \mu_{r}=\frac{1}{G}\sum_{j=1}^{G}r_{j},\qquad \sigma_{r}=\sqrt{\frac{1}{G}\sum_{j=1}^{G}(r_{j}-\mu_{r})^{2}}
$$

**符号说明**

- $G$：针对同一个提示采样的生成结果数量，即GRPO组大小。
- $r_i$：组内第i个生成结果的奖励。
- $\mu_r$：该生成组的平均奖励。
- $\sigma_r$：该生成组奖励的标准差，用于衡量组内奖励离散程度。
- $\hat{A}_i$：第i个生成相对于同组其他生成的标准化优势，用于缩放策略梯度更新。

<div class="equation-explanation" markdown="1">

**直观理解**：GRPO不直接看一个方案的绝对分数，而是看它相对同组方案好多少。若无界的 $r=-\delta$ 遇到一个极端差方案，$\sigma_r$ 会被放大，使两个近优方案之间的标准化优势差被压缩；有界倒数奖励通过改变整组奖励几何关系缓解这一问题。<br>
**原文位置**：附录A.5.3，式(11)；组内优势间距的进一步分析见式(13)。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标分为互补的两个阶段。SFT阶段以规则生成的结构化CoT和多行百分比权重为监督，使模型学会从混合输入与RAG案例形成可读推理，并按规定格式产生权重；多行监督比单一最优向量覆盖更多权重质量层次，为策略阶段提供较好的初始化。GRPO阶段则直接依据生成权重造成的预测MSE优化策略：同一提示采样多个输出，对 $K'$ 行权重分别计算反馈，再按组归一化优势更新模型。作者区分逐行的 $r_{\mathrm{mse}}$、先聚合各行再评分的 $r_{\mathrm{agg}}$ 和引导输出接近oracle的 $r_{\mathrm{oracle}}$；节选称纯逐行奖励配置G5在所有数据集上优于纯聚合奖励G6，而默认G1采用 $\lambda_1=0.8$ 与 $\lambda_3=0.2$，在实际MSE优化和小数据集上的oracle稳定作用之间折中。原文节选未给出完整总奖励公式以及各系数与三个奖励项的一一对应关系，因此不应据此补写未展示的目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 文本—数值混合路由输入**

该模块把原始时间序列转化为固定令牌成本的语义描述和数值特征，并同时提供候选模型信息。相较只接收预测值或统计量的神经网络集成器，语言模型可以显式联系“趋势、周期、波动、自相关”等模式与不同预测模型的归纳偏置；但原文节选未完整披露特征清单和编码模板，因此不能据此复现具体特征工程。

> 直观理解：纯数字路由器通常只能从训练数据中隐式猜测规律；混合输入则把关键现象直接命名，再用数字校准其程度，使模型能够用较稳定的概念跨数据集推理。

**2. 规则CoT与多行百分比权重监督**

规则CoT使用与GPT生成CoT相同的时间特征、候选模型信息、RAG参考和显式oracle权重，但通过确定性规则生成结构一致的推理文本。多行监督为每个样本提供 $K'$ 行权重，GRPO可逐行计算 $r_{\mathrm{mse}}$；百分比表将连续权重改写为紧凑的整数分配，从而降低语言模型处理高精度小数时的复杂度。

> 直观理解：规则CoT的重点不是模拟自由发挥，而是提供稳定、可学习的推理骨架。多行答案让同一个样本产生多次可比较反馈，整数表则减少格式错误和看似精确但实际无效的小数。

**3. 面向连续误差的倒数GRPO奖励**

先令 $\delta=\mathcal{L}(\mathbf{w})-\mathcal{L}(\mathbf{w}^{*})$，其中 $\mathcal{L}$ 是集成预测MSE、$\mathbf{w}$ 是生成权重、$\mathbf{w}^{*}$ 是oracle权重，再使用 $r(\delta)=1/(1+k\delta)$。与无界线性奖励 $r=-\delta$ 相比，该映射把奖励限制在有界区间内，并通过非线性改变组内优势间距；论文选择 $k=20$，报告其满足判据的有效区间为 $[10,25]$。

> 直观理解：若直接使用负误差，一个极差输出会把组内标准差拉得很大，使几个好输出之间的差别在标准化后几乎消失。倒数映射压住极端差值，又在接近最优处保持较高分辨率，因此更适合后期精修权重。

**训练与推理**

训练时，先为每个序列样本计算固定预算的文本—数值特征，并准备候选模型描述、候选预测及oracle权重；从样本库检索少量相似案例后，依据统一规则生成CoT，再把多组权重写成整数百分比表，由此建立SFT数据。完成SFT后，以该检查点启动GRPO：对每个增强提示采样一组推理—权重回答，把每一行权重转换为候选预测的加权结果，计算其相对oracle的MSE差距，经倒数函数映射为奖励，并依据组内标准化优势更新策略。CoT在此阶段还承担探索机制：不同推理路径可能强调趋势、周期性或自相关，从而产生更多样的权重；节选报告去掉CoT时八个数据集平均MSE为 $0.1151$，加入CoT后为 $0.1080$，作者计算为 $6.2\%$ 相对改善。

推理时无需oracle权重，也不再进行梯度更新。系统对新序列执行相同的特征转换和相似样本检索，把当前序列、候选模型信息及参考案例输入约17亿参数的REATS模型；模型先输出结构化理由，再输出权重表，最后对各候选模型预测加权得到最终预测。候选模型名称或描述可通过提示调整，这为未见候选模型泛化提供接口，但并不意味着任意新模型都必然有效：路由器仍需从描述和观察到的预测特征中判断其适用模式。

**复现信息**

复现和公平解释结果时最关键的设置包括：REATS使用约1.7B参数的可完整微调模型，作者称其可在单张轻量级GPU上训练和部署；RAG邻居数采用 $k=3$，因为节选中的比较显示其平均MSE为 $0.1210$，优于 $k=25$ 的 $0.1262$；倒数奖励缩放因子采用 $k=20$，作者按近oracle敏感度、中等差距信号和远距离非零信号三项判据确定其有效范围为 $[10,25]$；默认GRPO奖励配置G1使用 $\lambda_1=0.8$、$\lambda_3=0.2$。输出权重使用整数百分比表，规则CoT替代付费API生成的CoT。当前节选没有明确报告基础模型名称、序列特征的完整定义、提示模板、检索相似度函数、$K'$ 的具体取值、组大小 $G$、采样温度、学习率、批量大小、训练轮数和硬件型号，这些信息仍须回查论文完整方法、附录或代码后才能严格复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ETT系列：ETTh1、ETTh2、ETTm1和ETTm2，属于能源或电力设备时间序列。它们用于检验方法在不同采样粒度和相近领域数据上的稳定性。原文仅说明附录表7提供统计量，当前节选未给出各数据集的样本规模。
- Exchange与Weather：分别代表金融汇率和气象领域，用于测试跨领域时间模式下的路由能力。所有实验均采用单变量预测，历史输入长度和预测长度均为$96$，训练集、验证集、测试集按$7:1:2$划分。
- Electricity与Traffic：分别代表电力负荷和交通流量场景，用于考察集成方法在大型、多序列实际数据上的表现。当前节选未给出变量数量、时间跨度和采样频率，因此不能据此比较各数据集的绝对规模。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**MSE**

均方误差，对预测值与真实值之差进行平方后取平均；平方会更重地惩罚较大的预测偏差，是正文比较和GRPO奖励构造的核心指标。 （越低越好，因为数值越低表示预测与真实序列的平方偏差越小。）

</div>
<div class="metric-item" markdown="1">

**MAE**

平均绝对误差，对预测值与真实值的绝对差取平均；与MSE相比，它对少数极端误差不那么敏感。当前节选说明结果位于附录表14，但未提供具体数值。 （越低越好，因为数值越低表示平均绝对预测偏差越小。）

</div>
<div class="metric-item" markdown="1">

**符号检验$p$值**

根据REATS在各数据集上相对比较方法的胜负次数，检验其逐数据集优势是否可能由随机波动造成；它衡量的是跨数据集胜负的一致性，而不是误差改善幅度。 （通常越低表示反对“双方胜率无差别”的证据越强；论文以$p<0.05$报告统计显著性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 八个基准上的基础模型候选池

<div class="result-value" markdown="1">

REATS-GRPO取得平均MSE $0.1384$，相对验证集估计的固定权重OptW$_{\rm val}$的$0.1597$降低$13.3\%$，并在八个数据集上全部获胜。REATS从SFT阶段的$0.1455$进一步改善到GRPO阶段的$0.1384$。

</div>

作者据此主张，按样本生成权重比对所有测试样本使用同一固定权重更有效，而且基于预测误差的GRPO优化能够在模仿预言机权重之后继续改善预测。分析上，这一结果支持REATS在该候选池和统一协议下的有效性，但不能单凭八个数据集上的平均值证明其对任意基础模型池或任意预测长度都有效。

<div class="result-source" markdown="1">

来源：第4.2节，表2(a)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

REATS-GRPO achieves the lowest average MSE of 0.1384, reducing error by 13.3% over OptWval and winning on all eight datasets.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 八个基准上的小型专用模型候选池

<div class="result-value" markdown="1">

在候选质量差异更大的条件下，REATS-GRPO的平均MSE为$0.1080$，相对训练集估计的固定权重OptW$_{\rm tr}$的$0.1352$降低$20.1\%$。作为难度背景，TimeXer平均MSE为$1.6664$，均匀平均为$0.3173$，最佳零样本大语言模型Codex为$0.1709$。

</div>

作者将该结果解释为：经过专门微调的大语言模型路由器能识别弱模型和不可靠模型何时仍具有互补价值。更谨慎地说，实验表明REATS能在这一高度异质的既定候选池中避免被差模型严重拖累；它并未证明自然语言推理本身是唯一原因，因为SFT、RAG、权重监督格式和GRPO同时参与了最终系统。

<div class="result-source" markdown="1">

来源：第4.2节，表2(b)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

REATS-GRPO achieves 0.1080, reducing error by 20.1% over OptWtr, demonstrating that fine-tuned LLM reasoning can effectively identify complementary strengths even among weak and unreliable models.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 从小型专用模型训练迁移到未见过的基础模型候选

<div class="result-value" markdown="1">

REATS-GRPO在分布外候选池上的平均MSE为$0.1442$，优于OptW$_{\rm val}$的$0.1564$，相对误差降低$7.8\%$；同时优于最佳零样本大语言模型DeepSeek-V3.2的$0.1626$，相对降低$11.3\%$。

</div>

作者据此认为REATS学习了时间特征与模型能力之间可迁移的关系，而非只记忆候选模型名称。该实验确实排除了“测试时仍使用原训练候选模型”这一简单解释，并明确禁止使用测试标签重建知识库；但候选描述和RAG知识库会利用新模型在训练集上的预测重新构造，因此这里验证的是允许训练域适配信息时的候选模型迁移，不是完全无适配的零信息迁移。

<div class="result-source" markdown="1">

来源：第4.2节，表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

REATS-GRPO achieves 0.1442, outperforming the best traditional baseline (OptWval: 0.1564) by 7.8% and the best zero-shot LLM (DeepSeek-V3.2: 0.1626) by 11.3%.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前节选缺少表2、表3、图4和附录消融的完整数据，因此无法核验各数据集逐项结果、MAE表现、方差或置信区间，也无法评价DAPO、DrGRPO、GSPO和SAPO等GRPO变体是否公平且显著地弱于所提奖励映射。
- 主实验固定为单变量、输入长度$96$和预测长度$96$，并允许在分布外候选测试前利用新候选模型的训练集预测重建RAG知识库。因而结论尚不能直接外推到多变量预测、其他预测跨度、完全无训练域适配的新模型，或计算资源受限场景；推理延迟、令牌成本和与简单路由器的成本收益比较亦未在当前节选中报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 单个候选预测器：包括TimeXer、LSINet、CARD、TimeMixer等小型专用模型，以及MOMENT、Sundial、Timer、TimesFM、Chronos等基础模型。该比较用于确认是否存在一个始终占优的单模型，并判断集成是否确有必要。
- 启发式与误差型集成：包括均匀平均、随机权重、逆MSE加权和最优固定权重OptW。OptW使用与REATS预言机权重相同的非负单纯形约束二次规划，但训练或验证后对所有测试样本使用同一组权重，因此是检验“逐样本自适应”价值的关键基线；下标$m tr$或$m val$表示权重估计所用的数据划分。
- RLMC：一种基于神经网络或强化学习的集成方法，直接接收原始历史序列，并与REATS共享数据划分、候选预测和预言机监督。它用于区分大语言模型的文本化推理路由与传统数值黑盒路由。
- 零样本大语言模型集成：包括GPT-5.2/5.5、Codex、DeepSeek-V3.2和Grok-4，使用与REATS相同的时间特征、工具描述、RAG参考及“先推理后决策”输出格式，但不进行微调。它用于判断性能提升来自提示中的通用大语言模型能力，还是来自REATS的专门监督与奖励优化。

**实验想回答的问题**

- 在固定候选模型池与统一数据划分下，REATS能否根据每个样本的时间模式自适应地产生集成权重，并在基础模型候选与小型专用模型候选两种异质性条件下，优于单模型、固定权重、神经网络路由和零样本大语言模型路由方法？
- REATS学到的是可迁移的时间模式与候选模型能力之间的关系，还是仅记住了训练时的模型身份？具体通过未见候选模型的分布外测试，以及候选数量从$N=2$扩展到$N=8$的实验进行检验。

**实验实现**

实验统一采用长度为$96$的历史窗口预测未来$96$步，并按$7:1:2$划分训练、验证和测试数据。默认每次集成$4$个候选模型，同时测试$N=2,4,6,8$的扩展性。基础大语言模型为Qwen3-1.7B；检索模块为每个样本返回$K=3$个相似样本，监督中每个样本包含$K'=10$行权重，其中一行为二次规划预言机权重、九行为多样化权重。倒数奖励映射采用$k=20$，奖励系数为$(\lambda_1,\lambda_2,\lambda_3)=(0.8,0,0.2)$，格式违规惩罚为$-0.5$。推理时仅使用第一行权重。所有SFT监督及GRPO奖励中的预言机权重只由训练集真实标签构造；分布外实验会根据新候选模型在训练集上的预测重建RAG知识库和候选描述，不读取测试标签。训练硬件为NVIDIA A100，但当前节选未报告随机种子、重复次数、置信区间、具体GPU数量或训练成本。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 两阶段训练中SFT与GRPO的增量比较 | 在基础模型候选池中，平均MSE由仅完成SFT后的$0.1455$下降至加入GRPO后的$0.1384$，绝对下降$0.0071$，按SFT结果计算约为$4.9\%$的相对下降。 | 该比较主要隔离第二阶段基于预测误差的强化优化是否能超越对预言机权重的监督模仿。结果支持GRPO阶段具有额外贡献，但它没有单独隔离倒数奖励映射：要证明特定奖励映射优于普通奖励或其他GRPO变体，还需要第4.3节所述对照的完整数值，而当前节选未提供。 | 第4.2节，表2(a)<br><span class="experiment-evidence">The consistent SFT→GRPO gain (0.1455→0.1384) confirms that MSE-based reward effectively refines weights beyond imitation learning.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The method trains an LLM with supervised fine-tuning and GRPO to reason over time-series evidence and produce adaptive ensemble weights.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`6d8f99c480ef630a8679882eeb11e3faf9c5041c4da3e02844043fd1367c9f93`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
