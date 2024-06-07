import os
import requests
from bs4 import BeautifulSoup
import datetime
import streamlit as st  # 导入streamlit库

# 用requests和BeautifulSoup处理网页
def requestOver(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'html.parser')

# 辅助函数，用于清理标题中的非法字符
def sanitize_title(title):
    illegal_chars = [':','"','|','/','\\','*','<','>','?']
    for char in illegal_chars:
        title = title.replace(char, '')
    return title

# 从网页下载标题和内容到txt文档
def download(title, url, folder_path):
    soup = requestOver(url)
    tag = soup.find('div', class_="left_zw")
    if not tag:
        return
    title = sanitize_title(title)
    content = " ".join(tag.stripped_strings)  # 提取并连接所有段落的文本
    filename = os.path.join(folder_path, title + '.txt')
    with open(filename, 'w', encoding='utf-8', errors='ignore') as file_object:
        file_object.write(title + '\n')
        file_object.write(content)
    st.write(f'正在爬取新闻: {title}')  # 在Streamlit中显示爬取的新闻标题

# 爬虫具体执行过程
def crawlAll(url, max_news, folder_path):
    y = 1
    soup = requestOver(url)
    for s in soup.findAll("div", class_="content_list"):
        for tag in s.findAll("li"):
            sp = tag.findAll("a")
            if "财经" in str(sp):  # 假设我们只对包含'财经'的链接感兴趣
                title = sp[1].string.strip()
                # 假设href属性是相对路径，需要和基础URL拼接
                urlAll = os.path.join(url, sp[1]['href'])
                download(title, urlAll, folder_path)
                y += 1
                if y > max_news:  # 限制爬取的新闻数量
                    break
    return y

# Streamlit 应用程序的主函数
def main():
    st.title("新闻爬虫")
    
    max_news = 30  # 限制爬取的新闻数量
    date_selected = st.date_input("请选择要爬取新闻的日期", datetime.datetime.now())
    
    # 格式化日期为 "YYYY/MMDD" 格式，用于URL
    year = date_selected.year
    month = f"{date_selected.month:02d}".zfill(2)  # 月份补零
    day = f"{date_selected.day:02d}".zfill(2)    # 日期补零
    date_str = f"{year}/{month}{day}"
    
    # 动态生成URL
    url_base = "http://www.chinanews.com/scroll-news/{:%Y/%m/%d}/news.shtml"
    url = url_base.format(date_selected)
    
    # 创建存储新闻的文件夹路径
    current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_path = os.path.join(r'D:\0521', current_datetime)
    os.makedirs(folder_path, exist_ok=True)
    
    st.empty()
    
    # 显示用户选择的日期和URL
    st.write(f"您选择的日期是: {date_str}")
    st.write(f"正在爬取的URL: {url}")
    
    # 执行爬虫
    y = crawlAll(url, max_news, folder_path)
    
    # 显示爬取的新闻数量和完成消息
    st.write(f"共爬取了{y-1}篇新闻。")
    st.write("已爬取完成")

if __name__ == '__main__':
    main()
