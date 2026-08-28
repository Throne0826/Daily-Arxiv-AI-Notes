---
title: "[论文解读] SCIT: Testing Causal Cache Carriers in Latent Chain-of-Thought Models"
description: "[arXiv 2608.27265][LLM 机制与可解释性] 原文未明确报告。"
arxiv_id: "2608.27265"
announcement_date: "2026-08-28"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:31:15.932456+00:00"
source_sha256: "ed230a354667ced9cd5ea479c56cde0959b284317e116644b7c06b840a2b4eea"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "潜在思维链"
  - "机制可解释性"
  - "键值缓存"
  - "交换干预"
  - "反事实推理"
  - "因果载体定位"
  - "SCIT"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2608.27265</p>

# SCIT: Testing Causal Cache Carriers in Latent Chain-of-Thought Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Yi Ding, Lijun Huang, Menglin Yang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: The Hong Kong University of Science and Technology (Guangzhou)</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.27265v1) · [PDF 下载](https://arxiv.org/pdf/2608.27265v1) · **关键词** 潜在思维链, 机制可解释性, 键值缓存, 交换干预, 反事实推理, 因果载体定位, SCIT<br>


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

本文处于潜在思维链与机制可解释性的交叉领域。传统思维链把中间推理写成可读文本，但文本解释未必忠实反映模型真正使用的计算；潜在思维链则把部分中间推理移入连续隐藏状态，虽可减少冗长草稿，却使研究者无法直接观察推理过程。因此，本文关注的不是“能否从内部状态读出某种信息”，而是更严格的因果问题：在自回归 Transformer 的潜在推理过程中，究竟是隐藏状态、注意力键缓存、值缓存，还是某段更广的历史缓存，实际承载并传递了改变答案所需的反事实计算。作者将这一问题视为载体识别，而非一般任务性能评测。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**潜在思维链（latent chain-of-thought）**

模型不把全部中间推理生成为文字，而是在连续向量状态中推进若干推理步骤。这样更紧凑，但人们不能通过阅读推理文本直接判断其因果忠实性。

</div>
<div class="concept-item" markdown="1">

**Transformer 的键值缓存（K/V cache）**

自回归生成时，每一层会保存先前位置产生的键和值，以避免后续步骤重复计算；键主要参与注意力匹配与路由，值提供被聚合的内容。分别替换键缓存或值缓存，可以检验反事实影响主要来自“从哪里读取”还是“读取什么内容”。

</div>
<div class="concept-item" markdown="1">

**交换干预与因果充分性**

交换干预把来源样本的某个内部对象移植到接收样本中，并观察输出是否转向来源所规定的反事实答案。若仅替换该对象便能稳定产生目标变化，它对该效应具有因果充分性；但要主张其被选择性需要，还必须结合匹配破坏等必要性控制。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是具有潜在推理步骤的自回归 Transformer，主要问题设置采用答案可精确计算的受控算术反事实。每个测试单元包含来源样本与接收样本，并预先知道接收者原答案、来源定义的反事实答案、语义控制答案及随机负例；运行接收者时，SCIT 将来源运行中的指定缓存片段移植到接收者对应位置，并系统改变所替换的缓存区段、键或值成分、隐藏状态是否联动以及来源语义。输出不是单个补丁分数，而是一个载体判定图：根据接收者是否转向反事实目标，以及自由生成、解码验证和匹配破坏等控制是否通过，将测试单元标记为活跃载体、载体迁移或不作机制判定。该设置假定来源与接收者之间能构造精确反事实，因此受控合成算术在这里是因果识别工具，而不代表作者声称具有广泛基准覆盖。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$K$**

注意力键缓存；决定当前查询与既往位置的匹配及信息路由。

</div>
<div class="notation-item" markdown="1">

**$V$**

注意力值缓存；保存注意力读取并聚合的内容。

</div>
<div class="notation-item" markdown="1">

**$K/V$**

