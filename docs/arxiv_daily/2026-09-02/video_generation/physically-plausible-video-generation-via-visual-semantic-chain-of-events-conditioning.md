---
title: "[论文解读] Physically Plausible Video Generation via Visual-Semantic Chain-of-Events Conditioning"
description: "[arXiv 2609.00656][视频生成] 原文未明确报告。"
arxiv_id: "2609.00656"
announcement_date: "2026-09-02"
primary_category: "video_generation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:41:46.557861+00:00"
source_sha256: "28df5faa63f75a2320afc133eb51e1b781e5958eaa0809d6c4432e867fcde9e8"
tags:
  - "视频生成"
  - "LLM Reasoning"
  - "物理可信视频生成"
  - "视频扩散模型"
  - "链式推理"
  - "事件中心建模"
  - "场景图"
  - "物理条件控制"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">视频生成 · arXiv 2609.00656</p>

# Physically Plausible Video Generation via Visual-Semantic Chain-of-Events Conditioning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Zixuan Wang, Yixin Hu, Wen Li, Feng Chen, Yan Liu, Duo Peng, Yinjie Lei</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> thanks: Feng Chen is with the School of Computer Science, University of Adelaide</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00656v1) · [PDF 下载](https://arxiv.org/pdf/2609.00656v1) · **关键词** 物理可信视频生成, 视频扩散模型, 链式推理, 事件中心建模, 场景图, 物理条件控制<br>


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

原文未明确报告。

**不用术语来说**：原文未明确报告。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 原文未明确报告。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

物理可信视频生成（Physically Plausible Video Generation，PPVG）是文本到视频生成中的一个专门问题：除了画面逼真，还要求物体运动、相互作用及状态变化符合物理规律。现有文本到视频模型虽然能够合成写实场景，却常把复杂现象表现为单一、整体性的场景快照，无法可靠呈现从初态到终态之间的因果过程。本文据此采用“事件中心”视角，将物理演化理解为一系列因果相连的事件；每个事件对应场景配置的一次有意义变化，连续事件共同规定视频应呈现的时间顺序和中间状态。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视频扩散模型**

一种从噪声逐步去噪并生成连续视频帧的生成模型，可接受文本、图像或其他条件作为引导。本文不重新训练特定物理模拟器，而是把视觉与语义线索输入现成扩散模型，以约束其去噪过程。

</div>
<div class="concept-item" markdown="1">

**场景图与事件边界**

场景图用节点表示物体、用边表示物体之间的关系或交互；事件边界是一次物理变化发生前后具有明确意义的场景状态。相邻场景图之间的差异定义一个事件，从而把连续现象拆成可推理、可检查的因果步骤。

</div>
<div class="concept-item" markdown="1">

**分类器自由引导**

分类器自由引导（Classifier-Free Guidance，CFG）通过比较不同文本条件下的去噪预测来强化目标语义。本文同时提供物理合理的正条件和违反约束的反事实负条件，使模型趋向合理动力学并远离细微的物理错误。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是用户对物理现象的自然语言描述，生成目标是一段既具有视觉连贯性、又完整呈现因果事件顺序和中间物理状态的视频。本文假设仅靠原始文本往往无法明确指定每个过渡阶段，因此先将现象分解为连续的事件边界状态，并把适用公式推导出的方向、幅度或变化率绑定到相关物体和交互；随后为相邻事件状态生成关键帧视觉锚点，同时构造物理一致的正提示与违反约束的反事实负提示，最终将两类条件注入现成视频扩散模型。这里的“物理可信”并不只指运动轨迹看似平滑，还包括外观变化、物体变形或拓扑变化、交互方向以及事件先后关系符合相应物理约束；原文节选未给出统一的形式化输入输出符号或额外环境假设。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **基于图形引擎或可微模拟器的PPVG方法（文中引用[6]–[12]）**: 这类方法显式模拟运动和物体交互，能够提供较强的物理先验；但本文指出，已有方法常依赖视频级监督、短视频前缀或全局条件，未清楚规定跨事件的状态演化。本文改用不断演化的场景图链描述事件边界，并进一步生成逐事件视觉条件。
- **基于物理知识提示增强的CoT方法（文中引用[17]–[21]）**: 这类方法利用链式推理扩充用户描述，使提示包含物理原则，但通常仍从整体上叙述现象，容易遗漏中间状态和过渡动力学。本文保留推理增强思路，同时将其结构化为因果事件链，并通过物理一致正提示与事件级反事实负提示增强语义区分能力。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

