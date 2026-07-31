---
title: "[论文解读] VAD: Attributing Visual Evidence for Target Reconstruction in Multimodal On-Policy Distillation"
description: "[arXiv 2607.28590][多模态 VLM] VAD通过比较同一教师在“视觉证据存在”与“视觉证据移除”两种条件下的预测变化，估计教师纠正中可归因于视觉证据的部分，并据此重建以学生为锚点的蒸馏目标。"
arxiv_id: "2607.28590"
announcement_date: "2026-07-31"
primary_category: "multimodal_vlm"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.492425+00:00"
source_sha256: "66658cd7b42c8980f62ad7b1fddc60cdc706ef25a8d30ebccdb2555fa858071d"
tags:
  - "多模态 VLM"
  - "多模态大语言模型"
  - "在策略蒸馏"
  - "特权视觉证据"
  - "反事实视觉干预"
  - "视觉归因"
  - "目标重构"
  - "细粒度视觉感知"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">多模态 VLM · arXiv 2607.28590</p>

# VAD: Attributing Visual Evidence for Target Reconstruction in Multimodal On-Policy Distillation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Zhang, Kangning, Li, Yixing, Shao, Shuai, Li, Qingyao, Lu, Zhengxi, Yao, Zhiyuan, Lin, Jianghao, Jiao, Wenxiang, Lu, Yuan, Liu, Weiwen, Zhang, Weinan, Yu, Yong</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Shanghai Jiao Tong University；Xiaohongshu Inc.；The Chinese University of Hong Kong；Zhejiang University；Southeast University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.28590) · [PDF 下载](https://arxiv.org/pdf/2607.28590) · **关键词** 多模态大语言模型, 在策略蒸馏, 特权视觉证据, 反事实视觉干预, 视觉归因, 目标重构, 细粒度视觉感知<br>


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

VAD通过比较同一教师在“视觉证据存在”与“视觉证据移除”两种条件下的预测变化，估计教师纠正中可归因于视觉证据的部分，并据此重建以学生为锚点的蒸馏目标。

**不用术语来说**：多模态模型可能只因漏看一个文字、属性或空间关系，就沿着错误方向生成一整段看似流畅的回答。教师模型虽然能逐词纠正学生，但这些纠正既包含图像带来的信息，也混有语言常识、表达偏好和教师自身特性；因此，直接照搬教师的全部预测，并不能保证学生学到的确实是“如何依据图像改正错误”。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出视觉归因蒸馏（VAD）：在每个学生生成前缀上，对同一固定教师分别提供和移除相关视觉证据，以预测分布的反事实变化构造带符号的视觉证据方向，并将原始教师纠正投影到该方向上。
- 将估计出的视觉归因成分用于重建学生锚定的训练目标，而非直接蒸馏完整教师分布；作者进一步区分证据对候选词的支持与反驳，使训练既能提高正确词概率，也能压低由错误视觉判断产生的词。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于多模态大语言模型的知识蒸馏研究，关注细粒度视觉感知中的自回归生成错误：模型可能漏看文字、混淆属性或误判空间关系，并在错误视觉依据上继续生成流畅答案。多模态在策略蒸馏让教师在学生自己生成的前缀上提供下一词分布，以使训练状态贴近部署时实际遇到的状态；其中，特权视角教师还能看到局部裁剪等更清晰、但部署学生不可直接获得的视觉证据。本文指出，这类教师给出的完整修正同时混合了视觉证据、语言先验和教师自身偏好，因此教师与学生分歧较大并不等于该分歧确由视觉证据支持。研究核心由“在哪些词上、以多大权重蒸馏”转向“教师修正中哪一部分可归因于受控的视觉证据变化”。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**在策略蒸馏（On-Policy Distillation, OPD）**

学生先按当前策略生成回答前缀，教师再针对这些学生实际到达的状态提供下一词监督。它减少训练状态与部署状态之间的偏差，并能在早期感知错误刚出现时进行纠正。

</div>
<div class="concept-item" markdown="1">

**特权视角教师（Privileged-View Teacher）**

教师在训练时获得学生部署时没有的额外信息，例如突出关键细节的证据中心裁剪；学生仍需从完整图像独立作答。目标是把额外视角带来的有效知识内化到学生中，而不增加推理时的搜索或工具调用。

</div>
<div class="concept-item" markdown="1">

**反事实视觉干预与归因**

