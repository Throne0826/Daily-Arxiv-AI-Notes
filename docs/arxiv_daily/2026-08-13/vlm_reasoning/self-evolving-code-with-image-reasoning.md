---
title: "[论文解读] Self-Evolving Code-with-Image Reasoning"
description: "[arXiv 2608.11292][VLM Reasoning] 本文研究如何让多模态模型把无法靠目视或语言推理完成的像素级计算写成可执行程序，并通过反思、诊断和修复自身失败程序，在不更新模型权重的情况下积累可复用的视觉算法技能。"
arxiv_id: "2608.11292"
announcement_date: "2026-08-13"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:56:46.200496+00:00"
source_sha256: "17f3e6e27a464db8f1e0d04c0e28474310ae05a60f634cb458279c1cdedd0c75"
tags:
  - "VLM Reasoning"
  - "LLM Agent"
  - "LLM Reasoning"
  - "多模态视觉推理"
  - "Code-with-Image"
  - "程序原生推理"
  - "视觉算法"
  - "CwI-Bench"
  - "可执行推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.11292</p>

# Self-Evolving Code-with-Image Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Tianze Yang, Liang Wu, Ruitong Sun, Yucheng Shi, Yanqiao Wang, Mayank Darbari, Ninghao Liu, Jin Sun, Liangjie Hong</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Georgia；The Hong Kong Polytechnic University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11292v1) · [PDF 下载](https://arxiv.org/pdf/2608.11292v1) · **关键词** 多模态视觉推理, Code-with-Image, 程序原生推理, 视觉算法, CwI-Bench, 可执行推理<br>


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

本文研究如何让多模态模型把无法靠目视或语言推理完成的像素级计算写成可执行程序，并通过反思、诊断和修复自身失败程序，在不更新模型权重的情况下积累可复用的视觉算法技能。

**不用术语来说**：有些图像问题不是“看不清”，而是必须真正对整幅图像执行多步计算，例如判断颜色通道如何混合、拼接区域偏移了多少像素，或两次曝光是否被融合。模型往往能用语言说出大致算法，却不能仅靠文字推理准确执行数组运算；裁剪、放大等常用工具也只会让图像更容易观察，不能代替完整计算。本文因此要求模型直接编写并运行 Python 程序，让程序从像素中算出答案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出 Code-with-Image 问题范式及 CwI-Bench：模型只获得通用 Python 解释器，需要自行实现视觉算法；基准包含 30 个由隐含视觉计算生成的任务族，并采用互不重叠的学习、验证和测试划分，以测量模型是否真正学会可迁移的计算过程。
- 作者提出 Self-Reflection over Executable Reasoning：冻结模型参数，通过观察失败轨迹和在沙箱中重新执行、诊断、可视化中间结果及验证修复，把有效改进保存为纯文本技能；作者还声称这些技能可以跨模型规模和模型家族迁移。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究多模态大模型的视觉推理。现有“图像辅助思考”通常让模型通过裁剪、缩放、旋转或增强等工具获得更清晰的视觉证据，再由语言推理器生成答案；这种范式适合解决目标太小、画面不清或外部知识缺失等感知问题，但不适合必须对完整像素数组连续执行多步计算的任务。本文提出的 Code-with-Image 将程序作为推理载体：模型只获得通用 Python 解释器，需要自行确定并实现视觉算法，使每一步的数组输出直接成为下一步的输入，最终由程序计算答案，而不是把工具结果交还给语言链进行判断。CwI-Bench 据此构造了 $30$ 个由隐含视觉计算定义的任务族，涵盖位移、排列、定位、颜色混合与信号测量等类型，用于检验模型能否从“描述算法”转向“正确执行算法”。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**图像辅助思考（thinking-with-images）**

模型在推理过程中调用裁剪、缩放、旋转、亮度调整或搜索等工具，以暴露更容易观察的证据。工具一般只改善输入或补充信息，最终判断仍由语言推理完成。

</div>
<div class="concept-item" markdown="1">

**程序原生视觉推理（program-native visual reasoning）**

