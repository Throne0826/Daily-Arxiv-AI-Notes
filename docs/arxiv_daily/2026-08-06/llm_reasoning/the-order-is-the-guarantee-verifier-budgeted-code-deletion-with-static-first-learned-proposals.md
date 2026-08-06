---
title: "[论文解读] The Order Is the Guarantee: Verifier-Budgeted Code Deletion with Static-First Learned Proposals"
description: "[arXiv 2608.04611][LLM Reasoning] 本文将冗余代码删除重新表述为有限执行验证预算下的候选调度问题：学习模型负责扩展候选搜索，确定性的候选顺序约束模型失误，而测试套件保留对每次删除的最终否决权。"
arxiv_id: "2608.04611"
announcement_date: "2026-08-06"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-06T07:05:31.642917+00:00"
source_sha256: "07a4846e12727d5fa3eefdb54a1457d6e619cf807c53c03f59291115693beb88"
tags:
  - "LLM Reasoning"
  - "冗余代码删除"
  - "提案调度"
  - "执行验证"
  - "验证预算"
  - "静态分析"
  - "学习排序"
  - "分布偏移"
  - "行为保持"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.04611</p>

# The Order Is the Guarantee: Verifier-Budgeted Code Deletion with Static-First Learned Proposals

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-06</span>
<span><strong>作者</strong> Ruitong Li, Binjie Guo, Aisheng Mo, Guowei Su, Han Wang, Jie Li, Ru Zhang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.04611v1) · [PDF 下载](https://arxiv.org/pdf/2608.04611v1) · **关键词** 冗余代码删除, 提案调度, 执行验证, 验证预算, 静态分析, 学习排序, 分布偏移, 行为保持<br>


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

本文将冗余代码删除重新表述为有限执行验证预算下的候选调度问题：学习模型负责扩展候选搜索，确定性的候选顺序约束模型失误，而测试套件保留对每次删除的最终否决权。

**不用术语来说**：生成式编程往往不断加入分支、保护条件和后备逻辑，却很少清理已经失去作用的代码；这些代码即使不影响当前测试，也会扩大审查范围、掩盖程序应保持的规则并积累技术债。删除又比添加更危险，因为误删可能破坏必要行为，而实际系统只能测试有限数量的删除方案，因此关键不只是找出“可能多余”的语句，还要决定先验证哪些候选。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者把冗余代码削减形式化为有限验证预算下的提案调度，明确分离“候选生成与排序”和“执行测试后接受删除”两个职责，从而把可部署的控制变量从不可靠的模型置信度转向可审计的候选顺序。
- 作者提出两种依据可用证据选择的静态优先调度：有代表性目标域验证数据时，用验证支持的静态—学习混合顺序提高候选互补性；没有此类数据时，保留完整静态前缀并仅追加学习候选，使确定性验证器下的覆盖率和字符削减不会因学习排序而下降。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于软件工程中的程序化简、生成并验证式程序修复与神经代码模型的交叉处。传统程序化简通过反复执行测试来判断删除是否保持目标行为，编译器和静态分析工具则能可靠识别不可达代码、未使用绑定等可证明无用的成分；但对于仍可达、仍被引用、其作用却已被其他逻辑覆盖的语句，例如重复的条件保护、归一化操作或过时回退，仅靠静态证明通常难以发现。本文因此研究“由模型提出或排序、由执行测试最终裁决”的代码删除，并把有限验证资源下的候选顺序视为核心控制变量：测试套件决定何为行为保持，候选调度决定有限预算内能检查哪些删除。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**执行验证器**

执行验证器是运行相关测试套件并判断修改后程序是否全部通过的机制。本文只提交通过验证的删除，因此模型分数用于安排检查顺序，而不是充当正确性证明。

</div>
<div class="concept-item" markdown="1">

**静态分析与静态排序**

静态分析不运行程序，而是依据语法、引用关系和控制流等信息判断代码性质；其优势是确定、可审计，但通常只能覆盖可证明无用的代码。本文的静态排序优先考虑较短语句和零引用候选，为学习排序提供稳定基线。

</div>
<div class="concept-item" markdown="1">

**提案调度与验证预算**

提案调度是对单语句删除候选规定验证次序，验证预算则限制最多可执行测试的候选数量。预算有限时，学习候选若占据静态候选的位置，可能提高搜索覆盖，也可能在分布偏移下挤掉本可成功的静态删除。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是待简化程序$x$及其相关执行测试套件；系统从程序抽象语法树中构造单语句删除候选集合$C(x)$，再由确定性静态规则或学习排序器生成候选顺序$\pi$。验证器按$\pi$依次测试删除后的程序，并提交第一个通过全部测试的删除；若预算内没有候选通过，则保持原程序不变。该设置假定测试执行是最终接受边界，并且可用验证次数有限；它不声称测试通过等价于完整语义等价，而是把测试套件视为部署环境中的操作性行为规范。研究关注的不是一次生成任意重构，而是在静态候选与学习候选之间分配有限验证槽位，使已验证删除的任务覆盖和字符缩减尽可能高，同时控制学习排序失准或跨域偏移造成的损失。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

需要检查并尝试删除冗余语句的输入程序。

</div>
<div class="notation-item" markdown="1">

**$C(x)$**

从程序$x$的抽象语法树提取出的单语句删除候选集合。

</div>
<div class="notation-item" markdown="1">

**$\pi$**

提交给执行验证器的有序候选序列，即删除提案的调度顺序。

</div>
<div class="notation-item" markdown="1">

**$|\pi|$**

候选调度包含的验证槽位数；它受执行验证预算约束。

</div>

</div>

**直接相关的工作**

- **Delta Debugging 与 Hierarchical Delta Debugging**: 这些方法通过反复执行测试来定位可删除或与故障相关的程序片段，奠定了“搜索负责提出修改、可执行判据负责接受修改”的范式。本文继承执行验证原则，但研究的是冗余代码删除，并将重点从迭代到局部最小程序转为小型固定预算下不同排序器之间的候选分配。
- **编译器死代码消除与现代代码检查器**: 这类工具可可靠删除不可达代码、未使用绑定或未使用导入等能够静态证明无用的成分，是本文静态候选与排序基线的来源。其覆盖边界在于难以识别仍可达、仍被引用但行为已由其他实现涵盖的语句；本文以学习排序扩展这部分搜索空间，同时保留执行测试的否决权。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

大模型降低了生成可运行代码的成本，却没有同步解决代码维护问题。在反复提示、修补和重新生成的工作流中，新实现通常叠加在旧脚手架之上，使废弃分支、重复归一化、冗余保护条件和过时后备逻辑继续存在。项目因此需要自动发现可删除代码，但执行测试具有现实成本，系统不可能验证所有单语句删除候选；同时，任何未经充分验证的误删都可能移除必要功能、安全检查、日志或罕见行为。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **静态分析与确定性短候选优先排序**：编译器、静态分析器或检查工具依据不可达、未引用等可证明属性识别安全删除项；对于仍需执行验证的候选，可以按删除语句较短或零引用等确定性规则排序。这类方法行为稳定、便于审计，但主要覆盖能够从程序结构直接判断的冗余。
- **学习式候选排序**：学习模型结合程序上下文，为单语句删除候选估计其通过测试或实现有效削减的可能性，并优先提交高排名候选给执行套件。它有机会发现静态规则难以识别的行为性冗余，例如功能已被其他代码涵盖但仍然可达、也仍被引用的保护条件或后备逻辑。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 静态分析擅长处理可证明不可达或未使用的代码，却难以识别“结构上仍活跃、行为上已被其余实现覆盖”的冗余；因此单独依赖静态规则会遗漏需要上下文语义判断的删除机会。
- 学习排序分数不是语义正确性的证明，而且可能在分布变化时失准。在固定验证预算内，学习候选若替换了原本会通过测试的静态候选，就可能降低成功删除覆盖率；即使候选通过测试，也只能说明其满足当前测试所表达的规范，不能保证保留未被测试覆盖的行为。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有思路分别提供了稳定但覆盖有限的静态候选，以及覆盖可能更广但受分布偏移影响的学习候选，尚缺少一种能在有限验证次数内组合二者、明确说明何时可以交换静态验证槽位，并在缺乏目标域证据时仍能给出不劣于静态基线保证的部署机制。

</div>
<div markdown="1"><span>核心问题</span>

在执行测试次数受限的条件下，应如何安排静态候选与学习候选的验证顺序，使系统尽可能找到可通过测试的代码删除，同时防止失准的学习排序挤占可靠静态候选，并始终把删除决定交给执行验证器？

</div>
<div markdown="1"><span>作者直觉</span>

候选顺序是部署方可以直接控制和审计的，而模型置信度既可能校准不足，也会随数据分布改变。有目标域验证证据时，可以让少量学习候选替换静态排序尾部，以利用两类候选的互补性；没有证据时，则先完整尝试静态前缀，只有全部失败后才追加学习候选。这样，模型只负责扩大搜索范围，错误排名最多增加验证开销，而不会夺走静态方法原本能够获得的成功删除。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

DELSCOUT把冗余代码删除建模为“受验证预算约束的候选排序”，而不是让模型直接改写程序。输入是一个已通过基准执行套件的 Python 程序 $x$；系统先枚举所有可单独删除的完整 AST 语句，分别生成确定性的静态次序 $S(x)$ 和学习得到的次序 $M(x)$，再按部署条件组成固定预算混合日程 $\pi_{\mathrm{mix}}$ 或前缀保留日程 $\pi_{\mathrm{aug}}$。调度器从左到右逐个执行删除实验，只有当删除后的程序能够编译并通过指定测试套件时才接受，并在首个成功候选处停止；最终输出至多包含一次单语句删除的程序以及完整审计记录。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成单语句删除候选

用标准库 AST 解析 $x$，枚举导入、赋值、函数与类定义、控制流语句、上下文管理器和表达式等完整语句的源码跨度；每个候选 $c\in C(x)$ 由起始行、结束行和节点类型唯一标识。候选编辑 $x\setminus c$ 只删除该语句覆盖的完整行，不能编译的编辑不会被视为成功。

<div class="method-step__io" markdown="1">

**输入**：通过原始执行套件的 Python 程序 $x$。<br>
**输出**：语法上可定位且可独立执行删除的候选集合 $C(x)$，以及每个候选对应的确定性源码跨度。

</div>

**直观理解**：系统只允许一次拿掉一块完整的语句，类似逐件检查哪些零件可以拆除；这样每次测试的成败都能明确归因于唯一一次编辑。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造静态与学习排序

静态排序采用最短优先或零引用优先：前者依次按行跨度、字符数、源码位置和候选键排序，后者先偏好文件中标识符出现频率较低的语句，再偏好较短跨度。学习排序器读取节点类型、跨度、候选文本及其前后各至多 24 行编号上下文，以成功边际 $z_\theta(x,c)$ 对所有候选排序，并用候选键确定性地打破同分。

<div class="method-step__io" markdown="1">

**输入**：候选集合 $C(x)$、每个候选的文本与 AST 类型，以及候选周围的源码上下文。<br>
**输出**：覆盖同一候选空间的静态有序列表 $S(x)$ 和学习有序列表 $M(x)$。

</div>

**直观理解**：静态规则擅长发现短小或与其他代码联系很弱的残留，模型则比较上下文以发现表面合理、实际上可能被其他控制流覆盖的语句；两者是互补的搜索工具，而不是两个可以互换的安全判定器。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按部署契约组成候选日程

有代表性验证数据时，固定五槽日程先放入前三个静态候选，再放入两个不与其重复的学习候选；缺少此类验证时，先完整保留五个静态候选，再追加至多 $B$ 个去重后的学习候选。去重是稳定的：若静态与学习次序指向同一源码跨度，静态候选保留原槽位，学习列表继续寻找后续未重复候选。

<div class="method-step__io" markdown="1">

**输入**：静态次序 $S(x)$、学习次序 $M(x)$、学习尾部预算 $B\leq 2$，以及是否拥有代表性目标域验证数据这一条件。<br>
**输出**：固定长度为 5 的 $\pi_{\mathrm{mix}}(x)$，或长度不超过 $5+B$ 的 $\pi_{\mathrm{aug}}(x)$。

</div>

**直观理解**：固定预算方案用两个模型候选替换部分静态机会，因此可能找到新删除，也可能挤掉原本会成功的静态候选；保守方案则先把原有五次机会全部执行完，再额外尝试模型建议，所以模型排错最多浪费附加验证次数，不会破坏原静态覆盖。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 事务式验证并提交首个成功删除

调度器从左到右复制源码、删除候选的完整行跨度、编译，并在隔离进程中运行该领域指定的执行套件；失败补丁立即丢弃，首个满足 $V(x\setminus c_j)=1$ 的补丁被提交，后续候选不再测试。若原程序不能通过同一套基准测试，则该任务不具备评估资格。

<div class="method-step__io" markdown="1">

**输入**：物化完成的有序日程 $\pi(x)=(c_1,\ldots,c_m)$、原程序 $x$ 和确定性领域验证器 $V$。<br>
**输出**：首个通过验证的单语句删除程序，或在预算耗尽时保持原程序不变；同时记录候选次序、验证调用和提交结果。

</div>

**直观理解**：排序器只决定“先试谁”，没有权力直接宣布删除安全；最终修改必须经过真实编译和测试，这相当于让模型提出实验顺序，而让执行结果保留否决权。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 两种预算候选日程

$$
\begin{aligned}\pi_{\mathrm{mix}}(x) &= S_3(x)\,\Vert\,M^{S_3(x)}(x), &|\pi_{\mathrm{mix}}|&=5,\\ \pi_{\mathrm{aug}}(x) &= S_5(x)\,\Vert\,M^{S_5(x)}(x), &|\pi_{\mathrm{aug}}|&\leq 5+B,\quad B\leq2.\end{aligned}
$$

**符号说明**

- $x$：待检查的程序。
- $S_k(x)$：静态次序 $S(x)$ 的前 $k$ 个候选。
- $M^A(x)$：从学习次序 $M(x)$ 中依次取出不属于集合 $A$ 的候选；在式（4）中补足两个学习槽，在式（5）中至多取 $B$ 个。
- $\Vert$：保持各部分内部顺序的有序拼接。
- $B$：前缀保留日程允许追加的学习候选数量，文中限制为至多 2。
- $\pi_{\mathrm{mix}}$：三项静态加两项学习候选组成的固定五槽日程。
- $\pi_{\mathrm{aug}}$：完整五项静态前缀之后追加学习候选的日程。

<div class="equation-explanation" markdown="1">

**直观理解**：式（4）用相同的五次最坏情况预算换取模型带来的互补覆盖，但替换静态候选会产生分布偏移风险；式（5）通过增加至多两次验证保留完整静态前缀。由于执行遵循首个成功即停止，确定性验证器下，追加在尾部的模型候选不可能改变静态前缀原本已经成功的删除。<br>
**原文位置**：第 3 节，式（4）和式（5）；前缀性质见 Proposition 1

</div>

</div>

<div class="equation-block" markdown="1">

#### 验证删除质量的列表式目标与稳定项

$$
\begin{aligned}\mathcal{L}_{\mathrm{list}}(x)&=-\log\frac{\sum_{c\in P_x}\exp z_\theta(x,c)}{\sum_{c\in G_x}\exp z_\theta(x,c)},\\ \operatorname{BCE}(z,y)&=-y\log\sigma(z)-(1-y)\log(1-\sigma(z)),\qquad \sigma(z)=\frac{1}{1+e^{-z}},\\ \mathcal{L}(x)&=\mathcal{L}_{\mathrm{list}}(x)+\lambda\,\frac{1}{|G_x|}\sum_{c\in G_x}\operatorname{BCE}\!\left(z_\theta(x,c),y_{x,c}\right),\qquad \lambda=0.1.\end{aligned}
$$

**符号说明**

- $G_x$：程序 $x$ 的训练候选组，包含全部已验证正例和选取的负例，且 $|G_x|\leq8$。
- $P_x$：候选组中的验证正例集合，即 $P_x=\{c\in G_x:y_{x,c}=1\}$；没有正例的任务被丢弃。
- $y_{x,c}$：候选 $c$ 从程序 $x$ 删除后是否通过验证器的二值标签。
- $z_\theta(x,c)$：参数为 $\theta$ 的分类器对候选删除成功与保留两个输出 logit 的差，即成功边际。
- $\sigma$：把成功边际映射到零至一范围的 logistic 函数。
- $\lambda$：逐点二元交叉熵稳定项的权重，所有实验固定为 0.1。

<div class="equation-explanation" markdown="1">

**直观理解**：列表项不要求每个候选都得到校准准确的概率，而是推动模型把一组候选中的 softmax 权重集中到至少一个真实通过验证的删除上，这直接对应“尽早找到一次成功”的部署目标。列表损失不关心负例彼此如何排序，因此额外的二元交叉熵稳定分数尺度，并让失败候选保留 KEEP 方向的监督。<br>
**原文位置**：第 4.3 节，式（6）和式（7）；BCE 与 $\lambda$ 的定义紧随式（7）

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练单位是程序级候选组 $G_x$，而不是互相独立的语句样本。每组至多包含 8 个候选，保留该组全部验证正例 $P_x$ 并选择部分负例；若 $P_x=\varnothing$，该程序没有可学习的排序目标，因而被剔除。核心列表损失最大化模型分配给所有已验证可删除候选的总 softmax 质量，使训练直接服务于“在预算靠前位置放置至少一个成功候选”；权重为 $\lambda=0.1$ 的逐点 BCE 项则约束每个候选的成功边际，避免只优化正例集合总质量时负例分数尺度漂移。

论文还在保持式（7）形式不变的情况下比较三种证据组织方式：精确残差训练从 $G_x$ 中移除 $S_3(x)$，专门学习可能进入模型尾部的机会；效用训练将每个正例重复 $3+\min(5,\lfloor |c|/80\rfloor)$ 次，使较长且成功的删除获得 3 至 8 倍权重；任务边际训练只保留满足 $\tau(S_3,x)=\infty$ 的任务正信号，以贴近“补足静态排序失败任务”的目标。最后一种设计概念上最接近边际覆盖，却会在静态排序较强时丢弃大量正例，所以论文将其作为待比较目标，而不预设它必然更容易学习。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 异构静态候选排序器**

最短优先排序针对行跨度短、字符数少的语法残留；零引用排序利用文件内标识符频率寻找弱连接语句。二者均无训练参数、结果确定，并且具体使用哪个静态顺序由领域层面的比较决定，不借助学习模型的测试结果。

> 直观理解：许多遗留导入和赋值既短又少被引用，简单规则便能低成本地把它们提前；这为系统提供可复现的默认搜索前缀，也是前缀保留保证成立的基础。

**2. 验证效用学习排序器**

该模块是序列分类器，输入包含候选节点类型与跨度、候选源码以及前后各至多 24 行上下文，输出两个类别 logit 的差 $z_\theta(x,c)$。训练标签 $y_{x,c}\in\{0,1\}$ 完全来自在 MBPP 训练范围实际删除候选后的验证结果；提示、训练和检查点选择均不使用测试标签，部署时只执行候选排序，不执行模型生成的自然语言。

> 直观理解：模型学习的不是跨项目成立的语义等价，而是“在给定来源领域和验证套件下，哪种候选更值得优先做删除实验”；因此分数只是搜索线索，不能替代测试证据。

**3. 预算调度与前缀保护器**

固定预算混合日程在五个槽位内组合三个静态候选和两个学习候选；前缀保留日程则保持 $S_5(x)$ 为完全不变的前五项，只在其后追加学习尾部。对确定性验证器，后者使原本由 $S_5(x)$ 接受的候选及其接受位置保持不变，并使覆盖率与非负字符缩减量相对静态基线不下降，但不能保证测试套件未覆盖的行为仍保持不变。

> 直观理解：真正可审计的控制量是候选顺序，而不是模型声称有多自信；把静态列表完整放在前面，相当于锁住已有搜索能力，再把模型能力作为只可能增加成功机会的附加尝试。

**训练与推理**

训练阶段先在 MBPP 训练范围内，对每个程序的候选逐一实施删除并运行验证器，由真实执行结果产生 $y_{x,c}$；随后构造程序级候选组，使用列表式损失和逐点稳定项优化序列分类器。模型看到的是候选源码和局部上下文，不会看到测试标签；其输出被解释为领域与任务条件下的排序统计量，而不是独立于测试套件的语义安全概率。

推理阶段先为目标程序一次性生成全部候选和两个独立次序，再根据部署证据选择日程：若有代表性目标域验证，可采用固定五槽的 $\pi_{\mathrm{mix}}$；若无法确认学习排序在目标分布上的可靠性，则采用 $\pi_{\mathrm{aug}}$ 保留完整静态前缀。调度器物化并稳定去重列表后，逐项进行隔离、事务式的编译与执行测试，提交首个成功删除；模型分数本身从不触发提交，也不执行任何自然语言输出。

**复现信息**

复现时需要固定候选粒度、排序规则和验证协议：候选必须对应一个完整 AST 语句及其完整行跨度；最短优先按跨度、字符长度、源码位置和候选键依次打破平局，学习排序也用候选键作确定性同分处理。模型提示包含节点类型、跨度、候选文本以及前后各至多 24 行带编号上下文，并把不确定情况明确映射为 KEEP。

所有候选测试必须从未修改的原程序副本开始，不能让前一次失败编辑污染后续候选；每次测试均需先编译，再在隔离进程运行同一领域的指定套件。只有原程序已通过该套件的任务才可纳入评估。前缀不退化保证依赖验证器确定性和非负删除量，并且只保证相对于该测试套件的覆盖与字符缩减不下降，不代表未被测试的程序行为在语义上保持不变。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MBPP 是主要域内数据集：任务 601–974 用于生成训练标签，任务 511–600 构成互不重叠的验证集并用于检查点选择，任务 1–500 作为留出测试集；根据原程序能否通过基线测试，每次运行有 499 或 500 个合格程序。MBPP+ 进一步从中选出删除前能通过增强测试套件的 170 个程序，用于检验普通 MBPP 验证所接受的删除能否满足更强的行为规范。
- 分布迁移评测包括 DS-1000、HumanEval 和 BigCodeBench-Hard，分别有 866、164 和 148 个合格程序。实验把在 MBPP 上训练的 0.5B 排序器直接迁移到这些数据集，并使用各数据集的官方执行预言机；该部分用于检验学习排序替换静态排序时的域外可靠性，以及保留完整静态前缀能否提供不降级性质。
- HumanEval+ 由 EvalPlus 提供，共有 138 个合格程序。前缀保留策略在分布迁移结果之后设计，随后被冻结，并在 HumanEval+ 上仅评估一次且不做目标域调整；因此它承担更严格的域外确认角色，而不是参与策略选择。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accepted-deletion coverage**

成功找到至少一个通过指定执行预言机的单语句删除方案的合格任务比例；表 1 也以 accepted-task count 报告对应任务数。该指标衡量有限预算内能覆盖多少程序，而不表示删除在未测试输入上必然保持语义。 （越高越好，因为更多任务能在当前测试规范下完成经验证的代码删除。）

</div>
<div class="metric-item" markdown="1">

**Character reduction**

经验证并提交的删除使整个评测语料减少的字符比例，用于区分只删除短小、琐碎语句和能够删除较大代码片段的策略。 （越高越好，但必须与覆盖率共同解读；更大的删除量不能补偿大量任务无法删除或测试规范不足。）

</div>
<div class="metric-item" markdown="1">

**Verifier calls 与 accepted deletions per 1k calls**

前者统计执行验证器的总调用次数，后者统计每一千次调用获得的已接受删除数。由于找到首个成功候选后调度立即停止，这组指标同时反映验证成本和成功出现得是否足够靠前。 （在覆盖效果相当时 verifier calls 越低越好；每千次调用的已接受删除数越高越好。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### MBPP 域内九次匹配运行，覆盖 0.5B、0.6B 和 8B 排序器；static shortest-5 与三静态加二学习候选的五槽混合调度比较。

<div class="result-value" markdown="1">

作者报告九次配对比较全部有利于混合调度，单次增加 3–9 个已接受任务；全模型平均从 70.4 个增至 77.1 个，即增加 6.7 个任务、相对提升 9.5%，绝对覆盖率从 14.1% 增至 15.4%。

</div>

这说明在域内、预算严格匹配的条件下，学习候选放在静态核心之后可以稳定扩大有限搜索所覆盖的任务，而且收益没有明显依赖模型从 0.5B 扩大到 8B。该结果证明的是给定 MBPP 测试预言机下的调度收益，不证明删除对所有输入都语义等价，也不能单凭九次运行断言任意代码域中均有相同提升。

<div class="result-source" markdown="1">

来源：第 6.1 节；表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Thegainispositiveinallninematchedrunsandconsistentacrossmodelscales.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### MBPP 上共同的五提案预算，以 static shortest-5 对比三种 static-first 混合尾部；重点观察覆盖、字符缩减和验证成本。

<div class="result-value" markdown="1">

static shortest-5 接受 70 个任务、调用验证器 1,593 次，每千次调用接受 43.9 个删除，字符缩减 2.11%；utility 混合策略接受 83 个任务、调用 1,581 次，每千次调用接受 52.5 个删除，字符缩减 3.06%。相对静态基线，接受任务数提升 18.6%，调用量反而少 12 次，验证效率提升约 19.5%。

</div>

混合策略的收益不是通过额外调用验证器换来的：互补候选更可能较早成功，从而触发提前停止。utility 结果只是在本实验协议下形成最强观测点，不能证明 utility 权重在其他数据、预算或验证器下普遍最优。

<div class="result-source" markdown="1">

来源：表 2；第 6.2 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Mixture, utility 83 1,581 52.5 3.06%

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 更强测试预言机下的安全边界：170 个 MBPP+ 合格程序比较 static shortest-5 和全部三种混合策略，并以原始 MBPP 测试接受、但被 MBPP+ 拒绝的删除衡量弱测试造成的误接受。

<div class="result-value" markdown="1">

静态基线和三种混合策略在 MBPP+ 上都只接受 11 个删除，即覆盖率均为 6.47%；混合策略的字符缩减仅从 0.76% 增至 0.78%，而 base-only rejection 从 3 个增至 7 个。因此普通 MBPP 上的域内覆盖优势在增强测试下完全消失。

</div>

该结果表明调度只能决定先验证哪些删除，不能定义“行为保持”的真实含义；测试套件越弱，越可能接受只是在有限样例上碰巧通过的删除。混合策略提出了更多有挑战性的控制流删除，也更容易暴露弱预言机的缺口。这里不能推导学习候选本身总是不安全，只能说明任何安全结论都受指定测试预言机约束。

<div class="result-source" markdown="1">

来源：第 6.5 节；表 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Amongthe 170programsthat pass the stronger suite beforedeletion,thefive-candidateshortest-firstbaselineandallthreestatic-firstmixturesacceptexactly 11deletions,thatis6.47%coverage,andthemixturesraisebase-onlyrejections—patchesacceptedbytheoriginalMBPPtestsbutrejectedbyMBPP+—from 3to7.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 原文未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Static shortest-5：按待删除语句长度从短到长排列，并最多验证五个候选。它与混合策略具有相同的五提案预算，因而能直接判断学习候选带来的覆盖率提升是否只是购买了更多验证机会。
- 局部最强完整静态排序：在 DS-1000 和 HumanEval 上采用 zero-reference 静态顺序，在 BigCodeBench-Hard 上采用 shortest-first，并完整执行五个静态候选。它是分布迁移时的可靠性参照，也是前缀保留策略承诺不降低覆盖率的基准。
- Learned-only rankings：分别使用候选特征逻辑回归、listwise 排序和 utility 排序直接决定候选次序。它们与静态基线的比较用于检验学习排序能否独立迁移，而不是依赖静态前缀保护。
- Static-first mixtures：前三个位置使用确定性的 shortest-first 静态候选，后两个位置分别接候选特征逻辑回归、listwise 或 utility 排序产生的互补候选。三种尾部排序之间的比较用于判断收益是否依赖某个特殊学习目标。

**实验想回答的问题**

- 在固定的五次候选提案预算下，先执行三个确定性静态候选、再执行两个学习候选的 static-first 混合调度，能否跨模型规模和重复运行稳定提高通过执行验证的代码删除覆盖率，同时不增加验证器调用量？
- 收益究竟来自特定学习目标，还是来自静态候选与学习候选的互补排序；当分布发生变化或测试套件增强时，完整保留静态前缀的调度能否避免覆盖率下降，其验证成本和安全边界又是什么？

**实验实现**

域内实验采用 Qwen2.5-0.5B、Qwen3-0.6B 和 Qwen3-8B 排序器，并通过 LoRA 适配器训练；三个模型规模合计进行九次独立匹配运行。部署比较统一使用五提案预算：静态基线检查五个 shortest-first 候选，混合策略检查三个静态候选后再检查两个学习候选，首个通过测试的候选被接受并提前停止。模型和静态策略在同一任务、同一预算及同一执行预言机下配对比较。域外实验使用 MBPP 训练的 0.5B 排序器；前缀保留增强先完整执行五个静态候选，仅在全部失败后追加学习候选。论文明确将迁移数据上的增强结果标为探索性分析；HumanEval+ 则使用冻结策略，且因复用的标准验证日志没有记录全部失败的次级候选，其增强结果是保守下界。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 分布迁移下比较 learned-only 替换与 prefix-preserving augmentation：后者先执行完整五候选静态前缀，全部失败后才追加学习候选。 | learned-only 覆盖率在 DS-1000、HumanEval 和 BigCodeBench-Hard 上分别为 9.35%–9.70%、59.15%–96.95% 和 41.22%–50.00%，对应静态基线为 9.58%、93.29% 和 60.14%；前缀保留增强则达到 9.82%、95.53% 和 63.51%，但验证器调用量分别增加 62.5%、4.8% 和 24.8%。 | 该消融隔离了“替换静态顺序”和“在静态顺序之后扩展搜索”的差别。前缀保留在九次冻结回放中均不降级，符合确定性验证器下的顺序保证；但 DS-1000 为仅 0.23 个百分点的平均增益付出 62.5% 调用开销，说明形式上的覆盖保证并不自动意味着经济上值得部署。 | 表 3；第 6.4 节<br><span class="experiment-evidence">DS-1000 866 9.58 9.35–9.70 9.82 +62.5%</span> |
| 比较不同学习目标与候选组成：global listwise、exact-residual 和 task-marginal，并检查学习排序是否只是近似复制 shortest-first。 | 在 0.5B 验证集上，global listwise 与 exact-residual 的平均最佳成绩同为 8.75 个已接受任务；在两者都有结果的冻结测试种子上，global listwise 平均多接受 2.6% 的删除。task-marginal 的三个种子均最多达到 9 个验证任务，未达到预先设定的 10 个晋级门槛，因此未进入测试集评估。 | 这一对照削弱了“收益来自 residual-only 特殊监督”的解释：不同目标都能形成互补排序，而稀疏的 task-marginal 信号没有通过预设验证门槛。由于 task-marginal 未在测试集运行，不能据此量化它与其他目标的测试差距；能支持的结论只是架构互补比某个目标的独占优势更稳健。 | 第 6.3 节<br><span class="experiment-evidence">On0.5Bvalidation,globallistwiseandexact-residualtrainingtieatameanbestscoreof8.75acceptedtasks,andonthefrozentestseedsavailableforboth,globallistwiseaverages 2.6%moreaccepteddeletionsthanexactresidual.</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：研究语言模型生成的代码删除候选如何在有限验证预算下排序和筛选，核心是代码推理与可验证搜索。; rule check: no taxonomy category reached the rule threshold
- 全文指纹：`07a4846e12727d5fa3eefdb54a1457d6e619cf807c53c03f59291115693beb88`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
