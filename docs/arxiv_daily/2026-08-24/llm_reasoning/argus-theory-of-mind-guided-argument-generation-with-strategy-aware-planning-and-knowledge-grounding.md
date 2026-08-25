---
title: "[论文解读] ARGUS: Theory-of-Mind Guided Argument Generation with Strategy-Aware Planning and Knowledge Grounding"
description: "[arXiv 2608.20405][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.20405"
announcement_date: "2026-08-24"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-25T01:57:52.323832+00:00"
source_sha256: "70569cfe14482cd5758778b1550b298fa4626fa9503b058e25f8eb3c1f0807f1"
tags:
  - "LLM Reasoning"
  - "自动论证生成"
  - "说服性文本生成"
  - "心智理论"
  - "受众建模"
  - "修辞规划"
  - "证据检索"
  - "大语言模型智能体"
  - "知识落地"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.20405</p>

# ARGUS: Theory-of-Mind Guided Argument Generation with Strategy-Aware Planning and Knowledge Grounding

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Zhe Hu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The Hong Kong Polytechnic University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.20405) · [PDF 下载](https://arxiv.org/pdf/2608.20405) · **关键词** 自动论证生成, 说服性文本生成, 心智理论, 受众建模, 修辞规划, 证据检索, 大语言模型智能体, 知识落地<br>


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

本文属于自然语言处理中的自动论证生成，目标不是仅生成通顺文本，而是针对特定受众组织能够改变其立场的说服性论证。该任务要求模型同时处理三类信息：受众当前相信什么、重视什么以及可能抵触什么；应采用何种修辞功能来表达各个子论点；哪些可核查事实能够支撑这些论点。现有大语言模型智能体通常通过“规划—写作”分解或多智能体辩论改善长文本的连贯性，但受众心理状态往往只是提示词中的隐含上下文，规划也主要决定内容顺序，检索则常在写作前统一进行或在草稿后补充。ARGUS据此将任务建模为受众感知的闭环结构优化：先显式构造受众的对手模型与价值模型，再按子主题分配逻辑、情感、可信度和时机等修辞功能，同时围绕局部修辞目标检索证据，最后诊断并定向修订论证。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**心智理论（Theory of Mind, ToM）**

心智理论指推断他人信念、意图、情绪和价值取向的能力。本文关注的不是被动预测受众想法，而是利用显式受众模型规划如何推动其立场变化。

</div>
<div class="concept-item" markdown="1">

**经典修辞模式**

本文使用四类修辞功能：logos强调逻辑与证据，pathos诉诸情感，ethos建立说话者的可信度，kairos强调表达的时机与情境适切性。它们不是事后文风标签，而是规划每个子主题时使用的结构单元。

</div>
<div class="concept-item" markdown="1">

**知识落地与证据检索**

知识落地是用外部可核查材料约束论证中的事实性主张，降低无依据陈述。ARGUS按子主题及其修辞目标生成检索查询，使证据在规划阶段参与决定论证结构，而非仅在草稿完成后补丁式加入。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入至少包括待论证的命题、目标受众的初始立场，以及围绕命题检索得到的背景与事实证据；给出的示例中，输入分析器还区分背景摘要和从检索片段提取的具体主张。系统需要输出一篇面向该受众的完整说服性论证，其内容既要回应受众已有主张和情绪阻力，也要与受众价值建立连接，并以外部证据支撑关键事实。ARGUS假设大语言模型可承担多个智能体模块的自然语言推理，并将受众表示为显式的双重心智模型：对手模型$[0m\Psi_{\mathcal{O}}$描述受众的论点与情绪触发因素，价值模型$[0m\Psi_{\mathcal{V}}$描述其价值取向及可采用的桥接策略；二者合成的$[0m\Psi$用于约束后续子主题分解、修辞分配、反驳预防和证据检索。该设置关注面向特定立场的单篇论证生成，而不是无受众条件的通用文章写作；作者还以扮演抵触方的评审模拟论证是否能够诱发立场转移。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\Psi$**

ToM推理器生成的完整受众心智表示，供后续规划与生成模块使用。

</div>
<div class="notation-item" markdown="1">

**$\Psi_{\mathcal{O}}$**

对手模型，记录目标受众的已有主张、信念依据、情绪触发因素和潜在抵触。

</div>
<div class="notation-item" markdown="1">

**$\Psi_{\mathcal{V}}$**

价值模型，记录目标受众重视的原则、价值景观以及连接这些价值的桥接策略。

</div>

</div>

**直接相关的工作**

- **文本规划、分解式写作与多智能体辩论框架**: 这些方法将长篇论证拆分为规划和写作阶段，或通过智能体之间的辩论与自我博弈反复润色，因而比单步生成更连贯。但原文指出，它们通常将受众作为隐含上下文，并主要规划“接下来讲什么”；ARGUS进一步显式建模受众，并在“如何说”的修辞功能粒度上进行规划。
- **面向说服的心智理论与受众建模研究**: 既有研究包括说服对话中的ToM基准、使用ToM训练的对手感知说服者，以及双知识或元认知多智能体说服框架；相关研究也发现，针对目标受众定制内容可提升大语言模型的说服力。本文沿用这一受众适配方向，但强调“规划型ToM”：将显式的对手模型和价值模型直接用于子主题拆解、修辞匹配、预先回应反论点与局部证据检索，而不只评估模型能否预测他人信念。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

说服性论证生成不仅要求语言通顺和观点连贯，还要求论证能够针对特定受众的既有信念、价值取向与抵触情绪进行调整，并使用可靠证据支撑具体论点。现有系统若忽略受众差异，或只生成一般性的论证文本，就可能产生逻辑上合理但无法有效影响目标受众的内容；这会限制其在写作辅助、政策分析、对话工具和辩论系统中的实际应用。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **端到端或规划后生成方法**：早期方法直接从题目或立场生成完整论证；较新的智能体方法通常先进行内容规划，再依据提纲生成和修改文本。这类方法主要解决长文本的结构连贯性与表面表达质量问题。
- **独立的事实检索与多智能体迭代方法**：一类方法在写作前进行文档级检索，另一类方法在草稿形成后补充或修正事实依据；多智能体系统还会通过自我讨论、辩论或反复润色来改进内容。它们能够增强一般性的逻辑性、流畅性或事实支撑，但检索和修改未必由具体论证目标驱动。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 受众无关：现有方法缺少对受众心理状态的显式建模，因而不能系统表示受众相信什么、重视什么以及可能产生何种情绪抵触。其后果是同一套论证可能被机械地用于不同受众，难以实现针对性的说服。
- 策略无关且证据脱节：现有规划器多关注“先说什么、后说什么”，却没有把逻辑说服、情感诉求、可信度建构和时机选择等修辞功能作为明确的规划对象；同时，证据检索常被放在整体写作之前或草稿之后，不能根据每个子论题的修辞目标动态生成查询和选择证据。因此，文本可能结构完整，却缺少与受众和局部说服任务匹配的表达策略与证据。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚未形成一个闭环框架，把受众的信念与价值建模、细粒度修辞策略选择，以及面向具体子论题的证据检索统一到写作规划阶段。更具体地说，仍缺少一种方法能够先构造可供后续模块使用的受众心理表示，再据此决定每个子论题应采用何种说服功能，并让相关证据从一开始就服务于该策略，而不是事后修补。

</div>
<div markdown="1"><span>核心问题</span>

能否通过显式的受众心智建模，将受众信念和价值信息传递给组件级论证规划器，使系统为不同子论题选择合适的修辞策略并在规划阶段检索相应证据，随后通过针对性修订提高对持怀疑立场受众的实际说服效果？

</div>
<div markdown="1"><span>作者直觉</span>

说服效果取决于论证内容与受众心理之间的匹配，而不只是文本本身是否流畅。ARGUS的切入点是先让理论心智推理器生成受众信念与价值的双重描述，再让规划器把每个子论题分配给适合的修辞功能，并依据该功能检索证据。直观上，这相当于先回答“面对这个人，应该用什么理由、以什么方式、配什么依据”，再开始写作；最后的定向修订则检查并修复局部弱点，减少泛化式润色无法解决的策略错误。作者因此主张，该流程有望把语言质量提升转化为更具体的受众立场变化，但论文同时承认，模拟受众并不等于真实受众，心智模型和说服效果仍需进一步的人类研究验证。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

ARGUS将论证生成从一次性提示改造成五个可解释阶段：输入分析、心智理论推理、论证规划、论证写作和迭代精炼。给定争议命题$x$与立场$s\in\{\mathrm{support},\mathrm{refute}\}$，系统先检索并组织事实与逻辑信息，再显式建模受众的反对立场、情绪主题和价值观，随后为每个子论题分配修辞策略、关键主张、证据和预期反驳，最后生成并反复修订文章$y$。直观地说，ARGUS不是让模型直接“写一篇有说服力的文章”，而是先判断对谁说、对方担心什么、每一步应采用何种说服方式，再据此写作和检查。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 输入分析与知识检索

Input Analyzer先判断是否需要外部知识；需要时生成针对性网络查询，并将检索到的网页片段纳入上下文。随后提取输入中的关键主张、检索背景知识，并在输入是完整论证时分解前提、隐含假设和潜在逻辑缺口。

<div class="method-step__io" markdown="1">

**输入**：争议命题$x$、目标立场$s$，以及命题可能附带的完整论证文本。<br>
**输出**：结构化输入表示，包括关键主张、基于检索结果综合出的背景知识，以及可选的逻辑结构分解。

</div>

**直观理解**：这一步类似写作者在动笔前先读懂题目、查资料并找出对方论证中的薄弱环节。与只依赖模型记忆相比，检索结果为后续论证提供了可追溯的事实基础。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 受众心智理论建模

ToM Reasoner构造双重受众心智模型$\Psi=(\Psi_{\mathcal{O}},\Psi_{\mathcal{V}})$：$\Psi_{\mathcal{O}}$描述受众可能持有的具体立场、驱动这些立场的信念或动机，以及能引起共鸣的情绪主题；$\Psi_{\mathcal{V}}$描述受众的价值观和将目标立场与冲突价值观连接起来的桥接策略。

<div class="method-step__io" markdown="1">

**输入**：命题$x$、立场$s$和输入分析结果。<br>
**输出**：面向受众的论证画像，包括预期反对意见、心理动因、情绪诉求、价值观和价值协调方式。

</div>

**直观理解**：系统不再把受众当作模糊背景，而是先建立一个“对方怎么看、为什么这么看、最在乎什么”的显式档案。这样后续规划可以直接决定哪些异议要提前回应，以及如何避免让受众产生心理逆反。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 策略感知的论证规划与证据检索

Argument Planner生成子论题序列$\mathcal{P}=\langle t_1,t_2,\ldots,t_n\rangle$，并为每个子论题指定主修辞成分、关键主张、可选证据和预期反驳。主修辞成分从$\{\mathrm{logos},\mathrm{pathos},\mathrm{ethos},\mathrm{kairos},\mathrm{evidence}\}$中选择；对于需要事实支撑的子论题，规划器围绕该子论题的修辞功能和主张重新生成查询并检索证据，然后根据修辞多样性、ToM一致性、逻辑顺序和立场一致性自评计划，必要时重新规划和检索。

<div class="method-step__io" markdown="1">

**输入**：输入分析结果和受众模型$\Psi$。<br>
**输出**：可检查的结构化蓝图$\mathcal{P}$，其中每个子论题包含修辞策略、关键主张、局部证据和预期反驳。

</div>

**直观理解**：这相当于先画文章施工图：不仅安排“先讲什么、后讲什么”，还规定每段要靠逻辑、情感、信誉、时机或证据中的哪种方式说服。证据按段落分别检索，避免把一堆无差别资料平均撒进全文。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按计划写作

Argument Writer将计划展开为完整论证文章，并保持计划规定的修辞构成、子论题顺序、局部证据对应关系和受众价值衔接。写作阶段不重新决定核心论证结构，而是将已规划的控制信号实现为连贯文本。

<div class="method-step__io" markdown="1">

**输入**：结构化论证计划$\mathcal{P}$，其中包含受众价值框架、局部证据和预期反驳。<br>
**输出**：初始论证草稿$v_1$。

</div>

**直观理解**：写作者此时主要负责把蓝图变成文章，而不是边写边临时决定策略。这样可以减少文章表面流畅但没有回应目标受众关键疑虑的问题。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 条件论证生成任务

$$
y=\mathcal{M}(x,s)
$$

**符号说明**

- $y$：生成的论证文章。
- $\mathcal{M}$：ARGUS所实现的论证生成框架。
- $x$：争议主题上的命题，可以是简短主张或长篇、包含观点的论证文本。
- $s\in\{\mathrm{support},\mathrm{refute}\}$：目标立场，分别表示支持或反驳命题。

<div class="equation-explanation" markdown="1">

**直观理解**：该式定义了系统要解决的问题：根据命题和目标立场生成一篇能够为该立场辩护的文章。ARGUS的关键变化不是改变这个输入输出关系，而是将原本可能由一次提示完成的$\mathcal{M}$拆成可解释的分析、建模、规划、写作和精炼动作。<br>
**原文位置**：第3.1节，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 子论题属性表示

$$
\mathrm{Attr}(t_i)=(c_i,k_i,e_i,r_i)
$$

**符号说明**

- $t_i$：论证计划中的第$i$个子论题。
- $c_i\in\{\mathrm{logos},\mathrm{pathos},\mathrm{ethos},\mathrm{kairos},\mathrm{evidence}\}$：该子论题的主要修辞成分：逻辑、情感、信誉或共同规范、紧迫性或时机、经验性证据。
- $k_i$：该子论题需要表达的关键主张集合。
- $e_i$：与该子论题对应的可选外部证据。
- $r_i$：预期受众反驳，用于在正文中提前回应。

<div class="equation-explanation" markdown="1">

**直观理解**：该式把每个段落的说服任务写成结构化记录，而不是只保存段落标题。规划器因此同时决定段落讲什么、采用哪种修辞、依据什么事实，以及要先化解哪一种异议。<br>
**原文位置**：第3.5节，公式(2)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文未报告ARGUS的参数训练目标或梯度优化过程。方法描述的是基于大语言模型提示、结构化中间表示、网络检索和推理时迭代的生成框架；因此，在所给章节中，ARGUS主要属于推理阶段的流程设计，而不是提出新的可训练损失函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双重受众心智模型**

ToM Reasoner输出$\Psi=(\Psi_{\mathcal{O}},\Psi_{\mathcal{V}})$。其中$\Psi_{\mathcal{O}}$是受众的论证画像，包含情绪主题、具体立场及其信念或动机；$\Psi_{\mathcal{V}}$是开放式自然语言价值观集合，并包含将目标论点与潜在冲突价值观协调起来的桥接策略。该表示被传递给规划器，而不是仅隐含在一次生成提示中。

> 直观理解：该模块回答“应该如何对这个人说服”，而不是只回答“这个命题有哪些论据”。显式记录受众的担忧和价值观，使系统能够预先处理反驳，并选择更适合的表达路径。

**2. 修辞组件与子论题规划器**

规划器将文章表示为子论题序列，并为每个$t_i$分配$\mathrm{Attr}(t_i)=(c_i,k_i,e_i,r_i)$。其中$c_i$控制主修辞功能，$k_i$是关键主张集合，$e_i$是局部检索证据，$r_i$是用于预先回应的受众反驳；规划还进行自评和必要的迭代修订。

> 直观理解：普通大语言模型往往只会安排主题顺序，ARGUS还要求它明确每一段“用什么方式说服、说什么、拿什么证明、预先回答哪种反对”。因此，文章结构变成可检查和可调整的中间对象。

**3. 迭代精炼器与最佳候选缓冲**

精炼器使用多维度大语言模型评估器产生总体质量判断，并针对最低表现维度生成修改指令；精炼循环保留多个版本中的最高评分候选，以降低局部修改导致质量回退的风险。该模块与前面的ToM引导规划互补，不能简单等同于只对初稿进行自我批评。

> 直观理解：它像针对性编辑器：先诊断文章最薄弱的地方，再只修改相关部分。最佳候选缓冲确保“新版本更改了内容但整体变差”时仍能恢复较好的旧版本。

**训练与推理**

推理时，先向指定骨干模型提供命题、立场和相关上下文，由Input Analyzer决定是否检索并形成结构化输入分析；ToM Reasoner据此产生受众模型，Argument Planner生成带有子论题属性的蓝图，并对蓝图进行最多两轮自评、修改和必要的证据重检索。Argument Writer根据最终计划生成草稿，随后评估器从说服力、连贯性、事实准确性、价值观匹配和修辞平衡等维度评价草稿；低于阈值时按弱项定向修改，并在精炼轮次中保留最高评分版本，输出最终文章。实现使用DeepSeek-V3.2、Qwen3.5-Flash-2026-02-23或GPT-5-mini-2025-08-07作为生成骨干，统一使用GPT-5.4作为评估器；原文未报告针对ARGUS模块进行参数训练或微调。

**复现信息**

为保证公平比较，ARGUS及四个基线使用相同的生成骨干模型；评估器固定为能力更强且独立于生成骨干的GPT-5.4。网络检索使用ddgs获取URL和短片段、trafilatura解析网页，结构化JSON输出最多重试三次并采用指数退避；规划迭代和精炼轮次的最大值均为两轮。实验在Reddit/CMV、iDebate和ExplaGraph三个数据集上进行，每个数据集随机抽取30个输入；这些设置用于复现实验和公平解释结果，但不构成ARGUS的训练过程。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ChangeMyView（CMV）：Reddit 上政治与政策领域的帖子，原帖明确邀请反驳；输入为标题与正文的拼接，目标立场为 refute，用于测试模型针对包含丰富观点和受众信息的文本生成反驳论证。原文未明确报告数据规模、训练/验证/测试划分及具体预处理细节。
- iDebate：来自广泛领域的争议性短命题，目标立场为 refute。由于命题通常较抽象、上下文较少，该数据集主要测试模型在开放式输入下进行世界知识调用、推理和修辞构造的能力。原文未明确报告数据规模、训练/验证/测试划分及具体预处理细节。
- ExplaGraphs：要求模型生成支持给定陈述的论证，高质量输出依赖与辩题相关的背景知识；该数据集主要测试事实导向的知识 grounding、推理连贯性与支持性论证生成。原文未明确报告数据规模、训练/验证/测试划分及具体预处理细节。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**pairwise ELO ranking**

对同一命题下不同模型生成的论证进行两两比较，并据胜负结果累积ELO排名；附录说明每一对样本按$A\rightarrow B$和$B\rightarrow A$两个方向各判断一次，若$w_A-w_B>0.5$则判为胜，若$w_A-w_B<-0.5$则判为负，否则为平局。 （越高越好，因为更高的ELO表示在整体两两偏好比较中更常被评为优质论证。）

</div>
<div class="metric-item" markdown="1">

**absolute LLM-as-judge score**

由GPT-5.4使用Quality Evaluator提示词独立评价每条论证；原文指出其包含说服力、事实准确性和连贯性等维度，用于衡量绝对质量而非只比较两个候选。 （越高越好，表示在相应评价维度上的质量更高；但单一维度得分不必然等同于两两比较中的整体胜出。）

</div>
<div class="metric-item" markdown="1">

**coherence、persuasiveness与factual accuracy维度**

分别考察论证的结构连贯性、说服目标的有效程度和事实是否准确；这些维度用于分析总体优势究竟来自表面流畅、修辞效果还是知识与事实支撑。 （三项均为越高越好；不过原文特别指出不同维度可能与整体两两偏好不完全一致。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨数据集与模型骨干的两两ELO排名

<div class="result-value" markdown="1">

ARGUS在所报告的全部数据集和评价设置中总体优于所有基线；在iDebate上的提升最显著，在CMV上也表现出明显改进，并在ExplaGraphs的所有设置中取得最佳ELO。原文未提供具体ELO数值或差值。

</div>

该结果说明ARGUS的综合论证质量在不同输入形式和目标立场下具有较强稳定性，尤其适合上下文很短、需要补充世界知识并自行组织论证的开放式命题。它支持“统一规划框架有效”这一作者主张，但不能单独证明每个组成模块分别有效，也不能排除评价模型或骨干模型偏好的影响。

<div class="result-source" markdown="1">

来源：第5.1节 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Overall, Argus consistently outperforms all baselines across evaluation settings.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 绝对LLM评价及质量维度

<div class="result-value" markdown="1">

绝对评价总体支持两两ELO结果：ARGUS在几乎所有评价维度上取得最高分，优势尤其集中在说服力和事实准确性；不同方法的连贯性分数普遍较高。原文未提供具体分数或提升幅度。

</div>

这表明ARGUS的主要收益更可能来自更有效的说服策略和更可靠的事实支撑，而不是单纯让文本更流畅。连贯性普遍较高意味着该指标对现代大语言模型的区分度有限，因此不能把ARGUS的优势解释为全面改善所有语言质量维度。

<div class="result-source" markdown="1">

来源：第5.1节 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Argus achieves the highest scores across nearly all evaluation dimensions, particularly in persuasiveness and factual accuracy, where it shows clear and consistent margins over baselines.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 不同基线与数据集的行为差异

<div class="result-value" markdown="1">

Plan&Write被报告为总体最强基线；Self-Refine和Multi-Agent Debate相对落后，并且基线表现会随模型骨干和数据集变化。例如，在GPT-5-mini上的ExplaGraphs绝对评价中，Plan&Write的说服力最高，Self-Refine的事实准确性最高，但ARGUS仍在两两比较中获胜。原文未提供具体分数或ELO数值。

</div>

该结果说明单个评价维度的第一名不一定代表整体论证最佳：整体偏好还可能综合考虑组织、平衡性和修辞有效性。因此，ARGUS的优势应理解为多维质量的综合平衡，而不是在每个孤立指标上都必然第一。该观察也说明仅依靠迭代批评或多代理讨论，可能无法稳定替代显式受众建模和策略规划。

<div class="result-source" markdown="1">

来源：第5.1节 Main Results

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

However, Argus still wins in pairwise comparisons, indicating that isolated rubric dimensions do not fully capture holistic quality.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验章节未报告数据集规模、数据划分、完整模型骨干列表、具体表格数值、置信区间或显著性检验，因此无法据此判断提升幅度、统计稳定性和不同设置之间的可比性。
- 主要评价依赖GPT-5.4进行绝对评分和两两偏好判断；原文未报告人工专家评价、评价者间一致性、提示词敏感性或事实核查流程，因此结果可能受到LLM-as-judge偏差以及ELO评价协议的影响。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Plan&Write：显式先规划、再写作的基线，用于检验ARGUS的提升是否超出一般性规划带来的收益；原文称其为各基线中“consistently the strongest competitor”。
- Self-Refine：通过迭代批评与修改改进初始论证，用于比较针对性自我反馈与ARGUS统一规划框架的差异。
- Multi-Agent Debate：让多个代理进行辩论或协作，用于检验多代理 deliberation 是否足以替代理论心智建模、策略规划和知识支撑。
- 原文未明确报告的直接生成基线：可作为无显式规划或反思机制的参照，但所给章节没有提供其完整方法名称、实现方式或结果细节。

**实验想回答的问题**

- 在$\mathrm{CMV}$、$\mathrm{iDebate}$和$\mathrm{ExplaGraphs}$三类立场、领域与论证风格不同的任务上，ARGUS是否能稳定提升论证生成质量，尤其是说服力、事实准确性与整体偏好排名？
- 相较于直接生成、显式规划、迭代自我批评和多智能体辩论等方法，ARGUS的理论心智引导、策略感知规划与知识 grounding 是否能在开放领域和事实导向场景中带来更好的综合表现？

**实验实现**

两类评价均以模型生成的论证为对象。绝对评价中，每条论证由GPT-5.4独立评分，使用附录C所述的Quality Evaluator提示词。ELO评价按每个命题进行两两比较，每一对候选按两个相反展示顺序各评价一次；胜负阈值为$0.5$，中间区间判为平局。实验覆盖三个数据集，并在多个模型骨干上比较ARGUS与基线。所给章节未明确报告各数据集规模、数据划分、生成参数、随机种子、重复次数、显著性检验或完整表格数值。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文所给章节未提供逐案例的输入、生成论证、人工分析或可核验的定性案例；仅报告了ExplaGraphs在GPT-5-mini下不同基线在说服力和事实准确性上的维度差异，不能将其扩展为完整case study。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The contribution appears to combine theory-of-mind reasoning, strategic planning, and grounded generation for argument construction.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`70569cfe14482cd5758778b1550b298fa4626fa9503b058e25f8eb3c1f0807f1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
