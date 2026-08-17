---
title: "[论文解读] Bootstrapping Niche Multilingual Code Translation via Reinforcement Learning with Execution-Based Verifiable Supervision"
description: "[arXiv 2608.13854][对齐 / RLHF] 本文研究如何利用执行验证产生可靠监督，并以奖励模型和强化学习将大语言模型的代码翻译能力扩展到包含长尾语言的25种编程语言、600个有向翻译方向。"
arxiv_id: "2608.13854"
announcement_date: "2026-08-17"
primary_category: "llm_alignment"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-17T02:01:33.863347+00:00"
source_sha256: "6ce8ae23be6a66841cbbfb704b71432168360b24980d7cdd5d9f8e8b9f3d9c43"
tags:
  - "对齐 / RLHF"
  - "LLM Reasoning"
  - "多对多代码翻译"
  - "长尾编程语言"
  - "执行式验证"
  - "奖励模型"
  - "强化学习"
  - "GRPO"
  - "功能等价性"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">对齐 / RLHF · arXiv 2608.13854</p>

# Bootstrapping Niche Multilingual Code Translation via Reinforcement Learning with Execution-Based Verifiable Supervision

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-17</span>
<span><strong>作者</strong> Kouki Yuki, Jie Zeng, Kyoko Ogawa, Ryunosuke Ikeda, Yohei Kobashi, Takeshi Kojima, Ikuya Yamada, Yusuke Iwasawa, Yutaka Matsuo</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> National Institute of Technology, Numazu College, Japan；Seikei University, Japan；Osaka Metropolitan University, Japan；Recruit Co., Ltd., Japan；The University of Tokyo, Japan；Tokyo University of Science, Japan</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.13854) · [PDF 下载](https://arxiv.org/pdf/2608.13854) · **关键词** 多对多代码翻译, 长尾编程语言, 执行式验证, 奖励模型, 强化学习, GRPO, 功能等价性<br>


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

本文研究如何利用执行验证产生可靠监督，并以奖励模型和强化学习将大语言模型的代码翻译能力扩展到包含长尾语言的25种编程语言、600个有向翻译方向。

**不用术语来说**：代码翻译不能只做到“看起来像目标语言”，还必须保持原程序的行为并通过测试；但现有训练资源主要集中在C++、Java和Python等常用语言，较冷门语言缺少成对样本，使模型在这些方向上更容易生成语法 plausible 却无法正确执行的代码。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出NicheCodeTranslator：从可验证的Python种子程序出发，构建覆盖25种语言的执行验证代码池，再用候选译文的执行成败训练统一奖励模型，并通过GRPO优化600个有向语言对上的翻译策略。
- 提出HumanEval-X++：在HumanEval-X基础上，将代码翻译评测的目标语言从6种扩展到25种，并配套可执行函数签名和测试套件，以比较常用语言与长尾语言方向上的行为保持能力。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

代码翻译旨在把源语言程序转换为目标语言程序，同时保持其可执行行为，而不只是生成表面上相似的文本。判断译文质量通常依赖编译、运行和单元测试，因为 BLEU 等静态文本相似度无法可靠反映功能等价性。本文关注长尾、多对多代码翻译：热门语言之外的训练数据和语言知识较稀缺，同一模型却需要覆盖大量有向语言对，因而容易生成语法看似合理但不能通过测试的代码。已有执行反馈方法通常只覆盖少数语言，并要求强化学习采样阶段为每种目标语言持续维护编译器、运行时和测试工具；本文所处的核心问题是，如何在仍以功能正确性为依据的前提下，将训练扩展到包含小众语言的大规模语言矩阵。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多对多代码翻译**

一个模型同时处理多种源语言和多种目标语言之间的转换；翻译方向具有方向性，例如 Python 到 Rust 与 Rust 到 Python 是两个任务。本文覆盖 25 种语言之间不含同语言转换的 $25\times24=600$ 个有向方向。

</div>
<div class="concept-item" markdown="1">

**执行式验证**

将生成代码放入隔离环境中编译、运行，并用单元测试检查其行为是否符合预期。它直接检验功能正确性，但为许多语言维护编译器、运行时和测试框架会带来较高成本与不稳定性。

</div>
<div class="concept-item" markdown="1">

**基于偏好的强化学习与奖励模型**

先依据候选译文能否通过执行测试构造正负偏好，再训练奖励模型预测跨语言译文的质量；策略模型随后以该预测分数为奖励进行 GRPO 优化。通俗地说，昂贵的真实执行先用于训练一个“自动评分器”，强化学习采样时再由该评分器统一评价多种语言。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一个已知源语言的、具有可验证功能语义的程序，以及指定的不同目标语言；输出是目标语言代码，成功标准是译文可在相应环境中执行并通过由同一问题语义导出的测试。训练场景包含 25 种语言和 $600$ 个有向翻译方向，且重点包括监督数据较少的长尾语言。论文假设初始 Python 程序能够配套生成并执行断言，也假设规则化转换能够把程序接口与测试迁移到其他语言；离线数据构造阶段仍使用各语言沙箱验证，而强化学习阶段用从这些执行标签学得的统一奖励模型替代逐语言实时执行。评测则恢复真实执行：模型生成的目标代码需要接受对应语言测试套件检验。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{L}$**

参与翻译的编程语言集合；本文语境下其大小为 25。

</div>
<div class="notation-item" markdown="1">

**$(\ell_s,\ell_t)$**

一个有向翻译方向，其中源语言 $\ell_s$ 与目标语言 $\ell_t$ 不相同。

</div>
<div class="notation-item" markdown="1">

**$25$**

训练与评测所覆盖的编程语言数量。

</div>
<div class="notation-item" markdown="1">

**$25\times24=600$**

25 种语言两两有向转换且排除同语言转换后得到的翻译方向总数。

</div>

</div>

**直接相关的工作**

- **TransCoder-ST**: 该方法在 C++、Java 和 Python 之间使用通过单元测试的自生成译文进行执行验证自训练，说明无须完整人工平行语料也能借助功能反馈改进翻译；但其训练范围只有 3 种源语言和 3 种目标语言，未解决长尾语言上的大规模多对多扩展问题。
- **CodePivot**: 该方法利用执行奖励，以 SFT 和 GRPO 训练 Python 到 9 种目标语言的方向，并依靠零样本迁移处理其余语言间方向；相比之下，本文试图直接覆盖 25 种语言的全部 $600$ 个有向方向，并以学得的奖励模型降低强化学习采样时对逐语言执行基础设施的依赖。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

软件迁移、现代化改造、代码复用和跨语言互操作要求模型在不同语法、编程习惯与类型系统之间转换代码，同时保持可执行行为。现实中的转换需求并不限于少数主流语言，而较冷门语言的数据稀缺、模型知识较弱，因此多对多翻译中的错误风险更高。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **执行验证的自训练与回译**：TransCoder-ST等方法让模型生成伪平行译文，再通过实际执行或单元测试筛除错误候选，将通过验证的结果作为新的训练数据；TransCoder则主要依靠回译形成跨语言训练信号。
- **监督微调与执行反馈强化学习**：CoTran、OORL、EffiReasonTrans、BootTrans和CodePivot等方法使用监督微调，或采用PPO、GRPO等强化学习算法，根据执行结果或反馈信号提高译文的功能正确性。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有训练流程通常只覆盖少量主流语言或单一翻译方向；表1所列相关方法最多覆盖9种目标语言，因而尚未证明其监督构造与训练方式能够扩展到25种语言间的大规模多对多翻译。
- 直接在强化学习生成阶段为每种目标语言反复配置并调用沙箱执行，会带来跨语言测试环境和反馈获取上的扩展压力；原文因此将“如何构造可扩展的、源于执行结果的监督”列为尚未解决的问题。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚缺少一套面向长尾编程语言的完整方案，能够从稀缺的平行数据起步，自动产生跨语言、可由执行结果核验的训练偏好，并将同一反馈机制稳定地用于大规模多对多强化学习。

</div>
<div markdown="1"><span>核心问题</span>

能否从少量可验证的Python程序出发，通过执行验证构造覆盖25种语言的监督，再学习一个跨语言奖励模型，以避免强化学习期间逐语言调用沙箱，并有效训练覆盖$25\times24=600$个有向翻译方向的代码翻译模型？

</div>
<div markdown="1"><span>作者直觉</span>

单元测试把“译文是否保持原程序行为”转化为可自动判定的成败标签，比代码表面相似度更接近真实翻译目标。先用沙箱执行积累可靠的正负样本，再让统一奖励模型学习这些结果中的跨语言规律，就能在后续GRPO训练时快速评价候选译文，把昂贵且语言相关的即时执行反馈转化为可复用的学习信号。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

NicheCodeTranslator 的核心思路是先把 Python 中较容易获得的“可执行验证能力”传播到另外 24 种编程语言，再用这些验证信号训练一个覆盖全部方向的代码翻译模型。系统以 KodCode 中经过验证的 Python 函数级任务为起点，通过沙箱执行筛选有效断言、从测试字面量恢复类型、用确定性的规则转译器迁移函数接口和测试，并让数据生成模型产生能够通过目标语言测试的源程序；随后针对每个已验证源程序生成其他语言的候选翻译，以测试执行结果构造正负样本，训练统一奖励模型 $r_{\phi}(x,y)$，最后使用 GRPO 依据该奖励模型提供的组内相对分数优化翻译策略。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤一：构造带类型的可验证 Python 种子

首先只保留恰好定义一个函数、不含类、仅使用标准库且目标函数确实被断言调用的实例；数据生成 LLM 再生成仅含字面量的单条断言，并只保留在沙箱中对参考解答执行成功的断言。系统通过 AST 分析断言中的输入与输出字面量恢复参数和返回值类型，对同一实例中出现的不同类型组合分别建立变体，然后重新生成并执行测试，删除断言数量过少的样本。

<div class="method-step__io" markdown="1">

**输入**：KodCode 的函数级 Python 实例，每个实例包含问题描述、参考解答和原始单元测试。<br>
**输出**：具有明确函数签名、具体类型和执行验证断言的规范化 Python 种子；每条断言同时构成一个已经确认的输入—输出行为样例。

</div>

**直观理解**：它不是让模型猜测函数应接收什么类型，而是从已经运行成功的测试中反推类型。这样得到的类型和预期输出都有真实执行结果支撑，可作为跨语言迁移的可靠起点。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤二：将验证基础设施扩展到 24 种目标语言

规则转译器分别把 Python 类型签名转换为目标语言函数头，并把每条断言转换为目标语言测试，无法确定性转换的项目被保守丢弃；数据生成 LLM 根据问题描述和带类型参考解答生成目标语言程序，同时将转译后的函数头固定为生成前缀。每个种子和语言采样多个候选，在目标语言沙箱中运行全部测试，只有全部通过的程序才进入已验证源池。

<div class="method-step__io" markdown="1">

**输入**：步骤一得到的带类型 Python 函数、问题描述以及执行验证过的字面量断言。<br>
**输出**：覆盖 Python 与另外 24 种语言的执行验证程序、统一接口和对应测试，即全部 25 种语言都可充当后续翻译任务的源语言。

</div>

**直观理解**：规则系统负责搬运接口与考题，生成模型只负责写解题代码；固定函数头可避免仅因函数名或参数格式不同而失败。候选必须真正通过迁移后的测试，因此程序是否可用不依赖另一个 LLM 的主观判断。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤三：生成执行标注的多对多偏好数据

对每个已验证源程序和其余 24 种目标语言分别采样多个候选，并在对应语言的沙箱中执行测试；通过全部测试的候选标为正例，测试通过率低于固定阈值的候选标为负例，处于两者之间的候选被丢弃。随后把同一翻译提示下的正负候选组织成偏好对，汇总全部 $25\times24$ 个有向翻译方向。

<div class="method-step__io" markdown="1">

**输入**：步骤二的已验证源程序、源语言与目标语言方向、目标语言测试，以及待训练策略模型生成的候选翻译。<br>
**输出**：由策略自身成功翻译和执行失败样本组成的跨语言偏好数据，供统一奖励模型训练。

</div>

**直观理解**：这里把测试执行器变成自动标注员：全对的是正例，明显错误的是负例，难以确定的中间样本不参与训练。负例来自策略模型实际会犯的错误，因此奖励模型学习的是与当前翻译系统直接相关的错误边界。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 步骤四：训练执行感知奖励模型

跨编码器奖励模型联合编码源程序、翻译方向和候选代码，输出标量 $r_{\phi}(x,y)$；使用 Bradley–Terry 成对目标，使正候选的分数高于同一提示下的负候选。一个共享奖励模型在所有 $25\times24$ 个方向的数据上联合训练，从而近似多语言沙箱给出的执行判断。

<div class="method-step__io" markdown="1">

**输入**：步骤三汇总的翻译提示 $x$、正候选 $y^{+}$ 与负候选 $y^{-}$。<br>
**输出**：能够对任意受支持翻译方向的候选代码给出连续质量分数的统一奖励模型。

</div>

**直观理解**：奖励模型学习比较“哪段翻译更可能通过测试”，而不是直接生成代码。训练完成后，强化学习阶段无需在每一步同时维护和调用 25 套语言执行环境，便可获得与执行结果相关的密集分数。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### Bradley–Terry 奖励模型目标

$$
\mathcal{L}_{\mathrm{RM}}(\phi)=-\log \sigma\!\left(r_{\phi}(x,y^{+})-r_{\phi}(x,y^{-})\right)
$$

**符号说明**

- $\mathcal{L}_{\mathrm{RM}}$：奖励模型在一个正负候选对上的训练损失。
- $\phi$：奖励模型的可训练参数。
- $x$：翻译提示，包含源程序及源语言到目标语言的翻译方向。
- $y^{+}$：通过全部目标语言测试、被标记为正例的候选翻译。
- $y^{-}$：测试通过率低于固定阈值、被标记为负例的候选翻译。
- $r_{\phi}(x,y)$：跨编码器奖励模型对提示与候选组合输出的标量分数。
- $\sigma$：Sigmoid 函数，将正负候选的分数差映射为正例优于负例的概率。

<div class="equation-explanation" markdown="1">

**直观理解**：最小化该损失会增大 $r_{\phi}(x,y^{+})-r_{\phi}(x,y^{-})$，即要求通过执行验证的翻译比明显失败的翻译得分更高。它学习的是候选间排序而非绝对通过概率，因此输出可直接作为强化学习中的相对质量信号。<br>
**原文位置**：第 3.2 节“Reward model”

</div>

</div>

<div class="equation-block" markdown="1">

#### GRPO 组内相对优势

$$
r_i=r_{\phi}(x,y_i),\qquad \hat{A}_i=r_i-\operatorname{mean}\{r_1,\ldots,r_G\}
$$

**符号说明**

- $G$：策略针对同一翻译提示采样的候选数量。
- $y_i$：同一提示下第 $i$ 个候选翻译。
- $r_i$：奖励模型为第 $i$ 个候选给出的标量奖励。
- $\hat{A}_i$：第 $i$ 个候选相对于本组平均奖励的优势。
- $\operatorname{mean}\{r_1,\ldots,r_G\}$：同一提示下全部候选奖励的算术平均值，充当组内基线。

<div class="equation-explanation" markdown="1">

**直观理解**：候选得分高于组内平均值时，$\hat{A}_i$ 为正，其生成概率会在策略更新中得到提升；低于平均值时则受到抑制。用同题候选的均值充当基线可以在不训练额外价值网络的情况下估计相对优势，随后该优势被用于论文所述的裁剪策略梯度更新。<br>
**原文位置**：第 3.2 节“Policy optimization”

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：训练分为“学习执行判据”和“依据判据优化生成”两步。第一步在步骤三的执行标注偏好对上最小化 Bradley–Terry 损失，使共享奖励模型把通过测试的候选排在失败候选之前；第二步固定或调用该奖励模型为策略采样的候选评分，计算组内相对优势 $\hat{A}_i$，再以其加权 GRPO 的裁剪策略梯度更新。原文节选只明确说明相对优势用于 clipped policy-gradient update，未给出完整 GRPO 损失、裁剪系数、KL 正则项或其他优化超参数，因此不应据此补写具体公式。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 确定性接口与测试转译器**

该模块采用 MultiPL-E 风格的规则转译，把带类型的 Python 函数签名和仅含字面量的断言分别映射为目标语言声明与测试；不能可靠转译的样本直接删除。生成程序时，目标语言函数头还被固定为解码前缀，以确保候选与测试在函数名、参数及返回接口上兼容。

> 直观理解：跨语言监督最危险的环节是测试本身被生成模型改错，因此论文只让确定性规则搬运测试和接口。这样，执行失败更可能意味着程序语义错误，而不是测试含义或调用方式在迁移时发生漂移。

**2. 沙箱执行验证与标签生成**

Python 断言、目标语言源程序和最终候选翻译都要在相应沙箱中执行；种子断言及源程序需通过全部相关测试，奖励模型数据则依据候选测试通过情况划分正例、负例和被丢弃的中间区间。沙箱执行因而同时承担数据清洗、跨语言程序认证和偏好标签生成三项职责。

> 直观理解：这相当于用可重复运行的自动判题器代替 LLM 评审。它不能证明程序对所有可能输入都正确，但至少使保留样本在现有测试覆盖范围内具有客观、可复查的功能证据。

**3. 共享跨编码器奖励模型与 GRPO**

跨编码器将翻译提示 $x$ 与候选 $y$ 放入同一上下文联合建模，输出标量奖励，并通过执行标注的正负对学习排序；GRPO 不训练独立 critic，而是用同一提示下 $G$ 个候选的平均奖励作为基线，计算组内相对优势后进行裁剪策略更新。单一奖励模型和单一策略共同覆盖所有 $25\times24$ 个方向。

> 直观理解：奖励模型把昂贵的多语言执行判断压缩成一个快速评分器，GRPO 再利用同题候选之间的相对好坏更新生成模型。共享训练还允许数据较少的长尾语言利用其他语言中的共同程序语义，但原文节选未单独量化这种迁移效应。

**训练与推理**

训练时，系统先离线完成可验证数据构造：从 KodCode 清洗 Python 种子，生成并执行筛选断言，从断言恢复静态类型，再把接口和测试规则转译到 24 种其他语言；数据生成 LLM 翻译参考程序，只有通过全部目标测试的候选才成为源池。策略模型随后从这些源程序生成其余语言的候选，执行器提供正负标签；统一奖励模型在所有 $25\times24$ 个方向的偏好对上训练，之后策略针对每个提示成组采样，由奖励模型评分并通过 GRPO 更新。thinking 与 non-thinking 是分别训练和评估的生成模式，节选没有进一步说明二者的提示模板或思维过程监督方式。

推理时，输入应给出源语言程序及目标语言方向，策略直接生成目标语言代码；训练中的奖励模型、成组采样和目标语言沙箱属于优化过程，并非论文节选明确要求的单次部署推理组件。对于 HumanEval-X++ 式评测，输入还包括源声明、可选源 docstring、源参考实现以及目标语言声明，模型从目标声明之后续写函数体，再把目标声明、生成代码和目标测试组合后放入 MultiPL-E 沙箱执行，以 pass@1 判断功能正确性。

**复现信息**

复现该方法必须保留三项会改变监督可信度的设计：测试限制为可由规则系统确定性转换的字面量断言；静态类型从已执行成功的断言经 AST 恢复，而非由 LLM 猜测；候选程序只有通过全部转译测试才进入已验证源池。Stage 3 中正例要求通过全部测试，负例要求通过率低于固定阈值，中间样本被丢弃，但所给节选没有报告该阈值、最低断言数、最短响应长度、每个实例的采样数或组大小 $G$ 的具体取值。

强化学习覆盖全部 $25\times24$ 个有向翻译方向，并使用一个共享跨编码器奖励模型；缺少代码块或短于最低长度的响应被直接赋予最低奖励，以避免拒绝翻译等非代码输出利用奖励模型漏洞。公平解释结果时还需区分 thinking 与 non-thinking 模式，并注意该方法用奖励模型近似在线执行反馈，以避免每个 RL 步骤运行 25 套语言沙箱；然而训练标签本身仍来自真实沙箱执行，奖励模型并不等同于形式化正确性证明。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- HumanEval-X++是主评测基准：它通过MultiPL-E的规则转换，将函数级HumanEval-X任务扩展至25种目标语言。每个语言方向最多评测164个成功完成规则转换的样本；源代码和目标代码中的docstring均被删除，使模型只能依据代码进行翻译。它主要检验跨语言函数实现能否通过执行测试。
- CodeScope是外部补充基准，覆盖14种语言之间全部$14\times13=182$个翻译方向。清理前有5,382个样本；作者先运行参考解并删除测试输入输出不一致的任务，最终保留5,317个样本。每个方向有24至30个样本，其中130个方向各有30个。该基准使用独立完整程序及输入输出测试，可检验方法是否能从HumanEval-X++式函数任务泛化到另一种程序与测试组织方式。
- 训练数据来自三阶段自动生成流程：第一阶段从KodCode(-V1)随机抽取10,000个Python种子问题，经测试合成、类型标注与沙箱执行过滤后得到11,124个程序，覆盖9,127个不同问题，平均每个程序有11.4条验证断言；第二阶段扩展到25种语言，产生184,626个经执行验证的源程序；第三阶段在四种模型条件下生成10,724,077次翻译 rollout，其中3,734,461个成功、6,284,293个失败，并构造717,083个偏好对，覆盖$25\times24$个方向。该数据用于训练奖励模型及强化学习策略，而不是最终测试集。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**pass@1**

每道题只生成一个候选程序时，通过全部执行测试的题目比例，等价于标准准确率。它同时要求生成结果满足目标语言语法、接口格式和功能语义。 （越高越好，因为更高的$\mathrm{pass@1}$表示更多首次生成的翻译能够通过测试。）

</div>
<div class="metric-item" markdown="1">

**编译错误数或编译错误率**

生成程序在运行测试前即因语法、结构或输出格式问题无法编译的比例或数量，用于定位强化学习是否主要减少“无法进入执行”的失败。 （越低越好，因为编译失败的程序不可能通过后续功能测试。）

</div>
<div class="metric-item" markdown="1">

**全输入输出对通过率**

CodeScope任务只有在生成程序通过该任务提供的全部输入输出对时才判定正确；作者比官方代码只检查一个输入输出对的做法更严格。 （越高越好，因为通过全部测试对比仅通过单个测试更能支持程序行为正确。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### HumanEval-X++总体结果：4B与9B模型，Thinking与Non-Thinking两种模式

<div class="result-value" markdown="1">

作者报告四个条件均优于基础模型。Non-Thinking模式下，4B平均$\mathrm{pass@1}$由45.08升至58.29，增加13.21点；9B由52.42升至66.04，增加13.62点。Thinking模式下，4B由44.59升至59.15，9B由52.31升至63.11。

</div>

这说明收益并非只出现在某一模型规模或某一种推理模式，且在该主基准上幅度较大。由于比较使用相同规模的基础检查点，结果支持“执行监督下的强化学习改善代码翻译”这一作者主张；但实验是单次运行，且训练流水线同时包含偏好数据、奖励模型和策略优化，因此不能从该结果单独判断哪个组件贡献最大。

<div class="result-source" markdown="1">

来源：第5.2节，表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In the best configuration under Non-Thinking mode, the 4B model improves from 45.08 to 58.29 (+13.21) and the 9B model from 52.42 to 66.04 (+13.62) on average across all the languages; Comparable gains hold under Thinking mode (4B: 44.59 → 59.15, 9B: 52.31 → 63.11).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### HumanEval-X++按语言层级及具体目标语言分解：代表性条件为9B、Non-Thinking、基础模型对比GRPO

<div class="result-value" markdown="1">

Non-Thinking的GRPO结果中，中等资源语言提升最大：4B增加21.54点、9B增加20.55点；但4B长尾语言仅增加6.33点，低于流行语言的13.86点。具体语言中，Perl由9.2升至67.8、Ruby由29.9升至86.8、Lua由26.7升至76.4、Julia由40.5升至78.9、D由19.5升至49.5。

</div>

结果否定了“语言越长尾，强化学习收益必然越大”的简单关系。作者将中等资源组的高平均增益主要归因于Perl和Lua两个大幅恢复案例，而不是该层级整体都同等受益；高收益语言也横跨流行、中等和长尾三组。该分解揭示基础模型原本极弱的部分语言存在较大修复空间，但分组平均值容易被少数语言主导。

<div class="result-source" markdown="1">

来源：第5.3节，表5；层级汇总见第5.2节表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

The largest gains accrue to languages on which the base model scored extremely poorly: Perl 9.2 → 67.8, Ruby 29.9 → 86.8, Lua 26.7 → 76.4, Julia 40.5 → 78.9, D 19.5 → 49.5.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 共同评测的22,755个翻译样本上的错误类型分析：Qwen3.5-9B对比其GRPO版本

<div class="result-value" markdown="1">

基础模型与GRPO模型分别成功11,886和15,015次，净增3,129次；编译错误由4,222例降至2,538例，减少1,684例，超过成功增量的一半。

</div>

该结果支持作者的解释：主要收益之一是模型更常生成可编译、格式合规的目标语言代码，而不只是对已能运行的程序做细微语义修正。需要注意，“超过一半”是对成功数量增量与编译错误减少量的归因性对照，并非严格因果分解；同一个输出从编译错误转变后仍可能产生运行时错误或答案错误。

<div class="result-source" markdown="1">

来源：第5.3节，Result by Language中的失败分析

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Of these, compilation errors fall from 4,222 to 2,538 cases, a reduction of 1,684 cases that accounts for more than half of the increase.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 作者受计算资源限制，只对整条流水线进行一次超参数搜索；所有实验均为单次运行，未提供随机种子间方差、置信区间或统计显著性，因此无法判断部分小幅变化是否稳定。
- 原文所给实验章节没有报告受控组件消融，例如移除奖励模型、改变执行验证数据、对比不同强化学习目标或控制训练样本量，因而`ablations`为空。现有结果能支持完整方法优于基础模型，但不能可靠分离三阶段数据构造、奖励模型训练与GRPO各自的贡献；同时Ada、OCaml、Clojure和Racket等语言恢复有限，表明执行监督不能自动弥补目标语言知识不足或与源语言差异过大的问题。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen3.5-4B原始检查点：与强化学习后的同规模模型比较，可直接衡量训练流水线是否改善小规模策略模型，同时避免把收益归因于参数量增加。
- Qwen3.5-9B原始检查点：与其GRPO版本保持模型规模和初始检查点一致，用于检验方法在更强基础模型上是否仍有增益。
- Thinking推理模式下的基础模型：用于判断强化学习收益是否依赖显式思考过程；作者分别训练并评测Thinking与Non-Thinking策略。
- Non-Thinking推理模式下的基础模型：它排除了额外思考过程的帮助，更直接检验策略训练能否提高一次生成代码的可编译性和功能正确性。

**实验想回答的问题**

- 在不提供自然语言题意、仅给源代码的严格条件下，基于执行反馈训练奖励模型并采用强化学习，能否稳定提升不同参数规模、不同推理模式下的多语言代码翻译正确率？
- 性能提升是否集中于长尾语言，以及提升主要来自算法语义理解增强，还是来自减少编译失败、格式不合规等“尚未进入执行”阶段的错误？

**实验实现**

奖励模型从Qwen3.5-35B-A3B初始化，在第三阶段的偏好对上使用LoRA训练：秩为16、缩放系数为32并作用于全部线性层，共训练2,774步即1个epoch，批量大小256，学习率$10^{-5}$，使用AdamW、余弦调度及139步预热。强化学习策略从Qwen3.5-4B或Qwen3.5-9B初始化，以训练后的奖励模型提供监督，每个提示采样4个候选；策略训练100步即1个epoch，批量大小256，学习率$10^{-6}$，使用AdamW和无预热的常数调度。作者分别训练Thinking与Non-Thinking版本。评测时每题仅生成一个结果；HumanEval-X++删除源端和目标端docstring，CodeScope则要求通过全部输入输出对。实验运行于多台每设备90 GB显存的GH200节点。作者只进行一次超参数搜索，所有结果均来自单次运行，未报告方差、置信区间或显著性检验。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- C++到Julia的案例展示了机制层面的变化：在158个样本上，Qwen3.5-9B的编译错误率从62.7%（99例）降至GRPO后的22.2%（35例），通过测试的比例则从36.7%（58例）升至77.8%（123例）。图3中的基础模型遗漏解法主体及函数闭合所需的`end`，因此编译失败；GRPO模型保留同一算法并按Julia惯例生成完整结构，最终通过测试。该案例与总体错误统计一致，但单个案例不能说明所有语言或所有错误类型都按同样机制改善。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper post-trains language models for code translation with reinforcement learning and execution-based verifiable rewards, directly combining RLVR with code reasoning.; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`6ce8ae23be6a66841cbbfb704b71432168360b24980d7cdd5d9f8e8b9f3d9c43`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
