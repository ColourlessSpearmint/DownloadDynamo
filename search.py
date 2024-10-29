import yt_dlp
import os
import requests
from PIL import Image
from io import BytesIO
import re


def sanitize_title(title):
    # Remove punctuation, emojis, and similar characters
    sanitized = re.sub(
        r"[^\w\s]", "", title
    )  # Keep only alphanumeric characters and spaces
    sanitized = sanitized.strip()  # Remove leading/trailing spaces
    return sanitized


def get_video_info(search_query, num_results=5, output_folder="downloads"):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        "quiet": True,  # Suppresses all yt-dlp output
        "format": "bestaudio/best",  # Best quality audio format
        "noplaylist": True,  # Only download single video
        "skip_download": True,  # Do not download anything
    }

    # Use yt-dlp to search for the query
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(
            f"ytsearch{num_results}:{search_query}", download=False
        )["entries"]

    video_data = []

    for result in search_results[:num_results]:
        video_info = {
            "title": result.get("title", "N/A"),
            "artist": result.get("uploader", "N/A"),
            "release_year": (
                result.get("release_date", "N/A")[:4]
                if result.get("release_date")
                else "N/A"
            ),
            "thumbnail_output": result.get("thumbnail", "N/A"),
            "url": result.get("webpage_url", "N/A"),
        }

        # Sanitize the title for safe file naming
        sanitized_title = sanitize_title(video_info["title"])

        # Define the output paths for audio and thumbnail files
        audio_output = os.path.join(output_folder, f"{sanitized_title}.mp3")
        thumbnail_output = os.path.join(
            output_folder, f"{sanitized_title}.jpg"
        )  # Path for thumbnail

        # Download audio
        audio_opts = {
            "format": "bestaudio/best",
            "outtmpl": audio_output,  # Set the output template for audio
        }

        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            ydl.download([result["webpage_url"]])  # Download the audio file

        video_info["audio_output"] = (
            audio_output  # Store the path of the downloaded audio
        )

        # Download the thumbnail image
        response = requests.get(video_info["thumbnail_output"])  # Get the thumbnail
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.save(thumbnail_output)  # Save the image in the downloads directory
        else:
            thumbnail_output = None  # In case of an unsuccessful response

        video_info["thumbnail_output"] = (
            thumbnail_output  # Store the path of the thumbnail
        )

        video_data.append(video_info)  # Append the video info to the list

    return video_data


def search_videos(keyword):
    # Get the top 3 video information
    video_info = get_video_info(keyword, num_results=3)

    # Prepare data for Gradio output
    titles, artists, release_years, audio_paths, thumbnails, urls = (
        [],
        [],
        [],
        [],
        [],
        [],
    )
    for video in video_info:
        titles.append(video["title"])
        artists.append(video["artist"])
        release_years.append(video["release_year"])
        audio_paths.append(video["audio_output"])  # Path to the downloaded audio
        urls.append(video["url"])
        thumbnails.append(video["thumbnail_output"])  # Path to the thumbnail

    return titles, artists, release_years, audio_paths, thumbnails, urls
