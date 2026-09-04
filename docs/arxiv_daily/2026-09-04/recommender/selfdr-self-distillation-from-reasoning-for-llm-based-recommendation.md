---
title: "[论文解读] SelfDR: Self-Distillation from Reasoning for LLM-Based Recommendation"
description: "[arXiv 2609.03313][推荐系统] 原文未明确报告。"
arxiv_id: "2609.03313"
announcement_date: "2026-09-04"
primary_category: "recommender"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:42:21.287399+00:00"
source_sha256: "aa68f9d36e8320468612f17af3d96e9b3230f6141bac1a6e37e05c64012d2536"
tags:
  - "推荐系统"
  - "LLM Reasoning"
  - "LLM 其他"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">推荐系统 · arXiv 2609.03313</p>

# SelfDR: Self-Distillation from Reasoning for LLM-Based Recommendation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Chumeng Jiang, Jiayin Wang, Xinjie Lin, Zhiqiang Guo, Hengliang Luo, Min Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: DCST, Tsinghua University , Quan Cheng Laboratory , Beijing , China；DCST, Tsinghua University；Quan Cheng Laboratory；Affiliation: DCST, Tsinghua University , Beijing , China；Affiliation: Quan Cheng Laboratory , DCST, Tsinghua University , Beijing , China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03313v1) · [PDF 下载](https://arxiv.org/pdf/2609.03313v1) · **关键词** 推荐系统<br>


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

本文属于基于大语言模型（LLM）的推荐研究。该方向将用户历史、物品元数据、评论等信息组织为文本或文本与协同过滤信号的组合，再利用 LLM 的语言理解能力预测用户可能交互的物品。常见适配方式包括零样本提示、监督微调和混合架构；近年来，研究者进一步引入显式推理，使模型先解释用户偏好与物品特征，再生成推荐结果。SelfDR 关注其中一个核心矛盾：推理能够帮助模型处理细粒度文本偏好，但多步推理或生成长推理轨迹会增加推理延迟和计算开销，因此实际系统需要在推荐效果与单次推理效率之间取得平衡。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**LLM-based recommendation**

指把推荐任务转化为 LLM 可以处理的语言建模或指令跟随任务，例如输入用户历史和物品信息，输出下一件可能交互的物品。其优势是能够利用文本语义，但也依赖模型能否准确理解推荐领域中的偏好信号。

</div>
<div class="concept-item" markdown="1">

**显式推理与推理轨迹**

显式推理是模型在最终推荐前生成中间分析步骤或 rationale（理由文本），用于整理用户和物品信息、识别偏好并修正预测。它可能提升推荐质量和可解释性，但生成额外文本会增加 token 数、延迟和计算成本。

</div>
<div class="concept-item" markdown="1">

**知识蒸馏与自蒸馏**

知识蒸馏让学生模型学习教师模型的输出或内部知识，从而在较低推理成本下保留教师能力。自蒸馏不依赖独立的更强教师，而是利用同一模型或其不同阶段、不同推理方式产生教学信号；SelfDR 进一步蒸馏由推理过程增强的推荐结果。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

论文研究基于 LLM 的下一物品推荐：给定用户的历史交互及其关联文本信息，模型需要预测用户接下来可能交互的物品，通常表现为对候选物品进行排序或直接输出推荐结果。训练阶段可以使用历史交互中的真实下一物品作为监督信号；推理阶段则要求模型在不生成显式中间理由的情况下直接输出推荐。论文的关键设定是，输入信息保持一致时，直接推荐学生应尽量继承推理增强教师的判断能力，同时避免多步推理和长 reasoning trace 带来的额外开销。SelfDR 中的 reasoner、teacher recommender 和 student recommender 共享同一基础 LLM 架构，不假设存在可调用的外部强教师模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$u$**

用户，表示推荐任务中的目标用户。

</div>
<div class="notation-item" markdown="1">

**$H_u$**

用户 $u$ 的历史交互序列，包含该用户过去交互过的物品及其可用文本信息。

</div>
<div class="notation-item" markdown="1">

**$i^{+}$**

训练样本中的真实下一交互物品，即模型应当学习预测的正样本。

</div>
<div class="notation-item" markdown="1">

**$r$**

reasoner 生成的 rationale 或推理理由，用于概括用户历史与目标物品之间的偏好联系，并作为教师推荐器的辅助输入。

</div>

</div>

