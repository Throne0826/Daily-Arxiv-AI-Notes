---
title: "[论文解读] Deferred Exposure of Future Trajectories for Verifiable Reasoning in Autonomous Driving VLMs"
description: "[arXiv 2608.01755][自动驾驶] 论文揭示自动驾驶视觉语言模型训练中的“轨迹锚定偏差”，并通过AD-MCQ与DEFT-RLVR把未来轨迹从推理前可见的答案线索转化为推理后使用的可验证目标。"
arxiv_id: "2608.01755"
announcement_date: "2026-08-04"
primary_category: "autonomous_driving"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:57:40.237355+00:00"
source_sha256: "73ac655f0d1b69802258d20a2794f2bc62a7b223ade09f98d7289369f975de35"
tags:
  - "自动驾驶"
  - "VLM Reasoning"
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "视觉语言模型"
  - "视觉—语言—动作模型"
  - "思维链监督"
  - "轨迹锚定偏差"
  - "因果忠实性"
  - "候选轨迹"
  - "可验证奖励强化学习"
  - "延迟暴露未来轨迹"
  - "AD-MCQ"
  - "DEFT-RLVR"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">自动驾驶 · arXiv 2608.01755</p>

# Deferred Exposure of Future Trajectories for Verifiable Reasoning in Autonomous Driving VLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Zixuan Huang, Yang Zhou, Kaixuan Wang, Guli Zhang, Hongyan Xie, Yakun Zhu, Hao Geng, Yikun Ban, Deqing Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Beihang University；Zhejiang University；Tong University；VLM-only inference and controllable difficulty through candidate construction,AD-MCQprovides a flexible, scalable, and extensible foundation for future research on verifiable AD reasoning</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01755v1) · [PDF 下载](https://arxiv.org/pdf/2608.01755v1) · **关键词** 自动驾驶, 视觉语言模型, 视觉—语言—动作模型, 思维链监督, 轨迹锚定偏差, 因果忠实性, 候选轨迹, 可验证奖励强化学习, 延迟暴露未来轨迹, AD-MCQ, DEFT-RLVR<br>


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

论文揭示自动驾驶视觉语言模型训练中的“轨迹锚定偏差”，并通过AD-MCQ与DEFT-RLVR把未来轨迹从推理前可见的答案线索转化为推理后使用的可验证目标。

**不用术语来说**：自动驾驶模型需要先根据摄像头中的道路、车辆和交通规则判断应当怎样行驶，再说明判断依据；但现有数据制作流程常把车辆实际走过的未来路线提前交给负责生成推理文本的教师模型，使其可以看着答案编理由，甚至虚构画面中不存在的标志或因果证据。若完全隐藏路线并要求模型自行输出精确坐标，又会把道路决策与复杂的几何轨迹绘制混在一起，难以判断错误究竟来自推理还是坐标生成。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者识别并通过受控研究验证“轨迹锚定偏差”：提前暴露真实未来轨迹会诱使教师模型事后合理化既定动作，降低推理的因果忠实度，并在因果关系复杂的场景中产生更严重的幻觉。
- 作者提出AD-MCQ与DEFT-RLVR：前者用场景特定的显式候选轨迹把连续规划转化为可精确判定的选择问题；后者要求策略先依据场景形成并承诺决策，再展示候选轨迹进行落地与验证，从而避免候选集合成为新的推理捷径。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

主流自动驾驶视觉—语言—动作模型通常由大型视觉语言模型（VLM）与较小的动作专家组成：VLM读取道路图像等视觉观测，承担场景理解、高层推理和驾驶决策；动作专家则更擅长连续轨迹的几何预测。为增强VLM的驾驶推理能力，近期方法常用思维链（CoT）作为监督信号，但当教师模型在生成推理过程前已经看到日志中的真实未来轨迹时，它可能从已知结果反推理由，而不是依据场景证据作出决定。本文研究的核心背景因此不是一般性的轨迹预测，而是如何在保留明确轨迹监督的同时，使驾驶推理遵循“先根据场景决策、再用未来轨迹验证”的可核验范式。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉语言模型（VLM）**

能够联合处理图像与文本的模型，在本文的自动驾驶系统中负责理解道路场景、用语言表达推理过程并形成高层驾驶决策。它不同于动作专家，后者主要处理精确坐标、连续运动与车辆动力学。

