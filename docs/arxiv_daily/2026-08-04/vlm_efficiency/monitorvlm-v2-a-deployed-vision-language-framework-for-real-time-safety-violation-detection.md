---
title: "[论文解读] MonitorVLM-v2: A Deployed Vision-Language Framework for Real-Time Safety Violation Detection"
description: "[arXiv 2608.00975][VLM Efficiency] MonitorVLM-v2旨在把工业监控中开放式、耗时且难以稳定审计的视觉语言推理，压缩为有限安全规则集合上的单步符号决策，并以不确定性分流连接自动判断与人工复核。"
arxiv_id: "2608.00975"
announcement_date: "2026-08-04"
primary_category: "vlm_efficiency"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:02:27.990004+00:00"
source_sha256: "876832f7ffc1c4963f8296e97394d3f2f729ff18cc2bb70e72ceaecc3265ef9d"
tags:
  - "VLM Efficiency"
  - "多模态 VLM"
  - "LLM Reasoning"
  - "视觉语言模型"
  - "工业安全监控"
  - "有限符号决策空间"
  - "规则级违规检测"
  - "多路视频监控"
  - "低延迟推理"
  - "人机协同审核"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Efficiency · arXiv 2608.00975</p>

# MonitorVLM-v2: A Deployed Vision-Language Framework for Real-Time Safety Violation Detection

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Jiang Wu, Sichao Wu, Yinsong Ma, Lifang Zheng, Jingliang Duan</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> School of Mechanical Engineering, University of Science and Technology Beijing；The Laboratory for Computational Sensing and Robotics, Johns Hopkins University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.00975v1) · [PDF 下载](https://arxiv.org/pdf/2608.00975v1) · **关键词** 视觉语言模型, 工业安全监控, 有限符号决策空间, 规则级违规检测, 多路视频监控, 低延迟推理, 人机协同审核<br>


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

MonitorVLM-v2旨在把工业监控中开放式、耗时且难以稳定审计的视觉语言推理，压缩为有限安全规则集合上的单步符号决策，并以不确定性分流连接自动判断与人工复核。

**不用术语来说**：工业现场往往同时接入多路摄像头，系统不仅要看见人员、装备和动作，还要立即判断画面是否违反某一条具体安全规定。逐段依靠人工检查容易覆盖不足；让通用视觉语言模型逐句生成分析又太慢，而且答案格式和长度不固定，难以直接接入需要及时告警、明确责任和事后审计的生产流程。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出“推理到决策压缩”范式：将时间视觉片段直接映射为有限规则空间中的单个规则编号，使在线输出不再依赖自然语言推理链长度，并通过训练阶段的规则—符号随机重排抑制对固定编号的机械记忆。
- 针对压缩后的符号决策提出SymPO与熵引导分流：SymPO在提高正确规则概率的同时显式压低竞争规则；部署时则依据预测熵，将明确案例交由人工确认Top-1结果，将模糊案例升级为Top-3候选供专家审查。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于面向工业安全监控的视觉语言模型（VLM）研究。其目标不是一般性的图像描述或开放问答，而是持续分析多路监控视频，并依据预先定义的安全规程输出可供处置和审计的规则级判断。传统目标检测器与动作识别器能够发现人员、防护装备、设备和动作，却难以仅凭这些局部证据判定某项操作规程是否被违反；CLIP一类图文模型可计算视觉与文本的语义相似度，但其分数并不直接对应结构化的监管结论。具备思维链推理能力的VLM原则上可以综合场景关系，但其输出长度不固定，推理延迟随生成词元数与并发视频流数量共同增长，因而不适合要求低延迟、稳定吞吐和明确责任追溯的工业部署。本文据此将任务建模为有限监管空间上的概率分类：模型只需从“无违规”和各条规程对应的规则ID中选择一个符号，而不必在线生成完整的自然语言推理过程。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉语言模型（VLM）**

同时处理图像或视频与文本信息的模型，可依据视觉证据理解文本描述、回答问题或作出判断。本文向模型提供时序图像片段及安全规程，使其判断画面对应哪一种规则级结果。

</div>
<div class="concept-item" markdown="1">

**自回归思维链（CoT）**

模型逐词元生成中间推理步骤，再生成最终答案；后一个词元依赖此前已生成的内容。其推理表达能力较强，但输出长度可变，生成成本约随词元数$T$增长，在多路视频并发时容易形成吞吐瓶颈。

</div>
<div class="concept-item" markdown="1">

**有限符号决策空间**

把所有允许输出限制为预先定义的离散符号集合，例如“无违规”及每条安全规程对应的规则ID。这样可将开放文本生成改为单步类别选择，使输出更确定、更易被下游系统解释和审计。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

设操作安全规程集合为$\mathcal{R}=\{r_1,\ldots,r_K\}$，相应的符号决策空间为$\mathcal{Y}=\{y_0,y_1,\ldots,y_K\}$：$y_0$表示未违规，$y_k$表示与规程$r_k$关联的违规结果。模型输入由三帧构成的时序视觉片段$I=\{I_1,I_2,I_3\}$以及当前监管上下文$\mathcal{R}$，输出有限集合$\mathcal{Y}$上的条件概率分布$\pi_\theta(y\mid I,\mathcal{R})$，最终以单步最大概率选择得到规则ID。问题场景是假定规程集合已由组织预先定义，并要求系统在低质量工业画面、连续多路视频和低延迟约束下运行；预测仍由人审核，其中不确定性较低的样本提交Top-1结果确认，不确定性较高的样本提交Top-3候选供专家检查。训练时规则与输出词元的映射可被周期性打乱，以减少模型死记固定编号；部署时该映射固定，保证规则ID具有唯一、确定的业务含义。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{R}=\{r_1,\ldots,r_K\}$**

由$K$条预定义操作安全规程组成的有限集合，其中$r_k$表示第$k$条规程。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{Y}=\{y_0,y_1,\ldots,y_K\}$**

有限符号决策空间；$y_0$为无违规类别，$y_k$对应规程$r_k$的规则级结果。

</div>
<div class="notation-item" markdown="1">

**$I=\{I_1,I_2,I_3\}$**

送入模型的时序视觉片段，由三个时刻的图像帧组成。

</div>
<div class="notation-item" markdown="1">

**$\pi_\theta(y\mid I,\mathcal{R})$**

参数为$\theta$的模型在视觉片段$I$和监管上下文$\mathcal{R}$条件下，对符号结果$y$给出的预测概率。

</div>

</div>

**直接相关的工作**

- **目标检测器与动作识别器**: 这类方法可定位人员、设备、防护装备和预定义动作，为监控提供对象级或动作级证据；但实体或动作的出现本身不能确定是否违反了包含条件、关系和程序要求的安全规程，因此其输出粒度与本文要求的规则级决策不一致。
- **CLIP类图像—文本匹配模型**: 这类模型将视觉与语言映射到共享表示空间，并以相似度衡量画面与文本描述的匹配程度；然而相似度分数不是有限监管假设上的直接决策接口，难以单独满足确定输出、规则映射和审计追踪要求。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

地下矿山等安全关键场景需要连续处理多路低质量视频，并把每个片段及时转换为可执行、可追责的规则级结论。实际需求不是生成一段看似合理的场景描述，而是在预定义法规集合中判断“未违规”或“违反哪一条规则”，同时保持低延迟、稳定吞吐和完整人工可审计性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **目标检测与动作识别**：从视频中定位人员、设备和防护用品，或识别预先定义的动作，为安全判断提供对象与行为层面的局部证据。
- **图文匹配与开放式视觉语言推理**：CLIP类模型通过视觉与文本表示的相似度衡量画面和描述是否匹配；带思维链提示的视觉语言模型则自回归生成多步文字分析，再给出安全结论。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 目标检测、动作识别和图文相似度主要给出对象、动作或语义对应关系，不能直接表达结构化法规假设之间的排他性选择；因此，识别到安全帽、人员或某个动作，并不等于已经证明某条操作规程被违反。
- 思维链视觉语言模型需要生成长度可变的文本，推理成本会随生成令牌数$T$和并发视频流数量共同增长；这会形成多流实时处理的吞吐瓶颈，而且自由文本输出也弱化了确定性控制、统一解析和审计接口。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种经过真实长期运行验证的统一框架：它既能把复杂时序视觉证据直接落到有限、明确的法规决策空间，又能在多摄像头条件下维持可预测的单步解码；同时还应区分可信与模糊判断，把有限专家注意力集中到真正不确定的案例上。

</div>
<div markdown="1"><span>核心问题</span>

能否将视觉语言模型对工业场景的多步开放式推理，压缩为有限规则编号集合上的快速、校准且可审计的概率推断，并通过专门的符号空间优化和不确定性分流，使该机制能够支持真实工业现场的连续多流监控？

</div>
<div markdown="1"><span>作者直觉</span>

工业法规本身已经限定了答案范围，因此模型没有必要在每次判断时重新生成完整解释，只需比较“未违规”和各条违规规则哪个最符合视觉证据。把概率集中到正确规则、主动压低容易混淆的竞争规则，可以让边界更清楚；当分布仍然分散时，用熵识别这种犹豫并展示少量候选给专家，便能以较小人工成本保留最终监督权。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

MonitorVLM-v2把工业安全监控从开放式文本生成改写为有限类别上的条件概率推断。输入是一个三秒观察窗口中抽取的三帧图像$I=\{I_1,I_2,I_3\}$以及当前生效的安全规则表$\mathcal{R}$；模型不生成自然语言思维链，而只在包含35条违规规则和1个“无违规”类别的符号空间$\mathcal{Y}=\{y_0,y_1,\ldots,y_K\}$中输出一个规则ID。训练首先通过带规则令牌重排的监督微调学习视觉证据、规则语义和符号之间的对应关系，再通过符号策略优化SymPO压低错误候选的概率；部署时则根据输出分布的香农熵决定采用Top-1确认还是Top-3专家复核，并把人工纠正的困难样本写入反馈缓冲区。

直观地说，该方法把“观看视频后写一篇分析报告”压缩成“从有限规则清单中勾选一项”。这种设计牺牲了在线生成完整解释文本的能力，换取固定、可审计且近似常数长度的输出；但系统并未让模型独立形成最终执法结论，低不确定性和高不确定性预测都要经过人工确认。部署管线还先用轻量人员检测器过滤空画面，使较昂贵的视觉语言模型只处理确实出现人员、可能涉及安全行为的片段。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 人员哨兵筛选与片段构造

YOLO-v11人员哨兵以$1\,\mathrm{fps}$检查视频帧，丢弃未检测到人员的画面；对包含人员的事件，在三秒观察窗口内抽取三帧，构成$I=\{I_1,I_2,I_3\}$。

<div class="method-step__io" markdown="1">

**输入**：来自多路固定摄像机的连续视频流。<br>
**输出**：送往规则推断器的三帧人员活动片段。

</div>

**直观理解**：先用较便宜的检测器判断“画面里有没有人”，再让较昂贵的模型判断“这个人在做什么、是否违反哪条规则”。这样可以减少无人员画面对计算资源的占用。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 规则表条件化与单令牌预测

视觉语言模型计算$\pi_\theta(y\mid I,\mathcal{R})$，logit掩码将候选限制在有效符号集合$\mathcal{Y}$内；模型随后输出一个规则ID令牌，而不是自回归生成最长可达8192个令牌的推理文本。

<div class="method-step__io" markdown="1">

**输入**：三帧片段$I$、安全规则集合$\mathcal{R}$以及部署时固定的规则到令牌映射$\phi$。<br>
**输出**：36个有效类别上的概率分布及其Top-1规则ID，其中$y_0$表示无违规，$y_1$至$y_{35}$对应具体安全规则。

</div>

**直观理解**：模型只能在预先批准的规则清单里作答，不能生成清单之外的自由文本。输出长度固定为一个令牌，因此延迟更稳定，结果也能直接映射到具体规章。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 熵驱动的双路径人工复核

系统计算香农熵$H(I,\mathcal{R})$：当$H<\tau$时进入Top-1确认路径，当$H\geq\tau$时向专家展示紧凑的Top-3候选；部署采用$\tau=10^{-3}$，而阈值本身由验证集网格搜索确定。

<div class="method-step__io" markdown="1">

**输入**：符号输出分布$\pi_\theta(\cdot\mid I,\mathcal{R})$及其不确定性阈值$\tau$。<br>
**输出**：供人工确认的单个规则候选或三个候选，以及人工核验后的最终记录。

</div>

**直观理解**：概率集中时，审核员只需确认模型最有把握的一项；概率分散时，系统把三个较可能的规则同时交给专家比较。熵在这里相当于“模型犹豫程度”，但不是具有统计覆盖保证的置信区间。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 审核闭环与困难样本回流

系统将已核实的违规和人工纠正的假阳性写入困难样本缓冲区，并在后续适配轮次中重新纳入训练，以针对现场特有的视觉条件更新模型。

<div class="method-step__io" markdown="1">

**输入**：人工确认的违规事件、被纠正的误报以及对应视频片段。<br>
**输出**：可用于后续域适配的规则ID标注样本，以及具备完整人工审核轨迹的事件记录。

</div>

**直观理解**：系统把实际运行中最容易出错的案例留下来，下一轮训练优先学习这些案例。由于答案始终来自有限规则ID，现场人员无需重新撰写长篇思维链标注。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 有限规则空间上的条件预测

$$
\mathcal{Y}=\{y_0,y_1,\ldots,y_K\},\quad K=35,\qquad \pi_\theta(y\mid I,\mathcal{R}),\quad y\in\mathcal{Y}
$$

**符号说明**

- $\mathcal{Y}$：模型允许输出的有限符号决策空间。
- $y_0$：无违规类别对应的符号令牌。
- $y_1,\ldots,y_K$：分别对应具体安全规章的规则ID令牌。
- $K$：安全规章数量，本文取35；连同无违规类共有36个候选类别。
- $I=\{I_1,I_2,I_3\}$：从三秒观察窗口中抽取的三帧视觉输入。
- $\mathcal{R}$：当前提供给模型的安全规章集合或规则表。
- $\pi_\theta(y\mid I,\mathcal{R})$：参数为θ的模型在给定视觉片段与规则表时，对规则ID y赋予的条件概率。

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定了任务边界：模型只需在36个合法答案中分配概率并选择一个，而不需要逐词生成开放式解释。logit掩码进一步保证无效词元在决策时不可被选中，这使输出可直接进入规则数据库和审核界面。<br>
**原文位置**：Methods，Discrete symbolic mapping and vocabulary construction

</div>

</div>

<div class="equation-block" markdown="1">

#### 符号分布的香农熵与路由规则

$$
H(I,\mathcal{R})=-\sum_{y\in\mathcal{Y}}\pi_\theta(y\mid I,\mathcal{R})\log \pi_\theta(y\mid I,\mathcal{R}),\qquad \begin{cases}H(I,\mathcal{R})<\tau & \text{Top-1 confirmation},\\ H(I,\mathcal{R})\geq\tau & \text{Top-3 expert review}.\end{cases}
$$

**符号说明**

- $H(I,\mathcal{R})$：给定视觉片段和规则表时，符号预测分布的香农熵，即系统采用的不确定性分数。
- $\pi_\theta(y\mid I,\mathcal{R})$：规则ID y的预测概率。
- $\mathcal{Y}$：所有合法规则ID和无违规类别组成的集合。
- $\tau$：由验证集网格搜索选择的路由阈值，部署时设为10的负3次方。

<div class="equation-explanation" markdown="1">

**直观理解**：当概率几乎集中在一个规则上时，熵较低，审核界面只展示Top-1答案；当多个规则概率接近时，熵较高，界面展示Top-3供专家判断。原文明确采用香农熵，但所给正文只写出$H(I,\mathcal{R})$及阈值规则；这里展开的是该术语的标准定义，不应误解为论文提出了新的熵公式。<br>
**原文位置**：Methods，Entropy-based triage calibration；Results，Entropy-guided triage identifies ambiguous failure modes

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练目标分为两个层次。Stage 1以交叉熵最大化真实规则ID的条件似然，形式上可理解为最小化真实标签$y^*$的负对数概率$-\log\pi_\theta(y^*\mid I,\mathcal{R})$；同时，每个epoch重排映射$\phi$，使优化不能依赖固定的令牌编号，而必须结合视觉证据和当轮规则语义。Stage 2从该SFT检查点继续进行SymPO：每个提示从有限空间中采样一个规则ID，正确采样的奖励为$+1$，错误采样的奖励为$-1$，目标意图是同时强化真实假设并压制具有视觉迷惑性的竞争规则。

需要区分论文明确给出的设计与可复现信息的缺口：所给Methods明确说明了样本数和绝对对比奖励，但没有给出SymPO最终标量损失的完整数学表达，也没有说明是否包含参考策略KL约束、重要性采样比率或裁剪机制。因此可以确认其优化方向和采样成本，不能从节选中推断具体梯度估计公式；严格复现还需核对作者公开代码及论文未截取的算法定义。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 有限符号空间与规则令牌重排**

模型以规则到符号的映射$\phi:\mathcal{R}\rightarrow\mathcal{Y}$连接规章语义与输出令牌。训练时在每个epoch开始重新排列$\phi$，但保持图像片段与真实规章语义的配对不变；部署时再固定为确定性字典，并通过logit掩码禁止生成无效令牌。

> 直观理解：若某条规则永远对应同一个令牌，模型可能只记住标签编号，而没有真正利用规则内容。周期性换号迫使它先理解当前规则表中的语义，再选择该轮对应的符号；上线后固定字典则保证同一ID始终有唯一含义。

**2. 两阶段SFT与SymPO优化**

第一阶段在规则令牌重排数据上使用交叉熵进行监督微调，使模型学会从三帧视觉输入和当前规则表预测真实规则ID。第二阶段从SFT检查点初始化SymPO，每个提示仅采样一个符号：命中真实规则ID获得$+1$绝对奖励，任一错误规则ID获得$-1$奖励；与每个提示采样$G=8$次的GRPO和DAPO相比，论文报告其实现中的单步rollout成本降低87.5%。原文没有在所给章节中给出SymPO完整的可微损失、策略比率、裁剪项或正则项公式，因此不能仅凭奖励描述复原其全部优化目标。

> 直观理解：SFT主要是提高正确答案的概率，但相似违规规则仍可能同时得到较高分；SymPO进一步奖励正确选择并惩罚竞争选项，用来拉开相邻规则的决策边界。单提示只采一个答案也减少了强化学习阶段反复生成候选的开销。

**3. 不确定性路由与人工审计**

系统把有限类别分布的香农熵作为路由信号，并在验证集上搜索阈值$\tau$以权衡专家复核量和预期召回率。无论进入低熵Top-1路径还是高熵Top-3路径，每个预测都必须由人确认后才能写入记录，因此模型负责筛选和排序，人工承担最终判断与责任。

> 直观理解：该模块不是简单地把所有报警都交给人，也不是允许模型自动定案，而是按困难程度分配审核注意力。容易案例缩短确认流程，模糊案例提供多个候选，既保留吞吐量，也留下完整的人工审核链。

**训练与推理**

训练阶段先为35条规章及无违规类建立有限符号词表，并构造三帧片段、规章语义和真实规则ID配对。Stage 1在每个epoch开始随机重排规则到令牌的映射$\phi$，使用交叉熵进行两轮SFT；该过程训练模型根据当前规则表完成条件映射，而非记忆固定标签位置。随后选择Qwen3-2B-basic的SFT检查点进入Stage 2，运行一轮SymPO，每个提示只产生一个符号样本并根据是否命中真实规则ID获得$+1$或$-1$奖励。训练结束后固定$\phi$，从而形成可供下游系统稳定解释的规则ID字典。

推理阶段，YOLO-v11先以$1\,\mathrm{fps}$筛除无人画面；对包含人员的三秒片段抽取三帧，MonitorVLM-v2在logit掩码约束下计算36类分布并单步输出规则ID。系统再计算$H(I,\mathcal{R})$：低于阈值的事件交由人员确认Top-1，高于或等于阈值的事件展示Top-3候选。所有预测均须人工确认，不存在自主最终裁决；已确认违规和被纠正的误报进入困难样本缓冲区，供后续现场适配使用。该流程的关键收益来自把输出长度相关的解码复杂度由$O(T)$压缩为$O(1)$，其中$T$是自然语言推理序列长度，但视觉编码和模型前向计算本身并未因此消失。

**复现信息**

公平解释和复现所需的核心设置如下：实验使用8张NVIDIA A40 GPU、DeepSpeed ZeRO-3和BF16。SFT训练2个epoch，单设备批量为1，通过梯度累积得到总有效批量16，学习率为$1\times10^{-4}$并采用余弦衰减；最大序列长度为8192，LoRA秩$r=16$、缩放参数$\alpha=32$。SymPO从SFT检查点训练1个epoch，单设备批量为4、梯度累积为1、学习率为$1\times10^{-6}$，符号采样温度为0.7；原文节选在“top-$p$”处截断，故其具体取值原文未明确报告，不能补写。

部署侧必须保留三项条件才能公平理解系统：输入单位是三秒窗口中的三帧，而非完整长视频；人员哨兵承担前置计算过滤；最终事件必须经人工确认。高熵路由阈值$\tau=10^{-3}$是在验证集网格搜索后用于部署的操作点，并非由理论保证推导。SymPO源码地址由Code availability报告为https://github.com/JiangWu0826/ms-swift.git，但代码版本、提交哈希以及与论文实验完全对应的配置在所给节选中未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 领域训练集来自目标地下矿山的固定高清监控视频，包含 $8002$ 个违规事件和 $5077$ 个非违规事件，覆盖 $35$ 条安全法规。其作用是完成规则编号任务上的领域监督微调；违规片段由现场受训安全检查员依据对应法规核验，并标注精确规则编号。
- 留出测试集包含 $862$ 个事件，其中 $732$ 个违规、$130$ 个非违规。该集合用于统一比较专有模型、开源原始检查点、领域微调模型及不同强化学习目标；所有方法都按严格规则编号协议评分，非违规也作为一个类别。
- 前瞻性部署在一座实际运营的地下矿山进行，持续四个月并同时处理 $10$ 路摄像头视频。该部署用于检验完整系统在真实持续监控条件下的吞吐能力和违规发现效果，而不是只测离线分类性能。原文摘要报告其相对于现场常规人工巡检发现了 $2.78$ 倍的已确认违规，但所给章节未提供事件总数、人工复核流程细节或统计置信区间。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**精确规则编号准确率**

只有预测法规与真实法规完全一致时才计为正确，非违规也作为独立类别；该指标防止把相近法规之间的错分误算为成功。 （越高越好，因为它表示系统对整个有限法规决策空间的精确分类更可靠。）

</div>
<div class="metric-item" markdown="1">

**召回率**

衡量真实违规中被系统检出的比例，直接反映漏检风险；在安全监控中，假阴性通常比额外人工复核更危险。 （越高越好，因为更高召回率意味着遗漏的真实违规更少。）

</div>
<div class="metric-item" markdown="1">

**F1 分数**

精确率与召回率的调和平均，用于概括发现更多违规与控制误报之间的平衡。 （越高越好，因为只有精确率和召回率同时较好时，F1 才会较高。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 链式思维推理压缩与在线延迟

<div class="result-value" markdown="1">

带 RTS 的单步规则编号监督相对完整链式思维监督，四个骨干的平均准确率仅下降 $4.66$ 个百分点；三帧片段的在线解码时间由 $3.82$–$6.41$ 秒降至 $0.15$–$0.39$ 秒，即缩短 $19.45$ 倍并进入亚秒级。

</div>

作者据此主张，有限法规空间中的大部分判别能力可以压缩到单词元输出中，而无需在线生成长推理文本。通俗地说，模型在训练时吸收视觉与法规之间的关系，部署时只输出规则编号，因此速度大幅提高。该结果证明的是同一任务协议下的速度—准确率折中，并不证明隐式推理与完整自然语言推理在开放问题上等价；准确率仍有约 $4.66$ 个百分点损失。

<div class="result-source" markdown="1">

来源：Results，推理压缩实验，Fig. 4c（HTML 摘录中图号显示存在偏移）

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Replacing autoregressive CoT generation with bounded rule-ID prediction reduces online decoding time by 19.45-fold (from 3.82-6.41 s to 0.15-0.39 s per three-frame segment), enabling subsecond throughput and satisfying the real-time requirement of multistream deployment.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 严格规则编号测试集上的最终模型比较

<div class="result-value" markdown="1">

MonitorVLM-v2 在 $862$ 个测试事件上取得准确率 $69.84\%\pm2.07$、召回率 $74.73\%\pm3.22$ 和 F1 $80.80\%\pm2.28$；相比第一阶段 Qwen3-2B-basic 的召回率 $58.14\%\pm3.12$，召回提高 $16.59$ 个百分点，但精确率由 $93.32\%\pm2.20$ 降至 $87.94\%\pm2.31$。

</div>

结果表明 SymPO 后的模型找回了更多真实违规，并在准确率和 F1 上超过所列微调开源基线以及零样本专有模型。精确率下降说明这一提升并非所有维度同时改善，而是安全导向的取舍：接受更多误报来减少漏检。由于专有模型没有接受领域微调，跨组比较只能说明部署协议下的实际表现，不能单独证明 SymPO 在同等训练数据和算力条件下优于这些专有模型。

<div class="result-source" markdown="1">

来源：Results，Two-stage optimization sharpens decision boundaries；Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This improvement was driven primarily by a substantial increase in recall, from 58.14% for the SFT backbone to 74.73% for MonitorVLM-v2, indicating that more true violations were successfully recovered under the strict rule-ID protocol.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 四个月、$10$ 路摄像头的实际矿区前瞻性部署

<div class="result-value" markdown="1">

完整系统在实际地下矿山连续部署四个月，处理 $10$ 路并发视频；作者报告推理速度提高 $19.45$ 倍，并发现了现场常规人工巡检流程所确认违规数量的 $2.78$ 倍。

</div>

这项结果表明，低延迟符号预测和人工分流能够在真实持续监控中产生额外的已确认违规发现，而不仅是改善离线分数。不过，$2.78$ 倍比较的是该现场现有人工巡检工作流，不等同于对所有人工检查员的受控替代实验；所给材料也未披露绝对违规数、工作时长匹配方式及可能的时间或摄像头覆盖差异，因此不能据此推断系统将普遍提升事故预防效果。

<div class="result-source" markdown="1">

来源：Abstract；Results 开头亦说明四个月、$10$ 路视频的完整管线评估

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In a four-month prospective deployment across 10 concurrent camera feeds in an operational underground mining facility, MonitorVLM-v2 achieved a 19.45-fold increase in inference speed and identified 2.78 times as many confirmed violations as the site's routine manual inspection workflow, demonstrating the practical value of compressed symbolic decision-making for real-time, auditable industrial monitoring.

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

- 零样本专有多模态模型 Claude Sonnet 4.6、GPT-5.2 和 Gemini-3-Flash：通过官方 API、未经矿山领域微调进行评估，用来判断通用闭源模型仅凭提示能否完成精确法规映射。作者明确说明它们是诊断性零样本基线，不应用于证明领域适配模型与闭源模型之间的完全公平优越性。
- 零样本开源原始检查点 InternVL3-2B-Instruct、LLaVA-OneVision-0.5B、Gemma-3-4B 和 Qwen3-VL-2B-Instruct：使用相同规则编号提示但不做领域训练，用于测量预训练视觉语言能力直接迁移到矿山法规任务时的水平。
- 四个领域监督微调基线 InternVL3-2B-basic、LLaVA-0.5B-basic、Gemma-4B-basic 和 Qwen3-2B-basic：均在 RTS 领域数据上完成第一阶段监督微调，用于比较不同骨干的领域适配能力，并确定后续策略优化所采用的 Qwen3-2B-basic。
- Qwen3-2B-basic 加 GRPO 或 DAPO：二者与 SymPO 从同一监督微调检查点出发，属于组式强化学习目标对照，用于隔离性能提升是否来自一般性的强化学习阶段，还是来自 SymPO 对竞争规则假设的显式抑制。

**实验想回答的问题**

- 在严格的规则编号判定任务中，能否把最长达 $8192$ 个词元的在线链式思维生成压缩为单步规则编号预测，同时保留足够的法规区分能力并满足多路实时监控的延迟要求？
- 在完成领域监督微调后，SymPO 是否比常规监督微调及 GRPO、DAPO 更能分离相近违规类别；预测熵又能否识别剩余的困难样本，从而支持人工复核与实际矿区部署？

**实验实现**

评估采用分阶段设计：先在相同骨干上比较完整链式思维监督、固定规则编号监督以及带 RTS 的规则编号监督，再选择表现最好的 Qwen3-2B-basic 检查点，对比 GRPO、DAPO 与 SymPO，随后分析词元概率、错误类别和预测熵，最后开展真实矿区前瞻性部署。RTS 会在每个训练轮次开始时重新排列“法规到输出词元”的映射，以减少模型记忆固定词元索引的捷径。测试阶段在 $n=862$ 的留出集上执行严格规则编号匹配；表 1 的 $95\%$ 置信区间通过 $1000$ 次 bootstrap 重采样估计。延迟按三帧片段的端到端推理时间报告。熵分流在阈值 $\tau=10^{-3}$ 下，将低熵样本送入 Top-1 自动确认路径，将高熵样本的 Top-3 候选交由专家复核。所给章节未明确报告硬件型号、视频采样频率、各模型解码参数或统计显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 固定规则编号映射与带 RTS 的动态映射 | 带 RTS 的规则编号监督在四个骨干上持续优于固定映射；其中 Qwen3-2B-basic 在带 RTS 条件下达到 $60.21\%$ 准确率，并比 LLaVA-0.5B-basic 高 $18.45$ 个百分点。 | 该消融隔离了“单词元输出是否会让模型记住固定词元索引”这一问题。固定映射允许模型把某个输出词元与训练类别机械绑定；每轮重排映射后，模型必须结合当前规则表、图像和法规语义才能选择词元。结果支持 RTS 能削弱固定索引捷径，但不同骨干之间的 $18.45$ 个百分点差异还混合了模型容量和架构影响，不能全部归因于 RTS。 | Results，Reasoning compression preserves regulatory discrimination；Table 1<br><span class="experiment-evidence">Among the evaluated backbones, Qwen3-2B-basic achieved the highest accuracy of 60.21% under rule-ID with RTS, exceeding LLaVA-0.5B-basic by 18.45 percentage points, and was selected as the backbone for subsequent policy optimization (Table 1).</span> |
| 相同 Qwen3-2B-basic SFT 起点上的 GRPO、DAPO 与 SymPO | SymPO 收敛到 $69.84\%$ 准确率，高于 GRPO 的 $65.20\%$ 和 DAPO 的 $65.22\%$，分别提高 $4.64$ 和 $4.62$ 个百分点；词元概率分析显示，SymPO 对误分类样本的高置信竞争规则编号抑制更明显。 | 该对照控制了骨干和第一阶段监督微调起点，因而较直接地检验第二阶段优化目标。数值和概率分布共同支持 SymPO 比两个组式目标更适合有限规则空间的边界分离。它仍不能排除超参数敏感性，因为所给章节未报告多随机种子结果，也未说明三种强化学习方法是否获得完全等量的调参预算。 | Results，Two-stage optimization dynamics and token-level probability analysis，Fig. 6a；Table 1<br><span class="experiment-evidence">SymPO converges to 69.84%, surpassing GRPO (65.20%) and DAPO (65.22%).</span> |

**定性案例**

- 定性错误分析将失败归纳为低照度、强光与眩光、严重遮挡、拍摄距离过远、群体场景中的注意力分散以及细微动作差异。Grad-CAM 显示，正确样本的高激活区域通常对准任务相关位置，而失败样本的注意力较分散或偏离关键区域。这为“残余错误主要来自感知歧义”提供了可视化线索，也说明删除文本链式思维后仍可从视觉编码器的最终交叉注意力获得空间解释；但注意力图只是相关性诊断，不能证明模型的因果推理过程。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Compresses autoregressive VLM reasoning into single-token symbolic decisions for efficient real-time visual safety monitoring.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`876832f7ffc1c4963f8296e97394d3f2f729ff18cc2bb70e72ceaecc3265ef9d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
