---
title: "[论文解读] A Temporal Reasoning Benchmarking Framework for LRMs via Difficulty-controlled and Dynamic Test Generation"
description: "[arXiv 2607.04784][LLM 评测] 本文提出 TRACE 评测框架，通过动态生成、细粒度难度控制和推理轨迹验证，系统测试大型推理模型在时间推理任务中的真实能力边界。"
arxiv_id: "2607.04784"
announcement_date: "2026-08-18"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:13:21.337503+00:00"
source_sha256: "f6b58197b2bca44c6f0b1abe14be304200f21666f3663e04b5cf48490cb09d7f"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "大型推理模型"
  - "时间推理"
  - "Allen 区间代数"
  - "约束满足问题"
  - "动态合成评测"
  - "推理轨迹验证"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2607.04784</p>

# A Temporal Reasoning Benchmarking Framework for LRMs via Difficulty-controlled and Dynamic Test Generation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Shide Zhou, Kailong Wang, Ling Shi, Haoyu Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Huazhong University of Science and Technology , Wuhan , China；Huazhong University of Science and Technology；Affiliation: National University of Singapore , Singapore , Singapore；National University of Singapore；Affiliation: Nanyang Technological University , Singapore , Singapore；Nanyang Technological University；Affiliation: Huazhong University of Science and Technology；Affiliation: National University of Singapore；Affiliation: Nanyang Technological University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.04784) · [PDF 下载](https://arxiv.org/pdf/2607.04784) · **关键词** 大型推理模型, 时间推理, Allen 区间代数, 约束满足问题, 动态合成评测, 推理轨迹验证<br>


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

本文提出 TRACE 评测框架，通过动态生成、细粒度难度控制和推理轨迹验证，系统测试大型推理模型在时间推理任务中的真实能力边界。

**不用术语来说**：现有时间推理测试往往使用固定题库，只检查模型最后答对还是答错，因此模型可能依靠记忆、模式匹配或猜测取得高分，却没有真正按照逻辑完成推理。研究需要一种能够持续生成新题、精确调节题目难度，并同时检查推理过程和最终答案的评测方法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 TRACE 框架：利用 Allen 区间代数和约束满足问题建模时间关系，通过动态构造约束图、控制事件数量与关系类型来调节逻辑复杂度，并验证模型推理轨迹是否符合约束网络的代数闭包。
- 基于 TRACE 构建 TRACEBench，包含 1,200 个覆盖六个难度等级的合成实例，并据此揭示不同规模大型推理模型的失效模式，包括中型模型的无效推理猜中答案、小型模型的退化循环，以及高级模型的推理爆炸。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大型推理模型（Large Reasoning Models, LRMs）的时间推理评测。时间推理要求模型根据事件之间的先后、相遇、重叠、包含等关系，经过多步逻辑演绎判断未直接给出的关系；因此，最终答案正确并不必然意味着推理过程有效。本文将时间推理任务表示为基于 Allen 区间代数的约束满足问题，并关注三个评测要求：动态生成数据以降低训练数据污染和记忆的影响，精细控制逻辑难度以定位模型能力边界，以及同时验证推理轨迹和最终答案以检测表面猜测。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大型推理模型（LRM）**

LRM 是在测试时投入更多计算、生成较长中间思考过程后再给出结论的语言模型。中间轨迹用于展开问题求解步骤，但轨迹看似合理并不自动保证每一步都符合逻辑。

</div>
<div class="concept-item" markdown="1">

**Allen 区间代数**

Allen 区间代数把事件表示为具有起点和终点的时间区间，并用 13 种互斥的基本关系描述两个区间的相对位置，例如 before、overlaps 和 during。关系可以通过复合规则进行推导，因此适合检验多步时间逻辑。

</div>
<div class="concept-item" markdown="1">

**约束满足问题（CSP）与路径一致性**

CSP 用变量、取值和约束描述一个必须同时满足的逻辑问题；本文中变量是事件区间，约束是区间之间的时间关系。路径一致性要求直接关系与经过中间事件推导出的关系不矛盾，从而排除无法成立的时间场景。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一组事件及其时间区间关系，系统首先将每个事件表示为一个节点，将已知的时间关系表示为有向约束边，并构造满足路径一致性的约束图。任务构造器把图中的显式边转换为自然语言前提，再选择图中可由多步约束推导出的隐式边作为问题；模型的输入是自然语言时间场景和问题，输出应包含推理轨迹以及最终的关系标签。评测假设关系属于 Allen 区间代数规定的 13 种基本关系，生成的网络具有一致的时间解释；同时限制使用外部求解器，以测量模型本身的演绎能力，而非工具调用能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$X=[X_s,X_e]$**

