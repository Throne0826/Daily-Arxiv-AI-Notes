---
title: "[论文解读] Autoregressive Mosaics: Probing 2D Spatial Reasoning in Text-Only Language Models"
description: "[arXiv 2608.30751][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.30751"
announcement_date: "2026-09-01"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:35:16.670260+00:00"
source_sha256: "03f4d226f257d0ac36da456f124c9e0846e2b27d817f7e747d05f3cf64000e67"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "LLM 机制与可解释性"
  - "二维空间推理"
  - "文本与代码语言模型"
  - "程序化绘图"
  - "布局组合"
  - "输出媒介"
  - "SVG"
  - "激活探测"
  - "AM-Bench"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.30751</p>

# Autoregressive Mosaics: Probing 2D Spatial Reasoning in Text-Only Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Ashwin Nedungadi, Stefan Oehmcke, Stefan Lüdtke</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Institute for Visual & Analytic Computing (VAC), University of Rostock</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30751v1) · [PDF 下载](https://arxiv.org/pdf/2608.30751v1) · **关键词** 二维空间推理, 文本与代码语言模型, 程序化绘图, 布局组合, 输出媒介, SVG, 激活探测, AM-Bench<br>


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

本文位于文本生成、程序合成与二维空间推理的交叉领域。文本和代码语言模型可以根据自然语言生成绘图程序，但生成可辨认图像并不必然说明模型具有二维布局的内部表示：模型可能只是把已经明确的空间描述翻译成代码。因此，本文将“空间表达”与“空间组合”区分开来，研究模型能否从不完整描述中决定对象的位置、大小及相互关系，并将该布局通过某种输出媒介实现为图像。图像由程序确定性渲染为小型栅格图像，从而把语言模型的输出、几何布局和最终图像连接成可评估的流水线。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**二维空间布局**

指图像中对象的几何安排，包括位置、大小、形状、颜色以及对象之间的关系，例如“在……上方”“位于……内部”或“彼此相邻”。本文特别关注模型能否在提示信息不完整时主动组合出这样的安排。

</div>
<div class="concept-item" markdown="1">

**程序化绘图与输出媒介**

程序化绘图是让模型输出代码，再由确定性执行器运行代码并生成图像；输出媒介则是模型表达图像的形式，例如画布绘图代码或原始 SVG 标记。媒介可能增加或减少表达某种布局的难度，因此最终图像质量不只取决于模型本身。

</div>
<div class="concept-item" markdown="1">

**自回归生成**

自回归模型按顺序生成输出，每一步都依据提示和此前已经生成的内容预测下一个符号。对本文而言，这意味着模型可能在绘制过程中持续更新几何状态，而不是先形成一个完全固定的布局计划再机械执行。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

AM-Bench 将图像表示为由程序生成并经确定性执行器栅格化的自回归马赛克。其核心设置包含两个互补任务：翻译任务的输入是已经完整指定图像几何结构的文字提示，输出是能够产生该几何图像的绘图代码；布局任务的输入是空间信息不完整的文字提示，输出是模型自行决定布局后生成的绘图表示及其栅格图像。翻译任务主要控制代码生成和几何表达能力，布局任务则额外要求模型进行空间组合。实验还比较画布程序代码与原始 SVG 两种输出媒介，并通过生成前的激活探测及几何状态干预，考察模型是否具有可解码的布局表征以及是否在生成过程中使用它。翻译任务使用连续坐标中的精确面积几何指标，不依赖画布分辨率；布局任务没有唯一参考几何，因此由视觉语言模型按照提示匹配度评分，并以人工评分作为支持性验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$AM\text{-}Bench$**

Autoregressive Mosaics 基准，用于分离二维空间组合能力与空间描述到代码的表达能力。

</div>
<div class="notation-item" markdown="1">

**$T$**

翻译任务；提示完整给出目标几何，模型需要输出实现该几何的代码。

</div>
<div class="notation-item" markdown="1">

**$L$**

