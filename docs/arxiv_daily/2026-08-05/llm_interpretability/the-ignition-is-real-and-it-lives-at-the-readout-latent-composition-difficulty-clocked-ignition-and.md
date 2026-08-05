---
title: "[论文解读] The Ignition Is Real, and It Lives at the Readout: Latent composition, difficulty-clocked ignition, and the interface-constituted commit in a recurrent-depth reasoner"
description: "[arXiv 2608.03263][LLM 机制与可解释性] 本文通过从头复现一个仅以非语言合成结构训练的3000万参数循环深度推理器，并预注册、双通道追踪其训练与推理过程，检验“组合点火”究竟是真实计算事件、测量假象，还是语言语料遗产。"
arxiv_id: "2608.03263"
announcement_date: "2026-08-05"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:42:52.314769+00:00"
source_sha256: "2fbb30947d9e01822e23fb8ca655f56008087f8ad54fae24e02455acbbf305e5"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "循环深度推理"
  - "潜在推理"
  - "组合点火"
  - "词表读出"
  - "隐藏状态几何"
  - "决策提交"
  - "中间表示可解码性"
  - "非语言合成数据"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2608.03263</p>

# The Ignition Is Real, and It Lives at the Readout: Latent composition, difficulty-clocked ignition, and the interface-constituted commit in a recurrent-depth reasoner

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Simon Lam-Muir</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03263v1) · [PDF 下载](https://arxiv.org/pdf/2608.03263v1) · **关键词** 循环深度推理, 潜在推理, 组合点火, 词表读出, 隐藏状态几何, 决策提交, 中间表示可解码性, 非语言合成数据<br>


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

本文通过从头复现一个仅以非语言合成结构训练的3000万参数循环深度推理器，并预注册、双通道追踪其训练与推理过程，检验“组合点火”究竟是真实计算事件、测量假象，还是语言语料遗产。

**不用术语来说**：潜在推理模型会在内部反复更新表示，并在某一步突然稳定地给出答案；但仅观察输出端的突变，无法判断模型是否真的在这一刻完成了组合计算，也可能只是解码器把连续变化放大成突变，或模型复现了从人类语言中学到的表面模式。本文要辨明这一现象的来源及发生位置。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 建立独立复现与预注册检验框架：按已发表配方和相同随机种子从头训练模型，记录其发展过程，以完整行为签名验证复现忠实度，并同时测量词表读出排名与隐藏状态变化，从而区分计算现象和测量工具造成的现象。
- 将点火定位为读出接口上的承诺事件：答案到达时间随问题深度增加、解答在单次迭代内形成并保持稳定；提交时答案决策间隔出现大幅跳变，而此后的隐藏状态运动主要是几乎不影响读出的径向尺度变化。纯非语言训练也能产生该签名，说明语言语料继承并非必要条件。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于循环深度推理模型（recurrent-depth reasoner）的机理分析：模型反复应用同一计算模块，在隐藏状态中进行多轮迭代，最后经词表读出层给出答案。已有研究发现，正确答案似乎会在某次迭代中突然进入高排名，且首次出现的时间随问题所需推理跳数增加；这种现象被称为“组合点火”。本文关注的基础问题不是模型最终能否答对，而是该突变究竟代表真实的内部计算、仅由测量或读出接口造成的假象，还是从人类语言训练数据继承的模式。为区分这些解释，研究同时观察词表读出所呈现的答案排名和隐藏状态的几何变化，并在纯非语言合成结构上训练一个约 $30$M 参数的独立模型实现。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**循环深度推理**

模型在多个推理迭代中重复使用同一组参数，并逐步更新隐藏状态，而不是为每一层配置完全独立的参数。这里的“深度”主要来自重复计算次数，因此可以逐步检查答案在第几次迭代形成。

</div>
<div class="concept-item" markdown="1">

**词表读出与隐藏状态**

隐藏状态 $h$ 是模型内部的向量表示；词表读出将该向量映射为各候选词或答案的分数与排名。内部表示发生变化不一定会影响答案分数，因此必须分别测量状态空间和读出接口。

</div>
<div class="concept-item" markdown="1">

**组合点火**

本文用该词指正确答案在若干轮潜在计算后，于某一次迭代突然跨越判定阈值并保持稳定的现象。其关键可检验特征包括到达时间随推理深度变化、单步式的尖锐决议，以及到达后不再退出。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是按已发表配置与相同随机种子从头训练的独立 $30$M 参数循环深度推理器，训练数据为非语言的合成结构，以排除人类语料继承是该现象出现的必要条件。输入是具有不同组合或跳数复杂度 $k$ 的问题；模型经过多次循环迭代更新隐藏状态，并通过绑定的词表读出产生候选答案排名。研究同时记录两个观测通道：读出通道中的正确答案排名、决策边际及首次达到判据的迭代，以及状态通道中的相邻隐藏状态位移与方向变化。核心判别任务是确认“点火”是否具有随 $k$ 合法增长的到达时钟、单次迭代内的尖锐提交和到达后保持，并判断中间组合实体能否由同一词表接口恢复。由于论文强调读出接口可能构成而非仅观察最终决策，因此状态变化与读出变化不能被视为等价证据；各项判据在查看裁决数据前预注册，并以已知答案验证估计器。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$k$**

问题的组合深度或推理跳数；原文考察 $k=1$ 到 $10$。

</div>
<div class="notation-item" markdown="1">

**$h$**

某次循环推理迭代产生的隐藏状态向量。

</div>
<div class="notation-item" markdown="1">

**$\Delta h$**

相邻迭代之间的隐藏状态变化，其范数 $\|\Delta h\|$ 用于描述状态位移大小。

</div>
<div class="notation-item" markdown="1">

**$\|\Delta h\|$**

相邻隐藏状态差的向量范数，是论文状态通道采用的基本观测量之一。

</div>

</div>

**直接相关的工作**

- **本文所复现模型的参考论文**: 参考论文已表明首次命中答案的迭代会追踪分布内任务的跳数复杂度。本文在独立训练的实现上复现该规律，并进一步分析提交时的决策边际跳变、隐藏状态方向突变、提交后的径向且读出无效的运动，以及这些性质在训练过程中的形成；所给节选未提供参考论文题名。
- **Lu et al.**: 该工作没有在深度循环模型的答案排名轨迹中发现结构化潜在路径。本文报告中间实体同样无法通过绑定词表读出恢复，但认为仅观察排名会漏掉随难度计时的点火和隐藏状态的方向性提交；所给节选未提供论文题名。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

循环深度推理器通过多次内部迭代处理组合问题，因此研究者需要知道模型究竟在何时形成答案、该决定是否稳定，以及提交答案后仍在发生的隐藏状态变化是否具有计算意义。若不能把真正的决策形成与解码器效应、坐标尺度变化区分开，就可能错误解释模型的推理过程，也无法可靠比较不同训练阶段、模型实例或更大规模系统。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **词表读出或答案排名追踪**：在每次循环迭代后，使用模型自身的词表读出头解码隐藏表示，观察正确答案何时首次达到目标排名以及随后是否持续保持。该方法直接描述模型对外可见的决策，但单独使用时难以判断突变来自内部计算还是读出接口。
- **隐藏状态几何与速度分析**：比较相邻迭代的隐藏状态差异，例如状态位移、方向变化及径向与角向分量，以寻找与答案形成同步的内部动力学事件。本文特别区分原始隐藏空间和解码器的 LayerNorm 坐标，因为同一轨迹在不同归一化或坐标选择下可能呈现不同的速度特征。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有“组合点火”观察可能只来自单个已发布模型或单一读出通道，因而无法排除实现偶然性、训练轨迹差异和测量仪器造成的假象；若输出端和隐藏状态没有同步测量，就不能确定事件究竟发生在内部表示还是读出接口。
- 基于隐藏状态速度低谷的解释依赖坐标与归一化方式，尺度变化可能制造看似特殊的动力学信号；此外，若模型接触过人类语言数据，还无法判断点火签名是推理机制自行形成，还是从语言中的逐步推理模式继承而来。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一项受预注册标准约束的独立复现：它需要从头记录模型能力形成过程，在两个可能分化的同种子实例中检验完整签名，同时联合观测读出排名和隐藏状态，并以纯非语言合成训练排除语料继承。因而尚未确定组合点火是否可复现、是否代表真实而稳定的决策事件，以及它应被定位在隐藏计算、状态尺度还是模型读出接口。

</div>
<div markdown="1"><span>核心问题</span>

在循环深度推理器中，随任务组合深度推迟、随后突然且持续出现的答案解析，是否是一种真实且可复现的计算承诺；如果是，该事件主要体现于词表读出还是隐藏状态几何，并且在没有任何人类语言训练数据时是否仍会产生？

</div>
<div markdown="1"><span>作者直觉</span>

如果点火是真实的决策形成，而非某个曲线或坐标系制造的视觉效果，那么多种彼此独立的观测应在同一迭代附近汇合：更深的问题应更晚到达答案，答案排名应突然改善并保持，正确答案相对竞争答案的间隔应出现异常大的条件性跳变，而读出相关的隐藏状态方向应进入稳定区域。反之，仅改变隐藏状态长度却几乎不改变 logits 的后续运动，不应被解释为继续推理。独立重训、双通道测量和尺度不变性控制正好可以检验这种跨证据的一致性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文采用“独立复现＋双通道同步测量＋预注册判据”的方法，研究循环深度推理器在第几次迭代形成稳定答案，以及这一事件究竟发生在隐藏状态本身还是词表读出接口。作者按已发表配方从头训练一个约 $30$M 参数的循环深度 Transformer，并以参考模型的完整行为签名作为复现门槛；随后对不同推理跳数 $k$ 的样本执行固定迭代阶梯，在同一次前向传播中逐轮保存答案位置的隐藏状态 $h_r$，同时计算正确答案及经路径验证的中间实体在词表中的排名、正确答案决策边际、隐藏状态位移与方向变化。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 独立训练并进行整体验真

从头训练约 $30$M 参数、隐藏维度为 $768$、含四层循环块的循环深度 Transformer，课程训练推进至阶段 $21$；训练过程中按约每 $8$ 个 epoch 保存发展帧，并用预先冻结的整套行为签名检验其是否属于参考模型所代表的行为类别。

<div class="method-step__io" markdown="1">

**输入**：由 $200$ 个实体、$10$ 种关系和共 $2{,}000$ 条合成事实构成的封闭世界，以及参考工作的模型配置、随机种子和按跳数递增的课程训练配方。<br>
**输出**：一个独立生长的模型实现、跨训练阶段的检查点序列，以及是否通过复现门槛的判定。

</div>

**直观理解**：这一步不是直接下载原模型，而是依照同一“培养方案”重新训练一个模型，再检查它是否重现整组关键现象。这样可以区分可复现的计算规律与某个权重文件的偶然特征。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 固定迭代推理与双通道捕获

对每个样本运行固定长度的循环迭代，在最终循环块设置钩子，逐轮记录答案位置的隐藏状态 $h_r$；由同一批 $h_r$ 同步计算词表读出排名、前五候选边际、答案位置及全序列的状态位移。事件检测和状态测量并非统计独立，因为二者都是同一次前向传播中相同隐藏状态的确定性函数。

<div class="method-step__io" markdown="1">

**输入**：通过验真门槛的模型，以及具有不同关系跳数 $k$、答案和路径中间实体均可由合成世界精确验证的查询。<br>
**输出**：按样本、跳数和迭代 $r$ 对齐的词表排名轨迹、决策边际轨迹与隐藏状态轨迹。

</div>

**直观理解**：可以把模型的每轮循环看成连续拍摄的一帧：一台仪表观察“此时读出来的答案”，另一台仪表观察“内部状态怎样移动”。两台仪表看的是同一过程，因此可以直接比较读出变化与内部变化何时发生，但不能把它们当作相互独立的证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 定位提交事件并检验其时间结构

将正确答案首次达到词表排名 $1$ 的迭代定义为首次命中或提交时刻 $r^*$，再用首次命中时钟、带跑道限制的单步锐度和窗口内离开率分别检验到达时间是否随 $k$ 变化、转变是否集中于单次迭代、命中后是否保持。与此同时，按预注册排名标准检查路径中间实体是否曾经通过绑定词表读出显现，以区分静默组合与逐步外显的中继推理。

<div class="method-step__io" markdown="1">

**输入**：每个样本逐轮的正确答案排名及经真实路径验证的中间实体排名。<br>
**输出**：提交时刻 $r^*$、难度—到达时间关系、锐度与保持性统计，以及中间实体是否可读出的 relay 判定。

</div>

**直观理解**：这里把“第一次读出正确答案”当作接口上的提交点，然后问三个问题：更深的问题是否更晚提交、提交是否像开关一样突然、提交后答案是否稳定。再检查中间答案有没有依次出现在词表中，以判断模型是在内部静默组合，还是把每一步都写到可读接口。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 事件对齐的边际与状态几何分析

围绕 $r^*$ 计算正确答案相对最强竞争答案的有符号边际及单步跳变量，并与同一样本的非事件步、近阈值非事件步和回归基线比较；同时测量原始坐标与解码器坐标中的方向突变、提交后冻结，并把后续位移分解为沿状态尺度方向的径向分量和改变方向的切向分量。最后把径向分量重新送入真实读出，测定其对 logits 和排名的实际影响，从而判断持续状态运动是否基本属于读出不可见方向。

<div class="method-step__io" markdown="1">

**输入**：提交时刻 $r^*$、逐轮 logits、原始隐藏状态，以及经解码器 LayerNorm 变换后的坐标。<br>
**输出**：提交处的条件边际跳变量、非事件参照、方向突变与稳定化指标、径向／切向位移占比，以及读出不可见性的实测上界。

</div>

**直观理解**：排名从第二变第一本身必然伴随边际过零，因此过零不能证明出现了特殊计算；真正要比较的是这一步“跳得有多大”，以及普通的近阈值步骤是否也会这样跳。几何分解则类似把运动拆成“只把向量拉长”和“改变向量朝向”：LayerNorm 会大幅消除前一种变化，所以内部仍可移动，而读出的答案几乎不变。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 逐轮词表读出与排名

$$
z_r = W_U\,\mathrm{LN}(h_r),\qquad \rho_r(t)=\mathrm{rank}_t(z_r),\qquad r^*=\min\{r:\rho_r(y)=1\}
$$

**符号说明**

- $h_r$：第 $r$ 次循环后、答案位置的隐藏状态。
- $\mathrm{LN}(\cdot)$：解码器读出前使用的 LayerNorm 变换。
- $W_U$：将归一化隐藏状态映射到词表 logits 的绑定读出矩阵。
- $z_r$：第 $r$ 次循环产生的全词表 logit 向量。
- $\rho_r(t)$：词元 $t$ 在第 $r$ 次循环的词表排名，排名 $1$ 表示 logit 最大。
- $y$：样本的正确答案词元。
- $r^*$：正确答案首次达到排名 $1$ 的提交迭代。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把同一个隐藏状态转换成每个词元的分数，再确定正确答案第一次成为最高分候选的时刻。论文所谓提交或点火首先是一个读出接口事件；由于 $r^*$ 按排名 $1$ 定义，其对应边际由负变正是定义带来的事实，不能单独作为点火证据。<br>
**原文位置**：第 2 节“Substrate and instruments”；首次命中定义及其解释见第 3 节表 1说明与第 4 节。

</div>

</div>

<div class="equation-block" markdown="1">

#### 正确答案的有符号决策边际与提交跳变量

$$
m_r=z_r[y]-\max_{t\neq y}z_r[t],\qquad \Delta m_{r^*}=m_{r^*}-m_{r^*-1}
$$

**符号说明**

- $m_r$：第 $r$ 次循环中，正确答案 logit 减去最强错误候选 logit 的有符号边际。
- $z_r[y]$：第 $r$ 次循环时正确答案 $y$ 的 logit。
- $t$：词表中的候选词元；最大值仅在错误候选 $t\neq y$ 上取得。
- $\Delta m_{r^*}$：从提交前一轮到提交轮的单步决策边际变化。
- $r^*-1$：首次达到排名 $1$ 之前的迭代；只有 $r^*>0$ 的样本才具有该步。

<div class="equation-explanation" markdown="1">

**直观理解**：有符号边际衡量正确答案领先最强错误答案多少。因为提交被定义为正确答案第一次排名第一，$m_{r^*}$ 为正而前一步通常为负并不新鲜；方法上的关键是将 $|\Delta m_{r^*}|$ 与近阈值但未提交的普通步骤比较，判断提交是否对应异常大的连续读出变化，而不只是离散排名翻转。<br>
**原文位置**：第 3 节表 1“Margin geometry at the commit”说明；近阈值与回归参照见第 4 节。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文节选未给出训练损失的显式公式，只说明该模型严格复现参考工作的已发表训练配方：在由 $2{,}000$ 条合成关系事实构成的封闭世界中训练，并按推理跳数推进课程至阶段 $21$。因此不能从本文材料中可靠补写具体交叉熵形式、监督位置或优化器目标；本文的方法创新也不在提出新训练目标，而在独立训练一个同类推理器后，用预注册双通道仪器分析其提交动力学。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 循环深度 Transformer 推理底座**

模型约含 $30$M 参数，状态维度为 $768$，核心是四层循环块；同一计算块在深度方向反复作用，使第 $r$ 次循环产生状态 $h_r$。训练数据是纯非语言的合成关系世界，并按所需关系跳数逐步提高课程难度。

> 直观理解：普通 Transformer 通常为每层配置不同参数，而该模型反复使用同一个块进行更多轮思考。因训练材料不含人类语言，若仍出现类似“点火”的现象，就不能仅以语言语料中的心智描述来解释。

**2. 绑定词表读出与首次命中时钟**

每轮将答案位置状态先经 LayerNorm，再经绑定的词表矩阵 $W_U$ 映射为 logits，并据此计算正确答案及路径中间实体的排名。正确答案首次达到排名 $1$ 的迭代 $r^*$ 是事件锚点；所有时钟、锐度、保持性和事件对齐测量均使用预注册约定。

> 直观理解：该模块相当于每轮都向模型询问“如果现在必须回答，你会选什么”。它既能给出最终答案何时胜出，也能检查中间推理实体是否曾通过同一个公开出口出现。

**3. 原始／解码器坐标的状态几何仪器**

作者同时分析原始状态 $h_r$ 与解码器实际接收的 $\mathrm{LN}(h_r)$，测量相邻迭代的范数位移、余弦方向变化及提交后的方向稳定性；后续位移还被投影为径向与切向部分，并通过真实读出矩阵验证各分量对 logits 的影响。

> 直观理解：只看原始向量移动多远可能产生误导，因为读出前的 LayerNorm 会忽略大部分整体缩放。双坐标分析用于区分“模型内部数值仍在增长”和“真正会改变答案的方向仍在变化”。

**训练与推理**

训练阶段从相同配置与相同随机种子开始，但作者明确允许底层非确定性使训练轨迹分岔；模型能力与动力学按约每 $8$ 个 epoch 记录一次，现存档案从 epoch $328$ 开始，最早窗口因原文所述事件记录而缺失。训练完成或到达指定课程阶段后，先执行完整签名验真；只有通过参考类行为门槛的实现才进入主要分析。发展分析则在沿途检查点重复同一套仪器，以区分“已经会做题”与“已经形成快速、稳定提交动力学”两个阶段。

推理阶段不使用自适应停止，而是对每个查询运行固定迭代阶梯，并在最终循环块一次性捕获所有轮次的状态。每轮由 $W_U\mathrm{LN}(h_r)$ 得到词表分数，计算正确答案及路径中间实体的排名，并以 $r^*$ 对齐读出和状态轨迹；随后评估到达时钟、单步锐度、窗口保持、边际跳变、方向突变、提交后冻结及径向／切向位移。由于没有在 $r^*$ 前后强制提前退出或比较任务因果效果，本文只能定位并描述提交表面，不能证明该事件被模型的后续计算或停机机制功能性使用。

**复现信息**

公平解释结果所必需的约定包括：模型约 $30$M 参数、状态维度 $768$、四层循环块；合成世界含 $200$ 个实体与 $10$ 种关系，共 $2{,}000$ 条事实；训练按跳数课程推进至阶段 $21$。所有读数采用统一的 padded／eval-true 约定；快速解码路径在使用前被验证为逐字节一致；首次命中、带跑道限制的锐度、窗口离开率和分阶段状态位移估计器，均先在已知参考答案上复现参考类数值，再用于裁决数据。

预注册是方法的一部分：判据在相应数据产生前冻结，修改仅在参考侧进行版本记录。状态钩子与排名读出来自同一次前向传播，故双通道适合做时间对齐但不构成独立重复测量。状态几何必须区分原始坐标与 $\mathrm{LN}(h_r)$ 坐标；全序列平均会被填充位置稀释，因此方向突变的主要测量限定在答案位置。跨实现结论也被限制在同种子但非确定性分岔的两个实现，尚不能外推为跨独立随机种子的配方级不变性。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 主要任务是封闭的非语言合成事实世界，共含 $2{,}000$ 条事实，由 $200$ 个实体与 $10$ 种关系组成；问题按关系链跳数 $k$ 划分，课程训练推进至阶段 $21$。该数据用于隔离纯深度组合推理，并检验点火时钟是否随问题深度变化；它刻意排除了自然语言语料、干扰与绑定类任务。
- 事件级评估集合由能够在某次迭代首次达到正确答案排名第 $1$、且首次到达迭代 $r^*>0$ 的样本构成，共有 $274$ 个 event-eligible items。该集合用于测量提交前后一步的目标答案间隔变化；其中 $k=2$ 仅有一个合格样本，不能据此构造置信区间。
- 近阈值非事件控制集合包含 $71$ 个控制步骤，全部来自 $k=6$ 至 $10$，仅占全部非事件步骤的 $1.4\%$。它不是独立数据集，而是同一任务内的条件对照，用于判断提交时的间隔跳变是否大于普通的近阈值波动。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**首次命中、跑道限定锐度与窗口离开率**

首次命中记录正确答案第一次达到词表排名第 $1$ 的迭代；跑道限定锐度衡量在具有足够提交前轨迹的样本中，解决是否集中于单次迭代；窗口离开率衡量首次到达后是否又失去排名第 $1$。三者共同测试“随难度延迟、突然到达、到达后保持”的点火签名。 （首次命中本身没有统一的越高越好，其关键是随跳数 $k$ 呈规律增长；锐度越高表示提交越集中，离开率越低表示决策越稳定。）

</div>
<div class="metric-item" markdown="1">

**有符号目标间隔跳变**

目标间隔为正确答案 logit 减去所有错误 token 中最大 logit，即 $\mathrm{logit}(\mathrm{correct})-\max_{t\ne\mathrm{correct}}\mathrm{logit}(t)$；实验关注从提交前一步到提交步的间隔变化，并将其与同一样本中的近阈值非事件变化比较。由于排名第 $1$ 与正间隔等价，过零次数只是定义结果，真正有信息的是条件跳变幅度。 （在证明尖锐提交时，跳变幅度越大且越常超过非事件分布的高百分位越有力；但不能把提交点的符号过零本身当作额外证据。）

</div>
<div class="metric-item" markdown="1">

**隐藏状态方向与径向分解**

在答案位置测量相邻迭代隐藏状态 $h_r$ 的角度变化、提交后方向冻结，以及后续位移中径向分量的平方范数占比；再通过模型真实读出测量纯径向缩放对 logits 和排名的影响。这用于区分读出相关的方向提交与 LayerNorm 后近乎不可见的尺度运动。 （若主张方向提交，则到达步应出现较大的方向突变、提交后角步应迅速降低；若主张后续运动读出无关，则径向占比应更高且径向 logit 效应应更低。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 排名通道的难度时钟、单步解决与提交后保持

<div class="result-value" markdown="1">

首次命中中位数随跳数 $k=1$ 至 $10$ 从 $1$ 增至 $4$；跑道限定锐度为 $0.805$，区间为 $[0.714,0.867]$；各条件的窗口内离开率均不超过 $0.07$。这些指标满足作者预注册的 COHERENCE 标准，并在两个同种子但训练轨迹分歧的实现及两个课程阶段复现。

</div>

作者证据支持一种“难题更晚提交、提交集中在一步、之后保持”的真实读出事件，而不是排名曲线中的随机抖动。跨实现复现增强了排名规律的稳健性，但两个模型共享训练配方、配置和种子，且任务只覆盖一个合成事实世界，因此不能直接推出其他架构或自然语言任务也具有相同规律。

<div class="result-source" markdown="1">

来源：摘要；第3节 Findings（排名通道结果）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The rank-channel signature — arrival time rising lawfully with problem depth (first-hit median 1→4 across k=1–10), sharp single-iteration resolution (runway-qualified sharpness 0.805 ∈ [0.714, 0.867]), and arrive-and-hold stability (in-window departure ≤0.07 everywhere) — meets every pre-registered COHERENCE criterion and reproduces across two same-seed, chaotically divergent realizations of the training recipe at two curriculum stages.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 提交迭代的正确答案间隔跳变

<div class="result-value" markdown="1">

在 $274$ 个事件合格样本中，提交时的决策间隔在一次迭代内跳升 $5.8$ 至 $8.0$ logits；其中 $96\%$ 的事件跳变超过近阈值非事件步骤分布的第 $90$ 百分位。作者明确不把有符号间隔在提交点过零视为证据，因为首次排名第 $1$ 已在定义上蕴含正间隔。

</div>

该结果将“点火”具体化为读出界面的显著竞争优势跃迁，而不只是正确 token 恰好越过排名边界。与同样接近阈值的普通步骤相比，跃迁通常异常大；不过控制集合只有 $71$ 步且全部来自较深的 $k=6$ 至 $10$，所以该条件比较尚不能证明所有深度具有同样的效应分布。

<div class="result-source" markdown="1">

来源：摘要；第3节 Findings，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

What replaces it is sharper: at commitment the decision margin jumps 5.8–8.0 logits in a single iteration, exceeding the 90th percentile of near-threshold non-event steps in 96% of cases.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 答案位置的隐藏状态方向提交与提交后径向运动

<div class="result-value" markdown="1">

原始隐藏空间中的方向突变达到预注册标准；提交后的角步在八次迭代内由 $52.9^\circ$ 降至 $1.2^\circ$。后续位移的平方范数中有 $0.961$ 属于径向分量，而测得的径向 logit 影响不超过 $5.7\times10^{-6}$。但在解码器 LayerNorm 坐标中，到达步略低于预注册阈值，因此复合的解码器坐标主张未获确认。

</div>

方向变化会影响 LayerNorm 后的读出，因此提交时的“转向”与答案选择相关；此后隐藏状态仍可因长度增长而移动，但这种径向运动几乎不改变词表 logits，解释了为何表面上状态持续变化而答案已经稳定。结果支持“读出界面构成提交”，但不能声称所有坐标系都通过了预注册检验，也不能把状态几何当作跨训练实现完全一致的机制。

<div class="result-source" markdown="1">

来源：摘要；第3.3节（状态几何与归一化控制）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The hidden-state direction snaps in raw geometry, meeting its pre-registered criterion (in the decoder's LayerNorm coordinates it attenuates just below our bar, so the composite decoder-coordinate claim is not confirmed), and then freezes in both (descriptively so in decoder coordinates; angular steps 52.9 to 1.2 degrees over eight iterations), while subsequent displacement is predominantly radial (0.961 of squared-norm) and readout-null to a measured bound (radial logit effect <=5.7e-6).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 间隔跳变的近阈值零参照仅含 $71$ 个控制步骤，全部来自 $k=6$ 至 $10$，且只占非事件总体的 $1.4\%$；低跳数样本通常在一两步内提交，无法贡献同类控制。因此“$96\%$ 超过第 $90$ 百分位”是对该条件控制分布的结论，不能无条件推广到所有深度。
- 实验只覆盖一个约 $30$M 参数的循环深度模型类别、一个合成事实世界和纯深度组合任务；统计区间也以该世界为条件。隐藏状态几何对具体训练实现敏感，而整序列测量不显示答案位置的方向事件。推广到独立生成的事实系统、含干扰或绑定的任务、自然语言模型及更大规模模型，都需要重新训练或额外评估。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 已发布的参考模型及其参考类统计：作者按相同配置与随机种子从头训练独立实现，并在查看裁决数据前，用预注册的“完整签名门”及估计器复现来验证实现忠实度。这一比较用于排除点火仅是单次实现偶然现象，但相同种子并不等于完全独立的训练配方。
- 两个同种子但因非确定性而产生不同训练轨迹的模型实现：比较它们在两个课程阶段的排名通道签名，检验规律是否对训练轨迹的混沌分歧稳健；隐藏状态盆地几何则允许保留实现特异性。
- 样本内部的近阈值非事件步骤：使用与事件步骤相同的有符号目标间隔变化作为零参照，并以控制分布的第 $90$ 百分位为阈值。该基线比任意固定 logit 阈值更有意义，因为它控制了样本和测量量本身。
- 绑定词表读出的中间实体排名：将经图上路径验证的中间实体是否满足预注册排名标准作为“显式中继”对照，用于判断模型是否通过可读出的语言式中间步骤完成组合。

**实验想回答的问题**

- 所谓“组合点火”是否反映循环深度模型中的真实计算事件，而非词表读出、测量坐标或语言训练语料造成的假象？具体检验其到达时间是否随推理跳数增加、是否在单次迭代内形成稳定决策，以及该现象能否跨独立训练实现复现。
- 决策提交发生在何处、以何种几何形式出现？实验同时观察词表读出与隐藏状态，区分读出可见的方向变化和读出近乎不可见的径向运动，并检查中间推理实体是否曾通过绑定词表读出显现。

**实验实现**

模型为约 $30$M 参数的循环深度 Transformer，隐藏状态维数为 $768$，循环块含 $4$ 层。作者依照已发表配方并使用相同种子从头训练，在每个样本的一次前向传播中钩取最终块，因此排名事件与状态测量都是同一组 $h_r$ 的确定性函数，而不是相互独立的证据：排名通道计算 $\mathrm{rank}(W_U\mathrm{LN}(h_r))$，状态通道记录 $\lVert h_r\rVert$ 与 $\lVert h_{r+1}-h_r\rVert$。评估统一采用 padded/eval-true 约定，快速解码路径在使用前经逐字节一致性验证；首次命中、锐度、离开率和分阶段状态变化估计器均先在已知答案的参考统计上验证。判据在裁决数据产生前冻结，并以约每 $8$ 个 epoch 的分辨率记录训练发展；但最早训练窗口早于现存的 epoch $328$ 档案。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 原始隐藏坐标与解码器 LayerNorm 坐标的预注册归一化控制 | 原始几何中的方向突变通过预注册标准，但 LayerNorm 坐标中的到达步略低于预注册阈值，因此作者撤回早先的“速度低谷”解释，并明确不确认复合的解码器坐标主张。 | 该控制隔离了坐标尺度对状态速度的影响：若一种事件只在未归一化坐标中出现，就可能来自状态范数变化而非读出相关计算。结果保留了原始空间的方向突变和提交后冻结，却否定把速度低谷当作坐标不变机制证据，展示了预注册控制对结论边界的实质影响。 | 摘要；第3.3节<br><span class="experiment-evidence">A preregistered scale-invariance check rejected our earlier velocity-trough interpretation (Section 3.3).</span> |
| 答案位置测量与整段填充序列平均测量 | 在整段填充序列上，方向位移的事件前比值为 $0.87$，而答案位置为 $1.62$；原始 $\lVert\Delta h\rVert$ 的提交后/提交前比值分别为 $0.85$ 与 $1.99$。不过提交后方向冻结在两种测量中均存在，其方向位移提交后/提交前比值分别为 $0.06$ 与 $0.02$。 | 该位置消融说明方向提交集中在产生答案的位置；把大量 padding 和其他位置平均进去会稀释甚至反转幅度信号。与此同时，两种范围都观察到提交后方向冻结，表明稳定化并非完全由答案位置选择制造。它也限制了结论：不能把答案位置的尖锐事件概括成全序列同步发生的状态突变。 | 第7节 Limitations and future work<br><span class="experiment-evidence">The snap is answer-position-specific: measured over the whole padded sequence the directional event does not appear ((1−cos) displacement event/pre 0.87 vs 1.62 at the answer position) and raw ‖Δh‖ post/pre inverts (0.85 vs 1.99), as expected when the commit position is averaged against padding; the post-commit directional freeze appears in both ((1−cos) displacement post/pre 0.06 and 0.02).</span> |

**定性案例**

- 发展轨迹记录构成一个定性案例：模型首先获得答题能力，随后才逐步形成“到达后保持”等稳定决策签名。作者据此解释点火不是能力初现时自动附带的性质，而是训练路线后期塑造的读出动力学；但现有冻结阶段对照存在混杂，因此这仍是发展顺序证据，而非训练阶段的严格因果识别。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It mechanistically analyzes how a recurrent-depth latent reasoner reaches and represents discrete commitments during iterative reasoning.; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`2fbb30947d9e01822e23fb8ca655f56008087f8ad54fae24e02455acbbf305e5`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
