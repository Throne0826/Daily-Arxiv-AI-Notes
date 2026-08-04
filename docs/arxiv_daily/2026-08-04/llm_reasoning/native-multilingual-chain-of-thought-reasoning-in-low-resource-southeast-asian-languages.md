---
title: "[论文解读] Native Multilingual Chain-of-Thought Reasoning in Low-Resource Southeast Asian Languages"
description: "[arXiv 2608.00533][LLM Reasoning] 本文针对低资源东南亚语言在复杂推理中转回英语、且常规适配可能破坏既有能力的问题，提出通过动态翻译推理轨迹与跨语言语义对齐来迁移英语推理能力的后训练框架 OSCD。"
arxiv_id: "2608.00533"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:03:30.610358+00:00"
source_sha256: "f72a6305881cddcdf6df7fe9cdb4ae738bee6be41f02a6bf234d717f903cad60"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "多语言大语言模型"
  - "低资源东南亚语言"
  - "原生思维链推理"
  - "跨语言坍塌"
  - "强化学习冷启动"
  - "灾难性遗忘"
  - "跨语言表示漂移"
  - "联合嵌入语义对齐"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.00533</p>

# Native Multilingual Chain-of-Thought Reasoning in Low-Resource Southeast Asian Languages

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Sean Gip Lim, William Chandra Tjhi, Hai Leong Chieu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Nanyang Technological University；DSO National Laboratories</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.00533v1) · [PDF 下载](https://arxiv.org/pdf/2608.00533v1) · **关键词** 多语言大语言模型, 低资源东南亚语言, 原生思维链推理, 跨语言坍塌, 强化学习冷启动, 灾难性遗忘, 跨语言表示漂移, 联合嵌入语义对齐<br>
**代码**: [https://github.com/SG-Lim/OSCD](https://github.com/SG-Lim/OSCD)

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

本文针对低资源东南亚语言在复杂推理中转回英语、且常规适配可能破坏既有能力的问题，提出通过动态翻译推理轨迹与跨语言语义对齐来迁移英语推理能力的后训练框架 OSCD。

**不用术语来说**：许多多语言大模型可以用用户的母语读题和作答，却会在真正需要多步思考时改用英语书写中间过程。对于教育和科研等需要检查推理步骤的场景，这会降低可理解性与可用性。直接让模型从反馈中学习又缺少足够的母语成功样本，而用翻译数据常规微调则可能使模型遗忘原有的英语推理能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 Onramp-Sequence Cross-Distillation（OSCD）：在生成式训练过程中，通过集成的翻译智能体循环，将高资源语言的动态推理轨迹本地化到低资源语言的词汇空间，为母语推理训练提供可用的成功样本。
- 在轨迹本地化之外加入联合嵌入语义对齐，使语义相同的高资源语言与目标语言推理轨迹在表示空间中更接近，以兼顾低资源语言能力迁移、语言一致性和原有高资源语言能力的保持。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于多语言大语言模型的复杂推理与后训练研究。思维链推理要求模型在给出最终答案前生成可检查的中间推导，但现有推理能力主要建立在英语等高资源语言的数据与表示空间上；当模型以训练资源稀缺的东南亚语言处理多步数学问题时，中间推理常系统性切换回英语，即“跨语言坍塌”。这不仅降低母语用户在教育、研究等场景中理解和核验推理过程的能力，也使低资源语言难以直接采用依赖成功轨迹和奖励信号的策略优化。论文因此将问题置于一个双重约束下：既要把英语主导模型已有的推理能力迁移到低资源语言，又要避免常规多语言微调破坏模型原有的高资源语言能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**思维链推理（Chain-of-Thought, CoT）**

模型在最终答案之前显式生成一系列中间推导步骤，以完成需要多步逻辑或计算的问题。本文关注的不只是答案是否正确，还关注这些步骤能否持续使用用户的目标语言表达。

</div>
<div class="concept-item" markdown="1">

**跨语言坍塌（cross-lingual collapse）**

多语言模型虽然能读懂低资源语言输入，却在推理难度上升时把中间过程切换到英语等高资源语言。它反映的是模型推理路径对高资源语言的结构性依赖，而不只是偶发的代码切换。

</div>
<div class="concept-item" markdown="1">

**灾难性遗忘与表示漂移**

灾难性遗忘指模型学习新语言数据后，原有知识或能力明显退化；本文将其风险与跨语言表示漂移联系起来，即语义相同的平行文本在隐藏表示空间中落入彼此分离的区域。直接进行监督微调或继续预训练可能进一步扰动既有的高资源语言表示几何。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是以低资源东南亚语言呈现的开放式、多步数学推理问题，目标输出包括正确答案以及全程保持该目标语言的原生思维链。基础模型被假定已经在英语等高资源语言中具备较强推理能力，但缺少足够的低资源语言成功轨迹：这会造成强化学习的冷启动，因为模型难以采样到可获得有效奖励的母语推理过程；若直接使用合成或整理后的多语言数据进行监督微调，又可能因跨语言隐藏表示不对齐而引发表示漂移和灾难性遗忘。论文据此研究如何在后训练阶段迁移高资源推理轨迹、扩大低资源语言的推理搜索空间，并同时保持原有高资源语言智能。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Park et al. (2026), Cross-lingual collapse: how language-centric foundation models shape reasoning in large language models**: 为本文所讨论的核心现象提供直接背景：语言中心化的基础模型会使复杂推理过程回退到高资源语言。本文进一步把该现象视为低资源母语推理后训练中的冷启动障碍，并尝试通过跨语言推理轨迹迁移解决。
- **Lim et al. (2025), Language-specific latent process hinders cross-lingual performance**: 与本文的表示层假设直接相关：不同语言可能形成彼此分离的潜在处理过程，使语义相同的文本不能自然共享推理表示。本文据此强调需要对平行推理轨迹进行联合嵌入语义对齐，而不仅是增加翻译后的训练文本。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

低资源东南亚语言缺少足以训练原生复杂推理能力的数据。受英语中心偏置影响，多语言模型遇到复杂逻辑转换时往往将思维链切换为英语，使母语用户难以检查关键中间步骤；这在强调推理过程可解释性的教育与科研场景中尤其不利。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于奖励的策略优化**：让模型采样多条推理轨迹，根据答案正确性等奖励信号提高成功策略的概率；这类方法通常依赖模型已有的知识空间和成功推理轨迹，以获得足够有效的训练样本。
- **监督微调或继续预训练**：使用人工整理或合成的多语言数据继续训练模型，通过目标语言文本直接调整参数，使模型学习目标语言的生成形式与任务行为。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 策略优化存在冷启动障碍：模型本来就难以生成复杂任务中的低资源语言成功轨迹，因此无法获得足够的正奖励，也就难以把策略从既有的英语推理路径迁移到母语路径。
- 朴素的监督微调或继续预训练没有显式弥合平行文本之间的表示差异；语义相同但语言不同的文本可能位于分离的嵌入子空间，持续训练会加剧跨语言表示漂移，并可能引发灾难性遗忘，损害已经建立的高资源语言表示结构与推理能力。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方案尚未同时解决“低资源语言缺少可用于启动训练的成功推理轨迹”和“跨语言适配会扰动既有表示空间”两个相互关联的问题。所缺少的是一种能够持续产生母语化推理监督、又能明确约束平行推理轨迹保持语义等价的后训练机制。

</div>
<div markdown="1"><span>核心问题</span>

能否把英语主导模型已有的复杂推理轨迹稳定地迁移到低资源东南亚语言，使模型形成原生母语思维链并减少回退到英语，同时避免破坏其原有高资源语言推理能力？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把“会推理”和“用哪种语言表达推理”部分解耦：先利用模型已经掌握的高资源语言推理路径，再在生成过程中将这些路径动态本地化，为低资源语言提供训练入口；随后把原轨迹与本地化轨迹的语义表示拉近，使模型学到的是同一推理在不同语言中的对应关系，而不只是表面翻译。这样既补充了母语成功样本，也减少了学习目标语言时对原有表示几何结构的无约束改写。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

OSCD（Onramp-Sequence Cross-Distillation）的输入是面向低资源目标语言 $l\in\mathcal{L}$ 的提示 $p$，输出是能够用该语言书写中间推理过程、同时尽量保持原有解题能力的学生模型 $\pi_\theta$。方法分为两个阶段：首先由高资源参考模型 $\pi_\phi$ 动态生成完整回答，将其中的思维链与最终答案分离，只翻译思维链，再按原结构重建本地化训练序列 $c'$；随后以重建序列进行全序列监督训练，并在教师与学生完成推理的位置上对齐隐藏表示。学生初始化为教师，因此训练不是从零学习推理，而是把教师已有的推理轨迹迁移到低资源语言的词汇和表示空间中。
直观地说，OSCD先让原模型用擅长的语言解题，再把“草稿推理”改写成目标语言，但保留原来的最终答案作为稳定锚点；之后不仅要求学生逐字学会这份本地化草稿，还要求学生读完目标语言草稿后的内部理解接近教师读完原草稿后的内部理解。前者解决“能否生成目标语言推理”，后者缓解“换一种语言后是否把同一推理理解成了不同东西”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 参考推理轨迹生成

从 $\pi_\phi(\cdot\mid p)$ 采样完成序列 $c$，再通过解码函数 $\mathcal{D}$ 将离散 token 序列转换为文本 $s$。该阶段在训练过程中动态生成参考样本，而不是仅依赖预先固定的翻译语料。

<div class="method-step__io" markdown="1">

**输入**：目标语言提示 $p$、目标语言标识 $l$，以及高资源参考模型 $\pi_\phi$。<br>
**输出**：包含中间思维链和最终答案的参考完成序列 $c$ 及其文本形式 $s=\mathcal{D}(c)$。

</div>

**直观理解**：教师先完整做一遍题，提供一条与当前提示匹配的解题过程。动态生成意味着训练样本可以随提示产生，而不必提前人工整理所有推理文本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结构解析与思维链局部翻译

利用开始和结束 think 标签把文本拆成推理字符串 $s_r$ 与答案字符串 $s_a$，再调用外部翻译函数 $\mathcal{T}$，得到目标语言推理 $s'_r=\mathcal{T}(s_r,l)$。翻译被严格限制在推理部分，答案 $s_a$ 保持教师原文不变。

<div class="method-step__io" markdown="1">

**输入**：参考文本 $s$、结构分隔符集合 $\Delta=\{\delta_{\mathrm{open}},\delta_{\mathrm{close}}\}$，以及目标语言 $l$。<br>
**输出**：目标语言推理字符串 $s'_r$ 与未经修改的教师答案字符串 $s_a$。

</div>

**直观理解**：系统只改写“草稿”，不改动教师已经给出的结论。这样可以减少翻译器改坏答案格式、数值或结论所带来的监督噪声。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 变异完成序列重建

分别重新编码推理和答案，并按照“开始标签、目标语言推理、结束标签、原答案”的顺序拼接为 $c'$。受控编码与有序连接 $\oplus$ 保留原完成序列的推理边界，使后续模型仍能区分内部推理和最终作答。

<div class="method-step__io" markdown="1">

**输入**：目标语言推理 $s'_r$、原答案 $s_a$、结构分隔符和受控编码函数 $\mathcal{E}^{*}$。<br>
**输出**：用于监督微调的本地化完成序列 $c'$。

</div>

**直观理解**：这一步把翻译后的草稿装回教师回答的原有模板中。模型因此看到的是结构完整的训练答案，而不是彼此脱节的翻译片段。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多目标跨语言蒸馏

对 $c'$ 的全部 token 计算自回归交叉熵 $\mathcal{L}_{\mathrm{CE}}$；同时分别运行教师和学生，在结束 think 标签处提取最后一层隐藏状态，并以余弦距离构造 $\mathcal{L}_{\mathrm{JEPA}}$。两项损失经权重 $\lambda_{\mathrm{CE}}$ 与 $\lambda_{\mathrm{JEPA}}$ 加权后联合反向传播。

<div class="method-step__io" markdown="1">

**输入**：提示 $p$、本地化序列 $c'$、教师原推理 $s_r$、学生本地化推理 $s'_r$，以及初始化自教师的学生模型 $\pi_\theta$。<br>
**输出**：能够生成目标语言推理、且推理末端语义表示接近教师的学生模型 $\pi_\theta$。

</div>

**直观理解**：学生既要学会目标语言的表达形式，也要保证表达变化没有改变内部推理含义。只做前一项容易变成机械模仿翻译文本，加入后一项则给“意思是否一致”增加约束。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 思维链局部变异与序列重建

$$
\begin{aligned}(s_r,s_a)&=\operatorname{Split}\!\left(\mathcal{D}(c),\Delta\right),\\ s'_r&=\mathcal{T}(s_r,l),\\ c'&=\delta_{\mathrm{open}}\oplus\mathcal{E}^{*}(s'_r)\oplus\delta_{\mathrm{close}}\oplus\mathcal{E}^{*}(s_a).\end{aligned}
$$

**符号说明**

- $c$：由参考模型采样得到的原始完成 token 序列。
- $\mathcal{D}$：把 token 序列转换为文本字符串的解码函数。
- $\Delta=\{\delta_{\mathrm{open}},\delta_{\mathrm{close}}\}$：标记思维链起止边界的结构分隔符集合。
- $s_r,\,s_a$：从原始完成中分离出的推理字符串和答案字符串。
- $l$：需要生成本地化思维链的目标语言。
- $\mathcal{T}$：以目标语言为条件、仅处理推理字符串的外部翻译函数。
- $s'_r$：翻译到目标低资源语言后的推理字符串。
- $\mathcal{E}^{*}$：将文本片段映射回离散 token 空间的受控编码函数。
- $\oplus$：保持指定顺序的 token 序列拼接操作。
- $c'$：由目标语言推理和教师原答案组成的变异完成序列。

<div class="equation-explanation" markdown="1">

**直观理解**：第一行从教师回答中取出“推理”和“答案”，第二行只翻译推理，第三行把翻译结果放回原有边界并接上未修改答案。该式明确了 OSCD 的关键数据构造原则：改变用于推理的语言媒介，同时尽可能固定任务结论和输出结构。<br>
**原文位置**：Methodology，Rollout with Sequence Mutation，公式（1）至（3）

</div>

</div>

<div class="equation-block" markdown="1">

#### 全序列学习与联合嵌入语义对齐目标

$$
\begin{aligned}\mathcal{L}_{\mathrm{CE}}&=-\frac{1}{|c'|}\sum_{t=0}^{|c'|-1}\log\pi_{\theta}\!\left(c'_t\mid p,c'_{<t}\right),\\ \mathcal{L}_{\mathrm{JEPA}}&=1-\frac{h^S_{k'}\cdot h^T_k}{\lVert h^S_{k'}\rVert\,\lVert h^T_k\rVert},\\ \mathcal{L}_{\mathrm{total}}&=\lambda_{\mathrm{CE}}\mathcal{L}_{\mathrm{CE}}+\lambda_{\mathrm{JEPA}}\mathcal{L}_{\mathrm{JEPA}}.\end{aligned}
$$

**符号说明**

- $\pi_\theta$：待优化的学生模型，其参数初始化自参考教师模型。
- $p$：条件提示。
- $c'_t,\,c'_{<t}$：本地化完成序列在位置 $t$ 的目标 token，以及该位置之前的真实 token 前缀。
- $|c'|$：重建完成序列的 token 数，用于对序列损失取平均。
- $h^S_{k'}$：学生读取目标语言推理后，在结束 think 标签索引 $k'$ 处的最后一层隐藏状态。
- $h^T_k$：教师读取原语言推理后，在结束 think 标签索引 $k$ 处的最后一层隐藏状态。
- $\mathcal{L}_{\mathrm{CE}}$：要求学生复现完整本地化完成序列的平均交叉熵损失。
- $\mathcal{L}_{\mathrm{JEPA}}$：教师与学生推理汇总表示之间的余弦距离；方向越一致，该值越小。
- $\lambda_{\mathrm{CE}},\,\lambda_{\mathrm{JEPA}}$：分别控制语言序列学习与跨语言语义对齐强度的超参数权重。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项让学生能够逐 token 写出目标语言推理和稳定答案；第二项比较教师与学生“完成推理时”的内部向量方向，使两种语言的轨迹汇聚到相近语义。总损失同时优化外部文本行为和内部推理表示，避免只追求译文表面相似，或只追求抽象表示而不会实际生成目标语言。<br>
**原文位置**：Methodology，Multi-Objective Cross-Distillation，公式（4）至（6）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练最小化 $\mathcal{L}_{\mathrm{total}}=\lambda_{\mathrm{CE}}\mathcal{L}_{\mathrm{CE}}+\lambda_{\mathrm{JEPA}}\mathcal{L}_{\mathrm{JEPA}}$。其中，$\mathcal{L}_{\mathrm{CE}}$ 是直接的生成监督，梯度推动学生在给定提示和真实前缀时提高本地化序列 token 的概率；$\mathcal{L}_{\mathrm{JEPA}}$ 是表示层正则项，梯度推动学生在结束 think 标签处的隐藏状态靠近教师对应状态。论文实验中两项权重均设为 $1.0$，因此没有人为强调其中一项；但两项承担不同职责，交叉熵负责习得目标语言表达，联合嵌入对齐负责约束跨语言语义漂移。
这里的“蒸馏”不只是复制教师输出：教师提供原始推理、答案和内部表示，学生学习的是经过语言变异后的序列，同时仍以教师语义为参照。结束标签级对齐是一种序列级近似，它假设该位置汇总了此前推理；这一设计避免建立通常不可得的逐 token 翻译对应关系，但也意味着目标函数不会显式检查本地化思维链中的每一个中间步骤是否与教师逐步等价。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Rollout with Sequence Mutation**

该模块从参考模型的在线 rollout 中取得完成序列，通过结构标签定位思维链，仅将 $s_r$ 映射到目标语言词汇子空间 $\mathcal{V}_L$，再与保持不变的 $s_a$ 重组。所谓 sequence mutation 指改变完成序列中的推理语言，而不改变其宏观结构和答案锚点。

> 直观理解：低资源语言可能缺少足够的高质量长推理数据，因此模块借用高资源模型现成的解题轨迹来制造训练样本。保留答案不能从形式上保证翻译后的每一步都完全正确，但能降低同时翻译推理与答案时产生的双重误差。

**2. 全序列交叉熵蒸馏**

学生对重建完成 $c'$ 进行标准 teacher-forcing，即在给定 $p$ 和真实前缀 $c'_{<t}$ 时预测下一 token $c'_t$，并在整个完成序列上平均负对数似然。监督覆盖本地化思维链、结构标签和最终答案，使目标语言生成能力与答案格式共同受到训练。

> 直观理解：它直接教模型“下一步该写什么”，因而是获得目标语言思维链生成能力的主要信号。由于学生从教师参数初始化且答案未被翻译，训练仍被约束在教师原有行为附近，但这种设计不能单独排除跨语言表示漂移。

**3. 结束标签联合嵌入对齐**

教师读取原语言推理、学生读取目标语言推理后，方法在各自结束 think 标签索引 $k$ 和 $k'$ 处提取最后一层隐藏状态 $h_k^T$ 与 $h_{k'}^S$，并最小化两者的余弦距离。作者把 $\delta_{\mathrm{close}}$ 视为答案生成前汇总推理语义的信息瓶颈，因此只对齐这一位置，而不强制不同语言的每个 token 一一对应。

> 直观理解：不同语言的词序和 token 数通常不同，逐词对齐会施加不合理约束；结束标签则像读完草稿后的总结节点。让两个总结节点接近，可以要求学生与教师形成相似的整体理解，同时保留各语言自由组织句子的空间。

**训练与推理**

训练时，对每个目标语言提示 $p$，先由参考模型 $\pi_\phi$ 进行生成 rollout，解析完成序列并通过外部翻译函数构造 $c'$；随后教师在原推理轨迹上前向计算，学生在本地化轨迹上前向计算。学生使用完整 $c'$ 接受 teacher-forcing 监督，并在两条轨迹各自的结束 think 标签处计算表示对齐损失，最后对联合目标反向传播。学生参数从教师参数初始化，训练进行 $1$ 个 epoch；原文所称 integrated translator agentic loop 的作用是为动态生成的参考轨迹提供翻译，但所给方法章节没有进一步给出该翻译代理的提示模板、内部工具调用协议或失败重试规则。
推理或基准评测时，使用训练后的学生模型直接根据输入提示自回归生成完成，不再需要教师隐藏状态、交叉熵标签或 JEPA 对齐计算。原文说明生成 rollout 与推理基准采用相应模型开发者推荐的默认推理参数，评测最大完成长度为 $81920$ token；但节选没有明确列出温度、top-$p$、top-$k$ 等具体采样值，因此不能据此完整复现采样分布。

**复现信息**

为公平解释训练规模，论文采用 AdamW、余弦学习率调度和 $2\times10^{-5}$ 的学习率，warmup 比例为 $0.1$，梯度裁剪范数为 $1.0$，数值精度为 BF16。训练提示最长 $4096$ token、训练完成最长 $8192$ token，$\lambda_{\mathrm{CE}}=\lambda_{\mathrm{JEPA}}=1.0$；这些设置决定了可纳入监督的推理长度以及两个目标的相对量级。计算资源为 $4$ 张通过 NVLink 互联的 NVIDIA H200 GPU，每张具有 $141$ GB HBM3e 显存；软件栈包括 PyTorch 2.9.0、DeepSpeed 0.18.4、HuggingFace Transformers 4.57.1 和 vLLM 0.13.0。
复现时最关键、但当前节选未完整报告的部分是外部翻译函数 $\mathcal{T}$ 的具体模型、代理循环配置、译文质量控制方式，以及动态 rollout 的明确采样超参数。受控编码函数 $\mathcal{E}^{*}$ 与结构分隔符的模型相关实现也只给出功能定义；实现者必须确保开始和结束 think 标签使用正确 token 化方式，并分别定位教师索引 $k$ 与学生索引 $k'$，因为翻译后序列长度通常不同，不能假设两个索引相等。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- OpenMathReasoning-tir用于训练。作者仅抽取其中70000个“只有问题”的样本，丢弃原始推理过程和答案，再将问题分别配上中文、英语、菲律宾语、印尼语、泰米尔语、泰语和越南语提示，要求模型用提示对应语言生成中间思维链。该设计测试OSCD能否在缺少现成低资源语言推理轨迹时，通过动态生成和翻译构造训练监督。消融实验另从中建立7500条均衡子集，均匀覆盖中文、英语和印尼语，以降低比较不同组件时的实验成本。
- AIME25是主评测数学竞赛基准之一，被翻译为上述7种语言。所有模型在相同生成结果上接受Any-CoT与Target-CoT两种评分：前者只检查最终答案，后者还要求中间推理维持目标语言，因此该数据集同时测试数学能力与语言遵循能力。
- HMMT25是另一项主评测数学竞赛基准，同样翻译为7种语言并采用相同双模式评分。它用于检查AIME25上的结论能否迁移到另一套高难度、开放式且答案可判定的数学题，而不是局限于单一题集。FLORES-Plus仅被用于附录中的隐藏表示可视化，不承担主准确率评测。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass@5**

每道题生成5次时，至少有一次得到正确最终答案的比例，用来近似模型可达到的推理能力。在Any-CoT模式下不限制推理语言；在Target-CoT模式下，正确答案还必须伴随符合指令的目标语言思维链。 （越高越好，因为更高值表示5次尝试中成功解题的覆盖率更高；但Any-CoT较高本身不能证明模型具备原生目标语言推理能力。）

</div>
<div class="metric-item" markdown="1">

**Mean@5**

同一道题5次生成结果的平均正确表现，用来衡量推理的一致性，而非只看是否偶然成功。它同样分别在Any-CoT与Target-CoT条件下报告。 （越高越好，因为它表示模型在重复采样中更稳定地给出正确结果；Target-CoT版本还要求语言遵循，因此比Any-CoT更严格。）

</div>
<div class="metric-item" markdown="1">

**LRI**

语言保持指数LRI定义为目标语言集合$[1m\mathcal{G}[0m$上转移矩阵对角概率$[1mM_{i,i}[0m$的百分制平均值，即模型在提示语言$[1m\ell_i[0m$中持续完成推理、没有回退到英语等非目标语言的概率。语言由Gemma-SEA-LION-v4-27B-IT充当裁判判定。 （越高越好，取值范围为0至100；高值表示目标语言保持更稳定、语言偏置更弱，但它只度量推理所用语言，不直接代表答案正确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 7种语言上的Target-CoT原生数学推理表现

<div class="result-value" markdown="1">

作者报告OSCD在AIME25和HMMT25上的Target-CoT Pass@5与Mean@5平均获得约2至3倍提升。表2中，Ours-Qwen3-VL-8B的AIME25 Target-CoT Pass@5由基础模型的21.4提高到68.6，Mean@5由17.8提高到47.5；HMMT25对应指标由13.8和11.1提高到41.4和25.6。

</div>

Target-CoT同时要求答案正确和推理语言正确，因此结果表明OSCD主要改善了“能用指定语言正确推理”的联合能力，而不仅是最终答案准确率。由于各语言结果在表2中被平均，这一汇总结果不能证明7种语言均获得相同幅度的收益，也不能排除翻译质量差异对单个语言的影响。

<div class="result-source" markdown="1">

来源：表2，Ours-Qwen3-VL-8B行；“Low-Resource Native Reasoning”节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Ours-Qwen3-VL-8B 73.8 ± 11.0 60.9 ± 13.6 68.6 ± 14.0 47.5 ± 17.9 86.0 43.8 ± 12.2 33.2 ± 10.5 41.4 ± 13.7 25.6 ± 11.7 84.9

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 语言回退缓解与LRI提升

<div class="result-value" markdown="1">

三个OSCD模型均显著提高LRI。以Qwen3-VL-8B为例，AIME25的LRI从24.0升至86.0，HMMT25从23.8升至84.9；作者将整体变化概括为相对基础模型提升2.2至3.6倍。与此同时，该模型的Any-CoT分数有所下降，说明语言保持收益并不等价于所有不约束语言的解题指标都提高。

</div>

基础推理模型常在复杂中间步骤中回退到英语，而较高LRI表明OSCD确实改变了这种默认语言选择。Any-CoT下降提示存在权衡：模型可能不再依赖其最熟悉的英语推理路径。作者将下降解释为语言分布变得更均衡，但实验不能单凭LRI证明模型在目标语言中形成了与母语者完全一致的推理机制。

<div class="result-source" markdown="1">

来源：“Low-Resource Native Reasoning”节；表2；图5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Our models, however, demonstrate consistent mitigation of this bias, achieving a 2.2–3.6 × improvement in LRI relative to model baselines.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 相对900万样本多语SFT基线的数据效率及跨架构泛化

<div class="result-value" markdown="1">

OSCD只使用70000个训练问题，而Qwen-SEA-LION-v4-8B-VL使用900万条多语指令文本对。表2中，Ours-Qwen3-VL-8B在AIME25和HMMT25上的LRI分别为86.0和84.9，高于规模相近基线的65.8和65.5；作者概括为LRI高出约30%。类似方向的Target-CoT或LRI收益也出现在3B、4B和8B模型上。

</div>

这一比较支持OSCD具有较强样本效率，并表明方法不局限于单一模型规模或纯文本架构。不过，70000与900万不是严格受控的等预算比较：模型来源、训练目标、数据质量及训练算力均可能不同，因此结果不能直接证明OSCD在相同计算量下必然优于所有大规模SFT方案。

<div class="result-source" markdown="1">

来源：“Training Efficiency and Generalizability”节；表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Ours-Qwen3-VL-8B, in particular, surpasses Qwen-SEA-LION-v4-8B-VL in LRI by 30%, thus demonstrating the robustness of dynamic OSCD over static SFT pipelines for multilingual acquisition.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主评测只包含翻译后的AIME25和HMMT25数学题，低资源语言文本由翻译构造，尚未验证文化相关、开放式或真实原生写作任务，也未报告母语专家对题目翻译及思维链自然度的系统评估。语言正确性依赖单一LLM裁判，尽管作者截取中间片段并采用确定性温度，仍可能存在语言混合误判。
- 实验最大只扩展到8B参数，作者明确说明受算力限制无法测试更大模型。与900万样本SFT模型的数据效率比较也不是严格控制模型初始化、训练算力和数据质量的等条件实验；消融仅使用7500条、3种语言的缩小数据集，因此组件结论向全部7种语言和完整训练规模推广时仍需验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- SmolLM3-3B、Qwen3-4B-Thinking-2507和Qwen3-VL-8B-Thinking分别作为各OSCD模型的训练前基线。训练前后使用同一基础模型进行比较，可以较直接地衡量OSCD带来的变化；三者还覆盖3B、4B和8B规模、SmolLM3与Qwen3家族，以及纯文本和多模态稠密架构。
- Qwen-SEA-LION-v4-8B-VL是规模相近的多语模型，已在覆盖英语及东南亚语言的900万条样本上进行监督微调。它是有意义的数据效率基线，因为它代表“大规模静态多语语料微调”路线，而OSCD只使用70000个问题样本并动态生成本地化推理轨迹。
- 消融中的仅交叉熵配置$[1m\mathcal{L}_{\mathrm{CE}}[0m$使用非智能体、确定性翻译得到的推理轨迹，近似已有翻译式微调方案。它用于判断改进是否只是来自把高资源推理翻译成目标语言。
- 消融中的移除智能体翻译系统$[1m\mathcal{T}[0m$或移除联合嵌入对齐损失$[1m\mathcal{L}_{\mathrm{JEPA}}[0m$的配置，分别控制翻译质量管理与跨语言表示对齐因素，用于隔离OSCD两个核心组件的作用。

**实验想回答的问题**

- OSCD能否让原本缺乏东南亚语言原生思维链能力的推理模型，在遵守目标语言进行中间推理的条件下，提高开放式、答案可确定的数学推理准确率，并减少回退到英语的现象？
- 相较于大规模静态多语监督微调，OSCD是否具有更高的数据与训练效率；其收益能否跨越不同参数规模、模型家族及文本或多模态架构，同时避免明显损害英语等高资源语言中的既有推理能力？

**实验实现**

主实验在AIME25和HMMT25的7种语言版本上进行，每个完成结果同时接受Any-CoT和Target-CoT评分，并报告Pass@5、Mean@5及适用的标准差。语言判定采用Gemma-SEA-LION-v4-27B-IT作为LLM裁判：作者去除生成序列开头70%和末尾10%，仅分类中间20%的关键推理片段，以减少复述原生提示造成的假阳性；发现语言混合或切换时，判定优先归入英语等高资源语言。评分及语言分类温度均为0，以保持确定性。

训练时，本地部署Gemma-SEA-LION-v4-27B-IT并结合翻译智能体$[1m\mathcal{T}[0m$处理动态生成的长推理轨迹。翻译温度从0开始，每次失败增加0.1，上限0.4，最多尝试10次。硬件为4张通过NVLink连接的NVIDIA H200 GPU；含模型训练和专用翻译服务在内，SmolLM3-3B、Qwen3-4B与Qwen3-VL-8B分别累计使用384、440和625 GPU小时。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 完整的$[1m\mathcal{L}_{\mathrm{CE+JEPA}}[0m$加智能体翻译，与移除智能体$[1m\mathcal{T}[0m$的配置比较 | 在基于Qwen3-VL-8B-Thinking、覆盖中文、英语和印尼语的7500条均衡子集上，完整配置在两个基准中取得最高Target-CoT和LRI。移除智能体后，作者观察到梯度范数噪声增大、性能严重退化，并称翻译推理速度慢约一倍。 | 该比较隔离了智能体翻译循环的作用：它会重试并调整翻译过程，从而抑制零样本长轨迹翻译中的伪影和波动。结果支持“稳定的动态翻译监督很重要”，但所给节选没有包含表1的具体消融分数，因此无法核验各指标下降的绝对值或统计显著性。 | “Ablation Studies”节；表1；图4b<br><span class="experiment-evidence">Without the agentic translator to suppress zero-shot translation artifacts and variance, we observe increased noise in its respective gradient norms that led to severe performance degradations (Figure 4b), in addition to slower inference speeds by a factor of two.</span> |
| 完整配置与移除联合嵌入语义对齐损失$[1m\mathcal{L}_{\mathrm{JEPA}}[0m$的配置比较 | 保留$[1m\mathcal{L}_{\mathrm{JEPA}}[0m$的完整配置在AIME25和HMMT25上取得最高Target-CoT与LRI；移除该辅助损失后，余弦距离指标发生发散，推理准确率分布更分散且LRI更低。 | 这一消融用于判断仅靠翻译后的交叉熵监督是否足够。结果支持联合嵌入对齐能缩小参考语言与目标语言推理轨迹之间的表示漂移，使训练更稳定并提高语言保持。由于实验只覆盖3种语言且节选未提供表1数值，尚不能据此确定该组件在全部7种语言上的独立增益。 | “Ablation Studies”节；表1；图4d<br><span class="experiment-evidence">Similarly, without a secondary loss to mitigate cross-linguistic representational drifts, models consistently suffer from the divergence of its cosine distance metric (Figure 4d), causing a wider spread in reasoning accuracies and lower LRI scores despite a small set of 3 languages.</span> |

**定性案例**

- 图5的语言回退矩阵显示，基础模型在多数目标语言下倾向进入英语“下沉状态”，中文因预训练网页语料较丰富而略有例外；OSCD模型的对角概率明显增强。该案例直观说明LRI提升来自目标语言保持，而不是模型随机改用另一种非英语语言，但原文节选未提供逐语言矩阵数值。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出跨语言蒸馏与语义对齐后训练方法，以提升低资源语言中的原生数学链式推理能力。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`f72a6305881cddcdf6df7fe9cdb4ae738bee6be41f02a6bf234d717f903cad60`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
