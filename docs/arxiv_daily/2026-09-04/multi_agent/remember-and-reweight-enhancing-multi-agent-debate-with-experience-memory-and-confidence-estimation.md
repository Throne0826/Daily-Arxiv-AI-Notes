---
title: "[论文解读] Remember and Reweight: Enhancing Multi-Agent Debate with Experience Memory and Confidence Estimation"
description: "[arXiv 2609.03619][Multi-Agent] 原文未明确报告。"
arxiv_id: "2609.03619"
announcement_date: "2026-09-04"
primary_category: "multi_agent"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-09-04T04:36:25.384571+00:00"
source_sha256: "bee15ca524fec61997319139f95c9de48cd721ea7813db29cae0c467527609a0"
tags:
  - "Multi-Agent"
  - "LLM Reasoning"
  - "LLM 其他"
  - "多智能体辩论（MAD）"
  - "大语言模型智能体"
  - "共享误解"
  - "概念先验"
  - "同伴偏置"
  - "经验记忆"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">Multi-Agent · arXiv 2609.03619</p>

# Remember and Reweight: Enhancing Multi-Agent Debate with Experience Memory and Confidence Estimation

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-09-04</span>
<span><strong>作者</strong> Xuanfa Jin, Zhijian Ma, Yongcheng Zeng, Xinyu Cui, Haifeng Zhang, Jun Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Affiliation: Institute of Automation, Chinese Academy of Sciences；Affiliation: University of Chinese Academy of Sciences；Affiliation: University College London</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2609.03619v1) · [PDF 下载](https://arxiv.org/pdf/2609.03619v1) · **关键词** 多智能体辩论（MAD）, 大语言模型智能体, 共享误解, 概念先验, 同伴偏置, 经验记忆<br>
**代码**: [https://github.com/KylJin/R2-MAD](https://github.com/KylJin/R2-MAD)

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

本文研究大语言模型（LLM）驱动的多智能体辩论（MAD）：多个智能体先独立作答，再在若干轮中互相阅读、质疑并更新答案。该范式利用不同智能体之间的讨论来发现错误并改进推理，但也存在“共享误解”问题：如果多数智能体一开始共同支持错误答案，后续讨论可能使少数正确智能体被多数说服，从而放大错误而不是纠正错误。本文的核心背景是，MAD中的最终结果不仅受其他智能体意见的影响，还受每个智能体自身的概念先验影响；因此，改进方法需要同时处理自身信念偏差与同伴意见偏置。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**多智能体辩论（MAD）**

MAD让多个基于LLM的智能体围绕同一个任务进行多轮交互。第一个阶段通常是各自独立回答，之后每个智能体观察上一轮的回答并生成修订后的回答，直到达到最大轮数或形成共识。

</div>
<div class="concept-item" markdown="1">

**共享误解（shared misconception）**

共享误解指多数智能体恰好从一开始就相信同一个错误答案。由于辩论中的多数意见具有较强说服力，原本正确的少数智能体可能放弃正确立场，使错误答案最终成为集体共识。

</div>
<div class="concept-item" markdown="1">

**潜在概念分解**

该分析假设任务及其正确答案背后存在一个不可直接观察的真实概念 $\theta^{\star}$，智能体的回答由自身的概念先验和其他智能体回答带来的影响共同决定。概念先验表示智能体在没有参考同伴意见时的内在信念，peer skew（同伴偏置）表示辩论过程中其他智能体意见对该信念的累积推动。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定任务 $x$、目标答案 $y$、$n$ 个具有参数 $\phi_i$ 的LLM智能体，以及最多 $T$ 轮的辩论过程，初始轮 $t=0$ 中每个智能体独立生成回答 $z_i^{(0)}$。在后续轮次 $0<t\leq T$，智能体 $i$ 观察上一轮所有回答组成的集合 $Z^{(t-1)}=(z_1^{(t-1)},\ldots,z_n^{(t-1)})$，并基于任务、群体回答和自身参数生成新的回答 $z_i^{(t)}$；最终通过答案提取函数 $a(\cdot)$ 从回答中得到任务答案。该设定假定智能体能够读取并回应其他智能体的文本，且其生成同时受输入上下文与自身参数影响；论文关注的具体问题是：当多数智能体共同支持错误概念时，如何利用跨辩论经验减弱错误先验，并降低不可靠同伴对最终决策的影响。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$x$**

待解决的任务或问题输入。

</div>
<div class="notation-item" markdown="1">

**$z_i^{(t)}$**

智能体 $i$ 在第 $t$ 轮生成的文本回答或立场。

</div>
<div class="notation-item" markdown="1">

**$Z^{(t)}$**

第 $t$ 轮所有智能体回答组成的联合集合，即 $Z^{(t)}=(z_1^{(t)},\ldots,z_n^{(t)})$。

</div>
<div class="notation-item" markdown="1">

**$\phi_i$**

智能体 $i$ 的内部参数与先验信息，例如模型权重、训练数据或预先提供的上下文。

</div>

</div>

**直接相关的工作**

- **Du et al. (2024)，Multi-Agent Debate**: 该工作代表本文所采用的基础MAD范式：多个LLM智能体通过迭代讨论和答案修订提升推理能力。本文不是重新定义辩论流程，而是在这一流程上增加跨辩论经验记忆、状态感知检索和基于可靠性的意见加权。
- **Estornell and Liu (2024)，latent concept framework**: 该工作为本文分析共享误解提供理论基础，将智能体生成分解为自身的概念先验与同伴互动造成的peer skew。本文据此指出，现有主要抑制同伴影响的方法仍未直接校正有偏的概念先验，并以此构造同时干预两类因素的研究问题。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

多智能体辩论（MAD）通过让多个大语言模型代理反复讨论来改进答案，但当多数代理一开始共同相信同一个错误答案时，会出现“共享误解”：错误多数不仅无法被纠正，还可能逐步说服原本正确的代理，最终形成错误共识。该问题说明，单纯增加讨论轮次或代理数量并不能可靠提升群体推理质量，尤其不适用于需要稳定避免系统性错误的推理与问题求解场景。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **标准多智能体辩论**：多个代理分别生成答案，并在多轮讨论中交换理由、批评彼此观点，再根据讨论结果修正立场。其基本假设是代理之间的多样性能够暴露错误，迭代交流能够把群体引向正确答案。
- **降低同伴偏斜的辩论改进方法**：这类方法主要操纵代理之间的响应或信息交互，以削弱其他代理意见对当前代理的累积影响，即降低同伴偏斜（peer skew），从而减少多数意见对少数意见的压制。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有改进方法主要处理由代理交流产生的同伴偏斜，却没有处理代理自身原本就存在的错误概念先验。当多数代理既拥有相同的错误先验，又通过讨论相互强化时，两种因素会叠加，使错误共识更难纠正。
- 标准辩论及其多数面向同伴交互的改进通常缺乏可利用的历史经验，无法根据当前共识状态主动寻找能够挑战错误多数或支持可靠判断的外部证据；因此，正确但处于少数的观点可能在讨论中被逐渐说服放弃。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

尚未解决的缺口是：如何利用过去辩论的结果，同时校正代理的概念先验并控制不同代理意见在当前辩论中的影响强度。具体而言，已有工作缺少一种能根据当前共识程度选择历史经验、再依据历史表现估计代理可靠性的统一机制，以同时应对错误先验和同伴偏斜这两个相互强化的失效因素。

</div>
<div markdown="1"><span>核心问题</span>

能否构建一种经验记忆驱动的多智能体辩论框架，使代理根据当前辩论状态检索具有针对性的历史证据来修正概念先验，并利用这些经验估计各代理的可靠性，以置信度权重调节同伴影响，从而降低共享误解并提高最终答案的正确性？

</div>
<div markdown="1"><span>作者直觉</span>

过去辩论中已经出现过的成功与失败轨迹，可以为当前判断提供超越即时多数意见的参照。当前共识较高时，检索多样且具有对比性的经验有助于挑战可能错误的多数；代理意见分歧较大时，检索与成功结果相关的经验有助于稳定判断。进一步地，如果某个代理在相似情形下的立场历史上更可靠，就应让其意见获得更高权重；反之则降低其对群体的影响。这样，经验记忆分别为先验校正和意见重加权提供依据，直观上相当于让辩论不仅听取“当前谁说得多”，还参考“过去谁在类似问题上判断得更可靠”。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

R²-MAD 是一个在推理阶段增强多智能体辩论的框架，核心是“记住过去、重新分配影响力”。给定任务 $x$，多个基于大语言模型的智能体先独立作答，随后迭代查看同伴回答并修正立场。与普通 MAD 直接把所有同伴回答等权放入上下文不同，R²-MAD 为每个智能体 $i$ 维护经验库 $M_i$：历史辩论结束后，将各轮任务、辩论状态、全体回答、正确性及最终结果保存为案例；新一轮辩论中，再依据当前任务和共识程度检索 $K$ 条经验，形成 $E_i^{(t)}$。这些经验一方面作为历史证据修正智能体对潜在概念 $\theta$ 的先验判断，另一方面用于估计每名同伴当前回答的可靠性，并通过提示中的高、低置信度标注改变其影响。

端到端看，输入是当前问题 $x$、上一轮回答集合 $Z^{(t-1)}$ 与历史经验库；中间过程依次完成辩论状态构造、状态感知检索、基于历史正确性的同伴置信度估计，以及带记忆和置信度标注的下一轮生成；输出是各智能体更新后的回答 $Z^{(t)}$，在达到共识或最大轮数 $T$ 后通过答案抽取函数 $a(\cdot)$ 得到最终答案。其设计分别干预共享误解的两个来源：检索经验校正“模型本来就相信什么”，置信度加权控制“模型应当多大程度相信多数同伴”。直观而言，它不是让多数票自动获胜，而是让智能体先回忆类似争论中过去发生了什么，再判断当前哪些发言更值得听。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造当前辩论状态

系统总结上一轮讨论得到自然语言摘要 $h^{(t-1)}$，并计算共识率 $\mathrm{Cons}(Z^{(t-1)})$，从而组成状态 $s_i^{(t)}=\langle x,z_i^{(t-1)},h^{(t-1)},\mathrm{Cons}(Z^{(t-1)})\rangle$。共识率是持最流行答案的智能体比例，因此只描述意见集中程度，不把高共识直接视为正确。

<div class="method-step__io" markdown="1">

**输入**：当前任务 $x$、智能体 $i$ 在上一轮的回答 $z_i^{(t-1)}$、上一轮全部回答 $Z^{(t-1)}$。<br>
**输出**：供检索使用的智能体特定辩论状态 $s_i^{(t)}$。

</div>

**直观理解**：这一步给当前争论制作一张“现场快照”：不仅记录问题和自己的观点，还记录大家谈了什么以及意见是否高度一致。高一致可能是真共识，也可能是集体犯错，所以它被用于调整检索策略，而不是直接决定答案。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 按辩论状态检索历史经验

先按状态嵌入的余弦相似度取前 $3K$ 个案例形成候选集，再用共识率控制的最大边际相关性策略逐个选出 $K$ 条经验：低共识时更偏向相关且结果正确的案例，高共识时降低该偏好并增强多样性惩罚，以引入可能反驳多数意见的历史案例。

<div class="method-step__io" markdown="1">

**输入**：当前状态 $s_i^{(t)}$、智能体经验库 $M_i$、目标检索数 $K$。<br>
**输出**：检索经验集合 $E_i^{(t)}\subseteq M_i$。

</div>

**直观理解**：如果现场意见分散，系统优先找“类似问题过去怎样做对了”；如果多数人已经说出同一个答案，系统会刻意多找不同类型的往例，检查这种一致是否曾经导致共同误判。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 由经验估计同伴可靠性

对每条检索经验，计算 $z_j^{(t)}$ 与同伴 $j$ 在该经验中的历史回答之间的语义相似度，并以该相似度为权重汇总历史正确性，得到智能体 $i$ 视角下的置信分数 $c_{j,i}^{(t)}$。随后将分数离散为高置信、无标注或低置信三档。

<div class="method-step__io" markdown="1">

**输入**：检索集合 $E_i^{(t)}$、同伴 $j$ 的当前回答 $z_j^{(t)}$，以及经验中记录的同伴历史回答和正确性。<br>
**输出**：每个同伴相对于接收者智能体 $i$ 的置信度及提示标注。

</div>

**直观理解**：系统不根据智能体身份永久指定谁更可靠，而是问：“这个同伴现在的说法像不像它过去在类似场景中的说法，而那些说法当时是否正确？”因此，同一同伴面对不同任务可获得不同权重。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 带记忆与置信度的辩论更新

将历史经验和带置信度标注的同伴回答共同写入提示，令智能体生成下一轮回答 $z_i^{(t+1)}$；经验用于校正概念先验，标注用于增强可靠观点并抑制缺乏历史支持的观点。各智能体重复此过程，直到达到共识或最大轮数 $T$。

<div class="method-step__io" markdown="1">

**输入**：任务 $x$、上一轮同伴回答、检索经验 $E_i^{(t)}$、各回答的置信度标注及智能体参数 $\phi_i$。<br>
**输出**：更新后的多智能体回答集合以及经 $a(\cdot)$ 抽取的最终答案。

</div>

**直观理解**：记忆告诉模型“类似争论以前怎样发展”，置信标注告诉模型“哪些当前发言更值得参考”。两者分别修正自己的固有偏见和从众倾向，而不是简单增加更多上下文。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 共识自适应的最大边际相关性检索

$$
e^{\star}=\underset{e\in\mathcal{C}_{i}^{(t)}\setminus E_{i}^{(t)}}{\arg\max}\left[\lambda^{t}\,\mathrm{sim}(e,s_{i}^{(t)})\,r_i(e)-(1-\lambda^{t})\max_{e'\in E_{i}^{(t)}}\mathrm{sim}(e,e')\right],\qquad \lambda^{t}=1-\gamma\,\mathrm{Cons}(Z^{(t-1)}),\ \gamma\in[0,1]
$$

**符号说明**

- $e^{\star}$：当前贪心步骤选中的经验案例
- $\mathcal{C}_{i}^{(t)}$：按状态相似度预检索得到的候选经验集
- $E_{i}^{(t)}$：智能体 i 在第 t 轮已经选中的经验集合
- $s_{i}^{(t)}$：由任务、自身上一轮回答、辩论摘要和共识率组成的当前状态
- $\mathrm{sim}(\cdot,\cdot)$：基于嵌入表示计算的余弦相似度
- $r_i(e)$：经验 e 中智能体 i 对应的辩论结果奖励，正确为 1、错误为 0
- $\lambda^{t}$：相关性与多样性之间的动态权衡系数
- $\gamma$：控制共识率对检索权衡影响强度的超参数
- $\mathrm{Cons}(Z^{(t-1)})$：上一轮中支持最流行答案的智能体比例

<div class="equation-explanation" markdown="1">

**直观理解**：方括号第一项奖励与当前状态相似且历史结果正确的经验，第二项惩罚与已选案例重复的经验。由于共识越高，$\lambda^t$ 越小，系统会降低对“相似成功案例”的集中偏好并更强调多样性，从而为检验错误多数引入对照证据；共识较低时则相反，优先利用相关的正面经验帮助形成正确方向。<br>
**原文位置**：第 4.2 节，公式 (7) 与公式 (8)

</div>

</div>

<div class="equation-block" markdown="1">

#### 基于相似历史表现的同伴置信度

$$
c_{j,i}^{(t)}=\frac{\sum_{k=1}^{K}\mathrm{sim}\!\left(z_{j}^{(t)},z_j(e_{i,k})\right)\,\zeta_j(e_{i,k})}{\sum_{k=1}^{K}\mathrm{sim}\!\left(z_{j}^{(t)},z_j(e_{i,k})\right)}
$$

**符号说明**

- $c_{j,i}^{(t)}$：智能体 i 在第 t 轮对同伴 j 当前立场可靠性的估计
- $K$：为智能体 i 检索的经验数量
- $z_j^{(t)}$：同伴智能体 j 在当前轮的回答
- $e_{i,k}$：智能体 i 检索集合中的第 k 条经验
- $z_j(e_{i,k})$：经验 $e_{i,k}$ 中记录的智能体 j 的历史回答
- $\zeta_j(e_{i,k})$：经验 $e_{i,k}$ 中智能体 j 的历史回答正确性指示量
- $\mathrm{sim}(\cdot,\cdot)$：当前回答与历史回答之间的余弦相似度

<div class="equation-explanation" markdown="1">

**直观理解**：该式是历史正确性的相似度加权平均：与当前立场越相似的历史回答，对置信度贡献越大，不相似的经历影响较弱。因此它估计的不是同伴总体能力，而是同伴在当前类型的辩论状态下坚持这种立场时有多可靠；该分数随后被转成提示级置信标注，用于调节下一轮的同伴影响。<br>
**原文位置**：第 4.3 节，公式 (11)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用：R²-MAD 没有提出用于更新大语言模型参数的监督损失、强化学习目标或端到端训练目标。其“学习”发生在外部记忆层面，即把已结束辩论转为经验案例并持续加入 $M_i$；推理时通过检索和提示级标注改变生成上下文。论文的概率分解和“先验校正”“反多数支配”命题用于解释机制，而不是一个通过梯度最小化的目标函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 辩论状态感知的经验记忆**

经验案例包含状态、全体当前回答、答案、逐轮正确性与最终奖励，而非仅存储问题—答案对。检索先保证语义相关性，再根据当前共识率动态平衡“相关且成功的案例”与“彼此不重复的案例”；检索到的 $E_i^{(t)}$ 在概率解释上把裸概念先验 $\mathbb{P}(\theta\mid\phi_i)$ 更新为记忆条件先验 $\mathbb{P}(\theta\mid E_i^{(t)},\phi_i)$。

> 直观理解：普通相似度检索只问“过去有没有相似题”，该模块还问“过去的争论局面是否与现在相似”。这一区别很重要，因为意见分散时需要成功范例来指路，而意见高度一致时更需要能揭露集体错误的反例。

**2. 记忆导出的同伴置信度**

对接收者智能体 $i$，每个同伴 $j$ 都有条件化置信度 $c_{j,i}^{(t)}$；它由当前回答与相似历史回答的匹配程度及后者的正确性共同决定。理论表达中，相应权重 $w_{j,i}^{(t)}$ 作为同伴似然项的指数，减小错误多数对后验的累积推动；若共享误解的 $m$ 个智能体均获得权重 $\alpha\in(0,1)$，作者声称多数支配速度可从 $O(m)$ 减慢为 $O(\alpha m)$。

> 直观理解：同伴影响力不是“一人一票”，也不是固定专家排名，而是由类似历史中的表现决定。这样，即使错误观点人数更多，只要这些观点在相似案例中缺少成功记录，其从众压力就会被削弱。

**3. 黑盒模型的提示级重加权**

由于框架无法直接修改黑盒大语言模型的词元概率，实际系统不显式改写内部概率分布，而是依据阈值 $w_h$ 与 $w_l$ 给同伴回答添加高置信或低置信文本标记；处于两阈值之间的回答不标注。检索经验、辩论摘要、同伴回答及这些标记共同构成下一轮生成上下文。

> 直观理解：论文中的指数加权解释了理想情况下应怎样改变同伴影响，实际实现则通过模型能理解的文字标签近似完成。优点是适用于不能访问参数或概率接口的模型，代价是标记能否精确对应理论权重取决于模型对提示的遵循程度。

**训练与推理**

经验准备阶段，可先在已有任务上运行多智能体辩论，并在每轮结束后记录 $e_i^{(t)}=\langle s_i^{(t)},Z^{(t)},y,\zeta_i^{(t)},r_i\rangle$。其中结果反馈可以直接复用基准数据标签，也可以由验证器或程序执行反馈产生；因此方法需要某种可判断已结束辩论好坏的信号，但不要求额外训练语言模型。

在线推理阶段，第 $0$ 轮让 $n$ 个智能体根据 $x$ 独立生成回答；从第 $t>0$ 轮开始，为每个智能体分别构造状态、预检索前 $3K$ 个候选、以动态 MMR 选取 $K$ 条经验，再由这些经验估计每个同伴的条件化置信度。系统将检索案例与高、低置信度标注加入该智能体提示，生成下一轮回答；所有智能体可得到不同的检索结果和对同伴的不同可靠性判断。循环在形成共识或达到最大轮数 $T$ 时结束，再通过 $a(\cdot)$ 从响应中抽取答案；结束后的轨迹继续写入经验库，供未来任务使用。

**复现信息**

公平解释该方法所需的关键实现信息有四点。第一，状态和回答之间的相似度均通过嵌入表示的余弦相似度计算，检索与置信估计本身不调用生成模型。第二，每轮先取前 $3K$ 个相似案例，再通过 MMR 缩减为固定的 $K$ 条，因此注入的记忆数量不会随问题规模增长。第三，默认使用 $w_h=0.55$ 与 $w_l=0.45$：当 $c_{j,i}^{(t)}>w_h$ 时标为高置信，当 $c_{j,i}^{(t)}<w_l$ 时标为低置信，否则不加明确标记；这里的阈值是提示实现规则，不应与理论表达中的连续指数权重混为一谈。第四，每轮需要生成上一轮的自然语言摘要 $h^{(t-1)}$，这是相较普通 MAD 的额外生成步骤；经验检索和置信计算只增加嵌入计算，而记忆构建依赖可获得的结果正确性信号。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- MATH500：用于数学推理；Level-5（最难）题目作为测试集，其余题目用于构建记忆，检验方法对长链条推导问题的能力。
- MMLU-Pro 的 Economics 与 Engineering 子集：用于领域知识推理；从数据中随机抽取部分样本作为测试集，其余样本用于记忆构建，检验方法在专业知识密集型任务上的泛化。
- TruthfulQA：用于事实判断；采用训练集构建经验记忆、测试集进行评估的划分，检验方法识别和纠正事实性错误的能力。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Accuracy（准确率）**

预测答案正确的样本比例；表中同时报告各基准测试集准确率及其平均值。 （越高越好，因为它直接表示正确回答所占比例。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 总体性能：四个基准、三个主要开源模型上的 R$^2$-MAD 与 CoT、Self-Consistency、MAD 和 MAD-M$^2$ 比较。

<div class="result-value" markdown="1">

作者报告 R$^2$-MAD 在三个模型上都取得最高平均准确率，并且在知识密集型的 Economics 和 TruthfulQA 上优势更明显；在 MATH500 上提升相对有限。R$^2$-MAD 还在 Llama-3.3-70B-Instruct 和 GPT-4o-mini 上保持相对 CoT 与 MAD 的最高平均准确率。

</div>

这说明方法的收益并不只依赖小模型，也不只适用于某一种任务。知识密集型任务更容易受错误概念先验和事实偏差影响，因此记忆检索与置信度加权在这些任务上更有发挥空间；但该结果不能证明 R$^2$-MAD 能解决所有长链条数学推导错误，因为 MATH500 上的相对优势较小。

<div class="result-source" markdown="1">

来源：第5.2节 RQ1；表1及附录B.6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

R2-MAD achieves the highest average accuracy on all three models, consistently outperforming both single-agent methods and debate baselines, with the largest improvements on the knowledge-intensive benchmarks such as Economics and TruthfulQA and somewhat limited on MATH500, where the answer hinges on a long derivation rather than on domain knowledge.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 共享误解子集：只评估标准 MAD 在第0轮多数智能体已经给出错误答案的样本。

<div class="result-value" markdown="1">

在 Qwen2.5-7B-Instruct 上，R$^2$-MAD 在四个基准上均超过 MAD 和 MAD-M$^2$；Economics 的准确率为27.10%对 MAD 的17.65%，Engineering 为27.10%对17.42%。在 Gemma-3-4B-IT 上，R$^2$-MAD 在四个基准中的三个领先，TruthfulQA 的改善最显著。

</div>

该设置直接测试论文所针对的失败模式：多数智能体一开始都错时，普通辩论会把错误共识当作支持证据。R$^2$-MAD 在此处的相对优势大于总体测试，支持其机制确实有助于纠正共享误解；不过这是经过条件筛选的困难子集，不能把子集准确率直接等同于所有测试样本上的总体性能。

<div class="result-source" markdown="1">

来源：第5.2节 RQ4；图3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

On Qwen2.5-7B-Instruct, R2-MAD substantially outperforms both MAD and MAD-M2 across all four benchmarks, with the largest margins on Economics (29.41% versus 17.65% for MAD) and Engineering (27.10% versus 17.42%).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 辩论状态感知检索策略：在固定其他组件的条件下，将论文策略与随机、相似度、仅正例、仅多样性及固定 $\lambda$ 的策略比较。

<div class="result-value" markdown="1">

两种模型、两个基准上的平均准确率中，Debate-State-Aware 为0.663，优于最佳固定 $\lambda$ 设置的0.657、Similarity-based 的0.647和 Random 的0.635；该策略在四个单项设置中三项取得最好或并列最好结果。

</div>

随机检索较弱说明把任意历史案例塞入提示词本身不足以产生稳定收益；普通相似度检索也落后于状态感知策略，说明当前辩论共识程度应参与决定相关性与多样性之间的取舍。该对照支持“如何选择记忆”是关键因素，但仍不能单独证明置信度加权没有贡献，因为本实验保持了其他模块不变而只替换检索策略。

<div class="result-source" markdown="1">

来源：第5.2节 RQ3；表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Our policy attains the highest average accuracy (0.663), ahead of the best fixed-λ setting (0.657) and clearly ahead of random (0.635) and similarity-based (0.647) retrieval.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 实验覆盖的主要基准数量有限，且主表集中于 MATH500、MMLU-Pro 的两个子集和 TruthfulQA；对更广泛任务类型、不同语言和更长辩论轮数的适用性，原文未明确报告。
- 共享误解实验只分析标准 MAD 第0轮多数错误的条件子集，且论文主要报告准确率聚合结果；缺少逐案例的检索质量、置信度校准或统计显著性分析，因此机制层面的因果解释仍需进一步验证。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- CoT：单个智能体进行链式思考，是不使用多智能体协作或经验记忆的基础比较。
- Self-Consistency：单个智能体采样多条推理路径并多数投票，能够检验增益是否仅来自增加采样数量；其主实验使用9条路径，以匹配3个智能体进行3轮辩论的生成调用预算。
- MAD：标准多智能体辩论框架，是判断经验记忆和置信度机制是否真正改善辩论的核心基线。
- MAD-M$^2$：通过记忆掩码过滤前轮不可靠信息的辩论方法，用于比较两种不同的历史信息筛选思路；主实验采用其客观掩码变体。

**实验想回答的问题**

- RQ1：R$^2$-MAD是否在不同任务和模型上优于单智能体方法及现有多智能体辩论基线？
- RQ2–RQ4：记忆检索、置信度加权及辩论状态感知检索策略是否各自带来增益，并且是否特别能缓解共享误解情形？

**实验实现**

主要使用 Qwen2.5-7B-Instruct、Qwen3-8B 和 Gemma-3-4B-IT，另在 Llama-3.3-70B-Instruct 与 GPT-4o-mini 上进行扩展验证。所有辩论方法统一使用3个智能体、进行3轮辩论；各方法共享相同的系统提示、任务提示和辩论提示，以避免提示词差异造成不公平。数据先划分为用于构建经验记忆的训练集和用于最终评估的测试集，防止测试数据泄漏。共享误解分析进一步筛选出标准 MAD 在第0轮中多数智能体已经给出错误答案的样本。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 移除置信度模块：保留记忆检索，但不为智能体回答分配置信度权重，也移除同伴回答中的相关标注。 | 在 Qwen2.5-7B-Instruct 上，完整模型平均准确率为0.607，移除置信度后为0.585；在 Gemma-3-4B-IT 上，Economics 从0.521降至0.474，TruthfulQA 从0.705降至0.699。 | 该消融隔离了“根据历史经验估计不同智能体可靠性并调节其影响”的作用。性能下降说明记忆检索并不能完全替代可靠性加权，尤其在部分知识任务上，区分不同同伴意见的可信度很重要；但单个模型或基准上的下降幅度不能据此推出该模块在所有任务中同等重要。 | 第5.2节 RQ2；表2<br><span class="experiment-evidence">On Qwen2.5-7B-Instruct, the full R2-MAD achieves an average accuracy of 0.607, while removing confidence weighting (w/o Confidence) drops performance to 0.585, and removing memory retrieval (w/o Memory) further drops it to 0.576.</span> |
| 移除记忆模块及检索策略比较：先从任务提示中删除检索到的经验、仅保留置信度加权；再在完整框架中替换辩论状态感知检索策略。 | 在 Qwen2.5-7B-Instruct 上，移除记忆后的平均准确率为0.576；在 Gemma-3-4B-IT 上，移除记忆使 TruthfulQA 从0.705降至0.657。检索策略实验中，Debate-State-Aware 平均为0.663，Random 为0.635，Similarity-based 为0.647。 | 移除记忆后的下降表明，置信度估计需要历史经验提供依据，二者不是可互换模块。策略替换结果进一步说明，记忆的价值取决于是否根据当前共识状态选择案例，而不是仅仅拥有一个记忆库。由于这里没有报告每个策略在所有模型和任务上的完整统计显著性，结论应理解为经验性支持而非严格因果证明。 | 第5.2节 RQ2–RQ3；表2、表3<br><span class="experiment-evidence">Our policy attains the highest average accuracy (0.663), ahead of the best fixed-λ setting (0.657) and clearly ahead of random (0.635) and similarity-based (0.647) retrieval.</span> |

**定性案例**

- 共享误解分析是本文最接近案例级诊断的结果：在筛选出的样本中，标准 MAD 从第0轮起就受到错误多数意见的影响，而 R$^2$-MAD 在 Qwen2.5-7B-Instruct 的 Economics 和 Engineering 上分别达到27.10%和27.10%，高于 MAD 的17.65%和17.42%。这表明历史经验可能帮助智能体重新检查共同的错误先验，置信度权重则可能抑制错误多数意见；不过原文提供的是聚合准确率，而非具体问题、检索案例或逐轮回答，因此不能进一步判断单个案例究竟由哪条记忆导致翻转。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出利用经验记忆和置信度重加权来改进 LLM 多智能体辩论与推理的框架。; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`bee15ca524fec61997319139f95c9de48cd721ea7813db29cae0c467527609a0`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
