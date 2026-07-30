---
title: "[论文解读] UniVA: Unified Value Alignment for Generative Recommendation in Online Advertising at Tencent"
description: "[arXiv 2605.05803][推荐系统] UniVA针对生成式广告推荐中“生成概率不等于广告效用”的矛盾，将商业价值一致地注入语义标识构造、自回归解码与在线服务三个阶段。"
arxiv_id: "2605.05803"
announcement_date: "2026-07-30"
primary_category: "recommender"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:04.427388+00:00"
source_sha256: "c43fd9cfb341f264042cf7adee7cd98fdfd50980de36b91c1a770c33940f352e"
tags:
  - "推荐系统"
  - "生成式推荐"
  - "在线广告"
  - "语义 ID"
  - "商业价值对齐"
  - "自回归解码"
  - "eCPM"
  - "请求约束检索"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">推荐系统 · arXiv 2605.05803</p>

# UniVA: Unified Value Alignment for Generative Recommendation in Online Advertising at Tencent

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Xinxun Zhang, Yuling Xiong, Yangru Huang, Jiale Zhou, Zhengkai Guo, Zhennan Pang, Junbang Huo, Jingwen Wang, Xuyang Sun, Enming Zhang, Jiaguang Jin, Changping Wang, Yi Li, Jun Zhang, Xiao Yan, Jiawei Jiang, Jie Jiang</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2605.05803v2) · [PDF 下载](https://arxiv.org/pdf/2605.05803v2) · **关键词** 生成式推荐, 在线广告, 语义 ID, 商业价值对齐, 自回归解码, eCPM, 请求约束检索  


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

UniVA针对生成式广告推荐中“生成概率不等于广告效用”的矛盾，将商业价值一致地注入语义标识构造、自回归解码与在线服务三个阶段。

**不用术语来说**：生成式推荐像写句子一样逐步生成广告编号，但最容易被模型生成的广告不一定最有商业价值：一些出价高、预期收益高且符合当前请求条件的广告，可能因为早期编号生成概率较低而被提前淘汰；与此同时，不符合库存或定向条件的广告还可能占用有限的搜索名额。因此，系统需要在生成过程中就兼顾用户兴趣、商业收益和请求有效性，而不能等候选广告生成完毕后再补做价值排序。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将生成式广告推荐中的价值不一致明确分解为三个相互衔接的环节：语义中心的SID表示难以区分商业价值，概率主导的逐步解码会过早剪除高价值路径，请求无关的检索又会把搜索资源浪费在无效路径上；据此提出覆盖完整流水线的统一价值对齐框架。
- 作者提出语义—商业分层的CSID表示，并把SID解码改造为生成与价值排序的联合决策，再通过请求专属的有效路径前缀树约束在线搜索，使商业价值能够在候选路径被剪枝之前介入，同时过滤不满足库存或定向条件的分支。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

生成式推荐（Generative Recommendation, GR）把目录中的每个物品编码为一串离散的语义 ID（SID），再根据用户及其历史行为，以自回归方式逐 token 生成下一个物品，从而在同一框架中完成用户建模、候选生成与物品检索。该范式通常默认 SID 路径的生成概率与推荐效用一致，但在线广告还需同时考虑相关性和商业回报；广告的出价、ROI 目标和预期千次展示收益等因素会使“最可能生成的广告”不等于“商业效用最高的广告”。此外，每次请求受库存、定向和素材规则约束，可投放广告集合会动态变化，因此生成过程还必须避免把有限的搜索容量浪费在当前请求无效的 SID 路径上。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**语义 ID（Semantic ID, SID）**

SID 是将一个广告表示为固定长度离散 token 序列的标识，通常由残差量化等方法按从粗到细的语义层次构造。内容相似的广告往往共享较长前缀，但纯语义 SID 未必能区分出价或商业目标不同的广告。

</div>
<div class="conceptitem" markdown="1">

**自回归生成与束搜索（Beam Search）**

模型在给定请求和已生成前缀后逐步预测下一个 SID token，并将各步条件概率相乘得到完整路径的生成概率。束搜索每一步只保留有限数量的高分前缀，因此早期概率较低但最终商业价值较高的广告可能被永久剪枝。

</div>
<div class="conceptitem" markdown="1">

**广告商业价值与 eCPM**

广告商业价值不仅由用户相关性决定，还受出价、优化目标、ROI 约束及预估转化效果影响；eCPM 表示每千次展示的预期收益，可作为完整广告路径的终局回报。本文还学习 token 级动作价值，以预测选择某个前缀扩展后可能获得的下游商业回报。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一次广告请求 x=(u,c,\mathbf{x}_{1:T})，其中包含用户 u、请求上下文 c 和长度为 T 的历史交互序列，系统需要生成某个广告 i 对应的长度为 L 的 SID 序列 s_i=\Phi(i)。生成策略按 \pi_\theta(y\mid x)=\prod_{l=1}^{L}\pi_\theta(a_l\mid x,s_{<l}) 对完整轨迹 y=(a_1,\ldots,a_L) 建模；但在线输出还必须属于请求特定的可行集合 \mathcal{Y}(x)，该集合由库存、定向与素材约束确定。任务目标不是单纯选择生成概率最高的路径，而是在保留监督式下一 SID 预测能力的同时，使可行轨迹获得更高的终局 eCPM，并利用请求条件化的 token 级价值估计辅助前缀选择。该设定隐含三个需要贯通处理的环节：SID 空间应体现商业差异，解码时商业价值应在高价值路径被剪枝前介入，服务时则应只搜索当前请求有效的路径。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$x=(u,c,\mathbf{x}_{1:T})$**

一次广告请求；u 为用户，c 为请求上下文，\mathbf{x}_{1:T} 为用户的历史交互序列。

</div>
<div class="notationitem" markdown="1">

**$s_i=\Phi(i)=(s_i^1,\ldots,s_i^L)$**

广告 i 经映射函数 \Phi 得到的长度为 L 的 SID 序列，s_i^l 是第 l 层 token。

</div>
<div class="notationitem" markdown="1">

**$\pi_\theta(y\mid x)=\prod_{l=1}^{L}\pi_\theta(a_l\mid x,s_{<l})$**

参数为 \theta 的自回归生成策略；y 是完整 SID 轨迹，a_l 是第 l 步动作，s_{<l} 是此前已生成的前缀。

</div>
<div class="notationitem" markdown="1">

**$q_\phi(s_{<l},a;x)$**

参数为 \phi、以请求 x 为条件的 token 级动作价值函数，估计在前缀 s_{<l} 后选择候选 token a 所带来的下游商业回报。

</div>

</div>

**直接相关的工作**

- **RQ-based Semantic ID generative recommendation（Rajput et al., 2023；Hou et al., 2023）**: 这类方法以残差量化构造从粗到细的语义 token，并把推荐转化为 SID 自回归生成，是本文问题设定的直接基础；其 SID 主要保存语义相似性，未显式暴露广告之间的商业价值差异。
- **生成式广告推荐系统 GPR、EGA-v2 与 GR4AD（Zhang et al., 2025；Zheng et al., 2025；Xue et al., 2026）**: 这些工作已通过业务监督、拍卖信号或价值导向目标证明商业信息对生成式广告推荐的重要性，但相关机制通常只作用于训练或推理的局部阶段；本文所针对的缺口是 SID 表示、前缀级解码和请求约束服务之间缺少一致的价值对齐。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

工业广告推荐不仅要判断用户是否相关，还要考虑广告主出价、投资回报目标、预期千次展示收益等商业因素，并遵守当前请求下动态变化的库存与定向约束。传统生成式推荐按SID路径的生成概率选择候选，隐含假设“更可能生成”就意味着“更值得推荐”；在广告场景中，该假设不成立，因而可能直接损害候选质量与平台商业收益。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **语义SID驱动的生成式推荐**：先依据广告内容的语义相似性，把每个广告编码为离散的语义标识序列SID；模型根据用户历史逐个预测SID词元，并利用束搜索保留累计生成概率较高的路径，最终由完整路径定位广告。
- **局部价值感知的生成式广告推荐**：已有方法把拍卖信号、商业侧监督或价值目标加入某个训练或推理环节，常见做法包括辅助损失、样本重加权以及局部的价值感知分数调整，以提高模型对商业收益的敏感度。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 语义SID主要按内容相似性组织广告，可能把内容近似但出价、ROI目标或转化价值明显不同的广告映射到相邻路径，导致标识空间缺少商业区分度；后续解码因此难以仅凭路径结构识别更有价值的广告。
- 现有价值信号通常只作用于单个阶段，整体流程仍以生成概率为中心：高价值广告若早期前缀概率较低，会在束搜索中被不可逆地剪除；此外，全局路径搜索不考虑当前请求的库存与定向资格，无效分支会消耗有限的计算量和束宽，使有效高价值广告无法进入最终候选集。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种贯穿“广告如何被编码、路径如何被逐步选择、线上搜索允许扩展哪些路径”的统一机制。尚未解决的关键缺口不是单纯增加一个商业价值损失，而是让价值信息在每个可能造成候选丢失的环节都保持一致，并在高价值路径被剪枝之前发挥作用。

</div>
<div markdown="1"><span>核心问题</span>

如何在不依赖生成后独立价值模型或额外重排器的情况下，把用户相关性、商业回报与请求有效性共同纳入生成式广告推荐的逐词元决策，使高价值且符合请求约束的广告路径能够被保留并优先生成？

</div>
<div markdown="1"><span>作者直觉</span>

一条广告SID路径类似一条逐岔路选择的路线：若地图只记录内容语义，价值不同的广告会挤在相似路线中；若每个岔口只看“最常走”的概率，潜在收益高但暂时不热门的路线会过早消失；若还允许走入当前请求下不可用的道路，有限搜索名额又会被浪费。因而，可以在SID末层编码商业差异，在每次扩展时同时参考生成概率和预期商业回报，并用请求专属前缀树封闭无效道路，从表示、决策到服务连续保护有价值的候选。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

UniVA把广告生成推荐视为“在约束条件下逐层生成并排序语义ID（SID）路径”的统一问题，端到端流程覆盖表示、训练、解码和在线投放。首先，CSID Tokenization在原有语义层级末端加入由商业属性与相对出价共同决定的商业token；随后，共享主干的双头解码器同时输出下一token的生成logit与动作价值；训练时交替使用监督学习和以eCPM为终局奖励的强化学习，并通过束搜索与价值引导MCTS收集轨迹；服务时融合生成分数和动作价值，再用请求特定的合法路径trie屏蔽不可投放分支，最终在叶节点广告桶中按出价选出具体广告。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造语义—商业联合ID（CSID）

上层SID沿用RQ-KMeans+语义 tokenizer；末层先压缩长尾商业属性，再以压缩后的“优化目标—ROI—行业”组成商业上下文键，并在每个键内按出价分位数做等频分箱。各键的分箱数量在总词表预算和上下界约束下按最大化商业token熵进行分配，未见键和低支持键映射到回退键。

<div class="method-step__io" markdown="1">

**输入**：广告的语义特征、优化目标、ROI目标、行业类别和出价，以及商业token词表预算。  
**输出**：长度为L的CSID路径：前L-1层表达由粗到细的语义结构，第L层同时表达商业上下文和该上下文内的相对出价水平。

</div>

**直观理解**：普通SID主要回答“这是什么广告”，CSID还在路径末端标记“它处于什么经营条件、出价大致有多高”。等频分箱和回退键用于避免少量稀疏属性组合各自占用一个几乎学不到规律的token。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 编码请求并产生双头token分数

HSTU编码器将User、Organic、Environment和Item四类token编码为上下文状态；自回归解码器通过跨注意力读取请求上下文、通过因果自注意力建模SID前缀，并结合稀疏MoE与递归参数共享获得隐藏状态。共享隐藏状态分别送入生成头和动作价值头，前者给出下一token策略，后者估计选择各token后的预期商业回报。

<div class="method-step__io" markdown="1">

**输入**：用户属性与偏好、自然内容行为、当前请求环境、历史广告交互，以及已经生成的CSID前缀。  
**输出**：每个SID层级上的生成logit、生成策略πθ，以及对全部候选token的动作价值qφ。

</div>

**直观理解**：两个输出分别回答“这个token与用户和前缀有多匹配”以及“选它预计能带来多少商业收益”。它们共享对用户和广告序列的理解，但承担不同决策职责。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 联合监督学习与eCPM强化学习

监督交叉熵使策略维持合法且与用户相关的SID生成；强化学习把请求内归一化的终局eCPM反馈用于PPO策略更新，并以token级回报目标回归动作价值。训练按批次交替执行监督更新和强化学习更新，更新后的价值头再用于下一轮MCTS轨迹探索。

<div class="method-step__io" markdown="1">

**输入**：带目标CSID的监督样本，以及由旧策略束搜索和价值引导MCTS收集、经离线模拟器评估的完整CSID轨迹。  
**输出**：兼顾生成相关性与商业回报的共享解码主干、生成头和动作价值头。

</div>

**直观理解**：监督学习先保证模型“会沿正确路径生成”，强化学习再告诉它哪些完整路径更值钱。交替训练可降低模型为了短期商业奖励而偏离有效SID结构的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Generation-as-Ranking分数融合

对每个候选token，将生成logit与经αl校准的动作价值相加，形成GAR融合logit。αl=0时退化为仅使用强化学习后的生成策略，αl>0时商业价值可直接改变token之间的排序。

<div class="method-step__io" markdown="1">

**输入**：当前请求和SID前缀对应的生成logit、动作价值，以及在验证集上选定的各层融合系数αl。  
**输出**：同时反映用户相关性、路径兼容性与预测商业回报的下一token排序分数。

</div>

**直观理解**：这一步不是生成结束后再运行一个独立排序器，而是在每次扩展路径时就把“像不像正确答案”和“值不值得投放”合成一个分数。因而高价值分支能更早获得束搜索容量，而不是在前几层被纯似然剪掉。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="equation-block" markdown="1">

#### Generation-as-Ranking逐token融合

$$
\ell_{\mathrm{GAR}}^{(l)}[a]=o_{\mathrm{gen}}^{(l)}[a]+\alpha_l q_{\phi}(s_{<l},a;x),\qquad a\in\mathcal{S}_l
$$

**符号说明**

- $\ell_{\mathrm{GAR}}^{(l)}[a]$：SID第l层候选token a的融合排序logit。
- $o_{\mathrm{gen}}^{(l)}[a]$：生成头对候选token a输出的未归一化生成分数，主要表示请求相关性和与既有SID前缀的兼容性。
- $\alpha_l$：第l层非负价值校准系数，在留出验证数据上选择，并在在线服务中固定。
- $q_{\phi}(s_{<l},a;x)$：参数为φ的动作价值头对“请求x下，在前缀s<l后选择a”所预测的后续商业回报。
- $s_{<l}$：第l层之前已经生成的SID token前缀。
- $\mathcal{S}_l$：SID第l层的候选token词表。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把每次自回归生成改写为一次候选token排序：生成分数保证路径与用户及前缀相符，动作价值使高预期商业回报的分支获得额外优先级。它是训练得到的价值估计进入在线决策的直接接口。  
**原文位置**：第3.2节，公式(16)

</div>

</div>

<div class="equation-block" markdown="1">

#### 交替监督—强化学习目标

$$
\begin{aligned}\mathcal{L}_{\mathrm{SL}}&=-\sum_{(x,s^{\star})\in\mathcal{D}_{\mathrm{SL}}}\sum_{l=1}^{L}\log\pi_{\theta}(s_l^{\star}\mid x,s_{<l}^{\star}),\\ \mathcal{L}_{\mathrm{RL}}&=\mathcal{L}_{\mathrm{PPO}}+\lambda_v\,\mathbb{E}\!\left[\left(q_{\phi}(s_{<l},a_l;x)-\widehat{G}_l\right)^2\right],\\ \mathcal{L}_{\mathrm{train}}&=\mathbb{I}_{\mathrm{SL}}\mathcal{L}_{\mathrm{SL}}+\mathbb{I}_{\mathrm{RL}}\mathcal{L}_{\mathrm{RL}}.\end{aligned}
$$

**符号说明**

- $\mathcal{D}_{\mathrm{SL}}$：监督训练集，其中每个样本包含请求x和目标CSID序列s★。
- $\pi_{\theta}$：参数为θ的自回归生成策略。
- $L$：完整CSID的token层数。
- $\mathcal{L}_{\mathrm{PPO}}$：利用终局eCPM反馈优化生成策略的PPO策略损失；具体裁剪形式位于原文附录B。
- $\lambda_v$：动作价值回归项的权重。
- $\widehat{G}_l$：由请求内归一化终局奖励导出的、第l步固定回报目标。
- $q_{\phi}(s_{<l},a_l;x)$：价值头对轨迹第l步实际动作al的预测回报。
- $\mathbb{I}_{\mathrm{SL}},\mathbb{I}_{\mathrm{RL}}$：当前批次分别属于监督学习批次或强化学习批次的指示量。

<div class="equation-explanation" markdown="1">

**直观理解**：第一行训练模型复现有效且相关的目标SID，第二行一方面用PPO把商业奖励传给生成策略，另一方面让价值头拟合每个前缀动作的回报。第三行表示两类批次交替而非简单同时混合，从而兼顾生成稳定性和商业价值对齐。  
**原文位置**：第3.3节，公式(17)、(19)、(20)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练前固定CSID映射。监督批次通过逐token负对数似然更新共享解码主干和生成头，使模型掌握合法路径及用户相关性；强化学习批次由冻结的旧策略πold和旧价值函数qold收集轨迹，其中束搜索覆盖行为策略偏好的高概率路径，MCTS额外探索价值较高但生成概率可能较低的前缀。完整轨迹经近期生产快照构建的离线模拟器解析到具体广告并获得eCPM，奖励在同一请求内归一化后构造优势和token级回报目标；PPO更新生成策略，均方回归更新动作价值头，二者均可更新共享表示。作者选择PPO而非critic-free的GRPO，是因为显式学习的同一个动作价值头可同时充当PPO基线来源、离线MCTS启发函数和在线GAR排序信号；监督与强化学习批次交替执行，以抑制只追逐终局收益造成的生成漂移。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Commercial SID Tokenization（CSID Tokenization）**

该模块保留语义SID的上层层级，仅把最后一层定义为商业token。商业属性先独立压缩，再组成上下文键；稀有键合并至回退键，各键按样本占比分配有限数量的出价等频分箱，使token既有商业区分度又有足够训练支持。

> 直观理解：如果两个广告语义相近但经营目标或出价明显不同，纯语义ID可能把它们放在同一路径中，模型难以在早期区分价值。CSID显式把这种差异写入生成空间，同时用压缩和共享回退类别控制词表膨胀。

**2. Generation-as-Ranking双头解码器**

解码主干以HSTU编码结果为条件，使用跨注意力和因果自注意力生成SID；稀疏MoE每个token仅激活top-K专家，并保留始终激活的共享专家，MoR式递归共享则在固定递归预算内重复中间变换。主干上设置生成头fgen和动作价值头fvalue，在线直接融合二者输出，而无需额外的后置排序模型。

> 直观理解：共享主干避免为相关性和价值分别运行两套完整模型；双头又使两种信号不会被迫解释成同一个概率。MoE增加面对不同广告经营模式时的条件容量，递归共享则以较少独立参数获得更深计算。

**3. Value-Aware Constrained Serving**

全局trie存储服务创意库的完整CSID路径和叶节点广告桶，请求到来后按定向、广告状态及创意规则得到个性化子trie。非法token的logit被置为负无穷，合法分支按GAR掩码分布的累计对数概率做束搜索；叶节点使用与离线奖励模拟一致的出价优先解析器。

> 直观理解：纯束搜索可能把名额浪费在当前用户不可投、预算已耗尽或违反频控的路径上。硬约束先保证每条保留路径能落到广告，价值融合再决定这些合法路径中谁应排在前面。

**训练与推理**

离线阶段先从广告语义特征、商业属性和出价构建固定CSID；随后以用户、自然内容、环境和历史广告交互编码请求，并用监督样本训练生成策略。进入联合训练后，每轮先冻结当前策略和价值头作为行为快照，通过束搜索与MCTS组成候选轨迹集合；轨迹经确定性的“合法广告桶内最高出价”规则解析并由模拟器产生eCPM奖励，再交替执行PPO、价值回归和监督生成更新。MCTS与模拟器只用于离线训练。
在线阶段不运行MCTS，也不调用独立价值模型或全局生成后重排。系统从每日更新的创意服务库建立全局CSID trie，再根据当前请求执行定向、预算与状态、频控、去重和合规过滤，得到只含可投放路径的个性化trie；双头解码器逐层计算GAR融合logit，非法动作以负无穷掩码移除，合法前缀按累计对数概率执行束搜索。到达叶节点后，从非空的请求合法广告桶中按出价优先选出具体广告，因此过滤、SID生成和价值排序在一次受约束自回归搜索中完成。

**复现信息**

公平理解或复现该方法所需的关键设定包括：商业属性压缩必须保留高频值并合并长尾值，低支持商业组合统一进入回退键；各商业键的出价箱采用键内经验分位数等频划分，箱数受总商业token词表预算V、每键最小箱数bmin和最大箱数bmax约束。动作价值头必须输出当前SID层全部候选token的词表级价值，才能被MCTS和在线GAR共同复用；各层αl应仅在留出验证数据上校准并在服务时固定。在线trie建立在按日刷新的创意级抽样服务库上，叶桶只有在与当前请求合法库存求交后为空才删除；最终广告解析规则在离线奖励模拟与在线服务中保持一致。原文节选未给出具体词表预算、属性压缩阈值、束宽、MCTS预算、专家数量、激活专家数、递归次数、PPO超参数或αl数值，这些信息需结合附录及完整论文核验。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- Amazon Reviews的Industrial_and_Scientific（Industrial）子集：公开序列推荐基准，用于检验方法在非广告场景中的泛化。该场景采用语义SID，以评分所表达的用户效用作为价值监督，不使用广告专属CSID。原文未明确报告样本规模、数据划分与预处理细节。
- Amazon Reviews的Office_Products（Office）子集：第二个公开序列推荐基准，作用与Industrial相同，用于避免结论仅来自单一品类。原文未明确报告样本规模、数据划分与预处理细节。
- 腾讯大规模广告数据集及线上微信视频号流量：离线数据包含广告与自然内容混合流量、会话级用户行为和多模态物品特征，用于评估完整UniVA，包括CSID、eCPM对齐解码及GMV加权的下一转化集合；线上A/B测试于2026年3月7日至11日在20%生产流量上开展，平台覆盖数亿活跃用户和数千万动态广告。离线样本量及训练、验证、测试划分原文未明确报告。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**HR@K**

Hit Rate@K，判断真实下一交互物品是否出现在前K个候选中；公开数据报告K∈{3,5,10}，工业数据还重点报告HR@100。它主要衡量候选召回覆盖，而不直接衡量候选的商业价值或前K内部排序质量。 （越高越好，因为真实下一物品被召回的比例更高。）

</div>
<div class="metricitem" markdown="1">

**NDCG@K／wNDCG@K**

NDCG@K对命中位置进行折损，正确物品排得越靠前得分越高；wNDCG@K用于GMV加权的下一转化集合，并进一步强调高价值转化的排序质量。 （越高越好，因为相关物品，尤其是高商业价值转化，被排在更靠前的位置。）

</div>
<div class="metricitem" markdown="1">

**ValueHR@K／线上GMV指标**

ValueHR@K衡量Top-K候选覆盖了多少转化价值；线上GMV Lift与GMV(normal) Lift则报告相对同一生产基线的成交总额提升。原文节选未给出GMV(normal)的精确定义，其正式定义位于附录F.3。 （越高越好，因为候选覆盖的商业价值或线上实际成交额更大。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 两个Amazon公开序列推荐基准，与传统、生成式及LLM推荐基线比较

<div class="result-value" markdown="1">

UniVA在所有已报告指标上排名最佳；相对各指标最强基线的提升范围为1.5%至8.4%。Industrial上的最大相对提升为HR 2.9%、NDCG 3.0%，Office上的对应最大提升为HR 8.4%、NDCG 7.8%。

</div>

作者据此主张，价值感知解码不仅适用于广告eCPM，也能迁移到以评分表示用户效用的普通推荐场景。分析上，这支持方法具有跨场景适用性，且Office上的收益更明显；但节选未提供表1的绝对分数、方差或显著性检验，因此不能据此判断实际命中率增量的绝对大小，也不能排除不同复现实验设置造成的影响。

<div class="result-source" markdown="1">

来源：第4.2节 Public Benchmark Results，表1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">UniVA achieves the best performance across all reported metrics, with relative improvements ranging from 1.5% to 8.4% over the strongest baseline for each metric.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 腾讯工业广告离线基准，完整UniVA相对GPR+SID Decoder基础系统

<div class="result-value" markdown="1">

完整UniVA达到HR@100相对提升37.04%，解码器规模为80M参数、23.2G推理FLOPs；基础系统为3M参数、4.1G FLOPs。该结果汇总了CSID、扩容解码、eCPM感知强化学习和完整配置的共同作用。

</div>

结果说明，把商业价值同时写入SID表示、前缀决策学习和解码选择，可显著提高真实下一交互物品进入前100候选的概率。不过这是完整系统相对基础系统的联合增益，同时伴随约26.7倍参数量和约5.7倍解码FLOPs增长，不能将37.04%全部归因于价值对齐，也不能由HR@100单独证明GMV必然提高。

<div class="result-source" markdown="1">

来源：表2，Offline HR@100 ablation on the industrial advertising benchmark

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">UniVA (Full) | 80M | 23.2G | +37.04%</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 腾讯微信视频号生产广告流量线上A/B测试，V3完整UniVA相对同一生产基线

<div class="result-value" markdown="1">

在2026年3月7日至11日、20%生产流量上，完整UniVA带来1.50%的GMV提升和1.42%的GMV(normal)提升，优于V0、V1和V2三个逐步版本。

</div>

这是最直接的业务证据：离线价值对齐最终转化为真实成交额提升，而且无需另设线上重排器。由于V3同时把GRPO替换为PPO动作价值学习并启用Generation-as-Ranking，该结果证明的是最终组合方案有效，而不是单独某一项的因果贡献；节选也未给出置信区间、显著性、用户体验或广告主侧长期指标。

<div class="result-source" markdown="1">

来源：第4.5节 Online GMV Results，表4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Full UniVA achieves the strongest performance, with a 1.50% GMV lift and a 1.42% GMV(normal) lift.</span>

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

- 传统序列推荐器GRU4Rec、Caser和SASRec：代表基于循环网络、卷积网络和自注意力的判别式序列建模，用于判断生成式方案是否优于成熟的非生成式推荐方法。
- 生成式推荐器HSTU、TIGER和LCRec：与UniVA同属序列或SID生成路线，是检验其价值感知解码是否超越常规生成建模的直接参照。
- LLM推荐器BIGRec、D3、S-DPO和MiniOneRec：代表大模型生成、偏好优化等近期方法，用于比较UniVA与更强生成式基线在公开数据上的效果。
- 工业基线GPR加普通decoder-only Transformer SID解码器：GPR已通过价值感知训练和解码引入商业信号，因此是比纯相关性模型更严格的工业对照；实验在该基础上逐步加入CSID、解码器结构、强化学习和完整UniVA。

**实验想回答的问题**

- UniVA能否在公开序列推荐数据与腾讯工业广告数据上同时提高下一物品命中能力，并将广告商业价值有效纳入SID构造、自回归解码和在线服务，而不只优化生成概率？
- CSID、解码器扩容、eCPM感知强化学习、Generation-as-Ranking及个性化Trie约束分别解决什么问题，它们的收益是否能从离线指标延伸到真实线上GMV？

**实验实现**

公开基准报告HR@K和NDCG@K（K为3、5、10）；工业基准报告下一物品预测HR@K，并在GMV加权的下一转化集合上报告ValueHR@K和wNDCG@K。表2采用逐步累加配置，参数量与推理FLOPs只计算SID解码器、不含编码器；完整UniVA增加MoR递归预算，并将稀疏MoE从16个专家、Top-4激活扩展至64个专家、Top-16激活。Trie实验固定融合评分器和beam width=300，对比“全局beam search后过滤无效路径”与“在个性化Trie中只扩展请求有效路径”。线上四个版本均相对同一生产基线：V0为语义SID+GRPO，V1扩容解码器，V2加入CSID，V3改用基于PPO的动作价值学习并启用Generation-as-Ranking。除这些信息外，优化器、随机种子、置信区间、离线划分及显著性检验在所给节选中未明确报告。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 工业离线渐进消融：在Sparse MoE配置上加入eCPM-aware RL与Generation-as-Ranking | HR@100相对基础系统的提升由18.40%增至32.01%，增加13.61个百分点；参数从60M增至62M，FLOPs均为8.5G。 | 该对比在计算量基本不变的条件下，主要隔离终局商业反馈、前缀动作价值学习及其在解码中的复用。明显增益支持作者的核心判断：仅靠监督式下一SID学习不足以保留商业潜力较高的路径。不过表2把eCPM-aware RL和Generation-as-Ranking作为一个配置报告，无法进一步拆分训练目标与融合解码各自的贡献。 | 第4.2节 Industrial Advertising Benchmark Results，表2<br><span class="experiment-evidence">The eCPM-aware RL configuration with Generation-as-Ranking decoding increases the relative HR@100 improvement from 18.40% to 32.01%.</span> |
| 个性化Trie约束服务与全局beam search后过滤的对比；相同融合评分器，beam width=300 | 后过滤方案只返回48条有效SID路径，而Trie约束方案返回300条；候选平均bid从1.29提高至11.44。 | 该实验隔离了服务阶段的路径有效性约束：Trie在展开前就排除当前请求不可投放的分支，因此无效候选不会挤占固定beam预算。它证明约束搜索能同时提升可交付候选数量和平均出价，但平均bid不是最终GMV，且节选未报告相关性、多样性、延迟或转化率变化，因而不能说明更高出价必然带来更高长期收益。 | 第4.4节 Trie-Constrained Serving Analysis<br><span class="experiment-evidence">The former returns only 48 valid SID paths, whereas the latter returns 300. The average bid also increases from 1.29 to 11.44, nearly one order of magnitude.</span> |

**定性案例**

- CSID构造策略分析显示，Classify-then-Bin配合等频分箱取得最高商业token加权熵H_tok=7.487，同时词表规模V=1939最接近2048预算。作者解释为：先按结构化商业属性分类，再在类内按出价等频切分，可避免长尾出价使少数token过密，并兼顾商业区分度与词表利用率；这是一项聚合统计分析，而非单个用户或广告的定性案例。证据：“Classify-then-Bin combined with equal-frequency binning achieves the highest weighted entropy while keeping the vocabulary size closest to the target budget of 2048, with H_tok=7.487 and V=1939.”（附录C，图5）

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向在线广告生成式推荐的价值对齐框架，联合改进语义 ID、解码排序和约束服务。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`c43fd9cfb341f264042cf7adee7cd98fdfd50980de36b91c1a770c33940f352e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
