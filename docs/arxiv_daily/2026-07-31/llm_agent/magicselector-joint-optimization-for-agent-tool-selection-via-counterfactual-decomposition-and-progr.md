---
title: "[论文解读] MagicSelector: Joint Optimization for Agent Tool Selection via Counterfactual Decomposition and Progressive Reranking"
description: "[arXiv 2607.17751][LLM Agent] MagicSelector面向移动智能体的复杂工具检索，将任务分解、精细重排序与候选截断联合起来，重点解决分解奖励缺乏因果归因、相似工具难区分以及固定$K$造成召回与噪声难以兼顾的问题。"
arxiv_id: "2607.17751"
announcement_date: "2026-07-31"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.463166+00:00"
source_sha256: "eb9b6af8d984c4c38df7fe0a1d65528319f1b708b17208cb996f1237a217e6f7"
tags:
  - "LLM Agent"
  - "移动智能体"
  - "工具检索"
  - "任务分解"
  - "工具重排"
  - "动态Top-K"
  - "分布外泛化"
  - "静态知识注入"
  - "上下文效率"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2607.17751</p>

# MagicSelector: Joint Optimization for Agent Tool Selection via Counterfactual Decomposition and Progressive Reranking

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> HONOR Agentic Search Team, Chen, Zhengzong, Tang, Lei, Liu, Lijun, Jiang, Chuandi, Yang, Fan, Chu, Keyun, Zhao, Chu, Liu, Shihao, Li, Minghang, Liang, Bo, Wen, Can, Wu, Hailong, Ju, Jingnan, Liu, Mian, Zhang, Nengbin, Wang, Peiqiang, Nie, Penghe, Gu, Qinhui, Lv, Sijia, Chen, Siqi, Zhang, Wei, Xu, Yang, Qian, Yuhao, Zhang, Yuxiang, Cheng, Zeng, Wang, Zhen, Chen, Zuan, Zhao, Yuanyuan, Huang, Fei</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> HONOR</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.17751) · [PDF 下载](https://arxiv.org/pdf/2607.17751) · **关键词** 移动智能体, 工具检索, 任务分解, 工具重排, 动态Top-K, 分布外泛化, 静态知识注入, 上下文效率<br>


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

MagicSelector面向移动智能体的复杂工具检索，将任务分解、精细重排序与候选截断联合起来，重点解决分解奖励缺乏因果归因、相似工具难区分以及固定$K$造成召回与噪声难以兼顾的问题。

**不用术语来说**：移动智能体收到的指令常包含多轮上下文、模糊指代或多个任务，而工具库中的每个工具通常只对应一个具体操作；若直接用整段指令查找工具，语义便难以准确匹配。系统也不能把全部工具说明交给大模型，因为这会增加延迟和上下文开销，并可能让真正需要的工具被大量无关信息干扰。因此，实际系统需要先把复杂指令拆成可执行的小任务，再从大量功能相近的工具中准确选出必要项，同时控制送入模型的候选数量。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出偏好引导的反事实任务分解：比较采用分解与不采用分解时检索排序的相对变化，以分解带来的边际排序增益作为学习信号，试图让模型学习对检索真正有帮助且结构合理的原子子任务，而不是通过重复表达等捷径迎合静态结果指标。
- 作者将渐进式重排序与双语义边界动态Top-K结合：前者通过自蒸馏挖掘高分但错误的困难负例，并同时学习单工具相关性和候选列表内的相对次序；后者依据重排序分数突降与相邻工具语义变化自适应确定$K$，以兼顾关键工具召回、长尾噪声过滤和上下文效率。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究自主智能体中的工具检索，具体场景是移动智能体根据用户对话，从规模不断增长的外部工具库中选择可执行工具。移动交互常同时包含多轮上下文、指代不明和单句多任务，而工具通常以功能说明和严格的调用模式存在；受大语言模型上下文窗口、推理延迟和执行安全约束，系统不能将全部工具说明直接注入上下文。论文因此采用静态知识注入设定：先把复杂指令分解为可执行的原子子任务，再检索并重排候选工具，最后截断候选列表。这里的核心矛盾是既要召回完成所有子任务所需的工具，又要排除功能相近的错误工具和长尾噪声，尤其要在包含未见工具的分布外场景中保持泛化能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**任务分解**

将包含多个目标、跨轮信息或模糊指代的用户指令，转换成语义明确且可分别执行的原子子任务。它在本文中承担检索前的规划作用，使复杂自然语言需求能够与原子工具的功能描述对齐。

</div>
<div class="concept-item" markdown="1">

**工具检索与重排**

工具检索先从静态工具库中快速取得候选集合，重排模型再结合子任务与工具说明，对候选工具的相关性进行更细致的比较。本文关注的困难是多个工具可能共享相似表述，却只有少数工具在功能、参数模式和执行语义上真正匹配。

</div>
<div class="concept-item" markdown="1">

**分布外泛化**

分布外（OOD）泛化指模型面对训练阶段未出现的工具或不同于训练数据的交互模式时，仍能正确分解任务并选出所需工具。若模型只利用分解文本的表面特征与检索分数之间的偶然相关性，其域内结果可能较好，但遇到未见工具时容易失效。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一段移动场景中的用户交互，可为单轮指令、多轮对话，或在一个话语中包含多个任务；系统同时拥有一个静态原子工具库，每个工具由可供匹配的功能文档及调用模式描述。目标是把交互解析为逻辑连贯、无重复且可执行的原子子任务，以各子任务检索候选工具并进行精细重排，再根据候选之间的相关性边界动态确定返回数量，而不是预先固定 $K$。最终输出应覆盖完成用户目标所必需的工具，同时尽量减少错误工具和长尾工具说明进入大模型上下文，从而兼顾检索准确性、工具召回、上下文效率与执行安全。论文假设实际移动系统更偏向低延迟的静态注入，而非让智能体在执行时持续主动发现工具；它还特别考察训练中未见工具的 OOD 设置。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$K$**

候选工具列表的截断数量；传统方法使用固定值，本文所述问题要求依据候选相关性边界动态确定该值。

</div>

</div>

**直接相关的工作**

- **Schick et al. (2023), Patil et al. (2024), Qin et al. (2024a)**: 这些工作代表静态工具知识注入范式，即预先从工具库检索少量工具并放入模型上下文。MagicSelector沿用这一适合低延迟移动系统的基本设定，但面向多轮、多任务复杂指令加入任务分解、精细重排和动态截断。
- **Gangi Reddy et al. (2024), Yoon et al. (2024), Zhi et al. (2026)**: 论文将这些工作归入传统工具重排方法，并指出其在异构用户查询与工具文档之间缺少充分的深层词元级交互；若训练主要依赖随机负样本，也难以区分功能高度相似的工具。该判断是本文引入渐进式重排与困难负样本挖掘的直接背景。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

移动智能体需要在快速增长的外部工具库中处理多轮、含混和多任务指令。动态获取工具虽然能探索开放环境，但会增加系统延迟；静态注入更适合低延迟且要求工具模式精确匹配的移动场景，却受到有限上下文窗口约束，无法一次提供全部工具说明。复杂用户指令与原子工具文档之间还存在粒度和语义错位，使工具检索成为影响执行准确性、安全性与成本的关键瓶颈。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于提示、监督微调或结果奖励的任务分解**：这类方法先让模型把复杂指令改写为若干子任务，再用子任务检索原子工具。提示法依靠预设指令，监督微调学习标注分解，强化学习方法则依据最终检索指标优化分解策略；其共同目标是让分解结果更容易匹配工具库。
- **传统重排序与固定Top-K截断**：系统先召回一批候选工具，再按查询与工具文档的相关性分数重新排序，并保留预先设定的前$K$项。传统训练常使用随机负例，而固定$K$对所有查询采用相同候选规模，因而实现简单、延迟较稳定。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有分解优化缺少对“分解本身带来了多少检索改善”的因果归因：提示法和监督微调容易累积上游错误，静态结果奖励又可能诱导模型利用重复分解或浅层文本相关性等捷径。其后果是训练指标可能提高，但分解未必逻辑正确，并且在包含未见工具的域外场景中容易失效。
- 传统重排序缺少充分的细粒度交互，随机负例也往往过于容易，难以区分描述相似但功能不同的工具；在此基础上，固定Top-K进一步形成两难：较小的$K$会漏掉必要工具，较大的$K$会引入长尾噪声、增加推理开销，并加剧“中间信息被忽略”的上下文干扰。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有工作通常分别处理任务分解、候选重排序或结果截断，却缺少一个以最终工具检索质量为共同目标的联合机制：上游需要能够识别分解的真实边际价值，中游需要从模型自身的高置信错误中学习相似工具边界，下游还需要随查询和候选分布变化确定候选规模。与此同时，既有基准缺少面向移动多轮交互的过程级分解标注，因而难以系统检验分解质量如何影响后续检索。

</div>
<div markdown="1"><span>核心问题</span>

如何构建一条适用于复杂移动交互的静态工具检索流水线，使模型能够把含混、多轮或多任务指令可靠地分解为原子子任务，准确辨别功能高度相似的候选工具，并针对每个查询自适应选择$K$，从而同时改善域内与域外检索、关键工具保留和上下文效率？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是让每个阶段都围绕“哪些信息真正改变了正确工具的排序”学习。若去掉某次分解后排序明显变差，就说明该分解提供了实际增益，这比只看最终得分更能抑制无效重复；若模型把错误工具排得很高，这些错误正好暴露其最难掌握的功能边界，可作为高价值负例反复训练；最后，当排序分数出现断崖或相邻工具的语义明显改变时，该位置很可能对应相关候选与长尾噪声的分界，因此可据此动态停止，而不必为所有查询机械地使用同一个$K$。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MagicSelector将工具选择组织为“任务原子化、候选工具检索与重排、动态截断”的联合流程。训练阶段先输入多轮上下文$x=(H,q)$，其中$H$是历史对话、$q$是当前请求；分解策略生成若干原子子任务，再以“不分解时的检索结果”为反事实基线，计算分解带来的排序增益与完整覆盖增益，同时由过程奖励模型评价分解的语义质量，最终通过GRPO更新分解策略。推理阶段使用训练后的策略把复杂请求改写为原子任务，分别检索并融合候选工具；候选列表经渐进式重排后，再依据相邻工具的重排分数断崖和功能语义断层自适应确定$K$，输出较短且尽量完整的工具集合。
直观地说，该方法不直接让一个含糊的长请求与整个工具库硬匹配，而是先把它拆成可执行的小请求，并用实际检索效果反过来判断“拆得是否有用”。随后，它在相似工具中进一步辨别真正相关项，并寻找候选列表从“有用工具”进入“长尾噪声”的边界，以减少送入后续智能体上下文的无关工具；不过，所给章节未包含第4章渐进式重排的具体算法，因此该环节只能按原文已明确的接口描述，不能完整复现。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多轮上下文编码与原子任务生成

分解策略$\pi_\theta(\cdot\mid x)$为同一输入采样候选分解$y_i$，并将其解析为原子任务集合$\mathcal{A}(y_i)=\{a_1,\ldots,a_m\}$。分解需要处理多意图、上下文继承和指代关系，使每个$a_j$尽量对应单一、可检索的工具需求。

<div class="method-step__io" markdown="1">

**输入**：多轮输入$x=(H,q)$，其中$H$为已有对话历史，$q$为当前轮用户请求；训练时还提供目标工具集合$\mathcal{G}$。<br>
**输出**：一个或多个候选分解$y_i$及其原子任务序列$\mathcal{A}(y_i)$。

</div>

**直观理解**：这一步类似把“接着订票并通知刚才那个人”拆成若干明确动作，同时补全“刚才那个人”等上下文信息。拆分不是仅追求语句自然，而要让后续工具检索真正变得更准确。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 反事实检索评估与偏好联合训练

系统分别计算原始输入的列表$T_{\mathrm{raw}}^K=\mathcal{R}_K(x)$和逐个检索原子任务后经去重、融合得到的$T_{\mathrm{atom}}^K$，用NDCG@K及目标工具完整覆盖情况度量分解的边际收益；同时，过程奖励模型从完整性、准确性、指代消解、规范表达和上下文一致性五个维度比较候选分解与人工参考$y^\star$。两类奖励融合后，GRPO在每组$B$个候选内部标准化奖励并更新$\pi_\theta$，无需另训价值网络。

<div class="method-step__io" markdown="1">

**输入**：原始上下文$x$、候选分解$y_i$、目标工具集合$\mathcal{G}$、检索器$\mathcal{R}_K$和过程奖励模型$s_\phi$。<br>
**输出**：能够兼顾下游检索收益和分解语义质量的任务原子化策略$\pi_\theta$。

</div>

**直观理解**：原始请求的检索结果相当于“不拆分”的对照组，只有拆分后排序更好或覆盖更多必要工具，策略才得到相应奖励。语义偏好奖励则防止模型通过不完整、逻辑混乱但偶然命中工具的拆法获得高分。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分任务检索、融合与渐进式重排

检索器对各$a_j$独立召回工具，随后去重并融合为候选集合，再由渐进式工具重排模块产生降序列表$T=[t_1,\ldots,t_n]$、查询相关性分数$S=[s_1,\ldots,s_n]$及工具描述向量$E=[e_1,\ldots,e_n]$。摘要称该模块通过自蒸馏困难负例挖掘联合优化逐点相关性与列表级排序，但所给正文没有提供其损失函数、训练阶段或融合规则。

<div class="method-step__io" markdown="1">

**输入**：训练后策略生成的原子任务$a_j$以及工具库中的工具描述。<br>
**输出**：按相关性降序排列的工具列表$T$、重排分数$S$和描述嵌入$E$。

</div>

**直观理解**：初检索负责尽量不漏掉候选，重排负责在功能名称或描述高度相似的工具之间做精细比较。由于关键章节缺失，不能从当前材料判断困难负例如何构造，也不能确认逐点与列表级目标怎样加权。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双语义边界动态Top-K截断

算法先寻找相邻分数最大下降处$K_{\mathrm{score}}$，再计算相邻工具描述的余弦相似度$sim_i$并寻找相似度序列最大下降处$K_{\mathrm{sim}}$；最终取$K_{\mathrm{final}}=\max(K_{\mathrm{score}},K_{\mathrm{sim}})$。该保守融合只需扫描相邻项，原文给出的时间复杂度为$O(n)$。

<div class="method-step__io" markdown="1">

**输入**：重排列表$T=[t_1,\ldots,t_n]$、对应分数$s_i=\mathrm{score}(q,t_i)$和工具描述嵌入$e_i$。<br>
**输出**：最终工具列表$T_{\mathrm{final}}=\{t_1,\ldots,t_{K_{\mathrm{final}}}\}$，供后续智能体决策或工具调用。

</div>

**直观理解**：一个边界观察“工具与请求的匹配分是否突然变差”，另一个观察“相邻工具的功能是否突然换了一类”。选择两个边界中更靠后的一个，是用少量额外候选换取更低的漏召回风险。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 反事实奖励与偏好奖励的联合训练信号

$$
R=\alpha\,\sigma\!\left(s_{\phi}(x,y_i)-s_{\phi}(x,y^{\star})\right)+\beta\!\left[\lambda_{\mathrm{ndcg}}\max\!\left(0,N_{\mathrm{atom}}-N_{\mathrm{raw}}\right)+\lambda_{\mathrm{full}}\!\left(\mathbb{I}[\mathcal{G}\subseteq T_{\mathrm{atom}}^{K}]-\mathbb{I}[\mathcal{G}\subseteq T_{\mathrm{raw}}^{K}]\right)\right]
$$

**符号说明**

- $R$：用于策略优化的总奖励。
- $x=(H,q)$：由历史对话与当前用户请求组成的多轮上下文。
- $y_i$：分解策略生成的第$i$个候选任务分解。
- $y^{\star}$：人工标注的参考分解。
- $s_{\phi}(x,y)$：过程奖励模型对给定上下文和分解结果的偏好得分。
- $\sigma$：Sigmoid函数，将候选与参考的得分差映射为偏好奖励。
- $N_{\mathrm{raw}}$：不进行任务分解时，原始检索列表相对目标工具的NDCG@K。
- $N_{\mathrm{atom}}$：按原子任务检索并融合后，工具列表相对目标工具的NDCG@K。
- $\mathcal{G}$：当前样本所需的目标工具集合。
- $T_{\mathrm{raw}}^{K}$：直接用原始上下文检索得到的Top-K工具列表。
- $T_{\mathrm{atom}}^{K}$：逐原子任务检索、去重和融合后得到的Top-K工具列表。
- $\mathbb{I}[\cdot]$：指示函数，条件成立时取1，否则取0。
- $\lambda_{\mathrm{ndcg}},\lambda_{\mathrm{full}}$：分别控制正向排序增益和完整覆盖增益的权重。
- $\alpha,\beta$：分别控制偏好奖励与反事实奖励在总奖励中的权重。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把“分解是否符合语义规范”和“分解是否实际改善工具检索”合成同一个学习信号。排序项截断负增益，主要奖励优于原始请求的分解；覆盖项直接比较分解前后能否在Top-K内找齐目标工具，从而防止模型为了提升前几个位置而遗漏必要工具。<br>
**原文位置**：第3.2.2节反事实奖励定义、第3.3节公式(5)与公式(6)；此处按原文数学含义将三式合并展开。

</div>

</div>

<div class="equation-block" markdown="1">

#### 双边界动态Top-K融合

$$
K_{\mathrm{score}}=\underset{1\le i<n}{\arg\max}\,(s_i-s_{i+1}),\qquad K_{\mathrm{sim}}=\underset{1\le i<n-1}{\arg\max}\,(\mathrm{sim}_i-\mathrm{sim}_{i+1}),\qquad K_{\mathrm{final}}=\max(K_{\mathrm{score}},K_{\mathrm{sim}})
$$

**符号说明**

- $s_i$：查询$q$与降序列表中第$i$个工具$t_i$的重排相关性分数。
- $\mathrm{sim}_i$：相邻工具$t_i$与$t_{i+1}$的功能描述嵌入余弦相似度。
- $K_{\mathrm{score}}$：相邻重排分数下降幅度最大的位置。
- $K_{\mathrm{sim}}$：相邻工具语义连贯性下降幅度最大的位置。
- $K_{\mathrm{final}}$：综合两个边界后采用的最终截断位置。
- $n$：重排候选工具的总数。

<div class="equation-explanation" markdown="1">

**直观理解**：最大分数差尝试找到列表从高相关头部跌入低相关长尾的位置，最大语义差则尝试找到工具功能簇发生明显切换的位置。取两者的最大值会选择更靠后的边界，虽然可能多保留少量工具，但更符合工具检索优先避免漏掉正确工具的目标。<br>
**原文位置**：第5.2节公式(27)、公式(28)、公式(29)及Algorithm 2。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练的直接目标是最大化融合奖励$R=\alpha R_{\mathrm{pref}}+\beta R_{\mathrm{cf}}$。对每个输入$x_t$，旧策略$\pi_{\theta_{old}}$采样$B$个候选，并将每个奖励在组内标准化为优势$A_i=(R_i-\mathrm{mean}(\mathbf{R}))/(\mathrm{std}(\mathbf{R})+\epsilon)$；GRPO再采用裁剪的重要性比率目标更新当前策略，同时用相对参考模型$\pi_{ref}$的KL散度抑制策略漂移。这样无需单独训练Critic：同一请求下的候选彼此充当相对基准，高于组平均的分解被强化，低于组平均的分解被抑制；其中反事实奖励负责下游工具排序与完整召回，偏好奖励负责结构合理性和指令遵循。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 偏好引导的反事实任务分解**

模块以原始检索质量$N_{\mathrm{raw}}$为无干预基线，将原子化后的检索质量$N_{\mathrm{atom}}$与其比较，只对正向NDCG增益提供稠密奖励，并通过$\mathcal{G}$是否被Top-K完整覆盖施加完整性约束。过程奖励模型$s_\phi(x,y)$另行评价分解结构，以候选$y_i$相对人工参考$y^\star$的得分差形成偏好奖励。

> 直观理解：这个模块回答的不是“句子看起来是否拆开了”，而是“拆开后是否更容易找到正确工具，而且有没有漏掉必要动作”。检索反馈和语义评价分别约束实用性与逻辑质量。

**2. 自蒸馏困难负例驱动的渐进式重排**

根据摘要，该模块利用自蒸馏挖掘与正确工具高度相似的困难负例，并同时优化逐点相关性和列表级相关性，以提升细粒度工具区分能力。当前节选缺少第4章，未给出教师信号、负例采样、重排模型结构、损失函数和推理轮次，因而无法进一步核实或复现。

> 直观理解：普通负例往往与请求明显无关，模型很容易排除；困难负例则可能只在参数、权限或功能边界上与正确工具不同。专门学习这些近似候选，有助于避免“看起来都相关”时排错顺序。

**3. 双语义边界感知动态Top-K**

模块把降序重排列表视作一维语义序列，以最大相邻分数差定位查询相关性边界，以相邻工具嵌入的余弦相似度变化定位功能簇边界，并取两者较大的截断位置。其设计依据是原文观察到重排分数呈近似Pareto长尾，即少量头部工具高相关、大量尾部工具弱相关。

> 直观理解：固定$K$无法同时适应简单请求和多任务请求：取值太小会漏工具，太大则把无关描述塞入上下文。动态边界让简单请求早停、复杂请求保留更多候选，而取较大边界体现了工具检索对漏召回的低容忍度。

**训练与推理**

训练时，先为输入$x=(H,q)$计算不分解的检索基线$T_{\mathrm{raw}}^K$与$N_{\mathrm{raw}}$；再由策略批量采样候选分解，解析原子任务，逐任务检索并去重融合为$T_{\mathrm{atom}}^K$，计算$N_{\mathrm{atom}}$、完整覆盖变化及过程偏好得分。联合奖励在组内转化为相对优势，随后通过带裁剪与KL约束的GRPO更新分解策略。MTDTool的数据构造还以状态机显式记录上下文、原子任务和工具映射，可为分解与检索提供过程级监督，但节选未明确说明哪些字段具体进入每个训练阶段。
推理时，给定历史$H$和当前请求$q$，训练后的策略输出原子任务$a_j$；检索器分别召回工具并融合候选，渐进式重排器生成有序列表、相关性分数和工具描述嵌入。动态Top-K模块在线扫描相邻分数差与相邻语义变化，计算$K_{\mathrm{score}}$和$K_{\mathrm{sim}}$，取二者最大值后返回前$K_{\mathrm{final}}$个工具。此流程的最终输出是供智能体使用的精简候选工具列表，而不是直接执行工具或生成最终自然语言答复。

**复现信息**

为公平理解该方法，需要保留三项实现边界。第一，反事实评估中的原始检索和原子任务检索必须使用同一检索器$\mathcal{R}_K$、同一目标集合$\mathcal{G}$及一致的NDCG@K定义，否则增益不能归因于任务分解；原子任务的多个检索结果还需在计算$N_{\mathrm{atom}}$前去重和融合。第二，动态截断要求重排分数按降序排列，并为每个工具功能描述计算嵌入；算法只比较相邻项，因此时间复杂度为$O(n)$，而非全局两两比较的$O(n^2)$。第三，数据构造中的话题切换概率采用$P_{\mathrm{switch}}(r)=\max(p_{\min},p_0\alpha^{r-1})$，节选明确给出$p_0=0.10$、$\alpha=0.85$、$p_{\min}=0.01$，其用途是让早期轮次保持一定主题多样性、后期更倾向上下文连续；但这属于MTDTool生成设置，并非MagicSelector推理时的超参数。当前材料未报告策略模型、检索器、重排器和嵌入模型的具体型号，也未报告$K$、$B$、奖励权重、GRPO裁剪系数及训练资源；渐进式重排章节亦缺失，因此这些部分均应标记为“原文未明确报告”，不能据此完成严格复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ToolBench：真实 RESTful API 工具调用基准，包含 49 个类别、16,464 个 API 和约 12.6 万个指令—解答对，覆盖单工具与多工具任务。实验按 I1–I3 三个指令难度以及 Instruction、Tool、Category 三种泛化划分评估，并区分同域训练测试与全数据训练的多域设置。它主要检验模型能否从大规模结构化 API 库中找到执行任务所需的前置工具。
- ToolRet：汇集 Web、Code 和 Customized 三类领域、共 35 个数据集与约 4.4 万个工具的大规模检索基准。训练集包含 1 万个 Web 领域合成轨迹样本；3,100 个 Web 样本构成同域测试，其余样本用于域外评估。实验采用 instruction-augmented 格式并从完整工具库检索，用于检验异构工具库中的规模化检索与跨领域泛化。
- MTDTool：作者为复杂多轮移动交互构建的基准，包含 237 个垂直领域工具，并依据工具所属垂直领域划分同域和域外测试集。它强调多轮上下文、复合用户意图及未见工具领域，是检验任务分解和域外鲁棒性的核心数据集；摘录未明确给出训练集、测试集的具体样本数。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**NDCG@$k$**

归一化折损累计增益，衡量前 $k$ 个结果的排序质量：相关工具越靠前，得分越高。ToolBench 报告 $k\in\{1,3,5\}$，ToolRet 与 MTDTool 主要报告 NDCG@10；摘录中的表格将其简写为 N@$k$。 （越高越好，因为它同时奖励检索到相关工具和把相关工具排在列表前部。）

</div>
<div class="metric-item" markdown="1">

**Recall@10**

衡量前 10 个候选中找回了多少应检索的相关工具，主要反映候选集合的召回能力。该指标在 ToolRet 配置中报告；MTDTool 的总体表述虽提到 Recall@10，但所给表格主要展示 NDCG@10 与 Completeness@10。 （越高越好，因为遗漏任务所需工具的概率更低。）

</div>
<div class="metric-item" markdown="1">

**Completeness@10**

衡量前 10 个结果对任务所需工具集合的完整覆盖程度，适合存在多个必要工具的复合任务。原文摘录未给出其严格数学定义，因此不能仅凭本节判断它与 Recall@10 的具体计算差别。 （越高越好，因为候选列表更可能覆盖完成任务所需的全部工具，而不只是命中其中一部分。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### ToolRet 完整工具库上的跨 Web、Code 与 Customized 平均结果

<div class="result-value" markdown="1">

完整流水线达到 NDCG@10 59.90、Completeness@10 59.21；作为最强的直接对照之一，Tool-DE-Rerank-4B 在表 5 中为 57.01 和 56.98。作者据此主张 MagicSelector 在大规模异构工具检索上达到最佳总体表现。

</div>

结果说明分解、检索和重排序的组合不仅提高了前列排序质量，也提高了必要工具的覆盖程度，并且优势并非只来自单一 Web 领域。不过，表中不同方法可能采用不同规模的模型或训练资源，且本节没有显著性检验，因此不能把约 2 至 3 个点的领先直接解释为在所有查询上都稳定占优。

<div class="result-source" markdown="1">

来源：第 6.4 节，表 1 与表 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

It sets a new state-of-the-art across the datasets, peaking at 59.90 N@10 and 59.21 C@10 on ToolRet, and 96.28 N@10 and 96.01 C@10 on MTDTool.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### MTDTool 按工具垂直领域划分的同域与域外测试

<div class="result-value" markdown="1">

完整系统在同域测试上取得 NDCG@10 97.22、Completeness@10 95.33，在域外测试上取得 NDCG@10 95.33、Completeness@10 96.69，均为表 2 的最佳结果。相较 Qwen3-Embedding-4B 加通用 Qwen3-Reranker-4B，域外 NDCG@10 从 77.52 提高到 95.33，Completeness@10 从 81.48 提高到 96.69。

</div>

这是最直接支持域外泛化主张的实验：测试工具来自训练划分之外的垂直领域，完整方法仍能把相关工具排在前列并保持较完整覆盖。它说明专用分解和重排序对多轮移动任务有效，但域外划分仍来自同一个自建数据集，不能据此推断系统已经适用于任意真实移动平台或全新工具生态。

<div class="result-source" markdown="1">

来源：第 6.4 节，表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

After integrating both components, the full pipeline Ours achieves the best in-domain results with 97.22 N@10 and 95.33 C@10, and the best out-of-domain performance with 95.33 N@10 and 96.69 C@10, suggesting that decomposition can further improve ranking when user instructions involve multi-turn or compound intents.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### ToolBench 的同域与多域 API 工具检索

<div class="result-value" markdown="1">

完整方法在同域设置的九项 I1–I3、NDCG@$1/3/5$ 组合上平均达到 96.6，在多域设置平均达到 88.5；表 3 和表 4 中最强对照分别为 E5-Mistral-7B-Instruct 加 Qwen3-Reranker-8B 的 93.3，以及 ToolOmni 的 78.3。

</div>

同域结果表明模型能在真实 API 指令中精确定位前置工具，多域结果则显示其在更混杂的候选空间中仍保持明显优势。两种设置间平均分由 96.6 降至 88.5，也说明跨域混合检索仍更困难；此外，这些指标只评价工具排序，没有直接证明后续 API 参数生成、调用执行或任务成功率同样提升。

<div class="result-source" markdown="1">

来源：第 6.4 节，表 3 与表 4；具体数值来自对应完整表格行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

MagicSelector consistently achieves state-of-the-art performance, demonstrating superior efficacy over both prompting-based methods and specialized dense retrievers.

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

- 闭源大模型 GPT-5.0、MiniMax-M2.5 和 DeepSeek-V4-Pro：以零样本或少样本方式直接处理任务，用于提供通用大模型能力的高水平参照；但它们与 MagicSelector 的训练数据、参数规模和推理成本并未完全对齐，因此不是严格控制变量比较。
- 提示式方法 Q2E、ReInvoke、ToolReAGt 和 PLUTO：通过查询扩展、结构化检索增强或思维链改善工具检索，不需要针对任务进行专门训练。该组比较用于判断 MagicSelector 的收益是否超过仅改写提示或增加推理步骤所能获得的提升。
- 强化学习方法 ToolQP：利用混合奖励联合优化任务分解与工具检索，是与 MagicSelector 最接近的联合优化基线。它用于检验反事实分解监督和后续专用重排序是否优于已有的混合奖励联合训练。
- 稠密检索与重排序系统：包括 gte-Qwen2-7B-instruct、E5-Mistral-7B-Instruct，以及接入 Qwen3-Reranker-8B 的版本；ToolBench 和 ToolRet 还报告 BM25、ToolRetriever、ToolOmni、Tool-DE 等任务相关基线。该组用于区分收益究竟来自更强的基础语义检索能力，还是来自 MagicSelector 的分解和重排序设计。

**实验想回答的问题**

- 在完整工具库检索条件下，MagicSelector 能否在 ToolBench、ToolRet 与 MTDTool 三类互补场景中，比提示式方法、强化学习方法和强稠密检索器更准确地找回并排序相关工具？
- 反事实任务分解与专用渐进式重排序分别带来多少增益，这些增益能否延伸到按工具垂直领域划分的域外场景，并改善复合意图或多轮指令下的工具覆盖？

**实验实现**

默认系统使用 Qwen3-Embedding-4B 做稠密初检，并使用 Qwen3-Reranker-4B 做交叉编码器重排序。ToolBench 在 I1–I3 难度、同域和多域条件下评估，默认采用开放域协议，即每个查询面向完整工具语料库，而非预过滤 API 列表；ToolRet 遵循 Tool-DE 的 instruction-augmented 设置，同样从完整工具库检索；MTDTool 按工具垂直领域划分同域与域外测试。报告配置分为仅嵌入检索、嵌入加重排序，以及在检索前进一步加入任务分解的完整流水线。摘录未明确报告随机种子、重复运行次数、置信区间、显著性检验、训练超参数和推理硬件。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 在 Ours-Embedding-4B 上加入 Ours-Rerank-4B，不加入任务分解 | MTDTool 的 NDCG@10 从 91.36 提高到 96.00，增益为 4.64 个点；Completeness@10 从 87.65 提高到 95.71，增益为 8.06 个点。ToolRet 的 NDCG@10 和 Completeness@10 也分别从 54.23、53.71 提高到 59.44、58.90。 | 该比较主要隔离专用重排序器的贡献：初检候选保持不变，变化来自对候选的细粒度重新打分。Completeness@10 的提升大于 NDCG@10，表明重排序尤其有助于把多个必要工具共同推入前 10；但训练重排序器时使用的自蒸馏与难负例策略未在该表中进一步拆开，因此不能确定每个内部设计各自贡献多少。 | 第 6.4 节，表 1<br><span class="experiment-evidence">This addition boosts the N@10 on MTDTool from 91.36 to 96.00, and significantly improves performance across ToolBench to achieve the highest N@1 score of 85.7.</span> |
| 在 Ours-Embedding-4B 加 Ours-Rerank-4B 的基础上进一步加入 Ours-Decomp | ToolRet 的 NDCG@10 从 59.44 提高到 59.90、Completeness@10 从 58.90 提高到 59.21；MTDTool 分别从 96.00、95.71 提高到 96.28、96.01。ToolBench 的 NDCG@3 保持 90.7，NDCG@5 从 90.6 提高到 90.8，但 NDCG@1 从 85.7 降至 84.2。 | 该比较隔离检索前任务分解的边际作用。分解对 ToolRet 和 MTDTool 带来小而一致的总体增益，并稍微改善 ToolBench 较宽候选列表的覆盖；首位指标下降则提示把一个复合查询拆成多个原子子任务可能分散最高位排序信号。因此，实验支持“分解有利于多工具覆盖”，但不支持“分解在所有排序截断点都必然更好”。 | 第 6.4 节，表 1<br><span class="experiment-evidence">On ToolBench, the decomposition strategy provides crucial additional gains for broader candidate pools, reaching top results of 90.7 N@3 and 90.8 N@5.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向LLM Agent的任务分解、工具检索重排序与动态Top-K选择框架。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`eb9b6af8d984c4c38df7fe0a1d65528319f1b708b17208cb996f1237a217e6f7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