在教师、问题和生成前缀保持不变时，分别提供和移除相关视觉证据，再比较教师下一词预测的变化。该变化用于判断证据是在支持候选词还是反驳候选词，从而把视觉导致的修正与其他来源的变化区分开。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括完整图像、与图像相关的问题或指令、学生当前生成的前缀，以及训练阶段可用的相关局部视觉证据。学生仅基于完整图像沿自身策略产生前缀；同一个固定教师则在相同前缀上分别接受“证据存在”和“证据移除”的视图。系统比较两种条件下经中心化的下一词对数概率，得到带符号的视觉证据方向 $u_t$，再判断原始教师—学生修正中有多少与该方向一致：一致部分表示受到干预支持的视觉修正，其余部分被视为代理无法解释的残差。最终输出不是直接复制特权教师的完整分布，而是以完整图像学生分布为锚点、由视觉可归因分量重构的下一词训练目标；基本假设是，除受控视觉证据外，教师模型和生成前缀保持相同，因此两次预测之差可作为视觉归因的代理，而非严格的因果证明。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$t$**

自回归生成中的当前词元位置。

</div>
<div class="notation-item" markdown="1">

**$u_t$**

位置 $t$ 上的视觉证据方向：由同一教师在证据存在与证据移除条件下的中心化对数概率变化构成，是一个可正可负的词表方向；正向变化表示证据支持相应候选词，负向变化表示证据抑制或反驳相应候选词。

</div>

</div>

**直接相关的工作**

- **Vision-OPD**: 同样沿学生生成轨迹使用证据中心裁剪增强教师，但直接蒸馏证据存在时教师的完整下一词分布。VAD针对其监督来源混合的问题，通过证据存在/移除干预提取视觉方向，并只用与该方向对齐的修正重构目标。
- **Decomposed OPD**: 该方法也尝试构造视觉监督，但从学生文本先验与教师多模态相对文本条件的信息增益出发，侧重一般视觉信息匹配。VAD处理更具体的归因问题：把特权教师到学生的修正投影到同一教师的证据干预方向，并以完整图像学生为锚点，同时表达视觉支持与视觉反驳。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

多模态大语言模型的生成具有轨迹依赖性：早期对图中文字、物体属性或空间关系的一次误读，可能改变后续全部生成。在线策略蒸馏在学生自己生成的前缀上调用更强教师，因而能够针对部署时真正会遇到的错误状态提供逐词监督；但若监督信号不能区分视觉依据与非视觉因素，学生即使更接近教师，也未必获得更可靠的视觉落地能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **直接特权视图蒸馏（如 Vision-OPD）**：教师获得以相关证据为中心的裁剪图或其他特权视觉视图，并在学生生成的前缀上输出下一词分布；训练时直接让学生拟合教师的完整分布。
- **视觉优势加权**：利用加入视觉证据后预测得分是否提高来判断某个位置或词是否值得加强蒸馏，重点调节监督发生的位置或强度，而不重建监督分布本身。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 教师与学生的强分歧不等于该纠正由视觉证据解释。即使教师看到了证据中心视图，其完整下一词分布仍混合视觉信号、语言先验及教师特有偏好；直接蒸馏会把这些来源一并传给学生，无法有针对性地学习视觉纠错。
- 只关注正向视觉优势容易漏掉“反驳”作用：揭示证据未必直接提高学生原先候选词的得分，更可能先压低一个错误词，再把概率转移到正确替代词。因此，仅按正优势选择或加权监督，可能忽略视觉证据最关键的纠错信号。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法主要回答“在哪些位置蒸馏”或“以多大强度蒸馏”，尚缺少一种在固定教师和同一生成上下文内，利用视觉干预来估计教师纠正中哪一部分真正与证据变化一致，并把该部分转化为可训练目标的方法。尤其需要同时表示证据对候选词的支持和抑制，而不能把视觉作用简化为单向增益。

</div>
<div markdown="1"><span>核心问题</span>

能否通过比较同一教师在视觉证据存在与移除时的预测变化，构造一个带方向的视觉归因代理，并从来源混杂的教师—学生纠正中提取与该代理对齐的成分，以重建比完整教师分布更适合视觉学习的蒸馏目标？

</div>
<div markdown="1"><span>作者直觉</span>

如果只改变教师能否看到相关证据，而保持教师模型和学生前缀不变，那么两次预测之间的差异就近似刻画了这份证据把概率推向哪些词、又从哪些词移开的方向。再把原始教师纠正保留到这一方向上的部分，相当于优先学习“随证据而变化”的纠正；以学生当前分布为起点重建目标，则可减少无关教师偏好的迁移。不过作者明确指出，这只是语义上更富集的归因，并非可识别的纯视觉分解：单一视图对可能不足以表达组合证据，归因成分也仍可能残留非视觉教师效应。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

