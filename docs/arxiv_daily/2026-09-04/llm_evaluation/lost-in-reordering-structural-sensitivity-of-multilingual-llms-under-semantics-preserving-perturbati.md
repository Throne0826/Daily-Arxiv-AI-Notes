---
title: "[论文解读] Lost in Reordering: Structural Sensitivity of Multilingual LLMs under Semantics-Preserving Perturbations"
description: "[arXiv 2609.03511][LLM 评测] 本文以印地语和马拉雅拉姆语数学推理题为对象，检验多语大语言模型在语义不变但成分顺序或语态改变时能否保持一致推理，并据此揭示模型对表层句法结构的敏感性。"
arxiv_id: "2609.03511"
announcement_date: "2026-09-04"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:35:56.219812+00:00"
source_sha256: "56a2aeb354cf64ec5cb0f5a04ab1d4f32f72c6ab59442ab1ae615c08771411db"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 机制与可解释性"
  - "LLM 其他"
  - "多语言大语言模型"
  - "结构鲁棒性"
  - "组合语义推理"
  - "自由语序语言"
  - "数学推理"
  - "成分重排"
  - "主动—被动转换"
  - "机制可解释性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2609.03511</p>

# Lost in Reordering: Structural Sensitivity of Multilingual LLMs under Semantics-Preserving Perturbations

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Karthika Nhayakkat, Rajat Verma, Maharaj Brahma, Vetcha Gnana Mahesh, Maunendra Sankar Desarkar, Ganesh Ramakrishnan, Rohit Saluja</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03511v1) · [PDF 下载](https://arxiv.org/pdf/2609.03511v1) · **关键词** 多语言大语言模型, 结构鲁棒性, 组合语义推理, 自由语序语言, 数学推理, 成分重排, 主动—被动转换, 机制可解释性<br>


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

本文以印地语和马拉雅拉姆语数学推理题为对象，检验多语大语言模型在语义不变但成分顺序或语态改变时能否保持一致推理，并据此揭示模型对表层句法结构的敏感性。

**不用术语来说**：同一道数学题即使换一种合乎语言习惯的说法，人物、数量关系和正确答案也不会改变，模型却可能从答对变成答错。例如，论文图1中的印地语题只调整了词组成分的位置，模型答案便从正确的18美元变为14美元。现实中的印地语和马拉雅拉姆语允许说话者为强调、焦点或表达便利而改变语序，因此，一个真正理解题意的模型不应把常见的表达变化误当成数学关系发生了变化。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将研究焦点从词汇替换推进到受语言学约束的结构变化，构造IndicReStruct基准，包括成分重排的GSM8K-Reordered和主动—被动语态转换的GSM8K-Voice，用于比较语义等价输入下的推理一致性。
- 作者不只测量六个大语言模型在结构扰动后的性能下降，还通过错误分类与残差流激活修补追查失败来源，从而考察推理错误是否与实体—数量对应关系受扰以及模型内部特定层、特定词元类别有关。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于多语言大语言模型鲁棒性与数学推理研究。核心问题是：当同一个数学题的语义保持不变、但句法结构发生变化时，模型是否仍能稳定完成推理。研究特别关注印地语和马拉雅拉姆语等相对自由语序语言，因为这些语言允许在一定句法或语篇约束下调换成分，但成分不能被任意打乱。论文将这种语义保持的结构变化施加于数学文字题，并结合模型评测、错误分析和机制可解释性分析，考察模型是否真正依赖组合语义，还是依赖训练数据中更常见的表层语序模式。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**组合语义推理**

组合语义推理是指模型系统地组合词语和短语的含义来得到整句或题目的意义。若输入只是改变句法表达而没有改变语义，具备这种能力的模型应保持相近的推理行为。

</div>
<div class="concept-item" markdown="1">

**相对自由语序**

相对自由语序语言允许句子成分在一定条件下改变排列顺序，同时保留基本命题意义。这里的“自由”并不意味着所有随机排列都合乎语法，因此论文使用受语言学约束的成分重排，而不是任意打乱词语。

</div>
<div class="concept-item" markdown="1">

**思维链提示**

思维链提示要求模型先生成中间推理步骤，再给出最终答案，常用于数学和逻辑任务。本文主要考察思维链及其少样本和“先规划后求解”变体在结构扰动下是否仍然有效。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定来源于 GSM8K 的数学文字题，并将其翻译或呈现为印地语或马拉雅拉姆语。构造两类语义保持的输入变体：一类对受句法和语篇约束的成分进行重排，形成 GSM8K-Reordered；另一类将主动句转换为被动句，形成 GSM8K-Voice；二者共同构成 IndicReStruct。模型输入是原始或结构扰动后的数学题，输出是数学答案及可选的中间推理步骤；主要比较同一模型在结构变化前后的正确性。该设置假定扰动确实保持题目的数学语义和正确答案不变，并进一步使用模型内部激活的干预分析结构变化造成失败的可能机制。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$LLM$**

大语言模型（Large Language Model），本文中指用于多语言理解和数学推理的生成式语言模型。

</div>
<div class="notation-item" markdown="1">

**$IndicReStruct$**

本文提出的结构扰动基准数据集总称，包含 GSM8K-Reordered 和 GSM8K-Voice 两个变体，并覆盖印地语和马拉雅拉姆语。

</div>
<div class="notation-item" markdown="1">

**$GSM8K\text{-}Reordered$**

对 GSM8K 数学文字题实施受控成分重排后得到的数据集；题目语义和数学答案保持不变，但表层语序发生变化。

</div>
<div class="notation-item" markdown="1">

**$GSM8K\text{-}Voice$**

将 GSM8K 题目中的主动—被动语态进行转换后得到的数据集；其目标是测试语态结构变化对数学推理的影响。

</div>

</div>

**直接相关的工作**

- **Singh et al. (2024)，关于 Indic 语言中的语序适应**: 该工作表明，使模型适应目标语言的语序会影响低资源语言上的性能，为本文在印地语和马拉雅拉姆语中研究受控语序变化提供了直接动机。本文进一步把问题限定为数学推理，并比较语义等价结构变化前后的性能差异。
- **Wang et al. (2025)，关于句子结构变化对对比预测的影响**: 该工作报告句子结构变化会影响人类和大语言模型的预测，且模型受到的影响更强。本文将这一现象扩展到多语言数学推理，并通过成分重排、主动—被动转换及激活修补分析模型失败是否与内部实体—数量对齐有关。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

多语大语言模型正在被用于问答和数学推理，但真实交流并不总采用训练数据中常见的规范书面语序。对印地语、马拉雅拉姆语等相对自由语序且形态丰富的语言，使用者经常在不改变命题意义的情况下移动句子成分，或以不同语态表达同一事件。如果模型依赖固定语序来判断谁拥有哪个数量、执行何种操作，它在口语化或非典型表达中就可能产生不稳定答案；这意味着标准测试集上的高准确率未必代表模型已经获得与表达形式无关的推理能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **标准多语推理基准评测**：既有评测通常让模型回答采用规范、固定表达形式的多语数学或逻辑题，并以最终答案准确率衡量推理能力。这类评测可以比较不同模型或语言的总体表现，但往往没有为同一语义构造多个句法版本，因此难以区分模型是在理解数量关系，还是在利用训练中频繁出现的语序模式。
- **词汇、社会文化与一般表面形式扰动评测**：相关研究通过替换词语、改变提示的表面形式或引入社会文化变化，观察模型预测是否稳定；另有工作开始研究句子结构变化及组合关系推理。这些方向已表明模型可能依赖统计捷径，但论文指出，它们尚未系统覆盖自由语序语言中受约束、语义保持且语言学上合理的成分重排与语态转换。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 标准基准主要测量单一规范表述上的正确率，缺少原句与语义等价结构变体之间的配对比较；其后果是模型即使依靠表层结构规律获得正确答案，也可能被误判为具有稳健的组合语义推理能力。
- 既有鲁棒性研究更多关注词汇或一般表面扰动，对印地语、马拉雅拉姆语这类相对自由语序语言中的受控结构变化研究不足，也较少进一步定位结构变化为何会破坏推理；因此尚不清楚错误来自语义内容丢失、实体与数量错配，还是模型内部表征对非典型句法形式适应不足。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一个语言学上受约束的配对测试框架：在保持事件、实体、数量关系和答案不变的前提下，分别改变成分顺序或主动—被动语态，并跨模型、提示策略及微调条件检验多语推理的一致性。同时，对性能下降的内部机制也缺乏因果性分析，尤其不知道原始表达中的有效内部激活能否修复结构扰动输入的错误预测，以及哪些Transformer层和词元类别最关键。

</div>
<div markdown="1"><span>核心问题</span>

当同一数学推理问题以语义等价但句法结构不同的印地语或马拉雅拉姆语形式呈现时，当前多语大语言模型能否维持相同的正确推理；若不能，失败主要表现为何种语义关系错乱，并由模型内部哪些层级和词元表征所影响？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是建立严格的“同义对照”：如果只改变语序或语态而不改变题目的数量事实与答案，那么两个版本之间的性能差异就可更直接地归因于结构敏感性，而不是知识难度或词义变化。进一步把原始版本的残差流激活替换到重排版本中，相当于在模型内部逐层注入原句形成的表征；如果某一层或某类词元的替换能恢复正确答案，就能为该内部位置参与结构稳健推理提供比单纯相关性观察更强的因果证据。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<p class="paper-minor-label">关键流程</p>

原文未明确报告完整流程。

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

原文未明确报告。

**训练与推理**

原文未明确报告。

**复现信息**

原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- GSM8K及其印地语、马拉雅拉姆语结构扰动版本：原题作为对照；GSM8K-Reordered对题目进行保持语义的受约束成分重排；GSM8K-Voice进行主动—被动语态转换，用于测试模型是否依赖特定表面句法形式。微调实验将原始与扰动问答对合并为训练集和验证集，原文报告两者各有11,956和2,990个样本，但未明确说明这两个数字分别对应哪一数据变体或具体划分。
- Hindi ARC-Challenge：印地语多项选择科学问答测试集，共1,150个样本；原题与重排题进行比较，用于检验结构敏感性是否能推广到GSM8K之外的任务和数据领域。
- GSM8K-Reordered质量评估子集：GSM8K测试集seed 42中的1,319个重排实例，用于评估语言自然性、语义保持和可解性；另从三个质量类别各抽取20个实例进行人工评估。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**答案准确率**

按照GSM8K标准，抽取指定分隔符“#####”后的最终数值，并在归一化后与标准答案匹配；匹配则判为正确。 （越高越好，因为它直接衡量最终数学答案是否正确。）

</div>
<div class="metric-item" markdown="1">

**准确率绝对下降**

重排或语态转换条件相对于原始题目的准确率差值，用于量化结构扰动带来的性能损失。 （下降幅度越小越好，表示模型对语义等价结构变化更稳健。）

</div>
<div class="metric-item" markdown="1">

**均值与标准差**

重排结果在五次不同生成中的平均准确率及其波动，反映平均性能和生成稳定性。 （均值越高且标准差越小越好；它描述重复生成的稳定性，但不是新的任务质量指标。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 印地语与马拉雅拉姆语的重排题：六个模型、四种提示策略

<div class="result-value" markdown="1">

所有模型和提示条件下，GSM8K-Reordered相较原始题目均出现准确率下降。印地语中，零样本CoT下Llama-3.1-8B-it从56.63%降至25.42%，下降31.21个百分点；Plan-and-Solve下Param-2-17B-A2.4B从66.49%降至33.41%，下降33.08个百分点。马拉雅拉姆语中，零样本CoT下Param-2-17B-A2.4B从71.34%降至49.87%，下降21.47个百分点。

</div>

这说明模型通常不能把“同一个数学问题的另一种句法表达”当作完全等价输入处理。结果支持作者关于表面句法敏感性的判断，但不能单独证明所有错误都来自语言理解；不同模型、提示格式和语言的原始能力也可能影响下降幅度。

<div class="result-source" markdown="1">

来源：第5节 Results；表2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across all evaluated models and prompting settings, we observe a consistent degradation in reasoning performance when the input questions undergo semantically preserving reordering.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 跨任务泛化：印地语ARC-Challenge重排测试

<div class="result-value" markdown="1">

在Hindi ARC-Challenge上，Gemma-2-27B-it和Gemma-4-12B-it的四种提示策略均在重排题上低于原题。例如，Gemma-2-27B-it的三样本CoT准确率由87.65%降至84.09%，下降3.56个百分点；Gemma-4-12B-it由91.57%降至88.00%，下降3.57个百分点。

</div>

这一结果表明结构敏感性不只出现在GSM8K数学题，也能在印地语多项选择科学问答中观察到。不过该实验只涉及两个模型和一个语言，且下降幅度小于部分GSM8K条件，因此只能说明存在一定的跨任务迹象，不能据此确定普遍的性能损失规模。

<div class="result-source" markdown="1">

来源：第5节 Results；表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Table3 shows the results, where we observe a similar decrease in performance by both models, across all prompting techniques for the reordered questions, compared to the original questions.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 参数高效微调：Gemma-2-9B-it在重排与语态数据上的适配

<div class="result-value" markdown="1">

DoRA优于LoRA：GSM8K-Reordered准确率从41.59%提升至46.13%，GSM8K-Voice准确率从40.94%提升至51.25%。但作者报告两种微调变体仍低于相应的零样本提示基线，因此仅使用结构扰动数据进行轻量微调并未恢复充分的组合语义鲁棒性。

</div>

该比较说明DoRA在本实验设置中比LoRA更有效，但不能把这种优势解释为DoRA普遍优于LoRA，因为实验只涉及一个模型、有限数据和特定语言变体。微调仍低于零样本基线，提示模型可能学习了扰动表面模式，而没有获得可迁移的语义不变性。

<div class="result-source" markdown="1">

来源：第5节 Results；表5和表6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For parameter-efficient fine-tuning, DoRA substantially outperforms LoRA, improving performance from 41.59% to 46.13% for GSM8k-Reordered and from 40.94% to 51.25% for GSM8k-Voice data.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验覆盖的语言主要是印地语和马拉雅拉姆语，模型、任务和扰动类型也有限；因此结果支持这些设置下的结构敏感性，不能直接推广到所有多语言模型、语言或句法变换。
- 微调实验使用规模较小且领域特定的语料；作者认为模型可能过拟合局部句法重排模式。与此同时，所给摘录未提供语态转换表4的具体数值、激活修补实验的定量结果以及完整训练划分对应关系，相关结论仍需核对原文完整表格和附录。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 原始GSM8K题目：与语义保持扰动版本配对，是判断性能下降是否由结构变化引起的直接对照。
- GSM8K-Reordered：受约束成分重排条件，检验模型对不同词序或成分排列的适应能力。
- GSM8K-Voice：主动—被动语态转换条件，检验模型在另一种语义等价句法变换下的推理稳定性。
- 提示与参数高效微调比较：零样本、单样本、三样本CoT及Plan-and-Solve提示用于比较推理提示策略；LoRA与DoRA用于比较轻量适配方法。

**实验想回答的问题**

- 在保持题目语义不变的情况下，印地语和马拉雅拉姆语中的成分重排与主动—被动语态转换是否会系统性降低多语言大语言模型的数学推理准确率？
- 这些结构扰动造成的错误主要表现为何种推理失效，提示学习与轻量参数高效微调能否恢复模型的结构鲁棒性？

**实验实现**

实验覆盖Gemma-2-9B-it、Gemma-2-27B-it、GPT-OSS-20B、Llama-3.1-8B-it、Param-2-17B-A2.4B和Qwen3-30B-A3B六个开源指令微调模型，Param-2采用非思考模式。提示条件包括零样本、单样本和三样本CoT，以及Plan-and-Solve。推理固定随机种子为50、批大小为8、最大输入长度为2048个token，最多生成512个新token；默认贪心解码，温度为0，也支持运行时温度采样。准确率按最终答案而非中间推理步骤判定。Gemma-2-9B-it另分别在印地语重排和语态变体上进行LoRA或DoRA参数高效微调，并使用原始及扰动问答对进行80/20训练—验证划分。质量标注先由大语言模型按预定义词类标注，再由语言专家核验和修订。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 提示策略对照：零样本、单样本、三样本CoT与Plan-and-Solve | 重排造成的下降在四类提示策略中持续出现，且没有一种提示策略稳定消除该问题；例如印地语中Gemma-2-9B-it的零样本CoT由76.30%降至61.78%，三样本CoT由74.75%降至58.12%。 | 该对照隔离了提示信息量和推理组织方式的影响，说明增加示例或要求显式规划并不能可靠地使模型适应语义等价的成分重排。它不能证明所有其他提示设计都无效，因为实验只覆盖这四种策略。 | 表2表注；第5节 Results<br><span class="experiment-evidence">Reordered results report mean ± std across five different generations.</span> |
| LoRA与DoRA参数高效微调对照 | DoRA相对LoRA在重排数据上提升4.54个百分点，在语态数据上提升10.31个百分点；但原文未在所给摘录中报告完整的零样本对应数值，因此无法进一步计算其相对零样本的精确差距。 | 这个对照主要测试低参数适配机制本身，而不是测试数据规模、模型架构或更广泛训练语料。DoRA更高的结果说明其在该设置下更适合适配扰动数据，但仍不足以证明已经学会了跨结构的深层语义对应关系。 | 第5节 Results；表5和表6<br><span class="experiment-evidence">Despite this improvement, both fine-tuned variants underperform the corresponding zero-shot prompting baselines, indicating that lightweight adaptation on structurally perturbed data alone is insufficient to improve compositional semantic robustness.</span> |

**定性案例**

- 表8的实体—数量错配案例中，原始印地语题目正确推理出Jessa为20岁、Jone为25岁、Mary为23岁，总和为68；重排后模型却将关系方向链式反转，推导出15岁和13岁，答案变为48。该案例显示错误不是简单算术失误，而是重排后人物实体与年龄关系的绑定方向发生了改变。原文还展示了答案抽取错误、CoT语言不匹配和错误数学运算等类别，但表8每类仅给出代表性样例，不能据此估计各类错误的总体比例。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper benchmarks multilingual LLM mathematical reasoning under semantics-preserving syntactic perturbations and uses activation patching to analyze the resulting failures.; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`56a2aeb354cf64ec5cb0f5a04ab1d4f32f72c6ab59442ab1ae615c08771411db`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
