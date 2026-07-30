---
title: "[论文解读] Probing the Origins of Reasoning Performance: Representational Quality for Mathematical Problem-Solving in RL vs. SFT Fine-Tuned Models"
description: "[arXiv 2607.26119][LLM 机制与可解释性] 本文试图解释强化学习微调模型为何比监督微调模型更擅长数学推理，重点检验两者在答案正确性表征、层级计算结构和生成长度稳定性上的内部差异。"
arxiv_id: "2607.26119"
announcement_date: "2026-07-30"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:25.738223+00:00"
source_sha256: "add09df339440dddb61732186a41dc54af7290c38741225ef83eff48b3eed94d"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "大型推理模型"
  - "强化学习微调"
  - "监督微调"
  - "数学推理"
  - "机制可解释性"
  - "线性探针"
  - "均值消融"
  - "隐藏状态"
  - "自适应计算分配"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2607.26119</p>

# Probing the Origins of Reasoning Performance: Representational Quality for Mathematical Problem-Solving in RL vs. SFT Fine-Tuned Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Antyabha Rahman, Akshaj Gurugubelli, Omar Ankit, Kevin Zhu, Aishwarya Balwani</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26119v1) · [PDF 下载](https://arxiv.org/pdf/2607.26119v1) · **关键词** 大型推理模型, 强化学习微调, 监督微调, 数学推理, 机制可解释性, 线性探针, 均值消融, 隐藏状态, 自适应计算分配  
**代码**: [https://oankit.github.io/-rl-sft-reasoning/](https://oankit.github.io/-rl-sft-reasoning/)  

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

本文试图解释强化学习微调模型为何比监督微调模型更擅长数学推理，重点检验两者在答案正确性表征、层级计算结构和生成长度稳定性上的内部差异。

**不用术语来说**：强化学习训练出的推理模型通常能更准确地解决数学题，但仅比较最终正确率无法说明优势从何而来：模型可能更早形成了清晰的答案判断，也可能把关键计算集中在特定深层，或者只是生成了更长的推理文本。本文要区分这些可能性，从模型内部状态与生成行为两方面寻找机制证据。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将逐层线性探测与均值消融结合起来比较强化学习模型和监督微调模型，分别考察“答案正确性信息是否更容易从隐藏状态中读出”以及“哪些网络层对数学推理具有因果重要性”。
- 作者进一步通过同一问题的重复采样分析生成 token 数的变异性，用以检验模型是否会随问题调整计算量；其分析强调，这种长度变异未必由强化学习或监督微调这一单一因素决定，还可能取决于完整训练流程。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型数学推理与机制可解释性交叉领域。研究对象是经过强化学习（RL）训练的大型推理模型与经过监督微调（SFT）的模型；已知前者往往在数学和逻辑基准上表现更好，但仅比较最终答案准确率或思维链长度，不能解释这种优势来自何种内部计算差异。本文因此关注模型逐层隐藏状态所承载的答案正误信息、不同网络层对推理结果的因果重要性，以及同一问题重复生成时的令牌数量变化，从“内部表征—层级计算—外部行为”三个层面比较RL与SFT模型。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**强化学习微调（RL fine-tuning）与监督微调（SFT）**

SFT让模型模仿训练数据中的示范答案或推理过程；RL则依据生成结果获得的奖励来更新策略，使高奖励行为更可能出现。本文把训练方式视为关键比较变量，但不假定所有行为差异都只由RL或SFT这一标签决定。

</div>
<div class="conceptitem" markdown="1">

**隐藏状态与线性探针（linear probe）**

隐藏状态是Transformer某一层对当前输入及生成上下文形成的向量表示；线性探针是在冻结原模型后，用简单线性分类器判断这些向量能否预测答案正确性。探针准确率较高表示正误信息更容易被线性边界分开，但不等同于证明该信息被模型实际用于生成答案。

</div>
<div class="conceptitem" markdown="1">

**均值消融（mean ablation）**

均值消融把某层或某组激活替换为其参考均值，再观察模型性能变化，以估计该组件对任务的因果重要性。若替换后性能下降更明显，说明被干预层对数学推理更关键，但结论仍受替换基线与干预方式影响。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是数学推理问题，以及多个训练来源可比较的语言模型，核心分组为RL微调模型与SFT或指令微调模型。对每个模型，研究首先采集逐层隐藏状态，并训练线性分类器输出答案“正确/错误”的预测，以衡量正误表征出现于哪些层以及可分性有多强；随后对不同层实施均值消融，以输出各层受干预后的推理性能变化，判断计算重要性是否向深层集中；最后对同一道题重复采样多个回答，统计生成令牌数的题内变异，用于考察模型是否会稳定或自适应地分配推理计算。主要假设是：若RL的性能优势具有内部表征基础，则RL与SFT模型应在探针可分性或层级因果结构上呈现系统差异；令牌变异则作为补充行为证据，不能单独归因于RL。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$h_l$**

模型第 l 层的隐藏状态向量；本文用其训练逐层线性探针。该符号是为概括问题设置而采用的标准记法，原文节选未明确给出符号定义。

</div>
<div class="notationitem" markdown="1">

**$l$**

Transformer层的索引，用于比较正误表征随深度出现的时间及各层消融影响。

</div>
<div class="notationitem" markdown="1">

**$y \in \{0,1\}$**

生成答案的正确性标签，其中1表示正确、0表示错误；原文节选仅说明预测答案正确性，未明确规定数值编码。

</div>
<div class="notationitem" markdown="1">

**$T$**

一次回答生成所使用的令牌数量；重复采样时比较同一问题上T的变异。原文节选未明确指定该符号。

</div>

</div>

**直接相关的工作**

- **Zhang et al. (2025), Reasoning models know when they’re right: probing hidden states for self-verification**: 与本文的逐层线性探针最直接相关：该工作探测推理模型隐藏状态中的自我验证信息；本文进一步把答案正确性表征用于RL与SFT模型之间的系统比较，并考察其跨层出现模式。
- **Zhang and Nanda (2024), Towards best practices of activation patching in language models: metrics and methods**: 为本文的激活干预与均值消融提供方法论背景；本文利用此类干预定位数学推理依赖的网络层，并比较RL模型的深层集中结构与SFT模型较均匀的层间分布。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大型推理模型在数学与逻辑基准上已表现出相对于传统监督微调模型的明显优势，但缺少对优势来源的机制解释。这使研究者难以判断应当改进哪类训练过程、模型层级或计算分配机制，也无法仅凭较长的思维链和较高的最终正确率确认模型是否真正形成了更好的内部推理表征。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **机制可解释性研究**：通过分析神经元、激活模式或计算回路，定位模型执行算术等操作时依赖的内部组件；已有工作识别了特定算术回路，并发现思维链生成会提高激活稀疏性。
- **行为与信息论分析**：从模型可观察的输入输出行为研究推理能力，例如测量对题目措辞变化的敏感性、长推理行为、信息压缩限制，以及不同问题或采样条件下的输出差异。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 已有机制研究主要集中于较小模型和基础算术操作，所得局部回路或激活现象不足以解释大型推理模型在完整数学问题上的整体性能优势。
- 已有行为研究能够揭示措辞敏感性、输出长度或压缩限制，却通常不直接检查逐层隐藏表征及其因果作用；因此，外部行为差异无法确定究竟对应更清晰的内部表示，还是不同的层间计算组织。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有两条研究路线彼此补充但尚未连通：文献仍缺少在可比的强化学习与监督微调模型之间，同时衡量答案正确性信息何时出现、其线性可分程度，以及各层对推理输出因果重要性的整合分析；生成 token 的题内变异能否代表自适应计算分配，也仍需直接检验。

</div>
<div markdown="1"><span>核心问题</span>

强化学习微调相对于监督微调究竟造成了哪些内部表征与计算架构差异，从而可能支持更好的数学推理表现；这些差异是否还体现为模型在重复解答同一问题时对生成计算量的不同分配方式？

</div>
<div markdown="1"><span>作者直觉</span>

如果强化学习确实重塑了推理过程，那么“答案是否正确”的信息应当能在其隐藏状态中更早、更稳定地被简单线性分类器读取；同时，替换某一层激活后造成的性能损失应呈现有组织的层级模式，而不是各层近似均匀。重复采样的输出长度则提供另一个行为侧视角：长度随问题稳定变化可能反映确定的计算策略，较大波动则可能说明模型存在多种同样可行但尚未收敛的推理轨迹。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文采用三条互补的分析链路比较强化学习推理模型与监督微调模型。第一条链路在合成数学题上生成答案，从模型即将输出最终答案的位置提取逐层隐藏状态，并训练逐层逻辑回归探针，以检验“答案是否正确”在内部表示中是否线性可分；第二条链路对 DeepSeek-Math 两个版本逐层实施均值消融，用参考数据上的平均激活替换真实激活，再观察准确率下降，从而定位不同深度层对推理的因果重要性；第三条链路对同一题目重复采样，统计答案一致性与输出长度变异系数，考察模型是否会稳定或自适应地分配推理 token。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造并标注探针数据

每个模型对每题采样生成一次回答，从 \boxed{} 中抽取最终答案；答案与标准值匹配时标为正确，允许因舍入产生的 ±1 容差，无有效答案者剔除。随后取所有模型均作答题目的交集，并为每个模型等量抽取正、负样本，按标签分层划分为70%训练集、15%验证集和15%测试集。

<div class="method-step__io" markdown="1">

**输入**：由概率、分数和成本计算等四种固定模板生成的1000道合成数学题，以及每题可算法验证的标准答案。  
**输出**：跨模型样本量一致、正确与错误类别平衡的探针训练、验证和测试数据。

</div>

**直观理解**：这一步把模型回答转成“正确/错误”二分类样本，并尽量排除题目记忆、类别比例和模型答题覆盖范围不同造成的干扰。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提取逐层内部表示

定位 \boxed{} 前一 token，在一次前向传播中读取全部 Transformer 块在该位置的隐藏状态；仅使用第1至第L个块的输出，不使用输入嵌入和架构特有的后归一化状态。变长序列采用右侧填充和注意力掩码，以保持目标 token 相对序列起点的位置不变。

<div class="method-step__io" markdown="1">

**输入**：每个保留样本的完整生成文本及其正确性标签。  
**输出**：形状为 L×N×D 的逐层表示张量，其中L为层数、N为样本数或批大小、D为隐藏维度，文中模型的D为4096。

</div>

**直观理解**：作者在模型“已经完成推理、但尚未写出答案”的瞬间读取每一层状态，相当于检查答案落笔前，各层是否已经形成可识别的正确性信号。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 训练逐层线性探针

对每一层分别训练逻辑回归分类器，并用5折交叉验证从给定候选集合中选择正则化强度C；测试集准确率用于衡量正确与错误表示的线性可分性。各层探针彼此独立，不修改原语言模型参数。

<div class="method-step__io" markdown="1">

**输入**：每层的D维隐藏状态及对应的正确/错误标签。  
**输出**：每个模型的逐层探针准确率曲线，以及正确性信息出现和演化的层级位置。

</div>

**直观理解**：如果一个非常简单的直线分类器就能区分正确回答与错误回答，说明该层把正确性编码得更清楚；但这只表明信息容易被读出，并不自动证明模型生成答案时实际使用了该信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 实施逐层均值消融

依次选择每一层ℓ，将该层真实激活替换为参考均值μℓ，在其他设置不变时重新生成并计算准确率；再以未干预准确率减去消融准确率，并计算层深与准确率下降之间的Pearson相关系数。

<div class="method-step__io" markdown="1">

**输入**：DeepSeek-Math-7B-Instruct、DeepSeek-Math-7B-RL，每个模型20道GSM8K题，以及由GSM8K训练数据计算的各层参考平均激活。  
**输出**：逐层准确率下降曲线和深度—重要性相关性，用于比较两类训练方式形成的是深层递进结构还是较均匀的层间分工。

</div>

**直观理解**：把某一层的个体化活动换成“平均状态”，类似暂时抹去该层针对当前题目的信息；性能损失越大，该层对完成数学推理越关键。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 逐层逻辑回归探针

$$
f_{\ell}(\mathbf{h}_{\ell})=\sigma\!\left(\mathbf{w}_{\ell}^{\top}\mathbf{h}_{\ell}+b_{\ell}\right),\qquad \sigma(x)=\frac{1}{1+e^{-x}}
$$

**符号说明**

- $\ell$：Transformer层索引，取值为1至L。
- $\mathbf{h}_{\ell}\in\mathbb{R}^{D}$：第ℓ层在 \boxed{} 前一token处的D维隐藏状态。
- $\mathbf{w}_{\ell}\in\mathbb{R}^{D}$：第ℓ层逻辑回归探针的权重向量。
- $b_{\ell}\in\mathbb{R}$：第ℓ层探针的偏置项。
- $\sigma$：Sigmoid函数，将线性得分映射为0至1之间的预测值。
- $f_{\ell}$：从第ℓ层隐藏状态预测答案正确性的二分类探针。

<div class="equation-explanation" markdown="1">

**直观理解**：探针先对隐藏状态做加权求和，再经Sigmoid得到正确性预测。测试准确率越高，说明该层中正确与错误样本越容易被一个线性边界分开，但不能单独据此断言该表示导致了最终答案。  
**原文位置**：“Measuring Representation Quality via Probing”→“Probe Training”，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 均值消融准确率下降

$$
\mathrm{AD}_{\ell}=\mathrm{Acc}_{\mathrm{base}}-\mathrm{Acc}_{\ell}^{\mathrm{abl}}
$$

**符号说明**

- $\mathrm{AD}_{\ell}$：消融第ℓ层后相对于基线的准确率下降。
- $\mathrm{Acc}_{\mathrm{base}}$：不实施激活替换时的模型准确率。
- $\mathrm{Acc}_{\ell}^{\mathrm{abl}}$：将第ℓ层激活替换为参考均值μℓ后测得的准确率。
- $\mu_{\ell}$：由参考数据集计算的第ℓ层平均激活，用来替代当前题目的真实激活hℓ。

<div class="equation-explanation" markdown="1">

**直观理解**：该式直接比较正常模型和抹去某层题目特定信号后的表现；AD越大，表示该层受干预后损失越明显。若AD为负，则该次均值替换后的准确率反而高于基线，不应解释为负的重要性，而应结合小样本波动和干预副作用判断。  
**原文位置**：“Layer-Wise Mean Ablations”→“Evaluation Metric”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文没有重新训练或微调被比较的语言模型，因而不存在统一的语言模型训练目标。唯一新增训练过程是逐层逻辑回归探针：利用训练集正确/错误标签拟合线性分类器，并通过5折交叉验证选择正则化强度C；原文给出探针函数但未明确写出其优化损失，通常的逻辑回归损失不应在此替原文补写。均值消融和token变异分析均属于推理时评估，不更新模型参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 层级线性探针**

在每个Transformer层的目标位置隐藏状态上训练独立逻辑回归分类器，以测试答案正确性是否能由线性决策边界读出。该模块建立在“线性表示假设”上：若某层明确编码了正确性，简单线性分类器应能稳定提取该信息。

> 直观理解：它不是让模型重新做题，而是像用同一种简易检测器逐层扫描，判断哪一层已经把正确和错误整理成容易区分的表示。

**2. 均值激活消融**

对层ℓ进行干预时，用从GSM8K训练数据得到的参考均值激活μℓ替换当前样本的hℓ，并比较干预前后准确率。该方法比探针更接近因果检验，因为它直接扰动表示并观察行为变化，但其结论仍依赖参考分布和替换操作是否合理。

> 直观理解：探针回答“信息是否存在”，均值消融回答“抹去这层的题目特定信息后，性能是否真的受影响”，两者结合可减少只凭相关性解释机制的风险。

**3. 重复采样与长度归一化变异分析**

对每题的50次输出计算正确率和token长度分布，并以标准差除以均值得到变异系数CV，使不同平均输出长度的模型可比较。该模块分析的是生成策略的稳定性，而不是内部表示的线性可分性或层级因果重要性。

> 直观理解：即使两个模型平均都写得很长，也可能一个每次长度接近、另一个忽长忽短；CV把这种波动换算成相对于自身平均长度的比例。

**训练与推理**

探针阶段先让每个冻结模型生成合成题答案并标注，再在固定的答案前位置提取所有层隐藏状态；每层探针只在训练划分上拟合，在验证或交叉验证过程中选择C，最后在独立测试集报告准确率。均值消融阶段先以GSM8K训练数据建立逐层参考均值，再对每个待测层单独替换激活并重新完成生成；token分析阶段不做任何训练，而是对每个GSM8K-Platinum问题进行50次独立采样并汇总每题分布。三条链路的输出分别对应“信息是否容易读出”“该层是否影响行为”和“生成资源分配是否稳定”，不能互相替代。

**复现信息**

探针生成采用温度T∈[0.6,0.7]、top-p=0.95；按16至32条序列成批提取激活，使用右填充和注意力掩码，并排除输入嵌入及架构特有的后归一化状态。逻辑回归的C从{0.001,0.01,0.1,1.0,10.0}中经5折交叉验证选择，并设置class_weight='balanced'；主要指标为测试集准确率。均值消融生成采用temperature=0.1、top_p=0.9，并通过提示要求显式逐步推理。token分析使用输出长度变异系数CV=σ_tokens/μ_tokens进行跨模型归一化比较；原文说明各回答至少包含数百个token，因此均值不接近零。需要注意，探针依赖正确与错误样本数量足够均衡，均值消融每个模型仅测试20题，而token实验关于“50题×每题50次”与“每模型15000条响应”的陈述在算术上不一致，复现前应核对附录A或作者代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- GSM8K：小学数学文字题数据集。作者从其训练集计算每一层的参考均值激活；评测时每个模型使用 20 道 GSM8K 问题。评测问题所属的具体 split 原文未明确报告。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**Accuracy Drop（AD）**

对第 ℓ 层实施均值消融前后的准确率差，定义为 \(\mathrm{AD}_{\ell}=\mathrm{Acc}_{\text{base}}-\mathrm{Acc}_{\ell}^{\text{abl}}\)。其中，\(\mathrm{Acc}_{\text{base}}\) 是不干预时的准确率，\(\mathrm{Acc}_{\ell}^{\text{abl}}\) 是把第 ℓ 层激活 \(h_{\ell}\) 替换为参考均值激活 \(\mu_{\ell}\) 后的准确率。它衡量该层信息被抹平后性能损失多少。 （若用于衡量模型性能，AD 越低越稳健；若用于判断某层的重要性，正向 AD 越大表示该层被替换后损失越大、因而越关键。负值表示干预后的样本准确率反而高于未干预基准，不能直接解释为负的重要性。）

</div>
<div class="metricitem" markdown="1">

**层深与 Accuracy Drop 的 Pearson 相关系数（r）**

衡量层编号与 AD 之间的线性相关程度。正值表示越深的层通常受到干预时性能下降越大；接近零表示层重要性没有明显的线性深度趋势。论文同时报告 p 值来检验该相关是否显著。 （没有普遍的越高越好；在本文假设下，显著为正且较大的 r 更支持“深层逐渐更关键”的层级化结构。）

</div>
<div class="metricitem" markdown="1">

**答案准确率（Accuracy）**

根据生成结果中的 \boxed{...} 模式抽取最终答案，并判断回答是否正确。未干预准确率既反映模型在这 20 道题上的基础表现，也作为 AD 的参照。 （越高越好，因为表示正确解决的评测题比例更大；但仅有 20 道题时，该比例可能对个别题目非常敏感。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### DeepSeek-Math-7B-RL 的逐层均值消融

<div class="result-value" markdown="1">

该模型未干预准确率为 70%；层深与 AD 呈显著正相关，r=0.47、p<0.01，逐层 AD 范围为 −0.15 至 +0.15。

</div>

作者据此认为，RL 模型越靠后的层总体上越影响数学答题，支持其形成渐进式、层级化的计算结构。通俗地说，后层不像是在均匀重复前层工作，而更可能承担依赖前面处理中间结果的高阶计算。不过，该相关关系只说明深度与干预敏感性共同变化，不能单独证明某一层执行了哪一种具体推理操作，也不能建立 RL 训练导致该结构的严格因果链。

<div class="result-source" markdown="1">

来源：“Layer-Wise Mean Ablations”→“Results and Analysis”→“Layer Criticality Patterns”，Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">DeepSeek-Math-7B-RL (baseline acc. 70%) exhibits a significant positive correlation between layer depth and intervention impact (r=0.47, p<0.01), with AD ranging from −0.15 to +0.15.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### DeepSeek-Math-7B-Instruct 的逐层均值消融

<div class="result-value" markdown="1">

该模型未干预准确率为 65%；层深与 AD 的相关较弱且不显著，r=−0.11、p=0.55，AD 范围为 −0.20 至 +0.05。

</div>

结果不支持“该 SFT 模型越深的层越关键”这一线性趋势，作者将其解释为不同层较均匀地分担推理，并可能存在使模型对单层扰动更稳健的冗余。需要注意，p=0.55 只表示当前小规模样本未发现显著线性关系，并不证明所有层的重要性完全相同；负 AD 也可能来自题目数量少、生成波动或均值替换偶然改善输出。

<div class="result-source" markdown="1">

来源：“Layer-Wise Mean Ablations”→“Results and Analysis”→“Layer Criticality Patterns”，Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">In contrast, DeepSeek-Math-7B-Instruct (baseline accuracy: 65%) demonstrates a weak negative correlation (r=−0.11, p=0.55), with AD ranging from −0.20 to +0.05, suggesting relatively flat layer importance with slight emphasis on early layers.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 两个训练变体的跨层轨迹比较

<div class="result-value" markdown="1">

两模型在第 0–10 层表现出相近的干预敏感性，AD 约为 −0.15 至 0.00；第 15 层之后，两者的 AD 轨迹明显分离。

</div>

作者把浅层的相似性解释为两模型共享算术与基础推理机制，把较深层的分离解释为训练方法主要重塑了高阶数学推理。更谨慎地说，该结果直接支持的是“浅层干预曲线相似、深层曲线不同”；把这些层分别命名为基础算术或高阶推理仍属于功能解释，尚需任务特异探针、因果定位或更多数据验证。

<div class="result-source" markdown="1">

来源：“Layer-Wise Mean Ablations”→“Results and Analysis”→“Convergence and Divergence Points”，Figure 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Both models exhibit similar vulnerability across layers 0–10 (AD ≈ -0.15 to 0.00), indicating shared foundational mechanisms likely responsible for arithmetic operations and core reasoning primitives. Beyond layer 15, however, their trajectories diverge sharply, demonstrating that training methodology fundamentally reshapes higher-order mathematical reasoning.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 每个模型只评测 20 道 GSM8K 问题，单题对应约 5 个百分点的样本准确率变化；因此 70% 与 65% 的基础准确率差、负 AD 以及局部层峰值都可能不稳定。原文摘录未报告重复试验、置信区间或跨数据集复现。
- 比较只涉及 DeepSeek-Math-7B-RL 与 DeepSeek-Math-7B-Instruct 两个模型，且均值激活来自 GSM8K 训练集；由此尚不能把观察到的结构差异普遍归因于“RL 相对 SFT”，也不能排除训练数据、指令流程及其他训练管线差异。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- DeepSeek-Math-7B-Instruct：监督式指令微调模型，是与 RL 模型比较层级组织方式的主要对照；其未干预准确率为 65%。
- DeepSeek-Math-7B-RL：强化学习微调模型，是研究深层表示是否随 RL 训练形成层级化分工的目标模型；其未干预准确率为 70%。
- 各模型自身的未消融运行：作为计算 Accuracy Drop 的基准，使逐层干预影响不会与两个模型原本不同的准确率混淆。

**实验想回答的问题**

- RL 微调与监督式指令微调是否会使数学推理模型形成不同的逐层功能组织，尤其是深层网络对最终答题性能的重要性是否不同？
- 用参考均值替换单层隐藏激活后，模型准确率如何变化；这种变化与层深的相关性是否支持 RL 模型具有更明显的层级化推理结构？

**实验实现**

作者对两个 7B DeepSeek-Math 变体分别评测 20 道 GSM8K 问题。对每一层 ℓ∈{0,1,…,L−1}，把该层当前激活 h_ℓ 替换为由 GSM8K 训练数据计算的参考均值 μ_ℓ，再重新生成答案并计算准确率下降。所有生成固定使用 temperature=0.1、top_p=0.9，提示要求显式的逐步推理，最终答案通过 \boxed{...} 模式匹配提取。该协议隔离的是“单层激活偏离其平均状态所携带的信息是否必要”，而不是删除整层或重新训练模型。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 逐层均值消融：将第 ℓ 层激活 h_ℓ 替换为 GSM8K 训练集上的参考均值 μ_ℓ | RL 模型的 AD 随深度总体上升并达到显著正相关（r=0.47，p<0.01）；Instruct 模型没有显著的深度相关（r=−0.11，p=0.55）。 | 这一干预隔离每一层相对于“典型平均激活”的输入依赖：若替换后准确率明显下降，说明该层针对当前题目产生的特异信息对回答有用。它不能完全隔离层本身的独立因果贡献，因为替换会改变后续所有层接收到的表示，且离分布干预可能引发级联效应。 | “Layer-Wise Mean Ablations”→“Experimental Setup”<br><span class="experiment-evidence">For each layer ℓ∈{0,1,…,L−1}, we replace the activation hℓ with its corresponding reference mean activation μℓ and measure the resulting degradation in accuracy.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Uses probing and layer ablation to explain internal representational differences underlying mathematical reasoning in RL- versus SFT-tuned models.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`add09df339440dddb61732186a41dc54af7290c38741225ef83eff48b3eed94d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
