---
name: knowledge-intake
description: 视频入库工作流。用户上传视频到收件目录并说「处理/入库/提取知识点」时使用：扫描新增 → 转录或 OCR → 校对同音字 → 抽取带出处的知识点 → 重建知识库索引。
---

# 视频入库工作流

## 何时用

用户说「处理新视频」「入库」「提取知识点」「处理 0X 目录」时。

## 配置（安装前先改这里）

| 变量 | 含义 | 默认 |
|---|---|---|
| `INBOX_ROOT` | 待处理视频的根目录，下分 01–06 分类 | `~/Exchange` |
| `TRANSCRIPTS_DIR` | 转录 / OCR 产物 | `~/media/raw/transcripts` |
| `KNOWLEDGE_DIR` | 知识库笔记 | `~/knowledge` |
| `BIN_DIR` | `process-video.sh`、`intake.sh` 所在目录 | `~/bin` |

后三个脚本来自 [mac-ocr-kit](../mac-ocr-kit)；把它的 `scripts/` 加进 `BIN_DIR` 即可。

## 目录约定

- 输入：`$INBOX_ROOT/<分类>/`，分类为 01-机械与工程 / 02-生物与医学 / 03-心理与行为 / 04-信息与系统 / 05-审美与风格 / 06-创作技法 / 99-未分类
- 转录：`$TRANSCRIPTS_DIR/`
- 知识库：`$KNOWLEDGE_DIR/`

## 步骤

### 1. 扫描

```bash
"$BIN_DIR/intake.sh" "$INBOX_ROOT/<分类>"
```

列出尚未处理（无同名转录）的视频。为 0 则结束。

### 2. 转录 / OCR

对每条跑：

```bash
"$BIN_DIR/process-video.sh" "<视频>" "$TRANSCRIPTS_DIR"
```

- 有旁白 → whisper ASR（large-v3）
- 无旁白 → 自动转 OCR（1s 采样，短于 4 分钟用 1s，否则 2s）

**质量闸门**：字数/分钟 < 40、或出现「请不吝点赞/明镜与点点」等幻觉标记 → 判定无旁白，删产物改走 OCR。
OCR 检出 0 段 → 标记「纯视觉，无文字」，不产出知识。

### 3. 校对

每 3–4 条派一个 subagent，只改同音字导致的语义错；输出 `fixed/tNN.md` + `fixed/tNN.changes.md`。
底本路径要写死在 prompt 里（长文件名会超 255 字节，用短 slug 写输出）。

### 4. 抽取知识

每 3–4 条派一个 subagent，读校对稿，产出 `$KNOWLEDGE_DIR/<主题>/<slug>.md`：

```markdown
---
id: kn-<主题>-<slug>
topic: 经济 | 心理 | 文化 | 创作
source: 作者《片名》时长
captured: <日期>
stance: mix
confidence: medium
---

## 关键结论
- [事实] …（源：约 mm:ss）
- [机制] …
- [数字] …

## 我认同的判断（可作为 agent 的判据）
- …

## 待验证 / 存疑
- …

## 出处
```

规则：

- 每条标类型：[事实] / [机制] / [数字] / [观点]
- **必须有出处**，无出处的不写
- 观点不得混进「关键结论」
- 每条视频 6–15 条 claim
- 抽查 2–3 条引用是否与原文一致

### 5. 重建索引

用脚本扫 `$KNOWLEDGE_DIR/**/*.md`，重写 `_index.md`（按主题分组，列 claim 数）。

### 6. 汇报

给用户：

- 新增 N 条视频、M 条 claim
- 存疑 / 需要人工确认的条目
- 索引路径

## 失败模式

| 现象 | 原因 | 处理 |
|---|---|---|
| ASR 输出全是歌词/「中文字幕:CaptionCube」 | 纯音乐或模型幻觉 | 改 OCR |
| 文件名超过 255 字节写不出 | macOS 限制 | 用短 slug 输出 |
| OCR 0 段 | 纯视觉无文字 | 标记，不产出知识 |
| 时间戳不准 | 无字幕轨 | 按字符占比估算，标「约」 |