事件或时间区间 $X$，其中 $X_s$ 和 $X_e$ 分别表示起点与终点，并满足 $X_s<X_e$。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{R}_{Allen}$**

Allen 区间代数的 13 种基本时间关系构成的集合，包括具有逆关系的非对称关系以及 equals 对称关系。

</div>
<div class="notation-item" markdown="1">

**$X\xrightarrow{r_1}Y$**

事件区间 $X$ 与 $Y$ 之间存在关系 $r_1$，其中 $r_1\in\mathcal{R}_{Allen}$。

</div>
<div class="notation-item" markdown="1">

**$r_1\circ r_2$**

关系复合：若 $X$ 与 $Y$ 的关系为 $r_1$、$Y$ 与 $Z$ 的关系为 $r_2$，则 $X$ 与 $Z$ 的可能关系由 $r_1\circ r_2\subseteq\mathcal{R}_{Allen}$ 约束。

</div>

</div>

**直接相关的工作**

- **TRAM 与 TimeBench**: 二者主要依赖静态数据集或数据集聚合来评测时间推理。本文认为静态语料容易产生数据污染和记忆问题，因此进一步引入动态合成任务；同时，本文还补充了对推理轨迹和最终答案的双重验证。
- **Test of Time 与 t-BEN**: 二者使用合成机制降低静态数据污染风险，代表时间推理评测向动态生成的发展方向。但原文指出，这类方法通常采用较粗粒度的难度代理，难以精确控制逻辑复杂度和定位模型的具体失效边界；本文据此提出基于约束图的细粒度难度控制。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大型推理模型被用于复杂问题求解后，评测重点已从表面上的答案准确率转向其是否具备稳定、可解释且可复核的演绎能力。时间推理尤其适合作为检验对象，因为任务要求模型严格维护事件之间的先后、包含或重叠关系，近似检索或模糊语义匹配通常不足以保证正确。若评测不能区分真实推理和偶然答对，研究者就难以判断模型在何种复杂度下开始失效，也无法可靠地比较不同模型的推理能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **静态题库型基准，如 TRAM 和 TimeBench**：这类方法从已有数据中整理固定的时间推理样本，模型在预先确定的题目上作答，通常依据最终答案是否正确来衡量性能。
- **合成数据型基准，如 Test of Time 和 t-BEN**：这类方法通过规则或程序生成新的时间推理题目，以减少固定题库带来的记忆和数据污染问题，但主要通过较粗的难度代理变量组织测试样本。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 静态题库容易产生数据污染和记忆效应，模型可能复现训练中见过的题目或利用表面模式，而不是重新进行演绎；这会使最终准确率高估模型的真实推理能力。
- 现有合成基准的难度控制通常较粗，无法精确规定约束图中的逻辑复杂度，因此难以定位模型能力的具体崩溃边界；同时，单纯检查最终答案会遗漏无效推理后偶然答对的情况，无法判断推理轨迹是否忠实。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未同时解决三个相互关联的问题：持续生成不易被记忆的新任务、以细粒度方式控制时间约束的逻辑复杂度，以及独立验证中间推理步骤和最终结论。缺少这种统一框架，评测结果就难以回答模型究竟能处理多复杂的时间关系，以及正确答案是否确实由有效推理得到。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一个基于时间关系约束的动态评测框架，使任务难度可以被精确调节，并通过推理轨迹与最终答案的双重验证，可靠测量大型推理模型的真实时间演绎能力和失效边界？

</div>
<div markdown="1"><span>作者直觉</span>