物理可信视频生成旨在让文生视频模型不仅生成逼真的画面，还能正确呈现物体运动、相互作用与状态变化所遵循的物理规律。这对电影制作、自动驾驶仿真和具身智能等应用很重要；但现有模型即使画面逼真，也常把复杂物理过程表现成近似静态的整体场景，遗漏必要的中间状态或生成方向、顺序不合理的动态，因此不足以作为可靠的模拟与训练数据。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于模拟或反馈优化的物理约束方法**：一类方法借助图形引擎或可微模拟器显式计算运动和物体交互；另一类方法利用物理偏好、奖励或生成反馈优化视频，使最终结果在视频整体层面更符合物理规律。
- **物理知识增强的提示与视觉引导方法**：提示增强方法通过思维链推理把物理原理补充到用户文本中；视觉引导方法则提供短视频前缀、起止帧或合成光流，帮助扩散模型确定初始运动、端点状态或物体位移。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有方法主要施加视频级监督或给出全局物理描述，没有把现象组织为因果相连的事件，也未明确规定相邻事件之间物体配置、物理量及状态应如何变化。其后果是模型容易只呈现最终或整体场景，无法保持事件的正确时间顺序与中间状态的完整性。
- 短视频前缀和端点帧没有为每次连续物理转变提供专门的视觉锚点，光流又主要描述运动学位移，难以表达形变、相变或外观变化；同时，普通正向提示和泛化负向提示难以区分“液体向下流”与“液体向上流”这类细微但关键的物理差异。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种统一的事件级条件机制：它既要显式表示物理过程的因果阶段及其转变幅度，又要把这些阶段转化为覆盖中间状态的视觉条件，并构造针对具体物理违规的语义对比条件，从而共同约束连续视频生成。

</div>
<div markdown="1"><span>核心问题</span>

能否将物理可信视频生成重构为事件中心的生成问题，以带物理量的演化场景图描述因果过程，并由同一事件链派生逐阶段关键帧与正反事实语义条件，从而引导通用视频扩散模型完整、连贯且物理合理地呈现现象演化？

</div>
<div markdown="1"><span>作者直觉</span>

复杂物理现象可以理解为一串“前一状态导致下一状态”的事件，而不是一句整体描述。若先标出每个事件边界上有哪些对象、关系和关键物理量，再为相邻边界提供视觉锚点，模型就不必自行猜测缺失的中间过程；进一步把正确演化与违反约束的反事实演化同时交给分类器自由引导，等于同时告诉模型“应该朝哪里生成”和“必须避开什么”，因而更容易识别并保留细微但决定物理可信度的动态差异。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把“根据一句自然语言直接生成整段物理视频”改写为“先推理事件边界，再以边界状态约束视频扩散”。输入是用户对物理现象的描述 $w$；系统先用物理驱动事件链推理模块 PECR 将其展开为增广场景图序列 $\mathcal{G}_0^*\xrightarrow{e_1}\cdots\xrightarrow{e_N}\mathcal{G}_N^*$，其中每个事件 $e_n$ 同时记录对象或关系的变化、相关物理约束 $\mathcal{P}_n$ 以及由公式得到的物理量。随后，TRKC 根据事件造成的是颜色、纹理、位移还是形变，选择相应图像编辑算子，递归生成事件边界关键帧 $\mathbf{v}_0,\ldots,\mathbf{v}_N$；这些关键帧在潜空间中被插值，其相对初始状态的变化量作为残差注入视频去噪。最后，PCSG 将事件链压缩为正向物理描述 $\mathcal{W}_+^*$，并通过故意违反物理量或物理方向构造反事实负向描述 $\mathcal{W}_-^*$，二者共同参与分类器无关引导，输出物理演化更可信的视频 $\mathbf{V}$。

直观上，系统不要求视频模型仅凭一句“倒水”自行猜出全过程，而是先写出“容器倾斜—液体向下流出—液体在目标处积累”的分镜和物理规则，再为各分镜画出关键状态，最后明确告诉扩散模型“应当朝哪些变化生成、同时远离哪些违反物理规律的变化”。三个模块分别解决事件结构缺失、视觉过渡缺少锚点以及文本条件只说明正确现象却未排斥错误动力学的问题。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 物理现象分解与场景图递推

