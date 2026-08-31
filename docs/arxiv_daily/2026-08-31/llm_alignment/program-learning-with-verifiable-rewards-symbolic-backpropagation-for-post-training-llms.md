---
title: "[论文解读] Program Learning with Verifiable Rewards: Symbolic Backpropagation for Post-Training LLMs"
description: "[arXiv 2608.28421][对齐 / RLHF] 原文未明确报告。"
arxiv_id: "2608.28421"
announcement_date: "2026-08-31"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:36:07.980780+00:00"
source_sha256: "a5a69bb12a38817af8c24d4706b50fcb87619c73c29eafeb5898a75c37b87515"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "大语言模型后训练"
  - "程序学习"
  - "可验证奖励"
  - "符号反向传播"
  - "类型推理"
  - "契约验证"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.28421</p>

# Program Learning with Verifiable Rewards: Symbolic Backpropagation for Post-Training LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Vishvesh Bhat</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28421v1) · [PDF 下载](https://arxiv.org/pdf/2608.28421v1) · **关键词** 大语言模型后训练, 程序学习, 可验证奖励, 符号反向传播, 类型推理, 契约验证<br>


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

本文位于大语言模型后训练、可验证推理与程序学习的交叉领域。传统监督微调和强化学习后训练通常直接更新模型权重，使能力保存在模型内部；本文研究另一种设置：当任务的中间步骤可以由明确规则检查时，不更新基础模型，而是学习一个由确定性组件和小型神经组件构成、具有类型与输出契约的显式推理程序。程序在执行过程中逐步产生可检查的中间状态，因此既能定位错误，也能将已学得的程序迁移到其他规模的基础模型上。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**后训练**

后训练是指在基础语言模型预训练完成后，利用示例或奖励进一步调整其行为。本文把后训练对象从模型权重改为显式程序；基础模型在程序学习过程中保持冻结。

</div>
<div class="concept-item" markdown="1">

**类型与输出契约**

类型描述某一步输入或输出的结构和允许的数据形式，输出契约则规定该结果必须满足的可检查条件。例如工具调用必须符合接口签名，任务列表必须覆盖用户请求。它们使系统能够在每一步判断结果是否合格，而不必等到整条轨迹结束。

</div>
<div class="concept-item" markdown="1">

**符号反向传播**

这是本文提出的信用分配方法：先比较程序最终输出与真实答案，再依据各个原语的类型签名，反向推导上一层必须产生什么结构。它类似可微模型中的反向传播，但传递的是可推导的类型要求，而不是由数值梯度估计的信号。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定输入—输出示例以及一个由确定性原语和神经原语组成的原语库，目标是在冻结基础模型权重的条件下，学习一个由若干层原语、连接方式和参数构成的推理程序。程序的前向执行从任务输入开始，逐层产生带有本体信息的中间状态，最终输出任务答案；输出需与真实标签比较，并且每一步都必须满足相应的类型和契约约束。方法适用于中间结果可验证的任务，例如代码执行测试和对话约束满足，不主张适用于主要依赖主观判断的摘要或开放式生成。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N$**

程序包含的层数；每一层对应一个可检查的中间状态和一个程序检查点。

</div>
<div class="notation-item" markdown="1">

**$k$**

程序中的层索引；反向推导通常从第 $k$ 层所需的本体出发，得到第 $k-1$ 层必须满足的输入要求。

</div>
<div class="notation-item" markdown="1">

**$k-1$**

当前层的前一层；其所需输入本体由后一层的要求和原语声明的类型签名共同推导。

</div>
<div class="notation-item" markdown="1">

**$PLVR$**

Program Learning with Verifiable Rewards，即“带可验证奖励的程序学习”；本文提出的后训练方法名称。

</div>

</div>

**直接相关的工作**

- **强化学习与可验证奖励（RLVR）**: 原文将 RLVR 视为直接相关的对照范式：它用程序规则验证最终结果，而不是用学习得到的奖励模型，但奖励仍主要是轨迹结束时的标量信号。PLVR 保留可验证性的思想，并把检查扩展到每个程序步骤，从而将稀疏的终点反馈变为覆盖程序结构的逐步契约判定。
- **基于标量得分的智能体工作流优化**: 原文指出，这类方法在离散、部分符号化的程序结构上依据整条轨迹的粗粒度分数搜索，因而需要估计哪些步骤导致成功或失败。PLVR 的差异在于利用类型推理反向导出前一层的必要输入本体，把信用分配变成确定性的推导，而不是从多次运行结果中估计。

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

