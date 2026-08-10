# architect-fast-ai
一句话帮助建筑师在建筑设计前的调研阶段找到所有的想看到的建筑案例。需要版权，目前是演示小demo。A single sentence helps architects find all the architectural case studies they want to see during the pre-design research phase. Copyright reserved. This is currently a small demonstration demo..

  基于 **Vue 3 + Vite** 前端与 **Python FastAPI** 后端，结合大语言模型（LLM）的架构设计信息检索与阅读工具。

  用户输入建筑相关的搜索词后，系统通过 LLM 将搜索词拆解为关键词，从 ArchDaily 搜索并抓取相关项目文章与配图，再由 LLM
  对文章进行摘要总结，最终以卡片网格的形式在页面中呈现，帮助用户快速浏览建筑项目。

  ## 主要功能

  - **搜索词智能拆解**：通过 LLM 将建筑搜索请求提炼为风格、特点、设计师等关键词
  - **ArchDaily 搜索与抓取**：自动搜索 ArchDaily 项目，抓取文章正文与配图链接
  - **LLM 文章总结**：并发调用 LLM 对文章进行结构化摘要，并将原文链接追加到结尾
  - **卡片式阅读界面**：文章以卡片网格展示，支持悬停词语提示、图片弹窗、边框高亮与原文链接跳转

  ## 技术栈

  - **前端**：Vue 3、Vue Router 4、Vite 5、Axios
  - **后端**：Python FastAPI、requests、BeautifulSoup4、tqdm
  - **代理服务**：Express（可选辅助服务）
  - **大模型**：外部 Spring AI 服务（`http://localhost:8081/ai/chat`）

  ## 系统架构

  ```text
  ┌────────────┐   POST /api/vue-data   ┌────────────────────────────────┐
  │  前端 Vue   │ ────────────────────▶ │        FastAPI 后端 (8002)     │
  │  (3003)    │                        │                                │
  │            │   GET /api/summary ◀──│  ①  llm拆解搜索词.py            │
  │ HomePage   │   GET /api/pics ◀─────│      LLM 将搜索词拆解为关键词    │
  └─────┬──────┘                        │  ②  爬取archdaily搜索界面.py    │
        │                               │      抓取搜索结果的标题与链接     │
        │                               │  ③  爬取archdaily文章.py        │
        │                               │      逐篇抓取正文与图片链接       │
        │                               │  ④  llm总结文章list.py          │
        │                               │      并发 LLM 总结（线程池）     │
        │                               │  ⑤  结果写入 vue_data.json      │
        │                               │      / pics_data.json          │
        │                               └───────────────┬────────────────┘
        │                                                │ 请求
        │                               ┌───────────────▼──────────────────┐
        │                               │   外部 Spring AI (8081) LLM 服务  │
        │                               │   POST /ai/chat {prompt, chatId} │
        │                               └──────────────────────────────────┘
  ```
  数据链路说明：前端将搜索词提交给 FastAPI，后端依次完成「拆解 → 搜索 → 抓取 → 总结」，将结果写入 vue_data.json 与
  pics_data.json 两个 JSON 文件；前端随后通过 /api/summary、/api/pics 读取这两个文件并渲染。

  目录结构

  arch-fast.ai
  ├── index.html                  # 入口 HTML
  ├── vite.config.js              # Vite 配置（开发端口 3003）
  ├── package.json
  ├── server.js                   # Express 搜索词代理（端口 3000，可选）
  ├── src/                        # Vue 前端
  │   ├── main.js
  │   ├── App.vue
  │   ├── router/index.js         # 路由：/、/page-two、/home
  │   ├── services/api.js         # 接口层（FastAPI + Spring AI）
  │   └── views/
  │       ├── PageOne.vue         # 搜索词输入页
  │       ├── PageTwo.vue         # 示例页
  │       └── HomePage.vue        # 卡片展示主页
  └── python文件/fastapi/         # Python 后端
      ├── main.py                 # FastAPI 入口（端口 8002）
      ├── prompt.py               # 集中存放所有 LLM 提示词
      ├── llm拆解搜索词.py         # 搜索词拆解
      ├── llm总结文章list.py       # 文章并发总结
      ├── 爬取archdaily搜索界面.py  # ArchDaily 搜索抓取
      ├── 爬取archdaily文章.py      # ArchDaily 文章/图片抓取
      ├── vue_data.json           # 文章总结结果（生成物）
      └── pics_data.json          # 图片链接结果（生成物）

  本地运行

  说明：完整流程依赖外部的 Spring AI LLM 服务运行在 http://localhost:8081/ai/chat，未启动时 LLM
  相关步骤（拆解/总结）会失败。

  1. 前端

  npm install
  npm run dev        # 开发服务器：http://localhost:3003

  2. Python 后端

  pip install fastapi uvicorn requests beautifulsoup4 tqdm
  cd python文件/fastapi
  python main.py     # FastAPI：http://localhost:8002

  3.（可选）Express 代理

  npm run server     # http://localhost:3000

  端口一览

  ┌───────────────────┬──────┬────────────┐
  │       服务         │ 端口 │    说明    │
  ├───────────────────┼──────┼────────────┤
  │ 前端开发服务器      │ 3003 │ Vite       │
  ├───────────────────┼──────┼────────────┤
  │ FastAPI 后端       │ 8002 │ 主流程后端 │
  ├───────────────────┼──────┼────────────┤
  │ Express 代理       │ 3000 │ 可选       │
  ├───────────────────┼──────┼────────────┤
  │ Spring AI（外部）  │ 8081 │ LLM 服务   │
  └───────────────────┴──────┴────────────┘