LLM 从当前图 $\mathcal{G}_{n-1}$ 推断本步物理约束 $\mathcal{P}_n$，生成多个后继图候选，并选择属性和关系变化最符合该约束的 $\mathcal{G}_n$，递归形成具有因果顺序的事件边界。

<div class="method-step__io" markdown="1">

**输入**：用户描述 $w$，以及由其解析得到的初始场景图 $\mathcal{G}_0=(\mathcal{V}_0,\mathcal{R}_0)$；节点 $\mathcal{V}_0$ 表示对象及可观察属性，边 $\mathcal{R}_0$ 表示对象间的物理交互。<br>
**输出**：未量化的场景图链 $\mathcal{G}_0\xrightarrow{\mathcal{P}_1}\mathcal{G}_1\xrightarrow{\mathcal{P}_2}\cdots\xrightarrow{\mathcal{P}_N}\mathcal{G}_N$。

</div>

**直观理解**：场景图相当于每个关键时刻的结构化快照：它不只写“发生了倒水”，还明确记录容器、液体及其接触、倾斜和位置关系如何逐步改变。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 公式检索、物理量落地与事件链构造

LLM 生成公式查询，从在线来源检索候选公式并按语义相似度选取最佳公式；符号代数引擎解析变量，LLM 再把变量绑定到场景图节点或边，并通过解公式或查询知识库取得数值，对跨图不满足约束的物理量重新计算。

<div class="method-step__io" markdown="1">

**输入**：场景图序列及每一步的物理约束 $\mathcal{P}_n$。<br>
**输出**：带有物理量的场景图 $\mathcal{G}_n^*=(\mathcal{V}_n^*,\mathcal{R}_n^*)$，以及事件 $e_n=\{\mathcal{G}_{n-1}^*\rightarrow\mathcal{G}_n^*,\mathcal{P}_n\}$ 组成的完整事件链。

</div>

**直观理解**：这一步把“倾斜一些”“移动一段距离”等模糊说法尽量变成与具体对象绑定的方向和幅度，避免只靠语言模型凭印象描述物理过程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 事件路由关键帧生成与软视觉约束

VLM 根据 $\mathcal{G}_{n-1}^*\rightarrow\mathcal{G}_n^*$ 识别视觉变化类型并产生空间提示与文本编辑条件，SAM 定位受影响区域，图像编辑器递归生成 $\mathbf{v}_n$；关键帧经 VAE 编码和时间插值后，其相对 $\widetilde{\mathbf{v}}_0$ 的特征偏移以残差形式注入对应视频潜变量。

<div class="method-step__io" markdown="1">

**输入**：增广事件链、由 $\mathcal{G}_0^*$ 通过文生图模型生成的初始关键帧 $\mathbf{v}_0$，以及上一事件的关键帧 $\mathbf{v}_{n-1}$。<br>
**输出**：事件边界关键帧链 $\mathbf{v}_0\xrightarrow{e_1}\cdots\xrightarrow{e_N}\mathbf{v}_N$，以及带平滑关键帧引导的噪声视频特征 $\widetilde{\mathbf{Z}}$。

</div>

**直观理解**：系统先画出每个阶段结束时应该呈现的画面，再让中间帧逐渐靠近下一个状态；注入的是“相对起点发生了什么变化”，而不是强行复制整张关键帧，因此既提供方向又给视频模型保留生成空间。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 正反物理语义构造与扩散去噪

系统删除未变化背景和重复对象引用，把重要事件变化及粗粒度程度词压缩为 $\mathcal{W}_+^*$；同时对每个事件的关键物理量实施最小违反，如反转速度方向，得到 $\mathcal{W}_-^*$，并将两类文本编码用于对比式分类器无关引导。

<div class="method-step__io" markdown="1">

**输入**：事件链、用户原始描述 $w$、正向事件描述、逐事件构造的反事实描述，以及视觉引导潜变量 $\widetilde{\mathbf{Z}}$。<br>
**输出**：经迭代去噪和解码得到的物理可信视频 $\mathbf{V}$。

</div>

**直观理解**：正向提示告诉模型正确过程应该长什么样，负向反事实则明确指出需要避开的错误，例如液体沿倾斜容器向上流；二者的预测差异被放大，以抑制看似连贯但违反物理规律的运动。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 关键帧插值、累计变化与残差注入

