---
title: "[论文解读] STRIVE: Probing Reasoning Limits in Graded Plausibility Generation and Evaluation"
description: "[arXiv 2608.04567][LLM Reasoning] STRIVE研究如何让大语言模型生成并评估严格配对的四条件事件句集合，使句子仅在一个事件角色上变化，同时覆盖“合理或不合理”与“容易或困难判断”的组合。"
arxiv_id: "2608.04567"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T07:05:18.769928+00:00"
source_sha256: "4215562818f928966eebf74edbdb066783a940388175d6c0074497d9077f16f6"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "事件知识"
  - "事件合理性"
  - "心理语言学刺激"
  - "事件框架"
  - "槽位控制"
  - "分级合理性"
  - "大语言模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.04567</p>

# STRIVE: Probing Reasoning Limits in Graded Plausibility Generation and Evaluation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Bhiman Kumar Baghel, Anna Chrabaszcz, Tessa Warren, Michael Walsh Dickey, Haley C. Dresang, Xiang Lorraine Li</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> University of Pittsburgh；University of Wisconsin–Madison</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04567v1) · [PDF 下载](https://arxiv.org/pdf/2608.04567v1) · **关键词** 事件知识, 事件合理性, 心理语言学刺激, 事件框架, 槽位控制, 分级合理性, 大语言模型<br>


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

STRIVE研究如何让大语言模型生成并评估严格配对的四条件事件句集合，使句子仅在一个事件角色上变化，同时覆盖“合理或不合理”与“容易或困难判断”的组合。

**不用术语来说**：心理语言学实验需要比较一组几乎相同、但常识合理程度不同的句子，例如保持动作、对象、工具和地点不变，只替换动作执行者。研究者还希望句子既包含一眼可判的情况，也包含接近合理性边界、需要仔细判断的情况。人工制作这类材料不仅耗时，还必须同时保证合理性等级正确、其他内容严格一致，因此很难规模化。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出STRIVE，将共享事件框架构造、单槽位四条件生成、约束检查和基于评估反馈的修订整合为一个流程，用于自动化构造受控的事件合理性实验材料。
- 把问题明确为合理性类别、分类难度、事件框架和槽位选择的联合设计，并检验显式全局推理、候选槽位值比较及评估器引导修订是否能提高材料质量。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于心理语言学与自然语言处理的交叉领域，研究“事件知识”如何支撑人对句子所描述情境的合理性判断。事件知识可概括为对“谁以何种方式、使用什么、在何处对谁做了什么”的常识性预期；心理语言学实验通常通过句子或图像刺激测量人类对完整事件的可接受程度。为了把观察到的判断差异归因于合理性，而不是词汇、句法或场景变化，实验刺激必须严格匹配：同一组句子共享动词及大部分事件角色，只改变一个目标槽位。本文进一步采用“合理性类别 × 分类难度”的 $2\times2$ 设计，使刺激同时覆盖明确合理、边界附近合理、边界附近不合理和明确不合理四种操作性条件；这些条件是实验设计目标，并非自然形成的语义类别或经过校准的概率区间。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**事件知识（event knowledge）**

人们关于现实事件中各类参与者、动作、工具和地点通常如何组合的知识，例如什么主体通常能够执行某个动作。它既包括词义关联，也依赖普通世界知识。

</div>
<div class="concept-item" markdown="1">

**事件框架与槽位（event frame and slot）**

事件框架把一个事件表示为动词及其若干语义角色，如施事、受事、工具和地点；每个角色对应一个可填入具体实体的槽位。固定其他槽位而仅替换目标槽位，可以把组内合理性差异局部化到该角色。

</div>
<div class="concept-item" markdown="1">

**分级合理性与分类难度（graded plausibility and classification difficulty）**

