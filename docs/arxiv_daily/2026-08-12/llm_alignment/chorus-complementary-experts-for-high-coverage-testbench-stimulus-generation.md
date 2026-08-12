---
title: "[论文解读] CHORUS: Complementary Experts for High-Coverage Testbench Stimulus Generation"
description: "[arXiv 2608.10090][对齐 / RLHF] CHORUS把分阶段监督微调产生的多个中间检查点分别训练成能力互补的强化学习专家，再将这些专家合并或蒸馏为一个模型，以突破传统单模型后训练的性能上限。"
arxiv_id: "2608.10090"
announcement_date: "2026-08-12"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:09:02.447553+00:00"
source_sha256: "3ed0d9de1dc4aebbaefcc94053b507c9b4da7fc9ba9e6b1258434267bff62f70"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "硬件验证"
  - "测试平台激励生成"
  - "覆盖率"
  - "执行引导强化学习"
  - "分阶段监督微调"
  - "互补专家"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.10090</p>

# CHORUS: Complementary Experts for High-Coverage Testbench Stimulus Generation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Hejia Zhang, Sheng Lu, Zhongming Yu, Chia-Tung Ho, Brucek Khailany, Jishen Zhao</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Georgia Institute of Technology；NVIDIA</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.10090v1) · [PDF 下载](https://arxiv.org/pdf/2608.10090v1) · **关键词** 硬件验证, 测试平台激励生成, 覆盖率, 执行引导强化学习, 分阶段监督微调, 互补专家<br>


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

CHORUS把分阶段监督微调产生的多个中间检查点分别训练成能力互补的强化学习专家，再将这些专家合并或蒸馏为一个模型，以突破传统单模型后训练的性能上限。

**不用术语来说**：硬件芯片制造前需要用测试程序反复刺激待验证设计，尽可能触发各种内部行为；刺激程序覆盖得越全面，遗漏潜在设计问题的风险通常越低。生成这类程序可以通过仿真结果直接评分，但即使扩大通用大模型的规模，或只沿着一个微调后的模型继续强化学习，覆盖率仍可能提前饱和，因此需要更有效地利用紧凑模型中已经形成但分散存在的能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出一种新的后训练视角：不再只保留分阶段监督微调的最终检查点，而是对多个阶段检查点执行相同的、由仿真覆盖率引导的强化学习，将它们转化为总体性能接近但擅长不同设计任务的专家。
- 作者提出两种单模型整合路径：训练自由的权重合并用于低成本吸收部分互补能力；自适应多教师在线策略蒸馏则按任务执行奖励选择最佳专家，并在没有专家优于学生时跳过更新，以减少较差教师行为的迁移。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型辅助硬件验证与代码生成后训练的交叉研究。芯片制造前，验证工程师需要通过测试平台（testbench）向待验证设计施加输入激励，并在工业仿真器中观察信号、分支等行为是否被充分触发；本文关注的不是生成硬件设计本身，而是生成能够提高覆盖率的激励程序。由于候选程序可以被编译、仿真并获得客观覆盖率，执行反馈比文本模仿更可靠；但该反馈不可微，不能直接对覆盖率求梯度，因此通常先用监督微调（SFT）获得基础策略，再用基于标量执行奖励的强化学习（RL）继续优化。本文以开放的 4B 参数模型及 LLM4Cov 的三个分阶段 SFT 检查点为研究起点，考察这些检查点经过相同执行引导 RL 后是否保留互补的任务级能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**测试平台与覆盖率**

测试平台是驱动待验证硬件设计的可执行程序：它生成输入激励、运行设计，并记录哪些信号状态或控制分支已被触发。覆盖率 $c(x,y)\in[0,1]$ 是仿真器返回的行为覆盖比例，数值越高，表示候选测试平台探索到的设计行为越充分，但高覆盖率本身不等同于已经证明设计完全正确。

</div>
<div class="concept-item" markdown="1">

**执行引导强化学习**

模型生成代码后，由编译器和仿真器实际执行，再把编译状态、仿真状态或覆盖率等结果转换为奖励，用于更新生成策略。覆盖率是不可微的外部结果，因而不能像普通监督学习那样直接反向传播，只能依据采样结果的奖励高低调整策略。

</div>
<div class="concept-item" markdown="1">

**分阶段监督微调与互补专家**

