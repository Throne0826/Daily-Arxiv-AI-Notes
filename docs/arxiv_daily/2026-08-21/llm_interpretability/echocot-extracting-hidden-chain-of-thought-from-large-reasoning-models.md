---
title: "[论文解读] EchoCoT: Extracting Hidden Chain-of-Thought from Large Reasoning Models"
description: "[arXiv 2608.20055][LLM 机制与可解释性] 原文未明确报告。"
arxiv_id: "2608.20055"
announcement_date: "2026-08-21"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-21T02:06:32.750674+00:00"
source_sha256: "11f2170752ad5a5098bb63d797ce1cb6e49c6f4b01a30ae354224cd3ea33a7af"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "隐藏思维链"
  - "大型推理模型"
  - "黑盒模型攻击"
  - "工具调用"
  - "提示轨迹优化"
  - "模型安全"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2608.20055</p>

# EchoCoT: Extracting Hidden Chain-of-Thought from Large Reasoning Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-21</span>
<span><strong>作者</strong> Yiting Qu, Ziqing Yang, Chi Cui, Ye Leng, Junjie Chu, Yang Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: CISPA Helmholtz Center for Information Security</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20055) · [PDF 下载](https://arxiv.org/pdf/2608.20055) · **关键词** 隐藏思维链, 大型推理模型, 黑盒模型攻击, 工具调用, 提示轨迹优化, 模型安全<br>
**代码**: [https://github.com/TrustAIRLab/EchoCoT](https://github.com/TrustAIRLab/EchoCoT)

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

本文位于大语言模型安全与可解释推理交叉领域，研究大型推理模型（Large Reasoning Models，LRMs）的隐藏思维链（chain-of-thought，CoT）是否会在黑盒 API 交互中被近乎逐字恢复。给定用户问题，LRM 通常先生成包含中间计算、候选方案、失败尝试和自我修正的文本推理轨迹，再输出最终答案；但服务提供商往往只向用户返回答案或摘要，而不公开完整 CoT。隐藏 CoT 不仅可用于训练和蒸馏推理模型，也能帮助研究者诊断推理行为、分析模型差异并监测不安全或欺骗性行为，因此同时具有模型资产价值和安全敏感性。本文关注的不是从 CoT 中推断用户隐私，而是直接恢复模型自身的隐藏推理内容。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**大型推理模型与隐藏思维链**

大型推理模型会针对输入问题生成较长的中间推理过程，再给出最终答案；这些中间文本就是思维链。所谓隐藏 CoT，是模型内部或服务端生成、但 API 不直接展示给用户的推理轨迹。

</div>
<div class="concept-item" markdown="1">

**黑盒 API 交互**

黑盒设置下，攻击者只能向模型服务发送请求并观察返回结果，不能访问模型参数、隐藏状态或服务端保存的原始 CoT。本文进一步利用 API 返回的推理 token 数量和可选 CoT 摘要作为隐藏轨迹保真度的间接信号。

</div>
<div class="concept-item" markdown="1">

**工具调用与推理重放面**

工具调用是模型在一次回答过程中调用外部 scratchpad 等工具并接收返回值的交互步骤。论文认为，普通多轮对话中隐藏 CoT 通常会被丢弃，但工具调用可能使同一轮中的隐藏推理继续保留，从而形成可被指令反复唤回和重现的“推理重放面”。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究目标是在不访问目标模型内部参数和原始隐藏状态的黑盒 API 条件下，给定问题 $x$，诱导目标 LRM 产生隐藏 CoT $c$，并从多轮工具交互返回的候选文本中恢复与目标轨迹近乎逐字一致的版本。攻击者输入问题以及逐步注入的指令，目标模型输出工具调用结果、可见文本和 API 元数据；方法输出候选隐藏 CoT $[1m\hat{c}[0m$。在开放模型实验中，研究者能够取得真实 CoT 作为 ground truth，用长度误差和 Token-EM 检验 $[1m\hat{c}[0m$ 与 $c$ 的一致性；在专有黑盒模型中，真实 CoT 不可见，因此只能依据提供商报告的推理长度和可用 CoT 摘要评估长度接近程度与语义对齐。论文还假设工具调用能够在单轮中保留隐藏推理，并假设 API 返回的推理 token 数量或摘要能够提供一定的保真度反馈；这些是攻击进行迭代优化的关键条件。直观地说，攻击不是要求模型“一次性复述答案”，而是让它在工具交互中逐步回放此前的内部推理，并用外部可见信号判断下一次注入是否更接近原轨迹。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入问题或任务实例，例如数学、编程、生物、化学或物理问题。

</div>
<div class="notation-item" markdown="1">

**$c$**

目标 LRM 针对输入 $x$ 生成的真实隐藏思维链。

</div>
<div class="notation-item" markdown="1">

**$\hat{c}$**

攻击过程恢复出的隐藏 CoT 候选文本，用于与真实轨迹或代理信号比较。

</div>
<div class="notation-item" markdown="1">

**$T_d$**

API 报告或实验记录中的目标推理 token 数量；下标 $d$ 表示目标模型或对应数据条件。

</div>

</div>

**直接相关的工作**

- **REP**: REP 通过少样本提示和代码格式示例，要求模型把隐藏推理复现到可见输出中，因此与本文同样试图从黑盒模型获得 CoT。但原文指出，REP 没有验证恢复结果是否与真实隐藏 CoT 近乎逐字一致；EchoCoT 则利用工具调用造成的推理重放面，并以长度和文本代理信号迭代提高恢复保真度。
- **Stolen Thoughts**: Stolen Thoughts 通过在兼容的解码模型之间重放可复用的加密推理块，使较弱模型恢复较强模型的隐藏 CoT，曾取得接近目标长度的提取效果。本文的方法不依赖跨模型传递或特定的加密推理块，而是直接利用目标模型自身的工具调用交互；原文还称该先前攻击在相关提供商修补漏洞后已不再可复现。

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

EchoCoT面向具有隐藏思维链（Chain-of-Thought，简称CoT）的黑盒大推理模型（LRM）。给定目标问题$x$、模型$M$和攻击者提供的工具调用请求$t$，模型会在调用工具前生成目标CoT$c^{\star}$并输出答案$y^{\star}$，即$M(x,t)\rightarrow(c^{\star},y^{\star})$；攻击者通过工具接口诱导模型反复“拒绝当前候选—继续提取—最终接受并回答”，以重建近似原文的$hat{c}$。方法先用工具调用获得候选CoT，再根据长度误差和可用的摘要文本重合度评价候选，最后用辅助大语言模型自动搜索一个可跨问题复用的多步注入轨迹$P=(p_1,\ldots,p_K)$。直观地说，EchoCoT不是直接要求模型泄露思维链，而是让模型把隐藏推理逐步回放到攻击者控制的“草稿工具”中；自动优化器则像实验员一样，根据每批问题的反馈改写下一轮话术。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 威胁建模与接口构造

攻击者把$x$与$t$共同提交给模型，使模型在工具调用前生成$c^{\star}$并输出$y^{\star}$；工具接口被设计为可返回特定内容，从而形成模型与攻击者之间的交互回放表面。原文将$c^{\star}$视为目标CoT，因为工具请求可能改变推理条件，但最终答案通常仍保留原问题的核心推理。

<div class="method-step__io" markdown="1">

**输入**：目标问题$x$、黑盒目标模型$M$、工具请求$t$以及攻击注入提示$P$。攻击者只能通过公开API提交输入、提供可被模型调用的工具并读取工具调用内容、推理 token 数量以及在有条件时提供的压缩CoT摘要$s$。<br>
**输出**：可被攻击者观察和迭代处理的目标CoT候选、工具调用状态、最终答案及其长度或摘要信息。

</div>

**直观理解**：攻击者看不到模型内部的真实草稿，因此先给模型一个看似正常的工具任务，让模型把推理过程暴露在工具交互中；这里的目标不是读取参数，而是利用模型已经公开的接口行为。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多步候选提取

接口首先获得初始候选$\hat{c}_1$；对每个$k<K$，发送$p_k$拒绝当前候选并要求模型继续提取，得到$\hat{c}_{k+1}$；最后发送$p_K$接受候选并要求模型继续生成最终答案。每一步都记录候选的长度误差$E_{\mathrm{len}}$，并在存在摘要时记录摘要 token 召回率$R^{\mathrm{sum}}_{\mathrm{tok}}$。

<div class="method-step__io" markdown="1">

**输入**：一个问题、当前候选CoT以及多步注入轨迹$P=(p_1,\ldots,p_K)$。<br>
**输出**：候选序列$\{\hat{c}_1,\ldots,\hat{c}_K\}$、每个候选的保真度分数以及对应的最终回答。

</div>

**直观理解**：这相当于反复让模型修改一份草稿：前几轮说“这份还不完整，请继续回放”，最后一轮才说“可以了，请回答问题”。多轮反馈很重要，因为一次工具调用往往只能得到压缩或不完整的推理。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 轨迹自动优化

辅助LLM按Inject、Reflect、Distill三阶段搜索通用轨迹：Inject逐步生成注入，并将同一注入应用于批次中的所有问题；Reflect从批次级目标、逐步分数变化、有效或失败话术、模型反应和下一步扰动方向诊断轨迹；Distill把新经验合并进工作记忆。优化器每批次比较当前轨迹与历史最佳轨迹，并可保留或回退。

<div class="method-step__io" markdown="1">

**输入**：手工初始化的注入轨迹、问题批次、各步候选CoT及其保真度反馈，以及跨批次保存的经验文件。<br>
**输出**：针对目标模型优化出的最佳固定轨迹$P$及其批次级目标分数、可复用经验和后续部署版本。

</div>

**直观理解**：优化器像一个会记录实验日志的提示词工程师：先试用一套话术，再观察哪些步骤有效，最后把规律压缩保存，避免下一批问题重复试错。它搜索的是一条对许多问题都相同的轨迹，而不是为每道题单独训练一个策略。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 冻结轨迹部署与评估

冻结所有注入内容，停止调用辅助优化器，将同一轨迹逐题执行；对最终候选选择长度误差最小者，并根据长度阈值、摘要 token 召回率及文本重合指标判断提取质量。最终答案匹配率用于检查工具交互是否仍然保留原问题的解题结果。

<div class="method-step__io" markdown="1">

**输入**：针对特定目标模型优化出的最佳轨迹、不同任务和数据集中的未见问题。<br>
**输出**：未见问题上的提取CoT、最终答案、工具调用和答案匹配结果，以及长度和文本层面的攻击成功率。

</div>

**直观理解**：优化阶段结束后，方法不再为每道新题临时改提示，而是使用一套固定“操作手册”。这样测试的是真正的跨问题泛化能力，而不是优化器对测试题的现场适配。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 攻击者的CoT重建

$$
\hat{c}=\mathcal{A}(M,x,t,P)
$$

**符号说明**

- $\hat{c}$：攻击者重建出的目标CoT候选
- $\mathcal{A}$：攻击过程或攻击算法
- $M$：黑盒目标大推理模型
- $x$：目标问题
- $t$：工具调用请求
- $P$：多步注入轨迹

<div class="equation-explanation" markdown="1">

**直观理解**：该式说明输出不是模型内部状态的直接读取，而是攻击算法根据模型、问题、工具请求和注入轨迹，通过可观测交互重建出的CoT。<br>
**原文位置**：Threat Model，Attacker’s Goal

</div>

</div>

<div class="equation-block" markdown="1">

#### 双层批次优化目标

$$
J(P)=(\Phi_{\mathrm{len}},g),\qquad \Phi_{\mathrm{len}}=\frac{1}{N}\sum_{i=1}^{N}\mathbf{1}\!\left[E_{\mathrm{len}}(\hat{c}_{i}^{\mathrm{best}})\leq\tau\right]
$$

**符号说明**

- $J(P)$：轨迹$P$的批次级优化目标
- $\Phi_{\mathrm{len}}$：长度误差不超过容差的样本比例
- $g$：在相同长度达标比例下用于排序的连续保真度分数
- $N$：批次中的问题数量
- $\hat{c}_{i}^{\mathrm{best}}$：第$i$个问题在多步候选中按最小长度误差选出的候选
- $E_{\mathrm{len}}$：候选CoT与目标长度之间的误差
- $\tau$：可接受的长度误差阈值
- $\mathbf{1}[\cdot]$：条件满足时为1、否则为0的指示函数

<div class="equation-explanation" markdown="1">

**直观理解**：轨迹比较采用先后顺序：先看有多少问题的提取长度足够接近目标，再在比例相同时比较平均保真度。这样优先解决论文所指出的主要问题——候选CoT通常过短——同时减少少数拒答或极端样本对平均分的影响。<br>
**原文位置**：Section 4.2，Optimization Objective

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：EchoCoT不是对目标模型进行参数训练，也没有使用目标模型的梯度、logits或内部参数；它优化的是针对某一目标模型的通用注入轨迹$P$。LGO以$\Phi_{\mathrm{len}}$为首要目标，并以平均负长度误差$g=-\frac{1}{N}\sum_iE_{\mathrm{len}}(\hat{c}_i^{\mathrm{best}})$打破平局；LTGO在相同的首要目标下，以$q_i=R^{\mathrm{sum}}_{\mathrm{tok}}(\hat{c}_i^{\mathrm{best}})/(1+E_{\mathrm{len}}(\hat{c}_i^{\mathrm{best}}))$的批次平均值作为连续分数。辅助LLM依据在线反馈进行离散的提示词搜索，而非通过反向传播学习参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 回放式工具提取接口**

接口围绕scratchpad工具执行多步注入。前$K-1$步拒绝当前候选并请求进一步提取，最后一步接受候选并要求生成答案；每个候选都由长度误差评价，若有摘要则增加$R^{\mathrm{sum}}_{\mathrm{tok}}$。

> 直观理解：该模块提供了模型“重新写出隐藏草稿”的交互通道，并用连续的拒绝反馈推动模型从简短概括转向更完整的回放。

**2. Inject-Reflect-Distill搜索器**

辅助LLM以当前最佳轨迹为参照，逐步扰动第$k$步注入的一个维度，例如权威框架、拒绝措辞、施压强度、完整性要求或输出格式；随后根据批次级结果诊断并维护经验文件。

> 直观理解：单个提示词可能偶然有效，但多步提示相互依赖；该模块负责逐步试验、总结原因并保存经验，使轨迹能在不同问题批次中逐渐改进。

**3. 双层保真度目标**

优化先最大化达到长度容差的样本比例$\Phi_{\mathrm{len}}$，再用连续分数$g$打破相同比例下的平局。LGO仅使用长度误差，LTGO在有摘要时同时使用摘要 token 召回率。

> 直观理解：方法先判断“有多少样本的长度已经像原推理”，再比较这些候选谁更接近原文；这样可避免少数极端失败样本或仅有摘要的粗略文本信号主导搜索。

**训练与推理**

优化阶段从手工轨迹开始，按问题批次执行Inject：在每个工具调用步骤生成并测试注入，观察候选CoT及长度或摘要保真度；随后Reflect汇总批次结果，比较当前轨迹和历史最佳轨迹，分析有效措辞、失败模式及下一扰动方向；最后Distill将当前最佳轨迹、目标分数和经验整合到经验文件中，并在下一批次继续搜索。针对每个目标模型完成优化后，选取经验文件中的最佳轨迹并冻结；部署阶段仅将该固定轨迹应用于不同任务和未见数据集，不再调用辅助LLM。每个问题产生多步候选，按最小长度误差选择最佳候选，再报告答案匹配率、长度误差、Token F1、ROUGE-L、Token EM及不同阈值下的攻击成功率。

**复现信息**

攻击者假定拥有黑盒公开API，可提交任务输入、提供模型可能调用的工具并返回工具内容，但不能访问参数、梯度、logits、内部状态或目标模型 tokenizer。开源模型可使用原 tokenizer或同一第三方 tokenizer；专有模型则用公开代理 tokenizer估计候选长度。轨迹针对单一目标模型优化后固定部署；可用CoT摘要时采用LTGO，否则采用仅依赖长度的LGO。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- OpenThoughts：包含来自九个来源、覆盖数学、编程、化学和生物学等领域的推理问题。每个来源随机抽取 $100$ 道题，并按 $6{:}4$ 划分为 $540$ 道优化题和 $360$ 道测试题，优化集与测试集无重叠；优化过程只使用问题文本，不使用答案、标签或元数据。该数据集同时承担通用注入轨迹优化和同分布测试的作用。
- MATH500、JEEBench 和 LiveCodeBench：用于测试优化轨迹对未见数据集的迁移能力；每个数据集随机抽取 $100$ 道题进行评估。它们分别代表数学推理、考试型问题和代码任务，但摘录未提供更细的抽样或任务构成信息。
- 三个目标大推理模型（LRM）：DeepSeek-V4-Flash（2026-04-23 版本）、Qwen3.5-Plus（2026-02-15 版本）和 GLM-5.2（2026-06-16 版本）。实验记录原始思维链作为评估参照，但不向攻击者或注入优化器公开；攻击者只能看到工具调用参数以及目标思维链的摘要信息。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Token-EM**

衡量目标思维链中有多少令牌能够在允许插入或删除的对齐跨度中被精确匹配；它比 Token F1 和 ROUGE-L 更严格，强调近似逐字恢复。 （越高越好，因为较高分表示提取文本与目标思维链的精确令牌重合更多。）

</div>
<div class="metric-item" markdown="1">

**Length Error**

衡量提取思维链长度与目标思维链长度的偏差；开放模型使用同一分词器计算两者令牌数。摘录未给出该误差的具体公式。 （越低越好，因为较低误差表示提取轨迹的长度更接近目标轨迹。）

</div>
<div class="metric-item" markdown="1">

**Attack Success Rate（ASR@99、ASR@95、ASR@90）**

只有同时满足长度误差不超过 $1-x/100$ 且 Token-EM 不低于 $x/100$ 的样本才算成功；$x$ 分别为 $99$、$95$ 或 $90$。分母包含所有样本，未调用工具的样本计为失败。 （越高越好；更高的阈值代表更接近近乎逐字恢复，因此 ASR@99 比 ASR@90 更严格。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 当前源摘录在 Table 1 标题和表头处截断，未提供任何主结果数值、模型间比较、基线分数或 LGO 与 LTGO 的具体差异，因此无法完成有证据支撑的三条数值结果或决定性消融分析；原文未明确报告。
- 评估依赖 GPT-5-Nano 判断答案是否达到同一结论，而文本恢复指标依赖目标模型记录的原始思维链；这些设计可以衡量与目标轨迹的接近程度，但摘录未说明答案裁判的一致性校验、目标思维链是否具有唯一性，或恢复出的文本是否真正代表模型作答时的因果推理。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Direct Prompting：先仅给模型问题获得标准答案，再在后续轮次要求模型复现完整逐步推理；它检验简单的直接诱导是否足以恢复隐藏思维链。
- CoT Synthesis：由辅助大语言模型根据问题、最终答案和目标模型返回的思维链摘要，事后合成一条看似合理的思维链；它代表不直接恢复原始轨迹、而是重建 plausible 解释的方案。
- REP：使用影子模型生成“问题—推理—答案”示例，将三个示例以代码样式包裹并置于目标问题之前，以少样本上下文学习诱导隐藏推理；实验采用其三个示例和 Markdown 围栏的最佳设置。
- EchoCoT 的两种轨迹设置：LGO 仅优化长度保真度，LTGO 联合优化长度和文本保真度；二者用于检验加入文本层面目标是否带来额外收益。

**实验想回答的问题**

- 在攻击者只能观察工具调用参数、推理令牌数量和思维链摘要，而不能访问目标模型原始思维链的条件下，EchoCoT 能否提取与目标思维链在长度和文本内容上接近的推理轨迹？
- EchoCoT 相对于直接提示、事后思维链重建和少样本上下文诱导方法，能否在不同目标模型、任务来源和未见数据集上保持提取效果？

**实验实现**

针对每个目标模型，使用 OpenThoughts 优化集学习一个通用注入轨迹。每条轨迹最多包含 $K=3$ 个注入步骤；最后一步固定为继续生成最终答案，因此优化器实际搜索前两个注入步骤。LTGO 的文本思维链摘要只用于计算保真度分数，不进入优化上下文，从而避免优化器直接看到摘要文本。评估时将提取阶段的答案与 Direct Prompting 首轮标准推理答案比较，答案一致性由 GPT-5-Nano 判断；同时评估工具调用、答案一致性、长度保真度和文本保真度。当前摘录未包含 Table 1 的具体数值、完整优化提示词、思维链摘要流程或解码配置；后者据称位于附录 A.2。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：工作旨在从大型推理模型中提取不可见的思维链，核心涉及推理过程恢复与内部机制解释。; rule check: matched taxonomy keywords; top rule score=10.0
- 全文指纹：`11f2170752ad5a5098bb63d797ce1cb6e49c6f4b01a30ae354224cd3ea33a7af`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