VAD是一种面向多模态在线策略蒸馏（on-policy distillation, OPD）的反事实目标重构方法。学生先在完整图像$x^{0}$上生成回答；固定教师随后在相同学生前缀$y_{<t}$下分别查看“证据存在”的裁剪$x^{+}$与“证据移除或退化”的视图$x^{-}$。两种教师视图的分布差异构成视觉证据方向$u_t$，而证据视图教师相对学生的差异构成完整教师修正$r_t$。VAD只保留$r_t$中与$u_t$同向的部分，再将其拆成支持候选词与反驳候选词的两条分支，在固定修正预算内重构以当前学生分布为锚点的目标$q_{T,t}^{\mathrm{VAD}}$。

训练时，学生主要通过Jensen–Shannon散度匹配重构目标，而证据视图教师$p_T^{+}$只提供弱稳定正则，以维护语言表达、格式、回答长度和停止行为。直观地说，VAD不要求学生照抄教师的完整答案偏好，而是做一次“遮掉关键证据后教师会如何改变判断”的对照实验，只学习其中可归因于视觉证据的改变量。教师和辅助视图仅用于造训练标签；推理时只保留普通的完整图像学生，因此不增加额外模型调用或视觉视图。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在线生成与反事实视图构造

学生采样回答$y\sim\pi_{\theta}(\cdot\mid x^{0})$，视图构造器生成$(x^{+},x^{-})=\mathcal{V}(x^{0})$；每个位置$t$都复用学生已生成的前缀$y_{<t}$。

<div class="method-step__io" markdown="1">

**输入**：训练样本中的完整图像$x^{0}$、当前学生策略$\pi_{\theta}$、固定教师$\pi_{\bar{\theta}}$及视图构造器$\mathcal{V}$。<br>
**输出**：学生在线轨迹$y$，以及证据存在视图$x^{+}$和证据移除或退化视图$x^{-}$。

</div>

**直观理解**：先让学生按自己当前的行为作答，再让教师围绕学生真正走到的每一步做对照判断。这样监督针对学生实际会犯的错误，而不是只针对离线标准答案前缀。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 共享候选空间上的三路分布评估

计算学生分布$p_S^{0}=\pi_{\theta}(\cdot\mid x^{0},y_{<t})$及教师分布$p_T^{+},p_T^{-}$；在学生前$K$个候选构成的共享集合$V_t$上，将三者转换为去均值的中心化对数概率$\phi_t(p)$。

<div class="method-step__io" markdown="1">

**输入**：完整图像$x^{0}$、两种辅助视图$x^{+},x^{-}$和同一前缀$y_{<t}$。<br>
**输出**：处于同一坐标系的$\phi_t(p_S^{0})$、$\phi_t(p_T^{+})$和$\phi_t(p_T^{-})$。

</div>

**直观理解**：三次判断必须比较同一批候选词；中心化去掉所有候选共同升降的无关偏移，保留候选词之间真正的相对赔率变化。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 视觉归因与支持—反驳预算分配

计算完整修正$r_t=\phi_t(p_T^{+})-\phi_t(p_S^{0})$与反事实视觉方向$u_t=\phi_t(p_T^{+})-\phi_t(p_T^{-})$，再以单侧投影得到$r_t^{\mathrm{vis}}$；随后把$u_t$分为正分支$u_t^{+}$和负分支$u_t^{-}$，按各自与$r_t$的一致程度分配预算$B_t=\lVert r_t^{\mathrm{vis}}\rVert_2$。

<div class="method-step__io" markdown="1">

**输入**：三路中心化对数概率向量。<br>
**输出**：可归因视觉修正$r_t^{\mathrm{vis}}$、未解释残差$r_t^{\mathrm{res}}$及预算化有符号修正$r_t^{\mathrm{VAD}}$。

</div>

**直观理解**：若教师的完整纠正与“显示证据所造成的变化”方向一致，才把这部分算作视觉监督。正分支提升被证据支持的候选，负分支压低被证据反驳的候选；方法不会把剩余部分武断地称为纯语言信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 学生锚定目标重构与优化

将裁剪后的$r_t^{\mathrm{VAD}}$加到学生中心化对数概率上并经softmax得到$q_{T,t}^{\mathrm{VAD}}$；以该目标和$p_S^{0}$之间的Jensen–Shannon散度为主损失，并按未被视觉归因的比例加入弱教师正则。

<div class="method-step__io" markdown="1">

**输入**：学生中心化分布$\phi_t(p_S^{0})$、预算化修正$r_t^{\mathrm{VAD}}$、教师证据分布$p_T^{+}$。<br>
**输出**：小批量总损失$\mathcal{L}$及更新后的学生参数$\theta$；教师参数$\bar{\theta}$保持冻结。

</div>

**直观理解**：目标从学生当前判断出发，只改动有反事实视觉依据的候选赔率，而不是把整套教师分布复制过来。弱教师项相当于护栏，防止只强调视觉纠正后出现啰嗦、重复、格式失稳或不能及时结束。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 完整教师修正、反事实视觉方向与单侧归因

