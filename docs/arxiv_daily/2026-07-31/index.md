---
title: "arXiv 每日论文 · 2026-07-31"
description: "2026-07-31 筛选出的 50 篇 AI arXiv 新论文中文解读。"
---

# arXiv 每日论文：2026-07-31

<div class="daily-overview" markdown="1">

收录 **50** 篇不重复论文，形成 **79** 条分类记录。多标签论文会同时出现在所有相关方向中。

</div>

## LLM · 25 篇

<section class="daily-category-section" markdown="1">

### LLM Reasoning · 3 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [ReDiPPO: Reference-Guided Value Calibration and Discrepancy-Aware Token Reweighting for Mathematical Reasoning](llm_alignment/redippo-reference-guided-value-calibration-and-discrepancy-aware-token-reweighting-for-mathematical.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27631</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">强化学习</span></div>

<div class="daily-paper-summary" markdown="1">

ReDiPPO利用仅在训练期提供给评论器的参考答案校准中间状态价值，并依据参考引导评论器与标准评论器的分歧调整逐词元优势权重，以改善数学推理中的信用分配。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [SVR: Self-Verifying Refinement via Joint Verdict-Confidence Reinforcement Learning for Adaptive Test-Time Compute](llm_reasoning/svr-self-verifying-refinement-via-joint-verdict-confidence-reinforcement-learning-for-adaptive-test.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28457</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">对齐 / RLHF</span></div>

<div class="daily-paper-summary" markdown="1">

本文关注如何让语言模型依据自身生成的正确性判断与置信度，逐轮决定保留当前答案还是继续修改，从而在推理时无需外部正确性反馈也能按题目难度自适应分配计算。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [WhisperRec: Latent Reasoning for Efficient Foundation Recommendation Models](recommender/whisperrec-latent-reasoning-for-efficient-foundation-recommendation-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.26621</span><span class="paper-category-chip">推荐系统</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

WhisperRec旨在把教师模型生成的显式推荐推理压缩进可学习的潜在令牌，使基础推荐模型无需输出冗长思维链，也能利用与决策相关的推理信息。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### LLM Agent · 9 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [Baikal: Structured Search for Deep Research over Data Lakes](llm_agent/baikal-structured-search-for-deep-research-over-data-lakes.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27726</span><span class="paper-category-chip">LLM Agent</span></div>

<div class="daily-paper-summary" markdown="1">

Baikal 将异构数据湖上的深度研究重新表述为固定预算下的结构化搜索：先把表格与文本组织成语义区域，再依据已获得发现的质量，在区域之间自适应地平衡探索与利用。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Can Large Language Models Execute Parent Orders?](llm_agent/can-large-language-models-execute-parent-orders.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28410</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究大语言模型能否在无需预设市场行为假设和任务专用训练的条件下执行母订单，并以长周期规划、短周期调整相分离的 PACE 框架验证这一可能性。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Change2Task: From Repository Changes to Executable Coding Agent Tasks and Environments](llm_agent/change2task-from-repository-changes-to-executable-coding-agent-tasks-and-environments.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28591</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM 评测</span></div>

<div class="daily-paper-summary" markdown="1">

Change2Task研究如何把历史合并请求中由开发者真实意图支撑的软件变更，迁移到同一仓库健康、现代的后继版本上，并将其构造成可执行、可验证且可复用环境的编码智能体任务。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [EMBL AI Librarian: Life-Sciences Knowledge Layer for AI Agents](llm_agent/embl-ai-librarian-life-sciences-knowledge-layer-for-ai-agents.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28229</span><span class="paper-category-chip">LLM Agent</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究如何在不自建稠密向量索引的前提下，把面向人类的 Europe PMC 文献搜索服务改造成面向 AI 智能体的生命科学知识层，使智能体能够用自然语言提问并直接获得紧凑、可引用的证据片段。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [MagicSelector: Joint Optimization for Agent Tool Selection via Counterfactual Decomposition and Progressive Reranking](llm_agent/magicselector-joint-optimization-for-agent-tool-selection-via-counterfactual-decomposition-and-progr.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.17751</span><span class="paper-category-chip">LLM Agent</span></div>

<div class="daily-paper-summary" markdown="1">

MagicSelector面向移动智能体的复杂工具检索，将任务分解、精细重排序与候选截断联合起来，重点解决分解奖励缺乏因果归因、相似工具难区分以及固定$K$造成召回与噪声难以兼顾的问题。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [MemTxn: A Transaction Boundary for Source-Supported Updates and Complete-State Recovery in Agent Memory](llm_agent/memtxn-a-transaction-boundary-for-source-supported-updates-and-complete-state-recovery-in-agent-memo.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27834</span><span class="paper-category-chip">LLM Agent</span></div>

<div class="daily-paper-summary" markdown="1">

MemTxn将可写智能体记忆的更新与故障恢复视为应用级事务，通过来源支持校验、冲突版本选择和完整状态恢复，防止错误事实被持久化、错误版本对回答可见以及多键故障留下混合状态。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [SciDataSailor: Deep Scientific Data Exploring](llm_agent/scidatasailor-deep-scientific-data-exploring.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28098</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文关注如何让大语言模型智能体直接进入真实科学数据仓库，通过可执行工具发现、计算、核验并整合跨文件证据，并进一步解决这类长程交互轨迹难以低成本、可靠构造的问题。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [OSReward: Instituting Standardized Evaluation for Cross-Platform Computer-Use Reward Models](llm_evaluation/osreward-instituting-standardized-evaluation-for-cross-platform-computer-use-reward-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28609</span><span class="paper-category-chip">LLM 评测</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

本文围绕“视觉语言模型能否可靠且低成本地判断计算机使用智能体是否真正完成任务”这一问题，建立跨平台标准化评测基准，并据此开发针对主要误判模式的开放奖励模型。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [ThreatForest: Multi-Agent Attack Tree Generation with Pluggable TTP Framework Mapping](multi_agent/threatforest-multi-agent-attack-tree-generation-with-pluggable-ttp-framework-mapping.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27528</span><span class="paper-category-chip">Multi-Agent</span><span class="paper-category-chip">LLM Agent</span></div>

<div class="daily-paper-summary" markdown="1">

ThreatForest研究如何把云原生应用的源代码仓库自动转化为具有应用上下文、标准化TTP映射和针对性缓解措施的结构化攻击树，并通过可插拔映射组件与人工验证关口兼顾覆盖范围、可审查性和实际可用性。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### Multi-Agent · 1 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [ThreatForest: Multi-Agent Attack Tree Generation with Pluggable TTP Framework Mapping](multi_agent/threatforest-multi-agent-attack-tree-generation-with-pluggable-ttp-framework-mapping.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27528</span><span class="paper-category-chip">Multi-Agent</span><span class="paper-category-chip">LLM Agent</span></div>

<div class="daily-paper-summary" markdown="1">

ThreatForest研究如何把云原生应用的源代码仓库自动转化为具有应用上下文、标准化TTP映射和针对性缓解措施的结构化攻击树，并通过可插拔映射组件与人工验证关口兼顾覆盖范围、可审查性和实际可用性。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### 对齐 / RLHF · 4 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [ReDiPPO: Reference-Guided Value Calibration and Discrepancy-Aware Token Reweighting for Mathematical Reasoning](llm_alignment/redippo-reference-guided-value-calibration-and-discrepancy-aware-token-reweighting-for-mathematical.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27631</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">强化学习</span></div>

<div class="daily-paper-summary" markdown="1">

ReDiPPO利用仅在训练期提供给评论器的参考答案校准中间状态价值，并依据参考引导评论器与标准评论器的分歧调整逐词元优势权重，以改善数学推理中的信用分配。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [OSReward: Instituting Standardized Evaluation for Cross-Platform Computer-Use Reward Models](llm_evaluation/osreward-instituting-standardized-evaluation-for-cross-platform-computer-use-reward-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28609</span><span class="paper-category-chip">LLM 评测</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

本文围绕“视觉语言模型能否可靠且低成本地判断计算机使用智能体是否真正完成任务”这一问题，建立跨平台标准化评测基准，并据此开发针对主要误判模式的开放奖励模型。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [SVR: Self-Verifying Refinement via Joint Verdict-Confidence Reinforcement Learning for Adaptive Test-Time Compute](llm_reasoning/svr-self-verifying-refinement-via-joint-verdict-confidence-reinforcement-learning-for-adaptive-test.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28457</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">对齐 / RLHF</span></div>

<div class="daily-paper-summary" markdown="1">

本文关注如何让语言模型依据自身生成的正确性判断与置信度，逐轮决定保留当前答案还是继续修改，从而在推理时无需外部正确性反馈也能按题目难度自适应分配计算。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants](recommender/toolrec-calibrated-preference-alignment-for-query-recommendation-in-on-device-assistants.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2606.08466</span><span class="paper-category-chip">推荐系统</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

ToolRec面向端侧智能助手，将系统工具检索与点击信号校准结合起来，使大语言模型更可靠地推荐可直接触发设备功能、且符合用户真实偏好的查询。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### LLM 安全 · 1 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [TriShield: Zero-Utility-Loss Defense Against Privacy Backdoors in Federated Language Model Fine-Tuning via Orthogonal Gradient Projection and Optimizer State Entanglement](llm_safety/trishield-zero-utility-loss-defense-against-privacy-backdoors-in-federated-language-model-fine-tunin.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27940</span><span class="paper-category-chip">LLM 安全</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对恶意参数服务器在联邦大语言模型微调中预埋神经元级隐私后门的问题，提出完全在客户端运行的三层防御思路，目标是在不依赖服务器配合且不损害主任务效用的前提下阻断基于梯度的样本重建。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### LLM 评测 · 4 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [Change2Task: From Repository Changes to Executable Coding Agent Tasks and Environments](llm_agent/change2task-from-repository-changes-to-executable-coding-agent-tasks-and-environments.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28591</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM 评测</span></div>

<div class="daily-paper-summary" markdown="1">

Change2Task研究如何把历史合并请求中由开发者真实意图支撑的软件变更，迁移到同一仓库健康、现代的后继版本上，并将其构造成可执行、可验证且可复用环境的编码智能体任务。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Dimensionality and Measurement Precision in HLE's Multiple-Choice Subset](llm_evaluation/dimensionality-and-measurement-precision-in-hle-s-multiple-choice-subset.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27420</span><span class="paper-category-chip">LLM 评测</span></div>

<div class="daily-paper-summary" markdown="1">

本文把HLE视为需要验证的测量工具，而非天然可信的排行榜，检验其八个学科分数是否代表可分离能力，以及它能否精确区分能力接近的前沿语言模型。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [IFHierBench: Hierarchical Instruction Following for Large Language Models](llm_evaluation/ifhierbench-hierarchical-instruction-following-for-large-language-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27912</span><span class="paper-category-chip">LLM 评测</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文指出，现有基准因把输出约束视为作用于整段回答的扁平清单，无法评估大语言模型能否在正确的嵌套区域内满足约束，因此提出以分层作用域和确定性检查器测量这一能力的 IFHierBench。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [OSReward: Instituting Standardized Evaluation for Cross-Platform Computer-Use Reward Models](llm_evaluation/osreward-instituting-standardized-evaluation-for-cross-platform-computer-use-reward-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28609</span><span class="paper-category-chip">LLM 评测</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

本文围绕“视觉语言模型能否可靠且低成本地判断计算机使用智能体是否真正完成任务”这一问题，建立跨平台标准化评测基准，并据此开发针对主要误判模式的开放奖励模型。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### LLM 效率 · 4 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [PCAP-LM: An LLM-Native Text Representation for TLS Bulk Traffic Analysis](llm_efficiency/pcap-lm-an-llm-native-text-representation-for-tls-bulk-traffic-analysis.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28100</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

PCAP-LM将原始网络抓包转化为面向大语言模型的流级语义文本，在大幅缩短输入的同时保留流拓扑、TLS元数据、异常标注和行为模式，并允许分析者按引用回查原始数据包。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Prox: Training-Free FFN Activation Sparsity via Approximate Intermediate-Channel Salience in LLMs](llm_efficiency/prox-training-free-ffn-activation-sparsity-via-approximate-intermediate-channel-salience-in-llms.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27591</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

Prox利用低成本代理值近似SwiGLU中间状态的幅值排序来选择通道，再对入选通道执行精确计算，从而在无需训练的条件下兼顾高FFN稀疏率、模型质量与推理加速。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning](llm_efficiency/wide-boosting-adaptive-llm-inference-via-token-level-dynamic-width-pruning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28418</span><span class="paper-category-chip">LLM 效率</span></div>

<div class="daily-paper-summary" markdown="1">

WIDE旨在通过逐词元动态选择注意力头组和FFN通道组，并将这种细粒度剪枝与GPU内核协同设计，在更好保留大模型能力的同时，为预填充与解码阶段带来可落地的端到端加速。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [WhisperRec: Latent Reasoning for Efficient Foundation Recommendation Models](recommender/whisperrec-latent-reasoning-for-efficient-foundation-recommendation-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.26621</span><span class="paper-category-chip">推荐系统</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

WhisperRec旨在把教师模型生成的显式推荐推理压缩进可学习的潜在令牌，使基础推荐模型无需输出冗长思维链，也能利用与决策相关的推理信息。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### 知识编辑 · 1 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [Subtract or Replay? Exact Deletion from Language-Model Memory](knowledge_editing/subtract-or-replay-exact-deletion-from-language-model-memory.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27539</span><span class="paper-category-chip">知识编辑</span></div>

<div class="daily-paper-summary" markdown="1">

本文把语言模型持久化上下文记忆中的“精确删除”定义为：编辑后的记忆必须与从未摄入目标记录时的反事实参考一致，并指出删除机制取决于记忆表示——影响可寻址时做代数减除，影响被后续写入缠入共享状态时则从检查点回退并重放后缀。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### LLM 机制与可解释性 · 1 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [Metaphor Tracer: A Theory-Informed Analysis of Hidden States](llm_interpretability/metaphor-tracer-a-theory-informed-analysis-of-hidden-states.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28434</span><span class="paper-category-chip">LLM 机制与可解释性</span></div>

<div class="daily-paper-summary" markdown="1">

本文尝试把关于“文本意义取决于符号在具体文本中的关系位置”的理论主张转化为可检验问题：能否从语言模型一次前向传播的隐藏状态几何中，无训练地识别某个位置对全文的聚合与对其他词元的隐喻式迁移。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### LLM 其他 · 13 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [Can Large Language Models Execute Parent Orders?](llm_agent/can-large-language-models-execute-parent-orders.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28410</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究大语言模型能否在无需预设市场行为假设和任务专用训练的条件下执行母订单，并以长周期规划、短周期调整相分离的 PACE 框架验证这一可能性。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [SciDataSailor: Deep Scientific Data Exploring](llm_agent/scidatasailor-deep-scientific-data-exploring.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28098</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文关注如何让大语言模型智能体直接进入真实科学数据仓库，通过可执行工具发现、计算、核验并整合跨文件证据，并进一步解决这类长程交互轨迹难以低成本、可靠构造的问题。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [ReDiPPO: Reference-Guided Value Calibration and Discrepancy-Aware Token Reweighting for Mathematical Reasoning](llm_alignment/redippo-reference-guided-value-calibration-and-discrepancy-aware-token-reweighting-for-mathematical.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27631</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">强化学习</span></div>

<div class="daily-paper-summary" markdown="1">

ReDiPPO利用仅在训练期提供给评论器的参考答案校准中间状态价值，并依据参考引导评论器与标准评论器的分歧调整逐词元优势权重，以改善数学推理中的信用分配。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [PCAP-LM: An LLM-Native Text Representation for TLS Bulk Traffic Analysis](llm_efficiency/pcap-lm-an-llm-native-text-representation-for-tls-bulk-traffic-analysis.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28100</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

PCAP-LM将原始网络抓包转化为面向大语言模型的流级语义文本，在大幅缩短输入的同时保留流拓扑、TLS元数据、异常标注和行为模式，并允许分析者按引用回查原始数据包。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Prox: Training-Free FFN Activation Sparsity via Approximate Intermediate-Channel Salience in LLMs](llm_efficiency/prox-training-free-ffn-activation-sparsity-via-approximate-intermediate-channel-salience-in-llms.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27591</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

Prox利用低成本代理值近似SwiGLU中间状态的幅值排序来选择通道，再对入选通道执行精确计算，从而在无需训练的条件下兼顾高FFN稀疏率、模型质量与推理加速。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [IFHierBench: Hierarchical Instruction Following for Large Language Models](llm_evaluation/ifhierbench-hierarchical-instruction-following-for-large-language-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27912</span><span class="paper-category-chip">LLM 评测</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文指出，现有基准因把输出约束视为作用于整段回答的扁平清单，无法评估大语言模型能否在正确的嵌套区域内满足约束，因此提出以分层作用域和确定性检查器测量这一能力的 IFHierBench。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [SciSchema.org: A Multidisciplinary Collection of Schemas for Structured Scientific Process Descriptions](llm_nlp/scischema-org-a-multidisciplinary-collection-of-schemas-for-structured-scientific-process-descriptio.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27955</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文发布 SciSchema.org：一个覆盖五类学科领域、包含 16 个专家标注科学过程模式的多学科资源，旨在把散落于论文不同载体中的过程信息转化为可复用的结构化描述。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [TriShield: Zero-Utility-Loss Defense Against Privacy Backdoors in Federated Language Model Fine-Tuning via Orthogonal Gradient Projection and Optimizer State Entanglement](llm_safety/trishield-zero-utility-loss-defense-against-privacy-backdoors-in-federated-language-model-fine-tunin.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27940</span><span class="paper-category-chip">LLM 安全</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对恶意参数服务器在联邦大语言模型微调中预埋神经元级隐私后门的问题，提出完全在客户端运行的三层防御思路，目标是在不依赖服务器配合且不损害主任务效用的前提下阻断基于梯度的样本重建。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [FiRE: Enhancing MLLMs with Fine-Grained Context Learning for Complex Image Retrieval](multimodal_vlm/fire-enhancing-mllms-with-fine-grained-context-learning-for-complex-image-retrieval.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27959</span><span class="paper-category-chip">多模态 VLM</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

FiRE通过自动构建细粒度多模态五元组数据集，并将上下文推理与检索对齐拆分为两个微调阶段，使多模态大语言模型更好地处理组合图像、长文本和视觉对话等复杂图像检索任务。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [REPREC: Representation Driven Parameter-Efficient Recommendation System](recommender/reprec-representation-driven-parameter-efficient-recommendation-system.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.24845</span><span class="paper-category-chip">推荐系统</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

REPREC研究能否仅用一个轻量的用户表示注入器连接冻结的序列推荐编码器与冻结的大语言模型，在保留协同与序列信号的同时降低训练、推理和部署复杂度。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants](recommender/toolrec-calibrated-preference-alignment-for-query-recommendation-in-on-device-assistants.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2606.08466</span><span class="paper-category-chip">推荐系统</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

ToolRec面向端侧智能助手，将系统工具检索与点击信号校准结合起来，使大语言模型更可靠地推荐可直接触发设备功能、且符合用户真实偏好的查询。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [WhisperRec: Latent Reasoning for Efficient Foundation Recommendation Models](recommender/whisperrec-latent-reasoning-for-efficient-foundation-recommendation-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.26621</span><span class="paper-category-chip">推荐系统</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

WhisperRec旨在把教师模型生成的显式推荐推理压缩进可学习的潜在令牌，使基础推荐模型无需输出冗长思维链，也能利用与决策相关的推理信息。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Relational Scene Graphs for Object Grounding of Natural Language Commands](robotics/relational-scene-graphs-for-object-grounding-of-natural-language-commands.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2602.04635</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究在三维场景图中显式加入物体间空间关系，是否能帮助大语言模型更准确地把开放词汇自然语言指令指向真实环境中的目标物体，并比较开放词汇与封闭词汇关系的效果。

</div>

</article>

</div>

</section>

## 生成与多模态 · 6 篇

<section class="daily-category-section" markdown="1">

### 多模态 VLM · 6 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [OSReward: Instituting Standardized Evaluation for Cross-Platform Computer-Use Reward Models](llm_evaluation/osreward-instituting-standardized-evaluation-for-cross-platform-computer-use-reward-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28609</span><span class="paper-category-chip">LLM 评测</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

本文围绕“视觉语言模型能否可靠且低成本地判断计算机使用智能体是否真正完成任务”这一问题，建立跨平台标准化评测基准，并据此开发针对主要误判模式的开放奖励模型。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [FiRE: Enhancing MLLMs with Fine-Grained Context Learning for Complex Image Retrieval](multimodal_vlm/fire-enhancing-mllms-with-fine-grained-context-learning-for-complex-image-retrieval.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27959</span><span class="paper-category-chip">多模态 VLM</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

FiRE通过自动构建细粒度多模态五元组数据集，并将上下文推理与检索对齐拆分为两个微调阶段，使多模态大语言模型更好地处理组合图像、长文本和视觉对话等复杂图像检索任务。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [VAD: Attributing Visual Evidence for Target Reconstruction in Multimodal On-Policy Distillation](multimodal_vlm/vad-attributing-visual-evidence-for-target-reconstruction-in-multimodal-on-policy-distillation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28590</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

VAD通过比较同一教师在“视觉证据存在”与“视觉证据移除”两种条件下的预测变化，估计教师纠正中可归因于视觉证据的部分，并据此重建以学生为锚点的蒸馏目标。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Compact Task-Aligned Imitation Learning for Laboratory Automation](robotics/compact-task-aligned-imitation-learning-for-laboratory-automation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2603.01110</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对实验室日常操作难以低成本自动化的问题，研究如何用不足5亿参数的小型基础模型构建可在低显存GPU上运行、同时具备较高真实机器人任务成功率的模仿学习系统。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Do World Action Models Generalize Better than VLAs? A Robustness Study](robotics/do-world-action-models-generalize-better-than-vlas-a-robustness-study.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2603.22078</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

本文通过在单臂与双臂操作基准中施加视觉和语言扰动，系统比较世界动作模型（WAM）与视觉—语言—动作模型（VLA）的鲁棒性、训练依赖和推理代价，以检验显式预测未来状态是否真正带来更好的泛化。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [World Action Planner: Generalizable Decision-Making with Action-Conditioned World Models](robotics/world-action-planner-generalizable-decision-making-with-action-conditioned-world-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27599</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

World Action Planner以视觉语言模型提出高层动作方案，再借助动作条件世界模型想象执行结果并迭代修正，旨在让机器人在组合任务、新布局和零样本场景中获得比端到端模仿策略更强的泛化能力。

</div>

</article>

</div>

</section>

## 决策与具身 · 29 篇

<section class="daily-category-section" markdown="1">

### 机器人 / 具身智能 · 20 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [Critic Architecture Matters: Dual vs. Unified Critics for Humanoid Loco-Manipulation](reinforcement_learning/critic-architecture-matters-dual-vs-unified-critics-for-humanoid-loco-manipulation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2606.11891</span><span class="paper-category-chip">强化学习</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

本文考察人形机器人在同一策略中同时学习行走与伸手时，采用统一评论家还是双评论家是否会形成值得进一步因果验证的任务效率差异。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [A Robust Placeability Metric for Model-Free Unified Pick-and-Place Reasoning](robotics/a-robust-placeability-metric-for-model-free-unified-pick-and-place-reasoning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2510.14584</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出一种直接面向噪声、局部点云的概率式可放置性度量，联合评估候选六自由度放置姿态的物理稳定性与放置条件下的抓取可执行性，从而为未知物体选择稳定、无碰撞的抓取—放置组合。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [A Three-Stage Offline SDRE-Based Control Framework for Human Motion Reproduction on a Suspended Bipedal Robot](robotics/a-three-stage-offline-sdre-based-control-framework-for-human-motion-reproduction-on-a-suspended-bipe.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2506.04680</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究如何将 Vicon 捕获的人体下肢运动离线转换为满足电机约束、能够在悬吊式双足机器人上准确且跨试次稳定复现的关节命令，从而为外骨骼人体试验前的台架测试提供可重复运动基准。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [ARCSnake V2: Mechanical Adaptations For An Amphibious Multi-Domain Screw-Propelled Snake-Like Robot](robotics/arcsnake-v2-mechanical-adaptations-for-an-amphibious-multi-domain-screw-propelled-snake-like-robot.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2511.11970</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对原版 ARCSnake 无法水下作业的关键缺口，研究如何通过防水传动、关节密封与可调浮力控制，将螺旋推进蛇形机器人扩展为能在狭窄、非结构化陆水环境中运动和执行操作任务的两栖平台。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [CLAM: Continuous Latent Action Models for Robot Learning from Unlabeled Demonstrations](robotics/clam-continuous-latent-action-models-for-robot-learning-from-unlabeled-demonstrations.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2505.04999</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

CLAM旨在用少量带动作的任务无关玩耍数据，将大量无动作标签的机器人专家视频转化为可执行的连续控制策略，从而减少对昂贵专家遥操作数据的依赖。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Compact Task-Aligned Imitation Learning for Laboratory Automation](robotics/compact-task-aligned-imitation-learning-for-laboratory-automation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2603.01110</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对实验室日常操作难以低成本自动化的问题，研究如何用不足5亿参数的小型基础模型构建可在低显存GPU上运行、同时具备较高真实机器人任务成功率的模仿学习系统。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Direct Rotor Thrust Sensing and Feedback Control for Disturbance Rejection of Multirotors Using Load-cells](robotics/direct-rotor-thrust-sensing-and-feedback-control-for-disturbance-rejection-of-multirotors-using-load.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.10099</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究能否在多旋翼旋翼处用称重传感器直接测量瞬时推力，并通过高速内环调节推力，从而在阵风、垂直入流和地面效应等复杂气动扰动影响飞行轨迹之前或之初抑制其作用。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Do World Action Models Generalize Better than VLAs? A Robustness Study](robotics/do-world-action-models-generalize-better-than-vlas-a-robustness-study.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2603.22078</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

本文通过在单臂与双臂操作基准中施加视觉和语言扰动，系统比较世界动作模型（WAM）与视觉—语言—动作模型（VLA）的鲁棒性、训练依赖和推理代价，以检验显式预测未来状态是否真正带来更好的泛化。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [LeapBot-WA: World-Anchor Action Models via Predictive Latent Alignments](robotics/leapbot-wa-world-anchor-action-models-via-predictive-latent-alignments.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.23969</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

LeapBot-WA旨在以预测语义潜表示取代像素级未来画面生成，并通过分布适配与训练期动力学指导，使机器人策略兼具稳定学习、视觉鲁棒性和低开销部署能力。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Metrics vs Surveys: An Analysis for Human-Aligned Benchmarking in Social Robot Navigation](robotics/metrics-vs-surveys-an-analysis-for-human-aligned-benchmarking-in-social-robot-navigation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2510.02941</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究社会机器人导航中的数值指标与人类问卷评价之间是否存在稳定关联，以筛选更接近人类感知的指标子集，作为正式用户调查之前的初步基准工具。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [MorphQuad: Morphable Quadrotor for Superhuman Maneuverability, Manipulation, and Resiliency](robotics/morphquad-morphable-quadrotor-for-superhuman-maneuverability-manipulation-and-resiliency.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.02764</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对空中机器人难以同时获得全向最大推力、近乎全局稳定性与紧凑四旋翼结构的问题，提出通过双轴独立旋翼转向和面向奇异性、下洗干扰的控制分配协同设计，实现兼具高机动、操作与抗扰能力的 MorphQuad。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [REFINE-DP: Diffusion Policy Fine-tuning for Humanoid Loco-manipulation via Reinforcement Learning](robotics/refine-dp-diffusion-policy-fine-tuning-for-humanoid-loco-manipulation-via-reinforcement-learning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2603.13707</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">强化学习</span></div>

<div class="daily-paper-summary" markdown="1">

REFINE-DP通过强化学习联合微调扩散策略运动规划器与人形机器人全身控制器，使二者在交互中共同适应，从而缓解离线模仿学习的分布偏移和规划—控制失配。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [RL$^2$-VLA: Adaptive RL Latent Compositional Steering with Test-Time Scaling for Vision-Language-Action Models](robotics/rl-2-vla-adaptive-rl-latent-compositional-steering-with-test-time-scaling-for-vision-language-action.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.26991</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">强化学习</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对视觉-语言-动作模型在困难或分布外任务中容易失效、现有测试时干预又缺乏动作多样性与状态适应性的问题，提出根据失败预测选择性启用离线强化学习潜变量组合引导的框架 $RL^2$。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [RMBench: Memory-Dependent Robotic Manipulation Benchmark with Insights into Policy Design](robotics/rmbench-memory-dependent-robotic-manipulation-benchmark-with-insights-into-policy-design.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2603.01229</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对机器人在长时程操作中难以保留并调用历史信息、且现有研究缺少统一评测与机制分析的问题，以任务记忆复杂度、RMBench基准和模块化策略Mem-0建立从任务刻画到架构消融的系统研究框架。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Relational Scene Graphs for Object Grounding of Natural Language Commands](robotics/relational-scene-graphs-for-object-grounding-of-natural-language-commands.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2602.04635</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究在三维场景图中显式加入物体间空间关系，是否能帮助大语言模型更准确地把开放词汇自然语言指令指向真实环境中的目标物体，并比较开放词汇与封闭词汇关系的效果。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [SeedPolicy: Horizon Scaling via Self-Evolving Diffusion Policy for Robot Manipulation](robotics/seedpolicy-horizon-scaling-via-self-evolving-diffusion-policy-for-robot-manipulation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2603.05117</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对扩散策略无法从更长观测历史中稳定获益的问题，提出以紧凑递归状态和动态门控实现可扩展时间建模的 SeedPolicy。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [SharedAssembly: A Data Collection Approach via Shared Tele-Assembly](robotics/sharedassembly-a-data-collection-approach-via-shared-tele-assembly.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2503.12287</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对亚毫米级紧间隙装配示范难以通过传统遥操作高效采集的问题，提出在主端与从端共同嵌入装配辅助的共享自主双边遥操作框架 SharedAssembly，以降低操作门槛并提高高质量接触数据的采集成功率与效率。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Ultrafast Sampling-based Kinodynamic Planning via Differential Flatness](robotics/ultrafast-sampling-based-kinodynamic-planning-via-differential-flatness.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2603.16059</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出 FLASK：利用微分平坦性把非线性机器人动力学规划转化为平坦输出空间中的解析边值问题，并结合 SIMD 并行轨迹验证，使采样式规划器能够快速生成动力学可行的运动轨迹。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [World Action Planner: Generalizable Decision-Making with Action-Conditioned World Models](robotics/world-action-planner-generalizable-decision-making-with-action-conditioned-world-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27599</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">多模态 VLM</span></div>

<div class="daily-paper-summary" markdown="1">

World Action Planner以视觉语言模型提出高层动作方案，再借助动作条件世界模型想象执行结果并迭代修正，旨在让机器人在组合任务、新布局和零样本场景中获得比端到端模仿策略更强的泛化能力。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [{\tau}: Learning Touch-Augmented Vision-Language-Action Models from Future Visual Supervision](robotics/tau-learning-touch-augmented-vision-language-action-models-from-future-visual-supervision.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.24485</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出触觉增强的视觉-语言-动作框架 $\tau$，利用动作条件下的未来视觉特征变化作为训练监督，使高维视觉式触觉表示学习接触交互的时空动态，并将其用于机器人动作生成。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### 强化学习 · 4 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [ReDiPPO: Reference-Guided Value Calibration and Discrepancy-Aware Token Reweighting for Mathematical Reasoning](llm_alignment/redippo-reference-guided-value-calibration-and-discrepancy-aware-token-reweighting-for-mathematical.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27631</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">强化学习</span></div>

<div class="daily-paper-summary" markdown="1">

ReDiPPO利用仅在训练期提供给评论器的参考答案校准中间状态价值，并依据参考引导评论器与标准评论器的分歧调整逐词元优势权重，以改善数学推理中的信用分配。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Critic Architecture Matters: Dual vs. Unified Critics for Humanoid Loco-Manipulation](reinforcement_learning/critic-architecture-matters-dual-vs-unified-critics-for-humanoid-loco-manipulation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2606.11891</span><span class="paper-category-chip">强化学习</span><span class="paper-category-chip">机器人 / 具身智能</span></div>

<div class="daily-paper-summary" markdown="1">

本文考察人形机器人在同一策略中同时学习行走与伸手时，采用统一评论家还是双评论家是否会形成值得进一步因果验证的任务效率差异。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [REFINE-DP: Diffusion Policy Fine-tuning for Humanoid Loco-manipulation via Reinforcement Learning](robotics/refine-dp-diffusion-policy-fine-tuning-for-humanoid-loco-manipulation-via-reinforcement-learning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2603.13707</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">强化学习</span></div>

<div class="daily-paper-summary" markdown="1">

REFINE-DP通过强化学习联合微调扩散策略运动规划器与人形机器人全身控制器，使二者在交互中共同适应，从而缓解离线模仿学习的分布偏移和规划—控制失配。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [RL$^2$-VLA: Adaptive RL Latent Compositional Steering with Test-Time Scaling for Vision-Language-Action Models](robotics/rl-2-vla-adaptive-rl-latent-compositional-steering-with-test-time-scaling-for-vision-language-action.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.26991</span><span class="paper-category-chip">机器人 / 具身智能</span><span class="paper-category-chip">强化学习</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对视觉-语言-动作模型在困难或分布外任务中容易失效、现有测试时干预又缺乏动作多样性与状态适应性的问题，提出根据失败预测选择性启用离线强化学习潜变量组合引导的框架 $RL^2$。

</div>

</article>

</div>

</section>

<section class="daily-category-section" markdown="1">

### 推荐系统 · 8 篇

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [CoSimRec: Measuring Coordinated-Content Penetration in Recommender Feedback Loops](recommender/cosimrec-measuring-coordinated-content-penetration-in-recommender-feedback-loops.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.15114</span><span class="paper-category-chip">推荐系统</span></div>

<div class="daily-paper-summary" markdown="1">

本文将协同内容操纵从“目标项目排名是否上升”的静态问题，重新定义为“协同行为能否经推荐反馈循环转化为非协同用户可见度与响应”的动态测量问题。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Kairos: Numerically Robust News Recommendation under Item Cold-Start via Cholesky-based LinUCB](recommender/kairos-numerically-robust-news-recommendation-under-item-cold-start-via-cholesky-based-linucb.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.26832</span><span class="paper-category-chip">推荐系统</span></div>

<div class="daily-paper-summary" markdown="1">

Kairos面向新闻条目生命周期短、交互稀疏所造成的冷启动，尝试以基于内容上下文的LinUCB进行在线探索与排序，并通过Cholesky秩一更新和Matryoshka表示分别改善长期运行的数值稳定性与候选检索效率。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Learning Sparse Representations of Multimodal Content for Enhanced Cold Item Recommendation](recommender/learning-sparse-representations-of-multimodal-content-for-enhanced-cold-item-recommendation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.17184</span><span class="paper-category-chip">推荐系统</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究如何把文本、图像等多模态内容转换为稀疏物品表示，以同时提高冷启动推荐的准确性、存储效率、检索效率与可解释性。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [REPREC: Representation Driven Parameter-Efficient Recommendation System](recommender/reprec-representation-driven-parameter-efficient-recommendation-system.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.24845</span><span class="paper-category-chip">推荐系统</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

REPREC研究能否仅用一个轻量的用户表示注入器连接冻结的序列推荐编码器与冻结的大语言模型，在保留协同与序列信号的同时降低训练、推理和部署复杂度。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [ROCS: Request-Oriented Compute Sharing for Efficient Large-Scale Recommendation](recommender/rocs-request-oriented-compute-sharing-for-efficient-large-scale-recommendation.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27744</span><span class="paper-category-chip">推荐系统</span></div>

<div class="daily-paper-summary" markdown="1">

ROCS将推荐推理重构为“请求侧计算一次、候选侧按项计算”的非对称依赖模式，在保留中间请求—候选交互能力的同时减少同一请求内跨候选的重复计算。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants](recommender/toolrec-calibrated-preference-alignment-for-query-recommendation-in-on-device-assistants.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2606.08466</span><span class="paper-category-chip">推荐系统</span><span class="paper-category-chip">对齐 / RLHF</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

ToolRec面向端侧智能助手，将系统工具检索与点击信号校准结合起来，使大语言模型更可靠地推荐可直接触发设备功能、且符合用户真实偏好的查询。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Towards Transfer-Efficient Multi-modal Sequential Recommendation with State Space Duality](recommender/towards-transfer-efficient-multi-modal-sequential-recommendation-with-state-space-duality.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2506.02916</span><span class="paper-category-chip">推荐系统</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对可迁移多模态序列推荐微调收敛慢的问题，探索以符合序列推荐先验的代数结构约束替代复杂训练策略，并通过序列级对齐、时序衰减与跨模态融合兼顾推荐精度和迁移效率。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [WhisperRec: Latent Reasoning for Efficient Foundation Recommendation Models](recommender/whisperrec-latent-reasoning-for-efficient-foundation-recommendation-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.26621</span><span class="paper-category-chip">推荐系统</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

WhisperRec旨在把教师模型生成的显式推荐推理压缩进可学习的潜在令牌，使基础推荐模型无需输出冗长思维链，也能利用与决策相关的推理信息。

</div>

</article>

</div>

</section>
