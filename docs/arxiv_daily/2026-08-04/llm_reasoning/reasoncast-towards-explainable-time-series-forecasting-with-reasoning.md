---
title: "[论文解读] ReasonCast: Towards Explainable Time Series Forecasting with Reasoning"
description: "[arXiv 2608.01875][LLM Reasoning] 本文针对时间序列预测与解释彼此割裂的问题，提出任务融合的“理解×生成”范式，使模型在一次自回归响应中先形成可核验的推理链，再据此生成数值预测。"
arxiv_id: "2608.01875"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:05:54.746520+00:00"
source_sha256: "7ec8a09251f071904d93d2504a908a340dbd8091871d5e32012bbd72cfb19ce3"
tags:
  - "LLM Reasoning"
  - "时间序列预测"
  - "可解释人工智能"
  - "大语言模型"
  - "自回归生成"
  - "推理链"
  - "联合预测与解释"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.01875</p>

# ReasonCast: Towards Explainable Time Series Forecasting with Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Seunghan Lee, Jun Seo, Jaehoon Lee, Junhyeok Kang, Sangjun Han, Sungdong Yoo, Minjae Kim, Tae Yoon Lim, Dongwan Kang, Hwanil Choi, Soonyoung Lee, Wonbin Ahn</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> LG AI Research</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01875v1) · [PDF 下载](https://arxiv.org/pdf/2608.01875v1) · **关键词** 时间序列预测, 可解释人工智能, 大语言模型, 自回归生成, 推理链, 联合预测与解释<br>
**代码**: [https://github.com/seunghan96/reasoncast](https://github.com/seunghan96/reasoncast)

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

本文针对时间序列预测与解释彼此割裂的问题，提出任务融合的“理解×生成”范式，使模型在一次自回归响应中先形成可核验的推理链，再据此生成数值预测。

**不用术语来说**：在许多实际场景中，仅给出未来数值并不足以支持决策：使用者还需要知道模型依据了历史序列中的什么规律，例如趋势、周期性或时间依赖。现有系统通常只预测数值、只回答关于序列的文字问题，或用彼此独立的路径完成两项任务，因此解释未必真正参与预测过程，也难以判断它是否只是事后编造的理由。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“理解×生成”任务框架，将推理文本$o_{\mathrm{rsn}}$与预测结果$o_{\mathrm{gen}}$建模为联合输出，并让预测显式依赖先生成的推理链，以区别于同一模型内相互独立的理解与生成任务。
- 作者围绕该研究缺口配套提出ReasonTS-Bench与ReasonCast：前者利用五类可分离的基础时间序列模式及真实推理链联合评估预测和解释，后者提供可用于微调大语言模型的训练方案，使两种输出能在一次自回归过程中生成。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

时间序列预测以按时间排列的历史观测为输入，目标是生成未来数值。现有研究大致分为四种设置：理解（U）仅用文本回答序列相关问题；生成（G）仅预测未来数值；理解加生成（U+G）在同一架构中支持两类任务，但通过彼此分离的查询或输出路径完成；本文关注的理解乘生成（U×G）则要求模型在一次响应中同时给出推理链和数值预测，并使预测以该推理为条件。这个区别对可解释预测很重要：系统不只需要报告“未来是多少”，还应说明它从周期性、趋势或时间依赖等可核验动态中如何推出该结果。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**时间序列预测**

根据按时间排序的历史观测值推断后续数值。与普通回归相比，样本顺序和跨时刻依赖关系是问题结构的一部分。

</div>
<div class="concept-item" markdown="1">

**自回归生成**

模型按顺序生成输出，每一步都以输入和此前已经生成的内容为条件。本文利用这一机制先生成推理链，再让后续预测显式依赖该推理链。

</div>
<div class="concept-item" markdown="1">

**事后解释**

事后解释是在预测已经形成后，再附加一个看似合理的说明，因此该说明未必真正参与预测。本文所需的解释应位于预测之前并对预测形成条件约束。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定历史时间序列$X$，模型需要在单次自回归响应中依次输出自然语言推理链$o_{\mathrm{rsn}}$和未来数值预测$o_{\mathrm{gen}}$。目标联合分布写为$p_{\theta}(o_{\mathrm{gen}},o_{\mathrm{rsn}}\mid X)=p_{\theta}(o_{\mathrm{rsn}}\mid X)\cdot p_{\theta}(o_{\mathrm{gen}}\mid o_{\mathrm{rsn}},X)$：模型先依据$X$解释其识别出的时间动态，再依据$X$和该解释产生预测。这里的关键假设不是“同一模型能够分别回答解释问题和预测问题”，而是两种输出必须处于同一生成过程，使推理在生成顺序和条件概率上先于预测；相应评价也应同时检查数值预测是否准确、推理步骤是否可验证，以及二者是否一致。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$X$**

作为模型输入的历史时间序列观测。

</div>
<div class="notation-item" markdown="1">

**$o_{\mathrm{rsn}}$**

模型生成的自然语言推理链，用于描述并推导序列动态。

</div>
<div class="notation-item" markdown="1">

**$o_{\mathrm{gen}}$**

模型生成的未来时间序列数值预测。

</div>
<div class="notation-item" markdown="1">

**$p_{\theta}$**

参数为θ的模型所定义的条件概率分布。

</div>

</div>

**直接相关的工作**

- **TimeOmni-VL**: 它使用视觉语言骨干同时支持时间序列理解与生成，是与本文最接近的U+G模型之一；但两条输出路径在给定输入后条件独立，用户一次只能选择一种提示，因此不能让同一响应中的解释直接约束预测。
- **FinSTaR**: 它将推理轨迹与金融时间序列预测联系起来，但仍把推理和预测视为分离的任务族。本文试图进一步把二者合并为一个联合自回归输出，并评价预测与推理的相互一致性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

时间序列预测常用于需要后续行动的决策场景，而用户通常必须先理解预测依据，才能判断结果是否可信、适用或值得执行。若系统只返回未来数值，用户无法确认模型究竟捕捉到了趋势、周期性或时间依赖等真实结构，还是偶然拟合了输入；因此，可解释预测需要同时提供数值结果及其有依据的形成过程。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单任务时间序列模型**：传统预测模型执行生成任务$G$，根据历史序列$X$直接输出未来数值$o_{\mathrm{gen}}$；另一类基于大语言模型的时间序列理解方法执行理解任务$U$，围绕$X$生成自然语言答案$o_{\mathrm{und}}$。两类方法分别优化数值预测或文本理解，并不同时解决两者。
- **理解与生成并置的统一模型**：近期$U+G$模型把两种能力放入同一架构，但仍以任务分离的条件分布$p_{\theta}(o_{\mathrm{und}}\mid X)$和$p_{\theta}(o_{\mathrm{gen}}\mid X)$产生输出。它们共享模型或输入，却没有把解释作为预测生成过程中的显式条件。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单任务方法只能给出文字理解或数值预测中的一种，无法在同一响应中回答“未来是什么”以及“为什么如此”，因而不能满足需要依据预测理由再采取行动的使用场景。
- $U+G$方法虽然具备两种能力，但输出沿相互分离的任务路径产生；解释不参与预测的条件生成，因此二者缺乏过程层面的因果衔接，也难以排除解释只是对既有预测进行事后合理化的可能。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少一种任务融合的时间序列建模与评测设置：模型应在单次响应中联合生成解释和预测，使$o_{\mathrm{gen}}$明确依赖$o_{\mathrm{rsn}}$，同时还需要带有真实推理依据的受控基准，以联合检验预测是否准确、解释是否对应序列中的实际模式。作者将这一空缺定义为“理解×生成”即$U\times G$，而非能力简单并置的$U+G$。

</div>
<div markdown="1"><span>核心问题</span>

能否把时间序列解释与数值预测构造成一个统一的自回归任务，使模型先输出基于输入$X$的推理链$o_{\mathrm{rsn}}$，再以该推理链为条件输出预测$o_{\mathrm{gen}}$，并对两部分进行联合、可核验的评价？

</div>
<div markdown="1"><span>作者直觉</span>

如果模型必须先明确识别序列中的基础规律，再根据这段推理生成未来值，那么解释就不再是预测完成后的附加文字，而成为预测计算路径中的中间依据。受控数据进一步为不同规律提供对应的真实推理链，使研究者能够分别检查模型是否识别了正确模式、是否按该模式外推，以及解释与预测是否一致；这为“解释确实指导预测”提供了比仅比较预测误差更直接的证据。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ReasonCast不是新的专用时序网络，而是一套把任意自回归大语言模型微调为“先解释、后预测”模型的训练方案。输入是序列化后的时间序列$X$；模型先判断其结构类型并选择对应输出模式，再生成包含参数估计与演化规则的推理链$o_{\mathrm{rsn}}$，最后在同一次自回归生成中，以$X$和$o_{\mathrm{rsn}}$为条件输出数值预测$o_{\mathrm{gen}}$。这种顺序使预测在生成时直接依赖已陈述的规则，而不是在预测完成后追加一段事后解释。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 序列读取与文本化

将数值时间序列序列化到语言模型输入中，使后续路由、参数估计、规则生成和预测均以同一个$X$为条件。原文节选未明确给出具体数值编码格式或分词方式。

<div class="method-step__io" markdown="1">

**输入**：长度可变的历史时间序列$X$，其上下文长度与预测步数随样本变化。<br>
**输出**：可由自回归语言模型处理的时序上下文表示。

</div>

**直观理解**：这一步相当于把一串数值写成模型能阅读的输入；模型不能依赖固定窗口位置，因为不同样本的历史长度和预测长度不同。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 模式路由

模型从周期、趋势、AR(1)时间依赖、多周期、结构突变以及未知模式中选择输出模式。默认的显式路由把模式类别作为第一个生成标记；隐式路由不输出该标记，而是在解码器内部完成模式与字段模板的选择。

<div class="method-step__io" markdown="1">

**输入**：序列化后的时间序列$X$。<br>
**输出**：选定的模式类别及其对应的推理链模式；隐式版本仅产生内部路由结果。

</div>

**直观理解**：不同结构需要回答不同问题，例如周期序列要估计周期，突变序列要识别变化点，因此模型先决定应使用哪一套分析表格。显式路由便于检查分类结果，隐式路由则让模型直接进入相应回答格式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 参数化推理

模型按$p_{\theta}(o_{\mathrm{rsn}}\mid X)$自回归生成推理链，依次填写输入分析和推理字段，包括可观测统计、估计参数、模式类型及其隐含的外推规则。字段依模式而异，其监督目标由合成序列的真实生成参数直接构造。

<div class="method-step__io" markdown="1">

**输入**：时间序列$X$以及路由选择的模式。<br>
**输出**：结构化推理链$o_{\mathrm{rsn}}$，其中包含估计参数$\hat{\theta}$和由参数确定的预测规则。

</div>

**直观理解**：模型不仅说“这是趋势”，还要写出趋势斜率、周期或变化点等可核验事实。由于训练数据的生成参数已知，每个字段都能与标准答案逐项比较，而不只依靠语言流畅度判断解释质量。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 条件预测与未知模式回退

模型按$p_{\theta}(o_{\mathrm{gen}}\mid o_{\mathrm{rsn}},X)$继续生成各未来时刻的数值；若路由结果为未知，则声明没有预定义模式适配，并外推近期局部趋势。推理和预测连续出现在同一次自回归生成中。

<div class="method-step__io" markdown="1">

**输入**：原始输入$X$和已经生成的推理链$o_{\mathrm{rsn}}$。<br>
**输出**：由“INPUT ANALYSIS、REASONING、PREDICTION”三块组成的统一响应，其中$o_{\mathrm{gen}}$给出预测区间内各时刻的数值。

</div>

**直观理解**：预测阶段必须接着模型自己刚写出的规则作答，因此可以检查预测数字是否真的遵守该规则。回退机制允许模型承认无法匹配已有结构，减少把陌生序列强行解释成某个已知模式的风险。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 推理链条件生成

$$
p_{\theta}(o_{\mathrm{rsn}}\mid X)
$$

**符号说明**

- $p_{\theta}$：参数为$\theta$的自回归语言模型所定义的条件概率分布。
- $X$：序列化后的历史时间序列输入。
- $o_{\mathrm{rsn}}$：模型生成的结构化推理链，包含模式判断、参数估计和演化规则。

<div class="equation-explanation" markdown="1">

**直观理解**：该式表示模型先根据历史序列生成解释。关键不在于产生自由形式文本，而在于输出可解析字段，使估计参数能够与合成数据的真实参数逐项核验。<br>
**原文位置**：第4节“ReasonCast”，Step 3: Reason

</div>

</div>

<div class="equation-block" markdown="1">

#### 推理条件化预测

$$
p_{\theta}(o_{\mathrm{gen}}\mid o_{\mathrm{rsn}},X)
$$

**符号说明**

- $p_{\theta}$：与推理阶段共享参数$\theta$的自回归语言模型。
- $X$：原始历史时间序列输入。
- $o_{\mathrm{rsn}}$：预测之前已经生成的推理链。
- $o_{\mathrm{gen}}$：按未来时刻排列的数值预测输出。

<div class="equation-explanation" markdown="1">

**直观理解**：该式明确要求预测同时依赖原始序列和先前解释，因此解释处于生成预测的因果顺序之前。它并不自动保证解释正确，但使解释与预测之间的规则一致性能够被直接测量。<br>
**原文位置**：第4节“ReasonCast”，Step 4: Forecast

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：ReasonCast采用监督微调，使单个自回归模型学习按目标顺序输出模式、推理链和预测块；监督响应中的推理字段来自已知生成参数，预测字段来自相应未来序列。就概率分解而言，训练同时提高正确推理链的条件概率$p_{\theta}(o_{\mathrm{rsn}}\mid X)$以及在该推理链下正确预测的条件概率$p_{\theta}(o_{\mathrm{gen}}\mid o_{\mathrm{rsn}},X)$。所给节选未明确写出完整的负对数似然损失、各输出块是否加权或是否屏蔽输入标记，因此不能据此断言存在额外的一致性正则项；Consistency和Sensitivity在文中被描述为评估指标，而非明确的训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. ReasonTS-Bench可验证监督构造**

基准以五种生成原语构造训练和测试样本：$s_1(t)+\varepsilon$、$s_1(t)+mt+b+\varepsilon$、$\alpha x(t-1)+\varepsilon$、$s_1(t)+s_2(t)+\varepsilon$以及在$t^*$处发生变化的分段线性过程，其中$s_i(t)=A_i\sin(2\pi t/P_i+\phi_i)$。每个样本的推理字段直接由生成参数填充，并额外设置训练和测试均出现的Unknown集合，以及只在测试出现的OOD-novel集合。

> 直观理解：真实数据通常没有“为什么这样预测”的唯一标准答案；合成数据则知道振幅、周期、斜率和变化点等真值，因此能同时监督预测数字与解释内容。Unknown和OOD-novel分别检验模型是否会承认不确定，以及能否面对训练中未出现的新动力学。

**2. 模式路由与结构化输出模式**

路由器并非独立分类网络，而是同一自回归模型生成过程的一部分。显式版本首先输出模式类别并以该结果约束后续字段，隐式版本省略类别标记；单模式专家则预先获得模式并为每种模式单独训练，用作近似预知类别的对照。

> 直观理解：该模块解决“应该解释哪些参数”的问题。共享模型还可跨模式学习共同的时序规律，而单模式专家用于判断联合训练带来的收益是否仅来自已知类别。

**3. 推理条件化预测解码器**

同一模型先生成$o_{\mathrm{rsn}}$，再以$o_{\mathrm{rsn}}$和$X$为条件生成$o_{\mathrm{gen}}$；由估计参数$\hat{\theta}$重新执行规则可得到$\tilde{y}=f_{\hat{\theta}}(x)$，从而比较直接生成的预测$\hat{y}$与规则推导值$\tilde{y}$。该设计把解释从预测后的附加文本改为预测的前置条件。

> 直观理解：如果模型声称序列每隔固定周期重复，它随后给出的数值就应当符合这个周期。重新运行其自述规则，可以发现“解释说一套、数字做另一套”的情况。

**训练与推理**

训练时，ReasonCast使用ReasonTS-Bench中带有完整三块目标响应的样本。五种原语提供已知模式和参数监督；Unknown样本同时进入训练与测试，教会模型输出低置信度、声明无预定义模式并采用局部趋势；OOD-novel仅用于测试，不参与训练。默认方案将各模式及无模式数据联合训练，使一个模型完成显式路由、结构化推理和数值预测；论文还比较隐式路由和每种模式单独训练的Single-pattern specialist。推理时无需外部时序模型或第二次调用：模型读取$X$，生成模式标记，继续生成$o_{\mathrm{rsn}}$，随后生成$o_{\mathrm{gen}}$；若判为Unknown，则走局部趋势回退路径。整个响应由一次连续的自回归解码完成。

**复现信息**

公平解释结果所需的关键信息是：默认骨干为Qwen2.5-3B，ReasonCast在五原语联合、无模式和显式路由设置下使用72k样本训练一个epoch；还在0.5B、1.5B和3B规模上训练，其中3B为默认。7B至9B大语言模型骨干采用低秩适配；所给节选没有报告其秩、缩放系数等细节。对照的时序模型按模式在12k训练集上训练20个epoch，并固定使用200步输入和100步输出头，而ReasonTS-Bench样本本身具有变化的上下文长度和预测跨度；因此跨模型比较时应注意专用时序模型的固定窗口设定。预测指标通常在每种模式$n=200$个测试样本上计算，推理指标仅适用于实际输出推理链的方法。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ReasonTS-Bench 的五类基础模式测试集：周期信号 Sine、带趋势周期信号 Trend、一阶自回归过程 AR(1)、多频信号 Multi-freq 和结构突变 Changepoint。每类包含 12,000 个训练样本、1,000 个验证样本和 1,000 个测试样本；单个样本的上下文长度为 $N\in[50,200]$，预测范围为 $H\in[10,100]$。这些受控合成数据同时提供未来数值和由生成参数闭式计算出的推理字段，因此可分别检验预测准确性与解释是否正确。
- Unknown 与 OOD-novel 集合用于检验模式拒识。Unknown 包含五种不属于基础模式的信号，按 12,000/1,000/1,000 划分，用于训练和测试“无匹配模式”判断；OOD-novel 仅有 500 个测试样本，包含四种训练时从未出现的过程，用于检验拒识能力能否迁移到真正未见的生成机制。
- Counterfactual probe 是逐模式构造的成对测试集，每种模式约有 100 至 150 对样本。每对 $(x,x')$ 只改变一个生成参数，例如把正弦振幅或周期从 $\theta_j$ 改为 $\theta'_j$，用于判断模型陈述的对应推理字段是否随干预变化，以及其他字段是否保持稳定。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**MAE（表中记为 Error）**

预测序列与真实未来序列之间的平均绝对误差，直接衡量数值预测准确性。该指标可用于比较语言模型、朴素方法和专用时间序列模型，但不能评价解释质量。 （越低越好，因为误差越小表示预测值越接近真实未来值。）

</div>
<div class="metric-item" markdown="1">

**Fidelity**

将模型输出的各个推理字段与样本的真实生成参数或派生字段进行容差匹配，衡量解释是否忠实描述当前输入。不同字段使用附录表 18 给出的绝对或相对容差；因此它检查的是结构化事实是否正确，而不是文本是否流畅。 （越高越好，因为更高比例的推理字段与该样本的真实结构相符。）

</div>
<div class="metric-item" markdown="1">

**Consistency**

衡量推理内容与模型最终预测之间是否相互一致。它与 Fidelity 的区别是：Fidelity 对照真实生成结构，Consistency 关注模型自己的解释和预测是否形成同一套判断。 （越高越好，因为解释与预测之间的矛盾更少。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 默认 Qwen2.5-3B 骨干：使用 ReasonCast 与少样本、未训练版本比较，五类基础模式取平均。

<div class="result-value" markdown="1">

使用 ReasonCast 后，MAE 从 $2.223$ 降至 $0.236$，Fidelity 从 $0.252$ 升至 $0.899$，Consistency 从 $0.275$ 升至 $0.613$，Sensitivity 从 $0.138$ 升至 $0.794$。

</div>

这是最直接的联合任务结果：同一训练方案同时改善了未来数值和解释字段，而不是以牺牲预测换取更好看的文本。作者据此主张 ReasonCast 能把预测与自解释融合起来。分析上，这组对照仍同时改变了训练数据、监督目标和参数更新方式，因此不能仅凭它断言性能提升完全来自“显式推理”本身；输出顺序消融提供了更针对性的因果证据。

<div class="result-source" markdown="1">

来源：表 6，Reasoning abilities

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen2.5-3B (Default) w/o ReasonCast 2.223 0.252 0.275 0.138 w/ ReasonCast 0.236 0.899 0.613 0.794

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨骨干迁移：Qwen2.5-7B、Llama-3.1-8B、Phi-3.5-mini 和 Gemma-2-9B 分别比较使用与不使用 ReasonCast。

<div class="result-value" markdown="1">

四个非默认骨干使用 ReasonCast 后都同时降低 MAE 并提高三项推理指标。例如 Qwen2.5-7B 的 MAE 从 $1.721$ 降至 $0.316$，Fidelity、Consistency 和 Sensitivity 分别从 $0.338$、$0.250$、$0.142$ 提高到 $0.859$、$0.532$、$0.714$。

</div>

结果表明该方法更像一种可迁移的训练配方，而不是只适配某个 3B 模型的专用结构；其他三个模型家族也呈现相同方向的变化。不过不同尺寸模型采用的微调方式并不完全相同，大模型使用 LoRA，因此这些数值不适合被解释为骨干架构或参数规模的严格排名。

<div class="result-source" markdown="1">

来源：表 6，Reasoning abilities

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen2.5-7B w/o ReasonCast 1.721 0.338 0.250 0.142 w/ ReasonCast 0.316 0.859 0.532 0.714

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 五类基础模式上的预测轨迹，并与朴素预测器、专用时间序列模型、TimeOmni-1 及语言模型基线比较。

<div class="result-value" markdown="1">

作者报告，应用 ReasonCast 的多种语言模型在预测准确性上超过了专用时间序列模型；图 4 中使用 ReasonCast 的轨迹在五种模式上均能跟随真实序列，而未使用该方案的轨迹很快发生漂移。当前摘录未包含表 5 的逐模型数值，因此不能核验超过各专用模型的具体幅度。

</div>

该实验回答 ReasonCast 的解释能力是否以明显损害数值预测为代价。作者给出的结论是否定的，并声称其预测优于专用模型。但这只是在由五种已知生成机制构成的受控基准上成立，尚不能直接外推到含缺失值、非平稳噪声或复杂外生变量的真实业务序列。

<div class="result-source" markdown="1">

来源：第 5.1 节；表 5 与图 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The results show that applying ReasonCast to a range of LLM backbones gives them a TS forecasting ability that outperforms even the specialized TS forecasting models.

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

- 朴素预测器，包括延续最后观测值等简单规则，用来判断模型是否真正学到了动态结构，而非仅依赖短期持平假设。
- DLinear、PatchTST、iTransformer 和 TimeXer 四类专用时间序列预测模型。它们是数值预测能力的主要参照，但只输出预测值，因而不能参加推理指标比较。
- TimeOmni-1 代表能够在统一架构中处理时间序列理解与生成的模型，用于区分“同一模型支持两项任务”与“在同一回答中融合推理和预测”这两种能力。
- Qwen、Llama、Phi 和 Gemma 指令语言模型分别以少样本提示和微调方式运行。前者对应不使用 ReasonCast 的骨干模型，后者用于检验该训练方案能否跨模型家族迁移，而非只对默认 Qwen2.5-3B-Instruct 有效。

**实验想回答的问题**

- ReasonCast 能否让同一个语言模型在一次自回归输出中同时获得准确的数值预测与可核验的文本推理，并在预测误差上与专用时间序列模型竞争？
- 生成的推理是否真正依据输入并参与预测，而不是预测完成后的合理化文本或对训练样本参数的记忆？

**实验实现**

默认实例 ReasonCast-3B 以 Qwen2.5-3B-Instruct 为骨干，在 ReasonTS-Bench 训练集上全参数微调。应用到其他骨干时，不超过 3B 参数的模型采用全参数微调，更大的模型采用 LoRA。模型在一次自回归过程中先生成模式相关的结构化推理链，再生成数值预测；默认显式路由版本把模式类别作为第一个输出 token。未使用 ReasonCast 的语言模型获得少量上下文示例，以保证其理解任务和预测任务的输出格式可比较。结果取三个随机种子的平均值，但所给正文仅说明默认模型的标准差位于附录 J，当前摘录未提供具体标准差。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 输出顺序消融：保持训练目标和模型不变，只比较“先预测、后推理”与“先推理、后预测”。 | 先预测时 MAE、Fidelity 和 Consistency 分别为 $0.471$、$0.293$、$0.345$；先推理时分别为 $0.404$、$0.837$、$0.465$。即先推理使 MAE 降低约 $0.070$，Fidelity 提高 $55$ 个百分点，Consistency 提高 $13$ 个百分点。 | 该消融隔离了推理在生成流程中的位置。若解释只是预测后的装饰文本，交换顺序不应大幅改变解释忠实度或预测误差；实际结果显示先生成推理更好，支持推理 token 为后续预测提供条件信息。它仍不能证明自然语言中的每一步都具有因果必要性，但比单纯比较有无微调更能说明推理不是完全事后的合理化。 | 表 7，第 5.2 节 Order of reasoning & forecast<br><span class="experiment-evidence">Forecast → Reasoning 0.471 0.293 0.345; Reasoning → Forecast 0.404 0.837 0.465; Δ (improvement) −0.070 +55 pp +13 pp</span> |
| 反事实干预：成对输入只改变一个真实生成参数，比较未使用与使用 ReasonCast 时对应字段的 Sensitivity，以及未干预字段的 Stability。 | 使用 ReasonCast 后，Sine、Trend、AR、Multi-freq 和 Changepoint 的 Sensitivity 分别从 $0.270$、$0.200$、$0.050$、$0.070$、$0.100$ 提高至 $0.960$、$0.880$、$0.530$、$0.820$、$0.780$；可定义 Stability 的四类模式也均有提升，例如 Sine 从 $0.705$ 提高至 $0.905$。AR 只有一个推理字段，没有未干预字段可检查，因此 Stability 未定义。 | Sensitivity 检查模型是否跟随被改变的参数，Stability 检查它是否避免无关字段一起漂移；两者结合可区分“完全忽略干预”和“所有解释字段随意变化”。结果支持模型确实读取输入中的局部生成变化，但这里的“因果”限于已知合成机制上的受控参数干预，不等同于对真实世界因果关系的识别。 | 表 8、图 5，第 5.2 节 Counterfactual probing<br><span class="experiment-evidence">Sensitivity ↑ w/o ReasonCast 0.270 0.200 0.050 0.070 0.100 w/ ReasonCast 0.960 0.880 0.530 0.820 0.780; Stability ↑ w/o ReasonCast 0.705 0.690 – 0.680 0.650 w/ ReasonCast 0.905 0.890 – 0.765 0.840</span> |

**定性案例**

- 附录图 9 展示了反事实探针的成功与失败：改变 Sine 的振幅时，模型陈述的 detected amplitude 随之变化，Sensitivity 为 $0.94$；替换 Multi-freq 的慢周期包络时，模型报告的 period 2 几乎不变，Sensitivity 仅为 $0.09$。前者说明模型能局部追踪参数，后者则暴露了对多尺度、层级周期结构感知不足的问题；因此平均分提升并不意味着所有结构字段都已可靠识别。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出让 LLM 在单次自回归生成中联合完成时间序列预测与可验证推理链的方法和评测基准。; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`7ec8a09251f071904d93d2504a908a340dbd8091871d5e32012bbd72cfb19ce3`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
