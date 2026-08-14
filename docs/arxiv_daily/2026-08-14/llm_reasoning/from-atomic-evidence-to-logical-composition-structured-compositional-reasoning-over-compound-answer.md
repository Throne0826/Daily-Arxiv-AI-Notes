---
title: "[论文解读] From Atomic Evidence to Logical Composition: Structured Compositional Reasoning over Compound Answer Options"
description: "[arXiv 2608.12836][LLM Reasoning] 本文将复合答案推理中的“判断原子命题”与“按显式逻辑算子组合判断”分离，以检验并缓解大语言模型明明掌握局部证据、却在组合阶段答错的组合性缺口。"
arxiv_id: "2608.12836"
announcement_date: "2026-08-14"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-14T02:54:05.562490+00:00"
source_sha256: "38a850d49b58c8e65dc8482f9aa25f34625465e2b41396a48c3483295d76d45e"
tags:
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "组合推理"
  - "复合答案选项"
  - "布尔算子"
  - "原子证据"
  - "神经符号推理"
  - "整数线性规划"
  - "逻辑问答"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.12836</p>

# From Atomic Evidence to Logical Composition: Structured Compositional Reasoning over Compound Answer Options

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-14</span>
<span><strong>作者</strong> Obed Junias, Maria Leonor Pacheco</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: University of Colorado Boulder</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.12836v1) · [PDF 下载](https://arxiv.org/pdf/2608.12836v1) · **关键词** 大语言模型, 组合推理, 复合答案选项, 布尔算子, 原子证据, 神经符号推理, 整数线性规划, 逻辑问答<br>
**代码**: [https://github.com/obedjunias19/structured-compositional-reasoning](https://github.com/obedjunias19/structured-compositional-reasoning)

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

本文将复合答案推理中的“判断原子命题”与“按显式逻辑算子组合判断”分离，以检验并缓解大语言模型明明掌握局部证据、却在组合阶段答错的组合性缺口。

**不用术语来说**：一道题的选项可能不是单个答案，而是“A和B”“A或B”或“A、B都不是”。模型即使分别判断对了A和B，也可能因为没有正确执行“和”“或”“都不是”的规则而选错整个选项；尤其在需要同时处理多个可能性和否定时，这种错误更严重。论文要解决的不是一般性的知识不足，而是如何让模型的局部判断被可靠、一致地组合成最终选择。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出结构化复合推理框架：把每个复合选项拆成原子答案与显式算子，为每个唯一原子构造“得到支持”和“未得到支持”的对立假设并获取局部证据，再由受算子语义约束的整数线性规划统一分配原子真假并选出唯一复合选项。
- 提出相对校准，使一个原子的分数同时反映模型对它的置信度及其相对同题其他原子的地位；作者还构建阅读理解基准 Logical-SATA，并用它与常识推理基准 Logical-CommonsenseQA 检验该框架能否跨越不同类型的原子证据。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于大语言模型逻辑推理、组合推理与神经符号推理的交叉位置。它研究一种特殊的多项选择任务：候选答案不是单个陈述，而是由两个原子答案通过 AND、OR 或 NEITHER/NOR 显式连接而成。已有评测显示，模型即使能分别判断两个原子答案，也可能在组合时出错，并呈现出合取较容易、析取较困难、带否定的组合最困难的规律。因此，本文把“理解上下文并判断原子答案”与“依照布尔算子组合判断”视为两个可分离的问题；这也区别于一般多答案问答，后者通常要求独立选择所有正确项，却不在候选项内部规定显式逻辑关系。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**原子答案与复合答案**

原子答案是可被单独判断为受上下文支持或不受支持的基本陈述。复合答案则把两个原子答案用逻辑算子连接起来，例如 $A\land B$，其正确性取决于原子判断及算子语义。

</div>
<div class="concept-item" markdown="1">

**布尔算子**

AND（合取）要求 $A$ 与 $B$ 都成立；OR（析取）要求至少一个成立；NEITHER/NOR 表示两者都不成立，即 $\neg A\land\neg B$。这些算子把局部真假判断转换为复合候选项的真假判断。

</div>
<div class="concept-item" markdown="1">

**整数线性规划**

整数线性规划（ILP）是在离散变量和线性约束下寻找最优赋值的方法。本文用它把模型给出的原子证据分数组合起来，并强制最终结果遵守算子语义且只选择一个复合答案。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括自然语言上下文或问题，以及若干由两个原子答案和显式算子构成的复合候选项；算子属于 AND、OR 和 NEITHER/NOR。任务输出恰好一个正确的复合候选项。核心设定是逻辑结构已经直接写在候选项中，因此无须让模型把整道题自动翻译成形式逻辑；系统只需判断每个唯一原子答案是否得到上下文支持，再按已知算子组合这些判断。若同一原子答案出现在多个候选项中，它应只获得一个一致的局部判断，而不能因所在候选项不同而改变。该设定用于隔离“组合负担”：当模型正确解决原子子问题却未能依据算子得到正确复合结果时，即出现组合性缺口。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$A$**

复合候选项中的第一个原子命题或原子答案

</div>
<div class="notation-item" markdown="1">

**$B$**

复合候选项中的第二个原子命题或原子答案

</div>
<div class="notation-item" markdown="1">

**$A \land B$**

AND 复合：仅当两个原子命题都成立时成立

</div>
<div class="notation-item" markdown="1">

**$\neg A \land \neg B$**

NEITHER/NOR 复合：两个原子命题都不成立时成立

</div>

</div>

**直接相关的工作**

- **SATA-Bench（Xu et al., 2025）**: SATA-Bench研究 select-all-that-apply 多答案选择，每个选项被独立判断，但候选项内部没有显式布尔算子。本文据其独立标注答案构造段落级阅读理解基准 LOGICAL-SATA，以测试原子证据在 AND、OR 和 NEITHER/NOR 下的组合。
- **Logical-CommonsenseQA（Junias and Pacheco, 2026）**: 该基准把显式布尔算子置于常识问答的候选答案内部，并观察到模型表现随算子复杂性恶化。本文沿用这一任务结构，将其作为常识推理评测，并针对原子判断正确但逻辑组合失败的问题引入受约束推断。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

复合答案选项要求模型在一次预测中完成两类任务：先依据常识或篇章判断各个原子答案是否成立，再严格执行 And、Or 或 Neither/Nor 的组合语义。已有评估呈现随算子变化的系统性退化：And 相对容易，Or 更难，涉及否定的组合最困难。由于难度主要跟随算子而非题目内容变化，作者据此认为，相当一部分错误来自逻辑可能性的表示与组合负担，而不只是缺少知识。实际后果是，直接提示把内容理解和逻辑组合混在一起，模型即使解决了局部子问题，也可能在最终选项上失败，并且使用者难以判断错误究竟来自证据判断还是组合步骤。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **显式中间推理方法**：思维链、分解式提示、蕴含树和对立候选判断等方法把原本隐含的推理过程展开，让模型生成子问题答案、推理步骤或支持与反对证据，以获得比直接输出选项更丰富的中间结构。
- **神经符号推理方法**：这类方法先把自然语言问题自动翻译成逻辑式或其他形式化表示，再交给外部求解器执行满足硬约束的符号推理，从而避免仅靠自由文本生成来实现逻辑运算。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 显式中间推理方法虽然改善了局部证据的可见性，但最终组合通常仍由模型以不受约束的方式生成；因此模型可以在中间判断正确后错误执行算子，甚至悄然违反必须满足的逻辑约束，组合性缺口并未被真正封闭。
- 神经符号方法能够强制执行形式约束，却把关键风险转移到自动形式化：只要自然语言到逻辑表示的翻译有误，求解器就会对错误输入进行严格推理。它也没有充分利用本任务的特殊条件，即复合选项已经直接给出了原子答案及其逻辑算子，无须重新从自由文本构造完整形式表示。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法尚缺少一种针对“逻辑结构已在答案选项中显式给定”的端到端机制：它既要为共享于不同选项的同一原子命题产生一次、一致且经过校准的局部判断，又要把这些判断交给不可违反 And、Or 与 Neither/Nor 语义的全局组合过程，同时选出唯一答案。这个缺口位于纯提示分解与完整自动形式化之间：前者缺乏硬约束，后者承担了本场景并不必要的翻译风险。

</div>
<div markdown="1"><span>核心问题</span>

在不让大语言模型直接判断任何复合选项、也不要求它把整道自然语言题自动翻译成形式逻辑的条件下，能否仅从每个原子答案的正反对比证据出发，通过校准与受算子约束的全局推断，可靠地恢复唯一复合答案，并使改进集中出现在 Or 和 Neither/Nor 等组合负担较高的算子上？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把模型擅长但不稳定混合执行的两件事拆开：模型只负责阅读题目并比较“该原子得到支持”与“该原子未得到支持”这两个相反假设，确定局部证据；确定性的优化器只负责执行已经写在选项里的逻辑规则。相同原子无论出现在哪个选项中都只评分一次，可避免同一命题因措辞或位置而得到互相矛盾的判断；相对校准再利用同题原子之间的比较修正置信度尺度。直观上，这相当于让语言模型提供事实层面的票据，再让不能违背规则的组合器核算最终选项，从而把最容易出错的逻辑组合从自由生成中移除。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把“判断事实”和“执行逻辑组合”明确分工：大语言模型只接收上下文 $C=(P,q)$ 与单个原子答案 $a$，通过一对相反假设估计该原子成立或不成立的局部证据；模型在这一阶段看不到由两个答案组成的完整选项。随后，校准器把不同原子的分数变成更可比较的证据，整数线性规划（ILP）再用 AND、OR、Neither/Nor 的精确布尔语义组合这些证据，并强制四个选项中恰有一个有效，最终输出该选项的索引。

从直观上说，这是一种“先逐条核实、再按规则组装”的方案：语言模型负责回答“粉笔是否适合在白板上书写”之类的单项问题，确定性的求解器负责判断“记号笔 AND 粉笔”是否整体成立。这样可避免让语言模型同时理解内容、处理否定并比较四个复合选项，从而把容易混淆的自然语言推理转化为可检查的局部判断和显式逻辑计算。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 复合选项分解与原子去重

系统确定性地识别两个原子答案 $a_i^{(1)}$、$a_i^{(2)}$ 及连接算子 $\circ_i\in\{\textsc{And},\textsc{Or},\textsc{Neither/Nor}\}$，再构造去重集合 $\mathcal{U}_C=\bigcup_{i=1}^{4}\{a_i^{(1)},a_i^{(2)}\}$。同一原子若出现在多个选项中，只保留一个实例级表示。

<div class="method-step__io" markdown="1">

**输入**：一个实例的上下文 $C=(P,q)$，以及四个复合候选项 $\mathcal{A}=\{A_1,A_2,A_3,A_4\}$；每个选项写成 $A_i=(a_i^{(1)},\circ_i,a_i^{(2)})$。<br>
**输出**：结构化的四个选项三元组，以及当前实例的唯一原子答案集合 $\mathcal{U}_C$。

</div>

**直观理解**：先把每个复合选项拆成“答案一、逻辑词、答案二”，再建立一张不重复的事实清单。这样，同一个答案在不同选项中不会被模型作出互相矛盾的判断。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 对立假设构造与局部证据提取

为 $a$ 构造正假设 $h_C^{+}(a)$（$a$ 满足上下文）和负假设 $h_C^{-}(a)$（$a$ 不满足上下文），将二者作为同一提示中的 A/B 选项交给语言模型。读取两个选项首个答案标记的对数概率 $\ell_C^{+}(a)$ 与 $\ell_C^{-}(a)$，归一化为互补的原始分数 $s_{C,\mathrm{raw}}^{+}(a)$ 和 $s_{C,\mathrm{raw}}^{-}(a)$。

<div class="method-step__io" markdown="1">

**输入**：上下文 $C$ 和每个原子答案 $a\in\mathcal{U}_C$。<br>
**输出**：每个原子答案的一对局部证据分数，二者均在 $[0,1]$ 内且和为 $1$。

</div>

**直观理解**：模型不直接给一个孤立的“真”分数，而是在“成立”和“不成立”之间作正面对比。该设计让分数表达同一原子的两种解释谁更可信，同时隔离复合选项中的逻辑干扰。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 原子证据校准

方法比较 Platt scaling、保序回归和相对校准；相对校准用原始分数的 logit、实例内标准分数、实例内排名以及距最高分的差值组成特征 $\mathbf{f}_C(a)$，再由逻辑回归输出 $s_{C,\mathrm{cal}}^{+}(a)=\sigma(\mathbf{w}^{\top}\mathbf{f}_C(a)+b)$，并令 $s_{C,\mathrm{cal}}^{-}(a)=1-s_{C,\mathrm{cal}}^{+}(a)$。

<div class="method-step__io" markdown="1">

**输入**：训练集中的原始正向分数 $s_{C,\mathrm{raw}}^{+}(a)$、原子级金标签，以及测试实例内其他原子的分数。<br>
**输出**：跨原子更可比较的校准证据 $s_C^{+}(a)$ 与 $s_C^{-}(a)$；在后续推断中，该记号默认表示校准后的分数。

</div>

**直观理解**：原始的 $0.9$ 只是模型在两个说法之间的相对偏好，不一定真代表九成可靠。相对校准还考察一个原子在当前题所有原子中的位置，因此能区分“大家都接近 $0.9$”和“只有它明显最高”这两种情况。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 算子约束的全局 ILP 推断

为每个原子建立二元状态变量 $y_a$，为每个复合选项建立二元有效性变量 $x_i$；线性约束精确编码 AND、OR 和 Neither/Nor 的真值关系，并加入 $\sum_{i=1}^{4}x_i=1$。求解器在所有满足约束的赋值中，最大化被选原子状态得到的正、负证据总和。

<div class="method-step__io" markdown="1">

**输入**：去重原子集合 $\mathcal{U}_C$、每个原子的校准证据、四个选项的原子组成及其算子。<br>
**输出**：最优原子状态向量 $\mathbf{y}$、选项有效性向量 $\mathbf{x}$，以及唯一满足 $x_{\hat{\imath}}=1$ 的预测索引 $\hat{\imath}$。

</div>

**直观理解**：求解器尝试所有逻辑上允许的事实组合，选择与语言模型证据最一致的一组。逻辑规则是硬约束，所以最终答案不会出现“两个原子都不成立却把 AND 判真”之类的组合错误。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 对立假设的二项归一化证据

$$
s_{C,\mathrm{raw}}^{\pm}(a)=\frac{\exp\!\left(\ell_C^{\pm}(a)\right)}{\exp\!\left(\ell_C^{+}(a)\right)+\exp\!\left(\ell_C^{-}(a)\right)}
$$

**符号说明**

- $C=(P,q)$：当前实例的上下文，由可选段落 $P$ 和问题 $q$ 组成。
- $a$：从复合选项中抽取并去重后的一个原子答案。
- $\ell_C^{+}(a)$：在上下文 $C$ 下，模型选择“原子 $a$ 成立”这一选项时首个答案标记的对数概率。
- $\ell_C^{-}(a)$：在上下文 $C$ 下，模型选择“原子 $a$ 不成立”这一选项时首个答案标记的对数概率。
- $s_{C,\mathrm{raw}}^{+}(a)$：正假设在正、负两个候选之间归一化后的原始支持分数。
- $s_{C,\mathrm{raw}}^{-}(a)$：负假设归一化后的原始支持分数，并与正向分数之和为 $1$。
- $\pm$：统一表示正假设或负假设；分子应相应选取正向或负向对数概率。

<div class="equation-explanation" markdown="1">

**直观理解**：该式对两个互斥说法执行二项 softmax，把模型的标记对数概率转换成可比较的相对证据。它衡量的是模型更偏向“成立”还是“不成立”，并不自动等于原子真实成立的概率，因此后面仍需校准。<br>
**原文位置**：第 3.4 节，公式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 带逻辑可行域的全局证据最大化

$$
\begin{aligned}\max_{\mathbf{y},\mathbf{x}}\quad &\sum_{a\in\mathcal{U}_C}\left[s_C^{+}(a)y_a+s_C^{-}(a)(1-y_a)\right]\\ \text{s.t.}\quad &(\mathbf{y},\mathbf{x})\in\mathcal{F}_C,\\ &\sum_{i=1}^{4}x_i=1,\\ &x_i=\phi_{\circ_i}\!\left(y_{a_i^{(1)}},y_{a_i^{(2)}}\right)\quad(i=1,\ldots,4).\end{aligned}
$$

**符号说明**

- $\mathcal{U}_C$：上下文 $C$ 对应的全部去重原子答案集合。
- $y_a\in\{0,1\}$：原子答案 $a$ 的推断状态；$1$ 表示满足上下文，$0$ 表示不满足。
- $x_i\in\{0,1\}$：第 $i$ 个复合选项的推断有效性；$1$ 表示其原子状态满足对应算子。
- $\mathbf{y}$：由所有原子状态变量组成的二元向量。
- $\mathbf{x}$：四个候选选项的有效性变量组成的二元向量。
- $s_C^{+}(a)$：原子 $a$ 在上下文 $C$ 中成立的校准支持证据。
- $s_C^{-}(a)$：原子 $a$ 在上下文 $C$ 中不成立的校准支持证据。
- $\mathcal{F}_C$：满足全部二元取值、共享原子一致性和算子线性约束的可行赋值集合。
- $a_i^{(1)},a_i^{(2)}$：第 $i$ 个复合选项包含的第一和第二个原子答案。
- $\circ_i$：第 $i$ 个选项的显式逻辑算子，即 AND、OR 或 Neither/Nor。
- $\phi_{\circ_i}$：算子 $\circ_i$ 的布尔组合函数：AND 要求二者均为真，OR 要求至少一者为真，Neither/Nor 要求二者均为假。
- $i$：候选选项索引，取值为 $1$ 至 $4$。

<div class="equation-explanation" markdown="1">

**直观理解**：目标函数对每个原子选择一种状态：若令 $y_a=1$，就计入正向证据；若令 $y_a=0$，就计入负向证据。求解器不能逐个原子贪心选择，因为所有状态还必须共同满足四个选项的逻辑关系和“恰有一个选项为真”的条件；因此它寻找的是证据总量最大的全局一致解释。<br>
**原文位置**：第 3.6 节“Objective”；算子关系与唯一性约束见同节“Operator Constraints”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：该框架不重新训练或微调基础语言模型；语言模型只负责推断时产生原子级首标记概率。需要学习的部分是后处理校准器：Platt scaling 用原始正向分数拟合原子金标签，保序回归学习单调非参数映射，相对校准则以 $\mathbf{f}_C(a)$ 为输入训练逻辑回归参数 $\mathbf{w}$ 和 $b$，使输出对应原子成立的校准概率。

ILP 的目标不是神经网络训练损失，而是每个测试实例上的离散推断准则：在可行域 $\mathcal{F}_C$ 内最大化与全部原子状态相符的证据总和。因而训练阶段解决“如何让分数更可信”，推断阶段解决“哪组原子状态既最受证据支持，又能通过明确的逻辑真值表推出唯一选项”；两者职责不同，不能把 ILP 目标解释为对语言模型参数的端到端反向传播。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 原子级对比证据模块**

该模块以 $a\in\mathcal{U}_C$ 为推理单位，在同一提示中比较 $h_C^{+}(a)$ 与 $h_C^{-}(a)$，并仅使用 A/B 首标记的对数概率形成二项归一化分数。复合选项不进入语言模型提示，因此局部证据不受其连接算子和另一原子的直接影响。

> 直观理解：它把一道复杂选择题拆成若干个相互独立的“这个答案到底对不对”判断。正反说法同时出现，也使模型必须在两个明确立场之间比较，而不是生成一段难以量化的解释。

**2. 实例相对校准模块**

相对校准特征为 $\mathbf{f}_C(a)=[\operatorname{logit}(s_{C,\mathrm{raw}}^{+}(a)),z_C(a),\operatorname{rank}_C(a),s_{C,\max}^{+}-s_{C,\mathrm{raw}}^{+}(a)]^{\top}$。其中 $z_C(a)$ 是实例内标准化分数，$\operatorname{rank}_C(a)$ 是原子排名，$s_{C,\max}^{+}$ 是该实例最高正向分数；参数 $\mathbf{w}$ 和 $b$ 由训练集原子标签拟合。

> 直观理解：Platt scaling 和保序回归只看一个分数本身，而该模块还看它相对同题其他分数是高还是低。由于最终必须从四个选项中选出唯一答案，这种实例内相对位置与全局决策直接相关。

**3. 逻辑约束 ILP 模块**

对 AND，约束使 $x_i=1$ 当且仅当两个原子变量均为 $1$；对 OR，使 $x_i=1$ 当且仅当至少一个原子变量为 $1$；对 Neither/Nor，使 $x_i=1$ 当且仅当两个原子变量均为 $0$。共享原子只对应一个 $y_a$，因此其状态自动在所有相关选项间保持一致，同时唯一性约束保证最终恰有一个有效选项。

> 直观理解：这个模块相当于一个严格执行真值表的裁判。语言模型提供有噪声的事实证据，ILP 不重新理解语言，只负责找出既遵守所有逻辑规则、又最符合这些证据的答案。

**训练与推理**

训练或拟合阶段首先从训练实例中分解原子答案，并以原子金状态作为监督信号拟合校准器。Logical-SATA 使用完整的 $2{,}400$ 个训练实例；Logical-CommonsenseQA 抽取 $2{,}400$ 个训练实例，并在四种逻辑设置间保持平衡，以控制两套基准的校准数据规模。原文没有报告对 Llama-3.1-8B-Instruct 的参数更新，因此该框架应理解为冻结语言模型、只学习轻量校准映射。

测试时，对每个实例依次执行确定性选项解析、原子去重、正负假设成对打分和校准。然后建立二元变量 $y_a$ 与 $x_i$：AND 的线性约束等价于 $x_i=y_1\land y_2$，OR 等价于 $x_i=y_1\lor y_2$，Neither/Nor 等价于 $x_i=\neg y_1\land\neg y_2$；再加入 $\sum_i x_i=1$ 并优化全局证据目标。输出唯一的 $x_{\hat{\imath}}=1$ 所对应的选项；未校准变体保持相同流程，只把 $s_{C,\mathrm{cal}}^{\pm}(a)$ 替换为 $s_{C,\mathrm{raw}}^{\pm}(a)$。

**复现信息**

所有报告实验使用 Llama-3.1-8B-Instruct，原子置信度提取温度为 $0.7$；ILP 由 Gurobi Optimizer 13.0.2 求解。直接提示基线与结构化推断结果均取五次运行的平均值，随机种子为 $42$；这些设置关系到方差和结果复现，但不是方法本身的组成部分。

公平解释结果时需要注意，方法依赖训练集原子标签来拟合校准器，并依赖数据构造保证每题恰有一个逻辑有效选项；若实际任务允许零个或多个正确选项，约束 $\sum_i x_i=1$ 必须修改。共享原子的规范化匹配也很关键，因为该框架假设同一原子在一个实例中只对应一个 $y_a$；原文选项可被确定性解析，但未说明面对隐式算子、超过两个原子或解析歧义时的扩展方案。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- Logical-CommonsenseQA：用于考查常识原子判断与显式逻辑组合。每个样本包含一个问题和四个复合选项，每个选项由两个原子答案经 $\mathrm{And}$、$\mathrm{Or}$ 或 $\mathrm{Neither/Nor}$ 连接。共 19,996 个样本，按 11,996/6,000/2,000 划分训练集、开发集和测试集，并在四种设置间均衡分布：三种单一算子设置和一种候选项可含不同算子的 $\mathrm{Mixed}$ 设置。测试集又分为各 1,000 条的人工验证子集 $\mathrm{HV}$ 与非验证子集 $\mathrm{NV}$；正文主结果使用 $\mathrm{HV}$，$\mathrm{NV}$ 结果置于附录。
- Logical-SATA：本文从 SATA-Bench 的人工标注训练分区构造，用于检验结构化逻辑组合能否迁移到基于段落的阅读理解，而非只适用于常识问答。作者去重后保留至少含两个正确答案和三个错误答案的源问题，从 1,390 个合格问题中选择 1,350 个，以正确、错误原子答案配对生成有效选项和干扰项。最终得到 5,400 个复合选择题，按 2,400/1,000/2,000 划分训练集、开发集和测试集，并在 $\mathrm{And}$、$\mathrm{Or}$、$\mathrm{Neither/Nor}$ 和 $\mathrm{Mixed}$ 四种设置间均衡分布。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Macro-F1**

先分别计算各类别的 F1，再对类别等权平均；它降低类别频率差异对总分的支配，更适合比较不同逻辑设置或答案类别上的均衡预测能力。 （越高越好，因为更高值表示模型在各类别上兼顾了精确率与召回率。）

</div>
<div class="metric-item" markdown="1">

**Brier score**

衡量原子答案预测概率与二元真实标签之间的均方误差，主要用于评估原子证据的概率校准质量，而不是最终复合选项的分类表现。 （越低越好，因为预测概率越接近真实标签，平方误差越小。）

</div>
<div class="metric-item" markdown="1">

**log loss**

以对数惩罚预测概率与原子真实标签的不一致；对高置信度错误惩罚尤其大，用于检查原子评分是否给出了可靠概率。 （越低越好，因为较低损失意味着真实标签获得了更高预测概率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Logical-CommonsenseQA-HV：最强直接提示与结构化推断

<div class="result-value" markdown="1">

最强直接提示的 Macro-F1 为 48.3；配对多项选择原子证据加全局约束推断达到 75.8，绝对提高 27.5 分；进一步使用相对校准后达到 77.0。

</div>

作者据此主张，先独立评估原子答案、再按逻辑算子组合，比让模型直接理解复合选项有效得多。分析上，27.5 分的增益支持“组合过程是主要瓶颈”，而 75.8 到 77.0 的较小增量说明主要收益来自结构化分解和约束推断，相对校准提供进一步改善。但该结果基于同一个 8B 模型和一个人工验证子集，不能单独证明该结论适用于其他模型规模、提示策略或开放式任务。

<div class="result-source" markdown="1">

来源：第 5.1 节 Main Results，Direct Prompting vs. Structured Inference；对应表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On the Logical-CommonsenseQA-HV split, macro-F1 for the strongest direct-prompting configuration is 48.3, whereas our paired multiple-choice evidence with globally constrained inference achieves 75.8, an improvement of 27.5 points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Logical-SATA：跨阅读理解场景的整体比较

<div class="result-value" markdown="1">

最强直接提示的 Macro-F1 为 47.0；配对多项选择结构化推断达到 72.2，绝对提高 25.2 分。摘要另称完整框架达到 75.6，但所给正文节选没有给出该数值对应的完整结果句或表格行，因此此处不将其作为有完整证据支持的细分比较。

</div>

该结果表明，结构化分解的优势不局限于常识合理性判断，在需要依据段落或文档判断原子答案的 Logical-SATA 上仍然明显。由于 Logical-SATA 是由 SATA-Bench 的已有人工标签经过规则化配对构造的，结果证明的是对这种复合选项构造的适应能力，而不是对任意自然产生的阅读理解问题都具有同等增益。

<div class="result-source" markdown="1">

来源：第 5.1 节 Main Results，Direct Prompting vs. Structured Inference；对应表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The same pattern holds for Logical-SATA benchmark, where paired multiple-choice structured inference obtains 72.2 macro-F1, compared to 47.0 for the strongest direct-prompting baseline.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 按逻辑算子分析：Neither/Nor

<div class="result-value" markdown="1">

在 $\mathrm{Neither/Nor}$ 条件下，最强直接提示在 Logical-CommonsenseQA 和 Logical-SATA 上分别只有 14.0 与 12.6 Macro-F1；配对多项选择结构化推断分别提升到 75.1 与 71.9，加入相对校准后进一步达到 76.8 与 73.4。

</div>

这是最能定位方法作用机制的结果：$\mathrm{Neither/Nor}$ 要求同时否定两个原子命题，直接提示几乎失效，而结构化方法可先保留每个原子的证据，再机械地执行否定与合取。作者将其解释为模型可能知道各原子答案是否成立，却不能稳定完成两个否定判断的组合。该结果支持这一解释，但没有直接测量模型内部是否真正“保留”了这些知识，因此机制结论仍属于由行为差异推断出的解释。

<div class="result-source" markdown="1">

来源：第 5.1 节 Main Results，Performance Across Logical Operators；对应表 1 和表 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The strongest direct-prompting baseline reaches only 14.0 macro-F1 on Logical-CommonsenseQA and 12.6 on Logical-SATA, whereas paired multiple-choice structured inference raises these to 75.1, and 71.9, respectively, and relative to 76.8 and 73.4.

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

- Llama-3.1-8B-Instruct 直接提示，采用零样本至三样本提示：模型直接看到并选择复合答案，因此它同时承担原子事实判断和逻辑组合；这是检验“显式分解是否必要”的核心对照。
- Llama-3.1-8B-Instruct 零样本思维链提示：允许模型在直接预测复合答案前生成推理过程，用来检验仅通过提示模型逐步思考，是否足以替代显式的原子证据评分与受约束组合。
- 配对多项选择原子证据加全局约束推断：这是未加入相对校准增强时的结构化方法版本。它可与直接提示比较整体结构化推断的价值，也可与相对校准版本比较校准步骤的增量作用。
- 配对多项选择原子证据、相对校准与全局约束推断：这是报告中表现最强的完整框架；它将每个原子答案的对比证据校准后，再依照算子语义进行全局选择。

**实验想回答的问题**

- 将原子答案的判断与逻辑组合显式分离，并通过受逻辑算子约束的全局推断选出唯一答案，能否比直接让同一语言模型判断复合选项获得更高的 Macro-F1？
- 该结构化方法的收益是否随逻辑算子而变化，尤其能否修复模型在 $\mathrm{Neither/Nor}$、$\mathrm{Or}$ 和混合算子条件下的组合推理失败？

**实验实现**

所有实验均使用 Llama-3.1-8B-Instruct，生成温度设为 0.7；校准器在训练集上拟合，最终结果在测试集上报告。每种配置运行五次，主结果给出五次运行的均值与标准差。正文比较 Logical-CommonsenseQA 的人工验证测试子集 $\mathrm{HV}$ 和 Logical-SATA 测试集；Logical-CommonsenseQA 的 $\mathrm{NV}$ 结果以及替代评分策略置于附录。所给节选没有列出提示模板、校准器类型、求解器设置、各次运行的随机性来源或完整标准差数值，因此这些实现细节仍需查阅附录与原表。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 相对校准的增量作用：Logical-CommonsenseQA-HV | 在配对多项选择证据与全局约束推断已经启用时，相对校准将 Macro-F1 从 75.8 提高到 77.0，绝对增加 1.2 分。 | 这一比较近似隔离了相对校准的附加价值：校准有帮助，但远小于结构化方法相对直接提示的 27.5 分提升。不过，所给节选未说明两个版本除校准外是否完全相同，也未给出显著性检验，所以不能仅凭均值差断言 1.2 分提升具有统计显著性。 | 第 5.1 节 Main Results，Direct Prompting vs. Structured Inference；对应表 1<br><span class="experiment-evidence">Relative calibration further increases the performance to 77.0.</span> |
| 算子条件分析：And 相对于困难算子 | 在 $\mathrm{And}$ 设置上，Macro-F1 在 Logical-CommonsenseQA 中由 70.8 升至 72.4，在 Logical-SATA 中由 70.9 升至 73.6，绝对增益分别为 1.6 和 2.7 分，明显小于 $\mathrm{Neither/Nor}$ 上超过 59 分的提升。 | 这不是移除单个组件的标准消融，而是按算子切分的诊断实验。它隔离了逻辑形式对收益的影响：直接模型本已较擅长两个肯定判断的合取，因此显式组合的边际价值较小；困难算子上的大幅改善更符合“方法修复组合规则执行”的解释，而非简单提高所有预测。 | 第 5.1 节 Main Results，Performance Across Logical Operators；对应表 1 和表 2<br><span class="experiment-evidence">On And, gains are smaller: 70.8 to 72.4 on Logical-CommonsenseQA and 70.9 to 73.6 on Logical-SATA.</span> |

**定性案例**

- Figure 6 的 Logical-SATA 混合算子样例展示了同一原子内容如何因算子不同而改变有效性：选项 B 的两个原子标签均为 $1$，在 $\mathrm{Or}$ 下满足 $1\lor1=1$，因此是金答案；选项 C 使用相同的两个肯定原子，却通过 $\mathrm{Neither/Nor}$ 组合，得到 $\neg1\land\neg1=0$，因而无效。这个例子直观说明，仅判断原子内容是否正确还不够，系统必须显式执行候选项自己的逻辑算子；它用于解释任务结构，不构成总体性能证据。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution improves LLM logical reasoning by decomposing compound answer options and recomposing atomic judgments under explicit logical constraints.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`38a850d49b58c8e65dc8482f9aa25f34625465e2b41396a48c3483295d76d45e`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
