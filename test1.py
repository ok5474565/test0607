import streamlit as st

def main():
    st.title("在线视频播放示例")
    # 这是YouTube视频的URL示例
    youtube_video = "https://www.bilibili.com/video/BV1Ez421U7gi/?spm_id_from=333.1007.tianma.1-2-2.click&vd_source=a270110c75c3c0d495aff16daf9b25cf"
    st.video(youtube_video)

if __name__ == "__main__":
    main()