$$
\begin{gathered}
\phi_t(p)=\log\!\left(p[V_t]+\epsilon\right)-\operatorname{mean}\!\left(\log\!\left(p[V_t]+\epsilon\right)\right),\\
r_t=\phi_t(p_T^{+})-\phi_t(p_S^{0}),\qquad u_t=\phi_t(p_T^{+})-\phi_t(p_T^{-}),\\
\beta_t=\frac{[\langle r_t,u_t\rangle]_{+}}{\lVert u_t\rVert_2^2+\zeta},\qquad r_t^{\mathrm{vis}}=\beta_tu_t,\qquad r_t^{\mathrm{res}}=r_t-r_t^{\mathrm{vis}}.
\end{gathered}
$$

**符号说明**

- $\phi_t(p)$：位置$t$上，分布$p$在共享候选集合上经过对数变换和去均值后的向量。
- $p[V_t]$：从分布$p$中取出候选集合$V_t$对应的概率。
- $V_t$：由学生在位置$t$的前$K$个候选词构成的共享坐标集合。
- $\epsilon$：加入概率及分母中的小正数，用于避免取零的对数或数值不稳定。
- $p_S^{0}$：学生在完整图像$x^{0}$和前缀$y_{<t}$下的下一词分布。
- $p_T^{+}$：固定教师在证据存在视图$x^{+}$和相同前缀下的下一词分布。
- $p_T^{-}$：固定教师在证据移除或退化视图$x^{-}$和相同前缀下的下一词分布。
- $r_t$：证据视图教师相对当前学生提出的完整候选词修正。
- $u_t$：显示视觉证据相对移除证据所引起的教师分布变化，即视觉证据方向代理。
- $[a]_{+}$：正部算子$\max(a,0)$。
- $\beta_t$：单侧投影系数，只在完整修正与视觉方向具有正内积时非零。
- $\zeta$：稳定投影分母的小正数。
- $r_t^{\mathrm{vis}}$：完整教师修正中与反事实视觉方向对齐的归因部分。
- $r_t^{\mathrm{res}}$：未被视觉代理解释的剩余修正。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先统一比较尺度，再把“教师想怎样纠正学生”与“视觉证据出现后教师怎样改变判断”区分开。只有两者同向时才产生视觉监督，从而避免把教师的语言偏好或其他来源混入主要目标。<br>
**原文位置**：第3.1—3.2节，公式（2）—（4）

</div>

</div>

<div class="equation-block" markdown="1">

#### 预算化目标重构与联合训练目标

$$
\begin{gathered}
B_t=\lVert r_t^{\mathrm{vis}}\rVert_2,\qquad
r_t^{\mathrm{VAD}}=B_t\left(\omega_t^{+}\frac{u_t^{+}}{\lVert u_t^{+}\rVert_2+\epsilon}+\omega_t^{-}\frac{u_t^{-}}{\lVert u_t^{-}\rVert_2+\epsilon}\right),\\
q_{T,t}^{\mathrm{VAD}}=\operatorname{softmax}\!\left(\phi_t(p_S^{0})+\operatorname{clip}(r_t^{\mathrm{VAD}},-c,c)\right),\\
D_{\mathrm{JS}}(q,p)=\frac{1}{2}\left[D_{\mathrm{KL}}(q\|m)+D_{\mathrm{KL}}(p\|m)\right],\qquad m=\frac{q+p}{2},\\
\mathcal{L}_{\mathrm{vis}}=\frac{1}{|\mathcal{T}|}\sum_{t\in\mathcal{T}}D_{\mathrm{JS}}\!\left(\operatorname{stopgrad}(q_{T,t}^{\mathrm{VAD}}),p_S^{0}\right),\\
\rho_t=\frac{\lVert r_t^{\mathrm{VAD}}\rVert_2}{\lVert r_t\rVert_2+\epsilon},\qquad a_t=\operatorname{stopgrad}\!\left(\operatorname{clip}(1-\rho_t,0,1)\right),\\
\mathcal{L}_{\mathrm{reg}}=\frac{1}{|\mathcal{T}|}\sum_{t\in\mathcal{T}}a_tD_{\mathrm{JS}}\!\left(\operatorname{stopgrad}(p_T^{+}),p_S^{0}\right),\qquad
\mathcal{L}=\mathcal{L}_{\mathrm{vis}}+\lambda\mathcal{L}_{\mathrm{reg}}.
\end{gathered}
$$

**符号说明**