事件合理性是完整情境与事件知识及普通常识相符合的程度，不只是简单的真假判断。本文用“容易”表示预期远离合理性边界，用“困难”表示预期接近边界，但不把它们解释为固定分数范围。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个英语根动词 $v$，系统首先建立共享事件框架，再生成一个由四条句子组成的匹配刺激集 $S_v$。四条句子分别对应“合理且容易”“合理且困难”“不合理且困难”“不合理且容易”，组内只允许目标事件角色发生变化，其余角色、动词形式及场景属性保持一致；主要实验改变施事槽位，论文另行考察受事槽位变化。一个有效输出必须同时满足两类约束：每条句子的实际合理性应符合其预定条件，整个集合还必须保持非目标槽位一致。该设置面向心理语言学刺激构造，目标是自动完成初始生成和质量评估以减少人工劳动，而不是用模型判断替代最终的人类验证；尤其是合理性边界附近的项目仍可能产生显著的人际分歧。本文实验限于英语，因此不能直接假设框架或判断标准可无验证地迁移到其他语言。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$v$**

作为生成起点的根动词。

</div>
<div class="notation-item" markdown="1">

**$S_v$**

围绕根动词 $v$ 构造的四条件匹配刺激集。

</div>
<div class="notation-item" markdown="1">

**$r_t$**

在同一刺激集中允许改变的目标事件角色或目标槽位；主要实验中为施事。

</div>
<div class="notation-item" markdown="1">

**$r_{-t}$**

除目标槽位之外必须在四条刺激间保持固定的全部事件角色。

</div>

</div>

**直接相关的工作**

- **ADEPT（Emami et al., 2021）**: ADEPT通过给名词添加形容词构造句子对，并用五类标签描述形容词造成的合理性变化；其标签表达的是一对句子之间的变化，而不是共享事件框架下、仅改变一个槽位的四条件匹配设计。因此，它不能直接满足本文对组内角色控制和四级实验刺激的联合要求。
- **Cross-Refine（Wang et al., 2025）**: Cross-Refine使用独立批评模型提供反馈并修订生成结果，为STRIVE的评估器引导式优化提供直接方法背景。STRIVE将这种思想用于结构化刺激集，同时检查单条刺激的条件归属与整组刺激的非目标角色一致性，而不只评价或修订一个孤立输出。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

事件知识研究通过合理性判断考察人类如何利用“谁对谁做了什么、使用什么工具、发生在哪里”等常识处理语言。为了将实验差异归因于合理性，刺激句必须构成严格匹配的集合：每组共享同一事件框架，只改变代理者或受事者等一个目标槽位，并覆盖合理或不合理、易判或难判四种目标条件。这样的多层级受控材料依赖人工逐句设计和核查，成本高，也限制了心理语言学及语言与认知障碍研究扩展到更多动词和场景。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **人工构造受控刺激材料**：研究者围绕同一动词手工设计匹配句，固定非目标事件属性，只替换一个角色，并凭专业判断控制各句的合理性及判断难度。
- **大语言模型的一次性结构化生成与推理式生成**：一次性生成方法根据提示直接输出完整刺激集合；更强的推理式方法要求模型先进行全局规划并给出逐句理由，或先产生多个目标槽位候选，再为四种条件选择填充值。论文将前者具体化为Reasoning Base，将候选比较具体化为Reason-to-Verbalize。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 人工方法需要同时协调四个合理性条件、共享事件框架和单槽位变化，制作与检查负担较重，难以高效扩展到大量动词；这正是作者引入自然语言处理生成流程的直接原因。
- 单次模型生成容易局部满足某个条件，却无法保证整组材料同时满足“目标合理性正确”和“所有非目标槽位固定”两类约束；摘要报告基线提示下GPT-5.1仅有16.7%的集合达到高质量，说明一般生成能力不足以稳定完成这种集合级约束任务。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚缺少一种端到端框架，能够针对同一根动词联合生成和评估四种分级合理性条件，并在发现合理性标签错误或共享框架被破坏后，利用独立评估反馈自动修订。更细致地说，尚不清楚模型是否必须进行集合级全局推理、比较多个槽位候选并接受评估器反馈，才能可靠处理接近合理性边界的困难样例；同时也缺少对模型判断能否达到人类标注者一致性水平的验证。

