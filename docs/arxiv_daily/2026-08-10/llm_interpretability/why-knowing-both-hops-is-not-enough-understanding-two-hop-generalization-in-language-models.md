---
title: "[论文解读] Why Knowing Both Hops Is Not Enough: Understanding Two-Hop Generalization in Language Models"
description: "[arXiv 2608.07261][LLM 机制与可解释性] 原文未明确报告。"
arxiv_id: "2608.07261"
announcement_date: "2026-08-10"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-10T02:39:06.971528+00:00"
source_sha256: "ade27bb54d8590ea523bfe48035996164354adf809887dfc1e47c7c19052ca20"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "LLM 其他"
  - "两跳推理"
  - "组合性缺口"
  - "隐式推理"
  - "Transformer"
  - "机械可解释性"
  - "分布外泛化"
  - "桥接实体表示"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2608.07261</p>

# Why Knowing Both Hops Is Not Enough: Understanding Two-Hop Generalization in Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Zili Zhang, Yilin Wang, Heng Wang, Herun Wan, Minnan Luo</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Xi’an Jiaotong University；University of Illinois Urbana-Champaign</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.07261v1) · [PDF 下载](https://arxiv.org/pdf/2608.07261v1) · **关键词** 两跳推理, 组合性缺口, 隐式推理, Transformer, 机械可解释性, 分布外泛化, 桥接实体表示<br>


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

本文研究语言模型的隐式两跳推理：模型不必显式输出推理链，却应能把两个已学到的原子事实组合为新结论。核心现象是“组合性缺口”：即使模型能分别回答两条单跳事实，仍可能无法稳定回答它们的复合查询。为排除真实预训练语料中记忆、偶然相关性等混杂因素，作者在可控的符号环境中从头训练 Transformer，并从其逐层隐状态出发分析该能力何时出现、何时失效。来源：§1 Introduction；§6.2--§6.3。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**两跳推理（two-hop reasoning）**

给定两个可串联的原子事实，例如 $A\to B$ 与 $B\to C$，模型需要推出 $A\to C$。其中 $B$ 是连接前后两步的桥接实体。

</div>
<div class="concept-item" markdown="1">

**隐式推理（implicit reasoning）**

模型在最终答案中不生成中间推理步骤，但内部激活状态仍可能先形成桥接实体等潜在状态，再产生答案。本文关注的正是这种不外显的两跳计算。

</div>
<div class="concept-item" markdown="1">

**机械可解释性（mechanistic interpretability）**

该方向尝试把神经网络的行为还原为内部组件和层间计算，而不仅评价输入输出正确率。本文使用中间层表示与因果干预来定位桥接信息是否形成、是否被后续层使用。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是由两个可组合关系构成的符号化查询及其实体/关系表示；训练数据包含原子事实，并在不同分布切分下提供两跳组合；目标输出是复合关系对应的终点实体，即由 $A\to B$ 和 $B\to C$ 得到 $A\to C$。作者从头训练 Transformer，避免把预训练数据中的外部知识或表面统计关联误判为推理。测试按两跳中各跳是否符合训练分布区分：作者报告第二跳仍符合训练分布的 Test-II、Test-OI 可可靠泛化，而第二跳分布外的 Test-IO、Test-OO 失败。这里的研究问题不只是“模型答对了吗”，还包括：同一桥接实体在不同上下文中的内部表示是否一致，以及上层能否把下层形成的该表示继续用于第二跳计算。来源：§1 Introduction。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$A \to B$**

从实体 $A$ 到实体 $B$ 的第一条原子事实或第一跳关系。

</div>
<div class="notation-item" markdown="1">

**$B \to C$**

从桥接实体 $B$ 到实体 $C$ 的第二条原子事实或第二跳关系。

</div>
<div class="notation-item" markdown="1">

**$A \to C$**

由前两条原子事实组合得到的两跳结论，也是模型需要预测的目标关系。

</div>
<div class="notation-item" markdown="1">

**$r_1$**

作者在机制分析中选取的位置；其第 5 层输出被定义为桥接实体的表示。来源：§1 Introduction。

</div>

</div>

**直接相关的工作**

