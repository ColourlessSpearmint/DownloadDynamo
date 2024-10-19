# DownloadDynamo

DownloadDynamo is a Python tool that downloads audio from YouTube, extracts metadata, and allows users to add or modify metadata, including album art, through a simple web-based interface built with Gradio.

## Author

Developed by **Ethan Marks** ([@ColourlessSpearmint](https://github.com/ColourlessSpearmint)).

## Features
- **YouTube Audio Download**: Download audio from YouTube as MP3 using `yt-dlp`.
- **Automatic Playlist Iteration**: Download an entire playlist with one command.
- **Keyword Search**: Search YouTube's database without leaving the interface. 
- **Automatic Metadata Extraction**: Extract metadata like title, artist, and release year from YouTube videos.
- **Thumbnail Download**: Download the video thumbnail and use it as album art.
- **Editable Metadata**: Manually adjust metadata fields such as title, album, artist, and genre.
- **Web-Based Interface**: Interact with the tool through an easy-to-use Gradio interface.

## Requirements

To use DownloadDynamo, ensure the following dependencies are installed:

- Python 3.6+
- `gradio` for the user interface
- `yt-dlp` for downloading audio
- `mutagen` for MP3 metadata handling
- `Pillow` for image processing
- `requests` for downloading thumbnails

## Quickstart

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/ColourlessSpearmint/DownloadDynamo.git
    cd DownloadDynamo
    ```

1. **Install Packages**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Script**:

    ```bash
    python app.py
    ```

4. **Access the Interface**:

   The script will launch a Gradio web interface in your browser where you can:

   - Paste a YouTube URL.
   - Click "Extract Audio and Metadata" to download the audio and automatically fill the metadata fields.
   - Optionally edit metadata fields.
   - Click "Add Metadata and Download" to finalize the MP3 with updated metadata and album art.

## Upcoming Features

- MP4 support

## License

DownloadDynamo is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).