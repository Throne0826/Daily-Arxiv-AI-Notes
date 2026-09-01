---
title: "[论文解读] Call Neighbours Yourself: Graph Walks with Destination-Conditioned On-Policy Self-Distillation"
description: "[arXiv 2608.29588][LLM Agent] 原文未明确报告。"
arxiv_id: "2608.29588"
announcement_date: "2026-09-01"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:41:10.944063+00:00"
source_sha256: "5334f007a38fdbeac1f1b10c6135baa022110b045c4803d45f4b834bf730286e"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "LLM 其他"
  - "文本属性图（TAG）"
  - "大语言模型图推理"
  - "主动邻居探索"
  - "图游走"
  - "在策略自蒸馏"
  - "信用分配"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2608.29588</p>

# Call Neighbours Yourself: Graph Walks with Destination-Conditioned On-Policy Self-Distillation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Yilun Liu, Boyu Luo, Yanran Tang, Ruihong Qiu, Zi Huang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: School of Electrical Engineering and Computer Science；Affiliation: The University of Queensland</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.29588v1) · [PDF 下载](https://arxiv.org/pdf/2608.29588v1) · **关键词** 文本属性图（TAG）, 大语言模型图推理, 主动邻居探索, 图游走, 在策略自蒸馏, 信用分配<br>
**代码**: [https://github.com/superallen13/CNY](https://github.com/superallen13/CNY)

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

本文研究文本属性图（text-attributed graph，TAG）上的大语言模型（LLM）推理。TAG 是一种图结构数据：每个节点不仅有与任务相关的自由文本，还通过边连接到其他带文本节点；模型需要联合目标节点文本、邻域结构和邻居文本来完成节点或图级任务。现有方法通常在生成前预先选定邻居并将其拼接为固定上下文，而本文将邻居获取视为推理过程中的主动证据采集：模型先查看邻居的轻量预览，再依据当前推理状态决定是否沿图结构访问某个邻居。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**文本属性图（TAG）**

TAG 中的节点同时包含文本内容和图连接关系，例如论文及其引用关系、网页及其超链接关系。完成任务时，模型不能只读目标节点，还可能需要从相邻节点获取证据。

</div>
<div class="concept-item" markdown="1">

**图游走与邻域前沿**

图游走是从当前节点沿已有边访问另一个节点；本文把“访问哪个邻居”建模为模型可以执行的动作。邻域前沿指当前已经暴露、但尚未深入读取的候选邻居集合，访问一个候选节点后，环境会返回其文本并扩展可继续探索的范围。

</div>
<div class="concept-item" markdown="1">

**固定上下文与主动检索**

固定上下文方法在生成开始前一次性选定邻居，因此推理过程中无法根据新发现的证据修正检索范围。主动检索则把信息获取嵌入生成过程，使模型能够先看摘要或文本前缀，再决定是否读取完整邻居内容。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个文本属性图、一个目标节点及其任务指令，模型首先获得目标节点文本和候选邻居的轻量预览，而不是预先获得完整的固定邻居集合。模型在生成推理文本的过程中可以输出受图拓扑约束的 <walk> 动作，指定要访问的邻居；环境随后返回该目的节点的文本并更新可探索前沿。模型最终输出任务答案，训练目标还要求学习哪些邻居值得访问以及何时停止探索。该设定假定邻居访问必须遵循图中真实存在的连接，且任务答案或最终任务奖励可用，但中间每一步邻居选择没有人工标注；因此，方法需要在上下文长度有限、邻居相关性不均且证据可能分散的条件下进行自适应探索。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{TAG}$**

文本属性图，即节点带有自由文本且节点之间由图边连接的数据结构。

</div>
<div class="notation-item" markdown="1">

**$\pi_{\theta}$**

参数为 $\theta$ 的语言模型策略，表示模型在当前上下文中生成推理 token 或图游走动作的概率分布。

</div>
<div class="notation-item" markdown="1">

**$<walk>$**

模型在生成过程中发出的邻居访问动作；动作内容指定要沿图边访问的节点。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{KL}$**

反向 KL 散度，用于比较目的节点文本揭示前后的动作或 token 概率分布；本文利用这种概率变化构造图游走动作的信用信号。

</div>

</div>

**直接相关的工作**

- **Graph-R1**: Graph-R1 代表固定邻域上下文上的强化学习方法：它先将局部子图压缩为文本摘要，再使用 GRPO 微调模型。与本文的关键区别是，Graph-R1 优化的是模型如何在预先构造的上下文中推理，邻居获取本身仍由摘要或其他启发式过程决定；CNY 则让模型在生成期间通过受拓扑约束的 <walk> 动作主动选择邻居。
- **TRN-R1-Zero**: TRN-R1-Zero 在随机采样的邻域子图上进行推理，并使用邻居感知的奖励目标进行训练，但邻域仍在推理前确定。CNY 针对这一固定选择假设提出改进：模型先观察轻量邻居预览，再按需展开候选邻居，并通过目的地条件化的在策略自蒸馏为单次邻居选择提供动作级信用。

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

CNY（Call Neighbours Yourself）把文本属性图上的预测改写为“边推理、边取证”的序列决策问题。输入包括目标节点文本、候选标签描述以及初始邻居的简短预览；大语言模型依据当前上下文选择受图拓扑约束的 `<walk>` 动作，读取某个邻居的完整文本并扩展可访问前沿，或输出 `<answer>` 结束推理。这样，邻居选择不再是生成前完成的静态预处理，而成为模型推理轨迹的一部分；最终输出是目标节点的预测标签及其取证轨迹。
训练时，CNY先用分层轨迹奖励评价预测正确性、动作格式、是否成功读取证据和是否完成作答，再通过GRPO获得组内标准化的轨迹优势。其关键设计OPSD（destination-conditioned on-policy self-distillation，目的地条件化同策略自蒸馏）会在一次图游走完成后，用已揭示的目的地摘要重新评估当时选中的节点：若看到结果后模型更认可该选择，就提高对应节点ID词元的局部优势。通俗地说，普通强化学习只告诉模型“整次答题好不好”，OPSD还会事后追问“刚才打给这个邻居是否值得”，从而把延迟出现的证据价值归因到具体取证动作。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建受限初始观察

构造初始提示$q_0$，展示目标节点文本、标签语义和初始前沿中各邻居的短预览，但隐藏邻居完整文本；令$\mathcal{F}_0=\mathcal{N}(v_0)$。训练时还可对初始前沿设容量上限，以维持有限阅读预算。

<div class="method-step__io" markdown="1">

**输入**：目标节点$v_0$、其文本$x_{v_0}$、标签集合$\mathcal{Y}$及标签描述、初始一跳邻居$\mathcal{N}(v_0)$。<br>
**输出**：初始交互状态，包括提示$q_0$、空历史$h_0$和可选择前沿$\mathcal{F}_0$。

</div>

**直观理解**：模型先看到“联系人列表和简介”，却不能一次读完所有人的材料；它必须决定先向谁索取完整信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行拓扑约束图游走

模型生成 `<walk>` 节点动作或 `<answer>` 动作；合法游走只能选择$X\in\mathcal{F}_{k-1}$，随后环境揭示$x_X$，并用$X$的未读邻居更新前沿。若动作格式错误则记录该动作但不提供有效节点信息，若输出答案或达到最大跳数$T_{\max}$则终止。

<div class="method-step__io" markdown="1">

**输入**：当前提示$q_0$、历史$h_{k-1}$、前沿$\mathcal{F}_{k-1}$与当前策略$\pi_\theta$。<br>
**输出**：逐步扩充的证据历史$h_k$、更新后的前沿$\mathcal{F}_k$，以及最终答案或失败标记。

</div>

**直观理解**：每次只能沿已经接触到的图边继续探索，不能凭空跳到任意节点；读到一个节点后，才会获得继续联系其邻居的机会。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 轨迹评分与组内优势估计

按照正确预测、合法格式、成功取证和完成作答的优先级计算$R(\tau_i)$，再在同组内标准化为$\hat{A}_{\tau_i}=(R(\tau_i)-\mu_R)/\sigma_R$。这些中间层级奖励使尚未产生正确答案的训练早期也可能出现组内差异。

<div class="method-step__io" markdown="1">

**输入**：同一目标节点上由当前策略采样的$N$条轨迹$\{\tau_i\}_{i=1}^{N}$。<br>
**输出**：每条轨迹的标量奖励$R(\tau_i)$和轨迹级优势$\hat{A}_{\tau_i}$。

</div>

**直观理解**：即使模型暂时答错，也会区分“规范地查过证据再答错”和“动作混乱且没有完成回答”，避免所有错误样本得到完全相同的反馈。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 目的地条件化事后归因

同一策略先将$o$压缩为不超过$L$的摘要$\bar{o}=\varphi(o)$，且排除节点标识、类别标签和显式游走建议；随后分别在原上下文和插入目的地摘要的上下文中计算已执行节点ID词元的概率差$\delta_t$。只对游走目的地词元，将轨迹优势改为$\tilde{A}_t=\hat{A}_{\tau}+\beta\delta_t$，并对$\delta_t$停止梯度。

<div class="method-step__io" markdown="1">

**输入**：轨迹中的一次成功 `<walk>`、该动作揭示的观察$o$、原始动作上下文及策略$\pi_\theta$。<br>
**输出**：带有动作级事后信用的逐词元优势$\tilde{A}_t$。

</div>

**直观理解**：模型在看完邻居内容后回头判断：如果现在更相信当初应该选它，就奖励那次选择；摘要受到约束，是为了让反馈代表“发现了什么”，而不是泄露标签或直接命令模型选谁。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### OPSD增强的逐词元优势

$$
\tilde{A}_{t}=\begin{cases}\hat{A}_{\tau}+\beta\delta_{t},&t\in\text{walk action tokens},\\ \hat{A}_{\tau},&\text{otherwise},\end{cases}\qquad \delta_t=\log\pi_t^{\mathrm{tea}}-\log\pi_t^{\mathrm{stu}}
$$

**符号说明**

- $\tilde{A}_t$：最终用于优化第$t$个生成词元的优势值。
- $\hat{A}_{\tau}$：轨迹$\tau$的组内标准化奖励优势，对同一轨迹的普通词元共享。
- $\beta$：控制OPSD事后信用强度的系数。
- $\delta_t$：看到已访问目的地后，对已实现节点ID词元的对数概率变化；计算后从参数梯度中分离。
- $\pi_t^{\mathrm{stu}}$：策略在原始决策上下文中赋予已实现词元的概率。
- $\pi_t^{\mathrm{tea}}$：同一策略在决策前额外插入目的地摘要后赋予该词元的概率。
- $t$：生成轨迹中的词元位置；只有成功游走动作中的节点ID词元接受额外信用。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把全局结果反馈与局部事后判断相加。若目的地内容使模型更确信当时选中的邻居，即$\delta_t>0$，该动作获得额外正向信用；其他推理和回答词元不受这项自蒸馏信号影响。<br>
**原文位置**：第4.4节，式(7)与式(8)

</div>

</div>

<div class="equation-block" markdown="1">

#### 带非对称裁剪的策略优化目标

$$
\mathcal{J}(\theta)=\mathbb{E}_{\tau}\left[\frac{1}{|\tau|}\sum_t\min\left(\rho_t\tilde{A}_t,\bar{\rho}_t\tilde{A}_t\right)\right],\quad \rho_t=\frac{\pi_\theta(y_t\mid s_{<t})}{\pi_{\theta_{\mathrm{old}}}(y_t\mid s_{<t})},\quad \bar{\rho}_t=\operatorname{clip}\left(\rho_t,1-\epsilon_{\mathrm{lo}},1+\epsilon_{\mathrm{hi}}\right)
$$

**符号说明**

- $\mathcal{J}(\theta)$：需要最大化的PPO式裁剪策略目标。
- $\theta$：当前大语言模型策略的可训练参数。
- $\tau$：一次包含推理、游走、环境观察和回答的完整交互轨迹。
- $|\tau|$：轨迹中参与目标计算的词元数量，用于长度归一化。
- $y_t$：轨迹在位置$t$实际生成的词元。
- $s_{<t}$：生成$y_t$前已有的提示、历史动作、观察和文本上下文。
- $\rho_t$：当前策略与采样时旧策略对实际词元概率的比值。
- $\bar{\rho}_t$：经过非对称上下界裁剪后的重要性比率。
- $\epsilon_{\mathrm{lo}},\epsilon_{\mathrm{hi}}$：分别控制重要性比率下侧和上侧变化范围的裁剪参数。

<div class="equation-explanation" markdown="1">

**直观理解**：重要性比率允许复用旧策略采出的轨迹，而裁剪限制单次更新幅度，避免模型因少量高优势动作发生过大的概率变化。OPSD并未另建独立训练阶段，而是通过$\tilde{A}_t$直接进入这一统一目标。<br>
**原文位置**：第4.5节，式(9)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：总体目标是提高当前策略所生成轨迹的期望奖励$\mathbb{E}_{\tau\sim\pi_\theta}[R(\tau)]$，实际采用GRPO与PPO式裁剪进行近似优化。对每个目标节点采样$N$条同策略轨迹，以组内奖励均值$\mu_R$和标准差$\sigma_R$得到$\hat{A}_{\tau}$；普通词元直接使用该轨迹优势，成功游走的节点ID词元则使用加入OPSD信用后的$\tilde{A}_t$。因此，正确性与交互有效性决定全轨迹方向，目的地摘要只细化邻居选择动作的信用，不取代任务奖励，也不监督其余推理词元。
优化采用Dr. GRPO的非对称裁剪，且原文明确不加入相对参考策略的KL惩罚。OPSD中的$\delta_t$停止梯度，意味着目的地条件化分支提供固定的局部再定价信号，而不是让模型通过同时改变“教师”概率来投机降低目标；作者还将其解释为逐词元反向KL自蒸馏目标对应的梯度，但训练实现最终仍归结为对增强优势执行统一的裁剪策略更新。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 交互式图环境与动态前沿**

状态可写为$s_k=(q_0,h_{k-1},\mathcal{F}_{k-1})$。选择$X$后，前沿按$\mathcal{F}_k=(\mathcal{F}_{k-1}\setminus\{X\})\cup(\mathcal{N}(X)\setminus\mathcal{V}^{\mathrm{read}})$更新，因而新候选必须与已检查节点相邻；完整文本只有在节点被显式选择后才进入上下文。

> 直观理解：该模块把有限上下文窗口转化为主动阅读预算：模型不必吞下整个邻域，而是沿图逐步打开最可能有用的材料，同时保留访问路径的结构约束。

**2. 分层轨迹奖励与GRPO**

奖励按词典序偏好设置：正确且格式合法为$1.0$，正确但格式不合法为$0.6$，错误但格式合法且成功取证为$0.3$，错误但格式合法且未取证为$0.2$，格式不合法但完成答案为$0.1$，其余为$0$。这些数值用于实现行为排序而非校准效用；GRPO对同一目标节点的$N$条同策略轨迹做组内标准化。

> 直观理解：仅用答对或答错会让训练初期的大量错误轨迹没有可区分的信号；分层奖励先教会模型完成交互协议和实际读取证据，再由最高等级的正确性奖励主导最终目标。

**3. OPSD局部信用分配**

OPSD用同一当前策略构造学生视角和目的地条件化教师视角，并以实现动作的对数概率增量$\delta_t=\log\pi_t^{\mathrm{tea}}-\log\pi_t^{\mathrm{stu}}$衡量目的地对该动作的事后支持。该增量只加到成功游走的节点ID词元上，普通推理词元仍仅接受轨迹奖励监督。

> 直观理解：轨迹奖励很难辨别多个游走中究竟哪一步找到关键证据；OPSD把“读完后才知道是否值得”的信息送回对应选择，又避免让自蒸馏直接改写整段思维文本。

**训练与推理**

训练阶段，对批次$\mathcal{B}$中的每个目标节点并行采样$N$次交互：模型从初始前沿开始，在最多$T_{\max}$步内反复选择合法 `<walk>`、接收节点文本并扩展前沿，或生成 `<answer>`。每条轨迹先依据分层规则评分，再进行GRPO组内标准化；随后遍历其中每个成功游走，由同一策略生成目的地摘要$\bar{o}$，分别计算学生与教师上下文对节点ID词元的概率，并形成$\delta_t$和$\tilde{A}_t$。最后使用全部词元的增强优势执行一次PPO裁剪更新，训练数据采用原文第5.1节所述多任务混合，但所给节选未列出该混合的具体组成。
推理阶段不需要奖励函数、成组采样或OPSD教师视角。给定新目标节点，模型读取目标文本、标签描述和有限邻居预览，按当前策略沿真实图边逐步调用邻居；每次调用将完整节点文本加入历史并开放其未读邻居，直到生成合法答案或耗尽跳数预算。由此，训练所得探索策略可以直接用于动态取证，而不是先由另一个检索器固定上下文。

**复现信息**

参考CNY-14B配置使用Qwen2.5-14B-Instruct，GRPO组大小$N=8$、提示批量为$32$、全局批量为$256$，学习率为$1\times10^{-6}$并保持恒定；Adam参数为$\beta_1=0.9$、$\beta_2=0.98$，权重衰减为$0.01$。PPO非对称裁剪参数为$\epsilon_{\mathrm{lo}}=0.2$和$\epsilon_{\mathrm{hi}}=0.28$，OPSD系数为$\beta=0.03$；最大游走步数$T_{\max}=5$，训练初始前沿最多保留$3$个候选，目的地摘要不超过$50$个词元。
该配置最大响应长度为$2048$个词元、上下文长度为$32768$个词元，共运行$1000$个rollout步骤。14B主配置使用$4$张H100 80GB并采用张量并行$\mathrm{TP}=4$；原文报告中位每步约$300$秒，典型非评测步骤约$280$秒，且每十步评测一次。这些资源与时长信息对于判断复现成本有用，但不属于方法本身的必要组件。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 训练数据是八个带文本属性的图：七个用于节点分类，分别覆盖引文、电子商务、超链接等领域；另一个是用于关系分类的 WN18RR。测试采用零样本协议，在五个训练后保留图上评估同一检查点，不进行按任务微调。代表性测试集包括引文图 WikiCS、节点分类图 ogbn-products，以及未在训练中出现图级任务的 Expla-Graph。WikiCS 用于检验较密邻域中的邻居选择，ogbn-products 用于检验产品节点分类，Expla-Graph 用于检验向未见任务类型的迁移。原文未明确报告各数据集的节点规模、具体训练/测试划分；数据集统计见附录 D。
- 五个保留图覆盖节点级、边级和图级任务，包括 Cora、WikiCS、ogbn-products、FB15K237 和 Expla-Graph。Cora 代表邻域较稀疏且完整邻域通常可放入提示词的情形；WikiCS 代表邻域较密集、需要从候选邻居中筛选证据的情形；FB15K237 用于关系分类；Expla-Graph 是训练阶段未见的图级二元立场判断任务。
- Expla-Graph 的每个实例是一个常识解释图，模型先看到种子概念，再通过游走揭示其余概念；这使其能够测试训练于节点分类和关系分类的探索策略是否可以迁移到图级推理。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

预测标签或立场判断正确的样本比例；在节点分类、关系分类和图级二元判断中衡量最终任务正确性。 （越高越好，因为它表示更多测试实例被正确预测。）

</div>
<div class="metric-item" markdown="1">

**每节点游走次数**

模型为一个节点任务选择并访问邻居的平均次数，用于观察探索深度和探索成本。 （不存在单调的越高越好关系；次数增加可能意味着模型发现证据更困难，也可能表示更充分探索，需要结合准确率解释。）

</div>
<div class="metric-item" markdown="1">

**同类别邻居比例与最相似预览命中率**

前者衡量游走落点与种子节点属于同一类别的比例，后者衡量所选邻居是否是嵌入空间中最相似的预览节点；二者分别检验结构相关性和简单语义检索行为。 （同类别邻居比例越高通常越好；最相似预览命中率并非目标指标，因为论文要检验的是利用真实拓扑选择有用证据，而不是单纯选择文本嵌入最相似的邻居。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 保留图上的跨数据集迁移（训练中已出现的任务类型）

<div class="result-value" markdown="1">

CNY 在 WikiCS、Cora、ogbn-products 和 FB15K237 等已见任务家族的未见图上均取得表中最高准确率。WikiCS 在 $10$ 路和 $5$ 路设置下分别达到 $76.8$ 和 $85.5$，超过第二名的 $73.6$ 和 $80.9$；Cora 为 $73.7$，对比第二名 $72.6$；ogbn-products 为 $87.3$，对比 $85.7$；FB15K237 为 $82.1$，对比 $80.7$。

</div>

这些结果支持这样的解释：当邻域较大、不能把所有证据预先放入上下文时，生成过程中主动决定读取哪些邻居更有价值。Cora 上优势较小，因为其完整邻域通常已经能放入提示词。结果证明了在这些零样本迁移设置中的有效性，但不能单独证明优势完全来自游走策略；因此还需要文本预算、推理计算和重连图控制实验。

<div class="result-source" markdown="1">

来源：第 5.2 节 Cross-dataset transfer；具体数值见表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the four datasets whose task family is represented in training, CNY leads every graph foundation model and reasoning baseline, and the size of the lead tracks how much the prediction depends on selecting the right neighbours.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 未见任务类型上的跨任务迁移（Expla-Graph）

<div class="result-value" markdown="1">

Expla-Graph 是训练阶段未出现的图级任务，CNY 的立场准确率为 $92.60$，高于 Graph-R1 的 $89.71$ 和 TRN-R1-Zero 的 $85.92$。CNY 只获得种子概念并通过游走揭示解释图的其余内容，而两种推理基线直接接收完整解释图。

</div>

该结果表明，CNY 学到的并不只是某个节点分类数据集的标签模式，探索邻居、逐步获得证据的行为可以迁移到未见过的图级判断任务。由于 CNY 在输入信息上处于劣势，这一比较也显示其探索机制具有实际价值；不过它仍是单个图级任务上的迁移证据，不能据此断言对所有未见任务都有效。

<div class="result-source" markdown="1">

来源：第 5.2 节 Cross-task transfer；表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Despite this information handicap, and without any graph-level reasoning during training, CNY attains the strongest stance accuracy (92.60 against 89.71 for Graph-R1 and 85.92 for TRN-R1-Zero, Table 1).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 等文本预算和等推理计算的游走有效性控制

<div class="result-value" markdown="1">

在相同文本预算下，游走版本在每个数据集上都超过直接读取一个 $1$ 跳邻居完整文本的版本。在 WikiCS 的相近推理令牌预算比较中，一次贪心游走达到 $77.0$，使用每节点 $2{,}341$ 个令牌；四次自洽采样为 $74.5$，最佳的 $4$ 次重排序为 $74.4$，二者各使用 $2{,}899$ 个令牌。

</div>

等预算结果排除了“只是放进了更多文本”的主要解释，等计算结果则表明优势不只是投入更多测试时计算。预览加直接读取只能小幅改善直接基线，进一步说明关键在于根据当前推理状态选择邻居，而不是让模型看到更多预览。该实验仍不能完全排除不同生成路径或搜索策略之间的其他差异。

<div class="result-source" markdown="1">

来源：第 5.3 节 Matched inference compute；表 2 及附录 F.2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under a comparable inference token budget on WikiCS, one greedy walk (77.0 at 2,341 tokens per node) outperforms both self-consistency over four samples (74.5) and best-of-4 reranking (74.4, each at 2,899 tokens).

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

- Graph-R1：强化学习后训练的图推理模型，使用与 CNY 相同规模的 Qwen2.5-14B 骨干，是最重要的同规模推理基线；其邻域在生成前通过摘要或随机采样固定。
- TRN-R1-Zero：另一种强化学习后训练的图推理模型，在公开的 7B 规模上评估，用于比较不同图推理后训练方法。
- 图基础模型：作为一类更广泛的图模型基线，用于判断 CNY 的优势是否超出专门图模型；具体模型列表见附录 D.1，原文摘录未逐一列出。
- 通用大语言模型：作为不依赖该图游走后训练机制的通用模型基线，用于提供非专门图推理参照；具体模型列表见附录 D.1，原文摘录未逐一列出。

**实验想回答的问题**

- 在统一原始节点文本设置下，CNY 的自适应邻居探索能否在未见图上迁移，并优于固定上下文的图推理基线？
- CNY 的性能提升究竟来自选择性读取真实图结构，还是仅来自更多文本、额外推理计算或执行图游走这一动作本身？

**实验实现**

主实验使用 Qwen2.5-14B-Instruct 作为 CNY 骨干，与同为 14B 规模的 Graph-R1 匹配，避免将优势归因于更大的模型；TRN-R1-Zero 使用其发布的 7B 规模。所有分数均在贪心解码下计算，温度为 $0$。每个邻居预览是该节点原始文本的确定性前缀，并按数据集令牌预算截断，不使用摘要模型或元数据。CNY 使用固定的 OPSD 超参数 $eta=0.03$；另有 $eta=0$ 的 GRPO 消融。主评估遵循零样本协议：一个训练检查点直接应用于保留图，不进行每任务微调。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| WikiCS 度保持随机重连 | 随机交换边、保持每个节点度数不变但破坏拓扑后，WikiCS 游走准确率由 $76.6$ 降至 $73.0$，接近预览加直接读取基线的 $73.4$；每节点游走次数由 $1.24$ 增至 $2.01$。同类别落点比例在 WikiCS 由 $63.4\%$ 增至 $74.0\%$，在 Cora 由 $76.6\%$ 增至 $84.0\%。 | 该控制保持节点度数、节点文本和标签不变，因此主要隔离真实边连接的作用。准确率下降且游走次数上升，表明拓扑被破坏后模型更难找到有用证据；同类别落点比例上升并不意味着重连图更有用，可能反映模型增加了探索或数据分布变化。因此，这一实验支持依赖真实图结构，但不能单独说明模型理解了拓扑的哪一种语义。 | 第 5.3 节 Degree-preserving rewire<br><span class="experiment-evidence">Walk accuracy collapses on WikiCS (→ 73.0, matching the preview+direct baseline at 73.4) while walks-per-node rises (→ 2.01), consistent with recognising that each step now returns less useful evidence.</span> |
| 无 OPSD 的 $eta=0$ GRPO 消融 | 论文说明研究了使用相同奖励、但令 $eta=0$ 的 GRPO 消融；原文摘录未明确报告该消融的具体准确率、游走次数或与完整 CNY 的差值。 | 该设置用于检验目的地条件自蒸馏项是否提供了除最终任务奖励之外的动作级训练信号。由于当前材料没有给出数值，不能判断 OPSD 的增益大小，只能确认作者将其作为核心训练机制的消融。 | 第 5.1 节 Models；第 5.5 节<br><span class="experiment-evidence">The β=0 GRPO ablation (same reward, Eq. 3) is studied in § 5.5.</span> |

**定性案例**

- 邻居选择行为分析显示，CNY 在 WikiCS 和 Cora 上分别以 $74.0\%$ 和 $84.0\%$ 的比例落到同类别邻居，但只有 $22\%$ 的选择是嵌入空间中最相似的预览节点，平均相似度排名为 $4.0$，而检索器为 $1.0$。这说明模型选择的邻居通常与任务标签相关，却不等同于简单的文本相似度检索；它更像是在利用图结构和当前推理需求寻找证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It trains an LLM to perform active graph-walk actions that acquire evidence during inference for graph reasoning tasks.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`5334f007a38fdbeac1f1b10c6135baa022110b045c4803d45f4b834bf730286e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
