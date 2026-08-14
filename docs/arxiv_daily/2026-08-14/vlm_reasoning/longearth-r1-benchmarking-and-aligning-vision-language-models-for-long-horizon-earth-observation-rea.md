---
title: "[论文解读] LongEarth-R1: Benchmarking and Aligning Vision-Language Models for Long-Horizon Earth Observation Reasoning"
description: "[arXiv 2608.13344][VLM Reasoning] 本文针对长时间序列地球观测图像中多阶段地理变化难以被现有遥感视觉语言模型完整理解的问题，提出覆盖四类推理能力的LongEarth-Bench，并通过结构化监督与时空奖励训练LongEarth-R1。"
arxiv_id: "2608.13344"
announcement_date: "2026-08-14"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:54:12.215317+00:00"
source_sha256: "4f9afee6dd1ca07ad58e2350495b00da3007757ec06335c843dbfd941e8ff1eb"
tags:
  - "VLM Reasoning"
  - "对齐 / RLHF"
  - "LLM 评测"
  - "LLM Reasoning"
  - "长时域地球观测推理"
  - "遥感视觉语言模型"
  - "多时相遥感序列"
  - "时空证据落地"
  - "演化总结"
  - "空间推理"
  - "异常识别"
  - "逻辑预测"
  - "LongEarth-Bench"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.13344</p>

# LongEarth-R1: Benchmarking and Aligning Vision-Language Models for Long-Horizon Earth Observation Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Yupan Ding, Jing Xiao, Zhenyuan Zhang, Chaofeng Chen, Liang Liao, Gui-Song Xia, Mi Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> School of Artificial Intelligence, Wuhan University, Wuhan, China；School of Computer Science, Wuhan University, Wuhan, China；Xi’an University of Electronic Science and Technology, Xi’an, China；State Key Laboratory of Information Engineering in Surveying, Mapping and Remote Sensing, Wuhan University, Wuhan</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13344v1) · [PDF 下载](https://arxiv.org/pdf/2608.13344v1) · **关键词** 长时域地球观测推理, 遥感视觉语言模型, 多时相遥感序列, 时空证据落地, 演化总结, 空间推理, 异常识别, 逻辑预测, LongEarth-Bench<br>


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

本文针对长时间序列地球观测图像中多阶段地理变化难以被现有遥感视觉语言模型完整理解的问题，提出覆盖四类推理能力的LongEarth-Bench，并通过结构化监督与时空奖励训练LongEarth-R1。

**不用术语来说**：当卫星连续拍摄同一地区时，真正重要的往往不是某两张图有什么不同，而是洪水、城市建设或生态恢复在多个时间点上如何发生、扩展和结束。模型需要从最长30帧的序列中找出关键时刻和变化区域，排除季节差异或成像条件造成的假变化，并据此判断缺失状态或后续趋势；现有模型通常只看单幅、成对或较短的图像序列，难以完成这种连续且有证据支撑的判断。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将长时程地球观测推理明确划分为演化总结、空间推理、异常识别和逻辑预测四个递进维度，并据此构建LongEarth-Bench：约12万条问答样本来自11.7万幅独立图像，序列平均包含15.14帧、最长30帧，其中3万条样本提供连接关键帧、变化区域与最终答案的结构化推理标注。
- 作者建立两阶段模型对齐方案：LongEarth通过显式序列标识符和结构化思维链进行监督微调，LongEarth-R1进一步采用组相对策略优化，并结合格式、时间与空间奖励，使训练目标不仅考察最终答案，还约束阶段定位、时间顺序、关键帧选择和变化区域一致性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于遥感视觉语言模型（RSVLM）与多时相地球观测分析的交叉领域。高重访卫星能够连续记录城市建设、洪水演化和生态恢复等过程，但理解这类数据不能只判断两个时刻“哪里变了”：模型还需从较长图像序列中重建事件的多阶段轨迹，确定结论对应的关键帧与变化区域，区分真实地理变化和季节差异、成像条件变化等干扰，并据此推断缺失或后续状态。论文将这种综合能力定义为“长时域地球观测推理”，并将其划分为演化总结、空间推理、异常识别和逻辑预测四个逐步深入的认知维度。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**遥感视觉语言模型（RSVLM）**

