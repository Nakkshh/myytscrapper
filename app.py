import streamlit as st
import time
from downloader import fetch_video_details, get_file_size, download_stream

# Set Streamlit page configuration
st.set_page_config(page_title="MyYTScrapper", page_icon="🎬", layout="centered")

st.title("🎬 YouTube Video & Audio Downloader")
st.write("Paste a YouTube link below to fetch details and download the video or audio.")

# Input field for YouTube URL
url = st.text_input("🔗 Enter YouTube URL")

if url:
    yt, details = fetch_video_details(url)
    if yt:
        with st.spinner("Fetching video details..."):
            time.sleep(1.5)

        # Display video details
        st.subheader("📌 Video Details")
        st.image(details['thumbnail_url'], use_container_width=True)
        st.write(f"**🎥 Title:** {details['title']}")
        st.write(f"**👁️ Views:** {details['views']}")
        st.write(f"**⏳ Duration:** {details['duration']} seconds")
        st.write(f"**⭐ Rating:** {details['rating']}")
        st.write(f"**📝 Description:** {details['description'][:300]}...")

        # Download options
        download_type = st.radio("🎵 Select Download Type", ("Video", "Audio"))

        # Select available streams
        stream_dict = {}
        if download_type == "Video":
            for stream in details["video_streams"]:
                label = f"{stream.resolution} - {get_file_size(stream)} MB"
                stream_dict[label] = stream
            selected_label = st.selectbox("🎞️ Select Video Quality", list(stream_dict.keys()))
        else:
            for stream in details["audio_streams"]:
                label = f"{stream.abr} - {get_file_size(stream)} MB"
                stream_dict[label] = stream
            selected_label = st.selectbox("🎧 Select Audio Quality", list(stream_dict.keys()))

        selected_stream = stream_dict[selected_label]

        if st.button("📥 Click to Start Download"):
            with st.spinner("Please wait..."):
                file_bytes, file_name, mime_type = download_stream(selected_stream, download_type)

            if file_bytes:
                st.success("✅ File is ready for download.\nClick on the download button below.")

                st.download_button(
                    label="📥Download",
                    data=file_bytes,
                    file_name=file_name,
                    mime=mime_type
                )
            else:
                st.error("❌ Failed to process the file.")
    else:
        st.error(f"❌ Error fetching video details: {details}")