布局任务；提示只部分规定目标图像，模型需要自行确定空间布局并生成图像表示。

</div>
<div class="notation-item" markdown="1">

**$24\times24$**

画布媒介下用于展示和评判的栅格尺寸；评判提示明确将图像描述为由彩色像素组成的 $24\times24$ 网格。

</div>

</div>

**直接相关的工作**

- **文本与代码模型生成绘图程序的工作（例如 GPT-4 生成 TikZ 独角兽）**: 这些工作证明了未直接观看图像的语言模型能够根据文字生成可辨认图形，但只观察最终图像，无法区分模型真正组合了二维布局，还是仅将明确的空间描述翻译成绘图代码。AM-Bench 通过翻译任务和布局任务的拆分直接检验这一区别。
- **需要视觉输入的图像识别基准**: 相关识别基准主要评估模型理解已有视觉输入的能力，而本文研究的是仅接受文本和代码训练、且在生成时不接收图像的模型能否构造二维空间布局。因此，本文将识别能力与文本条件下的空间组合能力区分开来。原文未明确列出这些基准的具体名称。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

纯文本与代码训练的语言模型能够生成绘图程序，但一幅最终图像同时受三种能力影响：模型能否构思合理的二维布局、能否把布局准确写成可执行代码，以及所用输出媒介是否便于表达几何关系。若只观察生成图像的好坏，就无法判断失败究竟来自空间推理、代码表达还是媒介限制，也无法据此可靠比较不同模型的二维空间能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **视觉识别型空间基准**：向模型提供图像等视觉输入，再通过位置识别、空间关系判断或视觉问答评估其空间能力。这类方法适合研究视觉语言模型，却不能直接回答仅用文本和代码训练的语言模型是否形成了可用的二维空间表征。
- **基于最终生成结果的程序绘图评测**：要求模型生成 TikZ、画布程序或其他绘图代码，再根据渲染图像是否正确或可辨认进行总体评分。该范式可以证明模型有时能够画出图形，但通常不单独测量“根据既定几何写代码”与“自行决定对象布局”这两个环节。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有生成评测把空间构图和代码表达混在同一个结果中：较差的图像既可能说明模型没有形成合理布局，也可能只是说明它不熟悉指定绘图接口，因此最终分数不能定位真正瓶颈。
- 既有评测通常固定一种输出媒介，并只检查最终产物，因而难以判断媒介本身对表现的影响，也无法检验模型是在生成前形成具体且固定的空间计划，还是在自回归生成过程中逐步维护和修改几何状态。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一种面向纯文本与代码语言模型的受控评测框架，能够分别测量既定二维几何的表达能力和欠定描述下的自主构图能力，同时进一步控制输出媒介，并考察生成前及生成中的内部空间表征。这个缺口使“模型会画图”无法被严格解释为“模型具备二维空间推理”。

</div>
<div markdown="1"><span>核心问题</span>

论文要回答的是：纯文本语言模型在多大程度上能够自主组合二维空间布局；观测到的差异是否可由代码生成能力解释；输出媒介会如何限制这种能力；以及模型究竟在生成前形成可执行的具体布局计划，还是在生成过程中增量构造并追踪几何状态。

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把绘图过程拆成可对照的环节：当提示词已经完整给出几何结构时，任务主要检验模型能否把空间描述翻译成代码；当提示词故意不规定具体布局时，模型还必须自行完成空间构图。比较两者可以隔离额外的布局能力，再通过更换代码接口与探测内部激活，分别判断表达媒介和内部规划机制的作用。直观地说，这相当于先确认模型是否“会照施工图施工”，再测试它是否“会自己设计施工图”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

AM-Bench将文本型语言模型的二维空间能力拆成两个行为阶段：翻译任务向模型提供完整、精确的几何文字描述，要求其生成受限绘图程序；布局任务只提供对象名称和少量外观信息，要求模型自行构造空间布局。程序通过六种原语渲染为$24\times24$光栅图像；翻译任务用符号几何指标$\mathrm{PIoU}$评分，布局任务则由两个视觉语言模型从提示符合度、形状、颜色、空间准确性和完整性五个维度评分。直观地说，翻译测试模型能否把“已经画好的施工图”写成代码，布局测试模型能否从简短要求自行决定“画什么、放在哪里以及如何组合”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造受限二维绘图环境

