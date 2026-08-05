---
title: "[论文解读] BODHI: Do LLMs Branch Out and Discover Heterogeneous Inferences?"
description: "[arXiv 2608.02867][LLM Reasoning] 本文追问RLVR带来的推理性能提升究竟源于能力边界扩展，还是源于将采样集中到少数轨迹，并通过迷宫与按语义等价关系构造的BODHI-Tree区分表面措辞多样性和真正的推理分支。"
arxiv_id: "2608.02867"
announcement_date: "2026-08-05"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:39:44.928848+00:00"
source_sha256: "0334c63eb0d89055bdb1d395ae99ad9e944d712c38ab399de4182f2d73b6f343"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "强化学习"
  - "大型语言模型"
  - "带可验证奖励的强化学习"
  - "测试时探索"
  - "语义推理分支"
  - "BODHI-Tree"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.02867</p>

# BODHI: Do LLMs Branch Out and Discover Heterogeneous Inferences?

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Soumadeep Saha, Krish Sharma, Akshay Chaturvedi, Nicholas Asher</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02867v1) · [PDF 下载](https://arxiv.org/pdf/2608.02867v1) · **关键词** 大型语言模型, 带可验证奖励的强化学习, 测试时探索, 语义推理分支, BODHI-Tree<br>
**项目页**: [https://espressovi.github.io/BODHI](https://espressovi.github.io/BODHI)

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

本文追问RLVR带来的推理性能提升究竟源于能力边界扩展，还是源于将采样集中到少数轨迹，并通过迷宫与按语义等价关系构造的BODHI-Tree区分表面措辞多样性和真正的推理分支。

**不用术语来说**：一个模型可以用许多不同说法重复同一种解法，也可以真正尝试多条思路；只统计生成文本的差异，会把前一种“换个说法”误当成探索。本文要弄清楚：经过可验证奖励强化学习后，模型是否仍会考虑多种实质不同但同样正确的推理路径，以及这种路径收缩是否正是其更容易采样到正确答案的原因。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出以受控迷宫和BODHI-Tree共同研究测试时探索：BODHI-Tree将数学推理轨迹切分为节点，再合并语义等价节点，使不同子节点对应概念上不同的后续推理，从而能够测量真正的语义分支，而非仅测量文本差异。
- 围绕三个递进问题建立实证分析框架：检验RLVR是否强化对特定轨迹的偏好、这种集中是否超越句法或风格差异，以及策略空间收缩与性能提升之间有何联系；作者据此主张RLVR同时压缩无效路径和有效但语义不同的路径。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究大型语言模型（LLM）在带可验证奖励的强化学习（RLVR）之后，测试时还能否探索多个语义上不同的推理路径。RLVR把语言模型生成答案的过程视为策略 $[...][0m$ 在序列决策环境中的行动，并依据确定性验证器给出的奖励优化该策略。论文关注的不是模型能否生成表面形式不同的文本，而是对于同一问题，模型是否仍能访问多个真正不同、且可能同样有效的推理延续；这一区分是判断RLVR提升能力边界还是主要提升采样效率的基础。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**带可验证奖励的强化学习（RLVR）**

RLVR将模型生成下一个词看作在当前状态下采取行动，并用程序或规则验证最终答案是否正确，再把验证结果作为奖励训练模型。直观地说，模型不是只模仿示范文本，而是通过反复尝试并获得“答对或答错”的反馈来调整生成倾向。

</div>
<div class="concept-item" markdown="1">

**测试时探索**

测试时探索指模型面对同一个输入时，能够生成哪些可能的后续轨迹，以及这些轨迹被生成的概率。本文特别关心语义不同的推理路径，而不是变量改名、语序变化等不改变推理内容的表面差异。

</div>
<div class="concept-item" markdown="1">

**验证器等价与语义等价**

若多个生成结果都得到验证器认可，它们可以称为验证器等价，但这不保证它们采用了相同的正确推理。语义等价则要求推理步骤在概念或意义上基本相同；因此，验证器等价的不同语义路径才是本文要分析的有效探索空间。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定输入问题和当前生成状态 $s_t$，模型策略 $[...][0m$ 逐步生成词元 $o_t$，形成从初始输入到终止输出的轨迹。论文研究在RLVR训练前后，模型对所有有限延续的概率分配是否发生集中：一方面使用受控迷宫任务直接观察有效移动、非法移动和回溯等探索行为；另一方面从数学推理轨迹中切分推理节点，并依据语义相似性合并节点，构造BODHI-Tree，使同一节点表示若干语义等价轨迹、不同子节点表示概念上不同的后续推理。核心假设是，验证器通常只检查终态或答案，因此“得到正确答案”不足以刻画中间推理的多样性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\pi_{\theta}$**

参数为 $\theta$ 的语言模型策略，即在给定当前状态时生成下一个词元的概率分布。

</div>
<div class="notation-item" markdown="1">

**$s_t$**

第 $t$ 步的生成状态，通常包括原始输入以及此前已经生成的词元。

</div>
<div class="notation-item" markdown="1">

**$o_t$**

第 $t$ 步生成的词元，也就是策略在状态 $s_t$ 下采取的动作。

</div>
<div class="notation-item" markdown="1">

**$T$**

一条生成轨迹的终止步数或长度；完整轨迹可写为从输入开始、依次追加 $o_1$ 到 $o_T$ 的状态序列。

</div>

</div>

**直接相关的工作**

- **Yue et al.（2025）**: 该工作认为RL训练后的模型未必发现基础模型没有的全新推理路径，并观察到其高阶 $\mathrm{pass}@k$ 扩展能力下降。本文将问题推进到语义分支层面，检验这种性能现象是否对应真实推理多样性的减少，而不只是在答案采样层面观察变化。
- **Wang et al.（2025）**: 该工作指出RL策略依赖约 $20\%$ 的高熵“分叉词元”来产生测试时推理多样性。本文认为词元级熵无法区分风格变化与推理变化，因此通过迷宫和BODHI-Tree直接考察语义上不同的延续是否也发生集中。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

RLVR已在多类推理任务上提高大语言模型的表现，但其收益机制仍不清楚。若它只是让模型更频繁地选择既有的高成功率轨迹，而没有扩大可达到的推理能力，那么表面上的准确率或采样效率提升可能伴随真实探索能力下降。这会限制自洽采样、思维树等依赖多样候选路径的方法，也可能妨碍模型发现新解法。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于策略熵或生成多样性的RLVR分析**：已有研究通过策略熵、高熵词元或不同生成轨迹的分布，判断强化学习后模型是否发生策略坍缩、是否减少探索。这类分析能够显示输出概率更集中，却未必能判断差异来自推理思路还是措辞、变量命名和表达顺序。
- **通过训练机制维持探索或防止策略坍缩**：相关工作从强化学习训练动态入手，设计鼓励探索或抑制策略坍缩的方法，目标是避免模型过早集中于少数输出。然而，这一路线主要处理“如何保持分布广度”，尚未充分刻画RLVR如何重新分配语义不同推理后续之间的偏好。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 文本级或词元级差异会混合两种性质不同的变化：一种只是变量名、可交换运算顺序或自然语言表述不同，另一种才是采用了不同的推理策略。因此，仅观察策略熵下降不能判定RLVR是否压缩了真正的推理分支。
- 以往工作较多关注训练中的策略坍缩和探索保持，却缺少可控的分支环境与语义等价归并工具，因而难以同时回答轨迹偏好是否增强、有效异质路径是否被剪除，以及这种剪除如何关联采样效率和任务表现。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一种能够在分支点上比较RLVR模型与基础模型、并把表面表达变化从语义不同的推理后续中分离出来的分析框架。尤其未解决的是：RLVR是否会降低语义分支偏好的熵，从而连同错误路径一起排除部分验证结果同样正确、但推理方式不同的路径；这一策略变化又是否解释了其性能收益。

</div>
<div markdown="1"><span>核心问题</span>

RLVR是否限制大语言模型在测试时的探索并强化对少数轨迹的偏好；若确有集中，这种集中究竟只是句法或风格层面的，还是发生在语义不同的推理分支之间；这种策略转移又如何与性能提升相联系？

</div>
<div markdown="1"><span>作者直觉</span>

迷宫提供了路径、违规移动和回溯都可直接判定的受控环境，适合观察模型在明确分岔处如何选择；数学推理则需要先把大量轨迹按语义等价关系合并成BODHI-Tree，使同一节点代表实质相同的推理状态、不同子节点代表概念上不同的延续。这样，若RLVR模型在这些语义分支上的选择仍明显更集中，就不能仅用“表达风格更统一”解释；再把这种集中与约束遵守、回溯和轨迹有效性联系起来，便可检验其采样效率是否来自缩小可访问状态空间。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

BODHI采用两条互补的受控探测管线，比较基础模型、长思维链蒸馏模型与RLVR模型的探索策略。第一条管线把模型置于确定性迷宫中，将输出限制为上、下、左、右四种离散动作，使不同轨迹直接对应真正的路径选择，而不会混入措辞变化。第二条管线面向自然语言数学推理：先从多个前沿模型采样大量正确解答，将每条解答切分为推理步骤，再用语义等价判断把表达不同但数学含义相同的步骤合并，构造BODHI-Tree。树中的分叉因此代表语义上不同的后续推断，而不是同一推断的改写。

在两类环境中，作者都从一个已有至少两种后续选择的前缀$a$出发，计算待测模型对候选续写$s^{(1)}$与$s^{(2)}$的长度归一化对数概率，再经softmax得到二选一偏好分布，并以候选偏好熵CPE衡量分支偏好是否集中。最后，以同一基础模型为参照计算$\Delta\mathrm{CPE}$，把后训练前后的差异归因于蒸馏或RLVR；负值表示后训练使模型更偏向少数分支，正值则表示分支偏好变得更均匀。直观而言，该方法不是只数模型写出了多少种答案，而是先确认这些答案是否走了不同的“思路岔路”，再检查模型在每个岔路口把概率押在了哪些方向。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造受控迷宫探索探针

将迷宫状态视为推理前缀，将合法移动、撞墙移动、最短路径移动和其他可达移动视为可明确验证的后续选择；对基础、蒸馏和RLVR模型采样或读取其动作概率与访问轨迹。由于动作空间固定，轨迹差异可直接解释为策略差异。

<div class="method-step__io" markdown="1">

**输入**：由Maze Dataset库实例化的确定性图遍历任务，以及只能输出$\{\texttt{<left>},\texttt{<right>},\texttt{<up>},\texttt{<down>}\}$的语言模型。<br>
**输出**：模型在迷宫节点上的访问分布、候选移动偏好，以及可用于分析约束遵循、路径多样性和回溯能力的分支实例。

</div>

**直观理解**：迷宫相当于去掉语言包装的推理实验室：每一步只有四个方向，因此模型换一种说法不会被误认为发现了新路线。撞墙、绕路和折返也都有客观定义，便于判断模型究竟是在探索还是只沿最熟悉的路径前进。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 收集并切分正确数学推理轨迹

先依据标准答案过滤错误响应，仅保留正确轨迹$A^{(1)},\ldots,A^{(n)}$；随后由LLM把每条轨迹切成有独立推理含义的片段$a_j^{(i)}$，满足$A^{(i)}=\operatorname{concat}([a_1^{(i)},\ldots,a_{n_i}^{(i)}])$。切分把长文本转化为可逐步对齐的推理单元。

<div class="method-step__io" markdown="1">

**输入**：AIME问题$Q$，以及由$o3$、$o4$-mini$、DeepSeek R1和Qwen3-235B等模型在$T=1.0$下采样的自然语言解答。<br>
**输出**：每个问题对应的一组正确且已分段的推理轨迹；最终探针包含235道AIME题、约2万条正确响应，平均每题约85条。

</div>

**直观理解**：这一步类似把多位学生的完整解答拆成一行一行的关键推导。只保留最终答案正确的解答，是为了让后续树中的分支主要表示不同的有效解法，而不是把明显错误与有效探索混在一起。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按语义等价构造BODHI-Tree

算法从根节点$v_{\texttt{root}}$开始，为每条轨迹维护当前位置$z[i]$；依次读取轨迹头部片段，若它与当前节点或某个子节点语义匹配便合并，否则创建新子节点并形成分叉。$M(x,y)$在$y$与$x$完全等价或等价于$x$的一部分时返回真，以对齐粒度不同但含义兼容的推导。

<div class="method-step__io" markdown="1">

**输入**：问题$Q$、分段轨迹$A^{(i)}$及基于GPT-oss-120b的匹配函数$M(x,y)$。<br>
**输出**：前缀树$T=(V,E)$：每个节点$v\in V$收纳一组语义等价陈述，每条边$u\leadsto v\in E$表示某条解答中$v$类步骤接在$u$类步骤之后；根到叶的不同路径代表不同解题轨迹。

</div>

**直观理解**：它像把许多学生的解法叠成一张路线图：意思相同的步骤汇入同一站点，真正采用不同推断时才岔开。两条轨迹的最低公共祖先对应其最长的共享等价推理前缀，因此树能定位“从哪一步开始想法不同”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算分支偏好熵并比较后训练变化

分别计算各候选后续的逐token平均对数概率，以softmax归一化为候选间偏好，再计算条件熵$\mathrm{CPE}$；用待测模型的熵减去同源基础模型的熵得到$\Delta\mathrm{CPE}$。长度归一化避免较长续写仅因包含更多token而天然获得更低的总概率。

<div class="method-step__io" markdown="1">

**输入**：迷宫或BODHI-Tree中的分支前缀$a$、至少两个候选后续$s^{(1)}$与$s^{(2)}$，以及待测模型$P_{\texttt{model}}$和对应基础模型。<br>
**输出**：每个分支点的$\mathrm{CPE}$与$\Delta\mathrm{CPE}$，用于比较蒸馏或RLVR是否使可选推理后续的概率分布更集中。

</div>

**直观理解**：可把一个分支点看作岔路口：若两条路概率接近，熵较高，说明模型愿意尝试不同方向；若概率几乎都压在一条路上，熵较低。与训练前的同一模型相比，便能判断这种偏好集中是否由后训练造成。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 长度归一化候选偏好与候选偏好熵

$$
\begin{aligned} S_{\texttt{model}}\bigl(s^{(i)}\mid a\bigr) &= \frac{1}{\lvert s^{(i)}\rvert}\sum_{k=1}^{\lvert s^{(i)}\rvert}\log P_{\texttt{model}}\bigl(s_k^{(i)}\mid s_{<k}^{(i)},a\bigr),\\ P\bigl(s^{(i)}\mid a\bigr) &= \frac{\exp\!\left(S_{\texttt{model}}(s^{(i)}\mid a)\right)}{\sum_{j=1,2}\exp\!\left(S_{\texttt{model}}(s^{(j)}\mid a)\right)},\\ \mathrm{CPE}_{\texttt{model}}\bigl(s^{(1)},s^{(2)};a\bigr) &= H_{\texttt{model}}^{\mathrm{Branch}}\bigl(s^{(1)},s^{(2)}\bigr)=-\sum_{i=1,2}P\bigl(s^{(i)}\mid a\bigr)\log P\bigl(s^{(i)}\mid a\bigr). \end{aligned}
$$

**符号说明**

- $a$：分支发生前的共同推理前缀或迷宫状态。
- $s^{(i)}$：第i个候选后续序列；本文的公式在每次比较中使用两个候选。
- $s_k^{(i)}$：候选后续$s^{(i)}$的第k个token。
- $s_{<k}^{(i)}$：候选后续$s^{(i)}$中位于第k个token之前的局部前缀。
- $\lvert s^{(i)}\rvert$：候选后续$s^{(i)}$的token长度。
- $P_{\texttt{model}}$：待测语言模型给出的自回归条件概率。
- $S_{\texttt{model}}(s^{(i)}\mid a)$：候选后续在给定前缀下的平均每token对数概率。
- $P(s^{(i)}\mid a)$：只在当前两个候选之间softmax归一化后的相对偏好概率，并非候选在完整输出空间中的绝对生成概率。
- $H_{\texttt{model}}^{\mathrm{Branch}}$：模型在当前分支候选上的条件熵，与CPE为同一量。

<div class="equation-explanation" markdown="1">

**直观理解**：第一行把整段续写的概率换算成平均每个token的得分，以减轻长度差异；第二行只在两条备选路线间形成可比较的概率；第三行计算该二项分布的熵。两条路线越势均力敌，CPE越高；模型越只偏爱其中一条，CPE越低，因此它测量的是“对已知异质后续的偏好均匀程度”，而非模型能够创造多少全新推理。<br>
**原文位置**：第3.3节，公式(1)–(3)

</div>

</div>

<div class="equation-block" markdown="1">

#### 后训练引起的候选偏好熵变化

$$
\Delta\mathrm{CPE}_{\texttt{model}}\bigl(s^{(1)},s^{(2)};a\bigr)=\Delta H_{\texttt{model}}^{\mathrm{Branch}}\bigl(s^{(1)},s^{(2)}\bigr)=H_{\texttt{model}}^{\mathrm{Branch}}\bigl(s^{(1)},s^{(2)}\bigr)-H_{\texttt{base}}^{\mathrm{Branch}}\bigl(s^{(1)},s^{(2)}\bigr)
$$

**符号说明**

- $\Delta\mathrm{CPE}_{\texttt{model}}$：待测后训练模型相对于同源基础模型的分支偏好熵变化。
- $H_{\texttt{model}}^{\mathrm{Branch}}$：经过蒸馏或RLVR后模型在同一分支候选上的条件熵。
- $H_{\texttt{base}}^{\mathrm{Branch}}$：相应预训练基础模型在同一前缀和候选上的条件熵。
- $s^{(1)},s^{(2)}$：在同一前缀后语义或轨迹上不同的两个候选后续。
- $a$：两个模型共同接受的固定前缀。

<div class="equation-explanation" markdown="1">

**直观理解**：该式进行配对差分：在相同岔路口、相同候选上，将训练后的熵减去训练前基础模型的熵。若$\Delta\mathrm{CPE}<0$，说明后训练强化了对某条路线的偏好；但这本身不能区分“正确排除非法路线”和“丧失有效路线多样性”，所以作者又加入Legal Only、Avoid Short Path和死胡同回退实验作机制诊断。<br>
**原文位置**：第3.3节，公式(4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：CPE与$\Delta\mathrm{CPE}$是事后探测指标，不是用于反向传播的训练损失，论文也未提出新的优化目标。为隔离后训练方式，作者从公开基础检查点构造匹配三元组$(\mathrm{LLM}_{\texttt{Base}},\mathrm{LLM}_{\texttt{Distil}},\mathrm{LLM}_{\texttt{RLVR}})$：先用监督式长思维链蒸馏得到Distil模型，再在可验证奖励下继续强化学习得到RLVR模型；分析时则把两种后训练模型分别与同源Base模型比较。迷宫训练使用oracle生成的正确路线提供监督或可验证信号；数学训练使用OpenThoughts-114k-math中的长思维链样本进行蒸馏，并以DAPO-Math-17k进行RLVR。由于所给章节未给出RLVR具体奖励函数和优化器公式，不能把答案正确性之外的奖励结构进一步具体化。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双模态探索探针**

迷宫探针提供完全离散、可验证的动作空间，用于无语言噪声地测量路径选择；数学探针保留真实自然语言推理的复杂性，并通过语义合并消除同义改写造成的伪多样性。两者共享“前缀—候选后续”的分析单位，使同一套CPE指标可以跨环境解释。

> 直观理解：迷宫给出高内部效度，即分支几乎一定是真分支；数学题给出更贴近实际推理的外部效度。两者结论相互印证，可减少仅凭某一种任务误判模型探索能力的风险。

**2. 语义匹配与BODHI-Tree构造器**

匹配函数$M(x,y)$由GPT-oss-120b实现，判断$y$是否与$x$等价或被$x$涵盖；构树时以节点代表语义等价类，以父子边保存推理顺序。该非对称涵盖判据允许一个较细的片段与包含该含义的较粗节点对齐，作者还以其他前沿模型复核判断一致性。

> 直观理解：自然语言中“移项后求根”和更详细的三句推导可能表达同一数学动作，若逐字比较会被错误拆成多个分支。语义匹配器负责把这些表面差别折叠起来，让树的宽度更接近真实思路数量。

**3. 候选偏好熵评估器**

评估器不依赖实际采样频数，而是读取待测模型对固定候选续写的token条件概率；先形成长度归一化分数，再在同一分支的候选之间归一化并计算熵。通过与同源基础检查点相减，$\Delta\mathrm{CPE}$控制了模型家族和预训练策略本身的差异。

> 直观理解：直接数采样结果容易受样本量和随机性影响，而读取概率可更精细地看到模型在岔路口的真实倾向。对训练前后做差，则类似同一个学生接受训练前后的配对测试。

**训练与推理**

训练阶段，迷宫模型以SmolLM3-3B-Base和Qwen3-8B-Base为起点，在3万条oracle解答上做SFT蒸馏，再使用1.2万条样本做RLVR。数学模型以gemma-3-12b-pt、Qwen3-8B-Base、Qwen3.5-9B-Base和Qwen2.5-32B-Base为起点，在OpenThoughts-114k-math中抽取的5万条样本上进行Long-CoT蒸馏，再用DAPO-Math-17k进行RLVR；Qwen2.5-32B的RL版本直接采用同样在DAPO-Math-17k上训练的DAPO-Qwen2.5-32B。

评估阶段先离线建立探针。迷宫直接提供状态与可枚举动作；数学部分从304道AIME题开始采样，过滤后保留235题及约2万条正确轨迹，将其切分并构造成BODHI-Tree。随后，对树或迷宫中的每个候选分支，把相同前缀$a$与固定后续$s^{(i)}$送入Base、Distil和RLVR模型进行teacher-forcing式概率评分，计算CPE及相对Base的$\Delta\mathrm{CPE}$。最后实施受约束解码和前缀 steering：Legal Only屏蔽撞墙等非法token，Avoid Short Path屏蔽最优移动，No Reversal屏蔽连续反向动作；死胡同实验直接读取$p_b$，数学干扰实验则重新生成后续并按最终答案正确性判断是否恢复。

**复现信息**

BODHI-Tree数据采样时使用$T=1.0$并将可用推理强度设为最高，总API预算为3000美元；正确响应由o4-mini切分。语义匹配器采用GPT-oss-120b、4-shot提示、$T=1$、$\texttt{top}_p=0.99$和中等推理强度，总计约47万次匹配调用，即每棵树约2000次。匹配质量以独立前沿模型复核，GPT-oss-120b与deepseek-v4-pro、gpt-5.6-luna之间的Cohen's $\kappa$分别为0.815和0.837；这支持匹配器具有较高一致性，但并不等于人工标注的绝对正确率。

公平解释结果时需注意三点。第一，CPE是在作者预先收集到的两个候选之间重新归一化，不能解释为模型对整个可能推理空间的完整熵。第二，BODHI-Tree只由最终答案正确的轨迹构成，因此主要描述正确解空间内的语义分叉；非法或错误续写需由迷宫约束实验和干扰实验补充。第三，算法用节点代表片段与新片段比较，且允许“新片段被节点代表内容涵盖”的非对称匹配，这有助于处理粒度差异，但树形结构仍依赖LLM切分与语义裁决，复现时必须保留提示、匹配方向和节点代表选择规则。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Maze Dataset 用于受控迷宫实验：监督微调使用 $30\mathrm{K}$ 个大小为 $5\times5$、$7\times7$、$9\times9$ 的迷宫及 oracle 轨迹，RLVR 使用另行准备的 $12\mathrm{K}$ 个迷宫。评测第 4.1 节从 $50$ 个迷宫各采样 $1\mathrm{K}$ 条生成，以节点访问分布直接衡量状态空间探索；第 4.3 节另取 $5\mathrm{K}$ 个位于正确路径上的“走廊”节点，检验模型能否排除不符合迷宫结构的动作。
- OpenThoughts-114k-math 为数学 Long-CoT 蒸馏来源，实验随机选取 $50\mathrm{K}$ 个样本建立蒸馏策略。它提供与 RLVR 策略进行配对比较的起点，使差异更接近后续强化学习造成的变化，而不是不同基础模型或聊天模板造成的变化。
- DAPO-Math-17k 用于数学 RLVR 训练，共训练 $1\mathrm{K}$ 步；奖励由 Math-Verify 的答案正确性奖励和输出格式奖励组成，不使用长度奖励。所有训练数据均与探测集去重；数学推理轨迹进一步按语义等价关系组织为 BODHI-Trees，用于采样真实的语义分支点。原文没有在所给章节中明确报告探测集名称、规模或标准训练/验证/测试划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**节点访问熵 $H$**

先由多次迷宫生成估计每个节点被访问的概率，再计算该分布的熵。它衡量模型的轨迹覆盖是否分散：较高的 $H$ 表示生成能到达更多且分布更均衡的状态，较低的 $H$ 表示探索集中在较少路径。该指标会同时受合理探索、无效动作和回溯行为影响，因此不能单独等同于推理能力。 （若目标是测试时探索多样性，则越高表示覆盖越广；若目标是避免无效状态，则较低未必更差，必须结合走廊节点和语义分支实验解释。）

</div>
<div class="metric-item" markdown="1">

**条件前缀熵差 $\Delta\mathrm{CPE}$**

在同一锚点前缀下，对两条候选续写的模型概率偏好进行比较；候选被截断到 $20$ 个 token，并直接使用 logits 计算。论文比较 $\Delta\mathrm{CPE}_{\mathrm{RLVR}}-\Delta\mathrm{CPE}_{\mathrm{Distil}}$，负值表示 RLVR 后在分支点更偏向其中一条路线，即分支熵更低、轨迹偏好更强。 （没有统一的任务性能方向：较低意味着采样更集中、可能提高命中高概率正确路线的效率，但也意味着异质推理路线更少。）

</div>
<div class="metric-item" markdown="1">

**降低 $\Delta\mathrm{CPE}$ 的样本比例**

统计配对样本中 RLVR 模型相对蒸馏模型出现 $\Delta\mathrm{CPE}$ 下降的比例，用于判断平均变化是否由少量极端分支驱动。接近 $100\%$ 表示轨迹偏好增强广泛存在于样本层面。 （若要验证“RLVR 普遍收缩分支分布”这一描述性假设，则越高证据越强；它不表示准确率或总体推理能力更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 受控迷宫中的测试时状态探索：Qwen3-8B 与 SmolLM3-3B 的 RLVR 策略对比各自蒸馏策略。

<div class="result-value" markdown="1">

Qwen3-8B 的平均节点访问熵由蒸馏模型的 $2.3380$ 降至 RLVR 模型的 $1.8138$，差值为 $-0.5242$，其 $95\%$ 置信区间为 $[-0.7005,-0.3435]$，且 $p<0.0001$。SmolLM3-3B 同样由 $1.9288$ 降至 $1.6092$，差值为 $-0.3196$，$95\%$ 置信区间为 $[-0.4252,-0.2085]$，且 $p<0.0001$。

</div>

作者据此主张 RLVR 后的策略在测试时访问的迷宫状态更少，探索分布也更集中，而且该现象在两个模型规模上复现。分析上，这直接支持“RLVR 改变 rollout 分布”而非仅改变最终答案准确率；但节点访问熵下降本身不能区分有益地排除非法动作与有害地放弃合理替代路径，也不能证明模型能力边界缩小。

<div class="result-source" markdown="1">

来源：第 4.1 节“Measuring Test-time Exploration”；Qwen3-8B 对应 Figure 2 附近正文，SmolLM3-3B 数值见同节正文

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Results with SmolLM3-3B are similar, and we have: H Distil = 1.9288 (95% CI [1.7938, 2.0632]), H RLVR = 1.6092 (95% CI [1.4344, 1.7756]), and Δ H = − 0.3196 (95% CI [− 0.4252, − 0.2085], p < 0.0001).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 数学 BODHI-Tree 的真实分支点：比较 RLVR 与蒸馏策略在 $10\mathrm{K}$ 个分支元组上的轨迹偏好。

<div class="result-value" markdown="1">

四个模型的 $\Delta\mathrm{CPE}_{\mathrm{RLVR}}-\Delta\mathrm{CPE}_{\mathrm{Distil}}$ 均为负：Qwen3-8B、Qwen3.5-9B、Gemma3-12B 和 Qwen2.5-32B 分别为 $-0.0061$、$-0.0069$、$-0.0225$ 和 $-0.0345$；出现下降的样本比例分别为 $95.49\%$、$100.0\%$、$99.98\%$ 和 $99.46\%$。作者报告总体下降达到 $p<0.0001$。

</div>

这说明 RLVR 后的模型在遇到两条替代推理续写时，几乎总是比蒸馏模型更强烈地偏向其中一条，而不是平均效应由少数异常样本造成。该结果与采样效率提升相容：概率集中可让有限采样更常命中首选路线；但实验没有在这里证明首选路线总是正确，也没有直接建立熵下降与准确率提升之间的因果关系。

<div class="result-source" markdown="1">

来源：Table 1 及第 4.2 节“Trajectory Preference in RLVR”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

There is a significant drop in Δ CPE (p < 0.0001) for almost all samples, suggesting that RL-trained models have significantly stronger trajectory preferences at branch points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### BODHI-Tree 中句法变体与语义不同续写的对照：从 $2.5\mathrm{K}$ 个节点比较 RLVR 相对蒸馏模型的熵收缩。

<div class="result-value" markdown="1">

除 Qwen3.5-9B 的句法差异下降不显著外，其余模型在句法变体间也出现 $\Delta\mathrm{CPE}^{\mathrm{Syntax}}$ 下降；更关键的是，所有受测 RLVR 模型在语义不同续写间的 $\Delta\mathrm{CPE}^{\mathrm{Semantics}}$ 都显著下降。句法与语义收缩程度之差通常达到 $p<0.02$，但 Qwen3-8B 为 $p=0.11$。

</div>

作者据此否定“熵塌缩只是变量命名、交换律顺序等写法趋同”的单一解释：收缩也发生在解题思路不同的分支上，并且通常更强。严格地说，Qwen3-8B 的句法—语义差异没有达到显著水平，因此不能声称每个模型都已证明语义收缩强于句法收缩；更稳妥的结论是所有模型都存在显著的语义分支收缩。

<div class="result-source" markdown="1">

来源：第 4.4 节“Is Entropy Collapse Stylistic?”及 Figure 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The difference between them is statistically significant (p < 0.02 except for Qwen3-8B, p = 0.11).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验主要比较蒸馏策略与其 RLVR 后版本，但不同模型的训练路径并不完全一致：Qwen3.5-9B 和 DAPO-Qwen2.5-32B 使用 Zero-RL，而 Qwen3-8B 与 Gemma3-12B 采用蒸馏后 RLVR。因此跨模型一致性增强了外部有效性，却不等同于严格控制所有训练因素的统一因果实验。
- 节点访问熵和 $\Delta\mathrm{CPE}$ 衡量的是分布集中程度，而非正确率、能力边界或新推理方法的实际发现率。BODHI-Tree 的语义聚类质量、仅取 $20$ token 的候选截断，以及迷宫与数学任务的有限范围，都可能影响“语义探索收缩”向更广泛 LLM 推理场景的推广；本文证据支持相关机制，但未直接证明熵收缩导致采样效率提升。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Long-CoT 蒸馏策略是最核心基线：对同一模型比较蒸馏后与进一步接受 RLVR 后的策略，可以检验强化学习是否改变探索分布。作者还匹配两类模型的聊天模板，以减少格式差异这一混杂因素。
- Qwen3-8B 的蒸馏版与 RLVR 版用于迷宫和数学分支实验，是跨任务观察探索熵变化的主要模型对。
- SmolLM3-3B 的蒸馏版与 RLVR 版用于迷宫节点访问实验，检验状态探索收缩是否只发生在 Qwen3-8B 上。
- Qwen3.5-9B、Gemma3-12B 与 Qwen2.5-32B 等模型对用于 BODHI-Tree 分支测试，检验轨迹偏好增强能否跨模型规模与训练来源复现；其中部分模型采用 Zero-RL，因而并非所有比较都具有完全相同的训练路径。

**实验想回答的问题**

- 在控制任务难度与后训练数据的条件下，RLVR 模型在测试时是否比蒸馏模型访问更少的可达状态，并在推理分支点表现出更集中的轨迹偏好？
- 观察到的熵下降究竟来自模型更好地排除无效续写与表面句法变体，还是也意味着对语义不同但合理的推理路线探索不足？

**实验实现**

迷宫第 4.1 节在 $50$ 个迷宫上各采样 $1\mathrm{K}$ 次，温度为 $T=1.0$、$\mathrm{top\_k}=10$，并用 bootstrap 给出 $95\%$ 置信区间。第 4.2—4.4 节不通过完整采样估计分支概率，而是直接读取 logits；用于 CPE 的候选续写统一截断为 $20$ 个 token。轨迹偏好实验从 BODHI-Trees 抽取 $10\mathrm{K}$ 个元组，句法—语义分解实验抽取 $2.5\mathrm{K}$ 个分支节点，并采用配对 bootstrap 检验。迷宫训练使用自定义正确性验证器和可解析格式奖励；数学 RLVR 使用 Dr. GRPO、Math-Verify 正确性奖励及格式奖励，且明确不加入长度奖励。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 无歧义“走廊”节点对照：选择正确迷宫路径上的 $5\mathrm{K}$ 个度为 $2$ 的节点，此时除返回来路外只有一个符合结构的前进方向。 | RLVR 模型在这些走廊节点表现出统计显著的熵下降；所给节选未报告具体熵值、效应量、置信区间或精确 $p$ 值。 | 该对照隔离了“更好地排除无效续写”这一来源。因为走廊节点没有真正的路线歧义，较低熵在这里更可能表示模型学会迷宫语义和环境约束，而不是损失合理探索。因此，总体熵下降不能全部解释为能力恶化；但该对照也不能解释有真实多分支节点上的收缩。 | 第 4.3 节“Exploring Invalid Continuations”及 Figure 3<br><span class="experiment-evidence">We find that (see Figure 3) the RL-trained models demonstrate statistically significant entropy collapse in halls, suggesting that the RLVR policy better delineates between different verifier-equivalence classes.</span> |
| 保持同一锚点前缀 $A$，分别比较同一语义子树中的句法不同续写 $a,b$，以及不同语义子树中的续写 $a,g$。 | 所有 RLVR 模型的语义分支指标 $\Delta\mathrm{CPE}^{\mathrm{Semantics}}$ 均相对蒸馏模型显著下降；句法分支指标中只有 Qwen3.5-9B 未达到显著下降。原文在所给节选中未明确报告各模型的具体效应量。 | 这一拆分控制了共同前缀和局部上下文，把“只是偏好某种写法”与“偏好某种推理思路”区分开。语义条件在所有模型上显著收缩，说明 RLVR 压低的不仅是无关紧要的表述噪声；不过语义等价类依赖 BODHI-Tree 的构造质量，不能视为完全无误的人工真值。 | 第 4.4 节“Is Entropy Collapse Stylistic?”及 Figure 4<br><span class="experiment-evidence">However, all RL-trained models in the study have a statistically significant drop in Δ CPE Semantics compared to their distilled counterparts.</span> |

**定性案例**

- Figure 8 展示了数学推理干扰项：在一段正确的组合恒等式推导中插入与当前问题无关的二次方程求根内容，随后模型继续原推导。该例说明作者还关注模型面对局部不连贯片段时的行为，但所给节选没有包含第 5.2 节的定量结果，因此不能据此判断 RLVR 与蒸馏模型谁更能识别或回溯该错误。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Analyzes how RLVR post-training changes semantic branching, exploration diversity, and backtracking in LLM reasoning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`0334c63eb0d89055bdb1d395ae99ad9e944d712c38ab399de4182f2d73b6f343`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
