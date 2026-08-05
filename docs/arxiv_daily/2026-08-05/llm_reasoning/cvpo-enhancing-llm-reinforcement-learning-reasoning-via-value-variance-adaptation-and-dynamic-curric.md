---
title: "[论文解读] CVPO: Enhancing LLM Reinforcement Learning Reasoning via Value-Variance Adaptation and Dynamic Curriculum Learning"
description: "[arXiv 2608.03068][LLM Reasoning] 本文针对大语言模型数学推理的价值模型强化学习，提出同时利用轨迹内价值方差细化优势权重、并随模型能力动态调整题目权重的 CVPO，以改善探索、信用分配与难度漂移问题。"
arxiv_id: "2608.03068"
announcement_date: "2026-08-05"
primary_category: "llm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:39:43.480373+00:00"
source_sha256: "9f10e5ecfbc6aadee56cc01faf7dd39d6082bc3b7d086cf30a4a7aa8a06d9865"
tags:
  - "LLM Reasoning"
  - "对齐 / RLHF"
  - "LLM 其他"
  - "强化学习"
  - "大语言模型推理"
  - "强化学习后训练"
  - "价值网络"
  - "轨迹价值方差"
  - "信用分配"
  - "动态课程学习"
  - "难度漂移"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM Reasoning · arXiv 2608.03068</p>