</div>
<div markdown="1"><span>核心问题</span>

在共享事件框架和单槽位变化的严格约束下，大语言模型能否可靠地生成并评估覆盖四种预定条件的事件刺激集合；全局推理、多个候选比较和评估器引导修订分别能带来多大帮助，而接近合理性边界的样例是否仍需要人类介入？

</div>
<div markdown="1"><span>作者直觉</span>

四个句子不是彼此独立的文本，而是一套需要整体协调的实验材料，因此先规划共享场景和四个槽位填充值，有助于避免逐句生成造成的无关属性漂移；让模型比较多个候选，可以更有意识地拉开四个条件与合理性边界的距离。独立评估器再从“条件是否匹配”和“非目标内容是否固定”两个方面指出失败原因，生成器便可定向修改问题句，而不必推倒整组材料。该思路适合修正常见约束错误，但边界案例本身缺少清晰、统一的人类答案，所以自动推理再充分也不能消除由主观分歧造成的不确定性。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

STRIVE 是一个由生成器和评估器组成的、基于结构化提示的事件刺激构造框架。输入根动词 $v$ 后，生成器先确定共享场景，即动词变形 $v^{\prime}$、受事、工具和地点，再仅替换施事，得到四个句子组成的集合 $\mathcal{S}=\{s_{\mathrm{PE}},s_{\mathrm{PH}},s_{\mathrm{IH}},s_{\mathrm{IE}}\}$；四种条件分别表示“合理且易判断”（PE）、“合理但难判断”（PH）、“不合理但难判断”（IH）和“不合理且易判断”（IE）。评估器随后检查每个施事的等级归属、施事之间的视觉可区分性，以及共享场景能否同时容纳完整梯度；在 R2R 与 R2VR 中，评估结果还会被压缩为局部诊断，用于多轮修正。
直观地说，STRIVE 先搭建一个保持不变的“舞台”，再让四个不同角色依次进入同一舞台，使事件从明显合理逐步过渡到明显不合理。因为句子间只有角色发生变化，后续心理语言学实验更容易把参与者判断的差异归因于施事与事件的匹配程度，而不是词汇、句法、受事或地点等混杂因素。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 共享场景设计

生成器联合选择动词变形 $v^{\prime}$、受事、工具和地点，形成固定的五槽事件模板，并检查该场景原则上能否容纳 PE、PH、IH、IE 四级合理性。这里把四个固定槽位整体称为场景，后续只允许施事变化。

<div class="method-step__io" markdown="1">

**输入**：一个根动词 $v$。<br>
**输出**：共享事件框架 $\langle[\mathrm{Agent}],v^{\prime},\mathrm{Patient},\mathrm{Instrument},\mathrm{Location}\rangle$。

</div>

**直观理解**：这一步相当于先固定舞台、动作、物体和道具。若舞台本身过窄，例如其中只有高度专业化的人才能执行动作，就很难找到位于合理性边界附近的角色。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分级施事生成与选择

RB 直接为每个条件选择一个施事；R2V 则先生成覆盖完整合理性范围的候选池，再按照互不重叠的启发式分数区间选择候选：PE 为 $[0.80,1.00]$、PH 为 $[0.40,0.65]$、IH 为 $[0.15,0.35]$、IE 为 $[0.00,0.05]$。这些数值只用于组织生成，不是模型概率、真实事件概率或经校准的人类判断预测。

<div class="method-step__io" markdown="1">

**输入**：共享场景，以及 PE、PH、IH、IE 四种目标条件。<br>
**输出**：四个带目标等级和选择理由的施事候选。

</div>