键缓存与值缓存的合称；SCIT 可联合替换二者，也可拆分替换以定位因果载体。

</div>

</div>

**直接相关的工作**

- **潜在步骤的因果分析（Li et al., 2026）**: 该类工作把整个潜在步骤作为可干预变量，用于判断某一步是否影响答案；SCIT进一步追问该效应由潜在步骤内部的哪一种 Transformer 对象实现，例如键缓存、值缓存、隐藏状态或特定缓存区段。
- **Tuned Lens 与 Patchscopes（Belrose et al., 2023；Ghandeharioun et al., 2024）**: 这些方法把内部表示解码为词元分布或自然语言解释，回答信息能否从状态中恢复；SCIT将解码仅作为辅助验证，因为“可被读出”不等于模型在实际计算中因果使用了该信息。

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

SCIT（Suffix Cache Interchange Test，后缀缓存互换测试）是一套用于定位潜在思维链模型中“反事实计算由哪个内部对象承载”的因果诊断协议，而不是新的训练算法。它先为同一计算结构构造接收问题 $r$ 与来源问题 $s$：接收问题给出原答案 $a_r$，来源问题则提供经过验证的中间量，使其与接收问题未改变的信息组合后得到反事实答案 $a_{cf}$。模型分别运行到潜在推理步骤 $t$，随后把来源轨迹中特定位置、层和组件的缓存切片移植到接收轨迹，继续接收端生成，并检查答案是否从 $a_r$ 转向 $a_{cf}$。被测试对象包括潜在尾部、提示前缀和完整缓存，以及其中的键缓存、值缓存和当前隐藏状态。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 构造精确的来源—接收反事实对

利用已知的两步算术程序验证来源中间量，并把它与接收问题保留的信息组合，确定唯一的反事实答案 $a_{cf}$；同时构造同答案、同中间量、部分变量、跨模板精确来源和随机来源等语义控制。

<div class="method-step__io" markdown="1">

**输入**：一个接收问题 $r$、其正常答案 $a_r$，以及与其共享计算模板但改变指定中间变量的来源问题 $s$。<br>
**输出**：带有已验证 $a_r$、$a_{cf}$ 和控制来源类别的反事实测试单元。

</div>

**直观理解**：这一步像把一道题中的某个计算结果从另一道题搬来，并事先算清楚搬运后正确答案应是什么。各种控制来源用于排除模型只是识别答案词、单个数字或表面模板的可能。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 定义并执行缓存切片移植

将 $C_t(s)$ 中选定的提示前缀、潜在尾部或完整缓存切片替换到 $C_t(r)$ 的对应位置，并分别测试仅键、仅值或自然的键值联合替换；隐藏状态则通过缓存独立、缓存加隐藏状态和仅隐藏状态三种条件单独检验。

<div class="method-step__io" markdown="1">

**输入**：来源与接收模型在潜在步骤 $t$ 的缓存 $C_t(s)$、$C_t(r)$，当前隐藏状态 $h_t(s)$、$h_t(r)$，以及预先指定的缓存区段、层范围和组件类型。<br>
**输出**：保持接收端其余上下文与后续解码器不变的干预状态 $r'$。

</div>

**直观理解**：可把缓存看成模型推理时留下的内部笔记。本步骤只交换指定页或指定栏，从而判断真正能带走反事实计算的是值内容、寻址键、隐藏状态，还是更大的整体。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 继续接收端推理并验证答案转移

继续接收端 rollout，对固定候选答案计算教师强制的序列对数概率，以 target win 判断 $a_{cf}$ 是否成为最高分答案，并计算干预前后的反事实—原答案相对概率边际；标题级语义控制还通过贪心或采样解码检查自由生成结果。

<div class="method-step__io" markdown="1">

**输入**：干预后的接收状态 $r'$、与干净运行相同的候选答案集合，以及必要时的自由生成设置。<br>
**输出**：反事实 target win、概率边际变化、自由解码匹配结果及并列审计信息。

</div>

