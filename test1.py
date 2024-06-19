import streamlit as st

def main():
    st.title("视频播放示例")
    video_file_path = "279233.mp4"
    
    # 创建一个列，并将视频放入其中
    col1 = st.columns([1, 2])  # 这里创建了一个两列布局，视频放在第二列
    with col1[1]:  # 选择第二列
        st.video(video_file_path)  # 视频会自动适应列的宽度

if __name__ == "__main__":
    main()
