---
title: "[论文解读] InspectorGPT: A Comparative Reasoning Enhanced VLM for Comprehensive Industrial Anomaly Detection"
description: "[arXiv 2608.29783][VLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.29783"
announcement_date: "2026-09-01"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:28:52.904488+00:00"
source_sha256: "52b1b5f6481a616cfaab8cc4b56faca422d2f4e11e84ac0b2baca41a683f5653"
tags:
  - "VLM Reasoning"
  - "多模态 VLM"
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "工业异常检测"
  - "视觉语言模型"
  - "比较推理"
  - "正常参考图像"
  - "跨类别泛化"
  - "像素级异常分割"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.29783</p>

# InspectorGPT: A Comparative Reasoning Enhanced VLM for Comprehensive Industrial Anomaly Detection

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Weifei Chen, Honghao Zhang, Zhiyuan You, Xinyi Le</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Shanghai Jiao Tong University；The Chinese University of Hong Kong</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29783v1) · [PDF 下载](https://arxiv.org/pdf/2608.29783v1) · **关键词** 工业异常检测, 视觉语言模型, 比较推理, 正常参考图像, 跨类别泛化, 像素级异常分割<br>


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

工业异常检测（IAD）服务于制造业质量控制，目标是识别图像中偏离正常外观的产品，并定位缺陷区域。传统纯视觉方法通常仅用无缺陷样本学习特定产品类别的“正常性”：嵌入式方法比较测试特征与正常特征库之间的距离，重建式方法则以图像重建误差作为异常信号；这类方法在产品类别变化后往往需要重新收集正常样本或微调，而且通常只能给出异常分数或二元判断。视觉语言模型（VLM）可结合图像与文本指令进行零样本检测并生成解释，但现有方法依赖类别定义、文本提示或数据集特有的回答模式，推理导向的后训练甚至可能削弱最基本的异常判别能力；同时，其定位结果多为文字描述或粗粒度边界框，难以满足像素级缺陷勾画与定量评估。本文据此把工业检测设定为参考条件下的比较问题：以一张无缺陷参考图像作为可观察的正常模板，将查询图像中的差异作为判别、解释和定位异常的共同依据。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉语言模型（VLM）与多模态大语言模型（MLLM）**

VLM联合处理视觉与语言信息；其中具备指令理解和文本生成能力的大规模模型常称为MLLM。用于工业检测时，它们不仅可以判断是否异常，还能用自然语言描述异常类型、位置及判断理由。

</div>
<div class="concept-item" markdown="1">

**正常性建模与零样本异常检测**

正常性建模先从无缺陷样本中学习某一产品的正常特征或重建规律，再把明显偏离该规律的区域视为异常。零样本检测则希望不针对目标产品重新训练，直接依靠预训练模型、文本提示或给定参考图像处理未见类别。

</div>
<div class="concept-item" markdown="1">

**比较推理与思维链（CoT）**

比较推理是把无缺陷参考图像与待检查询图像逐区域对照，使异常判断落在具体、可观察的视觉差异上。CoT是在最终答案前生成结构化的中间推理过程，本文用它覆盖多个检查维度并为判别、分类和定位提供可解释依据。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括一张无缺陷的正常参考图像和一张待检查的查询图像；模型以参考图像作为当前产品的正常模板，对两幅图像进行语义级和区域级比较，而不是仅依赖训练阶段固化的类别正常原型。输出覆盖多个工业检查任务：判断查询图像是否异常，描述可观察差异并给出结构化推理，识别或分类缺陷，定位异常区域，并在需要时产生像素级异常掩码。其核心应用设定是跨类别与跨基准泛化，即面对训练中未见的产品类别或数据集时，不进行目标域适配或重新训练，而由测试时提供的正常参考图像界定“正常”；文中同时默认参考图像确为无缺陷样本。需要区分的是，二元异常分数只回答“是否异常”，边界框提供粗略范围，而像素掩码需要逐像素标明缺陷，因此能支持更精细的面积、形状与位置评估。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Roth et al. (2022), Towards Total Recall in Industrial Anomaly Detection**: 代表传统嵌入式工业异常检测范式：将测试图像特征与存储的正常表示进行比较，并从特征距离推导异常分数。它说明了正常特征库方法的基本机制，也构成本文所批评的类别特定正常性建模路线：更换产品类别后，新类别缺少可直接使用的正常原型。
- **Kang et al. (2026)**: 本文将其作为推理导向异常检测后训练存在风险的直接相关证据：经过异常数据与推理目标后训练的模型，其异常判别表现可能低于自身基础VLM。InspectorGPT试图用参考图像驱动的比较原则取代对数据集回答模式的模仿，并进一步补足现有方法缺少像素级分割的问题；所给节选未提供该工作的完整题名与具体数值。

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

InspectorGPT以正常参考图像、待检查询图像和检查提示为输入，先通过比较式思维链监督微调建立“对齐—对比—诊断”的推理格式，再用带有格式、定位和答案可验证性奖励的$\mathrm{GRPO}$优化检查输出。与此同时，模型从同一监督微调检查点训练像素级分割分支，最后以任务向量融合推理分支与分割分支的共享视觉语言模型参数，并保留分割解码器，从而同时输出结构化诊断、粗粒度框和像素级异常掩码。直观地说，系统先学习像人一样拿“无缺陷样品”与“待检样品”逐项比较，再分别强化语言判断和精确画出缺陷区域，最后将两种能力合并。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 比较式CoT监督微调

利用Qwen3-Plus生成并经人工核验的三阶段“Align-Contrast-Diagnose”思维链，对Qwen2.5-VL进行全参数监督微调，使模型学习比较两幅图像、描述差异、判断异常并按结构化标签输出。

<div class="method-step__io" markdown="1">

**输入**：训练样本包括缺陷无关的正常参考图像$I_r$、查询图像$I_q$、真实异常掩码$I_m$和检查提示；其中$I_m$仅用于构造空间提示，不作为模型推理时的输入。<br>
**输出**：得到监督微调策略$\pi_{\mathrm{ref}}$及共享初始化权重$\theta_0=\theta_{\mathrm{SFT}}$，前者作为后续强化学习的冻结参考策略，后者初始化推理和分割两个分支。

</div>

**直观理解**：这一步先规定一种稳定的检查流程：先把两张图对齐，再找不同，最后说明差异是否构成缺陷。真实掩码像教师给出的“看哪里”提示，但模型最终必须学会用图像比较自行完成判断。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 带可验证奖励的GRPO推理优化

对每个回答解析出预测框集合$B_{\mathrm{pred}}$和诊断答案$A_{\mathrm{pred}}$，分别计算XML格式奖励、条件$\mathrm{IoU}$定位奖励以及带空间门控的答案奖励，再按组归一化优势更新策略，并用KL约束防止其偏离$\pi_{\mathrm{ref}}$过远。

<div class="method-step__io" markdown="1">

**输入**：输入为参考图像$I_r$、查询图像$I_q$和检查提示$x$；当前策略对每个$x$采样$G$个候选回答$\{y_i\}_{i=1}^{G}$。<br>
**输出**：得到推理分支权重$\theta_G$，即InspectorGPT-Reason；其输出包含可解析的思维链、答案和边界框。

</div>

**直观理解**：模型一次提出多种检查报告，系统不只看答案对不对，还检查格式是否完整、框是否覆盖缺陷，以及“说有缺陷”时是否真的给出了框。这样可以减少只生成听起来合理但没有图像证据的回答。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 像素级分割分支训练

从视觉语言模型骨干提取多尺度特征，经$3\times3$卷积空间上下文适配器处理后送入改造的Mask2Former解码器，预测全局异常概率$P_{\mathrm{cls}}$和密集掩码$P_{\mathrm{mask}}$；先冻结骨干训练解码器，再注入LoRA并以较小学习率联合优化LoRA参数和解码器。

<div class="method-step__io" markdown="1">

**输入**：分支从$\theta_0$并行初始化，输入参考图像和查询图像形成的视觉特征，以及像素级异常标注。<br>
**输出**：得到分割骨干权重$\theta_S$和分割解码器$\Phi_S$，构成InspectorGPT-Seg，并提供像素级异常掩码。

</div>

**直观理解**：边界框只能告诉系统“缺陷大概在这里”，分割分支则要逐像素涂出缺陷。LoRA打开了从像素损失回传到视觉语言骨干的通路，使分割学习到的细粒度证据能够改善异常辨别。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务向量融合与推理

分别计算两个分支相对于$\theta_0$的参数位移，按$(1-\alpha)$和$\alpha$线性组合，再加回初始化权重；只融合共享骨干参数，分割解码器$\Phi_S$单独保留。

<div class="method-step__io" markdown="1">

**输入**：输入为共同初始化$\theta_0$、推理分支权重$\theta_G$、分割分支权重$\theta_S$和融合系数$\alpha$；最终实验采用$\alpha=0.3$。<br>
**输出**：得到融合骨干$\theta^*$及其配套解码器$\Phi_S$，即最终InspectorGPT。推理时模型比较参考图和查询图，生成思维链、诊断答案和框，并由分割解码器输出像素级掩码。

</div>

**直观理解**：两个分支像两个专长不同的检查员：推理分支更会解释，分割分支更会找准位置。任务向量融合不是重新训练，而是把两者相对同一出发点学到的“能力增量”按比例相加。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### GRPO策略优化目标

$$
\mathcal{L}_{\mathrm{GRPO}}=-\frac{1}{G}\sum_{i=1}^{G}\left[A_i\log\pi_{\theta}(y_i\mid x)-\beta\,\mathbb{D}_{\mathrm{KL}}(\pi_{\theta}\,\|\,\pi_{\mathrm{ref}})\right]
$$

**符号说明**

- $x$：输入检查任务，包括图像和提示
- $G$：每个输入采样的候选回答数量
- $y_i$：第$i$个候选回答
- $A_i$：由组内奖励归一化得到的第$i$个候选回答的优势
- $\pi_{\theta}$：当前待优化的视觉语言模型策略
- $\pi_{\mathrm{ref}}$：冻结的监督微调参考策略
- $\beta$：KL约束强度
- $\mathbb{D}_{\mathrm{KL}}$：当前策略与参考策略之间的KL散度

<div class="equation-explanation" markdown="1">

**直观理解**：目标鼓励模型提高高奖励候选回答的生成概率，同时限制模型不要偏离监督微调得到的稳定推理行为。$A_i$让同一输入下表现更好的回答获得更强更新，而不是依赖难以标定的绝对奖励。<br>
**原文位置**：Method，Stage 2，式(2)

</div>

</div>

<div class="equation-block" markdown="1">

#### 任务向量融合

$$
\tau_G=\theta_G-\theta_0,\qquad \tau_S=\theta_S-\theta_0,\qquad \tau^{*}=(1-\alpha)\tau_G+\alpha\tau_S,\qquad \theta^{*}=\theta_0+\tau^{*}
$$

**符号说明**

- $\theta_0$：共同的CoT监督微调初始化权重
- $\theta_G$：GRPO推理分支训练后的共享骨干权重
- $\theta_S$：分割分支训练后的共享骨干权重
- $\tau_G$：推理分支相对于共同初始化学到的参数位移
- $\tau_S$：分割分支相对于共同初始化学到的参数位移
- $\alpha$：分割任务向量的融合权重
- $\theta^{*}$：融合后的共享骨干权重

<div class="equation-explanation" markdown="1">

**直观理解**：公式先去掉两个分支共有的基础参数，只保留各自新增的能力，再按比例混合并恢复到原参数空间。这样可以用一个系数调节“解释推理”和“异常辨别”的平衡，且不需要再次训练融合模型。<br>
**原文位置**：Method，Stage 4，式(8)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练分为两个互补目标。第一阶段用标准自回归监督损失训练比较式思维链，但其主要作用是建立可解析的推理格式；第二阶段以$R_i=\lambda_{\mathrm{fmt}}R_{\mathrm{format}}+\lambda_{\mathrm{iou}}R_{\mathrm{iou}}+\lambda_{\mathrm{ans}}R_{\mathrm{answer}}$为标量奖励，通过GRPO直接优化格式、框定位和答案正确性，其中$\lambda_{\mathrm{fmt}}$、$\lambda_{\mathrm{iou}}$和$\lambda_{\mathrm{ans}}$为非负权重。分割分支最小化$\mathcal{L}_{\mathrm{total}}=\lambda_{\mathrm{cls}}\mathcal{L}_{\mathrm{cls}}+\mathcal{L}_{\mathrm{mask}}$，其中$\mathcal{L}_{\mathrm{mask}}$由BCE、Dice、总变分和一致性损失组成；该目标同时约束像素对齐、掩码连续性以及全局分类与局部掩码的一致。两个分支从同一$\theta_0$独立优化，最终不通过联合损失折中，而通过任务向量融合实现能力组合。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 比较式视觉语言推理**

模型同时接收正常参考图$I_r$和查询图$I_q$，被约束生成遵循“Align-Contrast-Diagnose”顺序的Chain-of-Thought，并以XML标签组织$\texttt{<think>}$、$\texttt{<bbox>}$和$\texttt{<answer>}$内容。

> 直观理解：该模块的核心不是单独记住某类产品的外观，而是寻找参考图与查询图之间的差异，因此理论上更容易迁移到未见类别。结构化标签还让后续程序能够可靠地读取框和答案。

**2. GRPO可验证奖励引擎**

奖励由$R_{\mathrm{format}}$、$R_{\mathrm{iou}}$和$R_{\mathrm{answer}}$加权组成。$R_{\mathrm{iou}}$对正常样本采用“真实框为空且预测框也为空”时得分为1的条件规则；答案奖励通过$\mathbb{I}_{\mathrm{gate}}$进行空间一致性门控，避免异常答案与框不匹配。

> 直观理解：系统把一份报告拆成格式、位置和结论三项检查，且不允许模型只靠猜答案得分。正常样本没有缺陷框，所以必须特别处理“空框对空框”的情况。

**3. 多尺度分割与任务向量融合**

分割分支使用卷积空间上下文适配器保留高频纹理，并以分类损失、BCE、Dice、总变分和分类—掩码一致性损失训练；随后将$\theta_G$和$\theta_S$相对$\theta_0$的任务向量融合，保留$\Phi_S$用于掩码解码。

> 直观理解：多尺度特征帮助模型既看整体布局又看细小纹理，连续性约束可减少破碎掩码。分支分开训练再融合，是为了避免一个模型同时优化解释能力和像素定位时互相牺牲。

**训练与推理**

训练时，先用正常参考图、查询图和掩码提示构造并核验比较式CoT数据，在Qwen2.5-VL上进行全参数SFT，得到$\pi_{\mathrm{ref}}$和$\theta_0$。随后从$\theta_0$分出GRPO分支和分割分支：前者采样多条结构化回答，解析框与答案并计算三类奖励；后者先冻结视觉语言模型训练分割解码器，再通过Seg-LoRA联合优化骨干适配器和解码器。最后计算两个分支的任务向量，以$\alpha=0.3$融合共享骨干，并保留分割解码器。推理时输入一张缺陷无关的参考图、一张查询图和检查提示；融合模型输出比较式思维链、异常答案和边界框，分割解码器根据多尺度视觉特征输出异常概率与像素级掩码。

**复现信息**

为保证输出可验证，回答使用严格的XML标签解析规则，并将预测结果拆分为$B_{\mathrm{pred}}$和$A_{\mathrm{pred}}$。分割模块采用$3\times3$卷积空间上下文适配器和改造的Mask2Former解码器；LoRA插入注意力与MLP投影层，训练后合并LoRA更新。仅共享骨干参与任务向量融合，$\Phi_S$不融合而单独保留。除最终融合系数$\alpha=0.3$外，奖励权重、采样组大小$G$、KL系数$\beta$及各分割损失权重的具体数值在所供原文节选中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MMAD是主要训练与测试基准，汇集MVTec-AD、VisA、MVTec-LOCO和GoodsAD，共覆盖38个类别。作者按类别分层抽取20%用于训练，并保持正常与异常样本比例为1:1；其余80%用于测试。它承担七维工业视觉问答评测，包括异常判别、缺陷分类、缺陷定位、缺陷描述、缺陷分析、对象分类和对象分析。
- DAGM与DTD-Synthetic被作为域外泛化基准；二者均不属于MMAD，训练完成的同一模型直接测试，不再针对目标基准训练。前者代表工业光学检测场景，后者用于合成纹理异常场景。原文节选未给出其规模及量化结果。
- SDD与MPDD同样作为不与MMAD重叠的直接迁移基准，用于考察表面缺陷和金属零件等新场景上的泛化。原文节选未报告数据规模、具体评测指标或结果数值。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**A-Disc.**

异常判别准确率，衡量模型能否正确判断待检图像是正常还是异常。这是工业检测最基础的决策能力，但不反映模型能否解释缺陷类型、位置或原因。 （越高越好，因为更高的准确率表示正常与异常样本的分类更可靠。）

</div>
<div class="metric-item" markdown="1">

**Sem-6**

除异常判别外六项语义子任务的宏平均准确率，覆盖缺陷分类、定位、描述、分析以及对象分类、分析。宏平均使六个维度获得相同权重，用于概括语义理解能力；Table 1展示各子项，但未单列Sem-6数值。 （越高越好，因为表示模型在多种语义任务上的平均正确率更高，而非只在某一个任务占优。）

</div>
<div class="metric-item" markdown="1">

**Avg.**

全部七项任务的宏平均准确率，按$\mathrm{Avg.}=(\mathrm{A\text{-}Disc.}+6\,\mathrm{Sem\text{-}6})/7$计算，用于衡量异常判别与六项语义能力的整体平衡。 （越高越好，因为七个任务等权汇总后，更高数值代表更强的综合检查能力；但它可能掩盖单项能力差异，因此需与A-Disc.及各语义子项共同阅读。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### MMAD七维综合检查，与同设置下可排名的专用模型和通用模型比较

<div class="result-value" markdown="1">

InspectorGPT的七项宏平均准确率为82.38%，高于最强可排名专用基线AD-FM的82.03%；其异常判别为73.90%，缺陷分析为88.25%，分别体现基础检测与高层解释能力。

</div>

作者据此主张模型在七类任务之间取得了较好的综合平衡，而不只是改善缺陷描述。平均分领先AD-FM仅0.35个百分点，因此更稳妥的解读是“小幅综合领先”；节选未提供方差、置信区间或显著性检验，不能据此断定该差距具有统计显著性。此外，AD-Copilot的平均分为82.29%，但因训练数据设置不同被作者排除出排名。

<div class="result-source" markdown="1">

来源：Main Results，Table 1及“Multi-dimensional Inspection on MMAD”段

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

InspectorGPT attains the best average accuracy (82.38%), ahead of the strongest specialist baseline AD-FM (82.03%) and of a 10× larger general-purpose VLM (Qwen2.5-VL-72B, 76.96%), while also leading on anomaly discrimination (73.90%) and defect analysis (88.25%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### MMAD比较式协议下，与约大十倍的Qwen2.5-VL-72B比较

<div class="result-value" markdown="1">

7B规模的InspectorGPT取得82.38%的综合平均准确率，而Qwen2.5-VL-72B为76.96%，前者高5.42个百分点。

</div>

该结果说明，在本实验协议中，围绕参考图比较进行专门训练，比单纯扩大通用VLM规模更有效，支持“任务设计与训练方式重要”的解释。不过两者并非只改变参数规模：InspectorGPT还接受了CoT监督微调、GRPO、分割训练和任务向量融合，因此实验不能把5.42个百分点全部归因于比较推理本身，也不是严格的规模控制实验。

<div class="result-source" markdown="1">

来源：Main Results，Table 1及“Multi-dimensional Inspection on MMAD”段

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

InspectorGPT attains the best average accuracy (82.38%), ahead of the strongest specialist baseline AD-FM (82.03%) and of a 10× larger general-purpose VLM (Qwen2.5-VL-72B, 76.96%), while also leading on anomaly discrimination (73.90%) and defect analysis (88.25%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 检验推理导向微调是否损害基础异常判别：OmniAD、JUDO与共同的Qwen2.5-VL-7B基础模型比较

<div class="result-value" markdown="1">

基础Qwen2.5-VL-7B的异常判别准确率为70.47%；OmniAD和JUDO分别降至68.80%和64.51%。与此同时，它们的缺陷描述准确率相对基础模型分别提高2.90和20.08个百分点。

</div>

这组对照直接展示了论文所称的能力权衡：模型可能更会描述缺陷，却更不善于完成最基本的正常/异常判断。它支持研究问题的存在，但尚不能证明所有推理后训练都会导致判别崩塌，因为这里只比较了若干具体模型，而且不同方法的训练目标和数据细节未必完全一致。

<div class="result-source" markdown="1">

来源：Main Results，Table 1及“Multi-dimensional Inspection on MMAD”段

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Reasoning-oriented specialists purchase semantic quality at the expense of the most elementary capability: OmniAD (68.80%) and JUDO (64.51%) both discriminate worse than the very base VLM they fine-tune (70.47%), despite leading it by 2.90 and 20.08 points, respectively, on defect description.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前节选声称会在DAGM、DTD-Synthetic、SDD和MPDD上直接评估泛化，但没有提供这些基准的量化结果。因此，能够由现有证据支持的结论仅限于MMAD的80%留出测试集，尚不能核验对未知基准的泛化优势。
- 节选没有给出消融表、重复运行方差、置信区间或统计显著性检验。因而无法从现有材料独立确认任务向量融合是否确实优于单独的推理/分割分支，也难以判断InspectorGPT相对AD-FM仅0.35个百分点的平均优势是否稳定。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen2.5-VL-7B是InspectorGPT所用的基础视觉语言模型，也是判断后训练究竟带来提升还是能力退化的关键对照；所有通用模型均接收待检图像和无缺陷参考图像，因而比较协议较为一致。
- Qwen2.5-VL-72B代表参数规模约大十倍的开源通用视觉语言模型，用于检验InspectorGPT的提升是否仅能通过扩大模型规模获得。
- AD-FM是MMAD表中平均准确率最高的可排名工业异常检测专用基线，因此是衡量综合七维能力的主要强基线。
- OmniAD与JUDO代表强调工业异常语义理解或推理的专用微调模型，用于检验论文所指出的核心问题：语义能力增强是否会伴随异常判别能力下降。另有AD-Copilot取得较高分数，但作者注明其训练数据设置不同并将其排除出排名，因此不宜作为严格同条件的主要胜负依据。

**实验想回答的问题**

- 在统一的“待检图像＋无缺陷参考图像”比较协议下，InspectorGPT能否同时做好异常判别、缺陷语义理解、定位与分析，而不是以牺牲基础异常判别能力来换取更强的描述和推理能力？
- 仅用MMAD的分层训练子集训练后，模型能否泛化到MMAD留出测试集以及与MMAD不重叠的工业异常基准？现有节选实际给出了MMAD主结果，但未提供四个外部基准的量化结果。

**实验实现**

所有模型按照比较式协议接收一张待检图像和一张无缺陷参考图像；MMAD参考图从其原有参考图集合中随机抽取。InspectorGPT以Qwen2.5-VL-7B初始化：第一阶段CoT监督微调训练3轮，使用AdamW及学习率$1\times10^{-5}$；第二阶段GRPO每个问题采样$G=8$个回答，IoU、答案和格式奖励权重分别为$0.4$、$0.4$和$0.2$，并采用动态长度惩罚。分割解码器输出$512\times512$掩码，以学习率$2\times10^{-4}$优化；VLM的注意力与MLP投影注入秩$r=16$、缩放参数$\alpha=32$、dropout为$0.05$的LoRA。最终模型以融合系数$\alpha=0.3$组合推理与分割分支的任务向量。实验使用4张NVIDIA A800 GPU和DeepSpeed ZeRO-3。主表报告MMAD七项VQA准确率；外部四基准虽被列入协议，但当前节选没有对应结果。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出通过比较推理和可验证后训练增强视觉语言模型工业异常检测与像素级分割能力。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`52b1b5f6481a616cfaab8cc4b56faca422d2f4e11e84ac0b2baca41a683f5653`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
