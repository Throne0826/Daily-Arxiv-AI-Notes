---
title: "[论文解读] Glance, Scrutinize, and Think: Advancing Video Anomaly Detection from Training-Free to Agentic Reasoning"
description: "[arXiv 2608.11260][VLM Reasoning] 本文针对视频异常检测中“能定位但不理解”与“能解释但定位不准”的能力割裂，探索统一的全局到局部推理范式，并分别提出无需训练的粗到细框架与可学习调用视频裁剪工具的智能体方法。"
arxiv_id: "2608.11260"
announcement_date: "2026-08-13"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-13T02:56:35.940188+00:00"
source_sha256: "ba30a23a4cbe6d9ca710c498a7cd2dace77a64aee876e8ac86a42a42a46a351a"
tags:
  - "VLM Reasoning"
  - "LLM Agent"
  - "LLM 其他"
  - "LLM Reasoning"
  - "视频异常检测"
  - "异常语义理解"
  - "时间定位"
  - "全局到局部推理"
  - "训练无关框架"
  - "工具增强推理"
  - "智能体强化学习"
  - "多模态大语言模型"
  - "VAGU-T"
  - "JeAUG"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.11260</p>

# Glance, Scrutinize, and Think: Advancing Video Anomaly Detection from Training-Free to Agentic Reasoning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-13</span>
<span><strong>作者</strong> Shibo Gao, Peipei Yang, Xu-Yao Zhang, Linlin Huang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Jiaotong University, Beijing 100044, China；Institute of Automation, Chinese Academy of Sciences, Beijing；State Key Laboratory of Multimodal Artificial Intelligence；Systems, Institute of Automation, Chinese Academy of Sciences</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.11260v1) · [PDF 下载](https://arxiv.org/pdf/2608.11260v1) · **关键词** 视频异常检测, 异常语义理解, 时间定位, 全局到局部推理, 训练无关框架, 工具增强推理, 智能体强化学习, 多模态大语言模型, VAGU-T, JeAUG<br>


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

本文针对视频异常检测中“能定位但不理解”与“能解释但定位不准”的能力割裂，探索统一的全局到局部推理范式，并分别提出无需训练的粗到细框架与可学习调用视频裁剪工具的智能体方法。

**不用术语来说**：实际监控系统不仅要判断视频里发生了什么异常，还要准确指出异常从何时开始、到何时结束，并尽快给出结果。例如，系统不能只回答“发生了交通事故”，也不能只标出一段可疑时间而不说明原因。现有方法通常只能做好其中一项；若逐帧或逐片段仔细分析，又会产生过高计算成本，难以满足实时监控需求。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将训练自由的 GtS 与经过训练的工具增强智能体置于同一“先全局浏览、再局部审查、必要时修正”的框架下：前者用静态和动态文本引导完成粗定位、异常解释与边界细化，后者通过冷启动监督微调和强化学习，学会自主裁剪可疑片段、密集复查并纠正错误定位。
- 作者扩展得到 VAGU-T 数据套件，并提出 JeAUG 评价指标：前者统一提供异常类别、语义解释、时间定位、问答及工具调用推理轨迹，后者联合考察语义解释质量与时间定位精度，从而支撑上述统一能力的训练和评价。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

视频异常检测（Video Anomaly Detection，VAD）面向监控、工业自动化和智能交通等场景，目标是从视频中发现偏离正常行为或具有安全风险的事件。本文关注比传统异常检测更完整的任务：系统不仅要定位异常发生的起止时间，即回答“何时发生”，还要用自然语言说明异常内容，即回答“发生了什么”。现有技术主要分为两类：传统深度神经网络通常擅长输出时间位置，却缺少开放语义解释能力；基于大语言模型或视觉语言模型的方法能够描述事件，但往往不能精确确定异常边界。本文因此把时间定位与语义理解视为同一推理过程中的两个相互约束目标。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**时间定位（Temporal Grounding）**

时间定位是从完整视频中确定目标事件的开始时刻和结束时刻。对异常检测而言，它要求模型不仅判断视频是否异常，还要指出异常具体出现在哪一段。

</div>
<div class="concept-item" markdown="1">

**多模态大语言模型（MLLM）**

多模态大语言模型能够同时处理视频帧等视觉信息与文本指令，并生成自然语言回答。本文进一步让模型调用视频裁剪工具，以便重新观察可疑时间段。

</div>
<div class="concept-item" markdown="1">

**训练无关与智能体式推理**

训练无关方法直接组合冻结的现成模型，无需针对目标数据重新更新参数；智能体式方法则训练模型自主选择和调用工具，并根据新增观察修正先前判断。两者分别对应低部署门槛与更强的任务适应能力。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一段可能较长的真实场景视频，其中可能包含犯罪行为、自然灾害、动物致伤或交通事故等异常事件。系统需要联合输出异常的语义说明及其精确时间区间，并在相关问答中展示对事件的理解；其核心假设是，全局稀疏浏览足以形成初始时间假设，而对可疑片段进行密集重采样和细致检查可以验证或修正该假设。论文研究两个设置：其一是在不进行领域训练的条件下，通过“全局扫视—局部审视”完成粗到细推理；其二是通过监督微调与强化学习，使单个多模态模型学会自主裁剪视频、复查局部帧并纠正错误定位。相应评价不能只看文本是否相似或时间边界是否准确，而应联合衡量语义解释质量与时间定位精度。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **VAGU**: VAGU是作者此前提出的视频异常定位与理解基准，也是本文训练无关框架和联合评价指标的早期载体。本文将其扩展为VAGU-T，新增经人工验证的问答标注以及包含视频裁剪工具调用的单轮、多轮思维链轨迹，从而同时支持评测、监督微调和智能体强化学习。
- **LAVAD与SUVAD**: 这类视觉语言方法通过逐帧或逐片段分析尝试联合异常定位与语义理解，说明两个目标可以在统一视觉语言框架中处理；但论文指出，其穷举式处理带来过高计算开销，难以满足视频异常检测的实时要求。本文据此采用先全局筛选、再局部精查的计算策略。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

工业自动化、智能监控和交通系统等场景要求视频异常检测同时回答两个直接影响处置的问题：异常“是什么”以及“何时发生”。系统还需兼顾推理速度，因为长视频中的异常通常只占很短片段，对整段视频进行高密度分析会浪费大量计算，而漏掉起止边界或误解事件含义又会削弱告警的可执行性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **传统 DNN 视频异常检测**：半监督、弱监督或开放集方法通常利用视频级标签学习正常与异常的视觉或时序模式，再为帧或片段输出异常分数和时间区间。其优势是能够形成较细的时序定位，但输出主要回答异常出现在哪里。
- **基于 LLM/VLM 的异常理解方法**：这类方法借助多模态模型和大语言模型的开放域知识，对整段视频直接问答，或逐帧、逐片段生成描述，以识别并用自然语言解释异常内容；后一种穷举式处理可增加观察细度，但需要反复运行视觉语言模型。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 传统 DNN 方法主要依赖分类监督学习异常模式，通常只给出异常分数或时间位置，缺少对事件类别、参与者行为和异常原因的自然语言理解，因此定位结果难以直接支持人工核验与后续决策。
- 现有 LLM/VLM 方法要么单次处理整段视频而忽视异常起止边界，要么逐帧或逐片段分析以换取细粒度信息；前者时间定位不精确，后者计算开销过高。即使尝试联合理解与定位，也难同时满足精度和实时速度要求。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种将时间假设与语义判断闭环连接的统一推理机制：模型应先从全局低成本地提出可疑时间范围，再用局部高密度证据验证异常含义和边界，并在证据不支持初始判断时主动修正。此前方法还缺少同时覆盖语义、定位及工具调用推理轨迹的数据与联合评价方式，因而难以系统训练和衡量这种能力。

</div>
<div markdown="1"><span>核心问题</span>

本文要回答的核心问题是：如何以全局到局部的方式统一视频异常的语义理解与精确时间定位，并分别验证两条实现路径，即现成冻结模块能否在不训练的条件下完成粗到细推理，以及单个多模态大语言模型能否通过工具调用训练内化该推理循环，在提高准确性的同时保持可接受的推理速度？

</div>
<div markdown="1"><span>作者直觉</span>

人的监控过程不会从头到尾以最高精度查看每一帧，而是先快速浏览整段视频，形成“哪里可能有问题”的假设，再放大可疑区间仔细检查；如果局部证据与初始判断冲突，就重新选择区间。将这种过程用于模型，可以把昂贵的密集视觉分析集中到少数可疑片段：全局观察负责缩小搜索范围，局部观察负责确认事件含义和起止边界，迭代修正则降低一次粗定位错误造成的连锁影响。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文给出统一“全局浏览—局部细查—迭代思考”范式的两种实现。第一种 GtS 是无需训练的模块化流程：输入完整视频后，先由视觉语言模型生成字幕，再结合异常类别表与预生成语句库构造静态主体/场景提示和动态动作/事件提示；随后分别计算帧级与片段级跨模态相似度，融合成时间曲线，据此截取少量高概率窗口；最后在这些窗口内重点采样，由 VQA 模型理解异常、LLM 跨片段整合证据，并由视频时间定位模型 VTG 输出异常区间。其核心目标是在不更新任何模型参数的情况下，同时回答“发生了什么”和“何时发生”。
第二种方法把上述固定流水线内化为一个可训练的工具增强多模态大语言模型。模型先观察全视频的稀疏帧，提出可疑时间假设，再调用视频裁剪工具取得该窗口内的密集帧；若证据不足或位置错误，它可修改窗口并再次检查，最后输出异常类别和描述，而最终一次工具调用的窗口直接作为时间定位结果。训练分为冷启动监督微调和 GRPO 强化学习：前者教会模型按格式推理、调用工具和利用返回帧，后者通过语义正确性、格式合法性和时间 IoU 联合奖励，优化模型在有限检查轮数内“查哪里、是否重查、何时作答”的策略。通俗地说，GtS 像由多个现成专家按固定流程协作；Agentic VAD 则训练一个能自己翻看录像、发现看错位置后重新查找的统一调查员。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 全局浏览与双路文本提示生成

GtS 先用现有 VLM 为视频生成字幕 $Cap_V$，再令 LLM 从 $Cap_V$、$\mathcal{A}$ 和 $\mathcal{B}_p$ 中提取静态主体/场景提示列表 $\mathcal{PL}_s$ 与动态动作/事件提示列表 $\mathcal{PL}_d$。这些提示不要求已经断言存在异常，其首要作用是识别主要内容并过滤无关背景。

<div class="method-step__io" markdown="1">

**输入**：完整输入视频 $V_{input}$、数据集提供的异常类别集合 $\mathcal{A}$，以及由 LLM 预生成的上下文语句库 $\mathcal{B}_p$。<br>
**输出**：静态提示列表 $\mathcal{PL}_s$、动态提示列表 $\mathcal{PL}_d$，以及供后续分析使用的全局视频语义。

</div>

**直观理解**：先快速看完整录像并列出“谁、在哪里”和“正在做什么”两份线索清单；即使首次字幕把异常误说成正常行为，主体和场景信息仍可帮助缩小搜索范围。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 跨模态打分与候选窗口切分

静态分支使用 CLIP 图像编码器，动态分支使用 Video-CLIP 视频编码器，分别计算文本与各时间位置视觉内容的余弦相似度并在时间轴上归一化；两条曲线按权重 $\alpha$ 融合，经 Savitzky–Golay 滤波平滑后，筛选超过阈值 $\tau$、彼此至少相隔 $\theta$ 的 Top-$K$ 局部峰值，并以峰值为中心按视频总时长 $T$ 建立动态窗口。

<div class="method-step__io" markdown="1">

**输入**：静态/动态文本提示、视频帧与短视频片段。<br>
**输出**：平滑时间分数曲线 $S(t)$、候选峰集合 $\mathcal{P}^{*}$，以及高概率窗口集合 $\mathcal{H}$ 和其余低概率片段。

</div>

**直观理解**：系统把“画面像不像某类主体或动作”画成一条随时间变化的曲线，峰值附近就是值得细看的位置；间距约束避免多个候选都挤在同一个事件附近。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 局部细查、证据融合与时间定位

在每个片段内依据 $S(t)$ 的累积分布进行非均匀采样，使高分区域获得更多帧；VQA 对高概率片段判断并描述异常，对低概率片段生成字幕和潜在线索，随后 LLM 去重并连接跨片段因果证据，VTG 再以细粒度异常描述为查询完成时间定位。

<div class="method-step__io" markdown="1">

**输入**：高/低概率片段、片段内分数 $S(t)$、异常类别表，以及前一片段的理解结果。<br>
**输出**：异常类别与自然语言解释，以及经语义条件约束的异常起止区间。

</div>

**直观理解**：有限的帧预算优先花在最可疑的位置，同时保留低分片段作为上下文；把前后片段串联后，系统才可能识别“先放置可燃物、后点火”这类不能由单帧说明的异常。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 冷启动工具调用监督微调

模型以标准下一词元预测损失学习交错的 think、tool_call 和 answer 序列，损失掩码只覆盖助手生成的推理、工具调用和答案词元。异常专用轨迹占 SFT 语料一半，另外一半由三类通用推理数据均衡构成，以同时建立工具使用能力并缓解领域微调造成的灾难性遗忘。

<div class="method-step__io" markdown="1">

**输入**：VAGU-T 的单轮及多轮工具调用轨迹、通用视频推理数据、LLaVA-CoT 图像推理数据和 GeminiCoT 长视频推理数据。<br>
**输出**：能够从全局稀疏帧提出时间窗口、调用裁剪工具、理解密集返回帧并在假设错误时改换窗口的初始策略。

</div>

**直观理解**：直接强化学习时，基础模型甚至不会稳定地调用工具，因此先用示范轨迹教会它完整操作规程；通用数据用于防止模型只会套异常检测格式而丢失基础视觉理解能力。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### GtS 双路跨模态时间相似度

$$
S_{s/d}(t)=\frac{\exp\!\left(\frac{1}{N}\sum_{n=1}^{N}\left\langle\Phi_x(pl_x^n),\Phi_x(V_t)\right\rangle\right)}{\sum_{t'}\exp\!\left(\frac{1}{N}\sum_{n=1}^{N}\left\langle\Phi_x(pl_x^n),\Phi_x(V_{t'})\right\rangle\right)},\qquad x\in\{\mathrm{image},\mathrm{video}\}
$$

