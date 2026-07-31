---
title: "[论文解读] HiFloat4 Format for End-To-End Reinforcement Learning Post-Training of Large Language Models"
description: "[arXiv 2607.26515][LLM 效率] 本文研究如何在大语言模型强化学习后训练中让采样与训练全流程均采用FP4，并指出主要障碍是采样侧激活异常值引发的大量下溢及采样—训练策略数值失配，进而以稀疏残差校正缓解该问题。"
arxiv_id: "2607.26515"
announcement_date: "2026-07-30"
primary_category: "llm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T10:14:52.832043+00:00"
source_sha256: "78ca15a6ac558d9f9760a2abbbbabecac11ccb1779ed0ecfbe14afe821c8d223"
tags:
  - "LLM 效率"
  - "LLM 其他"
  - "大语言模型强化学习后训练"
  - "RLVR"
  - "端到端 FP4"
  - "HiFloat4"
  - "rollout 激活量化"
  - "rollout–training mismatch"
  - "激活下溢"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 效率 · arXiv 2607.26515</p>

# HiFloat4 Format for End-To-End Reinforcement Learning Post-Training of Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Hei Yi Mak, Shadan Golestan, Hoang Le, Mehran Taghian Jazi, Yunke Peng, Yaoyuan Wang, Yao Wang, Junsong Wang, Tianchi Hu, Fengchen He, Guipeng Hu, Tanzila Rahman, Anandharaju Durai Raju</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26515v1) · [PDF 下载](https://arxiv.org/pdf/2607.26515v1) · **关键词** 大语言模型强化学习后训练, RLVR, 端到端 FP4, HiFloat4, rollout 激活量化, rollout–training mismatch, 激活下溢<br>


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

本文研究如何在大语言模型强化学习后训练中让采样与训练全流程均采用FP4，并指出主要障碍是采样侧激活异常值引发的大量下溢及采样—训练策略数值失配，进而以稀疏残差校正缓解该问题。

**不用术语来说**：强化学习后训练需要模型反复生成很长的回答，再根据奖励更新参数，计算和显存成本都很高；把运算压缩到4位本可显著降低成本，但少数特别大的中间数值会挤占有限的表示范围，使大量普通数值被舍入成零，导致生成数据质量和后续学习效果下降。研究需要一种既保留真正4位矩阵乘法的效率潜力，又尽量接近高精度模型准确率的方案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者声称首次实现端到端FP4强化学习后训练：采样策略与训练策略的前向、反向过程均以4位运行，不依赖LoRA适配器或高精度梯度路径；同时通过系统诊断将主要精度损失定位到采样侧激活量化，而非训练侧量化噪声。
- 提出Rollout-ResQ：在标准FP4采样矩阵乘法上增加一个满足硬件友好稀疏模式的残差校正项，用较低额外计算补偿异常值造成的量化误差，并可与HiF4和MXFP4两种格式配合。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大语言模型的强化学习后训练，重点是带可验证奖励的强化学习（RLVR）：模型针对提示生成较长的推理轨迹，再依据答案能否被规则或程序验证来获得奖励并更新策略。每次迭代包含 rollout（采样回答）与训练更新两个阶段；前者需要逐 token 自回归生成长序列，通常是主要计算瓶颈。量化可用较少比特表示权重、激活和梯度，从而降低显存占用并加速矩阵乘法。本文考察更激进的端到端 FP4 设置，即 rollout 策略和训练策略的前向、反向计算均采用 4 位浮点数，而不保留 LoRA 或其他高精度梯度路径。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**rollout 策略与训练策略**

rollout 策略根据提示逐 token 采样回答，训练策略则重新评估这些回答并根据奖励更新参数。两者数值精度或行为分布不一致时，训练所评估的轨迹可能偏离实际生成轨迹，形成 rollout–training mismatch。

</div>
<div class="concept-item" markdown="1">

**FP4 量化与激活下溢**

FP4 用约 4 位浮点格式表示计算中的数值，范围和分辨率都明显小于 BF16；若少数激活离群值拉大共享动态范围，大量普通值可能被舍入为零，这称为下溢。HiF4 使用三级分层缩放改善有限比特下的动态范围与分辨率，而 MXFP4 对每个数据块使用一个共享尺度。

</div>
<div class="concept-item" markdown="1">

**RLVR 与策略梯度**