**直接相关的工作**

- 原文未明确报告，待核对引用关系。

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

SelfDR的目标是把“显式推理后再推荐”的效果压缩到“直接推荐”模型中，使线上推理不再生成理由。给定用户$u$的按时间排序交互历史$H_u$和候选集$\mathcal{C}_{u,i}$，系统先用与推荐器相同的基础LLM训练一个Reasoner；Reasoner根据$H_u$与真实下一物品的元数据$\mathcal{M}_i$生成理由$r_{u,i}$。该理由与历史、候选集一起输入教师推荐器，形成带推理信息的候选分布；学生推荐器只读取历史和候选集，并同时学习真实标签与教师分布。教师和学生采用相同架构，蒸馏期间固定教师，仅更新学生参数，因此“自蒸馏”指监督信号来自同一基础LLM构造出的推理增强版本，而不是外部大模型。
端到端看，训练分为Reasoner强化学习、教师构造、教师到学生的离线蒸馏三个阶段。Reasoner的奖励直接取决于其理由能否帮助冻结推荐器正确预测下一物品，并通过提示约束与标题片段遮蔽降低答案泄漏；蒸馏时则根据教师对正样本的排名，以及教师是否优于学生，动态设置蒸馏权重$\alpha$。直观地说，教师可以在训练时“看一份关于用户偏好的分析笔记”，学生看不到笔记，但学习教师对所有候选项的相对判断；部署时只保留学生，以一次简短输出获得推荐结果。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 任务表示与推荐器预适配

将候选物品映射为唯一字符标识符，并对推荐LLM进行指令微调，使其能由$H_u$和$\mathcal{C}_{u,i}$预测标识符；同时用各标识符token的生成对数概率形成候选排序$\mathcal{R}_{u,i}$。蒸馏开始前，教师与学生共享这组指令微调后的参数。

<div class="method-step__io" markdown="1">

**输入**：用户历史$H_u=(h_{u,1},\ldots,h_{u,t})$、候选集$\mathcal{C}_{u,i}$、真实下一物品$i$及其元数据$\mathcal{M}_i$；每条历史记录$h_{u,j}$包含物品元数据与交互细节。<br>
**输出**：能够执行推荐任务的共同初始化模型$f$，以及可比较教师、学生候选排名的统一输出空间。

</div>

**直观理解**：模型不是生成物品长名称，而是在候选表中选择一个短标识符；标识符的概率也可用于把所有候选项排序。先让教师和学生站在同一起点，可使后续差异主要来自教师额外获得的理由。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 以下游推荐奖励训练Reasoner

Reasoner生成解释$r_{u,i}$，再将$r_{u,i}$、$H_u$和$\mathcal{C}_{u,i}$送入冻结推荐器；以所得下一物品预测$s_{u,i}$的推荐准确性作为GRPO奖励，优化Reasoner。提示要求Reasoner不要直接复述物品元数据；若理由与物品标题存在连续三个或更多完全重合的词，则在计算奖励前遮蔽这些词。

<div class="method-step__io" markdown="1">

**输入**：训练样本中的用户历史$H_u$与真实下一物品元数据$\mathcal{M}_i$，以及一个冻结的推荐器和相应候选集$\mathcal{C}_{u,i}$。<br>
**输出**：一个能生成面向推荐目标、而非仅追求语言流畅度的Reasoner。

</div>

**直观理解**：这里不直接给“好理由”打语言分，而是检验理由是否真的让推荐更准。标题遮蔽类似考试中盖住答案，避免模型仅把真实物品名称复制给推荐器。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造推理增强教师推荐器

将理由拼接到推荐输入中，并对推荐器进行指令微调，得到教师参数$\Theta_t$；教师计算$s^t_{u,i},\mathcal{R}^t_{u,i}=f(H_u,\mathcal{C}_{u,i},r_{u,i})$。其监督信息不仅包含最终预测，还包含候选标识符上的完整概率或logit结构。

<div class="method-step__io" markdown="1">

**输入**：训练完成的Reasoner、用户历史$H_u$、候选集$\mathcal{C}_{u,i}$及Reasoner生成的理由$r_{u,i}$。<br>
**输出**：固定的推理增强教师，以及教师对每个训练样本给出的候选分布和正样本排名$rank_i^t$。

</div>

