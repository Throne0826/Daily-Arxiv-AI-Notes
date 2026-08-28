---
title: "[论文解读] TTPO: Test-Time Policy Optimization"
description: "[arXiv 2608.27448][对齐 / RLHF] 原文未明确报告。"
arxiv_id: "2608.27448"
announcement_date: "2026-08-28"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:35:16.231791+00:00"
source_sha256: "852d4ee475762b8d88f5134b44976611e97be715fd6e73bd4557725c1fd0ae2d"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "强化学习"
  - "测试时训练"
  - "大语言模型数学推理"
  - "多数投票伪标签"
  - "在策略自蒸馏"
  - "GRPO"
  - "词元级选择"
  - "伪标签噪声"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.27448</p>

# TTPO: Test-Time Policy Optimization

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Aozhe Wang, Zhengxi Lu, Jianze Wang, Shangke Lv, Ying Liu, Weiming Lu, Jun Xiao, Yueting Zhuang, Hua Yang, Qianglong Chen, Yongliang Shen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Zhejiang University；Affiliation: Alibaba Group</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27448v1) · [PDF 下载](https://arxiv.org/pdf/2608.27448v1) · **关键词** 测试时训练, 大语言模型数学推理, 多数投票伪标签, 在策略自蒸馏, GRPO, 词元级选择, 伪标签噪声<br>
**代码**: [https://github.com/ZJU-REAL/TTPO](https://github.com/ZJU-REAL/TTPO)

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

本文位于大语言模型数学推理的测试时训练领域。常规后训练依赖带标准答案的数据：可验证奖励强化学习用答案判定整条推理轨迹是否正确，但只提供序列级的粗粒度信号；在策略自蒸馏则让同一模型在获得标准答案这一特权信息后充当教师，对模型自身生成的轨迹提供逐词元监督。测试时训练要求模型直接利用无标签测试题更新自身，因此上述两类方法失去了标准答案来源。现有办法通常对同一道题采样多条推理轨迹，以多数答案作为伪标签，但竞赛级难题上的多数投票可能频繁出错，使序列级强化学习强化错误答案，并使逐词元蒸馏在整条轨迹上放大伪标签噪声。TTPO所研究的核心问题是：如何只利用模型自身采样及其多数共识，在无真实标签条件下获得既细粒度又能容忍错误伪标签的训练信号。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试时训练（Test-Time Training, TTT）**

模型在部署或测试阶段直接使用当前无标签测试数据更新参数，并继续解决这些测试问题。这里不假设训练后会得到标准答案，因此监督只能由模型自身的预测结构产生。

</div>
<div class="concept-item" markdown="1">

**可验证奖励强化学习与GRPO**

可验证奖励强化学习根据最终答案是否正确，为整条推理轨迹分配奖励；GRPO通过比较同一问题的一组采样轨迹来形成相对优势并优化策略。其局限是一个序列级信号通常会影响轨迹中的所有词元，难以指出具体哪一步推理有误。

</div>
<div class="concept-item" markdown="1">

**在策略自蒸馏（On-Policy Self-Distillation, OPSD）**

学生模型先从当前策略采样轨迹，再由获得答案条件的同一模型充当教师，逐词元重新评估这些轨迹并提供密集监督。它不需要独立教师模型，但传统形式仍需要真实答案作为教师的特权上下文。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一批没有标准答案的数学测试题。对每道题，当前语言模型生成一组包含推理过程与最终答案的采样轨迹，并把出现次数最多的最终答案视为伪标签；轨迹随后按其答案是否与伪标签一致分为两组。目标是在不访问任何真实标签的前提下更新模型策略，使其输出更准确的推理和答案：一致轨迹可向伪标签条件下的教师学习细粒度词元信息，不一致轨迹则接受基于组内比较的负向强化学习信号。问题的关键假设不是“多数答案通常正确”，而是原文观察到的非对称性：即使多数伪标签错误，与它不一致的轨迹也大多仍是错误轨迹，因此“排除某条不一致轨迹”通常比“把伪标签当成正确答案”更可靠。该设定同时要求处理轨迹内部的信用分配，因为失败轨迹并非每个词元都错，而蒸馏轨迹中也有许多位置已经被学生掌握。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

一条无标签数学测试题或提示。

</div>
<div class="notation-item" markdown="1">

**$y_i$**

模型针对题目$x$采样得到的第$i$条推理轨迹及其最终答案。

</div>
<div class="notation-item" markdown="1">

**$\hat{a}$**

同一题多条采样轨迹的最终答案经多数投票得到的伪标签。

</div>
<div class="notation-item" markdown="1">

**$\pi_\theta$**

参数为$\theta$、在测试时接受优化的语言模型策略。

</div>

</div>

**直接相关的工作**

- **TTRL（Zuo et al., 2026）**: TTRL同样面向无标签推理测试时训练：它对每题采样多条轨迹，以多数投票构造伪奖励，再使用GRPO更新模型。它建立了本文最直接的任务基线，但监督仍是整条轨迹共享的单一序列级标量；多数投票错误时还可能直接强化错误答案。
- **OPSD（Zhao et al., 2026）**: OPSD让同一策略在获得真实答案条件后成为教师，对自身采样轨迹实施逐词元蒸馏，弥补序列级奖励缺乏局部监督的问题。它构成TTPO一致轨迹分支的技术基础，但原始方法依赖真实答案，直接改用错误伪标签又会让受污染教师在每个词元上传播错误。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

数学推理大语言模型通常依赖带标准答案的强化学习或在真实答案条件下的在策略自蒸馏，但测试时训练（$\mathrm{TTT}$）的目标正是让模型在面对新题时自我改进，而这些题目通常没有可用标签。因此，研究需要一种仅利用模型自身生成结果、同时还能提供序列级和令牌级学习信号的无标签训练方法。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于可验证奖励的强化学习（RLVR）及无标签伪标签强化学习**：有标准答案时，RLVR根据最终答案是否正确为整条推理轨迹提供奖励；在无标签场景中，TTRL等方法先对同一道题采样一组回答，再以多数答案作为伪标签，并把是否与该伪标签一致转化为奖励。其优点是训练目标不需要人工标签，但监督仍主要是每条轨迹一个标量。
- **在策略自蒸馏（OPSD）及其伪标签变体**：OPSD把正确答案作为额外条件输入教师模型，使教师对学生自身生成轨迹逐令牌重新评分，再提供密集的令牌级蒸馏信号。无标签变体以多数投票答案替代标准答案，尝试对全部轨迹，或仅对与伪标签不一致的轨迹进行蒸馏。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有RLVR和OPSD都依赖标准答案：前者需要答案验证奖励，后者需要答案作为教师的条件输入，因此不能直接用于没有标签的测试时训练。
- 多数投票伪标签并不可靠；原文报告在竞赛级题目上约$85\%$的提示词对应错误伪标签。若把伪标签直接用于蒸馏，错误答案会进入教师并在每个令牌位置传播错误；若仅使用伪标签作为轨迹奖励，则监督仍然稀疏，且错误投票可能系统性强化错误推理。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究缺少一种能够在多数投票经常错误时，区分可靠正向信号与可靠负向信号的无标签目标。具体而言，尚未解决的问题是：如何利用与伪标签一致的轨迹进行密集学习，同时避免把错误伪标签当作正确答案；又如何利用不一致轨迹，而不必知道伪标签本身是否正确。

</div>
<div markdown="1"><span>核心问题</span>

在没有任何标准答案的测试时训练中，能否根据模型生成轨迹与多数投票伪标签之间的关系，分别构造安全的正向蒸馏和负向强化学习信号，并通过令牌级选择降低错误监督，从而稳定提升数学推理能力？

</div>
<div markdown="1"><span>作者直觉</span>

作者观察到伪标签错误时，错误主要集中在“投票答案本身”，但“不一致”这一事实仍包含信息：原文称约$79\%$的反对伪标签的轨迹即使在伪标签错误时也确实是错误的，所以惩罚不一致轨迹通常仍然合理。由此，TTPO不把所有轨迹都蒸馏到伪标签，而是将一致轨迹用于OPSD蒸馏、将不一致轨迹用于Grouped RL惩罚；前者学习模型已经产生的答案条件下的有效思考方式，后者只利用“不一致”这一关系而不直接相信伪标签的答案。进一步地，蒸馏分支降低已经学会位置的权重，强化学习分支只惩罚模型高置信度却出错的位置，使两类更新都更集中于真正需要修正的部分。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TTPO面向无真实标签的测试时训练：给定测试问题集合，当前策略模型对每题采样多条推理轨迹，并以最终答案的多数簇作为伪标签。随后按照轨迹是否与伪标签一致进行非对称更新：一致轨迹进入OPSD分支，由注入伪答案的同模型教师提供逐词分布监督；不一致轨迹进入GRPO分支，以负的组相对优势削弱错误轨迹。两条分支分别使用词元加权与词元掩码，避免把梯度浪费在已经学会的位置，或误伤失败轨迹中局部正确的推理步骤。

其核心不是假设多数答案一定正确，而是控制错误伪标签的影响范围。若伪标签错误，直接对全部轨迹做蒸馏会让错误答案影响每个样本；TTPO只对与该答案一致的小集合做条件蒸馏，而对不一致集合仅利用“它不属于多数簇”这一相对信号施加选择性惩罚。直观地说，模型先用集体投票形成暂时答案，再分别“学习支持票中有价值的推理”和“抑制反对票中最可疑的步骤”，训练后重新采样并投票，使伪监督质量随模型能力共同提升。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多数投票与轨迹路由

从$π_θ(\cdot\mid x)$采样$K$条轨迹$\{y_k\}_{k=1}^{K}$，提取答案$a_k$并按数学等价性聚类；最大答案簇给出伪标签$\hat a$，一致索引形成正集合$\mathcal P$，其余形成负集合$\mathcal N$。

<div class="method-step__io" markdown="1">

**输入**：无标签问题$x$、当前策略$π_θ$以及每题采样数$K$。<br>
**输出**：伪标签$\hat a$、共识计数$c$、正轨迹集合$\mathcal P$与负轨迹集合$\mathcal N$。

</div>

**直观理解**：把同一题的多次作答看成一次班级投票，但不把多数票视为绝对真理；投票主要用于决定两类样本应接受哪一种更新。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 同模型教师与学生前向计算

教师分布为$q_t^{(\hat a)}=\pi_θ(\cdot\mid[x;\hat a]_{\mathrm{teacher}},y_{<t})$并停止梯度，学生分布为$p_t=\pi_θ(\cdot\mid x_{\mathrm{student}},y_{<t})$并保留梯度；二者读取相同完成前缀，仅教师额外看到答案提示。

<div class="method-step__io" markdown="1">

**输入**：问题$x$、伪标签$\hat a$、轨迹前缀$y_{<t}$及共享参数$θ$。<br>
**输出**：每个位置$t$上的教师分布$q_t^{(\hat a)}$和学生分布$p_t$。

</div>

**直观理解**：这不是另训一个更大教师，而是让同一模型在“提前知道暂定答案”时充当指导者；学生必须在看不到答案的情况下模仿其推理分布。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 正样本的加权OPSD蒸馏

以正向KL散度$\mathrm{KL}(q_t^{(\hat a)}\|p_t)$进行逐词蒸馏，并根据归一化学生熵$\hat H(t)$和归一化师生差异$\hat\Delta(t)$设置权重$w(t)=\hat H(t)+\hat\Delta(t)-\hat H(t)\hat\Delta(t)$；只有两种信号都低时，位置权重才接近零。

<div class="method-step__io" markdown="1">

**输入**：正集合$\mathcal P$中每条轨迹的教师分布$q_t^{(\hat a)}$、学生分布$p_t$及有效长度$T_k$。<br>
**输出**：正分支损失$\mathcal L_{\mathrm{OPSD}}$。

</div>

**直观理解**：学生不确定，或学生虽然自信却与教师不同，都说明该词值得学习；已经自信且与教师一致的词不必反复训练。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 负样本的掩码GRPO惩罚

按答案是否匹配$\hat a$赋予奖励并计算组相对优势，使负轨迹满足$A_k<0$；再用$s(t)=-\log p_t(y_k^{(t)})(1-\hat H(t))$排序，只保留得分不低于轨迹中位数的前50%词元，即$m(t)=1$的位置。

<div class="method-step__io" markdown="1">

**输入**：负集合$\mathcal N$、每组$K$条轨迹的二元奖励、学生生成概率及词元熵。<br>
**输出**：仅作用于可疑词元的负分支损失$\mathcal L_{\mathrm{GRPO}}$。

</div>

**直观理解**：整条答案失败不代表其中每一步都错，因此方法不删除整段推理，而是重点压低那些“生成概率低、模型却相对确定”的异常词元。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 正、负分支的样本级损失

$$
\begin{aligned}
\mathcal{L}_{\mathrm{OPSD}}(k)&=\frac{1}{T_k}\sum_{t=1}^{T_k}w(t)\,\mathrm{KL}\!\left(q_t^{(\hat a)}\,\|\,p_t\right),\quad k\in\mathcal P,\\
\mathcal{L}_{\mathrm{GRPO}}(k)&=-\frac{A_k}{T_k}\sum_{t=1}^{T_k}m(t)\log\pi_\theta\!\left(y_k^{(t)}\mid x,y_k^{(<t)}\right),\quad k\in\mathcal N.
\end{aligned}
$$

**符号说明**

- $\mathcal{L}_{\mathrm{OPSD}}(k)$：第k条正轨迹的在线策略自蒸馏损失
- $\mathcal{L}_{\mathrm{GRPO}}(k)$：第k条负轨迹的组相对策略优化损失
- $T_k$：第k条轨迹参与训练的有效响应词元数
- $w(t)$：正分支第t个词元的学习价值权重
- $q_t^{(\hat a)}$：额外条件化于伪标签的停止梯度教师分布
- $p_t$：不读取伪标签且参与梯度更新的学生分布
- $A_k$：同题多条轨迹之间计算的组相对优势；负样本的该值小于零
- $m(t)$：负分支的二元词元掩码，取1表示该位置接受惩罚
- $y_k^{(t)}$：第k条轨迹在位置t实际生成的词元
- $\pi_\theta$：参数为θ的语言模型策略

<div class="equation-explanation" markdown="1">

**直观理解**：第一行让学生在有学习价值的位置逼近“知道暂定答案”的教师完整概率分布，因此比只监督实际输出词元更细粒度。第二行利用$A_k<0$降低负轨迹中被掩码选中的词元概率，但不把整条失败轨迹的所有位置一并处罚。<br>
**原文位置**：第3.3节公式(3)与第3.4节公式(5)

</div>

</div>

<div class="equation-block" markdown="1">

#### TTPO统一目标

$$
\mathcal{L}_{\mathrm{TTPO}}=\frac{1}{|\mathcal B|}\left(\sum_{k\in\mathcal P}\mathcal{L}_{\mathrm{OPSD}}(k)+\lambda\sum_{k\in\mathcal N}\mathcal{L}_{\mathrm{GRPO}}(k)\right)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{TTPO}}$：TTPO在当前批次上的总训练目标
- $\mathcal B$：当前训练批次，分母用于批量归一化
- $\mathcal P$：最终答案与多数投票伪标签数学等价的轨迹索引集合
- $\mathcal N$：最终答案与多数投票伪标签不等价的轨迹索引集合
- $\lambda$：GRPO负分支相对于OPSD正分支的损失权重

<div class="equation-explanation" markdown="1">

**直观理解**：该目标把两类性质不同的监督信号合并：正样本提供逐词分布模仿，负样本提供选择性反向压力。$\lambda$用于避免数值规模更大的GRPO梯度压过蒸馏梯度，而不是表达两类样本数量的比例。<br>
**原文位置**：第3.5节公式(8)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：每轮训练先用当前$π_θ$产生伪标签和正负划分，再在同一批轨迹上计算两类损失。对$k\in\mathcal P$，最小化加权前向KL，使无答案提示的学生分布逼近答案条件教师；对$k\in\mathcal N$，由于$A_k<0$，最小化GRPO项会降低被$m(t)$选中的实际生成词元概率。最终采用$∇_θ(\mathcal L_{\mathrm{OPSD}}+λ\mathcal L_{\mathrm{GRPO}})$更新学生参数，教师前向停止梯度但与学生共享当前模型参数。

两分支必须做尺度平衡：原文指出未加权GRPO损失约比OPSD前向KL大一个数量级，因此引入$\lambda$。附录表8在$\lambda\in\{0.01,0.05,0.1,0.15,0.2\}$中报告$\lambda=0.1$最好；过小会使负样本抑制不足，过大则让粗粒度惩罚主导蒸馏。该结论来自特定的Qwen3-1.7B与OpenThoughts设置，不应在其他模型或批量构成下未经验证地视为固定最优值。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 基于多数簇的非对称路由**

答案先按数学等价性聚类，而非仅按字符串相等；与最大簇答案$\hat a$一致的轨迹使用前向KL蒸馏，不一致轨迹使用负优势GRPO。该设计把伪标签内容直接进入梯度的范围限制在$\mathcal P$，而$\mathcal N$分支只依赖“不属于多数簇”的判别。

> 直观理解：若投票答案错了，支持该错误答案的样本可能被误教，但系统不会再强迫所有不同答案都模仿它，从而缩小一次错误投票的破坏范围。

**2. 正分支的Soft-OR词元加权**

对每条正轨迹分别计算学生熵$H(t)$与师生KL差异$\Delta(t)$，经样本内最小—最大归一化得到$\hat H(t)$和$\hat\Delta(t)$，再以Soft-OR组合为$w(t)$。高熵表示学生尚不确定，高差异表示教师和学生尚未对齐，两者任一较高即可保留较强蒸馏梯度。

> 直观理解：它把训练预算放在“还不会”或“学偏了”的词上，而不是平均复习所有词。

**3. 负分支的异常词元掩码**

词元得分由未归一化负对数概率$-\log p$乘以归一化确定性$1-\hat H(t)$构成，并在每条轨迹内按中位数选取前50%。未归一化$-\log p$作为主要排序尺度，使通常具有高生成概率的局部正确词元更容易被排除。

> 直观理解：失败答案里可能包含正确公式和有效中间步骤；掩码只惩罚最像异常输出的一半位置，减少对这些局部正确内容的连带伤害。

**训练与推理**

训练阶段，对每个无标签问题重复执行“采样$K$条轨迹—提取并聚类答案—形成$\hat a$、$\mathcal P$和$\mathcal N$—教师/学生前向—计算双分支损失—更新$θ$”。伪标签不是预先固定的数据标注，而是在迭代中由最新策略重新生成；因此模型改善后，轨迹质量和多数投票质量也可能改善，形成自举式测试时优化。原文还区分在外部训练问题上进行的无标签训练与直接在待测题目上进行的TTT，但二者使用相同目标，主要差别是问题集合是否就是最终测试集合。

推理阶段不需要答案条件教师、投票路由或损失计算，直接用更新后的$π_θ(\cdot\mid x)$生成答案即可。论文也在关闭thinking mode时评估学生，以检验训练期间thinking教师的推理能力是否已迁移到普通生成分布；这属于评估设置，而不是TTPO目标要求的额外推理模块。

**复现信息**

复现时最关键的细节有四项。第一，最终答案需按数学等价性聚类，不能简单比较字符串，否则等值表达会被错误分到$\mathcal N$。第二，教师与学生使用相同完成词元和相同模型参数，但教师提示额外注入$\hat a$且停止梯度；正分支的$H(t)$与$\Delta(t)$按单条样本做最小—最大归一化。第三，负分支在每条轨迹内部按$s(t)$的中位数保留前50%词元，而非使用跨批次固定阈值。

第四，原文的补充消融表明训练子集采用固定50/50正负构成、并优先选择较短完成时表现最好；作者解释其实现最多只有前1,024个词元参与梯度，短轨迹能让该窗口覆盖更完整的关键推理。上述子集策略和1,024词元限制会影响结果解释，但所给节选未明确报告完整的$K$、$K_{\mathrm{train}}$、学习率$\eta$、批量大小、采样温度或训练步数，因此这些值不能从当前材料中补造。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 竞赛数学基准套件：AIME 2025、AIME 2026、HMMT 2025、HMMT 2026 和 BRUMO 2025。它们共同用于检验高难度数学推理能力；原文摘录未明确报告各数据集规模及训练/测试划分细节。在 OpenThoughts 设置中，模型在有标签数据上训练，但 TTPO 不读取标签；标签只用于监督基线和比较。
- 测试时训练（TTT）数据：直接在相应测试集上进行无标注训练，用于检验模型能否在部署阶段仅利用自身生成结果完成适应。原文摘录未明确报告每个测试集用于 TTT 的题目数量，也未说明是否另设独立验证集。
- AIME 2026：除参与总体评测外，还用于 Qwen3-1.7B 的训练动态分析，以比较多数投票路由、真实答案路由、OPSD（Leakage）和 OPSD-TTT 的损失变化。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Avg@12**

在温度 $1.0$ 下对每道题进行多次随机生成，并汇总 $12$ 次生成的平均正确表现，用于衡量策略在采样推理时的预期解题能力。摘录未给出其更细的计算公式。 （越高越好，因为更高数值表示随机采样得到正确答案的平均概率或平均正确率更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### OpenThoughts 设置：五个竞赛级数学基准上的无标签 TTPO 与标签监督 OPSD 对比

<div class="result-value" markdown="1">

作者声称，TTPO 在不使用任何答案标签的情况下，在五个竞赛级基准上达到标签监督 OPSD 的整体水平。

</div>

这表明多数投票形成的自监督信号可能替代真实答案所提供的路由信息，而且没有明显牺牲总体数学性能。由于所给摘录未包含表 1 的逐数据集数值、误差范围或重复实验结果，该结论应理解为作者报告的总体匹配关系；它不能证明 TTPO 在每个数据集、每个模型规模上都不低于 OPSD，也不能排除峰值检查点选择带来的影响。

<div class="result-source" markdown="1">

来源：Abstract；第 4.2 节表 1 的标题在摘录中出现，但具体表格行未提供

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Without any labels, TTPO matches label-supervised OPSD on five competition-level benchmarks, raises Qwen3-1.7B from 38.0% to 45.2% in TTT, yields +25.2% to +36.4% without thinking, and shows strong cross-task generalization.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-1.7B 的测试时训练（TTT）

<div class="result-value" markdown="1">

作者报告 TTPO 将 Qwen3-1.7B 的表现从 $38.0\%$ 提升到 $45.2\%$，绝对提升为 $7.2$ 个百分点。

</div>

该结果直接测试模型能否在测试集上不读取人工标注、仅依靠自身采样和投票实现适应。它支持 TTPO 在小规模模型上的测试时优化有效，但摘录没有说明这两个数值对应哪些基准的平均值、基线检查点如何确定，以及是否具有统计显著性，因此不能据此推断所有模型规模或所有测试集均有同等幅度的提升。

<div class="result-source" markdown="1">

来源：Abstract；第 4.2 节 Main Results，具体结果表未包含在所给摘录中

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Without any labels, TTPO matches label-supervised OPSD on five competition-level benchmarks, raises Qwen3-1.7B from 38.0% to 45.2% in TTT, yields +25.2% to +36.4% without thinking, and shows strong cross-task generalization.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 关闭思考模式的评测

<div class="result-value" markdown="1">

作者报告，在非思考模式下，TTPO 带来 $25.2\%$ 至 $36.4\%$ 的提升。

</div>

这一结果检验训练时从思考模式教师获得的知识能否转移到不显式展开长推理的推断方式。较大增益意味着训练可能改善了模型内部的解题策略，而不只是让模型生成更长的推理文本。不过原文摘要未明确这些百分比是相对提升还是绝对百分点，也未给出对应模型、数据集和基线，因此不能将该区间直接解释为所有非思考评测上的统一绝对增益。

<div class="result-source" markdown="1">

来源：Abstract；附录 D.2，表 7 的标题在摘录中出现，但具体表格行未提供

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Without any labels, TTPO matches label-supervised OPSD on five competition-level benchmarks, raises Qwen3-1.7B from 38.0% to 45.2% in TTT, yields +25.2% to +36.4% without thinking, and shows strong cross-task generalization.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给材料省略了表 1、表 7 及其他主要结果表的具体行，因此无法核验各模型、各数据集和各基线的完整分数，也无法判断摘要中的非思考提升区间是绝对提升还是相对提升；相关结论仍需对照原表复核。
- 实验报告每种方法训练过程中的峰值检查点，且 TTPO/OPSD 与 GRPO/TTRL 使用不同训练步数；摘录未报告多随机种子均值、方差、显著性检验或统一计算预算，因此结果足以说明可达到的性能，但不足以严格比较稳定性、样本效率和计算效率。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- OPSD：使用真实答案标签的在线策略自蒸馏。它是最直接的监督上界式对照，用于判断无标签 TTPO 能否接近依赖正确教师信息的蒸馏方法。
- GRPO：使用真实答案奖励的分组强化学习。它用于区分 TTPO 的收益究竟来自强化学习更新本身，还是来自多数投票路由、蒸馏分支与强化学习分支的组合。
- TTRL：通过多数投票奖励实施无标签强化学习。它与 TTPO 使用相近的无标签信息来源，因此可检验 TTPO 的非对称蒸馏与负样本惩罚设计是否优于直接将投票结果当作奖励。
- OPSD-TTT：使用模型在思考模式下、温度为 $0$ 的输出作为特权教师信息进行测试时自蒸馏。它用于比较 TTPO 的多轨迹投票监督与单个确定性教师输出之间的差异。

**实验想回答的问题**

- 在完全不使用人工答案标签的条件下，TTPO 能否仅凭多数投票伪标签，在竞赛级数学推理上达到依赖真实标签的 OPSD 或 GRPO 的性能，并优于已有无标签方法 TTRL 与 OPSD-TTT？
- TTPO 的多数投票路由与非对称训练设计是否能在困难题、伪标签可能错误以及关闭思考模式等条件下保持有效训练信号和性能收益？

**实验实现**

实验使用 Qwen3-1.7B、Qwen3-4B 和 Qwen3-8B，并在所有线性层上采用 LoRA 微调，秩为 $r=64$、缩放参数为 $\alpha=128$。主要评测开启思考模式；非思考模式结果另置于附录 D.2。OPSD 与 TTPO 训练 $100$ 步，每 $25$ 步保存检查点并报告其中峰值；GRPO 与 TTRL 训练 $500$ 步并报告全部检查点中的峰值。该“最佳检查点”协议反映训练期间可达到的最高表现，而不是固定训练步数下的最终表现。

TTPO 对每题采样 $K=64$ 条轨迹，以提高困难题上多数投票的稳定性，最大生成长度为 $16000$ 个 token；随后选择 $K_{\mathrm{train}}=8$ 条轨迹参与梯度更新，其中赞同伪标签和反对伪标签的轨迹各占一半。赞同分支接受 OPSD 式蒸馏，反对分支接受分组强化学习惩罚，强化学习权重为 $\lambda=0.1$。这些配置意在保证两类样本都能进入更新，而不是让数量占优的投票结果完全支配训练。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| AIME 2026 上 Qwen3-1.7B 的路由信号消融：TTPO 使用真实答案路由与使用多数投票伪标签路由 | 真实答案路由版本的损失几乎不下降，并经常停滞在接近 $0$；多数投票版本则在训练过程中保持稳定且明显的损失下降。 | 该对比隔离了“用什么答案划分正负轨迹”这一因素。困难题中若按真实答案路由，正确轨迹集合 $\|\mathcal{P}_{\mathrm{GT}}\|$ 可能接近 $0$，蒸馏分支没有正样本，而负样本的标准化优势也趋近 $0$，导致两个分支同时缺少梯度。多数投票保证赞同集合非空，因此能维持更新。需要注意，损失下降只说明优化信号更活跃，不等价于最终正确率必然更高；摘录也未给出该图的具体坐标值。 | 附录 D.1，Figure 7<br><span class="experiment-evidence">The most striking observation is that TTPO w/ GT exhibits dramatically weaker training signal than all other methods: its loss barely decreases and frequently stagnates near zero.</span> |
| 多数投票路由相对于真实答案路由的训练活性分析 | 作者报告，在困难 AIME 题目上，当 $\|\mathcal{P}_{\mathrm{GT}}\|\approx 0$ 时，真实答案路由会使两个训练分支同时缺少信号；投票路由则因始终形成非空共识而保持两个分支活跃。 | 这一分析解释了一个看似反直觉的结果：即使真实答案本身完全可靠，用它划分轨迹也可能因为模型暂时生成不出正确答案而无法学习；多数投票虽然可能选错答案，却能提供足够密集的相对监督。该结论支持 TTPO 的路由机制，但它主要验证训练信号是否存在，并未单独量化伪标签错误率与最终准确率之间的因果关系。 | 附录 D.1，Figure 7；理论依据见附录 E.3，式（13）—（16）<br><span class="experiment-evidence">In contrast, TTPO with majority-vote pseudo-labels maintains a steady and substantial loss decrease throughout training, confirming that vote-based routing keeps both branches active.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出无需标签的测试时策略优化方法，以自蒸馏和分组强化学习提升 LLM 数学推理能力。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`852d4ee475762b8d88f5134b44976611e97be715fd6e73bd4557725c1fd0ae2d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