**符号说明**

- $S_{s/d}(t)$：时间位置 $t$ 的静态分支分数 $S_s(t)$ 或动态分支分数 $S_d(t)$。
- $t,t'$：当前时间位置与归一化分母中遍历的视频时间位置。
- $N$：对应静态或动态分支中的文本描述数量。
- $pl_x^n$：分支 $x$ 中第 $n$ 条静态或动态文本提示。
- $V_t$：时间 $t$ 处的输入帧或视频片段。
- $\Phi_x$：分支 $x$ 对应的编码器；$x=\mathrm{image}$ 时使用图像编码器，$x=\mathrm{video}$ 时使用视频编码器。
- $\langle\cdot,\cdot\rangle$：文本特征与视觉特征之间的余弦相似度。

<div class="equation-explanation" markdown="1">

**直观理解**：每个时间位置先与该分支的全部文本提示比较并取平均，再通过沿时间轴的 softmax 转成相对概率。这样得到的不是孤立的“是否异常”分类，而是一张用于比较录像中哪些时刻更值得检查的时间注意力图；后续平滑、找峰和切窗都建立在该分数之上。<br>
**原文位置**：第 4.1 节，公式 (3)

</div>

</div>

<div class="equation-block" markdown="1">

#### Agentic RL 的裁剪策略目标与联合结果奖励