- **Press et al. (2023)**: 该工作将“单跳事实能够回忆、两跳组合却失败”的现象形式化为组合性缺口（compositionality gap）。本文以此为问题背景，但进一步在受控符号任务中区分第二跳是否分布外，并试图给出层级机制解释。来源：§6.3 Two-Hop Reasoning。
- **Biran et al. (2024)**: 该工作指出，即便第一跳已正确检索到桥接实体，高层也可能没有利用该实体，显示表示形成与后续推理之间存在脱节。本文将这一观察推进为关于层间功能错配的解释，并在所述受控设置中分析其与第二跳分布外失败的关系。来源：§1 Introduction；§6.3 Two-Hop Reasoning。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

语言模型在需要组合多个事实的任务中表现并不稳定。即使模型已经能够分别回答原子事实，例如已知$A\to B$和$B\to C$，它仍可能无法回答由两者推出的$A\to C$。这会限制模型在知识问答、关系推断及其他依赖隐式多步推理的应用中的可靠性；尤其是模型不输出中间推理步骤时，错误来源难以从最终答案直接诊断。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **显式链式推理提示（Chain-of-Thought, CoT）**：通过提示模型把问题拆成连续的中间步骤，并显式生成每一步结果，再据此得到最终答案。该类方法的目标是把原本隐藏在模型内部的多跳计算外化为可见文本过程。
- **端到端隐式组合推理研究**：关注模型不生成中间步骤时，能否直接回答组合查询。论文所讨论的设定将变换器从头训练在可控的符号数据上，并分别检查原子事实记忆与两跳组合泛化，从而试图隔离预训练语料中的记忆和偶然相关性。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 显式CoT可以提供可读的步骤，但不能说明变换器在不输出步骤时究竟如何在内部完成两跳推理，也无法直接定位原子知识已正确而组合答案仍错误的机制原因。
- 既有关于隐式多跳能力的观察缺少对泛化条件的细分与因果机制解释。作者指出，模型在第二跳遵循训练分布时可泛化（Test-II、Test-OI），而第二跳分布外时失败（Test-IO、Test-OO）；仅以“模型会或不会两跳推理”概括这一现象，无法解释这种不对称性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚未解决的问题是：在排除不透明预训练数据干扰后，如何以可验证的内部机制解释两类相反结果，即为何同一模型已掌握两个原子事实，却只在第二跳与训练分布一致时完成组合；并进一步找出能针对该机制缺陷改善分布外两跳泛化的训练或架构原则。

</div>
<div markdown="1"><span>核心问题</span>

变换器对两跳查询的泛化为何取决于第二跳是否在训练分布内？成功与失败分别对应怎样的跨层中间表征和计算功能，而这些机制能否被重用以提升分布外两跳推理？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是先在符号环境中把“是否记住每一跳”和“是否能把两跳接起来”分开测量，再观察各层对桥接实体的表示。其直觉是：若不同输入上下文中的同一桥接实体形成可兼容的内部表示，后续计算可以复用；若下层已构造该表示、上层却主要把特定格式的表示映射为答案，那么输入格式或第二跳分布一变，上层便不能把已有的中间结果当作新的推理输入。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文针对符号化二跳查询 $c e_1,r_1,r_2e$ 的分布外泛化，采用“looped transformer”（循环式/参数复用的 Transformer）训练策略：将网络下半部分与上半部分对应层的参数共享，使同一套计算能够先处理输入形式的原子事实，再在较高层处理二跳推理中形成的中间表示。其目标不是增加显式中间答案监督，而是让高层接收到的“桥接实体表示+第二跳关系表示”与低层学习原子事实时的输入表征对齐，从而把低层已经学到的分布外原子事实推理能力复用于第二跳。

从直观上说，标准模型的低层虽然能把第一跳结果变成有意义的内部向量，但高层更容易把训练中见过的原子事实直接映射为答案，未必会把该内部向量当作同类输入继续计算。循环式设计相当于让模型在“读原子事实”和“做第二跳”两种阶段反复使用同一套计算规则；因此，第二跳遇到训练分布外组合时，仍有机会调用已学习的原子事实能力。附录还用表征注入训练验证了这一解释：先获得稳定的中间表征，再将其送入第 $6$ 层至第 $8$ 层，直接训练这些层从表征形式的分布外原子事实得到正确答案。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造并编码二跳查询

