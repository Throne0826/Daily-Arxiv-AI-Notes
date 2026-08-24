---
title: "[论文解读] Enhancing LLMs in Predictive Political QA with Semi-Structured Data"
description: "[arXiv 2608.21218][LLM Reasoning] 原文未明确报告。"
arxiv_id: "2608.21218"
announcement_date: "2026-08-24"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-24T02:09:22.929444+00:00"
source_sha256: "cda5375b0b4f954a2f92a9caa2757aa3d299152277567573f4b976922432d4d8"
tags:
  - "LLM Reasoning"
  - "预测型政治问答"
  - "大语言模型增强"
  - "半结构化政治数据"
  - "政治人物立场"
  - "高阶结构信号"
  - "人物交互图"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.21218</p>

# Enhancing LLMs in Predictive Political QA with Semi-Structured Data

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-24</span>
<span><strong>作者</strong> Yinan Liu, Zihan Zhou, Zichun Jin, Xinyu Wang, Bin Wang, Xiaochun Yang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Zihan ZhouZichun JinXinyu WangBin WangXiaochun Yang School of Computer Science and Engineering, Northeastern University, Shenyang 110819, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.21218v1) · [PDF 下载](https://arxiv.org/pdf/2608.21218v1) · **关键词** 预测型政治问答, 大语言模型增强, 半结构化政治数据, 政治人物立场, 高阶结构信号, 人物交互图<br>


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

本文位于政治问答与大语言模型外部知识增强的交叉领域，聚焦预测型政治问答（predictive political QA），即根据政治人物的历史行为、立场及其关系网络，推断其尚未发生的未来行为，例如对某议案的投票选择。与可通过检索直接找到答案的事实型问答不同，政治数据通常只记录过去的背景、事件和行为，因此模型需要从间接证据中进行推理。本文所处理的外部资源主要包括社会背景资料、选举记录和立法投票记录；这些资料往往是半结构化的，既保留文本上下文，也保留人物与记录之间的组织关系。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**预测型政治问答**

任务不是查找已经明确记录的事实，而是根据历史证据预测政治人物在未来事件中的行为或态度。外部资料通常不直接包含目标答案，因此模型必须进行间接推断。

</div>
<div class="concept-item" markdown="1">

**半结构化政治数据**

半结构化数据介于自由文本和严格数据库表格之间，例如包含人物、事件、行为及其文本描述的记录。它既能保留细粒度语境，又能支持从共享记录中构造人物之间的关系。

</div>
<div class="concept-item" markdown="1">

**立场信号与高阶结构信号**

立场信号表示人物针对具体议题的主观偏好，可反映价值观、意识形态或党派利益。高阶结构信号表示人物在交互网络中的间接依赖和群体影响，例如通过中间组织或决策者形成的非直接关系。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一个关于政治人物未来行为的预测问题，以及来自公开政治资源的历史记录，系统需要输出该问题的预测答案。记录可能包括人物背景、既往政治行为、议题相关事件和人物之间的共同参与关系；目标行为尚未发生或未被资源直接记录。本文的关键设定是：不能仅依赖事实检索，而要把与问题相关的历史记录转化为适合推理的证据，并同时建模人物对具体议题的立场和政治行为网络中的间接影响。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

预测型政治问答的输入问题，例如询问某政治人物将如何对某项议案投票。

</div>
<div class="notation-item" markdown="1">

**$a$**

待预测行为的政治人物或政治行动者。

</div>
<div class="notation-item" markdown="1">

**$R_a$**

与政治行动者 $a$ 相关的历史政治记录集合，用于构造其人物档案并提取议题相关证据。

</div>
<div class="notation-item" markdown="1">

**$G=(V,E)$**

政治行动者交互图，其中 $V$ 是行动者集合，$E$ 表示由共享记录等关系形成的连接；图结构用于学习直接及间接的群体影响。

</div>

</div>

**直接相关的工作**

- **PAA**: PAA 采用基于人物档案的模拟方法，把政治人物的背景和历史行为组织成文本档案，再提示大语言模型通过角色扮演模拟其决策。它证明外部政治资源能够改善政治推理，但文本档案对人物之间隐含的群体影响建模较弱；本文转而从半结构化记录中提取针对议题的立场信号，并补充网络结构信号。
- **PEG**: PEG 将政治资源转换为知识图谱，检索相关三元组并注入大语言模型。该方法适合提供明确事实，但从原始资源抽取三元组可能丢失细粒度上下文；本文保留半结构化记录的语义信息，同时通过人物交互图表示高阶关系，以适应答案不直接存在的预测型问答。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

预测性政治问答并不是查找已经记录的事实，而是根据政治人物过去的行为、立场及其所处的关系网络，推断其尚未发生的投票或政策反应。现有大型语言模型在专业、长尾政治场景中的知识可能不完整或不可靠，而政治领域虽然拥有选举记录、立法投票记录、法案信息和外交事件等丰富的外部资源，这些资源通常只提供间接证据，不能直接给出未来行为的答案。因此，关键需求是把政治记录转化为适合推理而非仅适合检索的证据。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于政治人物画像的模拟方法（PAA）**：该方法把政治人物的背景资料和历史行为整理成文本画像，再通过角色扮演提示大型语言模型，模拟该人物在目标问题上的决策。它能够利用人物经历和过去行为帮助模型进行政治推理。
- **基于知识图谱的证据注入方法（PEG）**：该方法把外部政治资源转换为知识图谱，并检索与问题相关的结构化事实或关系，再将这些证据注入大型语言模型。它强调从结构化关系中寻找与问题相关的政治知识。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 两类方法主要把外部资源当作知识性证据，未充分提取政治人物针对具体议题的主观立场。其后果是模型能够看到历史事实，却未必能明确判断人物在目标议题上的偏好，而这种偏好往往是预测未来行为的直接依据。
- 基于画像的方法难以表达政治人物之间通过组织、党派或中介决策者形成的高阶间接影响；基于知识图谱的方法则常把复杂记录压缩为三元组，容易丢失细粒度语境。前者会遗漏群体层面的行为依赖，后者可能造成证据过于简化，二者都不足以完整表示预测所需的关系结构。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究尚缺少一种面向预测推理的证据表示，能够同时保留半结构化政治记录的语境细节，提取人物在具体议题上的立场，并建模政治人物交互网络中的高阶结构信号。换言之，现有方法尚未有效结合语义层面的个体偏好与向量层面的群体影响。

</div>
<div markdown="1"><span>核心问题</span>

如何利用半结构化政治记录，同时提取与问题相关的政治人物立场和政治人物之间的高阶关系结构，并将这两类互补信号转化为大型语言模型可以有效使用的证据，从而提升其对未来政治行为的预测能力？

</div>
<div markdown="1"><span>作者直觉</span>

同一政治人物过去对相关议题的行为可以揭示其具体立场，而与其共享投票、法案或其他政治记录的群体关系，则可能揭示直接记录中没有明确写出的间接影响。将前者以保留语境的语义证据呈现，将后者以图结构学习得到的表示呈现，能够让模型既回答“这个人倾向于什么”，又利用“这个人处在怎样的政治关系网络中”。两种信号分别补足个体偏好和群体依赖，因此联合使用可能比单纯检索事实或生成文本画像更适合预测尚未发生的政治行为。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PSL（Predictive Stance and high-order structure Learning）面向预测性政治问答，将半结构化政治记录转化为两类可供大语言模型使用的证据：语义视图中的问题相关行为立场，以及向量视图中的政治行动者高阶结构表示。整体流程是：从立法和外交记录构造行动者行为档案；依据问题分解结果进行分层检索；由小型语言模型提炼与问题相关的立场文本；在行动者—记录交互图上传播表示并通过行动者—问题焦点协同嵌入进行问题条件化；最后把原问题、立场和协同向量注入提示模板，由经过 LoRA 微调的大语言模型生成答案。直观地说，PSL 不仅询问“这个行动者过去说过或做过什么”，还进一步估计“与其他行动者和共同事件形成的关系结构，是否能帮助判断其在当前问题上的行为”。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造政治行为档案

将原始数据按政治行动者 $p\in P$ 重组为 JSON 格式的半结构化档案 $file(p)$；每条记录 $r_p$ 包含多个键值属性。立法记录保留法案标题、描述和投票结果，外交记录保留行动类型与参与方，并用摘要模型压缩法案描述。

<div class="method-step__io" markdown="1">

**输入**：立法记录、法案描述、议员投票记录，以及与美国政治相关的外交互动记录。<br>
**输出**：行动者集合 $P$ 及其档案集合 $file(P)$，其中每个档案包含可按属性检索的政治行为记录。

</div>

**直观理解**：这一步类似为每位政治人物建立一份结构化但不失细节的履历。与只保留知识图谱三元组相比，档案仍能保留“何时、针对什么议题、采取何种行为”等上下文。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 问题分解与阶梯检索

先由 LLM 将问题分解为主要行动者 $p^{*}$ 与问题焦点 $q^{*}$，再将其匹配到档案中的行动者 $p_s$。检索从 $R^{(0)}=file(p_s)$ 开始，在第 $i$ 轮依据 $q^{*}$ 与记录第 $i$ 个属性的语义相似度选出 $k_i$ 条记录，迭代得到最终集合 $R^{(n)}$。

<div class="method-step__io" markdown="1">

**输入**：预测问题 $q$ 和目标行动者档案 $file(P)$。<br>
**输出**：与当前预测问题最相关的记录集合 $R^{(n)}$。

</div>

**直观理解**：普通向量检索可能把一条记录的不同字段混在一起而引入噪声；阶梯检索像先按法案主题筛选，再按描述或行为字段逐层缩小范围，因此更适合具有多字段的政治记录。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 立场证据提炼

使用教师大模型从相关记录中抽取能够反映行动者议题偏好的信息，构造任务特定的蒸馏数据；随后训练小型语言模型（SLM），使其通过交叉熵学习教师生成的词元输出。推理时将 $R^{(n)}$ 与 $q$ 输入 SLM，得到问题相关立场文本 $\mathcal{S}$。

<div class="method-step__io" markdown="1">

**输入**：问题 $q$ 与检索记录 $R^{(n)}$。<br>
**输出**：自然语言形式的行动者立场证据 $\mathcal{S}$。

</div>

**直观理解**：原始投票或外交事件通常不会直接写出答案；该模块把多个事实概括为“行动者在这一议题上倾向于什么”的短文本，减少大模型自行从杂乱事实中推断的负担。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 交互图表示与协同嵌入

构造二部行动者—记录图 $\mathcal{G}_{I}$：节点包括行动者和记录，边表示行动者参与该记录；投票“Yea”的边权为 $1$，其他投票为 $-1$，外交互动边权为 $1$。在图上进行加权邻居传播，拼接行动者初始表示与第 $l$ 层表示得到 $\hat{\mathbf{e}}_p$，再将其与问题焦点表示输入 MLP，得到协同表示 $\hat{\mathbf{e}}_{p_s}^{*}$ 和 $\hat{\mathbf{e}}_{q^{*}}^{*}$。

<div class="method-step__io" markdown="1">

**输入**：行动者档案、记录文本嵌入，以及问题焦点 $q^{*}$。<br>
**输出**：包含高阶关系信息且依赖当前问题的行动者和问题焦点协同向量。

</div>

**直观理解**：共享记录会把不同政治行动者连接起来，因此即使某人没有直接回答当前问题，其与相关人物或事件的间接关系也可能提供线索。协同嵌入进一步过滤与当前问题无关的邻居，避免把整个关系网络的噪声都交给 LLM。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 阶梯检索更新

$$
R^{(i)}=LR(R^{(i-1)},q^{*},k_i)
$$

**符号说明**

- $R^{(i)}$：第 $i$ 轮检索后保留的记录集合。
- $LR$：阶梯检索函数，根据问题焦点与指定属性的语义相似度选择记录。
- $R^{(i-1)}$：上一轮得到的候选记录集合；初始化时为 $R^{(0)}=file(p_s)$。
- $q^{*}$：从原问题中分解出的、表达预测所需核心语义的问题焦点。
- $k_i$：第 $i$ 轮选择的记录数量。

<div class="equation-explanation" markdown="1">

**直观理解**：该式表示检索不是一次性在所有字段上计算相似度，而是从目标行动者的完整档案开始，逐轮按照不同属性筛选。经过 $n$ 轮后得到 $R^{(n)}$，即用于立场提炼的最终相关记录。<br>
**原文位置**：式（1），第 2.1 节 Ladder Retrieval

</div>

</div>

<div class="equation-block" markdown="1">

#### MLP 的贝叶斯个性化排序目标

$$
\mathcal{L}=-\sum_{p\in P}\sum_{r^{+}\in\mathcal{N}_{p}^{+}}\sum_{r^{-}\in\mathcal{N}_{p}^{-}}\ln\sigma\left(y_{pr^{+}}-y_{pr^{-}}\right)+\lambda\left\|\Theta\right\|^{2},\qquad y_{pr}=\left(\hat{\mathbf{e}}_{p}^{*}\right)^{T}\hat{\mathbf{e}}_{r}^{*}
$$

**符号说明**

- $\mathcal{L}$：MLP 的训练损失。
- $P$：政治行动者集合。
- $\mathcal{N}_{p}^{+}$：行动者 $p$ 的正记录集合，即观察到的正向关系记录。
- $\mathcal{N}_{p}^{-}$：行动者 $p$ 的负记录集合，包括明确的负向投票记录和未观察到的外交记录。
- $y_{pr}$：协同后的行动者表示与记录表示的内积得分。
- $\sigma$：Sigmoid 函数，将正负记录得分差转换为排序偏好的概率形式。
- $\lambda$：L2 正则化强度。
- $\Theta$：MLP 的可训练参数。
- $\hat{\mathbf{e}}_{p}^{*},\hat{\mathbf{e}}_{r}^{*}$：经 MLP 协同映射后的行动者和记录向量。

<div class="equation-explanation" markdown="1">

**直观理解**：优化目标不要求模型精确回归一个数值，而要求对同一行动者而言，真实观察到的正记录得分高于负记录。正负样本之间的排序差越大，损失越小；L2 项用于抑制 MLP 参数过度变大。<br>
**原文位置**：式（7），第 2.4 节 MLP Training

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：PSL 包含三个相互衔接的训练环节。第一，立场 SLM 通过任务特定知识蒸馏学习教师 LLM 对 $R^{(n)}$ 和 $q$ 的立场输出，文中说明其使用学生与教师词元输出 logits 之间的交叉熵损失，但未给出完整公式。第二，协同嵌入 MLP 使用式（7）的贝叶斯个性化排序损失，使正记录相对于负记录获得更高内积得分，并加入 L2 正则化。第三，从行动者—记录向量对生成关系分类式指令样本，用 LoRA 对最终 LLM 进行轻量微调，使其学会在提示中使用协同向量；文中未明确报告该 LoRA 阶段的独立损失公式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 阶梯检索与立场蒸馏**

问题被分解为 $p^{*}$ 和 $q^{*}$ 后，检索函数按属性逐轮更新记录集合 $R^{(i)}$。教师 LLM 根据这些记录生成立场监督信号，再以相同输入训练 SLM，使推理阶段以较低成本输出 $\mathcal{S}$。

> 直观理解：模块先精确找到与问题最相关的行为，再把行为事实翻译成议题偏好。这样做的核心不是增加更多外部知识，而是把已有记录改造成更直接服务于预测的证据。

**2. 行动者—记录图传播**

图 $\mathcal{G}_{I}=\{(p,e_{pr},r)\}\subseteq P\times E\times R$ 是二部图；记录节点使用冻结预训练嵌入初始化，行动者和记录通过带对称度归一化的加权和进行多层传播。最终行动者表示为 $\hat{\mathbf{e}}_p=\mathbf{e}_p^{(0)}||\mathbf{e}_p^{(l)}$，同时保留局部初始信息和高阶传播信息。

> 直观理解：图传播相当于让行动者从共同参与的事件中互相“传递信息”。保留第一层和最后一层，既避免丢失行动者自身的直接行为，也让模型看到更远距离的结构联系。

**3. 行动者—问题协同嵌入与混合提示**

由于 $\hat{\mathbf{e}}_{p_s}$ 的维度是问题焦点嵌入 $\mathbf{e}_{q^{*}}$ 的两倍，先构造 $\hat{\mathbf{e}}_{q^{*}}=\mathbf{e}_{q^{*}}||\mathbf{e}_{q^{*}}$，再由训练好的 MLP 分别映射二者为协同向量。训练后的向量与 $\mathcal{S}$ 一起填充 $T(q,\mathcal{S},\hat{\mathbf{e}}_{p_s}^{*},\hat{\mathbf{e}}_{q^{*}}^{*})$，供 LoRA 微调后的 LLM 使用。

> 直观理解：行动者的结构特征并非对所有问题都同样有用；协同模块让它与当前问题配对，突出有用关系并抑制无关关系。混合提示则把这种数值关系转换成 LLM 能够参与推理的输入。

**训练与推理**

训练时，先由政治行为档案构造记录和行动者—记录图。立场蒸馏阶段把档案记录转换为问题，经过阶梯检索得到 $R^{(n)}$，由教师模型生成监督输出并训练 SLM；图表示阶段以冻结预训练模型生成记录初始嵌入，按式（3）传播 $l$ 层，得到 $\hat{\mathbf{e}}_p$，再用档案中的正负记录训练 MLP。随后随机抽取 800 对行动者和记录向量，经 MLP 生成协同向量，并把向量连接后的输入与关系标签组成指令样本，用 LoRA 微调 LLM。

推理时，输入新问题 $q$，先由 LLM 得到 $(p^{*},q^{*})$，匹配目标行动者 $p_s$ 并从 $file(p_s)$ 进行 $n$ 轮阶梯检索；SLM 将 $q$ 与 $R^{(n)}$ 转换为立场 $\mathcal{S}$。同时，使用预先计算的行动者结构表示和当前问题焦点嵌入，经过维度对齐与 MLP 得到 $\hat{\mathbf{e}}_{p_s}^{*}$、$\hat{\mathbf{e}}_{q^{*}}^{*}$，再将四类信息填入模板 $T$，由 LoRA 微调后的 LLM 输出 $Answer$。

**复现信息**

为公平理解方法，关键可复现信息包括：立法数据来自 LegiScan API，外交数据来自涉及政治行动者的互动记录；记录节点嵌入由冻结的预训练嵌入模型初始化。MLP 训练数据先从每位行动者的正记录与随机负记录配对，原始样本超过 900,000 条，再随机抽取 500,000 条，以随机种子 42 按 70%/15%/15% 划分训练、验证和测试集；批大小为 40,960，最多训练 100 个 epoch，学习率为 0.0005，优化器为 Adam，L2 正则化系数为 $10^{-4}$，早停耐心为 10。文中还报告 MLP 使用 AUC 评估，但所给章节未提供具体 AUC 数值。

最终推理依赖三类预处理或学习结果：政治行为档案及其阶梯检索器、图传播得到的行动者表示、以及训练好的 SLM、MLP 和 LoRA-LLM。所给材料未明确报告阶梯检索的具体 $n$ 与各轮 $k_i$、记录嵌入模型名称、SLM 和教师模型的具体型号、LoRA 超参数，以及提示模板的完整内容，因此不能据此补全这些实现细节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- RCVP：政治行动者点名表决预测数据集，属于二分类任务；原文未明确报告样本规模、训练/验证/测试划分及具体时间范围，用于检验立场和群体结构对投票行为预测的作用。
- ICEWS：国际事件与外交行为相关的政治预测数据集，属于多项选择任务；原文未明确报告样本规模和数据划分，用于检验方法在外交或国际政治预测中的适用性。
- StaId：政治立场识别或相关政治状态预测数据集，属于二分类任务；原文未明确报告样本规模和数据划分，用于检验方法在声明资料可能不完整时的稳健性。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**宏平均 F1（macro F1）**

分别计算各类别的精确率与召回率并取平均，综合衡量二分类预测对不同类别的识别能力，尤其避免多数类主导总体评价。 （越高越好，表示预测标签与真实标签更一致且类别间表现更均衡。）

</div>
<div class="metric-item" markdown="1">

**准确率（accuracy）**

多项选择任务中预测正确的答案数占全部样本数的比例。 （越高越好，表示正确选择的样本比例更高；但它不能单独揭示不同选项之间是否存在类别不均衡。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 跨三个数据集和多个骨干大语言模型的总体比较

<div class="result-value" markdown="1">

作者报告 PSL 在三个数据集及不同骨干模型上均优于所比较的基线，说明将半结构化政治记录转化为面向推理的证据，能够稳定改善政治预测问答。

</div>

这一结果支持 PSL 的总体有效性，但不能单独区分提升究竟来自行动者立场、高阶结构、检索策略还是模型蒸馏；也不能证明它在未报告的数据集或其他任务上必然同样有效。

<div class="result-source" markdown="1">

来源：第 3.2 节 Effectiveness Study，Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

From the results shown in Table 1, we can see that PSL outperforms all baselines on three datasets with different LLMs.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 与不同外部知识增强范式的比较

<div class="result-value" markdown="1">

无外部知识生成的方法通常不能稳定超过 Vanilla；文档增强方法主要在 RCVP 上有效，而在 ICEWS 和 StaId 上受到检索不准及直接文本注入噪声的影响。知识图谱增强方法整体更稳定，但依赖实体路径的方法在面向未来的预测场景中较弱。

</div>

该结果表明政治预测需要的不只是更多文本或一般知识，而是与问题相关的行动者立场及可用于推断间接关系的结构信息。它并不意味着文档检索或知识图谱在所有政治任务中都无效，因为其表现会随数据集和表示形式变化。

<div class="result-source" markdown="1">

来源：第 3.2 节 Effectiveness Study

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Document-enhanced methods perform well only over RCVP, with limited effectiveness elsewhere, due to challenges in accurately retrieving relevant information and the interference caused by direct text injection in complex reasoning over ICEWS and StaId.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 与内容相近的政治行动者模拟方法及政治知识摘要方法比较

<div class="result-value" markdown="1">

PSL 在所有报告的比较设置中持续优于 PAA 和 PEG。作者将这一差异归因于 PSL 能够从半结构化数据中挖掘政治知识，并将其加工成更适合预测推理的证据，而不是直接把记录作为背景材料或仅进行知识摘要。

</div>

这说明证据的组织方式可能比证据数量更重要：PSL 试图把孤立记录转化为立场和关系信号。不过，PEG 的核心实现未公开，本文使用其原论文报告的性能，因此该比较的可复现性和严格公平性受到限制。

<div class="result-source" markdown="1">

来源：第 3.2 节 Effectiveness Study

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Although both PEG and PAA are designed to enhance LLMs in political tasks using external knowledge similar in content to that employed by PSL, PSL consistently outperforms them in all experimental setups, which may be attributed to the fact that PSL can mine political knowledge from semi-structured data to enhance the LLM.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 数据集规模、具体训练/验证/测试划分、重复运行方差和显著性检验原文未明确报告；因此难以判断不同方法之间的优势是否具有统计稳定性，也限制了结果复核。
- PEG 的核心实现未公开，本文采用原论文报告的性能；此外，主实验只覆盖给定的三个数据集和四类骨干模型，PSL 对其他政治制度、语言、时间范围及分布变化的泛化能力仍未被充分检验。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Vanilla：仅将问题输入大语言模型，不提供外部知识；它测量骨干模型本身的预测能力，是判断所有增强方法是否真正有益的基本参照。
- KAPING：从政治知识图谱中按语义相似度检索知识，并以三元组形式注入提示；它代表结构化知识图谱增强方法，可检验 PSL 是否不仅依赖一般事实检索。
- PAA：使用政治行动者档案引导大语言模型模拟立法行为；它与 PSL 使用内容相近的行动者记录，是检验“直接模拟行动者”与“显式抽取立场及结构信号”差异的关键比较。
- PEG：检索政治三元组并由大语言模型进行摘要或聚类摘要后再生成答案；它代表经过压缩和组织的知识图谱增强方法。由于核心实现未公开，文中采用原论文报告的性能进行比较。

**实验想回答的问题**

- 在不同政治预测场景、任务形式和骨干大语言模型上，PSL 是否比无外部知识、文档增强、知识图谱增强及政治行动者模拟等方法更有效？
- 行动者立场信号与高阶结构信号是否分别提供独立且互补的预测信息，且其获取方式和表示形式是否影响性能？

**实验实现**

实验使用 Llama-3.1-8B-Instruct、Mistral-7B-Instruct、Deepseek-7B-Chat 和 GPT-3.5-Turbo 作为骨干模型；蒸馏阶段使用 Flan-T5-Small 作为学生模型、GPT-4o-mini 作为教师模型。默认设置中，阶梯检索迭代次数为 $3$，候选记录数为 $5$，图传播层数为 $2$。用于训练多层感知机的资料全部来自行动者档案，网络结构为 $1536\rightarrow1024\rightarrow512\rightarrow256\rightarrow64\rightarrow32$，正则化系数为 $1\times10^{-4}$。作者还使用 $800$ 个样本对 Llama 进行 $3$ 个 epoch 的微调；LoRA 设置包括学习率 $5\times10^{-5}$、验证集比例 $0.1$、有效批大小 $32$ 和最大序列长度 $2048$。评估时，模型被要求从提示中的多个选项中输出选择；若输出没有显式写出选项，使用正则表达式匹配答案。文中将档案中的每条记录视为独立文档供 LangChain 和 InstructRAG 使用，并统一使用 MVPKG 作为知识图谱增强方法的外部知识源；PAA 按原方法为每个行动者抽取 $20$ 条记录。数据集规模、标准划分以及多次运行的方差原文未明确报告。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除行动者立场获取（w/o Actor Stance Acquisition） | RCVP、ICEWS、StaId 的宏平均 F1 分别为 $46.15$、$39.07$、$46.17$，相较完整 PSL 的 $55.92$、$57.81$、$48.50$ 均下降。 | 该消融隔离了立场获取模块，保留其他方法组件。三个数据集都下降，说明问题相关行动者记录经过立场推断后确实包含预测所需的议题偏好；但这仍是组件级相关证据，不能证明立场推断的每一个内部步骤都分别必要。 | Table 3: The results of ablation study for PSL<br><span class="experiment-evidence">w/o Actor Stance Acquisition \| 46.15 \| 39.07 \| 46.17</span> |
| 移除高阶结构信号获取（w/o High-Order Structure Signals Acquisition） | RCVP、ICEWS、StaId 的宏平均 F1 分别为 $39.35$、$49.02$、$46.35$，相较完整 PSL 的 $55.92$、$57.81$、$48.50$ 均下降；其中 RCVP 的下降最明显。 | 该消融取消协作嵌入，使模型只能使用立场和问题文本，从而检验行动者之间的间接依赖是否有用。结果支持高阶结构信号具有独立贡献，尤其适合表达投票或外交行为中的群体依赖；不同数据集降幅不同，说明结构信息的价值取决于任务场景。 | Table 3: The results of ablation study for PSL<br><span class="experiment-evidence">w/o High-Order Structure Signals Acquisition \| 39.35 \| 49.02 \| 46.35</span> |

**定性案例**

- 原文未提供具体的定性案例、问题实例或逐步预测示例，因此无法据此分析 PSL 在单个政治问题上的证据使用过程。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出将政治立场和高阶交互结构转化为推理证据以增强LLM预测性问答，核心贡献是面向预测任务的LLM推理增强。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`cda5375b0b4f954a2f92a9caa2757aa3d299152277567573f4b976922432d4d8`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
