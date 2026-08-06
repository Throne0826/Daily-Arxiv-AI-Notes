---
title: "[论文解读] Easy to Complete, Hard to Choose: Investigating LLM Performance on the ProverbIT Benchmark"
description: "[arXiv 2608.04670][LLM 评测] 本文通过意大利谚语基准 ProverbIT，检验大语言模型能否把“记得谚语结尾”转化为“在干扰项中正确选择并在正确答案缺席时拒绝选择”的辨别推理能力。"
arxiv_id: "2608.04670"
announcement_date: "2026-08-06"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:51:43.761948+00:00"
source_sha256: "a3997c80a9e620f782bb7051cd6c1f601d316431f9e9b4b5552ecd8d48422aa4"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "大语言模型"
  - "大推理模型"
  - "意大利语谚语"
  - "比喻性语言理解"
  - "谚语补全"
  - "多项选择评测"
  - "文化语言知识"
  - "ProverbIT"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.04670</p>

# Easy to Complete, Hard to Choose: Investigating LLM Performance on the ProverbIT Benchmark

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Enrico Mensa, Lorenzo Zane, Calogero Jerik Scozzaro, Matteo Delsanto, Tommaso Milani, Daniele Paolo Radicioni</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04670v1) · [PDF 下载](https://arxiv.org/pdf/2608.04670v1) · **关键词** 大语言模型, 大推理模型, 意大利语谚语, 比喻性语言理解, 谚语补全, 多项选择评测, 文化语言知识, ProverbIT<br>


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

本文通过意大利谚语基准 ProverbIT，检验大语言模型能否把“记得谚语结尾”转化为“在干扰项中正确选择并在正确答案缺席时拒绝选择”的辨别推理能力。

**不用术语来说**：模型看到一句熟悉谚语的前半句时，往往可以顺势补出后半句，但这并不等于它真正理解了谚语。更严格的测试是给出若干读起来合理的候选结尾，尤其故意不提供真正结尾，观察模型能否排除表面相似的选项并选择“以上皆非”。这一区分关系到我们应把模型的成功解释为语料记忆，还是可迁移的文化与语义理解。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出 ProverbIT，以人工设计的意大利谚语候选结尾构造对照任务，从直接补全、含正确答案的多项选择逐步过渡到不含正确答案的多项选择，使谚语知识检索与辨别推理能够被分开考察。
- 作者比较传统大语言模型与大型推理模型，并分析 DeepSeek R1 和 Qwen 3 的思维链，以定位模型在正确答案缺席时的失败模式，包括偏向字面同义项、推理中提到正确结尾却未发现其不在选项中，以及推理结论与最终答案不一致。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型评测与比喻性语言理解研究。谚语是由文化经验固化而成的常见短句，其整体含义往往不能仅由字面词义推出，因此既考查模型能否从训练语料中提取熟悉表达，也考查模型能否理解表达的整体语义并排除貌似合理的干扰项。现有通用基准覆盖释义识别、语法可接受性、自然语言推断、数学、编程和逻辑推理等任务，意大利语也已有 CALAMITA 与 Evalita-LLM 等原生基准；但意大利语谚语及其文化知识在综合评测资源中仍缺乏专门测试。ProverbIT 因而把同一批谚语置于自动补全和多项选择环境中，以区分模式记忆、正确选项识别以及正确答案缺失时的判别能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**谚语与比喻性语言**

谚语是广为流传、通常表达一般经验、智慧或建议的固定短句。其文化含义可能超出组成词的字面意义，因此，仅生成熟悉的后半句不必然证明模型理解了整句。

</div>
<div class="concept-item" markdown="1">

**大语言模型与大推理模型**

大语言模型（LLM）根据上下文预测并生成后续文本；大推理模型（LRM）是论文用于指称更强调多步推理能力的一类模型。本文同时评估二者，以检验显式或增强的推理能力能否缓解谚语选择中的失败。

</div>
<div class="concept-item" markdown="1">

**生成式补全与判别式选择**

生成式补全要求模型直接写出谚语结尾，可能依赖训练语料中的高频共现模式；判别式选择则要求模型比较多个候选项并排除干扰项。当正确结尾被移除并加入“以上皆非”时，模型还必须识别候选集合本身不含正确答案。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

ProverbIT 包含 100 道围绕意大利语谚语设计的题目，并用于考查 13 个前沿模型。对每条谚语，输入提供其未完成部分或相应的多项选择题；论文设置三种任务：直接生成正确结尾、在含有正确结尾的候选项中选择答案，以及在移除正确结尾并提供“None of the others”选项时作出选择。第一种设置主要检验模型是否能够访问或复现已知谚语，第二种设置进一步要求比较由人工设计的语义或句法上看似合理的结尾，第三种设置则检验模型能否抵制字面近义干扰，并明确判断所有具体候选项均不正确。该问题的核心假设是：若模型真正掌握谚语的固定形式与文化语义，它不仅应当能够补全谚语，也应能在候选项变化时稳定识别正确结尾是否存在；反之，补全成功但选择失败更符合依赖统计共现或记忆模式的解释。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Liu et al. [23], MAPS**: 这是与本文最直接相关的谚语理解基准：MAPS 在六种语言的对话语境中评估谚语理解，并发现模型“知道”某些谚语并不等于能够进行语境推理，面对比喻性谚语或要求选择错误答案时尤其困难。ProverbIT 将关注点收窄到意大利语，并通过补全、含正确答案的选择题以及不含正确答案的选择题，对记忆提取与候选判别之间的差异进行更受控的比较。
- **Kim et al. [19], 六语言习语及释义数据集**: 该工作研究多语言习语处理，认为模型表现来自内部知识检索、上下文线索与推理的混合，而非单纯记忆，并指出高资源语言与较低资源语言之间存在差距。本文以谚语结尾为对象，通过操纵候选项是否包含标准答案，进一步追问这种知识检索与语义推理能否在选择任务中保持一致。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

谚语是依赖共同文化经验的固定表达，理解它既需要词汇访问，也需要把握非字面含义。现有模型在常规语言任务上的高表现，不能直接证明其能够可靠处理这类文化表达；如果模型只凭高频共现模式作答，那么在需要排除看似合理选项或确认正确答案缺席的实际决策场景中，就可能表现出不可靠的判断。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **直接谚语补全**：向模型提供谚语前半句，要求自由生成后半句。该形式主要测试模型能否通过训练语料中的固定搭配和下一词预测模式检索出熟悉表达。
- **含正确答案的多项选择评测**：向模型同时提供正确结尾和若干在语义或句法上看似合理的人工干扰项，要求模型比较候选项并选出标准结尾；相较直接补全，它增加了辨别与排除步骤。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 直接补全的成功可能主要来自对高频固定字符串的记忆，因而无法区分模型是在理解谚语的文化性、比喻性含义，还是仅根据统计共现续写熟悉结尾。
- 只在候选集中始终放入正确答案，会弱化对否定性推理的检验：模型可能默认某个给定选项必然正确，而不核查真实结尾是否存在，因此该设置难以暴露其拒绝不充分候选项的能力缺陷。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

仍缺少一种针对意大利文化表达的受控评测，能够在同一批谚语上逐步改变作答形式，并特别设置真实结尾缺席且提供“以上皆非”的条件，从而将固定模式记忆、候选项辨别和正确答案缺席时的否定性推理区分开来；同时，也缺少对大型推理模型内部推理文本的分析，以解释它们为何可能已经回忆出正确结尾却仍选择错误选项。

</div>
<div markdown="1"><span>核心问题</span>

当意大利谚语任务从自由补全改为多项选择，并进一步移除正确结尾时，传统大语言模型和大型推理模型能否利用已掌握的谚语知识排除字面或句法上合理的干扰项、识别“正确答案不在选项中”，还是会继续依赖表面共现和字面相似性作答？

</div>
<div markdown="1"><span>作者直觉</span>

同一条谚语在三种递进设置中的表现差异可以充当诊断信号：若模型能补全谚语，却在正确结尾缺席时被近义干扰项吸引，就说明知识可能已经被检索出来，但没有被稳定用于候选核验。人工控制干扰项，再检查思维链是否提到真实结尾，可以进一步判断错误发生在知识回忆、语义比较、缺席检测还是最终答案输出环节。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文的方法不是训练新模型，而是构建诊断性基准 ProverbIT，并以统一提示对现有模型进行推理评测。作者先从 200 条常见意大利谚语中筛选 100 条，将每条谚语人工拆分为开头和标准结尾，再围绕标准结尾编写四类错误选项：近音但荒谬、字面同义、语义相反以及重言式或平凡续写。在核心多项选择设置中，这四个选项全部错误，另设“以上皆非”作为唯一正确答案；因此，模型既要知道谚语的固定结尾，也要判断该结尾是否真的出现在候选项中。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 谚语筛选与切分

三名以意大利语为母语的作者人工选出其中 100 条最常用的谚语，并将每条谚语拆分为开头与标准结尾。切分点需同时保证开头语义连贯，并使标准续写清晰且无歧义。

<div class="method-step__io" markdown="1">

**输入**：文献来源中的 200 条常见意大利谚语。<br>
**输出**：100 个由“谚语开头”和“标准结尾”组成的基础样本。

</div>

**直观理解**：这一步相当于把一句熟悉的固定表达截断，让模型补出后半句。切分不能过早或过晚，否则题目可能含糊，或者仅凭语法就能猜出答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 诊断性干扰项构造

作者为每条谚语人工构造四个错误结尾：A 类与标准结尾声音相似但通常荒谬，B 类是标准结尾的非近音字面同义改写，C 类表达与标准结尾相反并尽可能保留音韵，D 类是无近音关系的重言式或平凡陈述。B 类只改写字面含义，而不复述谚语的隐喻含义。

<div class="method-step__io" markdown="1">

**输入**：每条谚语的开头及其标准结尾。<br>
**输出**：每条谚语对应四个具有不同诱导机制的错误选项。

</div>

**直观理解**：四类选项分别测试模型是否会被押韵、字面近义、反义结构或看似合理的废话吸引。尤其是字面同义项看起来“意思差不多”，却不是约定俗成的原句，可用于区分固定表达记忆与严格选择能力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多项选择题与提示生成

作者将样本填入固定提示模板，要求模型“准确”补全谚语、相信选项不存在拼写错误，并且只能输出 A、B、C、D 或 E 中的一个字母。由于 A 至 D 均为人工编写的错误结尾，核心无正确结尾设置下的期望答案始终为 E。

<div class="method-step__io" markdown="1">

**输入**：谚语开头、四个错误结尾以及“以上皆非”选项。<br>
**输出**：100 道五选一的意大利语 ProverbIT 题目及其统一判定目标。

</div>

**直观理解**：提示中强调“没有拼写错误”，是为了阻止模型把陌生选项解释成用户笔误并擅自修正。真正的难点不是随便挑一个最顺口的句子，而是发现熟悉的标准结尾根本不在列表中。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 跨模型推理评测

作者评测传统大语言模型、具备显式推理能力的大型推理模型和较小的本地模型；论文摘要说明评测覆盖自由补全、含正确答案的多项选择，以及不含正确答案的多项选择三种任务。所给章节只完整展示了第三种任务的提示，因此其余两种任务的具体选项组织和提示模板在当前材料中未明确报告。

<div class="method-step__io" markdown="1">

**输入**：ProverbIT 题目、相应任务提示，以及 13 个被测前沿或本地模型。<br>
**输出**：各模型在不同任务形式下的回答，用于比较“知道标准谚语”与“能否在候选项中正确决策”之间的差异。

</div>

**直观理解**：三种任务像是逐步增加决策干扰：先看模型能否直接说出后半句，再看它能否从列表中选中原句，最后看它能否拒绝所有看似合理但实际错误的选项。这样可以避免把单纯记住谚语误判为真正理解并遵守题目约束。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。ProverbIT 是基准构建与推理评测工作，作者没有针对该数据集训练或微调模型，也没有提出需要优化的新损失函数；模型参数在评测期间保持不变。评价目标是观察模型在不同题型中是否产生预期补全或选项，而不是通过梯度更新最小化训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 四类对照干扰项**

A、B、C、D 四类错误续写分别控制音韵相似、字面同义、语义反转和平凡合理性，使不同错误选项对应不同的表层或语义诱因。所有选项均由作者人工编写，以保持谚语层面的语言自然性和诊断目的。

> 直观理解：普通随机错误答案往往一眼即可排除，无法说明模型为什么失败。这里让每种错误都以不同方式“像正确答案”，从而能够判断模型究竟依赖声音、字面意思，还是固定谚语知识。

**2. 正确答案缺席机制**

在所展示的核心多项选择任务中，标准谚语结尾不出现在 A 至 D 中，E“以上皆非”因而是全部 100 个样本的目标答案。该设计将标准结尾的回忆能力与候选项核验、拒绝错误选项的能力分离。

> 直观理解：模型即使记得完整谚语，也可能因为习惯从现有选项中挑一个最像的而答错。固定目标为 E 虽便于诊断“能否拒绝”，但也意味着结果可能受到位置偏好或恒定标签策略影响，解释时应结合其他任务设置，而不能单独等同于完整的谚语理解能力。

**3. 受约束的统一提示**

提示明确要求精确补全、声明选项无拼写错误、限制输出为单个选项字母，并禁止评论。这些约束减少自由生成格式差异，也抑制模型将人工干扰项误判为输入错误后自行改写答案。

> 直观理解：统一提示让不同模型面对尽量相同的考试规则，也让答案可以直接自动判定。额外说明并非装饰，而是针对作者观察到的模型行为：模型有时会假设用户写错了，从而绕开原本要测试的选择问题。

**训练与推理**

训练阶段不适用。推理阶段将每条谚语放入相应任务模板，提交给 13 个被测模型并收集回答；当前节选明确给出的无正确结尾模板要求仅返回 A 至 E 的字母，且每题的标准答案为 E。论文摘要还说明存在自由补全和含正确结尾的多项选择任务，用于先确认模型是否掌握谚语，再与无正确结尾条件比较；不过当前材料未提供这两种任务的完整推理模板、解码设置、重复运行次数或答案规范化规则。随后，作者汇总模型表现，并对两个大型推理模型的思维链进行错误分析，以研究模型在知道正确结尾时为何仍可能选择字面同义等干扰项。

**复现信息**

数据集包含 100 道题，由三名意大利语母语作者从 200 条常见谚语中筛选并人工构造干扰项。表 1 列出的 13 个模型为 Claude Sonnet 4、Claude Sonnet 4 Thinking、GPT-4o、GPT-o3、DeepSeek V3、DeepSeek R1、Gemini 2.5 Flash、Gemini 2.5 Pro、Qwen 3、Grok 3、Llama 4 Maverick、Mistral Small 3.1 和 Gemma 3，覆盖闭源前沿模型、推理模型与较小本地模型；已披露参数规模包括 DeepSeek V3 与 R1 的 671B、Qwen 3 的 235B、Llama 4 Maverick 的 400B、Mistral Small 3.1 的 24B 和 Gemma 3 的 27B，其余模型参数量标为未披露。数据集地址由原文脚注给出为 https://huggingface.co/datasets/emensa/proverbIT。当前节选未明确报告采样温度、最大生成长度、随机种子、每题调用次数、模型服务版本之外的运行日期、推理预算、评分脚本，以及思维链分析的标注者一致性；这些缺失信息会影响结果复现和模型间的严格公平比较。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ProverbIT 是核心评测集，包含 $100$ 道意大利语谚语多项选择题。每题给出谚语开头，但候选项不含真实结尾；模型需要从押韵或近音、同义、反义和可直接拼接等干扰类型中作答。它用于检验模型在缺少记忆答案这一直接选项时，能否依据谚语的文化性、惯用性和比喻意义进行选择。原文未明确报告训练集、验证集或测试集划分，实验看起来是在全部 $100$ 题上进行评测。
- Completion 是由同一批谚语构造的辅助任务：只提供谚语开头，要求模型直接生成准确的结尾。该任务主要检查模型是否记得这些谚语，从而区分“缺乏谚语知识”和“知道谚语但不会在干扰项中选择”两种失败原因。
- Base + true ending 是另一项由 ProverbIT 改造的辅助任务：保留原多选形式，同时加入真实谚语结尾作为新选项。它控制了题型因素，使研究者能够检查模型在正确答案明确出现时能否识别该答案，并将其与正确结尾缺席的 Base 任务直接比较。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**多项选择准确率**

用于 Base 和 Base + true ending，计算正确选择的题数占全部多选题的比例。每题独立调用模型三次，以多数票确定最终答案；若三个回答没有形成多数，则该题记为错误。该指标同时受到知识、推理、指令遵循和输出随机性的影响。 （越高越好，因为更高数值表示模型在更多题目上选中了评测所规定的正确选项。）

</div>
<div class="metric-item" markdown="1">

**基于编辑相似度阈值的 Completion 正确率**

作者使用 Python $\texttt{difflib}$ 的实现比较生成结尾与标准结尾，并在三次运行中至少两次超过 $0.8$ 阈值时判为正确。原文将该量称作 edit distance，却又规定“exceeds a threshold of 0.8”才正确，更像是归一化相似度；因此具体函数及方向仍需核对原代码或完整论文脚注。 （最终正确率越高越好；单次比较值按作者规则超过 $0.8$ 才支持判为正确。）

</div>
<div class="metric-item" markdown="1">

**错误类型分布**

在 Base 任务的错误答案中，分别统计近音或押韵项（A）、同义项（B）、反义项（C）和可直接拼接项（D）所占百分比。它不是总体能力分数，而是用于诊断模型失败时偏向哪类干扰项。 （没有统一的越高或越低越好方向；某一类型比例高表示模型错误集中于该干扰机制。对同义项而言，高比例支持模型偏向字面语义接近答案的诊断。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 最佳模型在三项任务上的总体表现

<div class="result-value" markdown="1">

作者报告 GPT o3 在 Base 上取得 $86.0\%$，同时在 Base + true ending 和 Completion 上分别达到 $98.0\%$ 与 $91.0\%$；按表格排序，它是核心 Base 任务表现最高的模型。

</div>

这表明显式推理较强的模型能够在真实结尾缺席时解决多数题目，但其 Base 表现仍低于正确结尾直接出现时的表现。该结果证明的是 GPT o3 在本基准和当前提示协议下具有最高准确率，不能单独证明它真正理解了谚语的文化或比喻意义，也不能把优势完全归因于推理机制。

<div class="result-source" markdown="1">

来源：Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GPT o3 86.0 98.0 91.0

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 非推理模型在正确结尾缺席时的性能下降

<div class="result-value" markdown="1">

作者以 GPT 4o 为例：Base + true ending 为 $92.0\%$，Completion 为 $88.0\%$，但 Base 仅为 $64.0\%$，相对加入真实结尾的多选条件下降 $28$ 个百分点。

</div>

同一模型能生成或识别真实结尾，却在该结尾不属于候选项时明显更难选择，这正是基准试图分离的能力缺口：记住固定表达并不等于能利用其整体含义排除诱人的干扰项。由于三个任务的输出形式和判分方式并不完全相同，最稳妥的证据是 Base 与 Base + true ending 的比较；Completion 的高分只能作为模型熟悉谚语的补充证据。

<div class="result-source" markdown="1">

来源：Table 2；Section 4.3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

GPT 4o 64.0 92.0 88.0

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Base 错误集中于同义干扰项

<div class="result-value" markdown="1">

DeepSeek R1 的错误分布中，同义项（B）占 $91.9\%$，近音项（A）与反义项（C）各占 $2.3\%$，可直接拼接项（D）占 $3.5\%$；表中其他高性能推理模型的错误也主要集中于同义项。

</div>

作者据此主张模型具有选择字面同义词的强偏差。分析上，这意味着模型即使能够回忆原谚语，也可能把“与真实结尾局部语义接近”误当作“最适合整条谚语的替代结尾”。不过该表给出的是错误内部的构成比例，而非该模型在全部题目上选择同义项的概率；当模型总错误数较少时，百分比还可能对少量样本较敏感。

<div class="result-source" markdown="1">

来源：Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

DeepSeek R1 2.3 91.9 2.3 3.5

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测仅含 $100$ 道意大利语谚语题，原文节选未报告数据划分、题目来源覆盖、人工一致性、统计置信区间或显著性检验。因此结论主要适用于该题集和该语言文化范围，模型间若干分差是否稳定仍需通过重采样、更多谚语及其他语言复验。
- 所有模型使用零样本提示、默认温度 $1.0$ 和三次多数票，但推理模型的思考预算并不完全一致，API 后端版本也可能变化。辅助任务与 Base 的选项数量或判分方法不同，Completion 所称“edit distance”的方向还存在表述歧义；这些因素限制了跨模型比较以及将任务差值严格归因于深层语义理解的力度。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 同机构的推理模型与非推理模型配对构成主要比较基线，包括 GPT o3 对 GPT 4o、Claude Sonnet 4 Thinking 对 Claude Sonnet 4，以及 DeepSeek R1 对 DeepSeek V3。该比较用于判断显式推理机制是否改善缺少真实结尾时的选项判断；但模型版本、训练语料和规模也可能不同，因此不能把差异完全归因于推理机制。
- Gemini 2.5 Pro、Qwen 3 等其他推理模型用于检验较强表现是否跨模型提供方成立。它们也揭示“推理模型”不是统一能力等级，例如 Qwen 3 的 Base 准确率明显低于 GPT o3。
- Grok 3、Gemini 2.5 Flash、Llama 4 Maverick 等传统或未被表中标为推理模型的前沿模型构成广覆盖基线，用来判断一般语言建模能力和谚语记忆能否自然转化为干扰项选择能力。
- Mistral Small 3.1 与 Gemma 3 是适合本地部署的小模型基线，用于观察较低计算资源条件下的表现。作者还预试了意大利语模型 Minerva，但因其经常无法连贯回答或遵循返回选项字母的格式而未纳入正式结果；因此它不能视为具有可比数值的正式基线。

**实验想回答的问题**

- 模型在意大利谚语结尾不直接出现在候选项中时，能否识别与谚语含义最相符的选项；这种选择能力与模型能否直接回忆谚语结尾是否存在明显差距？
- 显式推理模型（LRM）相较传统非推理大语言模型是否更能抵抗字面同义词等干扰项，以及错误选择和思维链暴露了何种决策偏差？

**实验实现**

实验评估 $13$ 个模型，所有任务均采用零样本提示，并通过 OpenRouter API 将请求分别发送；温度保持 OpenRouter 默认值 $1.0$。每道题运行三次，多选任务以多数票聚合，无多数票时按错误处理。Completion 同样运行三次，并采用阈值规则判定。GPT o3、Claude Sonnet 4 Thinking 和 Gemini 2.5 Pro 的思考预算设为 $2000$ token；DeepSeek R1 与 Qwen 3 不限制思考长度，并因可提供完整推理轨迹而被用于思维链分析。作者报告这两个模型的 $600$ 条思维链中只有 $22$ 条超过 $2000$ token，且其中一半最终答错，说明长度限制不是多数样本的直接约束，但这并不能排除不同模型推理预算和思维链可见性带来的可比性问题。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 向 Base 的候选项加入真实谚语结尾 | DeepSeek R1 从 Base 的 $74.0\%$ 提升到 Base + true ending 的 $100.0\%$，而其 Completion 为 $89.0\%$。 | 这一受控改动保留多选形式，只改变真实结尾是否可选，因此主要隔离“识别已知正确结尾”和“正确结尾缺席时选择语义替代项”之间的差异。提升说明该模型通常知道或能识别谚语，却会在必须接受所有候选项都不是真实结尾的条件下失误。它不是传统意义上移除模型组件的架构消融，也没有排除新增选项改变选项数量和猜测概率的影响。 | Table 2<br><span class="experiment-evidence">DeepSeek R1 74.0 100.0 89.0</span> |
| 移除多选候选项，改为直接补全谚语 | Llama 4 Maverick 在 Base 上仅为 $6.0\%$，但 Completion 达到 $88.0\%$；在加入真实结尾的多选任务中为 $75.0\%$。 | 该条件改变隔离的是自由回忆固定谚语与在误导选项中作决策的差别。极大的结果反差说明低 Base 分数不能直接解释为缺乏意大利谚语知识，更可能涉及候选项比较、任务理解或干扰抑制失败。但 Completion 与 Base 使用不同输出空间及判分规则，因此不能把两者差值视为纯粹的“推理能力损失”。 | Table 2<br><span class="experiment-evidence">LLama 4 Maverick 6.0 75.0 88.0</span> |

**定性案例**

- 作者选择 DeepSeek R1 和 Qwen 3 做完整思维链分析，因为这两个模型能够提供完整轨迹；其定性结论是模型常在推理中提到真实谚语结尾，却没有进一步识别该结尾不在候选项中，最后转而选择字面同义项。这一现象为 Table 3 的同义干扰偏差提供过程层面的例证，但所给节选没有提供具体题目、逐字思维链或各类现象的出现次数，因而无法判断其普遍程度；此外，外显思维链也不一定忠实对应模型实际生成答案的内部计算。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出并使用意大利谚语基准评测语言模型在文化语境和选项推理中的能力与局限。; rule check: matched taxonomy keywords; top rule score=10.0
- 全文指纹：`a3997c80a9e620f782bb7051cd6c1f601d316431f9e9b4b5552ecd8d48422aa4`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
