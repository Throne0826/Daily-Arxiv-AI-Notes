---
title: "[论文解读] Route-Align-Verify for Functional Correctness in Code Generation"
description: "[arXiv 2608.03341][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.03341"
announcement_date: "2026-08-05"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:40:51.629637+00:00"
source_sha256: "cd5dc69e233854841f982c9115047679e134444cbcc8edd15d1f9bf304974ce0"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "代码生成"
  - "功能正确性"
  - "MBPP"
  - "任务感知提示路由"
  - "训练—推理提示对齐"
  - "LoRA"
  - "执行式验证"
  - "多候选选择"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.03341</p>

# Route-Align-Verify for Functional Correctness in Code Generation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Erxue Zhou, Jingxiang Meng, Aofan Liu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Erxue Zhou is with the Software Engineering Institute, East China Normal University, Shanghai 200062, China；University of Chicago；Peking University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03341v1) · [PDF 下载](https://arxiv.org/pdf/2608.03341v1) · **关键词** 代码生成, 功能正确性, MBPP, 任务感知提示路由, 训练—推理提示对齐, LoRA, 执行式验证, 多候选选择<br>


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

本文属于大语言模型代码生成与执行式评测领域：模型根据自然语言题目、文档字符串或不完整实现生成可执行程序，系统质量主要由程序能否通过测试来判断，而非代码在文本层面是否合理。论文聚焦 MBPP 的短 Python 编程任务，并将提升功能正确性视为一个贯穿提示构造、参数高效适配和测试时选择的系统问题；其目标不是设计新骨干网络或新基准，而是在固定骨干模型下提高最终输出的 $\mathrm{pass@1}$。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**功能正确性与执行式评测**

功能正确性指生成程序是否真正实现题目要求，通常通过运行测试用例判断。执行式评测比文本相似度或表面合理性更直接，但结论会受到测试覆盖率影响：测试不足可能让存在隐藏缺陷的程序被误判为正确。

</div>
<div class="concept-item" markdown="1">

**LoRA 参数高效适配**

LoRA 冻结骨干模型的大部分预训练参数，仅学习低秩增量，以较低训练和存储成本让模型适应下游任务。本文并未提出新的 LoRA 算法，而是用它学习与测试时路由提示风格相匹配的适配器，从而减少训练提示和推理提示之间的分布不一致。

</div>
<div class="concept-item" markdown="1">

**多候选生成与执行验证**

同一模型对同一题目采样多个候选程序，因为正确答案可能没有出现在第一次生成中。随后运行 MBPP 提供的可见公开测试并据此选择最终程序，使候选集合中已有的正确解更可能成为系统输出。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一道异质的自然语言编程任务及其可见公开测试，任务可能涉及字符串处理、算术推理或复杂边界情况；输出是一个应满足题意并通过测试的 Python 程序。论文假设骨干大语言模型保持固定，通过 RAV 的三个环节改善系统行为：先根据任务特征选择提示方式，再使用与该推理提示风格对齐的 LoRA 适配器生成多个候选，最后执行候选并依据公开测试结果选出单个最终答案。评测在 MBPP Sanitized 与 MBPP Full 两种设置下进行，核心目标是提高 $\mathrm{pass@1}$；这里的“单个最终答案”是经过候选选择后的系统输出，不等同于只调用模型采样一次。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入的自然语言编程任务，可包含题目描述、文档字符串或部分实现。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{C}(x)=\{c_1,\ldots,c_K\}$**

针对任务生成的候选程序集合，其中 $c_i$ 是第 $i$ 个候选，$K$ 是候选数量；这是为解释论文问题设置而采用的概括性记号，原文节选未给出正式符号定义。

</div>
<div class="notation-item" markdown="1">

**$T_{\mathrm{pub}}$**

MBPP 中用于验证候选程序的可见公开测试集合；这是概括性记号，原文节选未正式定义该符号。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{pass@1}$**