</div>
<div class="concept-item" markdown="1">

**思维链监督（CoT supervision）**

训练数据不仅给出最终答案，还提供从场景证据到决策的中间推理文本。本文强调，推理文本即使与最终动作一致，也可能只是看到答案后的事后合理化，因而不一定具有因果忠实性。

</div>
<div class="concept-item" markdown="1">

**可验证奖励强化学习（RLVR）**

利用可自动检查的结果为模型提供强化学习奖励，例如候选轨迹是否选择正确，而不要求逐字模仿教师的全部推理。本文还结合问题特定的过程评价，但只有最终选择正确时才启用相应过程奖励。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是自动驾驶场景的视觉观测及相应问题，目标是让仅使用VLM的策略先依据可见场景形成候选不可见的推理与驾驶决定，随后在一组面向该场景构造的显式未来轨迹中选择最合适者。每条候选轨迹保留制动时机、速度曲线和横向几何等轨迹级差异，因此输出不是粗粒度的“左转、直行、停车”等元动作，也不是由VLM开放式生成连续坐标，而是一个可精确核验的候选选择。该设定假定日志真实未来轨迹可用于构造或判断候选答案，但不能在初始推理阶段作为前提暴露给策略；否则真实轨迹或候选集合都可能成为锚点，使模型绕过基于场景证据的因果推理。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\tau_{\mathrm{GT}}$**

日志记录的真实未来轨迹；此符号为便于说明问题而作的概念记号，原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$\mathcal{C}$**

针对当前场景构造的显式候选轨迹集合；原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$\hat{\tau}$**

模型从候选集合中选出的未来轨迹；原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$r$**

模型在看到候选轨迹之前，根据视觉场景生成的推理或决策表述；原文节选未给出正式符号。

</div>

</div>

**直接相关的工作**

- **基于真实轨迹条件的自动驾驶思维链监督**: 既有驾驶推理方法常让教师在已知日志未来轨迹的条件下生成CoT，从而使推理能够落实到具体驾驶结果；本文指出这种信息方向会诱发“轨迹锚定偏差”，即教师围绕已知结果事后组织理由，尤其可能在因果关系困难的场景中产生不忠实推理和虚构证据。
- **离散动作或轨迹表示方法**: 相关方法把连续驾驶行为编码为可由序列模型生成的离散词元，以缓解语言解码与连续控制之间的不匹配，但完整词表上的轨迹生成仍要求VLM合成精确几何，并可能导致任务特定记忆。本文改用场景特定、已解码的显式候选轨迹，把轨迹规划转化为精确选择，因此定位为推理验证接口，而非连续规划器的替代品。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

主流自动驾驶VLA系统通常由负责高层理解与决策的VLM和负责几何预测的动作专家组成，因此VLM能否从场景证据形成可靠、可泛化的驾驶判断，会直接影响下游规划。训练这种能力需要高质量的思维链监督，但监督文本不仅要与最终动作一致，还必须忠实反映模型从可见场景推导动作的因果过程；否则模型可能学会复述动作并编造依据，在最需要可靠判断的复杂场景中造成安全风险。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **真实轨迹条件化的思维链标注**：在生成自动驾驶思维链时，教师VLM同时接收观测场景和日志记录的真实未来轨迹，并围绕该轨迹生成解释及驾驶决策。这容易获得与示范动作一致的文本，也避开了让教师自行预测连续轨迹的困难。
- **隐藏真实轨迹的开放式轨迹生成**：教师只观察当前场景，先推导驾驶理由和决策，再自行生成未来轨迹，之后才能将预测与真实轨迹比较；这种流程符合“先求解、后验证”的推理蒸馏范式。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 真实轨迹条件化把待预测结果提前暴露给教师，形成轨迹锚定偏差：教师可能根据已知结果反向拼接理由，而不是从交通参与者、道路结构和规则等场景证据推出决策。由此产生的思维链虽然动作一致，却可能因果失真并包含虚构证据，作为监督数据时会把这种缺陷继续传递给策略模型。
- 开放式生成虽消除了答案泄露，却要求VLM同时完成高层行为选择、连续坐标构造、速度与制动曲线设计以及低层动力学处理。决策推理和精密几何合成因此相互纠缠，输出也难以进行稳定、精确的离散验证，不适合作为纯VLM可扩展的可验证推理接口。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一种同时满足三项要求的训练与评测接口：不在推理前泄露真实轨迹或候选答案，保留制动时机、速度变化和横向几何等轨迹级差异，并能用明确答案验证高层驾驶决策而无须VLM开放式生成连续坐标。即使把规划改造成候选轨迹选择，若一开始就展示选项，模型仍可能只比较候选的相对优劣，使候选集合取代真实轨迹成为新的锚点。

