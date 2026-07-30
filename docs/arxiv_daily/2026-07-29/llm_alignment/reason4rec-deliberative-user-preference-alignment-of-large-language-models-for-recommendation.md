---
title: "[论文解读] Reason4Rec: Deliberative User Preference Alignment of Large Language Models for Recommendation"
description: "[arXiv 2502.02061][对齐 / RLHF] 本文将推荐大模型从“看到历史与候选物品后立即预测反馈”改为“先显式分析偏好与物品特征、再匹配二者并预测反馈”，以提高复杂、低频和冷启动场景下推荐判断的可靠性。"
arxiv_id: "2502.02061"
announcement_date: "2026-07-29"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:03.598503+00:00"
source_sha256: "3ec97890783dc127772fd05bac118b686f4d70eb191f9a47c1f280c53dd10bdb"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型推荐"
  - "审慎推荐"
  - "用户偏好对齐"
  - "显式推理"
  - "言语化用户反馈"
  - "分步骤专家"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2502.02061</p>

# Reason4Rec: Deliberative User Preference Alignment of Large Language Models for Recommendation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-29</span>
<span><strong>作者</strong> Yi Fang, Wenjie Wang, Yang Zhang, Fengbin Zhu, Qifan Wang, Fuli Feng, Xiangnan He</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2502.02061v3) · [PDF 下载](https://arxiv.org/pdf/2502.02061v3) · **关键词** 大语言模型推荐, 审慎推荐, 用户偏好对齐, 显式推理, 言语化用户反馈, 分步骤专家  
**代码**: [https://github.com/Peter-Fy/Reason4Rec](https://github.com/Peter-Fy/Reason4Rec)  

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

本文将推荐大模型从“看到历史与候选物品后立即预测反馈”改为“先显式分析偏好与物品特征、再匹配二者并预测反馈”，以提高复杂、低频和冷启动场景下推荐判断的可靠性。

**不用术语来说**：现有推荐大模型常凭训练数据中表面的共现规律快速作答：某个候选内容看起来与用户看过的内容相关，模型就可能推荐它，却没有判断用户是否早已掌握相关知识、是否真正重视其具体特征。因此，推荐结果即使在主题上相关，也可能不符合用户当前需求。论文要解决的是如何让模型在给出喜欢或不喜欢的判断前，先形成一段与该用户真实偏好相符、能够支持最终判断的推理。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“审慎推荐（Deliberative Recommendation）”任务，将显式的用户偏好推理加入推荐大模型的对齐目标，要求模型先分析用户偏好和候选物品特征，再预测用户反馈。
- 作者提出利用评论等用户自然产生且可获取的文本反馈监督推理，使生成理由尽量对应反馈背后的真实、个性化偏好，而非依赖人工编写理由或受限的商业数据。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型推荐（RecLLM）研究方向：将用户历史行为与候选物品组织为语言模型输入，通过上下文学习、监督微调或直接偏好优化，使模型预测用户对候选物品的反馈。现有方法通常直接生成评分、点击倾向等反馈标签，容易依赖训练数据中的表面模式、偏差或伪相关，并且没有要求模型先分析用户的个性化偏好及候选物品特征；这在低频物品、冷启动物品或需要区分“内容相关”与“用户实际需要”的复杂场景中可能导致不可靠预测。本文据此提出“审慎推荐”：模型在输出反馈预测前，必须显式完成偏好提炼、偏好匹配和反馈预测，从而把中间推理也纳入推荐对齐目标。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**推荐大语言模型（RecLLM）**

指经过提示或任务专门训练、能够依据用户历史和候选物品预测用户反馈的大语言模型。本文关注的不是一般文本生成，而是让语言模型与个体用户的推荐偏好对齐。

</div>
<div class="conceptitem" markdown="1">

**审慎推荐（Deliberative Recommendation）**

一种要求模型先显式推理用户偏好与物品特征、再预测用户反馈的任务设定。其核心区别是把推理过程本身作为训练目标，而非只监督最终标签。

</div>
<div class="conceptitem" markdown="1">

**言语化用户反馈（verbalized user feedback）**

用户以自然语言表达的评价依据，例如评论或对话；它不仅表明用户喜欢或不喜欢，还可能说明具体原因。本文将其作为推理监督信号，以约束生成理由与用户真实表达的偏好一致。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定目标用户的历史交互信息、一个候选物品，以及训练阶段可获得的言语化用户反馈，目标是训练一个RecLLM：先从用户历史中提炼细粒度偏好，并从已有反馈中识别候选物品的正负特征；再匹配用户偏好与物品特征，形成该用户可能喜欢或不喜欢该物品的理由；最后结合这些理由预测用户反馈。该设定假定用户偏好高度个性化且多样，不能用统一、明确的规则完整描述，因此使用用户生成且可获得的评论或对话作为个体层面的推理监督；同时，部署时的最终输出仍服务于反馈预测，显式推理是提高预测可靠性与可解释性的中间过程。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **DRDT**: 通过提示让大语言模型从多个方面分析用户偏好，并使用批评提示进行自我反思，属于利用现有模型能力的上下文推理方法。作者认为此类方法缺少推荐任务专门微调，效果受基础模型已有能力限制；Reason4Rec则直接训练分步骤推理能力。
- **GOT4Rec**: 使用思维图提示模型沿三个方向开展推荐推理，同样属于提示驱动的上下文学习路线。它与本文都强调显式推理，但Reason4Rec进一步把言语化反馈作为监督，并为不同推理步骤训练专门专家。
- **RecSAVER与EXP3RT**: 两者均通过微调提升推荐推理能力：RecSAVER用更大语言模型生成的推理作为小模型训练真值，EXP3RT先从评论历史构建用户和物品画像，再在单一步骤中推理偏好并预测评分。作者指出，这类方法把复杂推理压缩为联合训练的单一步骤，且训练数据选择缺乏细粒度监督；Reason4Rec改为独立训练偏好提炼、偏好匹配和反馈预测，并以用户自身的言语化反馈约束理由。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

推荐大模型在一般场景中虽能取得性能提升，但面对需要理解用户知识水平、细粒度偏好或物品新颖性的复杂案例时仍可能给出无价值甚至令人失望的推荐。例如，仅依据内容相关性向已经观看过LLaMA视频的高年级博士生推荐基础注意力教程，会忽略该用户已有的知识基础。实际系统因此需要一种能在预测前检查“这个物品的哪些特征与这个用户当前偏好相符或冲突”的可靠决策机制。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **监督微调式推荐对齐**：将用户交互历史和候选物品作为输入，以用户评分、点击或喜欢与否等反馈标签作为目标，微调大语言模型直接生成预测结果。模型主要从历史样本中学习输入模式与反馈标签之间的映射。
- **直接偏好优化式推荐对齐**：利用偏好数据直接调整模型，使其更倾向于产生符合用户选择的推荐输出；虽然训练目标不同于普通监督微调，但现有任务设定仍主要关注最终反馈或推荐结果，没有把预测前的显式偏好推理作为独立对齐目标。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 直接预测反馈的目标容易使模型学习训练数据中的偏差和虚假相关性，而不是判断偏好与物品特征之间是否存在真实匹配；其后果是模型对低频物品或冷启动物品的泛化能力受限。
- 以最终标签为中心的优化会推动模型立即作出预测，并弱化对用户偏好、候选物品优缺点及二者关系的充分分析；因此模型可能只抓住主题相关性等表面线索，在复杂案例中产生看似合理但实际无价值的推荐。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有推荐对齐方法缺少一种同时满足两个条件的任务与学习机制：一是把预测前的显式偏好推理正式纳入优化目标，而非只优化最终反馈标签；二是使用可获得的真实用户信号约束这段推理，使其能够覆盖从历史中提炼偏好、识别候选物品特征、解释二者匹配关系到预测反馈的完整过程。原文进一步表明，该方向仍处于初步阶段，目前仅采用评论作为文本化用户反馈，历史选择、图结构建模和推理效率仍有待研究。

</div>
<div markdown="1"><span>核心问题</span>

能否利用评论等文本化用户反馈作为推理监督，并通过分步骤、专门化且相互协作的专家训练推荐大模型，使其在输出用户反馈预测之前生成与个体真实偏好一致的显式理由，从而同时改善预测准确性与推理质量？

</div>
<div markdown="1"><span>作者直觉</span>

评论不仅给出“喜欢或不喜欢”的结果，往往还说出了用户在意的方面以及物品的具体优缺点，因而比单一标签包含更直接的偏好证据。将复杂判断拆成三个步骤也能降低学习难度：先分别弄清用户在意什么和物品具有什么特征，再判断二者哪里契合或冲突，最后依据这些理由预测反馈。通俗地说，这相当于让模型先整理证据、再比较证据、最后下结论，从而减少仅凭表面相关性仓促推荐的情况。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Reason4Rec把评分预测改写为“先提炼偏好、再分析匹配、最后预测评分”的审议式推荐流程。对于历史交互中的每条“评分—评论”，Summarizer先将长评论压缩为正面方面、负面方面和用户偏好元素；Reasoner再按时间顺序汇总用户与目标物品的历史摘要，显式生成用户可能喜欢或不喜欢该物品的理由；Predictor最后结合历史评分、偏好摘要和匹配理由输出评分。这样，最终预测不必直接从冗长评论中猜测，而是建立在可检查的偏好证据和匹配分析之上。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤1：历史评论的偏好蒸馏

Summarizer根据物品、评分和评论生成结构化的 aspect-preference summary，分别概括评论中的正面方面、负面方面和用户偏好元素；摘要器通过监督微调学习教师模型生成的目标摘要。

<div class="method-step__io" markdown="1">

**输入**：历史交互 (r_{ui}, c_{ui})，其中 u 为用户、i 为物品、r_{ui} 为用户对物品的评分、c_{ui} 为对应评论文本。  
**输出**：每条历史交互对应的一份简短方面—偏好摘要，例如“Positive Aspects”“Negative Aspects”和“User Preference Elements”下的代表性关键词。

</div>

**直观理解**：这一步像先把每篇长评论整理成标签式笔记，留下真正说明用户为何喜欢或不喜欢某物品的信息。它既减少后续模型要阅读的噪声，也把分散在自然语言中的偏好变成较稳定的推理证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤2：用户与物品历史构建

系统分别收集用户过去评价过的物品摘要，以及其他用户过去对目标物品的摘要，并按交互时间顺序组织为Reasoner和Predictor可读取的上下文；受上下文长度限制，实验中保留双方最近的十条历史交互。

<div class="method-step__io" markdown="1">

**输入**：目标用户 u 和目标物品 i，以及二者历史交互集合 \mathcal{H}_{u} 与 \mathcal{H}_{i} 中预先生成的方面—偏好摘要和历史评分。  
**输出**：一个同时描述“用户通常偏好什么”和“目标物品通常呈现什么特征”的紧凑历史上下文。

</div>

**直观理解**：用户历史提供需求侧画像，物品历史提供供给侧画像；把两边放在一起，模型才能判断具体用户与具体物品是否匹配。只取最近十条是在信息覆盖、近期兴趣和上下文成本之间作折中。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤3：偏好匹配推理

Reasoner比较用户偏好与物品正负面特征，生成用户可能喜欢或不喜欢目标物品的显式匹配分析；训练时使用经过质量控制的理由监督，使模型学习从历史证据推导理由，而不是依赖目标交互评论。

<div class="method-step__io" markdown="1">

**输入**：按时间组织的用户历史 \mathcal{H}_{u}、物品历史 \mathcal{H}_{i} 及其方面—偏好摘要。  
**输出**：面向目标用户—物品对的自然语言推荐理由，说明偏好与物品特征的吻合点和冲突点。

</div>

**直观理解**：这一步相当于先写出判断依据，再作最终决定。它尤其能防止模型只照搬用户常给的评分，例如在用户几乎总打五星但目标物品并不符合其具体偏好时识别出不匹配。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤4：理由驱动的评分预测

Predictor作为与Reasoner分离训练的专家，根据历史证据和显式理由预测用户对目标物品的反馈；评分任务中最终只需解码一个评分 token。

<div class="method-step__io" markdown="1">

**输入**：历史评分、方面—偏好摘要，以及Reasoner生成的匹配理由。  
**输出**：目标用户 u 对目标物品 i 的预测评分；该分数还可用于候选物品排序。

</div>

**直观理解**：Reasoner负责把证据讲清楚，Predictor只负责把证据映射成分数。职责分离降低了一个模型同时生成长理由和精确评分的学习难度，也使最终解码成本较低。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

这篇论文不以中心数学公式展开，或全文中未提取到可靠的关键公式。

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：Summarizer使用教师模型生成的方面—偏好摘要作为监督目标进行SFT，即通过监督微调学习从“物品、评分、评论”生成结构化摘要。Reasoner采用专家级训练策略：先构造候选理由，再使用奖励模型判断理由是否与目标评论所体现的真实偏好一致，并依据阈值 \tau 筛选高质量理由作为推理监督；Predictor则独立学习从历史评分、摘要和匹配理由预测真实评分。所给原文节选没有提供这些模块的完整损失函数、奖励计算公式或明确编号的核心方程，因此不应补写交叉熵、回归损失或奖励公式；三者如何加权、是否联合优化也为原文节选未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Summarizer（偏好摘要器）**

该模块把单次交互的原始评论和评分转换为方面—偏好摘要，目标字段包含正面方面、负面方面和用户偏好元素。作者使用闭源ChatGPT作为教师生成摘要，再对开源LLM进行监督微调；所有历史摘要可以离线生成和存储，因此线上无需重复执行该模块。

> 直观理解：原始评论往往冗长、含噪且表达方式不统一，直接把它们全部交给推理模型会浪费上下文。摘要器把评论整理为可复用的结构化笔记，并让后续推理更直接地围绕用户明确表达过的偏好展开。

**2. Reasoner（偏好匹配推理器）**

该模块读取用户侧与物品侧按时间排列的历史摘要，显式分析用户偏好和目标物品特征的匹配关系。其训练理由需要经过奖励模型筛选：奖励模型利用候选理由进行评分预测，以候选理由是否能反映目标评论中的真实偏好作为质量信号，并通过数据集相关阈值 \tau 保留高质量理由。

> 直观理解：仅让语言模型自由生成解释，理由可能流畅但不忠于真实偏好；奖励筛选的作用是保留那些确实有助于恢复用户反馈的理由。换言之，系统关心的不只是“说得像理由”，还关心理由是否包含与真实评论一致的偏好信息。

**3. Reward Model（理由质量评估器）**

奖励模型通过读取不同候选理由并预测真实评分，评估理由与目标用户偏好的对齐程度；训练Reasoner时按照奖励阈值 \tau 筛选候选理由。原文实验表明，使用与目标评论更相似的理由时，该模型的评分误差更低，但所给节选未包含其完整架构、奖励函数和候选理由生成算法。

> 直观理解：奖励模型像一个理由审稿人：如果某段理由能帮助它更准确地判断用户最终评分，该理由就更可能抓住了真实偏好。阈值过严会使可用训练样本不足，过松则会混入低质量理由，因此需要在验证集上选择。

**4. Predictor（反馈预测器）**

该模块在Reasoner之后独立训练，输入历史评分、偏好摘要和Reasoner生成的理由，输出离散评分。独立Predictor避免在同一次生成中同时完成复杂匹配分析和数值预测；推理时最终阶段仅生成一个token。

> 直观理解：它相当于只做最后裁决，而不承担整理证据和撰写分析的任务。消融结果显示，把Reasoner与Predictor合并为一个模型会增加预测误差，说明这种专家分工是方法设计的一部分。

**训练与推理**

训练阶段首先让教师模型为历史“评分—评论”对生成方面—偏好摘要，并以这些目标数据监督微调Summarizer；随后可为训练集历史交互离线生成摘要。Reasoner阶段以用户侧和物品侧历史摘要为输入生成候选匹配理由，再由奖励模型利用这些理由进行评分预测并实施质量筛选：候选理由越能帮助恢复真实反馈，越可能被视为与用户真实偏好对齐；保留下来的理由用于Reasoner微调。最后单独训练Predictor，使其根据历史评分、摘要和理由预测目标评分。为保证比较公平，Reason4Rec、Rec-SAVER和EXP3RT均使用相同规模的12,000个用户—物品对作为LLM指令数据；奖励模型另用8,000个与指令数据不重叠的用户—物品对。
推理阶段先从离线存储中读取历史方面—偏好摘要，不再运行Summarizer；系统截取目标用户与目标物品双方最近十条历史交互，由Reasoner在线生成偏好匹配分析，再将该分析连同历史评分和摘要交给Predictor。Predictor输出单个评分token，该评分既可作为显式评分预测，也可作为候选物品的排序分数。因线上只执行Reasoner和Predictor，方法避免了逐次重新摘要全部评论的开销。

**复现信息**

所有需要微调的LLM推荐方法均以GPT-3.5-turbo作为教师模型，并在Llama-3-8B上采用QLoRA微调；QLoRA只更新约45M个低秩适配器参数，占8B模型不到1%，原文称相较全参数微调可减少超过70%的GPU显存开销。训练与推理由Unsloth加速，每个基于QLoRA的模块在一张NVIDIA A100上约需5小时。各数据集的奖励筛选阈值分别设为Music 0.1、Book 0.2和Yelp 0.08；作者在按时间划分的验证集上选择阈值，先找使约50%候选理由被保留的初值，再在其附近局部网格搜索。上下文统一采用最近十条历史交互，这是复现输入规模和解释推理成本所必需的设置；其余提示词全文、奖励函数细节及优化器等信息在所给节选中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- Amazon Digital Music：使用完整数据，共64,706次交互、5,541名用户和3,568个物品。该数据集用于检验方法在规模较小、相对稠密的商品推荐场景中的评分预测与理由生成能力。
- Amazon Book：受时间和计算资源限制，仅使用最后两个月的数据，共540,074次交互、174,050名用户和127,821个物品。它代表用户与物品规模更大、交互相对稀疏的商品推荐场景。
- Yelp Open Dataset：使用最后六个月的数据，共302,558次交互、173,099名用户和67,854个物品。它用于检验方法能否从亚马逊商品评论场景迁移到本地商户评论场景。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**MAE（Mean Absolute Error，平均绝对误差）**

计算预测评分与真实评分之间绝对误差的平均值，直接反映一次评分预测通常偏离真实值多少；相较RMSE，它对少数极大误差的额外惩罚较弱。 （越低越好，因为数值越小表示预测评分与真实用户反馈越接近。）

</div>
<div class="metricitem" markdown="1">

**RMSE（Root Mean Square Error，均方根误差）**

先对每个评分误差平方、求平均，再开平方。平方操作会放大较大的预测错误，因此该指标更强调模型是否避免严重错判。 （越低越好，因为较低的RMSE意味着整体预测误差更小，尤其意味着大误差更少。）

</div>
<div class="metricitem" markdown="1">

**BLEURT**

利用上下文语义表示比较模型生成理由与目标物品评论之间的语义一致性。它不只检查字面词汇重合，而是试图衡量两段文本表达的含义是否接近。 （越高越好，因为更高分通常表示生成理由与目标评论在语义上更一致；但它不能单独证明理由忠实反映了模型的真实决策过程。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 三个真实世界数据集上的评分预测准确性

<div class="result-value" markdown="1">

作者概括性声称，实验表明Reason4Rec能够提高预测准确性；但所给材料未包含表I的具体数据行，因而无法报告各数据集上的MAE、RMSE、排名、相对提升幅度或统计显著性。

</div>

这项结果若由完整表格支持，意味着显式推理不只是生成可读解释，也可能帮助模型更准确地预测用户评分。但当前证据只有摘要中的总体结论，没有分数据集数值，不能判断提升是否稳定、是否只集中在某个数据集，也不能判断收益相对最强基线有多大。

<div class="result-source" markdown="1">

来源：Abstract；所给5.1.3节仅出现表I标题，具体结果行未提供

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Extensive experiments conducted on three real-world datasets demonstrate the rationality of the deliberative task formulation and the effectiveness of the proposed framework in improving both prediction accuracy and reasoning quality.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 生成理由与目标评论的语义一致性

<div class="result-value" markdown="1">

作者概括性声称Reason4Rec提高了推理质量；所给材料说明使用BLEURT和GPTScore进行评价，但没有提供两项指标的具体分数或与基线的差值。

</div>

这里的“推理质量”在实验上主要被操作化为生成文本与用户目标评论的语义对齐程度。更高的一致性可以说明理由更贴近用户实际表达的偏好，但不等同于证明推理链条因果正确、事实完全可靠，或这些文字就是模型形成评分预测时真正采用的内部依据。

<div class="result-source" markdown="1">

来源：Section 5.1.2, Evaluation Metrics

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">To evaluate reasoning quality, we employ BLEURT [44] and GPTScore [49] to measure the semantic alignment between the generated reasoning and the target item review.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 时间顺序划分下的未来交互预测

<div class="result-value" markdown="1">

实验确保测试交互发生在训练和验证交互之后，以减少信息泄漏；这是评估协议的有效性结果，不是Reason4Rec优于基线的性能结果。

</div>

按时间划分比随机划分更接近实际推荐：模型只能使用过去预测未来。它提高了实验结论的可信度，但本身不能证明方法有效；真正的优越性仍需结合完整的基线得分、重复实验和显著性分析判断。

<div class="result-source" markdown="1">

来源：Section 5.1.1, Datasets

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">For each dataset, we split it into training, validation, and test sets following a ratio of 8:1:1 based on the timestamps of interactions, ensuring that test interactions occur after all training and validation interactions to prevent information leakage [23].</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 材料完整性限制：所给来源在5.1.3节表I标题处截断，没有表格数据、基线定义、RQ2/RQ3实验、消融表或案例分析。因而不能可靠填写要求中的数值主结果和关键消融；任何具体分数或组件贡献都会构成无依据推断。
- 评价有效性限制：BLEURT和GPTScore衡量生成理由与目标评论的语义一致性，但语义相似不必然意味着理由事实正确、偏好推断忠实，或推理过程真实支撑了评分预测。尤其GPTScore依赖GPT-4o，所给节选没有报告提示模板、重复评审或一致性分析。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。所给节选在“5.1.3 Baselines”标题及表I说明处截断，没有提供任何基线名称、类别、输入条件或训练方式，因此无法可靠判断各比较方法所代表的技术路线。

**实验想回答的问题**

- RQ1：Reason4Rec相较其他基线，在用户反馈（评分）预测准确性和生成理由质量上表现如何？
- RQ2与RQ3：多步推理为何优于一步推理，以及理由生成方法和奖励模型能否有效利用用户以自然语言表达的偏好反馈？

**实验实现**

实验对三个数据集执行按时间排序的8:1:1训练、验证、测试划分，而不是随机划分；这一协议模拟“用历史交互预测未来反馈”，并避免测试时期信息进入训练集。数据采用5-core过滤。评分预测以MAE和RMSE评价，生成理由以目标物品评论作为参照，使用BLEURT及基于GPT-4o的GPTScore评价语义一致性。所给节选未提供Reason4Rec及各基线的模型规模、训练超参数、随机种子、重复运行次数、显著性检验、解码配置、GPTScore提示模板或具体基线列表，因此这些实现与复现信息均为“原文未明确报告”。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：reused verified category during targeted regeneration
- 全文指纹：`3ec97890783dc127772fd05bac118b686f4d70eb191f9a47c1f280c53dd10bdb`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
