---
title: "[论文解读] OBJECTION! Lawyer Agents Mitigate Guilty Bias in Legal Judgment Prediction"
description: "[arXiv 2609.02158][LLM Agent] 本文将法律判决预测中的“有罪偏差”定位为推理阶段的叙事偏差问题，并提出由对抗式律师智能体逐阶段提出辩护意见的免训练推理流程 OBJECTION。"
arxiv_id: "2609.02158"
announcement_date: "2026-09-03"
primary_category: "llm_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-03T04:30:41.887726+00:00"
source_sha256: "e0c2722e3e4e02b2394efdf76406513e34d34415ba5df1747289d9bedf7440ac"
tags:
  - "LLM Agent"
  - "LLM Reasoning"
  - "法律判决预测"
  - "有罪偏差"
  - "无罪推定"
  - "虚假有罪率"
  - "对抗性律师智能体"
  - "推理时纠偏"
  - "刑事法律推理"
  - "Natural Innocent"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Agent · arXiv 2609.02158</p>

# OBJECTION! Lawyer Agents Mitigate Guilty Bias in Legal Judgment Prediction

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-03</span>
<span><strong>作者</strong> Jaehoon Jeong, Jay-Yoon Lee</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Seoul National University, Seoul, South Korea</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.02158v1) · [PDF 下载](https://arxiv.org/pdf/2609.02158v1) · **关键词** 法律判决预测, 有罪偏差, 无罪推定, 虚假有罪率, 对抗性律师智能体, 推理时纠偏, 刑事法律推理, Natural Innocent<br>


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

本文将法律判决预测中的“有罪偏差”定位为推理阶段的叙事偏差问题，并提出由对抗式律师智能体逐阶段提出辩护意见的免训练推理流程 OBJECTION。

**不用术语来说**：刑事案件文本通常由控方立场组织：它们着重陈述支持定罪的事实，而不是中立地罗列正反证据。模型长期学习这种文本后，容易把控方叙述直接当成完整事实，即使案件实际应判无罪，也可能作出有罪预测。由于误判无辜者的法律与社会代价尤其高，系统不能只追求总体准确率，还必须主动检查文本中被忽略的合理怀疑。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者把有罪偏差明确为法律判决预测中的核心风险，以错误有罪率（False Guilty Rate，FGR）衡量模型将真实无罪案件误判为有罪的倾向，并使用真实无罪案件检验既有系统。
- 作者提出 OBJECTION：无需额外训练，在犯罪成立、违法性与有责性三阶段推理中嵌入对抗式律师智能体，使其依据“存疑时有利于被告”原则主动提出辩护论点，而非仅检查答案的一致性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

法律判决预测（Legal Judgment Prediction, LJP）根据案件事实描述预测裁判结果。本文关注刑事案件中的二元判断，即被告有罪或无罪；关键背景是，模型读取的“事实”通常摘自书面判决，并非中立的事件记录，而是围绕指控组织的检方叙事。同时，现有数据集中的有罪标签占比较高，因此模型容易把起诉文本中的陈述直接当作客观事实，形成系统性的“有罪偏差”。这类偏差尤其表现为把真实无罪案件误判为有罪，违背无罪推定原则，也使只追求总体准确率的评估不足以反映实际法律风险。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**法律判决预测（LJP）**

给定案件事实描述，由模型预测罪名、刑罚或有罪与否等司法结果。本文聚焦有罪与无罪的判断，并考察模型是否因输入叙事和标签分布而偏向有罪。

</div>
<div class="concept-item" markdown="1">

**有罪偏差（Guilty Bias）**

模型在证据不足或存在免责情形时，仍倾向接受检方叙事并输出有罪。其来源包括训练文本的检方视角、数据中的有罪标签失衡，以及推理过程中缺少主动提出辩护意见的机制。

</div>
<div class="concept-item" markdown="1">

**无罪推定与存疑有利被告（In Dubio Pro Reo）**

刑事判断中，被告在依法证明有罪前应被视为无罪；若关键事实仍存在合理怀疑，应作出有利于被告的判断。本文将这一规范转化为推理时的对抗性辩护角色，使系统主动寻找能够阻却定罪的事实与法律理由。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一段来自刑事书面判决的案件事实描述，其语言结构可能天然偏向检方，并可能把指控性陈述包装成已确定事实。系统需要结合犯罪成立的三阶段法律审查——构成要件符合性、违法性与有责性——输出有罪或无罪判断；若在任一阶段发现足以阻却定罪的合理怀疑，例如事实不满足犯罪要件、存在正当防卫等违法阻却事由，或缺乏可归责性，则应停止后续定罪推理并作出无罪判断。本文所处的是无需额外训练的推理时纠偏场景：既有语言模型及其参数保持不变，通过引入职责明确的律师智能体，在每个审查阶段对初始判断提出基于案情的最强辩护。评估不能只看总体正确率，还要重点观察真实无罪案件被误判为有罪的比例，即$\mathrm{FGR}$；同时，降低$\mathrm{FGR}$不能以大幅增加真实有罪案件被误判为无罪的$\mathrm{FNR}$为代价。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathrm{LJP}$**

法律判决预测任务，即依据案件事实文本预测司法判决结果。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{FGR}$**

False Guilty Rate，真实无罪案件中被系统错误预测为有罪的比例；数值越低，说明有罪偏差越弱。

</div>
<div class="notation-item" markdown="1">

**$\mathrm{FNR}$**

False Not-Guilty Rate，真实有罪案件中被系统错误预测为无罪的比例；用于检验纠正有罪偏差是否造成过度宽纵。

</div>

</div>

**直接相关的工作**

- **基于信息抽取、犯罪构成要件模式或多步法律推理的LJP方法（Jiang and Yang, 2023；Deng et al., 2023；Liu et al., 2025；Zhang et al., 2025b）**: 这些方法通过结构化案件信息或显式分解法律推理来提高预测质量，但通常默认输入事实是中立可靠的，因而可能继续继承检方叙事中的有罪倾向。它们构成本文采用三阶段审查结构的基础，同时也是本文试图在推理阶段纠偏的对象。
- **Zhang et al. (2025a) 的合成无罪数据与三分类训练方法**: 该工作率先明确识别LJP中的有罪偏差，并主要通过训练时加入合成无罪样本进行纠正。本文指出，合成样本可能包含可被模型当作捷径的人工线索，使模型过拟合于显式无罪信号，而真实推理时面对检方化叙事仍缺乏主动质疑机制；因此本文转向无需额外训练的推理时对抗性辩护。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

法律判决预测模型的输入与训练语料大量来自书面判决或控方认定的案件事实，这些材料天然以证明犯罪为组织目标；同时，现有数据中的有罪标签占比很高。二者共同使模型形成系统性的有罪倾向。实际部署时，这种倾向会提高无罪案件被错误定罪的风险，既违背无罪推定，也会削弱公众对法律人工智能的信任。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **结构化法律推理**：通过显式犯罪构成要件模式或多阶段推理框架，把判决拆解为若干法律判断步骤，例如依次分析犯罪是否成立、行为是否违法以及行为人是否具有责任能力，从而提高推理的条理性与总体预测表现。
- **基于合成无罪案例的训练期校正**：人工或自动生成无罪样本，并用这些样本训练或微调模型，以缓解原始数据中有罪标签占优的问题，让模型在训练阶段接触更多支持无罪判决的模式。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 结构化推理方法通常默认输入的事实描述是中立、完整的，因此即使推理步骤形式上更严谨，也可能沿用控方叙事中的前提，把隐藏在文本中的偏向逐步传递到最终结论。
- 合成无罪数据可能包含真实案件中不存在的人工线索，模型因而可能学习识别这些表面特征而非掌握实质法律判断，造成过拟合；而且训练期校正不能保证模型在面对新的控方叙事时，会在推理过程中主动寻找合理怀疑。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有研究尚缺少一种无需重新训练、可直接作用于单个案件推理过程的机制：它不仅要按法律结构作答，还要主动质疑控方叙事所隐含的有罪前提，并且需要在真实无罪案件而非主要依赖合成样本的基准上验证其抗偏能力。

</div>
<div markdown="1"><span>核心问题</span>

能否在法律判决预测的推理阶段嵌入承担辩护职责的对抗式律师智能体，使模型逐阶段发现可能推翻定罪的合理怀疑，从而降低错误有罪率，同时保持对有罪与无罪案件的整体判别能力？

</div>
<div markdown="1"><span>作者直觉</span>

普通模型面对一份表述连贯的控方材料时，容易顺着文本完成“为何有罪”的论证；通用批评器也往往只检查前后矛盾。若为系统设置一个职责明确的辩护角色，让其在每个法律判断环节专门追问“哪些要件尚未证明、是否存在正当化理由、被告是否应承担责任”，就相当于在单向控诉之外补入制度化反方观点。这样，最终判断不再只依赖原始叙事的说服力，而要经受针对无罪可能性的实质挑战。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

OBJECTION 是一个仅在推理阶段运行的法律判决预测管线，不改变基础大语言模型的参数。给定检察叙事形式的案件事实 $X_{fact}$，系统先将事实抽取为主体、对象、客观行为及主观心理状态四类结构化信息，再按犯罪论的“犯罪构成—违法性—责任”三阶段顺序进行判断；在每一阶段，Judge 角色先给出初步结论，Adversarial Lawyer Agent 随后主动寻找合理怀疑、正当化事由或责任阻却事由，最后由 Judge 结合辩护意见重新判定。直观而言，系统不是让模型单方面接受控方故事，而是为每次定罪判断加入一个被明确要求“替被告找理由”的律师，并且把律师意见嵌入每个法律推理环节。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 案件事实输入与 SOAM 信息抽取

使用领域提示词 Prompt A 对案件进行零样本 Schema-based Information Extraction，仅在 Offense 阶段将叙事抽象为 SOAM 四元结构：Subject、Object、Actus Reus 和 Mens Rea。该设计不依赖针对每项罪名手工制定的细粒度规则，并将结构化结果作为后续律师定位法律薄弱点的事实锚点。

<div class="method-step__io" markdown="1">

**输入**：原始法律案件叙事 $X_{fact}$，通常包含行为事实、涉案人物、受害对象、结果及可能的主观状态信息。<br>
**输出**：案件的结构化事实表示，包括主体 $S$、对象 $O$、客观行为及其后果 $A$、从语境推断的主观要素 $M$。

</div>

**直观理解**：先把一段杂乱的案情整理成“谁对谁做了什么，以及可能有什么心理状态”。这一步像填写事实表格，便于律师指出具体事实缺口，但结构化本身并不保证结论无偏。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 犯罪论三阶段问题隔离

按有序集合 $T=\{\text{offense},\text{unlawfulness},\text{culpability}\}$ 依次处理三个相互隔离的问题：Offense 判断行为是否满足犯罪构成要件；Unlawfulness 判断是否存在正当防卫等违法性阻却事由；Culpability 判断行为人是否具有可归责性，例如是否存在精神障碍等责任阻却因素。每一阶段均要求在该阶段的法律前提下推理，避免把后阶段因素提前混入当前判断。

<div class="method-step__io" markdown="1">

**输入**：SOAM 结构化事实，以及在后两个阶段可直接访问的原始案件描述 $X_{fact}$。<br>
**输出**：三个阶段的待审判断及其后续修正结果，最终形成可解释的定罪或按具体阶段理由给出的无罪结论。

</div>

**直观理解**：把“是否构成犯罪”“是否违法”“是否应由本人负责”拆成三道门逐一检查。比如检查违法性时，暂时假定犯罪构成已经成立，而不让责任问题扰乱当前问题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 对抗性律师介入

将同一个基础 LLM 通过不同领域提示词实例化为 Judge $\mathcal{M}$ 与 Lawyer $\mathcal{A}$ 两种角色。Lawyer 不仅检查推理形式是否一致，而是被明确要求提出可能的无罪情境和合理怀疑，例如自卫、故意缺失或责任能力不足，并生成辩护论证 $d_k$。

<div class="method-step__io" markdown="1">

**输入**：第 $k$ 个阶段的事实上下文 $X_{fact}$ 及 Judge 的初步判断 $j_k$。<br>
**输出**：与第 $k$ 个阶段对应的主动辩护论证 $d_k$，以及一个以该论证为条件重新评估后的阶段结论。

</div>

**直观理解**：普通批评者只会问“这段推理有没有漏洞”，而这里的律师必须进一步问“有没有一种合理解释能让被告不应被定罪”。因此它会主动寻找控方叙事没有排除的替代解释。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 阶段重判与顺序裁决

Judge 根据初步判断、律师意见和案件事实重新输出阶段结果 $\hat{y}_k$，并按犯罪论层级顺序继续处理；若较高层级阶段未成立，例如 Offense 未被证明，则启动 Early Exit，立即输出无罪而不再评估后续阶段。系统同时保留 Granular Acquittal Labels，以区分因犯罪构成、违法性或责任问题而无罪。

<div class="method-step__io" markdown="1">

**输入**：初步判断 $j_k$、辩护论证 $d_k$、案件事实，以及前一阶段已经确定的结果。<br>
**输出**：最终法律判决预测 $\hat{y}$，以及必要时说明无罪发生于 Offense、Unlawfulness 或 Culpability 阶段的细粒度理由。

</div>

**直观理解**：每一关都要经过“法官初判—律师反驳—法官复核”。如果第一道门就证明不了犯罪构成，就直接判无罪，不再把后面的因素强行带入，从而避免错误逐级累积。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 三阶段对抗性推理管线

$$
\hat{y}=\overrightarrow{\prod_{k\in T}}\Psi_k\left(\mathcal{M},\mathcal{A},X_{fact}\right)
$$

**符号说明**

- $\hat{y}$：系统输出的最终法律判决预测。
- $T=\{\text{offense},\text{unlawfulness},\text{culpability}\}$：三个按固定顺序执行的法律推理阶段。
- $\Psi_k$：第 $k$ 个阶段的顺序决策函数，包含 Lawyer Agent 的对抗性介入。
- $\mathcal{M}$：承担 Judge 角色、生成初判与复判的基础大语言模型。
- $\mathcal{A}$：承担 Lawyer 角色、生成辩护论证的同一基础大语言模型。
- $X_{fact}$：原始案件事实叙事及其可用上下文。
- $\overrightarrow{\prod}$：表示各阶段不是并行执行，而是按照 Offense、Unlawfulness、Culpability 的顺序执行。

<div class="equation-explanation" markdown="1">

**直观理解**：该式表达了系统的整体结构：最终结论不是一次性由模型从事实直接预测，而是三个带有律师干预的法律决策函数依次作用的结果。这样可以把法律程序顺序和早停规则纳入推理过程。<br>
**原文位置**：第 3 节 Methodology，式（1）

</div>

</div>

<div class="equation-block" markdown="1">

#### 单阶段法官—律师—法官交互

$$
j_k=\mathcal{M}(X_{fact}),\quad d_k=\mathcal{A}(j_k,X_{fact}),\quad \hat{y}_k=\mathcal{M}(j_k,d_k,X_{fact})
$$

**符号说明**

- $j_k$：第 $k$ 个法律阶段中 Judge 产生的初步判断。
- $d_k$：Lawyer Agent 针对初步判断和案件事实生成的辩护论证。
- $\hat{y}_k$：Judge 结合辩护论证后的第 $k$ 阶段最终判断。
- $k$：当前法律阶段的索引，取自 $T$。

<div class="equation-explanation" markdown="1">

**直观理解**：该式对应一个明确的三步循环：法官先判断，律师针对这个判断寻找合理怀疑，法官再把律师意见纳入上下文后重判。辩护意见因此不是事后解释，而是直接成为最终阶段结论的输入。<br>
**原文位置**：第 3.3 节 Adversarial Interaction Design，式（2）—（3）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：OBJECTION 本身是 inference-time pipeline，不进行参数更新，因此原文没有为 OBJECTION 定义需要优化的训练损失或目标函数。其改进来自推理时的角色提示、阶段隔离、辩护论证注入和顺序裁决，而非重新训练基础模型。作为比较对象，论文另行对 LJPIV 进行 LoRA 微调；该训练过程属于基线实现，不是 OBJECTION 的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. SOAM Schema-based Information Extraction**

SOAM 将犯罪事实分解为 Subject $S$、Object $O$、Actus Reus $A$ 和 Mens Rea $M$。其中 $A$ 表示客观身体行为及其后果，$M$ 是根据语境推断的主观要素的广义集合；抽取采用零样本提示，不需要针对每项罪名进行专门标注。

> 直观理解：该模块把案情压缩成四种最基本的信息：行为人、行为对象、客观行为和主观心理。它不是直接判罪，而是提供一份更容易审查的事实清单。

**2. Trichotomous Reasoning with Issue Isolation**

系统采用民法法系刑法理论中的三阶段结构 $T$：Offense、Unlawfulness 和 Culpability。每个阶段在相应逻辑前提下独立判断，使正当防卫、精神障碍等因素分别进入违法性或责任分析，而不是在一个混合式二分类提示中同时处理。

> 直观理解：法律上的“有犯罪行为”不等于“违法”，也不等于“本人一定应负责”。将三件事分开检查，可以让最终无罪结论说明究竟是哪一个法律条件没有成立。

**3. Adversarial Lawyer Agent**

Lawyer Agent 与 Judge 使用同一基础 LLM 的不同角色提示词实现。它是管线的绑定机制：在每个阶段读取 Judge 的初判 $j_k$ 和事实 $X_{fact}$，生成辩护意见 $d_k$，再将该意见注入 Judge 的复判上下文；与只验证逻辑一致性的标准 Critic 不同，它承担主动制造合理怀疑和提出免责、阻却或正当化解释的任务。

> 直观理解：该模块的关键不是增加一个泛泛的“自我检查”，而是规定检查方向必须偏向被告利益。它把原本容易接受控方叙事的模型，强制置于一场具有控辩张力的内部法律讨论中。

**训练与推理**

系统部署时加载一个基础 LLM，并通过领域提示词分别赋予 Judge 与 Lawyer 两种角色；同一案件首先经过 SOAM 抽取，随后在三个法律阶段中循环执行初判、辩护和复判。推理阶段使用确定性生成设置，以便比较不同管线；论文未报告 OBJECTION 需要额外的人工辩护标注或专门训练。需要区分的是，实验中的 LJPIV 基线使用 Qwen2.5-7B-Instruct 进行 LoRA 微调，目标模块包括 $q_proj$、$k_proj$、$v_proj$、$o_proj$、gate_proj、up_proj 和 down_proj，LoRA rank 为 8、alpha 为 32、dropout 为 0.1，并使用 AdamW；这些设置只用于复现和比较该训练型基线。

**复现信息**

论文的主要开放权重骨干包括 Qwen2.5-7B-Instruct、Llama-3.1-8B-Instruct 和 Gemma2-9B-it，并额外测试 GPT-4.1-mini 与 Gemini-2.5-Flash 等商业 API，以检查方法是否依赖特定模型。推理采用 vLLM 服务，温度为 0.0，最大生成长度为 2,048 tokens，最大上下文长度为 8,192 tokens，GPU 显存利用率上限为 0.90；模型通常以 bfloat16 加载。论文未说明每个阶段是否使用独立模型参数，方法描述表明 Judge 与 Lawyer 是同一 LLM 通过不同提示词形成的两个角色。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LJPIV-CAIL：基于 CAIL 刑事案件数据集构造的域内基准，包含通过反事实改写生成的合成无罪样本，用于评估方法在已有评测分布上的表现。
- LJPIV-ELAM：基于 ELAM 构造的域外数据集，并采用与 LJPIV-CAIL 相同的样本生成流程，用于测试跨数据域泛化能力。
- Natural Innocent：本文提出的真实无罪数据集，包含来自韩国刑事法院的一审判决，共 $3{,}412$ 个真实案件；其中有罪案件 $1{,}291$ 件，无罪案件 $2{,}121$ 件，并按犯罪构成、违法性阻却和责任阻却三类无罪理由组织，用于更真实地评估 $FGR$ 与 False Not-Guilty Rate（$FNR$）。原文所给选段未明确报告各数据集的训练集、验证集和测试集划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**G-F1 与 NG-F1**

分别是有罪（Guilty）类和无罪（Not-Guilty）类的 F1 分数，综合衡量对应类别的精确率与召回率。 （越高越好；同时观察两者可以避免模型只偏向有罪或只偏向无罪。）

</div>
<div class="metric-item" markdown="1">

**False Guilty Rate（$FGR$）**

无罪案件被预测为有罪的比例，定义为 $FP/(TN+FP)$；它直接衡量违反无罪推定的风险。 （越低越好；数值越高表示模型越容易接受控方叙事并错误定罪。）

</div>
<div class="metric-item" markdown="1">

**False Not-Guilty Rate（$FNR$）**

有罪案件被预测为无罪的比例，定义为 $FN/(TP+FN)$；它衡量错误放过有罪案件的风险。 （越低越好，但应与 $FGR$ 结合解读，因为单独压低其中一种错误率可能造成另一种错误增加。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Natural Innocent 总体结果（Qwen-2.5-7B）

<div class="result-value" markdown="1">

在真实无罪案件上，OBJECTION 将基线 D 的 $FGR$ 从 $84.49\%$ 降至 $16.69\%$；该数据集包含 $2{,}121$ 个无罪案件。原文摘要另报告，SOTA 基线的 $FGR$ 从 $82.93\%$ 降至 $16.69\%$，但选段中的表 15 将总体基线记为 $84.49\%$，两处数值存在差异，应以完整原文表格和实验协议核查。

</div>

这说明律师代理显著减少了模型把真实无罪案件判为有罪的倾向，且测试对象不是带有明显“无罪提示”的人工改写文本。不过，这一结果主要证明降低定罪型错误的能力，不能单独证明模型整体法律判断准确，也不能排除 $FNR$ 或其他错误类型的变化。

<div class="result-source" markdown="1">

来源：Table 15, Appendix H.1；摘要另有相关数值

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

All 2,121 acquittals: 84.49 16.69

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 不同无罪理由的覆盖性（Natural Innocent，Qwen-2.5-7B）

<div class="result-value" markdown="1">

按法院实际采用的无罪理由分组，OBJECTION 将 Offense 类 $FGR$ 从 $85.79\%$ 降至 $17.08\%$，Unlawfulness 类从 $86.31\%$ 降至 $17.40\%$，Culpability 类从 $72.57\%$ 降至 $12.83\%$；总体从 $84.49\%$ 降至 $16.69\%。

</div>

三类阶段均出现大幅下降，尤其说明效果不只依赖提示词中列出的某个具体法律教义；犯罪构成阶段主要涉及证据不足，也能获得改善。但这是按数据集类别的聚合结果，不能说明每一种具体罪名或每一种辩护理由都同样有效。

<div class="result-source" markdown="1">

来源：Table 15, Appendix H.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Offense | 1,464 | 85.79 | 17.08

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 推理效率与 early exit（CAIL，Llama-3.1 与 Qwen-2.5）

<div class="result-value" markdown="1">

OBJECTION 的 early-exit 机制使 Llama-3.1 平均每案调用 $5.57$ 次、延迟 $5.77s$，相对 Debate 基线延迟降低约 $69.1\%$；Qwen-2.5 平均调用 $7.17$ 次、延迟 $6.77s$，相对 Debate 降低约 $57.9\%$。Debate 固定进行 $8.0$ 次交互。

</div>

该结果表明结构化流程不一定比多轮辩论更昂贵，因为模型在较早阶段足以排除指控时可以停止计算。它支持效率—性能折中更优这一作者主张，但选段没有同时给出各方法完整的准确率、token 消耗表和显著性检验，因此不能据此判断总体部署成本一定更低。

<div class="result-source" markdown="1">

来源：Appendix E, Inference Efficiency Analysis；具体数值见 Table 12

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, OBJECTION utilizes an early-exit mechanism, substantially decreasing the expected computational cost based on the verdict distribution:

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- Natural Innocent 虽包含真实判决，但样本来自韩国政府公开的一审刑事判决，并通过关键词筛选和人工核验构造；因此其法律制度、罪名分布和无罪理由分布可能限制对其他国家、审级及案件类型的外推。
- 选段报告了仍有 $404$ 个错误无罪，其中 $370$ 件（$91.6\%$）在 Offense 阶段退出，且部分错误存在推理内容与最终标签不一致；这说明骨干模型的自洽性和早期退出仍是部署风险，不能仅凭 $FGR$ 的下降就认为系统适合完全自动化司法决策。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Plain LLM：标准提示下的直接零样本预测，用于提供不加入结构化推理的基础参照。
- LJPIV：微调得到的当前最优方法，被作者视为域内性能上界，用于比较推理时方法与专门训练方法的差异。
- Self-Refine：不使用法律身份的通用批评器，用于检验仅增加一般性自我批评是否足以缓解有罪偏见。
- Debate-Feedback：通过随机采样进行多轮圆桌式辩论的方法，用于比较结构化律师干预与无结构多智能体辩论的效果。

**实验想回答的问题**

- 在合成无罪样本与真实无罪案件上，OBJECTION 是否能够降低模型把无罪案件判为有罪的错误率，即 False Guilty Rate（$FGR$），并保持合理的有罪与无罪分类性能？
- OBJECTION 中的 SOAM Schema、三步推理结构和 Adversarial Lawyer Agent 是否分别对降低有罪偏见有效，其效果能否推广到提示词中未明确列出的无罪理由？

**实验实现**

推理实验使用 Qwen-2.5-7B-Instruct、Llama-3.1-8B-Instruct 和 Gemma-2-9B-it 作为骨干模型。提示策略依次比较 Schema、三步结构及二者组合；主要方法在犯罪构成（offense）、违法性（unlawfulness）和责任（culpability）三个阶段分别加入主动提出辩护理由的 Adversarial Lawyer Agent。实验还报告三步推理过程的宏平均 Precision、Recall 和 F1。效率实验在单张 NVIDIA RTX PRO 6000 Blackwell GPU 上使用 vLLM，并比较平均延迟和每案 token 消耗；OBJECTION 使用 early exit，使模型在较早阶段作出结论时停止后续调用。原文所给选段未明确报告完整的数据划分、随机种子、重复次数及所有提示模板。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| LJPIV-CAIL 上移除组件（Qwen-2.5） | 完整 OBJECTION 的 G-F1、NG-F1、$FGR$、$FNR$ 分别为 $0.75$、$0.80$、$10.71\%$、$33.93\%$；移除 Schema 后为 $0.68$、$0.76$、$13.21\%$、$42.14\%$；移除 Lawyer Agent 后为 $0.66$、$0.69$、$27.86\%$、$37.14\%$；移除三步结构后为 $0.35$、$0.57$、$31.07\%$、$72.14\%$。 | 移除任一组件都会恶化结果，但移除三步结构造成最大幅度的整体退化，说明按犯罪构成、违法性和责任逐层分析是主要支撑。移除 Lawyer Agent 会使 $FGR$ 从 $10.71\%$ 升至 $27.86\%$，直接证明主动辩护干预对缓解有罪偏见不可或缺；Schema 则提供了较弱但仍有帮助的事实组织作用。 | Table 13, Appendix F<br><span class="experiment-evidence">(-) 3-Step Structure \| 0.35 \| 0.57 \| 31.07 \| 72.14</span> |
| 专门 Lawyer Agent 与普通 Critic 的比较（LJPIV-CAIL，Qwen-2.5） | 使用 Normal Critic 时 G-F1 为 $0.75$、NG-F1 为 $0.59$、$FGR$ 为 $55.71\%$、$FNR$ 为 $5.71\%$；完整 OBJECTION 的对应值为 $0.75$、$0.80$、$10.71\%$、$33.93\%$。 | 普通批评器虽然保持了有罪类 F1，却几乎没有缓解错误定罪，并明显牺牲了无罪类表现；相反，具有法律辩护角色的代理显著降低 $FGR$。这表明关键不是简单增加一次“检查”，而是让检查过程明确寻找有利被告的事实、法律理由和责任缺失。 | Table 13, Appendix F<br><span class="experiment-evidence">Ours w/ Normal Critic \| 0.75 \| 0.59 \| 55.71 \| 5.71</span> |

**定性案例**

- 定性案例描述了一起被害人持刀攻击、被告为等待警方到场而实施约束、被害人在约束过程中死亡的案件。SOAM 抽取将被告作为 Subject、受害人作为 Object，将按压颈部等客观行为归入 Actus Reus，并将多次报警等信息作为 Mens Rea 的证据，解释为限制攻击者而非杀人意图。该案例说明，方法试图把“发生了什么行为”和“行为人具有什么主观状态”分开，再在三步框架中检验防卫、因果关系和责任；但单个案例只能展示推理路径，不能证明整体性能。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出在法律推理各阶段调用对抗性律师代理进行辩护和质疑，核心是基于LLM Agent的推理时协作式干预。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`e0c2722e3e4e02b2394efdf76406513e34d34415ba5df1747289d9bedf7440ac`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