模型按 Transformer 层级处理查询；机制分析将 $r_1$ 位置的第 $5$ 层隐藏状态视为桥接实体 $e_2$ 的中间表示，并将 $r_2$ 位置的第 $5$ 层隐藏状态视为关系 $r_2$ 的中间表示。

<div class="method-step__io" markdown="1">

**输入**：二跳查询 $c e_1,r_1,r_2e$，其中 $e_1$ 为起始实体，$r_1$ 与 $r_2$ 分别为第一、第二跳关系。<br>
**输出**：可供后续第二跳计算使用的内部表征 $h_5(r_1)$ 与 $h_5(r_2)$。

</div>

**直观理解**：第一跳不会先被输出成文字答案，而是被压缩为模型内部的向量。后续层需要把这个向量正确理解为桥接实体，才能继续完成第二跳。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 共享上下半网络参数

采用 looped transformer 设计，在上下半部分层之间共享参数。附录 I 的具体例子是：$4$ 层模型共享底部 $2$ 层与顶部 $2$ 层的参数，$8$ 层模型共享底部 $4$ 层与顶部 $4$ 层的参数，其他层数依此类推。

<div class="method-step__io" markdown="1">

**输入**：具有偶数层结构的 GPT-2 式 Transformer；网络下半部分和上半部分的对应层。<br>
**输出**：低层原子事实处理与高层二跳处理使用同构且参数相同的计算模块。

</div>

**直观理解**：模型不是为“识别原子事实”和“继续推理”各学一套不同规则，而是让后一个阶段复用前一个阶段的规则。这样高层更可能把中间向量当成低层曾处理过的有效输入。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 联合训练以形成表征—输入对齐

按常规训练任务优化共享参数，使模型同时学习二跳答案与原子事实相关映射。论文通过逐层余弦相似度比较二跳查询中 $r_1$、$r_2$ 位置的隐藏状态，与对应第二跳原子事实中 $e_2$、$r_2$ 位置的隐藏状态，检验二者是否对齐。

<div class="method-step__io" markdown="1">

**输入**：训练集中的二跳样本 Train-II，以及其对应的第二跳原子事实；looped transformer 参数。<br>
**输出**：在共享模型中，二跳推理的中间表征与对应原子事实的嵌入式推理输入在层间具有更强对齐；作者据此解释其对 Test-IO 和 Test-OO 的泛化改善。

</div>

**直观理解**：训练希望“二跳推理做到一半时脑中形成的表示”，看起来像“模型直接读到第二跳原子事实时的表示”。两者足够相似时，已学会的单跳能力便能迁移过来。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 贪心解码输出答案

模型继续前向传播至输出层，并在测试集上采用 greedy decoding 生成预测答案。附录 G 的 logit-lens 分析显示，第 $6$ 层是第二跳推理开始的层：在 $r_2$ 位置，$r_2$ 的概率开始下降而目标实体 $e_3$ 的概率开始上升。

<div class="method-step__io" markdown="1">

**输入**：训练后的循环式模型和测试二跳查询。<br>
**输出**：预测的终点实体 $e_3$，用于计算各测试划分上的准确率。

</div>

**直观理解**：模型在前几层先形成第一跳结果，随后开始利用第二个关系寻找最终实体，最后直接选择当前最可能的答案。这里的贪心解码表示每一步都取概率最高的候选，而不进行多路径搜索。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文摘录未给出循环式训练的显式损失函数，因此不能据此重建交叉熵或其他目标的数学形式。可确认的是，训练监督要求模型对二跳问题和表征形式的分布外原子事实输出正确答案；在附录 F 的辅助验证中，$(h_{e_2},h_{r_2})$ 经第 $6$ 层至第 $8$ 层传播后接受答案监督。作者的核心优化诉求是通过跨半区参数共享，促成二跳中间表征与原子事实输入表征的可复用对齐，而非引入显式 CoT 的中间实体标注。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 循环式 Transformer 参数共享**

模型采用 looped transformer：上、下半网络对应层共享参数。附录 I 明确说明，所有比较模型保持 GPT-2 架构和隐藏维度 $768$，仅通过层数控制规模，并在底部与顶部对应半区共享参数。作者将此结构作为把低层“基于嵌入的原子事实推理”迁移到高层第二跳推理的架构机制。

> 直观理解：标准深层网络的不同层可以各自形成不同习惯，高层可能只会记忆训练格式。参数共享强制高层沿用低层已学到的处理方式，减少两段推理使用不兼容内部语言的风险。

