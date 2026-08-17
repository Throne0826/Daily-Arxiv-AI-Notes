---
title: "[论文解读] SimpleOPD: Simple Tokenizer-Agnostic On-Policy Distillation for Long-Context Reasoning"
description: "[arXiv 2608.14277][LLM Reasoning] 本文研究如何把长上下文教师模型的推理能力稳定地蒸馏给上下文较短且分词器不同的学生模型，重点解决跨分词器监督、输出长度失控和训练不稳定问题。"
arxiv_id: "2608.14277"
announcement_date: "2026-08-17"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-17T02:02:00.679180+00:00"
source_sha256: "fe87866b4a1a6df56169833417280ff6396092258694bd4cf8f0342919185977"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "按策略蒸馏"
  - "跨分词器蒸馏"
  - "长上下文推理"
  - "数学证明"
  - "教师—学生分布失配"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.14277</p>

# SimpleOPD: Simple Tokenizer-Agnostic On-Policy Distillation for Long-Context Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Haonan He, Haodi Lei, Yun Luo, Haoran Zhang, Shunkai Zhang, Yizhuo Li, Shengji Tang, Zhilin Wang, Runzhe Zhan, Lei Bai, Ganqu Cui, Fangchen Yu, Yafu Li, Peng Ye, Ning Ding, Yu Cheng</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> SU-01 Team, Shanghai Artificial Intelligence Laboratory</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14277) · [PDF 下载](https://arxiv.org/pdf/2608.14277) · **关键词** 按策略蒸馏, 跨分词器蒸馏, 长上下文推理, 数学证明, 教师—学生分布失配<br>


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

本文研究如何把长上下文教师模型的推理能力稳定地蒸馏给上下文较短且分词器不同的学生模型，重点解决跨分词器监督、输出长度失控和训练不稳定问题。

**不用术语来说**：较强的教师模型往往能进行很长的推理，但较小学生模型可处理的文本长度有限，而且二者可能用不同方式把同一句话切成词元。若直接要求学生逐词模仿教师，不仅难以确定哪些词元应当对应，教师还可能持续鼓励学生延长推理、阻止其正常结束，最终使回答超过长度上限而被截断。因此，实际需求不是简单复制教师答案，而是在学生自身生成过程中提供可对齐、可控制且不会破坏完整作答的教师指导。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将跨分词器蒸馏建立在共享文本空间上：学生先用自身分词器生成回答，教师再用自己的分词器评估同一文本，仅对覆盖完全相同文本区间的词元实施教师监督，从而避免人为构造不可靠的词表映射。
- 作者识别出长上下文教师向短上下文学生直接进行在策略蒸馏时的关键失稳机制，并提出终止词元优势屏蔽与学生参考策略 KL 正则化，分别避免教师压制正常结束、限制学生偏离初始策略，以缓解长度爆炸和频繁截断。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型后训练与推理能力蒸馏的交叉领域，核心对象是按策略蒸馏（on-policy distillation，OPD）。与先固定生成教师数据、再训练学生的离策略方法不同，OPD让学生先依据自身策略生成回答，再由教师对学生轨迹中的各个位置提供分布级监督，因此能够在学生实际会访问的状态上进行细粒度学习。本文关注一个现有研究较少覆盖的设置：把具有较长上下文预算和强证明推理能力的教师模型 SU-01，迁移到上下文较短、可能属于不同模型家族且使用不同分词器的学生模型。该设置需要同时处理词元无法直接对应、教师与学生生成分布差异大，以及长推理轨迹超出学生上下文预算等问题。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**按策略蒸馏（OPD）**

学生模型先按照自己的当前策略生成轨迹，教师再评估这些学生生成的文本，并在词元层面提供监督。这样学习到的不是教师固定数据的表面模式，而是教师对学生实际生成过程的指导。

</div>
<div class="concept-item" markdown="1">

**分词器与共享文本空间**

分词器把字符串切分成模型处理的词元，但不同模型可能采用不同切分方式，因此同一段文本不一定对应相同的词元序列。本文把学生生成的字符串作为共享文本空间，只对教师和学生所覆盖的文本区间完全相同的词元进行对齐。

</div>
<div class="concept-item" markdown="1">

**教师—学生分布失配**

