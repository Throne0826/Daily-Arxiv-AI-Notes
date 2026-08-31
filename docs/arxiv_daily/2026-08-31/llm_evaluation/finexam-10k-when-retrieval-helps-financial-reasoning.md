---
title: "[论文解读] FinExam-10K: When Retrieval Helps Financial Reasoning?"
description: "[arXiv 2608.28155][LLM 评测] 原文未明确报告。"
arxiv_id: "2608.28155"
announcement_date: "2026-08-31"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-31T05:39:50.619191+00:00"
source_sha256: "1e52b7cf1070b4f74f0afa1ad8b4ea3d5db3365745c7b98ec469d7da6f251c23"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "金融专业考试推理"
  - "CFA与FRM基准"
  - "上下文完整性"
  - "检索增强生成"
  - "选择性检索"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.28155</p>

# FinExam-10K: When Retrieval Helps Financial Reasoning?

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-31</span>
<span><strong>作者</strong> Yan Lin, Jingyu Sun, Zhongliang Guo, Qing Li, Zhuohan Xie, Yuxia Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Newcastle University；Affiliation: University of Manchester；Affiliation: University of Melbourne；Affiliation: University of Aberdeen；Affiliation: University of Groningen；Sofia University “St. Kliment Ohridski”</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.28155v1) · [PDF 下载](https://arxiv.org/pdf/2608.28155v1) · **关键词** 金融专业考试推理, CFA与FRM基准, 上下文完整性, 检索增强生成, 选择性检索<br>


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

本文位于金融领域问答与推理基准研究交叉方向，关注模型能否在专业考试环境中同时运用金融知识、数量计算、规则选择、时间或合约约束以及职业判断。研究对象是覆盖特许金融分析师（CFA）三级考试和金融风险管理师（FRM）两部分考试的英文选择题；这些考试阶段由外部课程体系规定，因此可用于分析模型在不同专业层级上的能力，而不只是比较一个总体分数。与仅要求从报告中抽取答案或执行单一金融公式的任务不同，本文还区分题目证据是否在当前记录中完整可见，从而将“知识覆盖不足”与“基于给定材料的推理失败”分开考察。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**检索增强生成（RAG）**

RAG先从外部知识库中检索与问题相关的内容，再把这些内容提供给模型生成答案。本文用它测试结构化金融知识能否修复模型原本答错的题目，但也检验检索内容是否会干扰原本正确的答案。

</div>
<div class="concept-item" markdown="1">

**上下文完整性（context completeness）**

如果回答一道题所必需的文字、表格、图像、共享案例或展品都在当前记录中，则该题具有上下文完整性。它解决了将同一案例下的多个子问题拆开后，题目可能失去必要证据的问题。

</div>
<div class="concept-item" markdown="1">

**困难度分层与选择性调用**

本文不直接把CFA或FRM的考试阶段当作难度，而是依据固定的17个模型在题目上的表现，将题目划分为Easy、Medium和Hard。选择性调用指由一个门控器根据问题和模型的初始回答，决定是否额外运行检索模块，而不是对所有题目无条件检索。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

FinExam-10K包含10,198道英文金融专业选择题；每条记录至少包括题干、答案选项、标准答案和参考解题理由。任务输入是一道题及其可用的本地记录，模型输出一个选项答案；在需要时，系统还可输入检索到的金融函数或知识结构。数据被划分为公开的5,110道题和保留评测的5,088道题，并保留两种评测范围：包含完整整理题库的10,198题Full-Coverage Track，以及只保留必要证据在本地可见的7,625题Context-Complete Reasoning Track。后者是关于“依据给定记录进行推理”的主要分析对象。本文还假设可用的外部检索知识和初始模型回答能够支持一个门控决策，即判断何时调用FunctionGraph-RAG可能有益；门控器只用公开题目训练，以避免利用保留测试集信息。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$D$**

FinExam-10K的题目集合，规模为10,198。

</div>
<div class="notation-item" markdown="1">

**$D_{\mathrm{public}}$**

公开训练或开发用题目集合，包含5,110道题。

</div>
<div class="notation-item" markdown="1">

**$D_{\mathrm{held\text{-}out}}$**

保留评测题目集合，包含5,088道题。

</div>
<div class="notation-item" markdown="1">

**$s(x)\in\{\mathrm{Easy},\mathrm{Medium},\mathrm{Hard}\}$**

题目$x$的经验困难度标签，由固定的17个模型在该题上的表现划分，而非由考试阶段直接指定。

</div>

</div>

**直接相关的工作**

- **FinQA（Chen et al., 2021）**: FinQA主要研究基于财务报告的数值问答；本文认为这类基准不能覆盖CFA与FRM的完整专业考试结构，也不能在统一协议下系统分析外部知识干预对错误和正确答案的双重影响。
- **FinanceReasoning（Tang et al., 2025）**: 本文沿用其匹配的Function-RAG思路，并使用其相关性标注训练的FunctionGraph-RAG选择器进行迁移测试，但不在本文数据上重新适配；这使研究能够检验结构化金融检索在专业考试推理中的条件性收益。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

专业金融考试中的问题通常要求模型同时运用课程知识、定量计算、规则选择、时间或契约约束以及职业判断，而不是只进行定义检索或单步代入公式。现有评测难以在统一协议下覆盖 CFA Levels I–III 与 FRM Parts I–II，也难以判断模型的错误究竟来自知识缺失、推理失败，还是题目所需的共享材料没有随题目提供。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **报告或材料驱动的金融问答基准**：模型根据金融报告、文档或给定材料回答问题，主要测试从外部文本中定位和整合信息的能力。
- **金融数学、专业考试与认证题库评测**：模型在金融计算题、部分专业考试题或较宽泛的认证题集合上进行选择题评测，用总体准确率比较模型能力。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 已有数据集通常只覆盖金融问答、金融数学、部分专业考试或广义认证题库，缺少同时覆盖 CFA 五个层级阶段、并能区分不同阶段难度的统一基准。因此，研究者难以定位模型在完整专业课程结构中的具体失败位置。
- 既有评测没有在同一协议中系统区分题目覆盖范围与局部证据完整性，也缺少对检索干预的成对分析：检索是否修复原本错误的回答，以及是否反过来改坏原本正确的回答都难以分开测量。由此，外部知识带来的表面收益可能掩盖其干扰成本。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚未解决的缺口是：建立一个覆盖完整 CFA 与 FRM 结构、保留公共集与隐藏集、并区分 Full-Coverage Track 与 Context-Complete Reasoning Track 的统一评测协议，同时用匹配的干预实验回答检索或结构化金融知识在何种情况下真正改善推理，以及何时会破坏已有的正确判断。

</div>
<div markdown="1"><span>核心问题</span>

在专业金融考试推理中，外部检索和结构化函数知识能否稳定修复模型错误；如果静态调用会同时引入新的错误，能否仅根据题目与初始回答选择性地决定何时调用 FunctionGraph-RAG，从而获得可靠的净收益？

</div>
<div markdown="1"><span>作者直觉</span>

检索并非对每道题都有益：如果模型已经答对，新增证据可能引入冲突或促使模型改变正确答案；如果模型答错且题目需要特定公式、规则或计算函数，结构化知识则可能提供缺失的局部支持。因此，作者的切入点不是无条件增加检索，而是先获得 Direct 初始回答，再由一个使用题目和初始响应信号的 gate 判断是否启动 FunctionGraph-RAG；这种选择性调用有望保留检索的纠错价值，同时减少不必要的干预。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

FinExam-10K的方法不是训练一个新的语言模型，而是构建一个经过专家复核、分层发布并可进行受控检索干预的金融考试推理基准。输入是与CFA三级和FRM两部分对齐的英文选择题及其选项，数据经过筛选、规范化、去重、专家重标注和难度冻结后，形成$10,198$题的Full-Coverage Track与$7,625$题的Context-Complete Reasoning Track；随后对模型的Direct回答施加Function-RAG或FunctionGraph-RAG干预，并训练一个只依赖公共数据的门控器决定何时调用图结构检索。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 题目构建与专家重标注

依次进行解释过滤、格式规范化、全局去重和两阶段专家复核。四人金融资格团队检查题干、选项、标准答案、原始解释、考试阶段、学科标签和元数据；三名外部审阅者先分工复核，首席整理者再复核全部保留题目并执行结构、编号、答案映射和重复内容检查。

<div class="method-step__io" markdown="1">

**输入**：来自CFA对齐和FRM对齐备考材料的英文选择题、选项、答案及原始解释；官方CFA Institute和GARP考试内容被排除。<br>
**输出**：每题包含题干、选项、标准答案、参考解释、考试项目和阶段；若原始共享案例、表格、图片或图形能够忠实恢复，则一并恢复，否则标记为上下文不完整。

</div>

**直观理解**：这一步相当于先把不同来源的试题整理成统一试卷，再由专业教师逐题校对。上下文不完整不表示题目记录损坏，而是表示单独拿出该小题后，原材料中可能还有回答所需的共享信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 数据划分与难度标注

将标记为Mock或Practice Exam的$5,110$题公开，其余$5,088$题作为隐藏测试集。对每题计算按API模型组和本地模型组等权的平均正确率$s_i$，再按$s_i\geq 2/3$、$s_i\leq 1/3$及其余情况分别标记Easy、Hard和Medium；难度条件结果采用留一模型法，避免被评测模型参与自身测试集定义。

<div class="method-step__io" markdown="1">

**输入**：经过冻结的$10,198$道题，以及$17$个模型在每道题上的一次性正确性结果。<br>
**输出**：得到公开集、隐藏集、冻结的Easy/Medium/Hard标签，以及包含所有保留题目的Full-Coverage Track和仅保留答案所需局部记录完整题目的Context-Complete Reasoning Track。

</div>

**直观理解**：难度不是凭单个专家主观判断，而是观察一组模型能否答对：多数模型答对就是容易，多数答错就是困难。第二个评测轨道只问模型那些本地材料足够完整的题，因此更适合判断真正的基于给定记录推理能力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Direct基线推理与结构化检索干预

模型先在不添加外部结构化证据的Direct路径上回答；Function-RAG检索相关金融函数，FunctionGraph-RAG进一步保留函数之间的结构关系，并将检索结果用于重新作答。研究在固定预算、封闭世界条件下比较干预前后的答案转移，分别统计原本错误而被纠正的rescue和原本正确却被改错的harm。

<div class="method-step__io" markdown="1">

**输入**：试题及选项；在干预设置中还包括模型的Direct初始回答，以及从金融知识中检索出的函数或函数图结构。<br>
**输出**：每道题的Direct答案、检索增强答案、是否纠正错误、是否引入新错误，以及总体准确率变化。

</div>

**直观理解**：系统先让模型独立考试，再给它一组可能有用的公式或知识结构重答。这样不仅能看检索找回了多少错误，也能看错误资料或不恰当干预是否把原本正确的答案改坏。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 门控选择与隐藏集评估

训练一个Direct-conditioned gate，仅使用题目和初始回答相关特征，采用公共分区五折out-of-fold性能选择配置和阈值；在隐藏集上，门控器只在预测FunctionGraph-RAG有益时调用该分支，否则保留Direct答案，并比较门控前后的配对准确率。

<div class="method-step__io" markdown="1">

**输入**：题目特征和Direct初始响应；公共分区上的训练数据，以及冻结后的$5,088$道隐藏题。<br>
**输出**：门控调用比例、rescue与harm数量、准确率变化、显著性检验结果，以及上下文完整隐藏子集上的选择性检索效果。

</div>

**直观理解**：门控器像一个考场监考员：大多数题目不额外检索，只有它认为图结构知识可能有帮助时才调用昂贵分支。它的目标不是让每题都使用工具，而是减少检索带来的反效果。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 按访问组等权的题目正确率

$$
s_i=\frac{1}{2}\left(\frac{1}{10}\sum_{m\in\mathcal{M}_{\mathrm{API}}}c_{m,i}+\frac{1}{7}\sum_{m\in\mathcal{M}_{\mathrm{local}}}c_{m,i}\right)
$$

**符号说明**

- $s_i$：题目$i$的经验正确率，用于构建难度标签
- $c_{m,i}\in\{0,1\}$：模型$m$是否答对题目$i$；答对为$1$，答错为$0$
- $\mathcal{M}_{\mathrm{API}}$：十个API调用模型组成的模型集合
- $\mathcal{M}_{\mathrm{local}}$：七个本地评测模型组成的模型集合
- $m$：模型索引
- $i$：题目索引

<div class="equation-explanation" markdown="1">

**直观理解**：先分别计算API模型组和本地模型组在题目$i$上的平均正确率，再让两个组各占一半权重。这样模型数量较多的一组不会仅因成员更多而对难度判断拥有更大影响。<br>
**原文位置**：第3.3节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 经验难度分段规则

$$
d_i=\begin{cases}\textsc{Easy},&s_i\geq 2/3,\\\textsc{Hard},&s_i\leq 1/3,\\\textsc{Medium},&\text{otherwise}.\end{cases}
$$

**符号说明**

- $d_i$：题目$i$的经验难度标签
- $s_i$：公式(1)得到的题目经验正确率
- $\textsc{Easy}$：容易难度标签
- $\textsc{Medium}$：中等难度标签
- $\textsc{Hard}$：困难难度标签

<div class="equation-explanation" markdown="1">

**直观理解**：若至少三分之二的加权模型答对，题目被标为容易；若至多三分之一答对，标为困难；介于两者之间则为中等。这个规则把连续的模型表现转换成可解释的三档测试难度。<br>
**原文位置**：第3.3节，公式(2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：数据集构建和检索干预本身没有在所给章节中定义新的端到端语言模型训练目标。门控器使用公共分区的五折out-of-fold性能选择配置和阈值，但原文未明确报告其具体模型结构、损失函数或参数化目标；因此不能据此补写优化公式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 专家复核与版本化数据管线**

数据管线包含解释过滤、规范化、全局去重、两阶段专家重标注、可恢复证据补全和确定性结构检查；在复核完成后才冻结$17$模型响应矩阵和经验难度，数据按季度维护并设置公开与隐藏分区。

> 直观理解：该模块保证评测对象尽量是答案、格式和出处都清楚的题，而不是把模型错误误认为数据错误。隐藏集和季度版本也降低了反复刷题造成的测试污染。

**2. 经验难度与双评测轨道**

经验难度由API组$10$个模型和本地组$7$个模型的组内平均正确率等权计算；Full-Coverage Track用于完整覆盖、难度构建和排行榜，Context-Complete Reasoning Track用于从答案所需局部记录进行推理的主要证据。

> 直观理解：两个轨道回答不同问题：前者衡量完整考试题库上的总体表现，后者尽量排除缺失共享上下文造成的干扰。难度标签是模型群体行为形成的统一尺度，不等同于CFA或FRM的课程等级。

**3. FunctionGraph-RAG与Direct-conditioned gate**

FunctionGraph-RAG以结构化函数知识及其关联关系增强回答；门控器根据题目和Direct初始响应选择是否调用该分支，配置和阈值只用公共集的五折out-of-fold结果确定，再固定到隐藏集评测。

> 直观理解：普通检索像查找若干孤立公式，图检索还保留公式之间的联系；门控器负责判断这次查资料是否值得，从而避免无差别检索把正确答案改错。

**训练与推理**

数据阶段先完成专家复核和确定性检查，再冻结模型响应矩阵、难度标签及访问划分。推理阶段对每道题生成Direct答案，并可分别运行Function-RAG或FunctionGraph-RAG重答；在选择性设置中，门控器只依据题目和Direct响应决定是否调用FunctionGraph-RAG，最后按标准答案计分，并记录rescue、harm和配对显著性。门控器在公共集上完成五折out-of-fold选择后固定，隐藏集只用于最终评估。

**复现信息**

复现或公平解读时必须区分$10,198$题的Full-Coverage Track与$7,625$题的Context-Complete Reasoning Track，且不能把上下文不完整误解为核心字段缺失。还应保持$5,110$公开题与$5,088$隐藏题的划分、官方考试内容排除规则、两组模型等权难度计算、留一模型难度评测和固定预算封闭世界干预；FunctionGraph-RAG的具体检索库、函数保留算法、门控器架构及训练损失在所给章节中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Full-Coverage Track：共 10,198 道题，覆盖 CFA Level I–III 与 FRM Part I–II；所有 17 个冻结模型均在同一题集上作答，用于总体排行榜、难度划分和模型间比较。
- Context-Complete Reasoning Track：共 7,625 道带有完整局部上下文的题目，是论文关于“依据所提供记录进行推理”结论的主要依据；其中包含 372 道 context-complete Hard 题，用于检验困难是否仅由上下文缺失造成。
- Held-out intervention partition：公开发布的 5,110 道题用于训练调用门控，另有 5,088 道保留题用于门控评估；保留集与 Context-Complete Reasoning Track 的交集为 4,219 道。静态检索干预同时在两个 reasoning track 上报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

答案选项与专家标注答案一致的题目比例；不可解析或因长度截断而无法提取答案的输出按错误计入固定分母。 （越高越好，因为它直接衡量最终答题正确率。）

</div>
<div class="metric-item" markdown="1">

**Matched transition 与净变化 $\Delta$**

rescue 表示 Direct 错而干预后正确，harm 表示 Direct 正确而干预后错误；净变化定义为 $\Delta=100(R-H)/N$，其中 $R$ 为 rescue 数，$H$ 为 harm 数，$N$ 为评估题数。 （净变化越高越好；同时应关注 rescue 与 harm 的平衡，因为较大的救错数可能被破坏正确答案的 harm 抵消。）

</div>
<div class="metric-item" markdown="1">

**双侧精确 McNemar 检验的 $p$ 值**

在配对题目上，根据 $(R,H)$ 检验干预与 Direct 的正确率差异是否可靠，避免把同一题上的偶然分支变化误判为总体提升。 （通常以较小的 $p$ 值作为差异具有统计证据的信号，但它不表示提升幅度大小，也不替代实际准确率和净变化。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 17 个模型在 Full-Coverage Track 上的总体能力与困难题表现

<div class="result-value" markdown="1">

最佳总体准确率为 85.29%（Gemini-3.1-Pro），第二高为 84.75%（GPT-5.6-Sol）；最强开放权重推理模型为 75.76%，最强金融专用模型为 68.07%。但最佳模型在 Hard band 上只有 34.68%。

</div>

模型在容易题上表现很强，但总体高准确率掩盖了困难题上的显著失效。Hard 题中有大量题目缺少局部父级证据，因此该结果同时混合了信息覆盖不足与真实推理困难，不能单独证明模型的金融推理能力只有 34.68%。

<div class="result-source" markdown="1">

来源：第 5 节 RQ1；表 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Gemini-3.1-Pro and GPT-5.6-Sol lead overall at 85.29% and 84.75%, compared with 75.76% for the strongest open-weight reasoning model and 68.07% for the strongest finance-specialized model.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Context-Complete Hard 子集与跨模型共享失败

<div class="result-value" markdown="1">

在 372 道 context-complete Hard 题上，最佳准确率升至 54.57%，但只有 3 个模型超过 30.40% 的按题目加权机会基线。严格的全模型失败核心包含 188 道题，其中 47 道上下文完整；另有 41 道题被所有模型选为同一个错误选项。

</div>

补齐局部上下文可以明显改善困难题结果，但不能消除困难：即使证据完整，模型仍会在部分题目上共同犯错。这支持“上下文缺失放大问题，但不能完全解释问题”的解释；共同错误还表明某些失败可能来自共享的知识、判断或选项偏置，而非单个模型偶然失误。

<div class="result-source" markdown="1">

来源：第 5 节 RQ1；Difficulty and subject heterogeneity

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the 372-item context-complete Hard subset, the best score rises to 54.57%, yet only three models exceed its 30.40% item-weighted chance baseline.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 保留集上的 Direct-Conditioned Invocation Gate

<div class="result-value" markdown="1">

门控在 5,088 道 held-out 题上仅触发 FunctionGraph-RAG 7.9% 的题目，并将准确率从 70.83% 提高到 71.23%，对应 0.40 个百分点的绝对提升，且报告 $p=0.0446$。

</div>

门控的核心价值不是让所有题都检索，而是只对模型和 Direct 输出看起来可疑的少数题调用较昂贵的图检索，从而减少静态增强对已正确答案的破坏。该提升幅度较小且只在规定的保留集和固定协议下成立；它也不是延迟、token、成本或能耗的实测改善。

<div class="result-source" markdown="1">

来源：摘要；第 4.3 节 Direct-Conditioned Invocation Gate

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the 5,088 held-out items, the gate invokes FunctionGraph-RAG for 7.9% of questions and improves accuracy from 70.83% to 71.23% (p = .0446).

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

- Direct：不给模型提供外部函数知识的直接作答条件，是所有检索和门控方法的核心基线。
- Function-RAG：将 FinanceReasoning 中按推理链划分的函数知识迁移到本任务；GPT-4o PoT 使用 Contriever 召回前 30 个候选，DeepSeek-R1 CoT 使用 BM25 召回前 30 个候选，再由语言模型判断保留函数。
- FunctionGraph-RAG：在候选函数上进行图扩展并重新排序；GPT-4o PoT 使用共享文章标题和 $k=4$ 近邻边，DeepSeek-R1 CoT 使用共享归一化输入或输出量的函数图。它用于检验结构化函数关系是否比普通检索更能找到可修复错误的知识。
- FunctionGraph-RAG+Verifier：仅在 GPT-4o 的 Function-RAG 与 FunctionGraph-RAG 结果不一致时启用验证器；验证器读取题目、选项、两条程序或轨迹及其执行结果，并选择一个冻结分支答案，用于检验后生成验证能否降低检索造成的伤害。

**实验想回答的问题**

- RQ1：当前大型语言模型在 CFA 与 FRM 不同考试阶段、难度层级和学科上的表现如何，困难题主要源于上下文缺失、推理困难，还是模型间共享的系统性错误？
- RQ2：静态函数知识检索及其图扩展何时能够修复金融推理错误，何时会破坏原本正确的答案；基于题目和初始答案的调用门控能否减少这种副作用？

**实验实现**

17 个模型包括 10 个闭源专有模型、2 个开放权重推理模型和 5 个金融专用模型；所有模型回答同一组 10,198 道 Full-Coverage Track 题目，且不获得金标准标签或参考理由。干预实验固定题目、选项、骨干模型、解码配置、答案抽取和评分规则；DeepSeek-R1 使用 CoT，GPT-4o 使用 PoT，并在支持时采用确定性解码。FunctionGraph-RAG 的 GPT-4o 选择器是四特征线性成对排序器，使用 511 个可达的 FinanceReasoning Easy 与 Medium 标签训练，最多返回 3 个函数；DeepSeek-R1 选择器是 56 特征线性重排序器，使用 890 个可达 Easy、Medium 和 Hard 标签训练，返回前 10 个函数。两个选择器均未使用 FinExam-10K 的题目、答案、理由、正确性信号或模型输出。调用门控先运行 Direct，再依据题目和 Direct 完成调用构造的 27 维特征向量 $\mathbf{x}_i$ 决定是否运行 FunctionGraph-RAG；门控训练只使用 5,110 道公开题，采用五折分层交叉验证，最终使用逻辑回归正则化 $C=0.5$ 和阈值 $0.68$。保留集上的门控结果基于预计算分支输出离线评估，但实际策略可按触发后再执行图检索。报告的 $1+$ 触发率只是隐含的分支调用次数，不是延迟、token、金钱或能耗测量。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| DeepSeek-R1 CoT 与 GPT-4o PoT 上的静态检索和验证器对照 | DeepSeek-R1 CoT 下，Function-RAG 产生 505 次 rescue 和 538 次 harm，净变化为 -0.32 个百分点（$p=.322$）；FunctionGraph-RAG 产生 509 次 rescue 和 500 次 harm，净变化为 +0.09 个百分点（$p=.801$）。GPT-4o PoT 下，两种检索分别下降 1.27 和 1.30 个百分点；验证器减少 130 次 harm、牺牲 43 次 rescue，恢复 0.86 个百分点，但仍比 Direct 低 0.45 个百分点（$p=.158$）。 | 该对照同时测试普通函数检索、图扩展和事后验证是否能稳定提升答案。结果表明，检索确实会大幅改变答案，但平均收益不可靠；验证器可以减少部分破坏，却不能完全恢复 Direct 的性能。因此“检索能找到互补证据”不等于“检索后最终答案更准确”。 | 第 5 节 RQ2；表 4<br><span class="experiment-evidence">Under DeepSeek-R1 CoT, Function-RAG yields 505 rescues and 538 harms (-0.32 points, p = .322); FunctionGraph-RAG yields 509 and 500 (+0.09, p = .801).</span> |
| 按相关性判断结果分层的 FunctionGraph-RAG 干预 | 相关性判断器在 68.7% 的题目上不保留函数；在该层强行注入 3 个图函数使准确率下降 1.10 个百分点（$p=.0040$）。当判断器恰好保留 1 个相关函数时，图扩展使准确率提高 2.92 个百分点（$p=.0007$）；两项效应经 Benjamini–Hochberg 校正后仍显著。 | 该消融检验“是否需要外部函数知识”能否预测干预方向。结果支持相关性判断具有信息量：没有相关函数迹象时，强行注入会造成伤害；存在一个可信种子时，图扩展更可能找到有用的关联函数。不过这些分层同时改变了证据需求和注入函数数量，不能把效果完全归因于图拓扑本身；数量更大的其他分层没有可靠差异。 | 第 5 节 RQ2；表 5<br><span class="experiment-evidence">Forcing the three-function PoT graph in this stratum reduces accuracy by 1.10 points (p = .0040).</span> |

**定性案例**

- 论文报告的共享失败分析显示，在 369 道 context-complete Hard 题中，错误投票集中于同一个干扰项的中位占比为 0.923，而精确题目特定零分布的中位数为 0.605；观察集中度高于零分布的题目有 346 道，其中 148 道的所有错误投票都指向同一干扰项（单侧精确符号检验 $p=1.9\times10^{-75}$）。这不是单一具体题目的逐步案例，而是说明模型可能共享同一种误读或错误判断路径；同时，答案位置偏好具有切片依赖性，不能简单归结为全 benchmark 统一偏向某个选项。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：该工作提出金融专业考试大规模基准并评估检索增强对金融知识、计算和判断推理的作用。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`1e52b7cf1070b4f74f0afa1ad8b4ea3d5db3365745c7b98ec469d7da6f251c23`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