**直观理解**：理由相当于给教师附加一份针对该用户和目标物品的分析提示，使教师在候选项之间作出更细致的比较。保留完整分布比只保留第一名更有信息，因为它还展示了哪些错误候选与正确候选接近。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 动态加权的离线自蒸馏

学生参数$\Theta_s$同时最小化对真实标签的交叉熵$\mathcal{L}_{ce}$和教师—学生分布差异$\mathcal{D}_{kd}$；论文采用其称为反向KL的蒸馏损失，并按样本动态计算$\alpha$。当教师未把正样本排得足够靠前，或教师排名比学生更差时，软门控与惩罚因子会降低教师监督的占比。

<div class="method-step__io" markdown="1">

**输入**：固定教师的候选分布、学生仅由$H_u$与$\mathcal{C}_{u,i}$得到的分布、真实下一物品标签，以及教师和学生对正样本的排名$rank_i^t$与$rank_i^s$。<br>
**输出**：无需理由输入、但吸收教师排序行为的直接推荐学生模型。

</div>

**直观理解**：学生一方面听真实答案，另一方面模仿教师对各候选项的“信心分配”。若某个样本上教师表现不可靠，系统就少听教师，避免把教师错误强行传给学生。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 真实标签与教师分布的联合蒸馏目标

$$
\min_{\Theta_s}\left[(1-\alpha)\mathcal{L}_{ce}(\Theta_s)+\alpha\mathcal{D}_{kd}(\Theta_t,\Theta_s)\right]
$$

**符号说明**

- $\Theta_s$：直接推荐学生模型的可训练参数
- $\Theta_t$：推理增强教师模型的参数；离线蒸馏期间保持固定
- $\mathcal{L}_{ce}$：学生预测相对于真实下一物品标签的交叉熵损失
- $\mathcal{D}_{kd}$：教师与学生在候选字符标识符上的分布差异；论文具体采用其称为反向KL的损失
- $\alpha$：按样本动态调整的蒸馏权重，用于平衡教师监督与真实标签监督

<div class="equation-explanation" markdown="1">

**直观理解**：该目标同时保留两类信息：$\mathcal{L}_{ce}$要求学生选中真实下一物品，$\mathcal{D}_{kd}$要求学生复现教师对整个候选集合的软排序。当$\alpha$较大时更依赖教师的推理增强判断，较小时更依赖真实标签；教师固定可避免师生分布在训练中同时漂移。论文的式（8）把蒸馏项写成对候选$j\in\mathcal{C}_{u,i}$求和的$p_{\Theta_t}\log(p_{\Theta_t}/p_{\Theta_s})$，即由教师分布加权的KL形式。<br>
**原文位置**：第3.4节，式（7）；蒸馏项展开见式（8）

</div>

</div>

<div class="equation-block" markdown="1">

#### 基于师生正样本排名的动态权重

$$
\begin{aligned}\alpha(rank_i^t,rank_i^s)&=\alpha_{base}f(rank_i^t-k)\,\sigma\!\left(\frac{rank_i^s-rank_i^t}{\tau}\right)\,\beta^{\mathbb{1}(rank_i^t>rank_i^s)},\\ f(x)&=1+\tanh(x/\gamma)\end{aligned}
$$

**符号说明**

- $rank_i^t$：教师对真实物品$i$给出的排名，数值越小表示越靠前
- $rank_i^s$：学生对真实物品$i$给出的排名
- $\alpha_{base}$：动态蒸馏权重的基础缩放系数
- $k$：期望教师将正样本排入的阈值名次
- $\sigma$：sigmoid函数，用师生排名差进行连续门控
- $\tau$：控制师生排名差门控平滑程度的温度系数
- $\gamma$：控制教师排名相对阈值的调整函数平滑程度的温度系数
- $\beta$：教师排名差于学生时启用的额外惩罚参数
- $\mathbb{1}(rank_i^t>rank_i^s)$：教师排名比学生差时取1、否则取0的指示函数

<div class="equation-explanation" markdown="1">

