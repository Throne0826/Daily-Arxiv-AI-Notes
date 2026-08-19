---
title: "[论文解读] T-LLM Compiler: Trusted LLM-based Code Optimization and Verification Framework"
description: "[arXiv 2608.14953][LLM Reasoning] T-LLM Compiler让大语言模型负责传统编译器难以实施的源代码改写，再以编译器、符号验证器和大语言模型组成的迭代验证流程筛除错误结果，从而在保留传统编译优化能力的同时扩大可探索的优化空间。"
arxiv_id: "2608.14953"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:22:57.452161+00:00"
source_sha256: "1fdeff2bd8198e185d1036fc0cca1c44e2f196952d1243394ee2957d78de30f8"
tags:
  - "LLM Reasoning"
  - "大语言模型辅助编译"
  - "代码优化"
  - "优化编译器"
  - "程序等价性验证"
  - "LLVM-IR"
  - "可信代码生成"
  - "迭代式程序变换"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.14953</p>

# T-LLM Compiler: Trusted LLM-based Code Optimization and Verification Framework

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Zahra Fazel, Sunanda Gamage, Shayan Shirahmad Gale Bagi, Amir H. Ashouri, Tomasz S. Czajkowski, Bryan Chan, Reza Azimi, Yaoqing Gao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Huawei Technologies, Heterogeneous Compiler Lab , Toronto , Canada；Huawei Technologies, Heterogeneous Compiler Lab；Affiliation: Huawei Technologies, Heterogeneous Compiler Lab</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14953) · [PDF 下载](https://arxiv.org/pdf/2608.14953) · **关键词** 大语言模型辅助编译, 代码优化, 优化编译器, 程序等价性验证, LLVM-IR, 可信代码生成, 迭代式程序变换<br>


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

T-LLM Compiler让大语言模型负责传统编译器难以实施的源代码改写，再以编译器、符号验证器和大语言模型组成的迭代验证流程筛除错误结果，从而在保留传统编译优化能力的同时扩大可探索的优化空间。

**不用术语来说**：程序员可以通过改写算法、循环或数据访问方式，让编译器生成更快的机器代码，但这种改写需要同时理解算法、硬件和编译器行为，难以自动完成。大语言模型虽能提出更大胆的代码改写，却可能生成无法编译、行为改变或仅在部分输入上正确的程序，因此实际问题不是单纯让模型“写出更快的代码”，而是如何可靠地得到既能通过后续编译优化、又保持原程序语义的改写结果。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出接近作者所定义“编译器 AI 辅助等级 3”的 T-LLM Compiler：将大语言模型的源代码级优化与传统编译器的低层优化串联，使模型主要负责打开编译器原本无法进入的优化空间，而不替代成熟的编译器基础能力。
- 提出自动迭代的优化与验证框架，综合使用编译器语法检查、Alive2、CBMC及大语言模型检查优化结果，并在验证失败后重试，以提高生成优化程序的可用性与正确性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于编译器优化与大语言模型辅助程序变换的交叉领域。传统优化编译器通过中低层代码变换降低程序运行时间、功耗或代码体积，但其决策通常依赖人工启发式规则，而且受编程语言语义、目标硬件特性及复杂变换实现成本的限制。现有机器学习方法多用于预测某项既有编译器变换是否有利，强化学习自动调优器则搜索编译选项；相比之下，大语言模型可以直接改写源代码或中间表示，甚至实施传统编译器通常不会进行的算法级修改，因此扩大了优化空间，但也引入语法错误、语义偏离和结果无法验证等可信性问题。本文将这种方向界定为大语言模型与传统编译器协同工作，而不是由模型完全替代编译器。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**优化编译器**

优化编译器在保持程序行为不变的前提下变换代码，以改善运行时间、功耗或代码体积。传统编译器通常依赖预先实现的变换及启发式收益判断，难以自动完成幅度较大的算法级改写。

</div>
<div class="concept-item" markdown="1">

**LLVM 中间表示**

LLVM-IR 是位于高级源代码与机器指令之间的低层程序表示，便于编译器统一分析和优化不同语言编写的程序。本文相关验证工具可比较变换前后的 LLVM-IR，以判断优化是否保持原有语义。

</div>
<div class="concept-item" markdown="1">

**程序等价性验证**

程序等价性验证用于判断原程序与优化程序是否在允许的输入范围内产生相同行为，而不只是检查代码能否编译。Alive2 主要验证 LLVM-IR 变换，CBMC 等工具则可通过符号推理检查更复杂的程序性质，但各自都有适用范围和能力限制。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究任务的输入是待优化程序及其编译上下文，输出是经大语言模型改写、能够通过编译并经多种验证手段确认正确的高性能程序。基本假设是：大语言模型可以提出传统编译器难以实施的源代码或算法级优化，但模型生成结果本身不可信，必须在迭代流程中接受语法检查、符号验证和语义检查；验证失败的信息还可用于继续修正代码。论文以编译器 AI 辅助等级描述系统定位：等级 0 使用纯启发式编译器，等级 1 用机器学习判断既有变换的收益，等级 2 让大语言模型作为顾问进行较实质的代码改写，等级 3 将更复杂的大语言模型变换序列与传统优化编译器协同集成，等级 4 再联合更广泛的分析和优化工具。T-LLM Compiler 旨在接近等级 3，其问题核心不是单次生成一段更快的代码，而是在扩大优化空间的同时，通过自动化验证维持程序正确性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **LLM Compiler**: 该工作以 LLVM-IR 为输入，训练模型生成面向代码体积的优化结果或预测 LLVM pass 序列。原文报告其直接生成结果有 95.6% 能成功编译，但只有 20% 与期望的编译器输出匹配，且没有执行运行时正确性检查；在 pass 推断设置中，无效序列会回退到 $-Oz$，最终变换仍由 LLVM 完成。它说明模型能够参与低层优化，却没有充分解决直接变换的正确性与成功率问题。
- **LLM-Vectorizer**: 该系统使用 GPT-4 生成 AVX2 向量化代码，并用 Alive2 比较变换前后的 LLVM-IR，在 TSVC-2 上验证了“生成后检查并重试”的系统化路线。原文称其正确生成比例为 52%，且增加尝试次数能够提高成功率；不过 Alive2 处理复杂循环结构的能力有限，因此该方案集中于特定向量化场景，尚不能提供覆盖多类代码变换的综合验证框架。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

优化编译需要算法、计算机体系结构和目标平台等多方面知识；与此同时，编程语言约束和低层变换日益复杂，使通用编译器难以自动完成程序员可能实施的算法级或源代码级改写。现实需求因而是建立一种自动化流程，在降低专家介入成本的同时，生成能够继续受益于传统编译器、且经过可信正确性检查的高性能程序。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **机器学习启发式与强化学习自动调优**：机器学习模型通常替代编译器中手写的收益判断规则，预测某项既定变换是否值得应用；强化学习自动调优器则通过选择编译选项，引导对大量参数和候选配置的搜索。实际代码变换仍由传统编译器执行，因此其正确性主要继承自编译器已有实现。
- **大语言模型代码优化**：大语言模型可以直接修改源代码，或在 LLVM 中间表示层面预测优化遍次顺序、实施从中间表示到中间表示的变换。与只选择现成编译优化的方案相比，这类方法可以尝试算法调整等更大幅度的改写。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 机器学习启发式和强化学习调优主要在既有编译变换或编译选项中作决策，无法主动重写输入程序来暴露新的优化机会；其结果是搜索效率可能提高，但优化空间仍受传统编译器已有能力限制。
- 大语言模型能够扩大变换空间，却会引入语法错误和算法语义错误；原文还指出，既有 LLVM 中间表示相关方法“have not improved the transformation success rate”。缺少覆盖多类错误并支持失败重试的验证机制，会使性能较好的候选程序仍难以被可信采用。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未形成一种编译器与大语言模型深度协作的自动化方案：它既要允许模型实施超出常规编译遍次能力的实质性代码改写，又要保留传统编译器擅长且成熟的低层优化，并通过语法、符号和语义层面的多重验证及迭代重试，将不正确的候选变换排除在最终结果之外。

</div>
<div markdown="1"><span>核心问题</span>

能否把大语言模型定位为传统编译器的优化协作者，使其负责改写源程序以解锁新的优化机会，再利用编译器和多种验证工具反复检查与修正候选代码，从而自动产出兼具性能收益和较高正确率的 C 程序？

</div>
<div markdown="1"><span>作者直觉</span>

传统编译器与大语言模型的能力具有互补性：编译器善于可靠执行已经形式化实现的低层变换，却通常不会主动改变算法或重构源代码；大语言模型善于模仿程序员进行更自由的改写，却不能天然保证正确。作者的切入点是让模型先把程序改写成更容易被编译器优化的形式，再由 BiSheng 编译器完成其擅长的低层优化，同时用不同验证工具从互补角度过滤错误，并在失败时重新生成。通俗地说，这相当于让模型提出优化方案，让编译器继续完成专业加工，再由多名职责不同的检查者共同验收。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

T-LLM Compiler 是一个面向 C 语言循环优化的“生成—验证—修正”框架。系统接收待优化源码，先由策略推荐器判断五类循环变换中哪些适用，再把选中的变换示例、优化指令和原始代码交给 Qwen2.5-32B-Instruct 生成候选程序；候选程序依次经过编译器语法检查、CBMC 有界符号等价检查和大语言模型语义检查。若验证器拒绝候选程序，系统将错误说明连同原程序和失败版本重新组织为反馈提示，让优化器继续修正，直到得到通过验证的版本或达到最大迭代次数；测试用例和性能测量仅用于最终评估，不属于在线验证链。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 推荐优化策略并合成首次提示

经 LoRA-SFT 微调的 Qwen2.5-Coder-3B-Instruct 判断循环展开、循环融合、循环分块、循环分布和循环交换中哪些策略适用，并选择对应示例组成少样本上下文；若判断代码无需循环优化，则生成要求优化器原样返回代码的保守提示。

<div class="method-step__io" markdown="1">

**输入**：待优化的 C 语言代码片段。<br>
**输出**：包含原始代码、优化规则、推荐策略及零个或多个示例的优化提示。

</div>

**直观理解**：该步骤类似先由一个较小的“分诊模型”选择合适的工具和参考案例，再让较大的模型动手。它避免对所有程序机械套用同一种循环变换，也允许明确选择“不修改”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 生成候选优化程序

Qwen2.5-32B-Instruct 按提示执行循环变换，提示设计可采用零样本、单示例或双示例方式，并借助少样本学习与思维链式指导约束变换过程；模型按指定标签格式只返回候选 C 代码。

<div class="method-step__io" markdown="1">

**输入**：首次优化提示，或包含原程序、失败候选及验证反馈的修正提示。<br>
**输出**：一个候选优化程序。

</div>

**直观理解**：大模型在这里承担代码改写工作，但它的输出只被视为候选答案。示例展示“某种代码形态应如何变换”，格式约束则便于系统稳定提取生成代码。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 执行分层正确性验证

验证链先调用编译器的 -fsyntax-only 模式排除语法错误，再用 CBMC 在给定循环展开界限内检查两版本输出是否相等，最后由未微调的指令模型比较控制路径、数据依赖和程序功能；LLM 验证提示可根据 CBMC 的接受、拒绝或无结论状态调整。

<div class="method-step__io" markdown="1">

**输入**：原始程序与候选优化程序。<br>
**输出**：接受决定，或包含语法、符号执行及语义问题的拒绝反馈。

</div>

**直观理解**：三层检查由便宜到昂贵逐步过滤：先确认代码能被解析，再在有限范围内寻找反例，最后让模型检查形式化工具不易覆盖的语义问题。CBMC 的“拒绝”通常意味着已经找到违反等价断言的证据，而“接受”只表示限定范围内未发现反例。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 根据反馈迭代并输出

若候选被拒绝，反馈与失败代码被送入提示合成器，要求优化器针对具体错误重新生成；若验证通过或达到最大迭代次数，循环终止，随后使用提供的测试用例检查最终输出并测量性能。

<div class="method-step__io" markdown="1">

**输入**：验证决定、原始代码、当前候选代码和验证器反馈。<br>
**输出**：通过验证的优化程序，或在迭代上限处得到的最终候选程序及其评测结果。

</div>

**直观理解**：这相当于把编译错误或逻辑疑点直接写进下一轮修改意见，而不是让模型从头盲猜。需要注意，达到迭代上限并不等于候选已经被证明正确，因此最终输出的可信度取决于实际终止原因。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文没有给出推荐器微调所使用的显式损失函数或中央优化方程，因此不能确定其交叉熵形式、标签编码方式或多标签决策细节。可确认的监督目标是：给定代码片段，预测适用的五类循环优化，或预测“No Loop Optimization Needed”；这一目标服务于提示与示例选择，而不是直接学习生成优化代码。优化器 Qwen2.5-32B-Instruct 和 LLM 语义验证器在本文流程中依靠提示调用，原文未报告对二者进行任务微调。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 优化策略推荐器与提示合成器**

推荐器以 Qwen2.5-Coder-3B-Instruct 为基础，通过 LoRA-SFT 学习六类决策：五种预定义循环优化以及“No Loop Optimization Needed”。每种优化策略绑定一个示例，推荐结果决定下游提示包含哪些少样本演示；首次尝试失败后，提示合成器还会把原始代码、失败代码和验证反馈组合为修正提示。

> 直观理解：论文先研究了 16 种提示配置，但发现不存在对所有基准都最好的固定提示，因此让模型按输入代码选择策略和示例。负类“不需要优化”尤其重要，因为不必要的变换可能降低性能或破坏正确性。

**2. LLM 循环优化器**

优化器采用 Qwen2.5-32B-Instruct，目标变换限定为循环展开、循环融合、循环分块、循环分布和循环交换。它同时处理首次生成和验证失败后的修正：首次输入由优化规则、源码及可选示例构成，重试输入则额外包含上一版候选与验证器逐项反馈。

> 直观理解：限制变换类型使任务比开放式程序重写更明确，也让推荐器能够提供与策略对应的示例。优化器仍可能产生越界、遗漏尾部迭代、错误交换依赖循环等问题，所以它必须与后续验证链配合，而不能单独作为可信编译器。

**3. 语法—符号—LLM 三阶段验证链**

语法层通过编译器快速失败；符号层构造同时包含原函数与变换函数的 C 验证程序，为两者复制相同的非确定输入，并逐元素断言输出相等，然后调用 CBMC、cvc5 求解器和有限循环展开进行有界模型检查；语义层使用未微调的预训练指令模型判断功能等价，并可把 CBMC 的接受、拒绝或无结论作为提示上下文。论文试验过 LLVM IR 层的 Alive2，但系统所述验证链采用 CBMC 处理 C 级候选变换。

> 直观理解：CBMC 会把“是否存在某个输入使两版输出不同”转成求解问题：找到满足条件的输入即可拒绝变换，但在有限边界内找不到反例不能证明所有输入上都等价。LLM 语义检查用于补充 CBMC 因循环边界、浮点复杂度或超时而留下的覆盖缺口，但它本身也不是形式化证明。

**训练与推理**

推荐器训练数据来自 LORE，并排除 PolyBench/C 子集以避免与下游评测重叠。作者先保留速度提升超过 5% 的变异版本，得到约 17,000 个候选，再对五类循环优化做类别均衡抽样；同时从未过滤数据中抽取等量的性能下降超过 20% 的样本，作为“不应执行循环优化”的负例。最终数据共 3,418 条，其中 3,009 条用于训练、409 条用于验证；Qwen2.5-Coder-3B-Instruct 采用 LoRA 训练三轮，LoRA 秩为 32、缩放系数为 32、LoRA-plus 学习率比为 16。原文没有明确说明数据标签生成细节、多策略是否可同时出现、学习率、批大小或随机种子。

推理时，推荐器先输出适用策略及其配套示例，系统据此从 16 类已研究提示配置的设计空间中形成针对输入的提示；若无需优化，则要求保持原代码。Qwen2.5-32B-Instruct 生成候选后，验证链按语法、CBMC、LLM 语义检查的顺序运行。CBMC 可返回接受、拒绝或因超时等原因无结论：拒绝信息被认为比有限边界下的接受更可信，语义验证器因此使用与状态相适配的提示；无结论时退回不依赖 CBMC 决定的通用等价检查提示。任何拒绝都会触发带反馈的下一轮生成，直至验证成功或达到系统设置的最大重试次数。

**复现信息**

复现时最关键的是 CBMC 验证包装程序：原函数和优化函数必须接收内容相同的非确定输入，分别产生输出，再由主函数逐元素加入等价断言。论文示例调用为 cbmc --cvc5 --no-standard-checks --function main --unwind 20，其中关闭标准指针和数组边界等属性检查，把关注点集中在主函数中的等价断言，并以 cvc5 求解 SMT 约束；循环展开深度是有界证明范围而非全程序证明范围。

CBMC 的适用边界会直接影响结果解释。论文称 PolyBench/C 上矩阵规模需小于 15×15 才能成功完成验证，复杂数组计算使用浮点类型时可能过慢或失败，因此该设置改用整数数组元素；有限输入空间还可能造成“错误等价”，即边界外存在反例但 CBMC 仍接受。系统刻意不把运行测试放进在线验证链，因为测试环境准备与执行开销不符合编译流程；测试仅在生成流程结束后用于最终正确性和性能评估。原文节选未给出最大迭代次数、LLM 解码参数、语义验证所用具体模型、超时阈值及硬件配置，这些缺失会影响严格复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- PolyBench/C：30 个 C 语言数值计算内核，用于端到端评估代码转换、功能等价性和运行时间；原文未报告训练集、验证集或测试集划分。
- PolyBench/C 的 400 个验证测试案例：由不同提示策略下的多次运行构成，用于评估 CBMC Verifier 的分类准确率、误拒绝率和误接受率；这是验证器分析用的测试集合，而非独立的模型训练集。
- doitgen 内核：PolyBench/C 中的单个案例，用于展示优化器产生错误代码、验证器拒绝、反馈重试并最终得到正确优化的完整工作流；该案例还用于分析传统 BiSheng 编译器如何利用变换后的代码进一步进行向量化。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Transformed kernels / 转换率**

成功生成变换版本的内核比例，表示系统是否实际产出了优化代码，而不是在失败后退回原始代码。 （越高越好，但必须结合正确性解释；单独提高转换率可能意味着系统接受了更多错误变换。）

</div>
<div class="metric-item" markdown="1">

**Accuracy / 正确率**

经过测试套件验证后，功能上正确的变换函数比例，衡量优化代码是否保持原程序语义。 （越高越好；它反映功能等价性，但不能单独证明代码更快。）

</div>
<div class="metric-item" markdown="1">

**Average speedup / 平均加速比**

优化后运行时间相对于基准运行时间的平均性能改善；若变换错误，论文将该变换的加速比记为 $1.0$。论文还报告“正确转换内核的平均加速比”，用于排除错误变换对性能统计的影响。 （越高越好；大于 $1.0$ 表示更快，小于 $1.0$ 表示变慢。由于错误变换被记为 $1.0$，该指标可能掩盖错误样本，需与正确率共同观察。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 不同提示策略下的 Qwen2.5-32B-Instruct 结果，以及跨全部提示策略为每个内核选择最佳变换

<div class="result-value" markdown="1">

无示例 Base Prompt 的转换率为 $90.00\%$、正确率为 $80.00\%$、平均加速比为 $1.167$；在所有提示策略中为每个内核选择最佳变换后，转换率仍为 $90.00\%$，正确率达到 $100\%$，平均加速比为 $1.175$，正确转换内核的平均加速比为 $1.195$。表中另列出的叙述性结果将最佳平均加速比写为 $1.178\times$，与表 2 的 $1.175$ 不一致，需以原表或实验脚本核查。

</div>

提示示例和事后选择能够同时改善正确性与平均性能，说明提示设计是重要变量。这里的“Best of All Prompts”相当于为每个内核选择已知表现最好的结果，因此是上界式分析，不等同于一个在未知测试内核上无需额外选择成本即可达到的统一策略；它不能单独证明自动推荐器具有同等效果。

<div class="result-source" markdown="1">

来源：第 4.1 节 Optimizer Performance；表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

When selecting the best-performing transformation for each kernel across all prompting strategies, the T-LLM compiler framework demonstrated 90% transformation success and perfect functional correctness (100%), alongside the highest observed speedup of 1.178×.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 不同 LLM 的 Best of All Prompts 比较

<div class="result-value" markdown="1">

CodeLlama-7B 的转换率为 $6.67\%$、正确率为 $100\%$、平均加速比为 $0.99$；CodeLlama-13B 的转换率为 $10\%$、正确率为 $100\%$、平均加速比为 $0.97$；Qwen2.5-32B 的转换率为 $90\%$、正确率为 $100\%$、平均加速比为 $1.178$，正确转换内核的平均加速比为 $1.198$。

</div>

在论文给出的设置中，Qwen2.5-32B 明显更能产生可接受的优化变换，并带来正向性能收益；两个 CodeLlama 模型虽然被接受的变换正确，但几乎不产生有效转换，且平均运行时间略有下降。该结果支持“模型能力或模型-提示组合会影响优化成功率”，但由于模型、提示适配和推理配置的细节有限，不能仅凭此表归因于参数量。

<div class="result-source" markdown="1">

来源：第 4.1 节 Optimizer Performance；表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen2.5-32B-Instruct demonstrates a substantial performance advantage, markedly outperforming both CodeLlama variants across all reported metrics.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 完整 T-LLM Compiler 流程与不同验证链配置的端到端表现

<div class="result-value" markdown="1">

仅使用优化器时，转换率为 $100\%$、正确率为 $60\%$、平均加速比为 $1.13$；加入语法验证后正确率为 $73\%$、平均加速比为 $1.14$；加入 CBMC 后正确率为 $83\%$、平均加速比为 $1.19$；完整的 Optimizer + Syntax Verifier + CBMC + 3-way LLM 配置达到 $90\%$ 转换率、$87\%$ 正确率和 $1.16$ 平均加速比。CBMC 在 400 个测试案例上的准确率为 $87\%$、误拒绝率为 $8.4\%$、误接受率为 $33.8\%$。

</div>

验证链显著降低了错误优化被最终接受的比例，并通过失败后的重试提升正确率；平均加速比没有因验证而消失，说明验证并非简单地拒绝所有激进变换。不过，完整链的平均加速比低于只加入 CBMC 的配置，而且 CBMC 的误接受率较高，因此该系统提供的是经验性风险控制，而不是对任意 C 代码变换的完备正确性保证。

<div class="result-source" markdown="1">

来源：第 4.3 节 Verification Chain Ablations；表 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For example, accuracy improves from 60% in the no-verification baseline to 87% with the full verification chain.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测主要覆盖 30 个 PolyBench/C 数值内核，规模和程序类型较集中；原文未报告跨数据集、真实大型软件项目或独立测试集上的泛化结果，因此不能把这些结果直接推广到一般 C 程序。
- CBMC 在 400 个测试案例上的误接受率为 $33.8\%$，且 Alive2 在这些 C 级、深嵌套循环内核上经常超时；因此验证链虽提高经验正确率，却不能提供完备的语义等价性保证。CoT、提示策略和最佳提示结果也缺少充分的重复实验统计，部分表述还存在数值不一致。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- BiSheng Enterprise 编译器的 $-O3$ 优化结果：主要性能比较基线，用于衡量 T-LLM Compiler 生成的代码相对于现有编译器优化的运行时收益。
- BiSheng 与 GCC 在 $-O2$ 和 $-O3$ 下的原始内核运行结果：用于确认实验平台上的编译器和优化级别不会造成明显的基线偏差，而不是用于直接比较 LLM 的正确性。
- Optimizer only：只使用 LLM 优化器、不使用语法检查、CBMC 或 LLM 验证的消融基线，用于测量没有验证保护时的正确性和速度表现。
- 不同 LLM 的 Best of All Prompts 结果：CodeLlama-7B-Instruct、CodeLlama-13B-Instruct 与 Qwen2.5-32B-Instruct 的模型规模比较，用于测试模型能力对代码转换效果的影响。

**实验想回答的问题**

- 在包含提示示例选择、代码验证与重试机制的完整流程下，T-LLM Compiler 能否在 PolyBench/C 上生成既正确又具有运行时收益的优化代码？
- 不同提示策略、LLM 规模以及验证链配置如何影响代码转换率、功能正确性和加速效果？

**实验实现**

实验在一台具有 128 个核心、512GB 内存的 AArch64/ARM64 服务器上运行。系统以 PolyBench/C 内核为输入，通过不同的零样本、单示例和双示例提示调用 LLM 生成优化代码，再依次进行语法验证、CBMC 验证、LLM 验证和基于测试的验证；验证失败时根据反馈重新生成，最多进行 3 次优化尝试。性能由优化后的代码交给 BiSheng Enterprise 编译器后测量。提示策略覆盖循环展开、循环合并、循环分块、循环交换和循环分布等示例组合。模型包括 CodeLlama-7B-Instruct、CodeLlama-13B-Instruct 和 Qwen2.5-32B-Instruct。论文声称 BiSheng/GCC 及 $-O2$/$-O3$ 基线运行时间不存在统计显著差异，但未给出完整统计检验方法或置信区间。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 验证链逐步增加：Optimizer only、加入 Syntax Verifier、再加入 CBMC，以及完整的 CBMC + 3-way LLM 配置 | 正确率依次为 $60\%$、$73\%$、$83\%$ 和 $87\%$；平均加速比依次为 $1.13$、$1.14$、$1.19$ 和 $1.16$。加入 CBMC 后转换率降至 $90\%$，并出现 $7\%$ 的多次尝试；完整链的多次尝试比例为 $10\%$。 | 该消融隔离了各验证组件对正确性的贡献。语法验证主要排除不可编译或形式不合法的输出，CBMC 进一步检查有界执行下的语义等价性，LLM 验证则提供额外判断。正确率随验证增强而升高，但转换率和加速比不保证单调增加，说明更严格的检查会拒绝一部分变换，重试机制在此处是提高质量的重要补偿。 | 表 5，System performance with different verification setups on PolyBench/C<br><span class="experiment-evidence">Optimizer + Syntax Verifier + CBMC + 3-way LLM (3 prompts) \| 90% \| 10% \| 87% \| 1.16</span> |
| 自动提示推荐器是否启用 CoT 推理 | 启用 CoT 时，转换率为 $80\%$、正确率为 $80\%$、平均加速比为 $1.115$；不启用 CoT 时，转换率为 $83.33\%$、正确率为 $83.33\%$、平均加速比为 $1.079$。 | CoT 在该实验中提高了平均加速比，但降低了转换率和正确率，体现了性能收益与可靠性之间的权衡。由于该比较没有报告重复实验、方差或显著性检验，不能据此断言 CoT 在一般情况下有利于或不利于代码优化。 | 第 4.1 节 Optimizer Performance<br><span class="experiment-evidence">When CoT was employed, the system achieved a transformation success rate of 80% and yielded a substantial average speedup of 1.115×.</span> |

**定性案例**

- doitgen 案例中，原始代码在内层循环中对数组 $C4$ 的访问不连续；循环交换使 $C4$ 的访问更顺序化，同时使数组 $A$ 的访问呈现循环不变量。第一次生成的代码把部分结果过早写回 $A$，CBMC 拒绝该变换；第二次根据反馈重新生成后通过验证，并达到 $4.33\times$ 加速。论文进一步检查 LLVM-IR，发现传统 BiSheng 编译器还对最内层 $p$ 循环进行了因子为 $2$ 的向量化，说明最终收益部分来自 LLM 变换为后端编译器创造了更有利的优化条件，而不是 LLM 明确生成了向量化代码。证据位置：第 4.2 节、图 5 至图 7、表 4。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：核心贡献是利用 LLM 进行代码优化并结合形式化验证的编译框架，属于代码推理与验证。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`1fdeff2bd8198e185d1036fc0cca1c44e2f196952d1243394ee2957d78de30f8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
