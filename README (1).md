# qian1 - 每日 AI 推送

这个文件夹里的 2 个文件，就是放到你的 `qian1` 仓库里就能跑起来的每日推送。

## 包含的文件
- `.github/workflows/daily-ai-news.yml` — 每天北京时间 09:38 自动跑一次，也可以在 GitHub 网页上手动点 Run workflow
- `scripts/fetch_ai_news.py` — 生成当天资讯的脚本，数据来自 Hacker News 公开接口，无需 Key

## 怎么放进 qian1（仓库现在是空的，用网页上传最快）
1. 打开 https://github.com/yesha-afk/qian1
2. 点 `uploading an existing file`（或 Add file -> Upload files）
3. 把这个文件夹里的 3 个文件按原路径上传：
   - `.github/workflows/daily-ai-news.yml`
   - `scripts/fetch_ai_news.py`
   - `README.md`（可选）
   注意：`.github` 是隐藏文件夹，上传时要保持路径不变
4. 上传完成后，去仓库的 `Actions` 标签页，点 `Daily AI News`，点 `Run workflow` 手动跑一次测试
5. 跑成功后，仓库里会出现 `docs/ai-news/2026-10-17.md` 这样的文件，之后每天 09:38 自动更新

## 如果用 git 命令行
```bash
git clone https://github.com/yesha-afk/qian1.git
cd qian1
# 把上面 2 个文件复制到对应路径
git add .
git commit -m "feat: daily AI news"
git push
```

## 说明
- 生成的文件在 `docs/ai-news/YYYY-MM-DD.md`，每天一个
- 现在的脚本用的是 Hacker News 热度排序，后续你可以换成你想要的源（比如 RSS、NewsAPI），只要改 `scripts/fetch_ai_news.py` 就行
- 如果你想让我这边的每日聊天推送也继续保留，可以两个都留着：聊天里看摘要，仓库里看存档
