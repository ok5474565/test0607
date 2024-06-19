import streamlit as st

def main():
    st.title("视频播放示例")
    # 请确保视频文件路径是正确的
    video_file_path = "279233.mp4"
    
    # 使用 st.video 嵌入视频
    st.video(video_file_path)

if __name__ == "__main__":
    main()
