---
title: "[论文解读] When Text and Numbers Disagree: Evidence Arbitration in Large Language Models"
description: "[arXiv 2608.20116][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.20116"
announcement_date: "2026-08-21"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-21T02:04:57.292493+00:00"
source_sha256: "c484af4415af6f1ff34d81a1941a98e685deb2406f861d54469d4b682a0cf362"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "多模态推理"
  - "证据整合"
  - "冲突解决"
  - "数值推理"
  - "证据仲裁"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.20116</p>

# When Text and Numbers Disagree: Evidence Arbitration in Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-21</span>
<span><strong>作者</strong> Mattia Carletti, Edward Phillips, Fredrik K. Gustafsson, Patitapaban Palo, Lei Clifton, Danielle Belgrave, Xiao Gu, David A. Clifton</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Nuffield Department of Primary Care Health Sciences, University of Oxford, Oxford, UK；Affiliation: Oxford Suzhou Centre for Advanced Research, University of Oxford, Suzhou, Jiangsu, China；Department of Engineering Science；University of Oxford</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20116) · [PDF 下载](https://arxiv.org/pdf/2608.20116) · **关键词** 大语言模型, 多模态推理, 证据整合, 冲突解决, 数值推理, 证据仲裁<br>


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

本文位于大语言模型（LLM）证据整合与工具增强决策系统的交叉领域。研究重点不是让模型单独完成文本理解或数值预测，而是考察当自然语言摘要、数值时间序列和外部工具输出对同一个二元决策给出相反结论时，模型如何进行“证据仲裁”（即优先采用、整合或舍弃相互冲突的信号）。这一问题与医疗、制造和金融等高风险场景相关，因为不同来源可能具有不同的时间新鲜度、可靠性和证据来源属性；但现实数据通常难以明确标注这些属性及真实标签，因此本文采用由潜在风险轨迹生成的受控合成基准，以便分别研究这些因素。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**证据仲裁**

证据仲裁是指模型面对支持不同结论的多个信息源时，决定应优先相信哪一个，或如何综合这些信息。本文特别关注文本证据与数值证据发生冲突时的选择行为。

</div>
<div class="concept-item" markdown="1">

**潜在风险轨迹**

潜在风险轨迹是随时间变化但不直接呈现给模型的真实风险状态。它被用来生成数值时间序列、文本摘要和最终二元标签，从而使研究者知道每个证据是否与真实状态一致。

</div>
<div class="concept-item" markdown="1">

**证据来源属性**

本文主要区分时间新鲜度、来源可靠性和证据来源类型。来源类型包括直接观察到的上下文与外部工具生成的预测，这些属性可以与文本或数值模态分别组合，形成可控冲突。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个二元决策提示，以及由同一潜在风险过程产生但可能来自不同时间窗口的数值时间序列、自然语言摘要和外部预测等证据，模型需要输出目标时刻的二元判断，例如高风险或低风险。基准构造的核心假设是：在每个冲突实例中，恰有一个证据源与由潜在风险轨迹确定的真实标签一致，其他证据源支持相反结论；研究者可以独立改变证据模态、时间新鲜度、来源可靠性和证据来源类型。模型的任务因此不是精确预测连续数值，而是在异质且相互矛盾的证据中识别应被优先采用的信号。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$T+k$**

目标决策时刻；图示中的冲突判断发生在该时刻。

</div>
<div class="notation-item" markdown="1">

**$T$**

参考时间点，数值时间序列和文本摘要可以从相对于该时间点不同的窗口生成。

</div>
<div class="notation-item" markdown="1">

**$s$**

证据源；可指数值时间序列、文本摘要或外部生成的预测等输入来源。

</div>
<div class="notation-item" markdown="1">

**$y$**

二元真实标签，表示目标时刻由潜在风险轨迹决定的正确决策类别。

</div>

</div>

**直接相关的工作**

- **文本证据冲突与参数知识—上下文知识冲突研究**: 既有工作研究了文本来源之间的矛盾，以及模型参数中存储的知识与推理时提供的外部上下文之间的不一致，并发现模型可能受到证据位置、表达风格等因素影响。本文将问题推进到文本与数值证据直接支持相反决策的场景，而不是只研究文本内部或参数知识与上下文之间的冲突。
- **LLM 数值任务、时间序列预测与工具增强系统研究**: 相关研究探索了利用重编程、多模态提示和跨模态对齐完成数值或时间序列任务，也研究了模型在工具调用和代理式决策中整合外部信息的方法。本文不以精确数值预测为目标，而是将任务设为二元判断，以隔离模型在文本、数值观测和外部预测相互冲突时的证据优先级。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在医疗、制造和金融等决策场景中，模型可能同时接收文本摘要、数值观测和外部工具输出，而这些证据可能指向相反结论。例如，较新的文字报告可能认为风险较低，但较早的生命体征或传感器数据可能显示风险升高。若模型优先采纳过时、不可靠或预测性工具输出，便可能在正确证据已经出现在输入中的情况下仍作出错误决策。随着大语言模型被用于工具增强型和多源决策系统，理解其如何处理证据冲突成为可靠性问题。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **多源知识或文本冲突处理**：这类研究考察不同文本来源之间的矛盾，或模型内部参数知识与外部知识之间的冲突，重点是判断应相信哪一段文字或哪类知识。它为研究模型的证据优先级提供了基础，但主要处理文本与知识来源的差异。
- **跨模态推理、数值推理与工具使用**：跨模态研究通常让模型联合处理图像和文本，数值推理研究考察模型从数字或时间序列中计算、比较和预测，工具使用研究则考察模型如何利用外部模型或程序输出完成任务。这些方向分别覆盖了相关能力，但通常不把文本证据、数值证据和工具生成证据放在同一任务中，并要求它们支持相互排斥的决策。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有工作缺少对文本证据与数值证据直接冲突时的系统刻画，因此无法回答模型究竟偏好哪种模态，以及这种偏好是否会导致模型忽视本应采纳的证据。
- 真实数据中的来源可靠性、时间对应关系、证据来源性质和真实标签往往不明确，使研究者难以独立操纵这些因素并判断错误究竟来自模态偏好、时间新近性、来源可靠性，还是对外部预测的过度信任。其后果是不同实验结果难以归因，也难以识别稳定的证据仲裁策略。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚未解决的问题是：在只有一个证据来源与真实标签一致、其他来源明确支持相反决策的受控条件下，如何分别测量大语言模型受到模态、时间新近性、来源可靠性和证据来源性质影响的程度。现有研究尚未提供一个能够同时控制这些变量、并系统揭示模型证据仲裁偏差的统一评测框架。

</div>
<div markdown="1"><span>核心问题</span>

当文本摘要、数值时间序列和外部工具输出支持相互冲突的二元决策时，大语言模型会优先采纳哪一种证据；这种选择如何随证据的模态、时间新近性、来源可靠性和来源性质而变化？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是构造受控合成基准：先由潜在风险轨迹生成数值序列和自然语言摘要，再有意安排冲突，使恰好一个来源与真实标签一致。这样可以像控制实验一样逐一改变证据的新旧、可靠程度和是否为直接观测或外部预测，同时保持其他条件可比。若模型仍稳定地选择错误来源，就能更清楚地说明它依赖了某种启发式线索，而不是把错误归因于真实世界数据本身的混乱。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法不是训练一个新的预测模型，而是构建一个用于测量大语言模型证据仲裁能力的受控基准。每个样本从潜在风险轨迹生成数值证据、文本摘要及可选的外部工具预测，并安排其中两个证据源支持相反标签且仅一个与真实未来标签一致；模型据此判断未来时刻 $T+k$ 的风险高低。整体流程依次为生成轨迹、生成文本、构造冲突提示词，以及通过答案令牌的分类对数几率评估模型选择了哪一类证据。直观地说，研究者先制造一组“数字和文字意见不一致”的小型决策题，再观察模型在时间新近性、可靠性、模态和工具权威性之间如何取舍。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 潜在风险轨迹生成

首先将未来目标值设为 $y_{T+k}=0.5+m$（high）或 $y_{T+k}=0.5-m$（low），再依据带高斯加性噪声的随机线性过程反向生成从时刻 $1$ 到 $T$ 的观测轨迹。主实验采用 $T=16$、$k=1$，并为每个观测配上时间戳。

<div class="method-step__io" markdown="1">

**输入**：二元目标标签（high 或 low）、潜在斜率 $s$、阈值边际 $m$、噪声尺度 $\sigma$、观测长度 $T$ 和预测步长 $k$。<br>
**输出**：一条带时间戳的数值风险时间序列，以及与之对应的未来二元真实标签。

</div>

**直观理解**：可以把它理解为先决定未来风险会越过还是低于 $0.5$，再倒推一段带随机波动的历史记录，使历史与未来标签保持可控关系。这样所有题目的“正确答案”都由生成过程明确给出，而不是依赖人工判断。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 文本证据生成

将连续特征离散为低、中、高或弱、中、强等语义类别，再使用模板和同义词随机组合成自然语言摘要；摘要不包含底层时间序列的明确数值。为制造模态冲突，保留原数值证据，同时从相反标签条件下重新采样另一条轨迹并将其转写为文本。

<div class="method-step__io" markdown="1">

**输入**：数值风险时间序列及其高层轨迹特征，包括初始水平、趋势方向和强度、是否跨越阈值，以及末端相对阈值的位置。<br>
**输出**：与数值证据语义一致或相冲突的文本摘要，且冲突标签可由生成器精确控制。

</div>

**直观理解**：这一步把一串数字翻译成“风险逐渐上升、最后仍处于高位”之类的话，但不直接泄露精确数值。需要冲突时，数字和文字分别来自不同的未来结果，因此两者都像合理证据，却只有一方正确。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 冲突场景与提示词构造

通过模块化模板组合任务说明、证据块、二元问题和 A/B 选项，并控制四类冲突：同窗口但模态相反、不同窗口且较新来源正确、带缺失或损坏标记的可靠性冲突，以及与上下文相反的工具预测。系统还改变证据出现顺序、领域框架（通用、医疗、工业、金融）和答案选项映射，以检验位置与令牌偏差。

<div class="method-step__io" markdown="1">

**输入**：数值证据、文本证据、真实标签，以及可选的外部预测值和领域框架。<br>
**输出**：用于模型推理的二元选择提示词，每个样本明确包含可比较的冲突证据和未来风险问题。

</div>

**直观理解**：研究者像做实验室控制实验一样，每次只突出一种“应该相信什么”的线索。例如让较新的记录始终正确，或让带有缺失值的一方始终不可靠，从而判断模型是否真的使用了这些线索，而不只是随机猜测。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 模型推理与证据仲裁评估

将提示词输入模型，直接读取二元答案令牌 “A” 和 “B” 对应的 logits，并依据其映射得到 high/low 预测；在冲突条件下计算准确率，同时与只提供正确单一证据源的单模态参考条件比较。各实验结果对三个随机种子取平均。

<div class="method-step__io" markdown="1">

**输入**：生成的提示词，以及待测的开放权重指令微调模型，包括 Qwen3、Gemma、Llama 和 Mistral 系列。<br>
**输出**：每个模型、冲突维度、证据顺序和领域条件下的分类预测及准确率，用于分析模型偏好的证据来源。

</div>

**直观理解**：模型不需要生成长篇解释，只需在 A、B 中选一个；研究者直接比较两个答案令牌的偏好，避免文字生成格式或解码随机性掩盖模型实际选择。若准确率接近零，说明模型不是犹豫，而是系统性地相信了错误来源。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 随机线性风险轨迹过程

$$
x_{t+1}=x_t+s+\epsilon_t,\qquad \epsilon_t\sim\mathcal{N}(0,\sigma^2)
$$

**符号说明**

- $x_t$：时刻 $t$ 的潜在风险值。
- $s$：潜在斜率，控制总体趋势的方向和幅度。
- $\epsilon_t$：时刻 $t$ 的随机扰动。
- $\mathcal{N}(0,\sigma^2)$：均值为 $0$、方差为 $\sigma^2$ 的高斯分布。
- $\sigma^2$：观测过程的噪声方差。

<div class="equation-explanation" markdown="1">

**直观理解**：下一时刻的风险等于当前风险、一个持续的趋势变化和随机波动之和。它使轨迹既有可解释的上升或下降趋势，又不会像人工画出的直线一样过于规则；研究者随后以反向递推方式生成观测历史。<br>
**原文位置**：第 3.3 节“Time Series Generation”，图 3A

</div>

</div>

<div class="equation-block" markdown="1">

#### 未来二元标签的目标值设定

$$
y_{T+k}=\begin{cases}0.5+m,&\text{if high},\\0.5-m,&\text{if low}.\end{cases}
$$

**符号说明**

- $y_{T+k}$：预测 горизон 时刻 $T+k$ 的目标风险值。
- $T$：观测窗口的最后时刻。
- $k$：从观测末端到目标时刻的预测步数，且 $k\geq1$。
- $m$：目标值距离二元决策阈值 $0.5$ 的边际。
- $high, low$：分别表示目标值高于或低于 $0.5$ 的二元标签。

<div class="equation-explanation" markdown="1">

**直观理解**：生成器先把未来值放在阈值 $0.5$ 的上方或下方，再要求模型只回答 high/low，而不是预测精确数字。这样实验主要测量模型在冲突证据中的取舍能力，而不是其细粒度数值回归能力。<br>
**原文位置**：第 3.1 节“Task Definition”及第 3.3 节“Time Series Generation”、图 3A

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未报告对本文基准或证据仲裁模块进行额外训练，也没有提出需要优化的新模型目标。研究对象是现成的开放权重指令微调大语言模型；评估目标是二元分类准确率，即模型是否选择与真实未来标签一致的答案，而不是通过梯度优化训练一个仲裁器。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 随机线性风险轨迹生成器**

轨迹由带潜在斜率和高斯噪声的随机过程生成，并通过目标标签与阈值边际 $m$ 固定未来值。该设计允许独立控制趋势方向、目标与阈值的距离、观测窗口和预测步长，同时构造数量相等的 high 与 low 样本。

> 直观理解：它相当于一个可调节的风险数据模拟器：研究者可以明确指定未来是高风险还是低风险，再生成一段看起来合理但带噪声的历史。平衡标签可避免模型只靠某一答案出现得更多而获得高分。

**2. 模板化文本与提示词生成器**

文本生成器从轨迹抽取离散语义特征，再通过模板和同义词采样产生摘要；提示词生成器将领域框架、任务指令、证据块、问题和答案选项模块化拼接，并显式控制证据顺序和答案映射。

> 直观理解：该模块把“数据内容”和“题目写法”分开控制：内容决定哪一方正确，写法决定哪一方先出现、使用什么领域背景。这样可以区分真正的证据仲裁与“最后出现的信息更容易被记住”等表面效应。

**3. 四维冲突操控与对照模块**

基准分别操控模态先验、时间新近性、来源可靠性和工具预测。可靠性通过对数值序列随机遮蔽 $50\%$ 的值并写入 NaN，或在文本中加入观测不完整或损坏的说明来标记；工具冲突则令上下文与真实标签一致、外部预测与其相反。

> 直观理解：四类操控分别回答四个问题：模型是否偏爱数字或文字、是否相信较新的证据、是否会降低对损坏来源的信任、是否盲从一个看似专业的外部预测。每类冲突都只让一个来源与真实答案一致，因此选择结果可以直接解释为仲裁策略。

**训练与推理**

训练阶段：原文未明确报告本文进行了任何模型训练；时间序列生成器、文本生成器和提示词生成器用于离线构造评测样本，而非作为待优化的神经网络。推理阶段：对每个提示词，将文本、数值和可选工具预测按指定顺序输入模型，读取答案令牌 “A” 与 “B” 的 logits，再依据预设的答案映射得到 high/low；随后在四种冲突条件及单模态参考条件下计算准确率，并对三个随机种子求平均。实验还改变证据顺序、答案选项顺序和领域框架，以测量位置偏差、令牌偏差和领域表述对仲裁的影响。

**复现信息**

为复现实验，需保留以下关键设置：风险值范围为 $[0,1]$，二元阈值为 $0.5$；主实验使用 $T=16$、$k=1$，模拟采样频率为每分钟一次；数值证据以时间戳—数值对呈现并保留两位小数，文本摘要不包含显式数值；可靠性损坏通过随机遮蔽数值时间序列的 $50\%$ 并写入 NaN，文本则加入观测不完整或损坏的说明；每个冲突维度使用 high/low 数量相等的数据。提示词包括通用、医疗、工业和金融四种框架，并将答案严格设为 A/B，但正式评估使用 logits 而非自由生成。待测模型包括 Qwen3 的 1.7B、4B、8B、14B 规模，以及 Gemma-2-9B-It、Llama-3-8B-Instruct 和 Mistral-7B-Instruct-v0.3；未提供的样本数量、具体随机分布参数、工具预测生成细节和完整默认配置应以附录原文为准，所给章节未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 主仲裁实验使用受控生成的平衡数据集，覆盖基线模态先验、时间新近性、来源可靠性和工具预测四类冲突设定；每个设定包含$2000$个实例，每个标签$1000$个。其作用是确保每次冲突中恰有一个证据源与真实标签一致，从而把性能差异主要归因于证据仲裁。
- 每类冲突同时改变证据呈现顺序，用于检验提示中的位置新近性效应；实验材料保持冲突结构不变，仅改变哪个证据先出现或后出现。原文未明确报告各数据集的训练集、验证集和测试集划分。
- 敏感性分析沿用基线模态先验设定，每个条件使用$1000$个实例，以默认领域、标签语义“ A=high ”和答案顺序“ A ”在前作为基线，分别改变领域或答案选项配置。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**分类准确率**

模型选择与真实标签一致的答案比例；在冲突条件中，它同时反映模型识别正确证据和抵抗错误证据的能力。 （越高越好；准确率低于$0.5$表示在二分类平衡条件下系统性偏向错误证据。）

</div>
<div class="metric-item" markdown="1">

**单模态参考准确率**

只输入与真实标签一致的证据源时的准确率，用于衡量模型对该证据类型本身的理解能力。 （越高越好；它高而冲突准确率低，说明问题更可能出在仲裁而非基础理解。）

</div>
<div class="metric-item" markdown="1">

**相对基线的绝对准确率变化**

敏感性分析中，将每个领域或答案配置的准确率与默认配置的准确率作差，并跨扫描值、随机种子和证据顺序聚合为均值$7$标准差。 （绝对变化越小越稳健；较大的变化表示仲裁行为对表面配置更敏感。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 基线模态先验冲突：文本证据与数字证据矛盾，并改变证据顺序

<div class="result-value" markdown="1">

所有模型在单模态参考条件下均取得很高准确率，因此冲突条件的差异主要反映仲裁行为。Qwen3各变体系统性偏好数字证据；Llama和Mistral相对更依赖文本证据；Gemma在两种模态间最均衡。正确证据通常放在提示后部时准确率更高，且文本证据比数字证据更明显地受“最后出现”影响。原文还报告，若文本正确而数字证据错误，若干较大的Qwen3模型准确率低于$0.5$，但未给出具体数值。

</div>

这说明模型并非单纯依据哪条证据更准确，而是带有稳定的模态先验，并会受到证据位置影响。Qwen3在数字冲突中低于随机水平支持“系统性偏向数字证据”的解释，但不能据此断言数字处理能力本身更强，因为模型间单模态数字准确率也不同，且原文没有给出完整数值表。

<div class="result-source" markdown="1">

来源：第4.1节，图4A–4B

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen3 models consistently favour numerical evidence, whereas Llama and Mistral models show comparatively stronger reliance on textual evidence.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 时间新近性与来源可靠性冲突

<div class="result-value" markdown="1">

时间新近性产生了比基线模态先验更强且更一致的仲裁行为；模型通常更信任时间上更新的证据，并且当该证据更晚出现在提示中时准确率更高。Gemma在不同顺序下最稳定，Qwen3也较可靠地遵循时间新近性线索。相比之下，来源可靠性冲突在大多数模型上造成的性能下降大于时间新近性冲突，说明显式可靠性是较弱的仲裁线索。原文未明确报告这些比较的具体准确率。

</div>

模型能够使用“哪个信息更新”这一线索，但不能同样稳定地使用“哪个来源更可靠”这一线索。这里的结论是不同冲突设计之间的相对行为差异，不等于证明模型真正理解了现实世界中的时间或来源可信度；实验只证明它们在受控提示中对这些线索作出不同反应。

<div class="result-source" markdown="1">

来源：第4.2–4.3节，图4C–4F

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across both evidence order settings (Figures 4E–4F), reliability conflicts produce larger performance drops than temporal recency conflicts across most models, suggesting that explicit source reliability is a weaker arbitration cue than temporal recency.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 工具预测与上下文测量冲突

<div class="result-value" markdown="1">

工具预测冲突造成所有实验中最强的性能下降，表明许多模型即使面对与上下文测量系统性矛盾的外部预测，仍会过度依赖该预测。上下文证据在工具预测之后出现时，准确率明显提高；若上下文证据正确但先出现，Qwen3和Gemma有时接近零准确率。Llama和Mistral受错误工具预测影响较小，冲突条件下通常仍保持相对较高准确率。原文未明确报告具体准确率。

</div>

外部工具输出似乎获得了比普通文本、数字或可靠性标记更高的默认权重，因而可能压过直接且正确的上下文测量。把上下文放在后面能部分纠正这种过度依赖，但这只说明提示顺序具有缓解作用，不证明模型已经学会可靠地验证工具预测。

<div class="result-source" markdown="1">

来源：第4.4节，图4G–4H

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Figures 4G–4H show that tool forecast conflicts produce the strongest degradation observed across all experiments, indicating that many models heavily over-rely on external forecasts even when these systematically conflict with the provided contextual measurements.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验使用受控生成的平衡冲突数据，主要测量模型在人工构造证据矛盾下的行为；原文未明确报告真实世界数据、训练/验证/测试划分或外部任务上的验证，因此结果对实际应用场景的外推范围有限。
- 主结果大量依赖图4的趋势性描述，所提供原文未包含完整图表数值；此外，提示顺序、答案token映射和答案选项配置都可能影响准确率，因此部分观察到的模型差异可能混合了证据偏好与格式、位置敏感性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 单模态参考条件：只提供与真实标签一致的证据源，图中以阴影柱表示；它检验任务本身是否容易，并作为冲突条件的能力上限参考。
- 双证据冲突条件：同时提供一个正确证据和一个冲突证据，图中以实心柱表示；它是核心比较条件，用于直接测量模型如何仲裁矛盾信息。
- 不同证据顺序条件：比较正确证据先出现与后出现的结果；它用于隔离提示位置新近性，而不是新的模型基线。
- 跨模型家族比较：比较Qwen3、Llama、Mistral和Gemma的仲裁模式；这不是传统任务基线，而是用于判断证据偏好是否具有架构或模型家族差异。

**实验想回答的问题**

- 在文本与数字、时间新近性、来源可靠性及工具预测发生冲突时，不同大语言模型如何选择证据，且这种仲裁是否受到证据呈现顺序和模型家族的影响？
- 仲裁行为对领域设定、答案选项配置等表面提示结构是否稳健，还是会在保持单模态性能稳定时产生显著变化？

**实验实现**

模型在推理模式下使用HuggingFace Transformers和PyTorch、贪心解码（$do\_sample=false$）以及最多$5$个生成token。最终预测不是根据生成文本，而是根据答案token“ A ”和“ B ”在下一token分布中的logits决定；作者确认两种答案在各模型分词器中均为单token（含前导空格）。输入采用左侧填充、批大小为$8$，使用FP16在GPU上推理；生成文本仅用于定性检查，不参与评估。每项结果平均于$3$个随机种子。所有实验在单张NVIDIA RTX PRO 5000 Blackwell（$48$GB显存）上完成，总计算成本约$40$ GPU小时。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 领域实例化敏感性：在基线模态先验设定中改变领域，其他参数保持默认 | 文本单模态条件对领域变化通常不敏感；在数字单模态和冲突条件中，部分模型出现更明显变化。原文未明确报告具体绝对变化数值。 | 该分析检验结论是否只适用于某个抽象或通用领域。文本条件较稳定而数字及冲突条件更易变化，说明领域语境可能影响模型如何解释数字证据或进行仲裁；但由于提供的节选未包含表A2具体行，不能判断每个模型变化的方向和大小。 | 第4.5节，表A2<br><span class="experiment-evidence">As shown in Table A2, sensitivity to both domain specialization and answer choice configuration is generally low in text-only settings, but more noticeable effects emerge in numeric-only and conflicting settings for several models.</span> |
| 答案选项配置敏感性：改变标签语义或答案顺序，并与默认配置比较 | 答案选项扰动可能在单模态性能相对稳定时，仍导致冲突准确率显著变化；Qwen3家族的稳健性通常随规模提高而改善，14B模型在各设定中相对稳定。原文未明确报告具体变化数值。 | 该分析隔离的是提示表面形式，而不是证据内容本身。若只改答案映射或选项顺序就改变冲突准确率，说明模型的仲裁决策可能依赖格式线索；这削弱了把冲突准确率直接解释为稳定推理能力的做法，但不能据此确定规模是唯一原因。 | 第4.5节，表A2<br><span class="experiment-evidence">In particular, answer choice perturbations can produce significant shifts in conflict accuracy despite relatively stable unimodal performance, indicating that arbitration behaviour can depend on superficial prompt structure.</span> |

**定性案例**

- 一个具有代表性的定性现象是：在文本证据正确、数字证据错误且两者冲突时，若错误数字证据具有较强位置或模态优势，较大的Qwen3模型可能达到低于随机水平的准确率；在工具预测冲突中，Qwen3和Gemma甚至可能在正确上下文证据先出现时接近零准确率。这说明失败不是随机犹豫，而是对错误证据的系统性偏好；不过原文未提供单个实例的完整提示、模型输出或逐案例分析，因此不能把它当作独立案例研究。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Studies how large language models reason over and arbitrate conflicting textual and numerical evidence.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`c484af4415af6f1ff34d81a1941a98e685deb2406f861d54469d4b682a0cf362`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
