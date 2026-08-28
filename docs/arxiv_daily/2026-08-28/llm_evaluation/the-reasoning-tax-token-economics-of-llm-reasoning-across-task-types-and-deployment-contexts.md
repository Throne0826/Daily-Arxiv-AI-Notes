---
title: "[论文解读] The Reasoning Tax: Token Economics of LLM Reasoning Across Task Types and Deployment Contexts"
description: "[arXiv 2608.26235][LLM 评测] 本文把推理型大语言模型的额外思考视为一项需要核算收益与成本的部署决策，并提出 Token Economy Score（TES）来衡量准确率增益是否足以补偿生成词元开销。"
arxiv_id: "2608.26235"
announcement_date: "2026-08-28"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:38:59.636285+00:00"
source_sha256: "d76fed7a206f8996d54f5a5fdfd245c330b553d432923753df526526af0e733d"
tags:
  - "LLM 评测"
  - "LLM 效率"
  - "LLM Reasoning"
  - "LLM 其他"
  - "推理型大语言模型"
  - "词元经济得分"
  - "边际推理效率"
  - "扩展思考"
  - "生成词元"
  - "推理成本占比"
  - "部署成本乘数"
  - "任务类型分层"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.26235</p>

# The Reasoning Tax: Token Economics of LLM Reasoning Across Task Types and Deployment Contexts

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Sachin Gopal Wani, Ajay Dholakia, David Ellison</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26235v1) · [PDF 下载](https://arxiv.org/pdf/2608.26235v1) · **关键词** 推理型大语言模型, 词元经济得分, 边际推理效率, 扩展思考, 生成词元, 推理成本占比, 部署成本乘数, 任务类型分层<br>


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

本文把推理型大语言模型的额外思考视为一项需要核算收益与成本的部署决策，并提出 Token Economy Score（TES）来衡量准确率增益是否足以补偿生成词元开销。

**不用术语来说**：推理模型通常会在给出答案前生成较长的内部思考过程，这可能提高正确率，也会增加延迟与推理费用。只看准确率排行榜无法判断这些额外计算是否值得：不同任务可能从长推理中获得截然不同的收益，而且继续提高推理强度还可能出现收益递减甚至准确率下降。因此，部署者需要一种能够同时反映质量改善与额外词元代价的比较方法。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出边际效率指标 TES：以推理模型相对非推理基线的准确率增益为收益，并用生成词元倍数进行归一化；同时区分具有推理开关时可直接配对的版本，以及缺少直接非推理对应模型时使用近似基线的版本。
- 将模型选择问题拆分为任务结构、推理强度与部署环境三个维度，考察何种任务值得启用推理、增加思考量是否仍有边际收益，以及本地部署等成本条件如何改变推理工作负载的经济可行性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

推理型大语言模型会在给出最终答案前生成较长的内部思考链，通常能改善数学、代码等多步任务的准确率，但也会显著增加生成词元数与推理成本。传统基准主要比较准确率，或用“准确率除以生成词元数”衡量绝对效率，难以回答部署中的边际决策：相对于非推理模式，额外思考究竟带来多少准确率增益，又需要付出多大的词元与经济成本。本文因此从任务类型、推理强度和部署环境三个维度考察推理是否值得启用，而不是把推理模式视为普遍有益的默认选项。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链推理**

模型在输出最终答案前生成若干中间推导步骤，以处理需要连续推断的问题。本文关注的“扩展思考”会产生更多生成词元，因此可能提高准确率，也可能造成过度推理。

</div>
<div class="concept-item" markdown="1">

**边际效率**

边际效率衡量从非推理基线切换到推理模式后，新增资源消耗换来了多少额外收益。它与单独评价某个模型的绝对准确率或单位词元准确率不同，直接服务于“是否启用推理”的部署决策。

</div>
<div class="concept-item" markdown="1">

**生成词元与推理成本**

生成词元是模型解码过程中产生的思考内容和回答内容的基本计量单位，通常与延迟、算力占用及按量计费成本相关。本文仅用生成词元刻画推理开销，以避免不同评测框架的输入长度差异干扰比较。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究输入是同一任务或基准上推理模型与非推理基线的准确率、生成词元数，以及用于部署分析的价格或硬件成本信息；研究对象包括具有推理开关的同架构模型，也包括没有直接非推理对应版本的前沿模型。核心输出是推理相对于基线的边际词元效率，以及推理成本占比和不同部署环境下的成本变化，据此判断某类任务、某档推理强度和某种部署方式是否值得承担“推理税”。实证范围由七个基准上的151次模型—基准评测运行构成，覆盖数学、代码生成、科学推理、指令遵循、专家知识、知识回忆和研究级物理；其关键假设是生成词元数能够作为推理计算开销的可比较代理，而准确率增益代表启用推理带来的任务收益。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{TES}$**

Token Economy Score，词元经济得分；衡量推理模型相对非推理基线的准确率增益，并按生成词元倍数归一化。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{TES}\text{-}\Delta$**

配对式TES变体，用于同一模型架构具有推理开关时，直接比较推理模式与非推理模式。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{RCS}$**

Reasoning Cost Share，推理成本占比；用于判断总推理支出中有多少由内部思考产生。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{DCM}$**

Deployment Cost Multiplier，部署成本乘数；用于估计云端API与本地硬件等部署环境如何改变达到给定TES水平的经济成本。

</div>

</div>

**直接相关的工作**

- **OckBench**: OckBench提出Per-Token Intelligence，即用准确率除以解码词元数，并讨论小型推理模型以更长思考链补偿能力不足的“Overthinking Tax”。本文的TES与其不同：TES比较推理模式相对非推理基线的边际准确率增益，而非衡量单个模型的绝对单位词元性能；同时仅统计生成词元，以隔离评测框架造成的输入差异。
- **ReEfBench**: ReEfBench以逻辑深度刻画推理效率，将其表示为单位计算消耗带来的推理收益。本文在这一效率视角上补充了跨七类基准的任务结构分层，并把词元效率与云端API、本地部署等经济环境联合分析。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推理型模型通过生成扩展思考链换取潜在的准确率提升，但这些内部词元可能成为推理成本的主要来源。实际系统不能仅问“哪个模型得分最高”，还必须判断在特定任务、推理强度和部署方式下，新增正确率是否值得额外的词元、算力与费用；否则，统一开启高强度推理可能在收益很小的任务上浪费资源。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **准确率导向的基准评测**：在标准数据集上比较模型最终答案的正确率或任务得分，并据此形成排行榜。这种方法适合判断绝对质量，却没有把推理模型相对普通模型多消耗的生成词元纳入同一评价量。
- **独立的推理成本核算**：根据生成词元量、服务价格或部署硬件估算一次推理的支出，从而描述模型有多昂贵；但若不与相对准确率增益配对，成本数字本身不能回答额外思考是否产生了足够价值。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 只按准确率比较会把任何微小提升都视为进步，即使该提升需要成倍增加生成词元；其后果是排行榜优势无法直接转化为部署中的成本效益判断。
- 把“推理模型”视为统一类别，或默认更高推理强度会单调改善质量，会忽略任务结构和边际收益递减；其后果是难以确定应在哪些请求上启用推理，以及应选择多大的思考预算。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有评测缺少一个面向部署的边际指标，将推理模式相对非推理基线带来的质量增量与生成词元增量直接关联起来；同时也缺少基于统一框架的证据，用来区分不同任务结构、推理强度和部署环境下的推理经济性。尤其对于没有直接非推理对应版本的前沿模型，还需要可操作但明确带有近似性质的比较办法。

</div>
<div markdown="1"><span>核心问题</span>

推理型大语言模型增加的思考词元在什么条件下能够赚回成本：哪些任务结构产生正向边际效率，提高推理强度如何改变这种效率，以及云端或本地等部署环境如何改变最终的经济可行性？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是比较“多付出的词元”与“多获得的正确率”，而不是分别观察最高准确率和总费用。若任务确实需要连续、多步的推断，额外思考可能显著提高成功率，因此单位词元开销更容易产生价值；若任务主要依赖知识回忆，或原有模型表现已接近饱和，继续生成长思考往往只能带来很小的增益。再把部署成本纳入解释后，同一推理负载也可能因硬件与计费方式不同而得到不同的采用结论。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是训练新的大语言模型，而是提出一套面向部署决策的评测流程：在同一基准任务 $T$ 上，收集推理模型 $M_r$ 与非推理基线 $M_b$ 的准确率、推理令牌数、最终输出令牌数及价格信息；先以生成令牌倍率刻画启用推理带来的额外计算量，再用 Token Economy Score（TES）衡量这部分开销换来了多少准确率增益。根据可用对照，作者采用同模型家族配对的 $\mathrm{TES}\text{-}\Delta$，或以当前表现最好的非推理模型近似反事实基线的 $\mathrm{TES}\text{-A}$。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定任务与比较对象

若同一模型家族提供推理开关或推理与非推理版本，则将对应非推理版本设为 $M_b$，形成 $\mathrm{TES}\text{-}\Delta$；否则选择该基准上准确率最高的可用非推理模型作为 $M_b$，形成 $\mathrm{TES}\text{-A}$。

<div class="method-step__io" markdown="1">

**输入**：基准任务 $T$、待评估的推理模型 $M_r$，以及候选非推理模型。<br>
**输出**：用于边际比较的三元组 $(M_r,M_b,T)$ 及其基线类型。

</div>

**直观理解**：这一步是在回答“如果不用该推理模式，现实中会改用什么模型”。前者尽量控制模型家族差异，后者模拟部署者在没有推理关闭版本时选择最佳可用替代品。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 采集效果与令牌统计

分别计算准确率 $\operatorname{Acc}(M,T)$ 和平均生成令牌数 $\operatorname{GenTok}(M,T)$；生成令牌仅包括内部推理令牌与最终答案令牌，不包括输入提示令牌。

<div class="method-step__io" markdown="1">

**输入**：三元组 $(M_r,M_b,T)$ 的评测运行记录。<br>
**输出**：推理模型与基线的准确率、推理令牌数、输出令牌数和平均生成令牌数。

</div>

**直观理解**：输入提示通常由数据集和评测框架决定，不能反映模型是否进行了更多思考，因此 TES 只比较模型实际生成的内容。可以把它理解为只核算“模型主动多做了多少工作”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算并解释边际令牌经济性

以准确率百分点增益除以生成令牌倍率得到 $\operatorname{TES}(M_r,M_b,T)$，并结合绝对准确率和基线准确率解释结果。作者采用 $\operatorname{TES}>1$、$0<\operatorname{TES}\leq1$ 和 $\operatorname{TES}\leq0$ 三个区间，分别表示高效、边际有效以及浪费或有害。

<div class="method-step__io" markdown="1">

**输入**：$M_r$ 与 $M_b$ 的准确率和平均生成令牌数。<br>
**输出**：每个模型—任务组合的 TES、效率区间及其对应的绝对准确率。

</div>

**直观理解**：TES 问的不是“哪个模型分数最高”，而是“多花若干倍生成令牌后，准确率提高得是否足够多”。阈值 $1$ 是作者设定的统一比较惯例，并非适用于所有业务的普遍效用函数。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 映射到实际部署成本

用 Reasoning Cost Share（RCS）计算内部推理链占总推理费用的比例，并用 Deployment Cost Multiplier（DCM）比较同一工作负载在云端与本地部署下的总费用。RCS 和 DCM 与 TES 分开报告，不参与 TES 的计算。

<div class="method-step__io" markdown="1">

**输入**：输入、推理和最终输出令牌量，云端 API 单价，以及本地系统的吞吐量和摊销成本。<br>
**输出**：推理费用构成、云端与本地成本倍率，以及结合 TES 的部署解释。

</div>

**直观理解**：TES 衡量“令牌换准确率是否划算”，RCS 说明钱主要花在思考还是答案上，DCM 则说明更换运行环境能否改变账单。三者合用可避免把令牌效率与具体硬件、价格体系混为一谈。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 生成令牌数与 Token Economy Score

$$
\begin{aligned}
\operatorname{GenTok}(M,T) &= \operatorname{ReasoningTokens}(M,T)+\operatorname{OutputTokens}(M,T),\\
\operatorname{TES}(M_r,M_b,T) &= \frac{\operatorname{Acc}(M_r,T)-\operatorname{Acc}(M_b,T)}{\operatorname{GenTok}(M_r,T)/\operatorname{GenTok}(M_b,T)}
\end{aligned}
$$

**符号说明**

- $M$：任意待评估模型。
- $M_r$：启用扩展推理或具有推理能力的模型。
- $M_b$：用于反事实比较的非推理基线模型。
- $T$：评测基准或任务。
- $\operatorname{ReasoningTokens}(M,T)$：模型在任务上平均生成的内部推理令牌数。
- $\operatorname{OutputTokens}(M,T)$：模型在任务上平均生成的最终答案令牌数。
- $\operatorname{GenTok}(M,T)$：内部推理令牌与最终答案令牌之和，不包含输入令牌。
- $\operatorname{Acc}(M,T)$：模型在任务上的准确率，以百分数表示，因此模型差值的单位是准确率百分点。
- $\operatorname{TES}(M_r,M_b,T)$：推理模型相对非推理基线的边际令牌经济性得分。

<div class="equation-explanation" markdown="1">

**直观理解**：分子计算启用或选择推理模型后增加了多少准确率百分点，分母计算其生成令牌是基线的多少倍。两者相除后，TES 越大表示额外生成开销换来的准确率增益越充分；负值意味着推理模型准确率没有提高，甚至因“过度思考”而下降。<br>
**原文位置**：第 3.2 节“Formal Definition”

</div>

</div>

<div class="equation-block" markdown="1">

#### Reasoning Cost Share 与 Deployment Cost Multiplier

$$
\begin{aligned}
\operatorname{CostReasoning}(M_r,T) &= \frac{\operatorname{ReasoningTokens}(M_r,T)}{10^6}P_{\mathrm{out}},\\
\operatorname{RCS}(M_r,T) &= \frac{\operatorname{CostReasoning}(M_r,T)}{\operatorname{CostTotal}(M_r,T)},\\
\operatorname{DCM}(M,T) &= \frac{\operatorname{CostTotal}(M,T,\mathrm{cloud})}{\operatorname{CostTotal}(M,T,\mathrm{on\text{-}prem})}
\end{aligned}
$$

**符号说明**

- $\operatorname{CostReasoning}(M_r,T)$：推理模型在任务上的内部推理令牌费用。
- $\operatorname{ReasoningTokens}(M_r,T)$：推理模型在任务上生成的内部推理令牌数。
- $P_{\mathrm{out}}$：服务提供商公布的每百万输出令牌价格。
- $\operatorname{CostTotal}(M,T)$：模型在任务上的总推理费用，由输入、内部推理和最终输出令牌费用组成。
- $\operatorname{RCS}(M_r,T)$：内部推理链费用占总推理费用的比例。
- $\operatorname{DCM}(M,T)$：同一模型工作负载的云端总费用与本地部署总费用之比。
- $\mathrm{cloud}$：按云端 API 定价计算的部署情境。
- $\mathrm{on\text{-}prem}$：按自有硬件吞吐量、资本摊销和运营支出计算的本地部署情境。

<div class="equation-explanation" markdown="1">

**直观理解**：RCS 接近 $1$ 时，意味着绝大部分推理费用用于内部思考而非最终答案；DCM 大于 $1$ 时，按本文定义表示云端成本高于本地成本。它们是成本描述量，而非模型准确率或 TES 的组成部分。<br>
**原文位置**：第 3.4 节“Reasoning Cost Share”和第 3.5 节“Deployment Cost Multiplier”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文提出的是评测指标与部署成本分析方法，不训练或微调模型，也没有通过梯度优化 TES、RCS 或 DCM；这些量均在模型完成基准推理后由准确率、令牌统计和成本数据计算得到。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. TES 基线构造**

$\mathrm{TES}\text{-}\Delta$ 使用同一模型家族中的推理与非推理版本，适合近似控制架构或权重差异；$\mathrm{TES}\text{-A}$ 使用任务 $T$ 上准确率最高的非推理模型，其准确率和平均生成令牌数共同进入计算。对于闭源模型，即使采用供应商配对，也不能据此断言两个版本之间唯一变化是推理机制。

> 直观理解：TES 必须先定义“不启用推理时会怎样”。配对版本更接近受控实验，近似基线更接近真实采购选择，但会把模型家族整体能力差异与推理机制的作用混在一起。

**2. 边际效率评分**

TES 的分子是推理模型相对基线的准确率百分点变化，分母是二者平均生成令牌数之比。作者同时要求报告基线与最终绝对准确率，因为接近满分的基线会压缩可提升空间，而接近随机或低分的基线可能产生看似较高的边际效率，却仍未达到实用准确率。

> 直观理解：单看“每个令牌对应多少准确率”会忽略部署者真正关心的替换收益；TES 只评价从基线升级到推理模型的增量回报。但它不能独立回答最终模型是否已经足够可靠。

**3. 部署成本分解**

RCS 按提供商的每百万输出令牌价格，将推理令牌折算为费用，并除以输入、推理和输出费用之和；DCM 则直接取云端总费用与本地总费用之比。本地每令牌成本来自 $8\times\mathrm{B300}$ 系统的实测吞吐量，并将资本支出摊销与运营支出计入总系统成本。

> 直观理解：相同的令牌量在不同价格和硬件条件下可能对应完全不同的金额。该模块把模型行为层面的令牌统计转换成部署者能够比较的费用结构。

**训练与推理**

推理阶段先让各模型按照统一基准与评测框架完成任务，记录准确率、输入令牌、内部推理令牌和最终输出令牌。随后为每个推理模型指定配对或近似非推理基线，离线计算 TES，并同时保留绝对准确率以识别天花板与地板效应；在成本分析中，再使用公开 API 价格或本地系统实测吞吐量将令牌折算为费用，计算 RCS 与 DCM。该流程不改变模型参数，输出是模型—任务—部署情境层面的效率与成本统计，而不是新的模型预测。

**复现信息**

公平解释 TES 的关键是使用同一任务和兼容的评测设置统计 $M_r$ 与 $M_b$，并以每次运行的平均生成令牌数作为分母数据。输入令牌因主要受提示和评测框架控制而从 TES 中排除，但在总费用 $\operatorname{CostTotal}$ 中仍应计入；$\mathrm{TES}\text{-A}$ 的基线必须同时提供准确率与生成令牌数，不能将一个模型的准确率和另一个模型的令牌成本拼接。部署成本方面，云端使用公布的 API 价格，本地成本依据 $8\times\mathrm{B300}$ 系统实测吞吐量，并将摊销资本支出与运营支出除以处理令牌量。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- AIME 2025：30 道高难度数学竞赛题，归为顺序推理任务；共有 9 组配对模型结果。它主要检验需要多步推导、且前一步结果约束后续步骤时，额外思考 token 是否有效。原文未明确报告训练/验证/测试划分。
- MMLU-Pro：12,000 道中高难度知识与理解题，文中将其操作性地归为知识回忆任务；共有 10 组配对模型结果。它用于检验题目即使较难，当瓶颈主要是事实检索或已有知识时，延长推理是否仍有经济收益。原文未明确报告本研究使用的具体数据划分。
- HLE：2,500 道极高难度前沿领域题，共有 12 组配对模型结果。它代表低正确率上限场景，用于检验在所有模型都远未达到人类水平时，TES 是否必须与绝对准确率共同解读。原文未明确报告本研究使用的具体数据划分。除上述三个代表性数据集外，完整实验还包括 IFBench、GPQA Diamond、LiveCodeBench 与 CritPt，共覆盖七个基准。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Token Economy Score（TES）**

衡量推理模型相对于非推理基线的边际准确率增益，并按生成 token 倍数进行归一化；生成 token 包括内部推理 token 与最终输出 token。TES-Δ 使用同家族配对模型，TES-A 使用近似跨家族对照。文中以 TES 大于 1 作为较强边际效率的判据，但低上限任务仍需同时报告绝对准确率。 （越高越好，因为这表示每单位额外生成 token 换得的准确率增益更大；低值或负向变化意味着推理成本与收益不成比例。）

</div>
<div class="metric-item" markdown="1">

**Reasoning Cost Share（RCS）**

表示一次推理总支出中由内部思考 token 占据的比例，用于揭示用户看不到的内部推理是否主导推理费用。 （通常越低越节省，因为较少成本被内部思考消耗；但它不是准确率指标，不能单独判定模型质量。）

</div>
<div class="metric-item" markdown="1">

**Deployment Cost Multiplier（DCM）**

比较云 API 与本地自有硬件执行同一类推理工作负载时的成本差异，用于量化部署地点对经济性的影响。 （若从采用本地部署的角度看，数值越大表示本地部署相对云 API 的潜在成本优势越明显；这一优势依赖持续负载和较高硬件利用率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨七个基准比较配对或近似配对的 TES，重点对照顺序推理、知识回忆、指令遵循和前沿领域推理等任务结构。

<div class="result-value" markdown="1">

作者报告，任务结构比名义难度更能解释 TES：AIME 2025 的平均 TES 最高，LiveCodeBench 与 IFBench 的平均 TES 也超过 1；相较之下，MMLU-Pro 和 GPQA Diamond 虽然困难，但 TES 较弱。HLE 仅表现为边际正收益，而 CritPt 因非推理基线接近准确率地板，必须结合绝对准确率判断。

</div>

多步数学、程序生成或调试任务存在明确的中间状态，额外思考可以逐步修正后续行动，因此较容易把更多 token 转化为准确率。知识回忆任务的主要瓶颈可能是模型是否存有相关事实，延长思考并不能稳定补回缺失知识。该结果支持按任务结构选择性开启推理，但它是基准层面的关联结论，不能证明任务结构是唯一因果因素，也不能说明所有顺序推理样本都值得增加预算。

<div class="result-source" markdown="1">

来源：第 5.1 节，图 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Figure 1 shows that TES varies more by task structure than by nominal difficulty. Sequential inference-chain tasks produce the strongest returns: AIME 2025 has the highest mean TES, while LiveCodeBench and IFBench also exceed the TES > 1 threshold on average.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 在提供多个 reasoning effort 档位的同一模型家族内，比较中等、高和最大推理预算。

<div class="result-value" markdown="1">

作者报告，数据集中所有具备多推理强度设置的模型家族，在超过中等预算后都出现明显的边际 TES 递减；部分设置中，增加思考预算甚至使准确率下降。

</div>

推理预算不是越多越好。中等预算可能已经完成主要推导，继续生成内部思考会显著增加分母，却只能带来很小的准确率增益，甚至因过度推演或偏离正确路径而降低准确率。该结论针对文中纳入且公开多个强度档位的模型家族，并不证明任意未来模型都具有相同拐点；节选也没有给出各家族的具体下降幅度。

<div class="result-source" markdown="1">

来源：第 5.2 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across every such family in the dataset, increasing reasoning budget beyond a moderate level yields sharply diminishing marginal TES, and in some cases, negative marginal accuracy.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 对相同推理工作负载比较云 API 与 8×NVIDIA B300 本地系统的推理成本，并结合 TES 判断部署选择。

<div class="result-value" markdown="1">

作者报告，在其满利用率摊销假设下，相同模型与工作负载在自有硬件上可比云 API 便宜 2 至 26 倍，具体幅度取决于模型架构。因此，一些 TES 较高但云端成本昂贵的工作负载，若长期重复运行，转为本地部署后可能具有经济可行性。

</div>

TES 本身按 token 倍数计算，不随价格变化，但同一个 TES 对应的实际货币成本会随部署地点变化。该结果说明模型选择不能只看准确率或 token 数，还要结合调用频率、硬件吞吐和利用率。它不意味着购买硬件总是更便宜：若请求零散、设备闲置或运维成本更高，论文给出的本地优势会缩小，云 API 仍可能更合理。

<div class="result-source" markdown="1">

来源：第 6.1 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The same reasoning model serving the same workload can cost 2x to 26x less on owned hardware than on a cloud API, depending on model architecture.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- TES-Δ 依赖同家族推理/非推理配对，但并非所有前沿模型都提供直接对照；TES-A 的跨家族近似比较会混入架构、训练数据、模型规模与基础能力差异。文中特别提示 Gemini 结果属于近似比较，因此其 TES 不应被解释为纯粹由开启推理造成的因果增益。
- 成本结论对数据时间与利用率假设敏感：云 API 价格取自 2026 年 5 月下旬，之后可能变化；本地成本按五年总拥有成本和充分工作负载摊销，未充分利用硬件时实际成本会更高。此外，部分准确率和 token 数据来自外部评测平台，作者虽进行了有限独立校验，但并未对全部 151 次运行统一复现。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 同一模型家族的非推理配置：这是 TES-Δ 的核心基线，尽量固定模型家族与规模，只比较开启推理后准确率和生成 token 的变化，因此比直接比较两个不同模型更接近受控实验。
- 近似的跨家族非推理对照：用于没有直接非推理版本的前沿模型，对应 TES-A。它扩大了模型覆盖面，但模型架构、训练数据和能力差异可能混入结果，因此不能与严格配对的 TES-Δ 等量齐观；文中特别说明 Gemini 结果属于这一类。
- 同一模型家族的较低或中等推理强度：与高或最大推理强度比较，用来判断增加思考预算的边际收益是否递减，以及更多推理是否可能反而降低准确率。
- 云 API 成本基线：将相同推理工作负载的云端价格与本地自有硬件的摊销成本比较，用于判断部署环境是否会改变高 token 推理模型的经济可行性。

**实验想回答的问题**

- 在不同任务结构上，推理模型相对于非推理基线带来的准确率增益，是否足以补偿额外生成的思考与回答 token；任务结构是否比名义难度更能预测这种边际效率？
- 推理强度与部署环境如何改变推理的经济性：提高思考预算是否持续改善收益，以及云 API 与本地部署的成本差异是否会改变模型选择结论？

**实验实现**

实验汇总了七个基准上的 151 次模型—基准评测运行，覆盖 GPT、Claude、DeepSeek、Qwen、Gemini、Grok、GLM 与 Gemma 八个模型家族、27 种模型配置。云端模型的准确率、平均输入 token、推理 token、输出 token 及价格主要取自 Artificial Analysis；生成 token 定义为推理 token 与输出 token 之和，价格采用 2026 年 5 月下旬公开 API 费率。AIME 2025 的部分 Claude 数据补充自 MathArena。作者还在 IFBench、GPQA Diamond、AIME 2025 和 HLE 上对若干开放权重模型进行独立运行，以校验外部数据并测量本地部署成本。

本地实验使用 8 张 NVIDIA B300 GPU，并以 FP16 运行。硬件五年总拥有成本估算为 101.3 万美元，对应每秒 0.00633 美元的摊销运行成本；每 token 成本由该每秒成本除以实测 token 吞吐率得到。吞吐率包含 prefill 与 decode 阶段，并在基准运行间取平均。该核算默认工作量足以充分摊销硬件；突发或低利用率业务的实际本地成本会更高。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 推理预算消融：在同一模型家族内逐级提高 reasoning effort，以较低或中等档位作为对照。 | 超过中等推理预算后，边际 TES 在所有可比较家族中显著下降，且存在增加推理反而降低准确率的案例；原文节选未明确报告各档位的具体 token、准确率和 TES 数值。 | 这一比较尽量固定模型家族，只改变可用思考预算，因此主要隔离“额外思考量”的作用。结果表明最高强度并非稳健默认值，但由于节选没有提供逐模型数值，无法判断不同家族的最优预算是否相同，也无法量化负向准确率变化的统计显著性。 | 第 5.2 节<br><span class="experiment-evidence">Across every such family in the dataset, increasing reasoning budget beyond a moderate level yields sharply diminishing marginal TES, and in some cases, negative marginal accuracy.</span> |
| 部署环境消融：保持模型与工作负载不变，将云 API 价格替换为基于 8×NVIDIA B300 吞吐率和五年总拥有成本估算的本地每 token 成本。 | 在论文的充分利用率假设下，本地执行成本相对云 API 可降低 2 至 26 倍；但作者明确指出，突发或低利用率负载会提高有效每 token 成本。 | 该比较隔离了部署地点和成本模型，而不是模型能力：准确率与 token 需求不变，变化的是每个 token 的货币价格。因而它说明高云端费用不必然否定推理模式，但本地优势依赖持续工作量、吞吐率和硬件摊销条件，不能直接外推到低流量应用。 | 第 4.4 节；成本倍数另见第 6.1 节<br><span class="experiment-evidence">For bursty or low-utilization deployments, effective per-token cost will be higher, and cloud APIs may remain preferable despite a large DCM under full-utilization assumptions.</span> |

**定性案例**

- 论文将 TES 与云端运行成本组成部署象限：AIME 2025 及部分中等推理强度的 LiveCodeBench 运行落入“高 TES、低成本”区域，适合默认开启推理；MMLU-Pro 与最大推理强度的 HLE 更常落入“低 TES、高成本”区域，应关闭推理、降低强度或改用强非推理模型。该象限是操作性决策工具，而非固定排行榜，其结论会随价格、模型版本和业务对准确率的价值估计而变化。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向推理模型的 token 成本效益评测指标，并系统分析不同任务与部署条件下的推理效率。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`d76fed7a206f8996d54f5a5fdfd245c330b553d432923753df526526af0e733d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