# CVPO: Enhancing LLM Reinforcement Learning Reasoning via Value-Variance Adaptation and Dynamic Curriculum Learning

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Ziqi Jia, Yalu Ouyang, Bo Pang, Panpan Li, Hangfei Xu, Shengzhao Wen, Shiyong Li, Yanpeng Wang</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Tsinghua University；University of California, San Diego</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03068v1) · [PDF 下载](https://arxiv.org/pdf/2608.03068v1) · **关键词** 大语言模型推理, 强化学习后训练, 价值网络, 轨迹价值方差, 信用分配, 动态课程学习, 难度漂移<br>


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

本文针对大语言模型数学推理的价值模型强化学习，提出同时利用轨迹内价值方差细化优势权重、并随模型能力动态调整题目权重的 CVPO，以改善探索、信用分配与难度漂移问题。

**不用术语来说**：模型在强化学习中会反复生成解题过程，并根据结果反馈学习，但现有训练方式常把同为答对或同为答错的过程近似同等对待，难以判断哪些过程更值得巩固或探索；与此同时，模型能力不断提高，同一道题对它而言会逐渐变简单，固定不变的题目权重因而无法始终提供合适的训练挑战。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 在回答轨迹层面，作者将逐词价值估计的方差视为生成探索强度的信号，并据此按奖励类型自适应调整轨迹优势：鼓励错误回答继续探索，同时使正确回答更稳定地收敛；作者还声称理论分析表明该方差会约束策略更新幅度。
- 在问题层面，作者提出动态课程权重机制，持续依据模型当前表现评估题目相对难度并调整训练权重，使训练重点随能力变化，从而缓解题目由难变易所造成的难度漂移。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于大语言模型推理的强化学习后训练研究。其基本做法是把回答生成建模为逐词元决策过程：模型根据题目与已生成内容选择下一个词元，并利用答案奖励及价值网络估计的长期回报更新生成策略。本文聚焦数学推理中的价值型方法；相较于仅以同组回答奖励归一化来构造优势的无价值方法，价值型方法可在回答内部进行更细粒度的信用分配，但仍面临同批轨迹结果高度同质时反馈缺乏区分度，以及模型能力提升后题目相对难度持续变化的问题。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**词元级马尔可夫决策过程（MDP）**

将文本生成看作连续决策：状态是题目和当前已生成前缀，动作是选择下一个词元，直至形成完整回答。给定当前前缀和所选词元后，下一个状态由拼接操作确定。

</div>
<div class="concept-item" markdown="1">

**状态价值与优势估计**

状态价值 $V(s_t)$ 估计从当前生成前缀继续作答可获得的未来回报；优势 $hat{A}_t$ 衡量某个实际动作相对该状态平均水平好多少。价值网络因此能够把最终答案奖励向推理链中的不同位置分配。

</div>
<div class="concept-item" markdown="1">

**近端策略优化（PPO）**

PPO依据优势信号提高有利动作的概率、降低不利动作的概率，同时通过概率比裁剪限制单次更新幅度。这样可避免新策略相对旧策略变化过大，从而提高强化学习训练的稳定性。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是从初始分布 $d_0$ 采样的数学题提示 $x=(x_0,cldots,x_m)$，策略 $pi_theta$ 自回归生成回答 $y=(y_0,cldots,y_T)$。在时刻 $t$，状态 $s_t$ 包含完整提示及截至当前的回答前缀，动作 $a_t$ 是下一个词元，环境转移是确定性的文本拼接；奖励函数 $R$ 提供标量评价，价值函数估计后续回报。训练目标是在限制新旧策略偏移的条件下提高预期奖励，并为长推理轨迹提供准确的词元级学习信号；本文进一步假设轨迹内价值估计的波动可反映生成探索程度，且题目难度会随模型能力变化而动态漂移。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathcal{M}=(S,\mathcal{A},\mathbb{P},R,d_0)$**

语言生成对应的马尔可夫决策过程；依次包含状态空间、词表动作空间、状态转移、奖励函数和初始提示分布。

</div>
<div class="notation-item" markdown="1">

**$s_t=(x_0,\ldots,x_m,y_0,\ldots,y_t)$**

时刻 t 的状态，由全部输入提示词元和截至该时刻生成的回答词元组成。

</div>
<div class="notation-item" markdown="1">

**$r_t(\theta)=\frac{\pi_\theta(a_t\mid s_t)}{\pi_{\theta_{\mathrm{old}}}(a_t\mid s_t)}$**

新策略与旧策略对当前动作所赋概率之比，PPO用它衡量策略更新幅度；这里的 $r_t(θ)$ 是概率比，不是即时奖励。

</div>
<div class="notation-item" markdown="1">

**$\hat{A}_t=\sum_{k=0}^{T-t-1}(\gamma\lambda)^k\delta_{t+k}$**

基于广义优势估计得到的时刻 t 优势，其中 δ 为时序差分误差，γ 为折扣因子，λ 控制估计的偏差—方差权衡。

</div>

</div>

**直接相关的工作**

- **GRPO**: 代表性的无价值网络方法，通过同一题目多条回答的组内归一化奖励构造优势，训练较高效稳定；但不能利用轨迹内部的价值信息，因此难以对长推理过程进行细粒度信用分配。
- **VAPO**: 本文最直接的价值型参照方法，在价值网络框架中采用长度自适应的广义优势估计和词元级损失，显示出高于无价值方法的潜力；CVPO针对其尚未充分利用轨迹价值方差、同质结果反馈不足及动态题目难度适配的问题展开改进。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

强化学习已能显著提升大语言模型处理高难度数学推理任务的能力，但进一步提升依赖两类更精确的训练决策：一是区分不同生成轨迹各自应获得多强、何种方向的学习信号，二是在模型能力持续变化时选择与当前水平相匹配的题目。若这两类决策不准确，有限训练计算会被低信息量轨迹或已经过易的题目占用，推理性能、鲁棒性与训练效率都会受到限制。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **以 GRPO 为代表的无价值模型方法**：对同一问题采样多条回答轨迹，以组内多条轨迹奖励的相对关系计算优势，而不额外训练逐状态或逐词预测未来回报的价值模型。其优点是训练结构较简洁，但反馈主要来自组内结果比较。
- **以 VAPO 为代表的价值模型方法**：训练价值模型估计生成过程中各状态或词位置的预期回报，再用这些估计进行更细粒度的信用分配，即判断一条推理轨迹中的哪些决策对最终结果贡献更大。论文据既有研究称，训练良好的价值模型具有比 GRPO 一类方法更高的性能上限。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 现有价值型方法对回答轨迹的反馈仍不够精细；当一组轨迹全部正确或全部错误、结果高度同质时，仅靠最终奖励难以产生有区分度的梯度信号，导致不同推理过程受到近似处理，削弱有效学习与进一步提升性能的空间。
- 现有训练常对题目采用固定权重，但题目难度是相对于模型当前能力而言的：随着训练推进，原本困难的题目可能变成中等或简单题。继续无差别训练会降低样本与计算利用效率，并因高难题关注不足而限制模型的推理上限。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有价值型强化学习虽能提供比纯组内奖励更细的信用分配，却尚未充分利用单条轨迹内部价值估计的波动来刻画生成随机性与探索状态，也缺少把这一轨迹级信号同训练过程中不断变化的题目相对难度联合起来的机制。因此，当前方法无法同时做到“按轨迹状态差异化更新”和“按模型当前能力动态选重题目”。

</div>
<div markdown="1"><span>核心问题</span>

能否构造一种统一的价值型策略优化方法：在轨迹层面，根据逐词价值方差及奖励类型自适应调节优势权重，以增强错误轨迹的探索并稳定正确轨迹的收敛；在问题层面，根据训练阶段中的相对难度动态分配题目权重，从而提升数学推理的准确性、鲁棒性和训练效率？

</div>
<div markdown="1"><span>作者直觉</span>

一条轨迹中各词位置的价值估计若起伏较大，意味着模型对后续回报的判断变化明显，可把它理解为生成过程仍在尝试不同方向；起伏较小时，生成更固定或更“僵化”。因此，价值方差可作为比最终对错更细的过程信号：对答错但方差不同的轨迹给予不同探索压力，对答对轨迹则避免过度扰动。另一方面，课程学习类似为学生动态选题——模型进步后，应降低已掌握题目的训练占比，并把资源转向当前既有挑战、又并非完全超出能力范围的问题。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

CVPO建立在PPO式的大语言模型强化学习之上：输入一道问题后，当前策略采样多条回答轨迹，同时价值模型给出各生成位置的状态价值，规则或验证器给出整条轨迹的二元正确性奖励。方法不改变语言模型的自回归生成结构，而是在计算优势时引入两个乘法权重：轨迹级随机性感知权重$W_{\mathrm{S}}$根据同一回答内价值估计的波动及回答正误，分别抑制正确轨迹的过度探索、保留错误轨迹的探索空间；问题级难度权重$W_{\mathrm{D}}$根据每道题近期正确率的Beta后验及训练阶段，提高与模型当前能力匹配的问题权重，并在检测到学习瓶颈后将重点移向更难的问题。加权优势随后进入PPO裁剪目标，更新生成策略。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 采样回答并收集轨迹信号

策略逐词生成回答轨迹$\tau_i$，形成状态序列，并记录价值模型输出的状态价值序列$v_i\in\mathbb{R}^{T_i}$、词元级奖励序列$r_i$和整轨迹二元回报$R(\tau_i)\in\{0,1\}$。同一道问题可采样多条轨迹，以便比较相同提示语境下的价值波动和估计该题的成功率。

<div class="method-step__io" markdown="1">

**输入**：从初始问题分布中采样的问题$q$、当前语言模型策略$\pi_\theta$，以及每道问题对应的实例索引$\mathrm{idx}_i$。<br>
**输出**：批数据$\mathcal{B}=\{(v_i,r_i,\mathrm{idx}_i,\tau_i,R(\tau_i))\}_{i=1}^{B}$。

</div>

**直观理解**：模型先对每道题作答若干次，并为回答中的每一步估计“当前走法最终答对的希望有多大”。这些记录同时告诉算法回答是否正确、推理过程有多摇摆，以及模型目前是否掌握该题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 估计轨迹随机性并修正优势

先计算每条轨迹的价值标准差$\sigma_i=\mathrm{std}(v_i)$，再计算同一问题内的参照均值$\mu_k=|\mathcal{G}_k|^{-1}\sum_{i\in\mathcal{G}_k}\sigma_i$；随后用非对称Sigmoid函数生成$W_{\mathrm{S}}$。对于正确轨迹，价值波动越高，权重越大以强化使其收敛的更新；对于错误轨迹，低波动轨迹受到更强调整，而高波动轨迹的负向约束被减弱，以免过早固定在错误模式中。

<div class="method-step__io" markdown="1">

**输入**：每条轨迹的价值序列$v_i$、整轨迹回报$R(\tau_i)$以及同题轨迹分组$\mathcal{G}_k=\{i\mid\mathrm{idx}_i=k\}$。<br>
**输出**：每条轨迹对应的随机性感知权重$W_{\mathrm{S}}(\mathrm{Var}(\tau_i),R(\tau_i))$。

</div>

**直观理解**：若已经答对却仍在不同推理方向之间摇摆，算法会更强地巩固这条正确路线；若答错但尝试了较多不同方向，算法不会把这些探索一概重罚。需要注意，原文先以标准差$\sigma_i$构造同题参照$\mu_k$，后续权重公式却记为$\mathrm{Var}(\tau)$，因此实现时应依据作者代码或补充材料核实究竟传入方差还是标准差。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 在线估计问题难度并切换课程阶段

每题以$\mathrm{Beta}(1,1)$为均匀先验，将成功数和失败数累加到后验参数，并以其后验均值$\bar{\gamma}_\tau^t$估计当前成功率；算法再依据相对变化$\Delta_\tau^t$检测低正确率区与高正确率区是否同时停滞。初始阶段的$W_{\mathrm{D}}$重点覆盖模型有机会解决但尚未稳定掌握的问题；触发瓶颈后，权重分布移向低正确率题，并令正确率为$1$的已掌握题权重为零。

<div class="method-step__io" markdown="1">

**输入**：每道题历轮采样所得的二元奖励、该题Beta分布参数，以及相邻训练轮的历史记录。<br>
**输出**：问题$q$的动态正确率$\rho_q$、课程阶段$t_c$和难度权重$W_{\mathrm{D}}(\rho_q,t_c)$。

</div>

**直观理解**：难度不是数据集预先贴好的固定标签，而是“当前模型答这道题有多大概率成功”。训练早期先练略有把握的题以获得清晰反馈，进步停滞后再把训练预算转向尚未解决的难题。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 合并权重并执行PPO更新

将两个权重与基础优势相乘得到统一加权优势$A'_{t'}$，并用它替换PPO裁剪代理目标中的原始优势；裁剪概率比仍限制单次策略变化，以避免权重调整导致过大的更新。价值估计、优势估计、策略优化和每题成功率后验在后续轮次中循环更新。

