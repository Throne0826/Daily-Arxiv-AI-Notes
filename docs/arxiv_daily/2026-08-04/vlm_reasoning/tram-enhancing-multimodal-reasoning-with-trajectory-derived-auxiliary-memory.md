---
title: "[论文解读] TRAM: Enhancing Multimodal Reasoning with Trajectory-Derived Auxiliary Memory"
description: "[arXiv 2608.01922][VLM Reasoning] 本文认为，多模态长程推理的关键障碍不只是视觉信息逐渐失效，还包括早期推理形成的关系、约束和中间结论难以持续影响后续计算，因此提出用模型自身已完成的推理轨迹构造辅助记忆。"
arxiv_id: "2608.01922"
announcement_date: "2026-08-04"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:57:17.822177+00:00"
source_sha256: "df01bcac30a6429293c47b6250070da3a8e0e0da26631883e77b7747dd40daf9"
tags:
  - "VLM Reasoning"
  - "LLM Reasoning"
  - "多模态大推理模型"
  - "视觉推理"
  - "推理轨迹"
  - "视觉落地"
  - "长程信息保持"
  - "轨迹衍生记忆"
  - "测试时解码"
  - "无需训练"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.01922</p>

# TRAM: Enhancing Multimodal Reasoning with Trajectory-Derived Auxiliary Memory

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Kang Liu, Zijing Wang, Yongkang Liu, Mengjie Zhao, Xiaocui Yang, Shi Feng, Yifei Zhang, Daling Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Northeastern University, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01922v1) · [PDF 下载](https://arxiv.org/pdf/2608.01922v1) · **关键词** 多模态大推理模型, 视觉推理, 推理轨迹, 视觉落地, 长程信息保持, 轨迹衍生记忆, 测试时解码, 无需训练<br>


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

本文认为，多模态长程推理的关键障碍不只是视觉信息逐渐失效，还包括早期推理形成的关系、约束和中间结论难以持续影响后续计算，因此提出用模型自身已完成的推理轨迹构造辅助记忆。

**不用术语来说**：模型解答需要看图并连续推导的问题时，可能在前面已经正确识别条件并得到有用结论，却随着回答变长而逐渐“忘记”这些内容，导致后续步骤偏离原本正确的思路。仅让模型反复看原图并不能完全解决这一问题，因为许多关键知识并未直接画在图中，而是模型通过前几步分析才推导出来的。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者通过归因分析区分原始图像证据与不同推理阶段信息的作用，指出图像归因的下降同时出现在正确和错误轨迹中，不能稳定解释成败；相比之下，正确轨迹表现出对多个阶段所形成信息的更广泛整合。
- 作者据此提出无需额外训练的 TRAM：将模型自身已完成的推理压缩为潜在辅助记忆，通过快、慢两种时间尺度在线更新，并以轻量残差路径反馈至选定解码层，使早期推理所得信息能直接参与后续计算。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

多模态大推理模型（MLRM）是在视觉语言模型基础上加入显式多步推理能力的模型：它不仅根据图像直接作答，还会生成中间推理轨迹，把视觉观察逐步转化为与任务有关的关系、约束和阶段性结论。本文关注长推理轨迹中的信息保持问题：随着生成内容增加，模型后续步骤可能无法稳定利用图像证据以及早期已经形成的推理信息，从而偏离原本正确的推理方向。现有研究多通过反复查看图像、视觉条件解码校准、视觉表示引导或可学习视觉通路来维持视觉依据；本文所处的研究背景则进一步区分了两类信息，即输入图像提供的原始视觉证据，以及模型在推理过程中从这些证据中推导出的任务特定信息。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多模态大推理模型（MLRM）**

能够联合处理图像与文本，并在输出最终答案前执行多步推理的生成模型。与只做直接识别或描述的模型相比，它需要在较长上下文中持续整合视觉证据和中间结论。

</div>
<div class="concept-item" markdown="1">

**推理轨迹**

模型从问题和图像出发，到生成最终答案为止所产生的一系列中间分析步骤。轨迹越长，早期信息对后续计算的影响越可能减弱。

</div>
<div class="concept-item" markdown="1">

**视觉落地（visual grounding）**

推理内容与输入图像中的实际对象、属性或关系保持对应，而不是仅依赖语言模式继续生成。维持视觉落地可以减少脱离图像证据的推断，但不必然保存已经从图像推导出的关系、约束和中间结论。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入是图像与相应的问题，模型通过自回归解码生成包含若干中间步骤的推理轨迹，并最终输出答案。本文考虑无需额外训练的推理时设置：基础MLRM及其参数保持不变，也不依赖外部验证器或修改注意力机制；需要解决的是，当轨迹逐渐增长时，如何让早期已完成推理所形成的信息继续参与后续计算。该设置隐含的关键区分是：重新增强图像只能恢复原始视觉证据，不能直接恢复模型先前据此得到的任务特定关系、约束和阶段性结论，因此需要一种从模型自身轨迹构造并在线更新的辅助记忆。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **VisRef: Visual Refocusing While Thinking Improves Test-Time Scaling in Multi-Modal Large Reasoning Models（Ghosal et al., 2026）**: 属于推理过程中重新查看或重新聚焦输入图像的方法，用于持续强化视觉落地。它能让模型再次访问原始视觉证据，但按照本文的论述，不能直接携带此前推理已经形成的任务特定关系和中间结论。
- **Persistent Visual Memory: Sustaining Perception for Deep Generation in LVLMs（Huang et al., 2026b）**: 通过可学习的视觉通路维持长生成过程中的图像信息影响，代表以持续视觉感知缓解长程推理退化的方向。TRAM所针对的背景问题不同：它关注的是推理轨迹衍生信息的保留，并采用无需额外训练的辅助记忆路径。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

多模态大推理模型需要同时处理图像证据与多步文本推导，但推理轨迹越长，模型越可能无法稳定调用上下文早期已经建立的信息。其实际后果是：即使前半段观察和推导正确，后半段仍可能遗漏既有条件、违反已推出的约束，或转向与前文不一致的结论。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **训练式持续视觉接地**：通过强化学习或可学习的视觉通路，训练模型在生成较长推理轨迹时继续依赖输入图像，降低推理逐渐脱离视觉证据的风险。
- **推理时视觉增强**：在不改变或少量改变模型训练的情况下，利用视觉条件解码校准、视觉表征引导，或在推理过程中重新查看输入图像，持续提高原始视觉信息对后续生成的影响。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有方法大多把问题归因于长文本上下文削弱了图像贡献，因此主要强化对原图的访问；但作者的归因分析表明，图像归因会在正确与错误轨迹中同时下降，两者之间没有稳定差异，所以单独维持视觉归因不足以解释或可靠区分推理成败。
- 原图只能重新提供视觉观察，不能直接保存模型已从这些观察中推导出的任务特定关系、约束和中间结论；当这些推理衍生信息随轨迹增长而影响减弱时，重复看图仍可能迫使模型重新推导，或使后续步骤无法利用此前已经形成的结论。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一种面向长程多模态推理、能够在推理时持续保留并重新注入“由既往推理产生的信息”的机制。该机制还应避免额外训练、参数更新、外部验证器以及对注意力结构的大幅修改，从而能直接附加到已有模型的标准解码过程。

</div>
<div markdown="1"><span>核心问题</span>

能否把模型自身已经完成的推理在线压缩为紧凑记忆，并在后续解码中持续反馈，使近期推理与更早阶段形成的信息都保持可用，从而在无需额外训练的条件下减少长轨迹中的推理偏移？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把推理轨迹视为一种不断生成的新证据，而不只是越来越长的文本历史。直观地说，原图类似原始材料，早期推理则是从材料中整理出的关键笔记；后续步骤既需要查看材料，也需要直接读取笔记。若用快速记忆跟踪最近推导、用慢速记忆保留跨阶段结论，再把两者送回模型内部，模型就更可能兼顾当前进展与长期约束，而不必每一步都从原图重新推导。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TRAM 是一种无需训练的测试时干预方法。给定图像 $I$ 和问题 $Q$，原多模态推理模型仍按常规方式自回归生成推理文本；TRAM 将已经完成的推理按句末符或换行划分为步骤，并在若干选定解码层中读取每一步末尾 $w$ 个 token 的前馈网络输出。每层分别用快速、慢速两条指数衰减流递归汇总这些步骤表示：快速流侧重最近结论，慢速流保留更早的关系与约束；随后限制慢速流的范数并将二者相加，得到紧凑的轨迹记忆。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成并在线识别推理步骤

模型 $4\mathcal{M}$ 继续执行标准自回归解码，并依据句末符和换行在线确定已完成步骤 $S_k$ 的结束位置 $e_k$。只有确认完成的步骤才进入记忆更新，因此在转移位置 $4\tau_k=e_k+1$ 处不读取下一步的未来 token。

<div class="method-step__io" markdown="1">

**输入**：多模态提示 $4\mathcal{P}=(I,Q)$，其中 $I$ 是图像、$Q$ 是文本问题，以及模型当前已生成的 token 序列。<br>
**输出**：已完成的推理步骤 $S_k$、边界位置 $e_k$ 和下一步的首个解码位置 $4\tau_k$。

</div>

**直观理解**：系统一边作答一边把已经写完的句子视为推理单元。它只整理已经说过的内容，不提前查看尚未生成的文字。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提取步骤级推理表示

对 $U_k$ 内的 $4f_t^{(\ell)}$ 做均值池化，得到层特定的步骤表示 $4s_k^{(\ell)}$。选择 FFN 输出是为了读取该层已经变换过的推理信号；只读取尾部窗口可减少整步池化混入中间过程的风险，也比单个边界 token 更稳定。

<div class="method-step__io" markdown="1">

**输入**：步骤 $S_k$ 在选定解码层 $4\ell$ 中产生的前馈网络输出 $4f_t^{(\ell)}$，以及该步骤末尾至多 $w$ 个 token 构成的窗口 $U_k$。<br>
**输出**：每个选定层各自的紧凑步骤向量 $4s_k^{(\ell)}$。

</div>

**直观理解**：这一步从一句推理的结尾附近提炼“本句最后得出了什么”。连续读取几个 token，相当于参考一句话的收尾片段，而不是只看最后一个标点或把整句所有细节平均掉。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 更新双时间尺度记忆

两条记忆流分别按衰减因子 $4\lambda_{\mathrm{fast}}$ 和 $4\lambda_{\mathrm{slow}}$ 递归更新，满足 $40\leq\lambda_{\mathrm{fast}}<\lambda_{\mathrm{slow}}<1$。慢速记忆在合并前被限制为不超过快速记忆范数的 $r$ 倍，然后二者相加形成 $4m_k^{(\ell)}$；不同层的记忆互不共享。

<div class="method-step__io" markdown="1">

**输入**：当前步骤表示 $4s_k^{(\ell)}$、上一时刻的快速记忆 $4m_{k-1,\mathrm{fast}}^{(\ell)}$ 与慢速记忆 $4m_{k-1,\mathrm{slow}}^{(\ell)}$。<br>
**输出**：兼顾近期推理与较早推理历史的层特定记忆 $4m_k^{(\ell)}$。

</div>

**直观理解**：快速流像短期便笺，优先保留刚得到的结论；慢速流像长期摘要，使早先形成的条件不会迅速消失。范数上限用于防止长期摘要因不断累积而压过近期信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在步骤转移处注入记忆

对每个 $4\ell\in\mathcal{L}_{\mathrm{inj}}$，将 $4\alpha m_k^{(\ell)}$ 加到下一步首个位置的残差状态中；可选的范数保持操作再把新状态缩放回原状态的二范数。干预只发生在步骤边界，而不是每个生成位置。

<div class="method-step__io" markdown="1">

**输入**：转移位置 $4\tau_k$ 的原始残差隐藏状态 $4h_{\tau_k}^{(\ell)}$、对应层记忆 $4m_k^{(\ell)}$、注入强度 $4\alpha$ 和注入层集合 $4\mathcal{L}_{\mathrm{inj}}=[L_{\min},L_{\max}]$。<br>
**输出**：供后续解码层继续处理的记忆增强状态 $4\widehat{h}_{\tau_k}^{(\ell)}$。

</div>

**直观理解**：开始下一句推理时，模型会收到一份由此前推理整理出的提示。恢复原有向量长度主要改变信息方向而非整体激活强度，可减小干预破坏模型原始计算尺度的风险。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 双时间尺度轨迹记忆的更新与合并

$$
\begin{aligned}
s_k^{(\ell)}&=\frac{1}{|U_k|}\sum_{t\in U_k}f_t^{(\ell)},\\
m_{k,q}^{(\ell)}&=\lambda_q m_{k-1,q}^{(\ell)}+s_k^{(\ell)}=\sum_{j=1}^{k}\lambda_q^{k-j}s_j^{(\ell)},\quad q\in\{\mathrm{fast},\mathrm{slow}\},\\
\bar m_{k,\mathrm{slow}}^{(\ell)}&=m_{k,\mathrm{slow}}^{(\ell)}\min\!\left(1,\frac{r\|m_{k,\mathrm{fast}}^{(\ell)}\|_2}{\|m_{k,\mathrm{slow}}^{(\ell)}\|_2}\right),\\
m_k^{(\ell)}&=m_{k,\mathrm{fast}}^{(\ell)}+\bar m_{k,\mathrm{slow}}^{(\ell)}.
\end{aligned}
$$

**符号说明**

- $s_k^{(\ell)}$：第 $k$ 个推理步骤在第 $\ell$ 层的紧凑表示。
- $U_k$：步骤 $S_k$ 末尾至多 $w$ 个 token 的位置集合。
- $f_t^{(\ell)}$：位置 $t$ 在第 $\ell$ 个解码层的前馈网络输出。
- $m_{k,q}^{(\ell)}$：处理完第 $k$ 步后，第 $\ell$ 层分支 $q$ 的递归记忆，其中 $q$ 为快速或慢速分支。
- $\lambda_q$：分支 $q$ 的历史衰减因子；论文规定 $0\leq\lambda_{\mathrm{fast}}<\lambda_{\mathrm{slow}}<1$。
- $r$：慢速记忆相对于快速记忆所允许的最大范数比例。
- $\bar m_{k,\mathrm{slow}}^{(\ell)}$：经过相对范数限制的慢速记忆。
- $m_k^{(\ell)}$：快速记忆与受限慢速记忆合并后的最终层记忆。

<div class="equation-explanation" markdown="1">

**直观理解**：每个步骤先被压缩成一个向量，再按“越早的信息权重越小”的规则累计。快速流衰减更快、偏重最近步骤，慢速流衰减更慢、保留较长历史；限制慢速流的长度后相加，得到既有近期敏感性又有长期保持能力的记忆。<br>
**原文位置**：Method，Recurrent Dual-Timescale Memory，式（6）至式（11），核心递推展开见式（9）

</div>

</div>

<div class="equation-block" markdown="1">

#### 边界处的加性注入与范数保持

$$
\begin{aligned}
\widetilde h_{\tau_k}^{(\ell)}&=h_{\tau_k}^{(\ell)}+\alpha m_k^{(\ell)},\\
\widehat h_{\tau_k}^{(\ell)}&=\widetilde h_{\tau_k}^{(\ell)}\frac{\|h_{\tau_k}^{(\ell)}\|_2}{\|\widetilde h_{\tau_k}^{(\ell)}\|_2},\qquad \tau_k=e_k+1.
\end{aligned}
$$

**符号说明**

- $\tau_k$：第 $k$ 个步骤完成后的转移位置，即下一推理步骤的首个生成位置。
- $e_k$：第 $k$ 个推理步骤的结束位置。
- $h_{\tau_k}^{(\ell)}$：注入前，转移位置在第 $\ell$ 层入口处的残差隐藏状态。
- $m_k^{(\ell)}$：处理完第 $k$ 个步骤后，由第 $\ell$ 层历史推理构造的记忆。
- $\alpha$：控制记忆影响强度的正数系数。
- $\widetilde h_{\tau_k}^{(\ell)}$：加上记忆后、尚未恢复范数的隐藏状态。
- $\widehat h_{\tau_k}^{(\ell)}$：恢复到原隐藏状态二范数后的最终注入状态。

<div class="equation-explanation" markdown="1">

**直观理解**：第一行把轨迹记忆作为残差方向加入下一步的起始状态；第二行把结果缩放到注入前的长度。这样主要调整状态所表达的信息组合，同时避免单纯放大激活值造成过强扰动。<br>
**原文位置**：Method，Memory Injection，式（12）至式（13）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。TRAM 是训练无关的测试时方法，没有新增损失函数、参数优化或微调过程；它直接复用冻结模型在生成期间产生的 FFN 激活，并通过确定性的递推、范数约束和残差注入改变后续解码状态。因此，其性能变化来自推理计算路径的干预，而不是从评测数据学习参数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 尾部窗口步骤读取器**

对步骤 $S_k$ 的尾部索引集 $4U_k=\{\max(b_k,e_k-w+1),\ldots,e_k\}$ 内的 FFN 输出做均值池化，并在每个注入层独立生成 $4s_k^{(\ell)}$。该设计依赖在线检测到的自然推理边界，而不是按固定 token 数机械分块。

> 直观理解：推理步骤的末尾通常集中体现该步形成的关系或中间结论。按真实句子边界读取，能让记忆更新与文本的推理结构对齐。

**2. 递归双时间尺度记忆**

快速与慢速分支对历史步骤表示采用不同衰减率进行指数加权累积；较大的 $4\lambda_{\mathrm{slow}}$ 提供更长的有效记忆范围，较小的 $4\lambda_{\mathrm{fast}}$ 提高对近期变化的响应。慢速分支经过相对范数上限后再与快速分支相加，避免长期累积造成尺度失衡。

> 直观理解：单一记忆速度难以同时处理“刚得出的结果”和“很早提出但仍有效的条件”。两条流分工保留这两类信息，再通过幅度约束保持平衡。

**3. 层特定边界注入器**

记忆仅注入区间 $4\mathcal{L}_{\mathrm{inj}}$ 内的对应层，并且第 $4\ell$ 层只读取由该层 FFN 输出构造的记忆。注入发生于 $4\tau_k=e_k+1$，采用残差加法和可选的输出范数保持，不额外引入需要学习的参数。

> 直观理解：不同层编码的信息层次不同，因此不强行共用一份记忆；只在新步骤开始时提醒模型，也比持续修改每个 token 的状态更克制。

**训练与推理**

训练阶段不做任何修改，也不需要为 TRAM 准备监督数据。推理开始时，将每个选定层的快速和慢速记忆初始化为零；模型接收 $4\mathcal{P}=(I,Q)$ 并照常生成。检测到步骤 $S_k$ 完成后，TRAM 从该步骤尾部窗口读取层内 FFN 输出，形成 $4s_k^{(\ell)}$，更新快慢记忆，对慢速记忆执行相对范数限制，并形成 $4m_k^{(\ell)}$。随后在 $4\tau_k=e_k+1$ 处，将记忆注入指定层的残差状态并按配置恢复原范数；模型基于修改后的状态继续生成。该循环持续到最终答案完成，之后清空当前样本的全部记忆状态。

**复现信息**

公平复现所需的关键选择包括：使用句末符和换行作为因果步骤边界；在每个步骤末尾读取至多 $w$ 个 token 的 FFN 输出并均值池化；默认敏感性分析显示适中的窗口 $w=8$ 最合适；每个注入层维护独立的快慢记忆，不跨层共享；仅在 $4\mathcal{L}_{\mathrm{inj}}=[L_{\min},L_{\max}]$ 内注入，文中层敏感性分析在相应实验模型上以 $4L_{\min}=28$ 最优；快速衰减因子分析以 $4\lambda_{\mathrm{fast}}=0.3$ 的总体结果最佳。还应实现式（10）的慢速记忆范数上限和式（13）的输出范数保持，并确保边界检测、记忆构造和注入均只使用当前位置以前的信息。原文节选未明确给出默认 $4\lambda_{\mathrm{slow}}$、比例上限 $r$、注入强度 $4\alpha$ 的具体数值及 $4L_{\max}$，这些参数不能据此节选自行补造。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 数学推理组包含 MathVision、MathVerse 和 MMK12-Math，用于检验模型能否在图表或视觉题面上持续保存并组合中间关系、约束与阶段性结论。原文未明确报告各数据集规模、所用划分及样本筛选规则。
- 科学推理组包含 MMK12-Phys、MMK12-Chem 和 MMK12-Bio，分别覆盖物理、化学和生物问题，用于检验轨迹记忆对多步科学推断的帮助。原文未明确报告各子集规模与评测划分。
- 通用视觉问答与幻觉评测包括 MMStar、MMMU，以及额外使用的 MMVP 和 MME-Hall。前两者测试跨领域视觉理解与推理能力，后两者专门检查模型是否忠实使用图像信息，从而判断隐藏状态干预是否引入视觉幻觉。原文未明确报告这些数据集的规模和具体划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

答案正确的样本比例，用于统一衡量数学推理、科学推理、通用视觉问答和幻觉基准上的任务表现。原文说明结果取三次运行的平均值，但未在节选中给出方差、置信区间或显著性检验。 （越高越好，因为更高的准确率表示模型在相应基准上给出更多正确答案；在 MMVP 和 MME-Hall 上，更高分也被作者用于表示更好的视觉忠实性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四个骨干模型 × 八个主要视觉推理基准：TRAM 对比 Vanilla Decoding

<div class="result-value" markdown="1">

作者报告，TRAM 在每一个骨干模型与基准的组合上都优于标准解码，覆盖数学、科学和通用视觉推理三类任务。由于节选未包含表 1 的具体分数，无法核验各设置的绝对提升幅度、相对提升比例或运行波动。

</div>

这说明收益并非只出现在单一数据集或单一模型家族上，为“轨迹派生记忆具有较广适用性”提供了直接证据。不过，这一结果只能证明 TRAM 相对同模型的标准解码更有效，不能单独证明提升必然来自长期信息保持，也不能排除额外推理时计算或特定超参数造成的影响。

<div class="result-source" markdown="1">

来源：Main Results，表 1 的文字总结

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with vanilla decoding, TRAM improves accuracy on all individual backbone–benchmark settings, covering mathematical, scientific, and general visual reasoning tasks.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### TRAM 对比其他免训练推理时方法，并按任务组汇总

<div class="result-value" markdown="1">

在 Qwen3-VL-4B 和 InternVL3.5-4B 上，TRAM 在数学、科学和通用视觉问答三个任务组均取得最佳平均结果；在 Qwen3-VL-8B 上，其数学与科学平均结果最佳，通用视觉问答平均结果第二。InternVL3.5-8B 上，作者称 TRAM 与最强基线保持竞争力，并称其任务组平均结果最佳，但节选未提供具体差值。

</div>

任务组平均值可降低单个数据集偶然波动对结论的影响，结果尤其支持 TRAM 对需要保存中间关系和约束的数学、科学推理有帮助。它并不表示 TRAM 在所有单项任务上都排名第一：作者明确指出 LEAD 在 Chemistry 和 MMMU 上略高，因此应将结论限定为整体和分组表现更强，而非逐项支配。

<div class="result-source" markdown="1">

来源：Main Results，表 1 的文字总结

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen3-VL-4B and InternVL3.5-4B, TRAM obtains the best average result in all three benchmark groups. On Qwen3-VL-8B, it achieves the best mathematical and scientific averages and the second-best General VQA average.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### MMVP 与 MME-Hall 幻觉评测：TRAM 对比 Vanilla Decoding

<div class="result-value" markdown="1">

作者报告，InternVL3.5-4B 和 InternVL3.5-8B 加入 TRAM 后，MME-Hall 与 MMVP 分数均提高；Qwen3-VL-4B 和 Qwen3-VL-8B 的结果相对标准解码大体稳定，仅有小幅变化。节选未给出表 2 的具体数值，因而无法判断变化大小及统计可靠性。

</div>

这一评测回应了隐藏表示注入可能导致模型偏离图像的问题：现有结果没有显示跨骨干的一致性视觉忠实度下降，InternVL 系列上甚至同时改善两项幻觉指标。但“没有系统性退化”不等于证明 TRAM 消除了幻觉；缺少具体差值、误差范围和更广泛幻觉类别时，只能作有限的安全性判断。

<div class="result-source" markdown="1">

来源：Hallucination Evaluation，表 2 的文字总结

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the two InternVL3.5 backbones, TRAM improves both MME-Hall and MMVP scores. On the two Qwen3-VL backbones, the results remain largely stable, with only small changes relative to vanilla decoding.

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

- Vanilla Decoding：完全不加入推理时干预的标准解码，是判断 TRAM 是否真正带来净增益的直接对照。
- VISTA：利用激活信号和早层视觉词元的输出分布引导生成，代表持续增强视觉证据的免训练方法；与其比较可区分“复用推理轨迹”与“强化原始视觉信息”的效果。
- MemVR：在不确定性触发的网络层中重新注入视觉特征，代表按需视觉回溯方法；该比较检验轨迹派生记忆是否比单纯重放视觉特征更适合长链推理。
- LEAD：根据不确定性在潜在推理与离散推理之间切换，并重新注入视觉锚点，是功能较综合的强基线；它用于检验 TRAM 在不增加训练的前提下能否与多机制视觉干预竞争。原文还评测了 ECRD，但受基线数量限制未单列。

**实验想回答的问题**

- 在不同模型家族、参数规模和任务类型上，TRAM 相比未经修改的标准解码以及其他免训练推理时干预方法，能否稳定提高多模态推理准确率？
- TRAM 对隐藏表示的干预是否会削弱模型对图像证据的忠实性，即推理准确率的提升是否以增加视觉幻觉为代价？

**实验实现**

实验覆盖 Qwen3-VL-4B、Qwen3-VL-8B、InternVL3.5-4B 和 InternVL3.5-8B 四个骨干模型。推理步骤按句末终止符和换行符切分，所有模型通过 vLLM 运行，最大生成长度为 $4096$ 个词元，采样温度为 $0.6$，准确率报告三次运行的平均值。该协议控制了主要生成配置，使不同解码方法可以在相同骨干上比较；但节选未说明随机种子、批大小、提示模板、答案抽取规则和统计显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过轨迹衍生的在线辅助记忆增强多模态模型对长推理过程中间结论的保留与整合。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`df01bcac30a6429293c47b6250070da3a8e0e0da26631883e77b7747dd40daf9`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
