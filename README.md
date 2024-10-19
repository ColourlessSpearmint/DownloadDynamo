# DownloadDynamo

DownloadDynamo is a Python tool that downloads audio from YouTube, extracts metadata, and allows users to add or modify metadata, including album art, through a simple web-based interface built with Gradio.

## Features
- **YouTube Audio Download**: Download audio from YouTube as MP3 using `yt-dlp`.
- **Automatic Playlist Iteration** Download an entire playlist with one command.
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

Install the dependencies using pip:

```bash
pip install gradio yt-dlp mutagen Pillow requests
```

## How to Use

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/ColourlessSpearmint/DownloadDynamo.git
    cd DownloadDynamo
    ```

2. **Run the Script**:

    ```bash
    python app.py
    ```

3. **Access the Interface**:

   The script will launch a Gradio web interface in your browser where you can:

   - Paste a YouTube URL.
   - Click "Extract Audio and Metadata" to download the audio and automatically fill the metadata fields.
   - Optionally edit metadata fields.
   - Click "Add Metadata and Download" to finalize the MP3 with updated metadata and album art.

## Example Usage

1. Enter a YouTube URL (e.g., a music video link).
2. The tool downloads the audio and automatically extracts and fills in metadata such as the title and artist.
3. You can edit any metadata or preview the thumbnail.
4. After editing, download the MP3 file with updated metadata and album art.

## Customization

- **Metadata Fields**: Add or modify fields such as genre or album artist through the Gradio interface.

## Upcoming Features

- MP4 support
- Keyword Search

## License

DownloadDynamo is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).

## Author

Developed by **Ethan Marks** ([@ColourlessSpearmint](https://github.com/ColourlessSpearmint)).