<div class="method-step__io" markdown="1">

**输入**：基础优势$A$、随机性权重$W_{\mathrm{S}}$、难度权重$W_{\mathrm{D}}$，以及新旧策略的词元概率比$r_t(\theta)$。<br>
**输出**：更新后的生成策略$\pi_\theta$及供下一轮使用的价值模型和问题难度统计。

</div>

**直观理解**：两个权重分别回答“这条回答应多大程度被强化或惩罚”和“这道题当前值得投入多少训练资源”。它们只重新缩放学习信号，而PPO仍负责控制模型每次不要改得过猛。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 价值方差与策略梯度幅度上界

$$
\left\|\nabla_{\theta}J(\theta)\right\|_{2}\leq C\left(\sigma_{Q}+\sqrt{\operatorname{Var}(V)}\right)
$$

**符号说明**

- $J(\theta)$：参数为θ的策略优化目标
- $\nabla_{\theta}J(\theta)$：目标关于策略参数的梯度，即策略更新方向与尺度的核心信号
- $C$：策略对数概率梯度二范数的上界，满足相应梯度不超过该常数
- $\sigma_Q$：状态—动作价值Q的标准差，即Var(Q)的平方根
- $\operatorname{Var}(V)$：采样状态上的状态价值函数V的方差

<div class="equation-explanation" markdown="1">

