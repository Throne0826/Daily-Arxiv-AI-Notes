# Daily arXiv AI Notes
https://lifexoryoung.cn/Daily-Arxiv-AI-Notes/   运行网站
一个独立的每日 arXiv AI 论文筛选、分类与中文解读系统。自动完成每日抓取、多标签分类、全文解析和结构化笔记生成。

本站最初基于 [Paper-Notes](https://github.com/zhaoyang97/Paper-Notes) 的 MkDocs Material 站点框架进行改造，但不包含原仓库的顶会论文语料；来源、许可证与主要改动详见文末说明和 [NOTICE.md](NOTICE.md)。

目前是自用 ，其他领域可以fork完自己本地加。
每天处理 arXiv 的 `new submissions` 与 `cross submissions`，覆盖三个大领域、21 个细分方向：

- LLM：推理、Agent、多智能体、对齐/RLHF、安全、幻觉、评测、效率、预训练、知识编辑与其他 LLM/NLP。
- 生成与多模态：图像生成、视频生成、多模态 VLM、VLM Reasoning、VLM Efficiency。
- 决策与具身：自动驾驶、机器人/具身智能、强化学习、推荐系统。

## 核心流程

```text
arXiv 日榜
  -> 多分类抓取、new/cross-list 去重
  -> Atom 元数据，摘要页兜底
  -> 规则召回 + LLM 多标签分类
  -> arXiv HTML 全文，PDF 兜底
  -> 背景、动机、方法、实验四部分中文论文笔记
  -> 数值证据检查、审核队列与状态持久化
  -> MkDocs 日报、领域索引与全文检索
```

自动生成只负责召回、分类和草稿。论文相关性、实验口径、baseline 完整性、related work 关系和所有数字必须由研究者本人审核。

## 本地运行

要求 Python 3.11 或更高版本：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[site,test]"
pytest
```

只验证抓取、规则分类和站点输出，不调用 LLM：

```powershell
$env:ARXIV_CONTACT_EMAIL = "you@example.com"
arxiv-notes --config config.toml run --date latest --metadata-only --max-papers 10
mkdocs serve
```

`metadata_only` 页面会记录为待升级状态；以后配置好 LLM 再运行完整流水线时，会自动重生成正式 AI 草稿，不会被断点状态永久跳过。

完整生成需要配置任意兼容 OpenAI Chat Completions 的服务：

```powershell
Copy-Item .env.example .env
# 在 .env 中填写 OPENAI_API_KEY、OPENAI_BASE_URL 和 OPENAI_MODEL
arxiv-notes --config config.toml run --date latest --require-llm
```

本地密钥从已被 Git 忽略的 `.env` 读取；自动化使用 GitHub Secrets。不要把密钥写入 `.env.example` 或提交到仓库。

## 输出结构

```text
docs/
├── arxiv_daily/
│   ├── index.md
│   └── YYYY-MM-DD/<category>/<paper>.md
├── categories/<category>/index.md
└── review/index.md
data/
├── state.json
├── review_queue.jsonl
└── raw/YYYY-MM-DD/
```

`data/review_queue.jsonl` 是机器可读审核队列；站点内的 `review/index.md` 是人工入口。审核完成后，将论文 frontmatter 的 `review_status` 改为 `human_verified`，并由单独提交记录审核人和时间。

## 自动化

`.github/workflows/daily-arxiv.yml` 在北京时间工作日 08:07 运行抓取与生成，目前只发布 `LLM Reasoning` 方向；`.github/workflows/deploy.yml` 构建并部署 GitHub Pages。仓库需要配置：

- Secret `LLM_API_KEY`
- Variable `LLM_BASE_URL`
- Variable `LLM_MODEL`
- Variable `ARXIV_CONTACT_EMAIL`

## 来源与许可证

站点框架改编自 zhaoyang97 的 [Paper-Notes](https://github.com/zhaoyang97/Paper-Notes)，上游版本与改动说明见 [NOTICE.md](NOTICE.md)。派生的站点材料继续采用 [CC BY-NC-SA 4.0](LICENSE)，须署名、非商业使用并以相同方式共享。