**直观理解**：不能只看某个内部数值是否变化，而要看搬运后模型是否真的更相信预先验证的反事实答案。自由生成检查用于防止结论仅由封闭候选集的强制比较造成。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 以能力门控、充分性和必要性规则判定载体

先要求干净来源与接收任务达到规定能力门槛；再以 oracle 互换测试充分性，以同模板同数值范围的随机来源替换同一区段测试必要性，并比较互不重叠的竞争区段。满足门槛后，将最小充分区段标为主动载体；若充分区段变化则标为载体迁移，证据或能力不足则不作机制判定。

<div class="method-step__io" markdown="1">

**输入**：干净任务能力、各缓存区段的反事实转移结果、语义与组件控制结果，以及匹配随机腐败结果。<br>
**输出**：主动载体、完整必要性、部分必要性、载体迁移或 no-call 五类诊断结论。

</div>

**直观理解**：一个区段既要在放入正确反事实信息时足以改答案，也应在被匹配噪声破坏时选择性损害原计算，才有较强的因果机制证据。若模型本来不会做题，或多个检查互相矛盾，SCIT宁可不下结论。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 潜在步骤的 Transformer 缓存对象

$$
C_t=\{(K_t^{\ell},V_t^{\ell})\}_{\ell=1}^{L}
$$

**符号说明**

- $C_t$：潜在推理步骤 t 的 Transformer 缓存，包含截至该步骤可供后续注意力使用的条目
- $t$：执行缓存干预时的潜在推理步骤
- $K_t^{\ell}$：第 $\ell$ 层在步骤 t 可用的键缓存
- $V_t^{\ell}$：第 $\ell$ 层在步骤 t 可用的值缓存
- $\ell$：Transformer 层索引
- $L$：Transformer 的总层数

<div class="equation-explanation" markdown="1">

**直观理解**：该式明确SCIT交换的基本因果对象：各层注意力的键和值缓存集合。当前隐藏状态 $h_t$ 不包含在 $C_t$ 内，因此缓存转移与隐藏状态复制可以被分别测试，避免把两类内部状态混为一谈。<br>
**原文位置**：第3.1节，Step 1: patch a cache slice

</div>

</div>

<div class="equation-block" markdown="1">

#### 反事实相对证据边际变化

$$
\Delta_{\mathrm{cf-rec}}=[\log P(a_{cf})-\log P(a_r)]_{\mathrm{patched}}-[\log P(a_{cf})-\log P(a_r)]_{\mathrm{clean}}
$$

**符号说明**

- $\Delta_{\mathrm{cf-rec}}$：干预相对干净运行对反事实答案与接收原答案之间证据差的改变量
- $P(a_{cf})$：在固定候选与教师强制评分条件下，反事实答案字符串的概率
- $P(a_r)$：在相同评分条件下，接收问题原答案字符串的概率
- $a_{cf}$：由来源中间量和接收端保留信息共同确定的已验证反事实答案
- $a_r$：未干预接收问题的正确答案
- $\mathrm{patched}$：完成指定缓存或隐藏状态干预后的接收 rollout
- $\mathrm{clean}$：未进行干预的接收 rollout

<div class="equation-explanation" markdown="1">

**直观理解**：先在干预运行中比较模型对 $a_{cf}$ 和 $a_r$ 的相对偏好，再减去干净运行已有的相对偏好。若 $\Delta_{\mathrm{cf-rec}}>0$，说明移植使模型相对更支持反事实答案；该连续指标可补充 target win 的封闭集最高分判定。<br>
**原文位置**：第3.1节，Step 3: validate the readout

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。SCIT不是用于更新模型参数的损失函数，也不重新训练被测潜在思维链模型；它是在既有检查点上实施的因果干预与读出协议。教师强制对数概率仅用于对相同候选答案进行可比较的推断期评分，$\Delta_{\mathrm{cf-rec}}$ 是诊断统计量而非反向传播目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 缓存对象与可变长度尾部对齐**

