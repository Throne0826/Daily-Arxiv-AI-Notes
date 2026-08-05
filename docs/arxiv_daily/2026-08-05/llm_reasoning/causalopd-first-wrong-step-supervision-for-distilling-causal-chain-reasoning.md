---
title: "[论文解读] CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning"
description: "[arXiv 2608.03673][LLM Reasoning] CausalOPD面向具有前后依赖关系的因果推理，通过显式领域知识定位学生推理中最早可验证的错误，并按因果阶段对错误后缀进行局部在线优化。"
arxiv_id: "2608.03673"
announcement_date: "2026-08-05"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:37:40.355972+00:00"
source_sha256: "429bfb62645e14dd8017bf3d2d562e17a07fb5d4622b0e34dca1799785d423e2"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "多步因果推理"
  - "知识蒸馏"
  - "同策略蒸馏"
  - "过程监督"
  - "首个错误步骤"
  - "因果链"
  - "本地部署小模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.03673</p>

# CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Jian Zhang, Bingyi Wang, Yizhi Liu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Zhejiang University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03673v1) · [PDF 下载](https://arxiv.org/pdf/2608.03673v1) · **关键词** 多步因果推理, 知识蒸馏, 同策略蒸馏, 过程监督, 首个错误步骤, 因果链, 本地部署小模型<br>


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

CausalOPD面向具有前后依赖关系的因果推理，通过显式领域知识定位学生推理中最早可验证的错误，并按因果阶段对错误后缀进行局部在线优化。

**不用术语来说**：在临床诊断、法律判断和工业故障诊断中，模型不仅要给出正确结论，还必须说明一条可信的推理链；如果前面误认了证据，后续机制和结论即使表面连贯，也可能建立在错误前提上。现有蒸馏方法容易只看最终答案或模仿教师的完整解题过程，因而可能把“答案碰巧正确、理由实际错误”的模型部署到高风险场景。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出基于知识的“首个错误步骤”监督：知识增强教师依据领域因果规则、实体关系和结构约束，检查学生自己生成的推理轨迹，定位最早能够被现有知识明确判定为违规的状态转移，从而区分原始错误与其后续传播结果。该判定是知识覆盖范围内的验证，而不是对步骤绝对正确性的证明。
- 提出依赖感知的局部优化与课程训练：保留首错之前已经验证的前缀，仅对受影响的推理后缀实施短时域强化学习，并按照“证据识别→机制推断→结论归因”的先决关系逐级推进纠错。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究面向临床诊断、法律裁判推理和工业故障诊断等决策关键场景的多步因果推理蒸馏。这类任务不是仅从输入预测标签，而是要求模型依次完成证据识别、机制推断与结论归因；前一步会约束后一步，因此早期错误可能沿推理链传播，甚至出现“结论正确但推理无效”。大型语言模型虽具备较强推理能力，但外部 API 在数据隐私、推理延迟和可控性方面存在部署限制，因而需要将能力迁移到可本地运行的小模型。本文所处的技术交叉点是知识蒸馏、同策略蒸馏与过程监督：核心关注对象不仅是最终答案，还包括学生模型在自身生成分布上形成的完整因果路径。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**同策略蒸馏（On-policy Distillation, OPD）**

由学生模型先生成当前策略下的推理轨迹，再由教师针对这些轨迹提供监督，从而减少只学习教师示范所造成的训练—推理分布错位。本文指出，常规 OPD 即使看到了学生自己的错误，也未必能确定因果链从哪一步开始失效。

</div>
<div class="concept-item" markdown="1">

**过程监督（Process Supervision）**

监督信号作用于推理的中间步骤，而非只根据最终结论给整条轨迹一个分数。它有助于发现“答案碰巧正确、过程却不成立”的情况，但若逐步独立评分，仍可能混淆源头错误与其后续影响。

</div>
<div class="concept-item" markdown="1">

**首个错误步骤（First Wrong Step）**

