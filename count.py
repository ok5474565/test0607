import streamlit as st
import jieba
from collections import Counter
import pandas as pd


# 辅助函数，用于清理标题中的非法字符
def sanitize_word(word, illegal_chars):
    for char in illegal_chars:
        word = word.replace(char, '')
    return word

# 定义去停用词的函数
def remove_stopwords(words, stopwords_set):
    return [word for word in words if word not in stopwords_set]

# 定义高频词统计的函数
def get_top_words(words, top_k):
    counter = Counter(words)
    return counter.most_common(top_k)

# 在Streamlit中显示应用程序
def main():
    #st.title("文本分词与高频词统计")
    
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
            stopwords_set = set(stopwords)
        
        # 定义非法字符列表
        illegal_chars = [':','"','|','/','\\','*','<','>','?']
        
        # 清理非法字符并去除停用词
        sanitized_words = [sanitize_word(word, illegal_chars) for word in words if word]
        filtered_words = remove_stopwords(sanitized_words, stopwords_set)
        
        # 设置要统计的高频词数量
        top_k = 10
        top_words = get_top_words(filtered_words, top_k)
        
        # 创建条形图的数据框
        top_words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
        
        # 反转DataFrame，因为我们想要按降序显示高频词
        top_words_df = top_words_df.sort_values(by='Frequency', ascending=False).reset_index(drop=True)

        # 使用Markdown添加图名
        st.markdown("## 条形图：高频词统计", unsafe_allow_html=True)
        
        # 显示高频词
        st.write("高频词统计:")
        st.dataframe(top_words_df)
        
        # 生成条形图
        # 由于我们想要x轴显示'Word'列，我们将使用'Word'列作为x轴，'Frequency'作为y轴
        st.bar_chart(top_words_df.set_index('Word')['Frequency'])

if __name__ == '__main__':
    main()