$$
\begin{aligned}\mathcal{J}(\theta)&=\mathbb{E}\!\left[\frac{1}{K}\sum_{k=1}^{K}\frac{1}{|o_k|}\sum_{t=1}^{|o_k|}\left(\min\!\left(\rho_{k,t}(\theta)A^{(k)},\operatorname{clip}(\rho_{k,t}(\theta),1-\epsilon,1+\epsilon)A^{(k)}\right)-\beta D_{KL}[\pi_\theta\|\pi_{ref}]\right)\right],\\ A^{(k)}&=R^{(k)}-\frac{1}{K}\sum_{j=1}^{K}R^{(j)},\qquad R=R_{acc}+R_{format}+R_{time},\\ R_{time}&=\operatorname{IoU}([\hat t_s,\hat t_e],[t_s,t_e])=\frac{|[\hat t_s,\hat t_e]\cap[t_s,t_e]|}{|[\hat t_s,\hat t_e]\cup[t_s,t_e]|}.\end{aligned}
$$

**符号说明**

- $\theta$：当前待优化策略模型的参数。
- $K$：针对同一强化学习提示采样的轨迹数量。
- $o_k$：第 $k$ 条完整工具使用轨迹，$|o_k|$ 为其中参与策略目标的生成词元数。
- $\rho_{k,t}(\theta)$：当前策略与采样旧策略在第 $k$ 条轨迹第 $t$ 个生成词元上的概率比。
- $A^{(k)}$：第 $k$ 条轨迹的组相对优势，即其奖励减去同组 $K$ 条轨迹的平均奖励。
- $\epsilon$：PPO 风格概率比裁剪范围，限制单次策略更新幅度。
- $\beta$：KL 正则项的权重。
- $D_{KL}[\pi_\theta\|\pi_{ref}]$：当前策略 $\pi_\theta$ 相对参考策略 $\pi_{ref}$ 的 KL 偏离惩罚。
- $R_{acc}$：最终异常类别、描述及因果解释与真值的一致性奖励。
- $R_{format}$：think、tool_call 与唯一 answer 块是否严格按规定交错排列的格式奖励。
- $R_{time}$：最后一次裁剪窗口与真实异常区间之间的时间交并比奖励；无工具调用时为 $0$。
- $[\hat t_s,\hat t_e]$：轨迹最后一次 crop video 调用的预测起止时间。
- $[t_s,t_e]$：人工标注的真实异常起止时间。

