import streamlit as st

def main():
    st.title("在线视频播放示例")
    # 这是YouTube视频的URL示例
    youtube_video = "https://player.bilibili.com/player.html?aid=413672301&bvid=BV1MV41167e9&cid=208508865&page=1&t=60&autoplay=true"
    st.video(youtube_video)

if __name__ == "__main__":
    main()