</div>
<div markdown="1"><span>核心问题</span>

能否设计一种仅依赖VLM的可验证自动驾驶推理机制，使模型先根据视觉场景独立形成驾驶决策，随后才接触显式候选轨迹并接受精确结果与过程监督，从而提高因果忠实的轨迹级决策能力，同时避免损害通用视觉能力？

</div>
<div markdown="1"><span>作者直觉</span>

候选轨迹把难以直接评分的连续规划变成有明确正确项的选择任务，但关键不只是“提供选项”，而是控制选项出现的时机。先让模型在看不到候选轨迹时解释场景并作出承诺，相当于先独立答题；之后再展示候选项，只用于把已形成的语义决策映射到具体路线并核验正误。这样，未来轨迹提供的是决策后的校验信号，而不是决策前可供倒推理由的答案线索。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文把自动驾驶规划改写为“先独立判断、后对照轨迹”的可验证推理任务。给定历史视觉场景 $V_i$，模型在第一轮看不到任何未来轨迹，只根据道路结构、交通参与者、信号状态及潜在冲突形成高层驾驶计划；第二轮才展示由真实未来及结构化困难干扰项组成的候选轨迹集合，模型将先前计划与候选项匹配并输出选择。AD-MCQ 因而把难以自动判定的开放式轨迹生成，转化为可用正确选项精确判分的多项选择问题；DEFT 则通过延迟候选曝光，防止模型先看到结果再编造理由。

训练时，DEFT-RLVR 在这一两阶段交互上采用可验证奖励强化学习：最终选择由精确匹配奖励 $R^{\mathrm{MCQ}}$ 检查，候选不可见阶段的推理由实例专属规则奖励 $R^{\mathrm{RUB}}$ 评价。规则由外部强视觉语言模型离线生成，因此既约束“答案是否正确”，也约束“答案出现前的场景推理是否有依据”，同时避免在线通用裁判带来的高计算成本。直观地说，方法像让驾驶员先在没有答案选项时说明应该减速、让行或转向，再打开若干路线图选择最符合该判断的一条；这样，路线图是事后验收标准，而不是诱导解释的提示。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造场景与候选轨迹

以真实未来对应的轨迹作为正确选项，并从码本中检索或采样显式航点轨迹作为干扰项；困难测试场景使用结构化困难干扰项，相似度约束和候选数量可用于控制题目难度。码本只承担候选检索，不要求 VLM 在自身词表中直接生成轨迹 token。

<div class="method-step__io" markdown="1">

**输入**：历史视觉输入 $V_i$、日志中的真实未来轨迹，以及用于检索候选的轨迹码本；每个 $V_i$ 由前左、前方和前右三个相机在 $2\,\mathrm{Hz}$ 下采样的四帧图像组成。<br>
**输出**：一个 AD-MCQ 实例，包括场景输入、暂不展示的候选轨迹集合、正确选项标识，以及训练时使用的实例信息。

</div>

**直观理解**：系统先把连续规划问题制成一道有标准答案的选择题。候选越多、错误路线越像正确路线，题目就越难。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选盲的因果规划

VLM 在 DEFT 的第一轮分析道路环境、交通参与者及潜在因果约束，生成候选不可见的高层计划和理由。该顺序强制推理方向从可观测场景指向驾驶决策，避免由已知未来反向合理化。

<div class="method-step__io" markdown="1">

**输入**：仅包含历史场景证据的 $V_i$，不包含真实未来轨迹或任何候选项。<br>
**输出**：第一轮场景推理与高层驾驶计划，例如保持、减速、让行或改变行驶方向及其依据。

</div>