教师和学生的模型容量、上下文长度及推理习惯不同，导致它们在相同历史文本下偏好的后续文本分布不同。长上下文教师尤其可能持续生成超过学生预算的推理轨迹，使学生频繁截断、无法完成答案并造成训练不稳定。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个能够生成长推理轨迹的教师模型 SU-01，以及一个上下文长度较短的学生模型，输入是数学或科学问题，学生使用自己的分词器自回归生成回答，教师则使用自己的分词器评估同一条学生生成文本。目标是在不依赖教师轨迹监督微调的前提下，通过 OPD 把教师的证明与长程推理能力迁移给学生，同时使生成长度保持在学生上下文预算内。本文允许教师与学生来自不同模型家族、使用不同词汇表和分词器；因而不假设两者存在完整的一一词元对应关系，而只利用文本区间相同的局部对应关系。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$T_d$**

教师模型，用于评估学生生成轨迹并提供蒸馏监督。

</div>
<div class="notation-item" markdown="1">

**$S$**

学生模型，按照自身当前策略生成回答并接受训练。

</div>
<div class="notation-item" markdown="1">

**$x$**

输入问题，例如数学证明题或科学问题。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{KL}$**

KL散度，用于衡量两个概率分布之间的差异；本文特别使用学生当前策略与其初始策略之间的参考 KL 约束，以限制学生策略过度漂移。

</div>

</div>

**直接相关的工作**

- **MiniLLM 与 GKD**: 这两项工作代表 OPD 的早期研究：在学生生成的轨迹上，以教师分布对学生分布进行词元级蒸馏。本文继承其按策略监督思想，但将问题扩展到不同模型家族、不同分词器以及长上下文教师到短上下文学生的异构迁移。
- **SU-01**: SU-01 是本文使用的长上下文推理教师，具有奥林匹克数学证明能力。本文不重新训练教师，而是研究如何将其长程证明推理能力稳定地迁移到多种短上下文学生模型。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

需要把 SU-01 等长上下文强推理模型的数学证明能力迁移到上下文预算更小、模型家族不同的学生模型中。部署侧学生必须在有限长度内形成完整推理，而教师偏好的长回答可能超出学生预算；一旦大量轨迹被截断，训练得到的就不是完整的论证行为，而是不断延长却无法收束的生成模式。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **离策略蒸馏**：预先由教师生成固定训练数据，再让学生学习这些教师轨迹。其监督不随学生当前策略变化，因此学生训练时实际会访问的生成状态可能与固定教师数据存在偏差。
- **直接在策略蒸馏**：由学生当前策略生成轨迹，再让教师对轨迹中的词元进行评价，提供贴近学生自身状态分布的稠密词元级监督。已有研究主要在教师与学生属于同一模型家族、共享词表或分词器的条件下采用这种方法。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 教师与学生使用不同分词器时，同一段文本会被切成不同词元，二者词元级概率分布无法直接逐位置对应；强行对齐会使教师监督落到语义或字符范围不一致的学生词元上。
- 长上下文教师与短上下文学生在容量、策略分布和可用上下文上存在明显差距。直接在策略蒸馏会让教师反复降低 `</think>`、`<|im_end|>` 等终止词元的相对收益，导致学生持续延长回答、遗漏结束标记并频繁被截断，进而使优化不稳定。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有工作尚未充分回答：在教师与学生既不共享分词器、也不共享上下文预算和模型家族的情况下，如何保留在策略蒸馏基于学生轨迹提供稠密监督的优势，同时建立可信的词元监督对应关系，并将生成长度控制在学生可承受范围内。尤其缺少一种无需先对教师轨迹做监督微调、又能适用于多种学生模型的简洁稳定方案。

</div>
<div markdown="1"><span>核心问题</span>

能否以学生生成的文本作为教师和学生的共同参照，只使用文本跨度一致的词元监督，再通过保护终止行为和约束策略漂移，稳定地把长上下文教师的推理能力迁移给跨分词器、短上下文的学生模型？

</div>
<div markdown="1"><span>作者直觉</span>

