import yt_dlp
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import requests
from PIL import Image
from io import BytesIO
import os
import zipfile

# Define the downloads directory
DOWNLOADS_DIR = "downloads"

def ensure_downloads_directory():
    """Ensure the downloads directory exists."""
    if not os.path.exists(DOWNLOADS_DIR):
        os.makedirs(DOWNLOADS_DIR)

def download_audio_and_metadata(youtube_url, track_number=None):
    """
    Downloads audio from a YouTube video and applies metadata including title, artist,
    album, and thumbnail as album art.

    Args:
        youtube_url (str): The URL of the YouTube video to download audio from.
        track_number (int, optional): The track number for playlist downloads. Defaults to None.

    Returns:
        tuple: Contains the path to the downloaded audio file, thumbnail image (if available),
        the title, artist, album, album artist, release year, and genre (empty string by default).
    """
    # Ensure downloads directory exists
    ensure_downloads_directory()

    # Set options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOADS_DIR, 'audio.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        audio_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')
        
        # Extract metadata from YouTube video
        title = info_dict.get('title', 'Unknown Title')
        artist = info_dict.get('uploader', 'Unknown Artist')
        if "music.youtube.com" in youtube_url:
            artist = artist.replace(' - Topic', '')  # Remove ' - Topic' from artist

        album = title  # Set album to the title of the song by default
        album_artist = artist  # Default album artist to the uploader/artist
        
        # Rename the audio file to the title of the song
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", ".", "_")).rstrip()  # Sanitize title
        new_audio_title = os.path.join(DOWNLOADS_DIR, f"{safe_title}.mp3")
        if os.path.exists(new_audio_title):  # Overwrite if file exists
            os.remove(new_audio_title)
        os.rename(audio_file, new_audio_title)  # Rename the file
        audio_file = new_audio_title

        # Extract release year from 'upload_date' if available (format is YYYYMMDD)
        upload_date = info_dict.get('upload_date', None)
        release_year = upload_date[:4] if upload_date else 'Unknown Year'
        
        # Extract thumbnail URL
        thumbnail_url = info_dict.get('thumbnail', None)
        
        # Save thumbnail to thumbnail.jpg
        thumbnail_file = os.path.join(DOWNLOADS_DIR, 'thumbnail.jpg')  # Always use this filename
        
        if thumbnail_url:
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                if "music.youtube.com" in youtube_url:
                    img = crop_image_to_square(img)  # Crop to square
                img.save(thumbnail_file)  # Save the image
            else:
                thumbnail_file = None  # In case of an unsuccessful response
        else:
            thumbnail_file = None  # No thumbnail URL available
        
        # Automatically add metadata
        add_metadata(audio_file, title, artist, album, album_artist, release_year, "", thumbnail_file, track_number)

        # Return audio file path, thumbnail file path, and extracted metadata
        return audio_file, thumbnail_file, title, artist, album, album_artist, release_year, ""

def crop_image_to_square(image):
    """
    Crops the given image to a square, based on the smaller of the width or height.

    Args:
        image (PIL.Image.Image): The image to be cropped.

    Returns:
        PIL.Image.Image: The cropped square image.
    """
    width, height = image.size
    min_side = min(width, height)
    
    left = (width - min_side) / 2
    top = (height - min_side) / 2
    right = (width + min_side) / 2
    bottom = (height + min_side) / 2
    
    # Crop the image to a square
    return image.crop((left, top, right, bottom))

def add_metadata(audio_file, title, artist, album, album_artist, release_year, genre, thumbnail_file, track_number):
    """
    Adds metadata to an audio file, such as title, artist, album, and optionally attaches a thumbnail as album art.

    Args:
        audio_file (str): The path to the audio file to which metadata will be added.
        title (str): The title of the audio track.
        artist (str): The artist of the audio track.
        album (str): The album name for the audio track.
        album_artist (str): The album artist name.
        release_year (str): The year of release.
        genre (str): The genre of the audio track (optional).
        thumbnail_file (str): The path to the thumbnail image (if available).
        track_number (int, optional): The track number for playlist downloads. Defaults to None.

    Returns:
        str: The path to the audio file with metadata added.
    """
    # Add metadata using mutagen
    audio = EasyID3(audio_file)
    audio['title'] = title
    audio['artist'] = artist
    audio['album'] = album
    audio['albumartist'] = album_artist
    audio['date'] = release_year
    if genre:
        audio['genre'] = genre
    
    # Add track number if provided
    if track_number is not None:
        audio['tracknumber'] = str(track_number)
    
    audio.save()

    # Attach thumbnail as album art using ID3
    if thumbnail_file and os.path.exists(thumbnail_file):
        with open(thumbnail_file, 'rb') as img_file:
            audio_tags = ID3(audio_file)
            audio_tags['APIC'] = APIC(
                encoding=3,  # UTF-8
                mime='image/jpeg',  # Image MIME type
                type=3,  # Front cover
                desc='Cover',
                data=img_file.read()
            )
            audio_tags.save()

    return audio_file  # Return the updated file with metadata and thumbnail