$$
\widetilde{\mathbf{v}}_{\tau_n}=(1-\lambda_{\tau_n})\widetilde{\mathbf{v}}_{n-1}+\lambda_{\tau_n}\widetilde{\mathbf{v}}_n,\quad \mathbf{d}_{\tau_n}=\widetilde{\mathbf{v}}_{\tau_n}-\widetilde{\mathbf{v}}_0=\sum_{m=0}^{n-2}(\widetilde{\mathbf{v}}_{m+1}-\widetilde{\mathbf{v}}_m)+\lambda_{\tau_n}(\widetilde{\mathbf{v}}_n-\widetilde{\mathbf{v}}_{n-1}),\quad \widetilde{\mathbf{z}}_{\tau_n}=\mathbf{z}_{\tau_n}+\beta\mathbf{d}_{\tau_n}
$$

**符号说明**

- $\mathbf{v}_n$：第 n 个事件边界处生成的关键帧
- $\widetilde{\mathbf{v}}_n$：关键帧经图像 VAE 编码后的潜空间特征
- $\tau_n$：第 n-1 与第 n 个关键帧之间的时间位置
- $\lambda_{\tau_n}$：该时间位置的线性插值比例，取值位于 0 到 1
- $\mathbf{d}_{\tau_n}$：当前位置相对初始关键帧特征的累计变化量
- $\mathbf{z}_{\tau_n}$：注入关键帧引导之前的噪声视频潜特征
- $\widetilde{\mathbf{z}}_{\tau_n}$：注入残差引导之后的噪声视频潜特征
- $\beta$：控制视觉残差引导强度、并随去噪推进逐渐增大的系数

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分在相邻关键状态之间构造平滑潜特征；第二部分把当前位置写成相对初始状态的累计变化，因此已经完成的事件不会在后续区间被遗忘；第三部分将该变化加到视频扩散潜变量上。该设计约束的是“视频应如何逐步变化”，而不是把某张关键帧作为硬条件覆盖生成内容。<br>
**原文位置**：Section III-C，Equations (6)–(8)

</div>

</div>

<div class="equation-block" markdown="1">

#### 物理正向—反事实负向分类器无关引导

$$
\mathbf{W}_{+}=\psi_{\mathrm{txt}}(\mathcal{W}^{*}_{+}),\quad \mathbf{W}_{-}=\psi_{\mathrm{txt}}(\mathcal{W}^{*}_{-}),\quad \hat{\boldsymbol{\epsilon}}_{\theta}=\boldsymbol{\epsilon}_{\theta}(\widetilde{\mathbf{Z}}_{\tau_z},\tau_z,\mathbf{W}_{-})+\gamma\left[\boldsymbol{\epsilon}_{\theta}(\widetilde{\mathbf{Z}}_{\tau_z},\tau_z,\mathbf{W}_{+})-\boldsymbol{\epsilon}_{\theta}(\widetilde{\mathbf{Z}}_{\tau_z},\tau_z,\mathbf{W}_{-})\right]
$$

**符号说明**

- $\mathcal{W}^{*}_{+}$：由用户描述和事件链压缩得到的物理增强正向文本
- $\mathcal{W}^{*}_{-}$：通过违反事件物理约束构造的反事实负向文本或文本集合
- $\psi_{\mathrm{txt}}$：视频生成模型使用的文本编码器
- $\mathbf{W}_{+},\mathbf{W}_{-}$：正向文本与反事实负向文本的嵌入
- $\widetilde{\mathbf{Z}}_{\tau_z}$：扩散时间步 tau_z 上、已接受关键帧残差引导的视频潜变量
- $\boldsymbol{\epsilon}_{\theta}$：参数为 theta 的去噪网络所预测的条件噪声
- $\hat{\boldsymbol{\epsilon}}_{\theta}$：结合正向与反事实条件后的最终引导噪声预测
- $\gamma$：分类器无关引导尺度，控制正负预测差异的放大程度

<div class="equation-explanation" markdown="1">