**直观理解**：这一步相当于先收起答案，让模型仅凭现场情况作判断。即使之后的选择正确，第一轮文本仍可单独检查它是否真正看懂了场景。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 延迟曝光与轨迹匹配

模型保持第一轮决策语境，将计划中的高层动作、方向和交互约束与各候选轨迹的航点几何相匹配，并选出最一致的未来轨迹。该步骤只要求在明确选项间判别，不要求开放式合成精确坐标或处理低层车辆动力学。

<div class="method-step__io" markdown="1">

**输入**：第一轮计划以及第二轮才展示的显式候选轨迹集合。<br>
**输出**：离散候选编号及可选的匹配说明，可直接与正确选项进行精确比较。

</div>

**直观理解**：模型不用凭空画出一条毫米级路线，只需判断哪张路线图符合自己刚才的计划。这样能把“是否作出正确决策”与“是否擅长生成精确坐标”分开。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 双信号可验证强化学习

用 $R^{\mathrm{MCQ}}$ 对最终选项进行精确判分，并用 $R^{\mathrm{RUB}}$ 评价第一轮候选盲推理是否满足该场景的关键证据和决策要求；两类信号共同构成论文所称的 DEFT-RLVR 奖励并用于更新策略。由于规则预先生成，训练时不必为每个 rollout 调用昂贵的在线场景裁判。

<div class="method-step__io" markdown="1">

**输入**：完整的两轮 rollout、正确候选编号，以及由 Qwen3.6-35B-A3B 离线生成的实例专属推理规则。<br>
**输出**：经过强化学习优化的 VLM，使其同时提高轨迹选择正确性和候选曝光前推理的因果忠实度。

</div>

**直观理解**：最终答案像客观题一样自动判对错，推理过程则按每道题预先准备的评分要点检查。模型只有既会判断又会给出有场景依据的理由，才能获得完整的训练信号。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：论文的核心优化目标是同时强化最终决策正确性与决策前推理质量：$R^{\mathrm{MCQ}}$ 检查模型是否选择正确候选，$R^{\mathrm{RUB}}$ 检查候选不可见推理是否符合该实例的场景证据与决策规则。原文指出 DEFT-RLVR 使用式 (11) 定义的实例专属奖励 $R^{\mathrm{MCQ}}R^{\mathrm{RUB}}$，但所给章节没有包含式 (11) 的完整数学表达、组合方式或权重，因此 equations 保持为空，不能据相邻文本擅自补写加权和、乘积或其他目标。

优化层面的关键设计是从基础 VLM 直接进行 RLVR，而不是必须先用驾驶教师回答进行冷启动 SFT。精确选择奖励提供低歧义的结果监督，实例规则则阻止策略只学会猜选项；相比逐 token 模仿教师，奖励学习只强化满足目标的行为，意在减少模型整体输出分布向自动驾驶专用语体偏移，从而兼顾驾驶专门化与通用视觉能力保持。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. AD-MCQ 候选落地规划**

AD-MCQ 将规划表示为对显式未来轨迹候选的离散选择，候选由场景对应的正确轨迹与结构化干扰轨迹构成。候选数量和困难负例的相似度边界可调整，因而能系统控制细粒度轨迹辨别难度；同时，选择结果可以精确验证。

> 直观理解：它解决的是开放式轨迹输出难判分的问题：不再要求语言模型掌握庞大的轨迹 token 库，而是把几何轨迹放在模型外部，让模型集中判断哪条路线合理。

**2. DEFT 两轮延迟曝光协议**

DEFT 在第一轮仅输入场景并诱导高层计划，在第二轮才加入候选轨迹并要求匹配。其对照设置 JEFT 使用相同场景、候选、提示和总 token 预算，但从一开始就联合展示候选，因此两者主要区别是候选曝光顺序。

> 直观理解：该模块控制信息何时出现。候选不是永远隐藏，而是在模型作出独立判断后才出现，所以仍可利用真实未来进行验收，却不会让真实未来成为推理捷径。

**3. 实例专属规则监督**

Qwen3.6-35B-A3B 根据各场景离线产生实例专属 rubric，训练时据此形成 $R^{\mathrm{RUB}}$，并与精确选择奖励 $R^{\mathrm{MCQ}}$ 配合。它区别于共享通用规则的 $R^{\mathrm{GEN}}$：后者需要在线、场景条件化的 VLM 裁判，而实例规则把评分依据预先固化。