系统为每道题提交一个最终程序时，该程序通过评测测试的比例；本文关注经过 RAV 选择后的最终输出表现。

</div>

</div>

**直接相关的工作**

- **CodeT**: CodeT 使用测试对模型生成的程序进行重排序，是 RAV 的 Verify 阶段最直接的相关方向之一。区别在于，RAV 不额外生成测试，而是使用 MBPP 已有的可见公开测试，并把执行选择与任务感知提示路由、训练—推理提示对齐联合研究。
- **LoRA**: LoRA 为冻结骨干权重、仅学习低秩更新的参数高效适配方法。RAV 直接采用该机制，但研究重点不是改进 LoRA 本身，而是让适配训练所用提示更接近测试时的路由提示，以降低提示不匹配造成的性能损失。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

代码生成系统的可靠性最终取决于程序能否通过测试、实现题目要求，而不只是代码表面上是否合理。面对字符串处理、算术推理和边界条件密集等异质任务，固定提示方式未必都合适；同时，模型即使具备生成正确程序的能力，正确答案也不一定出现在第一次采样中。因此，仅依靠固定骨干模型的一次直接生成，难以稳定获得较高的功能正确性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **代码专用训练与参数高效适配**：WizardCoder、Magicoder、StarCoder 和 Code Llama 等方法通过代码预训练或指令微调，使模型行为更贴近下游编程任务；LoRA 则只训练少量低秩参数，以较低成本完成模型适配。
- **执行感知的多候选生成与筛选**：CodeT、Self-Debug 和 AlphaCode 一类方法生成多个候选程序，再利用测试执行结果、调试反馈或过滤规则选择更可能正确的输出，从而挖掘一次采样未能体现的模型能力。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单一通用提示无法适应不同任务的结构与失败模式；此外，如果微调阶段的指令形式与推理阶段实际使用的提示不一致，训练得到的专门化能力可能无法充分迁移到测试任务。
- 已有研究大多分别考察提示设计、模型适配或执行筛选，缺少对三者协同关系的系统研究；因此，即使某个环节改善了候选程序的整体质量，也未必能把这种改善稳定转化为最终输出的功能正确性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚不清楚在不改变骨干模型架构的条件下，能否把任务感知提示、训练—推理提示对齐和轻量级执行验证组织成统一流水线，以及这些组件是否必须协同使用才能产生明显收益。尤其缺少证据说明：路由与对齐对候选池的潜在改善，能否通过验证阶段转化为更高的最终 $pass@1$。

</div>
<div markdown="1"><span>核心问题</span>

对于固定骨干模型，联合优化“如何针对任务构造提示”“如何使 LoRA 微调提示与测试提示保持一致”以及“如何借助公开测试从多个候选中选出最终程序”，是否能够比单一提示、单独适配或一次直接生成更有效地提高代码生成的功能正确性？

</div>
<div markdown="1"><span>作者直觉</span>

三阶段分别处理不同误差来源：Route 让不同类型的任务获得更合适的提问方式，Align 使模型训练时看到的指令形式更接近实际推理输入，Verify 则通过运行可见公开测试，从多个候选中挑选更可信的程序。直观地说，前两步负责让“备选答案池里更容易出现正确程序”，最后一步负责把这一潜在优势转化为最终选择，而不是把成败押在第一次生成上。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

RAV（Route-Align-Verify）是在固定主干模型上依次干预提示、适配和输出选择的模块化代码生成框架。输入是包含自然语言描述、函数签名、文档字符串及可见公共测试的编程任务 $x$；Route 根据任务线索将其改写为路由提示 $p$，带可选对齐 LoRA 适配器的生成器从该提示采样候选集 $\mathcal{C}(x)$，Verify 再执行候选并返回公共测试得分最高的程序 $\hat{c}$。框架不修改 Qwen2.5-Coder-7B-Instruct 的主干结构，主要额外成本来自多候选生成和测试执行。