PLVR（Program Learning with Verifiable Rewards）不直接更新待服务基础模型的权重，而是从输入—输出示例中搜索一个由类型化原语和高阶算子组成的显式程序。程序以神经符号分词器把原始文本转换为本体 $4\Omega_04$，逐层执行并产生中间本体；输出再与目标本体 $4\Omega_{\mathrm{out}}4$ 比较得到损失。随后，方法从输出端向输入端进行符号反向传播：利用原语签名和类型推理，推导每一层必须产生的输入本体，并搜索满足这些要求且能改善最终输出的组合。直观地说，它把传统反向传播中的“梯度”替换成可检查的类型需求和契约违例，因此学习结果是可读、可逐层检查、可迁移的程序及其小型神经原语，而不是隐藏在基础模型权重中的能力。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 输入与输出本体化

神经符号分词器执行 $4\textsc{Tokenize}:\mathrm{Raw}\times\mathrm{Schema}\to\Omega4$，将实例转换为输入本体 $4\Omega_04$，将候选答案或目标答案转换为输出本体 $4\Omega_{\mathrm{out}}4$。分词器的学习部分识别说话者、动作等语义结构，符号部分检查类型、顺序、交叉引用、形式语言解析以及文本字段是否为源文本的逐字片段。

<div class="method-step__io" markdown="1">

**输入**：基准任务提供的原始输入文本、答案文本以及相应的输入和输出模式（Schema）。<br>
**输出**：结构化、可嵌套且带类型的本体对象集合，包括用户轮次、助手轮次、工具描述、配置、代码和工具调用等对象。

</div>

**直观理解**：这一步像把自然语言问题和答案装入统一格式的“数据结构”。后续程序不直接处理杂乱文本，而是在这些带标签的对象上计算，因此分词器决定了损失函数究竟能看见哪些错误。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 逐层执行与输出评分

程序由每层中的原语和算子组合而成；从全为 pass-through 的初始层开始，顺序执行候选程序并记录每一层的本体。最终输出按照目标本体的键域评分，先进行按内容而非键位置的对象对齐，再计算对象类型错误和对象值错误；代码使用测试通过率，工具调用使用精确匹配并保留绑定层面的部分得分。

<div class="method-step__io" markdown="1">

**输入**：输入本体 $4\Omega_04$、固定层数 $4N4$ 的候选程序、原语参数以及目标输出本体。<br>
**输出**：每一层的中间本体、最终预测本体、输出本体损失，以及用于候选排序的运行状态、类型错误数、值误差和偏离项。

</div>

**直观理解**：这相当于给程序设置一串天然的调试断点：每层状态都能直接读出。评分不仅问“最终答案是否完全相同”，还区分缺失对象、类型错误和部分正确的值，从而给搜索提供更细的反馈。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 符号反向传播与候选合成

对所需本体中的每个对象进行一阶类型统一，筛选输出类型可统一的原语；若单个原语无法覆盖需求，则由 Sequence、Parallel、Branch、Foreach、Loop 或 Fallback 等高阶算子组合候选，并由叶节点签名推出所需输入本体 $4\Omega_{\mathrm{in}}=igcup\{\mathrm{intype}(p)\mid p\in\mathrm{leaves}(c)\}4$。随后枚举声明范围内的自由参数，用当前可用对象、scratchpad 和轮次上下文缩小范围；违反原语输出契约的赋值在执行前被剪除。

<div class="method-step__io" markdown="1">

**输入**：当前层所需的本体 $4\Omega_{\mathrm{req}}4$、原语输入—输出类型签名、可用的下层本体、最大组合深度 $4d_{\max}4$ 以及原语契约。<br>
**输出**：带有局部组合、参数赋值和下一层所需输入本体的候选集合；在第一层，候选必须能由固定的 $4\Omega_04$ 满足。

</div>

**直观理解**：它不是猜一个黑盒步骤再估计“可能有用”，而是从最终需要什么倒推前一步必须提供什么。类型签名像拼插头：不匹配的组合直接淘汰，契约则像每个零件的质量检查，防止产生不可接受的中间结果。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 束搜索、交替训练与收敛

