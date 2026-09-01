---
title: "[论文解读] SUP-MIMIC: A Multi-Task Clinical Diagnosis Benchmark for Evaluating LLMs' Robustness to Contradictory Evidence"
description: "[arXiv 2608.29582][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.29582"
announcement_date: "2026-09-01"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:35:02.897898+00:00"
source_sha256: "07836875f35f1ecbf2936927e6931a2b4d0fd5e6933d6ec256922db48d3c4aad"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型医学诊断"
  - "临床推理鲁棒性"
  - "诊断分歧"
  - "诊断收敛"
  - "对比式病例对"
  - "MIMIC-IV"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.29582</p>

# SUP-MIMIC: A Multi-Task Clinical Diagnosis Benchmark for Evaluating LLMs' Robustness to Contradictory Evidence

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Yi Yu, Bo Wang, Chong Feng, Ge Shi, Xia Liu, Ziyi Yang, Xuewen Shi</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Beijing University of Technology；Affiliation: Beijing Institute of Technology；Affiliation: Department of Rheumatology and Immunology, China-Japan Friendship Hospital；Affiliation: Dongbei University of Finance and Economics * Equal contribution；Affiliation: Department of Rheumatology and Immunology；China-Japan Friendship Hospital；Affiliation: Dongbei University of Finance and Economics</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29582v1) · [PDF 下载](https://arxiv.org/pdf/2608.29582v1) · **关键词** 大语言模型医学诊断, 临床推理鲁棒性, 诊断分歧, 诊断收敛, 对比式病例对, MIMIC-IV<br>


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

本文位于临床诊断基准与大语言模型医学推理评估的交叉领域。现有医学基准通常要求模型根据单个病例或医学问题输出疾病诊断，重点考察医学知识回忆、文本理解或表面统计模式；但真实临床诊断并不是症状到疾病的简单一一对应关系：相似的临床表现可能源于不同病因，不同的症状组合也可能指向同一疾病。因此，SUP-MIMIC关注模型能否在真实重症监护病房数据中处理这种非双射的“特征—诊断”映射，尤其检验模型面对相似病例中的关键差异，以及不同病例中的共同诊断依据时，是否仍能保持诊断可靠性。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**非双射的特征—诊断映射**

非双射表示临床指标与诊断之间不是一一对应：相似指标组合可能对应多种疾病，而同一疾病也可能以不同指标组合出现。模型不能只依赖整体表面相似度，还必须识别真正改变诊断的关键证据。

</div>
<div class="concept-item" markdown="1">

**诊断分歧与诊断收敛**

诊断分歧（DDT）指两个病例外观相似但真实诊断不同，要求模型发现少数具有决定性的差异。诊断收敛（DCT）指病例表现差异很大但诊断相同，要求模型忽略不改变诊断的表面异质性并识别共同模式。

</div>
<div class="concept-item" markdown="1">

**对比式、成对评估**

该评估不是独立判断每个病例，而是同时检查一对病例及其诊断关系是否被模型正确保留。这样可以暴露“单病例答对、病例关系答错”的情况，即模型可能依靠捷径而非稳定的临床推理。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

SUP-MIMIC以MIMIC-IV-v3.1重症监护病房记录为数据来源，输入是经过整理的单个患者临床特征，或由两个患者组成、并带有预设诊断关系的病例对；输出是患者诊断标签，或对病例对关系的判断。框架包含三个层次：Basic Assessment（BA）要求在200种常见疾病中完成单病例诊断；Diagnostic Divergence Task（DDT）要求在临床表现相似但诊断不同的病例对中分别识别疾病；Diagnostic Convergence Task（DCT）要求在临床表现异质但诊断相同的病例对中识别共同疾病。其核心假设是，真实临床证据包含可能相互冲突或具有误导性的指标，可靠模型应对诊断决定性差异敏感，并对不改变诊断的表现差异保持相对稳定。研究还使用成对鲁棒性指标检验模型是否保留病例对的诊断关系，而不只计算每个病例的独立准确率。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D_{\mathrm{task}}$**

任务数据集或任务层次；本文具体对应BA、DDT或DCT中的一个评估集合。

</div>
<div class="notation-item" markdown="1">

**$x$**

输入病例的临床特征，包括人口学信息、实验室指标、生命体征、合并症等经处理后的患者信息。

</div>
<div class="notation-item" markdown="1">

**$y$**

病例的真实诊断标签，即模型应预测的疾病类别。

</div>
<div class="notation-item" markdown="1">

**$(x_i,x_j)$**

由两个患者病例组成的对比样本；在DDT中二者相似但诊断不同，在DCT中二者表现异质但诊断相同。

</div>

</div>

**直接相关的工作**

- **MIMIC-IV-v3.1**: SUP-MIMIC以该重症监护病房电子健康记录数据库为基础构造病例及对比样本。相较于仅提供固定题目的医学问答基准，MIMIC数据支持从真实临床记录中挖掘自然出现的相似或异质病例对。
- **MedQA、PubMedQA、MMLU-Medical与LLMEval-Med**: 这些基准证明大语言模型能够完成医学知识问答或单病例诊断，但主要测量知识回忆、文本理解或孤立病例判断，较少系统检验相似表现对应不同病因、不同表现对应相同诊断时的成对一致性。因此，SUP-MIMIC将它们未充分覆盖的矛盾证据鲁棒性作为评估重点。

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

SUP-MIMIC 将临床诊断表述为多标签患者记录上的二元验证问题：给定患者的结构化临床指标 $\mathbf{X}_{p}$ 与候选诊断 $d_k$，模型判断该诊断是否属于患者的 ICD 诊断集合 $Y_p$。方法先从 MIMIC-IV-v3.1 的 ICU 记录中筛选并预处理早期临床数据，再为每个疾病学习诊断相关特征、构造疾病特异的患者相似度，最后从真实病例中挖掘 DDT 与 DCT 对比样本供 LLM 评估。直观地说，BA 检查模型能否判断单个病例是否患有某病；DDT 检查“看起来相似但诊断不同”的病例，DCT 检查“表现差异很大但诊断相同”的病例，从而避免模型只依赖表面统计线索。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 数据筛选与预处理

仅保留 ICU 入院后前 24 小时的临床测量，并将 ICU 期间的 ICD 诊断作为验证标签；删除核心信息缺失或数值不合理的记录，对有限缺失值进行均值填补或时间插值。

<div class="method-step__io" markdown="1">

**输入**：MIMIC-IV-v3.1 中 ICU 患者记录，包括 ICU 入院后的临床测量值、结构化变量和 ICU 期间的 ICD 编码诊断。<br>
**输出**：具有完整核心结构化变量、早期临床指标和多标签 ICD 诊断集合的患者记录。

</div>

**直观理解**：只使用入院早期能看到的信息，模拟较早阶段的诊断判断，并减少模型利用住院后期信息的机会。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基础任务与疾病特征选择

按频率排除最常见的 10% ICD 标签，删除阳性病例少于 100 例的诊断，并选择 $M=200$ 个数据完整度至少为 70%、无严重异常模式的疾病。对每个疾病 $d_k$，用等量阳性与阴性患者训练随机森林，按特征重要性选出诊断特异的前 $K_f$ 个指标集合 $F_k$。

<div class="method-step__io" markdown="1">

**输入**：预处理后的多标签患者记录及其 ICD 诊断标签。<br>
**输出**：BA 的患者—诊断二元验证实例，以及每个疾病对应的特征集合 $F_k$。

</div>

**直观理解**：先去掉过于宽泛或样本太少的疾病，避免任务被类别频率主导；随机森林只用于找出哪些指标适合比较病例，不会限制 LLM 最终看到的输入。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 疾病特异的患者相似度计算

仅在 $F_k$ 上计算平均特征距离：连续变量和有序变量先归一化后比较绝对差，二元或类别变量使用是否相等的指示距离。对同样患有 $d_k$ 的患者对估计距离分布，并取第 25 百分位 $\theta_k$ 与第 75 百分位 $\phi_k$ 作为相似和不相似的阈值。

<div class="method-step__io" markdown="1">

**输入**：患者对 $(p_i,p_j)$、目标诊断 $d_k$ 及其特征集合 $F_k$。<br>
**输出**：诊断 $d_k$ 的病例相似度尺度，以及用于挖掘对比病例的阈值 $\theta_k$ 和 $\phi_k$。

</div>

**直观理解**：不同疾病依赖的临床指标不同，因此不能用一套固定距离比较所有病例；该步骤为每个疾病建立自己的“相似程度尺子”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### DDT、DCT 对比样本构造与专家核验

DDT 选择一个患有 $d_k$ 的患者与一个未患有 $d_k$、但距离小于 $\theta_k$ 的患者；DCT 选择两个均患有 $d_k$、但距离大于 $\phi_k$ 的患者。每个疾病保留距离最小的 DDT 对和距离最大的 DCT 对，并由专家检查疾病特征的临床意义及抽样病例的目标诊断可判断性。

<div class="method-step__io" markdown="1">

**输入**：患者—诊断标签、疾病特异距离、阈值 $\theta_k$ 和 $\phi_k$。<br>
**输出**：BA、DDT 和 DCT 的评估实例，以及经临床合理性检查的对比病例集合。

</div>

**直观理解**：DDT 故意制造“外表相像、结论不同”，DCT 制造“外表不同、结论相同”；它们分别测试模型能否拒绝表面类比，以及能否识别跨表现形式的共同疾病。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 诊断特异的患者距离

$$
\mathrm{dist}_{k}(p_i,p_j)=\frac{1}{|F_k|}\sum_{f\in F_k}\delta_f(x_{i,f},x_{j,f})
$$

**符号说明**

- $\mathrm{dist}_{k}(p_i,p_j)$：以诊断 $d_k$ 为参照时，患者 $p_i$ 与 $p_j$ 的平均特征距离。
- $F_k$：由随机森林为诊断 $d_k$ 选出的诊断特异临床指标集合。
- $|F_k|$：特征集合 $F_k$ 中的指标数量。
- $f$：特征集合 $F_k$ 中的一个临床指标。
- $x_{i,f},x_{j,f}$：患者 $p_i$ 和 $p_j$ 在特征 $f$ 上的取值。
- $\delta_f$：特征 $f$ 的类型特定距离：连续或有序变量使用归一化绝对差，类别变量使用不相等指示函数。

<div class="equation-explanation" markdown="1">

**直观理解**：公式把一个疾病相关的多个指标差异取平均，得到病例之间的总体距离。先按变量类型标准化比较方式，可以避免某个数值尺度较大的指标单独支配相似度。<br>
**原文位置**：第 3.3 节，公式 (1)；连续变量与类别变量的定义见公式 (2)–(3)

</div>

</div>

<div class="equation-block" markdown="1">

#### 患者—诊断二元验证标签

$$
y_{p,k}=\mathbb{1}[d_k\in Y_p]
$$

**符号说明**

- $y_{p,k}$：患者 $p$ 是否具有候选诊断 $d_k$ 的二元标签。
- $d_k$：第 $k$ 个候选 ICD 诊断。
- $Y_p$：患者 $p$ 在 ICU 记录中对应的 ICD 诊断集合。
- $\mathbb{1}[\cdot]$：指示函数：括号内命题为真时取 1，否则取 0。

<div class="equation-explanation" markdown="1">

**直观理解**：该式将多标签诊断记录转换为清晰的判断题：若目标疾病出现在患者的诊断集合中，标签就是 1；否则就是 0。它是 BA、DDT 和 DCT 统一标签定义的基础。<br>
**原文位置**：第 3 节，方法问题定义

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告 SUP-MIMIC 是否训练或微调被评估的 LLM，也未给出 LLM 的损失函数或优化目标。随机森林在每个疾病上用于特征重要性排序和病例配对，并非文中所述的最终 LLM 训练目标；其训练过程也未给出可复现的具体超参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 多标签患者—诊断二元验证**

患者 $p$ 具有临床指标向量 $\mathbf{X}_p$ 和诊断集合 $Y_p\subseteq\mathcal{D}$，对候选诊断 $d_k$ 定义标签 $y_{p,k}=\mathbb{1}[d_k\in Y_p]$。完整的 448 维特征向量作为 LLM 输入，而二元标签用于构造和评价患者—诊断验证实例。

> 直观理解：模型不是从所有疾病中一次性选一个答案，而是逐一回答“这个病例是否有目标疾病”，因此同一患者可以对应多个验证实例和多个诊断。

**2. 疾病特异特征与相似度**

对每个疾病 $d_k$，随机森林从平衡的阳性、阴性患者中选出 $F_k$；患者距离只在该集合上计算，并根据同病患者距离分布设定 $\theta_k$ 与 $\phi_k$。

> 直观理解：例如某疾病可能主要依赖实验室指标，另一疾病可能更依赖生命体征；按疾病选择特征可以使“相似”更贴近该疾病的临床证据，而不是被无关变量影响。

**3. 自然发生的对抗性病例对**

DDT 的集合满足 $y_{i,k}=1$、$y_{j,k}=0$ 且 $d^k_{ij}<\theta_k$；DCT 的集合满足 $y_{i,k}=1$、$y_{j,k}=1$ 且 $d^k_{ij}>\phi_k$。这里的“对抗性”指从真实记录中挖掘特征与诊断标签相冲突的对比病例，并非合成扰动或针对模型的攻击。

> 直观理解：样本不靠人为修改病例来制造困难，而是从真实临床数据中寻找自然存在的诊断歧义和诊断汇聚，因此更接近模型在真实记录中会遇到的困难。

**训练与推理**

数据处理阶段先从 ICU 入院后前 24 小时记录中形成完整的 448 维患者特征，并依据 ICD 标签生成 $y_{p,k}$。对每个候选疾病，以等量阳性和阴性患者训练随机森林并获得 $F_k$，再在该特征空间计算距离、估计 $\theta_k$ 和 $\phi_k$，分别构造 BA、DDT 和 DCT 实例。推理或评估阶段，LLM 接收完整临床特征而不是仅接收 $F_k$，并对候选诊断执行二元验证；DDT 与 DCT 的正确性分别由“相似病例应有不同诊断结论”和“差异病例仍共享目标诊断”来检验。原文未明确报告具体提示词、输出解析规则或是否进行模型微调。

**复现信息**

复现该方法所必需的选择包括：数据源为 MIMIC-IV-v3.1，输入窗口为 ICU 入院后 24 小时；保留 $M=200$ 个疾病，要求每个疾病至少有 100 个阳性病例、数据完整度至少 70%，并排除最常见的 10% 诊断标签。距离阈值取同病患者对距离分布的第 25 与第 75 百分位；每个疾病保留前 $m$ 个合格病例对，DDT 取距离最小者、DCT 取距离最大者，但 $m$、$K_f$、随机森林具体配置、数据划分及 LLM 评估提示词在所给方法章节中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- SUP-MIMIC：基于 $MIMIC\text{-}IV\text{-}v3.1$ 构建的多任务临床诊断基准，覆盖 $200$ 种疾病，并映射到 $17$ 个基于 ICD 的疾病类别。原文未明确报告训练集、验证集、测试集的具体划分规模；本实验内容显示其主要用于统一测试不同模型的诊断验证能力。
- Basic Assessment（BA）：标准诊断验证任务。每个样本包含患者 $p$ 和锚定诊断 $d_k$，模型判断该患者的临床资料是否支持该诊断，用于测量基础点式诊断性能。
- Diagnostic Divergence Task（DDT）与 Diagnostic Convergence Task（DCT）：两类成对对抗评测。DDT 将表型相似但诊断标签相反的患者配成一对，测试模型能否对同一锚定诊断“一接受、一拒绝”；DCT 将临床表现不同但共享同一诊断的患者配成一对，测试模型能否识别“多种表现、同一疾病”。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy、Sick Recall 与 Healthy Recall**

Accuracy 衡量全部二元诊断验证决策的正确比例；Sick Recall 衡量真实支持锚定诊断的患者被正确识别的比例；Healthy Recall 衡量真实不支持锚定诊断的患者被正确拒绝的比例。每个模型对患者 $p$ 和诊断 $d_k$ 输出 $4\hat{y}_{p,k}\in\{0,1\}\u00024$，其中 $1$ 表示支持、$0$ 表示不支持。 （Accuracy、Sick Recall 和 Healthy Recall 均越高越好；同时比较两类 Recall 的差距，以识别偏向“健康”或拒绝诊断的决策倾向。）

</div>
<div class="metric-item" markdown="1">

**Pairwise Diagnostic Robustness Accuracy（PDRA）**

PDRA 只在一对患者的全部决策都正确时计为正确。DDT 的正确条件是模型对阳性患者接受 $d_k$、对困难阴性患者拒绝 $d_k$；DCT 的正确条件是模型对两个真实阳性患者都接受 $d_k$。因此它测量的是成对关系是否保持一致，而非单个样本是否偶然答对。 （越高越好。较低的 PDRA 表明点式准确率可能掩盖了模型无法同时处理相互关联的两个病例。）

</div>
<div class="metric-item" markdown="1">

**SUP-MIMIC Robustness Score（SRS）**

SRS 将 BA 的准确率与 DDT、DCT 的成对鲁棒性结合，定义为 $\mathrm{SRS}=\mathrm{Acc}_{\mathrm{BA}}\cdot\sqrt{\mathrm{PDRA}_{\mathrm{DDT}}\cdot\mathrm{PDRA}_{\mathrm{DCT}}}$。几何平均会惩罚某一对抗任务表现特别差的模型。 （越高越好；它要求模型既具备基础诊断能力，又不能在 DDT 或 DCT 中出现明显短板。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 主结果：点式准确率与成对鲁棒性的差异

<div class="result-value" markdown="1">

模型在 DDT 上的点式准确率并不必然意味着稳定推理；例如，GPT-4o 的 $\mathrm{PDRA}_{\mathrm{DDT}}$ 为 $0.5586$，而 Llama3.3-70B 为 $0.2038$。作者指出，DDT 的成对指标显著暴露了被单个样本准确率掩盖的不一致性。

</div>

模型可能在两个病例中各自猜对一个，或因为多数样本不支持该诊断而普遍选择“拒绝”，但仍无法识别同一锚定诊断在相似病例之间的真正差异。该结果支持 DDT 具有额外诊断价值，但不能单独证明模型进行了因果推理，因为评测仍基于文本输入和二元决策。

<div class="result-source" markdown="1">

来源：Section 4.2 Main Results；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Pairwise evaluation exposes reasoning inconsistency masked by pointwise accuracy.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 主结果：DCT 暴露非典型表现识别失败与健康偏置

<div class="result-value" markdown="1">

所有模型的 DCT 准确率均低于 $0.53$，部分模型低于 $0.35$；同时 Healthy Recall 比 Sick Recall 高 $30$ 至 $50$ 个百分点。作者据此认为，模型在患者表现偏离典型模式时倾向于拒绝锚定诊断，造成系统性漏诊风险。

</div>

DCT 要求模型把两个外观不同的病例都识别为同一种疾病，因此不能只寻找典型症状组合。较高的 Healthy Recall 说明模型更擅长排除诊断而不是确认非典型疾病。这个结果揭示了漏诊倾向，但由于原文没有给出每个模型的 Recall 差值和统计不确定性，不能据此精确比较所有模型的偏置程度。

<div class="result-source" markdown="1">

来源：Section 4.2 Main Results；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Because DCT requires accepting the anchor diagnosis for two clinically dissimilar patients, success depends on recognizing atypical presentations.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 主结果：医学预训练模型的综合鲁棒性

<div class="result-value" markdown="1">

HuatuoGPT-o1-8B 的 SRS 为 $0.3976$，在表中为最高值，但它并未在任何单项任务上取得最高成绩；作者还报告，医学预训练模型相较规模相近或更大的通用模型具有更高 SRS 和更小的 Sick–Healthy Recall 差距。

</div>

综合分数强调均衡性：模型不需要在某一个任务上最好，但不能在 DDT 或 DCT 中严重失稳。这一结果表明医学领域训练可能改善跨任务一致性，不过它并不能证明医学预训练本身是唯一原因，因为模型架构、数据、提示行为和训练目标也可能同时不同。

<div class="result-source" markdown="1">

来源：Section 4.2 Main Results；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

HuatuoGPT-o1-8B attains the highest SRS overall without leading on any individual task.

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

- Llama3.3-70B、Qwen2.5-7B/14B/32B、Mistral-7B、DeepSeek-V3 和 GLM-4.7：开放源代码通用大语言模型，用于考察通用语言模型在不同规模和模型系列下的临床诊断鲁棒性。
- HuatuoGPT-o1-8B 和 MedReason-8B：开放源代码医学大语言模型，用于与规模相近或更大的通用模型比较医学领域预训练是否改善成对诊断一致性。
- GPT-3.5、GPT-4o、Gemini-2.5 Flash 和 Claude Sonnet 4.5：闭源通用大语言模型，用于检验先进商业模型是否已经具备超越开放模型的矛盾证据处理能力。
- Qwen2.5 的 $7\mathrm{B}$、$14\mathrm{B}$ 和 $32\mathrm{B}$ 变体：控制架构与训练来源后进行的规模对比，用于隔离参数规模对 BA、DDT 和 DCT 的影响。

**实验想回答的问题**

- 在基本诊断验证表现相近或较高的情况下，模型能否在诊断分歧任务（DDT）和诊断收敛任务（DCT）中保持成对诊断关系的一致性，而不是依赖“疾病不存在”的统计捷径？
- 医学领域预训练、模型规模和疾病类别的差异，分别如何影响模型对矛盾证据、非典型表现及跨系统证据的鲁棒性？

**实验实现**

所有任务都被统一为针对锚定诊断 $d_k$ 的二元诊断验证。主结果表中的指标是五次独立运行的均值，标准差为简洁起见未报告。DDT 和 DCT 额外采用成对评估，以避免疾病稀有性和默认拒绝诊断策略造成的点式准确率假象。失败模式分析对 $128{,}904$ 个错误预测进行结构化理由分析，并划分为 Combinatorial Neglect、Feature Misweighting、Comorbidity Conflation 和 Biomarker Omission 四类。类别分析将疾病划分为 $17$ 类，并使用单因素方差分析检验任务间差异。原文未明确报告提示词、解码参数、随机种子、样本具体划分及置信区间。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 规模分析：Qwen2.5-7B、14B 与 32B | Qwen2.5 从 $7\mathrm{B}$ 扩展到 $32\mathrm{B}$ 时，BA 从约 $0.30$ 升至 $0.56$，DDT 从约 $0.50$ 升至 $0.62$，而 DCT 仅从约 $0.31$ 升至 $0.35$，且 $14\mathrm{B}$ 在 DCT 出现暂时下降。 | 在同一模型系列内控制架构和训练差异后，规模扩展明显增强了多数类模式识别和表面特征匹配，却几乎没有增强非典型表现下的整合推理。该分析支持“规模收益不均衡”的结论，但并不等同于严格因果证明，因为只比较了三个规模点，且原文未明确报告完整方差或显著性检验。 | Section 4.5 Scaling Analysis；Figure 7<br><span class="experiment-evidence">DCT, however, improves only marginally from 0.31 to 0.35, with a transient dip at 14B, indicating that the reasoning required to recognize atypical presentations resists parameter scaling almost entirely.</span> |
| 疾病类别分层：单系统生物标志物类别与跨系统整合类别 | 单因素方差分析拒绝三个任务表现完全一致的假设（各任务 $F\geq5.81$，$p<0.001$）。具有鲜明单系统生物标志物特征的类别在 BA、DDT、DCT 间较稳定；代谢、呼吸和肿瘤相关等需要跨系统证据的类别出现选择性的 DCT 崩溃，代谢和呼吸类别的显著性达到 $p<0.001$。 | 模型的脆弱性不是所有疾病都相同，而是随诊断所需的证据整合复杂度变化：单一器官系统的明显指标较易处理，多系统线索和共病背景则更容易触发 DCT 失败。该结果把失败模式与临床类别联系起来，但不能说明具体疾病类别的差异完全由证据整合造成，因为类别还可能包含不同的样本量、文本质量和疾病先验。 | Section 4.6 Disease Category Stratification；Figure 4<br><span class="experiment-evidence">Categories requiring cross-system evidence integration, including metabolic, respiratory, and neoplasm-related diseases, show selective DCT collapse with statistical significance (p < 0.001 for metabolic and respiratory categories).</span> |

**定性案例**

- 失败模式分析提供了一个具有代表性的定性结论：较弱模型（如 Mistral-7B 和 Qwen2.5-7B）超过 $20\%$ 的错误属于 Biomarker Omission，并伴随较高的 Comorbidity Conflation；较强通用模型则在基本指标利用方面改善，却在 DeepSeek-V3 和 GPT-4o 中出现接近一半错误属于 Combinatorial Neglect。其含义是，模型“看见”某个生物标志物并不代表能把它与其他证据联合用于最终诊断；原文仅说明代表性病例见 Appendix Table 3，未在所给实验摘录中提供具体病例内容。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution is a benchmark evaluating LLM diagnostic reasoning under ambiguous and contradictory clinical evidence.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`07836875f35f1ecbf2936927e6931a2b4d0fd5e6933d6ec256922db48d3c4aad`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