**直观理解**：RB 是直接挑选四个角色，R2V 则先在一把人为划分的尺子上广泛找候选，再从每个区段选一个。区段之间留出空隙，是为了减少相邻等级的角色混在一起。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 视觉预筛、句子组合与生成器自检

生成器依据职业服装等可见线索进行文本层面的视觉可识别性预筛，将施事分别填入同一场景，随后执行覆盖既有约束的 16 项 YES/NO 检查；任何 NO 均须在输出前修正。该检查只预测角色在白色背景照片中是否容易识别，并不实际生成或验证图像。

<div class="method-step__io" markdown="1">

**输入**：共享场景和四个已选施事。<br>
**输出**：包含场景、四个施事、等级理由和四个完整句子的结构化刺激集 $\mathcal{S}$。

</div>

**直观理解**：四个角色被放入完全相同的句子骨架，并接受一份交付前检查表。视觉预筛关注的是角色将来能否仅凭外观区分，而不是当前文本中的职业名称是否不同。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 评估器多维诊断

评估器分别执行施事等级的对抗式判定、视觉可区分性判定和场景评估。对每个等级，它提出施事应上移或下移一级的最强反论证；对 IH 还审计其与 PE 在职业领域、场景、工具、受事类型和身体动作上的重叠，若少于五项中的两项，则把 IH 重新归为 IE。

<div class="method-step__io" markdown="1">

**输入**：根动词 $v$ 与四句候选刺激集 $\mathcal{S}$。<br>
**输出**：逐条件的 CORRECT/INCORRECT 结论、视觉结论，以及 AGENT_FIXABLE 或 NEEDS_REDESIGN 的场景诊断。

</div>

**直观理解**：评估器不只问“看起来对不对”，还主动尝试证明角色被放错了等级。它同时判断问题是某个角色选错了，还是整个舞台无法形成四级梯度，从而为下一步提供可执行的修改方向。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 四条件刺激集合

$$
\mathcal{S}=\{s_{\mathrm{PE}},\,s_{\mathrm{PH}},\,s_{\mathrm{IH}},\,s_{\mathrm{IE}}\}
$$

**符号说明**

- $\mathcal{S}$：由同一根动词和共享场景构成的四句受控事件刺激集合。
- $s_{\mathrm{PE}}$：合理且容易被判断为合理的事件句。
- $s_{\mathrm{PH}}$：合理但接近分类边界、较难判断的事件句。
- $s_{\mathrm{IH}}$：不合理但接近分类边界、较难判断的事件句。
- $s_{\mathrm{IE}}$：不合理且容易被判断为不合理的事件句。

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定一次生成的基本输出不是孤立句子，而是一组覆盖合理性类别与判断难度交叉组合的四句刺激。四句必须联合成立，因此任何一个条件失败都会削弱整组材料的实验可用性。<br>
**原文位置**：第 3.1 节，公式（1）前的集合定义；亦见图 2

</div>

</div>

<div class="equation-block" markdown="1">

#### 固定五槽事件模板

$$
s=\langle\textit{Agent},\,v^{\prime},\,\textit{Patient},\,\textit{Instrument},\,\textit{Location}\rangle
$$

**符号说明**

- $s$：一个完整的事件句或事件刺激。
- $\textit{Agent}$：动作执行者，也是本文四个条件之间唯一允许变化的槽位。
- $v^{\prime}$：由输入根动词选择出的具体屈折形式。
- $\textit{Patient}$：动作所作用的对象，即受事。
- $\textit{Instrument}$：执行动作所使用的工具。
- $\textit{Location}$：事件发生的地点。

<div class="equation-explanation" markdown="1">

