---
title: "对齐 / RLHF"
---

# 对齐 / RLHF

当日共 **9** 篇相关论文。多标签论文链接到其唯一正文页。

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [Don't Peek at the Answer: Outcome-Masked Group Relative Policy Optimization for Label-Free RLVR](don-t-peek-at-the-answer-outcome-masked-group-relative-policy-optimization-for-label-free-rlvr.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.03119</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">强化学习</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出 OM-GRPO，通过在保留答案层面共识奖励的同时屏蔽答案片段的梯度更新，将无标签强化学习中的优化压力转移到推理轨迹，并利用成对比较增强奖励估计，以缓解投票式训练中的奖励投机与模式坍塌。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Hi-TTRL: Regulating Consensus with Hints for Test-Time Reinforcement Learning](hi-ttrl-regulating-consensus-with-hints-for-test-time-reinforcement-learning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.03545</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

Hi-TTRL针对无标签测试时强化学习中“低共识导致错误多数被放大、高共识导致学习信号消失”的两难，在多数投票前用自适应生成的前缀提示调节采样共识，使伪标签可靠性与策略更新强度取得更稳定的平衡。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [PAMT: Process-Aligned Reinforcement Learning for Multi-Domain Machine Translation](pamt-process-aligned-reinforcement-learning-for-multi-domain-machine-translation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.03077</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

本文指出多领域机器翻译中的显式推理虽能帮助处理长文本和高难度输入，却可能造成术语与风格偏移，并据此提出通过步骤级奖励对齐翻译决策与最终译文的PAMT框架。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [ReflectRL: Learning from Golden Negative Trajectories via Reflective-to-Direct Reasoning](reflectrl-learning-from-golden-negative-trajectories-via-reflective-to-direct-reasoning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.03972</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出 ReflectRL：不再丢弃强专家模型生成的错误推理轨迹，而是让目标模型先识别并修正其中的局部错误，再把这种反思能力迁移到不依赖专家轨迹的直接推理中。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [SFT Conflicts, RL Coexists: A Theoretical and Empirical Analysis of Multi-Task Learning for LLMs](sft-conflicts-rl-coexists-a-theoretical-and-empirical-analysis-of-multi-task-learning-for-llms.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.03573</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">强化学习</span></div>

<div class="daily-paper-summary" markdown="1">

本文围绕多任务推理训练中的“SFT 冲突、RL 共存”现象，解释监督微调为何在多阶段训练中发生任务间破坏，而强化学习为何能以近似正交的参数更新累积不同任务能力，并据此提出可并行训练后合并更新的 Parallel-RL。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [BODHI: Do LLMs Branch Out and Discover Heterogeneous Inferences?](../llm_reasoning/bodhi-do-llms-branch-out-and-discover-heterogeneous-inferences.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.02867</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">强化学习</span></div>

<div class="daily-paper-summary" markdown="1">

本文追问RLVR带来的推理性能提升究竟源于能力边界扩展，还是源于将采样集中到少数轨迹，并通过迷宫与按语义等价关系构造的BODHI-Tree区分表面措辞多样性和真正的推理分支。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [CVPO: Enhancing LLM Reinforcement Learning Reasoning via Value-Variance Adaptation and Dynamic Curriculum Learning](../llm_reasoning/cvpo-enhancing-llm-reinforcement-learning-reasoning-via-value-variance-adaptation-and-dynamic-curric.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.03068</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">强化学习</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对大语言模型数学推理的价值模型强化学习，提出同时利用轨迹内价值方差细化优势权重、并随模型能力动态调整题目权重的 CVPO，以改善探索、信用分配与难度漂移问题。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [CausalOPD: First-Wrong-Step Supervision for Distilling Causal Chain Reasoning](../llm_reasoning/causalopd-first-wrong-step-supervision-for-distilling-causal-chain-reasoning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.03673</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

CausalOPD面向具有前后依赖关系的因果推理，通过显式领域知识定位学生推理中最早可验证的错误，并按因果阶段对错误后缀进行局部在线优化。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [DiagLoop: A Counterfactual Data Flywheel with Stage-Localized Reinforcement for Diagnostic LLMs](../llm_reasoning/diagloop-a-counterfactual-data-flywheel-with-stage-localized-reinforcement-for-diagnostic-llms.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2608.03674</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">对齐 / RLHF</span></div>

<div class="daily-paper-summary" markdown="1">

DiagLoop旨在把一次编写的物理关系或临床指南转化为经过机制校验的反事实训练场景，并依据模型最早出错的诊断阶段定向生成数据和实施局部强化学习，从而训练可本地部署、推理路径可核查的诊断大模型。

</div>

</article>

</div>