在每个示例上按“前向执行—计算损失—反向推导”处理候选，并以全局束宽 $4k4$ 保留累计得分最好的程序；排序键依次考虑是否无法运行、类型错误数、值损失、与当前程序的输入本体偏离，剩余并列再按大小和标签打破。搜索阶段冻结原语，阶段之间利用逐步所需本体和局部契约违例微调神经原语，随后用更新后的原语重新评估束，直至再训练阶段不再降低平均束损失。

<div class="method-step__io" markdown="1">

**输入**：各层候选程序、其最终输出损失、累计示例得分、局部契约违例和当前束中的程序。<br>
**输出**：收敛的显式程序、其参数、被该程序调用的神经原语权重，以及可检查的逐层本体和契约记录。

</div>

**直观理解**：这像先固定零件质量来挑选装配方案，再根据最常失败的零件进行专项训练，然后重新评估整套方案。最终部署的不是一个被整体改写的基础模型，而是一份可以阅读、验证、替换组件和重新训练的程序。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 本体损失的综合评分

$$
\mathcal{SC}(\ell)=\Big(\underbrace{\sum_{k}\ell(k)_{\mathrm{type}}}_{\mathrm{integer}},\ \underbrace{\sqrt{\sum_{k}\ell(k)_{\mathrm{val}}^{2}}}_{\mathrm{unbounded\ above\ 1}}\Big)
$$

**符号说明**

- $\mathcal{SC}(\ell)$：由损失映射得到的二元评分，按字典序比较。
- $\ell$：按目标本体对象键索引的损失映射。
- $k$：目标本体中的对象键。
- $\ell(k)_{\mathrm{type}}$：对象的类型损失；对象缺失或类型不匹配时为 $1$，否则为 $0$。
- $\ell(k)_{\mathrm{val}}$：对象的值损失；类型正确时为 $1-a(p_k,t_k)$，其中 $a$ 是该类型声明的值一致性度量。
- $a(p_k,t_k)$：预测对象 $p_k$ 与目标对象 $t_k$ 的类型专属一致性；代码使用测试通过率，工具调用使用精确匹配并支持绑定层面的部分得分。

<div class="equation-explanation" markdown="1">

**直观理解**：评分先最小化类型错误数量，再最小化值误差的 $L_2$ 范数；因此一个额外的类型错误会压过任意大小的值改进。设计意图是先保证程序产出的对象种类正确，再在正确类型内优化具体内容，但代价是类型误判可能使搜索排序较为刚性。<br>
**原文位置**：§3.5，式（4）定义逐对象损失，式（5）定义综合评分

</div>

</div>

<div class="equation-block" markdown="1">

#### 反向推导的所需输入本体

$$
\Omega_{\mathrm{in}}=\bigcup\{\,\mathrm{intype}(p)\mid p\in\mathrm{leaves}(c)\,\}
$$

**符号说明**

- $\Omega_{\mathrm{in}}$：候选组合 $c$ 在执行前需要由前一层提供的输入本体。
- $c$：能够产生当前所需输出本体的原语—算子组合。
- $\mathrm{leaves}(c)$：组合 $c$ 中所有叶节点原语的集合。
- $\mathrm{intype}(p)$：原语 $p$ 声明的输入类型集合。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把组合中所有叶原语需要的输入类型合并起来，形成前一层的需求。它就是符号反向传播的核心：组合越复杂，必须从更早层准备的对象类型越明确；在第一层还要检查这些对象确实存在于分词器产生的 $4\Omega_04$ 中。<br>
**原文位置**：§3.6“Type resolution”，式（7）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：PLVR的直接优化对象不是基础模型权重，而是程序结构、程序参数以及其调用的神经原语权重。对每个示例，程序以最终输出本体相对于目标本体的损失排序；类型错误优先于值误差，无法执行的候选优先淘汰。搜索阶段冻结神经原语，使累计评分对应一个稳定的候选函数；再训练阶段则把反向推导出的逐步所需本体和定位到具体原语的契约违例作为训练目标，微调小型神经原语，并在更新后重新评分束。原文将停止条件表述为再训练阶段不再改善平均束损失，未给出一个统一的可微标量目标或基础模型权重更新规则。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 类型化本体与神经符号分词器**

