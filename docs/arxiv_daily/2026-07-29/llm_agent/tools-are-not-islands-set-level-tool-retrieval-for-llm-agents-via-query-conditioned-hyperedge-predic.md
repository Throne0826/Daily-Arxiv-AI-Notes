---
title: "[论文解读] Tools Are Not Islands: Set-Level Tool Retrieval for LLM Agents via Query-Conditioned Hyperedge Prediction"
description: "[arXiv 2607.25718][LLM Agent] HYSET将LLM智能体的工具检索从“逐个工具排序”改写为“给定查询后对整组工具联合评分”，并通过随集合大小变化的交互建模，提高所需工具集合的完整覆盖能力。"
arxiv_id: "2607.25718"
announcement_date: "2026-07-29"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:03.695152+00:00"
source_sha256: "92900626aea9e517ab60e44a85b7ade753c4b0a40033e5c377e496140dc2b067"
tags:
  - "LLM Agent"
  - "LLM 其他"
  - "大型语言模型智能体"
  - "工具检索"
  - "集合级检索"
  - "超图"
  - "查询条件超边预测"
  - "工具共调用"
  - "基数特定交互"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2607.25718</p>

# Tools Are Not Islands: Set-Level Tool Retrieval for LLM Agents via Query-Conditioned Hyperedge Prediction

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-29</span>
<span><strong>作者</strong> Xinyi Hong, Pinjun Dong, Xinyang Yu, Binyan Jiang</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.25718v1) · [PDF 下载](https://arxiv.org/pdf/2607.25718v1) · **关键词** 大型语言模型智能体, 工具检索, 集合级检索, 超图, 查询条件超边预测, 工具共调用, 基数特定交互  


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

HYSET将LLM智能体的工具检索从“逐个工具排序”改写为“给定查询后对整组工具联合评分”，并通过随集合大小变化的交互建模，提高所需工具集合的完整覆盖能力。

**不用术语来说**：面对包含数千个API的工具库，智能体不能把所有工具说明都放进提示词，而要先筛出少量候选工具。困难在于现实任务往往需要多个工具协作：只挑选各自看起来最相关的工具，可能会重复覆盖同一子任务，却遗漏完成整个任务不可缺少的工具。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出查询条件化的超边预测视角：把一次任务需要共同调用的工具集合视为超图中的一条“超边”，直接以完整集合为评分单位，并据此统一解释独立排序、图增强检索和顺序生成等既有范式的受限之处。
- 提出具有集合基数特定交互的HYSET预选择模块，使工具兼容关系能够随候选集合大小变化；该模块位于下游智能体之前，无需修改智能体本身。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

大型语言模型智能体可通过调用搜索、订票、天气查询等外部 API 完成现实任务。由于工具库可能包含数千个端点，将全部工具描述放入提示词会带来过长上下文、推理延迟和成本，因此通常先执行“工具检索”：根据用户查询筛出少量候选工具，再交给下游智能体规划和调用。本文关注的关键特征是，多步骤任务往往需要若干工具共同完成；因此检索目标不仅是找到各自与查询相似的工具，还要保证所选集合能够完整覆盖任务，并避免功能重复但联合价值较低的工具。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**工具检索（tool retrieval）**

给定用户查询和大型工具库，在智能体开始规划或调用之前选出一个较小的候选工具子集。它用于缩小智能体的搜索空间，而不是直接决定工具的调用顺序或参数。

</div>
<div class="conceptitem" markdown="1">

**超图与超边预测（hypergraph / hyperedge prediction）**

普通图的一条边通常连接两个节点，而超图中的一条超边可以同时连接多个节点；在本文中，节点是工具，一条超边表示一组曾被共同调用或适合共同完成任务的工具。查询条件下的超边预测，就是判断哪个完整工具集合最适合当前查询。

</div>
<div class="conceptitem" markdown="1">

**集合基数（cardinality）**

集合基数是集合所含元素的数量，例如四工具集合的基数为 4。本文认为工具之间的兼容关系会随集合大小变化，因此不能用同一种两两关系统一解释不同规模的工具组合。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括自然语言查询与包含大量 API 端点的工具库；系统需要在下游智能体行动前输出一个规模受限、与查询相关且联合有用的工具集合。论文假设现实任务可能由多个子任务构成，所需工具之间存在共同调用关系，而这些关系可能随目标集合的基数变化。与独立地为每个工具打分并取前若干名不同，本文把整个候选集合视为评分单位，并将任务表述为工具共调用超图上的查询条件超边预测；输出仍是可直接交给原有智能体的预选工具集合，无须修改后续规划与调用模块。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$q$**

当前用户的自然语言查询；原文节选未给出正式符号表，此处仅用作问题描述中的简写。

</div>
<div class="notationitem" markdown="1">

**$\mathcal{T}$**

可供检索的完整工具或 API 端点库；原文节选未明确规定该符号。

</div>
<div class="notationitem" markdown="1">

**$S \subseteq \mathcal{T}$**

针对查询选出的候选工具集合，也是本文主张直接进行整体评分的基本单位；原文节选未明确规定该符号。

</div>
<div class="notationitem" markdown="1">

**$|S|$**

候选工具集合的基数，即其中工具的数量；不同基数对应的工具交互模式可能不同。

</div>

</div>

**直接相关的工作**

- **COLT（Qu et al., 2024）**: 代表图增强式工具检索：利用查询—场景—工具二部图上的协同学习改善完整工具集合的召回，但协同信息最终被压入单工具表示，推理时仍采用独立的 top-k 排名，因而没有直接比较完整候选集合。
- **ToolGen（Wang et al., 2024）**: 代表生成式工具检索：语言模型按序生成工具标识符，使后续选择可依赖先前结果；但训练与解码依据局部条件概率和序列似然，完整工具集合在生成结束前不会被作为整体显式比较。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大规模API生态使穷举式上下文输入在有效信息利用、延迟和成本上都不可行，因此必须在智能体执行前压缩工具空间。同时，多步骤任务通常要求若干API共同完成不同子任务，检索目标实际上是一个小而完整、内部互补的工具集合，而不只是若干语义相似的单个工具。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **独立评分式检索，包括BM25、稠密双编码器及图增强检索**：BM25按词汇重合度排序，Contriever或Sentence-BERT类模型按查询与工具描述的嵌入相似度排序；COLT等图增强方法在训练中利用查询—场景—工具图学习协同信息，但推理时仍为每个工具产生独立分数并取top-k。
- **生成式工具检索，如ToolGen**：语言模型根据查询逐步生成工具标识符，以序列似然训练，并由前面已经生成的工具条件化后续选择，最终把多个局部决策拼成候选工具集合。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 独立排序不知道其他工具是否已被选中，因而无法显式衡量互补性、冗余性和完整任务覆盖：多个高分工具可能集中于同一子任务，而某个单独相关度较低但不可缺少的工具会被挤出；图增强方法虽然注入协同信号，最终仍只近似而非直接评价集合质量。
- 顺序生成只优化每一步的局部条件概率，没有在完整集合层面比较不同候选；此外，固定形式的联合建模容易忽视集合大小带来的语义变化——同一对工具在二工具任务中可能罕见，在四工具复合任务中却可能自然共现。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种能够以完整候选集合为基本预测对象、直接评价其联合效用，并允许工具间兼容关系随目标集合基数变化的检索框架；同时，该框架还需能作为独立预选择组件接入既有智能体。

</div>
<div markdown="1"><span>核心问题</span>

给定用户查询，能否通过查询条件化的超边预测直接为候选工具集合评分，并通过基数特定的工具交互模型，更准确地找回完成任务所需的完整工具集合？

</div>
<div markdown="1"><span>作者直觉</span>

把工具看作彼此协作的团队而非相互独立的候选人，可以在评分时识别“重复做同一件事”的冗余工具和“补齐尚未覆盖子任务”的关键工具；再按集合大小分别学习交互规律，可避免把简单任务中的共现关系机械套用于更复杂的多工具任务。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

HYSET把工具检索重新定义为“查询条件下的超边预测”：工具库中的每个工具是超图节点，一组曾被共同调用的工具构成一条超边；给定自然语言查询，模型不再独立判断每个工具是否相关，而是直接为完整候选集合打分。设工具库为 \(\mathcal{T}=\mathcal{V}\)，训练样本为查询—标注工具集对 \((x_i,E_i^\star)\)，允许的输出是大小在1到训练集最大集合规模 \(M\) 之间的无序集合。模型总分由两部分组成：查询无关的集合内部兼容性，以及查询与整个集合的匹配程度。前者使用随集合大小变化的交互矩阵，使同一工具对在二工具组合和三工具组合中可以具有不同作用；后者以查询为注意力条件，对集合内工具进行联合加权，而非简单累加独立相关性。
训练时，HYSET从标注集合及三类负集合构造小型候选池，以集合级对比损失提升正确集合的得分；同时把当前最高分集合交给冻结的下游LLM智能体执行任务，用执行奖励加强实际有效的预测集合。推理时由于全工具库的所有子集数量呈组合增长，系统先按单工具相关性与工具互补性建立短名单，再枚举短名单中大小不超过 \(M\) 的集合并进行集合级重排，最终将变长、无序的最佳工具集交给无需修改的下游智能体。直观地说，传统方法像逐个招聘“看起来合适的人”，HYSET则同时考虑候选人是否符合任务、彼此能否组成有效团队，以及团队规模变化后分工是否仍然合理。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建工具共调用超图与训练候选池

把每个标注工具集 \(E_i^\star\) 视为超边，并令 \(M=\max_i|E_i^\star|\)；对每个查询建立 \(\mathcal{C}_i=\{E_i^\star\}\cup\mathcal{N}_i\)，其中负集合按50%大小匹配随机集合、30%批内标注集合和20%近邻替换困难负例组成。

<div class="method-step__io" markdown="1">

**输入**：工具节点集合 \(\mathcal{V}=\mathcal{T}\)，以及训练集 \(\mathcal{D}_{\mathrm{tr}}=\{(x_i,E_i^\star)\}_{i=1}^{N}\)。  
**输出**：包含一个标注正集合和若干对比负集合的、可计算的集合级候选池 \(\mathcal{C}_i\)。

</div>

**直观理解**：全部工具子集多到无法逐一训练，因此模型只在一组有代表性的“错误团队”中辨认正确团队。随机负例测试基本区分能力，批内负例测试查询特异性，困难负例则迫使模型分辨功能相近但组合不正确的工具。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算查询条件下的集合总分

先对集合内所有工具对计算由 \(\mathbf{M}_m\) 控制的兼容性之和，再以查询向量为注意力查询，对投影后的工具嵌入进行归一化加权，得到查询—集合对齐分；两项相加形成 \(F_\theta(x_i,E)\)。

<div class="method-step__io" markdown="1">

**输入**：查询 \(x_i\)、候选工具集 \(E=\{t_{j_1},\ldots,t_{j_m}\}\)、工具嵌入 \(\mathbf{Z}\)、冻结查询编码器 \(\mathbf{r}(\cdot)\)、投影矩阵 \(\mathbf{P}\) 和集合规模专属矩阵 \(\mathbf{M}_m\)。  
**输出**：表示候选集合对当前查询联合效用的单一实数分数。

</div>

**直观理解**：模型同时回答两个问题：这些工具平时是否能协作，以及它们组成的整体是否适合当前请求。注意力权重在集合内部归一化，因此加入或移除一个工具会改变其他工具的相对重要性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 集合级监督与执行反馈联合训练

集合级检索损失把标注集合的softmax概率推高；奖励加权自训练损失则在当前预测确实帮助智能体完成任务时强化该预测，并对各 \(\mathbf{M}_m\) 加Frobenius范数正则，同时约束每个工具嵌入为单位范数。

<div class="method-step__io" markdown="1">

**输入**：候选池内各集合的分数、标注集合 \(E_i^\star\)、当前最高分集合 \(\widehat{E}_i\)，以及冻结智能体执行该集合所得奖励 \(\rho_i\in[0,1]\)。  
**输出**：学习后的参数 \(\widehat{\theta}=(\widehat{\mathbf{Z}},\{\widehat{\mathbf{M}}_m\}_{m=2}^{M},\widehat{\mathbf{P}})\)及评分函数 \(\widehat{F}=F_{\widehat{\theta}}\)。

</div>

**直观理解**：标注监督告诉模型“标准答案是哪一组”，执行奖励补充说明“模型自己找到的其他组合是否也真正可用”。这对原文所述标注集合不一定是唯一可行集合的情形尤其重要。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 短名单生成与集合级推理

先用单例分数选出 \(K_1\) 个工具，再按其与初选工具的最大已学习互补性补足短名单；随后枚举短名单中所有大小为1至 \(M\) 的子集，用完整集合分数选取最高分集合。

<div class="method-step__io" markdown="1">

**输入**：新查询 \(x_{\mathrm{new}}\)、学习后的评分函数、初始相关工具数 \(K_1\)、短名单规模 \(K_{\mathrm{pool}}\)和最大输出规模 \(M\)。  
**输出**：变长无序工具集 \(\widehat{E}(x_{\mathrm{new}})\)，并将其交给冻结的下游LLM智能体执行。

</div>

**直观理解**：第一阶段保证多数候选与问题直接相关，互补性扩展则允许纳入一个单看不突出、但能补齐关键功能的工具。第二阶段才真正比较不同团队及不同团队规模，避免把独立排名前几名机械拼在一起。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="equation-block" markdown="1">

#### HYSET的查询条件集合评分函数

$$
F_{\theta}(x_i,E)=F_{\mathrm{set}}(E)+F_{\mathrm{align}}(x_i,E)=\sum_{1\le a<b\le m}\mathbf z_{j_a}^{\top}\mathbf M_m\mathbf z_{j_b}+\sum_{k=1}^{m}\alpha_k(x_i,E)\ell(x_i,t_{j_k}),\quad \ell(x_i,t_{j_k})=\mathbf r(x_i)^{\top}\mathbf P\mathbf z_{j_k},\quad \alpha_k(x_i,E)=\frac{\exp(\ell(x_i,t_{j_k}))}{\sum_{q=1}^{m}\exp(\ell(x_i,t_{j_q}))}
$$

**符号说明**

- $F_{\theta}(x_i,E)$：参数为 \(\theta\) 时，候选工具集 \(E\) 对查询 \(x_i\) 的联合效用分数。
- $F_{\mathrm{set}}(E)$：不依赖当前查询、刻画集合内部共调用与功能互补性的分数。
- $F_{\mathrm{align}}(x_i,E)$：查询与整个候选集合之间的对齐分数。
- $E=\{t_{j_1},\ldots,t_{j_m}\}$：包含 \(m=|E|\) 个工具的无序候选集合，\(t_{j_k}\) 是其中第 \(k\) 个记号化成员。
- $\mathbf z_{j_k}$：工具 \(t_{j_k}\) 的可学习 \(d_z\) 维嵌入。
- $\mathbf M_m$：供大小为 \(m\) 的集合使用的对称交互矩阵。
- $\mathbf r(x_i)$：冻结预训练查询编码器产生的 \(d_r\) 维查询向量。
- $\mathbf P$：把工具嵌入从工具空间映射到查询表示空间的可训练矩阵。
- $\ell(x_i,t_{j_k})$：查询与单个工具投影表示之间的内积匹配分数。
- $\alpha_k(x_i,E)$：工具 \(t_{j_k}\) 在集合 \(E\) 内的softmax注意力权重。
- $a,b,k,q$：集合成员索引；\(a<b\)保证每个无序工具对只计算一次，\(q\)用于注意力归一化。
- $\theta=(\mathbf Z,\{\mathbf M_m\}_{m=2}^{M},\mathbf P)$：全部可训练参数，包括工具嵌入矩阵、各集合规模的交互矩阵和跨空间投影矩阵。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项检查工具之间能否协作，并允许协作关系随集合规模改变；第二项让查询在当前集合内部重新分配关注度。两者相加意味着一个集合只有在“成员搭配合理”和“整体符合当前任务”两方面都表现良好时才会获得高分。  
**原文位置**：第2.4节，公式(2)–(6)

</div>

</div>

<div class="equation-block" markdown="1">

#### 标注检索与执行反馈联合目标

$$
\mathcal L(\theta)=\mathcal L_{\mathrm{ret}}(\theta)+\eta\mathcal L_{\mathrm{self}}(\theta)+\lambda\sum_{m=2}^{M}\|\mathbf M_m\|_F^2,\quad \mathcal L_{\mathrm{ret}}(\theta)=-\sum_{i\in\mathcal B}\log\frac{\exp F_\theta(x_i,E_i^\star)}{\sum_{E\in\mathcal C_i}\exp F_\theta(x_i,E)},\quad \mathcal L_{\mathrm{self}}(\theta)=-\sum_{i\in\mathcal B}\rho_i\log\frac{\exp F_\theta(x_i,\widehat E_i)}{\sum_{E\in\mathcal C_i}\exp F_\theta(x_i,E)},\quad \widehat\theta=\arg\min_{\theta\in\Theta}\mathcal L(\theta)\ \mathrm{s.t.}\ \|\mathbf z_j\|_2=1\ \forall t_j\in\mathcal V
$$

**符号说明**

- $\mathcal L(\theta)$：HYSET用于参数优化的完整训练损失。
- $\mathcal L_{\mathrm{ret}}$：集合级标注检索损失，使标注工具集在候选池softmax中的概率增大。
- $\mathcal L_{\mathrm{self}}$：奖励加权自训练损失，强化由当前模型选中且执行有效的集合。
- $\eta$：执行反馈损失的正权重。
- $\lambda$：基数专属交互矩阵正则项的正权重。
- $\|\mathbf M_m\|_F^2$：矩阵 \(\mathbf M_m\) 的平方Frobenius范数，用于限制交互参数规模。
- $\mathcal B$：当前小批量中的训练样本索引集合。
- $E_i^\star$：查询 \(x_i\) 的标注工具集合。
- $\mathcal C_i$：由标注集合和负集合共同构成的有限训练候选池。
- $\widehat E_i$：当前参数下在候选池 \(\mathcal C_i\) 中得分最高的工具集合。
- $\rho_i$：冻结智能体使用 \(\widehat E_i\) 执行查询后得到的任务奖励，取值位于 \([0,1]\)。
- $\Theta$：模型参数的可行空间。
- $\widehat\theta$：满足工具嵌入单位范数约束的学习后参数。
- $\|\mathbf z_j\|_2=1$：每个工具嵌入的欧氏范数固定为1，以消除任意尺度并稳定交互分数。
- $\mathcal V$：超图节点集合，即完整工具库。

<div class="equation-explanation" markdown="1">

**直观理解**：第一项以人工标注为教师，第二项以真实执行是否成功为补充信号：奖励越高，模型越强地学习当前预测集合；奖励为零时该样本不产生自训练强化。正则化和单位范数约束防止模型仅通过无限放大工具嵌入或交互矩阵来降低softmax损失。  
**原文位置**：第2.4节，公式(8)–(11)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优化以有限候选池上的集合级分类为核心。对每个训练查询，HYSET将标注集合与 \(K_{\mathrm{neg}}-1\) 个不同负集合放入 \(\mathcal C_i\)，通过 \(\mathcal L_{\mathrm{ret}}\)提高完整标注集合相对于所有负集合的得分，而不是分别监督各工具。负例混合兼顾三种错误：规模相同但成员随机的集合、对其他查询正确但对当前查询不合适的集合，以及只替换一两个相似工具的近似错误集合；后者直接检验模型能否学习组合兼容性，而非仅识别工具类别。
在每轮更新中，模型还选出候选池内最高分集合，并让冻结智能体在最多 \(R\) 个DFSDT步骤内执行查询。执行得分 \(\rho_i\)作为权重加入 \(\mathcal L_{\mathrm{self}}\)，因此作者的方法能够利用标注之外、实际执行成功的替代工具组合，但 \(\widehat E_i\) 与 \(\rho_i\)在单次参数更新内被视为常数，并非对智能体执行过程反向传播。最终最小化联合损失，训练 \(\mathbf Z\)、\(\mathbf P\)及各 \(\mathbf M_m\)；查询编码器和下游智能体保持冻结。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 基数专属集合交互模块**

对规模为 \(m\) 的候选集，模块使用对称矩阵 \(\mathbf{M}_m\) 计算全部工具对的双线性交互。虽然形式上是成对求和，但当不同规模使用不同矩阵时，Möbius意义下可诱导高于二阶的集合效应；例如三工具集合的三阶效应由 \(\mathbf{M}_3-\mathbf{M}_2\) 引入。若所有工具对在 \(\mathbf{M}_2,\ldots,\mathbf{M}_M\) 下得分完全相同，该模块才退化为固定的普通成对模型。

> 直观理解：同一对工具单独搭配可能很好，但放进更大的团队后可能冗余或产生冲突。按团队人数选择交互规则，能表达这种“组合环境改变成员关系”的现象，又避免直接学习参数量随阶数指数增长的高阶张量。

**2. 查询—集合交叉注意力模块**

冻结的预训练语言模型把查询映射为 \(\mathbf{r}(x)\)，可训练矩阵 \(\mathbf{P}\)把工具嵌入投影至同一空间。查询与每个工具的内积经过集合内softmax得到注意力权重，再加权汇总工具表示；由于分母包含整个集合，任一工具的权重都依赖其他候选成员，因此它是集合级而非独立工具级匹配。

> 直观理解：该模块让任务描述决定集合中谁最关键，同时检查一个候选工具在当前团队中的相对作用。它不同于把若干独立相似度直接相加，因为团队成员变化会重新分配所有成员的权重。

**3. 相关性—互补性两阶段搜索模块**

完整候选空间大小为 \(\sum_{m=1}^{M}\binom{|\mathcal{V}|}{m}\)，无法穷举。HYSET先按单例查询匹配建立核心集合 \(\mathcal{S}_0\)，再使用 \(g(t_j)=\max_{t_i\in\mathcal{S}_0}\widehat{\mathbf z}_j^\top\widehat{\mathbf M}_M\widehat{\mathbf z}_i\)选择互补工具，最终只在 \(\mathcal{S}\) 内评估 \(\sum_{m=1}^{M}\binom{K_{\mathrm{pool}}}{m}\) 个集合。

> 直观理解：直接搜索所有团队不可行，只看单工具相关性又可能漏掉辅助工具。两阶段设计先缩小范围，再把“能与核心工具配合”的候选补回来，在计算成本与集合质量之间折中。

**训练与推理**

训练流程：首先由标注查询—工具集建立工具共调用超图，并以训练样本中最大工具集大小确定 \(M\)。每个小批量中，为每个正集合生成固定规模的集合候选池，使用共享工具嵌入、查询—集合注意力和基数专属交互矩阵计算全部候选分数；取候选池最高分集合交给冻结智能体执行并取得奖励。随后联合计算标注检索损失、奖励加权自训练损失和交互矩阵正则项，更新 \(\theta\)，并把每个工具嵌入约束在单位球面上，重复直至收敛。
推理流程：先对每个工具计算单例分数 \(\mathbf r(x_{\mathrm{new}})^\top\widehat{\mathbf P}\widehat{\mathbf z}_j\)，选择前 \(K_1\) 个形成 \(\mathcal S_0\)；再按候选工具与 \(\mathcal S_0\) 的最大交互得分补充至 \(K_{\mathrm{pool}}\) 个工具，得到 \(\mathcal S\)。系统在 \(\mathcal E_M(\mathcal S)=\{E\subseteq\mathcal S:1\le |E|\le M\}\)中计算完整分数并取最大者，因此同时预测成员与集合大小。最终无序集合直接限制冻结智能体可调用的工具；若评测需要有序列表，则另行使用同一评分函数进行贪心边际增益排序。该设计是智能体之前的预选择模块，不要求修改智能体参数、规划逻辑或工具调用接口。

**复现信息**

公平理解和复现所需的关键设置包括：查询编码器保持冻结，工具嵌入矩阵 \(\mathbf Z\)由集合兼容性项和查询对齐项共享，下游LLM智能体同样冻结；训练负例总数由 \(K_{\mathrm{neg}}\)控制，并按50%大小匹配随机负例、30%批内负例和20%近邻替换困难负例混合。困难负例中的近邻依据当前工具嵌入 \(\mathbf Z\)确定；智能体训练反馈通过DFSDT搜索获得，并受最大执行步数 \(R\)限制。
推理必须满足 \(K_1<K_{\mathrm{pool}}\)、\(M\le K_{\mathrm{pool}}\ll|\mathcal V|\)。互补性扩展按原文使用 \(\widehat{\mathbf M}_M\)，之后对短名单内所有不超过 \(M\) 的子集作精确集合评分；这只是对全库组合最优化的近似，计算量由工具库规模相关的组合数降为仅依赖 \(K_{\mathrm{pool}}\)和 \(M\) 的组合数。原文节选未明确给出 \(K_{\mathrm{neg}}\)、\(K_1\)、\(K_{\mathrm{pool}}\)、\(R\)、\(\eta\)、\(\lambda\)、嵌入维度或优化器的具体取值，复现时需进一步核查补充材料。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- ToolBench是主要训练与测试基准。官方过滤后包含13,860个可调用API端点和200,311条带真实API集合的指令；作者合并官方训练部分进行训练，并在六个留出测试集的共600个查询上评估。它用于比较离线检索、集合完整性和冻结智能体的端到端执行成功率，并额外按训练测试重合情况、未见完整工具集和未见工具对进行切分，以检查结果是否依赖记忆既有组合。
- UltraTool用于检验跨工具库迁移，包含22个领域的2,032个工具，且工具库与ToolBench完全不相交。其真实工具集合仅6.1%为单工具集合，而ToolBench为20.4%，因此它更强调多工具协作检索；实验比较目标域训练、从ToolBench直接零样本迁移以及HYSET与ToolGen的差距。
- ToolBench上的泛化划分包括UT、UC和CD三种设置：UT留出工具，UC留出工具类别，CD考查跨领域迁移。UC还提供每个目标类别1、5、10个标注样本的少样本适配及完整监督，用于区分工具新颖性、类别分布偏移和领域偏移，并衡量少量目标域标注能恢复多少性能。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**Recall@5**

衡量长度为5的检索排名覆盖了多少真实所需工具，主要检查单个相关工具能否被召回。它不能单独保证一个多工具任务所需的全部工具同时出现。 （越高越好，因为更高值表示真实工具中有更大比例进入前5名。）

</div>
<div class="metricitem" markdown="1">

**COMP@5**

集合完整性指标，检查前5个结果是否覆盖任务所需的完整工具集合。相较Recall@5，它更直接测试多工具任务是否因缺少任一必要工具而无法执行，是验证集合级检索主张的核心指标。 （越高越好，因为智能体只有获得完整的必要工具组合，才具备完成任务的工具条件。）

</div>
<div class="metricitem" markdown="1">

**GPT-4/Human Pass Rate**

在官方ToolEval协议下，把检索结果交给同一个冻结的ToolLLaMA-2-7B-v2智能体执行，再由GPT-4或人工判断任务是否成功。它衡量端到端可用性，但同时受到智能体推理、API执行与评判误差影响，不能被解释为纯检索质量。 （越高越好，因为通过率更高表示受检索工具集合约束的智能体更常完成查询。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### ToolBench域内主结果：HYSET-BERT与HYSET-Qwen对比六类现有检索器

<div class="result-value" markdown="1">

作者报告HYSET在所有检索指标和端到端指标上均超过全部基线；相对最强基线，BERT配置的检索增益最高为15.3%，Qwen配置最高为17.8%。核心集合指标COMP@5相对ToolGen分别提高10.8%和11.6%，且所有主结果差距在5%显著性水平下成立。

</div>

这支持论文的核心判断：直接评价整个工具组合尤其有助于找齐完整工具集，而非只改善某个相关工具的名次。两种主干的相对表现差异有限，也降低了“收益完全来自更强语言模型主干”的可能性。不过，主表中的HYSET额外使用了执行反馈，因此这些完整主结果不能单独证明模型结构在相同监督下贡献了全部端到端差距；作者随后用统一监督预算补做了比较。

<div class="result-source" markdown="1">

来源：第3.2节 Main Results，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Table 1 shows that HYSET outperforms every baseline on every retrieval and end-to-end metric. Retrieval gains over the strongest baseline reach 15.3% relative for the BERT configuration and 17.8% for Qwen, and are largest on COMP, where COMP@5 improves by 10.8% and 11.6% relative over ToolGen.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 控制执行反馈后的公平比较：HYSET与强基线使用相同奖励、评判器及20,000次 rollout 预算

<div class="result-value" markdown="1">

仅用人工标注训练时，HYSET-BERT达到77.02% COMP@5、82.14% Recall@5和65.14% GPT-4 Pass Rate；其COMP@5仍比ToolGen高10.0%（相对值），但Recall@5优势缩小至0.9%。给强基线加入同等执行反馈后，ToolGen达到83.12% Recall@5、70.94% COMP@5和66.85% Pass Rate；此时HYSET相对ToolGen的Pass Rate优势由8.8%降至4.3%，COMP@5优势则由10.8%降至9.3%。

</div>

该控制实验把“集合模型结构”和“额外执行监督”分开。执行反馈对HYSET和基线都有明显帮助，因此不能把主表中的全部通过率提升归因于超边建模；但统一反馈后COMP@5仍保持较大差距，说明集合完整性收益更可能来自模型设计。相反，Recall@5在仅标注监督下仅略高于ToolGen，表明HYSET最突出的价值不是一般性的逐工具召回，而是把相关工具组成完整集合。

<div class="result-source" markdown="1">

来源：第3.2节 Main Results；补充材料C.2、C.3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Retraining the two strongest baselines with the identical reward, judge and 20,000-rollout budget raises ToolGen to 83.12% Recall@5, 70.94% COMP@5 and 66.85% Pass Rate, and ToolLLaMA-Retriever to 66.42% Pass Rate. Execution feedback thus helps them by about as much as it helps HYSET, whose own Pass Rate gains 7.0% relative over its annotation-only value of 65.14%. The GPT-4 Pass Rate margin consequently falls from 8.8% to 4.3% relative while the COMP@5 margin falls only from 10.8% to 9.3%.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 泛化与数据效率：未见工具UT、未见类别UC、跨领域CD及UC少样本适配

<div class="result-value" markdown="1">

跨领域零样本CD达到72.83% Recall@5、61.96% COMP@5和54.85% Pass Rate；其COMP@5保留域内77.55%的79.9%。UC从零样本的65.28% COMP@5提升到5-shot的71.40%，相当于完整目标类别监督76.60%的93.2%；10-shot进一步达到74.38%。在工具库完全不同的UltraTool上，HYSET的COMP@5比ToolGen高11.5%，而ToolBench直接迁移可保留目标库训练性能的77.9%。

</div>

性能随分布偏移从未见工具、未见类别到跨领域逐步下降，说明HYSET并未消除领域差异；但零样本仍保留相当比例的域内集合完整性，少量每类标注即可恢复大部分完整监督表现，表明模型学习到部分可迁移的工具兼容关系。UltraTool的工具库与ToolBench不相交，因此该结果比固定库划分更能排除记忆具体工具组合；不过摘要未给出UltraTool绝对分数及全部置信区间，不能据此判断其绝对可用性。

<div class="result-source" markdown="1">

来源：第3.4节 Generalization and Data Efficiency，Table 3；补充材料D.1–D.4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Performance decreases as the shift grows, yet CD retains 79.9% of in-domain set completeness, and 5-shot UC recovers 93.2% of fully supervised performance. On UltraTool, whose library is disjoint from ToolBench, HYSET improves COMP@5 by 11.5% over ToolGen. Direct transfer from ToolBench without target training retains 77.9% of the performance obtained by training on UltraTool.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 主基准ToolBench只有六个测试集、共600条查询，端到端结果还依赖单一冻结智能体ToolLLaMA-2-7B-v2、DFSDT协议及ToolEval评判流程。因而实验能证明在该统一管线中的相对优势，但尚不能证明对不同智能体模型、规划器或真实在线API故障环境同样有效；作者使用的是缓存StableToolBench镜像而非实时端点。
- 泛化实验显示分布偏移越强性能越低，跨领域零样本仅保留79.9%的域内COMP@5，说明模型仍依赖源领域中学到的工具关系。此外，训练需要最多20,000次执行 rollout 和评判调用，报告成本为43.2 GPU小时及186美元评判费用；虽然推理远快于ToolGen，但仍约为单次稠密检索延迟的1.9倍。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- BM25：基于词项匹配的稀疏检索器，代表不依赖神经语义编码的逐工具检索范式，可检验HYSET的优势是否只来自基本的语义匹配能力。
- ToolLLaMA-Retriever：基于BERT的官方稠密工具检索器，也是HYSET-BERT所采用的冻结主干来源。共享或接近的编码基础使比较更能隔离集合级超边建模的作用，而不是编码器规模差异。
- ToolRerank与COLT：代表先召回、再重排或组合候选的工具检索方法。它们是有意义的中间比较对象，因为其目标也不止简单词法匹配，但仍未把整个候选工具集合统一作为一次评分的基本单位。
- ToolGen：文中最强的关键基线之一，代表生成式或顺序式工具集合构造，并多次作为COMP@5、迁移和执行反馈实验的直接参照。作者还以相同奖励、评判器和20,000次 rollout 预算重新训练它，以减少HYSET独享执行反馈造成的不公平。

**实验想回答的问题**

- 与逐工具打分或顺序组装工具的检索器相比，直接对候选工具集合进行超边打分，能否更完整地找回任务所需工具，并进一步提高冻结智能体的实际任务成功率？
- HYSET的收益是否确实来自集合级、基数相关的兼容性建模，而非更强的编码器、更多执行监督或训练测试重合；在未见工具、未见类别及跨领域工具库上，这种能力能否迁移？

**实验实现**

所有方法在同一个冻结的ToolLLaMA-2-7B-v2智能体和DFSDT执行协议下比较。HYSET分别使用冻结的BERT-base检索主干和调优后的Qwen2.5-1.5B检索主干；查询编码器、用于从API描述初始化工具表示的工具编码器以及下游智能体均冻结，只训练工具表示、按集合基数区分的交互矩阵和相关投影参数。BERT配置训练13.59M参数，其中10.64M属于工具表示，而冻结编码器有109.5M参数。最大集合大小设为5，第一阶段候选数为15、重排池为20、负样本数为64，每个查询共评分21,699个候选集合。执行反馈覆盖5,000条训练查询，每20,000步刷新，最多使用20,000次 rollout 和相同数量的评判调用；调用来自缓存的StableToolBench API镜像而非实时端点。每个配置运行三个随机种子，并按验证集Recall@5早停。离线指标基于固定长度排名，而真正交给智能体的是可变大小集合，因此作者另行直接评估该集合。显著性检验对检索指标采用10,000次配对bootstrap，对通过率采用精确McNemar检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除集合级评分函数F_set | 完整模型为84.75±0.09% Recall@5、77.55±0.12% COMP@5和69.69±0.61% Pass Rate；移除F_set后分别降至72.04±0.18%、67.36±0.09%和57.97±0.73%。作者按相对变化概括为COMP@5下降13.1%、Pass Rate下降16.8%。 | 该消融直接检验“把候选集合整体作为评分单位”是否必要。三个指标均大幅下降，尤其集合完整性和最终通过率同步下降，说明逐工具或缺少联合集合项的表示无法充分捕捉工具间互补关系。这是支持核心结构主张最直接的消融，但它同时移除了一个较大的功能模块，不能进一步区分该模块内部究竟哪种交互形式贡献最大。 | 第3.3节 Ablation Study，Table 2(a)<br><span class="experiment-evidence">Removing F_set reduces COMP@5 by 13.1% and Pass Rate by 16.8%, showing that joint set scoring drives the gains.</span> |
| 基数相关交互矩阵对比共享矩阵、恒等矩阵及去正则化 | 完整模型为84.75±0.09% Recall@5、77.55±0.12% COMP@5和69.69±0.61% Pass Rate；改用共享矩阵后降至78.43±0.20%、73.66±0.08%和64.37±0.69%，使用恒等矩阵则进一步降至75.05±0.16%、68.68±0.15%和59.92±0.71%。去掉正则化后的结果为83.17±0.07%、75.34±0.13%和68.93±0.64%。 | 共享矩阵保留了可学习的工具交互，却不再根据集合大小选择不同参数，因此它与完整模型的差距主要隔离“基数条件化”的价值；恒等矩阵进一步取消了可学习兼容性，表现更差。结果支持这样的直观解释：两个工具在小集合中可能构成核心互补，而在更大集合中可能冗余或需要其他工具配合，因此兼容性不应被视为与集合大小无关。去正则化的较小下降还表明，正则项有帮助，但不是主要收益来源。 | 第3.3节 Ablation Study，Table 2(b)<br><span class="experiment-evidence">Replacing cardinality-specific matrices with a learned shared matrix reduces performance, and identity matrices perform worse still. These results confirm that compatibility should vary with set size.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：reused verified category during targeted regeneration
- 全文指纹：`92900626aea9e517ab60e44a85b7ade753c4b0a40033e5c377e496140dc2b067`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
