import requests
from bs4 import BeautifulSoup
import streamlit as st
from io import BytesIO
from datetime import datetime

# 用request和BeautifulSoup处理网页
def requestOver(url):
    try:
        response = requests.get(url)
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

    # 假设新闻列表在某个具体的class下，这里需要根据实际页面结构调整
    for news in soup.find_all("div", class_="news-item"):  # 根据实际class名称修改
        title = news.find("h2").text.strip() if news.find("h2") else "无标题"
        href = news.find("a")['href'] if news.find("a") else ""
        if href.startswith('http'):
            urlAll = href
        else:
            urlAll = url + href
        article_soup = BeautifulSoup(requestOver(urlAll), 'html.parser')
        # 假设新闻内容在某个具体的class下，这里需要根据实际页面结构调整
        content = article_soup.find("div", class_="article-content").text.strip() if article_soup.find("div", class_="article-content") else "无内容"
        news_list.append((title, content, urlAll))
        news_count += 1
        if news_count >= max_news:
            break

    return news_list, news_count

# Streamlit 应用程序的主函数
def main():
    st.title("新闻爬虫")  # 设置网页标题
    
    max_news = 30  # 限制爬取的新闻数量为30
    
    # 使用date_input让用户选择日期
    date_selected = st.date_input("请选择要爬取新闻的日期", datetime.datetime.now())
    
    # 格式化日期为 "YYYY/MMDD" 格式
    year = date_selected.year
    month = f"{date_selected.month:02d}"  # 月份补零
    day = f"{date_selected.day:02d}"      # 日期补零
    date_str = f"{year}/{month}{day}"
    
    # 动态生成URL
    url_base = "http://www.chinanews.com/scroll-news/{}/news.shtml"
    url = url_base.format(date_str)
    
    # 创建存储新闻的文件夹路径
    current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_path = os.path.join(r'D:\0521', current_datetime)
    os.makedirs(folder_path, exist_ok=True)
    
    # 清空页面输出，以便重新运行时不显示旧内容
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
    main()  # 直接调用main函数