**直观理解**：该式先以反事实条件的噪声预测为基准，再放大“正确物理描述下的预测”与“错误物理描述下的预测”之间的差值。因而去噪方向不仅追求与正向描述一致，也主动远离专门构造的物理违规模式。<br>
**原文位置**：Section III-D，Equations (9)–(10)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文所给方法章节没有提出新的参数训练损失，也未描述对视频扩散模型、LLM、VLM、SAM、VAE 或图像编辑器进行联合微调；因此这里不存在可据原文复述的新增训练目标。式 (10) 是推理阶段的噪声预测组合规则，而不是训练损失：它在每个扩散时间步利用正向条件 $\mathbf{W}_+$ 与反事实负向条件 $\mathbf{W}_-$ 改变采样方向；式 (6)–(8) 同样是在采样时修改潜变量。就所给章节而言，该框架应理解为由预训练模型、检索工具和符号计算工具构成的推理期编排方法，而不能据此声称作者训练了一个新的端到端 PPVG 模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Physics-driven Event Chain Reasoning（PECR）**

PECR 以场景图演化而非自由文本短语表示物理过程：每个 $\mathcal{G}_n$ 是事件边界处的对象—关系配置，$\mathcal{P}_n$ 是从上一配置转移到下一配置的物理依据。模块进一步检索适用公式、解析公式变量、将变量绑定到具体节点或关系，并检查相邻场景图中的数值变化是否违背 $\mathcal{P}_n$；最终事件 $e_n$ 同时包含定性配置变化和定量物理变化。需要注意，候选图评分、公式查询和符号绑定均依赖 LLM 或外部工具，因此这里得到的是受物理知识约束的推理结果，而非数值模拟器给出的严格轨迹。

> 直观理解：普通提示只给出物理现象的名称，PECR 则把它改写成可执行的状态清单，并用公式检查变化的方向和幅度。它的核心价值是为后续视觉生成提供明确的中间状态，而不是让视频模型从起点直接猜到终点。

**2. Transition-aware Routed Keyframe Conditioning（TRKC）**

TRKC 不使用同一种编辑方式处理所有事件，而是把事件路由到颜色变化、纹理变化、位移、形变或默认增删元素五类算子。颜色算子提供局部 RGB 先验；纹理算子用边界框与分割区域的交集限定覆盖范围；位移算子估计二维平移和旋转并补全空缺背景；形变算子以缩放率、轮廓偏移等参数重绘掩码；这些编辑均由 VLM 生成条件、SAM 提供区域约束、Qwen-Image-Edit 生成后继关键帧。之后，关键帧 VAE 特征按时间线性插值，并把相对初始关键帧的累计变化残差注入去噪潜变量，引导强度 $\beta$ 随去噪过程逐渐增加。

> 直观理解：颜色改变、物体移动和物体变形需要不同的控制信号，统一编辑器容易改错位置或破坏形状，因此该模块先判断“变化属于哪一类”再调用合适工具。软残差引导则像给动画补间提供若干路标：模型被要求经过正确状态，但不被固定成关键帧的机械复制。

**3. Physics-injected Contrastive Semantic Guidance（PCSG）**

PCSG 先逐事件比较相邻场景图的节点和边，只保留可观察的关键变化，并将难以直接视觉化的精确数值转成“浅色”等粗粒度程度词；各事件描述去重压缩后与原始描述合成正向条件 $\mathcal{W}_+^*$。负向条件 $\mathcal{W}_-^*$ 通过干预物理量构造：系统选出每个事件中对 $\mathcal{P}_n$ 最关键的最小变化，并令其违反约束，但保持对象和背景不变；每个反事实仅针对当前事件生成，不回写场景图或传播到相邻事件。

> 直观理解：若只告诉模型“应该发生什么”，模型仍可能用错误的运动方式达到相似终态。PCSG 同时给出与正确现象尽量接近、但在关键物理量上出错的反例，使引导信号更集中地辨别物理正确与物理错误，而不是仅区分相关与无关内容。

**训练与推理**

训练过程：所给方法章节未报告额外训练或参数更新流程，相关训练数据、优化器、学习率及损失函数均原文未明确报告。推理过程：首先解析 $w$ 得到 $\mathcal{G}_0$，递归推断 $\mathcal{P}_n$ 并选择后继场景图；随后检索公式、解析和绑定变量、求解或查询物理量，并通过跨事件一致性检查得到 $\mathcal{G}_n^*$ 与 $e_n$。系统以 $\mathcal{G}_0^*$ 生成 $\mathbf{v}_0$，再针对每个事件由 VLM 产生编辑条件、SAM 提供局部掩码，并由路由后的图像编辑算子递归生成 $\mathbf{v}_n$。全部关键帧被 VAE 编码、按时间插值并转成累计变化残差，在视频扩散的相应时刻注入潜变量；与此同时，事件链被压缩为 $\mathcal{W}_+^*$，各事件的物理量被最小化干预以形成 $\mathcal{W}_-^*$。最后，在每个扩散时间步按式 (10) 合成噪声预测，迭代去噪后将潜变量解码为视频 $\mathbf{V}$。

