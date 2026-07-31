---
title: "[论文解读] Relational Scene Graphs for Object Grounding of Natural Language Commands"
description: "[arXiv 2602.04635][机器人 / 具身智能] 本文研究在三维场景图中显式加入物体间空间关系，是否能帮助大语言模型更准确地把开放词汇自然语言指令指向真实环境中的目标物体，并比较开放词汇与封闭词汇关系的效果。"
arxiv_id: "2602.04635"
announcement_date: "2026-07-31"
primary_category: "robotics"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-31T05:30:51.549561+00:00"
source_sha256: "f7766ed0547412098a104c005d89385dff749b6b21231e775da8880427f7c05a"
tags:
  - "机器人 / 具身智能"
  - "LLM 其他"
  - "机器人自然语言交互"
  - "目标物体落地"
  - "三维场景图"
  - "空间关系"
  - "大语言模型"
  - "视觉语言模型"
  - "开放词汇"
  - "封闭词汇"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">机器人 / 具身智能 · arXiv 2602.04635</p>

# Relational Scene Graphs for Object Grounding of Natural Language Commands

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-31</span>
<span><strong>作者</strong> Kuhn, Julia, Verdoja, Francesco, Mihaylova, Tsvetomila, Kyrki, Ville</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> Aalto University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2602.04635) · [PDF 下载](https://arxiv.org/pdf/2602.04635) · **关键词** 机器人自然语言交互, 目标物体落地, 三维场景图, 空间关系, 大语言模型, 视觉语言模型, 开放词汇, 封闭词汇<br>


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

本文研究在三维场景图中显式加入物体间空间关系，是否能帮助大语言模型更准确地把开放词汇自然语言指令指向真实环境中的目标物体，并比较开放词汇与封闭词汇关系的效果。

**不用术语来说**：当用户说“把桌上的小盘子拿来”时，机器人不仅要理解“拿来”这一动作，还要从多个盘子和桌子中判断用户具体指哪一个。仅知道环境里有哪些物体通常不够，因为人经常用“桌上”“床下”“旁边”等位置关系消除歧义；如果机器人的环境地图没有明确保存这些关系，即使语言模型理解句子，也可能选错目标。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 构建一个基于现成大语言模型的目标物体指代落地流程，使模型能够结合开放词汇指令与三维场景图，识别指令所指向的环境实体。
- 构建一个基于现成视觉语言模型的空间关系生成流程，从机器人建图期间采集的图像中提取并标注相关视图，为三维场景图添加开放词汇空间边，从而支持开放词汇关系与封闭词汇关系的对比研究。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文位于机器人自然语言交互、三维环境表征与语言指令落地的交叉领域。机器人接收到“把桌上的小盘子拿给我”一类开放词汇指令后，不仅要理解动作意图，还必须将“盘子”“桌子”等语言表达对应到真实环境中的具体实体。大语言模型（LLM）擅长处理自由形式语言，但其内部语言知识不能替代机器人对当前环境的感知；三维场景图（3DSG）则以节点表示物体、房间或智能体，以边表示实体间关系，为语言推理提供结构化的几何与语义上下文。本文特别关注物体间的显式空间关系，因为人类常用“床下的箱子”“桌上的盘子”等关系消除同类物体之间的指称歧义，而许多现有3DSG并未记录这类关系。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**语言落地（grounding）**

将自然语言中的名称、描述或动作参数对应到物理环境中的具体实体，例如从多个盘子中确定“桌上的小盘子”指哪一个。本文只评估指令中目标物体的落地，而不是完整的任务规划与动作执行。

</div>
<div class="concept-item" markdown="1">

**三维场景图（3D scene graph, 3DSG）**

一种图结构环境地图：节点表示物体、房间和智能体等实体，边表示实体之间的语义或空间关系。它把机器人感知到的场景整理成LLM可以查询和推理的结构化上下文。

</div>
<div class="concept-item" markdown="1">

**开放词汇与封闭词汇空间关系**

封闭词汇方法只能从预先规定的关系集合中选择标签，开放词汇方法则可生成不受固定列表严格限制的自然语言关系描述。本文比较两类关系表示是否会对LLM的目标物体落地能力产生不同影响。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

研究场景是已完成建图的室内机器人环境。输入包括一条自由形式的开放词汇自然语言指令，以及描述当前环境实体的3DSG；图可以不含显式空间边，也可以加入封闭词汇或由视觉语言模型（VLM）从建图图像推断的开放词汇空间边。目标输出是指令所指向的具体目标物体节点。论文假设场景中的相关实体已经被纳入3DSG，重点考察LLM能否利用图中的空间关系完成消歧，而非同时解决底层运动控制、抓取执行或完整任务分解。核心比较包括两个问题：显式空间边相对无空间边是否提升目标物体落地，以及在已有空间边时开放词汇与封闭词汇关系哪一种更有利。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **SayPlan（Rana et al., 2023）**: 该工作使用3DSG为大语言模型提供环境依据，以支持可扩展的机器人任务规划，说明场景图可以连接语言推理与现实环境。本文将关注点进一步收窄到自然语言指令中的目标物体落地，并专门检验物体间显式空间边的作用。
- **文献[5]的封闭词汇空间边方法**: 本文采用该方法产生的封闭词汇边作为比较条件，并另行实现基于现成VLM的开放词汇关系生成流程。所给原文节选未提供文献[5]的完整题名，因此不进一步补写其模型名称或技术细节。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

在人类环境中工作的机器人必须把自由表达的语言指令连接到可感知、可操作的实体。该过程称为指代落地：机器人需要结合指令和环境上下文，确定相关物体、人员或位置。真实指令往往依赖物体间的空间关系来区分同类实例，因此目标识别不能只靠语言理解或物体类别标签，还需要结构化的场景知识。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **大语言模型与三维场景图结合的指令理解**：大语言模型负责理解开放词汇指令，三维场景图则把环境表示为图：节点对应物体、房间或智能体，边表示实体间的语义联系。模型通过查询或解析该图，将语言中的描述对应到环境节点。
- **带空间边的关系场景图**：近期方法将“在……上方”“在……下方”等空间关系编码为图中的边。其中，封闭词汇方法从预先规定的有限关系集合中选择标签，部分关系可由三维包围盒推断；开放词汇方法则使用大语言模型或视觉语言模型，从图像和文本上下文中生成不受固定标签表严格限制的关系描述。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 多数现有三维场景图没有显式记录物体之间的空间关系，导致图表示缺少人类描述目标时常用的判别信息；当场景中存在多个同类物体时，大语言模型可能无法仅凭节点类别和一般语义关系确定正确实例。
- 已有工作虽然能够生成封闭词汇或开放词汇空间边，但原文指出，尚不清楚这些边是否真的有助于大语言模型解析三维场景图并完成目标物体落地，也缺少证据说明两种关系词汇策略中哪一种更适合该下游任务。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究在“生成空间关系”与“利用场景图执行语言指代落地”之间缺少下游任务验证：空间边是否提供可被大语言模型有效利用的信息仍未确定，而且关系表达自由度与结构规范性之间的取舍也没有经过直接比较。换言之，能够加入关系不等于这些关系会提高机器人对指令中目标物体的识别能力。

</div>
<div markdown="1"><span>核心问题</span>

论文明确提出两个问题：第一，在三维场景图中加入空间边，能否提高大语言模型对自然语言指令中目标物体的落地能力；第二，在已经提供空间边的条件下，封闭词汇关系与开放词汇关系哪一种能带来更好的目标物体落地表现。

</div>
<div markdown="1"><span>作者直觉</span>

空间关系边把原本需要模型从零推断的视觉与几何上下文直接写入场景图。例如，指令中的“床下的箱子”可以与图中连接“箱子”和“床”的“在……下方”关系相匹配，从而缩小候选目标范围。开放词汇关系可能更贴近人类多样化的表达，封闭词汇关系则更统一、便于稳定匹配；因此，以同一目标物体落地任务比较两者，能够检验表达灵活性是否真正优于规范化关系标签。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

论文构建了两条相互衔接、但不进行联合训练的流水线。第一条是目标物体落地流水线：将三维场景图（3DSG）压缩并序列化为文本，与自然语言指称语句一同送入大语言模型（LLM），要求其返回唯一目标物体的标识符。第二条是开放词汇空间关系生成流水线：从机器人建图图像中选择能同时清楚看到一对物体的图像，用实例分割掩码突出这两个物体，再由视觉语言模型（VLM）生成简短的自然语言关系，并将其作为物体间的空间边加入3DSG。最终，可分别使用无显式空间边、闭合词汇空间边和开放词汇空间边的图，比较关系表示对目标物体落地的影响。
直观地说，3DSG相当于机器人持有的一份“带编号的房间物品清单”。关系生成流水线为清单补上“椅子在桌旁”之类的说明；物体落地流水线则让LLM根据用户说法和这份清单，选出用户实际指向的物体编号。该设计刻意采用现成模型，将研究重点放在空间边是否有用以及关系词汇形式是否重要，而不是训练新的感知或语言模型。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 场景图提取与紧凑序列化

从3DSG中提取目标落地所需的信息并转换为适合LLM读取的紧凑文本。二元有序关系写成“目标物体ID｜关系｜锚物体ID”，三元关系“between”则写入一个目标物体和两个锚物体的ID；原文还提到提取颜色标签、中心和尺寸，但所给章节未完整列出全部保留字段及具体序列化模板。

<div class="method-step__io" markdown="1">

**输入**：VLA-3D场景图，或由REACT建图框架生成并转换为VLA-3D格式的3DSG；图中包含带唯一ID的物体节点、类别及可用属性，并可能包含空间关系边。<br>
**输出**：经过预处理、可直接放入提示词的文本化3DSG。

</div>

**直观理解**：原始场景图不适合直接交给语言模型，因此先把它改写成简洁的“物体—关系—物体”记录。目标物体是需要被找出的对象，锚物体则是帮助定位它的参照物。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 候选物体对的视觉证据选择与标记

检查所有同时包含两个物体的图像，计算两者分割掩码的像素数之和，并选择总像素数最大的图像。随后把两个物体的分割轮廓以颜色叠加到原图上，使VLM无需自行猜测需要比较的是哪两个实例。

<div class="method-step__io" markdown="1">

**输入**：REACT保存的建图图像、每个检测物体出现过的图像集合及其实例分割掩码，以及待生成关系的一对物体。<br>
**输出**：一张同时清楚展示并突出标记两个指定物体的预处理图像。

</div>

**直观理解**：这一步类似在照片上用彩笔圈出“请比较这两个东西”，把定位对象的问题提前解决，让VLM集中判断二者的空间关系。选取可见像素最多的照片通常能提供更清晰证据，但论文也指出，当两个物体尺寸差异很大时，这一启发式规则可能失效。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 开放词汇空间关系生成与图增强

调用现成VLM，根据图像生成两个指定物体之间的开放词汇自然语言关系；提示词要求输出格式一致且足够简短，以避免关系边描述过长。生成结果随后作为空间关系边加入对应3DSG。

<div class="method-step__io" markdown="1">

**输入**：突出标记物体对的预处理图像，以及由固定系统消息和随图像变化的用户消息组成的VLM提示。<br>
**输出**：带有VLM生成的开放词汇物体—物体空间边的关系增强3DSG。

</div>

**直观理解**：闭合词汇方法只能从预设关系表中选择词语，而这里允许VLM自由描述，例如图3给出的“both are positioned around the same table, facing each other”。这样能表达仅凭包围盒规则不易概括的关系，但也可能引入视觉判断或措辞不一致造成的噪声。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 基于LLM的目标物体落地

把系统消息与用户消息组成完整提示，其中用户消息同时包含场景图文本和自然语言查询；LLM直接查询该图，并输出最符合指称的物体ID。每次请求都不携带聊天记忆，系统消息和用户消息均重新发送，以减少前序样本对当前判断的影响。

<div class="method-step__io" markdown="1">

**输入**：序列化后的3DSG和一条开放词汇自然语言指称语句或命令。<br>
**输出**：被模型判定为自然语言语句所指对象的唯一物体ID。

</div>

**直观理解**：例如用户说“把桌上的小盘子拿来”，LLM要在带编号的场景清单中结合类别、属性和关系，最终只报出那个盘子的编号。清空对话历史相当于让每道题独立作答，避免上一场景或上一命令泄漏到下一次预测。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。本文的方法由现成LLM、现成VLM、YOLOv11实例检测与分割，以及规则式图预处理组成；所给章节没有报告参数微调、损失函数或端到端优化目标。实验改变的是提供给LLM的3DSG关系表示，而不是通过监督学习更新模型权重。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 3DSG文本化接口**

该模块把图结构转换成LLM可消费的紧凑文本，并明确编码有方向的二元关系以及“between”三元关系中的目标和锚点角色。VLA-3D关系可直接进入该表示；REACT生成的图先转换为VLA-3D格式，再使用相同预处理，以尽量保证不同图来源之间的输入格式一致。

> 直观理解：LLM本身不能直接读取机器人内部的图数据结构，文本化接口充当“翻译器”。统一格式也使性能差异更可能来自空间边类型，而不是不同数据集采用了不同书写方式。

**2. 图像选择与实例高亮模块**

REACT为每个检测实例保存其出现图像及分割掩码；模块在共同可见图像中，以两个掩码的合计像素数最大为准选择一帧，并将掩码轮廓覆盖到原图。该模块依赖场景图保留与对象实例对应的建图图像，因此不能直接用于没有图像记录的3DSG。

> 直观理解：VLM若只看到整张房间照片，可能比较错物体；高亮模块把物体身份固定下来。它也是方法的一项实际限制：若地图只保存几何图而不保存相机图像，就无法按此流程生成开放词汇边。

**3. 提示驱动的现成VLM与LLM模块**

VLM模块从标记图像生成开放词汇关系，LLM模块则从序列化3DSG和指称语句预测目标ID；两者均通过提示进行约束，而非使用本文数据重新训练。物体落地实验采用OpenAI的GPT-4o和GPT-5，以检验结论是否仅依赖单一LLM。

> 直观理解：作者没有设计新的神经网络，而是把现成模型分别当作“看图写关系”和“读图谱找编号”的组件。这样更直接地隔离了论文关注的变量，即给场景图增加什么关系信息是否会改善最终落地。

**训练与推理**

整个方法属于推理期组合。图构建侧，REACT真实场景的原始数据先重新经过REACT处理，并使用在COCO上预训练的YOLOv11完成物体检测和实例分割；随后选取物体对共同出现且掩码总像素最多的图像，叠加掩码轮廓，调用VLM生成简短的开放词汇关系，再把关系写回3DSG。闭合词汇关系则由VLA-3D代码依据几何信息生成，不经过VLM。
目标落地侧，系统将每个3DSG变为紧凑文本，把该文本和一条自然语言指称语句放入用户消息，并连同规定模型行为的系统消息一起发送给GPT-4o或GPT-5。模型不保留跨请求聊天记忆，输出应为最匹配对象的ID；该ID与语句所对应的唯一目标对象比较，用于评估不同空间边配置。原文将目标物体落地定义为把自然语言指称语句解析到环境中的唯一对象，因此该流水线不负责机械臂动作规划或执行。

**复现信息**

公平解释结果所需的关键实现信息包括：REACT真实场景原先只标注chair、couch和dining table三类，作者用完整COCO标签空间重新运行REACT后，将类别扩展到十类，以增加对象及其关系的多样性；REACT的合成场景使用其自有类别空间。REACT图被转换到VLA-3D格式，并以VLA-3D代码生成几何闭合词汇边及相应指称语句，从而可与VLM开放词汇边采用相同的下游LLM接口比较。
在VLA-3D预处理中，作者排除了“closest”和“farthest”，因为它们对大量对象对均有定义，会产生过多且常常无关的关系；同一底层关系若存在多个同义指称模板，则随机只保留一个，以减少重复并测试较多样的语言表达。提示词的完整内容未包含在所给正文片段中，原文仅说明所有提示公开于论文列出的GitHub仓库；VLM的具体型号、生成参数、边写回时的冲突处理规则，以及序列化字段的完整模板在当前节选中未明确报告，复现时仍需核对论文全文及代码。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- VLA-3D：室内三维场景数据，主要用于实验1，测试模型能否利用场景图中的位置属性和空间关系消解自然语言指称。原文摘要称完整评估覆盖14个场景和905条陈述，其中786条为程序生成、119条为人工撰写，但所给章节未明确报告VLA-3D单独包含多少场景或陈述，也未给出训练、验证和测试划分。
- REACT程序生成命令集：用于实验1和实验2。其环境中同类、相似属性对象较多，因此比VLA-3D更容易出现指称歧义。实验2只保留关联关系确由视觉语言模型重新生成的26条指称，其中22条对应封闭关系“near”，4条对应“on”。
- REACT人工命令集：由人撰写的自然语言命令，用于实验2检验开放词汇关系在更自然表达上的效果。所给章节未明确报告该子集总规模；论文摘要只报告全部评估数据中共有119条人工撰写陈述。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**目标对象定位准确率**

模型输出的对象ID与自然语言陈述所指目标ID一致的样本比例；它直接衡量场景图条件下的指称消解能力。 （越高越好，因为正确定位目标对象的陈述占比更大。）

</div>
<div class="metric-item" markdown="1">

**McNemar检验**

针对同一批样本上的成对正确或错误结果，检验两个图输入条件的错误分布是否存在显著差异。论文使用$p<0.05$、$p<0.01$和$p<0.001$三级阈值。 （不存在简单的越高或越低；较小的$p$值表示观察到的条件差异更难用随机波动解释，但不表示效应一定很大。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 实验1，VLA-3D与REACT，比较$G$、$G_P$和$G_{P,E}$

<div class="result-value" markdown="1">

显式关系边在两个数据集和两个模型上均提高准确率。GPT-4o在VLA-3D上由$G$的0.7300升至$G_P$的0.7697，再升至$G_{P,E}$的0.8427；在REACT上相应为0.3617、0.4459和0.5405。GPT-5使用$G_{P,E}$时在VLA-3D达到0.9958，在REACT达到0.8514，均高于其$G_P$结果0.9817和0.7297。

</div>

结果说明，边界框和颜色已能提供部分消歧线索，而把对象间关系直接写成边通常还能进一步帮助模型。GPT-5在完整图上的表现尤其高，表明能力更强的模型更能利用结构化关系；但该比较不能单独证明提升来自真实空间推理，也可能部分来自提示中的关系定义或关系文本与陈述之间的词汇匹配。

<div class="result-source" markdown="1">

来源：表II，实验1结果

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Graph VLA-3D REACT
Random G 0.7300 0.3617
GPT-4o $G_P$ 0.7697 0.4459
$G_P,E$ 0.8427 0.5405
GPT-5 $G_P$ 0.9817 0.7297
$G_P,E$ 0.9958 0.8514

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 实验1，对不同图输入条件进行成对McNemar检验

<div class="result-value" markdown="1">

对GPT-4o，$G$与$G_P$在两个数据集上的差异均不显著；$G$与$G_{P,E}$在VLA-3D上达到$p<0.001$、在REACT上达到$p<0.01$；$G_P$与$G_{P,E}$仅在VLA-3D上达到$p<0.001$。对GPT-5，所有已报告比较均显著，其中$G_P$与$G_{P,E}$在VLA-3D上为$p<0.01$、在REACT上为$p<0.05$。

</div>

统计检验强化了“完整空间关系有帮助”的结论，尤其是完整图相对名称基线的差异。与此同时，GPT-4o在REACT上从$G_P$加入边后的提升未达到显著水平，说明数值上升并不自动等于稳定效应；检验也不衡量提升幅度或跨场景泛化能力。

<div class="result-source" markdown="1">

来源：表III及实验1结果第2节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

For GPT-4o, no statistically significant differences were observed when comparing the baseline G with the graph $G_P$. When comparing G with $G_P,E$ on both datasets, a statistical significance was shown, from $G_P$ to $G_P,E$ only on the VLA-3D dataset. For GPT-5, all differences were statistically significant.

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 实验2，REACT程序生成命令与人工命令，比较封闭词汇边和自动生成的开放词汇边

<div class="result-value" markdown="1">

开放词汇边没有形成一致优势：在程序生成命令上，GPT-4o准确率由封闭边的0.7308降至开放边的0.6923，而GPT-5由0.8077升至0.8462；在人工命令上，GPT-4o由0.4202降至0.3613，GPT-5由0.6218降至0.5882。作者报告这些差异均不具有统计显著性。

</div>

开放关系有时能提供更具体描述，但整体结果随模型和命令来源改变，无法据此认定开放词汇优于或劣于封闭词汇。该结论只是“没有发现显著差异”，并不证明两类关系等效，因为实验2只有26条符合条件的程序生成指称，统计功效有限，而且未成功重估的边仍沿用封闭关系。

<div class="result-source" markdown="1">

来源：表IV及实验2结果第2节

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

These differences in accuracy between the closed-vocabulary edges and the generated open-vocabulary edges were not statistically significant.

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

- 随机名称基线图$G$：节点只含对象名称与ID，不含属性或边。同类对象仅凭名称无法区分，因此每个目标的理论正确概率为$1/|O_C|$，其中$O_C$是同一对象类别的实例集合。该基线衡量没有空间信息时仅靠类别名称能够达到的水平。
- 属性图$G_P$：在$G$的节点上加入颜色和边界框，但不加入对象间关系。它与$G$的比较隔离了节点级外观和几何位置属性的作用，与$G_{P,E}$的比较则隔离了显式空间边的增益。
- 封闭词汇关系图$G_{P,E}$：包含节点属性以及数据集中预定义类型的空间边，是实验1的完整场景图条件，也是实验2评价开放词汇边是否更有表达力的直接参照。
- 开放词汇关系图：用GPT-4o视觉语言模型从图像中生成自然语言空间关系，以生成关系替换可重新估计的封闭词汇边；没有合适图像时仍沿用原封闭词汇边。它测试自由文本关系是否比固定关系类别更有助于对象定位。

**实验想回答的问题**

- 实验1检验：在三维场景图中加入对象颜色、三维边界框等位置属性以及显式空间关系边，是否能提高大语言模型从自然语言指称中定位目标对象的准确率；同时，这种收益是否跨数据集和模型成立并具有统计显著性。
- 实验2检验：由视觉语言模型根据机器人采集图像生成的开放词汇空间关系，能否在目标对象定位任务上优于预先定义关系类型的封闭词汇空间边，并考察自动生成关系的可靠性。

**实验实现**

实验1使用GPT-4o和GPT-5。提示中解释任务、输入、预期输出、全部空间边定义并提供一个示例；用户消息包含序列化三维场景图和待解析陈述，模型应只输出目标对象ID。由于GPT-5只接收一个输入，系统消息与用户消息被合并。$G_P$与$G_{P,E}$分别通过同一定位流水线评测；$G$则按同类对象集合$O_C$中的均匀随机选择计算准确率，并在统计检验时从$O_C$随机抽取一个对象。实验2使用GPT-4o视觉语言模型读取预处理图像以及待判断的两个对象名称和ID，生成开放词汇关系；随后以与实验1相同的定位设置比较开放与封闭关系。论文未明确报告随机种子、重复运行次数、温度、解码参数或置信区间。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 节点属性消融：比较名称图$G$与加入颜色和边界框的$G_P$ | GPT-4o在VLA-3D上从0.7300升至0.7697，在REACT上从0.3617升至0.4459，但两处McNemar检验均不显著。GPT-5在VLA-3D和REACT上的$G_P$准确率分别为0.9817和0.7297；相对$G$的差异均达到$p<0.001$。 | 该比较隔离颜色与边界框等节点级信息的作用。结果表明强模型可以有效读取位置属性，而GPT-4o的数值提升尚不足以排除随机波动；由于$G$采用随机同类选择，它还混合衡量了属性信息与模型推理能力，而不是纯粹的边界框贡献。 | 表II、表III及实验1结果第2节<br><span class="experiment-evidence">For GPT-4o, no statistically significant differences were observed when comparing the baseline G with the graph $G_P$.</span> |
| 空间边消融：比较仅有节点属性的$G_P$与完整关系图$G_{P,E}$ | GPT-4o加入空间边后，VLA-3D准确率由0.7697升至0.8427，REACT由0.4459升至0.5405；GPT-5相应由0.9817升至0.9958、由0.7297升至0.8514。McNemar检验中，GPT-4o仅在VLA-3D达到$p<0.001$，GPT-5在VLA-3D和REACT上分别达到$p<0.01$和$p<0.05$。 | 这是最直接检验显式关系边价值的消融：节点内容保持不变，只增加对象间关系。四个组合的准确率都提高，但统计证据强度不同，因此可支持“关系边通常有益”，不能支持“每个模型和数据集上都必然产生稳定提升”。 | 表II、表III及实验1结果第2节<br><span class="experiment-evidence">For both datasets, edges had a considerable effect on the performance of both LLMs, with GPT-5 outperforming GPT-4o in all cases.</span> |

**定性案例**

- 开放关系“both are positioned around the same table, facing each other”比封闭关系“near”提供了更具体且语义相关的布局信息；相反，“left side of the table, closer to the camera”依赖拍摄视角，而三维场景图不包含相机位姿，换一个观察方向后左右和远近可能反转。该对照说明开放词汇关系的潜在价值在于更细致的语义描述，但生成器必须避免相机中心描述、图中不存在的参照物以及用于图像标注的轮廓颜色。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：研究利用带空间关系的3D场景图提升机器人对自然语言指令的目标物体落地能力。; rule check: matched taxonomy keywords; top rule score=8.0
- 全文指纹：`f7766ed0547412098a104c005d89385dff749b6b21231e775da8880427f7c05a`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
