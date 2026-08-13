---
title: "[论文解读] LEMUR: Latent Entropy-aware Multimodal Unlearning via Visual-anchored Reasoning Redirection"
description: "[arXiv 2608.11691][LLM 安全] 本文针对强化学习后训练的多模态大推理模型会在思维链中泄露已要求遗忘的敏感事实这一新型隐私风险，提出利用逐词元熵变化定位泄露阶段并在解码时重定向推理轨迹的免训练遗忘框架 LEMUR。"
arxiv_id: "2608.11691"
announcement_date: "2026-08-13"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:57:07.932014+00:00"
source_sha256: "e63b535618a73309c53941194ef871a29547b6afe10da7ef257e02ce5f40f280"
tags:
  - "LLM 安全"
  - "知识编辑"
  - "LLM Reasoning"
  - "多模态大推理模型"
  - "机器遗忘"
  - "强化学习后训练"
  - "思维链隐私泄露"
  - "逐词元熵"
  - "推理时干预"
  - "自回归解码"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2608.11691</p>

# LEMUR: Latent Entropy-aware Multimodal Unlearning via Visual-anchored Reasoning Redirection

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Xinhao Zhong, Yuxia Qiao, Junhao Li, Hao Fang, Yi Sun, Bin Chen</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Harbin Institute of Technology, Shenzhen；Tsinghua University；Pengcheng Laboratory</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11691v1) · [PDF 下载](https://arxiv.org/pdf/2608.11691v1) · **关键词** 多模态大推理模型, 机器遗忘, 强化学习后训练, 思维链隐私泄露, 逐词元熵, 推理时干预, 自回归解码<br>


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

本文针对强化学习后训练的多模态大推理模型会在思维链中泄露已要求遗忘的敏感事实这一新型隐私风险，提出利用逐词元熵变化定位泄露阶段并在解码时重定向推理轨迹的免训练遗忘框架 LEMUR。

**不用术语来说**：现有遗忘方法通常只检查模型最后给出的答案，但具有长推理过程的模型可能在最终答案中避开某项私人信息，却先在内部推理文本中把它完整写出来；如果简单地强力干扰整个推理过程，又会损害模型原有的视觉推理能力。因此，实际需求是在敏感内容即将出现时及时介入，并在风险消失后停止干预，使模型既不泄密，又尽量保持正常思考和回答。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者识别出强化学习后训练模型特有的推理轨迹泄露问题，并观察到敏感属性的复述通常呈现两阶段逐词元熵特征：模型选择属性值时熵较高，确定并连续输出该属性后熵迅速降至接近零，直到敏感片段边界才恢复；该结构在非推理基础模型中大体不明显。
- 作者据此提出 LEMUR：一种完全在推理时运行、无需更新模型参数的多模态遗忘框架。它联合监测遗忘相关内容与异常熵动态，在可能泄露的区间从普通离散自回归解码切换到潜在解码，并注入经熵调节、重新锚定输入图像的净化表示，以重定向后续推理。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于多模态大模型、强化学习后训练与机器遗忘的交叉领域。多模态大推理模型（MLRM）同时接收图像和文本问题，并在给出最终答案前生成显式思维链；强化学习后训练鼓励模型探索多个推理方向，因而提升视觉问答能力，却也扩大了隐私暴露面：模型即使不在最终答案中给出指定主体的敏感事实，仍可能在思维链里复述姓名、职业、住址或宠物等信息。本文因此把机器遗忘从只检查最终答案的“答案级遗忘”扩展为同时约束推理过程与答案的“轨迹级遗忘”，并关注无需重新训练、直接在自回归解码阶段实施控制的场景。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多模态大推理模型（MLRM）**

这类模型联合处理图像与文本，并在最终作答前输出较长的显式推理轨迹。本文特别关注经过强化学习后训练、会主动探索和比较候选结论的模型，而不是直接生成短答案的基础多模态模型。

</div>
<div class="concept-item" markdown="1">

**机器遗忘**

机器遗忘要求模型按请求移除或抑制与指定主体相关的信息，同时尽量保留对非敏感任务的原有能力。本文的判定范围不仅包括最终答案，还包括可被用户观察到的思维链。

</div>
<div class="concept-item" markdown="1">

**逐词元熵**

逐词元熵衡量模型在某一步对下一个词元预测的不确定程度：候选词元概率越分散，熵越高；模型越确信某个候选，熵越低。原文观察到，强化学习训练模型泄露记忆属性时常先在候选值之间出现高熵犹豫，随后在确定并连续复述该属性时熵降至接近零，直至敏感片段结束才恢复。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入由一张包含目标人物的图像、关于该人物的文本问题，以及指定需要遗忘的主体及其受保护内容组成；问题可以是多项选择、开放式生成或填空。模型处于已经完成训练的原生强化学习推理模型设定，按自回归方式先生成显式思维链、再生成最终答案；遗忘机制不得依赖重新训练，而是在推理时监测当前生成内容与逐词元熵。当检测到遗忘相关词元或异常熵变化时，系统需要在敏感推理形成或延续期间改变解码轨迹，并在风险区间结束后恢复常规生成。输出仍是连贯的推理与答案，但其中不应泄露指定主体的敏感事实，同时应尽量保留非敏感视觉推理能力和语言流畅性。该任务的关键假设是：强化学习诱导的探索与“作出决定”过程会为敏感记忆的浮现留下可监测的两阶段熵特征；原文称这一特征在非推理基础模型中基本不存在。文中转录样例进一步说明，仅让最终答案变错或表现为已经遗忘并不足够，因为思维链仍可能明确复述人物身份及其职业、住址、宠物等传记属性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Qwen2-VL（Wang et al., 2024）**: 原文将其列为指令微调多模态大语言模型的代表；强化学习推理模型可建立在这类基础模型之上。本文通过比较此类非推理基础模型与强化学习训练模型，指出后者具有更明显的敏感信息泄露及逐词元熵结构。
- **R1-Onevision 与 Vision-R1（Yang et al., 2025；Huang et al., 2025）**: 原文将二者列为现代多模态大推理模型的代表，它们会在显式思维链区域内进行较长的探索式推理。LEMUR针对的正是这类原生强化学习训练模型在推理轨迹中泄露敏感事实的问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

机器遗忘要求模型按请求移除指定主体的信息，而不必从头训练模型。对于会显式输出长思维链的多模态大推理模型，仅清理最终答案已不足以满足这一要求：模型可能在探索视觉问题的过程中回忆并写出目标主体的敏感属性，造成推理轨迹层面的隐私泄露。与此同时，隐私控制不能以显著破坏模型赖以完成视觉问答的探索性推理能力为代价。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于微调的参数遗忘**：利用遗忘数据继续训练或调整模型权重，使模型在最终答案中降低对目标主体及其属性的生成倾向。其控制主要作用于模型参数和答案行为，而不是逐步观察一次推理过程中敏感记忆何时被唤起。
- **免训练的推理时干预**：不更新模型权重，而是在推理阶段扰动提示嵌入、修正输出 logits、设置提示防护，或采用激活引导来压制目标内容。这类方法可以降低部署成本，但通常以提示或答案为中心，缺少针对长思维链内部状态变化的精细启停机制。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有方法缺少可靠机制来持续监测强化学习诱导的多样、探索性推理轨迹。因此，即使某个已知敏感表述被压制，模型仍可能回忆同一主体的其他敏感属性，或通过同义、语义等价的表达在思维链中泄露；仅看最终答案会漏掉这类风险。
- 微调或较强的激活干预可能对整个生成过程施加过度扰动。干预过弱时推理轨迹仍会泄密，干预过强时又会破坏连贯推理、非敏感任务效用与语言流畅性，形成隐私保护和推理能力之间的直接冲突。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少专门面向原生强化学习后训练多模态推理模型的遗忘机制：它需要同时覆盖最终答案与显式思维链，并能依据当前解码状态判断敏感回忆何时开始、何时结束，从而只在必要区间干预。现有研究也尚未把这类模型的逐词元熵动态系统地用作遗忘控制信号。

</div>
<div markdown="1"><span>核心问题</span>

能否在不重新训练或修改模型权重的条件下，联合遗忘相关性与逐词元熵轨迹，实时识别敏感推理区间，并通过局部的潜在表示重定向同时抑制思维链和最终答案中的泄露，同时尽量保留视觉推理能力、非敏感效用与输出流畅性？

</div>
<div markdown="1"><span>作者直觉</span>

词元熵可理解为模型对下一步输出有多犹豫：作者观察到，模型在多个可能的敏感属性值之间选择时较不确定，而一旦认定某个记忆，后续复述就会变得异常确定。这个由高熵决策点转入持续低熵片段的变化，像是敏感记忆被启动和展开的内部信号。若在该窗口内不再把已经选定的敏感词元原样送回模型，而是注入由候选概率加权、并重新联系输入图像的净化表示，推理就可能转向与图像相关但不含目标隐私的路径；熵恢复后再退出干预，则有望减少对其余正常推理的影响。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

LEMUR 是一个面向原生强化学习训练多模态大推理模型（MLRM）的无训练、推理时遗忘框架。输入是图像、问题、待保护主体对应的禁用词元集合 $\Phi_s$，以及原模型 $\mathcal{M}_\theta$；模型参数始终保持 $\hat{\theta}=\theta$。它在自回归解码的每一步读取词元分布 $p_t$，联合监测禁用词元概率质量 $P_t^{\Phi}$ 与分布熵 $H_t$：一旦发现模型正在犹豫或已经准备复述敏感属性，就从普通离散解码模式 $\mathrm{D}$ 切换到敏感模式 $\mathrm{S}$。在该模式中，LEMUR 删除禁用词元的概率并重新归一化，将剩余候选的概率加权嵌入与视觉锚点、安全回答锚点混合后反馈给模型，从而改变后续推理轨迹，而不是只屏蔽当前输出词元。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造输入并执行普通自回归解码

将输入拼接为 $x=x_v\oplus x_t$；在第 $t$ 步，根据输入和历史反馈 $y_{<t}$ 计算下一词元分布 $p_t=\mathcal{M}_\theta(\cdot\mid x,y_{<t})$。未触发敏感检测时，模型处于模式 $m_t=\mathrm{D}$，按原有离散解码方式生成显式推理轨迹 $r_{1:m}$，随后生成最终答案 $a_{1:n}$。

<div class="method-step__io" markdown="1">

**输入**：主体图像 $I$、问题 $q$、视觉编码器产生的视觉词元 $x_v$、文本词元 $x_t$，以及原始模型 $\mathcal{M}_\theta$。<br>
**输出**：每一步的词元概率分布 $p_t$、候选输出词元，以及供后续敏感检测使用的解码状态。

</div>

**直观理解**：这一阶段保持原模型的正常行为，同时观察它下一步想说什么。LEMUR 不预先改写模型，而是在生成过程中寻找敏感记忆即将进入推理文本的时刻。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于词汇质量与熵的敏感阶段触发

计算禁用词元总概率 $P_t^{\Phi}=\sum_{v\in\Phi_s}p_t(v)$ 与词元分布熵 $H_t=-\sum_{v\in\mathcal{V}}p_t(v)\log p_t(v)$。若 $P_t^{\Phi}\geq\rho$，或同时满足 $H_t\geq\tau$ 与 $P_t^{\Phi}\geq\rho_{\mathrm{lo}}$，则令门控 $g_t=1$，从模式 $\mathrm{D}$ 切换到模式 $\mathrm{S}$。

<div class="method-step__io" markdown="1">

**输入**：当前分布 $p_t$、主体 $s$ 的禁用词元集合 $\Phi_s$、常规阈值 $\rho$、低阈值 $\rho_{\mathrm{lo}}$ 和熵阈值 $\tau$。<br>
**输出**：敏感触发信号 $g_t$ 和当前解码模式 $m_t\in\{\mathrm{D},\mathrm{S}\}$。

</div>

**直观理解**：只检查敏感词概率通常要等模型几乎确定答案后才会报警；熵信号则能识别多个敏感候选仍在竞争的早期犹豫阶段。两种条件结合后，高熵但与敏感内容无关的普通连接词不会仅因“不确定”而误触发。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 受约束的软反馈与视觉锚定重定向

先将 $\Phi_s$ 内词元的概率置零并对其余概率重新归一化为 $\tilde p_t$，再计算剩余候选的期望嵌入 $\hat e_t$。随后把视觉锚点 $e_{\mathrm{vis}}$ 与安全回答锚点 $e_{\mathrm{safe}}$ 合成为 $a$，并按由熵决定的强度 $\gamma_t$ 得到反馈嵌入 $e_t=(1-\gamma_t)\hat e_t+\gamma_t a$；该连续嵌入取代采样词元，作为下一步输入。

<div class="method-step__io" markdown="1">

**输入**：敏感模式下的分布 $p_t$、禁用集合 $\Phi_s$、词元嵌入表 $\bar{E}$、视觉特殊词元集合 $\mathcal{V}_{\mathrm{vis}}$、安全模板词元集合 $\mathcal{S}$，以及系数 $\beta$、$\gamma$、$\gamma_{\max}$。<br>
**输出**：不含禁用词元质量且受到图像与安全表达引导的连续反馈嵌入 $e_t$，以及由此改变的后续推理分布。

</div>

**直观理解**：该步骤不是简单把敏感词替换成另一个词，而是让模型沿着“所有安全候选的平均方向”继续思考。图像锚点把推理重新拉回可见证据，安全锚点则提供拒答或不确定表达的方向；高熵时轨迹尚未定型，因此施加更强引导，低熵时则减弱干预以保护语言流畅性。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 自适应结束敏感阶段并恢复离散生成

仅在模式 $\mathrm{D}$ 下更新主体相关的基线熵 $\bar H_t$；进入模式 $\mathrm{S}$ 后，持续使用连续反馈，直到禁用信号消失且 $H_t\geq\kappa\bar H_t$，或阶段长度达到 $W_{\max}$。退出后恢复模式 $\mathrm{D}$，并在至少 $C$ 个离散步骤内禁止重新触发。

<div class="method-step__io" markdown="1">

**输入**：当前熵 $H_t$、普通模式下熵的指数移动平均 $\bar H_t$、当前门控 $g_t$、敏感阶段起点 $t_0$、恢复比例 $\kappa$、最大长度 $W_{\max}$ 和冷却长度 $C$。<br>
**输出**：被限制在敏感跨度附近的动态干预区间，以及不再泄露目标属性的完整推理轨迹和最终答案。

</div>

**直观理解**：敏感记忆被复述时熵通常下降，复述结束后熵会回升，因此熵恢复可充当“敏感片段结束”的边界。相对主体自身基线的阈值比全局固定阈值更能适应不同模型和主体，最大长度与冷却期则防止干预持续过久或连续触发而破坏文本。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 熵增强敏感触发规则

$$
\begin{aligned} H_t(v)&=-\sum_{v\in\mathcal{V}}p_t(v)\log p_t(v),\\ P_t^{\Phi}&=\sum_{v\in\Phi_s}p_t(v),\\ g_t&=\big[P_t^{\Phi}\geq\rho\big]\lor\big[H_t(v)\geq\tau\land P_t^{\Phi}\geq\rho_{\mathrm{lo}}\big]. \end{aligned}
$$

**符号说明**

- $t$：当前自回归解码步。
- $\mathcal{V}$：模型词表。
- $v$：词表中的候选词元；原文也用它作为熵函数的记号参数。
- $p_t(v)$：第 t 步生成候选词元 v 的概率。
- $H_t(v)$：第 t 步下一词元分布的香农熵，用于度量模型在多个候选之间的不确定程度。
- $s$：当前查询涉及的主体。
- $\Phi_s$：主体 s 的受保护属性所对应的禁用词元集合，是词表的子集。
- $P_t^{\Phi}$：第 t 步分配给全部禁用词元的总概率质量。
- $\rho$：识别已集中敏感复述的常规禁用质量阈值。
- $\rho_{\mathrm{lo}}$：高熵条件下采用的较低禁用质量阈值，满足 rho_lo 小于 rho。
- $\tau$：判定当前分布处于高不确定状态的熵阈值。
- $g_t$：布尔触发信号；为真时开启敏感模式。

<div class="equation-explanation" markdown="1">

**直观理解**：第一行把预测分布的不确定性压缩成一个数：多个词元概率接近时熵高，某个词元占主导时熵低。第三行允许两条触发路径：敏感概率已经足够高时直接拦截；若模型仍在高熵犹豫，则用更低的敏感概率门槛提前介入，同时要求存在一定禁用质量，以免把一般的不确定生成误判为隐私泄露。<br>
**原文位置**：Method，Entropy-augmented Sensitivity Switching，式（3）至式（5），核心门控见式（5）

</div>

</div>

<div class="equation-block" markdown="1">

#### 禁用质量移除、锚点合成与熵控制注入

$$
\begin{aligned} \tilde p_t(v)&=\frac{p_t(v)\mathbb{1}[v\notin\Phi_s]}{\sum_{u\notin\Phi_s}p_t(u)},\\ \hat e_t&=\sum_{v\in\mathcal{V}}\tilde p_t(v)\bar E[v],\\ e_{\mathrm{vis}}&=\frac{1}{|\mathcal{V}_{\mathrm{vis}}|}\sum_{v\in\mathcal{V}_{\mathrm{vis}}}\bar E[v],\qquad e_{\mathrm{safe}}=\frac{1}{|\mathcal{S}|}\sum_{w\in\mathcal{S}}\bar E[w],\\ a&=\beta e_{\mathrm{vis}}+(1-\beta)e_{\mathrm{safe}},\\ \gamma_t&=\min\!\left(\gamma_{\max},\frac{H_t(v)}{\tau}\gamma\right),\\ e_t&=(1-\gamma_t)\hat e_t+\gamma_t a. \end{aligned}
$$

**符号说明**

- $\tilde p_t(v)$：删除禁用词元后，在允许词元上重新归一化的第 t 步概率。
- $\mathbb{1}[v\notin\Phi_s]$：指示函数；词元 v 不在禁用集合中时取 1，否则取 0。
- $u$：归一化分母中遍历允许词元的索引。
- $\bar E[v]$：词元 v 的模型输入嵌入。
- $\hat e_t$：允许候选词元嵌入在受约束分布下的期望，即未加入锚点的软反馈。
- $\mathcal{V}_{\mathrm{vis}}$：预训练模型中的视觉特殊词元集合。
- $e_{\mathrm{vis}}$：视觉特殊词元嵌入的平均值，用于把推理重新锚定到图像模态。
- $\mathcal{S}$：固定拒答或不确定回答模板所含词元的集合。
- $w$：安全模板集合中的词元索引。
- $e_{\mathrm{safe}}$：安全模板词元嵌入的平均值。
- $a$：由视觉锚点与安全回答锚点组合得到的复合锚点。
- $\beta$：视觉锚定与安全措辞之间的混合权重，取值位于 0 与 1 之间。
- $\gamma$：熵等于参考阈值 tau 时的基础注入强度。
- $\gamma_t$：第 t 步由熵自适应决定的实际锚点注入强度。
- $\gamma_{\max}$：锚点注入强度上限，用于避免反馈过度偏离嵌入流形。
- $e_t$：最终反馈给模型、用于下一解码步的连续嵌入。

<div class="equation-explanation" markdown="1">

**直观理解**：前两行先把敏感候选彻底排除，再把所有安全候选压成一个概率加权的连续表示；中间两行构造“关注图像”和“采用安全回答”两个方向。最后两行依据熵调整锚点力量：模型越犹豫，越容易以较强锚点改变轨迹；模型越确定，注入越弱，从而避免在已形成的流畅句段中引入过大扰动。<br>
**原文位置**：Method，Entropy-aware Visual Anchor Injection，式（6）至式（11）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：从机器遗忘的抽象目标看，论文希望在遗忘集 $\mathcal{D}_f$ 上最小化模型对受保护知识的正确恢复能力，同时使正常数据 $\mathcal{D}_n$ 上的能力近似保持原状，即降低 $\mathcal{A}(\theta';\mathcal{D}_f)$ 并约束 $\mathcal{A}(\theta';\mathcal{D}_n)\approx\mathcal{A}(\theta;\mathcal{D}_n)$。但 LEMUR 本身不通过梯度优化这个目标，也不产生新的参数 $\theta'$；它固定 $\hat\theta=\theta$，在推理时修改式（1）的解码反馈与后续分布，因此更准确地说，它是对遗忘目标的解码级近似实现。对推理模型而言，保护范围覆盖完整响应 $y=(r_{1:m},a_{1:n})$：不仅最终答案不能包含目标属性，显式思维链也不能泄露同一主体的其他私人属性。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 熵增强敏感切换器**

切换器联合使用两类证据：$P_t^{\Phi}\geq\rho$ 捕捉低熵、已经集中的敏感复述，$H_t\geq\tau\land P_t^{\Phi}\geq\rho_{\mathrm{lo}}$ 捕捉高熵、概率分散在敏感值及其变体之间的早期推敲。禁用集合 $\Phi_s\subset\mathcal{V}$ 是按主体维护的显式词汇线索，因此该模块并非无需先验敏感词表的检测器。

> 直观理解：普通词表过滤像在敏感词已经到嘴边时才拦截；该模块还观察模型是否正在多个敏感候选之间犹豫，从而把干预起点提前。不过它仍要求研究者事先给出要保护的属性词元及变体，熵只是辅助信号而不是独立的隐私识别器。

**2. 熵感知视觉锚点注入器**

模块先通过 $\tilde p_t$ 严格移除禁用词元质量，再以期望嵌入 $\hat e_t$ 保留所有允许候选的相对概率。锚点 $a=\beta e_{\mathrm{vis}}+(1-\beta)e_{\mathrm{safe}}$ 同时编码视觉模态特殊词元与固定安全模板，其注入强度为 $\gamma_t=\min(\gamma_{\max},H_t\gamma/\tau)$；该操作发生在输入嵌入空间，不更新参数 $\theta$。

> 直观理解：概率置零解决“不能继续说哪些词”，锚点则补充“接下来可以朝哪里说”。软嵌入保留多个安全续写方向，比每步强行选择单个替代词更不容易立即回到原来的敏感轨迹；但固定拒答模板也意味着安全表达的覆盖范围和措辞质量会影响输出。

**3. 动态熵阶段控制器**

控制器在普通模式中用平滑率 $\eta$ 更新基线 $\bar H_t=(1-\eta)\bar H_{t-1}+\eta H_t$，并以 $\kappa\bar H_t$ 作为主体自适应恢复阈值。退出还需满足 $\neg g_t$，并由 $W_{\max}$ 提供硬上限；退出后的 $C$ 步冷却抑制连续敏感阶段。

> 直观理解：这一模块决定干预持续多久：过早停止可能让模型继续补全敏感值，过晚停止则会压制无害内容。用该主体正常生成时的熵作参照，等价于按模型当前说话习惯判断它是否已离开敏感片段，而不是要求所有样本达到同一个绝对熵值。

**训练与推理**

LEMUR 阶段完全不训练：无需遗忘集微调、梯度更新或重新进行强化学习，只需能够取得每步完整词元分布和输入嵌入，并为主体准备禁用集合 $\Phi_s$。推理开始时按原模型离散解码，并只在模式 $\mathrm{D}$ 中维护熵基线 $\bar H_t$；门控 $g_t$ 触发后，模式 $\mathrm{S}$ 对禁用词元执行零概率约束，计算安全候选的期望嵌入，加入熵调节的视觉与安全锚点，并把连续嵌入反馈到下一步。当前禁用信号清除且熵恢复到 $\kappa\bar H_t$ 以上时退出；若未恢复，则最迟在 $W_{\max}$ 步后强制退出，随后等待 $C$ 个普通离散步骤才允许再次触发。最终输出仍由原 MLRM 产生，但其敏感片段附近的潜在推理路径已被重定向。

**复现信息**

公平复现所需的关键条件有四点。第一，系统必须暴露每步全词表概率 $p_t$，因为 $P_t^{\Phi}$、$H_t$ 和期望嵌入 $\hat e_t$ 都不能仅由最终采样词元计算；还必须允许把连续嵌入 $e_t$ 作为下一步输入，否则无法实现潜在反馈。第二，需要按受保护主体构建禁用集合 $\Phi_s$，并覆盖属性值、词元化变体及同义表达；论文摘录没有明确给出该集合的自动构建算法，因此其覆盖率会直接限制检测与屏蔽效果。第三，视觉锚点来自模型已有视觉特殊词元的平均嵌入，安全锚点来自少量固定拒答和不确定模板，例如“I'm not sure”及“I cannot identify this person from the image”；$\beta$ 控制二者比例，$\gamma$、$\gamma_{\max}$ 控制干预强度。第四，阶段控制需要阈值 $\rho$、$\rho_{\mathrm{lo}}$、$\tau$、$\kappa$，平滑率 $\eta$、长度上限 $W_{\max}$ 和冷却长度 $C$；所给章节未报告这些超参数的具体数值或选择流程，复现时必须回查论文实现与附录，不能从摘录推断。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 重构版 MLLMU-Bench 是核心隐私遗忘基准。原始语料包含虚构人物、肖像图像和人工整理的私有属性问答，并划分为 forget、retain、celebrity 三个集合：forget 检验目标知识是否被遗忘，retain 检验非目标虚构人物知识是否受损，celebrity 检验更一般的已知人物能力是否保留。由于原问答没有推理轨迹，作者用 Qwen3.5-35B-A3B 根据图像和人物其他属性，为每一对问答蒸馏带有 $\langle\textsc{think}\rangle$ 与 $\langle\textsc{answer}\rangle$ 的第一人称推理链。实验覆盖分类、填空和开放生成三种任务，并测试不同遗忘比例；节选未报告样本总量及各比例的完整取值。
- VQAv2 用于检验方法是否只对隐私属性数据有效。作者从一般视觉推理问题中抽样，沿用 MLLMU-Bench 的蒸馏流程构造带推理链的数据及 forget、retain 划分，然后直接评测原有 R1-Onevision-7B 权重。该实验关注一般领域中的生成目标召回、推理泄漏和推理保留质量，从而区分“强化学习产生的通用熵现象”与“特定隐私数据集伪相关”；节选未给出 Table 4 的具体数值和抽样规模。
- Qwen2.5-VL 的 forget_5 设置用于跨模型机制迁移测试。它不是原生强化学习推理模型，因此不会稳定产生论文所依赖的显著熵突增。作者在其 forget 集上逐步加入 LEMUR 组件，并与专门面向该模型设计的 R-MUSE 比较，用来判断视觉锚点和熵控制在缺少典型强化学习熵特征时是否仍有效。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务遗忘与保留指标：Task Accuracy 和 Target Recall（TR）**

Task Accuracy 是分类准确率与填空准确率的均值；TR 是开放生成中，被查询人物属性出现在输出里的比例。在 forget 集上，它们衡量目标事实是否仍可从最终答案取回；在 retain 和 celebrity 集上，它们衡量非目标能力是否被误伤。表格还分别报告 CLS Acc、FIB Acc 与 Gen TR，以区分不同任务形式。 （forget 集越低越好，因为目标属性越难被恢复；retain 与 celebrity 集越高越好，因为这表示非目标知识和任务效用得到保留。）

</div>
<div class="metric-item" markdown="1">

**Subject-level Reasoning Leakage（SRL）**

判断内部推理轨迹是否泄露被查询人物的任一人工整理属性，并排除提示中已经直接给出的属性；论文对三种任务取平均。它补足了只检查最终答案的指标，因为模型可能答错或拒答，却仍在 $\langle\textsc{think}\rangle$ 中复述敏感事实。 （forget 集越低越好，表示敏感属性较少出现在推理链中；retain 集的表头标为越高越好，因为在非遗忘对象上保留原有属性推理被视为能力保留。）

</div>
<div class="metric-item" markdown="1">

**Reasoning Retention Ability（RRA）**

由 Gemini-2.5-Pro 自动评判全部任务输出的流畅性和自然度，用来检测遗忘干预是否导致重复、截断或退化推理。它衡量文本质量而非事实正确性，因此需要与准确率、TR 和 SRL 联合解释。 （越高越好，因为更高分表示推理文本更自然、完整；但高 RRA 本身不能证明目标事实已被遗忘。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 两种原生强化学习骨干、多个遗忘比例及 MLLMU-Bench 三类任务上的总体比较

<div class="result-value" markdown="1">

作者报告 LEMUR 在 forget 集上的分类准确率、填空准确率和生成 TR 均低于所有基线，同时 SRL 也显著低于答案导向与推理感知基线。由于所给节选缺少 Table 1 的具体表格行，无法核验优势幅度或逐模型数值。

</div>

该结果支持 LEMUR 不只是让最终答案变错，还减少了推理链对目标属性的直接复述，这正是论文要解决的隐私缺口。它说明在所测设置中“答案遗忘”和“推理遗忘”可以同时改善，但没有证明底层参数已删除相关知识：LEMUR 不修改权重，敏感关联可能仍存在，只是在当前推理路径和评测提示下较难被取回。

<div class="result-source" markdown="1">

来源：Main Results，Table 1 的文字分析；所给节选未包含 Table 1 数值

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

LEMUR drives reasoning leakage far below all of them, which shows that it erases the target concept from the intermediate reasoning as well as from the final answer and thus achieves genuine reasoning-process forgetting rather than answer-only suppression.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen2.5-VL forget_5 上与专门基线 R-MUSE 的迁移比较

<div class="result-value" markdown="1">

完整 LEMUR 配置在 CLS Acc、FIB Acc、Gen TR、SRL、RRA 上分别为 25.9、9.2、17.7、28.5、7.3；R-MUSE 分别为 25.4、12.1、18.3、30.9、7.7。LEMUR 在填空准确率、生成 TR 和 SRL 上更低，分别改善 2.9、0.6 和 2.4 点；但分类遗忘弱 0.5 点，RRA 低 0.4 点。因此原文所称“superior overall forgetting performance”成立于多数遗忘指标，而不是每项指标全面领先。

</div>

这一比较表明，即使非强化学习模型没有明显熵突增，视觉锚定仍能带来可观的遗忘效果；熵机制更像辅助门控而非核心检测器。不过结果也限定了结论：LEMUR 没有在分类遗忘和推理质量上超过 R-MUSE，且这里只测试一个模型和一个遗忘比例，不能据此证明对所有非强化学习架构普遍优越。

<div class="result-source" markdown="1">

来源：Table 3；表中写作“DPED”，正文和 Table 2 写作“DEPD”，存在命名不一致

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

R-MUSE | 25.4 | 12.1 | 18.3 | 30.9 | 7.7; + DPED | 25.9 | 9.2 | 17.7 | 28.5 | 7.3

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### VQAv2 一般视觉推理数据上的跨数据域泛化

<div class="result-value" markdown="1">

作者声称 LEMUR 在 VQAv2 forget 集取得最低 Gen TR 和 SRL，同时保持 retain 集的生成召回，并使 RRA 基本处于 Vanilla 水平；还观察到记忆片段附近再次出现明显熵变化。所给节选截断了 Table 4 的数据行，因此这些结论只能按作者的定性陈述记录，不能给出或复算数值差异。

</div>

该实验试图排除方法只适配虚构人物隐私属性的可能性：若一般视觉问答也出现相同熵模式并可被同一流程控制，说明现象可能与强化学习后的推理行为有关。它仍不能单独证明强化学习是该熵变化的因果来源，因为节选没有展示匹配架构、匹配数据但不经过强化学习的严格对照，也没有给出熵差异的统计检验。

<div class="result-source" markdown="1">

来源：More Experimental Results，Generalization beyond privacy data，Table 4；所给节选未包含数值行

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Accordingly, LEMUR remains effective in this general-domain setting—it attains the lowest generation target recall and reasoning leakage on the forget split while preserving retain-split recall and keeping RRA at essentially the vanilla level—mirroring the behavior observed on MLLMU-Bench and demonstrating the generality of our method.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 核心主结果的可核验性受节选限制：Table 1 和 Table 4 的数值行缺失，因此无法检查两种强化学习骨干、不同遗忘比例及 VQAv2 泛化结果的具体提升、方差和统计显著性。节选也未报告重复实验、置信区间、解码设置及 Gemini-2.5-Pro 与人工评价的一致性；RRA 作为单一自动裁判分数可能受提示和裁判模型偏差影响。
- 实验主要证明推理时输出抑制，而非参数层面的知识删除。权重保持不变意味着目标关联可能通过改写提示、改变图像、采样策略、访问隐藏状态或绕过检测条件重新出现。Qwen2.5-VL 迁移仅覆盖一个非强化学习模型和 forget_5，且其熵机制贡献明显减弱；VQAv2 实验也缺少匹配的非强化学习因果对照，因此“熵特征源自强化学习”及跨架构普适性仍需更严格验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Vanilla：未经任何遗忘处理的原始检查点，是衡量原始任务能力、敏感信息泄漏和推理流畅度的上界参照。LEMUR 同样不修改权重，因此与 Vanilla 的差距可以直接反映推理时干预本身的代价。
- GA 与 NPO：代表基于梯度或优化的训练式遗忘方法。它们是有意义的参照，因为论文的关键主张之一是 LEMUR 无需训练、保持参数不变，并能减少参数更新从 forget 集外溢到 retain 知识的副作用。两者在节选中只被概括为训练式基线，未提供各自目标函数和训练预算。
- MMUnlearner 与 R2MU：代表面向多模态遗忘的训练式方法，其中 MMUnlearner 被作者归为主要针对最终答案的方法，适合检验“答案正确率下降是否等同于推理过程真正遗忘”；R2MU 被列为推理感知比较对象，但节选未解释其具体机制。
- R-MUSE：训练免费方法，也是作者所称的现有先进基线；它尤其适合作为 Qwen2.5-VL 迁移实验的对照，因为该方法原本就是为 Qwen2.5-VL 设计的。该比较检验 LEMUR 的收益是否仅来自采用推理时干预，而非其熵检测和视觉锚定设计。

**实验想回答的问题**

- LEMUR 能否在原生强化学习训练的多模态大推理模型中，同时抑制最终答案与内部推理轨迹对指定敏感属性的泄漏，并避免参数更新式遗忘常见的保留知识损伤和生成质量下降？
- 各推理时组件分别解决什么问题，以及依赖强化学习熵特征设计的 LEMUR 能否迁移到非强化学习模型和一般视觉问答数据？

**实验实现**

主要骨干为原生强化学习训练的 R1-Onevision-7B 和 Vision-R1-7B。LEMUR 直接作用于原始检查点的推理过程且不更新权重；对照方法包括训练式 GA、NPO、MMUnlearner、R2MU 和训练免费 R-MUSE。评测在不同遗忘比例及分类、填空、生成三类任务上进行，并分别检查 forget、retain、celebrity 集。组件消融固定在 Onevision-R1-7B 的 forget_5 设置，以词法禁词掩码 Base 为起点，依次累计加入 ESS、VAI、EVAI 和 DEPD。迁移实验在非强化学习的 Qwen2.5-VL forget_5 上重复累计组件分析。除教师模型和 Gemini-2.5-Pro 裁判外，节选未明确报告解码参数、提示模板、重复运行次数、方差、显著性检验、硬件成本或自动裁判一致性验证，因此这些实现条件仍需查阅附录。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| Onevision-R1-7B forget_5：从 Base 累计加入 ESS、VAI 和 EVAI | Base 的 forget CLS Acc、Gen TR、SRL、RRA 为 46.0、26.5、42.0、6.1；加入 ESS 后前三项降至 38.5、22.4、28.7，说明熵增强检测尤其降低了推理泄漏。继续加入固定强度 VAI 后降至 27.0、15.5、12.5，但 retain CLS Acc 和 Gen TR 从 ESS 的 56.0、29.7 降至 55.5、29.0。改用 EVAI 后 forget 指标进一步降至 25.0、14.2、10.3，同时 retain CLS Acc、Gen TR、RRA 回升至 57.5、30.2、6.8。 | 该累计消融分别检验“能否更准地发现敏感片段”和“发现后如何改变轨迹”。ESS 相对 Base 的大幅 SRL 下降支持熵信号补充纯词法阈值；VAI 的进一步下降说明图像条件潜表示提供了有效重定向信号；EVAI 同时改善遗忘与 retain 指标，支持按熵调节注入强度可减少固定强度的过度转向。由于组件是累计加入而非全因子独立消融，不能严格分离组件交互，也无法确认 EVAI 脱离 VAI/ESS 时的单独效果。 | Table 2，Component ablation on Onevision-R1-7B forget_5<br><span class="experiment-evidence">Base \| 46.0 \| 26.5 \| 42.0 \| 6.1 \| 55.8 \| 29.5 \| 56.3 \| 6.4; + ESS \| 38.5 \| 22.4 \| 28.7 \| 6.2 \| 56.0 \| 29.7 \| 56.4 \| 6.1; + VAI \| 27.0 \| 15.5 \| 12.5 \| 6.1 \| 55.5 \| 29.0 \| 56.5 \| 6.2; + EVAI \| 25.0 \| 14.2 \| 10.3 \| 6.4 \| 57.5 \| 30.2 \| 57.0 \| 6.8</span> |
| Onevision-R1-7B forget_5：在 ESS、VAI、EVAI 完整前级配置上加入 DEPD | 加入 DEPD 后，forget CLS Acc、Gen TR、SRL 从 25.0、14.2、10.3 轻微变为 26.0、15.1、11.3，即遗忘指标各退化 1.0、0.9、1.0 点；但 forget RRA 从 6.4 升至 6.9，retain CLS Acc、Gen TR、SRL、RRA 从 57.5、30.2、57.0、6.8 升至 59.1、30.9、57.6、7.2。它主要改善效用与推理质量，而不是继续增强遗忘。 | 这一消融隔离动态退出时机的作用：DEPD 根据熵变化使干预区间贴合敏感片段长度，减少敏感区间结束后的无谓干预。结果体现明确权衡，即以约 1 点的 forget 指标损失换取 retain 能力和 RRA 提升。因此“几乎不牺牲遗忘”是作者的价值判断，是否值得取决于部署对泄漏与效用的相对成本。 | Table 2，Component ablation on Onevision-R1-7B forget_5<br><span class="experiment-evidence">+ EVAI \| 25.0 \| 14.2 \| 10.3 \| 6.4 \| 57.5 \| 30.2 \| 57.0 \| 6.8; + DEPD \| 26.0 \| 15.1 \| 11.3 \| 6.9 \| 59.1 \| 30.9 \| 57.6 \| 7.2</span> |

**定性案例**

- Figure 4 与 Listings 3–5 检查 R1-Onevision-7B 在 5% forget 集中三个虚构人物、三种任务格式下的逐例输出。以 subject 270 为例，真实宠物为 Rabbit，但模型仍能正确描述图中人物外观，随后在推理中虚构“a cat named Whiskers”，最终选择 Cat。其他人物的出生地、职业等属性也在分类、填空和生成中被一致替换。该案例支持干预主要破坏私有属性召回而非基础视觉识别，并显示跨任务错误具有一致性；但只有三个经展示的样例，不能估计此行为的总体频率。作者还承认少量 forget 输出出现重复或截断，这说明聚合 RRA 较高并不代表每个样例都保持流畅。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper proposes inference-time multimodal unlearning to prevent sensitive information leakage from both reasoning traces and final answers.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`e63b535618a73309c53941194ef871a29547b6afe10da7ef257e02ce5f40f280`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
