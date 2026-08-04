---
title: "[论文解读] Recompute or Reuse? Diagnosing and Mitigating Textual Shortcuts in VLM Self-Reflection"
description: "[arXiv 2608.01930][VLM Reasoning] 本文将视觉语言模型自反思中的更新失败重新刻画为“当前图像上的新鲜视觉重计算”与“先前思维链中的陈旧证据复用”之间的竞争，并据此提出隔离先前推理的干预思路。"
arxiv_id: "2608.01930"
announcement_date: "2026-08-04"
primary_category: "vlm_reasoning"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-08-04T10:57:54.575242+00:00"
source_sha256: "db49fda0b4ba14d5086fa456348eb2b8188cf8ce8ac757ad14fc8c1b77062840"
tags:
  - "VLM Reasoning"
  - "LLM Reasoning"
  - "多模态 VLM"
  - "视觉语言模型"
  - "视觉自反思"
  - "思维链"
  - "文字捷径"
  - "视觉重计算"
  - "反事实图像"
  - "证据更新"
  - "上下文复用"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">VLM Reasoning · arXiv 2608.01930</p>

# Recompute or Reuse? Diagnosing and Mitigating Textual Shortcuts in VLM Self-Reflection

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-08-04</span>
<span><strong>作者</strong> Wenxiao Fan, Jingling Fu, Fang Li, Luohang Liu, Yu He, Lichen Ma, Zhiyang Yu, Weishan Bi, Junshi Huang, Yan Li, Gu Simiu, Kan Li</span>
<span><strong title="按论文首页署名机构汇总">通讯单位</strong> School of Computer Science, Beijing Institute of Technology；Institute of Artificial Intelligence and Robotics, Xi’an Jiaotong University</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2608.01930v1) · [PDF 下载](https://arxiv.org/pdf/2608.01930v1) · **关键词** 视觉语言模型, 视觉自反思, 思维链, 文字捷径, 视觉重计算, 反事实图像, 证据更新, 上下文复用<br>


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

本文将视觉语言模型自反思中的更新失败重新刻画为“当前图像上的新鲜视觉重计算”与“先前思维链中的陈旧证据复用”之间的竞争，并据此提出隔离先前推理的干预思路。

**不用术语来说**：当图像已经改变时，模型理应重新查看图像、更新依据并修改答案，但它可能直接沿用上一轮文字推理里已经整理好的观察、数值和关系；这样即使最终答案偶尔改对，也不能证明模型真正放弃了旧依据，因此在需要随视觉证据变化而可靠更新的任务中仍可能再次退回旧答案。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出“文本捷径”这一诊断：先前思维链不只是保留最终答案，还把旧图像中的证据及推导组织成可直接复用的文本路径。通过匹配反事实框架中的删除与重排对照，作者主张证据承载内容是跨模型最稳定的先前控制来源，而且捷径强度同时取决于保留的陈旧证据数量及其组织顺序。
- 作者指出答案纠正不足以证明内部证据状态已更新，并由此提出无需训练的 Fresh-State Attention Firewall（FSAF），通过阻止新鲜计算关注先前思维链来保护当前图像上的重计算；其设计不需要目标答案，也不需要证据解析器。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于视觉语言模型（VLM）的视觉自反思与自纠错研究。此类模型不仅要根据图像和问题生成答案，还应在图像证据发生变化后撤销由旧图像支持的判断，并依据当前图像重新推理。已有研究通常把更新失败归因于模型没有充分重新关注图像，或受到对话上下文惯性的影响；本文进一步区分两条可能的计算路径：一是从当前图像重新提取证据，二是直接复用上下文中由旧图像生成的文字推理。后一条路径可能包含观察结果、数值、关系和中间推导，因此即使视觉输入已经改变，仍能像一条现成的“文字捷径”一样影响新答案。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="concept-item" markdown="1">

**视觉语言模型（Vision-Language Model, VLM）**

同时处理图像与文本的模型，可根据图像内容回答自然语言问题并生成解释。本文关心的不是一般静态准确率，而是模型能否在视觉证据变化后相应更新推理和答案。

</div>
<div class="concept-item" markdown="1">

**思维链（Chain of Thought, CoT）**

模型在最终答案之前生成的分步文字推理，其中可能记录从图像读出的对象、数值、空间关系及中间结论。CoT不一定忠实揭示模型内部计算，但保留在上下文中时仍可能因果性地影响后续输出。

</div>
<div class="concept-item" markdown="1">

**匹配反事实分析（matched counterfactual analysis）**

为同一问题构造结构相近但支持不同答案的两幅图像，以控制无关差异并制造明确的证据冲突。通过比较无历史条件与带旧CoT条件下的回答，可以估计旧文字推理相对于当前视觉证据的影响。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

每个样例包含一个问题，以及两幅结构相似但导向不同答案的图像。模型先在反事实旧图像 $I^{-}$ 上生成一段连贯且由模型自身撰写的旧推理 $R^{-}$；随后图像切换为当前图像 $I$，模型需要反思并输出与当前视觉证据一致的答案。研究比较直接基于 $I$ 推理的无历史路径与同时看到 $I$ 和 $R^{-}$ 的历史条件路径，并通过删除、逐步减少或重排旧CoT中的证据性内容，区分三种可能来源：旧证据本身的任务特定控制、一般上下文长度效应，以及旧最终答案造成的锚定。该设定的核心判断标准不是模型是否简单换了答案，而是它是否真正废弃旧图像所支持的证据路径，并从当前图像重新计算。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notation-item" markdown="1">

**$I^{-}$**

反事实旧图像；用于诱导出与当前图像答案冲突但内部连贯的旧推理。

</div>
<div class="notation-item" markdown="1">

**$R^{-}$**

模型依据旧图像生成的先前思维链，其中可能包含已经过时的视觉证据、关系与中间推导。

</div>
<div class="notation-item" markdown="1">

**$I$**

反思阶段提供给模型的当前图像；模型应以其中的现时视觉证据重新作答。

</div>

</div>

**直接相关的工作**

- **VisualSwap（Shi et al., 2026）**: 该工作通过图像交换揭示：VLM即使声称重新检查图像，也可能不随变化后的视觉证据更新。它建立了本文所需的动态证据冲突场景；本文则进一步追问更新失败时模型具体复用了什么，并把旧CoT中的证据性推理识别为与视觉重计算竞争的文字路径。
- **Look Again, Think Slowly（Jian et al., 2025）**: 该工作代表通过鼓励模型重新关注视觉信息来改善视觉反思的方法，主要针对当前图像利用不足。本文补充其问题诊断：仅要求模型“再看一次”不能说明旧推理是否仍可被访问，因此需要考察并限制旧证据性CoT对新计算的持续影响。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

视觉语言模型（VLM）被用于根据图像回答问题，并被期待在视觉证据改变后进行自我检查与修正。可靠修正不能只是把旧答案替换成新答案，而应使旧视觉状态下的证据失效，并依据当前图像重新形成观察与推导。原文指出，模型即使声称重新查看图像，也可能无法完成这种更新；更严重的是，一次输出当前正确答案后，先前答案和旧前提仍可能保留潜在影响，使模型在当前图像支持减弱时重新偏向旧答案。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **自反馈与自我纠正**：让模型检查已有推理或答案，并在后续轮次生成修订结果。该类方法提供了“再次思考”的交互过程，但仅观察答案是否改变，无法判定模型是否真正从当前图像重建了证据。
- **促进重新视觉注意的方法**：针对视觉更新失败，引导模型再次关注或检查当前图像，希望补足反思阶段对新视觉证据的利用。其基本诊断是模型没有充分“再看一次”，代表性上下文包括原文提到的 VisualSwap 所揭示的问题及后续鼓励 renewed visual attention 的方法。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- “视觉注意不足”或“上下文惯性”的解释主要说明模型缺少什么，却没有识别失败时究竟复用了哪一种现成计算路径。因此，已有诊断难以区分三种可能来源：旧思维链中的证据与推导、一般性的长文本上下文，以及旧最终答案本身的锚定效应；无法定位来源，就难以设计有针对性的控制。
- 以答案是否纠正作为自反思成功标准过于宽松。模型可能输出当前答案，同时仍受旧证据路径的分数级牵引；当当前图像的支持被削弱时，这种残余依赖可能使偏好退回先前答案。因此，提示模型“重新看图”或取得一次正确答案，都不能充当旧证据状态已经失效的可靠证明。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未给出对先前思维链影响来源的受控、内容级诊断：需要在图像结构可比但答案不同的条件下，分离“证据承载推理”的作用与文本长度缩短、非证据上下文减少、最终答案锚定等混杂因素；同时还需检验模型改对答案后，这条旧路径是否真正退出计算。该空缺也意味着干预目标尚不明确：究竟应继续增强视觉关注，还是应限制新计算访问陈旧推理。

</div>
<div markdown="1"><span>核心问题</span>

当当前图像已经改变而 VLM 未能重新计算时，它具体复用了先前思维链中的什么；这种复用在答案被纠正后是否仍然存在，以及能否通过隔离先前思维链来减弱其控制？

</div>
<div markdown="1"><span>作者直觉</span>

旧思维链已经把上一张图像中的观察、数值、关系和中间推导整理成一条低成本的文字路径，而从当前图像重新提取证据并组织推理成本更高。模型因此可能选择“读取现成解题过程”，而不是重新看图计算。若有选择地删除旧推理中的证据句，比删除同等长度的普通上下文或仅删除最终答案更能改变模型偏好，就能说明起作用的是证据内容而非单纯长度或答案锚定；若打乱证据顺序也削弱影响，则说明可复用的不只是若干词语，还包括已组织好的推理结构。沿此判断，直接阻断新鲜计算对旧思维链的注意访问，应比仅用提示语要求模型重新检查更能迫使模型依赖当前图像。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

本文的方法由“配对反事实诊断”和“Fresh-State Attention Firewall（FSAF）干预”两部分组成。诊断阶段以同一模型、同一样本为配对单位，在当前图像、问题、候选答案表示、图像预处理和解码设置保持不变的前提下，只改变历史思维链（CoT）中的证据内容、答案片段、上下文或排列方式，再比较自由生成结果以及当前答案 $y$ 相对旧答案 $y^{-}$ 的偏好变化。这样可以把“模型是否沿用旧推理”进一步分解为“旧推理中的哪类文本在承载影响”，而不是仅把错误归因于视觉注意不足。FSAF阶段则在普通反思条件之外建立隔离的新鲜计算过程，通过推理时的注意力控制阻止新计算直接复用旧CoT；随后在统一前缀和统一候选评分规则下比较普通反思、仅重新提问与FSAF。

端到端地看，输入包括当前图像、问题、先前图像条件下产生的旧CoT、当前正确答案 $y$ 和先前答案 $y^{-}$。系统先构造只在指定因素上不同的匹配条件，交给同一VLM生成或进行候选打分；自由生成由一个不看图像的语义裁判分别判断是否匹配 $y$ 与 $y^{-}$，候选打分则用长度归一化的平均对数概率计算偏好差。作者由此测量旧CoT的控制强度，并用FSAF测试隔离旧历史后能否恢复基于当前图像的更新。通俗地说，这套方法像是给模型做受控的“换图复查”：逐段删改旧笔记以找出最容易让模型照抄的部分，再把重新观察得到的计算与旧笔记隔开，检查答案是否真正随新证据改变。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造配对的图像变化与反思输入

以“模型－样本”为配对单位渲染各模型原生聊天模板；匹配条件中的图像位置、图像分辨率、预处理、解码配置和最大生成长度保持一致，只改变实验指定的历史内容或注意力访问方式。

<div class="method-step__io" markdown="1">

**输入**：同一任务样本的当前图像、问题、旧CoT、当前目标答案 $y$ 与先前目标答案 $y^{-}$。<br>
**输出**：一组除目标干预因素外均相同的反思条件，以及完整的模型、数据集、样本ID、条件名、$y$ 和 $y^{-}$ 来源记录。

</div>

**直观理解**：这相当于控制变量实验：同一道题、同一个模型和同一套推理设置下，只动旧笔记中的一个因素，因而输出差异更可能由该因素造成。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 定位旧CoT中的文本捷径载体

比较完整历史与证据删除、答案片段删除、等长非证据删除及证据重排等匹配条件，并观察自由生成语义结果和答案偏好差的配对变化；随机操作使用由样本身份导出的共享种子。

<div class="method-step__io" markdown="1">

**输入**：完整旧CoT及其证据承载片段、非证据上下文和最终答案片段。<br>
**输出**：不同历史成分对当前答案更新的因果诊断，包括证据内容被移除或重排后旧答案控制是否减弱。

</div>

**直观理解**：方法不是笼统地问“旧CoT有没有影响”，而是逐块拆除旧推理，判断真正让模型沿用旧结论的是旧答案本身、文本长度，还是组织成推理链的旧证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行FSAF新鲜状态隔离

FSAF通过Transformers的eager-attention hooks在推理时控制注意力访问，使新鲜计算与先前CoT隔离；它是无需额外训练的推理干预。所给节选未提供注意力掩码的精确定义、层级作用范围或完整阶段划分，因此不能据此进一步还原其内部算法。

<div class="method-step__io" markdown="1">

**输入**：当前图像与问题、先前CoT，以及需要从当前视觉输入重新计算答案的VLM。<br>
**输出**：在降低旧CoT直接复用机会的条件下产生的新反思输出及候选答案分数。

</div>

**直观理解**：可以把FSAF理解为给重新观察设置一道信息防火墙：模型仍可完成当前任务，但新一轮视觉判断不能无约束地从旧推理中复制现成证据。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 统一评估自由生成与候选偏好

自由生成由Qwen3-VL-235B-A22B-Instruct文本裁判独立返回是否匹配新、旧目标；候选偏好则在同一前缀下教师强制两个候选，按候选token平均对数概率计算分数与差值。FSAF比较中的所有条件都追加候选中立脚手架“Final answer:”，并统一候选字符串、分词规则和评分位置。

<div class="method-step__io" markdown="1">

**输入**：各条件下的生成文本，或共享渲染前缀下的规范候选 $y$ 与 $y^{-}$。<br>
**输出**：视觉更新率（VUR）、旧答案率（PAR）、双匹配标记Both，以及当前答案相对旧答案的偏好边际 $m(c)$。

</div>

**直观理解**：生成评估回答“模型最后说了什么”，候选打分回答“即使没有直接生成，模型内部更偏向哪个固定答案”；两种读数相互补充，避免只凭表面措辞判断。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--ready" markdown="1">

**已定位 2 个关键公式**

以下方程保留符号说明、直观解释与原文位置。

</div>

<div class="equation-block" markdown="1">

#### 候选序列的长度归一化平均对数概率

$$
s(a\mid c)=\frac{1}{|a|}\sum_{t=1}^{|a|}\log p(a_t\mid c,a_{<t})
$$

**符号说明**

- $a$：待评分的规范候选答案序列，可以是当前答案或先前答案
- $c$：两个候选共享的已渲染上下文前缀，包括相应实验条件下的图像、问题和可见历史
- $|a|$：候选答案包含的token数量
- $a_t$：候选序列中的第t个token
- $a_{<t}$：候选序列中位于第t个token之前的所有候选token
- $p(a_t\mid c,a_{<t})$：模型在上下文及此前候选token给定时，为第t个候选token赋予的条件概率
- $s(a\mid c)$：候选序列在上下文中的平均token对数概率得分

<div class="equation-explanation" markdown="1">

**直观理解**：该式逐token读取模型给候选答案的概率，取对数后求平均。除以候选长度可减少短答案仅因token较少而获得的机械优势，使新旧候选的比较更公平。<br>
**原文位置**：Appendix A.7, Answer-Preference Scoring Details

</div>

</div>

<div class="equation-block" markdown="1">

#### 当前答案相对先前答案的偏好边际

$$
m(c)=s(y\mid c)-s(y^{-}\mid c)
$$

**符号说明**

- $m(c)$：在上下文c下，模型对当前答案相对先前答案的偏好边际
- $y$：与当前图像证据对应的规范目标答案
- $y^{-}$：与先前状态或先前图像对应的旧目标答案
- $s(y\mid c)$：当前答案在共享上下文下的长度归一化平均对数概率
- $s(y^{-}\mid c)$：先前答案在同一上下文下的长度归一化平均对数概率
- $c$：保持候选评分位置一致的实验条件前缀

<div class="equation-explanation" markdown="1">

**直观理解**：该差值为正表示模型更偏向当前图像对应的答案，为负表示旧答案仍占优势。研究关注同一模型、同一样本在干预前后该边际的变化，因为它比跨模型原始均值更直接地反映删除旧证据或启用FSAF造成的影响。<br>
**原文位置**：Appendix A.7, Answer-Preference Scoring Details

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。FSAF被明确描述为training-free intervention，本文所给方法节选没有参数训练、损失函数或梯度优化过程；其中的平均对数概率与偏好边际仅用于教师强制评估，不是用于更新模型权重的训练目标。语义裁判同样以温度零进行推理并输出严格JSON标签，原文未报告为本研究重新训练该裁判。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 配对反事实操纵模块**

核心估计量是同一模型、同一样本在两个匹配条件间的变化，而非直接比较不同模型的原始平均值。条件操纵覆盖旧CoT证据删除、长度匹配的非证据删除、最终答案片段处理、证据重排，以及普通反思、仅重新提问和FSAF之间的比较。

> 直观理解：不同模型本来就可能有不同的输出风格、校准程度和可评估样本集合；让每个样本与自身对照，可以先消除这些固定差异，再回答“只改变旧历史后发生了什么”。

**2. FSAF注意力隔离模块**

FSAF是training-free推理干预，使用Transformers eager-attention hooks实现对注意力访问的直接控制，目标是隔离从当前输入产生的新鲜计算与先前CoT。当前节选只说明其实现入口位于Appendix F.2，未给出精确掩码公式、缓存处理方式或各token间可见性矩阵。

> 直观理解：普通的“再看一次”仍可能让模型走旧文本捷径；该模块需要在计算通路上限制旧推理可被直接调用，才能检验模型是否真正依据当前图像重算。

**3. 双通道评估模块**

语义通道使用文本裁判独立判定输出是否匹配 $y$ 和 $y^{-}$，因此VUR与PAR不被强制为互补事件，能同时匹配两者的输出记为Both。概率通道在相同上下文 $c$ 下对两个规范候选进行教师强制，用长度归一化平均对数概率和二者差值读取相对偏好。

> 直观理解：独立语义判定可以处理同义表达、等价数值和选项字母，而候选概率能检测生成文本之外的偏向；Both被保留，是因为一段回答可能同时提到或对比新旧答案。

**训练与推理**

整个流程发生在推理与评估阶段。首先，每个检查点都使用自己的processor和原生chat template，Qwen3.5与Qwen3.6统一后训练检查点采用non-thinking模式；标准Qwen2.5-VL/Qwen3-VL推理由vLLM执行，其余模型家族以及需要直接控制渲染前缀或候选logit的探针使用Transformers。每个配对比较固定模型、图像预处理、解码参数和最大生成长度，仅改变指定干预；FSAF与普通反思基线最多生成256个token，并由eager-attention hooks实施隔离。

评估有两条路径。自由生成路径把数据集名称、目标答案或目标对及待评文本交给Qwen3-VL-235B-A22B-Instruct，但不向裁判提供图像；裁判以batch size 1、temperature 0和严格JSON schema分别输出新旧目标匹配结果，无效响应会重试，不会默认记为错误。候选偏好路径在同一渲染前缀下教师强制 $y$ 和 $y^{-}$：若两个目标都有合法选择题字母，就都用字母表示，否则都用答案值，避免字母与长字符串的不对称比较；FSAF、普通反思和仅重新提问条件共享“Final answer:”前缀，若此前存在未闭合的“<think>”块则先闭合。作者还报告二选一归一化读数，但明确指出它只是两个固定候选之间的相对偏好，不是覆盖所有可能答案的校准概率。

**复现信息**

可复现性上最关键的是检查点、后端、配对控制与记录规则。16模型诊断使用Table 8列出的公开检查点，覆盖Qwen2.5-VL、Qwen3-VL、Qwen3.5、Qwen3.6、InternVL2、Gemma 4和Kimi-VL的base、instruct、thinking或non-thinking配置；“Type”仅描述实际评估的检查点或解码模式，不能据模型名称反推训练配方。实验运行于8张NVIDIA B200 180GB GPU的服务器，235B语义裁判使用4卡、tensor parallelism为4；软件环境为CUDA 12.8、PyTorch 2.10.0、vLLM 0.19.0，以及按模型家族配置的Transformers 4.49.0至5.13.0。

每条结果以模型、来源数据集和样本ID为键，干预记录还包含条件名、$y$ 与 $y^{-}$；审计检查预期任务ID、重复项、缺失记录、分数有限性及匹配条件是否完整。随机操纵的种子由样本身份导出，并在相关匹配条件间共享；聚合率从保留的逐行记录重新计算。语义判定允许同义字符串、明确情况下等价的百分数与小数、以及指向同一选项的字母；VUR与PAR独立计算，Both同时计入二者。需要注意，当前节选没有给出FSAF注意力防火墙的完整可见性规则，因而仅凭该节选不足以独立复现其核心hook逻辑，必须回查原文Appendix F.2。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1">

<span class="paper-mini-label">数据与任务</span>

- 核心诊断集为800个人工核验的VS-Bench匹配反事实样本对。每个样本包含当前任务$\mathcal{T}=(I,Q,y)$和反事实任务$\mathcal{T}^{-}=(I^{-},Q,y^{-})$：两者共享问题与答案空间，但任务相关视觉证据不同，且$y^{-}\neq y$。只有被测模型能分别在$I$和$I^{-}$上直接得到正确答案的样本才进入评估，从而将自反思失败与基础解题失败区分开。
- 800对样本等量取自MathVista-MINI、MathVerse-MINI、MathVision和MMMU-Pro，覆盖数学图表、视觉数学推理及多学科视觉问答等任务。这里这些来源集的作用不是分别报告排行榜性能，而是为VS-Bench提供多样化且可构造反事实图像的题目。
- FSAF在5个VLM上评估；所给节选未明确报告其完整样本来源分解，但附录指出普通反思与FSAF评估共涉及1,800个输出。该数字是输出规模而非独立样本数，因此不能据此推断每个模型或条件的样本量。

</div>

<div markdown="1">

<span class="paper-mini-label">指标怎么看</span>

<div class="metric-list" markdown="1">

<div class="metric-item" markdown="1">

**视觉更新率（VUR）**

在$N$个合格样本中，生成结果与当前图像目标$y_i$语义匹配的比例，即$\mathrm{VUR}(S)=N^{-1}\sum_i J(\mathcal{M}(S_i),y_i)$。语义匹配由Qwen3-VL-235B-A22B-Instruct独立判断。 （通常越高越好，因为它表示模型根据当前视觉证据给出新答案；但VUR与PAR由两个独立布尔判断产生，可能同时命中，因而二者不必相加为100%。）

</div>
<div class="metric-item" markdown="1">

**历史答案率（PAR）**

生成结果与反事实历史目标$y_i^{-}$语义匹配的比例，即$\mathrm{PAR}(S)=N^{-1}\sum_i J(\mathcal{M}(S_i),y_i^{-})$，用于测量陈旧答案在当前图像条件下仍被复用的频率。 （越低越好，因为当前图像已经改变，继续输出$y^{-}$通常表明历史思维链仍在控制回答；不过该指标描述可观察输出，不能直接证明模型内部存在某种特定隐藏状态。）

</div>
<div class="metric-item" markdown="1">

**答案偏好边际$m(S)$**

先按候选答案的平均逐词元对数概率计算$\ell(a\mid S)$，再取$m(S)=\ell(y\mid S)-\ell(y^{-}\mid S)$。它在固定候选之间测量模型更偏向当前答案还是历史答案，并能揭示自由生成已经改正后仍残留的旧答案偏好。 （数值越大、尤其由负转正越好，因为正值偏向当前答案$y$，负值偏向历史答案$y^{-}$。它只是两个固定候选间的相对偏好，不是覆盖全部可能答案的校准概率。）

</div>

</div>

</div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 图像是否能够推翻陈旧思维链：Qwen3-VL-8B Thinking在仅给$Q+R^{-}$与给$I+Q+R^{-}$之间的比较。

<div class="result-value" markdown="1">

没有当前图像时，VUR/PAR为0.6%/53.3%；加入当前图像后变为22.6%/7.0%。作者据此主张历史思维链在缺少图像时可以控制反思，而当前图像能显著削弱旧答案，但该模型的视觉更新仍不充分。

</div>

直观上，模型只看到问题和旧推理时，超过一半回答沿用旧答案；重新提供图像后，旧答案率明显下降。这说明视觉输入确有纠偏作用，同时22.6%的VUR也表明“看见当前图像”并不等于可靠地重新计算。该对照证明的是输入条件与行为变化的关联，不能单独确定内部注意力或因果表征机制。

<div class="result-source" markdown="1">

来源：Table 1

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Qwen3-VL-8B (Thinking) | 0.6 / 53.3 | 22.6 / 7.0

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 16个VLM上的证据内容删除与长度匹配非证据删除比较。

<div class="result-value" markdown="1">

跨模型描述性平均显示，删除历史证据相对删除长度匹配的非证据文本，使答案偏好边际提高2.010，VUR提高43.76个百分点，PAR降低62.58个百分点。作者将其解释为历史思维链中的证据承载内容是文本捷径控制的主要载体。

</div>

关键不只是历史里有多少文字，而是历史是否保留了支持旧答案的前提和推导。删除证据后，模型明显更愿意接受当前答案；删除同样长度的普通上下文没有产生相当变化，因此简单的上下文变短解释不足。不过这些是经合格样本筛选后的配对效应，跨模型平均不等于任一部署模型都能获得相同幅度。

<div class="result-source" markdown="1">

来源：Table 2

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Average | +2.069 | +2.010 | +0.074 | +43.76 | -62.58

</div>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 5个VLM上的训练免除干预Fresh-State Attention Firewall（FSAF）与普通反思比较。

<div class="result-value" markdown="1">

作者报告FSAF将平均VUR从35.28%提高到53.61%，即增加18.33个百分点，同时将PAR从39.22%降至3.67%，即减少35.55个百分点。

</div>

FSAF的目的不是再次提示模型“看图”，而是在注意力层面保护当前图像上的新计算，减少其读取陈旧思维链的机会。结果表明隔离历史访问比普通反思更能抑制旧答案复用。不过所给节选没有提供5个模型各自的完整结果、置信区间或显著性检验，因而这里只能确认作者报告的平均行为改善，不能判断最差模型表现或统计不确定性。

<div class="result-source" markdown="1">

来源：Abstract；FSAF详细结果表在所给节选中未提供

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<div class="experiment-evidence" markdown="1">

Across five VLMs, FSAF raises visual update rate from 35.28% to 53.61% and reduces prior-answer rate from 39.22% to 3.67%.

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

- 无历史的当前图像直接推理：模型仅接收$(I,Q)$。它提供当前任务可解时的参照，并用于判断加入陈旧思维链后发生的变化是否来自历史条件，而非题目本身的难度。
- 完整历史思维链条件，即模型接收$(I,Q,R^{-},P_{\mathrm{reflect}})$。其中$R^{-}$是在反事实图像$I^{-}$上生成、能连贯支持旧答案$y^{-}$的推理；它是诊断文本捷径和比较各删除干预的基准。
- 长度匹配的非证据上下文删除控制$C$。它删除与证据片段长度相当、但不承载解题证据的文本，用于排除性能变化只是由提示缩短、上下文位置变化或一般文本缺失造成的可能性。
- 普通反思与仅重新提问条件是FSAF的主要比较对象。三种条件使用相同候选答案、评分位置和候选中性前缀“Final answer:”，因此差异主要对应是否隔离新鲜计算对历史思维链的注意力访问。

**实验想回答的问题**

- 当当前图像与历史思维链所支持的答案冲突时，VLM究竟会依据当前视觉证据重新计算，还是沿用历史思维链中的陈旧答案与推理依据？这种历史影响在移除图像、重新提问和派生计算等条件下是否仍然存在？
- 历史思维链中的哪类内容构成主要文本捷径，以及通过隔离新鲜计算与历史思维链的注意力访问，FSAF能否提高视觉更新并抑制历史答案复用？

**实验实现**

诊断覆盖16个公开VLM检查点，包括Qwen2.5-VL、Qwen3-VL、Qwen3.5、Qwen3.6、InternVL2、Gemma 4和Kimi-VL的不同规模或推理模式。实验先在$I^{-}$上生成$R^{-}$，仅保留模型在$I^{-}$上回答$y^{-}$且在$I$上直接回答$y$的样本；随后固定$I$、$Q$和反思前缀，比较无历史直接推理、完整历史反思以及证据删除等匹配条件。等价重新提问用于测试旧回答路径是否被重新激活，派生计算则测试旧前提能否迁移到新的运算。作者强调主要估计量是同一模型、同一样本内的条件差，而跨模型均值仅作描述性汇总。

标准推理主要使用vLLM，其余模型与需要控制前缀或候选logit的探针使用Transformers；FSAF通过Transformers eager-attention hooks实现。配对比较固定模型、图像预处理、解码配置和最大生成长度，随机操作按样本身份派生共享种子。FSAF与普通反思最多生成256个词元。语义裁判以温度0、批大小1和严格JSON模式运行，不接收图像；无效输出会重试。作者还保留逐样本记录并检查任务ID、重复项、缺失项、有限分数和条件完整性。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 证据片段删除$E$对比长度匹配的非证据上下文删除$C$，以Qwen3-VL-8B Thinking为例。 | 相对$C$，删除证据使偏好边际增加2.832，VUR增加35.39个百分点，PAR降低84.65个百分点。 | 该消融隔离“内容类型”而非“删除长度”：若变化只来自提示缩短，$E$与$C$应较接近；实际差异很大，说明支持旧答案的证据语句是捷径的重要载体。它仍是行为层面的因果干预，不能直接说明每个证据词元在网络内部如何编码。 | Table 2<br><span class="experiment-evidence">Qwen3-VL-8B \| Thinking \| +2.826 \| +2.832 \| +0.237 \| +35.39 \| -84.65</span> |
| 删除历史证据$E$与仅删除历史最终答案$A$的效果比较，使用Table 2的跨模型平均。 | 证据删除相对完整历史的平均偏好变化为2.069，而最终答案删除相对完整历史仅为0.074；前者约为后者的28倍。 | 该消融检验模型是否只是机械复制最终答案字符串。仅移除答案本身几乎不能消除历史影响，而移除支持答案的证据能大幅改变偏好，说明模型更可能沿用整条陈旧依据，而非只复述结论。倍数是根据表中均值计算的分析性描述，不是作者另行报告的统计量，也不表示所有模型都有相同比例。 | Table 2<br><span class="experiment-evidence">Average \| +2.069 \| +2.010 \| +0.074 \| +43.76 \| -62.58</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：分析 VLM 自我反思中旧文本推理对视觉重计算的捷径效应，并通过注意力隔离提高视觉证据更新能力。; rule check: matched taxonomy keywords; top rule score=5.0
- 全文指纹：`db49fda0b4ba14d5086fa456348eb2b8188cf8ce8ac757ad14fc8c1b77062840`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
