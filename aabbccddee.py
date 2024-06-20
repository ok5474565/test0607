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

# 定义高频词统计的函数
def get_top_words(words, top_k):
    counter = Counter(words)
    return counter.most_common(top_k)

# 生成词云图
def generate_wordcloud(frequencies, font_path, width=800, height=600):
    try:
        wc = WordCloud(
            font_path=font_path,
            background_color='white',
            max_words=200,
            width=width,
            height=height
        ).generate_from_frequencies(frequencies)
        image = wc.to_image()
        return image
    except Exception as e:
        # 打印错误信息，或者将其记录到日志中
        print(f"Error generating wordcloud: {e}")
        # 可以在这里返回一个占位图像或者None
        return None

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
        filtered_words = remove_stopwords(sanitized_words, set(stopwords))
        
        # 统计词频
        word_freq = Counter(filtered_words)
        
        # 获取高频词
        top_k = 10
        top_words = get_top_words(filtered_words, top_k)
        
        # 直接使用整个词频字典来创建词云图的频率字典
        wordcloud_freq = dict(word_freq)
        
        # 设置中文字体路径
        font_path = 'simhei.ttf'  # 请确保这个路径是正确的
        
        # 生成并显示词云图
        wordcloud_image = generate_wordcloud(wordcloud_freq, font_path)
        st.image(wordcloud_image, use_column_width=True)
        
        # 创建条形图的数据框
        top_words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
        
        # 反转DataFrame，因为我们想要按降序显示高频词
        top_words_df = top_words_df.sort_values(by='Frequency', ascending=False).reset_index(drop=True)
        
        # 显示高频词
        st.write("高频词统计:")
        st.dataframe(top_words_df)
        
        # 生成条形图
        st.bar_chart(top_words_df.set_index('Word')['Frequency'])

if __name__ == '__main__':
    main()
