---
title: "[论文解读] To Add Is Machine, To Delete Is Human: Measuring and Mitigating Deletion Avoidance in LLM Code Editing"
description: "[arXiv 2607.28887][LLM Reasoning] 本文将“删除规避”界定为大语言模型在代码编辑中保留本应移除代码的系统性行为，并通过真实补丁分析、删除专用基准和训练试验，研究其表现、成因及缓解可能性。"
arxiv_id: "2607.28887"
announcement_date: "2026-08-03"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-03T02:16:18.799742+00:00"
source_sha256: "0ef9fd91957c079753f0484cfe9a9ba73c5fd6b8d74cb1feb1d14642bc061e4a"
tags:
  - "LLM Reasoning"
  - "LLM 评测"
  - "大语言模型"
  - "代码编辑"
  - "仓库级代码修复"
  - "删除回避"
  - "Guard-and-Go"
  - "SWE-bench Verified"
  - "CanItDelete"
  - "删除敏感评测"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2607.28887</p>

# To Add Is Machine, To Delete Is Human: Measuring and Mitigating Deletion Avoidance in LLM Code Editing

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-03</span>
<span><strong>作者</strong> Amir M. Ebrahimi, Mohammed Mehedi Hasan, Aaditya Bhatia, Gopi Krishnan Rajbahadur, Ahmed E. Hassan</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> School of Computing, Queen’s University, Kingston, Ontario, Canada</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.28887) · [PDF 下载](https://arxiv.org/pdf/2607.28887) · **关键词** 大语言模型, 代码编辑, 仓库级代码修复, 删除回避, Guard-and-Go, SWE-bench Verified, CanItDelete, 删除敏感评测<br>


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

本文将“删除规避”界定为大语言模型在代码编辑中保留本应移除代码的系统性行为，并通过真实补丁分析、删除专用基准和训练试验，研究其表现、成因及缓解可能性。

**不用术语来说**：代码补丁通过测试，并不意味着它适合直接合并：模型常常不删除已经过时或错误的逻辑，而是在其外面增加条件判断、旁路或回退，使测试暂时通过。这样生成的代码更臃肿，增加维护者理解和审查的负担，还可能保留本应彻底消失的行为；然而，现有测试通常只检查功能结果，很少确认目标代码是否真正被移除。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出并操作化定义“删除规避”，分析通过 SWE-bench Verified 的真实模型补丁，识别出以新增守卫或旁路代替删除的主要模式“Guard-and-Go”，并用删除敏感测试检验常规通过率是否高估补丁的可合并性。
- 作者构建包含 200 个真实提交任务的删除专用基准 CanItDelete，并设计从一般指令、区域提示到精确删除跨度的诊断阶梯；此外，以单个 7B 模型进行试验性后训练，考察删除监督能否缓解该行为并迁移到一般代码编辑任务。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于基于大语言模型的软件工程与代码编辑研究。仓库级代码修复通常以自然语言问题描述和修改前的代码仓库为输入，由编码智能体定位相关文件并生成补丁；SWE-bench Verified 等基准主要依据补丁能否通过测试来判定任务是否解决。然而，测试通过并不等同于补丁忠实实现了预期修改，也不保证其适合合并与长期维护。本文聚焦其中一种可观察偏差——“删除回避”：当预期编辑要求移除某段代码时，模型仍保留该代码，常通过增加条件分支、保护逻辑或旁路使其暂时不执行。作者将这种主要表现称为 Guard-and-Go，并强调研究对象是补丁行为，而非对模型内部意图的推断。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**仓库级代码修复**

模型不仅改写一个独立函数，还需根据问题描述在完整项目中定位文件和代码区域、理解上下文并生成补丁。其困难同时包含修改意图理解、代码定位和编辑边界控制。

</div>
<div class="concept-item" markdown="1">

**删除回避（deletion avoidance）**

指预期修改要求删除代码时，模型补丁却系统性地保留目标代码。保留可以是原样留下，也可以是把它放入条件分支或回退路径，使现有测试暂时观察不到其影响。

</div>
<div class="concept-item" markdown="1">

**删除敏感评测**

传统测试只检查程序行为是否满足有限用例；删除敏感评测还明确检查目标代码是否仍然存在。本文使用基于出现位置与次数的确定性评估，避免把“绕开目标代码”误判为完成删除。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究包含两个互补场景。第一，作者分析真实仓库修复：输入为 SWE-bench Verified 的问题、修改前仓库以及模型生成的测试通过补丁，并以开发者补丁中的删除内容作为参照，检查模型是否到达正确文件与代码区域、是否删除精确目标行，以及是否采用 Guard-and-Go 保留目标逻辑；这里的核心假设是开发者补丁可用于界定该任务中预期移除的代码，但作者并不把文本完全一致视为唯一正确修复。第二，作者构建 CanItDelete，将加法和混合编辑等混杂因素移除：每个任务给出真实提交对应的完整修改前文件，所需编辑全部是删除，模型输出修改后的代码，再由能够区分重复代码出现位置的确定性评估器判断目标实例是否被完整删除、非目标内容是否被保留，以及模型是否额外添加代码。诊断提示依次提供明确删除意图、目标区域和精确删除跨度，用来区分意图理解、定位与编辑范围控制三类困难。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$P_m$**

模型 $m$ 针对一个代码编辑任务生成的补丁；这是为说明问题设置采用的记号，原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$P_d$**

开发者参考补丁，用于识别真实修复中要求删除的目标内容；原文节选未给出正式符号。

</div>
<div class="notation-item" markdown="1">

**$D$**

由开发者补丁确定的待删除代码实例集合；评估需区分相同文本在文件中的不同出现位置。

</div>
<div class="notation-item" markdown="1">

**$R_{del}$**

删除召回率，即集合 $D$ 中被模型补丁实际移除的目标实例比例；原文摘要将其用于衡量删除完成程度，但未在节选中提供正式公式。

</div>

</div>

**直接相关的工作**

- **SWE-bench 及 SWE-bench Verified（Jimenez et al., 2024；OpenAI, 2024）**: 这类基准从真实问题报告出发评估仓库级修复，为本文分析真实模型补丁提供场景；但其参考补丁通常混合增加、修改和删除，且以测试通过为主要判据，因此不能单独测量模型执行纯删除编辑的能力。
- **SWE-bench 有效性审计（Aleithan et al., 2024；Yu et al., 2025；OpenAI, 2026）**: 既有审计指出测试薄弱、通过标注错误及任务规格缺陷，说明测试通过未必代表正确实现需求。本文在此基础上进一步隔离删除行为，并加入“目标代码仍存在即失败”的删除敏感检查，以识别普通测试遗漏的保留代码问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

代码代理正被用于修复缺陷和提交拉取请求，但维护者需要的是符合仓库意图、简洁且可长期维护的补丁，而不只是能够通过现有测试的补丁。论文关注一种具体风险：当需求实际上要求移除旧逻辑时，模型可能保留该逻辑并添加控制流绕开它。作者将这种可观察的补丁行为称为“删除规避”；其后果是旧行为仍潜伏在代码中，补丁变得冗长，人工审查成本上升，而基于测试通过与否的评测仍可能把它判为成功。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于测试通过率的仓库级代码修复评测**：以 SWE-bench Verified 为代表的方法向模型提供真实软件问题和代码仓库，再运行原项目测试；若补丁通过规定测试，就将任务记为已解决。这类评测主要验证外部功能结果，通常不比较模型是否执行了开发者补丁中的必要删除。
- **通过提示提供更强的删除定位信息**：在删除任务中逐步补充明确删除要求、目标区域以及精确行或跨度，使模型更容易找到应当移除的代码。该思路把问题视为指令理解或定位不足，并通过增加上下文来诊断错误究竟发生在找不到目标，还是无法正确控制删除边界。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原有测试大多验证输出行为是否正确，却很少断言目标代码必须消失，因此模型可以用新增条件、守卫或回退绕过旧逻辑并照样得分；其直接后果是基准解决率可能高估补丁的可维护性与可合并性。
- 一般仓库修复任务同时包含代码定位、添加、修改和删除，因而观察到未删除目标时，无法判断根因是没有找到位置、没有理解需求，还是模型本身倾向于避免删除；即使给出精确跨度，也可能从“删得不够”转变为越界删除或额外添加代码，说明单纯加强定位仍不足以保证边界控制。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

既有代码修复研究缺少一套专门衡量删除行为的框架：没有把“本应删除却被保留”从普通功能失败中独立出来，也缺少能够区分目标定位、删除完整性和删除边界错误的真实任务基准。因此，尚不清楚删除规避在已通过测试的补丁中有多普遍、常以何种替代策略出现，以及它究竟主要源于定位困难、删除控制不足，还是模型训练中删除示例不足。

</div>
<div markdown="1"><span>核心问题</span>

当代码编辑确实要求移除现有逻辑时，当前大语言模型能否准确找到并完整删除目标、同时避免越界删除和无关新增；常规测试在多大程度上掩盖了这类失败，而有针对性的删除后训练能否缓解它并改善更广泛的代码编辑能力？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把删除从复杂修复中单独隔离：若任务的全部正确改动只有删除，就能排除新增功能和混合补丁带来的混淆；再逐级提供区域和精确跨度，可以判断失败发生在“找不到”还是“删不准”。进一步地，如果少量删除监督就能同时改善删除任务和一般修复任务，那么更合理的解释不是模型原则上不会删除，而是代码后训练更常奖励生成与添加，未充分训练模型在明确边界内停止保留旧代码。该训练结论目前只是单一 7B 模型上的概念验证，不能直接外推到所有规模、语言或部署环境。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文采用“现象测量—评测诊断—训练干预”的端到端研究路线。首先，以开发者补丁为行为参照，在固定 OpenHands 脚手架的五个 SWE-bench Verified 模型提交中定义并测量“参考删除”，同时区分模型是否到达目标文件、进入目标作用域以及真正删除目标行；随后，用带证据约束的 LLM 分类器判断模型是否以新增守卫或旁路替代删除，并通过删除敏感检查检验原测试套件能否发现目标代码仍被保留；最后，在通用代码后训练混合数据中加入少量删除监督，对比训练前后模型的删除完成度、边界保持能力及通用代码编辑性能。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造参考删除并对齐模型补丁

将开发者补丁和模型补丁分别应用到基础提交，以非测试 Python 文件中的源位置为单位提取删除；若开发者删除的行又出现在同一函数、类或模块的新增内容中，则将其视为代码移动而非真正删除。模型只有删除同一文件中的同一位置才算匹配，同时检查模型触及的所有非测试 Python 文件，以记录其额外删除。

<div class="method-step__io" markdown="1">

**输入**：SWE-bench Verified 的基础提交、开发者补丁，以及五个采用 OpenHands 脚手架的官方模型补丁。<br>
**输出**：每个任务 $t$ 的参考删除集合 $G_t$、每个模型 $m$ 的删除位置集合 $M_{t,m}$，以及任务、文件、作用域和源行之间的结构化对应关系。

</div>

**直观理解**：开发者补丁不是唯一正确答案，而是一把统一的比较尺。这里比较的是“模型是否删掉开发者删掉的那个位置”，并排除把代码搬到附近却误算为删除的情况。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 量化删除复现与定位层级

计算逐任务删除召回率和删除精确率，并对任务做宏平均，使删除一行和删除二十行的任务权重相同；对每个参考删除进一步记录模型是否修改目标文件、是否修改其 enclosing scope、是否删除精确源行。对全体模型一致解决与一致失败的任务，使用双侧 Mann–Whitney $U$ 检验、Cliff’s $\delta$ 效应量和 Holm 校正后的 $p$ 值进行描述性比较。

<div class="method-step__io" markdown="1">

**输入**：参考删除集合 $G_t$、模型删除集合 $M_{t,m}$，以及每个删除位置所属的文件和函数、类或模块作用域。<br>
**输出**：按模型和任务结果分组的删除召回、删除精确率、文件—作用域—源行三级到达率，以及组间统计差异。

</div>

**直观理解**：三级检查把“没找到代码”和“已经在附近编辑却仍不愿删除”分开。宏平均则避免长删除任务仅因行数多而支配总体结论。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 识别以新增控制流替代删除的补丁策略

使用 MiniMax-M2.7 将每个任务—模型对标为 Delete-and-Replace、Guard-and-Go 或 non-reference alternative，并要求分类器引用输入差异中的具体代码行；若引用证据不存在，则拒绝该标签。对 Guard-and-Go 样本再经开放编码形成结构类别，并由封闭编码器应用到全部相应样本。

<div class="method-step__io" markdown="1">

**输入**：问题描述、开发者补丁、模型补丁，以及预先计算的删除特征。<br>
**输出**：补丁级策略标签及 Guard-and-Go 的细分结构形式，用于判断模型保留开发者删除逻辑时新增了何种守卫、旁路或回退路径。

</div>

**直观理解**：低删除召回本身可能只是另一种正确修法，因此这一阶段检查模型“用什么代替了删除”。证据校验要求分类器指出补丁中的实际代码，降低仅凭语言印象贴标签的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立删除敏感评测并实施删除监督后训练

评测侧优先选择被删除的条件、控制流语句和完整代码块，构造源代码级检查，要求目标在其 enclosing scope 中消失，并仅保留基础版本检查失败而开发者补丁检查通过的任务。训练侧把 CanItDelete 流程生成并经确定性或测试驱动拒绝采样筛选的删除示例加入原代码后训练混合数据，在其余训练配方不变的条件下训练干预模型，并在删除专项与通用代码编辑基准上各运行三次推理取均值。

<div class="method-step__io" markdown="1">

**输入**：删除占开发者补丁较高比例的 SWE-bench Verified 任务、经 AST 分析选出的删除目标，以及由文件级和仓库级删除编辑构成的训练样本。<br>
**输出**：一组具有已验证删除要求的评测任务，以及仅在删除监督数据上不同的基线与干预检查点，可分别检验删除完成、删除边界和非删除任务迁移。

</div>

**直观理解**：普通测试只问程序行为是否通过，这个检查还明确问“指定旧代码是否真的消失”。训练实验则像在原课程中加入少量专项删除练习，用严格对照判断改变来自删除监督还是其他训练差异。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 1 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 逐任务删除召回率

$$
R_{t,m}=\frac{|G_t\cap M_{t,m}|}{|G_t|}
$$

**符号说明**

- $R_{t,m}$：模型 m 在任务 t 上复现开发者参考删除的比例。
- $G_t$：任务 t 中开发者补丁产生的参考删除位置集合。
- $M_{t,m}$：模型 m 在任务 t 的补丁中删除的源位置集合。
- $G_t\cap M_{t,m}$：开发者与模型共同删除的文件—源位置集合。
- $|\cdot|$：集合中的位置数量。

<div class="equation-explanation" markdown="1">

**直观理解**：分子统计模型与开发者共同删除的位置，分母统计开发者删除的全部位置；值越高，表示模型越完整地复现开发者的减法式修改。论文按任务宏平均该值，因此每个任务贡献相同权重，但该指标不宣称开发者补丁是唯一正确实现。<br>
**原文位置**：第 2.1 节 Study Design，Metrics

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：原文没有给出新的显式损失函数或优化目标公式；删除干预仍属于通用代码后训练，只是向原有代码数据混合中加入删除监督样本。因而可归因的实验变量是训练分布中删除示例的增加，而不是损失函数、优化器或专用适配器的改变；作者希望同时强化模型“选择删除”和“在正确边界停止删除”两种能力，但实验结果也说明二者并未被一个简单的数据增强步骤同时解决。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 位置级参考删除匹配器**

以基础提交为共同坐标系，对开发者和模型补丁进行位置级比较；参考删除限定为非测试 Python 文件中由开发者移除、且未在同一 enclosing scope 内恢复的源位置。匹配要求文件和位置一致，另以文件、作用域、行三个嵌套层级记录模型对目标的接近程度。

> 直观理解：它解决了文本相同但位置不同、代码移动却被误判为删除等问题，并能区分模型根本没找到目标与找到目标后选择保留。

**2. 证据约束的补丁策略分类器**

MiniMax-M2.7 综合问题、开发者补丁、模型补丁和删除特征，在“删除或替换大部分目标逻辑”“保留逻辑并新增条件或旁路”“在别处修复”三类之间分类。标签必须由所给 diff 中真实存在的行支持，Guard-and-Go 再通过开放编码与封闭编码得到结构子类。

> 直观理解：位置指标只能说明模型没有照着开发者删除；该模块进一步判断模型是否形成了稳定的替代模式，尤其是把旧逻辑留作仍可执行的默认或回退路径。

**3. 删除敏感检查与 CanItDelete 训练数据管线**

检查模块利用 AST 感知过程选择具有语义结构的删除目标，并验证检查在基础版本失败、在开发者版本通过。训练数据包括 10,000 个完整文件编辑样本和 2,821 个多文件仓库修复样本：前者由 DeepSeek-V3.2 生成完整编辑后文件并确定性拒绝采样，后者从仅含 Python 删除的提交构造指令与 fail-to-pass 测试，再由 mini-SWE-agent 和 MiniMax-M2.7 生成并按测试筛选。

> 直观理解：AST 帮助选择“整个条件或代码块”这类有意义的目标，而不是任意字符串。拒绝采样和修复测试用于过滤没有真正执行所需删除、破坏代码或不能证明修复有效的训练例子。

**训练与推理**

测量阶段直接分析官方排行榜补丁，不重新生成第 2 节所用提交，并固定 OpenHands 脚手架以减少工具调用和代码定位机制的混杂。删除敏感评测阶段则使用 GPT-5.6 Sol、Opus 4.8、GLM-5.2 和 DeepSeek-V4-Pro 重新生成补丁，再分别运行原测试套件与新增删除检查；两种判据作用于同一任务和同一模型补丁，因此差异来自评测标准而非生成设置。

后训练阶段使用同一 7B 内部模型初始化和相同训练配方建立对照：基线仅使用 15.9B-token 代码后训练混合数据，干预模型在同一混合数据上额外加入 12,821 个删除样本，共 112.1M tokens，约占混合数据的 0.7%；CanItDelete 评测题被排除出训练。两个检查点均训练六个 epoch，global batch size 为 64，并在 CanItDelete、SWE-bench Verified、CanItEdit 和 EditBench 上分别推理三次、报告均值；前三个非专项或仓库级基准用于检查删除监督能否迁移及是否造成通用编辑回退。

**复现信息**

公平解释该方法需要注意四点。第一，核心观察只把开发者补丁当作参照，不把任何不一致自动判为错误；真正的评测缺口由经验证的删除敏感检查单独检验。第二，第 2 节仅分析开发者补丁至少从非测试 Python 文件删除一行的任务，并以五模型结果一致的任务进行 solved–failed 对比，以同时控制任务和结果，但该对比仍是描述性的。第三，删除敏感任务先从删除至少占开发者补丁四分之一的任务中筛选，再要求检查在基础版本和开发者版本上呈现预期的失败—通过关系，因此它刻意偏向删除密集任务，不能代表完整 SWE-bench Verified 分布。第四，7B 模型和硬件细节因工业设置被匿名化，原文也未明确报告优化器、学习率或具体序列长度；这些缺失限制了完全复现，但基线与干预运行除约 0.7% 的删除训练数据外保持一致，足以支持该试点中的受控归因。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- CanItDelete：包含200个真实提交衍生的删除任务，来自35个活跃的高星仓库，其中151个为Python任务、49个为JavaScript家族任务，53个修改测试文件。候选池由Python和JavaScript各100个最受欢迎且活跃的非fork公开仓库产生；先获得79,074个“删除源码行但不增加行”的文件编辑，去除重复的仓库—提交—文件身份后得到74,485个候选，再按编辑前非空行数$L$、被删非空源码行数$C$和删除块数$H$的等权百分位指数排序，选取最高难度的200项。每项至少跨越三个彼此分离的删除块，因此它是刻意构造的多位置删除压力测试，而非GitHub修改的代表性样本。其作用是排除跨文件定位、替换代码生成和任务歧义：参考修改不添加任何内容，模型只需在保留无关代码的同时完成全部删除。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**删除合规成功率**

在全部任务中，同时满足完整目标已消失、目标外可执行结构得到保留、且没有引入影响行为或无关修改的输出比例。把代码注释掉或禁用不算删除；重复行必须删除指定的那一次出现。 （越高越好，因为它要求模型既删全目标，又不破坏任务范围之外的代码。）

</div>
<div class="metric-item" markdown="1">

**不完整删除率**

输出中仍保留至少一处必删代码的比例或失败构成；该指标包括以新增防护或替代逻辑掩盖保留代码等机制，衡量模型找到并执行全部必需删除的能力。 （越低越好，因为残留任何指定目标都表示删除任务未完成。）

</div>
<div class="metric-item" markdown="1">

**完整删除后的无效编辑率**

模型已经移除全部目标，但又发生过度删除、越界修改或其他影响行为及无关改动的比例，衡量删除边界和范围保持能力。 （越低越好，因为正确删除还要求模型在目标边界处停止。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 12个模型在CanItDelete原始模式上的总体删除合规表现

<div class="result-value" markdown="1">

删除合规成功率横跨18.0%至79.0%；Claude Opus 4.8以79.0%最高，GPT-5.6 Sol为74.0%。即使最强模型也仍有约五分之一的删除专用任务失败。

</div>

这说明删除回避并不只是完整仓库修复中的定位困难或替换代码错误：在文件已经直接给出、任务只要求删除时，问题仍然存在。不过，该结果只证明这些受控、高难度任务上的行为，不能直接推出模型在所有日常删除修改中的失败率。

<div class="result-source" markdown="1">

来源：第4.2节，图3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Claude Opus 4.8 leads the twelve models we evaluate at 79.0% deletion-compliant success, and GPT-5.6 Sol follows at 74.0% (Figure 3).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 原始模式下开放权重模型与前沿模型的比较

<div class="result-value" markdown="1">

最强开放权重模型Kimi K2 Thinking、MiniMax-M3、GLM-5.2和DeepSeek-V4-Pro集中在65.0%至67.0%，约落后前沿模型12个百分点；Qwen指令模型和较早MiniMax版本仅为18.0%至47.5%。任务难度具有区分度：200项中9项被全部12个模型解决，19项没有任何模型解决。

</div>

这一比较表明基准没有在高端或低端完全饱和，并能区分不同能力层级。开放权重领先模型彼此接近，但与最强闭源模型仍有明显差距；然而这是按高结构难度筛选后的压力测试，不能解释差距来自训练数据、模型规模还是编辑接口。

<div class="result-source" markdown="1">

来源：第4.2节，图3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The strongest of them, Kimi K2 Thinking, MiniMax-M3, GLM-5.2, and DeepSeek-V4-Pro, cluster within a narrow 65.0–67.0% band, whereas the Qwen instruct models and the earlier MiniMax releases reach only 18.0–47.5% and fail predominantly by leaving required code behind.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 12个模型的失败机制分解

<div class="result-value" markdown="1">

汇总失败中69.8%属于不完整删除，而且12个模型中有10个以此为主要失败类型；但GPT-5.6 Sol与GLM-5.2更常完整移除目标后发生过度删除或越界编辑。GPT系列中，不完整删除由114例降至20例，而完整删除后的无效编辑由14例升至32例。

</div>

单一成功率会掩盖两种不同控制问题：模型可能不会删全，也可能删全后停不下来。GPT系列的变化说明能力提升可能只是把“保留目标”转换成“过度编辑”，并不必然形成合规修改；这是机制层面的相关观察，不足以证明模型升级直接导致越界编辑。

<div class="result-source" markdown="1">

来源：第4.2节，图3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Along the GPT line in Figure 3, incomplete deletions fall from 114 to 20 while invalid edits after complete removal rise from 14 to 32, and Qwen shows the same exchange at lower capability, whereas MiniMax-M3 reduces both.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- CanItDelete是刻意选择高结构难度候选的诊断压力测试：每项至少有三个分离删除块，并从复杂度排名最高的候选中选取200项。因此其成功率适合比较模型和分析失败机制，但不能当作普通GitHub删除编辑的自然发生率或总体模型失败率。
- 基准只覆盖35个仓库中的Python与JavaScript家族文件，且阶梯实验仅评估5个模型、Claude Opus 4.8仅运行173项而非200项；此外，提供完整文件和精确跨度隔离了若干混杂因素，却也弱化了真实仓库中的跨文件依赖、上下文选择及测试执行问题。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 前沿闭源模型Claude Opus 4.8与GPT-5.6 Sol：用于估计当前高能力模型在删除专用任务上的上限，并检验一般代码能力较强是否足以消除删除回避。
- 领先开放权重模型Kimi K2 Thinking、MiniMax-M3、GLM-5.2与DeepSeek-V4-Pro：用于比较开放权重模型与前沿闭源模型之间的删除合规差距；原文将它们报告为表现接近的一组。
- Qwen系列指令模型：既覆盖较低的原始成功率，又参与诊断阶梯实验；其价值在于观察提供精确删除行后，目标保留是否会转化为越界编辑。
- 较早的MiniMax版本：作为同一模型家族内较早能力水平的参照，用于判断改进是否同时降低“未删完整”和“删除后无效编辑”两类错误。

**实验想回答的问题**

- 在完整文件已提供、唯一正确变换就是删除指定代码的受控条件下，大语言模型是否仍会回避删除；不同模型的失败主要来自未删干净，还是来自完成删除后又越界修改？
- 逐步提供“明确要求删除”“指出相关区域”“给出精确且区分重复出现位置的删除行”等线索，能否区分模型缺失的是删除意图理解、目标搜索能力，还是删除边界判断与范围控制能力？

**实验实现**

实验向模型提供完整的编辑前文件，并要求只执行删除，不需要跨文件搜索或编写替换代码。输出由确定性的、能区分重复出现位置的评价器评分，不使用LLM裁判。评价器先判断是否删除合规，再将失败划分为“必删代码仍存在的不完整删除”和“目标已完全删除但编辑无效”，并进一步识别add-and-retain、过度删除等机制。原始模式在12个模型、每个模型200项任务上评估；诊断阶梯选择5个模型，依次采用vanilla、explicit deletion、region pointer和exact lines四种累积模式，每一级只增加一种定位线索。阶梯实验中4个模型使用200项任务，Claude Opus 4.8使用173项。任务选择未使用任何模型表现，指令则在选样之后由GPT-5.6 Sol依据完整编辑前文件与参考差异起草，并经过LLM规则检查和作者审核。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 诊断阶梯中的低成本线索：在原始指令上明确禁止变通方案，并进一步提供相关区域指针 | 明确的“必须删除、不得变通”指令仅使成功率变化−2.5至+2.5个百分点；区域指针带来的变化为0.0至7.0个百分点，其中GLM-5.2增益最大。 | 这两个干预分别近似隔离任务意图理解和粗粒度搜索。效果普遍很小，说明失败通常不是因为模型没有读懂删除要求，也不主要是因为完全找不到相关区域；但不同模式并非随机对照实验，因此不能排除提示措辞与模型交互的影响。 | 第4.3节，图4<br><span class="experiment-evidence">Region pointers change success by 0.0–7.0 points, with the largest gain for GLM-5.2.</span> |
| 诊断阶梯最终级：提供区分重复出现位置的精确删除行 | 精确跨度使5个模型的成功率提高6.5至31.5个百分点，并将其中4个模型的不完整删除率降至0.6%至3.0%；Claude Opus 4.8达到97.7%，其余4个模型最终为56.5%至87.5%。但完整目标删除后仍有1.7%至26.0%的尝试因越界编辑失败。 | 该干预直接提供目标边界，因而主要隔离模型的边界定位负担。显著增益及残留错误的大幅下降支持“边界知识不足”的解释；同时仍存在的无效编辑说明，准确定位与克制地保持修改范围是两项独立能力。该结果不表示精确跨度即可完全解决代码编辑，因为除Claude外各模型仍有明显失败。 | 第4.3节，图4，Finding 5<br><span class="experiment-evidence">Exact deletion spans raise success by 6.5–31.5 points and nearly eliminate incomplete deletion for four of five models.</span> |

**定性案例**

- Qwen3-235B展示了错误类型转换：即使被精确告知删除内容，它仍在17.5%的任务中保留必删代码；与此同时，其完整删除后的无效编辑率由20.5%升至26.0%。这不是单个文件案例，而是模型级机制案例：更强的定位提示减少目标保留时，可能暴露或加剧过度编辑，因此只看成功率增量会遗漏模型是否真正学会在边界处停止。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Measures and mitigates a systematic failure mode in LLM code-editing behavior, combining code reasoning with capability evaluation.; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`0ef9fd91957c079753f0484cfe9a9ba73c5fd6b8d74cb1feb1d14642bc061e4a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
