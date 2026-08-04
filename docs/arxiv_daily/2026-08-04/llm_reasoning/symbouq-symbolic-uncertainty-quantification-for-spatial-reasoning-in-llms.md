---
title: "[论文解读] SymboUQ: Symbolic Uncertainty Quantification for Spatial Reasoning in LLMs"
description: "[arXiv 2608.00417][LLM Reasoning] SymboUQ通过区分“推理语句能否被形式化”与“形式化后能否得到确定语义判定”，使符号验证证据能够按实际适用程度与神经表示、解码置信信号结合，从而估计大语言模型空间推理最终答案的可靠性。"
arxiv_id: "2608.00417"
announcement_date: "2026-08-04"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T11:04:35.108669+00:00"
source_sha256: "bce15eea0a19c78c90c559998fa7a1915c50b4e3f9db5aa13de9c09470020955"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "空间推理"
  - "不确定性量化"
  - "符号验证"
  - "符号化能力"
  - "语义确定性"
  - "推理链可靠性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.00417</p>

# SymboUQ: Symbolic Uncertainty Quantification for Spatial Reasoning in LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Dahai Yu, Lin Jiang, Rongchao Xu, Guang Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Florida State University, Tallahassee, Florida</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.00417v1) · [PDF 下载](https://arxiv.org/pdf/2608.00417v1) · **关键词** 大语言模型, 空间推理, 不确定性量化, 符号验证, 符号化能力, 语义确定性, 推理链可靠性<br>


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

SymboUQ通过区分“推理语句能否被形式化”与“形式化后能否得到确定语义判定”，使符号验证证据能够按实际适用程度与神经表示、解码置信信号结合，从而估计大语言模型空间推理最终答案的可靠性。

**不用术语来说**：大语言模型可能写出语言流畅、看似连贯的空间推理过程，但其中某个方向、包含或状态变化关系一旦出错，最终空间布局和答案就可能随之错误。词元概率主要反映模型生成文字时是否“自信”，不能直接判断这些空间关系是否真的支持结论；符号验证虽然能检查关系，却不一定对每条语句都能作出明确判断。因此，关键问题不是简单地问验证器能解析多少内容，而是判断它实际提供了多少可用于评价最终答案的确定证据。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出概念上的关键区分：可符号化性表示生成语句能否转换为验证器的形式语言，语义确定性表示执行该语句后能否得到“蕴含”或“矛盾”的确定结论，而不是“未知”或“不可评估”。该区分比单纯的解析覆盖率更准确地描述符号验证器的实际适用性。
- 提出SymboUQ框架：由顺序执行空间关系并提取可行性、冲突和修复证据的Layout Auditor，无需正确性标签即可概括有效可执行覆盖度的Determinacy Profile，以及依据验证器适用性融合约束、内部表示和解码信号的DARC组成。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型空间推理与不确定性量化的交叉领域。空间推理要求模型根据文本中的方向、包含关系或状态变化构造一致的空间布局，并据此回答问题；但语言流畅的推理链可能包含错误关系，甚至无法真正支持最终答案。不确定性量化的目标不是再次生成答案，而是估计现有最终答案的可靠性。传统方法主要依赖词元概率、模型自报置信度、多次采样的一致性、语义一致性或内部表示，这些统计信号可能与正确性相关，却不直接检查空间语义。形式验证器可以把推理步骤翻译为约束并执行，从而提供更直接的语义证据，但其适用范围有限：成功解析一条关系并不保证验证器能判定其成立或矛盾。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**不确定性量化**

不确定性量化是为模型输出估计可靠程度，而不只是给出一个离散答案。本文关注最终答案是否正确的可靠性估计，并综合生成概率、神经表示和符号执行证据。

</div>
<div class="concept-item" markdown="1">

**符号化能力**

符号化能力指生成声明能否被转换为验证器形式语言中的实体、关系和约束。它只说明声明可以表示和执行，不意味着验证器已经获得足够信息来判断其真假。

</div>
<div class="concept-item" markdown="1">

**语义确定性**