RLVR 使用可自动核验的结果作为奖励，常用于数学推理等答案可判定的任务。GRPO 等策略梯度算法利用同一提示下多条回答的相对奖励来调整生成策略，使高奖励轨迹更可能被模型生成。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是待回答的提示、初始大语言模型以及可验证奖励信号；在每轮强化学习中，量化后的 rollout 策略先生成推理与答案，随后量化后的训练策略对这些轨迹执行前向评估、反向传播和参数更新，输出经过 RL 后训练的模型。核心约束是权重与激活相关的 rollout 计算以及训练阶段前向、反向路径均使用 FP4，以保留真正的低精度矩阵乘法吞吐；研究对象包括 Qwen2.5-3B 和 Qwen2.5-Math-7B，并比较 HiF4 与 MXFP4 两种 4 位格式。该设置不允许依赖 LoRA 适配器或高精度梯度旁路，因此必须同时处理 FP4 表示能力不足、rollout 激活离群值造成的下溢，以及 rollout 与训练策略之间的数值一致性问题。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **JetRL**: JetRL 将 rollout 与训练策略统一到低精度流水线，以减少两者的数值不匹配，但相关工作采用的是 8 位级别精度，未处理本文所指出的 FP4 rollout 激活下溢问题。
- **QeRL**: QeRL 已将 rollout 策略推进到 4 位 NVFP4，但通过 LoRA 适配器保留较高精度的梯度路径；本文进一步研究不保留该路径、训练前向与反向也采用 FP4 的端到端设置。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

LLM强化学习后训练每轮都包含自回归采样和参数更新；推理任务的轨迹较长，使采样通常成为主要瓶颈，而训练前向与反向同样消耗大量算力和显存。仅量化其中一侧还会造成采样策略与训练策略的数值行为不一致，因此，要获得端到端效率，需要两侧都采用低精度；然而FP4的动态范围和分辨率极其有限，容易导致优化脆弱甚至不收敛。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **低精度RL流水线与QeRL**：已有方法使用FP8或INT8量化采样侧，或统一量化采样与训练两侧，并通过重要性采样校正或一致的低精度流水线减少策略失配；QeRL进一步把采样策略降至4位NVFP4，但通过LoRA适配器保留较高精度的梯度更新路径。
- **静态激活异常值处理与双FP4张量分解**：后训练量化方法通常先在固定校准集上估计激活分布，再通过平滑、缩放、截断、可学习变换或旋转处理异常值；另一类分解方法把异常值从原激活中分离，形成两个FP4张量并分别进行低精度矩阵乘法。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 8位方案没有验证更激进的端到端FP4，QeRL则仍依赖高精度梯度路径；更关键的是，本文观察到仅恢复训练侧精度、同时保持FP4采样反而比全FP4更差，说明预训练式的训练侧精度恢复无法解决采样—训练策略失配。
- 静态校准假设部署时激活统计基本不变，但RL策略持续更新会使采样分布逐步漂移，校准参数很快过时，频繁重校准又会侵蚀效率；双FP4分解虽能恢复精度，却把采样阶段的FP4矩阵乘法次数加倍。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未给出一种不依赖高精度梯度路径、不过度依赖易失效的静态校准、也不将稠密FP4矩阵乘法数量翻倍的端到端FP4 RL方案；同时，FP4 RL的主导误差究竟来自训练量化还是采样量化，以及不同FP4格式对可恢复精度上限的影响，仍缺少系统辨析。

</div>
<div markdown="1"><span>核心问题</span>

在采样策略和训练策略的前向、反向均限制为FP4的条件下，精度退化的主要来源是什么，以及能否用计算开销较小、硬件可执行的采样侧校正，使RL后训练接近BF16准确率并保持真正的FP4矩阵乘法路径？

</div>
<div markdown="1"><span>作者直觉</span>

异常值把FP4量化尺度拉得过大后，主体激活会被压成零；与其把全部激活恢复为高精度，不如保留标准FP4结果，只额外表示其最关键的量化残差。若再把该残差限制为硬件支持的半结构化稀疏形式，校正计算就只处理少量重要位置，从而以小于第二次稠密FP4矩阵乘法的代价，补回最具破坏性的采样误差。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文研究端到端 FP4 强化学习后训练：用于采样回答的 rollout 策略，以及执行前向、反向传播和参数更新的训练策略，均采用 W4A4 线性层。作者先在 GRPO 框架中逐项切换训练端与 rollout 端精度，定位到主要误差并非低精度反向传播，而是 rollout 激活中的离群值抬高块缩放尺度，使大量普通数值量化为零；训练与 rollout 精度不一致还会进一步破坏策略更新所依赖的分布一致性。

