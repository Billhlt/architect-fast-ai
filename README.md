# Arch-Fast AI

Arch-Fast AI 是一个基于「LLM + 爬虫」的**建筑方案搜索与智能总结**应用。用户输入一个建筑相关的搜索词（如"安藤忠雄 现代风格"），系统会自动完成以下流程：

1. **LLM 拆解**搜索词，提炼出纯名词关键词；
2. 从 **ArchDaily** 搜索并抓取匹配项目的标题与链接；
3. 抓取每个项目的**正文与图片**；
4. 由 **LLM 并发总结**每一篇文章，提取基本信息、设计灵感与技术亮点；
5. 前端以**卡片网格**的形式渲染总结，支持查看图片、切换边框、跳转原文。

整个项目使用**中文**作为工作语言：注释、提示词、函数名、文件名均为中文。

---

## ✨ 功能特性

- 🏗️ **语义搜索**：自然语言搜索词 → LLM 拆解为建筑关键词（无程度形容词、无"建筑/作品"等泛词）
- 🔍 **ArchDaily 抓取**：调用 ArchDaily 搜索 API 获取项目标题与链接
- 📄 **全文 + 图片抓取**：BeautifulSoup 解析文章正文与所有图片链接
- 🤖 **LLM 并发总结**：`ThreadPoolExecutor`（默认 200 并发）对每篇文章独立总结，要求返回基本信息、设计灵感、技术亮点
- 🃏 **卡片式展示**：每张卡片包含总结文本，可**查看项目图片**、**切换边框高亮**、**一键打开原文链接**
- 💬 **聊天功能**：前端集成与 LLM 的流式聊天接口（辅助功能，不参与主流程）

---

## 🏗️ 系统架构

```
┌──────────────┐     ┌──────────────────────────────────────────────────────┐
│   前端 Vue 3  │     │              Python 后端 (FastAPI :8002)              │
│  (Vite :3003) │     │                                                      │
│              │     │  POST /api/vue-data                                   │
│  PageOne.vue ─┼────►│   ① llm拆解搜索词        → 关键词                    │
│  (输入搜索词)  │     │   ② 爬取archdaily搜索界面 → 标题+链接                │
│              │     │   ③ 爬取archdaily文章     → 正文+图片                 │
│              │     │   ④ llm总结文章list(并发)  → 总结列表                 │
│              │     │   ⑤ 追加"文章链接为：xxx"                              │
│              │     │   ⑥ 写入 vue_data.json / pics_data.json              │
│              │     │                                                      │
│  HomePage.vue│     │  GET /api/summary  ◄────────── 读取 vue_data.json     │
│  (卡片展示)   ┼────►│  GET /api/pics     ◄────────── 读取 pics_data.json    │
└──────────────┘     └──────────────┬───────────────────────────────────────┘
                                    │
                         ┌──────────▼──────────┐
                         │  外部 LLM (Spring AI) │
                         │  http://localhost:8081 │
                         │  POST /ai/chat         │
                         └───────────────────────┘
```

> **重要说明**：LLM 本体是**仓库外的独立服务**（Spring AI 后端，`http://localhost:8081/ai/chat`，未包含在本仓库中）。前端与 Python 流水线都通过 `POST` 表单数据 `{ prompt, chatId }` 调用它。**该服务未启动时，所有 LLM 调用都会失败。**

### 技术栈

| 模块 | 技术 | 端口 |
|---|---|---|
| 前端 | Vue 3 + Vue Router + Vite | 3003 |
| Python 后端 | FastAPI + Uvicorn + requests + BeautifulSoup4 + tqdm | 8002 |
| 搜索词代理 | Express (CommonJS，备用) | 3000 |
| LLM | Spring AI（仓库外部） | 8081 |

---

## 📁 目录结构