每个潜在步骤的缓存由所有层的键值条目组成，而当前残差隐藏状态 $h_t$ 被明确排除在缓存对象之外。若来源和接收分别在 $T_s$ 与 $T_r$ 停止，令 $c_x=T_x-1$，长度为 $k$ 的潜在尾部按距各自停止点的反向距离对齐，即用来源区间 $[c_s-k:c_s]$ 替换接收区间 $[c_r-k:c_r]$，未匹配的接收位置保持不变。

> 直观理解：两个问题可能使用不同数量的隐式推理步，因此不能机械地按绝对位置交换。按“离结束还有几步”对齐，比较的是两条推理轨迹中功能上对应的尾部。

**2. 区段、键值组件与层范围干预网格**

区段维度测试潜在尾部、提示前缀和完整缓存；组件维度测试 K-only、V-only 与自然 K/V；隐藏状态维度测试 cache-only、cache+$h$ 和 $h$-only。GPT-2 的层定位包括全部层、预声明的末三分之一层 $8$–$11$、其补集 $0$–$7$、子块 $8$–$9$ 与 $10$–$11$，并通过改变后缀长度排除单个末尾 token 触发器。

> 直观理解：这相当于从“笔记在哪一段、哪几层、哪一栏”三个方向逐步缩小位置。仅键或仅值的组合不一定是模型自然产生的状态，因此它们只用于因果拆分，必须与自然 K/V、隐藏状态和解码控制共同解释。

**3. 语义控制、匹配腐败与载体决策器**

精确反事实来源用于测试充分性；同答案、同中间量、部分变量、跨模板部分来源、单 token、仅键和仅隐藏状态用于排除简单特征解释。必要性测试不采用零消融，而用同模板、同数值范围的随机来源缓存替换目标区段；决策时要求干净能力至少为 $0.80$，oracle 区段 target win 至少为 $0.80$，主要互斥竞争区段至多为 $0.25$，完整必要性还要求主动区段腐败使接收答案 target win 相对干净运行至少下降 $0.50$。

> 直观理解：正确来源能改答案只说明该区段“可以使用”，不自动证明模型平时“必须使用”它。语义控制排除搬运单个线索，匹配腐败则以较少偏离模型分布的方式检查该区段是否对正常计算不可替代。

**训练与推理**

训练阶段沿用各被测检查点原有的训练过程，所给方法章节未提出额外优化步骤。推断时，首先分别运行来源 $s$ 和接收 $r$ 至指定潜在步骤 $t$；根据停止策略对齐缓存位置，按干预网格替换选定区段、层和 K/V 组件，并按条件决定是否复制 $h_t(s)$。随后从干预状态继续接收端 rollout，以固定候选集计算 target win 和 $\Delta_{\mathrm{cf-rec}}$，并对关键行执行自由解码。最后运行语义控制及匹配随机腐败，在能力门控后依据预声明阈值给出充分性、必要性、载体迁移或 no-call 判定。

**复现信息**

公平解释结果所需的关键设置有四点。第一，来源与接收潜在长度不同时按距停止点的反向距离对齐，载体结论因此以具体停止策略为条件。第二，完整缓存替换只是可实现转移的上界，不参与最小载体竞争；若完整缓存和更小区段均通过，应选择最小通过区段。第三，K-only 与 V-only 是人为拼接的外科式干预，成功只表示该组件在固定接收端路由或内容条件下具有充分性，失败也不能推出该组件在自然计算中完全无关。第四，算术来源的 balls、books 和 coins 只是同一两步程序的词汇变体，主要测试表面措辞稳健性而非广泛任务多样性；每个接收样本原则上使用一个同模板、同范围的匹配随机来源进行腐败测试。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GPT-2 局部潜在推理数据：CODI-GPT2 与 Sim-CoT-GPT2 两个六步 GPT-2 型检查点，在 balls、books、coins 三种词汇变体上评估。主 CODI-GPT2 balls 单元使用 240 个留出源—接收者对，其他 GPT-2 模板或检查点行通常使用两个各含 60 个样本的种子；其作用是定位局部算术反事实的缓存载体。
- 匹配破坏与控制数据：三个词汇变体合计 360 个样本，用于比较干净的反事实缓存交换、语义来源控制和匹配破坏；解码自由生成检查用于验证缓存干预是否不仅改善教师强制评分，也改变最终生成行为。
- 规模与任务范围单元：包括公共或匹配的 1B、修复后的 8B 以及若干关系链、实体查找、表达式树和列表筛选/求和任务；载体图通常为每个任务使用 $N=128$ 个留出对，并先通过能力门控。其作用是检验局部算术机制能否跨规模、任务和训练路径保持，或识别载体机制发生转移与无法判定的边界。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**final-step target-win rate**

