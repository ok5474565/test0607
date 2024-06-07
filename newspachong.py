import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from io import BytesIO
from datetime import datetime

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
    file.seek(0)
    return file, filename

# 爬虫具体执行过程
def crawlAll(url, max_news):
    y = 1
    soup = BeautifulSoup(requestOver(url), 'html.parser')
    for s in soup.findAll("div", class_="content_list"):
        for tag in s.findAll("li"):
            sp = tag.findAll("a")
            if "财经" in str(sp):  # 假设我们只对包含'财经'的链接感兴趣
                title = sp[1].string.strip()
                urlAll = url + sp[1]['href']
                article_soup = BeautifulSoup(requestOver(urlAll), 'html.parser')
                tag_article = article_soup.find('div', class_="left_zw")
                if tag_article:
                    content = " ".join(tag_article.stripped_strings)
                    file, filename = download(content, title)
                    if file:
                        with st.spinner(f'Downloading {title}...'):
                            st.download_button(
                                label=f"下载: {filename}",
                                data=file.getvalue(),
                                file_name=filename,
                                mime="text/plain"
                            )
                y += 1
                if y > max_news:
                    break
    return y

# Streamlit 应用程序的主函数
def main():
    st.title("新闻爬虫")
    
    # 设置URL的基础部分和结束部分
    url_base = "http://www.chinanews.com/scroll-news/"
    url_end = "/news.shtml"
    
    # 允许用户输入日期
    date_input = st.date_input("请输入想要爬取的日期", datetime.now())
    
    # 根据用户输入的日期生成完整的URL
    date_str = date_input.strftime("%Y/%m/%d")
    url = url_base + date_str + url_end
    
    st.write(f"您选择的日期是: {date_str}")
    
    # 限制爬取的新闻数量
    max_news = st.slider("选择要爬取的新闻数量", min_value=1, max_value=100, value=30)
    
    # 按钮触发爬虫程序
    crawl_button = st.button("开始爬取")
    
    if crawl_button:
        y = crawlAll(url, max_news)
        st.write(f"共爬取了{y-1}篇新闻。")
        st.write("已爬取完成")

if __name__ == '__main__':
    main()