**复现信息**

公平理解该方法所必需的组件包括：LLM 负责场景图推理、公式查询改写、变量—对象绑定、事件描述压缩和反事实生成；外部在线来源提供候选物理公式，符号代数引擎负责解析公式变量；T2I 模型生成初始关键帧，VLM 判断视觉变化并估计 RGB、边界框、平移、旋转、缩放率或轮廓偏移等编辑条件，SAM 分割受影响区域，Qwen-Image-Edit 生成后继关键帧；VAE 与视频扩散模型分别承担潜空间编码和最终去噪。公式检索在最佳候选相似度低于预设阈值时会改写查询并重试，但阈值数值、相似度模型、LLM/VLM 的具体版本、扩散主干、采样器、去噪步数、$\beta$ 的增长日程和引导尺度 $\gamma$ 在所给节选中均原文未明确报告，因此不能从该节选独立完成严格复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- PhyGenBench：包含160条语言描述，覆盖力学、光学、热学和材料四个领域的27条物理规律。它是综合评测与全部消融实验的主要基准，用于检验关键物理现象是否出现、事件顺序是否正确以及视频整体是否自然；原文未明确报告训练集、验证集或测试集划分。
- VideoPhy：包含688条经人工核验的提示词，按固体—固体、固体—流体和流体—流体三类交互组织。该基准用于区分“是否遵循提示语义”与“交互过程是否符合现实物理”，因而重点检验物体状态和关系随事件推进的变化；原文未明确报告数据划分。
- PhyWorldBench：实验采用物体运动与运动学、交互动力学、形变与弹性、能量守恒、流体与粒子动力学、光照与阴影等基础物理类别，并额外采用故意违反现实规律的反物理类别。其作用是同时测试模型遵循正常物理规律和忠实执行用户指定反物理过程的能力；所给章节未报告样本总量与数据划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Physical Commonsense Alignment（PCA）**

PhyGenBench的综合指标，同时考虑关键现象检测、物理事件顺序验证和整体自然度；因此它不仅检查画面是否好看，也检查必要物理阶段是否出现且顺序合理。 （越高越好，因为更高分表示生成视频在现象覆盖、因果次序和自然性上的综合一致性更强。）

</div>
<div class="metric-item" markdown="1">

**Semantic Adherence（SA）**

检查提示中的对象、动作或Basic Standards是否在视频帧中得到语义落实。在反物理测试中，高SA表示模型忠实呈现用户要求，而不等同于过程符合现实规律。 （越高越好，因为更高分表示视频更完整、准确地实现输入描述。）

</div>
<div class="metric-item" markdown="1">

**Physical Commonsense（PC）及联合SA-PC**

PC检查动作和物体属性是否符合现实物理规律，或在PhyWorldBench中是否满足相应Key Standards；联合SA-PC要求语义与目标物理现象同时成立，因而比单独SA或PC更严格。对于反物理类别，较高分表示更好地执行预定义的反物理指令，并不表示出现了更多非预期物理错误。 （越高越好，因为它表示视频更符合该基准指定的关键物理过程，并在联合指标中同时满足语义要求。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### PhyGenBench：以CogVideoX-5B为骨干，与未增强骨干及多种物理感知方法比较四个基础物理领域的PCA。

<div class="result-value" markdown="1">

加入所提框架后，力学、光学、热学和材料PCA分别达到70.0%、78.7%、76.7%和64.2%，平均72.5%；未增强CogVideoX-5B平均为45.0%，对应提升27.5个百分点。作者据此主张事件中心条件能跨物理领域改善合理性。

</div>

这说明改进并非只集中在一个容易类别，且在同一CogVideoX-5B骨干上的增幅较大。尤其热学与材料变化通常需要展示渐进中间状态，结果与方法设计目标一致。不过PCA由自动评估流程综合得到，单个平均分不能证明每段视频都严格满足守恒定律，也不能排除推理模型、图像编辑器等外部组件带来的贡献。

