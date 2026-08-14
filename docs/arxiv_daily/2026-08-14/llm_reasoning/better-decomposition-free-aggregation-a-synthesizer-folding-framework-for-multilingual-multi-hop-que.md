---
title: "[论文解读] Better Decomposition, Free Aggregation: A Synthesizer-Folding Framework for Multilingual Multi-Hop Question Answering"
description: "[arXiv 2608.13160][LLM Reasoning] 本文针对多语言多跳问答中“默认翻译造成噪声与成本”和“分解后独立聚合放大误差”两类结构性问题，提出按分解质量决定是否启用跨语言路径、并把最终综合写入末端子问题的 Syfer 框架。"
arxiv_id: "2608.13160"
announcement_date: "2026-08-14"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:58:33.990907+00:00"
source_sha256: "176ef399fa1238aa3a5798c82bd0274260a5c7ac878de7a1f59c7579ccdee3df"
tags:
  - "LLM Reasoning"
  - "LLM Agent"
  - "LLM 其他"
  - "多语言问答"
  - "多跳推理"
  - "问题分解"
  - "检索增强生成"
  - "大语言模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.13160</p>

# Better Decomposition, Free Aggregation: A Synthesizer-Folding Framework for Multilingual Multi-Hop Question Answering

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Yilin Wang, Yuchun Fan, Weidong Bao, Zili Wei, Shi Feng, Tong Xiao, Zhengtao Yu, Jingbo Zhu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Computer Science and Engineering, Northeastern University, Shenyang, China；Affiliation: Yunnan Key Laboratory of Artificial Intelligence, Kunming University of Science and Technology, Kunming, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13160v1) · [PDF 下载](https://arxiv.org/pdf/2608.13160v1) · **关键词** 多语言问答, 多跳推理, 问题分解, 检索增强生成, 大语言模型<br>
**代码**: [https://github.com/f6ster/Syfer](https://github.com/f6ster/Syfer)

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

本文针对多语言多跳问答中“默认翻译造成噪声与成本”和“分解后独立聚合放大误差”两类结构性问题，提出按分解质量决定是否启用跨语言路径、并把最终综合写入末端子问题的 Syfer 框架。

**不用术语来说**：回答复杂的多语言问题时，系统往往要从不同语言的多篇文档中逐步拼出答案。现有系统通常先大规模翻译材料，或把问题拆成若干小问题后再单独汇总答案；前者可能丢失原语言特有的信息并增加开销，后者则可能生成多余或不连贯的小问题，使早期错误一路累积，最后的汇总步骤又进一步放大这些错误。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出 Syfer 的“延迟翻译”策略：默认在原问题语言中分解和推理，先检查子问题图的质量，只有检查失败时才启用英语平行子问题图及双语对齐，从而把跨语言处理从固定步骤改为按需恢复机制。
- 提出“综合器折叠”设计：由受约束的分解器直接生成一个用于综合前序线索的末端子问题，以同一推理链中的问答替代独立的流水线末端聚合，使分解与综合处于统一逻辑结构中，并让分解质量可以被直接检查。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于多语言检索增强生成与多跳问答的交叉领域。检索增强生成先从外部文档集合中寻找证据，再由大语言模型依据证据作答，以降低知识密集型任务中的事实错误；多语言场景还要求系统跨越语言差异，利用分布在不同语言文档中的知识。现有系统已能较好处理只依赖单条证据的多语言单跳问题，但面对多跳问题时，必须连续检索并整合散落在多个文档、甚至多种语言中的线索。由于大语言模型的训练数据偏向英语等高资源语言，中低资源语言上的理解与推理能力较弱，因此系统通常借助翻译实现语言对齐，或把复杂问题分解为有依赖关系的子问题并逐步回答。本文研究的核心正是如何在保留跨语言知识访问能力的同时，减少无条件翻译、冗余分解和长推理轨迹带来的噪声、成本与误差传播。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多语言检索增强生成（mRAG）**

系统先从多语言文档库检索与问题有关的材料，再让大语言模型基于这些材料生成答案。它既要解决“找到哪些证据”，也要解决“问题、证据和模型擅长的语言不一致”所造成的语义差距。

</div>
<div class="concept-item" markdown="1">

**多跳问答**

答案不能由单个事实直接得到，而要连接两个或更多分散线索，例如先确定某个人物，再根据该人物查找另一项事实。每一跳的检索或回答错误都可能进入后续步骤并累积。

</div>
<div class="concept-item" markdown="1">

**问题分解与子问题图**

问题分解把复杂问题改写成若干较简单的子问题；子问题图进一步表示这些子问题之间的先后依赖关系，使后续问题能够利用先前答案。图过于冗余或逻辑不连贯时，会增加检索次数、上下文长度和误差传播风险。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入包括一种目标语言书写的复杂多跳问题，以及可能包含多种语言、信息分布不均的外部文档集合；目标输出是该问题的最终答案。系统需要在大语言模型对英语等高资源语言能力更强、证据可能散落于多个跨语言文档的条件下，完成问题分解、证据检索、逐步推理和答案综合。本文所依赖的基本假设是：并非每个问题都需要翻译或英语侧推理；若原语言中的分解质量足够好，可以直接按子问题顺序执行“先检索、后回答”，只有分解质量不合格时才值得启用英语平行路径和双语子问题图对齐。这里的“聚合”不是简单拼接已有答案，而是依据完整推理链形成最终回答。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **DaPT**: DaPT是与本文任务最接近的分解式多语言多跳问答方法：它利用问题分解构造双语推理过程，但原文指出其分解缺少约束，容易生成较长的中间上下文，并受到“中间信息遗失”现象影响。Syfer沿用分解式骨架，但增加分解格式约束与质量检查，仅在原语言分解失败时启用英语平行图，并把最终综合改写为分解器生成的终止子问题。
- **迭代检索与树/图结构检索方法**: 这类多跳RAG方法通过逐轮更新证据，或使用树、图结构引导模型寻找线索密集的文档与上下文片段。论文指出，它们通常依赖模型较强的英语理解能力；迁移到含平行文档及中低资源语言的环境时，结构化证据可能引入冗余内容并放大信息抽取噪声，因此不能直接解决本文关注的多语言分解质量与选择性翻译问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

多语言多跳问答不仅要弥补大语言模型在中低资源语言上的能力不足，还必须跨文档、跨语言收集并整合多个线索。知识在不同语言中的分布并不均匀，因此系统既不能只依赖模型内部知识，也不能假定把所有内容统一到一种语言后仍能无损保留证据；实际需求是在准确率、计算成本与延迟之间取得可用的平衡。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **翻译对齐式多语言 RAG**：先把用户问题或检索到的文档翻译成英语或查询语言，以缩小查询、证据和生成模型之间的跨语言语义差距，再基于对齐后的文本检索或生成答案。
- **分解与聚合式多跳推理**：把复杂问题拆成一组具有依赖关系的子问题，通常构成单语或双语子问题图；系统逐跳检索并回答这些子问题，最后通过一个独立的聚合调用汇总中间答案，得到原问题的最终答案。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 一刀切的翻译对齐不区分样例是否真正需要跨语言辅助：全面翻译可能删除目标语言中具有文化或语言特性的原生信息，引入会被后续模型误当作证据的翻译噪声，同时增加计算成本与延迟。作者还指出，对本来就能清晰分解的低复杂度问题，无条件加入英语平行图可能提供冗余选择，反而干扰生成器。
- 缺少约束的贪心分解容易产生冗余、逻辑不连贯的子问题，导致逐跳错误传播和累积；此外，独立于分解结构的最终聚合调用需要处理较长的中间推理轨迹，会集中而非吸收已有噪声，并在逻辑上打断原有推理链。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作分别利用翻译解决跨语言对齐、利用问题分解解决多跳推理，但尚缺少一个统一机制来判断某个样例是否确实需要跨语言路径，并同时约束分解结构、检查分解可信性，以及避免用独立的末端聚合器重新处理整条含噪推理轨迹。换言之，关键空缺不是增加更多翻译或更多推理步骤，而是让跨语言辅助具有条件性，并让分解与答案综合共享同一可验证的逻辑结构。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一种多语言多跳 RAG 框架，使其默认保留原语言证据，仅在子问题图未通过质量检查时启用英语平行分解与双语融合，同时把最终答案综合改写为分解器生成的末端子问题，从而在保持竞争性准确率的同时降低翻译噪声、误差放大和不必要的计算开销？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把英语路径视为“失败后的恢复手段”，而不是每个问题都必须支付的固定成本：如果原语言分解已经可靠，直接沿该图逐步检索和回答即可；只有分解不可信时，英语平行图才提供额外结构来纠偏。与此同时，把综合任务写成依赖前序线索的最后一个子问题，相当于让系统沿同一条受约束的推理链自然收束答案，避免另设一个聚合器重新阅读并压缩全部中间过程，因此有望减少噪声集中和推理链断裂。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

Syfer接收语言为$L$的复杂问题$Q$和多语语料库$\mathcal{C}$，最终输出答案$A$。其核心不是默认把全部问题或文档翻译成英语，也不在所有推理步骤结束后额外调用一次生成器做答案汇总，而是先用离线蒸馏的分解器把$Q$变成带依赖关系的子问题有向无环图；终端子问题通过占位符吸收前序答案，因此回答终端节点本身就承担了最终聚合功能。系统在检索前检查该终端问题是否仍忠实于原问题：检查通过时保持目标语言推理，失败时才启用英语分解和双语图融合。随后，系统按拓扑顺序逐节点执行“填充依赖答案、跨语检索、证据去重、生成短答案”，并直接返回终端节点答案。

从直观上看，Syfer先把一道需要多步查证的题改写成一张任务清单，其中后一项明确引用前一项的答案；最后一项被特意训练成“已经包含完整原题意图的收尾问题”。它还设置一道质量闸门：目标语言任务清单可靠时不翻译，只有清单偏离原题时才借助英语版本校正；这样同时减少无必要翻译、错误子分支和末端重复总结造成的噪声。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 离线逻辑分解蒸馏

教师把每个问题$Q$映射为具有唯一终端节点和占位符依赖的无环子问题图$D^*$；仅保留填充后的终端问题$q_n^{\mathrm{filled}}$与原问题嵌入余弦相似度不低于$\tau_{\mathrm{constraint}}$的样本。图随后被线性化为保留节点次序和边结构的序列$y$，学生分解器以逐词元交叉熵学习条件生成该序列。

<div class="method-step__io" markdown="1">

**输入**：与评测集合隔离的语料—问题池、教师模型生成的候选分解，以及检索器嵌入函数$\mathbf{e}(\cdot)$。<br>
**输出**：训练完成的分解器参数$\theta^*$，以及由高忠实度问题—图对构成的监督集$\mathcal{D}_{\mathrm{train}}$。

</div>

**直观理解**：教师先示范如何把复杂题拆成可靠的步骤，再用“最后一步是否仍像原题”筛掉不合格示范。学生因此在离线阶段学会拆题，线上不必为每个问题调用昂贵教师。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 合成器折叠式分解

分解器生成$D_L=(V_L,E_L)$，其中节点$q_i$是子问题，边$(q_i,q_j)$表示$q_j$必须用答案$a_i$替换占位符$\#i$后才能求解。图保持无环且只有一个终端节点$q_n$；该节点经训练后，其填充形式$q_n^{\mathrm{filled}}$同时编码原问题意图与前序答案。

<div class="method-step__io" markdown="1">

**输入**：目标语言$L$中的原问题$Q$和已训练分解器$\theta^*$。<br>
**输出**：目标语言子问题图$D_L$，包括有序依赖、占位符和可充当最终聚合器的终端节点。

</div>

**直观理解**：常规方法先回答很多小题，再让模型重新读一遍所有过程并总结；Syfer把“总结任务”预先写进最后一个小题。这样最后一次正常问答就是最终答案生成，不再需要独立聚合调用。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 忠实度验证与条件式双语回退

系统比较$q_n^{\mathrm{filled}}$与$Q$的检索器嵌入相似度；达到阈值时直接采用$D_L$，否则把$Q$翻译为英语，用同一分解器得到$D_{\mathrm{en}}$，再按跨语节点嵌入相似度对齐并融合超过$\tau_{\mathrm{align}}$的节点。该过程产生按问题级忠实度门控的双语图，而不是无条件翻译全部节点或文档。

<div class="method-step__io" markdown="1">

**输入**：原问题$Q$、目标语言图$D_L$、相似度阈值$\tau_{\mathrm{constraint}}$和节点对齐阈值$\tau_{\mathrm{align}}$。<br>
**输出**：通过验证的单语图$D_L$，或融合目标语言与英语视图的双语图$D_F=\mathrm{Fuse}(D_L,D_{\mathrm{en}})$。

</div>

**直观理解**：这一步像给拆题结果做语义验收：最后的小题仍能代表原题，就继续用原语言；若已经跑题，才引入英语版本进行交叉校正。英语在这里是故障恢复路径，不是每个样本都支付的固定成本。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 跨语检索与顺序回答

系统对$D$拓扑排序，并在每个节点上先代入全部前驱答案；单语节点用目标语言问题检索，双语节点分别用目标语言和英语问题检索并合并候选，再用最大边际相关性MMR兼顾相关性与证据多样性。生成器依据筛选证据为每个节点产生短答案$a_i$，答案继续填入后继节点，最终直接返回终端答案$A=a_m$。

<div class="method-step__io" markdown="1">

**输入**：路由后的图$D\in\{D_L,D_F\}$、多语语料库$\mathcal{C}$、检索器、生成器和MMR权衡系数$\lambda$。<br>
**输出**：逐节点中间答案、经过去重和多样化选择的证据集合，以及最终答案$A$。

</div>

**直观理解**：系统严格按依赖顺序逐项查资料，避免在必要事实尚未得到时提前回答后续问题。双语检索可能找回同一文档的多个翻译版本，MMR会保留与当前问题相关但彼此不重复的证据，最后一项的答案直接作为整题答案。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 分解器蒸馏目标

$$
\mathcal{L}_{\mathrm{Distill}}(\theta)=-\mathbb{E}_{(Q,y)\sim\mathcal{D}_{\mathrm{train}}}\sum_{t=1}^{T}\log p_{\theta}\!\left(y_t\mid Q,y_{<t}\right),\qquad \theta^*=\arg\min_{\theta}\mathcal{L}_{\mathrm{Distill}}(\theta)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{Distill}}$：学生分解器的蒸馏训练损失。
- $\theta$：学生分解器的可训练参数；其最优值记为θ星。
- $\mathcal{D}_{\mathrm{train}}$：经过终端问题忠实度过滤的问题—分解序列监督集。
- $Q$：输入的复杂多跳问题。
- $y=(y_1,\ldots,y_T)$：由教师子问题DAG线性化得到、保留节点和边信息的长度为T的词元序列。
- $p_\theta(y_t\mid Q,y_{<t})$：给定原问题和此前输出词元时，学生模型生成第t个目标词元的条件概率。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标要求学生逐词元复现教师提供的结构化分解；最小化负对数概率等价于提高正确图序列的生成概率。由于训练对已先经过终端忠实度筛选，优化的不只是表面格式模仿，也把“最终子问题应能代表原问题”的约束间接蒸馏进$\theta^*$。<br>
**原文位置**：第3.1节，公式(2)；训练样本过滤条件见公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 分解忠实度评分与双语路由

$$
\mathrm{score}(D_L)=\cos\!\left(\mathbf{e}(q_n^{\mathrm{filled}}),\mathbf{e}(Q)\right),\qquad \mathrm{Route}(D_L)=\begin{cases}D_L,&\mathrm{score}(D_L)\geq\tau_{\mathrm{constraint}},\\ \mathrm{BilingualFallback}(D_L,Q),&\mathrm{score}(D_L)<\tau_{\mathrm{constraint}}.\end{cases}
$$

**符号说明**

- $D_L$：在原问题语言L中生成的子问题有向无环图。
- $q_n^{\mathrm{filled}}$：用前序子答案替换全部依赖占位符后的唯一终端子问题。
- $Q$：未经分解的原始复杂问题。
- $\mathbf{e}(\cdot)$：检索器提供的文本嵌入函数。
- $\cos(\cdot,\cdot)$：衡量两个嵌入方向接近程度的余弦相似度。
- $\tau_{\mathrm{constraint}}$：判定终端子问题是否仍忠实于原问题的阈值。
- $\mathrm{BilingualFallback}(D_L,Q)$：翻译原问题、生成英语分解，并将英语图与目标语言图对齐融合的恢复过程。

<div class="equation-explanation" markdown="1">

**直观理解**：公式先把“分解是否跑题”转化为终端问题与原问题在检索语义空间中的接近程度，再据此选择单语或双语路径。其关键作用是推迟翻译：高分样本避免额外翻译及双语噪声，低分样本才用英语视图弥补不可靠分解。<br>
**原文位置**：第3.3节，公式(4)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练分为教师数据构造和学生优化两部分。教师首先为评测外的问题生成带唯一终端节点的候选图$D^*$；系统填充终端问题，并以$\cos(\mathbf{e}(q_n^{\mathrm{filled}}),\mathbf{e}(Q))\geq\tau_{\mathrm{constraint}}$作为硬过滤条件，只让终端语义仍接近原题的分解进入$\mathcal{D}_{\mathrm{train}}$。随后将每张图线性化为$y=(y_1,\ldots,y_T)$，通过最小化$\mathcal{L}_{\mathrm{Distill}}(\theta)$训练学生预测下一个词元，得到$\theta^*$。因此，硬过滤负责监督质量，交叉熵负责学习结构化输出；论文节选未给出检索器或最终答案生成器的联合训练目标，也未说明它们与分解器端到端反向传播。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 格式约束的DAG分解器与终端合成器**

分解器不是输出无结构的问题列表，而是生成$D_L=(V_L,E_L)$形式的有向无环图，并用$\#i$显式标记节点间答案依赖。训练样本要求唯一终端节点$q_n$的填充形式与$Q$在检索嵌入空间中保持接近，使终端节点成为被折叠进分解过程的合成器；同一组参数$\theta^*$同时用于目标语言和英语回退分支，不进行分支专用微调。

> 直观理解：显式依赖能告诉系统“哪个答案应填到哪个后续问题”，比自由生成一串小题更可控。终端节点承担汇总职责，可避免额外聚合模型再次读取整条推理路径时放大早期错误。

**2. 忠实度门控与双语图对齐**

门控分数为$q_n^{\mathrm{filled}}$与$Q$的嵌入余弦相似度；低于$\tau_{\mathrm{constraint}}$才触发英语翻译和第二次分解。回退阶段在$V_L$与$V_{\mathrm{en}}$之间按嵌入相似度寻找节点对应关系，仅融合相似度超过$\tau_{\mathrm{align}}$的节点，形成双语节点集合$V_{\mathrm{bi}}$。

> 直观理解：该模块解决的是“何时值得翻译”，而不只是“如何翻译”。可靠样本走短而原生的单语路径，疑难样本才获得双语补充，从而在信息覆盖、语言噪声和计算成本之间作样本级取舍。

**3. 拓扑推理与跨语MMR证据选择**

图经$\mathrm{TopoSort}(D)$得到执行序列$S=(v_1,\ldots,v_m)$；每个$q_i^{\mathrm{filled}}$仅在前驱答案就绪后检索和作答。双语节点合并两种语言查询得到的候选集合$R_i$，MMR以$\lambda$平衡查询相关性和相对已选集合$S_i$的非冗余性，再把过滤后的证据交给生成器。

> 直观理解：拓扑顺序保证推理条件完整，MMR则防止同一事实的平行翻译占满证据窗口。两者分别控制推理次序错误和检索冗余错误，使双语信息只有在提供新增证据时才更有价值。

**训练与推理**

训练时，先在与评测隔离的问题池上调用教师模型，生成含节点、边、唯一终端节点及占位符依赖的$D^*$；填入依赖答案后计算终端问题与$Q$的检索嵌入余弦相似度，丢弃低于$\tau_{\mathrm{constraint}}$的样本。保留图被序列化，并以教师强制方式最小化逐词元交叉熵，得到独立分解器$\theta^*$；该参数在所有推理分支中复用。

推理时，$\theta^*$先在语言$L$中把$Q$分解为$D_L$。系统在正式检索前验证$q_n^{\mathrm{filled}}$对$Q$的忠实度：通过则保留单语图，未通过则翻译$Q$为英语、用相同分解器产生$D_{\mathrm{en}}$，按节点嵌入相似度融合为$D_F$。选定图按拓扑顺序执行；节点先接收前驱答案并完成占位符替换，随后单语检索或双语联合检索，候选证据经MMR去除平行翻译等近重复内容，生成器输出短答案$a_i$并传给后继。终端节点完成后直接令$A=a_m$，不再执行基于$(Q,q_{1:n},a_{1:n})$的独立聚合调用。

**复现信息**

公平复现需要保留四项决定性设置：第一，教师数据必须来自评测外的问题池，防止分解监督泄漏；第二，图的序列化格式必须保存节点顺序、边和$\#i$占位符，否则无法恢复依赖及拓扑执行；第三，训练样本过滤与推理路由共用忠实度阈值$\tau_{\mathrm{constraint}}$，双语节点融合另用$\tau_{\mathrm{align}}$；第四，多语语料包含文档对齐的翻译版本，因此双语候选合并后必须使用带系数$\lambda$的MMR控制相关性与多样性。节选未明确报告教师模型、学生模型、检索器、生成器、阈值具体数值、检索深度、MMR保留数量、优化器、学习率、训练轮数、提示模板或硬件配置，不能据此补造；这些信息仍需回查论文其余实现章节或代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HotpotQA：英文多跳问答基准，实验采用与HippoRAG2相同的1,000条查询测试划分。作者用GPT-4o将原始英文测试池翻译并扩展到九种语言，用于考察系统在需要组合多个证据的问答任务上的多语言表现。
- 2WikiMultiHopQA（2Wiki）：以跨维基实体关系组合为核心的多跳问答基准，同样采用1,000条查询测试划分并扩展为九种语言。它主要检验系统能否正确分解实体关系链、逐步检索证据并汇总答案。
- MuSiQue：强调可组合、不可通过浅层捷径轻易回答的多跳问答基准，同样使用1,000条查询测试划分及九语言版本。该数据集还提供了实验所遵循的语言特定答案规范化原则，用于降低不同语言分词、大小写和标点差异对评分的干扰。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Exact Match（EM）**

比较查询语言中的预测答案与参考答案；规范化后完全一致记为1，否则记为0。它严格衡量答案字符串是否精确正确，但对语义正确而措辞略有差异的答案不宽容。 （越高越好，因为更高的EM表示更多样本的规范化预测与标准答案完全匹配。）

</div>
<div class="metric-item" markdown="1">

**token-level F1**

在语言特定分词与规范化后，根据预测答案和参考答案之间的词元精确率与召回率计算调和平均值。它允许部分重合，因此比EM更能反映答案内容的局部正确程度。 （越高越好，因为更高的F1表示预测答案与参考答案在词元层面同时具有更高的精确率和召回率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文摘录未包含表1的数据行、后续消融实验、效率或成本统计。因此不能给出要求带逐句证据的三项主要数值结果，也无法判断分解质量门控、延迟翻译、双语节点对齐和MMR各自贡献了多少性能变化。
- 九语言测试集由GPT-4o从英文测试池翻译扩展，而不是由各语言使用者独立编写；即使实体表提高了名称一致性，仍可能保留英语问题结构或产生翻译偏差。训练分解器的标注也由大型教师模型生成，因此评测结论同时受到合成训练数据质量与机器翻译质量的影响。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Vanilla RAG：直接以原始问题进行一次检索并生成答案。它用于判断复杂的子问题分解、质量门控和双语对齐是否比标准单次检索流程更有效。
- HippoRAG2：在三元组索引知识图谱上运行的结构感知Graph-RAG强基线。与它比较可检验Syfer的子问题图及顺序推理能否与显式知识图结构方法竞争。
- CrossRAG：先从多语言语料检索文档，再把检索文档翻译成查询语言后生成答案。它代表统一执行翻译对齐的路线，可用于比较Syfer按需启用翻译是否能减少翻译噪声与额外计算，同时维持准确率。
- DaPT：把复杂问题分解为子问题有向无环图，并在每一跳融合子问题及其英语平行版本。它是与Syfer最直接的分解式多语言RAG对照，用于检验分解质量检查、延迟翻译以及失败后才进行双语图对齐是否优于每跳固定双语融合。

**实验想回答的问题**

- 在统一生成器与检索器的条件下，Syfer能否在九种语言、三个多跳问答数据集上取得有竞争力的答案准确率，并优于单次检索、结构化图检索、检索后翻译及逐跳双语融合等代表性方案？
- Syfer能否在高、中、低资源语言以及分布内、分布外语言上保持稳定表现，从而验证其“优先使用原语言分解，仅在分解质量检查失败时启用英语翻译与双语图对齐”策略的跨语言泛化能力及成本效益？

**实验实现**

所有需要生成器的方法均使用DeepSeek-V4 Pro作为回答模型，所有方法共享BGE-m3多语言检索器；检索索引由九种语言语料的并集构成，每次查询返回$\mathrm{top}\text{-}k=5$篇文档。Syfer设置分解忠实性门控阈值$\tau_{\mathrm{constraint}}=0.8$、跨语言节点对齐阈值$\tau_{\mathrm{align}}=0.6$以及MMR权衡系数$\lambda=0.6$。这种统一后端的协议意在把比较重点放在推理与翻译策略，而非生成器或检索器差异上。分解器采用知识蒸馏训练：Qwen3-235B-A22B-Instruct-2507生成训练侧翻译和标注，Qwen3-8B作为学生模型；训练集含59,688条分解记录，覆盖英语、中文、德语、西班牙语、斯瓦希里语和泰语六种分布内语言，法语、孟加拉语和韩语完全留作分布外评测。学生训练2轮，全局批量为64，学习率为$2\times10^{-4}$。测试集翻译使用GPT-4o，并维护逐文档实体表，以保持问题、支持段落和子问题中的实体名称一致；回答模型、分解器家族和测试集翻译模型彼此不同，以降低同模型家族带来的混杂因素。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：核心方法通过受控问题分解、质量检查和检索调用完成多语言多跳推理。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`176ef399fa1238aa3a5798c82bd0274260a5c7ac878de7a1f59c7579ccdee3df`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