语义确定性指符号化声明执行后能否得到“蕴含”或“矛盾”这样的确定结论，而不是“未知”或“不可评估”。实体未落地、前提不足或先前声明造成上下文不一致，都可能使已成功符号化的声明仍不确定。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括可信的文本场景描述、冻结大语言模型生成的有序空间推理链及其最终答案，以及可从生成过程或模型表示中取得的辅助分数。系统假定空间关系能够在预定义形式语言中表示，但不假定每条生成声明都可解析、可落地或可被确定判决；可信场景与模型在推理链中新增的假设必须分开处理。目标是依次执行推理声明，将每条声明相对于明确上下文归为蕴含、矛盾、未知或不可评估，并据此估计最终答案正确的可靠程度。关键问题不是单纯计算解析覆盖率，而是同时判断“多少声明能够符号化”以及“其中多少声明能产生确定语义证据”；当后者较低时，约束证据的信息量有限，需要由表示和解码信号补充。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Kuhn et al. (2023), Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation**: 代表基于多次生成及语义一致性的输出级不确定性方法。它能够利用不同表述之间的语义分歧估计风险，但不直接执行推理链中的空间关系，因此无法确认中间关系是否在给定场景中成立并支持最终结论。
- **Lightman et al. (2024), Let’s verify step by step**: 代表对中间推理步骤进行细粒度评估的过程监督与学习式验证路线。本文同样重视推理过程，但进一步采用显式空间约束执行，并专门处理形式验证器只能覆盖部分声明、且可解析声明未必具有确定语义结论的问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在文本空间推理任务中，一条错误的方向关系、包含关系或状态转移就可能破坏整个空间配置，但模型仍可生成流畅且貌似合理的解释。实际应用需要估计最终答案是否可信，且这种估计应检查推理链是否在空间语义上支持结论，而不能只依据答案措辞或生成概率。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **统计与神经不确定性估计**：利用模型口头报告的置信度、词元级概率、重复采样之间的一致性、答案的语义一致程度或模型内部表示来预测正确性；过程监督和学习式逐步验证器则进一步为中间推理步骤打分。
- **形式化或符号验证**：将生成的关系语句解析为预定义形式语言中的约束，再按空间规则执行，以判断语句相对于当前场景是被蕴含、与场景矛盾，还是无法确定。它能够直接检查底层空间语义，而不只利用与正确性相关的统计特征。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 统计置信、语义一致性和学习式验证分数可能与答案正确性相关，却未必直接检查空间关系是否成立；因此，模型即使对一条语义错误但表达流畅的推理链表现出高置信，也可能被误判为可靠。
- 符号验证的解析成功不等于获得了有效证据：实体可能没有被场景绑定，已有前提可能不足，或先前生成语句已使当前上下文不一致。此时即使关系可以形式化，执行结果仍可能是“未知”或“不可评估”，所以解析覆盖率会高估验证器对可靠性估计的实际贡献。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有方法缺少一种面向整条推理轨迹的适用性刻画：它需要分别度量语句能否进入形式系统以及进入后能否产生确定判定，还要显式处理未解析语句、语义未决语句、上下文失效，以及依赖先前生成假设所得的条件性结论。在此基础上，仍需解决如何随轨迹而变地融合符号证据与神经、解码证据。

</div>
<div markdown="1"><span>核心问题</span>

能否从大语言模型生成的有序空间推理轨迹中，先识别符号验证在每条语句和整条轨迹上的真实适用程度，再据此组合约束验证、内部表示与解码置信信号，以更可靠地预测最终答案是否正确？

</div>
<div markdown="1"><span>作者直觉</span>

符号证据的价值取决于它是否真正“判得出来”：当多数关系都能在一致场景中得到蕴含或矛盾判定时，约束执行直接检验了推理语义，应承担更大权重；当大量关系只能解析却无法确定时，强行把它们视作通过会制造虚假置信，此时模型内部状态和生成概率可作为补充。因而，先用确定性画像判断验证器在当前轨迹上有多少有效证据，再进行条件化融合，比对所有轨迹固定使用同一种分数组合更合理。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SymboUQ把冻结语言模型生成的空间推理轨迹转化为最终答案可靠性，而不是重新生成或纠正答案。给定场景描述与问题组成的输入$x=(\eta,q)$，冻结模型$M$生成轨迹$r=M(x)$；系统先把$r$拆成按生成顺序排列的声明，再由Layout Auditor在形式化空间关系系统中逐条解析、执行并记录可行性、蕴含、矛盾、未知和修复证据。随后，Determinacy Profile分别度量“文本能否进入验证器”的可符号化程度$\pi(r)$与“进入后能否得到确定语义结论”的确定性$d(r)$，并以$\delta(r)=\pi(r)d(r)$表示有效可执行覆盖率。最后，DARC依据这些适用性信号，组合约束、模型表示和解码概率三类基础分数，输出最终答案正确的校准概率。