**直观理解**：权重同时回答两个问题：教师自身是否把正确物品排得合理，以及教师是否比当前学生更好。$f$和sigmoid使权重随排名连续变化，而不是在某个边界突然开关；若$rank_i^t>rank_i^s$，说明教师把正样本排得更后，便额外启用$\beta$惩罚。需要注意，具体增减幅度还取决于论文所设$\alpha_{base}$、$\beta$、$\tau$和$\gamma$，所给方法节摘录未报告这些数值。<br>
**原文位置**：第3.4节，式（9）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优化分两层进行。第一层用GRPO更新Reasoner：Reasoner对$(H_u,\mathcal{M}_i)$生成$r_{u,i}$，冻结推荐器再根据$(H_u,\mathcal{C}_{u,i},r_{u,i})$预测$s_{u,i}$，其推荐正确性构成奖励；因此梯度所追求的是“理由对推荐是否有用”，而不是理由与人工文本的相似度。训练好的Reasoner随后生成理由，用于指令微调推理增强教师。
第二层是固定教师的离线自蒸馏。学生最小化真实标签交叉熵与分布蒸馏损失的加权和，其中教师分布以额外理由为条件，学生分布不以理由为条件。论文将蒸馏损失称为reverse KL，但其展示的式（8）为$\sum_j p_{\Theta_t}(j)\log[p_{\Theta_t}(j)/p_{\Theta_s}(j)]$；分析时应以原式为准，即由教师概率加权，推动学生在教师高概率候选上分配相近概率。动态$\alpha$不是全局常数，而是利用当前样本的师生正样本排名决定教师信号强度，从而降低错误或不具优势的教师输出对学生的干扰。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 下游奖励驱动的Reasoner**

Reasoner与推荐器基于同一基础LLM，采用Group Relative Policy Optimization（GRPO）训练。对给定$H_u$和$\mathcal{M}_i$生成$r_{u,i}$后，冻结推荐器在加入该理由的条件下作出预测，奖励定义为$Reward(r_{u,i})=\mathrm{Acc}_{rec}(s_{u,i})$；其中$\mathrm{Acc}_{rec}$可实例化为推荐准确性指标。该设计将理由优化目标直接绑定到最终推荐，而不是使用独立的文本质量指标。

> 直观理解：模块关心的不是解释是否写得漂亮，而是它是否帮助推荐器找到正确物品。这样可减轻“解释评价很高、推荐却没有改善”的目标错位；不过Reasoner训练时读取真实下一物品元数据，因此必须依靠禁止复述和标题片段遮蔽来控制标签泄漏。

**2. 同骨干推理增强教师与直接推荐学生**

教师和学生具有相同推荐器架构及蒸馏前参数，但输入不同：教师使用$(H_u,\mathcal{C}_{u,i},r_{u,i})$，学生仅使用$(H_u,\mathcal{C}_{u,i})$。蒸馏采用离线方案，固定$\Theta_t$并只更新$\Theta_s$；监督对象是候选字符标识符的概率分布，而不只是教师生成的单个答案。

> 直观理解：教师的优势来自训练输入中多了一段理由，而不是模型更大或调用了外部系统。学生模仿整套候选概率，可以学习教师认为“次优但相似”的物品关系，避免把蒸馏退化为再次用硬标签做普通微调。

**3. 基于排名可靠性的动态蒸馏权重**

每个样本的$\alpha$由教师正样本排名相对阈值$k$的位置、师生排名差以及教师是否劣于学生共同决定。函数$f(x)=1+\tanh(x/\gamma)$和sigmoid提供连续软门控；当$rank_i^t>rank_i^s$时额外乘以$\beta$，论文表述该因子用于显著降低不利教师样本的蒸馏权重。

> 直观理解：固定蒸馏权重默认教师永远值得相信，但Reasoner生成的理由和教师预测都可能出错。动态机制相当于逐题评估教师：教师明显更有帮助时多模仿，教师连学生都不如时少模仿，同时避免使用非连续的硬筛选。

**训练与推理**

完整训练流程为：先将同一基础LLM指令微调为能通过候选字符标识符执行推荐的模型；再复制或沿用该骨干训练Reasoner，以真实下一物品元数据为条件生成解释，并用冻结推荐器的下游准确性反馈进行GRPO更新。Reasoner收敛后，为训练样本生成经过泄漏控制的理由，将其加入推荐输入，对推荐器进行指令微调，得到推理增强教师。蒸馏前教师和学生从相同的推荐器参数出发；随后冻结教师，教师读取理由而学生不读取理由，计算二者在候选标识符上的分布及正样本排名，并以动态加权的交叉熵和KL蒸馏目标更新学生。
推理阶段只保留学生。对新的$H_u$和$\mathcal{C}_{u,i}$，学生直接生成一个候选标识符，并可根据各候选标识符token的对数概率输出排序$\mathcal{R}_{u,i}$；无需先生成$r_{u,i}$，也无需运行教师。由此，额外推理主要存在于训练监督构造阶段，而不进入线上推荐链路。