分词器虽然可能把句子切得不同，但底层文本本身是共同的；因此只在双方词元恰好覆盖同一文本区间时传递监督，可以舍弃含义不明确的对应关系，同时保留可靠信号。另一方面，学生并不需要无条件复制教师偏好的推理长度：屏蔽结构性终止词元上的教师优势，相当于不让教师直接阻止学生“收尾”；参考策略 KL 约束则像限制每次更新离原有生成习惯走得过远。两者结合，使学生能够逐步吸收更长、更强的推理模式，而不是突然把回答拉长到自身上下文上限之外。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SimpleOPD是一种面向异构分词器的在线策略蒸馏方法。给定消息列表形式的输入对话 $\mathbf{x}$，学生先使用自己的聊天模板 $\mathcal{C}_{\theta}$ 构造上下文 $c_{\theta}$，再由当前或近当前的学生策略生成响应 token 序列 $y_{1:n}$；该序列被解码为响应字符串 $s$。教师不直接接收学生模板下的上下文，而是用自己的聊天模板 $\mathcal{C}_{\phi}$ 重建上下文 $c_{\phi}$，并在自己的分词器下重新编码同一个字符串 $s$，得到教师 token 序列 $z_{1:m}$ 及逐 token 对数概率。这样，师生虽然使用不同模板和分词器，评价的自然语言响应仍完全相同。

随后，方法以共享字符串 $s$ 中的字符偏移为桥梁，只对“起止位置和实际文本片段均一致”的师生 token 建立一对一对齐，并把相应教师对数概率映射到学生位置；无法严格对齐的位置回退到旧学生策略自身的对数概率，因此其蒸馏优势为零。训练上，教师与旧学生概率之差形成固定的逐 token 优势 $\widehat{A}_t$，再通过带裁剪的 PPO 代理目标更新学生。直观地说，该方法不强迫两套词表互相翻译，而是在两套分词结果恰好切出同一段文字时传递教师信号，其余位置保持中性，从而以简单、保守的方式支持跨分词器在线蒸馏。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 学生在线生成响应

先计算 $c_{\theta}=\mathcal{C}_{\theta}(\mathbf{x})$，再从 $\pi_{\theta_{\mathrm{roll}}}(\cdot\mid c_{\theta})$ 采样 $y_{1:n}$，最后用学生解码器 $\mathcal{D}_{\theta}$ 得到表层字符串 $s=\mathcal{D}_{\theta}(y_{1:n})$。样本来自学生当前行为分布，因此属于在线策略蒸馏，而不是只学习预先固定的教师样本。

<div class="method-step__io" markdown="1">

**输入**：消息列表 $\mathbf{x}$、学生聊天模板 $\mathcal{C}_{\theta}$，以及执行采样的学生 rollout 策略 $\pi_{\theta_{\mathrm{roll}}}$。<br>
**输出**：学生 token 序列 $y_{1:n}$、学生上下文 $c_{\theta}$ 和双方共享的响应字符串 $s$。

</div>

**直观理解**：学生先亲自完成题目，教师随后评价学生实际写出的答案。这样训练直接覆盖学生当前容易产生的推理轨迹与错误，而不是只模仿教师理想答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在教师原生接口下重新评分

教师独立构造 $c_{\phi}=\mathcal{C}_{\phi}(\mathbf{x})$，形成完整文本 $u_{\phi}=c_{\phi}\oplus s$，并将响应部分编码为 $z_{1:m}=\mathcal{E}_{\phi}(s\mid c_{\phi})$。教师对每个 $z_i$ 计算条件对数概率 $\log\pi_{\phi}(z_i\mid c_{\phi},z_{<i})$，且不要求 $m=n$。

<div class="method-step__io" markdown="1">

**输入**：原始对话 $\mathbf{x}$、共享响应字符串 $s$、教师聊天模板 $\mathcal{C}_{\phi}$、教师编码器 $\mathcal{E}_{\phi}$ 和教师策略 $\pi_{\phi}$。<br>
**输出**：教师 token 序列 $z_{1:m}$、教师上下文 $c_{\phi}$，以及逐教师 token 的对数概率。

</div>

**直观理解**：同一句回答分别交给师生各自的“阅读规则”处理，避免教师被迫使用不熟悉的学生模板或词表。二者看到的上下文格式可能不同，但被评价的回答文字 $s$ 不变。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于文本偏移的跨分词器对齐

用线性双指针扫描两套有序分段；仅当两个 token 的起始前缀相同且贡献的文本片段完全相同时，将 $(i,t)$ 加入对齐集合 $\mathcal{M}$。部分重叠不被拆分或合并，因为单个 token 的条件概率不能唯一分配给另一侧的多个 token。