对象是带有类型字段和键值集合的结构化记录，允许值继续包含对象或对象列表；本体是从键到对象的部分映射。分词器在程序边界把原始文本映射到本体，并要求对象符合模式、顺序连续、引用可解析、工具调用绑定通过类型检查，且文本字段必须是源文本的逐字片段。

> 直观理解：本体是程序的统一中间语言：它同时保存“这是什么类型”和“在当前输入中具体是什么值”。统一表示使输入、所有中间层和输出都能用同一套契约和损失检查。

**2. 带契约的原语与高阶算子**

原语是无状态、无副作用的一阶计算叶节点，具有声明的输入—输出类型签名和输出契约；库包含 Decompose、Elaborate、Init-Scratchpad、Get-Order、Denote、Check-Prerequisites、Match、Identity、Wrap、Append。原语可为确定性的符号组件或针对单一操作训练的小型语言模型；高阶算子则接收原语或子组合，负责顺序、并行、分支、循环、逐项处理和回退等控制流。

> 直观理解：原语像功能单一且有验收标准的积木，算子像安排积木如何连接和重复的控制结构。把复杂任务拆成小操作，使每个中间结果都能单独检查，也避免要求一个模型一次完成整个任务。

**3. 符号反向传播与束搜索**

前向过程产生最终损失，反向过程不计算数值梯度，而是依据类型统一、原语签名和高阶算子规则推导所需输入本体；类型可行性过滤后，再搜索声明范围内的值参数，并以最终输出表现进行候选排序。候选按累计得分保留全局 top-$k$，等价于在受类型约束的程序空间中进行受控搜索；契约违例可在后续层执行前剪枝。

> 直观理解：传统反向传播回答“参数应向哪个数值方向移动”，这里回答“前一层必须产出哪些类型的对象”。因此信用分配是一条可复核的推导链，搜索仍存在于参数取值和组合选择部分，但不会在明显不合法的程序上浪费预算。

**训练与推理**

训练时，示例逐个进入当前束：先用冻结的原语执行候选程序并记录每层本体，再计算输出损失；随后从最后一层开始反向推导所需本体，进行类型统一、组合生成、输入可达性过滤、参数值搜索和契约剪枝。所有示例上的累计分数用于保留全局 top-$k$ 程序，而不是只保留当前示例上表现好的程序；行为等价于 Identity 的组合会被规范化并去重。搜索与神经原语训练交替进行，原语更新后必须重新评估现有束，直到平均束损失不再改善。推理时，输入先由同一分词器转换为 $4\Omega_04$，再执行已学习程序及其原语；中间本体可作为检查点直接读取，输出本体最后转换回代码或工具调用等原始答案格式。基础模型本身保持冻结，只有显式程序和其中的小型神经原语被学习。

**复现信息**

复现或公平解读所必需的结构约束包括：程序固定为 $4N4$ 层，每层初始为 Identity；候选组合受最大深度 $4d_{\max}4$ 约束，束宽为 $4k4$，但这些超参数的具体数值在所给摘录中仅指向附录A，原文未明确报告。第一层的输入可达性检查是精确过滤，而不是启发式惩罚；当前方法也不对候选推导输入本体与真实 $4\Omega_04$ 的残差进行分级评分，无法满足者直接过滤。损失按目标对象键域计算，但对象按内容对齐，以避免插入一个设置调用造成后续对象整体错位时被错误地判为完全失败。确定性契约可穷举保证其声明属性，神经原语的经验契约只能发现违反条件的输出，不能证明所有满足契约的输出都语义正确。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LiveCodeBench v6（时间范围为 2025 年 3 月至 4 月）：通过执行生成代码并对照测试用例验证结果，测试程序在可执行代码任务上的正确性；原文未明确报告该实验所使用的具体题目数量、训练集划分或测试集规模。
- $\tau^{2}$-Bench：在多轮对话中依据既定策略验证约束是否满足，测试方法能否迁移到不同于代码执行的结构化、策略约束型验证；实验覆盖三个领域，原文未明确报告各领域的具体样本数与划分。
- 合成原语微调语料：用于训练独立神经原语，而非直接训练基准任务解法；共 18,502 个样本，按 90/10 划分为 16,645 个训练样本和 1,857 个验证样本。其作用是检验各原语能否可靠执行单一操作，并支持同一原语库服务多个基准。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务得分或成功率**