指推理轨迹中最早能够被现有领域知识或因果约束明确判定为冲突的状态转移。该定义具有知识覆盖边界：未检测到冲突只表示当前约束无法证伪，并不等于该步骤在所有意义上都正确。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是工业、临床或法律领域的案例，以及可供教师使用的领域知识，包括因果规则、实体关系和结构约束；学生模型需要输出由证据识别、机制推断到结论归因构成的多步因果轨迹及最终结论。训练设置中，知识增强教师首先提供有知识依据的示范以初始化学生，随后检查学生按当前策略生成的轨迹，并寻找最早可验证的违规转移。问题的关键假设是因果步骤具有方向性依赖：证据决定可支持的机制，机制进一步限制合理结论；因此，训练目标不能只追求最终标签正确，还必须提高整条路径的有效性，并区分原始错误与由其传播产生的后续错误。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **On-policy distillation（Gu et al., 2024；Agarwal et al., 2024）**: 这些方法在学生自身生成的轨迹上对齐师生输出分布，缓解传统教师轨迹模仿的分布错位；本文以此为直接基础，但进一步要求定位最早使因果路径失效的转移，而不是只进行序列级对齐。
- **Process reward models（Uesato et al., 2022；Lightman et al., 2024）**: 过程奖励模型利用人工标注评价中间推理步骤，使监督比最终结果奖励更细粒度。本文认为，常见的局部步骤评分没有充分表达因果链的依赖结构，因此改用显式领域约束验证首个错误步骤，并保留此前已验证的前缀。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

关键决策任务要求推理过程可审查，同时又受到隐私、推理延迟和系统可控性的约束，因此需要把大型或专有模型的因果推理能力迁移到可在本地部署的小模型。此类任务具有明显的步骤依赖：证据识别约束机制推断，机制又约束最终归因；早期错误会沿链条传播，而只检查结论会漏掉“结论正确但推理无效”的风险。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **轨迹模仿与序列级在线策略蒸馏**：传统轨迹模仿让学生复现教师生成的完整推理；在线策略蒸馏则改为在学生自身生成的轨迹上，用教师分布监督学生，以减轻训练时教师轨迹与测试时学生行为之间的分布偏移。
- **结果监督与通用过程监督**：结果监督根据最终结论为整条轨迹给出单一奖励；过程奖励模型则利用人工步骤标注或后续成功概率，对中间步骤分别评分，从而提供比最终答案更细粒度的反馈。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有反馈缺乏可靠的知识锚点：强模型也可能不一致地应用形式化因果规则，而单纯模仿教师输出还可能把无依据或错误的推理复制给学生。其后果是过程评分看似细致，却未必能证明某一步符合领域约束。
- 现有方法通常独立评价各步骤或重新优化整条回答，没有显式识别导致路径失效的最早转移。由于首错之后的步骤可能只是在错误前提下保持自洽，这会混淆错误原因与传播后果，也忽略证据、机制和结论之间应有的学习顺序。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究分别改善了监督与学生生成分布的一致性和反馈粒度，但尚缺少一种同时尊重因果链依赖结构的过程蒸馏机制：它既要用可核验的领域知识判断错误，又要定位首个可证实的违规步骤，并依据各推理阶段的先决关系安排纠错，而不是把所有步骤视为彼此独立、同等可学的单元。

</div>
<div markdown="1"><span>核心问题</span>

能否在学生的在线推理轨迹中，以显式领域约束可靠地定位首个可验证错误，保留此前正确前缀并只修复受影响后缀，再按因果传播顺序组织训练，从而提升小模型的整条推理路径可信度，而非仅提高最终标签正确率？

</div>
<div markdown="1"><span>作者直觉</span>

因果链类似逐层搭建的结构：地基出错后，继续修饰上层无法消除根因。若先找到最早违反规则的位置，就可以保留此前已经验证的部分，把学习信号集中到真正引发失败的局部区间；再先训练证据识别、后训练机制和结论，便能让后续能力建立在较可靠的前置能力上，减少错误传播和无效的全序列重优化。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CausalOPD 是一种面向因果链推理的在线过程蒸馏框架。对每个案例，学生仅接收观测 $x$ 与推理时可用的系统或上下文元数据 $\mu_x$，并生成结构化推理轨迹 $\tau=(z_1,\ldots,z_H)$；教师在训练时额外获得特权上下文 $p_x=(y,\mathcal{K}_x)$，其中 $y$ 是参考结论，$\mathcal{K}_x$ 包含领域因果规则、实体关系及结构约束。框架先用经知识检验和修订的教师轨迹完成冷启动，再让当前学生进行在线采样，由教师依据显式约束找出最早可证实的错误转移 $h^*$ 及其违反的约束 $c^*$，随后从已验证前缀之后实施短时域修复，并按证据、机制、结论的因果传播顺序安排训练。

其核心不是让学生重写整条答案，而是把一次错误定位同时用于决定“修什么、从哪里修、何时优先修”：$c^*$ 指明错误内容，$h^*$ 给出优化边界，阶段映射 $g(h^*)$ 决定该样本进入课程的时机。通俗地说，教师像批改多步证明一样找到第一处真正出错的推导，保留此前正确步骤，只训练学生改正该点及其较短后续；每轮重新收集当前学生的新错误，避免一直练习模型早已克服的旧问题。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 知识落地的教师轨迹构造与冷启动