三个阶段具有明确的协同关系：Align 在训练时把监督样本改写成接近 Route 推理提示的形式，使模型学到的输入分布与实际使用方式一致；Route 在推理前选择更适合任务类型的提示模板；Verify 利用可见公共测试从多个候选中筛选最终答案。通俗地说，系统先为不同题型选择合适的“答题说明”，再让模型提前适应这种说明，最后像运行单元测试一样比较若干答案，而不是盲目提交第一次生成的代码。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造对齐训练数据

使用训练时重写规则 $R_{\mathrm{train}}(\cdot)$ 将每个 $x_i$ 改写为接近推理阶段路由提示的形式，并保持参考程序 $y_i$ 不变，得到 $D'$。

<div class="method-step__io" markdown="1">

**输入**：原始监督训练集 $D=\{(x_i,y_i)\}_{i=1}^{N}$，其中 $x_i$ 是训练任务，$y_i$ 是参考程序。<br>
**输出**：提示风格对齐的数据集 $D'=\{(R_{\mathrm{train}}(x_i),y_i)\}_{i=1}^{N}$。

</div>

**直观理解**：模型训练时见到的题目格式应与考试时一致；否则即使学过正确程序，也可能因提示写法变化而不能稳定调用所学能力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 训练对齐 LoRA 适配器

冻结主干权重，只学习低秩更新矩阵构成的 LoRA 适配器 $A$；论文将该过程描述为参数高效的监督微调，但未在所给章节中明确写出逐词损失函数。

<div class="method-step__io" markdown="1">

**输入**：固定的 Qwen2.5-Coder-7B-Instruct 主干模型 $M$ 与对齐数据集 $D'$。<br>
**输出**：与路由式提示相匹配的生成器 $G_{\mathrm{align}}(p)=G(M;A,p)$。

</div>

**直观理解**：LoRA 类似在不重写整本“模型知识”的情况下加上一组小型校正参数，使模型更习惯后续实际使用的提示风格。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 任务感知提示路由

启发式路由器 $\rho(x)$ 根据关键词和任务结构选择模板索引 $r$，再由 $R_{\mathrm{test}}(x;r)$ 形成提示 $p$；模板包括字符串、算法或数学、边界情况以及默认类型。

<div class="method-step__io" markdown="1">

**输入**：待求解任务 $x$，包括题目文字、函数接口、文档字符串和可能提供的公共测试。<br>
**输出**：供代码模型使用的路由提示 $p=R_{\mathrm{test}}(x;r)$。

</div>

**直观理解**：路由器不负责解题，只判断题目更像字符串处理、数学算法还是边界条件题，并选择相应的答题提醒。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 多候选生成与执行验证

生成器采样候选集 $\mathcal{C}(x)=\{c_1,\ldots,c_n\}$；启用 Verify 时逐一执行公共测试并选取通过数最多的候选，得分并列时优先选择较短代码。关闭 Verify 时无论是否生成多个样本都直接返回 $c_1$，不能解释为 best-of-$n$。

<div class="method-step__io" markdown="1">

**输入**：路由提示 $p$、主干模型 $M$、可选适配器 $A$、候选数量 $n$ 和任务的公共测试集 $T(x)$。<br>
**输出**：单个最终提交程序 $\hat{c}$，供基准隐藏评测判断功能正确性。

</div>

**直观理解**：系统像先写出多份草稿，再用题目公开的样例测试筛选；若关闭验证，则其余草稿不会参与最终决策。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 训练提示对齐数据构造

$$
D^{\prime}=\left\{\left(R_{\mathrm{train}}(x_i),y_i\right)\right\}_{i=1}^{N}
$$

**符号说明**

- $D^{\prime}$：用于训练对齐 LoRA 适配器的提示重写后监督数据集。
- $R_{\mathrm{train}}$：训练阶段的提示重写规则，其目标是近似推理阶段的路由提示风格。
- $x_i$：第 i 个原始训练任务输入。
- $y_i$：与第 i 个训练任务对应的参考程序。
- $N$：监督训练样本总数。