**直观理解**：作者从策略梯度、优势$A=Q-V$以及Cauchy–Schwarz不等式推导出该上界，用于论证价值估计的方差会影响策略梯度可能达到的幅度。因此，依据轨迹质量调节与价值波动相关的优势信号，有望在错误轨迹上保留探索、在正确轨迹上促进稳定；不过该式是上界而非等式，不能据此断言增大价值方差一定带来更优更新。<br>
**原文位置**：第4.1.1节，公式(3)–(13)，最终结论为公式(13)

</div>

</div>

<div class="equation-block" markdown="1">

#### 随机性与难度统一加权优势

$$
A_{t'}'=W_{\mathrm{S}}\!\left(\operatorname{Var}(\tau),R(\tau)\right)\,W_{\mathrm{D}}\!\left(\rho_q,t_c\right)\,A
$$

**符号说明**

- $A_{t'}'$：经过随机性和课程难度共同修正后、用于策略优化的优势
- $A$：修正前的基础优势估计；预备知识部分给出其可由GAE计算
- $W_{\mathrm{S}}$：依据轨迹价值波动和整轨迹正误产生的随机性感知权重
- $\tau$：模型针对问题q生成的完整回答轨迹
- $\operatorname{Var}(\tau)$：轨迹中状态价值估计的波动指标；原文符号写作方差，但参照阈值由标准差计算
- $R(\tau)$：完整轨迹的回报，文中正确回答为1、错误回答为0
- $W_{\mathrm{D}}$：由问题近期正确率和当前课程阶段决定的难度权重
- $\rho_q$：采样问题q最近的正确率
- $t_c$：当前动态课程训练阶段，如初始阶段或瓶颈后的困难题偏置阶段

<div class="equation-explanation" markdown="1">

**直观理解**：该式是CVPO连接两个设计与PPO训练的核心接口：先决定某条回答信号应被放大还是减弱，再决定其所属问题当前应占多少训练权重。因为两项采用乘法组合，任一项接近零都能显著抑制该样本的策略梯度贡献。<br>
**原文位置**：第4.3节，公式(27)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：CVPO仍优化PPO的裁剪代理目标，但将原始优势$\hat A_t$替换为统一加权优势$A'_{t'}$：新旧策略概率比$r_t(\theta)=\pi_\theta(a_t\mid s_t)/\pi_{\theta_{\mathrm{old}}}(a_t\mid s_t)$通过$\operatorname{clip}(r_t,1-\epsilon,1+\epsilon)$限制单轮更新，而$W_{\mathrm{S}}W_{\mathrm{D}}$重新分配不同轨迹和不同问题对梯度的贡献。基础优势可按预备知识中的广义优势估计计算，即由词元奖励、折扣因子$\gamma$、GAE参数$\lambda$及价值函数$V(s)$形成；作者方法的新增部分不是另设一个独立损失，而是修改送入PPO目标的优势尺度。训练上的关键含义是：随机性权重处理同一道题内部不同回答轨迹的探索—收敛平衡，课程权重处理不同问题之间训练预算的分配，PPO裁剪则继续承担稳定更新的约束。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 轨迹价值波动感知模块**

该模块把回答过程中状态价值的离散程度视为生成随机性和探索强度的代理量，并以同一问题下多条轨迹的平均标准差$\mu_k$作相对基准。理论上，在$\|\nabla_\theta\log\pi_\theta(a|s)\|_2\le C$的假设下，策略梯度范数满足$\|\nabla_\theta J(\theta)\|_2\le C(\sigma_Q+\sqrt{\mathrm{Var}(V)})$，说明价值方差会进入更新幅度的上界；但这一上界只建立关联，并不单独证明价值波动必然等同于有益探索。

> 直观理解：价值估计若沿回答大幅变化，表示模型对不同中间状态的前景判断变化较大，作者据此把它当作“尝试不同方向”的可观测信号。同题内比较而非全局比较，可以减少题目本身尺度差异造成的误判。

**2. 正负轨迹非对称优势修正模块**

对$R(\tau)=1$的正确轨迹，$W_{\mathrm{S}}=1+\alpha_P\operatorname{sigmoid}(\lambda_P(\mathrm{Var}(\tau)-\mu_k))$，使高波动正确轨迹获得更大的优势尺度；对$R(\tau)=0$的错误轨迹，$W_{\mathrm{S}}=1-\alpha_N\operatorname{sigmoid}(\lambda_N(\mu_k-\mathrm{Var}(\tau)))$，降低低方差错误轨迹对应权重。$\lambda_P,\lambda_N$控制权重随波动变化的陡峭程度，$\alpha_P,\alpha_N$控制调整幅度；节选未给出这些超参数的具体数值。

> 直观理解：正确答案的目标是减少无谓摇摆并形成稳定策略，错误答案则需要避免因为惩罚过硬而不再尝试新路线，因此两类轨迹不能使用同一种缩放规则。这里所谓“抑制”或“鼓励”最终如何作用，还取决于基础优势$A$的符号：乘大正优势会强化动作，乘小负优势会减轻惩罚。

**3. 贝叶斯动态课程模块**

模块为每道题维护Beta-Bernoulli后验，将二元作答结果递归累积为成功率估计，而不是依赖静态难度标签。若低正确率集合$T_{\mathrm{low}}=\{\tau\mid\bar{\gamma}_\tau^t\le0.3\}$中的变化满足$|\Delta_\tau^t|\le0.05$，且高正确率集合$T_{\mathrm{high}}=\{\tau\mid\bar{\gamma}_\tau^t\ge0.8\}$中的变化满足$\Delta_\tau^t\le0.03$，作者判定出现学习瓶颈并切换$W_{\mathrm{D}}$。初始权重采用参数$k_1=1.6,c_1=-0.2,k_2=2,c_2=1.2$，瓶颈后采用$k'_1=4.1,c'_1=-0.1,k'_2=2,c'_2=0.9$并额外乘$1-\rho_q^2$。

> 直观理解：该模块像一名持续更新判断的教师：它根据模型最近的真实答题记录重估每道题难度。只有简单题和难题的进步都停滞时才改变课程，避免过早把训练集中到几乎无法获得有效反馈的题目上。

**训练与推理**

训练时，首先从训练题目中组成批次，并由旧策略对每题采样一条或多条回答；价值模型逐词估计状态价值，奖励机制判断回答正确与否。随后按问题索引分组，计算轨迹价值标准差及组内参照$\mu_k$，根据正负回报得到$W_{\mathrm{S}}$；同时将每题本轮成功和失败次数更新到Beta后验，以后验均值和相邻轮趋势判断是否触发课程阶段切换，再计算$W_{\mathrm{D}}$。两个权重乘到基础优势上，所得$A'_{t'}$用于PPO裁剪目标更新策略；新的作答记录、价值估计和后验参数进入下一轮，形成在线闭环。

