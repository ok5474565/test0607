import streamlit as st
from count import main as count_main
from ciyuntu import main as ciyuntu_main

# 创建侧边栏
st.sidebar.title("功能选择")
choice = st.sidebar.selectbox(
    "选择一个功能:",
    ("文本分词与高频词统计", "文本分词、高频词统计与词云图生成")
)

if choice == "文本分词与高频词统计":
    # 调用 count.py 文件的 main 函数
    count_main()
elif choice == "文本分词、高频词统计与词云图生成":
    # 调用 ciyuntu.py 文件的 main 函数
    ciyuntu_main()
else:
    st.sidebar.write("请选择一个有效选项。")
