---
title: "[论文解读] G0.5: One Autoregressive Stream for Robot Reasoning and Action"
description: "[arXiv 2608.11739][机器人 / 具身智能] 本文研究如何让视觉—语言—动作模型中的预训练视觉语言模型不再只是为外部动作专家提供条件，而是通过统一的自回归序列直接完成推理与机器人动作生成。"
arxiv_id: "2608.11739"
announcement_date: "2026-08-13"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:51:25.455091+00:00"
source_sha256: "4d69ad169f2c9888c67a7120fd5c493b2ec61800f63d4bd7e00125fc94c8aad9"
tags:
  - "机器人 / 具身智能"
  - "LLM Reasoning"
  - "视觉-语言-动作模型"
  - "自回归机器人控制"
  - "跨本体动作词元化"
  - "思维链"
  - "视觉记忆"
  - "长时程操作"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2608.11739</p>

# G0.5: One Autoregressive Stream for Robot Reasoning and Action

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Yicheng Liu, Zibin Dong, Baijun Ye, Tianyuan Yuan, Tao Jiang, Anqi Yang, Shicheng Cao, Haonan Liu, Yue Sun, Zihan Guo, Xiao Liu, Dong Ke, Changxun Pan, Chenru Wu, Tailai Cheng, Xiaoshu Ren, Xinlei Zhang, Jianning Cui, Zijie Zhao, Haoyu Zhang, Kaiming Xu, Haodong Yang, Bowen Zhang, Jiahui Niu, Shaoting Zhu, Shiduo Zhang, Hang Zhao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11739v1) · [PDF 下载](https://arxiv.org/pdf/2608.11739v1) · **关键词** 视觉-语言-动作模型, 自回归机器人控制, 跨本体动作词元化, 思维链, 视觉记忆, 长时程操作<br>


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

本文研究如何让视觉—语言—动作模型中的预训练视觉语言模型不再只是为外部动作专家提供条件，而是通过统一的自回归序列直接完成推理与机器人动作生成。

**不用术语来说**：现有高性能机器人模型通常把“理解指令和图像”与“生成电机动作”交给两个分别训练的模块：视觉语言模型负责理解，动作专家负责控制。这样虽然能高效地产生连续动作，却使模型在语言预训练中获得的任务分解、上下文学习和按提示调整行为等能力难以直接作用于机器人决策。早期由视觉语言模型逐个生成动作符号的方案连接更直接，但面对高控制频率、长动作时域和多自由度机器人时，需要输出过多符号，推理成本过高。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出以单一 Transformer 解码器和统一的下一词元目标生成推理词元与动作词元，使任务分解、物体定位、动作提示和实际控制成为同一生成过程，而不是视觉语言模型与外部动作专家之间的两个阶段。
- 作者提出可学习的跨机器人动作编解码器，将不同形态、自由度和控制频率下的连续动作块压缩为共享离散词表，并仅编码当前活跃的自由度组；该入口旨在消除自回归控制的词元效率瓶颈，同时保留视觉语言模型直接决定动作的能力。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

视觉-语言-动作模型（VLA）把图像理解、语言指令理解与机器人控制放入同一学习框架。早期方法将连续动作离散为词元，由视觉语言模型（VLM）像生成文本一样逐个预测，因此VLM本身就是策略；但随着控制频率、动作时域和自由度增加，每个时间步所需的动作词元迅速增多，推理延迟与计算成本随之上升。主流方案因此改用“VLM作为编码器”：VLM只提供视觉语言条件，独立的流匹配或扩散动作专家再生成连续动作块。本文重新研究自回归VLA，核心问题是在保留VLM直接生成动作、推理和提示控制能力的同时，压缩异构机器人的动作表示，使统一自回归控制能够扩展到基础模型规模。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自回归视觉-语言-动作模型**

模型把图像、指令、机器人状态、推理文本和动作都表示为一个有序序列，并依据已有上下文逐个预测下一个词元。这样，语言推理与动作决策由同一解码器和同一组参数完成。

</div>
<div class="concept-item" markdown="1">

**动作词元化**

动作词元化把关节位置、末端位姿或夹爪状态等连续控制量编码为有限词表中的离散代码，使VLM能够用文本生成式接口预测机器人动作。本文进一步将一段动作压缩为紧凑代码，并省略当前不活动自由度对应的词元组，以降低解码开销。

</div>
<div class="concept-item" markdown="1">

**流匹配动作专家**

流匹配策略通常使用独立网络，在VLM提供的条件特征下把简单初始分布逐步变换为连续动作分布，适合并行生成动作块。其效率较高，但最终动作由独立参数和独立目标产生，VLM的思维链、上下文学习和提示响应只能经过条件表示间接影响控制。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务是在闭环机器人控制中学习一个统一策略：每轮输入包括多视角RGB图像、自然语言任务指令、机器人本体状态以及用于区分机器人形态的本体标识；模型还可通过视觉记忆接收跨越数秒的历史图像信息。输出是一个自回归生成段，其中可包含任务分解、目标物体边界框、轨迹或动作提示等思维链内容，随后生成离散动作代码；跨本体动作编解码器再将这些代码还原为连续电机命令。问题设置允许不同数据源中的机器人具有不同形态、控制频率和自由度，并要求它们共享一个动作词表；推理时模型根据更新后的视觉与本体状态反复生成动作，从而执行长时程任务并进行闭环重规划。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$R$**

动作编解码器的残差量化轮数；每轮由自由度组标记及其后的动作代码组成。

</div>
<div class="notation-item" markdown="1">

**$\pi_{0.5}$**

论文实验与引言中用于比较的VLM编码器式VLA基线。

</div>

</div>

**直接相关的工作**

- **FAST**: 直接相关的自回归动作词元化方案；它对每种机器人本体分别采用固定的离散余弦变换流程，而本文提出可学习、端到端且跨本体共享的动作编解码器。
- **CoT-VLA与DualCoT-VLA**: 这些方法把推理模块附加到VLM编码器式控制架构上；本文则让推理词元与动作词元共享同一解码器、上下文和下一词元训练目标，使推理成为动作生成过程的原生组成部分。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

通用机器人需要同时理解自然语言、识别场景对象、把长指令拆成可执行阶段，并在持续变化的环境中闭环地产生高频动作。实际部署还涉及不同机器人形态、控制频率和动作维度，因此模型既要复用大规模视觉语言预训练所得的推理与指令遵循能力，又必须以足够紧凑的表示生成连续控制序列；现有架构往往只能较好满足其中一方面。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **自回归动作词元模型**：把连续机器人动作离散化为动作词元，加入语言词表，再由视觉语言模型像生成文本一样逐词元预测动作。视觉语言模型因此直接充当策略，但每个时间步和自由度都可能引入额外词元；控制频率、动作时域或动作维数增加时，序列会迅速变长。
- **视觉语言模型编码器加流匹配或扩散动作专家**：预训练视觉语言模型先把图像和指令变成隐藏状态或键值缓存，另一个具有独立参数和训练目标的动作专家据此一次生成连续动作块。该架构减少了逐词元解码负担，但最终动作分布由外部专家而非视觉语言模型产生。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 早期自回归方案存在过度动作词元化：高频、长时域、多自由度控制会产生很长的输出序列，导致推理延迟和计算成本上升，因而难以扩展到基础模型规模及复杂机器人平台。
- 动作专家方案在视觉语言模型与控制输出之间形成压缩条件瓶颈；链式推理、上下文学习和提示驱动的动作调整只能间接影响独立专家，不能作为下一动作生成的原生组成部分。作者据此主张其语言遵循与长时程执行能力可能受到结构性削弱，但提示控制部分在本文中主要得到初步定性证据，尚非系统定量结论。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作尚未同时实现两项目标：一方面保持自回归接口，使预训练视觉语言模型直接决定动作并让推理过程进入控制序列；另一方面把异构机器人的连续动作压缩到足够少的离散词元，使该接口能承担高维、高频和长时域控制。相关链式推理方法即使增加推理模块，也通常仍建立在“视觉语言模型作为编码器、外部专家生成动作”的分离结构上。

</div>
<div markdown="1"><span>核心问题</span>

能否通过共享参数、上下文和训练目标的单一自回归词元流，统一生成机器人推理与动作，同时利用学习式跨机器人动作压缩和活跃自由度编码控制序列长度，从而兼顾动作效率、跨平台迁移、指令遵循及长时程闭环执行？

</div>
<div markdown="1"><span>作者直觉</span>

动作片段中存在大量时间相关性，而且许多时刻只有部分关节或机械臂真正运动，因此没有必要逐时刻、逐自由度地完整输出。若先把动作块压缩成少量共享代码，并省略静止控制组，视觉语言模型就能以接近语言生成的方式直接预测控制结果；又因为推理文字与动作代码由同一解码器依次生成，模型刚刚作出的子任务判断、物体定位或动作提示可以直接成为后续动作的上下文。直观上，这相当于让同一个决策者一边观察和分解任务、一边执行，而不是先把理解结果压缩后交给另一个独立控制器。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

G0.5 将机器人策略建模为一个统一的自回归序列生成问题：输入是最近数秒的多视角 RGB 观测、机器人本体标识、自然语言任务指令和与图像同步的本体状态；输出则是可选的思维链文本以及结构化离散动作码。模型以 Qwen3.5 2B 视觉语言模型为初始化基础，视觉编码器负责融合当前帧与短期历史，单个 Transformer 解码器在共享词表中依次生成任务分解、目标框、运动轨迹或动作提示，随后生成动作 token；跨本体 ActionCodec 再把动作 token 解码为统一连续动作空间中的控制命令。训练时，条件部分只提供上下文，交叉熵损失仅施加于思维链与动作组成的生成部分，因此感知条件下的推理和控制由同一组参数、同一次前向生成及同一个目标联合学习。

与“视觉语言模型只编码上下文、另设流匹配动作专家”的方案相比，核心设计不是简单地在动作前附加解释文本，而是让推理 token 与动作 token 位于同一因果序列中：后续动作可直接注意此前生成的目标定位、子任务和动作提示。直观地说，模型像一个同时负责观察、制定步骤并执行的控制器，而不是先由一个模型理解场景，再把压缩后的表示交给另一个独立控制器。论文的主实验默认使用这一自包含的自回归策略；额外的流匹配头仅用于比较或可选部署，不属于统一自回归主路径的必要组成。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多模态条件构造与时间对齐

模型把图像、历史视觉信息、本体类型、任务和连续状态嵌入序列化到用户侧条件段，并以 `<EOC>` 标记条件结束；连续状态嵌入与对应视觉帧同步，避免先离散成文本 token 所造成的时间或数值错配。

<div class="method-step__io" markdown="1">

**输入**：来自 $K$ 个摄像头、覆盖短时间窗口的 RGB 观测 $\{o_{t-h}^{(k)}\}$，机器人本体标识 $e$，自然语言指令 $\ell$，以及当前或逐帧对齐的本体状态 $s_t$。<br>
**输出**：一个不参与直接损失计算、但为后续生成提供上下文的条件 token 序列。

</div>

**直观理解**：这一步相当于先把“看到了什么、使用哪种机器人、要做什么、机器人当前姿态如何”整理成同一份时序一致的任务上下文。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 视觉记忆编码

视觉 Transformer 每隔四层插入分解的空间注意力与时间注意力，先后混合不同图像区域和不同时间点的信息；最终层丢弃历史 token，仅保留融合过历史上下文的当前表示，以限制后续解码开销。

<div class="method-step__io" markdown="1">

**输入**：当前与历史多视角图像所形成的时空视觉 token，以及与图像同步的连续本体状态嵌入。<br>
**输出**：包含短期运动历史、遮挡前线索和当前场景信息的紧凑视觉条件表示。

</div>

**直观理解**：模型不把所有旧画面一直带入语言解码器，而是在视觉编码阶段先将“刚才发生了什么”压缩进当前表示，因此能利用历史，又不会让生成成本随历史长度迅速膨胀。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 原生思维链与动作码自回归生成

同一个解码器按 token 顺序生成可选的思维链字段，包括 `Subtask:`、`BBox:`、`Trace:` 和 `ActionHint:`，并以 `<EOV>` 标记推理与动作的边界，随后生成按运动部件和残差轮次组织的离散动作码；训练时从八种经整理的思维链组合中采样，也包括完全不生成思维链的配置。

<div class="method-step__io" markdown="1">

**输入**：完整条件序列及视觉记忆表示。<br>
**输出**：助手侧生成段，即可选推理 token 加上结构化动作 token。

</div>

**直观理解**：模型可以先说清当前子目标、关键物体在哪里以及动作大致怎么走，再继续输出真正的控制符号；由于两者在同一序列内，动作能够直接利用刚生成的推理内容。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 跨本体动作解码与执行

ActionCodec 根据部件标记和机器人本体，将共享词表中的离散码经残差向量量化解码器还原成统一动作空间内的连续控制命令，并只为当前活跃的自由度组生成动作；非活跃部件保持静止。

<div class="method-step__io" markdown="1">

**输入**：按残差量化轮次排列、带有左侧控制、右侧控制及可选下半身控制标记的动作 token。<br>
**输出**：适配指定机器人本体的连续控制指令，可直接送入机器人或仿真环境执行。

</div>

**直观理解**：共享动作词表像一套跨机器人的“动作拼音”，部件标记说明由哪只手或哪部分身体执行，解码器再把这些符号翻译成具体机器人的连续关节控制量。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 生成段下一 token 交叉熵目标

$$
\mathcal{L}(\theta)=-\sum_{i\in\mathcal{G}}\log p_{\theta}\bigl(x_i\mid x_{<i}\bigr)
$$

**符号说明**

- $\mathcal{L}(\theta)$：参数为 $\theta$ 的 G0.5 在一个序列上的训练损失。
- $\theta$：统一视觉语言动作模型的可训练参数，包括产生推理 token 与动作 token 的共享参数。
- $\mathcal{G}$：生成段 token 的位置索引集合；条件段不属于该集合。
- $x_i$：序列中第 $i$ 个目标 token，可能是思维链文本、结构标记或离散动作码。
- $x_{<i}$：第 $i$ 个位置之前的全部条件与已生成 token。
- $p_{\theta}(x_i\mid x_{<i})$：模型在历史序列 $x_{<i}$ 条件下赋予正确下一 token $x_i$ 的概率。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标逐位置提高正确推理 token 和正确动作 token 的条件概率，但不要求模型重建输入条件。其关键意义在于，任务分解、目标定位等推理监督与机器人动作监督被化为同一种“预测下一个符号”的学习问题，不需要预训练阶段的额外连续动作回归损失或动作专家蒸馏。<br>
**原文位置**：第 3 节，公式 (1)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练样本先被序列化为条件段和生成段：前者包含图像、本体、指令与状态，并以 `<EOC>` 结束；后者包含可选思维链、推理—动作边界 `<EOV>` 和动作码。优化时仅对索引属于 $\mathcal{G}$ 的生成位置计算教师强制下的下一 token 交叉熵，因此条件段用于提供因果上下文，却不被当作待预测目标。一次损失同时监督文本式推理与离散动作生成，使二者更新同一解码器参数；论文明确指出，预训练阶段没有附加动作回归目标或专家蒸馏。

ActionCodec 自身采用按运动部件分组的 RVQ 表示，并额外引入时间对比目标来提高相邻动作的 token 一致性，但所给节选未提供该目标的具体公式或权重，因而不能据此重构完整损失。主模型从 Qwen3.5 2B 初始化，并在机器人示范与视觉问答数据的异构混合上单阶段预训练；节选没有完整给出机器人数据构成、采样比例和全部优化超参数。训练中从八种思维链配置采样且随机丢弃全部历史帧，分别用于让同一模型兼容有无显式推理的生成方式，以及降低对固定视觉历史模式的过拟合。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 跨本体结构化 ActionCodec**

该模块先依据机器人拓扑把异构动作分成语义对齐且相互独立的运动部件，例如左侧控制、右侧控制和下半身控制，再把各部件补齐到共享最大维度，并用残差向量量化（RVQ）学习统一离散动作词表。动作序列展开为 $R$ 个残差轮次；每轮先输出 `<left_control_r>`、`<right_control_r>` 或可选的 `<lower_body_control_r>` 等部件标记，再为每个活跃部件输出 8 个动作码，同时通过时间对比目标鼓励时间相邻、语义相近的动作得到更一致的编码。

> 直观理解：直接把所有关节拼成一个长向量，会把左右手等不同功能混在一起，而且机器人自由度越多，token 越长。按身体部件编码既让不同机器人能够共享“左手操作”等结构，也允许只预测正在运动的部件，从而减少无效 token；时间一致性约束则避免相邻动作被编码成差异很大的符号，降低主模型学习动作序列时的噪声。

**2. 原生思维链支架**

推理并非独立辅助头，而是生成段内位于动作之前的普通 token，可包含任务分解、关键物体边界框、二维运动轨迹和动作提示四类自描述目标；每一步可以生成其中任意子集。所有组合与动作共享词表、解码器参数和下一 token 损失，推理结束后，自回归动作码可通过因果注意力直接读取完整思维链。

> 直观理解：传统辅助任务通常只在训练时要求模型找物体或预测子任务，执行时却不显式经过这些中间结果。这里把中间判断真正放进控制流程，使“先确定当前要做什么、目标在哪里，再行动”成为可在测试时开关和提示的生成过程；但思维链由模型自行生成，错误推理也可能继续影响后续动作。

**3. 短期视觉记忆**

视觉编码器每隔四层加入分解式时空注意力：空间注意力处理同一帧内不同图像块的关系，时间注意力聚合不同时间点的对应信息。为控制延迟，最终层删除历史 token；训练时还以随机方式丢弃全部历史帧，防止策略过度依赖固定时间轨迹，并使用连续状态嵌入实现本体状态与图像逐帧同步。

> 直观理解：单帧策略在机械臂遮挡物体、操作失败后重试等情形下缺少记忆，而把所有历史帧直接送入解码器又会显著增加计算量。该模块在视觉端先融合再压缩历史，并通过随机移除历史训练模型，使它既能利用过去，也能在历史缺失或时间模式变化时工作。

**训练与推理**

训练流程为：先按语义运动部件整理不同机器人本体的连续动作，用跨本体 ActionCodec 将其转换为共享词表中的结构化动作码；再把多视角时间窗口、机器人标识、语言任务、连续本体状态、可选思维链标注及动作码拼成单一因果序列。视觉编码器利用分解式时空注意力融合历史帧，解码器在教师强制下预测生成段的每个 token，并以统一交叉熵更新推理和动作参数。思维链监督可从任务分解、边界框、轨迹和动作提示中选取任意子集，八种整理好的组合包含无思维链基线，因此预训练后的模型不必依赖固定推理模板才能输出动作。

默认推理流程为：给定 $\{o_{t-h}^{(k)}\}$、$e$、$\ell$ 和 $s_t$，模型先编码视觉记忆和其他条件，再依据提示模板决定是否生成思维链。若启用思维链，模型依次产生相关推理字段并输出 `<EOV>`，随后同一解码器继续采样结构化动作 token；若关闭，则直接进入动作生成。ActionCodec 把离散码解码为连续命令并执行，新的观测再进入下一控制周期。提示可在不再训练的情况下改变是否推理及推理内容，进而影响动作粒度、任务阶段和异常场景处理。论文还实现了一个可选流匹配头：它读取自回归主干隐藏状态并产生连续动作，用于对照或部署；当思维链开启时，自回归和流匹配两种解码器都读取思维链之后的隐藏状态，但主实验默认策略仍是完整的自回归 VLA。

**复现信息**

公平理解该方法所需的结构细节包括：主干初始化自 Qwen3.5 2B；视觉 Transformer 每隔四层插入空间与时间注意力；最终视觉层丢弃历史 token；状态使用连续嵌入并与相应视觉帧同步；动作采用按部件分组的 RVQ，每个残差轮次中，每个活跃自由度组跟随 8 个动作码。部件序列至少支持左侧和右侧控制，具有下半身的本体还可加入下半身控制；残差轮次数 $R$、共享最大动作维数、RVQ 码本规模、控制频率和历史窗口长度在所给节选中未明确报告。

复现时还需注意，自回归 VLA 是所有主实验的默认策略，流匹配头是附加比较接口，不能把后者误作训练统一性的必要组件。节选仅说明预训练使用机器人示范与网络规模视觉语言数据的单阶段混合、八种思维链组合、历史帧随机全丢弃和生成段交叉熵；完整数据比例、批量大小、学习率、训练步数及 ActionCodec 时间对比损失系数均原文未在所给内容中明确报告，因此仅凭该节选无法做到参数级复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- DROID：用于对 G0.5 及对比方法进行后训练。评测端采用标准 DROID 硬件形态的 Franka Research 3 机械臂，但物理环境和物体实例均未出现在预训练或后训练中，因此测试的是经过 DROID 适配后的环境级与物体级零样本泛化，而不是完全不接触 DROID 数据的数据集级零样本迁移。评测包含 10 个桌面操作任务、8 种留出场景设置，覆盖放置、颜色条件选择、小孔径插入、可变形物体操作、空间移动及多阶段任务。
- BridgeData V2：用于把 G0.5 后训练到 WidowX/Bridge 具身形态；随后在 SimplerEnv 的 Bridge 标准任务套件中评测，不再使用仿真域训练数据。四项任务分别是把勺子放到毛巾上、把胡萝卜放到盘子上、把绿色方块叠到黄色方块上，以及把茄子放入黄色篮子，主要检验从真实机器人示范向模拟评测环境的迁移。
- Bridge-SimplerEnv：基于 BridgeData V2/WidowX 配置构建的真实到仿真评测基准。它在可规模化的模拟环境中测试语言条件 WidowX 操作策略；本文采用不输入关节状态等本体感觉信息的 state-free 设置，使模型只能依据视觉和语言完成控制。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务成功率**

统计试验中完成指定操作目标的比例。DROID 通常按二元结果计分；“把方块放入抽屉并关闭抽屉”任务若只完成插入子步骤得 $0.5$ 分，完整完成得 $1.0$ 分，因此其汇总值兼有成功比例与部分完成程度的含义。 （越高越好，因为更高数值表示策略在更多试验中完成了全部目标，或在指定顺序任务中至少完成了更多子目标。）

</div>
<div class="metric-item" markdown="1">

**平均成功率**

对一个基准内多项任务的成功率进行汇总，用于衡量策略覆盖不同物体、指令和操作技能时的总体可靠性；它可能掩盖单项任务差异，需结合逐任务结果理解。 （越高越好，因为它表示策略在整个任务集合上的总体完成能力更强。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### DROID 留出物理环境与物体实例上的零样本评测

<div class="result-value" markdown="1">

G0.5-DROID 在 10 项任务上的平均成功率为 $82.5\%$，相比 $\pi_{0.5}$-DROID 的 $57.5\%$ 高 $25.0$ 个百分点，相比 MolmoAct2-DROID 的 $52.0\%$ 高 $30.5$ 个百分点。

</div>

作者结果表明，在三种方法均利用 DROID 数据训练或后训练后，G0.5 对未见环境和未见物体实例的迁移更稳定，优势覆盖物体放置、颜色选择、空间指令和顺序执行等任务。该结果证明的是 DROID 数据分布内具身适配后的环境级、实例级泛化，并不证明模型能在从未使用 DROID 数据的情况下直接部署，也不能单独排除训练流程、模型规模或数据处理差异带来的影响。

<div class="result-source" markdown="1">

来源：Figure 6 caption; Section 5.1.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

G0.5 achieves an average of 82.5%, outperforming π0.5-DROID (57.5%) by 25.0 percentage points and MolmoAct2-DROID (52.0%) by 30.5 percentage points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### DROID 逐任务比较与多阶段操作

<div class="result-value" markdown="1">

G0.5-DROID 在全部 10 项任务上均优于 $\pi_{0.5}$-DROID；对于“把方块放入打开的抽屉并关闭抽屉”这一顺序任务，MolmoAct2-DROID 完全失败，而 G0.5-DROID 在超过一半的试验中成功。

</div>

这一结果补充了平均分：提升并非只由少数简单任务拉动，而且在需要先插入方块、再关闭抽屉的时间依赖任务上仍能体现出来。作者将其解释为更强的多阶段执行能力，但摘录没有给出该任务的精确成功率、置信区间或显著性检验；同时该任务允许部分计分，因此“超过一半成功”的具体统计口径仍需结合原图核查。

<div class="result-source" markdown="1">

来源：Section 5.1.2, “G0.5-DROID vs. MolmoAct2-DROID”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Most notably, MolmoAct2-DROID completely fails on the sequential task put the block into the open drawer and close the drawer, while G0.5-DROID succeeds on over half of the trials, demonstrating substantially stronger multi-stage task execution capability.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### BridgeData V2 后训练后直接迁移到 Bridge-SimplerEnv

<div class="result-value" markdown="1">

在不使用额外仿真域训练、且不输入关节状态等本体感觉信息的条件下，G0.5 在四项 Bridge 风格任务上取得 $87.3\%$ 的平均成功率，为表 1 所比较方法中的最高值。

</div>

该结果测试的是模型先通过 BridgeData V2 适配 WidowX 具身，再从真实示范分布迁移到 SimplerEnv 仿真域的能力。state-free 输入使策略更依赖视觉和语言，也说明较高分数不是直接读取关节状态所得；但这仍是经过 80K 步 Bridge 后训练的结果，不是未经目标具身数据适配的零样本控制。由于部分基线数值由其他研究汇编，最高排名还应结合各来源的实现和协议一致性审慎解读。

<div class="result-source" markdown="1">

来源：Section 5.2.1; Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We then evaluate the resulting policy in SimplerEnv without any additional simulation-domain training. Results are summarized in Tab. 1, where G0.5 achieves the highest average success rate of 87.3% among the compared methods.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- DROID 每项任务只有 10 次试验，且摘录未报告随机化方案、置信区间或统计显著性；因此 $82.5\%$ 的总体结果足以显示较大平均优势，但较小的逐任务差异和“超过一半”等表述仍需通过更多重复试验验证。
- 两组评测都包含目标具身数据上的后训练：DROID 结果不是数据集级零样本，Bridge 结果也经过 80K 步 BridgeData V2 后训练。此外，Bridge 的部分基线分数汇编自先前研究，跨论文的实现、检查点和评测细节可能并不完全一致。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- $\pi_{0.5}$-DROID：使用 PaliGemma 骨干并在原始 DROID 数据上训练，是与 G0.5 比较 DROID 具身适配效果和留出环境泛化能力的直接 VLA 基线。
- MolmoAct2-DROID：建立在 Molmo 视觉语言模型之上，并使用 MolmoAct2 数据处理流程训练；该基线用于比较另一种通用视觉语言策略在语义 grounding、抓取和多阶段执行方面的表现。
- Bridge-SimplerEnv 表 1 中的既有方法：原文说明部分模型的 SimplerEnv-WidowX 数值并非来自其原始论文，而是汇编自先前在该基准上评测这些模型的研究。该组基线可用于判断 G0.5 在统一任务套件中的相对位置，但跨来源实现和评测细节可能削弱严格可比性。

**实验想回答的问题**

- 在使用 DROID 或 BridgeData V2 进行具身适配后，G0.5 能否迁移到训练中未出现的物理环境、物体实例或仿真域，并在语言条件操作任务上优于已有 VLA 策略？
- G0.5 的优势是否延伸到视觉定位、多阶段执行和语言 grounding 等关键能力，以及视觉对比度等输入条件会怎样影响其实际表现？

**实验实现**

DROID 评测使用 Franka Research 3 七自由度机械臂和 Robotiq 2F-85 平行夹爪，输入包括固定的右侧第三人称 RGB 相机、腕部 RGB 相机以及自然语言指令。每个任务运行 10 次，共覆盖 10 个任务；除一个顺序任务允许 $0.5$ 的部分得分外，其余任务按完成或失败计分。Bridge 设置中，G0.5 在 BridgeData V2 上后训练 80K 个梯度步骤，学习率为 $3\times10^{-5}$；训练和评测都不输入机器人关节状态或其他本体感觉状态，之后直接进入 SimplerEnv，且不使用额外的仿真域训练。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 抽屉内部是否加入高对比度橙色标记 | 在没有标记的早期毛巾插入实验中，$\pi_{0.5}$-DROID、MolmoAct2-DROID 和 G0.5-DROID 的成功率分别为 $90\%$、$80\%$ 和 $60\%$；加入高对比度标记后，G0.5-DROID 提升到 $100\%$，而作者称 $\pi_{0.5}$-DROID 相对不受影响。 | 该受控比较主要隔离抽屉开口的视觉可定位性，而不是模型整体推理能力。G0.5 的 $40$ 个百分点提升说明其失败很可能与白色半透明表面的低对比度有关；这既证明显式视觉提示有效，也暴露模型对视觉条件变化的敏感性。原文没有在摘录中给出加入标记后另两种方法的精确分数、重复次数变化或统计检验，因此不能据此完整比较三者的视觉鲁棒性。 | Section 5.1.2, “Effect of visual contrast on drawer localisation”<br><span class="experiment-evidence">Adding the high-contrast markers dramatically improves G0.5-DROID’s performance to 100%, while π0.5-DROID remains comparatively unaffected.</span> |

**定性案例**

- 作者观察到 MolmoAct2-DROID 在接近胡萝卜、桃子或碗时经常停住或不产生动作，并会在夹爪尚未到达有效预抓取位姿时执行空抓；这提示其失败不只发生在最终放置阶段，也可能源于目标 grounding 到接近、抓取动作之间的转换不稳定。该现象属于定性观察，原文未明确报告发生频率，不能替代系统的错误分类统计。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出统一自回归生成推理与动作 token 的视觉语言动作基础模型，并在多项机器人操作任务上验证。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`4d69ad169f2c9888c67a7120fd5c493b2ec61800f63d4bd7e00125fc94c8aad9`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
