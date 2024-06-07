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
    st.title("新闻爬虫")
    
    # 设置URL的基础部分和结束部分
    url_base = "http://www.chinanews.com/scroll-news/"
    # 注意这里不需要在年份前添加斜杠
    
    # 允许用户输入日期，并格式化为"年/月日"格式
    date_input = st.date_input("请输入想要爬取的日期", datetime.now())
    year = date_input.year
    month = f"{date_input.month:02d}"  # 月份补零
    day = f"{date_input.day:02d}"      # 日期补零
    # 组合年/月/日，确保年和月日之间有一个斜杠
    date_str = f"{year}/{month}{day}"
    
    # 根据用户输入的日期生成完整的URL
    url = url_base + date_str + "/news.shtml"  # 确保news前面没有多余的斜杠
    
    st.write(f"您选择的日期是: {date_str}")
    st.write(f"正在爬取的URL: {url}")
    
    # 限制爬取的新闻数量
    max_news = st.number_input("请输入要爬取的新闻数量", min_value=1, max_value=100, value=30)
    
    # 按钮触发爬虫程序
    crawl_button = st.button("开始爬取")
    
    if crawl_button:
        news_list, news_count = crawlAll(url, max_news)
        if news_count > 0:
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
