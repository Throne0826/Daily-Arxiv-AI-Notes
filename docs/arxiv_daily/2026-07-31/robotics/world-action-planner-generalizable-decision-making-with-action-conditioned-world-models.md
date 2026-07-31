---
title: "[论文解读] World Action Planner: Generalizable Decision-Making with Action-Conditioned World Models"
description: "[arXiv 2607.27599][机器人 / 具身智能] World Action Planner以视觉语言模型提出高层动作方案，再借助动作条件世界模型想象执行结果并迭代修正，旨在让机器人在组合任务、新布局和零样本场景中获得比端到端模仿策略更强的泛化能力。"
arxiv_id: "2607.27599"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.192042+00:00"
source_sha256: "d2ef93f65a99ab9163f3328a4d64317869428d7a0baf1f3bad250c001f4c500f"
tags:
  - "机器人 / 具身智能"
  - "多模态 VLM"
  - "机器人操作"
  - "模型式规划"
  - "动作条件世界模型"
  - "视觉语言模型"
  - "位姿图像条件生成"
  - "测试时规划"
  - "组合泛化"
  - "零样本泛化"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.27599</p>

# World Action Planner: Generalizable Decision-Making with Action-Conditioned World Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Zhang, Xiangcheng, Du, Yilun</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27599) · [PDF 下载](https://arxiv.org/pdf/2607.27599) · **关键词** 机器人操作, 模型式规划, 动作条件世界模型, 视觉语言模型, 位姿图像条件生成, 测试时规划, 组合泛化, 零样本泛化<br>
**项目页**: [https://worldactionplanner.github.io](https://worldactionplanner.github.io)

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

World Action Planner以视觉语言模型提出高层动作方案，再借助动作条件世界模型想象执行结果并迭代修正，旨在让机器人在组合任务、新布局和零样本场景中获得比端到端模仿策略更强的泛化能力。

**不用术语来说**：机器人若只照着训练演示学习，往往记住的是“在某个位置做某个动作”，而不是真正理解任务目标和动作造成的物理后果。因此，一旦物体被移动、多个简单任务被串成较长流程，或测试时出现从未演示过的任务，机器人就可能抓向旧坐标、完成第一步后停滞，甚至发生碰撞。论文要解决的是：如何让机器人先构思动作，再预演和检查其结果，最后据此调整计划。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出World Action Planner，将视觉语言模型的高层推理与动作条件世界模型的物理预测结合起来，通过“提出方案—想象执行—反馈修正—局部搜索”的规划过程，为新任务和新场景合成动作序列，而非直接复现训练轨迹。
- 构建姿态—图像条件、多视角、多任务机器人世界模型，并从表格设定与线性函数逼近设定分析基于模型的规划为何可能比模仿学习具有更好的多任务泛化；作者还在仿真中的组合任务、新布局和零样本场景上验证这一主张，但尚未进行真实机器人实验。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于机器人操作中的模型式决策与规划研究。目标是让机器人面对训练演示之外的新任务、新场景和新物体布局时，仍能生成可执行动作。主流端到端模仿学习策略直接从视觉与语言指令预测动作，但其行为容易受训练轨迹分布限制；本文转而采用“先提出动作计划，再用世界模型想象执行结果并修正计划”的路线，把视觉语言模型的任务推理能力与动作条件世界模型的物理预测能力结合起来。这里的世界模型接收当前视觉观测及候选机器人动作，预测动作可能造成的未来画面，从而在真实执行前检查任务进展、碰撞风险和操作可行性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉语言模型（VLM）**

能够联合理解图像和自然语言的基础模型，可依据场景图像与任务指令进行物体识别、空间推理和步骤规划。本文用它提出并审查动作计划，但不假设它仅凭语言推理就能准确掌握机器人动力学。

</div>
<div class="concept-item" markdown="1">

**动作条件世界模型**

一种预测模型：给定当前场景和候选动作，生成该动作执行后可能出现的未来视觉状态或轨迹。它相当于供规划器试演动作的模拟器，使系统能够先比较想象结果，再决定真实执行什么。

</div>
<div class="concept-item" markdown="1">

**模型式规划**

利用环境预测模型评估、搜索和优化动作序列，而不是直接由策略一次性输出最终动作。本文中的规划会反复经历动作提议、未来轨迹想象、反馈纠正和候选搜索，以处理组合任务及训练分布外布局。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

系统面对机器人操作任务：输入包括当前场景的多视角图像、自然语言任务描述、机器人当前状态，以及可供调用的原子技能或候选低层动作；输出是能够在物理环境中执行的动作序列。测试设置重点包含三类泛化：将训练时分别出现的原子技能组合成长时程任务、改变物体位置或场景布局，以及零样本处理未见任务或配置。核心假设是训练得到的多任务世界模型能够依据机器人位姿图像和动作推演未来交互，而视觉语言模型能够读取这些想象轨迹并判断任务进展或失败原因。与需要直接复现专家动作分布的端到端策略不同，该问题允许系统在测试时对多个动作方案进行模拟、修正与局部搜索；世界模型所需的未来机器人位姿由动力学计算得到，而不是从真实未来帧中提取，因此可以用于尚未执行动作的反事实预测。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Vision-Language-Action（VLA）模型，包括 OpenVLA 与 π0.5**: 这类方法以预训练视觉语言模型为骨干，通过自回归动作头或扩散式动作专家直接生成动作，属于本文重点对照的端到端模仿学习路线。它们依赖带动作标注的高质量演示，测试行为可能受训练轨迹和示范坐标束缚；本文改用视觉语言模型负责规划、世界模型负责物理落地与验证。
- **World-Action Models（WAM）与视频规划器**: WAM通常微调视频生成模型，使其同时生成未来画面与动作；视频规划器则先生成任务完成视频，再通过逆动力学模型或位姿估计恢复控制动作。本文与它们都利用未来视觉预测，但区别在于采用动作条件世界模型评估明确提出的候选动作，并引入视觉语言模型代理在测试时依据想象轨迹进行推理、纠错和搜索。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

实际机器人需要在异构环境中连续处理多种任务，而测试条件通常不会与演示数据完全一致：物体位置可能变化，若干原子操作可能被重新组合成长时程任务，还可能出现未经演示的新目标。系统不仅要决定“下一步做什么”，还必须判断动作是否可执行、是否会碰撞以及某个子任务结束后如何过渡到下一个子任务，这使依赖固定训练轨迹的策略难以可靠部署。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于视觉语言模型的端到端模仿学习策略（包括VLA类模型）**：模型以视觉观测和语言任务为输入，直接从专家演示中学习输出机器人动作。预训练视觉语言模型提供语义知识，但动作生成仍主要受训练期间所见轨迹分布约束。
- **以视频生成模型为骨干的端到端策略（文中概括为WAM类方法）**：这类方法利用生成模型所学习的视觉变化模式来预测未来或生成控制行为，希望以视觉动态知识支持机器人操作；然而在本文的论述中，它们仍属于由演示数据驱动的端到端策略，缺少显式提出、模拟并修订动作计划的闭环。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 端到端模仿策略受演示覆盖范围限制：只在单独拾取—放置轨迹上训练时，可能无法组合出对象之间的移动与子任务衔接，因此在长时程组合任务中容易完成首个子任务后停滞。
- 模型可能拟合演示中的偶然运动模式而非任务因果关系，例如训练数据总在固定坐标抓取时，即使物体已经移动仍伸向旧坐标；同时，仅靠基础模型生成的高层计划通常缺乏对物理动力学、碰撞风险和动作可执行性的可靠理解。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法尚未同时打通两种能力：一方面利用基础模型理解语言目标并进行系统性的高层动作组合，另一方面以具有动作可控性和物理落地能力的世界模型预演候选动作，进而依据预演结果优化和搜索可执行方案。缺少这一接口，使高层推理难以直接转化为安全、精细且能适应未见配置的机器人动作。

</div>
<div markdown="1"><span>核心问题</span>

能否训练一个可跨动作、场景和任务泛化的姿态—图像条件世界模型，并让视觉语言模型围绕其想象轨迹反复提出、评估、修正和搜索动作，从而在组合任务、物体位置变化及零样本任务中，比受专家轨迹分布束缚的端到端策略更可靠地完成决策？

</div>
<div markdown="1"><span>作者直觉</span>

模仿学习像是记住示范者走过的路线，而基于世界模型的规划更像是在行动前使用“内部模拟器”试走多条路线。视觉语言模型负责把任务拆成有意义的步骤，世界模型则显示这些动作可能造成的视觉与物理后果；若想象结果暴露出目标位置错误、碰撞或抓取失败，系统便可在真实执行前调整动作，并通过局部搜索比较更细粒度的候选方案。这样，系统复用的是环境动力学与任务推理能力，而不只是复现某条专家轨迹。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

World Action Planner（WAP）不是直接把视觉观测映射成机器人动作，而是组合视觉语言模型（VLM）、低层控制器、动作条件世界模型和可选的模仿学习策略。给定任务描述 $\ell$、当前视觉与本体状态 $s$，VLM先提出由 MOVE、ROTATE、GRASP、RELEASE 等原语构成的高层计划；控制器 $\phi$ 将目标末端执行器位姿转换为可执行动作 $a$。世界模型随后预测执行这些动作后的多视角视频，VLM依据预测结果先做全局语义纠错，再在候选动作附近进行局部网格搜索与排序，最终只把筛选出的动作 $a_{i^*}$ 送入真实环境。若任务需要精细抓取，系统还可以预测候选动作之后的策略 $\pi$ rollout，以选择最适合策略接管的中间状态。

支撑规划的是姿态图像条件世界模型。它不直接用机器人特有的低维动作向量作为条件，而是通过动作的前向动力学计算未来关节位置，并从相机视角渲染为机器人骨架式姿态图像；姿态帧经视频模型的 VAE 编码后，与视频 token 拼成统一序列。第三人称和腕部视角被组合到同一帧网格中，使模型能从多视角关系推断关节与物体的相对三维位置。直观地说，该系统先让 VLM提出“做什么”，再让世界模型播放“这样做会发生什么”，最后让 VLM基于预演结果纠错和选择，从而把语言模型的常识推理与机器人世界模型的物理落地能力结合起来。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 多视角状态理解与动作原语提议

VLM代理调用 $\texttt{Agent.ProposeActions}(s,\ell)$ 生成 MOVE、ROTATE、GRASP、RELEASE 等动作原语序列 $g$。对于 MOVE，代理在多个相机视图中指出目标夹爪的二维像素位置，系统通过多视角三角化恢复三维目标，无须显式深度输入。

<div class="method-step__io" markdown="1">

**输入**：任务描述 $\ell$、当前状态 $s$，其中包括第三人称图像、腕部图像和机器人本体状态 $s_{\mathrm{proprio}}$。<br>
**输出**：高层动作原语及目标末端执行器位姿 $g$。

</div>

**直观理解**：VLM负责理解指令和场景，例如判断“应该移动到哪个物体旁边”；多视角三角化则把图像中的点击位置换算成机器人可使用的空间位置。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 低层动作生成与世界模型预演

低层控制器计算动作块 $a=\phi(g,s_{\mathrm{proprio}})$；动作经前向动力学转换为未来关节位置并渲染成多视角姿态图像，姿态图像作为无噪声条件输入世界模型，以生成预测后继状态或 rollout 视频 $\hat{s}_{\texttt{next}}=\texttt{WM}(s,a)$。

<div class="method-step__io" markdown="1">

**输入**：VLM提出的目标 $g$、本体状态 $s_{\mathrm{proprio}}$ 和当前状态 $s$。<br>
**输出**：候选机器人动作序列 $a$，以及该序列可能导致的视觉后果 $\hat{s}_{\texttt{next}}$。

</div>

**直观理解**：控制器把“夹爪去杯子上方”翻译成连续关节动作；世界模型则像模拟器一样先播放执行结果，但其条件是可视化的机器人骨架，而不是某一机器人的专用动作编号。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 基于代理反馈的全局优化

VLM检查预测轨迹是否安全且符合任务目标，并通过 $\texttt{Agent.Optimize}(\hat{s}_{\texttt{next}},\ell)$ 给出高层修正 $\Delta g$；控制器再将 $g+\Delta g$ 转换为更新后的动作。例如，预测到碰撞时可提高运动高度，预测到物体落点偏后时可要求向前调整。

<div class="method-step__io" markdown="1">

**输入**：预测 rollout $\hat{s}_{\texttt{next}}$、任务描述 $\ell$、原动作目标 $g$ 和本体状态 $s_{\mathrm{proprio}}$。<br>
**输出**：经过大尺度语义纠错的动作序列 $a=\phi(g+\Delta g,s_{\mathrm{proprio}})$。

</div>

**直观理解**：这一步处理“方向明显不对、会撞到障碍物、放置区域错误”等大问题。VLM不必直接给出精确距离，只需看预演视频并说明应该怎样改。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 局部候选搜索、策略接管评估与执行

系统在 $a$ 周围通过 $\texttt{GridSearch}$ 生成 $N$ 个候选 $a_1,\ldots,a_N$，分别用世界模型预测 $\hat{s}_i$；若启用策略，还继续预测从 $\hat{s}_i$ 出发执行 $\pi(\hat{s}_i)$ 的结果。VLM比较所有预测视频并选出索引 $i^*$，环境执行 $a_{i^*}$，必要时随后执行策略动作，循环直至 $\texttt{done}$。

<div class="method-step__io" markdown="1">

**输入**：全局优化后的动作 $a$、当前状态 $s$、任务描述 $\ell$，以及可选的模仿学习策略 $\pi$。<br>
**输出**：被选中的动作 $a_{i^*}$、更新后的真实状态 $s$ 和任务终止标志 $\texttt{done}$。

</div>

**直观理解**：VLM可能难以说出“向左移动几毫米”，却较容易从多个视频中看出哪一个抓取位置最好，因此系统把精确回归改成候选选择。已有策略被当作擅长局部操作的工具，而非必须独立解决整个新任务的端到端代理。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 动作提议、世界模型预演与全局反馈修正

$$
g=\texttt{Agent.ProposeActions}(s,\ell),\quad a=\phi(g,s_{\mathrm{proprio}}),\quad \hat{s}_{\texttt{next}}=\texttt{WM}(s,a),\quad \Delta g=\texttt{Agent.Optimize}(\hat{s}_{\texttt{next}},\ell),\quad a\leftarrow\phi(g+\Delta g,s_{\mathrm{proprio}})
$$

**符号说明**

- $s$：当前环境状态，包含供代理和世界模型使用的视觉观测，并关联机器人本体状态。
- $\ell$：自然语言任务描述。
- $g$：VLM提出的动作原语序列或目标末端执行器位姿。
- $s_{\mathrm{proprio}}$：机器人的本体感知状态，例如当前关节或末端执行器状态。
- $\phi$：把高层目标和当前本体状态转换成低层动作块的机器人控制器。
- $a$：供世界模型预测并最终可能执行的低层机器人动作序列。
- $\texttt{WM}$：动作条件世界模型。
- $\hat{s}_{\texttt{next}}$：世界模型预测的动作后继状态或 rollout 视频。
- $\Delta g$：VLM根据预测后果给出的高层动作修正。

<div class="equation-explanation" markdown="1">

**直观理解**：该式概括闭环纠错：先提出计划并转换成动作，再让世界模型预演；如果预演显示碰撞、偏离目标等问题，VLM不直接修改关节值，而是修正高层目标，随后由控制器重新生成动作。这使优化建立在预测到的物理后果上，而不是只依赖初始图像和语言常识。<br>
**原文位置**：第3.2节，Algorithm 1：Agent Action Proposal 与 Global Optimization Guided by Agent Feedback

</div>

</div>

<div class="equation-block" markdown="1">

#### 局部候选预演与代理排序

$$
a_1,\ldots,a_N=\texttt{GridSearch}(a),\quad \hat{s}_i=\texttt{WM}(s,a_i),\quad \hat{s}_i\leftarrow\texttt{WM}\!\left(\hat{s}_i,\pi(\hat{s}_i)\right)\ \text{if policy is used},\quad i^*=\operatorname*{argmax}\texttt{Agent.Rank}(\hat{s}_1,\ldots,\hat{s}_N,\ell)
$$

**符号说明**

- $N$：局部搜索产生的候选动作数量。
- $a_i$：围绕当前动作生成的第 i 个局部候选。
- $\hat{s}_i$：执行第 i 个候选后预测到的状态；启用策略时还包含后续策略 rollout 的预测结果。
- $\pi$：可选的模仿学习操作策略，用于完成局部精细动作。
- $i^*$：VLM根据任务符合度和预测轨迹质量选出的最佳候选索引。
- $\texttt{Agent.Rank}$：VLM对多个预测 rollout 进行比较排序的操作。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把难以可靠完成的精确坐标生成转化为多选一判断：系统先在动作附近枚举若干微调，再比较各自的未来视频。若后续要交给策略完成抓取，排序依据不只看候选动作刚结束的状态，还看策略从该状态继续运行后是否成功。<br>
**原文位置**：第3.2节，Algorithm 1：Local Search with Agent Ranking

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：世界模型的训练目标是基于 flow-matching 的 diffusion-forcing，但所给章节没有展示其显式损失公式，因此不应补造具体积分、速度场或权重形式。训练时，历史视频 token 被加入彼此独立的随机噪声，未来视频 token 被加入均匀噪声，姿态图像 token 始终保持无噪声并充当动作控制条件；优化使模型在这些条件下恢复或预测未来视频演化。其作用是让模型学习“当前场景与未来机器人姿态给定时，视觉世界将如何变化”，从而为规划阶段提供可比较的动作后果。VLM代理、低层控制器以及可选策略的训练目标在所给方法章节中没有统一定义；规划本身主要是测试时的生成、反馈修正和搜索，而不是对整个系统进行端到端反向传播。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 姿态图像条件、多视角动作世界模型**

模型先依据动作的前向动力学计算未来机器人关节位置，再从对应相机视角渲染姿态骨架帧。姿态帧通过视频模型的 VAE 编码，其 token 与真实视频 token 连接为统一序列；第三人称与腕部视图在每个视频帧和姿态帧中拼成网格。训练采用 diffusion-forcing 与 flow-matching：历史视频 token 加独立随机噪声，未来视频 token 加均匀噪声，而作为动作条件的姿态图像 token 保持无噪声。

> 直观理解：低维动作向量的维数和含义会随机器人变化，模型容易把动作语义绑定到特定硬件；姿态图像则直接展示“机器人身体将移动到哪里”，为不同机械臂和动作空间提供较统一的视觉接口。多视角还能缓解单个相机无法可靠判断前后、遮挡和深度的问题。

**2. VLM代理与分层动作接口**

VLM根据状态 $s$ 和语言任务 $\ell$ 生成离散动作原语与目标末端位姿 $g$，低层控制器 $\phi$ 再结合 $s_{\mathrm{proprio}}$ 输出可执行动作块。VLM还承担 rollout安全性检查、语义修正和候选排序，但不被要求直接稳定地产生全部关节控制量。

> 直观理解：这种分层设计让语言模型负责其擅长的物体识别、任务分解和关系判断，让控制器负责连续运动。它避免把视觉语言模型不可靠的度量坐标直接当作最终控制命令。

**3. 全局纠错、局部搜索与策略工具化**

全局阶段根据预测视频产生语义修正 $\Delta g$，用于消除碰撞、错误路径或明显落点偏差；局部阶段围绕修正后的动作采样 $N$ 个候选，并以VLM对世界模型 rollout 的判别排序代替直接坐标回归。对于精细操作，系统可把 diffusion policy、VLA 或 WAM 等策略作为模块化工具，并预演候选动作之后的策略 rollout，以选择适合策略接管的状态。

> 直观理解：全局优化负责改正“大方向错误”，局部搜索负责比较细微位置差别。策略只在已有示范覆盖、且其精细动作能力可靠的局部区域工作，VLM与世界模型则负责把机器人带到该区域并处理分布外的连接动作。

**训练与推理**

训练阶段，先由轨迹中的机器人动作通过前向动力学获得未来关节位置，并针对第三人称和腕部相机渲染姿态图像；真实视频与姿态帧分别经同一视频模型的 VAE 编码后，在 token 层连接。模型以多任务数据学习动作条件视频预测，且姿态图像提供跨动作空间的视觉化控制接口。若使用 diffusion policy、VLA 或 WAM 等工具策略，它们可在有示范的数据分布内单独训练；WAP不要求这些策略覆盖所有组合任务或新布局。

推理阶段以闭环方式反复执行：VLM根据 $s$ 与 $\ell$ 提出原语和目标位姿，控制器生成动作，世界模型预演未来；VLM先依据预演视频输出全局修正，再对动作附近的网格候选进行逐一预演和排序。精细操作时，每个候选之后还可接入策略 $\pi$ 并在世界模型中继续 rollout，以判断候选是否把机器人带到策略能够成功接管的状态。系统仅执行排名最高的 $a_{i^*}$，可选地继续执行一次策略动作，然后用真实环境返回的新状态重新规划，直至任务结束。因而世界模型承担的是反事实预测，VLM承担的是计划生成与判别，真实机器人不会执行被预测为明显不安全或效果较差的候选。

**复现信息**

复现方法结构所必需的信息包括：世界模型同时接收腕部与第三人称视图，并将两种视图在每帧中拼为网格；动作条件由前向动力学得到的未来关节姿态图像表示，而非仅用低维动作通过 AdaLN-Zero 或交叉注意力注入；姿态图像经视频模型 VAE 编码并与视频 token 拼接。MOVE 目标通过多视角二维像素三角化为三维位置，低层控制器以当前状态和目标末端执行器位姿生成动作块。规划需要实现一次全局反馈修正、围绕动作的局部网格搜索、世界模型候选 rollout、VLM排序，以及可选的策略后续 rollout。所给正文未明确报告网格大小 $N$、候选间隔、优化轮数、视频预测长度、flow-matching 损失的具体形式或控制器架构，这些参数仍需查阅附录 C.1.1 与 C.2 后才能完整复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LIBERO 与 RoboCasa：两套模拟机器人操作基准，用于检验模型在不同任务和场景中的动作条件未来预测能力。每个任务使用 100 条训练轨迹，其中包含按 MPPI 方法加入高斯噪声的扰动版本；另保留 10 条轨迹用于评估。扰动轨迹的作用是覆盖示范数据之外的探索性动作，降低世界模型只会复现专家轨迹的风险。
- MimicGen：模拟操作数据套件，同样采用每任务 100 条训练轨迹和 10 条留出评估轨迹，用于扩大任务与运动模式的多样性，并检验模型能否学习多任务动力学。
- DexMimicGen：面向灵巧操作及不同机器人形态的数据套件，主要服务于跨本体、跨动作空间测试。它与 MimicGen 共同检验位姿图像这种视觉化动作表示能否避免依赖某一种机器人的低维关节或末端执行器动作格式。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**LPIPS**

学习式感知图像相似度，用深层视觉特征衡量预测帧与真实未来帧之间的感知差异；相较逐像素误差，它更关注人眼可感知的结构和外观偏差。 （越低越好，因为较低距离表示生成未来图像在感知特征上更接近真实图像。）

</div>
<div class="metric-item" markdown="1">

**PSNR**

峰值信噪比，根据预测图像与真实图像的像素误差衡量重建保真度，可反映生成帧是否出现明显噪声或数值偏差。 （越高越好，因为更高信噪比通常表示预测图像与真实图像之间的像素误差更小。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前节选没有包含第 5.1 节结果表、第 5.2 节规划实验、消融实验或定性案例，因此不能可靠填写三项主要结果、数值改进、成功率、置信区间或组件贡献；相应字段保持为空，而不是从摘要推断。
- 评估设置只报告每任务 10 条留出轨迹，且未说明随机种子、误差条、跨任务聚合方式及测试轨迹是否包含训练分布之外的机器人本体、布局和动作。因而即使获得 LPIPS 或 PSNR 均值，也需要结合方差、物理一致性和闭环规划成功率判断泛化能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- WPE：扩散式世界模型，以 AdaLN-Zero 将低维动作嵌入注入视频生成骨干。它是有意义的对照，因为可直接比较“低维动作调制”和本文“机器人位姿图像条件”两种动作表达方式。
- IRA-Sim：同样通过 AdaLN-Zero 使用动作嵌入的扩散式世界模型。与 WPE 一起代表当前低维动作条件路线，可用于判断收益是否来自本文的条件表示，而非仅来自扩散视频骨干。
- Ctrl-World：通过交叉注意力接收低维动作 token。该基线采用与 AdaLN-Zero 不同的条件注入机制，因此能够区分本文优势究竟来自位姿图像本身，还是仅来自改变动作条件的融合方式。
- 跨本体 VLA 改造基线：包括统一动作空间、机器人本体感知编码器和软提示三类架构适配。它们代表显式对齐不同机器人动作接口的方案，用于检验位姿图像条件是否更适合共享跨本体动力学。节选没有给出这些改造基线各自的正式模型名称或单独成绩。

**实验想回答的问题**

- 世界模型层面：机器人位姿图像条件能否支持准确的多视角未来图像生成，并且比低维动作条件在未见状态或探索性动作上具有更好的泛化能力？这对应原文的 Q1 与 Q2。
- 跨本体与规划层面：同一模型能否学习不同机器人本体和动作空间的动力学，并为后续 World Action Planner 提供可用于推演与决策的环境预测？节选仅给出了世界模型实验设置，未提供第 5.2 节规划实验的具体协议与结果。

**实验实现**

所有方法均使用 Wan-T2V-1.3B 作为视频生成骨干，并采用相同的相机配置和帧时间表，以控制骨干能力及观测条件。本文模型微调 10K 步、全局批大小为 64；基线训练 20K 步，即训练时长为本文的两倍，作者意图是给予基线更充分的优化预算。模型读取以 7 FPS 采样的 21 帧历史，预测以 20 FPS 表示的 20 帧未来；四个相机视角被拼成 $2\times2$ 网格，每个视角为 224 像素。推理采用 20 个扩散采样步骤。每个任务的训练轨迹还依照 MPPI 方法加入高斯噪声，使测试更接近规划时可能遇到的非专家动作。该协议主要评估图像预测质量；节选未说明 LPIPS、PSNR 是逐帧计算后平均，还是按视角、轨迹或任务汇总，也未给出第 5.2 节机器人规划的成功率协议。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出结合VLM与动作条件世界模型的机器人规划系统，通过想象轨迹搜索和优化提升任务泛化。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`d2ef93f65a99ab9163f3328a4d64317869428d7a0baf1f3bad250c001f4c500f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