推理时，CVPO训练所得策略与普通自回归语言模型相同：给定问题后按词元生成回答。节选没有说明推理阶段需要继续计算$W_{\mathrm{S}}$、维护Beta后验或执行课程切换，因此这些机制应理解为训练期的优势重加权，而非增加推理解码步骤；推理温度、采样策略、答案验证方式及是否保留价值模型，原文节选均未明确报告。

**复现信息**

公平复现至少需要保留以下设计：每题采用$\mathrm{Beta}(1,1)$成功率先验；低正确率区阈值为$0.3$且停滞阈值为$|\Delta|\le0.05$，高正确率区阈值为$0.8$且放缓阈值为$\Delta\le0.03$，二者同时满足才切换课程；初始难度函数使用$k_1=1.6,c_1=-0.2,k_2=2,c_2=1.2$，瓶颈后使用$k'_1=4.1,c'_1=-0.1,k'_2=2,c'_2=0.9$，并通过$1-\rho_q^2$使$\rho_q=1$的题权重为零。随机性模块必须在同一问题的多条轨迹内计算参照$\mu_k$，否则无法实现文中所述的组内归一化。

节选未明确报告$\alpha_P,\alpha_N,\lambda_P,\lambda_N$的具体取值、每题采样轨迹数$k$、批大小$B$、PPO裁剪系数$\epsilon$、折扣与GAE参数、优化器或学习率。另一个需源代码核验的关键歧义是：原文定义$\sigma_i=\mathrm{std}(v_i)$并以其均值构造$\mu_k$，但权重函数输入写作$\mathrm{Var}(\tau)$；直接比较方差与标准差均值在量纲上不一致，复现时不应自行假定，应核对作者实现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- DAPO-Math-17k：强化学习训练集。原文给出名称但未在节选中说明题目来源、难度构成、具体划分方式或清洗后的样本数；其作用是统一训练各强化学习方法。
- AIME 2024 与 AIME 2025：高难度数学竞赛测试集，用于检验模型处理复杂、多步推理问题的能力；二者均只用于评测，原文未明确报告过滤规则或测试题数。
- AMC 2023、AMC 2024 与 MATH-500：覆盖相对广泛数学难度的评测集。AMC 中需要理解图像才能作答的问题被删除，以避免把视觉理解能力混入纯文本推理评估；MATH-500 的具体划分沿用既有数据集，但节选未进一步说明。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**avg@32 accuracy**

