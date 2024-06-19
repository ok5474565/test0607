import streamlit as st

def main():
    st.title("视频播放示例")
    # 假设您的视频文件位于应用程序的相同目录中
    video_file = open("279233.mp4", "rb")
    st.video(video_file,width=400,height=600)

if __name__ == "__main__":
    main()
