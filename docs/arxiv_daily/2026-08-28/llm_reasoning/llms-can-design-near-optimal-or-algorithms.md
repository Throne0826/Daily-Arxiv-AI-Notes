---
title: "[论文解读] LLMs Can Design Near-Optimal OR Algorithms"
description: "[arXiv 2608.27296][LLM Reasoning] 本文通过统一、无提示调优的单次查询实验，检验通用大语言模型能否针对数学定义明确但难以精确求解的运筹优化问题，直接生成单实例解或可复用于整个问题类别的高性能算法。"
arxiv_id: "2608.27296"
announcement_date: "2026-08-28"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:34:59.214426+00:00"
source_sha256: "bc7f73d1f56768f3f6b8e0449f5546288f621eed4ca8828bfe8006d8bd9fab0e"
tags:
  - "LLM Reasoning"
  - "LLM Agent"
  - "LLM 其他"
  - "大语言模型"
  - "运筹学"
  - "算法设计"
  - "库存控制"
  - "排队网络控制"
  - "商品组合优化"
  - "实例级求解"
  - "通用算法生成"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.27296</p>

# LLMs Can Design Near-Optimal OR Algorithms

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Jackie Baek</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> thanks: Stern School of Business, New York University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27296v1) · [PDF 下载](https://arxiv.org/pdf/2608.27296v1) · **关键词** 大语言模型, 运筹学, 算法设计, 库存控制, 排队网络控制, 商品组合优化, 实例级求解, 通用算法生成<br>


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

本文通过统一、无提示调优的单次查询实验，检验通用大语言模型能否针对数学定义明确但难以精确求解的运筹优化问题，直接生成单实例解或可复用于整个问题类别的高性能算法。

**不用术语来说**：库存补多少货、排队网络下一步服务谁、向顾客展示哪些商品，通常都需要在巨大的候选方案中寻找成本低或收益高的决策。传统上，研究者会利用每类问题的特殊结构，分别推导策略、编写求解程序并进行调参。本文关心的是：如果只把问题规则、输入范围和输出要求交给一个通用大语言模型，并允许它在有限预算内运行 Python，它能否独立写出接近专业方法的算法，而不需要人类提供解题提示或为每个实例专门训练模型？

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出两个层级来区分“解一个实例”与“设计一个算法”：Level 1 向模型提供某个实例的数值参数并要求输出该实例的解；Level 2 只提供问题类别和宽泛参数范围，要求模型预先生成一个从实例参数映射到解的固定算法。该区分使实验能够直接检验模型是否学会了可复用的算法结构，而不只是针对已知数字进行一次性搜索。
- 作者在库存控制、排队网络控制和商品组合优化的十个问题类别上，采用单次、未经调优的提示，将四种不同时期的模型与来源论文中逐实例表现最好的专业方法比较；同时公开提示、代码及完整运行记录，以建立“前沿大语言模型作为运筹算法设计经验基线”的可复现实验框架。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于运筹学（Operations Research, OR）与大语言模型辅助算法设计的交叉领域。运筹学研究如何在需求、容量、服务流程或消费者选择等约束下作出优化决策；本文聚焦库存控制、排队网络控制和商品组合优化三类问题，并考察大语言模型能否在问题定义清楚、参数范围给定且计算预算固定的条件下，直接生成单个实例的解，或进一步生成可用于一类新实例的通用算法。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**良定义的运筹学问题**

指决策变量、目标、约束和相关参数均被明确说明的优化问题。本文讨论的不是让模型自行发现业务目标，而是在数学任务已经清楚的前提下测试其算法设计能力。

</div>
<div class="concept-item" markdown="1">

**实例级求解（Level 1）**

模型先看到某个具体问题实例的全部参数，再为该实例输出一个解。它衡量模型针对已知数据进行一次性优化的能力。

</div>
<div class="concept-item" markdown="1">

**问题类级算法设计（Level 2）**

模型只看到问题类别的描述和宽泛参数范围，必须预先输出一个将实例参数映射为解的算法。评测实例在算法固定后才出现，因此该设置更强调算法对未见实例的泛化能力，而非针对测试实例临时调优。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入分为两个层级：在实例级设置中，模型接收一个库存控制、排队网络控制或商品组合优化的具体实例；在问题类级设置中，模型只接收问题描述与大致参数范围。模型通过一个具有固定计算预算的 Python 沙箱进行计算，并在单次、未经调优的提示下输出具体解或可复用算法；后者应把任意合法实例的参数映射为相应决策方案。实验设置强调极少人工介入，但所给摘要未进一步明确各类问题的数学目标、约束、参数分布及最优性判定方式。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$L_1$**

实例级使用方式：模型看到一个具体实例并为其返回解。

</div>
<div class="notation-item" markdown="1">

**$L_2$**

问题类级使用方式：模型在看到评测实例之前生成从实例参数到解的固定算法。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

现实运筹项目包含建模、算法设计、实现、验证和部署等环节，其中算法设计通常依赖研究者识别问题结构并开发专用方法，成本较高且需要领域经验。随着大语言模型已经具备编程、数学推理和程序生成能力，一个具有实际决策价值的问题是：对于已经被形式化清楚、但搜索空间过大而难以直接穷举或精确优化的问题，能否把部分算法设计工作交给通用模型，从而降低从数学模型到可运行求解器的开发成本？

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于问题结构的经典精确算法与人工启发式策略**：研究者利用特定模型的数学结构开发动态规划、精确求解器、基库存或订货至策略、压力型调度规则、线性规划策略以及局部搜索等方法。精确方法在状态空间可控时计算最优解；启发式方法则以可解释的规则缩小搜索范围，并通过针对问题类别或实例的调参与结构设计获得较好性能。
- **按实例训练的深度学习或强化学习方法**：来源论文中的神经网络、PPO 等方法通常针对一个给定实例反复训练策略，再将训练后的策略用于该实例的决策。它们可以从模拟或优化反馈中学习复杂映射，但训练过程、超参数和所得策略往往与具体实例绑定；在本文的层级划分中，这些方法属于 Level 1，而不是预先生成、可直接处理整个实例类别的 Level 2 算法。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 专业运筹方法高度依赖问题特有的结构知识：库存、排队和商品组合问题分别需要不同的理论、近似方法和计算技巧。其后果是，每遇到一个新模型或新约束，往往都要投入专家时间重新推导、实现和验证，难以判断通用模型能否以更低的人力投入自动完成这一环节。
- 已有学习型基准多为逐实例训练，因而没有回答更严格的泛化问题：在看不到评测实例的数值参数时，系统能否只根据问题类别描述生成一个固定算法，并在整个类别上保持竞争力。逐实例训练的好成绩不能证明模型获得了这种可复用的算法设计能力。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前尚缺少一个受控且跨领域的实证评估，用统一协议将大语言模型置于纯粹的算法设计环节：只给出形式化问题与输出规范，不进行提示调优、不提供优质策略的结构暗示，并同时考察一次性实例求解和事前生成类别级算法。尤其缺少证据说明，类别级算法在评测实例不可见且每个实例计算时间受限时，能否接近逐实例选择的经典精确方法、人工启发式方法或学习型方法。

</div>
<div markdown="1"><span>核心问题</span>

对于库存控制、排队网络控制和商品组合优化这些数学定义明确但精确求解困难的运筹问题，通用大语言模型在最少人类干预下，能否生成性能可与最佳现有专业方法竞争的实例解；更关键地，能否仅凭问题类别及参数范围，设计一个在未见实例上仍有效的可复用算法？

</div>
<div markdown="1"><span>作者直觉</span>

这些问题虽然来自不同领域，但都能被完整写成输入、约束、目标和输出格式，因此模型不必处理需求访谈或现实建模中的歧义，而可以集中进行代码生成、数值试验和策略组合。大语言模型可能已从技术文献和代码中获得动态规划、贪心、松弛、局部改进、基库存控制和压力调度等通用算法构件；借助 Python 沙箱，它可以把这些构件组合并快速检查。直观地说，作者不是要求模型从零发明全部理论，而是检验它能否像熟悉多种工具的算法工程师一样，根据正式规格选择、改造并组装合适的求解步骤。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文提出的不是一种固定的运筹优化算法，而是一套把大语言模型作为“算法设计者”进行评测的方法框架。给定问题类 $C=(\Theta,\mathcal{X},R)$，其中实例参数为 $\theta\in\Theta$、可行解集合为 $\mathcal{X}(\theta)$、确定性评价函数为 $R(\theta,x)$，作者比较两种调用粒度：Level 1 让模型看到具体实例并直接生成该实例的解；Level 2 只让模型看到问题类描述和参数范围，并生成可复用于未知实例的算法 $\sigma$。对于单次决策问题，输出 $x$ 是一个具体选择；对于序贯决策问题，输出是从状态到动作的策略。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 形式化问题类与可行输出

将每个待研究任务写成问题类 $C=(\Theta,\mathcal{X},R)$，并明确实例参数、合法输出形式及统一评价方式。随机需求或顾客选择等不确定性通过期望或长期平均折叠进确定性的 $R$。

<div class="method-step__io" markdown="1">

**输入**：运筹问题的参数空间 $\Theta$、实例相关可行域 $\mathcal{X}(\theta)$ 和奖励函数 $R(\theta,x)$。<br>
**输出**：可由同一接口描述和评测的一组实例，以及每个实例的可行解类型。

</div>

**直观理解**：这一步相当于先写清楚题目、允许提交什么答案，以及如何给答案打分，避免模型和专业算法解决的其实不是同一道题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 选择LLM调用层级

Level 1 将具体实例 $\theta$ 交给模型，要求返回 $x\in\mathcal{X}(\theta)$；Level 2 仅提供问题类及宽泛参数范围，要求返回可执行算法 $\sigma$，且对任意实例应满足 $\sigma(\theta)\in\mathcal{X}(\theta)$。论文不测试在每个状态上调用模型并返回动作的 Level 0。

<div class="method-step__io" markdown="1">

**输入**：问题类 $C$，或一个具体实例 $\theta$。<br>
**输出**：Level 1 的实例专用求解代码，或 Level 2 的跨实例可复用算法代码。

</div>

**直观理解**：Level 1 类似把一道带具体数字的题交给模型；Level 2 则要求模型先写出通用解题程序，再用从未见过的数字测试它。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行单次工具增强设计会话

模型在一次会话中阅读问题，可调用带有 Python 标准库、NumPy 和 SciPy 的沙箱进行推导、搜索或模拟，随后返回规定格式的代码。提示不命名基准策略、不建议求解方法，也不描述理想答案的结构。

<div class="method-step__io" markdown="1">

**输入**：未调优的数学问题提示、Python 沙箱说明、计算预算和规定的代码接口。<br>
**输出**：一次LLM查询生成的具体代码制品，即论文所称的 artifact。

</div>

**直观理解**：作者只给模型题目、有限的计算工具和提交格式，不给解题提示，借此观察模型能否自行发明有效方法。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 隔离执行并进行实例评测

返回代码在LLM会话之外执行，并被禁止再次调用LLM；Level 2 的代码固定后才接收评测实例。作者将其在每个实例上的结果与同一实例上最好的现有方法比较，主结果通常对每个模型—实例或模型—问题类只查询一次。

<div class="method-step__io" markdown="1">

**输入**：模型返回的 artifact、评测实例及其奖励函数 $R$。<br>
**输出**：各模型、调用层级和实例上的可行性与任务奖励，以及相对现有最佳方法的比较结果。

</div>

**直观理解**：模型提交后不能继续问模型或临场改答案，尤其是 Level 2 必须像真正的通用算法一样接受新实例。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 损失销售库存策略的长期平均奖励

$$
R(\theta,\pi)=-\lim_{T\to\infty}\frac{1}{T}\,\mathbb{E}\!\left[\sum_{t=1}^{T}h\,(I_t-d_t)^+ + p\,(d_t-I_t)^+ + c\,a_t\right]
$$

**符号说明**

- $\theta=(F,\ell,h,p,c,\bar q)$：库存实例参数：需求分布、确定性交货提前期、持有成本、缺货惩罚、单位订货成本和最大订货量
- $\pi$：从库存状态映射到订货动作的策略
- $T$：用于定义长期平均值的时间范围
- $I_t$：第 t 期订单到达后的现有库存
- $d_t$：第 t 期随机需求，服从分布 F
- $a_t$：第 t 期下达的订货量
- $h$：单位剩余库存的持有成本
- $p$：单位未满足需求的损失销售惩罚
- $c$：单位订货成本
- $(z)^+$：正部函数，即 max(z,0)

<div class="equation-explanation" markdown="1">

**直观理解**：每一期同时计算卖不掉的库存、无法满足的需求和新订货三类成本，再取无限期平均；由于框架统一使用“奖励越大越好”，总成本前加负号。LLM生成的不是某一期的订单，而是根据现有库存和在途订单持续决定 $a_t$ 的策略。<br>
**原文位置**：第2.1节，Example 1（Inventory control with lost sales）

</div>

</div>

<div class="equation-block" markdown="1">

#### MMNL商品组合的期望收入

$$
R(\theta,S)=\sum_{j=1}^{m}\omega_j\,\frac{\sum_{i\in S}r_i u_{ji}}{v_{0j}+\sum_{i\in S}u_{ji}}
$$

**符号说明**

- $\theta=(m,n,\omega,u,v_0,r,k)$：商品组合实例参数，包括顾客分群数、商品数、分群权重、商品效用、外部选项权重、价格和集合大小上限
- $S$：提供给顾客的商品集合，满足 |S| 不超过 k
- $m$：顾客分群数量
- $\omega_j$：第 j 类顾客在总体中的权重
- $r_i$：商品 i 的价格或售出收入
- $u_{ji}$：商品 i 对第 j 类顾客的效用权重
- $v_{0j}$：第 j 类顾客不购买任何商品的外部选项权重
- $k$：允许提供的最大商品数量

<div class="equation-explanation" markdown="1">

**直观理解**：对每类顾客，分式计算所选商品带来的期望收入，再按该顾客群体的占比加权求和。这里输出 $S$ 是一次性的商品选择，因此与库存策略不同，模型不需要在后续状态中反复行动。<br>
**原文位置**：第2.1节，Example 2（Assortment optimization under MMNL）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文没有针对这些任务训练或微调LLM，也没有定义用于更新模型参数的训练损失；模型在推理阶段通过一次工具增强查询生成代码。优化目标由各问题的奖励函数 $R(\theta,x)$ 给出：算法应在满足 $x\in\mathcal{X}(\theta)$ 的前提下获得尽可能高的奖励，但所给章节没有规定LLM必须采用某种特定搜索、动态规划或数学规划过程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 问题类统一接口**

问题类写为 $C=(\Theta,\mathcal{X},R)$。单次决策问题的 $x$ 可以是商品集合等静态对象；序贯问题的解则是策略 $\pi:\mathcal{S}\to\mathcal{A}$，其中 $\mathcal{S}$ 和 $\mathcal{A}$ 分别是状态空间与动作空间。

> 直观理解：统一接口让库存控制、排队网络控制和商品组合优化可以在同一框架下讨论，但不会强迫它们使用相同的内部算法。

**2. 分层调用与代码制品**

Level 1 的 artifact 实现一个实例专用解；Level 2 的 artifact 实现映射 $\sigma:\Theta\to\bigcup_{\theta}\mathcal{X}(\theta)$，并要求其在输入 $\theta$ 上输出属于 $\mathcal{X}(\theta)$ 的解。Level 2 不能在执行时调用LLM，否则会退化为把 Level 1 查询包装进代码。

> 直观理解：该设计区分“模型会不会解当前题”和“模型会不会写出以后都能用的算法”，后者是更严格的算法设计能力。

**3. 受限Python沙箱与外部评测**

单次会话可使用 Python 标准库、NumPy 和 SciPy，但没有 Gurobi 等外部优化求解器；示例提示给出总计 $3600$ 秒 Python 计算量和最多 $50$ 次调用。代码提交后在外部环境运行且不得访问LLM，从而把设计阶段的计算与部署阶段的算法行为分开。

> 直观理解：沙箱允许模型做数值试验，但不能直接依赖昂贵商业求解器或在测试时继续向模型求助，因此比较更接近受固定资源约束的算法竞赛。

**训练与推理**

整个过程属于推理时算法设计。Level 1 中，每个模型—实例对运行一次独立会话，模型看到具体 $\theta$，利用受限 Python 沙箱生成该实例的解或策略代码；Level 2 中，每个模型—问题类对运行一次会话，模型只看到类定义和宽泛参数范围，生成接收实例参数的设计函数或通用算法 $\sigma$。随后 artifact 被固定并在外部环境执行：单次决策任务直接返回集合等解，序贯任务返回状态到动作的策略。主结果不通过多次采样择优，只有 artifact 存在缺陷时按附录A的规则重跑；重复查询的稳定性另在第6.3节检查。

**复现信息**

公平解释结果所需的关键约束是：提示未经任务方法调优，只说明数学问题、沙箱、计算预算和输出接口；沙箱仅提供 Python 标准库、NumPy 与 SciPy，不提供 Gurobi 等外部优化器；示例库存提示允许总计 $3600$ 秒 Python 计算和最多 $50$ 次工具调用。返回代码不得调用LLM，否则 Level 2 可以用 $\sigma(\theta)=\mathrm{LLM}(\theta)$ 绕过通用算法要求。库存任务要求输出整数订货量，Level 1 接口示例为 `order(on_hand, pipeline)`，Level 2 接口示例为 `design(params)` 并返回相应的订货函数。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 库存控制基准沿用 Gijsbrechts et al. (2022) 的实例体系，覆盖缺货损失、双源采购和多级分销三类设置；正文重点考察 26 个缺货损失实例，另外两类的说明和结果被放入附录。其作用是检验 LLM 在随机、动态库存决策中能否匹配面向具体结构设计的库存启发式或学习方法。原文说明尽可能保留既有实例与基准，但调整了原本可被精确求解的情形；所给节选未交代训练集、验证集或随机种子划分。
- 排队控制基准来自 Dai and Gluzman (2022)，共 13 个连续时间多类别排队网络实例，包括可用截断均匀化马尔可夫链上的相对价值迭代求解的 criss-cross 与 N-model，以及规模更大、动态规划不可行的扩展六类别网络。每个实例由到达率 $\lambda_q$、服务率 $\mu_{sq}$、服务器—队列兼容矩阵 $A_{sq}$、路由结构和单位持有成本 $h_q$ 定义，用于检验 LLM 生成的调度策略能否降低长期平均在队成本。
- 选品优化采用 Guo et al. (2025) 专门构造的困难实例，分为三个独立问题类：带基数约束的混合多项 Logit（MMNL）共 628 个已发布实例；嵌套 Logit 共 971 个已发布实例；带五个线性约束 $Ax\leq B$ 的 MMNL 从 1,800 个再生成实例中删除 6 个无可行商品的退化实例，留下 1,794 个用于 Level 2。Level 1 采用分层子集：72 个 MMNL、48 个嵌套 Logit和 36 个约束 MMNL 实例。该基准旨在避免只在标准启发式容易处理的实例上得出乐观结论。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**长期平均持有成本**

排队网络的目标为 $\limsup_{T\to\infty}\frac{1}{T}\mathbb{E}[\int_0^T\sum_{q=1}^Q h_qX_q(t)\,dt]$，即时间跨度趋于无穷时，所有队列中作业数量按单位持有成本加权后的平均值。它同时反映拥堵程度与不同作业类别的成本重要性。 （越低越好，因为目标是减少作业等待和滞留造成的长期平均成本。）

</div>
<div class="metric-item" markdown="1">

**期望收益**

选品问题根据给定离散选择模型计算所提供商品集合的预期收入；例如嵌套 Logit 中，它综合顾客选择各巢及巢内商品的概率与商品收入。该指标检验算法能否在基数约束或一般线性约束下选出高价值商品组合。 （越高越好，因为选品优化的直接目标是最大化选择模型下的期望销售收入。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个运筹优化领域的总体比较

<div class="result-value" markdown="1">

作者声称，最强模型 gpt-5.6-sol 在几乎所有评测实例上达到或超过最佳既有方法。

</div>

若由完整结果表支持，这意味着前沿 LLM 已可成为这些定义清楚的运筹问题上的强经验基线，而不只是生成可运行但质量一般的代码。不过“几乎所有”并不等于全部，且所给章节节选没有各数据集的分数、最优差距或显著性分析，因此无法核验优势的大小与稳定性。

<div class="result-source" markdown="1">

来源：Abstract；所给实验章节节选未包含对应结果表

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The strongest model we test, gpt-5.6-sol, matches or outperforms the best existing method on almost all evaluated instances.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Level 2：算法在看到评测实例之前固定

<div class="result-value" markdown="1">

作者声称，即使模型只获得问题类别与参数范围、必须预先生成通用算法，其表现仍可与最佳既有方法匹配或更优。

</div>

Level 2 比逐实例求解更接近真正的算法设计：模型不能根据每个测试实例临时修改方法。因而该结果若成立，说明生成物具有一定跨实例泛化能力，而非只是在单个实例上进行计算搜索。但这仍只证明在论文给定的参数范围与同分布基准中有效，不能推出对新问题类别或范围外规模也能泛化。

<div class="result-source" markdown="1">

来源：Abstract；所给实验章节节选未包含对应分领域数值

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This holds even at level 2, where the returned algorithm is fixed before seeing the evaluation instances.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 不同发布时间模型之间的能力变化

<div class="result-value" markdown="1">

作者报告，在发布时间相隔不到八个月的模型序列中，算法设计表现出现显著提升。

</div>

这一比较意在说明能力增长速度，而非证明某个架构组件导致提升。由于节选没有列出模型清单、各模型分数及是否采用完全相同的工具和预算，“显著提升”目前只能作为作者的总体观察，不能据此量化时间趋势或做因果归因。

<div class="result-source" markdown="1">

来源：Abstract；所给实验章节节选未包含模型对比表

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Performance also improves sharply across models released less than eight months apart, suggesting that this capability is moving quickly.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验章节节选缺少核心结果表及附录结果，未明确报告各领域的具体得分、相对最优差距、方差、置信区间和失败实例。因此摘要中的“几乎所有实例”和“显著提升”无法在当前材料内独立核验，也不能判断少数失败是否集中于某一问题族或规模区间。
- 基准均来自三个定义明确且参数范围已知的运筹问题族；Level 2 证明的至多是这些范围内的跨实例泛化。选品 Level 1 还只使用分层子集。实验不能直接证明模型能处理分布外规模、建模含糊的问题、现实数据误差，或无需人工验证地部署所生成算法。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Gijsbrechts et al. (2022) 的专用库存启发式及其单一深度强化学习方法：该工作原本就在检验通用深度强化学习能否匹配专家库存策略，因此适合作为 LLM 自动设计算法的直接参照；节选未列出各库存基线的具体名称。
- 截断均匀化链上的相对价值迭代：用于低维 criss-cross 和 N-model 排队实例，并提供可计算的动态规划最优值。它比单纯比较另一种启发式更有判别力，因为可直接衡量 LLM 策略与最优策略之间的差距。
- Dai and Gluzman (2022) 的 PPO 策略：针对每个扩展六类别排队网络实例分别训练，是这些无法由动态规划处理的大规模实例上的最强既有比较方法。它与 Level 2 的对比尤其严格，因为 PPO 可针对测试实例训练，而 Level 2 算法在看到评测实例前已经固定。
- Guo et al. (2025) 困难选品基准中的文献算法与标准启发式：这些实例被刻意构造成标准选品启发式难以处理的情形，因而可测试 LLM 是否只是复现常见规则。所给节选未提供各算法名称及逐方法结果，不能进一步区分具体比较对象。

**实验想回答的问题**

- 在实例参数已知的 Level 1 设置中，单次、未经调优的 LLM 查询能否直接为库存控制、排队网络控制和选品优化实例生成与专用算法竞争的解或策略？
- 在评测实例尚不可见的 Level 2 设置中，LLM 能否仅依据问题类别和参数范围设计一个固定算法，并使该算法在新实例上的表现接近动态规划、专用启发式、深度强化学习或文献中的选品算法？

**实验实现**

实验区分两种使用层级。Level 1 向模型提供一个具体实例，模型为该实例生成解；Level 2 仅提供问题类别描述和宽泛参数范围，模型必须返回从实例参数映射到解的算法，并在接触评测实例之前固定。人类只使用一个未经调优的提示，模型可调用具有固定计算预算的 Python 沙箱。选品 Level 1 对每个实例单独查询，沙箱预算为 900 秒，并因成本采用按配置分层抽取的小型评测集；Level 2 则覆盖更完整的已发布或再生成实例。选品提示会指出选择模型，但不命名基线，也不暗示求解路线，从而减少直接照抄指定算法的可能。所给节选未完整报告库存和排队实验的运行时预算、重复次数、置信区间、随机性处理方法，也未给出结果表中的统一相对差距计算公式。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 排队实验形成了一个有解释力的难度分层案例：criss-cross 与 N-model 规模较小，可用相对价值迭代计算最优策略；扩展六类别网络随站点数增长到动态规划不可处理，只能与逐实例训练的 PPO 比较。前一组回答“LLM 离可计算最优值有多远”，后一组回答“在实际不可精确求解的规模上是否胜过强学习基线”，两者不能混为同一种最优性证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper studies LLM algorithmic reasoning on operations-research problems through generation of solutions and reusable algorithms using a Python tool.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`bc7f73d1f56768f3f6b8e0449f5546288f621eed4ca8828bfe8006d8bd9fab0e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