> 直观理解：不同场景的关键点不同，例如有的必须注意行人，有的必须注意并线车辆。实例专属评分表能检查模型是否提到了当前场景真正决定动作的证据，而不是套用泛泛的安全驾驶话术。

**训练与推理**

训练阶段首先将 Waymo Open E2E 与内部驾驶语料划分为 Train、Dev 和 AD-MCQ-500 Test，规模分别为 $5{,}000$、$100$ 和 $500$ 个场景；训练集遵循自然场景分布，Dev 与 Test 强调需要因果判断的困难场景，且 Dev 被刻意整理为更难的开发集。对每个训练实例，策略按 DEFT 协议先生成候选盲计划，再读取候选并完成选择；最终选择获得 $R^{\mathrm{MCQ}}$，第一轮推理依据离线实例规则获得 $R^{\mathrm{RUB}}$，随后以 RLVR 更新模型。论文还设置三类关键训练对照：JEFT+$R^{\mathrm{MCQ}}$ 用于检验候选提前曝光的影响，DEFT+$R^{\mathrm{MCQ}}$ 用于检验仅靠答案正确性是否足够，DEFT+$R^{\mathrm{MCQ}}R^{\mathrm{GEN}}$ 用于比较在线共享规则裁判与离线实例规则。

推理阶段不需要外部教师、在线奖励裁判或轨迹 token 解码器，只运行训练后的 VLM 两轮交互：第一轮根据多相机历史图像形成计划，第二轮接收显式轨迹候选并输出编号，因此属于 VLM-only inference。若采用论文的蒸馏替代方案，则由 Qwen3.5-397B-A17B 在相应曝光设置下生成监督目标：JEFT Distillation 模仿单轮“推理加选择”，DEFT Plan Only 只模仿第一轮计划，Full Interaction 模仿完整两轮过程，Mixed Targets 等量混合后二者；这些蒸馏版本是与 RLVR 比较的训练路径，不是 DEFT-RLVR 主流程的一部分。

**复现信息**

主实验以 Qwen3-VL-8B-Instruct 和 Qwen3.5-4B 为基础模型；Qwen3.5-397B-A17B 只用于生成蒸馏监督，Qwen3.6-35B-A3B 离线生成实例规则并担任推理过程裁判。数据构造参数报告为轨迹码本规模 $K=8192$、样本或轨迹相关总量 $N=489{,}042$；由于节选未进一步定义 $N$ 的精确对象，复现时应查验正文对应定义，不能仅凭数值推断。每个视觉样本包含三个前向相机的四帧历史图像。

公平比较 DEFT 与 JEFT 时，两者采用相同提示、场景和候选，并统一使用温度 $T=1.0$、top-$p=0.95$ 以及总计 $24{,}576$ token 的预算；DEFT 每轮最多 $12{,}000$ token。候选集合可通过五种候选数量和四种困难负例相似度边界重新采样，用于检查方法是否依赖固定选项几何。直接轨迹 token 生成实验使用共享码本作为反例：码本重建 ADE 为 $0.279\,\mathrm{m}$，但节选没有给出训练目标的完整公式，因此该实验不能据此补成方法方程。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 码本构建语料：约 $5.1\times10^5$ 条轨迹，来自 Waymo Open E2E 与一个内部驾驶语料库；二者统一表示为自车坐标系下 $5\,\mathrm{s}$、$2\,\mathrm{Hz}$、$T=10$ 个二维航点的未来轨迹。完整聚类规模为 $N=489042$，用于拟合离散轨迹原型，并研究码本规模与数据规模的影响。
- 同分布留出集：从码本拟合来源中保留 $5\%$，共 $25739$ 条轨迹，不参与聚类。其作用是检验原型是否只记住训练样本位置，并测量样本外 ADE、FDE 与码本利用率。
- 独立 Waymo 验证集：包含 $106360$ 条轨迹，作为跨来源评估集。它用于判断不同 $K$ 下的重建趋势是否仅适用于同一留出分布，而非用于训练或选择场景级驾驶策略。另有 AD-MCQ 下游划分：Train、Dev、Test 分别含 $5000$、$100$、$500$ 个场景，其中训练集遵循自然分布，Dev/Test 强调停车、急刹和急转等因果困难场景；但所给节选没有提供这些划分上的模型性能结果。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**平均位移误差（ADE）**

