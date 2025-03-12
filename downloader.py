from pytubefix import YouTube
from io import BytesIO

# Function to fetch video details
def fetch_video_details(url):
    try:
        yt = YouTube(url)
        details = {
            "title": yt.title,
            "views": yt.views,
            "duration": yt.length,
            "description": yt.description,
            "rating": yt.rating,
            "thumbnail_url": yt.thumbnail_url,
            "video_streams": yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc(),
            "audio_streams": yt.streams.filter(only_audio=True).order_by('abr').desc()
        }
        return yt, details
    except Exception as e:
        return None, str(e)

# Function to get file size
def get_file_size(stream):
    try:
        return round(stream.filesize_approx / (1024 * 1024), 2)  # Approximate file size in MB
    except Exception as e:
        print(f"Error fetching file size: {e}")
        return 0

# Function to download a stream into memory (BytesIO) instead of saving locally
def download_stream(stream, download_type):
    try:
        buffer = BytesIO()
        stream.stream_to_buffer(buffer)  # Download content into the buffer
        buffer.seek(0)  # Reset buffer position

        file_name = f"downloaded.{ 'mp3' if download_type == 'Audio' else 'mp4' }"
        mime_type = "audio/mp3" if download_type == "Audio" else "video/mp4"

        return buffer, file_name, mime_type
    except Exception as e:
        return None, None, str(e)