- $B_t$：位置$t$可使用的视觉修正总预算，等于归因修正的二范数。
- $u_t^{+}$：视觉方向$u_t$的非负部分，表示证据支持候选词的方向。
- $u_t^{-}$：视觉方向$u_t$的非正部分，表示证据反驳候选词的方向。
- $\omega_t^{+}$：分配给支持分支的预算权重；原方法按分支一致性计算并以$\tau_{+}$封顶。
- $\omega_t^{-}$：分配给反驳分支的预算权重。
- $r_t^{\mathrm{VAD}}$：在固定视觉预算内重新组合支持和反驳分支后得到的有符号修正。
- $c$：对每个修正坐标进行上下界裁剪的幅度。
- $q_{T,t}^{\mathrm{VAD}}$：以当前学生分布为锚点、加入视觉归因修正后得到的训练目标分布。
- $D_{\mathrm{JS}}$：Jensen–Shannon散度，用于对称地度量两个概率分布的差异。
- $D_{\mathrm{KL}}$：Kullback–Leibler散度。
- $q$：Jensen–Shannon散度中的第一个概率分布。
- $p$：Jensen–Shannon散度中的第二个概率分布。
- $m$：分布$q$与$p$的等权混合。
- $\mathcal{T}$：回答中参与训练的有效位置集合。
- $\mathcal{L}_{\mathrm{vis}}$：学生匹配VAD重构目标的主要视觉监督损失。
- $\rho_t$：预算化视觉修正相对完整教师修正的范数比例。
- $a_t$：教师正则的停止梯度权重；视觉归因比例越小，该权重通常越大。
- $\operatorname{stopgrad}$：停止梯度算子，使目标侧量不参与反向传播。
- $\mathcal{L}_{\mathrm{reg}}$：学生匹配证据视图教师的弱稳定正则。
- $\lambda$：弱教师正则在总损失中的系数。
- $\mathcal{L}$：用于更新学生参数的总训练损失。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分保持视觉修正总强度不变，但允许支持与反驳采用不同份额，再把修正施加到学生自身的候选赔率上。第二部分用重构目标承担主要学习信号；当视觉归因只能解释完整教师纠正的一小部分时，弱教师项自动增强，为语言流畅性、格式和停止行为提供稳定锚点。<br>
**原文位置**：第3.3—3.4节，公式（7）—（10）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优化变量只有学生参数$\theta$，固定教师参数$\bar{\theta}$不更新。主损失$\mathcal{L}_{\mathrm{vis}}$在每个有效响应位置上最小化停止梯度后的$q_{T,t}^{\mathrm{VAD}}$与学生$p_S^{0}$之间的Jensen–Shannon散度；因此，与标准OPD相比，散度形式没有改变，关键变化是把直接教师目标替换为反事实归因后的学生锚定目标。所有目标侧量，包括构造目标时使用的$p_S^{0}$副本，均从计算图中分离，避免学生通过改变目标本身来降低损失。

仅使用$\mathcal{L}_{\mathrm{vis}}$会把监督集中在证据敏感成分上，原文报告其视觉-only消融出现回答变长、重复、承诺答案延迟以及格式和停止不稳定。为此，总目标加入$\lambda\mathcal{L}_{\mathrm{reg}}$：当$\lVert r_t^{\mathrm{VAD}}\rVert_2$相对$\lVert r_t\rVert_2$较小时，权重$a_t$更大，使学生弱匹配$p_T^{+}$；这一项是稳定护栏而非主要视觉知识来源。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 同前缀反事实教师对照**

固定同一个教师$\pi_{\bar{\theta}}$和文本前缀$y_{<t}$，只把视觉输入从$x^{-}$替换为$x^{+}$，以$u_t=\phi_t(p_T^{+})-\phi_t(p_T^{-})$表示证据可见性引起的分布响应。该量是视觉信息方向的代理，而非像素级梯度或真实定位标签。

> 直观理解：控制教师和文字上下文不变后，两次预测的主要实验差别就是关键视觉证据是否可见，因此差值比单独查看裁剪教师更能说明某个候选为何被支持或反驳。

**2. 单侧归因投影**

将完整教师修正$r_t$投影到视觉代理$u_t$上，并通过$[\langle r_t,u_t\rangle]_{+}$只接受非负一致性；若两者不一致，则$\beta_t=0$，不施加视觉位移。残差$r_t^{\mathrm{res}}=r_t-r_t^{\mathrm{vis}}$仅表示代理未解释的修正，不被假定为纯语言成分。

> 直观理解：教师可能同时带来视觉知识、语言习惯和教师自身偏好；投影像一个来源过滤器，只留下与“证据出现时的变化”相符的纠正。

**3. 预算化支持与反驳重构**

方法把$u_t$拆为非负支持方向$u_t^{+}$和非正反驳方向$u_t^{-}$，用与$r_t$的分支一致性分配总预算$B_t$，并仅对支持份额设置上限$\tau_{+}$。所得$r_t^{\mathrm{VAD}}$经逐坐标裁剪后加到学生中心化对数概率上，形成$q_{T,t}^{\mathrm{VAD}}$。

