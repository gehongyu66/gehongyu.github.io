#!/usr/bin/env python3
import feedparser, json, re, os
from datetime import datetime, timedelta

AI_KEYWORDS = [
    'openai', 'gpt', 'chatgpt', 'claude', 'anthropic', 'gemini', 'google ai',
    'llm', 'large language model', 'stable diffusion', 'midjourney', 'dall-e',
    'machine learning', 'deep learning', 'neural network', 'transformer',
    'artificial intelligence', 'ai model', 'hugging face', 'meta ai',
    'mistral', 'llama', 'qwen', 'copilot', 'cursor', 'github copilot',
    'nvidia', 'gpu', 'tpu', 'agent', 'rag', 'embedding', 'vector database',
    '字节跳动', '百度', '阿里云', '腾讯AI', '华为云', '科大讯飞',
    '大模型', 'AI模型', '人工智能', '生成式AI', 'ChatGPT', '文心一言'
]

def is_ai_related(title, summary=''):
    text = (title + ' ' + summary).lower()
    return any(kw.lower() in text for kw in AI_KEYWORDS)

def fetch_rss(url, source_name):
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:20]:
            title = entry.get('title', '')
            summary = entry.get('summary', '')
            if is_ai_related(title, summary):
                items.append({
                    'title': re.sub(r'<[^>]+>', '', title),
                    'link': entry.get('link', ''),
                    'summary': re.sub(r'<[^>]+>', '', summary)[:300],
                    'published': entry.get('published', ''),
                    'source': source_name
                })
        return items
    except Exception as e:
        print(f'Error fetching {source_name}: {e}')
        return []

all_news = []
rss_urls = [
    ('https://feeds.feedburner.com/TechCrunch/startups', 'TechCrunch'),
    ('https://www.theverge.com/rss/index.xml', 'The Verge'),
    ('https://feeds.arstechnica.com/arstechnica/index', 'Ars Technica'),
    ('https://www.wired.com/feed/rss', 'Wired'),
    ('https://36kr.com/feed', '36Kr'),
    ('https://www.jiqizhixin.com/rss', '机器之心'),
]

for url, name in rss_urls:
    items = fetch_rss(url, name)
    all_news.extend(items)
    print(f'Fetched {len(items)} from {name}')

seen = set()
unique_news = []
for news in all_news:
    title_key = news['title'].lower()[:50]
    if title_key not in seen and len(news['title']) > 10:
        seen.add(title_key)
        unique_news.append(news)

print(f'Total unique AI news: {len(unique_news)}')
with open('ai_news_data.json', 'w', encoding='utf-8') as f:
    json.dump(unique_news, f, ensure_ascii=False, indent=2)

if unique_news:
    print('HAS_NEWS=true')
else:
    print('HAS_NEWS=false')