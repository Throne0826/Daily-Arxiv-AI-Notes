---
title: "[论文解读] Mind the Cap: Output-Budget Regimes Change the Measured Multilingual Reasoning Gap"
description: "[arXiv 2608.04160][LLM 评测] 本文指出，多语言推理评测中的“母语作答弱于先译成英语作答”不一定代表模型的推理能力差距，因为固定输出 token 上限会对表达长度不同的语言和答案出现时机不同的提示策略施加不等约束。"
arxiv_id: "2608.04160"
announcement_date: "2026-08-06"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:52:45.432929+00:00"
source_sha256: "77a67c355b14ca73ab4a20ae742389e54708b0d39fed9bb4677813af595b60e7"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "多语言推理评测"
  - "输出词元预算"
  - "长度归一化"
  - "截断效应"
  - "答案发出时机"
  - "MGSM"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.04160</p>

# Mind the Cap: Output-Budget Regimes Change the Measured Multilingual Reasoning Gap

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Ankit Goyal, Jaideep Ray</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04160v1) · [PDF 下载](https://arxiv.org/pdf/2608.04160v1) · **关键词** 多语言推理评测, 输出词元预算, 长度归一化, 截断效应, 答案发出时机, MGSM<br>


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

本文指出，多语言推理评测中的“母语作答弱于先译成英语作答”不一定代表模型的推理能力差距，因为固定输出 token 上限会对表达长度不同的语言和答案出现时机不同的提示策略施加不等约束。

**不用术语来说**：同一道题用不同语言书写和推理时，表达相同内容所需的 token 数可能不同；如果评测统一规定模型最多生成相同数量的 token，较费 token 的语言就更容易在答案尚未输出前被截断。此时，母语策略准确率较低可能只是“来不及写出答案”，而非模型“不会推理”。因此，只在一个输出上限下比较准确率，可能把评测配置造成的截断误判为多语言推理差距。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将输出预算视为独立实验变量，把“预算伪影”具体定义为：母语策略与翻译策略的准确率差距，在 token 数相同的上限与按语言长度溢价归一化的上限之间发生的变化；由此把笼统的能力比较转化为可检验的评测设计问题。
- 作者进一步区分强制上限与告知模型的预算，并以独立硬截断解码和预先冻结的检验设计验证预算依赖性；同时明确推断对象只是受控前缀预算下的策略表现，而不是模型内在推理能力的因果差异。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于多语言大语言模型推理评测研究。常见评测在固定输出词元上限下，比较模型直接使用题目原语言作答（NATIVE）与先借助英语转换或推理的策略；两者准确率之差常被称为“多语言推理差距”。但不同语言表达相同内容所需的词元数不同，策略给出最终答案的时机也不同，因此统一的硬性输出上限可能更早截断词元开销较大的语言，使测得差距同时混入语言词元效率、答案发出时机和策略本身性能。本文据此把输出预算视为独立实验变量，研究预算制度如何改变 MGSM 上的原语言与翻译策略对比；其推断对象是受控前缀预算下的策略性能，而不是模型内在或因果意义上的跨语言推理能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**输出词元预算（output-token budget）**

生成模型一次回答最多可以输出的词元数；硬上限为 $B$ 时，达到该长度的解码会被强制停止。若正确答案本应在上限之后出现，评测会把一次潜在正确推理变成截断或错误输出。

</div>
<div class="concept-item" markdown="1">

**长度归一化（length normalization）**

根据平行文本估计某种语言相对基准语言的长度倍率 $r$，再为原语言策略分配约为 $rB$ 的预算，以近似补偿表达同等内容所需的额外词元。本文用 FLORES-200 的语言长度溢价构造这一校正，并比较校正前后的策略差距。

</div>
<div class="concept-item" markdown="1">

**答案发出时机（answer-emission timing）**

它指模型在推理轨迹的第几个词元首次给出可解析的最终答案。即使两种策略最终都能解题，只要正确答案出现得早晚不同，固定上限也可能使它们获得不同准确率。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是 MGSM 的德语、泰语和斯瓦希里语数学文字题，模型为 Qwen3-8B 与 Llama-3.1-8B-Instruct，并在四种提示策略下生成推理及最终答案。核心比较是原语言策略与翻译相关策略在给定输出预算 $B$ 下的准确率差距；研究者既改变实际强制执行的硬上限，也比较词元匹配预算与按 FLORES-200 长度溢价调整后的预算，并进一步区分“向模型宣告的预算”和解码器真正执行的上限。若原语言获得按倍率扩展的预算后差距缩小，则统一词元上限对原测量有贡献；若在不再发生截断的饱和区间仍有差距，该残差只能解释为当前提示、翻译、输出格式等共同构成的策略性能差异，不能据此识别模型的内在推理能力差异。该设置明确承认提示语言、题目重述、翻译质量、推理轨迹语言和答案格式服从性彼此混杂。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$B$**

基准输出词元预算或实际执行的硬性生成上限。

</div>
<div class="notation-item" markdown="1">

**$r$**

由 FLORES-200 平行文本估计的目标语言相对长度倍率，用于给原语言输出分配扩展预算。

</div>
<div class="notation-item" markdown="1">

**$G(t)$**

一条生成轨迹既能正确作答、又已在第 $t$ 个词元之前发出答案的概率。

</div>
<div class="notation-item" markdown="1">

**$\Delta_L(B)$**

在预算 $B$ 处由长度归一化所对应的准确率变化；原文给出的时机恒等式将其表示为 $G(\lfloor rB\rfloor)-G(B)$。

</div>

</div>

**直接相关的工作**

- **MGSM（Shi et al., 2023）**: 为本文提供多语言小学数学推理评测任务。本文不主要提出新的解题方法，而是重新检验该类原语言与英语转换策略比较是否受到输出预算和截断机制影响。
- **FLORES-200 / NLLB（Goyal et al., 2022；NLLB Team et al., 2022）**: 提供跨语言平行文本及语言长度比较基础。本文据此估计语言长度溢价 $r$，构造原语言策略的长度归一化预算，以检验统一词元上限是否制造或放大测得的多语言差距。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

多语言大模型评测常依据单一输出 token 上限下的准确率来判断母语推理是否弱于“先翻译成英语再推理”。这一结论会影响模型选择、语言公平性判断以及词表扩展等适配投入；但如果统一上限对不同语言并不等价，评测就可能系统性低估 token 表达成本较高的语言，并把资源约束造成的失败归因于推理能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **单一固定输出上限评测**：对所有语言和提示策略使用相同的最大生成 token 数，再比较母语策略与翻译策略的准确率。这种做法便于控制计算量，但默认“相同 token 数”代表相同的表达机会。
- **母语与翻译策略的准确率对比**：在原语言直接提示模型推理，或先把题目翻译为英语再推理，然后将两者准确率之差解释为多语言推理表现差距。该比较同时改变了提示语言、问题改写方式、推理轨迹语言和答案格式等因素。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 语言表达相同内容所需的 token 数不同，且不同策略输出最终答案的时机不同；当固定上限具有约束力时，较长或较晚输出答案的轨迹更容易被截断。因此，单点准确率差距混合了推理表现与预算截断效应，甚至可能随预算变化而改变方向。
- 母语与翻译策略并非只改变推理语言，还混杂提示语言、重述方式、翻译质量、答案格式合规性和推理轨迹语言。因而现有对比不能直接识别“内在推理能力”的因果差异，只能描述特定策略与评测配置共同作用下的表现。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有评测尚未系统识别母语与翻译策略的差距在何种输出预算区间由截断产生、在语言长度归一化后是否缩小或反转，以及模型表现究竟只取决于实际强制上限，还是也会受到提示中所宣布预算的影响。更关键的是，缺少将预算扫描中观察到的现象预先冻结，并通过各预算独立硬截断生成加以确认的设计。

</div>
<div markdown="1"><span>核心问题</span>

在 MGSM 的德语、泰语和斯瓦希里语任务上，对 Qwen3-8B 与 Llama-3.1-8B-Instruct 而言，母语策略相对翻译策略的准确率差距是否是输出 token 预算造成的伪影；具体说，按 FLORES-200 估计的语言长度溢价为母语策略调整预算后，该差距是否会闭合，以及这种结论是否随预算约束区间而变化？

</div>
<div markdown="1"><span>作者直觉</span>

若两种策略最终都能解出题目，但母语轨迹需要更多 token 或更晚才输出可解析答案，那么紧预算会优先截断母语轨迹；适当放宽或按语言长度比例调整母语预算，就能恢复那些“已经推对但尚未写出答案”的样本。反之，当准确率已经随预算饱和，继续增加上限仍存在的差异便不能再由这一截断机制解释，而应谨慎表述为策略表现差距。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出新的推理模型，而是把输出令牌上限视为一个需要主动操纵的实验变量，重新测量多语言推理中的“母语作答差距”。输入为德语、泰语和斯瓦希里语的 MGSM 数学题；对每道题分别采用 NATIVE、TRANSLATE-ACT、PIVOT 和 CODE-SWITCHED 四种提示策略，由 Qwen3-8B 与 Llama-3.1-8B-Instruct 生成回答。核心比较集中于 NATIVE 与 TRANSLATE-ACT：前者用目标语言推理并作答，后者先把题目翻译为英语再求解。作者在多个预算 $B$ 下对回答前缀进行严格精确匹配，计算两种策略的准确率差，并将 NATIVE 的预算扩大到按目标语言令牌溢价 $r_{m,L}$ 缩放后的 $\lfloor r_{m,L}B\rfloor$，从而估计同等语义内容因分词长度不同而受到的截断影响。

研究流程包含发现性前缀扫描和独立硬截断确认两个阶段。前缀扫描从每条最长 4096 令牌的已存生成中截取不同长度，避免预算间生成随机性干扰；独立确认则在每个上限下重新解码，确保不同预算不共享生成轨迹，并用预先冻结的预算与假设进行检验。直观地说，作者先观察“如果在回答写到不同位置时强行停笔，成绩怎样变化”，再让模型在每个限额下真正重新作答，以确认观察到的差距不是复用同一篇长回答造成的。之后，论文通过语言识别、解析器稳健性、解码器一致性和正确答案发射位置等审计验证截断机制，并以交叉拟合的目标语言词表扩展为反事实干预，直接测量更省令牌的分词能否在固定预算下恢复准确率。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造语言、模型与提示策略实验单元

对每个题目、模型和策略抽取 $k=8$ 个样本，形成题目、语言、模型、策略和采样重复的完整实验单元。主要估计对象只比较 NATIVE 与 TRANSLATE-ACT，PIVOT 和 CODE-SWITCHED 用于策略排序及辅助检查。

<div class="method-step__io" markdown="1">

**输入**：MGSM 的德语、泰语和斯瓦希里语题目，每种语言 250 题；Qwen3-8B 与 Llama-3.1-8B-Instruct；NATIVE、TRANSLATE-ACT、PIVOT、CODE-SWITCHED 四种提示策略。<br>
**输出**：覆盖三种语言、两个模型和四种策略的生成任务，以及每个单元八次独立采样所对应的回答轨迹。

</div>

**直观理解**：同一道题让模型按四种语言组织方式各答八次，以免一次采样的偶然性决定结论。主要问题是：直接用母语推理看起来较差，究竟是能力不足，还是母语文本更快耗尽令牌额度。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立前缀账本并扫描预算区间

将完整生成及其所有可评分前缀组成账本；评估预算 $B$ 时只保留长度为 $B$ 的前缀，并按严格的前缀内答案规则评分。由于各预算来自同一条生成轨迹，预算曲线不含预算间重新采样噪声，但其结论限定在这种前缀定义的反事实中。

<div class="method-step__io" markdown="1">

**输入**：每个题目与采样单元的一条最长 4096 令牌生成，以及预算集合 $B\in\{64,128,192,256,384,512,768,1024\}$；扩展检查另加入 2048 和 4096。<br>
**输出**：每种语言、模型、策略和预算下的准确率曲线、截断率、策略差距，以及按语言令牌溢价缩放预算后的 NATIVE 准确率。

</div>

**直观理解**：这相当于先让模型写一篇较长答案，再分别在第 64、128、192 个令牌处剪断并阅卷。这样能清楚看到“多给一些书写空间”带来的变化，但不能代表模型提前知道限额后会采用的所有不同写法。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算长度归一化效应并冻结检验

以 $\operatorname{gap}(B)=\operatorname{acc}_{T}(B)-\operatorname{acc}_{N}(B)$ 表示同一预算下的策略差距，再比较该差距与将 NATIVE 上限调整为 $\lfloor r_{m,L}B\rfloor$ 后的差距，得到长度归一化效应 $\Delta_L(B)$。作者在新数据产生前以内部 Git 标签冻结 Qwen 的预算、方向性假设和六项检验，并用题目聚类的配对自助法及 Holm 校正控制多重比较。

<div class="method-step__io" markdown="1">

**输入**：NATIVE 与 TRANSLATE-ACT 的预算准确率、模型 $m$ 对语言 $L$ 的 FLORES-200 令牌溢价 $r_{m,L}$，以及发现性扫描得到的候选峰值预算。<br>
**输出**：预算约束区间、各语言的长度归一化效应曲线、预先指定的峰值预测，以及经多重比较控制的确认性统计结论。

</div>

**直观理解**：若目标语言平均需要英语的两倍令牌，就把母语回答的书写空间相应放大，再看原来的差距缩小多少。缩小的部分可以归因于预算与分词长度的共同作用；母语准确率饱和后仍存在的差距则不能继续解释为截断造成的推理缺陷。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 独立硬截断解码与测量审计

在每个上限下独立重新生成，共执行 540000 次硬截断解码；不同预算使用不同随机种子，任何轨迹都不得超过其上限。评分采用意向处理原则下的严格前缀精确匹配，同时进行语言识别、COMET 翻译质量、解析器稳健性、生产解码器一致性和答案发射时间审计。

<div class="method-step__io" markdown="1">

**输入**：冻结的预算和假设、两个模型的全部语言与策略单元，以及包括常规预算和 $\lfloor r_{m,L}B\rfloor$ 在内的硬上限。<br>
**输出**：不共享生成轨迹的确认数据、六项独立确认检验，以及对语言遵循、翻译质量、解析错误和特殊令牌规范化等潜在替代解释的诊断结果。

</div>

**直观理解**：第二阶段不再把同一篇长答案剪成多段，而是在每个限额下让模型从头回答，检验预算曲线是否能在真实硬限制中重现。附加审计用于确认分数变化确实主要来自正确答案写得太晚，而不是阅卷程序、语言跑偏或解码器格式差异。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 长度归一化预算效应恒等式

$$
\Delta_L(B)=\left[\operatorname{acc}_T(B)-\operatorname{acc}_N(B)\right]-\left[\operatorname{acc}_T(B)-\operatorname{acc}_N\!\left(\left\lfloor r_{m,L}B\right\rfloor\right)\right]=\operatorname{acc}_N\!\left(\left\lfloor r_{m,L}B\right\rfloor\right)-\operatorname{acc}_N(B)
$$

**符号说明**

- $\Delta_L(B)$：语言 $L$ 在基准预算 $B$ 下，由令牌溢价归一化所恢复的 NATIVE 准确率，也即归一化前后策略差距的变化。
- $B$：对生成输出施加的基准令牌上限。
- $\operatorname{acc}_N(B)$：NATIVE 策略在预算 $B$ 下的严格精确匹配准确率。
- $\operatorname{acc}_T(B)$：TRANSLATE-ACT 策略在预算 $B$ 下的严格精确匹配准确率。
- $r_{m,L}$：模型 $m$ 的分词器下，语言 $L$ 相对英语的 FLORES-200 总令牌数溢价。
- $\left\lfloor r_{m,L}B\right\rfloor$：按语言令牌溢价放大并向下取整后的 NATIVE 预算。
- $m$：被评估的模型。
- $L$：目标语言，即德语、泰语或斯瓦希里语。

<div class="equation-explanation" markdown="1">

**直观理解**：两个括号中的 TRANSLATE-ACT 准确率完全相消，因此 $\Delta_L(B)$ 并不是两种策略之间复杂的交互项，而只是 NATIVE 从预算 $B$ 增加到 $\lfloor r_{m,L}B\rfloor$ 后新增的正确率。若正确答案仍会在这段令牌区间内出现，预算处于约束区间且 $\Delta_L(B)$ 为正；一旦 NATIVE 准确率已经饱和，两端准确率相同，$\Delta_L(B)$ 必然趋近于 0。该恒等式因此既定义了论文的主要估计量，也限定了解释边界：饱和后残留的 NATIVE–TRANSLATE-ACT 差距不能由长度归一化识别为推理能力缺陷。<br>
**原文位置**：第 3 节“Design and estimands”，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 正确答案发射子累积分布预测式

$$
G(t)=P(C=1,E\le t),\qquad \Delta_L(B)=G\!\left(\left\lfloor rB\right\rfloor\right)-G(B)
$$

**符号说明**

- $G(t)$：截至令牌位置 $t$ 已经发射正确答案的联合概率，即正确答案发射位置的子累积分布。
- $C$：完整轨迹的正确性指标；$C=1$ 表示最终答案正确。
- $E$：可评分答案行在生成轨迹中的发射令牌位置。
- $t$：用于累计答案发射事件的令牌位置阈值。
- $r$：当前模型与语言对应的令牌溢价；此处为简写，作用与 $r_{m,L}$ 相同。
- $\Delta_L(B)$：预算从 $B$ 扩展到 $\lfloor rB\rfloor$ 时，预计新增的正确 NATIVE 回答比例。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把预算效应定位到答案何时真正写出：$G(B)$ 统计在原上限前已经写出正确答案的比例，而 $G(\lfloor rB\rfloor)$ 统计在归一化上限前写出的比例，两者之差正是中间窗口内迟到但正确的答案。它提供一个可检验的机制预测：$\Delta_L(B)$ 的峰值应出现在正确答案发射密度较高、且语言溢价窗口覆盖较多迟到答案的预算附近；但同一账本内的前缀准确率差与该表达式在吸收式正确性假设下代数等价，因此论文只把独立解码或拆分题目后的匹配视为一致性检查，而非独立因果证明。<br>
**原文位置**：附录 J“Correct-emission sub-CDF consistency check”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。主体方法不训练或微调 Qwen3-8B、Llama-3.1-8B-Instruct，也没有新的损失函数；研究对象是既有模型在不同输出预算、提示策略和分词成本下的测量结果。唯一带有数据拟合的组件是词表扩展：它从 NATIVE 轨迹学习字节级合并规则，目标是减少目标语言文本的令牌数，而非通过梯度优化模型准确率；扩展规模规则不读取准确率。由于新词元没有训练嵌入，词表实验固定已生成文本并重分词，只构成令牌成本反事实，不能等同于部署一个训练完成的新模型。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 预算账本与严格评分器**

账本保存每条 4096 令牌生成及其所有前缀分数。评分器只接受当前前缀内形如 `#### <integer>` 的答案行；截断、非整数、多答案或格式不合规均记为 0，每个题目下的八个样本分别计分后再对全部题目–样本单元取平均，不使用 best-of-$k$、pass@$k$ 或多数投票。

> 直观理解：该模块保证预算为 128 时绝不会偷看第 129 个令牌之后的正确答案，也不会用八次尝试中的最好一次美化成绩。严格格式会把推理能力、按时完成和遵循答案格式共同纳入实际可用准确率，因此论文明确提醒不能把该分数等同于纯粹推理能力。

**2. 令牌溢价归一化与确认性推断**

语言溢价 $r_{m,L}$ 是模型 $m$ 自身分词器在 FLORES-200 的 1012 对平行 devtest 句子上，目标语言总令牌数相对英语总令牌数的比值；文本先做 NFC 规范化，并通过句对配对百分位自助法评估。推断以 250 个平行 MGSM 题目为聚类单位重采样 10000 次，保留每道题的全部语言、策略和八个样本；六个 Qwen 原始 $p$ 值先乘预设的 1.3 尾部保守系数，再在族水平 $\alpha=0.05$ 下进行 Holm 校正。

> 直观理解：归一化不是假设每条答案都恰好按固定比例变长，而是用独立平行语料估算总体上某种语言要多花多少令牌。统计重采样按题目整体搬动，避免把同一道题的八次回答误当成八道互相独立的题；尾部系数和 Holm 校正则降低从多个语言、预算和假设中偶然挑中显著结果的风险。

**3. 交叉拟合词表扩展测量器**

扩展器不修改 Qwen 基础词表及原有合并列表，只从一半题目的 NATIVE 轨迹学习新的字节级合并并追加，使基础合并保持优先；另一半题目负责评估，随后交换两折。评估时固定模型已发出的文本，仅分别用基础与扩展分词器重分词、截取前 $B$ 个令牌并解码评分，扩展规模由不查看准确率的预设规则确定且同时作用于两个主要策略。

> 直观理解：交叉拟合避免针对待测题目专门制造能压缩其答案的词元，同时把“文本更省令牌”与“模型因新词元而改变推理过程”分开。它给出的是令牌成本反事实，不包含新词元嵌入训练，因此只能评估截断通道，不能被解释为完整的模型适配方案。

**训练与推理**

推理阶段先按模型、语言、题目和提示策略生成回答。发现性阶段为每个题目–样本单元保存一条最多 4096 令牌的轨迹，并在多个 $B$ 上评分其前缀；Qwen 是确认性分析对象，Llama 被作者明确定位为次要分析而非复现。每个样本独立计分，准确率对全部题目–样本单元平均；置信区间与检验则以题目为聚类单位，重采样时保留同题的八个样本及跨语言、跨策略配对结构。

确认阶段使用冻结协议在各预算下重新执行硬截断解码，不同预算更换随机种子且不复用轨迹。主要统计族包括是否存在任一语言满足 $\Delta_L>0$、是否存在超过 5 个百分点的最小关注效应、泰语效应是否大于德语，以及三个语言各自是否在按名义服务成本匹配的预算网格上发生策略排序反转。词表扩展阶段不重新调用模型生成，而是对既有文本做两折交叉拟合重分词，并在相同 $B$ 下比较基础词表与扩展词表的评分；因此该阶段隔离的是令牌计数和截断效应，而不是模型行为适应。

**复现信息**

复现和解释结论所需的关键设置如下：MGSM 每种语言含 250 题，每题每策略采样 $k=8$ 次；主要前缀预算为 $64$ 到 $1024$ 的八点网格，2048 与 4096 只用于扩展交叉和最佳策略检查。独立硬截断阶段覆盖 $B\in\{64,128,192,256,384,512,768,1024,2048\}$ 及 NATIVE 的 $\lfloor r_{m,L}B\rfloor$ 上限，共 540000 次解码、270 个按上限分片的任务；预算间不共享随机种子或轨迹。

答案解析必须严格限制在当前前缀，并只认可 `#### <integer>`；截断、非整数和不合规回答均按 0 分处理。FLORES-200 溢价应使用每个模型自己的分词器，在 1012 对 NFC 规范化平行句上按目标语言与英语的总令牌数比计算，不能跨模型复用。统计推断使用 10000 次题目聚类配对自助重采样、studentized sup-$t$ 最大统计量、预设 1.3 尾部保守系数和六项 Holm 校正；作者同时指出模拟所得校正一类错误率为 0.00917，而目标为 0.00833，差异仅在蒙特卡洛误差范围内，因此该系数是保守防护而非已验证的精确族错误率校准。词表扩展必须保持基础词表和合并优先级不变，以两个互斥题目半集交叉拟合，并对两个主要策略同时应用；英语控制只保证 FLORES-200 英语总令牌变化低于 0.02%，不保证每个英语字符串的切分完全相同。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 核心评测使用 MGSM 数学文字题的德语、泰语和斯瓦希里语版本，比较同一任务上的 NATIVE 与 TRANSLATE-ACT 策略。预算扫描先用于发现峰值；随后冻结 Qwen 的三个峰值预算以及 $B^*=1024$，在独立硬截断解码样本上确认，摘要报告该确认阶段共生成 540,000 条解码记录。
- 预算声明实验仍使用 MGSM，但固定实际强制上限为不易触发截断的 2048，仅把提示中声明的预算改为 $\{128,256,2048\}$。该实验包含 192,000 条固定上限记录，作用是把“模型知道预算后的行为变化”与“到达上限后被截断”分离。
- 论文还在三个额外基准上进行了探索性、仅限 Qwen 的逐题二分验证，用一半题目估计正确答案发射时间关系，再在留出题目上预测长度归一化峰值。所给章节未报告这些基准的名称、题量或具体划分比例之外的信息，因此不能把它们视为与 MGSM 同等强度的确认性证据。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**准确率**

在给定策略与预算下得到可解析且正确最终答案的题目比例。它同时受推理能力、答案是否及时发射以及输出是否被截断影响，因此单一预算下的准确率不能直接解释为纯粹的推理能力。 （越高越好，因为表示更多题目在预算内产生了可解析的正确答案。）

</div>
<div class="metric-item" markdown="1">

**长度归一化效应 $\Delta_L(B)$**

同一 NATIVE 策略从预算 $B$ 增加到语言缩放预算 $\lfloor rB\rfloor$ 后的准确率增量。较大的正值说明原预算对该语言形成了明显截断约束，而不是直接说明模型获得了新的推理能力。 （该指标没有一般意义上的越高越好；接近零表示额外语言预算不再改变准确率，较大正值表示测量对预算选择敏感。）

</div>
<div class="metric-item" markdown="1">

**正确答案发射子分布与预测误差**

$G(t)=P(C=1,E\leq t)$ 表示完整轨迹最终正确且在位置 $t$ 前已发射可解析答案的概率，其中 $C$ 是完整轨迹正确性，$E$ 是答案发射位置。由 $G(\lfloor rB\rfloor)-G(B)$ 预测预算扩展可救回的正确答案比例，并用平均绝对误差检验预测与独立解码结果的一致性。 （预测平均绝对误差越低越好，因为说明一次长上限运行中的答案发射时序更准确地解释了不同预算下的准确率变化。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen 在独立硬截断确认样本上的三个预冻结峰值预算

<div class="result-value" markdown="1">

独立估计的长度归一化效应分别为：德语在 $B=192$ 时 34.65 点、泰语在 $B=256$ 时 38.60 点、斯瓦希里语在 $B=128$ 时 13.70 点；三项检验均为 $p=0.0001$，且六项 Holm 校正确认检验全部拒绝相应原假设。

</div>

作者的确认性结论是：紧预算下的大幅提升并非仅由同一长轨迹的事后截断回放或峰值重选造成，独立解码仍重现了三个预先冻结的 Qwen 峰值。分析上，这表明输出上限确实能制造很大的测量差异；但 $\Delta_L(B)$ 比较的是同一策略在不同输出宽度下的表现，尤其泰语从 256 扩到 652 token，因此不能解释为严格相同计算资源下的两种策略优劣，也不能单独证明所有母语差距都源于分词长度。

<div class="result-source" markdown="1">

来源：第 4.2 节，Table 1 后的独立确认结果

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The independent peak estimates are 34.65 points for German at B=192, 38.60 for Thai at 256, and 13.70 for Swahili at 128.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 冻结预算 $B^*=1024$ 下的 Qwen 与程序匹配的 Llama 分析

<div class="result-value" markdown="1">

Qwen 的 $\Delta_L(1024)$ 在德语、泰语、斯瓦希里语上分别为 0.00、0.15、0.05 点，六项原确认检验均未拒绝；Llama 三种语言均为 0.00 点，也未拒绝，但其结果不属于确认性检验族。

</div>

作者将 Qwen 的近零效应解释为 NATIVE 准确率在 1024 token 左右已经饱和，因此继续增加语言预算几乎不再救回正确答案；此时剩余的 NATIVE 与 TRANSLATE-ACT 差异是策略性能差异，不能据此识别“母语推理缺陷”。Llama 的近零值原因不同：德语和泰语常常根本没有发射可解析答案，表现接近地板。因而相同的零归一化效应可能来自准确率饱和，也可能来自严重的答案不发射，不能统一解释为语言公平。

<div class="result-source" markdown="1">

来源：第 4.1 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen ΔL(B∗): de 0.00, th 0.15, sw 0.05 points.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 紧预算下 Qwen 的 NATIVE 与 TRANSLATE-ACT 策略排序

<div class="result-value" markdown="1">

在 $B=128$ 时，Qwen 德语 NATIVE 准确率为 2.55%，TRANSLATE-ACT 为 1.15%；斯瓦希里语在 128 和 192 token 时也由 NATIVE 领先，而泰语没有出现 NATIVE 领先，Llama 的三种语言均未发生交叉。

</div>

结果说明预算不仅改变两种策略间差距的大小，还可能改变“哪种策略更好”的结论。交叉与答案发射时序的左尾相符：少量较早发射答案的 NATIVE 轨迹在极紧上限下占优。不过作者明确指出，这些汇总不能分离翻译片段长度，也未建立发射时序的中介因果关系；斯瓦希里语交叉还发生在重尾、低分单元中，因此不应概括成 NATIVE 普遍优于翻译策略。

<div class="result-source" markdown="1">

来源：第 4.3 节，Table 2 后

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

At B=128, Qwen German NATIVE scores 2.55% versus 1.15% for TRANSLATE-ACT; Swahili NATIVE leads with bootstrap probability 1.00 at 128 and 192 (transition [192,256]), while German leads with probability 0.958 at 128 (transition [128,192]).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 确认性证据的主要对象是 Qwen3-8B、MGSM 的三种语言和预冻结预算；Llama 明确不在确认检验族内，三个额外基准也只是 Qwen-only 的探索性二分分析。由此不能直接外推到其他模型规模、语言、任务类型或解码设置。
- FLORES 长度比给予的预算溢价在六个模型-语言单元中都大于行为轨迹长度比，而行为比又因内容、正确性和停止行为不同而不是有效性已确认的归一化器。特别是泰语峰值实际比较 256 与 652 token，故结果能识别预算敏感性，却不能唯一确定一个语言应获得多少额外 token 才算资源公平。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- NATIVE：模型直接以目标语言推理并输出答案，是受目标语言分词效率和答案发射时间影响的主要实验组。
- TRANSLATE-ACT：模型采用翻译后作答的策略；与 NATIVE 在相同强制预算 $B$ 下比较，用于构成未归一化差距 $\operatorname{gap}(B)=\operatorname{acc}_T(B)-\operatorname{acc}_N(B)$。
- FLORES 长度溢价归一化：根据语言长度比 $r$，比较 NATIVE 在 $\lfloor rB\rfloor$ 与 $B$ 下的准确率，得到 $\Delta_L(B)=\operatorname{acc}_N(\lfloor rB\rfloor)-\operatorname{acc}_N(B)$。它测试同一 NATIVE 策略仅因获得更符合语言表达长度的预算而能恢复多少准确率。
- 行为轨迹长度比：以模型实际生成轨迹估计的长度比替代 FLORES 比率，作为归一化敏感性对照。它可检验结论是否完全依赖某个外部语料长度系数，但由于轨迹的内容、正确性和停止行为不同，作者明确不把它视为经过验证的归一化器。

**实验想回答的问题**

- 在不同输出预算 $B$ 下，MGSM 的母语作答与翻译作答准确率差距是否主要由截断造成；按语言长度比将母语预算扩展为 $\lfloor rB\rfloor$ 后，这一差距会放大、消失或反转到什么程度？
- 除实际强制执行的输出上限外，向模型声明预算是否会独立改变生成行为与准确率；观察到的预算效应能否在独立硬截断解码、替代长度归一化方法和答案边界干预下得到区分？

**实验实现**

实验评估 Qwen3-8B 与 Llama-3.1-8B-Instruct，并围绕 NATIVE、TRANSLATE-ACT 等四种提示策略开展预算扫描；所给章节仅完整呈现前两种策略，其他策略名称与结果未明确报告。主扫描通过 `max_tokens` 强制停止解码，但不把预算写入提示；保存的长轨迹被按不同 token 上限回放以计算逐预算前缀准确率。峰值区间采用逐题聚类 bootstrap 的点置信区间，并以同时 max-$|t|$ 置信带检查扫描中的多预算不确定性。确认阶段预先冻结 Qwen 的德语 $B=192$、泰语 $B=256$、斯瓦希里语 $B=128$ 峰值以及 $B^*=1024$，在独立硬截断解码上执行六项 Holm 校正检验：三个检验 $\Delta_L(B)>5$ 点的最小实际重要效应，三个检验 $|\Delta_L(1024)|<5$ 点的等效性。Llama 只作程序匹配的次要分析，不属于确认性检验族。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 固定实际强制上限为 2048，仅向 Qwen3-8B 声明 128、256 或 2048 token | 泰语 NATIVE 在声明 128 token 时准确率为 63.20%，声明 2048 token 时为 58.10%，差值为 $+5.10$ 点，标准误为 1.67，$p=0.0029$；三个声明值下的准确率依次为 63.20%、59.90%、58.10%。四个 Holm 校正对比中只有该单元拒绝原假设。 | 这一控制只改变模型看到的预算信息，不改变真正允许生成的 2048-token 上限，因此隔离出“预算声明改变规划或表达行为”的效应。结果反驳了准确率仅由强制上限决定的简单模型，但证据只来自一个模型、一个基准中的一个语言与策略单元；它不能支持“声明紧预算通常提高准确率”这一方向性结论。 | 第 4.4 节<br><span class="experiment-evidence">Thai NATIVE scores 63.20% when 128 is announced against 58.10% when 2048 is, a difference of +5.10 points (SE 1.67, p=0.0029), and the announced grid is monotone: 63.20, 59.90, 58.10 at 128, 256 and 2048.</span> |
| Qwen 德语 NATIVE 在 $B=128$ 到达上限时强制注入答案分隔符 | 强制答案分隔符使准确率从 2.55% 提高到 25.70%；分开统计时，被上限截断的轨迹准确率为 23.72%，已自然运行结束但未输出答案行的轨迹为 100%。 | 该干预测试低分是否部分来自“模型尚未切换到最终答案格式”，而非内部推理必然错误。大幅提升表明答案边界与发射时机是重要通道，但 25.70% 是两个性质不同群体的合并结果，且强制分隔符改变了生成过程，不能当作常规提示策略的无偏性能估计。 | 第 4.4 节<br><span class="experiment-evidence">Forcing—injecting the answer delimiter when the cap arrives—instead lifts Qwen NATIVE German at B=128 from 2.55% to 25.70%, a pooled figure over two populations we keep separate because their average means little: 23.72% among traces the cap truncated and 100% among traces that ran to completion without emitting an answer line.</span> |

**定性案例**

- 斯瓦希里语展示了策略交叉为何需要谨慎解释：其 NATIVE 答案发射位置的第 10 百分位为 96，而 TRANSLATE-ACT 为 170.7，较早的左尾与 NATIVE 在 64、128、192 token 下领先一致；但 NATIVE 输出长度第 90 百分位达到 4096，且 25.1% 的轨迹从未发射可解析答案。因此，这一交叉更像紧预算对少量早发射轨迹的选择效应，而不是 NATIVE 整体推理质量更高。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Studies how output-token budgets distort multilingual mathematical reasoning evaluation and proposes budget-regime reporting.; rule check: matched taxonomy keywords; top rule score=2.0
- 全文指纹：`77a67c355b14ca73ab4a20ae742389e54708b0d39fed9bb4677813af595b60e7`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