同时处理卫星或航空遥感影像与自然语言的模型，可执行图像描述、视觉问答和目标定位等任务。本文关注其输入从单幅或成对影像扩展到长图像序列后的时空推理能力。

</div>
<div class="concept-item" markdown="1">

**多时相遥感序列**

对同一地理区域在不同时间获取并按时间排列的一组影像。序列中的地表差异既可能来自真实变化，也可能来自季节、光照或采集条件，因此不能把所有视觉差异都直接解释为地理事件。

</div>
<div class="concept-item" markdown="1">

**时空证据落地**

模型不仅要给出答案，还要指出答案由哪些时间帧和哪些空间区域支持。通俗地说，模型需要说明“变化何时发生、发生在哪里”，从而降低仅凭整体外观猜测答案的风险。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定按时间顺序排列的同一区域地球观测影像序列，以及针对该序列提出的自然语言问题，模型需要综合跨帧视觉证据生成答案；部分样本还要求形成连接关键帧、时间位置、变化区域与最终结论的结构化推理过程。问题覆盖四类设置：概括地理实体的主要演化阶段；定位变化并判断其空间关系如何演变；识别时间顺序违规、重复帧或上下文干扰；依据已观测轨迹推断缺失状态或后续状态。该设置假定序列具有可用于分析的时间次序，但允许存在季节变化、采集差异和异常排列等干扰，因此模型必须同时进行时间组织、空间定位与证据筛选，而不能只比较首尾两帧。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{I}=(I_1,I_2,\ldots,I_T)$**

按时间排列的地球观测影像序列；$I_t$表示第$t$个时间位置的影像，$T$表示序列长度。该记法用于概括论文的任务输入，并非原文显式给出的公式。

</div>
<div class="notation-item" markdown="1">

**$q$**

针对影像序列提出的自然语言问题。

</div>
<div class="notation-item" markdown="1">

**$a$**

模型依据跨帧、跨区域证据生成的最终答案。

</div>
<div class="notation-item" markdown="1">

**$T$**

输入序列包含的影像帧数；LongEarth-Bench中的序列平均为$15.14$帧，最长为$30$帧。

</div>

</div>

**直接相关的工作**

- **TEOChat**: 属于面向时序地球观测数据的视觉语言助手，代表已有模型从单幅或双时相影像向多时相交互理解扩展的方向；本文指出，现有序列模型通常更偏重识别或描述式问答，尚不足以完整重建多阶段过程并把结论稳定落地到关键帧和变化区域。
- **UniRS**: 尝试通过视觉语言模型统一多时相遥感任务，是本文所处的多时相RSVLM研究脉络之一；LongEarth-Bench进一步把评测重点放在更长序列中的演化总结、空间推理、时间异常识别和逻辑预测。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

高重访率地球观测影像已经能够连续记录城市建设、灾害演化和生态恢复等过程。以洪水监测为例，实际分析不仅要判断是否发生变化，还要识别洪水何时开始、影响哪些区域、如何发展以及当前处于何种恢复阶段；可靠结论还必须能追溯到相应帧和空间区域，并避免把季节变化或采集条件差异误判为真实地理演化。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单时相与双时相遥感视觉语言模型**：单时相模型把一幅遥感图像与语言连接起来，用于图像描述、视觉问答或目标定位；双时相模型比较同一区域两个时间点的图像，以描述并定位两端之间发生的地理变化。
- **多时相或序列型遥感视觉语言模型**：这类模型一次接收多个时间点的观测，执行序列级对话或变化理解；相比图像对，它能利用更多时间信息，但现有工作主要强调对象识别、变化描述或一般性问答。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单幅图像没有演化轨迹，而图像对主要暴露变化的起点和终点，因此无法可靠恢复“发生、发展、结束或恢复”等中间阶段；其后果是模型可能答对总体变化，却无法说明关键转折出现在哪一帧。
- 现有序列模型通常没有把跨帧证据组织、变化区域定位、时间异常辨别和后续状态推断作为统一训练目标，因而难以同时追踪关键转折、将结论落到具体帧与区域，并区分真实地理变化和季节性或采集因素造成的干扰。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一个面向扩展地球观测序列的统一问题定义、系统化任务体系和大规模评测基准，也缺少能够把最终答案与关键帧、时间顺序及变化区域显式对齐的训练方案。因此，模型是否真正理解了完整的多阶段地理过程，而非依赖端点差异或表面模式，仍无法被充分训练和检验。