冻结教师依据参考结论 $y$ 和领域知识 $\mathcal{K}_x$ 构造结构化因果轨迹，并通过“构造—评价—修订”流程检查其是否符合适用因果规则、实体关系与结构约束；修订后的轨迹用于学生的初始监督微调。原文节选未给出该阶段的精确损失函数。

<div class="method-step__io" markdown="1">

**输入**：案例观测 $x$、共享元数据 $\mu_x$，以及仅供训练教师使用的特权上下文 $p_x=(y,\mathcal{K}_x)$。<br>
**输出**：具有知识依据的教师轨迹，以及能够按规定模式输出证据、机制和结论阶段的冷启动学生策略 $\pi_\theta$。

</div>

**直观理解**：先让专家写出并复核一批标准解题过程，再让学生学习基本格式和可靠推导；这比直接模仿教师第一次生成、但可能含错的答案更稳妥。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 当前策略在线采样与逐步验证

学生按当前策略生成在策略轨迹 $\tau=(z_1,\ldots,z_H)$；验证接口逐步检查每个转移是否满足当前案例中适用的知识与结构约束，并允许对证据不足或约束不适用的步骤保持未决，而非强行判错。

<div class="method-step__io" markdown="1">

**输入**：冷启动或上一轮更新后的学生策略 $\pi_\theta$，以及学生可见的 $x$ 和 $\mu_x$。<br>
**输出**：带有逐步验证状态的学生轨迹，以及供本轮重建的候选纠错池。

</div>

**直观理解**：不只在教师写出的标准答案上训练，而是让学生先自己作答，再观察它现在实际会犯什么错；这样训练数据跟随学生能力变化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 第一错误步定位与纠错状态构造

教师确定最早被可用约束明确否定的转移位置 $h^*$，记录被违反的约束 $c^*$，并通过阶段函数 $g(h^*)$ 将错误归为证据、机制或结论阶段；$h^*$ 之前的已验证轨迹作为保留前缀，错误边界附近的状态进入纠错池。若某一步不能被可靠判定，框架将其视为未决，而不把它伪装成已验证错误。

<div class="method-step__io" markdown="1">

**输入**：学生轨迹、教师可见的 $p_x=(y,\mathcal{K}_x)$，以及逐步验证结果。<br>
**输出**：定位结果 $(c^*,h^*,g(h^*))$、已验证前缀及阶段化纠错状态。

</div>

**直观理解**：教师寻找第一张倒下的多米诺骨牌，而不是只看最后一张是否倒对；因为后面的错误可能只是第一处错误传播出的结果。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 纠错状态微调与课程化短时域强化学习

框架先对错误边界处的纠错状态做监督微调，再从已验证前缀开始，仅优化局部后缀的短时域强化学习目标；课程按 Evidence、Mechanism、Conclusion 的传播顺序推进，使上游错误优先得到修复。节选表明其奖励项与完整轨迹过程强化学习基线相同，但未披露奖励的精确代数形式，因此不能据此重建具体目标。

<div class="method-step__io" markdown="1">

**输入**：按 $g(h^*)$ 分类的纠错状态、保留前缀、教师修订目标及过程验证信号。<br>
**输出**：减少当前阶段首错的更新后学生策略，以及下一轮在线采样所需的检查点。

</div>

**直观理解**：保留已经做对的前半段，只重练从首错开始的一小段；先修“看错证据”，再修“机制推错”，最后修“结论归因错”，可减少上游错误不断污染后续步骤。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标可概括为：在保持已验证前缀的条件下，提高学生从首错边界开始生成约束一致后缀和正确结论的概率，并通过阶段课程优先消除会向下游传播的错误。三阶段训练分别承担不同作用：知识落地的教师轨迹为学生提供可靠初始化，纠错状态监督微调让模型先学会首错处应如何转向，短时域强化学习再用过程与结论反馈优化学生自己的在策略后缀。原文节选只说明 CausalOPD 与完整轨迹过程强化学习使用相同奖励项，没有提供奖励函数、权重、优势估计或监督损失的完整公式，故不应臆造中心方程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 知识驱动的第一错误步验证器**

验证器利用训练期特权上下文 $p_x=(y,\mathcal{K}_x)$，按轨迹顺序寻找最早可由适用规则或结构约束证实为错误的转移，并返回违反约束 $c^*$、位置 $h^*$ 和阶段 $g(h^*)$。其判定对象是文档化机制下的逐步因果归因，而不是干预式或反事实因果推断；对缺失证据、混杂因素和约束适用性的信息由共享元数据 $\mu_x$ 描述。