模型只能使用$\mathrm{fill}$、$\mathrm{set\_pixel}$、$\mathrm{rect}$、$\mathrm{circle}$、$\mathrm{line}$和$\mathrm{poly}$六种原语，并可使用算术、迭代和数学运算；程序随后被栅格化为$24\times24$图像。光栅化分别采用Bresenham直线算法、中点圆填充和多边形填充。

<div class="method-step__io" markdown="1">

**输入**：模型生成的单个渲染函数，以及预定义的绘图API。<br>
**输出**：受统一接口约束的绘图程序及其$24\times24$输出图像。

</div>

**直观理解**：这相当于给所有模型同一套很小的积木，而不是允许它调用现成的绘图库。低分辨率减少计算成本，同时迫使评价集中在形状和空间组合，而不是细节绘制。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行翻译任务

模型将完整的文字几何描述直接翻译成受限绘图程序；参考提示使用行列网格和类型—范围描述，例如给出圆心位置与半径，而不使用“太阳”等真实对象名称。生成的每个原语被分配给其重叠面积最大的参考部件，低于最小重叠阈值的原语不分配，然后在连续归一化坐标中计算几何重叠。

<div class="method-step__io" markdown="1">

**输入**：包含所有参考部件类型、位置、大小和颜色的几何文字提示，以及对应参考几何$R_1,\ldots,R_n$。<br>
**输出**：每个模型对已知几何配置生成的程序、图像和翻译分数$\mathrm{PIoU}$或带过度绘制惩罚的分数。

</div>

**直观理解**：任务故意把“应该画成什么”说清楚，因此主要考察模型能否忠实地把文字施工图转换成代码，而不是考察它是否会自行设计布局。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行开放式布局任务

模型必须自行推断空间结构并生成绘图程序；由于欠充分提示通常没有唯一正确图像，不能使用参考几何的$\mathrm{PIoU}$，而由Qwen2.5-VL-7B和InternVL3-8B依据相同评分规程，对五个维度分别给出$0$至$5$分。

<div class="method-step__io" markdown="1">

**输入**：只说明对象名称及至多粗略外观的欠充分提示；每个模型使用150条提示，覆盖元素、标志性对象和组合布局三层类别。<br>
**输出**：每个生成图像的多维布局评价和模型级布局分数；只有其中位翻译分数达到预设阈值$\tau_{\mathrm{trans}}=0.6$的模型才进入跨模型布局比较。

</div>

**直观理解**：这里不再告诉模型具体位置，因此模型需要自己形成空间方案。两个视觉评委分别检查“是否符合要求、形状和颜色是否正确、位置关系是否正确、内容是否完整”，以减少单一自动指标的偏差。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 进行表示探测与输出介质比较

实验比较程序媒介与SVG媒介对布局成绩的影响，并在生成前后及生成过程中探测模型激活，以判断是否存在粗粒度布局计划以及模型是否持续追踪已生成的几何状态。

<div class="method-step__io" markdown="1">

**输入**：模型在生成过程中的内部激活，以及相同或可比布局要求下的不同输出媒介，包括受限程序API和原始SVG。<br>
**输出**：关于输出媒介、潜在布局计划和生成时几何状态跟踪的行为与表示层证据。

</div>

**直观理解**：这一步检查低布局成绩究竟来自模型不会规划，还是来自代码这种表达方式不适合它。激活探测还用于区分“事先固定好整张图”与“边生成边更新空间状态”两种生成机制。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 部件平均交并比

$$
\mathrm{PIoU}=\frac{1}{n}\sum_{i=1}^{n}\frac{|R_i\cap\hat{G}_i|}{|R_i\cup\hat{G}_i|}\in[0,1]
$$

