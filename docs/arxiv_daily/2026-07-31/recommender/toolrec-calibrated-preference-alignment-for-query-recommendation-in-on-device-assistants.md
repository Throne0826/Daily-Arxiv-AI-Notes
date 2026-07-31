---
title: "[论文解读] ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants"
description: "[arXiv 2606.08466][推荐系统] ToolRec面向端侧智能助手，将系统工具检索与点击信号校准结合起来，使大语言模型更可靠地推荐可直接触发设备功能、且符合用户真实偏好的查询。"
arxiv_id: "2606.08466"
announcement_date: "2026-07-31"
primary_category: "recommender"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.500539+00:00"
source_sha256: "70909414be048b4c540afaa938650af40ef0534d6595f5ca2e2d2f4405cd4d47"
tags:
  - "推荐系统"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "端侧智能助手"
  - "生成式查询推荐"
  - "工具调用"
  - "隐式点击反馈"
  - "偏好对齐"
  - "大语言模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">推荐系统 · arXiv 2606.08466</p>

# ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Luo, Zihan, Chen, Lingkui, Zhang, Ruike, Huang, Hong, Zhang, Boyang, Chen, Ziniu, Wang, Lizhong, Chen, Chao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Huazhong University of Science and Technology；OPPO AI Center；Chongqing University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2606.08466) · [PDF 下载](https://arxiv.org/pdf/2606.08466) · **关键词** 端侧智能助手, 生成式查询推荐, 工具调用, 隐式点击反馈, 偏好对齐, 大语言模型<br>


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

ToolRec面向端侧智能助手，将系统工具检索与点击信号校准结合起来，使大语言模型更可靠地推荐可直接触发设备功能、且符合用户真实偏好的查询。

**不用术语来说**：手机助手中的用户往往不是只想获得文字回答，而是希望快速完成清缓存、打开设置或调用其他设备功能。然而，普通查询推荐模型既不一定知道哪些设备操作可以执行，也容易把“没有点击”误判为“不喜欢”：低活跃用户可能本来就很少互动，而不同类型点击对端侧场景的价值也并不相同。因此，直接使用原始点击日志训练模型，可能产生看似相关却不能立即执行的建议。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者建立包含708个系统工具的SysToolkit，并设计上下文感知的工具检索机制，只向推荐模型提供与当前用户意图高度相关的工具信息，以支持可执行查询生成并控制推荐相关性。
- 作者提出用户级与系统级双层偏好校准：前者依据用户活跃程度调整正负反馈的可靠性，后者提高成功触发系统工具、尤其是高频工具的点击信号权重；随后通过样本级加权Kahneman–Tversky Optimization进行细粒度偏好对齐。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

查询推荐的目标是依据用户当前输入、历史对话和上下文，主动生成用户下一步可能需要的查询，从而降低交互成本。本文研究的不是传统搜索框中的查询补全，而是端侧智能助手中的生成式查询推荐：用户常希望推荐项能够直接调用清缓存、设置闹钟等系统工具，因此模型不仅要生成语义相关的查询，还要理解设备可执行能力。大语言模型具备零样本生成与语义推理能力，但其通用训练目标与推荐任务存在差距，通常需要利用点击等隐式反馈进行偏好对齐；在端侧场景中，点击信号还会受到用户活跃度以及推荐项能否触发工具的影响，不能被简单视为同等可靠的标签。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**生成式查询推荐**

模型不再只从历史日志中检索已有查询，而是根据当前交互上下文直接生成若干候选查询。这样可以覆盖日志中未出现过的表达，但也要求模型控制相关性、可执行性和生成质量。

</div>
<div class="concept-item" markdown="1">

**工具调用查询**

工具调用查询是能够触发设备系统功能的推荐项，例如针对手机卡顿推荐“清理设备缓存”。它区别于只提供信息或解释的普通查询，强调用户点击后可以立即执行操作。

</div>
<div class="concept-item" markdown="1">

**偏好对齐与隐式反馈**

