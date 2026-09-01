---
title: "[论文解读] ScienceArena: Benchmarking LLMs on Latest Scientific Olympiad Competitions"
description: "[arXiv 2608.30517][LLM 评测] ScienceArena旨在用近期公开的物理、化学与生物奥林匹克竞赛题、官方过程评分细则和奖牌选手校准的自动评分，较真实地衡量大语言模型的开放式、多步骤科学推理能力。"
arxiv_id: "2608.30517"
announcement_date: "2026-09-01"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:30:11.438508+00:00"
source_sha256: "99e47c6a40d3972d923361bc479f0c84860048dd0399a71bc139a5ecff5891dd"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "大型语言模型"
  - "科学推理"
  - "科学奥林匹克竞赛"
  - "开放式多步骤解题"
  - "过程给分"
  - "LLM-as-judge"
  - "专家校准"
  - "多模态评测"
  - "数据污染"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.30517</p>

# ScienceArena: Benchmarking LLMs on Latest Scientific Olympiad Competitions

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Guangxiang Zhao, Qilong Shi, Xusen Xiao, Wenpu Liu, Yaoming Li, Linfeng Hao, Shuyang Hou, Zijian Guo, Xinrui Zhang, Yuntian Zhao, Zhengyang Wang, Wenrui Liu, Yuhan Wu, Tong Yang, Lin Sun, Xiangzheng Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Tsinghua University；Affiliation: The University of Hong Kong；Affiliation: Peking University 🖂 Correspondence；Affiliation: Peking University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30517v1) · [PDF 下载](https://arxiv.org/pdf/2608.30517v1) · **关键词** 大型语言模型, 科学推理, 科学奥林匹克竞赛, 开放式多步骤解题, 过程给分, LLM-as-judge, 专家校准, 多模态评测, 数据污染<br>
**项目页**: [https://science-arena.onrender.com/](https://science-arena.onrender.com/)

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

ScienceArena旨在用近期公开的物理、化学与生物奥林匹克竞赛题、官方过程评分细则和奖牌选手校准的自动评分，较真实地衡量大语言模型的开放式、多步骤科学推理能力。

**不用术语来说**：现有科学能力测试常让模型选择选项或填写短答案，难以判断它是否真正理解图像、建立了正确的科学模型并完成了前后一致的长推导；而奥林匹克竞赛虽能检验这些能力，却包含公式、图表、化学结构和按步骤给分的规则，既难以整理成模型可读的数据，也不能仅靠答案匹配来评分。若每次比较新模型都由竞赛专家逐题批改，成本又难以承受。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建ScienceArena：将2023—2026年十三个物理、化学和生物竞赛年度的公开试题、图示、官方答案、详细解法及评分细则结构化，并由奥林匹克奖牌获得者审核，使近期竞赛材料能够用于统一的开放式科学推理评测。
- 建立经专家校准的“LLM作为裁判”评分流程，并比较整题一次作答与按小问交错作答两种协议，从而在保留过程分和人类奖牌标准参照的同时，将评测扩展到十四个近期模型。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大型语言模型科学推理评测领域，关注模型能否解决物理、化学和生物奥林匹克竞赛中的开放式、多步骤问题。传统选择题或短答案基准主要检查最终结论，难以衡量长推导、图表与化学结构理解、跨步骤一致性以及部分正确时应得的过程分；同时，常用题库日趋饱和并可能进入模型训练数据，使高分未必代表真实推理能力。科学奥赛试题由领域专家编写，赛后通常公开题目、官方解答、评分细则和奖牌线，因此既能提供高难度任务，也能用人类竞赛成绩解释模型水平；但其 PDF 中含公式、图像、表格和分子结构，且评分依赖专家对中间步骤的判断，必须先解决可靠数字化与可扩展评分问题。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**过程给分评分细则**

评分不只核对最终答案，而是依据官方 rubric 检查建模、关键推导、中间结论和最终结果，并为正确步骤分配部分分。它比精确匹配更适合奥赛长答案，但也更依赖结构化规则和专业判断。

</div>
<div class="concept-item" markdown="1">

**LLM-as-judge**

使用另一个大型语言模型按照给定答案与评分细则评阅模型解答，并输出分项得分。本文并不默认这种评分可靠，而是用奥赛奖牌获得者的人工评分作为真值，对裁判系统进行校准。

</div>
<div class="concept-item" markdown="1">

**数据污染与基准饱和**

数据污染指评测题或其解答可能出现在模型训练数据中；基准饱和指大量强模型已在固定题库上接近满分。两者都会削弱分数对未知科学推理能力的区分力，因此本文强调具有明确发布日期的近期公开竞赛。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

ScienceArena 将 2023—2026 年十三个物理、化学和生物竞赛年度的数据组织为统一评测套件。输入是由官方 PDF 转换并经奥赛奖牌获得者审核的结构化题目，其中可包含多小问、公式、图表、示意图或化学结构，同时提供官方答案、详细解法和逐步评分细则；被测模型需要生成开放式、多步骤解答。输出不是简单的对错标签，而是依据官方 rubric 汇总的分项与总分，并可参照官方奖牌线或优胜者成绩解释模型所处的人类水平。评测假设公开材料及其发布日期可核查，数字化内容忠实于原考试，并通过 IPhO/IChO 2025 上五个模型的存档答案及奖牌获得者评分，检验自动裁判能否近似专家评分；主评测采用顺序呈现子问题并保留先前上下文的交错式求解设置。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

一个结构化奥赛题目或其中的子问题输入；原文未规定统一符号，此处仅用于说明任务。

</div>
<div class="notation-item" markdown="1">

**$y$**

被测语言模型针对题目生成的开放式、多步骤解答；原文未规定统一符号。

</div>
<div class="notation-item" markdown="1">

**$R$**

随题提供的官方过程给分评分细则，用于判断各关键步骤应得分数；原文未规定统一符号。

</div>
<div class="notation-item" markdown="1">

**$S(y;R)$**

依据评分细则对模型解答得到的分项或汇总分数；原文未给出形式化评分公式。

</div>

</div>

**直接相关的工作**

- **OlympicArena、OlympiadBench 与 MathArena**: 这些工作同样使用奥赛或竞赛问题评估高难度推理；ScienceArena 的区别是集中于近期公开的物理、化学和生物竞赛，并结合官方过程给分 rubric、奖牌参照线和奖牌获得者审核。
- **HiPhO／PhyArena**: 这是与本文最接近的物理奥赛评测方向，使用最新物理奥赛和官方奖牌阈值；ScienceArena 将范围扩展到三门科学学科，并建立统一的结构化数据处理与专家校准评分协议。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

前沿大语言模型的科学推理能力越来越难被可靠区分：常用基准可能已趋于饱和，训练数据污染也会使高分无法证明模型进行了真实推理。更接近科学解题实际的题目通常是开放式、多步骤且包含图像或结构表示的，但这种答案可能部分正确，需要依据明确评分点分配过程分；因此，评测不仅要找到足够新且有挑战性的题目，还要解决材料数字化和可扩展评分的问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **短答案、多项选择及通用偏好式评测**：短答案或选择题通过答案匹配计算正确率；Chatbot Arena、Arena-Hard一类通用竞技场则主要让人类或裁判模型比较回答的整体偏好。这些方式易于规模化，但评分信号通常不是针对可核验的科学推导过程。
- **近期竞赛或专家题目驱动的高难度基准**：OlympicArena、OlympiadBench、MathArena以及HiPhO/PhyArena等工作采用竞赛题、近期题源或专家编写问题，以降低陈旧基准饱和的影响并提高推理难度；其中部分工作还使用官方答案或奖牌门槛作为参照。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 短答案、选择题和总体偏好评分无法充分检验长推导、图表与化学结构理解、多步骤一致性，也难以区分完全错误与完成了关键中间步骤的部分正确答案，因而可能高估表面流畅或最终答案碰巧正确的模型。
- 已有竞赛型评测往往只覆盖单一学科，或缺少同时结合近期发布日期、官方过程评分细则、奖牌选手审核与专家校准自动评分的统一协议；若直接依赖专家逐题批改，持续评估新模型的成本又不现实。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一个跨物理、化学和生物、以近期公开奥林匹克竞赛为题源的统一评测框架：它既要忠实保留复杂图示、官方解答和逐步给分规则，又要用人类竞赛专家验证数据与评分有效性，并把这种可靠评分扩展到大量模型和长篇开放式答案。

</div>
<div markdown="1"><span>核心问题</span>

能否将近期科学奥林匹克竞赛可靠地转化为大语言模型可读、可按官方过程分评分的基准，并通过奖牌选手校准的自动裁判与合适的作答协议，可信地区分模型在跨学科、视觉依赖和长程多步骤科学推理上的能力边界？

</div>
<div markdown="1"><span>作者直觉</span>

奥林匹克试题本身由领域专家设计，公开后通常附有标准解答、细化评分点和奖牌分数线，因此同时提供了高难度任务、可核验的推理依据和可解释的人类能力参照。将原始PDF严格结构化并由奖牌选手审核，可减少公式、图形和结构转换造成的失真；再用专家评分校准裁判模型，便可让自动评分模仿“检查每个关键步骤并给部分分”的人工批改，而按小问交错作答则有望降低模型一次规划整道长题的负担。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ScienceArena的方法不是训练一个新的求解模型，而是建立一条可审计的科学奥赛评测流水线：先把公开发布的物理、化学和生物竞赛材料数字化为保留题目层级、图像信息、官方解答及逐项评分细则的结构化数据；再让被测大语言模型按统一协议作答；最后用经奥赛奖牌选手标定的LLM-as-judge逐评分点给出部分分，并通过格式、分数边界和总分一致性检查得到考试级总分。其关键假设是：开放式奥赛题不能仅按最终答案判对错，正确建模、推导或中间结果即使未得到正确终值也应获得过程分，而只有表面正确却缺少依据的答案可能只能得到少量分。
直观地说，这套框架同时处理了“把复杂试卷可靠录入”“让模型以适合连续子题的方式答题”和“按照真实奥赛规则批改”三个问题。人工专家并未被完全替代：奖牌选手负责审计数据并提供评分真值，自动裁判只是在官方解答和评分细则均可用、且数字化正确的前提下，作为可扩展的专家评分代理。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 竞赛材料采集与数字化

策展人员先收集官方公开材料，再将PDF页面渲染为图像，并使用OCR或多模态模型解析公式、曲线图、分子结构、实验装置和答案图像。解析结果被规范化为题干、官方答案、详细解答、评分细则、最高分、发布日期和来源溯源等字段。

<div class="method-step__io" markdown="1">

**输入**：十三项公开科学奥赛的官方题目PDF、插图、答案、详细解答、评分方案、发布日期及来源信息，学科覆盖物理、化学和生物。<br>
**输出**：包含文本、视觉上下文、官方解答、逐项评分规则和来源元数据的初步结构化竞赛条目。

</div>

**直观理解**：这一步类似把版式复杂的纸质试卷录入数据库，但不能只复制文字，还必须保证题图、公式、答案与评分点彼此正确对应。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 专家审计与交错式数据组织

对应学科的奥赛奖牌选手检查材料是否完整、图文是否对齐、官方答案是否忠实、各评分点之和是否等于题目总分；随后保留原试卷的多级题目结构，将每个子题组织为一个相互关联的轮次。最终导出统一的交错式数据集，其中每行对应一个子题轮次，同时保留它与前序子题和整道大题的关系。

<div class="method-step__io" markdown="1">

**输入**：自动解析后的竞赛条目、原始页面以及官方评分材料。<br>
**输出**：经专家核验、按子题轮次组织且具有完整审计轨迹的ScienceArena评测数据。

</div>

**直观理解**：可以把一道含多个连续小问的大题看成一段对话：每个小问单独存放，但仍知道自己属于哪道大题、依赖哪些前文以及值多少分。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按统一协议生成候选答案

开放式物理和化学主评测采用交错式求解：模型依次回答$Q_t$，先前回答持续保留在上下文中；对照协议则让模型一次看到完整问题并提交一份整体解答。若回答为空、不完整或缺少可评分的具体内容，系统最多重试五次并保留首个有效回答；全部失败时写入失败标记，后续轮次仍能看到该标记，但系统不给纠错提示。

<div class="method-step__io" markdown="1">

**输入**：静态化题目内容、相关视觉证据和被测模型；对于第$t$个交错轮次，还包括截至该轮的题目上下文$Q_{1..t}$与模型此前的答案$A_{1..t-1}$。<br>
**输出**：与各子题一一对应、保留跨轮推导历史的候选回答序列；客观题则产生可直接与标准答案匹配的回答。

</div>

**直观理解**：交错式协议相当于让学生按小问逐题作答，并把草稿历史留在桌面上，而不是要求其一次写完一整道很长的大题。它改变的是交互和上下文组织方式，不是为模型增加新的推理算法。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 专家标定的自动评分与汇总

LLM裁判模拟严格的奥赛阅卷员，按评分细则分配部分分，并输出含总分、最高分、子项分、证据、扣分理由和置信度的JSON；后处理检查JSON合法性、LaTeX转义、分数边界、评分上限和加总一致性，再将轮次分数聚合为试卷总分。IBO等客观键控项目不调用生成式裁判，而是确定性评分；2026年四项竞赛使用更严格的密封实现，无效裁判输出会被拒绝并重试，而不是直接截断到合法范围。

<div class="method-step__io" markdown="1">

**输入**：每个非客观子题的静态化题目、官方答案、详细解答、评分细则、最高分和候选回答；必要时还直接输入原题及解答页面PNG。<br>
**输出**：可追溯到具体轮次、评分条目和答案证据的子项分、题目分及整场考试总分。

</div>

**直观理解**：自动裁判不是只问“答案对不对”，而是像阅卷老师一样逐条核对得分点；每一分都要能追溯到评分标准和考生回答中的依据。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。ScienceArena是数据集与评测框架，原文没有提出需要训练或参数优化的新模型，也没有给出中心训练损失函数；被测大语言模型以既有能力进行推理，裁判模型则通过提示词、结构化输入输出、专家评分校准和确定性验证规则构成评分系统，而非在本文中通过一个新目标函数训练。所谓“校准”主要是将裁判对存档模型答案的评分与奥赛奖牌选手真值进行比较，并据此完善输入包、子项分约束和边缘情况处理，不能等同于梯度更新。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 专家审计的结构化试题表示**

每个多部分问题被保存为相互链接的轮次，并同时携带$question\_text$、$official\_answer$、$official\_detailed\_solution$、$official\_rubric$、$max\_score$、$release\_date$及来源溯源字段。系统还保留解析文本、图像派生描述、原始页面和审计记录，以显式呈现物理中的图表读取与符号传递、化学中的反应式与立体结构、以及生物中的长文本和图示等不同信息需求。

> 直观理解：这个模块决定评测材料是否可信。若题图错配、化学结构丢失或评分点总和错误，即使求解模型和裁判都很强，最终分数也没有解释价值。

**2. 经奖牌选手标定的LLM-as-judge**

系统使用五个模型在IPhO 2025与IChO 2025上的存档回答建立人工评分锚点，由专家共同阅卷并解决评分细则层面的分歧；候选裁判随后与这些人工总分及题目级评分比较。裁判被设计为完整管线而非单一提示词：输入包显式包含官方解答、专家理由和评分条目标识，输出强制采用结构化子项分，并针对化学表面相似答案、极小分值子题和分数越界等边缘情况执行固定后处理。

> 直观理解：裁判模型不能因为“看起来像标准答案”就随意给分，因此作者先用真正的奥赛阅卷结果校准它，再要求它说明每个得分和扣分来自哪里。这里的自动评分只在官方解答、评分标准及数字化内容可靠时成立，不能视为脱离参考材料的通用科学正确性判定器。

**3. 交错式求解协议**

若一题包含$m$个相关子题，交错式协议在第$t$轮向模型提供$Q_{1..t}$和$A_{1..t-1}$，仅要求生成当前答案$A_t$，并对$t=1,\ldots,m$重复；一次性协议则提供全部$Q_{1..m}$并生成完整解答。失败回答不会由系统纠正，且误差延续得分仅在模型明确给出可识别的中间结果时才能按评分规则授予。

> 直观理解：许多奥赛后续小问会沿用前一问的变量或数值。逐小问交互能减少一次生成过长答案造成的遗漏，同时仍保留真实考试中的错误传播，因为系统不会告诉模型前一问是否做错。

**训练与推理**

整个方法主要发生在推理与评测阶段。首先冻结已审计的题目表示，避免不同模型运行时得到不同版本的题干或视觉描述。对于开放式物理、化学题，主实验按交错协议遍历子题：第$t$轮组合当前及此前题目$Q_{1..t}$、既有回答$A_{1..t-1}$和所需视觉内容，调用被测模型生成$A_t$；无效回答最多重试五次，成功后进入下一轮，连续失败则记录不可回答标记。对客观题，直接保存模型选择并与答案键匹配。
评分时，非客观轮次被封装成固定的裁判数据包，包含题目、官方答案、详细解答、逐项评分细则、最高分和候选回答。裁判输出每个标准对应的有界子分及文本证据，验证器检查输出格式、子分范围和算术总和，最后聚合为题目与整场考试分数；客观题采用确定性规则。裁判可靠性不是由待测模型的主实验结果反向决定，而是预先用IPhO 2025和IChO 2025的存档回答及专家评分进行核验，从而避免为了匹配新模型表现而临时调整评分器。

**复现信息**

复现时最重要的不是常规采样参数，而是固定数据版本、求解协议和评分路径。题目侧应保留原始层级、发布日期、来源、图像或静态化视觉证据、官方解答、逐项评分细则和最高分；“静态化”指将题目侧内容冻结为文本表示，并纳入文本路线所需的视觉证据。所有模型应在同一题目表示和上下文规则下运行，且一次性与交错式结果不可混为同一协议。
裁判输出至少应包含$total\_score$、$max\_score$、$sub\_scores$、证据、扣分理由和置信度，并保存从总分到轮次、评分条目及证据的完整映射。常规路径会修复常见LaTeX转义错误、限制不可能分数并核对最高分；用于2026年四项竞赛的密封路径固定采用Gemini 3.5 Flash裁判，向其提供带来源标签的官方材料、精确评分条目标识与上限，并在可用时直接提供题目和解答页PNG。该路径要求有界小数子分、证据引文和算术一致的总分；无效输出被拒绝，保存一次初始调用及最多六次重试的连续日志，求解器明确返回“无答案”哨兵时则确定性计零且不调用裁判。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ScienceArena 十三项竞赛套件：涵盖物理、化学和生物，包括 IPhO、IChO、IBO、APhO、EuPhO、USNCO、CPhO、CChO、INChO、NBPhO 和 USAPhO 等；表 6 给出各竞赛的发布日期、满分和模型得分。其作用是提供跨学科、开放式、多步骤的主评测集。
- 国际竞赛人类参考集：表 5 汇总 IPhO 2025、IChO 2025 和 IBO 2023 的官方理论或客观题排名分数，用于把模型分数映射为金、银、铜牌等相对水平，而不是把模型表现解释为绝对意义上的科学能力。
- 图像依赖子问题与重复调用集：模态消融选取 IPhO 2025、IChO 2025 和 IBO 2023 各四道图像依赖子题，由十二个具备视觉能力的模型路由在原图、忠实文字描述和无视觉信息三种条件下重复评测；稳定性实验则在 IPhO 和 IChO 2026 上重复完整求解与评分调用。其作用分别是检验视觉输入价值和 API 输出稳定性。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**竞赛原始分数与归一化分数**

原始分数按各竞赛官方满分计算；加权平均则把每项分数归一化到 $0$ 至 $100$ 后取平均，用于跨满分不同的竞赛比较。 （越高越好，因为表示获得了更多官方评分点；但跨竞赛的加权平均只表示套件内总体表现，不代表所有学科或所有题型同等困难。）

</div>
<div class="metric-item" markdown="1">

**人类奖牌等效线**

将模型在 IPhO 2025、IChO 2025 和 IBO 2023 上的分数与官方冠军、金牌、银牌和铜牌参考分数比较，用于描述模型达到的竞赛等级。 （分数越高、超过的奖牌线越高越好；它是相对参照，不证明模型在未知题、真实考场或严格防污染条件下具有人类竞赛者的完整能力。）

</div>
<div class="metric-item" markdown="1">

**稳定性与评分一致性指标**

重复调用中使用均值、样本标准差和取值范围衡量模型输出的波动；固定答案的多评分器实验使用跨评分器一致率、归一化 MAE 和 Pearson 相关衡量评分稳定性。 （均值和一致率、相关系数越高越好；标准差、范围和 MAE 越低越好，因为它们分别表示表现更稳定、评分误差更小。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 十三项竞赛上的总体与奖牌线比较

<div class="result-value" markdown="1">

Gemini 3.1 Pro 的加权平均为 $88.7$（表 6 排名第 1），在 IPhO 2025 得到 $29.45/30$，在 IChO 2025 得到 $48.95/60$，在 IBO 2023 得到 $431.00/453$。它超过了 IPhO 金牌参考线 $23.4$ 和 IBO 人类冠军参考分数 $395.4$，但低于 IChO 人类冠军分数 $57.1$。

</div>

作者据此认为，顶尖模型在物理、化学和生物的部分公开奥赛中已经达到金牌等效水平，但不同学科并未饱和：物理和生物出现超过人类冠军参考线的结果，而最困难的 IChO 结构题仍存在明显差距。这里的“金牌等效”只是按公开评分线进行标注，不证明模型具备稳定、无污染且可迁移到新题的奥赛推理能力。

<div class="result-source" markdown="1">

来源：第 3.2 节；表 5、表 6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On IPhO 2025, Gemini 3.1 Pro reaches 29.45/30, slightly above the best human theory score in the official ranking.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 学科和题型诊断

<div class="result-value" markdown="1">

化学中，物理化学得分率为 $78.4\%$，立体化学为 $34.7\%$；要求结构图的化学题得分率为 $64.5\%$，不要求结构图的题为 $74.1\%$；视觉依赖化学题为 $63.3\%$，非视觉化学题为 $83.1\%$。物理的视觉与非视觉得分率分别为 $77.6\%$ 和 $79.7\%$。IBO 中生物化学为 $91.4\%$，实验数据解释为 $64.3\%$。

</div>

这些切片表明，模型在化学中往往能说出正确反应机制，却不能可靠地把机制绑定到具体底物、取代基位置、立体关系和最终结构图；物理的主要问题则更像是早期选错物理模型或变量定义，错误随后传播到多个小问。生物总体分数较高，但涉及同一实验图中多条陈述的交叉核对时仍会失分。切片统计是模型—题目评分实例，不是完全独立题目；小样本切片只能作探索性证据。

<div class="result-source" markdown="1">

来源：第 3.5 节；图 5 及附录 B

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The strongest pattern is that chemistry is bottlenecked by structure fidelity.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 重复 API 调用的端到端稳定性

<div class="result-value" markdown="1">

表 8 中，Gemini 3.5 Flash 在 IPhO 2026 的均值、标准差和范围为 $28.75/30$、$1.00$ 和 $2.00$，在 IChO 2026 为 $53.73/60$、$0.92$ 和 $1.77$；GPT-5.5 的对应 IPhO 范围为 $0.00$、IChO 范围为 $1.50$；Claude Opus 4.7 的范围分别为 $2.50/30$ 和 $4.95/60$。

</div>

在固定路由、输入包、提示词、评分标准和评分器配置后，三个模型都保持在相近的高分区间，说明这些 API 评测结果并非每次调用都会完全失控。不过不同提供商和考试的波动不同，Claude 的 IChO 波动最大；因此单次调用分数仍不应被视为精确的确定值。

<div class="result-source" markdown="1">

来源：第 3.3 节；表 8

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Claude Opus 4.7 has the largest variation, yet its maximum span is 2.50/30 on IPhO and 4.95/60 on IChO.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 基准材料来自公开竞赛，存在潜在数据污染和训练暴露问题；文中的发布日期屏障只是描述性边界，不能证明模型未见过题目。作者仅把 Gemini 2.5 Pro 的部分发布时间关系称为狭窄的 release-based holdout，并明确不把发布时间当作无污染证明。
- 开放式物理和化学题依赖校准后的 LLM-as-judge，尽管其与专家分数有较高相关性，校准样本仍有限且同属 Gemini 家族；不同输入模态与 API 路由在主表中存在耦合，四个 2026 年列因此是能力评估而非严格的模态对照。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 人类官方参考分数：使用国际竞赛的冠军、金牌、银牌和铜牌线作为外部能力参照；这是有意义的比较，因为它把模型得分放在真实竞赛评分尺度上，但不等同于模型参加了同一场比赛。
- 五个赛前发布模型的归档表现：Gemini 2.5 Pro、GPT-5、GLM 4.5、DeepSeek V3.1 和 Qwen3 235B；这些结果用于校准评分器并提供较早模型的对照，而非严格的数据污染控制。
- 十四个近期模型的跨基准比较：包括 Gemini、GPT、Claude、Doubao、Qwen、DeepSeek、MiniMax、GLM 和 Xiaomi 等模型家族；该比较测试不同模型家族在统一竞赛套件上的总体能力和学科差异。
- 三种输入模态条件：原生图像、经审核的忠实文字描述和无视觉信息；它们不是模型能力基线，而是用于隔离视觉证据对图像依赖题表现的因果性对照。

**实验想回答的问题**

- 在十三个科学奥林匹克竞赛基准上，十四个近期大语言模型能否达到与人类奖牌线相当的分数；不同学科和竞赛结构下的能力是否一致？
- 模型表现的主要瓶颈究竟是科学知识不足，还是视觉证据绑定、结构保真、全局问题控制和多步答案一致性不足？

**实验实现**

主评测包含十四个近期模型和十三项竞赛。九个基准列采用统一的纯文本交错协议；四个 2026 年竞赛列依据具体 API 路由能力输入数据，八个视觉路由接收原始题目文本和原题页 PNG，六个纯文本路由接收经过审核、且不含答案、解答或评分标准的静态文字化题目。开放式物理和化学题由第 2.2 节校准的 LLM-as-judge 评分，IBO 则由原始客观答案键和专用运行器确定性评分。主表报告所有 $182$ 个模型—基准单元，四个 2026 年竞赛列贡献 $56$ 个完整单元且不进行插补。跨竞赛排名使用归一化加权平均。模态消融中，物理和化学单元取三个评分器均值，IBO 使用客观答案键；每个条件重复四次。稳定性章节的文字称“three times”，但表 8 说明每个精确模型路由进行五次独立端到端调用，故重复次数应以表 8 的表注为准。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 受控视觉模态消融：原生图像、忠实文字描述与无视觉信息 | 原生图像的平均归一化分数为 $72.75\%$，忠实文字描述为 $71.73\%$，无视觉信息为 $49.85\%$。原生图像相对无视觉信息高 $22.90$ 个百分点，配对 bootstrap $95\%$ 置信区间为 $[20.02,25.77]$；原生图像相对文字描述的差异为 $1.02$ 个百分点，$95\%$ 置信区间为 $[-1.20,3.27]$。 | 该实验把路由能力与输入模态分开：同一批视觉能力路由分别面对原图、质量受控的文字描述和完全没有视觉信息的题目。结果支持视觉证据对刻意设计的图像依赖题确实重要；高质量文字描述可以恢复大部分原图收益，但总体上尚不能证明与原生像素输入等价。化学中原图相对文字描述的优势达到 $5.01$ 个百分点，说明结构敏感的化学图像更难被文字完全替代。 | 第 3.4 节；表 9；附录表 11<br><span class="experiment-evidence">Native images outperform no visual information by 22.90 percentage points (paired-bootstrap 95% CI [20.02, 25.77]), showing that visual evidence materially affects performance on this deliberately image-dependent panel.</span> |
| 评分器稳定性与专家校准 | 两个 Gemini 评分器在 $525$ 条共享专家评分记录上的归一化 MAE 为 $0.093$，Pearson 相关为 $0.907$；冻结答案的六个评分器之间，三次重复的逐题一致率范围为 $90.11\%$ 至 $96.70\%$。 | 该实验不测试模型解题能力，而是测试开放式物理、化学答案的自动评分是否足够接近奖牌选手的人工评分。较高相关性和较高逐题一致率支持其用于大规模评测，但校准数据来自 IPhO/IChO 的有限专家记录，且文中明确指出这是同一模型家族内部的狭窄诊断，不能推出所有评分器、所有学科或所有答案形式都同样可靠。 | 第 3.6 节；第 3.7 节及图 2<br><span class="experiment-evidence">A deterministic replay of 1,050 stored rows from the two calibrated Gemini judges gives interjudge normalized MAE 0.093 and Pearson correlation 0.907 across 525 shared expert rows; this remains a narrow same-family diagnostic.</span> |

**定性案例**

- IChO 2025 Q2.2a–b 展示了最典型的结构绑定失败：Gemini 3.5 Flash 能流畅解释 Zimmerman–Traxler 过渡态和 Evans aldol 反应，却把具体烯醇负离子误当作通用甲基酮/丙酸酯情形，导致取代基位置和产物结构错误；在受影响小问中，评分器对过渡态定位给出 $0/15$、对产物给出 $0/4$。该案例说明，模型会调用正确的反应模板，但若未保持真实底物、辅助基和立体化学约束，语言上的化学流畅性不能转化为竞赛评分点。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces an expert-audited benchmark and calibrated judging protocol for evaluating LLM scientific reasoning on recent Olympiad problems.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`99e47c6a40d3972d923361bc479f0c84860048dd0399a71bc139a5ecff5891dd`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