**2. 中间表征与输入对齐**

对查询 $c e_1,r_1,r_2e$，论文比较所有层中 $r_1$ 位置隐藏状态与对应第二跳原子事实 $c e_2,r_2e$ 里 $e_2$ 位置隐藏状态，并比较两处 $r_2$ 的隐藏状态；每类比较形成大小为 $(L+1)ctimes(L+1)$ 的逐层余弦相似度矩阵，$L$ 为 Transformer 层数，层 $0$ 是不含位置编码的输入嵌入。作者报告循环式模型在红框区域的对角方向相似度更高，尤其 $(1,5)$ 项显著，而常规训练模型没有此模式（附录 J、图 21）。

> 直观理解：该模块不是额外的预测头，而是一种解释和验证工具：它检查模型做第二跳时的内部状态，是否真的像在处理相应的单跳事实。相似度高支持“能力复用”这一机制解释，但相似度本身不等同于因果证明。

**3. 表征注入式机制验证训练**

附录 F 先对标准模型训练 $3,500,000$ 个优化步，待其在 Test-II 和 Test-OI 上具有高泛化性能后，收集 Train-II 中所有实体的 $h_5(r_1)$ 与所有关系的 $h_5(r_2)$。随后将每个分布外原子事实 $(e_2,r_2)$ 改写为 $(h_{e_2},h_{r_2})$，送入第 $6$ 层并经后续层传播，以正确答案监督第 $6$ 至第 $8$ 层；该过程与标准训练交替、多轮重复，以避免额外训练损害原有泛化。

> 直观理解：这是一个针对机制的干预实验，而非最终部署时必需的输入格式。它直接把第一跳形成的内部表示交给高层，并训练高层据此回答，检验高层缺少的是否正是“从这种表示继续做分布外原子推理”的能力。

**训练与推理**

主方法训练时使用循环式参数共享架构，在常规任务训练中优化模型；附录 F 的机制验证则先进行标准训练，再交替执行标准训练和表征式训练。推理时不需要显式 CoT，也不需要把中间实体作为额外文本输入：模型直接接收二跳查询，在内部形成 $h_5(r_1)$ 与 $h_5(r_2)$ 等状态，随后由上层完成第二跳并生成答案。测试采用贪心解码。需要区分的是，表征注入训练是为验证和补强“高层可对内部表示推理”的假设而设计的附加程序；论文所提可部署方案是修改架构的 looped transformer，而非要求推理阶段输入隐藏状态。

**复现信息**

可复现且影响结果解释的设置包括：实验使用 Tesla V100-PCIE-32GB GPU，在 $4$ 张 GPU 上训练；每张 GPU 的 batch size 为 $1024$；学习率为 $1\times10^{-4}$，weight decay 为 $0.1；测试使用 greedy decoding（附录 B）。模型尺度实验固定 GPT-2 架构、隐藏维度 $768$，考察 $4$、$8$、$16$、$24$ 层的循环式模型，并令上下半网络共享参数（附录 I）。对表征式验证训练，原文明确使用标准训练 $3,500,000$ 个优化步后的模型，并在第 $5$ 层提取表征、从第 $6$ 层注入；原文未在所给摘录中明确报告其每轮训练步数、总轮数、词表/实体关系规模、损失函数形式及初始化细节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 合成符号数据集：包含 $2{,}000$ 个实体和 $200$ 个关系。每个实体随机连接 $20$ 个不同的出边关系，共形成 $40{,}000$ 条原子事实；其中 $95\%$ 为 ID 原子事实、$5\%$ 为 OOD 原子事实。它用于在可控条件下区分“模型是否知道每一跳”与“模型是否能组合两跳”。训练集含 $38{,}000$ 条 ID_atomic、$2{,}000$ 条 OOD_atomic 和 $273{,}600$ 条 Train-II；测试中各主要分割通常为 $3{,}000$ 条，Test-OO 为 $1{,}987$ 条。
- 两跳分布组合分割：将第一跳和第二跳分别标记为 ID 或 OOD，构成 II、IO、OI、OO 四类路径。Train-II 是训练用 ID-ID 路径；Test-II 检验未见的 ID-ID 组合；Test-OI 检验第一跳 OOD、第二跳 ID；Test-IO 与 Test-OO 则检验第二跳 OOD 时的泛化。这些分割的核心作用是隔离第二跳分布变化，而不是测试单跳事实记忆。
- 从 Wikidata5M 提取的真实世界稠密子图：作者以 human 类型实体为候选，按 $\text{score}(e)=\frac{\text{in-degree}(e)\times\text{out-degree}(e)}{\text{in-degree}(e)+\text{out-degree}(e)}$ 选取前 $100$ 个中心节点，再保留其邻居及节点间边。过滤环路、限制每个关系对的单一目标占比不超过 $0.2N$，并丢弃目标实体少于 $10$ 个的关系对；最终有 $14{,}995$ 个实体、$176$ 个关系。该数据用于检验循环式训练在非合成图上的适用性，训练时将 Train-II/单跳事实比例设为 $\phi=7.2$。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（accuracy）**