针对这一问题，Rollout-ResQ 在每个 Transformer 块的 rollout 线性投影中保留标准 FP4 主矩阵乘法，同时计算激活量化残差，并用第二个稀疏 FP4 矩阵乘法补回部分丢失信息。主干训练流程不变，训练仍优化 GRPO 目标；残差修正只用于生成训练样本的 rollout 阶段。直观地说，第一次 FP4 计算负责低成本地传递主要信号，第二次计算只携带被量化遗漏且经结构化筛选的重要误差，因此避免将整个 rollout 恢复到高精度。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. FP4 策略表示与线性层量化

利用 HiF4 或 MXFP4 的分块缩放量化算子 Q，将权重和激活都映射到 FP4，并以 Q(X_ℓ)Q(W_ℓ)^⊤ 作为标准 W4A4 投影。HiF4 对 64 元素块使用三级层次缩放，MXFP4 对 32 元素块使用微缩放。

<div class="method-step__io" markdown="1">

**输入**：当前策略参数中的线性层权重 W_ℓ，以及由提示词和已生成 token 形成的层输入激活 X_ℓ。<br>
**输出**：FP4 权重、FP4 激活及标准 FP4 线性投影结果。

</div>

**直观理解**：分块共享尺度相当于给局部数值分别选择量尺，避免整张张量只用一把量尺；但块内若存在极大离群值，量尺仍会过粗，使普通数值下溢为零。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. Rollout 激活残差构造与稀疏化

先计算量化残差 ΔX_ℓ=X_ℓ−Q(X_ℓ)，再将残差量化为 Q(ΔX_ℓ)，并用结构化通道稀疏、2:4 半结构化稀疏或块稀疏函数 S 保留其中一半的候选信息。稀疏化施加于残差而非主激活，因为作者观察到残差在 2:4 删除后产生的 MSE 和 RMSE 更小。

<div class="method-step__io" markdown="1">

**输入**：rollout 线性层的原激活 X_ℓ、其 FP4 近似 Q(X_ℓ)以及量化权重 Q(W_ℓ)。<br>
**输出**：满足硬件友好稀疏模式的 FP4 残差激活 S(Q(ΔX_ℓ))。

</div>

**直观理解**：残差记录第一次量化时被舍弃的部分；方法只从这份“纠错清单”中留下重要项，而不裁剪承载主体语义的主激活。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 带残差校正的 rollout 生成

每个 rollout 线性投影将主 FP4 GEMM 与稀疏残差 GEMM 相加，并据此自回归生成每组 G 个回答，直至 EOS 或最大回答长度。每个回答随后依据任务正确性或可验证目标获得标量奖励。

<div class="method-step__io" markdown="1">

**输入**：标准 FP4 主激活、稀疏 FP4 残差、量化权重，以及训练提示词 q。<br>
**输出**：回答组 {$o_1$,…,$o_G}$、对应奖励以及生成这些 token 的旧 rollout 策略信息。

</div>

**直观理解**：模型仍主要依靠一次普通 FP4 乘法生成文本，只额外进行一次较小的稀疏纠错计算，从源头提高强化学习所用回答及概率的可靠性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. GRPO 优势计算与 FP4 策略更新

GRPO 在组内归一化奖励以得到 token 级优势，通过当前策略与旧策略的概率比进行重要性采样，并以非对称区间裁剪该比值；实际目标还含 KL 惩罚，但节选中的公式将其省略。训练策略以前向和反向均为 FP4 的方式优化该目标，更新后的参数再成为后续 rollout 的策略。

<div class="method-step__io" markdown="1">

**输入**：同一提示词下的 G 个回答、组内奖励、旧策略概率和当前训练策略概率。<br>
**输出**：更新后的全量 FP4 策略参数。

</div>

**直观理解**：同一道题的多个回答互相充当参照，因此无需另训价值网络；裁剪概率变化则防止模型因少量高奖励样本一次更新过猛。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### GRPO 裁剪策略目标

