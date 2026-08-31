---
title: "[论文解读] Regime-Aware Portfolio Management via Retrieval-Augmented LLM-Guided Expert Switching"
description: "[arXiv 2608.28252][LLM Agent] 原文未明确报告。"
arxiv_id: "2608.28252"
announcement_date: "2026-08-31"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:44:43.129823+00:00"
source_sha256: "8b383535773b9394a2a74e6d0a125a40cc68ae7f3a4016648085af6d3d22f5d7"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "知识库系统"
  - "检索增强生成"
  - "大语言模型"
  - "专家切换"
  - "投资组合管理"
  - "金融市场"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.28252</p>

# Regime-Aware Portfolio Management via Retrieval-Augmented LLM-Guided Expert Switching

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Ahmad Asadi, Reza Safabakhsh</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Deep Learning Lab, Computer Engineering Department, Amirkabur University of Technology, Hafez Avenue, Tehran, Iran</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28252v1) · [PDF 下载](https://arxiv.org/pdf/2608.28252v1) · **关键词** 知识库系统, 检索增强生成, 大语言模型, 专家切换, 投资组合管理, 金融市场<br>


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

本文研究非平稳金融市场中的自适应投资组合管理。非平稳性是指价格、波动率、资产间相关性及收益规律会随时间变化，因此某一投资组合策略在一种市场状态下有效，并不意味着在另一种状态下仍然有效。论文将投资组合管理视为连续的序贯决策问题：系统根据当前市场信息选择或激活一个已有的专业策略（expert），再由该策略生成投资组合，而不是要求一个单一模型在所有市场环境中同时完成预测、风险控制和资产配置。论文重点讨论如何利用历史上相似市场情境下各专家的实际表现，进行有依据的专家切换。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**非平稳性与市场状态（regime）**

非平稳性表示数据生成规律会变化，例如市场可能在低波动、高波动、上涨或下跌状态之间转换。市场状态是对这些潜在环境的概括；论文不假设所有历史时期共享同一套收益和风险规律。

</div>
<div class="concept-item" markdown="1">

**专家切换与混合专家**

混合专家（Mixture-of-Experts, MoE）维护多个擅长不同输入区域或市场环境的模型，并由一个门控机制选择或组合它们的输出。本文更关注选择哪个完整的投资组合管理专家，而非让单一模型扩大规模来覆盖所有情况。

</div>
<div class="concept-item" markdown="1">

**检索增强与变分自编码器**

检索增强方法先从历史知识库中找出与当前输入相似的案例，再将这些案例作为决策依据。变分自编码器（VAE）是一种学习低维概率表示的模型；本文用双流VAE分别编码资产层面技术指标和市场整体特征，以便比较当前情境与历史情境的相似性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

设系统在每个决策时刻接收两类当前市场信息：一类是单个资产层面的技术指标，另一类是市场范围的宏观或整体特征。双流VAE将这两类信息编码为市场情境的紧凑表示，系统据此从历史知识库中检索相似情境，并读取各投资组合专家在这些情境中的历史表现。预先给定专家集合，每个专家能够根据市场数据构造投资组合；系统的输出不是由大语言模型直接生成的交易动作，而是被选中的专家，随后由该专家负责后续投资组合构建。该设定假定历史相似情境及专家表现具有一定参考价值，同时承认测试期可能出现训练期未充分覆盖的新市场状态；研究目标是在加密货币、股票和外汇市场中提高累计收益与风险调整后的表现，并降低单一固定专家或不可靠门控机制在状态变化下的失效风险。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

当前时刻的市场输入，包含资产层面的技术指标与市场范围特征。

</div>
<div class="notation-item" markdown="1">

**$z$**

由双流变分自编码器得到的市场情境低维表示，用于与历史情境进行相似度检索。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{E}$**

预先给定的投资组合专家集合；其中每个专家代表一种可独立执行的投资组合管理策略。

</div>
<div class="notation-item" markdown="1">

**$e^*$**

切换机制根据当前情境和检索到的历史证据选出的专家，并由该专家生成后续投资组合。

</div>

</div>

**直接相关的工作**

- **深度学习与强化学习投资组合管理**: 已有研究使用循环神经网络、卷积结构、时间注意力以及深度强化学习预测收益、波动率或方向，并将投资组合优化表示为序贯决策。论文承接强化学习对收益—风险权衡的处理方式，但将重点从训练一个端到端策略转向在多个已有专家之间进行情境感知的选择。
- **金融领域的混合专家与门控机制**: 既有混合专家方法通常通过监督式门控网络或元学习动态组合专家输出，在训练分布覆盖充分时能够提升预测表现。论文指出，当测试市场状态偏离训练分布时，门控网络可能把权重分配给不匹配的专家；因此本文改用历史情境检索和专家绩效陈述作为选择依据，并进一步分析新增局部优势专家不会降低整体性能的单调性。

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

该方法面向非平稳市场中的自适应投资组合管理，输入是近期资产级与市场级行情窗口以及一组已有投资组合专家。系统先用双流 Transformer-VAE 将当前窗口和历史窗口编码到同一潜在空间，再离线建立“市场状态—专家表现”索引；在线阶段检索与当前状态相似的历史片段，计算各专家的相似度加权表现，并将检索到的数值记录、Performance Statement（SoP）和当前市场描述交给指令微调的 LLM。LLM 只负责结合历史证据进行风险收益判断和专家切换，不直接生成投资组合权重；最终由被选中的专家输出权重向量。直观地说，系统不是让 LLM 凭空预测市场或下单，而是先在历史数据库中寻找“以前出现过的相似行情”，查看不同策略当时表现，再选择更合适的策略执行。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双流市场状态构造

分别构造资产级张量 $S_t^{\mathrm{tech}}\in\mathbb{R}^{L\times A\times F_1}$ 和市场级张量 $S_t^{\mathrm{mkt}}\in\mathbb{R}^{L\times F_2}$。前者包含对数收益率、RSI、MACD、ATR、实现波动率和成交量变化，后者包含总体趋势、波动率状态和流动性变量；所有特征采用滚动 $z$ 分数标准化。

<div class="method-step__io" markdown="1">

**输入**：当前或历史时刻的滚动行情窗口，长度为 $L$；资产数量为 $A$；资产级特征数为 $F_1$；市场级特征数为 $F_2$。<br>
**输出**：两个保持独立语义来源的标准化市场状态表示。

</div>

**直观理解**：资产级信息回答“每个资产最近表现如何”，市场级信息回答“整个市场处于什么环境”。先分开整理这两类信息，可以避免个别资产的局部变化掩盖全市场的共同状态。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双流 Transformer-VAE 编码

两个预训练 Transformer-VAE 编码器分别输出高斯后验的均值与对角协方差，并使用重参数化采样得到 $z_t^{\mathrm{tech}}$ 和 $z_t^{\mathrm{mkt}}$。随后将两者拼接为统一状态向量 $h_t\in\mathbb{R}^{D}$；历史窗口和当前窗口必须使用同一编码函数，以保证最近邻距离位于同一潜在空间。

<div class="method-step__io" markdown="1">

**输入**：资产级状态 $S_t^{\mathrm{tech}}$ 和市场级状态 $S_t^{\mathrm{mkt}}$。<br>
**输出**：当前或历史市场窗口的潜在表示 $h_t$ 或 $h_\tau$。

</div>

**直观理解**：VAE 将高维、噪声较大的行情压缩成较短的“市场状态指纹”。同一套压缩规则处理过去和现在，才能有意义地判断两个行情窗口是否相似。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 离线历史表现索引

对每个历史时刻 $\tau$ 编码得到 $h_\tau$，从该状态分别执行每个专家，并在未来 $H$ 个时间单位内计算其累计收益、Sharpe ratio 和最大回撤。系统同时生成描述市场片段、专家行为及不确定性因素的 SoP，并将状态、各专家表现和 SoP 存入向量数据库。

<div class="method-step__io" markdown="1">

**输入**：历史市场数据、专家集合 $\mathcal{E}=\{E^{(e)}\}_{e=1}^{E}$ 和固定前视评估 horizon $H$。<br>
**输出**：历史索引条目 $\mathcal{D}_\tau=(h_\tau,\{R_\tau^{e}\},\{\mathrm{SoP}_\tau^{e}\})$。

</div>

**直观理解**：这一步把过去的经验整理成可查询档案：每条档案不仅记录当时市场长什么样，还记录每个策略在随后一段时间赚了多少、承受了多大风险。它在部署前完成，因此不必在每次决策时重新评估所有历史策略。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在线检索与证据聚合

当前窗口经同一双流编码器得到 $h_t$，再检索距离最近的 $K$ 个历史状态构成 $\mathcal{N}_t$。根据相似度计算归一化权重 $w_\tau$，并对每个专家的历史结果进行相似度加权，得到当前状态下的表现估计 $\hat{R}_t^{(e)}$，同时计算加权不确定性。

<div class="method-step__io" markdown="1">

**输入**：当前市场窗口、向量数据库、专家集合和检索数量 $K$。<br>
**输出**：与当前市场最相似的历史证据、各专家的加权表现估计及其不确定性。

</div>

**直观理解**：系统会优先参考更像当前行情的历史案例，而不是把所有历史平均对待。相似案例越多、越接近当前状态，对专家选择的参考价值通常越高。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 双流潜在状态拼接

$$
h_t=[z_t^{\mathrm{tech}}\mid z_t^{\mathrm{mkt}}]\in\mathbb{R}^{D}
$$

**符号说明**

- $h_t$：时刻 $t$ 的统一市场状态潜在向量。
- $z_t^{\mathrm{tech}}$：由资产级技术特征流编码得到的潜在向量。
- $z_t^{\mathrm{mkt}}$：由市场级特征流编码得到的潜在向量。
- $\mid$：向量拼接操作，而非条件概率符号。
- $D$：拼接后潜在向量的总维度。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把两种互补的市场信息合并为一个可检索的状态指纹。历史状态和当前状态都经过同样的拼接过程，因此可以直接在这个空间中进行最近邻匹配。<br>
**原文位置**：式（14），第 3.6 节

</div>

</div>

<div class="equation-block" markdown="1">

#### 相似度加权的专家表现估计

$$
\hat{R}_{t}^{(e)}=\sum_{\tau\in\mathcal{N}_{t}}w_{\tau}R_{\tau}^{(e)},\qquad w_{\tau}=\frac{\mathrm{sim}(h_t,h_{\tau})}{\sum_{j\in\mathcal{N}_{t}}\mathrm{sim}(h_t,h_j)}
$$

**符号说明**

- $\hat{R}_{t}^{(e)}$：时刻 $t$ 对专家 $e$ 的相似度加权表现估计。
- $\mathcal{N}_{t}$：与当前状态最接近的 $K$ 个历史状态集合。
- $w_{\tau}$：历史状态 $\tau$ 对当前估计的归一化检索权重。
- $\mathrm{sim}(h_t,h_{\tau})$：当前潜在状态与历史潜在状态之间的相似度。
- $R_{\tau}^{(e)}$：专家 $e$ 从历史状态 $\tau$ 出发、在前视区间 $H$ 内获得的实际表现。
- $e$：候选投资组合专家的索引。

<div class="equation-explanation" markdown="1">

**直观理解**：该式不是预测单一未来价格，而是把若干相似历史案例中的专家结果按相似程度平均起来。越接近当前市场的案例权重越大，所得估计随后与 SoP 和 LLM 判断一起用于路由。<br>
**原文位置**：式（17）—（18），第 3.8 节

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文所给章节未明确报告该路由器的端到端联合训练目标。双流 VAE 在预训练阶段通过解码器重构输入来学习潜在表示；预训练后移除解码器并固定或保留编码器用于状态匹配。专家表现不是通过该系统重新优化得到的，而是在离线阶段执行已有专家并记录其在前视区间 $H$ 内的表现。LLM 则通过提示约束进行推理与不确定性校准，而非直接优化投资组合权重；原文未明确报告其参数是否在本研究中进一步更新。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双流 Transformer-VAE 状态表示**

资产级流和市场级流分别对 $S_t^{\mathrm{tech}}$ 与 $S_t^{\mathrm{mkt}}$ 建模，并输出各自的高斯潜变量；解码器仅用于预训练阶段的输入重构，部署时保留编码器。拼接后的 $h_t$ 同时用于历史索引和在线检索，因此表示空间的一致性是匹配机制成立的必要条件。

> 直观理解：单一输入流可能混淆“某个资产的特殊表现”和“全市场共同变化”。双流设计保留了这两种互补线索，使系统更可能找到真正相似的市场片段，而不是只找到表面数值相近的片段。

**2. 检索增强的历史表现知识库**

每个历史状态对应所有专家在固定前视区间 $H$ 内的实际表现记录和 SoP。在线时通过近邻集合 $\mathcal{N}_t$ 取证，并以相似度权重聚合专家表现；知识库将状态相似性与策略结果直接绑定，避免只依据通用市场描述选择专家。

> 直观理解：它相当于一本按市场情境分类的策略案例库。系统关心的不是某个专家总体上是否优秀，而是它在“类似当前环境”中是否有效。

**3. 保守的 LLM 路由器与单调性保障**

LLM 接收检索证据并产生风险收益评估 $\rho_i(s)$，但不生成权重。设计采用经验范围约束、对新专家施加风险缓冲以及尾部情景检查；理论上在估计误差、保守切换和专家区域优势等条件下，新增专家不会降低期望效用。

> 直观理解：新增策略只有在证据显示它明显更好时才替换当前策略；如果优势可能只是估计噪声，系统保持原策略。这种“宁可不换，也不因小差异乱换”的规则用于保护组合稳定性。

**训练与推理**

训练或离线准备阶段包括两部分：首先，使用资产级和市场级历史窗口预训练两个 Transformer-VAE 编码器，使其能够重构输入并获得稳定的高斯潜变量；其次，对每个历史时刻编码状态、执行所有专家、计算未来 $H$ 内的累计收益、Sharpe ratio 和最大回撤，并生成 SoP 后写入向量数据库。提示词经过验证集上的迭代设计，最终限制数值评估不得超出检索证据的经验范围，在证据稀疏时回退到历史基线统计，并要求单独分析尾部事件。

**复现信息**

在线决策从当前滚动窗口开始，分别构造 $S_t^{\mathrm{tech}}$ 和 $S_t^{\mathrm{mkt}}$，使用与离线阶段相同的编码器得到 $h_t$，并从历史向量索引中检索 $K$ 个近邻。系统据此计算每个专家的 $\hat{R}_t^{(e)}$ 及加权不确定性，再把检索到的 SoP、表现摘要和当前市场上下文输入 LLM；LLM 输出结构化记录，包括专家标识、评估值、误差界限、切换边际和尾部最优标志，路由器据此选择专家。论文明确给出的关键切换原则是：候选专家相对 incumbent 的估计优势必须超过切换阈值 $\tau$；理论分析要求估计误差上界为 $\epsilon$ 且 $\tau\geq2\epsilon$，但实际系统中相关阈值、相似度具体形式、$K$ 的最终取值以及不确定性计算细节，原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 加密货币市场：选取流动性最高的30种资产，并配套两个合成市场指数；由于不存在标准加密货币指数，作者同时构造等权累计收益指数和成交量加权累计收益指数。其作用是测试方法在高波动、强周期性的市场环境中的适应性。来源为第4.1节、表2和图5。
- 股票市场：选取30只高流动性美国股票，并使用标普500、纳斯达克综合指数和道琼斯工业平均指数作为市场层面的参考序列。其作用是测试方法在具有共同宏观趋势但个股行为存在差异的资产面板上的表现。来源为第4.1节、表3和图6。
- 外汇市场：选取30个高流动性货币对；原文未报告可与该货币对集合直接对应的标准综合市场指数，因此市场状态主要由状态编码器的聚合特征流表示。其作用是测试方法在缺乏统一市场基准、资产间关系不同于股票和加密货币的环境中的泛化性。来源为第4.1节、表4。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**累计收益率（Cumulative Return）**

衡量评估期内投资组合相对于初始资金的累计增长幅度，直接反映最终财富增长。 （通常越高越好，但不能单独说明收益承担了多大风险。）

</div>
<div class="metric-item" markdown="1">

**夏普比率（Sharpe Ratio）**

衡量单位总波动所获得的收益，即把收益与整体收益波动联系起来的风险调整指标。 （越高越好，因为表示在相近波动下获得了更高收益，或以更低波动获得了相近收益。）

</div>
<div class="metric-item" markdown="1">

**最大回撤（Maximum Drawdown，MDD）**

衡量净值从历史峰值下降到随后谷值的最大幅度，用于刻画最严重的不利阶段损失。 （回撤绝对值越小越好；表中的负值越接近零，说明下行损失越小。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 独立专家性能：三类市场中的专家池异质性

<div class="result-value" markdown="1">

作者报告不同专家在收益、风险调整收益、最大回撤和主导频率上各有优势，没有一个专家在三类市场及所有指标上同时最优。例如，加密货币中 TQC 的累计收益最高，为 $76.16\%$；股票中 CrossQ 的累计收益最高，为 $38.21\%$，而 PPO 的夏普比率最高，为 $0.96$；外汇中 A2C 的累计收益最高，为 $4.27\%$，而 PPO 的最大回撤最小，为 $-2.00\%$。这些数值均来自表5的完整表格行。

</div>

该实验首先验证切换问题是否值得研究：如果所有专家表现几乎相同，切换就没有明确收益来源。结果显示专家优势依赖市场和评价指标，因此存在选择“当前状态下更合适专家”的机会。不过，单次完整面板运行只能说明本次实验中存在异质性，不能证明这些优势在不同时间段或随机种子下都稳定。

<div class="result-source" markdown="1">

来源：第4.2节及表5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In cryptocurrency, TQC achieves the highest cumulative return (76.16%), while DDPG obtains the highest Sharpe (1.74) and Sortino (2.73); A2C has the smallest MDD (-25%) and the highest dominance frequency (34.5%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 切换策略的跨市场比较

<div class="result-value" markdown="1">

摘要报告，所提出的 RAG 专家选择器在加密货币、股票和外汇三类市场中，均取得所评估选择策略中最高的累计收益和夏普比率。所给实验节在表6标题后未提供具体完整数值，因此除摘要明确报告的股票示例外，其他市场的精确数值为原文未明确报告。

</div>

这一结果支持方法的核心经验性主张：根据相似历史状态及其对应专家表现进行选择，可能比始终持有一个专家或只看最近5天表现更有效。它证明的是本论文实验协议下的相对优势，而不是证明大语言模型在所有金融市场、所有时间段或真实交易成本条件下必然优越；由于每个市场只运行一次，也不能据此估计统计显著性。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments across cryptocurrency, stock, and foreign-exchange markets show that the proposed selector achieves the highest cumulative return and Sharpe ratio among the evaluated selection strategies in all three markets.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 股票市场中的最佳固定专家与 RAG 选择器

<div class="result-value" markdown="1">

在股票市场示例中，最佳固定专家的累计收益为 $26\%$，RAG 选择器提高到 $34\%$；夏普比率从 $0.74$ 提高到 $0.96$。该比较说明动态选择同时改善了最终累计收益和单位波动收益。

</div>

相对于事先选定一个全局表现最好的专家，RAG 选择器能够在不同状态间更换候选策略，因此股票实验显示出明显的组合收益。这里的“最佳固定专家”必须以论文规定的评估期结果为依据理解，不能解读为事前可知的无偏基准；同时，所给摘录没有提供交易成本、置信区间或多次运行结果。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In the stock market, for example, cumulative return increases from 26% for the best fixed expert to 34%, while the Sharpe ratio improves from 0.74 to 0.96.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验按每个市场只运行一次，结果是单次点估计而非多随机种子均值；原文未报告置信区间、统计显著性或重复实验稳定性，因此跨策略的小幅差异可能无法判断是否稳健。
- 所给摘录没有提供表6及后续消融实验的具体结果，也未明确报告训练、验证和测试日期切分、交易成本或滑点设置；因此无法仅凭当前材料评估时间外推能力和真实交易净收益。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Best Fixed Expert：在整个评估期内始终使用同一个表现最好的专家，用来检验动态切换是否真正优于全局最优的静态选择。
- Recent-Performance Gating：根据滚动最近5天的已实现表现选择专家，用来区分“短期追逐近期赢家”与“检索历史相似市场状态”两种选择依据。
- A2C、DDPG、PPO、TQC和CrossQ单独运行的专家：这些不是切换器，而是独立专家基线，用来确认候选池内部确实存在性能异质性，并提供固定专家比较对象。
- Proposed RAG：提出的检索增强专家切换方法；它是主要待评估方法，而不是传统基线，用来检验历史相似状态检索与大语言模型推理的联合效果。

**实验想回答的问题**

- 五个具有不同强化学习归纳偏置的专家是否在不同市场或市场状态下表现出互补性，从而为动态切换提供实际改进空间？
- 基于历史相似情形检索并由大语言模型选择专家的机制，是否优于固定专家和仅依据近期表现的选择策略？

**实验实现**

所有市场均使用长度为 $L=22$ 个交易日的滚动输入窗口和 $H=5$ 天的持有期，以保持跨市场评估协议一致。每个市场均使用完整的30个符号面板，每项实验只运行一次，因此结果是单次运行的点估计，而不是多个随机种子的均值。检索库按时间顺序建立：对每个训练时刻 $t$，保存变分自编码器（VAE）嵌入 $z_t$、已实现收益 $R_t$ 以及随后 $H=5$ 天的摘要；测试时只允许检索满足 $\tau<t$ 的历史观测，避免未来信息泄漏。检索使用嵌入维度 $d=64$ 的余弦相似度，取最近邻数量 $K=3$。大语言模型每个决策步最多调用一次，温度为 $0.1$；原文未在所给实验节中明确报告训练集、验证集和测试集的具体日期切分。所有实验在单张 NVIDIA H100 GPU 上运行。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 市场指数可视化提供了一个定性案例：加密货币的成交量加权指数呈现2021年牛市、2022年回撤以及2024至2025年的反弹后部分反转；等权指数在2024年末出现极端飙升并随后剧烈修正。作者据此将成交量加权指数作为主要市场层面描述量，因为原始价格的等权聚合容易被少数极端成分主导。该案例说明市场状态表示会受到聚合方式影响，但它是数据与状态表示的可视化解释，不是独立的预测性能证明。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Uses retrieval-grounded LLM reasoning to dynamically select portfolio-management experts under changing market regimes.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`8b383535773b9394a2a74e6d0a125a40cc68ae7f3a4016648085af6d3d22f5d7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