在各原子事实或两跳测试分割上，模型输出正确尾实体的比例。它直接衡量模型是否答对组合查询，而非仅检查隐藏层是否出现某个实体表征。 （越高越好；接近完美准确率表示模型能稳定回答该分割中的事实或组合，接近随机水平则表示未获得可用泛化。）

</div>
<div class="metric-item" markdown="1">

**训练过程中的分割准确率曲线**

沿优化步数记录 Train-II、Test-II、Test-OI、Test-IO、Test-OO 等分割的准确率，用于区分先记忆训练组合、后泛化到未见组合的阶段性行为。 （测试分割准确率在训练持续后上升且稳定较高更好；若仅 Train-II 很高而测试分割不升，说明拟合不能证明组合泛化。）

</div>
<div class="metric-item" markdown="1">

**Logit lens 概率**

对第 $l$ 层、位置 $t$ 的隐藏状态 $h_l(t)$ 经 LayerNorm 和词嵌入转置投影后得到目标实体或关系的概率，用来观察桥接实体、第二跳关系和最终实体何时在层间显现。它是机制诊断指标，不等同于端到端准确率。 （不存在单一的数值优劣方向；若桥接实体表征先形成、随后最终实体概率在第二跳开始处上升，且该过程能支持跨输入形式的正确输出，才与两跳推理解释一致。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 标准训练模型在未见的 ID-ID 两跳组合 Test-II 上的训练动态。

<div class="result-value" markdown="1">

模型先迅速把 Train-II 拟合到近乎完美，继续训练后 Test-II 准确率稳步上升并最终达到完美准确率。作者将此解释为模型从直接记忆训练组合转向对 ID 第二跳条件下组合规则的泛化。

</div>

这表明“只知道两个单跳事实不足以推出一定失败”：在第二跳仍符合训练分布时，模型最终可以把未见的两跳路径答对。不过该现象只证明此特定的受控符号设置存在 Test-II 泛化，不能证明模型在任意知识图谱、任意关系组合或自然语言问题上都进行了可迁移的显式推理。

<div class="result-source" markdown="1">

来源：Section 3, Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

After continued training, the accuracy on Test-II begins to increase steadily and eventually reaches perfect accuracy, suggesting that the model transitions from memorization to generalization.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 标准训练模型在第一跳 OOD、第二跳 ID 的 Test-OI 上的训练动态。

<div class="result-value" markdown="1">

在较晚训练阶段，Test-OI 出现明显准确率提升；结合作者的总体结论，这一结果被归入“第二跳保持训练分布时能够可靠泛化”的模式。

</div>

第一跳为 OOD 并不必然阻断两跳泛化，关键差异在于第二跳仍是 ID。这为论文随后提出的机制假设提供实验动机：模型可以先构造某种桥接实体的中间表征，再由后层处理熟悉的第二跳。原文在所给摘录中没有提供 Test-OI 的最终准确率，因此不能量化其是否与 Test-II 同样达到完美。

<div class="result-source" markdown="1">

来源：Section 3, Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At a later stage of training, the model also exhibits noticeable gains on the Test-OI split, indicating the emergence of an additional generalization phase.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 标准训练模型在第二跳 OOD 的 Test-IO 和 Test-OO 上的训练动态。

<div class="result-value" markdown="1">

即使延长训练，Test-IO 和 Test-OO 的表现仍接近随机水平；作者据此得出高度不对称的泛化模式，即第二跳偏离训练分布时模型持续失败。

