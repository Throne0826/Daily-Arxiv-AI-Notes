---
title: "[论文解读] Can Large Language Models Execute Parent Orders?"
description: "[arXiv 2607.28410][LLM Agent] 本文研究大语言模型能否在无需预设市场行为假设和任务专用训练的条件下执行母订单，并以长周期规划、短周期调整相分离的 PACE 框架验证这一可能性。"
arxiv_id: "2607.28410"
announcement_date: "2026-07-31"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.336480+00:00"
source_sha256: "02497947c1a23e6abaed651aca680ab8a53771b1326b24cd14e80699f332be0a"
tags:
  - "LLM Agent"
  - "LLM 其他"
  - "母单执行"
  - "算法交易"
  - "执行成本"
  - "市场冲击"
  - "大语言模型"
  - "分层规划"
  - "PACE"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2607.28410</p>

# Can Large Language Models Execute Parent Orders?

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Shen, Zane, Xu, Xinli, Zhang, Guangyi, Chen, Jialong, Zhou, Jinsong, Chen, Cong, Shen, Guibao, Yan, Dongyu, Wang, Luozhou, Yang, Zhen</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.28410) · [PDF 下载](https://arxiv.org/pdf/2607.28410) · **关键词** 母单执行, 算法交易, 执行成本, 市场冲击, 大语言模型, 分层规划, PACE<br>
**代码**: [https://github.com/zaneopen/PACE](https://github.com/zaneopen/PACE)

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

本文研究大语言模型能否在无需预设市场行为假设和任务专用训练的条件下执行母订单，并以长周期规划、短周期调整相分离的 PACE 框架验证这一可能性。

**不用术语来说**：机构若一次性提交一笔大额买卖订单，可能暴露交易意图并推动价格向不利方向变化；但若把它拆成多笔小订单，又必须持续决定每个时点交易多少，既要争取更有利的成交价格，也要确保在截止时间前完成全部订单。市场价格同时包含较慢的趋势和大量短期噪声，因此这一数量分配问题难以依靠固定规则稳定解决。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者声称首次系统研究大语言模型在母订单执行中的应用，将其金融用途从决定“交易什么”扩展到决定“如何执行”，并建立相应的实验与行为分析框架。
- 作者提出 PACE，将长周期执行计划与依据短期市场变化进行的数量调整分离，目标是在不预设具体市场模型、也不训练任务专用策略的情况下生成执行决策。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

母单执行属于算法交易中的交易执行问题。机构若一次性提交大额买卖单，可能暴露交易意图、造成市场冲击，并失去随行情变化调整订单的机会，最终以更差价格成交。母单执行因此将一笔大额“母单”拆成多个较小的“子单”，核心是在规定期限内决定各时点的成交数量，使买单尽量低价成交、卖单尽量高价成交，从而降低执行成本。现有方案主要分为两类：静态方法依据预设的价格动态、成交量分布或市场冲击模型制定执行轨迹；学习方法从历史数据中训练自适应策略。本文把大语言模型引入这一问题，研究重点由“交易什么资产”转向“已知要交易的母单应如何执行”。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**母单与子单**

母单是需要在一段时间内完成的大额交易指令，子单是将其拆分后分批提交的小额订单。拆分能降低一次性交易造成的价格冲击，并保留根据后续市场变化调整数量的空间。

</div>
<div class="concept-item" markdown="1">

**执行成本与市场冲击**

执行成本反映实际成交价格相对于某个参考价格的不利偏离；买得更贵或卖得更便宜通常意味着成本更高。市场冲击是交易行为本身推动价格向不利方向变化的现象，大额订单更容易产生明显冲击。

</div>
<div class="concept-item" markdown="1">

**长周期趋势与短周期波动**

论文将价格变化理解为较缓慢的长期趋势与围绕趋势发生的短期噪声或波动的组合。该区分支持其分层设计：先根据较长时间尺度规划总体执行进度，再依据短期行情调整具体交易量。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一笔方向、总数量和完成期限已经确定的母单，以及执行期间可观察到的深圳证券交易所 Level-1 市场数据；输出是在各决策时点应提交的子单数量，且全部母单需要在截止时间前完成。策略要在价格高度噪声、市场规律可能漂移的环境中分配交易进度，目标是降低成交价格带来的执行成本。本文关注推理时决策：大语言模型结合当前市场观察生成长周期计划和短周期数量调整，不要求先指定价格动态、日内成交量或市场冲击的函数形式，也不为该执行任务单独训练策略。原文节选没有给出母单数量、时点动作或成本函数的正式符号定义，因此此处不补造数学记号。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Almgren and Chriss (2001)**: 代表性的静态执行方法，以均值—方差框架权衡执行成本和风险，并依赖预先设定的市场影响等建模假设。本文将 Almgren–Chriss 作为代表性基线，用来检验无需显式价格模型的 LLM 执行框架能否优于经典模型驱动策略。
- **Ning et al. (2021)**: 代表数据驱动的强化学习执行路线，通过任务专用的状态、动作和奖励学习自适应策略。它体现了本文试图解决的另一类限制：市场模式或任务规格变化时，策略设计与训练往往需要相应调整，而 PACE 旨在直接利用预训练模型在推理阶段决策。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

母订单执行直接影响金融机构的交易成本。大额订单若一次成交，容易暴露意图、造成不利价格冲击，而且无法随市场变化调整；拆单后则产生一个动态决策问题：在有限期限内如何分配各时点的交易量，使买入价格尽量低或卖出价格尽量高，同时完成全部订单。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于预设市场假设的传统执行策略**：这类方法先规定市场或成交量的简化结构，再据此安排交易，例如假设日内成交量分布固定，或使用 Almgren-Chriss 一类模型在预设价格冲击与风险结构下求取执行轨迹；TWAP 则按时间近似均匀地拆分订单。
- **基于数据学习的执行策略**：这类方法利用历史市场数据训练预测模型或决策策略，例如 XGBoost、LSTM 以及强化学习方法，并围绕特定任务定义状态、动作和奖励，使模型学习各时点应提交的交易量。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统策略依赖固定成交量分布等简化假设及其参数；真实市场未必符合这些形式，参数也会随时间漂移，因此预先求得的执行轨迹可能在市场结构变化后失效。
- 学习型策略依赖任务专用的奖励、状态和动作设计；当市场模式、订单条件或任务规格变化时，策略往往需要重新设计或训练，限制了其对新环境的适应能力。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有大语言模型金融研究主要回答“交易什么”，包括金融文本理解、因子挖掘和交易代理，却尚未系统检验模型能否解决“如何执行”的母订单拆分问题。因而仍缺少一种能够利用通用先验知识、在推理时产生决策，并同时摆脱显式市场假设与任务专用策略训练的执行框架。

</div>
<div markdown="1"><span>核心问题</span>

大语言模型能否用于母订单执行，即能否在不依赖预设市场行为模型和任务专用训练的情况下，决定各时点的交易数量并降低执行成本？

</div>
<div markdown="1"><span>作者直觉</span>

作者观察到价格序列可理解为较稳定的长周期趋势与噪声较强的短周期波动叠加。若让同一决策过程直接逐时响应全部波动，模型容易被短期噪声干扰；PACE 因而让 Planner 先依据长周期信息制定整体交易安排，再让 Executor 根据近期变化有限度地调整数量。通俗地说，它先确定“整段时间大致怎么做”，再处理“眼前这一小步要不要加快或放慢”，从而兼顾全局完成目标与局部市场适应性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PACE（Plan-Ahead Controlled Execution）把母订单执行建模为“长期规划—短期执行—市场撮合—绩效评估”的分层流程。输入包括母订单 $O=(s,d,t_s,t_e,Q)$、执行开始前及执行过程中的价格与成交量历史，以及均匀分配数量的 TWAP 参考曲线；Planner 先判断整个执行窗口的价格趋势并把总量分配到 $N$ 个等长子时段，Executor 再依据最新局部市场信息逐次调整相对 TWAP 的下单量。两层输出都受到控制系数约束，因此大语言模型只在 TWAP 附近改变交易节奏，而不是不受限制地直接生成订单。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造订单、市场历史与TWAP参考

以最优卖价与最优买价的均值作为中间价，并整理回看窗口内的价格—成交量序列。按照决策间隔 $\Delta$ 将执行窗口划分为 $K=(t_e-t_s)/\Delta$ 个决策时点，生成每次交易 $Q/K$ 的 TWAP 曲线。

<div class="method-step__io" markdown="1">

**输入**：母订单 $O=(s,d,t_s,t_e,Q)$，其中 $s$ 为股票标识，$d\in\{\mathrm{BUY},\mathrm{SELL}\}$ 为方向，$[t_s,t_e]$ 为执行窗口，$Q$ 为目标数量；另输入逐分钟最优卖价、最优买价和成交量。<br>
**输出**：结构化母订单、市场历史 $\mathcal{H}$ 与参考执行曲线 $\mathcal{C}^{\mathrm{TWAP}}$。

</div>

**直观理解**：TWAP 相当于先准备一份“平均速度完成订单”的保守日程表。PACE 后续不是从零猜测交易量，而是在这份日程表附近做有边界的调整。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. Planner进行长期趋势判断与分段配额

Planner 由大语言模型生成整个执行窗口的文字趋势判断 $\mathcal{R}^{L}$，并输出各子时段的数量偏好 $a_n\in[-1,1]$ 与整体置信度 $c\in[0,1]$。随后把 TWAP 的均匀权重与偏好分数的 softmax 权重混合，将总量 $Q$ 分配到 $N$ 个等长子时段。

<div class="method-step__io" markdown="1">

**输入**：母订单 $O$、执行开始前长度约为执行窗口的市场历史 $\mathcal{H}_{t_s-T:t_s}$，以及 TWAP 曲线 $\mathcal{C}^{\mathrm{TWAP}}$。<br>
**输出**：长期趋势评估 $\mathcal{R}^{L}$，以及子计划集合 $\{S_n=(u_n,v_n,q_n)\}_{n=1}^{N}$，其中每个子计划规定起止时间和应完成数量。

</div>

**直观理解**：这一层决定“哪几个阶段多交易、哪几个阶段少交易”，类似先按天气预报安排整段行程。置信度越低，分配越接近均匀 TWAP，从而降低不可靠判断造成的大幅偏移。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. Executor进行短期动态下单

每个决策时点由大语言模型输出调整分数 $z_t\in[-1,1]$，再用受控乘法规则把基准数量调整为 $Q_t^E$。长期判断提供方向背景，最新局部价格和成交量则用于决定当前时点相对 TWAP 加速还是减速。

<div class="method-step__io" markdown="1">

**输入**：当前子计划 $S_n$、最近 $\tau$ 分钟的市场历史 $\mathcal{H}_{t-\tau:t}$、Planner 的长期判断 $\mathcal{R}^{L}$，以及单次 TWAP 基准数量 $Q^{\mathrm{TWAP}}$。<br>
**输出**：当前时点提交的订单数量 $Q_t^E$；连续决策最终形成完整的时间—数量执行曲线。

</div>

**直观理解**：Planner 决定每一段的大致预算，Executor 决定这一段内部何时具体多下或少下。这样可以同时利用较稳定的长趋势与快速变化的局部行情，避免只看其中一个尺度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 撮合成交并计算执行结果

Matcher 按订单方向、价格和当前盘口判断能否成交：激进设置下买单报在 $A_t$、卖单报在 $B_t$，通常立即成交；被动设置下买单报在 $B_t$、卖单报在 $A_t$，价格更有利但可能未成交。Evaluator 根据实际成交订单计算完成率和相对 TWAP 的价格表现。

<div class="method-step__io" markdown="1">

**输入**：策略生成的订单，以及每个市场快照中的最优卖价 $A_t$ 和最优买价 $B_t$。<br>
**输出**：成交订单序列、平均成交价、完成率以及以基点计量的价格表现。

</div>

**直观理解**：该环境区分了“付出价差换取立即成交”和“等待更好价格但承担未成交风险”。因此评估的不只是模型建议了多少数量，还包括这些订单在现实盘口规则下是否能够成交。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 置信度控制的长期数量分配

$$
w_{n}=(1-\lambda c)\frac{1}{N}+\lambda c\frac{\exp(a_{n})}{\sum_{j=1}^{N}\exp(a_{j})}
$$

**符号说明**

- $w_n$：第 $n$ 个子时段获得的总量权重，各时段权重之和为 $1$。
- $N$：执行窗口被划分出的等长子时段数量。
- $a_n$：大语言模型对第 $n$ 个子时段的数量偏好分数，取值范围为 $[-1,1]$；数值越大表示越倾向于在该时段多交易。
- $c$：Planner 对整组偏好判断的置信度，取值范围为 $[0,1]$。
- $\lambda$：控制 LLM 分配影响强度的超参数，取值范围为 $[0,1]$。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项是每段获得 $1/N$ 的均匀 TWAP 分配，第二项把偏好分数经 softmax 转为总和为 $1$ 的非均匀分配；权重 $\lambda c$ 决定采用后者的程度。当 $c=0$ 或 $\lambda=0$ 时完全退回均匀分配，而较高的置信度会允许模型更明显地前置或后置交易量。<br>
**原文位置**：第3.3节，公式(5)

</div>

</div>

<div class="equation-block" markdown="1">

#### 受控的短期下单量调整

$$
Q^{E}_{t}=(1+\gamma z_{t})Q^{\mathrm{TWAP}}
$$

**符号说明**

- $Q_t^E$：Executor 在时点 $t$ 生成的实际订单数量。
- $Q^{\mathrm{TWAP}}$：同一决策时点的 TWAP 基准订单数量。
- $z_t$：大语言模型生成的当前数量调整分数，取值范围为 $[-1,1]$；正值增量、负值减量、零表示遵循 TWAP。
- $\gamma$：控制局部订单相对 TWAP 最大偏离程度的超参数，取值范围为 $[0,1]$。

<div class="equation-explanation" markdown="1">

**直观理解**：该式将 LLM 的判断限制为对 TWAP 数量的乘法修正，而不是让模型任意输出规模。当 $z_t=0$ 时执行 TWAP；当 $\gamma$ 较小时，即使模型给出极端分数，实际数量也只会小幅变化，从而形成风险控制边界。<br>
**原文位置**：第3.3节，公式(6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。PACE 不进行面向母订单执行任务的参数训练，也没有反向传播优化的损失函数；文中的核心公式是推理阶段的确定性控制与数量映射规则，而非训练目标。方法依赖预训练大语言模型已有的通用先验，通过提示输入订单、市场历史、TWAP 参考和交易术语，使模型生成受范围约束的 $a_n$、$c$ 与 $z_t$，再由外部公式转换为执行数量。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Long-horizon Planner**

Planner 将执行窗口切分为 $N$ 个等长子时段，生成文本趋势评估、每段偏好分数 $a_n$ 和统一置信度 $c$。其分配规则通过 $\lambda c$ 在均匀 TWAP 权重与 LLM softmax 权重之间插值，并据此令各段数量满足 $q_n=w_nQ$。

> 直观理解：该模块解决跨越整个执行窗口的总量安排问题。置信度门控使模型在不确定时自动退回接近 TWAP 的保守方案，而不是强行采纳尖锐的分配判断。

**2. Short-horizon Executor**

Executor 在每个决策时点读取当前子计划、最近局部市场历史和长期趋势文本，输出数量调整分数 $z_t$。参数 $\gamma$ 限制相对 TWAP 的最大偏离幅度，使局部响应不能无限放大。

> 直观理解：即使长期方向判断正确，短时间内价格仍会波动，因此还需要逐时点修正。该模块相当于在既定分段预算内寻找更合适的具体成交时机。

**3. Matcher与Evaluator**

Matcher 保存尚未成交的订单，并在每个盘口快照检查买单价格是否达到 $A_t$、卖单价格是否低至 $B_t$；满足条件即成交并从挂单集合移除。Evaluator 同时使用完成率衡量是否完成目标数量，并用方向调整后的相对 TWAP 价格表现衡量执行成本。

> 直观理解：只比较预测信号无法说明策略能否实际交易，该模块把模型输出放入明确的成交规则中。完成率与价格表现必须共同考虑，否则策略可能通过少成交或不成交来获得表面上较好的价格。

**训练与推理**

推理开始时，系统只调用一次 Planner：它读取执行前历史、母订单和 TWAP 曲线，输出长期趋势文本、各子时段偏好及置信度，再生成整段子计划。执行期间，Executor 在每个决策时点读取当前可用的局部历史、所属子计划及长期判断，生成 $z_t$ 并计算 $Q_t^E$；订单随后进入 Matcher，成交结果由 Evaluator 汇总。默认方案不会在执行中更新 Planner；论文另测了每个子计划结束后用最新历史重规划剩余窗口的变体，但这属于设计分析而非默认流程。

**复现信息**

复现或公平解释方法时必须保留三项设置。第一，价格输入采用最优卖价与最优买价的中间价，市场历史还包括逐分钟总成交量；第二，$\lambda$、$\gamma$ 与子计划时长 $\tau$ 分别控制长期 LLM 权重、短期调整幅度和规划粒度，原文指出中等取值更稳健，但所给节选未明确报告默认数值；第三，激进与被动报单使用不同的盘口价格，后者可能遗留未成交订单，因此比较价格表现时还必须检查完成率。模型如何满足分数范围、提示模板全文、决策间隔和剩余数量约束等细节在所给节选中未完整报告，复现前仍需核对论文正文及补充材料。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 深圳证券交易所Level-1快照数据，覆盖2026年4月的全部交易日。实验在每个交易日随机生成10个母单；母单生成细节位于补充材料，当前节选未给出股票数量、订单规模分布、买卖方向比例及训练集、验证集、测试集划分。该数据用于回放市场状态并比较不同策略的执行成本。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$wbp$**

表1用于衡量母单执行表现的指标。正文以基点（bps）报告不同策略之间的改善，但当前节选未展开该缩写、计算公式、价格基准及符号方向，因此无法仅据节选严格判断它对应执行收益、执行成本还是相对基准价格的滑点。 （按“improves $wbp$”及“positive gains”的表述，作者将更高或更有利的$wbp$视为更好；其严格方向仍需结合论文中的指标定义与表1表头核验。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 全主动订单提交设置，PACE最佳变体与TWAP及最强基线比较

<div class="result-value" markdown="1">

PACE最佳变体的$wbp$相对TWAP提高1.02 bps，相对所有参评基线中表现最强者提高0.65 bps。

</div>

这表明在实验所构造的深圳证券交易所母单上，PACE不仅胜过简单的均匀拆单，还超过了AC、XGBoost和LSTM候选基线中的最佳方法。0.65 bps是更严格的增量，因为它以最强竞争者而非较弱的TWAP为参照。不过，该结果只覆盖2026年4月、随机生成的母单和当前报价机制，不能单独证明其在其他市场、真实机构订单或不同交易费用条件下仍有同等优势。

<div class="result-source" markdown="1">

来源：第4.2节，表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under the aggressive setting, its best variant improves wbp over TWAP by 1.02 bps, and over the strongest baseline by 0.65 bps.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 全被动订单提交并在最后一分钟执行sweep，PACE最佳变体与TWAP及最强基线比较

<div class="result-value" markdown="1">

PACE最佳变体的$wbp$相对TWAP提高1.07 bps，相对最强基线提高0.71 bps。

</div>

该结果检验优势能否延伸到先挂被动单、临近截止时间再强制完成剩余数量的执行流程。相对最强基线的0.71 bps改善说明PACE的收益并非只在全主动成交方式中出现。但由于被动单可能无法成交，最终效果会受到排队位置、成交模型及最后一分钟sweep成本的影响；当前节选没有给出这些因素的独立分析。

<div class="result-source" markdown="1">

来源：第4.2节，表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under the passive setting, the corresponding improvements are 1.07 bps and 0.71 bps.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨大语言模型比较：ChatGPT-5.4与DeepSeek-v4-flash

<div class="result-value" markdown="1">

两个大语言模型驱动的PACE变体均取得正向增益，作者据此认为该框架可跨不同模型工作；当前节选未分别给出两个模型的完整数值。

</div>

这一结果提供了初步的模型可迁移性证据：PACE的有效性并非只来自单一闭源模型。然而，实验只包含两个模型，而且二者默认推理强度不同，因此尚不能把差异完全归因于模型能力，也不能证明框架对更广泛模型家族普遍有效。

<div class="result-source" markdown="1">

来源：第4.2节，表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In addition, both LLM variants achieve positive gains, suggesting that PACE works across different models.

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

- TWAP（时间加权平均价格）策略：按时间较均匀地拆分母单，是简单、常用且不依赖预测模型的执行基准，可检验PACE是否优于固定时间调度。
- Almgren–Chriss（AC）策略：基于市场冲击与风险之间权衡的经典最优执行方法，用于比较PACE与依赖预设市场模型及假设的传统策略。
- XGBoost学习型策略：以树模型从数据中学习执行决策，用于检验无需任务特定训练的PACE能否超过监督学习式基线；当前节选未说明其特征、标签与训练划分。
- LSTM学习型策略：利用循环神经网络建模时间序列信息，用于比较PACE与能够学习市场动态的神经网络基线；当前节选未提供网络结构及训练细节。

**实验想回答的问题**

- PACE在全主动成交与全被动挂单两种提交方式下，能否比TWAP、Almgren–Chriss以及学习型策略取得更好的母单执行效果？
- 性能改善是否同时出现在闭源模型ChatGPT-5.4和开源模型DeepSeek-v4-flash上，从而初步表明PACE不依赖某一个特定大语言模型？

**实验实现**

作者评估两种订单报价设置：全主动设置直接以可成交方式提交订单；全被动设置以被动方式挂单，并在最后一分钟撤销未成交订单、主动成交剩余数量，这一收尾过程称为sweep。为降低大语言模型利用身份信息造成的信息泄漏风险，输入中删除股票代码和交易日期。每个母单重复运行8次，以减弱模型随机性的影响。PACE分别使用闭源ChatGPT-5.4与开源DeepSeek-v4-flash，均采用默认API参数；前者默认推理强度为none，后者为high。主要超参数为$\lambda=0.3$、$\gamma=0.5$、$\tau=5$分钟和$\Delta=1$分钟，但当前实验节选未提供$\lambda$与$\gamma$的具体定义。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper proposes an LLM-based hierarchical planning and execution framework for sequential trading decisions.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`02497947c1a23e6abaed651aca680ab8a53771b1326b24cd14e80699f332be0a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
