import streamlit as st
import jieba
from collections import Counter
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import pandas as pd

# 辅助函数，用于清理标题中的非法字符
def sanitize_word(word, illegal_chars):
    return ''.join([char for char in word if char not in illegal_chars])

# 定义去停用词的函数
def remove_stopwords(words, stopwords):
    return [word for word in words if word not in stopwords]

# 在Streamlit中显示应用程序
def main():
    st.title("文本分词、高频词统计与词云图生成")
    
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
        illegal_chars = [':','"','|','/','\\\\','*','<','>','?']
        
        # 清理非法字符并去除停用词
        sanitized_words = [sanitize_word(word, illegal_chars) for word in words if word]
        filtered_words = remove_stopwords(sanitized_words, stopwords)
        
        # 统计词频
        word_freq = Counter(filtered_words)
        
        # 获取不同数量的高频词
        top_k_for_bar = 10  # 条形图取前10个高频词
        top_k_for_wordcloud = 30  # 词云图取前30个高频词
        
        # 根据top_k_for_bar获取条形图需要的高频词
        top_words_for_bar = word_freq.most_common(top_k_for_bar)
        
        # 根据top_k_for_wordcloud获取词云图需要的高频词
        top_words_for_wordcloud = word_freq.most_common(top_k_for_wordcloud)
        
        # 创建词云图的频率字典
        wordcloud_freq = {word: freq for word, freq in top_words_for_wordcloud}
        
        # 设置中文字体路径
        font_path = 'simhei.ttf'  # 请确保这个路径是正确的
        
        # 生成并显示词云图
        wc = WordCloud(font_path=font_path, background_color='white').generate_from_frequencies(wordcloud_freq)
        st.image(wc, use_column_width=True)
        
        # 创建条形图的数据框
        top_words_df_bar = pd.DataFrame(top_words_for_bar, columns=['Word', 'Frequency'])
        
        # 反转DataFrame，因为我们想要按降序显示高频词
        top_words_df_bar = top_words_df_bar.sort_values(by='Frequency', ascending=False).reset_index(drop=True)
        
        # 显示高频词
        st.write("高频词条形图（前10）:")
        st.dataframe(top_words_df_bar)
        
        # 生成条形图
        st.bar_chart(top_words_df_bar.set_index('Word')['Frequency'])

if __name__ == '__main__':
    main()