如果把时间推理题表示为由事件和关系组成的约束图，就可以直接控制图的规模及关系组合，从而逐步增加模型必须维护的逻辑依赖；把图中显式给出的关系作为前提、把隐含可推出的关系作为问题，则能确保题目需要实际推理而非简单复述。进一步地，利用约束网络能够推出的全部关系作为检查依据，可以逐步核对模型的推理轨迹和结论：即使模型最后答对，任何不符合约束闭包的步骤仍会被识别出来。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TRACE 是一个面向大型推理模型（LRM）的动态时序推理测试框架。其输入是用户指定的目标难度 $\mathcal{D}_{\mathrm{tar}}$，核心中间表示是 Allen 区间代数约束图 $\mathcal{G}=(V,E)$：顶点表示具有起止点的事件，边表示两个事件之间显式给出的时序关系。框架先把目标难度转换为事件数、显式约束数和关系类型多重集，再构造连通、路径一致且与历史样本非同构的具体图；随后将图中的显式边改写为自然语言事实，通过约束传播找出未直接给出但可唯一推导的关系，并据此生成二元问题及标准答案。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 目标难度建模与候选配置生成

TRACE 用事件规模项 $|V|^{\alpha}$ 与平均关系权重 $\overline{w}$ 的乘积定义难度，并反解事件数 $n$；随后围绕密度决定约束数 $m$，按与目标平均权重的距离采样关系多重集 $\mathcal{L}$，再以贪心替换将相对误差压到容差内。

<div class="method-step__io" markdown="1">

**输入**：目标难度 $\mathcal{D}_{\mathrm{tar}}$、13 种 Allen 关系及其权重 $w(r)$、尺度指数 $\alpha$、图密度 $\rho$、采样宽度 $\sigma$、容差 $\tau$ 等生成参数。<br>
**输出**：候选配置 $(n,m,\mathcal{L})$，分别规定事件数量、显式约束数量以及待嵌入图中的 Allen 关系组成。

</div>

**直观理解**：这一步类似先按试卷目标难度决定“题目涉及多少对象”和“每条条件有多复杂”，而不是先随机出题再事后贴难度标签。贪心校准确保有限次随机采样没有让实际关系复杂度明显偏离目标。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 路径一致约束图构造与去重

算法先由随机 Prüfer 序列生成含 $n-1$ 条边的生成树，并将一部分关系放到树骨架上；其余关系优先加入端点度数和 $k(u,v)=\deg(u)+\deg(v)$ 较小的未连接事件对，每次加入前调用一致性检查，最后计算规范哈希并过滤同构重复图。

<div class="method-step__io" markdown="1">

**输入**：候选配置 $(n,m,\mathcal{L})$ 以及已生成图的规范签名集合 $\Sigma$。<br>
**输出**：满足约束、连通且结构未重复的时序约束图 $\mathcal{G}=(V,E)$ 及其规范签名 $\mathcal{S}$；失败的随机尝试被丢弃并重新生成。

</div>

**直观理解**：生成树先保证所有事件都在同一条推理网络中；之后逐条加边并即时检查，作用类似搭积木时每放一块就确认整体没有矛盾。优先连接度数较低的节点可避免少数事件承载绝大多数条件，规范哈希则防止只更换事件名称却重复同一种题型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 隐式事实提取与问答构造

TRACE 将显式边映射为自然语言事实集 $\mathcal{F}$，再执行路径一致性传播，计算每个事件对的可行关系集合 $\mathcal{R}_{\mathrm{inferred}}(u,v)$；仅保留不在 $E$ 中且满足 $|\mathcal{R}_{\mathrm{inferred}}(u,v)|=1$ 的事件对，并为每种 Allen 关系生成 YES/NO 验证问题。

<div class="method-step__io" markdown="1">

**输入**：有效约束图 $\mathcal{G}=(V,E)$，其中 $E$ 只包含将在题面中出现的显式关系。<br>
**输出**：逻辑任务 $\mathcal{T}=(\mathcal{F},\mathcal{Q},\mathcal{A})$，其中 $\mathcal{F}$ 是共享前提，$\mathcal{Q}$ 是候选问题集合，$\mathcal{A}$ 是由约束传播确定的标准答案。

</div>

**直观理解**：问题刻意询问题面没有直接写出的关系，因此模型不能靠查找原句作答；只选择唯一可确定的关系，又避免了题目本身存在多个合法答案。对同一隐式事实枚举关系类型，可以同时构造一个肯定问题和若干否定问题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 模板化执行与推理轨迹验证

模板要求被测 LRM 在不访问外部工具或求解器的条件下，以 JSON 同时返回逐步的 "reasoning" 和 "final_answer"；随后 TRACE 从响应中抽取推理轨迹，并调用约束求解器逐步核验其逻辑正确性。

