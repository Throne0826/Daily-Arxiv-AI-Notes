---
title: "[论文解读] Perception Before Reasoning: Dynamic Latent Reasoning for Video Understanding and Question Answering"
description: "[arXiv 2608.04124][VLM Reasoning] DyLaR将视频问答拆分为必需的视觉证据感知与按需启用的潜空间推理，使模型能够根据问题难度选择直接作答或继续推理。"
arxiv_id: "2608.04124"
announcement_date: "2026-08-06"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:59:42.146062+00:00"
source_sha256: "39c06bcab11c888c3f2d5a12399a2e8f43f9de2e6d70fbccb00fbd9947cc8085"
tags:
  - "VLM Reasoning"
  - "VLM Efficiency"
  - "LLM Reasoning"
  - "视频问答"
  - "多模态大语言模型"
  - "视觉证据落地"
  - "潜在推理"
  - "连续隐状态"
  - "自适应路由"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.04124</p>

# Perception Before Reasoning: Dynamic Latent Reasoning for Video Understanding and Question Answering

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Haotian Xia, Zilin Xiao, Junbo Zou, Vicente Ordonez, Hanjie Chen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Department of Computer Science, Rice University；College of Sciences, Georgia Institute of Technology</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04124v1) · [PDF 下载](https://arxiv.org/pdf/2608.04124v1) · **关键词** 视频问答, 多模态大语言模型, 视觉证据落地, 潜在推理, 连续隐状态, 自适应路由<br>


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

DyLaR将视频问答拆分为必需的视觉证据感知与按需启用的潜空间推理，使模型能够根据问题难度选择直接作答或继续推理。

**不用术语来说**：视频问答模型不仅要在多个画面中找到与问题有关的人、物体或动作，有时还要比较不同时刻的事件或综合分散线索；但现有模型往往不区分这两种情况，对每个问题都生成很长的文字推理过程，导致回答缓慢且计算开销大。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出证据优先的自适应潜推理范式：所有问题先用一小段感知潜变量保存与查询相关的视觉证据，只有在局部证据不足以直接确定答案时，才追加推理潜变量。
- 提出DyLaR训练框架，分别利用经验证的局部视觉证据监督感知潜变量、将经验证的文字推理蒸馏到推理潜变量，并通过可验证奖励的强化学习优化何时继续推理的路由决策。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究视频问答：多模态大语言模型需要根据自然语言问题，在视频的多个帧中定位相关对象、动作或事件，并据此生成答案。现有视频推理模型通常对每个问题都先输出文本思维链，以额外的测试时计算换取准确率，但这会产生数百乃至数千个文本词元；而连续隐状态能够承载中间信息，使模型有可能在不解码完整推理文本的情况下完成计算。本文据此区分两类需求：所有问题都需要跨帧视觉证据定位，但只有涉及时间比较、关系组合或因果推断等情况的问题，才需要在证据之上继续推理。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多模态大语言模型（MLLM）**

能够联合处理视频或图像与自然语言的生成模型。在本文场景中，它读取视频和问题，将视觉内容与语言查询对齐后生成答案。

</div>
<div class="concept-item" markdown="1">

**文本思维链（CoT）**

模型在给出最终答案前生成的逐步文字推理过程，可通过增加测试时计算改善复杂问题的表现。其缺点是即使问题只需找到一个明显视觉证据，也可能生成冗长且重复描述视频内容的文本。

</div>
<div class="concept-item" markdown="1">

**潜在推理（latent reasoning）**

把中间计算保留在模型的连续隐状态中，而不将每一步都解码为离散文字。本文进一步把这些状态分成用于保存问题相关视觉证据的感知潜变量，以及仅在必要时用于进一步推断的推理潜变量。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一段包含多个视频帧的视频和一个自然语言问题，输出是该问题的最终答案。基本假设是：每个问题都必须先完成以问题为条件的视觉证据落地，即从跨帧内容中找出相关对象、动作或时刻；但证据落地之后是否仍需推理取决于问题本身。感知导向问题在定位证据后即可直接回答，推理导向问题则还需比较不同时刻的事件，或组合分散在多个帧中的线索。因此，本文关注的设置不是为所有问题分配固定推理长度，而是在共享的视频问答模型中动态选择“证据定位后直接回答”或“证据定位后继续潜在推理再回答”。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **CODI**: CODI通过自蒸馏把显式文本思维链压缩为连续状态，支持“推理收益来自隐状态而非必须输出文字”这一技术前提；但原文将其归入通用潜在推理工作，并未说明它解决视频中的跨帧证据定位或按问题动态决定是否推理。
- **Mull-Tokens**: Mull-Tokens在答案前插入固定长度、模态无关的潜在词元，并可从以图像为主的训练迁移到视频问答。它与本文最直接的差别是对每个问题使用相同潜在预算，而本文要把必需的视觉落地与可选的额外推理解耦。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

视频问答需要在多帧内容中完成查询相关的证据定位，并在必要时对跨时间证据进行比较、组合或推断。实际问题的难度并不一致：感知型问题在找到相关物体、动作或画面后即可回答，推理型问题才需要额外整合多个时刻的线索。因此，统一采用冗长推理流程会把大量计算浪费在本可直接回答的问题上。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **显式文本思维链视频推理**：模型对每个问题先用自然语言描述相关视频内容，再逐步写出推理过程，最后生成答案。额外的测试时计算通常有助于准确率，但每个查询可能产生数百乃至数千个中间文本词元。
- **潜空间推理与视觉潜变量方法**：这类方法不必把全部中间计算解码成文字，而是用连续隐藏状态承载推理或查询相关的视觉表示；已有图像方法还会重建相关视觉特征，或把视觉潜状态插入显式文本思维链中。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 显式文本思维链通常对所有问题采用相似的推理流程，即使答案在证据定位后已经明确，仍会重复描述已找到的内容，造成较高的生成长度、延迟和测试时计算成本。
- 已有潜推理工作主要面向图像，重点是如何在潜空间中推理，而未解决视频问答中是否需要推理的逐题判断；部分方法仍在潜视觉状态之间生成完整文字推理，因此没有充分消除显式思维链的成本。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种适用于视频问答的统一机制，能够先对每个问题可靠地保留跨帧视觉证据，再根据证据是否足以支持答案，动态决定是否投入额外的潜空间推理计算。该缺口同时涉及感知与推理的功能分离，以及二者之间可学习的自适应路由。

</div>
<div markdown="1"><span>核心问题</span>

能否让多模态模型对所有视频问题先进行紧凑、受证据约束的潜表示学习，再逐题判断是直接回答还是追加潜推理，从而在不依赖冗长文本思维链的情况下兼顾答案准确性与生成效率？

</div>
<div markdown="1"><span>作者直觉</span>

文字思维链的有效部分主要是生成文字时形成的内部隐藏状态，而不是这些状态被解码后的句子本身。若先把与问题有关的画面压缩进感知潜变量，简单问题便可直接读取这些证据作答；只有需要跨时刻比较或组合线索时，模型才继续生成推理潜变量。这样既保留了必要的内部计算，又避免为每个问题支付完整文字推理的成本。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

DyLaR 将视频问答建模为“先感知、后按需推理”的单模型自回归生成过程。输入视频 $V$ 与问题 $q$ 经多模态大语言模型编码为前缀后，模型先生成固定预算的感知潜变量 $mathbf{z}^{p}_{1:K_p}$，使其聚合与问题相关的对象、区域或动作证据；到达 $\texttt{<perc\_end>}$ 后，模型依据问题和已形成的视觉表征，自适应选择直接输出答案，或先生成推理潜变量 $\mathbf{z}^{r}_{1:K_r}$ 再回答。潜变量不是词表中的可读 token，而是连续隐藏状态：每一步把上一解码步的隐藏状态直接作为下一位置的输入嵌入，因此中间计算留在隐空间中，只有分段标记与最终答案需要文本生成。

训练分两阶段。监督微调先用经过验证的证据框约束感知潜变量，再将经过验证的文本推理依据蒸馏到推理潜变量，并学习合法的直接回答或推理回答结构；强化学习随后对模型自行生成的完整轨迹执行带潜状态回放的 GRPO，以答案正确性和格式合法性为可验证奖励，进一步校准“是否需要推理”的路由决策。直观上，它先用少量内部位置完成类似“把相关画面指出来”的工作；若定位证据已足够便立即回答，只有需要跨帧整合或逻辑推断时才额外进行不可见的内部思考。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多模态输入编码

基础多模态大语言模型将视觉 patch 表征投影到语言模型隐藏空间，并与问题编码共同组成自回归解码所条件化的多模态前缀。

<div class="method-step__io" markdown="1">

**输入**：采样后的视频帧 $V$ 与自然语言问题 $q$。<br>
**输出**：包含视频内容和问题语义的多模态前缀。

</div>

**直观理解**：这一步相当于让模型先看完抽取的视频画面并读懂问题，但尚未决定答案，也尚未决定是否需要额外推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 证据优先的感知潜变量生成

模型在 $K_p$ 个连续位置上执行潜变量分段解码：不采样词表 token，而将前一步解码器隐藏状态直接作为下一步输入嵌入，形成 $mathbf{z}^{p}_{1:K_p}$；训练时这些状态通过证据框内视觉 patch 的平均表征接受余弦距离约束。

<div class="method-step__io" markdown="1">

**输入**：多模态前缀，以及感知段起始标记 $\texttt{<perc\_start>}$。<br>
**输出**：由 $\mathcal{P}_{K_p}=[\texttt{<perc\_start>}\,\mathbf{z}^{p}_{1:K_p}\,\texttt{<perc\_end>}]$ 表示的查询相关视觉证据摘要。

</div>

**直观理解**：它不是把整段视频逐字描述出来，而是先在内部压缩出回答当前问题真正需要看的对象、区域或动作；这保证每个问题都经过视觉落地。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自适应路由与潜空间推理

在 $\texttt{<perc\_end>}$ 后的决策位置，模型生成 $\texttt{<answer>}$ 以采用直接路径，或生成 $\texttt{<reason\_start>}$ 并分配 $K_r$ 个推理潜变量 $mathbf{z}^{r}_{1:K_r}$；后者通过连续隐藏状态整合已定位的视觉证据。

<div class="method-step__io" markdown="1">

**输入**：问题、多模态前缀及感知潜变量 $mathbf{z}^{p}_{1:K_p}$。<br>
**输出**：直接结构 $\mathcal{S}^{\mathrm{direct}}=[\mathcal{P}_{K_p},\mathcal{A}(a)]$，或推理结构 $\mathcal{S}^{\mathrm{reason}}=[\mathcal{P}_{K_p},\mathcal{R}_{K_r},\mathcal{A}(a)]$。

</div>

**直观理解**：这相当于一道选择题：如果“看到相关画面”已经足以回答，就跳过思考；若还需比较时间顺序、因果或多个证据，才开启额外的内部推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结构化答案解码

潜变量预算耗尽后，解码恢复为普通词表上的逐 token 生成，并在 $\mathcal{A}(a)=[\texttt{<answer>}\,a\,\texttt{</answer>}]$ 中输出最终答案 $a$；分隔符和答案参与语言建模，潜变量占位符本身不作为语义 token 预测。

<div class="method-step__io" markdown="1">

**输入**：感知段，以及可选的推理潜变量段。<br>
**输出**：可解析的最终答案及其直接或推理响应结构。

</div>

**直观理解**：内部证据整理和推理完成后，模型只把简短答案写出来；潜变量承担中间计算，因此无需输出冗长的文本思维链。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 联合监督目标及其核心潜变量约束

$$
\begin{aligned}
\mathcal{L}_{\mathrm{SFT}}
&=\mathcal{L}_{\mathrm{text}}+\lambda_g\mathcal{L}_{\mathrm{ground}}
+\mathbb{I}[s=\textsc{reason}]\left(\lambda_e\mathcal{L}_{\mathrm{exp}}+\lambda_d\mathcal{L}_{\mathrm{distill}}\right),\\
\mathcal{L}_{\mathrm{ground}}
&=\frac{1}{M_p}\sum_{i=1}^{M_p}\left[1-\cos\left(\hat{\mathbf{z}}^p_i,\mathbf{u}_i\right)\right],\qquad
\mathbf{u}_i=\frac{1}{|\mathcal{P}_i|}\sum_{p\in\mathcal{P}_i}\mathbf{x}^v_p,\\
\mathcal{L}_{\mathrm{exp}}
&=-\sum_{t\in\mathcal{T}_{\mathrm{exp}}}\log\pi_\theta\left(w_t\mid V,q,w_{<t}\right),\\
\mathcal{L}_{\mathrm{distill}}
&=\frac{1}{L}\sum_{\ell=1}^{L}\mathrm{SmoothL1}\left(\mathbf{h}^{\mathrm{lat}}_\ell,\mathrm{sg}\left[\mathbf{h}^{\mathrm{exp}}_\ell\right]\right).
\end{aligned}
$$

**符号说明**

- $\mathcal{L}_{\mathrm{SFT}}$：监督微调的总损失。
- $\mathcal{L}_{\mathrm{text}}$：响应中非潜变量文本位置的语言建模损失，覆盖结构分隔符和最终答案，忽略潜变量占位位置。
- $s$：经验证的样本类型，取 direct 或 reason；只有 reason 样本启用显式依据与蒸馏项。
- $\lambda_g,\lambda_e,\lambda_d$：分别控制感知落地、显式推理依据学习和潜变量蒸馏强度的权重。
- $M_p$：当前监督样本中经过验证的证据框数量。
- $\mathcal{P}_i$：落入第 i 个证据框的视觉 patch 索引集合。
- $\mathbf{x}^{v}_p$：第 p 个视觉 patch 投影到语言模型隐藏空间后的 d 维嵌入。
- $\mathbf{u}_i$：第 i 个证据框中所有视觉 patch 嵌入的平均值，即对象级监督目标。
- $\hat{\mathbf{z}}^p_i$：紧邻第 i 个感知潜变量之前的解码器隐藏状态。
- $\pi_\theta$：参数为 θ 的模型所给出的下一 token 概率分布。
- $\mathcal{T}_{\mathrm{exp}}$：教师响应中推理依据和答案 token 的位置集合。
- $\mathbf{h}^{\mathrm{lat}}_\ell,\mathbf{h}^{\mathrm{exp}}_\ell$：学生潜变量分支与教师显式依据分支在首个答案预测位置、第 ℓ 层的隐藏状态。
- $L$：解码器层数。
- $\mathrm{sg}[\cdot]$：停止梯度算子，使蒸馏目标只更新学生方向而不反向改变教师目标状态。

<div class="equation-explanation" markdown="1">

**直观理解**：总目标同时约束“输出什么”和“内部状态表示什么”：文本损失学习合法结构与答案，感知损失把每个感知状态拉向相应证据框的对象级视觉向量；对确实需要推理的样本，教师分支学习可读推理依据，学生分支则在答案入口处模仿教师的逐层内部状态。这样，推理潜变量无需逐 token 复制文本思维链，也能继承该依据为回答所提供的信息。<br>
**原文位置**：第 3.2 节，式 (2)；Perception grounding，式 (3)–(4)；Rationale-to-latent self-distillation，式 (5)

</div>

</div>

<div class="equation-block" markdown="1">

#### 格式门控的强化学习奖励

$$
R(o_i)=\mathbb{I}_{\mathrm{form}}(o_i)\left(\alpha_{\mathrm{form}}+\alpha_{\mathrm{acc}}\mathbb{I}_{\mathrm{acc}}(o_i)\right)
$$

**符号说明**

- $o_i$：针对同一视频问题提示采样得到的第 i 条完整响应轨迹。
- $\mathbb{I}_{\mathrm{form}}(o_i)$：格式合法性指示函数，检查轨迹是否严格符合直接结构或推理结构。
- $\mathbb{I}_{\mathrm{acc}}(o_i)$：答案正确性指示函数，检查提取出的答案是否匹配真实答案。
- $\alpha_{\mathrm{form}},\alpha_{\mathrm{acc}}$：格式奖励与答案正确奖励的权重。
- $R(o_i)$：轨迹获得的标量奖励，随后在同组轨迹间标准化为 GRPO 优势。

<div class="equation-explanation" markdown="1">

**直观理解**：格式指示函数位于乘法门控位置，因此格式无效的响应即使碰巧含有正确答案也得不到准确性奖励；格式正确后，答对可获得主要奖励。该奖励不直接规定每道题必须走哪条路径，而是让路由选择通过最终结构和答案质量接受反馈。<br>
**原文位置**：第 3.2 节，Reinforcement Learning with Latent Replay，Reward，式 (7)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：监督阶段以 $\mathcal{L}_{\mathrm{SFT}}$ 联合优化模型参数。所有样本都学习结构分隔符、最终答案和感知落地；只有带有验证推理依据的 $s=\textsc{reason}$ 样本才加入 $\mathcal{L}_{\mathrm{exp}}$ 与 $\mathcal{L}_{\mathrm{distill}}$，从而避免强迫本可直接回答的样本生成推理。感知训练采用教师强制：第 $i$ 个证据框的对象级向量 $mathbf{u}_i$ 被送入对应潜变量位置，同时前一隐藏状态通过 $\mathcal{L}_{\mathrm{ground}}$ 学习预测该向量；推理训练中，显式依据只作为教师表征，学生从未被要求输出依据 token。

强化学习阶段使用 GRPO 对完整响应进行优化。由于连续潜状态没有词表概率，生成轨迹时记录其潜隐藏状态 $\tilde{\mathbf{H}}_i$，重新评分时将其作为固定输入嵌入回放，只对普通文本 token 以及感知段后的路由 token 计算新旧策略概率比；每个提示的 $G$ 条轨迹以组内标准化奖励形成优势，并使用裁剪目标和相对冻结 SFT 参考策略的 KL 惩罚。作者方法上的主张是，这一阶段可把固定监督序列下学到的能力转化为推理时由模型自己决定的路由行为；分析上看，答案奖励主要校准任务效用，格式门控则防止模型通过破坏输出协议获得偶然收益。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 潜变量分段解码**

每个潜变量段由普通文本分隔符包围，内部序列化为固定数量的 $\texttt{<|latent\_pad|>}$ 占位位置；在这些位置上，模型跳过词表采样与 token 嵌入查找，将上一位置的解码器隐藏状态直接送入下一位置。段长结束后恢复普通自回归文本生成，整个过程仍由同一个模型完成。

> 直观理解：占位符只预留计算步数，不表达词义；真正流动的是连续向量，所以模型可以进行中间计算而不必把每一步思考翻译成自然语言。

**2. 证据框驱动的感知落地**

对于第 $i$ 个已验证证据框，取框内 patch 集合 $\mathcal{P}_i$，将其投影视觉嵌入 $mathbf{x}^{v}_p$ 平均为对象级目标 $mathbf{u}_i=|\mathcal{P}_i|^{-1}\sum_{p\in\mathcal{P}_i}\mathbf{x}^{v}_p$；证据框按视频时间排序，监督时感知潜变量数量 $M_p$ 跟随框数，并用平均余弦距离使前序隐藏状态 $\hat{\mathbf{z}}^{p}_i$ 接近 $mathbf{u}_i$。推理时没有证据框，模型依据已学到的映射自行生成固定预算的感知潜变量。

> 直观理解：单个视觉 patch 往往只是对象的一小块，框内平均把多个 patch 合成对象或区域级证据；这种监督让内部感知位置真正对应可核验的画面，而不是仅凭问题语言猜答案。

**3. 推理依据到潜变量的自蒸馏与自适应路由**

对类型 $s=\textsc{reason}$ 的样本，同一模型执行两次前向传播：教师分支显式生成经过验证的推理依据和答案，学生分支用 $K_r$ 个推理潜变量替代文本依据。两分支在预测首个答案 token 的位置逐层对齐隐藏状态，教师状态停止梯度；随后强化学习还将 $\texttt{<perc\_end>}$ 后生成 $\texttt{<answer>}$ 或 $\texttt{<reason\_start>}$ 的选择作为策略动作评分。

> 直观理解：教师分支展示完整解题过程，学生分支不模仿这些文字，而是学习到达相近的“准备回答”内部状态；路由训练则让模型根据结果反馈学习哪些问题无需额外推理。

**训练与推理**

训练数据按验证注释分为两类：仅有局部证据框的样本标记为 $\textsc{direct}$，同时具有证据框和验证推理依据的样本标记为 $\textsc{reason}$；这些注释由独立验证模型自动生成并过滤。第一阶段执行监督微调：证据框按时间排序，感知潜变量数量随框数变化；推理样本用显式教师分支与潜变量学生分支共同前向传播，并在首个答案预测位置跨全部解码层进行 SmoothL1 表征对齐。第二阶段从旧策略为每个提示采样一组响应，记录其中连续潜状态，再以固定潜状态回放、文本动作重评分和格式门控奖励执行 GRPO，从而同时训练答案行为和 $\texttt{<answer>}$／$\texttt{<reason\_start>}$ 路由选择。

推理时不再提供证据框、推理依据或教师分支。模型先编码视频与问题，再生成 $K_p$ 个感知潜变量；到达感知段末尾时，若生成 $\texttt{<answer>}$，便直接输出答案，若生成 $\texttt{<reason\_start>}$，则先运行 $K_r$ 步潜空间推理再输出答案。两条路径都由同一模型以一次连续的自回归序列完成，且外部可见内容仅包括结构标记和最终答案。

**复现信息**

复现时最关键的容量设定是：监督训练中感知潜变量数等于每个样本的验证证据框数，推理潜变量固定为 $K_r=6$；推理及强化学习轨迹统一使用 $K_p=4$ 和 $K_r=6$。SFT 训练一轮，优化器为 AdamW，学习率为 $1\times10^{-5}$，损失权重为 $\lambda_g=1.0$、$\lambda_e=1.0$、$\lambda_d=20.0$；较大的蒸馏权重沿用 CODI 的设定。

GRPO 使用学习率 $5\times10^{-7}$、组大小 $G=8$、采样温度 $\tau=0.9$、裁剪系数 $\epsilon=0.2$、KL 系数 $\beta=0.04$，训练 $2500$ 步；奖励权重为 $\alpha_{\mathrm{form}}=0.05$ 和 $\alpha_{\mathrm{acc}}=1.0$。公平解释这些设置时应注意，固定的推理潜变量预算限制了每次启用推理的隐空间计算量，而路由机制节省的是不必要的推理段及冗长文本生成，并非完全取消视频编码成本。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 通用与长视频理解组：Video-MME含900个视频上的2700道四选一题，按短、中、长视频各900题划分；LVBench含103个小时级视频上的1549道四选一题；LongVideoBench使用有真值的完整验证集，共1337道长视频指代与推理题。该组主要检验固定16帧采样下，对不同时长视频及稀疏关键证据的理解能力。
- 时序与长程推理组：MVBench包含20类时序感知任务、每类200题，共4000题；LongVideo-Reason使用1000题的精选评测集，考查长视频推理；TempCompass采用Video-R1所用官方评测集合，将四种官方任务格式统一为字母选择题。该组用于区分基础时序感知与跨片段证据组合能力。
- 复杂综合推理组：Video-TT评测其1000道五选一题；Video-Holmes包含1837道六选一题，要求对悬疑短片进行多步推断；MMVU仅采用公开验证集中的625道多选题，排除其余375道开放题。该组测试整体视频思考、多步情节推断和专家级多学科理解。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（Accuracy, %）**

九个数据集均被整理为字母多项选择问答，准确率表示最终选项与标准答案一致的样本比例；平均准确率是九个基准准确率的算术汇总，用于衡量跨任务总体表现。 （越高越好，因为它表示模型在更多视频问题上选出正确答案。）

</div>
<div class="metric-item" markdown="1">

**每题可见词元数（Tok/query）**

每个问题平均生成或预填的可见词元数量，用来近似衡量文本输出及显式思维链的长度；潜变量内部计算不以可见文本词元呈现。 （在准确率相当或更高时越低越好，因为较少可见词元意味着更紧凑的响应；但该指标不等同于完整计算量或端到端延迟。）

</div>
<div class="metric-item" markdown="1">

**推理分支触发率**

DyLaR选择可选推理潜变量分支的样本比例，用于观察路由器是否会根据问题类型分配潜空间推理计算。 （没有统一的单调优劣方向；理想现象是感知类问题触发率较低、推理类问题触发率较高，表明计算分配与问题难度相关。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-VL-4B骨干上的DyLaR与同家族Thinking模型比较

<div class="result-value" markdown="1">

DyLaR的九基准平均准确率为58.2%，比Qwen3-VL-4B-Thinking的54.0%高4.2个百分点；每题可见词元由1220.7降至18.5。分任务看，DyLaR并非全面占优：其MMVU和TempCompass准确率分别为63.8%和69.6%，低于Thinking的66.7%和71.3%。

</div>

该结果支持作者的核心主张：先压缩视觉证据、再按需进行潜空间推理，可以在同一模型家族中取得更高的总体准确率，同时避免生成很长的文本理由。不过，平均值掩盖了任务差异，DyLaR在两个基准上仍落后；而Tok/query只统计可见词元，不能据此断言其总FLOPs、显存占用或实际延迟按相同比例下降。

<div class="result-source" markdown="1">

来源：第4.2节 Main Results，表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Although Qwen3-VL-4B-Thinking remains stronger on MMVU and TempCompass, DyLaR achieves the best overall average while generating only 18.5 visible tokens per query, compared with 1,220.7 tokens from Qwen3-VL-4B-Thinking and 3,572.3 tokens from explicit CoT prompting.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen2.5-VL-7B骨干上与近期专用视频推理方法比较

<div class="result-value" markdown="1">

DyLaR平均准确率达到57.5%，高于VideoAuto-R1的57.0%、Open-o3-Video的56.2%、Mull-Token的55.8%、Video-R1的55.4%和VideoRFT的55.3%；其Tok/query为18.2，也低于上述方法的40.1、162.1、27.0、415.2和358.9。

</div>

这是较严格的同骨干比较，说明DyLaR的优势不只来自换用更新的Qwen3模型，并且相较已有紧凑推理方法Mull-Token仍同时获得更高平均准确率与更少可见词元。但各方法仍可能具有不同训练数据、优化目标和官方解码配置，因此结果不能单独把增益完全归因于某一个结构部件。

<div class="result-source" markdown="1">

来源：第4.2节 Main Results，表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Meanwhile, DyLaR uses only 18.2 tokens on average, compared with 27.0 for Mull-Token, 40.1 for VideoAuto-R1, 162.1 for Open-o3-Video, 415.2 for Video-R1, and 358.9 for VideoRFT.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨InternVL3.5-4B与LLaVA-OneVision-7B骨干的迁移验证

<div class="result-value" markdown="1">

在InternVL3.5-4B上，DyLaR将平均准确率从CoT基线的54.0%提高到56.7%，Tok/query从173.9降至13.4；在LLaVA-OneVision-7B上，平均准确率从49.7%提高到54.2%，Tok/query由14.1变为17.8。

</div>

两个非Qwen骨干均获得平均准确率提升，支持该训练与响应机制具有跨模型家族的可迁移性。LLaVA基线因未稳定遵循CoT指令而只输出14.1个词元，所以该组不能证明DyLaR更短；它证明的是在相近可见预算下准确率更高。四个骨干仍都属于多模态语言模型，不能外推到任意视频架构。

<div class="result-source" markdown="1">

来源：第4.2节 Main Results，表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On LLaVA-OneVision-7B, it improves the average from 49.7 to 54.2. Its CoT baseline emits few visible tokens (14.1) due to weak adherence to the CoT instruction, yet DyLaR still gains 4.5 points at a comparable budget (17.8).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主评测统一使用16帧均匀采样，每帧最多307200像素。虽然作者报告增加到32帧和64帧时平均准确率继续上升，固定稀疏采样仍可能遗漏短暂事件；同时，论文没有在给定节选中报告端到端延迟、FLOPs、峰值显存或潜变量计算成本，因此Tok/query不能代表完整效率。
- 所有评测题都被处理为字母多项选择题，格式不服从时还使用LLM裁判提取选项；MMVU的375道开放题被排除。由此得到的准确率不能直接说明模型能否生成可靠的开放式答案或忠实解释。此外，训练证据框和理由由大型模型生成并由另一模型过滤，尽管附录提到人工审计，当前节选未给出审计规模与误差率，监督噪声风险仍需源文核查。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 同骨干显式文本思维链基线：Qwen2.5-VL-7B-Instruct、Qwen3-VL-4B-Instruct、InternVL3.5-4B-Instruct和LLaVA-OneVision-7B均配合CoT提示。它们用于判断潜空间方案是否优于在词表空间直接生成理由；同骨干比较也降低了参数规模和预训练差异的干扰。
- Qwen3-VL-4B-Thinking：与主模型DyLaR共享Qwen3-VL-4B家族，是具有长推理输出的直接强基线，用于比较准确率与可见推理开销之间的权衡。
- Qwen2.5-VL-7B视频推理方法：Video-R1、VideoRFT、Open-o3-Video、VideoAuto-R1和Mull-Token均建立在相同骨干上，覆盖长思维链强化学习、自适应推理及紧凑词元方法，用于检验DyLaR相对近期专用视频推理系统的竞争力。
- GPT-4o与Gemini-1.5-Pro：仅作为前沿闭源模型的性能尺度参照。作者明确指出其推理设置可能不同，因此不能将其结果视为严格受控的直接对比。

**实验想回答的问题**

- 在统一视频输入协议下，DyLaR能否跨不同多模态语言模型骨干，在九个视频问答基准上同时提高选择题准确率并减少可见输出词元，从而验证潜空间感知与推理相较长文本思维链的效用？
- 性能提升究竟来自哪些设计：基于局部视觉证据的感知潜变量、由文本理由监督的推理潜变量、按问题难度选择推理分支的自适应路由，以及后续强化学习是否分别产生可辨别的贡献？

**实验实现**

四种骨干采用同一流程：先进行1轮监督微调，再进行2500步GRPO强化学习；冻结视觉编码器和多模态投影器，仅更新语言模型参数。训练数据来自Video-R1-CoT及LongVideo-Reason、CG-Bench、Video-Holmes和MLVU训练集；候选证据框和理由由Qwen3.5-397B-A17B生成，并由独立的Kimi-K2.5过滤，最终约保留2万条SFT样本和3万条RL样本。训练与主评测均匀采样16帧，每帧最多307200像素；推理采用贪心解码，感知与推理潜变量预算分别固定为$K_p=4$和$K_r=6$。本地基线和DyLaR共享16帧视觉协议并使用完整官方题集，但各模型沿用其官方提示模板与解码配置；若CoT或Thinking模型未按要求输出选项，则使用LLM裁判识别答案。作者因此提醒，统一协议下的表1结果不能直接与各方法论文原始报告值比较。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Qwen3-VL-4B在LVBench、16帧且尚未进行RL时的SFT目标消融 | 完整DyLaR SFT总体准确率为40.5%；去除推理潜变量、理由监督、感知证据定位以及自适应路由后，分别降至39.1%、38.3%、38.7%和39.1%。三种文本推理或答案监督基线仅为38.9%、39.0%和38.7%。 | 该实验分别隔离了“是否保留潜空间推理”“推理潜变量是否由验证理由监督”“感知潜变量是否对齐局部证据”和“是否按需路由”。四项移除均降低总体准确率，其中去除理由监督降幅最大，支持潜变量需要明确的语义监督，而不只是增加隐藏计算步。由于实验只在LVBench和SFT阶段进行，且类别分数并非每项都一致下降，这些结论主要适用于总体初始化质量，不能证明每个部件对所有任务类型都同等有效。 | 表2，第4.3节 SFT objective ablation<br><span class="experiment-evidence">DyLaR SFT \| 41.5 \| 41.7 \| 39.2 \| 36.3 \| 34.5 \| 32.8 \| 40.5; w/o reasoning latents \| 40.2 \| 40.0 \| 38.1 \| 39.8 \| 34.5 \| 25.9 \| 39.1; w/o reasoning supervision \| 38.0 \| 37.7 \| 42.3 \| 35.3 \| 32.7 \| 32.8 \| 38.3; w/o perception grounding \| 38.1 \| 38.3 \| 39.2 \| 41.3 \| 34.1 \| 34.5 \| 38.7; w/o adaptive routing (mandatory latent reasoning) \| 39.1 \| 39.4 \| 38.5 \| 40.3 \| 33.2 \| 29.3 \| 39.1</span> |
| SFT之后加入GRPO强化学习的跨骨干消融 | RL使九基准平均准确率在Qwen2.5-VL-7B上由56.0%升至57.5%，在Qwen3-VL-4B上由56.8%升至58.2%，在InternVL3.5-4B上由55.6%升至56.7%，在LLaVA-OneVision-7B上由53.0%升至54.2%，对应提升1.5、1.4、1.1和1.2个百分点。 | 该比较隔离了SFT初始化之后RL精炼的增量价值，四个骨干的平均值均上升，说明RL收益具有一定一致性。但单项基准并非全部改善，例如Qwen3的LVBench和MMVU、InternVL的LongVideo-Reason和Video-TT、LLaVA的Video-Holmes出现下降，因此RL更像是在总体任务分布上重新优化，而不是无条件改善每项能力。 | 附录E.1，表4<br><span class="experiment-evidence">Table 4 reports the per-backbone breakdown of the SFT → RL comparison summarised in Section 4.3, where RL improves the nine-benchmark average on all four backbones by +1.1 to +1.5 points.</span> |

**定性案例**

- 图2分析一个必须跨帧结合“1997”和“2002”两条线索的时序问答样例。作者观察到DyLaR的高斯平滑视觉块注意力热图集中在这两个诊断性线索及其支持区域，而Qwen3-VL-4B-Instruct CoT与Qwen3-VL-4B-Thinking的注意力更分散或发生偏移。该可视化与“先保存局部视觉证据再作答”的机制一致，并提供非文本解释线索；但它只是单个案例，注意力集中也不等同于因果解释，不能替代大规模定位评测。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces adaptive latent perception and reasoning for video question answering while substantially reducing generated reasoning tokens.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`39c06bcab11c888c3f2d5a12399a2e8f43f9de2e6d70fbccb00fbd9947cc8085`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