> 直观理解：“看到证据后更相信正确词”和“看到证据后排除错误词”不是同一种信号；分开处理可避免不确定的正证据占满预算，同时保留强烈反证纠正错误答案的能力。

**训练与推理**

训练循环以小批量$\mathcal{B}\subset\mathcal{D}$为单位：学生在$x^{0}$上在线采样回答，构造$x^{+}$与$x^{-}$；对回答每个位置$t$，在同一前缀上计算三路分布及共享候选集合$V_t$上的中心化对数概率，形成$r_t$和$u_t$，完成单侧归因、支持—反驳预算分配及$q_{T,t}^{\mathrm{VAD}}$重构；随后累计主JSD与弱正则并更新$\theta$，同时保持$\bar{\theta}$固定。这一流程属于在线策略蒸馏，因为监督前缀来自当前学生而非固定参考轨迹。

推理时只使用优化后的全图学生$\pi_{\theta}(\cdot\mid x^{0})$。固定教师、证据裁剪$x^{+}$、退化视图$x^{-}$、归因投影和目标重构全部移除，因此VAD不会增加推理阶段的模型调用、视觉视图数量或额外输出模块。

**复现信息**

为使三路分布可比较且控制计算量，每个位置只在学生前$K$候选形成的$V_t$上收集教师对应词元的概率；中心化对数概率保留共享支持上的成对对数赔率，并消除共同logit偏移。投影分母使用$\zeta$稳定，概率对数和归一化分母使用$\epsilon$稳定；重构位移逐坐标裁剪到$[-c,c]$，支持分支份额由$\tau_{+}$封顶，而被截去的支持预算不重新分配。

这些细节决定了方法的公平解释：$x^{+}$与$x^{-}$只改变训练目标的构造，不改变学生 rollout；教师始终是初始模型的冻结副本；所有教师查询复用同一学生前缀，避免把文本上下文变化误当成视觉贡献。原文节选未给出$K$、$c$、$\tau_{+}$、$\lambda$、$\epsilon$和$\zeta$的具体数值，故不能从所给材料中补造。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 训练集：Vision-OPD 发布的 6,241 条合成视觉问答样本。每条样本包含带相关区域标记的完整图像 $x^0$、保留细粒度证据的 $2\times2$ 裁剪视图 $x^+$，以及将同一区域先按 $0.1\times$ 双线性下采样、再最近邻上采样得到的证据退化视图 $x^-。$训练图像和问题均不与六个主要测试基准重叠；该数据用于构造“证据存在/证据移除”的反事实教师响应。
- 主要细粒度评测套件：VStar、ZoomBench、HRBench-4K、HRBench-8K、MME-RealWorld-EN 和 MME-RealWorld-CN，共六项准确率测试。它们共同检验细节定位、高分辨率感知以及中英文真实场景识别；六项结果还计算不加权平均 $\operatorname{Avg}_6$。
- 留出泛化套件：MMVP、CV-Bench、MMStar 和 POPE，均处于后训练与检查点选择流程之外，使用各基准原生指标并计算不加权平均 $\operatorname{Avg}_4$。该套件用于判断针对细粒度视觉能力的专项训练是否损害更广泛的视觉理解与幻觉控制能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率与 $\operatorname{Avg}_6$**

六个主要细粒度视觉基准分别报告准确率，$\operatorname{Avg}_6$ 是六项准确率的不加权平均，用于衡量模型在不同细节感知任务上的总体均衡表现。 （越高越好，因为更高值表示更多问题得到正确回答；但平均值可能掩盖单项退化，因此还需同时检查六个分项。）

</div>
<div class="metric-item" markdown="1">

**$\operatorname{Avg}_4$ 与相对 Base 的 $\Delta$**

$\operatorname{Avg}_4$ 汇总四个留出基准的原生百分制指标，$\Delta$ 表示后训练模型相对同尺度 Base 的平均变化，用于检测专项训练是否牺牲域外能力。 （$\operatorname{Avg}_4$ 越高越好，$\Delta$ 为正更理想；正值表示总体泛化能力至少未因专项后训练而下降。）

</div>
<div class="metric-item" markdown="1">

**正确令牌支持与错误令牌抑制**

在固定答案令牌位置离线测量监督目标使正确答案概率上升、使学生已选错误答案概率下降的百分点，直接观察目标分布的更新方向，而不是仅看训练后的端到端分数。 （两者均越高越好，因为理想监督应同时提升正确候选并压低错误候选；置信区间重叠时只能说明方向性趋势，不能宣称两方法之间存在显著差异。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 匹配训练数据与更新预算的 4B、9B 细粒度视觉评测

<div class="result-value" markdown="1">