<div class="equation-explanation" markdown="1">

**直观理解**：GRPO 在同一视频的多条尝试之间做相对比较：奖励高于组均值的推理和工具调用会被增强，较差尝试会被抑制，裁剪与 KL 项则避免更新过猛。奖励同时要求语义正确、结构可执行和区间精确；时间项采用 IoU 而非召回率，是因为覆盖整段视频虽可获得高召回，却会因并集过大得到较低 IoU，从而抑制无限扩张裁剪窗口的投机策略。<br>
**原文位置**：第 5.4 节，公式 (10)、(12)、(14) 和 (15) 的联合表达

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：GtS 不涉及参数训练，其静态/动态提示生成、编码、平滑、切窗、VQA 理解、LLM 汇总和 VTG 定位均在推理期调用冻结模块。Agentic VAD 的第一阶段最小化掩码自回归损失 $\mathcal{L}(\theta)=-\sum_{t=1}^{L}m_t\log p_\theta(x_t\mid x_{<t})$；其中 $x_t$ 是第 $t$ 个词元，$x_{<t}$ 是此前词元，$L$ 是序列长度，$m_t$ 仅在助手产生的 think、tool_call 和 answer 词元上取 $1$。该阶段解决直接 RL 时不调用工具、不能整合返回帧以及退化为普通字幕生成的问题。
第二阶段以 SFT 模型为初始策略执行 GRPO。每个提示生成 $K$ 条完整轨迹，奖励 $R$ 等权汇总三项：$R_{acc}$ 由 GPT-4o 作为裁判按完全一致、部分一致、不一致或空答案给出 $1$、$0.5$、$0$，且超长答案记为 $0$；$R_{format}$ 仅在块结构完全合法时为 $1$；$R_{time}$ 是最后裁剪窗口与真值区间的 IoU。工具返回的密集视觉帧被掩码，不作为策略生成词元计算梯度；论文也不设置额外工具使用奖励，因为 SFT 已建立调用能力，而额外奖励可能诱导无意义的重复调用。训练仅保留同组 rollout 结果有对有错的提示，以避免全对或全错造成近零相对优势，并平衡视频时长分布以维持长视频训练信号。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 静态—动态双文本引导模块**