偏好对齐是利用用户行为调整模型，使其更倾向生成用户认可的内容；点击与未点击属于隐式反馈，因为它们没有直接给出人工质量评分。未点击可能源于用户缺乏交互意愿而非推荐质量差，因此反馈可靠性需要校准。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定用户当前查询 $q_u$、智能助手回复 $\mathcal{A}$、历史对话上下文 $\mathcal{C}$ 和可用工具集合 $\mathcal{T}$，参数为 $\theta$ 的推荐模型 $\mathcal{M}_\theta$ 在一次前向推理中生成包含 $K$ 条查询的候选集合 $Q_r=\{q_r^1,\ldots,q_r^K\}$；$K$ 受推理时延约束。候选集合随后还会经过本文不研究的召回与重排模块，最终由界面展示预先确定的 $N$ 条查询。训练日志以点击作为隐式监督：若集合中至少一条查询被点击，则整个集合记为正样本 $Q_r^+$；若所有查询均未被点击，则记为负样本 $Q_r^-$。研究目标是在端侧智能助手环境中，使模型既保持推荐与用户意图的相关性，又更偏向可调用系统工具的可执行建议，并避免把不同用户和不同查询类型的点击信号一律当作同等可靠的监督。该设定默认系统拥有明确的可用工具目录；本文构建的 SysToolkit 包含 708 个系统工具，但实际提供给模型的应是与当前上下文高度相关的工具信息，而非无差别注入全部工具。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{M}_{\theta}$**

参数为 $\theta$ 的大语言模型查询推荐器。

</div>
<div class="notation-item" markdown="1">

**$(q_u,\mathcal{A},\mathcal{C},\mathcal{T})$**

模型输入，依次表示当前用户查询、助手回复、历史对话上下文和可用工具集合。

</div>
<div class="notation-item" markdown="1">

**$Q_r=\{q_r^1,q_r^2,\dots,q_r^K\}$**

模型一次生成的候选查询集合，其中 $q_r^k$ 是第 $k$ 条候选，$K$ 是生成数量。

</div>
<div class="notation-item" markdown="1">

**$y(q_r)\in\{0,1\}$**

候选查询 $q_r$ 的点击指示变量；$1$ 表示被点击，$0$ 表示未被点击。

</div>

</div>

**直接相关的工作**

- **GQS（Min et al., 2025）**: 该方法使用直接偏好优化（DPO）将大语言模型生成与用户点击行为对齐，说明点击反馈可用于提升查询建议的质量与多样性；但它面向较标准的交互场景，并将点击更直接地作为偏好标签，没有专门处理端侧工具调用需求及用户活跃度导致的反馈可靠性差异。
- **GaRM（Yin et al., 2026）**: 该方法以高斯分布刻画用户偏好的不确定性，并通过组相对策略优化（GRPO）进行稳健对齐。ToolRec与其共同关注点击驱动的生成式查询推荐，但进一步把问题限定为端侧助手，并显式区分工具调用查询与普通查询，同时从用户层面校准低活跃用户的行为噪声。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

端侧智能助手承担调用设备系统功能的任务。论文基于OPPO小布过去六个月的线上统计指出，可触发系统工具的推荐在点击率和点击量上均显著高于一般查询，说明用户更重视能够立即执行操作的建议。因此，推荐系统不仅要预测用户可能继续询问什么，还要识别其操作意图，并把该意图连接到真实可用的系统工具。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于直接偏好优化的生成式查询推荐**：以用户点击行为构造偏好数据，再使用Direct Preference Optimization直接调整大语言模型，使其更倾向生成被点击的、高质量且多样的查询建议。
- **考虑偏好不确定性的群组相对策略优化**：使用高斯分布描述用户偏好的不确定性，并通过Group Relative Policy Optimization比较一组候选输出的相对质量，以获得更稳健的偏好对齐。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有方法主要针对标准聊天机器人，缺少端侧系统工具的显式表示及其与当前语境的匹配机制，因而可能给出被动的文字说明，而不是用户期望的可立即执行操作。
- 现有对齐通常把点击和未点击当作同等可靠的标签，既忽略不同用户活跃度造成的反馈噪声，也不区分工具调用查询与一般查询的场景价值；结果可能错误惩罚低活跃用户未点击的优质建议，并削弱模型对执行型需求的学习。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未形成一套面向端侧助手的统一方案：一方面需要把自然语言意图可靠地落到真实系统工具上，另一方面需要在训练前校正点击日志，使反馈同时反映用户行为信号的可信度与工具调用行为的重要性。

