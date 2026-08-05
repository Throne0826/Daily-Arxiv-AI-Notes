---
title: "[论文解读] PI-Mem: Pushing Long-Context Reasoning to 3.6M Tokens with Parallel-Iterative Memory"
description: "[arXiv 2608.03048][LLM Reasoning] PI-Mem以“并行读取、迭代整合”的共享记忆机制替代逐块串行改写，在超长上下文推理中同时改善远距离证据保留与推理延迟。"
arxiv_id: "2608.03048"
announcement_date: "2026-08-05"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:38:30.315382+00:00"
source_sha256: "fdf04cdf96c704df914d68afa71cd0ac41a763c573ad174c3023f77c25952e55"
tags:
  - "LLM Reasoning"
  - "LLM 效率"
  - "LLM 其他"
  - "长上下文推理"
  - "并行迭代记忆"
  - "循环记忆"
  - "多跳问答"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.03048</p>

# PI-Mem: Pushing Long-Context Reasoning to 3.6M Tokens with Parallel-Iterative Memory

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Dawei Liu, Haixu Song, Shuang Cheng, Shijie Wang, Haozheng Hou, Kaifeng Liu, Ermo Hua, Zhonghang Yuan, Zhijie Zhong, Yuchen Fan, Biqing Qi, Bowen Zhou</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Shanghai Jiao Tong University；Shanghai Artificial Intelligence Laboratory；Tsinghua University；Zhejiang University；Harbin Institute of Technology；University of Science and Technology of China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03048v1) · [PDF 下载](https://arxiv.org/pdf/2608.03048v1) · **关键词** 长上下文推理, 并行迭代记忆, 循环记忆, 多跳问答<br>
**代码**: [https://github.com/JetAstra/PI-Mem](https://github.com/JetAstra/PI-Mem)

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

PI-Mem以“并行读取、迭代整合”的共享记忆机制替代逐块串行改写，在超长上下文推理中同时改善远距离证据保留与推理延迟。

**不用术语来说**：面对数百万词元的文档，模型既不能总把全文一次性读完，也不能只靠不断改写一份短笔记来稳定记住关键信息：较早发现的线索可能被后续无关内容覆盖，而且逐段处理必须等待上一段完成，文档越长，耗时越大。论文要解决的是如何在有限记忆容量下，更快、更可靠地汇集散落在不同位置、需要联合使用的证据。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出PI-Mem：每轮基于同一份全局记忆并行读取所有文本块，从各块选择新增或互补证据，再合并为下一轮共享记忆；通过有限轮次的重复读取，使一个文本块中发现的信息能够指导后续从其他文本块提取证据。
- 采用端到端强化学习联合优化答案正确性与轮次效率，并引入轮次效率奖励抑制无效重复，使系统可在证据充分时提前结束，而不必固定执行全部更新轮次。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究超长上下文推理，即让大语言模型在输入远超其常规处理范围时，仍能从分散在远距离文本中的信息完成问答或多跳推理。直接扩大上下文窗口通常需要对整段序列进行密集注意力计算，计算开销高；稀疏注意力只处理部分令牌或键值块，线性注意力则把历史信息压缩为紧凑状态，但这些方法仍可能面临超长外推能力有限、训练成本高或依赖高质量合成长上下文数据等问题。因此，本文关注一种基于记忆的处理设定：把长文档切分为多个块，以固定长度的文本记忆保存与当前问题相关的信息，再据此生成答案。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**长上下文推理**

指模型需要在很长的输入中识别、保留并整合与问题相关的信息。难点不仅是找到证据，还包括把分散在远距离位置的多个证据连接起来。

</div>
<div class="concept-item" markdown="1">

**循环记忆**

循环记忆方法按顺序读取文本块，并用当前文本块和上一时刻记忆生成新的记忆。新记忆会覆盖旧记忆，因此后面出现的无关内容可能削弱早期的重要证据。

</div>
<div class="concept-item" markdown="1">

**多跳问答**

多跳问答要求模型组合来自不同位置或不同文档片段的多个事实，经过若干推理步骤得到答案。HotpotQA 是本文用于检验这类跨证据推理能力的基准。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个问题和被切分为多个文本块的超长文档，记问题为 $q$，文本块为 $C_1,[...][?]$（原文未给出统一符号，本文为便于说明采用此记号），目标是输出正确答案 $a$。模型不能或不宜把全部令牌一次性放入高成本的密集注意力计算中，而应通过有限长度的共享记忆逐步汇总证据。与按块串行更新记忆的设定不同，本文要求每一轮让所有文本块同时读取当前共享记忆，提取新的或互补的证据，再合并为下一轮记忆；当证据足够或达到预设最大轮数后，模型依据问题和最终记忆生成答案。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$q$**

用户问题。

</div>
<div class="notation-item" markdown="1">

**$C_i$**

第 $i$ 个文本块；所有文本块共同构成长文档输入。

</div>
<div class="notation-item" markdown="1">

**$M_t$**

第 $t$ 轮开始时的共享全局记忆，用于条件化该轮对所有文本块的读取。

</div>
<div class="notation-item" markdown="1">

**$T$**

记忆更新轮数；本文将其限制在预设上限内，并允许模型在证据充分时提前退出。

</div>

</div>

**直接相关的工作**

- **MemAgent（循环记忆基线）**: 本文将其作为直接比较对象。循环记忆按文本块串行处理并反复重写固定长度记忆，可能覆盖早期证据，而且后一块必须等待前一块完成，形成严格的跨块串行依赖；PI-Mem 改为在共享记忆条件下并行读取所有文本块，并通过多轮迭代实现跨块信息交换。
- **YaRN：efficient context window extension of large language models**: YaRN 代表通过位置编码方法扩展模型上下文窗口的路线。本文指出，这类方法虽然能够直接处理更长输入，但通常只在有限外推范围内可靠，并且在超长上下文上仍承担密集注意力的高计算成本，因此 PI-Mem 采用记忆压缩与分块处理来侧重效率。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

长文档问答、多轮对话、代码仓库理解和智能体工作流都要求模型从相距很远的文本位置识别、保存并组合相关信息；但随着输入增长，模型利用远距离证据的能力往往下降。若直接使用稠密注意力处理超长输入，计算代价又会迅速上升，因此实际系统需要一种可扩展的上下文管理方式。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **上下文窗口扩展与高效注意力架构**：位置编码插值或外推让模型直接接收超过原训练窗口的序列；稀疏注意力只计算部分词元或键值块之间的交互，线性注意力的递归形式则把历史内容压缩进紧凑状态，以降低超长序列的处理成本。
- **循环记忆方法**：将长输入切成多个文本块，按顺序把当前文本块与上一轮固定长度的文本记忆一起交给模型，再生成新记忆覆盖旧记忆；处理完全部文本块后，模型依据最终记忆回答问题。每次只处理有限上下文，因此总计算量可随输入长度近似线性增长。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 窗口扩展通常只在有限的外推范围内可靠，超长输入上的稠密注意力仍然昂贵；稀疏或线性注意力等架构还可能需要较高训练成本及大规模、高质量的合成长上下文语料，而这类语料难以覆盖多样化推理任务。
- 循环记忆连续把新文本块和旧记忆压缩成固定长度的新状态，早期关键证据可能在其用途尚未显现时被后续噪声覆盖；同时，各文本块之间存在严格串行依赖，后一块必须等待前一块完成记忆更新，导致延迟随上下文长度增长。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有方案尚未提供一种机制，能够在不依赖一次性处理全部超长输入的前提下，避免按文本顺序反复覆盖记忆，并允许分散证据在有限次数的信息交换中相互补充；换言之，证据保真度、跨块整合能力与并行效率仍未被统一解决。

</div>
<div markdown="1"><span>核心问题</span>

能否把长上下文记忆更新从“逐块串行覆盖”改造成“全块并行读取、少量轮次迭代整合”，并通过学习决定何时停止，从而在数百万词元上下文上同时提高多跳问答准确性和推理速度？

</div>
<div markdown="1"><span>作者直觉</span>

若所有文本块在同一轮都看到相同的全局记忆，它们就能独立寻找与当前问题和已有线索相关的内容，不必让后出现的文本块覆盖先前线索；合并首轮证据后再读一轮，又能让某处新发现的实体或关系成为检索其他文本块的提示。并行读取缩短等待链，有限轮次和提前退出则把额外迭代控制在必要范围内。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PI-Mem 将超长上下文 $C$ 切分为多个块 $\{c_i\}_{i=1}^{n}$，但不按文档顺序递归改写记忆。每一轮中，模型 $\pi_\theta$ 在同一份上一轮全局记忆 $m^{(k-1)}$ 条件下并行读取所有块；各读取调用通过 `<check>yes</check>` 或 `<check>no</check>` 判断当前块是否提供相对已有记忆而言的新证据或互补证据，仅保留肯定观察，再由一次合并调用压缩为新记忆 $m^{(k)}$。这一“并行读取—选择—合并”循环最多执行 $K$ 轮；若某轮没有新增证据则提前停止，最后仅根据问题 $q$ 和最终记忆 $m^\star$ 生成答案 $a$。

训练不是分别监督某次读取或合并，而是把一次完整工作流视为轨迹 $\tau_i$，其中包含该样本的全部读取、合并和最终回答调用。作者采用轨迹级 GRPO：依据最终答案正确性和实际轮数 $k_i$ 给整条轨迹一个奖励，并把相同的组相对优势传播到轨迹内所有生成 token，从而联合优化证据判断、记忆整合、停止决策和最终回答。直观上，PI-Mem 类似让许多读者同时检查不同章节：每个读者只上报对当前共享笔记有增量的信息，编辑再将上报内容压缩进共享笔记；下一轮所有读者依据更新后的笔记重新检查，因此既能发现依赖先前线索的证据，又避免一个读者按顺序阅读时让后文噪声覆盖前文要点。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 上下文分块与状态初始化

将 $C$ 划分为近似等长的块 $\{c_i\}_{i=1}^{n}$，并将初始全局记忆设为空，即 $m^{(0)}=\texttt{EMPTY}$；同时用 $m^\star$ 保存最近一次有效合并后的记忆。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、完整上下文 $C$、模型 $\pi_\theta$ 和最大迭代轮数 $K$。<br>
**输出**：上下文块集合 $\{c_i\}_{i=1}^{n}$、空记忆 $m^{(0)}$ 和迭代控制状态。

</div>

**直观理解**：先把一本超长资料拆给多个读者，并准备一张最初为空的共享笔记。分块使单次模型调用不必承载整个超长上下文。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 条件化并行读取

对所有块并行执行 $o_i^{(k)}=\textsc{ReadCall}(\pi_\theta,q,c_i,m^{(k-1)})$；所有调用看到同一份记忆，并必须输出检查信号以及在信号为 yes 时给出相关证据。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、每个上下文块 $c_i$、上一轮共享记忆 $m^{(k-1)}$。<br>
**输出**：第 $k$ 轮的块级观察集合 $\{o_i^{(k)}\}_{i=1}^{n}$，每项带有 `<check>` 信号。

</div>

**直观理解**：所有读者同时根据同一张共享笔记检查各自章节，因此后读的章节不会逐步覆盖先读章节形成的中间状态。并行调用也缩短了随块数增长的串行关键路径。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 增量证据选择

构造 $O^{(k)}=\{o_i^{(k)}\mid\chi(o_i^{(k)})=\text{yes}\}$，只保留与问题相关且相对 $m^{(k-1)}$ 新增或互补的观察；若 $O^{(k)}=\emptyset$，立即结束迭代。

<div class="method-step__io" markdown="1">

**输入**：全部块级观察 $\{o_i^{(k)}\}$ 及其检查信号 $\chi(o_i^{(k)})$。<br>
**输出**：选中观察集合 $O^{(k)}$，或触发自适应退出。

</div>

**直观理解**：不是把每位读者的所有摘录都塞进笔记，而是只接收确实增加信息的上报。没有人找到新内容时，系统认为现有证据已足够或继续搜索无益。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 跨块压缩合并与迭代细化

执行 $m^{(k)}=\textsc{MergeCall}(\pi_\theta,q,m^{(k-1)},O^{(k)})$，整合跨块证据、去除重复并保留回答所需细节；随后以 $m^{(k)}$ 为条件重新并行读取所有块，直至无新增证据或达到 $K$ 轮。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$、旧记忆 $m^{(k-1)}$ 和选中观察 $O^{(k)}$。<br>
**输出**：紧凑的更新记忆 $m^{(k)}$，最终记为 $m^\star$。

</div>

**直观理解**：编辑不会简单拼接所有摘录，而是把它们改写成一份长度受控、相互关联的笔记。重新阅读允许模型在发现一条线索后，再识别先前看似无关但现在有意义的跨文档证据。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 并行迭代记忆更新与证据选择

$$
\begin{aligned} m^{(k)}&=\textsc{Turn}\!\left(\pi_{\theta},q,m^{(k-1)},\{c_i\}_{i=1}^{n}\right),\\ o_i^{(k)}&=\textsc{ReadCall}\!\left(\pi_{\theta},q,c_i,m^{(k-1)}\right),\\ O^{(k)}&=\left\{o_i^{(k)}\mid \chi(o_i^{(k)})=\mathrm{yes}\right\},\\ m^{(k)}&=\textsc{MergeCall}\!\left(\pi_{\theta},q,m^{(k-1)},O^{(k)}\right). \end{aligned}
$$

**符号说明**

- $q$：待回答的问题。
- $C$：完整背景上下文。
- $c_i$：上下文的第 i 个分块。
- $n$：上下文分块总数。
- $\pi_\theta$：参数为 θ、承担读取、合并和回答调用的语言模型策略。
- $k$：当前读取—选择—合并轮次。
- $m^{(k-1)},m^{(k)}$：第 k 轮更新前后的共享全局记忆。
- $o_i^{(k)}$：第 k 轮读取第 i 个块产生的观察。
- $\chi(o_i^{(k)})$：观察中 `<check>` 标签的值，用于判断是否包含新增或互补证据。
- $O^{(k)}$：第 k 轮通过检查的观察集合；该集合为空时触发提前退出。

<div class="equation-explanation" markdown="1">

**直观理解**：这些关系定义了 PI-Mem 的核心状态转移：同一轮的每个块都依据同一旧记忆独立产生观察，筛选后再集中形成唯一的新记忆。因此信息交换只通过轮次之间的共享记忆发生，而不是在同一轮按块顺序传递，这既减轻顺序覆盖，也提供块级并行性。<br>
**原文位置**：Method，Read-Select-Merge Turn，公式（1）—（2）及 Algorithm 1

</div>

</div>

<div class="equation-block" markdown="1">

#### 轨迹奖励与组相对优势

$$
\begin{aligned} r_{\mathrm{turn}}(\tau_i)&=\frac{K-k_i}{K-1},\\ R_i&=r_{\mathrm{acc}}(a_i)+\lambda_{\mathrm{turn}}r_{\mathrm{turn}}(\tau_i),\\ A_i&=R_i-\frac{1}{G}\sum_{j=1}^{G}R_j. \end{aligned}
$$

**符号说明**

- $\tau_i$：第 i 条完整工作流轨迹，包含其全部读取、合并和最终回答调用。
- $K$：允许的最大读取—选择—合并轮数。
- $k_i$：第 i 条轨迹实际使用的轮数。
- $r_{\mathrm{turn}}(\tau_i)$：轮数效率奖励；使用轮数越少，数值越高。
- $a_i$：第 i 条轨迹产生的最终答案。
- $r_{\mathrm{acc}}(a_i)$：根据最终答案正确性计算的准确性奖励。
- $\lambda_{\mathrm{turn}}$：轮数效率奖励在总奖励中的权重。
- $R_i$：第 i 条完整轨迹的标量总奖励。
- $G$：针对同一训练问题采样的完整轨迹数量。
- $A_i$：第 i 条轨迹相对于同组平均奖励的优势值。

<div class="equation-explanation" markdown="1">

**直观理解**：奖励首先要求最终答案正确，再对少用轮次的正确轨迹给予额外收益；随后用轨迹奖励减去同组平均值，判断该轨迹比同一问题的其他采样更好还是更差。整条轨迹中的所有模型调用共享 $A_i$，所以最终回答的成败和停止效率会共同反向影响早期证据选择与合并行为。<br>
**原文位置**：Method，Trajectory-Level Reinforcement Learning，公式（4）—（5）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：对每个训练问题，旧策略 $\pi_{\theta_{\mathrm{old}}}$ 采样 $G$ 条完整轨迹，每条轨迹 $\tau_i=\{(x_{i,s},y_{i,s})\}_{s=1}^{S_i}$ 包含 $S_i$ 次阶段特定调用；$x_{i,s}$ 是由当前工作流状态构造的读取、合并或回答提示，$y_{i,s}$ 是对应生成。作者以最终答案准确性和轮数效率计算 $R_i$，再采用不除以组内标准差的 Dr. GRPO 式组相对优势 $A_i$；同一 $A_i$ 广播到轨迹内每次调用的每个 token，使优化评价的是完整工作流，而非孤立调用。

具体更新使用带裁剪的 token 级策略比率：当前策略相对旧策略的生成概率变化被限制在 $1-\varepsilon$ 到 $1+\varepsilon$ 附近，以避免一次更新过大；所有轨迹、所有调用的 token 损失按 DAPO 风格以生成 token 总数聚合，并加入系数为 $\beta$ 的、当前策略 $\pi_\theta$ 相对参考策略 $\pi_{\mathrm{ref}}$ 的 KL 约束。因而训练目标同时学习四件事：识别增量证据、压缩跨块信息、在证据足够时退出、根据最终记忆正确作答；轮数奖励不是单纯削减计算量，而是用最终正确性约束“少轮次”不能以随意早停为代价。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 并行条件化读取器**

每轮的全部 $\textsc{ReadCall}$ 共享问题 $q$ 和记忆 $m^{(k-1)}$，但分别处理块 $c_i$，块间不存在同轮内的递归依赖，因此可以并发执行并跨样本批处理。与顺序记忆方法不同，块 $c_i$ 的输出不会成为同轮下一个块的输入。

> 直观理解：该设计直接针对两类瓶颈：一是后续无关块不断改写状态造成早期证据丢失，二是逐块串行导致延迟随上下文长度累积。代价是多轮时会重复读取各块，但并行性使这种重复通常比长串行链更适合 GPU。

**2. 检查信号驱动的选择—合并记忆**

读取器以显式信号 $\chi(o_i^{(k)})\in\{\text{yes},\text{no}\}$ 判断观察是否对当前记忆有增量；选择器丢弃 no 项，合并器再联合压缩 $m^{(k-1)}$ 与 $O^{(k)}$。合并不是简单串接，而是要求消除冗余、连接跨块事实并限制记忆增长。

> 直观理解：选择解决“哪些信息值得写入”，合并解决“如何把值得保留的信息组织成短而完整的笔记”。缺少选择会积累噪声，缺少合并则会让证据碎片化并使中间上下文快速膨胀。

**3. 迭代细化与自适应退出**

后续轮次以更新后的 $m^{(k)}$ 重新判断所有块的相关性，使共享记忆成为跨块信息交换通道；当 $O^{(k)}=\emptyset$ 或轮数达到 $K$ 时停止。训练中的轮数效率奖励进一步鼓励模型在证据充分后稳定输出 no，而不是机械耗尽轮数预算。

> 直观理解：有些事实只有在先找到另一条线索后才显得相关，因此单轮贪心筛选可能漏证据；迭代负责补漏，自适应退出负责避免无意义的反复阅读。二者共同平衡证据完整性与推理延迟。

**训练与推理**

训练数据沿用 MemAgent 的合成 HQA 构造：把 HotpotQA 的金标准段落嵌入同数据集采样的干扰文章中，使模型必须在长上下文中收集多跳证据。Qwen2.5-7B 使用已发布的约 $28\mathrm{K}$ token、每样本 200 篇文章的数据；Qwen3.5-35B-A3B 使用同一流程扩展到约 $140\mathrm{K}$ token、每样本 1,000 篇文章。每次 rollout 从空记忆开始运行完整 PI-Mem，得到读取、选择、合并、退出和回答组成的轨迹，再由轨迹级 GRPO 联合更新模型；这意味着训练长度明显短于测试时最高 $3.6\mathrm{M}$ token，超长能力主要来自分块工作流的可扩展性，而不是在同等长度上直接训练。

推理时先切分任意长度上下文，并将同轮所有 $\textsc{ReadCall}$ 批量并行执行。若存在 yes 观察，则调用一次 $\textsc{MergeCall}$ 更新共享记忆并进入下一轮；若全部为 no，则保留最近有效的 $m^\star$ 并提前结束，达到 $K$ 也强制停止。最终 $\textsc{FinalCall}$ 只接收 $q$ 与 $m^\star$。这种结构降低的是墙钟时间中的串行依赖，不保证总计算量始终最小：每轮重新读取全部块可能增加 FLOPs，但在超长上下文下可通过并行执行显著缩短端到端延迟。

**复现信息**

公平解释结果所需的关键配置是：两个模型训练时均设最大轮数 $K=3$；Qwen2.5-7B 的块大小为 $5\mathrm{K}$ token、最大输出长度为 1,024、GRPO 组大小 $G=16$，Qwen3.5-35B-A3B 的对应设置为 $15\mathrm{K}$、4,096 和 $G=8$。两者使用学习率 $1\times10^{-6}$、裁剪比率 $\varepsilon=0.2$、KL 系数 $\beta=1\times10^{-3}$；Qwen3.5 关闭 thinking mode，以减少 rollout 输出长度和训练成本。消融中轮数效率权重设为 $\lambda_{\mathrm{turn}}=0.2$。

比较训练条件存在需要注意的差异：Qwen3.5 上的 PI-Mem 与 MemAgent 使用相同的更长合成数据和相同超参数重新训练；Qwen2.5 上仅训练 PI-Mem，而 MemAgent 使用官方发布检查点。系统效率方面，同轮块读取可并行并跨样本批处理，但合并调用和轮次之间仍是串行的；因此实际加速依赖硬件并发、批处理方式、块大小、选中观察数量和实际退出轮数，不能仅由渐近复杂度推断。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HotpotQA（HQA）：多跳问答数据集。训练时将答案所需的 gold paragraphs 嵌入同数据集抽取的干扰文档中；Qwen3.5-35B-A3B 每个训练样本含 1,000 篇文档、约 140K tokens，Qwen2.5-7B 每个样本含 200 篇文档、约 28K tokens。由于强化学习训练数据由 HQA 合成，RULER 中的 HQA 被视为分布内任务，主要检验跨文档证据发现与组合能力。
- RULER：合成长上下文基准，覆盖信息检索、多跳追踪、聚合和问答，并在多个上下文长度上评测；除 HQA 外，其余任务均被作者视为分布外任务。每个子任务、每个上下文长度使用 64 个样本，用于测试方法能否扩展到训练分布之外以及最长约 $3.6$M tokens 的输入。
- LongBench v2：包含 503 道四选一题，覆盖六类真实任务。论文仅报告 Qwen3.5-35B-A3B 的结果；作者称 Qwen2.5-7B 上所有被测方法都接近四选一随机猜测水平，因此不作方法间比较。该基准用于补充检验真实长文本任务，而非只看合成检索场景。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Sub-EM／目标值覆盖比例**

单答案任务采用归一化答案匹配 Sub-EM，判断预测是否与目标答案匹配；多答案任务计算预测中出现的目标值占全部目标值的比例。它们分别衡量答案是否正确命中以及多目标召回是否完整。 （越高越好，因为更高分表示模型命中了更多标准答案；但该指标主要评价最终答案字符串，不直接诊断证据链是否忠实。）

</div>
<div class="metric-item" markdown="1">

**LongBench v2 官方指标**

按照 LongBench v2 的官方协议评价四选一长上下文问题，衡量真实任务类别上的选择准确性。原文节选未进一步给出指标计算细节。 （越高越好，因为正确选择比例更高；四选一随机水平约为 25%，接近该水平时方法差异难以解释。）

</div>
<div class="metric-item" markdown="1">

**推理加速比**

比较 PI-Mem 与循环记忆基线的推理速度，反映并行读取全部文本块后，端到端推理耗时缩短的倍数。 （越高越好，因为更大的加速比表示相对基线所需时间更少；但摘要未说明计时边界、吞吐量和延迟的具体统计方式。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3.5-35B-A3B，HotpotQA 长上下文评测，最长约 $3.6$M tokens；相对循环记忆基线 MemAgent。

<div class="result-value" markdown="1">

作者报告 PI-Mem 的得分相对循环记忆基线提高 6.25 个绝对百分点。

</div>

这一结果支持并行读取文本块并反复整合共享记忆可以缓解串行更新中早期关键证据被后续内容覆盖的问题。它说明在该骨干、数据构造和 HQA 评价方式下 PI-Mem 更有效，但不能单独证明对所有长上下文任务、其他模型或自然文档分布都同样提升。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We evaluate PI-Mem with Qwen3.5-35B-A3B and Qwen2.5-7B on the HotpotQA benchmark across context lengths up to 3.6 million tokens and find that it outperforms the recurrent-memory baseline by +6.25 and +7.81 absolute points while achieving 6.1× and 2.1× inference speedups, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen2.5-7B-Instruct，HotpotQA 长上下文评测，最长约 $3.6$M tokens；相对使用相同骨干的官方 MemAgent 检查点。

<div class="result-value" markdown="1">

作者报告 PI-Mem 的得分相对循环记忆基线提高 7.81 个绝对百分点。

</div>

较小的稠密模型上仍出现提升，表明收益并非只存在于 Qwen3.5 的 MoE 与混合注意力架构中。不过两种骨干的训练规模、分块长度和基线获取方式并不完全相同，因此 7.81 与 6.25 个百分点不能直接解释为小模型受益更多。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We evaluate PI-Mem with Qwen3.5-35B-A3B and Qwen2.5-7B on the HotpotQA benchmark across context lengths up to 3.6 million tokens and find that it outperforms the recurrent-memory baseline by +6.25 and +7.81 absolute points while achieving 6.1× and 2.1× inference speedups, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### PI-Mem 相对循环记忆基线的推理效率比较，分别使用 Qwen3.5-35B-A3B 与 Qwen2.5-7B-Instruct。

<div class="result-value" markdown="1">

作者报告两种骨干上的推理加速比分别为 $6.1\times$ 和 $2.1\times$。

</div>

该结果与方法设计相符：PI-Mem 在每轮中并行处理全部块，而串行循环记忆存在逐块依赖，因此前者更容易控制随上下文长度增加的延迟。该数字证明了特定硬件和实现下相对基线的速度优势，但摘要与所给实验节选未明确计时口径，也不能据此推断成本、峰值显存或所有部署环境下的加速幅度。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We evaluate PI-Mem with Qwen3.5-35B-A3B and Qwen2.5-7B on the HotpotQA benchmark across context lengths up to 3.6 million tokens and find that it outperforms the recurrent-memory baseline by +6.25 and +7.81 absolute points while achieving 6.1× and 2.1× inference speedups, respectively.

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

- Vanilla 与 YaRN：Vanilla 直接让骨干模型处理上下文，检验记忆工作流相对标准推理的价值；YaRN 以缩放因子 4.0 外推位置编码，代表通过扩展模型可接受长度而不显式压缩记忆的直接推理路线。
- RAG：对每个样本的解码文本块单独建立 Okapi BM25 索引，以原问题为查询并选取分数最高的 6 个块，再基于检索证据作答。它检验 PI-Mem 相对一次性稀疏检索的优势，尤其是问题关键词不足以直接定位全部多跳证据时的差异。
- MemAgent：与 PI-Mem 最直接的循环记忆基线，按块串行更新记忆。Qwen3.5 实验采用相同强化学习超参数训练，Qwen2.5 则使用官方发布且骨干相同的检查点，用来隔离并行迭代记忆相对串行记忆更新的准确率与速度影响。
- GRU-Mem 与 ReMemR1：其他循环记忆工作流，论文采用其已发表的 HQA 结果。它们扩大了记忆方法的比较范围，但由于结果并非在本文统一流程下重新评测，横向比较的控制程度弱于 MemAgent。

**实验想回答的问题**

- 在最长约 $3.6$M token 的上下文中，PI-Mem 能否比直接推理、检索增强和串行循环记忆方法更准确地完成长文本检索与多跳问答，同时降低随上下文长度增长的推理延迟？
- PI-Mem 的收益是否确实来自多轮共享记忆迭代，以及该方法对最大轮数 $K$、分块大小和记忆容量等关键设计是否稳健？

**实验实现**

Qwen3.5-35B-A3B 是采用混合注意力的 MoE 模型，PI-Mem 使用 15K-token 分块、4,096-token 最大输出长度和最大轮数 $K=3$；其训练数据约 140K tokens，关闭 thinking mode。与 MemAgent 公平训练时，rollout batch 为 128 个提示，每个提示的 GRPO group size 为 8，共 80 个 rollout steps，即按提示计 10,240 个训练样本。Qwen2.5-7B-Instruct 是全注意力稠密模型，使用 5K-token 分块、1,024-token 最大输出长度、每提示 16 次 rollout 和 240 个 rollout steps，并与同骨干的官方 MemAgent 检查点比较。

评测时温度为 0.7、top-$p$ 为 0.95；Qwen3.5 关闭 thinking mode，Qwen2.5 不适用。推理使用 8 张 NVIDIA H200 GPU，tensor parallel size 为 2。RULER 每个任务在每个上下文长度上评测 64 个样本。每个模型只训练一次，每个评测样本对每种方法也只运行一次，因此论文没有通过多次独立训练或重复采样报告方差和置信区间。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Qwen2.5-7B HQA 最大轮数预算：比较 $K=1$、$K=3$ 与 $K=5$，上下文长度覆盖 7K 至 $3.6$M tokens。 | $K=1$ 在所有列都低于对应的 $K=3$ 得分，例如 7K 上由 73.44 提升至 82.81，$3.6$M 上由 70.31 提升至 81.25；但从 $K=3$ 增至 $K=5$ 没有一致提升。$K=5$ 时 75.94% 的样本在两轮后退出，只有 4.84% 使用四轮或五轮。 | 该实验隔离了“迭代”本身的作用。$K=1$ 时所有块只能依据初始空记忆读取，某一块发现的线索无法反向指导其他块；$K=3$ 的稳定优势因此支持跨轮证据交换。$K=5$ 没有持续获益且多数样本提前停止，说明自适应退出避免了为简单样本支付全部轮数成本。不过不同 $K$ 下结果仍是单次评测，部分小幅波动不宜解释为显著差异。 | Table 8 and Section 3.1, Maximum Turn Budget<br><span class="experiment-evidence">Increasing the budget from K=3 to K=5, however, does not yield consistent further gains because most samples converge early: under K=5, 75.94% of samples exit after two turns, whereas only 4.84% use four or five turns.</span> |
| 训练自由的 Qwen3.5-35B-A3B HQA 消融：固定记忆为 4K tokens 时将块大小从 5K 改为 15K 或 25K；固定块大小为 15K tokens 时将记忆大小从 2K 改为 4K 或 8K。 | 作者报告，在块大小 5K–25K tokens、记忆大小 2K–8K tokens 的测试范围内，性能没有随某一尺寸变化而在所有上下文长度上一致下降；默认配置为 15K-token 块和 4K-token 记忆。 | 该实验分别隔离输入分块粒度与共享记忆容量，检验主结果是否依赖某个偶然的超参数点。不同长度上最优配置会变化，因此结论应理解为“测试区间内总体稳健”，而不是默认 15K/4K 始终最佳，也不是尺寸完全不影响单个长度上的得分。 | Table 9 and Section 3.2, Chunk and Memory Sizes<br><span class="experiment-evidence">Table 9 shows no consistent degradation across context lengths when the chunk size varies from 5K to 25K or the memory size varies from 2K to 8K.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出并行迭代记忆机制，同时提升超长上下文多跳推理的准确率与推理效率。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`fdf04cdf96c704df914d68afa71cd0ac41a763c573ad174c3023f77c25952e55`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