> 直观理解：该模块把教师的笼统“这段推理不好”变成可执行的诊断：哪条规则被违反、第一处错在哪里、属于哪类错误。显式允许未决也能降低教师在证据不足时制造错误监督的风险。

**2. 前缀保留的局部修复器**

以 $h^*$ 为边界固定或保留此前已验证前缀，把优化集中在错误转移及其短后缀；训练结合纠错状态监督微调与短时域强化学习。该设计与“使用相同奖励但优化完整响应”的基线相区分，因此方法增益所检验的不只是奖励内容，还包括优化边界与信用分配方式。

> 直观理解：整篇重写会让模型重复修改正确内容，也难以判断奖励应归功或归咎于哪一步；从首错处局部重做，相当于把反馈直接送到故障源。

**3. 因果阶段课程与动态纠错池**

阶段函数把每个首错映射到 Evidence、Mechanism 或 Conclusion，课程依照证据到机制再到结论的因果传播方向安排优先级；每轮依据当前策略的新轨迹重建纠错池。课程控制训练顺序，动态池则使监督分布持续贴近学生当前的在策略分布。

> 直观理解：先纠正输入事实的读取，再学习事实之间的机制联系，最后训练结论归因，能避免在错误地基上反复修饰结论；刷新纠错池则避免模型一直复习已经会做的旧错题。

**训练与推理**

训练时，每个领域独立训练一个学生。冻结的 Qwen3.7-max 教师可访问 $p_x=(y,\mathcal{K}_x)$，Qwen3-8B 学生和其他对比方法只接收 $x$ 与 $\mu_x$；先用经知识评价和教师修订的轨迹完成冷启动，随后循环执行“当前学生采样—约束验证—定位 $h^*$—按 $g(h^*)$ 入池—纠错状态微调—局部短时域强化学习—刷新轨迹池”。不同领域之间不共享数据、知识库或检查点，以免把跨域迁移误当成算法效果。

推理时不存在训练期信息不对称：学生仅依据案例观测与正常可用元数据生成 $\tau=(z_1,\ldots,z_H)$ 和最终结论，不访问参考答案 $y$、训练知识 $\mathcal{K}_x$、教师或验证器。因而方法的部署成本主要是单个学生模型的前向生成；知识库与大型教师用于训练监督，而不是作为推理期检索组件。

**复现信息**

公平比较所需的关键设置是：学生统一为 Qwen3-8B，教师为冻结的 Qwen3.7-max；三个领域分别训练，采用相同三阶段流程、逐轮新鲜采样和纠错池重建。所有训练方法共享学生基座、提示、输出结构和解码配置；序列级在线过程蒸馏还匹配初始化、采样数量、更新步数与被优化 token 预算，完整轨迹过程强化学习则使用与 CausalOPD 相同的奖励项，从而分别隔离首错定位、阶段调度和局部优化的作用。原文节选未给出学习率、批量大小、奖励权重、每轮采样数、课程切换阈值及短时域长度，复现时需回查论文附录，不能从现有材料推定。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 工业领域评测：用于检验模型能否按照工业故障的证据、机制和结论依赖关系生成有效因果链。所给实验章节摘录仅列出“Industrial”，未提供数据集名称、样本规模、训练/验证/测试划分或具体任务构成。
- 临床领域评测：用于检验模型能否基于临床证据形成逐步诊断因果链。所给摘录仅列出“Clinical”，未报告数据集名称、病例数量、划分方式或隐私处理细节。
- 法律领域评测：用于检验模型能否依据事实、规则和法律结论之间的结构约束完成链式判断。所给摘录仅列出“Legal”，未报告数据集名称、规模、划分或标签体系。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**平均路径正确性**

衡量整条推理路径中的步骤和因果转移是否满足可用领域约束，而不只检查最终答案。摘要报告的是三个领域上的平均结果，但所给摘录未说明逐步判定规则、聚合公式以及采用人工评审还是自动验证器。 （越高越好，因为更高的路径正确性表示模型更经常得到过程有效、因果关系成立的推理链。）

</div>
<div class="metric-item" markdown="1">

**正确标签—错误推理率**

衡量最终标签虽然正确，但中间推理链存在错误的样本比例。该指标用于揭示只看答案准确率时会被掩盖的过程错误。 （越低越好，因为较低比例表示正确结论更可能由有效推理得到，而不是由猜测、捷径或相互抵消的中间错误产生。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个领域的平均结果：CausalOPD 对比序列级在线过程蒸馏

<div class="result-value" markdown="1">

作者报告，CausalOPD 的平均路径正确性比序列级在线过程蒸馏高 23.4 个百分点。