</div>
<div markdown="1"><span>核心问题</span>

如何利用含噪的真实点击日志训练端侧查询推荐模型，使其在保持建议与当前语境相关的同时，更准确地生成可触发系统级工具的查询？

</div>
<div markdown="1"><span>作者直觉</span>

可执行推荐需要同时解决“有什么工具可用”和“哪些反馈值得相信”。先检索少量与语境匹配的工具，相当于给模型划定可操作且相关的候选范围；再降低低可信行为信号的影响、提高成功调用工具的点击权重，相当于纠正训练数据中的错误奖惩。这样，偏好优化学习到的就更接近用户真正想完成的设备操作，而不是机械模仿原始点击记录。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ToolRec 将端侧查询推荐建模为“工具检索—在线反馈采集—偏好校准—加权对齐”的闭环。给定当前用户查询 $q_u$、助手回复 $\mathcal{A}$、历史对话 $\mathcal{C}$ 和可用工具集合 $\mathcal{T}$，模型 $\mathcal{M}_\theta$ 一次生成 $K$ 条候选查询；线上系统再经下游重排与召回展示其中 $N$ 条，并把是否点击转化为未配对的正、负偏好样本。方法的关键不是直接相信每次点击，而是同时估计反馈对该用户是否置信、查询对端侧工具是否有执行价值，再用合成后的样本权重训练模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建并检索端侧工具

使用 Qwen-3-embedding 将 708 个工具的描述预编码到向量数据库；推理时编码对话上下文，再由 Qwen-3-reranker 筛选最相关的前 $N$ 个工具。

<div class="method-step__io" markdown="1">

**输入**：包含工具名称与文本描述的 SysToolkit，以及当前查询、历史对话和助手回复所构成的交互上下文。<br>
**输出**：与当前用户意图相关的小规模工具子集及其描述。

</div>

**直观理解**：系统不把全部工具塞进提示词，而是先像搜索目录一样找出最可能有用的几个工具。这既节省上下文空间，也减少模型推荐与对话无关功能的概率。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成查询并收集隐式偏好

推荐模型 $\mathcal{M}_\theta$ 单次前向生成候选集合 $Q_r=\{q_r^1,\ldots,q_r^K\}$，线上模块最终展示 $Q_r'$；若集合中至少一条展示查询被点击，则记为正样本 $Q_r^+$，若全部未点击则记为负样本 $Q_r^-$。

<div class="method-step__io" markdown="1">

**输入**：用户查询 $q_u$、助手回复 $\mathcal{A}$、历史上下文 $\mathcal{C}$ 和检索到的工具信息。<br>
**输出**：由交互上下文、推荐查询集合和点击标签组成的未配对偏好数据集 $D$。

</div>

**直观理解**：用户点击被视为“这组推荐至少有一条有用”，全部未点击则暂时视为负反馈。这里没有要求同一输入同时具备一条胜者和一条败者，因此数据更容易从真实线上日志获得。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双层校准偏好信号

用户侧根据 $uctr$ 计算权重 $w_u$：活跃用户的未点击更可信，低活跃用户的偶发点击更可信；系统侧计算 $w_s$，强化已点击且可执行的工具查询，并屏蔽未点击工具查询的负向训练信号。

<div class="method-step__io" markdown="1">

**输入**：原始正负样本、用户历史点击率 $uctr$、查询能否成功调用 SysToolkit 工具，以及被调用工具的使用频率分位数 $p$。<br>
**输出**：每个样本对应的用户侧权重 $w_u$、系统侧权重 $w_s$ 和聚合权重 $w(Q_r)$。

</div>