<div class="method-step__io" markdown="1">

**输入**：自然语言事实、Allen 关系的正式定义、目标问题、结构化输出说明和格式示例。<br>
**输出**：模型最终答案、可解析的形式化推理轨迹，以及用于区分有效推导与偶然猜测的轨迹验证结果。

</div>

**直观理解**：只检查最终 YES/NO 无法判断模型是推出来的还是猜中的，因此框架要求模型交出中间步骤，再让独立求解器逐步验算。所给节选只概述了验证器的职责，未包含第 3.4 节的完整抽取规则和判定算法。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 时序约束图难度函数

$$
\mathcal{D}(\mathcal{G})=|V|^{\alpha}\cdot\left(\frac{1}{|E|}\sum_{(v_i,v_j)\in E}w(r_{ij})\right)=|V|^{\alpha}\overline{w}
$$

**符号说明**

- $\mathcal{G}=(V,E)$：时序约束图；顶点集合表示事件，边集合表示题面明确给出的时序约束。
- $V$：事件集合，事件数为其基数。
- $E$：显式约束边集合，不包含需要模型推导的隐式关系。
- $r_{ij}$：事件 $v_i$ 与 $v_j$ 之间显式边所标注的 Allen 时序关系。
- $w(r_{ij})$：关系 $r_{ij}$ 的标量复杂度权重，用于近似该关系带来的推理负担。
- $\overline{w}$：图中全部显式约束的平均关系权重。
- $\alpha$：事件规模对难度的放大指数；作者以参考任务校准为约 $1.75$。
- $\mathcal{D}(\mathcal{G})$：图 $\mathcal{G}$ 的总体目标难度分数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把难度视为“要同时处理多少事件”与“平均每条约束多难”的乘积。规模项采用幂函数，使增加事件带来的上下文长度、候选排列和推理链负担能够超线性增长；平均权重则让事件数相同但关系类型不同的图具有不同难度。需要注意，边数 $|E|$ 只通过平均权重进入该核心分数，边密度另由生成算法控制，因此该分数并未直接把更多显式边单调解释为更难。<br>
**原文位置**：第 3.2.1 节，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 目标关系复杂度的偏置采样分布

$$
\overline{w}_{\mathrm{tar}}=\frac{\mathcal{D}_{\mathrm{tar}}}{n^{\alpha}},\qquad p(r)=\frac{\exp\left(-\frac{(w(r)-\overline{w}_{\mathrm{tar}})^2}{2\sigma^2}\right)}{\sum_{r'\in\mathcal{R}_{\mathrm{Allen}}}\exp\left(-\frac{(w(r')-\overline{w}_{\mathrm{tar}})^2}{2\sigma^2}\right)}
$$

**符号说明**

- $\mathcal{D}_{\mathrm{tar}}$：用户指定的目标难度。
- $n$：候选任务中的事件数量。
- $\overline{w}_{\mathrm{tar}}$：在事件规模 $n$ 固定后，为达到目标难度所需的平均关系权重。
- $\mathcal{R}_{\mathrm{Allen}}$：可采样的 Allen 区间关系集合。
- $p(r)$：关系 $r$ 被抽入候选多重集 $\mathcal{L}$ 的归一化概率。
- $w(r)$：关系 $r$ 的预设复杂度权重。
- $\sigma$：高斯形 softmax 的宽度参数；越小越集中选择权重接近目标均值的关系。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分先扣除事件规模造成的难度，算出每条关系平均应有多复杂；第二部分让权重更接近这一目标的关系获得更高采样概率。随机采样保留了题型多样性，而后续相对误差检查与贪心替换负责纠正小样本波动；此处将原文公式 (8) 的正比形式忠实写成了等价的归一化概率形式。<br>
**原文位置**：第 3.2.2 节，公式 (7) 与公式 (8)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。TRACE 是测试生成与验证框架，不训练或微调被测 LRM，也没有通过梯度下降优化的损失函数；难度函数用于配置和筛选测试图，约束求解器用于生成标准答案与验证轨迹，二者都不是模型训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 难度感知约束图生成器**

