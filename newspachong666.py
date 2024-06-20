import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from io import BytesIO
from zipfile import ZipFile
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
def crawlAll(url, max_news, categories):
    soup = BeautifulSoup(requestOver(url), 'html.parser')
    global news_list
    news_list = []  # 存储新闻文件的列表
    count = 0
    
    for s in soup.findAll("div", class_="content_list"):
        for tag in s.findAll("li"):
            sp = tag.findAll("a")
            # 检查新闻链接是否包含用户选择的任意一个类别
            if any(cat in str(sp) for cat in categories):
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
                    news_list.append((file, filename, title))  # 添加到列表
                    count += 1
                if count >= max_news:
                    break
    return news_list, count

# 用于生成zip文件的函数
def get_zipfile(files):
    in_memory_file = BytesIO()
    with ZipFile(in_memory_file, 'w') as zf:
        for file, filename, _ in files:
            file.seek(0)
            zf.writestr(filename, file.getvalue())
    in_memory_file.seek(0)
    return in_memory_file

# Streamlit 应用程序的主函数
def main():
    
    st.title("新闻爬虫")
    st.audio("1132983854.mp3", format="audio/mp3")

    # 允许用户选择感兴趣的新闻类别
    categories = ["教育", "科技", "体育", "娱乐", "财经", "国内", "国际"]  # 假设有这些类别
    user_selected_categories = st.multiselect("选择感兴趣的新闻类别", categories, default=categories)
  
    max_news = st.number_input("请输入要爬取的新闻数量", min_value=1, max_value=100, value=30)
    
    # 允许用户选择日期
    date = st.date_input("请选择新闻的日期", datetime.now())
    year, month, day = date.year, date.month, date.day
    # 格式化日期为"年月日"的形式，确保两位数的月和日
    formatted_date = f"{year}/{str(month).zfill(2)}{str(day).zfill(2)}"
    # 动态生成URL
    url = f"http://www.chinanews.com/scroll-news/{formatted_date}/news.shtml"
    
    st.write(f"将要爬取的URL: {url}")
    
    # 创建一个按钮，当用户点击时执行爬取操作
    crawl_button = st.button("开始爬取")
    
    if crawl_button:
        # 执行爬虫
        news_list, news_count = crawlAll(url, max_news, user_selected_categories)
        
        # 显示单独的下载按钮
        for file, filename, title in news_list:
            file.seek(0)  # 重置文件指针到开头
            with st.spinner(f'Downloading {title}...'):
                st.download_button(
                    label=f"下载: {filename}",
                    data=file,
                    file_name=filename,
                    mime="text/plain"
                )
        
        # 添加下载全部的按钮
        if news_list:
            with st.spinner("正在打包文件..."):
                download_all_button = st.download_button(
                    label="下载全部文件",
                    data=get_zipfile(news_list),
                    file_name="news_files.zip",
                    mime="application/zip"
                )
        
        st.write(f"共爬取了{news_count}篇新闻。")
        st.write("已爬取完成")

if __name__ == '__main__':
    main()
