---
title: "[论文解读] When Absence Is Evidence: Evaluating Completeness-Sensitive Negative Reasoning in Large Language Models"
description: "[arXiv 2608.04591][LLM 评测] 本文研究大语言模型能否正确判断“材料中没看到某事物”究竟足以证明其不存在，还是只能说明现有证据不足，并以查询范围是否被证据完整覆盖作为关键判据。"
arxiv_id: "2608.04591"
announcement_date: "2026-08-06"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T06:58:12.666960+00:00"
source_sha256: "3c19ef10f8fb1a2a8f8f0576d9d5bd948c6607e8a5feab54465325e452c31720"
tags:
  - "LLM 评测"
  - "LLM Reasoning"
  - "LLM 其他"
  - "完整性敏感的否定推理"
  - "查询相对完整性"
  - "证据覆盖"
  - "否定许可"
  - "未知判断"
  - "检索增强生成"
  - "开放世界假设"
  - "CROWN-QA"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2608.04591</p>

# When Absence Is Evidence: Evaluating Completeness-Sensitive Negative Reasoning in Large Language Models

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Byoungjae Min, Kennedy Edemacu, Sae-Hong Cho, Yoonhyuk Choi, Beakcheol Jang, Jong Wook Kim</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Department of Computer Science, Sangmyung University, Seoul, Republic of Korea；College of Staten Island, The City University of New York, New York, NY, USA；School of Computer Engineering, Hansung University, Seoul, Republic of Korea；Sookmyung Women’s University, Seoul, Republic of Korea；Graduate School of Information, Yonsei University, Seoul, Republic of Korea</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04591v1) · [PDF 下载](https://arxiv.org/pdf/2608.04591v1) · **关键词** 完整性敏感的否定推理, 查询相对完整性, 证据覆盖, 否定许可, 未知判断, 检索增强生成, 开放世界假设, CROWN-QA<br>


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

本文研究大语言模型能否正确判断“材料中没看到某事物”究竟足以证明其不存在，还是只能说明现有证据不足，并以查询范围是否被证据完整覆盖作为关键判据。

**不用术语来说**：一份材料没有提到某个对象，并不必然意味着该对象不存在。例如，在会议全部论文的官方索引中找不到某个标题，可以据此回答“没有”；但若查看的只是前 20 条搜索结果，或只覆盖主会场的完整索引，就无法排除其他结果或其他分会场中存在该标题，此时只能回答“不知道”。实际应用中的模型却可能把这些情况都当成否定证据，在医疗禁忌、资格排除和文档检索等场景中造成风险。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“完备性敏感的否定推理”问题：当待查事实未出现在证据中时，只有证据完整且覆盖查询要求的全部范围，结论才是“可认证否定”（Certified-Negative）；否则应判为“未知”（Unknown）。
- 作者提出 CROWN-QA 评测框架，通过 CROWN-Synth 在保持问题和已观察事实相同的条件下仅改变覆盖状态，并通过 CROWN-Real 检验真实文档中的迁移表现；配套的结构化证书进一步定位模型是否在查询范围、证据范围或闭合判断上出错。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于自然语言问答、检索增强生成（RAG）与大语言模型不确定性判断的交叉点。传统评测主要考察模型能否找到并忠实使用支持答案的正面证据；本文关注相反但更容易误判的情形：给定记录、列表或检索上下文后，模型能否根据“没有观察到目标”回答目标不存在。关键前提是，未观察到并不等于不存在；只有证据对问题所询问的范围既完整又覆盖充分时，缺失才构成否定证据。例如，完整的全会议论文索引可以证明某标题不存在，但前二十条搜索结果或仅覆盖主会场的完整索引都不能回答涉及所有分会场的问题。该问题可视为开放世界与封闭世界语义在自然语言问答中的查询相对版本：不封闭的证据使未观察事实保持未知，完整且覆盖查询范围的证据才允许推出否定结论。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**查询相对完整性（query-relative completeness）**

证据是否“完整”不能脱离具体问题判断：即使一份材料完整列出了自身范围内的项目，只要该范围没有包含问题要求的全部范围，它对该问题仍不完整。判断重点是查询范围是否被证据范围包含，而不只是材料是否带有“完整列表”之类的描述。

</div>
<div class="concept-item" markdown="1">

**开放世界与封闭世界假设**

开放世界假设认为资料中没有出现的事实仍可能为真，因此结论应为未知；封闭世界假设允许把完整资料中未出现的事实视为假。本文不固定采用其中一种假设，而是先根据证据覆盖范围判断当前问题能否局部采用封闭世界推理。

</div>
<div class="concept-item" markdown="1">

**检索增强生成（RAG）中的上下文充分性**

RAG先检索外部文本，再要求模型依据这些文本作答；上下文充分性通常衡量检索内容是否足以支持答案。本文进一步区分“没有正面支持”与“足以证明不存在”，因为只有后者需要完整且覆盖查询范围的上下文。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入包括一个询问某对象或属性是否存在的自然语言问题、证据所覆盖的范围，以及证据中实际观察到的事实；CROWN-QA将正面支持固定为缺失，使模型只需判断这种缺失能否推出否定。输出是二分类语义判断：若证据完整覆盖查询范围，则输出 Certified-Negative，表示否定答案获得证据认证；否则输出 Unknown，表示现有材料不足以判定。核心判定可概括为：在目标未出现在观察事实中的前提下，只有当证据覆盖完整且查询范围包含于证据范围时，才可从“不在记录中”推出“不存在于查询范围内”。设置中特别包含范围错配：证据可能对自身范围完整，却只覆盖查询范围的一个子集；此时仍须输出 Unknown。普通的正面证据问答不属于本文评测范围。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$Q$**

自然语言查询，以及由该查询限定的目标范围。

</div>
<div class="notation-item" markdown="1">

**$E$**

提供给模型的证据或上下文，包括已观察事实及其覆盖范围。

</div>
<div class="notation-item" markdown="1">

**$S_Q$**

查询要求检查的范围，例如某会议的全部分会场。

</div>
<div class="notation-item" markdown="1">

**$S_E$**

证据实际覆盖的范围；只有证据完整且满足查询范围被其覆盖时，缺失才能支持否定。

</div>

</div>

**直接相关的工作**

- **AbsenceBench（Fu et al., 2025）**: 该工作考察语言模型能否识别被遗漏的内容，但没有检验“缺少支持”在什么覆盖条件下可以推出否定。CROWN-QA固定问题和观察事实，仅改变查询相对覆盖状态，从而把遗漏识别与否定许可区分开。
- **知识库完整性与否定推理（Razniewski et al., 2024）**: 该方向通过开放世界、封闭世界及完整性声明形式化缺失事实的语义，与本文的理论基础最直接相关；区别在于知识库方法通常用符号或元数据表示范围，而CROWN-QA要求模型从自然语言证据中识别范围、完整性及其与查询范围的包含关系。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

检索增强生成、文档问答和高风险决策经常要求模型判断某项信息是否缺失，例如药物禁忌表中是否没有某种病症、排除名单中是否没有某位申请者，或会议论文索引中是否没有匹配标题。此类任务的风险不只是漏读文本，而是把“当前材料未观察到”错误升级为“确定不存在”：只有来源完整，并且其覆盖范围包含问题要求检查的全部范围时，缺失才构成可靠的否定证据。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **可回答性、弃答与知识边界评测**：这类研究根据问题是否可由现有信息回答，要求模型作答、拒答、请求澄清或承认未知；相关任务也会考查歧义信息需求、遗漏信息、错误前提以及模型能否表达自身知识边界。
- **检索增强生成中的相关性、充分性与事实性评测**：这类方法检查检索内容是否与问题相关、是否提供足够的正面支持，以及模型生成的答案是否忠实于上下文；核心通常是发现和使用支持答案的证据，或判断上下文总体上能否支撑作答。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有弃答、不可回答与遗漏信息任务通常没有在保持查询和已观察事实完全不变的同时，只改变证据是否覆盖查询范围。因此，模型表现可能混合了事实识别、文本差异、歧义处理和覆盖判断，无法单独测出它是否理解“未观察到不等于不存在”。
- 相关性或上下文充分性评测主要关注证据是否支持答案，却没有系统区分“证据对自身范围是完整的”和“证据完整覆盖了查询范围”。其后果是：模型可能把完整的主会场索引误当成覆盖全会议，或把部分搜索结果误当成封闭全集，从而产生过度闭合；反过来，始终弃答又会错过证据确实完整时可以合理给出的否定结论。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有自然语言大模型评测很少把“相对于查询的覆盖完备性”作为唯一改变标签的受控变量。尚缺少一种成对评测：固定问题、固定已观察内容，并确保目标事实在各版本中都未出现，仅通过改变证据的完整性或范围，检验模型能否区分开放证据下的 Unknown 与封闭、查询覆盖证据下的 Certified-Negative；同时也缺少能指出错误首先来自证据范围表征还是最终闭合决策的诊断机制。

</div>
<div markdown="1"><span>核心问题</span>

当目标事实在给定材料中均未出现时，大语言模型能否依据证据是否完整且覆盖查询所要求的范围，稳定地区分“可认证否定”与“证据不足、仍属未知”，并且这种能力能否从受控合成场景迁移到真实文档？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把内容缺失固定住，只操纵覆盖条件。这样，两个样例可以拥有完全相同的问题和可见条目，却因一个来源覆盖全部查询范围、另一个仅覆盖部分范围而具有不同答案。若模型真正掌握否定推理，它就必须先比较“问题要求查多大范围”和“证据实际覆盖多大范围”，再决定是否允许从未观察到推出不存在；结构化证书则把这一步拆开记录，使错误不再只表现为最终标签错误，而能追溯到对覆盖关系的误判。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CROWN-QA把“没有观察到某事实”与“能够断言该事实不存在”严格区分开来。输入是自然语言问题$q$及证据集合$E=\{e_1,\ldots,e_n\}$；论文预先保证证据的事实内容不直接支持所查询事实，因此模型无需检索正面答案，而只需判断证据覆盖范围是否足以封闭问题范围。具体而言，模型需要从问题中识别查询范围$S(q)$，从证据文本及其来源语义中识别覆盖范围$S(E)$和覆盖状态，再判断证据是否完整覆盖$S(q)$。若覆盖完整且范围匹配，则输出Certified-Negative；若覆盖部分、抽样、未说明、存在歧义，或完整覆盖的是另一个范围，则输出Unknown。

直观地说，看到名单里没有“小王”并不自动说明小王不在目标群体中：只有当名单明确是目标群体的完整名单时，缺席才构成否定证据。该方法本身不是新的模型架构或训练算法，而是一套隔离“否定答案授权”能力的二分类评测框架；其核心设计是保持问题和已观察事实不变，只改变与查询相关的覆盖条件，从而检验模型是否真正依据证据完整性改变判断，而不是仅凭措辞、事实缺席或默认的封闭世界假设作答。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造缺席条件下的评测输入

评测实例被限制为查询事实在$E$的已观察事实内容中没有正面支持，使后续决策只考查“这种缺席能否授权否定结论”。覆盖信息可以涉及时间段、实体、属性、列表、数据库字段或文档集合。

<div class="method-step__io" markdown="1">

**输入**：自然语言问题$q$与证据上下文$E=\{e_1,\ldots,e_n\}$，其中证据可同时包含事实陈述和显式或隐式的覆盖信息。<br>
**输出**：一个不含查询事实正面支持、但包含不同覆盖条件的$(q,E)$实例。

</div>

**直观理解**：先排除“模型只是找到了答案”这一可能性，让所有样本表面上都看不到目标事实；真正需要判断的是证据是否查得足够全。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 解析查询范围与证据覆盖

从$q$确定查询要求的语义范围$S(q)$，并从$E$确定证据声称覆盖的范围$S(E)$及其完整、部分、抽样、未指定或歧义状态。范围匹配按语义而非词面判断，因此时间、实体、属性、总体或文档集合不一致都会影响闭合性。

<div class="method-step__io" markdown="1">

**输入**：实例$(q,E)$及证据中关于来源、范围和完整性的自然语言描述。<br>
**输出**：查询范围$S(q)$、证据覆盖范围$S(E)$以及证据自身的覆盖状态。

</div>

**直观理解**：这一步相当于分别回答“问题究竟问哪一块”和“材料究竟完整检查了哪一块”；即使两段文字用了相似词语，只要实际对象或时间不同，也不能视为覆盖。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 计算查询相对的闭合判断

仅当$E$确立了对$S(E)$的完整覆盖，并且$S(q)\subseteq S(E)$时，令$c=\mathrm{Comp}(E,S(q))=1$；其余情况令$c=0$。这使“完整性”成为相对于当前查询的性质，而不是证据来源的全局标签。

<div class="method-step__io" markdown="1">

**输入**：查询范围$S(q)$、证据范围$S(E)$及证据覆盖状态。<br>
**输出**：二值闭合变量$c\in\{0,1\}$。

</div>

**直观理解**：一本书即使被完整读完，也只能排除书中应当记录的事项，不能排除书外世界中的事项；因此既要“资料完整”，也要“完整的范围确实包住问题范围”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成标签或结构化证书

直接标签条件下，$c=1$映射为Certified-Negative，$c=0$映射为Unknown；Certificate条件下解析JSON，并将布尔字段$complete_for_query$的true和false分别映射到这两个标签。Self-check使用第二次响应作为最终预测，CoT类条件则从规定的最终标签行或最终JSON对象取值。

<div class="method-step__io" markdown="1">

**输入**：闭合判断$c$，或提示模型显式给出的$query_scope$、$evidence_coverage_scope$和$complete_for_query$字段。<br>
**输出**：统一二分类预测$\hat{y}\in\{\text{Certified-Negative},\text{Unknown}\}$，以及证书条件下可供错误定位的中间字段。

</div>

**直观理解**：模型既可以只交最终答案，也可以先填写“问题范围、材料范围、是否完整覆盖”这张检查表；后者用于判断错误究竟发生在范围理解还是最终决策。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 查询相对闭合与目标标签

$$
c=\mathrm{Comp}(E,S(q))\in\{0,1\},\qquad c=1\iff \bigl(E\text{ establishes complete coverage of }S(E)\bigr)\land S(q)\subseteq S(E),\qquad y^{*}(q,E)=\begin{cases}\textsc{Certified-Negative},&c=1,\\ \textsc{Unknown},&c=0.\end{cases}
$$

**符号说明**

- $q$：自然语言问题。
- $E=\{e_1,\ldots,e_n\}$：由事实陈述及覆盖信息组成的证据上下文。
- $S(q)$：问题要求判断的语义范围，例如特定时间、实体、属性、总体或文档集合。
- $S(E)$：证据声称覆盖的语义范围。
- $c=\mathrm{Comp}(E,S(q))$：证据是否对当前查询范围构成完整闭合的二值变量；$c=1$表示闭合，$c=0$表示不闭合。
- $y^{*}(q,E)$：实例$(q,E)$的金标准标签。

<div class="equation-explanation" markdown="1">

**直观理解**：该式规定了任务的决策边界：在查询事实已知没有正面支持的前提下，只有“证据自身完整”与“证据范围覆盖问题范围”同时成立，缺席才可升级为Certified-Negative。只要任一条件缺失，正确行为就是Unknown，而不是猜测事实不存在。<br>
**原文位置**：Task Definition，Absence-Conditioned Completeness Judgment

</div>

</div>

<div class="equation-block" markdown="1">

#### 配对完整性敏感度

$$
\mathrm{CS}=\Pr\!\left[\hat{y}(x_c)=\textsc{Certified-Negative}\ \wedge\ \hat{y}(x_o)=\textsc{Unknown}\right],\qquad x_c=(q,E_c),\quad x_o=(q,E_o)
$$

**符号说明**

- $\mathrm{CS}$：配对完整性敏感度，即一对样本的两个方向都预测正确的比例。
- $\hat{y}$：模型输出的预测标签。
- $x_c=(q,E_c)$：完整且覆盖查询范围的配对成员，其金标签为Certified-Negative。
- $x_o=(q,E_o)$：与$x_c$共享问题和已观察事实、但证据不闭合的配对成员，其金标签为Unknown。

<div class="equation-explanation" markdown="1">

**直观理解**：CS不因模型只答对配对中的一个样本就给足信用。它要求模型面对相同问题和事实时，仅根据覆盖条件的改变，从Certified-Negative正确切换到Unknown，因此比单例准确率更直接地检验论文关注的推理能力。<br>
**原文位置**：Task Definition，Metrics

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。CROWN-QA是推理阶段的评测方法，所评估的Qwen3.5-9B、Gemma-4-12B和Claude Haiku 4.5均为已有的指令微调模型；原文没有用CROWN-QA继续训练模型，也没有定义供参数优化的损失函数。形式化目标$y^*(q,E)$用于生成或判定金标签，OCR、UCR、类别平衡准确率和CS用于评分，均不应被解释为训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 查询相对覆盖判定器**

核心判定不是检查$E$是否笼统地被称为“完整”，而是联合检查证据对其声称范围$S(E)$是否完整，以及查询范围是否满足$S(q)\subseteq S(E)$。任何部分覆盖、抽样、未指定、歧义或范围错配均被视为$c=0$。

> 直观理解：它防止模型把“这份材料本身很完整”误解成“它能回答所有缺席问题”；完整材料只有在覆盖当前问题所问范围时才有否定效力。

**2. 受控覆盖对**

CROWN-Synth使用共享同一问题$q$和同一已观察事实的配对$x_c=(q,E_c)$与$x_o=(q,E_o)$，只改变与查询相关的覆盖条件；前者金标签为Certified-Negative，后者为Unknown。该设计把事实内容与覆盖信息解耦，使CS能够直接测量模型对完整性变化的敏感程度。

> 直观理解：可以把它理解为同一道题配两份事实相同的名单：一份声明是完整名单，另一份只是抽样；模型只有因这一区别改变答案，才说明它理解了缺席证据的适用条件。

**3. 结构化证书与字段级诊断**

Certificate提示要求模型返回包含$query_scope$、$evidence_coverage_scope$和$complete_for_query$的JSON对象，评分器由最后一个布尔字段生成最终标签。错误分析依次核对查询范围、证据范围与覆盖状态、最终布尔判断，并把错误分配给第一个失败字段。

> 直观理解：最终标签只能说明答错了，证书则展示模型的判断链条；例如它可能正确理解问题，却把“抽样记录”误认为完整记录，这种错误可被单独定位。

**训练与推理**

推理时，每个模型接收同一冻结版本数据集中的问题与完整证据上下文，且不提供上下文示例。根据实验条件，模型直接输出标签，或经过Definition-aware、Abstain、CoT、Self-check、Certificate等提示流程生成结果；其中Self-check通常顺序调用两次，第一次产生初始标签，第二次响应作为最终预测，其余条件通常调用一次。所有输出最终统一映射到$\{\text{Certified-Negative},\text{Unknown}\}$：直接提示读取标签，CoT读取以FINAL LABEL:开头的最终行，Certificate读取JSON中的$complete_for_query$，Certificate+CoT读取FINAL_JSON:之后的对象。

评分时，无法解析的首次响应会在输入、提示和生成设置不变的情况下重试一次；第二次可解析则用于评分，仍不可解析则记为错误并保留在分母中，不能默认映射为Unknown。对于结构化证书，评分脚本先核对$query_scope$，再核对$evidence_coverage_scope$及覆盖状态，最后核对$complete_for_query$，从而把错误定位到第一个失败环节。该流程评估的是现成模型在不同提示条件下的闭合判断稳定性，而不是通过反馈更新模型参数。

**复现信息**

实验覆盖三个指令微调模型：Qwen3.5-9B、Gemma-4-12B和Claude Haiku 4.5；各基准对所有模型使用相同的冻结数据版本且不提供in-context examples。开放权重模型在Google Colab的一张NVIDIA A100 GPU上运行，Claude Haiku 4.5通过Anthropic API访问。所有调用的temperature为$0$，开放权重模型采用greedy decoding，以尽量减少随机采样对覆盖判断比较的干扰。

每次调用最多生成5120个新token，问题和证据上下文均不截断，因此结果不应归因于输入范围被裁剪。Definition-aware+Self-check通常每例需要两次顺序调用，其他条件通常一次；解析失败最多按相同设置重试一次。作者说明提交的artifact包含数据集、精确提示词、原始输出、推理与评分代码、模型配置及Python环境，但所给章节未提供训练过程，因为该研究执行的是零样例推理评测。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- CROWN-Synth：受控合成配对数据集，是检验因果性失效模式的核心测试集。每对样本固定问题与已观察事实，只改变证据对查询范围的覆盖状态；实验重点比较“完整覆盖—部分覆盖”和“完整覆盖—范围不匹配”两类配对。完整—部分分支共有1250对，并按$L1$至$L4$四种覆盖机制细分；其中$L3$用于测试隐式完整证据与隐式部分证据的辨别，是论文发现的主要瓶颈。
- CROWN-Real Proceedings：来自真实会议录文档的A/B/C对照变体。A覆盖完整查询范围，正确答案为Certified-Negative；B只完整覆盖更窄的集合，属于范围不匹配；C只包含被查询集合的部分标题，属于部分覆盖。它用于检验合成实验中“部分覆盖比窄范围完整覆盖更容易诱发过度闭包”的排序能否迁移到真实文本。
- CROWN-Real Medical：来自真实医疗文档的覆盖变体，用于检验不同文档来源和结构下的迁移。A是查询覆盖变体，B应回答Unknown；医疗数据中的C是显式部分覆盖控制，因此作者没有把它纳入Proceedings式的隐式部分覆盖差值比较。所给章节未明确报告两个CROWN-Real来源的样本规模或训练、验证、测试划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy（Acc）**

在统一的Certified-Negative/Unknown二标签空间中，逐样本预测正确的比例。它反映总体正确率，但可能掩盖模型在配对两端使用同一标签的情况。 （越高越好，因为表示单个样本的闭包结论更常与标注一致。）

</div>
<div class="metric-item" markdown="1">

**Closure Sensitivity（CS）**

配对敏感性指标：只有模型同时把完整覆盖成员判为Certified-Negative、把对应的不闭包成员判为Unknown，该配对才算正确。它直接测试模型是否会随着查询相对覆盖变化而切换判断。 （越高越好，因为高$CS$意味着模型真正区分覆盖条件，而非碰巧依赖固定回答偏好。）

</div>
<div class="metric-item" markdown="1">

**Over-Closure Rate / Under-Closure Rate（OCR/UCR）**

$OCR$衡量模型把不闭包证据错误判为Certified-Negative的比例；$UCR$衡量模型把完整且覆盖查询的证据错误判为Unknown的比例。二者必须联合观察，因为更保守的提示可能降低$OCR$却提高$UCR$。 （二者均越低越好；只降低其中一个不足以证明辨别能力提高，因为错误可能只是从过度闭包转移为不足闭包，或反向转移。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### CROWN-Synth总体闭包表现，比较三个模型在Naive、显式规则及推理提示下的错误结构

<div class="result-value" markdown="1">

Naive条件下，三个模型均表现为$OCR$高于$UCR$，说明默认错误方向是把不完整证据当作足以支持否定。显式规则使三个模型的Accuracy和$CS$均提高，继续加入CoT又提高这两个总体指标；但不同干预不能稳定地同时降低$OCR$和$UCR$。作者据此主张，模型具备一定的完整性敏感推理能力，却没有形成稳定的查询相对闭包判断。

</div>

总体分数改善不等于核心推理缺陷被消除：模型可能因为提示而更偏向Unknown或Certified-Negative，从而在一类样本上少犯错、在另一类样本上多犯错。该结果支持“闭包判断不稳定”，但不能证明模型内部采用了特定推理机制，也不能单靠总体Accuracy说明配对辨别已经改善。

<div class="result-source" markdown="1">

来源：Overall Closure Profiles，Table 3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under Naive prompting, OCR exceeds UCR for all three models, revealing a default tendency to license negative answers from non-closing evidence rather than remain uncertain. Explicit task rules improve Acc and CS for all three models, and adding CoT further improves both metrics. However, these aggregate gains do not consistently reduce OCR and UCR together: abstention lowers OCR by increasing UCR, while self-checking and certificate elicitation have model-dependent effects.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### CROWN-Synth失效条件分析，重点考察1250个完整—部分配对中的$L3$隐式覆盖机制

<div class="result-value" markdown="1">

在所有模型与提示条件组合中，$L3$的$CS$总是最低或并列最低。$L3$完整成员的正确率为82.4%至100.0%，而部分成员的正确率仅为0.0%至27.9%。因此，配对失败主要不是模型无法识别隐式完整证据，而是它把形式相似的隐式部分证据也误判为Certified-Negative。

</div>

这是论文最关键的不对称性：模型能处理“证据实际上完整”的一半，却不能可靠识别“证据看似充分但仍缺一部分”的另一半。由于问题和观察事实按对固定，该差异较有力地指向覆盖判断缺陷；不过它只证明这些受控机制下的行为差异，不能直接推断所有开放域检索任务都会出现相同比例的错误。

<div class="result-source" markdown="1">

来源：Failure Conditions，Table 5；完整条件见Appendix D，Table 13

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As shown in Table 5, L3 has the lowest or tied-lowest CS in every model–condition row. Within L3, the correct rate for the complete member ranges from 82.4 to 100.0%, whereas that for the partial member ranges from 0.0 to 27.9%. Thus, the low L3 CS is driven primarily by predicting Certified-Negative for the partial member, rather than by errors on the complete member.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### CROWN-Real Proceedings真实文档迁移，对比范围不匹配的B变体与部分覆盖的C变体

<div class="result-value" markdown="1">

在Proceedings的全部15个模型—提示组合中，$\Delta_{B-C}=\text{B-UNK}-\text{C-UNK}$均不小于0，其中12个组合的bootstrap区间排除0。B和C的正确标签都为Unknown，但C的正确率更低，表明模型更容易把部分覆盖C误判为Certified-Negative；这一难度排序与CROWN-Synth一致。

</div>

真实文档结果说明，部分覆盖过度闭包不只是合成模板现象，而且相对于“只完整覆盖较窄范围”的证据，部分证据至少同样困难。然而，结果并不表示所有模型、提示和来源具有相同错误幅度；作者明确指出查询覆盖样本的准确率和部分覆盖差距会随模型、提示与文档来源变化。

<div class="result-source" markdown="1">

来源：Transfer to CROWN-Real，Table 8；置信区间见Appendix D，Table 20

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across all 15 model–condition cells, ΔB−C is nonnegative, and its bootstrap interval excludes zero in 12 (Appendix D, Table 20). Because B and C are both labeled Unknown, the lower C-UNK rates show that models more often predict Certified-Negative for partial C than for narrower-complete B.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验只覆盖三个模型、七类提示条件和温度为0的单次贪心解码；所给章节没有报告采样解码、不同随机运行、少样本示范或更广泛模型规模下的结果。因此，跨模型的共同失效模式具有证据支持，但其普遍性和运行稳定性仍需额外验证。
- 真实文档迁移只展示Proceedings与Medical两种来源，且Medical的C是显式部分覆盖控制，不能直接参与Proceedings式的隐式部分覆盖比较。CROWN-Real支持该现象超出合成数据，但尚不足以证明其在任意检索系统、长文档结构或开放域事实核验中同样成立。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Naive：不给出任务规则，测量模型默认如何解释“记录中没有观察到某项”。它是判断模型是否天然把缺失错误地当作否定证据的基础参照。
- Definition-aware（Def.）：明确告知只有证据完整覆盖查询范围时，缺失才能支持Certified-Negative。与Naive比较可隔离“知道判定规则”本身的作用。
- Definition-aware+CoT（Def.+CoT）：在显式规则基础上要求逐步推理。它检验推理过程是否修复覆盖判断，还是仅改变模型在完整与不完整证据之间的错误分布。
- Certificate（Cert.）：要求输出结构化证书$(\hat{S}_q,\hat{S}_E,\hat{c})$，分别描述查询范围、证据范围和最终覆盖判断；只有$\hat{c}$映射为评分标签，前两个字段用于诊断。它既是提示条件，也用于定位错误首先来自范围理解还是最终布尔决策。

**实验想回答的问题**

- 配对闭包判断与失效条件：当问题和已观察事实完全相同、只有相对于查询范围的证据覆盖发生变化时，模型能否稳定地区分“可认证否定”（Certified-Negative）与“未知”（Unknown）；错误是否特别集中在部分覆盖和范围不匹配情形？
- 干预与迁移：显式规则、思维链、保守弃答、自检和结构化证书能否真正改善配对辨别，错误最早出现在哪个证书字段；在真实文档中，合成数据上的部分覆盖过度闭包是否仍然存在？

**实验实现**

实验评估Qwen3.5-9B、Gemma-4-12B和Claude Haiku 4.5，覆盖两个开放权重模型家族和一个API模型家族。每个样本在各提示条件下接收相同的问题与证据上下文，不使用少样本示例；采用温度为0的贪心解码，并统一映射到Certified-Negative/Unknown二标签空间。表格把比例报告为百分数、把差值报告为百分点。作者使用10000次bootstrap给出百分位数95%置信区间：CROWN-Synth按匹配样本对重采样，CROWN-Real按A/B/C对照组重采样。该协议控制了解码随机性和输入差异，因而提示条件之间的比较主要反映指令变化；但它没有检验采样解码、少样本示范或重复运行下的稳定性。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 在Definition-aware基础上加入CoT，按完整、$L3$部分、$L4$部分和范围不匹配样本逐项比较准确率变化 | Qwen加入CoT后，完整样本提高8.9个百分点，但$L3$部分、$L4$部分和范围不匹配样本分别下降3.8、7.7和11.1个百分点；Haiku对应变化为+11.8、-5.8、-4.2和+3.6个百分点；Gemma则为+0.5、+6.7、+6.1和+9.8个百分点。CoT因此不是统一的修复器：它改善Qwen和Haiku完整证据判断时，可能加剧部分覆盖错误，而Gemma呈现更广泛的非闭包修复。 | 该消融只改变是否要求逐步推理，从而隔离CoT的边际作用。正负变化并存且跨模型方向不同，说明总体Accuracy提升可能来自特定样本组，而非普遍改善查询相对覆盖判断；这些数字是项目级净变化，不能揭示模型实际生成的推理步骤是否忠实。 | Prompting Effects，Table 6；列顺序为Complete、L3-Part.、L4-Part.、SM<br><span class="experiment-evidence">Qwen Def. → Def.+CoT +8.9 -3.8 -7.7 -11.1; Haiku Def. → Def.+CoT +11.8 -5.8 -4.2 +3.6; Gemma Def. → Def.+CoT +0.5 +6.7 +6.1 +9.8</span> |
| 错误Certificate的字段级诊断，将每个错误归到最早偏离标注的查询范围、证据覆盖或最终布尔判断 | Qwen的858个错误中，查询范围、证据覆盖和布尔判断分别占24.4%、50.1%和25.5%；Haiku的606个错误中分别占23.9%、45.4%和30.7%；Gemma的1438个错误中分别占26.7%、72.0%和1.3%。三个模型的最大错误来源均为证据覆盖字段$\hat{S}_E$，Gemma尤其集中。 | 该分析隔离了结构化证书中最早出现的可观察错误，表明许多最终标签错误之前已经发生了证据范围或完整性误表征。它是对模型输出的诊断分解，而不是内部因果机制证明：模型可能生成与其真实计算过程不完全一致的证书。 | Diagnostic Decomposition，Table 7；列顺序为#Err.、Query $\hat{S}_q$、Evidence $\hat{S}_E$、Boolean $\hat{c}$<br><span class="experiment-evidence">Qwen 858 24.4 50.1 25.5; Haiku 606 23.9 45.4 30.7; Gemma 1438 26.7 72.0 1.3</span> |

**定性案例**

- Proceedings的B/C对照构成一个集合层面的定性案例：B对某个被查询集合是完整的，却没有覆盖整个查询范围；C则只列出被查询集合中的部分标题。两者都应回答Unknown，但模型更常把C判为Certified-Negative。这说明模型可能把“看到了一个像清单的局部列表”误当成“已穷尽查询范围”，而对显式较窄的完整范围反而更容易保持不确定。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces controlled benchmarks for evaluating LLM completeness-sensitive negative reasoning and diagnoses systematic closure errors.; rule check: matched taxonomy keywords; top rule score=9.0
- 全文指纹：`3c19ef10f8fb1a2a8f8f0576d9d5bd948c6607e8a5feab54465325e452c31720`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
