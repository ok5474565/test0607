import jieba
import requests
import streamlit as st
from streamlit_echarts import st_echarts
from collections import Counter
from streamlit.logger import get_logger
import re
import string
from pathlib import Path

#http://www.qstheory.cn/yaowen/2022-10/25/c_1129079926.htm

LOGGER = get_logger(__name__)

def clean_text(text):
    text = text.replace('\n', '')
    text = text.replace(' ', '')
    text = text.strip()
    return text

def load_stopwords(filepath):
    stopwords = set()
    if filepath.is_file():
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                stopwords.add(line.strip())
    return stopwords

def segment(text, stopwords):
    punctuation = string.punctuation
    text = text.translate(str.maketrans('', '', punctuation))
    words = jieba.lcut(text)
    words = [word for word in words if word not in stopwords]
    return words

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def extract_body_text(html):
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find('body').get_text()
    return text



LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="",
    )

    st.write("# 作业展示 ")

    url = st.text_input('Enter URL:')

    if url:
        r = requests.get(url)
        r.encoding = 'utf-8'
        text = r.text
        text = extract_body_text(text)
        
        text = remove_html_tags(text)
        text = clean_text(text)

        # 读取本地停用词文件
        stopwords_filepath = Path(__file__).parent / "stopwords.txt"
        stopwords = load_stopwords(stopwords_filepath)

        words = segment(text, stopwords)
        word_counts = Counter(words)
    
        top_words = word_counts.most_common(20)
    
        bar_chart_options = {
            "title": {
                "text": "词语条形图"  # 添加图名
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {
                    "type": "shadow"
                }
            },
            "xAxis": {
                "type": "category",
                "data": [word for word, _ in top_words],
                "axisLabel": {
                    "interval": 0,  # 显示所有标签
                    "rotate": 45    # 旋转标签45度
                },
                "splitLine": {"show": False},
            },
            "yAxis": {
                "type": "value",
                "splitLine": {"show": False},
            },
            "series": [{
                "type": "bar",
                "data": [count for _, count in top_words],
                "itemStyle": {
                    "normal": {
                        "color": {
                            "type": "linear",
                            "x": 0,
                            "y": 0,
                            "x2": 0,
                            "y2": 1,
                            "colorStops": [{
                                "offset": 0, "color": "rgba(255,0,0,1)"  # 开始颜色
                            }, {
                                "offset": 1, "color": "rgba(0,255,0,1)"  # 结束颜色
                            }]
                        }
                    }
                }
            }],
            "visualMap": {
                "type": "continuous",
                "min": min([count for _, count in top_words]),
                "max": max([count for _, count in top_words]),
                "calculable": True,
                "inRange": {
                    "color": ["#00796B", "#FBC02D", "#E53935"]  # 颜色渐变
                }
            }
        }
    
        # 调整图表高度以适应宽度
        st_echarts(bar_chart_options, height='500px')

if __name__ == "__main__":
    run()