该模块将静态主体/场景与动态动作/事件分开建模：$\Phi_{image}$ 对文本和帧编码以生成 $S_s(t)$，$\Phi_{video}$ 对文本和视频片段编码以生成 $S_d(t)$；二者融合后平滑，并通过峰值阈值、峰间距和相对时长窗口完成粗定位。设计依据是现有 VLM 即使误判异常属性，通常仍能较准确识别主体，因此可先利用较可靠的主体和动作语义过滤背景。

> 直观理解：静态线索适合回答“谁和什么场景出现了”，动态线索适合回答“发生了什么动作”；两类线索互补，能降低仅凭单帧漏掉动作、或仅凭短片段忽略关键主体的风险。

**2. 分数驱动的非均匀采样与跨片段理解模块**

对片段 $[a,b]$，系统按累计分数的等质量分位点选择 $N$ 个时间戳，使局部采样密度与 $S(t)$ 大致成正比；处理非首片段时还输入前一片段的理解结果，最后由 LLM 合并字幕、删除重复或无关内容并建立跨片段语义联系。高概率片段用于直接识别异常，低概率片段仍用于补充前因、后果和主体连续性。

> 直观理解：它不是机械地每隔固定时间抽一帧，而是在疑点密集处多看几眼；同时保留前后文，避免把一个连续事件切开后分别误解。