**直观理解**：同一个“不点击”对经常点击的人和几乎不点击的人含义不同，因此不能等权处理。同时，工具查询即使暂未被点击也不应轻易受到惩罚，否则模型会退化为只推荐安全但不可执行的闲聊内容。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 样本级加权 KTO 对齐

以 KTO 的隐式奖励衡量当前策略相对参考策略对响应概率的调整，并用 $w(Q_r)$ 缩放每个样本的损失；正样本采用 $\max(w_u,w_s)$ 强奖励，负样本采用 $\min(w_u,w_s)$ 保守惩罚。

<div class="method-step__io" markdown="1">

**输入**：未配对偏好数据 $D$、校准权重 $w(Q_r)$、待训练策略 $\pi_\theta$ 和参考策略 $\pi_{\mathrm{ref}}$。<br>
**输出**：与用户点击倾向及端侧工具执行需求共同对齐的推荐模型参数 $\theta$。

</div>

**直观理解**：只要正样本在用户置信度或工具价值之一上很强，模型就积极学习；负样本则只有在两个角度都较可信时才受到较强惩罚。这种非对称策略降低了噪声点击日志把模型带偏的风险。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 双层校准与样本权重聚合

$$
\begin{aligned}
w_u&=\begin{cases}
1-\alpha\tanh\!\left(\frac{uctr-\mu}{s}\right),&Q_r\sim Q_r^+,\\
1+\alpha\tanh\!\left(\frac{uctr-\mu}{s}\right),&Q_r\sim Q_r^-,
\end{cases}\\
w_s&=\begin{cases}
(1+\gamma)^{p^k},&Q_r\sim Q_r^+\ \&\ Q_r\sim Q_r^t,\\
0,&Q_r\sim Q_r^-\ \&\ Q_r\sim Q_r^t,\\
1,&\text{otherwise},
\end{cases}\\
w(Q_r)&=\begin{cases}
\max(w_u,w_s),&Q_r\sim Q_r^+,\\
\min(w_u,w_s),&Q_r\sim Q_r^-.
\end{cases}
\end{aligned}
$$

**符号说明**

- $Q_r$：模型生成的一组候选推荐查询。
- $Q_r^+$：至少包含一条被点击查询的正样本候选集合。
- $Q_r^-$：所有查询均未被点击的负样本候选集合。
- $Q_r^t$：能够成功触发 SysToolkit 中系统工具的可执行查询。
- $w_u$：由用户活跃程度校准得到的样本权重。
- $uctr$：该用户的历史点击率，用作自然点击倾向或活跃程度指标。
- $\mu$：用户点击率的经验中心阈值，原文设为 0.07，即分布的上四分位数。
- $s$：所有用户点击率的标准误，用于归一化用户点击率与阈值的差异。
- $\alpha$：控制用户侧权重变化幅度及边界的超参数。
- $w_s$：根据查询可执行性和工具使用频率得到的系统侧权重。
- $\gamma$：控制系统侧增权上界的超参数。
- $p$：被调用工具的归一化使用频率分位数，取值位于区间 [0,1]。
- $k$：控制权重对工具频率敏感度的指数超参数，原文依据线上日志设为 3。
- $w(Q_r)$：用于最终 KTO 训练的样本级聚合权重。

<div class="equation-explanation" markdown="1">

**直观理解**：当 $uctr>\mu$ 时，活跃用户的负样本权重上升、正样本权重下降；当 $uctr<\mu$ 时则相反。对正向工具调用，$p$ 越大通常意味着工具越常用，系统增权越强；对未点击的工具查询令 $w_s=0$，再通过负样本的最小值聚合将其屏蔽。正样本取最大值表示任一校准信号足够强即可奖励，负样本取最小值则要求两个信号均支持时才明显惩罚。<br>
**原文位置**：第 4.3 节公式（6）、公式（7）及第 4.4 节公式（9）

</div>

</div>

<div class="equation-block" markdown="1">

#### 样本级加权 KTO 目标