模型不是从预设工具集中选择操作，而是自行编写完整程序，对图像像素或数组实施任务所需的算法。程序执行过程承担推理，程序输出直接对应问题答案。

</div>
<div class="concept-item" markdown="1">

**建设性真值（constructive ground truth）**

样本标签由已知的数据生成过程或隐含计算规则直接算出，而不是依赖人工目测标注。这样可以持续生成带精确答案的实例，并用真值检查程序修复是否真正有效。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一幅图像及其视觉问题，目标通常要求恢复由像素完全决定、但无法凭观察达到指定精度的结果，例如检测颜色通道混合、估计拼接区域的像素级错位或测量图像信号。求解器不获得预设视觉 API 或参考工具链，只能使用通用 Python 解释器，自行选择算法、编写代码、载入图像并对数组执行多步变换，程序的最终输出即为答案。评测采用 CwI-Bench 的 $30$ 个任务族，并设置互不重叠的学习、验证和测试划分；这种设计旨在区分两种能力：模型是否仅能用语言说出大致方法，以及它是否能把方法实现为可正确执行、可迁移到同族新实例的算法。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$I$**

作为程序输入的图像，其像素可在 Python 中表示为数组。

</div>
<div class="notation-item" markdown="1">

**$q$**

与图像配套的视觉问题或任务指令。

</div>
<div class="notation-item" markdown="1">

**$P$**

模型根据图像与问题编写的 Python 程序，即承载视觉算法的推理过程。

</div>
<div class="notation-item" markdown="1">

**$\hat{y}=P(I,q)$**

执行程序后得到的预测答案；这是根据论文任务流程整理的概念记号，并非原文正式定义的公式。

</div>

</div>

**直接相关的工作**

- **V*、DeepEyes 与 Pixel Reasoner**: 这些方法以搜索、裁剪和缩放改善高分辨率或小目标感知，工具负责返回视觉证据，答案仍由语言推理器产生；本文关注的任务则要求程序自行实现对像素数组的完整算法，因而不是单纯增强可见性。
- **VisProg、ViperGPT、PyVision、Thyme、CodeV 与 CodeDance**: 这些工作也允许模型生成代码，但生成程序主要调用预训练视觉 API 或裁剪、旋转、对比度增强等既有操作。Code-with-Image 不提供固定工具词表，模型必须编写任务特定算法，且程序输出直接作为答案。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

图像取证等任务要求从像素恢复精确且可验证的答案，例如识别图像是否被篡改、确定颜色通道的重混合方式，或测量拼接区域的像素偏移。这些答案虽然完全由输入图像决定，却通常不能通过观察、放大或检索直接得到，而必须让多个数组运算按顺序处理整幅图像；任何数据类型溢出、索引偏差或中间步骤错误都可能使最终答案失败。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **Thinking-with-Images（借助图像工具的语言推理）**：模型在语言推理过程中反复调用裁剪、缩放、旋转、亮度或对比度调整等工具，必要时结合网络搜索；工具负责暴露更清楚的证据或补充外部信息，随后模型继续用语言组织推理并生成答案。
- **代码调用型多模态智能体**：已有智能体能够生成并执行代码或调用图像操作，但通常把程序视为辅助工具之一，研究重点仍是工具返回何种证据，而不是要求模型针对每个问题自行构造一条完整的、由程序承载的视觉计算过程。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有图像工具主要弥补单步感知或知识缺口，不能完成中间状态为完整数组、后一步必须消费前一步全部输出的多步计算。原文指出，这类工具型方法中，当前先进智能体用工具解决的问题有 93%–96% 也能在不用工具时解决，而且工具在专门为其设计的测试集上仅增加 2%–5% 的准确率；作者据此认为，其主要作用仍是改善证据获取，而非提供新的算法执行能力。
- 语言链可以描述正确算法，却不能可靠地执行像素数组上的算法；即使提供 Python 解释器，模型仍可能出现无符号算术回绕、边界索引差一位等不易从文字说明中发现的实现错误。因此，“能够运行代码”只消除了执行环境限制，真正的瓶颈转为选择、实现和调试正确算法。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一个把程序本身作为视觉推理主体的明确研究设定：模型既不能依赖预先规定的工具词表，也没有参考工具链可以模仿，而要针对检查无法确定的精确目标自行编写视觉算法。同时，还缺少一种无需人工编写程序规则或更新模型权重、能够利用构造式真值检验失败程序并沉淀通用修复经验的机制，以及能用独立数据划分衡量这种算法能力是否真正改善的基准。

