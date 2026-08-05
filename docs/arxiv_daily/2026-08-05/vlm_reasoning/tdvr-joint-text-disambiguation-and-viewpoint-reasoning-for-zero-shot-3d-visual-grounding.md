---
title: "[论文解读] TDVR: Joint Text Disambiguation and Viewpoint Reasoning for Zero-Shot 3D Visual Grounding"
description: "[arXiv 2608.03763][VLM Reasoning] TDVR针对零样本3D视觉指代中的文本歧义与视点缺失，通过补全查询语义、推断观察视点并区分同类干扰物，使自然语言描述能够更可靠地对应到三维场景中的目标实例。"
arxiv_id: "2608.03763"
announcement_date: "2026-08-05"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-05T03:43:27.187893+00:00"
source_sha256: "75e8877f8df3d2dec22e11d91d3e290c897bb2b640ceb32763fc53e60df3105d"
tags:
  - "VLM Reasoning"
  - "LLM Reasoning"
  - "三维视觉指代定位"
  - "零样本学习"
  - "文本消歧"
  - "视角推理"
  - "三维场景图"
  - "多模态大语言模型"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.03763</p>

# TDVR: Joint Text Disambiguation and Viewpoint Reasoning for Zero-Shot 3D Visual Grounding

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-05</span>
<span><strong>作者</strong> Qingxi Du, Junbo Wang, Yuke Li, Yining Zhu</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Northwestern Polytechnical University Software School Xi’an Shaanxi China；Northwestern Polytechnical University；Software School；Northwestern Polytechnical University School of Computer Science Xi’an Shaanxi China；School of Computer Science</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.03763v1) · [PDF 下载](https://arxiv.org/pdf/2608.03763v1) · **关键词** 三维视觉指代定位, 零样本学习, 文本消歧, 视角推理, 三维场景图, 多模态大语言模型<br>


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

TDVR针对零样本3D视觉指代中的文本歧义与视点缺失，通过补全查询语义、推断观察视点并区分同类干扰物，使自然语言描述能够更可靠地对应到三维场景中的目标实例。

**不用术语来说**：机器人若要根据一句话在三维房间中找到物体，不能只识别物体类别：同一房间里可能有多把外观相近的椅子，而“左边”“后面”等说法还会随观察方向改变。现有方法在不知道说话者从哪里观察、且描述过短或含有多个相似候选时，容易选错物体，甚至只能在候选之间猜测。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出无需额外训练的TDVR框架，将查询消歧与视点推理联合起来：利用物体外观和空间关系丰富原始查询，再把自然语言转换为可用于场景匹配的结构化描述。
- 提出面向未知观察方向和同类干扰物的推理机制：通过旋转点云寻找最符合描述的视点，并在该视点下比较同类别实例之间的空间关系，以提高相似目标的可区分性。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

三维视觉指代定位（3D Visual Grounding, 3DVG）要求智能体依据自然语言描述，在三维场景中找出被指称的对象，通常输出该对象的三维实例或包围框。与二维定位相比，三维场景不仅包含类别和外观信息，还包含复杂的几何结构以及依赖观察方向的空间关系；例如“左侧”和“后方”的含义会随观察者视角改变。本文研究更严格的零样本设定：不使用目标任务的标注数据训练专用定位模型，而是借助大语言模型或多模态大语言模型已有的语义与视觉推理能力完成定位。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**零样本三维视觉指代定位**

输入自然语言查询和三维场景，在不利用目标任务标注数据训练专用模型的条件下，确定查询所指的三维对象。其难点是同时对齐文本语义、对象外观与三维空间结构。

</div>
<div class="concept-item" markdown="1">

**视角依赖空间关系**

“左边”“右边”“前方”“后方”等关系必须相对于某个观察方向解释；同一组对象在视角旋转后可能呈现相反的方向关系。若查询没有明确说明观察者姿态，定位系统就需要推断最符合描述的视角。

</div>
<div class="concept-item" markdown="1">

**语义三维场景图**

场景图把检测到的对象表示为节点，并用对象之间的空间或语义关系连接节点，从而将原始点云转换为便于推理的结构化表示。本文还结合低遮挡的二维对象图像，为节点补充类别与外观信息。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入包括三维点云场景、从中检测得到的对象实例，以及描述目标对象的自然语言查询；查询可能较短、含有视角未指定的方向词，也可能对应多个类别相同、外观相似且彼此邻近的候选对象。系统可利用对象的三维位置关系和裁剪得到的二维外观图像，但处于无需任务专用训练的零样本、training-free 设置。输出是查询所指目标实例的三维定位结果。本文将问题理解为联合消歧：一方面补充并结构化查询中的类别、外观和空间关系，另一方面推断最符合描述的观察视角，再综合视角一致性、同类对象区分、类别匹配和外观匹配信息选择目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **VPP-Net**: 与本文最直接相关的监督式视角建模方法：它显式预测说话者视角并旋转三维场景，说明视角信息能够缓解方向关系歧义；但其属于监督式方法，而TDVR面向无需任务专用训练的零样本设定。
- **LASP**: 代表训练自由的零样本3DVG路线：它使用大语言模型把自然语言指令转换为可执行的三维空间程序，并通过数学逻辑解析对象及空间关系。TDVR与之同属基于大模型的结构化推理范式，但进一步针对查询歧义、未知视角和同类相似实例干扰进行联合处理。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

3D视觉指代要求智能体依据自然语言，在复杂三维环境中精确定位目标，服务于具身智能和自动驾驶等需要语言—空间交互的任务。实际描述常同时包含类别、外观及“左侧”“后方”等方向关系；然而室内场景又常有多个类别相同、外观相似且位置接近的实例，因此正确定位既依赖理解语言，也依赖恢复描述者所采用的观察坐标系。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **基于类别、外观与文本—三维特征对齐的3D视觉指代方法**：这类方法通常检测三维场景中的候选实例，再比较查询文本与候选物体的类别或视觉特征，选择语义相似度较高的实例。它们能够处理明确的物体名称和外观描述，但原文指出，多数现有模型没有充分考虑观察视点对方向词含义的影响。
- **基于自然语言空间关系的候选筛选方法**：这类方法利用“在某物旁边”“位于某物左侧”等关系约束，在多个候选中寻找与参照物位置关系相符的目标。然而，当输入没有给出相机姿态或观察方向时，同一空间关系会因视点变化而反转；当多个同类实例都满足简短描述时，关系约束也不足以形成唯一答案。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 视点依赖的空间歧义没有被显式解决：“左边”“后面”等观察者中心方向会随视点改变，例如旋转$180^\circ$后，“左侧”可能对应另一物体。若模型直接在固定或未知坐标系中解释方向词，就会把正确的关系约束应用到错误方向，导致目标定位错误。
- 相似实例干扰下缺少细粒度判别：在多个物体具有相同类别、近似外观和相近位置时，简短查询可能同时匹配多个候选。原文认为多数智能体缺乏进一步区分这些实例的方法，因而可能在候选之间随机猜测，无法得到稳定且确定的定位结果。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

已有零样本方法尚缺少一个统一、无需任务训练的推理过程，能够先利用场景中的外观与关系证据补足含糊查询，再从三维几何中恢复描述所隐含的观察视点，并在该视点下对同类别候选进行关系级消歧。换言之，文本歧义、未知视点和相似实例干扰往往被分开处理或未被处理，缺乏把三者联结为可执行几何约束的端到端方案。

</div>
<div markdown="1"><span>核心问题</span>

在不针对下游数据集进行额外训练的条件下，能否结合多模态大语言模型、语义3D场景图和点云旋转推理，将含糊自然语言转化为结构化约束，推断最符合描述的观察视点，并据此从多个相似候选中可靠地定位唯一目标？

</div>
<div markdown="1"><span>作者直觉</span>

一句含糊描述单独看可能不足以确定目标，但三维场景本身提供了额外证据：候选物体长什么样、附近有哪些物体，以及它们之间的几何关系。先用这些证据补全并结构化查询，相当于把模糊语言变成可核验的条件；再尝试不同观察方向，寻找能让“左侧”“后方”等关系同时成立的视点；最后在该视点下比较同类物体与其他实例的相对布局，就能逐步排除仅在类别或外观上相似的干扰项。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

TDVR是一个无需针对下游数据训练的零样本3D视觉指代定位框架。输入为室内场景的3D点云、配准的RGB-D帧与自然语言查询；系统先用预训练检测器把场景转换为语义3D场景图，再借助多模态大模型和大语言模型补充外观、观察者视角下的空间方向以及同类实例间的相对位置，并将增强查询解析为结构化约束。随后，框架对每个候选物体遍历水平旋转视角，分别计算全局空间关系得分$S_v$、同类消歧得分$S_c$、类别匹配得分$S_{cat}$和外观匹配得分$S_{app}$，最终以融合分数$S_{total}$排序并输出最高分候选的3D包围盒。
技术上，TDVR把通常纠缠在一起的三个问题拆开处理：查询含义不完整由语言消歧解决，诸如“左边”“前面”等依赖观察方向的关系由视角推理解决，多把同类椅子同时满足全局关系的问题则由类内相对位置解决。直观地说，系统先把含糊的“那把椅子”改写成一张更明确的寻找清单，再转动场景寻找最符合清单中方向关系的观察角度，最后结合物体类别和外观作出决定。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 语义3D场景图构建

预训练3D检测器产生实例集合$\mathcal{O}=\{o_1,\ldots,o_n\}$；每个节点$v_i$保存3D包围盒$p_i$、类别标签$l_i$和最佳二维裁剪$a_i$，其中$a_i$来自可见点比例最高的RGB帧，边集合$E$按空间邻近关系构造。

<div class="method-step__io" markdown="1">

**输入**：场景点云$\mathbf{P}_w$、配准RGB帧集合$\mathcal{F}$、深度图$\mathcal{D}_f$、相机内参$K$、世界到相机的外参$T_{w2c}$以及可见性阈值$\epsilon$。<br>
**输出**：语义场景图$G=(V,E,\mathcal{X}_V)$，其节点属性为$\mathbf{x}_i=[p_i,a_i,l_i]$。

</div>

**直观理解**：这一步把稠密点云整理成“物体清单加关系网络”，并为每个物体挑选遮挡最少的一张照片。后续模块因此无需反复处理全部原始点，而可以直接查询某个物体在哪里、属于什么类别以及看起来怎样。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 观察者中心的协同文本消歧

多模态大模型从二维裁剪生成颜色、纹理等外观描述；系统以$V_{gt}=L-P$建立观察者中心坐标系，补充目标相对多个锚点的方向描述，并在同类物体集合的局部坐标系中生成目标的类内相对位置描述，最后由大语言模型融合这些信息与原始查询。

<div class="method-step__io" markdown="1">

**输入**：原始查询、场景中物体的二维裁剪、相机位置$P$与注视点$L$、各实例的3D包围盒及类别。<br>
**输出**：包含目标属性、锚点关系和同类区分线索的消歧查询。

</div>

**直观理解**：自然语言中的“左边”必须先说明是谁看过去的左边，而“椅子旁边的椅子”还需要更多外观或排序线索。该步骤相当于自动追问并补全这些缺失条件，使后续几何推理面对的是较明确的描述。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 结构化关系抽取

大语言模型通过四阶段思维链依次抽取目标实体$T$及外观属性$\mathcal{A}_T$、锚点集合$S_{anc}$、标准化空间关系集合$\mathcal{R}=\{\langle s_i,r_i\rangle\}$和类内方向线索；若输出不符合预定义格式，则重新执行抽取。

<div class="method-step__io" markdown="1">

**输入**：经过消歧的自然语言查询。<br>
**输出**：可由几何与特征模块直接读取的结构化目标类别、外观文本、锚点类别、方向关系及类内位置。

</div>

**直观理解**：大模型不直接猜最终包围盒，而是把长句转换成类似数据库条件的字段，例如“目标=椅子、锚点=冰箱、关系=冰箱在目标右侧”。格式复核降低了自由文本无法被后续程序稳定解析的风险。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 视角推理与同类候选消歧

对每个候选物体遍历水平角集合$\Theta$，旋转场景并计算候选到各类锚点的相对向量与标准方向向量的对齐程度，由此得到最佳视角集合$\Theta_{best}$和得分$S_v$；在最佳视角下，再比较候选相对同类几何中心$\mathbf{M}_C$的方向，得到类内混淆得分$S_c$。

<div class="method-step__io" markdown="1">

**输入**：场景图$G$、结构化空间约束以及每个候选目标的3D中心坐标。<br>
**输出**：每个候选物体的最佳水平视角、全局方向匹配得分$S_v$和类内区分得分$S_c$。

</div>

**直观理解**：系统相当于在水平方向转动整个房间，寻找一个能让“冰箱在椅子右侧”等描述同时成立的观察角度。若多把椅子都满足这一关系，它再检查哪一把位于椅子群内部所描述的“最右边”或其他相对方向。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 最优视角匹配得分

$$
S_v=\max_{\theta\in\Theta}\sum_{j=1}^{N}\Psi(T,C_j,\theta),\qquad \Psi(T,C_j,\theta)=\max_{A_i\in C_j}\left\{\operatorname{ReLU}\left(\frac{\vec{v}_{TA_i}(\theta)\cdot\vec{v}_{\mathrm{ref},j}}{\|\vec{v}_{TA_i}(\theta)\|}\right)\right\}
$$

**符号说明**

- $S_v$：候选目标在所有测试视角中的最佳全局空间关系匹配分数。
- $\Theta$：待遍历的水平旋转角集合。
- $\theta$：一个候选水平旋转角。
- $T$：当前被评估的候选目标物体。
- $N$：结构化查询中的空间约束数量。
- $C_j$：第j条约束所指锚点的类别。
- $A_i$：属于锚点类别的一个具体实例。
- $\vec{v}_{TA_i}(\theta)$：旋转角为θ时，从候选目标T指向锚点实例$A_i$的相对向量。
- $\vec{v}_{\mathrm{ref},j}$：第j条文本空间关系对应的标准方向向量。
- $\Psi(T,C_j,\theta)$：在给定视角下，目标与第j类锚点之间的最佳正向对齐分数。
- $\operatorname{ReLU}$：将负对齐值截断为零的函数，用于排除方向相反的匹配。

<div class="equation-explanation" markdown="1">

**直观理解**：内层先在同一锚点类别的多个实例中选择最符合文本方向的一个，外层把所有空间约束的匹配程度相加，再从全部水平视角中取最大值。它同时回答“从哪个方向看最合理”和“该候选在这个方向下有多符合查询”，是TDVR处理缺失视角的核心。<br>
**原文位置**：第3.5节，公式(7)与公式(8)

</div>

</div>

<div class="equation-block" markdown="1">

#### 最终目标融合分数

$$
S_{\mathrm{total}}=S_{\mathrm{cat}}\cdot\left(\alpha S_v+\beta S_c+\gamma S_{\mathrm{app}}\right)
$$

**符号说明**

- $S_{\mathrm{total}}$：一个候选物体的最终综合评分。
- $S_{\mathrm{cat}}$：候选类别标签与查询中目标类别文本的语义相似度。
- $S_v$：候选的最佳视角及全局空间关系匹配分数。
- $S_c$：候选在同类别实例群体中的相对方向匹配分数。
- $S_{\mathrm{app}}$：候选二维裁剪与目标外观文本之间的跨模态相似度。
- $\alpha$：全局视角关系分数的融合权重。
- $\beta$：类内消歧分数的融合权重。
- $\gamma$：外观匹配分数的融合权重。

<div class="equation-explanation" markdown="1">

**直观理解**：括号内把全局方向、同类相对位置和外观三类互补证据加权组合，类别相似度则乘在外部作为门控。这样，候选不仅要处于合理位置并具有正确外观，还必须在类别语义上与目标相符；系统最终选择$S_{total}$最大的候选。<br>
**原文位置**：第3.8节，Target Grounding公式

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。TDVR被定义为training-free、zero-shot推理框架，文中没有给出需要反向传播优化的损失函数，也没有在ScanRefer上训练新增网络参数；BERT、CLIP、预训练检测器、MLLM和LLM均作为现成模型参与检测、编码、描述生成或结构化解析。公式中的$S_v$和$S_{total}$是推理阶段的搜索与排序目标，而不是训练损失：前者通过离散遍历$\Theta$取最大值，后者通过对候选物体排序取最大值。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 观察者中心协同消歧与结构化抽取**

模块先以相机位置$P$为原点，并将视线$V_{gt}=L-P$投影到地面以定义水平朝向；目标到锚点的向量与八个标准方向向量比较，最大余弦相似度对应的方向被写入模板。水平方向由观察者坐标确定，垂直关系直接比较$Z$轴；同类位置则以该类别全部实例的平均坐标为局部中心生成描述，之后大语言模型融合原始查询、外观描述、锚点方向和类内线索，并抽取$T$、$\mathcal{A}_T$、$S_{anc}$及$\mathcal{R}$。

> 直观理解：该模块解决的是“文字条件本身不够可执行”的问题：原查询可能省略观察方向、外观或同类排序，而几何算法不能可靠推断这些隐含语义。它先显式补全条件，再把自然语言压缩为固定字段；需要注意，原文将这种处理描述为大模型推理和格式复核，而不是通过ScanRefer标注训练一个新的解析器。

**2. 视角感知方向推理**

共同旋转两个物体后，其相对向量满足$\mathbf{v}'=R\mathbf{v}$，与旋转中心$\mathbf{c}$无关；再结合垂直方向可直接由$Z$轴判断的先验，论文把原本的六维视角搜索简化为绕竖直轴的一维角度搜索。对于约束$j$，模块在锚点类别$C_j$的全部实例中取最大正向对齐值$\Psi(T,C_j,\theta)$，使用ReLU去除反向匹配干扰，并遍历$\theta\in\Theta$得到$S_v$与$\Theta_{best}$；所有候选均参与计算，不先做高分筛选。

> 直观理解：“左、右、前、后”会随观察方向改变，因此固定坐标系可能把正确目标判错。该模块不直接假设视角，而是尝试多个水平旋转角；对同类锚点取最佳匹配可容纳场景中存在多张桌子或多台柜子的情况，对全部目标保留评分则减少早期误删造成的级联错误。

**3. 视角下的类内解耦与多证据融合**

在候选对应的最佳视角下，同类集合$\mathcal{S}_C$的中心为$\mathbf{M}_C=\frac{1}{n}\sum_{O_j\in\mathcal{S}_C}\mathbf{p}'_j$，候选位移为$\vec{v}_{conf}=\mathbf{p}'_i-\mathbf{M}_C$；该位移与类内参考方向$\vec{R}_{ref}$的余弦相似度构成$S_c$。与此同时，BERT给出类别语义相似度$S_{cat}$，CLIP给出二维裁剪与外观文本的相似度$S_{app}$，最终由类别门控的加权融合分数选择候选。

> 直观理解：全局关系可能只能定位到一组相邻同类物体，例如两把椅子都在桌子左侧；类内中心提供了一个只针对“椅子群”的稳定参照，从而检查哪把椅子位于群体右侧。最后加入类别和外观证据，是为了避免仅靠几何方向把位置合适但语义或长相错误的实例选中。

**训练与推理**

训练阶段：原文方法章节未设置TDVR专属训练流程，也未描述对预训练检测器、BERT、CLIP、MLLM或LLM进行微调，因此不能把分数融合解释为端到端学习。推理阶段：首先检测场景实例，并依据深度一致性从RGB-D帧中为各实例挑选遮挡最少的二维裁剪，构成场景图；随后利用观察者坐标、外观生成和类内空间描述增强原查询，再由LLM输出经过格式校验的结构化表示。
对每个候选物体，系统依据结构化锚点约束遍历水平角$\theta\in\Theta$，计算各角度下的方向对齐并取得$S_v$及$\Theta_{best}$；接着在所得视角下计算同类相对位置分数$S_c$。最后，BERT计算类别分数$S_{cat}$，CLIP计算外观分数$S_{app}$，四类信息经$S_{total}$融合，对所有候选排序并返回最高分实例的3D包围盒。方法明确强调视角和混淆分数均对全部候选计算，不在中间阶段提前过滤，以避免早期判断错误传播到最终结果。

**复现信息**

公平复现所必需、且原文摘录明确给出的设计包括：场景图节点由检测实例的3D包围盒、类别标签与最佳二维裁剪组成，边按空间邻近性建立；二维裁剪通过投影和深度一致性条件$|d_{calc}-d_{map}|<\epsilon$统计可见点比例，并选择比例最高的帧。视角搜索只优化绕竖直轴的水平旋转，因为垂直关系直接比较$Z$轴；方向约束采用标准参考向量、ReLU和同类锚点最大池化，类内消歧使用最佳视角下的类别几何中心。
语义模型分工也影响复现：MLLM负责从裁剪生成细粒度外观文本，LLM负责查询融合、思维链结构化抽取和格式复核，BERT负责类别文本嵌入，CLIP负责图像—外观文本匹配。所给方法摘录未明确报告预训练检测器、MLLM、LLM、BERT和CLIP的具体模型版本，也未给出角度集合$\Theta$的采样间隔、可见性阈值$\epsilon$、邻近边阈值以及融合权重$\alpha$、$\beta$、$\gamma$的数值；这些参数不能从摘录中自行补全，复现实验时需要回查论文其余章节或代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- ScanRefer：建立在ScanNet三维场景之上，包含$51{,}583$条自由形式自然语言描述，涉及$11{,}046$个物体。其描述强调外观属性和复杂空间关系，用于测试三维点云与语言之间的跨模态对齐及歧义消解能力；论文在该数据集上报告了主要定量结果。
- Sr3D：ReferIt3D中的合成空间关系子集，使用合成的空间模板。由于其构造代码能够推断相机位姿，适合测试方法中的视角推理模块；论文说明在该数据集上报告不同划分下的定位准确率。
- Nr3D：ReferIt3D中的自然语言子集，包含自然语言描述，但不提供相机位姿信息。因此论文没有将其用于实验，而是选择Sr3D进行视角相关评估。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**Acc@0.25**

预测三维边界框与真实边界框的交并比至少为$0.25$时，被视为定位正确的比例；该阈值较宽松，主要反映目标召回和粗粒度定位能力。 （越高越好，因为更高比例表示更多预测与真实目标有足够空间重叠。）

</div>
<div class="metric-item" markdown="1">

**Acc@0.5**

预测框与真实框的交并比至少为$0.5$时的正确率；相较于$0.25$，它要求更精确的空间定位。 （越高越好，尤其适合检验视角推理、相似物体区分和精确框定位是否有效。）

</div>
<div class="metric-item" markdown="1">

**类别分组准确率**

论文按场景中目标类别是否唯一，将样本划分为$Unique$和$Multiple$，并在相应分组上报告定位准确率；$Multiple$专门检验存在同类干扰物时的区分能力。 （越高越好；其中$Multiple$上的提升比$Unique$更能说明方法是否解决了相似实例辨别问题。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### ScanRefer整体测试，比较零样本TDVR与既有方法

<div class="result-value" markdown="1">

TDVR取得$70.85\%$的Acc@0.25和$64.06\%$的Acc@0.5；在Acc@0.5上，超过SPAZER的$48.8\%$，按论文正文的表述提升$15.26$个百分点。

</div>

这说明TDVR不仅能够找到大致正确的物体，而且在更严格的空间重叠要求下也能更精确地定位。结果支持作者关于整体定位能力提升的主张，但不能单独证明每一个模块分别带来了多少收益，因为摘录中没有提供逐模块消融结果。

<div class="result-source" markdown="1">

来源：Section 4.2, Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Under the overall metric, we achieve 70.85% (Acc@0.25) and 64.06% (Acc@0.5).

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### ScanRefer整体结果与此前最佳零样本方法SPAZER比较

<div class="result-value" markdown="1">

在严格的Acc@0.5指标上，TDVR达到$64.06\%$，SPAZER为$48.8\%$；论文称TDVR是首个超过$60\%$的零样本方法，并报告相对SPAZER提升$15.26$个百分点。

</div>

该比较直接检验TDVR是否改善零样本场景下的精确定位，结果表明改进幅度主要体现在严格阈值上。不过，提升可能同时受到查询消歧、视角推理、相似物体判别以及检测器差异等因素影响，不能仅归因于某一个设计。

<div class="result-source" markdown="1">

来源：Section 4.2, Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Notably, our approach is the first zero-shot method to surpass the 60% threshold on the strict Acc@0.5 metric, outperforming the previous best competitor, SPAZER (48.8%), by a substantial margin of 15.26%.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### ScanRefer中的Multiple类别，重点考察同类干扰物

<div class="result-value" markdown="1">

在$Multiple$类别的Acc@0.5上，TDVR达到$58.93\%$，比此前最佳零样本方法高$15.53$个百分点。

</div>

$Multiple$包含同一类别的多个候选物，因此该结果比唯一目标场景更直接地检验细粒度实例区分。结果与作者关于视角感知方向推理和基于视角的相似度解耦有助于消除空间歧义的解释一致，但由于摘录未给出完整基线表格，无法进一步核验所有比较对象和统计显著性。

<div class="result-source" markdown="1">

来源：Section 4.2, Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

We achieve 58.93% (Acc@0.5), exceeding the previous best zero-shot method by 15.53%.

</div>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 所提供实验摘录没有完整给出Table 1和Table 2的数值表，也没有报告运行次数、方差或显著性检验，因此难以判断改进的统计稳定性；Sr3D各划分的具体结果在摘录中为“原文未明确报告”。
- 论文没有提供消融实验数值来分别隔离查询消歧、视角推理、干扰物判别和视觉语言匹配模块，因此无法仅凭当前证据确定各组件的独立贡献。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- SPAZER：此前的零样本三维视觉指代表达方法，是最重要的直接比较对象，用于衡量TDVR相对于已有零样本方法的改进。
- SeeGround：用于定性比较的三维目标定位方法，可以观察不同方法在复杂空间关系和相似物体场景中的具体预测差异。
- TSP3D：全监督方法，用于比较零样本TDVR与依赖训练标注的方法之间的性能差距。
- Pseudo-EV：近期全监督方法，用于检验TDVR是否不仅优于零样本基线，而且能够接近或超过监督式方法。

**实验想回答的问题**

- 在零样本三维视觉指代表达任务中，TDVR能否在ScanRefer和Sr3D上提升目标定位准确率，尤其是严格的交并比阈值$0.5$下的性能？
- TDVR是否能有效处理同类干扰物、空间关系和视角缺失等困难，而不仅仅是识别场景中唯一的目标类别？

**实验实现**

实验使用Mask3D进行初始实例分割，并据此生成场景图节点。查询消歧使用GPT-4o，温度为$0.7$；结构化推理使用DeepSeek-V3，温度为$0.3$，并采用基于思维链的解析。文本嵌入由本地部署的all-MiniLM-L6-v2计算；视角感知方向推理中将$10$度设为一个旋转单位。视觉语言匹配使用CLIP ViT-B/32提取二维物体裁剪图和外观描述的特征。目标融合阶段的权重设为$\alpha=5$、$\beta=3$和$\gamma=1$。全部实验在单张NVIDIA RTX 4090 GPU上进行。论文给出了定性比较图Figure 5，并说明Table 2报告Sr3D上的比较结果；所提供摘录未包含Table 1和Table 2的完整数值行。

**关键消融**

原文未明确报告，或自动提取阶段未获得可靠数据。

**定性案例**

- Figure 5展示四个包含空间关系描述或多个相似干扰物的案例。第一例的描述要求找到“沿墙从右数第一把椅子”：SeeGround错误预测为桌子，SPAZER预测为从右数第二把椅子，而TDVR正确定位到真实目标；其余三个案例中，TDVR均与真实框一致。该结果直观说明TDVR能够利用方向、相对位置和外观信息处理歧义查询，但仅是少量定性案例，不能替代整体测试集上的统计结论。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces a training-free multimodal reasoning framework for textual disambiguation and viewpoint inference in 3D visual grounding.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`75e8877f8df3d2dec22e11d91d3e290c897bb2b640ceb32763fc53e60df3105d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
