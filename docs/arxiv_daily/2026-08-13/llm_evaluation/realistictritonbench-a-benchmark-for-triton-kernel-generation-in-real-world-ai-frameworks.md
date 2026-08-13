---
title: "[论文解读] RealisticTritonBench: A Benchmark for Triton-Kernel Generation in Real-World AI Frameworks"
description: "[arXiv 2608.12004][LLM 评测] 本文提出 RealisticTritonBench，以真实 AI 框架中的 Triton 相关拉取请求为任务来源，并通过单元测试、模型精度测试和端到端性能测试，评估大语言模型在实际内核开发场景中的能力。"
arxiv_id: "2608.12004"
announcement_date: "2026-08-13"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:56:08.636463+00:00"
source_sha256: "db6c0e196d94492ab059ae9df44e340b0a456a6cb202d3d8d61cdedc42b1df6f"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "Triton"
  - "GPU kernel 生成"
  - "大语言模型"
  - "真实拉取请求"
  - "AI 框架"
  - "端到端评测"
  - "代码生成基准"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.12004</p>

# RealisticTritonBench: A Benchmark for Triton-Kernel Generation in Real-World AI Frameworks

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Jinjun Huang, Zhongzhen Wen, Tongtong Xu, Meng Yan, Xin Xia, Zhongxin Liu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: College of Computer Science and Technology and the State Key Laboratory of Blockchain and Data Security, Zhejiang University , Hangzhou , China；College of Computer Science and Technology and the State Key Laboratory of Blockchain and Data Security, Zhejiang University；Affiliation: State Key Lab for Novel Software Technology, Nanjing University , Nanjing , China；State Key Lab for Novel Software Technology, Nanjing University；Affiliation: Software Engineering Application Technology Laboratory, Huawei , Hangzhou , China；Software Engineering Application Technology Laboratory, Huawei；Affiliation: The School of Big Data and Software Engineering, Chongqing University , Chongqing , China；The School of Big Data and Software Engineering, Chongqing University；Affiliation: College of Computer Science and Technology and the State Key Laboratory of Blockchain and Data Security, Zhejiang University；Affiliation: State Key Lab for Novel Software Technology, Nanjing University；Affiliation: Software Engineering Application Technology Laboratory, Huawei；Affiliation: The School of Big Data and Software Engineering, Chongqing University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12004v1) · [PDF 下载](https://arxiv.org/pdf/2608.12004v1) · **关键词** Triton, GPU kernel 生成, 大语言模型, 真实拉取请求, AI 框架, 端到端评测, 代码生成基准<br>


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

本文提出 RealisticTritonBench，以真实 AI 框架中的 Triton 相关拉取请求为任务来源，并通过单元测试、模型精度测试和端到端性能测试，评估大语言模型在实际内核开发场景中的能力。

**不用术语来说**：Triton 能以接近 Python 的方式编写高性能 GPU 程序，但开发者仍需处理内存访问、并行划分和硬件优化等底层问题，因此研究者希望让大语言模型自动完成这类工作。问题在于，已有测试通常只要求模型把一段 PyTorch 程序改写成独立的 Triton 内核，并在专门编写的小型脚本中检查结果；这种成绩不能充分说明生成代码放回真实 AI 框架后是否仍然正确、是否会损害模型精度，以及是否真的缩短整体运行时间。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建 RealisticTritonBench：从流行开源 AI 框架的真实 Triton 相关拉取请求中提取任务，使评测覆盖性能优化、已有内核修改和新内核或算子实现等实际开发活动。
- 建立从内核级到系统级的评测流程：在条件允许时同时执行单元测试、端到端模型精度测试和整体加速测试，从而考察生成内核在原框架中的功能正确性、数值可靠性与实际性能影响。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

现代大模型通常依托 PyTorch、DeepSpeed、Megatron-LM、vLLM 等训练或推理框架运行，其中 GPU kernel（GPU 核函数）负责张量运算、注意力计算和稀疏计算等底层并行操作，直接影响系统延迟、吞吐量与部署成本。Triton 是一种基于 Python 的 GPU 领域特定语言：开发者仍需描述分块并行、内存访问和张量计算，但编译器会处理部分底层优化，因此其开发门槛低于 CUDA，同时可获得接近手写 CUDA 的性能。大语言模型虽然已被用于自动生成 Triton kernel，但真实框架中的开发并不只是把 PyTorch 算子翻译成 Triton，还包括性能优化、缺陷修复、已有实现修改和新 kernel 增加；生成结果也必须在原框架的运行时、内存管理、分布式流程及框架抽象中保持正确和高效。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**GPU kernel（GPU 核函数）**

GPU kernel 是在 GPU 上由大量线程并行执行的函数，通常用于处理张量或矩阵中的数据并行计算。它是深度学习算子的底层构件，其计算组织和内存访问方式会显著影响整体性能。

</div>
<div class="concept-item" markdown="1">

**Triton**

Triton 是面向 GPU kernel 开发的 Python 风格领域特定语言，开发者通过 Triton 原语显式组织程序块、张量计算和内存访问。它隐藏了一部分 CUDA 级细节，但高性能实现仍要求理解并行策略、数据布局、访存模式和硬件特性。

</div>
<div class="concept-item" markdown="1">

**框架级端到端评测**

框架级端到端评测是把生成的 kernel 集成回原始 AI 框架，并运行完整模型或系统流程，以检查最终准确性和执行性能。它不同于只单独测试一个 kernel，因为后者无法充分反映 kernel 与运行时、内存管理及其他算子交互后的实际部署效果。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

RealisticTritonBench 将流行开源 AI 框架中涉及 Triton kernel 修改的真实拉取请求整理为生成任务。每项任务以自然语言工程需求及其所在框架的具体代码环境为输入，要求被评测模型生成或修改相应的 Triton kernel 实现；输出代码随后被集成回原框架，在完整且可复现的环境中接受 kernel 单元测试，并在条件允许时进一步接受模型准确性和端到端速度测试。任务覆盖性能优化、已有实现修改和新 kernel 增加等真实开发活动，而非仅限于从 PyTorch 参考实现到 Triton 的翻译；其基本假设是，只有同时满足局部功能正确性、数值稳健性以及框架级兼容性和性能要求的实现，才具有实际部署意义。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **AutoTriton**: 代表性的基于大语言模型的 GPU kernel 生成方法，用于说明模型自动生成 Triton 实现的可行性；本论文关注的不是提出另一种生成器，而是建立更贴近真实框架开发与部署条件的评测基准。
- **KernelFalcon**: 同属大语言模型辅助 Triton kernel 生成研究，体现了该方向对自动化 kernel 开发的探索；RealisticTritonBench 用来源于真实拉取请求的多类型任务和框架级端到端测试，评估此类模型在生产式工程环境中的能力。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

GPU 内核直接影响现代 AI 框架的延迟、吞吐量和部署成本，而即使采用较高层的 Triton，开发者仍必须正确设计块级并行、内存访问和硬件相关优化。人工完成这些工作专业门槛高且耗时，因此需要判断大语言模型能否在真实工程上下文中生成既正确又高效、并且能够直接集成到现有框架的 Triton 内核。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **以 PyTorch 到 Triton 翻译为主的生成基准**：给模型提供 PyTorch 参考实现，要求其生成具有相同计算语义的 Triton 内核，再比较输出正确性以及相对 PyTorch 实现的内核级速度；原文列举的相关基准研究包括文献 20、28 和 46。
- **面向自动 GPU 内核生成的 LLM 方法**：AutoTriton、QiMeng-Kernel 和 KernelFalcon 等方法利用大语言模型合成 Triton 或其他 GPU 内核，展示了自动化内核开发的可能性；其能力通常借助独立任务和人工编写的测试脚本进行验证。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 任务分布过窄且评测层级不足：已有基准主要考察 PyTorch 到 Triton 的翻译，并在隔离环境中度量内核正确性和速度，较少覆盖真实开发中的性能优化、缺陷修复、功能扩展及已有内核修改。其结果也无法反映生成内核与框架运行时、内存管理、分布式执行流程和框架抽象交互后，对模型精度与端到端延迟产生的实际影响。
- 评测管线可能被利用：人工编写的单内核测试脚本可能存在覆盖不足或检查缺陷，模型有机会绕过正确性检查并获得虚高分数。因此，即使某个生成内核通过脚本或取得局部加速，也不能据此确认它在完整系统中具有真实、稳健的收益。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种以真实 AI 框架变更为任务来源、保留具体工程上下文，并把生成内核重新集成至原框架进行系统级验证的可复现基准。这个缺口使研究者难以可靠比较不同模型在多样化实际任务中的完成能力，也难以区分“通过局部测试”与“在真实系统中保持精度并改善性能”。

</div>
<div markdown="1"><span>核心问题</span>

在来自真实开源 AI 框架拉取请求的 Triton 开发任务上，当前大语言模型能否生成可集成的实现，使其通过功能测试、保持端到端模型精度，并在完整框架运行中获得实际加速？

</div>
<div markdown="1"><span>作者直觉</span>

真实拉取请求天然包含工程需求、已有代码和框架约束，因此比合成翻译题更接近开发者实际面对的任务；把候选内核放回原框架运行，则让错误的数据类型、边界处理、数值行为或集成逻辑最终体现为测试失败、精度下降或整体延迟增加。端到端指标直接观察最终系统效果，模型若只钻独立测试脚本的空子而没有真正实现正确计算，通常难以同时维持模型精度和系统性能，因此这种入口能更可信地衡量实际部署能力。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

RealisticTritonBench不是一种训练新模型的算法，而是一套从真实软件变更中构造任务并进行系统级评测的基准方法。其数据源是PyTorch、vLLM和SGLang等开源AI框架中已经合并、且涉及Triton内核修改的拉取请求（PR）。构造流程先用文本关键词和代码差异筛出候选PR，再由人工确认内核目标、测试可用性和任务独立性；随后将每个合格PR转化为包含任务描述、仓库上下文和目标函数定义的代码生成实例，并为实例建立可复现的Docker环境。最终基准包含31个任务，覆盖性能优化、既有内核修改和新内核实现三类真实开发需求。

评测时，语言模型只接收上述任务输入，并生成符合指定接口的Triton实现；生成代码随后替换容器中原框架的目标实现。评测流水线依次考察内核级单元测试、模型级精度以及端到端延迟，使“代码是否算对”“替换后模型行为是否保持”和“整个系统是否真正受益”成为彼此独立的判断维度。通俗地说，该方法不是让模型完成脱离项目的编程题，而是把模型生成的内核放回原项目、原版本和相应运行流程中，检查它能否像真实工程补丁一样工作。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 收集并初筛真实Triton PR

首先依据“triton”“kernel”“operation”“optimization”等关键词进行粗粒度文本过滤，再检查代码差异，仅保留实际新增或修改Triton内核的PR，例如包含“@triton.jit”内核定义的变更。

<div class="method-step__io" markdown="1">

**输入**：PyTorch、vLLM和SGLang等流行且持续维护的开源AI框架的历史PR，包括标题、描述、提交消息和代码差异。<br>
**输出**：约2,000个需要进一步人工分析的Triton相关候选PR。

</div>

**直观理解**：文本关键词负责快速缩小搜索范围，代码差异检查则确认PR确实动过Triton实现。两层筛选相当于先查标题目录，再打开文件核验正文。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提取并审核内核生成任务

人工按照Triton内核相关性、测试可用性和目标清晰度三项标准筛选PR，并识别目标函数及预期功能或性能变化；随后由LLM起草任务描述，再由两名有Triton经验的开发者依据意图忠实性、需求完整性和无金标准补丁泄漏三项标准审核。

<div class="method-step__io" markdown="1">

**输入**：候选PR的描述、代码差异、目标函数、相关函数与类，以及仓库中已有的测试。<br>
**输出**：具有明确需求的任务描述、实现所需上下文、目标函数定义，以及单元测试、模型精度测试和延迟测试的候选命令。

</div>

**直观理解**：这一步把一份可能包含大量讨论和文件改动的PR，压缩成模型可以执行的工程任务。人工审核既要保证题目没有遗漏关键约束，也要避免把原补丁的具体实现直接透露给模型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建两级可复现执行环境

为同一仓库的实例建立共享基础Docker镜像，再在其上构建包含精确代码版本和依赖的实例级环境；对于依赖版本含糊、接口不兼容等构建失败，记录完整日志并将人工修复整理成可执行的实例级脚本。

<div class="method-step__io" markdown="1">

**输入**：任务所属仓库、对应代码版本、系统与Python依赖、CUDA配置、仓库构建命令和测试需求。<br>
**输出**：每个任务独立、可自动重建并能够运行目标测试的容器化环境。

</div>

**直观理解**：共享镜像避免每道题都从零安装相同工具，实例镜像则固定每个历史PR需要的特殊版本。这样可以减少“代码相同但环境不同”造成的评测偏差。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 依据执行反馈验证和精炼实例

先运行全部单元测试并剔除无法通过者，但排除纯硬件原因导致的失败；再运行模型精度与延迟测试，根据重建环境中的真实执行结果修正因仓库演化而失效的脚本接口或参数。

<div class="method-step__io" markdown="1">

**输入**：候选任务、其原始或参考实现、已构建的容器，以及三类测试命令。<br>
**输出**：31个经执行验证的最终任务，其中优化、修改和新内核任务分别占41.93%、22.58%和35.48%。

</div>

**直观理解**：只有能够在固定环境中稳定复现并被测试的任务才进入基准。这里修正的是评测命令与环境适配问题，而不是降低任务对生成内核正确性或性能的要求。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。RealisticTritonBench是基准构造与推理期代码生成评测方法，原文未提出用于训练或微调LLM的损失函数，也没有通过基准反馈更新模型参数。它的目标是测量现有LLM完成真实Triton内核工程任务的能力；单元正确性、模型精度和端到端延迟属于评测信号，而不是可微训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 真实PR驱动的任务定义**

每个实例对应一个已合并的真实Triton相关PR，模型输入由任务描述、文件—函数或文件—类形式的上下文引用以及目标函数定义组成。任务描述先由LLM根据PR内容生成，再由两名开发者以0/1/2分审核意图忠实性、需求完整性和实现泄漏；任一标准的平均分低于1.5时，审核者共同修改至达成一致。

> 直观理解：该模块保留真实项目中的接口、依赖和工程约束，同时把PR整理成边界清楚的生成问题。评分和复核用于防止题目歪曲原PR目标、缺少成功条件，或因透露金标准补丁而让任务变得不真实。

**2. 实例级容器化复现模块**

环境采用“仓库共享基础镜像加实例专用层”的两级结构：基础镜像统一Python、CUDA Toolkit等系统配置，实例层固定目标代码版本、依赖和必要补丁。无法直接构建时，维护者依据完整日志解决依赖或配置兼容问题，并把修复写入自动执行的构建脚本。

> 直观理解：真实历史代码常依赖旧版库或特定配置，若只提供代码而不固定环境，测试可能根本无法运行。实例容器把这些历史条件封装起来，使不同模型面对同一可重复的执行条件。

**3. 分层系统评测套件**

评测套件包括Unit Test、Model Accuracy Test和Latency Test。Unit Test复用仓库已有的pytest类命令检查内核功能；Model Accuracy Test通过仓库既有评测脚本检查替换算子后模型性能是否出现明显下降；Latency Test测量替换后的端到端系统延迟，而非只记录单个内核的微基准时间。

> 直观理解：三个层级分别控制局部计算错误、模型级语义退化和系统级性能收益。它还能降低仅针对单个手写测试脚本取巧的空间，因为生成实现最终必须在完整框架工作流中接受检验。

**训练与推理**

训练过程不适用，论文所述流程不训练新的内核生成模型。推理时，每个任务将自然语言任务描述、与实现相关的文件—函数或文件—类上下文，以及必须遵守的目标函数接口合并成提示交给LLM；模型据此输出目标Triton内核实现。原文节选未明确说明多轮交互、采样参数、候选数量、工具调用或执行反馈是否会返回模型，因此不能据此假定模型能够在测试失败后自动修改代码。

生成完成后，评测端把模型代码替换到对应历史版本的原框架中，先执行单元测试确认目标内核满足预期行为，再在框架与模型工作流中执行精度测试和端到端延迟测试。该顺序体现了部署门槛：局部功能错误的实现不能仅凭速度获得认可，而局部正确的实现还必须维持模型级行为，并在真实系统路径上体现性能影响。

**复现信息**

复现基准需要保留每个任务对应的仓库与精确代码版本、共享基础Docker镜像、实例级依赖和修复脚本、任务提示、目标函数定义以及三类测试命令。数据构造的关键筛选条件是：PR确实涉及Triton内核、至少具有可用于正确性验证的测试，并且改动目标能够表述为独立的功能或性能任务；最终无效实例通过实际执行被剔除。任务类别及占比为优化41.93%、修改22.58%、新内核35.48%，总计31个实例。

公平解释结果时还需注意，模型获得的是经审核的需求和必要上下文，而不是原PR的金标准实现；生成代码必须严格匹配目标函数定义，并在同一实例容器内替换原实现后接受测试。模型精度与延迟命令可能因仓库接口长期演化而经过适配，但适配依据是重建环境中的执行反馈。节选未给出GPU具体型号、超时限制、延迟预热与重复次数、精度容差、模型解码配置或失败计分规则，这些内容原文未明确报告，不能从本章自行补全。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- RealisticTritonBench：由流行开源 AI 框架中修改 Triton 内核的真实拉取请求转化而成。每项任务向代理提供自然语言需求和原始仓库环境，要求其检索上下文、修改代码并在框架内接受端到端测试。给定节选未明确报告任务总数、训练/验证/测试划分；这不是用于模型训练的传统数据集，而是面向真实软件工程场景的评测任务集。
- 任务类别划分：Optimization 要求在已有 Triton 实现上提升性能；Modification 要求修复缺陷或扩展功能；New-kernel 要求在没有现成 Triton 实现可参考时从头生成内核。节选明确说明 New-kernel 含 11 项任务，但未明确报告另外两类的任务数。该划分用于检验“有无现成内核参考”以及“修改目标是性能还是功能”对模型表现的影响。
- 模型级通用基准：通过将生成内核集成回原框架，再在一个 common benchmark 上检查模型性能是否下降，以判定数值鲁棒性。给定节选未提供该基准的名称、规模或数据划分，因此不能据此判断其任务覆盖面。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务成功率（Success%）**

严格的综合指标：生成实现的单元测试通过情况必须与 gold patch 一致，模型级数值鲁棒性必须为真，并且端到端速度比同时满足 $S_{\mathrm{TTFT}}\geq 0.98$ 和 $S_{\mathrm{TPOT}}\geq 0.98$。它衡量补丁是否具备整体部署可用性，而非只检查代码能否运行。 （越高越好，因为更高表示更多任务同时满足功能、数值稳定性和系统性能要求；$0.98$ 的阈值允许少量运行波动。）

</div>
<div class="metric-item" markdown="1">

**测试正确性（FTP% 与 UTP%）**

FTP% 是通过全部单元测试的任务比例；UTP% 是每项任务所通过测试占该任务全部单元测试的比例。FTP 更严格，UTP 则能反映未完全成功的补丁完成了多少测试行为。 （均为越高越好，但高 FTP 或 UTP 只说明测试层面的功能较正确，不能保证模型精度不下降，也不能保证端到端推理不变慢。）

</div>
<div class="metric-item" markdown="1">

**部署质量（NR、$S_{\mathrm{TTFT}}$ 与 $S_{\mathrm{TPOT}}$）**

NR 检查替换内核后模型在通用基准上的性能是否不下降；$S_{\mathrm{TTFT}}=\mathrm{TTFT}_{\mathrm{base}}/\mathrm{TTFT}_{\mathrm{new}}$ 衡量首个 token 延迟变化，$S_{\mathrm{TPOT}}=\mathrm{TPOT}_{\mathrm{base}}/\mathrm{TPOT}_{\mathrm{new}}$ 衡量后续每个输出 token 的延迟变化。论文仅在通过全部单元测试的任务上汇总 NR 和速度比。 （NR 为真且其比例越高越好；两个速度比越高越好，超过 $1$ 表示比 gold patch 更快，等于 $1$ 表示大致持平，低于 $1$ 表示变慢。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 五种模型在完整 RealisticTritonBench 上的综合表现

<div class="result-value" markdown="1">

Qwen3.5-397B-A17B 的成功率最高，为 $25.81\%$；五种模型平均成功率仅为 $18.71\%$。尽管平均 FTP 为 $43.23\%$、UTP 为 $60.33\%$，它们明显高于综合成功率，说明通过测试与满足真实部署要求之间存在较大差距。

</div>

作者据此主张，即使先进模型也很难同时保证代码功能、模型精度和系统延迟。更直白地说，模型经常能写出“测试看起来正确”的补丁，却可能令完整模型数值退化或推理变慢。该结果支持基准具有区分度，但不证明所有单元测试天然不足，也不能排除代理脚手架、上下文长度和模型配置对成功率的影响。

<div class="result-source" markdown="1">

来源：第 4.2 节 RQ1；汇总数值见表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Specifically, Qwen3.5-397B-A17B achieves the best performance, with a task success rate of 25.81%, indicating that only a small portion of tasks can be fully solved under realistic constraints.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 通过全部单元测试后的数值稳定性与端到端速度

<div class="result-value" markdown="1">

在纳入 NR 与速度统计的全测试通过任务上，平均 NR 仅为 $47.65\%$；平均 $S_{\mathrm{TTFT}}$ 为 $1.0579$，平均 $S_{\mathrm{TPOT}}$ 为 $0.9612$。后者低于 $1$，表示生成内核在输出 token 阶段平均略慢于 gold patch。GPT-5.4 的 $S_{\mathrm{TTFT}}=1.375$ 看似突出，但作者指出其正确案例数量有限，代表性不足。

</div>

这一结果把“功能正确”与“系统可用”分开：全过单测的代码仍可能改变浮点计算行为，或因内存访问、调度和框架交互而没有实际加速。平均速度比不能说明每个任务都变慢或变快；尤其当不同模型进入速度统计的正确案例数量不同时，直接比较均值可能受到样本选择影响。

<div class="result-source" markdown="1">

来源：第 4.2 节 RQ1；完整模型级指标见表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Regarding numerical robustness, only 47.65% of the cases maintain model accuracy without degradation after replacing the original code.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 按 Optimization、Modification 与 New-kernel 分类评测

<div class="result-value" markdown="1">

Optimization、Modification、New-kernel 的平均成功率分别为 $23.08\%$、$31.43\%$ 和 $5.455\%$；New-kernel 的平均 FTP 仅为 $20.00\%$，UTP 为 $40.62\%$，平均 $S_{\mathrm{TTFT}}=0.9025$、$S_{\mathrm{TPOT}}=0.9310$。Modification 虽有最高平均成功率，但平均 NR 只有 $20.00\%$；Optimization 的平均速度比也仅为 $1.152$ 和 $0.9654$，未显示两个推理阶段都稳定加速。

</div>

分类结果表明，已有 Triton 实现可作为结构和语义参考时，模型较容易完成测试层面的修改；从头实现新内核则最困难。Modification 的低 NR 提醒读者：功能扩展或修复可能通过测试，却引入测试未覆盖的数值边界问题。不过，各类别任务数量和难度并不相同，因此这些差异是描述性证据，不能单独证明“缺少参考实现”是性能下降的唯一原因。

<div class="result-source" markdown="1">

来源：表 4，New-kernel 的 Average 行；其他类别对照亦见表 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

New-kernel Average 5.455% 93.94% 20.00% 40.62% 40.00% 0.9025 0.9310

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 给定实验节选未报告基准总任务数、Optimization 与 Modification 的任务数、仓库构成、模型级 common benchmark 名称以及各模型进入 NR/延迟统计的有效样本量。由于 NR 和速度只在全测试通过任务上取平均，尤其是 GPT-5.4 的高 $S_{\mathrm{TTFT}}$ 已被作者指出来自有限正确案例，跨模型均值可能存在选择偏差。
- 实验固定使用 mini-SWE-agent、Bash-only 工具接口、高推理强度和 $8\times$ RTX 3090 环境，因此结果反映“模型加该脚手架与硬件配置”的联合表现，不能直接外推到其他代理、上下文策略或 GPU。三类任务也不是随机控制实验，类别间任务数量与内在难度可能不同；论文在所给节选中没有提供真正的组件消融，故不能从分类结果中建立因果结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Gold patch reference implementation：以真实拉取请求中经内核专家审查并被项目接受的实现作为延迟基线，计算生成补丁相对它的 $S_{\mathrm{TTFT}}$ 与 $S_{\mathrm{TPOT}}$。该比较回答生成代码是否达到当时真实框架所接受的工程方案，而不是仅仅优于修改前代码。
- DeepSeek-V3.2（non-reasoning）：685B 开源非推理模型，用于观察不显式启用推理时的代码代理表现，并与同系列 reasoning 配置形成有限的推理模式对照。
- DeepSeek-V3.2（reasoning）与 Qwen3.5-397B-A17B：两种开源推理模型；前者可与同系列非推理配置比较，后者用于检验不同架构和训练范式下的强开源模型能力。
- GPT-5.4 与 Gemini-3.1 Pro Preview：闭源推理模型，用于比较先进闭源模型和开源模型在相同代理脚手架、仓库环境与评价标准下的表现；该实验并不控制模型规模、训练数据或发布时间，因而不是严格的单变量比较。

**实验想回答的问题**

- RQ1：五种先进大语言模型在 RealisticTritonBench 的真实仓库任务上，能否生成同时满足功能正确、模型级数值稳定和端到端性能要求的 Triton 内核？
- RQ2–RQ3：模型能力在 Optimization、Modification 与 New-kernel 三类任务间如何变化，失败主要来自 Triton 底层编程能力不足，还是对真实仓库中内核语义理解不充分？

**实验实现**

所有模型均通过 mini-SWE-agent 操作仓库；该脚手架采用仅含 Bash 的工具接口，使模型能够自行检索依赖和代码上下文。对具备推理能力的模型，在可配置时将 reasoning effort 设为 high，否则启用 thinking。生成补丁先接受应用检查和单元测试，再被集成回原 AI 框架，执行模型级数值稳定性检查及 TTFT、TPOT 端到端测量。实验运行于配备 $8\times$ NVIDIA RTX 3090 GPU 的服务器，每项测量取三次运行的平均值；论文报告 $S_{\mathrm{TTFT}}$ 与 $S_{\mathrm{TPOT}}$ 的平均波动分别为 $1.08\%$ 和 $0.98\%$。Cost 以 token 消耗报告，但节选未说明其中 M 的精确定义以及是否包含输入、输出和推理 token。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 图 4 展示了一个 API 语义错误：生成代码对两个标量 $q\_end\_pos$ 和 $cur\_batch\_query\_len$ 调用 `tl.min`。在 Triton 中，`tl.min` 是需要输入张量及归约轴的归约操作，并非二元标量最小值；此处应使用逐元素运算 `tl.minimum`。该案例说明模型可能写出表面上类似常见 Python 数值代码、实际却违反 Triton API 约束的实现，支持作者关于“底层编程模型理解不可靠”的定性判断。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces a benchmark for evaluating LLM code-generation capabilities on realistic Triton kernel engineering tasks.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`db6c0e196d94492ab059ae9df44e340b0a456a6cb202d3d8d61cdedc42b1df6f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
