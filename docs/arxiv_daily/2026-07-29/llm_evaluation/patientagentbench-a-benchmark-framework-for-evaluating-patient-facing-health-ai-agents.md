---
title: "[论文解读] PatientAgentBench: A Benchmark Framework for Evaluating Patient-Facing Health AI Agents"
description: "[arXiv 2607.25485][LLM 评测] PatientAgentBench面向患者侧医疗智能体，评估其在多轮对话中结合电子健康记录进行临床判断、调用工具完成医疗流程并守住安全边界的综合能力。"
arxiv_id: "2607.25485"
announcement_date: "2026-07-29"
primary_category: "llm_evaluation"
review_status: "ai_draft"
generator_model: "gpt-5.6-sol"
generated_at: "2026-07-30T07:32:03.770264+00:00"
source_sha256: "ca09b4dbaffd40b0925df9f71bb3c0ebe5f74ae19637a2a38f14db2b8495b940"
tags:
  - "LLM 评测"
  - "LLM Agent"
  - "面向患者的医疗智能体"
  - "智能体评测"
  - "多轮医疗对话"
  - "临床分诊"
  - "临床安全"
  - "电子健康记录"
  - "医疗工具调用"
  - "LLM-as-a-Jury"
---

<div class="paper-shell" markdown="1">

<p class="paper-eyebrow">LLM 评测 · arXiv 2607.25485</p>

# PatientAgentBench: A Benchmark Framework for Evaluating Patient-Facing Health AI Agents

<div class="paper-meta-row" markdown="1">

<span><strong>日榜</strong> 2026-07-29</span>
<span><strong>作者</strong> Korosh Vatanparvar, Ashutosh Joshi, Maria Xenochristou, Mohammad Abuzar Hashemi, Prasad Kasu, Deepak Bansal, Daniel Lopez-Martinez, Anchal Nema, Ramya Ganesan, Will Kimbrough, Alex Woody, Yadunandana Rao, Dilek Hakkani-Tur, Wilko Schulz-Mahlendorf</span>
<span><strong>通讯单位</strong> arXiv 元数据未标注</span>

</div>

<div class="paper-link-row" markdown="1">

