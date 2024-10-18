import yt_dlp
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import requests
from PIL import Image
from io import BytesIO
import os

def download_audio_and_metadata(youtube_url):
    # Set options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
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
        album = title  # Set album to the title of the song by default
        album_artist = artist  # Default album artist to the uploader/artist
        
        # Rename the audio file to the title of the song
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", ".", "_")).rstrip()  # Sanitize title
        new_audio_title = f"{safe_title}.mp3"
        os.rename(audio_file, new_audio_title)  # Rename the file
        audio_file = new_audio_title

        # Extract release year from 'upload_date' if available (format is YYYYMMDD)
        upload_date = info_dict.get('upload_date', None)
        release_year = upload_date[:4] if upload_date else 'Unknown Year'
        
        # Extract thumbnail URL
        thumbnail_url = info_dict.get('thumbnail', None)
        
        # Save thumbnail to thumbnail.jpg
        thumbnail_file = 'thumbnail.jpg'  # Always use this filename
        
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
        add_metadata(audio_file, title, artist, album, album_artist, release_year, "", thumbnail_file)

        # Return audio file path, thumbnail file path, and extracted metadata
        return audio_file, thumbnail_file, title, artist, album, album_artist, release_year, ""

def crop_image_to_square(image):
    width, height = image.size
    min_side = min(width, height)
    
    left = (width - min_side) / 2
    top = (height - min_side) / 2
    right = (width + min_side) / 2
    bottom = (height + min_side) / 2
    
    # Crop the image to a square
    return image.crop((left, top, right, bottom))

def add_metadata(audio_file, title, artist, album, album_artist, release_year, genre, thumbnail_file):
    print(thumbnail_file)
    # Add metadata using mutagen
    audio = EasyID3(audio_file)
    audio['title'] = title
    audio['artist'] = artist
    audio['album'] = album
    audio['albumartist'] = album_artist
    audio['date'] = release_year
    if genre:
        audio['genre'] = genre
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
