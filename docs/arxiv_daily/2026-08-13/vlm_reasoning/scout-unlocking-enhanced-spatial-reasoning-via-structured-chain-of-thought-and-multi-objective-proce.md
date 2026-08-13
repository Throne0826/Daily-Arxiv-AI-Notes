---
title: "[论文解读] SCOUT: Unlocking Enhanced Spatial Reasoning via Structured Chain-of-Thought and Multi-Objective Process Reward"
description: "[arXiv 2608.12220][VLM Reasoning] SCOUT通过显式组织“空间感知—逻辑分析—答案生成”的推理过程，并用分阶段过程奖励训练视觉语言模型，以同时补足三维空间表征和中间推理信用分配能力。"
arxiv_id: "2608.12220"
announcement_date: "2026-08-13"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:52:04.025112+00:00"
source_sha256: "a38ad345c0e2ffd80b2f8093737cbd91e8aecaaa3eaa78d2ab74f372bb255fe7"
tags:
  - "VLM Reasoning"
  - "LLM Reasoning"
  - "多模态 VLM"
  - "视觉语言模型"
  - "空间推理"
  - "三维空间感知"
  - "结构化思维链"
  - "可验证奖励强化学习"
  - "过程奖励"
  - "信用分配"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.12220</p>

# SCOUT: Unlocking Enhanced Spatial Reasoning via Structured Chain-of-Thought and Multi-Objective Process Reward

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Zile Zhou, Huining Yuan, Weichen Zhang, Xinlei Chen, Xiao-ping Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Shenzhen International Graduate School, Tsinghua University, Shenzhen, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12220v1) · [PDF 下载](https://arxiv.org/pdf/2608.12220v1) · **关键词** 视觉语言模型, 空间推理, 三维空间感知, 结构化思维链, 可验证奖励强化学习, 过程奖励, 信用分配<br>


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

SCOUT通过显式组织“空间感知—逻辑分析—答案生成”的推理过程，并用分阶段过程奖励训练视觉语言模型，以同时补足三维空间表征和中间推理信用分配能力。

**不用术语来说**：视觉语言模型虽然能识别图像内容，却常难以可靠判断物体的前后、远近、相对位置及视角变化，因为正确答案不仅依赖“看见了什么”，还依赖先恢复场景的空间结构，再据此逐步推断。现有训练方式要么要求大量人工或合成数据并容易让模型记住固定模式，要么只在最终答案处给分，无法判断中间哪一步看错或推错，因此难以形成稳健、可迁移的空间推理能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出深度感知的结构化思维链，将推理轨迹拆分为空间感知与逻辑分析等可独立提取的部分，要求模型显式描述物体边界框、深度及场景信息，使后续结论建立在三维环境表征之上。
- 提出结合多目标过程奖励与定制优势估计的强化学习方法，分别监督边界框感知、深度感知和推理—答案一致性，并将奖励归因到对应推理片段；同时构建覆盖基础空间关系、相对距离和复杂视角变换的SCOUT-24k结构化推理数据集，为冷启动与后续强化学习提供训练基础。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于视觉语言模型（VLM）的空间推理研究。模型需要从图像与语言问题中识别物体、理解物体间的方向和距离关系，并在涉及视角变化等复杂条件时完成推导；这类能力直接关系到机器人导航与操作、自动驾驶和虚拟现实。现有模型虽能处理一般视觉语言任务，但对三维空间的理解仍不稳健，尤其容易忽略深度线索。相关训练路线主要包括监督微调（SFT）和带可验证奖励的强化学习（RLVR）：前者依靠标注或合成推理数据学习答案与模板，数据和计算开销较高且可能形成模板记忆；后者依据最终答案是否正确提供奖励，通常更有利于学习可泛化的推理策略，但稀疏的结果奖励难以判断中间步骤各自应承担多少功劳或责任。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**结构化思维链（Structured Chain-of-Thought）**

将推理过程划分为具有明确功能的阶段，而不是生成一段无固定组织的解释。本文所需的关键结构是先提取包含物体位置与深度的三维环境信息，再基于这些观察进行逻辑分析并给出答案。

</div>
<div class="concept-item" markdown="1">

**带可验证奖励的强化学习（RLVR）**

模型生成推理轨迹和答案后，系统利用可自动检查的正确性信号计算奖励，并据此更新生成策略。若只在答案末尾给出一个总体奖励，就难以区分哪些中间推理步骤有效、哪些步骤造成错误。

</div>
<div class="concept-item" markdown="1">

**过程奖励与信用分配**

过程奖励直接评价推理轨迹中的特定行为，例如物体边界框定位、深度感知以及推理与答案的一致性；信用分配则决定这些评价如何影响不同阶段或词元的参数更新。直观地说，它不仅判断最终答案对不对，还尝试定位推理过程中具体哪里做得好或做得差。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一幅图像及其空间推理问题，输出包括结构化推理轨迹和最终答案。论文假设单幅二维图像包含可用于恢复三维关系的物体位置与深度线索，因此模型首先显式抽取物体边界框、相对深度和场景信息，再依据这些空间观察完成关系判断、相对距离预测或视角变换等推理。训练采用两阶段设置：先用SCOUT-24k中的结构化思维链进行SFT冷启动，使模型学会规定的输出结构；再通过强化学习，分别评价感知阶段、分析阶段与最终结果，并将奖励分配到对应的推理片段。论文训练数据仅包含单图像样本，同时考察模型能否将所学空间原则迁移到多图像和视频场景。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\pi_\theta$**

由参数θ控制的视觉语言生成策略；给定图像和问题后生成结构化推理轨迹及答案。原文节选未给出该符号的正式定义，此处仅作问题设置中的通用记号。

</div>
<div class="notation-item" markdown="1">

**$x$**

模型输入，由图像与对应的空间推理问题组成；原文节选未规定正式符号。

</div>
<div class="notation-item" markdown="1">

**$y$**

模型生成的完整输出，包括三维感知信息、逻辑分析过程和最终答案；原文节选未规定正式符号。

</div>
<div class="notation-item" markdown="1">

**$r$**

训练时用于评价输出的奖励信号，可涵盖边界框、深度感知、推理一致性和最终答案等目标；原文节选未给出具体公式或统一符号。

</div>

</div>

**直接相关的工作**

- **基于监督微调的空间推理方法（第4.1节，引用[7, 8, 5, 11, 37, 30, 17, 19]）**: 这类方法通过大规模合成数据后训练，或加入专用几何编码器来增强空间表征。作者认为其主要不足是数据与计算成本较高、专用结构限制模型架构的通用性，而且SFT模型可能记忆训练模板而非掌握可迁移的空间规律；SCOUT仍使用SFT作为冷启动，但将主要能力优化交给后续过程监督强化学习。
- **空间推理与结构化思维链的可验证强化学习方法（第4.2节，引用[36, 26, 39, 47, 34, 4, 20]）**: 这些方法利用思维链和可验证的最终结果奖励提升空间推理，部分工作还用结构化模板增强感知或解释性。作者指出其结构通常没有显式纳入深度信息，且稀疏的结果奖励无法准确评价中间步骤；SCOUT针对这两个缺口，引入深度感知型结构化思维链、多目标过程奖励和细粒度优势估计。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

机器人导航与操作、自动驾驶和虚拟现实等应用要求模型理解真实环境中的三维关系，而不仅是识别二维图像中的对象。模型必须区分物体的前后、远近和相对方位，并在视角变化下进行连续推断；一旦空间感知或中间推理出错，最终动作即使语言表达流畅，也可能与物理环境不一致。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于大规模空间数据的监督微调**：利用带有辅助空间表示或合成标注的数据直接训练模型模仿目标答案与推理文本，使其学习常见空间关系和固定解题格式。
- **结果可验证强化学习与结构化思维链**：结果可验证强化学习依据最终答案是否正确提供奖励，并配合思维链生成推理步骤；结构化思维链则用预定义模板把感知和分析过程组织成可读的模块，以增强推理轨迹的可解释性。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 监督微调依赖大量合成数据及高成本的数据整理，而且以模仿为主的训练容易形成模式记忆；其后果是模型可能适应训练分布中的固定表达，却难以把空间规律迁移到新场景、不同视角或新任务。
- 仅使用最终答案奖励时，奖励信号稀疏，无法准确判断错误源于对象定位、深度估计还是逻辑推导；已有结构化模板又通常缺少深度信息，也没有为不同推理模块分别计分，因此二维描述不足以支撑完整三维理解，强化学习还可能把同一成败信号错误地分配给整条推理轨迹。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未形成一个统一训练框架：既能在推理表示中显式纳入深度和对象位置等三维线索，又能利用这些结构化模块进行可验证的局部监督，把不同过程奖励精确分配到相应推理片段。换言之，三维感知结构与细粒度强化学习信用分配此前没有被协同设计。

</div>
<div markdown="1"><span>核心问题</span>

能否把视觉空间推理拆成可独立检查的三维感知与逻辑分析阶段，并为边界框、深度和推理一致性分别构造过程奖励及优势信号，从而使视觉语言模型学到比纯监督微调或最终答案奖励更稳健、更可解释且更具跨场景泛化能力的空间推理策略？

</div>
<div markdown="1"><span>作者直觉</span>

如果模型必须先写出对象在哪里、谁更近以及场景如何组织，再根据这些观察推导答案，训练系统就能定位错误发生在哪个环节。边界框奖励校验“找得准不准”，深度奖励校验“前后远近看得对不对”，一致性奖励校验“结论是否真的由前述观察推出”；再把各奖励只作用于相关推理片段，便可避免因最终答案偶然正确而奖励错误过程，也避免因最后一步失误而否定此前正确感知。严格结构因此不仅提高可读性，更充当过程监督与精确信用分配的接口。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SCOUT 是一个“数据构造、结构化监督微调、过程监督强化学习”相互配合的空间推理框架。输入是单幅图像与空间问题；模型先在 $\langle\mathrm{caption}\rangle$ 中概括场景，再在 $\langle\mathrm{scene}\rangle$ 中显式输出关键对象的语义标签、二维边界框和深度，随后在 $\langle\mathrm{analyze}\rangle$ 中依据这些三维线索完成比较、视角转换或关系推导，最后在 $\langle\mathrm{answer}\rangle$ 中给出答案。训练分为两阶段：先用 SCOUT-24k 做监督微调，使模型掌握固定推理格式；再以五种奖励分别检查定位、深度、推理一致性、答案正确性和格式，并把不同优势分配给感知、分析和答案区段的 token。
该方法的关键不是简单增加更多奖励，而是建立“哪个步骤由哪个反馈负责”的对应关系：场景描述部分主要接受定位与深度反馈，逻辑分析部分主要接受一致性反馈，最终答案部分接受格式与准确率反馈；同时，前两部分还混入最终结果优势，避免模型把中间格式或局部指标做得很好却答错问题。通俗地说，SCOUT 像把空间题的解答拆成“看清物体、建立三维草图、按草图推理、填写答案”四段，并分别批改每一段，而不是只看最后选项是否正确。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### SCOUT-24k 场景信息构造

使用 Qwen-VL-Max 生成场景描述，并用 Depth-Anything-3 估计单目深度；对每个对象，在其边界框中心采样坐标 $(u,v,z)$，再整理为 JSON 场景表示。这里 $u,v$ 是图像平面坐标，$z$ 是估计深度。

<div class="method-step__io" markdown="1">

**输入**：来自 EmbSpatial 与 STVQA 的图像，以及原数据提供的对象标签、二维边界框和部分答案标注。<br>
**输出**：包含场景描述、对象语义标签、边界框和中心深度的结构化感知真值。

</div>

**直观理解**：这一阶段把图片转换成可计算的“三维物体清单”。模型之后不必只凭模糊视觉印象推理，而能明确比较物体在哪里、离相机多远。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 空间问题与推理链合成及筛选

依据三维空间信息合成相对距离与视角转换等任务的推理步骤和答案；再让 Qwen-VL-Max 根据场景描述与合成步骤预测答案，只保留预测与真值一致的样本，并由人工专家复核和修订。STVQA 与 EmbSpatial 中已有答案的样本只执行感知构造阶段，随后用于强化学习。

<div class="method-step__io" markdown="1">

**输入**：结构化场景表示、原始问答标注，以及由 CV-Bench 和 Spatial-SSRL 改编的任务模板。<br>
**输出**：覆盖空间关系理解、相对距离预测、视角转换推理和对象中心空间推理四类任务的 SCOUT-24k 数据。

</div>

**直观理解**：自动模板负责扩大数据规模，模型筛选与人工复核负责减少错误推理链。这样得到的数据不仅有答案，还展示了从场景信息到答案的中间过程。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结构化 CoT 冷启动

通过监督微调约束模型依次生成 $\langle\mathrm{caption}\rangle$、$\langle\mathrm{scene}\rangle$、$\langle\mathrm{analyze}\rangle$ 和 $\langle\mathrm{answer}\rangle$，并将前三部分包在 $\langle\mathrm{think}\rangle$ 内。该阶段先建立稳定的输出边界，供后续强化学习识别不同功能区段。

<div class="method-step__io" markdown="1">

**输入**：图像、问题，以及带有结构标签的空间推理示例。<br>
**输出**：能够按照指定模块化格式生成空间推理轨迹的初始策略模型。

</div>

**直观理解**：强化学习开始前，模型先学会规范地写出“观察、分析、答案”。明确的段落边界既降低训练初期的格式混乱，也让系统知道每条奖励应批改哪一段。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多目标过程奖励计算

先用匈牙利算法按语义相似度、EIoU 和深度一致性匹配预测对象与真值对象，再计算带过生成惩罚的定位奖励和连续深度奖励；另以盲验证器检查推理链能否在不看图像时推出真值，并计算二值准确率与格式奖励。

<div class="method-step__io" markdown="1">

**输入**：同一问题下模型生成的一组结构化回答，以及对象、深度和最终答案真值。<br>
**输出**：每个生成样本的五个奖励：$r_{\mathrm{grounding}}$、$r_{\mathrm{depth}}$、$r_{\mathrm{consistency}}$、$r_{\mathrm{accuracy}}$ 和 $r_{\mathrm{format}}$。

</div>

**直观理解**：五项反馈分别回答“物体找得准不准、远近估得准不准、推理是否支持答案、答案是否正确、格式是否合规”。其中盲验证器不看图，是为了检查文字推理本身是否连贯，而不是重新依赖视觉猜答案。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 阶段优势构造、混合与 token 级分配

$$
\tilde{r}_{k}^{(i)}=\frac{r_{k}^{(i)}-\mu_k}{\sigma_k},\quad \mathcal{A}_{\mathrm{scene}}=\tilde{r}_{\mathrm{grounding}}+\tilde{r}_{\mathrm{depth}},\quad \mathcal{A}_{\mathrm{analyze}}=\tilde{r}_{\mathrm{consistency}},\quad \mathcal{A}_{\mathrm{outcome}}=\tilde{r}_{\mathrm{format}}+\tilde{r}_{\mathrm{acc}},\\ \hat{A}_{\mathrm{scene}}=\alpha_1\mathcal{A}_{\mathrm{scene}}+(1-\alpha_1)\mathcal{A}_{\mathrm{outcome}},\quad \hat{A}_{\mathrm{analyze}}=\alpha_2\mathcal{A}_{\mathrm{analyze}}+(1-\alpha_2)\mathcal{A}_{\mathrm{outcome}},\\ A_t=\begin{cases}\hat{A}_{\mathrm{scene}},&t\le T_{\mathrm{scene}},\\ \hat{A}_{\mathrm{analyze}},&T_{\mathrm{scene}}<t\le T_{\mathrm{think}},\\ \mathcal{A}_{\mathrm{outcome}},&t>T_{\mathrm{think}}.\end{cases}
$$

**符号说明**

- $r_k^{(i)}$：同一生成组内第 i 个样本的第 k 类原始奖励
- $\mu_k$：生成组内第 k 类奖励的均值
- $\sigma_k$：生成组内第 k 类奖励的标准差
- $\tilde r_k^{(i)}$：经过组内 z-score 标准化的第 k 类奖励
- $\mathcal A_{\mathrm{scene}}$：由定位与深度奖励组成的场景感知基础优势
- $\mathcal A_{\mathrm{analyze}}$：由盲验证一致性奖励组成的分析基础优势
- $\mathcal A_{\mathrm{outcome}}$：由格式奖励和最终答案准确率奖励组成的结果优势
- $\hat A_{\mathrm{scene}}$：混合局部场景优势与全局结果优势后的感知区段优势
- $\hat A_{\mathrm{analyze}}$：混合局部分析优势与全局结果优势后的推理区段优势
- $\alpha_1,\alpha_2$：局部过程优势的混合权重，取值位于 [0,1]；其余权重分配给结果优势
- $A_t$：分配给第 t 个生成 token 的优势
- $T_{\mathrm{scene}}$：结束 scene 区段的标签所在 token 索引
- $T_{\mathrm{think}}$：结束整个思考区段的标签所在 token 索引
- $t$：生成序列中的 token 时间步

<div class="equation-explanation" markdown="1">

**直观理解**：第一行先把量纲不同的五类奖励变成组内可比较的相对分数，再按场景、分析和结果三个功能聚合。第二行把局部过程质量与最终任务成败混合；最后一行利用结构标签把相应优势发给对应 token，从而实现细粒度信用分配。<br>
**原文位置**：第 2.3 节，公式 (4) 至 (7)

</div>

</div>

<div class="equation-block" markdown="1">

#### 带 KL 正则的裁剪策略优化目标

$$
\mathcal{J}(\theta)=\mathbb{E}_{t}\left[\min\left(\rho_t(\theta)A_t,\operatorname{clip}(\rho_t(\theta),1-\epsilon,1+\epsilon)A_t\right)\right]-\beta D_{\mathrm{KL}}(\pi_\theta\|\pi_{\mathrm{ref}}),\quad \rho_t(\theta)=\frac{\pi_\theta(y_t\mid x,y_{<t})}{\pi_{\mathrm{old}}(y_t\mid x,y_{<t})}
$$

**符号说明**

- $\mathcal J(\theta)$：需要最大化的强化学习目标
- $\theta$：当前视觉语言策略模型的可训练参数
- $\mathbb E_t$：对生成序列各 token 时间步求期望
- $\rho_t(\theta)$：当前策略与采样时旧策略在第 t 个 token 上的条件概率比
- $A_t$：由功能区段决定的第 t 个 token 优势
- $\operatorname{clip}(\cdot)$：将概率比限制在指定区间的裁剪操作
- $\epsilon$：概率比裁剪区间 [$1-\epsilon,1+\epsilon]$ 的半宽
- $\beta$：控制 KL 正则强度的自适应系数
- $D_{\mathrm{KL}}$：衡量当前策略偏离参考策略程度的 KL 散度
- $\pi_\theta$：参数为 θ 的当前策略
- $\pi_{\mathrm{old}}$：生成训练样本时使用的旧策略
- $\pi_{\mathrm{ref}}$：用于约束策略漂移的参考模型
- $x$：模型输入，包括视觉内容与文本问题
- $y_t$：生成序列在时间步 t 的 token
- $y_{<t}$：时间步 t 之前已经生成的 token 前缀

<div class="equation-explanation" markdown="1">

**直观理解**：概率比衡量新策略相对旧策略更倾向于生成某个 token 的程度；若该 token 的分段优势为正，优化会提高其概率，反之会降低。裁剪项限制单次更新幅度，KL 项进一步约束模型不要偏离参考策略过远，从而在利用过程奖励的同时保持训练稳定。<br>
**原文位置**：第 2.3 节，公式 (8)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是最大化带 token 级优势的裁剪代理目标 $\mathcal J(\theta)$，同时以 $\beta D_{\mathrm{KL}}(\pi_\theta\|\pi_{\mathrm{ref}})$ 抑制策略过度偏离参考模型。与标准 GRPO 的核心差异在于，$A_t$ 不再是整条回答共享的单一优势：感知 token 使用定位、深度与结果混合优势，分析 token 使用一致性与结果混合优势，答案 token 使用格式与准确率构成的结果优势。因而梯度能够针对错误发生的位置更新，又不会失去最终答案正确性这一全局锚点。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 显式三维结构化 CoT**

推理轨迹采用固定顺序：场景语义描述、对象级场景表示、逻辑分析和最终答案。$\langle\mathrm{scene}\rangle$ 不只列出二维位置，还显式记录对象深度，使相对距离、遮挡相关判断和视角转换可以基于三维线索展开。

> 直观理解：普通 CoT 可能直接用语言猜测空间关系，SCOUT 则要求先画出一份带远近信息的“文字三维草图”。这份草图把视觉感知与逻辑推导连接起来，也提供了可单独检查的中间结果。

**2. 正则化定位与多目标过程验证**

对象匹配成本同时考虑标签语义、边界框 EIoU 和深度一致性；匹配后，定位奖励以平均 EIoU 衡量质量，并用系数 $\eta$ 惩罚预测对象数超过真值对象数的部分，以抑制通过大量输出边界框碰运气的奖励投机。深度奖励连续衡量 $z$ 轴误差，盲一致性奖励则检查生成推理是否足以推出真值。

> 直观理解：只奖励命中的边界框会诱使模型多报物体，因此必须同时惩罚过量预测。连续深度反馈比简单判定对错提供更细的改进方向，而一致性检查避免模型虽然选对答案，却写出与答案无关或错误的理由。

**3. 面向功能区段的优势估计**

SCOUT 不沿用标准 GRPO 对整条回答赋予同一个优势，而是依据 $\langle/\mathrm{scene}\rangle$ 与 $\langle/\mathrm{think}\rangle$ 的位置划分感知、分析和答案 token。局部优势分别由对应过程奖励构成，并以 $\alpha_1$、$\alpha_2$ 与结果优势混合；文中默认 $\alpha_1=\alpha_2=0.3$。

> 直观理解：若整篇解答只得到一个总分，训练系统无法判断错误来自看错物体、推理断裂还是答案格式。分段优势相当于把总评改成分项评分，同时仍让每一项对最终答对负责。

**训练与推理**

训练时，首先由 SCOUT-24k 的结构化推理样本执行 SFT 冷启动，使基础视觉语言模型掌握固定标签、对象级场景表示和显式分析流程。随后对每个图像问题采样一组回答：解析结构标签；用匈牙利匹配建立预测对象与真值对象的对应；计算定位、深度、一致性、准确率和格式奖励；在组内分别标准化各奖励；构造三个阶段的优势并按 token 区段分配；最后最大化裁剪目标并加入 KL 正则更新策略。文中将 $\alpha_1$ 与 $\alpha_2$ 均设为 $0.3$，表示中间段优势仍以最终结果反馈为主要锚点。
推理时不再需要真值对象、奖励模型、匈牙利匹配或策略更新。给定图像和问题，训练后的模型自回归地产生完整轨迹：先概括场景，再输出对象边界框和深度，随后执行显式空间分析，最终输出答案。虽然数据构造阶段借助 Qwen-VL-Max 和 Depth-Anything-3 生成或筛选监督信号，但原文节选没有说明部署推理时需要额外调用这些外部模型；因此应将它们理解为训练数据生产工具，而非已明确报告的在线推理组件。

**复现信息**

公平复现时需要保留三项关键设置。第一，对象匹配成本同时使用语义、EIoU 和深度项，其权重分别为 $\lambda_{\mathrm{sem}}=2.0$、$\lambda_{\mathrm{iou}}=3.0$、$\lambda_{\mathrm{dep}}=0.5$；定位奖励对预测对象数超过真值对象数的部分施加系数 $\eta=0.2$ 的惩罚。第二，深度一致性采用 $\delta(d_i,d_j)=\exp(-2|d_i-d_j|/d_j)$，其中 $d_i$ 和 $d_j$ 分别是预测与真值深度；该连续函数使相对深度误差越大，奖励越低。第三，默认局部过程权重为 $\alpha_1=\alpha_2=0.3$，且每类奖励必须先在同一生成组内独立标准化，否则不同奖励的数值尺度会改变预期的优势混合关系。
其余会显著影响复现的配置，如基础 VLM 的确切检查点、SFT 与强化学习的学习率、批量大小、每题采样数、裁剪系数 $\epsilon$、KL 系数 $\beta$ 的自适应规则、语义相似度模型、盲验证所用基础模型及解码参数，在所给方法节选中均未明确报告。因而只能复现算法结构，不能仅凭该节选完整复现训练数值。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 通用单图空间理解组：EmbSpatial 测试左/右、上/下、远/近等基础关系；CV-Bench 测试二维关系、物体计数、深度排序和距离推理；BLINK 仅使用 Relative Depth 子集，重点检查相对深度感知。原文未在所给章节中明确报告各测试集规模与具体划分；三者用于表 1 的通用空间能力评估。
- 复杂单图空间推理组：RoboSpatial 的 Configuration 与 Compatibility 子集模拟具身环境中的物体配置和兼容性判断；SpatialBench 涵盖物体存在、位置关系、可达性等物理交互及尺寸比较；3DSRBench 面向真实场景三维推理，并细分高度、位置、朝向和多物体任务。原文未明确报告规模与划分；三者用于表 2 的复杂推理评估。
- 域外输入组：ViewSpatial 用多图输入测试相机视角和人物视角下的方向、物体视图与朝向推理；VSI-Bench 用视频输入测试数值题与选择题，包括计数、尺寸/房间大小/绝对距离估计、相对方向、相对距离、出现顺序和路线规划。它们不属于 SCOUT 的单图训练域，用于检验跨视觉格式迁移；原文未明确报告规模与划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率（Accuracy）**

预测答案与基准真值一致的样本比例，是全部任务的主要指标；各表中的 Overall 或 Avg. 是相应任务或子任务准确率的汇总。 （越高越好，因为更高数值表示正确完成空间判断的样本比例更大；但它不直接衡量推理过程是否忠实或三维表征是否真实。）

</div>
<div class="metric-item" markdown="1">

**VSI-Bench 数值题准确率（NQ）**

衡量视频中的物体计数、物体尺寸、房间尺寸和绝对距离等数值估计能力，侧重动态场景中的跟踪与定量判断。 （越高越好；该指标可以区分关系型空间推理提升与绝对数值估计能力，避免总体分数掩盖数值任务退化。）

</div>
<div class="metric-item" markdown="1">

**VSI-Bench 多项选择题准确率（MCQ）**

衡量视频中的相对方向、相对距离、出现顺序和路线规划等选择式空间推理能力。 （越高越好；它主要反映在候选答案约束下识别结构化空间关系与时序关系的正确率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 通用单图空间基准：EmbSpatial、CV-Bench 与 BLINK，分别比较 3B/7B 同规模模型及 GPT-4o。

<div class="result-value" markdown="1">

作者报告 SCOUT-3B 的 Overall 为 77.56，比基础 Qwen2.5-VL-3B 的 60.71 高 16.85 个百分点，也高于 GPT-4o 的 75.38；SCOUT-7B 的 Overall 为 79.66，比基础 Qwen2.5-VL-7B 的 70.15 高 9.51 个百分点，并比 GPT-4o 高 4.28 个百分点。SCOUT-7B 在 EmbSpatial、CV-Bench、BLINK 的三个分项上分别达到 78.76、78.85 和 79.03，均超过 GPT-4o 的 70.27、75.44 和 76.61。

</div>

这组结果最有力地说明，收益并非只出现在某一种基础空间关系上：SCOUT 同时改善了基础关系、二维/三维综合判断和相对深度。与同规模 Qwen2.5-VL 的差距支持“专门训练有效”，但不能仅凭主结果判定增益来自结构化思维链、过程奖励还是训练数据，因为这些因素同时发生变化。超过 GPT-4o 只适用于所列零样本基准及当前评测协议，不代表通用视觉能力全面超过 GPT-4o。

<div class="result-source" markdown="1">

来源：第 3.2 节 Main Results，表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Most remarkably, SCOUT-7B strictly outperforms the proprietary GPT-4o across all individual benchmarks. Impressively, even our smaller SCOUT-3B variant achieves a higher overall score (77.56) than GPT-4o (75.38), decisively demonstrating the effectiveness of our proposed method.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 复杂单图空间推理：RoboSpatial、SpatialBench 与 3DSRBench。

<div class="result-value" markdown="1">

SCOUT-3B 的 Overall 为 58.31，高于基础 Qwen2.5-VL-3B 的 52.01，即提升 6.30 个百分点，并略高于同组 SpatialThinker-3B 的 58.04；其中 RoboSpatial 为 72.81，比基础模型的 59.64 高 13.17 个百分点。SCOUT-7B 的 Overall 为 61.79，是表 2 中最高结果，比 GPT-4o 的 60.92 高 0.87 个百分点，也比 SpatialThinker-7B 的 61.50 高 0.29 个百分点。

</div>

复杂任务上的提升小于通用基准，且不同数据集并非一致领先：例如 SCOUT-7B 在 RoboSpatial 上为 71.05，低于 SpatialThinker-7B 的 74.12；在 3DSRBench 上为 48.23，也低于表中 SpatialReasoner-7B 的 53.79。因而更稳妥的结论是 SCOUT 提高了三项复杂任务的综合表现，特别是 SpatialBench，而不是在所有复杂空间子能力上都占优。作者把总体提升解释为复杂推理能力增强，但准确率本身无法排除数据分布适配或答案模式学习。

<div class="result-source" markdown="1">

来源：第 3.2 节 Main Results，表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At the 3B scale, SCOUT achieves 72.81% accuracy on RoboSpatial (+13.17% over Qwen2.5-VL-3B) and secures the highest overall score (58.31) in its group. This advantage amplifies at the 7B scale. Remarkably, SCOUT-7B achieves the highest overall score (61.79) in the entire evaluation, surpassing even the proprietary GPT-4o (60.92).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 域外迁移：模型仅接受单图训练，直接零样本评测多图 ViewSpatial 和视频 VSI-Bench。

<div class="result-value" markdown="1">

在 ViewSpatial 上，SCOUT-3B 从基础模型的 36.20 提升到 38.91，SCOUT-7B 从 38.03 提升到 40.49。在 VSI-Bench 的 MCQ 上，3B 从 31.65 提升到 32.97，7B 从 34.94 提升到 38.07；但 NQ 明显下降，3B 从 25.03 降到 19.26，7B 从 40.52 降到 29.35。

</div>

多图结果及视频选择题结果表明，单图训练获得的结构化关系知识具有一定跨输入格式迁移能力，尤其是方向和关系类判断；但视频数值题的退化说明这种迁移并不全面。结合附录子任务，SCOUT 在部分视频计数题上提高，却在尺寸、房间大小和绝对距离估计上下降，因此不能笼统声称其视频空间能力整体增强。作者将这一缺口归因于动态场景中的时间跟踪和绝对数值估计需求，这一解释合理但尚未通过专门消融验证。

<div class="result-source" markdown="1">

来源：第 3.3 节 Out-of-domain Evaluation，表 3；附录表 11、表 12

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Notably, we observe a performance drop in the numerical questions of VSI-Bench. This indicates a significant gap between the single-image and video domain in terms of temporal object tracking, requiring a more specialized set of spatial reasoning capabilities to perform absolute numerical estimation across dynamic scenes.

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

- Qwen2.5-VL-3B/7B：SCOUT 的直接基础模型。与它们比较可以控制主干架构和参数规模，较清楚地衡量 SCOUT-24k、结构化思维链及强化学习训练带来的净变化。
- SpatialThinker、SpaceOm、SpatialLadder 与 SpatialReasoner：均为 Qwen2.5-VL 生态中的空间专用模型，分别代表结构化空间微调、更深思维链与机器人数据、渐进式空间训练、强化学习与显式三维表示等路线；它们是最有针对性的同架构方法比较。
- InternVL-3.5-4B/8B：强开源通用视觉语言模型，用来判断 SCOUT 的优势是否只来自选择了 Qwen 系列主干，或能否超过另一条通用模型路线。
- GPT-4o：闭源商业多模态模型，作者将其视为闭源训练条件下空间泛化能力的高水平参照；由于训练数据、参数量和推理系统不可控，该比较能说明最终任务表现，但不能单独归因于 SCOUT 的某个组件。

**实验想回答的问题**

- 在严格零样本条件下，SCOUT 的结构化空间推理训练能否稳定提升单图二维、深度与三维空间推理能力，并在相同参数规模下优于基础 Qwen2.5-VL 和已有空间专用模型？
- 仅使用单图训练的 SCOUT 能否迁移到未见过的多图与视频输入；其改进究竟适用于结构化关系推理，还是也能覆盖动态场景中的绝对数值估计？

**实验实现**

SCOUT-3B 与 SCOUT-7B 分别以 Qwen2.5-VL-3B/7B 为主干，按两个阶段训练。冷启动阶段在 SCOUT-24k 的 SFT 子集上训练一轮，对所有线性模块应用秩为 $r=8$ 的 LoRA，学习率为 $1\times10^{-4}$；随后采用论文提出的强化学习算法训练 200 步，全局批量为 128，学习率为 $1\times10^{-6}$，KL 惩罚系数为 $\beta=0.01$。探索时每个提示采样 $N=8$ 条轨迹，温度为 $T=1.0$，每 50 步保存检查点并报告表现最好的检查点。评测采用严格零样本协议和贪心解码，推理温度为 $T=0.0$；对需要显式推理的模型使用与模型相适配的思维链指令。评测管线扩展自 SpatialThinker，以兼容单图、多图和视频输入。选择最佳检查点可能引入验证集选择效应，而所给章节未说明最佳检查点的选择集及重复运行方差。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 表 4 设计了完整 SCOUT-3B 与 SFT、普通思维链 GRPO、去除多目标过程奖励、去除细粒度信用分配、令感知优势权重 $\alpha_1=0$、令推理优势权重 $\alpha_2=0$ 等变体的比较。 | 原文未明确报告：所给来源只包含表 4 的说明文字，没有包含各变体在六个空间基准上的数值行，因此无法判断过程奖励、信用分配、感知优势和推理优势各自带来多大增益，也无法确认完整模型是否在所有基准上占优。 | 该消融原本可分别隔离监督微调、强化学习、过程级奖励、分段信用分配以及感知/推理两类优势项的作用，是验证方法机制的关键实验。但缺少数值意味着当前材料只能确认作者进行了这些比较，不能据此作出任何组件有效性或贡献排序结论。 | 表 4 Ablation study on reward configurations；具体数值行未包含在所给来源节选中<br><span class="experiment-evidence">We compare the full SCOUT-3B model against several baseline variants: Supervised Fine-Tuning (SFT), GRPO with vanilla Chain-of-Thought (GRPO + vanila CoT), GRPO without purposed multi-objective process rewards (w/o Process.), GRPO without fine-grained credit assignment (w/o Credit.), and our method omitting either the perception advantage (α1 = 0) or the reasoning advantage (α2 = 0).</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过显式建模三维感知的结构化思维链和过程奖励强化学习，提升 VLM 的空间推理能力。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`a38ad345c0e2ffd80b2f8093737cbd91e8aecaaa3eaa78d2ab74f372bb255fe7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
