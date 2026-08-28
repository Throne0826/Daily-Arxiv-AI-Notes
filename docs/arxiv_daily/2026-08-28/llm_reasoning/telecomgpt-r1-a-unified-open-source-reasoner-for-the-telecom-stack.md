---
title: "[论文解读] TelecomGPT-R1: A Unified Open-Source Reasoner for the Telecom Stack"
description: "[arXiv 2608.26126][LLM Reasoning] 本文针对通用推理模型缺少电信领域依据、现有电信模型又缺乏跨任务多步推理能力的双重缺口，尝试构建一个能统一处理协议、知识、建模与故障问题的开源电信推理模型。"
arxiv_id: "2608.26126"
announcement_date: "2026-08-28"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:37:05.426073+00:00"
source_sha256: "17226315d4e43dd54c811b57e9efe6f7d4624ed2789f9ff38060241231cb97e4"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "电信大语言模型"
  - "统一电信推理"
  - "异构电信证据"
  - "监督微调"
  - "思维链"
  - "低秩适配"
  - "群组相对策略优化"
  - "可验证奖励"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.26126</p>

# TelecomGPT-R1: A Unified Open-Source Reasoner for the Telecom Stack

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Bohao Wang, Chenwei Wu, Haoyu Li, Hang Zou, Yu Tian, Lina Bariah, Li Wei, Chongwen Huang, Yongliang Shen, Zhaoyang Zhang, Merouane Debbah</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> for the Telecom Stack；College of Information Science and Electronic Engineering, Zhejiang University, 310027, Hangzhou, China；Department of Electrical Engineering and Computer Science, University of Michigan, Ann Arbor, MI 48109-2122, USA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26126v1) · [PDF 下载](https://arxiv.org/pdf/2608.26126v1) · **关键词** 电信大语言模型, 统一电信推理, 异构电信证据, 监督微调, 思维链, 低秩适配, 群组相对策略优化, 可验证奖励<br>


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

本文针对通用推理模型缺少电信领域依据、现有电信模型又缺乏跨任务多步推理能力的双重缺口，尝试构建一个能统一处理协议、知识、建模与故障问题的开源电信推理模型。

**不用术语来说**：真实的电信排障或配置检查通常不能只靠回答一道知识题：工程师可能需要同时查阅通信标准、读取网络日志和表格、核对性能指标、计算无线参数，并检查代码或配置是否违反约束。不同材料的表达方式和判错规则并不相同，因此，一个回答流畅但不会正确使用这些证据的模型，很难可靠地进入日常工程流程。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者将电信推理明确表述为一个跨异构任务与证据类型的统一策略学习问题，要求同一模型面向标准、日志、表格、公式、代码及配置证据，按照来源特定的正确性标准完成有依据的长链推理。
- 作者以四类推理轴组织包含67,427个样本的监督微调语料，并提出“多教师LoRA监督微调后接DAPO稳定化GRPO”的两阶段训练路线；其目的分别是注入电信知识与推理格式，以及利用按推理轴设计的二元验证奖励进一步优化统一策略。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于“面向电信工程的大语言模型推理”领域。实际电信任务并非单一的静态问答：模型可能需要联合理解3GPP等规范性标准、O-RAN配置表、无线接入网日志、关键性能指标、射频与网络公式、程序代码及厂商相关故障证据，并依据各类来源不同的结构和正确性规则形成可核验的多步推理。论文因此把电信推理界定为一种跨异构任务与数据模态的统一能力：同一模型既要掌握标准约束和专业术语，又要能分析结构化证据、执行精确计算并定位故障，而不能只生成表面连贯的技术回答。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**监督微调（SFT）**

使用“输入—期望回答”样本继续训练预训练模型，使其学习特定领域知识、回答格式和推理模式。本文的SFT语料覆盖协议、知识、建模和故障四类推理轴。

</div>
<div class="concept-item" markdown="1">

**思维链（CoT）**

在最终答案之外显式给出中间推理步骤，以帮助模型学习多步分析。本文强调按证据类型生成不同的思维链，因为标准条文、日志、公式和故障材料所需的推理方式并不相同。

</div>
<div class="concept-item" markdown="1">

**可验证奖励强化学习**

模型生成多个候选回答后，由可自动判定的验证器给出奖励，再据此更新生成策略。本文针对四个推理轴设置二元验证奖励，以强化答案在相应任务上的正确性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是来自电信工程异构来源的问题及其证据，例如标准条文、协议流程、日志、配置表、性能计数器、公式、代码或故障记录；输出是包含必要中间步骤、以证据为依据并满足来源特定正确性标准的答案。研究设定要求一个约90亿参数的开源模型以统一策略处理协议、知识、建模和故障四条推理轴，而非为每一种来源分别维护专用模型。其关键假设是：通用推理模型虽具备数学和编码能力，但缺少可靠的电信领域落地能力；现有电信模型虽增加了专业知识，却多集中于静态问答、检索辅助回答或单一任务族，尚不足以完成跨标准、日志、表格、公式和代码的长链推理。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **TelecomGPT与Tele-LLMs**: 二者通过领域语料、继续预训练、指令微调或任务对齐增强电信知识，并改善电信问答、分类等任务；本文将其视为领域适配的重要基础，但指出它们主要面向静态问答或特定任务，未解决异构证据上的统一多步推理。
- **WirelessMathLM与ORANSight-2.0**: 前者展示可验证奖励强化学习对无线数学推理的价值，后者展示检索增强指令微调对O-RAN理解的价值；它们分别聚焦特定任务族或证据来源，本文试图进一步训练一个覆盖协议、知识、建模和故障任务的统一策略。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

电信工程中的标准解释、协议分析、日志诊断、配置审查、无线公式验证和代码排错往往相互关联。例如，定位网络故障可能需要把3GPP流程与O-RAN配置表对应起来，再追踪日志异常、核验KPI变化，并检查实现是否违反标准约束。部署所需的核心能力因而不是静态问答，而是从多种结构和语义不同的材料中提取证据、建立联系并完成可核验的多步判断。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **通用前沿推理模型**：以GPT-5、Claude Opus 4.5等为代表，依靠大规模通用训练获得数学、编程和多步推理能力，再直接将这些通用能力迁移到电信问题上。
- **电信领域专用模型与任务型增强方法**：TelecomGPT、Tele-LLMs等通过电信语料、持续预训练、指令微调或任务对齐增强领域知识；WirelessMathLM和ORANSight-2.0则分别利用可验证奖励强化学习或检索增强指令微调，改善无线数学、O-RAN理解等特定任务。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 通用推理模型缺少对电信标准、计数器、协议流程和运维证据的可靠 grounding。作者指出，这类模型可能把结构化RAN日志当作普通文本，混淆3GPP工作组职责，或虚构信息元素、定时器、计数器及协议流程；结果是推导表面连贯，却不满足标准约束。
- 现有电信专用模型多集中于静态问答、检索辅助回答或单一任务与证据来源。即使其领域知识或局部能力有所提升，也尚未证明同一个策略能够在标准、日志、表格、公式和代码之间迁移，并持续生成较长且有证据支撑的推理链。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有研究分别覆盖了“擅长一般推理但不熟悉电信证据”和“熟悉部分电信内容但只处理有限任务”两端，尚缺少一种统一、开源的训练框架，使同一模型能够针对异构电信证据采用相匹配的推理形式与判定标准，并把这些能力整合为可跨任务泛化的策略。

</div>
<div markdown="1"><span>核心问题</span>

如何构建一个统一的电信推理模型，使其能够跨越异构的电信任务与数据来源进行泛化？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是先按协议、知识、建模和故障四种推理轴拆分能力需求，让训练样本、思维链生成方式和验证规则都与相应证据结构匹配；随后再用监督微调把领域知识与回答规范装入同一骨干模型，并通过按轴设置的可验证奖励联合优化。直观地说，这不是要求模型用一种固定套路读取所有材料，而是先分别教会它如何读标准、做计算和查故障，再把这些专长收束到一个能够按题目选择推理方式的统一模型中。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TelecomGPT-R1-9B采用“数据构建—监督微调—验证器强化学习”的两阶段后训练路线。首先按协议、知识、建模和故障四条推理轴，从3GPP/O-RAN规范、运营商与厂商资料、srsRAN代码、通信教材论文及合成RAN运行记录中构建问题；随后使用与各轴证据形态匹配的方法生成并校验思维链，形成含67,427个样本的统一语料。模型以Qwen3.5-9B为起点，先通过LoRA监督微调学习通信知识、回答格式和分轴推理模式，再通过DAPO稳定的GRPO，依据四类二值验证器提供的奖励优化完整推理轨迹。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 定义推理轴并收集原生证据

将任务划分为协议、知识、建模和故障四轴，并为每一轴选择保留其原生证据结构的来源：协议轴对应规范条款，知识轴对应事实与术语，建模轴对应代码、公式和计算，故障轴对应运行记录与诊断规则。四轴在最终语料中的占比分别为50.7%、21.5%、17.4%和10.4%。

<div class="method-step__io" markdown="1">

**输入**：公开的3GPP与O-RAN规范、运营商和厂商文档、通信论文与术语表、srsRAN C++代码、教材讲义，以及由用户侧记录和工程参数表组成的5G RAN故障数据。<br>
**输出**：带有推理轴与来源标签的原始材料集合。

</div>

**直观理解**：这一步不是把所有通信材料混在一起，而是先区分“查规范、记知识、做计算、诊故障”四种能力，再为每种能力准备最合适的证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成轴匹配的问题与答案

从规范中合成需要条款级或流程级理解的问题；从srsRAN的抽象语法树和Doxygen符号中生成带邻近模块干扰项的层次化选择题；从教材、讲义和论文中遮蔽公式或推导目标以生成计算题；同时将术语事实转为问答，并基于371张真实3GPP表格构造表格推理题。故障轴把原有粗粒度规则扩展为依次执行计算、阈值检查和根因指派的规则回放系统。

<div class="method-step__io" markdown="1">

**输入**：按四轴组织的原始材料。<br>
**输出**：覆盖规范理解、事实问答、代码与数学建模、表格推理及故障根因分析的候选问答样本。

</div>

**直观理解**：同一套出题模板无法同时考查规范阅读和无线计算，因此作者让题目形式跟随证据形式；例如代码题围绕真实函数关系设置干扰项，而故障题要求从指标逐步推出根因。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成并验证分轴思维链

协议与知识题采用教师LLM生成解释并进行自验证；数学题生成可由Python执行的推理链，再以符号等价和单位容差检查；故障题通过确定性规则回放产生$[Calculation]/[Rules]/[Answer]$结构。所有轴还执行前缀续写自验证：把已有推理作为强制前缀，只有后续仍能重新导出标准答案的样本才保留。

<div class="method-step__io" markdown="1">

**输入**：候选问答样本、标准答案及对应的原始证据。<br>
**输出**：经过多轮验证、增强、泄漏过滤、难度分层和风格混合的67,427条监督微调轨迹，统一表示为$\{system,user,assistant\}$结构，并保留轴与来源标签。

</div>

**直观理解**：作者不仅检查最终答案，还检查推理过程能否被执行或重放；前缀续写验证相当于遮住推理的后半段，测试模型能否沿着已有步骤再次得到正确答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### LoRA监督微调

使用秩为$r$、缩放系数为$\alpha=2r$的LoRA适配器，以按回答长度归一化的逐词元负对数似然训练统一策略$\pi_\theta$。四轴样本在同一训练流中出现，使一个模型同时吸收通信知识、答案约束和不同的思维链格式。

<div class="method-step__io" markdown="1">

**输入**：四轴交错排列的已验证轨迹集$\mathcal{D}$和Qwen3.5-9B基础模型。<br>
**输出**：具备通信领域知识与结构化推理格式的SFT策略，同时作为后续强化学习的初始策略和KL参考策略$\pi_{\mathrm{ref}}$。

</div>

**直观理解**：这一阶段类似先用标准解题示范教会模型“知道什么、按什么步骤写、答案放在哪里”；LoRA只训练较小的附加参数，避免完整更新全部基础模型参数。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### LoRA监督微调目标

$$
\mathcal{L}_{\mathrm{SFT}}(\theta)=-\,\mathbb{E}_{(x,y)\sim\mathcal{D}}\!\left[\frac{1}{|y|}\sum_{t=1}^{|y|}\log\pi_{\theta}\!\left(y_t\mid x,y_{<t}\right)\right]
$$

**符号说明**

- $\mathcal{D}=\{(x^{(n)},y^{(n)})\}_{n=1}^{N}$：含有N个样本的已验证监督轨迹集，每个样本由输入提示和目标回答构成。
- $x$：系统指令、用户问题及必要上下文组成的模型输入。
- $y$：目标回答序列，包括分轴思维链和最终答案。
- $y_t$：目标回答的第t个词元。
- $y_{<t}$：目标回答中位于第t个词元之前的前缀。
- $|y|$：目标回答的词元长度，用于对长短样本的损失进行归一化。
- $\pi_\theta$：参数为θ的LoRA适配后生成策略。
- $\theta$：监督微调和后续强化学习需要优化的策略参数。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标逐词元提高标准推理轨迹的生成概率，并用$1/|y|$消除长回答天然产生更大总损失的影响。其作用不仅是记忆答案，还包括把协议解释、数学计算和故障诊断所需的结构化书写方式安装到同一策略中。<br>
**原文位置**：Section II-B，Equation (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### DAPO-GRPO目标、组相对优势、二值奖励与动态采样

$$
\begin{aligned}
\mathcal{J}(\theta)={}&\mathbb{E}_{(x,\{o_i\})\in\mathcal{G}_{\mathrm{train}}}\!\left[\frac{1}{\sum_i|o_i|}\sum_{i,t}\min\!\left(\rho_{i,t}\hat A_{i,t},\operatorname{clip}(\rho_{i,t},1-\varepsilon_\ell,1+\varepsilon_h)\hat A_{i,t}\right)\right]\\
&-\beta D_{\mathrm{KL}}(\pi_\theta\|\pi_{\mathrm{ref}}),\\
\rho_{i,t}(\theta)={}&\frac{\pi_\theta(o_{i,t}\mid x,o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t}\mid x,o_{i,<t})},\\
\hat A_i={}&\frac{R(o_i)-\operatorname{mean}_{j=1}^{G}R(o_j)}{\operatorname{std}_{j=1}^{G}R(o_j)+\eta},\\
R^{(a)}(o)={}&\mathbbm{1}\!\left[V^{(a)}(o,y^\star)=1\right],\qquad R(o_i)=R^{(a(x))}(o_i),\\
\mathcal{G}_{\mathrm{train}}={}&\left\{(x,\{o_i\}_{i=1}^{G}):0<\frac{1}{G}\sum_{i=1}^{G}R(o_i)<1\right\}.
\end{aligned}
$$

**符号说明**

- $x$：带有推理轴标签a(x)的训练提示。
- $o_i$：当前策略针对同一提示采样的第i条完整推理输出。
- $G$：每个提示所采样的输出数量，即GRPO组大小。
- $\rho_{i,t}$：第i条输出在第t个词元处，新策略相对旧策略的生成概率比。
- $\hat A_i$：第i条输出相对于同组其他输出的标准化优势；在目标中按其词元共享为逐词元优势。
- $R^{(a)}(o)$：轴a对应的二值奖励；验证通过为1，否则为0。
- $V^{(a)}$：协议、知识、建模或故障轴对应的专用正确性验证器。
- $y^\star$：用于验证生成输出的标准答案。
- $a(x)$：提示x所属的推理轴标签。
- $\mathcal{G}_{\mathrm{train}}$：动态采样后保留的训练组集合，只包含奖励均值严格位于0和1之间的组。
- $\varepsilon_\ell,\varepsilon_h$：重要性概率比的下侧和上侧裁剪宽度，文中分别设为0.20和0.28。
- $\pi_{\theta_{\mathrm{old}}}$：生成当前批次输出时使用的旧策略。
- $\pi_{\mathrm{ref}}$：SFT阶段得到且在强化学习中固定的参考策略。
- $\beta$：KL正则权重，文中设为0.001。
- $\eta$：加入奖励标准差分母的正数，用于数值稳定。

<div class="equation-explanation" markdown="1">

**直观理解**：每条输出先由对应轴的验证器判为0或1，再与同组平均表现比较：比组内平均更好的轨迹获得正优势，更差的轨迹获得负优势。裁剪限制单次策略变化，KL项把模型拉回SFT策略附近；动态采样排除全对和全错组，因为这些组的奖励没有组内差异，几乎不能提供有效的相对学习信号。<br>
**原文位置**：Section II-B，Equations (2)–(5)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：第一阶段最小化$\mathcal{L}_{\mathrm{SFT}}$，使策略复现经过验证的四轴答案与推理格式；该阶段解决“领域知识和输出规范尚未安装”的问题。第二阶段最大化$\mathcal{J}(\theta)$：模型不再只模仿固定示范，而是对每个提示采样多条轨迹，由轴匹配验证器判断正确性，再用组相对优势提高正确轨迹的概率、降低错误轨迹的概率。非对称裁剪控制更新幅度，逐词元聚合适配长推理，动态采样缓解二值奖励导致的大量零信息组，KL正则则维持SFT阶段学到的知识和结构化格式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 分轴数据生成与前缀续写自验证**

协议和知识轴使用教师LLM解释，数学建模轴使用Python重执行、符号等价与单位容差校验，故障轴使用确定性规则回放；随后把推理链作为强制前缀，要求模型续写时仍能导出标准答案。共享处理还包括多轮验证、数据增强、泄漏过滤、难度分层和风格混合。

> 直观理解：不同任务的“正确推理”判据不同：计算应能复算，故障诊断应能重放规则，规范题则要保持答案一致。分轴验证比仅让教师模型口头判断自己的解释更可靠。

**2. 统一的轴匹配二值验证器接口**

每个样本由轴标签$a(x)$选择验证器$V^{(a)}$：协议和知识任务检查$\boxed{L}$或$ANSWER: L$形式的选项，建模任务采用符号等价、单位容差及选择题字母检查，故障任务执行确定性规则回放。相同验证器既用于语料筛选，也用于强化学习奖励$R^{(a)}(o)$，使数据质量控制和策略优化采用一致的正确性标准。

> 直观理解：验证器相当于四类专用阅卷器，而不是一个模糊的通用评分模型；同一套阅卷规则贯穿数据制作和强化学习，可减少训练目标前后不一致。

**3. DAPO稳定的GRPO优化器**

GRPO以同一提示的多条输出为比较组，通过组内奖励均值和标准差计算相对优势，无需单独训练价值模型。作者加入动态采样、逐词元损失、非对称概率比裁剪和锚定SFT策略的KL正则，以应对二值奖励稀疏、长轨迹更新不稳定及结构化格式遗忘。

> 直观理解：动态采样把算力集中在模型“有时会、有时不会”的题目上；非对称裁剪允许一定探索，而KL锚点则防止强化学习把SFT阶段学到的故障模板和尾部JSON等格式破坏掉。

**训练与推理**

训练时，先将67,427条样本按四轴交错送入Qwen3.5-9B，以LoRA完成监督微调；随后对强化学习提示按组采样输出，依据$a(x)$调用协议、知识、建模或故障验证器，计算二值奖励并过滤全对或全错组，再执行DAPO式GRPO更新。推理时不再需要组采样、标准答案、动态过滤或奖励计算：用户输入单个通信问题，统一策略根据训练中形成的轴相关能力生成推理过程和最终答案；原文节选未明确说明部署时是否显式预测轴标签或调用外部验证器，因此不能认定推理阶段存在额外路由器。

**复现信息**

复现方法所需的关键设置包括：基础模型为Qwen3.5-9B；SFT采用LoRA，适配器缩放设为$\alpha=2r$；语料规模为67,427，协议、知识、建模、故障轴占比分别为50.7%、21.5%、17.4%和10.4%；强化学习使用逐词元损失、动态保留混合奖励组、非对称裁剪$\varepsilon_\ell=0.20$与$\varepsilon_h=0.28$，并使用权重$\beta=0.001$的SFT锚定KL正则。原文节选未明确报告LoRA秩$r$的具体数值、GRPO组大小$G$、学习率、批量大小、训练轮数、最大上下文长度、采样温度或计算硬件。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 协议与网络知识组：3GPP-TSG、ORANBench和srsRANBench。它们分别考查3GPP规范知识、O-RAN相关知识以及srsRAN软件栈知识，是检验模型能否依据专业规范和实现语境作答的主要任务。原文未明确报告各基准的样本规模、数据划分或是否使用隐藏测试集。
- 运维诊断与定量推理组：TeleLogs和TeleMath。TeleLogs要求依据遥测或日志中的阈值、变化方向和规则链定位故障；TeleMath要求执行符号化、分步骤的射频或网络计算。二者也是思维链设计和强化学习消融的重点，因为它们分别需要确定性规则复演与可靠的数学推导。原文未明确报告样本规模和划分。
- 通用电信问答与结构化证据组：TeleQnA和TeleTables。TeleQnA测试电信领域问答，TeleTables测试基于表格证据的理解与作答；文中将二者描述为接近监督微调性能上限的选择题型任务。原文未明确报告样本规模和划分。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**单轴准确率**

模型在某一电信基准上给出正确最终答案的比例；论文对七个任务轴分别报告该指标。它能衡量结果正确性，但不能单独证明中间推理过程真实、无捷径或可解释。 （越高越好，因为正确回答的测试样本占比更大。）

</div>
<div class="metric-item" markdown="1">

**七轴平均准确率（Avg）**

七个公开电信基准准确率的聚合平均值，用于概括模型在整个电信栈上的总体表现。该平均数会掩盖任务间差异，因此需要结合TeleLogs等单轴结果解读。 （越高越好，因为表示跨任务的整体正确率更高。）

</div>
<div class="metric-item" markdown="1">

**百分点变化（pp）**

两个准确率之间的绝对差，例如从$42.0\%$到$75.0\%$是增加$33$个百分点；它用于量化后训练阶段相对监督微调初始化的增益，而不是相对百分比增长率。 （在比较改进方法时通常越高越好，但负值或接近零也可揭示某些任务已经饱和或发生性能退化。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### GSMA开放电信排行榜七轴总体结果及与开源、闭源模型的比较

<div class="result-value" markdown="1">

TelecomGPT-R1-9B取得$82.1\%$的七轴平均准确率。作者报告其比685B参数的开源通用模型DeepSeek-V3的$59.3\%$高$22.8$个百分点，同时高于文中列出的GPT-5（$71.9\%$）、Claude-Opus-4.6（$73.3\%$）和Gemini-3.1-Pro（$75.6\%$）。

</div>

该结果支持论文的核心经验结论：有针对性的电信语料、推理轨迹和验证器驱动后训练，可使9B模型在该排行榜上超过规模远大的开源通用模型，并处于论文所称的闭源前沿层级。由于各模型的训练数据、推理预算和评测配置未被统一控制，这不是参数效率的严格因果实验，也不能推出该模型在排行榜之外普遍优于这些闭源模型。

<div class="result-source" markdown="1">

来源：第III节，图2及其前置结果说明

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

TelecomGPT-R1-9B traces the outer edge among open-source models, exceeding the current best open-source generalist DeepSeek-V3, a 685B-parameter model that reaches a 59.3% seven-axis mean, by +22.8 pp at roughly 1/75 of the parameter count, and stays within the closed-source frontier tier alongside GPT-5 at 71.9%, Claude-Opus-4.6 at 73.3%, and Gemini-3.1-Pro at 75.6%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 最终SFT+DAPO检查点在七个任务轴上的表现

<div class="result-value" markdown="1">

最终模型的平均准确率为$82.1\%$；各轴依次为3GPP-TSG $79.0\%$、ORANBench $86.7\%$、srsRANBench $88.7\%$、TeleLogs $75.0\%$、TeleMath $75.0\%$、TeleQnA $84.3\%$和TeleTables $86.0\%$。

</div>

结果表明总体均值并非由单一任务支撑：模型在七轴上均取得较高准确率。不过TeleLogs和TeleMath仍低于多个知识或选择题型任务，说明故障规则推演与精确计算仍是相对困难的能力。该行只展示最终检查点的横向覆盖面，不单独证明DAPO是全部提升的来源。

<div class="result-source" markdown="1">

来源：表I，SFT+DAPO行；列顺序为Avg、3GPP、ORAN、srsRAN、TeleLogs、TeleMath、TeleQnA、TeleTables

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

SFT+DAPO | 82.1 | 79.0 | 86.7 | 88.7 | 75.0 | 75.0 | 84.3 | 86.0

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 在共享9B SFT初始化上比较SFT、GRPO和DAPO

<div class="result-value" markdown="1">

SFT的七轴均值为$75.2\%$，SFT+GRPO为$77.2\%$，SFT+DAPO为$82.1\%$。相对SFT，DAPO增加$6.9$个百分点；其中TeleLogs从$42.0\%$升至$75.0\%$，3GPP-TSG从$71.0\%$升至$79.0\%$，而ORANBench、TeleQnA和TeleTables仅在其SFT水平附近波动。

</div>

共享初始化使该比较主要考查不同强化学习策略的作用。增益集中在初始表现较弱、奖励信号仍有区分度的TeleLogs和3GPP-TSG，而不是所有任务一致提升；这符合动态采样将更多 rollout 分配给未饱和样本的解释。它仍不能把改进完全归因于DAPO的某个单独机制，因为DAPO同时涉及动态采样和非对称裁剪，且论文没有给出多次运行误差。

<div class="result-source" markdown="1">

来源：第III-A节，表I

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Empirically, as quantified in Table I, the SFT-only checkpoint reaches a mean of 75.2%, with DAPO adding +6.9 pp on top to reach 82.1%. The largest DAPO gains land on the under-saturated axes: TeleLogs jumps from 42.0% to 75.0% (+33 pp), and 3GPP-TSG rises from 71.0% to 79.0% (+8 pp).

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验未报告测试集规模与划分细节、解码协议、随机种子、多次重复训练、置信区间或显著性检验。因此，$1$至$3$个百分点的波动是否超过随机误差无法判断，尤其不宜把饱和任务上的小差异解释为稳定优劣。
- 关键消融存在因素耦合：Multi-source方案同时改变来源匹配、生成提示和教师多样性，DAPO也同时引入动态采样与非对称裁剪。现有结果支持“完整方案有效”，但不能严格量化每个子组件的独立因果贡献；此外，与闭源模型的比较基于排行榜分数，训练数据和推理预算并未统一。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 共享初始化的SFT、SFT+GRPO和SFT+DAPO三个训练阶段：三者均从Qwen3.5-9B的LoRA监督微调初始化出发，因此可较直接地比较普通组相对策略优化GRPO与带动态采样、非对称裁剪的DAPO所带来的变化。
- DeepSeek-V3：685B参数的开源通用模型，被论文视为当时表现最强的开源通用基线；它用于判断电信专门训练能否弥补约两个数量级的参数规模差距。
- GPT-5、Claude-Opus-4.6和Gemini-3.1-Pro：三种闭源前沿推理模型，作为能力层级参照，用于判断9B开源模型是否进入闭源前沿区间，而非用于严格控制训练数据或计算量的同条件比较。
- NoCoT与BadCoT：NoCoT仅以答案作为监督目标，用于测试显式推理轨迹是否必要；BadCoT由单一通用教师生成、不匹配数据来源，用于比较通用思维链与论文所用轴匹配、多教师思维链。

**实验想回答的问题**

- TelecomGPT-R1-9B在覆盖协议规范、开放无线接入网、软件无线接入网、故障诊断、通信计算、领域问答和表格理解的统一评测中，能否以较小参数规模超过现有开源电信模型，并接近闭源前沿推理模型？
- 性能提升分别来自哪些环节：领域监督微调、来源匹配且多教师生成的思维链，以及采用动态采样的DAPO强化学习；这些环节是否对不同任务轴产生不同作用？

**实验实现**

所有阶段以Qwen3.5-9B为基础模型，在单个$8\times$H200节点上训练。监督微调使用QLoRA，覆盖注意力层与MLP的全部投影，秩为$r=128$，学习率为$10^{-4}$，在67,427条训练语料上训练两个epoch。强化学习从SFT检查点出发运行100个DAPO更新步骤，采用非对称裁剪$(\varepsilon_{\ell},\varepsilon_h)=(0.20,0.28)$和KL系数$\beta=0.001$。评测覆盖GSMA开放电信排行榜的七个公开基准，表I报告各轴准确率及平均值；原文未说明解码参数、随机种子、重复运行次数、置信区间、统计显著性检验及排行榜测试集的具体规模。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除思维链或改用单一、来源无关的BadCoT，并在TeleMath与TeleLogs上比较SFT阶段 | NoCoT的TeleMath与TeleLogs准确率分别为$42.2\%$和$35.4\%$；BadCoT为$72.0\%$和$59.0\%$；论文的多来源、多教师SFT为$68.0\%$和$42.0\%$。因此，通用BadCoT在SFT即时成绩上反而高于论文方案，尤其TeleLogs高$17.0$个百分点。 | NoCoT与含思维链方案的差距说明，数学推导和规则诊断需要显式分配推理过程；但SFT阶段BadCoT更高也提醒读者，来源匹配思维链的优势并不是更高的初始准确率。该消融真正要检验的是初始化能否为后续验证器强化学习提供可利用的结构，不能仅凭SFT行宣称多来源方案已优于单教师方案。 | 表II，SFT only中的BadCoT行；NoCoT与Multi-source数值见同表相邻行<br><span class="experiment-evidence">BadCoT \| Single generic teacher, source-blind CoT \| 72.0 \| 59.0</span> |
| 固定100步DAPO训练，比较BadCoT SFT初始化与论文的多来源、多教师SFT初始化 | BadCoT初始化经DAPO后在TeleMath和TeleLogs上分别得到$65.2\%$和$72.9\%$；多来源初始化经相同100步DAPO后达到$75.0\%$和$75.0\%$，分别高$9.8$和$2.1$个百分点。 | 这一比较显示，SFT安装的推理骨架会影响后续强化学习能否继续改善策略：来源匹配、多教师轨迹虽然SFT即时分数未必更高，却在DAPO后得到更好的最终结果。作者将差距归因于教师多样性和验证器对齐结构；但该行同时改变了教师数量与来源匹配方式，因此不能严格区分两者各自的独立贡献。 | 表II，DAPO + 100 RL steps中的Multi-source行；BadCoT初始化结果见同表相邻行<br><span class="experiment-evidence">Multi-source SFT init, ours \| Axis-matched 4-quadrant generators, multi-teacher mixture \| 75.0 \| 75.0</span> |

**定性案例**

- 图3的TeleLogs案例比较了规则盲的前沿模型与TelecomGPT-R1-9B：前者观察到吞吐下降边界处发生PCI切换后选择C5，却没有检查定义C1所需的下倾角阈值与切换恢复符号；本文模型计算$m_{07}=-30.69\,\mathrm{Mbps}$和$m_{10}=23^{\circ}$，命中规则S5并恢复答案C1。该案例直观说明SFT所学的规则复演框架如何约束诊断步骤，但单个成功案例不能估计此机制在整个TeleLogs测试集上的普遍性。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：Develops a telecom-specialized LLM reasoner using chain-of-thought data and verifier-reward GRPO post-training.; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`17226315d4e43dd54c811b57e9efe6f7d4624ed2789f9ff38060241231cb97e4`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