</div>
<div markdown="1"><span>核心问题</span>

在仅提供通用 Python 解释器的条件下，冻结的多模态模型能否从自身失败的视觉程序中定位原因、提出并执行修复、用构造式真值筛选有效改动，并把这些改动保存为能够推广到同类新样本乃至其他模型的纯文本技能？

</div>
<div markdown="1"><span>作者直觉</span>

程序能够保存并逐步变换完整像素数组，因此适合承载语言难以直接执行的视觉算法；程序运行还会留下变量、数组和渲染后的中间结果，使隐藏错误可以被复现和检查。作者的切入点是把错误答案转化为可调试的程序故障：先从已有轨迹中归纳有限的技能修改，阅读不足时再进入沙箱执行诊断和修复，最后只保留能提升留出数据准确率的技能。直观上，这相当于让模型通过可执行测试学习“下次应如何写代码”，而不是仅凭文字反省自己为何答错。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把视觉问题的推理载体从自然语言转为可执行 Python 程序：模型接收题目与图像，在仅提供解释器的环境中选择并实现多步视觉算法，再依据程序输出作答。这里的关键不是调用裁剪、放大等工具帮助“看清”，而是让程序直接操作像素、计算中间状态并执行完整算法，因此程序本身构成可检查、可重运行的推理过程。
在此基础上，作者设计了一个无需参数训练的技能自演化循环。系统收集求解失败的轨迹，以已有技能库 $L_{r-1}$ 为条件，先通过观察式反思阅读提示、代码、输出和渲染图像；若仅阅读无法定位实现错误，则在预载失败案例的沙箱 $E^{\prime}$ 中执行诊断代码、检查中间变量并用标准答案验证修复。候选技能编辑由训练集内的探针集 $D_{\mathrm{probe}}$ 引导搜索，最终仅在独立验证集 $D_{\mathrm{val}}$ 上相对空技能库 $\varnothing$ 达到规定增益时交付；测试集不参与搜索或交付决策。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 程序化视觉求解

模型判断问题隐含的视觉计算，生成并运行实现该算法的代码，再根据像素运算结果产生答案。程序可承载多步计算及中间状态，而不仅是为语言推理提供一次局部观察。

<div class="method-step__io" markdown="1">

**输入**：视觉问题、对应图像、当前技能库 $L_{r-1}$，以及可执行 Python 代码的解释器。<br>
**输出**：预测答案，以及包含提示、程序、运行输出和渲染图像的可执行求解轨迹。

</div>

**直观理解**：模型不只用语言说出“应该采用什么算法”，而要像编程解题一样真正把算法运行完。这样，算法选择或实现中的错误会具体落在可检查的代码和变量上。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 失败批次构造与观察式反思

模型执行一次只读的观察式反思 $R_{\mathrm{obs}}$，从失败轨迹中识别策略层问题，并生成数量受限的技能编辑操作，例如更换目标、加入验证条款或删除误导性条目。

<div class="method-step__io" markdown="1">

**输入**：第 $r$ 轮失败批次 $B_r$、上一轮技能库 $L_{r-1}$ 和反思配置 $\alpha_r$；$B_r$ 包含提示、原程序、运行输出及全部渲染图像。<br>
**输出**：候选技能库编辑，或“仅观察不足以确定原因”的信号。

</div>

**直观理解**：这一阶段相当于代码审查：先看现有记录是否已经暴露了方向性错误。能从日志直接判断的问题，无需立即进入更昂贵的交互调试。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 可执行反思与修复验证

在第 $t$ 步，模型依据累计会话 $\mathcal{E}_{t-1}$ 生成调查代码 $q_t$，由沙箱执行并返回 $o_t$；模型可重跑旧程序、打印数值与数据类型、渲染中间结果，或对照标准答案测试修复。会话在原因得到验证并产出技能编辑时结束，最迟在步数预算 $T_{\max}$ 后通过最终调用强制输出编辑；编辑还需在多个相互独立的失败案例上确认。

