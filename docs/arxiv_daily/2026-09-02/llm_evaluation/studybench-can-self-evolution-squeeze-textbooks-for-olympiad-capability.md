---
title: "[论文解读] StudyBench: Can Self-Evolution Squeeze Textbooks for Olympiad Capability?"
description: "[arXiv 2609.00787][LLM 评测] 原文未明确报告。"
arxiv_id: "2609.00787"
announcement_date: "2026-09-02"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-02T04:49:44.768140+00:00"
source_sha256: "359989dddb82ed6812de586d90e2fa8346f9d9674140b8a5d55a1b4044fe921e"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "大语言模型自进化"
  - "知识到能力转换"
  - "物理问题求解"
  - "能力迁移"
  - "受控基准测试"
  - "教材学习"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2609.00787</p>

# StudyBench: Can Self-Evolution Squeeze Textbooks for Olympiad Capability?

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-02</span>
<span><strong>作者</strong> Yinghao Chen, Zixi Chen, Bingxiang He, Ziqing Qiao, Huan-ang Gao, Yinuo Xu, Yuxin Zuo, Zeyuan Liu, Yuhao Zhan, Chaojun Xiao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Tsinghua University Zhejiang University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.00787v1) · [PDF 下载](https://arxiv.org/pdf/2609.00787v1) · **关键词** 大语言模型自进化, 知识到能力转换, 物理问题求解, 能力迁移, 受控基准测试, 教材学习<br>
**代码**: [https://github.com/thunlp/StudyBench](https://github.com/thunlp/StudyBench)

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

本文位于大语言模型自进化（self-evolution）评测领域。自进化方法旨在让模型在不依赖持续人工标注的情况下，从环境或给定训练材料中自主改进；关键不只是吸收材料中直接陈述的知识，还要把知识转化为能够解决新问题的可迁移问题求解能力。StudyBench将这一过程具体化为：在固定物理教材作为训练材料的条件下，测量方法把材料转换为能力的效率，并区分对教材内困难题目的吸收能力与对教材外奥赛题目的迁移能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**自进化**

指模型在部署或训练过程中利用自身生成的练习、反馈、记忆或提示等机制持续改进，而不是完全依赖新增的人工高质量数据。本文关注的是模型能否自主把给定材料转化为更强的解题能力。

</div>
<div class="concept-item" markdown="1">

**吸收与迁移**

吸收是学习并运用训练材料中已有的知识，例如解决教材中的困难习题；迁移是将这些知识和解题原则用于材料没有直接给出答案的、更困难的新题。后者更能检验模型是否获得了可泛化的能力，而非只记忆或复述材料。

</div>
<div class="concept-item" markdown="1">

**受控评测**

受控评测固定训练材料、测试题目和评测流程，使不同方法之间的分数差异主要归因于方法本身。本文还要求测试题既超出基座模型的可靠能力范围，又能借助教材材料解决，以分别保证能力缺口和可达性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

StudyBench在物理领域构造统一的自进化评测环境。输入是固定的11本经典物理教材及其三种材料形式：原始段落组成的Corpus、带答案的Instructions with Answer，以及不带答案的Instructions without Answer；方法还接收一个基座模型，并通过自身的学习、提示演化或其他自进化过程处理材料。输出是改进后的解题系统，其能力在两个固定测试集上评估：Application Set由教材中的困难章末题组成，用于测量吸收；Transfer Set由奥赛级理论题组成，用于测量超出教材直接题面范围的迁移。题目经过Qwen3-8B筛选：Application Set中的题目要求该模型不能可靠独立解决，Transfer Set中的题目要求该模型独立失败但在获得基于教材段落构造的指导后可以解决。这样，在同一基座模型内，比较不同方法的成绩即可更接近测量方法带来的能力增量，而不是基座模型、数据或题目差异造成的增量。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{Application\ Set}$**

应用集；由教材中的困难章末题构成，用于衡量模型是否吸收了训练材料。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{Transfer\ Set}$**

迁移集；由奥赛级物理理论题构成，用于衡量模型能否把教材知识转化为解决更陌生、更困难问题的能力。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{Par}@8$**

论文使用的主要成绩指标，表示在8次采样或尝试下的解题通过率；具体数值定义在所给章节中未进一步展开。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{Qwen3\text{-}8B}$**

用于筛选测试题和建立能力基准的8B规模Qwen3模型；论文将其视为中等能力模型，以便同时保留能力缺口和基于教材指导的可达性。

</div>

</div>

**直接相关的工作**

- **GEPA**: GEPA属于上下文层面的自进化方法，不修改模型权重，而是演化提示或上下文策略。StudyBench将其作为代表性方法进行比较，并检验其在固定教材上获得的应用能力能否迁移到更难的奥赛题。
- **SE-Bench**: SE-Bench与StudyBench都关注模型能否内化知识并形成能力，但StudyBench进一步固定源语料，同时设计能力缺口、可达性和指导上限，从而更直接地隔离自进化方法对教材可达能力的实际吸收程度。

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

StudyBench 的方法不是提出一个新的自进化算法，而是构造一个可控的物理学评测流程，用来测量模型能否把教材材料转化为独立解题能力。流程从 $11$ 本教材和 $6$ 个国际物理、天文学奥林匹克竞赛中抽取问题，经过能力筛选与可达性筛选，形成 Application Set 和 Transfer Set；随后让不同自进化方法仅使用固定训练材料进行训练或推理时演化，并用 $\mathrm{Par}@k$ 与 $\mathrm{Sub}@k$ 评估结果。

直观地说，Application Set 检查模型是否学会“教材刚教过的典型用法”，Transfer Set 检查模型能否把教材中的概念、公式和技巧重新组合，用于更难的竞赛题。方法还提供教材引导作为上限参照：如果模型在看到经过验证的教材知识路径后能解决问题，却在独立作答时失败，则说明问题主要在知识内化和迁移，而不是材料中没有答案。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 教材与竞赛材料抽取

先用 MinerU 将 PDF 转换为 Markdown，再通过确定性规则和大语言模型修复 OCR 错误，并针对不同书籍和竞赛版式编写抽取器。教材被组织为三个嵌套层次：原始段落 Corpus、无答案的 Instructions without Answer，以及包含标准答案的 Instructions with Answer；每道题还保存完整题面、子问题、参考解和 gold answer。

<div class="method-step__io" markdown="1">

**输入**：来自 $11$ 本物理教材、配套解答材料以及 $6$ 个国际物理和天文学奥林匹克竞赛历届理论题的 PDF 文件。<br>
**输出**：可供自进化方法使用的训练材料层，以及仅用于评测的教材题和竞赛题；每个子问题的答案被归入 $\mathrm{NV}$、$\mathrm{EX}$、$\mathrm{EQ}$、$\mathrm{TUP}$、$\mathrm{IN}$、$\mathrm{MC}$、$\mathrm{TF}$、$\mathrm{QL}$ 或 $\mathrm{ALT}$ 等类型。

</div>

**直观理解**：这一步把格式各异的书和试题整理成统一的数据记录，同时保留题目由多个小问组成的结构。三个训练层次适配不同方法：有的方法读连续教材段落，有的方法只能使用问题和答案对。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 能力筛选与 Application Set 构造

对每道父问题采样 $8$ 次；只有当没有任何一次完成该父问题的全部子问题时才视为失败。失败的教材题按子学科重新抽样，以避免某一学科主导 Application Set；另外保留少量恰好成功 $1$ 次的题，以免严格零成功规则使某些学科为空。

<div class="method-step__io" markdown="1">

**输入**：教材题和竞赛题候选池，以及 Qwen3-8B 的 $\mathrm{pass}@8$ 结果。<br>
**输出**：Application Set，即模型原本不能可靠解决、但来自教材章节且其先修材料在训练集中可获得的困难教材题。文中报告 Application Set 有 $88$ 个父问题，其中 $15$ 个来自恰好一次成功的特殊保留项，比例为 $17.05\%$；其余 $73$ 个以及全部 Transfer Set 父问题均为 $8$ 次尝试全部失败。

</div>

**直观理解**：筛选的目的不是挑选普通练习题，而是先找出基准模型确实不会稳定解决的题。Application Set 像考试中“刚学完这一章却仍然较难”的题，用来测量教材内容是否被吸收。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 教材可达性筛选与 Transfer Set 构造

对每个子问题依次执行五步：教师从 gold solution 中分解必要概念、定律、公式、技巧和假设；检索教材中的讲解与例题片段；按 $0$ 到 $3$ 的覆盖标准验证片段并复制原文证据；生成不泄露答案或关键计算的教材引导；最后在引导下让 Qwen3-8B 重试，至少一次解决父问题才被保留。检索采用 BM25 与稠密向量检索，并通过 reciprocal rank fusion 融合，且偏好领域内教材。

<div class="method-step__io" markdown="1">

**输入**：未被 Qwen3-8B 稳定解决的竞赛题、教材训练材料、DeepSeek V4 Pro 教师模型，以及待验证的知识点和参考解。<br>
**输出**：Transfer Set，即比教材题更难、但可以由教材材料重组解决的奥林匹克竞赛题；同时得到可审计的教材知识路径和不含答案的 guidance trace。用 GLM-5.1 重新生成引导后，$90$ 个父问题中有 $56$ 个仍可由 Qwen3-8B 解出，比例为 $62.22\%$；子问题层面为 $242/280=86.43\%$。

</div>

**直观理解**：这一步排除“教材根本没有提供足够信息”的竞赛题。只有当教师能指出相关教材片段，并且模型在不直接看到答案的引导下确实能解出，题目才进入 Transfer Set，因此独立作答失败更可能反映内化或迁移不足。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 固定协议下的自进化与评测

每种方法可使用训练材料的任意适合层次，但测试集、题目、验证器和采样协议保持不变。开放权重模型每个子问题生成 $k=8$ 个样本，Opus 4.7 因 API 成本使用 $k=1$；所有运行使用温度 $1.0$、$\mathrm{top\text{-}p}=0.95$、$\mathrm{top\text{-}k}=20$ 和 $32768$ token 上限，并在独立作答与教材引导两种条件下比较。

<div class="method-step__io" markdown="1">

**输入**：固定的训练材料、Application Set、Transfer Set、不同基座模型和自进化方法。<br>
**输出**：每个方法在两个测试集上的父问题准确率和子问题准确率，以及由 solo 与 guided 结果计算的 Guidance Gap；进一步记录中间检查点或推理时产物随累计 GPU 时间变化的 Application-Set 准确率，用于检测 Compute Plateau。

</div>

**直观理解**：所有方法面对同一批题和同一套评分规则，所以差异主要来自“如何学习和使用材料”。solo 测试模型能否独立解决，guided 测试教材提示能解锁多少能力；两者的差距就是没有被模型内化的能力。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 父问题准确率

$$
\mathrm{Par}@k=\frac{1}{|\mathcal{P}|}\sum_{p\in\mathcal{P}}\max_{1\le a\le k}\prod_{j=1}^{n_p}c_{p,j,a}
$$

**符号说明**

- $\mathcal{P}$：测试集中的父问题集合。
- $p$：一个父问题。
- $n_p$：父问题 $p$ 所包含的子问题数量。
- $k$：每个子问题生成的尝试次数。
- $a$：第 $a$ 次完整尝试，满足 $1\le a\le k$。
- $c_{p,j,a}\in\{0,1\}$：验证器对父问题 $p$ 的第 $j$ 个子问题在第 $a$ 次尝试中的正确性判断，$1$ 表示正确，$0$ 表示错误。

<div class="equation-explanation" markdown="1">

**直观理解**：对每个父问题，先在每一次尝试中把所有子问题的正确性相乘；只要某一次尝试全部答对，该父问题就计为正确。最后对所有父问题求平均，因此该指标衡量的是“能否完整解决一道题”，而不是把不同尝试中的答案拼在一起。<br>
**原文位置**：Section 2.2 Evaluation，Protocol

</div>

</div>

<div class="equation-block" markdown="1">

#### 子问题准确率

$$
\mathrm{Sub}@k=\frac{1}{\sum_{p\in\mathcal{P}}n_p}\sum_{p\in\mathcal{P}}\sum_{j=1}^{n_p}\max_{1\le a\le k}c_{p,j,a}
$$

**符号说明**

- $\sum_{p\in\mathcal{P}}n_p$：测试集中全部父问题所包含的子问题总数。
- $p,j,a,k$：分别表示父问题、其子问题索引、尝试索引和尝试总数。
- $c_{p,j,a}\in\{0,1\}$：验证器对相应子问题在相应尝试中的正确性判断。

<div class="equation-explanation" markdown="1">

**直观理解**：该指标对每个子问题单独计分，只要它在 $k$ 次尝试中有一次答对就算正确，再对全部子问题求平均。它比父问题指标更宽松，适合观察模型到底是完全不会，还是只能解决复杂题中的部分环节。<br>
**原文位置**：Section 2.2 Evaluation，Protocol

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确给出一个统一适用于所有自进化方法的训练损失或优化目标。StudyBench 是评测框架，允许每种方法按照自身范式使用 Corpus、Instructions with Answer 或 Instructions without Answer；因此具体目标由 Bonito、GEPA、ACE、Intuitor、R-Zero 等方法各自决定，而不是由 StudyBench 规定。框架层面的目标是比较材料到能力的转换效率，并通过 solo 与 guided 的差异量化 Guidance Gap。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 分层训练材料与结构化验证器**

教材内容被表示为 Corpus、Instructions without Answer 和 Instructions with Answer 三个嵌套层次；问题记录支持父问题与子问题层级，并为九类答案类型配置相应验证方式。父问题只有在同一次尝试中解决全部子问题时才算正确，避免把多个独立尝试拼接成一次完整解答。

> 直观理解：该模块同时解决“方法能看到什么”和“答案怎样判定”两个问题。尤其是父问题指标要求一次性完成所有小问，因而更接近真正的整题能力，而不是零散答对若干小问。

**2. Capability Filter 与 Naive Reachability Filter**

Capability Filter 用 Qwen3-8B 的 $\mathrm{pass}@8$ 排除已具备可靠能力的题；Naive Reachability Filter 则用教师分解、双通道检索、证据验证、无答案引导和重试构成可审计的可达性见证。检索证据只有覆盖分数 $2$ 或 $3$ 才计入，且引导经过确定性脱敏规则和教师复核的双重泄漏门控。

> 直观理解：前一个过滤器寻找基准模型真正不会稳定做的题，后一个过滤器确认题目不是“超出教材范围”。二者结合，才能把失败解释为学习方法问题，而不是题目太简单或材料不够。

**3. Solo/Guided 双条件与计算轨迹分析**

模型在不提供额外引导的 solo 条件和提供教材 grounded guidance 的 guided 条件下分别评测。方法还在 Qwen3-8B 上保存中间 checkpoint 或 inference-time artifact，绘制 Application-Set $\mathrm{Sub}@8$ 随累计 A800 GPU 时间的曲线，以判断性能是否在预算耗尽前饱和。

> 直观理解：guided 条件相当于告诉模型“应当从哪几章、用哪些公式、按什么顺序思考”，但不直接给答案。若增加训练时间后曲线仍然不升，说明继续投入计算量不能自动解决能力内化问题。

**训练与推理**

训练阶段，各自进化方法从固定教材材料的一个或多个层次中产生训练信号、更新模型或优化推理时程序；输入材料和最终测试题之间由 benchmark 固定隔离，Application Set 题目的题面与参考解还会从用于构建 Corpus 的原始 Markdown 中物理删除，以降低答案泄漏。推理阶段，每个 evolved model 在 Application Set 和 Transfer Set 上生成规定数量的答案样本，由答案类型对应的验证器判断子问题是否正确，并同时进行 solo 与 guided 评测；Open-weight 模型使用 $\mathrm{pass}@8$ 式的 $8$ 次采样，Opus 4.7 使用 $1$ 次采样。对于计算平台曲线，方法在中间 checkpoint 或推理时产物上重复评测，并把 Application-Set $\mathrm{Sub}@8$ 与累计 GPU 时间对应起来。

**复现信息**

复现实验时需要注意：所有运行统一使用温度 $1.0$、$\mathrm{top\text{-}p}=0.95$、$\mathrm{top\text{-}k}=20$ 和 $32768$ token 上限；不同基座模型复用同一测试项目和同一引导轨迹，但可达性过滤主要以 Qwen3-8B 为基准。教材 PDF 不公开，公开内容包括抽取后的 Instructions with Answer、Instructions without Answer 及由研究者合法持有的教材重建 Corpus 的脚本；需要 Corpus 的方法必须本地重建。计算轨迹的报告显示不同方法成本差异很大：Bonito 为 $8.12$ GPU hour，R-Zero 为 $614$ GPU hour；这些数值来自 Appendix I，原文证据为“Compute scales differ by nearly two orders of magnitude—from 8.12 GPU hour for Bonito to 614 GPU hour for R-Zero”。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 训练材料由 $11$ 本物理教材构成。它既作为 Bonito 等方法读取的原始语料，也用于构造有答案或无答案的训练指令。为防止测试答案直接泄漏，Application Set 中保留题目的题干、参考解答以及答案索引均从原始 Markdown 中删除，并进一步审计是否存在逐字残留。
- Application Set 由困难教材题组成，用于测试方法是否吸收了训练教材中的知识。测试题先经过以 Qwen3-8B 为基准的 Capability Filter：通常只有该模型在 $\mathrm{pass}@8$ 下零次成功的题目才进入测试集；另有 $15$ 道 Application 父题允许出现一次成功。节选未明确报告该集合的总题数及具体划分规模。
- Transfer Set 来自物理奥林匹克理论考试，且题目不出现在上述 $11$ 本教材中，用于测试教材知识能否迁移到比教材题更困难的问题。它同样经过 Capability Filter；Naive Reachability Filter 则确认这些题在提供教材依据的指导轨迹时可以被 Qwen3-8B 解出，从而把测试重点放在“可调用但尚未内化”的知识上。节选未明确报告该集合的总题数。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$\mathrm{Sub}@8$**

在最多八次采样下按子问题统计的通过率。多问问题会逐问评测：模型能看到共同题干、之前的子问题及其自身先前回答，但看不到标准解；某一问未给最终答案时会插入固定失败占位符并继续后续问题。该指标反映局部步骤或子任务被解出的比例。 （越高越好，因为它表示更多子问题在八次尝试范围内至少得到正确答案；但它不保证整道多问父题全部完成。）

</div>
<div class="metric-item" markdown="1">

**$\mathrm{Par}@8$**

在最多八次采样下按完整父题聚合的通过率，比子问题指标更严格，用于衡量模型是否能完成整道多部分问题。 （越高越好，因为它更接近完整解决一道综合物理题，而不是只答对其中若干部分。）

</div>
<div class="metric-item" markdown="1">

**Guidance Gap**

定义为 $\mathrm{Acc}_{\mathrm{guided}}-\mathrm{Acc}_{\mathrm{solo}}$，其中前者是在系统提示中加入教材依据指导轨迹后的 Transfer Set 准确率，后者是不提供该指导时的独立准确率；论文分别在 $\mathrm{Par}@8$ 与 $\mathrm{Sub}@8$ 上报告该差值。 （对训练后的独立能力而言越小越好：差距越小，说明原本只能由上下文指导激活的知识已更多地被训练内化；但若两种准确率都很低，小差距本身并不代表能力强。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen3-8B，Application Set，除 Bonito 外的自进化方法

<div class="result-value" markdown="1">

相对基础模型的 $\Delta\mathrm{Sub}@8$ 提升范围为 $+8.87$ 至 $+14.98$。

</div>

作者结果表明，多数方法确实能提高对困难教材题中局部子问题的处理能力，因此自进化并非完全没有吸收教材内容。但该结果只验证同分布或近教材问题上的吸收，不能单独证明能力已迁移到奥赛级问题。

<div class="result-source" markdown="1">

来源：第 4.1 节 The Guidance Gap（对 Table 2 的总结）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen3-8B, Application ΔSub@8 ranges from +8.87 to +14.98 for every method except Bonito, yet Transfer ΔSub@8 is at most +2.14 and Transfer Par@8 stays in the single digits.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen3-8B，Transfer Set，各自进化方法

<div class="result-value" markdown="1">

Transfer Set 上最好的 $\Delta\mathrm{Sub}@8$ 也不超过 $+2.14$。

</div>

与 Application Set 上最高达到两位数的子问题增益相比，迁移集增益明显受限。作者据此认为，改善教材题表现通常不会自动转化为更困难奥赛题上的独立迁移能力；不过节选未给出 Table 2 的完整方法级结果，因此无法判断各方法之间的显著性或稳定排名。

<div class="result-source" markdown="1">

来源：第 4.1 节 The Guidance Gap（对 Table 2 的总结）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen3-8B, Application ΔSub@8 ranges from +8.87 to +14.98 for every method except Bonito, yet Transfer ΔSub@8 is at most +2.14 and Transfer Par@8 stays in the single digits.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen3-8B，Transfer Set，完整父题指标

<div class="result-value" markdown="1">

各方法的 $\mathrm{Par}@8$ 均停留在个位数百分比。

</div>

即使允许最多八次采样，完整解决奥赛级多部分题目的成功率仍很低。这比 $\mathrm{Sub}@8$ 更直接地说明模型可能只获得零散步骤上的改善，尚未形成稳定的整题推理能力；该结果不能证明教材知识完全无效，只能说明现有训练方法未充分把可达知识转化为独立完成能力。

<div class="result-source" markdown="1">

来源：第 4.1 节 The Guidance Gap（对 Table 2 的总结）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen3-8B, Application ΔSub@8 ranges from +8.87 to +14.98 for every method except Bonito, yet Transfer ΔSub@8 is at most +2.14 and Transfer Par@8 stays in the single digits.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- Capability Filter 是相对于 Qwen3-8B 定义的，但同一题集也用于 Llama-3.2-3B-Instruct 与 Opus 4.7；因此“未被基础模型可靠解决”的难度条件并未针对另外两个模型分别校准，跨模型比较需谨慎解释。
- 所给节选缺少 Table 2、Table 4 及 Compute Plateau 分析的完整数据，无法核验方法级排名、方差、统计显著性、指导差距的具体大小以及增加计算后何时饱和；此外 Opus 4.7 只运行一次 $\mathrm{pass}@1$，与其他模型的重复采样协议并不完全对齐。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Bonito 代表直接消费原始 Corpus 的路线：先根据教材段落合成问答对，再对基础模型进行监督微调。它检验仅靠合成教材训练样本能否提高吸收与迁移能力。
- GRPO 代表使用“指令及标准答案”的监督强化学习参照：以带标签问题训练，并用金标准结果提供奖励。它用于判断明确答案监督能否比无标签自训练更有效地内化教材知识。
- TTRL 与 Intuitor 代表“只有指令、没有答案”的无标签强化学习路线，分别以多数投票一致性和策略自身的确定性作为奖励。二者检验模型能否依靠自身生成的反馈完成自进化，而不访问标准答案。
- R-Zero 代表完全不使用 StudyBench 训练材料的数据自由方法，通过 Challenger-Solver 自博弈及自一致性奖励提升能力。它提供对照，以判断教材材料本身是否带来超出通用自博弈的收益。另有 Naive Guidance 作为推理时可达性上界，但它不是训练方法。

**实验想回答的问题**

- RQ1：教材语料中可通过上下文指导调用的知识，有多少能被自进化方法内化为无需指导、可独立使用的迁移能力？实验以 Application Set 衡量教材知识吸收，以更难且不出现在教材中的 Transfer Set 衡量跨题型迁移，并通过 Guidance Gap 区分“模型在提示下能够使用”与“训练后能够独立使用”。
- RQ2：迁移能力的剩余差距是否只需延长自进化循环、增加计算量即可弥合，还是源于方法本身无法继续有效地把材料转化为能力？所给节选提出该问题，但没有提供 Compute Plateau 的完整曲线、预算或数值结果。

**实验实现**

测试题先用开启 thinking mode 的 Qwen3-8B 过滤，随后在 Llama-3.2-3B-Instruct、Qwen3-8B 和通过 Claude Code 使用的 Opus 4.7 上评测同一批题。各方法从官方代码库复现，只做适配训练材料与评测协议所需的最小修改；开放权重方法运行于单个 $8\times$ NVIDIA A800-80GB 节点。一般实验使用独立采样种子重复三次并报告均值与标准差，Opus 4.7 仅报告一次 $\mathrm{pass}@1$。判分器以 UG-Physics 的规则判分器为基础，覆盖九种答案类型，并在排行榜评测中把规则判分失败的题交给 DeepSeek-V4-Flash-0731 二次判断；当判分器用于强化学习奖励时，只开放规则部分，以降低奖励投机风险。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Qwen3-8B 的 Transfer Set 指导消融：比较 solo 推理与注入教材依据指导轨迹的 guided 推理 | 由于 Naive Reachability Filter 的构造条件，Qwen3-8B 的 guided 分数为 $100$；消融以 guided 与 solo 准确率之差衡量尚未被训练内化的可达能力。 | 该消融保持模型与测试题不变，只改变推理时是否提供教材依据的指导轨迹，因此主要隔离“缺少相关知识”与“模型无法自主调用相关知识”这两种原因。guided 达到 $100$ 是筛选流程保证的可达性上界，而不是训练方法取得的泛化成绩，也不能直接用于宣称模型已独立掌握全部 Transfer Set。 | Table 4 表注及第 4.1 节 Guidance ablation<br><span class="experiment-evidence">Qwen3-8B’s guided scores are 100 by construction of that filter.</span> |
| 五种自进化方法在 Qwen3-8B 上重新加入相同指导轨迹 | 论文分别以 $\mathrm{Par}@8$ 和 $\mathrm{Sub}@8$ 比较 $\mathrm{Acc}_{\mathrm{guided}}$ 与 $\mathrm{Acc}_{\mathrm{solo}}$；所给节选未包含 Table 4 的具体方法级数值。 | 这一设计测试训练后模型还需要多少外部教材提示：若某方法的 solo 分数接近 guided 分数，说明它较充分地内化了指导中可用的知识；若差距大，则说明训练主要改善了表面吸收，关键知识仍依赖推理时提示。由于表格行缺失，不能从节选判断哪一种方法的差距最小。 | 第 4.1 节 Guidance ablation，Table 4<br><span class="experiment-evidence">Both quantities are reported for Par@8 and Sub@8.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：StudyBench benchmarks how effectively LLM self-evolution methods acquire and transfer textbook knowledge to difficult physics reasoning problems.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`359989dddb82ed6812de586d90e2fa8346f9d9674140b8a5d55a1b4044fe921e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
