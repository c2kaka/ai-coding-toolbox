# AI Coding Toolbox

集中维护 AI 辅助编程时常用的 **规则（rules）**、**技能（skills）** 与 **工作流（workflows）**，方便在多项目间复用、版本化和渐进集成。

## 目标

- **规则**：可复制到各仓库的 `.cursor/rules`、`AGENTS.md`、项目级 constitution 等，统一助手行为边界。
- **技能**：与 Agent 技能体系对齐的说明与模板（可与个人或团队的 `skills` 目录对照安装）。
- **工作流**：可重复的协作步骤（例如：先澄清再写码、拆分 PR、合并冲突处理），用简短清单或链接沉淀。

## 当前布局

```
ai-coding-toolbox/
├── README.md                 # 本说明
├── meta/
│   └── constitution/         # 跨项目行为准则 / 与 CLAUDE.md 等合并使用
│       └── claude.md
└── (planned)                 # 可按需新增，无需一次到位
    ├── rules/                # Cursor / 通用规则片段
    ├── skills/               # SKILL 规格与示例
    └── workflows/            # 流程说明与检查清单
```

后续若增加 `rules/`、`skills/`、`workflows/`，在 README 的「当前布局」中补一行即可。

## 快速使用

1. **Constitution / 行为准则**  
   将 [`meta/constitution/claude.md`](meta/constitution/claude.md) 作为基础，与目标仓库中已有的 `CLAUDE.md`、`AGENTS.md` 或团队 constitution **合并**；避免整条覆盖，只增补缺失的原则。

2. **Cursor 规则**  
   若本仓库提供可复制规则文件，在目标项目中放到 `.cursor/rules/`（或 Cursor 设置中引用的路径），并按项目需要删减。

3. **技能与工作流**  
   以各目录下的 `SKILL.md` 或流程文档为准；安装方式遵循 [Cursor Agent Skills](https://cursor.com/docs) 或团队内部约定（例如 `~/.cursor/skills-cursor/`）。

## 贡献与约定

- **语言**：面向人的说明可用中文；规则正文若需被英文模型优先读取，可在对应文件内采用英文（与现有 `claude.md` 一致）。
- **改动原则**：单次提交尽量只做一类事（例如只加规则或只补工作流），便于下游挑选合并。
- **敏感信息**：勿提交密钥、内网地址或个人数据；仓库已忽略常见本地配置文件（见 `.gitignore`）。

## 许可证

若未另设 `LICENSE` 文件，默认以仓库后续补充的许可证条款为准；用于内部工具箱时可由维护者自行指定。
