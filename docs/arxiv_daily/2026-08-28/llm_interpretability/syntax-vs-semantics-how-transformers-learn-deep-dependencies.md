---
title: "[论文解读] Syntax vs. Semantics: How Transformers Learn Deep Dependencies"
description: "[arXiv 2608.26139][LLM 机制与可解释性] 原文未明确报告。"
arxiv_id: "2608.26139"
announcement_date: "2026-08-28"
primary_category: "llm_interpretability"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-28T11:41:34.453157+00:00"
source_sha256: "e335490519abf27bc7fcec808d351ec9f54978716a98d2057d35ed85d0ac8092"
tags:
  - "LLM 机制与可解释性"
  - "LLM Reasoning"
  - "LLM 其他"
  - "Transformer"
  - "深层依赖"
  - "梯度饥饿"
  - "训练动力学"
  - "机制可解释性"
  - "抽象语法树"
  - "变量绑定"
  - "思维链"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 机制与可解释性 · arXiv 2608.26139</p>

# Syntax vs. Semantics: How Transformers Learn Deep Dependencies

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-28</span>
<span><strong>作者</strong> Jiangrui Zhao, Xiaoting Du</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> 原文页首未识别</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.26139v1) · [PDF 下载](https://arxiv.org/pdf/2608.26139v1) · **关键词** Transformer, 深层依赖, 梯度饥饿, 训练动力学, 机制可解释性, 抽象语法树, 变量绑定, 思维链<br>
**代码**: [https://github.com/jr-zhao/Deep-Dependencies/tree/main](https://github.com/jr-zhao/Deep-Dependencies/tree/main)

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

本文属于大语言模型训练动力学与机制可解释性研究，关注 Transformer 如何从序列数据中学会跨越局部词元模式的深层依赖。已有观察表明，模型通常先掌握高频、局部的表面统计规律，随后才可能突然表现出变量绑定、远距离关联和结构推理能力；论文将这种先后次序视为优化过程中的梯度竞争，而非 Transformer 架构原则上无法表达深层关系。由于自然语言中的潜在关系结构缺乏无歧义标注，作者主要以源代码及其抽象语法树作为可控代理：代码词元提供表面序列，抽象语法树则提供可核验的关系拓扑。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**深层依赖（Deep Dependencies）**

指不能仅凭相邻词元或高频共现判断、必须恢复潜在关系结构才能处理的关联，例如远距离变量使用与其定义之间的绑定。这里的“深层”强调关系跨越表面位置并依赖结构，而不只是网络层数较多。

</div>
<div class="concept-item" markdown="1">

**梯度饥饿（Gradient Starvation）**

当多个可学习信号共同影响损失时，频繁且高曲率的局部模式会主导早期参数更新，使稀疏、较弱的语义依赖信号受到抑制。论文用它解释模型为何先学习表面规律，而深层推理能力要到临界阶段才突然显现。

</div>
<div class="concept-item" markdown="1">

**抽象语法树（Abstract Syntax Tree, AST）**

AST 将程序表示为树状结构，其中节点对应变量、表达式或语句等成分，边表示明确的组合与从属关系。本文把它作为潜在语义拓扑的受控近似，以便判断模型注意力或内部表示是否恢复了真实结构。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究对象是从玩具 Transformer、Pythia 中间训练检查点到 Llama-3.1-8B 和 Qwen2.5-Coder-7B 等不同规模模型。输入主要是包含局部统计规律与跨位置结构关系的词元序列，尤其是具有可提取 AST 的源代码；期望输出或内部行为是正确恢复关系拓扑、完成变量绑定等结构推理。核心假设是标准 Transformer 的表示几何中已经存在实现深层依赖所需的潜在线性子空间，因此问题不在于表达能力是否存在，而在于训练时表面统计梯度会不会压制稀疏语义梯度，以及显式写出中间推理步骤是否能增加有效的梯度路径。作者据此考察依赖回路的阶段性形成，并把思维链视为将隐式中间状态外化为具体词元、从而部分绕过梯度抑制的一种机制。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Pezeshki et al. (2021), Gradient Starvation**: 为“强特征对应的优化信号压制弱特征学习”提供既有概念基础；本文将该现象具体应用于 Transformer 中表面统计与深层语义依赖之间的竞争。
- **Olsson et al. (2022), Transformer Circuits / Induction Heads**: 代表对 Transformer 注意力回路及其形成过程的机制研究；本文进一步追问内容无关的关系算子与可靠指针式绑定在什么优化条件下出现。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原文未明确报告。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- 原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 原文未明确报告。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

原文未明确报告。

</div>
<div markdown="1"><span>核心问题</span>

原文未明确报告。

</div>
<div markdown="1"><span>作者直觉</span>

原文未明确报告。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文的方法首先把 Transformer 学习深层依赖的过程建模为两个功能子空间之间的竞争：局部、高频模式构成句法子空间 $\mathcal{U}_{syn}$，跨位置的变量绑定或程序图依赖构成语义子空间 $\mathcal{U}_{sem}$。在损失函数的局部二次近似下，作者用 Hessian 曲率差异说明句法方向为何在训练初期主导梯度；随后分析注意力 softmax 饱和如何进一步压低正确语义位置的梯度；当抑制减弱后，注意力交互矩阵 $W_{QK}=W_Q^TW_K$ 才逐渐对齐到表示依赖边的低秩拓扑算子。作者以对齐率 $\rho(t)$ 描述这一过程，并将学习划分为句法主导、交叉过渡和系统性涌现三个阶段。

从端到端角度看，输入是含局部格式规律与远程依赖的序列 $\mathcal{S}=\{x_1,\ldots,x_T\}$，模型先容易学会分隔符、邻近共现等表面模式，而后才可能形成从使用位置指向信息源位置的绑定回路。训练时，普通终点监督需要把误差信号沿完整推理链反传，容易遭遇梯度饥饿；链式思维监督则把中间状态 $z$ 写成可预测 token，并增加局部损失 $\mathcal{L}_z$，从而提供不依赖最终答案是否正确的并行梯度通路。直观地说，模型原本要一次完成一条很长的“寻址链”，而显式中间步骤把它拆成多个较短、较容易学习的查找动作。摘要还声称提出了拓扑对齐的对比目标，但所给章节未包含其公式、样本构造或完整训练算法，因此此处不能据此重建该目标。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 区分表面模式与深层依赖

将预测所依赖的特征概念性地分为句法功能 $\mathcal{F}_{syn}$ 与语义功能 $\mathcal{F}_{sem}$；前者对应局部统计，后者对应查询位置到程序图信息前驱的拓扑映射。

<div class="method-step__io" markdown="1">

**输入**：含有局部高频标记和远程变量绑定关系的序列 $\mathcal{S}=\{x_1,\ldots,x_T\}$。<br>
**输出**：两个竞争的功能及参数子空间 $\mathcal{U}_{syn}$、$\mathcal{U}_{sem}$，以及需要恢复的语义依赖边。

</div>

**直观理解**：同一训练样本同时提供“格式长什么样”和“信息应从哪里取”两类线索；前者通常更频繁、更容易，因而会先被模型利用。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 刻画梯度饥饿与注意力抑制

在 Hessian 特征基中分解梯度，并利用 $\lambda_{syn}\gg\lambda_{sem}$ 推出更新主要沿句法方向；若句法位置令 softmax 饱和，则语义分数梯度还会随 $A_{sem}$ 近似线性缩小，并随分数差 $s_{syn}-s_{sem}$ 指数衰减。

<div class="method-step__io" markdown="1">

**输入**：当前参数残差 $e=\theta-\theta^*$、损失 Hessian $H$，以及正确语义位置和干扰句法位置的注意力分数。<br>
**输出**：语义方向有效更新被遮蔽的“梯度屏障”，解释深层依赖为何长期不被稳定学习。

</div>

**直观理解**：优化器像是优先沿最陡的坡下山，容易先把表面规律学得很自信；一旦注意力几乎全押在错误但显眼的位置上，正确位置收到的纠错信号反而接近于零。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 重建语义拓扑并监测相变

注意力交互矩阵的梯度由外积 $x_jx_i^T$ 累积；在噪声零均值且与误差信号近似不相关的假设下，其期望方向对齐到 $M_{sem}=\mu_{use}\mu_{src}^T$，再用 $\rho(t)$ 衡量当前更新与该拓扑算子的几何一致性。

<div class="method-step__io" markdown="1">

**输入**：已脱离严重饱和的注意力头、token 表示 $x=\mu+\delta$，以及反向误差信号 $\gamma_{ji}=\partial\mathcal{L}/\partial s_{ji}$。<br>
**输出**：实现“使用位置指向来源位置”的低秩绑定回路，以及从句法阶段到系统性语义阶段的相位判定。

</div>

**直观理解**：若许多样本都要求同一种寻址关系，梯度会反复强化对应的“从这里看向那里”方向；当这种方向足够稳定时，性能可能突然提升，而不是均匀缓慢改善。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 用显式推理轨迹缩短信用分配

推理时将困难条件分解为 $P(z\mid x)P(y\mid x,z)$；训练时使用 $\mathcal{L}_{total}=\mathcal{L}_{y\mid z}+\mathcal{L}_z$，使中间状态损失直接向绑定回路注入局部梯度。

<div class="method-step__io" markdown="1">

**输入**：原始输入 $x$、中间推理状态 $z$、最终输出 $y$，以及包含中间步骤的链式思维监督。<br>
**输出**：显式中间 token、最终预测，以及一条不完全依赖终点误差反传的并行语义学习通路。

</div>

**直观理解**：这相当于不仅批改最终答案，还逐步批改草稿中的关键中间结论；即使最后一步暂时做错，前面的寻址关系仍能得到有效训练。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 句法与语义子空间的梯度范数比

$$
\frac{\lVert g_{syn}\rVert_2}{\lVert g_{sem}\rVert_2}\approx\frac{\lambda_{syn}}{\lambda_{sem}}\sqrt{\frac{m_{syn}}{m_{sem}}}\gg1
$$

**符号说明**

- $g_{syn}$：总梯度在句法子空间上的分量
- $g_{sem}$：总梯度在语义子空间上的分量
- $\lambda_{syn}$：句法子空间中代表性的 Hessian 曲率或特征值尺度
- $\lambda_{sem}$：语义子空间中代表性的 Hessian 曲率或特征值尺度
- $m_{syn}$：句法子空间的有效维数
- $m_{sem}$：语义子空间的有效维数

<div class="equation-explanation" markdown="1">

**直观理解**：在两个子空间的参数残差投影规模相近时，曲率更大且有效维数更高的一侧会贡献更大的梯度。该式因此给出“梯度饥饿”的第一层原因：训练更新主要用于拟合句法统计，语义方向即使包含任务所需信息，也只能获得较慢的优化进展；这一结论依赖文中的谱差异假设，而不是对任意 Transformer 都无条件成立。<br>
**原文位置**：第2.2节，命题2.2，公式(1)

</div>

</div>

<div class="equation-block" markdown="1">

#### 语义拓扑对齐率

$$
\rho(t)=\frac{\left\langle\nabla_{W_{QK}}\mathcal{L},M_{sem}\right\rangle_F^2}{\left\lVert\nabla_{W_{QK}}\mathcal{L}\right\rVert_F^2\left\lVert M_{sem}\right\rVert_F^2+\epsilon},\qquad M_{sem}=\mu_{use}\mu_{src}^T
$$

**符号说明**

- $\rho(t)$：训练时刻 $t$ 的梯度—拓扑对齐率，取值位于零到一之间
- $W_{QK}=W_Q^TW_K$：由查询与键投影构成的注意力双线性交互矩阵
- $\nabla_{W_{QK}}\mathcal{L}$：损失对注意力交互矩阵的梯度
- $M_{sem}$：编码目标语义依赖边的理想拓扑算子
- $\mu_{use}$：使用或查询位置在低维信号子空间中的平均表示
- $\mu_{src}$：信息来源位置在低维信号子空间中的平均表示
- $\langle\cdot,\cdot\rangle_F$：矩阵的 Frobenius 内积
- $\lVert\cdot\rVert_F$：矩阵的 Frobenius 范数
- $\epsilon$：防止分母为零的正稳定项

<div class="equation-explanation" markdown="1">

**直观理解**：该式计算当前梯度矩阵与正确依赖边之间的平方余弦相似度：$\rho(t)$ 越高，说明优化更新越集中于建立目标绑定，而不是继续拟合无关局部统计。作者把 $\rho(t)$ 越过稳定阈值 $\tau_{stable}$ 解释为语义回路的系统性涌现，并以此将类似 grokking 的突然泛化提升解释为梯度几何结构的重组。<br>
**原文位置**：第2.5节，公式(4)；目标算子定义紧邻公式之前

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：所给章节明确写出的监督分解是 $\mathcal{L}_{total}=\mathcal{L}_{y\mid z}+\mathcal{L}_z$：$\mathcal{L}_{y\mid z}$ 训练模型在已有中间状态 $z$ 时预测最终答案 $y$，$\mathcal{L}_z$ 则直接监督中间推理状态。优化上的关键不是简单增加更多 token 损失，而是让 $\nabla_\theta\mathcal{L}_z$ 构成一条独立于最终答案反传质量的局部梯度路径，从而在隐式语义梯度接近消失时提高语义子空间中的有效更新。

摘要提到“topology-aligned contrastive objective”，并称其用于纠正梯度几何；然而给定来源没有提供该对比目标的数学表达、正负样本定义、权重系数或它与交叉熵的组合方式。末尾仅给出部分结果行，不能据此可靠恢复目标。因此，对该论文完整训练目标及其所谓拓扑对齐对比项，原文在所供章节中未明确报告。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 曲率竞争与 softmax 梯度屏障**

作者假设句法子空间具有更大的有效曲率 $\lambda_{syn}$，使其梯度范数显著高于语义子空间；句法注意力达到 $A_{syn}\approx1$ 后，正确位置的 $A_{sem}\approx0$，从而使 $\left|\partial\mathcal{L}/\partial s_{sem}\right|$ 指数趋零。这是对训练动力学的机制性描述，而非额外加入 Transformer 的网络层。

> 直观理解：该模块解释了“模型不是完全看不到语义线索，而是语义线索得不到足够更新”这一核心现象，因此能够区分数据中缺少信息与优化过程压制信息两种失败原因。

**2. 低秩拓扑对齐与对齐率**

将理想依赖边编码为非对称秩一算子 $M_{sem}=\mu_{use}\mu_{src}^T$，并比较 $\nabla_{W_{QK}}\mathcal{L}$ 与 $M_{sem}$ 的平方余弦相似度 $\rho(t)$。作者用阈值 $\tau_{low}$ 和 $\tau_{stable}$ 区分句法主导、交叉和稳定语义涌现三个区域，但所给正文没有给出阈值的具体数值或估计程序。

> 直观理解：它检查模型的更新是否真正朝着正确的“指针方向”移动，而不只观察最终答题准确率；因此可用于识别能力突然出现之前的内部结构变化。

**3. 链式思维的局部梯度注入**

隐式监督的梯度必须穿过从输入到最终答案的完整计算链，而链式思维增加中间状态目标 $\mathcal{L}_z$；该项不依赖最终输出 $y$ 的反向信号，因此可在下游依赖弱或噪声大时直接训练中间绑定。作者据此预测：深层组合任务的相对收益较大，浅层任务的收益接近于一。

> 直观理解：显式步骤既是推理时的外部记忆，也是训练时的阶段性答案。它让模型先学会相邻节点之间的指针传递，再通过更深层和残差流逐步完成远距离取值。

**训练与推理**

训练阶段可分为诊断性描述与可操作的链式思维监督两部分。对于普通隐式训练，模型直接从序列预测终点 $y$，其误差必须沿多跳依赖反传；局部句法特征因高曲率先被拟合，并可能使注意力落入 $A_{syn}\approx1$ 的饱和区。随着句法损失趋于饱和、冲突模式或正则化削弱表面捷径，语义位置重新获得梯度；随后 $W_{QK}$ 的更新通过样本外积逐步对齐 $M_{sem}$。若使用显式轨迹，则同时预测中间状态 $z$ 和答案 $y$，以 $\mathcal{L}_{y\mid z}+\mathcal{L}_z$ 更新参数，并可跟踪 $\rho(t)$ 判断绑定回路是否由句法主导阶段跨入稳定语义阶段。

推理阶段，隐式方案试图直接建模 $P(y\mid x)$，需要网络内部一次完成多跳检索；链式思维方案先生成 $z$，再根据 $x$ 与 $z$ 生成 $y$，对应 $P(z\mid x)P(y\mid x,z)$。对于依赖链 $i\to j\to k$，理论预测模型先形成从使用位置 $i$ 指向中间指针 $j$ 的回路；残差更新 $x_i\leftarrow x_i+W_{OV}x_j$ 将 $j$ 的信息写入位置 $i$，更深层随后利用该内容解析 $j\to k$。这是一项关于回路形成顺序的理论预测，不应误读为所有模型都被硬编码执行固定的两阶段寻址算法。

**复现信息**

公平理解该方法所必需的结构量包括注意力交互矩阵 $W_{QK}=W_Q^TW_K$、值—输出组合 $W_{OV}$、语义目标算子 $M_{sem}=\mu_{use}\mu_{src}^T$，以及按训练时间计算的对齐率 $\rho(t)$。理论成立还依赖三项重要条件：句法曲率满足 $\lambda_{syn}\gg\lambda_{sem}$；表示可分为低维信号 $\mu$ 与零均值上下文噪声 $\delta$；反向误差 $\gamma$ 与前向噪声 $\delta$ 在数据分布上近似不相关。作者称这些条件分别在附录中进行了经验核验，但所给来源未包含核验方法和结果。

所给章节没有报告优化器、学习率、批大小、训练轮数、对齐阈值 $\tau_{low}$ 与 $\tau_{stable}$ 的取值、$\mu_{use}$ 和 $\mu_{src}$ 的估计方式，也没有给出拓扑对齐对比目标的实现。因此这些内容均不能从当前材料补全，复现完整方法时必须回查论文的方法后续章节及附录。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 合成代码数据：包含变量赋值（绑定定义）和算术运算（绑定使用），用于在可控环境中分离表层语法标记与变量依赖语义，并验证梯度动力学。
- Pythia 在 The Pile 上的预训练检查点：使用 Pythia-160M 分析对齐比率 $\rho(t)$ 与 CoT 信号传播，使用 Pythia-1.4B 分析指针形成；依托密集的中间检查点进行纵向训练动态分析。
- 受控自然语言实体绑定任务：使用传递身份链作为依赖探针，用于检验去除高频功能词是否也会加速语义对齐，从而判断机制是否不限于代码语法。数据规模、划分和具体样本数量原文未明确报告。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**语法 token 与变量 token 的平均 embedding 梯度范数**

分别衡量语法 token 集合 $\mathcal{T}_{\mathrm{syn}}$ 和变量 token 集合 $\mathcal{T}_{\mathrm{sem}}$ 接收的误差信号强度，用于识别变量语义梯度是否在早期被压制。 （不存在统一的高低优劣；变量 token 梯度在语义任务中应随有效依赖学习而增强，早期持续接近语法基线则支持梯度饥饿解释。）

</div>
<div class="metric-item" markdown="1">

**语义对齐比率 $\rho(t)$**

衡量更新方向中与语义依赖拓扑对齐的成分相对于竞争性语法成分的比例；在 Pythia 中通过有效梯度 $\nabla_{\mathrm{eff}}\approx(\nabla_{W_Q}\mathcal{L})^TW_K+W_Q^T(\nabla_{W_K}\mathcal{L})$ 重构因分解参数化而无法直接观测的注意力几何更新。 （通常越高越好，因为较高的 $\rho(t)$ 表示更新更偏向语义依赖结构；跨过临界阈值时应伴随依赖能力出现。）

</div>
<div class="metric-item" markdown="1">

**选择性比率 $\mathcal{R}$**

定义为 $\mathcal{R}=\frac{\|\nabla_{x_{src}}\mathcal{L}\|_F}{\|\nabla_{\mathcal{S}}\mathcal{L}\|_F+\epsilon}$，其中 $x_{src}$ 是真实因果祖先，$\mathcal{S}$ 是完整输入序列，$\|\cdot\|_F$ 是 Frobenius 范数，$\epsilon$ 是稳定化小常数；它衡量梯度能量是否集中到真正的因果来源。 （越高越好，表示模型对真实祖先更敏感；在不同链深度下保持较高值支持 CoT 恢复局部学习信号。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 小型 Transformer 的梯度饥饿与阶段性学习

<div class="result-value" markdown="1">

训练呈现两阶段过程：早期变量 token 的梯度在高语义损失下仍被压制；语法梯度衰减且注意力模式不稳定后，变量梯度突然上升，表现为语义依赖学习的相变。

</div>

这说明模型并非完全没有学习变量依赖，而是早期误差信号主要被表层语法竞争遮蔽，直到语法预测变得足够容易后，语义信号才获得有效更新通道。该图支持梯度饥饿机制，但仅凭训练曲线不能单独证明所有大型语言模型都遵循同一因果机制。

<div class="result-source" markdown="1">

来源：Figure 2，Section 3.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In the early phase, despite large semantic errors reflected by a high loss, gradients on variable tokens (blue curve) remain suppressed and comparable to the syntactic baseline, consistent with gradient starvation: under Softmax Saturation (Section 2.3), semantic errors fail to propagate to the embeddings.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### Pythia-160M 中对齐比率 $\rho(t)$ 的纵向变化

<div class="result-value" markdown="1">

对齐比率早期接近零，随后经历不稳定的交叉阶段，并在后期持续上升；作者将后期上升解释为注意力交互矩阵逐步锁定低秩语义算子 $M_{\mathrm{sem}}$。

</div>

该结果把小模型中的梯度竞争现象延伸到真实预训练模型检查点：语义结构不是从训练一开始就稳定形成，而可能经历先被语法噪声掩盖、再逐渐系统化的过程。它支持对齐比率作为诊断指标，但并未提供与其他独立结构指标的完整定量对照。

<div class="result-source" markdown="1">

来源：Figure 5，Section 4.1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Figure 5 reveals a distinct non-monotonic transition.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 隐式推理与 CoT 的长程信号传播

<div class="result-value" markdown="1">

随着链深度增加，隐式推理中的真实因果祖先信号快速衰减；CoT 通过逐步预测中间结果维持较高的梯度选择性，减轻长程梯度瓶颈。

</div>

CoT 的作用在这里不是简单增加输出文字，而是把一个难以跨越多层传播的远程依赖拆成多个局部预测，使监督信号更接近当前要学习的中间关系。该结果支持 CoT 能改善信号传播的机制性解释，但不等于证明 CoT 在所有任务或最终准确率上必然优于隐式推理。

<div class="result-source" markdown="1">

来源：Figure 7，Section 4.3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

In contrast, CoT (green) effectively short-circuits this bottleneck.

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

- Control 模型：作为未进行梯度干预的标准训练参照，用于比较语法抑制、变量扰动和语法移除的因果影响。
- Suppress Syntax：对语法 token 的梯度进行人为屏蔽，即令 $\nabla_{\mathrm{syn}}\to 0$，用于测试降低非语义梯度竞争是否会提高 $\rho(t)$ 并加速依赖学习。
- Noisy Variables：向变量 token 的梯度注入噪声，用于破坏语义对齐方向，检验语义梯度质量下降是否延迟推理结构出现。
- Implicit 与 CoT：分别表示不显式输出中间步骤和显式生成中间推理步骤，用于比较长程隐式梯度传播与局部逐步监督。

**实验想回答的问题**

- 小型合成代码 Transformer 是否表现出梯度饥饿、Softmax 饱和门控，以及由语义对齐比率 $\rho(t)$ 控制的阶段性依赖学习？
- 这些机制是否能在真实语言模型中复现，并解释指针式依赖形成与 CoT 对长程梯度信号的改善？

**实验实现**

实验先在小型 Transformer 上训练合成代码，并记录损失、分组梯度和注意力分配；课程学习先训练变量赋值，随后在 step 1500 引入加法任务。因果干预包括屏蔽语法梯度、扰动变量梯度，以及移除高频语法标记。随后在 Pythia-160M 和 Pythia-1.4B 的中间检查点上分析对齐比率、注意力指针和梯度显著性；指针探针使用代码中的递归变量赋值链与自然语言中的传递身份链，CoT 分析比较隐式模式和显式中间步骤模式。原文未明确报告完整的数据规模、训练轮数、随机种子、评测划分及统计显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 语法梯度屏蔽、Control 与变量梯度噪声注入 | 语法梯度屏蔽提高语义对齐比率并加速对齐；变量梯度噪声降低 $\nabla_{W_{QK}}\mathcal{L}$ 与 $M_{\mathrm{sem}}$ 的相关性、降低 $\rho(t)$，从而延迟语义出现。 | 这组对照分别削弱语法竞争和破坏语义方向，形成方向相反的操纵。如果两者变化确实对应相反的学习速度，就比单纯观察相关曲线更能支持 $\rho(t)$ 是依赖学习的重要中介。不过原文以图示和定性描述为主，未报告完整数值效应量。 | Figure 4，Section 3.3<br><span class="experiment-evidence">When gradients associated with syntactic tokens are suppressed (red), the update direction becomes less dominated by non-semantic components, which increases the alignment ratio $\rho(t)$ and accelerates alignment with semantic dependency structure.</span> |
| 语法标记移除与保留语法的 Control | 移除高频语法标记后，模型显著更早退出早期优化平台；在受控自然语言实体绑定任务中，移除高频功能词也观察到类似加速。 | 该消融检验的是数据输入层面的语法竞争，而不是参数梯度层面的直接屏蔽。两类任务都出现加速，提示逻辑密度和结构信号的相对比例可能影响依赖学习；但移除 token 也可能改变输入分布和任务难度，因此不能把全部效果唯一归因于梯度饥饿。 | Figure 4，Section 3.3<br><span class="experiment-evidence">Similarly, the syntax-free setting (orange) exits the early optimization plateau substantially earlier, suggesting that syntactic competition itself contributes to delayed dependency learning.</span> |

**定性案例**

- Pythia-1.4B 的指针形成探针比较了递归代码赋值链（如 `a = 42; b = a;`）与自然语言传递身份链（如 `The Alpha is the Bravo.`）。自然语言中的注意力头在训练过程中呈稳定的对角结构，后期第一列注意力增强，被解释为通过迭代传播形成多跳聚合；代码中的引用机制更晚且更浅，作者将其归因于更强的语法曲率和较少的代码预训练暴露。该案例说明同一类指针式依赖在不同模态中的形成速度可能不同，但这些归因在所给摘录中未通过独立控制实验完全分解。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper mechanistically explains how transformers acquire deep dependencies and why chain-of-thought facilitates structural reasoning.; rule check: matched taxonomy keywords; top rule score=7.0
- 全文指纹：`e335490519abf27bc7fcec808d351ec9f54978716a98d2057d35ed85d0ac8092`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
