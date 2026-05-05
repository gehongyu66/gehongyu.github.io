#!/usr/bin/env python3
import json, os, re
from datetime import datetime

with open('ai_news_data.json', 'r', encoding='utf-8') as f:
    news_items = json.load(f)

today = datetime.now().strftime('%Y-%m-%d')
date_cn = datetime.now().strftime('%Y年%m月%d日')

# 分类新闻
intl_news = []  # 国际
cn_news = []    # 国内
tech_news = []  # 开源/技术

ai_keywords_intl = ['google', 'openai', 'microsoft', 'anthropic', 'meta', 'apple', 'amazon', 'nvidia', 'gpt', 'claude', 'gemini', 'llm', 'hugging face', 'stable diffusion', 'musk', 'twitter', 'x.ai']
ai_keywords_cn = ['百度', '阿里', '腾讯', '字节', '华为', '科大讯飞', '商汤', '旷视', '字节跳动', '大模型', '文心', '通义千问', '豆包', '智谱', 'minimax', '月之暗面']
ai_keywords_tech = ['github', 'open source', '开源', 'hugging face', 'arxiv', 'paper', 'langchain', 'cursor', 'stable diffusion', 'llama', 'mistral', 'qwen']

for news in news_items:
    title = news.get('title', '').lower()
    summary = news.get('summary', '').lower()
    source = news.get('source', '')

    if any(kw in title or kw in summary for kw in ai_keywords_intl):
        intl_news.append(news)
    elif any(kw in title or kw in summary for kw in ai_keywords_cn):
        cn_news.append(news)
    elif any(kw in title or kw in summary for kw in ai_keywords_tech):
        tech_news.append(news)
    else:
        if '36kr' in source or '机器之心' in source:
            cn_news.append(news)
        else:
            intl_news.append(news)

# 取前5条
intl_news = intl_news[:5]
cn_news = cn_news[:5]
tech_news = tech_news[:3]

# 开篇导语
intro = f'''AI行业又迎来激动人心的一天。从硅谷到北京，大模型军备竞赛持续升温，开源与闭源的角力愈发精彩。让我们一起来看看今天都发生了什么。

'''

# 生成文章
article = f'''---
title: "【AI日报】{date_cn}"
date: {today} 12:00:00
tags: [AI, 热点, 日报, 全球AI, 工具推荐]
categories: AI日报
author: AI日报
---

## 【AI日报】{date_cn}

{intro}

---

## 核心事件详述

### 国际AI动态

'''

# 国际事件
for i, news in enumerate(intl_news[:3], 1):
    title = re.sub(r'<[^>]+>', '', news.get('title', ''))
    summary = re.sub(r'<[^>]+>', '', news.get('summary', ''))[:300]
    link = news.get('link', '#')
    source = news.get('source', 'Unknown')
    article += f'''**{i}. {title}**

{summary}...

📌 **意义**：这条新闻反映了{"国际AI竞争格局的变化" if "google" in title.lower() or "openai" in title.lower() or "microsoft" in title.lower() else "AI技术发展的最新趋势"}。

[阅读原文]({link})

---

'''

# 国内事件
if cn_news:
    article += '### 国内AI进展\n\n'
    for i, news in enumerate(cn_news[:3], 1):
        title = re.sub(r'<[^>]+>', '', news.get('title', ''))
        summary = re.sub(r'<[^>]+>', '', news.get('summary', ''))[:300]
        link = news.get('link', '#')
        source = news.get('source', 'Unknown')
        article += f'''**{i}. {title}**

{summary}...

📌 **意义**：{"国内大厂正在加速AI布局" if any(kw in title.lower() for kw in ['百度', '阿里', '腾讯', '字节', '华为']) else "国内AI生态持续繁荣"}。

[阅读原文]({link})

---

'''

# 深度分析
article += f'''## 深度分析

今天的事件再次证明，AI行业正在经历三个重要转变：

**1. 从实验室到商业化**
大模型正在从"炫技"走向"实用"。无论是GPT-4o的多模态升级，还是国内厂商的能力提升，都指向一个趋势：2024年将成为AI应用爆发的元年。

**2. 开源与闭源的较量**
Meta开源Llama系列、阿里开源Qwen系列，正在动摇闭源模型的商业护城河。开源社区的活跃度成为衡量AI生态的重要指标。

**3. 监管与创新并重**
政府开始深度参与AI治理，这既是挑战也是机会。合规能力将成为AI企业的核心竞争力。

---

## 免费AI羊毛专区

本周免费工具推荐：

| 工具名称 | 简介 | 入口地址 | 使用方法 |
|---------|------|---------|---------|
| **Cursor** | 免费AI编程工具 | cursor.sh | 下载后用GitHub账号登录即可使用 |
| **Hugging Face Spaces** | 免费AI模型体验 | huggingface.co/spaces | 浏览器直接访问，无需注册 |
| **通义千问API** | 阿里免费API额度 | qwen.ai | 注册后每月100万token免费额度 |
| **文心一言** | 百度免费体验 | yiyan.baidu.com | 百度账号直接登录 |

> 💡 **小提示**：以上工具均无需特殊网络即可访问，适合国内用户薅羊毛。

---

## 结语与展望

今天的AI日报就到这里。明天值得关注的是：{"GPT-5的任何新动向" if intl_news else "各大厂商可能的新动作"}。如果觉得内容有帮助，欢迎转发给更多朋友！

---

## 参考资料

'''

# 添加参考资料
all_refs = intl_news + cn_news
for news in all_refs[:8]:
    title = re.sub(r'<[^>]+>', '', news.get('title', ''))[:50]
    link = news.get('link', '#')
    source = news.get('source', 'Unknown')
    article += f'- [{source}] {title}...\n'

article += f'''
*本文由 AI 日报自动整理，内容源包括 TechCrunch、The Verge、Ars Technica、Wired、36Kr、机器之心等。*
'''

filename = f'source/_posts/ai-daily-{today}.md'
os.makedirs('source/_posts', exist_ok=True)
with open(filename, 'w', encoding='utf-8') as f:
    f.write(article)
print(f'Article generated: {filename}')

# 自动推送到GitHub
import subprocess
try:
    subprocess.run(['git', 'add', 'source/_posts/', 'ai_news_data.json'], cwd='E:/blogs/myblogs', check=True, shell=True)
    subprocess.run(['git', 'commit', '-m', f'AI日报: {today} 全球AI热点'], cwd='E:/blogs/myblogs', check=True, shell=True)
    subprocess.run(['git', 'push'], cwd='E:/blogs/myblogs', check=True, shell=True)
    print('Pushed to GitHub successfully')
except subprocess.CalledProcessError as e:
    print(f'Push failed: {e}')