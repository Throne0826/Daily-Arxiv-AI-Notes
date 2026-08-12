---
title: "[论文解读] Long-Horizon AI Research for Grothendieck Constant: A Case Study in Human-AI Mathematical Collaboration"
description: "[arXiv 2608.11195][LLM Agent] 本文以长期未决的 Grothendieck 常数 $K_G$ 边界改进为案例，研究如何让受人类异步引导、具备持久记忆与内部验证机制的 AI 系统参与目标会演化、反馈稀疏且需要长期积累的数学研究。"
arxiv_id: "2608.11195"
announcement_date: "2026-08-12"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:09:45.693403+00:00"
source_sha256: "66e8fb7a4238f2a3dd3ac9dc350f4e11bb0fc29d8f860f0b3ce912760d7e5b1c"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "AI 辅助数学研究"
  - "长程研究"
  - "Grothendieck 常数"
  - "组合优化"
  - "连续松弛"
  - "舍入算法"
  - "人机协作"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.11195</p>

# Long-Horizon AI Research for Grothendieck Constant: A Case Study in Human-AI Mathematical Collaboration

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Alan Li, Rahul Saha, Anton Xue, Swarat Chaudhuri, Adam Klivans, Pravesh K Kothari, Raghu Meka</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Long-Horizon AI Research for Grothendieck Constant</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11195v1) · [PDF 下载](https://arxiv.org/pdf/2608.11195v1) · **关键词** AI 辅助数学研究, 长程研究, Grothendieck 常数, 组合优化, 连续松弛, 舍入算法, 人机协作<br>


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

本文以长期未决的 Grothendieck 常数 $K_G$ 边界改进为案例，研究如何让受人类异步引导、具备持久记忆与内部验证机制的 AI 系统参与目标会演化、反馈稀疏且需要长期积累的数学研究。

**不用术语来说**：现有 AI 已能解决题目明确、答案可核验的数学问题，但真正的数学研究并不会预先给出一条清晰路线：研究者既要选择值得证明的命题，也要记住失败尝试、判断中间发现是否重要，并在很久以后才获得成功信号。论文选择自 1953 年以来精确值仍未知的 Grothendieck 常数 $K_G$ 作为压力测试，考察 AI 能否不只完成局部推导，还能在持续探索中产生经领域专家判断为新颖的关键思路。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者给出一个长周期人机协作案例：AI 研究系统在人工异步引导下参与研究计划的推进，其关键数学思路帮助同时收紧 $K_G$ 的上界与下界；定理均由作者独立核验，完整证明置于配套论文。
- 作者将运行过程作为方法学对象，记录推理模型与编码代理的分工、基于文件的持久记忆、校准后的内部验证协议及人工引导通道，并据完整记录分析系统在技术执行、研究判断和研究状态维护方面的能力差异。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于“AI 辅助数学研究”与组合优化交叉领域，关注的不是让模型解决一个预先形式化、可自动判分的题目，而是让 AI 在长期研究过程中参与选择下一步问题、记录失败原因、提出新猜想并协助验证。案例所研究的 Grothendieck 常数 $K_G$ 衡量一类困难的离散组合优化问题与其可高效处理的连续松弛之间最坏情况下的差距；其精确值自 1953 年以来仍未知。论文报告的人机协作同时改进了 $K_G$ 的上下界，但完整数学证明置于配套论文中；本文主要用于说明研究系统如何支持这种目标会演化、反馈稀疏且验证周期较长的数学工作。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**连续松弛**

把取值受限的离散优化问题扩展为可在连续空间中求解的问题，以获得更容易计算的近似解。$K_G$ 可理解为相关离散最优值与连续松弛最优值之间最坏差距的统一控制常数。

</div>
<div class="concept-item" markdown="1">

**舍入算法**

将连续松弛所得的向量或实数解转换为满足原离散约束的解。本文提到的上界来自一种新的舍入算法渐近分析框架，并引入扩大既有算法空间的 limiting Krivine schemes。

</div>
<div class="concept-item" markdown="1">

**长程 AI 数学研究**

指目标可能随探索而改变、有效反馈稀疏且成果要经过多轮尝试才能显现的研究过程。它不仅要求技术推导，还要求管理研究状态、判断方向价值、保留失败经验并独立核验结论。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

数学任务是在不预设 $K_G$ 精确值的条件下，寻找可证明的更大下界和更小上界，从而缩窄其可能范围；论文报告的结果为 $\frac{6\pi}{11}\leq K_G\leq\frac{\pi}{2\log(1+\sqrt{2})}-3.47\times10^{-4}$。研究系统的输入包括该开放问题、已有数学知识、运行中积累的文件化研究记录以及人类操作者的异步指导；系统执行文献与思路整理、推导、计算实验、失败分析和候选论证检查，输出新的研究方向与可供作者验证的数学论证。其关键设定是没有固定的自动评分函数或固定形式化命题，AI 可以提出核心步骤，但所有作为定理陈述的结果均由作者独立验证，完整证明由配套论文给出。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$K_G$**

Grothendieck 常数，用于控制相关离散组合优化问题与连续松弛之间的最坏差距。

</div>
<div class="notation-item" markdown="1">

**$\frac{6\pi}{11}$**

本文报告的改进后下界，约为 $1.7135$。

</div>
<div class="notation-item" markdown="1">

**$\frac{\pi}{2\log(1+\sqrt{2})}-3.47\times10^{-4}$**

引言中报告的改进后上界，约为 $1.7818$。

</div>

</div>

**直接相关的工作**

- **FunSearch 与 AlphaEvolve**: 二者代表评估器引导的搜索方法，可探索程序或数学构造空间，但通常要求目标固定且候选结果能够由自动评分函数评价；本文研究的开放式长期数学过程缺少这种持续、明确的反馈信号。
- **AlphaProof**: AlphaProof 借助证明助手获得清晰的正确性反馈，但需要预先固定并形式化待证明命题；本文关注的研究计划还包含选题、调整目标、维护失败记录和形成新陈述，因此问题设置更开放。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

数学研究需要跨越大量失败和延迟反馈来形成新知识，而 AI 应如何在这种长周期任务中被有效组织仍是开放问题。对 $K_G$ 而言，研究目标是进一步缩小已知上下界之间的区间；这不仅要求执行证明或计算，还要求发现新的舍入算法分析框架或新的下界论证路径，因此能够检验 AI 是否具备支持真实前沿研究的能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **由自动评估器引导的搜索**：FunSearch、AlphaEvolve 等系统在预先规定的程序或数学构造空间中生成候选方案，再利用固定目标和自动评分函数反复筛选、改进。其优势是反馈快速且可规模化，但搜索方向和成功标准必须事先明确。
- **固定命题证明与交互式模型辅助**：AlphaProof 一类形式化证明系统依靠证明助手提供明确的正确性信号，但需要预先固定并形式化待证命题；另一类做法是研究者直接与前沿模型交互，让模型提供推导、编程或文献理解等技术协助，而研究议程、长期记忆和结果核验主要由人类承担。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 自动评估器搜索和形式化证明都依赖固定目标以及清晰、即时的正确性信号，难以处理研究中命题选择本身尚未确定、目标随发现而改变且价值只能延迟显现的情形；结果是系统更适合解定义完备的问题，而非持续经营一个研究计划。
- 普通交互式模型虽能提供广泛技术帮助，却把议程设定、失败经验保存、研究状态维护和可靠性核验留给人类；这使模型的局部输出难以自动积累为连贯的新数学，而论文记录还表明 AI 在研究判断及准确维护研究状态方面明显弱于技术执行。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一个经过完整记录的真实前沿案例，能够说明 AI 如何在没有固定自动评分函数、研究方向会演化且奖励稀疏延迟的条件下，持续保留失败原因、决定下一步尝试并把多次失败转化为专家认可的新颖数学；同时也缺少对这种系统应由哪些记忆、验证和人类干预机制支撑的经验分析。

</div>
<div markdown="1"><span>核心问题</span>

一个由人类异步引导并配备持久记忆、技术执行代理和内部验证协议的 AI 系统，能否在 $K_G$ 边界这一长期开放问题上以研究计划而非单次问答的方式工作，产生可由人类独立验证的关键新思路；在此过程中，它的可靠能力边界和必要的人机分工是什么？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把研究过程外化为可持续更新的系统状态：文件记忆保存尝试、失败及其原因，推理模型负责提出和调整方向，编码代理承担计算与技术检验，人工则在关键节点校正价值判断和研究状态。直观地说，突破未必来自一次正确回答，而可能来自对许多失败线索的长期保存与重新组合；这种结构既让 AI 发挥高强度技术执行的优势，也用验证协议和人类判断补偿其容易误判研究价值、遗失上下文或错误估计进展的弱点。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文的方法不是训练一个新的数学模型，而是搭建一个面向长期数学研究的双智能体协作系统，并将其用于 Grothendieck 常数的上下界研究。系统以已有的立方—五次 Krivine 方案、系数公式、认证程序、研究笔记和候选方向为输入；推理智能体负责选择研究方向、提出引理、设计数值实验和审计论证，编码智能体负责维护文件化研究状态、实现计算、检索文献并运行验证。工作被拆成若干有界会话，每个会话依次完成状态读取、方向选择、推理—计算循环和结尾审计；会话之间不保留模型上下文，而以问题说明、汇总文件、追加式记录和实验日志传递研究状态。人类研究者通过异步文本指令设定优先级、检查结论并在方向停滞时实施重构。

在核心下界发现中，系统最初搜索更好的上界方案，却反复观察到同一权衡：压低相关函数逆控制中的高阶非线性项会同时削弱线性主项。人类将这一停滞解释为可能存在普适障碍，并要求系统把构造搜索改写为障碍证明。系统随后把障碍表示为 Krivine 方案相关函数前两个非零系数之间的仿射不等式 $b_3\geq 2b_1-11/6$；该约束在取平均和取极限时仍成立，因而覆盖混合与极限 Krivine 方案。再借助 Naor–Regev 关于这类方案渐近最优的定理，系数障碍被转化为 $K_G\geq 6\pi/11$。直观地说，系统不再继续寻找更好的“舍入地图”，而是证明所有这类地图都受同一道性能上限约束；作者随后独立核验并修订了证明。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 研究状态初始化与会话定向

每个有界会话先读取文件化的活动研究状态，其中包含当前目标、已证明或猜测的命题、数值证据、失败方向、待补证明义务和未决选择；随后选定一个与其他并行会话不同的研究焦点。模型上下文不会跨会话继承，连续性完全依赖这些持久化文件。

<div class="method-step__io" markdown="1">

**输入**：问题说明、立方—五次 Krivine 方案、相关函数系数公式、计算认证工具、既有研究笔记、候选上下界方向，以及前序会话写入的汇总文件和日志。<br>
**输出**：一个范围明确的会话任务，以及执行该任务所需的当前假设、证据和未解决问题。

</div>

**直观理解**：这相当于研究者每次上班先读实验室笔记，再决定本次只处理哪一个问题。文件承担长期记忆，避免把模型一次会话的上下文误当成可靠的永久记忆。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双智能体推理—计算循环

推理智能体选择高层行动，例如提出辅助引理、比较失败构造、寻找反例、重写目标或审计旧结论，并把所需计算或文献任务交给编码智能体；编码智能体实现与运行实验、维护代码仓库、调用脚本接口继续驱动推理，并将结果返回。浮点搜索用于发现候选结构，而需要认证的计算改用区间算术复核，以控制舍入误差。

<div class="method-step__io" markdown="1">

**输入**：当前研究焦点和活动研究状态。<br>
**输出**：候选构造、数值证据、引理、反例、证明草稿、计算证书或对既有结论的否定性审计。

</div>

**直观理解**：一个智能体像负责制定研究策略的数学家，另一个像负责写程序、跑实验和整理材料的研究助手。数值实验先帮助发现规律，严格认证再判断规律能否进入证明。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 由上界构造搜索转向普适障碍

人类操作者判断上界搜索已经进入平台期，并要求系统综合失败案例，而不是继续枚举构造；系统将共同障碍重写为相关函数 $H(t)=b_1t+b_3t^3+\cdots$ 的系数约束，并寻找对任意方案均成立、且在混合和极限操作下保持的不等式。该步骤把存在性构造问题改造成全称量词下的分析证明问题。

<div class="method-step__io" markdown="1">

**输入**：多个极限 Krivine 方案的失败记录，以及“抑制高阶非线性会削弱线性主项”的重复现象。<br>
**输出**：仿射系数障碍 $b_3\geq 2b_1-11/6$，以及将高维分区估计约化为少量一维高斯不等式的证明路线。

</div>

**直观理解**：连续尝试更好的方案都撞上同一限制时，研究目标被改成证明这堵“墙”对所有方案都存在。这样，失败记录不再只是负面结果，而成为下界证明的线索。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 证明认证、会话审计与人类核验

系统通过内部验证协议测试证明义务，并在会话结束时把每项结论标记为已证明、数值支持、猜测或启发式，再合并到汇总文件；对需计算认证的部分，浮点结果由 CPU 上的区间算术重新计算。作者只把额外经过人工独立检查的结论称为定理，并对系统生成的 $K_G\geq 6\pi/11$ 证明进行了修订和复核。

<div class="method-step__io" markdown="1">

**输入**：系数不等式、降维后的一维高斯不等式、计算机辅助证书和证明草稿。<br>
**输出**：经作者核验的下界定理，以及与之分离的、仅通过系统内部协议但尚未完成人工核验的机器验证候选结论。

</div>

**直观理解**：系统必须同时记录“发现了什么”和“证据强到什么程度”，防止把漂亮的数值或未补齐的证明当成定理。最终发表级结论还要经过人类逐项检查。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Krivine 方案的归一化相关函数

$$
H(t):=\frac{\pi}{2}\,\mathbb{E}\bigl[f(X)g(Y)\bigr],\qquad \mathbb{E}[X_iY_i]=t
$$

**符号说明**

- $H(t)$：输入高斯向量的坐标相关度为 $t$ 时，两个舍入标签相关性的归一化函数；它概括一个 Krivine 舍入方案的性能。
- $t$：对应坐标 $X_i$ 与 $Y_i$ 的相关系数，也用于编码原 SDP 向量的内积。
- $X,Y$：$\mathbb{R}^k$ 中的标准高斯随机向量，各对应坐标满足 $\mathbb{E}[X_iY_i]=t$。
- $f,g$：将 $\mathbb{R}^k$ 分成正负区域的奇符号函数，取值属于 $\{\pm1\}$，分别产生两侧的离散标签。
- $k$：Krivine 分区所在高斯空间的维数；极限方案允许它沿经典方案序列增长。
- $\mathbb{E}$：对相关高斯随机变量取期望。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把整个几何舍入过程压缩成一个单变量函数：给定连续向量之间的相关度 $t$，它描述最终正负标签还能保留多少相关性。若 $H$ 接近斜率较大的直线，舍入造成的非线性失真较小；因此研究上界构造和下界障碍都可转化为研究 $H$ 的形状及其幂级数系数。<br>
**原文位置**：第 2 节“The normalized correlation function”

</div>

</div>

<div class="equation-block" markdown="1">

#### 相关函数的普适系数障碍

$$
H(t)=b_1t+b_3t^3+\cdots,\qquad b_3\geq 2b_1-\frac{11}{6}
$$

**符号说明**

- $b_1$：归一化相关函数在原点附近的一次项系数，表示舍入对弱输入相关性的首阶保留能力。
- $b_3$：相关函数的三次项系数，刻画首个关键非线性修正。
- $\cdots$：更高奇次项；由于分区函数为奇函数，相关函数按奇次幂展开。
- $K_G$：所有矩阵上 SDP 最优值与离散双线性优化最优值之比的最坏情形上确界，即 Grothendieck 常数。

<div class="equation-explanation" markdown="1">

**直观理解**：不等式说明线性收益 $b_1$ 与三次非线性 $b_3$ 不能被任意独立调节：试图提高首阶保留能力时，必须付出一定的非线性代价。因为该仿射约束在方案平均和维数极限下仍成立，它不只排除某个具体构造，而是约束整个混合与极限 Krivine 方案族；结合该方案族的渐近最优性，作者据此推出 $K_G\geq 6\pi/11$。<br>
**原文位置**：第 3 节，定理 3.2，公式 (1)；证明发现过程见第 6 节

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。论文没有通过梯度下降、监督数据或强化学习训练专用模型，也没有给出新的参数化训练损失；所用语言模型是现成的前沿模型。系统层面的“优化目标”是推进 Grothendieck 常数的上下界并形成可核验的数学证书，其中上界方向寻找相关函数非线性更小、舍入保证更强的 Krivine 方案，下界方向则证明所有此类方案都必须满足的性能障碍。这个目标通过研究方向选择、程序实验、证明搜索和审计实现，而不是通过更新模型权重实现。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 推理智能体**

使用高推理强度的前沿语言模型，在活动研究状态上选择方向、提出定义与引理、设计计算实验、发展证明并审计结论。其职责对应研究循环中的高层行动选择和数学技术执行，但会话结束后不保留内部上下文。

> 直观理解：它负责决定“下一步值得研究什么”并尝试完成数学推导，但其判断不自动等于可靠证明，因此必须由记录、验证程序和人类审查约束。

**2. 编码与验证智能体**

编码代理维护项目仓库和追加式日志，实现浮点搜索、区间算术认证与其他实验，检索文献，并通过脚本接口向推理模型提交任务和回收结果。计算职责与推理职责分离，使候选发现、复现和证书检查能够留下可审计工件。

> 直观理解：它把数学想法变成实际可运行的程序，并保存输入、输出和失败信息。这样，关键数值不会只存在于对话里，而能被重新计算和检查。

**3. 文件化研究状态与人工导向**

问题说明和单一汇总文件构成跨会话工作记忆，转录和实验日志保持追加式记录；人类作者通过会话开始或运行中的文本文件异步提供优先级、目标、审计意见和少量数学提示。关键方向转折由人类触发，而仿射重构、降维估计和证明证书主要由系统完成。

> 直观理解：长期研究的难点不只是解一道题，还包括记住失败、区分证据等级并及时换方向。该模块让机器负责大规模技术探索，同时保留人类对研究价值和方向的判断。

**训练与推理**

整个过程属于带工具和人工导向的长时程推理。每轮会话首先从问题说明与汇总文件恢复活动研究状态，再由推理智能体选择一个焦点；在研究循环中，它提出数学步骤或计算需求，编码智能体实现实验、检索材料并返回结果，推理智能体据此继续证明、改写目标或审计旧结论。多个会话可并行探索互不相同的方向，但模型会话之间没有隐藏状态共享，只有文件会被持续更新。

在本论文的关键轨迹中，系统先对极限 Krivine 方案进行上界构造搜索，观察到首阶系数与高阶非线性之间反复出现的权衡。人类随后发出方向性指令，将任务从“再找一个更好的构造”改为“证明所有构造共有的障碍”。系统据此提出仿射系数不等式，将高维分区问题约化为一维高斯不等式，生成计算机辅助证书和首版证明；内部协议先检查证明与计算，作者再独立核验并修订。推理阶段的最终输出不是一个预测标签，而是带证据等级的数学命题、证明文本、代码和可复算证书。

**复现信息**

系统由两个角色明确分离的代理组成：推理代理先使用 GPT-5.5-Pro 的最大推理强度，运行中期替换为 GPT-5.6-Sol；编码代理使用 Claude Code，底层模型先为 Claude Opus、后为 Claude Fable 5。会话通常持续数小时，同时运行约 $2$ 至 $5$ 个互不重复的研究方向；每个会话采用固定阶段，包括定向、焦点选择、研究循环和结尾审计。跨会话状态至少包括问题说明、单一汇总文件、追加式对话转录和实验日志。

计算上，候选搜索可在单个四 GPU 节点上采用浮点运算，但所有 Arb 认证计算都在 CPU 上以区间算术重做；这是解释“机器验证”可信度所必需的设计，因为区间算术显式包围数值误差。结论按已证明、数值支持、猜测或启发式分类，而论文中的“定理”还要求作者额外人工核验。需要注意，系统并非从空白问题开始：初始化材料已经包含立方—五次方案、系数公式、认证机制、数月笔记和候选方向，并曾提示可把构造障碍转化为下界；因此该案例证明的是系统在既有研究框架下进行长期综合、技术推导和证书构造的能力，不能解释为模型独立建立了全部数学框架。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 本文没有传统机器学习数据集。主要经验材料是 2026 年 6 月 16 日至 7 月 24 日的完整研究运行记录，包括约 240 个研究会话、智能体调用遥测、追加式对话记录、实验日志和反复合并的工作摘要；其作用是重建发现过程、统计资源消耗并分析系统失误。
- 数学搜索对象是 Krivine scheme 的推广空间。系统从作者已有的 cubic–quintic scheme、系数公式、认证程序、数月研究笔记以及同时列出上下界候选方向的问题陈述出发，因此测试的是“给定成熟研究框架后的长期推进能力”，不是从零发现整个理论框架的能力。
- 验证材料由浮点搜索产生的候选解及其证书组成。浮点计算在单个四 GPU 节点上运行，所有 Arb 认证计算随后在 CPU 上用区间算术重做，以检查舍入误差下结论是否仍成立；其中只有作者进一步独立核验的结果才被本文称为定理。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**认证后的 $K_G$ 下界**

证明所有允许方法都无法把 $K_G$ 压到该值以下；更大的下界会缩小未知区间。本文区分机器协议接受与作者独立核验两种证据等级。 （越高越好，因为它排除了更大的低值范围，但只有证书和证明经相应验证后才构成可靠进展。）

</div>
<div class="metric-item" markdown="1">

**认证后的 $K_G$ 上界**

由显式 Krivine scheme 保证 $K_G$ 不超过的值，用于衡量构造或连续松弛分析的性能。 （越低越好，因为它缩小了 $K_G$ 的可能区间；未经可靠认证的浮点最优值不能算有效上界。）

</div>
<div class="metric-item" markdown="1">

**证据等级**

结论被标为已证明、数值支持、猜想或启发式，并进一步区分“通过系统内部验证协议”与“作者独立核验后作为定理发表”。它不是单一分数，而是防止把搜索候选误报为数学结论的评价维度。 （作者独立核验的定理级证据强于仅机器验证，机器验证又强于普通浮点或启发式证据。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 经作者独立核验的 AI 发现下界

<div class="result-value" markdown="1">

系统在会话 55–57 的 affine reframe 后导出 $K_G\geq\frac{6\pi}{11}=1.7135\ldots$；核心约束是任意 Krivine scheme 的相关函数 $H(t)=b_1t+b_3t^3+\cdots$ 都满足 $b_3\geq2b_1-\frac{11}{6}$。作者随后独立检查并修订证明，因此该结果以 Theorem 3.2 的定理身份报告。

</div>

作者的结论是，这一证明不再构造单个困难实例，而是给所有 Krivine schemes 的性能设置统一上限，从而推出 $K_G$ 的下界。分析上，这表明系统能够在人工提示进行方向重构之后完成较长且技术复杂的证明链；它并不证明系统可自主选择这一关键重构，也不证明更强的机器生成下界已经成立。

<div class="result-source" markdown="1">

来源：Section 3, Theorem 3.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Combined with the optimality theorem of Naor and Regev [25], this implies $K_{G}\;\geq\;\frac{6\pi}{11}\;=\;1.7135\ldots$

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 运行前由 GPT-5.5-Pro 对话辅助得到的增长维度上界构造

<div class="result-value" markdown="1">

显式 limiting cubic–quintic scheme 给出 $K_G\leq\frac{\pi}{2\log(1+\sqrt{2})}-3.47\times10^{-4}$。论文称这是首个通过让维度增长获得的改进，并据此肯定回答高维是否有帮助的问题。

</div>

该结果说明增长维度的 scheme 能超过此前固定低维构造，而不只是把同一低维搜索做得更精细。它是人机交互产生并已有证书的数学结果，但早于本文所分析的当前长周期双智能体系统，因此不能作为该运行自主产出的证据。

<div class="result-source" markdown="1">

来源：Section 3, Theorem 3.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

There is an explicit limiting Krivine scheme, the cubic–quintic scheme, which can be used to show $K_{G}\;\leq\;\frac{\pi}{2\log(1+\sqrt{2})}-3.47\times 10^{-4}.$

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 通过内部协议但尚未经作者核验的后续边界

<div class="result-value" markdown="1">

系统报告上界 $1.781801841033$，随后改进到 $1.7813319810625639$，并报告更强下界 $\frac{27\pi}{49}\approx1.7311$ 与 $\frac{51\pi}{92}\approx1.7415$。这些候选均通过论文所述机器验证协议，但作者尚未亲自核验证书，故没有作为定理陈述。

</div>

这些数值显示系统的搜索与认证流水线可能继续缩小 $K_G$ 的区间，也说明内部审计并非只产生单个偶然结果。不过，“machine-verified”是作者明确限定的内部证据等级，不等同于同行审查或作者独立证明；在证书完成外部核验前，不应把这些数字当作已确立的新界。

<div class="result-source" markdown="1">

来源：Section 5, Results; lower-bound values listed in Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Beyond it, the run produced system-tested upper bounds of $1.781801841033$ and then $1.7813319810625639$, improving on the cubic–quintic value, together with the two stronger lower bounds listed in Table 2.

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

- 运行起点区间 $1.6769566742\leq K_G\leq1.7818666070$：用于判断系统是否真正推进了已知边界；上端点对应本文运行前已有的 cubic–quintic 上界。
- 经典 Krivine 上界 $\frac{\pi}{2\log(1+\sqrt{2})}$：Theorem 3.1 报告的改进以从该值减去 $3.47\times10^{-4}$ 表示，因此它是评价新上界构造的直接参照。
- 既有固定低维 Krivine schemes，包括此前约 $10^{-5}$ 量级的改进：它们用于检验让维度增长是否带来固定低维构造不能实现的收益。
- 传统的 gap instance 下界证明路线：Theorem 3.2 改为证明每个 Krivine scheme 都必须满足统一系数约束，因而比较的是一种不同的证明机制，而不只是更大的数值。

**实验想回答的问题**

- 在给定既有数学框架、数值搜索与认证工具以及人类方向性指导的条件下，长周期双智能体研究系统能否发现并验证改进 Grothendieck 常数 $K_G$ 上下界的新结果？
- 该系统在数学研究的技术执行、全局研究判断和研究状态表示三类功能上分别表现如何；哪些结果能够通过机器内部协议，哪些还需要作者独立核验后才能称为定理？

**实验实现**

系统由两个分工明确的智能体组成：推理智能体选择方向、发展论证、指定实验并审计结论；编码智能体维护仓库、实现和运行计算、检索文献并通过脚本接口驱动推理模型。推理端先使用 GPT-5.5-Pro，运行中更换为 GPT-5.6-Sol；执行端使用 Claude Code，模型由 Claude Opus 更换为 Claude Fable 5。每个数小时会话依次执行问题与摘要定向、选择焦点、研究循环和结束审计，且会话之间不保留模型上下文，只通过问题陈述、单一工作摘要、追加式记录和实验日志传递状态。每项结论在摘要中标注为已证明、数值支持、猜想或启发式；浮点候选还要接受区间算术和内部证书协议。人类通过约四十条异步指令设置优先级、推动上下界方向切换并审计结果。该设置评价的是人机协作系统整体，而没有随机划分、重复试验或统计显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 会话 44 的撤回上界构成一个失败案例：会话 4 的快速数值评估器明确注明只适合探索，但这一限制在多轮摘要改写中丢失，使未经认证的 $1.7802243$ 一度成为记录；一个本可否定它的可行性判据也在会话 8 得到后从交接状态中消失，直到 25 天后的审计才被重新证明并撤回该值。该事件定性隔离出“研究状态表示”问题：原始档案仍保存事实，失败发生在供后续决策使用的压缩摘要，而不是局部计算能力本身。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：以改进Grothendieck常数界为案例，研究长程AI研究智能体开展数学推理并产生新颖洞见的能力。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`66e8fb7a4238f2a3dd3ac9dc350f4e11bb0fc29d8f860f0b3ce912760d7e5b1c`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