在最终步骤上，接收者采用干预后目标反事实答案的比例；它衡量缓存交换是否足以把源样本的计算结果转移给接收者。 （对目标反事实而言越高越好；解释载体时应同时要求候选干预高、控制干预低，而不是只看单独的高分。）

</div>
<div class="metric-item" markdown="1">

**log-probability drop**

匹配破坏缓存后，接收者目标输出对数概率的下降量；它衡量破坏候选载体是否损害已转移的反事实计算。 （下降量越大越支持必要性，但必须与干净交换和能力门控结合，不能仅凭概率下降断言具体机制。）

</div>
<div class="metric-item" markdown="1">

**clean accuracy / competence gate**

模型在未干预任务上的正确性，以及用于保留载体判断的能力阈值；它排除模型本身尚未学会任务映射时产生的假阴性。 （清洁任务能力越高越能支持定位结果；论文还审计了 $0.70$、$0.80$、$0.90$ 的能力门槛以及 $0.75$–$0.90$ 的充分性下限和 $0.10$–$0.30$ 的竞争者上限。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### GPT-2 局部算术载体定位：CODI-GPT2 与 Sim-CoT-GPT2 的分层 K/V 交换

<div class="result-value" markdown="1">

CODI-GPT2 在最终步骤的第 8–9 层值缓存块达到 $0.875$–$0.908$ 的目标胜率，而第 10–11 层仅为 $0.017$–$0.029$，非后期片段为 $0.000$–$0.008$；Sim-CoT-GPT2 的第 8–9 层为 $0.958$–$0.992$，第 10–11 层为 $0.133$–$0.192$。隐藏状态、key-only 及语义来源控制更弱。作者据此将局部载体定位为中后期 value-cache suffix trajectory，而不是当前隐藏向量、key 侧路由或可复用答案槽位。

</div>

这说明把源样本中后期若干层的值缓存后缀复制给接收者，能够把反事实答案带过去；关键对象更像“被注意力读取的内容轨迹”，而不是单个最终隐藏状态或单独的寻址键。它只证明了指定 GPT-2 检查点和任务范围内的局部因果载体，不能推出所有潜在思维链模型都使用同一缓存区域。

<div class="result-source" markdown="1">

来源：Section 5.1, Local arithmetic carrier

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across the two GPT-2-scale arithmetic checkpoints, the active local carrier is a middle-to-late value-cache suffix trajectory.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 后缀长度与匹配破坏：充分性和必要性链条

<div class="result-value" markdown="1">

CODI-GPT2 中，单 token 后缀目标胜率为 $0.203$，而 $k\geq3$ 的后缀达到 $0.984$–$1.000$；Sim-CoT-GPT2 在 $k=1$ 时为 $0.516$、$k=2$ 时为 $0.995$。匹配破坏后，CODI-GPT2 的目标胜率降至 $0.211$，并伴随 $13.655$ 的对数概率下降；Sim-CoT-GPT2 降至 $0.606$，论文仅称其为方向性的必要性支持。作者因此认为完整的充分性—必要性证据只在主 CODI-GPT2 检查点成立。

</div>

