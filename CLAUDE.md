# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"Arch-Fast AI" is a Chinese-language architecture-search app. A user types an architecture search term, an LLM decomposes it into keywords, the app scrapes ArchDaily for matching projects, scrapes the full article text + images from each project page, LLM-summarizes each article, and renders the summaries as a grid of cards in the browser.

The repo has three independently-run services:

| Service | Tech | Port | Entry point |
|---|---|---|---|
| Frontend | Vue 3 + Vite | 3003 | `npm run dev` |
| Python backend | FastAPI | 8002 | `python文件/fastapi/main.py` |
| Search-term proxy | Express (CommonJS) | 3000 | `npm run server` |

The LLM itself is **external**: an unversioned Spring AI backend expected at `http://localhost:8081/ai/chat`. Both the frontend (`src/services/api.js`) and the Python pipeline POST to that endpoint with form data `{ prompt, chatId }`.

## Commands

```bash
npm install          # install JS deps
npm run dev          # Vite dev server on port 3003
npm run build        # production build
npm run preview      # preview the production build
npm run server       # Express proxy on port 3000 (CommonJS; note "type": "module" is set in package.json)
```

Python backend (no requirements.txt; deps: fastapi, uvicorn, requests, beautifulsoup4, tqdm):

```bash
cd "python文件/fastapi" && python main.py       # uvicorn on port 8002
# or: uvicorn main:app --port 8002
```

There is no test framework, linter, or formatter configured.

## Architecture

### Frontend (`src/`)
- `main.js` mounts `App.vue` with the router; `App.vue` is just `<router-view>`.
- `router/index.js`: three routes — `/` (PageOne), `/page-two` (PageTwo), `/home` (HomePage).
- `views/PageOne.vue`: input box; on Enter sends the search term to FastAPI via `sendVueData()`.
- `views/HomePage.vue`: the main display. On mount it fetches summaries and image URLs from FastAPI (`getSummary`, `getPicsUrls`) and renders one card per summary. It renders summary text with `v-html`, with hover tooltips (ranges + messages), per-card image popups, border toggling, and an article link extracted from a trailing `文章链接为：` pattern.
- `services/api.js` is the single API layer. It exposes two sets of calls:
  - `chatAPI` → Spring AI on `http://localhost:8081` (streaming chat, chat-history retrieval). Used for chat features, not the main search flow.
  - axios calls → FastAPI on `http://localhost:8002` (`sendVueData`, `getSummary`, `getPicsUrls`).

### Python pipeline (`python文件/fastapi/`)
The core flow lives in `main.py` → `POST /api/vue-data`:
1. `llm拆解搜索词.py:optimize_text()` — asks the LLM to reduce the search term to bare keyword nouns (no adjectives).
2. `爬取archdaily搜索界面.py:fetch_archdaily_urls()` — hits ArchDaily's search API, returns article titles + URLs.
3. `爬取archdaily文章.py:fetch_archdaily_articles()` — scrapes article body + image links from each URL (BeautifulSoup + regex; extracts from between `<span class="afd-specs__value">` and the `<h2>项目图库</h2>` marker).
4. `llm总结文章list.py:optimize_articles()` — LLM-summarizes articles concurrently via `ThreadPoolExecutor` (default `max_workers=200`), using `chatId` = index.
5. Appends `\n文章链接为：<url>` to each summary, then writes results to `vue_data.json` and `pics_data.json`.

`GET /api/summary` and `GET /api/pics` read those same two JSON files back — **the JSON files are the hand-off mechanism / data store between pipeline and frontend**, not a database. Deleting or editing them changes what the frontend displays.

`prompt.py` centralizes all LLM prompts and reusable test data. `shared_data.py` is a near-empty module used only by commented-out code.

Other scrapers (`爬取古德网*.py`, `提取需解释的词语.py`, `测试（正式版）.py`, `爬虫/`) exist but are not currently wired into the main pipeline.

## Critical Conventions

- **Chinese is the working language.** Comments, prompts, variable names, function names, and file names are in Chinese. Python identifiers are valid non-ASCII (e.g. `llm拆解搜索词.py`, `拆解完成词`, `总结内容list`). Imports reference these exact names — do not rename them to ASCII without updating every import.
- The `vue_data.json` / `pics_data.json` files are generated artifacts in the `python文件/fastapi/` working directory; they are read on every `GET /api/summary` and `GET /api/pics` call.
- Ports are fixed in multiple places: Vite dev = 3003 (`vite.config.js`), FastAPI = 8002 (`main.py`), Express = 3000 (`server.js`), LLM = 8081 (hardcoded in `src/services/api.js` and all Python LLM-call modules).
- The full search flow requires the external Spring AI backend on 8081 running, or every LLM call fails.
- `__MACOSX/` at the repo root is leftover junk from a zip extraction (a stale `my-vue-app` copy).