**符号说明**

- $n$：参考图中的部件数量。
- $R_i$：第$i$个参考部件的连续几何区域。
- $\hat{G}_i$：分配给第$i$个参考部件的生成原语并集。
- $|\cdot|$：几何区域的面积。
- $\cap$：两个区域的交集。
- $\cup$：两个区域的并集。

<div class="equation-explanation" markdown="1">

**直观理解**：该式先分别计算每个参考部件与模型生成部件的交并比，再对所有部件取平均；完全重合时该部件得分为$1$，没有重合时为$0$。因为直接使用连续几何面积而不是像素计数，理论上不依赖输出分辨率。<br>
**原文位置**：第3.2节，式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 过度绘制惩罚后的翻译分数

$$
\mathrm{PIoU}_{\mathrm{pen}}=\mathrm{PIoU}\times(1-\text{over-paint fraction})
$$

**符号说明**

- $\mathrm{PIoU}_{\mathrm{pen}}$：考虑额外绘制区域后的翻译评分。
- $\mathrm{PIoU}$：未惩罚的部件平均交并比。
- $\text{over-paint fraction}$：生成的额外、未请求绘制区域所占比例。

<div class="equation-explanation" markdown="1">

**直观理解**：模型不能通过先画对目标部件、再覆盖大量额外形状来获得高分；额外区域越多，乘法惩罚越强。无效输出的分数为$0$。<br>
**原文位置**：第3.2节

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告针对AM-Bench任务进行模型训练或参数优化；该基准主要进行推理时评测。模型生成绘图程序，翻译任务以符号$\mathrm{PIoU}$及其过度绘制惩罚评分，布局任务以视觉语言模型评分，因此没有由本文定义并用于反向传播的训练损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 受限原语绘图API**

绘图程序只能调用六种原语，并在统一$24\times24$画布上运行；环境允许算术、循环和数学函数，但不提供通用SVG词汇。作者选择自定义原语词汇，以降低模型从预训练数据中记忆SVG模板所造成的数据污染风险。

> 直观理解：API像一套专门为实验设计的简化画笔，限制模型使用熟悉的现成图形模板，从而更接近测试零样本空间组合能力。

**2. 翻译任务与符号几何评分**

翻译提示显式提供每个部件的类型、位置、范围和颜色；生成原语按最大重叠分配到参考部件，再用连续坐标中的精确多边形裁剪计算每部件IoU并取平均。该任务只测试从文本计划到代码的映射，不足以证明模型内部已经形成了独立的布局计划。

> 直观理解：它把“想象布局”和“写出代码”分开：因为答案的几何结构已被文字规定，模型只需准确照着执行。

**3. 开放式布局评价与表示探测**

布局任务没有唯一参考答案，因此由两个视觉语言模型在五个整体维度上进行$0$至$5$分评价，并设通过阈值为$3.0$；跨模型比较还要求模型的中位翻译分数达到$\tau_{\mathrm{trans}}$。内部激活探测用于分析生成前的粗粒度布局信息，以及生成期间是否表示不断演化的几何状态。

> 直观理解：开放题不能只问“像不像唯一标准答案”，所以评价模型同时看多个方面。翻译门槛避免把“连基本代码都写不好”的模型误判为空间推理差。

**训练与推理**

评测使用八个开放权重、仅以文本和代码训练的模型进行推理；布局部分每个模型使用150条合成提示，并对多个样本进行生成，源文摘要报告总规模为$8$个模型、每模型$11$个样本。推理结果先由绘图API渲染，再分别进入翻译几何评分或布局视觉评价；只有中位翻译分数达到$\tau_{\mathrm{trans}}=0.6$的模型才用于跨模型布局比较，内部激活则在生成前后及生成过程中进行探测。

**复现信息**

