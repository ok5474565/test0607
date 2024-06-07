import os
import requests
from bs4 import BeautifulSoup
import datetime
import streamlit as st  # 导入streamlit库

"""
参考文献：https://blog.csdn.net/weixin_44485744/article/details/109563474
"""

# 用request和BeautifulSoup处理网页
def requestOver(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# 辅助函数，用于清理标题中的非法字符
def sanitize_title(title):
    illegal_chars = [':','"','|','/','\\','*','<','>','?']
    for char in illegal_chars:
        title = title.replace(char, '')
    return title

# 从网页下载标题和内容到txt文档，并提供下载链接
def download(title, content, folder_path):
    title = sanitize_title(title)
    filename = title + '.txt'
    # 将内容写入文件。这里我们不保存到本地，而是直接返回文件对象。
    file = open(os.path.join(folder_path, filename), 'wb')
    file.write(content.encode('utf-8'))
    file.seek(0)  # 移动文件指针到文件开头，以便下载
    return file

# 爬虫具体执行过程
def crawlAll(url, max_news, folder_path):
    y = 1
    soup = requestOver(url)
    for s in soup.findAll("div", class_="content_list"):
        for tag in s.findAll("li"):
            sp = tag.findAll("a")
            if "财经" in str(sp):
                title = sp[1].string.strip()
                urlAll = "http://www.chinanews.com" + sp[1]['href']
                download(title, urlAll, folder_path)  # 传递folder_path
                y += 1
                if y > max_news:  # 限制爬取的新闻数量
                    break
    return y

# Streamlit 应用程序的主函数
def main():
    st.title("新闻爬虫")  # 设置网页标题
    
    max_news = 30  # 限制爬取的新闻数量为30
    current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # 获取当前日期时间
    folder_path = os.path.join(r'D:\0521', current_datetime)  # 创建基于当前时间的文件夹路径
    os.makedirs(folder_path, exist_ok=True)  # 创建文件夹，如果已存在则忽略
    url = "http://www.chinanews.com/scroll-news/2024/0605/news.shtml"   # 示例URL
    
    # 清空页面输出，以便重新运行时不显示旧内容
    st.empty()
    
    # 执行爬虫
    y = crawlAll(url, max_news, folder_path)
    # 显示爬取的新闻数量
    st.write(f"共爬取了{y-1}篇新闻。")
    st.write("已爬取完成")  # 在Streamlit中显示完成消息
    
    # 为每个新闻生成下载按钮
    for title in os.listdir(folder_path):
        if title.endswith('.txt'):
            file_path = os.path.join(folder_path, title)
            with open(file_path, 'rb') as file:
                # 使用st.download_button创建下载按钮
                st.download_button(
                    label=f"下载 {title}",
                    data=file,
                    file_name=title,
                    mime="text/plain"
                )

if __name__ == '__main__':
    main()  # 直接调用main函数