每道题独立生成 32 次回答后计算的平均正确率。最终答案必须置于 $\boxed{\cdot}$ 中，或在新行的“Answer:”之后；答案与标准答案精确匹配才算正确。该指标反映重复采样下单次生成的平均成功概率，而不是 pass@32 所表示的“32 次中至少一次正确”。 （越高越好，因为更高数值表示模型在重复生成中更频繁地产生正确最终答案。）

</div>
<div class="metric-item" markdown="1">

**轨迹级价值方差分布**

统计回答轨迹内 token 级价值估计的波动，并观察其分布是否向较高方差移动。论文将较高价值方差解释为更强的生成探索，即模型在推理过程中尝试更多可能路径；它是机制诊断量，不是答案正确率。 （论文通常将适度升高解释为探索增强，但并非无条件越高越好；过大的方差系数会扩大策略更新，可能损害收敛和高难任务表现。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen2.5-7B 在五个数学基准上的总体准确率比较

<div class="result-value" markdown="1">

完整 CVPO 在 AIME24、AIME25、AMC23、AMC24 和 MATH500 上的 avg@32 分别为 0.237、0.133、0.720、0.512 和 0.802，五项均为表中最高值。作者报告其相对各数据集第二名分别提高 9.3%、3.1%、25.2%、12.9% 和 13.7%；结合表格数值，这些实际是准确率的绝对百分点差，例如 AIME24 为 $0.237-0.144=0.093$，不应理解为相对百分比增幅。