关键设计是把“解析成功”与“验证有效”分开：一句话即使能被翻译为空间关系，也可能因实体未落地、上下文不可行、前缀冲突或规则不充分而只能得到unknown或not-evaluable。通俗地说，Layout Auditor像按顺序检查推理草稿的几何审计员，Determinacy Profile判断这名审计员实际看懂并判清了多少内容，DARC再决定审计证据、语言模型内部信号和生成概率各应占多大权重。该框架因此不会把验证器沉默误当成推理正确，也不要求符号验证器覆盖任意自然语言空间推理。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 轨迹生成与声明结构化

将包含$L$个词元的轨迹$r$分解为保持原始顺序的$K$个声明$\mathcal{C}(r)=((c_k,t_k,m_k))_{k=1}^{K}$，其中$c_k$是声明文本，$t_k$标记声明在推理中的类型，$m_k$保存与声明位置或对齐有关的元信息。主实验采用结构化声明以控制声明与词元的对齐，部署时也可对自由形式思维链自动分段。

<div class="method-step__io" markdown="1">

**输入**：输入$x=(\eta,q)$，其中$\eta$是场景描述，$q$是空间问题；冻结语言模型$M$及其生成的推理轨迹$r=M(x)$。<br>
**输出**：有序声明序列及其与原轨迹、词元和最终结论的对应关系。

</div>

**直观理解**：先把一整段推理切成可逐句检查的步骤，并保留先后次序；否则系统只能评价整段文字，无法定位前面的假设如何影响后面的结论。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 空间声明规范化与顺序审计

审计器将别名规范化到七类关系族，并对每个可解析声明抽取实体与关系；方向关系通过两个相互独立的差分约束系统检查横、纵轴可满足性，其他受支持关系通过逆关系、合法对称规则、受限传递闭包和不相容关系对进行推理。声明按顺序在上下文$A_k$中执行，聚合为entailed、contradicted或unknown，并记录首次冲突、整体可行性和有界修复代价等特征。

<div class="method-step__io" markdown="1">

**输入**：场景中的可信空间事实$D$、有序声明$c_1,\ldots,c_K$以及验证器支持的空间关系词表。<br>
**输出**：每条声明的解析、落地、可行性、语义状态与修复证据，以及汇总后的声明级和轨迹级审计特征。

</div>

**直观理解**：审计器把“甲在乙左边”一类文字改写成可计算约束，再检查新声明是否由已有关系推出、与它们冲突或暂时无法判断。它只对实现的形式语言和规则精确，并不声称能完整理解所有自然语言空间表达。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 确定性画像构造

计算可符号化率$\pi(r)$，再在已符号化内容上计算得到确定语义裁决的比例$d(r)$，并构造有效适用性$\delta(r)=\pi(r)d(r)$；画像不使用裁决的正负方向，也不使用最终答案正确标签。默认确定性设计纳入因前缀阻塞而无法评价的声明，以免把缺失覆盖误作正确证据。

<div class="method-step__io" markdown="1">

**输入**：全部声明的解析结果、语义状态和因前缀问题而不可评价的记录。<br>
**输出**：无标签的轨迹级Determinacy Profile，包括$\pi(r)$、$d(r)$、$\delta(r)$及相关适用性特征。

</div>

**直观理解**：$\pi(r)$回答“审计器读懂了多少”，$d(r)$进一步回答“读懂后真正判清了多少”。两者分开后，一个大量解析成功但多数结论仍未知的轨迹不会被误认为得到了充分验证。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 适用性感知的可靠性组合与校准