**直观理解**：该模板把事件拆成五个可控部分，并固定除施事外的所有部分。于是组内合理性变化可主要归因于“谁在做这件事”，降低词汇和句法差异造成的混杂。<br>
**原文位置**：第 3.1 节，公式（1）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。原文将 STRIVE 描述为由独立结构化提示构成的生成与评估框架，没有报告参数训练、微调、损失函数或梯度优化；R2V 的 $[0,1]$ 数值也明确只是组织候选生成的启发式分数，而非需要拟合或校准的概率。这里的“优化”发生在推理时：评估器定位错误，修正器按错误范围更新当前刺激集。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 分解式生成器与四种变体**

生成器将任务依次分解为场景设计、施事选择、视觉区分预筛、句子组合和 16 项验证，并在结构化输出前使用自由形式推理草稿。RB 是单次前向生成，R2V 加入分数区间引导的候选采样，R2R 为 RB 加入评估器驱动的迭代修正，R2VR 则以 R2V 结果初始化同一修正过程。

> 直观理解：直接一次性要求模型满足所有约束时，很难定位究竟哪一步出错；分解流程把复杂任务变成相互衔接的小决策。四种变体用于区分“显式分级推理”和“反馈修正”分别带来的作用。

**2. 对抗式分级与 IH 重叠审计**

评估器对每个施事构造其应位于相邻更高等级和更低等级的最强理由，仅当两种反论证都明显弱于当前归属时才判为 CORRECT。IH 还必须与 PE 在五类语义维度中至少重叠两类，并通过去掉共享动词后关联仍存在的负向测试；二取五阈值来自提示开发时对种子样例的检查，是可调操作规则而非普适语义定律。

> 直观理解：边界条件最容易被表面上似乎合理的解释蒙混过去，因此评估器要主动替相邻等级“辩护”。IH 既要总体不合理，又不能与正常场景毫无联系，否则它只是明显荒谬的 IE。

**3. 分层错误路由**

评估器将可替换单个施事的问题标为 AGENT_FIXABLE，将找不到可行替代施事、因而无法支撑完整梯度的场景标为 NEEDS_REDESIGN。修正器据此分别执行局部施事替换或全局场景重建，并保留简化的反馈历史。

> 直观理解：框架先判断故障发生在零件还是底座：角色放错等级属于零件问题，场景天然无法产生四级差异则属于底座问题。错误路由决定修改范围，是迭代能够稳定推进的关键。

**训练与推理**

框架只有推理流程。对于 RB，模型从根动词 $v$ 出发，在一次结构化提示调用中完成场景设计、四级施事选择、视觉预筛、组合和自检；R2V 在相同流程中增加候选池和分数区间约束。对于 R2R 与 R2VR，先分别取得 RB 或 R2V 的初始结果，再将结果交给评估器；评估器输出逐条件、视觉和场景诊断，修正器据此替换失败施事或重建场景，并可将修正结果再次送评。原文节选未明确给出最大迭代轮数、停止条件或具体模型解码参数。

**复现信息**

复现时需要保持三项关键设计。第一，四句必须共用相同的 $v^{\prime}$、受事、工具和地点，只改变施事；第二，R2V 使用四个互不重叠且带缓冲区的启发式范围，文中采用 PE $[0.80,1.00]$、PH $[0.40,0.65]$、IH $[0.15,0.35]$、IE $[0.00,0.05]$，但作者说明具体边界属于设计选择；第三，迭代反馈应是实例级紧凑诊断，而非重复完整规则，并应区分施事级与场景级失败。生成器和评估器提示由心理语言学与人工智能研究者协作开发，并依据 catch、break、erase 三个随机动词上的失败模式修订；提示与输出模式位于附录 B 至 E。视觉检查只是基于文本线索的预筛，不能被解释为真实图像质量或图像可辨识度验证。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 60 个可图示英语动词，来自三个 verb-naming assessments：Cho-Reyes and Thompson (2012)、Masterson (2000) 和 Swinburn et al. (2004)。原始数据只提供词根，STRIVE 为每个动词生成词形及事件角色值；动词还需能够填入模板中的 agent、patient、instrument 和 location 四种角色。该数据集用于大规模比较生成方法和模型。
- 主生成实验产生的 stimulus sets：每个集合包含四个条件对应的句子，即 PE、PH、IH 和 IE。其核心控制是保持共享事件框架及其他事件特征不变，只改变一个事件槽位，以形成从高 plausibility、低难度到低 plausibility、高难度的梯度。该集合用于计算 GOLD 等级和比较生成质量。
- 人类标注子集包含 30 个 stimulus sets、120 个句子，覆盖 GOLD、SILVER 和 FAIL tiers。8 名心理语言学本科研究者为每个句子进行 plausibility 判断，共产生 960 条句子级评分，并对每个四-agent 集合评估视觉可区分性。该子集用于建立人类一致性基准和验证 evaluator。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**GOLD rate**