画布固定为$24\times24$，颜色使用推荐的30个颜色名称，以避免颜色词元化成为混杂因素。翻译参考集包括从布局生成中分层抽取的145个配置、沿四个受控难度轴新增的100个配置，以及13个手工制作图标；翻译通过阈值$\tau_{\mathrm{trans}}=0.6$在查看分数前预先设定，并据原文称高于随机基线。布局提示分为T1元素、T2标志性对象和T3组合布局三层，每层含五个子类别、每个子类别10条提示；所有150条正式提示由Claude Opus 5合成，早期人工提示仅用于构造示例而不属于发布套件。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- AM-Bench Layout 任务：包含 $150$ 个提示词；每个提示词生成 $11$ 次，即 $1$ 次确定性生成和 $10$ 次随机生成，用于评估提示不完全指定时的开放式布局能力。原文未明确报告训练集、验证集或测试集划分。
- AM-Bench Translation 任务：将完整指定的几何图像描述直接作为用户输入，要求模型生成可执行绘图代码；该任务作为代码翻译能力的对照，检验模型能否把已知空间关系落实为程序操作。原文未明确报告独立样本总数。
- Exp. 3 行为与表征分析数据：使用 $145$ 个真实 Layout 提示；表征阶段按各模型的有效生成构造本模型的共识占据目标，最终每个模型使用 $138$–$145$ 个提示。因果行为阶段包含 $731$ 个项目、$165$ 个模型—提示组合、$2{,}924$ 个项目—干预配对和 $26{,}316$ 个评分续写，用于测试模型是否实际利用布局信息。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**VLM composite score**

视觉语言模型在提示符合度、形状准确度、颜色准确度、空间准确度和完整性五个维度上分别以 $0$–$5$ 的整数评分，复合分数是五项均值；通过阈值 $3.0$ 判定是否通过。 （越高越好，因为它表示生成图像在内容、形状、颜色、空间关系和元素覆盖方面更符合提示。）

</div>
<div class="metric-item" markdown="1">

**out-of-fold pooled $R^2$**

嵌套交叉验证中，利用模型隐藏状态预测其自身共识占据图的解释方差；$R^2$ 衡量激活能够解释多少布局目标变化。 （越高越好；但必须结合文本基线和可靠性上限解释，不能把高于基线直接等同于模型已经执行了完整布局规划。）

</div>
<div class="metric-item" markdown="1">

**drew_anything**

在给定续写前缀后，模型是否继续输出任意画布调用；它是代码层面的二值行为指标，不直接依赖被干预语句下方最终呈现的像素。 （在特定行为比较中，若模型对被移动到未使用位置的语句更可能继续绘制，说明它对当前几何状态存在响应；单独的更高绘制率并不等于空间定位更准确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 八个模型的 Layout 视觉评分

<div class="result-value" markdown="1">

模型间开放式布局能力差异显著。按 Judge 1 的所有层级和模型汇总，GLM-4 32B 的五项分数为 $3.56$、$3.57$、$3.80$、$3.60$、$3.57$，而 CodeLlama 34B 为 $1.65$、$1.64$、$2.19$、$1.70$、$1.65$；颜色准确度是每个模型中最高的维度，整体颜色均值为 $3.11$。

</div>

这说明模型规模或代码训练背景并不能单独预测开放式二维布局质量：同为文本与代码模型，生成结果仍有明显差距。由于评分来自 VLM 判定，且提示允许多种合理布局，因此结果支持“布局能力不同”的结论，但不能证明某个模型具有类似视觉系统的精确二维内部地图。

<div class="result-source" markdown="1">

来源：Appendix C.1，Judge 1 的逐维度评分表

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GLM-4 32B 3.56 3.57 3.80 3.60 3.57
CodeLlama 34B 1.65 1.64 2.19 1.70 1.65
Pooled 2.72 2.72 3.11 2.76 2.72

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 预先指定几何的 Translation 与开放式 Layout 的对比

<div class="result-value" markdown="1">

摘要报告八个模型都能可靠地把明确指定的几何描述翻译为代码，但开放式 Layout 表现差异很大；因此代码生成能力不能解释全部二维空间表现。原文所给摘录未明确报告 Translation 与 Layout 的完整数值表。