<div class="method-step__io" markdown="1">

**输入**：观察式反思未解决的失败批次 $B_r$、技能库 $L_{r-1}$，以及预载每个案例图像、标准答案、错误答案和原程序的沙箱 $E^{\prime}$。<br>
**输出**：经执行证据支持的故障原因与可迁移技能编辑。

</div>

**直观理解**：有些错误不会出现在最终日志里，例如数组类型错误或坐标差一位，因此必须亲自重跑并插入诊断。它类似调试器中的逐步实验：每次执行结果都会成为下一次调查的依据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 探针搜索、验证门控与技能交付

每轮以探针准确率 $\hat{J}_{\mathrm{probe}}$ 引导非贪心搜索，并通过早停、重启及受保护的当前最优库 $L^{\dagger}$ 管理候选；交付时才读取验证分数 $\hat{J}_{\mathrm{val}}$。当前最优库或次优库必须比裸 Code-with-Image 至少高出 $\gamma$，否则不交付任何技能；多次重启中保留验证分数最高者。

<div class="method-step__io" markdown="1">

**输入**：候选技能库、训练集内固定且难度均衡的探针集 $D_{\mathrm{probe}}$、独立验证集 $D_{\mathrm{val}}$、空技能库 $\varnothing$ 和交付阈值 $\gamma$。<br>
**输出**：通过门控的任务技能库，或回退到使用空技能库的裸 Code-with-Image。

</div>

**直观理解**：探针集负责在开发过程中指路，验证集只在最后验收，测试集始终不参与选择。门控可以阻止明显无效的技能被交付，但作者明确说明它不能保证测试集上绝不退化。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 可执行反思的交互状态更新

$$
\mathcal{E}_{0}=B_{r},\qquad q_{t}\sim M(\cdot\mid L_{r-1},\,\mathcal{E}_{t-1}),\qquad o_{t}=E^{\prime}(q_{t}),\qquad \mathcal{E}_{t}=\mathcal{E}_{t-1}\cup\{(q_{t},o_{t})\}.
$$

**符号说明**

- $\mathcal{E}_{t}$：截至第 $t$ 步的调查会话记录，包含初始失败批次及此前所有调查代码与执行输出。
- $B_r$：第 $r$ 轮失败批次，沙箱中还预载各案例的图像、标准答案、错误答案和原始求解代码。
- $q_t$：模型在第 $t$ 步生成的调查代码，例如打印中间变量、重跑程序或测试候选修复。
- $M$：执行反思的模型；它根据现有技能库与累计会话生成下一步调查。
- $L_{r-1}$：进入第 $r$ 轮反思前已有的技能库。
- $o_t$：沙箱执行调查代码 $q_t$ 后返回的输出。
- $E^{\prime}$：预载失败案例及相关信息、可运行调查代码的反思沙箱。
- $t$：可执行反思会话中的交互步编号。

<div class="equation-explanation" markdown="1">

**直观理解**：会话起点就是失败材料；此后模型每次根据全部既往实验决定下一段诊断代码，沙箱执行后再把代码与结果追加到记录中。这个闭环使模型能够通过实际干预逐步验证错误原因，而不是一次性猜测修复方案。<br>
**原文位置**：第 4.2 节“Executable reflection”，公式 (5)

</div>

</div>

<div class="equation-block" markdown="1">

#### 技能库交付门控条件

$$
\text{deliver }L^{\dagger}\;\iff\;\hat{J}_{\mathrm{val}}(L^{\dagger})\;\geq\;\hat{J}_{\mathrm{val}}(\varnothing)+\gamma.
$$

**符号说明**