<div class="equation-explanation" markdown="1">

**直观理解**：该式只改变模型看到的输入表达，不改变监督目标程序。它把训练提示与 Route 在测试时生成的提示拉到相近分布，从而降低训练—推理提示失配。<br>
**原文位置**：式（8），第 III-E 节“Align: Training–Inference Prompt Alignment”

</div>

</div>

<div class="equation-block" markdown="1">

#### 公共测试评分与最终候选选择

$$
V(c_i,x)=\sum_{t\in T(x)}\mathbf{1}\!\left[c_i\text{ passes }t\right],\qquad \hat{c}=\arg\max_{c_i\in\mathcal{C}(x)}V(c_i,x)
$$

**符号说明**

- $x$：当前待求解的编程任务。
- $c_i$：生成器采样的第 i 个候选程序。
- $\mathcal{C}(x)$：针对任务 x 生成的全部候选程序集合。
- $T(x)$：任务 x 附带的可见公共测试集合。
- $t$：公共测试集合中的一个测试。
- $\mathbf{1}[\cdot]$：指示函数；条件成立时取 1，否则取 0。
- $V(c_i,x)$：候选程序 $c_i$ 在任务 x 的公共测试上通过的测试数量。
- $\hat{c}$：验证后返回的最终程序；最高分并列时优先选择较短代码。

<div class="equation-explanation" markdown="1">

**直观理解**：验证器先数出每个候选通过了多少项公开测试，再选择通过数最多者。该规则把程序的实际运行行为用于最终决策，比仅依赖生成顺序或模型置信度更贴近功能正确性，但仍可能对未被公开测试覆盖的错误失察。<br>
**原文位置**：式（10）和式（11），第 III-F 节“Verify: Execution-Based Candidate Selection”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文所给方法章节明确说明采用参数高效监督微调：冻结主干模型 $M$，仅在重写后的配对数据 $D'$ 上学习 LoRA 适配器 $A$，从而使参考程序 $y_i$ 与路由式输入 $R_{\mathrm{train}}(x_i)$ 建立对应关系。所给原文没有明确报告训练损失的数学表达、标签掩码方式或是否只对答案 token 计算损失，因此不能据此补写具体交叉熵目标；可确定的优化对象仅是 LoRA 的低秩参数，而非完整主干权重。Verify 的公共测试得分用于推理阶段排序，不参与文中所述 LoRA 梯度训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Route：任务感知提示路由**

路由器使用词法及任务结构线索，把 MBPP 任务分派至 $\text{string\_relaxed}$、$\text{algo\_relaxed}$、$\text{edge\_relaxed}$ 或 $\text{default}$ 提示。字符串关键词如 palindrome、substring，算术线索如 prime、gcd；明确边界提示或测试描述较密集时使用边界模板。

> 直观理解：单一通用提示难以同时突出字符串约束、数学推理和特殊输入。轻量路由以很低成本为模型补充与题型相关的注意事项，但它只是规则选择器，不会自行生成程序或证明正确性。

**2. Align：训练—推理提示对齐**

Align 将训练输入通过 $R_{\mathrm{train}}(\cdot)$ 重写为近似推理路由提示的形式，再用这些样本训练 LoRA 适配器 $A$。主干模型 $M$ 保持冻结，因此基础生成器为 $G(M;\varnothing,p)$，对齐生成器为 $G(M;A,p)$。

> 直观理解：该模块解决的不是模型规模不足，而是训练时与推理时“题目说法”不一致。对齐后，Route 给出的提示更接近适配器训练中见过的输入，也更可能产生可供验证器筛选的高质量候选。

**3. Verify：基于执行的候选选择**