**复现信息**

公平复现所必需的结构性细节包括：候选物品通过唯一字符标识符表示，推荐列表依据这些标识符token的生成对数概率排序；教师、学生和Reasoner均建立在同一基础LLM上，不调用外部LLM；教师和学生在蒸馏前均经过推荐指令微调并共享相同参数，蒸馏时教师固定；Reasoner训练采用GRPO，并将冻结推荐器的下游预测正确性作为奖励。为防止Reasoner利用真实目标物品直接泄漏答案，提示明确禁止复述输入元数据，并在理由中出现与物品标题连续三个或更多完全相同的词时，于奖励计算前遮蔽重合片段。
候选集可来自两种设置：普通ranking通常把真实物品与随机负样本组合，reranking则使用基础排序器依据目标交互发生前的历史检索出的top-$K$物品，且真实物品不保证包含其中。方法节摘录没有给出基础LLM型号、GRPO采样组大小、优化器、学习率、$k$、$\alpha_{base}$、$\beta$、$\tau$、$\gamma$、训练轮数、最大理由长度或具体准确性奖励实例，故这些数值不能从当前材料中补全，需查阅论文实验设置或代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Amazon Clothing Shoes and Jewelry（Clothing）：包含 39,387 个用户、23,033 个物品和 278,677 次交互，密度为 0.0307%。数据带有商品元数据和用户评论，用于检验方法在稀疏、属性丰富的电商服饰场景中的表现；预处理采用 5-core 过滤和 leave-one-out 划分。
- Amazon Home and Kitchen（Home）：包含 66,519 个用户、28,237 个物品和 551,682 次交互，密度为 0.0294%。它同样提供商品元数据与评论，但用户和物品规模更大，用于检验方法在另一种属性丰富且高度稀疏的电商领域中的稳健性；采用相同的 5-core 与 leave-one-out 设置。
- MovieLens-1M（ML1M）：包含 6,040 个用户、3,416 部电影和 999,611 次评分，密度为 4.8448%，并提供用户与电影元数据。它比两个 Amazon 数据集密集，但缺少评论，因此既用于跨领域验证，也用于检验依赖评论的方法是否受数据模态限制；EXP3RT 因依赖评论而不能用于该数据集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**$H_g@1$**

Top-1 Generation Accuracy，即模型直接生成的单个物品标识符是否为真实下一物品。由于下一物品训练只提供一个正确标签，该指标直接检验生成答案本身是否正确，而不是利用所有候选的概率重新排序后是否命中。 （越高越好；更高表示模型直接输出正确下一物品的概率更大。）

</div>
<div class="metric-item" markdown="1">

**$H_l@K$**

基于候选物品标识符 token 的生成对数概率排序得到完整列表后，真实物品是否进入前 $K$ 位。它衡量命中能力，但不区分真实物品位于前 $K$ 中的具体位置。 （越高越好；更高表示更多测试样本的真实下一物品进入推荐列表前 $K$。）

</div>
<div class="metric-item" markdown="1">

**$N_l@K$**

列表上的 NDCG@K，对前 $K$ 位中的命中按位置折损；同样命中的情况下，真实物品排得越靠前，得分越高。因此它比 $H_l@K$ 更能反映列表内部的排序质量。 （越高越好；更高表示真实物品不仅更常进入前 $K$，而且通常处于更靠前的位置。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RQ1：三个数据集上的推荐列表质量

<div class="result-value" markdown="1">

作者报告 SelfDR 在 Clothing、Home 和 ML1M 的全部列表指标上均优于表中最佳基线，并以星号标记相对最佳基线达到 $p<0.05$。例如，SelfDR 的 $H_l@1$ 分别为 0.0132、0.0148 和 0.0845；对应的最佳基线分别为 0.0114、0.0142 和 0.0753。其优势也延伸至较大截断位置，例如 $N_l@5$ 分别达到 0.0228、0.0245 和 0.1437。

</div>

这说明 SelfDR 的收益不只体现在直接猜中第一项，也体现在利用 token 对数概率形成的候选列表中，并且跨稀疏电商数据与较密集电影数据保持一致。由于所有 LLM 方法使用相同的 8B 骨干，该结果较有力地支持训练框架本身有效。不过，它不能单独证明 SelfDR 对任何召回器或更大候选集都同样有效，因为实验固定使用 SASRec 的前 20 个候选；此外，部分推理基线使用外部闭源模型生成标签，训练资源并非完全同构。