- $L^{\dagger}$：探针搜索过程中受保护的当前最佳技能库，即交付阶段首先检查的候选。
- $\hat{J}_{\mathrm{val}}(L)$：使用技能库 $L$ 时在独立验证集 $D_{\mathrm{val}}$ 上测得的准确率。
- $\varnothing$：空技能库，对应不加载演化技能的裸 Code-with-Image。
- $\gamma$：要求候选技能库相对空技能库达到的最小验证增益阈值。
- $D_{\mathrm{val}}$：仅在最终交付阶段读取的独立验证集。

<div class="equation-explanation" markdown="1">

**直观理解**：只有候选库在验证集上的准确率至少比不使用技能高出 $\gamma$，系统才会交付它；否则继续检查次优候选，二者都失败便回退到裸方法。该规则是验证侧的质量保护措施，但不是测试性能不下降的数学保证。<br>
**原文位置**：第 4.3 节“Validation and delivery”，公式 (6)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该方法不进行梯度训练，也没有更新模型参数的损失函数；其优化对象是文本技能库。搜索阶段以训练集内部探针集上的准确率 $\hat{J}_{\mathrm{probe}}$ 作为候选选择信号，通过失败反思、受限编辑、非贪心搜索、早停和重启寻找更好的 $L^{\dagger}$；验证集分数 $\hat{J}_{\mathrm{val}}$ 不参与逐轮搜索，只执行最终门控。因而这里的“自演化”应理解为基于可执行反馈优化外部技能记忆，而非模型权重的自训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Code-with-Image 可执行推理算子**

该算子让模型在只有 Python 解释器的条件下，将视觉任务转写成真正作用于图像像素的算法程序，并依据执行结果回答；可执行反思 $R_{\mathrm{exec}}=\mathcal{A}^{M}_{E^{\prime}}$ 复用同一算子，只是把输入改为模型过去的失败案例。

> 直观理解：同一套能力既用来解题，也用来调试自己的旧解法。因为推理状态保存在程序和中间数据中，反思能够直接干预失败计算，而不只是评论一段文字解释。

**2. 双模式反思器**

观察式反思 $R_{\mathrm{obs}}$ 以一次只读模型调用处理策略层错误；可执行反思则维护会话状态 $\mathcal{E}_t$，循环生成诊断代码并接收沙箱结果，用于定位无法由轨迹表面观察到的实现错误。

> 直观理解：先读记录，再按需动手实验，可以分别覆盖“方法选错”和“代码写错”两类故障。后者尤其适合检查未打印的数组、数据类型和边界约定。

**3. 技能库选择与验证门控器**

搜索阶段只使用训练集子集 $D_{\mathrm{probe}}$ 的准确率，并保存当前最优技能库 $L^{\dagger}$；交付阶段用独立的 $D_{\mathrm{val}}$ 将候选与空库 $\varnothing$ 对比，同时隔离测试集。系统允许非贪心探索、早停和重启，并在最优与次优候选均未通过门槛时回退到裸方法。

> 直观理解：该模块把“发现技能”和“批准技能”分开，减少技能只记住开发案例的风险。技能是普通文本形式的可交付产物，不涉及更新模型权重。

**训练与推理**

技能演化阶段，系统用当前技能库运行 Code-with-Image，收集失败批次 $B_r$，先进行一次观察式反思；若轨迹阅读不足以确认原因，则启动可执行反思，在最多 $T_{\max}$ 步内反复生成并运行调查代码。经多个独立失败案例确认的修复被写成候选技能编辑，再由固定的 $D_{\mathrm{probe}}$ 评估并更新当前候选；搜索采用非贪心策略、早停与多次重启，且始终保护目前最佳库 $L^{\dagger}$。最终在 $D_{\mathrm{val}}$ 上按公式 (6) 检查最优库和次优库，多次重启之间保留验证分数最高的通过者；若均未通过，则交付空库。
正式推理时，模型接收新问题、图像与已交付技能库，在 Python 解释器中实现并执行视觉算法，再从运行结果生成答案。学习划分与评测划分相互隔离，且测试集既不提供探针搜索分数，也不参与交付门控；根据给定原文，技能库以普通文本形式使用，但具体提示模板、代码接口和答案解析规则未明确报告。

**复现信息**