</div>

结果表明，在论文给定训练配置和重复采样协议下，完整 CVPO 的跨数据集表现优于列出的基础模型、GRPO（ASYN）、VAPO 和单组件变体，而且收益同时出现在较难的 AIME 与较广泛的 AMC、MATH500 上。这支持两个模块组合有效，但由于没有多随机种子方差或显著性检验，尚不能判断增益在不同训练运行中是否稳定；它也不能证明 CVPO 优于未纳入实验的其他强化学习算法。

<div class="result-source" markdown="1">

来源：第 6.1 节；具体原始分数见表 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Specifically, it achieves improvements of 9.3%, 3.1%, 25.2%, 12.9%, and 13.7% over the second-best methods on AIME24, AIME25, AMC23, AMC24, and MATH500, respectively.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### AIME 2024 上超过 2000 个训练步骤的学习过程

<div class="result-value" markdown="1">

图 2 的作者分析称，CVPO、VAPO 和 GRPO（ASYN）均训练超过 2000 步；CVPO 在训练早期较快提升，并在约 1500 步后仍继续提高准确率，而对照方法的曲线整体较弱。

</div>

该曲线关注的不只是最终分数，还检验训练策略是否能在中后期突破平台。作者将持续提升归因于早期侧重约 50% 正确率的中等难题、随后增加难题权重，并用轨迹方差修正优势估计。不过曲线上的共同变化只能提供与机制一致的证据，不能单独建立“课程切换导致 1500 步后提升”的因果关系；节选也未提供各步的精确数值或误差带。

<div class="result-source" markdown="1">

来源：图 2及第 6.1 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

As a result, CVPO continues to improve in accuracy after 1500 training steps, showing its more effective learning strategy.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 不同训练算法的轨迹级价值方差分布

<div class="result-value" markdown="1">

图 3 显示，从 Qwen2.5-7B 基础模型到 GRPO（ASYN）、VAPO，再到 CVPO，轨迹级价值方差分布逐渐向更高值移动，其中 CVPO 的右移最明显。原文未明确报告均值、中位数或分布距离等数值。

</div>

在论文的理论与度量解释下，分布右移意味着模型在回答轨迹中进行更强探索，因而可能尝试更多推理路径；这为 CVPO 的随机性机制提供过程层证据。但价值方差是代理指标，高方差本身不保证推理正确，也可能来自不稳定更新。需要结合表 1 的准确率，才能说明这里的探索增强至少与更好任务表现同时出现。

<div class="result-source" markdown="1">

来源：图 3及第 6.2 节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

This shift in value-variance distribution towards higher values indicates a greater degree of exploration in the generated response trajectories, which can potentially assist models to generate correct answers by considering more possible pathways.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 结果仅基于 Qwen2.5-7B、单一训练集和数学任务；节选没有更大或不同模型、非数学推理任务及分布外评测，因此不能确认方法是否具有模型规模与领域普适性。
- 实验未明确报告多随机种子结果、置信区间或显著性检验，图 3 至图 5 也缺少关键精确数值。GRPO 对照还是为避免长度坍缩而采用的异步变体，因此对标准 GRPO 的优劣不能直接下结论；价值方差与探索之间的关系主要是代理度量和相关性证据。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Qwen2.5-7B：未经这些强化学习算法增强的基础模型，用来衡量后训练带来的净收益，并在轨迹价值方差分析中作为低探索水平参照。
- VAPO：已有的价值模型强化学习方法，也是论文最重要的同类强基线；与 CVPO 的比较主要检验方差自适应和动态课程设计是否超出一般价值引导训练的效果。
- GRPO（ASYN）：不依赖价值模型的单步异步 GRPO 变体，用于比较价值式与无价值式算法。作者没有采用通用 GRPO，是因为实验中出现严重的响应长度坍缩，因此该比较不能直接等同于标准 GRPO。
- CVPO 单组件变体：分别仅保留随机性感知优势修正或仅保留动态课程加权，用于隔离两个核心组件的独立贡献；它们属于消融对照，而不是外部已有方法。

