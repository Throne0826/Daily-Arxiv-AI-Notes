---
title: "[论文解读] LeapBot-WA: World-Anchor Action Models via Predictive Latent Alignments"
description: "[arXiv 2607.23969][机器人 / 具身智能] LeapBot-WA旨在以预测语义潜表示取代像素级未来画面生成，并通过分布适配与训练期动力学指导，使机器人策略兼具稳定学习、视觉鲁棒性和低开销部署能力。"
arxiv_id: "2607.23969"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.343900+00:00"
source_sha256: "9fb58ca5f36b3362ddf98975c9fa74861aa468b2723e763330ff718b7833b0ef"
tags:
  - "机器人 / 具身智能"
  - "具身智能"
  - "机器人操作"
  - "世界动作模型"
  - "预测潜变量"
  - "联合嵌入预测架构"
  - "语义对齐"
  - "扩散模型"
  - "流匹配"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2607.23969</p>

# LeapBot-WA: World-Anchor Action Models via Predictive Latent Alignments

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Liu, Pei, Zheng, Nan, Zhang, Lang, Peng, Daojie, Zhang, Yanan, Kong, Feilong, Feng, Mingyue, Liu, Jiachao, Wang, Yaonong, Chen, Qifeng, Ma, Jun</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> The Hong Kong University of Science and Technology (Guangzhou)；The Hong Kong University of Science and Technology；Southeast University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.23969) · [PDF 下载](https://arxiv.org/pdf/2607.23969) · **关键词** 具身智能, 机器人操作, 世界动作模型, 预测潜变量, 联合嵌入预测架构, 语义对齐, 扩散模型, 流匹配<br>
**代码**: [https://github.com/LeapWM/leapbot-wa](https://github.com/LeapWM/leapbot-wa)

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

LeapBot-WA旨在以预测语义潜表示取代像素级未来画面生成，并通过分布适配与训练期动力学指导，使机器人策略兼具稳定学习、视觉鲁棒性和低开销部署能力。

**不用术语来说**：机器人执行操作时，真正需要判断的是动作会怎样改变物体和环境，而不是精确画出未来画面中的纹理、阴影与背景。现有世界动作模型往往把大量能力用于重建这些与任务无关的视觉细节，因此在背景、光照或干扰物变化后容易失效；但若直接改用抽象视觉特征，又会遇到特征分布不适合扩散模型、训练不稳定以及部署时仍依赖笨重世界模型等问题。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出以微调后的联合嵌入预测架构（JEPA）作为“预测锚点”的潜空间世界动作建模范式，不再以重建未来像素为核心，而是让策略学习与动作相关的抽象状态变化。
- 提出各向同性语义自编码器（ISAE）与非对称混合令牌（MoT）架构：前者将结构化、非高斯的预测特征变换为适合扩散学习的潜分布；后者让 Anchor DiT 在训练时向 Action DiT 提供动力学指导，并在推理时移除该重型分支。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于具身智能中的机器人操作研究。其核心问题是：智能体不仅要根据当前视觉观测直接生成动作，还应学习“执行某个动作后环境将如何变化”的世界模型。世界动作模型（WAM）把环境动态预测与动作生成结合起来，通常从视频和机器人轨迹中学习物理先验；但主流方案以未来视频帧或可重建视频的潜变量作为预测目标，因而同时建模纹理、光照、阴影和背景等与操作无关的细节。本文关注一种替代设定：不再把精确视觉合成视为世界建模的必要条件，而是在预训练表征空间中预测与物体状态变化和动作后果有关的高层语义动态，并利用这些动态辅助机器人策略训练。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**世界动作模型（World Action Model, WAM）**

一种同时学习环境如何随动作演化以及机器人应执行何种动作的模型。与只对当前观测作出反应的策略相比，它显式引入了对未来状态或未来表征的预测。

</div>
<div class="concept-item" markdown="1">

**联合嵌入预测架构（Joint-Embedding Predictive Architecture, JEPA）**

JEPA不要求逐像素生成未来图像，而是在特征空间中根据当前信息预测目标观测的语义表示。这样可弱化纹理和背景等表面细节，使表征更侧重物体关系、状态转移与潜在物理规律。

</div>
<div class="concept-item" markdown="1">

**扩散模型与各向同性先验**

扩散模型通常从结构较均匀的高斯噪声出发，经逐步去噪或流匹配生成目标变量，因此希望其建模空间接近各方向统计性质相似的各向同性分布。直接使用高度结构化、非高斯的预测特征可能使生成轨迹偏离有效数据流形，即产生文中所称的“离流形漂移”。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定机器人当前的视觉观测、任务意图以及训练轨迹中的动作监督，目标是学习一个能够输出机器人动作的策略，同时借助未来语义动态预测获得物理先验。训练环境允许模型访问由经过适配的JEPA“预测锚点”提取的视觉语义特征，并学习这些特征随交互发生的变化；这些结构化特征还需被变换到适合扩散或流匹配建模的潜空间。论文进一步假设部署时应避免依赖计算量较大的世界动态生成分支：动态分支只在训练阶段作为具有额外信息的专家指导动作分支，推理时被移除，由动作分支直接产生控制输出。因而该问题同时要求动作生成有效、语义动态可预测、潜变量分布适配扩散训练，并对未见环境及视觉干扰具有鲁棒性。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **Hafner et al. (2023), Mastering Diverse Domains through World Models**: 代表利用预测环境动态支持规划与控制的世界模型研究，为本文将“预判环境演化”作为机器人决策基础提供总体背景；本文进一步面向机器人操作，把世界建模与动作生成整合为WAM。
- **Hu et al. (2024), Video Prediction Policy: A Generalist Robot Policy with Predictive Visual Representations**: 与本文直接相关，因为它同样将预测性视觉表征用于机器人策略。LeapBot-WA进一步强调在JEPA语义空间预测动态、将非高斯特征整形成适合扩散建模的空间，并在部署时移除动态预测分支。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

通用机器人操作需要根据视觉观测和任务意图预测动作造成的环境变化，同时还要在背景、纹理、光照及干扰物发生变化时保持可靠。若策略主要记住训练环境的外观，而没有掌握物体与动作之间的状态转移规律，就难以迁移到未见环境；若部署还必须运行完整的生成式世界模型，则计算成本也会限制实际使用。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **像素级生成式世界动作模型**：通过显式合成未来视频帧，或学习以视频重建为目标的潜编码来表示环境动力学，再将这种未来预测与动作生成结合。其训练信号完整，但把世界建模在很大程度上处理成视觉渲染问题。
- **压缩潜空间世界动作模型**：先把视觉观测压缩为潜代码，再在潜空间中预测未来状态或联合生成动作，以减少直接生成高维像素的成本；部分方法还将现成的预测表征接入基于扩散或流匹配的生成模型。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 像素或视频重建目标要求模型同时表示纹理、阴影、光照和背景等高频细节，使有限的表示容量被任务无关信息占用，并将物理动力学与特定视觉外观纠缠；作者据此认为，这会造成表示浪费，并使策略对视觉干扰和新环境变化高度敏感。
- 仅把像素压缩成潜代码并不能保证所得空间具有动作相关的语义；而现成预测特征通常高度结构化且呈非高斯分布，与扩散模型偏好的各向同性先验不匹配，可能导致去噪轨迹偏离有效特征流形。此外，既有架构常把世界建模与策略执行紧密耦合，使部署仍依赖重型生成分支。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未同时解决三个相互关联的问题：选择能够突出物理状态转移而抑制外观细节的世界模型表征空间；把该结构化语义空间可靠地适配到扩散式动作学习；以及让世界模型只在训练阶段传递动力学知识，而不成为推理阶段的必要计算路径。换言之，缺少一种兼顾语义抽象、生成分布稳定性和部署效率的统一潜空间方案。

</div>
<div markdown="1"><span>核心问题</span>

能否以预测基础模型提供的抽象潜表示作为机器人世界动作模型的语义锚点，并通过专门的分布整形和非对称训练架构，把潜空间动力学蒸馏进动作生成器，从而在不生成未来像素、也不增加推理期世界模型开销的条件下获得稳健的操作策略？

</div>
<div markdown="1"><span>作者直觉</span>

物体是否移动、接触关系如何变化以及动作会产生什么后果，比墙面纹理或阴影形状更接近控制所需的信息，因此先在预测表征空间中学习“变化规律”可以减少对外观捷径的依赖。ISAE相当于把形状复杂的语义特征重新整理成扩散模型容易采样和去噪的坐标空间；非对称 MoT 则类似训练时由掌握未来状态变化的专家指导动作分支，部署时学生已吸收这类规律，因此可以移除专家分支。该解释是对作者设计动机的分析性概括，实际有效性仍需结合完整实验与消融结果核验。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

LeapBot-WA把机器人策略建模为从多视角视觉观测、语言指令和本体状态到动作序列的条件生成过程，但不要求模型生成未来图像。给定观测$\mathbf{o}$，经过机器人数据适配的V-JEPA 2.1预测编码器$\Phi_{\mathrm{JEPA}}$提取高层语义特征；ISAE再将这些高维、非高斯特征压缩成96维近似各向同性高斯潜变量$\mathbf{z}$。语言指令$l$和本体状态$s$被编码为共享上下文$\mathbf{c}$。训练时，Anchor DiT对未来语义潜变量去噪，Action DiT对动作块去噪，并通过非对称注意力读取Anchor分支所表达的未来动态；Anchor分支不能反向读取动作，因此其预测必须主要依靠当前场景、任务意图和机器人状态，而不能把真实动作当作捷径。

整体训练分为三个阶段：先用LoRA把互联网视频预训练的V-JEPA适配到机器人视频，再单独训练ISAE完成语义空间与扩散空间的分布对齐，最后冻结前两部分并联合训练语义扩散和动作扩散分支。部署时不再迭代运行较重的Anchor DiT，而是从当前观测计算一次静态语义缓存，Action DiT在该缓存、语言和状态条件下从高斯噪声生成动作块；控制器仅执行前$R$个动作便重新观测和规划。直观地说，训练阶段让一个“预测世界将怎样变化的老师”参与动作学习，推理阶段移除老师的反复推演，只保留当前场景的语义笔记供轻量动作分支查询。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 预测锚点的机器人领域适配

冻结V-JEPA主体参数，只优化LoRA残差和轻量掩码预测器，以时空掩码预测目标学习机器人操作中的物体、几何和动态规律；多相机训练采用固定的第三人称与腕部视角比例。该阶段仍是特征预测，不进行像素级未来帧重建。

<div class="method-step__io" markdown="1">

**输入**：来自五种数据源的机器人视频，多相机数据包含第三人称视角与腕部视角；初始模型为V-JEPA 2.1的ViT-G/16检查点。<br>
**输出**：适应机器人视觉和物理分布、同时尽量保留通用视频先验的预测编码器$\Phi_{\mathrm{JEPA}}$。

</div>

**直观理解**：这一步相当于让原本看过大量网络视频的视觉模型学习机器人相机的视角和操作方式，同时只做小范围参数调整，以免破坏已有的通用物理常识。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### ISAE生成式潜空间对齐

共享权重的ISAE编码器预测高斯后验的均值和方差，并采样潜变量$\mathbf{z}^{(v)}$；解码器重建原始JEPA特征。训练同时约束重建误差、余弦方向一致性、KL散度和随机一维投影上的各向同性，使1664维结构化特征压缩为96维、适合流匹配的潜空间。

<div class="method-step__io" markdown="1">

**输入**：冻结预测锚点输出的多视角JEPA语义标记$\mathbf{F}^{(v)}$，其中$v$表示相机视角。<br>
**输出**：保留动作相关语义且近似各向同性高斯分布的紧凑潜变量$\mathbf{z}$，以及训练后冻结的ISAE。

</div>

**直观理解**：原始JEPA特征像形状复杂且方向偏置明显的数据云，扩散模型很难稳定地在其中从噪声移动到有效样本；ISAE把它整理成更接近圆对称高斯球的空间，同时尽量不丢失物体关系和动态信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 上下文与多视角条件构造

模型计算$\mathbf{z}=\mathrm{ISAE}(\Phi_{\mathrm{JEPA}}(\mathbf{o}))$和$\mathbf{c}=\Psi_{\mathrm{enc}}(l,s)$；对每个视角的带噪潜标记做归一化和线性投影，再加入可学习视角残差$\mathbf{e}^{(v)}_{\mathrm{view}}$及独立的时空位置编码。这样语义内容、相机身份、位置和扩散条件分别进入模型。

<div class="method-step__io" markdown="1">

**输入**：当前多视角观测$\mathbf{o}$、语言指令$l$、本体状态$s$以及扩散时刻$t$。<br>
**输出**：带有明确视角身份的语义标记和供两个DiT分支交叉注意的共享上下文$\mathbf{c}$。

</div>

**直观理解**：共享ISAE让不同相机采用同一种特征语言，但也可能使模型分不清标记来自哪个镜头；视角残差相当于给每个标记附上“相机编号”，便于跨视角判断同一物体的几何对应。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 非对称世界—动作联合去噪

Anchor DiT预测语义潜变量的去噪速度或未来语义，Action DiT预测动作的去噪速度；非对称掩码禁止Anchor标记关注动作标记，却允许Action标记关注Anchor标记。两个分支还分别通过交叉注意力读取语言和本体状态，联合损失同时监督动作生成与语义动态。

<div class="method-step__io" markdown="1">

**输入**：未来语义潜序列$\mathbf{z}$、真实动作块$\mathbf{a}_{t:t+H-1}$、共享上下文$\mathbf{c}$和同一随机扩散时刻加入的独立高斯噪声。<br>
**输出**：能够依据任务意图生成动作块的Action DiT，以及仅在训练阶段提供未来动态指导的Anchor DiT。

</div>

**直观理解**：信息只能从“世界预测”流向“动作决策”，不能从标准答案动作倒流到世界预测；因此世界分支被迫学习任务相关的物理后果，动作分支再把这些后果反推为控制命令。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### ISAE复合训练目标

$$
\mathcal{L}_{\mathrm{ISAE}}=\underbrace{\|\hat{\mathbf{F}}-\mathbf{F}\|_{2}^{2}+\lambda_{\mathrm{cos}}\,\mathbb{E}\!\left[1-\cos(\hat{\mathbf{F}},\mathbf{F})\right]}_{\mathcal{L}_{\mathrm{rec}}}+\beta\underbrace{D_{\mathrm{KL}}\!\left(q_{\phi}(\mathbf{z}\mid\mathbf{F})\,\|\,\mathcal{N}(\mathbf{0},\mathbf{I})\right)}_{\mathcal{L}_{\mathrm{KL}}}+\lambda_{\mathrm{iso}}\underbrace{\mathcal{R}_{\mathrm{SIGReg}}(\mathbf{z})}_{\mathcal{L}_{\mathrm{iso}}}
$$

**符号说明**

- $\mathbf{F}$：冻结JEPA输出的原始语义特征。
- $\hat{\mathbf{F}}$：ISAE解码器从潜变量重建的语义特征。
- $\mathbf{z}$：ISAE编码得到的紧凑语义潜变量。
- $q_{\phi}(\mathbf{z}\mid\mathbf{F})$：参数为$\phi$的编码器给出的条件高斯后验。
- $\mathcal{N}(\mathbf{0},\mathbf{I})$：零均值、单位协方差的标准各向同性高斯先验。
- $\mathcal{R}_{\mathrm{SIGReg}}$：在随机一维投影上惩罚潜分布偏离各向同性高斯的正则项。
- $\lambda_{\mathrm{cos}},\beta,\lambda_{\mathrm{iso}}$：分别控制方向重建、KL正则和各向同性正则强度的权重。

<div class="equation-explanation" markdown="1">

**直观理解**：第一部分要求压缩后仍能恢复JEPA特征的数值和方向，避免丢掉动作相关语义；第二、三部分共同把潜变量约束到适合高斯噪声扩散的规则空间。KL主要约束后验接近标准高斯，而SIGReg显式检查不同投影方向，补充防止维度坍缩和方差方向不均的问题。<br>
**原文位置**：Methodology，Diffusion-Friendly Semantic Autoencoding，式(4)至式(7)，合并表达以展示完整目标。

</div>

</div>

<div class="equation-block" markdown="1">

#### 非对称注意力与联合训练目标

$$
\mathrm{Attn}_{\mathrm{asym}}(\mathbf{H}^{(\ell)})=\mathrm{Softmax}\!\left(\frac{\mathbf{Q}\mathbf{K}^{\top}}{\sqrt{d}}+\mathbf{M}\right)\mathbf{V},\qquad \mathcal{L}_{\mathrm{train}}=\lambda_{a}\mathcal{L}_{\mathrm{action}}+\lambda_{s}\mathcal{L}_{\mathrm{semantic}}+\lambda_{f}\,\mathrm{SmoothL1}\!\left(\mathrm{LN}(\hat{\mathbf{z}}_{\mathrm{future}}),\mathrm{LN}(\mathbf{z}_{\mathrm{future}})\right)
$$

**符号说明**

- $\mathbf{H}^{(\ell)}=[\mathbf{H}_{s}^{(\ell)};\mathbf{H}_{a}^{(\ell)}]$：第$\ell$层中语义标记与动作标记的拼接序列。
- $\mathbf{Q},\mathbf{K},\mathbf{V}$：由拼接标记投影得到的查询、键和值矩阵。
- $\mathbf{M}$：非对称注意力掩码；屏蔽Anchor对动作标记的读取，但允许Action读取语义标记。
- $d$：注意力键或查询的通道维数，平方根用于缩放点积。
- $\mathcal{L}_{\mathrm{action}}$：Action DiT的动作流匹配速度预测损失。
- $\mathcal{L}_{\mathrm{semantic}}$：Anchor DiT的语义流匹配速度预测损失。
- $\hat{\mathbf{z}}_{\mathrm{future}},\mathbf{z}_{\mathrm{future}}$：预测的未来语义潜变量与由未来观测提取的目标潜变量。
- $\mathrm{LN}$：层归一化，用于在SmoothL1比较前规范化潜特征。
- $\lambda_a,\lambda_s,\lambda_f$：动作、语义和可选未来语义监督的损失权重。

<div class="equation-explanation" markdown="1">

**直观理解**：掩码决定信息流向：世界分支不能查看真实动作，动作分支却能读取世界分支的前瞻语义，因此动态知识可被蒸馏到策略而不形成动作泄漏。损失同时要求模型学会生成动作、还原语义去噪速度，并可选择直接贴近真实未来语义；后者用于防止Anchor分支只满足去噪目标却失去明确的前瞻物理含义。<br>
**原文位置**：Methodology，Asymmetric Latent Dynamics Distillation，式(10)至式(13)，其中核心注意力为式(11)、联合目标为式(12)、未来监督为式(13)。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：优化过程按模块解耦。第一阶段使用V-JEPA标准时空掩码预测目标训练LoRA和轻量预测器；第二阶段冻结预测锚点，以$\mathcal{L}_{\mathrm{ISAE}}$在特征层同时优化语义保真和潜分布几何；第三阶段再冻结V-JEPA与ISAE，将真实动作和未来语义潜变量在同一随机扩散时刻独立加噪，联合训练Anchor DiT与Action DiT。动作损失和语义损失均属于流匹配速度预测，即模型学习从带噪状态指向干净数据的速度场；可选的未来SmoothL1项把预测语义与未来观测对应的ISAE潜变量对齐。

原文不同章节对第三阶段目标的记号和权重存在需要源文核查的不一致：正文式(12)写为$\lambda_a\mathcal{L}_{\mathrm{action}}+\lambda_s\mathcal{L}_{\mathrm{semantic}}+\lambda_f\mathcal{L}_{\mathrm{future}}$，并称未来项可选；附录C式(44)简写为$\mathcal{L}_{\mathrm{action}}+\lambda_{\mathrm{jepa}}\mathcal{L}_{\mathrm{jepa}}$且给出$\lambda_{\mathrm{jepa}}=0.1$；附录D式(46)则写成$\lambda_{\mathrm{act}}\mathcal{L}_{\mathrm{act}}+\lambda_{\mathrm{jepa}}\mathcal{L}_{\mathrm{jepa}}$，并报告$\lambda_{\mathrm{act}}=0.1$、$\lambda_{\mathrm{jepa}}=1.0$。这些表述可能对应不同归一化或目标合并方式，但所给章节没有明确解释，不能据此认定唯一的最终权重配置。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Predictive Anchor**

以V-JEPA 2.1为初始化，通过LoRA和时空掩码预测适配机器人轨迹。它从多视角图像中提取表达对象关系、场景状态和物理变化的高层标记，避免以未来像素重建为世界建模目标。

> 直观理解：像素生成必须同时还原照明、纹理和背景等未必影响动作的细节；预测锚点把建模能力集中到与操作后果相关的语义变化，并利用大规模视频预训练获得的通用动态先验。

**2. Isotropic Semantic Autoencoder（ISAE）**

ISAE是带高斯后验的语义自编码器，其重建项同时比较特征的欧氏距离与余弦方向；KL项把单样本后验推向标准高斯，SIGReg进一步通过随机一维投影约束聚合潜分布的各向同性。所有相机共享编码器，并且训练和重建均发生在特征空间，不解码图像像素。

> 直观理解：仅把JEPA特征直接送入扩散模型会产生分布失配，去噪轨迹可能离开有效语义流形；KL和SIGReg共同把潜空间整理得更均匀，使从高斯噪声出发的生成过程更稳定。

**3. Asymmetric Mixture-of-Transformers（MoT）**

MoT包含Anchor DiT与Action DiT。训练时两种标记在Transformer层中进行带掩码的联合注意力：Anchor侧与动作侧隔离，Action侧可读取Anchor侧；推理时移除Anchor的迭代语义去噪，仅保留由当前观测得到的语义缓存作为Action DiT的条件。

> 直观理解：这种不对称结构将“预测任务相关未来”和“选择具体电机动作”分开：前者提供较纯粹的动态知识，后者负责控制；昂贵的教师分支只在训练中使用，因此部署时不会承担完整世界预测的迭代成本。

**训练与推理**

训练采用渐进三阶段流程。阶段I从V-JEPA 2.1 ViT-G/16开始，冻结基础参数，以五源机器人视频训练LoRA残差和掩码预测器；多相机样本维持第三人称与腕部视角的$7:3$比例。阶段II冻结适配后的锚点，在最长三视角、2秒时间窗上训练共享ISAE，把维度$d_{\mathrm{jepa}}=1664$的特征映射到$d_z=96$的潜变量。阶段III冻结锚点和ISAE，从未来视频提取目标语义潜变量，并与动作序列分别加入高斯噪声；Anchor DiT预测语义动态，Action DiT读取其标记并预测动作。跨机器人数据具有7自由度单臂和14自由度双臂等不同动作空间，因此模型保留按数据源路由的独立动作投影头，并使用单一来源的小批次避免同批动作维度冲突。

推理时，当前观测先经过冻结的V-JEPA和ISAE得到确定性的语义缓存，训练专用的未来语义去噪路径被旁路。Action DiT从纯高斯动作噪声开始，在语义缓存、冻结T5产生的任务语言嵌入和当前本体状态条件下迭代生成动作块$\hat{\mathbf{a}}_{t:t+H-1}=\pi_\theta(o_t,s_t,l)$。滚动时域控制每次只执行前$R$个动作便重新观测，因此最终策略仍是闭环的；所谓“零额外开销”应理解为相对于同一动作策略不再运行训练期Anchor语义去噪分支，而不是完全取消V-JEPA、ISAE或语义条件计算。

**复现信息**

预测锚点初始化自V-JEPA 2.1 ViT-G/16，并以LoRA适配机器人轨迹；ISAE将1664维JEPA特征压缩到96维潜空间，且整个对齐阶段不重建像素。Asymmetric MoT中的Anchor DiT和Action DiT各有30个Transformer块，隐藏维度为1664，采用24个注意力头；两支结构规模对称，但访问权限和部署角色不对称。语言条件由冻结T5编码器预计算，本体状态与语言共同形成上下文。

复现时最关键的工程约束是按阶段冻结组件、为不同动作维度使用独立投影头、按数据源构造同质批次，以及在多视角语义标记进入Anchor DiT前加入视角残差。训练采用bfloat16混合精度。所给章节未明确列出扩散采样步数、动作块长度$H$、实际执行长度$R$、优化器与学习率，以及ISAE各损失权重；这些参数不能从当前摘录推断，需对照完整附录或代码核查。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- RoboTwin 2.0：包含50个双臂操作任务；多任务策略使用由干净场景和随机化场景组成的27.5K条示范训练，并分别在Clean与Randomized视觉环境中测试。其作用是同时检验双臂协调、总体任务成功率以及对环境外观变化的稳健性。附录称每个任务、每种环境评估100次，但正文Table 1与附录Table 8的汇总值存在不一致。
- LIBERO：包含40个操作任务，覆盖Spatial、Object、Goal与LIBERO-10等任务组；模型使用专家轨迹训练，结果汇总自2,000个评估回合。该基准用于比较整体操作能力，并在消融实验中区分语义理解、物体操作、目标条件和长时序执行能力。
- LIBERO-plus与真实UR5部署：LIBERO-plus对环境施加模糊、雾、地面纹理和光照等系统性视觉扰动，用于零样本稳健性测试；真实部署使用UR5机械臂完成水果、容器等物体的拾取放置，并采用非受控光照，用于观察从仿真或训练分布向真实环境迁移的可行性。所给节选未报告这两部分的定量成功率。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**任务成功率**

一个评估回合是否完成指定操作的比例；RoboTwin按Clean、Randomized及其平均值报告，LIBERO按不同任务组和总体平均值报告。 （越高越好，因为它直接表示策略可靠完成任务的频率。）

</div>
<div class="metric-item" markdown="1">

**Clean与Randomized成功率差异**

比较标准视觉环境和强随机化视觉环境下的成功率，用来观察模型受到纹理、光照等外观变化影响的程度。 （在Clean性能相近时，下降越小通常表示视觉稳健性越强；但若Randomized反而更高，不能简单解释为负下降，还需考虑有限试验造成的波动。）

</div>
<div class="metric-item" markdown="1">

**分任务组成功率**

LIBERO消融分别报告Spatial、Object、Goal和LIBERO-10成绩，用于识别组件对空间推理、物体操作、目标条件和长时序任务的影响。 （越高越好；其中LIBERO-10对长时序或多阶段行为更敏感，因此更能检验未来预测是否有助于持续规划。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### RoboTwin 2.0总体比较（Table 1）

<div class="result-value" markdown="1">

LeapBot-WA在Clean、Randomized和平均成功率上分别达到91.04、92.48和91.76，且不使用具身预训练。它明显超过同为预测式模型的JEPA-VLA平均45.60，也超过多种预训练VLA；但平均值略低于Fast-WAM的91.85、LingBot-VA的92.24以及最强VLA Qwen-RobotManip的93.85，因此更准确的结论是“具有竞争力”，而不是该表上的绝对最佳。

</div>

这一结果支持潜变量世界锚点能够在较少预训练依赖下形成有效控制表征，并且Randomized成绩没有低于Clean成绩，显示出较强视觉稳健性。不过，不同方法的预训练数据、模型规模和训练预算未在节选中统一，因而该比较不能单独证明架构本身具有更高的数据效率或计算效率。

<div class="result-source" markdown="1">

来源：Table 1, Quantitative results on the RoboTwin 2.0 benchmark

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

LeapBot-WA | ✗ | 91.04 | 92.48 | 91.76

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### RoboTwin 50任务附录汇总（Table 8）

<div class="result-value" markdown="1">

Table 8的Average行报告LeapBot-WA为Clean 91.04、Rand. 92.48；相比$\pi_{0.5}$的82.74和76.76，分别高8.30和15.72个百分点。LeapBot-WA的Rand.成绩也高于Fast-WAM的90.52、LingBot-VA的90.92和Motus的87.02。

</div>

逐任务评估的汇总表表明，LeapBot-WA相对于通用预训练策略的优势在强视觉随机化环境中更明显，并在附录所列对照中取得最高Rand.平均值。但正文紧随其后的文字却声称Clean 92.64、Randomized 89.80，与表格及Table 1冲突，因此这里以可核对的表格行作主要依据，结论仍需作者原始结果确认。

<div class="result-source" markdown="1">

来源：Appendix E, Table 8

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Average | 82.74 | 76.76 | 91.98 | 90.52 | 91.50 | 90.92 | 88.66 | 87.02 | 91.04 | 92.48

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### LIBERO预测式WAM比较与LIBERO-plus零样本视觉扰动测试

<div class="result-value" markdown="1">

作者宣称LeapBot-WA在LIBERO上取得预测式WAM类别中的最佳表现，并在LIBERO-plus的模糊、雾、复杂纹理和光照变化下保持成功执行；但所给节选省略了Table 2的具体数值，也未提供LIBERO-plus定量成功率。

</div>

该结果的实验意图是把“常规操作能力”和“视觉分布变化下的稳健性”分开检验。现有材料只能支持作者的类别内排名陈述和定性案例，不能计算相对提升、确认统计可靠性，也不能证明潜变量不变性是稳健性的唯一原因。

<div class="result-source" markdown="1">

来源：Table 2 caption, Success rates on the LIBERO suites

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

LeapBot-WA achieves the best performance among all predictive WAMs and shows highly competitive results compared to more computationally expensive generative models.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- RoboTwin结果存在明显内部矛盾：Table 1和Table 8均给出LeapBot-WA为Clean 91.04、Randomized 92.48，但附录正文声称92.64和89.80，并进一步声称存在2.84%的下降；这些数字无法由所示表格复现，必须回查原始论文版本或代码结果。
- 节选未提供LIBERO Table 2的完整数值、LIBERO-plus与真实UR5实验的定量成功率，也未报告方差、置信区间、随机种子或显著性检验；因此预测式类别排名、真实迁移可靠性以及小幅消融增益的稳定性仍不能被独立判断。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- $\pi_{0.5}$：带具身预训练的通用策略，用于判断LeapBot-WA在没有大规模机器人轨迹预训练时，能否超过通用预训练策略。
- Fast-WAM：不使用具身预训练的强世界动作模型，在RoboTwin上与LeapBot-WA的训练资源条件更接近，因此是判断新世界锚点设计是否真正改善性能的关键对照。
- LingBot-VA：使用具身预训练的强WAM，在RoboTwin总体成绩接近领先水平，用于比较LeapBot-WA与依赖预训练的世界动作模型之间的性能和数据效率。
- JEPA-VLA：同属预测式、潜变量对齐路线且不使用具身预训练；它是检验LeapBot-WA的ISAE、未来预测及双分支训练设计是否超越简单JEPA特征接入方式的直接对照。

**实验想回答的问题**

- 在不使用大规模机器人轨迹预训练的条件下，LeapBot-WA能否在双臂与单臂操作基准上达到或接近强生成式世界动作模型及预训练视觉-语言-动作模型的任务成功率？
- 基于JEPA的语义上下文与未来潜变量预测分别贡献了什么，尤其能否提升视觉扰动下的稳健性和长时序任务的执行能力？

**实验实现**

RoboTwin使用27.5K条干净与随机化示范训练一个覆盖50项任务的多任务策略，并独立测试Clean和Randomized环境；附录Table 8称每个任务在每种环境下进行100次试验。LIBERO遵循标准专家轨迹训练协议，并在2,000个评估回合上汇总结果；LIBERO-plus不进行针对扰动的再训练，而是测试系统性环境变化下的零样本迁移。消融依次移除语义上下文、仅加入冻结V-JEPA语义特征，以及进一步以权重$\lambda=0.2$启用未来预测的流匹配损失。节选没有给出随机种子、置信区间、方差或显著性检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 加入JEPA语义上下文，但不启用未来预测（$\lambda=0$） | 平均成功率由47.7提升至90.7，增加43.0个百分点；Spatial由34.0升至94.8，Object由84.8升至99.8，Goal由70.2升至89.8，LIBERO-10由1.8升至78.4。 | 该对照隔离了冻结V-JEPA语义流的作用：原始视觉和本体状态不足以稳定处理空间关系及多阶段任务，而高层语义特征带来主要性能增益。它支持语义上下文的重要性，但由于一次加入了完整语义流，不能进一步区分特征预训练、融合方式和模型容量各自的贡献。 | Appendix E, Table 9<br><span class="experiment-evidence">✓ \| 0 \| 94.8 \| 99.8 \| 89.8 \| 78.4 \| 90.7</span> |
| 在语义上下文基础上启用未来预测（$\lambda=0.2$） | 总体平均成功率由90.7升至92.0，增加1.3个百分点；最明显的提升出现在LIBERO-10，由78.4升至85.0，即增加6.6个百分点，而Spatial、Object和Goal分别轻微下降0.2、0.8和0.6个百分点。 | 该对照较直接地检验未来潜状态预测是否超越静态语义输入。结果表明预测目标主要有利于长时序一致性，而不是对所有任务组均匀增益；因此作者关于“预测动力学帮助长期行为”的解释具有针对性，但不能把平均提升解读为所有类别都改善。 | Appendix E, Table 9<br><span class="experiment-evidence">✓ \| λ=0.2 \| 94.6 \| 99.0 \| 89.2 \| 85.0 \| 92.0</span> |

**定性案例**

- Figure 9展示LIBERO-plus中的相机模糊、雾、复杂地面纹理和光照变化。作者观察到策略仍能完成多类操作，并将其归因于V-JEPA潜表示忽略低层视觉噪声、保留物体几何与语义结构。该可视化适合说明模型在何种扰动下仍可工作，但只是成功案例展示，缺少失败案例、对照模型的同场轨迹和定量统计，不能单独验证“内在不变性”这一因果解释。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出基于预测潜空间世界模型和动作扩散的高效机器人控制方法。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`9fb58ca5f36b3362ddf98975c9fa74861aa468b2723e763330ff718b7833b0ef`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