公平解释该方法所需的关键设置包括：观察式反思默认只有一次只读调用；可执行反思沙箱 $E^{\prime}$ 预载失败案例的图像、标准答案、错误答案及原求解代码，并受最大步数 $T_{\max}$ 限制；技能编辑须在多个独立失败案例上确认。探针集 $D_{\mathrm{probe}}\subset D_{\mathrm{tr}}$ 固定且按难度平衡，验证集 $D_{\mathrm{val}}$ 仅在交付时读取，测试集完全不用于技能选择；若最优库和次优库均未达到阈值 $\gamma$，任务保持裸 Code-with-Image。给定节选未明确报告 $T_{\max}$、$\gamma$、失败批次大小、重启次数、早停条件、允许的 Python 包、沙箱资源限制及技能编辑数量上限的具体数值，因此这些复现参数不能从当前材料中确定。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- CwI-Bench：论文构造的核心评测集，包含 30 个由隐藏视觉计算定义的任务族，分为变换与重排、感知与计数、定位、颜色四组，并设置四个难度层级。每个任务使用 60 个训练样本供反思、50 个独立验证样本供技能选择、100 个完全留出的测试样本供最终报告；标签由生成程序先采样目标再渲染图像，因此属于构造式真值。
- COCO train2017：作为 CwI-Bench 训练侧实例的源照片集合，用于生成反思阶段可见的任务图像；它不是直接按 COCO 原标签评测。生成器从源图像出发施加隐藏变换或信号构造，并记录精确目标。
- COCO val2017：仅用于生成 CwI-Bench 测试侧实例；论文通过自动审计保证其源照片与训练侧零交集。该划分用于降低模型通过相同底图记忆程序或答案的可能性，但不能排除模型预训练期间见过 COCO 图像。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**测试准确率**

对每个样本进行二值判定后取平均：离散答案要求精确匹配，连续答案要求落入任务预先定义的容差。它直接衡量最终程序输出是否恢复构造式真值；复合答案即使只错一个分量也可能记为失败。 （越高越好，因为更高值表示在统一评分器和留出样本上正确恢复目标的比例更大。）

</div>
<div class="metric-item" markdown="1">

**相对 bare Code-with-Image 的验证集提升量（pp）**

技能条件准确率减去无技能代码条件准确率，以百分点表示。消融实验同时报告三个随机种子的平均提升，以及按任务选择验证表现最佳种子后的提升。 （越高越好；正值表示反思流程相对仅执行代码产生额外收益，接近零则表示该组件没有稳定改善。）

</div>
<div class="metric-item" markdown="1">

**技能交付率**

在任务与随机种子组合中，候选技能通过验证门槛并被交付给测试求解器的比例。它衡量反思流程形成可部署技能的覆盖面，不等同于最终准确率。 （在验证门槛固定时通常越高越好，但必须结合准确率提升判断，因为交付更多低质量技能并不必然改善测试结果。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 冻结模型：无工具语言推理与 bare Code-with-Image 的比较

<div class="result-value" markdown="1">

Qwen3.5-27B 从 Instruct 的 8.6% 提升到 bare Code-with-Image 的 32.6%，GPT-5.6-luna 从 12.9% 提升到 43.0%；所有冻结模型的 Instruct 准确率位于 7% 至 13%，Thinking 最高仍不超过 25%。

</div>

作者据此主张，主要瓶颈不是模型能否说出算法，而是能否把像素级中间量交给程序持续计算。由于模型、样本和评分器保持一致，这一比较较直接地支持代码执行介质的作用；但它不是严格的单组件因果消融，也不能说明 Python 是唯一有效的执行环境。

<div class="result-source" markdown="1">

来源：第 5.2 节，Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In Instruct mode, tool-free CoT stays between 7% and 13% for all six frozen models, and thinking mode lifts it to at most 25%: these targets sit beyond what language-side reasoning recovers, however strong. Under Code-with-Image, where the environment supplies a general-purpose interpreter and nothing else (no visual API, no reference toolchain), the same frozen models rise at every scale (8.6% → 32.6% on 27B, 12.9% → 43.0% on luna); 99.9% of 27B Code-with-Image trajectories execute code (3.5 executions per instance), so code carries the solution rather than assisting a language reasoner.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 四种执行器加载各自的自演化技能

