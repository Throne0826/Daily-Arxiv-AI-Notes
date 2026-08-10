---
title: "[论文解读] CoBa: Cost-Effective Test-Time Scaling via Compute-Balanced Routing"
description: "[arXiv 2608.07424][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.07424"
announcement_date: "2026-08-10"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-10T02:39:11.498974+00:00"
source_sha256: "0ab0a51ae18c431c34c6764e888e60fc9c55609c8a011f3742dd3e6acda69ab2"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "测试时扩展"
  - "计算分配"
  - "动态路由"
  - "候选解采样"
  - "验证器"
  - "数学推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.07424</p>

# CoBa: Cost-Effective Test-Time Scaling via Compute-Balanced Routing

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Yan Zhou, Yue Ouyang, Kaiyang Zheng, Suncheng Xiang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> School of Mathematics and Statistics, Changsha University of Science and Technology, Changsha, China；School of Biomedical Engineering, Shanghai Jiao Tong University, Shanghai, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.07424v1) · [PDF 下载](https://arxiv.org/pdf/2608.07424v1) · **关键词** 测试时扩展, 计算分配, 动态路由, 候选解采样, 验证器, 数学推理<br>


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

测试时扩展（test-time scaling）研究的是：在模型已经训练完成后，如何在推理阶段额外投入计算以提高答案质量。对推理任务而言，额外计算可用于生成更多候选解、延长推理过程，或调用验证器判断候选解是否可靠；本文关注的核心不是单独扩大其中一项，而是在固定推理预算下，将计算动态分配给生成、轻量验证、强验证或停止。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**候选解采样与自一致性**

模型对同一题目生成多条推理链和答案，形成候选解集合。自一致性通常以多数答案作为最终输出，借由多次采样降低单次生成出错的影响。

</div>
<div class="concept-item" markdown="1">

**验证器**

验证器是对候选解或其中间推理步骤进行正确性、可信度判断的模型或程序。轻量验证成本较低但判断能力有限，强验证通常更可靠，也消耗更多计算。

</div>
<div class="concept-item" markdown="1">

**参数加权 token 成本**

本文用参数量与生成或评估 token 数共同刻画推理成本，因此大模型处理同样长度文本会被计为更高成本。它用于比较不同生成器和验证器组合下的计算开销，而非直接表示实际延迟。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一道需要多步推理的输入，以及可用的本地生成模型、轻量验证器和强验证器，系统在有限的推理预算内逐步决定下一次操作：继续采样一个候选解、对已有候选做轻量验证、将部分候选送入强验证，或停止并输出答案。系统的目标是在预算约束下提高最终答案准确率；论文尤其考察竞争数学和程序化符号推理场景，并假定不同题目及不同候选的歧义程度不同，因而不应固定地对所有样本使用相同数量的采样或强验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

待求解的输入题目或推理实例。

</div>
<div class="notation-item" markdown="1">

**$c_i$**

针对输入 $x$ 生成的第 $i$ 个候选解及其推理过程。

</div>
<div class="notation-item" markdown="1">

**$B$**

单个实例在测试时可使用的固定推理计算预算。

</div>
<div class="notation-item" markdown="1">

**$a_t$**

第 $t$ 个决策时刻采取的动作，可对应采样、轻量验证、强验证或停止。

</div>

</div>

**直接相关的工作**

- **Wang et al. (2022), self-consistency**: 该工作通过多次采样推理链并聚合最终答案提升鲁棒性，是本文“增加生成计算”这一基线思路的代表。CoBa进一步询问：在已有候选后，额外预算是否应继续采样，还是应转投验证。
- **Cobbe et al. (2021); Lightman et al. (2024), verifier and process supervision**: 这些工作说明验证候选答案及中间推理步骤可以改善数学推理质量，为本文的轻量与强验证层提供方法背景。本文的区别在于不固定调用某一种验证强度，而是根据可观察的候选证据和不确定性进行路由。

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

CoBa 将测试时推理建模为固定预算 $B$ 下的序贯计算分配：面对题目 $x$，系统不是预先固定“生成多少条解答”或“对所有解答使用多强的评审器”，而是持续决定下一步应生成新候选、使用哪一级验证器，还是停止并输出答案。候选为 $c=(r,a)$，其中 $r$ 是推理轨迹、$a$ 是抽取出的最终答案；真实标签 $y$ 仅用于离线评估，绝不输入路由策略。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 初始候选生成

从 $G(x)$ 采样 $k$ 个候选 $c_j$ 并加入候选集合 $C$，同时从剩余预算 $b$ 扣除每次生成的成本。该固定小规模预热旨在先获得答案多样性，而不在开始就生成完整的大候选池。

<div class="method-step__io" markdown="1">

**输入**：问题 $x$、生成器 $G$、预算 $B$ 与预热数量 $k=2$。<br>
**输出**：含两个初始推理轨迹及其最终答案的候选集合 $C$，以及更新后的预算 $b$。

</div>

**直观理解**：系统先让生成器独立作答两次，先检查是否已有不同思路；这相当于先用小成本确认题目是否存在明显分歧。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 全候选低成本筛查

对所有候选计算答案频率，并由 $V_1$ 赋予轻量判别分数 $s_1(c)$；若可用，则补充 $V_2$ 的过程分数 $s_2(c)$。频率、评审分数与候选长度、重复信号、是否达到 token 上限等历史特征共同构成后续决策依据。

<div class="method-step__io" markdown="1">

**输入**：当前候选集合 $C$、答案频率验证器 $V_0$、轻量评审器 $V_1$，以及可选过程验证器 $V_2$。<br>
**输出**：每个候选的廉价验证证据、当前答案一致性和不确定性特征。

</div>

**直观理解**：先用便宜的检查同时查看所有答案：既看多少候选给出同一答案，也看轻量模型是否认为这些解答可靠。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自适应扩展或早停

当 $|C|<N_{\max}$ 且 $b>0$ 时，若最高频答案的占比至少为 $0.6$ 且其轻量分数满足 $s_1\geq0.7$，则停止扩展；否则再生成一个候选，并仅以 $V_0$、$V_1$ 为其打分。三种变体分别设定 $N_{\max}=2,4,8$，以产生不同成本与精度位置。

<div class="method-step__io" markdown="1">

**输入**：候选数 $|C|$、最大候选数 $N_{\max}$、剩余预算 $b$、答案一致性、分数差距和轻量分数。<br>
**输出**：已满足稳定条件的候选池，或扩展至上限前尽可能降低不确定性的候选池。

</div>

**直观理解**：答案已高度一致且便宜评审也有把握时，系统不再花钱；只有现有证据仍不足以决定时，才多生成一个解答。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 选择性强验证

仅将排名前 $K$ 个候选送入 $V_3$，得到深度验证分数 $s_3(c)$；CoBa-Routed-Light、CoBa-Routed、CoBa-Routed-Strong 分别使用 $K=0,2,4$。未被路由的候选不会因缺少 $s_3(c)$ 而被人为扣分。

<div class="method-step__io" markdown="1">

**输入**：按答案频率与轻量分数排序的候选、强验证器 $V_3$ 与强路由数量 $K$。<br>
**输出**：少数关键候选的强验证证据，以及保留原有廉价证据的完整候选集。

</div>

**直观理解**：昂贵评审器不批改所有答案，而是只仔细审查最可能成为最终答案的少数解答。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 预算约束下的计算分配目标

$$
\max_{\pi}\;\mathbb{E}_{x\sim\mathcal{D}}\left[\mathbf{1}\{\hat{y}_{\pi}(x)=y\}-\lambda\frac{C_{\pi}(x)}{B}\right]
$$

**符号说明**

- $\pi(a_t\mid s_t)$：在状态 $s_t$ 下选择动作 $a_t$ 的路由策略。
- $\mathcal{D}$：由问题与标签对组成的评估集。
- $x$：推理时可观测的问题输入。
- $y$：仅在离线评估时用于判断正确性的真实答案。
- $\hat{y}_{\pi}(x)$：策略 $\pi$ 停止后为问题 $x$ 选择的最终答案。
- $C_{\pi}(x)$：策略 $\pi$ 在问题 $x$ 上实际消耗的计算成本。
- $B$：预先给定的推理预算。
- $\lambda$：成本敏感系数，用于权衡答对收益与计算开销。
- $\mathbf{1}\{\hat{y}_{\pi}(x)=y\}$：当最终答案正确时取 $1$，否则取 $0$ 的指示函数。

<div class="equation-explanation" markdown="1">

**直观理解**：目标奖励答对，同时惩罚相对预算 $B$ 的成本。它说明论文关心的不是单独最大化准确率，而是在有限资源下让每一步计算带来更高的预期决策价值；原文实验通过固定回放策略报告准确率-成本 Pareto 前沿，而非直接数值求解此目标。<br>
**原文位置**：第 3 节 Problem Formulation，式 (5)

</div>

</div>

<div class="equation-block" markdown="1">

#### 候选证据融合排序分数

$$
R(c)=0.20\,f(c)+0.30\,s_{1}(c)+0.15\,s_{2}(c)+0.45\,s_{3}(c)
$$

**符号说明**

- $R(c)$：候选 $c$ 的最终排序分数。
- $c$：包含推理轨迹与抽取答案的候选解答。
- $f(c)$：候选 $c$ 所对应最终答案的归一化出现频率。
- $s_1(c)$：Qwen3-8B 轻量评审器对候选 $c$ 给出的分数。
- $s_2(c)$：可选过程验证器对候选 $c$ 给出的分数。
- $s_3(c)$：Qwen3-14B 深度验证器对候选 $c$ 给出的分数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把多数一致性与逐级验证证据加权合并，其中最昂贵的深度验证权重最高，但只提供给被路由的少数候选。原文规定当 $s_2(c)$ 缺失时重新归一化剩余权重；未路由候选也不会从不存在的 $s_3(c)$ 获得虚假的支持或惩罚。<br>
**原文位置**：第 4 节 CoBa Routing，式 (6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：主方法不以端到端训练的方式优化路由器。概念性优化目标是式 (5) 的正确性-成本效用；实际实验采用在最终汇总前设定的固定路由规格，并在共享离线候选池上回放。原文还报告 learned MLP controller 在最终 leave-one-dataset-out 设置中退化为近似贪心策略，因此其结果不构成一个可替代固定 CoBa 规则的有效训练方案。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 计算均衡路由策略**

系统状态为 $s_t=(C_t,S_t,B_t,H_t)$：$C_t$ 为候选集合，$S_t$ 为已观测验证分数，$B_t$ 为剩余预算，$H_t$ 为答案多样性、候选长度、答案翻转和 token 截断等历史特征。动作集合为 $\mathcal A=\{\mathrm{SAMPLE},\mathrm{VERIFY}_1,\ldots,\mathrm{VERIFY}_L,\mathrm{STOP}\}$，原文在实验中以固定的回放路由规则实例化该思想，而非部署一个最终训练成功的控制器。

> 直观理解：它把推理过程视为持续做资源决策：该继续想一个新答案、核查已有答案，还是立即交卷。

**2. 分级验证器栈**

$V_0$ 是基于最终答案出现频率的规则验证器，$V_1$ 是对全部候选运行的 Qwen3-8B 轻量评审器，$V_2$ 是可选过程验证器，$V_3$ 是仅评估路由候选的 Qwen3-14B 深度验证器。该层级把候选覆盖范围与单次验证强度分离：前者由廉价验证保障，后者仅在候选竞争仍明显时提升。

> 直观理解：先普查、后复核：快速检查覆盖全部候选，耗费较高的深入检查只处理少数难以判断的候选。

**3. 共享候选池离线回放**

对每个数据集、生成器和 token 预算，原文先离线生成每题 $N=16$ 个候选；不同方法只能从同一候选池选择前缀、子集或验证动作。候选正确性仅供显式标注的 pool oracle 上界与最终评估使用，因此 CoBa 的运行特征不含 oracle 正确性标签。

> 直观理解：所有比较方法面对同一批已有答案，因而分数差异主要反映“如何分配生成和验证计算”，而不是某方法碰巧生成了更容易答对的题解。

**训练与推理**

离线阶段，针对每个数据集、生成器和 token 预算预生成 $16$ 个候选，并缓存可供回放的候选与验证特征；真实正确性标签被保留给评估及 pool oracle。推理回放阶段，CoBa 先采样两个候选，遍历运行 $V_0$ 与 $V_1$，按稳定条件决定是否逐个扩展候选，随后将频率和轻量分数领先的前 $K$ 个候选交给 $V_3$，最后用 $R(c)$ 选择答案。严格说，该协议近似需要交互式中途续写的方法，论文也将 s1 budget-forcing、uncertainty-allocation、evolving-ICL 和 self-evaluation weighted-voting 的相应比较标为 replay 或 proxy 变体。

**复现信息**

公平解释结果所需的固定设置为：初始预热 $k=2$；CoBa-Routed-Light、CoBa-Routed、CoBa-Routed-Strong 的 $N_{\max}$ 分别为 $2$、$4$、$8$，强验证路由数 $K$ 分别为 $0$、$2$、$4$；早停阈值为最高答案占比至少 $0.6$ 且 $s_1\geq0.7$。成本同时按总 token $C_{\mathrm{tok}}=\sum_m(T^m_{\mathrm{in}}+T^m_{\mathrm{out}})$ 和参数加权 token $C_{\mathrm{ptok}}=\sum_mP_m(T^m_{\mathrm{in}}+T^m_{\mathrm{out}})$ 计量，其中 $P_m$ 是模型 $m$ 以十亿计的参数量；后者用于近似大模型处理同一 token 更昂贵的事实。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MATH-500：数学推理基准；与 AIME 2024、AIME 2025、AMC 2023 共同用于检验竞赛数学题上的答案选择与计算分配。
- AIME 2024、AIME 2025、AMC 2023：竞赛数学测试集。其中 AIME 2025 被附录指出是路由策略剩余差距最大的任务组，因而用于观察困难数学题上的改进空间。
- Reasoning Gym hard subset：程序化符号推理的高难子集，用于检验方法是否不仅适用于传统竞赛数学。五个测试集总计含 $1{,}043$ 个唯一题目，并形成 $3{,}129$ 个“题目-生成器”评测单元。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

经增强答案抽取与任务特定规范化后的最终答案正确率；主表对 $15$ 个数据集-生成器组合取宏平均。 （越高越好，因为它直接衡量最终作答正确性。）

</div>
<div class="metric-item" markdown="1">

**平均参数加权 token 数**

将不同参数规模模型实际处理的 token 按模型参数规模加权后的每题计算成本，用以同时计入生成器和不同层级验证器的成本。 （越低越好，因为在相近准确率下它表示所需模型计算更少。）

</div>
<div class="metric-item" markdown="1">

**平均总 token 数**

每题生成与核验过程消耗的 token 总量；论文还记录模型调用次数和实测延迟，但此处优先保留两种最直接的成本口径。 （越低越好，因为它反映推理文本与核验处理的总体开销。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨 $15$ 个数据集-生成器组合的宏平均；CoBa-Routed-Strong 对比 self-evaluation weighted-voting proxy。

<div class="result-value" markdown="1">

CoBa-Routed-Strong 的准确率为 $85.13\%$，平均总 token 为 $5.80\times10^{4}$，平均参数加权 token 为 $6.30\times10^{5}$；self-evaluation weighted-voting proxy 的准确率为 $85.20\%$，但 CoBa 的参数加权 token 少 $49.1\%$。

</div>

作者将两者称为统计上可比，说明在该离线共享候选池协议下，分层路由强验证可以以接近的最终准确率替代普遍的自评加权投票，并显著降低按模型规模计的计算成本。这不证明两种方法绝对等效：文段没有给出该比较的置信区间、显著性数值或逐数据集稳定性。

<div class="result-source" markdown="1">

来源：Section 5, Main Accuracy-Cost Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This is statistically comparable to the self-evaluation weighted-voting proxy, which obtains 85.20%, but CoBa-Routed-Strong uses 49.1% fewer parameter-weighted tokens.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨 $15$ 个数据集-生成器组合的宏平均；CoBa-Routed-Strong 对比 best-of-16 majority voting。

<div class="result-value" markdown="1">

CoBa-Routed-Strong 与 best-of-16 majority voting 的宏平均准确率差距在 $0.01$ 个百分点以内，同时参数加权 token 减少 $58.9\%$。

</div>

该结果直接检验“把更多计算用于生成 $16$ 条解并投票”这一常见扩展路线。结果支持作者的资源分配判断：当候选证据相同，先广泛轻核验、再将强核验集中给关键候选，能以远低的参数加权成本接近高采样投票。不过摘要同时说明配对检验中 best-of-16 仍有小幅优势，因此不能解读为 CoBa 在准确率上严格超过 best-of-16。

<div class="result-source" markdown="1">

来源：Section 5, Main Accuracy-Cost Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

CoBa-Routed-Strong also matches best-of-16 majority voting within 0.01 macro-accuracy points while reducing parameter-weighted tokens by 58.9%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### CoBa 相对单样本解码的配对 bootstrap 比较，以及与 pool oracle 的差距。

<div class="result-value" markdown="1">

作者报告 CoBa 相对 single-sample decoding 存在显著增益；同时，CoBa 与 pool oracle 之间仍有差距。

</div>

前半部分说明在相同题目和共享候选证据上，CoBa 的决策改进并非仅由题目难度构成的偶然平均差异所致。后半部分表明候选池中已有的正确答案尚未总能被路由与验证识别出来，未来提升重点是改善不确定性判断、候选排序或强验证器的调用策略，而不是仅盲目扩大候选数。该摘录未报告这两项差距的具体百分点，不能量化其实际幅度。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Paired bootstrap tests show significant gains over single-sample decoding, while the remaining gap to the pool oracle exposes headroom for sharper routing.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主要结果依赖离线生成的共享 $N=16$ 候选池，且 greedy、fixed-long 与自适应方法均从该池回放；该协议严谨隔离了分配策略，但不能直接代表允许在线续写、重新采样或动态改变生成长度时的端到端表现。
- 过程验证器 $V_2$ 的解析分数在最终运行中稀疏，主比较因而集中于结果验证；同时多项近期方法仅以本地代理实现，论文不能据此声称精确复现了需要专用检查点、私有 API 或任务特定训练的原方法。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Greedy single-sample decoding / fixed-long：直接取共享候选池中的第一个候选，是不进行多候选聚合或额外核验的低计算基线；最终回放中两者等价。
- Best-of-$N$ majority voting / self-consistency：对前 $N\in\{2,4,8,16\}$ 个候选按规范化最终答案投票，检验仅增加生成样本并依赖答案一致性能达到的效果；最终回放中 self-consistency 与多数投票相同。
- Self-evaluation weighted voting proxy：用本地结果判别器分数和答案频率对生成器候选答案加权，代表“对候选普遍做较强自评后再聚合”的推理时模式；作者明确将其称为代理实现，而非完整复现经强化学习训练的验证器。
- Pool oracle：若离线候选池中存在正确解即选择它，使用评测端正确性信息；它不可部署，只用于估计既定 $N=16$ 候选池中尚未被路由策略利用的上限。

**实验想回答的问题**

- 在固定推理预算下，CoBa 将计算分配给候选解生成、轻量核验与强核验，能否比单样本解码及高采样投票取得更好的准确率-成本折中？
- 当所有方法共享同一批已生成候选解时，CoBa 的收益是否来自更有效的核验路由与选择，而非获得了更有利的生成证据？

**实验实现**

评测使用 Qwen3-14B、Phi-4-reasoning 和 Qwen3-8B 作为生成器；Qwen3-8B 还充当轻量二元结果判别器，Qwen3-14B 充当强结果验证器。对每个数据集-生成器组合，先以温度 $0.6$、top-$p=0.95$ 生成共享的 $N=16$ 个候选，每个候选最大输出预算为 $16{,}384$ token；所有回放方法只能在同一候选池或其前缀/子集中作决策。因此，比较主要测量“如何检查和选择既有候选”，不能证明 CoBa 在在线生成时也会产生更好的候选。数学答案统一优先抽取 boxed 答案、显式最终答案和末尾符号表达式，并规范化分数、元组、$\pi$ 等形式。统计检验采用按题目配对的 bootstrap，重采样 $2{,}000$ 次；一条题目因配对覆盖不完整被排除，检验样本为 $1{,}042$ 题。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 附录的按数据集 Pareto 前沿图显示，路由策略在主要任务组上改善前沿，而 AIME 2025 的剩余差距最大。这是跨任务组的定性诊断，不是单个题目的案例，也未在所给摘录中报告具体数值；它提示高难竞赛题更可能暴露路由置信度或验证质量的不足。证据："Routed policies improve the frontier across the main task groups, with the largest remaining gap on AIME 2025."（Appendix B, Figure 5）

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It routes fixed test-time compute among candidate generation and verification for mathematical and symbolic LLM reasoning.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`0ab0a51ae18c431c34c6764e888e60fc9c55609c8a011f3742dd3e6acda69ab2`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