<div class="method-step__io" markdown="1">

**输入**：学生分段 $\tau_{\theta}(y_t)$、教师分段 $\tau_{\phi}(z_i)$，以及它们在共享字符串 $s$ 中的累计前缀 $P_{\theta}(t)$ 与 $P_{\phi}(i)$。<br>
**输出**：部分一对一映射 $\mathcal{M}$、学生位置指示量 $a_t$，以及监督覆盖率 $\rho=|\mathcal{M}|/n$。

</div>

**直观理解**：可以把两套 token 看成对同一行文字的不同切词：只有两边画出的格子起点、终点都相同，格子才配对。若一边一个格子覆盖另一边两个格子，方法宁可跳过，也不任意猜测怎样拆分概率。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造蒸馏优势并更新学生

对齐位置把教师对数概率写入学生长度的目标 $\widetilde{\ell}^{\phi}_t$；未对齐位置则令目标等于旧学生对数概率。由 $\widehat{A}_t=\widetilde{\ell}^{\phi}_t-\log\pi_{\theta_{\mathrm{old}}}(y_t\mid c_{\theta},y_{<t})$ 得到固定优势，并以重要性比率 $r_t$ 和 PPO 裁剪目标执行一次或多次更新。

<div class="method-step__io" markdown="1">

**输入**：对齐集合 $\mathcal{M}$、教师对数概率、旧学生策略 $\pi_{\theta_{\mathrm{old}}}$ 的对数概率，以及待更新策略 $\pi_{\theta}$。<br>
**输出**：优化后的学生参数 $\theta$；未对齐位置的 $\widehat{A}_t=0$，不会产生人为的跨分词器监督。

</div>

**直观理解**：教师若比旧学生更认可某个已对齐 token，该 token 就获得正向推动；反之则被抑制。裁剪限制同一批数据上的更新幅度，防止学生因概率差异过大而一步偏离生成该批样本时的策略。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 跨分词器严格对齐集合

$$
\mathcal{M}=\{(i,t):P_{\phi}(i)=P_{\theta}(t)\land\tau_{\phi}(z_i)=\tau_{\theta}(y_t)\}
$$

**符号说明**

- $\mathcal{M}$：教师 token 位置与学生 token 位置构成的部分一对一对齐集合。
- $i$：教师响应 token 序列中的位置索引。
- $t$：学生响应 token 序列中的位置索引。
- $z_i$：教师分词器对共享响应字符串编码后得到的第 i 个 token。
- $y_t$：学生策略生成的第 t 个响应 token。
- $P_{\phi}(i)$：教师第 i 个 token 之前已经覆盖的响应文本前缀。
- $P_{\theta}(t)$：学生第 t 个 token 之前已经覆盖的响应文本前缀。
- $\tau_{\phi}(z_i)$：教师 token $z_i$ 在增量解码时贡献的实际文本片段。
- $\tau_{\theta}(y_t)$：学生 token $y_t$ 在增量解码时贡献的实际文本片段。
- $\land$：逻辑与，表示起始前缀相同和当前文本片段相同必须同时成立。

<div class="equation-explanation" markdown="1">