该模块把难度拆成事件规模与单边关系复杂度两个维度。关系权重按约束对端点自由度和边界精度的影响分层：equals 为 $0.8$，before/after 为 $1.0$，meets/met-by 为 $1.1$，starts/finishes 为 $1.5$，overlaps/during 等多重不等式关系为 $2.0$；逆关系共享权重。尺度指数通过三事件、两显式关系、推断第三关系的参考任务校准：令其难度为 $10$，并使用平均关系权重约 $1.46$，得到 $\alpha\approx1.75$。候选图并非直接随机连边，而是经过规模估计、关系偏置采样、平均权重校准、生成树初始化、逐边一致性检查和同构消除。

> 直观理解：事件越多，模型需要同时维护的时间对象和可能排列越多；关系越复杂，需要联立处理的端点等式或不等式也越多。该模块分别控制这两类负担，使“难度 80”对应可复现的结构参数，而不只是作者对题目的主观分级；不过这些关系权重属于作者基于推理状态空间作出的建模选择，并非由所给章节中的人类认知实验直接测得。

**2. 时序推理任务构造器**

该模块将符号边 $(u,v,r)$ 通过预定义词典映射成自然语言事实，并在完整约束网络上执行路径一致性传播。显式边被排除在问题候选之外，且只有传播后关系集合收缩为单元素的事件对才会进入问题集；对唯一真关系 $r_{\mathrm{true}}$，候选关系 $r_k$ 与其相同则标签为 YES，否则为 NO。提示模板同时提供 13 种 Allen 区间关系定义，以减少模型因关系名称歧义而产生的错误。

> 直观理解：图是机器可验证的“题目底稿”，自然语言只是它的表述层。先用符号系统算出唯一答案，再生成文字题，可以避免人工写题时漏条件、答案不唯一或标签错误；同时，排除显式关系保证测试对象确实是演绎能力。

**3. 基于轨迹的验证器**

被测模型必须输出结构化推理过程和最终答案，验证器解析其中的推理步骤，并借助约束求解器检查每一步是否由给定事实和合法时序推导支持。该设计将最终答案正确性与推理忠实性分开：答案正确但中间步骤不成立时，不应被视为可靠推理。所给材料未包含第 3.4 节正文，因此轨迹的精确语法、逐步验证准则、失败类型及聚合评分方式原文未明确报告。

> 直观理解：它相当于不仅核对选择题答案，还检查草稿中的每一步是否成立，从而发现“过程错误但碰巧答对”的情况。由于关键实现细节不在节选中，对验证覆盖范围不能作超出原文的推断。

**训练与推理**

不存在训练阶段。离线生成时，用户给定 $\mathcal{D}_{\mathrm{tar}}$，系统估计 $n$ 和 $m$，采样并校准关系多重集 $\mathcal{L}$，反复尝试构造满足路径一致性的图，过滤规范签名已存在的同构结构，再传播约束以获得唯一可判定的隐式关系，最终生成事实、问题与标签。在线评测时，目标 LRM 独立读取包含 Allen 关系定义、事实和问题的模板化提示，不得调用外部工具或求解器，并输出含 "reasoning" 与 "final_answer" 的 JSON；TRACE 解析输出，由约束求解器核验推理步骤及答案。作者将这种设置解释为对模型内部纯推理能力和推理忠实性的隔离测试，但所给节选未提供验证器的完整算法，因而无法确认其对自然语言改写、遗漏步骤或等价证明路径的具体处理方式。

**复现信息**

复现难度生成器时必须保留三项关键设计。第一，关系权重按 Allen 关系的端点约束复杂度分层，逆关系共享权重，且作者以 $\mathcal{D}_{\mathrm{ref}}=10$ 的三事件原子传递任务和 $\overline{w}\approx1.46$ 校准出 $\alpha\approx1.75$。第二，显式边数围绕 $m_{\mathrm{exp}}=\mathrm{round}(\rho\binom{n}{2})$ 采样，下界至少为 $n-1$ 以促进连通，上界至多为 $\binom{n}{2}-1$ 以保留隐式推断空间；精确的 $\rho$、$\Delta$、$\sigma$、$\tau$ 和最大调整次数在所给节选中原文未明确报告。第三，图生成允许失败重试且可离线并行：原文举例称在 Difficulty 80 生成 40 个有效图约需 800 次尝试，这说明高难度配置的可满足率会下降，但该数字是生成成本示例，不是模型性能结果。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- TRACEBench：由TRACE动态生成的时序推理基准。目标难度为$\mathcal{D}_{\mathrm{tar}}\in\{10,45,80,115,150,185\}$；每个难度生成40个不同的约束图并从中采样200道题，共1,200个测试样本。所有难度固定约束密度$\rho=0.5$，难度对齐容差为$\tau=0.1$。它同时用于检验难度控制、比较模型能力、衡量伪猜测，以及诊断复杂推理中的故障类型；原文未说明训练集、验证集或额外测试划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**真实推理准确率（True Reasoning Accuracy）**