Verify 对每个候选 $c_i$ 执行任务 $x$ 附带的所有可见公共测试 $T(x)$，以通过测试的数量作为 $V(c_i,x)$，再返回得分最大的候选；并列时采用偏好较短代码的弱简洁性先验。

> 直观理解：语言模型自身给出的概率并不等同于程序正确性，而实际执行能直接暴露语法、接口或样例行为错误。不过公共测试通常不覆盖全部输入，因此此模块只是更可靠的筛选信号，并不构成功能正确性的完整证明。

**训练与推理**

训练阶段先从原监督数据 $D$ 出发，用 $R_{\mathrm{train}}(\cdot)$ 将输入统一改写成接近推理路由的风格，再在冻结的 Qwen2.5-Coder-7B-Instruct 上训练 LoRA 适配器 $A$。这一步产生可插拔的对齐生成器；Route 和 Verify 本身没有被描述为需要学习参数，前者采用启发式规则，后者采用确定性的测试执行计分。

推理阶段首先由 $r=\rho(x)$ 决定提示类别，并构造 $p=R_{\mathrm{test}}(x;r)$；随后生成器 $G(M;A,p)$ 采样 $n$ 个候选。启用 Verify 时，系统在隔离执行环境中以公共测试通过数排序并返回 $\hat{c}$；关闭时固定返回首个候选 $c_1$。因而 RAV 的改进来源应解释为提示选择、适配分布和候选筛选三处联合干预，而不是主干架构变化；其推理复杂度由论文概括为生成成本随 $n$ 线性增加，开启验证后还需承担每个候选的测试执行成本。

**复现信息**

主干模型固定为 Qwen2.5-Coder-7B-Instruct。主实验的对齐 LoRA 使用秩 16、目标设为 all、截断长度 1024、最多 12000 个样本、学习率 $8\times10^{-5}$、训练 1 个 epoch、余弦调度和 bf16 精度；这些配置是复现适配阶段及公平比较基础模型与适配模型所需的关键信息。路由依据关键词、文档字符串和测试描述密度选择四类模板，验证则直接使用 MBPP 已提供的可见公共测试。

解释结果时必须保留两项实现语义：第一，设置 $n>1$ 但关闭 Verify 只是多次采样后返回第一份程序，并非从多个候选中事后挑选最佳答案；第二，启用验证时若公共测试得分相同，系统偏好较短代码。所给章节没有明确报告采样温度、top-p、确切候选数 $n$、随机种子、执行超时、安全沙箱或 LoRA 的具体目标层含义，因此这些内容仍需查阅完整论文或代码后才能完成严格复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MBPP Sanitized：MBPP 的清洗评测设置，用于降低题目或测试中的潜在噪声并评估程序功能正确性；原文未明确报告本设置的任务规模。
- MBPP Full：MBPP 的完整评测设置，用于检验方法在更全面题目集合上的表现；原文未明确报告任务规模。稳健性分析另从该设置抽取 120 个任务并重复运行三次。
- 训练数据—MBPP 配对集合：仅用于污染检查。作者比较每个训练样本与基准实例的 token 集合，检测完全重合以及 Jaccard 相似度不低于 $0.8$ 的近重复，而不是用它衡量代码正确性。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**pass@1**

最终返回的单个程序通过基准测试的任务比例，直接衡量系统交付结果的功能正确性。这里评估的是整个生成与选择流程的最终输出，而不只是候选池中是否曾出现正确程序。 （越高越好，因为更高数值表示更多任务的最终返回程序通过测试。）

</div>
<div class="metric-item" markdown="1">

**相对 Base 的绝对 pass@1 增量**

配置的 pass@1 与 Base 的 pass@1 之差，以百分点表示；它用于量化组件组合相对固定骨干模型带来的实际提升，而非相对百分比增长。 （正值且越大越好，因为它表示相较 Base 通过测试的任务比例提高得更多。）

</div>
<div class="metric-item" markdown="1">

**token-set Jaccard 相似度**