<div class="result-source" markdown="1">

来源：表I；IV-B节“Performance Comparisons on PhyGenBench”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table I, with CogVideoX-5B [35], our framework achieves PCA scores of 70.0%, 78.7%, 76.7%, and 64.2% in mechanics, optics, thermal, and material, respectively, yielding the highest average score of 72.5%. Applying our framework to CogVideoX-5B [35], Wan2.1-1.3B-VACE [22], Wan2.1-14B [22], and Wan2.2-14B [22] raises their average scores by 27.5, 10.0, 30.8, and 18.1, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### VideoPhy：以CogVideoX-5B为骨干，评测固体—固体、固体—流体和流体—流体交互的联合SA-PC。

<div class="result-value" markdown="1">

所提方法在三类交互上的联合SA-PC分别为50.0%、63.0%和63.8%，总体58.5%，高于PhysHPO的总体45.9%；在Wan2.2-14B上也把总体分数从39.2%提高到57.3%。

</div>

联合分数要求视频既呈现提示中的交互，又展示相应物理响应，因此结果支持事件级对象状态与关系绑定有助于材料混合、液体位移等动态过程。跨CogVideoX和Wan骨干均有提升，也削弱了“只对单一生成器有效”的解释；但该结果仍是基准评估器判断，不能单独证明模型内部真正学习了可泛化的物理定律。

<div class="result-source" markdown="1">

来源：表II；IV-B节“Performance Comparisons on VideoPhy”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table II, our approach improves physical interaction modeling across various evaluated categories. With CogVideoX-5B [35], our approach achieves SA-PC scores of 50.0%, 63.0%, and 63.8% for solid-solid, solid-fluid, and fluid-fluid interactions, respectively, yielding an overall score of 58.5% and surpassing the overall score of 45.9% achieved by PhysHPO [38]. When applied to Wan2.2-14B [22], our approach increases the overall score from 39.2% to 57.3%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### PhyWorldBench：分别测试正常基础物理与用户明确要求的反物理过程，并比较三个底层视频生成器加入框架前后的联合SA-PC。

<div class="result-value" markdown="1">

CogVideoX-5B加入框架后，基础物理联合SA-PC由19.2%升至31.4%，反物理由0.0%升至5.7%；Wan2.2-14B加框架后分别达到36.8%和7.6%，为表中两类最高结果。

</div>

基础物理提升表明框架更容易实现预期因果演化；反物理提升则表明它也能遵循用户明确指定、但违背现实的事件序列。后一点检验的是指令忠实性而非现实物理正确性，所以不能把7.6%解释成更强的现实物理合理性；反物理绝对分数仍很低，也显示此类精确控制依然困难。

<div class="result-source" markdown="1">

来源：表III；IV-B节“Performance Comparisons on PhyWorldBench”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table III, our approach consistently improves the SA-PC score across all evaluated video generators under both fundamental and anti-physics scenarios. The most substantial improvements are obtained with CogVideoX-5B [35], increasing the SA-PC scores from 19.2% to 31.4% for fundamental physics and from 0.0% to 5.7% for anti-physics. When applied to Wan2.2-14B [22], our approach achieves the best performance in both categories, with scores of 36.8% and 7.6%, respectively.

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

- 未增强的视频基础模型，包括CogVideoX-5B、Wan2.1-1.3B-VACE、Wan2.1-14B和Wan2.2-14B。它们与“+ Ours”共享底层生成器，可直接检验收益是否来自所提条件框架，而非更换更强骨干。
- 提示或引导式物理视频生成方法PhyT2V与SGD。它们代表在现有生成器上加入物理知识或采样引导的路线，用于判断显式事件链、关键帧和反事实语义引导是否优于较整体化的物理条件。
- 偏好优化方法PhysHPO、VideoDPO、Vanilla DPO和PhyGDPO。它们通过物理偏好或奖励优化生成行为，是判断免训练推理时条件框架能否与训练型对齐方法竞争的有意义参照。
- PhysVideo、VideoREPA与WISA等物理感知生成方法。它们分别构成VideoPhy定量比较或开放源代码定性比较的直接同类基线，用于检验材料混合、流体操控及长事件链中的过程完整性。

