---
title: "[论文解读] Tri-Manual Visuomotor Imitation Learning of Robot Policies"
description: "[arXiv 2607.25731][机器人 / 具身智能] 本文研究单人通过双手遥操作采集三臂机器人示范时产生的非必要串行化问题，并提出通过离线重排示范时序来训练三臂同步策略的 TriManPolicy。"
arxiv_id: "2607.25731"
announcement_date: "2026-07-30"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:25.037315+00:00"
source_sha256: "805cc41f1613406669244277d1c14952d4c805a2671543b7d971be6e2016da79"
tags:
  - "机器人 / 具身智能"
  - "三臂机器人"
  - "视觉—运动模仿学习"
  - "单人遥操作"
  - "行为克隆"
  - "成对模式切换"
  - "示范重定时"
  - "Dependency-Aware Tri-Arm Scheduling"
  - "同步多臂控制"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.25731</p>

# Tri-Manual Visuomotor Imitation Learning of Robot Policies

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> James Zhao, Mingyuan Ba, Weiming Zhi</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.25731v2) · [PDF 下载](https://arxiv.org/pdf/2607.25731v2) · **关键词** 三臂机器人, 视觉—运动模仿学习, 单人遥操作, 行为克隆, 成对模式切换, 示范重定时, Dependency-Aware Tri-Arm Scheduling, 同步多臂控制  


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

本文研究单人通过双手遥操作采集三臂机器人示范时产生的非必要串行化问题，并提出通过离线重排示范时序来训练三臂同步策略的 TriManPolicy。

**不用术语来说**：三臂机器人可以让三条机械臂同时工作，但一名操作者一次只能连续控制其中两条；因此，原本可以并行完成的动作在示范中常被分成先后两段。若直接模仿这些记录，机器人不仅会学会正确动作，也会学到由操作界面造成的等待，无法充分利用第三条机械臂。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 将遥操作模仿学习扩展到“机器人拥有的同时控制通道多于单人示范接口”的三臂场景，明确区分任务本身要求的动作依赖与成对切换控制造成的采集时序。
- 提出依赖感知三臂调度 DATS：保留固定时长的局部传感—动作片段，在人工审核的任务顺序与机械臂使用约束下离线调整片段时间，使相互独立的跨臂动作能够重叠，并用重定时数据训练统一的三臂同步视觉运动策略。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于机器人视觉—运动模仿学习：系统把人类遥操作过程记录为包含视觉观测与机器人动作的轨迹，再用行为克隆学习从当前观测到动作的策略。常规双臂遥操作中，操作者的两只手可同时对应两个机器人末端执行器；本文研究这一对应关系失效的三臂场景——机器人能够同时协调三条机械臂，但单个操作者只能连续控制其中两条。第三条机械臂可承担支撑、稳定或呈递物体等辅助角色，使另外两臂不必因重新抓取或维持支撑而中断主要操作。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**视觉—运动模仿学习（visuomotor imitation learning）**

模型从示范轨迹中学习视觉观测到机器人动作的映射，而不依赖人工设计的奖励函数。训练后的策略根据相机等传感器输入直接预测机械臂控制指令。

</div>
<div class="conceptitem" markdown="1">

**行为克隆（behaviour cloning）**

行为克隆把示范中的观测—动作对当作监督学习样本，要求策略复现记录动作。由于它通常也继承示范的全局时间线，接口造成的等待和串行执行可能被误学为任务本身所需的行为。

</div>
<div class="conceptitem" markdown="1">

**成对模式切换（pairwise mode switching）**

单个操作者在三条机械臂的不同二臂组合之间切换，每一时刻只连续操控两臂，从而完成三臂示范采集。该接口覆盖了全部机械臂，却可能把本可并行的独立动作记录成先后执行。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是由一名操作者通过成对模式切换采集的三臂真实机器人示范，其中包含视觉/传感器观测与各机械臂动作；其原始时间顺序同时混合了任务依赖和遥操作接口引入的串行化。目标是在保留局部传感器—动作片段、必要任务先后关系及机械臂占用约束的前提下，离线重新安排片段时间，生成三臂同步监督数据，并据此训练一个从观测联合输出三臂动作的单一视觉—运动策略。设定假定任务中的部分跨臂动作可以并行，但必要依赖须经人工审阅；部署时策略同步控制三臂，不再需要依赖图或调度器。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$\pi$**

由示范数据训练得到的同步视觉—运动策略；根据当前观测联合预测三条机械臂的动作。

</div>
<div class="notationitem" markdown="1">

**$o_t$**

时刻 t 的视觉及其他传感器观测。

</div>
<div class="notationitem" markdown="1">

**$a_t^{(i)}$**

时刻 t 第 i 条机械臂的动作，其中 i 对应三条协作机械臂之一。

</div>
<div class="notationitem" markdown="1">

**$\tau$**

一条按时间排列的机器人示范轨迹，由观测和三臂动作组成；原始轨迹可能含有模式切换造成的非必要等待。

</div>

</div>

**直接相关的工作**

- **MART**: MART同样学习双臂或三臂协调，但使用多名操作者同时遥操作；TriManPolicy关注仅由一名操作者通过成对连续控制采集三臂示范，因此需要处理接口导致的时间串行化。
- **HATS**: HATS把辅助机械臂分配给在线多模态智能体，以避免操作者进行模式切换；TriManPolicy则保留单人模式切换采集方式，并在离线阶段重定时已执行的机器人片段。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

三臂系统可让第三条机械臂承担支撑、稳定或递送物体等辅助角色，例如撑开袋口或托住衣架，从而避免主操作臂反复换抓和等待。然而，单人只有两只手，无法通过标准遥操作接口同时连续控制三条机械臂，导致机器人的并行执行能力与示范者的控制能力不匹配。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **标准双臂遥操作与行为克隆**：操作者的两只手分别映射到两个机器人末端执行器，采集观察—动作轨迹，再通过行为克隆让策略复现示范中的动作及其时间组织。
- **三臂成对模式切换遥操作**：单次只控制三条机械臂中的两条，并通过切换受控机械臂对来覆盖全部三臂动作；最终记录可包含所有必要动作，但这些动作按照操作者的切换过程被分阶段执行。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 标准双臂遥操作隐含“操作者与机器人具有相同数量的同步控制通道”这一前提；三臂机器人打破该前提，因此无法直接获得三臂同时协调的自然示范。
- 成对模式切换会把本可并行的独立动作记录为串行动作；直接行为克隆会将界面造成的停顿和先后顺序误当成任务要求，在部署时复现不必要的等待，降低三臂协作效率。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有采集方式能够记录三条机械臂分别应执行什么动作，却缺少一种机制，在不破坏局部传感—动作行为和必要任务依赖的前提下，剔除仅由双手控制接口引入的时序约束，并形成可供三臂联合策略学习的同步监督。

</div>
<div markdown="1"><span>核心问题</span>

能否由一名操作者通过成对切换完成三臂示范，再依据任务顺序和机械臂占用约束离线重定时这些示范，使单一视觉运动策略在部署时联合控制三臂、减少非必要等待，同时不依赖在线调度器或依赖图？

</div>
<div markdown="1"><span>作者直觉</span>

示范中的“动作内容”和“动作发生时间”并不具有同等可信度：局部动作通常仍表达了正确的操作技能，但其先后关系可能只是操作者必须切换控制对象的产物。因此，可把示范切成保持局部传感—动作对应关系的短片段，只保留任务真正要求的顺序与同一机械臂不能同时执行多个动作等约束，再让彼此独立的跨臂片段在时间上重叠；这样训练数据便能展示机器人实际具备的三臂并行能力。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TriManPolicy是一条“采集—标注—重排—训练—部署”的三臂模仿学习流水线。输入是单个操作者通过双路控制器、在左臂L、右臂R和第三臂O的三个臂对LR、LO、RO之间切换而采集的演示；原始数据包含统一时钟下的图像、本体状态、三臂命令和当前控制模式。系统先把每段演示划分为固定时长的局部子任务，并由视觉语言模型提出边界、所需机械臂和前驱关系，再经人工审核。随后，Dependency-Aware Tri-Arm Scheduling（DATS）在不改变子任务内部传感—动作序列的前提下，为这些片段重新安排开始时间：必须满足任务前驱关系，同一机械臂不能同时参与两个片段，并以最小化整段演示的完工时间为目标。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 模式切换式三臂演示采集

每个时刻将两路输入分配给LR、LO或RO中的一个臂对，未被选中的机械臂执行保持控制；所有观测、三臂命令与模式轨迹按统一控制时钟记录。

<div class="method-step__io" markdown="1">

**输入**：操作者的两路连续控制输入，以及机器人三臂L、R、O的视觉、本体状态和夹爪状态。  
**输出**：原始演示集，其中每个时刻均含三臂同步格式的观测和动作，但动作时序可能受到操作者切换臂对的限制。

</div>

**直观理解**：操作者一次只能连续操控两只手，因此通过切换控制组合覆盖三只机械臂；这能录下正确的局部动作，却可能人为地把本可并行的动作排成先后顺序。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 子任务切分与依赖图构建

视觉语言模型提出子任务边界、所需机械臂集合、语义标签和前驱节点，作者审核并修正对象状态先决条件、支撑关系及共享工作空间顺序；系统另行检查格式、正时长、无环性和机械臂标识。

<div class="method-step__io" markdown="1">

**输入**：单条原始演示的视频与时间戳记录。  
**输出**：每条演示对应的有向无环图，其中节点记录原始区间、固定时长、占用机械臂和可选语义，边表示必须“前一片段完成后，后一片段才能开始”。

</div>

**直观理解**：该图不是完整的任务规划器，而是一张经人核查的最低限度施工图：它只说明哪些动作必须有先后、每个动作占用哪些手。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. DATS固定时长区间调度

将时间离散为0.01秒的整数刻度，用CP-SAT搜索各片段的新起止时刻；解必须满足全部前驱约束和逐臂NoOverlap资源互斥约束，并最小化最大结束时刻。

<div class="method-step__io" markdown="1">

**输入**：审核后的子任务图、各片段的原始持续时间和所需机械臂集合。  
**输出**：每条演示的最优重定时映射，即所有片段的新起止刻度及新的演示总时长。

</div>

**直观理解**：这类似在三台共享设备上重排固定长度的工序：没有依赖且不用同一只手的动作可以重叠，但真正的任务先决条件不能被打乱。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 重定时监督数据构造

对片段内所有消息施加相同时间偏移，多臂片段的各参与臂共享同一偏移；随后在数据集时钟上重新采样，图像和本体状态取最近样本，命令取输出时刻之前最近的因果样本，片段间则保持最近状态或命令。

<div class="method-step__io" markdown="1">

**输入**：原始的逐臂传感—动作消息，以及DATS给出的片段新位置。  
**输出**：新的同步三臂观测—动作序列，以及由其形成的长度为H的动作目标窗口。

</div>

**直观理解**：系统只搬动整段录像在时间轴上的位置，不改写片段内部动作，也不插值生成新轨迹；因此改变的是哪些三臂动作同时成为训练目标。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### DATS最小完工时间调度目标

$$
\{s_j^{\ast},e_j^{\ast}\}_{v_j\in\mathcal{V}_n},C_{\max}^{\ast}\in\arg\min_{\{s_j,e_j\},C_{\max}} C_{\max}\quad\mathrm{s.t.}\quad C_{\max}\ge e_j,\; e_j=s_j+d_j,\; e_p\le s_j\ \forall v_p\in\mathcal{P}_j,\; \mathrm{NoOverlap}(\mathcal{Q}_{\alpha})\ \forall\alpha\in\mathcal{A},\; s_j,e_j,C_{\max}\in\mathbb{Z}_{\ge0}
$$

**符号说明**

- $v_j$：第j个固定时长子任务节点。
- $\mathcal{V}_n$：第n条演示中的全部子任务节点集合。
- $s_j,e_j$：子任务j重新调度后的开始与结束整数刻度。
- $d_j$：子任务j从原始演示保留下来的离散持续时间，满足e_j=s_j+d_j。
- $\mathcal{P}_j$：子任务j经人工审核的前驱节点集合。
- $\mathcal{A}$：机械臂资源集合\{L,R,O\}。
- $\mathcal{Q}_{\alpha}$：所有占用机械臂α的调度区间集合。
- $\mathrm{NoOverlap}(\mathcal{Q}_{\alpha})$：机械臂α参与的任意两个子任务区间不得重叠；多臂子任务会同时占用其全部所需机械臂。
- $C_{\max}$：整条重定时演示的最大结束时刻，即完工时间或makespan。

<div class="equation-explanation" markdown="1">

**直观理解**：目标是在不缩短、不改写任何局部动作的情况下，把整条演示尽量排紧。前驱约束保护真实任务逻辑，资源互斥防止同一机械臂同时执行两个动作；二者之外的跨臂先后关系可以被放松，从而形成更合理的并行监督。  
**原文位置**：第III-D节，公式(8)；前驱约束和资源集合分别见公式(6)与公式(7)

</div>

</div>

<div class="equation-block" markdown="1">

#### 动作分块行为克隆目标

$$
\mathcal{L}(\vartheta;\mathcal{D})=\frac{1}{|\Omega_H(\mathcal{D})|}\sum_{(n,t)\in\Omega_H(\mathcal{D})}\ell\!\left(\pi_{\vartheta}(o_{n,t}),A_{n,t}^{H}\right),\qquad A_{n,t}^{H}=[a_{n,t},\ldots,a_{n,t+H-1}]
$$

**符号说明**

- $\vartheta$：同步三臂Transformer策略的可训练参数。
- $\mathcal{D}$：用于训练的演示集，可为原始演示或DATS重定时演示。
- $\Omega_H(\mathcal{D})$：演示集内所有有效长度H观测—动作训练窗口的确定性索引集合。
- $(n,t)$：第n条演示中从时刻t开始的训练窗口索引。
- $o_{n,t}$：窗口起点的视觉与机器人本体观测。
- $\pi_{\vartheta}(o_{n,t})$：策略根据当前观测预测的未来H步同步三臂动作块。
- $A_{n,t}^{H}$：从时刻t到t+H-1的真实三臂联合动作目标序列。
- $\ell$：预测动作块与示范动作块之间的训练损失；其具体形式在所给章节中未明确报告。

<div class="equation-explanation" markdown="1">

**直观理解**：原始条件与DATS条件优化完全相同的行为克隆目标，区别只在训练窗口中的监督内容。DATS会把彼此兼容的跨臂片段放入同一未来动作窗口，使策略学习同步进展，而非复制模式切换造成的等待。  
**原文位置**：第III-F节，公式(10)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练阶段首先独立求解每条演示的离散调度问题，得到满足审核后依赖和机械臂互斥条件的最小完工时间时间线；这一优化不学习神经网络参数，而是改变训练数据的时间排列。随后，策略参数通过公式(10)在全部有效动作窗口上最小化平均动作分块损失。论文的因果比较设计是保持网络、损失、窗口采样、终端填充和掩码规则不变，仅将原始数据替换为DATS重定时数据，因此性能差异应主要解释为联合三臂监督组成发生变化，而不能简单归因于不同模型或损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 人工审核的子任务依赖图**

节点v_j包含所需机械臂集合、原始起止时间、前驱集合和可选语义标签；调度只使用区间边界、机械臂集合和前驱ID，语义标签不进入优化目标。前驱边编码跨臂任务先决条件或需保留的顺序，机械臂集合则编码片段持续期间的资源占用。

> 直观理解：关键是区分“任务真的要求先后”和“因为操作者只有两路控制而碰巧先后”。如果两个片段没有依赖路径且使用不同机械臂，DATS便可重新安排它们；人工审核用于避免错误地并行化存在对象状态或支撑依赖的动作。

**2. Dependency-Aware Tri-Arm Scheduling（DATS）**

DATS把每个子任务建模为持续时间固定的整数区间，以三只机械臂作为互斥资源。它强制所有finish-to-start前驱约束和逐臂NoOverlap约束，并最小化episode makespan；论文使用Google OR-Tools 9.12中的CP-SAT求解。

> 直观理解：DATS不是删除停顿的剪辑工具，而是根据依赖和资源重新组合三臂监督。例如一只手处理胶带时，另外两只手可同时准备袋子，但胶带插入仍必须等待袋口形成。

**3. 动作分块同步三臂策略**

Transformer策略以当前视觉和本体观测o_t为条件，一次预测未来H步的三臂联合动作序列；片段边界不作为输入，也不会重置动作块。原始数据与DATS数据采用相同网络、窗口索引规则、终端填充和损失掩码，因此主要变量是监督时间线及联合目标窗口的组成。

> 直观理解：一次预测一段未来动作有助于表达连续协调。DATS让训练窗口更常出现真正可并行的三臂进展，而不是“一只手动作、其他手因界面限制而等待”的示范模式。

**训练与推理**

训练时，对每条模式切换演示先生成并人工审核子任务图，再以CP-SAT求解DATS。对原始片段内时间q，系统采用时间映射\phi_{n,j}(q)=\Delta t\,s_j^{\ast}+(q-\bar{s}_j)，即整体平移到新起点并保留片段内相对时间；多臂片段共享偏移，片段间使用初值或最近值保持。重建同步数据后，枚举所有有效长度H窗口，以当前观测预测未来H步三臂动作并优化行为克隆损失。
部署时，机器人提供物理上同步的实时图像和本体状态，策略直接输出同步三臂动作块并闭环执行。推理不访问控制模式、子任务标签、片段边界、依赖图或DATS求解器；因此DATS本质上是离线监督构造方法，而不是在线任务规划模块。该方法能否工作依赖一个关键假设：经图判定可组合的逐臂局部片段在新的并发上下文中仍具有物理和语义意义。

**复现信息**

时间以\Delta t=0.01秒离散；原始片段起点向下取整、终点向上取整，以保留其离散持续时间，舍入最多可能延长两个刻度，延长部分保持末值。调度使用Google OR-Tools 9.12的CP-SAT；图的自动检查覆盖结构合法性、正持续时间、无环性和机械臂标识，但任务依赖与支撑关系仍需人工审核。重定时不使用插值、逆运动学连接或边界处的新运动；图像和本体状态取最近时间样本，命令取不晚于输出时刻的最近样本，以维持动作采样的因果性。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- 真实机器人三臂示范集：共237条处理后示范，覆盖TowelHang、BinTowel、ToteCards、BagTape、LidEraser和TrayWipe六项任务；各任务分别有47、30、50、30、30和50条示范。每项任务都包含一个机械臂建立或维持条件、另一个机械臂据此执行操作的耦合阶段。实验不使用独立测试数据集，而是在真实机器人上从带有数厘米物体位姿变化的匹配初始状态进行策略评测。
- Raw时间线：保留双手遥操作和切换控制所记录的原始时间安排，作为策略训练的基准监督。它用于检验原始串行化示范是否会把人为等待复制到策略中。
- DATS与Gap诊断时间线：DATS对Raw中的同一批局部动作片段进行依赖约束下的离线重排，并作为另一训练条件；Gap删除所有无标注片段活动的最大空闲区间，但保持原有片段顺序和重叠关系，仅用于离线诊断、不训练策略。三种时间线共享相同的动作片段样本，便于区分删空闲与重新组织跨臂监督的影响。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**任务成功数（Succ.）**

每个任务、每种训练条件进行25次真实机器人试验，按任务特定完成标准统计成功次数；安全停止或超过10秒不可恢复的状态计为失败。该指标检验加速是否以牺牲任务完成可靠性为代价。 （越高越好，因为表示在固定试验次数中满足完整任务完成标准的次数更多。）

</div>
<div class="metricitem" markdown="1">

**成功试验平均完成时间与时间降幅**

从策略释放（预对齐后）到首次视觉上满足完成标准的时间，仅对成功试验计算均值和样本标准差；宏平均对六个任务的均值等权平均。它衡量成功执行时的协调效率，但排除失败试验，因此必须结合成功数解读。 （完成时间越低、相对Baseline的降幅越高越好，因为表示在成功条件下更快完成任务。）

</div>
<div class="metricitem" markdown="1">

**共同目标窗口覆盖率（co-window coverage）**

对第n条示范及时间线X，定义为ρ_n^X=|C_n^{H,X}|/|C_n|：C_n是允许并行安排的候选片段对，C_n^{H,X}是至少有一个长度为H的有效目标窗口同时包含该对两个片段样本的子集。论文使用H=100步、即2.0秒。该指标衡量有多少种合格跨臂片段对进入共同训练窗口，而非部署时并发动作的频率。 （越高通常越好，因为同步三臂策略可在更多动作块中同时看到兼容的跨臂目标；但它本身不是任务成功率，也不能单独证明实际协调更好。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 六项真实机器人任务的总体效率比较：Raw Baseline与DATS各150次试验

<div class="result-value" markdown="1">

DATS在六项任务的成功试验中均具有更短的平均完成时间，单任务降幅为31.3%至49.9%；六任务非加权宏平均由83.1秒降至47.8秒，下降42.5%。

</div>

这说明将同一批示范片段按依赖关系重新定时，与更高效的三臂执行一致，而且效果并非由某一项任务单独驱动。由于完成时间只在成功试验上计算，该结果必须与成功数共同看待；同时，实验没有跨训练种子重复，不能据此估计训练随机性下的置信区间或稳定性。

<div class="result-source" markdown="1">

来源：第IV-B节，表II

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">DATS-trained policies have lower mean completion time among successful trials on every task, with reductions between 31.3% and 49.9%. The unweighted macro-mean falls from 83.1 s to 47.8 s, a 42.5% reduction.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 六项真实机器人任务的成功表现：每项任务、每种条件25次试验

<div class="result-value" markdown="1">

DATS共成功129/150次，Baseline成功126/150次；DATS在每项任务上的成功次数均不低于Baseline。其中TowelHang为19/25对17/25，BinTowel为21/25对20/25，另外四项任务两条件成功数相同。

</div>

观察结果没有显示DATS通过更冒险地执行来换取速度：其总体及逐任务成功数至少未下降。不过129与126仅是观察计数，论文未给出显著性检验；因此合理结论是“在本次评测中成功表现可比且未观察到下降”，而不是证明DATS必然提高成功率。

<div class="result-source" markdown="1">

来源：第IV-B节，表II

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">DATS records 129 successes in 150 trials, compared with 126 for Baseline, with an equal or higher task-level count in all six tasks.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 237条示范上的跨臂共同目标窗口覆盖分析：Raw、Gap与DATS时间线

<div class="result-value" markdown="1">

共同窗口覆盖率的六任务宏平均从Raw的4.2%和Gap的11.5%提高到DATS的67.1%；配对比较中，全部237条示范的DATS覆盖率都高于Gap。

</div>

DATS并非只把示范整体缩短，而是让更多可兼容的跨臂片段进入同一个2秒动作预测窗口，从而改变同步策略实际接收的联合监督。该覆盖率按每条示范先计算比例，可避免分段更细的图在汇总中占过大权重；但它只刻画训练目标的组成，不等同于部署时三臂真正并发的持续时间，也不能脱离机器人结果单独证明因果收益。

<div class="result-source" markdown="1">

来源：第IV-C节，表IV与图6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">DATS increases co-window coverage over Raw and Gap on every task. The task macro-mean rises from 4.2% in Raw and 11.5% in Gap to 67.1% under DATS. The paired comparison in Fig. 6 shows higher co-window coverage under DATS than under Gap in all 237 processed episodes.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 每个任务和训练条件仅训练一次，随机种子固定为1000；25次真实机器人试验描述的是这些特定策略在初始状态变化下的表现，不能估计跨训练种子的方差。成功数也未报告统计显著性或置信区间。
- 真实机器人评测只比较Raw与完整DATS干预；Gap仅用于离线诊断而未训练策略。因此实验能够说明DATS整体有效、且其监督变化超越简单删空闲，但不能严格分解性能提升中“时长压缩”和“目标窗口组成改变”各自的因果贡献。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Baseline（Raw训练）：在原始示范时间线上训练与DATS条件完全相同的策略，是最直接的系统级对照。由于数据条数、动作内容、模型、训练步数和部署方式均保持不变，差异主要对应示范时间安排的改变。
- Gap时间线：删除全局无活动间隔，但不依据人工审核的任务依赖图重排片段。它是有意义的机制对照，因为Raw到Gap近似隔离“简单去除空闲”的作用，而Gap到DATS反映依赖感知放置带来的额外变化；但论文没有训练或部署Gap策略，因此它不能作为真实机器人性能基线。
- Raw离线诊断：在监督时长和共同窗口覆盖率分析中作为未经压缩、未经重排的参考，用来量化原始接口导致的片段间隔及跨臂联合监督不足。

**实验想回答的问题**

- 在使用完全相同的三臂示范样本和学习器时，经过依赖感知三臂调度（DATS）离线重定时的数据，能否让同步三臂策略更快完成真实任务，同时不降低观察到的任务成功率？
- DATS的作用是否只是删除示范中的空闲时段，还是会进一步改变不同机械臂动作片段进入同一预测窗口的方式，从而向策略提供更充分的跨臂联合监督？

**实验实现**

平台由三台相同的AgileX Piper-X带夹爪机械臂组成。策略接收以各机械臂为中心的RGB图像和本体感觉观测，以50 Hz同步输出关节与夹爪命令。学习器固定为动作分块Transformer，视觉编码器为冻结的SigLIP 2 Base-Patch16-256，预测窗口为100步（2.0秒），并采用时间聚合。每个任务分别训练Raw和DATS策略，共12个策略；每个策略训练100k步，批量大小16，AdamW固定学习率10^{-5}，种子1000。每个任务、每种条件进行25次交错排列的真实机器人试验，共300次；两条件使用匹配初始状态并加入数厘米级物体位姿变化。所有237个审核后的分段图均在30秒限制内由CP-SAT求得最优解。每个条件只有一次训练运行，因此真实机器人结果反映特定训练实例，而非跨随机种子的稳定均值。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Raw→Gap→DATS的离线时长审计，用Gap隔离简单删除全局空闲区间的作用 | 相对Gap，DATS在TowelHang、BinTowel、BagTape和LidEraser中分别进一步缩短19.8±7.0秒、23.9±5.8秒、6.0±1.7秒和12.7±2.5秒；但ToteCards的DATS时间线反而长0.8±0.7秒，TrayWipe仅短0.1±0.2秒。 | 这个诊断说明DATS是否缩短总时长取决于原始跨臂串行安排是否处于任务关键路径。前四项任务中，依赖感知重排提供了超越删空闲的压缩；后两项则表明DATS不以最短时间线为唯一目标，它可能为满足审核后的先后约束略微加长时间线。由于Gap没有用于训练，该分析不能直接给出“Gap策略与DATS策略”的性能差值。 | 第IV-C节，表III<br><span class="experiment-evidence">The duration audit shows additional compression beyond Gap for TowelHang, BinTowel, BagTape, and LidEraser. The other two tasks separate placement from episode length. ToteCards has a DATS timeline 0.8 ± 0.7 s longer than Gap because DATS enforces a checked finish-to-start relation that the raw overlap violates, yet card transfer begins 29.3 ± 5.4 s earlier. In TrayWipe, the paired duration difference is 0.1 ± 0.2 s, while towel preparation and wiping begin 22.5 ± 2.3 s and 15.1 ± 1.4 s earlier.</span> |
| ToteCards与TrayWipe中的近等时长对照，用于隔离目标窗口组成变化 | ToteCards在Raw和Gap下共同窗口覆盖率均为0.0±0.0%，DATS达到94.0±16.4%，尽管DATS时间线比Gap略长；TrayWipe的时长差仅0.1±0.2秒，但覆盖率由Raw和Gap的9.5±1.8%提高到DATS的71.2±10.6%。 | 这是最关键的机制消融式证据：即使总监督时长几乎不变或略有增加，DATS仍可让原先相隔较远的兼容跨臂片段进入同一2秒预测窗口。因此覆盖提升不是时长压缩的机械结果，而是依赖感知片段放置造成的监督重组。不过这仍是离线指标分析，并未单独训练“仅改变覆盖、不改变时长”的严格受控策略。 | 第IV-C节，表III、表IV<br><span class="experiment-evidence">DATS places at least one pair in a common 2.0 s target window in every episode, producing 94.0 ± 16.4% coverage even though its timeline is slightly longer. TrayWipe rises from 9.5 ± 1.8% under Raw and Gap to 71.2 ± 10.6% under DATS with nearly unchanged duration.</span> |

**定性案例**

- 选定成功轨迹展示了共同的行为模式：TowelHang中取衣架与毛巾折叠、抬升重叠；TrayWipe中策略在持续稳定托盘时开始拿取毛巾；LidEraser中DATS策略在定位盒盖期间已拿到两块橡皮，而Baseline仍在等待。作者据此主张，策略学会了在保留必要支撑动作的同时提前启动独立动作流。该证据直观说明“更快”来自协调重叠而非单纯提高动作速度，但它只来自挑选的成功轨迹，不能替代全体试验的统计结果。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The contribution is a demonstration-retiming and imitation-learning system for coordinated three-arm robot policies.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`805cc41f1613406669244277d1c14952d4c805a2671543b7d971be6e2016da79`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
