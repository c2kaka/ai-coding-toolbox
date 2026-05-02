---
name: youtube-to-article
description: >-
  Converts YouTube videos into polished Chinese articles using yt-dlp for
  captions and metadata, VTT cleanup, then template-based rewriting. Trigger
  when the user says「把这个视频做成文章」「YouTube 转文章」「视频改写」「video to
  article」「这个 YouTube 视频帮我整理一下」or clearly wants an article derived
  from video content. Applies when the user provides a youtube.com or youtu.be
  link with改写/整理文章 intent; do not use when the user only shares a link
  without改写 intent or when the link is not YouTube.
---

# YouTube 转文章（youtube-to-article）

把 YouTube 视频转为中文可读文章：**拉元数据与字幕 → 清洗字幕 → 按模板改写**。不下载视频本体；输出须保留原作者与来源链接。

## 依赖

- `yt-dlp`：`brew install yt-dlp`，或 `pip install --user yt-dlp` 后用 **`python -m yt_dlp`**（与 `yt-dlp` CLI 等价，适合未加入 PATH 的 Windows 环境）。
- `python3`
- **Bash**（macOS/Linux、Git Bash、WSL）用于运行 `scripts/fetch_subs.sh`。若当前环境没有可用 Bash（例如仅有 PowerShell），在输出目录 **`OUT`** 下用下面两条等价命令亦可完成「步骤 2 / 步骤 3」（将 `URL` 替换为真实链接）：

```text
python -m yt_dlp --dump-json --skip-download "URL" > OUT/metadata.json
python -m yt_dlp --write-subs --write-auto-subs --sub-langs "en,zh-Hans,zh-Hant" --skip-download --sub-format vtt -o "OUT/%(id)s" "URL"
```

**注意**：不要将 API Key、用户名或私有固定路径写入本 Skill 的配置；运行时以当前环境与用户指定的输出目录为准。

## 执行流程（六步）

| 步骤 | 输入 | 输出 | 脚本/工具 |
|------|------|------|-----------|
| 1 | 用户提供的合法 YouTube URL、工作目录 | 确认改写意图与非 YouTube 排除 | （对话层） |
| 2 | URL | JSON 元信息文件 | `yt-dlp --dump-json --skip-download`，由 `scripts/fetch_subs.sh` 封装 |
| 3 | URL | `.vtt` 字幕文件（人工字幕优先，`en` / `zh-Hans` / `zh-Hant`，缺省再用自动字幕） | 同上脚本内第二条 `yt-dlp` |
| 4 | 选定的 `.vtt` 路径 | 连续纯文本（stdout） | `python3 scripts/clean_vtt.py <path.vtt>` |
| 5 | 纯文本 + `metadata.json` + `prompts/article_template.md` | 中文文章正文 | 大模型：按模板与规则改写 |
| 6 | 成稿 | Markdown 写入**用户当前工作目录**（如 `Slug-中文整理.md`） | （代理写入文件） |

**脚本入口**：在项目内本 Skill 根目录执行：

```bash
bash scripts/fetch_subs.sh "<YOUTUBE_URL>" [输出目录]
```

输出目录默认为 `./youtube-to-artifact`。

## 人工执行检查清单（代理）

1. 元信息：`metadata.json`（标题、作者、时长、`upload_date`、原链接等）。
2. 字幕：若多语言并存，优先与视频主语种一致或可读的 `en` / 中文简体或繁体，用于 `clean_vtt.py`。
3. **自动字幕**：清洗必须经 `clean_vtt.py` **按行去重**，避免滚动重复导致篇幅与 Token 暴增。
4. 成稿：仅用 `#`（标题）与 `##`（章节），**不要用 `###`**；标点符合中文排版习惯（如中文双引号「」、“”、全角逗号等，按版面统一）。
5. 文章来源块须含：原视频标题、作者、`upload_date`、时长、原文链接。
6. 尊重版权：改写为评述/整理文体，标明来源，不隐含原创视频内容。

## 参考文件

- 改写结构与规则注释：`prompts/article_template.md`
- 字幕清洗逻辑：`scripts/clean_vtt.py`

## 端到端自检（写完或更新 Skill 后可跑）

```bash
python3 -c "import re"
python3 -m yt_dlp --version         # 或已加入 PATH 时：yt-dlp --version
bash scripts/fetch_subs.sh "https://www.youtube.com/watch?v=jNQXAC9IVRw" ./tmp-yt-verify
python3 scripts/clean_vtt.py "$(ls ./tmp-yt-verify/*.vtt | head -1)"
```

无 Bash 时：用上文「依赖」中的两条 `python -m yt_dlp ...` 命令代替 `fetch_subs.sh`，再任选生成的 `.vtt` 传给 `clean_vtt.py`。

最后用真实视频的清洗文本 + 模板做一次完整改写验证。