VAD 的 $\operatorname{Avg}_6$ 在 4B 和 9B 上分别达到 78.32% 和 79.93%，相对各尺度最强的匹配替代方法分别领先 2.40 和 2.80 个百分点；相对最接近的 Decomposed OPD，分别提升 2.95 和 2.88 个百分点。

</div>

作者据此主张，收益来自对特权教师修正进行视觉归因并重构目标，而不是增加训练样本或更新次数。进一步看分项，VAD 在 4B 的六项测试全部领先受控后训练方法，在 9B 的六项中领先五项；唯一例外是 ZoomBench，VA-OPD 高 0.35 个百分点。因此改进并非只由单一基准推动。不过，这些结果仍依赖同一 Qwen3.5 模型家族、合成训练集和自动裁判流程，不能单独证明对所有模型和真实部署场景都成立。

<div class="result-source" markdown="1">

来源：第 4.2 节 RQ1；表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

It reaches 78.32 and 79.93 in Avg6, leading the best scale-matched alternative by 2.40 points at 4B and 2.80 points at 9B.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 对教师修正、视觉归因分量与残差进行令牌级语义分析

<div class="result-value" markdown="1">

在排除 Other 后的相对 top-5 构成中，视觉属性、对象/内容及 A–D 决策令牌在视觉归因方向 $r_t^{\mathrm{vis}}$ 中合计占 42.0%，高于完整教师修正 $r_t$ 的 26.7% 和残差 $r_t^{\mathrm{res}}$ 的 17.7%；语言/格式及伪影/元语义则分别为 58.0%、73.3% 和 82.3%。

</div>

这一分析回答了 VAD 是否只是把教师修正整体缩小：若只是标量缩放，各语义类别的相对构成不应明显重排。结果显示视觉属性、对象和答案决策更集中于 $r_t^{\mathrm{vis}}$，而语言实现与退化相关内容更多留在残差中，支持“视觉可归因方向具有不同语义”的解释。但类别标注与 top-5 词汇统计只是代理证据；残差仍是未被视觉干预解释的混合成分，不能被等同为纯语言噪声。

<div class="result-source" markdown="1">

来源：第 4.3 节 RQ2；图 3(a)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In Figure 3(a), visual attributes, objects/content, and A–D decisions jointly account for 42.0% of the relative top-5 composition in rtvis, compared with 26.7% in rt and only 17.7% in rtres.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 在 MMVP、CV-Bench、MMStar 与 POPE 上测试后训练检查点的留出泛化

<div class="result-value" markdown="1">

VAD 在 4B 和 9B 上分别取得 79.14% 与 82.62% 的 $\operatorname{Avg}_4$，相对同尺度 Base 分别为 $+0.24$ 和 $+0.23$ 个百分点；它是唯一在两个尺度上 $\Delta$ 都为正的后训练方法。相较 Vision-OPD，VAD 分别领先 1.13 和 2.18 个百分点。

</div>

结果表明，VAD 提升细粒度视觉套件时没有表现出总体留出能力下降，并比其他后训练方法更稳定地维持 Base 水平。不过，提升幅度只有约 0.2 个百分点，主要应解读为“未观察到总体损害”，而不是强泛化增益；此外，四项平均值不能排除个别任务退化，例如 4B VAD 的 MMStar 分数低于 Base。

<div class="result-source" markdown="1">

来源：第 4.5 节 RQ4；表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Among post-trained models, VAD achieves the highest held-out average at both 4B (79.14) and 9B (82.62), improving over the scale-matched Base by +0.24 and +0.23 points.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 跨家族结果不能作为严格受控证据：封闭模型、大型开源模型和图像代理在架构、训练数据、推理策略及算力上均不同。论文也明确指出这些差异排除了受控比较，因此参数效率结论只能作为能力背景，核心证据仍是 Qwen3.5 内部的匹配实验。
- 主要结果使用 GPT-OSS-120B 自动裁判和官方准确率流程，且训练仅基于 6,241 条合成问答样本；原文未在所给章节中报告人工评分一致性、多随机种子方差或显著性检验。图 4 的置信区间还存在重叠，因此离线正确令牌支持与错误令牌抑制只能说明一致趋势，不能证明目标之间具有两两统计显著优势。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen3.5 Base 与 GRPO：前者给出未经专项后训练的能力基准，后者代表基于奖励的策略优化。二者分别帮助判断专项训练的净收益，以及 VAD 相对非蒸馏式后训练的优势。
- Vision-OPD：直接使用完整特权视图教师分布进行在线策略蒸馏，是检验“重构视觉可归因目标是否优于直接模仿来源混合教师修正”的核心基线。
- VA-OPD 与 V-Zero：代表视觉优势加权或相关视觉后训练方法，用于区分 VAD 的反事实方向投影与仅调整样本或令牌权重的做法。
- Decomposed OPD：同样尝试分解蒸馏信号，是与 VAD 最接近的结构性基线；比较重点在于 VAD 是否因视觉归因和目标重构本身获益，而非仅因一般性的分解操作。

