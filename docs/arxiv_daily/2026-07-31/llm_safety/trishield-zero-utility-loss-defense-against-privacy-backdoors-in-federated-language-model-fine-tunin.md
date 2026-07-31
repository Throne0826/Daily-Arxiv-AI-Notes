---
title: "[论文解读] TriShield: Zero-Utility-Loss Defense Against Privacy Backdoors in Federated Language Model Fine-Tuning via Orthogonal Gradient Projection and Optimizer State Entanglement"
description: "[arXiv 2607.27940][LLM 安全] 本文针对恶意参数服务器在联邦大语言模型微调中预埋神经元级隐私后门的问题，提出完全在客户端运行的三层防御思路，目标是在不依赖服务器配合且不损害主任务效用的前提下阻断基于梯度的样本重建。"
arxiv_id: "2607.27940"
announcement_date: "2026-07-31"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.040673+00:00"
source_sha256: "8e88007cd26c52551362f1b8a8bbc1ad7524126c804519229e35d610bcb311f6"
tags:
  - "LLM 安全"
  - "LLM 其他"
  - "联邦微调"
  - "参数高效微调"
  - "隐私后门"
  - "梯度反演"
  - "恶意参数服务器"
  - "正交梯度投影"
  - "优化器状态"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2607.27940</p>