衡量模型在 LiveCodeBench v6 或 $\tau^{2}$-Bench 上是否产生通过验证的结果；代码任务依据测试执行结果，多轮任务依据策略约束满足情况。 （越高越好，因为更高分表示更多输出通过任务验证。）

</div>
<div class="metric-item" markdown="1">

**Top-1 accuracy**

在程序搜索中，衡量当前领先等价类所对应程序或候选解获得正确结果的比例；图 1 将其作为训练样本前缀长度的函数进行统计，并对 109 个训练集排列报告均值与 5–95% 区间。 （越高越好，因为它表示单个最高排名候选程序更可能正确。）

</div>
<div class="metric-item" markdown="1">

**Top-1 loss**

衡量领先候选程序相对于目标输出的损失；图 2 观察该损失是否接近最优程序 $p^{*}$ 的损失下界。 （越低越好，因为较低损失意味着候选程序输出更接近正确目标。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### LiveCodeBench v6 与 $\tau^{2}$-Bench 上的总体比较

<div class="result-value" markdown="1">

摘要声称，30B 基础模型使用 PLVR 后，在匹配预算下平均超过 RL 方法 27.8 个百分点；同时超过参数量大一个数量级的前沿模型 13.6 个百分点。

</div>

该结果支持 PLVR 在代码执行验证和多轮策略约束验证两种不同验证机制上都具有优势，并且优势不只是来自更大的基础模型或更多测试时预算。但由于所给章节摘录没有提供表 2 的逐模型、逐领域分数，无法判断优势是否在三个 $\tau^{2}$-Bench 领域中均匀出现，也无法从摘录单独核验平均值的计算方式。

<div class="result-source" markdown="1">

来源：摘要；实验章节 5.1 提及表 2，但所给摘录未包含表 2 的具体数值

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On LiveCodeBench v6 and Tau2Bench, 30B base models with PLVR outperform RL at matched budget by 27.8 points on average and frontier models an order of magnitude larger by 13.6 points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨任务复用原语库

<div class="result-value" markdown="1">

同一原语库被用于两个基准；作者称新任务的边际成本为 100 个程序搜索样本，且不需要新的微调数据。

</div>

这说明方法试图学习可组合的通用操作，例如分解、排序、检查前置条件和匹配函数，而不是为每个基准单独记忆任务行为。它支持任务无关原语的可迁移性主张，但不等于证明原语库能迁移到任意领域；当前证据只覆盖 LiveCodeBench v6 与 $\tau^{2}$-Bench，且摘录未给出该复用实验的独立对照或完整成本表。

<div class="result-source" markdown="1">

来源：摘要；实验章节 4.3 的“Task-agnosticism and provenance”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

A single primitive library serves two benchmarks, so the marginal cost of a new task is 100 examples of program search and no new finetuning data.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 程序搜索收敛与训练集顺序稳定性

<div class="result-value" markdown="1">

在 109 个训练集排列上，$n=70$ 个训练样本时正确程序 $p^{*}$ 在所有排列中都进入领先等价类；图 2 显示此时损失带收敛到 $p^{*}$ 的损失下界 0.355。

</div>

该结果表明 PLVR 的程序搜索不必依赖很大的程序搜索训练集，并且在足够样本数后对训练样本顺序较稳定。不过，图中衡量的是领先等价类的搜索准确率与损失，而不是最终基准任务的泛化性能；因此它主要支持搜索收敛性，不能单独证明跨数据分布的鲁棒性。

<div class="result-source" markdown="1">