**3. 可自我修正的视频裁剪智能体**

统一 MLLM 接收全局均匀采样帧，生成 think 块和带时间参数的 tool_call，工具从指定窗口返回更密集的帧；模型可依据新证据结束推理，也可否定原假设并再次调用工具。训练奖励将最后一次工具窗口绑定为定位输出，从机制上要求模型对最终区间进行实际视觉核验，而不能只在答案文本中虚构一个时间范围。

> 直观理解：全局稀疏帧负责快速找方向，裁剪工具相当于回放并放大某段录像；若放大后发现没有异常，模型可以移动时间窗口重新检查，而不是被第一次猜测锁死。

**训练与推理**

训练数据方面，VAGU-T 的异常专用工具轨迹用于学习与异常相关的时间假设、裁剪调用和密集帧解释，占 SFT 语料的 $50\%$、RL 提示的 $70\%$；SFT 的另一半由通用视频推理、LLaVA-CoT 图像推理和 GeminiCoT 长视频推理三类来源等量组成。训练顺序不能颠倒：论文报告直接从基础模型开始 RL 会发生训练崩溃，表现为不调用工具，偶发调用时也无法把返回帧纳入连贯推理；完成冷启动 SFT 后，模型才具备用结果奖励继续探索的基本行为策略。
GtS 推理是一次固定的粗到细执行：完整视频生成字幕和双路提示，得到时间分数曲线与候选窗口，再对各窗口非均匀采样、逐段理解、跨段汇总，最后交给 VTG 定位。Agentic 模型推理则从均匀采样的全局稀疏帧开始，输出第一轮时间假设并调用 crop video；每次获得密集帧后，要么输出最终异常类别和描述，要么修订窗口继续调用，直至置信度足够或达到 $T_{max}$。达到轮数上限时必须依据已收集证据作答，且答案文本只承担异常理解，时间定位统一读取最后一次工具调用窗口，从而让输出语义和可核验的视觉检查行为保持一致。

**复现信息**

公平理解方法所需的关键细节包括：GtS 使用 CLIP 处理静态帧语义、Video-CLIP 处理动态片段语义，并用 Savitzky–Golay 滤波保持事件曲线的时间连续性；候选窗口由 Top-$K$ 峰值、分数阈值 $\tau$、峰间距 $\theta$ 和相对窗口比例 $\eta$ 共同决定。片段内不是均匀抽帧，而是按 $S(t)$ 的累计质量划分为 $N$ 份并取对应分位时间戳；这使帧数预算集中于高分区域。原文节选未给出 $K$、$\alpha$、$\tau$、$\theta$、$\eta$、$N$、$T_{max}$、GRPO 裁剪范围 $\epsilon$、KL 权重 $\beta$ 或答案长度阈值的具体取值，复现时不能据此自行声称论文采用了某个数值。
Agentic 方法把视频裁剪作为原生工具调用，强化学习时只对模型自己生成的推理、调用和答案词元更新参数，工具返回内容不进入策略梯度。时间奖励固定取最后一次调用窗口；没有调用工具时 $R_{time}=0$，因此无需另设工具使用奖励。RL 提示经过两项筛选：剔除 $K$ 条 rollout 全对或全错的样本，并按视频时长平衡批次。语义奖励依赖 GPT-4o 裁判，因而结果解释时应注意该奖励含有外部评判模型的偏差；原文作者将其作为训练奖励设计，而不是人工标注准确率的等价替代。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- VAGU-T 是本文统一的训练与评测套件，包含 7,567 个真实世界视频和 21 类异常，并提供经过人工核验的异常时间区间、解释、问答对及带工具调用的思维链轨迹。实验在该套件上评估训练自由 GtS、SFT 模型和 Agentic RL 模型；节选未给出训练集、验证集与测试集的具体样本数及划分比例。另有 100 个随机抽取且明确不进入评测集的异常视频，仅用于确定 GtS 的分段超参数，不能视为最终测试样本。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**A.U.**