# TriShield: Zero-Utility-Loss Defense Against Privacy Backdoors in Federated Language Model Fine-Tuning via Orthogonal Gradient Projection and Optimizer State Entanglement

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Wei, Cheng</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27940) · [PDF 下载](https://arxiv.org/pdf/2607.27940) · **关键词** 联邦微调, 参数高效微调, 隐私后门, 梯度反演, 恶意参数服务器, 正交梯度投影, 优化器状态<br>


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

本文针对恶意参数服务器在联邦大语言模型微调中预埋神经元级隐私后门的问题，提出完全在客户端运行的三层防御思路，目标是在不依赖服务器配合且不损害主任务效用的前提下阻断基于梯度的样本重建。

**不用术语来说**：联邦微调虽然不要求客户端上传原始文本，但客户端必须接收服务器下发的模型并返回训练更新；如果服务器暗中改造模型中的少量适配器神经元，这些更新就可能像带有隐藏内容的回执一样泄露训练文本。客户端看到的训练过程和模型效果仍可保持正常，因此仅仅“不共享原始数据”并不能消除隐私风险。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出 TriShield：一种无需服务器合作、无需改变联邦通信协议的客户端三层防御框架，分别在训练前检查参数异常、训练中利用 Adam/AdamW 状态混合不同虚拟步骤的梯度，并在上传前将更新投影到主任务语义子空间。
- 作者试图同时建立功能保持与隐私阻断保证：投影保留与微调目标相关的梯度方向，而优化器状态纠缠和正交投影共同破坏 NeuroImprint 所需的单样本解析反演条件。上述保证是论文作者的理论主张，仍需结合完整定理假设和证明核验。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究联邦大语言模型参数高效微调中的隐私泄露。标准流程由服务器下发冻结的基础模型与可训练的 PEFT 适配器，客户端仅在本地私有数据上更新少量适配器参数，再上传参数增量；这种机制避免直接共享原始文本，却不保证更新本身不泄露数据。本文关注更强的恶意服务器场景：服务器可在下发的适配器中预埋“隐私后门”，使特定神经元分别记录训练样本，并在收到客户端更新后通过梯度反演恢复文本。因而安全目标不仅是隐藏原始数据，还要在不依赖服务器诚实、尽量不损害主任务性能的前提下，阻断适配器更新成为样本信息的隐蔽传输通道。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**联邦学习与联邦微调**

联邦学习让多个客户端在本地数据上训练，只向服务器发送模型更新，由服务器聚合得到共享模型。本文采用恶意服务器威胁模型，因此“数据不离开设备”并不等于隐私安全：服务器可能操纵下发模型，使上传更新泄露训练样本。

</div>
<div class="concept-item" markdown="1">

**参数高效微调（PEFT）**

PEFT 冻结大模型主体，只训练 LoRA 或 adapter 等小型参数模块，从而降低客户端计算量和通信量。本文的攻击面正是这些可训练适配器：恶意服务器可预先篡改其中的行或神经元，将其变成按样本分配的记忆槽。

</div>
<div class="concept-item" markdown="1">

**梯度反演与隐私后门**

梯度反演是从参数梯度或更新中推回训练输入；NeuroImprint 进一步通过预埋结构，让某个记忆神经元只被一个样本更新，从而利用权重梯度与偏置梯度之比进行闭式恢复。所谓隐私后门不是改变模型预测的传统后门，而是把客户端更新改造成编码私有样本的隐蔽信道。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

在一轮联邦 PEFT 中，服务器向客户端分发基础模型参数 $\theta_0$ 与初始适配器 $\phi_0$；客户端 $i$ 在私有数据集 $D_i$ 上进行 $E$ 个本地训练轮次，得到 $\phi_i$，并上传增量 $\Delta\phi_i=\phi_i-\phi_0$，服务器再聚合各客户端更新。本文假设基础模型保持冻结，而服务器可能恶意篡改适配器：它为样本 $x_j$ 配置专用记忆神经元 $r_j$，利用单次激活、线性更新及 LayerNorm 的归一化不变性，使该神经元的权重梯度和偏置梯度保留可解析的样本表示；服务器收到更新后可按 $\hat{x}_j=\nabla W_{r_j}/\nabla B_{r_j}$ 恢复输入。防御部署在客户端侧，其输入是服务器下发的模型与适配器、本地训练数据及训练过程中产生的梯度，预期输出仍是协议兼容的适配器更新；核心要求是在不需要服务器配合、不增加通信轮次和不改变基础架构的条件下，消除 NeuroImprint 式可恢复信息，同时保留主任务所需更新。该问题依赖攻击的三项关键假设：每个记忆神经元恰好接收一次样本更新，优化器状态不跨步骤混合该神经元的梯度，以及后续 LayerNorm 的归一化不变性成立。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\theta_0$**

服务器下发并在 PEFT 中保持冻结的基础模型参数。

</div>
<div class="notation-item" markdown="1">

**$\phi_i$**

客户端 $i$ 完成本地训练后的 PEFT 适配器参数。

</div>
<div class="notation-item" markdown="1">

**$\Delta\phi_i=\phi_i-\phi_0$**

客户端 $i$ 上传给服务器的适配器参数增量。

</div>
<div class="notation-item" markdown="1">

**$\hat{x}_j=\nabla W_{r_j}/\nabla B_{r_j}$**

NeuroImprint 对样本 $x_j$ 的闭式重建，其中 $\nabla W_{r_j}$ 与 $\nabla B_{r_j}$ 分别是记忆神经元 $r_j$ 的权重梯度和偏置梯度。

</div>

</div>

**直接相关的工作**

- **NeuroImprint**: 本文直接防御的攻击。该方法由恶意服务器在 PEFT 适配器中预置按样本分配的记忆神经元，并设法保证每个神经元至多由一个样本更新，使服务器能够利用权重梯度与偏置梯度的比例解析恢复客户端文本；本文将其单次更新和梯度可分离条件视为需要破坏的核心攻击基础。
- **Gradient Projection Memory（GPM）**: GPM 原本用于持续学习，通过把新梯度投影到既有任务子空间的正交补来减少灾难性遗忘。本文借用子空间投影思想但反转目标：保留当前主任务语义子空间内的更新，并去除子空间外可能承载记忆后门信息的分量。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在采用 LoRA 或适配器层等参数高效微调方法的联邦学习中，基础模型被冻结，客户端只训练少量适配器参数。参数服务器既负责下发初始模型，又能收集客户端更新，因此可以预先把某些适配器神经元改造成专用记忆槽。NeuroImprint 进一步利用归一化不变性，使每个记忆神经元至多接收一个样本的更新，服务器随后可通过权重梯度与偏置梯度的比值解析恢复文本。原文称该攻击在多种语言模型上达到 $59\%$ 至 $79\%$ 的重建成功率，同时不降低模型效用，因而难以由常规性能监控发现。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **客户端梯度扰动：局部差分隐私与梯度裁剪**：局部差分隐私在客户端上传前向梯度加入高斯或拉普拉斯噪声，以降低单个样本对输出的可辨识度；论文给出的噪声尺度关系为 $\sigma^2=O(1/\epsilon^2)$，其中 $\epsilon$ 是隐私预算。梯度裁剪则限制更新的范数或幅度，试图压制异常大的泄露信号。
- **服务器端异常检测与拜占庭鲁棒聚合**：FLTrust、FLAME 等方法由服务器评估客户端更新是否异常；Krum、Trimmed Mean 等鲁棒聚合方法则削弱偏离多数分布的客户端更新，主要用于防御恶意或失常客户端。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 局部差分隐私必须加入足够强的噪声才能掩盖私有梯度；原文称在实际隐私预算 $\epsilon<1$ 时，语言任务性能会下降 $5\%$ 至 $20\%$。梯度裁剪也缺乏针对性，因为 NeuroImprint 可按比例缩放记忆适配器行，使后门神经元更新在幅度上与正常更新难以区分。其后果是客户端在隐私与任务效用之间承受明显权衡，或者裁剪后仍然泄露数据。
- 服务器端检测隐含服务器可信这一前提，但该威胁模型中的攻击者正是服务器；拜占庭鲁棒聚合关注异常客户端，而非服务器预埋在正常模型中的异常神经元。因此，这些方法的观察层级和信任假设均与 NeuroImprint 不匹配，无法直接保护诚实客户端。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方案尚未同时满足四项要求：防御恶意服务器预植的神经元级隐私后门、完全由客户端执行、不依赖额外通信或服务器配合，并在阻断单样本梯度反演时保留主任务所需的训练信号。尤其缺少一种能主动破坏 NeuroImprint 的“单个记忆槽只对应一个样本”这一解析可逆结构，而非仅对上传梯度增加噪声或检查其幅度的方法。

</div>
<div markdown="1"><span>核心问题</span>

客户端能否在收到可能被恶意篡改的 PEFT 模型后，通过训练前识别参数痕迹、训练中让多个步骤的梯度在优化器状态内不可分离地混合，并在上传前删除主任务子空间之外的更新分量，从而使 NeuroImprint 式闭式重建失效，同时不牺牲联邦微调的任务效用且不改变通信协议？

</div>
<div markdown="1"><span>作者直觉</span>

NeuroImprint 能解析恢复样本，是因为攻击者人为建立了近似“一槽一条样本”的干净对应关系，使权重梯度与偏置梯度之比仍携带可解码内容。TriShield 的切入点是依次破坏这条泄露链：先寻找下发参数中的记忆槽特征；再借助 Adam/AdamW 的动量状态，把不同虚拟步骤的梯度混合，使服务器难以把上传量归因于某一个样本；最后以奇异值分解得到主任务语义子空间，只保留沿该子空间的更新，并去除可能承载专用记忆的正交分量。通俗地说，它不是用随机噪声淹没秘密，而是保留完成任务需要的方向，同时拆散并删除后门赖以编码样本的方向。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TriShield 是部署在联邦微调客户端上的三层确定性防御封装。输入是服务器下发的全局模型与 PEFT 适配器参数 $\phi_0$、客户端私有数据 $D_i$，以及少量公开且与任务领域相近的辅助数据 $D_{aux}$；客户端依次检查并重置可疑记忆神经元、用辅助梯度预热 Adam/AdamW 的内部状态、正常执行本地微调，再把最终适配器更新投影到公开数据估计的任务梯度子空间，输出净化后的更新 $\Delta\phi_i^*$ 供服务器按原有 FedAvg 协议聚合。整个过程不要求服务器配合，也不增加通信轮次。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 参数伪迹检测与适配器净化（PAD）

逐行计算 $W_A$ 的行内方差以及该行与其他行的最大相关系数；若方差低于 $\tau_{var}=10^{-4}$ 或相关系数高于 $\tau_{corr}=0.95$，便将该行判为可疑记忆神经元，使用 Kaiming 正态初始化重置权重，并以均值为 $0$、标准差为 $0.02$ 的正态分布重置对应偏置。

<div class="method-step__io" markdown="1">

**输入**：服务器下发的适配器 $\phi_0$，具体包括待检查的权重矩阵 $W_A$、相关权重或偏置参数。<br>
**输出**：净化后的初始适配器 $\phi_0^{clean}$ 及可疑行重置标记。

</div>

**直观理解**：NeuroImprint 需要提前布置形状异常且彼此相似的参数行，为不同样本准备专用“记忆槽”。PAD 像训练前的参数安检，先拆除最明显的记忆槽，但作者仍假定后两层负责处理漏检或变体攻击。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 有状态虚拟迭代（SVI）与本地微调

先保存适配器快照，并在 $D_{aux}$ 上执行默认 $K=3$ 次虚拟前向与反向计算：只用虚拟梯度更新优化器的一阶、二阶状态 $m_k$ 和 $v_k$，每次均保持或恢复适配器权重为快照值；随后保留预热状态 $(m_K,v_K)$，在 $D_i$ 上正常执行真实本地微调。

<div class="method-step__io" markdown="1">

**输入**：净化后的 $\phi_0^{clean}$、公开辅助数据 $D_{aux}$、客户端私有数据 $D_i$，以及 Adam 或 AdamW 优化器。<br>
**输出**：完成私有数据微调后的原始本地适配器更新 $\Delta\phi_i$，其真实样本梯度已经与客户端未上传的优化器状态混合。

</div>

**直观理解**：原攻击依赖某个神经元只更新一次，从而让上传变化量与单个样本嵌入近似成比例。SVI 先向优化器的“历史记忆”中写入公开数据梯度，却不真的改模型，使后续更新不再是单个私有样本梯度的简单线性缩放。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 零效用损失正交投影（ZUOP）

对每个辅助样本计算关于适配器参数的任务梯度，并按列组成矩阵 $G$；对 $G$ 做奇异值分解，取前 $k$ 个左奇异向量构成 $U_k$，再将展平的 $\Delta\phi_i$ 左乘投影矩阵 $U_kU_k^\top$，默认取 $k=\min(0.8\,\mathrm{rank}(G),n-1)$。

<div class="method-step__io" markdown="1">

**输入**：原始本地更新 $\Delta\phi_i$、公开辅助数据 $D_{aux}$，以及投影秩 $k$。<br>
**输出**：位于估计任务子空间内的净化更新 $\Delta\phi_i^*$。

</div>

**直观理解**：公开辅助样本用于估计哪些更新方向真正有助于任务，投影只保留这些方向并删除与之正交的成分。其“零效用损失”并非无条件事实，而依赖真实任务梯度确实落在所估计的前 $k$ 维子空间、记忆梯度与该子空间正交等假设。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 上传与联邦聚合

客户端仅上传 $\Delta\phi_i^*$，不上传 SVI 的 $m_K$、$v_K$、辅助样本梯度或中间状态；服务器继续使用既有 FedAvg 流程聚合各客户端更新。

<div class="method-step__io" markdown="1">

**输入**：净化后的客户端更新 $\Delta\phi_i^*$。<br>
**输出**：按原通信协议更新的全局 PEFT 适配器。

</div>

**直观理解**：防御完全位于客户端，因此通信接口和轮数保持不变。服务器看到的是已经混合并投影的结果，无法直接访问用于解释或逆转混合过程的优化器内部状态。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### SVI 预热状态下的 Adam 更新

$$
\begin{aligned} m_{K+1}&=\beta_1m_K+(1-\beta_1)g_{\mathrm{real}},\\ v_{K+1}&=\beta_2v_K+(1-\beta_2)g_{\mathrm{real}}^2,\\ \Delta\theta_{\mathrm{mem}}&=\alpha\frac{m_{K+1}/\beta_1^c}{\sqrt{v_{K+1}/\beta_2^c}+\epsilon}. \end{aligned}
$$

**符号说明**

- $K$：真实训练前执行的虚拟优化器步骤数，默认值为 3。
- $g_{\mathrm{real}}$：真实私有训练样本对目标记忆神经元产生的梯度；攻击模型中可写成样本嵌入的缩放形式。
- $m_K$：经过 K 次辅助数据虚拟迭代后的一阶动量状态，仅保存在客户端。
- $v_K$：经过 K 次辅助数据虚拟迭代后的二阶矩状态，仅保存在客户端。
- $\beta_1,\beta_2$：Adam 对一阶动量和二阶矩的指数衰减系数。
- $\alpha$：优化器学习率。
- $\beta_1^c,\beta_2^c$：原文更新式中的偏差校正因子记号。
- $\epsilon$：防止分母为零的数值稳定常数。
- $\Delta\theta_{\mathrm{mem}}$：记忆神经元最终产生的参数更新。

<div class="equation-explanation" markdown="1">

**直观理解**：没有预热时，单次 Adam 更新仍可能与样本嵌入保持可利用的比例关系；预热后，分子和分母都含有攻击者看不到的历史状态，因此同一个上传更新可对应多组真实梯度与状态。该式是 SVI 阻断闭式反演的核心，但论文的结论依赖服务器确实无法观察或准确推断这些状态。<br>
**原文位置**：第 IV-B 节，Layer 2: Stateful Virtual Iteration；Theorem 1 前的真实更新推导

</div>

</div>

<div class="equation-block" markdown="1">

#### ZUOP 任务子空间投影与正交消除

$$
\begin{aligned} G&=[\nabla_{\phi}\mathcal{L}(x_1),\ldots,\nabla_{\phi}\mathcal{L}(x_n)]=U\Sigma V^\top,\\ k&=\min\!\left(0.8\,\operatorname{rank}(G),n-1\right),\\ \Delta\phi_i^*&=\operatorname{reshape}\!\left(U_kU_k^\top\operatorname{flatten}(\Delta\phi_i)\right),\\ g_{\mathrm{mem}}\perp\operatorname{col}(U_k)&\;\Longrightarrow\;U_kU_k^\top g_{\mathrm{mem}}=0. \end{aligned}
$$

**符号说明**

- $G$：由 n 个公开辅助样本的适配器梯度按列组成的任务梯度矩阵。
- $x_j$：公开辅助数据中的第 j 个样本。
- $\phi$：参与联邦微调的 PEFT 适配器参数。
- $\mathcal{L}$：用于生成辅助任务梯度的损失函数。
- $U,\Sigma,V$：梯度矩阵 G 的奇异值分解因子，其中 U 的列表示参数空间中的梯度方向。
- $U_k$：U 的前 k 个左奇异向量，张成经验主任务子空间。
- $n$：参与子空间估计的辅助样本数量。
- $\Delta\phi_i$：客户端 i 在投影前得到的本地适配器更新。
- $\Delta\phi_i^*$：投影后上传给服务器的净化适配器更新。
- $g_{\mathrm{mem}}$：攻击者布置的记忆神经元所产生的梯度分量。

<div class="equation-explanation" markdown="1">

**直观理解**：SVD 从公开样本梯度中找出最主要的任务方向，$U_kU_k^\top$ 则把客户端更新正交投影到这些方向。若真实任务梯度位于该子空间，它在投影后不变；若记忆梯度与该子空间严格正交，它会被投影为零，这分别对应论文的效用保持与隐私消除论证。<br>
**原文位置**：第 IV-C 节，ZUOP Algorithm、Theorem 2 与 Theorem 3

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：TriShield 不引入新的联合损失函数，也不改变服务器的 FedAvg 优化目标；客户端仍以原任务损失 $\mathcal{L}_{task}$ 微调适配器。它改变的是优化过程和可上传更新：SVI 在真实训练前只改变 Adam/AdamW 状态，ZUOP 在真实训练后施加约束 $\Delta\phi_i^*\in\mathrm{span}(U_k)$。论文所称“零效用损失”来自条件性投影结论：只有当 $\nabla_\phi\mathcal{L}_{task}\in\mathrm{span}(U_k)$ 时，$U_kU_k^\top\nabla_\phi\mathcal{L}_{task}=\nabla_\phi\mathcal{L}_{task}$ 才能严格成立；实际采用截断秩和有限辅助数据时，这是需由实验验证的近似条件，而不是由算法形式无条件保证。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Parameter Artifact Detector（PAD）**

PAD 利用 NeuroImprint 初始化所需的三类参数伪迹：适配器多行归一化向量近重复、单行元素方差异常接近零，以及相关偏置集中在固定初始化常数附近。算法主要以 $r_{var}<\tau_{var}$ 或 $r_{corr}>\tau_{corr}$ 为触发条件，并对命中行重新初始化；原文声称普通 Kaiming 或截断正态初始化的行内方差通常约为 $10^{-3}$ 至 $10^{-2}$，因而与阈值 $10^{-4}$ 有间隔。

> 直观理解：这一层针对攻击的参数准备阶段，而不是尝试从上传梯度中识别泄露。它能以较低成本破坏已知特征明显的记忆神经元，但检测规则具有攻击特定性，因此不能单独承担对未知初始化模式的完整保证。

**2. Stateful Virtual Iteration（SVI）**

SVI 将模型参数与优化器状态分离处理：虚拟步骤产生 $g_1,\ldots,g_K$ 并递推 Adam 状态，但不让这些步骤形成实际参数更新。真实梯度 $g_{real}$ 到来后，上传参数变化由 $g_{real}$、未知的 $m_K$ 和 $v_K$ 共同经过逐元素归一化产生；作者据此把恢复 $g_{real}$ 描述为欠定的非线性逆问题。

> 直观理解：攻击者原本可以把一次更新当成可直接解码的样本信号，SVI 则在解码前加入只有客户端知道的优化历史。需要注意，这提供的是基于未知状态与欠定性的论证；仅由“存在无限多代数解”并不能自动推出严格的零互信息，攻击者若掌握辅助数据分布或额外先验，仍需通过更完整的安全模型评估。

**3. Zero-Utility Orthogonal Projection（ZUOP）**

ZUOP 将每个辅助样本的适配器梯度向量化后组成 $G\in\mathbb{R}^{d_{param}\times n}$，通过截断 SVD 得到经验任务子空间 $\mathrm{span}(U_k)$，并应用正交投影 $P_k=U_kU_k^\top$。对于 LoRA，原文称分别处理 $A$、$B$ 矩阵，同时在组合更新 $\Delta W=B\cdot A$ 上计算 SVD；普通瓶颈适配器则直接逐权重矩阵投影。

> 直观理解：这一层是最后的物理过滤器：不只让私有信号难以求逆，而是尝试把承载记忆的非任务方向直接置零。效果取决于辅助数据能否覆盖真实任务方向；若领域存在偏移，或攻击把样本编码进保留子空间，论文给出的正交消除结论就不能直接套用。

**训练与推理**

每轮联邦训练开始时，客户端接收服务器给出的基础模型和适配器。客户端先运行 PAD 并重置异常参数行，再建立 Adam/AdamW 优化器，在 $D_{aux}$ 上进行 $K$ 次仅更新优化器状态的虚拟步骤；保持初始适配器权重不变后，携带预热状态在私有数据 $D_i$ 上执行常规本地微调。训练结束后，客户端从 $D_{aux}$ 计算梯度矩阵 $G$，通过截断 SVD 构造投影矩阵，将完整本地更新变换为 $\Delta\phi_i^*$ 并上传，服务器仍按 FedAvg 聚合。TriShield 是训练期防御，原文没有给出独立的推理期净化流程；聚合后的模型按原模型方式推理。

**复现信息**

实现被描述为 HuggingFace PEFT 适配器外层封装，不需要服务器端修改，并面向 LoRA、普通 adapter 和 prefix tuning 等 PEFT 形式。复现时关键设置是 SVI 默认 $K=3$，PAD 使用 $\tau_{var}=10^{-4}$ 与 $\tau_{corr}=0.95$，ZUOP 默认秩比例为 $0.80$；原文特别指出秩比例是敏感参数，设为 $0.95$ 时可能保留更多与攻击向量偶然对齐的方向。辅助数据必须公开、无敏感信息且与私有任务领域相近：正文一般建议使用 200 至 500 个样本，但实验实现实际使用了 32 个领域相近的 ML/NLP 文本样本，因此解读方法时应区分部署建议与实验配置。原文对 GPT-2 配置报告总 GPU 开销低于单轮训练的 $5\%$，但给出的 CPU 分层耗时明显更高；这些复杂度数据说明该方法的主要额外成本来自辅助梯度计算和 SVD，而非通信。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 原文摘录仅出现“Local Verification:”标题，后续数据集名称、规模、训练/验证划分及具体用途均被截断，因此无法可靠报告实验数据集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**重建率**

衡量攻击者成功恢复客户端训练样本的比例，是评估隐私防御有效性的核心指标。该指标需要与成功重建的判定标准共同解释，但摘录未说明判定阈值。 （越低越好；$0\%$表示按论文采用的判定规则，没有测试样本被攻击成功重建。）

</div>
<div class="metric-item" markdown="1">

**训练准确率**

衡量加入防御后模型在训练任务上的预测表现，用于检查隐私保护是否损害模型效用；摘录没有提供具体任务、计算方式或测试集指标。 （通常越高越好；与无防御训练持平意味着未观察到效用损失，但训练准确率本身不能充分证明未知数据上的泛化能力。）

</div>
<div class="metric-item" markdown="1">

**额外GPU计算开销**

衡量TriShield相对原始训练增加的GPU计算成本；摘要以百分比报告，但未说明该比例基于训练时间、FLOPs还是其他统计量。 （越低越好；较低开销意味着防御更容易部署，但不能据此判断显存、通信量或端到端延迟。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### GPT-2与Llama-Guard-3-1B上的全部已测试NeuroImprint攻击变体

<div class="result-value" markdown="1">

作者报告TriShield将NeuroImprint重建率降低到$0\%$。

</div>

按论文的成功判定标准，攻击者在已测试设置中未能恢复任何训练样本。这直接支持TriShield对所测NeuroImprint变体的经验防御效果，但不等于对所有隐私攻击、任意自适应攻击或未测试模型都具有绝对安全性；摘录也未提供样本总数和置信区间，因此无法判断零成功事件对应的统计上界。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments on GPT-2 (117M) and Llama-Guard-3-1B verify that TriShield reduces NeuroImprint reconstruction rate to $\textbf{0\%}$ across all tested attack variants, while maintaining or improving training accuracy, with less than 5\% additional GPU computation overhead.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 启用完整TriShield后的模型训练效用

<div class="result-value" markdown="1">

作者称训练准确率得到保持或提高，因此在其报告的训练准确率口径下没有观察到效用损失。

</div>

这一结果意在说明防御没有通过简单破坏梯度来换取隐私，符合“零效用损失”的设计目标。不过“保持或提高”未附逐数据集数值、测试集结果或误差范围，偶然波动也可能造成小幅提高；因此现有摘录只能支持作者关于训练准确率的经验陈述，不能证明所有下游效用指标均无损。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments on GPT-2 (117M) and Llama-Guard-3-1B verify that TriShield reduces NeuroImprint reconstruction rate to $\textbf{0\%}$ across all tested attack variants, while maintaining or improving training accuracy, with less than 5\% additional GPU computation overhead.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 完整TriShield相对原始联邦微调的计算成本

<div class="result-value" markdown="1">

作者报告额外GPU计算开销低于$5\%$，并称防御不增加通信轮次。

</div>

该结果表明TriShield在所测实现中的额外本地计算较小，且没有通过增加客户端与服务器交互次数来获得防御效果。但摘录没有给出计时方法、硬件、显存开销和不同模型的独立结果，所以不能直接外推到其他设备、批大小或更大模型。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Experiments on GPT-2 (117M) and Llama-Guard-3-1B verify that TriShield reduces NeuroImprint reconstruction rate to $\textbf{0\%}$ across all tested attack variants, while maintaining or improving training accuracy, with less than 5\% additional GPU computation overhead.

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

- 无防御的联邦参数高效微调：用于呈现NeuroImprint攻击下的原始隐私泄露风险；摘要称该攻击可重建$59\%$至$79\%$的客户端训练数据，但所给实验章节摘录未提供对应表格、配置或逐模型结果。
- 局部差分隐私（LDP）：通过在客户端更新中引入随机扰动来限制单个样本的可辨识性，是隐私保护的标准比较对象；作者称其对该攻击无效或会造成不可接受的效用下降，但摘录未给出噪声强度及实验分数。
- 梯度裁剪：通过限制梯度范数抑制异常或高幅度更新，是成本较低的常见防御；其比较意义在于检验仅约束更新幅度能否破坏NeuroImprint的解析反演，然而摘录没有报告裁剪阈值和定量结果。
- 原始NeuroImprint攻击：作为主要攻击基线，它为每个训练样本分配专用记忆神经元，并使每个神经元至多更新一次，从而尝试由上传更新解析恢复训练文本；实验声称覆盖其全部已测试攻击变体，但变体名称与参数未在摘录中给出。

**实验想回答的问题**

- TriShield能否在GPT-2与Llama-Guard-3-1B上阻止不同NeuroImprint攻击变体，使客户端训练数据的重建率降至零？
- TriShield在防止隐私重建的同时，能否保持模型训练效用，并将额外计算开销控制在较低水平？

**实验实现**

实验使用GPT-2与Llama-Guard-3-1B。GPT-2含117M参数、12个Transformer层，模型宽度为$d_{model}=768$，LoRA秩为8；它与原始NeuroImprint论文所测试的模型家族一致，用于较直接的攻击对照。Llama-Guard-3-1B含1.498B参数，在$q\_proj$与$v\_proj$上采用秩为4的LoRA，用于考察方法能否扩展到基于Llama 3架构的十亿参数级因果语言模型。摘要称实验覆盖全部已测试攻击变体，且不增加通信轮次；然而所给摘录缺少数据集详情、客户端数量、联邦轮次、随机种子、超参数、硬件、重复次数、方差和统计检验，因而目前不能完整复现实验，也不能核验各模型上的逐项结果。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Proposes a defense against privacy backdoors and training-data reconstruction attacks in federated LLM fine-tuning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`8e88007cd26c52551362f1b8a8bbc1ad7524126c804519229e35d610bcb311f6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