**直观理解**：该式要求配对 token 在共享响应字符串中具有相同起点，并贡献完全相同的文字，因此也具有相同终点。它是整个方法能够在不同分词器之间传递逐 token 概率、同时避免含糊概率拆分的基础。<br>
**原文位置**：第 2.1 节，公式 (2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 带裁剪的在线策略蒸馏目标

$$
\mathcal{L}_{\theta}=-\mathbb{E}\left[\sum_{t=1}^{n}\min\left(r_t\widehat{A}_t,\operatorname{clip}(r_t,1-\epsilon,1+\epsilon)\widehat{A}_t\right)\right],\quad \widehat{A}_t=\widetilde{\ell}^{\phi}_t-\log\pi_{\theta_{\mathrm{old}}}(y_t\mid c_{\theta},y_{<t}),\quad r_t=\frac{\pi_{\theta}(y_t\mid c_{\theta},y_{<t})}{\pi_{\theta_{\mathrm{old}}}(y_t\mid c_{\theta},y_{<t})}
$$

**符号说明**

- $\mathcal{L}_{\theta}$：用于更新学生参数 θ 的 PPO 裁剪损失。
- $\mathbb{E}$：对学生 rollout 数据及相关采样随机性的期望。
- $n$：学生响应的 token 数量。
- $t$：学生响应 token 的位置索引。
- $\widehat{A}_t$：第 t 个学生位置的固定蒸馏优势，即目标对数概率减去旧学生对数概率。
- $\widetilde{\ell}^{\phi}_t$：学生长度的目标对数概率；对齐时来自教师，未对齐时来自旧学生自身。
- $r_t$：新学生策略相对旧学生策略在已采样 token 上的重要性采样比率。
- $\pi_{\theta}$：当前正在优化的学生策略。
- $\pi_{\theta_{\mathrm{old}}}$：生成当前 rollout 批次或更新前冻结的旧学生策略。
- $c_{\theta}$：由学生聊天模板构造的输入上下文文本。
- $y_{<t}$：学生位置 t 之前已经生成的响应 token 前缀。
- $\epsilon$：PPO 比率裁剪半径，将有效比率限制在 1 附近的区间。
- $\operatorname{clip}$：把重要性比率截断到给定上下界的裁剪算子。

<div class="equation-explanation" markdown="1">

**直观理解**：教师与旧学生对同一已对齐 token 的对数概率差决定更新方向和强度，重要性比率则修正“数据由旧策略生成、参数已变为新策略”的分布差异。取未裁剪项和裁剪项中的较保守者，可限制重复使用 rollout 批次时的策略变化；未对齐位置因目标等于旧学生概率而具有零优势。<br>
**原文位置**：第 2.2 节，公式 (7) 至 (9)，核心优化目标为公式 (9)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：概念上的蒸馏目标是在学生在线样本上累加 $\log\pi_{\theta}(y_t\mid c_{\theta},y_{<t})-\widetilde{\ell}^{\phi}_t$。当师生分词器相同时，每个位置都可对齐，该目标退化为学生相对于教师的反向 KL 散度 $D_{\mathrm{KL}}(\pi_{\theta}(\cdot\mid c_{\theta})\parallel\pi_{\phi}(\cdot\mid c_{\phi}))$；反向 KL 的采样来自学生，因此会重点修正学生实际访问到的输出区域。

分词器不同时，完整的逐 token KL 无法直接逐项对应，SimpleOPD只在局部切分一致的位置采用教师概率。实际优化将 rollout 时的学生参数冻结为 $\theta_{\mathrm{old}}$，构造固定优势 $\widehat{A}_t$，再最小化 PPO 裁剪损失；这使同一批 rollout 可以进行多次梯度更新。必须注意，该目标是严格对齐位置上的反向 KL 代理，而不是不同分词器之间完整序列分布 KL 的精确计算。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双模板同字符串评估**

学生和教师分别使用 $\mathcal{C}_{\theta}$ 与 $\mathcal{C}_{\phi}$ 构造上下文，但教师评分的响应部分始终是学生解码得到的同一字符串 $s$。教师通过 $\mathcal{E}_{\phi}(s\mid c_{\phi})$ 在自身词表中重新分词，从而保留教师原生聊天格式和概率语义。

> 直观理解：该设计把“回答内容相同”与“模型输入格式相同”区分开来：内容必须一致，模板和词表则允许各用各的。这减少了模板错配对教师判断的干扰。

**2. 严格文本跨度对齐器**

对齐器比较 $P_{\theta}(t)$、$P_{\phi}(i)$ 和当前文本跨度，只接受覆盖共享字符串 $s$ 中相同起止偏移的 token 对。由于两侧都是 $s$ 的有序分段，所得 $\mathcal{M}$ 是部分一对一映射，并可由双指针线性扫描枚举。

> 直观理解：模块不试图建立完整词表映射，而是寻找当前回答中真实出现的局部共同切分。其代价是丢弃部分监督，但换来概率归属明确，避免把一个整体 token 的概率武断地摊给多个 token。

**3. 零优势回退与 PPO 更新器**

若 $a_t=1$，目标 $\widetilde{\ell}^{\phi}_t$ 取对应教师 token 的对数概率；若 $a_t=0$，则取 $\log\pi_{\theta_{\mathrm{old}}}(y_t\mid c_{\theta},y_{<t})$。后一设置令未对齐位置的固定优势恰为零，并允许在同一 rollout 批次上通过 PPO 重要性校正进行多轮参数更新。

> 直观理解：无法可靠翻译的监督被设置为“不奖不罚”，而不是用错误目标训练。旧策略作为生成数据时的参照，PPO 裁剪则控制新策略不要在重复使用同一批响应时变化过猛。

**训练与推理**

训练时，对每个输入对话 $\mathbf{x}$，学生 rollout 策略先在 $c_{\theta}$ 上采样响应并解码为 $s$；教师随后在自己的 $c_{\phi}$ 和分词器下重新编码同一响应，输出逐 token 对数概率。系统以文本偏移扫描得到 $\mathcal{M}$，将教师概率填入对齐的学生位置，并在未对齐位置填入旧学生概率；由此计算 $\widehat{A}_t$ 和 $r_t$，通过裁剪目标更新 $\theta$。更新后的学生可继续生成下一批在线样本，形成“学生生成、教师评分、局部对齐、策略更新”的循环。

原文所给方法不要求推理阶段保留教师、对齐器或 PPO 组件；完成蒸馏后，输出是更新后的学生策略 $\pi_{\theta}$，可按常规方式使用学生自身聊天模板和分词器生成响应。教师主要承担训练期评分角色，但所给章节未进一步明确部署配置、解码参数或推理阶段是否采用额外策略。

**复现信息**

复现该方法时最关键的实现约束有三项。第一，师生分别应用各自聊天模板，且必须把学生响应先解码为未经修改的字符串 $s$，再交由教师重编码；原文明确不做额外清理或规范化，否则字符偏移可能失去一致性。第二，对齐应基于 token 的增量文本跨度及其在 $s$ 中的起止偏移，并按线性双指针方式扫描；部分重叠 token 不得拆分、合并或平均概率。第三，多轮更新同一 rollout 批次时，未对齐位置必须使用预更新策略 $\pi_{\theta_{\mathrm{old}}}$ 的对数概率作为回退值，以确保相应 $\widehat{A}_t=0$，同时使用 PPO 的重要性比率和裁剪。

覆盖率 $\rho=|\mathcal{M}|/n$ 应作为监督可用性的诊断量：它表示学生响应 token 中实际获得教师监督的比例，而不是任务正确率。所给章节没有明确报告具体的裁剪系数 $\epsilon$、优化器、学习率、批量大小、每批更新轮数、生成温度或最大上下文长度，因此这些设置不能仅据该节推断。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 训练数据：共5,528道数学证明题，包括Open Proof Corpus的63题、Art of Problem Solving社区的2,948题、在线数学竞赛训练书籍的900题，以及Shuzhimi论坛和Evan Chen奥数材料的617题。它们只用于提供证明型提示；原文未明确报告训练集划分、去重方式或与评测集的污染检查。
- IMO-Bench评测：ProofBench用于检验开放式自然语言证明能力，答案不能由简单规则直接验证；AnswerBench用于检验具有可验证答案的数学推理能力。ProofBench由DeepSeek-V4-Flash判分并对同一证明评估4次后取平均，AnswerBench先经规则验证器检查，错误时再交给GPT-OSS-120B评估。
- 竞赛答案评测：AIME25与AMOBench都是可验证数学基准，用于检验学生是否不仅模仿证明文风，而且提高竞赛题求解正确性。两者均采用规则验证优先、GPT-OSS-120B复核规则判错样本的流程，并报告8次生成的平均结果；原文未在所给章节中明确报告题目数量与具体划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**ProofBench@$4$**

衡量自然语言数学证明质量。由于证明不是可直接规则验证的短答案，论文使用模型裁判评分，并对4次生成或评估取平均；它主要反映论证完整性和正确性，但也会受到裁判模型偏差影响。 （越高越好，因为更高分表示生成的证明更可能被裁判认定为正确且充分。）

</div>
<div class="metric-item" markdown="1">

**AnswerBench@$8$**

衡量IMO-Bench中可验证答案题的求解表现，报告8次生成的平均结果；规则验证器先确认答案，规则判错后再由GPT-OSS-120B复核。 （越高越好，因为更高分表示模型在重复采样下给出正确答案的比例或平均得分更高。）

</div>
<div class="metric-item" markdown="1">

**竞赛正确性指标AIME25@$8$与AMOBench@$8$**

两项指标分别衡量AIME 2025题目和AMO类竞赛题上的可验证求解能力，均报告8次生成的平均结果。将它们与ProofBench并列可以区分开放式证明迁移和短答案求解迁移。 （越高越好，因为分数提高意味着模型在相应竞赛题上更频繁地产生可验证的正确答案。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 同分词器蒸馏：SU-01到Qwen3-4B与Qwen3-30B-A3B

<div class="result-value" markdown="1">

作者报告，Qwen3-4B经OPD后，ProofBench、AnswerBench、AIME25和AMOBench分别从$11.42$、$47.50$、$71.25$、$23.00$提高到$23.72$、$64.50$、$90.83$、$35.00$；Qwen3-30B-A3B则分别从$13.80$、$59.13$、$88.33$、$36.50$提高到$36.47$、$74.46$、$93.75$、$52.75$。

</div>

这组受控比较表明，在师生共享Qwen分词体系时，在线蒸馏同时改善开放式证明和可验证答案任务，而且小模型与较大混合专家模型均受益。较大的Qwen3-30B-A3B在ProofBench上增加$22.67$分，但该结果不能单独证明模型规模必然带来更高蒸馏效率，因为两种学生的初始能力、参数结构和训练轨迹并未受到严格控制。

<div class="result-source" markdown="1">

来源：第4.2节，表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Among the same-tokenizer models, Qwen3-4B-OPD gains 12.30 points on ProofBench, 17.00 points on AnswerBench, and 19.58 points on AIME25.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨分词器蒸馏：SU-01到Qwen3.5与Intern-S2-Preview

<div class="result-value" markdown="1">

作者报告，Qwen3.5-35B-A3B-OPD在ProofBench、AnswerBench、AIME25和AMOBench上相对基础模型分别提高$15.61$、$6.99$、$2.06$和$4.00$分；Intern-S2-OPD分别提高$22.80$、$4.07$、$6.67$和$1.50$分，其中ProofBench由$21.70$升至$44.50$，接近教师的$45.00$，AnswerBench与AIME25分别达到$80.10$和$95.00$。

</div>

这些结果直接支持方法不要求师生共享词表：可对齐位置上的监督足以向不同分词器学生迁移相当一部分证明能力。Intern-S2在两个答案型基准上超过SU-01，只说明其在当前评测协议和采样次数下得分更高，不能证明学生已全面超越教师，也不能排除基础模型原有能力和裁判误差的影响。

<div class="result-source" markdown="1">

来源：第4.2节，表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Intern-S2-Preview exhibits the largest ProofBench gain, improving by 22.80 points from 21.70 to 44.50, nearly matching the teacher’s score of 45.00.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨模型家族蒸馏：SU-01到GLM-4.7-Flash与Gemma-4-26B-A4B

<div class="result-value" markdown="1">

作者报告，GLM-4.7-OPD的ProofBench由$30.8$升至$39.7$，AnswerBench由$69.6$升至$72.0$；Gemma-4-26B-A4B-OPD的ProofBench由$25.5$升至$34.2$，但AnswerBench由$68.8$降至$67.5$。

</div>

GLM在两个基准上均提高，而使用SentencePiece且与教师分词差异更大的Gemma只提高证明分数、答案分数反而下降。这说明跨家族证明知识可以迁移，但收益并非对所有能力和分词器都一致。作者把差异与分词器不匹配联系起来是合理解释，但实验没有在固定模型结构下只改变分词器，因此尚不能建立因果关系。

<div class="result-source" markdown="1">

来源：第4.3节，图7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Gemma-4-26B-A4B-OPD also achieves a substantial ProofBench gain, rising from 25.5 to 34.2, although its AnswerBench score decreases from 68.8 to 67.5.

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

- 未蒸馏学生模型：包括Qwen3、Qwen3.5、Intern-S2-Preview、GLM-4.7-Flash和Gemma-4-26B-A4B。它们与各自的OPD版本逐一比较，直接衡量蒸馏带来的模型内增量，是最关键的对照。
- 教师SU-01：基于Qwen3-30B-A3B的$30\mathrm{B}$-$\mathrm{A3B}$推理模型。它既提供逐词元监督，也作为能力上界参照，用来判断学生是否接近教师；但学生在个别指标上超过教师并不等于整体能力更强。
- OPD加特殊词元掩码：在Intern-S2-Preview上屏蔽结构和终止词元的蒸馏损失，用于判断不强迫学生匹配教师的终止行为是否足以控制长度膨胀。
- 强前沿模型比较：论文在Gemini-2.5-Pro判分的ProofBench结果中比较Intern-S2-OPD与Gemini-2.5-Pro、GPT-5、SU-01和DeepSeek-V3.2-Speciale，用于定位其开放式证明能力；所给文字未列出这些外部模型的完整数值，因此该比较不能替代与未蒸馏学生的受控对照。

**实验想回答的问题**

- SimpleOPD能否把SU-01的数学证明与答案推理能力稳定迁移到不同规模的学生模型，并且在教师与学生使用相同词表和不同分词器时都取得提升？
- 直接在策略蒸馏是否会造成输出长度膨胀、重复和截断，以及特殊词元掩码与学生参考KL损失能否分别缓解这些训练退化现象？

**实验实现**

教师为SU-01，训练响应由当前学生策略在线采样，教师仅在师生分词结果能够对齐的位置提供词元级监督。实验同时覆盖同词表的Qwen3学生，以及分词器或模型家族不同的Qwen3.5、Intern-S2-Preview、GLM-4.7-Flash和Gemma-4-26B-A4B。训练基于Slime，进行100次采样迭代；每批64个提示，每个提示采样4个响应，恒定学习率为$10^{-6}$，PPO裁剪系数为$0.2$，每次采样后更新策略4次。Qwen系列最长训练响应为32K词元，GLM-4.7和Gemma-4为6K词元。学生参考KL系数在Qwen系列和Intern-S2-Preview上设为$0.5$，在GLM与Gemma上设为$1.0$。

评测生成采用温度$1.0$、top-p $0.95$、重复惩罚$1.0$和最多160,000词元。ProofBench主要由DeepSeek-V4-Flash裁判，对同一证明评估4次并取平均；AnswerBench、AIME25和AMOBench先用规则验证器，规则判错时再由GPT-OSS-120B评估，报告8次生成的平均值。最佳检查点按AIME@$4$与AnswerBench@$1$的平均分选择，这会使最终结果对这两个验证指标存在选择偏好；ProofBench另以Gemini-2.5-Pro裁判进行一次补充比较。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Intern-S2-Preview上仅加入特殊词元掩码 | 相对未蒸馏模型，OPD加特殊词元掩码把ProofBench从$21.70$提高到$38.10$、AnswerBench从$76.03$提高到$77.60$、AIME25从$88.33$提高到$95.00$，对应增益为$16.40$、$1.57$和$6.67$分；但后期截断率仍快速上升。 | 该实验隔离了结构词元和终止词元上的蒸馏约束。屏蔽这些位置后，学生不必精确模仿长上下文教师的结束行为，因此长度不稳定有所缓解；然而截断仍在后期恶化，说明问题不只来自终止词元，还来自整个学生分布逐渐偏离初始策略。 | 第4.1.2节，表1与图5<br><span class="experiment-evidence">The results suggest that the masking strategy helps mitigate length-related instability.</span> |
| Intern-S2-Preview上加入系数为$0.5$的学生参考KL损失 | OPD加参考KL后，ProofBench由$21.70$提高到$38.50$，AnswerBench由$76.03$提高到$79.10$，AIME25由$88.33$提高到$95.80$，对应增益为$16.80$、$3.07$和$7.47$分；作者同时报告截断率降至接近零。 | 参考KL惩罚学生策略过度偏离其训练前分布，因此检验的是“保留学生原有生成习惯”能否稳定在线蒸馏。它在三个任务指标上均略优于只做特殊词元掩码，并显著控制截断，支持全分布约束比局部终止词元处理更有效；但表1没有报告重复率和平均长度的具体数值，也未提供KL系数扫描。 | 第4.1.3节，表1与图6<br><span class="experiment-evidence">Specifically, OPD + Ref KL improves ProofBench@4 from 21.70 to 38.50, and further raises AnswerBench@8 and AIME25@8 to 79.10 and 95.80, respectively.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops an on-policy distillation post-training method for long-context language-model reasoning.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`fe87866b4a1a6df56169833417280ff6396092258694bd4cf8f0342919185977`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
