---
title: "[论文解读] CordisBench: Can Language Models Reason About Component Lifecycles in Dynamic Agent Harnesses?"
description: "[arXiv 2609.01600][LLM 评测] CordisBench系统评测语言模型能否在没有符号工具或执行反馈的情况下，推断动态智能体运行框架中组件依赖、停用清理及清理顺序共同造成的状态变化。"
arxiv_id: "2609.01600"
announcement_date: "2026-09-02"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:40:05.342637+00:00"
source_sha256: "375f60b428a53653eae52bb5a2a960e48ff65254b4e8cf4c10eb977d16731949"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "动态智能体框架"
  - "组件生命周期"
  - "依赖传播"
  - "清理副作用"
  - "拆卸顺序"
  - "形式语义"
  - "Cordis"
  - "语言模型推理评测"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2609.01600</p>

# CordisBench: Can Language Models Reason About Component Lifecycles in Dynamic Agent Harnesses?

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Damien Sileo, Dimitri Kachler</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Univ. Lille, Inria, CNRS, Centrale Lille, UMR 9189 - CRIStAL, F-59000 Lille, France</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.01600v1) · [PDF 下载](https://arxiv.org/pdf/2609.01600v1) · **关键词** 动态智能体框架, 组件生命周期, 依赖传播, 清理副作用, 拆卸顺序, 形式语义, Cordis, 语言模型推理评测<br>
**代码**: [https://github.com/sileod/cordis-bench](https://github.com/sileod/cordis-bench) · **项目页**: [https://huggingface.co/datasets/sileod/cordis-bench](https://huggingface.co/datasets/sileod/cordis-bench)

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

CordisBench系统评测语言模型能否在没有符号工具或执行反馈的情况下，推断动态智能体运行框架中组件依赖、停用清理及清理顺序共同造成的状态变化。

**不用术语来说**：智能体可以在运行时安装、删除或重新配置插件，但一次看似局部的修改可能连带停用其他组件，并触发多个清理操作；如果这些清理会恢复各自启动时保存的旧值，那么执行顺序不同，最终状态也可能不同。问题在于，模型不仅要知道“哪些组件会受影响”，还要准确预判“操作完成后系统究竟变成什么样”，否则它提出的重配置方案可能无法达到目标，或删除不必要的组件。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出CordisBench：一个包含1200个结构化问题的生命周期推理基准，覆盖受影响组件定位、给定停用顺序下的最终状态预测、跨顺序的必然或可能条件判断，以及可执行重配置方案选择。
- 设计从2到32个相关交互的受控难度扩展，并结合形式化实例与可执行Cordis程序，使模型预测和重配置方案能够通过确定性评分、运行时执行及独立有限参考语义进行核验。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于动态智能体运行框架与程序生命周期推理的交叉领域。动态智能体框架允许语言模型在运行期间添加、移除或重新配置插件、服务、记忆策略和工具；因此，框架结构本身也成为持续变化的执行状态。以 Cordis 为例，运行时负责管理组件依赖、存活期和清理操作，但“正确执行请求”并不等于“执行后得到预期状态”：移除一个组件可能沿依赖关系停用其他组件，而多个组件的清理操作还可能因执行顺序不同而写回不同状态。CordisBench 专门评估模型在没有符号求解工具和执行反馈时，能否预先推断这些机械后果，并考察这种能力在相关交互数量由 2 增至 32 时如何变化。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**组件生命周期**

组件从启动、运行到停止和清理的完整过程。组件启动时可能读取或修改共享状态，停止时则执行清理逻辑，例如恢复启动时保存的旧值。

</div>
<div class="concept-item" markdown="1">

**依赖驱动的移除**

若组件依赖另一个组件，被依赖项停止后，依赖它的组件也可能必须停用。因此，一次局部变更可能传播为一组组件的级联移除。

</div>
<div class="concept-item" markdown="1">

**拆卸顺序**

拆卸顺序是多个组件停止并执行清理操作的合法先后次序。即使每个清理操作单独看都合理，不同顺序也可能产生不同的最终共享状态。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

CordisBench 将问题置于两类互补环境中：一类是受控的形式化系统，另一类是实际运行于 Cordis 的可执行程序。每个实例给出当前组件配置、依赖与生命周期效果，以及待执行的移除或重配置要求；模型必须输出结构化答案，包括识别受影响组件、预测指定拆卸顺序后的状态、判断某个条件是在所有合法顺序下成立还是仅在部分顺序下可达，以及选择能够保证目标状态的重配置方案。基准共含 1,200 个问题，并在保持题型和答案格式不变的情况下，将每题需要追踪的相关交互数设置为 2、4、8、16、24 或 32，以区分题目规模带来的组合推理难度。其核心假设是模型不能借助符号计算或运行时反馈，只能根据给定规则预判后果；在 Cordis 原生实例中，预测与操作方案可由真实执行检验。直观地说，模型不仅要知道“哪些插件会被关掉”，还要像手工执行程序一样按顺序追踪每次清理写回的值，并区分某结果是必然出现还是只在某些合法顺序中出现。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$C$**

当前运行或参与推理的组件集合；原文节选未给出统一的正式符号，此处仅用于概括问题设置。

</div>
<div class="notation-item" markdown="1">

**$\pi$**

一个合法的组件拆卸顺序；不同顺序可能产生不同最终状态。

</div>
<div class="notation-item" markdown="1">

**$s_0$**

生命周期变更和清理开始之前的初始共享状态。

</div>
<div class="notation-item" markdown="1">

**$s_{\pi}$**

按照拆卸顺序执行全部相关清理操作后得到的最终状态。

</div>

</div>

**直接相关的工作**

- **PLSemanticsBench**: 该基准评估语言模型能否充当给定操作语义的解释器，包括处理被修改的规则；它与 CordisBench 都考察基于形式规则的执行推理。区别在于 CordisBench 聚焦组件依赖、清理副作用及拆卸顺序共同决定的运行框架状态。
- **DeepSeek Harness**: DeepSeek Harness 提供语言模型构造和操作动态插件的具体应用背景，并由 Cordis 管理插件依赖、生命周期和清理。CordisBench 不评估完整框架演化带来的下游任务收益，而是隔离并测量执行这些插件操作前所需的生命周期后果推理。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

动态智能体运行框架允许模型按需增删插件、服务、记忆策略和工具，因此框架本身也成为持续变化的状态。组件之间存在依赖关系，停用组件还可能执行恢复旧值等清理逻辑；多个局部上合理的清理操作叠加后，可能因合法停用顺序不同而留下不同结果。若模型不能提前判断这些连锁后果，它就可能选择无法实现目标或代价过大的重配置操作，影响运行可靠性与推理成本。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **动态组件运行时管理**：以Cordis为代表的运行时负责维护组件依赖、生命周期和清理，并按请求实际执行添加、删除或重配置。它能忠实完成给定操作，但操作目标是否合理、执行后是否会得到预期状态，仍需要请求操作的模型事先判断。
- **显式形式语义与机械验证**：当依赖关系和清理效果可被明确表示时，可以用有限参考语义枚举或计算合法生命周期过程，直接求出最终状态，或在执行前验证方案。论文报告该参考语义与全部528道可执行问题中用于评分的Cordis观察结果和动作结果一致。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 仅由运行时正确执行请求并不能保证请求本身能达到目标：模型仍可能忽略依赖传播、清理副作用或顺序敏感性，从而选错干预对象，或者提前移除过多组件。
- 现有模型在小规模系统上的表现不能证明其可扩展性，而真实困难来自相关交互数量增加后对多重效果和不同停用顺序的持续追踪；此外，提高推理强度虽可能恢复部分可靠性，却会显著增加推理开销。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

在问题形式和输出格式保持不变时，尚缺少一个可控、可执行且可确定评分的基准，用来隔离并测量语言模型的生命周期推理能力如何随相关交互数量增长而变化，尤其缺少对“定位潜在影响”与“预测实际最终状态”、对指定顺序与跨所有可能顺序推理，以及对重配置方案实际成败的区分评估。

</div>
<div markdown="1"><span>核心问题</span>

当语言模型不能使用符号辅助或执行反馈、必须自行预判生命周期后果时，它能否可靠地识别受影响组件、预测给定停用顺序后的状态、判断哪些条件在全部或部分合法顺序下成立，并选择执行后确实达到目标的重配置；这种可靠性又如何随相关交互从2个增加到32个而变化？

</div>
<div markdown="1"><span>作者直觉</span>

作者把复杂度增长限定为“需要同时追踪的相关交互变多”，同时固定题型和答案格式，因此性能变化更可能反映生命周期组合推理本身，而不是题目表达方式改变。再用Cordis真实执行候选操作，并以独立有限语义交叉核验，就能把模型是否真正推对机械后果，与它是否只是给出表面合理答案区分开来；这种设计也可直接比较让模型投入更多推理与交给确定性分析工具两条路线的可靠性和成本。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CordisBench把动态组件系统中的生命周期变化转化为有限、可执行的推理问题。每个形式化实例明确给出组件、服务依赖、初始应用状态、激活与清理效果，以及待分析的生命周期变更；方法随后找出可能影响答案的合法生命周期延续，逐一执行到终止状态，并从所有终止观测中生成定位受影响组件、预测指定拆卸顺序后的状态、判断跨顺序必然或可能成立的条件、统计结果，以及选择可成功执行的重配置等参考答案。

关键难点不是普通的静态依赖追踪，而是清理操作之间可能相互干扰：组件离开时，其效果会恢复该效果启动时记录的状态，因此两个单独看来合理的效果若生命周期重叠，最终状态就可能取决于清理顺序。直观地说，这类似两个人先后保存同一份文档的旧版本，并在退出时各自恢复自己的备份；最后留下哪个版本取决于谁先退出、谁后退出。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造有限生命周期实例

将上述信息编码为一个有限的形式化系统，使组件何时可存在、移除提供者会影响哪些依赖者，以及组件离开时执行什么清理操作都具有明确语义。实例有意允许不满足Cordis全局恢复与合流保证所要求的独立性条件。

<div class="method-step__io" markdown="1">

**输入**：组件集合、组件之间的服务依赖、初始应用状态、各组件的激活效果与清理效果，以及一个待分析的生命周期变更。<br>
**输出**：一个可能包含依赖传播和清理干扰的、可枚举执行的Cordis生命周期实例。

</div>

**直观理解**：先搭建一个规模受控的插件系统，并明确每个插件依赖谁、启动时做什么、退出时撤销什么。部分实例故意让不同插件的撤销操作碰到同一状态，从而产生真正需要推演的顺序效应。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定受影响范围与合法延续

依据显式服务依赖传播生命周期影响，并枚举所有能够影响问题答案的合法后续执行；对于给定拆卸顺序的问题，则只沿指定顺序推进。枚举范围是有限的，因此可以覆盖相关的生命周期分支，而不依赖语言模型的近似判断。

<div class="method-step__io" markdown="1">

**输入**：形式化实例及指定的生命周期变更，例如移除某个服务提供组件或执行一次重配置。<br>
**输出**：受影响组件及其可能发生的激活、退出和清理事件序列。

</div>

**直观理解**：如果底层插件被移除，依赖它的上层插件也可能被迫退出；随后需要列出这些插件所有允许的退出次序。它相当于先画出会倒下的多米诺骨牌，再列出规则允许的倒下顺序。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行激活与清理语义

按照事件顺序执行组件效果：效果启动时记录其观察到的应用状态，效果停止时恢复该记录状态；不同组件的清理可能读写同一状态，因此必须保留严格的执行次序。每条延续均执行到完成，并记录终止观测和动作是否成功。

<div class="method-step__io" markdown="1">

**输入**：每一条合法生命周期事件序列、初始应用状态，以及各效果保存和恢复状态的规则。<br>
**输出**：每条合法延续对应的终止应用状态、存活组件、已执行清理及重配置成败等观测。

</div>

**直观理解**：不能只判断哪些插件会退出，还必须按顺序真正模拟每次撤销。后执行的恢复操作可能覆盖先前清理留下的状态，所以交换两个退出动作就可能改变结局。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 聚合终止观测并生成确定性答案

对终止观测进行任务特定聚合：直接读取受影响组件；为指定顺序返回对应终态；对全部延续取共同成立条件以回答“必然成立”；对至少一条延续检查条件以回答“可能成立”；同时可统计不同结果或验证候选重配置是否执行成功。所得结果作为确定性的参考答案和评分依据。

<div class="method-step__io" markdown="1">

**输入**：所有相关合法延续的终止观测，以及题目要求的答案类型。<br>
**输出**：定位、顺序状态预测、必然条件、可达条件、结果计数或可执行重配置选择等标准答案。

</div>

**直观理解**：同一组模拟结果可以回答不同问题：“每条路线都成立”对应保证，“至少一条路线成立”对应可达。这样评分建立在完整执行结果上，而不是依靠人工印象或另一个语言模型裁判。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。CordisBench是评测基准与有限参考语义，而不是通过某个损失函数训练的新模型；所给章节没有提出参数优化目标，也没有报告使用基准题目微调被测语言模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 显式组件依赖与生命周期语义**

Cordis组件可以声明其所需服务；当服务提供者离开时，依赖组件也可能被迫离开，并触发各自的清理效果。该语义把一次局部插件变化扩展为沿依赖关系传播的生命周期事件集合。

> 直观理解：它负责回答“改动会波及谁”。没有这一模块，系统只能看到被直接移除的插件，无法追踪依赖它的插件为何也必须退出。

**2. 状态保存—恢复型效果**

基准集中考察一种效果模式：效果启动时保存其观察到的应用状态，停止时恢复该状态。多个效果的生存期若重叠，其保存值与恢复次序可能不同，从而破坏顺序无关性；这些实例位于Cordis全局恢复和合流定理所需独立性条件之外。

> 直观理解：每个插件都像在启动时拍一张状态快照，退出时把系统恢复到自己的快照。多个插件拿着不同时刻的快照依次恢复时，最后状态自然可能由退出顺序决定。

**3. 有限参考语义**

由于生成系统有限，参考程序枚举所有会影响答案的合法生命周期延续，并将每条延续执行到完成。终止观测被用于精确生成定位、顺序预测、全称条件、存在条件和结果计数答案；论文摘要还说明，该独立参考语义与Cordis真实执行在全部用于评分的观测和动作结果上保持一致。

> 直观理解：它相当于一个穷举式标准答案生成器：把所有规则允许且相关的路线都走完，再根据完整结果判题。其作用是避免让待评测模型或人工启发式方法自行决定什么答案正确。

**训练与推理**

参考答案生成阶段先读取有限形式化实例，依据Cordis依赖与生命周期规则枚举相关合法延续，再逐条执行至终止并聚合观测。模型推理阶段则接收由这些实例形成的问题，输出受影响组件、指定拆卸顺序下的最终状态、跨顺序必然或可能成立的条件、结果计数，或应选择的可执行重配置；评分采用任务特定的确定性规则，而不是生成式裁判。论文摘要说明评测覆盖不同数量的相关交互，并比较较低与额外推理强度，但所给方法章节未明确披露完整提示模板、输出解析流程或各模型的解码参数。

**复现信息**

复现所必需的核心是同时实现两条相互独立的路径：一条在Cordis运行时中实际执行程序，另一条使用有限参考语义枚举并模拟合法生命周期延续。形式化实例必须包含组件、依赖、初始状态、激活和清理效果及目标生命周期变化；执行器必须保留清理的先后顺序，不能把清理操作当作可交换操作。论文摘要称参考语义在全部528个可执行问题上，与Cordis执行用于评分的每个观测和动作结果一致；但当前节选没有进一步给出枚举算法的数据结构、剪枝策略、运行时版本或硬件配置，因此这些细节需结合论文其余章节及公开代码核验。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Formal 设置：由 $240$ 个独立生成系统构造，使用有限形式语义描述固定宽度的模 $m$ 整数状态向量、组件依赖和算术效果；共 $672$ 道题，包括 $192$ 道规模为 $2/4$ 的题和 $480$ 道规模为 $8/16/24/32$ 的题，用于测试可控的生命周期推理。
- Cordis-native 设置：将相同的生命周期模式编译为 Cordis 插件，并在 Cordis 4.0.0-rc.7 上执行；共 $528$ 道题，包括 $240$ 道规模为 $2/4$ 的题和 $288$ 道规模为 $8/16/24/32$ 的题，用于测试真实运行时中的依赖解析、清理和重配置。
- 规模与诊断子集：完整基准包含 $1,200$ 道结构化输出题，其中 $1,056$ 道为主要任务、$144$ 道为终态数量诊断；另有平衡的 $78$ 题、$16$ 交互推理预算子集，以及固定为两个拆卸顺序的 $240$ 题诊断子集，用于区分规模、顺序数量、输出截断和推理预算的影响。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Jaccard 相似度**

用于定位任务和保证/可达条件集合，衡量模型输出集合与标准集合的交并比；它比整集合精确匹配更能反映部分正确。 （越高越好，因为更接近完整且准确的目标集合；条件任务中的 $50\%$ 还可与 return-all-conditions 基线比较。）

</div>
<div class="metric-item" markdown="1">

**per-observable accuracy**

用于指定拆卸顺序后的状态预测，逐个应用可见观测量判断是否正确，再计算观测量层面的准确率；它测试模型是否正确追踪状态变化，而不把长答案的整体匹配失败全部视为同一种错误。 （越高越好，表示更多应用可见状态被正确预测。）

</div>
<div class="metric-item" markdown="1">

**executed success**

用于重配置：将模型提出的预先处置依赖集合实际执行，只有同时达到目标、保留无关应用状态并使用最少处置次数才算成功。 （越高越好；该指标比静态答案匹配严格，因为它同时检验动作有效性和最小性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 主基准的规模扩展：定位、终态预测与跨拆卸顺序推理

<div class="result-value" markdown="1">

模型通常能处理小规模系统，但交互数量增加后，定位性能下降较慢，而最终状态预测和条件集合推理下降更明显。GPT-5.6 Luna 的 Formal reachable-condition Jaccard 从 $91.7\%$ 降至 $14.1\%$，Cordis-native executed reconfiguration success 从 $62.5\%$ 降至 $25.0\%$；其所有主要回答均成功解析，因此这些下降主要反映推理错误而非格式失败。DeepSeek V4 Flash 的 Formal prediction accuracy 从 $81.2\%$ 降至 $57.7\%$。

</div>

结果支持“模型能找到可能受影响的组件，却难以把这些影响正确传播到终态并跨多个拆卸顺序求交/求并”的解释。但不同任务使用不同指标，绝对分数不能直接横向比较；此外，下降本身不证明错误全部来自依赖跟踪，也可能包含算术状态追踪和组合规模增长的影响。

<div class="result-source" markdown="1">

来源：Section 5.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GPT-5.6 Luna shows the clearest separation between identifying affected components and reasoning through their consequences: localization stays near ceiling, while formal reachable-condition Jaccard falls from 91.7% to 14.1% and Cordis-native executed reconfiguration success from 62.5% to 25.0%. All of its primary responses parse, so these drops reflect incorrect answers rather than formatting failures.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 重配置执行与最小性检查

<div class="result-value" markdown="1">

在 $16$ 交互的 $96$ 道重配置题上，Gemini 3.7 Flash 成功 $92/96$，其中 $2$ 道目标失败、$2$ 道格式错误；GPT-5.6 Luna 达到目标 $67/96$，但其中 $11$ 个方案处置过多，最终有 $56$ 个最小成功；DeepSeek V4 Flash 达到目标 $33/96$，其中 $32$ 个非最小，最终只有 $1$ 个最小成功。GPT-5.6 Luna 和 DeepSeek V4 Flash 的目标达成率与基准成功率分别相差 $11.5$ 和 $33.3$ 个百分点。

</div>

执行评测揭示了静态答案匹配看不到的决策差异：模型可能知道如何让目标成立，却为了保险而删除不必要的依赖。对该基准而言，这仍然是失败，因为研究问题要求最少的预先处置；因此“达到目标”不能等同于“提出正确重配置”。

<div class="result-source" markdown="1">

来源：Section 5.4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Gemini 3.7 Flash succeeds on 92 of 96 questions, with two target failures and two malformed answers.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 参考语义与 Cordis 执行的一致性

<div class="result-value" markdown="1">

有限参考语义与 Cordis 执行在全部 $528$ 道 Cordis-native 题上，对评分所用的每个观测结果和动作结果都完全一致。

</div>

这说明在论文覆盖的受控实例和 Cordis 版本中，实验标签可以由独立有限语义可靠复算，模型性能下降不太可能是参考答案与运行时实现不一致造成的。它只证明这些受控生命周期模式上的一致性，不能自动推广到未覆盖的真实代理框架、并发行为或更复杂运行时特性。

<div class="result-source" markdown="1">

来源：Section 5.3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For all 528 Cordis-native questions, the finite reference semantics and Cordis execution agree on every observation and action outcome used for scoring.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 基准主要是受控、独立生成的有限生命周期模式；虽然 Cordis-native 题目实际运行于 Cordis 4.0.0-rc.7，但结果不能直接代表具有并发、外部副作用、异常处理或更复杂资源语义的真实代理框架。
- 不同任务采用不同主指标，且交互规模增加会使整答案精确匹配天然更严格；论文用 Jaccard、逐观测准确率和执行成功率缓解这一问题，但任务之间仍不能依据绝对分数直接排序。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 快捷方式控制：忽略系统语义，仅利用任务身份、交互数量、提示长度、题目位置或与示例的词汇相似度；它检验模型是否可以靠表面线索答题，而非进行生命周期推理。
- 条件任务的 return-all-conditions 基线：返回所有条件。由于每道条件题包含数量相等的真、假条件，该策略的 Jaccard 相似度恰为 $50\%$；它用于判断模型曲线是否只是保守地输出全部标签。
- 有限参考语义：独立于 Cordis 实现，根据依赖和效果结构计算终态及动作结果；它不是与模型竞争的预测基线，而是验证可执行设置标签是否正确、是否存在运行时实现偏差的参考。
- 文本答案与执行结果对照：重配置答案不仅与参考答案比较，还被翻译为 Cordis 的 $dispose(...)$ 操作并执行；该对照区分达到目标但非最小的方案、目标失败、格式错误和非法动作。

**实验想回答的问题**

- 随着相关生命周期交互数量从 $2$ 增加到 $32$，模型在组件定位、指定拆卸顺序后的状态预测、跨顺序条件推理和可执行重配置上的可靠性如何变化？
- 额外推理预算是否能改善生命周期推理，以及这种收益是否足以抵消额外的推理成本？

**实验实现**

评估 Gemini 3.7 Flash、GPT-5.6 Luna 和 DeepSeek V4 Flash (0731)，温度为 $0$，默认低推理强度，输出上限为 $8,192$ 个 token；每道题只生成一次答案，不使用工具或执行反馈，仅在没有返回时重试。解析失败或格式错误记为 $0$。主要指标排除 $144$ 道终态数量诊断；同一生成系统派生的题目存在相关性，因此 Figure 3 使用按系统聚类 bootstrap 的 $95\%$ 区间，并为每个任务和交互规模生成三个独立复本。规模比较在固定任务和设置内进行：Formal 中一次交互表示一个共同影响相邻状态项的 effect group，Cordis-native 中一次交互表示一个清理可能改变观测槽的 dependent。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 推理强度消融：平衡的 $16$ 交互、$78$ 题子集 | 将 GPT-5.6 Luna 从无推理提高到默认 medium 后，Cordis-native prediction 从 $31.2\%$ 升至 $85.4\%$，executed reconfiguration 从 $0\%$ 升至 $50\%$；medium 下平均每题使用 $2,967$ 个推理 token。 | 该消融直接测试额外内部推理是否能恢复生命周期计算能力。收益很大，但并非所有重配置题都被解决，而且每题近三千个推理 token 会增加代理运行的延迟和计算成本，因此“更强推理”是有效但昂贵的补救，而不是低成本替代方案。 | Section 5.2<br><span class="experiment-evidence">From no reasoning to the default medium setting, Cordis-native prediction rises from 31.2% to 85.4%, and executed reconfiguration from 0% to 50%.</span> |
| 控制输出截断与拆卸顺序数量的诊断 | Gemini 有 $29$ 个回答触及 $8,192$ token 上限；改用 $32,768$ token 后，这些回答全部完成并解析，Formal guaranteed-condition Jaccard 从 $20.2\%$ 升至 $71.2\%$，reachable-condition 从 $31.1\%$ 升至 $45.0\%$，prediction accuracy 从 $79.8\%$ 升至 $84.0\%。另一方面，在始终只有两个拆卸顺序的 $240$ 题诊断中，GPT-5.6 Luna 的 guaranteed-condition Jaccard 仍从规模 $8$ 的 $81.2\%$ 降至规模 $32$ 的 $64.4\%$，reachable-condition 从 $91.1\%$ 降至 $69.7\%$。 | 输出上限确实解释了 Gemini 保证条件分数下降的很大部分，但不能解释其剩余的可达条件下降，也不能解释已完全解析的 GPT-5.6 Luna 的趋势。固定顺序数量后 GPT-5.6 Luna 仍随交互规模退化，说明困难不只是候选拆卸顺序变多，还来自需要追踪的依赖和状态交互增加。 | Section 5.1, Output-limit diagnostic<br><span class="experiment-evidence">The token limit therefore explains much of the drop in Gemini’s guaranteed-condition score.</span> |

**定性案例**

- Figure 2 的 Cordis-native 重配置例子展示了为何最小处置集合需要理解清理时保存的状态：槽位 $S$ 初始为 $488151$，依赖 $A$ 启动时写入 $36000$、依赖 $B$ 随后写入 $934261$，每个插件清理时恢复其启动时捕获的值；当提供者 $P$ 被处置且顺序可能为 $A\rightarrow B$ 或 $B\rightarrow A$ 时，预先处置 $B$ 即可在两种顺序下恢复 $S$ 到 $488151$，参考答案为 $["B"]$。该例说明模型不能只看最后一次写入，还必须判断哪个依赖的清理会干扰目标以及何时应先移除它。
- evidence_quote_source_location_note:

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出并使用 CordisBench 评测语言模型在动态智能体运行时中的组件生命周期与依赖推理能力。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`375f60b428a53653eae52bb5a2a960e48ff65254b4e8cf4c10eb977d16731949`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
