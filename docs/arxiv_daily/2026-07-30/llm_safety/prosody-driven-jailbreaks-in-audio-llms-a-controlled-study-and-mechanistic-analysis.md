---
title: "[论文解读] Prosody-driven Jailbreaks in Audio LLMs: A Controlled Study and Mechanistic Analysis"
description: "[arXiv 2607.26541][LLM 安全] 本文通过固定有害请求的文字内容、仅改变语音表达方式，研究音频大模型的越狱风险能在多大程度上由韵律及相关声学属性触发。"
arxiv_id: "2607.26541"
announcement_date: "2026-07-30"
primary_category: "llm_safety"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:04.094448+00:00"
source_sha256: "0f4f01eb0b23cd9adbfdb85b37154a025f331db00a7d048744c999973d0e7cc1"
tags:
  - "LLM 安全"
  - "音频大语言模型"
  - "音频越狱"
  - "语音韵律"
  - "匹配文本"
  - "副语言信息"
  - "黑盒安全评测"
  - "PJ-Break"
  - "AdvAudio-Prosody"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 安全 · arXiv 2607.26541</p>

# Prosody-driven Jailbreaks in Audio LLMs: A Controlled Study and Mechanistic Analysis

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Jiachen Qian, Junyu Li</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26541v1) · [PDF 下载](https://arxiv.org/pdf/2607.26541v1) · **关键词** 音频大语言模型, 音频越狱, 语音韵律, 匹配文本, 副语言信息, 黑盒安全评测, PJ-Break, AdvAudio-Prosody  


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

本文通过固定有害请求的文字内容、仅改变语音表达方式，研究音频大模型的越狱风险能在多大程度上由韵律及相关声学属性触发。

**不用术语来说**：同一句话即使一个字不改，用惊慌、愤怒、命令式或快速的方式说出来，也可能让音频大模型作出不同的安全判断。现实中的音频助手直接处理语音，其中不仅有文字内容，还有音高、响度、语速和音质等信息；如果安全评测只测试文字改写或中性朗读，就可能漏掉由“怎么说”造成的风险。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出受控的韵律越狱研究设置与 PJ-Break 黑盒评测协议：保持转录文本不变，按预先规定的语音表达条件改变输入，从而把研究重点从词汇改写收窄到语音表达本身，并明确指出 Commanding 条件存在说话人变化这一混杂因素。
- 构建含 600 个样本、声学属性经过核验的 AdvAudio-Prosody 基准，覆盖唤醒度、权威感和语速等表达维度；同时用单条件查询、固定六查询覆盖率、同声线敏感性分析及“情绪语音对比情绪文字”消融来检验表达方式是否构成独立且重要的安全变量。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文研究原生音频大语言模型（Audio LLM）的安全性。与先将语音转写为文本、再交给语言模型的级联系统不同，原生 Audio LLM 能更直接地利用语音信号中的副语言信息；因此，即使文字内容完全相同，音高、响度、语速和音质等表达差异也可能改变模型的推理与回答。本文将这种“文本不变、说法改变”的语音韵律视为独立的潜在越狱通道，重点考察预设的唤醒度、权威感、语速及音质变化能否诱导模型产生经核验的不安全服从回答。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**音频大语言模型（Audio LLM）**

能够直接接收语音或其他音频并生成回答的基础模型。它不仅可能理解转写出的词语，还可能利用说话人的情绪、语速和音质等非文字线索。

</div>
<div class="conceptitem" markdown="1">

**韵律与副语言信息**

韵律指音高、响度、节奏和时长等协同变化；副语言信息还包括音质、情绪和交际意图等不由字面文本直接表达的信号。本文的“speech-delivery preset”可能同时改变多个声学属性，因而不是对单一声学变量的严格操控。

</div>
<div class="conceptitem" markdown="1">

**音频越狱**

攻击者通过音频输入诱使模型绕过安全约束并提供有害内容。本文以是否出现“经核验的不安全服从”为成功标准；未成功不等同于模型明确拒绝，也可能是安全引导、无关回答或未达到有害内容判据。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

给定一条固定的有害文本指令，PJ-Break 使用文本转语音系统将同一文本渲染为六种预先规定的表达条件：Panic、Anger、Commanding、Fast、Neutral 和 Whisper，分别主要针对唤醒度、权威感、时间节奏、基准表达或音质。所得音频被输入黑盒 Audio LLM，系统输出自然语言回答，再依据经核验的不安全服从标准判定攻击是否成功。核心假设是所有条件保持词汇内容一致，从而把观察重点收窄到语音表达差异；但作者明确承认，每个预设内部的多个声学属性可能共同变化，且 Commanding 使用不同说话人，存在声音身份混杂。单条件设置以固定一次查询衡量某个预设的效果，六条件池则以固定六次查询预算衡量这些表达方式对不同有害种子的联合覆盖能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

<div class="notation-list" markdown="1">

<div class="notationitem" markdown="1">

**$Q$**

针对每个有害指令种子所允许的查询次数，即固定攻击预算。

</div>
<div class="notationitem" markdown="1">

**$Q=1$**

每个种子仅测试一种表达条件一次，用于估计单个预设自身的越狱效果。

</div>
<div class="notationitem" markdown="1">

**$Q=6$**

每个种子依次测试固定的六种表达条件，用于衡量六条件池在相同查询预算下的种子级覆盖能力。

</div>

</div>

**直接相关的工作**

- **ASR 导向的音频扰动攻击（Carlini and Wagner, 2018；Abdoli et al., 2019）**: 这些工作主要通过扰动攻击语音识别或音频系统，说明语音输入具有对抗脆弱性；本文转向端到端 Audio LLM，并研究无需改写文本、仅改变自然语音表达时出现的安全失效。
- **StyleBreak 及其他风格驱动的音频越狱方法（Li et al., 2026 等）**: 这是与 PJ-Break 最接近的研究方向，但已有方法常同时改变人物设定、词汇框架、说话风格或搜索预算，难以归因于语音表达本身。PJ-Break 固定文本、限制为六种预设表达，并设置固定六查询预算，以支持与 StyleBreak 重实现的匹配预算比较。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

原生音频大模型能够直接利用语音信号中的副语言信息，即文字之外的音高、响度、节奏和音质等线索。因此，一个在文字层面看似已经接受安全训练的系统，仍可能因说话方式变化而削弱拒答。若开发者只用文本提示或中性语音做红队测试，部署中的高唤醒情绪、快速讲话等自然表达就可能成为未覆盖的攻击面。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **扰动式音频攻击**：在语音或音频信号上加入经过设计的扰动，使语音系统产生错误识别或非预期行为；这类工作证明了音频通道可被攻击，但关注点通常不是自然语音表达在文本完全相同时对音频大模型拒答行为的影响。
- **声学控制或风格化越狱**：通过改变声音风格、角色设定、表达方式或其他声学条件来诱导端到端音频大模型输出不安全内容；部分方法还会配合文本改写或多次搜索，以提高攻击成功机会。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 既有攻击常同时改变词汇内容、人物设定、说话风格或查询与搜索预算。多个变量共同变化时，即使越狱率提高，也无法判断增益究竟来自文本语义、角色提示、更多尝试，还是语音表达本身。
- 已有结果缺少严格的匹配文本对照与明确的剩余混杂说明，因而不足以回答因果归因更窄的问题；与此同时，作者也承认单个表达预设内部可能有多种声学属性共同变化，所以可识别的是“预设级语音表达”的关联效应，而不是某一个声学参数的纯粹效应。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

在相同有害转录文本、可比查询预算和预先规定的表达条件下，尚缺少受控证据来量化不同语音表达预设各自能够带来多少越狱能力，以及若组合多个固定预设，它们能覆盖多少仅靠单一中性表达无法攻破的样本。这个缺口也使研究者难以判断韵律相关变化是否应被列为音频大模型安全评测的一等变量。

</div>
<div markdown="1"><span>核心问题</span>

当输入的转录文本保持完全不变时，仅改变语音的表达预设——例如惊慌、愤怒、命令式、快速、耳语或中性表达——与音频大模型越狱能力之间有多强的关联？

</div>
<div markdown="1"><span>作者直觉</span>

原生音频模型并非只把语音转换成文字后再推理，它还可能利用情绪强度、语速、权威感和音质等副语言线索。这些线索可能让输入偏离安全微调中以中性语音为主的分布，或改变模型对紧急性、说话者意图及应答优先级的判断，从而削弱拒答。作者将分布偏移、注意路由变化和隐式危机响应等仅视为可能解释，而非已经得到因果验证的机制。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PJ-Break是一套面向音频大语言模型的黑盒安全评测方法，核心控制变量是“文字内容不变、说话方式改变”。方法从同一组有害种子指令出发，用固定TTS系统生成Neutral、Panic、Anger、Commanding、Fast和Whisper六种语音版本；经转录一致性、削波、响度及声学属性检查后，将音频以单轮方式输入目标模型，并统计单个预设与固定六查询池的攻击成功情况。攻击者只能提交音频，不能访问梯度、logits或参数；开放权重模型的内部访问仅用于论文中次要的可解释性分析，不参与攻击生成。

直观地说，该方法把同一句话分别用中性、惊慌、愤怒、命令、快速和耳语方式“念出来”，观察模型是否会仅因语气和节奏变化而改变安全行为。其控制重点不是证明某一个声学变量具有独立因果作用，而是在尽量固定文本、说话人和合成环境后，检验成组的语音表达差异是否构成可重复的越狱因素。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建固定文本的安全测试种子

保留每条种子指令的词汇内容和请求语义，将其作为六种语音条件共享的文本基础；完整设计形成100条指令乘以6种条件的600个样本。

<div class="method-step__io" markdown="1">

**输入**：来自AdvBench和HarmBench的100条种子指令，覆盖暴力、非法活动、仇恨言论、自伤、错误信息和隐私侵犯六类风险。  
**输出**：按风险类别组织、可进行逐种子配对比较的固定文本集合。

</div>

**直观理解**：先固定“说什么”，再改变“怎么说”，这样模型输出差异更可能与语音表达有关，而不是由改写提示词造成。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成六种语音表达预设

使用同一Azure Neural TTS技术栈和en-US区域生成音频；Neutral、Panic、Anger、Fast、Whisper采用JennyNeural，Commanding因需要明显降低基频而采用GuyNeural。预设分别侧重唤醒度、权威感或时间节奏，但允许多个声学属性共同变化。

<div class="method-step__io" markdown="1">

**输入**：每条固定种子文本，以及Neutral、Panic、Anger、Commanding、Fast、Whisper六种预设。  
**输出**：AdvAudio-Prosody的六条件配对音频，其中五个条件构成同说话人比较，Commanding被明确标记为说话人身份部分混杂的条件。

</div>

**直观理解**：这一步相当于让同一位朗读者用五种方式读同一句话；命令语气因换成男声而不再是完全公平的同说话人对照，所以需要单独分析。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行质量控制与声学验证

排除削波样本及不满足合成后转录保真要求的样本，并通过响度归一化和峰值限制降低音量差异；测量平均及方差基频F0、RMS强度、频谱倾斜和语速，以确认各预设确实产生预期的总体声学偏移。

<div class="method-step__io" markdown="1">

**输入**：TTS生成的全部候选音频。  
**输出**：通过质量控制的配对评测面板；Qwen2-Audio主要结果使用共享的95条post-QC种子。

</div>

**直观理解**：研究者先确认音频没有爆音、音量异常或明显念错，再检查“惊慌是否更高更抖、快速是否真的更快”等。该检查只能验证预设整体不同，不能把效果唯一归因于某个声学特征。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 黑盒查询与配对安全评测

以单轮、仅音频输入的方式查询模型；分别评估每个预设的Q=1成功率，并用固定六条件构成best-of-six查询池，按种子统计六次中是否至少一次成功。进一步移除Commanding形成五条件同声线池，并用文本情绪与音频情绪的四条件消融区分词汇包装和韵律表达的贡献。

<div class="method-step__io" markdown="1">

**输入**：通过质检的各条件音频和目标Audio LLM。  
**输出**：单预设攻击结果、六查询种子覆盖率、同声线敏感性结果及文本—韵律消融结果。

</div>

**直观理解**：单条件实验回答“某一种说法是否比中性朗读更危险”，六查询池回答“给攻击者固定六次机会时能覆盖多少不同问题”。去掉换声线条件和拆分文字情绪、声音情绪，则用于判断结果是否主要由换人说话或情绪化措辞造成。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

这篇论文不以中心数学公式展开，或全文中未提取到可靠的关键公式。

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。PJ-Break不是需要训练或微调的攻击模型，而是基于可控TTS、质量控制和固定查询预算的黑盒评测协议；论文给出的核心方法章节没有定义用于参数优化的中心损失函数。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 受控语音表达预设**

六个预设围绕三类目标维度组织：Panic或类似尖叫的表达侧重高唤醒度，Commanding侧重低基频权威感，Fast侧重超过220 WPM的时间压缩；Anger、Whisper和Neutral提供其他情绪或基准条件。预设是复合干预，同一条件内的基频、强度、频谱和语速可能相关变化。

> 直观理解：研究对象不是抽象的单一“韵律旋钮”，而是现实中可听见的整套说话方式。因此结果能说明表达方式重要，却不能直接断言只有音高、只有语速或只有音量导致越狱。

**2. 声学验证与混杂控制**

方法以F0均值和方差、RMS强度、频谱倾斜及语速描述条件差异，同时实施转录保真筛选、LUFS响度归一化、峰值限制和削波排除。五个条件固定JennyNeural说话人；Commanding使用GuyNeural，故其权威表达与说话人身份不能完全分离。

> 直观理解：该模块确保比较的音频在技术质量上可比，并诚实标出仍未排除的替代解释。尤其是Commanding的结果不能简单理解为纯粹的低音高效应。

**3. 固定预算的黑盒攻击协议**

攻击阶段不使用模型参数、梯度或输出logits，只允许单轮音频输入；核心预算为每个种子固定六次查询。Q=1结果用于同预算比较各单预设与Neutral，best-of-six结果用于衡量多个预设的互补覆盖，并可与同为六查询预算的StyleBreak重实现进行公平比较。

> 直观理解：固定查询次数可避免某种方法仅因尝试更多次而显得更强。开放模型上的探测和激活修补属于解释性分析权限，不是攻击算法的一部分。

**训练与推理**

无训练阶段。评测时，研究者先为每条固定文本离线合成六种语音表达，完成转录保真、削波、响度和声学属性检查，再将保留音频逐个送入目标Audio LLM。单预设评测对共享种子面板各查询一次；完整PJ-Break对同一种子使用六个固定预设各查询一次，只要任一输出满足论文的安全判定协议，该种子即计为best-of-six成功。

为分析控制强度，方法另计算不含Commanding的Neutral/Panic/Anger/Fast/Whisper五条件池，从而避免把全部效果归因于换用GuyNeural。文本—韵律消融使用NN（中性文本与中性音频）、EF（情绪文本与平淡音频）、NE（中性文本与情绪音频）和EE（情绪文本与情绪音频）四种组合；其中情绪文本仅加入紧迫、愤怒或权威包装而保持底层请求语义，借此比较词汇框架与声音表达的边际影响。

**复现信息**

语音统一由Azure Neural TTS生成，区域固定为en-US；五个同声线条件使用en-US-JennyNeural，Commanding使用en-US-GuyNeural。Fast预设目标语速超过220 WPM；具体SSML参数位于补充材料，所给节选未完整列出。数据集规模为100条种子乘以6种条件，共600条TTS音频；主要Qwen2-Audio分析采用转录质检后保留的95种子共享面板。

公平解释结果时必须保留三项边界：第一，预设会同时改变多个相关声学属性，方法没有识别单变量因果效应；第二，Commanding包含声线变化，因此只能视为附加且部分混杂的条件；第三，残余语音识别差异仍可能影响模型接收到的内容。RealSpeech-20人工录音和1米智能手机播放的OTA-Replay只属于小规模迁移检查，不能替代主TTS面板的受控结论。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- AdvAudio-Prosody：作者构建的600样本音频安全评测基准，包含经过声学属性验证的不同语音表达预设，用于研究转写文本不变时韵律变化造成的越狱风险。原文节选未明确报告其训练、验证和测试划分；该基准在本文中承担攻击评测集而非模型训练集的角色。
- 主评测种子面板：初始包含100条恶意指令种子，经一次统一质量控制后保留95条。删除项包括3条转写不匹配（词错误率至少5%）、1条音频质量失败和1条重复内容。该固定面板用于Qwen2-Audio核心比较、GPT-4o的PJ-Break评测及共享面板上的配对显著性检验。
- 人工校准子集：从表3主要比较样本中按危害类别分层抽取200个样本，由3名人工标注者判断是否有害。它用于校准自动裁判体系，而不是替代整个测试集上的人工审核。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**音频级攻击成功率（Audio-level ASR）**

把每个渲染后的音频视为一次独立试验，统计单一语音预设诱导模型产生有害回答的比例。它适合比较Panic、Anger、Fast和Neutral等单次渲染条件。 （对攻击者而言越高越强，因为更高表示一次给定语音表达更容易绕过安全机制；对防御者而言则越低越好。）

</div>
<div class="metricitem" markdown="1">

**种子级best-of-six成功率**

对每条恶意指令固定生成并查询6种韵律版本，只要任意一个版本得到有害回答，该种子即计为成功。该指标衡量固定六查询池能够覆盖多少不同指令，而不是某一种语音的单次成功概率。 （对攻击者而言越高越好，因为它表示固定查询预算下至少一种韵律奏效的种子更多；但不能直接与Q=1控制条件或查询数更大的best-of-N方法等同比较。）

</div>
<div class="metricitem" markdown="1">

**Fleiss’ κ与Cohen’s κ一致性**

Fleiss’ κ衡量多名人工标注者之间超越随机水平的一致性，Cohen’s κ用于概括自动裁判集成结果与人工多数标签之间的一致性。人工标注的总体Fleiss’ κ为0.78，自动集成与人工多数标签的一致性κ为0.76。 （通常越高表示标注或裁判结果越稳定、越可信；但高一致性并不保证安全政策定义本身没有偏差。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### Qwen2-Audio上的单预设Q=1比较：Panic、Anger、Fast相对Neutral

<div class="result-value" markdown="1">

在质控后95条种子上，Panic成功38条、Anger成功35条、Fast成功32条，而Neutral仅成功4条。

</div>

这直接表明，在文本保持相同且每条种子只查询一次时，高唤醒情绪或快速语速与更高的有害回答率相关，因此核心现象并非只能由六次尝试的机会累积来解释。不过，这些预设的多个声学属性可能共同变化，结果不能单独证明某一个声学参数具有因果作用。

<div class="result-source" markdown="1">

来源：摘要；单预设结果对应表6

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">On the exact post-QC Qwen2-Audio panel, the Q=1 Panic (38/95), Anger (35/95), and Fast (32/95) presets are all well above Neutral (4/95).</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 固定六查询PJ-Break池在Qwen2-Audio与GPT-4o上的种子覆盖

<div class="result-value" markdown="1">

六种预设的固定查询池在Qwen2-Audio上成功覆盖44/95条种子，在GPT-4o上覆盖15/95条种子。

</div>

该结果说明韵律攻击不仅出现在开放权重替代模型上，也能迁移到主要黑盒目标，但在GPT-4o上的覆盖明显较低。这里衡量的是每条种子六次固定尝试中至少一次成功，不能解释为单个音频具有同等成功率，也不能据此证明对所有音频模型都具有普遍迁移性。

<div class="result-source" markdown="1">

来源：摘要；第4.3节主结果，表3

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">The fixed six-query pool covers 44/95 Qwen2-Audio seeds and 15/95 GPT-4o seeds and exceeds a matched-budget StyleBreak reimplementation (27/95) on Qwen2-Audio.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### Qwen2-Audio上PJ-Break与StyleBreak的同预算比较

<div class="result-value" markdown="1">

在每条种子均使用6次查询的条件下，PJ-Break覆盖44/95条种子，StyleBreak重新实现覆盖27/95条；共享质控面板上的配对McNemar检验给出p<0.001。

</div>

同预算结果支持作者的核心主张：预先设计的韵律变化比所比较的一般风格化方案覆盖更多种子，而且差异在共享样本上的配对检验中显著。它证明的是对该StyleBreak重新实现和该Qwen2-Audio面板的优势，不等于对所有风格攻击或所有模型的全面领先。

<div class="result-source" markdown="1">

来源：第4.3节“Main Results”，表3；准确覆盖计数见摘要

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">PJ-Break clearly exceeds transcript-preserving controls and the matched-budget StyleBreak reimplementation on Qwen2-Audio, and a paired McNemar test on the shared retained panel confirms the gain over StyleBreak (p<0.001).</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 六种语音预设是受控的表达条件，但其声学属性可能共同变化；即使移除Commanding的说话人混杂，实验仍难把效果唯一归因于基频、响度、语速或其他单一声学特征。因此结果支持“语音表达整体影响安全性”，但不是细粒度声学因果识别。
- 有害性标签依赖自动裁判集成：LLM裁判可能受措辞影响，关键词规则可能漏掉隐晦危害，多数投票也可能掩盖边界案例。Llama Guard 3同时出现在裁判集成和Pro-Guard-Lite中，使部分防御比较缺乏完全独立的评测；200样本人工研究只能用于校准，不能替代全量人工审核。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- Text-Only与Neutral Audio：二者是保持指令内容不变的控制组；前者检验纯文本输入的风险，后者使用中性TTS语音，检验“仅把文本变成音频”是否足以解释攻击效果。Neutral Audio同时对应第4.5节的NN基线和表6的Neutral条件。
- StyleBreak：最接近本文问题的风格感知攻击基线。作者对其重新实现，并为每个种子同样分配6次查询，因此它是判断PJ-Break收益是否超出一般语音风格变化的关键公平对照。
- BoN Jailbreaking与AJailBench-APT：分别代表高预算best-of-N搜索和扰动导向攻击。它们用于覆盖不同音频越狱攻击家族，但查询预算明显更高，因此只能辅助说明攻击强度，不能与固定六查询PJ-Break作严格同预算归因。
- SACRED-Bench：组合式音频安全基线，用于判断PJ-Break相对复合攻击或复合评测设计的表现。表3仅保留一个代表行，以避免与作用重叠的基线重复展示。

**实验想回答的问题**

- 在恶意指令文本完全相同的条件下，仅改变语音的唤醒度、权威感或语速，能否显著提高音频大语言模型输出实质性有害内容的概率？
- 这种韵律驱动攻击相对文本控制、风格化攻击及高预算搜索基线是否仍然有效，并能否跨模型迁移；观察到的提升究竟来自语音表达本身，还是来自文本情绪化、说话人变化等混杂因素？

**实验实现**

主要目标模型是黑盒GPT-4o audio-preview；Qwen2-Audio-7B-Instruct作为开放权重替代模型，主要支持可审计核心比较和探索性分析。Gemini 2.0 Flash与SALMONN仅用于描述性的历史或跨模型验证。PJ-Break为每条种子使用6个预先规定的语音表达，不自适应提前停止，也不使用梯度或额外搜索；单预设分析为Q=1，汇总攻击为固定Q=6。所有音频统一归一化至−23 LUFS、峰值限制为−1 dBFS，并重采样为16 kHz单声道。回答只有在3个裁判中至少2个判为有害，且拒绝措辞之外包含超过50个词元的实质性有害内容时才记为成功；裁判包括Claude 3.5 Sonnet、Llama Guard 3和政策关键词分类器。作者还报告阈值敏感性检查保持方法相对排序，并且仅在具有准确质控后计数的分析上进行统计检验。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 同说话人敏感性分析：从六预设池中移除存在说话人混杂的Commanding条件 | 排除Commanding后，同说话人预设池在95条Qwen2-Audio种子上仍成功覆盖40条。 | 该消融用于排除“攻击提升主要来自Commanding条件更换说话人”这一解释。覆盖仍然较高，说明主要现象并不依赖该混杂条件；但相较完整池的变化同时受到查询集合减少影响，不能精确量化说话人身份本身的独立贡献。 | 摘要；第4.3节指向表4的same-voice sensitivity view<br><span class="experiment-evidence">A same-voice pool excluding the confounded Commanding condition still reaches 40/95, and a retained-panel ablation shows emotional-delivery audio alone (44/95) is far more effective than emotional text alone (11/95).</span> |
| 模态归因消融：情绪化语音表达与情绪化文本对比 | 在保留面板上，仅使用情绪化语音表达成功44/95，而仅使用情绪化文本成功11/95。 | 该对比试图隔离情绪信息通过声音传递还是通过词汇改写传递。语音条件远高于文本条件，支持韵律载体本身是主要风险因素，而非只要把文字写得更情绪化即可获得相同效果。不过，该结果仍依赖具体情绪化实现，不能证明所有声学变化都优于所有文本攻击。 | 摘要；保留面板模态消融<br><span class="experiment-evidence">A same-voice pool excluding the confounded Commanding condition still reaches 40/95, and a retained-panel ablation shows emotional-delivery audio alone (44/95) is far more effective than emotional text alone (11/95).</span> |

**定性案例**

- 原文未明确报告。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper studies prosody-based jailbreak attacks and mitigations for audio-capable language models.; rule check: matched taxonomy keywords; top rule score=6.0
- 全文指纹：`0f4f01eb0b23cd9adbfdb85b37154a025f331db00a7d048744c999973d0e7cc1`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