$$
J(\theta)=\mathbb{E}_{q,o_i\sim\mu_{\theta_{\mathrm{old}}}(\cdot\mid q)}\!\left[\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_i|}\sum_{t=1}^{|o_i|}\min\!\left(R_{i,t}A_{i,t},\operatorname{clip}(R_{i,t},1-\epsilon_{\mathrm{low}},1+\epsilon_{\mathrm{high}})A_{i,t}\right)\right],\quad R_{i,t}=\frac{\pi_\theta(o_{i,t}\mid q,o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t}\mid q,o_{i,<t})}
$$

**符号说明**

- $J(\theta)$：待最大化的 GRPO 策略目标，θ 为当前训练策略参数。
- $q$：从训练数据集中取得的提示词。
- $\mu_{\theta_{\mathrm{old}}}$：生成回答组的旧 rollout 策略。
- $G$：同一提示词采样的回答数量。
- $o_i,\ |o_i|$：第 i 个回答及其 token 数量。
- $o_{i,t},\ o_{i,<t}$：第 i 个回答的第 t 个 token，以及该 token 之前的回答前缀。
- $A_{i,t}$：由组内相对奖励得到的 token 级优势，表示该动作相对于同组样本的好坏。
- $R_{i,t}$：当前策略对该 token 的条件概率与旧参考策略概率之比。
- $\pi_\theta,\ \pi_{\theta_{\mathrm{old}}}$：当前目标策略与更新前参考策略。
- $\epsilon_{\mathrm{low}},\ \epsilon_{\mathrm{high}}$：重要性比率的下侧和上侧裁剪幅度。
- $\operatorname{clip}$：将概率比限制在给定区间内的裁剪函数。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标先对每个回答的 token 更新贡献取平均，再对同组回答平均。min 与 clip 共同限制新旧策略概率比带来的收益，保留有利更新的同时抑制过大的策略跳变；原文说明实际目标另含 KL 惩罚项，但此处公式未展开。<br>
**原文位置**：第3节 Preliminaries，公式(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 稀疏 Rollout-ResQ 线性投影

$$
\widehat{Y}_{\ell}=Q(X_{\ell})Q(W_{\ell})^{\top}+S\!\left(Q(\Delta X_{\ell})\right)Q(W_{\ell})^{\top},\quad \Delta X_{\ell}=X_{\ell}-Q(X_{\ell})
$$

**符号说明**

- $\ell$：线性层索引。
- $X_\ell\in\mathbb{R}^{m\times d}$：第 ℓ 层的输入激活；m 为 token 数，d 为输入维度。
- $W_\ell\in\mathbb{R}^{n\times d}$：第 ℓ 层权重；n 为输出维度。
- $Q$：将高精度数值映射到 HiF4 或 MXFP4 等低精度格式的量化算子。
- $\Delta X_\ell$：原激活与其 FP4 近似之差，即激活量化残差。
- $S$：对量化残差施加通道级、2:4 半结构化或块级稀疏模式的函数。
- $\widehat{Y}_\ell\in\mathbb{R}^{m\times n}$：经标准 FP4 投影和稀疏残差校正后的低精度输出。
- $(\cdot)^\top$：矩阵转置。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项是原有 FP4 线性层，第二项用相同量化权重把部分激活量化误差投影到输出空间并加回。若 S 为恒等函数，校正项是完整的第二次稠密 FP4 乘法；采用 50% 结构化稀疏后，只计算作者认为最重要且适合稀疏内核处理的残差信息。<br>
**原文位置**：第4.3节，公式(3)与公式(5)的合并表达；核心投影见公式(5)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练最大化 GRPO 的组相对裁剪目标：rollout 策略对每个提示词采样一组回答，可验证奖励经组内归一化形成优势，训练策略再利用新旧 token 概率比估计更新方向。Rollout-ResQ 本身不是新增损失项，也没有需要单独学习的校正参数；它通过改善 rollout 前向计算，减少激活归零对回答、奖励和策略概率的污染，从而让输入 GRPO 目标的数据更接近训练策略所依据的分布。作者注明完整目标含 KL 惩罚，但节选未给出其具体形式或系数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. HiF4 分层 FP4 格式**

HiF4 在 64 元素块上采用三级层次缩放：第一级缩放器为 E6M2，第二、三级为 E1，单元素采用 S1P2（等价于 E1M2）。顶层缩放器和 FP4 数值均保留尾数精度，用于在 4 bit 元素预算下兼顾动态范围与分辨率。

> 直观理解：层次缩放像先选择大范围量尺，再逐级微调局部量尺；与只有共享块指数的设计相比，它更有机会区分块内相近的小数值，但仍不能完全消除离群值导致的归零。

**2. Rollout-ResQ 残差投影**

模块在所有 Transformer 块的 rollout 线性投影中，将标准项 Q(X_ℓ)Q(W_ℓ)^⊤ 与校正项 S(Q(X_ℓ−Q(X_ℓ)))Q(W_ℓ)^⊤ 相加。残差按整张量构造，而不是逐量化块构造，以便使用现代深度学习框架实现；该模块不改变训练侧的 GRPO 目标。

> 直观理解：普通 FP4 投影负责快速近似原计算，残差投影专门补偿因离群值和下溢而消失的激活信息；把修正放在 rollout 端，是因为训练样本的生成误差被诊断为主要瓶颈。

**3. 硬件友好残差稀疏函数**

作者比较三种 50% 稀疏实例：$S_{50\%}$ 保留 L2 范数最大的 50% 通道；$S_{2:4}$ 在每连续 4 个元素中保留绝对值最大的 2 个；$S_{50\%}^{32\times64}$ 保留 L2 范数最大的半数 32×64 块。令 S 为恒等映射则得到带第二次稠密 FP4 GEMM 的 Rollout-ResQ-Dense。

> 直观理解：三种模式分别按整条通道、四元素小组和矩形块筛选误差，以匹配不同稀疏矩阵乘法内核；目的不是减少模型参数，而是让 rollout 的纠错项比完整第二次乘法便宜。

**训练与推理**

训练时，在 VeRL 的 GRPO 流程中先用带 Rollout-ResQ 的 FP4 rollout 策略自回归采样回答：每一步的所有 Transformer 线性投影均计算主 FP4 项和稀疏残差校正项。回答获得任务奖励后，系统计算组相对优势和重要性比率，以 FP4 训练策略完成前向、反向传播及参数更新；因此“端到端 FP4”覆盖 rollout 与训练，而不是只量化部署模型。更新后的策略进入下一轮采样。

若将该策略用于生成，原文方法对应的前向过程仍可使用 Rollout-ResQ：输入提示词后逐 token 解码，并在各线性层加入稀疏残差投影，直到产生 EOS 或达到长度上限。不过节选将该模块明确定位于 RL 的 rollout 阶段，未明确报告独立部署推理流程、端到端延迟或实际加速比，因此不能据此断言部署时必然获得速度提升。

**复现信息**

量化格式采用 HiF4 或 MXFP4：前者以 64 元素为块并使用三级缩放，后者以 32 元素为块、共享 E8M0 块尺度且元素为 FP4 E2M1。默认残差稀疏率为 50%，比较通道级 $S_{50\%}$、硬件支持的 $S_{2:4}$ 和 32×64 块级 $S_{50\%}^{32\times64}$；S 为恒等函数时是 Dense 版本。

Qwen2.5-3B 与 Qwen2.5-Math-7B 的策略学习率均为 1×10^{-6}，组大小 G 均为 16，优化器均为 AdamW；训练批量分别为 32 和 128，最大提示长度分别为 512 和 2048，最大回答长度分别为 1024 和 4096。两者的 ($ε_low,ε_high)$ 分别为 (0.2,0.2) 与 (0.2,0.28)，并统一使用阈值 5.0 的 token 级截断重要性采样；原文报告相应实验约需 100 GB/10 小时和 370 GB/20 小时，但未在节选中给出具体加速器型号、并行配置或稀疏内核实测速度。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K：用于Qwen2.5-3B的GRPO训练；GSM8K-test作为同分布留出测试集。原文未明确报告训练样本规模、具体训练划分或测试样本数。
- DAPO-Math-17K：用于Qwen2.5-Math-7B的GRPO训练，代表更困难的数学推理任务。实验设置段一度写作“DAPO-Math-17B”，但第5.3节及表3写作“DAPO-Math-17K”，命名存在原文内部不一致；具体规模与划分原文未明确报告。
- 跨分布数学评测集合：Qwen2.5-3B在Math-500上评测；Qwen2.5-Math-7B在AIME-2024、AIME-2025、AMC-2023和Math-500上评测。它们用于检验强化学习训练所得能力能否迁移到未作为训练任务报告的不同数学竞赛与解题基准，而不只是记住训练分布。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Mean@1**

Qwen2.5-3B采用贪心解码时单次回答的平均准确率，反映模型在确定性生成协议下直接解对问题的比例。 （越高越好，因为更高数值表示更多问题在一次生成中得到正确答案。）

</div>
<div class="metric-item" markdown="1">

**Mean@32**

Qwen2.5-Math-7B对每道题采样32个回答后得到的平均准确率；它衡量随机采样条件下单个回答的平均正确概率，不等同于“32次中至少一次答对”的pass@32。 （越高越好，因为它表示采样回答总体具有更高的正确率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen2.5-3B在GSM8K上训练，GSM8K-test上以Mean@1评测，并分别使用HiF4与MXFP4。

<div class="result-value" markdown="1">

BF16准确率为86.96；朴素HiF4和MXFP4分别为82.03和73.31，对BF16的差距为4.93和13.65个百分点。加入2:4稀疏Rollout-ResQ后，两种格式均取得各自最佳的GSM8K-test结果：HiF4为85.90、仅差1.06个百分点；MXFP4为81.65、差5.31个百分点。

</div>

该结果表明，直接把rollout和训练都降到FP4会显著损害同分布数学准确率，而只在rollout矩阵乘法中加入稀疏残差校正可以收回大部分损失。HiF4恢复后更接近BF16，说明FP4格式本身会限制可恢复的性能上限。不过，这一结果不能单独证明收益完全来自作者提出的“激活下溢”机制，也不能证明在非数学任务或其他模型家族上同样有效。

<div class="result-source" markdown="1">

来源：第5.2节，表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

By contrast, Rollout-ResQ-S2:4 reduces these gaps to 1.06% and 5.31% on GSM8K-test for HiF4 and MXFP4, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen2.5-3B在GSM8K上训练后，于跨分布Math-500上以Mean@1评测。

<div class="result-value" markdown="1">

BF16为61.2；朴素HiF4和MXFP4分别只有44.6和27.8。HiF4下最佳方法是块结构50%稀疏的Rollout-ResQ，达到55.8；MXFP4下最佳方法是稠密Rollout-ResQ，达到48.2。两者仍分别落后BF16 5.4和13.0个百分点。

</div>

Rollout-ResQ的改进不仅出现在训练任务的留出测试集，也能迁移到Math-500，因而支持其改善数学推理泛化的说法。但跨分布差距明显大于GSM8K-test上的差距，尤其MXFP4仍远低于BF16；因此该方法是缓解而非消除低精度损失。此外，不同格式的最佳稀疏结构不同，说明不存在由这些实验确立的单一全局最优配置。

<div class="result-source" markdown="1">

来源：第5.2节，表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Math500, under HiF4, Rollout-ResQ-S50%32×64 achieves the highest accuracy (55.8%), followed by other Rollout-ResQ variants.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen2.5-Math-7B在DAPO-Math-17K上训练，使用HiF4，并在AIME-2024、AIME-2025、AMC-2023和Math-500上以Mean@32评测。

<div class="result-value" markdown="1">

相对BF16，朴素HiF4在四个基准上的差距依次为11.14、4.79、9.37和15.19个百分点；2:4稀疏Rollout-ResQ将差距缩小为6.56、3.54、8.75和5.64个百分点。其对应准确率为20.73、8.54、55.78和68.95；其中AIME-2024与AMC-2023为Rollout-ResQ变体中的最佳结果，而稠密变体在AIME-2025和Math-500略高，分别达到8.96和69.02。

</div>

7B实验说明Rollout-ResQ的效果并非只存在于3B模型或GSM8K：它在四个难度和分布不同的数学基准上总体改善朴素HiF4。2:4结构的优势是表现较一致，而不是每个数据集都绝对最优；AIME-2024和AMC-2023仍与BF16存在较大差距，因此不能据此宣称FP4已达到完整精度。

<div class="result-source" markdown="1">

来源：第5.3节，表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, Rollout-ResQ-S2:4 narrows the gaps to BF16 to 6.56%, 3.54%, 8.75%, and 5.64%, respectively, with Rollout-ResQ-Dense performs slightly better on AIME25 and Math500.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 任务覆盖集中于数学推理，模型仅包括Qwen2.5-3B与Qwen2.5-Math-7B；没有语言理解、代码、对话、安全对齐或其他模型家族实验，因此格式和恢复机制的广泛通用性尚未得到验证。
- 效率结论主要是基于FP4相对FP16具有四倍吞吐量的理论FLOP换算。原文摘录未报告真实硬件上的训练或rollout吞吐量、延迟、显存占用、稀疏内核利用率及通信开销，也未报告多次运行的统计不确定性；因此约2.67倍加速应理解为理想上限，而非实测端到端速度。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- BF16：rollout策略与训练策略都使用BF16，是完整精度参考上界；所有括号中的准确率差距均以它为基准。
- 朴素HiF4或MXFP4：所有Transformer块的线性层在rollout和训练两侧均量化为相应FP4格式，但不加入rollout恢复机制；该比较直接测量端到端FP4量化本身造成的损失。
- SmoothQuant：对rollout激活进行平滑，并在每次强化学习迭代开始时重新校准尺度；用于检验依赖校准的经典激活量化方法能否适应不断变化的rollout分布。
- RHT与OCC：均作为rollout激活恢复或异常值处理基线，用于判断Rollout-ResQ的收益是否只是一般性的异常值缓解效果，而非其残差校正设计特有的优势。

**实验想回答的问题**

- 在端到端FP4强化学习后训练中，Rollout-ResQ能否在HiF4与MXFP4两种量化格式下缩小相对于BF16的数学推理准确率差距，并改善训练收敛性？
- Rollout-ResQ采用何种残差稀疏结构能在准确率、跨任务泛化与理论计算效率之间取得较好平衡？

**实验实现**

全部实验使用VeRL混合引擎训练框架，以vLLM执行rollout、FSDP执行训练策略，并以GRPO作为强化学习算法。HiF4与MXFP4量化应用于所有Transformer块的线性层。Qwen2.5-3B在GSM8K上训练并报告Mean@1；Qwen2.5-Math-7B在DAPO-Math-17K上训练并报告Mean@32。比较对象包括BF16、无恢复方法的FP4、SmoothQuant、RHT、OCC以及多种Rollout-ResQ稠密或稀疏变体。原文摘录未提供随机种子、重复运行次数、置信区间或显著性检验，因此表中差异应视为所报告运行的结果，而不是已证明具有统计显著性的总体差异。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 固定FP4格式与训练流程，仅改变Rollout-ResQ残差的稠密、非结构化50%稀疏、32×64块级50%稀疏和2:4结构化稀疏形式。 | 在GSM8K-test上，2:4结构在HiF4和MXFP4下分别达到85.90和81.65，是两种格式的最佳结果；但在Math-500上，HiF4的32×64块稀疏版本以55.8最高，MXFP4的稠密版本以48.2最高。7B实验中，2:4版本在AIME-2024和AMC-2023分别达到20.73和55.78，而稠密版本在AIME-2025和Math-500分别以8.96和69.02略胜。 | 这一消融隔离了残差保留模式的作用：2:4稀疏并非简单依靠保留更多残差，因为它只保留一半元素，却在多数核心设置下提供最稳定的收益，并可映射到结构化稀疏硬件。另一方面，各任务最优结构不一致，表明稀疏模式会与模型、量化格式和评测分布交互；实验支持选择2:4作为实用折中，但没有证明它在所有任务上最优。 | 第5.2节表2；第5.3节表3<br><span class="experiment-evidence">Overall, these results show that Rollout-ResQ-S2:4 delivers the best GSM8K-test accuracy across both FP4 formats and remains competitive on Math500.</span> |

**定性案例**

- 训练曲线提供了定性过程证据：图5显示2:4 Rollout-ResQ在3B的HiF4、MXFP4以及7B的HiF4设置中通常更快达到较高平均奖励并保持相对稳定；SmoothQuant收敛缓慢，RHT在7B训练后期奖励下降，MXFP4整体波动也更明显。这支持方法改善训练动态的解释，但图中未给出方差带或多随机种子轨迹，因而不能排除单次运行波动。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution is an FP4 format and residual quantization mechanism for efficient end-to-end LLM RL post-training.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`78ca15a6ac558d9f9760a2abbbbabecac11ccb1779ed0ecfbe14afe821c8d223`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