GOLD rate 是被 evaluator 判定为同时通过四个条件的 plausibility 检查、scene 检查和 visual-distinctiveness 检查的事件集合比例。条件等级由 Table 1 的层级规则映射为 GOLD、SILVER、BRONZE 或 FAIL，其中 plausibility 是前置 gate。 （越高越好，因为它表示更多生成集合可以直接进入后续人工、图像和领域专家验证流程；但它不是已经通过真实图片验证的最终可用率。）

</div>
<div class="metric-item" markdown="1">

**unweighted Cohen's $\kappa$**

Cohen’s $\kappa$ 衡量两个标注者在分类任务上的一致性，并扣除随机一致的部分。研究将其用于四级 plausibility 分类、AgentID 的三分类视觉任务和 PairDist 的二分类视觉任务；人类-人类一致性是 evaluator 的参照基准。 （越高越好，表示 evaluator 与人类或人类之间的分类一致性更强；对于四级分类，unweighted $\kappa$ 将不同类别错误视为同等严重。）

</div>
<div class="metric-item" markdown="1">

**Friedman 检验与相邻条件 Wilcoxon 检验**

Friedman 检验测试同一批人类评分在 PE、PH、IH、IE 四个条件之间是否总体不同；Holm 校正后的 Wilcoxon signed-rank tests 进一步测试相邻条件边界是否可区分。 （这些是显著性检验而非单调性能指标；较小的 $p$ 值表示条件间差异更难由随机波动解释，但不直接表示生成质量更高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 迭代 refinement 对生成质量的影响：比较 RB、R2V 与 R2R、R2VR，并分别使用 GPT evaluator 和 Qwen evaluator。

<div class="result-value" markdown="1">

GPT evaluator 下，两个闭源生成器的 RB 和 R2V GOLD rate 为 11%–13%，R2R 和 R2VR 为 74%–77%；Qwen evaluator 下，单次方法在六个生成器上为 36%–37%，迭代方法为 65%–68%。在 plausibility gate 单独通过率上，GPT-5.1 的 RB 到 R2R 从 51.7% 升至 86.7%，Sonnet 4.6 从 43.3% 升至 89.1%。

</div>

作者据此认为 iteration 是最核心的质量杠杆，因为提升已经出现在后续 scene 与 visual checks 之前。结果支持 evaluator-guided refinement 能修正初始事件，但不能简单把 GPT 与 Qwen 的 GOLD rate 横向当作同一尺度：两位 evaluator 对闭源生成器的单次与迭代输出给出了不同幅度的判断，而且开源生成器的 R2R/R2VR 使用 Qwen 自评反馈，存在自评偏差。

<div class="result-source" markdown="1">

来源：§5.1 Generation Quality

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under the GPT judge, RB and R2V reach 11–13% GOLD while R2R and R2VR reach 74–77% on the two closed-source generators.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 人类 plausibility 判断与 evaluator 判断的一致性，以及四个目标条件是否真的形成可分离梯度。

<div class="result-value" markdown="1">