</div>

Translation 只要求模型把已经给出的对象、位置和形状转成 API 调用，主要测试语义到程序的映射；Layout 还要求模型从不完整描述中决定构图。两者的分离使作者能够把“会写绘图代码”和“会组织二维布局”区分开，但该摘录不足以量化二者的相关程度。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across eight open-weight text-and-code-only models, all models reliably translate specified geometry into code, but their open-ended layout performance differs substantially, indicating that these differences are not explained by code-generation ability alone.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Exp. 3 的预生成表征与生成中几何状态使用

<div class="result-value" markdown="1">

激活对本模型共识布局的解码能力高于 TF-IDF 文本基线，平均增量为 $\Delta R^2=+0.164$，八个模型的增量范围为 $+0.130$ 至 $+0.205$，且均经多重比较校正显著，$p_{\mathrm{FDR}}\leq0.0004$。但跨模型自己的目标与其他模型目标的平均差仅为 $+0.015$，特定于模型的布局残差在 GLM-4 32B 和 Gemma 2 27B 中分别为 $R^2=0.005$ 和 $-0.005$。行为干预还显示，在模型已完成图像的情形，原坐标语句后停止率对应的继续绘制率为 GLM-4 32B 的 $43.8\%$ 到 $84.6\%$、Gemma 2 27B 的 $2.5\%$ 到 $41.2\%$，差值分别为 $+0.415$ 和 $+0.387$。

</div>

结果支持一个较窄而重要的结论：生成前激活中存在与提示所暗示的粗粒度布局相关的信号，生成时模型也会根据被改变的空间状态调整是否继续绘制。但跨模型选择性弱、特定布局残差几乎不可解码，说明该信号更像共享的提示条件化计划，而不是模型独有且预先固定的完整图纸；行为实验也只能约束模型“会使用某些状态信息”，不能证明具体神经机制。

<div class="result-source" markdown="1">

来源：Appendix D.2.1，Result and controls；行为结果见 Appendix D.2.2 Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Decodability exceeds the text baseline for all eight models, every interval excluding zero and every model significant after Benjamini-Hochberg correction: mean Δ R2 = +0.164, from +0.130 (Qwen2.5-Coder 14B) to +0.205 (Gemma 2 9B), all pFDR ≤ 0.0004, prompt-clustered bootstrap with 10,000 resamples.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 开放式 Layout 没有唯一金标准，视觉评分依赖两个 VLM 评审；虽然作者报告了维度分数和评审比较，但摘录未提供完整的人类评审一致性或统计检验信息，因此分数可能同时反映媒介可读性和视觉评价偏差。
- Exp. 3 的因果行为测试只覆盖 GLM-4 32B 与 Gemma 2 27B，共 $731$ 个项目；移动坐标会改变语句所处的渲染状态，且 $4$ 像素条件有 $64\%$–$69\%$ 的位置重叠，所以结论主要约束这两个模型的行为，不应外推为所有八个模型都使用同一内部机制。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Translation 任务：将已明确指定几何的代码生成作为能力门槛，而不是布局性能基线；若翻译可靠但开放布局较差，说明问题不只是代码生成。
- TF-IDF 文本基线：用提示文本的词面特征预测布局占据，作为非神经表征、近似词袋信息的比较；探针必须在每个训练折内重新拟合，避免测试集选择偏差。
- Embedding-layer 表征控制：探测模型第 $0$ 层嵌入表示，其预期接近词袋式文本表示，用于检验深层激活的增益是否超出表面文本信息。
- Prompt-to-activation permutation 控制：打乱提示与激活的对应关系，检验探针结果是否来自真实的提示—表征对应，而非数据或回归程序的偶然相关。

**实验想回答的问题**

- 文本与代码模型能否仅凭语言提示完成二维图像布局，而不仅是把已经明确的几何描述翻译成绘图代码？
- 模型的布局表现差异是否还受到输出媒介影响，并且模型是否在生成过程中利用不断变化的几何状态？

