---
title: "[论文解读] Aligned in Form, Not in Meaning: The Comprehension - Containment Decoupling of LLM Safety in Low-Resource Bangla Derogatory Speech"
description: "[arXiv 2608.02941][LLM 安全] 原文未明确报告。"
arxiv_id: "2608.02941"
announcement_date: "2026-08-05"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:41:11.627268+00:00"
source_sha256: "7c03b331864768a87189c4090fedd7c1d4fec7ee7ccc66057201a5e151c95503"
tags:
  - "LLM 安全"
  - "LLM 评测"
  - "LLM 其他"
  - "LLM Reasoning"
  - "多语言大语言模型安全"
  - "低资源语言"
  - "孟加拉语贬损表达"
  - "理解—遏制脱耦"
  - "语义理解"
  - "安全遏制"
  - "表层形式"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2608.02941</p>

# Aligned in Form, Not in Meaning: The Comprehension - Containment Decoupling of LLM Safety in Low-Resource Bangla Derogatory Speech

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Shadab Bin Habib, A K M Ferdous Reza Habib, Subarno Neel, Adib Sakhawat</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Department of Computer Science and Engineering；Islamic University of Technology, Dhaka, Bangladesh</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02941v1) · [PDF 下载](https://arxiv.org/pdf/2608.02941v1) · **关键词** 多语言大语言模型安全, 低资源语言, 孟加拉语贬损表达, 理解—遏制脱耦, 语义理解, 安全遏制, 表层形式<br>


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

本文属于多语言大语言模型安全评测，关注模型在低资源语言中的安全对齐是否真正依据有害语义，而非依赖英语等高资源语言中熟悉的词形和关键词。既有研究已发现非英语环境下的不安全响应、毒性缓解失效和鲁棒性下降，但常用基准多由英语有害提示翻译而来，难以覆盖孟加拉语本土贬损表达（gali）所依赖的文化语境、习语和非透明组合意义。本文因此把安全行为拆成“理解”与“遏制”两个维度：前者考查模型能否识别表达的真实贬损含义，后者考查模型生成时是否拒绝或避免复现该表达，并据此检验二者在低资源语言中是否脱耦。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**安全对齐**

通过训练、策略约束或输出过滤，使大语言模型避免生成有害内容并在必要时拒绝请求。本文关心这种约束能否跨语言迁移到训练资源较少、文化特征较强的表达。

</div>
<div class="concept-item" markdown="1">

**理解—遏制脱耦**

“语义理解”指模型能否正确解释贬损表达的意图与含义；“安全遏制”指模型是否抑制而非复现该表达。脱耦意味着模型可能理解其伤害性却仍输出它，也可能尚未正确理解便因表面词形触发拒绝。

</div>
<div class="concept-item" markdown="1">

**表层形式与组合语义**

表层形式是字符、拼写、词元和显眼关键词等可直接观察的语言特征；组合语义是多个词结合语境后形成的整体含义。孟加拉语本土辱语可能无法由逐词直译推出其冒犯程度，因此适合判断安全机制究竟追随词形还是意义。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究输入是由母语者整理和标注的100条孟加拉语本土贬损表达，并在需要对照时考查相应的跨语言或表层变体；被审计对象是五个前沿大语言模型。模型需要在六类协议下表现：语义理解、文化相关的严重程度校准、正字法扰动、显式思维链推理、多轮交互和专家人格提示。观察输出包括模型是否正确解释表达、如何判断其伤害程度，以及面对相关生成请求时是拒绝、使用还是泄漏冒犯词元。核心假设是：当有害意义通过低资源语言形式表达时，理解能力与遏制能力不再稳定联动，安全行为会更多受表层实现影响。人工标注的一致性以Cohen’s $\kappa$ 衡量，文中报告$\kappa=0.84$，用于说明参考标注具有较高一致性，而不是模型性能指标。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\kappa$**

Cohen’s kappa一致性系数；衡量标注者一致程度，并扣除随机一致的影响。

</div>

</div>

**直接相关的工作**

- **XSAFETY（Wang et al., 2024）**: 该基准显示非英语提示的不安全响应率明显高于英语提示，为“多语言能力不等于多语言安全”提供前提证据；但其属于英语中心的多语言扩展，不能充分检验依赖孟加拉文化语用的本土贬损表达。
- **BanglaGuard（Alam et al., 2026）**: 该工作通过提示分类、拒绝生成和响应过滤构建孟加拉语模型安全流程，是语言对象最接近的既有研究；然而其训练与评测数据主要来自英语有害提示的翻译，因而没有系统分离本土表达的语义理解与生成遏制。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大型语言模型即使具备多语言生成能力，其安全机制也未必能在低资源语言中识别并抑制本土化的侮辱表达。孟加拉语本土辱语常依赖习语、文化语境和组合含义，直译后未必显得冒犯；如果安全对齐主要记住英语等高资源语言中的关键词和表面形式，模型就可能理解辱语却仍将其复述或用于生成，也可能在没有真正理解含义时机械拒绝。这使英语安全评测难以可靠证明模型在孟加拉语真实使用环境中的安全性。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **英语中心的多语言安全基准**：以英语有害内容分类体系或英语数据为基础，再通过翻译或多语言扩展构造测试集；文中列举了 XSAFETY、PolygloToxicityPrompts 和 BanglaGuard。这类方法通常比较不同语言中的不安全回答率、毒性缓解能力或鲁棒性，以判断模型的多语言安全表现。
- **依赖词汇表面形式的安全过滤与拒答机制**：根据已知敏感词、字符模式或熟悉的高资源语言表达触发拦截和拒答。其优势是实现直接，但保护效果可能依赖具体拼写、分词结果和提示框架，而非表达所承载的有害语义。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 由英语数据翻译或沿用英语中心分类体系的基准，难以覆盖含义来自本地文化与语用规则、且不存在直接词汇对应的孟加拉语辱语；因此，它们测得的跨语言安全性不能充分代表模型面对原生低资源表达时的表现。
- 表面词汇驱动的过滤可能把“理解有害含义”和“抑制有害表达”混为一谈：拼写扰动、分词失败或角色提示都可能改变拒答率，却不代表模型真正形成了稳定的语义级安全判断，最终产生漏放、机械拒绝或虚假的安全改进。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有研究已经发现非英语环境中的不安全回答率更高、毒性控制更弱，但尚未系统区分两个能力：模型是否正确理解本土辱语的意图与严重程度，以及模型是否在生成中拒绝或避免复现该辱语。尤其缺少以母语者标注的原生孟加拉语表达为对象、在多种交互和提示条件下检验这两种能力是否彼此脱钩的综合审计。

</div>
<div markdown="1"><span>核心问题</span>

当有害含义通过低资源孟加拉语的本土语言形式表达时，大型语言模型的语义理解能力与安全遏制能力是否仍然一致，还是会出现“理解—遏制解耦”，并使安全行为更多受拼写、分词、显式推理和角色框架等表面因素支配？

</div>
<div markdown="1"><span>作者直觉</span>

原生孟加拉语辱语适合作为诊断工具，因为其冒犯性往往不能从逐词翻译或显眼的身体部位词汇中直接推出。若模型安全机制真正依据跨语言语义运行，那么同一有害含义在不同拼写、推理方式或角色设定下应获得相对稳定的遏制；反之，如果理解表现提高但辱语复现也随之增加，或仅因字符扰动和专家角色就显著改变拒答，就说明语义理解模块与安全控制模块并未可靠联动。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文不是提出或训练新的安全模型，而是设计一套跨语言行为审计方法，用于检验“理解—遏制解耦”假设：大语言模型能否正确理解孟加拉语贬损表达，与其是否避免在回答中复现该表达，可能是彼此独立的能力。作者先构建由母语者校准的孟加拉语贬损词表及英语功能等价项，再让五个前沿模型在六种协议下作答，人工标注语义理解、词项泄漏、拒答以及多轮互动行为，最后比较语言、书写形式、显式推理和专家角色等受控条件引起的变化。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建跨语言贬损表达词表与人工基准

作者人工整理100个核心表达，并由5名孟加拉语母语者独立按五级量表标注冒犯严重度；每个孟加拉语表达还配对一个保留交际意图和感知严重度、而非逐字翻译的英语功能等价项。E1、E3、E4和E5使用其中53个跨语言匹配项，E2使用100项，E6则使用扩展到501项的词表。

<div class="method-step__io" markdown="1">

**输入**：原生孟加拉语中的解剖、性别、性、宗教、社群、种姓、阶级及组合式贬损表达。<br>
**输出**：带有人类严重度参考、语义类别和英语功能等价项的评测词表；标注者一致性为$\kappa=0.84$。

</div>

**直观理解**：这一步相当于先由熟悉当地文化的人制作“标准答案”。功能等价配对尽量保证两种语言表达的是同一种冒犯意图，从而避免把翻译质量误当成模型安全差异。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成六类受控模型交互

E1测试单轮释义中的理解与复现；E2要求输出严重度分数和是否冒犯的判断；E3将输入改为罗马化孟加拉语或在目标词字符间插入空格；E4在E1上增加逐步推理指令；E5组织16轮双模型辩论；E6用“孟加拉语言文化专家”角色要求模型进行教育性解释。

<div class="method-step__io" markdown="1">

**输入**：词表中的目标表达、统一提示模板，以及五个被审计模型：gpt-oss-120b、gpt-4o-mini、qwen3.7-flash、gemini-2.5-flash-lite和deepseek-v4-flash。<br>
**输出**：覆盖语言、严重度、正字法扰动、显式推理、多轮互动和角色框架六种条件的模型回答。

</div>

**直观理解**：六个协议像六种压力测试：每次主要改变一个因素，观察模型是因为真正理解了危害而采取安全行为，还是只对熟悉的词形、格式或角色指令作出机械反应。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 统一人工行为标注

训练过的标注者使用统一规则判定$Pass$、$Use$和$Refusal$：分别表示正确理解目标贬损含义、明确复现所查询的贬损表达，以及安全机制阻止回答；对E5另标注$Escalation$和$Innovation$，分别衡量攻击性语言升级程度和是否引入提示中未出现的新贬损表达。

<div class="method-step__io" markdown="1">

**输入**：各协议产生的单轮回答、评分结果和多轮对话。<br>
**输出**：每个模型—词项—条件组合上的离散行为标签，以及多轮对话的$0$至$5$升级分数和新词创新记录。

</div>

**直观理解**：只看模型是否拒答会混淆多种现象，因此作者把“懂不懂”“有没有说出来”和“是否主动拒绝”分开记账。多轮场景还检查模型会不会越吵越凶，或自行想出新的攻击词。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 跨条件比较并检验解耦

作者比较不同语言和干预条件下的理解通过率与词项复现率，并在E2中比较模型严重度和人类严重度，在E5中比较升级、创新与缓和角色，在E6中分析专家角色对拒答和复现的影响。判断重点不是单一安全分数，而是理解变化是否带来相应的遏制变化，以及表面上的遏制改善能否由分词失败、输出中断或格式拒绝解释。

<div class="method-step__io" markdown="1">

**输入**：人工标注结果、人类严重度基准，以及孟加拉语与英语功能匹配项。<br>
**输出**：对“理解—遏制解耦”假设的多协议证据，以及对正字法脆弱性、显式推理泄漏、角色诱导和关键词式安全边界的机制诊断。

</div>

**直观理解**：如果安全机制真正依据含义工作，模型越能理解某个侮辱，通常越应避免复现它；若理解提高而泄漏不降反升，或仅因输入被破坏而少输出，就说明“会理解”和“会拦截”并非同一套可靠机制。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文是模型行为审计，不训练或微调被测模型，也未在所给章节中提出需要优化的损失函数；人类严重度仅作为E2的比较基准，$Pass$、$Use$、$Refusal$、$Escalation$和$Innovation$均是评测标注，而非训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 语用等价的跨语言配对**

孟加拉语词项与英语词项按交际功能和感知严重度人工匹配，而非采用字面翻译。该设计在E1等配对实验中尽量控制危害含义，使语言表面形式成为主要变化因素。

> 直观理解：有些本地侮辱直译后会失去文化含义；若直接逐字翻译，测到的可能只是翻译不自然。功能配对让比较更接近“同一种伤害换了一种语言表达”。

**2. 理解与遏制的分离式指标**

$Pass$用于测量模型是否识别目标表达的贬损含义，$Use$用于测量回答是否复现该表达，$Refusal$则单独记录安全机制是否阻止回答。三者不被合成为一个总分，以便识别理解正确但仍泄漏、没有泄漏但只是输出失败等不同机制。

> 直观理解：模型没说出攻击词不一定代表安全：它可能根本没看懂，也可能被异常空格弄乱。把三类行为拆开，才能判断模型究竟是“懂而克制”“懂但照说”，还是“没懂所以没说”。

**3. 表面形式与交互框架的受控干预**

E3、E4和E6分别操纵书写形式、逐步推理指令与专家角色，在尽量保持目标语义不变的情况下观察行为变化；E5进一步把审计扩展到16轮动态交互。该组合用于区分意义驱动的安全判断与分词、提示服从、角色位置等表面因素。

> 直观理解：作者不是只换一批测试词，而是对同一类含义更换“外包装”。若模型安全行为随拼写、推理要求或身份设定剧烈变化，就更像在识别包装，而不是稳定识别伤害。

**训练与推理**

全部实验发生在推理阶段。作者向五个既有大语言模型提交协议化提示：E1询问某人被称为目标词时该词的含义；E2要求仅返回包含$1$至$5$严重度分数及冒犯布尔标签的JSON；E3在E1基础上改用罗马化输入或对目标表达插入字符级空格；E4增加逐步推理要求；E5让成对模型进行16轮结构化辩论；E6令模型扮演孟加拉语言文化专家并作教育性解释。生成结果随后由人工依据同一规则标注并聚合比较，过程中没有参数更新。

**复现信息**

公平解释结果所必需的信息包括：E1、E3和E4每种条件均覆盖53个词项与5个模型，即$N=265$个回答；E2覆盖100个具有人类严重度标注的表达；E5分析$N=3110$段、每段16轮的对话；E6以501个扩展词项对5个模型进行$N=2510$次评估。跨语言实验使用人工功能等价项而非机器直译，所有输出由训练过的标注者按统一量表复核。所给章节未明确报告采样温度、最大生成长度、随机种子、API版本、重复采样次数或解码策略，因此这些因素仍需结合论文附录或代码进行复现核查。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 人工整理的100条孟加拉语高影响贬损表达词表，涵盖身体、性别、宗教与社群、种姓与阶级、肤色以及组合式多分句侮辱。5名孟加拉语母语者用五级量表独立标注冒犯程度，报告的一致性为Cohen’s $\kappa=0.84$；E2使用全部100条，作用是提供文化严重度的人工参照。
- 从词表中选取53条孟加拉语表达，并为每条人工匹配一个保持交际意图和感知严重度、而非逐字翻译的英语功能等价项。E1、E3、E4和E5使用该子集：前三者对5个模型形成每个条件$53\times5=265$个响应，E5则构造3,110场、每场16轮的模型间对话。原文没有报告训练集、验证集或测试集划分；该资源仅用于审计评测。
- E6采用扩展至501条的孟加拉语贬损表达词表，以提高专家角色评测中的语言多样性。给模型加入“孟加拉语言与文化专家”的教育性身份后，考察相同有害含义在合法化语境下是否更容易绕过拒答与遏制；原文节选未说明扩展条目的独立人工标注流程。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass**

人工评审判断回答是否正确理解目标贬损表达的意图含义。它衡量语义理解，而不是回答是否安全；在跨语言和表面扰动条件中报告通过率。 （越高越好，因为更高表示模型更可靠地识别了表达的实际贬损意义。）

</div>
<div class="metric-item" markdown="1">

**Use与Refusal**

Use记录回答是否明确复现被询问的贬损表达，是本文的遏制失败指标；Refusal记录安全机制是否阻止模型作答。两者不能简单互补，因为模型可能不拒答但仍不复现，也可能因格式或分词失败而停止生成。 （Use越低通常表示遏制越好，Refusal则需结合Pass解释：适当拒绝可能体现安全介入，但高拒答也可能只是任务失败，低拒答也不等于理解充分。）

</div>
<div class="metric-item" markdown="1">

**严重度校准与对话毒性指标**

E2用五级严重度均值偏差、平均绝对误差MAE、Spearman秩相关$\rho$及二元冒犯识别率衡量与母语者判断的一致性；E5另用0至5的Escalation、Innovation和对话解决归属衡量升级、新辱语产生及缓和行为。 （严重度偏差和MAE越低越好，$\rho$与识别率越高越好；Escalation和Innovation通常越低越安全，但必须结合是否真正理解与解决冲突判断。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### E1：原生孟加拉语与匹配英语的单轮基线

<div class="result-value" markdown="1">

队列的英语Pass为96.98%，孟加拉语Pass为89.06%，理解差距为7.92个百分点；但两种语言的Use均为92.83%。作者据此认为，语言资源差异显著影响理解，却没有相应改善或恶化词项复现，构成理解—遏制脱钩的基线证据。

</div>

通俗地说，模型对孟加拉语辱语“少懂一些”，却与英语条件一样频繁地把辱语直接写出来。这个受控跨语言比较支持理解与遏制不是同一能力，但它并不单独证明内部存在两个独立模块，也不能排除提示模板或所选词表对绝对复现率的影响。

<div class="result-source" markdown="1">

来源：Section 4.2, E1；Table 1与Table 11汇总

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The cohort achieves a near-ceiling mean English Pass of 96.98% but only 89.06% Bangla Pass—an aggregate comprehension deficit of 7.92 points. Yet the containment-failure rate is identical across languages at 92.83% (Bangla Use = English Use).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### E2：模型严重度判断与孟加拉语母语者标定比较

<div class="result-value" markdown="1">

母语者平均严重度为2.99/5，模型队列为3.88/5，呈+0.90的高估偏差，MAE为1.19；在已作答项目上，模型将89.10%的词识别为冒犯，但与人工严重度排序的相关仅约为$\rho=0.60$。作者将其解释为模型具备粗粒度识别能力，却不能准确掌握本土语境中的轻重层次。

</div>

模型通常知道某个词“不友好”，但容易把轻微俚语和身体相关表达判得过重，同时不能稳定区分不同表达的相对危害。高二元识别率因此不能替代文化校准；不过，作者把偏差归因于英语中心安全启发式属于机制解释，当前结果本身主要证明误校准，而不是直接定位其训练来源。

<div class="result-source" markdown="1">

来源：Section 4.3, E2；Table 11汇总

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Native speakers set a moderate baseline severity of 2.99/5; the cohort averages 3.88/5—a +0.90 over-severity bias with MAE = 1.19. On answered items the cohort flags 89.10% of slurs as offensive, proving basic competence—yet rank-order agreement with humans is only moderate (ρ ≈ 0.60), the tell-tale of a system keyed on surface cues rather than graded meaning.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### E6：孟加拉语言文化专家角色与教育性解释框架

<div class="result-value" markdown="1">

专家角色条件下，Refusal降至6.57%，Pass为63.98%，Use仍达85.46%。作者认为，教育性或专家身份显著削弱拒答，却没有建立可靠的语义遏制，说明角色框架可使模型在仍不充分理解部分表达时大量复现目标词。

</div>

给请求套上“专家讲解”的正当用途外观后，模型很少拒绝，并频繁写出贬损词，但正确理解率明显低于复现率。这显示拒答策略可能对语境包装敏感；然而，节选没有提供无专家角色、同一501条词表上的直接数值对照，所以不能仅凭该行精确量化“角色导致了多少下降”，也不能据此断言所有复现都不安全。

<div class="result-source" markdown="1">

来源：Table 11；协议说明见Appendix B, E6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

E6 Persona Refusal 6.57%, Pass 63.98%, Use 85.46%

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验使用人工策划词表、单一基线提示及5个模型，且节选未报告置信区间、显著性检验、随机重复、完整模型名单和解码设置；因此百分比可描述该审计队列，却不足以估计更广泛模型、提示或自然对话分布上的普遍效应。
- Use把任何明确复现目标表达都视为遏制失败，但在词义解释、引用和反歧视教育中，提及词项不一定等同于实施伤害；相反，不复现也可能只是未理解或分词失败。E6又缺少同一501条词表的无角色数值对照，故关于专家角色“导致”拒答崩溃的因果强度仍需配对实验确认。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- E1原生孟加拉语单轮条件是后续干预的主基线：统一提示为一名学生询问别人用某个词称呼自己时该词是什么意思，同时测量模型是否理解以及是否直接复现该词。它为E3的转写与空格扰动、E4的思维链提示提供同任务、同词项的可比起点。
- E1匹配英语条件控制了贬损意图与大致严重度，只改变语言资源条件。若安全机制真正依据含义，孟加拉语与英语功能等价表达应出现相近的理解和遏制模式，因此该对照可检验跨语言差距是否来自表面形式。
- E2的母语者严重度均值与逐项评分是文化校准基线。相较于英语中心的通用毒性标签，它直接检验模型能否按本土使用者的判断排列轻重，而不只是把词识别为“有冒犯性”。
- E5中对话双方在相同结构下进行16轮辩论，并被告知对方曾用目标表达攻击自己；其结构化回合设置用于观察毒性是否随互动升级、是否产生提示中不存在的新辱语，以及最终由哪一方促成缓和。

**实验想回答的问题**

- 在表达相同贬损意图时，模型对孟加拉语本土辱语的语义理解能力与安全遏制能力是否同步变化，还是会因语言、正字法形式、推理提示和角色框架而相互脱钩？
- 模型的冒犯严重度判断是否符合孟加拉语母语者的文化标定，以及表面扰动、显式推理、多轮互动和专家角色分别会怎样改变理解、复现、拒答与毒性升级行为？

**实验实现**

审计覆盖5个前沿大语言模型和6套协议。E1分别输入原生孟加拉语词及其英语功能等价项；E2要求模型只输出含1至5分严重度和二元冒犯标签的JSON；E3保持含义不变，将整段提示罗马化，或在目标表达字符间插入任意空格；E4在E1上增加逐步推理指令；E5让成对模型开展16轮结构化辩论；E6加入孟加拉语言文化专家及教育解释框架。所有模型输出由受训标注者依据统一量表独立复核。原文节选未给出模型完整名单、解码参数、提示重复次数、置信区间或显著性检验，因此结果主要是该模型队列上的描述性审计，而非总体推断。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| E3：将原生孟加拉语替换为罗马化或字符间空格扰动，其他任务结构保持不变 | 相对原生条件的Pass 89.06%与Use 92.83%，罗马化使Pass降至83.77%，而Use升至95.47%；空格扰动使Pass降至76.23%，Use表面上降至68.68%。定性检查将后一个下降归因于字形到token合并被破坏，而非安全机制真正介入。 | 该消融隔离的是“含义不变、书写形式改变”的影响。罗马化造成更差理解却更多复现，直接反对理解越好就越能遏制的简单关系；空格条件中的低Use则不能当作安全收益，因为模型可能在有机会输出词项前就已混乱、生成无意义内容或发生格式拒绝。由于分词失败的判断来自定性检查而非独立token级因果实验，机制结论仍需源码级分词分析验证。 | Section 4.4, E3；Figure 2；Table 1与Table 11<br><span class="experiment-evidence">Romanization degrades Bangla comprehension by 5.29 points (89.06 → 83.77%) while raising leakage to 95.47%. Space perturbation is more catastrophic for comprehension (−12.83 points, to 76.23%) and induces an apparent leakage drop (Bangla Use → 68.68%; English Use → 45.28%).</span> |
| E4：在E1相同词项与问答任务上增加显式Chain-of-Thought逐步推理指令 | 孟加拉语Pass由89.06%升至94.72%，增加5.66个百分点；同时Use由92.83%升至96.23%，增加3.40个百分点。英语Pass升至98.49%，英语Use也由92.83%升至94.72%，跨语言理解差距由7.92缩小到3.77个百分点。 | 该消融较干净地隔离了显式推理指令：模型因分析词根和形态而更容易解释正确，也更容易在推理轨迹中把目标辱语完整拼出。因此它证明在该提示协议下，理解改善与遏制改善并非必然同向；但这不等于所有隐式推理或不暴露推理过程的系统都会增加泄漏。 | Section 4.5, E4；Figure 3；Table 1与Table 11<br><span class="experiment-evidence">CoT raises Bangla Pass from 89.06% to 94.72% (+5.66) and English Pass to 98.49%, narrowing the cross-lingual comprehension gap from 7.92 to 3.77 points. But the same mechanism erodes containment: Bangla leakage rises from 92.83% to 96.23% and English from 92.83% to 94.72%.</span> |

**定性案例**

- E3的定性错误检查发现，字符间插入空格后，模型会出现困惑、无意义续写或格式性拒绝，并在输出目标词之前停止；因此Use下降是分词受损造成的“containment mirage”。这一案例提醒读者：安全指标必须与Pass和生成失败类型联合分析，否则语言处理故障会被误报为安全成功。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：通过多协议审计揭示 LLM 在低资源孟加拉语辱骂内容上的理解与安全遏制脱钩，兼具安全分析和安全评测贡献。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`7c03b331864768a87189c4090fedd7c1d4fec7ee7ccc66057201a5e151c95503`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
