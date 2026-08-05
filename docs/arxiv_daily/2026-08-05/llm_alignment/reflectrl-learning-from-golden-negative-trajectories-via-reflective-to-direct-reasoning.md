---
title: "[论文解读] ReflectRL: Learning from Golden Negative Trajectories via Reflective-to-Direct Reasoning"
description: "[arXiv 2608.03972][对齐 / RLHF] 本文提出 ReflectRL：不再丢弃强专家模型生成的错误推理轨迹，而是让目标模型先识别并修正其中的局部错误，再把这种反思能力迁移到不依赖专家轨迹的直接推理中。"
arxiv_id: "2608.03972"
announcement_date: "2026-08-05"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:38:49.192229+00:00"
source_sha256: "cabdddd5c6622b05652b8c22d8922f9fcd9f2a7306e069f8134f98d4ab743277"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型推理"
  - "在策略训练"
  - "黄金负轨迹"
  - "反思优势"
  - "可验证奖励强化学习"
  - "组相对策略优化"
  - "在策略蒸馏"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.03972</p>

# ReflectRL: Learning from Golden Negative Trajectories via Reflective-to-Direct Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Jinhe Bi, Chennan Zhou, Zengjie Jin, Aniri, Shuo Lu, Wenke Huang, Hu Cao, Xun Xiao, Zhihong Zhu, Volker Tresp, Fei Shen, Yunpu Ma, Tat-Seng Chua</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> National University of Singapore；Ludwig Maximilian University of Munich；University of Munich；Nanyang Technological University；Peking University；Huawei；Heisenberg Research Center；Southeast University；Institute of Automation, Chinese Academy；Munich Center for Machine Learning</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03972v1) · [PDF 下载](https://arxiv.org/pdf/2608.03972v1) · **关键词** 大语言模型推理, 在策略训练, 黄金负轨迹, 反思优势, 可验证奖励强化学习, 组相对策略优化, 在策略蒸馏<br>
**项目页**: [https://github.com/bibisbar/ReflectRL](https://github.com/bibisbar/ReflectRL)

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

本文提出 ReflectRL：不再丢弃强专家模型生成的错误推理轨迹，而是让目标模型先识别并修正其中的局部错误，再把这种反思能力迁移到不依赖专家轨迹的直接推理中。

**不用术语来说**：训练语言模型解决难题时，人们常借用更强模型给出的完整解题过程；但难题恰恰也可能难倒强模型，于是这些包含错误答案的过程通常会被删除。问题在于，它们往往并非从头到尾都错，而是包含较长的正确思路，只在某个局部步骤出错。直接删除会浪费昂贵且有结构的信息，照着模仿又会把错误教给目标模型。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“黄金负轨迹”（Golden Negative Trajectories, GNT）及“反思优势”（Reflection Advantage）：实验观察表明，面对难题时，目标模型在看到高质量专家的失败轨迹并被要求查错后，可能比从零直接求解更容易得到正确答案；过程奖励模型分析与轨迹成分干预进一步把收益归因于高质量有效前缀和局部错误区域的共同作用。
- 作者提出可插接到现有在策略训练中的 ReflectRL，并以“反思到直接策略迁移”逐步减少反思式样本、增加直接推理样本，使训练阶段从 GNT 获得的纠错与恢复能力最终服务于无需专家轨迹的推理；同时发布包含约 6.9 万条专家失败轨迹的 OpenR1-GNT-69k。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型推理能力的在策略后训练研究。在该范式中，模型针对训练问题现场采样推理轨迹，再依据可验证奖励、奖励模型或教师分布更新自身策略；因此，采样轨迹能否提供有效反馈直接决定训练质量。已有方法常借助更强专家模型生成的正确“黄金轨迹”引导强化学习或蒸馏，但在困难问题上专家也可能作答错误，这些失败轨迹通常被过滤。本文关注的核心对象是“黄金负轨迹”：它们虽未得到正确答案，却可能包含较长的有效推理前缀和局部、可定位的错误，因而可作为反思而非模仿的上下文。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**在策略训练（On-policy Training）**

训练数据中的推理轨迹由当前或近期策略自身生成，模型再根据这些轨迹获得的奖励或教师反馈更新参数。它能让训练状态贴近模型实际会遇到的状态，但在难题上容易因正确轨迹稀少而得到稀疏、微弱的学习信号。

</div>
<div class="concept-item" markdown="1">

**可验证奖励强化学习（RLVR）与组相对策略优化（GRPO）**

RLVR利用答案是否通过规则或验证器检查来产生奖励；代表性算法GRPO对同一问题采样一组回答，并以组内奖励均值和标准差归一化每条轨迹的相对优势。它不需要单独的价值网络，但若专家轨迹同样失败，奖励机制就难以区分结构良好的专家失败与低质量的模型自身失败。

</div>
<div class="concept-item" markdown="1">

**在策略蒸馏（OPD）**

学生模型先生成自己的轨迹，训练时再让其逐步预测分布接近固定教师，以减轻离线模仿中的暴露偏差和分布偏移。传统OPD通常把外部轨迹当作应模仿的正面示范，因此不能直接照搬包含错误的专家负轨迹。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

训练数据集由问题—标准答案对$(q,a)$组成，待训练策略$[0m$生成回答轨迹$o=(o_1,\dots,o_{|o|})$；在RLVR设置中，轨迹由验证器给出奖励并用于策略更新，在OPD设置中，学生生成的状态由固定教师提供分布级监督。本文额外假设能够取得强专家在困难问题上的失败轨迹，即黄金负轨迹；目标不是让模型复制这些错误答案，而是在训练时把它们作为反思上下文，使模型识别有效前缀、定位局部错误并尝试修正，同时最终仍能在推理阶段仅依据原问题直接作答。该设定的背景性难点是：标准奖励只看最终成败时，专家失败与普通自生成失败都可能获得负反馈；标准蒸馏则默认教师上下文值得模仿，两者均缺少利用“高质量但最终错误”轨迹的机制。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{D}$**

由问题—标准答案对$(q,a)$构成的训练数据集。

</div>
<div class="notation-item" markdown="1">

**$q, a$**

分别表示输入问题与对应的标准答案。

</div>
<div class="notation-item" markdown="1">

**$o=(o_1,\dots,o_{|o|})$**

模型生成的完整回答或推理轨迹，其中$o_s$是第$s$个词元，$|o|$是轨迹长度。

</div>
<div class="notation-item" markdown="1">

**$\pi_\theta$**

参数为$\theta$的可训练策略；它按自回归方式根据问题及已有前缀$o_{<s}$预测下一词元。

</div>

</div>

**直接相关的工作**

- **Group Relative Policy Optimization（GRPO）**: 论文将其作为RLVR的代表性基础方法：GRPO根据同一问题下多条采样轨迹的组内相对奖励估计优势。ReflectRL所针对的背景局限是，最终奖励为负时，该机制本身无法识别专家失败轨迹中仍然存在的高质量推理结构。
- **On-Policy Distillation（OPD）**: 论文将其作为另一类在策略后训练基础范式：学生在自身生成的轨迹状态上匹配固定教师的预测分布。其相关局限在于外部轨迹通常被视为正面特权信息，而黄金负轨迹含有错误，不能被直接当作示范模仿。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在策略训练依赖模型自己采样推理过程，并由验证器、奖励模型或分布目标提供反馈。对于困难问题，目标模型直接采样时通常很少产生正确轨迹，因而正奖励稀疏、策略更新信号弱。引入强专家轨迹本可改善探索，但专家在这些高难问题上也会失败；若将失败轨迹全部过滤，训练便失去大量由强模型产生、成本较高且仍包含部分正确推理结构的数据。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **可验证奖励强化学习及其轨迹引导变体（RLVR）**：模型在当前策略下生成多个推理轨迹，由可验证答案或验证器赋予奖励，再依据轨迹之间的相对优势更新策略。轨迹引导方法还会利用专家的正确解题过程，把采样导向更可能成功的推理路径。
- **在策略蒸馏（OPD）**：目标模型仍从自身当前分布中学习，但训练时把外部专家轨迹作为教师侧的特权信息，以塑造更有信息量的学习信号；这种设计通常把专家轨迹视为值得模仿的正示范。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- RLVR 的轨迹引导机制依赖正确专家轨迹产生正奖励，并借此形成相对于模型自身失败样本的优势；专家失败轨迹无法产生这种正奖励，标准优势估计也难以区分“包含长段正确推理的高质量失败”与“目标模型自身的低质量失败”，因此不能有效利用前者推动更新。
- OPD 通常要求外部轨迹充当正面示范，但 GNT 本身含有导致错误答案的缺陷；直接模仿会复制错误，而简单过滤又会同时丢失错误前的有效推理前缀以及定位、修复局部错误所需的信息。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种兼容主流在策略目标的机制，能够把专家失败轨迹当作“待诊断的对象”而非正示范或普通负样本，并在不改变最终推理输入形式的前提下，将其中的有效前缀、错误定位和恢复信号转化为可学习的策略改进。

</div>
<div markdown="1"><span>核心问题</span>

能否利用通常被丢弃、但仍含有结构化推理信息的专家负轨迹，持续提升目标模型的推理能力，并把依赖该轨迹的训练收益迁移到推理时的直接作答？

</div>
<div markdown="1"><span>作者直觉</span>

从零解一道难题要求模型同时找到正确方向、展开步骤并避免错误；若先给出强专家的一条失败过程，模型便可沿着其中较可靠的前半段继续，只需重点发现并修复少数局部错误。作者将这种相对容易的学习情形称为反思优势。GNT 比弱模型或目标模型自己的失败更有价值，并不是因为其答案正确，而是因为它通常保留更长的有效推理前缀，同时提供了具体、可诊断的错误点；逐渐撤去这份“错题解析材料”，则有望迫使模型把纠错经验内化为独立解题能力。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ReflectRL 的输入是训练问题 $q$、标准答案 $a$，以及强专家模型预先生成但最终答案错误的“黄金负轨迹” $o^{-}$。它不把 $o^{-}$ 当作应模仿的正确示范，而是将其放入反思提示中，让策略识别错误、修复推理；训练初期较多使用这种反思接口，随后按余弦日程逐步切换到只给原问题的直接接口，使纠错行为进入模型参数，而不是形成对外部错误轨迹的依赖。框架不增加辅助损失、不修改结果奖励，也不改变推理时接口，可嵌入基于可验证奖励的强化学习与在策略蒸馏。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造黄金负轨迹与双推理接口

直接接口构造 $x^{D}(q)=\text{Chat\_Temp}_{D}(q)$，只提供原问题；反思接口构造 $x^{R}(q,o^{-})=\text{Chat\_Temp}_{R}(q,o^{-})$，要求模型定位 $o^{-}$ 中的错误并推导修正答案。$o^{-}$ 离线生成，训练过程中不再调用专家。

<div class="method-step__io" markdown="1">

**输入**：数据集中的问题—答案对 $(q,a)$，以及专家针对 $q$ 预先生成的错误轨迹 $o^{-}$。<br>
**输出**：同一问题对应的直接上下文 $x^{D}$ 与反思上下文 $x^{R}$。

</div>

**直观理解**：直接接口相当于让学生从空白开始答题；反思接口则给出一份有错误的草稿，让学生先批改再作答。错误草稿提供了可能的思路与关键岔路，因此可能比完全从头搜索更容易。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按日程混合反思与直接训练状态

利用转移核 $g(t)$ 决定反思样本比例；强化学习中取 $K_t=\operatorname{round}(Ng(t))$ 条反思 rollout，其余 $N-K_t$ 条采用直接接口，蒸馏中则在批内取 $K_t^{\mathrm{batch}}=\operatorname{round}(Bg(t))$ 个反思教师上下文。默认余弦衰减使反思比例从 $p_h$ 平滑降至 $p_l$，强化学习终点经取整后为零条反思轨迹。

<div class="method-step__io" markdown="1">

**输入**：训练步 $t$、每题采样数 $N$ 或蒸馏批大小 $B$，以及双接口上下文。<br>
**输出**：随训练推进由“主要借助错误轨迹”逐渐变为“直接独立解题”的训练状态分布。

</div>

**直观理解**：这类似先允许学生参考并批改错题，之后逐渐撤去错题材料，检查其是否已经把纠错方法内化。平滑撤去比突然切换更能减少训练状态与实际推理状态之间的落差。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在 RLVR 中进行混合组联合优化

使用 $\mathrm{MathVerify}(a,o^{(i)})$ 给每条输出计算二元正确性奖励，并在包含两种接口的整个组内标准化奖励得到相对优势 $\hat A_i$；随后以 PPO/GRPO 的裁剪策略比目标共同更新参数 $\theta$。由于二元奖励在非退化组中仍使正确输出具有正优势、错误输出具有负优势，接口类型本身不会固定获得奖励偏置。

<div class="method-step__io" markdown="1">

**输入**：同一问题下由旧策略 $\pi_{\theta_{\mathrm{old}}}$ 生成的 $N$ 条直接或反思 rollout，以及标准答案 $a$。<br>
**输出**：既能从 $o^{-}$ 的错误结构中学习，又逐步提升直接解题能力的策略 $\pi_\theta$。

</div>

**直观理解**：直接作答和批改错题的答案被放在同一组比较，真正答对的轨迹得到鼓励，答错的轨迹受到抑制。模型因此学习的是“如何修正并得到正确结果”，而不是简单复制专家的失败文本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在 OPD 中蒸馏反思教师的分布

学生始终基于直接上下文 $x^{D}(q^{(b)})$ 生成并计算预测分布；教师则按 $g(t)$ 在反思上下文 $x^{R}(q^{(b)},o^{-(b)})$ 与直接上下文之间切换。训练最小化学生分布到教师分布的反向 KL 散度，使学生在自身访问到的前缀状态上逼近经过反思增强的教师。

<div class="method-step__io" markdown="1">

**输入**：批内问题 $q^{(b)}$、学生直接生成的轨迹 $o^{(b)}$、固定教师策略 $\pi_{\mathrm{teacher}}$ 与对应的 $o^{-(b)}$。<br>
**输出**：训练和推理均不读取黄金负轨迹、但吸收了教师纠错倾向的直接推理学生模型。

</div>

**直观理解**：错误轨迹只作为教师的“隐形参考资料”，学生从未看到它；学生只能通过模仿教师对下一词的判断，间接学会避开错误。这样不会把额外上下文变成学生推理时的必需输入。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 反思到直接的余弦转移核

$$
g(t)=p_{l}+\frac{p_{h}-p_{l}}{2}\left[1+\cos\!\left(\pi\tau(t)\right)\right],\qquad K_t=\operatorname{round}(Ng(t))
$$

**符号说明**

- $g(t)$：训练步 $t$ 时反思推理 rollout 的目标比例。
- $t$：当前训练步。
- $p_h$：转移开始时的反思样本比例。
- $p_l$：转移结束时的反思样本比例。
- $\tau(t)$：预热后归一化到 $[0,1]$ 的转移进度。
- $N$：RLVR 中每个问题采样的 rollout 总数。
- $K_t$：训练步 $t$ 中实际采用反思接口的 rollout 数。

<div class="equation-explanation" markdown="1">

**直观理解**：当 $\tau(t)$ 从 $0$ 增至 $1$ 时，余弦项使反思比例平滑地从 $p_h$ 降到 $p_l$。它是方法实现“先借助错误轨迹学习、再回到直接解题”的核心控制器；论文在 RLVR 设置中让末端数量经取整后变为零。<br>
**原文位置**：第 3.2 节，公式（7）；$K_t$ 定义紧随公式（7）

</div>

</div>

<div class="equation-block" markdown="1">

#### RLVR 与 OPD 的 ReflectRL 优化目标

$$
\begin{aligned}\mathcal{J}_{\mathrm{ReflectRL}}(\theta)=\mathbb{E}\Bigg[&\frac{1}{N}\sum_{i=1}^{K_t}\sum_{s=1}^{|o^{(i)}|}\min\!\left(w_{i,s}(\theta)\hat A_i,\operatorname{clip}(w_{i,s}(\theta))\hat A_i\right)\\+&\frac{1}{N}\sum_{i=K_t+1}^{N}\sum_{s=1}^{|o^{(i)}|}\min\!\left(w_{i,s}(\theta)\hat A_i,\operatorname{clip}(w_{i,s}(\theta))\hat A_i\right)\Bigg],\\\mathcal{L}_{\mathrm{OPD}}^{\mathrm{ReflectRL}}(\theta)=\mathbb{E}\!\left[\frac{1}{B}\sum_{b=1}^{B}\sum_{s=1}^{|o^{(b)}|}\mathbb{D}_{\mathrm{KL}}\!\left(p_{b,s}^{\mathrm{student}}\parallel p_{b,s}^{\mathrm{teacher}}\right)\right].\end{aligned}
$$

**符号说明**

- $\theta$：待训练策略或学生模型的参数。
- $N$：RLVR 中同一问题的 rollout 数。
- $K_t$：混合组内采用反思接口的 rollout 数；索引不超过 $K_t$ 的项为反思 rollout，其余为直接 rollout。
- $o^{(i)}$：RLVR 混合组中的第 $i$ 条生成轨迹。
- $s$：生成轨迹中的 token 位置。
- $w_{i,s}(\theta)$：新策略与冻结 rollout 旧策略在第 $i$ 条轨迹、第 $s$ 个 token 上的概率比。
- $\hat A_i$：根据整个直接—反思混合组的奖励均值与标准差计算的组相对优势。
- $\operatorname{clip}(\cdot)$：PPO 式概率比裁剪操作，用于限制单次策略更新幅度。
- $B$：OPD 的批大小。
- $p_{b,s}^{\mathrm{student}}$：学生在直接上下文及自身轨迹前缀下的下一 token 概率分布。
- $p_{b,s}^{\mathrm{teacher}}$：教师在按日程选定的直接或反思上下文及同一轨迹前缀下的下一 token 概率分布。
- $\mathbb{D}_{\mathrm{KL}}$：从学生预测分布到教师预测分布的反向 Kullback–Leibler 散度。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分把反思与直接 rollout 放进同一 GRPO/PPO 目标：正确性决定优势方向，裁剪概率比控制更新稳定性，而不是为反思接口另设奖励。第二部分让始终直接作答的学生匹配教师分布；教师可暂时查看 $o^{-}$，因此纠错知识通过概率分布传给学生，但黄金负轨迹不会进入学生输入。<br>
**原文位置**：第 3.3 节公式（9）及第 3.4 节公式（11）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：RLVR 路径最大化混合组的裁剪策略目标。每条输出先由 $r(q,o^{(i)})=\mathrm{MathVerify}(a,o^{(i)})$ 判定正确性，再在同一问题的全部直接与反思 rollout 上计算组相对优势 $\hat A_i$；因此优化信号奖励最终正确的修复或直接推理，而不会把专家失败轨迹本身视作正标签。OPD 路径则最小化 $\mathcal{L}_{\mathrm{OPD}}^{\mathrm{ReflectRL}}$：学生始终处于直接输入状态，教师在部分样本上借助 $o^{-}$ 形成更有纠错信息的目标分布。两条路径都保持原始 RLVR/OPD 目标形式，ReflectRL 的作用集中在训练上下文及其随时间的分配。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 直接—反思双接口**

两个提示模板共享同一待训练策略：$\text{Chat\_Temp}_{D}$ 仅编码问题，$\text{Chat\_Temp}_{R}$ 同时编码问题与黄金负轨迹，并明确要求发现错误、修复过程和导出正确解。论文用反思增益 $\Delta_{\mathrm{ref}}$ 表示两种接口下期望正确率之差；当 $\Delta_{\mathrm{ref}}>0$ 时，称存在反思优势。

> 直观理解：该模块改变的是模型看到的上下文，而不是网络结构。其关键假设是：困难问题上，检查一条结构化但有缺陷的解法，可能比无提示地搜索完整正确解更容易。

**2. 反思到直接的策略转移**

转移核 $g(t)$ 控制特权上下文的暴露比例，并从 $p_h$ 平滑降至 $p_l$；RLVR 按组内 rollout 分配接口，OPD 按批内教师上下文分配接口。RLVR 的终端分配取整为零条反思 rollout，从而让训练末期状态与只使用 $x^D(q)$ 的部署状态一致。

> 直观理解：如果始终提供 $o^{-}$，模型可能只会“有错稿时纠错”，实际部署时便发生暴露偏差。逐步撤去错稿迫使模型把纠错模式压缩进参数，并练习在真实输入条件下独立调用这些能力。

**3. 保持原目标的插件式适配**

在 RLVR 中，ReflectRL 保留原有可验证奖励、组相对优势与 PPO 裁剪目标，只改变组内 rollout 的提示上下文；在 OPD 中，它保留逐 token 的反向 KL 目标，只给教师提供按日程变化的特权上下文。两种实现都不引入辅助损失，且不增加在线专家查询、rollout 数或验证器调用数。

> 直观理解：ReflectRL 主要重新安排“训练样本如何呈现”，而不是设计新的评分规则。因而它可以接到既有 GRPO、DAPO 或 OPD 流程中，新增成本主要是训练早期读取错误轨迹的上下文预填充。

**训练与推理**

训练前，从专家模型获得与训练问题对应、最终验证失败的 $o^{-}$，并离线保存。RLVR 训练时，对每个问题生成 $N$ 条 rollout，按 $K_t$ 分配反思或直接提示，统一验证答案、计算混合组优势并更新同一策略；随着 $g(t)$ 下降，组内反思 rollout 逐渐减少，最终只在直接接口上训练。OPD 训练时，学生始终从 $x^{D}(q)$ 生成轨迹；教师对批内 $K_t^{\mathrm{batch}}$ 个样本读取 $x^{R}(q,o^{-})$，其余读取 $x^{D}(q)$，学生在自身生成的前缀上匹配教师分布。部署时无论采用哪种训练路径，都只向模型提供原问题对应的 $x^{D}(q)$，不生成、不检索也不输入黄金负轨迹。

**复现信息**

论文基于 verl 实现，训练数据使用 OpenR1-Math-220k 的一个子集；全局训练批大小为 $128$，提示与回答最大长度均为 $2048$ token。RLVR 每题采样 $N=8$ 条回答，训练温度为 $1.0$、验证温度为 $0.6$；采用 GRPO 优势估计器，actor 学习率为 $1\times10^{-6}$，熵系数为 $0.001$，KL 惩罚系数设为 $0$，以免限制反思到直接的策略迁移。复现或比较开销时应注意：ReflectRL 不增加 rollout 与验证器预算，也不进行在线专家查询；相对基线的主要新增成本仅是反思阶段对 $o^{-}$ token 的预填充，且随 $g(t)$ 衰减。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- OpenR1-GNT-69k 是训练集：作者从 OpenR1-Math-220k 的子集中取题，题目提示来自 NuminaMath 1.5，候选轨迹由 DeepSeek-R1 生成，再用 Math-Verify 保留被判定为错误的轨迹，最终得到约 6.9 万条黄金负轨迹。它用于检验模型能否把强专家的失败过程当作待诊断材料，而不是当作正确示范模仿；原文未明确报告训练/验证划分。
- 分布内数学评测组包含 AIME 2024、AIME 2025、AMC、MATH-500、Minerva 和 OlympiadBench，共六个基准。前三个小测试集报告 $\mathrm{avg@32}$，其余报告 $\mathrm{pass@1}$；该组主要测试在数学负轨迹上训练后，模型对同领域推理任务的学习效果。
- 分布外评测组包含 ARC-c、GPQA-Diamond 和 MMLU-Pro，共三个基准，用于测试数学训练所得能力能否迁移到科学问答、研究生级知识推理和多任务知识推理。作者特别指出 OpenR1-GNT-69k 与 ARC-c 没有数据重叠，因此 ARC-c 增益可作为迁移证据，但这并不能单独证明对所有领域都具有普适泛化能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**avg@32**

对 AIME 2024、AIME 2025 和 AMC 等较小测试集进行多次随机生成后汇总的平均正确率；它降低单次采样波动，但不是“32 次中至少一次答对”的 $\mathrm{pass@32}$。 （越高越好，因为表示在重复采样条件下平均答对更多题。）

</div>
<div class="metric-item" markdown="1">

**pass@1**

对其余基准采用单次生成的正确率，直接衡量一次作答成功的能力。 （越高越好，因为表示模型不依赖多次尝试即可正确作答。）

</div>
<div class="metric-item" markdown="1">

**训练效率与稳定性指标**

包括每步更新时间、成功推理的输出长度、策略熵和相对参考策略的 KL 散度。更新时间与输出长度衡量计算代价和推理简洁性；策略熵反映响应分布是否过早收缩；KL 散度衡量策略漂移程度。 （更新时间和在保持正确率前提下的输出长度通常越低越好；KL 过大可能意味着不稳定漂移；策略熵并非简单越高越好，但训练中过快接近零通常表示探索坍缩。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen2.5-1.5B-Instruct：比较原始模型、GRPO 与 GRPO+ReflectRL 在六个分布内及三个分布外基准上的准确率。

<div class="result-value" markdown="1">

加入 ReflectRL 后，分布内平均分由 GRPO 的 20.47 提高到 21.78，分布外平均分由 6.66 提高到 14.76；其中 ARC-c 从 0.34 大幅提高到 18.60。相较原始模型，ReflectRL 的两个平均分也分别由 18.13、5.15 提高到 21.78、14.76。

</div>

这说明即使在 1.5B 小模型上，黄金负轨迹反思也能补充分组策略优化，最突出的收益来自分布外 ARC-c，而不只是数学测试。由于分布外平均值被 ARC-c 的大幅提升显著影响，不能据此声称三个分布外任务均同等改善；例如 GPQA 只从 GRPO 的 1.01 提高到 2.53。

<div class="result-source" markdown="1">

来源：Table 2，Section 7 Detailed Evaluation Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen2.5-1.5B-Instruct | +ReflectRL | 4.37 | 1.04 | 26.88 | 58.00 | 18.75 | 21.63 | 21.78 | 18.60 | 2.53 | 23.15 | 14.76

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen2.5-3B-Instruct：比较 GRPO 与 GRPO+ReflectRL 的整体表现。

<div class="result-value" markdown="1">

ReflectRL 将分布内平均分从 27.15 提高到 28.84，将分布外平均分从 14.43 提高到 20.86；ARC-c 从 1.71 提高到 19.37，MMLU-Pro 从 40.58提高到 42.20，但 AIME 2025 从 3.44 降至 2.08，GPQA 保持 1.01。

</div>

该结果支持“平均性能提高且可跨模型规模复现”，但也明确显示增益并非逐基准一致：ReflectRL 在部分任务上持平或退步。因此，更准确的结论是其总体均值和若干关键任务显著改善，而不是每项测试都占优。

<div class="result-source" markdown="1">

来源：Table 2，Section 7 Detailed Evaluation Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen2.5-3B-Instruct | +ReflectRL | 8.65 | 2.08 | 37.50 | 67.80 | 27.21 | 29.78 | 28.84 | 19.37 | 1.01 | 42.20 | 20.86

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 训练行为与计算效率：在 Reflective-to-Direct Policy Transition 过程中比较 ReflectRL 和 GRPO 的更新时间、生成长度与策略熵。

<div class="result-value" markdown="1">

作者报告 ReflectRL 最终约需 13 秒/步，而 GRPO 约需 20 秒/步；到第 500 步，GRPO 响应超过 800 tokens，ReflectRL 约为 420 tokens。到第 250 步，GRPO 的策略熵从 0.97 降至 0.03 以下，而 ReflectRL 仍约为 0.15。

</div>

这些训练曲线表明，ReflectRL 虽在早期加入负轨迹上下文，却因后续生成更短而降低昂贵的自回归解码成本；较高的剩余熵也与持续学习而非过早模式收缩相符。不过，这些是曲线相关性和单一硬件配置下的壁钟结果，不能单独证明熵保持是性能提升的唯一原因，也不能直接外推到其他推理引擎或 GPU。

<div class="result-source" markdown="1">

来源：Figure 3(a)，Section 4.3 RQ2: Computational Efficiency；相关长度见 Figure 3(b)，熵见 Figure 3(c)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Figure 3(a) shows that the update time of ReflectRL decreases throughout the Reflective-to-Direct Policy Transition, eventually stabilizing at approximately 13 seconds per step, compared with around 20 seconds for GRPO.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 逐项结果显示收益高度不均衡：Qwen2.5-3B 的 AIME 2025 低于 GRPO，GPQA 持平；LLaMA-3.1-8B 的分布外平均提升也较小。论文节选未报告随机种子、方差、置信区间或显著性检验，因此小幅差异是否稳健尚不能确认。
- 训练负轨迹均来自 DeepSeek-R1 在数学题上的失败，并由 Math-Verify 筛选；实验虽覆盖三个分布外基准，但最显著迁移集中于 ARC-c。现有证据尚不足以确定该方法对开放式生成、非可验证任务、其他专家模型或更大规模学生模型是否同样有效。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原始模型与 GRPO：原始模型给出未经在线强化学习的起点；GRPO 是主要在线策略优化基线，可直接检验 ReflectRL 的提升究竟来自负轨迹反思机制，还是一般在线训练本身。
- DAPO：另一种代表性的在线策略训练方法。将 ReflectRL 接入 DAPO，用于测试该框架是否依赖 GRPO 的特定优化形式。
- EchoRL：该方法从已验证成功的在线采样组中抽取按熵筛选的片段作为辅助监督。它是有意义的比较对象，因为 EchoRL 与 ReflectRL 都试图恢复额外学习信号，但前者利用成功轨迹片段，后者利用强专家的失败轨迹。
- OPD：在线策略蒸馏基线，实验中以 Qwen2.5-3B-Instruct 为学生、Qwen2.5-7B-Instruct 为专家。该比较用于判断 ReflectRL 是否也能补充在线蒸馏，而不只适用于基于结果奖励的强化学习。

**实验想回答的问题**

- RQ1：将 ReflectRL 接入不同的在线策略后训练方法、模型规模与架构后，能否稳定提高分布内数学推理和分布外迁移性能，并改善推理长度与策略熵等训练行为？
- RQ2–RQ3：ReflectRL 是否以较低计算与存储开销取得增益，以及这些增益是否确实来自高质量且题目对齐的黄金负轨迹和渐进式“反思到直接推理”策略迁移，而非任意附加上下文？

**实验实现**

实验覆盖 Qwen2.5 与 LLaMA-3.1 系列的四种、参数规模约 1.5B–8B 的模型，并把 ReflectRL 接入 GRPO、DAPO、EchoRL 和 OPD。实现基于 verl，常规设置使用 128 的 rollout batch、64 的 update batch，每道在线训练题采样 8 个回答；评测温度为 0.6，并打乱选择题选项以降低污染风险。OPD 使用反向 KL，rollout batch 为 1024。全部实验运行于 16 张 H200 GPU；黄金负轨迹离线生成，因此在线 rollout 数量与验证器预算不变。原文节选未给出各基准具体样本数、随机种子、置信区间或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 反思来源消融：比较题目对齐的强专家黄金负轨迹、自生成失败、弱模型失败、长度匹配但题目不匹配的负轨迹，以及对轨迹前缀、错误区域、乱序轨迹和仅最终答案等组成部分的处理。 | 黄金负轨迹带来持续增大的 Reflection Gain；自生成失败的帮助有限，弱模型失败和不匹配负轨迹产生负增益。有效前缀提供推理脚手架，局部错误提供明确修正目标，二者结合最好；打乱轨迹或只保留最终答案则低于直接推理。 | 该消融排除了“只要增加一段错误文本就会有帮助”的解释。真正有效的信号需要同时具备较高推理质量、与当前题目对齐且结构连贯：模型应先理解一条大体合理但局部出错的路径，再定位并修复错误。节选没有给出这些条件的精确数值，因此只能报告方向性结论。 | Figure 1(a)、Figure 1(c)，Section 4.4 Source of Reflection<br><span class="experiment-evidence">GNTs produce a large and steadily increasing Reflection Gain, whereas self-generated failures provide only limited benefits, and weak-model failures or length-matched mismatched GNTs yield negative gains.</span> |
| 策略迁移机制消融：比较余弦、逆 Sigmoid 等平滑迁移核与突变或过快迁移日程，并比较正确专家轨迹 GT 指导和黄金负轨迹 GNT 指导的训练稳定性。 | 平滑迁移日程整体更强且更稳定，余弦核最终准确率最高，逆 Sigmoid 趋势相近；过快移除反思指导会削弱性能。GT 指导虽早期改善，却在训练步骤 70–130 附近伴随严重策略漂移并最终崩溃，而 GNT 指导保持稳定。 | 该实验分别隔离了“如何退出反思模式”和“用正确还是错误专家轨迹指导”两个因素。结果支持渐进迁移的重要性，也说明可直接模仿的正确答案不一定是更稳定的在线指导；负轨迹迫使策略执行诊断与修复，可能减少剧烈策略漂移。但节选未提供最终准确率或 KL 的精确数值，因而无法量化不同核之间的差距或崩溃幅度。 | Figure 5、Figure 6，Section 4.4 Mechanistic Validity<br><span class="experiment-evidence">The cosine kernel achieves the best final accuracy, while the inverse-sigmoid variant follows a similar trend, suggesting that the exact functional form is less important than maintaining a gradual shift from Reflective Reasoning to Direct Reasoning.</span> |

**定性案例**

- Figure 10 标为“Reflective Reasoning (Success)”，Figure 11 标为“Direct Reasoning (Fail)”，意在展示同一类困难问题上，检查并修复既有错误轨迹可能比从零直接求解更容易。不过所给节选没有包含题目、推理文本、错误位置或最终答案，无法独立判断成功是否真正来自错误诊断，也不能把单个案例视为总体因果证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出利用失败专家轨迹进行反思并迁移至直接推理的 LLM 在线策略后训练方法。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`cabdddd5c6622b05652b8c22d8922f9fcd9f2a7306e069f8134f98d4ab743277`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
