---
title: "[论文解读] Rigorous Evaluation of Large Language Models for Malaria Drug Discovery: Trade-offs in Performance, Scale, and Resource Utility"
description: "[arXiv 2608.20418][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.20418"
announcement_date: "2026-08-24"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-24T02:08:47.311426+00:00"
source_sha256: "93252a9b04577e5d61eed7441da3d32da0776367dbcd5b51f478af2a6936d7cf"
tags:
  - "LLM 评测"
  - "LLM 其他"
  - "LLM Reasoning"
  - "抗疟药物发现"
  - "配体虚拟筛选"
  - "分子语言模型"
  - "SMILES"
  - "分布外泛化"
  - "Lo-Hi 不相似性分割"
  - "生物活性预测"
  - "指令微调"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.20418</p>

# Rigorous Evaluation of Large Language Models for Malaria Drug Discovery: Trade-offs in Performance, Scale, and Resource Utility

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Marvellous O. Ajala, Zainab Ashimiyu-Abdusalam, Comfort Adesina</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Magami Open Sciences Initiative</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20418v1) · [PDF 下载](https://arxiv.org/pdf/2608.20418v1) · **关键词** 抗疟药物发现, 配体虚拟筛选, 分子语言模型, SMILES, 分布外泛化, Lo-Hi 不相似性分割, 生物活性预测, 指令微调<br>


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

本文位于抗疟药物发现、化学信息学与大语言模型交叉领域，关注配体虚拟筛选（virtual screening，VS）：根据分子结构预测其是否可能对疟原虫具有活性，并优先选择少量候选物进行实验验证。分子通常以 SMILES 字符串表示，使其能够被序列模型处理；本文重点考察模型能否在与训练分子结构差异较大的测试集上保持活性判别能力，而不是仅记忆相似分子。评价同时关注整体排序能力与筛选前 1% 候选物中的活性富集程度。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**配体虚拟筛选与生物活性预测**

配体虚拟筛选先对大量小分子进行计算排序，再对排名靠前的分子开展实验。本文的预测目标是依据分子的 SMILES 结构及测定条件，判断其是否属于抗疟活性分子。

</div>
<div class="concept-item" markdown="1">

**SMILES 与分子表示**

SMILES 是用字符序列描述原子、键和环结构的分子表示方式，因此可以像文本一样输入语言模型。模型需要从这种序列中学习结构与生物活性之间的关系，而不是只理解普通自然语言。

</div>
<div class="concept-item" markdown="1">

**分子分割与分布外泛化**

分割方法决定哪些分子用于训练、验证和测试。本文采用 Lo-Hi 不相似性分割，限制不同数据子集之间的 Tanimoto 相似度，尽量避免结构近似物跨越数据边界，从而测试模型面对新化学骨架时的泛化能力。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定经过整理的抗疟活性数据集，每条记录包含分子结构、活性标签以及可能的测定条件，例如疟原虫菌株、实验时长和机制背景；模型输出该分子的活性预测分数或活性类别。研究设置要求训练集、验证集和测试集在结构上具有较强不相似性，并按测定方法分别处理，以检验模型在分布外化学空间中的排序与判别能力。论文还比较两种知识注入方式：通过参数高效微调使模型学习任务规律，以及仅用少量示例进行上下文学习（few-shot prompting）。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入分子，通常以 SMILES 字符串表示。

</div>
<div class="notation-item" markdown="1">

**$y$**

分子的抗疟活性标签，例如活性或非活性。

</div>
<div class="notation-item" markdown="1">

**$s(x)$**

模型对分子 $x$ 输出的活性评分或排序分数；分数越高通常表示越优先进行实验筛选。

</div>
<div class="notation-item" markdown="1">

**$T_{\mathrm{sim}}$**

跨数据子集允许的最大 Tanimoto 相似度阈值；Lo-Hi 分割通过控制该阈值来构造结构上不相似的训练、验证和测试分子集合。

</div>

</div>

**直接相关的工作**

- **ChEMBL 与 ChEMBL Legacy Malaria 数据**: 本文以 ChEMBL Legacy Malaria corpus 为基础构建 Malaria-Instruct，但进一步处理类别不平衡、测定异质性和重复生物活性记录，并统一 48 小时与 96 小时读数、补充部分阴性样本。因此，它不是直接使用原始数据库，而是将其整理为适合抗疟虚拟筛选指令微调的数据集。
- **LlaSMol 与 TxGemma**: LlaSMol 是经过化学指令数据训练的分子语言模型，提供了化学结构相关的先验；TxGemma 面向治疗学任务进行生物医学专业化预训练。本文将二者作为关键开源模型进行比较，以区分化学专业预训练与生物医学专业预训练在抗疟活性预测中的作用。

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

方法将疟疾生物活性数据整理为可监督学习的分子预测任务：输入是标准化分子结构及部分实验上下文，输出是化合物是否具有活性及其排序分数。研究分别训练经典指纹模型和参数高效微调的开源大语言模型，并将其与未微调模型的少样本推理进行比较；最终在严格的结构分布外验证集上，以分类判别能力、前列化合物富集效果和资源消耗共同评价模型。直观地说，研究不是只问模型“平均判断是否正确”，还问它能否把真正的活性分子排到最前面，以及这种能力需要多少显存和推理时间。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 数据筛选、去重与上下文构造

仅保留 potency 和 IC50 测定；对每个分子—测定组合聚合技术重复测量，只有全部重复一致为活性或非活性时才保留，冲突记录删除。24、48 和 96 小时读数也按一致性规则协调；随后通过电荷中和、母体片段提取、价态和官能团表示规范化以及规范互变异构体选择统一分子表示，并为 TxGemma 构造包含测定类型、菌株和实验特征的结构化上下文。

<div class="method-step__io" markdown="1">

**输入**：输入为 ChEMBL Legacy Malaria corpus 中的分子、potency 或 IC50 活性测定记录、重复测量结果、时间点、测定类型、靶点、疟原虫菌株和实验条件。<br>
**输出**：输出是 Malaria-Instruct 数据集，每条记录包含标准化分子表示、二元活性标签，以及供 TxGemma 使用的测定上下文；LlaSmol 保持其原有格式，仅使用测定层面的细节。

</div>

**直观理解**：这一步像先清理实验台账：删除无法确定的标签，把同一化合物的不同写法统一，并补充“实验是在什么条件下做的”。这样模型学习的是较可靠、可比较的监督信号，而不是重复测量噪声。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 化学空间中的负样本补充与分布外划分

对于主要由活性化合物组成、缺少非活性观察的确认性测定，先按数据集划分完成训练、测试和验证，再从被舍弃测定中计算 ECFP4，经 PCA 降维后用欧氏距离 t-SNE 投影到二维，并在已确认活性样本的凸包区域内选择化学上邻近的候选负样本，使正负比例恢复到整体 Malaria-Instruct 数据集的水平。随后采用 Lo-Hi 划分：训练—测试样本的最大 Tanimoto 相似度不超过 $0.4$，训练—验证样本的最大相似度不超过 $0.55$，且每个测定独立划分。

<div class="method-step__io" markdown="1">

**输入**：输入为清理后的活性数据、被舍弃测定中的候选分子，以及每个分子的 ECFP4 指纹；该指纹使用半径 $2$ 和 $2048$ 个二进制位。<br>
**输出**：输出是带有化学上相关负样本的训练数据，以及结构与训练分布明确不同的训练、测试和验证分区；微调模型的每次重复实验都重新抽取 Lo-Hi 划分。

</div>

**直观理解**：补负样本是避免模型只看到“几乎全是活性”的不完整课堂；Lo-Hi 划分则像用没有见过的化学骨架考试，而不是把训练分子换个名字再考一次，因此更接近真实的新颖命中发现。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 模型训练与监督微调

Random Forest 和 XGBoost 直接以半径 $2$、$2048$ 位 Morgan 指纹为特征训练。开源大语言模型采用参数高效微调：Gemma-2 和 TxGemma 分别测试 $2$B 与 $9$B 参数规模，LlaSMol-Mistral 测试 $7$B；微调语料由 $70\%$ 的少样本格式实例和 $30\%$ 的零样本实例组成，少样本示例数从 $\{2,3,4,5\}$ 均匀抽取，所有训练示例均来自训练分区。

<div class="method-step__io" markdown="1">

**输入**：输入包括训练分区中的分子—活性实例、ECFP4 指纹，以及供不同模型使用的 SMILES、少量示例和测定上下文；比较对象包括 Random Forest、XGBoost、Gemma-2、TxGemma 和 LlaSMol-Mistral。<br>
**输出**：输出是能够根据分子及相应上下文生成二元活性预测和可用于排序的分数的微调模型，以及用于对照的经典分类器；每个微调模型进行两次独立 Lo-Hi 重划分实验。

</div>

**直观理解**：经典模型把分子压缩成固定长度的“化学指纹”后分类；大语言模型则通过任务微调把分子文本和实验条件与活性标签联系起来。微调相当于改变模型内部参数，使其真正记住该任务的结构—活性规律，而不只是临时模仿提示中的几个例子。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 少样本推理、预测解析与评价

少样本条件下，将训练分区或规定分区中的分子—活性示例放入查询提示，但查询分子严格来自验证集；所有最终验证实例均不含验证分子或其结构邻居。解析模型输出得到二元预测，并在可用时从输出 token 的 logits 提取概率分数，否则依据预测类别标签的排序生成分数；计算 MCC、ROC-AUC、EF@1%、准确率、精确率及推理时间和显存需求。

<div class="method-step__io" markdown="1">

**输入**：输入为未微调开源模型、Gemini 2.5 和 OpenAI o3，以及验证分区中的查询分子；开源和闭源模型分别使用 $3$、$4$、$5$ 个示例，闭源模型每种条件抽取 $500$ 个分子。<br>
**输出**：输出是每个模型和条件的验证集预测、分类指标、前 $1\%$ 排名富集结果及资源记录；ROC-AUC 衡量整体排序判别，MCC 衡量类别不平衡下的综合分类质量，EF@1% 衡量真实筛选中最前列化合物的实用富集。

</div>

**直观理解**：最后像一次盲测：模型不能看到验证答案，也不能靠与训练分子过于相似的邻居取巧。ROC-AUC 看整体排序是否可靠，EF@1% 看实验人员真正只买最前面 $1\%$ 的化合物时能多找到多少活性分子，MCC 则防止“全部猜成多数类”造成虚高表现。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确给出可直接复制的训练损失函数或优化目标，因此不补写具体公式。技术上，经典模型学习由 ECFP4 指纹到二元活性预测的分类器；大语言模型通过 Malaria-Instruct 的分子—标签实例进行参数高效任务微调，使模型能够生成活性类别及其可排序分数。最终验证指标并非训练目标的等价替代，其中 EF@1% 被作者指定为虚拟筛选的主要操作性指标，ROC-AUC 和 MCC 用于分别衡量整体排序与类别不平衡下的判别质量。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 保守标签清理与实验上下文模块**

该模块按唯一分子—测定对聚合重复读数，并对 24、48、96 小时读数应用一致性判定；全体保留分子经过统一化学标准化。TxGemma 的上下文列融合专家标注和经专家验证模板约束的 LLM 结构化抽取，编码测定性质、具体 Plasmodium 菌株及实验特征。

> 直观理解：生物活性不是脱离实验条件的分子固有属性；该模块尽量确保标签明确，并让适合使用实验上下文的模型知道“在哪种测定和菌株环境下”观察到活性。

**2. Lo-Hi 结构分布外划分模块**

模块在 ECFP4 指纹上计算分子间 Tanimoto 相似度，约束任意训练—测试分子对的最大相似度为 $0.4$，任意训练—验证分子对的最大相似度为 $0.55$，并按测定分别执行划分。负样本增强在划分之后、按测定和分区进行，避免候选负样本跨分区泄漏。

> 直观理解：它专门检验模型能否迁移到新化学结构，而不是只识别训练集中出现过的局部结构。把负样本增强放在划分之后，也避免同一个补充样本间接影响测试结果。

**3. 双范式模型比较模块**

模块并列比较指纹驱动的 Random Forest/XGBoost、参数高效微调的 Gemma-2、TxGemma、LlaSMol-Mistral，以及未微调开源和闭源模型的少样本上下文学习。微调模型最终在验证集以零样本格式评估，少样本模型则按独立 shot-count 划分构造上下文；闭源模型不进行微调，原因是研究目标强调低资源、开放基础设施下的可部署性。

> 直观理解：这种设计把三个因素拆开：传统分子机器学习是否足够、领域预训练和任务微调是否有用、以及一般大模型仅凭提示能否完成任务。因而性能差异不只反映模型大小，也反映模型是否真正接受了生物医学或化学领域适配。

**训练与推理**

训练阶段，先仅使用训练分区构造微调实例；其中 $70\%$ 为包含 $2$ 至 $5$ 个训练示例的少样本格式，$30\%$ 为零样本格式。训练期间监控测试分区，但最终性能只在验证分区报告；微调模型采用两次独立实验并重新进行 Lo-Hi 划分，经典模型进行五次独立重复并在每次重复中重新划分。推理阶段，微调模型以验证分子为查询并使用零样本格式；未微调模型在每个 $3$、$4$、$5$ shot 条件下将示例置于查询前，查询分子严格来自验证集。输出被解析为二元活性预测；若模型提供输出 token logits，则由其导出概率分数，否则使用预测类别的排名形成排序分数。闭源模型 Gemini 2.5 和 OpenAI o3 通过公开 API 进行少样本推理，每种条件使用 $500$ 个验证分子并重复两次。

**复现信息**

为保证可复现性，分子采用半径 $2$、$2048$ 位 ECFP4/Morgan 指纹进行相似度划分和经典模型训练；Random Forest 与 XGBoost 使用默认超参数和固定随机状态 $2024$，各进行五次重复。所有开源大语言模型均采用参数高效微调；训练在 Google Colab Pro+ 上完成，文中报告 $2$B 模型训练使用 $16$GB GPU、$7$B 和 $9$B 模型训练使用 $24$GB GPU，推理至少需要 $24$GB GPU。验证预测使用 vLLM 以降低推理延迟；闭源模型未微调，主要因为 API 微调不符合本文面向低资源、开放基础设施研究环境的目标。数据集地址为 https://zenodo.org/records/19222923，代码地址为 https://github.com/Magami-Open-Sciences-Initiative/LLMS-for-Malaria。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Malaria-Instruct：由 ChEMBL Legacy Malaria corpus 整理而成的指令跟随数据集，用于疟疾虚拟筛选；原文未明确报告其样本规模、分子数量及具体数据划分规模。
- 严格的分布外测试划分：用于检验模型对训练阶段未见结构分布的泛化能力；原文说明使用了 rigorous out-of-distribution data split，但未明确报告划分比例、结构去重规则或测试集规模。
- ChEMBL Legacy Malaria corpus：Malaria-Instruct 的数据来源，承担疟疾药物活性数据基础语料的角色；原文未明确报告该语料库在本实验中的完整规模和筛选标准。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**ROC-AUC**

受试者工作特征曲线下面积，衡量模型将活性分子排在非活性分子之前的整体排序判别能力；$0.5$ 约等于随机排序，越高越好。 （越高越好；它反映全阈值范围的总体区分能力，但不直接说明在极低筛选比例下能找到多少真正活性分子。）

</div>
<div class="metric-item" markdown="1">

**EF@1%**

前 $1\%$ 筛选比例下的富集因子，衡量模型挑出的最前面 $1\%$ 分子相对于随机筛选包含了多少额外活性分子。 （越高越好；它更贴近虚拟筛选的实际用途，即在只能实验验证极少数候选物时提高命中密度。）

</div>
<div class="metric-item" markdown="1">

**资源效用**

论文标题所指的 performance、scale 与 resource utility 之间的比较维度，用于讨论性能收益与模型规模或推理资源成本的关系；原文所给材料未明确报告其独立的数学定义或单独数值指标。 （原文未明确报告统一的数值判定方向；因此不能将其解释为一个已明确规定的越高或越低越好的单一指标。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 不同模型的整体判别性能：领域微调开源 LLM 与经典模型、闭源模型比较

<div class="result-value" markdown="1">

TxGemma-9B 取得最高 ROC-AUC，为 $0.731\pm0.005$；Gemini 2.5 约为 $0.53$，OpenAI o3 约为 $0.59$。摘要还明确指出，微调后的 LLM 整体超过所有基线。

</div>

该结果支持作者关于领域微调开源模型具有较强总体排序能力的主张，尤其说明通用闭源模型的规模或推理能力不能自动替代疟疾药物领域适配。但 ROC-AUC 只说明整体排序，不等于模型在实际前 $1\%$ 候选筛选中一定最好；同时，摘要没有给出 Random Forest、XGBoost、Gemma-2 或 TxGemma-2B 的具体 ROC-AUC，因此不能据此计算它们之间的精确差距。

<div class="result-source" markdown="1">

来源：摘要；第 4 节 Results 开头

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Fine-tuned LLMs substantially outperformed all baselines: TxGemma-9B achieved the highest ROC-AUC ($0.731 \pm 0.005$)

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 低比例实际筛选能力：以 EF@1% 衡量前端候选富集

<div class="result-value" markdown="1">

LlaSMol-Mistral-7B 获得最佳 EF@1%，约为 $4.99$。

</div>

这表明 LlaSMol-Mistral-7B 在只挑选排名最前 $1\%$ 分子时，能够把活性分子集中到比随机筛选更高的密度，因而在实验验证预算有限的虚拟筛选场景中具有实际意义。它也说明最高 ROC-AUC 模型不必然是低比例富集最好的模型；但原文材料没有提供其他模型的 EF@1% 数值、置信区间或统计显著性，因此不能判断优势是否稳定。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

and LlaSMol-Mistral-7B the best enrichment factor (EF@1\% $\approx$ 4.99).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 领域适配与通用闭源模型的比较

<div class="result-value" markdown="1">

摘要报告 Gemini 2.5 的 ROC-AUC 约为 $0.53$，OpenAI o3 约为 $0.59$；二者在没有微调时均未达到可靠判别水平。作者据此认为，经过领域微调的开源模型在结构上具有挑战性的条件下超过了闭源推理模型。

</div>

该比较主要检验“通用能力是否足以完成专业虚拟筛选”，结果表明仅依靠 few-shot 提示并不能稳定解决该任务。不过，这不是对闭源模型全部能力的否定：比较的是特定 few-shot 协议，而不是对其进行同等领域微调后的性能；此外，原文未明确报告闭源模型的提示模板、调用次数或成本。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

neither Gemini 2.5 (ROC-AUC $\approx 0.53$) nor o3 (ROC-AUC $\approx 0.59$) achieved reliable discrimination without fine-tuning.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验摘录没有报告数据集规模、活性标签定义、分布外划分细节、分子表示、随机种子、置信区间覆盖范围及完整超参数；这些信息不足以全面判断结果的可复现性和统计稳健性。
- 实验主要验证模型在单一疟疾数据来源和分布外测试上的排序与富集能力；材料未提供真实前瞻性实验验证、跨数据集外部验证、推理成本的统一量化，或闭源模型在同等领域微调条件下的公平比较，因此不能把结果直接推广为所有抗疟药物发现任务中的普遍优势。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Random Forest：经典集成机器学习模型，用于检验 LLM 方法是否超过传统分子活性预测管线。
- XGBoost：经典梯度提升模型，与 Random Forest 共同构成非 LLM 基线，用于比较传统监督学习方法的判别能力。
- Gemini 2.5：闭源前沿模型，在 few-shot 条件下评估，用于检验通用闭源模型能否在没有领域微调时完成该任务。
- OpenAI o3：另一闭源推理模型，在 few-shot 条件下评估，用于比较更强通用推理能力与领域专门化微调之间的差异。

**实验想回答的问题**

- 在严格的分布外数据划分下，经过领域微调的开源大语言模型是否能够在疟疾药物虚拟筛选中超过经典机器学习模型以及闭源大语言模型？
- 模型规模、生物医学或化学领域预训练、领域微调与推理资源之间如何影响判别性能和实际筛选富集效果？

**实验实现**

实验比较了五个开源模型，即 Gemma-2 2B/9B、TxGemma-2B/9B 和 LlaSMol-Mistral-7B；其中重点比较领域微调后的模型，并将闭源模型 Gemini 2.5 与 OpenAI o3 置于 few-shot 条件下。经典模型使用训练后的 Random Forest 和 XGBoost。评价采用严格的分布外划分；对于闭源模型，报告其最佳上下文学习结果，对于训练模型，报告结果均值。原文未明确报告各模型的训练轮数、分子表示、随机种子数量、硬件、推理成本、few-shot 示例数及完整超参数。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除领域微调：TxGemma-9B 的微调模型与最佳 few-shot 条件比较 | TxGemma-9B 的 ROC-AUC 从 $0.731$ 降至 $0.499$。 | 这一对照直接隔离领域微调的作用：模型在微调后具有较好的活性排序能力，去掉领域适配后接近随机水平，支持“领域微调不可或缺”的作者结论。它不能证明所有模型、所有数据集或所有提示策略都会产生同样幅度的下降，因为该结果只明确涉及 TxGemma-9B 及其最佳 few-shot 对照。 | 摘要<br><span class="experiment-evidence">Domain-specific fine-tuning proved categorically indispensable with TxGemma-9B collapsing from ROC-AUC 0.731 to 0.499, under its best few-shot condition</span> |
| 预训练领域与模型规模的对照 | 作者报告，生物医学预训练在相同规模下具有可测优势，而化学感知预训练产生更好的前瞻性富集；原文所给材料未明确报告该消融中每个模型的具体分数或差值。 | 该分析试图区分两种来源：模型容量本身，以及预训练语料是否包含与生物医学或化学结构相关的知识。结果的方向性支持领域相关预训练有助于任务迁移，但由于缺少逐组数值、方差和严格匹配信息，不能据此断言优势大小，也不能完全排除模型架构或训练程序差异的影响。 | 摘要<br><span class="experiment-evidence">Biomedical pretraining conferred a measurable advantage at equivalent scale, while chemistry-aware pretraining yielded superior prospective enrichment.</span> |

**定性案例**

- 原文所给材料未提供具体分子、预测解释、成功命中候选物或失败案例，因此无法构造可核查的定性案例研究。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Its main contribution is a rigorous out-of-distribution evaluation of open and proprietary LLMs for a specialized drug-discovery task, including resource and scale comparisons.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`93252a9b04577e5d61eed7441da3d32da0776367dbcd5b51f478af2a6936d7cf`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