量化原始轨迹与其最近码本原型在全部 $T$ 个时间点上的平均空间偏差，单位为米；文中还报告 p50、p95、p99，以观察典型样本和长尾样本的误差。 （越低越好，因为较小 ADE 表示离散原型能更忠实地重建整段未来运动。）

</div>
<div class="metric-item" markdown="1">

**最终位移误差（FDE）**

量化原始轨迹与重建原型在预测终点处的距离，单位为米；它比 ADE 更集中地反映速度累计误差、停车位置或转向终点的偏差。 （越低越好，因为候选终点越接近真实未来，轨迹选项的几何含义越可靠。）

</div>
<div class="metric-item" markdown="1">

**码本利用率（Utilization）**

评估轨迹中至少匹配到一次的原型占全部 $K$ 个原型的比例，用于衡量码本容量是否得到数据支持。 （通常越高越好；在误差相近时，高利用率意味着较少原型被浪费。但该指标需与 ADE、FDE 联合判断，因为仅追求高利用率可能迫使码本过于粗糙。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 完整聚类语料 $N=489042$ 下选择 $K=8192$

<div class="result-value" markdown="1">

该配置在同分布样本外评估中取得 ADE $0.290\,\mathrm{m}$、FDE $0.516\,\mathrm{m}$，同时保留 $92.0\%$ 的原型利用率。作者据此将 $K=8192$ 作为 AD-MCQ 的默认码本规模。

</div>

这说明 $8192$ 个原型在几何精度与覆盖率之间形成了可用折中：轨迹平均可被较精细地近似，多数原型也确实会被未参与聚类的数据使用。它只支持“候选轨迹表示足够细且有数据覆盖”，不能证明 VLM 能从场景证据中选对轨迹，也不能直接证明闭环驾驶更安全。

<div class="result-source" markdown="1">

来源：Appendix C.5, Codebook Selection；对应 Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At the full clustering scale, it achieves 0.290 m out-of-sample ADE and 0.516 m out-of-sample FDE while retaining 92.0% utilization.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 固定完整语料并将码本从 $K=8192$ 扩大至 $K=16384$

<div class="result-value" markdown="1">

样本外 ADE 从 $0.290\,\mathrm{m}$ 降至 $0.252\,\mathrm{m}$，FDE 从 $0.516\,\mathrm{m}$ 降至 $0.446\,\mathrm{m}$，但样本外利用率从 $92.0\%$ 降至 $73.7\%$。因此，更大码本虽然提高重建精度，却产生更多缺乏样本外支持的稀疏原型。

</div>

结果揭示了分辨率与覆盖率的直接权衡：增加原型可更贴近罕见轨迹，但约四分之一原型在留出集上未被使用。作者选择 $K=8192$ 并不是因为误差已经饱和，而是为了避免把大量容量分配给不稳定或极少出现的运动模式；这一判断仍依赖当前数据分布与利用率定义。

<div class="result-source" markdown="1">

来源：Table 5, row $K=16384$

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

16384 | 0.242 | 0.252 | 0.297 | 0.426 | 0.446 | 99.4% | 73.7%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 独立 Waymo 验证集上的跨来源重建评估

<div class="result-value" markdown="1">

跨来源 ADE 随 $K$ 增大而单调下降，并相对同分布留出集保持约 $0.02$ 至 $0.05\,\mathrm{m}$ 的 ADE 偏移；例如 $K=8192$ 时 Cross ADE 为 $0.331\,\mathrm{m}$，而同分布 Out ADE 为 $0.290\,\mathrm{m}$。

</div>

独立数据仍呈现相同的规模趋势，说明“大码本带来更细重建”并非只在一个随机留出集上成立；小幅但持续的误差上升也表明存在数据源差异。该实验检验的是轨迹分布层面的迁移，不涉及图像域变化下的 VLM 感知与推理泛化。

<div class="result-source" markdown="1">

