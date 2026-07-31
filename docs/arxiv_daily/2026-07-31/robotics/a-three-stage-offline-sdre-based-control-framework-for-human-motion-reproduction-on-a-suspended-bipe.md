---
title: "[论文解读] A Three-Stage Offline SDRE-Based Control Framework for Human Motion Reproduction on a Suspended Bipedal Robot"
description: "[arXiv 2506.04680][机器人 / 具身智能] 本文研究如何将 Vicon 捕获的人体下肢运动离线转换为满足电机约束、能够在悬吊式双足机器人上准确且跨试次稳定复现的关节命令，从而为外骨骼人体试验前的台架测试提供可重复运动基准。"
arxiv_id: "2506.04680"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.448978+00:00"
source_sha256: "677d38c0dd2d6a417d055eee55fbb9e5c9614f53a187ad94aaae1ebef3f18e9f"
tags:
  - "机器人 / 具身智能"
  - "下肢外骨骼测试"
  - "悬吊式双足机器人"
  - "人体运动复现"
  - "状态相关黎卡提方程"
  - "梯形速度轨迹"
  - "PID-LQR补偿"
  - "离线命令生成"
  - "动作捕捉"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2506.04680</p>

# A Three-Stage Offline SDRE-Based Control Framework for Human Motion Reproduction on a Suspended Bipedal Robot

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Huang, Ping-Kong, Lan, Chien-Wu, Wu, Chin-Tien, Lin, Ching-Kai</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Department of Applied Mathematics, National Yang Ming Chiao Tung University；Department of Electrical Engineering, National Central University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2506.04680) · [PDF 下载](https://arxiv.org/pdf/2506.04680) · **关键词** 下肢外骨骼测试, 悬吊式双足机器人, 人体运动复现, 状态相关黎卡提方程, 梯形速度轨迹, PID-LQR补偿, 离线命令生成, 动作捕捉<br>


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

本文研究如何将 Vicon 捕获的人体下肢运动离线转换为满足电机约束、能够在悬吊式双足机器人上准确且跨试次稳定复现的关节命令，从而为外骨骼人体试验前的台架测试提供可重复运动基准。

**不用术语来说**：直接让受试者测试尚未充分验证的下肢外骨骼，可能因执行器故障、关节错位或辅助方式不当而造成伤害；但人体动作捕捉系统只给出关节如何运动，并不会直接告诉机器人电机应施加多大作用或怎样在速度、加速度限制内执行。因此，需要先把人体动作转成机器人实际能够执行的命令，并保证机器人每次都尽量做出同样的动作，才能形成可信的安全测试环境。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将悬吊式双足机器人构造成外骨骼早期评估的替代运动平台：利用 Vicon 采集步行与下蹲的下肢运动，在暂不引入地面反作用力和足地碰撞的条件下，建立与平台四个驱动自由度相容的可重复关节轨迹基准。
- 作者提出三级离线命令生成架构：先以状态依赖 Riccati 方程控制根据机器人动力学估计人体参考运动对应的关节力矩需求，再通过参数化优化生成满足电机速度与加速度限制的梯形速度命令，最后利用实验跟踪数据进行 PID-LQR 加速度补偿，以缩小理论动力学需求与实际硬件执行之间的差距。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于下肢外骨骼的机器人化测试与运动复现研究。外骨骼在机械故障、关节错位或助力不当时可能使受试者承受伤害、 discomfort 或寄生载荷，因此早期评估需要用可控、可重复的机器人平台替代真人。此类平台的核心问题不是简单回放动作捕捉得到的关节角，而是把仅含运动学信息的人体轨迹转换为符合机器人动力学、机械结构以及电机速度和加速度限制的可执行命令。本文采用悬吊式双足机器人，使系统不受连续地面反作用力与落地冲击影响，从而先隔离并研究四个驱动自由度上的关节运动复现，为以后引入人机耦合和接触动力学提供标准化基线。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**状态相关黎卡提方程控制（SDRE）**

SDRE把非线性系统改写为系数随当前状态变化的形式，并在各状态处求解黎卡提方程，从而得到状态相关的反馈控制律。本文利用它沿人体参考轨迹估计机器人完成该运动所需的次优关节力矩，而不是直接把关节角当作电机命令。

</div>
<div class="concept-item" markdown="1">

**梯形速度轨迹**

梯形速度轨迹通常由加速、匀速和减速阶段组成，可用少量参数表示，并能显式限制最大速度与加速度。本文用参数化优化将理论力矩需求映射为电机可执行的关节角速度命令。

</div>
<div class="concept-item" markdown="1">

**PID-LQR补偿**

PID根据跟踪误差的比例、积分和微分信息进行修正，LQR则通过带权二次代价在误差抑制与控制代价之间折中。本文将二者结合为离线加速度补偿器，利用既有实验跟踪数据修正下一版命令，而不在每次试验中依赖可能含延迟、噪声和同步误差的实时反馈。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是由Vicon光学动作捕捉系统记录的步行与深蹲下肢关节运动学轨迹；该数据不包含连续地面反作用力信息。执行对象是完全悬吊、同样不受地面反作用力影响的双足机器人，其任务范围限定为与平台四个驱动自由度兼容的关节运动。系统首先依据机器人动力学计算与目标轨迹对应的关节力矩需求，再在电机速度和加速度约束下生成梯形角速度命令，最后依据实验跟踪误差离线补偿命令。输出是可由电机执行且能在多次试验中稳定复现目标关节角与模型力矩需求的命令序列；本文不直接评估外骨骼与人体之间的相互作用，也暂不处理足地接触、地面冲击或复杂人机耦合。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$q(t)$**

时刻 $t$ 的机器人关节角向量；本文关注与四个驱动自由度对应的关节运动。

</div>
<div class="notation-item" markdown="1">

**$\dot{q}(t)$**

时刻 $t$ 的关节角速度向量，也是参数化梯形命令所处的主要执行空间。

</div>
<div class="notation-item" markdown="1">

**$\tau(t)$**

机器人沿参考运动所需的关节力矩向量，由动力学模型和SDRE阶段建立其参考需求。

</div>
<div class="notation-item" markdown="1">

**$r(t)$**

由Vicon人体动作数据构成的目标关节运动轨迹。

</div>

</div>

**直接相关的工作**

- **文献[24]：悬吊式双足机器人的关节状态约束轨迹跟踪研究**: 该工作表明悬吊配置可用于受控关节运动，并为在关节状态限制下生成轨迹提供直接基础。本文沿用相近思路，但将重点扩展为由SDRE力矩参考到受电机约束的速度、加速度命令的系统级离线转换，并在引入地面接触和外骨骼耦合前强调重复运动复现。
- **文献[19]：状态相关黎卡提方程控制方法**: 该方法提供本文第一阶段的控制基础，即把非线性动力学写成状态相关系数形式并求取状态相关反馈律。本文用它沿捕获的人体运动轨迹生成描述动态需求的次优关节力矩基线，随后再解决理论力矩无法被实际电机精确实现的问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

下肢外骨骼的早期测试同时面临安全性与可重复性要求。若直接使用人体受试者，机械故障、动作复现不一致、外骨骼与人体关节轴线错位以及受约束的膝关节机构都可能引起伤害、不适或额外寄生载荷，对身体障碍者尤其不适合。机器人台架可以隔离人体风险，但要成为标准化测试工具，它必须把真实人体动作稳定地复现到机器人关节上，并使不同试次具有可比较的执行条件。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **替代人体的机器人测试平台**：已有研究使用专用力矩测量装置、人工腿或下肢模拟器，以及结合仿真和人体运动模型的人形机器人框架，在不让受试者直接承担早期风险的情况下测试外骨骼。这类平台能够提供可测量、可重复的运动条件；悬吊式双足机器人还可先隔离足地接触及地面反作用力，使研究集中于关节轨迹复现。
- **模型控制与受约束轨迹生成**：非线性模型控制及 LQR 派生方法利用机器人动力学计算稳定或跟踪所需的控制作用，其中状态依赖 Riccati 方程方法把非线性系统写成随状态变化的系数形式，并沿参考轨迹求取次优反馈和力矩需求；梯形速度或优化加速度轨迹则通过有限参数描述电机运动，以满足速度、加速度等硬件边界。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 动作捕捉得到的是关节角等运动学参考，而机器人执行还取决于机构质量、动力学、执行器性能和机械约束；因此，直接把捕获轨迹当作电机命令，不能保证其在具体平台上具有正确的动力学需求或硬件可执行性。
- 模型计算得到的次优理论力矩无法由真实电机精确产生，原因包括力矩饱和及运行限制；另一方面，若在每次试验中依赖存在延迟、噪声和同步误差的实时传感反馈更新命令，不确定测量可能使各次运动发生变化，从而破坏标准化台架所要求的跨试次一致性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作分别证明了机器人替代测试、悬吊条件下的受限关节跟踪、模型控制和参数化轨迹生成的可行性，但尚缺少一个面向具体悬吊式双足硬件的统一命令生成流程：它需要从仅含运动学信息的人体动作出发，先补足动力学力矩需求，再把该需求映射为满足电机速度与加速度限制的命令，并利用实际跟踪误差进行校正，同时维持固定命令带来的跨试次可重复性。

</div>
<div markdown="1"><span>核心问题</span>

能否构造一种三级离线控制方法，将 Vicon 捕获的步行和下蹲关节轨迹转换为悬吊式双足机器人可执行的电机命令，使机器人在满足执行器约束的前提下准确复现关节角及相应的模型力矩，并比 MPC 与 IPSO-PID 基线获得更小的跟踪误差和试次间波动？

</div>
<div markdown="1"><span>作者直觉</span>

该切入点把一个难以一次解决的转换问题拆成三个职责明确的环节：动力学模型先回答“完成该人体动作需要怎样的关节力矩”，参数化优化再回答“电机在速度和加速度边界内应怎样运动”，实验补偿最后修正模型与真实硬件之间的系统性偏差。将补偿结果离线固化为后续试次使用的命令，还可避免实时噪声和时延在每次运行中引入不同扰动；悬吊设置则暂时移除复杂的足地冲击，使关节复现能力能够被单独、稳定地检验。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法不是直接在线控制人体或外骨骼，而是为悬吊式双足机器人离线生成一套可重复执行的电机命令。输入是 Vicon 采集的人体下肢期望运动，核心处理依次为：用状态依赖 Riccati 方程控制（SDRE）和单腿动力学求出与期望运动相匹配的理论关节力矩；把理论力矩转换为满足伺服电机速度、加速度及命令时序约束的分段线性速度命令；再根据机器人实测跟踪误差，通过离线 PID-LQR 进行加速度补偿。最终输出左右腿髋、膝关节的目标角度、轮廓速度、轮廓加速度及命令更新时间序列，并由电机控制板执行。

技术上，第一阶段提供动力学意义上的“理想力矩基准”，第二阶段解决理想力矩不能直接发送给位置/速度型伺服电机的问题，第三阶段则补偿模型与真实硬件之间的摩擦、饱和和命令延迟等差异。通俗地说，该框架先计算机器人理论上应当怎样用力，再把这种用力方式翻译成电机听得懂且做得到的命令，最后通过一次或多次实验反馈修正命令，使真实运动更接近期望人体动作。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段一：SDRE 理论力矩生成

将单腿动力学写成状态依赖系数形式，并在各状态点求解代数 Riccati 方程，得到反馈律 $\bm{u}(t)=-\bm{R}^{-1}\bm{B}(\bm{x}(t))^T\bm{P}(\bm{x}(t))\bm{x}(t)$。该反馈律在状态误差与控制耗能之间进行二次型权衡，并产生髋、膝关节的 SDRE 参考力矩。

<div class="method-step__io" markdown="1">

**输入**：Vicon 记录并转换得到的期望下肢关节运动，以及论文建立的单腿非线性动力学模型；控制状态为相对期望轨迹定义的状态或状态误差 $\bm{x}(t)$。<br>
**输出**：左右腿各自的期望关节状态轨迹与 SDRE 理论参考力矩 $\bm{\tau}_{\kappa}(t)$，其中 $\kappa\in\{L,R\}$。

</div>

**直观理解**：这一阶段相当于先在动力学模型中计算“为了复现这段人体动作，机器人每一时刻理想上应施加多大力矩”。它给后续命令生成提供目标，但其结果尚未考虑真实电机能否直接实现。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段二：执行器约束下的参数化命令优化

以命令更新时间 $\bm{\xi}_{\kappa}$、髋膝关节轮廓速度 $\bm{\omega}_{\kappa}$ 和轮廓加速度 $\bm{\alpha}_{\kappa}$ 为决策变量，构造速度连续的分段线性速度轨迹，并积分得到角度轨迹；随后通过单腿动力学计算该命令诱导的估计力矩 $\tilde{\bm{\tau}}_{\kappa}(t)$，最小化其与 SDRE 力矩之间的加权均方根误差。

<div class="method-step__io" markdown="1">

**输入**：阶段一得到的 SDRE 参考力矩 $\bm{\tau}_{\kappa}(t)$、期望关节角，以及伺服电机允许的轮廓速度和轮廓加速度范围。<br>
**输出**：每个关节的命令序列 $C_{\ell,\kappa}=(\bm{\theta}_{\ell,\kappa}^{*},\bm{\omega}_{\ell,\kappa}^{*},\bm{\alpha}_{\ell,\kappa}^{*})$，其中 $\ell\in\{H,K\}$ 表示髋或膝，且同一条腿的髋、膝命令共享优化后的更新时间。

</div>

**直观理解**：这一阶段把连续、理想化的力矩目标压缩成少量电机参数，并允许优化器决定何时更新命令。它类似于在电机的速度和加速度上限内，寻找一组最接近理想用力过程的可执行动作指令。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段三：基于实测误差的离线加速度补偿

先执行初始命令并比较期望轨迹与实验轨迹；作者观察到初始命令存在明显的加速度不足，因此采用离线 PID-LQR 计算加速度补偿并据此修正命令轮廓。所给节选在初步跟踪分析处截断，未包含 PID-LQR 的完整状态定义、增益求解公式和命令迭代终止条件。

<div class="method-step__io" markdown="1">

**输入**：阶段二生成的初始电机命令、机器人实际执行后反馈的关节角 $\theta^m(t)$ 及其数值微分速度 $\dot{\theta}^m(t)$，以及期望角度和速度。<br>
**输出**：经实验反馈细化的关节轮廓加速度及相应统一命令集，用于机器人后续重复执行目标人体动作。

</div>

**直观理解**：动力学模型无法准确描述摩擦、饱和和通信或执行延迟，所以模型中可行的命令在实机上仍可能动作偏慢。该阶段把第一次执行暴露出的误差转化为额外加速度修正，相当于根据实机表现进行离线校准。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### SDRE 代数 Riccati 方程与反馈控制律

$$
\bm{P}(\bm{x})\bm{A}(\bm{x})+\bm{A}(\bm{x})^{T}\bm{P}(\bm{x})-\bm{P}(\bm{x})\bm{B}(\bm{x})\bm{R}^{-1}\bm{B}(\bm{x})^{T}\bm{P}(\bm{x})+\bm{Q}=0,\qquad \bm{u}(t)=-\bm{R}^{-1}\bm{B}(\bm{x}(t))^{T}\bm{P}(\bm{x}(t))\bm{x}(t)
$$

**符号说明**

- $\bm{x}(t)$：时刻 $t$ 的系统状态或相对目标运动定义的状态误差向量。
- $\bm{A}(\bm{x})$：随状态变化的系统矩阵，用于描述无控制输入时的状态演化。
- $\bm{B}(\bm{x})$：随状态变化的输入矩阵，描述控制力矩如何影响状态。
- $\bm{Q}$：对状态误差进行加权的对称半正定矩阵；本文将其视为常矩阵。
- $\bm{R}$：对控制输入进行加权的对称正定矩阵；本文将其视为常矩阵。
- $\bm{P}(\bm{x})$：Riccati 方程的状态依赖正定或半正定解，用于形成反馈增益。
- $\bm{u}(t)$：SDRE 计算得到的控制输入，在本文中对应模型生成的关节力矩参考。

<div class="equation-explanation" markdown="1">

**直观理解**：Riccati 方程把“尽快减小运动误差”和“不要使用过大控制力矩”合并成一个局部最优反馈规则。机器人姿态改变时，动力学矩阵及反馈增益也随之改变，因此得到沿整条目标运动变化的理论力矩轨迹；该轨迹是第二阶段的拟合目标，而不是直接发送给伺服电机的命令。<br>
**原文位置**：第 III-A 节，式（18）和式（19）；对应二次代价见式（17）

</div>

</div>

<div class="equation-block" markdown="1">

#### 执行器可行命令的力矩匹配优化

$$
(\bm{\omega}_{\kappa}^{*},\bm{\alpha}_{\kappa}^{*},\bm{\xi}_{\kappa}^{*})=\underset{\bm{\omega}_{\kappa},\bm{\alpha}_{\kappa},\bm{\xi}_{\kappa}}{\operatorname{arg\,min}}\;J_{\kappa},\qquad J_{\kappa}=\left(\frac{1}{T}\int_{0}^{T}\bm{e}_{\kappa}(t)^{T}\bm{W}\bm{e}_{\kappa}(t)\,dt\right)^{1/2},\qquad \bm{e}_{\kappa}(t)=\bm{\tau}_{\kappa}(t)-\tilde{\bm{\tau}}_{\kappa}(t;\bm{\omega}_{\kappa},\bm{\alpha}_{\kappa},\bm{\xi}_{\kappa})
$$

**符号说明**

- $\kappa$：腿的索引，取 $L$ 或 $R$，分别表示左腿和右腿。
- $\bm{\omega}_{\kappa}$：该腿髋、膝关节各命令段的目标轮廓速度参数。
- $\bm{\alpha}_{\kappa}$：该腿髋、膝关节各命令段的轮廓加速度参数。
- $\bm{\xi}_{\kappa}$：该腿的命令更新时间向量，各时刻严格递增并位于运动区间内。
- $T$：待复现动作的总持续时间。
- $\bm{\tau}_{\kappa}(t)$：阶段一生成的 SDRE 关节力矩参考向量。
- $\tilde{\bm{\tau}}_{\kappa}(t;\bm{\omega}_{\kappa},\bm{\alpha}_{\kappa},\bm{\xi}_{\kappa})$：由参数化角度和速度轨迹代入单腿动力学后计算的估计力矩。
- $\bm{e}_{\kappa}(t)$：SDRE 参考力矩与参数化命令所诱导力矩之间的误差。
- $\bm{W}$：维度为 $2\times2$ 的对角权重矩阵，用于调整髋、膝力矩误差的重要性。

<div class="equation-explanation" markdown="1">

**直观理解**：优化器搜索每段命令的速度、加速度和发送时刻，使电机命令在动力学模型中产生的力矩尽量接近 SDRE 理想力矩，同时满足速度上下界、加速度上下界和命令时间顺序约束。其关键不是直接最小化角度误差，而是在把命令角度固定到相应期望轨迹采样值的基础上，用力矩误差评价不同可执行速度轮廓的动力学一致性。<br>
**原文位置**：第 III-B 节，式（34）至式（36）；速度、加速度和更新时间约束见式（35）及其后续约束

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该方法不涉及机器学习训练。其核心离线目标分为两层：SDRE 通过式（17）的无限时域二次代价权衡状态误差与控制输入，得到理论力矩参考；随后参数化优化通过式（36）最小化 SDRE 力矩 $\bm{\tau}_{\kappa}(t)$ 与可执行命令所诱导力矩 $\tilde{\bm{\tau}}_{\kappa}(t)$ 的加权均方根差。第三阶段再以实机跟踪误差为依据修正加速度，但当前节选未给出 PID-LQR 补偿的完整目标函数，因此不能把它表述为已明确报告的第三个优化目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. SDRE 非线性状态反馈模块**

该模块将非线性单腿模型表示为状态依赖矩阵 $\bm{A}(\bm{x})$ 和 $\bm{B}(\bm{x})$，在质量矩阵 $\bm{M}(\theta)$ 非奇异的运动范围内求解状态相关代数 Riccati 方程。论文利用 Hautus 条件说明 $\left(\bm{A},\bm{B}\right)$ 可稳定化，并因输出矩阵 $\bm{C}=\bm{I}_5$ 而得到 $\left(\bm{A},\bm{C}\right)$ 可检测，从而支持 Riccati 解的存在性和闭环误差渐近稳定性。

> 直观理解：普通 LQR 主要针对固定线性模型，而这里机器人的动力学会随关节姿态变化；SDRE 在不同状态处更新等效线性模型和反馈增益。稳定化与可检测性验证的作用，是排除控制器在相关运动范围内无法求解或无法压低误差的基本理论问题。

**2. 可变更新时间的分段线性速度参数化模块**

第 $k$ 段从初速度 $\omega_0^k$ 以加速度 $\alpha^k$ 向目标轮廓速度 $\omega^k$ 变化，到达时间由 $\xi_1^k=\xi_0^k+(\omega^k-\omega_0^k)/\alpha^k$ 隐式确定；若下一命令提前到达，则当前梯形轮廓可以在完成前被覆盖，并继承上一段末速度以保持速度连续。命令更新时间 $\xi_0^k$ 也参与优化，因此各段可以只含加速过程、包含恒速过程，或在条件允许时形成完整梯形速度轮廓。

> 直观理解：固定时长的完整梯形速度曲线难以跟随复杂人体动作，因此论文不仅调节“跑多快、加速多快”，还调节“什么时候发送下一条命令”。利用电机支持中途覆盖命令且保持速度连续的特性，可以用较少参数表达更灵活的运动。

**3. 离线 PID-LQR 实机补偿模块**

该模块以初始命令的实机跟踪结果为反馈，针对期望与实测角度、速度之间的偏差生成加速度补偿；其目标是处理动力学建模误差、关节摩擦、执行器饱和、命令切换延迟和命令结构限制。节选仅明确该补偿由 PID-LQR 计算，未给出完整控制增益、代价矩阵或更新方程，因而不能从当前材料进一步还原其算法细节。

> 直观理解：前两个模块解决“模型上正确”和“电机规格允许”，但不能保证真实硬件完全照做。补偿模块使用真实执行数据纠正这种差距，不过它仍是离线命令细化，而不是机器人运行时实时改变目标动作。

**训练与推理**

“训练/推理”对本文并不适用，更准确的划分是离线设计与在线回放。离线阶段先从人体动作得到期望关节轨迹，基于单腿模型逐状态求解 SDRE 并生成参考力矩；然后分别对左、右腿优化共享于髋膝关节的更新时间，以及各关节的轮廓速度和加速度；优化后在对应更新时间采样期望角度，形成 $C_{\ell,\kappa}$，再把两腿命令按时间拼接。之后执行一次初始实机跟踪试验，读取电机角度反馈并数值求导得到速度，利用离线 PID-LQR 生成加速度补偿，最终获得细化命令。实际运行时，电机控制板只需按统一时间轴回放这些目标角度、轮廓速度和轮廓加速度；框架的主要计算和实验校准均已在运行前完成。

**复现信息**

优化使用 MATLAB 的 `fmincon`。轮廓速度与加速度的初值从 SDRE 状态轨迹均匀采样，初始命令更新时间按 $0.25\,\mathrm{s}$ 间隔均匀设置；作者说明该间隔用于在时间分辨率与过密分段导致的收敛失败之间折中。速度参数受 $\omega_{\min}\leq\omega_{\ell\kappa}^{k}\leq\omega_{\max}$ 约束，加速度参数受 $\alpha_{\min}\leq\alpha_{\ell\kappa}^{k}\leq\alpha_{\max}$ 约束，内部更新时间必须严格递增且落在 $(0,T)$ 内。参数化依据 PH54-200-S500-R 执行器支持对未完成轮廓进行命令覆盖并保持速度连续的特性；同一条腿的髋、膝共享更新时间，但速度和加速度分别优化。SDRE 的理论保证限定在质量矩阵 $\bm{M}(\theta)$ 非奇异的运动范围内。当前节选未报告电机速度与加速度界的具体数值、`fmincon` 选项、SDRE 权重 $\bm{Q}$、$\bm{R}$、力矩权重 $\bm{W}$，以及 PID-LQR 的状态、增益和迭代流程，这些信息需要回查论文其余章节或补充材料后才能完整复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 人体行走动作：参考轨迹由Vicon动作捕捉系统获得，再将人体下肢骨架简化为包含六个离散关节的SLLM，并把每条腿投影到参考运动平面以滤除平面外噪声；投影后计算的髋、膝关节角作为机器人目标轨迹。原文未明确报告受试者数量、动作序列数量、时长或训练/测试划分；其作用是检验周期性步态的跟踪与重复性。
- 人体下蹲动作：采用与行走相同的Vicon、SLLM简化及平面投影流程生成髋膝参考轨迹。原文未明确报告受试者数量、动作序列数量、时长或训练/测试划分；其作用是检验不同于行走的双腿协同屈伸运动，避免结论仅建立在单一动作类型上。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**平均均方根误差 $\overline{\mathrm{RMSE}}$**

先计算每次试验中执行关节角与目标关节角在全部 $N$ 个时间采样点上的RMSE，再对 $M=10$ 次试验取平均；衡量典型试次的整体轨迹偏差。 （越低越好，因为数值越小表示复现轨迹总体上越接近参考轨迹。）

</div>
<div class="metric-item" markdown="1">

**最大试次均方根误差 $\mathrm{RMSE}_{\max}$**

在 $M=10$ 次重复执行中取最大的单次RMSE，用于衡量最差试次的跟踪精度；关节角以度为单位，模型计算力矩以Nm为单位。 （越低越好，因为它反映重复实验中最不利一次的偏差上界。）

</div>
<div class="metric-item" markdown="1">

**试次RMSE标准差 $\mathrm{STD}$**

计算 $M=10$ 个单次RMSE相对其平均值的标准差，衡量相同命令重复执行时误差是否稳定，而不是衡量单条轨迹内部的瞬时波动。 （越低越好，因为更小的跨试次离散程度表示更高的执行重复性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 本文方法在行走与下蹲任务上的绝对关节角跟踪精度和重复性

<div class="result-value" markdown="1">

八个“动作－侧别－关节”设置的 $\overline{\mathrm{RMSE}}$ 均低于 $3^\circ$：行走为 $0.8257^\circ$ 至 $2.3186^\circ$，下蹲为 $1.0472^\circ$ 至 $2.5507^\circ$。十次试验中的 $\mathrm{RMSE}_{\max}$ 为 $0.9650^\circ$ 至 $2.6428^\circ$，RMSE的 $\mathrm{STD}$ 为 $0.0346^\circ$ 至 $0.1454^\circ$。

</div>

这说明固定离线命令在两类动作和四个髋膝关节上都能把典型误差控制在几度以内，并且十次重复执行的误差变化很小。不过，这些结果只覆盖悬吊平台、给定参考轨迹和十次重复，不能证明机器人面对外部扰动、不同人体、未见动作或地面接触变化时仍有相同精度。

<div class="result-source" markdown="1">

来源：Section IV-C；具体逐关节数值见Table II，最大RMSE与STD见Table III

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The results in Table II report RMSE values of 0.8°–2.3° for walking and 1.0°–2.6° for squatting.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 关节角比较：本文方法对比MPC与IPSO-PID，覆盖行走、下蹲、左右髋膝关节

<div class="result-value" markdown="1">

在全部八个设置中，本文方法同时取得最低的角度 $\mathrm{RMSE}_{\max}$ 和最低的角度 $\mathrm{STD}$。作者汇总称，相对MPC，所有设置的 $\mathrm{RMSE}_{\max}$ 至少降低 $46.3\%$、$\mathrm{STD}$ 至少降低 $75.0\%$；相对IPSO-PID则至少降低 $20.6\%$ 和 $69.1\%$。例如行走左膝的 $\mathrm{RMSE}_{\max}$ 为 $2.2518^\circ$，而MPC和IPSO-PID分别为 $12.9637^\circ$、$8.8037^\circ$。

</div>

比较结果支持本文方法在该平台上兼具更好的最差试次精度与跨试次一致性，而且优势并非只出现在某个关节或动作。由于对照的是完整控制器，实验不能单独判断优势来自SDRE、执行器约束参数化，还是PID-LQR补偿；此外，离线方法与在线基线的目标和扰动响应能力并不完全相同。

<div class="result-source" markdown="1">

来源：Section IV-C，Table IV；轨迹对比见Figure 10

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In terms of maximum RMSE for repeated trials, the proposed framework reduces RMSEmax by at least 46.3% relative to MPC and 20.6% relative to IPSO-PID for all joints and motion tasks reported.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 模型计算关节力矩比较：本文方法对比MPC与IPSO-PID

<div class="result-value" markdown="1">

在全部八个设置中，本文方法的模型力矩 $\mathrm{RMSE}_{\max}$ 与 $\mathrm{STD}$ 均最低。作者报告，相对MPC，力矩 $\mathrm{RMSE}_{\max}$ 至少降低 $39.2\%$、$\mathrm{STD}$ 至少降低 $75.7\%$；相对IPSO-PID则至少降低 $11.3\%$ 和 $65.9\%$。本文方法各设置的力矩 $\mathrm{RMSE}_{\max}$ 为 $0.1431$ 至 $0.3108$ Nm，$\mathrm{STD}$ 为 $0.0037$ 至 $0.0128$ Nm。

</div>

在统一动力学模型下，本文方法复现出的运动更接近参考运动对应的力矩变化模式，因此不仅角度相似，模型推断的动力学需求也更相似。但这些力矩由运动学轨迹代入模型计算，并非执行器力矩传感器的直接测量；结果会受到模型参数、速度估计和加速度估计误差影响，不能等同于证明真实输出力矩具有同样误差。

<div class="result-source" markdown="1">

来源：Section IV-C，Table V；力矩轨迹见Figure 11

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table V, the proposed method reduces the torque RMSEmax by at least 39.2% relative to MPC and 11.3% relative to IPSO-PID.

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

- MPC：通过二次规划计算控制输入，是有模型、在线滚动优化控制器的代表。它与本文基于动力学模型但离线固定命令的方案形成直接对照，用于判断实时反馈与在线求解是否有利于该平台所强调的重复再现任务。
- IPSO-PID：使用改进粒子群优化策略自适应整定PID参数，是数据驱动参数搜索与经典反馈控制结合的代表。它用于判断本文优势是否只是来自更好的PID参数整定，还是来自SDRE力矩生成、执行器约束优化和离线PID-LQR补偿组成的完整流程。

**实验想回答的问题**

- 在相同悬吊式双足机器人硬件上，三阶段离线控制框架能否以较低的关节角跟踪误差和较小的跨试次波动，重复再现人体行走与下蹲轨迹？
- 与在线模型预测控制（MPC）和经改进粒子群优化整定的PID（IPSO-PID）相比，该方法是否能更准确地保持参考运动对应的模型计算关节力矩模式？

**实验实现**

三种方法在同一硬件和实验条件下执行相同的行走、下蹲参考轨迹，每种设置重复 $M=10$ 次。平台采用Robotis PH54-200-S500-R执行器、3D打印轻量结构、C#控制程序和USB连接的U2D2接口；SDRE与参数化优化在MATLAB R2020b中实现。本文方法先以SDRE生成参考力矩，再在速度 $\pm50^\circ/\mathrm{s}$、加速度 $\pm1000^\circ/\mathrm{s}^2$、髋关节 $[-50^\circ,50^\circ]$ 和膝关节 $[-20^\circ,75^\circ]$ 的约束下生成命令，最后依据首次执行反馈通过离线PID-LQR计算加速度缩放并重新执行。关节角直接来自实验反馈；力矩并非传感器实测，而是把各方法产生的角度、角速度和角加速度代入同一机器人动力学关系得到。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Figure 9以红线表示SLLM参考角度、蓝线表示机器人复现角度，并用十次试验逐时刻最大值与最小值之间的蓝色阴影表示重复范围。作者将狭窄包络解释为高重复性；该图直观展示误差在动作周期中的分布，但阴影只是极值范围，且原文未提供逐时刻置信区间，定量判断仍应以Table II至V为准。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper proposes a control and command-generation framework for repeatable human-motion reproduction on a bipedal robotic platform.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`677d38c0dd2d6a417d055eee55fbb9e5c9614f53a187ad94aaae1ebef3f18e9f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
