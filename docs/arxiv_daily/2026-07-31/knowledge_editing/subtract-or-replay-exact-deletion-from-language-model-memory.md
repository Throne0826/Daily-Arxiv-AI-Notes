---
title: "[论文解读] Subtract or Replay? Exact Deletion from Language-Model Memory"
description: "[arXiv 2607.27539][知识编辑] 本文把语言模型持久化上下文记忆中的“精确删除”定义为：编辑后的记忆必须与从未摄入目标记录时的反事实参考一致，并指出删除机制取决于记忆表示——影响可寻址时做代数减除，影响被后续写入缠入共享状态时则从检查点回退并重放后缀。"
arxiv_id: "2607.27539"
announcement_date: "2026-07-31"
primary_category: "knowledge_editing"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T03:25:49.180533+00:00"
source_sha256: "7f1bb21cc41efc15b3b7caff0eb40390c05bad9f16d7ca55e9611e1eaf21466f"
tags:
  - "知识编辑"
  - "精确记忆删除"
  - "上下文机器遗忘"
  - "反事实记录省略"
  - "可寻址记忆"
  - "支持向量记忆"
  - "循环状态"
  - "回退与重放"
  - "语言模型记忆"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">知识编辑 · arXiv 2607.27539</p>

# Subtract or Replay? Exact Deletion from Language-Model Memory

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Ramesh, Vishwajith</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.27539) · [PDF 下载](https://arxiv.org/pdf/2607.27539) · **关键词** 精确记忆删除, 上下文机器遗忘, 反事实记录省略, 可寻址记忆, 支持向量记忆, 循环状态, 回退与重放, 语言模型记忆<br>


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

本文把语言模型持久化上下文记忆中的“精确删除”定义为：编辑后的记忆必须与从未摄入目标记录时的反事实参考一致，并指出删除机制取决于记忆表示——影响可寻址时做代数减除，影响被后续写入缠入共享状态时则从检查点回退并重放后缀。

**不用术语来说**：语言模型一旦把对话或文档压缩进长期状态，仅从当前提示中删掉原文或追加一条更正，并不会清除已经存下的影响。例如临床助手先记住错误家族病史，之后即使收到澄清，旧信息仍可能影响风险评估或再次出现在摘要中。真正的删除应直接修正模型记忆，使其后续行为等同于当初根本没有读过那条错误记录。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出面向持久化语言模型记忆的表示级判据：以“记录从未被摄入”或论文明确声明的记录省略重建作为反事实标准，区分可由记录局部量逆转的可寻址影响与会被后续写入持续变换的非可分离影响，从而决定应采用减除还是重放。
- 将该判据落实到两类预训练模型记忆：在植入支持向量记忆的 Gemma 3 中验证记录级代数减除，在原生 Kimi Linear 递归状态中说明固定删除收据为何失效，并以检查点回退和后缀重放实现删除及更正。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究部署阶段语言模型的“上下文记忆删除”：模型已经把一条记录压缩进持久注意力或循环状态后，如何直接修改该状态，使其与“从未摄入该记录”时构建的状态一致。它不同于主要修改模型参数的机器遗忘，也不同于从可见提示中删掉原文或追加更正；后两者都不能保证已写入记忆的影响消失。本文把精确删除视为一种反事实等价要求，并强调可实现的删除操作取决于记忆表示：保留记录局部地址的影响可以代数相减，而被后续写入反复变换并混入共享循环状态的影响通常需要恢复早期检查点并重放后缀。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**持久上下文记忆**

指语言模型在处理长序列时，将先前内容写入注意力存储或循环状态，并在原始文本不再被重新读取时继续使用这些信息。本文删除的是这种已经摄入的记忆，而不是模型训练权重中的知识。

</div>
<div class="concept-item" markdown="1">

**反事实记录省略参考**

它表示同一个模型在其他条件保持一致、但目标记录从未被摄入时应得到的记忆状态或下一词输出。删除是否“精确”由编辑后结果能否匹配这一参考来判定，而不是只看目标事实是否暂时难以被问出。

</div>
<div class="concept-item" markdown="1">

**记录影响的可寻址性**

若一条记录的影响仍对应独立系数、缓存项或其他记录局部量，系统便能定位并逆转该影响；若后续写入持续读取和变换共享状态，旧记录的贡献会随后缀变化，不再能由写入时保存的一份固定“收据”表示。前者适合减量删除，后者需要回退并重放。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个已经按时间顺序摄入多条记录的预训练语言模型、一条待删除或待更正的目标记录，以及必要时目标记录之前保存的状态检查点和其后的原始记录后缀。输出是编辑后的持久记忆；论文要求它在声明的比较范围内匹配同一模型未摄入目标记录时的参考，而非仅降低目标内容的召回率。Gemma分支将全局注意力层替换为具有记录地址的支持向量记忆，并把“删除后对保留的上下文化键重新拟合”作为参考；Kimi Linear分支不改造其原生循环记忆，以“从目标记录之前的状态开始、跳过该记录并重放后缀”作为参考。该设定假定能够访问记忆内部状态；回退重放还要求保存记录边界检查点和后续原始输入，并在同一确定性实现内比较。结论范围仅覆盖模型的上下文记忆，不声称删除训练权重中的知识，也不能撤回删除前已经对外产生的输出。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **MUNKEY（Laguna et al., 2026）**: 与本文最接近的“按设计实现遗忘”工作：它为图像分类器的每个训练样本设置外部键控库中的可学习样本令牌，并通过删除对应键来遗忘样本，支持了“表示结构决定可删除性”的前提。其对象是分类器和训练实例，评估依赖单独重训的参考模型；本文进一步研究自回归语言模型已经写入持久注意力或循环状态的记录，并比较同一实例化记忆与其记录省略参考。
- **Ramesh（2026）的支持向量记忆**: 该工作提供Gemma分支所需的可寻址记忆原语：注意力权重来自对上下文键的一类支持向量拟合，其系数可作为记录影响的地址；结合经典增量支持向量算法，可以逆转求解并删除某个词元。本文将该记忆移植进Gemma 3，并把局部记忆层的可逆删除要求提升为完整语言模型下一词输出上的反事实一致性检验。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

GDPR 删除权、临床同意撤回、错误记录更正，以及撤回研究、版权内容或危险内容的移除，都要求已部署模型按记录遗忘。难点在于目标内容可能已经进入持续存在的注意力或递归状态并影响后续写入；删除可见文本、屏蔽一次输出或追加相反陈述，都不能保证旧影响已从内部状态消失，而且已经对外产生的历史输出也无法由事后删除撤回。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **权重编辑与近似机器遗忘**：直接调整模型参数，使目标事实在 TOFU、MUSE、WMDP 等基准的问答、准确率或文本相似度评测中更难被召回；其主要验证对象通常是编辑后的输出行为，而非某条记录从内部记忆中被严格消除。
- **按设计可删除的外部键控记忆**：以 MUNKEY 为代表，为每个训练样本设置可学习的示例令牌并存入外部键控库，需要遗忘时删除对应键。该思路证明“先选择可删除表示”比事后修补任意模型更有结构优势，但原工作面向图像分类，并以分类性能和输出空间成员推断相对独立重训练模型进行评估。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 近似权重遗忘可能只是压低目标输出概率，而没有移除其内部表示：目标信息仍可被中间层探针或对数几率差恢复，也可能在少量正常微调后重新变得可提取。因此，准确率或 ROUGE 的下降不足以证明删除，部署期攻击者仍可能利用残留。
- 已有可删除键控方案尚未回答自回归语言模型已经把记录写入持久注意力或共享递归状态后的问题。尤其当后续写入会读取并变换旧状态时，记录刚写入时保存的固定“收据”不再等于当前状态中应扣除的贡献；仅删除键、遮蔽提示或追加更正都无法复现记录从未出现的状态。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一个同时适用于不同语言模型记忆结构、可在同一实例内部审计的精确标准与操作判据：应明确编辑后状态要匹配哪个记录省略参考，并判断某条记录的影响是否始终保有独立地址。由此仍待解决的是，何时可以用成本较低的记录级减除达到该参考，何时这种操作在结构上不可能、必须重建部分历史。

</div>
<div markdown="1"><span>核心问题</span>

对于已经摄入记录的持久化语言模型记忆，记忆表示的哪些性质允许编辑后的下一词输出及相关内部状态精确匹配声明的记录省略反事实参考；当记录影响可寻址或被后续递归写入纠缠时，分别应采用何种删除机制？

</div>
<div markdown="1"><span>作者直觉</span>

如果记忆像带编号的账本，每条记录的贡献仍对应一个系数、缓存项或其他记录局部量，那么删除就是撤销这一笔，并可通过对保留记录重新拟合来核验。若记忆更像不断揉合旧内容的共享草稿，后来的每次写入都会改写早先记录在当前状态中的形态，最初保存的差值便不再适用；此时可靠办法是回到目标记录之前的检查点，跳过它后重新执行其余写入，以直接构造所需反事实状态。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文把“精确删除”定义为一个反事实状态等价问题，而不是目标答案是否暂时消失：删除操作后的模型输出应与“从未摄入该记录”的参考模型一致；若持久记忆状态本身相等，则得到更强证书。方法首先检查记忆表示是否保留了可定位到单条记录的“删除地址”：若记录影响可由记录局部账本恢复，就执行代数减量；若后续写入以内容相关方式改写了该影响，则恢复受害记录之前的检查点并重放后缀。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立删除单元与反事实参考

明确记录粒度、记忆构建过程和比较标准，并将删除后的输出与省略 $r_j$ 后重新构建的参考输出比较。Gemma 使用“固定已上下文化保留键的重拟合”作为减量证书参考；Kimi 使用从原始记录流省略受害记录后得到的完整反事实状态。

<div class="method-step__io" markdown="1">

**输入**：按顺序摄入的记录流 $R=(r_1,\ldots,r_n)$、待删除记录 $r_j$、查询 $q$，以及由构建器 $B$ 形成的持久记忆。<br>
**输出**：一个可审计的删除目标：输出分布等价，或更强的持久状态逐元素乃至逐比特等价。

</div>

**直观理解**：不能只看模型是否不再说出秘密，因为提示抑制也可能让答案消失。这里要求编辑后的模型与真正没有见过该记录的模型走到同一个规定参考点。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 判定记录影响是否可寻址

计算记录贡献 $\delta_x(S)$，并比较它在不同后缀下是否保持不变，或能否由保存的局部凭据和紧凑后缀账本精确运输。加法写入允许固定减量，逐通道衰减可用累计乘积校正；若贡献随后缀内容变化，则固定凭据不足。

<div class="method-step__io" markdown="1">

**输入**：受害记录前缀 $P$、记录 $x$、一个或多个后缀 $S$，以及相应的记忆状态。<br>
**输出**：删除路径选择：可寻址表示进入代数减量，不可寻址或未通过检验的表示进入检查点回退与后缀重放。

</div>

**直观理解**：这一步相当于检查一笔账能否凭原始收据直接冲销。若后来的交易不断以内容相关方式改写旧账，就不能只拿旧收据做减法，而要回到交易发生前重新记账。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### Gemma 支持向量记忆改造与恢复

仅把全局注意力层替换为支持向量门控记忆，保留局部滑窗层、投影、归一化、旋转位置编码和分组查询结构；先拟合每层核带宽以近似原注意力，再冻结基础模型并训练秩为 $8$ 的 LoRA，使改造模型通过语言模型损失恢复效用。

<div class="method-step__io" markdown="1">

**输入**：预训练 Gemma 3、各全局注意力层的上下文键值、原模型注意力输出和语言建模训练数据。<br>
**输出**：一个长程键带支持系数 $\alpha$ 的 Gemma：保留键参与核加权读出，系数为 $0$ 的 reserve 键对读出严格无贡献，并可通过可逆增量求解器删除。

</div>

**直观理解**：改造只针对长期记忆通道，不动短期滑窗。LoRA 像一个小型适配补丁，用很少的可训练参数补偿更换长期记忆机制带来的能力损失。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按表示执行精确删除或精确修订

对 Gemma，以固定的预删除盒约束 $C$ 反向运行 float64 增量算法，求得删除目标后保留键重拟合的支持系数，并直接注入双精度完整模型读出；对 Kimi，恢复受害记录前的检查点，跳过该记录并确定性重放后缀，修订时则先写入更正记录再重放。

<div class="method-step__io" markdown="1">

**输入**：Gemma 的支持向量求解状态及目标位置，或 Kimi 中受害记录之前保存的循环与卷积状态、受害记录和其后缀。<br>
**输出**：Gemma 得到与固定 $C$ 保留键重拟合相符的下一词元 logits；Kimi 得到与从未摄入受害记录或从一开始摄入更正记录相同的 logits、循环状态和卷积状态。

</div>

**直观理解**：Gemma 的记录仍有地址，因此可以像删除数据库中的可逆条目一样快速冲销。Kimi 的旧影响已被后续内容纠缠，只能回到记录之前并重演之后的历史，但不必从整个上下文开头重建。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 精确删除的反事实输出标准

$$
f\!\left(q;D_j(B(R))\right)=f\!\left(q;B(R_{\setminus j})\right)
$$

**符号说明**

- $R=(r_1,\ldots,r_n)$：按顺序摄入的记录序列。
- $r_j$：需要删除的第 j 条记录。
- $B(R)$：构建器摄入记录序列 R 后形成的持久记忆。
- $D_j$：作用于现有持久记忆、删除第 j 条记录影响的操作。
- $R_{\setminus j}$：从原记录序列中省略第 j 条记录后得到的序列。
- $q$：用于审计删除结果的查询。
- $f(q;B)$：模型在记忆 B 和查询 q 下的下一词元概率分布。

<div class="equation-explanation" markdown="1">

**直观理解**：等式左侧是在已经摄入全部记录后再执行删除，右侧则是从一开始就没有摄入目标记录。两者对任意审计查询在声明的数值容差内一致，才构成输出级精确删除；若两边的记忆状态也相等，则是更强保证。<br>
**原文位置**：第 3.1 节，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 后缀条件下的记录状态贡献

$$
\delta_x(S)=B(P,x,S)-B(P,S)
$$

**符号说明**

- $P$：受害记录出现之前的记录前缀。
- $x$：待删除的受害记录。
- $S$：受害记录之后摄入的记录后缀。
- $B(P,x,S)$：依次摄入前缀、受害记录和后缀后得到的记忆状态。
- $B(P,S)$：省略受害记录，仅摄入前缀和后缀后得到的反事实记忆状态。
- $\delta_x(S)$：在给定后缀 S 后，受害记录 x 对最终状态造成的净贡献。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把“有受害记录”和“无受害记录”的最终状态相减，以观察目标记录的影响是否被后续写入改变。若 $\delta_x(S)$ 与后缀无关，就能保存固定凭据并直接扣除；若它随后缀内容变化且无法由紧凑账本校正，则应重放后缀。<br>
**原文位置**：第 3.2 节，公式 (3)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：Gemma 改造需要恢复训练，但论文节选未给出单独编号的损失公式：基础模型参数被冻结，先为每个被替换的全局层拟合一个核带宽以匹配原注意力输出，再通过可微支持向量门控在标准下一词元语言模型损失上训练秩为 $8$ 的 LoRA。优化的目的不是学习删除动作本身，而是在引入可寻址长程记忆后恢复预测效用；删除由可逆求解器在推理阶段执行。Kimi 部分完全不训练，只对发布的 $48$B、$8$-bit 权重做确定性推理、状态诊断和重放。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 支持向量门控长程记忆**

给定键 $x_i\in\mathbb{R}^d$、值 $v_i$ 和查询 $q$，门控器使用核加权平均读出，并由单类支持向量描述求得系数 $\alpha$；盒约束为 $C=1/(\nu n)$。键被分成 margin、error 与 reserve 集，reserve 键满足 $\alpha=0$；反向运行可逆增量算法，可把求解状态恢复为删去目标键后的固定 $C$ 重拟合状态。

> 直观理解：该模块给长期记忆中的每个键保留可审计的代数位置。目标不是简单把某个权重缩小，而是重新得到“如果这个键从未进入当前求解，其他键应具有哪些系数”的精确答案。

**2. KDA 写入可分离性诊断**

诊断在共同坐标中比较同一记录经过不同后缀后的状态贡献。加法写入保持固定贡献，逐通道对角衰减可用运行乘积运输贡献；KDA 的 delta-rule 写入先读取当前状态再更新，因此后续内容会以内容相关方式变换旧记录的贡献，固定记录凭据及所测试的衰减账本均不足以精确反演。

> 直观理解：循环结构本身不是问题，关键在写入规则是否把旧记录与新内容混在一起。若后续每次写入都根据当前混合状态修改记忆，一条记录就不再对应一块可直接扣除的固定影响。

**3. 检查点回退与确定性重放**

系统在记录边界保存循环状态和卷积状态；删除时恢复受害记录之前的检查点，省略受害记录后只重算其后缀。确定性执行使结果等于直接构建 $B(P,S)$，计算成本为 $O(\text{suffix})$；若在边界插入更正记录再重放，则实现精确修订。

> 直观理解：检查点像文档的历史快照。记录无法单独拆出时，从它之前的快照重新执行后续内容，能够消除该记录对所有后来状态的连锁影响。

**训练与推理**

训练阶段仅适用于 Gemma：保留原投影、归一化、旋转位置编码、分组查询布局和局部滑窗层，只替换全局层；冻结基础模型后完成带宽拟合与 LoRA 恢复。推理阶段分为普通运行和证书运行：普通训练、攻击、成员推断与采样实验使用单精度批量门控求解器，目标位置被 mask 后重新拟合；这条路径提供行为证据，不承担精确性声明。证书运行对每个待删除目标固定预删除的 $C$，使用 float64 反向增量算法计算删后系数，绕过单精度求解器直接注入实时读出，并让完整模型以双精度产生删后 logits；近似对照只把目标读出权重缩放为 $\gamma=0.01$，不能视作重拟合。

Kimi 推理先在记录边界保存全部相关循环与卷积状态。删除时选择受害记录之前最近的检查点，恢复该状态，跳过受害记录并按原顺序重放余下后缀；若目标是修订，则在同一边界写入更正记录后再重放。因为 KDA 的 delta rule 不保留固定删除地址，论文不把 attention-only masking 当作完整删除，而只把它与重放 oracle 比较以定位直接通道移除遗漏的循环状态影响。

**复现信息**

公平解释 Gemma 结果需要注意三个边界。第一，支持向量改造只覆盖 Gemma-3-1B 的 $4$ 个全局层，$22$ 个局部层保持不变，因此证书针对超出局部窗口的长程记忆；仍在窗口中的文本需要重新 prefill，而非只做门控减量。第二，删除证书比较的是固定已上下文化保留键、固定预删除 $C$ 的重拟合，而不是重新按不变 $\nu$ 求解；从原始词元流重新打包还会消除目标记录在摄入时对邻近键编码留下的印记，是更强但更昂贵的参考。第三，float64 减量与双精度完整前向是证书级配置，不能用普通单精度 masked refit 的行为结果替代。

Kimi 使用同一确定性 MLX 实现和发布的 $8$-bit 权重比较删除路径与从未摄入参考，并审计 logits、全部循环状态及卷积状态的逐比特相等。检查点位于记录边界，重放成本随受害记录之后的后缀长度增长，而不是随完整上下文长度增长；混合架构中的全局注意力与 KDA 循环记忆必须同时被纠正，仅清零循环状态或仅遮蔽注意力位置都不构成完整删除。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- FineWeb-Edu sample-10BT：使用其中 $3300$ 万 token 进行模型恢复训练，批大小为 $8$、序列长度为 $512$。它不是删除评测集，而是用于让替换全局注意力后的 Gemma-3-1B 恢复语言建模能力。
- WikiText-103 test：主要困惑度评测使用 $400$ 个文本块；附加的跨域检查对 WikiText 使用 $300$ 个块。它衡量记忆门控改造及恢复训练对常规语言建模效用的影响。
- TOFU forget10/retain90：将待遗忘事实与保留事实打包到超出局部注意力窗口的位置，用于评估记录删除后的目标回忆、保留信息抽取、提示诱导、重学习和 LiRA 成员推断。恢复分数以预算匹配的“从未写入”模型为 $0$、原始回忆为 $1$ 进行归一化。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**下一词输出 KL 散度**

比较递减后模型与 retained-key refit 的下一词概率分布；接近浮点舍入误差表示两条删除路径在输出层面一致，但不是对所有未来提示和所有内部状态的普遍数学证明。 （越低越好；理想值为 $0$，数量级约 $10^{-14}$ 时可视为所用双精度执行下的数值一致。）

</div>
<div class="metric-item" markdown="1">

**困惑度与门控相对开销**

困惑度衡量模型对测试文本的预测质量，门控开销则比较恢复模型与 matched control 的相对困惑度差。它回答可删除记忆是否以常规语言能力下降为代价。 （困惑度及相对开销越低越好，因为较低值代表测试 token 获得更高概率。）

</div>
<div class="metric-item" markdown="1">

**归一化恢复与 LiRA**

归一化恢复以 never-ingested 下限为 $0$、删除前回忆为 $1$，用于观察目标信息能否被诱导或重学习；LiRA 以 AUC 及低 FPR 下的 TPR 判断攻击者能否区分目标记录是否存在。 （遗忘目标的恢复值越接近 $0$ 越好；LiRA AUC 越接近 $0.5$、低 FPR 下 TPR 越低，越接近随机猜测。恢复值略低于 $0$ 可能来自归一化和测量波动，并不表示“比从未写入更彻底”的强结论。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Gemma-3-1B 上的单条支持 token 精确删除证书

<div class="result-value" markdown="1">

在 $31$ 个支持 token 删除实例上，float64 代数递减相对 retained-key refit 的下一词输出 KL 中位数为 $5.4\times10^{-15}$，最差为 $9.3\times10^{-14}$；相比之下，Decay 的中位 KL 为 $1.8\times10^{-6}$。

</div>

作者结果表明，可寻址支持向量记忆中的目标影响可通过逆增量更新删除，其输出与“移除目标后重新拟合”在双精度误差范围内一致；简单缩小目标权重虽可能让行为测试看似遗忘，却没有达到同样的输出等价性。该证书只覆盖给定模型、提示、支持位置和下一词分布，不能单独推出任意上下文或整段生成均完全一致。

<div class="result-source" markdown="1">

来源：Appendix D, “Certificate and sequence”; Figure 4(c,e)

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On 31 support-token deletions, decrement output KL to retained-key refit has median 5.4 × 10−15 and worst 9.3 × 10−14.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 可删除记忆改造后的 Gemma-3-1B 常规效用

<div class="result-value" markdown="1">

恢复后的门控模型在 WikiText-103 上困惑度为 $21.18$，matched control 为 $20.76$，相对成本为 $+2.0\%$；五项零样本任务的平均准确率差为 $-0.11$ 个百分点，三个语料上的平均困惑度开销为 $+0.9\%$。

</div>

作者据此将 1B 模型描述为在获得可删除记忆后仍接近同预算控制模型：主要语言建模和零样本能力没有发生大幅下降。分析上，这只证明特定 LoRA 预算、门控层位置、$\nu$ 和带宽设置下的效用接近，不代表改造无成本，也不能外推到更大模型。

<div class="result-source" markdown="1">

来源：Appendix B, Figure 3; Tables 3–5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Against an identically fine-tuned control: +2.0% WikiText perplexity, −0.11 percentage-point mean zero-shot accuracy, and +0.9% mean perplexity overhead across three corpora.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### TOFU 上 masked-refit 面对成员推断与信息恢复攻击

<div class="result-value" markdown="1">

LiRA 在 $39$ 个满足准入条件的目标上产生每类 $312$ 次测试，masked-refit 的 AUC 为 $0.499$，在 $1\%$ FPR 下 TPR 为 $1.3\%$；同时，提示诱导使归一化恢复仅从 $0.00$ 变为 $0.02$，相关样本重学习则从 $0.01$ 变为 $-0.10$。

</div>

作者结果显示，在所评估的攻击协议中，masked-refit 与随机成员判断及 never-ingested 行为下限难以区分，而 ICUL 等表面遗忘仍可被提取。需要严格区分：masked-refit 是单精度代理，行为和 LiRA 结果支持“未检测到残留”，但不能替代 float64 递减相对重拟合的精确性证书。

<div class="result-source" markdown="1">

来源：Appendix D, “LiRA”; Figure 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Masked refit reaches AUC 0.499 and TPR 1.3% at 1% FPR.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给章节中的精确输出证书主要基于固定 $192$-token 提示的 $31$ 个支持 token 删除，并只比较下一词分布；该覆盖范围不足以证明所有提示、长程生成或任意记录粒度下都严格等价。行为评测使用的 masked-refit 又是单精度代理，作者明确不将其用于精确性主张。
- 1B 效用结论依赖单一 LoRA 预算、固定替换层、$\nu=0.3$ 和带宽初始化，且完整训练只报告一个随机种子。源文还指出更大模型成本会升高，但当前所给实验章节未提供相应完整表格，因此不能从 1B 的 $+2.0\%$ 困惑度开销外推可扩展性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Matched control：未替换全局注意力的 Gemma-3-1B，采用与门控模型完全相同的 LoRA 预算、数据流和随机种子。它控制了低秩微调本身带来的收益，使困惑度差异更接近支持向量门控的额外成本。
- Retained-key refit / never-ingested reference：删除目标键后从保留键重新拟合门控，或使用从未写入目标记录的预算匹配参考。前者是输出级精确性证书的直接参照，后者是行为遗忘的目标下限。
- Decay 与 ICUL：Decay 将目标读出权重乘以 $\gamma=0.01$，测试强抑制能否等价于删除；ICUL 仅在提示前缀中加入遗忘指令而不改变记忆，测试表面拒答是否仍可被重新诱导。
- Gradient ascent（GA）：通过新建 rank-$8$ LoRA 对目标答案 token 做梯度上升，并在目标回忆接近 never-ingested 下限时提前停止。它代表权重空间遗忘方法，用于比较删除目标与损伤共享读取器之间的差别。

**实验想回答的问题**

- 将 Gemma 3 的全局注意力替换为可寻址的支持向量记忆后，删除目标记录的代数递减结果，能否在下一词输出上与“从未写入该记录”的保留键重拟合结果一致，同时维持可接受的语言建模与零样本任务效用？
- 行为层面的遗忘是否足以证明精确删除；在提示诱导、相关样本重学习、生成采样和 LiRA 成员推断等攻击下，masked-refit、权重衰减、提示遗忘和梯度上升分别会留下怎样的可恢复信息或共享能力损伤？

**实验实现**

实验以 google/gemma-3-1b-pt 为基础，只替换第 $5$、$11$、$17$、$23$ 个全局层，保留原查询、键、值、输出投影及位置编码等结构。恢复分两阶段：先训练每个全局层的核带宽以拟合原注意力输出，再对所有层的投影施加 rank-$8$ LoRA；matched control 只执行同预算的第二阶段。精确性证书从固定 $192$-token 通用提示的支持位置取删除目标，使用 float64 增量递减和双精度模型，与删除目标后的完整重拟合比较。行为实验采用单精度 FISTA masked-refit，因此作者明确不据此主张数值精确删除。LiRA 为上下文版本：每个目标、每一类别使用 $32$ 个随机填充影子上下文拟合高斯分布，再在留出上下文上计算似然比；由于记录通过上下文而非梯度训练写入，实验不训练影子模型。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 是否需要第一阶段 attention transfer 作为带宽初始化 | 跳过第一阶段、直接使用中位距离带宽并进行相同 LoRA 恢复时，WikiText-103 困惑度为 $21.13$；完整两阶段方案为 $21.18$。作者判断该差异处于评测噪声内，第一阶段不是最终效用的关键来源。 | 该消融隔离了带宽 attention-transfer 预训练的贡献。几乎相同的困惑度说明从未训练的 $33.29$ 恢复到约 $21.1$ 主要依赖低秩 LoRA 阶段；attention transfer 最多是可选初始化，不能被视为方法成立的必要组件。 | Appendix B, Table 3 and following ablation discussion<br><span class="experiment-evidence">LoRA recovery without stage 1 (median-bandwidth heuristic, identical stage-2 token stream via an aligned data offset, same seed and budget) reaches 21.13 versus 21.18 with it—a wash within evaluation noise.</span> |
| 恢复训练是否破坏支持向量门控的可逆删除性质 | 在未进行恢复适配的门控模型上，一次删除相对重拟合的输出 KL 为 $1.6\times10^{-14}$；恢复后的 $31$ 个删除实例中位数仍为 $5.4\times10^{-15}$、最差为 $9.3\times10^{-14}$。 | 该对照检查 LoRA 恢复是否通过改变共享投影而破坏代数删除机制。恢复前后都处于双精度数值误差量级，支持“精确性来自记忆表示及更新规则，而非偶然的未训练参数状态”；但样本数有限，仍需在更多提示和记录类型上复核。 | Appendix D, “Certificate and sequence”; Figure 4(c,e)<br><span class="experiment-evidence">A deletion on the unadapted graft is 1.6 × 10−14, so the property survives recovery training.</span> |

**定性案例**

- GA 权重编辑构成一个反例式案例：它在 $19$ 个准入目标上平均用 $9$ 步把目标回忆压至 never-ingested 下限，残差为 $-0.33\pm0.12$，但保留信息抽取同时下降 $-0.125\pm0.030$；随后对 $10$ 个目标进行良性重学习，目标恢复并过冲至 $+3.5\pm2.2$。这说明“当前答不出来”可能源于读取能力被扰乱，而不是记录状态已被删除。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Develops and validates exact deletion and amendment methods for records stored in persistent language-model memory.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`7f1bb21cc41efc15b3b7caff0eb40390c05bad9f16d7ca55e9611e1eaf21466f`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
