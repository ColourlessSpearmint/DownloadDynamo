import gradio as gr
from downloader import download_audio_and_metadata, add_metadata, process_playlist, video_pipeline
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
            
            # Display outputs for the top 3 videos, each in its own row
            def create_video_row(index):
                with gr.Row():
                    # Create a row for each video
                    title_output = gr.Textbox(label=f"Title {index + 1}")
                    artist_output = gr.Textbox(label=f"Artist {index + 1}")
                    release_year_output = gr.Textbox(label=f"Release Year {index + 1}")
                    audio_output = gr.Audio(label=f"Audio {index + 1}", type="filepath", show_download_button=True)
                    thumbnail_output = gr.Image(label=f"Thumbnail {index + 1}", type="filepath")
                    url_output = gr.Textbox(label=f"URL {index + 1}", interactive=False)  # URL output, non-interactive
                    
                    return title_output, artist_output, release_year_output, audio_output, thumbnail_output, url_output

            # Create placeholders for video outputs
            video_outputs = [create_video_row(i) for i in range(3)]
            titles_output = [output[0] for output in video_outputs]
            artists_output = [output[1] for output in video_outputs]
            release_years_output = [output[2] for output in video_outputs]
            audio_output_search = [output[3] for output in video_outputs]
            thumbnails_output = [output[4] for output in video_outputs]
            urls_output = [output[5] for output in video_outputs]  # URL outputs

            # Search functionality
            def update_outputs(keyword):
                titles, artists, release_years, audio_paths, thumbnails, urls = search_videos(keyword)
                return (*titles, *artists, *release_years, *audio_paths, *thumbnails, *urls)  # Return URLs as well

            search_btn.click(
                update_outputs, 
                inputs=search_keyword, 
                outputs=[*titles_output, *artists_output, *release_years_output, *audio_output_search, *thumbnails_output, *urls_output]
            )

        # Fourth Tab: Video
        with gr.Tab("Download Video"):
            youtube_url_pipeline = gr.Textbox(label="YouTube URL", placeholder="Enter YouTube video or playlist link here")
            pipeline_btn = gr.Button("Process Video/Playlist")
            
            # Outputs for video or playlist zip
            video_output = gr.File(label="Downloaded Video/Playlist", type="filepath")
            
            # Functionality for processing video or playlist
            pipeline_btn.click(video_pipeline, inputs=youtube_url_pipeline, outputs=video_output)


# Launch the interface
interface.launch(inbrowser=True)