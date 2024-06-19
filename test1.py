import streamlit as st

def main():
    st.title("视频播放示例")
    # 假设您的视频文件位于应用程序的相同目录中
    video_file = open("path_to_your_video.mp4", "rb")
    st.video(video_file)

if __name__ == "__main__":
    main()
