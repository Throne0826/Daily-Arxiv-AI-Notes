---
title: "arXiv 每日论文 · 2026-08-13"
description: "2026-08-13 筛选出的 18 篇 AI arXiv 新论文中文解读。"
---

# arXiv 每日论文：2026-08-13

<div class="daily-overview" markdown="1">

收录 **18** 篇不重复论文，形成 **40** 条分类记录。多标签论文会同时出现在所有相关方向中。

</div>

## LLM · 18 篇

<section class="daily-category-section" markdown="1">

### LLM Reasoning · 18 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [Towards Understanding On-Policy Distillation through the Lens of Test-Time Scaling](llm_alignment/towards-understanding-on-policy-distillation-through-the-lens-of-test-time-scaling.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11829</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文质疑“在策略蒸馏能把强教师的新推理能力传给学生”这一通行解释，并通过随采样预算 $K$ 增长而比较 $\mathrm{pass}@K$ 与 $\mathrm{avg}@K$，将其收益重新解释为主要提高正确推理路径的采样效率，而非稳定扩大学生模型的能力边界。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [OEIS Open: How many conjectures can language models turn into theorems?](llm_evaluation/oeis-open-how-many-conjectures-can-language-models-turn-into-theorems.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11941</span><span class="paper-category-chip">LLM 评测</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出以 Lean 形式化证明为判定标准的 OEIS Open 基准，用统一、可复现且较难受答案泄漏影响的评测，衡量通用语言模型能否自主证明或否证尚未解决的数学猜想。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [RealisticTritonBench: A Benchmark for Triton-Kernel Generation in Real-World AI Frameworks](llm_evaluation/realistictritonbench-a-benchmark-for-triton-kernel-generation-in-real-world-ai-frameworks.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.12004</span><span class="paper-category-chip">LLM 评测</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出 RealisticTritonBench，以真实 AI 框架中的 Triton 相关拉取请求为任务来源，并通过单元测试、模型精度测试和端到端性能测试，评估大语言模型在实际内核开发场景中的能力。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Chain-of-Thought Shows the Path to a Tree: Realizing Branching Complexity](llm_reasoning/chain-of-thought-shows-the-path-to-a-tree-realizing-branching-complexity.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11716</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文要把“线性步数的链式思维能够表达更强计算”这一抽象复杂度结论变成可检查的具体构造：先用小深度硬注意力 Transformer 显式实现图遍历，再以遍历为计算底座求树的 Strahler 数与宽度，并考察这些能力在树和 Dyck 路径两种表示之间能否迁移。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Claim-Level Reliability Assessment for Efficient Test-Time Reasoning](llm_reasoning/claim-level-reliability-assessment-for-efficient-test-time-reasoning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11994</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出免训练的声明级可靠性评估框架（CLR），把部分测试时计算从重复生成完整解答转向核验决定答案正确性的关键声明，再依据核验结果加权聚合候选答案。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [DexterSQL: Deep Schema Exploration and Rule-based Correction for Text-to-SQL Generation](llm_reasoning/dextersql-deep-schema-exploration-and-rule-based-correction-for-text-to-sql-generation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11889</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