[arXiv 原文](https://arxiv.org/abs/2607.25485v1) · [PDF 下载](https://arxiv.org/pdf/2607.25485v1) · **关键词** 面向患者的医疗智能体, 智能体评测, 多轮医疗对话, 临床分诊, 临床安全, 电子健康记录, 医疗工具调用, LLM-as-a-Jury  
**代码**: [https://github.com/amazon-science/PatientAgentBench](https://github.com/amazon-science/PatientAgentBench)  

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

PatientAgentBench面向患者侧医疗智能体，评估其在多轮对话中结合电子健康记录进行临床判断、调用工具完成医疗流程并守住安全边界的综合能力。

**不用术语来说**：一个医疗智能体即使正确预约了门诊或提交了续药请求，也可能没有先询问症状严重程度、检查药物相互作用或识别紧急风险，从而把“操作正确”变成“不安全的医疗行为”。因此，只用医学考试题或单次问答来测试模型，无法判断它在真实、持续且需要实际办事的患者对话中是否可靠。

</div>

<div class="paper-quickread__side" markdown="1">

<span class="paper-mini-label">核心贡献</span>

- 提出开放的患者侧医疗智能体基准：让被测基础模型在统一智能体框架中读取合成患者资料，与模拟患者开展任务导向的多轮对话，并通过有状态医疗工具沙箱执行预约、处方和转诊等工作流，从而联合考察临床推理与工具操作。
- 建立经临床人员参与校准的多维评价框架，以可复用规则同时衡量临床安全、分诊质量、工作流准确性、任务完成度、临床帮助性和对话质量，使评价不再局限于答案正确率或工具调用成功率。

</div>

</div>

<section class="paper-section paper-section--background" markdown="1">

## 研究背景

<div class="paper-section-deck" markdown="1">

本文属于面向患者的智能体式医疗人工智能评测。与只回答医学问题的模型不同，医疗智能体需要在持续多轮对话中读取患者的电子健康记录，判断症状严重程度及合适的照护级别，并调用预约、处方管理、远程医疗或转接临床人员等工具完成实际流程。由于同一个技术上正确的工具操作可能在不同病情、合并症或用药背景下产生完全不同的临床后果，评测不能只检查医学知识或调用参数，还必须同时考察分诊、临床安全、工作流准确性、任务完成情况、临床帮助性与对话质量。

</div>

<p class="paper-minor-label">小白先知道</p>

<div class="concept-list" markdown="1">

<div class="conceptitem" markdown="1">

**智能体式系统（agentic system）**

以基础模型为推理核心，并配备工具调用与状态管理机制，使其不只生成回答，还能执行预约、处方管理或升级至临床人员等多步操作。本文中的被测模型统一封装在智能体框架内，以便比较模型在相同工具环境中的表现。

</div>
<div class="conceptitem" markdown="1">

**电子健康记录（Electronic Health Record, EHR）**

包含患者人口统计特征、既往疾病、合并症、用药及其他临床信息的数字化记录。智能体必须结合这些信息判断某项操作是否适合当前患者，而不能脱离个体背景机械执行请求。

</div>
<div class="conceptitem" markdown="1">

**临床分诊（triage）**

根据症状严重程度和风险因素决定患者所需照护级别，例如常规预约、紧急远程问诊或立即升级处理。它不同于直接作出确诊，重点是及时识别危险信号并把患者引导到安全的下一步。

</div>

</div>

<div class="paper-focus" markdown="1">

**论文具体研究什么**

评测对象是面向患者的医疗智能体：基础模型被置于统一的智能体框架中，可访问带状态的医疗工具沙箱，并与具有合成人物设定和健康记录的模拟患者进行任务导向、多轮对话。输入包括患者提出的行政或医疗需求、患者画像与EHR、历史对话以及工具返回结果；智能体需要追问必要信息、结合合并症和多重用药进行临床推理、选择是否调用工具，并在超出安全边界时升级至专业人员。输出不是单个答案，而是完整对话轨迹及工具操作轨迹；随后由基于临床准则的LLM评审组按六个维度评分。该设置假定智能体可以提供一般健康教育并协助流程，但个体化临床判断需要适当监督，确定性诊断和最终临床决策应保留给持证临床人员。

</div>

<details class="paper-details" markdown="1">
<summary>查看符号与相关工作</summary>

**必要符号**

原文未明确报告，或这里不需要额外前置概念。

**直接相关的工作**

- **MedQA及其他孤立式医学问答基准（Jin et al., 2021；Singhal et al., 2025）**: 这类工作主要用单轮或静态问题检验医学知识，不能观察智能体在长期对话中结合患者记录、选择照护级别并执行工具流程时产生的安全问题；本文据此把评测单位从单个答案扩展为完整的患者—智能体交互轨迹。
- **临床人员使用EHR的智能体基准（Jiang et al., 2025；Lee et al., 2025）**: 相关基准包含较丰富的合成病历或EHR操作，但面向临床人员执行医嘱、记录等任务，而非患者发起的多样化需求。PatientAgentBench关注患者视角下行政请求与复杂医疗问题的结合，以及工具调用、患者复杂性和临床安全之间的相互作用。

</details>

</section>

<section class="paper-section paper-section--motivation" markdown="1">

## 研究动机

<div class="paper-section-deck" markdown="1">

患者侧健康智能体正从提供信息转向代表患者执行预约、处方管理、远程问诊发起、照护协调和升级转诊等操作。此类系统会直接影响就医路径，因而可能产生与基层医疗相似的风险，包括遗漏紧急症状、用药不安全、转诊或检查后随访不足，以及在缺少专业监督时给出个体化临床判断。随着智能体自主性提高，需要一种能够在接近真实患者情境下暴露这些风险的评价机制。

</div>

<div class="paper-two-column" markdown="1">

<div markdown="1">

<span class="paper-mini-label">过去怎么做</span>

- **静态医学知识与对话问答基准**：主要通过单轮问题、考试式题目或少量短轮次交流，检查模型能否回忆医学知识、回答健康问题或完成诊断对话；部分长对话基准只覆盖心理治疗等较窄场景。
- **工具调用与医疗工作流基准**：通过预设任务检查智能体能否选择工具、填写参数并完成操作；现有医疗版本多面向临床人员使用电子健康记录的流程，其他通用智能体基准则集中于零售、航空和电信等非医疗场景。

</div>

<div markdown="1">

<span class="paper-mini-label">问题出在哪里</span>

- 静态问答把医学知识正确性近似为临床可靠性，却无法观察模型在持续对话中是否主动收集关键信息、结合合并症与多重用药判断严重程度并适时升级处理；其后果是模型可能在考试题上表现良好，却在真实决策链中遗漏安全步骤。
- 现有工具基准通常把工作流是否完成作为核心结果，未充分评价行动选择的临床合理性与安全边界。两个智能体可能都正确调用预约工具，但其中一个未做严重程度筛查便执行操作；仅看工具参数和任务成功率会把这种潜在危险误判为成功。

</div>

</div>

<div class="motivation-core" markdown="1">

<div markdown="1"><span>研究空白</span>

此前缺少一个统一基准，能够在患者发起的多样化医疗任务中，把多轮交互、复杂患者记录、临床推理、有状态工具执行和临床安全评价放入同一测试过程；也缺少对主流基础模型在这些联合维度上的系统比较，以及对“提供一般健康教育、作出需专业监督的个体化判断、给出应由执业人员负责的确定性诊断”三类行为边界的综合检查。

</div>
<div markdown="1"><span>核心问题</span>

当基础模型被封装为可读取患者健康记录并调用医疗工具的智能体后，它能否在患者侧多轮任务中既完成工作流，又正确分诊、遵守临床安全边界并保持有帮助且适当的沟通；不同模型在这些能力上的缺口能否被一致、可复现且与临床人员判断对齐的评价框架识别出来？

</div>
<div markdown="1"><span>作者直觉</span>

作者的切入点是把评价单位从孤立答案或单次工具调用提升为完整会话轨迹。模拟患者提供动态信息，健康记录提供合并症和用药背景，有状态沙箱记录智能体实际做了什么，而临床规则从多个维度评价它为何行动、行动前是否充分筛查以及何时转交真人。这样，评价不仅能发现“工具有没有用对”，还能够发现“本来就不该立即执行该操作”这类只有结合上下文才会显现的问题。

</div>

</div>

</section>

<section class="paper-section paper-section--method" markdown="1">

## 研究方法

<div class="paper-section-deck" markdown="1">

PatientAgentBench不是训练新模型的方法，而是一套端到端评测框架：将待测基础模型放入统一的患者服务智能体外壳，使其在最长15轮的对话中读取结构化电子健康记录、询问患者需求，并调用沙箱工具完成预约、处方、远程医疗或资料管理任务。患者侧由另一个模型根据隐藏的患者故事、任务和性格生成回复；待测智能体只能看到患者档案与已经说出的内容，因此必须通过对话主动获取症状、严重程度和真实意图。框架保存自然语言消息、工具调用、工具返回值及智能体内部调用链，形成完整会话轨迹。

</div>

<p class="paper-minor-label">关键流程</p>

<div class="method-steps" markdown="1">

<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 构造场景并初始化双智能体

框架将患者故事、任务和性格仅提供给用户智能体，将结构化患者档案提供给助手智能体；助手不知道隐藏任务，所有待测模型均使用相同的基础智能体外壳和工具环境。

<div class="method-step__io" markdown="1">

**输入**：一个基准场景，包括结构化患者档案、患者故事、待完成任务、患者性格、当前时间，以及统一的智能体系统提示和医疗工具定义。  
**输出**：一个信息非对称的患者—助手交互环境。

</div>

**直观理解**：这类似真实问诊：患者知道自己为何来访，而助手只看到病历，必须通过提问弄清患者真正需要什么，不能直接偷看标准任务。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### 生成患者开场与后续回应

用户智能体依据角色设定生成开场消息，随后只根据助手的可见回复继续对话；当其判断请求已经解决且没有追问时，输出预定义终止信号。

<div class="method-step__io" markdown="1">

**输入**：隐藏的患者故事、任务、性格，以及助手上一轮对患者可见的最终回复。  
**输出**：符合场景设定的患者消息，或会话终止信号。

</div>

**直观理解**：患者模拟器不是静态题目，而会根据助手的提问和处理结果改变下一句话，从而检验助手能否持续沟通并补齐信息。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### ReAct推理与医疗工具执行

基于LangGraph与LangChain实现的ReAct助手判断下一步行动，可连续调用一个或多个沙箱工具并读取返回结果，然后生成面向患者的最终回复；该循环最多持续15轮。

<div class="method-step__io" markdown="1">

**输入**：完整可见对话历史、结构化患者档案、当前时间、系统提示和沙箱工具描述。  
**输出**：助手回复、工具调用及返回结果，以及包含中间调用链的完整会话轨迹。

</div>

**直观理解**：助手既要“想清楚”是否需要追问或分诊，也要“做正确”预约、处方等操作；只说已经完成但没有真正调用工具，会在轨迹中暴露。

</div>

</div>
<div class="method-step" markdown="1">

<div class="method-step__body" markdown="1">

#### LLM-as-a-Jury多维评分

两个前沿评审模型Claude Opus 4.8与GPT-5.5分别依据六个临床人员奠定的量表维度给出1至5分及简短理由，并各自计算加权综合分；框架再对两名评审的逐维分数和综合分取平均，平均分不低于3视为该维度通过。

<div class="method-step__io" markdown="1">

**输入**：去除待测模型身份标签的完整会话轨迹，包括患者资料、对话、工具调用和工具结果。  
**输出**：六维评审分数、综合分、逐项通过状态、评审解释，以及评审间标准差和通过一致性。

</div>

**直观理解**：它相当于让两位独立阅卷者同时检查“事情是否办成、流程是否真实、医疗上是否安全、是否正确分诊、是否有帮助、沟通是否合适”，避免只凭任务完成率判断。

</div>

</div>

</div>

<p class="paper-minor-label">真正需要看懂的公式</p>

<div class="equation-block" markdown="1">

#### 单个评审模型的加权量表综合分

$$
A_k=\frac{\sum_{d=1}^{6} w_d s_{k,d}}{\sum_{d=1}^{6} w_d}
$$

**符号说明**

- $A_k$：第k个评审模型针对一段会话计算的加权综合分。
- $k$：评审模型索引；论文实验中共有K=2个评审模型。
- $d$：六个评分维度的索引。
- $s_{k,d}$：第k个评审在第d个维度给出的1至5分。
- $w_d$：第d个维度的临床重要性权重；权重由临床团队讨论确定，所给节选未列出具体数值。

<div class="equation-explanation" markdown="1">

**直观理解**：先由每个评审分别把六项分数按临床重要性合成一个总分。该总分便于排列模型，但作者明确指出它不是安全门槛，某个危险维度的低分不会被强制转化为整体失败。  
**原文位置**：第4.1节，Equation 1；所给节选仅保留该公式的文字说明，未展示原始公式排版及具体权重。

</div>

</div>

<div class="equation-block" markdown="1">

#### 评审团平均分与维度通过判定

$$
\bar{s}_d=\frac{1}{K}\sum_{k=1}^{K}s_{k,d},\qquad \bar{A}=\frac{1}{K}\sum_{k=1}^{K}A_k,\qquad \operatorname{Pass}_d=\mathbb{I}[\bar{s}_d\ge 3]
$$

**符号说明**

- $\bar{s}_d$：评审团在第d个维度上的平均分。
- $\bar{A}$：各评审加权综合分的平均值，即最终报告的综合分。
- $K$：评审模型数量；实验设置为2。
- $\operatorname{Pass}_d$：第d个维度是否通过的二值指标。
- $\mathbb{I}[\cdot]$：指示函数：括号内条件成立时取1，否则取0。

<div class="equation-explanation" markdown="1">

**直观理解**：框架先让评审独立打分，再对同一维度取平均；平均分达到3即判定该维度通过。作者还实现了多数投票，但为保留模型之间更细的分数差异，正式实验采用分数平均。  
**原文位置**：第4.1节及Figure 4；公式为原文所述jury averaging与通过阈值的数学表达。

</div>

</div>

<div class="paper-focus" markdown="1">

**优化目标如何起作用**：不适用。PatientAgentBench是评测框架，不使用基准会话或评审分数更新待测基础模型参数，也未定义用于训练被测模型的损失函数；综合分和逐维分用于比较、诊断及指导后续智能体设计。用户智能体、助手智能体与评审模型均以推理方式运行。

</div>

<details class="paper-details" markdown="1">
<summary>查看关键模块、训练与复现补充</summary>

**关键模块**

**1. 双智能体多轮会话环境**

环境由隐藏场景信息的用户智能体和作为被测系统的助手智能体组成。助手只能访问结构化患者记录而不能访问患者故事、底层任务或性格；用户智能体只能看到助手最终回复，看不到其内部推理和工具调用链。

> 直观理解：这种权限隔离防止助手直接读取答案，也防止患者模拟器根据助手的隐藏思考配合演出，使评测更接近真实患者服务。

**2. 统一ReAct助手外壳与医疗沙箱**

所有基础模型共享固定的通用智能体脚手架、系统提示和工具定义。系统提示规定患者中心沟通、重要操作前确认、紧急情况升级、必要时澄清，并禁止确定性诊断、未经医护人员批准停药及淡化严重症状；工具覆盖预约、处方、远程医疗和患者资料管理。

> 直观理解：统一外壳控制了提示工程和工具条件，使模型差异更能归因于基础模型能力；沙箱则让错误操作可检查，又不会触及真实医疗系统。

**3. 临床量表驱动的LLM评审团**

评审团依据六个维度独立检查整段会话，而非只比较最终答案。论文采用两个与临床判断对齐较好的强评审模型，并保留每个评审的分数和理由；综合分只用于单轴排序，不被定义为安全准入门槛，安全、流程和分诊等维度仍需分别检查。

> 直观理解：医疗任务可能出现“预约办对了但没有发现急症”的情况，因此必须把操作正确性与临床判断拆开评分；综合平均分不能掩盖某个致命短板。

**训练与推理**

评测推理时，框架为每个场景加载患者档案、隐藏故事、任务和性格，并以统一外壳实例化待测助手。用户智能体先生成开场，助手在每轮读取全部可见历史和患者档案，通过ReAct决定是否调用工具及如何回复；用户智能体再依据可见回复继续交流，直至输出终止信号或达到15轮。全过程被记录为含工具调用和结果的轨迹。随后，两个匿名化评审模型分别对每条轨迹的六个维度评分并说明理由，框架计算每名评审的加权综合分，再跨评审平均并按3分阈值生成逐维通过状态。自动评审的可信度通过持证临床人员对75条分层抽样会话的盲评进行验证，而不是通过额外训练评审模型获得。

**复现信息**

助手ReAct外壳使用LangGraph和LangChain实现；所有待测模型共享系统提示、工具说明、医疗沙箱、1,200个场景和评分量表，且不加入少样本示例、思维链脚手架或模型专属优化。实验评审团固定为Claude Opus 4.8与GPT-5.5；作者称加入较弱评审模型会降低与临床判断的对齐，因此选择评审质量而非扩大评审团规模。轨迹提交评审时隐藏待测模型身份，同时保存单个评审结果，以便检查评审偏差和开展错误类型分析。

</details>

</section>

<section class="paper-section paper-section--experiments" markdown="1">

## 实验

<div class="paper-setup-grid" markdown="1">

<div markdown="1"><span class="paper-mini-label">数据与任务</span>- 核心基准包含1,200个患者端医疗场景；10个模型在同一批场景上运行，以控制任务差异。每次评测输入包括患者消息、智能体回复、工具调用及返回结果；评审模型额外获得完整患者档案和底层场景真值，用于判断智能体是否在行动前收集了足够信息。原文节选未明确报告训练集、验证集或测试集划分。
- 临床一致性验证集由核心基准中分层抽取的75段对话构成，覆盖不同被测模型、六个评分维度和1—5分范围，并优先纳入Fail与Excellent等极端样本。8名持证临床人员分为临床轨和运营轨，每段对话的每个维度获得2—4份人工标注，总计约500个维度级评分。
- 评测标准本身由六个维度、30个子维度和102条经临床审核的通用准则组成。它不是传统意义上的独立数据集，而是所有场景共享的评分资源；其作用是在没有逐场景标准答案的条件下，根据患者档案、对话上下文和工具轨迹评价任务完成、临床安全、工作流准确性、分诊质量、临床帮助性和对话质量。</div>
<div markdown="1"><span class="paper-mini-label">指标怎么看</span><div class="metric-list" markdown="1">

<div class="metricitem" markdown="1">

**六维度评分及通过率**

每段对话在六个维度上分别取得1—5分，1表示Fail、5表示Excellent；评审团平均分不低于3视为通过。该指标既衡量基本可接受性，也保留通过线以上的质量差异。所有维度应用于所有对话，即使请求表面上只是行政事务，也仍检查潜在临床风险。 （分数和通过率越高越好，因为表示更多对话达到患者端医疗交互的最低可接受标准；但单项低分不能被总体均分替代，临床安全、分诊和工作流仍需单独检查。）

</div>
<div class="metricitem" markdown="1">

**加权综合分**

综合分按 \(\mathrm{Aggregate\ Score}=\frac{\sum_{i=1}^{6}w_i s_i}{\sum_{i=1}^{6}w_i}\) 计算，其中 \(s_i\) 是第i个维度的1—5分，\(w_i\) 是其权重。默认权重依次强调临床安全2.0、工作流准确性1.6、分诊质量1.4、临床帮助性1.4、任务完成1.0和对话质量0.9，总权重为8.3。它用于单轴排序，而不是安全准入门槛。 （越高越好，因为表示经临床风险重要性加权后的整体表现更强；但高综合分不证明不存在低频严重安全事故。）

</div>
<div class="metricitem" markdown="1">

**相邻一致率**

LLM评审团平均分与持证临床人员平均分之差不超过±1的对话比例。该指标适合1—5级有序量表，因为相差一级通常比完全相同分数更能反映具有临床意义的近似一致。 （越高越好，因为表示自动评审更接近专家判断；不过它允许一分误差，因此不等同于精确一致，也不能单独证明所有失败类型都被可靠识别。）

</div>

</div></div>

</div>

<p class="paper-minor-label">最重要的实验结果</p>

<div class="result-list" markdown="1">

<article class="result-item" markdown="1">

<span class="result-index">01</span>

#### LLM评审团与持证临床人员在75段分层抽样对话上的一致性验证

<div class="result-value" markdown="1">

六个维度上，LLM评审团与专家评分的相邻一致率达到79%—93%；作者据此主张自动评审与临床判断的对齐程度可比或高于临床人员之间的一致性。

</div>

这说明由两个强评审模型给出的分数通常不会偏离临床人员平均分超过一级，为大规模自动评测提供了经验依据。但相邻一致率容许±1分误差，且验证样本只有75段、经过分层并优先选择极端分数，因此不能据此认定评审团可在所有临床领域或罕见风险上替代专家。

<div class="result-source" markdown="1">

来源：Abstract；临床标注设计见Section 4.2 Clinician Alignment Validation

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">To validate alignment, licensed clinicians annotated shared conversations, yielding 79-93% adjacent agreement between jury and expert raters, on par with or exceeding clinician inter-rater agreement.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">02</span>

#### 10个模型在相同1,200个患者端智能体场景上的分诊质量比较

<div class="result-value" markdown="1">

分诊质量是最能区分模型能力的维度：最弱模型的通过率为32%，最强模型达到88%。作者观察到，常见失败是智能体把请求视为单纯行政事务并直接行动，没有先筛查可能改变处置方式的症状或风险。

</div>

56个百分点的跨度表明，能否在执行预约等操作前主动询问关键症状，是模型能力差异的重要来源。即使最强模型仍有约12%的场景未达到分诊通过线，也说明更强的通用模型尚未消除患者端风险。该结果比较的是该基准中的通过率，不直接等价于真实临床环境中的诊断准确率或患者结局改善。

<div class="result-source" markdown="1">

来源：Abstract

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Triage quality is the most discriminating dimension: pass rates rise from 32% for the weakest models to 88% for the strongest, with agents often acting on administrative requests without clinical screening.</span>

</details>

</article>
<article class="result-item" markdown="1">

<span class="result-index">03</span>

#### 相同1,200场景上的临床安全、工作流准确性与总体表现

<div class="result-value" markdown="1">

临床安全和工作流准确性呈现与分诊相同的能力梯度：较弱模型经常失败并虚构未实际执行的操作，而前沿模型仅在1%—3%的案例中失败；尽管如此，最强模型的总体综合分仍只有4.25/5。

</div>

工具轨迹让评测能够识别“口头说已完成、实际上没有调用工具”的执行幻觉，这是只看最终回答的静态基准难以发现的。1%—3%的失败率说明前沿模型显著减少了错误，却并非零风险；4.25分也表示整体质量较高但仍未达到满分。由于综合分是加权平均，它不能证明每个关键安全维度都达到部署要求。

<div class="result-source" markdown="1">

来源：Abstract；综合分4.25/5另见Abstract末段

</div>

<details class="result-evidence" markdown="1">
<summary>核对原文证据</summary>

<span class="experiment-evidence">Clinical safety and workflow accuracy follow the same pattern: the weakest models fail often, fabricating unexecuted actions, while frontier models fail on only 1-3% of cases, from unverified tool outputs and omitted crisis resources in an emergency.</span>

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

- 同一1,200场景上的10个被测模型，来自四个模型家族；统一场景使模型间差异更可能来自智能体能力而非测试样本难度。所给节选未列出各模型名称及具体版本，因此不能逐一报告。
- HealthBench：面向患者的固定健康问答基准，以准确性、完整性、沟通和安全等案例特定标准评分；它用于对照说明静态问答无法检验持续对话、患者记录推理和工具执行。
- MedAgentBench：面向临床人员的EHR任务基准，提供有状态FHIR API沙箱并评价任务成功与动作准确性；它是工具型医疗智能体的重要对照，但目标用户并非患者。
- MedSafetyBench：包含1,800个患者侧对抗安全样本，以安全拒答和越狱抵抗为主；它能测试局部安全行为，但不能覆盖常规患者请求中潜藏的分诊和工作流风险。

**实验想回答的问题**

- 在持续多轮、可读取患者记录并调用医疗工具的真实工作流中，不同基础模型驱动的患者端智能体能否安全、准确地完成任务，尤其能否做好临床分诊、风险升级和工具执行？
- 由两个前沿模型组成的LLM评审团是否与持证临床人员的判断足够一致，从而可作为六维度、大规模自动评测的可信替代方案？

**实验实现**

每个基础模型被包装为可调用医疗工具的智能体，与模拟患者进行持续多轮交互。完整轨迹包含用户消息、智能体回复、工具调用及工具结果；评审者因而能够核验某项操作是否真正执行，而不只看智能体是否口头声称完成。评测采用LLM-as-a-Jury：Claude Opus 4.8与GPT-5.5独立依据同一套102条准则为六个维度评分，并分别计算加权综合分；最终对两个评审者的维度分和综合分取平均。被测模型身份对评审者隐藏，以降低身份偏差，评审解释和单评审结果则被保留以供事后分析。临床验证中，人工界面同样隐藏模型身份和LLM评分；标注者先经过三轮留出对话校准，再独立评价目标样本。原文节选未明确报告智能体提示词、工具清单的完整内容、采样参数、运行次数、统计显著性检验或置信区间。

**关键消融**

| 对比 / 设置 | 结果 | 怎么理解 | 原文位置与证据 |
|---|---|---|---|
| 评审团规模与评审模型质量：两个强评审模型对比更大、更多样但包含较弱模型的评审团 | 作者报告，加入较弱评审模型会降低与临床判断的一致性；由Claude Opus 4.8和GPT-5.5组成的两模型评审团获得最高总体一致性，因此正式实验选择评审质量而非评审数量。原文未明确报告各评审团配置的具体一致率或差值。 | 这一分析隔离的是“评审者数量”与“评审者能力”的影响：更多投票者并不必然更可靠，低质量评审可能稀释强评审对临床风险的判断。不过缺少逐配置数值、置信区间和显著性检验，因此只能支持定性设计选择，不能量化两模型配置的优势大小。 | Section 4.1 Scoring and Aggregation<br><span class="experiment-evidence">We also explored larger and more diverse juries, but found that weaker evaluator models aligned poorly with clinician judgment and diluted the panel’s accuracy; restricting the jury to two strong, well-aligned models gave the highest overall agreement with clinician scores, so we favored evaluator quality and alignment over jury size.</span> |

**定性案例**

- 代表性失败模式是：智能体面对表面上的行政请求时未先进行临床筛查便执行操作；另有系统声称某项操作已经完成，但工具轨迹显示并未实际执行。前沿模型仍出现未核验工具输出，以及在紧急心理健康情境中遗漏危机求助资源的案例。作者将这些现象视为持续多轮、工具使用评测的必要性证据；分析上，它们说明患者端智能体的风险不仅来自医学知识错误，也来自信息收集不足、执行状态不真实和升级流程缺失。

</details>

</section>

<details class="auto-review" markdown="1">
<summary>生成与校验信息</summary>

- 状态：`ai_draft`
- 分类理由：提出并经临床专家验证了一个用于评测持续对话、医疗工具调用型患者端 LLM Agent 的基准框架。; rule check: matched taxonomy keywords; top rule score=3.0
- 全文指纹：`ca09b4dbaffd40b0925df9f71bb3c0ebe5f74ae19637a2a38f14db2b8495b940`
- 注意：本页由 AI 辅助生成；数值、baseline、公式和相关工作必须对照原文复核。

</details>

</div>