DARC先在目标验证集上筛选并统一基础分数方向，再构造原始分数块$h_{\mathrm{score}}$、可符号化交互块$h_{\mathrm{sym}}$和确定性交互块$h_{\mathrm{det}}$，学习不同验证器适用状态下各分数与正确性的关系；模型设计、正则化与后处理校准均在验证集选择。推理时只需计算当前轨迹的缓存特征和画像，通过已拟合组合器及校准器得到概率。

<div class="method-step__io" markdown="1">

**输入**：约束型基础分数、冻结模型表示上的神经基础分数、词元概率或采样产生的解码型分数，以及轨迹的确定性画像。<br>
**输出**：最终答案正确性的校准可靠性估计，可用于排序、拒答或选择性预测。

</div>

**直观理解**：不同信号在不同数据上会失灵，因此不能始终固定平均。DARC像一个按“符号审计当前是否真正适用”动态调权的裁判，但这种抑制由训练出的交互权重实现，并非硬性门控。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 有效语义适用性

$$
\delta(r)=\pi(r)d(r)
$$

**符号说明**

- $r$：冻结语言模型生成的完整推理轨迹。
- $\pi(r)$：轨迹的可符号化程度，即声明能够被解析并表示在审计器形式语言中的覆盖比例。
- $d(r)$：语义确定性，即相关执行结果中得到entailed或contradicted等确定裁决、而非unknown或not-evaluable的比例。
- $\delta(r)$：有效可执行覆盖率，用于表征符号验证器对当前轨迹实际提供确定语义证据的程度。

<div class="equation-explanation" markdown="1">

**直观理解**：该式要求一段内容既能被送入验证器，又能在执行后产生明确裁决，才算有效覆盖。若大量声明无法解析，$\pi(r)$会降低；若虽能解析却因冲突、落地不足或规则能力有限而无法判定，$d(r)$会降低，因此单纯提高解析率不能伪装成验证能力提高。<br>
**原文位置**：RQ 3“Determinacy Characterizes Applicability”；原文同时说明该量用于Equation (14)中的适用性交互。

</div>

</div>

<div class="equation-block" markdown="1">

#### 上下文保持的矛盾修复代价

$$
R_k(z)=\min_{S\subseteq P_k}|S|\quad\text{s.t.}\quad\operatorname{SAT}\bigl(D\cup(P_k\setminus S)\cup\{z\}\bigr),\qquad P_k=A_k\setminus D
$$

**符号说明**

- $R_k(z)$：第$k$个声明中的矛盾关系$z$相对于此前生成上下文的最小修复代价。
- $z$：当前被审计器判定为矛盾的关系实例。
- $D$：来自原始场景描述、始终保留的可信关系集合。
- $A_k$：检查第$k$个声明时的假设上下文，包含可信场景关系以及此前可符号化的生成声明。
- $P_k$：第$k$步之前由模型生成的关系实例多重集，即从$A_k$中排除可信场景关系$D$后的部分。
- $S$：为恢复可满足性而从此前生成关系中删除的实例子集。
- $\operatorname{SAT}(\cdot)$：判断给定空间约束集合是否可同时满足的谓词。

<div class="equation-explanation" markdown="1">

**直观理解**：修复搜索始终保留场景事实$D$，只允许撤回模型先前生成的关系，并寻找使当前关系$z$可与剩余上下文共存的最少删除数。该值衡量冲突有多深：删除一条旧推断即可修复的局部口误，与需要撤回多条前提的系统性矛盾应提供不同的可靠性证据。<br>
**原文位置**：Appendix B.2, Equation (23)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：SymboUQ不是端到端微调语言模型，也不以符号规则替代生成模型；主干$M$和用于产生表示特征的模型保持冻结。原文节选未给出DARC损失函数的显式公式，因此不能据此指定未报告的优化目标；可确定的是，监督式基础评分器在源数据StepGame上训练，DARC利用每个目标数据集的验证集正确性标签筛选、定向并组合候选分数，同时选择正则化和组合设计，之后再拟合后处理概率校准器。Determinacy Profile和Layout Auditor不使用中间声明标签，另一个Qwen3-1.7B裁判提供的声明标签只用于训练监督式基础评分器，而不进入审计器执行。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Layout Auditor**