分阶段 SFT 按不同训练阶段或课程逐步产生检查点；这些检查点参数相关，但行为并不完全相同。本文所称“互补专家”是指经过 RL 后总体性能相近、却分别擅长不同设计任务的模型，而不是简单指多个独立的大模型。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定待验证设计 $x$，输入包括设计源文件以及验证环境，如模块接口、参考或期望行为、编译与仿真工具链；模型需要输出候选测试平台 $y$，由它产生激励并驱动该设计。工业仿真器编译并运行 $y$，返回执行状态、日志以及覆盖率 $c(x,y)\in[0,1]$；论文将这一执行结果视为判断生成质量的可靠依据。生成可采用两种设置：直接生成在单次输出中完成测试平台；智能体式改进则把仿真反馈追加到上下文，在有限轮次内修订程序。本文固定沿用 LLM4Cov 的 SFT 流程，以其三个检查点 $\pi_0,\pi_1,\pi_2$ 为初始策略，研究相同执行引导 RL 如何将它们转化为任务级能力互补的专家，为后续整合到单一可部署模型提供基础。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

待验证的硬件设计及其验证环境。

</div>
<div class="notation-item" markdown="1">

**$y$**

模型为设计生成的候选测试平台或激励程序。

</div>
<div class="notation-item" markdown="1">

**$c(x,y)\in[0,1]$**

仿真器运行设计与候选测试平台后得到的覆盖率；越接近 1，表示触发的目标行为比例越高。

</div>
<div class="notation-item" markdown="1">

**$\pi_0,\pi_1,\pi_2$**

LLM4Cov 三阶段 SFT 课程留下的三个固定策略检查点，也是本文执行引导 RL 的不同初始化。

</div>

</div>

**直接相关的工作**

- **LLM4Cov**: 本文最直接的前序工作与实验起点。LLM4Cov 通过三阶段 SFT 课程训练覆盖率激励生成策略，并在 CVDP-ECov 上进行智能体式评测；CHORUS 不修改该 SFT 过程，而是保留其三个阶段检查点 $\pi_0,\pi_1,\pi_2$，研究它们经过相同执行引导 RL 后形成的互补性。
- **DAPO / CodeV-R1**: DAPO 是使用可验证奖励进行策略优化的强化学习方法，CodeV-R1 将相应训练方案用于代码领域。本文的 RL 阶段沿用 CodeV-R1 所采用的 DAPO 训练方案，因此论文贡献不在提出新的基础 RL 算法，而在揭示分阶段 SFT 初始化经过独立 RL 后仍能保留可利用的任务级异质性。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

高覆盖率测试台刺激生成直接服务于芯片制造前的功能验证：模型需要编写可执行刺激程序，驱动已有硬件设计，并以仿真覆盖率衡量触发行为的充分程度。该任务具有可执行、相对稠密但不可微的反馈信号，同时仍令前沿大模型感到困难；因此，实践需求不是一般意义上的代码模仿，而是利用实际执行反馈，让可部署的紧凑模型生成覆盖更全面的刺激。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **扩大通用或领域模型规模**：依赖增加参数量以及通用代码能力，希望更大的模型自然获得更强的硬件测试程序生成能力。论文以CVDP-ECov上的规模与通过率关系说明，这一任务仅呈现较弱的规模趋势。
- **单检查点的监督微调到强化学习流水线**：先通过分阶段监督微调获得一个最终模型，再选取通常表现最强的最终检查点，使用仿真执行反馈进行强化学习，使生成程序直接朝更高覆盖率优化；LLM4Cov之后继续对其最终检查点进行执行引导强化学习就是这种自然延伸。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 单纯扩大模型规模不能稳定解决该任务：作者指出通用、代码专用及硬件专用模型的性能与规模只有较弱关系，甚至671B参数的前沿模型仍低于该任务可达到的最佳表现。其后果是，仅依赖更大模型会带来高计算和部署成本，却未必补齐具体硬件设计上的覆盖缺口。
- 传统流水线只优化并部署一个监督微调检查点，强化学习最终会在某个性能上限附近饱和；与此同时，中间检查点因训练阶段不同而形成的行为差异被直接丢弃。即使分别训练多个专家，简单整合也可能把有价值的专长平均掉，或把某位教师在特定任务上的较差行为转移给最终模型。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚未解决如何把同一分阶段监督微调过程中的中间检查点系统地转化为多个“都足够强、但在任务层面仍有不同优势”的专家，并进一步把这些分散优势无损地压缩进一个可部署模型。关键缺口同时包含专家形成与专家整合：前者要避免共同强化学习目标抹平差异，后者要避免无差别平均或错误教师监督。