**实验想回答的问题**

- 在相同的 Qwen2.5-7B 起点和数学强化学习训练集上，CVPO 是否比价值模型方法 VAPO 与无价值模型方法 GRPO（ASYN）取得更高且更稳定的数学推理准确率？
- CVPO 的随机性感知优势修正和动态课程加权是否分别有效，以及它们是否确实改变了轨迹探索强度与训练期间关注的问题难度？

**实验实现**

所有方法以 Qwen2.5-7B 为基础，在 DAPO-Math-17k 上训练，并以规则奖励监督最终答案：精确匹配标准答案得 $+1$，否则得 $-1$。训练使用 8 个服务器节点、每节点 8 张 NVIDIA A800；AdamW 的 actor 与 critic 学习率分别为 $1\times10^{-6}$ 和 $2\times10^{-6}$，训练批量为 256，每个 rollout 批次对每题生成 16 个响应，最大响应长度为 6144 token。作者未使用 KL 约束，理由是其会限制长推理轨迹上的策略更新。价值模型同样从 Qwen2.5-7B 初始化，并选用价值损失小于 1、解释方差大于 0 的检查点。评测对每题尝试 32 次并报告 avg@32；节选未明确报告随机种子、置信区间、显著性检验、解码温度及各测试集清洗后的规模。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 分别只启用随机性感知优势修正或动态课程加权 | 仅启用随机性修正时，AIME24、AIME25、AMC23、AMC24、MATH500 的 avg@32 为 0.188、0.100、0.676、0.497、0.765；仅启用动态课程时分别为 0.162、0.065、0.538、0.412、0.558。两者在五项上均高于 VAPO 的 0.144、0.046、0.441、0.260、0.452，而且仅随机性修正始终优于仅动态课程。 | 该消融分别隔离轨迹层方差修正和问题层课程加权，说明两个组件单独加入都能超过同类价值式基线；随机性模块贡献更大。完整 CVPO 又高于两个单组件版本，支持二者具有互补性。不过各变体是否完全共享其余超参数和训练随机性，节选未明确报告，因此差值仍可能部分受优化条件影响。 | 表 1<br><span class="experiment-evidence">VAPO 0.144 0.046 0.441 0.260 0.452
CVPO (only Stochasticity) 0.188 0.100 0.676 0.497 0.765
CVPO (only Dynamic Curriculum) 0.162 0.065 0.538 0.412 0.558</span> |
| 改变随机性感知优势修正中的价值方差系数 | 表 1 报告方差系数为 0.3 的完整 CVPO 在五项测试上达到 0.237、0.133、0.720、0.512 和 0.802。图 4 进一步显示，系数升高时 AMC 表现总体继续改善，但 AIME 在越过某一交叉点后下降；原文未明确报告图中其他系数及对应精确分数。 | 该实验隔离“方差对优势和策略损失的放大强度”。较大系数会使策略更新更激进，能够增强探索并帮助相对容易的 AMC，但可能破坏收敛，使模型难以适应需要精细长推理的 AIME。因此 0.3 的强结果不能推出系数越大越好，而是表明需在探索和稳定性之间调节。 | 表 1；趋势分析见图 4及第 6.2 节<br><span class="experiment-evidence">CVPO (w/ 0.3 variance coeff) 0.237 0.133 0.720 0.512 0.802</span> |

**定性案例**

- 图 5 给出训练问题难度分布的可视化机制案例：不使用动态难度加权时，训练样本逐渐集中在简单题，形成作者所称的“简单题陷阱”；使用该机制后，早期重点落在当前正确率约 50% 的问题上，并在约第 1000 步出现瓶颈时提高困难题权重、降低简单题权重。该图解释了课程模块如何改变训练关注点，但未展示具体题目的推理文本，因此属于训练动态案例而非答案级错误分析。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出面向数学推理的方差自适应策略优化与动态课程学习，是强化学习后训练提升 LLM 推理能力的方法。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`9f10e5ecfbc6aadee56cc01faf7dd39d6082bc3b7d086cf30a4a7aa8a06d9865`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
