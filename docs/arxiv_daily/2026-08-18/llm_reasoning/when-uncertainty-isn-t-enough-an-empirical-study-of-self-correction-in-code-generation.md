---
title: "[论文解读] When Uncertainty Isn't Enough: An Empirical Study of Self-Correction in Code Generation"
description: "[arXiv 2608.14659][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.14659"
announcement_date: "2026-08-18"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-19T02:23:01.896488+00:00"
source_sha256: "4cf8c3dd493630999ca81f330b57e16fa16230b8b890ec432ff05db8dfbec76b"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "代码生成"
  - "大语言模型"
  - "不确定性估计"
  - "选择性自我纠正"
  - "语义熵"
  - "执行验证"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.14659</p>

# When Uncertainty Isn't Enough: An Empirical Study of Self-Correction in Code Generation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-18</span>
<span><strong>作者</strong> Pranav Rakasi, Maanas Lalwani, Arnav Srivastava, Arya Palanivel, Tinuade Adeleke, Ruizhe Li, Sean Wu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.14659) · [PDF 下载](https://arxiv.org/pdf/2608.14659) · **关键词** 代码生成, 大语言模型, 不确定性估计, 选择性自我纠正, 语义熵, 执行验证<br>


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

本文属于大语言模型代码生成中的可靠性研究。代码模型根据自然语言题目生成函数实现，但生成成功与否通常只能通过编译、测试或执行来确认；这些外部验证较可靠，却会增加延迟和计算成本，在实时补全等场景中也未必可用。因而，本文考察能否从模型的输出概率、隐藏状态、自我报告或多次采样中得到不确定性分数，以低成本预测代码是否正确，并据此只对高风险结果启动重新生成或调整解码。代码不同于一般自然语言：单个错误词元就可能使程序失败，表面相近的程序可能行为不同，而写法迥异的程序又可能功能等价，因此基于词元或文本相似性的自然语言不确定性方法不能被直接假定为适用于代码。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**不确定性估计**

为模型输出计算一个表示“不可靠程度”的标量分数；分数越高，通常表示该程序越可能出错。它只是正确性的代理信号，并不等同于编译、运行测试等直接验证。

</div>
<div class="concept-item" markdown="1">

**语义熵**

先对同一问题生成多个答案，再按语义等价关系聚类，并根据答案分散在不同语义簇中的程度计算不确定性。本文还涉及语义熵探针，即用单次生成的隐藏状态近似这一多次采样指标，以降低额外开销。

</div>
<div class="concept-item" markdown="1">

**选择性自我纠正**

系统不对所有生成结果统一重试，而是将不确定性分数与阈值比较，仅在结果被判为高风险时触发重新生成或自适应解码。其目标是在正确率、推理成本和响应延迟之间取得更合适的折中。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是 HumanEval 或 BigCodeBench 中的自然语言编程题目 $x$，基础代码大模型先进行一次生成，输出候选代码，并在可访问时提供逐词元 logits 或隐藏状态等内部信息。系统据此计算标量不确定性 $u(x)$；若 $u(x)\leq\tau$，直接返回初始代码，若 $u(x)>\tau$，则启动重新生成或自适应解码等纠正策略，最终输出一份代码实现。研究设置聚焦三个小型代码大模型，并以测试用例所判定的程序正确性为目标；核心问题是自然语言领域的不确定性估计能否迁移到代码，以及这种廉价代理信号能否在尽量少增加延迟的条件下改善代码生成，而不是仅用于拒绝回答。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入的编程问题；在图 1 的流程中也对应一次待评估的代码生成实例。

</div>
<div class="notation-item" markdown="1">

**$u(x)$**

不确定性估计器针对输入及其生成结果计算的标量分数，数值较高表示系统认为结果风险较高。

</div>
<div class="notation-item" markdown="1">

**$\tau$**

触发选择性自我纠正的判定阈值。

</div>
<div class="notation-item" markdown="1">

**$P(\mathrm{True})$**

模型自我评估其候选答案正确的概率；它属于置信度信号，使用时需转换或解释为与不确定性方向一致的控制依据。

</div>

</div>

**直接相关的工作**

- **Kuhn et al. (2023), Semantic Entropy**: 该工作指出逐词元概率无法妥善处理“不同字符串表达相同含义”的情况，提出对多次生成按语义聚类后计算熵。本文将这一思路带入代码场景，并进一步评估由单次生成隐藏状态近似语义熵的探针是否足以预测程序正确性和驱动纠正。
- **Sharma and David (2025)**: 该工作把熵和互信息方法用于代码任务，发现不确定性与正确性之间只有弱负相关，但基于不确定性的弃答可以显著减少错误输出。本文沿用“以不确定性识别风险代码”的问题方向，却把控制动作从弃答改为自我纠正，检验高风险样本经重新生成或解码调整后能否真正提高最终正确率。

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

该方法包含“评估不确定性信号”和“用信号触发自我纠正”两个相连阶段。输入是编程任务 $x$，代码模型按 $p_\theta(y\mid x)$ 生成候选程序 $y$，单元测试给出二元正确性 $c(y)\in\{0,1\}$；研究首先比较平均词元熵、口头置信度、基于多次采样与执行验证的 $P(\mathrm{True})$、提示多样性熵集成和语义熵探针，目标是得到一个标量 $U(x)$，使其越高越可能对应程序失败。随后，作者选用开销较低的语义熵探针作为纠正触发器，分别测试完整函数生成后的 SLT 探针和生成开始前后的 TBG 探针。

端到端地看，系统先生成代码或提取早期隐藏状态，再由探针判断是否超过模型专属阈值 $\tau$。SLT 路径在完整代码生成后选择不修改、按不确定性反复重采样，或执行测试并重采样；TBG 路径只生成一个后继词元便判断是否切换到自适应解码。两类重生成最多尝试 $N=5$ 次，最终输出满足停止条件的候选，或按策略规定返回最低不确定性的候选。直观上，这项方法不是直接训练一个更会写代码的模型，而是在模型外增加“风险检测器”和“是否重写”的控制器，并通过与真实测试反馈对照，检验仅凭模型内部的不安程度是否足以支持可靠纠错。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选代码生成与功能标注

模型通过贪心或随机解码从 $p_\theta(y\mid x)$ 产生候选程序 $y$，再使用 verifiers 库执行单元测试，得到 $c(y)\in\{0,1\}$。随机采样用于构造多解统计和重生成候选，贪心解码则构成自我纠正实验的基线输出。

<div class="method-step__io" markdown="1">

**输入**：编程任务提示 $x$，以及参数为 $\theta$ 的代码语言模型。<br>
**输出**：候选程序、生成过程中的 logits 或隐藏状态，以及由测试确定的通过或失败标签。

</div>

**直观理解**：先让模型交卷，再实际运行测试判卷；测试结果既是评估标准，也是部分不确定性方法和验证式纠正策略所需的监督信号。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 不确定性信号计算与比较

所有方法均输出每个任务的标量不确定性：MTE 平均逐词元熵；口头置信度解析并截断到 $[0,1]$；$P(\mathrm{True})$ 统计 $K$ 个候选的测试通过率；熵集成融合 $N$ 个等价提示下 MTE 的均值和方差；SEP 则从隐藏状态预测语义熵的高低。作者用不确定性与通过或失败结果的 Pearson 相关性及校准图比较这些信号。

<div class="method-step__io" markdown="1">

**输入**：候选程序、逐词元概率、模型自报置信度、多个随机候选、不同等价提示下的生成结果或模型隐藏状态。<br>
**输出**：各任务的不确定性分数 $U(x)$，以及用于选择纠正触发器的信号质量评估。

</div>

**直观理解**：这些方法分别询问“模型每一步有多犹豫”“模型自己说有多确信”“多写几次实际能对几次”“换一种问法是否仍稳定”和“内部表示是否呈现多种行为答案”。它们都试图在执行完整验证之前估计代码出错风险，但信息成本明显不同。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 语义熵探针训练与阈值校准

作者借助符号执行按功能行为聚类多个解，根据各簇概率计算语义熵，并将其离散为高或低标签；标准化并拼接最后三层特征后，训练三层 MLP 探针。随后在候选阈值 $\{0.3,0.4,0.5,0.6,0.7\}$ 上计算精确率、召回率、F1、准确率和触发率，为每个模型与特征位置选择使 F1 最大的阈值 $\tau$。

<div class="method-step__io" markdown="1">

**输入**：多个生成解的功能聚类标签、最后三层 Transformer 隐藏状态，以及 SLT 或 TBG 位置的特征。<br>
**输出**：SLT 与 TBG 两类轻量不确定性探针，以及模型和特征位置专属的触发阈值 $\tau$。

</div>

**直观理解**：探针相当于冻结代码模型后安装一个小型读表器：它不重新理解全部代码，只读取模型内部状态并判断当前是否属于高风险情形。阈值决定系统多敏感，过低会频繁重写正确答案，过高则会漏掉真正需要纠正的错误。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 选择性自我纠正与最终返回

SLT 路径在完整生成后触发两种政策：不确定性式纠正持续随机重生成直至 $U(x)\leq\tau$，验证式纠正则持续生成和执行测试直至通过；TBG 路径在只产生一个后继词元后评估风险，若 $U(x)>\tau$ 就对剩余生成切换到自适应解码，否则继续贪心解码。达到尝试上限仍未停止时，不确定性策略返回分数最低的候选，验证策略返回已通过测试的候选；原文没有完全说明验证策略在五次均失败时的具体候选选择规则。

<div class="method-step__io" markdown="1">

**输入**：初始候选、探针分数 $U(x)$、阈值 $\tau$、外部测试器，以及最多 $N=5$ 次的尝试预算。<br>
**输出**：最终代码解，以及相对于贪心基线的 Pass@1 和平均墙钟延迟。

</div>

**直观理解**：SLT 是“整份答案写完后再决定是否重写”，TBG 是“刚起笔便决定是否采用更复杂的写法”。验证式策略依据实际考试结果停手，而不确定性式策略只依据风险预测停手，因此两者检验的是执行反馈能否被廉价内部信号替代。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 验证器经验正确概率

$$
P(\mathrm{True}\mid x)=\frac{1}{K}\sum_{k=1}^{K}V(\hat{c}_k)
$$

**符号说明**

- $x$：输入的编程任务提示
- $K$：对同一任务进行随机解码所采样的候选数量
- $\hat{c}_k$：第 k 个独立采样得到的候选程序
- $V(\hat{c}_k)$：外部验证器的二元结果；候选通过全部测试时为 1，否则为 0
- $P(\mathrm{True}\mid x)$：模型在任务 x 上经随机采样产生正确程序的经验概率

<div class="equation-explanation" markdown="1">

**直观理解**：该式直接计算“同一道题写 $K$ 次，有多少次通过测试”。它比模型自报置信度更接近可观察的功能正确性，但每道题需要多次生成并执行测试，因此是质量较强、在线成本也较高的信号。<br>
**原文位置**：第 3.2.3 节 P(True)

</div>

</div>

<div class="equation-block" markdown="1">

#### 提示多样性熵集成的失败概率

$$
U(x)=P_{\mathrm{fail}}(x)=\sigma\!\left(w_1H(x)+w_2V(x)+b\right),\quad H(x)=\frac{1}{N}\sum_{i=1}^{N}\mathrm{MTE}_i(x),\quad V(x)=\frac{1}{N}\sum_{i=1}^{N}\left(\mathrm{MTE}_i(x)-H(x)\right)^2
$$

**符号说明**

- $N$：语义等价但措辞不同的系统提示数量
- $\mathrm{MTE}_i(x)$：任务 x 在第 i 个系统提示下生成结果的平均词元熵
- $H(x)$：跨提示的平均 MTE，表示总体预测不确定性
- $V(x)$：跨提示 MTE 的方差，表示对提示措辞的敏感性或认知不稳定性代理
- $w_1,w_2$：逻辑回归学习到的均值与方差权重
- $b$：逻辑回归偏置
- $\sigma$：将线性输出映射到 0 至 1 的 sigmoid 函数
- $U(x)$：经验证集校准后预测的失败概率

<div class="equation-explanation" markdown="1">

**直观理解**：先观察模型在多种等价问法下平均有多犹豫，以及这种犹豫是否随措辞剧烈变化，再让一个轻量分类器把两项统计转换为失败概率。平均值高表示普遍没有把握，方差高表示答案过程容易受提示方式影响；两者共同刻画风险。<br>
**原文位置**：第 3.2.4 节 Entropy Ensembles via Prompt Diversity

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：基础代码语言模型在本文中不进行再训练；优化对象是后置的不确定性预测器和触发阈值。提示熵集成使用逻辑回归，以 $H(x)$ 与 $V(x)$ 预测功能失败概率；SEP 使用高或低语义熵标签训练线性分类器或小型神经网络，最终实现采用三层 MLP，原文未给出显式损失函数，按分类设定可知其目标是区分高、低语义熵，但不应据此臆造具体损失形式。推理阈值不是通过梯度学习，而是在 $0.3$ 至 $0.7$ 的离散候选中选择 F1 最大者，以同时抑制不必要纠正和漏检失败。需要注意，正文第 3.3.1 节称阈值在 HumanEval validation split 上网格搜索，而附录 B.2 称在 held-out test data 上调节；数据划分表述存在不一致，复现时必须核对原始代码或完整附录，避免在最终测试集上调参造成评估泄漏。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 多源不确定性估计器**

MTE 从每个生成步的 softmax 分布计算熵并跨词元平均；口头置信度从最后一个可解析的“Confidence”模式抽取数值并截断，缺失时该次尝试不能满足相应停止条件；$P(\mathrm{True})$ 对 $K$ 个随机候选运行验证器；提示熵集成则对固定的 $N$ 个语义等价系统提示各生成一次，在温度 $0.9$ 下计算 MTE 均值与方差，再以逻辑回归映射为失败概率。

> 直观理解：该模块的关键区别是证据来源：词元熵和隐藏状态只需模型内部信息，自报置信度依赖模型语言表达，多次采样与验证则直接观察程序能否运行正确。成本越低并不意味着越能指导行动，因此作者先统一比较信号，再把廉价 SEP 放入纠正流程做压力测试。

**2. 语义熵探针 SEP**

SEP 先把多个候选按功能行为而非表面文本聚类，并由长度归一化后的词元对数概率聚合出簇概率；探针输入为最后三层隐藏状态的拼接向量，维数随模型为 $6144$ 至 $9216$，分类器是 $256\rightarrow128\rightarrow64$ 的三层 MLP，并使用特征标准化和早停。SLT 读取倒数第二个生成词元处的表示，用于事后风险判断；TBG 读取正式生成前的状态，用于提前门控。

> 直观理解：两段代码即使写法不同，只要行为相同就属于同一语义簇；若模型的概率质量分散到许多互不相同的行为，说明它对“程序应该做什么”并不稳定。SEP 学习从一次前向传播的内部状态近似这种昂贵的多次生成统计，从而降低在线决策成本。

**3. 纠正策略控制器**

控制器把 $U(x)>\tau$ 转化为重生成或切换解码的动作，并比较三种政策：SLT 不确定性式重生成、SLT 执行验证式重生成和 TBG 自适应解码。完整重生成受 $N=5$ 次预算约束，阈值按模型和探针位置分别调节，使触发错误答案的召回与避免误触发正确答案的精确率取得 F1 意义下的平衡。

> 直观理解：风险预测本身不会修复代码，真正影响最终效果的是“预测高风险后做什么”。这个控制器刻意把触发信号和停止依据拆开，使实验能够判断失败究竟来自风险识别不准，还是来自随机重写本身不可靠。

**训练与推理**

训练阶段首先对每个任务生成多个候选，通过符号执行按功能行为聚类；各簇概率由长度归一化的词元对数概率聚合得到，再计算语义熵并构造高、低标签。随后分别在 SLT 和 TBG 位置提取最后三层 Transformer 隐藏状态，拼接并标准化后训练 MLP 探针，使用早停控制过拟合；最后按模型和特征位置搜索阈值 $\tau$，以 F1 为选择标准。提示熵集成另在验证数据上拟合逻辑回归；$P(\mathrm{True})$、MTE 和口头置信度属于统计或解析方法，不需要训练。

推理阶段中，SLT 路径先完整生成贪心候选，再从倒数第二词元表示计算 $U(x)$。若采用不确定性式纠正且 $U(x)>\tau$，系统以随机解码重生成并重新估计风险，直至 $U(x)\leq\tau$ 或达到五次上限；若采用验证式纠正，则执行候选并持续重生成到测试全部通过或预算耗尽。TBG 路径只进行一次后继词元预测，从生成前状态计算风险：低于阈值继续标准贪心解码，高于阈值则对剩余序列启用结合词元级与语义级熵信号的自适应解码。最终以功能正确率和墙钟时间同时衡量“是否修对”以及“为纠正付出多少计算成本”。

**复现信息**

公平解释结果所需的核心设置如下：评估模型为约 $3$B 规模的 LLaMA 3、Qwen2.5-Coder 和 DeepSeek-R1 系列 instruct 变体，但表格具体列名使用 Llama-3.2-3B-Instruct、Qwen2.5-Coder-3B-Instruct 与 DeepSeek-Coder-1.3B-Instruct，模型命名在方法概述和结果表之间并不完全一致，应以实际检查点配置为准。代码正确性通过 verifiers 库执行测试；数据覆盖 HumanEval 和 BigCodeBench。提示熵集成对每个任务使用固定的 $N$ 个语义等价系统提示，每个提示仅生成一个候选，随机解码温度为 $0.9$；原文节选未给出 $N$、$K$、最大生成长度、采样 top-p 或随机种子，不能据此补全。

SEP 拼接最后三层 $[-3,-2,-1]$ 的隐藏状态，形成 $6144$ 至 $9216$ 维特征，经标准化后输入 $256\rightarrow128\rightarrow64$ 的 MLP，并使用早停。模型专属阈值来自 $\{0.3,0.4,0.5,0.6,0.7\}$，实际范围为 $0.3$ 至 $0.7$；完整函数纠正最多尝试五次。主要输出指标是 Pass@1 和每题平均墙钟延迟，不确定性质量另用 Pearson 相关性和校准图；墙钟时间会受硬件、批处理和验证器环境影响，而节选未报告这些条件，因此延迟只能在论文同一实验环境内作相对比较。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 原文节选仅称在“these benchmarks”上进行评估，未提供数据集名称、规模、划分方式或各数据集的具体作用。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**不确定性信号与代码正确性的相关系数**

衡量某种不确定性或置信度估计与代码是否正确之间的线性关联。本文报告的符号方向取决于信号定义：$P(\mathrm{True})$ 是置信度，因而与正确性呈较强正相关；熵类量通常表示不确定性，因而可能与正确性呈负相关。仅凭绝对值和正负号不能直接比较方法优劣，还需确认各信号的方向定义。 （在方向定义一致时，相关系数绝对值越大，说明信号越能区分正确与错误代码；对于 $P(\mathrm{True})$，正相关越高越好。）

</div>
<div class="metric-item" markdown="1">

**推理开销**

衡量每个任务需要多少次模型前向计算或随机生成。多样本 $P(\mathrm{True})$ 需要 $K$ 次随机 rollout，而语义熵探针等方法只需一次前向传播。 （越低越适合实时使用，但低开销本身不代表信号足够准确或能改善自我纠正。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Llama 上比较各类不确定性估计与代码正确性的相关性

<div class="result-value" markdown="1">

多样本 $P(\mathrm{True})$ 的相关系数为 $0.842$，是该模型上报告的最强结果；其他方法整体与正确性呈弱至中等负相关。

</div>

这一结果支持作者关于多样本自评信号最可靠的判断：Llama 给出的 $P(\mathrm{True})$ 与代码正确性高度同向变化。但它只说明相关性较强，不证明该信号能因果性地提升自我纠正，也不能说明其额外 $K$ 次生成成本在实际系统中一定值得。

<div class="result-source" markdown="1">

来源：表 1；第 4.1 节 Uncertainty Evaluations

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The correlation analysis in Table 1 reveals that P(True) achieves the strongest performance across all three models (0.842, 0.782, 0.303 for Llama, Qwen, and DeepSeek respectively), though the substantial degradation on DeepSeek suggests that smaller models exhibit less consistent self-evaluation behavior.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Qwen 上比较各类不确定性估计与代码正确性的相关性

<div class="result-value" markdown="1">

多样本 $P(\mathrm{True})$ 的相关系数为 $0.782$，仍是所比较方法中最强的信号，但低于 Llama 上的 $0.842$。

</div>

Qwen 的结果表明，多样本 $P(\mathrm{True})$ 的优势并非只在单一模型上出现。不过，该节选没有报告模型间差异的统计显著性，因此不能仅凭 $0.842$ 与 $0.782$ 的数值差异断言 Llama 的自评能力显著优于 Qwen。

<div class="result-source" markdown="1">

来源：表 1；第 4.1 节 Uncertainty Evaluations

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The correlation analysis in Table 1 reveals that P(True) achieves the strongest performance across all three models (0.842, 0.782, 0.303 for Llama, Qwen, and DeepSeek respectively), though the substantial degradation on DeepSeek suggests that smaller models exhibit less consistent self-evaluation behavior.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### DeepSeek 上比较各类不确定性估计与代码正确性的相关性

<div class="result-value" markdown="1">

多样本 $P(\mathrm{True})$ 的相关系数降至 $0.303$；作者据此认为较小模型的自我评估行为一致性较差。与此同时，语义熵探针的相关性处于 $-0.196$ 至 $-0.475$ 的区间，与简单熵基线属于同一表现区间。

</div>

DeepSeek 上的明显下降说明，即使采用当前最强的多样本信号，不确定性估计的可靠性也可能强烈依赖模型。作者把下降解释为较小模型自评不稳定，但节选没有提供受控的模型规模实验，因此“模型更小”仍是作者解释而非已被严格隔离的因果结论。语义熵探针未明显优于简单熵方法，也表明更复杂的低成本探针不必然产生更有判别力的信号。

<div class="result-source" markdown="1">

来源：表 1；第 4.1 节 Uncertainty Evaluations

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Semantic entropy probes, in particular, place in the same regime as the simpler entropy-based baselines (-0.196 to -0.475).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 节选未提供数据集名称与规模、任务划分、模型具体版本、正确性判定方式、样本量、置信区间或显著性检验，因此无法判断相关系数的稳定性、跨数据集泛化能力以及模型间差异是否具有统计意义。
- 后续自我纠正实验采用的是表现较弱的语义熵探针，而非最强的 $P(\mathrm{True})$。因此，即使后续纠错效果有限，也只能说明廉价弱信号的可操作性有限，不能据此否定更强但更昂贵的不确定性信号；反过来，相关性较强也不自动证明信号能够改善纠错结果。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 多样本 $P(\mathrm{True})$：对每个任务执行 $K$ 次随机采样，并估计答案为真的概率；它是文中表现最强但计算成本较高的不确定性信号，用于衡量低开销方法与强信号之间的差距。
- 简单熵方法：根据模型输出分布的熵估计不确定性，是语义熵探针的直接低成本参照；节选未列出这些方法的具体名称与计算公式。
- 语义熵探针：以单次前向传播提供低开销不确定性信号。作者虽发现其相关性较弱，仍将其用于后续自我纠正实验，以检验廉价而不完美的信号是否具有可操作性。
- 其他单次前向传播方法：作者将其概括为比多样本 $P(\mathrm{True})$ 便宜约一个数量级的替代方案，但节选未明确报告其名称或实现。

**实验想回答的问题**

- 不同不确定性估计方法与代码生成正确性的相关程度如何，尤其是多样本 $P(\mathrm{True})$ 相对于单次前向传播方法是否更可靠？
- 低开销但相关性较弱的语义熵探针能否作为后续自我纠正实验中可操作的不确定性信号？

**实验实现**

评估覆盖 Llama、Qwen 和 DeepSeek 三个模型，并比较多样本 $P(\mathrm{True})$、语义熵探针、简单熵基线及其他单次前向传播方法与代码正确性的相关性。多样本 $P(\mathrm{True})$ 对每个任务执行 $K$ 次随机 rollout；单次前向传播方法的成本被作者描述为低一个数量级。后续自我纠正实验选择语义熵探针，目的不是采用最强不确定性估计器，而是控制计算开销并单独检验廉价弱信号是否可用于纠错。节选未报告模型具体版本、数据集、样本数、解码参数、正确性判定协议、显著性检验或置信区间。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It empirically evaluates uncertainty-guided self-correction behavior in LLM code generation, a reasoning and capability-evaluation problem.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`4cf8c3dd493630999ca81f330b57e16fa16230b8b890ec432ff05db8dfbec76b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
