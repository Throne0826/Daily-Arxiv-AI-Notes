---
title: "[论文解读] LLM-Assisted Dynamic Threat Analysis for Attacker-Reachable Software Weaknesses in Autonomous Vehicles"
description: "[arXiv 2608.13450][LLM Agent] 本文研究大语言模型能否把静态分析发现的、可受攻击者输入影响的 Autoware 候选弱点自动转化为可编译、可执行且确实触达目标代码的动态测试工件，并据此定位当前自动化流程的主要瓶颈。"
arxiv_id: "2608.13450"
announcement_date: "2026-08-14"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:59:56.477496+00:00"
source_sha256: "904249b309a7d74df4f0b7f1a95bff07c1f53e448e587227d6b8ac809b99407b"
tags:
  - "LLM Agent"
  - "LLM 其他"
  - "LLM Reasoning"
  - "自动驾驶软件安全"
  - "Autoware"
  - "静态分析"
  - "攻击者可达弱点"
  - "大语言模型"
  - "模糊测试"
  - "测试驱动程序生成"
  - "编译器在环修复"
  - "ROS 2"
  - "目标代码可达性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.13450</p>

# LLM-Assisted Dynamic Threat Analysis for Attacker-Reachable Software Weaknesses in Autonomous Vehicles

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Md Wasiul Haque, Sagar Dasgupta, Mizanur Rahman, Md Rayhanur Rahman</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Department of Civil, Construction & Environmental Engineering, The University of Alabama；Department of Computer Science, The University of Alabama</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13450v1) · [PDF 下载](https://arxiv.org/pdf/2608.13450v1) · **关键词** 自动驾驶软件安全, Autoware, 静态分析, 攻击者可达弱点, 大语言模型, 模糊测试, 测试驱动程序生成, 编译器在环修复, ROS 2, 目标代码可达性<br>


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

本文研究大语言模型能否把静态分析发现的、可受攻击者输入影响的 Autoware 候选弱点自动转化为可编译、可执行且确实触达目标代码的动态测试工件，并据此定位当前自动化流程的主要瓶颈。

**不用术语来说**：静态分析可以在自动驾驶软件中圈出许多值得检查的代码位置，但这些位置只是“可能有问题”，不能证明攻击输入在真实运行时一定能够到达那里并造成安全影响。要进一步验证，测试者必须编写能在原生工程中构建和运行的测试程序，正确处理类型、初始化、消息格式、中间件和跨软件包依赖；对于 Autoware 这类大型系统，这项工作成本很高，也难以靠人工扩展到大量候选位置。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将研究焦点从“模型能否生成测试代码”推进到完整的动态确认链路，考察生成工件能否接入 Autoware 原生构建、通过带有消毒器的编译与链接、接受编译器反馈修复、进入模糊测试并实际执行预定目标代码。
- 作者建立构建集成失败分类，并区分“名义上编译成功”与“忠实执行真实目标”：后者要求工件没有通过存根、替代实现或绕过方式避开待验证的 Autoware 代码，从而揭示动态确认在进入模糊测试之前为何失效。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于自动驾驶软件安全保障、程序分析与大模型辅助测试的交叉领域。Autoware 等自动驾驶软件栈由感知、定位、预测、规划和控制等模块组成，并通过 ROS 2 的发布—订阅中间件交换序列化消息；来自传感器、网络或消息接口的外部数据可能跨越多个软件包，最终影响转向、加速或制动等安全关键输出。软件级保障通常先用静态分析在整个代码仓库中寻找“外部输入可达且可能影响安全决策”的候选位置，再用覆盖率引导模糊测试和 Sanitizer 在运行时验证这些路径是否真实可达、是否会触发内存错误或其他安全相关行为。本文关注两阶段之间的关键缺口：动态验证必须有一个能够在真实构建环境中编译、链接、初始化目标并把攻击者控制数据送入目标实现的测试驱动程序，而 Autoware 的生成式 ROS 2 类型、节点生命周期、跨包依赖和构建配置使该程序难以人工批量构造。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**静态分析（static analysis）**

在不实际运行程序的情况下检查源代码、控制流和数据流，用于定位外部输入可能到达安全相关判断、校验逻辑或输出路径的位置。它给出的是候选弱点，因为静态路径在运行时可能不可达、条件不可满足，或者即使执行也没有安全影响。

</div>
<div class="concept-item" markdown="1">

**模糊测试与测试驱动程序（fuzzing and fuzz harness）**

模糊测试持续生成或变异输入，并依据覆盖率等反馈探索新的程序路径；测试驱动程序负责把这些字节转换成目标 API 或 ROS 2 消息所需的对象、状态和调用序列。只有驱动程序成功编译、链接并执行真实目标代码，发现的崩溃或异常才可能用于确认原候选弱点。

</div>
<div class="concept-item" markdown="1">

**ROS 2 发布—订阅中间件**

ROS 2 中的节点通过主题发送和接收类型化消息，底层通常使用基于 DDS 的通信机制；反序列化和订阅回调是外部字节进入 C++ 对象和业务逻辑的自然入口。测试这些入口往往还需满足消息类型生成、节点初始化、参数、主题映射和软件包依赖等工程条件。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是生产规模的开源自动驾驶栈 Autoware，分析环境保留各翻译单元的真实编译参数、头文件路径、预处理定义、生成接口和原生包依赖。输入首先是完整代码仓库及其构建信息，静态阶段从中识别外部输入能够传播到安全相关决策、验证检查或输出路径的候选位置，并为每个候选提取代码与数据流上下文；论文在 185 个软件包中识别出 1,375 条决策规则、2,274 个验证检查和 482 条输入到安全输出的数据流，并据此分层抽样 740 个可达候选。动态阶段的输入是候选代码、可选的静态上下文以及面向本地开放权重大模型的生成任务；模型输出应是可执行测试制品，包括驱动程序及其必要构建配置，使模糊输入能够进入候选所对应的真实 Autoware 实现。系统随后在原生构建环境和 Sanitizer 下编译、链接这些制品，对失败项执行编译器反馈驱动的修复，并仅对可执行项进行固定预算的模糊测试和事后归因。任务输出不是“模型生成了可编译代码”这一单一标签，而是候选弱点是否被动态确认，以及从生成、依赖接线、编译、链接、初始化、真实目标可达性到异常归因的分阶段证据。其核心假设是外部输入可由攻击者影响，但静态可达性不等于运行时可利用性；替换、绕过或桩化目标实现的制品即使名义上编译成功，也不能作为原候选被确认的证据。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$C$**

静态分析得到的候选弱点集合；每个候选对应一个外部输入可能到达安全相关代码的位置或路径。

</div>
<div class="notation-item" markdown="1">

**$c \in C$**

一个待动态验证的具体候选位置，并附带目标代码、类型信息和静态数据流上下文。

</div>
<div class="notation-item" markdown="1">

**$H_c$**

大模型或基线针对候选 $c$ 生成的测试驱动程序及相关可执行制品。

</div>
<div class="notation-item" markdown="1">

**$R(H_c)$**

制品 $H_c$ 是否实际执行候选对应的真实 Autoware 目标实现；若只执行替代实现或桩代码，则不满足真实目标可达性。

</div>

</div>

**直接相关的工作**

- **基于 LLVM/Clang 或 CodeQL 的仓库级静态控制流与数据流分析**: 这类方法能够在真实编译配置下定位不可信输入到安全相关判断或输出的传播路径，是本文候选发现阶段的技术基础；但其结果可能包含不可行、不可达或运行时无害的路径，因此不能单独完成动态确认。
- **大模型生成模糊测试驱动程序及编译器在环迭代修复**: 已有研究主要面向孤立程序、库或 API，通过生成驱动程序并把编译诊断反馈给模型来修复代码。本文把该思路扩展到完整 Autoware 软件栈，并额外检查原生构建集成和真实目标执行，从而防止将删除依赖、替换实现或引入桩代码造成的表面编译成功误判为有效验证。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

自动驾驶软件接收传感器和网络等外部数据，并据此产生转向、加速和制动命令；如果攻击者可影响的数据经过多个组件后触发软件缺陷，后果可能直接涉及车辆和道路参与者的安全。因此，安全保障不能停留在列出可疑代码，还需要证明相关执行路径在现实构建与运行条件下是否可达、是否可触发，以及是否会产生安全或安全性相关影响。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **仓库级静态分析**：静态分析在不实际运行程序的情况下检查整个代码库，追踪外部输入如何流向安全相关决策、校验逻辑和重要输出，并标记校验薄弱、数据传播可疑或可能影响控制结果的位置。它适合大范围筛选候选点，但输出本质上是待验证线索。
- **基于模糊测试与消毒器的动态确认**：动态方法先构造测试工件或模糊测试驱动器，用它建立目标所需状态、注入异常输入并调用待测代码，再借助模糊测试探索输入空间，利用消毒器捕获越界访问等运行时异常。已有研究还尝试使用大语言模型生成此类驱动器、测试程序或结构化输入，以减少人工编写成本。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 静态证据不能单独证明运行时可达性、路径可行性或安全影响，因此静态告警既不能直接视为已确认漏洞，也不能因为后续没有触发就推断攻击面是良性的。
- 成熟的模糊测试器和消毒器仍依赖一个能够忠实接入真实目标的可执行工件；在 Autoware 中，目标类型、初始化顺序、ROS 2 接口、生命周期假设、软件包边界、跨包依赖和构建配置共同造成集成障碍。大语言模型即使生成了表面合理的代码，也可能无法编译、链接或触达目标，修复过程还可能用存根替换真实实现，使“编译成功”失去验证意义。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有工作表明大语言模型能够以不同成功率生成模糊测试驱动器和测试输入，但尚不清楚这种能力能否扩展到完整的生产规模自动驾驶软件栈，也缺少对“静态候选点到动态确认”全链路的系统评估。尤其需要识别失败究竟发生在候选选择、代码生成、原生构建集成、目标代码触达还是模糊执行阶段，并验证修复后的工件是否仍然测试原目标，而非仅通过替换或绕过实现获得形式上的可编译性。

</div>
<div markdown="1"><span>核心问题</span>

在固定分析预算下，大语言模型能否为 Autoware 中受外部输入影响的安全相关候选位置自动构造忠实的动态测试工件，并完成从原生编译、链接和目标执行到弱点确认的全过程；若不能，模型选择、静态上下文以及各类构建失败如何限制这一过程？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把静态分析与大语言模型的互补能力串联起来：前者负责从庞大代码库中提供目标位置、相关代码和输入到安全输出的结构化证据，缩小模型需要理解和生成的范围；后者尝试把这些局部证据转化为原本需要专家手工编写的测试工件。再让真实编译器反馈错误并驱动修复，理论上可以逐步补齐类型和依赖问题；同时逐阶段记录编译、链接、触达和执行结果，可以判断自动化真正卡在哪里，而不会把无法进入目标代码误解为候选弱点已被否定。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把“静态分析发现的可疑代码位置”转化为可编译、可执行并可判定结果的动态测试。输入是固定版本的 Autoware 源码、原生构建元数据、ROS 2 接口与启动配置；流程先在编译器精确的条件位置中筛选高优先级目标，再让不同 LLM 或基线为每个目标生成模糊测试驱动等四类工件，随后在真实 Autoware 头文件和 API 环境中编译，通过最多 3 轮编译器反馈修复，最后链接为 libFuzzer 可执行文件并在固定预算下运行。输出不是简单的“崩溃或未崩溃”，而是构建失败、未执行、预算内证伪、误报或确认弱点等带有可达性语义的分类，以及跨模型和实验条件汇总的构建集成结果。
直观地说，静态分析负责指出“哪些门可能没锁好”，LLM 负责制作能够实际走到这些门前并尝试开门的测试工具；编译器检查工具能否接入真实系统，模糊测试再反复改变攻击输入。该设计的关键约束是：只有测试输入真正到达预定 Autoware 实现，而且出现可复现的安全或安全性影响，才可确认弱点；工具本身无法构建、没有到达目标或仅在桩代码中崩溃，都不能当作目标代码存在漏洞的证据。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段 0：仓库级静态提取与目标筛选

Clang 按每个翻译单元的真实编译配置恢复 $\texttt{if}$／$\texttt{switch}$ 条件和简化调用图，launch 与 YAML 文件补充节点组合、重映射和运行参数，CodeQL 用于交叉核查；分类器标注安全相关决策、验证检查及启发式输入到安全输出路径。随后按 0 至 11 分的规则为 2,749 个条件位置排序：执行器相关词、验证或边界检查、外部 ROS 输入暴露、位于输入到安全输出路径上以及属于安全关键域分别贡献相应分值，并保留全部 P1 和 P2 位置。

<div class="method-step__io" markdown="1">

**输入**：Autoware 源码、各翻译单元的导出编译配置、ROS 2 接口、launch 与 YAML 配置、包依赖和部署范围信息。<br>
**输出**：740 个确定性选择的动态测试目标，其中 P1 为 214 个、P2 为 526 个，覆盖 34 个包和 107 个源文件；每个目标附有源码窗口、候选描述、输入主题、安全相关输出及构建上下文。

</div>

**直观理解**：这一步先绘制软件中的“攻击路线图”，再把更接近外部输入和车辆关键输出的位置排到前面。740 个目标不是人工挑选的少量案例，而是评分达到 P1 或 P2 的完整集合，因此减少了研究者主观选例造成的偏差。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段 1：条件受控的测试工件生成

使用固定提示模板和相同解码参数，让两个本地开放权重 LLM 分别生成四类工件；另设无静态上下文条件和根据元数据确定性生成脚手架的朴素模板基线。每个目标生成函数级 libFuzzer 驱动、ROS 2 消息变异器、软件在环故障注入规范及 ASan/UBSan 构建配置。

<div class="method-step__io" markdown="1">

**输入**：每个目标的元数据，以及正常条件下的相关源码窗口、候选说明、已恢复输入主题和安全相关输出；无静态上下文消融仅接收目标元数据。<br>
**输出**：面向 740 个目标、可进入真实构建验证的成套测试工件，同时保留全部提示和原始模型响应以支持复现与条件间比较。

</div>

**直观理解**：模型不仅要写一个随机输入函数，还要说明怎样改变 ROS 2 消息、怎样模拟延迟或陈旧数据，以及怎样启用内存和未定义行为检测。固定除模型或静态上下文外的其他条件，是为了把差异尽量归因于模型能力或上下文信息，而不是提示和预算不同。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段 2：真实构建集成与编译器闭环修复

使用 $\texttt{clang++}$、AddressSanitizer 和 UndefinedBehaviorSanitizer，在真实 Autoware 头文件与 API 上尝试对象文件编译，并按固定错误分类记录失败；失败工件最多进入 3 轮修复，模型每轮接收当前源代码和 Clang 诊断。无静态上下文条件在修复时仍只能看到生成工件和编译反馈，不会重新获得被扣留的静态分析上下文。

<div class="method-step__io" markdown="1">

**输入**：生成的模糊测试驱动与构建配置、固定 Autoware 版本，以及目标翻译单元在 $\texttt{compile\_commands.json}$ 中记录的包含路径、预处理定义和编译选项。<br>
**输出**：首轮和修复后的对象编译结果、结构化编译错误记录，以及能够继续链接的候选驱动；首轮产物被保留，以区分模型直接生成能力与依赖编译器反馈后的修复能力。

</div>

**直观理解**：真实大型工程中，代码片段“看起来正确”并不代表能接上原有依赖、类型和构建规则，所以这里让原生编译器充当严格验收者。最多 3 轮修复模拟开发者根据报错改代码，但对象编译成功只说明接口层面接入成功，尚不等于能链接、运行或真正触达目标。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段 3 至 4：链接、模糊执行、归因与聚合

将驱动链接为 libFuzzer 可执行文件并运行，只有驱动调用预定 Autoware 实现且模糊输入实际传播到目标时才算有效；对崩溃去重并人工检查可达性、可复现性及安全或车辆安全影响。随后把每个目标划分为构建失败、未执行、预算内证伪、误报或确认弱点，并按模型、上下文条件和失败类型汇总。

<div class="method-step__io" markdown="1">

**输入**：成功对象编译的驱动、libFuzzer 运行环境、固定执行预算，以及目标位置和预期数据流信息。<br>
**输出**：具有明确证据边界的目标级判定和实验条件级统计：真实目标被触达且出现可复现弱点才是“确认”，目标外崩溃为“误报”，完整运行预算而无相关失败为“预算内证伪”，未到达目标或未进入模糊阶段则为“未执行”。

</div>

**直观理解**：这一步把“测试工具坏了”和“被测程序安全”严格分开：编译失败或跑不到目标，只能说明测试没有完成，不能替候选位置洗清风险。即使出现崩溃，也要确认崩溃来自真实 Autoware 目标，而不是驱动、替身实现或其他外围代码。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文没有训练或微调任何模型，也没有报告需要优化的损失函数；两个本地开放权重 LLM 作为既有生成模型使用。方法层面的“优化”表现为固定规则的目标优先级排序和最多 3 轮基于 Clang 诊断的生成式修复，但这不会更新模型参数，因此不能称为训练目标；原文也未给出中心数学目标函数，不应根据文字评分规则另造方程。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 编译器精确的静态攻击面分析器**

该模块以真实导出编译配置处理翻译单元，恢复条件位置、简化调用关系、ROS 2 订阅与发布接口、参数面和包级输入到安全输出路径。它把候选组织为决策策略保护、验证弱点、输入依赖和状态分派四类，但启发式路径分析并非完全跨过程、污点精确的可达性证明。

> 直观理解：它的作用是给模型提供具体目标和周边语境，而不是直接宣布某处存在漏洞。尤其是所谓“输入到输出路径”只用于排序，表示值得优先检查，不能代替动态执行中的真实数据流证据。

**2. 多工件 LLM 生成器与受控比较接口**

生成器把统一模板与目标上下文组合，要求每个目标同时产出 libFuzzer 驱动、ROS 2 消息变异器、故障注入规范和 sanitizer 构建配置；实验保持目标、模板、解码参数、构建环境及执行预算不变。无静态上下文消融检验源码和静态数据流信息是否必要，确定性模板基线则提供不依赖模型推理的朴素下界。

> 直观理解：单独生成一段测试代码不足以覆盖 ROS 2 系统的消息和时间行为，因此作者把“如何调用函数”“如何改消息”“如何制造系统故障”和“如何检测运行错误”作为一套工件。受控接口确保模型间比较面对的是同一批目标和同一套工程约束。

**3. 编译器闭环与证据约束的动态判定器**

该模块从对象编译、反馈修复、链接和 libFuzzer 执行逐级推进，并用 sanitizer 捕获内存错误和未定义行为。判定逻辑同时要求预定实现被调用、输入受 fuzzer 控制并到达目标、异常可复现且具有相关影响，从而隔离依赖接线失败、无效驱动和目标外崩溃。

> 直观理解：它相当于多道验收门：先看工具能否装进系统，再看能否启动，然后看是否真的测到指定代码，最后才判断异常是否属于目标弱点。这样的分层避免把“生成代码能编译”误写成“漏洞已证实”，也避免把没跑起来误写成“候选已证伪”。

**训练与推理**

整个方法只有推理与外部工具反馈，没有模型训练。生成阶段对每个目标填充同一提示模板：常规模型条件获得目标元数据、源码窗口、候选描述、输入主题和安全输出，无静态上下文消融仅获得元数据；模型一次生成四类测试工件，确定性模板基线则直接依据元数据生成脚手架。所有条件采用相同解码参数，但所给节选未列出参数具体数值。
推理后的工件必须经过真实工程验证：首先按目标翻译单元的编译命令进行带 ASan/UBSan 的对象编译；失败时，模型接收生成源代码和 Clang 错误，最多修复 3 轮，且消融条件始终不补回静态上下文。对象编译成功的驱动再尝试链接并进入固定预算的 libFuzzer 执行。最终判定不是模型自评，而是结合构建日志、目标覆盖、受控输入传播、崩溃去重和人工归因形成；这使“代码生成能力”“工程集成能力”和“动态弱点证据”成为三个不同层级。

**复现信息**

复现所需的核心约束包括：固定 Autoware 代码版本；使用 $\texttt{compile\_commands.json}$ 中目标翻译单元的包含路径、宏定义和编译选项；以 $\texttt{clang++}$ 编译，并启用 AddressSanitizer 与 UndefinedBehaviorSanitizer；使用真实 Autoware 头文件和 API，而不是仅在隔离片段上做语法检查；保存提示、原始响应、首轮产物、每轮诊断和修复结果。论文把“可编译”明确限定为针对真实 API 的对象文件编译成功，它比成功链接和执行更弱，因此解读结果时不能把对象编译率当作可运行率。
公平比较还依赖以下控制：740 个 P1/P2 目标对各条件一致，提示模板、可见上下文字段、解码设置、构建环境和执行预算保持固定，只有模型身份变化；消融实验额外移除静态分析上下文，并在修复阶段继续维持该隔离。动态有效性要求驱动调用预定实现且 fuzzer 输入到达目标；崩溃必须去重并人工检查来源、复现性和影响。所给节选未明确报告固定代码版本标识、模型名称、硬件配置、解码参数数值、单个目标的模糊测试时长及具体链接命令，这些信息需要结合论文其余章节或发布工件核验。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 被测系统是固定修订版的开源自动驾驶软件栈 Autoware，工作区于 2026 年 2 月 10 日克隆。前置静态分析覆盖 185 个包，恢复 2,749 个编译器精确的条件位置，并按安全相关性打分；动态实验不随机划分训练集或测试集，而是穷举所有优先级为 P1 和 P2 的位置，共 740 个目标、34 个包和 107 个源文件。
- 740 目标构成动态评测的目标全集，其中 P1 有 214 个、P2 有 526 个；按领域包括规划 361 个、控制 138 个、感知 124 个、定位 115 个和地图 2 个。该分布用于检验方法在不同自动驾驶子系统中的构建集成与动态触达能力，不是用于训练模型。
- 五种实验条件对同一批 740 个目标各生成一套工件，总计 3,700 套。每套包含函数级 libFuzzer harness、ROS 2 消息变异器、软件在环故障注入规范以及 ASan/UBSan 构建配置；这些工件共同构成被编译、修复、链接和模糊测试的实验样本。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**首次对象编译成功率**

生成的 harness 在任何修复之前，能否使用目标翻译单元的真实头文件、API、包含路径、预处理定义和编译选项通过对象编译；它衡量首轮生成与真实工程接口的兼容性，但不代表已经成功链接、执行或触达目标。 （越高越好，因为更高比例意味着模型较少依赖编译器反馈即可生成满足真实构建约束的代码。）

</div>
<div class="metric-item" markdown="1">

**修复后对象可编译率与进入模糊测试的比例**

前者衡量最多 3 轮编译器在环修复后能否通过对象编译，后者衡量 harness 是否进一步完成链接并实际启动 libFuzzer。两者的差距反映“能编译”与“可执行且可测试”之间的集成障碍。 （两者均越高越好；尤其应关注进入模糊测试的比例，因为对象编译成功只是较弱的中间条件。）

</div>
<div class="metric-item" markdown="1">

**动态确认结果**

只有 harness 调用预期的 Autoware 实现、由 fuzzer 控制的输入到达目标，并观察到可复现且具有安全或安全性影响的弱点时，候选才算确认；源于目标之外的崩溃属于假阳性，未到达执行阶段的目标属于未测试，而不是被否证。 （在严格排除桩代码和目标外崩溃后，真实确认数量越高越好；但零确认只能表示在给定 harness 有效性与时间预算内未确认，不能直接证明候选不存在弱点。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 两个 LLM 在真实 Autoware 环境中的首次对象编译

<div class="result-value" markdown="1">

通用推理模型首次编译成功率为 64%，代码专用模型仅为 6%。作者据此表明，模型类别对真实工程接口兼容性有显著影响，代码专用定位本身并不保证更强的构建集成能力。

</div>

直观地说，推理模型生成的 harness 更常能直接通过编译器这一关，而代码专用模型多数需要修复。不过该结果只衡量对象编译，不说明 64% 的 harness 已成功链接、能把模糊输入送到目标代码，或发现了真实弱点；原文节选也未提供不确定性检验，因此不能仅凭该差值推断对其他软件栈普遍成立。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The reasoning model compiled 64% of harnesses on the first attempt, compared with 6% for the code-specialized model.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 首次编译失败的原因分类

<div class="result-value" markdown="1">

80% 的首次编译失败来自依赖接线问题，而不是被测程序逻辑。作者将其作为主要失败分类结果，认为全栈动态分析的核心障碍是让生成代码正确接入真实项目的头文件、类型、构建目标和依赖关系。

</div>

这说明“模型能写出看似合理的测试逻辑”与“工件能嵌入大型 ROS 2/Autoware 工程”是两件不同的事。该比例定位了第一轮编译失败的主要来源，但不证明修好依赖后一定能够链接、触达目标或暴露缺陷，也不能说明剩余 20% 全部来自程序逻辑。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The main result is a build-integration failure taxonomy showing that 80% of first-shot compilation failures arise from dependency wiring rather than program logic.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 修复、模糊执行与最终弱点确认

<div class="result-value" markdown="1">

推理模型依靠大量桩代码才达到全部对象可编译，但其 harness 中不足一半进入 fuzzer；观察到的 37 次崩溃全部源自桩代码而非 Autoware，最终在预算内没有动态确认任何候选弱点。

</div>

该结果揭示了中间指标可能产生的假象：对象编译率可以通过补桩提升，但桩代码既可能阻断真实调用路径，也可能自行崩溃。因此，37 次崩溃不能算作 Autoware 缺陷证据；零确认也不等于 740 个候选均为假阳性，因为许多 harness 没有到达 fuzzer 或真实目标，且成功链接后的实际执行仅为每目标 60 秒。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Repair achieved full object-compileability for the reasoning model only through extensive stubbing; fewer than half of its harnesses reached the fuzzer, and all 37 observed crashes originated in stubbed code rather than Autoware. No candidate weakness was dynamically confirmed within budget.

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

- 代码专用模型 `codestral:22b`：用于检验面向代码生成优化的模型是否更擅长生成与 Autoware 真实接口兼容的 harness；它与推理模型共享提示模板、解码参数、目标上下文、构建环境和执行预算。
- 开源权重通用推理模型 `gpt-oss:20b`：作为主要 LLM 条件，与代码专用模型比较，考察一般推理能力是否有助于处理跨文件 API、构建依赖和编译诊断。
- 无静态上下文消融：模型只接收目标元数据，不接收相关源码窗口、候选描述、输入话题和安全相关输出；修复阶段也不重新加入这些信息。该条件用于隔离静态分析上下文对工件生成和后续编译修复的贡献。
- 确定性朴素模板基线：依据目标元数据生成固定脚手架，作为不依赖 LLM 推理的下界。它检验实验收益是否只是来自统一工件结构和构建流程，而非模型对目标代码的理解。

**实验想回答的问题**

- 在真实 Autoware 构建环境中，本地开源权重 LLM 能否为攻击者可达的软件弱点生成可编译、可链接、能把模糊输入传递到目标实现的动态测试工件，并最终确认可复现的安全或安全性缺陷？
- 模型类型、静态分析上下文和编译器反馈修复分别如何影响测试工件跨越“生成、对象编译、链接、执行、触达目标、发现真实缺陷”各阶段的能力；失败的主要瓶颈究竟是程序逻辑、依赖接线，还是动态执行本身？

**实验实现**

实验固定提示模板、目标上下文、解码参数、Autoware 工作区、构建环境和执行预算，仅改变模型；无静态上下文条件额外移除静态分析信息。两个本地开源权重模型通过 Ollama 的 OpenAI 兼容端点提供服务，解码参数为 temperature 0.1、max_tokens 4096。每个 harness 使用 `compile_commands.json` 中对应目标翻译单元的包含路径、宏定义和编译选项，由 `clang++` 在 AddressSanitizer 与 UndefinedBehaviorSanitizer 下编译。失败样本最多接受 3 轮编译器在环修复，输入为失败源码和 Clang 诊断。通过对象编译后再链接为 libFuzzer 可执行文件；配置预算为每目标 600 秒，但成功链接样本实际执行时间为每目标 60 秒。崩溃经过去重和人工核查，检查目标可达性、复现性及安全影响。该协议把对象可编译、成功链接、真实目标触达和弱点确认严格分开，避免把前置集成失败误判为候选已被动态否证。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除静态分析上下文，仅保留目标元数据 | 该消融确实被纳入五种实验条件之一，但给定原文节选没有报告其首次编译、修复后编译、链接、执行或确认结果，因而无法量化静态上下文的贡献。 | 该设置原本用于隔离源码窗口、候选描述、输入话题和安全输出信息是否帮助模型理解目标及生成有效 harness；修复时继续隐去上下文，可避免编译反馈阶段重新引入被消融信息。由于缺少对应结果，不能声称静态上下文有效、无效或造成性能变化。 | 第 6.2 节 Artifact Generation<br><span class="experiment-evidence">The no-static-context ablation receives only target metadata, while a deterministic baseline produces metadata-based scaffolds as a naive lower bound.</span> |

**定性案例**

- 桩代码崩溃构成一个跨样本的定性失败案例：修复过程为了绕过真实依赖而大量使用 stubbing，最终观察到的 37 次崩溃全部位于桩实现，而非 Autoware。它说明崩溃数量本身不是有效的安全发现指标，必须检查崩溃位置、真实目标是否被调用，以及 fuzzer 输入是否确实传播到该目标。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The study evaluates an LLM-driven compiler-feedback workflow for generating, repairing, and executing security test harnesses in a large software stack.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`904249b309a7d74df4f0b7f1a95bff07c1f53e448e587227d6b8ac809b99407b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