该模块支持方向、包含、距离、拓扑、位置和路径等七类关系族；方向部分把二维关系拆成横轴与纵轴差分约束，两个系统都可满足时才认为布局可行，符号部分则迭代计算规则闭包并检查不相容关系。逆关系用于方向与包含关系，对称性只在语义有效时使用，传递性仅用于inside和contains，near与touching不会被错误地传递；含多个关系的声明采用保守聚合，即任一关系矛盾则整句contradicted，全部蕴含才是entailed，蕴含与未决混合则为unknown。

> 直观理解：这些限制防止验证器把词义相似错误升级成逻辑规则，例如“甲靠近乙、乙靠近丙”不能推出“甲靠近丙”。保守聚合则避免一句复杂声明只验证了一部分，就被当作整句已经成立。

**2. Determinacy Profile**

画像明确区分可符号化$\pi(r)$与语义确定性$d(r)$，并通过$\delta(r)=\pi(r)d(r)$刻画整个轨迹上得到确定裁决的有效比例。它只描述执行覆盖，不编码entailed或contradicted的极性，因此本身不是置信度分数，也不需要最终正确性标签；默认设计还把prefix-blocked声明计入覆盖缺口。

> 直观理解：解析成功只表示验证器获得了输入接口，不表示验证器已经提供证据。确定性画像专门描述“这次验证到底工作了多少”，让后续组合器知道何时应信任或弱化约束分数。

**3. Determinacy-Aware Reliability Composer（DARC）**

DARC组合三类互补证据：约束分数反映轨迹与空间规则的一致性，表示分数来自冻结语言模型的缓存激活，解码分数来自词元概率或多次生成。除保留原始分数块$h_{\mathrm{score}}$外，它还加入分数与$\pi(r)$、$\delta(r)$等画像量的交互，使同一个约束分数在高、低验证器适用性下可对应不同的最终正确概率；约束证据仍可经原始分数块直接进入模型，因此低$\delta(r)$并不会在结构上强制其权重为零。

> 直观理解：单一证据源不存在跨数据集稳定优势：概率高可能只是语言流畅，神经探针可能发生领域偏移，符号分数又受验证器覆盖限制。DARC利用少量目标域验证标签学习何时采用哪类证据，而不是假定某一种分数永远可靠。

**训练与推理**

训练阶段首先用冻结主干生成源域与目标域轨迹，并从文本、词元概率和缓存激活中提取约束型、解码型与表示型候选分数；监督式基础评分器在StepGame上拟合后冻结。对每个目标数据集，系统在其验证集上运行Layout Auditor并计算$\pi(r)$、$d(r)$和$\delta(r)$，按统一协议筛选候选分数、校正分数方向，拟合包含$h_{\mathrm{score}}$、$h_{\mathrm{sym}}$与$h_{\mathrm{det}}$的DARC，并以验证表现选择设计、正则化和后处理校准。

推理阶段输入新的$(\eta,q)$，冻结模型只生成一次待评价的主轨迹；系统结构化其声明、顺序执行审计、汇总画像及三类基础分数，再由已拟合的DARC和校准器输出最终答案正确概率。默认审计上下文$A_k$把此前所有可符号化声明当作工作假设，因此entailed表示“相对于场景与生成链前置承诺成立”，并不总是完全扎根于场景；这保留了自相矛盾、首次冲突和修复代价等诊断信号，但也可能让依赖未证实前提的后续结论获得条件性蕴含。论文另以仅接纳此前已蕴含声明的$T_k$做端到端变体，以检验结果是否主要依赖假设传播。

**复现信息**

公平复现需要保持三点。第一，所有关系别名必须先规范化，方向关系使用两个轴的差分约束，规则闭包严格限制逆关系、对称性和传递性；审计结果只对实现的关系语言与规则精确，不能解释为通用自然语言证明。第二，矛盾修复只枚举删除一至三个先前生成关系的子集，无法在该预算内修复时以四作为有界特征值，非矛盾声明的修复特征按约定设为零；因此该特征在真实距离超过三时不是精确最小距离。第三，缓存流程从部署时可见文本重建审计特征并检查维度，默认产生23个声明级特征和16个轨迹级特征；主实验依靠结构化声明保证声明与词元对齐，自由形式轨迹则需要额外自动分段。