异常理解分数，由外部大语言模型依据主体、场景、事件过程和影响四个方面，将生成描述相对真实答案的准确性、清晰性、简洁性与连贯性评为 1 至 10 分。它主要测量语义解释质量，不直接代表时间定位精度。 （越高越好，因为高分表示生成的异常描述在四个语义方面更接近人工参考答案。）

</div>
<div class="metric-item" markdown="1">

**JeAUG**

联合异常理解与定位指标，形式为 $\min(\gamma F(\mathrm{IoU}),1)\cdot\mathrm{Score}_{A.U.}$。其中，$F(\mathrm{IoU})$ 把预测区间与人工区间的重叠程度转换为符合人工偏好的定位权重，并在 $\mathrm{IoU}=0.7$ 后饱和；$\gamma$ 根据视频长度补偿长视频定位难度。因此，该指标要求模型既能正确解释异常，也能把异常落到合理时间范围。 （越高越好，因为分数同时受异常理解质量和时序重叠质量制约；但其数值也依赖本文设计的人工偏好函数与视频长度补偿。）

</div>
<div class="metric-item" markdown="1">

**FPS**

每秒处理帧数，用于衡量推理吞吐量。本文将 30 FPS 作为可接受的实时阈值，并用它比较穷举片段流水线、训练自由 GtS 和训练后智能体的计算效率。 （越高越好，因为更高 FPS 表示单位时间可处理更多视频帧；但 FPS 受硬件、采样策略和实现方式影响，跨系统比较需要保持实验条件一致。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 相同 Qwen2.5-VL-7B 骨干下，GtS 对比直接应用现成模型的训练自由基线

<div class="result-value" markdown="1">

加入 GtS 后，JeAUG 从 2.28 提升至 4.04，且 FPS 保持在 30 以上。

</div>

作者据此主张，粗到细的全局浏览、可疑片段复查和文本引导，比把现成 VQA/VTG 模型直接用于长视频更能兼顾语义与时间定位，并达到其设定的实时门槛。该结果支持 GtS 流程有效，但不能单独确定提升来自静态文本引导、动态文本引导、分段算法还是具体模型组合；节选也未提供置信区间或显著性检验。

<div class="result-source" markdown="1">

来源：第 7.2 节，Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, GtS attains a favorable balance: on the same backbone it substantially improves both A.U. and JeAUG over the corresponding direct baseline (e.g., Qwen2.5-VL-7B: JeAUG 2.28→4.04) while keeping FPS above the acceptable threshold of 30.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 冷启动 SFT 模型对比最强逐帧或逐片段流水线 SUVAD

<div class="result-value" markdown="1">

SFT 的 A.U. 为 6.62，高于 SUVAD 的 5.73，同时推理速度接近快 3 个数量级。

</div>

作者将其解释为：模型通过 SFT 内化全局到局部工具调用轨迹后，无须穷举所有片段也能获得更好的异常语义理解。这里明确比较的是 A.U. 与速度，不能据此断言 SFT 在每个异常类别、时间定位精度或所有联合指标上都优于 SUVAD；“接近三个数量级”也依赖 Table 5 的具体硬件与实现条件。

<div class="result-source" markdown="1">

来源：第 7.2 节，Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The SFT model already surpasses the strongest frame/segment-wise pipeline SUVAD in A.U. (6.62 vs. 5.73) while running nearly three orders of magnitude faster, confirming that internalizing the global-to-local reasoning loop eliminates the need for exhaustive segment processing.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 完整 Agentic RL 模型在全部对比方法中的总体表现

