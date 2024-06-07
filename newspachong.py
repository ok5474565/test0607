import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from io import BytesIO
from datetime import datetime

# 用request和BeautifulSoup处理网页
def requestOver(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # 确保请求成功
        response.encoding = 'utf-8'
        return response.text
    except requests.exceptions.RequestException as e:
        st.write(f"请求网页时发生错误: {e}")
        return None

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
    file.seek(0)
    return file, filename

# 爬虫具体执行过程
def crawlAll(url, max_news):
    soup = BeautifulSoup(requestOver(url), 'html.parser')
    news_list = []  # 存储新闻信息的列表
    news_count = 0  # 新闻计数器

    for s in soup.findAll("div", class_="content_list"):
        for tag in s.findAll("li"):
            sp = tag.findAll("a")
            if len(sp) >= 2 and "财经" in sp[1].text:  # 检查链接和文本
                title = sp[1].text.strip()
                href = sp[1].get('href')
                if not href.startswith('http'):  # 确保是完整的URL
                    urlAll = url + href
                else:
                    urlAll = href
                article_soup = BeautifulSoup(requestOver(urlAll), 'html.parser')
                tag_article = article_soup.find('div', class_="left_zw")
                if tag_article and news_count < max_news:
                    content = " ".join(tag_article.stripped_strings)
                    news_list.append((title, content, urlAll))  # 将新闻信息存储到列表
                    news_count += 1
    return news_list, news_count

# Streamlit 应用程序的主函数
def main():
    st.title("新闻爬虫")
    
    # 设置URL的基础部分和结束部分
    url_base = "http://www.chinanews.com/scroll-news/"
    url_end = "/news.shtml"
    
    # 允许用户输入日期，格式化日期为"/年月日/"格式
    date_input = st.date_input("请输入想要爬取的日期", datetime.now())
    date_str = date_input.strftime("/%Y/%m/%d/")
    url = url_base + date_str + url_end
    
    st.write(f"您选择的日期是: {date_str[1:-1]}")  # 显示日期，去掉两侧的"/"
    st.write(f"正在爬取的URL: {url}")
    
    # 限制爬取的新闻数量
    max_news = st.number_input("请输入要爬取的新闻数量", min_value=1, max_value=100, value=30)
    
    # 按钮触发爬虫程序
    crawl_button = st.button("开始爬取")
    
    if crawl_button:
        news_list, news_count = crawlAll(url, max_news)
        if news_list:
            for title, content, urlAll in news_list:
                file, filename = download(content, title)
                with st.spinner(f'Downloading {title}...'):
                    st.download_button(
                        label=f"下载: {filename}",
                        data=file.getvalue(),
                        file_name=filename,
                        mime="text/plain"
                    )
            st.write(f"共爬取了{news_count}篇新闻。")
        else:
            st.write("没有找到符合条件的新闻或请求网页失败。")

if __name__ == '__main__':
    main()