最终标签正确且推理轨迹通过有效性检查的样本比例，用来衡量模型是否真正完成了时序推导，而不只是碰巧猜中答案。 （越高越好，因为它同时要求答案正确和推理过程有效。）

</div>
<div class="metric-item" markdown="1">

**伪猜测率（Spurious Guessing Rate）**

最终标签正确、但没有提供有效推理轨迹的样本比例；它刻画只看答案正确率时可能被误计为成功的部分。 （越低越好，因为较低值表示正确答案更可能建立在有效逻辑推导之上。）

</div>
<div class="metric-item" markdown="1">

**难度与真实推理准确率的Pearson相关系数$r$**

衡量理论难度分数上升与模型真实推理准确率变化之间的线性关系，用于验证难度指标是否对应实际推理负荷。 （在本文验证目标下，越接近$-1$越好，因为这表示难度越高，模型性能越稳定地下降；但它只验证相对排序关系，并不证明难度分数具有绝对心理或计算复杂度含义。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RQ1：六个目标难度层级上的生成控制与难度有效性

<div class="result-value" markdown="1">

生成图的平均达成难度从目标$10$时的$9.36$变化到目标$185$时的$185.40$；随难度提高，各模型真实推理准确率与难度的Pearson相关系数介于$-0.85$和$-0.99$之间，平均为$-0.96$。例如Qwen-32B从$67.50\%$降至$29.50\%$，GPT-5-mini从$93.50\%$降至$72.50\%$。

</div>

作者据此主张TRACE既能在结构层面对齐指定难度，也能产生模型可感知的性能梯度。直观地说，生成器要求更难时，图更大、约束更多，而且所有受测模型都更容易失败。不过，相关性只能说明该分数适合作为这组生成题中的相对难度指标；它不能证明不同难度差值等距，也不能排除图规模增长、提示长度增长等共同因素对性能的影响。

<div class="result-source" markdown="1">

来源：第4.2节，Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The Pearson correlation coefficients further quantify this trend, ranging from -0.85 to -0.99 across all models, with an average of -0.96.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### RQ2：参数规模、基础架构与先进模型的能力边界

<div class="result-value" markdown="1">

DeepSeek-R1-Distill-Qwen-32B、14B和7B在六个难度上的平均真实推理准确率分别为$45.42\%$、$41.08\%$和$17.42\%$，显示同一Qwen系列中较大模型总体更强；先进模型Claude-Sonnet-4.6、DeepSeek-R1和GPT-5-mini的平均值分别达到$83.00\%$、$80.50\%$和$79.83\%$。在难度$185$时，Claude-Sonnet-4.6、GPT-5-mini和DeepSeek-R1分别为$75.50\%$、$72.50\%$和$60.50\%$。

</div>

结果表明扩大参数规模通常改善真实推理能力，但收益并非只由规模决定：Llama-8B在难度升高后逐渐接近更大的Qwen-14B，说明基础架构也影响退化速度。先进模型明显领先，却仍在最高难度下降，因此TRACEBench没有在当前模型上完全饱和。由于这些模型的训练数据、推理预算、API配置和上下文机制并未受控，该实验是综合系统比较，不能把模型间差异严格归因于参数量或某一架构组件。

<div class="result-source" markdown="1">

来源：第4.3节，Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Claude-Sonnet-4.6, DeepSeek-R1, and GPT-5-mini demonstrate exceptional capabilities with average True Reasoning Accuracies of 83.00%, 80.50%, and 79.83%, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### RQ3与RQ4：结果正确率的高估程度及逻辑故障构成

<div class="result-value" markdown="1">

