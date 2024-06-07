import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from io import BytesIO
from datetime import datetime, timedelta

# 其他函数保持不变...

# 用于生成日期列表的函数
def generate_date_options(start_date, end_date):
    date_options = []
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y/%m/%d")
        date_options.append(date_str)
        current_date += timedelta(days=1)
    return date_options

# Streamlit 应用程序的主函数
def main():
    st.title("新闻爬虫")
    
    # 允许用户输入新闻页面的URL
    url_base = "http://www.chinanews.com/scroll-news/"
    url_end = "/news.shtml"
    
    # 设置日期范围，例如从2024年5月30日到2024年6月5日
    start_date = datetime.strptime("2024/05/30", "%Y/%m/%d")
    end_date = datetime.strptime("2024/06/05", "%Y/%m/%d")
    
    # 生成日期列表供用户选择
    date_options = generate_date_options(start_date, end_date)
    date = st.selectbox("请输入想要爬取的日期", date_options)
    
    # 根据用户选择的日期生成完整的URL
    url = url_base + date + url_end
    
    st.empty()
    
    # 限制爬取的新闻数量
    max_news = st.number_input("请输入要爬取的新闻数量", min_value=1, max_value=100, value=30)
    
    # 执行爬虫程序
    y = crawlAll(url, max_news)
    st.write(f"共爬取了{y-1}篇新闻。")
    st.write("已爬取完成")

if __name__ == '__main__':
    main()