```
├── src/                            # 前端源码
│   ├── main.js                     # 入口，挂载 App + 路由
│   ├── App.vue                     # 仅 <router-view>
│   ├── router/index.js             # 路由：/ 、/page-two 、/home
│   ├── services/api.js             # 唯一 API 封装层
│   └── views/
│       ├── PageOne.vue             # 搜索词输入页
│       ├── PageTwo.vue             # 聊天/辅助页（占位）
│       └── HomePage.vue            # 结果卡片展示页
│
├── python文件/
│   └── fastapi/                    # Python 后端（工作目录）
│       ├── main.py                 # FastAPI 入口，核心流水线
│       ├── llm拆解搜索词.py         # LLM 拆解搜索词为关键词
│       ├── 爬取archdaily搜索界面.py  # ArchDaily 搜索 API
│       ├── 爬取archdaily文章.py      # 抓取正文 + 图片
│       ├── llm总结文章list.py       # 并发 LLM 总结
│       ├── prompt.py               # 集中管理所有 LLM 提示词
│       ├── vue_data.json           # 生成的总结数据（前端读取）
│       └── pics_data.json          # 生成的图片数据（前端读取）
│
├── server.js                       # Express 代理（备用，未接入主流程）
├── package.json
├── vite.config.js                  # Vite 配置（端口 3003）
└── index.html
```

> `vue_data.json` 和 `pics_data.json` 是**流水线 → 前端的数据交接文件（数据存储）**，并非数据库。前端每次 `GET /api/summary` 和 `GET /api/pics` 都会重新读取它们，直接修改/删除会影响页面展示。

---

## 🚀 快速开始

### 环境要求

- Node.js（含 npm）
- Python 3（需安装以下依赖）

```bash
# Python 依赖（当前无 requirements.txt，需手动安装）
pip install fastapi uvicorn requests beautifulsoup4 tqdm
```

### 1. 启动外部 LLM（必需）

启动仓库外的 Spring AI 后端，确保 `http://localhost:8081/ai/chat` 可访问。

### 2. 安装前端依赖并启动

```bash
npm install          # 安装 JS 依赖
npm run dev          # Vite 开发服务器 → http://localhost:3003
```

### 3. 启动 Python 后端

```bash
cd "python文件/fastapi"
python main.py       # Uvicorn 启动 → http://localhost:8002
# 等价于：uvicorn main:app --port 8002
```

### 4. 使用

1. 打开 `http://localhost:3003`，在**页面一**输入建筑搜索词并回车；
2. 等待流水线跑完（LLM 拆解 → 抓取 → 总结）；
3. 点击"前往主页面"，即可看到以卡片网格展示的总结结果。

> 首次运行会较慢，因为需要抓取多篇文章并逐篇调用 LLM 总结。

### 常用命令

```bash
npm run build        # 生产构建
npm run preview      # 预览生产构建
npm run server       # 启动 Express 代理 (端口 3000，备用)
```

---

## 🔌 API 接口

### Python 后端（FastAPI，端口 8002）

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/api/vue-data` | 接收搜索词（`text/plain` 请求体），执行完整流水线，写入 JSON 文件 |
| `GET` | `/api/summary` | 从 `vue_data.json` 读取并返回总结列表 |
| `GET` | `/api/pics` | 从 `pics_data.json` 读取并返回图片链接列表 |

### 外部 LLM（Spring AI，端口 8081）

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/ai/chat` | 表单数据 `{ prompt, chatId }`，返回 LLM 响应（流式/普通） |
| `GET` | `/ai/history/:type` | 获取聊天历史列表 |
| `GET` | `/ai/history/:type/:chatId` | 获取指定对话的消息历史 |

### Express 代理（端口 3000，备用）

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/process-search-term` | 接收 `{ searchTerm }`，调用 Python 脚本处理（遗留功能，未接入主流程） |

---

## ⚙️ 配置说明

- **端口**固定散落在多处：
  - Vite 开发端口 `3003` → `vite.config.js`
  - FastAPI 端口 `8002` → `python文件/fastapi/main.py`
  - Express 端口 `3000` → `server.js`
  - LLM 地址 `http://localhost:8081` → `src/services/api.js` 及所有 Python LLM 调用模块
- **Python 标识符为中文**（如 `llm拆解搜索词.py`、`拆解完成词`、`总结内容list`），导入时严格依赖这些名称，**请勿改成 ASCII**，否则需同步更新所有 import。
- 后端当前使用 `CORS allow_origins=["*"]`，生产环境建议收紧。

---

## 🧪 可选的独立爬虫

`python文件/fastapi/` 下还包含其他未接入主流程的脚本：古德网抓取、公众号文章抓取、需要解释词语的提取、热榜爬虫等，可在有需要时单独运行或复用。

---

## 📜 许可证

本项目采用 [MIT License](LICENSE)。

Copyright (c) 2026 Billhlt