人类观察均值从 PE 的 1.21、PH 的 1.89、IH 的 2.58 递增到 IE 的 3.86；Friedman 检验得到 $\chi^2(3)=76.5$、$p<10^{-15}$，所有相邻边界在 Holm 校正后均为 $p<0.001$。GPT-5.1 high reasoning evaluator 与人类的一致性为 $\kappa=0.530$，人类-人类基线为 $\kappa=0.529$，差值为 $+0.001$，并通过 $\delta\leq0.05$ 的 AAT non-inferiority 检验。

</div>

这些结果表明，人类确实能区分四种设计条件，而不是只区分极端的 PE 与 IE；不过 IH 仍最不稳定，标准差为 1.03。作者的主要结论是 GPT evaluator 在文本 plausibility 分类上可达到人类间一致性的水平，但这不等于它已经可靠判断了视觉 distinctiveness，也不证明其在真实图片上的判断同样准确。

<div class="result-source" markdown="1">

来源：§5.2 Evaluator Validation, Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For the GPT-5.1 evaluator with high reasoning effort, L-H $\kappa$ matches the H-H baseline on the primary 4-point classification metric (0.530 vs 0.529, $\Delta=+0.001$; Table 3).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 困难条件和视觉 distinctiveness 的可靠性：重点考察 IH，以及 AgentID 和 PairDist 两个视觉子任务。

<div class="result-value" markdown="1">

IH 是人类判断中变异最大的条件，标准差为 1.03。视觉 distinctiveness 的人类-人类一致性较低：AgentID 的 $\kappa=0.277$，PairDist 的 $\kappa=0.407$；PairDist 上虽然 Gwet’s AC1 通过了报告的标准，但 LLM-human 的 Cohen’s $\kappa$ 存在较大差距。摘要还报告，最佳 evaluator 在 implausible-hard 条件上的准确率仅为 57%。

</div>

边界附近的事件最难判断，原因是人类对“略不合理”事件的 plausibility 本身意见不一致；因此提高 reasoning effort 不能消除任务内在的不确定性。视觉结果尤其不能被解释为模型已经完成图像层面的验证，因为标注者只是根据文字想象职业外观，真正的验证仍需展示实际 stimulus photographs。

<div class="result-source" markdown="1">

来源：§5.2 Evaluator Validation

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Human-human agreement on visual distinctiveness is itself low ($\kappa=0.277$ for AgentID, 0.407 for PairDist), so humans do not form a reliable benchmark.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验的主生成规模为 60 个英语动词，且动词必须能填入 agent、patient、instrument 和 location 四种角色；因此结果对其他语言、动词类型、事件模板和更广泛心理语言学材料的泛化尚未得到验证。
- GOLD 主要由文本 evaluator 的 plausibility、scene 和视觉 distinctiveness verdicts 决定，真实下游任务仍需要图像验证和领域专家验证；特别是视觉任务的人类-人类一致性较低，且最佳 evaluator 在 implausible-hard 条件上只有 57% 准确率，说明自动化流程仍不能完全取代人工判断。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- RB（baseline generation）：单次生成事件集合，不使用 evaluator 反馈；它检验没有迭代修正时的基础生成能力。
- R2V：单次生成中加入视觉可识别性相关约束，但不进行多轮 evaluator-guided refinement；它用于区分视觉约束本身与迭代反馈的作用。
- R2R：使用 evaluator 反馈进行最多 $k=3$ 轮的 plausibility 及条件判定修正；与 RB、R2V 比较可直接测试迭代 refinement 是否是质量提升的主要来源。
- R2VR：同时结合迭代 refinement 与视觉相关约束；它检验两类约束联合使用时是否能提高完整事件集合的合格率。

**实验想回答的问题**

- 在六个生成模型和四种生成方法下，STRIVE能否自动构造同时满足四种目标条件，即可 plausibility 分级与分类难度控制的事件集合，并通过迭代 refinement 提高完整合格率？
- LLM evaluator 对事件 plausibility 和视觉可区分性的判断，能否达到人类标注者之间的一致程度；哪些组件和条件最影响生成质量？

