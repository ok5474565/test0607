import streamlit as st
import jieba
from collections import Counter
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import pandas as pd

st.audio("1132983854.mp3", format="audio/mp3")

# 辅助函数，用于清理标题中的非法字符
def sanitize_word(word, illegal_chars):
    return ''.join([char for char in word if char not in illegal_chars])

# 定义去停用词的函数
def remove_stopwords(words, stopwords):
    return [word for word in words if word not in stopwords]

# 生成词云图
def generate_wordcloud(frequencies, font_path, width=800, height=600):
    # 创建词云对象
    wc = WordCloud(
        font_path=font_path,
        background_color='white',
        max_words=200,
        width=width,  # 设置词云图的宽度
        height=height  # 设置词云图的高度
    ).generate_from_frequencies(frequencies)
    
    # 显示词云图
    image = wc.to_image()
    st.image(image, use_column_width=True)  # 根据需要调整图像大小

# 主函数
def main():
    #st.title("文本分词、高频词统计与词云图生成")
    
    # 设置上传文件的按钮
    uploaded_file = st.file_uploader("请上传你的文本文件", type=["txt"])
    
    if uploaded_file is not None:
        # 读取文件内容
        text = uploaded_file.read().decode('utf-8')
        
        # 使用jieba进行分词
        words = jieba.lcut(text)
        
        # 读取停用词典文件
        with open('stopwords.txt', 'r', encoding='utf-8') as f:
            stopwords = f.read().splitlines()
        
        # 定义非法字符列表
        illegal_chars = [':','"','|','/','\\','*','<','>','?']
        
        # 清理非法字符并去除停用词
        sanitized_words = [sanitize_word(word, illegal_chars) for word in words if word]
        filtered_words = remove_stopwords(sanitized_words, stopwords)
        
        # 统计词频
        word_freq = Counter(filtered_words)
        
        # 获取高频词
        top_words = word_freq.most_common(50)
        
        # 创建词云图的频率字典
        wordcloud_freq = {word: freq for word, freq in top_words}
        
        # 设置中文字体路径
        font_path = 'simhei.ttf'  # 请确保这个路径是正确的

        # 显示词云图的标题
        st.write("以下是生成的词云图：")
        
        # 生成并显示词云图
        generate_wordcloud(wordcloud_freq, font_path)
        
        # 显示高频词
        st.write("高频词统计:")
        top_words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
        st.dataframe(top_words_df)

if __name__ == '__main__':
    main()