还需区分默认$A_k$与更保守的$T_k$：$A_k$保留此前可符号化但未必已证实的模型声明，便于发现生成链内部冲突；$T_k$只纳入此前在递归接地上下文中已蕴含的声明，更接近证明检查，但会丢失由未证实假设触发的后续冲突。DARC中的$\delta(r)$交互是附加于原始分数块的学习项，不是乘法门控，所以低确定性只可能通过拟合权重弱化约束证据，不能从模型结构上保证约束分数被关闭。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- StepGame：受控方向链推理数据集，答案空间为九类方向；训练集、验证集和测试集分别含10000、300和3000个样本。它是唯一的源域，基础评分器参数仅在其训练数据上学习，用于检验模型能否从规则清晰、推理深度可控的空间关系中学习不确定性证据。
- SpaRTQA：包含较丰富自然语言场景的空间问答数据集，答案空间为四类关系；原文未列训练集，验证集和测试集分别含300和3000个样本。它作为目标域，用于检验从规则化方向链获得的可靠性评分能力能否迁移到表达更自然、场景更复杂的问题。
- SpaRTUN：覆盖多种空间关系族，并允许集合形式答案；原文未列训练集，验证集和测试集分别含300和3000个样本。它用于检验方法面对多关系及非单标签输出时，是否仍能有效评估最终答案可靠性。其余两个目标基准为三分类空间自然语言推断SpaceNLI和具有显式关系组合路径的五分类SpaRP；受列表上限约束，此处不再逐项展开。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**AUROC**

衡量随机抽取一条最终答案正确的轨迹和一条最终答案错误的轨迹时，前者获得更高可靠性分数的概率；分数相同时按一半计入。它主要评价排序和区分能力，不直接保证输出概率已经校准。 （越高越好，因为这表示正确答案更经常排在错误答案之前；随机排序的参照通常接近$0.5$。）

</div>
<div class="metric-item" markdown="1">

**类别平衡Brier损失**

分别在正确类集合$\mathcal{P}$和错误类集合$\mathcal{N}$内计算预测概率$s_i$的平方误差，再令两类各占一半权重。该设计防止类别不平衡使多数类主导结果，评价的是类别对称的概率误差，而不是实际部署类别先验下的严格适当概率评分。 （越低越好，因为较低值表示对正确类和错误类的预测概率平均更接近各自真实标签。）

</div>
<div class="metric-item" markdown="1">

**Judge一致率与Cohen's $\kappa$**

一致率统计Qwen3-1.7B与人工或大型参考Judge给出相同中间声明标签的比例；Cohen's $\kappa$进一步扣除随机一致的影响。二者验证中间监督信号的可靠程度，而不衡量最终答案预测性能。 （越高越好，因为更高的一致率和$\kappa$表示轻量Judge的声明标签更接近独立参考判断。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 四个冻结骨干与五个空间推理基准构成的20个设置，指标为AUROC；每个设置均与该设置中AUROC最高的外部非随机基线比较。

<div class="result-value" markdown="1">

作者报告SymboUQ的平均相对AUROC提升约为$8\%$。

</div>

这表明SymboUQ通常能更好地把最终答案正确的轨迹排在错误轨迹之前，并且比较对象是逐设置选出的最强外部基线，定义较保守。不过，节选未提供各数据集、各骨干的完整分数、置信区间或显著性检验，因此不能据此断言每个设置都提升，也不能判断绝对增益大小。

<div class="result-source" markdown="1">

来源：Appendix D.4, Metrics and Statistical Analysis

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This gives roughly 8% higher AUROC and 7% lower class-balanced Brier loss.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 同一20个骨干—数据集设置，指标为类别平衡Brier损失；每个设置均与该设置中损失最低的外部非随机基线比较。

<div class="result-value" markdown="1">

作者报告SymboUQ的平均相对类别平衡Brier损失降低约$7\%$。

</div>

该结果说明方法不仅改善正确与错误答案的排序，还减少了两类等权条件下的概率平方误差。但类别平衡Brier改变了评估中的类别先验，不能直接解释为真实部署分布下概率校准改善$7\%$；原文也明确将其称为损失，而非经验部署分布上的适当概率评分。

<div class="result-source" markdown="1">