**实验实现**

实验评估了四个模型家族、$8$ 个开放权重文本与代码模型，参数规模为 $8$B–$34$B，包括 Qwen2.5-Coder、Gemma 2、GLM-4、CodeLlama 和 Llama 3.1；模型逐一加载。Layout 每个提示进行 $11$ 次生成。生成媒介主要比较 $24\times24$ 画布 API 的 Python 代码与原始 SVG；SVG 还被重新栅格化为 $24\times24$，以隔离媒介本身和抗锯齿分辨率的混淆。表征实验对真实生成所用的完全相同聊天模板输入执行一次前向传播，不进行生成，在所有层、三个 token 位置上提取激活，随后标准化、PCA 和岭回归，并在嵌套交叉验证内选择层、位置、PCA 维度和正则强度。行为因果实验截断模型首次绘图语句，再将该语句原样保留或仅替换数字坐标后继续生成；每个项目—干预条件生成 $8$ 个续写。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 输出媒介消融：Canvas 代码对比 SVG，并进行分辨率匹配 | 分辨率匹配后的 SVG 相对原生 Canvas 的复合分数增量在八个模型上汇总为 $+0.37$；各模型为 $+0.09$ 至 $+0.76$。原生比较的汇总增量为 $+0.49$，高于分辨率匹配结果。 | 该消融隔离模型不变、提示不变时，仅改变模型表达图像的媒介。分辨率匹配后增益仍存在，说明 SVG 的优势不完全来自抗锯齿或原生渲染质量；原生与匹配结果的差异则表明渲染方式确实会影响评价。Qwen2.5-Coder 32B 的匹配置信区间包含零，因此媒介效应并非每个模型都同样稳定。 | Appendix D.1，Table 6；正文 Sec. 4.2<br><span class="experiment-evidence">Pooled +0.49 +0.37 [0.26,0.47]</span> |
| 生成中空间状态的因果干预：原坐标、移动到未使用位置、移动到后续将使用位置 | 在模型已经完成图像的分层中，把自身绘图语句移动到未使用位置后，GLM-4 32B 的继续绘制率差值为 $+0.415$，置信区间为 $[0.268,0.564]$；Gemma 2 27B 为 $+0.387$，置信区间为 $[0.219,0.563]$，两者 $p_{\mathrm{FDR}}=0.0007$。小位移条件的增量分别为 $+0.084$ 和 $+0.155$，低于大位移条件的 $+0.415$ 和 $+0.387$。 | 干预只替换语句中的数字坐标，保持图元类型、尺寸、颜色和文本格式不变，因此较直接地测试位置变化是否影响后续生成。大位移引起更强的继续绘制反应，符合模型追踪当前几何状态的解释；但该实验只有两个模型，而且干预改变了渲染状态，所以它支持行为层面的“使用”，不能单独确定内部计算机制。 | Appendix D.2.2，Results<br><span class="experiment-evidence">Handed its own statement unmodified, it stops; handed the displaced version, it keeps drawing, from 43.8% to 84.6% for GLM-4 32B and from 2.5% to 41.2% for Gemma 2 27B (Δ = +0.415, CI [0.268, 0.564] and Δ = +0.387, CI [0.219, 0.563], both pFDR = 0.0007).</span> |

**定性案例**

- Exp. 3 的目标设计本身是一个关键方法性案例：作者放弃用每个提示的一次参考生成作为唯一真值，改用同一模型多次有效生成的 $6\times6$ 共识占据概率作为连续目标。这样承认开放式 Layout 允许多个合理答案，避免把某一次随机布局误当成唯一正确布局；相应地，表征结果更适合解释为对提示约束下共享布局结构的解码，而不是对单一图像的逐像素复原。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Introduces a benchmark and probing analysis for 2D spatial reasoning and planning in text-only language models.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`03f4d226f257d0ac36da456f124c9e0846e2b27d817f7e747d05f3cf64000e67`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