<div class="result-source" markdown="1">

来源：第 4.2.1 节，表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 2, our method consistently achieves significantly better performance across all metrics than both traditional and LLM-based recommenders on all three datasets.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### RQ1：直接生成的 Top-1 准确率

<div class="result-value" markdown="1">

SelfDR 在 Clothing、Home 和 ML1M 上的 $H_g@1$ 分别为 0.0118、0.0136 和 0.0735，均为表 3 的最高值并带有 $p<0.05$ 标记。作为对照，RecR1 在三个数据集上分别为 0.0114、0.0128 和 0.0515；这表明 SelfDR 的改进并非仅来自事后按 token 概率重排。

</div>

该结果检验学生模型能否直接生成正确物品，而不是先输出多个候选或借助测试时理由。SelfDR 在三个领域均领先，支持“训练时利用理由、推断时直接推荐”的核心主张。需要注意，$H_g@1$ 只评价单个最终输出，不反映候选列表的整体顺序、多样性或校准程度；同时其绝对值仍较低，部分原因是正样本不保证出现在基础排序器给出的 20 个候选中。

<div class="result-source" markdown="1">

来源：表 3，SelfDR（Ours）完整数据行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

SelfDR (Ours) 0.0118* 0.0136* 0.0735*

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### RQ2：不同 Reasoner 构造的教师在 Clothing 训练样本上的表现

<div class="result-value" markdown="1">

在 Clothing 随机抽取的 2,000 个训练实例上，使用 SelfDR 训练后的 LLaMA Reasoner 构造教师时，$H_g@1$、$H_l@1$、$H_l@3$、$N_l@3$、$H_l@5$ 和 $N_l@5$ 分别为 0.552、0.615、0.910、0.7908、0.968 和 0.8151，全部高于表中未经任务训练的 LLaMA 以及 GPT-4o-Mini、Claude-3-Haiku、DeepSeek-V3、GPT-5-Chat。相比蒸馏前学生的 $H_g@1=0.373$，教师达到 0.552。

</div>

该对比隔离了“谁来生成理由”的影响：更大的通用模型不必然产生更适合该学生和推荐任务的监督，而由同一基础模型经下游奖励训练出的 Reasoner 可能生成更任务定向、也更容易被学生学习的理由。这里测量的是训练样本上的教师质量，并非独立测试集上的最终泛化；虽然作者称图 3 中蒸馏后测试趋势一致，但节选未提供图 3 的具体数值，因此不能据此量化 SelfDR Reasoner 相对各外部 LLM 的测试集优势。

<div class="result-source" markdown="1">

来源：表 4，Ours（trained LLaMA）完整数据行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Ours (trained LLaMA) 0.552 0.615 0.910 0.7908 0.968 0.8151

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 给定节选未提供图 3 的具体数值、表 6 的消融结果以及 RQ4 的训练成本和推理效率结果。因此只能核验“训练后 Reasoner 在表 4 的抽样训练集上最好”，不能量化其蒸馏后测试优势，也不能验证摘要所称的效率收益或动态加权贡献。
- 实验范围存在外推边界：重排序固定依赖 SASRec 的前 20 候选，所有主要 LLM 实验仅使用 LLaMA-3.1-8B-Instruct；教师分析又只抽取 Clothing 的 2,000 个训练实例。由此尚不能确定结论是否适用于其他召回器、更大候选集、其他骨干规模或完全不同的数据领域。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 传统重排序器：以 PRM、SetRank、MIR 为 ID-based 方法，以 BGE、Jina 为 content-based 方法。前者主要利用协同交互和候选间关系，后者利用文本语义；这组比较用于判断 SelfDR 的收益是否超过专门设计的非生成式重排序模型，而不只是超过基础召回排序器。
- 直接推荐式 LLM：ZSRanker 直接以零样本提示完成推荐，SOFT 则通过自优化微调和模型生成的课程数据增强训练。二者不要求测试时显式生成多步理由，因此是评估 SelfDR 是否能在同类直接推断形式下获得更高准确率的关键参照。
- 多步推理式方法：EXP3RT 根据评论构建画像、生成推理并预测评分，COT4Rec 使用外部 LLM 生成的分析标签训练推荐模型。这组基线检验 SelfDR 的任务定向、自生成理由是否优于依赖外部推理标签或评分式重排序的方案。
- 推理并推荐式方法：RecSAVER 在测试时一次生成理由和预测，RecR1 使用推荐反馈通过强化学习直接优化生成。这组比较尤其重要，因为它们也试图利用推理提升推荐，但仍需在推断阶段输出推理轨迹；SelfDR 的目标是把这类推理收益压缩到无需生成理由的学生推荐器中。

