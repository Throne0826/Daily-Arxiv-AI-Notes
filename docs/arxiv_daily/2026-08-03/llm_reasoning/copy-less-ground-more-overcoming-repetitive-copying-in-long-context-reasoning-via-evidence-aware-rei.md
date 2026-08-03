---
title: "[论文解读] Copy Less, Ground More: Overcoming Repetitive Copying in Long-Context Reasoning via Evidence-Aware Reinforcement Learning"
description: "[arXiv 2607.19345][LLM Reasoning] 本文将长上下文推理中的大段重复抄写诊断为证据定位不足，并提出证据感知奖励 GEAR，引导模型关注关键证据、避开无关上下文。"
arxiv_id: "2607.19345"
announcement_date: "2026-08-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-03T02:16:01.474066+00:00"
source_sha256: "558c107710474b2f2e94ff7079cb4ab327399d649ed6b0f6410c1c3fedae48b3"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "长上下文推理"
  - "重复复制"
  - "证据落地"
  - "干扰上下文"
  - "可验证奖励强化学习"
  - "推理轨迹"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2607.19345</p>

# Copy Less, Ground More: Overcoming Repetitive Copying in Long-Context Reasoning via Evidence-Aware Reinforcement Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-03</span>
<span><strong>作者</strong> Lizhe Fang, Weizhou Shen, Tianyi Tang, Yisen Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Peking University；Alibaba Group ATH</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.19345) · [PDF 下载](https://arxiv.org/pdf/2607.19345) · **关键词** 长上下文推理, 重复复制, 证据落地, 干扰上下文, 可验证奖励强化学习, 推理轨迹<br>


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

本文将长上下文推理中的大段重复抄写诊断为证据定位不足，并提出证据感知奖励 GEAR，引导模型关注关键证据、避开无关上下文。

**不用术语来说**：面对很长的输入，推理模型常把原文大段搬进思考过程，却没有有效判断哪些内容真正有助于回答问题；输入越长，这种现象越严重，不仅浪费推理令牌、拉长思考过程，还更容易得到错误答案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者识别并系统分析了“重复抄写”这一长上下文推理失效模式，进一步指出真正有害的并非引用输入本身，而是不区分关键证据与干扰内容的无选择抄写。
- 作者据此提出 GEAR 奖励塑形方案：在答案正确性奖励之外，同时奖励推理轨迹与关键证据的重合、惩罚其与无关上下文的重合，并配套设计从任意长文档自动构造带证据标注问答数据的流程。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于长上下文大语言模型推理与强化学习交叉领域。具备显式思考能力的模型会先生成逐步推理轨迹，再输出最终答案；当输入扩展为包含大量文本的长上下文时，任务重点也由定位某个事实转向综合多处信息完成复杂推理。论文关注这一场景中的“重复复制”现象：模型把输入中的大段文字直接搬入推理轨迹，消耗生成预算，却未必有效推进求解。理解该问题的关键是区分任务相关的关键证据与无关的干扰上下文，并判断模型是否选择性地依据前者进行推理。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**长上下文推理**

模型需要在较长输入中定位、组合并推导与问题有关的信息，而不只是复述或检索单个片段。较长输入通常同时包含有用证据和大量无关内容，因此要求模型具备可靠的信息筛选能力。

</div>
<div class="concept-item" markdown="1">

**证据落地（evidence grounding）**

指模型的推理和答案能够明确依托输入中真正支持结论的证据。本文所说的“落地不足”表现为模型不能稳定区分关键证据与干扰内容，因而从整个提示中无差别复制。

</div>
<div class="concept-item" markdown="1">

**可验证奖励强化学习（RLVR）**

使用可自动核验的结果信号训练模型，例如根据最终答案是否正确给予奖励，而不必为每一步推理提供人工标注。本文背景中的关键局限是：仅奖励答案正确与否，可能无法充分指导长上下文中的证据选择过程。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个长上下文问题，输入由问题、任务相关的关键证据以及无关的干扰上下文构成；具备显式思考能力的语言模型先生成推理轨迹，再给出最终答案。论文考察模型在推理轨迹中从输入复制文本的行为，尤其关注复制是否具有选择性：引用关键证据可能有助于求解，而广泛复制干扰内容则反映证据落地不足。该设置覆盖合成任务与自然语言文档，并假定训练样本能够直接提供或通过自动流程构造关键证据和干扰内容的区分，以便后续奖励机制分别评价两类重叠。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

包含问题、关键证据和干扰上下文的长上下文输入；原文节选未给出统一形式化符号，此处仅作任务描述用。

</div>
<div class="notation-item" markdown="1">

**$y$**

模型针对输入生成的推理轨迹；原文节选未给出统一形式化符号，此处仅作任务描述用。

</div>
<div class="notation-item" markdown="1">

**$E$**

与回答当前问题直接相关的关键证据集合；原文节选未给出统一形式化符号，此处仅作概念整理用。

</div>
<div class="notation-item" markdown="1">

**$D$**

输入中与当前任务无关的干扰上下文集合；原文节选未给出统一形式化符号，此处仅作概念整理用。

</div>

</div>

**直接相关的工作**

- **LongRLVR（Chen et al., 2026）**: 同样研究长上下文强化学习，并指出仅依赖结果奖励会使上下文落地相关的梯度消失，因而加入基于文本块级 $F$ 分数的可验证上下文奖励。与本文最直接的区别是，LongRLVR在较粗的文本块层面评价上下文使用，而本文从重复复制这一具体失效模式出发，要求区分关键证据与干扰上下文，并在更细的 $n$-gram 层面衡量重叠。
- **LoongRL（Wang et al., 2025）**: 该工作通过向短上下文多跳问答加入干扰项来构造长上下文训练数据，与本文都利用“有效信息加干扰内容”的结构训练长上下文能力。本文进一步把这种结构用于诊断复制内容的来源，并将关键证据重叠和干扰内容重叠作为性质相反的训练信号。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长上下文评测正从简单的信息检索转向需要多步推理的复杂任务，但显式生成思考轨迹的模型在处理长输入时，会把大量上下文机械复制到推理轨迹中。这会消耗有限的生成预算，使模型把计算资源用于复述而非求解，并伴随准确率下降；因此，长上下文推理不仅需要“读得到”信息，还需要可靠地判断应依据哪些信息作答。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **长上下文思维链推理**：模型先生成逐步推理轨迹，再给出最终答案，借助显式中间步骤处理跨段信息和复杂推断。该范式在一般复杂任务上有效，因此也被自然用于长上下文场景。
- **基于答案正确性的强化学习**：训练时主要根据最终答案是否正确提供奖励，让模型通过强化学习提高任务得分；这种信号监督最终结果，却不直接约束推理过程中引用了哪些输入内容。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 显式思考并不自动带来有效的证据筛选：模型可能无差别复制关键证据和无关干扰内容，而且上下文越长，重复抄写越严重，最终导致推理轨迹膨胀并挤占真正求解所需的令牌预算。
- 仅依据最终正确性提供奖励，无法明确告诉模型“应关注哪段证据、应忽略哪段干扰”。即使两个推理过程得到相同奖励，它们的证据依据也可能完全不同，因此训练信号不足以直接纠正无选择抄写。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有长上下文训练缺少一种可扩展的过程级监督机制，既能区分有益的证据引用与有害的上下文搬运，又能用于缺少人工证据标注的自然语言文档。未解决的关键是：如何把“选择性依据相关证据”转化为可计算的强化学习奖励，并获得支持该奖励的大规模训练数据。

</div>
<div markdown="1"><span>核心问题</span>

若在答案正确性奖励之外，显式奖励推理轨迹与任务关键证据的重合，并惩罚其与无关上下文的重合，能否使不同规模的长上下文模型减少无选择抄写、缩短无效思考，并提高超出训练长度分布时的推理准确性？

</div>
<div markdown="1"><span>作者直觉</span>

抄写并非一概有害：模型重述真正决定答案的句子，往往说明其注意到了正确依据；问题在于把整份输入都当作同等重要。GEAR 的思路类似给阅读者同时设置“加分项”和“扣分项”——抓住支持答案的段落会得到奖励，搬运无关材料会受到惩罚。这样，模型不仅知道答案是否正确，还能获得关于证据选择方向的反馈，从而学习把有限的推理预算集中到真正有用的信息上。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

GEAR（Grounding Evidence-Aware Reward）是一种用于长上下文推理强化学习的奖励塑形方法。其输入是带有答案及证据位置标注的长上下文问题：支持答案的文本被划为关键证据 $x^{\mathrm{key}}$，其余内容划为干扰上下文 $x^{\mathrm{dist}}$。模型生成推理轨迹 $y$ 和最终答案后，系统先计算答案正确性，再分别计算 $y$ 与关键证据、干扰上下文的 $n$-gram 重叠率；总奖励在正确性奖励上增加关键证据重叠奖励，并扣除干扰内容重叠惩罚。该奖励用于 GSPO（Group Sequence Policy Optimization）训练 Qwen3.5 系列模型，最终输出策略模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造带证据边界的长上下文训练样本

对程序化数据直接读取生成器提供的支持位置；对自然文档则先过滤不适合问答的文档，将其切成每块 1,024 字符的文本块，随机选择 1–3 块作为指定证据区域，并约束语言模型仅依据这些块生成问题、单值答案和 1–3 条原文证据。

<div class="method-step__io" markdown="1">

**输入**：程序化生成的 GSM-Infinite、PhantomWiki 样本，或来自 RedPajama-v2 的自然语言长文档 $d$。<br>
**输出**：包含问题、长上下文、参考答案、关键证据 $x^{\mathrm{key}}$ 和干扰上下文 $x^{\mathrm{dist}}$ 的训练样本。

</div>

**直观理解**：这一步先划定“允许出题的材料”，再从其中出题，因此证据位置天然已知，不必在生成问题后重新人工寻找证据。其余长文本则充当模型必须学会忽略的干扰信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 验证自然语言问答及证据标注

使用独立回答过程，仅向验证器提供指定证据区域并重新回答问题；只有重新得到的答案与参考答案一致时才保留该样本，同时将答案限制为数字或实体短语等单值响应，并排除是非题。

<div class="method-step__io" markdown="1">

**输入**：由指定证据块生成的问题、参考答案和证据区域。<br>
**输出**：能够由指定关键证据独立、明确回答的自然语言训练样本。

</div>

**直观理解**：该步骤检查题目是否真的只靠标出的证据就能回答，避免模型因证据标错而受到错误奖励。单值答案也使正确性奖励可以自动判定。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成推理轨迹并计算证据相关重叠

将提示各区域转换为不同 $n$-gram 的集合，并用滑动窗口统计推理轨迹中有多少 $n$-gram 分别出现在关键证据和干扰上下文中；若某个 $n$-gram 同时存在于两者，则从干扰项中排除，以免惩罚对合法证据的引用。

<div class="method-step__io" markdown="1">

**输入**：提示 $x$、其关键证据 $x^{\mathrm{key}}$、干扰上下文 $x^{\mathrm{dist}}$，以及当前策略生成的推理轨迹 $y$ 和最终答案。<br>
**输出**：答案正确性 $R_{\mathrm{acc}}$、关键证据重叠率 $\mathrm{Overlap}_n(y\|x^{\mathrm{key}})$ 和干扰重叠率 $\mathrm{Overlap}_n(y\|x^{\mathrm{dist}})$。

</div>

**直观理解**：系统不只检查模型是否答对，还检查它在思考时“抄了哪里”。引用关键事实会得到鼓励，复述无关长文则会留下可被惩罚的统计信号。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算 GEAR 奖励并执行策略优化

按照 $R(x,y)=R_{\mathrm{acc}}+\alpha\,\mathrm{Overlap}_n(y\|x^{\mathrm{key}})-\beta\,\mathrm{Overlap}_n(y\|x^{\mathrm{dist}})$ 合成奖励，并以该奖励通过 GSPO 更新策略；默认使用 $n=3$、$\alpha=0.1$、$\beta=0.3$。

<div class="method-step__io" markdown="1">

**输入**：每条 rollout 的正确性奖励、关键证据重叠率、干扰重叠率，以及同一提示下的一组模型输出。<br>
**输出**：更偏向提取关键证据、减少无关复述，同时保持答案正确性的长上下文推理策略。

</div>

**直观理解**：仅奖励关键证据可能诱使模型把整篇输入都复制一遍，因为这样同样能覆盖证据；加入更强的干扰惩罚后，最有利的策略才变成“只抓有用信息”。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### $n$-gram 重叠率

$$
\text{Overlap}_{n}(y\|x)=\frac{1}{m-n+1}\sum_{i=1}^{m-n+1}\mathbf{1}\!\left[(y_i,\ldots,y_{i+n-1})\in\mathcal{N}_{n}(x)\right]
$$

**符号说明**

- $x$：输入提示，或计算时选定的关键证据、干扰上下文子区域。
- $y=(y_1,\ldots,y_m)$：模型生成的推理轨迹，由 $m$ 个词元组成。
- $m$：推理轨迹 $y$ 的词元数。
- $n$：连续匹配片段的长度；训练默认取 $3$，诊断证据选择性时取 $10$。
- $\mathcal{N}_{n}(x)$：从输入区域 $x$ 收集的所有不同 $n$-gram 组成的查询集合。
- $\mathbf{1}[\cdot]$：指示函数：条件成立时为 $1$，否则为 $0$。
- $i$：推理轨迹中滑动窗口的起始位置。

<div class="equation-explanation" markdown="1">

**直观理解**：该式依次检查推理轨迹中的每个长度为 $n$ 的连续窗口是否也出现在输入文本中，再用匹配窗口数除以全部窗口数。结果越高，说明推理轨迹中直接沿用输入连续片段的比例越大；对 $x^{\mathrm{key}}$ 和 $x^{\mathrm{dist}}$ 分别计算后，便能区分有依据的引用与无关复制。<br>
**原文位置**：式（1），第 3.1 节

</div>

</div>

<div class="equation-block" markdown="1">

#### GEAR 总奖励

$$
R(x,y)=R_{\mathrm{acc}}+\alpha\cdot\text{Overlap}_{n}(y\|x^{\mathrm{key}})-\beta\cdot\text{Overlap}_{n}(y\|x^{\mathrm{dist}})
$$

**符号说明**

- $R(x,y)$：提示 $x$ 下生成推理轨迹 $y$ 所获得的 GEAR 总奖励。
- $R_{\mathrm{acc}}\in\{0,1\}$：最终答案是否正确的二值奖励；正确为 $1$，错误为 $0$。
- $x^{\mathrm{key}}$：包含解题所需事实的关键证据文本。
- $x^{\mathrm{dist}}$：提示中除关键证据外的干扰上下文。
- $\text{Overlap}_{n}(y\|x^{\mathrm{key}})$：推理轨迹与关键证据之间的 $n$-gram 重叠率。
- $\text{Overlap}_{n}(y\|x^{\mathrm{dist}})$：推理轨迹与干扰上下文之间的 $n$-gram 重叠率。
- $\alpha$：关键证据重叠奖励的非负权重，默认值为 $0.1$。
- $\beta$：干扰重叠惩罚的非负权重，默认值为 $0.3$。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项要求最终答案正确，第二项奖励推理轨迹接触真正有用的证据，第三项扣除复述无关上下文所获得的收益。将 $\beta$ 设得高于 $\alpha$，体现了作者的核心设计判断：关键证据奖励只需适度，而抑制干扰复制必须足够强，才能防止模型通过扩大总体复制量来投机。<br>
**原文位置**：式（3），第 4.1 节

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标是在 GSPO 框架中提高策略对高 GEAR 奖励序列的生成倾向。对同一提示采样一组完整输出后，以式（3）给每条序列评分并形成组内相对优化信号；因此，能答对、适度引用 $x^{\mathrm{key}}$ 且较少复述 $x^{\mathrm{dist}}$ 的序列会优于答错或无差别复制的序列。这里的重叠项不是单独训练的分类器，也不依赖外部检索器，而是由已有证据位置和生成文本直接计算。作者选择 $\alpha=0.1$、$\beta=0.3$，意味着干扰复制的单位惩罚强于关键证据重叠的单位奖励；这一不对称性用于堵住“复制全部输入也能提高关键证据重叠率”的奖励漏洞。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 证据标注数据构造模块**

该模块统一产生分区后的 $x^{\mathrm{key}}$ 与 $x^{\mathrm{dist}}$。GSM-Infinite 和 PhantomWiki 直接使用程序生成器给出的支持位置；自然语言数据采用“先选证据块、后生成问题、再仅凭证据复答验证”的三阶段流程，从而以构造方式获得支持标注。

> 直观理解：GEAR 必须知道哪些文本有用、哪些文本无关。程序化任务自带这份答案，而自然文档则通过先圈定材料再出题，低成本地制造同样的监督信号。

**2. 基于 $n$-gram 的证据匹配模块**

模块把长度为 $n$ 的连续词元片段作为匹配单位，分别建立提示关键区域和干扰区域的 $n$-gram 查询集合，再扫描推理轨迹计算匹配窗口比例。训练采用 $n=3$ 以提供较密集的奖励信号；论文的故障诊断采用 $n=10$，因为较长连续片段更能排除偶然词汇重合并识别明确转录。

> 直观理解：它类似用短语指纹检查推理文本来自输入的哪一部分。三词片段出现得更频繁，适合给强化学习持续反馈；十词片段证据更严格，适合分析模型是否真的在大段照抄。

**3. 双向证据感知奖励模块**

奖励由二值正确性项 $R_{\mathrm{acc}}$、正向关键证据项 $R_{\mathrm{ground}}=\alpha\,\mathrm{Overlap}_n(y\|x^{\mathrm{key}})$ 和负向干扰项 $R_{\mathrm{dist}}=\beta\,\mathrm{Overlap}_n(y\|x^{\mathrm{dist}})$ 组成。关键证据与干扰区域共有的 $n$-gram 不计入干扰惩罚，避免同一通用短语同时触发奖励和惩罚。

> 直观理解：正确性项保证模型仍以解决问题为目标，证据奖励告诉它该关注哪里，干扰惩罚告诉它不该复述哪里。正负两项缺一不可：只有奖励会鼓励“全抄”，只有惩罚又可能让模型完全不接触输入证据。

**训练与推理**

训练数据共 3,200 题，包括 1,000 条 GSM-Infinite、1,000 条 PhantomWiki，以及从 RedPajama-v2 文档自动合成并验证的 1,200 条自然语言问答。训练时，每条样本提供长上下文、问题、参考答案和证据分区；Qwen3.5-9B、Qwen3.5-27B 或 Qwen3.5-35B-A3B 针对提示生成一组推理轨迹与答案，系统自动判定 $R_{\mathrm{acc}}$，以 $n=3$ 计算关键证据和干扰上下文的重叠率，合成 GEAR 奖励后通过 GSPO 更新模型。训练上下文长度在 16k–32k 词元之间均匀分布，使策略在不同长输入规模上学习证据选择行为。

推理阶段不再需要参考答案、支持位置或奖励计算，只需将新长上下文问题输入训练后的模型并自回归生成推理轨迹与最终答案。因而，证据标注是训练监督而非部署依赖；论文方法本身也没有增加外部检索、证据分类器或推理时验证器。不过，对训练范围之外的自然问题，模型能否准确定位证据来自参数更新后的行为泛化，而不是测试时获得显式证据边界。

**复现信息**

复现所需的关键设置如下：基础模型为 Qwen3.5-9B、Qwen3.5-27B 和混合专家模型 Qwen3.5-35B-A3B；优化算法为 GSPO；奖励默认采用 $n=3$、$\alpha=0.1$、$\beta=0.3$。模型训练 $1$ 个 epoch，约 $100$ 个优化步骤，学习率为 $2\times10^{-6}$，批大小为 $32$，每组 rollout 数为 $8$；最大提示长度为 32k 词元，最大生成长度为 16k 词元。自然文档按每块 1,024 字符切分，每题随机指定 1–3 块作为证据，并保留 1–3 条精确证据引文；若一个 $n$-gram 同时出现在关键证据和干扰上下文中，必须从干扰惩罚统计中移除。需要注意，32k 是训练提示上限，而实验还评估了 128k 上下文，因此超长上下文结果同时反映了长度外推能力；原文节选未进一步说明解码温度、采样参数、GSPO 的裁剪或正则化超参数。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Ruler：合成长上下文检索基准，测试模型在不同上下文长度下抽取多个键及其对应多个值的能力；与 GEAR 训练数据不重叠。实验同时使用上下文不超过 $32\mathrm{k}$ 的子集和完整 $128\mathrm{k}$ 集合，其作用是检验精确检索与长度扩展能力。
- LongBench-v2 与 BrowseComp-LC：前者覆盖多种长上下文理解任务，后者要求综合长篇网页文档中分散的信息；二者均与训练数据不重叠，并在 $32\mathrm{k}$ 子集和 $128\mathrm{k}$ 完整集合上评测。它们分别检验任务覆盖面以及跨文档证据综合能力。
- GraphWalks 与 AA-LCR：GraphWalks 要求模型根据长文本形式的图描述执行多跳路径跟踪并保存中间状态；AA-LCR 是长上下文推理基准，且所有样本均超过 $32\mathrm{k}$，因此只出现在 $128\mathrm{k}$ 结果中。二者主要检验结构化多步推理和超长上下文推理能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**各基准任务得分**

衡量模型在对应检索、理解、网页信息综合、图路径推理或长上下文推理任务上的表现；节选未说明各基准得分的具体计算公式。 （越高越好，因为原文以最高得分判断最佳配置。）

</div>
<div class="metric-item" markdown="1">

**跨基准平均得分**

汇总同一模型规模和上下文长度下各基准的表现，用于比较不同训练配置的总体长上下文能力；原文未明确报告平均方式或是否加权。 （越高越好，表示该配置在多种长上下文任务上的综合表现更强。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### $32\mathrm{k}$ 上下文，三种模型规模，完整 GEAR 对比准确率奖励 GSPO

<div class="result-value" markdown="1">

完整 GEAR 的跨基准平均得分分别提高 $2.8$ 分（$9\mathrm{B}$）、$2.1$ 分（$35\mathrm{B}$-A3B）和 $1.5$ 分（$27\mathrm{B}$）。

</div>

作者结果表明，联合奖励在训练长度范围附近对三个模型规模均有正收益，并非只对某一参数规模有效。分析上，这支持“证据筛选奖励具有跨规模稳定性”，但平均分掩盖了各数据集的差异；没有方差或显著性检验时，也不能据此判断每项提升是否统计显著。

<div class="result-source" markdown="1">

来源：第 5.1 节 Main Results，Table 1 结果说明

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At 32k context, GEAR improves over accuracy-only GSPO by +2.8 (9B), +2.1 (35B-A3B), and +1.5 (27B) points on average.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### $128\mathrm{k}$ 上下文，三种模型规模，完整 GEAR 对比准确率奖励 GSPO

<div class="result-value" markdown="1">

完整 GEAR 的跨基准平均增益扩大为 $4.6$ 分（$9\mathrm{B}$）、$2.8$ 分（$35\mathrm{B}$-A3B）和 $2.1$ 分（$27\mathrm{B}$）。

</div>

作者将更大的增益解释为：上下文越长，定位关键证据越困难，证据感知奖励越有价值。与 $32\mathrm{k}$ 结果相比，这一趋势与该解释一致；但实验只比较两个长度档位，且 $32\mathrm{k}$ 与 $128\mathrm{k}$ 纳入的样本并不完全相同，因此不能单独证明上下文长度是增益扩大的唯一原因。

<div class="result-source" markdown="1">

来源：第 5.1 节 Main Results，Table 1 结果说明

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At 128k, the gains are larger: +4.6, +2.8, and +2.1, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 全部六种“模型规模×上下文长度”组合

<div class="result-value" markdown="1">

完整 GEAR 在三种模型规模与两种上下文长度构成的全部六种组合中均取得最高平均得分。

</div>

这说明联合使用关键证据奖励和干扰项惩罚的方案，在所报告设置中具有最稳定的总体排序。它证明的是这些基准和配置下的相对优势，不等同于对所有长上下文任务、其他基础模型或超过 $128\mathrm{k}$ 的上下文都能保持最佳。

<div class="result-source" markdown="1">

来源：第 5.1 节 Main Results，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GSPO + GEAR achieves the highest average score in all six model–context combinations.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 节选只提供平均增益和定性总结，没有 Table 1 与 Table 3 的完整逐数据集数值，也未报告重复实验、误差条或统计显著性，因此无法核验收益是否由少数数据集驱动，或小幅提升是否稳定。
- $32\mathrm{k}$ 使用可装入该长度的任务子集，而 $128\mathrm{k}$ 使用完整集合并额外包含 AA-LCR；因此两个长度下增益的直接比较同时受到上下文长度与样本组成变化影响。作者关于长度外推的结论有实验支持，但不能仅凭该比较严格归因于长度增加。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 预训练 Qwen3.5 基座模型：不经过所述强化学习训练，用于衡量训练前的原始长上下文能力。
- GSPO 加准确率奖励：只根据最终答案是否正确进行强化学习，是判断收益究竟来自一般的结果监督还是 GEAR 特有证据奖励的核心基线。
- GSPO 加 $R_{\mathrm{ground}}$：在准确率奖励之外只加入证据定位奖励，用于隔离“鼓励依据关键证据作答”这一正向信号的独立效果。
- GSPO 加完整 GEAR，即同时加入 $R_{\mathrm{ground}}$ 与 $R_{\mathrm{dist}}$：前者鼓励利用关键证据，后者惩罚复制或依赖干扰内容；该配置用于检验模型能否学会区分相关与无关上下文，而非笼统增加或减少复制。

**实验想回答的问题**

- 完整的证据感知奖励 GEAR 相比仅使用答案准确率奖励的 GSPO，能否在不同模型规模、不同类型的长上下文任务以及 $32\mathrm{k}$ 和 $128\mathrm{k}$ 两种上下文长度下稳定提升性能？
- GEAR 的证据定位奖励 $R_{\mathrm{ground}}$ 与干扰信息惩罚 $R_{\mathrm{dist}}$ 是否必须联合使用，以及这种训练得到的证据筛选能力能否从 $16\mathrm{k}$–$32\mathrm{k}$ 训练上下文外推到未见过的 $128\mathrm{k}$ 上下文？

**实验实现**

评测覆盖 Qwen3.5 的 $9\mathrm{B}$、$35\mathrm{B}$-A3B 和 $27\mathrm{B}$ 三种模型规模。每个规模比较预训练基座、准确率奖励 GSPO、加入 $R_{\mathrm{ground}}$ 的 GSPO，以及同时加入 $R_{\mathrm{ground}}$ 和 $R_{\mathrm{dist}}$ 的完整 GEAR。所有基准均与训练数据不重叠；$32\mathrm{k}$ 设置仅保留上下文可装入 $32\mathrm{k}$ token 的任务，$128\mathrm{k}$ 设置使用完整集合。由于 AA-LCR 全部样本超过 $32\mathrm{k}$，它只计入 $128\mathrm{k}$ 列。GEAR 的训练上下文长度为 $16\mathrm{k}$–$32\mathrm{k}$，因此 $128\mathrm{k}$ 评测还承担长度分布外泛化测试。节选未给出解码参数、重复运行次数、误差条或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 仅在准确率奖励上加入 $R_{\mathrm{ground}}$，不加入 $R_{\mathrm{dist}}$ | 相对准确率奖励 GSPO，平均性能在 $32\mathrm{k}$ 下最多下降 $5.1$ 分，在 $128\mathrm{k}$ 下最多下降 $8.3$ 分；GraphWalks 和 BrowseComp-LC 的退化尤其明显。 | 该消融隔离了“只奖励证据 grounding”的效果。结果说明单纯鼓励模型贴近上下文并不足够，可能反而强化对提示内容的无差别复制；必须同时惩罚对干扰信息的依赖。这里的“可能强化复制”属于机制解释，节选没有提供直接的生成案例或因果测量。 | 第 5.1 节 Both reward components are indispensable，Table 1<br><span class="experiment-evidence">Adding the grounding reward without the distractor penalty (+$Rground+R_{\mathrm{ground}})$ consistently hurts performance relative to accuracy-only GSPO, with drops of up to 5.1 points at 32k and 8.3 points at 128k.</span> |
| 只使用干扰项惩罚，即 $\alpha=0$、$\beta=0.3$ | 性能低于基线，但所给节选未报告具体下降数值。 | 该设置去除证据定位信号，只保留减少干扰复制的约束，用于判断“少复制”本身是否足够。作者解释为：没有正向信号指向关键证据，惩罚会笼统抑制复制，连有用证据也可能被忽略。因此完整方法的关键不是简单减少复制，而是有选择地利用相关上下文。 | 第 5.1 节 Both reward components are indispensable，Table 3<br><span class="experiment-evidence">Conversely, Table 3 we demonstrate that training with only the distractor penalty ($α=0\alpha=0, β=0.3\beta=0.3)$ also yields an results worse than the baseline.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It improves long-context reasoning through evidence-aware reinforcement-learning post-training that discourages repetitive copying.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`558c107710474b2f2e94ff7079cb4ab327399d649ed6b0f6410c1c3fedae48b3`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