</div>

这一差值支持首错定位与局部修复比整序列级监督更适合纠正会沿因果链传播的过程错误。它是“百分点”的绝对提升，而不是 23.4% 的相对提升。但现有材料没有给出两种方法各自的绝对分数、分领域结果、误差范围或显著性检验，因此无法判断提升是否由某一个领域主导，也不能单凭该结果确定是哪一项组件造成提升。

<div class="result-source" markdown="1">

来源：摘要；所给第 4 节摘录未包含对应表格编号

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across three domains, CausalOPD improves average path correctness by 23.4 percentage points over sequence-level online process distillation and reduces the right-label-wrong-reasoning rate from 15.7% to 4.4%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 三个领域的平均结果：正确标签但错误推理的样本

<div class="result-value" markdown="1">

作者报告，正确标签—错误推理率从 15.7% 降至 4.4%，绝对下降 11.3 个百分点，按起始值计算约下降 72.0%。

</div>

该结果表明，CausalOPD 不仅可能让最终答案正确，还减少了“碰巧答对但因果链无效”的情况，这与论文强调的过程可靠性直接对应。约 72.0% 是依据摘要数字计算的相对降幅，不是原文直接报告的统计量；此外，所给材料未说明该指标的判定者、错误阈值和置信区间，因此不能据此断言模型在真实高风险场景中已经安全可靠。

<div class="result-source" markdown="1">

来源：摘要；所给第 4 节摘录未包含对应表格编号

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across three domains, CausalOPD improves average path correctness by 23.4 percentage points over sequence-level online process distillation and reduces the right-label-wrong-reasoning rate from 15.7% to 4.4%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 工业、临床和法律三个领域：领域专用 8B 学生模型对比两个专有参考模型

<div class="result-value" markdown="1">

作者声称，领域专用 8B 学生模型在全部三个领域的路径正确性上均超过两个被评测的专有参考模型；原文未明确报告各模型的具体分数或差值。

</div>

这一比较说明，较小且可本地部署的学生模型在特定领域经过过程蒸馏后，路径质量可能优于所选闭源参考模型。它不证明 8B 学生在通用能力、最终答案准确率、延迟、成本或所有专有模型上都更优；由于参考模型名称、版本、提示词和推理预算均未提供，也无法评估比较范围与公平性。

<div class="result-source" markdown="1">

来源：摘要；所给第 4 节摘录未包含对应表格编号

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The domain-specific 8B students also surpass both evaluated proprietary references in path correctness across all domains.

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

- 序列级在线过程蒸馏：摘要将其作为主要比较对象。该基线同样利用在线生成的推理过程进行蒸馏，但比较结果旨在检验“定位首个可验证错误并进行局部修复”是否优于对整条序列进行较粗粒度的过程监督；其算法定义和实现配置在所给摘录中未出现。
- 两个专有参考模型：用于判断本地部署的领域专用 8B 学生模型是否能在推理路径质量上达到或超过闭源模型。摘要未给出这两个模型的名称、版本、提示设置或解码配置，因此无法判断比较是否严格控制了模型访问方式与推理预算。
- CausalOPD 的知识增强教师：它为学生提供受领域因果规则、实体关系和结构约束约束的轨迹，构成蒸馏监督的来源。它更接近系统组成部分而非独立基线；所给实验材料没有报告教师自身的结果，因此不能据此比较学生与教师的能力差距。

**实验想回答的问题**

- 与序列级在线过程蒸馏相比，CausalOPD 是否能提高学生模型在工业故障诊断、临床诊断和法律判断三类任务中的因果推理路径正确性，并减少“答案正确但推理错误”的情况？
- 经过领域知识增强、首个错误步骤定位、局部强化学习修复和因果阶段课程训练后，领域专用的 8B 学生模型能否在路径正确性上超过被评测的专有模型？

**实验实现**

评测覆盖工业、临床和法律三个领域，并报告跨领域平均值。摘要说明被评测学生为领域专用 8B 模型，训练流程包含知识增强教师轨迹、学生在策略轨迹、教师识别首个错误步骤、从已验证前缀出发的短视野强化学习修复，以及从证据层到机制层再到结论层的课程推进。然而，所给第 4 节摘录只有实验标题和领域表头，未提供模型底座、训练数据量、超参数、随机种子、解码策略、评审者一致性、显著性检验或计算预算，因而目前无法复现实验或核验比较公平性。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过首个错误步骤监督、在线过程蒸馏和局部强化学习训练小型语言模型的因果链推理能力。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`429bfb62645e14dd8017bf3d2d562e17a07fb5d4622b0e34dca1799785d423e2`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