</div>
<div markdown="1"><span>核心问题</span>

如何让遥感视觉语言模型在较长的多时相图像序列上，联合完成多阶段演化概括、空间变化定位、时间异常识别以及缺失或未来状态预测，并使其推理过程能够由相关帧和变化区域提供可核查的证据？

</div>
<div markdown="1"><span>作者直觉</span>

显式序列标识符相当于给每幅图像设置稳定的时间坐标，使模型不易混淆先后次序；结构化推理标注再示范如何从全部观测中筛选关键帧、比较变化并定位区域。随后，时间和空间奖励直接评价这些中间步骤是否一致，而不只检查最后一句答案。分析上，这种设计有望减少“答案偶然正确但依据错误”的情况，并迫使模型按地理过程的实际顺序整合证据；这是对作者设计逻辑的解释，而非原文单独验证的因果结论。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法以 Qwen2.5-VL-7B 为基础，采用“监督式序列扎根，再用强化学习校准”的两阶段训练框架。输入是按时间排序的遥感图像序列 $X=\{I_1,\ldots,I_T\}$ 与问题 $q$。第一阶段先为每一帧附加显式序列标识符，如 Image 1 到 Image $T$，再将问题、标识符和视觉编码器产生的帧级视觉 token 按时间顺序拼接；模型同时从答案级样本和含结构化推理轨迹的 30k 子集学习，得到 LongEarth。第二阶段从 LongEarth 初始化，对同一输入采样一组包含推理与答案的候选响应，依据格式正确性、时间扎根和空间一致性计算相对奖励，并通过组相对策略优化（GRPO）得到 LongEarth-R1。

技术上，显式序列标识符解决“模型提到的是哪一帧”这一索引问题，结构化思维链监督解决“应先检查哪些帧和区域、再怎样综合证据”的过程学习问题，GRPO 则直接惩罚参考帧次序错误和空间描述不一致。直观地说，第一阶段先教模型给一叠按日期排列的遥感图像编号，并示范如何做观察笔记；第二阶段不再要求它逐字模仿唯一范文，而是比较同题的多个答案，奖励格式规范、时间顺序正确且地点和变化方向对得上的回答。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 时序多模态输入构造

冻结视觉编码器 $f_v$，将每帧编码为 $V_t=f_v(I_t)$，并按 $H=[q;\mathrm{Image}\ 1,V_1;\ldots;\mathrm{Image}\ T,V_T]$ 组织输入。Image $t$ 作为显式序列标识符，使视觉内容与帧序号形成稳定绑定。

<div class="method-step__io" markdown="1">

**输入**：时间有序的遥感序列 $X=\{I_1,\ldots,I_T\}$ 和问题 $q$，其中 $I_t$ 是第 $t$ 次观测，$T$ 是序列长度。<br>
**输出**：包含问题、时间顺序、帧标识和帧级视觉 token 的多模态上下文 $H$。

</div>

**直观理解**：模型看到的不只是一串图片，还会看到每张图的明确编号。这样它在回答“第几阶段”“哪一帧异常”或“哪两帧之间发生变化”时，有可引用的时间坐标。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 序列感知答案监督

在冻结视觉编码器的条件下，通过应用于语言模型层的低秩适配模块（LoRA）进行参数高效监督微调，使模型学习从完整长序列和问题生成答案。该部分主要约束最终答案，不单独规定模型必须如何挑选关键帧或组织中间推理。

<div class="method-step__io" markdown="1">

**输入**：多模态上下文 $H$ 与对应参考答案 $a$。<br>
**输出**：具备长序列遥感问答能力和基本帧级时间锚定能力的模型参数。

</div>

**直观理解**：这一步先让模型学会“看完整段序列后答对题”。LoRA 只训练少量附加参数，减少训练成本，但单靠答案监督仍不能保证模型的推理过程真正对应正确帧和区域。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结构化思维链监督

