import gradio as gr
from downloader import download_audio_and_metadata, add_metadata, process_playlist
from search import search_videos  # Import the search function

# Gradio interface
with gr.Blocks() as interface:
    # Create a tabbed interface
    with gr.Tabs():
        # First Tab: Download Single
        with gr.Tab("Download Single"):
            youtube_url = gr.Textbox(label="YouTube URL", placeholder="Enter YouTube link here")
            extract_btn = gr.Button("Extract Audio and Metadata")
            
            # Audio output with playback and download
            audio_output = gr.Audio(type="filepath", show_download_button=True)
            
            # Thumbnail preview
            thumbnail_output = gr.Image(label="Thumbnail Preview", type="filepath")  # Use 'filepath' for local file reference
            
            # Metadata input fields, pre-filled from yt-dlp
            with gr.Row():
                title = gr.Textbox(label="Title", placeholder="Enter title")
                artist = gr.Textbox(label="Artist", placeholder="Enter artist name")
                album = gr.Textbox(label="Album", placeholder="Enter album name")
                album_artist = gr.Textbox(label="Album Artist", placeholder="Enter album artist name")
                release_year = gr.Textbox(label="Release Year", placeholder="Enter release year")
                genre = gr.Textbox(label="Genre", placeholder="Enter genre (optional)")
                
            add_metadata_btn = gr.Button("Add Metadata and Download")
            
            # Audio extraction functionality with metadata pre-filling
            extract_btn.click(download_audio_and_metadata, 
                              inputs=youtube_url, 
                              outputs=[audio_output, thumbnail_output, title, artist, album, album_artist, release_year, genre])

            # Metadata functionality
            add_metadata_btn.click(add_metadata, 
                                   inputs=[audio_output, title, artist, album, album_artist, release_year, genre, thumbnail_output], 
                                   outputs=audio_output)

        # Second Tab: Download Playlist
        with gr.Tab("Download Playlist"):
            youtube_url = gr.Textbox(label="YouTube URL", placeholder="Enter YouTube link here")
            playlist_btn = gr.Button("Download Playlist")
            zip_output = gr.File(label="Playlist", type="filepath")

            playlist_btn.click(process_playlist, inputs=youtube_url, outputs=zip_output)

        # Third Tab: Search by Keyword
        with gr.Tab("Search Videos"):
            search_keyword = gr.Textbox(label="Search Keyword", placeholder="Enter keyword to search")
            search_btn = gr.Button("Search Videos")
            
            # Display outputs for the top 5 videos
            with gr.Row():
                titles_output = gr.Label(label="Titles")
                artists_output = gr.Label(label="Artists")
                release_years_output = gr.Label(label="Release Years")

            # Audio and thumbnails for each video
            with gr.Row():
                audio_output_search = gr.Audio(label="Audio Outputs", type="filepath", show_download_button=True)
                thumbnails_output = gr.Image(label="Thumbnails", type="filepath")

            # Search functionality
            search_btn.click(
                search_videos, 
                inputs=search_keyword, 
                outputs=[titles_output, artists_output, release_years_output, audio_output_search, thumbnails_output]
            )

# Launch the interface
interface.launch(inbrowser=True)