后缀曲线排除了“只要复制最后一个缓存 token 就够了”的解释，表明需要一个短轨迹；破坏实验进一步检验这段轨迹是否不可替代。CODI-GPT2 的破坏效应足够强，支持较严格的必要性判断；Sim-CoT-GPT2 虽然有同方向下降，但下降不足以完成论文设定的必要性证据链。

<div class="result-source" markdown="1">

来源：Section 5.1, Local arithmetic carrier; Appendix Tables 21 and 58

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Matched corruption closes the sufficiency-and-necessity loop only for CODI-GPT2: late-value corruption drops recipient target win to 0.211 with a 13.655 log-probability drop, while Sim-CoT-GPT2 drops only to 0.606 and is reported as directional necessity support.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 跨规模与任务的载体机制图：能力门控后的 regime shift

<div class="result-value" markdown="1">

算术样式的 GPT-2/1B 单元保留 latent-tail value/KV transfer；而能力达标的 8B 算术、实体、关系和表达式/列表单元转向 prompt-prefix 或 full-cache K/V。主 8B 行中，prompt-prefix K/V 目标胜率为 $1.000$，latent-tail K/V 为 $0.000$；关系链任务在 1B 和 8B 上的 latent/prompt/whole-cache K/V 目标胜率均为 $0/1/1$。作者还报告 8B 的 prompt-prefix 交换从第一个扫描的潜在步骤起即充分，并由无 latent 探针和后缀前消融支持可见提示字段仍被读取。

</div>

模型变大或任务改变后，反事实信息不一定继续写入潜在后缀；在这些 8B 单元中，提示中已经出现的事实、查询或规则字段本身就足以支持输出。因此，实验支持的是“能力门控的载体地图”，不是一个普适的 latent-tail 机制。完整缓存阳性也不能单独定位局部载体，因为它同时包含提示前缀和潜在后缀。

<div class="result-source" markdown="1">

来源：Section 5.2, Carrier-regime boundaries; Figure 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Competent 8B arithmetic, entity, relation, and expression/list cells instead shift to prompt-prefix or full-cache K/V: Figure 3 shows prompt-prefix K/V at 1.000 and latent-tail K/V at 0.000 for the main 8B rows.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 机制结论高度依赖检查点、任务和训练路径：完整的充分性—必要性闭环只在主 CODI-GPT2 算术检查点成立；Sim-CoT-GPT2 缺少足够的匹配破坏证据，三个新训练 seed 也没有达到局部载体门槛，因此不能宣称普适机制。
- 部分大规模或边界单元只能得到 full-cache 阳性、能力不足或支持不足，论文将其保留为 no-call；即使 8B prompt-prefix 交换充分，无 latent 探针仍无法完全区分“答案在 latent rollout 前已完成”和“后续读出重新访问已编码的提示字段”。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 隐藏状态控制：只交换当前隐藏向量，与值缓存交换形成对照，用于检验反事实是否由显式隐藏状态而非缓存轨迹携带。
- 键缓存控制：只交换 K（key）侧缓存，与只交换 V（value）侧缓存比较，用于区分注意力寻址与被读取内容的因果作用。
- 语义来源控制：使用 same-answer、partial-variable、cross-template partial 等保留部分答案或变量语义的来源，检验结果是否只是复用答案槽位、变量槽位或表面相似模板。
- 匹配破坏与解码控制：匹配地破坏候选缓存并观察目标胜率和对数概率下降，同时进行自由生成；前者检验必要性，后者检验效应是否能在实际生成中显现。

**实验想回答的问题**

- 在局部算术型潜在思维链模型中，反事实计算主要由哪一种 Transformer 缓存对象携带：隐藏状态、键缓存、值缓存，还是缓存中的特定后缀轨迹？
- 当模型规模、任务类型或训练路径变化时，已定位的潜在尾部值缓存机制是否稳定，还是会转移到提示前缀、完整缓存，或因证据不足而无法判定？

**实验实现**