Qwen-14B和Qwen-32B的平均伪猜测率分别为$28.00\%$和$26.00\%$，其中Qwen-14B在难度$150$达到$35.00\%$；相比之下，DeepSeek-R1、GPT-5-mini和Claude-Sonnet-4.6的平均值分别为$7.83\%$、$12.17\%$和$13.92\%$。自动分类还显示，直接推断错误在每个模型的逻辑错误中至少占$50\%$。

</div>

作者据此认为，只检查最终标签会把大量“答案碰巧正确但推理无效”的输出算作成功，尤其会高估中型蒸馏模型。失败分类进一步说明，主要瓶颈仍是错误应用传递性或时序约束，而非单纯的格式问题。这里的伪猜测率衡量的是论文验证器判定的轨迹无效，并不直接证明模型依赖了某一种统计捷径；逻辑故障比例也依赖作者自动分类脚本的规则，而节选未给出其独立验证结果。

<div class="result-source" markdown="1">

来源：第4.4节，Table 4；逻辑故障结论见第4.5.1节与Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

DeepSeek-R1-Distill-Qwen-14B and 32B exhibit consistently high spurious guessing rates, averaging 28.00% and 26.00% respectively across all difficulties.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评估仅使用TRACE生成的1,200道题，固定约束密度为$\rho=0.5$，且节选未报告在人工编写题、其他时序关系体系、不同密度或分布外图结构上的验证。因此，难度控制和模型排名能否推广到更广泛的真实时序推理场景仍不确定。
- 实验缺少重复运行、置信区间和统计显著性检验；部分API模型不能统一温度设置，模型之间的上下文窗口、隐藏推理机制和服务端配置也未完全受控。此外，逻辑故障自动分类脚本的精度与人工一致性未报告，因此细粒度故障比例仍需源代码或人工复核支持。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- DeepSeek-R1-Distill-Qwen系列（7B、14B、32B）：控制蒸馏来源与基础架构、改变参数规模，用于检验扩大模型是否提高时序推理能力和高难度鲁棒性。
- DeepSeek-R1-Distill-Llama-8B：与规模接近的Qwen-7B及更大的Qwen-14B比较，用于区分参数规模与基础架构带来的影响。
- Gemini-2.5-Flash与DeepSeek-R1：作为先进API模型，与本地部署的开放权重蒸馏模型比较；其中DeepSeek-R1还用于观察较强推理模型的推理忠实性及长推理输出限制。
- GPT-5-mini与Claude-Sonnet-4.6：作为论文设定中的高性能上界基线，用于衡量TRACEBench最困难层级是否仍能区分先进模型，并考察其指令遵循和输出可解析性。

**实验想回答的问题**

- TRACE能否生成结构难度与目标值严格对齐的时序推理题，并且该难度指标是否与不同大推理模型的实际性能下降一致？
- 不同参数规模与基础架构的模型在TRACEBench上表现如何，传统的只看最终答案是否正确的评估会在多大程度上高估真实推理能力，以及模型主要出现哪些逻辑或结构故障？

**实验实现**

共评估8个模型：本地部署DeepSeek-R1-Distill-Qwen-7B、14B、32B和DeepSeek-R1-Distill-Llama-8B，通过各自API评估Gemini-2.5-Flash、DeepSeek-R1、GPT-5-mini和Claude-Sonnet-4.6。所有模型最大生成长度设为8,192 tokens；支持温度参数的模型统一设为0，不支持者使用默认配置。评估先比较目标难度与实际生成图的节点数、边数和达成难度，再在六个难度层级上统计真实推理、伪猜测、答案错位、完全失败和解析失败。逻辑失败先经代表性样本人工检查归纳类别，随后作者编写自动化脚本对全部逻辑失败分类；但节选未报告人工抽样规模、分类器准确率、重复运行次数、置信区间或显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 在难度$115$的一条GPT-5-mini推理轨迹中，模型生成了未由题目定义的事件或关系，例如关系`less_than`。作者将其归为“复杂度下的幻觉”：模型输出形式近似结构化推理，却通过引入不存在的符号填补逻辑缺口。该案例说明仅检查JSON是否可解析仍不足以保证推理合法，还必须核对每个事件和关系是否来自题目定义；但单个案例不能确定此类错误的总体发生率或因果机制。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a dynamically generated, difficulty-controlled benchmark for evaluating temporal reasoning in language reasoning models.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`f6b58197b2bca44c6f0b1abe14be304200f21666f3663e04b5cf48490cb09d7f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