<div class="result-value" markdown="1">

相对 bare Code-with-Image，Qwen3.5-9B 从 11.1% 提升到 30.6%，gemma-4-26B-A4B 从 27.7% 提升到 46.5%，Qwen3.5-27B 从 32.6% 提升到 55.9%，GPT-5.6-luna 从 43.0% 提升到 66.6%。

</div>

作者将一致的跨模型提升解释为：执行器可把自身失败转化为之后能够调用的程序性知识，而且这一机制不只适用于最强模型。分析上，这说明经验证筛选的技能库具有实际价值；但实验把技能生成、候选筛选和提示注入作为整体评估，不能仅凭该结果判断其中哪一步贡献最大。

<div class="result-source" markdown="1">

来源：第 5.3 节，Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Self-evolved skills raise bare Code-with-Image for all four executors: 11.1% → 30.6% on 9B, 27.7% → 46.5% on gemma-26B, 32.6% → 55.9% on 27B, and 43.0% → 66.6% on luna (Figure 3).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 纯文本技能跨规模与跨模型家族迁移

<div class="result-value" markdown="1">

Qwen3.5-27B 编写的技能将 Qwen3.5-9B 从 11.1% 提升到 34.5%，超过 9B 自演化的 30.6% 和 bare 27B 的 32.6%；同一技能库将 gemma-4-26B-A4B 从 27.7% 提升到 45.0%，距离 gemma 自演化结果 46.5% 仅差 1.5 个百分点。相反，luna 编写的技能迁移到 27B、9B 和 gemma 后分别达到 40.3%、17.9% 和 40.8%，均低于对应模型自身演化的结果。

</div>

结果表明技能中确实包含可跨执行器复用的算法信息，而且较强开放模型产生的技能甚至能让小模型超过大模型的无技能水平。前沿模型技能反而迁移较差，支持作者提出的“技能与作者执行能力共同适配”解释；不过该解释主要来自结果模式，实验没有直接测量静默运行错误或代码复杂度，因此尚非完备的机制证明。

<div class="result-source" markdown="1">

来源：第 5.4 节，Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across scale, the 27B model’s per-task delivered skills raise the 9B solver from 11.1% to 34.5%: above the 9B’s own self-evolved skills on every family (30.6% overall) and past the bare 27B itself (32.6%), with the gain concentrated on Transformation (transferred 38.4% vs. self-written 30.1%), where procedures are most algorithmic. Across families, the same library injected into gemma-4-26B-A4B over its native tool-calling transport lifts bare Code-with-Image from 27.7% to 45.0%, within 1.5 pp of gemma’s own evolution (46.5%) and ahead of it on Transformation: nothing the skills encode is specific to their author’s family. Transfer down from the frontier helps, but helps least: luna-written skills lift every recipient over bare Code-with-Image (40.3% on 27B, 17.9% on 9B, 40.8% on gemma) yet land below both the recipient’s own evolution and the 27B-written library.

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

- Instruct：关闭模型原生思考模式的无工具链式推理。它衡量模型仅凭直接语言生成能恢复多少答案，是判断任务是否确实超出目测和浅层推理的下界。
- Thinking：启用模型原生思考模式、但仍不提供代码执行环境。它控制了额外语言推理预算，用来区分“思考得不够久”与“语言无法可靠执行像素级算法”。
- Bare Code-with-Image：只提供通用 Python 解释器，不提供任务专用视觉 API、固定工具集或参考实现。它与无工具基线的差异主要对应程序承载中间数组、掩码和拟合参数的能力。
- Code-with-Image + self-evolved skills：在相同代码执行循环中加入模型通过训练免除的反思流程产生并经验证集筛选的文本技能；未交付技能的任务回退到 bare Code-with-Image。它检验对既往程序失败的总结与修复能否形成可复用过程。

**实验想回答的问题**