实验采用固定的教师强制评分规则，并构造精确的源—接收者反事实对。预声明的分阶段流程先比较潜在后缀、提示前缀和完整缓存上的 oracle K/V 交换，再仅在选定片段上进行 key-only 与 value-only 检验；证据顺序为充分性、组件与来源控制、匹配破坏、解码验证和载体范围校准。主要 GPT-2 诊断每次使用单 GPU；论文报告点估计，因为 oracle 与控制之间通常存在较大间隔，并在附录提供部分行的标准误或 bootstrap 区间。大规模载体图在能力门控后判断最小的、互不重叠的充分片段；完整缓存交换被视为上界控制，而非最终的局部机制。分阶段复用干净状态可使一个匹配的 8B 提示载体单元墙钟时间减少 34.6%–40.0%，但这只是运行效率审计，不是模型效果结论。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| K/V 组件拆分与语义来源控制 | value-cache 交换保留高目标胜率，而 hidden-only、key-only、same-answer、partial-variable 和 cross-template partial 控制较弱；论文将这些控制用于排除当前隐藏向量、key-side routing 以及可复用答案/中间量槽位。 | 该消融不是简单删除一个网络层，而是把同一源—接收者交换拆成不同信息通道。若 key-only 也同样有效，就可能是注意力寻址在传递结果；若 same-answer 控制有效，则可能只是复制答案表面。控制较弱使 value 后缀解释更具体，但不能单独证明其中每个 value token 都不可替代。 | Section 5.1, Local arithmetic carrier<br><span class="experiment-evidence">Hidden-only, key-only, same-answer, partial-variable, cross-template partial, and decoded controls remain weaker, ruling out the current hidden vector, key-side routing, or a reusable answer/intermediate slot as the main explanation.</span> |
| 训练路径、能力门控与阈值审计 | 三个新训练的 CODI-style seeds 虽有较高 clean accuracy，但第 8–9 层值缓存充分性仅为 $0.049$–$0.138$，匹配破坏下降仅为 $0.026$–$0.089$；三组 latent/prompt/whole-cache 目标胜率分别为 $0.370/0.203/0.870$、$0.208/0.427/0.865$ 和 $0.427/0.141/0.906$，均未达到 $0.80$ 局部载体门槛。另一方面，阈值扫描仍保留 5 个 latent-tail 和 7 个 prompt-prefix 调用。 | 这项消融检验的是结论对训练随机种子和报告阈值的敏感性。新种子并未稳定地产生强 prompt-prefix 局部机制，而只是显示完整缓存能传递信息；因此不能把主检查点的 late-value 结果当作训练后必然出现的属性。阈值审计减少了“换一个合理阈值就改变地图”的担忧，但没有消除训练路径依赖。 | Section 5.3, Path sensitivity and reporting audits; Appendix Tables 42 and 43<br><span class="experiment-evidence">Their latent/prompt/whole-cache K/V target-win rates are .370/.203/.870, .208/.427/.865, and .427/.141/.906: whole-cache transfer is present, but neither disjoint segment reaches the .80 carrier gate, so all three receive no localized-carrier call.</span> |

**定性案例**

- 关系链任务是最清晰的非算术精确控制案例：可执行的“person → badge → room”关系提供验证过的接收者、反事实和控制标签；1B 与 8B 上 latent/prompt/whole-cache K/V 目标胜率均为 $0/1/1$，8B 解码 transfer 为 latent/prompt 的 $0/1$，匹配破坏后的接收者保持为 $1/0$。跨三种语义等价表述，能力达标单元仍选择 prompt-prefix carrier，说明该结果更符合可见提示字段绑定，而非算术型 late-value 机制。证据来源：Section 5.2, Carrier-regime boundaries；Appendix Table 24。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：It introduces a causal cache-patching diagnostic to identify internal mechanisms carrying computations in latent chain-of-thought reasoning models.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`ed230a354667ced9cd5ea479c56cde0959b284317e116644b7c06b840a2b4eea`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