**实验想回答的问题**

- RQ1：SelfDR 相比传统重排序模型、直接推荐式 LLM 方法以及显式推理式 LLM 推荐方法，能否同时提高推荐列表质量与首项生成准确率？
- RQ2–RQ4：SelfDR 自训练的 Reasoner 和自蒸馏机制是否确实提供有效监督，以及这种设计能否在避免推理时生成理由的同时保持较好的训练与推理效率？其中给定节选完整覆盖了 Reasoner 对比，但未给出效率实验和自蒸馏消融表的完整结果。

**实验实现**

实验采用重排序协议：先由 SASRec 为每个样本产生前 20 个候选，正样本不保证位于候选集内；这比从随机负例组成的小候选集上排序更接近实际推荐，但最终指标也同时受基础候选生成器的召回上限约束。所有 LLM 推荐器统一使用 LLaMA-3.1-8B-Instruct，COT4Rec、EXP3RT 和 RecSAVER 所需的外部理由标签由闭源 DeepSeek-V3 生成；结果取三个随机种子的平均值。传统 ID-based 基线通过 ReChorus 实现。

SelfDR 将训练数据按时间分成前后两半：较早一半训练 Reasoner，较晚一半执行蒸馏，以降低在同一实例上生成教师信号并训练学生所造成的信息泄漏风险。蒸馏前先进行三个 epoch 的指令微调，随后最多训练三个蒸馏 epoch，并使用 early stopping；候选数为 20，动态加权所用阈值设为 $k=5$。Reasoner 对比还使用 GPT-4o-mini、Claude-3-Haiku、DeepSeek-V3、未经任务训练的 LLaMA-3.1-8B-Instruct，并补充观察 GPT-5-Chat。教师训练集分析因计算成本仅在 Clothing 随机抽取的 2,000 个样本上进行。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| RQ3：去除或替换自蒸馏目标，包括 Before SD、Sup-Only、Dist-Only 与固定 $[0m\alpha=0.5$ | 实验设计分别考察：完全不做自蒸馏、只使用交叉熵监督、只使用知识蒸馏损失，以及关闭动态加权并固定 $[0m\alpha=0.5$。给定节选在表 6 标题处被截断，未包含各设置的数值或完整结论，因此原文未明确报告可供核验的消融变化幅度。 | Before SD 用于判断蒸馏阶段整体是否必要；Sup-Only 与 Dist-Only 分别隔离真实标签监督和教师软监督的作用；固定 $[0m\alpha$ 则检验动态权重是否比简单的等权混合更有效。所有蒸馏设置保持训练 epoch 数一致，有助于排除训练步数差异，但在缺少表 6 数据时，不能判断哪个组件贡献最大，也不能声称动态加权显著优于固定权重。 | 第 4.4.1 节；表 6 数值未包含在给定节选中<br><span class="experiment-evidence">For all settings involving self-distillation, we keep the number of training epochs consistent to ensure a fair comparison.</span> |

**定性案例**

- 表 5 比较同一 Clothing 样本的理由：未经训练的 LLaMA 能概括“时尚、实用、可能作为礼物”等一般偏好，却没有突出与目标物品最相关的信号；Claude 更好地连接历史与下一物品，但遗漏送礼意图；训练后的 SelfDR Reasoner 同时指出功能性、日常穿着和可能为年轻亲友购买。作者据此主张其理由更有针对性且信息更丰富。分析上，这个案例与表 4 的教师性能方向一致，但它只是单个经选择的样本，不能证明所有生成理由都更忠实，也没有独立人工标注者、一致性统计或自动理由质量指标。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work distills reasoning-enhanced LLM predictions into direct, efficient recommendations, making both recommendation and reasoning-based supervision central.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`aa68f9d36e8320468612f17af3d96e9b3230f6141bac1a6e37e05c64012d2536`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