</div>

这是论文最关键的负结果：模型已在训练中见过组成路径的 OOD 原子事实，因此失败不能简单归因于“第二跳知识从未学习”。它支持作者对层间失配的后续分析，但仅凭准确率曲线还不能单独证明失配一定是唯一因果原因；该因果解释需依赖后续的表征和干预实验。

<div class="result-source" markdown="1">

来源：Section 3, Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

However, even with longer training, the model cannot generalize on Test-IO and Test-OO splits.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给材料的主训练结论来自随机构造的符号知识图谱。尽管真实世界 Wikidata5M 子图的构造过程被说明，摘录未报告该真实数据上的循环式训练准确率、方差或与标准训练的直接比较，因此现实任务上的收益仍需核对原文结果章节。
- 当前摘录未给出表征式训练和循环式训练的主结果表、随机种子、重复实验或统计显著性；Table 5 只列优化步数和训练时间。因而“显著改善 OOD 两跳泛化”的作者主张在本材料中缺少可逐项核验的数值证据。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 标准训练（Standard Training）：在所有 ID/OOD 原子事实和 Train-II 上，以普通自回归方式训练 Transformer。这是检验“只给原子知识和部分两跳示例”能否自然学会组合推理的主基线。
- 表征式训练（Representation-Based Training）：先由已泛化的标准模型提取桥接实体和第二跳关系在第 $5$ 层的隐藏表征，再把 OOD 原子事实的表征对输入第 $6$ 至第 $8$ 层并监督其输出。这一对照直接针对上层不会读取中间表征的解释。
- 循环式训练（Looped Training）：论文提出的 recurrent-style 策略，目标是让 Transformer 在不同输入形式间复用推理电路。它应与标准训练比较，以判断结构/训练路径复用是否解决第二跳 OOD 的失配。
- 分布条件对照：Test-II、Test-OI、Test-IO、Test-OO 并非不同模型，但构成关键比较组。它们保持两跳任务形式一致，只改变两跳各自来自 ID/OOD 的位置，因此可定位第二跳 OOD 是否是失败条件。

**实验想回答的问题**

- 在模型已经见过全部单跳原子事实、且训练过部分 ID-ID 两跳组合的条件下，Transformer 能否把两个已知单跳事实组合为未见两跳答案；这种泛化是否取决于第二跳属于 ID 还是 OOD？
- 若失败来自“下层已形成桥接实体表征、上层却不会基于该表征执行第二跳”的层间失配，那么以中间表征为输入训练后层，以及循环复用推理电路，能否改善 OOD 第二跳上的两跳泛化？

**实验实现**

主实验训练一个 GPT2 风格、decoder-only 的 Transformer，模型有 $8$ 层、隐藏维度为 $768$，使用 AdamW，学习率为 $1\times10^{-4}$。训练数据包括全部原子事实（ID 和 OOD）及 Train-II；Test-II、Test-IO、Test-OI、Test-OO 均不参与训练。合成数据设置中取 $\phi=7.2$，即以 ID 原子事实数量的 $7.2$ 倍抽取 Train-II，以保证 Test-II 可出现泛化而训练成本不过高。标准训练、表征式训练与循环式训练的优化步数和训练时长分别报告为 $3{,}500{,}000/263.05$ 小时、$7{,}750/0.88$ 小时、$1{,}212{,}500/86.80$ 小时；但该表仅报告成本，不能据此比较各方法的最终准确率。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Logit lens 个案分析显示，在记忆阶段，即使桥接实体 $e_2$ 的表征尚不清晰，最终答案 $e_3$ 的概率也会变得显著；而第一泛化阶段，在 $r_2$ 位置第 $6$ 层开始 $r_2$ 概率下降、$e_3$ 概率上升，作者据此把第 $5$ 层 $r_1$ 位置的隐藏状态 $h_5(r_1)$ 定为桥接实体表征。这一观察支持“早期直接记忆终答、后期经中间状态执行第二跳”的解释，但它是模型内部读出证据，不能独立替代干预因果证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper mechanistically explains two-hop reasoning failures in transformers and proposes training changes to improve out-of-distribution reasoning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`ade27bb54d8590ea523bfe48035996164354adf809887dfc1e47c7c19052ca20`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
