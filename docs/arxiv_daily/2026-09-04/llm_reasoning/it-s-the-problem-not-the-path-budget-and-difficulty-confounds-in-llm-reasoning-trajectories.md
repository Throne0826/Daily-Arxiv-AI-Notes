---
title: "[论文解读] It's the Problem, Not the Path: Budget and Difficulty Confounds in LLM Reasoning Trajectories"
description: "[arXiv 2609.03436][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2609.03436"
announcement_date: "2026-09-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:37:02.941514+00:00"
source_sha256: "170c64021b5a4f3c5e76fb0228829aeafbe2d028e4fcd8cfbf4084bce381f6be"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型推理轨迹"
  - "测试时计算"
  - "截断—续写探针"
  - "重启控制"
  - "计算预算混淆"
  - "题目难度混淆"
  - "早期正确性预测"
  - "题目内评估"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2609.03436</p>

# It's the Problem, Not the Path: Budget and Difficulty Confounds in LLM Reasoning Trajectories

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Yigit Utku Bulut</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Johannes Kepler University Linz</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03436v1) · [PDF 下载](https://arxiv.org/pdf/2609.03436v1) · **关键词** 大语言模型推理轨迹, 测试时计算, 截断—续写探针, 重启控制, 计算预算混淆, 题目难度混淆, 早期正确性预测, 题目内评估<br>
**代码**: [https://github.com/bulutyigit/problem-not-path](https://github.com/bulutyigit/problem-not-path) · **项目页**: [https://github.com/bulutyigit/problem-not-path](https://github.com/bulutyigit/problem-not-path)

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

本文位于大语言模型推理轨迹分析、测试时计算与可解释性研究的交叉领域。研究对象是模型生成的逐步推理文本及其内部信号，核心问题有两类：一是推理过程中是否存在真正使后续求解能力跃升的“突破时刻”，二是生成早期的内部状态是否已经包含该次尝试最终正确与否的信息。要回答这些问题，不能只观察同一条轨迹随生成长度增加的表现，还必须设置与主张相匹配的反事实控制：对“突破”应比较继续当前前缀与在相同总生成预算下从头重启；对“早期可预测性”应排除模型仅仅识别出题目难度的影响，并进行题目内比较。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**推理轨迹与截断—续写探针**

推理轨迹是模型从题目到答案生成的连续文本。截断—续写探针在位置 $t$ 截断已有前缀，再多次采样后续文本，用后续解题成功率估计该前缀在不同时间点的价值。

</div>
<div class="concept-item" markdown="1">

**反事实重启控制与计算预算**

重启控制不使用已有前缀，而是让模型从题目重新生成，并把从头生成与继续生成的总 token 数控制在相同范围内。这样可以区分“前缀确实提供了额外信息”和“只是剩余预算终于足够完成解题”。

</div>
<div class="concept-item" markdown="1">

**AUROC与题目内评估**

AUROC衡量一个预测分数区分正确与错误样本的排序能力，数值为 $0.5$ 时接近随机。跨题目汇总的高 AUROC 可能只反映不同题目的难度差异，因此题目内评估要求在同一道题的不同生成尝试之间进行比较，以检验信号是否真正反映当前尝试的状态。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文研究两个相互关联但需要不同控制的问题。对于突破时刻问题，输入是题目、模型生成的推理轨迹及其截断位置 $t$，输出是各位置继续生成后的解题成功率，并与从同一题目重新开始、在匹配总生成 token 预算下得到的成功率曲线比较；研究假设是，若前缀本身具有不可由新计算替代的价值，则继续前缀应相对于匹配预算的重启表现出稳定优势。对于早期预测问题，输入是生成早期窗口中的模型内部信号以及题目本身，输出是对该次生成最终正确性的预测；评估必须与仅使用题目的难度基线比较，并优先采用题目内分析。实验设置包括 $89$ 道 MATH 题目与两个小型开放权重模型构成的 $178$ 个题目—模型单元，模型以 thinking mode 生成最多 $16K$ token 的轨迹；另使用公开推理模型语料进行无需重新生成的规模化检验。本文结论范围限定于所测试的模型、题目和信号位置，并不假设其他规模、领域或中间答案位置必然具有相同结果。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\hat{p}(t)$**

在轨迹位置 $t$ 截断并继续生成时的估计解题成功率，即多个续写尝试中最终得到正确答案的比例。

</div>
<div class="notation-item" markdown="1">

**$R(C)$**

从题目重新开始、总生成 token 预算为 $C$ 时的解题成功率曲线，用于表示新计算本身随预算增加带来的收益。

</div>
<div class="notation-item" markdown="1">

**$T_F$**

预算适配时间，即继续生成后的剩余工作首次开始适合当前可用预算的时间尺度；它对应“只是终于有足够预算完成”的效应。

</div>
<div class="notation-item" markdown="1">

**$T_V$**

前缀价值时间，即已有推理前缀相对于匹配预算的从头重启首次产生不可由新计算替代的优势的时间尺度。

</div>

</div>

**直接相关的工作**

- **截断—重采样式推理轨迹探针**: 既有做法在位置 $t$ 截断轨迹并采样续写，把后续成功率的上升解释为“突破时刻”。本文指出这种设计同时受到剩余预算的影响，并补充匹配总生成预算的从头重启曲线，以区分前缀价值与预算足够。
- **基于隐藏状态的早期正确性预测**: 已有研究报告从推理早期隐藏状态预测最终正确性的 AUROC 约为 $0.79$–$0.95$，甚至可从前四个 token 开始预测。本文认为跨题目评估可能利用了题目难度，因而加入题目-only难度基线与题目内评估，检验早期信号是否包含超出难度的信息。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文采用两条互补的实证管线，分别检验“推理轨迹中途是否产生不可由额外计算替代的突破”以及“早期内部状态是否包含超越题目难度的单次尝试结果信息”。第一条管线先在模型自身轨迹的多个位置截断并续写，得到固定续写预算下的成功率；再以相同总生成 token 预算从头重启，构造反事实对照。这样可将“答案现在能在剩余预算内写完”与“此前前缀真正缩小了搜索空间”区分开，并据此把问题—模型单元分类为即时、预算受限、前缀受限、无交叉、终端或未解决。
第二条管线比较仅使用生成前题目信息的难度基线，与额外加入前 $512$ 个 token 动态特征的预测器；只有增量 $\Delta$AUROC 的按问题聚类置信区间排除零，才认定早期信号提供了额外信息。论文进一步利用同一题目的大量重复采样，将 pooled AUROC 分解为题内与题间成分：题间成分主要反映问题难度，题内成分才回答“同一道题的这一次生成是否已经显露成败”。直观地说，作者不仅问“沿这条路继续是否容易成功”，还问“把已经消耗的计算预算交给一条全新路线，是否同样能成功”；预测部分则要求模型在同一道题的多次尝试之间辨别成败，而不能只靠识别哪道题更容易。”

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建难度定向、结果盲的轨迹队列

在观察探针结果之前，按中等难度筛选并冻结开发、补充和扩展队列，共得到 $89$ 道题、$178$ 个问题—模型单元；每个单元生成一条最多 $16{,}384$ 个推理 token 的基础轨迹，并记录逐 token logits 与末层隐藏状态。另预先划分 $54/18/17$ 个训练、验证和测试问题，测试集只在确认性预测实验中使用一次。

<div class="method-step__io" markdown="1">

**输入**：MATH 基准中的候选题目，以及 Gemma-4 E4B 和推理微调模型 Ministral-3 3B。<br>
**输出**：带完整 token 级仪器信息的基础轨迹，以及固定的问题级研究划分。

</div>

**直观理解**：作者先寻找“有时能做对、有时会失败”的题，因为在始终正确或始终错误的题上谈中途突破没有意义。筛选不读取后续探针结论，可减少为了获得理想结果而挑题的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 截断续写并估计预算适配时间

在锚点 $t$ 截断模型自己的轨迹，从该前缀以确定性分支种子采样 $m=4$ 条续写，并以正确分支比例估计 $\hat p(t;B)$。首个满足 $\hat p(t;B)\geq\tau$、且下一锚点仍满足阈值的稳定交叉被定义为预算适配时间 $T_F(B)$，其中主阈值为 $\tau=0.75$；交叉区间通过二分细化，未交叉轨迹按右删失处理。

<div class="method-step__io" markdown="1">

**输入**：每个单元的基础轨迹、从 $16$ 到 $8{,}192$ token 的对数间隔锚点、续写预算 $B=1{,}024$ 和额外 $512$ token 答案保留区。<br>
**输出**：每个问题—模型单元的锚点成功率曲线、稳定交叉区间及 $T_F(B)$。

</div>

**直观理解**：$T_F(B)$ 只表示从某个位置开始，剩余工作能塞进固定续写预算；它并不自动证明前面的文字含有不可替代的关键发现。就像考试做到某一步后能在十分钟内收尾，可能只是因为剩余题量变少，而不是那一步突然产生了新洞见。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 从头重启并进行匹配预算反事实比较

每个预算从头独立生成四次，得到重启成功率 $\hat R(C)$，并在网格点间按对数预算线性插值；将前缀续写的总生成量 $t+B$ 与从头计算预算匹配，通过 $\mathrm{adv}(t)=\hat p(t;B)-\hat R(t+B)$ 测量前缀优势。最早同时稳定满足 $\hat p(t;B)\geq\tau$ 与 $\mathrm{adv}(t)\geq\delta$ 的锚点定义为 $T_V(\delta)$，主分析取 $\delta=0.5$，并报告 $0.25$、$0.75$ 与保守重启包络敏感性分析。

<div class="method-step__io" markdown="1">

**输入**：同一题目提示、空前缀，以及 $C\in\{1{,}024,2{,}048,4{,}096,8{,}192\}$ 的重启预算网格。<br>
**输出**：每个锚点的匹配预算前缀优势、前缀价值时间 $T_V$，以及按冻结优先级得到的单元类别。

</div>

**直观理解**：如果保留旧推理比把相同 token 预算用于全新尝试明显更好，才有证据说旧前缀携带了独特价值；若重启也能达到相同成功率，长前缀主要是在压缩后续所需计算，而非打开原本无法到达的答案。该比较只匹配生成 token，不等同于匹配 FLOPs、延迟或缓存成本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 加固离散成功率并冻结判定规则

对末端达到阈值但无法验证稳定性的轨迹追加四个分支，仅当合并结果至少为 $6/8$ 时记录 terminal 事件；扩展队列中的模糊单元统一扩充到八次尝试后再分类。分类按 instant、budget-limited、prefix-limited、no-crossing、terminal、unsolved 的冻结优先级执行，所有规则、功效门槛和修订均在查看其所管辖结果前提交。

<div class="method-step__io" markdown="1">

**输入**：每锚点四分支的成功计数、末端缺少下一稳定锚点的候选事件，以及成功数为 $1$ 至 $3$ 的模糊单元。<br>
**输出**：对小样本二项噪声更稳健的事件标签与可审计的确认性分析协议。

</div>

**直观理解**：四次采样中出现三次成功并不罕见，即使真实成功概率只有一半，因此不能把一次 $3/4$ 直接当成稳定突破。追加采样和预先冻结规则用于防止随机波动或事后改标准把普通单元误判为前缀受限。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 匹配总 token 预算的前缀优势

$$
\operatorname{adv}(t)=\hat p(t;B)-\hat R(t+B)
$$

**符号说明**

- $t$：基础推理轨迹被截断的锚点位置，以已生成 token 数计。
- $B$：截断后允许生成的固定推理续写预算；主实验取 1,024 token。
- $\hat p(t;B)$：保留截至锚点的模型自身前缀后，在给定续写预算内得到正确答案的经验成功率。
- $\hat R(C)$：从空前缀、同一问题提示开始，在总预算为 C 时的经验重启成功率；网格之间采用对数线性插值。
- $\operatorname{adv}(t)$：保留前缀相对于使用相同总生成 token 预算从头重启的成功率增益。

<div class="equation-explanation" markdown="1">

**直观理解**：式子将“先生成 $t$ 个 token 再续写 $B$ 个 token”与“直接用 $t+B$ 个 token 从头尝试”放在同一生成预算上。正优势说明旧前缀优于新计算，但论文以较大的主阈值 $\delta=0.5$ 和稳定交叉作为前缀受限证据，以减少采样噪声造成的误判。<br>
**原文位置**：Section 2.3, Restart control and the prefix-value time $T_V$

</div>

</div>

<div class="equation-block" markdown="1">

#### 总体 AUROC 的题内—题间分解

$$
\mathrm{AUROC}_{\mathrm{pooled}}(S)=\lambda\,\mathrm{AUROC}_{\mathrm{within}}(S)+(1-\lambda)\,\mathrm{AUROC}_{\mathrm{between}}(S)
$$

**符号说明**

- $S$：预测每次尝试成功可能性的评分函数。
- $\mathrm{AUROC}_{\mathrm{pooled}}$：将所有问题与尝试合并后，对成功—失败样本对计算的总体排序能力。
- $\mathrm{AUROC}_{\mathrm{within}}$：仅比较来自同一问题—模型单元的成功与失败尝试所得的 AUROC。
- $\mathrm{AUROC}_{\mathrm{between}}$：比较来自不同问题—模型单元的异类结果对所得的 AUROC，容易受到题目难度差异驱动。
- $\lambda$：所有成功—失败异类样本对中，来自同一问题—模型单元的比例。

<div class="equation-explanation" markdown="1">

**直观理解**：总体 AUROC 是题内辨别与题间难度排序的加权平均。任何只依赖题目的评分在同一道题内都为常数，因此其题内 AUROC 必为 $1/2$；若每题只有一次生成，则 $\lambda=0$，总体 AUROC 完全无法检验单次轨迹是否含有成败信息。<br>
**原文位置**：Equation (1), Section 4.2

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文不提出或训练新的推理语言模型，也没有用于改变生成模型参数的优化目标。确认性预测部分拟合逻辑回归分类器，其目的只是比较题目难度特征与“难度加早期轨迹特征”的预测增量；判定目标不是训练损失是否下降，而是 held-out 测试集上配对 $\Delta$AUROC 的问题聚类 $95\%$ 置信区间是否排除零。公共 R1-Distill-Qwen-7B 分析通过 teacher forcing 将已有轨迹重新送入对应的 4-bit 模型以提取隐藏状态，不进行生成模型微调；问题中心化探针和逐题 oracle 均被明确标为事后诊断，而非确认性训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 重启控制的截断探针**

模块同时估计固定续写预算下的 $\hat p(t;B)$ 与从空前缀开始的预算—成功率曲线 $\hat R(C)$，并在相同总生成 token 数 $t+B$ 下计算前缀优势。$T_F$ 衡量解何时适合剩余预算，$T_V$ 则额外要求前缀相对重启具有至少 $\delta$ 的稳定优势。

> 直观理解：普通截断实验缺少“如果不用这段前缀会怎样”的对照，因此容易把任务接近完成误读为推理突破。重启曲线补上这一反事实，使“节省计算”与“扩大可解范围”成为可区分的解释。

**2. 噪声加固与冻结分类器**

由于每个预算点通常只有四次尝试，模块对末端候选和模糊单元追加采样，并要求跨相邻锚点稳定；随后按固定优先级赋予 instant、budget-limited、prefix-limited、no-crossing、terminal 或 unsolved 标签。budget-limited 的核心条件是 $\hat R(4{,}096)\geq\tau$，说明足够长的独立重启已可解决该题。

> 直观理解：该模块不提高模型能力，而是提高测量可信度。它避免把一次幸运续写、末端无法复核的交叉，或本来可由更大重启预算解决的问题称为真正突破。

**3. 难度基线与题内 AUROC 评估**

问题基线仅含生成前可知变量：人工难度级别、主题、字符数、空白分词数、数字、运算符和方程 token 计数，以及模型身份；增强模型再加入熵、surprisal、连续分布散度、隐藏状态几何和谱摘要等十五组早期特征。公共重复采样数据允许直接估计 $\mathrm{AUROC}_{\mathrm{within}}$；只有单轨迹每题的数据则必须依靠相对于显式问题基线的增量价值。

> 直观理解：难题更容易失败，因此任何能识别题目的表示都可能获得很高的总体 AUROC。显式难度基线回答“只看题目能预测到什么程度”，题内 AUROC 则进一步删除题目难度这条捷径。

**训练与推理**

生成阶段，两种本地 4-bit 模型以 thinking mode 对每题产生一条最长 $16{,}384$ token 的基础轨迹；随后在预定锚点恢复该前缀并执行固定预算分支采样，同时从空前缀按四档预算独立重启。答案按二元正确性评分，锚点曲线经稳定性检查、必要的追加采样和重启插值后计算 $T_F$、前缀优势与 $T_V$，最后按冻结规则分类。
预测阶段先在问题级互斥的训练与验证折上选择或拟合逻辑回归，再一次性评估测试问题。基础模型只能访问生成前信息，增强模型额外访问早期窗口统计；两者的 AUROC 差异使用按问题聚类的方法估计置信区间。公共数据分析不再生成文本：DeepSeek-R1 与 GPQA 数据直接由同题其他尝试估计难度；R1-Distill-Qwen-7B 轨迹则通过 teacher forcing 重建早期隐藏状态，并在固定 pooled 子集和具有足够成败变异的同题重复样本上分别评估。

**复现信息**

核心生成模型为 `google/gemma-4-E4B-it` 与 `mistralai/Ministral-3-3B-Reasoning-2512` 的 `mlx-community` 4-bit 转换版本；作者本地运行并记录逐 token logits 与末层隐藏状态。截断探针主设定为每锚点 $m=4$ 条续写、$B=1{,}024$ 个推理 token 加 $512$ 个答案保留 token，锚点从 $16$ 到 $8{,}192$ token 对数分布；重启预算为 $1{,}024$、$2{,}048$、$4{,}096$ 和 $8{,}192$ token，每档四次。预算匹配只按生成 token 数进行，未测量 FLOPs、墙钟延迟或 KV-cache 复用，因此结论应解释为 token 预算下的计算压缩或可达性，而非硬件成本等价。
早期预测窗口的主设定覆盖前 $512$ 个 token，动态特征包括熵、surprisal、连续分布散度、隐藏状态几何和谱摘要；测试判定采用问题聚类的 $95\%$ 置信区间及预注册功效门槛。公共 R1-Distill-Qwen-7B 重建使用每题 $256$ 条现有样本，并以 4-bit 模型 teacher forcing 提取状态；文中报告该重放过程的 top-1 fidelity，但这种近似仍意味着隐藏状态分析依赖量化模型对原生成轨迹的重建质量。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 主要受控队列包含 89 道 MATH 数学题与两个小型开放模型 Ministral-3、Gemma-4 形成的 178 个“题目—模型”单元。题目选择不使用单次生成结果，但针对难度进行设计。该队列同时用于重启控制的截断实验和预注册的早期信号检验；后者只在冻结分析方案后对留出测试集评估一次。
- 大规模公开 DeepSeek-R1 语料包含 91,573 道题上的 192,315 次生成。它不用于训练本文的受控推理实验，而用于检验：完全不读取推理轨迹、只利用同题其他尝试结果构造的难度代理，是否也能达到文献中内部状态探针常见的汇总 AUROC。
- 开发队列用于形成并检查“预算受限、即时、终末、无交叉、未解决、前缀受限”等分类规则。文中举例说明 Ministral-3 上看似清晰的中途突破，在把 continuation 预算提高到 4,096 token 后可从仅含 16 token 的前缀解出，因此该部分主要承担发现预算混淆并冻结后续分类方案的角色，而不是最终确认性检验。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**锚点 continuation solve rate 与匹配预算 restart solve rate**

前者测量从某个已有推理前缀继续生成时的成功概率，后者测量在相同总生成 token 预算下从零开始的成功概率。两者的关系用于区分“答案只是终于能放进预算”与“前缀携带了新计算无法购买的信息”，并据此将题目—模型单元归类。 （不存在统一的越高越好方向；核心看继续前缀是否在匹配预算下稳定优于重启，以及该差异是否足以支持前缀受限而非预算受限的解释。）

</div>
<div class="metric-item" markdown="1">

**AUROC**

衡量预测分数将一次成功尝试排在一次失败尝试之前的概率，平分时计一半。汇总 AUROC 混合了同一题内部的排序与不同题之间的排序，因此可能仅反映题目难度；同题内部 AUROC 才更直接检验单次尝试信息，题目固定分数在同题内理论上为 $0.5$。 （通常越高表示排序能力越强，但只有在明确控制题目难度或进行同题内评估时，较高值才能支持存在单次轨迹信息。）

</div>
<div class="metric-item" markdown="1">

**配对 $\Delta$AUROC 及题目聚类 95% 置信区间**

定义为加入早期窗口动态后的 AUROC 减去题目-only 基线 AUROC，并按题目聚类估计不确定性。预注册成功标准要求其 95% 置信区间排除零，以避免把题目难度已能解释的预测力误当成早期轨迹信号。 （正值越大越支持早期动态具有增量价值；但只有置信区间排除零才满足本文的确认性标准。区间跨零表示未检测到增益，不等同于已经证明两种模型完全等效。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 178 个 MATH 题目—模型单元上的重启控制截断实验

<div class="result-value" markdown="1">

作者报告，178 个单元中只有 1 个最终被判为真正的“前缀受限”；在匹配预算落入可观测重启网格的 9 个单元中，继续模型自身前缀全部优于从零重启，即 9/9。整体证据更符合前缀压缩后续所需计算，而不是前缀让原本不可解的问题变得可解。

</div>

若一个表面突破只在剩余预算足够写完解答时出现，那么它不是认知能力突然产生，而是长度限制的产物。只有当已有前缀在相同总计算预算下仍提供从零重启买不到的优势，才可称为前缀携带独特价值。这里 1/178 表明强意义的“突破点”极少；9/9 则说明已有前缀通常有用，但这种用处主要是节省或压缩计算。该结果不证明所有更大模型、任务或搜索策略中都没有真正突破。

<div class="result-source" markdown="1">

来源：Abstract；对应 Results I 与 Figure 1 的总体结论

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Applied to 178 problem-model cells (89 MATH problems x two small open models, an outcome-blind but difficulty-targeted cohort), exactly 1 of 178 cells survives as prefix-limited; restart dose-response separates a compute-starved model from a capability-limited one; and wherever the matched budget lies inside the restart grid, continuing the model's own prefix beats restarting (9 of 9) -- predominantly compute compression rather than expanded reachability.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 预注册、难度控制的留出测试：题目-only 基线对比题目基线加前 512 token 早期动态

<div class="result-value" markdown="1">

主要终点的 AUROC 从 0.83 增至 0.85，配对 $\Delta=+0.026$，95% 置信区间为 $[-0.054,+0.167]$；次要终点从 0.88 降至 0.78，$\Delta=-0.090$，区间为 $[-0.213,+0.033]$。两个区间都跨越零，均未达到预注册的“检测到增量信息”标准。

</div>

题目本身已经提供很强的成功率线索。加入早期内部动态后，主要终点只有小幅点估计提升，次要终点反而下降，而且不确定区间均包含无变化。因此作者能够主张的是“本实验没有检测到超越难度基线的早期信号”，而不是“早期信号必定不存在”。尤其主要终点区间上界仍为 $+0.167$，尚不能排除中等大小的真实效应。

<div class="result-source" markdown="1">

来源：Section 4.1；Figure 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Primary: baseline AUROC 0.83 versus 0.85 with early signals, Δ=+0.026 [-0.054,+0.167]. Secondary: baseline 0.88 versus 0.78, Δ=-0.090 [-0.213,+0.033] — the point estimate is negative, consistent with uninformative added features.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 192,315 次 DeepSeek-R1 公开生成上的无轨迹难度代理分析

<div class="result-value" markdown="1">

只使用同题其他尝试结果的留一法通过率、不读取当前轨迹或题面的难度代理，取得 AUROC 0.873，题目聚类 bootstrap 95% 置信区间为 $[0.870,0.876]$。该值落在相关内部状态探针论文所报告的 0.79–0.95 区间内。

</div>

一个完全不知道当前尝试如何推理的预测器，只要能识别哪些题通常容易、哪些题通常困难，就能获得看似很高的汇总 AUROC。因此，跨题汇总得分不能单独证明模型的早期状态已经透露本次尝试的命运。该分析揭示的是评价设计的可识别性问题，并不表明留一法代理在同题内部具有真正预测力；文中还指出它在同题内部会机械地把失败尝试排在成功尝试之前。

<div class="result-source" markdown="1">

来源：Section 4.3；Figure 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On 192,315 DeepSeek-R1 generations over 91,573 problems [19], a trace-blind difficulty proxy — the leave-one-out pass rate of the problem’s other attempts, for 92% of problems a single binary observation, reading neither the trace nor the question — achieves AUROC 0.873 [0.870,0.876] (problem-clustered bootstrap; estimator frozen before evaluation, and likely conservative, since dataset curation truncates the difficulty range).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 确认性队列只有 89 道 MATH 题、两个小型开放模型和 178 个题目—模型单元，部分按模型拆分的测试样本仅为 11 或 16。主要 $\Delta$AUROC 区间仍较宽，其上界未排除中等正效应；论文明确将结论表述为“未检测到增益”，而非早期信息不存在或两种特征集等效。
- 题目-only 基线仅使用文本层面的人工难度、主题与表面统计，作者指出生成前激活探针可能构成更强基线。公开语料中的留一法通过率也不是真正固定的题目-only 分数，并会在同题内部产生机械反向排序；因此它适合揭示汇总 AUROC 的难度混淆，却不应被当作可部署的单次尝试预测器。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 匹配总 token 预算的从零重启曲线：对每个截断锚点，不仅测量继续原轨迹前缀的成功率，还测量模型在相同总生成预算下重新开始的成功率。它是判断前缀是否具有不可由新增计算替代之价值的关键反事实；若继续前缀仅因拥有更多剩余 token 而获益，重启控制会暴露这一点。
- 题目-only 难度基线：输入包括人工难度等级、主题类别、题面字符数、空白分词数、数字 token 数、运算符 token 数、等式 token 数以及模型身份，完全不读取当前运行生成后的信息。它检验早期动态是否提供超过题目先验难度的增量信息，而非仅区分容易题和困难题。
- 题目-only 基线加 15 个冻结的早期窗口动态摘要：摘要来自前 512 token，包括熵、惊讶度、相邻分布差异、隐藏状态几何和谱统计等，并使用与题目-only 基线相同的逻辑回归与交叉验证协议。两者 AUROC 的配对差值直接对应论文的核心早期信号主张。
- 留一法通过率难度代理 $\hat{d}_{c,j}$：对单元 $c$ 的第 $j$ 次尝试，用同题其他尝试的正确比例估计该题成功概率，但不使用第 $j$ 次尝试自身的结果，也不读取其题面或轨迹。它是一个可扩展的难度上限参照，用来证明高汇总 AUROC 本身不能归因于单次轨迹信息；不过它并非严格的题目-only 分数，因为其值会随被留出的尝试而变化。

**实验想回答的问题**

- 所谓推理轨迹中的“突破点”究竟表示前缀已经积累了从零重启无法替代的信息，还是仅仅表示剩余生成预算终于足以容纳完整解答？实验通过在相同总生成 token 预算下比较“继续已有前缀”和“从头重启”的解题率来构造反事实控制。
- 模型在前若干 token 中的熵、惊讶度、隐藏状态几何等内部动态，能否在题目本身所决定的难度之外，继续预测单次作答最终是否成功？实验分别检验相对于题目难度基线的增量预测价值，以及汇总 AUROC 是否可能主要来自题目间难度差异。

**实验实现**

突破实验在多个轨迹截断锚点上估计 continuation 成功率，并将其与匹配总生成 token 预算的从零重启剂量—反应曲线比较；分析单位是题目—模型单元，而不是把所有轨迹无条件汇总。早期信号实验在查看测试结果前冻结两个终点：主要终点为 16K 运行最终是否成功，次要终点为非即时单元在 4,096 token 从零重启时是否达到预设成功阈值。模型使用逻辑回归，在训练集与验证集上按题目分组交叉验证，并设置每类样本量的统计功效门槛；留出测试集只评估一次。主要特征窗口为前 512 token，确认性判断依据配对 $\Delta$AUROC 的题目聚类 95% 置信区间是否排除零。另有明确标为事后的预测时点扫描，以及在公开语料上的生成-free 难度分析；这些属于稳健性或混淆诊断，不能替代预注册主检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 按模型拆分题目难度基线的预测表现 | Gemma-4 上题目难度基线对两个终点的测试 AUROC 都为 1.0，对应样本量分别为 $n=16$ 和 $n=11$；Ministral-3 上仅为 0.69–0.73。 | 该拆分隔离了模型能力形态对混淆强度的影响。对能力受限的 Gemma-4，哪些题能成功几乎可由题目本身完全区分，早期动态没有多少剩余方差可解释；对预算更有弹性的 Ministral-3，题目难度基线较弱，但残余波动也未被早期动态可靠解释。由于拆分后的样本很小，尤其 Gemma-4 的 AUROC 1.0 不应被理解为可泛化的完美预测器。 | Section 4.1；Figure 5 后的 per-model split<br><span class="experiment-evidence">Why the null has this shape is visible in the per-model split: the difficulty baseline alone is near-perfect for Gemma-4 (test AUROC 1.0 on both endpoints, n=16 and 11) and mediocre for Ministral-3 (0.69–0.73).</span> |
| 事后改变早期预测窗口至 $t\in{128,256,1024,2048}$ | 10 个点估计中有 8 个为负，所有置信区间均跨越零；因此没有任何被测试窗口显示可检测的增量收益。 | 该敏感性分析检验主结论是否只是选择前 512 token 作为预测窗口造成的。多个更早或更晚时点仍未出现稳定正增益，说明零结果并非明显依赖单一窗口选择。不过这是事后分析，而且各区间统计功效不足，只能作为稳健性证据，不能证明所有可能窗口的真实效应均为零。 | Section 4.1；Figure 6<br><span class="experiment-evidence">A post-hoc sweep of the forecast point over t∈{128,256,1,024,2,048} — labeled post-hoc in the amendment — found 8 of 10 point estimates negative and every CI straddling zero (Figure 6): no tested alternative window yields a detectable gain, though these post-hoc intervals are individually underpowered.</span> |

**定性案例**

- Ministral-3 的开发队列曾出现外观清晰的中途交叉，但把 continuation 预算提高到 4,096 token 后，仅保留 16 token 的前缀也能解出同一问题。这一案例直观展示了预算混淆：原先标记的“突破”对应的是完整解答开始能够装入剩余预算，而非前缀在该位置突然获得决定性知识。它说明仅观察单条轨迹从失败变成功的截断曲线不足以定位认知事件，必须加入匹配预算的从零重启曲线。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作通过受控实验分析 LLM 推理轨迹、计算预算、难度混淆与早期可预测性。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`170c64021b5a4f3c5e76fb0228829aeafbe2d028e4fcd8cfbf4084bce381f6be`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
