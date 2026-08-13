---
title: "[论文解读] Towards Understanding On-Policy Distillation through the Lens of Test-Time Scaling"
description: "[arXiv 2608.11829][对齐 / RLHF] 本文质疑“在策略蒸馏能把强教师的新推理能力传给学生”这一通行解释，并通过随采样预算 $K$ 增长而比较 $\\mathrm{pass}@K$ 与 $\\mathrm{avg}@K$，将其收益重新解释为主要提高正确推理路径的采样效率，而非稳定扩大学生模型的能力边界。"
arxiv_id: "2608.11829"
announcement_date: "2026-08-13"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:51:58.794522+00:00"
source_sha256: "ffaac842938228e27185ea6b472a17d0cacd39c675625af38a26388a82c5ceec"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "在线策略蒸馏"
  - "大语言模型推理"
  - "测试时扩展"
  - "反向 KL 散度"
  - "采样效率"
  - "能力边界"
  - "pass@K"
  - "avg@K"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.11829</p>

# Towards Understanding On-Policy Distillation through the Lens of Test-Time Scaling

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Xinmu Ge, Zizhuo Zhang, Yu Huang, Jianing Zhu, Lin Yuan, Wanli Gu, Weichang Wu, Weiran Huang, Xiaolu Zhang, Bo Han, Jun Zhou, Jiangchao Yao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Hong Kong Baptist University University of Texas at Austin；Affiliation: Hong Kong Baptist University；University of Texas at Austin；Shanghai Jiao Tong University；Shanghai Innovation Institute</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11829v1) · [PDF 下载](https://arxiv.org/pdf/2608.11829v1) · **关键词** 在线策略蒸馏, 大语言模型推理, 测试时扩展, 反向 KL 散度, 采样效率, 能力边界, pass@K, avg@K<br>


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

本文质疑“在策略蒸馏能把强教师的新推理能力传给学生”这一通行解释，并通过随采样预算 $K$ 增长而比较 $\mathrm{pass}@K$ 与 $\mathrm{avg}@K$，将其收益重新解释为主要提高正确推理路径的采样效率，而非稳定扩大学生模型的能力边界。

**不用术语来说**：一个模型经过在策略蒸馏后，少量尝试时往往更容易答对，但这不一定意味着它真正学会了以前不会解决的问题：训练也可能只是让模型更频繁地选择原本就会的解法，同时降低某些罕见解法出现的概率。论文要区分这两种情况，因为只观察一次或少量采样的准确率，会把“更容易抽到正确答案”误判为“获得了新的推理能力”。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出以测试时扩展为诊断视角：逐步增加采样预算 $K$，联合考察 $\mathrm{pass}@K$ 与 $\mathrm{avg}@K$，分别判断模型在多次尝试下能否找到至少一个正确答案，以及其单次采样的平均成功水平，从而区分采样效率提升与能力边界扩张。
- 作者将多种在策略蒸馏设置、问题级可解性变化和轨迹分布联系起来，提出“虚幻蒸馏”解释；作者声称，在策略蒸馏主要把概率质量移向更容易访问的正确轨迹，却可能丢失基础模型中低概率但有效的能力，而离策略蒸馏表现出不同的能力扩张趋势。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型推理后训练与测试时扩展的交叉领域。其研究对象是在线策略蒸馏（on-policy distillation，OPD）：学生模型先根据当前策略生成推理轨迹，教师模型再对学生实际访问到的每个前缀状态提供下一词元概率分布，训练则使学生分布接近教师分布。传统解释认为这种教师指导能够把新的推理能力传给学生，但仅比较单次或小预算采样的准确率，无法区分两种效果：一是提高已有正确推理路径被采到的概率，即改善采样效率；二是使学生能够解决训练前在其采样空间中几乎不可达的问题，即扩展能力边界。本文因此改变测试时采样预算 $K$，联合考察 $\mathrm{pass}@K$ 与 $\mathrm{avg}@K$，把高频地产生正确答案和在大量尝试中至少能找到一次正确答案视为两个不同维度。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**在线策略蒸馏（OPD）**

学生模型从自身当前分布采样完整推理轨迹，教师模型在这些学生访问到的状态上提供逐词元的密集监督，学生据此更新参数。它与离线策略蒸馏的关键区别是轨迹来源：前者使用当前学生生成的轨迹，后者通常使用教师生成的轨迹。

</div>
<div class="concept-item" markdown="1">

**反向 KL 散度**

本文以学生分布为第一项、教师分布为第二项计算 $D_{\mathrm{KL}}(\pi_\theta\|\pi_T)$，并最小化该差异。直观上，这会推动学生把概率集中到教师认为更可能的词元上，但分布集中也可能降低对罕见推理路径的覆盖。

</div>
<div class="concept-item" markdown="1">

**测试时扩展**

测试时扩展是在不继续训练模型的情况下增加推理计算，例如对同一道题独立采样 $K$ 条回答。小 $K$ 主要检验有限预算下找到正确路径的效率，而大 $K$ 能更广泛地探索模型分布，因此可作为观测能力边界的经验性诊断工具。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定问题分布 $\mathcal{D}$、学生模型 $\pi_\theta$ 和更强的教师模型 $\pi_T$，学生对问题 $x$ 自回归采样长度为 $L$ 的推理轨迹 $y=(y_1,\ldots,y_L)$；在第 $t$ 步，教师针对学生已经生成的前缀 $(x,y_{<t})$ 给出下一词元分布，训练通过缩小学生与教师在这些状态上的分布差异来更新参数 $\theta$。评估时，对同一道题独立生成 $K$ 个回答：$\mathrm{pass}@K$ 判断其中是否至少有一个正确回答，用于描述预算相关的可达性；$\mathrm{avg}@K$ 统计这些回答的平均正确率，用于描述采样分布的整体质量。论文的核心背景问题不是简单判断 OPD 后准确率是否上升，而是判断上升究竟来自正确轨迹概率增大，还是来自可解问题集合真正扩大。这里把大 $K$ 下仍能否采到正确答案作为能力边界的经验指标，并不等同于对模型理论能力的完备证明。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\pi_\theta$**

参数为 $\theta$ 的学生语言模型及其条件词元分布

</div>
<div class="notation-item" markdown="1">

**$\pi_T$**

教师语言模型及其条件词元分布

</div>
<div class="notation-item" markdown="1">

**$y=(y_1,\ldots,y_L)$**

学生为问题生成的推理轨迹，其中 $y_t$ 是第 $t$ 个词元，$L$ 是轨迹长度

</div>
<div class="notation-item" markdown="1">

**$K$**

测试时对每个问题独立生成回答的采样预算

</div>

</div>

**直接相关的工作**

- **GKD**: 与本文研究对象直接相关的 OPD 方法：它在学生生成的输出上查询教师反馈，以减轻自回归蒸馏中训练分布与测试分布不一致的问题。本文不提出 GKD 的替代训练目标，而是利用不同采样预算下的行为分析这类在线策略蒸馏是否真正扩展学生能力。
- **MiniLLM**: 同样使用学生生成的轨迹开展蒸馏，并强调反向 KL 优化，是本文标准 OPD设定的重要方法基础。本文进一步区分小 $K$ 下的采样效率与大 $K$ 下的经验能力边界，从而检验其性能提升应被解释为能力迁移还是已有推理分布的重加权。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在策略蒸馏已被用于提升大语言模型推理表现，其训练方式是让学生模型生成在策略轨迹，再由更强教师的逐词概率分布提供指导。实际评估若只采用较小采样预算，蒸馏后模型的较高成功率很容易被解释为教师向学生传递了新知识；但模型部署时的采样预算可能变化，因此必须判断收益究竟来自真正新增的可解问题，还是来自对既有正确路径的重新加权。这一区分直接影响蒸馏方法的能力宣称、评估方式以及训练收益在大预算推理场景中的可靠性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **传统离策略知识蒸馏**：教师先生成训练数据或推理轨迹，学生在这些教师产生的离策略样本上学习。由于训练数据可以直接包含学生原先难以生成的解题路径，这类方法在机制上具有把学生现有生成分布之外的知识或轨迹引入训练的可能。
- **在策略蒸馏及其改进变体**：学生先从自身当前策略生成推理轨迹，教师再以逐词分布监督这些学生轨迹，使学生的输出分布靠近教师。已有扩展主要改善训练稳定性、最终表现或适用范围，但其训练起点仍受学生当前能够采样到的轨迹约束。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有工作通常依据有限采样预算下的最终成绩判断蒸馏效果，因而没有充分分离“每次采样更容易成功”和“多次尝试后可达到的解题集合更大”。其后果是，小 $K$ 下的性能增益可能被过度解读为能力边界扩张。
- 已有实证结论并不一致：部分研究与实践显示在策略蒸馏有效，另一些研究则发现蒸馏模型不能稳定超过、甚至可能落后于蒸馏前基础模型。仅比较单一预算或汇总准确率，无法解释这种反转，也无法识别训练是否以提高常见正确轨迹的概率为代价，压低了罕见但有效的推理轨迹。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种围绕采样预算展开的系统诊断，用来判断在策略蒸馏是否把原本不可达的正确解纳入学生的可达范围。具体而言，尚未充分检验小 $K$ 优势能否延续到大 $K$，也未从问题级别统计哪些题由不可解变为可解、哪些题反而失去可解性，更缺少将这些变化与推理轨迹概率重分配联系起来的统一解释。

</div>
<div markdown="1"><span>核心问题</span>

在策略蒸馏究竟会把强教师的新推理能力传递给学生、扩大其在大采样预算下的能力边界，还是主要重塑学生已有的推理分布，使原本存在的正确路径在小采样预算下更容易被抽到？

</div>
<div markdown="1"><span>作者直觉</span>

若训练真正增加了模型能够生成的正确解法，那么随着 $K$ 增大，蒸馏后模型在“至少一次答对”的 $\mathrm{pass}@K$ 上应继续保持优势；反之，若训练只是提高少数既有正确路径的概率，它会改善平均采样表现和小 $K$ 成功率，但基础模型经过足够多次采样后仍可能凭借更丰富的低概率轨迹追平或反超。因而，把 $K$ 当作逐渐扩大搜索范围的旋钮，并同时观察 $\mathrm{avg}@K$、$\mathrm{pass}@K$ 和问题级可解性，就能较直接地区分“更会做”与“更容易抽中会做的答案”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文的方法不是提出新的蒸馏算法，而是建立一套以测试时扩展为核心的诊断流程，用来区分 OPD 带来的两类潜在收益：一类是提高正确推理轨迹被采到的概率，即采样效率；另一类是让学生获得训练前无法生成的新解法，即扩展能力边界。训练阶段，学生模型 $\pi_{\theta}$ 对训练问题 $x$ 自行生成推理轨迹 $y$；教师模型 $\pi_T$ 在这些“学生实际访问的状态”上给出下一词元分布，学生通过最小化反向 KL 散度进行更新。分析阶段，对训练前学生、不同 OPD 检查点、最终学生和教师使用相同解码条件，每题独立采样最多 $K=1024$ 条回答，并联合考察 $\mathrm{pass}@K$ 与 $\mathrm{avg}@K$ 随预算变化的曲线。

其中，小 $K$ 下的 $\mathrm{pass}@K$ 和各预算下的 $\mathrm{avg}@K$ 主要反映正确路径是否容易被抽到；大 $K$ 下的 $\mathrm{pass}@K$ 则被作者用作能力边界的近似指标，因为大量采样可以更充分地搜索模型已有的输出空间。在此基础上，论文进一步进行逐题可解性分类、训练动态跟踪、先进 OPD 变体对照、离策略蒸馏对照及困惑度分析，从不同角度判断概率质量究竟是被重新集中到学生原有的成功路径上，还是教师真正向学生引入了原本不可达的推理模式。通俗地说，这套方法既检查“学生一次或少数几次能否更稳定地答对”，也检查“给足一千多次机会后，学生到底会不会做更多种题”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造学生在策略蒸馏训练信号

从当前学生分布 $\pi_{\theta}(\cdot\mid x)$ 采样完整推理轨迹 $y=(y_1,\ldots,y_L)$，并在每个学生访问的前缀状态 $(x,y_{<t})$ 上查询教师的下一词元分布。论文采用 top-$k$ 词元 KL 的实现形式，使分布匹配集中在所选高概率词元上。

<div class="method-step__io" markdown="1">

**输入**：训练集 $\mathcal{D}$ 中的问题 $x$、当前学生模型 $\pi_{\theta}$ 和教师模型 $\pi_T$。<br>
**输出**：由学生自身轨迹及教师稠密分布组成的逐词元蒸馏样本。

</div>

**直观理解**：学生先按自己当前的思路作答，教师再针对学生走到的每一步给出概率层面的纠正，而不是把教师预先写好的整条解答直接交给学生模仿。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 优化 OPD 学生并保存训练检查点

对轨迹各位置的反向 KL 散度求和并对训练样本取期望，通过梯度更新参数 $\theta$；除最终模型外，还保留多个训练步的检查点，以观察小预算与大预算性能如何随训练演化。

<div class="method-step__io" markdown="1">

**输入**：学生访问状态上的学生分布与教师分布，以及反向 KL 蒸馏损失。<br>
**输出**：最终 OPD 学生模型以及 Step 20、80、140、200、260 等中间检查点。

</div>

**直观理解**：该步骤逐渐把学生的出词概率推向教师偏好的方向；保存中间版本则能判断性能变化是在训练早期出现、持续发展，还是只存在于最终模型。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行统一的测试时多次采样

在一致的温度、top-$p$、上下文长度和随机种子设置下，为每个问题生成 $K$ 条相互独立的推理回答，其中 $K$ 从小预算逐步增加到 $1024$。随后判定每条回答是否正确，并计算 $\mathrm{pass}@K$ 与 $\mathrm{avg}@K$。

<div class="method-step__io" markdown="1">

**输入**：训练前学生、OPD 学生、教师或对照蒸馏模型，四个数学基准中的问题，以及采样预算 $K$。<br>
**输出**：各模型在不同预算下的成功可达率曲线和平均采样正确率曲线。

</div>

**直观理解**：$\mathrm{avg}@K$ 关注随机抽一条回答通常有多好，$\mathrm{pass}@K$ 关注多试几次后是否至少能找到一条正确路径；将两者一起看，才能避免把“更稳定”误判成“学会了新能力”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分解逐题能力变化并跟踪训练动态

以是否在 $K$ 次采样中至少出现一次正确回答作为可解性标准，将问题分为 retained、learned 和 forgotten，并计算 learned 比例减去 forgotten 比例的净变化；同时比较各检查点的小 $K$ 与大 $K$ 的 $\mathrm{pass}@K$。

<div class="method-step__io" markdown="1">

**输入**：训练前学生与 OPD 学生在同一问题、同一预算 $K$ 下的多次采样结果，以及各训练检查点的结果。<br>
**输出**：保留、学会和遗忘问题的比例，净可解性变化，以及采样效率与能力边界随训练步数变化的轨迹。

</div>

**直观理解**：该分解直接追问 OPD 是让学生学会了以前不会的题，还是只让原本偶尔会做的题更容易答对；检查点曲线则揭示这种变化在训练过程中何时发生。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 在策略蒸馏的反向 KL 目标

$$
\mathcal{L}_{\mathrm{OPD}}(\theta)=\mathbb{E}_{x\sim\mathcal{D},\,y\sim\pi_{\theta}(\cdot\mid x)}\left[\sum_{t=1}^{L}D_{\mathrm{KL}}\!\left(\pi_{\theta}(\cdot\mid x,y_{<t})\,\middle\|\,\pi_{T}(\cdot\mid x,y_{<t})\right)\right]
$$

**符号说明**

- $\mathcal{L}_{\mathrm{OPD}}(\theta)$：学生参数为 $\theta$ 时的 OPD 训练损失。
- $\theta$：待优化的学生模型参数。
- $\mathcal{D}$：训练问题的分布或数据集。
- $x$：从 $\mathcal{D}$ 采样的输入问题。
- $\pi_{\theta}$：当前学生模型的条件概率分布。
- $\pi_T$：教师模型的条件概率分布。
- $y=(y_1,\ldots,y_L)$：学生针对问题生成的长度为 $L$ 的推理轨迹。
- $y_{<t}$：第 $t$ 个解码位置之前已经生成的词元前缀。
- $D_{\mathrm{KL}}(P\|Q)$：分布 $P$ 相对于分布 $Q$ 的 KL 散度；此处第一项是学生、第二项是教师，因此属于反向 KL 方向。

<div class="equation-explanation" markdown="1">

**直观理解**：先由学生自己生成一条推理轨迹，再沿着这条轨迹逐步比较学生与教师的下一词元概率，并把所有位置的不一致累加。最小化该式会使学生在自己实际到达的状态上更接近教师，但它没有直接要求学生复现教师独立生成的完整推理轨迹，因此教师知识能否越过学生原有探索范围正是论文要检验的问题。<br>
**原文位置**：第 2.1 节，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 测试时扩展的互补指标

$$
\begin{aligned}\mathrm{pass}@K&=\mathbb{E}_{x\sim\mathcal{D},\,\{y^{(i)}\}_{i=1}^{K}\sim\pi_{\theta}(\cdot\mid x)}\!\left[\mathbb{I}\!\left(\exists i\in\{1,\ldots,K\}:y^{(i)}\text{ is correct}\right)\right],\\ \mathrm{avg}@K&=\mathbb{E}_{x\sim\mathcal{D},\,\{y^{(i)}\}_{i=1}^{K}\sim\pi_{\theta}(\cdot\mid x)}\!\left[\frac{1}{K}\sum_{i=1}^{K}\mathbb{I}\!\left(y^{(i)}\text{ is correct}\right)\right].\end{aligned}
$$

**符号说明**

- $K$：每个问题允许生成的独立回答数量，即测试时采样预算。
- $y^{(i)}$：针对同一问题生成的第 $i$ 条推理回答。
- $\{y^{(i)}\}_{i=1}^{K}\sim\pi_{\theta}(\cdot\mid x)$：从学生模型对问题 $x$ 的条件分布中独立采样 $K$ 条回答。
- $\mathbb{I}(\cdot)$：指示函数：条件成立时为 $1$，否则为 $0$。
- $\mathrm{pass}@K$：在 $K$ 条回答中至少出现一条正确回答的期望比例。
- $\mathrm{avg}@K$：$K$ 条回答中正确回答比例的期望，即采样分布的平均正确率。

<div class="equation-explanation" markdown="1">

**直观理解**：$\mathrm{pass}@K$ 只关心多次尝试中是否至少成功一次，因此增大 $K$ 可以逐渐暴露低概率但仍可生成的正确路径；$\mathrm{avg}@K$ 则关心每次采样通常有多可靠。论文据此把“正确路径概率变高”和“可生成的正确路径集合扩大”分开，不过有限的 $K=1024$ 仍只能给出能力边界的经验近似，不能证明概率严格为零。<br>
**原文位置**：第 2.2 节，公式 (2) 与公式 (3)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：标准 OPD 通过最小化 $\mathcal{L}_{\mathrm{OPD}}(\theta)$ 更新学生参数。每轮先用当前学生进行在策略采样，因此训练状态分布会随参数 $\theta$ 改变；随后在学生生成前缀上取得教师分布，并使用 top-$k$ 词元近似计算反向 KL。反向 KL 倾向于让学生概率集中到教师高概率且学生已能访问的模式上，这为论文观察到的“提高已有正确路径的采样概率”提供了机制解释，但该解释属于结合实验的分析，不等同于目标函数本身已经证明 OPD 必然缩小能力边界。

先进变体用于检查结论是否只由标准反向 KL 导致：纯前向 KL 交换分布匹配方向；EOPD 在教师高熵位置加入前向 KL、其余位置保留反向 KL；Direct-OPD 使用教师强化学习前后检查点的对数概率比作为隐式奖励；ExOPD 将 OPD 视为带 KL 正则的稠密强化学习并进行奖励外推。论文对这些方法采用统一的测试时扩展诊断，而不是把训练损失值直接当成能力迁移证据。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 学生访问状态上的反向 KL 蒸馏**

OPD 的轨迹由当前学生 $\pi_{\theta}$ 采样，而教师只在状态 $(x,y_{<t})$ 上提供下一词元目标分布。损失方向为 $D_{\mathrm{KL}}(\pi_{\theta}\|\pi_T)$，论文具体采用 top-$k$ 词元 KL；这与使用教师生成轨迹的离策略蒸馏形成关键区别。

> 直观理解：该模块能持续纠正学生真正会走到的状态，但训练数据仍受学生当前探索范围限制：若学生从未进入某类有效推理路径，教师的逐步概率指导未必足以把该路径带入学生的可达空间。

**2. 双指标测试时扩展诊断**

$\mathrm{pass}@K$ 判断 $K$ 次采样中是否至少一次正确，衡量预算相关的成功路径可达性；$\mathrm{avg}@K$ 对 $K$ 条回答的正确指示量取平均，衡量整个采样分布的平均质量。论文将小 $K$ 表现解释为有限预算下的采样效率，将大 $K$ 的 $\mathrm{pass}@K$ 作为能力边界的经验代理，而非严格的理论边界。

> 直观理解：同一模型可能把少量已有正确解法的概率提高，从而更常答对，却没有增加任何新解法。此时平均正确率和少次尝试表现会上升，但充分采样后能覆盖的问题集合未必扩大。

**3. 逐题可解性与分布归因分析**

逐题分析以 $\mathrm{pass}@K$ 为二元可解性判据：retained 表示 Base 与 OPD 均可解，learned 表示仅 OPD 可解，forgotten 表示仅 Base 可解；困惑度分析再比较 $\mathrm{PPL}_{\mathrm{Base}}(Y)$ 与 $\mathrm{PPL}_{\mathrm{Teacher}}(Y)$，其中 $Y$ 分别来自 Base、OPD 和 Teacher。

> 直观理解：总体分数可能掩盖“学会一些题、同时忘掉另一些题”的交换。逐题分类显示得失来自哪里，困惑度则检查 OPD 是否真的采用教师的新思路，还是主要把基础模型本来就熟悉的正确思路变得更常见。

**训练与推理**

训练时，三个主要设置均使用 DAPO-Math-17k：Qwen3 设置以 Qwen3-1.7B-Base 为学生、Qwen3-4B-Base-GRPO 为教师；Skywork 设置以 R1-Distill-Qwen-1.5B 为学生、Skywork-OR1-Math-7B 为教师；JustRL 设置使用同一学生底座和 JustRL-DeepSeek-1.5B 教师。标准 OPD 从学生当前策略生成轨迹，在每个前缀上读取教师概率并更新学生。为分析训练动态，Skywork 设置保存多个训练步检查点；为检验目标函数依赖性，另行训练 EOPD、ExOPD、Direct-OPD 和纯前向 KL 版本。

推理与分析时，对 AMC2023、AIME2024、AIME2025 和 AIME2026 中的每个问题独立采样，预算覆盖 $K\in\{1,2,\ldots,512,1024\}$，再计算两条预算曲线。作者首先比较 Base、OPD 与 Teacher，判断小预算增益是否延伸至大预算；其次用相同 $K$ 对问题做 retained、learned、forgotten 分类；再次跟踪检查点上的小 $K$ 和大 $K$ 指标；最后对先进 OPD、纯前向 KL 与离策略蒸馏重复比较，并用 Base 和 Teacher 对不同来源轨迹计算困惑度。整个推断链条是：若小 $K$ 的 $\mathrm{pass}@K$ 和 $\mathrm{avg}@K$ 上升，而大 $K$ 的 $\mathrm{pass}@K$ 不升，且 OPD 轨迹仍受 Base 分布高度支持，则更符合概率质量重分配，而非稳定的能力边界扩展。

**复现信息**

公平解释主结果所需的评测条件为：温度 $0.7$、top-$p=0.95$、随机种子 $0$，上下文窗口为 $32768$ 个词元，提示最多 $1024$ 个词元，输出最多 $31744$ 个词元；每题最高生成 $1024$ 条回答。训练 OPD 变体时统一使用温度 $1$、top-$p=1$、禁用 rollout top-$k$、每批一个 PPO epoch、无学习率预热、权重衰减 $0.01$，但各变体仍遵循各自代码库的默认批量、长度与学习率配置。因此，变体比较共享总体诊断框架，却不是所有优化超参数完全相同的严格控制实验。

标准 OPD 的关键配置包括全局批量与 PPO mini-batch 均为 $64$、最大提示与响应长度分别为 $1024$ 和 $7168$、学习率 $1\times10^{-6}$ 并采用余弦调度、学生 top-16 词元 KL。Direct-OPD、EOPD 和纯前向 KL 使用 $128/32$ 的批量配置、$1024/4096$ 的长度配置及 $3\times10^{-6}$ 的余弦学习率，其中 Direct-OPD 使用学生 top-16，EOPD 与纯前向 KL 使用教师 top-16；ExOPD 使用 $1024/1024$ 批量、$2048/16384$ 长度、$1\times10^{-5}$ 恒定学习率和采样词元对数概率。复现时还应注意，大 $K$ 的 $\mathrm{pass}@K$ 是有限采样下的代理指标，结果会受题目数量、采样随机性和解码设置影响。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- DAPO-Math-17k：包含约 1.7 万道数学题的训练集，用于三个学生—教师配置中的 OPD 训练。原文节选未说明具体数据划分、题目来源构成及是否进行去重，因此无法判断其与评测集之间是否存在潜在重合。
- AMC2023：美国数学竞赛的 2023 年快照，作为相对较易的数学推理评测集；论文使用 math-vault 整理的固定快照，并通过 math-eval 完成推理、答案抽取和评分。该数据集用于比较预 OPD 基座、OPD 学生和教师在不同采样预算下的表现。
- AIME2024、AIME2025 与 AIME2026：三个年度的高难度数学竞赛快照，在分析中作为同一类高难推理基准；既分别报告测试时扩展曲线，也与 AMC2023 合并，用于 retained、learned、forgotten 三类问题级可解性统计。原文节选未明确报告各快照的题目数量。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$\mathrm{pass@}K$**

对每道题独立采样 $K$ 个回答，只要至少一个回答正确，就将该题视为可解；总体指标是满足这一条件的题目比例。小 $K$ 更强调有限推理预算下命中正确路径的效率，大 $K$，尤其 $K=1024$，被作者用作模型能力边界的代理。它仍是有限采样下的经验边界，而非对模型所有潜在能力的严格证明。 （越高越好，因为它表示在给定采样预算内至少找到一次正确答案的题目更多。）

</div>
<div class="metric-item" markdown="1">

**$\mathrm{avg@}K$**

统计 $K$ 个采样回答的平均正确率，反映单次随机生成正确答案的概率。若 OPD 的 $\mathrm{avg@}K$ 提高而大预算 $\mathrm{pass@}K$ 不提高，说明正确路径被赋予了更高概率，但可访问的解题集合未必扩大。 （越高越好，因为随机抽取一个生成结果时答对的概率更高，也意味着达到同等可靠性通常需要更少采样。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 小预算下的 OPD 收益，以 Qwen3 配置在 AIME2024 上的完整 $K=1$ 至 $32$ 曲线为例。

<div class="result-value" markdown="1">

在 $K=1$ 时，预 OPD 基座、OPD 学生和教师的 $\mathrm{pass@}1$ 分别为 4.2%、12.0% 和 24.2%；OPD 学生比基座高 7.8 个百分点。随着预算增至 $K=32$，二者变为 28.2% 和 30.5%，差距缩小到 2.3 个百分点。作者据此并结合其余配置与基准，主张 OPD 的优势最大多出现在小采样预算。

</div>

这表明 OPD 把概率质量集中到了更容易被抽中的正确推理路径上，因此单次或少量尝试更有效。它能证明有限预算下的实用性能改善，但不能单独证明学生学会了基座完全无法生成的新解法，因为同一基座增加采样次数后也可能找到这些答案。

<div class="result-source" markdown="1">

来源：附录 C，表 3，Qwen3—AIME24 行；列依次为 $K=1,2,4,8,16,32$，每格依次为 Base / OPD / Teacher（%）。

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

AIME24 4.2/12.0/24.2 7.0/16.7/30.7 10.9/20.9/37.2 16.0/24.2/44.4 22.0/27.3/51.8 28.2/30.5/58.2

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 大预算下的能力边界，以 Qwen3 配置在 AIME2024 上的 $K=64$ 至 $1024$ 曲线为例。

<div class="result-value" markdown="1">

在 $K=64$ 时，基座与 OPD 学生的 $\mathrm{pass@}64$ 分别为 35.0% 和 33.6%；到 $K=1024$ 时分别为 70.0% 和 53.3%，OPD 学生低 16.7 个百分点。作者报告三个 OPD 配置和四个基准在 $K=1024$ 时均不存在 OPD 学生超过其基座的情况，并将其解释为能力边界没有得到一致扩展。

</div>

增加采样次数后，基座能够搜索到更多低概率但正确的推理路径，而 OPD 学生的可访问解题集合没有同步扩大，甚至可能因概率分布收缩而丢失部分路径。该结果支持“未观察到能力扩展”，但 $\mathrm{pass@}1024$ 仍只是有限 1024 次采样和特定解码设置下的代理，不能证明 OPD 学生在理论上绝不可能解出这些题。

<div class="result-source" markdown="1">

来源：附录 C，表 4，Qwen3—AIME24 行；列依次为 $K=64,128,256,512,1024$，每格依次为 Base / OPD / Teacher（%）。

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

AIME24 35.0/33.6/63.1 42.9/37.0/67.1 51.6/41.6/70.4 61.0/47.3/73.7 70.0/53.3/76.7

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨预算的平均采样正确率，以 JustRL 配置在 AIME2024 上的 $\mathrm{avg@}K$ 曲线为例。

<div class="result-value" markdown="1">

在所列预算 $K=32,64,128,256,512,1024$ 下，OPD 学生的 $\mathrm{avg@}K$ 均明显高于基座；例如 $K=1024$ 时为 49.4%，基座为 29.9%，提高 19.5 个百分点。教师对应为 52.1%。这与同一论文中大预算 $\mathrm{pass@}K$ 优势消失的现象共同构成作者“主要改善采样效率”的证据。

</div>

平均正确率持续提高意味着随机生成一次时更容易答对，因而 OPD 对实际有限预算推理很有价值；但该指标主要反映输出分布中正确答案的概率，而不是不同题目上是否出现了全新的可达推理路径。因此，较高的 $\mathrm{avg@}K$ 不能替代大预算 $\mathrm{pass@}K$ 来证明能力集合扩大。

<div class="result-source" markdown="1">

来源：附录 C，表 5，JustRL—AIME24 行；列依次为 $K=32,64,128,256,512,1024$，每格依次为 Base / OPD / Teacher（%）。

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

AIME24 29.1/48.5/52.4 29.4/48.8/52.4 29.8/49.1/51.9 30.1/49.3/52.0 29.7/49.3/52.1 29.9/49.4/52.1

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

- 预 OPD 基座模型：Qwen3 配置使用 Qwen3-1.7B-Base，Skywork 与 JustRL 配置使用 R1-Distill-Qwen-1.5B。它们与对应 OPD 学生共享训练起点，是判断 OPD 是否增加新能力、而非仅重新分配输出概率的核心对照。
- 教师模型：三个配置分别使用 Qwen3-4B-Base-GRPO、Skywork-OR1-Math-7B 和 JustRL-DeepSeek-1.5B。教师强度覆盖“多数预算下明显更强”和“主要在小预算下占优”两种情况，用于检验结论是否只由某一种师生能力差距造成。
- 离策略蒸馏模型 DeepSeek-R1-Distill-Qwen-1.5B/7B：由 Qwen-Math-1.5B/7B 在 DeepSeek-R1 预先生成的数据上微调得到。它用于区分 OPD 特有现象与一般蒸馏现象：如果离策略蒸馏在大采样预算下仍提升 $\mathrm{pass@}K$，则能力边界不扩展不能简单归因于所有蒸馏方法。
- Qwen-Math-1.5B/7B：离策略蒸馏模型各自的基座，用于衡量 DeepSeek-R1 生成数据是否同时提高小预算采样效率和大预算可解范围。该比较与主要 OPD 配置的基座不同，因此适合做范式级对照，但不适合直接比较绝对分数。

**实验想回答的问题**

- 在测试时采样预算从小到大变化时，OPD 相对预训练前学生模型的收益究竟来自能力边界扩展，还是仅来自提高已有正确推理路径的采样概率？
- OPD 训练如何改变问题级可解性与不同采样预算下的性能，并且这种变化是否区别于真正利用教师生成数据的离策略蒸馏？

**实验实现**

三个 OPD 配置均在 DAPO-Math-17k 上训练，并在 AMC2023、AIME2024、AIME2025 和 AIME2026 上比较预 OPD 基座、OPD 学生与教师。测试时采样预算覆盖 $K\in\{1,2,\ldots,512,1024\}$；默认解码温度为 $0.7$，top-$p$ 为 $0.95$，随机种子为 $0$。上下文窗口为 32768 token，其中提示上限为 1024 token、输出上限为 31744 token。提示要求模型逐步推理，并把最终答案放入 $\boxed{\cdot}$；官方评分比较最后一个完整 boxed answer 与标准答案。推理、回放、答案抽取和评分使用 math-vault 快照与 math-eval 流程。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 沿 OPD 训练步数追踪小预算与大预算的 $\mathrm{pass@}K$，而不是只比较最终检查点。 | 作者观察到 $K=1$ 或 $2$ 的 $\mathrm{pass@}K$ 随训练总体改善，而 $K=512$ 或 $1024$ 的指标逐渐下降；大预算退化在约 80 个训练步时已经明显出现。原文节选未提供图 4 的具体纵轴数值。 | 该分析隔离了训练进程的影响：最终模型的大预算劣势不是只在训练结束时偶然出现，而是可能较早形成，并与小预算收益同步发展。这支持采样效率与经验能力边界之间存在权衡，但由于缺少重复训练、误差条和逐点数值，不能确定约 80 步这一时间点是否具有统计稳定性。 | 第 3.3 节，图 4。<br><span class="experiment-evidence">Additionally, large-$K$ pass@$K$ exhibits noticeable fluctuations and already shows a clear decline by around 80 training steps.</span> |
| 用离策略蒸馏替换 OPD 范式，比较 DeepSeek-R1-Distill-Qwen-1.5B/7B 与对应 Qwen-Math-1.5B/7B 基座。 | 作者报告离策略蒸馏模型在四个基准的小、大采样预算下，其 $\mathrm{pass@}K$ 和 $\mathrm{avg@}K$ 均持续高于对应基座。原文节选未给出图 5 的具体数值。 | 这一对照隔离的是蒸馏数据获取方式：离策略方法直接学习教师生成轨迹，而 OPD 使用学生当前策略产生的轨迹。若前者的大预算 $\mathrm{pass@}K$ 也提高，则说明教师知识确实可能扩大学生的经验可解范围，OPD 的结果更可能来自其训练机制，而不是“学生模型无法从教师获得新能力”。不过两组实验使用不同模型与训练设置，因而属于范式级证据，不是严格控制所有变量的单因素消融。 | 第 3.4 节，图 5。<br><span class="experiment-evidence">As illustrated in Figure 5, across both small and large sampling budgets, off-policy distillation-trained models consistently achieve higher pass@$K$ and avg@$K$ than their corresponding base models.</span> |

**定性案例**

- 随机轨迹困惑度分析从四个基准各独立抽取 4 道题，并让 Skywork 的基座、OPD 学生和教师各为每题生成 32 条轨迹，共得到每个来源 512 条、总计 1536 条轨迹。教师作为评分器时，OPD 轨迹比基座轨迹困惑度低；基座作为评分器时，OPD 轨迹又比基座或教师轨迹困惑度低。作者将其解释为：OPD 把学生分布推向教师偏好的路径，但这些路径仍受到原基座分布支持，并非简单复制教师轨迹。该样本规模较小，适合作为机制线索，不能独立支撑总体因果结论。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper analyzes on-policy distillation as reasoning post-training and studies its effects on test-time sampling efficiency and capability boundaries.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`ffaac842938228e27185ea6b472a17d0cacd39c675625af38a26388a82c5ceec`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