<div class="result-value" markdown="1">

Agentic RL 达到 A.U. 7.35、JeAUG 5.91 和 148 FPS，为文中比较方法中的最高准确性，并明显超过 30 FPS 的实时阈值。

</div>

这一结果表明，在本文数据、指标和实现条件下，最终智能体同时取得最好的语义与联合定位分数，并保持高吞吐量，体现了准确性与效率的综合优势。它不证明模型在 VAGU-T 之外同样泛化，也不证明 148 FPS 能直接复现于其他硬件；此外，JeAUG 包含本文自定义的人工偏好映射与长度补偿，因此仍需结合原始 IoU 或外部指标审查。

<div class="result-source" markdown="1">

来源：第 7.2 节，Table 5；另见 Figure 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Overall, the Agentic RL model achieves the best accuracy among all compared methods (A.U. 7.35, JeAUG 5.91) at 148 FPS, exceeding the real-time threshold by a large margin (see also Fig. 1).

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

- LAVAD：逐帧或逐片段穷举处理视频的 VAD 流水线。它用于检验细粒度遍历能取得怎样的异常理解与联合评测表现，以及这种准确性是否以明显降低 FPS 为代价。
- SUVAD：另一种逐帧或逐片段流水线，也是文中用于比较的最强此类方法。它与 SFT、Agentic RL 的比较用于判断学习到的全局到局部推理是否能取代昂贵的穷举片段处理。
- 现成 VQA 与 VTG 模型的直接组合：VQA 负责回答视频内容问题，VTG 负责把文本事件定位到时间区间。该组是训练自由 GtS 最关键的对照，因为二者使用相同或对应的现成骨干模型，差异主要在于是否加入 GtS 的粗到细检索与文本引导流程。
- SFT：以 Qwen2.5-VL-7B-Instruct 为基础、通过带工具调用轨迹进行冷启动监督微调的模型。它既是训练模型，也构成 Agentic RL 的直接起点，用于区分模仿人工轨迹与进一步接受结果奖励优化的效果。

**实验想回答的问题**

- 训练自由的全局到局部框架 GtS，能否在不更新模型参数的条件下，比直接组合现成视频问答模型与时序定位模型更准确地完成异常理解和时间定位，同时保持实时推理速度？
- 经过冷启动监督微调后，基于结果奖励的智能体强化学习能否进一步学会调用视频裁剪工具、复查局部帧并修正定位，从而同时改善异常语义理解、时序定位和推理效率？

**实验实现**

所有方法均在 VAGU-T 上报告指标。实验原本还报告多项选择 QA 准确率，但该指标只适用于原生支持选择题协议的方法：逐帧或逐片段流水线输出描述与异常曲线，训练模型则输出开放式工具思维链答案，因此并非所有方法都有可比的 QA 数值。GtS 使用 CLIP-L/14 编码视频帧，以不同 VLM 分别承担异常理解和定位，并用 Llama-3.1-8B 整合描述；关键分段参数包括 $\alpha=0.4$、阈值 $\tau$ 取相似度曲线所有峰值的均值、$\theta$ 取总帧数除以 12，以及 $\eta=1/20$。GtS 的全部实验在 14 张 A6000 GPU 上累计约 210 小时。训练模型以 Qwen2.5-VL-7B-Instruct 为基础：SFT 训练 2 个 epoch，学习率为 $1\times10^{-5}$ 并采用余弦衰减；随后以 GRPO 进行 Agentic RL，每个提示生成 $K=8$ 个 rollout，裁剪范围 $\epsilon=0.2$，KL 系数 $\beta=1\times10^{-3}$，最多调用工具 3 轮，全局视频与裁剪片段均采样 128 帧；训练硬件为 24 个、每个 96 GB 的 Alibaba T-Head PPU。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work develops video-grounded multimodal reasoning together with an agentic model that invokes cropping and resampling tools to iteratively correct temporal hypotheses.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`ba30a23a4cbe6d9ca710c498a7cd2dace77a64aee876e8ac86a42a42a46a351a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
