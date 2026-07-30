---
title: "[论文解读] Recover, Decode, Reguard: Guard-Agnostic Defense Amplification againstEncoded VLM Jailbreaks"
description: "[arXiv 2607.26574][LLM 安全] 本文研究如何在不修改现有安全分类器和目标视觉语言模型的前提下，先恢复并解码被改写或跨模态隐藏的恶意请求，再交由安全分类器审查，同时揭示这类防御难以兼顾安全性与正常请求可用性的经验上限。"
arxiv_id: "2607.26574"
announcement_date: "2026-07-30"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:04.128433+00:00"
source_sha256: "9db7c2d7d5d6afdc7089102bb145b3b114e79a317ec59844930b5297973195cc"
tags:
  - "LLM 安全"
  - "多模态 VLM"
  - "视觉—语言模型安全"
  - "编码越狱"
  - "黑盒安全分类器"
  - "解码缺口"
  - "表示迁移攻击"
  - "恢复与解码"
  - "攻击集成"
  - "安全—可用性权衡"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2607.26574</p>

# Recover, Decode, Reguard: Guard-Agnostic Defense Amplification againstEncoded VLM Jailbreaks

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Haoyu Zhang, Zhuoxi Wang, Shibo Zheng, Zijian Xiao, Xiangchen Guan, Mohammad Zandsalimy, Shanu Sushmita</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26574v1) · [PDF 下载](https://arxiv.org/pdf/2607.26574v1) · **关键词** 视觉—语言模型安全, 编码越狱, 黑盒安全分类器, 解码缺口, 表示迁移攻击, 恢复与解码, 攻击集成, 安全—可用性权衡  


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

本文研究如何在不修改现有安全分类器和目标视觉语言模型的前提下，先恢复并解码被改写或跨模态隐藏的恶意请求，再交由安全分类器审查，同时揭示这类防御难以兼顾安全性与正常请求可用性的经验上限。

**不用术语来说**：现有安全分类器通常能拦截直白的有害请求，却可能被“换一种写法”绕过：攻击者可把同一意图写成集合论、形式逻辑、替换密码、程序代码或图片中的文字。分类器看到的是陌生外壳，而不是解码后的真实含义，因此会放行本应阻止的请求。部署方需要一种无需训练或改造既有系统、又能识别这些变形请求的通用前置防御。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出无需训练、无需访问安全分类器内部参数的 recover-and-decode amplifier：利用目标视觉语言模型恢复图像文字并把编码请求改写为明文载荷，再让任意现成分类器审查；同时加入可选的 reguard 层，对解码前的恢复文本也进行检查。
- 采用覆盖十一种攻击的 best-of-suite 集成评估，并在五个安全分类器、两个目标视觉语言模型上刻画经验性的安全—效用上限：恢复与解码只能部分缩小漏洞，而进一步拦截残余攻击通常会造成严重的正常请求过度拒绝。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

视觉—语言模型（VLM）同时处理文本与图像请求，部署时常在模型前接入独立的黑盒安全分类器（guard），先判断输入是否有害，再决定放行或拦截。这类分类器无需修改目标VLM，但主要依据收到的表面表达作判断：攻击者可保持有害语义不变，仅将请求改写为集合论、形式逻辑、替换密码、代码、稀有或古典语言，或把文字渲染到图像及网格中，从而形成“解码缺口”。本文只研究仍含可辨认载荷的表示迁移攻击，不涵盖仅在像素或模型嵌入空间隐藏信息、无法从可读表面恢复请求的攻击。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**黑盒安全分类器（guard）**

位于用户输入与目标VLM之间的独立安全判别器，通常只输出允许或拒绝，而不要求访问或修改目标模型内部参数。其模型无关性便于部署，但若不能理解输入所用的编码形式，就可能漏掉语义上有害的请求。

</div>
<div class="conceptitem" markdown="1">

**解码缺口（decode gap）**

同一有害意图以明文出现时会被拦截，换成代码、符号系统、密码或图像文字后却能绕过分类器，这种表面形式识别与真实语义识别之间的差距即为解码缺口。问题并非载荷消失，而是guard看到的表示不适合直接判断。

</div>
<div class="conceptitem" markdown="1">

**攻击集成与best-of-suite评估**

对同一有害行为尝试多种攻击，只要其中任意一种成功，就把该行为计为被攻破；这近似部署中攻击者会选择最有效手段的最坏情形。它不同于对各攻击成功率取平均，后者可能掩盖不同攻击分别攻破不同样本的风险。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

输入是一条面向VLM的请求，可能包含文本、图像，或二者组合；其中有害语义可能被编码、改写或跨模态渲染。系统由可直接调用但不依赖其内部状态的目标VLM、一个现成黑盒guard，以及置于guard之前的无训练恢复与解码预处理器组成；预处理器需要把图像中的内容恢复成文本，并将编码表达还原为明文语义，随后由guard筛查真实载荷。评估既考察十一种攻击构成的攻击集成能否诱导目标VLM产生有害行为，也考察对正常请求的过度拒绝，以刻画安全性与可用性的权衡。基本假设是攻击表面仍留有可辨认、可恢复的载荷；因此所得结论针对非迭代、恢复式黑盒防御，而不能直接推广到隐藏状态编辑、像素级扰动或嵌入空间攻击。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$\mathrm{ASR}$**

攻击成功率（attack-success rate），表示有害行为成功绕过防御并使目标模型产生攻击者所求结果的比例。

</div>
<div class="notationitem" markdown="1">

**$\mathrm{ASR}_{\mathrm{ens}}$**

攻击集成的best-of-suite成功率：对每个行为，只要攻击集合中至少一种攻击成功，就将其记为被攻破。

</div>
<div class="notationitem" markdown="1">

**$\mathrm{ORR}$**

良性过度拒绝率，可用于表示正常、无害请求被防御系统错误拦截的比例；原文节选使用“benign over-refusal”概念，但未明确给出该缩写。

</div>

</div>

**直接相关的工作**

- **ECSO（Gou et al., 2024）**: 与本文最接近的transform-then-guard基线：它先把图像内容转换为文本，以重新启用文本侧安全判断；但其变换仅是图像到描述的单步caption，没有文本分支，也不会逆转符号、密码或代码编码。本文的恢复—解码方案则面向文本与图像两条通道，目标是输出任何现成guard均可筛查的明文载荷。
- **AutoAttack式集成评估（Croce and Hein, 2020）**: 本文借用其对多种攻击进行最坏情形汇总的评估思想：不以逐攻击平均值代表防御强度，而是对每个行为检查攻击集合中是否有任一攻击成功。该关系主要是评估方法上的继承，并非采用AutoAttack本身的图像扰动算法。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

托管视觉语言模型常把黑盒安全分类器作为第一道防线，因为它可以独立于目标模型部署；但真实攻击者能够在不改变有害意图的情况下改变请求的表示形式。集合论、逻辑表达式、代码、稀有语言或图像文字等表示转换会造成作者所称的“解码鸿沟”：安全分类器依据输入表面形式判断，因而可能放过语义上有害但外观陌生的请求，使现有前置防线无法可靠覆盖编码型和跨模态越狱。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **黑盒安全分类器（guard）**：WildGuard、Llama Guard 或推理型 guard 等现成分类器在请求进入目标视觉语言模型前判断其是否有害，并阻断被判为不安全的输入；该方案不要求修改目标模型，因而适合托管系统。
- **按单种攻击分别评估的越狱防御**：常见评估针对每种编码攻击分别计算成功率，再汇总为逐攻击平均值，以衡量某项防御在典型攻击上的平均表现；这种口径没有把攻击者可从多种攻击中择优尝试的能力计入最终风险。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- guard 主要识别输入中直接可见的危险线索，而不会稳定地恢复图像内容或解码替代表示；结果是同一有害请求以明文出现时会被拦截，换成代码、逻辑、密码或图像载荷后却可能通过。
- 逐攻击平均成功率会掩盖不同攻击在不同有害行为上的互补性。作者报告 best-of-suite 攻击成功率约为通常逐攻击均值的 3.5 倍，因此仅看平均结果可能高估防御在实际攻击者可择优尝试时的稳健性。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究尚未充分回答：一个与具体 guard 解耦、无需额外训练的恢复—解码前处理器，能否在多种表示转换攻击共同构成的最坏情形下真正提升黑盒视觉语言模型防御；若再检查解码前的中间表示，所获得的额外安全收益是否会以不可接受的正常请求过度拒绝为代价。尤其缺少跨多个 guard 和目标模型、同时观察集成攻击成功率与良性可用性的系统刻画。

</div>
<div markdown="1"><span>核心问题</span>

在攻击者可从十一种编码与跨模态越狱中选择任一成功方案的威胁模型下，recover-and-decode amplifier 及其 reguard 扩展能否跨不同 guard 和目标视觉语言模型，把集成攻击成功率降至可部署水平，同时维持较低的良性过度拒绝率？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是先把“表达方式不同但含义相同”的请求归一化：图像中的文字先被恢复成文本，编码内容再被解释成普通语言，使 guard 能在自己更熟悉的明文空间中识别真实意图。若解码会丢失代码形态等原本可供判断的危险信号，就再对解码前的恢复文本执行一次 guard；这相当于同时检查请求的原始恢复视图与语义明文视图。不过，增加检查视图也更容易把正常内容误判为有害，因此该思路天然需要检验安全收益与过度拒绝之间的权衡。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

该方法把安全防护建模为“恢复（recover）→解码（decode）→守卫分类（guard）→可选再守卫（reguard）”的模块化推理流程。输入请求为 x=(t,v)，其中 t 是文本通道、v 是图像通道；目标视觉语言模型 M 先把图像转写为文本 ρ，再将原文本与转写结果合并为 r，并把其中的编码、形式逻辑、代码或跨模态表达还原为明文语义 d。安全分类器 G 检查 d；启用 reguard 时还检查解码前的 r，只要任一视图被判为有害就返回固定拒绝，否则目标模型才对原始输入 x 作答。
直观上，普通 guard 往往只看“请求表面写成什么”，而不是“实际在要求什么”。该方法相当于先让 VLM 做转录和翻译，把藏在图片或特殊编码中的请求改写成易于审查的普通语言；但最终回答仍基于原始输入，以免预处理改写损害正常任务信息。它在接口上与 guard 无关，不访问分类器内部，也不需要重新训练；不过效果仍取决于目标 VLM 能否正确恢复、解码，以及具体 guard 能否识别恢复后的有害内容。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 1. 图像内容恢复

当 v≠∅ 时，使用目标 VLM M 的固定 recover 指令生成图像转写 ρ=M.recover(v)；纯文本请求不调用该步骤，并令 ρ=∅。

<div class="method-step__io" markdown="1">

**输入**：请求 x=(t,v) 中的图像通道 v；若请求仅含文本，则 v 为空。  
**输出**：图像内容的文本转写 ρ，或纯文本场景下的空结果。

</div>

**直观理解**：这一步类似 OCR 与视觉理解的组合：先把图片里可读但原本无法直接交给文本 guard 的内容搬到文本通道。它不仅处理普通文字截图，也试图重新拼合分散在图像区域中的文字信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 2. 构造恢复后的统一文本视图

通过连接算子 ⊕ 构造 r=t⊕ρ；文本、图像任一通道缺失时，r 就由现有通道的文本内容构成。

<div class="method-step__io" markdown="1">

**输入**：原始文本通道 t 与图像转写 ρ。  
**输出**：解码前的统一文本表示 r。

</div>

**直观理解**：r 是系统对请求内容的“文字汇总”：纯文本攻击保留原编码文本，纯图像攻击获得转写，多模态攻击则把两部分放在一起。这个中间视图也为可选 reguard 提供额外审查对象。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 3. 编码语义解码与首次审查

M 使用固定 decode 指令把 r 改写为明文负载 d=M.decode(r)，随后 G(d) 判断其是否有害；若被标记，则立即返回固定拒绝回复。

<div class="method-step__io" markdown="1">

**输入**：统一文本表示 r、目标 VLM M 与安全分类器 G。  
**输出**：通过审查的明文语义 d，或固定拒绝回复。

</div>

**直观理解**：这一步不只是识别字符，而是把集合论、形式逻辑、罕见语言或代码等表面形式重新说成其实际请求。这样 guard 审查的是攻击意图，而不只是攻击者选择的包装方式。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 4. 可选再守卫与原输入作答

若启用 reguard，则额外计算 G(r)，并在 G(r) 或 G(d) 任一为 harmful 时拒绝；两次检查均通过后，调用 M(x) 对原始请求而非 d 作答。

<div class="method-step__io" markdown="1">

**输入**：解码前表示 r、首次审查结果、reguard 开关，以及原始请求 x。  
**输出**：固定拒绝回复，或目标 VLM 对原始输入生成的最终回答。

</div>

**直观理解**：解码有时会删掉 guard 依赖的危险线索，例如把可执行代码改写成 prose 后丢失代码语法，因此再检查 r 可以保留解码前证据。通过审查后仍让模型读取原请求，是为了把安全判断与实际任务回答分开。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="equation-block" markdown="1">

#### 恢复、合并与解码

$$
\rho=\begin{cases}M.\mathrm{recover}(v),&v\neq\emptyset\\ \emptyset,&v=\emptyset\end{cases},\qquad r=t\oplus\rho,\qquad d=M.\mathrm{decode}(r)
$$

**符号说明**

- $x=(t,v)$：原始请求；t 为文本通道，v 为图像通道，任一通道都可以缺失。
- $M$：目标视觉语言模型，既执行恢复与解码，也在安全检查通过后生成最终回答。
- $\rho$：目标 VLM 从图像中恢复出的文本转写；无图像时为空。
- $\oplus$：文本连接或联合操作，用于合并原始文本与图像转写。
- $r$：解码前的统一文本视图，也是可选 reguard 的检查对象。
- $d$：将编码请求还原后得到的普通语言负载。

<div class="equation-explanation" markdown="1">

**直观理解**：这组关系描述预处理主链路：有图像就先转写，再把所有文本证据汇总，最后把特殊编码改述成直接语义。其核心目的不是生成回答，而是构造更适合安全分类器判断的输入视图。  
**原文位置**：第4节 Method，Algorithm 1，第1—3行

</div>

</div>

<div class="equation-block" markdown="1">

#### 双视图拒绝与原输入作答规则

$$
F(x)=\begin{cases}\mathrm{canned\ refusal},&G(d)=\textsc{harmful}\ \lor\ (\mathrm{reguard}\land G(r)=\textsc{harmful})\\ M(x),&\text{otherwise}\end{cases}
$$

**符号说明**

- $F(x)$：完整防御管线对请求 x 返回的最终结果。
- $G$：现成安全分类器（guard），把文本视图判断为 harmful 或非 harmful。
- $G(d)$：对解码后明文负载 d 的基础安全检查。
- $\mathrm{reguard}$：是否启用额外审查解码前文本 r 的布尔开关。
- $\lor$：逻辑或；任一有效检查判为有害即拒绝。
- $\land$：逻辑与；只有启用 reguard 时才采用 G(r) 的结果。
- $M(x)$：在所有已启用的安全检查通过后，目标 VLM 对原始请求 x 的回答。

<div class="equation-explanation" markdown="1">

**直观理解**：判定规则采用保守的双视图策略：解码结果暴露真实意图，解码前文本保留可能被改写删除的形式信号。值得注意的是，d 只用于安全判断，最终生成仍读取 x，因此系统不会把自动改写文本当成用户原始任务直接执行。  
**原文位置**：第4节 Method，Algorithm 1，第4—10行；Figure 1

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。该方法不是通过损失函数优化的新模型，而是由目标 VLM、固定 recover/decode 指令和现成安全分类器组成的推理时预处理与路由管线；原文明确说明它“不需要 guard internals and no training”。因此其性能来自现有 VLM 的转写与语义改写能力、guard 的分类能力，以及是否启用 reguard，而非额外参数训练。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. Recover 图像恢复模块**

该模块复用目标 VLM M，通过一条固定指令将图像 v 转写为文本 ρ；文本-only 输入跳过调用。对 image-only 请求，ρ 是 guard-alone 基线原本看不到的新文本视图；对 multimodal 请求，ρ 会与原文本连接。

> 直观理解：文本安全分类器不能直接可靠理解图片中的请求，因此必须先把视觉内容“念出来”。对于分散网格等攻击，转写还可能把散落字符重新组合，从而暴露完整语义。

**2. Decode 语义还原模块**

该模块同样复用目标 VLM，以固定 decode 指令将 r 中可能存在的编码或特殊表示改述为普通语言负载 d。它不修改 guard，也不针对某一分类器训练，因此在接口层面可接入任意接受文本的现成 guard。

> 直观理解：它充当安全检查前的“翻译器”，把同一个有害意图从难识别的包装转换为 guard 更熟悉的表达。风险在于翻译可能不完整，或反而抹去代码语法等分类信号。

**3. Guard 与可选 Reguard 判定模块**

基础流程检查解码结果 G(d)；reguard 进一步检查 G(r)，并采用逻辑 OR 决策，即任一视图被标为 harmful 都拒绝。r 的组成随输入通道变化：text-only 时 r=t，image-only 时 r=ρ，multimodal 时 r=t⊕ρ。

> 直观理解：这相当于同时检查“翻译后的意思”和“翻译前保存的文字证据”。它能修复因解码丢失信号造成的漏检，但若 guard 在原始和解码视图上都不认识某类危险表达，再检查一次也无法根治。

**训练与推理**

训练阶段：无新增训练，也不微调目标 VLM 或 guard。推理阶段：接收 x=(t,v)；若存在图像则调用 M.recover(v) 得到 ρ；拼接 t 与 ρ 得到 r；调用 M.decode(r) 得到 d；先以 G(d) 审查明文语义，若有害则拒绝。启用 reguard 时再以 G(r) 审查解码前文本，只要任一检查失败即拒绝；否则调用 M(x)，让目标模型依据原始文本与图像生成答案。该次序意味着 recover 和 decode 都发生在最终回答之前，但 guard 不直接控制或修改这两个模块的内部行为。

**复现信息**

复现该方法所需的关键设定是：recover 与 decode 均由目标 VLM执行，且各使用一条固定指令；逐字提示词位于附录 H，但当前节选未提供其内容。图像缺失时不得进行 recover 调用；r 必须按 t⊕ρ 构造。基础版本只审查 d，可选 reguard 版本同时审查 r 与 d，并在任一视图被标记时返回 canned refusal；通过后必须对原始 x 而不是解码文本 d 作答。模型型号、生成参数、分类阈值及固定拒绝文本的具体措辞在所给方法节选中原文未明确报告。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- HarmBench：取100个有害行为作为安全测试集；每个行为分别实例化为11种攻击表示，共11×100个成功生成的编码样本。它用于测量目标VLM是否实际完成有害任务，而不只是识别输入是否含有恶意意图。
- OR-Bench-Hard：取100个良性请求测量过度拒绝，并包含文本与图像变体。其作用是检验防御在增强安全性的同时是否错误阻断正常请求；无防御时文本和图像拒绝率分别为38%和15%，平均良性拒绝基线为26%。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**Ensemble ASR（best-of-11攻击成功率）**

对每个有害行为，只要11种攻击中任意一种使目标完成有害任务，就将该行为计为攻破；形式为 \mathrm{ASR}_{\mathrm{ens}}=\frac{1}{|B|}\sum_{b\in B}\max_{a\in\mathcal{A}}s_a(b)，其中B是行为集合，\mathcal{A}是攻击集合，s_a(b)表示攻击a是否攻破行为b。这模拟攻击者按行为选择最有效编码，而非随机使用某一种攻击。 （越低越好，因为它衡量固定攻击菜单下防御留下的联合攻击面；增加攻击种类只可能提高该指标，因此当前结果仍是攻击成功率的下界。）

</div>
<div class="metricitem" markdown="1">

**Per-attack mean ASR**

先分别计算每种攻击的成功率，再对11种攻击取平均。它用于观察单类攻击是否被压低，但不同攻击可能攻破不同的行为，因此不能代表部署中的最佳攻击者。 （越低越好；但论文发现它比ensemble ASR约低3.5倍，所以仅凭该指标容易高估防御效果。）

</div>
<div class="metricitem" markdown="1">

**Benign over-refusal（良性过度拒绝率）**

在OR-Bench-Hard良性输入上，被系统错误拒绝的比例，并对文本与图像通道取平均。它衡量安全增强造成的可用性损失。 （越低越好，因为正常请求应被回答；论文同时报告ASR与过度拒绝，以判断安全提升是否只是通过更激进地拒绝所有内容获得。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 无防御与最佳单一守卫：两个目标VLM上的best-of-11联合攻击

<div class="result-value" markdown="1">

无防御时，ensemble ASR在Qwen2.5-VL和InternVL3上分别为89%和91%；即使选用各目标上表现最好的单一守卫，仍分别有71%和81%的行为可被至少一种攻击攻破。相应的逐攻击平均值仅为18%–21%，明显掩盖了攻击之间的互补性。

</div>

单一守卫可能挡住某一种编码，却无法同时覆盖符号改写、罕见语言、代码包装和图像渲染。这里证明的是固定11种攻击集合内的联合脆弱性，而不是对所有可能攻击的完整鲁棒性；由于扩展攻击集合只会使OR联合成功率不降，未覆盖的攻击族更可能令防御结果变差。

<div class="result-source" markdown="1">

来源：第5节，RQ1: no single guard closes the gap；附录D表4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Undefended, the eleven-attack ensemble breaks 89% (Qwen) / 91% (InternVL3) of behaviors; against the best single guard it still breaks 71% (Qwen) / 81% (InternVL3) (Appendix D).</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### guard + recover-and-decode amplifier：五种守卫、两个目标VLM

<div class="result-value" markdown="1">

最优“守卫+放大器”配置的ensemble ASR仍为Qwen上的65%和InternVL3上的63%。放大器虽能把多数符号、罕见语言和图像渲染攻击的单项ASR压到个位数，但其相对guard-alone的ensemble改善只在10个守卫—目标组合中的4个达到显著，因此不能声称该接口对所有守卫都稳定有效。

</div>

恢复和解码确实让守卫读懂了许多原本不可见的表示，但best-of-suite指标要求同一行为的所有可选攻击都失败；只要CodeAttack或分散网格等少数互补攻击仍成功，该行为就仍被计为攻破。因此，“多数单项攻击下降”不等于“整体防线可靠”，而且不同守卫对恢复文本的判定习惯不同。

<div class="result-source" markdown="1">

来源：第5节，RQ2: the amplifier is a partial defense；附录D表4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">At the ensemble level the benefit is only partial: the strongest guard-plus-amplifier still leaves 65% (Qwen) / 63% (InternVL3) (Appendix D, middle bars).</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### amplifier + reguard的安全—效用权衡

<div class="result-value" markdown="1">

reguard使两个目标上的所有10个守卫—目标组合的ensemble ASR下降，Qwen上的LlamaGuard-3由79%降至48%，且10组中9组达到显著；但四个较严格、校准较好的守卫出现严重效用损失，过度拒绝达到Qwen上的81%–87%或InternVL3上的86%–92%。较宽松的LlamaGuard-3在Qwen上仅从28%升至33%过度拒绝，但仍留下48% ASR。

</div>

reguard是安全改善最一致的模块，因为它保留了解码前可能被改写抹去的结构信号；然而，额外检查也会把大量良性恢复内容判为危险。实验因此支持的是所研究管线和表示迁移攻击范围内的经验性Pareto前沿：现有配置只能在更安全与更可用之间移动，没有一个配置同时达到低ASR和低过度拒绝。它不是对所有未来防御方法均存在理论上限的证明。

<div class="result-source" markdown="1">

来源：第5节，RQ4: the reguard layer and the safety–utility ceiling；图2；表1；附录D表4–5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">For the four well-calibrated guards the gain is bought at a steep utility cost: benign over-refusal rises to 81–87% (Qwen, three guards) / 86–92% (InternVL3, the three guards measured on its benign axis), with ThinkGuard likewise paying 45→66% (Figure 2).</span>

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

- 无防御目标模型：直接测试Qwen2.5-VL-7B与架构不同的InternVL3-8B，给出编码攻击在没有输入过滤时的成功率上限，并检验结论是否跨VLM架构复现。
- guard alone（gb）：仅使用现成安全守卫过滤原始输入，是判断放大器是否提供增量收益的核心基线。五个守卫为WildGuard、LlamaGuard-3-8B、Qwen3Guard-8B、ThinkGuard和多模态GuardReasoner-VL-7B；前四者只查看文本，因此面对仅在图像中承载有害内容的攻击时存在结构性盲区。
- guard + amplifier（mc）：先恢复图像文字并将编码内容解码、改写为明文，再交给同一守卫。与gb比较可测试统一的恢复—解码前处理是否让不同黑盒守卫看见原始有害语义。
- amplifier + reguard（+rg）：除检查解码后的内容外，再检查解码前的恢复表示，用于捕获可能被自然语言改写削弱的代码结构，以及未被完整重组的分散式图像载荷。它与mc的比较衡量二次守卫带来的安全增益和效用代价。

**实验想回答的问题**

- 在攻击者可针对每个有害行为从11种编码攻击中选择最有效攻击时，单一安全守卫以及“恢复—解码”放大器能否稳定降低跨攻击联合成功率，并在不同守卫和目标VLM上泛化？
- 加入reguard、调整判定阈值或扩大解码模型后，能否同时实现低攻击成功率与低良性过度拒绝，还是这些恢复式防御存在经验性的安全—效用上限？

**实验实现**

主要目标为Qwen2.5-VL-7B，InternVL3-8B用于跨架构泛化。攻击套件含5种文本编码——集合论、形式逻辑、古典语言、Base64/Caesar替换密码和CodeAttack——以及6种图像表示——FigStep、流程图、低对比度、遮挡文字、mm-typo和分散式编号网格。所有11×100个攻击实例均成功生成。输出由gpt-5-mini按HarmBench任务完成准则评分；作者分别以100个人工盲标样本校准有害性判断和良性“回答/拒绝”判断，Cohen's κ为0.68和0.79。作者还以gpt-5-nano复评全部449个“攻击×守卫×条件”单元，单元ASR相关系数为0.975。ensemble ASR报告Wilson 95%置信区间和10^4次行为级bootstrap区间；同一批100个行为上的条件比较采用精确McNemar检验，并对20个ensemble比较采用Bonferroni阈值0.05/20。WildGuard只作为输入守卫，不作为结果裁判，因为作者发现它容易把恶意意图误判为任务已完成。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 组件消融：recover-only与recover+decode，在全部11种攻击和两个目标上比较 | 在Qwen上，加入decode后集合论攻击ASR由12%降至1%，形式逻辑由14%降至4%，但CodeAttack由43%升至50%，distraction由5%升至31%。最终ensemble ASR在Qwen上为72%对61%，p=0.09；在InternVL3上为63%对65%，p=0.84，均无显著差异且方向相反。与此同时，decode把过度拒绝从76%降至57%。 | 该消融隔离了解码步骤，而恢复步骤保持不变。结果表明decode能翻译符号表示并改善良性可用性，但也可能删除代码攻击赖以被守卫识别的语法信号，或错误处理分散网格；正负效应在联合指标上抵消。因此论文没有把decode解释为显著提升ensemble安全性的组件，而是把它主要定位为保持可用性的组件。 | 第5节，What decode is, and is not, worth；表2<br><span class="experiment-evidence">At the ensemble level these cancel to no significant effect on either target — 72 vs 61 on Qwen (p=0.09) and 63 vs 65 on InternVL3 (p=0.84), the two pointing opposite ways — so we do not claim an ensemble-level safety benefit for decode.</span> |
| 守卫判定阈值全范围扫描：过度拒绝预算≤35%及放宽至≤60% | 在≤35%过度拒绝预算下，5个守卫中4个没有可用的内部阈值，唯一满足预算的选择相当于完全不拦截，ASR退回无防御水平；LlamaGuard-3虽可重新校准，但仍允许58%的攻击套件成功。即使把预算放宽至≤60%，五个守卫可达到的最低ensemble ASR仍为58%。 | 该实验区分“默认阈值选得不好”与“模型分数本身无法分开良性和攻击输入”。若只是校准问题，扫描阈值应出现同时改善两轴的工作点；结果却显示多数守卫只能沿安全—效用曲线移动。因此观察到的上限不能仅归因于论文选择了一个不合适的默认阈值，但结论仍限于这五个守卫、当前数据和攻击套件。 | 第5节，Is the ceiling just bad thresholds?；附录4（原文如此标注）<br><span class="experiment-evidence">Nor does this depend on the budget: relaxing it to ≤60% still leaves 58% as the lowest ensemble ASR any of the five can reach.</span> |

**定性案例**

- 残余攻击机制显示两类互补失败。CodeAttack把有害请求包装为代码补全任务，解码为自然语言后反而可能移除守卫可利用的代码语法信号；distraction把载荷分散在编号网格中，恢复器虽能读取局部文本，却未必按正确顺序重组完整请求。reguard检查解码前表示，因而能修复分散网格并削弱CodeAttack，但同时会把更多良性恢复内容暴露给守卫，解释了安全提升与过度拒绝同步上升。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：核心贡献是针对编码及跨模态VLM越狱攻击的防御放大器与安全—效用权衡评估。; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`9db7c2d7d5d6afdc7089102bb145b3b114e79a317ec59844930b5297973195cc`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
