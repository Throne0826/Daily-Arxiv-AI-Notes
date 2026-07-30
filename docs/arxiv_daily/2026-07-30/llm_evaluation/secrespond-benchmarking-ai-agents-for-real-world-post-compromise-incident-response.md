---
title: "[论文解读] SecRespond: Benchmarking AI Agents for Real-World Post-Compromise Incident Response"
description: "[arXiv 2607.26791][LLM 评测] SecRespond通过真实受侵云主机的取证磁盘快照与安全产品报告，评测LLM智能体能否完成从主动调查、攻击链重建到全面修复规划的完整事后事件响应。"
arxiv_id: "2607.26791"
announcement_date: "2026-07-30"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T09:23:24.895713+00:00"
source_sha256: "a36b1c515776bbe2c0991c339f7d23a1e3028e6ad80cc439482fb139998ac56d"
tags:
  - "LLM 评测"
  - "LLM Agent"
  - "LLM 其他"
  - "大语言模型智能体"
  - "事后入侵响应"
  - "数字取证"
  - "网络安全基准"
  - "命令行工具使用"
  - "MITRE ATT&CK"
  - "修复规划"
  - "LLM-as-a-Judge"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2607.26791</p>

# SecRespond: Benchmarking AI Agents for Real-World Post-Compromise Incident Response

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-30</span>
<span><strong>作者</strong> Lehan Wang, Boli Chen, Ruixue Ding, Pengjun Xie, Jinwei Huang, Zhendong Liu, Shuo Wang, Tao Lei, Xin Ouyang, Xiaomeng Li</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.26791v1) · [PDF 下载](https://arxiv.org/pdf/2607.26791v1) · **关键词** 大语言模型智能体, 事后入侵响应, 数字取证, 网络安全基准, 命令行工具使用, MITRE ATT&CK, 修复规划, LLM-as-a-Judge  
**代码**: [https://github.com/Alibaba-NLP/qqr/tree/main/data/secrespond](https://github.com/Alibaba-NLP/qqr/tree/main/data/secrespond)  

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

SecRespond通过真实受侵云主机的取证磁盘快照与安全产品报告，评测LLM智能体能否完成从主动调查、攻击链重建到全面修复规划的完整事后事件响应。

**不用术语来说**：服务器遭入侵后，安全人员不能只处理告警直接指出的问题，还要检查磁盘中未被告警发现的恶意文件、持久化机制和被擦除的痕迹，弄清攻击者做过什么，并制定可验证且不遗漏的修复方案；本文关心现有LLM智能体是否真正具备完成这一整套工作的能力。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 作者提出首个面向完整事后事件响应流程的SecRespond基准：10个场景均来自经端到端网络攻击后冻结的云主机环境，覆盖4类入侵入口、21种ATT&CK技术和5种操作系统。
- 作者建立分层能力评估框架，将任务拆为280个专家设计的检查点，并映射到5个维度下的52个能力项；检查点分别评估“是否发现问题”和“是否规划有效处置”，以支持跨场景比较和细粒度能力诊断。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文处于大语言模型智能体与网络安全事件响应的交叉领域。传统网络安全基准多考察攻击发生前的漏洞发现、利用、修补或安全知识，通常假设环境干净且任务边界明确；SecRespond转而考察主机已被成功入侵后的响应流程，要求智能体面对真实磁盘遗留物、告警及正常活动噪声，通过命令行主动取证，识别入侵实体与持久化机制，评估基线和漏洞风险，并提出可验证、覆盖完整的修复方案。该设置关注的不是模型是否“知道”安全概念，而是其能否在长流程中关联多个文件和证据，将发现、攻击链重建与处置规划连成闭环。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**事后入侵响应（post-compromise incident response）**

指攻击者已经突破主机之后开展的调查与处置，包括发现恶意痕迹、重建攻击链、判断风险并清除或缓解威胁。与攻击前漏洞检查不同，此时系统可能含有持久化机制、被删除的痕迹以及大量无关活动。

</div>
<div class="conceptitem" markdown="1">

**取证磁盘快照（forensic disk snapshot）**

主机磁盘在某一时刻的冻结副本，保存文件、配置及其他可供调查的系统痕迹。智能体需要跨文件检索和关联这些材料，而不能只依赖已经给出的告警文本。

</div>
<div class="conceptitem" markdown="1">

**MITRE ATT&CK技术**

ATT&CK用标准化技术条目描述攻击者在入侵过程中采取的具体行为，例如建立持久化或执行恶意命令。本文用其刻画10个靶场所覆盖的攻击行为多样性，共涉及21种技术。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

每个任务对应一台已遭端到端网络攻击的真实云主机冻结环境。输入包括该主机的取证磁盘快照，以及主机安全产品产生的告警、漏洞扫描和安全基线检查结果；智能体在OpenCode智能体框架中通过命令行检查磁盘与相关材料。输出为一个进度文件和四份报告，分别覆盖已发现的入侵、漏洞风险、基线风险及修复计划；报告还应重建事件经过，并说明如何处理发现的问题。基准由10个相互不同的网络靶场组成，覆盖4类初始入口、21种ATT&CK技术和5种操作系统。其关键假设是主机已经被攻陷，显式告警可能只暴露部分问题，因此智能体必须主动寻找未触发告警的静默入侵证据。评价框架把任务拆成280个专家设计的检查点，并映射到52个能力项及五个维度：入侵实体、持久化机制、基线风险、漏洞风险、调查与响应质量；检查点分别从“是否发现”和“是否规划处置”两个方面评分，以便比较不同靶场中的能力。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **CyberSOCEval（Deason et al., 2025）**: 属于防御侧安全运营评测，但原文指出其将问题简化为对孤立告警的推理，没有让智能体直接调查被攻陷主机中的真实文件系统和攻击遗留物，因此不足以覆盖完整的事后响应流程。
- **ExCyTIn-Bench（Wu et al., 2025）**: 同样面向事后威胁检测，并要求多步和跨文件分析；但论文表1将其标为不具备真实文件系统、细粒度量规评价和命令行兼容性。SecRespond进一步以冻结的云主机磁盘为任务基础，并同时评价调查发现与修复规划。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

LLM智能体正在进入真实安全运营流程，并可读取主机材料、调用命令行工具。一旦主机已经失陷，智能体必须从混杂着正常活动与攻击残留的系统中发现入侵、还原攻击链，并给出完整修复计划；若缺乏贴近该工作流的可靠评测，就无法判断它们能否安全地参与生产环境中的人工事件响应。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **攻击前的攻防能力基准**：CTF、真实Web应用或软件项目类基准通常把智能体置于干净、理想化的初始环境，要求其发现和利用漏洞，或在攻击发生前完成漏洞修补；部分新基准进一步覆盖较完整的攻击生命周期。
- **孤立安全材料上的防御评测**：这类工作通过安全知识问答、漏洞发现与补丁任务，或让模型单独分析告警、系统日志和事件报告，衡量其知识、推理或局部处置能力，而不是让智能体直接调查一台真实受侵主机的完整磁盘材料。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 攻击前基准没有呈现入侵成功后留下的持久化机制、被刻意删除的痕迹以及并发主机活动噪声，因此不能检验智能体能否主动发现告警之外的隐蔽问题并重建实际攻击链。
- 基于孤立告警、日志或报告的评测把事件响应切割成局部推理任务，无法判断智能体能否把调查结果转化为覆盖所有风险、处理恶意残留且可验证的完整修复计划。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

现有研究缺少一个以真实受侵主机为对象、贯穿调查与修复的事后事件响应基准，也缺少能同时区分问题发现能力与处置规划能力，并在异构攻击场景间进行细粒度比较的统一评价框架。

</div>
<div markdown="1"><span>核心问题</span>

面对受侵主机的取证磁盘快照以及安全产品给出的告警、漏洞扫描和基线检查，当前LLM智能体能否主动发现显性与静默入侵，准确重建事件，并为入侵、漏洞和基线风险制定全面有效的修复方案？

</div>
<div markdown="1"><span>作者直觉</span>

真实磁盘快照保留了智能体必须自行搜索和交叉验证的攻击残留，而安全产品报告则提供现实工作中常见但不完整的线索；将两者同时交给智能体，再用专家检查点分别核验“找到了什么”和“准备如何处理”，可以暴露仅会复述告警或执行第一个显然修复动作的模型，并定位其在持久化发现、风险覆盖和响应闭环等环节的具体短板。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

SecRespond不是训练新模型的方法，而是一套面向失陷后事件响应的评测流程。每个网络靶场以一台经真实网络协议完成端到端入侵的云主机为基础，向代理提供该主机的取证磁盘快照，以及主机安全产品生成的告警、漏洞扫描结果和基线检查结果；代理通过命令行调查这些材料，最终提交入侵取证、基线风险、漏洞风险和修复计划等开放式报告。由于报告无法像选择题或CTF flag那样直接精确匹配，作者把事件响应能力分解为五维能力分类及每个靶场对应的细粒度检查点，再使用分层的LLM-as-a-Judge框架逐项判定报告是否满足检查点，并聚合为靶场内分析和跨靶场能力比较。直观而言，这套方法先搭建“真正被攻陷过的机器”，再让代理像SOC事件响应人员一样查证和写报告，最后用结构化评分清单而不是笼统印象评价报告。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构建真实失陷后的网络靶场

作者对云主机实施完整入侵，使磁盘中自然留下攻击入口、后续行为、持久化机制、可能被部分清理的痕迹以及正常活动噪声。基准共实例化10个靶场，覆盖4类入口、21种ATT&CK技术和5种操作系统。

<div class="method-step__io" markdown="1">

**输入**：完整实例化的云主机、真实网络协议上的端到端攻击过程，以及攻击期间并发存在的正常活动。  
**输出**：10个彼此独立、具有真实失陷后状态的云主机环境。

</div>

**直观理解**：这一步不是人工摆放几份理想化日志，而是先让攻击真实发生，再保留攻击结束后的现场，因此代理必须面对残缺痕迹和正常噪声。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 封装代理可调查的证据与任务输入

每个靶场向代理提供取证磁盘快照，并附带安全产品报告的告警、漏洞扫描发现和基线检查结果；代理在OpenCode代理框架中访问主机材料和命令行接口。任务要求代理同时调查已暴露问题和磁盘中未被告警直接指出的潜在问题。

<div class="method-step__io" markdown="1">

**输入**：失陷云主机及主机安全产品对该主机生成的安全分析结果。  
**输出**：由磁盘现场、告警和两类扫描发现组成的标准化事件响应任务。

</div>

**直观理解**：安全产品给出的信息相当于调查线索，而磁盘快照相当于完整案发现场；代理不能只复述告警，还要主动搜查没有被点名的静默入侵痕迹。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 执行取证调查并形成响应报告

受测LLM代理使用命令行检查磁盘工件并推断攻击与风险，随后生成开放式事件响应报告。规定输出覆盖入侵取证报告、基线风险报告、漏洞风险报告及相应修复计划，并应提供可核验的调查依据。

<div class="method-step__io" markdown="1">

**输入**：单个靶场的取证磁盘快照、告警、漏洞扫描结果和基线检查结果。  
**输出**：面向该靶场的综合事件响应报告。

</div>

**直观理解**：代理需要完成从“找出发生了什么”到“说明该怎样修复”的完整闭环，而不是只回答某个文件是否恶意。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 建立能力分类与靶场检查点

作者将任务所需技能组织成五维能力分类，并为每个靶场把各项能力映射到细粒度检查点。检查点把一份开放报告拆成可以分别验证的事实、证据或响应要求。

<div class="method-step__io" markdown="1">

**输入**：每个靶场的真实攻击过程、风险状态、预期调查证据及事件响应要求。  
**输出**：按靶场定制、同时可映射到统一能力维度的评分细则。

</div>

**直观理解**：它类似教师先把一道开放论述题拆成多个得分点：既能判断代理漏掉了哪条关键事实，也能汇总判断它在哪类能力上薄弱。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="formula-status formula-status--none" markdown="1">

**未收录可核对的关键公式**

该工作以系统设计、数据或实验分析为主，或现有全文证据不足以可靠还原中心方程。

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。SecRespond是评测基准而非模型训练方法，所给章节没有提出用于参数优化的损失函数，也没有说明利用该基准微调受测模型；LLM-as-a-Judge在此承担结构化判定作用，而不是受测代理的训练目标。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 真实失陷后取证环境**

每个靶场源自一台真实、完整实例化的云主机，并通过真实网络协议经历端到端攻击；评测输入保留磁盘取证工件、持久化机制、部分清理痕迹和并发正常活动，而不只提供预先筛选的安全日志。10个靶场覆盖4类攻击入口、21种ATT&CK技术和5种操作系统。

> 直观理解：该模块决定了评测是否接近真实事件响应：攻击留下的证据可能零散、被删除一部分或混在正常文件中，因此仅依靠告警摘要的代理难以取得完整结果。

**2. 五维能力分类与细粒度检查点**

作者先建立五维事件响应能力分类，再针对每个靶场把能力落实为可判定的检查点。检查点既作为该靶场的评分量规，也提供跨靶场汇总时的统一能力索引；所给章节未列出五个维度的具体名称及完整检查点生成流程。

> 直观理解：不同主机的攻击细节并不相同，不能使用完全相同的事实答案；能力分类提供共同坐标，检查点则保留每个现场特有的正确答案。

**3. 分层LLM-as-a-Judge评测器**

针对无法进行固定字符串匹配的开放式调查报告，评测器将目标分解为可核验单元，先在检查点层面作出判断，再依据检查点与能力项的映射进行能力级分析。论文将这一设计与选择题准确率、CTF flag匹配及执行输出验证等确定性协议区分开来。

> 直观理解：事件响应报告可能用不同措辞描述同一事实，简单关键词匹配容易误判；逐项语义判断可以容纳表达差异，同时通过固定检查点减少裁判只凭整体印象打分的问题。

**训练与推理**

评测阶段，对每个受测前沿LLM，将其接入OpenCode代理框架，并在各个SecRespond靶场中提供取证磁盘快照、告警、漏洞扫描和基线检查等输入。代理通过命令行开展调查并输出开放式事件响应报告；随后，分层LLM-as-a-Judge按照该靶场的细粒度检查点逐项判定，再沿检查点到五维能力项的映射汇总结果，以支持单靶场诊断和跨靶场、跨模型比较。摘要说明共评测23个前沿LLM，但所给章节未明确报告每个代理的上下文配置、工具权限、运行轮数、采样参数、停止条件、裁判模型身份及重复评测策略。

**复现信息**

公平解释结果所需的核心规模信息是：基准包含10个由不同失陷云主机构建的网络靶场，覆盖4类入口、21种ATT&CK技术和5种操作系统；受测对象为运行在OpenCode代理框架上的23个前沿LLM。每个任务同时提供磁盘快照与安全产品侧信息，并要求产出入侵、基线风险、漏洞风险和修复计划相关报告。基准公开地址为https://github.com/Alibaba-NLP/qqr/tree/main/data/secrespond。所给文本没有进一步明确主机镜像格式、命令行沙箱限制、检查点数量、五维分类名称、评分聚合公式或LLM裁判配置，复现时应回查论文完整章节与公开仓库。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- SecRespond 基准：包含 10 个网络靶场，每个靶场来自一台不同的已受入侵云主机；共覆盖 4 类攻击入口、21 种 ATT&CK 技术和 5 种操作系统。每个任务向代理提供取证磁盘快照，以及主机安全产品产生的告警、漏洞扫描和基线检查结果；代理需输出入侵、基线风险、漏洞风险的取证报告与修复计划。原文节选未说明训练集、验证集或测试集划分，实验用途是端到端评测。
- 靶场按攻击结构形成难度层次：Log4j-RCE、Docker-Escape、Redis-RCE主要测试单入口、线性攻击链和告警可见的常见持久化；SSH-Miner、Next.js-RCE、Jenkins-RCE加入更宽的主机基线、多步提权及跨服务关联；Shiro-Fastjson、RDP-Service-Abuse、NPM-Worm、ASP .NET-ViewState进一步测试宽攻击面、跨服务或跨运行时关联及伪装持久化。各靶场的具体样本数和检查点数量在所给节选中未明确报告。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**检查点级 CHK-score**

由三名独立 LLM 裁判依据预定义检查点标准，分别评价报告在 Detection 或 Planning 轴上是否达到要求，再对三名裁判的检查点得分取平均。Detection 衡量是否发现并正确说明问题，Planning 衡量是否提出正确、完整且包含验证环节的处置方案。 （越高越好，因为更高表示更多检查点被正确满足；但它是基于 LLM-as-a-Judge 的标准符合度，不等同于真实环境中修复命令已经成功执行。）

</div>
<div class="metricitem" markdown="1">

**靶场级 CHK-score**

对某一靶场及某一评价轴，将该靶场所有相关检查点的已获 CHK-score 求均值并转成百分比，即 CHK-score^a_r = (∑_{c∈C^a_r} CHK-score^a_c / |C^a_r|) × 100%，其中 r 为靶场，a∈{det, plan} 为检测或规划轴，C^a_r 为对应检查点集合。它用于比较模型在具体攻击场景中的端到端完成度。 （越高越好，因为代表该靶场内更多应检测或应处置事项得到满足。）

</div>
<div class="metricitem" markdown="1">

**CAP-score**

依据检查点到能力项目的映射，将得分聚合到五个维度：入侵实体 ENT、持久化机制 PER、基线风险 BAS、漏洞风险 VUL、调查与响应质量 Q；每个维度分别报告 Detection 和 Planning 百分比，用于定位模型能力短板。 （越高越好，因为表示模型在相应能力维度覆盖了更多检查点；不同维度的分数不宜直接解释为相同的实际业务风险。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### 23 个模型在 10 个靶场上的总体检测与修复规划比较

<div class="result-value" markdown="1">

所有模型的 Detection 均高于 Planning，说明修复规划是共同瓶颈；例如 GPT-5.5 的检测为 70.7%，规划仅为 36.0%，而 Claude Sonnet 4.5 的两轴差距最小，为 8.5 个百分点。作者进一步报告，没有任何模型在任何单一靶场上同时实现完整检测和完整修复。

</div>

模型通常能沿告警线索找到明显恶意进程、文件或漏洞，却容易在后续漏掉凭据轮换、外联阻断、残余持久化清理以及业务服务健康验证。因此，“发现问题”不能推出“能够安全收尾”。这些分数评价的是书面报告对检查点的满足程度，并不证明模型在真实生产主机上执行修复时同样可靠。

<div class="result-source" markdown="1">

来源：§4.3 Finding 1；总体趋势见 Figure 3(a)，无模型完整完成的结论见 §4.3 Finding 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">For example, GPT-5.5 scores 70.7% on detection but only 36% on planning, while Claude Sonnet 4.5 presents the narrowest gap of 8.5%.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 模型总体排名及跨场景稳定性

<div class="result-value" markdown="1">

Claude Opus 4.7 的平均靶场级成绩最高，为 Detection 79.0%、Planning 65.7%；其后是 Claude Opus 4.6（78.2%/58.0%）、GLM-5.1（76.3%/59.2%）和 Qwen3.7 Plus（75.6%/58.8%）。开放模型 GLM、DeepSeek 可超过部分 GPT 和 Gemini 模型，表明闭源或专有身份本身不能保证更强的事件响应能力。

</div>

结果说明部署选型应直接依据取证和响应任务，而不能仅凭模型品牌或通用排行榜。Claude Opus 4.7 在该基准的平均分领先，但这不表示它在每一能力维度都最佳，也不表示其结果可无条件推广到基准未覆盖的攻击、操作系统或在线响应环境。

<div class="result-source" markdown="1">

来源：§4.3 Finding 2；详细逐靶场结果见 Table 4

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Claude Opus 4.7 achieves the highest average range-level CHK-score across ranges (79.0% for detection and 65.7% for planning), followed by Claude Opus 4.6 (78.2%/58.0%), GLM-5.1 (76.3%/59.2%), and Qwen3.7 Plus (75.6%/58.8%), whereas Gemini 3.1 Pro, MiniMax M2.5, and Gemini 3 Flash present the lowest results.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 代理与传统无代理静态扫描器的能力维度比较

<div class="result-value" markdown="1">

传统扫描器在 ENT、VUL、BAS、PER 检测上的 CAP-score分别为 43.6%、50.0%、20.7%和2.1%；代理在四个可比较维度上平均更强，优势在持久化机制检测上尤其明显。代理还能关联分散文件证据、尝试重建攻击链并生成根因分析与修复计划，而扫描器只输出静态发现列表。

</div>

这项比较支持交互式推理和跨证据关联相对固定规则扫描具有增量价值，尤其适合发现不在显眼告警中的持久化。但双方功能边界并不对称：扫描器没有规划输出，且其知识库覆盖范围会直接影响得分，所以该结果不能证明代理应取代传统扫描器，更合理的含义是两者可互补。

<div class="result-source" markdown="1">

来源：§4.4 Finding 5；Table 5

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">We map the agentless-detection findings to our capability dimensions and observe that the scanner reaches 43.6% on ENT and 50.0% on VUL, but only 20.7% on BAS and 2.1% on PER.</span>

</details>

</article>

</div>

<div class="paper-boundary" markdown="1">

**这篇论文还没有解决什么**

- 评测采用 LLM-as-a-Judge。虽然三名强模型独立评分并取平均可降低单一裁判偏差，但所给节选没有提供人工专家一致性验证、误判分析、置信区间或统计显著性，因此模型间的小幅分差不宜过度解释。
- 基准仅含 10 个受入侵云主机靶场，且输入以离线磁盘快照和既有安全产品结果为主；它不能完整覆盖实时内存、持续网络流量、分布式多主机关联、修复命令真实执行风险及生产业务约束。技能实验也只说明通用流程先验在这些靶场上的效果，不能证明跨组织和跨攻击类型普遍有效。

</div>

<details class="paper-details" markdown="1">
<summary>查看 baseline、实验问题、消融与复现细节</summary>

**主要 baseline**

- 23 个前沿大语言模型，覆盖 8 个模型系列及多个连续版本；同系列版本比较用于判断事件响应能力是否随模型迭代稳定提升，不同系列比较用于检验通用模型排名能否迁移到真实取证与修复任务。
- 传统 agentless 生产扫描器：对同一磁盘快照执行基于预定义知识库的静态模式匹配，包括恶意样本签名、软件版本与 CVE、配置加固规则及敏感文件匹配。它是有意义的现实工作流基线，但只检测、不重建攻击链，也不生成修复建议，因此只可与代理的四个检测维度比较。
- 无程序性技能的原始代理：与加入安全事件响应团队所提炼通用流程技能的同一模型对照，用于隔离系统化调查流程、报告模板和修复模板的作用；技能明确排除了靶场真值、检查点、预期发现、恶意路径及 CVE 列表。
- 三名独立 LLM 裁判的联合评分：Claude Opus 4.7、Gemini 3.1 Pro 与 GPT-5.4 Pro 分别逐检查点评分，再取平均，以降低单一裁判偏差；这属于评测基准而非被测事件响应系统。

**实验想回答的问题**

- 在相同代理框架、输入和工具条件下，当前前沿大语言模型能否从受入侵主机的磁盘快照与安全告警中完整发现入侵、持久化、基线及漏洞风险，并给出正确、完整且经过验证的修复计划？
- 不同模型、攻击场景与能力维度之间的表现如何变化；传统无代理静态扫描和注入通用事件响应流程知识，分别能提供多大帮助？

**实验实现**

所有 23 个模型均由 OpenCode 代理框架驱动，接收相同的任务输入、指令提示和工具集；调用默认参数并开启推理，以控制代理框架差异。生成报告由三名专有模型在同一 OpenCode 框架中独立评分：裁判获得评分提示和带标准的检查点列表，并通过 bash 工具读取被测模型报告，逐检查点打分后取三者平均。随后分别聚合为靶场级 CHK-score和跨靶场、分能力的 CAP-score。节选未报告重复运行次数、随机种子、置信区间、显著性检验、推理成本或上下文长度控制。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 为 Claude Opus 4.7 注入不含靶场答案的通用程序性技能，对比无技能版本 | 持久化机制 PER 的 Detection CAP-score由68%升至88%，Planning CAP-score由49%升至75%，分别提高20和26个百分点。 | 该对照主要隔离“系统化调查与完整修复流程”这一程序先验，而不是额外攻击知识的作用。显著提升说明强模型的部分失败来自没有稳定执行全盘枚举、分阶段清理和验证流程；但技能来自实际产品经验，仍不能据此认定所有提升只由提示格式产生。 | §4.5；Figure 6<br><span class="experiment-evidence">For example, although Claude Opus 4.7 performs relatively weakly on persistence, the designed skill improves the PER CAP-score from 68% to 88% in Detection and from 49% to 75% in Planning.</span> |
| 加入相同通用程序性技能后，观察 GLM-5.1 在复杂靶场上的负向变化 | GLM-5.1 在 Shiro-Fastjson 上的检测下降12%，在 Docker-Escape 上下降11%，表明程序流程注入并不保证所有模型、所有场景受益。 | 这一负向结果用于检验技能是否具有普适增益。它提示固定流程可能增加无关搜索、分散模型注意力，或与模型原有策略冲突；因此技能应按模型和场景验证，而不能把流程模板视为无成本增强。作者只给出可能原因，节选不足以建立确定因果机制。 | §4.5；Figure 5<br><span class="experiment-evidence">GLM-5.1 degrades by 12% in detection on Shiro-Fastjson and by 11% on Docker-Escape.</span> |

**定性案例**

- 典型失败链条是：代理根据告警找到恶意进程或落地文件，并提出终止进程、删除文件等直接动作，但没有继续搜索 cron、systemd、shell 初始化文件或平台特定钩子中的静默持久化，也未轮换泄露凭据、阻断外联、验证恶意机制确已消失或确认业务服务仍健康。该案例解释了为何 Detection 普遍高于 Planning，以及 Investigation & Response Quality 和 PER 成为共同短板。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：The paper introduces a benchmark for evaluating tool-using LLM agents on post-compromise incident-response tasks.; rule check: matched taxonomy keywords; top rule score=4.0
- 全文指纹：`a36b1c515776bbe2c0991c339f7d23a1e3028e6ad80cc439482fb139998ac56d`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