将目标响应统一为 `<think>`$r$`</think><answer>`$a$`</answer>`，并以自回归负对数似然联合学习推理和答案。轨迹依次覆盖视觉扫描、特征识别和综合分析：先概括跨帧地表状态，再找出关键帧、变化区域、方向或异常，最后整合时空证据。

<div class="method-step__io" markdown="1">

**输入**：结构化样本 $(X,q,r,a)$，其中 $r$ 是推理轨迹，$a$ 是最终答案。<br>
**输出**：完成监督阶段的 LongEarth，其响应能够显式给出结构化推理轨迹和最终答案。

</div>

**直观理解**：这相当于不仅提供标准答案，还提供一份三步解题示范。模型因此学习先浏览全局，再圈出与问题有关的帧和区域，最后下结论。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选响应生成与时空奖励评估

旧策略 $\pi_{\theta_{\mathrm{old}}}$ 为同一输入采样 $G$ 个候选 $y_i=(r_i,a_i)$；每个候选按格式奖励 $R_i^{\mathrm{fmt}}$、时间奖励 $R_i^{\mathrm{time}}$ 和空间奖励 $R_i^{\mathrm{space}}$ 的加权和评分。若任务没有时间或空间标签，则省略不适用项，并重新归一化其余权重。

<div class="method-step__io" markdown="1">

**输入**：LongEarth、同一多模态输入 $H$，以及可用的格式、时间和空间监督标签。<br>
**输出**：每个候选响应的总奖励 $R_i$，以及由组内奖励均值和标准差归一化得到的相对优势 $A_i$。

</div>

**直观理解**：模型针对同一道题写出多份答案，再在组内比较优劣。评分既检查标签和答案格式，也检查引用帧是否按时间成立、变化位置和方向是否与证据一致。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 结构化思维链监督目标

$$
\mathcal{L}_{\mathrm{CoT}}=-\sum_{n=1}^{N}\log p_{\theta}(y_{n}\mid y_{<n},H)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{CoT}}$：结构化思维链监督的负对数似然损失。
- $y=(y_1,\ldots,y_N)$：由结构化推理轨迹和最终答案共同组成的目标 token 序列。
- $N$：目标响应的 token 总数。
- $y_n$：目标序列中的第 n 个 token。
- $y_{<n}$：生成第 n 个 token 前的所有目标 token。
- $H$：由问题、显式帧标识和按时间排序的视觉 token 构成的多模态输入。
- $p_{\theta}$：参数为 θ 的视觉语言模型给出的条件生成概率。
- $\theta$：监督训练中被优化的模型参数，文中主要通过语言模型层的 LoRA 模块调整。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标逐 token 提高参考响应的生成概率，因此 `<think>` 中的观察与证据整合过程和 `<answer>` 中的结论会被联合学习。它能教会模型模仿完整解题过程，却没有单独的项直接判定某个帧引用是否错位或空间方向是否矛盾。<br>
**原文位置**：Method，Supervised Sequence Grounding and Reasoning，Structured CoT Supervision，公式 (2)

</div>

</div>

<div class="equation-block" markdown="1">

#### GRPO 裁剪策略目标

$$
\mathcal{J}_{\mathrm{GRPO}}=\frac{1}{G}\sum_{i=1}^{G}\min\!\left(\rho_i A_i,\bar{\rho}_i A_i\right)-\beta D_{\mathrm{KL}}\!\left(\pi_{\theta}\|\pi_{\mathrm{ref}}\right),\quad A_i=\frac{R_i-\mu_R}{\sigma_R+\epsilon},\quad \rho_i=\frac{\pi_{\theta}(y_i\mid H)}{\pi_{\theta_{\mathrm{old}}}(y_i\mid H)},\quad \bar{\rho}_i=\operatorname{clip}(\rho_i,1-\varepsilon,1+\varepsilon)
$$

**符号说明**

