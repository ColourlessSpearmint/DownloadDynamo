import gradio as gr
from downloader import download_audio_and_metadata, add_metadata

# Gradio interface
with gr.Blocks() as interface:
    # Create a tabbed interface
    with gr.Tabs():
        # First Tab: Current interface
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

        # Second Tab: Input text and output zip file
        with gr.Tab("Download Playlist"):
            youtube_url = gr.Textbox(label="YouTube URL", placeholder="Enter YouTube link here")
            process_btn = gr.Button("Download Playlist")
            zip_output = gr.File(label="Playlist", type="filepath")

            process_btn.click(lambda x: "playlist.zip", inputs=youtube_url, outputs=zip_output)

# Launch the interface
interface.launch(inbrowser=True)
