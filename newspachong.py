import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from io import BytesIO
from datetime import datetime

# 参考文献：https://blog.csdn.net/weixin_44485744/article/details/109563474

# 用request和BeautifulSoup处理网页
def requestOver(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

# 辅助函数，用于清理标题中的非法字符
def sanitize_title(title):
    illegal_chars = [':','"','|','/','\\','*','<','>','?']
    title = "".join([c for c in title if c not in illegal_chars])
    return title

# 从网页下载标题和内容到内存中的文件对象
def download(content, title):
    filename = sanitize_title(title) + '.txt'
    file = BytesIO()
    file.write(content.encode('utf-8'))
    return file, filename

# 爬虫具体执行过程
def crawlAll(url, max_news):
    soup = BeautifulSoup(requestOver(url), 'html.parser')
    news_list = []
    count = 0
    
    for s in soup.findAll("div", class_="content_list"):
        for tag in s.findAll("li"):
            sp = tag.findAll("a")
            if "财经" in str(sp):  # 假设我们只对包含'财经'的链接感兴趣
                title = sp[1].string.strip()
                href = sp[1]['href']
                if not href.startswith(('http:', 'https:')):
                    urlAll = "http://www.chinanews.com" + href
                else:
                    urlAll = href
                article_soup = BeautifulSoup(requestOver(urlAll), 'html.parser')
                tag_article = article_soup.find('div', class_="left_zw")
                if tag_article:
                    content = " ".join(tag_article.stripped_strings)
                    file, filename = download(content, title)
                    news_list.append((file, filename, title))
                    count += 1
                if count >= max_news:
                    break
    return news_list, count

# Streamlit 应用程序的主函数
def main():
    st.title("新闻爬虫")
    
    max_news = st.number_input("请输入要爬取的新闻数量", min_value=1, max_value=100, value=30)
    
    # 允许用户选择日期
    date = st.date_input("请选择新闻的日期", datetime.now())
    year, month, day = date.year, date.month, date.day
    # 格式化日期为"年月日"的形式，确保两位数的月和日
    formatted_date = f"{year}/{str(month).zfill(2)}{str(day).zfill(2)}"
    # 动态生成URL
    url = f"http://www.chinanews.com/scroll-news/{formatted_date}/news.shtml"
    
    st.write(f"正在爬取的URL: {url}")
    
    # 执行爬虫
    news_list, news_count = crawlAll(url, max_news)
    
    # 显示下载按钮
    for file, filename, title in news_list:
        file.seek(0)  # 重置文件指针到开头
        with st.spinner(f'Downloading {title}...'):
            st.download_button(
                label=f"下载: {filename}",
                data=file,
                file_name=filename,
                mime="text/plain"
            )
    
    st.write(f"共爬取了{news_count}篇新闻。")
    st.write("已爬取完成")

if __name__ == '__main__':
    main()