- $\mathcal{J}_{\mathrm{GRPO}}$：需要最大化的组相对策略优化目标。
- $G$：针对同一输入采样的候选响应数量。
- $y_i=(r_i,a_i)$：第 i 个候选响应，由推理轨迹 $r_i$ 和最终答案 $a_i$ 组成。
- $R_i$：第 i 个候选的加权总奖励，由格式、时间和空间奖励构成。
- $\mu_R$：同一候选组内奖励的均值。
- $\sigma_R$：同一候选组内奖励的标准差。
- $A_i$：第 i 个候选相对于同组其他候选的标准化优势。
- $\pi_{\theta}$：正在优化的当前策略。
- $\pi_{\theta_{\mathrm{old}}}$：采样候选时使用的旧策略。
- $\rho_i$：当前策略与旧策略生成候选 $y_i$ 的概率比。
- $\bar{\rho}_i$：被限制在区间 [1-ε,1+ε] 内的策略概率比。
- $\varepsilon$：策略比率的裁剪系数，用于限制单次更新幅度。
- $\epsilon$：优势标准化分母中的微小常数，用于避免数值不稳定。
- $\pi_{\mathrm{ref}}$：监督训练结束后得到的参考策略，即 LongEarth。
- $D_{\mathrm{KL}}$：当前策略与参考策略之间的 Kullback–Leibler 散度。
- $\beta$：KL 正则项的权重。

<div class="equation-explanation" markdown="1">

**直观理解**：组内奖励高于平均水平的候选具有正优势，其生成概率会被提高；低于平均水平的候选则被压低。裁剪项限制策略概率一次改变过多，KL 项让模型不要远离监督训练所得的 LongEarth，从而在加强时空一致性的同时尽量保留原有视觉语言能力。<br>
**原文位置**：Method，Spatiotemporal Alignment via GRPO，公式 (4)；优势、策略比率与裁剪定义位于公式 (4) 前

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：第一阶段最小化监督生成损失：答案级样本主要约束最终答案，结构化样本则通过 $\mathcal{L}_{\mathrm{CoT}}$ 联合约束推理轨迹与答案。两类监督共同使模型适应长时序遥感输入，并形成基于显式帧标识的序列引用能力；其中结构化监督进一步教授视觉扫描、关键特征提取和证据综合，但它仍依赖单一参考输出，不能直接针对时间错序或空间冲突施加惩罚。

第二阶段最大化 $\mathcal{J}_{\mathrm{GRPO}}$。候选总奖励由格式、时间和空间三部分加权构成，随后在同一输入的 $G$ 个候选内标准化为相对优势；策略梯度提高高优势候选的概率，裁剪机制控制更新幅度，KL 正则则约束当前策略不要过度偏离监督阶段的 $\pi_{\mathrm{ref}}$。因此，两阶段目标的分工是：SFT 建立可生成的长序列推理范式，GRPO 再把优化重点从逐字模仿参考轨迹转向可验证的结构、时间顺序和空间一致性。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 显式序列标识与有序多模态表示**

视觉编码器分别计算 $V_t=f_v(I_t)$，随后将 $q$、Image $t$ 和 $V_t$ 按观测顺序组成 $H$。该设计不改变基础视觉编码器，而是在语言模型可读取的上下文中显式加入帧级索引，从而支持关键帧引用、时间区间定位和跨帧关系建模。

> 直观理解：长序列中外观相近的帧很多，仅依靠隐含位置容易把“第 8 帧”与“第 18 帧”混淆。给每帧贴上编号，相当于为模型提供可复述、可核对的时间坐标。

**2. 结构化推理监督**

推理轨迹 $r$ 被组织为视觉扫描、特征识别和综合分析三个语义步骤，并与答案 $a$ 一同放入规定标签中进行 token 级监督。它把监督范围从答案结果扩展到关键观测选择、变化区域识别和跨帧证据整合，但本质上仍是对单一参考轨迹的最大似然模仿。

> 直观理解：答案监督只能告诉模型结论是否相同，无法说明它是否看对了帧。结构化轨迹提供可学习的检查顺序，不过逐字模仿范文仍不能直接保证时间顺序和空间关系都正确，这正是第二阶段需要补足的部分。

**3. 时空奖励驱动的 GRPO**

对每个候选响应计算 $R_i=\lambda_fR_i^{\mathrm{fmt}}+\lambda_tR_i^{\mathrm{time}}+\lambda_sR_i^{\mathrm{space}}$。格式项检查 `<think>`/`<answer>` 结构和任务答案是否可解析；时间项联合检查所引用帧及其先后关系；空间项检查变化位置、方向和范围。GRPO 使用组内标准化优势进行相对更新，因此不要求额外训练一个价值模型。

