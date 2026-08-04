---
title: "[论文解读] Self-Improving Large Language Models via Progressive Experience Evolution"
description: "[arXiv 2608.02139][对齐 / RLHF] 本文将大模型自我改进的关键瓶颈定位为“经验蒸馏”：先把多次交互轨迹提炼成可迁移、可演化的显式经验并写入模型参数，再通过强化学习探索超出现有经验的新策略。"
arxiv_id: "2608.02139"
announcement_date: "2026-08-04"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:57:04.602762+00:00"
source_sha256: "d863fc759f3b52e6a85a7e49d63d45c30dec4af19eff2e5b456dad100c15e33b"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "LLM 其他"
  - "强化学习"
  - "大语言模型自演化"
  - "经验蒸馏"
  - "渐进式经验演化"
  - "在策略自蒸馏"
  - "数学推理"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.02139</p>

# Self-Improving Large Language Models via Progressive Experience Evolution

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Shijie Ren, Xiting Wang, Meng Li, Yujie Guo, Yunhang Yao, Ziheng Peng, Xunlong Wang, Yuetan Chen, Haoyang Zhou, Yunlong Liang, Fandong Meng</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Gaoling School of Artificial Intelligence, Renmin University of China；WeChat AI, Tencent Inc, China</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.02139v1) · [PDF 下载](https://arxiv.org/pdf/2608.02139v1) · **关键词** 大语言模型自演化, 经验蒸馏, 渐进式经验演化, 在策略自蒸馏, 强化学习, 数学推理<br>
**代码**: [https://github.com/rrrsj/SPEE](https://github.com/rrrsj/SPEE)

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

本文将大模型自我改进的关键瓶颈定位为“经验蒸馏”：先把多次交互轨迹提炼成可迁移、可演化的显式经验并写入模型参数，再通过强化学习探索超出现有经验的新策略。

**不用术语来说**：模型在解题过程中会产生成功方案和失败教训，但这些信息通常只在当前上下文中短暂存在，或被压缩为一个稀疏奖励来更新参数，因而难以沉淀成以后遇到不同问题仍可复用的能力。本文要解决的不是让模型简单记住更多答案，而是让它从多次尝试中归纳一般性的解题策略、约束条件和常见错误，并将这些知识稳定地转化为模型自身能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出SPEE统一后训练框架，将显式经验演化、基于特权经验的在线策略自蒸馏和奖励驱动的强化学习顺序连接起来，形成从经验获取、提炼、内化到继续优化的完整流程。
- 作者引入持续演化的全局经验池，联合利用成功与失败轨迹提取和筛选可迁移知识，以减少单条完整轨迹中的题目特定信息及事后合理化风险，并让后续策略能够累积跨交互经验。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型自演化与后训练研究。传统离线训练依赖大量高质量数据，难以让模型在部署后持续适应新环境；自演化则要求模型从自身与任务环境的多轮交互中学习，将一次性的解题轨迹转化为可在新问题上复用、并能长期保留的能力。现有路线主要分为两类：测试时方法把示例、反思或检索知识放入提示上下文，经验表达明确但不进入模型参数，因而受到上下文容量、检索准确性和跨问题泛化能力的限制；训练时方法以强化学习为代表，通过奖励驱动参数更新，能够内化行为并探索新策略，但成功与失败轨迹中的具体经验通常只经由稀疏奖励间接发挥作用，探索成本较高且效果依赖初始模型。本文据此把“经验蒸馏”视为两类路线之间的关键环节：先从交互轨迹中提炼紧凑、可迁移的文本经验，再通过密集监督将其写入策略参数，最后继续用强化学习扩展已有经验之外的能力。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**交互轨迹**

模型针对一个问题进行推理和作答时形成的完整过程，可包含中间推理、最终答案及成功或失败结果。轨迹记录了模型如何行动，但也混有只对当前题目有效的细节，不能直接等同于可迁移经验。

</div>
<div class="concept-item" markdown="1">

**经验蒸馏**

从多条成功与失败轨迹中抽取可跨问题复用的推理策略、任务不变约束和常见失败模式，再用监督信号将这些知识内化到模型参数中。其目标不是记住某道题的答案，而是把短暂交互转化为持久能力。

</div>
<div class="concept-item" markdown="1">

**在策略自蒸馏**

模型使用当前策略生成数据，并让获得额外信息的教师分布指导同一策略的学生分布学习，因此训练数据会随策略变化。本文使用特权信息增强教师侧行为，再把增强后的行为蒸馏回不依赖该信息的策略。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是能够在数学推理任务中持续自我改进的大语言模型策略。输入包括待解问题，以及当前策略在多次交互中产生的成功和失败轨迹；系统假设任务结果可由奖励或验证信号判断，并且模型能够继续接受后训练。期望的中间输出不是原始轨迹或实例答案，而是删除题目特有信息后形成的紧凑、可迁移经验，包括通用推理策略、任务不变约束和重复出现的失败模式；最终输出是参数得到更新的策略模型，它在正常推理时无需把完整经验库作为额外上下文，也能利用已内化经验解决新问题。本文关注的设置包含连续阶段：经验随当前策略产生的新轨迹不断抽取、验证和演化，经自蒸馏进入模型参数，随后由奖励驱动的强化学习继续探索经验库尚未覆盖的解法。这里的核心假设是，显式经验内化能够为强化学习提供更强的初始化，但从单条完整参考轨迹直接蒸馏可能泄露答案或依赖实例线索，诱发“事后合理化”，因此需要跨轨迹聚合和筛选。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Hübotter et al. (2026), Reinforcement Learning via Self-Distillation**: 该工作代表在线策略自蒸馏路线：教师策略以实例级参考轨迹为附加条件，学生策略学习教师增强后的行为，为经验内化提供了直接机制。本文认为其仍依赖完整轨迹，容易把可迁移知识与题目特有细节、答案信息混合，且没有覆盖经验获取、精炼、内化及后续优化的完整流程。
- **Guo et al. (2025), DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning**: 该工作代表以奖励驱动的训练时推理能力优化：强化学习可以把受奖励的行为写入模型参数并促进新策略探索。本文以此类方法为对照背景，指出轨迹中的具体成功经验和失败教训通常仅通过稀疏奖励间接影响更新，因此可能需要更多探索，并对初始模型质量较敏感。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

随着模型规模扩大，依赖大量高质量离线数据的训练方式成本高且难以覆盖持续变化的新环境，因此需要模型从自身交互中稳定、连续地获得训练分布之外的能力。真正困难之处在于：交互产生的是短暂且高度实例化的轨迹，而目标是形成可复用、可持久保存在模型参数中的能力。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **测试时经验利用**：在推理时把示例、反思结果或检索到的知识作为额外上下文输入模型，使模型无需更新参数即可参考以往经验完成当前任务。
- **训练时策略优化与在线策略自蒸馏**：强化学习依据成功或失败对应的奖励更新模型参数并探索新行为；在线策略自蒸馏则让教师策略读取当前样本的参考轨迹，生成增强行为，再把这些行为蒸馏给学生策略。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 测试时方法把经验保留在参数之外，其效果受上下文容量、检索准确性和跨问题泛化能力限制；训练时强化学习虽然可以内化行为，但轨迹中的具体经验通常只能通过稀疏奖励间接起作用，导致探索需求更大，并使结果较依赖初始模型质量。
- 现有在线策略自蒸馏直接使用完整的单题参考轨迹，其中可迁移策略与题目细节、解法细节乃至答案信息相互纠缠，教师可能借助结果反向拼接解释，形成事后合理化；同时，这类方法没有覆盖经验获取、验证、精炼、内化和继续优化的完整闭环。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作缺少位于轨迹生成与奖励强化学习之间的系统化“经验蒸馏”阶段：尚无机制能够跨多次交互，从成功和失败轨迹中持续抽取、验证并更新紧凑的可迁移经验，再用密集监督将其写入策略参数，为后续强化学习提供更强的起点。

</div>
<div markdown="1"><span>核心问题</span>

如何构建一个无需人工经验标注的统一后训练框架，使大模型能够把多次交互中的短暂轨迹转化为持续演化的通用经验，将这些经验内化为参数能力，并在此基础上继续通过强化学习发现新的解决策略？

</div>
<div markdown="1"><span>作者直觉</span>

单条轨迹像一道题的完整草稿，其中既有通用方法，也混有题目数字、具体答案和偶然步骤；直接学习草稿容易记住局部线索。若先比较多条成功与失败轨迹，把反复有效的策略和常见错误整理进全局经验池，再让教师在这些经验的辅助下指导学生，模型更可能学到跨题可用的原则。完成内化后再进行强化学习，则已有经验可减少低效探索，而强化学习发现的新轨迹又能反过来丰富下一轮经验。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SPEE把大语言模型的自我改进组织为一个反复闭环：先让当前策略对训练问题进行多次作答，从正确与错误轨迹中抽取可迁移的文字经验；再把新经验与跨问题共享的全局经验池合并，并依据其在留出探测集上的边际效用进行筛选；随后通过特权引导的在策略自蒸馏（OPSD），把仅在训练时提供给教师分支的经验压入不读取经验的学生策略参数；最后以蒸馏后的策略为起点执行GRPO，通过奖励驱动的探索发现经验池尚未覆盖的新行为。新产生的轨迹又可供下一轮经验演化使用，因此显式文字经验与隐式参数能力能够逐步共同提升。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 多响应采样与正负轨迹构造

策略为每个问题采样$G$个响应$y_i$，由可验证奖励$r(q,y_i)\in\{0,1\}$判定正确性，并将轨迹$\tau_i=(q,y_i)$划分为成功集合$\mathcal{T}^{+}(q)$和失败集合$\mathcal{T}^{-}(q)$；随后按二者的经验比例抽取$S$条轨迹用于经验提炼。

<div class="method-step__io" markdown="1">

**输入**：输入分布$q\sim\mathcal{D}$、第$k$轮策略$\pi_{\theta_k}$以及每题采样数$G$。<br>
**输出**：带有成功或失败标签$s_i$的轨迹子集$\{(\tau_i,s_i)\}$。

</div>

**直观理解**：同一道题不只看一次作答，而是同时观察模型做对和做错的多条路径。正确路径说明哪些策略值得复用，错误路径则暴露应避免的思维模式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 经验抽取、全局演化与效用过滤

抽取器把每条轨迹转写为可迁移经验$e_i^{(s_i)}$，演化算子$\Phi$再将新旧经验合并、去重、化解冲突并抽象掉题目特有细节；系统比较加入单条候选经验前后在$\mathcal{Q}_{\mathrm{pb}}$上的期望奖励，只保留边际效用$w^{(k)}(e)>\epsilon$的候选，并再次整合得到$\mathcal{E}^{(k+1)}$。

<div class="method-step__io" markdown="1">

**输入**：已标注轨迹、当前模型实现的经验抽取器$\Sigma_{\theta_k}$、旧经验池$\mathcal{E}^{(k)}$和留出探测集$\mathcal{Q}_{\mathrm{pb}}$。<br>
**输出**：经过验证、可跨问题共享的更新经验池$\mathcal{E}^{(k+1)}$。

</div>

**直观理解**：经验池不是把所有解题记录原样堆起来，而像一本持续修订的错题与方法手册：相似规则被合并，有冲突的内容被校正，实际不能帮助留出题目的建议会被删除。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 特权引导的在策略自蒸馏

学生仅根据$q$按自身当前分布生成响应，教师则在同一前缀上额外读取$q$与经验$e$并给出逐词概率；优化反向KL散度，使学生在自己的在策略轨迹上逼近信息更充分的教师，而梯度只更新学生侧参数。

<div class="method-step__io" markdown="1">

**输入**：训练问题$q$、演化后的经验$e\in\mathcal{E}$以及共享底层参数的学生分支$\pi_\theta^{\mathrm{stu}}$和停止梯度的教师分支$\pi_{\bar\theta}^{\mathrm{tea}}$。<br>
**输出**：无需在输入上下文中携带经验、但已将经验内化到参数中的蒸馏策略。

</div>

**直观理解**：训练时允许教师查阅经验手册，学生不能查阅；学生通过模仿教师对每个后续词的判断，把手册中的方法学进模型本身。由于练习样本来自学生当前会生成的答案，教学重点与学生眼下的行为分布保持一致。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### GRPO奖励驱动的隐式策略优化

GRPO在同题响应组内对奖励标准化得到相对优势$A_i$，再用当前策略与旧策略的逐词概率比率构造裁剪代理目标并进行梯度上升；高于组内平均水平的响应被增强，低于平均水平的响应被抑制，裁剪则限制单次更新幅度。

<div class="method-step__io" markdown="1">

**输入**：蒸馏策略、训练问题$q$、每题一组$G$个响应、响应奖励$r_i$以及采样时的旧策略$\pi_{\theta_{\mathrm{old}}}$。<br>
**输出**：能够探索经验池外高奖励解法的更新策略，以及可进入后续经验演化轮次的新轨迹。

</div>

**直观理解**：蒸馏先把模型推到更可能答对的区域，强化学习再在附近继续探索新方法。只要同一组答案中有对有错，就能形成有效的相对学习信号；若全对或全错，组内优势接近零，更新信息便很弱。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 特权引导的在策略自蒸馏目标

$$
\mathcal{L}_{\mathrm{OPSD}}(\theta)=\mathbb{E}_{q\sim\mathcal{D}}\left[D_{\mathrm{KL}}\left(\pi_{\theta}^{\mathrm{stu}}(\cdot\mid q)\,\|\,\pi_{\bar{\theta}}^{\mathrm{tea}}(\cdot\mid q)\right)\right],\qquad \pi_{\bar{\theta}}^{\mathrm{tea}}(y_t\mid q)\triangleq\pi_{\bar{\theta}}(y_t\mid q,e,y_{<t})
$$

**符号说明**

- $\mathcal{L}_{\mathrm{OPSD}}$：OPSD需要最小化的自蒸馏损失。
- $\mathcal{D}$：训练问题的输入分布。
- $q$：从输入分布采样的原始问题。
- $\pi_{\theta}^{\mathrm{stu}}$：只观察原始问题、接受梯度更新的学生策略。
- $\pi_{\bar{\theta}}^{\mathrm{tea}}$：额外观察经验且停止梯度的教师策略；横线表示该分支参数不通过此目标更新。
- $e$：从全局经验池取出的特权经验，仅在训练教师分支时可见。
- $y_t$：响应在位置$t$处的下一个词元。
- $y_{<t}$：位置$t$之前的响应词元前缀。
- $D_{\mathrm{KL}}(P\|Q)$：从分布$P$到分布$Q$的KL散度，此处衡量学生分布偏离教师分布的程度。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标让不读取经验的学生分布靠近读取经验的教师分布，从而把外部文字经验转化为参数中的持久能力。采用学生到教师的反向KL，并在学生自己采样的轨迹上重评分，意味着训练集中修正学生当前真正会采取的行为，而不是只模仿固定离线答案。<br>
**原文位置**：Method，Stage I，Privileged experience distillation，公式(14)与公式(15)

</div>

</div>

<div class="equation-block" markdown="1">

#### GRPO裁剪策略优化目标

$$
\mathcal{J}_{\mathrm{GRPO}}(\theta)=\mathbb{E}_{\substack{q\sim\mathcal{D},\\\mathbf{y}\sim\pi_{\theta_{\mathrm{old}}}(\cdot\mid q)}}\left[\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|y_i|}\sum_{t=1}^{|y_i|}\min\left\{\rho_{i,t}(\theta)A_i,\operatorname{clip}\!\left(\rho_{i,t}(\theta),1-\epsilon,1+\epsilon\right)A_i\right\}\right],\quad A_i=\frac{r_i-\mu_G}{\sigma_G+\delta},\quad \rho_{i,t}(\theta)=\frac{\pi_\theta(y_{i,t}\mid q,y_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(y_{i,t}\mid q,y_{i,<t})}
$$

**符号说明**

- $\mathcal{J}_{\mathrm{GRPO}}$：通过梯度上升最大化的GRPO代理目标。
- $G$：针对同一问题采样的响应数量。
- $y_i$：组内第$i$个完整响应，$|y_i|$为其词元长度。
- $r_i$：第$i$个响应获得的奖励。
- $\mu_G$：同一响应组内奖励的均值。
- $\sigma_G$：同一响应组内奖励的标准差。
- $A_i$：第$i$个响应相对于组内其他响应的标准化优势。
- $\delta$：加入分母以避免数值不稳定的正小常数。
- $\rho_{i,t}(\theta)$：当前策略与采样旧策略在第$i$个响应第$t$个词元上的概率比率。
- $\pi_{\theta_{\mathrm{old}}}$：生成当前训练批次响应的行为策略或旧策略。
- $\epsilon$：限制概率比率变化范围的裁剪系数。

<div class="equation-explanation" markdown="1">

**直观理解**：该目标先用组内奖励均值和标准差判断每个答案相对好坏，再提升高优势答案中已生成词元的概率、降低低优势答案的概率。概率比率裁剪防止策略一次偏移过大；从蒸馏策略开始训练的意义在于更容易采到既有正确答案又有错误答案的组，从而获得非零且有区分度的优势信号。<br>
**原文位置**：Method，Stage II: Implicit Policy Optimization，公式(16)至公式(20)，核心目标为公式(20)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练按先蒸馏、后强化学习的顺序优化。第一阶段固定教师分支的梯度，最小化$\mathcal{L}_{\mathrm{OPSD}}(\theta)$，使学生仅凭问题$q$即可复现教师在额外条件$e$下给出的逐词分布；这一步对应论文所说的“经验蒸馏”，即实现$\pi_{\theta'}(y\mid q)\leftarrow\pi_\theta(y\mid q,e)$。第二阶段以所得$\theta'$为初始化，最大化$\mathcal{J}_{\mathrm{GRPO}}(\theta)$：组相对优势提供奖励方向，重要性比率连接当前策略与生成数据的旧策略，裁剪控制更新稳定性。两项目标并非简单加权同时训练，而是承担互补职责的顺序优化：OPSD吸收已有经验并提高有效采样概率，GRPO利用奖励继续搜索经验池外的新策略。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 动态全局经验池**

经验池沿$\mathcal{E}^{(0)}\rightarrow\mathcal{E}^{(1)}\rightarrow\cdots\rightarrow\mathcal{E}^{(M)}$迭代演化，汇总不同问题、不同轮次及成功与失败轨迹中的经验。当前模型同时承担经验抽取器$\Sigma_{\theta_k}$与演化算子$\Phi$的实现，但通过不同提示执行抽取、归并、冲突处理和策略抽象。

> 直观理解：共享经验池使一道题中发现的方法能够服务其他题目，也使早期不完整的经验可随模型能力提升而被修订。纳入失败经验尤其重要，因为仅总结成功答案无法明确标出反复出现的无效探索方向。

**2. 边际效用验证器**

对候选经验$e$，方法比较当前策略在留出探测集$\mathcal{Q}_{\mathrm{pb}}$上使用候选池$\hat{\mathcal{E}}_{e}^{(k+1)}$与使用旧池$\mathcal{E}^{(k)}$时的平均期望奖励差，并以阈值$\epsilon\geq0$决定是否接纳。为降低验证成本，先在探测集的小子集上粗筛，仅将效用为正的项目送入完整探测集评估。

> 直观理解：模型对单条轨迹的事后解释可能听起来合理却没有实际帮助，因此经验不能只靠语言表面质量入库。该模块用留出问题检验经验是否真的增加正确作答概率，从而抑制错误总结、偶然规律和事后合理化。

**3. OPSD与GRPO的顺序耦合**

OPSD先利用经验增强教师提供的稠密逐词分布，把显式经验内化为学生策略的先验；GRPO随后依据答案级奖励优化该策略，补充经验池覆盖范围之外的行为。两阶段顺序不能简单颠倒，因为OPSD旨在提高强化学习初始策略产生正奖励轨迹以及产生奖励有差异响应组的概率，而GRPO负责继续扩展能力边界。

> 直观理解：OPSD解决的是“怎样把总结出的经验真正学进参数”，GRPO解决的是“怎样继续发现尚未总结的新策略”。前者提供更好的探索起点，后者避免模型能力被现有经验池的内容上限锁住。

**训练与推理**

训练时，首先在训练分布$\mathcal{D}$上用当前策略进行多响应采样，通过可验证的二元奖励构造成功和失败轨迹；同一模型在经验抽取提示下把轨迹转化为正面策略或负面教训。候选经验进入全局池后，由演化算子进行跨问题归并与抽象，再通过留出探测集的边际奖励检验过滤；这一过程可重复$M$轮，使经验池与策略共同演化。随后建立共享底层参数的教师和学生分支：学生只读问题并产生在策略轨迹，教师额外读取经验池内容，对这些轨迹逐词重评分，OPSD把教师的特权知识蒸馏给学生。最后对蒸馏策略执行标准GRPO，使用成组采样、组内标准化奖励和裁剪概率比率更新策略；强化学习产生的更高质量或新型轨迹可用于下一轮经验演化，从而闭合自我改进循环。

推理时只保留已经更新的单一策略$\pi_\theta(y\mid q)$，输入是原始问题$q$，输出是模型生成的解答$y$；教师分支、经验抽取提示、探测集验证和显式经验$e$均不是常规推理的必要输入。因而SPEE与纯测试时经验提示的关键差异是：经验在训练中充当“特权信息”，部署时相关知识已被压入参数，不需要持续扩展上下文或外接经验缓存。

**复现信息**

复现时最关键的结构性设置有四点。第一，经验抽取器$\Sigma_{\theta_k}$和经验演化算子$\Phi$由当前策略模型在相应提示下实现，而不是另设一个外部大型教师；这使其成为自蒸馏框架。第二，每题需生成$G$个候选并保留成功与失败轨迹，抽取阶段仅按原有成功/失败比例随机选择$S$条以节省成本；但所给章节未明确报告$G$、$S$、阈值$\epsilon$、探测集规模及优化超参数的具体取值。第三，效用过滤采用小探测子集粗筛加完整探测集复核的两阶段流程，只有边际效用超过阈值的候选才能进入共享池。第四，OPSD的学生数据必须来自学生当前策略，教师在相同响应前缀上逐词重评分且停止梯度；随后从蒸馏检查点启动标准GRPO。论文说明主实验出于计算效率采用单轮经验演化，而方法本身允许多轮演化；第二阶段理论上也可替换为其他GRPO变体，但本文使用标准GRPO。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- DAPO-math-17k：数学推理训练集，用于对 Qwen3-1.7B、Qwen3-4B 和 Qwen3-8B 三种基座模型进行后训练。所给原文未说明具体训练样本数、数据划分方式或是否使用全部 17k 样本。
- AIME 2024 与 AIME 2025：合并视为一组竞赛级数学评测集，主要检验较难奥林匹克式问题上的推理和搜索能力；报告 pass@16 的平均结果，以及相对基座检查点的性能变化。原文未明确报告各测试集题量。
- GSM8K、MATH500 与 Minerva Math：合并视为一组覆盖小学文字题、一般数学推理及更专业数学问题的评测集，分别用于考察不同难度和知识范围下的泛化能力；三者均报告 pass@1。原文未明确说明所用划分，但语境表明它们用于评测而非训练。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**pass@1**

每道题只采用一次生成时得到正确答案的比例，用于 GSM8K、MATH500 和 Minerva Math；它侧重衡量模型单次作答的可靠性。 （越高越好，因为更高数值表示无需多次采样即可正确解题的比例更大。）

</div>
<div class="metric-item" markdown="1">

**pass@16 average**

AIME 2024 和 AIME 2025 在每题进行 16 次生成条件下的平均通过表现。原文称其为“pass@16 average results”，但未在所给章节中进一步给出聚合公式。 （越高越好，因为它表示在固定多次采样预算下获得正确解答的能力更强。）

</div>
<div class="metric-item" markdown="1">

**相对基座性能变化**

后训练模型相对于同规模 Base model 检查点的准确率变化，以百分点表示，用来区分模型原有能力与训练方法带来的增益。 （越高越好；正值表示方法优于对应基座，且百分点差异是准确率的绝对变化而非相对百分比。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### SPEE 相对于同规模 Base model，在 Qwen3-1.7B、Qwen3-4B 和 Qwen3-8B 上的五基准平均表现

<div class="result-value" markdown="1">

作者报告，SPEE 在三种模型规模上均取得最高平均准确率；相对对应基座检查点，1.7B、4B 和 8B 模型分别提高 4.87、6.96 和 6.53 个百分点。增益并未随参数规模单调变化，其中 4B 的绝对提升最大。

</div>

这说明 SPEE 的收益并非只出现在某一个模型规模上，具有一定的跨规模稳定性。由于比较控制了训练步数和 rollout 总量，结果支持“经验演化与内化提高了固定预算下的训练效果”这一作者主张；但只有平均准确率和单次实验结果时，不能据此证明每个数据集都提升，也不能判断差异是否具有统计显著性。

<div class="result-source" markdown="1">

来源：Experiments, Main Results, Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with the base model checkpoints, SPEE yields improvements of +4.87, +6.96, and +6.53 percentage points on the 1.7B, 4B, and 8B models, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### SPEE 与奖励驱动强化学习基线 GRPO 在三种模型规模上的比较

<div class="result-value" markdown="1">

作者称 SPEE 在所有模型规模上均优于 GRPO，跨规模平均优势为 1.16%。作者将其归因于 SPEE 先把演化出的经验蒸馏进参数，再以这些先验支持后续奖励驱动探索。

</div>

该比较表明，仅靠奖励探索可能受到初始策略能力的限制，而训练前半段形成的参数化经验可能提高后续探索效率。不过这仍是方法级整体比较，不是严格的组件因果检验；在缺少逐基准结果、误差范围和移除经验蒸馏阶段的消融时，1.16% 的优势不能单独证明提升必然来自经验内化。

<div class="result-source" markdown="1">

来源：Experiments, Main Results, Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Compared with GRPO, SPEE achieves superior performance at all model scales, with an average improvement of 1.16%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### SPEE 与 SDPO、Domain Prompt 两类经验利用方式的总体比较

<div class="result-value" markdown="1">

作者报告 SPEE 持续优于 SDPO，并指出与 Domain Prompt 的比较支持参数级经验积累的重要性。前者检验全局经验池式蒸馏是否优于直接蒸馏参考答案，后者检验把经验写入模型参数是否优于仅在推理时提供人工提示；所给原文没有提供这两组比较的具体差值。

</div>

结果方向与论文动机一致：跨轨迹汇总并筛选经验，理论上比绑定单条参考推理路径更容易形成可迁移规则；参数更新也可能比一次性提示保留更持久的能力。但“持续优于”只说明表中比较方向一致，并不能仅凭当前摘录验证作者关于减少事后合理化或增强迁移性的机制解释。

<div class="result-source" markdown="1">

来源：Experiments, Main Results, Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

SPEE also consistently outperforms SDPO.

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

- Base model：未经 SPEE 后训练的对应规模 Qwen3 基座检查点，用于测量所有方法相对于初始模型的净提升。
- Domain Prompt：推理时加入人工设计数学推理提示的测试时方法。它不更新模型参数，因此与 SPEE 的比较用于判断显式提示经验和参数级经验积累之间的差异。
- GRPO：奖励驱动的强化学习基线，通过采样和奖励信号优化策略。该对照用于检验 SPEE 的经验蒸馏阶段是否能改善后续策略优化，而不只是增加另一轮强化学习。
- SDPO：基于自蒸馏的训练方法，用于比较直接蒸馏参考答案与 SPEE 从多次交互轨迹中提取、验证并演化可迁移经验这两种经验内化方式。

**实验想回答的问题**

- 在训练步数与采样轨迹总量受控的条件下，SPEE 能否在不同参数规模的 Qwen3 基座模型上稳定提升数学推理准确率，并优于仅依赖提示、强化学习或自蒸馏的代表性方法？
- 显式经验演化与参数级经验内化是否能为后续策略优化提供更有效的先验，使模型相较 GRPO 和 SDPO 获得更稳定、可迁移的推理能力？

**实验实现**

实验采用 Qwen3-1.7B、Qwen3-4B 和 Qwen3-8B 三种基座规模，统一在 DAPO-math-17k 上训练，并在五个数学基准上评测。为提高方法比较的公平性，作者控制不同方法的训练步数和采样 rollout 总量；这意味着主要差异应来自训练机制，而不是明显不同的交互预算。AIME 2024/2025 使用 pass@16 平均结果，GSM8K、MATH500 和 Minerva Math 使用 pass@1。所给原文没有提供随机种子、重复实验次数、方差或置信区间，也没有给出优化器、学习率、推理温度及确切采样预算，因此目前只能核验总体协议，不能完整复现实验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces a self-improvement post-training framework combining trajectory-based experience distillation, on-policy self-distillation, and reinforcement learning for mathematical reasoning.; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`d863fc759f3b52e6a85a7e49d63d45c30dec4af19eff2e5b456dad100c15e33b`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