</div>
<div markdown="1"><span>核心问题</span>

在模型规模固定且单一检查点的执行引导强化学习已经趋于饱和时，能否利用分阶段监督微调检查点保留下来的行为多样性，训练出互补专家，并通过权重合并或按执行奖励路由的多教师蒸馏，得到一个性能超过所有单独专家的模型？

</div>
<div markdown="1"><span>作者直觉</span>

不同监督微调阶段像是从不同起点学习同一道题：后续使用相同的仿真奖励，可以把每个起点都提升为强模型，但起点造成的解题偏好未必完全消失，因此这些模型可能在平均成绩相近时分别擅长不同硬件设计。若先用实际覆盖率判断每项任务应向哪位专家学习，并在没有更好专家时不强行学习，就有机会只吸收各专家的长处；权重合并则提供一种无需额外训练、但选择性较弱的近似整合方式。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CHORUS 的输入不是单个监督微调模型，而是同一基础模型经过分阶段监督微调（staged SFT）得到的三个检查点 $\pi_0,\pi_1,\pi_2$。方法先以完全相同的数据、预算和执行反馈强化学习流程分别训练它们，得到三个总体能力接近、但在具体硬件设计上各有所长的专家 $\pi_0^{\mathrm{RL}},\pi_1^{\mathrm{RL}},\pi_2^{\mathrm{RL}}$。每个专家同时学习两种工作模式：直接从设计描述生成测试平台，以及根据仿真反馈修复低覆盖率测试平台；二者统一由基于编译、仿真和覆盖率的奖励驱动。
随后，CHORUS 将专家互补性整合进一个可部署模型。低成本方案直接在权重空间平均专家；主要方案则从一个较强 RL 专家初始化学生 $\pi_\theta$，对每个设计在线比较所有教师与学生的执行奖励，只选择当前任务上最强且确实优于学生的教师进行在策略蒸馏，否则跳过该任务。技术上，这是“按实例动态路由 + 奖励门控 + 学生自身轨迹蒸馏”；直观上，它像让学生逐题向最会做该题的老师学习，同时拒绝比自己更差的示范，从而把多个专家的长处压缩到单个 4B 模型中。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造同源的分阶段 SFT 初始化

保留不同 SFT 阶段形成的行为差异，并将三个检查点作为后续独立 RL 训练的固定初始化；后续三次训练使用相同数据、目标和预算，使初始化成为唯一受控变量。

<div class="method-step__io" markdown="1">

**输入**：同一模型谱系中的三个分阶段 SFT 检查点 $\pi_0,\pi_1,\pi_2$，分别对应 Stage-0、Stage-1 和 Stage-2。<br>
**输出**：三个参数结构一致、可独立强化学习且可进行权重合并的初始策略。

</div>

**直观理解**：这相当于保留同一名学生在三个学习阶段的版本，再让它们接受完全相同的强化训练，以观察不同起点会形成哪些不同专长。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 联合训练直接生成与反馈修复

每个训练步骤混合直接生成与 agentic refinement 轨迹组；修复模式从组内覆盖率最低的候选状态继续生成，并用统一的仿真奖励和 DAPO 更新同一策略。

<div class="method-step__io" markdown="1">

**输入**：一个 SFT 初始化策略、硬件设计 $x$、直接生成任务，以及包含候选测试平台和执行反馈的修复任务。<br>
**输出**：一个同时支持从零生成和依据反馈迭代修复的 RL 专家 $\pi_k^{\mathrm{RL}}$。

</div>

**直观理解**：模型既练习“第一次就写好”，也练习“看到失败结果后修改”；修复时优先处理最差答案，把训练资源用于覆盖缺口最大的地方。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 形成并验证互补 RL 专家

分别从 $\pi_0,\pi_1,\pi_2$ 运行独立 RL，得到 $\pi_0^{\mathrm{RL}},\pi_1^{\mathrm{RL}},\pi_2^{\mathrm{RL}}$；通过逐设计执行结果识别它们在总体性能相近情况下的任务级差异。

<div class="method-step__io" markdown="1">

**输入**：三个 SFT 检查点及同一套执行引导 RL 流程。<br>
**输出**：一个可供静态合并或动态蒸馏使用的互补教师池 $\{\pi_t\}$。

</div>

**直观理解**：三位专家的平均成绩可能接近，但答对的题目并不完全重合；CHORUS 利用的正是这种“分数相近、会做的题不同”。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 整合专家能力

