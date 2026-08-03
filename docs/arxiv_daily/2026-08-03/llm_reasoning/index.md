---
title: "LLM Reasoning"
---

# LLM Reasoning

当日共 **12** 篇相关论文。多标签论文链接到其唯一正文页。

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [CMT-RAG: Complementary Memory Traces for Multi-turn Multi-hop RAG](../llm_agent/cmt-rag-complementary-memory-traces-for-multi-turn-multi-hop-rag.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.26470</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对多轮对话中需要跨轮复用中间推理与证据的多跳问答，提出以“子问题级推理轨迹”而非原始对话历史作为检索记忆，并通过 CMT-RAG 与 MuMu-QA 分别提供实现框架和评测基准。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Benchmarking LLM Competence on Logical Inference over Probability Operators](../llm_evaluation/benchmarking-llm-competence-on-logical-inference-over-probability-operators.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27405</span><span class="paper-category-chip">LLM 评测</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文旨在检验大语言模型能否依据底层逻辑稳定地处理含“可能”“很可能”“必然”等概率算子的自然语言推理，并通过控制逻辑形式、表面措辞与答案类别，揭示总体准确率可能掩盖的固定回答偏差。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [DRIP-R: A Benchmark for Decision-Making and Reasoning Under Real-World Policy Ambiguity in the Retail Domain](../llm_evaluation/drip-r-a-benchmark-for-decision-making-and-reasoning-under-real-world-policy-ambiguity-in-the-retail.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2605.07699</span><span class="paper-category-chip">LLM 评测</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

DRIP-R针对零售退货政策存在多种合理解释的现实情形，评估大语言模型智能体如何在动态对话中解释政策、权衡利益并作出决策。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Copy Less, Ground More: Overcoming Repetitive Copying in Long-Context Reasoning via Evidence-Aware Reinforcement Learning](copy-less-ground-more-overcoming-repetitive-copying-in-long-context-reasoning-via-evidence-aware-rei.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.19345</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">对齐 / RLHF</span></div>

<div class="daily-paper-summary" markdown="1">

本文将长上下文推理中的大段重复抄写诊断为证据定位不足，并提出证据感知奖励 GEAR，引导模型关注关键证据、避开无关上下文。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [How Hard Does It Think? Analyzing Step-Aware Reasoning Energy in LLM Chain-of-Thought Trajectories](how-hard-does-it-think-analyzing-step-aware-reasoning-energy-in-llm-chain-of-thought-trajectories.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28674</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 机制与可解释性</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出步感知推理能量（SARE），通过比较相邻 Transformer 层中思维链步骤的词元关系几何变化，刻画模型在每个推理步骤投入的内部计算努力，并研究该信号与语义阶段及推理失败的关系。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Metaphor-Induced Algorithmic Steering: Cross-Domain Procedural Transfer in LLM Code Generation](metaphor-induced-algorithmic-steering-cross-domain-procedural-transfer-in-llm-code-generation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28683</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究“隐喻诱导的算法转向”：看似无害且不直接指定算法的跨领域隐喻，可能把源领域的操作模式迁移到代码或 SQL 生成中，使大模型偏向正确但低效的实现。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [ThinkReset: Learnable Intermediate Interface Construction for Bounded-Context Long-Horizon Reasoning](thinkreset-learnable-intermediate-interface-construction-for-bounded-context-long-horizon-reasoning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28642</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文将固定上下文窗口中的长程推理重新界定为“可复用中间接口”的学习问题：模型应学习一种能够替代冗长历史并支持后续求解的文本状态，而非仅压缩或调度原有推理轨迹。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [To Add Is Machine, To Delete Is Human: Measuring and Mitigating Deletion Avoidance in LLM Code Editing](to-add-is-machine-to-delete-is-human-measuring-and-mitigating-deletion-avoidance-in-llm-code-editing.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28887</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 评测</span></div>

<div class="daily-paper-summary" markdown="1">

本文将“删除规避”界定为大语言模型在代码编辑中保留本应移除代码的系统性行为，并通过真实补丁分析、删除专用基准和训练试验，研究其表现、成因及缓解可能性。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [When Iterative RAG Beats Ideal Evidence: A Diagnostic Study in Scientific Multi-hop Question Answering](when-iterative-rag-beats-ideal-evidence-a-diagnostic-study-in-scientific-multi-hop-question-answerin.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2601.19827</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 评测</span></div>

<div class="daily-paper-summary" markdown="1">

本文通过统一控制的诊断实验，研究科学多跳问答中同步交替的检索与推理为何以及何时能够优于一次性提供全部标注证据的 Gold Context。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Implicit Reasoning for Large Language Model-based Generative Recommendation](../recommender/implicit-reasoning-for-large-language-model-based-generative-recommendation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2606.14142</span><span class="paper-category-chip">推荐系统</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文诊断了显式思维链难以有效服务于语义 ID 推荐的原因，并提出以可训练的 $\texttt{<pause>}$ token 进行隐式计算的 PauseRec，以更低成本连接语言知识与下一物品预测。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [SERPO: Self-Evolving Rubric Policy Optimization for Open-Ended Test-Time Reinforcement Learning](../reinforcement_learning/serpo-self-evolving-rubric-policy-optimization-for-open-ended-test-time-reinforcement-learning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.26873</span><span class="paper-category-chip">强化学习</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

SERPO旨在让语言模型在没有参考答案、人工反馈、外部奖励模型或更强评审器的开放式测试场景中，通过共同演化响应档案、查询专属评分准则与策略参数，自主构造持续有效的强化学习奖励。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Combining Large Language Models and Symbolic Reasoning for Multi-Robot Temporal Planning through Explainable Knowledge Bases](../robotics/combining-large-language-models-and-symbolic-reasoning-for-multi-robot-temporal-planning-through-exp.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2502.19135</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">Multi-Agent</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

PLANTOR探索一种混合式多机器人规划路线：让大语言模型把自然语言任务转写为可查询、可修正的Prolog知识库，再由符号组件负责正确性检查、规划与调度，以兼顾建模便利性和决策可解释性。

</div>

</article>

</div>
