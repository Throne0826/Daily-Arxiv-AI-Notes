---
title: "[论文解读] XCoT-VLA: Executable Chain-of-Thought for Vision-Language-Action Driving"
description: "[arXiv 2608.10976][自动驾驶] XCoT-VLA将自动驾驶中的自由文本推理压缩为少量可执行语义—动作令牌，使场景理解产生的驾驶意图能够以较低延迟直接约束连续轨迹生成。"
arxiv_id: "2608.10976"
announcement_date: "2026-08-12"
primary_category: "autonomous_driving"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-12T03:04:39.399942+00:00"
source_sha256: "395508cf1e623ad55e8a963a674680913c4ce18bf21c1065e0ebc27039db20bc"
tags:
  - "自动驾驶"
  - "VLM Reasoning"
  - "LLM Reasoning"
  - "视觉-语言-动作模型"
  - "可执行思维链"
  - "语义动作词元"
  - "连续轨迹生成"
  - "流匹配"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">自动驾驶 · arXiv 2608.10976</p>

# XCoT-VLA: Executable Chain-of-Thought for Vision-Language-Action Driving

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-12</span>
<span><strong>作者</strong> Foundation Model Team, XPeng Inc</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Foundation Model Team, XPeng Inc</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.10976v1) · [PDF 下载](https://arxiv.org/pdf/2608.10976v1) · **关键词** 自动驾驶, 视觉-语言-动作模型, 可执行思维链, 语义动作词元, 连续轨迹生成, 流匹配<br>


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

XCoT-VLA将自动驾驶中的自由文本推理压缩为少量可执行语义—动作令牌，使场景理解产生的驾驶意图能够以较低延迟直接约束连续轨迹生成。

**不用术语来说**：自动驾驶模型不仅要看懂道路，还要及时决定转向、减速或停车；但让模型先逐字写出一段完整理由，再据此规划轨迹，会产生与当前动作无关的内容并增加响应时间，而且这些文字与车辆应如何运动之间缺少明确联系，因此不适合作为实时控制的中间接口。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出可执行思维链（XCoT）：用通常仅含$2$至$6$个令牌的语义—动作序列表示影响驾驶决策的意图，例如准备左转、减速和红灯等待，以替代开放式自然语言解释。
- 提出面向推理—控制衔接的计算设计：利用日志轨迹中的动作证据和场景中的因果语义构造Reason–Action监督，并通过共享多模态注意力、分离的Reason FFN与Control FFN，将XCoT推理接入连续轨迹生成；同一令牌空间还可支持可选的XCPO策略优化。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

视觉-语言-动作模型（VLA）把摄像头等视觉观测、语言或导航指令以及车辆运动控制放入统一建模流程：模型先理解道路结构、交通规则和周围参与者，再将这些高层语义转化为可执行轨迹。本文关注的关键接口不是一般性的场景问答，而是“推理结果如何进入连续控制”：自动驾驶要求模型持续规划且满足严格实时预算，因此中间表示既要保留会改变驾驶行为的语义，又不能像自由形式的自然语言推理那样产生大量与当前决策无关的自回归词元。XCoT-VLA据此使用通常仅含$2$至$6$个词元的可执行思维链，作为多模态理解与连续轨迹生成之间的语义动作接口；这些词元表达转弯准备、减速或红灯停车等高层意图，而非直接充当转向、加速度或轨迹点等底层动作。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉-语言-动作模型（VLA）**

VLA模型联合处理视觉场景、语言语义和动作输出，使感知与控制能够在同一模型中衔接。在本文的驾驶场景中，动作输出是车辆的连续未来轨迹，而不是一段文本回答。

</div>
<div class="concept-item" markdown="1">

**思维链与自回归解码**

思维链（CoT）是在最终预测前生成的一系列中间推理内容；自回归解码意味着每个新词元都依赖此前已生成的词元。自由文本越长，串行解码延迟通常越高，而且其描述未必与车辆动作存在明确对应关系。

</div>
<div class="concept-item" markdown="1">

**流匹配轨迹生成**

流匹配是一类连续生成方法，学习把简单初始分布沿时间相关的向量场逐步变换为目标数据分布。本文用它生成连续驾驶轨迹，并让轨迹查询在生成过程中受到XCoT语义动作词元的条件约束。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

任务运行在需要连续、实时规划的自动驾驶环境中。输入是多模态驾驶上下文，包括视觉观测以及能够提供导航意图、交通规则、道路结构和周围交通参与者交互信息的场景上下文；训练阶段还可利用日志轨迹作为车辆实际行为的动作证据。模型先预测一个短XCoT序列，其中每个离散词元编码与控制直接相关的驾驶意图；该序列保留在模型上下文中，通过共享的多模态自注意力影响固定轨迹查询，随后生成连续未来轨迹。问题的核心假设是：轨迹规划并不需要完整自然语言解释，只需保留足以改变控制行为的决策关键信息；因此，中间推理表示应同时满足决策相关、紧凑和可执行三个条件。这里“可执行”并不表示XCoT词元本身就是底层控制量，而是表示它们能够直接条件化后续轨迹生成。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$\mathbf{o}$**

多模态驾驶上下文的概括性记号，包括视觉观测及导航、道路和交通交互等场景信息；原文节选未给出统一正式符号。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{z}_{\mathrm{XCoT}}$**

模型预测的短可执行思维链序列，用于表示决策关键的语义动作意图；原文节选未给出统一正式符号。

</div>
<div class="notation-item" markdown="1">

**$\mathbf{q}_{\mathrm{traj}}$**

用于读取XCoT条件信息并驱动连续轨迹生成的固定轨迹查询；原文节选未给出统一正式符号。

</div>
<div class="notation-item" markdown="1">

**$\hat{\boldsymbol{\tau}}$**

模型生成的连续未来驾驶轨迹；原文节选未给出统一正式符号。

</div>

</div>

**直接相关的工作**

- **RT-2与OpenVLA**: 这些机器人VLA方法把离散动作表示为可由语言模型骨干预测的词元。XCoT-VLA同样使用离散词元，但其XCoT词元不是最终底层动作，而是连接多模态推理与连续轨迹控制的中间语义动作表示。
- **DriveLM、LingoQA与Reason2Drive**: 这些工作以结构化问答、语言理解或链式推理组织驾驶语义，说明语言中间表示能够支持驾驶决策。XCoT-VLA进一步聚焦推理到动作的接口，将控制相关语义压缩成短词元序列，以减少自由文本推理的自回归开销并直接条件化轨迹生成。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

自动驾驶VLA模型必须连续地把摄像头等多模态场景信息、导航意图、交通规则和周围车辆交互转化为可执行轨迹，同时满足严格的实时规划预算。中间推理若过慢或包含大量无关信息，即使语义上合理，也可能延迟车辆控制并削弱其部署价值。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **不显式暴露中间推理的VLA控制**：模型从视觉、语言或导航上下文直接预测物理动作或轨迹，把语义理解和控制映射主要隐含在网络内部；这种方式避免生成长篇解释，但缺少一个清晰、可监督的决策级接口来表达当前驾驶意图。
- **基于自然语言CoT的驾驶VLM/VLA**：模型先以自回归方式逐词生成场景描述、因果判断或驾驶理由，再利用这些文本辅助最终决策。它能显式展示语义推理过程，但其表示目标主要是形成通顺解释，并不天然对应连续控制变量。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 自由文本CoT是开放式的，可能描述不影响当前决策的场景细节；其语言结构与转向、速度变化等可执行运动仅有隐式联系，因而轨迹生成器难以稳定提取真正影响动作的信号。
- 自然语言CoT需要逐令牌自回归解码，文本越长，推理延迟和计算开销越高；在持续运行且有严格时限的自动驾驶规划中，这种额外成本会直接压缩控制模块的实时预算。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有工作尚缺少一种位于高层场景语义与连续轨迹之间的中间表示：它既应保留导航、交通规则和交互关系中会改变驾驶行为的因果信息，又应具有固定而紧凑的动作语义，并能作为轨迹生成器可直接利用和优化的条件，而不是仅供人阅读的解释。

</div>
<div markdown="1"><span>核心问题</span>

自动驾驶VLA应当向轨迹生成器暴露何种形式的推理，才能在保持决策语义的同时减少自回归开销，并让该推理对连续运动生成产生直接、可训练的作用？

</div>
<div markdown="1"><span>作者直觉</span>

驾驶控制通常不需要复述完整场景，而只需要识别少数会改变轨迹的意图。将“准备左转”“减速”“红灯保持”等意图编码成短令牌序列，相当于先把复杂场景压缩成控制模块能理解的指令；这些令牌继续留在模型上下文中并与轨迹查询共享注意力，使轨迹预测可以直接读取决策依据。再按令牌功能分别使用Reason FFN和Control FFN，可让语义推理与连续控制各自学习合适的变换，同时保留二者的信息交互。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

XCoT-VLA把自动驾驶建模为部分可观测马尔可夫决策过程：在决策时刻$t$，模型接收多模态观测$o_t$，其中包括视觉场景、任务提示、自车状态$s_t$、历史轨迹和高层导航指令。方法先自回归生成长度不超过$M_{\max}=6$的可执行思维链$z_t$，再让固定的$24$个轨迹查询通过共享多模态自注意力读取观测与XCoT表示，并由流匹配解码器预测未来$H=24$步的纵向加速度和航向角变化$u_t$；确定性的时间积分算子$\mathcal{I}_{\mathrm{traj}}$最终将其转换为自车坐标系轨迹$\tau_t$。这里的“可执行”并不表示每个符号直接调用一条手写控制规则，而是表示这些符号携带面向动作的语义，并作为连续轨迹生成器的显式条件。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 离线提取动作证据

动作提取函数$f_{\mathrm{act}}$分析$-3\,\mathrm{s}$至$6\,\mathrm{s}$范围内的速度、加速度、车道相对位移和轨迹几何，将轨迹归纳为纵向证据$\mathbf{a}^{\mathrm{lon}}_t$与横向证据$\mathbf{a}^{\mathrm{lat}}_t$。这些证据描述已经发生的保持速度、减速停车、车道保持或横向移动等行为，但不单独推断行为原因。

<div class="method-step__io" markdown="1">

**输入**：日志样本$(o_t,\tau_t)$，其中$o_t$是当前多模态观测，$\tau_t$是仅在训练标签构造阶段可用的未来实车轨迹。<br>
**输出**：动作证据$\mathbf{a}_t=(\mathbf{a}^{\mathrm{lon}}_t,\mathbf{a}^{\mathrm{lat}}_t)$。

</div>

**直观理解**：日志轨迹先回答“车实际怎样开了”，避免仅凭图像猜测驾驶动作。它还不能回答“为什么这样开”，因为相似的减速可能分别由红灯、行人或前车造成。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 场景语义归因与Reason–Action配对

函数$f_{\mathrm{reason}}$从导航意图、道路结构、交通规则、周围交通参与者交互和安全约束等方面生成$K$个候选原因$\mathcal{R}_t$；随后$f_{\mathrm{ground}}$依据一致性分数$S_{\mathrm{cons}}$选择与场景和动作最相符的$r_t^*$。实践中多个视觉语言专家使用固定提示生成解释，规则模板、关键词和嵌入相似度只负责把自由文本映射为临时分类签名并形成共识，自由文本本身不会成为模型标签。

<div class="method-step__io" markdown="1">

**输入**：当前观测$o_t$与轨迹导出的动作证据$\mathbf{a}_t$。<br>
**输出**：经语义对齐的Reason–Action对$(r_t^*,\mathbf{a}_t)$。

</div>

**直观理解**：这一步把“看见什么”和“车怎样运动”交叉核对，从候选解释中选出最可信的原因。语言模型只在离线制标签时充当语义标注工具，因此在线规划不需要生成长篇解释。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 语义压缩为规范XCoT序列

基于固定可解释词表的压缩函数$g_{\mathrm{XCoT}}$生成规范序列$z_t^*=(z_{t,1}^*,\ldots,z_{t,M_t}^*)$，其中$2\leq M_t\leq6$，之后另行附加EOS。序列首先放置主要横向或导航动作，再依次加入可选的交互或纵向意图以及环境、规则或安全修饰符，以消除同一决策的等价排列。

<div class="method-step__io" markdown="1">

**输入**：Reason–Action对$(r_t^*,\mathbf{a}_t)$。<br>
**输出**：监督标签$z_t^*$，例如由`RIGHT_TURN_PREPARE`、`DECELERATE`和`HAZARD_YIELD`组成的动作语义序列。

</div>

**直观理解**：它把“准备右转、减速并礼让危险目标”压缩成少量标准符号，而不是几十个自然语言词元。固定词表和固定顺序使同类驾驶决策具有统一答案，降低自回归生成成本和标签歧义。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 分离推理与控制并生成连续运动

所有有效位置先通过共享多模态自注意力交换信息，随后确定性掩码把视觉、文本、自车状态、导航命令和XCoT等非轨迹位置送入Reason FFN，只把$24$个轨迹查询送入Control FFN；两类位置互斥且不使用可学习路由器。流匹配轨迹头据此生成$\hat u_t\in\mathbb{R}^{24\times2}$，每步包含纵向加速度$\hat a_{\mathrm{lon},h}$和航向角变化$\Delta\hat\psi_h$。

<div class="method-step__io" markdown="1">

**输入**：在线观测$o_t$、已生成或教师强制输入的XCoT序列，以及$24$个可学习轨迹查询$Q_{\mathrm{traj}}\in\mathbb{R}^{24\times d}$。<br>
**输出**：未来运动序列$\hat u_t$，经$\hat\tau_t=\mathcal{I}_{\mathrm{traj}}(\hat u_t;s_t)$积分后得到未来二维坐标轨迹。

</div>

**直观理解**：共享注意力相当于推理符号和轨迹查询共用一块信息交换区，因而控制查询能够读取XCoT；不同FFN则让语义推理和连续控制分别使用专门的参数。这样既建立推理到动作的连接，又避免把两种功能完全混在同一前馈分支中。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 条件流匹配损失

$$
\mathcal{L}_{\mathrm{FM}}=\mathbb{E}_{\alpha,x_{0},x_{1},c}\left\|v_{\theta}(x_{\alpha};\alpha,c)-(x_{1}-x_{0})\right\|_{2}^{2},\qquad x_{\alpha}=(1-\alpha)x_{0}+\alpha x_{1}
$$

**符号说明**

- $\mathcal{L}_{\mathrm{FM}}$：轨迹生成器的条件流匹配训练损失
- $x_1=\mathrm{vec}(u_t)\in\mathbb{R}^{48}$：将24步、每步2维的专家未来运动序列展平所得目标向量
- $x_0\sim\mathcal{N}(0,I_{48})$：作为生成起点的48维标准高斯噪声
- $\alpha\in[0,1]$：连接噪声与专家运动的流匹配时间
- $x_\alpha$：噪声$x_0$与目标$x_1$之间在流时间$\alpha$处的线性插值状态
- $c$：由XCoT词元表示和轨迹查询构成的条件上下文
- $v_\theta(x_\alpha;\alpha,c)$：参数为$\theta$的条件速度网络在插值状态上预测的运输方向
- $x_1-x_0$：线性概率路径对应的目标速度

<div class="equation-explanation" markdown="1">

**直观理解**：该损失要求网络在任意中间状态$x_\alpha$上预测从噪声走向真实专家动作的方向。模型学成后可从$x_0$出发积分速度场生成连续运动，而条件$c$使生成结果受场景和XCoT驾驶意图共同约束。<br>
**原文位置**：第3.3节，公式(10)

</div>

</div>

<div class="equation-block" markdown="1">

#### XCPO裁剪策略优化目标

$$
\mathcal{L}_{\mathrm{XCPO}}=-\mathbb{E}_{o}\left[\frac{1}{G}\sum_{i=1}^{G}\min\left(\rho_iA_i,\operatorname{clip}(\rho_i,1-\varepsilon,1+\varepsilon)A_i\right)\right]+\beta\,\mathbb{E}_{o}\left[D_{\mathrm{KL}}\left(\pi_{\theta_{\mathrm{reason}}}(\cdot\mid o)\,\|\,\pi_{\mathrm{ref}}(\cdot\mid o)\right)\right]
$$

**符号说明**

- $\mathcal{L}_{\mathrm{XCPO}}$：可选第二阶段用于优化XCoT推理策略的损失
- $o$：当前多模态驾驶观测
- $G$：旧策略针对同一观测采样的XCoT序列数量
- $\rho_i$：第$i$条完整XCoT序列在当前策略与旧策略下概率之比，计算范围包括EOS
- $A_i$：第$i$条轨迹总奖励在采样组内进行均值和标准差归一化后得到的相对优势
- $\varepsilon$：限制策略概率比变化幅度的裁剪阈值
- $\pi_{\theta_{\mathrm{reason}}}$：正在更新的自回归XCoT策略
- $\pi_{\mathrm{ref}}$：作为KL约束参考的Stage-I检查点
- $\beta$：KL散度正则项权重
- $D_{\mathrm{KL}}$：衡量当前策略偏离Stage-I参考策略程度的KL散度

<div class="equation-explanation" markdown="1">

**直观理解**：组内优势让同一场景下产生较好轨迹的XCoT序列获得更高概率，裁剪项防止一次更新过大，KL项则约束策略不要远离监督学习所得的可解释词元分布。奖励通过冻结执行器生成的轨迹计算，但优化时轨迹和奖励被视为固定样本，梯度只经过XCoT序列的自回归对数概率。<br>
**原文位置**：第3.4节，公式(15)；序列概率比与组内优势分别定义于公式(14)和公式(13)

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：Stage I的总目标为$\mathcal{L}_{\mathrm{SFT}}=\lambda_{\mathrm{XCoT}}\mathcal{L}_{\mathrm{XCoT}}+\lambda_{\mathrm{FM}}\mathcal{L}_{\mathrm{FM}}$。其中$\mathcal{L}_{\mathrm{XCoT}}$是对离线标签$z_t^*$及其EOS计算的自回归负对数似然，负责学习“观测到可执行意图”；$\mathcal{L}_{\mathrm{FM}}$负责学习“意图与场景到连续未来运动”，两者共同训练使XCoT不只是可读分类结果，而会实际进入轨迹条件上下文。论文设$\lambda_{\mathrm{XCoT}}=1$，并在验证集上调整$\lambda_{\mathrm{FM}}$；填充词元不计入XCoT损失。

Stage II的$\mathcal{L}_{\mathrm{XCPO}}$是可选扩展。每条采样轨迹的总奖励为$R_i=\sum_k w_kr_k(\tau_i)$，再用同组奖励均值$\mu_{\mathbf R}$与标准差$\sigma_{\mathbf R}$形成$A_i=(R_i-\mu_{\mathbf R})/(\sigma_{\mathbf R}+\epsilon)$；该阶段只更新Reason FFN和XCoT预测头。作者明确说明当前版本没有对XCPO进行定量评估，因此公式描述的是所提出的优化机制及预期用途，不能据此断言它已经带来实验提升。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Reason–Action监督构造器**

其完整映射为$(o_t,\tau_t)\xrightarrow{f_{\mathrm{act}}}\mathbf{a}_t\xrightarrow{f_{\mathrm{ground}}}(r_t^*,\mathbf{a}_t)\xrightarrow{g_{\mathrm{XCoT}}}z_t^*$。轨迹提供可核验的动作证据，场景提供因果语义，最终分类体系只分配已有的规范词元，不学习或创造新词元。

> 直观理解：单用语言标注容易得到听起来合理但与真实驾驶动作不一致的解释，单用轨迹又无法区分红灯停车和避让行人。该模块把两类信息绑定后再压缩，使监督同时保留“原因”和“动作”。

**2. 共享注意力与确定性双FFN路由**

每层先以共享自注意力更新全部位置，然后由$m^{\mathrm{Reason}}_{t,j}$与$m^{\mathrm{Control}}_j$进行互斥路由：所有有效非轨迹位置进入$\mathrm{FFN}_{\mathrm{Reason}}$，轨迹查询进入$\mathrm{FFN}_{\mathrm{Control}}$，满足$m^{\mathrm{Reason}}_{t,j}+m^{\mathrm{Control}}_j=1$及$m^{\mathrm{Reason}}_{t,j}m^{\mathrm{Control}}_j=0$。填充位置不进入任一分支，轨迹查询仍可在FFN路由前通过注意力读取XCoT和场景特征。

> 直观理解：注意力负责让推理和控制互相看见，两个FFN负责各自加工信息。路由完全由词元功能决定，因此不存在混合专家模型中路由器选错专家或额外学习不稳定的问题。

**3. 条件流匹配轨迹执行器**

专家运动$u_t$被展平为$x_1\in\mathbb{R}^{48}$，从高斯噪声$x_0$出发，在流时间$\alpha\in[0,1]$上学习条件速度场$v_\theta$；条件$c$来自XCoT表示和轨迹查询。推理时积分所学常微分方程得到$24$步运动量，再以当前自车状态$s_t$为初值进行物理时间积分，获得坐标轨迹。

> 直观理解：该执行器学习如何把随机噪声逐渐运输成符合场景和驾驶意图的连续动作。流时间上的生成积分与未来$24$步动作的时间积分是两件不同的事，论文明确指出二者都不属于XCoT策略采样。

**训练与推理**

训练前先离线处理日志：未来轨迹经$f_{\mathrm{act}}$产生动作证据，视觉语言专家和一致性选择器产生原因$r_t^*$，随后$g_{\mathrm{XCoT}}$生成固定词表中的规范标签。Stage I中，Reason分支在观测$o_t$上自回归预测相同序列；轨迹解码器则采用教师强制的$z_t^*$作为条件，联合优化XCoT交叉熵与流匹配损失。教师强制减少训练初期错误XCoT对连续控制学习的干扰，但也意味着训练时使用真值XCoT、测试时使用预测$\hat z_t$，两者存在条件分布差异。

若执行Stage II，旧策略对每个$o$采样$G$条离散XCoT序列$z_i$，冻结执行器$\mathcal F$把每条序列解码为轨迹$\tau_i$并计算奖励；策略通过组相对优势、概率比裁剪及相对Stage-I策略的KL约束更新。正式推理时，模型只接收当前可用的$o_t$：先生成$2$至$6$个XCoT词元直到EOS或$M_{\max}$，保持这些词元在上下文中，再由轨迹查询和流匹配ODE生成$\hat u_t$，最后用$s_t$积分为$\hat\tau_t$。日志未来轨迹只用于离线标签构造，推理阶段不可用；运动解码和轨迹积分均为确定性模型操作，只有XCPO中的XCoT词元抽样被称为策略采样。

**复现信息**

对复现和结果解释关键的设置包括：预测时域使用$H=24$个未来运动步，因此$Q_{\mathrm{traj}}$含$24$个查询，流匹配目标展平后为$48$维；每个动作步预测纵向加速度与航向角变化，而非直接回归二维坐标。XCoT正文标签长度为$2$至$6$，实现上$M_{\max}=6$，EOS单独附加，填充仅用于批处理。标签词表统一覆盖纵向控制、横向或导航动作、交通规则、交互、环境和安全意图；确定性排序要求主要横向或导航动作在前，以避免相同词元集合的排列歧义。

架构只含Reason FFN和Control FFN两个前馈分支，路由由位置功能决定，不存在学习式MoE路由器。Stage II冻结视觉前端、共享自注意力、Control FFN和流匹配轨迹头，时间积分本身无可训练参数；不过更新Reason FFN仍会改变非轨迹位置的表示，因此后续采样时轨迹查询通过共享注意力接收到的条件也会变化。论文未在所给方法章节明确报告视觉语言专家数量$K$、XCoT完整词表规模、流匹配ODE求解器、采样组大小$G$、奖励项$r_k$及权重$w_k$的具体取值，这些缺失会影响对离线标注与XCPO的完整复现。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 一般分布评测集：用于检验模型在常规驾驶数据分布上的纵向轨迹预测能力。原文摘要报告了该评测集上的纵向ADE，但所给实验章节片段未提供数据来源、规模、场景构成或训练/测试划分。
- 换道场景评测集：用于重点检验横向控制与换道终点预测。原文摘要报告了该场景集上的横向FDE，但所给片段未说明样本数量、换道类型、划分方式及是否与训练数据同分布。
- 大规模混合训练数据：实验设置称模型使用一个大规模混合数据集训练，但原文片段在“approximately”处截断，因此其准确规模、数据来源、组成比例及标注方式均无法核实。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**纵向ADE（Average Displacement Error）**

衡量预测轨迹与真实轨迹在纵向方向上的平均位移误差，通常对预测时域内各时间点的误差取平均。它主要反映加速、减速与跟车距离等纵向规划的整体准确性；所给片段未明确单位和具体计算公式。 （越低越好，因为较小的平均位移误差表示预测轨迹在整个时间范围内更接近真实纵向运动。）

</div>
<div class="metric-item" markdown="1">

**横向FDE（Final Displacement Error）**

衡量预测时域终点在横向方向上与真实终点之间的位移误差，适合检验换道后车辆是否到达正确的横向位置；它不直接反映中间轨迹是否平滑或安全。所给片段未明确单位和具体计算公式。 （越低越好，因为较小的终点误差意味着模型对换道最终横向位置的预测更准确。）

</div>
<div class="metric-item" markdown="1">

**自回归推理token数量**

记录模型在生成动作前需要解码的可执行XCoT token数量，用于近似衡量推理序列长度及其自回归解码开销。该指标不是轨迹质量指标，也不能单独代表端到端延迟。 （在轨迹质量相当的前提下通常越少越好，因为自回归生成必须逐token执行，较短序列通常意味着较低的推理开销。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 一般分布评测集上的纵向轨迹预测

<div class="result-value" markdown="1">

纵向ADE从$1.645$下降到$1.323$，绝对下降$0.322$；按起始值计算，相对降幅约为$19.6\%$。

</div>

作者报告XCoT-VLA在一般驾驶分布上的纵向平均轨迹误差更低，说明其预测的加减速或纵向位置整体上更接近记录轨迹。相对降幅是依据摘要数值计算的分析结果，不是原文直接表述。由于比较基线、误差单位、统计波动和显著性均未在所给材料中出现，该结果不能单独证明模型在所有驾驶环境中更安全，也不能证明改进完全来自XCoT设计。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

XCoT-VLA reduces longitudinal ADE from 1.645 to 1.323 on a general-distribution set and lateral FDE from 1.616 to 0.648 in lane-change scenarios.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 换道场景评测集上的横向终点预测

<div class="result-value" markdown="1">

横向FDE从$1.616$下降到$0.648$，绝对下降$0.968$；按起始值计算，相对降幅约为$59.9\%$。

</div>

作者报告的较大降幅表明，模型在换道结束时更准确地预测了车辆应处的横向位置。这一指标尤其对应换道动作是否到达目标车道，但它只测量终点偏差，不能说明换道过程中的中间轨迹一定平滑、无碰撞或符合交通规则。相对降幅为依据摘要数值计算的分析结果；缺少基线身份和置信区间也限制了因果解释。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

XCoT-VLA reduces longitudinal ADE from 1.645 to 1.323 on a general-distribution set and lateral FDE from 1.616 to 0.648 in lane-change scenarios.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 可执行推理序列长度与实时规划可行性

<div class="result-value" markdown="1">

模型使用$2$至$6$个可执行XCoT token表示驾驶推理；作者称这显著减少了自回归推理开销，并使系统保持在实时规划预算内。

</div>

少量离散token意味着动作生成前需要逐步解码的推理序列很短，这与降低自然语言长推理链的延迟目标一致。不过，“处于实时预算内”是作者结论；所给材料没有提供毫秒级延迟、硬件平台、吞吐量、预算阈值或与自然语言CoT的直接速度对照，因此不能据此量化实际部署收益。

<div class="result-source" markdown="1">

来源：摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

By representing driving-oriented reasoning with only 2-6 executable XCoT tokens, our method substantially reduces autoregressive reasoning overhead and remains within the real-time planning budget.

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

- 原文未明确报告。摘要中的“from 1.645 to 1.323”和“from 1.616 to 0.648”表明存在比较对象，但所给材料没有给出该对象的名称、架构、训练数据或是否仅移除了XCoT机制，因而不能将其可靠地归类为特定基线。

**实验想回答的问题**

- 与论文所比较的基线方法相比，XCoT-VLA是否能在一般分布与换道场景中降低轨迹预测误差？
- 将自然语言推理压缩为少量可执行XCoT token后，模型能否在保持实时规划可行性的同时，直接支持轨迹生成？

**实验实现**

模型在一个大规模混合数据集上训练，但所给实验章节片段没有完整呈现数据规模、训练轮数、优化器、硬件、输入配置、轨迹预测时域或评测重复次数。根据摘要，模型以固定轨迹查询生成轨迹，并仅生成$2$至$6$个可执行XCoT token；XCPO被描述为可选的策略优化扩展。由于缺少完整实验表格和协议，无法判断摘要结果是否采用XCPO、各方法是否共享相同训练数据，以及延迟是否包含视觉编码、XCoT解码和轨迹生成的全部耗时。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper develops a VLA driving model with compact executable reasoning tokens directly conditioning real-time trajectory generation.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`395508cf1e623ad55e8a963a674680913c4ce18bf21c1065e0ebc27039db20bc`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
