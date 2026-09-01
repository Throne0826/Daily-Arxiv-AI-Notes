---
title: "[论文解读] Quantifying and Mitigating Korean Jamo-Level Typographical Vulnerabilities in Large Language Models"
description: "[arXiv 2608.30229][LLM 安全] 原文未明确报告。"
arxiv_id: "2608.30229"
announcement_date: "2026-09-01"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-01T05:51:28.749720+00:00"
source_sha256: "65498f7fcb1a1ef79f974753326722f353fc31185ca54d8507b3c858a2e3e130"
tags:
  - "LLM 安全"
  - "LLM Reasoning"
  - "LLM 其他"
  - "韩语 jamo 级扰动"
  - "大语言模型鲁棒性"
  - "键盘输入错误"
  - "子词分词"
  - "隐藏状态探针"
  - "链式思维推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2608.30229</p>

# Quantifying and Mitigating Korean Jamo-Level Typographical Vulnerabilities in Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-01</span>
<span><strong>作者</strong> Seojin Lee, Hwanhee Lee</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Chung-Ang University, Seoul, Korea</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.30229v1) · [PDF 下载](https://arxiv.org/pdf/2608.30229v1) · **关键词** 韩语 jamo 级扰动, 大语言模型鲁棒性, 键盘输入错误, 子词分词, 隐藏状态探针, 链式思维推理<br>


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

本文位于大语言模型（LLM）输入鲁棒性与可信人工智能研究交叉领域，具体考察韩语键盘输入错误如何影响模型理解和问答。现有多数拼写鲁棒性基准把噪声建模为可见字符层面的替换、删除或插入，但韩语具有不同的文字结构：一个表面音节块由更小的字母单位 jamo 组合而成，因此错误可以发生在音节块内部。此类错误可能生成表面上仍是合法、但语义已经改变的韩语字符，也可能使独立 jamo 暴露在文本中；两者都会破坏面向正常音节块训练的子词分词过程。本文以 KMMLU 中的韩语选择题为测试环境，研究 jamo 级扰动对 LLM 答题准确率和内部表示的影响，并进一步利用可检测的表示变化识别可能含有错字的输入。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**韩语音节块与 jamo**

韩语文字表面通常以音节块呈现，但音节块内部由较小的字母单位 jamo 组合而成。由于键盘输入实际上按 jamo 序列进行，错误可能只破坏音节块内部结构，而不只是替换一个完整的表面字符。

</div>
<div class="concept-item" markdown="1">

**子词分词**

子词分词器把输入文本切分为模型词表中的词、词片段或其他较短单位，再将这些单位转换为模型可处理的表示。韩语 jamo 暴露或音节结构异常时，输入可能无法按照正常韩语文本被切分，从而使模型接收到与训练分布不同的表示。

</div>
<div class="concept-item" markdown="1">

**隐藏状态与线性探针**

隐藏状态是 LLM 在处理输入过程中形成的内部向量表示，虽然不直接等同于最终答案，但可能包含输入是否受到扰动等信息。线性探针是在冻结模型表示上训练的简单分类器，用线性决策边界判断隐藏状态属于某类输入；本文用它检测输入是否可能含有 jamo 级错字，而不是直接修改文本。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个原本格式正常的韩语问题及其选项，本文构造带有 jamo 级键盘扰动的对应输入，并将干净输入与扰动输入都交给 LLM 完成 KMMLU 选择题。扰动可以发生在音节块内部，并呈现两类主要表面结果：其一是生成语义错误但形式合法的字符，其二是暴露独立 jamo、破坏原有音节结构。模型输出是选择题答案以及在需要时产生的内部表示；研究首先比较不同扰动强度下的答题性能，然后检验这些扰动是否造成区别于普通答题错误的表示变化。进一步地，使用一部分带标注的表示训练线性探针，并测试其对未见扰动类型的检测能力；最后，Typo-Aware Chain-of-Thought（TACoT）根据探针判断结果决定是否启用链式思维推理：疑似含错字的输入进入 CoT 推理，其他输入采用较低成本的普通推理。该设定的核心假设是，jamo 级错误会留下可检测的内部信号，且不必为所有输入付出 CoT 的推理成本。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

输入的韩语问题文本；在本文语境中，$x$ 可以是干净输入，也可以是施加 jamo 级扰动后的输入。

</div>
<div class="notation-item" markdown="1">

**$y$**

模型对 KMMLU 选择题给出的答案。

</div>
<div class="notation-item" markdown="1">

**$h(x)$**

LLM 处理输入 $x$ 后得到的内部隐藏状态表示，线性探针利用该表示判断输入是否可能含有错字。

</div>
<div class="notation-item" markdown="1">

**$s(x)$**

探针对输入 $x$ 的错字检测结果或类别判定；在 TACoT 中，该信号用于决定是否路由到链式思维推理。

</div>

</div>

**直接相关的工作**

- **DeepWordBug（Gao et al., 2018）**: 该工作表明少量黑盒字符级编辑即可显著降低文本分类器性能，为研究神经语言模型的字符级脆弱性提供了基础。本文继承其“通过控制文本扰动评估模型鲁棒性”的思路，但指出普通可见字符编辑不足以描述韩语音节块内部的 jamo 级错误。
- **KoGEC（Kim et al., 2024）**: KoGEC 将韩语语法错误纠正建模为类似翻译的文本修复任务，为韩语错误纠正提供了模型和资源。本文不把目标设为恢复一段流畅文本，而是考察受控 jamo 扰动对下游 LLM 答题和隐藏状态的影响；文中示例显示，KoGEC 有时能修复暴露的 jamo，却可能忽略合法形式错误或进行改变原意的流畅改写，因此不能作为可靠的前置防护。

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

论文的方法由“受控扰动构造—内部表征探测—按需推理防御”三部分组成。首先，作者只修改韩语问题文本，在音节内部或词间施加五类键盘相关错误，并以不同扰动强度形成可控测试输入；随后，从模型经 Fisher 准则选定的层提取末尾 token 隐状态，在与测试集来源分离的 HAERAE-GK 上训练带 $L_2$ 正则的逻辑回归探针，估计输入含错概率；最后，TACoT 将该概率与验证集阈值比较，只把疑似含错输入路由到思维链推理，其余输入仍采用短输出的标准推理。最终输出是模型对 KMMLU 选择题或 HRM8K 自由回答题的答案，同时降低相对于全量 CoT 的平均生成成本。
直观地说，该方法不先尝试把所有错字改回去，而是把语言模型的中间表示当作“错字传感器”：模型若在阅读某个输入时表现出典型的内部异常，就投入较昂贵的逐步分析；若没有异常，则快速直接作答。这样避开了通用韩语纠错器难以修复音节内部 jamo 错误、甚至可能改变原意的问题，也避免了对每个干净输入都运行长 CoT。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造受控韩语错字输入

分别施加 Jamo Substitution、Jongseong Deletion、Jamo Repetition、Space Deletion 和 Jamo Transposition 五类扰动，每类独立设置 $5\%$、$10\%$、$15\%$、$20\%$、$25\%$ 五档强度，且同一实例不混合不同错误类型。除 Space Deletion 按空格数计算强度外，其余类型按问题中的韩语音节数随机选择扰动位置。

<div class="method-step__io" markdown="1">

**输入**：KMMLU、HAERAE-GK 或 HRM8K 的原始韩语问题文本；KMMLU 的答案选项保持不变。<br>
**输出**：带有已知错误类型和强度标签的干净—扰动输入对；KMMLU 共形成 $35{,}030\times5\times5=875{,}750$ 个扰动实例。

</div>

**直观理解**：这一步像在同一份试卷上系统地制造不同种类、不同严重程度的打字错误，从而把错误类型和错误数量控制住。只改问题、不改选项，可使准确率下降主要反映模型没有正确理解受损问题，而不是答案选项也被破坏。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 提取内部表征并确定监测层

将输入送入模型，在第 6 节所述 Fisher 准则选定的层 $l$ 上提取末尾 token 的隐藏状态 $h_l(x)$；层选择只使用 HAERAE-GK，不使用 KMMLU 或 HRM8K。所给节选未提供 Fisher 分数的具体公式与逐层选择细节，因此不能据此重建该计算。

<div class="method-step__io" markdown="1">

**输入**：HAERAE-GK 的干净问题及其扰动版本，以及待监测语言模型。<br>
**输出**：每个输入对应的固定维度表示 $h_l(x)$，以及每个模型各自选定的监测层 $l$。

</div>

**直观理解**：隐藏状态可理解为模型读完问题后形成的内部摘要；作者选择最能区分正常输入与错字输入的一层作为观察点。使用末尾 token，是为了取得模型已经看完整个问题后的汇总性表征。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 训练错字概率探针并校准阈值

对特征标准化后训练带 $L_2$ 正则的逻辑回归，错字类从四种 jamo 层错误、五档强度的样本池中等量抽取，避免数量更大的扰动池主导分类器；再在留出验证集上选择使 Youden’s $J$ 统计量最大的阈值 $\theta$。KMMLU 与 HRM8K 均不参与层选择、探针拟合或阈值调节。

<div class="method-step__io" markdown="1">

**输入**：HAERAE-GK 上的隐藏状态 $h_l(x)$、干净或含错二元标签，以及独立验证划分。<br>
**输出**：给定 $h_l(x)$ 后输出 $P(\mathrm{typo}\mid h_l(x))$ 的轻量探针，以及固定路由阈值 $\theta$。

</div>

**直观理解**：逻辑回归相当于在模型内部摘要上画一条简单分界线，判断当前输入是否像带错字的样本。类别均衡与独立验证校准分别用于防止探针偏向常见错误，并把概率转化为实际的路由决定。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### TACoT 按需路由与答案生成

先运行模型以取得 $h_l(x)$ 并计算含错概率；若 $P(\mathrm{typo}\mid h_l(x))\geq\theta$，则使用要求逐步分析的 CoT 提示生成答案，否则使用只要求直接输出答案的 Standard 提示。KMMLU 中标准路径最多生成 8 个新 token，CoT 路径最多生成 1024 个新 token。

<div class="method-step__io" markdown="1">

**输入**：新的问题 $x$、冻结的语言模型、选定层 $l$、训练好的探针及阈值 $\theta$。<br>
**输出**：选择题的答案字母或自由形式解答，以及由实际进入 CoT 的样本比例决定的推理成本。

</div>

**直观理解**：这相当于医院分诊：大多数看起来正常的问题走快速通道，只有内部信号显示可能受损的问题才进入耗时的详细诊断。TACoT 的收益因此同时取决于探针是否找对受损输入，以及 CoT 是否能从这些输入中恢复原意。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### TACoT 推理路由规则

$$
\mathrm{route}(x)=\begin{cases}\mathrm{CoT},&P(\mathrm{typo}\mid h_l(x))\geq\theta,\\ \mathrm{Standard},&P(\mathrm{typo}\mid h_l(x))<\theta.\end{cases}
$$

**符号说明**

- $x$：当前待回答的韩语问题输入。
- $h_l(x)$：模型处理输入 $x$ 时，在 Fisher 准则选定层 $l$ 上取得的末尾 token 隐藏状态。
- $l$：针对当前语言模型选出的内部监测层。
- $P(\mathrm{typo}\mid h_l(x))$：逻辑回归探针根据隐藏状态估计输入含有排印错误的条件概率。
- $\theta$：在 HAERAE-GK 留出验证集上通过最大化 Youden’s $J$ 统计量选出的路由阈值。
- $\mathrm{CoT}$：使用逐步分析提示和较长生成上限的思维链推理路径。
- $\mathrm{Standard}$：使用默认直接作答提示和较短生成上限的标准推理路径。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把错字检测转化为成本控制决策：概率达到阈值时，系统认为额外推理的潜在收益足以承担长输出成本，因而调用 CoT；否则快速作答。它不会改变模型参数，也不要求先生成纠错后的句子。<br>
**原文位置**：第 7.1 节，TACoT: Typo-Aware CoT

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：TACoT 不对基础语言模型进行微调，唯一需要拟合的是二元逻辑回归探针。其优化目标是利用干净与扰动 HAERAE-GK 样本区分“clean”和“typo”，并通过 $L_2$ 正则限制权重复杂度；原文节选未给出该损失函数的显式公式，因此不额外构造方程。训练后并不按准确率直接选择路由阈值，而是在留出验证集上最大化 Youden’s $J$，即综合考虑真阳性率与假阳性率，使系统既能触发真正含错的输入，又尽量避免把干净输入送入高成本 CoT。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 五类韩语排印扰动生成器**

Jamo Substitution 将某个 jamo 替换为标准韩语键盘上的邻键，可能仍组成合法但语义改变的音节；Jongseong Deletion 删除音节终声，也总会留下合法音节；Jamo Repetition 复制内部 jamo，使额外原始 jamo 暴露在音节块外；Jamo Transposition 交换音节内 jamo 顺序并破坏声母—中声—终声结构；Space Deletion 则连接相邻 eojeol，不改变音节内部组成。前四类用于探针的 jamo 层错字类，Space Deletion 因不改变音节内部结构而表现为较弱的内部表征信号。

> 直观理解：韩文表面上的一个方块字实际上由多个 jamo 组合，因此键盘错误既可能生成“看起来合法但意思错了”的另一个字，也可能把零散字母暴露出来。该分类把这两种音节内部破坏与普通空格丢失分开，便于判断模型究竟对哪类结构最脆弱。

**2. 隐藏状态逻辑回归探针**

探针输入为 Fisher 选层上的末尾 token 隐状态 $h_l(x)$，输出二元含错概率 $P(\mathrm{typo}\mid h_l(x))$；其特征先标准化，并采用 $L_2$ 正则逻辑回归。训练和校准数据来自含 176 道四选一题的 HAERAE-GK，且与主要评测集 KMMLU 来源分离。

> 直观理解：探针并不重新理解整道题，也不生成纠正文本，只读取主模型已经形成的内部向量，所以比再调用一个大型纠错或推理模型更轻。跨数据源训练与测试用于检验它捕捉的是较一般的错字表征，而不是记住 KMMLU 题目。

**3. Typo-Aware Chain-of-Thought 路由器**

TACoT 以探针概率和阈值 $\theta$ 为唯一决策依据，在 Standard 与 CoT 两种推理模式间二选一。Standard 要求直接输出答案且限制为短生成；CoT 明示输入可能含错，要求先逐步推断问题意图，再在末行输出答案。

> 直观理解：通用纠错器可能忽略仍然合法的错误音节，或把专业、数学文本改坏；单纯警告模型有错字又未必促使其真正恢复语义。TACoT 不强制改写原文，而是在检测到风险时让原模型花更多推理步骤重建问题意图。

**训练与推理**

校准阶段按模型分别进行：在 HAERAE-GK 的干净问题及扰动对应项上运行冻结模型，用 Fisher 准则选层并提取该层末尾 token 隐状态；从四类 jamo 层扰动和五种强度中均衡抽取错字样本，与干净样本组成二元训练数据；标准化隐藏向量后拟合逻辑回归，并在留出验证划分上确定阈值 $\theta$。HAERAE-GK 负责所有拟合和选择，而 KMMLU、HRM8K 始终只用于最终评测，从流程上避免测试题泄漏。
推理阶段对每个新输入先执行一次用于取得 $h_l(x)$ 的模型前向计算，再由探针输出含错概率并依据路由式选择提示。标准路径直接生成答案；CoT 路径要求模型先识别或重建可能受损的题意、逐步推理，再输出最终答案。需要注意，所给节选只说明“先通过模型提取隐藏状态，随后路由到推理”，没有明确说明隐藏状态提取所需前向计算能否与最终答案生成完全复用，因此复现成本时不应自行假设零额外前向开销。

**复现信息**

五档扰动均从原始干净输入独立生成，受影响位置随机选择，不在单个样本内混合错误类型；KMMLU 仅扰动题干并保留选项，HRM8K 同样只修改问题文本。模型通过 vLLM 服务，采用温度为 0 的贪心解码；非 CoT 最多生成 8 个新 token，CoT 最多生成 1024 个新 token。隐藏状态使用 HuggingFace Library 提取，逻辑回归使用 scikit-learn 实现，特征标准化，采用 $L_2$ 正则且 $C=1.0$。这些设置对公平解释尤其重要：CoT 与 Standard 的输出预算差异很大，因此 TACoT 所优化的是准确率与生成 token 成本之间的折中，而不是在完全相同解码预算下比较两种提示。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- KMMLU：包含 45 个学科、35,030 道四选一题目的韩文专家级多项选择基准，题目来自原始韩文考试而非由英文翻译而来。它是论文的主要评测集，用于测试五类 Jamo 级扰动下的准确率、在未见问题上的拼写检测能力以及不同缓解方法。KMMLU 不参与层选择、探针训练或阈值调节，以避免评测泄漏。
- HAERAE-GK：HAERAE Bench 的韩文常识子集，共 176 道四选一题目，数据源与 KMMLU 不重合。它承担校准数据的作用，用于 Fisher 层选择、未见扰动检测的线性探针训练，以及 TACoT 的探针训练和路由阈值选择；因此 KMMLU 测试题在这些步骤中保持未见。
- HRM8K：包含 8,011 道韩文数学推理题，覆盖翻译题目和原生韩文数学竞赛题。与 KMMLU 不同，它要求生成自由形式的解答，且主题是数学文字题，与 KMMLU 的百科知识和专业知识领域不重合。论文在其问题文本上施加同样的五类扰动和五个强度等级，并且只将 HRM8K 用于评测，不用于拟合或选择。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy**

模型在多项选择题上选中正确答案的比例；在扰动条件下，它直接衡量拼写噪声造成的任务性能损失。 （越高越好，因为较高准确率表示模型更能保持正确回答。）

</div>
<div class="metric-item" markdown="1">

**AUROC**

线性探针区分正常输入与拼写扰动输入的排序能力，综合考虑不同检测阈值下的真正例率和假正例率。 （越高越好；数值越高表示探针越能把可能含有拼写错误的输入与正常输入分开。）

</div>
<div class="metric-item" markdown="1">

**Mean accuracy over all 25 typo conditions**

五类扰动乘以五个强度等级共 25 个条件下的平均准确率，用于概括模型的总体扰动鲁棒性，并比较不同随机种子是否改变总体结论。 （越高越好；但它是跨条件平均值，不能替代对某一种扰动或某一强度的单独分析。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### KMMLU 上的韩文 Jamo 级扰动与模型规模鲁棒性

<div class="result-value" markdown="1">

论文报告五类 Jamo 级扰动下的准确率会随扰动强度单调下降，并且模型参数规模并未带来对音节内部噪声的可靠鲁棒性。附加的 API 规模模型实验进一步显示，Jamo 级扰动造成的准确率下降持续大于 Space Deletion。

</div>

这说明问题不只是普通的空格或字符缺失，而是韩文音节内部结构被破坏后，模型的子词切分和后续理解都会受到影响。结果支持“扩大模型规模不能自动解决该类错误”的作者主张，但并不证明所有韩文任务、所有模型或所有类型的拼写错误都具有完全相同的下降幅度。

<div class="result-source" markdown="1">

来源：Appendix E, Figure 9 discussion

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The degradation pattern persists: jamo-level perturbations consistently cause larger accuracy drops than Space Deletion across both models, suggesting that Korean typo vulnerability is not a limitation of model scale or training regime.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 随机扰动采样的稳定性检验

<div class="result-value" markdown="1">

在三个随机种子下，四个模型跨 25 个扰动条件的平均准确率变化最多为 0.07 个百分点；所有模型和条件中最大的单条件变化出现在 EXAONE-7.8B 的 Jongseong Deletion、等级 3，准确率范围为 43.26 至 43.83，跨度为 0.57 个百分点。

</div>

该实验隔离了“随机选中了哪些音节”这一因素。总体平均结果几乎不变，说明主结论不太可能只是某一次随机腐蚀位置造成的偶然现象。不过，单条件仍可能出现小幅波动，因此它支持结果稳定性，而不是证明随机性完全没有影响。

<div class="result-source" markdown="1">

来源：Appendix E, Table 7 discussion

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The mean moves by at most 0.07 points across seeds, and even the largest single-condition deviation is negligible: in the worst case across all models and conditions, Jongseong Deletion at level 3 on EXAONE-7.8B, accuracy ranges only from 43.26 to 43.83, a 0.57-point spread.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 多模型复现与模型规模比较

<div class="result-value" markdown="1">

实验不仅评测 EXAONE-2.4B、EXAONE-7.8B、A.X-Light 和 Qwen3-4B，还在 Gemini-3.1-Flash-Lite 与 Qwen3-235B-A22B-2507 上检查同样的扰动模式；作者报告两个 API 规模模型都出现 Jamo 级扰动比 Space Deletion 更大的准确率下降。

</div>

跨不同模型系列和更大规模模型仍观察到相同的相对退化模式，增强了结论的外部可信度：脆弱性可能来自韩文 Jamo 破坏与模型输入表示、分词之间的不匹配，而不只是某一个开源模型的训练缺陷。但该结果仍局限于论文选取的模型、扰动分类和韩文基准。

<div class="result-source" markdown="1">

来源：Appendix E, Figure 9 discussion

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Figure 9 evaluates two API-scale models, Gemini-3.1-Flash-Lite (Google DeepMind, 2026) and Qwen3-235B-A22B-2507 (Yang et al., 2025), on the same perturbations.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验摘录没有提供 Figure 9 的完整数值、各扰动类型的逐项分数、AUROC 的具体结果，也没有提供 HRM8K 上的具体准确率；因此不能据此判断不同扰动之间的绝对差异或 TACoT 的收益大小。
- 评测主要覆盖韩文知识选择题、韩文数学推理题和所选模型，且扰动位置是随机采样的。即使三个种子显示稳定，也不能直接推出真实用户输入中的键盘错误分布、其他韩文任务或未测试模型同样具有相同脆弱性。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 干净输入基线：没有施加拼写扰动的题目，用来衡量模型在正常输入上的参考准确率；图 9 中以虚线表示。
- Space Deletion：删除空格的扰动条件，是与 Jamo 级扰动进行比较的普通字符或表面格式噪声基线，用于检验 Jamo 级错误是否造成更严重的性能下降。
- 五类 Jamo 级扰动及其五个强度等级：这是核心受扰条件，用于比较韩文音节块内部不同类型、不同程度的键盘级破坏；随机选择受影响的音节，强度固定腐蚀比例。
- 不同规模或不同模型系列：实验比较 EXAONE-2.4B、EXAONE-7.8B、A.X-Light、Qwen3-4B，并在附加实验中比较 Gemini-3.1-Flash-Lite 和 Qwen3-235B-A22B-2507，用于测试脆弱性是否依赖具体架构或模型规模。

**实验想回答的问题**

- 韩文 Jamo 级拼写扰动是否会系统性降低大语言模型在韩文知识理解任务上的准确率，并且这种脆弱性是否会随模型规模扩大而消失？
- 实验中的扰动结果是否具有跨模型、跨随机种子和跨数据集的稳定性，从而支持将其视为韩文输入鲁棒性的普遍问题，而非特定评测设置的偶然现象？

**实验实现**

评测在每种扰动类型的五个强度等级下进行；随机种子只改变被选中的音节位置，不改变由强度决定的腐蚀率。附加稳定性实验使用三个随机种子，并对四个模型重新生成完整基准后评测。KMMLU 仅用于最终评测，HAERAE-GK 用于所有拟合和选择步骤，HRM8K 仅用于泛化评测。实验还在两个 API 规模模型上复现扰动比较，以检验结论是否仅由小型或特定训练体系模型造成。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 随机种子敏感性：三个扰动采样种子 | 四个模型在 25 个扰动条件上的平均准确率最大仅变化 0.07 个百分点；表 7 给出的最大跨种子差异分别为 EXAONE-2.4B 的 0.04、EXAONE-7.8B 的 0.06、A.X-Light 的 0.07 和 Qwen3-4B 的 0.02。 | 这是对扰动生成过程的稳定性消融，而不是对模型组件的消融。它表明改变受损音节的位置不会实质改变总体结论，因此观察到的退化更可能由扰动类型和强度驱动。 | Appendix E, Table 7<br><span class="experiment-evidence">EXAONE-2.4B \| 39.76 \| 39.76 \| 39.72 \| 0.04</span> |
| 模型规模与训练体系：API 规模模型扩展检验 | 在 Gemini-3.1-Flash-Lite 和 Qwen3-235B-A22B-2507 上，Jamo 级扰动仍比 Space Deletion 导致更大的准确率下降；原文未明确报告该图中各模型各条件的完整数值。 | 该检验相当于把模型规模和模型系列作为外部消融变量，测试脆弱性是否会在更大模型中消失。结果没有支持“更大模型自然更鲁棒”的假设，但由于缺少完整数值，不能据此比较两个 API 模型的绝对性能。 | Appendix E, Figure 9 discussion<br><span class="experiment-evidence">The degradation pattern persists: jamo-level perturbations consistently cause larger accuracy drops than Space Deletion across both models, suggesting that Korean typo vulnerability is not a limitation of model scale or training regime.</span> |

**定性案例**

- 原文摘录未提供具体题目级案例或模型输出，因此无法进行单题定性分析。现有结果只支持条件级结论：Jamo 级扰动会造成比 Space Deletion 更大的准确率下降，但未展示某个音节如何改变答案、分词结果或推理过程。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The work studies LLM robustness to Korean typographical perturbations and mitigates failures through selectively routed chain-of-thought inference.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`65498f7fcb1a1ef79f974753326722f353fc31185ca54d8507b3c858a2e3e130`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
