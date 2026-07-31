---
title: "LLM 效率 · 每日 arXiv"
description: "LLM 效率 方向每日 arXiv 论文中文解读。"
---

# LLM 效率

共收录 **10** 篇，按 arXiv 日榜日期倒序排列。

## 2026-07-31

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [WhisperRec: Latent Reasoning for Efficient Foundation Recommendation Models](../../arxiv_daily/2026-07-31/recommender/whisperrec-latent-reasoning-for-efficient-foundation-recommendation-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.26621</span><span class="paper-category-chip">推荐系统</span><span class="paper-category-chip">LLM Reasoning</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

WhisperRec旨在把教师模型生成的显式推荐推理压缩进可学习的潜在令牌，使基础推荐模型无需输出冗长思维链，也能利用与决策相关的推理信息。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning](../../arxiv_daily/2026-07-31/llm_efficiency/wide-boosting-adaptive-llm-inference-via-token-level-dynamic-width-pruning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28418</span><span class="paper-category-chip">LLM 效率</span></div>

<div class="daily-paper-summary" markdown="1">

WIDE旨在通过逐词元动态选择注意力头组和FFN通道组，并将这种细粒度剪枝与GPU内核协同设计，在更好保留大模型能力的同时，为预填充与解码阶段带来可落地的端到端加速。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Prox: Training-Free FFN Activation Sparsity via Approximate Intermediate-Channel Salience in LLMs](../../arxiv_daily/2026-07-31/llm_efficiency/prox-training-free-ffn-activation-sparsity-via-approximate-intermediate-channel-salience-in-llms.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.27591</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

Prox利用低成本代理值近似SwiGLU中间状态的幅值排序来选择通道，再对入选通道执行精确计算，从而在无需训练的条件下兼顾高FFN稀疏率、模型质量与推理加速。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [PCAP-LM: An LLM-Native Text Representation for TLS Bulk Traffic Analysis](../../arxiv_daily/2026-07-31/llm_efficiency/pcap-lm-an-llm-native-text-representation-for-tls-bulk-traffic-analysis.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.28100</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

PCAP-LM将原始网络抓包转化为面向大语言模型的流级语义文本，在大幅缩短输入的同时保留流拓扑、TLS元数据、异常标注和行为模式，并允许分析者按引用回查原始数据包。

</div>

</article>

</div>

## 2026-07-30

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [LLMET: Enabling Cross-Layer Evaluation of Emerging M3D Memories for Energy-Efficient LLM Serving](../../arxiv_daily/2026-07-30/llm_efficiency/llmet-enabling-cross-layer-evaluation-of-emerging-m3d-memories-for-energy-efficient-llm-serving.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.26491</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文提出跨层仿真框架 LLMET，用于判断单片三维集成（M3D）带来的超大容量片上存储器，能否通过减少片外内存访问来降低大语言模型服务的芯片能耗。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [Keyless Attention: Value-Space Routing and Value-Only Caching for Efficient Transformers](../../arxiv_daily/2026-07-30/llm_efficiency/keyless-attention-value-space-routing-and-value-only-caching-for-efficient-transformers.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2606.21848</span><span class="paper-category-chip">LLM 效率</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究能否用“价值空间路由”取代传统键投影，使Transformer在不缓存键表示的情况下保持模型能力，并将自回归推理的KV缓存及其访问开销减半。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [HiFloat4 Format for End-To-End Reinforcement Learning Post-Training of Large Language Models](../../arxiv_daily/2026-07-30/llm_efficiency/hifloat4-format-for-end-to-end-reinforcement-learning-post-training-of-large-language-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.26515</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文研究如何在大语言模型强化学习后训练中让采样与训练全流程均采用FP4，并指出主要障碍是采样侧激活异常值引发的大量下溢及采样—训练策略数值失配，进而以稀疏残差校正缓解该问题。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [FinCacheServe: Dependency-Consistent Answer Reuse for Cost-Efficient RAG Serving over Mutable Enterprise Documents](../../arxiv_daily/2026-07-30/llm_efficiency/fincacheserve-dependency-consistent-answer-reuse-for-cost-efficient-rag-serving-over-mutable-enterpr.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2607.26076</span><span class="paper-category-chip">LLM 效率</span></div>

<div class="daily-paper-summary" markdown="1">

FinCacheServe通过把生成答案与文档版本、证据、工具输出及模型配置等依赖共同绑定，在企业文档持续更新的条件下安全复用答案，从而减少RAG服务中的GPU推理调用。

</div>

</article>

<article class="daily-paper-item" markdown="1">

#### [ARC-Encoder: learning compressed text representations for large language models](../../arxiv_daily/2026-07-30/llm_efficiency/arc-encoder-learning-compressed-text-representations-for-large-language-models.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2510.20535</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span><span class="paper-category-chip">LLM Reasoning</span></div>

<div class="daily-paper-summary" markdown="1">

ARC-Encoder旨在不修改目标大语言模型的前提下，将长文本压缩成可直接替代原始词元嵌入的连续表示，并通过轻量适配支持多个解码器。

</div>

</article>

</div>

## 2026-07-29

<div class="daily-paper-list" markdown="1">

<article class="daily-paper-item" markdown="1">

#### [PilotRL: Training Language Model Agents via Global Planning-Guided Progressive Reinforcement Learning](../../arxiv_daily/2026-07-29/llm_agent/pilotrl-training-language-model-agents-via-global-planning-guided-progressive-reinforcement-learning.md)

<div class="daily-paper-meta"><span class="daily-paper-id">arXiv 2508.00344</span><span class="paper-category-chip">LLM Agent</span><span class="paper-category-chip">强化学习</span><span class="paper-category-chip">LLM 效率</span><span class="paper-category-chip">LLM 其他</span></div>

<div class="daily-paper-summary" markdown="1">

本文针对语言模型智能体缺乏长程规划、规划与执行协同不足以及监督微调泛化受限的问题，提出自适应全局规划范式 AdaPlan，并以三阶段渐进式强化学习框架 PilotRL 依次训练计划遵循、计划生成和规划—执行协同能力。

</div>

</article>

</div>