训练免费路线对专家参数做 Model Soup 平均；主要路线在每个设计 $x$ 上执行所有教师和学生，选择奖励最高的教师 $t^*$，仅当其奖励严格高于学生时应用在策略蒸馏损失。

<div class="method-step__io" markdown="1">

**输入**：三个 RL 专家，以及从一个 RL 专家初始化的学生策略 $\pi_\theta$。<br>
**输出**：静态权重合并模型，或经自适应多教师 OPD 训练得到的单一学生模型。

</div>

**直观理解**：权重平均像把三份解题经验一次性混合；自适应蒸馏则逐题选老师，而且只有老师确实更强时才学习，因此更能保留任务相关的专长。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 执行与覆盖率奖励

$$
R(x,y)=\begin{cases}1+c(x,y),&\text{if }y\text{ runs and yields coverage},\\0,&\text{otherwise}.\end{cases}
$$

**符号说明**

- $x$：待验证的硬件设计。
- $y$：模型生成的候选测试平台或测试刺激程序。
- $c(x,y)$：候选测试平台在设计上取得的覆盖率比例。
- $R(x,y)$：由编译、仿真和覆盖率共同确定的标量奖励。

<div class="equation-explanation" markdown="1">

**直观理解**：该奖励先用是否可执行建立硬边界：不能编译、不能仿真或不能产生覆盖率的候选得 $0$；可执行候选至少得 $1$，再按覆盖率增加奖励，完全覆盖时得 $2$。这样，训练既不会把“代码能运行”和“代码直接失败”混在一起，又能在可运行候选之间持续区分覆盖质量。<br>
**原文位置**：第 3.1 节，公式 (1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 奖励门控的自适应多教师蒸馏目标

$$
t^{*}=\arg\max_{t}R(\pi_t,x),\qquad \mathcal{L}(x)=\begin{cases}\mathcal{L}_{\mathrm{OPD}}\!\left(x;\pi_{t^{*}}\right),&R(\pi_{t^{*}},x)>R(\pi_{\theta},x),\\0,&\text{otherwise}.\end{cases}
$$

**符号说明**

- $t$：教师池中的专家索引。
- $\pi_t$：第 t 个 RL 教师策略。
- $t^{*}$：在当前设计上取得最高执行奖励的教师索引。
- $\pi_{\theta}$：参数为 θ、待整合专家能力的学生策略。
- $R(\pi,x)$：策略 π 在设计 x 上生成轨迹后得到的执行奖励；原文以该记号概括策略 rollout 的评分。
- $\mathcal{L}_{\mathrm{OPD}}(x;\pi_{t^{*}})$：在设计 x 上以最佳教师为目标的在策略蒸馏损失。
- $\mathcal{L}(x)$：设计 x 对本次学生更新贡献的最终损失。

<div class="equation-explanation" markdown="1">

**直观理解**：公式先逐任务选择当前奖励最高的教师，再检查它是否严格强于学生；只有两个条件同时满足，学生才接受蒸馏。其关键不是简单集成多个教师，而是把执行器变成在线裁判，使教师选择随任务和学生能力变化，并让无优势教师对应的样本贡献零梯度。<br>
**原文位置**：第 3.4 节，公式 (3)；最佳教师定义紧邻公式之前

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：专家训练阶段以公式 (1) 的执行奖励评价同一设计 $x$ 下的 $G$ 条轨迹 $\{y_i\}$，并计算组相对优势 $\hat A_i=(R(x,y_i)-\operatorname{mean}_j R(x,y_j))/\operatorname{std}_j R(x,y_j)$。随后使用 token 级 DAPO 截断代理目标更新策略：每个 token 的新旧策略概率比与组优势相乘，并用非对称上下界 $\varepsilon_{\mathrm{lo}}<\varepsilon_{\mathrm{hi}}$ 限制单次更新；该配置不对 SFT 初始化施加 KL 惩罚，也不使用动态采样。直接生成和反馈修复共享这一目标，因此奖励只关心最终测试平台能否执行及达到何种覆盖率。
整合阶段不再仅优化同一策略的自奖励，而由公式 (3) 决定哪些任务进入 v-OPD。学生在自己的在策略轨迹上接收面向最佳教师的反向 KL 学习信号，控制变量用于降低采样梯度方差；奖励门控决定“向谁学以及是否学习”。原文将 v-OPD 的完整数学形式放在附录 C，所给节选未包含该公式，因此这里不补写未提供的表达式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 执行反馈驱动的联合 RL**

同一策略 $\pi_\theta$ 同时处理直接生成和 agentic refinement。候选测试平台必须通过编译与仿真并产生覆盖率才获得正奖励；组内轨迹通过相对标准化优势参与 token 级 DAPO 更新，修复轨迹采用最低覆盖率状态作为下一轮起点。

> 直观理解：硬件验证可以实际运行生成代码，因此训练信号不依赖文字风格是否像参考答案，而直接判断代码能否运行、覆盖了多少行为。把两种推理模式放进同一策略，也避免部署时维护两个模型。

**2. 同源专家的权重空间合并**

Model Soup 对三个 RL 专家的对应参数做均匀平均；论文还比较了 DARE-TIES 和 DELLA，它们先稀疏化参数增量并协调增量符号，以减少专家更新之间的干扰。由于专家来自共同的 SFT 谱系且结构相同，其参数具有直接对齐和合并的条件。

> 直观理解：该模块检验不同专家的能力是否能通过简单参数平均叠加。它不需要额外训练，但对所有任务使用同一固定组合，无法根据当前设计决定更应依赖哪位专家。

**3. 奖励门控的自适应多教师 OPD**

对每个设计 $x$，系统用统一执行奖励比较教师池 $\{\pi_t\}$ 与学生 $\pi_\theta$，动态选择 $t^*=\arg\max_t R(\pi_t,x)$。若最佳教师优于学生，则在学生自身采样的轨迹上使用方差缩减在策略蒸馏（v-OPD），以采样 token 的反向 KL 信号靠近教师，并以学生 top-$K$ 词表支持上的停止梯度控制变量降低方差；否则该任务不产生梯度。

> 直观理解：教师不是按预设题型固定分工，而是每道题现场比试后再选。门控避免学生模仿较差答案，跳过规则则防止已经学会的任务继续接受无效 RL 更新而干扰教师监督。

**训练与推理**

训练分为两段。第一段从三个 SFT 初始化分别运行相同的 RL：训练批次混合直接生成轨迹组与两轮式反馈修复轨迹组；对修复组选择覆盖率最低的候选作为后续状态；所有候选经电子设计自动化工具编译、仿真并测量覆盖率，所得奖励用于 DAPO 更新。三次训练互不共享参数，最终构成教师池。作为无需再训练的整合方式，可以直接均匀平均三个专家权重；作为主要方式，则从最佳 SFT 阶段对应的 RL 专家初始化学生，在每个训练批次中分别采样教师与学生输出、执行评分、按任务选择最佳教师，并只对教师胜出的样本执行 v-OPD 更新。
推理时，最终交付的是一个合并后或蒸馏后的单模型，不需要同时部署教师池。它可在 direct inference 中从硬件设计直接生成测试平台，也可在 agentic 模式中读取编译、仿真和覆盖率反馈后继续修复候选；教师比较与奖励门控只用于后训练，不是最终推理的必需组件。

**复现信息**

公平解释专家差异所需的关键设置是：三个初始化均来自已发布的 LLM4Cov Qwen3-4B Stage-0、Stage-1 和 Stage-2 检查点，每个专家使用同一份 RL 数据、目标、训练预算和超参数，因而可将最终任务级差异主要归因于 SFT 初始化。每次 RL 运行包含 $1000$ 次更新，使用 Adam、恒定学习率 $10^{-6}$、每提示 $4$ 个样本、全局批量 $16$、最多 $2$ 轮 agentic refinement，以及 DAPO 截断参数 $\varepsilon_{\mathrm{lo}}=0.2$、$\varepsilon_{\mathrm{hi}}=0.28$；KL、熵和权重衰减系数均为 $0$，动态采样关闭。来源：附录 B.1、表 4。
计算成本方面，每个独立 RL 运行使用 $2$ 张 NVIDIA H100 PCIe GPU，约需 $50$ 小时，即约 $100$ GPU-hours；自适应 OPD 从一个 RL 专家继续训练，并在论文比较中采用相同的 $100$ 步运行窗口。权重平均无需额外训练；DARE-TIES 与 DELLA 依赖基模型定义参数增量，因此结果会受基模型选择影响。v-OPD 的 top-$K$、教师与学生 rollout 聚合细节以及附录 C 的完整损失形式未出现在所给节选中，应在复现前回查原文。来源：附录 B.1、第 3.3 至 3.4 节及第 5.4 节。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- CVDP-ECov 是主要评测集，包含 83 个由 CVDP 改造而来的硬件代码仓库；每个任务的覆盖率达标阈值由人类专家设定。它更接近复杂、跨文件的实际硬件验证场景，主要用于检验模型生成的测试平台激励能否达到工程上认可的覆盖目标。
- AutoEval-ECov 是辅助评测集，包含 156 个由 VerilogEval 按 CorrectBench 方法构造的任务，所有任务均要求达到 100% 覆盖率。其设计规模较小、阈值更严格，用于检查结论能否延伸到单模块设计，但论文不把它作为主要排名依据。
- CodeV-R1-11kRTL 的训练划分包含 11,488 条记录，用于全部强化学习与在线策略蒸馏训练。作者仅保留 RTL 长度超过 1,000 个 token 且恰有一个候选顶层模块的设计，以集中训练复杂 RTL 问题并排除顶层模块含糊的样本；该数据不用于报告最终泛化成绩。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Pass@1**

对每个任务的 5 个独立样本分别判断覆盖率是否达到任务阈值，再在全部任务和样本上求成功比例；因此这里的“@1”是单次生成的平均成功概率，而不是只评测一个固定样本。编译、仿真或覆盖率报告失败均按 0% 覆盖率处理。 （越高越好，因为它直接衡量一次部署生成达到覆盖门槛的概率；论文的首要指标是 CVDP-ECov 在智能体迭代模式下的 Pass@1。）

</div>
<div class="metric-item" markdown="1">

**Pass@5**

每个任务生成 5 个样本，只要其中至少一个样本达到该任务的覆盖率阈值，就将任务计为成功，然后对任务求平均。它衡量允许多次尝试时的任务解决率。 （越高越好；但它允许从多个候选中选择最佳者，部署成本高于 Pass@1，因此主要作为候选多样性和搜索潜力的辅助证据。）

</div>
<div class="metric-item" markdown="1">

**Coverage@1 / Coverage@5**

Coverage@1 对所有任务和独立样本的实际覆盖率求平均，Coverage@5 则先取每个任务 5 个样本中的最高覆盖率再求平均。它们能够区分“未达阈值但接近成功”和“完全失败”，补充二值化的 Pass 指标。 （越高越好，因为更高覆盖率表示生成激励触达了更多硬件行为；不过覆盖率提升未必跨过任务阈值，所以不能替代 Pass@1。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

原文未明确报告，或自动提取阶段未获得可靠数据。

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- DeepSeek-R1（671B）代表大规模通用推理模型。它与 CHORUS 的 4B 模型形成参数规模悬殊的比较，用于判断硬件专用后训练能否胜过依靠大模型容量和长推理输出的通用方案。
- LLM4Cov Stage-2 是此前面向测试平台覆盖率生成的硬件专用方法，也是 CHORUS 所使用分阶段 SFT 检查点的来源。与它比较可检验增益是否来自后续强化学习和专家整合，而不只是已有监督微调流程。
- 三个独立 RL 专家分别从 LLM4Cov 的 Stage-0、Stage-1 和 Stage-2 SFT 检查点初始化，并使用完全相同的 DAPO 配置训练。它们既是单模型基线，也是研究初始化影响和专家互补性的受控对象。
- 三个专家的 oracle union 是分析性上界：只要任一专家解决某个设计，就把该设计计为成功。它不是可部署模型，而是估计现有专家集合中已经存在、理论上可由路由或整合方法回收的性能空间。

**实验想回答的问题**

- 分阶段监督微调得到的不同初始化，在采用相同的执行反馈强化学习后，是否仍会形成不同的性能上限，还是会收敛到相近的总体成绩？
- 当多个强化学习专家总体成绩相近但逐任务优势不同，这种互补性是否足以支持 CHORUS 通过专家整合超过任一单独专家及现有大模型基线？

**实验实现**

主要评测采用智能体迭代模式：每个任务进行 3 轮交互，生成 5 个样本，温度为 0.7，top-$p$ 为 0.8；同时报告单次直接推理作为辅助设置。Qwen3-4B 系列模型的回答上限为 16,384 token，API 基线使用 Google API 暴露的模型特定最大长度，因此不同模型的输出预算并不完全一致。硬件代码由 Cadence Xcelium 22.03-s001 编译和仿真，并由 Cadence IMC 25.09-a001 计算覆盖率，运行环境为 Rocky Linux 8.9。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The central contribution is an SFT, reinforcement-learning, and expert-consolidation post-training framework for improving LLM code-generation reasoning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`3ed0d9de1dc4aebbaefcc94053b507c9b4da7fc9ba9e6b1258434267bff62f70`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