来源：图 2；实验章节 4.6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The band collapses onto the p* loss floor at n=70.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验摘录缺少表 2 的逐系统、逐领域结果以及完整置信区间，因此摘要中的平均优势可以引用，但无法核查不同基准领域、不同模型和不同运行之间的分布。
- PLVR 与后训练基线没有进行 FLOP 匹配，且程序由多个神经原语串联执行；作者报告令牌和参数组成但不报告延迟。因此结果不能直接推出训练计算效率或实际部署速度优于 RL，也不能排除复杂原语库带来的工程成本。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Vanilla prompting：仅将函数签名、对话历史和用户请求置于上下文中，作为不使用额外代理脚手架或后训练的性能下界。
- Token-matched agentic harness（RLM）：使用代理式迭代脚手架，并将推理令牌数调到与 PLVR 程序近似匹配，用于检验优势是否仅来自测试时计算量或任务分解框架。
- RL 后训练检查点：包括数据规模匹配的 DeepCoder-14B-Preview 与 Nemotron-Cascade-2-30B-A3B，以及参数规模匹配的 INTELLECT-3；这些是已发布模型，作者不自行重训，以避免因自行选择数据、超参数或停止点而低估基线。
- 较大规模或前沿模型的 vanilla prompting 与 token-matched agentic harness：不进行微调，用于检验 PLVR 是否能够超过参数量显著更大的通用模型；原文未明确报告该组所有模型的完整名称与逐项结果。

**实验想回答的问题**

- PLVR 在具有可验证中间步骤的代码生成与多轮工具调用任务上，是否比相同规模或相近训练预算的强化学习后训练方法更有效？
- PLVR 的性能优势主要来自类型约束搜索空间，还是来自通过符号反向传播获得的损失引导与逐步信用分配？

**实验实现**

所有实验臂运行 3 次；对 vanilla prompting、token-matched harness 和 PLVR，重复运行改变推理或搜索随机种子；已发布后训练检查点只能测量推理方差，不能被解释为训练方差。所有方法共享相同题目顺序和 $\tau^{2}$-Bench 用户模拟器种子，因此比较是配对的；主要置信区间对题目进行 bootstrap，而不是根据 3 次运行估计标准差。PLVR 的原语由 3B、8B 和 27B 基础模型分别微调，并在推理时驻留；总参数约为 57B，每次前向传播激活参数约为 3B–27B。作者报告输入、输出令牌、总参数和激活参数，但不进行 FLOP 匹配，也不报告延迟。程序搜索在训练集前缀上进行，并通过 109 个训练集排列评估收敛；预注册的随机采样对照保持相同的类型定向传播、最大深度 $d_{\max}$ 与可用性过滤，只替换损失引导评分，从而尽量隔离符号反向传播的作用。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 将损失引导的程序搜索替换为等预算的均匀随机采样 | 在保持相同类型可行空间与采样预算的情况下，均匀采样使中位程序得分从 65.6 降至 17.5。 | 该对照保留类型系统、最大深度和可用性过滤，因此主要改变的是搜索是否使用反向传播产生的损失引导。性能大幅下降支持作者关于“优势来自 backward pass 而非仅来自 type system”的解释；但它并未隔离原语质量、搜索候选表示或不同随机种子对结果的全部影响。 | 摘要；实验协议 4.7 的“Pre-registration”说明该随机采样零假设已预注册<br><span class="experiment-evidence">Replacing the loss guided search with uniform sampling over the same type admissible space at equal budget collapses the median program from 65.6 to 17.5, identifying the backward pass rather than the type system as the source of the advantage.</span> |
| 程序搜索训练集前缀长度与排列敏感性 | 未打乱运行在 $n=10$ 时达到最终准确率，但直到 $n=100$ 前领先的仍不是 $p^{*}$；在 $n=70$ 时，$p^{*}$ 在每一种排列下都处于领先等价类。 | 这一分析区分了“当前最高准确率已不再变化”和“真正目标程序已经被稳定识别”两个概念。少量样本可能足以得到表面上不再改进的分数，但需要更多样本才能让正确程序在不同训练顺序下都成为领先候选；因此它检验的是搜索选择的稳定性，而不是一个独立的模型组件。 | 图 1；实验章节 4.6<br><span class="experiment-evidence">The unshuffled run reaches its final accuracy at n=10 and does not move thereafter, but is leading with a program other than p* until n=100.</span> |

**定性案例**

- 原文摘录没有提供具体任务的程序轨迹、错误案例或定性可视化，因此无法在不臆测的情况下给出单个案例研究及其行为解释。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Presents a verifiable-reward post-training method that teaches LLMs to perform structured, inspectable reasoning programs.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`a5a69bb12a38817af8c24d4706b50fcb87619c73c29eafeb5898a75c37b87515`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