$$
\begin{aligned}
\mathcal{L}&=\mathbb{E}_{x,y\sim D}\left[w(Q_r)\left(1-v(x,y;\beta)\right)\right],\\
v(x,y;\beta)&=\begin{cases}
\sigma\!\left(r(x,y)-z_{\mathrm{ref}}\right),&y\sim y^+,\\
\sigma\!\left(z_{\mathrm{ref}}-r(x,y)\right),&y\sim y^-,
\end{cases}\\
r(x,y)&=\beta\log\frac{\pi_\theta(y\mid x)}{\pi_{\mathrm{ref}}(y\mid x)},\\
z_{\mathrm{ref}}&=\mathbb{E}_{x'\sim D}\left[\beta\mathbf{KL}\!\left(\pi_\theta(y'\mid x')\Vert\pi_{\mathrm{ref}}(y'\mid x')\right)\right].
\end{aligned}
$$

**符号说明**

- $\mathcal{L}$：ToolRec 最小化的样本级加权 KTO 损失。
- $D$：由线上交互上下文、推荐响应及正负点击标签组成的训练数据集。
- $x$：完整交互输入，包括当前查询、历史对话和助手回复；训练时还可包含检索到的工具上下文。
- $y$：模型生成的推荐查询响应或候选查询集合。
- $y^+$：被标记为正偏好的推荐响应。
- $y^-$：被标记为负偏好的推荐响应。
- $w(Q_r)$：双层偏好校准后分配给候选集合的样本权重。
- $v(x,y;\beta)$：基于前景理论构造的价值函数，用于分别评价正、负偏好样本。
- $\sigma$：将奖励差映射为价值的激活函数。
- $r(x,y)$：当前策略相对参考策略提高或降低响应概率所形成的隐式奖励。
- $\beta$：缩放隐式奖励并控制相对参考策略偏离程度的 KL 惩罚系数。
- $\pi_\theta$：参数为 θ 的待优化推荐策略。
- $\pi_{\mathrm{ref}}$：固定的参考策略，用于约束模型不要偏离原始能力过远。
- $z_{\mathrm{ref}}$：由数据集平均 KL 散度定义的动态参考点。
- $x'$：从数据集采样、用于估计动态参考点的另一交互输入。
- $y'$：与输入 x' 对应、用于估计动态参考点的响应。
- $\mathbf{KL}$：衡量当前策略与参考策略条件分布差异的 Kullback–Leibler 散度。

<div class="equation-explanation" markdown="1">

**直观理解**：隐式奖励比较当前模型与参考模型对同一推荐响应的概率：正样本希望该奖励高于动态参考点，负样本则希望其低于参考点。外层权重 $w(Q_r)$ 决定每条线上反馈对参数更新的影响大小，因此优化目标同时编码了偏好方向、反馈可信度和端侧工具价值。<br>
**原文位置**：第 3.2 节公式（3）、公式（4）与第 4.4 节公式（8）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练阶段最小化加权 KTO 损失 $\mathcal{L}$。与需要同一输入下“偏好—拒绝”成对响应的 DPO 不同，KTO 可直接使用独立的正样本 $Q_r^+$ 和负样本 $Q_r^-$；ToolRec 再以 $w(Q_r)$ 将点击日志的可信度注入梯度大小。参考策略 $\pi_{\mathrm{ref}}$ 提供行为锚点，$\beta$ 和动态参考点 $z_{\mathrm{ref}}$ 约束待训练策略 $\pi_\theta$ 的偏移，避免模型为了适配噪声反馈而过度改变原有生成分布。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. SysToolkit 与上下文感知工具检索**

SysToolkit 收录 708 个系统工具，覆盖显示、通用系统、媒体、通信、网络、交通和健康等功能域。工具描述由 Qwen-3-embedding 建立向量索引，在线阶段根据对话上下文召回候选，并由 Qwen-3-reranker 选出前 $N$ 个相关工具作为生成条件。

> 直观理解：该模块把推荐空间明确锚定到设备真正能够执行的功能上，而不是仅生成语言上相关的后续问题。先检索再生成还能避免全部工具描述占满模型上下文。

**2. 双层偏好校准**

用户侧以用户点击率 $uctr$ 相对阈值 $\mu$ 的偏差调节正负样本可信度，并通过 $\tanh$ 将权重变化限制在稳定范围。系统侧识别可成功触发工具的查询：对已点击工具查询按工具频率分位数 $p$ 增权，对未点击工具查询令 $w_s=0$，避免模型因曝光或时机噪声而放弃主动调用工具。

> 直观理解：用户侧解决“谁给出的反馈更可信”，系统侧解决“哪类反馈更符合端侧助手的产品目标”。两者分别修正行为噪声和任务目标偏差。

**3. 样本级加权 KTO**

KTO 不要求同一输入下成对出现偏好响应和拒绝响应，适合直接使用线上点击日志。ToolRec 将标准 KTO 的类别级固定权重替换为样本级 $w(Q_r)$，并通过正样本取最大值、负样本取最小值实现积极奖励与谨慎惩罚。

> 直观理解：普通 KTO 可以利用零散的“喜欢或不喜欢”记录；ToolRec 进一步让每条记录按可靠程度和工具价值产生不同影响。

**训练与推理**

训练闭环中，现有模型先在线生成并展示查询，平台记录点击或未点击，按集合级规则构造未配对偏好样本；随后由用户历史 $uctr$ 计算 $w_u$，由工具触发情况及频率分位数计算 $w_s$，聚合成 $w(Q_r)$，最终用加权 KTO 更新 $\pi_\theta$。推理时，系统先根据当前对话从 SysToolkit 检索并重排前 $N$ 个相关工具，将其与 $q_u$、$\mathcal{A}$、$\mathcal{C}$ 一并输入模型，单次生成 $K$ 条候选；下游重排与召回模块再根据界面槽位展示 $N$ 条，但这些下游模块不属于本文重点。

**复现信息**

复现方法所需的关键设定包括：SysToolkit 含 708 个工具；工具向量索引使用 Qwen-3-embedding，上下文相关性重排使用 Qwen-3-reranker；用户侧阈值 $\mu=0.07$，对应用户点击率分布的上四分位数；系统侧频率敏感度 $k=3$，其值来自线上交互日志分析。生成候选数 $K$ 由推理延迟预算决定，最终展示数 $N$ 由界面槽位决定；检索工具数也在原文中记作前 $N$ 个，所给章节未明确报告其具体数值，也未给出 $\alpha$、$\gamma$、$\beta$ 等超参数的具体取值。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 在线主实验使用 OPPO 小布助手的真实线上请求与点击日志；该平台月活跃用户超过 1.5 亿。实验将主市场流量等量分配给对照组和处理组，并在正式测试前监控超过 12 小时，以检查两组请求分布是否一致。主结果实验于 2026 年 4 月 21 日至 27 日进行，每个模型获得 5% 的用户流量；它用于检验真实用户环境下的点击量、CTR 和相关性。
- 离线比较从线上日志随机抽取 2,000 条真实用户对话历史，作为各模型生成查询推荐的共同输入。Doubao-Seed-1.8 对 ToolRec 与每个基线进行严格成对判断，输出 Win、Tie 或 Loss，主要考察工具调用的帮助性和推荐查询的多样性。
- 消融实验同样使用 OPPO 小布助手主市场的线上流量，于 2026 年 4 月 28 日至 5 月 4 日连续运行 7 天，每个模型变体分配 2% 流量。它通过改变用户侧权重和系统侧权重的配置，隔离不同偏好校准组件的贡献。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Click Number（总点击量）**

统计实验流量内推荐查询被点击的总次数，反映系统实际促成用户交互的总体规模；该指标会同时受到推荐质量、请求量和用户活跃度影响。 （越高越好，因为在流量分配可比时，更多点击通常表示推荐更能触发用户所需操作。）

</div>
<div class="metric-item" markdown="1">

**Click-Through Rate（CTR）**

衡量展示推荐后产生点击的比例，相比总点击量更直接地反映单次推荐被用户接受的概率。 （越高越好，因为更高的 CTR 表示推荐在相同曝光机会下更符合用户点击偏好。）

</div>
<div class="metric-item" markdown="1">

**Relevance（相关性）**

衡量推荐查询与用户当前输入及对话上下文一致的比例。由于全量日志评估成本过高，每个模型随机抽取 1,000 个线上推荐实例，由 Doubao-Seed-1.8 判断上下文相关性。 （越高越好，因为它表明模型没有为了增加点击而生成偏离当前语境的推荐；但该指标依赖自动评审模型，并不等同于人工相关性判断。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 主市场 5% 流量、2026 年 4 月 21 日至 27 日的在线 A/B 测试，ToolRec 对比 Base、SFT 和 Vanilla KTO。

<div class="result-value" markdown="1">

ToolRec 获得 1,113,871 次点击、$0.3198$ 的 CTR 和 $0.9570$ 的相关性。相对 Base，其总点击量和 CTR 分别提升 $4.74\%$ 和 $3.32\%$，相关性下降 $1.44\%$；在三个对齐方法中，其点击量和 CTR 最高。

</div>

作者结果表明，经过双层校准的点击反馈比直接监督微调或未经校准的 KTO 更能促成真实用户点击。相关性仍接近 SFT 和 Vanilla KTO，但低于 Base，因此结果体现的是“点击收益与相关性损失之间的折中”，不能证明 ToolRec 在所有质量维度上都优于基础模型。表 1 的 ToolRec 相关性为 $0.9570$，而正文写作 $0.956$，应以表格数值为准并进一步核对原论文。

<div class="result-source" markdown="1">

来源：Table 1；Section 5.2 Main Online Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

ToolRec 1,113,871 0.3198 0.9570; Improve. +4.74% +3.32% -1.44%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 从线上日志抽取 2,000 条真实对话历史，以 Doubao-Seed-1.8 对 ToolRec 与三个基线进行离线成对评审。

<div class="result-value" markdown="1">

ToolRec 对三个基线均取得高于负率的胜率；各比较中 Tie 的比例介于 $43.6\%$ 至约 $50\%$。

</div>

离线评审从工具调用帮助性和推荐多样性两个角度补充了点击指标，说明 ToolRec 的优势并非只表现为线上点击增加。大量平局意味着各模型在普通对话上的能力接近，增益更可能集中在存在工具调用需求的场景。不过，原文摘录未给出各组完整的 Win、Tie、Loss 数值，而且评审来自单一 LLM，不能视为人工偏好的确定结论。

<div class="result-source" markdown="1">

来源：Figure 5；Section 5.3 Offline Comparisons

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Interestingly, we observe a notably high proportion of ”Tie” outcomes across all three comparison pairs, ranging from 43.6% to roughly 50%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 基于 2026 年 4 月 21 日至 27 日在线服务日志的查询类型分布分析，每个模型占 5% 用户流量。

<div class="result-value" markdown="1">

相对 Base，SFT 生成工具调用查询的占比变化为 $-0.19\%$，Vanilla KTO 为 $+0.45\%$，ToolRec 为 $+1.44\%$；ToolRec 的相对增幅最大。

</div>

这一结果直接检验系统侧校准是否把生成分布推向可执行查询，而不只是提高总体点击。ToolRec 的增幅支持该设计确实鼓励工具调用，但占比变化本身不能证明每个新增工具查询都正确、有用或被成功执行；它还需要结合 CTR、相关性和实际执行结果判断。

<div class="result-source" markdown="1">

来源：Table 4；Section 5.6 Query Type Distribution Analysis

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Base –; SFT -0.19%; Vanilla KTO +0.45%; ToolRec +1.44%

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 相关性和离线 Win/Tie/Loss 均由 Doubao-Seed-1.8 自动判断，原文未报告人工复核、评审一致性或偏差分析；因此这些质量结论可能受到单一评审模型偏好的影响。
- 主要结论来自单一移动助手平台和有限日期窗口，且原文未提供置信区间、显著性检验或长期留存、工具执行成功率与误触发率。流量分配和预实验平衡降低了初始偏差，但尚不能证明结果可推广到其他平台、长期运行或安全敏感工具。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Base：未经偏好对齐的 Qwen-3-14B 基础模型，用于判断训练和校准相对于原始生成能力是否带来实际收益。
- SFT：监督微调基线，代表直接学习已有训练样本的常规对齐方法，可用于判断偏好优化是否比标准模仿式训练更适合点击反馈。
- Vanilla KTO：不使用 ToolRec 双层校准权重的普通 Kahneman-Tversky Optimization。KTO 可以利用非成对的正、负反馈，因此适合无法为同一输入稳定构造偏好对的数据，也是隔离 ToolRec 校准机制贡献的核心基线。

**实验想回答的问题**

- 在真实移动助手流量中，ToolRec 能否比未对齐模型、监督微调和普通 KTO 更有效地促成用户点击，同时维持较高的上下文相关性？
- ToolRec 的用户侧校准、系统侧校准及其频率感知动态权重是否分别有效，并且能否互补地提升可执行工具类查询的推荐效果？

**实验实现**

所有模型均以 Qwen-3-14B 为基础，在配备 8 张 NVIDIA A100 GPU 和 200GB 内存的服务器上运行。训练采用 LoRA 参数高效微调，将秩为 8 的适配器应用到所有网络层；批大小为 32，优化器为 AdamW，学习率为 $5\times10^{-6}$，并使用余弦学习率调度和 $0.1$ 的预热比例。KTO 损失中的 $\beta$ 设为 $0.01$，控制用户侧和系统侧校准范围的 $\alpha$、$\gamma$ 分别设为 $0.25$ 和 $1.25$。在线主实验对每个模型分配 5% 主市场流量；DPO 和 SimPO 因要求相同输入下的正负偏好对，而线上数据难以形成这种配对，故未纳入比较。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 在普通 KTO 上分别加入用户侧校准或系统侧静态校准，每个变体使用 2% 主市场流量。 | 无校准的 Variant 1 获得 423,561 次点击和 $0.3051$ CTR；仅加入用户侧校准的 Variant 2 提升到 434,084 次和 $0.3090$；仅加入系统侧静态校准的 Variant 3 提升到 429,931 次和 $0.3080$。 | 该对照分别隔离两种校准信号。两种单独改动都优于无校准 KTO，支持用户活跃度校正和工具导向加权各自有效；其中用户侧校准在该次实验中的数值更高。不过这些变体共享同期流量但原文未报告置信区间或显著性检验，因此不能仅凭差值判断两种组件贡献存在可靠的统计排序。 | Table 2；Section 5.4 Ablation Study<br><span class="experiment-evidence">1 × × × 423,561 0.3051; 2 ✓ × × 434,084 0.3090; 3 × ✓ × 429,931 0.3080</span> |
| 比较用户侧校准与系统侧静态权重的组合 Variant 4，以及将系统侧权重升级为频率感知动态权重的完整 ToolRec。 | Variant 4 获得 446,527 次点击和 $0.3162$ CTR；完整 ToolRec 达到 458,334 次点击和 $0.3226$ CTR，两项指标均进一步提高。 | Variant 4 高于任一单独校准变体，说明用户侧和系统侧信号具有互补性；完整模型进一步提升，则隔离出频率感知动态系统权重相对于固定系统权重的增益。作者将其解释为模型更重视用户频繁交互的工具，但实验只验证了最终点击效果，未直接证明该因果机制，也未提供统计显著性。 | Table 2；Section 5.4 Ablation Study<br><span class="experiment-evidence">4 ✓ ✓ × 446,527 0.3162; ToolRec ✓ × ✓ 458,334 0.3226</span> |

**定性案例**

- 在手机进水案例中，ToolRec 除了给出文字排障建议，还推荐了“Help me clean the speaker.”，可直接触发设备内置排水工具，且用户随后点击了该推荐。该案例直观展示了模型如何把对话语境映射到可执行系统能力；但它只是作者挑选的代表性成功案例，不能据此估计此类推荐的总体成功率或错误调用风险。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出利用校准点击偏好和加权KTO对齐LLM的端侧工具调用查询推荐框架。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`70909414be048b4c540afaa938650af40ef0534d6595f5ca2e2d2f4405cd4d47`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