> 直观理解：这一模块把“推理写得像示范”改成“推理是否满足可检查规则”。同题候选相互比较，可使模型偏向时间和空间证据更可靠的回答；但其效果仍取决于奖励规则与标签能否覆盖真实推理质量。

**训练与推理**

训练时，先将每个图像序列按时间排序，为第 $t$ 帧加入 Image $t$ 标识，并用冻结的视觉编码器产生 $V_t$；问题和全部帧表示共同组成 $H$。随后在 Qwen2.5-VL-7B 的语言模型层加入 LoRA：答案级样本训练从 $H$ 到 $a$ 的基本映射，30k 结构化子集训练从 $H$ 到 `<think>`$r$`</think><answer>`$a$`</answer>` 的完整映射，由此得到 LongEarth。原文将两者描述为监督阶段的两个互补组成部分，但所给章节未明确报告它们在批次或训练日程中的具体混合比例。

强化学习阶段以 LongEarth 初始化当前与参考策略。对每个 $H$，旧策略采样 $G$ 个候选，奖励器分别检查输出结构、帧引用及时间先后关系、变化位置及方向和范围，再计算组内相对优势并更新策略；不适用于某任务的时间或空间奖励被移除，其余权重重新归一化。推理阶段沿用相同的序列编号与输入组织方式，LongEarth-R1 根据完整序列和问题自回归输出推理轨迹及答案；无需结构化参考轨迹、奖励标签或 GRPO 更新。

**复现信息**

基础模型为 Qwen2.5-VL-7B。监督训练冻结视觉编码器，并仅通过语言模型层中的 LoRA 模块进行参数高效适配；这一点对复现和公平解释很重要，因为性能提升不是通过全面更新视觉骨干获得。结构化监督使用 LongEarth-Bench 中跨 12 项任务平衡构建的 30k 样本子集，其目标输出必须包含 `<think>` 与 `<answer>` 标签，推理语义顺序为视觉扫描、特征识别和综合分析。

GRPO 的奖励由格式、时间和空间项组成：格式项检查推理—答案结构和任务特定答案的可解析性，时间项检查引用帧匹配及时间顺序，空间项检查变化地点、方向和范围。所给正文说明详细奖励定义位于补充材料，但当前摘录没有提供 $G$、$\lambda_f$、$\lambda_t$、$\lambda_s$、$\varepsilon$、$\beta$、LoRA 秩、学习率、批大小、采样温度或训练轮数，因此这些值均不能从当前材料可靠复现，原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LongEarth-Bench是核心评测集，包含约12万条问答样本和11.7万张唯一图像；序列平均含15.14帧、最长30帧，覆盖演化总结（EvoSum）、空间推理（Spatial）、异常识别（AnomID）和逻辑预测（LogPred）四个维度、共12项任务。其中约3万条样本带有连接关键帧、变化区域与答案的结构化推理轨迹。原文摘录未给出具体训练、验证和测试划分规模。
- 标准单图与双时相遥感基准用于检查长时序专门化是否损害通用能力：AID和UCM测试单图场景识别；ABCD-CD、CDVQA-QA、xBD和S2Looking测试双时相变化理解。作者按照各数据集的标准协议，在对应训练集上微调LongEarth-R1，再使用任务原生协议评测；摘录未报告各数据集规模及具体划分数量。
- Qfabric与fMoW用于短序列多图迁移评测，其中fMoW分为低分辨率时序分类（fMoW-LR-TSC）和高分辨率时序分类（fMoW-HR-TSC）；该组输入不超过8张图像，用来判断模型在较短序列上的能力是否因长时序训练而退化。原文摘录未报告样本规模及具体划分数量。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

用于封闭答案，包括类别判断、单帧定位、固定空间标签和离散范围等级；计算预测答案与参考答案完全正确的比例。 （越高越好，因为更高数值表示更多封闭式问题得到正确答案。）

</div>
<div class="metric-item" markdown="1">

**Temporal F1**

