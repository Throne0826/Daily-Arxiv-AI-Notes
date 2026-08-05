---
title: "[论文解读] DiagLoop: A Counterfactual Data Flywheel with Stage-Localized Reinforcement for Diagnostic LLMs"
description: "[arXiv 2608.03674][LLM Reasoning] DiagLoop旨在把一次编写的物理关系或临床指南转化为经过机制校验的反事实训练场景，并依据模型最早出错的诊断阶段定向生成数据和实施局部强化学习，从而训练可本地部署、推理路径可核查的诊断大模型。"
arxiv_id: "2608.03674"
announcement_date: "2026-08-05"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:38:28.002802+00:00"
source_sha256: "7562eb2197f10f754b94d7e8a78d7dbc85c0307857ce597cb8266af9fe44d29a"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "诊断大语言模型"
  - "反事实数据生成"
  - "因果推理"
  - "可验证合成数据"
  - "过程监督"
  - "本地部署"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.03674</p>

# DiagLoop: A Counterfactual Data Flywheel with Stage-Localized Reinforcement for Diagnostic LLMs

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Jian Zhang, Bingyi Wang, Yizhi Liu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Zhejiang University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03674v1) · [PDF 下载](https://arxiv.org/pdf/2608.03674v1) · **关键词** 诊断大语言模型, 反事实数据生成, 因果推理, 可验证合成数据, 过程监督, 本地部署<br>


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

DiagLoop旨在把一次编写的物理关系或临床指南转化为经过机制校验的反事实训练场景，并依据模型最早出错的诊断阶段定向生成数据和实施局部强化学习，从而训练可本地部署、推理路径可核查的诊断大模型。

**不用术语来说**：诊断模型不能只猜对故障或疾病名称，还必须说明观察到的现象如何一步步指向该结论，因为错误理由可能导致错误维修或治疗。然而，严重病例少见且难以安全采集，现有记录通常只有最终结论而没有专家推理过程，不同设备配置或患者群体的数据也难以直接迁移。因此，研究需要在缺少逐病例专家标注的情况下，构造可信的训练案例，并让模型针对自己真正薄弱的推理环节持续改进。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出反事实数据飞轮：由训练期教师改变原因、条件和观测来生成候选世界，再由独立的混合检查器依据编码后的物理机制或临床指南验证场景及推理路径；由此可在不依赖逐病例专家推理标注的情况下，获得覆盖机制内多种配置与对照情形的训练监督。
- 提出因果弱点驱动的训练闭环：用症状抽象、因果链构建和根因归因三阶段标准定位最早失败，通过受限修复测试错误是否向下游传播，再据此路由后续数据生成与阶段局部强化学习；同时以回放、能力保持轨迹和参考模型约束降低已掌握能力的遗忘。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型辅助诊断与可验证合成数据的交叉领域，覆盖工业故障诊断和临床诊断。两类任务都要求模型从观测证据推断隐藏原因，但诊断结果会直接影响维修或治疗，因此仅预测正确标签并不充分，模型还需给出可核查的推理路径。实际训练受到三类数据约束：严重故障或病例稀少且难以安全采集，隐私及网络隔离限制数据共享，不同设备配置或患者群体之间又存在分布差异；同时，多数记录只有最终结论，没有从症状到原因的中间推理。论文据此将物理关系、工程规则或临床指南视为比单一档案中的表面统计模式更稳定的知识来源，用它们构造并检查训练场景，目标是训练可在本地部署、能够沿因果链解释结论的开放大模型。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**反事实推理**

反事实推理通过有控制地改变原因、条件或观测，比较“如果情况不同会发生什么”。在本文中，它用于生成仅在某个故障、疾病或环境条件上不同的场景，迫使模型依据稳定机制而非数据中的偶然相关性作出诊断。

</div>
<div class="concept-item" markdown="1">

**过程监督**

过程监督不只检查最终答案，还检查推理过程中的中间步骤。本文把诊断路径划分为症状抽象、因果链构建和根因归因三个阶段，以定位最早出现错误的位置。

</div>
<div class="concept-item" markdown="1">

**可验证合成数据**

可验证合成数据是由模型或规则生成、并通过独立标准检查有效性的训练样本。本文强调生成器不能自行认证输出，而应由独立的混合检查器依据已编码的物理关系或临床指南判断场景及推理链是否成立。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务输入包括某一机制家族的已编码领域规范，以及描述设备状态或患者表现的诊断场景；领域规范可以是物理关系、工程规则或临床指南，并按机制家族编写，而非为每个病例单独标注推理。学生模型需要依次完成症状抽象、因果链构建和根因归因，输出隐藏故障或疾病及其可检查的推理路径。训练环境假设真实严重案例、跨机构数据和病例级专家推理标注均有限，但存在可形式化的领域规则；训练阶段允许教师模型提出反事实世界，并由与提出者分离的检查机制决定是否接纳。部署阶段只保留学生模型及输出格式，不依赖训练教师或检查器。论文关注的是严格路径正确性，即不仅要求最终根因正确，还要求证据到结论之间的诊断链条正确。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **LLM生成训练数据与错误驱动的数据飞轮**: 既有方法可生成指令、推理文本和逐渐变难的任务，也可围绕失败任务继续扩充数据；但其过滤通常依赖答案一致性、模型共识、结果正确性或任务级评分。论文指出，这些判断仍可能复制生成模型的因果错误，无法保证场景与物理或临床机制一致，因此留下“验证缺口”。
- **过程奖励、课程学习与回放或权重正则化**: 过程奖励能够评价中间步骤，课程学习能够调整已有样本顺序，回放和权重正则化能够缓解遗忘；然而这些技术通常没有把“最早失败阶段”直接连接到下一轮定向数据生成，也未联合解决共享参数更新对已掌握阶段的破坏。本文将前者概括为“归因缺口”，将后者概括为“巩固缺口”。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

工业故障与临床诊断都会直接触发维修或治疗决策，因而要求模型给出可核查的因果推理路径，而不只是正确标签；敏感数据、网络隔离和时延要求又推动模型在本地部署。现实中，严重故障可能破坏记录数据流且不能人为诱发，临床数据受隐私与共享限制，档案还常绑定特定设备或人群并缺少中间推理，使本地模型难以获得兼具真实性、迁移性和过程监督的训练数据。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **记录分布附近的数据增强与课程训练**：GAN等方法围绕已有样本分布生成更多数据，课程学习则重新安排既有样本的训练顺序，让模型由易到难学习。它们主要提高样本数量或调整训练次序，并不直接构造由机制控制、只改变某个原因或条件的诊断世界。
- **LLM合成数据、结果过滤与过程监督**：生成模型自动撰写指令、推理链或更困难的任务，再通过答案一致性、多模型共识、最终结果正确性或任务级规则筛选；过程监督进一步评价中间步骤，错误驱动生成则根据失败任务补充新样本。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 生成模型可能制造违反物理关系或临床指南的场景，例如遗漏确诊所需证据，或让多个相似根因同时成立；而答案一致性、共识和任务级评分仍主要依赖模型判断，可能复现同类因果错误，使不可信场景进入训练，这形成作者所称的“验证缺口”。
- 最终对错无法说明链式诊断中最早损坏的是症状抽象、因果链还是根因归因；过程评分通常止于评价，课程学习只重排已有数据，错误驱动生成也多停留在任务层面。于是系统既不能把弱点准确转化为定向新数据，又可能因共享参数更新而损害已经掌握的阶段，分别形成“归因缺口”和“巩固缺口”。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有方法缺少一个统一闭环：它既要依据领域机制而非生成者自评来验证合成场景，又要把模型轨迹中的最早阶段性失败转化为下一轮反事实数据生成目标和训练信号，并在定向更新时保护已有能力。尤其缺少可被一致复用的阶段标准，使数据准入、错误归因、奖励计算和再生成都服从同一诊断语义，同时保持检查过程与候选生成过程相互独立。

</div>
<div markdown="1"><span>核心问题</span>

在只有编码后的物理关系或临床指南、没有逐病例专家推理标注的条件下，能否构建一个训练期闭环，持续生成机制一致的反事实诊断场景，定位模型最早失败的推理阶段，并仅针对该处及其后续输出进行强化更新，从而提高完整诊断路径的正确性且减少遗忘？

</div>
<div markdown="1"><span>作者直觉</span>

专家面对陌生设备或患者时，依靠的通常不是记住某条历史记录，而是判断“若某个原因成立，应出现哪些表现；若条件或原因改变，哪些观察应随之变化”。因此，以稳定的机制关系生成受控反事实世界，可以迫使模型区分表面相似但因果不同的案例。进一步地，像排查流水线一样先找到最早出错的阶段，再临时修复该处并观察模型能否完成后续步骤，就能区分局部知识缺失与连锁失败；据此定向造题和更新，比对整个错误答案笼统训练更可能把学习信号送到真正薄弱的位置。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

DiagLoop把领域中已有的物理关系或临床指南编码为世界规格，并围绕固定病因生成反事实诊断场景。训练时，教师模型已知目标病因，只负责构造该病因在特定上下文中的观测及参考推理链；与教师提议过程相分离的混合检查器依据统一的阶段准则筛除无效场景。学生只接收观测$x_\omega$，依次输出症状抽象、因果链和根因归因三个阶段。检查器定位学生最早失败的阶段，对非末端失败提供受约束的局部修复，再从修复边界训练学生生成后续阶段；各阶段及变换类型的失败统计又决定下一轮重点生成什么数据，形成“生成—诊断弱点—局部更新—再生成”的闭环。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 编码世界规格并定义反事实空间

作者将组件、拓扑、可观测字段、运行逻辑及“条件到表现”的关系写入世界规格$\mathcal{W}$；随后对基础世界$\omega_0(f,c)$组合至多$K$个算子，改变病因、上下文或观测的可见性、混杂信息与缺失情况。

<div class="method-step__io" markdown="1">

**输入**：某一机制族的条件集合$\mathcal{F}$、上下文集合$\mathcal{C}$、物理约束或临床指南关系$\mathcal{R}_f$，以及有界变换算子集合$\mathcal{V}$。<br>
**输出**：候选反事实世界空间$\Omega_K$及其中的候选世界$\omega=(f,c,x_\omega)$。

</div>

**直观理解**：这一步相当于先写好一套可执行的领域规则，再系统地改变设备配置、患者背景或可见证据。它扩大了训练情形，但不允许生成内容脱离既有物理机制或指南。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 固定病因生成并约束准入

教师策略$\pi_T$在病因已知的条件下生成观测$x_\omega$与参考轨迹$\tau_\omega=(z_1,z_2,z_3)$；独立混合检查器逐项检查证据忠实性、症状分层、因果链有效性、根因充分性及鉴别排除，失败草稿只做最小修改并重新检查，无法修复者丢弃。

<div class="method-step__io" markdown="1">

**输入**：候选世界$\omega$、世界规格$\mathcal{W}$和已知的目标病因$f$。<br>
**输出**：通过全部阶段准则的训练集$\mathcal{D}=\{(x_\omega,\tau_\omega)\}$，以及包含目标病因、变换类型和检查结果的审计记录。

</div>

**直观理解**：教师不做困难的“由症状猜病因”，而做较受约束的“已知病因后写出合理表现”。检查器像独立质检员，防止教师把自洽但违反规则的故事直接用于训练。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 学生推理与最早失败定位

检查器计算各阶段通过值$P_g$并选取最早失败阶段$g^*$；若$g^*<3$，系统仅替换失败阶段且禁止加入未观测事实、泄露目标病因或给出完整答案，再让学生独立生成后续阶段；若$g^*=3$，则不提供修复，只让学生重生成根因归因。

<div class="method-step__io" markdown="1">

**输入**：学生在无辅助条件下根据$x_\omega$生成的三阶段轨迹$\tau=(z_1,z_2,z_3)$。<br>
**输出**：带有单一失败边界的训练回合，以及按阶段$g$和变换族$v$聚合的首次失败与修复后失败记录。

</div>

**直观理解**：系统先找推理链中最早坏掉的一环，因为后续错误可能只是由这一环传递而来。局部修复不是标准答案，而是一块受限的“踏板”，用来测试学生在前提恢复后是否具备继续推理的能力。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 阶段局部强化学习与能力保持

在一次全量监督微调后，方法使用GRPO优化学生实际生成的后缀：修复内容进入提示但不进入损失，奖励只覆盖边界之后的阶段，并惩罚观测或规格不支持的断言；训练批次同时混入历史回放、当前强项的完整轨迹及少量教师参考轨迹。

<div class="method-step__io" markdown="1">

**输入**：失败边界$g^*$、保留的学生前缀、通过检查的局部修复，以及学生从边界之后生成的候选续写$\tau'$。<br>
**输出**：更新后的学生策略$\pi_{\theta_t}$，以及新的无辅助推理结果和弱点统计。

</div>

**直观理解**：模型只为自己重新写出的部分获得奖励，不能靠复制系统提供的修复“领功”。回放和完整轨迹则像复习旧题，用于避免修好一个阶段后破坏原先已经掌握的能力。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 阶段局部奖励

$$
R(\tau^{\prime})=\sum_{g=b(g^{*})}^{3}\sum_{\kappa\in\mathcal{K}_{g}}\lambda_{\kappa}\,\kappa(z^{\prime}_{g};\omega,\mathcal{W})-\mu\,U(\tau^{\prime}),\qquad b(g^{*})=\min\{g^{*}+1,3\}
$$

**符号说明**

- $R(\tau^{\prime})$：对学生生成续写轨迹的总奖励。
- $\tau^{\prime}$：从失败边界之后由学生重新生成的轨迹或后缀。
- $g^{*}$：检查器定位到的最早失败阶段。
- $b(g^{*})$：开始计奖的阶段；非末端修复时跳过被系统替换的失败阶段，末端失败时仍评价第三阶段。
- $\mathcal{K}_{g}$：分配给第g阶段的二元判定准则集合。
- $\kappa(z^{\prime}_{g};\omega,\mathcal{W})$：准则对学生生成阶段、目标世界和世界规格的通过值。
- $\lambda_{\kappa}$：准则权重，在训练前冻结。
- $U(\tau^{\prime})$：续写中不受观测或世界规格支持的断言惩罚。
- $\mu$：不受支持断言惩罚的系数。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标只奖励学生实际生成的后续阶段，不奖励系统提供的修复内容，并扣除凭空添加证据的行为。例如第二阶段被修复时，模型只因第三阶段的根因判断和鉴别排除得分，从而把优化信号集中到当前可训练的续写部分。<br>
**原文位置**：第4.4节，公式(4)

</div>

</div>

<div class="equation-block" markdown="1">

#### 弱点驱动的下一轮数据路由

$$
q_{t+1}(g,v)=(1-\epsilon)\frac{\exp(\eta w_t(g,v))}{\sum_{g^{\prime},v^{\prime}}\exp(\eta w_t(g^{\prime},v^{\prime}))}+\epsilon q_0(g,v)
$$

**符号说明**

- $q_{t+1}(g,v)$：下一轮选择阶段g与变换族v这一数据单元的概率。
- $w_t(g,v)$：第t轮该单元的弱点分数，由首次失败率和修复后失败率加权得到。
- $\eta$：控制采样概率向高弱点单元集中的程度。
- $\epsilon$：基础覆盖分布的混合比例，取值位于零到一之间。
- $q_0(g,v)$：覆盖全部阶段—变换单元的基础分布，文中采用均匀分布。
- $g$：推理阶段索引。
- $v$：反事实或观测变换族。

<div class="equation-explanation" markdown="1">

**直观理解**：Softmax项使错误越多的阶段—变换组合越常被选中，基础分布项则保证暂时表现较好的组合仍有机会被采样。这样既能集中资源补弱，也不会因短期错误统计而永久丢失某类数据覆盖。<br>
**原文位置**：第4.4节，公式(5)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练先在经约束准入的完整参考轨迹集合$\mathcal{D}$上执行一次监督微调，使学生掌握三阶段输出格式和基本推理。随后采用GRPO按组比较多个有效续写，以阶段局部奖励$R(\tau')$优化失败边界之后的学生生成内容，并相对于监督微调后的参考策略施加KL约束；奖励权重在训练前冻结，其中因果链有效性和根因充分性的权重较高。每轮还加入教师参考的少量监督损失、历史回放和强项完整轨迹，以限制跨阶段干扰、策略漂移及格式坍塌；新生成世界的完整参考轨迹则为被定位的薄弱阶段补充直接监督，因为修复条件下的强化学习刻意不对修复阶段本身计算损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 统一阶段准则与混合检查器**

学生轨迹分为$z_1$症状抽象、$z_2$因果链构造和$z_3$根因归因。阶段准则分别为$\mathcal{K}_1$中的证据忠实性与症状分层、$\mathcal{K}_2$中的因果链有效性，以及$\mathcal{K}_3$中的根因充分性与鉴别排除；结构化问题由规格查询处理，LLM只负责把自由文本片段映射到字段，并为违规给出字段和文本依据。

> 直观理解：同一组准则同时服务于数据准入、错误归因、奖励计算和再生成目标，使各环节对“正确”的定义一致。检查器与教师提议分开运行，可降低同一模型既生成又自我批准所造成的偏差，但作者明确指出它仍是经审计的有界检查器，而非形式化证明器。

**2. 受约束的失败边界修复**

系统以$g^*$表示最早未通过阶段，只保留$z_{1:g^*-1}$并用经准入的内容替换$z_{g^*}$；修复不得添加未观测事实、暴露目标病因或提供完整答案，后续$z'_{g^*+1:3}$由学生生成。更深层修复仅用于能力画像，不进入同一强化学习回合，因此每个回合只有一个可解释的失败边界。

> 直观理解：该模块把“整条答案错了”改写成“从哪一步开始错”。它既减少无关前缀对学习信号的干扰，也能区分学生是局部前提没建立好，还是即使前提被修复也无法完成下游推理。

**3. 双飞轮耦合：局部更新与定向生成**

强化学习飞轮根据$g^*$从修复边界启动，只优化学生生成的续写；数据飞轮则把首次失败率$\mathrm{FF}_t(g,v)$与修复后失败率$\mathrm{PRF}_t(g,v)$组合为$w_t(g,v)$，再经冻结映射$\rho(g,v)$转换成具体的数据生成操作。阶段局部化描述的是采样和损失边界，并不意味着模型拥有分阶段的独立参数。

> 直观理解：一个飞轮回答“该改模型哪段输出”，另一个回答“下一轮该造什么题”。二者通过同一弱点标签连接，使训练资源投向真实错误，而不是只增加更多均匀、重复的数据。

**训练与推理**

训练阶段中，教师和检查器可访问世界规格$\mathcal{W}$及预定病因，学生始终只看到观测$x_\omega$。完整流程为：构造并验收反事实世界；用完整参考轨迹进行初始监督微调；采样当前策略$\pi_{\theta_t}$的无辅助输出；定位$g^*$并构造单一失败边界回合；使用修复条件下的后缀或无修复的第三阶段进行GRPO更新；加入保存与回放数据；依据$w_t(g,v)$更新$q_{t+1}(g,v)$并生成下一轮新世界。推理阶段不再使用教师、世界规格、检查器、局部修复或飞轮，只保留训练后的学生模型和固定输出模式；学生根据新观测独立生成$z_1$、$z_2$和$z_3$。因此其部署目标是把训练期可访问的领域规则蒸馏进本地学生，而不是在测试时依赖规则检索或教师模型。

**复现信息**

公平解释该方法需要注意四点。第一，检查器的结构化查询与自由文本映射采用分工设计，且教师生成、数据准入、失败定位和奖励评分使用角色不同的调用；测试则使用独立构造并冻结的评分器，训练检查器不评价测试输出。第二，反事实算子包括改变条件或上下文的组合操作，以及保持诊断不变的可见性调整、混杂注入和遮蔽；标签改变类变换的目标标签在生成前固定。第三，下一轮路由并非让生成器自由解释弱点，而是通过训练前冻结的$\rho(g,v)$规定目标准则、算子子型、不变量和准入规则。第四，主训练流使用当前策略的新鲜在策略轨迹，旧轨迹只通过回放进入；开发集增益低于冻结阈值时停止，并设置最多八轮的上限，文中两个领域均在六轮后停止。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- LBNL industrial fault benchmark：包含 26,175 个病例、91 种故障，覆盖八类异构工业系统，用于工业故障诊断评测。基准病例不参与数据合成或训练；除病例留出外，还设置了在合成开始前固定的配置留出划分，以检验模型能否迁移到未见设备配置。所有工业评测病例的金标准推理链均由领域专业人员标注。
- DDXPlus evaluation subset：包含 128,800 个病例，按十类疾病分组，用于临床诊断评测；临床金标准推理链由基准中的证据和鉴别诊断标注独立构造。该基准的病例同样不参与合成或训练，因此它测试的是从冻结指南所生成监督向真实留出病例的迁移。
- 独立合成开发集与密封审计集：互不重叠的合成开发集在查看测试集或锁定审计集之前，用于确定提示词、阈值、超参数、停止目标和检查点。另有 1,500 个场景的密封审计集，按被接纳和被拒绝的草稿分层，用于估计训练检查器的错误率及最早失败阶段 $g^*$ 的定位质量；它不用于提示词调优。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Top-1 accuracy（Acc）**

衡量模型排名第一的最终诊断是否正确，主要反映根因或疾病结论的正确率；它不要求中间推理链全部正确。 （越高越好，因为更高表示更多病例得到正确的最终诊断。）

</div>
<div class="metric-item" markdown="1">

**Strict all-stage path correctness（Path）**

只有症状抽象、因果链构造和根因归因等全部阶段都符合金标准时才计为正确，是比最终答案准确率更严格的端到端推理指标。 （越高越好，因为它要求结论及其证据到原因的完整路径同时成立，能减少“答案碰巧正确但推理错误”的情况。）

</div>
<div class="metric-item" markdown="1">

**Stage-level scores**

分别评估诊断流程中各阶段的正确性，用于定位模型首先在哪个阶段失败，并判断训练改善发生在症状抽象、因果链构造还是根因归因环节。 （越高越好，因为更高表示相应诊断阶段更可靠；但单阶段高分不能替代严格全路径正确性。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 八类 LBNL 工业系统上的严格全阶段路径正确性，与最强常规基线比较

<div class="result-value" markdown="1">

作者报告，最终 8B 模型的 Path 指标比最强常规基线提高 11.6 个百分点。

</div>

这表明在工业故障诊断中，DiagLoop 的优势不仅是给出正确根因，还体现为更多病例能够通过完整的分阶段因果路径检查。由于摘要未给出双方绝对分数、置信区间及逐系统结果，该数字不能说明所有工业系统都获得同等幅度的提升，也不能仅凭此断定真实部署中的维修效果。

<div class="result-source" markdown="1">

来源：Abstract；所给第 5 节摘录未包含主结果表

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Gains are 11.6 points across eight industrial systems and 5.5 points across ten disease categories.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 十类 DDXPlus 疾病类别上的严格全阶段路径正确性，与最强常规基线比较

<div class="result-value" markdown="1">

作者报告，最终 8B 模型的 Path 指标比最强常规基线提高 5.5 个百分点。

</div>

临床域中的正向增益说明同一训练框架在更换指南、字段映射和判据后仍可能有效，支持方法跨机制领域复用的主张。不过 DDXPlus 是结构化诊断基准，结果不能直接外推到开放式真实病历、临床安全性或患者结局；摘要也未提供绝对 Path 分数和统计显著性。

<div class="result-source" markdown="1">

来源：Abstract；所给第 5 节摘录未包含主结果表

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Gains are 11.6 points across eight industrial systems and 5.5 points across ten disease categories.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 教师前提实验：直接诊断与已知预期原因后的前向场景构造

<div class="result-value" markdown="1">

在工业域/临床域的匹配开发集上，Qwen3.7-Max 直接诊断通过阶段判据的比例为 41.6%/38.2%；给定预期原因后，首稿通过率升至 78.4%/74.9%，在最多三轮修订—复检后接纳率达到 93.1%/90.6%。

</div>

该实验验证数据飞轮的一项关键前提：让教师从指定原因向前构造证据世界，比要求其从证据反向诊断更容易满足规则，而且有限次数的检查反馈能够进一步修复草稿。它支持采用“先指定原因、再生成反事实世界”的数据构造方向，但测量对象是教师生成可接纳训练场景的能力，并不直接等价于学生在留出测试病例上的诊断性能。

<div class="result-source" markdown="1">

来源：Section 5.2, “Forward construction”

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Testing H2, Qwen3.7-Max performs both directions on the matched development sets: direct diagnosis passes the stage criteria in 41.6%/38.2% of cases. Given the intended cause, first drafts pass in 78.4%/74.9% and revise–recheck reaches admission within 3 rounds in 93.1%/90.6%; expert audit preserves this ordering, supporting H2 (revision and call costs in Appendix C).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所给实验摘录在主结果表开始前截断，因此无法核验工业域和临床域的绝对 Acc、Path、分阶段分数、置信区间、校正后显著性及逐组表现；摘要中的百分点只能确认相对增益，正式引用前必须回查主表和附录。
- 训练与评测覆盖两个大型但结构化的基准，临床结果尤其不能直接代表开放式真实病历、分布漂移环境或实际治疗安全性。此外，闭源参考模型的参数量和训练数据未披露，作者也明确指出不能据此作模型规模层面的结论。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen3-8B 数据微调基线：分别使用未筛选、按答案一致性筛选、按约束检查器接纳的教师场景进行微调。三者比较生成数据的筛选质量，尤其用于判断独立约束检查是否优于仅检查教师答案是否一致。
- Plain GRPO：在均匀采样的新反事实世界上执行计算量匹配的强化学习，是判断收益是否仅来自一般强化学习更新而非阶段定位与数据飞轮的主要优化基线。
- Uniform-regeneration：持续生成新世界，但把提议分布固定为均匀分布，并匹配调用次数、令牌数和 GPU 小时。它隔离了“根据弱点调整后续数据分布”相对于“等预算地持续补充随机数据”的价值。
- Deranged-routing control：对完整的弱点画像条目 $ho$ 做类型兼容的错配，使测得的学生弱点被分配给错误的生成操作，同时尽量保持数据与计算流程不变。该对照直接检验性能是否依赖正确的弱点—生成路由关系。评测中另报告 Qwen3.7-Max 与 Claude-Sonnet-4.6 作为闭源参考，但因参数规模和训练条件不透明，不适合据此声称模型规模上的优势。

**实验想回答的问题**

- 在完全不使用基准病例进行合成或训练、也不依赖病例级专家推理标注的条件下，DiagLoop 是否能同时提高工业故障诊断与临床疾病诊断的最终答案准确性和严格全阶段推理路径正确性？
- 性能提升是否真正来自按学生最早失败阶段进行弱点定位与定向数据再生成，而非教师生成更多数据、筛选后数据量变化、计算预算增加，或一般性的强化学习？

**实验实现**

学生模型为 Qwen3-8B，工业域和临床域分别运行六轮数据飞轮；算法、阶段模式和优化超参数跨领域共享，仅替换规范、字段映射和具体判据。冻结的 Qwen3.7-Max 仅在训练阶段提议并修复场景，评测时作为零样本参考。四种反事实算子为遮蔽、混杂、可见性变化和组合，最大深度为 $K=3$；经过去重和领域有效性过滤，工业域与临床域分别得到 30,614 和 49,876 个可生成世界，最终接纳 14,302 和 21,744 个场景，其中 12,874 和 19,566 个场景用于冷启动监督微调答案。训练总成本分别为 218 和 342 聚合 GPU 小时。评测时所有模型共享证据、候选空间、输出模式、解析器和工具权限。训练模型对每个病例以温度 0.6 采样五次完成并取指标均值；主要比较使用三个随机种子，两个预先指定的因子实验各使用五个配对种子。统计检验采用保持方法配对关系的配对 bootstrap，并对预先固定的检验族进行 Holm 多重比较校正。测试输出由冻结的、以金标准推理链为条件的评分器评判，而训练检查器不参与测试评分；专家对 $g^*$ 的双重标注在 300 个病例上达到 Cohen's $arkappa=0.81$。单张 GPU 可部署，原文报告在 bf16、2,048-token 上限下每病例约 3.6 秒。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 正确阶段路由与 deranged-routing control 比较 | 作者报告，DiagLoop 相对错乱路由对照在工业域和临床域的 Path 指标分别提高 3.9 和 2.3 个百分点。 | 错乱路由保持弱点画像条目的类型兼容性，却故意把弱点分配给不对应的生成操作，因此该差距主要隔离“是否把后续数据生成指向正确失败阶段”。结果支持定向路由有独立价值，而非所有收益都来自相同预算下不断生成新样本；但所给摘录没有提供绝对分数、误差区间和显著性结果，仍需核对附录或主表。 | Abstract；控制构造见 Section 5.1, “Baselines and budgets”<br><span class="experiment-evidence">Gains over a deranged-routing control are 3.9 and 2.3 points, respectively.</span> |
| 反事实组合深度从一阶扩展至最大深度 $K=3$ 的可生成性检查 | 作者报告，从深度一扩展到 $k=K$ 时，各深度的接纳率始终与深度一接纳率相差不超过 5.1 个百分点。 | 该检查隔离组合深度增加是否会使生成世界迅速失效。接纳率变化较小，说明更复杂的遮蔽、混杂、可见性与组合扰动在操作上仍可由教师生成并通过检查器，而没有出现明显的有效样本率崩溃。但接纳率只反映场景可用性，不直接证明深层反事实一定提升最终诊断性能；其效用还需结合原文所称的算子和头尾类别结果判断。 | Section 5.2, “Forward construction”；详细结果指向 Appendix C<br><span class="experiment-evidence">Admission rates stay within 5.1 points of the depth-one rate through k=K, an operational feasibility check for H1 (Appendix C); the operator and head–tail results below assess the utility of the resulting variations.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：利用反事实数据生成、阶段化错误定位和局部强化学习后训练诊断语言模型的因果推理过程。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`7562eb2197f10f754b94d7e8a78d7dbc85c0307857ce597cb8266af9fe44d29a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