DexterSQL面向无需微调的Text-to-SQL场景，试图通过深层模式探索、跨数据库纠错规则和基于句法结构的多路径生成，弥补提示式系统在列消歧、重复错误利用和复杂条件还原方面的不足。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Policy-as-logic for robust reasoning over rules](llm_reasoning/policy-as-logic-for-robust-reasoning-over-rules.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11905</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究如何把自然语言政策转化为可靠的自动决策：让大语言模型只负责从用户查询中提取事实，再由形式逻辑求解器依据政策规则推导结论，以降低输入扰动和生成随机性对结果的影响。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Reinforcing Step-level Reasoning for Effective Self-Correction in LLMs](llm_reasoning/reinforcing-step-level-reasoning-for-effective-self-correction-in-llms.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11573</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出两阶段框架 SFS-DPO：先强化小型大语言模型的逐步推理能力，再训练其在推理过程中识别并改正错误步骤，从而提升数学推理的可靠性。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Retrofitting Recurrent Depth into a Pretrained Language Model: Installation, Extrapolation, Transfer, and Retention at Two Parameter Budgets](llm_reasoning/retrofitting-recurrent-depth-into-a-pretrained-language-model-installation-extrapolation-transfer-an.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11233</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究能否在不从头训练、尽量保留原有通用能力的前提下，把预训练稠密语言模型改造成可反复调用同一组参数、在隐状态中逐步推理的循环深度模型。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [When Self-Consistency Backfires: Majority Vote Hurts the Majority of Hard Science Problems for Small LLMs](llm_reasoning/when-self-consistency-backfires-majority-vote-hurts-the-majority-of-hard-science-problems-for-small.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11403</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 评测</span></div>

<div class="daily-paper-summary" markdown="1">

本文发现，在GPQA Diamond高难度科学题上，对小型指令微调语言模型增加推理采样并进行多数投票，往往会强化模型稳定但错误的答案；同时，基于答案一致率或词元熵的廉价无验证器门控也无法可靠判断何时应采用投票。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [LEMUR: Latent Entropy-aware Multimodal Unlearning via Visual-anchored Reasoning Redirection](llm_safety/lemur-latent-entropy-aware-multimodal-unlearning-via-visual-anchored-reasoning-redirection.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11691</span><span class="paper-category-chip">LLM 安全</span><span class="paper-category-chip">知识编辑</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对强化学习后训练的多模态大推理模型会在思维链中泄露已要求遗忘的敏感事实这一新型隐私风险，提出利用逐词元熵变化定位泄露阶段并在解码时重定向推理轨迹的免训练遗忘框架 LEMUR。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Do LLMs Take Care of Their Own? Similarity Signals Can Induce Cooperation](multi_agent/do-llms-take-care-of-their-own-similarity-signals-can-induce-cooperation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.12125</span><span class="paper-category-chip">Multi-Agent</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究大语言模型智能体在战略互动中如何响应连续的相似度信号，并检验这种信号能否作为促进合作的机制，以及如何依据智能体的真实行为计算该信号。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Social Chain of Thought: A Multi-Agent Architecture Grounded in Medical Differential Diagnosis Methodology](multi_agent/social-chain-of-thought-a-multi-agent-architecture-grounded-in-medical-differential-diagnosis-method.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11420</span><span class="paper-category-chip">Multi-Agent</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出社会思维链（SCoT），以动态生成、角色条件化的医学专家智能体开展多轮协商，并检验这种社会化推理结构能否在复杂鉴别诊断中获得单体推理扩展难以复现的召回优势。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [GeoBridge: Decoupled Semantic Conditioning for Generative Image Geolocalization](multimodal_vlm/geobridge-decoupled-semantic-conditioning-for-generative-image-geolocalization.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11838</span><span class="paper-category-chip">多模态 VLM</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

GeoBridge研究的不是如何让多模态大语言模型提出更好的地点猜测，而是如何把其多粒度地理语义转换为适合连续球面坐标生成器的条件表示，并以角色解耦避免离散语义监督破坏该表示的几何结构。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [G0.5: One Autoregressive Stream for Robot Reasoning and Action](robotics/g0-5-one-autoregressive-stream-for-robot-reasoning-and-action.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11739</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究如何让视觉—语言—动作模型中的预训练视觉语言模型不再只是为外部动作专家提供条件，而是通过统一的自回归序列直接完成推理与机器人动作生成。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Glance, Scrutinize, and Think: Advancing Video Anomaly Detection from Training-Free to Agentic Reasoning](vlm_reasoning/glance-scrutinize-and-think-advancing-video-anomaly-detection-from-training-free-to-agentic-reasonin.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11260</span><span class="paper-category-chip">VLM Reasoning</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对视频异常检测中“能定位但不理解”与“能解释但定位不准”的能力割裂，探索统一的全局到局部推理范式，并分别提出无需训练的粗到细框架与可学习调用视频裁剪工具的智能体方法。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [SCOUT: Unlocking Enhanced Spatial Reasoning via Structured Chain-of-Thought and Multi-Objective Process Reward](vlm_reasoning/scout-unlocking-enhanced-spatial-reasoning-via-structured-chain-of-thought-and-multi-objective-proce.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.12220</span><span class="paper-category-chip">VLM Reasoning</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

SCOUT通过显式组织“空间感知—逻辑分析—答案生成”的推理过程，并用分阶段过程奖励训练视觉语言模型，以同时补足三维空间表征和中间推理信用分配能力。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Self-Evolving Code-with-Image Reasoning](vlm_reasoning/self-evolving-code-with-image-reasoning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11292</span><span class="paper-category-chip">VLM Reasoning</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究如何让多模态模型把无法靠目视或语言推理完成的像素级计算写成可执行程序，并通过反思、诊断和修复自身失败程序，在不更新模型权重的情况下积累可复用的视觉算法技能。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### LLM Agent · 2 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [Glance, Scrutinize, and Think: Advancing Video Anomaly Detection from Training-Free to Agentic Reasoning](vlm_reasoning/glance-scrutinize-and-think-advancing-video-anomaly-detection-from-training-free-to-agentic-reasonin.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11260</span><span class="paper-category-chip">VLM Reasoning</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对视频异常检测中“能定位但不理解”与“能解释但定位不准”的能力割裂，探索统一的全局到局部推理范式，并分别提出无需训练的粗到细框架与可学习调用视频裁剪工具的智能体方法。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Self-Evolving Code-with-Image Reasoning](vlm_reasoning/self-evolving-code-with-image-reasoning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11292</span><span class="paper-category-chip">VLM Reasoning</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究如何让多模态模型把无法靠目视或语言推理完成的像素级计算写成可执行程序，并通过反思、诊断和修复自身失败程序，在不更新模型权重的情况下积累可复用的视觉算法技能。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### Multi-Agent · 2 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [Do LLMs Take Care of Their Own? Similarity Signals Can Induce Cooperation](multi_agent/do-llms-take-care-of-their-own-similarity-signals-can-induce-cooperation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.12125</span><span class="paper-category-chip">Multi-Agent</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究大语言模型智能体在战略互动中如何响应连续的相似度信号，并检验这种信号能否作为促进合作的机制，以及如何依据智能体的真实行为计算该信号。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Social Chain of Thought: A Multi-Agent Architecture Grounded in Medical Differential Diagnosis Methodology](multi_agent/social-chain-of-thought-a-multi-agent-architecture-grounded-in-medical-differential-diagnosis-method.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11420</span><span class="paper-category-chip">Multi-Agent</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出社会思维链（SCoT），以动态生成、角色条件化的医学专家智能体开展多轮协商，并检验这种社会化推理结构能否在复杂鉴别诊断中获得单体推理扩展难以复现的召回优势。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### 对齐 / RLHF · 2 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [Towards Understanding On-Policy Distillation through the Lens of Test-Time Scaling](llm_alignment/towards-understanding-on-policy-distillation-through-the-lens-of-test-time-scaling.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11829</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文质疑“在策略蒸馏能把强教师的新推理能力传给学生”这一通行解释，并通过随采样预算 $K$ 增长而比较 $\mathrm{pass}@K$ 与 $\mathrm{avg}@K$，将其收益重新解释为主要提高正确推理路径的采样效率，而非稳定扩大学生模型的能力边界。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Reinforcing Step-level Reasoning for Effective Self-Correction in LLMs](llm_reasoning/reinforcing-step-level-reasoning-for-effective-self-correction-in-llms.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11573</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出两阶段框架 SFS-DPO：先强化小型大语言模型的逐步推理能力，再训练其在推理过程中识别并改正错误步骤，从而提升数学推理的可靠性。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### LLM 安全 · 1 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [LEMUR: Latent Entropy-aware Multimodal Unlearning via Visual-anchored Reasoning Redirection](llm_safety/lemur-latent-entropy-aware-multimodal-unlearning-via-visual-anchored-reasoning-redirection.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11691</span><span class="paper-category-chip">LLM 安全</span><span class="paper-category-chip">知识编辑</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对强化学习后训练的多模态大推理模型会在思维链中泄露已要求遗忘的敏感事实这一新型隐私风险，提出利用逐词元熵变化定位泄露阶段并在解码时重定向推理轨迹的免训练遗忘框架 LEMUR。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### LLM 评测 · 3 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [OEIS Open: How many conjectures can language models turn into theorems?](llm_evaluation/oeis-open-how-many-conjectures-can-language-models-turn-into-theorems.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11941</span><span class="paper-category-chip">LLM 评测</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出以 Lean 形式化证明为判定标准的 OEIS Open 基准，用统一、可复现且较难受答案泄漏影响的评测，衡量通用语言模型能否自主证明或否证尚未解决的数学猜想。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [RealisticTritonBench: A Benchmark for Triton-Kernel Generation in Real-World AI Frameworks](llm_evaluation/realistictritonbench-a-benchmark-for-triton-kernel-generation-in-real-world-ai-frameworks.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.12004</span><span class="paper-category-chip">LLM 评测</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出 RealisticTritonBench，以真实 AI 框架中的 Triton 相关拉取请求为任务来源，并通过单元测试、模型精度测试和端到端性能测试，评估大语言模型在实际内核开发场景中的能力。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [When Self-Consistency Backfires: Majority Vote Hurts the Majority of Hard Science Problems for Small LLMs](llm_reasoning/when-self-consistency-backfires-majority-vote-hurts-the-majority-of-hard-science-problems-for-small.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11403</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 评测</span></div>

<div class="daily-paper-summary" markdown="1">

本文发现，在GPQA Diamond高难度科学题上，对小型指令微调语言模型增加推理采样并进行多数投票，往往会强化模型稳定但错误的答案；同时，基于答案一致率或词元熵的廉价无验证器门控也无法可靠判断何时应采用投票。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### 知识编辑 · 1 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [LEMUR: Latent Entropy-aware Multimodal Unlearning via Visual-anchored Reasoning Redirection](llm_safety/lemur-latent-entropy-aware-multimodal-unlearning-via-visual-anchored-reasoning-redirection.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11691</span><span class="paper-category-chip">LLM 安全</span><span class="paper-category-chip">知识编辑</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对强化学习后训练的多模态大推理模型会在思维链中泄露已要求遗忘的敏感事实这一新型隐私风险，提出利用逐词元熵变化定位泄露阶段并在解码时重定向推理轨迹的免训练遗忘框架 LEMUR。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### LLM 其他 · 5 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [RealisticTritonBench: A Benchmark for Triton-Kernel Generation in Real-World AI Frameworks](llm_evaluation/realistictritonbench-a-benchmark-for-triton-kernel-generation-in-real-world-ai-frameworks.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.12004</span><span class="paper-category-chip">LLM 评测</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出 RealisticTritonBench，以真实 AI 框架中的 Triton 相关拉取请求为任务来源，并通过单元测试、模型精度测试和端到端性能测试，评估大语言模型在实际内核开发场景中的能力。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [DexterSQL: Deep Schema Exploration and Rule-based Correction for Text-to-SQL Generation](llm_reasoning/dextersql-deep-schema-exploration-and-rule-based-correction-for-text-to-sql-generation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11889</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

DexterSQL面向无需微调的Text-to-SQL场景，试图通过深层模式探索、跨数据库纠错规则和基于句法结构的多路径生成，弥补提示式系统在列消歧、重复错误利用和复杂条件还原方面的不足。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Reinforcing Step-level Reasoning for Effective Self-Correction in LLMs](llm_reasoning/reinforcing-step-level-reasoning-for-effective-self-correction-in-llms.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11573</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出两阶段框架 SFS-DPO：先强化小型大语言模型的逐步推理能力，再训练其在推理过程中识别并改正错误步骤，从而提升数学推理的可靠性。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [GeoBridge: Decoupled Semantic Conditioning for Generative Image Geolocalization](multimodal_vlm/geobridge-decoupled-semantic-conditioning-for-generative-image-geolocalization.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11838</span><span class="paper-category-chip">多模态 VLM</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

GeoBridge研究的不是如何让多模态大语言模型提出更好的地点猜测，而是如何把其多粒度地理语义转换为适合连续球面坐标生成器的条件表示，并以角色解耦避免离散语义监督破坏该表示的几何结构。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Glance, Scrutinize, and Think: Advancing Video Anomaly Detection from Training-Free to Agentic Reasoning](vlm_reasoning/glance-scrutinize-and-think-advancing-video-anomaly-detection-from-training-free-to-agentic-reasonin.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11260</span><span class="paper-category-chip">VLM Reasoning</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对视频异常检测中“能定位但不理解”与“能解释但定位不准”的能力割裂，探索统一的全局到局部推理范式，并分别提出无需训练的粗到细框架与可学习调用视频裁剪工具的智能体方法。

</div>

</article>

</div>

</section>

## 生成与多模态 · 4 篇

<section class="daily-category-section" markdown="1">

### 多模态 VLM · 2 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [GeoBridge: Decoupled Semantic Conditioning for Generative Image Geolocalization](multimodal_vlm/geobridge-decoupled-semantic-conditioning-for-generative-image-geolocalization.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11838</span><span class="paper-category-chip">多模态 VLM</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

GeoBridge研究的不是如何让多模态大语言模型提出更好的地点猜测，而是如何把其多粒度地理语义转换为适合连续球面坐标生成器的条件表示，并以角色解耦避免离散语义监督破坏该表示的几何结构。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [SCOUT: Unlocking Enhanced Spatial Reasoning via Structured Chain-of-Thought and Multi-Objective Process Reward](vlm_reasoning/scout-unlocking-enhanced-spatial-reasoning-via-structured-chain-of-thought-and-multi-objective-proce.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.12220</span><span class="paper-category-chip">VLM Reasoning</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

SCOUT通过显式组织“空间感知—逻辑分析—答案生成”的推理过程，并用分阶段过程奖励训练视觉语言模型，以同时补足三维空间表征和中间推理信用分配能力。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### VLM Reasoning · 3 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [Glance, Scrutinize, and Think: Advancing Video Anomaly Detection from Training-Free to Agentic Reasoning](vlm_reasoning/glance-scrutinize-and-think-advancing-video-anomaly-detection-from-training-free-to-agentic-reasonin.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11260</span><span class="paper-category-chip">VLM Reasoning</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对视频异常检测中“能定位但不理解”与“能解释但定位不准”的能力割裂，探索统一的全局到局部推理范式，并分别提出无需训练的粗到细框架与可学习调用视频裁剪工具的智能体方法。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [SCOUT: Unlocking Enhanced Spatial Reasoning via Structured Chain-of-Thought and Multi-Objective Process Reward](vlm_reasoning/scout-unlocking-enhanced-spatial-reasoning-via-structured-chain-of-thought-and-multi-objective-proce.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.12220</span><span class="paper-category-chip">VLM Reasoning</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

SCOUT通过显式组织“空间感知—逻辑分析—答案生成”的推理过程，并用分阶段过程奖励训练视觉语言模型，以同时补足三维空间表征和中间推理信用分配能力。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Self-Evolving Code-with-Image Reasoning](vlm_reasoning/self-evolving-code-with-image-reasoning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11292</span><span class="paper-category-chip">VLM Reasoning</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究如何让多模态模型把无法靠目视或语言推理完成的像素级计算写成可执行程序，并通过反思、诊断和修复自身失败程序，在不更新模型权重的情况下积累可复用的视觉算法技能。

</div>

</article>

</div>

</section>

## 决策与具身 · 1 篇

<section class="daily-category-section" markdown="1">

### 机器人 / 具身智能 · 1 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [G0.5: One Autoregressive Stream for Robot Reasoning and Action](robotics/g0-5-one-autoregressive-stream-for-robot-reasoning-and-action.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.11739</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究如何让视觉—语言—动作模型中的预训练视觉语言模型不再只是为外部动作专家提供条件，而是通过统一的自回归序列直接完成推理与机器人动作生成。

</div>

</article>

</div>

</section>