将预测文本解析为帧索引集合，再计算预测集合与参考集合之间的$F1$；用于T1、T3、T8，以及T7、T9、T12的时间集合变体，同时兼顾关键帧查全率与查准率。 （越高越好，因为模型既需要覆盖相关帧，也要避免选择无关帧。）

</div>
<div class="metric-item" markdown="1">

**Spatial F1**

对自由形式空间答案抽取集合$\mathcal{S}=\{\text{object},\text{change},\text{region},\text{direction},\text{extent}\}$中的对象、变化、区域、方向和范围元素，再计算集合$F1$；用于T4至T6和T11。 （越高越好，因为高分要求空间描述包含更多正确要素且减少错误要素。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### LongEarth-Bench全部12项长时序任务

<div class="result-value" markdown="1">

作者报告LongEarth-R1在EvoSum、Spatial、AnomID和LogPred所涵盖的12项任务上均排名第一，并称异常识别及依赖长距离时间证据的任务增益尤其明显。

</div>

这说明完整方法在该基准内部具有广泛而非单一任务上的优势，支持序列定位、结构化推理和奖励对齐能够共同改善长时序推理这一作者结论。但摘录未提供Table 1的逐任务分数与显著性检验，因此无法核验每项领先幅度，也不能据此断言模型已解决跨数据源或真实业务环境中的长时序推理。

<div class="result-source" markdown="1">

来源：Experimental Results, Performance on LongEarth-Bench；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 1 shows that LongEarth-R1 ranks first on all tasks, with particularly strong gains on AnomID and tasks requiring long-range temporal evidence.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 标准单图、双时相和不超过8帧的短序列遥感任务

<div class="result-value" markdown="1">

LongEarth-R1在9个数据集中的6个取得最高结果，并包揽4个双时相变化理解基准：ABCD-CD为91.20、CDVQA-QA为56.60、xBD平均为71.50、S2Looking平均为60.50。单图AID上其86.03低于EarthDial的88.67；短序列Qfabric上其69.70低于TEOChat的70.80，fMoW-HR-TSC上其72.90低于TEOChat的75.10。

</div>

这组实验主要检验长时序训练是否牺牲常规遥感能力。四个双时相任务全部领先，表明长时间演化监督可迁移到变化分析；其余任务与最强专用模型接近，但并非全部最优。由于LongEarth-R1针对每个基准都在相应训练集上微调，这些数字不能解释为零样本泛化，也不能单独排除训练预算或基座模型差异的影响。

<div class="result-source" markdown="1">

来源：Experimental Results, Performance on Standard Remote Sensing Tasks；Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table 2 shows that LongEarth-R1 achieves the best result on six of nine datasets, including all bi-temporal change-understanding benchmarks, indicating effective transfer from long-horizon supervision to conventional change analysis.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 按输入帧数分组的时间鲁棒性分析

<div class="result-value" markdown="1">

所有方法均随输入序列变长而退化，但LongEarth-R1在每个输入长度区间领先10.7至31.9个百分点；其得分从2至5帧时的87.8降至26至30帧时的51.4。按答案所需证据跨度分组时，它在7个区间中的6个最优，仅在23至30帧证据跨度上落后于TEOChat*。

</div>

输入越长，模型越需要抑制无关观测并找到关键帧；持续领先说明显式序列定位与奖励优化提高了抗长上下文干扰能力。然而从87.8降至51.4也表明超长输入仍是明显瓶颈。证据跨度较大并不必然更难：若多帧提供互补线索，跨帧推理反而可能受益；但该分组分析是相关性证据，不能证明跨度扩大本身导致性能提高。

<div class="result-source" markdown="1">

来源：Experimental Results, Temporal Robustness Analysis；Figure 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

LongEarth-R1 nevertheless leads every input-length interval by 10.7–31.9%, retaining 51.4 at 26–30 frames after reaching 87.8 on 2–5-frame inputs.

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

- Video-LLaVA：通用视频视觉语言模型，用于比较一般视频建模能力能否直接迁移到遥感时序推理。
- GeoChat：面向遥感图像对话的视觉语言模型，是检验领域适配能力的代表性对照，但其核心能力并非长时序演化推理。
- EarthDial：遥感视觉语言模型，在定性案例和标准遥感任务中均参与比较，可用于判断现有遥感对话模型在关键时间区间定位上的局限。
- TEOChat：面向时间地球观测的模型，是最直接的时序遥感基线；带星号的TEOChat*表示经过LongEarth-Bench微调，因此在时间跨度分析中还能区分数据适配与LongEarth-R1训练设计的作用。

