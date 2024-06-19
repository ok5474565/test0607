import streamlit as st

def main():
    st.title("视频播放示例")
    # 请确保视频文件路径是正确的
    video_file_path = "279233.mp4"
    
    # 确保 width 和 height 是整数类型
    width = 600
    height = 400
    
    # 使用 st.video 嵌入视频，并设置宽度和高度
    st.video(video_file_path, width=width, height=height)

if __name__ == "__main__":
    main()