**实验想回答的问题**

- 所提事件中心条件框架能否在不同视频生成骨干、物理领域与物质交互类型上稳定提高生成视频的物理合理性，而非只适用于某一模型或少数现象？
- 性能提升是否分别来自事件边界关键帧约束、正反事实语义引导以及物理事件链推理中的一致性检查、公式推理和物理量绑定？

**实验实现**

该框架不额外训练底层视频生成模型，并使用各骨干官方推理配置。默认以DeepSeek-Pro完成推理与验证，最大输出为4096个token；物理事件链推理每步产生3个后继场景图候选，每个现象最多推断5个事件，物理量违反约束时最多重推3轮。关键帧模块使用Qwen-Image-Edit进行40步采样，并借助SAM获得待编辑物体掩码；残差引导系数$\beta$随去噪按余弦计划由0增至1。分类器自由引导尺度$\gamma$按骨干设为4.0至6.0。所有实验在单张80 GB NVIDIA H100上进行。定量评测覆盖四个互补基准，但受列表限制，此处仅展开三个；另有Physics-IQ图像条件续写实验，其输入为3秒条件片段的最后一帧，并以空间、时空、影响范围及过程误差组合计分。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 在PhyGenBench和CogVideoX-5B设置下保持物理事件链推理模块PECR，分别移除过渡感知路由关键帧模块TRKC或物理注入对比语义引导模块PCSG。 | 完整系统平均PCA为72.5%；移除TRKC后降至66.9%，下降5.6个百分点；移除PCSG后降至69.2%，下降3.3个百分点。TRKC移除造成更大平均退化。 | 该对照隔离了两种互补条件：TRKC用相邻事件边界关键帧明确“中间状态应长什么样”，PCSG用物理正提示与反事实负提示规定“应朝哪种动态发展并避开什么”。数值与图8的失败案例相符：无TRKC时渐进变化不足，无PCSG时可能出现与提示无关的倒入和火焰。不过两种删减均保留PECR，因而只能说明它们在当前组合中的边际作用，不能据此断言TRKC在所有骨干和指标上都比PCSG重要。 | 表V（正文误写为Table 8）；图8；IV-D节“Effect of TRKC and PCSG Modules”<br><span class="experiment-evidence">As shown in Table 8, removing TRKC or PCSG decreases the average score from 72.5% to 66.9% and 69.2%, respectively.</span> |
| PhyGenBench上的PECR累积式消融：从完整PECR开始，依次去除相邻场景图一致性检查、公式推理和显式物理量。 | 完整PECR平均PCA为72.5%；累积去除一致性检查后为71.9%，再去除公式推理后为71.7%，再去除物理量后为71.0%，总下降1.5个百分点。 | 该实验检验PECR是否只需语言化事件分解，还是还需要数值物理约束。逐步下降支持一致性验证、公式依据和对象级物理量均有贡献，其中全部移除后的累计影响最明显。但各行是累积删除而非彼此独立的单因素实验，因此不能直接把相邻两行差值当成各组件的纯因果贡献，也无法判断组件间交互。 | 表VI；图9；IV-D节“Effect of Physics-driven Reasoning in PECR Module”<br><span class="experiment-evidence">Full PECR \| 70.0 \| 78.7 \| 76.7 \| 64.2 \| 72.5; - Consistency Check \| 69.2 \| 78.7 \| 75.6 \| 63.3 \| 71.9; - Formula Reasoning \| 71.7 \| 78.0 \| 74.4 \| 61.7 \| 71.7; - Physical Quantities \| 69.2 \| 78.0 \| 73.3 \| 62.5 \| 71.0.</span> |

**定性案例**

- 长事件链案例中，同一提示要求冰块落入热茶后经历下沉、到达最低点、稳定上浮并逐渐融化。图7显示WISA主要呈现早期下落与飞溅，而所提方法覆盖后续漂浮和融化。该案例直观说明事件分解可减少生成器只聚焦最显著碰撞、跳过后续阶段的问题；但它是挑选的定性示例，事件标注仅用于展示，不能替代大规模人工盲评，也不能证明所有长链现象都能完整生成。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution is a physics-conditioned framework for generating videos with causally coherent and physically plausible event transitions.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`28df5faa63f75a2320afc133eb51e1b781e5958eaa0809d6c4432e867fcde9e8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