对训练样本与基准实例的 token 集合计算交集大小除以并集大小；作者同时检查完全重合及 $J\geq0.8$ 的模糊重合，以评估提示级泄漏或近重复污染风险。 （用于污染检测时越低越好；高相似度配对越少，越不支持性能提升来自训练—测试近重复这一解释。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 完整 RAV 在 MBPP Sanitized 与 MBPP Full 上的最终功能正确性

<div class="result-value" markdown="1">

Full RAV 的 pass@1 在 MBPP Sanitized 上为 $0.8911$，在 MBPP Full 上为 $0.8520$，均为所评估配置中的最高值。

</div>

该结果表明，在相同骨干模型下，把任务路由、对齐适配和执行验证串成完整流程，比论文评测矩阵中的其他组件组合更可能返回通过测试的程序。它证明的是 MBPP 及当前配置范围内的最终输出改善；由于没有与其他骨干模型、其他代码基准或更广泛外部系统比较，不能据此断言 RAV 对所有代码生成任务都最优。

<div class="result-source" markdown="1">

来源：Section IV-B, Table III

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The full RAV pipeline achieves the best performance on both MBPP settings, reaching 0.8911 on MBPP Sanitized and 0.8520 on MBPP Full.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Full RAV 相对未增强骨干模型 Base 的净提升

<div class="result-value" markdown="1">

相较 Base，Full RAV 在 MBPP Sanitized 上提高 $6.35$ 个百分点，在 MBPP Full 上提高 $9.92$ 个百分点；对应表中数值分别由 $0.8276$ 升至 $0.8911$、由 $0.7528$ 升至 $0.8520$。

</div>

绝对百分点增量说明完整流程不仅略微改变得分，而且在 MBPP Full 上产生接近十个百分点的实际改善。由于 Full RAV 同时启用了三个组件，这个比较支持整个系统有效，却不能单独确定每个组件的因果贡献；组件作用需要结合部分消融解释。

<div class="result-source" markdown="1">

来源：Section IV-B, Table III

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with the base model, Full RAV improves pass@1 by 6.35 points on MBPP Sanitized and by 9.92 points on MBPP Full.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 重复子集稳健性与训练—评测污染检查

<div class="result-value" markdown="1">

在三次 120 题子集重复实验中，MBPP Full 的提升之 95% 置信区间为 $[0.0250,0.1417]$，完全高于零；MBPP Sanitized 的区间为 $[-0.0194,0.0722]$，跨越零。污染分析中，训练—基准配对的完全重合数以及满足 $J\geq0.8$ 的模糊重合数均为零。

</div>

MBPP Full 的区间支持提升在这些重复子集上较稳定，而 Sanitized 的区间跨零，意味着现有重复实验不足以排除无提升或轻微负效应。零重合结果削弱了“训练数据直接包含相同或高度相似题目”这一解释，但 token 集合 Jaccard 只能检测特定形式的文本近重复，不能排除语义改写、骨干模型预训练污染或测试用例泄漏。

<div class="result-source" markdown="1">

来源：Sections IV-C and IV-D

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the MBPP Full split, the observed improvement remained stable, with a 95% confidence interval of [0.0250,0.1417]. On the MBPP Sanitized split, the trend remained positive, with a 95% confidence interval of [-0.0194,0.0722], although it crossed zero. Across all training–benchmark pairs, both exact overlap and fuzzy overlap with J≥0.8 remained zero.

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

- Base：不使用 Route、Align 或 Verify 的原始 Qwen2.5-Coder-7B-Instruct，是判断完整框架相对固定骨干模型是否带来净收益的核心参照。
- Route + Verify：使用任务感知提示路由和执行验证，但不使用对齐 LoRA；用于观察经过路由形成的候选池能否被验证阶段有效利用。
- Align + Verify：使用对齐 LoRA 和执行验证，但不使用路由；用于检验减少微调提示与推理提示失配后，候选池是否更利于执行筛选。
- Route + Align：同时改进提示选择与模型适配，但直接返回生成候选而不执行 Verify；它是判断验证阶段是否为大幅收益所必需的关键对照。