- 在同一批完全留出的测试样本上，仅依靠语言推理、使用无任务专用工具的 Python 解释器，以及进一步加载自演化技能，这三种求解方式的准确率如何变化？该比较旨在检验视觉算法由代码实际执行是否比模型仅在语言中描述算法更有效。
- 可执行反思产生的技能能否跨模型规模和模型家族迁移，以及反思过程中重新执行、检查和修复程序，相比只阅读失败轨迹的观察式反思是否带来独立增益？

**实验实现**

第一部分冻结全部模型，在每个任务相同的 test-100 样本、相同评分器下比较 Instruct、Thinking 和 bare Code-with-Image。被测模型包括 Qwen3.5-9B、Qwen3.5-27B、Qwen3.5-35B-A3B、gemma-4-12B、gemma-4-26B-A4B、GPT-5.6-luna，以及三种按各自原生协议运行的 thinking-with-images 智能体。第二部分仅对 Qwen3.5-9B、Qwen3.5-27B、gemma-4-26B-A4B 和 GPT-5.6-luna运行自改进流程，所有任务共享同一配方且不做逐任务调参：每任务训练集大小为 60，探测集大小为 32、每个难度层取 8 个，验证集大小为 50；耐心值为 5，最多进行 10 个可执行反思步骤。技能库最多 6 条、每条最多 250 词，求解最多 5 步并受 40,960 token 预算约束。所有报告值由归档的原始交互轨迹重新计算。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Qwen3.5-27B：完整可执行反思与移除执行干预的观察式反思比较 | 完整流程的平均验证集提升为 19.7 个百分点，移除可执行反思后为 13.8 个百分点，差值为 6.0 个百分点；按部署规则选择每任务最佳种子时，完整流程为 27.5 个百分点、移除后为 20.3 个百分点，差值为 7.1 个百分点。技能交付率也由 58.9% 增至 70.0%。 | 该消融保持其余循环不变，只把停滞后的程序重执行与修复替换成更多观察式反思，因此较集中地隔离了执行干预的贡献。完整流程取得更高提升和交付率，表明仅阅读失败轨迹不能发现所有隐藏在数组、中间状态或边界约定中的错误；不过感知组出现负差值，说明执行升级并非所有任务都需要。 | 第 5.5 节，Table 4<br><span class="experiment-evidence">Removing intervention costs 6.0 pp of the 19.7 pp mean uplift (7.1 pp at the per-task best seed used for deployment); the interventional share of the total reflection gain stays within a quarter to a third across executors (6.0/19.7 = 30% on 27B vs. 3.0/12.2 = 24% on 9B).</span> |
| 按任务组分析可执行反思对 Qwen3.5-27B 的影响 | 完整流程相对移除执行干预，在变换与重排组的平均提升增加 12.9 个百分点，在定位组增加 3.8 个百分点，在颜色组增加 3.5 个百分点；感知与计数组反而减少 3.3 个百分点。变换组的技能交付由移除执行干预时的 20/36 次提高到完整流程的 27/36 次。 | 这一分组消融说明可执行反思的总体收益主要来自需要精确调试实现的任务，而不是各类任务上的均匀小幅改善。感知组的反向结果提示固定升级策略存在机会成本：当问题主要是阈值或信号处理策略微调时，额外执行轮次可能挤占更有用的观察式反思轮次。 | 第 5.5 节，Table 4<br><span class="experiment-evidence">The loss concentrates on Transformation (12.9 pp; delivery 27/36 → 20/36), where faults hide in intermediate state; Localization loses 3.8 pp, while on Perception observational reflection alone is slightly better (−3.3 pp): escalation there displaces observational rounds it did not need.</span> |

**定性案例**

- 在 Qwen3.5-27B 的测试中，循环移位任务达到 100%，对齐任务达到 97%，作者称这两个确定性任务上的已交付过程“基本完整”。这一案例说明技能可以固化为接近可靠算法的明确步骤，而不仅是宽泛提示；但原文节选未提供对应程序、失败样本或置信区间，因此不能据此推断全部任务都能演化出完整求解器。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper studies visual algorithmic reasoning through code execution and a self-improving reflection loop that turns executable tool use into multimodal reasoning.; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`17f3e6e27a464db8f1e0d04c0e28474310ae05a60f634cb458279c1cdedd0c75`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