**实验想回答的问题**

- 在训练数据、模型初始化和更新预算匹配的条件下，VAD 能否比直接特权视图蒸馏、视觉优势加权及强化学习等方法更准确地完成细粒度视觉任务，并将这种能力迁移到未参与训练和选模的任务？
- VAD 的反事实分解与目标重构是否确实提取了视觉证据相关的监督方向；分支感知重构、弱教师正则、散度函数及超参数分别如何影响正确答案支持、错误答案抑制和最终准确率？

**实验实现**

实验分别以 Qwen3.5-4B 和 Qwen3.5-9B 初始化，在相同的 6,241 条训练样本和匹配的后训练预算下比较受控方法；初始学生的冻结副本充当教师。VAD 在学生生成的前缀上计算教师面对 $x^+$ 与 $x^-$ 时的响应，以学生 top-100 令牌支持集加一个尾部桶优化重构目标上的逐令牌 JSD。主要训练配置为批量大小 96、每提示 8 条 rollout、学习率 $2\times10^{-6}$、投影稳定项 $\zeta=10^{-3}$、坐标界 $c=20$、弱正则权重 $\lambda=0.1$；正分支上限 $\tau_+$ 在 4B 和 9B 上分别为 0.8 和 0.7。六个主基准统一采用 Vision-OPD 官方推理与准确率流程，并以 GPT-OSS-120B 作为裁判。跨模型家族的结果仅提供能力背景，因为架构、数据和算力并不匹配；因果性较强的比较应限于共享初始化、数据和预算的 Qwen3.5 行。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 监督目标构造与弱教师正则消融（Qwen3.5-4B） | 直接匹配教师的 $\operatorname{Avg}_6$ 为 75.92%，仅做标量缩放为 76.19%；无正则时，从单侧目标 $q_T^{\mathrm{one}}$ 改为分支感知目标 $q_T^{\mathrm{VAD}}$，平均分由 77.06% 升至 78.06%，即提升 1.00 个百分点。加入弱教师锚点后，单侧目标和 VAD 分别达到 77.52% 与 78.32%；Full VAD 比无正则版本再高 0.26 个百分点。 | 标量缩放只改变修正强度而保留来源混合方向，其 0.27 个百分点的小幅收益说明“少蒸馏一点”不足以解释 VAD。无正则条件下的 1.00 个百分点差值更直接隔离了分支感知目标重构的作用；正则带来的 0.26 个百分点则表明教师锚点是辅助稳定项，而非主要性能来源。该消融只在 4B 上完整报告，因此不能假定各组成部分在 9B 上具有相同贡献。 | 第 4.4 节 RQ3；表 2<br><span class="experiment-evidence">Without regularization, replacing qTone with qTVAD raises the average from 77.06 to 78.06, isolating a 1.00-point gain from branch-aware reconstruction.</span> |
| 监督散度消融：JSD、前向 KL 与反向 KL | 4B 上 JSD、前向 KL、反向 KL 的 $\operatorname{Avg}_6$ 分别为 78.32%、77.62%、77.85%；9B 上分别为 79.93%、79.21%、79.56%。JSD 因而分别领先次优反向 KL 0.47 和 0.37 个百分点。分项上，4B 的 VStar 以及 9B 的 HRBench-8K、MME-RealWorld 分项并非由 JSD 全部领先。 | 该实验固定目标构造及尺度对应的 $\lambda$、$\tau_+$，主要隔离“如何度量学生分布与目标分布差异”的影响。JSD 的平均表现最好，说明对称散度在不同基准间更均衡；但优势幅度有限且并非每项占优，因此不能推断 JSD 在所有视觉任务上都严格优于方向性 KL。 | 第 4.6 节 RQ5；表 4<br><span class="experiment-evidence">At 4B, JSD reaches 78.32 Avg6 and leads on five benchmarks, except VStar.</span> |

**定性案例**

- 图 3(b)–(c) 的代表性令牌分析显示，A–D 答案符号以及“vertical”“metal”等属性或对象词在 $r_t^{\mathrm{vis}}$ 中更突出，而“to”“inside”等语言支架或伪影相关词在 $r_t^{\mathrm{res}}$ 中更突出。直观上，VAD 倾向把“图中证据支持哪个答案”的变化放入视觉分量，把表达方式及未被干预解释的内容留给残差；这是聚合式定性例证，并非逐样本因果证明。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出基于反事实视觉证据归因的多模态在策略蒸馏目标重构算法，以传递细粒度视觉知识。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`66658cd7b42c8980f62ad7b1fddc60cdc706ef25a8d30ebccdb2555fa858071d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