**实验想回答的问题**

- 在固定 Qwen2.5-Coder-7B-Instruct 骨干模型的条件下，联合使用任务感知路由 Route、提示对齐的 LoRA 适配 Align 与基于公开测试执行结果的 Verify，能否提高 MBPP 上最终程序的功能正确性？
- 性能提升来自单个组件的独立作用，还是来自 Route、Align 与 Verify 的协同；该提升在重复子集实验中是否稳定，并且能否排除训练数据与评测题目近重复污染这一替代解释？

**实验实现**

所有配置使用同一 Qwen2.5-Coder-7B-Instruct 骨干，以尽量把差异归因于 Route、Align 和 Verify 的组合。评测环境为 NVIDIA GeForce RTX 5090（32GB VRAM，Driver 580.105.08）、Python 3.11.14 和 Linux 5.15.0。主实验分别在 MBPP Sanitized 与 MBPP Full 上报告 pass@1；组件实验只覆盖 Base、Route + Verify、Align + Verify、Route + Align 和 Full RAV，因此属于部分组件消融而非完整析因实验。稳健性分析在 120 题子集上重复三次并报告提升的 95% 置信区间；污染分析则遍历训练样本—基准实例配对，检查完全重合与 $J\geq0.8$ 的近重复。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除 Verify，仅保留 Route + Align | Route + Align 在 MBPP Sanitized 和 Full 上的 pass@1 分别为 $0.8366$ 与 $0.7640$；相对 Base 的 MBPP Full 提升仅为 $0.0112$，即 $1.12$ 个百分点。 | 该对照隔离了“改进提示与适配、但不执行候选验证”的情形。与 Base 的 $0.7528$ 相比，MBPP Full 只升至 $0.7640$，说明 Route 和 Align 并不会自动把更好的候选分布转化为大幅 pass@1 提升。它支持 Verify 很关键，但并非严格的单变量消融，因为实验矩阵未报告只移除 Verify 且完全控制候选数量、采样过程等因素的更多重复结果。 | Table III, Route + Align row<br><span class="experiment-evidence">Route + Align \| ✓ \| ✓ \| 0.8366 \| 0.7640 \| +0.0112</span> |
| 在 Verify 下分别移除 Align 或 Route，并与完整 RAV 比较 | Route + Verify 在 Sanitized/Full 上为 $0.8794/0.8500$，Align + Verify 为 $0.8833/0.8460$，完整 RAV 为 $0.8911/0.8520$。完整系统在两种设置上都超过两个双组件版本，但边际差距较小：相对 Route + Verify 分别高 $0.0117$ 和 $0.0020$，相对 Align + Verify 分别高 $0.0078$ 和 $0.0060$。 | 这组比较检验 Route 与 Align 在已有 Verify 时是否冗余。完整系统持续更高，支持二者具有互补性；但 MBPP Full 上 Full RAV 仅比 Route + Verify 高 $0.0020$，且原文未给出这些配置差值的置信区间或显著性检验，因此不能断言每个小幅边际提升都具有统计稳定性。 | Table III, Route + Verify, Align + Verify, and Full RAV rows<br><span class="experiment-evidence">Route + Verify \| ✓ \| ✓ \| 0.8794 \| 0.8500 \| +0.0972; Align + Verify \| ✓ \| ✓ \| 0.8833 \| 0.8460 \| +0.0932; Full RAV \| ✓ \| ✓ \| ✓ \| 0.8911 \| 0.8520 \| +0.0992</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过任务路由、LoRA 适配和执行测试验证提升 LLM 代码生成的功能正确性。; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`cd5dc69e233854841f982c9115047679e134444cbcc8edd15d1f9bf304974ce0`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
