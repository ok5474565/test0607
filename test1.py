import streamlit as st

def main():
    st.title("视频播放示例")

    # 假设您的视频文件位于应用程序的相同目录中
    video_file_path = "277293.mp4"
    
    # 使用视频文件路径而不是文件对象
    st.video(video_file_path, width=600, height=400)

if __name__ == "__main__":
    main()
