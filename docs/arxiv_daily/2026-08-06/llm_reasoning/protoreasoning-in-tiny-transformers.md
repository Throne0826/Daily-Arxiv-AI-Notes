---
title: "[论文解读] Protoreasoning in Tiny Transformers"
description: "[arXiv 2608.04980][LLM Reasoning] 本文研究约$1M$参数的微型Transformer能否通过一种面向Dyck语言的原始链式思维形式学习更具泛化性的逐步推理，而不只是记忆输入模式或依赖局部启发式规则。"
arxiv_id: "2608.04980"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:52:24.220452+00:00"
source_sha256: "063d1e857f49e380f31e0a37d34db57f23f20698d2c329da9c560a26401f4646"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "微型 Transformer"
  - "原型推理"
  - "思维链"
  - "Dyck-$k$ 语言"
  - "形式语言"
  - "程序性推理"
  - "分布外泛化"
  - "算法学习"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.04980</p>

# Protoreasoning in Tiny Transformers

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Eduardo Valle, Fergal Reid</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Eduardo Valle Fin AI Research；Fergal Reid Fin AI Research</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04980v1) · [PDF 下载](https://arxiv.org/pdf/2608.04980v1) · **关键词** 微型 Transformer, 原型推理, 思维链, Dyck-$k$ 语言, 形式语言, 程序性推理, 分布外泛化, 算法学习<br>


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

本文研究约$1M$参数的微型Transformer能否通过一种面向Dyck语言的原始链式思维形式学习更具泛化性的逐步推理，而不只是记忆输入模式或依赖局部启发式规则。

**不用术语来说**：大型语言模型在数学、逻辑和编程任务中常能生成逐步解题过程，但研究者仍不清楚这些过程是否体现了真正可迁移的算法。直接在大型模型上回答这一问题代价高、训练数据不透明，也难以进行大量受控实验。因此，本文尝试用很小的模型和结构可控、答案可精确验证的括号任务，检验显式中间步骤究竟是否能帮助模型处理训练分布之外的样本。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出并验证一种称为protoreasoning的原始逐步推理形式：模型在解决Dyck语言任务时生成确定性的中间轨迹，反复删去不可能属于答案的树节点；该设计使远低于自然语言能力规模的微型Transformer也能表现出有用的逐步推理。
- 构造基于Dyck-$k$语言与树森林对应关系的两个推理友好任务，并利用可控制的难度轴、精确的合法性判定和大规模受控实验，研究推理轨迹对分布外泛化的影响。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型逐步推理与形式语言学习的交叉点。思维链（Chain of Thought, CoT）通过让模型输出中间步骤来提高数学、逻辑和代码任务的准确率，但前沿模型训练成本高、训练数据不透明，而且输出的推理过程未必忠实反映其内部计算，因此难以用大量受控实验判断模型究竟学到了可泛化算法，还是仅组合了一组只在特定输入模式下生效的启发式规则。本文把研究对象缩小到约 $10^6$ 参数的微型 Transformer，并以可精确生成、控制难度和自动验证的 Dyck 形式语言作为实验环境，从而在远低于自然语言推理所需规模的模型上研究一种原始的逐步推理形式。这里考察的是有限长度数据上的经验学习与分布外泛化，而不是证明固定 Transformer 能识别任意长度的完整 Dyck 语言。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链与原型推理**

思维链要求模型在最终答案之前生成一系列中间步骤，使复杂计算被分解为较简单的连续操作。本文将适合微型模型的确定性中间轨迹称为“原型推理”（protoreasoning）：模型通过反复删去不可能属于答案的树节点来逐步求解。

</div>
<div class="concept-item" markdown="1">

**Dyck-$k$ 语言**

Dyck-$k$ 语言由至多 $k$ 种括号构成，其中每个左括号都必须由同类型右括号按正确的嵌套次序闭合；它是典型的上下文无关语言，也是测试递归结构处理能力的标准对象。Dyck 句子与有序树组成的森林存在自然对应：外层括号表示祖先节点，嵌套括号表示向子节点深入。

</div>
<div class="concept-item" markdown="1">

**分布外泛化**

分布外泛化指模型在结构复杂度、长度或其他属性超出训练数据范围时仍能正确求解。它比同分布准确率更能区分模型是否掌握了可复用程序，因为局部模式匹配或狭窄启发式规则通常会在输入结构改变后失效。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文利用 Dyck-$k$ 句子与树森林之间的对应关系构造两个“推理友好”任务：输入是一个括号类型不超过 $k$、正确平衡且正确嵌套的有限长度 Dyck 句子，也可等价地视为一片树森林；输出是由相应任务定义的答案。模型可直接预测答案，也可先生成确定性的原型推理轨迹，再给出答案；轨迹的基本操作是反复剪除确定不可能属于答案的节点。研究设置采用约 $10^6$ 参数的微型 Transformer、合成且结构可控的数据以及可精确判定的输出，重点比较模型在训练分布内与更困难分布外实例上的表现。所给章节没有说明两个任务各自的完整输入输出规则、长度边界或具体数据划分，因此这些细节不能从当前材料进一步确定。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$k$**

Dyck 语言允许使用的括号类型数；Dyck-$k$ 中每对括号必须按类型匹配并正确嵌套。

</div>
<div class="notation-item" markdown="1">

**$n$**

形式语言理论分析中的输入序列长度；相关复杂度与精度结论可能随 $n$ 增长。

</div>
<div class="notation-item" markdown="1">

**$O(\log n)$**

随输入长度 $n$ 对数增长的数量级；相关工作用它描述某些 Transformer 表达能力结论所假设的数值精度。

</div>
<div class="notation-item" markdown="1">

**$\sim 10^6$**

本文所研究微型 Transformer 的近似参数规模，即约一百万参数。

</div>

</div>

**直接相关的工作**

- **Hahn (2020)**: 该工作证明，在有限精度和 Lipschitz 连续注意力等假设下，固定的 Transformer 解码器无法识别足够长输入上的完整 Dyck-2 语言。本文研究长度受限的有限样本学习和经验泛化，因此不与这一关于无界长度语言的渐近不可能性结果冲突；该区别限定了本文结论的适用范围。
- **Vafa et al. (2024)**: 该工作用正规自动机检验 GPT-2 风格模型是否学到真实状态转移结构，发现很高的下一词元预测准确率仍可能伴随轻微分布偏移下的彻底失败。它直接支持本文的评估立场：局部分布内预测表现不足以证明模型掌握了底层算法，因而需要结构可控的形式语言和分布外测试。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

当前大型语言模型的链式思维通常能提升数学、逻辑和代码推理表现，但其成功原因仍不清楚：模型可能学习了可迁移的程序，也可能只是组合了许多只适用于局部输入的启发式规则。这个科学问题对理解模型可靠性和推理能力的边界具有直接意义，但前沿模型训练成本高、训练数据不透明，难以通过重复训练、系统消融和机制分析获得有说服力的证据。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **前沿大型语言模型上的自然语言链式思维**：模型先生成若干自然语言或符号化的中间步骤，再依据这些步骤给出最终答案；这种推理时过程通常用于提升数学、逻辑和编程任务的准确率。
- **微型Transformer与形式语言任务**：研究者使用参数量很小的Transformer作为可控的“模型生物”，并在Dyck语言等形式语言上训练。Dyck语言由正确嵌套的括号组成，样本结构可人工生成，合法性可以精确检查，因而能够分别控制任务难度并测量分布内和分布外泛化。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 前沿模型的训练成本和数据不透明性使研究者难以进行密集的重复实验、结构化消融和机制分析；因此，即使模型在复杂任务上展示逐步推理，也很难判断其是否学习了真正一般的算法。
- 已有证据表明模型在足够复杂的计算任务上会失败，且其算法行为可能来自针对特定输入触发的“启发式规则集合”；同时，部分链式思维可能只是对已生成答案的事后解释，而非事先参与决策的推理过程。这会削弱其分布外泛化能力，也使表面上的推理文本难以作为算法学习的可靠证据。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未在一个成本低、数据完全可控、答案可精确验证的环境中，系统分离“额外中间词元带来的计算容量”与“中间轨迹内容本身带来的算法指导”，并检验微型模型能否借助这种轨迹缩小分布内与分布外合法性之间的差距。特别是，在模型远低于自然语言推理能力规模时，显式且可验证的步骤是否仍能促进可迁移的结构学习，缺少直接答案。

</div>
<div markdown="1"><span>核心问题</span>

在约$1M$参数的微型Transformer上，为Dyck语言任务提供内容明确、可逐步验证的protoreasoning轨迹，是否比不提供推理轨迹或仅增加等量无关词元，更能促进模型对训练分布之外样本的泛化？

</div>
<div markdown="1"><span>作者直觉</span>

Dyck语言中的括号嵌套可以对应树森林；模型若直接从输入映射到答案，容易记住训练样本中出现的局部结构。protoreasoning把求解过程改写为一系列确定的树节点删减操作，相当于把隐含的结构判断拆成连续、可复用的中间状态。这样，模型不必一次性猜出完整答案，而可以在每一步利用前一步留下的结构信息；若性能提升来自轨迹中的有效操作，而不是单纯来自更长的序列，那么加入等量但无关的额外词元应无法产生同等收益。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文把形式语言中的确定性结构查询改写为微型 Transformer 可学习的序列生成问题。输入是一个正确嵌套、平衡且包含 $k$ 种括号的 Dyck-$k$ 句子；该句子可等价解释为树或森林，其中外层括号对应祖先节点，内层括号对应后代节点。模型执行两类任务：最深路径（DP）要求输出从根通向最深叶子的路径所对应的左括号；最大阶前叶（PL）要求找出全部子节点均为叶子的最大兄弟组，并输出相应左括号。两个任务遇到多个同优候选时均选择最右候选，输出中不保留右括号。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造 Dyck 结构查询样本

将括号嵌套关系解释为树或森林，并用确定性规则计算答案：DP 选择通向最深叶子的路径，PL 选择规模最大的全叶兄弟组；并列时取最右候选。句子以半长度 $\mathrm{hl}$ 表示括号对数量，同时按任务相关结构参数分层，DP 使用深度，PL 使用最大前叶阶数。

<div class="method-step__io" markdown="1">

**输入**：由 $k$ 类括号组成的合法 Dyck-$k$ 句子，以及任务类型 DP 或 PL。<br>
**输出**：仅由左括号构成的唯一目标答案，以及样本的半长度和结构参数。

</div>

**直观理解**：括号的包含关系可以看成树的父子关系，因此任务不是判断括号是否合法，而是在这棵树上寻找一条最深路径或一组最大的叶子兄弟。确定性的并列规则保证每个输入只有一个标准答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成原始格式或原型推理格式

原始格式按“输入句子、任务分隔符、答案”排列；原型推理格式在分隔符后加入状态序列 $s_1,\ldots,s_m$，其中每个 $s_i$ 都由前一状态 $s_{i-1}$ 删除不可能属于最终解的树节点得到，并用专用标记划分推理轨迹和最终答案。

<div class="method-step__io" markdown="1">

**输入**：Dyck 输入句子、任务分隔符和已计算的目标答案。<br>
**输出**：可直接用于序列模型训练的 vanilla 样本或 trace 样本。

</div>

**直观理解**：vanilla 样本只告诉模型题目和答案，trace 样本则展示逐步排除错误候选的过程。所谓“原型推理”并非自然语言解释，而是一串越来越精简的括号结构。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行任务特定剪枝并施加步骤丢弃

DP 每一步删除当前仍存在的最浅叶子，直至结构退化为一条路径；PL 从根部逐层剥离，并在至少两棵树只剩两层时删除其中最小者，直至仅余一棵树。若待删除候选并列则先删最左者；训练时再以 $15\%$ 概率独立跳过每个中间步骤。

<div class="method-step__io" markdown="1">

**输入**：初始括号树或森林，以及完整的确定性剪枝轨迹。<br>
**输出**：可能省略部分中间状态、但仍指向同一最终答案的原型推理轨迹。

</div>

**直观理解**：DP 像不断擦掉较浅的枝叶，最后留下最深路线；PL 像逐轮淘汰较小的候选子树。随机跳步使模型不能只记住固定的相邻状态变换，而要适应不同粒度的推理过程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 训练微型模型并进行无轨迹提示测试

使用四层、残差宽度为 $128$、含 $16$ 个注意力头且不采用分组查询注意力的微型 Llama 2 解码器训练；所有处理均使用 SkipAlign 扩充位置索引分布。测试提示只包含从起始标记到任务分隔符的前缀，模型自行续写；评测程序从 $\langle\mathrm{EOT}\rangle$ 之后截取最终答案，若不存在该标记则从任务分隔符之后截取，并在 $\langle\mathrm{EOS}\rangle$ 前停止。

<div class="method-step__io" markdown="1">

**输入**：经过位置增强的 vanilla 或 trace 训练序列，以及按结构参数划分的训练、验证和测试层。<br>
**输出**：模型生成的轨迹及最终答案，或直接生成的答案；随后依据答案对当前输入是否正确计算 validity。

</div>

**直观理解**：测试时不会把推理步骤作为提示送给模型，因此性能提升必须来自训练中学到的逐步处理方式。截取规则把中间轨迹与最终作答分开，使 trace 模型和 vanilla 模型可按同一答案标准比较。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文第 2 节没有明确写出损失函数或给出中心优化方程，因此不能据此补造具体目标。方法层面的监督信号是完整的目标序列：vanilla 处理监督模型续写最终答案，trace 处理额外监督模型续写剪枝状态序列及其后的最终答案；二者最终都以答案有效性而非轨迹文本相似度作为主要任务评测。由于使用的是 Llama 2 式解码器，可确认任务被实现为前缀后的序列续写，但具体 token 级损失、标签屏蔽范围及优化器配置在所给章节中原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 任务特定的确定性剪枝器**

剪枝器利用 Dyck 句子与树结构的一一对应关系，为 DP 和 PL 生成不同的状态转移。DP 反复移除最浅叶子，PL 通过根部剥离与较小候选淘汰缩减森林；删除并列候选时取最左者，而最终任务答案的并列选择取最右者。

> 直观理解：该模块相当于生成教师示范：它不直接给自然语言理由，而是展示哪些括号可以逐步删除。左右并列规则固定后，同一个输入会产生可复现的轨迹和唯一答案。

**2. 步骤丢弃**

对于 trace 处理中的每个推理状态，训练时以 $0.15$ 的概率独立跳过。它改变可见轨迹的步长，但不改变输入问题和最终标准答案。

> 直观理解：如果每次都展示完全相同的细碎步骤，模型可能只学习机械复制相邻状态；随机省略若干步迫使它学会一次跨过不同数量的剪枝操作。

**3. SkipAlign 位置增强**

SkipAlign 是一种 PoSE 风格的位置编码数据增强，在特定边界插入位置索引间隙，使模型在不填充大量真实 token、也不承担长上下文二次注意力成本的情况下接触更多样的位置编码。论文将其用于所有处理，以缓解 trace 序列长度范围更宽、标准旋转位置编码 RoPE 对未见位置分布不利这一混杂因素。

> 直观理解：推理轨迹会让样本明显变长；若不处理，trace 模型可能只是因为测试位置超出训练经验而吃亏。SkipAlign 类似在训练时人为改变 token 的“位置刻度”，从而让比较更接近对推理内容本身的比较。

**训练与推理**

训练前，生成器持续采样新的 Dyck-$4$ 句子；默认每句含 $\mathrm{hl}=32$ 对括号，并依据深度或最大前叶阶数归入结构层。结构层按照 Random、Blocks、Even、Middle、High 和 Low 六种留出模式划分为互不相交的训练、验证与测试集合，其中前四种主要检查不同距离的插值泛化，High 和 Low 主要检查外推泛化。每种处理进行一次含 $8$ 个试验的准随机超参数搜索，该搜索只在第一个随机种子上运行；最终结果跨 $10$ 个影响权重初始化和训练数据采样的随机种子平均。训练样本从规模足够大的生成器中动态抽取，论文认为模型在实践中不会重复看到同一句子。

推理时，无论模型接受 vanilla 还是 trace 训练，都只获得输入句子及其任务分隔符，不会获得任何预先写好的推理状态。trace 模型需要从此前缀自行续写训练格式中的轨迹和答案，vanilla 模型则直接续写答案。评测提取 $\langle\mathrm{EOT}\rangle$ 与 $\langle\mathrm{EOS}\rangle$ 之间的内容作为输出；若未生成 $\langle\mathrm{EOT}\rangle$，则改取任务分隔符之后、$\langle\mathrm{EOS}\rangle$ 之前的内容。主要报告未见测试结构层上的 OOD validity，即最终输出对给定输入是否完全正确；新训练批次上的 validity 则反映已见结构层内的新样本泛化。

**复现信息**

默认模型约为百万参数量级，具体结构为微型 Llama 2：$4$ 层、残差宽度 $128$、$16$ 个注意力头，并移除分组查询注意力。形式语言默认采用 Dyck-$4$，输入半长度为 $\mathrm{hl}=32$；DP 与 PL 使用不同任务分隔符，轨迹由专用的开始、结束和换行 token 分隔。PL 还有一个边界约定：若输入森林全部由单节点树组成，例如连续的若干对空括号，则整个森林被视为最大的兄弟组。

公平解释结果时最关键的控制是：所有处理都使用 SkipAlign，而非只给 trace 处理使用；trace 的默认步骤丢弃概率为 $15\%$，并对每一步独立采样。论文指出微型模型接近容量极限，不同初始化和数据采样可能造成从完全失败到完全成功的波动，因此单次运行不可靠，需结合 $10$ 个随机种子的平均值理解结果。所给章节未明确报告优化器、学习率、批大小、训练步数和精确参数总量，这些信息据称位于附录，复现时需要进一步核查原文。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Deepest Path（DP）合成任务：数据由正确嵌套括号构成的 Dyck 语言句子生成，并可解释为树；任务要求输出最深路径。样本按半长度与树深度划分为 strata（分层）。单分层实验用于区分域内表达能力与跨分层泛化，多分层实验则通过 Random、Blocks、Even、Middle、High、Low 六种留出模式构造训练、验证和测试集合。原文未明确报告各集合的样本总数。
- Maximum-order Preleaf（PL）合成任务：输入同样是分层生成的 Dyck 句子，目标是输出最大序号的 preleaf；preleaf 可理解为其子节点均为叶节点的内部节点。数据按半长度与 maximum preleaf 结构参数分层，并采用与 DP 相同的六类留出模式，作用是检验模型能否在未见过的长度或结构区域上泛化。原文未明确报告各集合的样本总数。
- DP+PL 混合任务集合：一个模型同时学习 DP 与 PL，输入中的分隔符 $|$ 或 $!$ 指示应完成哪项任务。数据联合考虑 depth 与 maximum preleaf，只保留具有足够样本多样性的参数组合；Even Mixed、Middle Mixed 和 High Mixed 分别测试联合分层下的插值或外推。该设置用于判断推理轨迹能否减轻多任务干扰，而不是引入新的自然语言数据集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**输出有效率（output validity, %）**

测试输出满足任务正确性要求的样本比例；论文对相关测试 strata 求平均，并汇总 10 个随机种子的均值与标准差。它衡量完整输出是否有效，而不是局部 token 准确率。 （越高越好，因为更高比例表示模型在相应域内或分布外分层上生成了有效答案。）

</div>
<div class="metric-item" markdown="1">

**跨随机种子标准差**

10 个随机种子所得输出有效率的离散程度，用于观察训练结果是否稳定；例如外推设置中的较大标准差意味着结论对初始化或训练随机性更敏感。 （越低通常越好，因为在均值相近时，较低标准差表示结果更稳定；但它不能脱离平均有效率单独判断模型质量。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 单一 stratum 的 vanilla 模型：域内表达能力与长度、结构 OOD 泛化

<div class="result-value" markdown="1">

模型在域内几乎完美，但结构 OOD 基本归零。例如 DP 在训练半长度 32、深度 16 时，域内有效率为 $99.8\pm0.5\%$，长度 OOD 为 $34.9\pm13.5\%$，结构 OOD 为 $0.0\pm0.0\%$，双轴 OOD 为 $0.2\pm0.2\%$；PL 在训练半长度 64、maximum preleaf 16 时，域内为 $99.8\pm0.3\%$，长度 OOD 为 $91.1\pm10.3\%$，结构 OOD仅为 $0.2\pm0.5\%$。

</div>

作者据此主张，这些小模型拥有拟合复杂括号任务的容量，但没有自然获得跨结构的通用算法。分析上，长度变化有时仍能保留部分性能，而结构参数变化几乎摧毁有效率，因此实验难点主要不是训练内表达能力，而是结构性组合泛化。这不证明模型完全没有任何算法行为，因为这里只观察特定训练分层和 OOD 轴，也没有直接解析内部计算。

<div class="result-source" markdown="1">

来源：第 3.1 节；数值见表 1，分层可视化见图 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Near-perfect validity shows that the model has enough capacity to express the correct solution for in-distribution prompts, even for over a hundred brackets and very complex structure. However, the picture reverses out-of-distribution: validity is only partly retained along the length axis (hl), and all but vanishes along the structural axis (depth for DP, maximum preleaf for PL).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 多 stratum 单任务训练：trace 与 vanilla 在六种留出模式上的比较

<div class="result-value" markdown="1">

在四种插值模式中，trace 对两项任务均达到 $95\%$ 以上有效率，并通常优于 vanilla。差距在长距离插值时尤其明显：Middle 模式下，DP 从 $80.5\pm9.7\%$ 提升至 $98.0\pm2.0\%$，PL 从 $85.8\pm11.0\%$ 提升至 $97.1\pm1.1\%$。但外推仍困难：High 模式虽由 DP 的 $50.9\pm5.4\%$ 提至 $66.7\pm9.4\%$、PL 的 $23.9\pm24.3\%$ 提至 $62.2\pm7.3\%$，仍明显低于插值；Low 模式中 trace 甚至低于 vanilla。

</div>

作者的结论是原型推理轨迹几乎总能改善跨分层泛化，特别适合训练范围内部的长距离插值。更谨慎的解释是，trace 缩小而未消除 OOD 缺口，其优势依赖留出方向：Low 要求测试时产生比训练中更多的推理步骤，DP 和 PL 的 trace 分别降至 $21.6\pm7.4\%$ 与 $41.0\pm5.4\%$，低于 vanilla 的 $39.6\pm2.0\%$ 与 $43.9\pm3.0\%$。因此结果支持“轨迹改善泛化”，但不支持“轨迹使模型学会任意长度或结构上的完全通用算法”。

<div class="result-source" markdown="1">

来源：第 3.2 节；表 2；图 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the interpolation patterns (R, B, E, M) the trace format leads to validities above 95%, with small deviation across seeds. The extrapolation regime (H, L), however, is hard for both formats: validity drops precipitously and becomes much noisier.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### DP+PL 混合任务训练：分别在两项任务上评估 vanilla 与 trace

<div class="result-value" markdown="1">

trace 对混合任务干扰的耐受性总体更强。Even Mixed 中，DP 从 $62.7\pm33.2\%$ 提升至 $98.6\pm0.2\%$，PL 从 $74.4\pm15.8\%$ 提升至 $94.5\pm1.6\%$；Middle Mixed 中，PL 从 $60.5\pm24.1\%$ 提升至 $94.8\pm1.7\%$。High Mixed 的 DP 是例外，trace 为 $43.0\pm4.9\%$，低于 vanilla 的 $46.6\pm5.2\%$，但 PL 从 $17.7\pm13.7\%$ 提升至 $60.5\pm7.7\%$。

</div>

作者据此认为，显式轨迹比直接答案格式更能维持多任务条件下的泛化。混合训练没有优于对应的纯任务训练，因此未观察到预期的跨任务迁移；这更符合“每项任务的解法绑定方式仍限制泛化”的解释。该结果不能证明 trace 已彻底解决任务干扰，因为 High Mixed 的 DP 没有改善，而且实验只包含两个高度相关的合成任务。

<div class="result-source" markdown="1">

来源：第 3.3 节；表 3；图 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Tab. 3 shows that mixed-task training is more challenging for both formats, but that validity drops much more for vanilla than for trace.

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

- Vanilla 输出格式：模型直接生成任务答案，不输出中间步骤。它与 trace 使用相同任务和模型规模，因此是判断显式中间推理是否改善泛化的核心对照。
- 单一 stratum 训练的 vanilla 模型：只在一个半长度与结构参数组合上训练，再分别测试域内、长度 OOD、结构 OOD 和双轴 OOD。该基线用于确认模型有能力拟合任务，同时揭示拟合成功不等于学会可迁移算法。
- Erased trace：训练时将推理轨迹逐 token 替换为点号，尽量保留额外序列长度，却删除中间步骤的语义内容。它直接检验 trace 收益是否仅来自更多 token 或更大的串行计算预算。
- 不使用或部分使用增强的模型：比较普通 RoPE、加入 SkipAlign，以及 trace 再加入 step dropout 的版本，用来分离位置编码扰动和推理步骤随机丢弃对泛化的作用。

**实验想回答的问题**

- 约百万参数的小型 Transformer 在 Dyck 括号语言任务上，是否只是拟合训练分层，还是能够跨长度与树结构分层进行分布外泛化；结构变化是否比长度变化更难？
- 显式原型推理轨迹能否比仅输出答案的 vanilla 格式更好地支持单任务与混合任务泛化；若能，收益究竟来自轨迹所表达的中间计算、额外 token 带来的计算预算，还是 SkipAlign 与 step dropout 等数据增强？

**实验实现**

评测首先固定 vanilla 格式并进行单 stratum 训练，分别在域内、仅半长度变化、仅结构变化以及两者同时变化的 strata 上测试。随后从多个 strata 训练，以 Random、Blocks、Even、Middle、High、Low 留出模式划分训练、验证和测试；其中前四类主要考查插值，High 与 Low 主要考查外推。单任务模型分别在 DP 或 PL 上训练和评估，混合模型则同时训练两项任务后分别报告 DP 与 PL 有效率。所有表格结果均为相关测试 strata 上的平均输出有效率，并对 10 个随机种子报告均值与标准差。两种格式均可使用 SkipAlign，在位置编码索引中引入间隔；trace 还使用 step dropout，随机跳过 15% 的推理步骤。原文节选未明确报告优化器、训练步数、参数量的精确值、每个 stratum 的样本数或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 将 trace 的中间内容逐 token 替换为点号，与完整 trace 比较 | 删除轨迹语义后性能大幅下降。DP 的 Random 模式从完整 trace 的 $95.4\pm2.1\%$ 降至 erased trace 的 $9.8\pm9.0\%$，Blocks 从 $98.7\pm0.4\%$ 降至 $5.4\pm9.0\%$；PL 的 Random 从 $97.8\pm0.5\%$ 降至 $30.3\pm12.9\%$，High 从 $62.2\pm7.3\%$ 降至 $0.0\pm0.0\%$。 | 该消融尽量保留轨迹带来的额外 token 数量，同时移除每步所表达的中间计算，因此隔离了“内容”与“长度或计算预算”。结果支持作者关于轨迹内容确实重要的主张。不过，点号序列与结构化轨迹在 token 分布和可学习性上也不同，所以它排除了简单的纯长度解释，却未严格证明所有收益都来自人类预期的逐步算法。 | 第 3.4 节；表 4<br><span class="experiment-evidence">To exclude that possibility, we implement a “dot-by-dot” replacement of the reasoning traces at training time, which dramatically deteriorates validity, showing that the trace contents indeed contribute to the validity improvements.</span> |
| 逐步加入 SkipAlign 与 step dropout，比较未增强、仅 SkipAlign、两者并用的 trace | SkipAlign 对两种格式和两项任务总体有益；在 trace 上继续加入随机丢弃 $15\%$ 推理步骤的 step dropout，尤其改善轨迹较长的 DP。例如 DP Random 从未增强的 $59.8\pm24.4\%$ 提至仅 SkipAlign 的 $85.2\pm8.5\%$，再提至两者并用的 $94.4\pm1.7\%$；DP Even 相应为 $64.6\pm38.7\%$、$91.7\pm20.1\%$ 和 $99.1\pm0.3\%$。但 PL Blocks 从仅 SkipAlign 的 $97.2\pm0.9\%$ 略降至加入 step dropout 后的 $97.1\pm0.6\%$，说明该增强并非所有设置都单调受益。 | SkipAlign 通过扰动位置索引，减少模型把绝对位置当作捷径的可能；step dropout 则迫使模型在缺少部分中间步骤时仍保持计算连续性。DP 轨迹更长、跨 strata 的步骤数变化更大，因此正则化收益更明显；PL 轨迹较短，删除步骤可能轻微损伤有效信息。该消融表明最终 trace 结果包含增强策略的贡献，不能把全部增益只归因于输出格式本身。 | 表 4 标题说明；第 3.4 节<br><span class="experiment-evidence">Both data augmentations (SkipAlign and step dropout) help improve generalization, especially on deepest path, which has longer reasoning traces.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该论文研究小型 Transformer 的链式思维原型及其对算法泛化和逐步推理的作用。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`063d1e857f49e380f31e0a37d34db57f23f20698d2c329da9c560a26401f4646`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
