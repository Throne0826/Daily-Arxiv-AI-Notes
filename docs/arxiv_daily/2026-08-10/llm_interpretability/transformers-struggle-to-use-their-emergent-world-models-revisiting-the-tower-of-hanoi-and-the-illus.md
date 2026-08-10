---
title: "[论文解读] Transformers Struggle to Use Their Emergent World Models: Revisiting the Tower of Hanoi, and the Illusion of Thinking"
description: "[arXiv 2608.07077][LLM 机制与可解释性] 原文未明确报告。"
arxiv_id: "2608.07077"
announcement_date: "2026-08-10"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-10T02:39:08.642659+00:00"
source_sha256: "c9a529228115f6923d7ef40565296010fc56fc16a98869f9d6f28ad049fbbf75"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "大型推理模型"
  - "汉诺塔规划"
  - "涌现世界模型"
  - "机制可解释性"
  - "线性探针"
  - "激活干预"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2608.07077</p>

# Transformers Struggle to Use Their Emergent World Models: Revisiting the Tower of Hanoi, and the Illusion of Thinking

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-10</span>
<span><strong>作者</strong> Devin Pereira, Willem Zuidema</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Artificial Intelligence Program, University of Amsterdam；Institute for Logic Language and Computation, University of Amsterdam</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.07077v1) · [PDF 下载](https://arxiv.org/pdf/2608.07077v1) · **关键词** 大型推理模型, 汉诺塔规划, 涌现世界模型, 机制可解释性, 线性探针, 激活干预<br>


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

本文位于大语言模型规划与机制可解释性研究的交叉领域。研究对象是大型推理模型（Large Reasoning Models，LRMs）：这类模型通常先生成较长的思维链，再给出最终答案。本文关注一个关键问题：模型在解决规划任务时，是否在内部形成了关于任务状态空间的“世界模型”，以及这种表示是否真正参与了决策。为回答该问题，作者结合线性探针、表示干预和激活修补等方法，研究模型内部是否编码了汉诺塔状态空间的几何结构，并检验该表示与实际解题成功之间的因果关系。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**汉诺塔规划任务**

汉诺塔要求在若干柱子之间移动大小不同的圆环：每次只能移动某根柱子最上方的圆环，且较大的圆环不能放在较小圆环上方。规划的目标是在满足这些约束的前提下，把给定初始状态转换为指定目标状态。

</div>
<div class="concept-item" markdown="1">

**涌现世界模型**

世界模型是模型内部对任务环境状态及其变化规律的表示。本文所说的“涌现”表示模型只接受动作序列或解题文本训练，却自行形成了可从隐藏状态中解码的任务状态表示，而非被直接提供一个显式模拟器。

</div>
<div class="concept-item" markdown="1">

**线性探针与因果干预**

线性探针是在模型隐藏表示上训练一个简单的线性预测器，用来检验某种信息是否容易被读取；能被解码只能说明信息存在，不能说明模型使用了它。因果干预则直接替换或修改模型激活，观察输出是否随之改变，从而检验该表示是否参与了实际规划。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

本文研究三柱汉诺塔的两类设定。标准设定要求初始状态和目标状态分别将所有圆环集中在单根柱子上；平面到平面（flat-to-flat）变体则允许初始状态和目标状态分布在多根柱子上，因此需要处理更一般的状态转换。模型输入是描述初始状态、目标状态及规则的提示，输出是满足移动约束并完成状态转换的动作计划；在大型推理模型设置中，模型还会生成较长的思维链。作者重点考察圆环数为 $N$ 时的规划表现，特别关注 $N\geq 4$ 后的性能下降，并分析模型隐藏表示是否编码了该任务的状态空间。该状态空间具有谢尔宾斯基三角形的几何结构，本文将其作为检验内部世界模型是否忠实表示任务状态的依据。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$N$**

汉诺塔中的圆环数量。

</div>
<div class="notation-item" markdown="1">

**$N\geq 4$**

圆环数量不少于四个；摘要指出大型推理模型在这一规模后开始在多数任务上失败。

</div>
<div class="notation-item" markdown="1">

**$S$**

汉诺塔的状态空间，即所有满足圆环堆叠约束的配置及其结构；文中将其几何结构描述为谢尔宾斯基三角形。

</div>
<div class="notation-item" markdown="1">

**$T$**

从初始状态到目标状态的动作计划或解题轨迹。

</div>

</div>

**直接相关的工作**

- **Shojaee et al. (2025)**: 该工作将汉诺塔用于评估大型推理模型，报告模型能够解决标准设定，却在任务规模超过少量圆环后出现显著准确率下降，并观察到推理轨迹在问题变难时反而变短。本文继承这一问题设定，但进一步追问性能崩溃究竟源于模型没有形成任务表示，还是形成后无法维持该表示。
- **Li et al. (2022)**: 该工作表明，仅根据棋步序列训练的小型 Transformer 可以在隐藏状态中编码棋盘位置，构成涌现世界模型。本文借鉴其“序列训练加表示探测”的思路，将研究对象扩展到汉诺塔规划，并结合因果干预检验表示是否真正参与解题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大推理模型能够完成证明、编程和高难考试题，但在不使用工具时却不能稳定完成汉诺塔这类规则明确、可逐步验证的规划任务。尤其当任务规模增大时，失败会使模型在需要长程状态跟踪的规划场景中缺乏可靠性；因此，关键科学问题不只是测出准确率下降，而是识别模型内部究竟缺少问题表征、无法从表征读出动作，还是在生成推理过程时遗失了已获得的状态信息。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于任务准确率与推理链长度的行为评测**：已有工作让大推理模型输出汉诺塔移动方案，按解是否正确或最优评估性能，并比较不同圆盘数下的准确率和生成的链式思维长度。Shojaee 等人（2025）据此发现：问题超过少量圆盘后，模型准确率会急剧下降，且推理文本会在任务更难时反常变短；这一现象被称为“illusion of thinking”。
- **把模型失败归因为推理能力或搜索能力不足的外部行为解释**：围绕上述性能坍塌，后续讨论主要根据最终答案和推理轨迹判断模型是否具备可泛化的推理能力。这类解释把模型视为黑箱，关注它是否给出正确计划，却没有直接检查其内部是否形成了汉诺塔配置的可用表征，也未追踪该表征在计划生成期间的变化。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 行为评测只能证明模型“失败了”，不能定位失败机制。原文明确指出：“Despite many follow-ups, the phenomenon has not been explained mechanistically: we know that these models fail, but we do not know what inside the model is failing.” 因而，准确率下降本身无法区分模型从未理解初始局面、理解了但不能将其转成动作、或是在长推理中忘记了局面这几种不同原因。
- 此前重点考察的塔到塔（tower-to-tower）设定对前沿模型已不够有区分度；论文认为其“by now is saturated for frontier models”。相比之下，平铺到平铺（flat-to-flat）允许初始和目标圆盘分散在多个柱上，要求模型处理更一般的中间配置。仅用较容易的设定或最终输出，无法检验模型是否持续维护了规划所需的内部世界状态。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚缺少一个将可控小型 Transformer 与前沿大推理模型联系起来的机制性证据链：在更困难的 flat-to-flat 汉诺塔中，需要先确认模型是否编码了配置状态的“世界模型”，再在推理生成的不同阶段测量该表示是否保持，并通过干预验证表示衰减是否确为错误原因，而非仅与错误相关。

</div>
<div markdown="1"><span>核心问题</span>

对于圆盘数 $N\geq4$ 时 flat-to-flat 汉诺塔的规划失败，大推理模型究竟是没有形成任务状态的内部世界模型，还是已经在提示词结束时形成该模型、却在后续链式思维和动作生成过程中未能维持它；若属后者，恢复该表示能否改善求解表现？

</div>
<div markdown="1"><span>作者直觉</span>

汉诺塔求解不是一次性猜出答案，而是在每一步都依据当前圆盘配置选择合法移动。若模型的隐藏表示能以几何上忠实的方式保存当前配置，那么它原则上拥有规划所需的状态基础；因此，沿生成过程探测这一表示，并把提示阶段仍清晰的表示注入后续推理，可将“模型知道但忘了”与“模型从未知道”区分开来。论文摘要的核心观察正是两种前沿模型“encode the Sierpiński world model near-perfectly at the end of the prompt”，却在多数 $N\geq4$ 任务中失败；这使“表征维护”成为比“表征缺失”更可检验的切入点。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文采用“先在可控小模型中验证表征，再在大推理模型中追踪并干预该表征”的两阶段机制研究路线。任务是平面到平面（flat-to-flat）汉诺塔：给定起始盘面$s_I$与目标盘面$s_G$，模型须输出一串合法且最优的移动；与经典塔到塔任务不同，最优路径依赖具体的$(s_I,s_G)$组合，不能直接套用固定递归模板。作者把全部合法盘面视为图$G$的节点、合法移动视为边；四盘三柱时共有$81$个状态，其图距离$d_G(s,s')$是两个盘面之间最短合法移动数。该状态图可嵌入为谢尔宾斯基三角形，因此可作为“世界模型”是否编码了任务状态及其可达关系的可检验目标。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造符号化规划数据并训练小型生成模型

将每个问题序列化为起始配置、分隔符SEP、目标配置和移动token序列；训练GPT-2式decoder-only Transformer，并只在移动后缀上计算掩码交叉熵。四盘任务的$6,480$个$s_I\ne s_G$有序状态对按$80/20$划分为训练集和验证集。

<div class="method-step__io" markdown="1">

**输入**：四盘汉诺塔的有序起止状态对$(s_I,s_G)$及其符号程序生成的最优移动轨迹。<br>
**输出**：一个从盘面条件生成解法轨迹的小型模型，以及可供逐层、逐token读取的残差流激活。

</div>

**直观理解**：先让规模小、答案可精确生成的模型学习解题，便于研究它内部究竟保存了什么信息。训练时不要求模型复述题目，只要求它根据题目部分预测后面的每一步移动。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在SEP和生成位置探测联合状态几何

对各层残差流训练二维线性距离匹配探针$f_\phi$，使状态嵌入之间的欧氏距离逼近真实状态图距离$d_G$；用Spearman相关、Pearson相关和最近状态检索准确率评价。对大模型，作者在17个层位采样，并将不同时间点的可解码性进行比较。

<div class="method-step__io" markdown="1">

**输入**：小模型在SEP处的隐藏状态$h_s$，以及大模型在三个位置的激活：提示末token的Position A、输出最终移动列表前的Position B、逐个输出移动时的Position C。<br>
**输出**：状态是否以接近谢尔宾斯基三角形的联合几何形式被编码、该编码在网络深度和推理生成过程中的变化曲线。

</div>

**直观理解**：探针相当于一把受限的线性尺子：如果它能把内部向量摆成正确的状态图形，说明模型内部不仅可能记住了若干标签，还保留了盘面之间“相隔多少步”的关系。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 区分联合编码与按盘分解编码

为每个盘$k$训练三分类逻辑探针，其权重矩阵$W_k\in\mathbb{R}^{3\times d}$预测该盘所在柱；再以$W_k$行空间之间的主角度衡量各盘表示子空间的重叠程度。小主角度表示多个盘共用表示维度的统一编码，大主角度表示近似正交的分解编码。

<div class="method-step__io" markdown="1">

**输入**：SEP位置和移动token位置的残差流，以及每个盘所在柱子的监督标签。<br>
**输出**：每个盘位置的可读出准确率，以及状态表示从统一几何格式转向按盘分解格式的证据。

</div>

**直观理解**：联合探针问“整个棋盘像不像正确的地图”，逐盘探针问“每个盘分别在哪里”。两者结合能区分模型是在保持全局规划状态，还是仅保留零散的局部盘位信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 通过激活替换和在线引导检验因果性

在小模型中，将$s_{clean}$的SEP残差流替换到$s_{corrupt}$的前向计算中，并按最终输出与供体、受体或第三状态的关系分类。在大模型中，外部符号跟踪器从已输出的合法移动重放当前盘面$s_t$；在每个生成token的第$\ell$层，向残差流加入指向该盘面提示期激活的归一化方向，并扫描注入强度$\alpha$。

<div class="method-step__io" markdown="1">

**输入**：小模型中干净问题$s_{clean}$与扰动问题$s_{corrupt}$的SEP激活；大模型中每个真实当前盘面$s_t$在Position A的缓存激活$h_{prompt}(s_t)$。<br>
**输出**：小模型中状态转移到输出的因果证据，以及大模型在恢复提示期状态表征后最优求解性能是否提升的干预结果。

</div>

**直观理解**：相关性只能说明“内部表示和答案一起出现”。替换实验直接把一个题目的内部状态塞给另一个题目；在线引导则持续提醒模型当前盘面，从而测试遗忘状态是否正是后续规划失败的重要原因。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 状态空间距离匹配探针目标

$$
\mathcal{L}_{\text{probe}}(\phi)=\frac{1}{|\mathcal{S}|^{2}}\sum_{s,s^{\prime}\in\mathcal{S}}\bigl(\|f_{\phi}(h_{s})-f_{\phi}(h_{s^{\prime}})\|_{2}-d_{G}(s,s^{\prime})\bigr)^{2}
$$

**符号说明**

- $\mathcal{L}_{\text{probe}}(\phi)$：参数为$\phi$的距离匹配探针损失。
- $\phi$：线性探针$f_\phi$的可训练参数。
- $\mathcal{S}$：全部四盘合法配置组成的状态集合，文中大小为$81$。
- $s,s^{\prime}$：状态集合$\mathcal{S}$中的两个盘面配置。
- $h_s$：输入状态为$s$时，在被探测层和token位置提取的模型隐藏状态或残差流向量。
- $f_\phi$：将$d$维隐藏状态映射到二维嵌入空间的线性探针。
- $\|\cdot\|_2$：欧氏范数。
- $d_G(s,s^{\prime})$：汉诺塔状态图$G$中状态$s$与$s^{\prime}$之间的最短合法移动距离。

<div class="equation-explanation" markdown="1">

**直观理解**：该损失遍历所有状态对，要求内部表示映射后的二维距离等于真实盘面之间所需的最短移动数。损失较低并不单独证明模型会使用该地图，因此论文随后以激活替换和引导实验检验其因果作用。<br>
**原文位置**：第4.1节，式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 在线激活引导更新

$$
\tilde{h}^{(\ell)}=h^{(\ell)}+\alpha\cdot\frac{h_{\text{prompt}}(s_{t})-\bar{h}}{\|h_{\text{prompt}}(s_{t})-\bar{h}\|_{2}}
$$

**符号说明**

- $\tilde{h}^{(\ell)}$：在第$\ell$层施加引导后的残差流激活。
- $h^{(\ell)}$：当前生成token在第$\ell$层的原始残差流激活。
- $\ell$：被干预的Transformer层索引；Qwen3.6-27B使用$\ell=28$。
- $\alpha$：引导强度，作者通过扫描多个数值评估其效果。
- $h_{\text{prompt}}(s_t)$：盘面为$s_t$时，在提示结束位置Position A缓存的第$\ell$层激活。
- $s_t$：解码至时刻$t$时由外部符号跟踪器重放得到的当前盘面状态。
- $\bar h$：所有缓存盘面提示期激活的均值。
- $\|h_{\text{prompt}}(s_t)-\bar h\|_2$：中心化提示期状态方向的欧氏长度，用于将方向单位化。

<div class="equation-explanation" markdown="1">

**直观理解**：该式不把完整提示期向量直接覆盖到当前激活，而是沿“当前状态相对平均状态”的单位方向推一步，强度由$\alpha$控制。这样可比较不同干预强度，并避免不同状态向量范数本身决定注入大小。<br>
**原文位置**：第5节“Restoring the world model recovers performance”，式(2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：小型Transformer的生成训练目标是移动token上的掩码交叉熵：题目条件部分只提供上下文，不直接计入预测损失，优化目标是给定$s_I$与$s_G$生成正确的最优移动序列。世界模型探针与原模型分开训练，其目标为式(1)的几何距离拟合，不能反向说明原模型被训练时显式接收过谢尔宾斯基坐标监督。大模型部分不再训练基础模型；探针仅作为诊断读出器，引导实验则在推理时改变中间激活。原文报告小模型在验证集上达到“99.2% token-level and 93.2% sequence-level validation accuracy”（第4节），这说明其已基本学会轨迹生成，因而后续表征分析不是针对明显未学会任务的模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 距离匹配线性探针**

探针$f_\phi:\mathbb{R}^d\to\mathbb{R}^2$读取指定token、指定层的残差流，把每个盘面状态映射到二维。它不以盘面类别正确率为目标，而最小化所有状态对的嵌入欧氏距离与图最短路距离$d_G$之间的平方误差；因此它检验的是全局状态空间的相对几何。作者还报告秩相关、线性相关及最近邻检索，以避免单一指标把单调但尺度失真的嵌入误判为精确几何。

> 直观理解：这是本文识别“世界模型”的核心测量工具。若所有状态在内部表示中的远近关系与真实合法移动步数一致，模型就拥有了可用于规划的状态地图，而非仅仅记住训练答案。

**2. 逐盘探针与主角度分析**

每个盘对应一个预测其三种柱位的逻辑分类器，$W_k$的行空间被定义为该盘的编码子空间。作者计算不同$W_k$行空间的主角度：接近$0^\circ$意味着盘的信息混合在共享方向中，接近$90^\circ$意味着各盘信息由彼此独立的方向承载；该模块与联合距离探针并用，而不是以逐盘准确率替代联合状态评估。

> 直观理解：一个模型即使能分别说出若干盘的大致位置，也未必仍持有适合全局规划的完整盘面。主角度帮助判断它是在使用一张整体地图，还是把地图拆成几张互不协调的小纸条。

**3. 状态跟踪驱动的残差流引导**

作者为每个四盘配置缓存第$\ell$层的Position-A激活，并减去配置激活均值$\bar h$后归一化为控制方向。解码时符号跟踪器检测输出中的“moves = [”块，解析$[disk, from, to]$三元组、从初始状态重放合法前缀，并在盘面变化后把目标方向切换为新的$s_t$；always-steer设置从第一生成token起持续施加该方向。

> 直观理解：该模块把真实盘面作为外部记账本，再把对应的“刚读完题时最清醒的内部状态”不断写回模型。它不是替模型搜索答案，而是测试保持状态本身能否让模型更会规划。

**训练与推理**

训练阶段，作者首先用符号方法预计算四盘flat-to-flat最优解，将状态对与轨迹编码为单个token序列，训练6层小型decoder-only Transformer共50个epoch；然后在每一层、SEP位置及移动位置提取残差流，分别训练联合距离探针和逐盘分类探针。因果验证时，使用验证问题的供体和受体组合，对SEP激活实施整段残差流替换，并按输出是否跟随供体、受体或发生破坏来统计结果。原文称“Substituting a donor’s SEP activation transfers state to the recipient’s output in a large majority of pairs”（第4.3节）；这是作者的因果性主张，严格说检验的是整层SEP残差流而非被二维探针读出的单独子空间。

**复现信息**

大模型推理采用Shojaee et al. (2025)的优化提示，并选择会输出显式$\texttt{<think>}$链的Qwen3.6-27B与DeepSeek-R1-Distill-Qwen-32B；两者均为64层、隐藏维度$5,120$。探针在第1层及从第4层到第64层每隔4层的位置执行，Position A使用$81$个可达配置与固定目标配对；生成结果分为optimal、suboptimal、incorrect和illegal，分别表示最优、合法但过长、合法但未到达目标、以及违反规则或无法解析。在线引导中，Qwen3.6-27B在第28层干预，且仅对未引导时失败的问题施加干预；原文报告在$\alpha=2$时最优解数“from 33 (41%) to 59 (73%)”（第5节，Table 5），证据表明恢复状态表征可改善该模型，但非单调效果也表明$\alpha$过大可能扰乱生成。该流程依赖外部符号状态跟踪器来提供真实$s_t$，所以它是机制验证和性能恢复实验，不是无需任务状态监督的通用部署方案。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 小型模型实验使用预先计算的汉诺塔解轨迹；文段明确说明训练对象是“small Transformers from scratch on precomputed solution traces”。其训练/验证划分与样本总量在所给摘录中未明确报告。状态覆盖汉诺塔合法配置，四盘时状态空间具有谢尔宾斯基三角形结构；激活修补在全部供体—受体验证对上进行。
- 大型推理模型的表征探测在 $N=4$ 的 81 个可达配置上进行，并为 Position A（提示末 token）固定一个目标状态。论文还在 Position B（输出动作列表前的最后 token）和 Position C（每个动作输出 token）探测，但所给摘录未给出这两个位置各自的实例数、目标采样方式或完整结果表。
- 任务比较包括经典 tower-to-tower 与更难的 flat-to-flat。后者的起止状态都可将盘分布在多个柱上，最优路径依赖状态对 $(s_I,s_G)$，因此不能直接套用单塔到单塔的递归模板。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**解答结果类别**

对生成序列分为 optimal（合法、到达目标且最短）、suboptimal（合法、到达目标但过长）以及其他失败类别；摘录仅完整给出了前两类定义。它衡量模型最终规划是否正确，以及正确时是否最优。 （optimal 比例越高越好；suboptimal 或失败比例越低越好，因为它们分别表示效率不足或未完成合法到达目标的规划。）

</div>
<div class="metric-item" markdown="1">

**状态表征探测**

作者在残差流上施加距离匹配探针与逐盘探针，考察隐藏状态能否恢复汉诺塔状态空间的谢尔宾斯基几何及每个盘所在柱。大型模型在 Position A、B、C 的多个层上重复探测，以定位表征何时建立、何时衰减。 （与真实状态空间距离结构或逐盘位置越一致越好；较高的可解码性支持“模型内部保有状态信息”，但单独不能证明该信息被生成过程使用。）

</div>
<div class="metric-item" markdown="1">

**激活修补迁移率**

在受体状态 $s_{\mathrm{corrupt}}$ 的 SEP token 处替换为供体状态 $s_{\mathrm{clean}}$ 的残差激活后，将输出判为 full transfer、partial、unchanged、novel 或 disrupted；partial 同时报告平均被供体解带动的盘数 $K$。该指标检验状态表征的因果作用。 （full 或 partial transfer 越高、disrupted 越低，越说明被替换层的表示能够稳定且因果性地改变输出计划；但 partial transfer 不等同于完整状态控制。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 两个大型推理模型在 flat-to-flat 汉诺塔上的行为结果，问题规模超过三盘。

<div class="result-value" markdown="1">

作者报告：当 $N\geq4$ 时，两模型在多数任务上失败。

</div>

这说明即使任务规模只从三盘增加到四盘，最终生成的规划已不可靠；它并不说明模型完全不具备汉诺塔状态知识，因为后续探测发现提示结束时仍存在高质量状态表征。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Surprisingly, we find that both models encode the Sierpiński world model near-perfectly at the end of the prompt, and yet fail at the majority of tasks when N≥4.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 大型模型在提示结束、思维链完成和动作生成期间的分位置表征探测。

<div class="result-value" markdown="1">

作者将失败定位为世界模型表征在规划阶段衰减，而非该表征从未形成。

</div>

该结果把“会不会表示状态”和“能否在长程生成中保持并调用状态”分开：Position A 的强表征只能证明模型在读完题目后建模成功，不能保证其后续每一步都以该状态为条件。所给摘录未提供各位置、各层的具体探测分数，因而不能据此比较衰减速度或两模型差异大小。

<div class="result-source" markdown="1">

来源：Abstract；§5 Large Reasoning Models

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We locate the source of this failure in the decaying representation of the world model.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 在推理时向大型模型注入提示阶段的状态表征。

<div class="result-value" markdown="1">

作者报告该干预可提升性能，表明丢失后的状态信息至少部分可恢复使用。

</div>

这是比相关性探测更强的证据：若把早期表征注入后结果改善，说明状态维护与失败有因果关联。不过注入的是何层、何种向量、改善幅度、是否对所有任务一致，在给定摘录中均未明确报告；因此不能据此断言该表征是唯一失效原因。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We probe for the representation at different stages during planning, and establish causality by showing that performance can be improved by injecting the prompt-time representation at inference.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 给定摘录未包含大型模型在 Position A/B/C 的完整探测图表、最终成功率表或注入干预的数值结果。因此，“近乎完美”“表征衰减”和“性能改善”目前只能按作者定性表述解读，不能核验效应大小、方差或统计显著性。
- 激活修补替换的是某层 SEP token 的整个残差流，而不是仅替换被探测到的二维世界模型子表示。原文也明确指出该干预并非外科式定位，因此它支持该残差流的因果参与，却不能精确证明谢尔宾斯基几何表示本身是唯一的因果变量。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- tower-to-tower 任务作为结构更规则的任务变体对照，用于区分模型是否只会复用递归式解法，而非根据任意起止状态规划。
- flat-to-flat 任务是本文关键行为基准：它要求追踪完整的初始状态和目标状态，作者用它复现并机制化研究既有“复杂度升高后性能坍塌”的现象。
- 在小型模型因果实验中，未修补的受体输入 $s_{\mathrm{corrupt}}$ 与干净供体输入 $s_{\mathrm{clean}}$ 构成内部对照：输出是否随供体状态改变，用来检验 SEP 残差流是否实际影响规划，而不只是可被探针读取。
- 大型模型比较 Qwen3.6-27B 与 DeepSeek-R1-Distill-Qwen-32B；二者均为 64 层、隐藏维度为 $5120$、会显式生成 `<think>` 链的开放权重推理模型。该比较检验结论是否跨两个不同模型成立，而不是把单一模型行为当作普遍机制。

**实验想回答的问题**

- 小型、从头训练的 Transformer 是否形成了可线性解码、且在因果上参与汉诺塔求解的内部世界模型？
- 推理模型在平铺到平铺（flat-to-flat）汉诺塔上于 $N\geq4$ 时的失效，究竟源于未学到状态模型，还是源于规划生成过程中未能维持该模型？

**实验实现**

小型 Transformer 在预计算解轨迹上从头训练，并对 SEP token 的残差流做线性/几何探测与激活修补。修补时运行受体配置 $s_{\mathrm{corrupt}}$，但用干净运行 $s_{\mathrm{clean}}$ 的 SEP 激活替换；作者在第 4、5、6 层统计所有验证供体—受体对。大型模型采用 Shojaee et al. (2025) 的优化提示词，分析 Qwen3.6-27B 与 DeepSeek-R1-Distill-Qwen-32B；在第 1 层及从第 4 至第 64 层每隔四层的共 17 个层位探测。Position A 是推理前提示末 token，Position B 是完整思维链后、动作列表前的提交点，Position C 是动作生成 token。采样次数、解码参数、置信区间及显著性检验均为原文未明确报告。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 小型 Transformer 的 SEP 激活修补：第 4 层，对全部验证供体—受体配对统计。 | 完整迁移为 $5.75\%$，部分迁移为 $63.89\%$，且平均 $K=1.46$ 个盘随供体解迁移；未改变、novel、disrupted 分别为 $17.56\%$、$0.37\%$、$12.42\%$。 | 该层的大量部分迁移说明 SEP 残差流携带了能影响计划的盘状态信息；但完整迁移很低、仍有 $12.42\%$ 被扰动，意味着第 4 层表示尚未足以干净地替换整个问题状态，也不能将结果归因到一个已被单独定位的二维几何子空间。 | Table 3，§4.3<br><span class="experiment-evidence">4 \| 5.75% \| 63.89% (1.46) \| 17.56% \| 0.37% \| 12.42%</span> |
| 小型 Transformer 的 SEP 激活修补：第 6 层，与第 4 层形成深度对照。 | 完整迁移为 $5.89\%$，部分迁移升至 $78.74\%$，平均 $K=1.44$；disrupted 降为 $0.00\%$，novel 也为 $0.00\%$。 | 相较第 4 层，深层修补几乎不再造成无效输出，且部分迁移更常见，支持后层 SEP 表示更适合稳定地替换状态条件。平均 $K$ 未提升，故这不能证明每个盘的状态都被整体复制；作者据此将作用描述为“causal but graded”。 | Table 3，§4.3<br><span class="experiment-evidence">6 \| 5.89% \| 78.74% (1.44) \| 15.37% \| 0.00% \| 0.00%</span> |

**定性案例**

- 作者把汉诺塔合法状态排列为谢尔宾斯基三角形，并以其作为“几何忠实”的世界模型判据：节点对应盘所在柱的配置，合法移动对应相邻节点。定性上，这避免只凭单盘分类正确便声称模型掌握全局状态；因为联合距离结构可能存在于重叠的几何编码中，而逐盘探针会遗漏这一部分。相关数值图表在所给摘录中不完整，故不能进一步报告该图的定量比较。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It mechanistically analyzes why reasoning models fail Tower of Hanoi planning despite encoding a causal world-model representation.; rule check: matched taxonomy keywords; top rule score=10.0
- 全文指纹：`c9a529228115f6923d7ef40565296010fc56fc16a98869f9d6f28ad049fbbf75`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