**实验想回答的问题**

- LongEarth-R1能否在LongEarth-Bench的12项长时序地球观测任务中，比现有视觉语言模型更准确地定位关键帧与变化区域，并完成演化总结、空间推理、异常识别和逻辑预测？
- 面向长时序推理的监督微调、显式序列标识、结构化思维链、GRPO及其三类奖励，是否真正改善了长上下文鲁棒性，同时保留单图、双时相和短序列遥感任务上的通用能力？

**实验实现**

训练分为SFT和GRPO两阶段，均使用8张NVIDIA A800 GPU；视觉编码器冻结，只调整语言侧LoRA模块，秩为$r=128$、缩放参数为$\alpha=256$。SFT训练2轮，使用bfloat16、梯度检查点、余弦学习率衰减，峰值学习率为$2\times10^{-5}$、预热比例为$0.03$且不使用权重衰减；输入上限为8192个token，将方形缩放图像、时间前缀和指令交错组织。GRPO从SFT检查点开始，对同一组LoRA参数使用成组采样回答及格式、时间、空间奖励进行优化。标准遥感基准并非直接零样本测试：LongEarth-R1会在各基准对应训练划分上再次微调，然后按任务原生协议评测，因此结果衡量的是迁移后的适应能力。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 累积加入SFT、序列标识、结构化CoT和GRPO | 完整配置在EvoSum、Spatial、AnomID和LogPred上分别达到74.67、65.55、76.73和76.85。与加入SFT、Seq.IDs和CoT但尚未使用GRPO的配置相比，四项分别提高5.20、6.47、12.61和6.04个百分点，其中AnomID增益最大。 | 该对照保持SFT、显式序列编号和结构化推理监督不变，只增加GRPO，因此较直接地隔离了奖励驱动策略优化的贡献。异常识别提高12.61个百分点，支持GRPO强化异常敏感证据选择的作者解释；不过累积消融没有展示多次随机运行方差，无法判断增益稳定性。另一个值得注意的现象是，单独加入CoT后四项分数均下降，说明结构化推理监督本身并不保证收益，需与后续奖励对齐配合。 | Table 3，Component Ablation完整配置行<br><span class="experiment-evidence">✓ ✓ ✓ ✓ 74.67 65.55 76.73 76.85</span> |
| 分别移除格式、时间或空间奖励 | 完整三奖励配置的四维平均分约为73.45；移除格式、时间、空间奖励后，平均分分别约为68.26、66.77和66.96，对应下降约5.19、6.68和6.49个百分点。移除格式奖励时LogPred由76.85略升至77.33，但整体平均仍下降。 | 逐项移除实验检验每种奖励是否提供不可替代的信息：格式奖励约束输出结构，时间奖励约束关键帧或区间，空间奖励约束对象、变化与区域定位。任意一项被移除都会降低总体平均，说明三者具有互补性；局部指标偶有上升则表明奖励之间可能存在任务权衡，完整目标追求的是四个认知维度的均衡表现，而非保证每一维都由每个奖励单调改善。 | Experimental Results, Ablation Analysis of Core Components；Table 3下半部分<br><span class="experiment-evidence">Removing any reward lowers the macro-average by 5.19–6.68%; although removing the format reward slightly improves LogPred, the full objective remains best overall, confirming the complementarity of the three rewards.</span> |

**定性案例**

- Figure 5比较了一个低水位时段判断案例：EarthDial和TEOChat给出错误时间区间，LongEarth-R1则依据多帧视觉证据定位到正确低水位时期。该案例直观展示了模型如何避免时间错位，并与时间鲁棒性定量结果一致；但单个成功案例不能估计整体错误率，也不能证明其推理文本忠实反映内部决策过程。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It centrally contributes a long-horizon visual reasoning benchmark and a VLM post-training method using chain-of-thought supervision and reward-based policy optimization.; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`4f9afee6dd1ca07ad58e2350495b00da3007757ec06335c843dbfd941e8ff1eb`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
