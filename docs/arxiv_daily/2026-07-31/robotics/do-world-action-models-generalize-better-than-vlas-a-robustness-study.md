---
title: "[论文解读] Do World Action Models Generalize Better than VLAs? A Robustness Study"
description: "[arXiv 2603.22078][机器人 / 具身智能] 本文通过在单臂与双臂操作基准中施加视觉和语言扰动，系统比较世界动作模型（WAM）与视觉—语言—动作模型（VLA）的鲁棒性、训练依赖和推理代价，以检验显式预测未来状态是否真正带来更好的泛化。"
arxiv_id: "2603.22078"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.575476+00:00"
source_sha256: "c12dd985e4412cba5e951f893490f96e23d7d253b8c68fb7c76ba3fd5d920aac"
tags:
  - "机器人 / 具身智能"
  - "多模态 VLM"
  - "机器人操作"
  - "视觉—语言—动作模型"
  - "世界动作模型"
  - "世界模型"
  - "分布外泛化"
  - "上下文扰动"
  - "鲁棒性"
  - "视频预训练"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2603.22078</p>

# Do World Action Models Generalize Better than VLAs? A Robustness Study

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Zhang, Zhanguang, Li, Zhiyuan, Rahmati, Behnam, Yang, Rui Heng, Ma, Yintao, Rasouli, Amir, Pakdamansavoji, Sajjad, Wu, Yangzheng, Zhang, Lingfeng, Cao, Tongtong, Wen, Feng, Wang, Xinyu, Quan, Xingyue, Zhang, Yingxue</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Huawei Technologies Canada；University of Toronto</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2603.22078) · [PDF 下载](https://arxiv.org/pdf/2603.22078) · **关键词** 机器人操作, 视觉—语言—动作模型, 世界动作模型, 世界模型, 分布外泛化, 上下文扰动, 鲁棒性, 视频预训练<br>
**代码**: [https://robot-robustness.github.io/RoboTwin2.0-Plus/](https://robot-robustness.github.io/RoboTwin2.0-Plus/)

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

本文通过在单臂与双臂操作基准中施加视觉和语言扰动，系统比较世界动作模型（WAM）与视觉—语言—动作模型（VLA）的鲁棒性、训练依赖和推理代价，以检验显式预测未来状态是否真正带来更好的泛化。

**不用术语来说**：机器人在训练时见过的场景中完成任务，并不意味着它能在光照改变、背景杂乱、物体布局变化或指令措辞不同后继续可靠工作。本文要弄清楚：相比主要依据当前图像和语言直接生成动作的模型，先学习环境如何随动作演化、再据此控制机器人的模型，是否更能抵抗这些变化，以及这种优势需要付出什么代价。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 建立面向鲁棒性的对照评测：使用含七类扰动的单臂操作基准 LIBERO-Plus，以及采用相似扰动协议构建的双臂 Aloha-Agilex 基准 RoboTwin 2.0-Plus，在不同机器人形态和上下文变化下比较代表性 VLA、WAM及混合方法。
- 将比较从成功率扩展到机制与代价：研究发现WAM通常对噪声、光照和布局变化表现出较强鲁棒性，但高性能VLA或混合方法也可能达到相当水平，只是往往更依赖多样化机器人数据或显式动态预测目标；同时，WAM单次推理至少比$\pi_{0.5}$慢$4.8$倍，揭示了鲁棒性、数据需求与部署效率之间的权衡。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于具身智能中的机器人操作策略研究，关注机器人如何依据视觉观测和语言指令生成连续控制动作。比较对象分为两类：视觉—语言—动作模型（VLA）通常复用大规模视觉语言基础模型，并通过动作专家将多模态表示映射为机器人动作；世界动作模型（WAM）则以大规模视频预训练的世界模型为骨干，先利用其时空表示预测或表征动作引起的未来状态，再将潜在表示解码为动作。论文并非提出新的控制模型，而是在单臂与双臂操作环境中，通过视觉和语言扰动比较两类策略的分布外泛化能力、鲁棒性及部署代价。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉—语言—动作模型（Vision-Language-Action Model, VLA）**

VLA接收相机图像与自然语言任务指令，利用视觉语言基础模型理解场景和目标，再由动作模块输出机器人控制序列。它可能从训练数据中隐式学到物理规律，但通常没有被明确要求预测执行动作后的未来场景。

</div>
<div class="concept-item" markdown="1">

**世界动作模型（World Action Model, WAM）**

WAM建立在能够预测未来视觉状态的世界模型之上，并将其潜在时空表示进一步解码成机器人动作。通俗地说，它不仅判断“现在看到什么、应该做什么”，还借助视频预训练知识表征“做完后场景可能怎样变化”。

</div>
<div class="concept-item" markdown="1">

**上下文扰动与鲁棒性**

上下文扰动是任务目标基本不变时，对视觉噪声、光照、物体布局或语言表达等输入条件所作的改变；鲁棒性表示策略在这些变化下仍能完成任务的能力。该设置用于检验模型是否真正掌握可迁移的任务与动力学规律，而非依赖训练环境中的表面线索。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究将若干代表性VLA、WAM及部分混合策略置于统一的机器人操作评测中。每次决策的输入包括机器人当前视觉观测、语言任务指令以及模型所需的状态信息，输出为单臂或双臂机器人的控制动作或动作序列；环境则在视觉外观、噪声、光照、布局和语言等上下文因素上施加扰动。评测分别使用LIBERO-Plus的单臂任务和基于Aloha-Agilex平台的RoboTwin 2.0-Plus双臂任务，核心问题是在任务语义保持不变但输入分布发生变化时，WAM是否比VLA具有更稳定的任务成功表现。比较需要同时考虑模型设计和训练条件：WAM可能继承网页规模视频预训练得到的时空先验，经典VLA可能依赖规模更大且更多样的机器人数据，而混合方法还可能加入显式动态预测目标。因此，观察到的鲁棒性差异不能简单归因于模型类别，还需结合视频先验的整合方式、具身预训练数据多样性与推理延迟解释。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\pi$**

机器人策略，即从当前观测和任务条件映射到控制动作或动作序列的函数。

</div>
<div class="notation-item" markdown="1">

**$\pi_{0.5}$**

论文纳入比较的代表性经典VLA策略；下标是模型名称的一部分。

</div>

</div>

**直接相关的工作**

- **LIBERO-Plus**: 本文采用的增强型单臂操作基准；它向LIBERO任务引入七类扰动，用于比较不同策略面对上下文变化时的鲁棒性。
- **RoboTwin 2.0**: 本文内部构建的RoboTwin 2.0-Plus以该双臂操作基准及其Aloha-Agilex设置为基础，并采用与LIBERO-Plus相近的扰动协议，以检验结论能否从单臂场景延伸到双臂场景。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

真实环境具有训练集无法穷尽的不确定性，例如传感噪声、照明改变、杂乱干扰、物体布局变化和语言表达变化。机器人策略不仅要识别当前状态，还要预判动作会怎样改变环境；如果策略只在训练分布内有效，轻微上下文扰动就可能导致连续规划失误，使其难以安全、稳定地部署到真实机器人。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **视觉—语言—动作模型（VLA）**：VLA复用在大规模图像与文本上预训练的基础模型，以视觉观测和语言指令为条件，再通过动作专家等模块直接生成机器人动作。它们在导航、操作和运动控制任务上表现突出，也可能隐式学到部分物理规律，但其泛化通常受机器人训练数据的覆盖范围以及预训练目标设计影响。
- **世界动作模型（WAM）及世界模型混合方案**：世界模型先从大规模视频中学习状态随时间变化的时空规律。混合方案把这种能力用作辅助训练目标、规划模块或动作策略的引导；更直接的WAM则预测未来视觉状态，并将内部潜在表示解码为动作。直观上，它不是只问“现在该做什么”，而是先估计“做下去世界会变成什么样”，再据此控制机器人。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 经典VLA对未见场景、干扰物和杂乱环境的泛化与鲁棒性有限；即使$\pi_{0.5}$等模型在部分任务上能达到较强鲁棒性，也往往需要经过精心整理且高度多样的机器人数据、复合学习目标或具身预训练，因此尚不清楚性能来自模型范式本身，还是来自更重的数据与训练配方。
- WAM虽可能继承视频预训练中的时空先验，但其优势尚缺少统一、公平的跨平台扰动评测，而且计算代价明显偏高。原文指出单次推理至少比$\pi_{0.5}$慢$4.8$倍；较快的联合去噪式方案仍可能在训练数据缺少多样性时出现鲁棒性骤降，限制实时控制和实际部署。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未在统一扰动协议下，跨单臂与双臂操作系统直接区分三类因素：显式未来状态预测本身带来的泛化收益、机器人训练数据多样性与动态学习目标带来的收益，以及这些收益对应的推理开销。因此，“世界模型作为控制策略”是否天然比基础模型驱动的VLA更鲁棒，仍缺乏可归因的实证答案。

</div>
<div markdown="1"><span>核心问题</span>

在视觉噪声、光照、布局及语言等上下文扰动下，WAM是否比代表性VLA更稳健；若表现更好，这一差异能否归因于世界模型骨干继承的时空先验与显式动态预测，而非额外的数据和训练目标，并且这种鲁棒性需要承担多大的训练与推理成本？

</div>
<div markdown="1"><span>作者直觉</span>

控制动作的质量取决于模型能否理解动作后的结果。网络视频包含大量物体运动、接触和场景变化，世界模型通过预测后续状态，可把这些规律压缩为对动态过程的先验；当颜色、光照或背景发生变化时，这类先验可能比表面视觉相关性更稳定。因而作者选择用受控扰动来“压力测试”不同范式：若WAM在外观变化后仍能维持动作成功，且具身训练并未使用同等规模的多样化数据，就更支持其优势来自动态预测；反之，若精心训练的VLA同样稳健，则说明显式世界模型并非获得鲁棒性的唯一途径。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出一种新的机器人策略，而是建立统一的鲁棒性比较流程，回答世界动作模型（World Action Model, WAM）是否比视觉—语言—动作模型（Vision-Language-Action, VLA）更能应对训练分布之外的上下文变化。研究以语言指令、当前视觉观测和机器人状态为策略输入，在 LIBERO-Plus 的单臂任务与 RoboTwin 2.0-Plus 的双臂 Aloha-Agilex 任务中，对代表性 VLA、融合世界模型的混合策略以及 WAM 施加视觉和语言扰动，再以任务成功情况和推理开销比较不同模型类别。这里的“鲁棒性”不是只看标准环境中的最高性能，而是考察同一控制策略在噪声、光照、场景布局和语言表达等条件变化后能否继续完成任务。

技术上，比较的关键变量是动态先验如何进入动作生成：经典 VLA 通常从预训练视觉语言模型出发，通过动作专家直接把当前观测与指令映射为动作；WAM 则复用视频世界模型学习到的时空表征，通常同时预测未来视觉状态与机器人动作，或先预测未来状态再由逆动力学模型（Inverse Dynamics Model, IDM）解码动作；VLA-JEPA、MOTUS 等混合方法则在 VLA 中加入视频动态学习。通俗地说，VLA 更像“看图听命令后直接动手”，WAM 更像“先利用视频经验想象接下来会发生什么，再决定怎样动手”；本文通过统一扰动测试判断后一种机制是否真正带来更稳定的控制，而不是仅比较各模型在原始任务上的分数。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤一：按动态建模方式选择并归类策略

作者依据动作是否直接由世界模型骨干产生、是否显式学习未来视觉状态以及动作与视频之间的条件关系对模型归类；WAM 的纳入标准是使用预训练世界模型骨干生成机器人动作，且只进行轻量或不进行架构修改。

<div class="method-step__io" markdown="1">

**输入**：具有不同预训练数据、动作解码器和动态预测目标的现有机器人策略，包括经典 VLA、VLA 与世界模型的混合方法以及 WAM。<br>
**输出**：可比较的三类策略及其训练数据、预测目标和因果结构描述。

</div>

**直观理解**：这一步先区分模型究竟靠语言视觉语义直接控制，还是利用视频预测经验控制，避免把所有带有视频模块的方法都笼统称为 WAM。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤二：在统一操作任务上进行任务特定适配

各模型按照自身范式完成任务特定微调：经典 VLA 学习从当前观测和语言到动作轨迹的映射；WAM 使用视频骨干的潜在时空特征，并通过 IDM、联合去噪或动作条件视频预测等设计学习动作。原文表明不同模型的预训练规模和任务数据量差异明显，因此该阶段并非严格控制训练数据总量的等数据比较。

<div class="method-step__io" markdown="1">

**输入**：各策略已有的通用或具身预训练参数，以及 LIBERO-Plus 或 RoboTwin 2.0-Plus 对应的任务演示轨迹。<br>
**输出**：能够在相应单臂或双臂基准中闭环执行的策略检查点。

</div>

**直观理解**：相当于让每名参赛者先用自己的既有知识和规定的任务示范熟悉赛场；但由于其先前训练经历不同，结果反映的是完整模型方案的实际鲁棒性，而非仅由架构造成的纯粹因果差异。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤三：构造标准条件与上下文扰动条件

在保持操作目标可执行的前提下改变与任务相关或无关的上下文因素；文中明确提到的维度包括噪声、光照、布局以及语言扰动，LIBERO-Plus 总计引入七类扰动，RoboTwin 2.0-Plus采用相似协议扩展双臂场景。

<div class="method-step__io" markdown="1">

**输入**：LIBERO-Plus 单臂任务、RoboTwin 2.0-Plus 双臂任务，以及各基准规定的视觉和语言扰动协议。<br>
**输出**：覆盖原始条件和分布外上下文变化的一组评测环境。

</div>

**直观理解**：不是把任务换成完全不同的问题，而是改变机器人看到或听到的呈现方式，从而检查策略是否学会了任务规律，而不是记住固定背景、固定摆放或固定措辞。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤四：闭环执行并汇总鲁棒性与效率

策略在闭环中反复读取当前状态并生成动作：VLA 通常直接输出动作块，IDM 型 WAM 先形成预测未来状态再反推动作，联合生成型 WAM 则在共享生成过程中预测动作与未来视觉状态；随后按任务是否完成汇总成功率，并比较单步推理延迟。

<div class="method-step__io" markdown="1">

**输入**：微调后的策略、当前相机观测、语言指令、机器人关节状态以及扰动后的仿真环境。<br>
**输出**：各模型在两个基准及不同扰动条件下的任务成功率、鲁棒性表现与推理成本。

</div>

**直观理解**：机器人不是只回答一次该怎么做，而是在执行过程中持续观察和纠正；因此测试同时揭示模型在干扰下能否完成任务，以及这种稳定性是否以过慢的控制速度为代价。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：本文是鲁棒性比较研究，没有提出统一的新训练损失，所给章节也未提供可适用于所有参评模型的中心优化方程，因此不应人为写出一个共同目标。被比较模型的目标可按功能概括：经典 VLA 主要优化动作预测；混合方法在动作监督之外加入未来视觉表征对齐、视频重建或动态预测；WAM 通常联合学习未来视觉状态与动作，其中 IDM 型方法从预测未来状态推断导致该状态的动作，联合去噪型方法则在同一生成过程内恢复动作和视觉模态。作者的分析重点不是证明某一损失最优，而是比较不同目标和预训练先验在上下文扰动下产生的实际后果。

需要注意，训练目标与训练数据无法完全解耦。例如，$\pi_{0.5}$ 使用多种网页、机器人及高层规划数据和多样学习目标，而部分 WAM 可主要依靠视频世界模型先验及较简单的具身适配。因而作者将 WAM 的优势解释为“动态预测能力与视频时空先验可能共同贡献”，而不是仅凭结果断言显式世界模型是唯一原因；Fast-WAM 在缺少多样训练数据时于 LIBERO-Plus 上鲁棒性显著下降，也说明联合去噪设计仍可能高度依赖数据覆盖。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 经典 VLA 的视觉语言骨干与动作专家**

经典 VLA 复用大规模视觉语言模型的语义理解与空间定位能力，再由动作专家把当前视觉观测、语言指令和机器人状态映射为连续动作或动作轨迹。其预训练主要受自回归下一词元预测等语言中心目标驱动，精细物理动态通常不是显式预测对象。

> 直观理解：该模块擅长理解“要拿哪个物体、放到哪里”，但不一定明确模拟物体在动作后如何运动；其鲁棒性往往依赖大规模、多样化机器人数据和额外训练目标。

**2. 视频世界模型骨干与时空动态先验**

WAM 从大规模视频预训练模型继承潜在时空表征，使模型能够预测未来视觉状态或在联合生成过程中表达环境演化。机器人关节状态、动作和未来图像可被编码为潜在帧，或交由独立的小型动作 Transformer 与视频流交互。

> 直观理解：视频预训练让模型见过大量“事物怎样随时间变化”的模式，即使这些视频不是机器人演示，也可能帮助它在光照、噪声或布局改变时抓住较稳定的运动规律。

**3. 动作—未来状态耦合与解码机制**

被比较的 WAM 包含不同因果设计：LingBot-VA 等 IDM 型方法让动作以预测未来视觉状态为条件；Cosmos-Policy、DreamZero 和 Fast-WAM 等可联合去噪动作与视觉模态；GigaWorld-Policy 则让未来视觉状态以动作作为条件。部分方法在测试时必须显式生成未来视觉状态，Fast-WAM 和 GigaWorld-Policy 则允许只输出动作。

> 直观理解：这些设计的差别在于模型是“先想象结果再反推动作”、让动作和结果“一起成形”，还是“先给动作再预测结果”。它直接影响对训练数据多样性的依赖、动态一致性以及推理速度，也是本文解释鲁棒性差异的核心维度。

**训练与推理**

训练方面，各参评模型保留原有训练范式，整体可分为世界模型或视觉语言基础预训练、具身预训练或后训练、任务特定微调三个层次。表 2 显示这些层次并不对所有模型同时存在：例如 $\pi_0$、OpenVLA-OFT 和 X-VLA 依赖不同规模的跨具身机器人数据；$\pi_{0.5}$ 还结合网页视觉问答、描述、定位、高层规划和移动操作数据；LingBot-VA 使用大规模跨具身具身预训练；Cosmos-Policy 与 Fast-WAM 则未列出额外具身预训练，只使用任务轨迹完成适配。因此，本文评测的是现实可获得模型在各自完整训练配方下的表现，同时借助训练数据表解释鲁棒性来源，不能视为在完全相同数据预算下的架构消融。

推理方面，所有策略接收语言指令、当前视觉观测及所需机器人状态，并在环境反馈下闭环输出动作。经典 VLA 通常由动作专家直接生成动作；LingBot-VA、DreamZero 等可利用自回归历史上下文和缓存维持时间一致性，IDM 型 WAM 还需要预测未来视觉状态后再解码动作；Cosmos-Policy 可同时支持直接策略生成和借助未来状态、价值估计的模型式规划；Fast-WAM 与 GigaWorld-Policy 训练时学习视觉动态，但测试时可省略显式视频生成而只产生动作。论文同时检查推理延迟，因为即使 WAM 在扰动下成功率较高，单步生成未来视觉状态造成的开销也可能妨碍平滑、实时的机器人控制。

**复现信息**

公平解释结果所需的实现信息主要有三点。第一，评测跨越两种具身设置：LIBERO-Plus 检查单臂操作，RoboTwin 2.0-Plus 在 Aloha-Agilex 环境检查双臂操作；二者采用相近扰动思想，使结论不局限于单一机器人形态。第二，模型类别必须按动作是否真正由世界模型骨干产生来界定：例如 MOTUS 虽使用 Wan2.2-5B 生成视频，但动作由额外 VLM 产生，因此被视为混合方法而非表 1 中的严格 WAM。第三，推理速度比较需区分是否在测试时显式生成视觉状态；原文指出 WAM 单步推理至少比 $\pi_{0.5}$ 慢 $4.8$ 倍，并列出 GigaWorld-Policy、Fast-WAM 与 $\pi_0$ 的设备相关延迟，但当前所给章节未完整说明所有模型的硬件、采样步数、控制频率、试验回合数和随机种子，复现或横向比较绝对延迟时必须回查原文实验设置。

此外，表 2 中“小时数”“轨迹数”和跨具身样本数属于不同统计口径，不能直接当作统一数据量相除比较。评测所得成功率应理解为模型架构、视频或语言视觉预训练、具身数据多样性、任务微调和推理机制的综合结果；若要严格识别视频动态先验的独立因果贡献，还需要保持骨干规模、机器人数据和微调预算一致的受控实验，而当前研究主要提供跨现有先进系统的实证比较。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LIBERO-Plus：单臂操作鲁棒性基准，在LIBERO任务上引入七类扰动，用于检验模型面对视觉与语言上下文变化时能否继续完成任务。所给原文未列出具体任务数、测试回合数、数据划分及七类扰动的完整名称。
- RoboTwin 2.0-Plus：作者基于RoboTwin 2.0构建的双臂操作鲁棒性基准，使用Aloha-Agilex双臂平台，并采用与LIBERO-Plus相似的扰动协议。它用于判断单臂环境中的鲁棒性结论能否延伸到双臂协作操作；所给原文未明确报告任务规模、测试回合数和划分方式。
- 各模型的任务特定训练数据：这不是统一测试集，而是解释结果差异的重要训练条件。表2显示，不同模型使用的机器人预训练与任务微调数据量差异明显，例如LingBot-VA经过跨本体机器人数据预训练，而Cosmos-Policy和Fast-WAM未列出机器人具身预训练。因而实验比较的是实际训练方案下的系统鲁棒性，不是严格控制数据预算后的纯架构比较。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务成功率**

在给定扰动条件下成功完成机器人操作任务的评测回合比例，直接反映策略在上下文变化后是否仍能实现任务目标。 （越高越好，因为更高比例表示模型在更多受扰动回合中完成了任务。）

</div>
<div class="metric-item" markdown="1">

**鲁棒性**

模型在噪声、照明、布局以及语言等扰动下维持任务成功表现的能力。所给原文主要通过受扰动基准上的成功率进行表征，但未提供独立的鲁棒性计算公式。 （受扰动后的成功率越高或相对性能下降越小越好；原文未明确给出统一的下降率指标。）

</div>
<div class="metric-item" markdown="1">

**单步推理延迟**

策略生成一次动作决策所需的时间，用于衡量能否支持平滑、实时的机器人控制。 （越低越好，因为较短延迟更适合高频闭环控制，也能减少环境已变化而动作仍基于旧观测的问题。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RoboTwin 2.0-Plus双臂操作扰动评测

<div class="result-value" markdown="1">

LingBot-VA达到$74.2\%$任务成功率，是原文明确报告的RoboTwin 2.0-Plus代表性WAM结果。

</div>

作者据此主张WAM在双臂任务的上下文扰动下具有较强鲁棒性。该结果说明显式利用视频动态先验的策略能够在此基准上保持较高成功率，但不能单独证明WAM架构必然优于所有VLA：LingBot-VA还使用了大规模跨本体机器人预训练数据，而且所给节选没有提供同一数据预算下的受控比较或统计误差。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Our results show that WAMs achieve strong robustness, with LingBot-VA reaching 74.2% success rate on RoboTwin 2.0-Plus and Cosmos-Policy achieving 82.2% on LIBERO-Plus.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### LIBERO-Plus单臂操作扰动评测

<div class="result-value" markdown="1">

Cosmos-Policy达到$82.2\%$任务成功率，是原文明确报告的LIBERO-Plus代表性WAM结果。

</div>

作者将该分数视为WAM在单臂视觉与语言扰动下保持强鲁棒性的证据。它支持视频世界模型先验可能帮助策略适应测试时变化，但不能确定收益究竟来自世界模型骨干、联合训练目标、任务微调数据还是其他实现差异；节选也未给出逐扰动结果，因而无法判断该模型对哪类扰动最强或最弱。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Our results show that WAMs achieve strong robustness, with LingBot-VA reaching 74.2% success rate on RoboTwin 2.0-Plus and Cosmos-Policy achieving 82.2% on LIBERO-Plus.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### WAM与$\pi_{0.5}$的推理效率比较

<div class="result-value" markdown="1">

作者报告WAM单步推理至少比$\pi_{0.5}$慢$4.8$倍，表明鲁棒性优势伴随显著计算开销。

</div>

这意味着即使WAM在离线成功率上表现强，其生成未来视觉状态或执行视频模型去噪的过程仍可能妨碍实时控制。该倍数说明部署权衡，而不是任务成功率排名；由于所给节选没有同时给出硬件、批量大小和推理配置，不能据此精确比较所有模型的工程效率。

<div class="result-source" markdown="1">

来源：Section 1, Introduction

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

However, the high inference overhead of WAMs remains a major challenge that limits their deployment in real-world robotic systems, with a single inference step being at least 4.8 times slower than $\pi_{0.5}$.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 模型间训练数据、具身预训练阶段和目标函数并未统一：例如$\pi_{0.5}$使用多类网络与机器人数据，LingBot-VA使用大规模跨本体数据，而部分WAM仅做任务微调。因此，成功率差异不能被纯粹归因于“VLA或WAM”这一架构类别。
- 所给来源节选缺少完整实验表、逐扰动分数、方差或置信区间、评测回合数及受控消融。现有证据足以概括作者报告的总体趋势，却不足以检验差异是否显著，也无法确定视频动态先验、数据多样性与动作解码设计各自的独立贡献。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 经典VLA：以$\pi_{0.5}$为重点，并涉及$\pi_0$、OpenVLA-OFT和X-VLA。这类方法直接由视觉、语言及机器人状态预测动作，是判断显式预测未来视觉状态是否必要的主要参照。
- 混合VLA与世界模型方法：VLA-JEPA和MOTUS在VLA训练中加入视频学习或动态预测，但并非完全依靠世界模型骨干生成动作。它们用于观察只部分引入视频动态先验能否获得介于经典VLA与WAM之间的鲁棒性。
- 基于逆动力学模型的WAM：以LingBot-VA为代表，先形成或利用预测的未来视觉状态，再据此推断动作。该比较用于检验显式以未来状态为动作条件是否有利于跨扰动泛化。
- 联合生成式WAM：以Cosmos-Policy和Fast-WAM为代表，对未来视觉状态与动作进行联合预测或联合去噪；其中Fast-WAM测试时可仅生成动作。它们用于比较不同视频先验整合方式以及省略测试时视频生成后的速度—鲁棒性权衡。

**实验想回答的问题**

- 在单臂与双臂机器人操作任务遭遇视觉和语言扰动时，基于视频世界模型的世界动作模型（WAM）是否比经典视觉—语言—动作模型（VLA）具有更强的任务成功率与鲁棒性？
- WAM的鲁棒性是否取决于其动作生成设计、视频动态先验和机器人训练数据多样性，以及这种鲁棒性是否以更高的推理延迟为代价？

**实验实现**

实验在LIBERO-Plus单臂环境和RoboTwin 2.0-Plus双臂Aloha-Agilex环境中，对代表性VLA、混合方法与WAM施加视觉和语言上下文扰动，并比较任务成功率。分析同时结合表2所列的具身预训练、后训练及任务特定微调数据，以避免把数据规模带来的收益误判为架构收益。所给节选没有给出随机种子、每项任务的评测回合数、置信区间、检查点选择规则、硬件配置或所有扰动类别，因此无法判断分数差异的统计显著性和严格复现条件。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文对Fast-WAM给出跨基准的诊断性比较：它在RoboTwin 2.0-Plus上与LingBot-VA基本相当，但在缺少多样化训练数据的LIBERO-Plus上鲁棒性明显崩溃。作者据此认为，联合去噪设计比显式让动作依赖预测未来状态的逆动力学设计更依赖训练数据多样性。该观察有助于定位失败来源，但所给节选未提供逐任务案例、可视化轨迹或对应数值，因此只能视为定性机制线索，不能替代受控消融。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：系统评估并比较机器人VLA策略与世界动作模型在视觉和语言扰动下的泛化鲁棒性。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`c12dd985e4412cba5e951f893490f96e23d7d253b8c68fb7c76ba3fd5d920aac`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