**实验实现**

生成器包括 GPT-5.1、Claude Sonnet 4.6、Qwen3-Next-80B、Qwen3-30B、Ministral-3-14B 和 Qwen3-4B，覆盖闭源与开源模型及不同规模。RB、R2V、R2R 和 R2VR 在 60 个动词上运行；迭代方法最多运行 $k=3$ 轮，当 evaluator 返回 GOOD scene 且四个条件均为 CORRECT 时提前停止。温度设为 $0.3$，以兼顾中间梯度条件 PH 与 IH 所需的候选多样性和结果稳定性；模型原生 reasoning/thinking mode 被关闭，改用 §3.1 的 scratchpad 保存完整推理痕迹。主结果使用 GPT-5.1 evaluator；为检验开源替代方案，还用 Qwen3-30B 重新评价全部生成结果。人类验证中，GPT-5.1（high reasoning effort）和 Claude Sonnet 4.6（non-thinking mode）通过了 AAT 上关于 unweighted Cohen’s $\kappa$ 的 non-inferiority 要求；Qwen3-30B 虽未通过该阈值，但其与 GPT-5.1 的 GOLD-tier concordance 为 81.5%。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除视觉可识别性约束 $Viz$：比较带视觉约束和不带视觉约束的 RB 生成结果，并使用 GPT evaluator。 | 移除 $Viz$ 后，所有模型的 GOLD rate 降至不高于 1.7%；对 GPT-5.1 的 RB，GOLD rate 从带视觉约束且无 scratchpad 的 16.7% 降至不带视觉约束的 0.0%。 | 该消融说明视觉约束对满足 STRIVE 文本预筛选规则很重要，尤其能避免生成在文字上容易被想象成相似外观的职业组合。它只测量对 text-based evaluator 约束的服从，不证明这些职业在真实图片中的视觉区分度已经提高。 | §7 Ablations, Table 4<br><span class="experiment-evidence">Under the text-based evaluator, removing the visual constraint from RB reduces GOLD% to $\leq 1.7\%$ across all models.</span> |
| 移除 reasoning scratchpad $ResSP$：比较有无 scratchpad 时各生成方法的 GOLD rate。 | scratchpad 在多数模型和方法上提高 GOLD rate；GPT-5.1 的 R2R 从 40.0% 升至 75.0%，增加 35.0 个百分点，R2VR 从 30.0% 升至 71.7%，增加 41.7 个百分点。Qwen3-Next-80B-A3B 是例外，在两个 single-shot 方法上约下降 8 个百分点。 | 在 GPT-5.1 的迭代方法中，scratchpad 带来的增益很大，说明显式保留全局推理过程可能帮助模型同时检查事件 plausibility、条件差异和其他约束。不过该结论不能外推到所有开源迭代设置，因为开源迭代单元使用 Qwen evaluator 提供反馈，作者因此没有把它们纳入保持 GPT-judge 一致性的消融读取。 | §7 Ablations, Table 4<br><span class="experiment-evidence">On iterative methods, GPT-5.1 gains +35.0 on R2R (40.0→75.0) and +41.7 on R2VR (30.0→71.7).</span> |

**定性案例**

- 视觉约束消融中的例子显示，不带约束时模型可能生成 glazier 与 home renovation contractor 这类都穿着普通工作服的职业组合；加入约束后则倾向选择具有更鲜明职业线索的 agent。该案例直观说明 $Viz$ 如何改变候选事件角色，但由于证据来自文字 evaluator，不能据此断言实际生成照片一定具有更高的视觉可区分性。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work probes and improves LLM reasoning and evaluator reliability for controlled graded-plausibility generation, including scratchpad reasoning and evaluator-guided refinement.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`4215562818f928966eebf74edbdb066783a940388175d6c0074497d9077f16f6`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