来源：Appendix C.3, Resolution as the Codebook Scales；数值见 Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The independent Waymo split exhibits the same monotonic resolution trend with a consistent 0.02–0.05 m ADE offset, showing that the comparison across K is not specific to a single held-out split.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 证据范围不完整：所给材料跳过了第 5 节实验正文及其模型结果表，因此无法可靠报告 AD-MCQ 答题性能、DEFT-RLVR 相对基线的增益、轨迹锚定偏差或幻觉严重度。上述结论仅覆盖附录中的码本表示与数据构造实验。
- 码本是独立于场景观测的纯运动学聚类，正确答案又由日志未来的最近原型定义；因此量化误差、日志行为并非唯一安全行为，以及内部语料库未公开等因素，都会限制基准标签的因果含义、可复现性与外部泛化。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原文未明确报告。

**实验想回答的问题**

- 轨迹码本能否在保持较低几何重建误差的同时，覆盖未参与聚类的真实驾驶轨迹，从而为 AD-MCQ 提供细粒度且可靠的候选轨迹？
- 码本规模 $K$ 与聚类语料规模 $N$ 如何共同影响重建精度、跨数据源泛化和原型利用率，作者据此选择 $K=8192$ 是否合理？

**实验实现**

轨迹首先展平为 $20$ 维向量，再使用 MiniBatchKMeans 聚类；批大小为 $10000$，迭代 $300$ 次，每个 $(N,K)$ 配置采用三个初始化种子，分别在拟合语料、同分布留出集和独立 Waymo 集上报告种子均值。码本仅用于离线量化和检索候选轨迹，VLM 看不到原型索引，只接收解码后的航点坐标，因此这些实验验证的是候选表示与构造基础，而不是端到端驾驶推理性能。AD-MCQ 的每个问题含 $M=6$ 个选项：一个量化后的日志未来和五个干扰项；Train 随机采样困难负例，Dev/Test 则加入尺度匹配、恒速外推和困难负例，以提高因果判别难度。所给材料未包含第 5 节的模型对比表，因此无法列出 DEFT-RLVR 相对其他训练方法的基线、准确率或通用视觉能力结果。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 码本规模消融：在 $N=489042$ 固定时将 $K$ 从 $256$ 增至 $16384$ | 样本内 ADE 随码本增大平滑下降，每次将 $K$ 加倍约降低 $15\%$；与此同时，样本外利用率在 $K\leq2048$ 时为 $100.0\%$，在 $K=4096$、$8192$、$16384$ 时依次降至 $98.7\%$、$92.0\%$、$73.7\%$。 | 该消融单独改变原型数量，隔离了“运动词表分辨率”的作用：更多原型持续改善几何重建，但超过一定规模后，一部分原型只描述数据稀疏区域，难以在新样本上得到使用。它支持选择中等规模码本，却没有直接检验候选数量或相似度区间对答题准确率的影响。 | Appendix C.3；Table 5 and Figure 4a<br><span class="experiment-evidence">Out-of-sample utilization remains complete through K=2048, is 98.7% at K=4096 and 92.0% at K=8192, but falls to 73.7% at K=16384.</span> |
| 聚类数据规模消融：固定 $K=8192$，将 $N$ 从 $50000$ 增至 $489042$ | 训练内与样本外 ADE 的差距从 $0.060\,\mathrm{m}$ 缩小到 $0.007\,\mathrm{m}$，样本外利用率从 $89.6\%$ 提升到 $92.0\%$；完整规模下样本内 ADE 为 $0.283\,\mathrm{m}$，样本外 ADE 为 $0.290\,\mathrm{m}$。 | 该消融保持码本容量不变，只增加用于估计聚类中心的轨迹数，因此主要测量数据支持对泛化的影响。差距缩小说明更多轨迹让原型中心不再过度贴合有限样本；但利用率提升较小，也说明仅增加数据不能完全解决高分辨率码本中的稀疏原型问题。 | Table 6, $K=8192$ and $N=489042$ row<br><span class="experiment-evidence">489,042 \| 0.283 \| 0.290 \| +0.007 \| 92.0%</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work introduces trajectory-choice verification and RLVR post-training to improve causally faithful VLM reasoning for autonomous-driving planning.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`73ac655f0d1b69802258d20a2794f2bc62a7b223ade09f98d7289369f975de35`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