def process_playlist(playlist_url):
    """
    Processes a YouTube playlist by downloading the audio for each video, applying metadata,
    and zipping all the audio files.

    Args:
        playlist_url (str): The URL of the YouTube playlist to process.

    Returns:
        str: The path to the zip file containing the downloaded audio files.
    """
    # Extract video URLs from the playlist
    ydl_opts = {'extract_flat': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        video_urls = [entry['url'] for entry in playlist_info['entries']]
    
    # Store audio files for zipping
    audio_files = []
    
    # Download each video and modify metadata
    for track_number, video_url in enumerate(video_urls, start=1):
        audio_file, thumbnail_file, _, _, _, _, _, _ = download_audio_and_metadata(video_url, track_number)
        audio_files.append(audio_file)
        if thumbnail_file and os.path.exists(thumbnail_file):
            os.remove(thumbnail_file)  # Remove thumbnail after processing to clean up

    # Zip the audio files
    zip_filename = os.path.join(DOWNLOADS_DIR, "playlist.zip")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for audio_file in audio_files:
            zipf.write(audio_file, os.path.basename(audio_file))  # Add the file to the zip

    print(f"Zipped {len(audio_files)} audio files into {zip_filename}")

    return zip_filename

def download_video(youtube_url):
    """
    Downloads a video from YouTube in mp4 format.

    Args:
        youtube_url (str): The URL of the YouTube video to download.

    Returns:
        str: The path to the downloaded mp4 video file.
    """
    # Ensure downloads directory exists
    ensure_downloads_directory()

    # Set options for yt-dlp to download video in mp4 format
    ydl_opts = {
        'format': 'bestvideo+bestaudio',
        'outtmpl': os.path.join(DOWNLOADS_DIR, 'video.%(ext)s'),
        'merge_output_format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        video_file = ydl.prepare_filename(info_dict).replace('.mkv', '.mp4').replace('.webm', '.mp4')
        
        # Rename the video file to the title of the video
        title = info_dict.get('title', 'Unknown Title')
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", ".", "_")).rstrip()  # Sanitize title
        new_video_title = os.path.join(DOWNLOADS_DIR, f"{safe_title}.mp4")
        if os.path.exists(new_video_title):  # Overwrite if file exists
            os.remove(new_video_title)
        os.rename(video_file, new_video_title)  # Rename the file
        video_file = new_video_title

        # Return the video file path
        return video_file

def process_video_playlist(playlist_url):
    """
    Processes a YouTube playlist by downloading the videos and zipping them into a single file.

    Args:
        playlist_url (str): The URL of the YouTube playlist to process.

    Returns:
        str: The path to the zip file containing the downloaded video files.
    """
    # Extract video URLs from the playlist
    ydl_opts = {'extract_flat': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        video_urls = [entry['url'] for entry in playlist_info['entries']]
    
    # Store video files for zipping
    video_files = []
    
    # Download each video
    for i, video_url in enumerate(video_urls, start=1):
        video_file = download_video(video_url)
        video_files.append(video_file)

    # Zip the video files
    zip_filename = os.path.join(DOWNLOADS_DIR, "videos_playlist.zip")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for video_file in video_files:
            zipf.write(video_file, os.path.basename(video_file))  # Add the file to the zip

    print(f"Zipped {len(video_files)} videos into {zip_filename}")

    return zip_filename

def video_pipeline(url):
    """
    Determines if the provided URL is a video or a playlist and processes it accordingly.

    Args:
        url (str): The URL of the YouTube video or playlist to process.

    Returns:
        str: The path to the zip file containing the downloaded files.
    """
    # Set options for yt-dlp to check if the URL is a playlist or video
    ydl_opts = {'extract_flat': True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

    # Check if the URL is a playlist
    if 'entries' in info_dict:  # It's a playlist
        print(f"Processing playlist: {info_dict.get('title')}")
        return process_video_playlist(url)  # Process the playlist
    else:  # It's a single video
        print(f"Downloading video: {info_dict.get('title')}")
        return download_video(url)  # Download the single video