来源：Appendix D.4, Metrics and Statistical Analysis

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This gives roughly 8% higher AUROC and 7% lower class-balanced Brier loss.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen3-1.7B中间声明Judge与人工标注者的可靠性比较；每个基准随机抽取100条轨迹，五个数据集合计500条轨迹、1426个声明。

<div class="result-value" markdown="1">

作者报告五个基准上的人工一致率均超过$93\%$，Cohen's $\kappa$均不低于$0.83$；表7的具体范围为一致率$93.1\%$至$97.6\%$、$\kappa=0.83$至$0.94$。

</div>

这支持轻量Judge可作为中间声明标签来源，并表明一致性并非主要由随机巧合造成。它不证明Judge标签完全正确，也不证明SymboUQ的最终可靠性分数优于基线；该实验验证的是评估管线中的标签质量。大型LLM参考Judge在完整评估池上的$\kappa$均至少为$0.80$，提供了额外的跨模型一致性证据。

<div class="result-source" markdown="1">

来源：Appendix D.2, Table 7

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Human agreement exceeds 93% with κ≥0.83 on every benchmark, and the three LLM references have κ≥0.80 throughout.

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

- 解码统计基线，以MCP为代表：对声明所对应生成token的最高预测概率取平均，并将其转换为正确性分数；同组还包括Perplexity、Token Entropy和CCP。该比较检验仅依赖语言模型局部token置信度是否足以判断整个空间推理结论。
- 重复采样基线，以Semantic Entropy为代表：每个输入额外进行$K=10$次随机解码，按双向蕴含关系聚类不同生成结果，再计算语义类别熵；同组还包括SelfCheckGPT和P(True)。它是重要比较，因为它用多次生成的一致性估计不确定性，但计算成本高于SymboUQ所依赖的单条贪心轨迹。
- 神经探针基线，以Neural-Seq为代表：使用Transformer表示带标记的声明，再由双向LSTM按生成顺序整合，但不输入Layout Auditor特征；同组包括Factoscope、UHead和MLP。Neural-Seq在结构上与顺序推理建模相匹配，因此可用于判断性能是否只来自神经序列编码能力。
- 符号基线，以Constraint为代表：联合声明级与轨迹级审计特征、冻结token表示及蕴含或矛盾规则的直接残差；另有固定规则的Constraint-Rule和不使用语言模型激活的Constraint-Only。该组是最直接的比较，用于区分SymboUQ的“按验证器适用性组合证据”与单一约束评分器的贡献。

**实验想回答的问题**

- 在五个空间推理基准和四个冻结语言模型骨干上，SymboUQ给出的最终答案可靠性分数，能否比解码统计、重复采样、神经探针和纯符号约束等外部基线更准确地区分正确答案与错误答案，并同时降低类别平衡的概率误差？
- 实验中的可靠性提升是否来自可执行语义证据，而非更换生成模型、访问参考答案或针对目标任务微调推理模型；用于标注中间推理声明的轻量Judge是否具有足够的一致性？

**实验实现**

四个生成骨干Mistral-7B-Instruct-v0.3、Llama-3.1-8B-Instruct、Gemma-2-9B-it和Qwen3-8B均被冻结，各自生成独立推理轨迹并缓存特征；Qwen3-1.7B仅为中间推理声明提供验证标签。最终答案正确性不由Judge决定，而是将解析后的答案经确定性规范化后与基准答案匹配；Judge的输入不含参考答案及结论正确性标签，从而降低标签泄漏风险。基础评分器参数只从StepGame学习；每个目标数据集的300例验证集仅用于证据组合、归一化、聚合选择和单调Platt校准，配置冻结后测试集只评估一次。所有方法使用相同的生成轨迹和缓存输出，声明级分数统一通过结论、均值或最小值摘要为最终答案分数。重复采样方法是例外：每个输入额外生成$K=10$条随机解码。论文所称相对提升是在20个“骨干—数据集”设置中，逐设置选择最佳非SymboUQ、非Random外部基线后计算，再对相对改进取平均。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出基于符号验证器的空间推理轨迹可靠性估计方法，核心贡献是推理过程的语义验证与不确定性量化。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`bce15eea0a19c78c90c559998fa7a1915c50b4e3f9db5aa13de9c09470020955`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
