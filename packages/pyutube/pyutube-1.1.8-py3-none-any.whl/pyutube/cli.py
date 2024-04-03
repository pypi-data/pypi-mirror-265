"""
Pyutube is a command-line interface, a versatile tool 
to download YouTube videos, shorts, and playlists.

This module provides a command-line interface (CLI), a powerful tool designed 
to simplify the process of downloading YouTube content directly from the terminal.
Pyutube supports downloading videos (as video or audio), shorts, and playlists, 
offering users flexibility and convenience in managing their media downloads.

Usage:
    $ pyutube download <URL> [options]

Options:
    -a, --audio          Download only audio.
    -f, --footage        Download only video (footage).
    -v, --version        Show the version number.

Example:
    $ pyutube <YouTube_URL> -a
        Download the audio of the specified YouTube video.

    $ pyutube <YouTube_URL> -f
        Download the video (footage) of the specified YouTube video.

    $ pyutube <YouTube_URL>
        Download the file of the specified YouTube video, 
        it will ask you about downloading it as video or audio.

    $ pyutube <YouTube_playlist_URL>
        Download all videos from the specified YouTube playlist.

    $ pyutube <YouTube_short_URL>
        Download the specified YouTube short video.

Made with ❤️ By Ebraheem. Find me on GitHub: @Hetari. The project lives on @Hetari/pyutube.

Thank you for using Pyutube! Your support is greatly appreciated. ⭐️
"""

import os
import sys

import typer

from .utils import (
    __version__,
    clear,
    error_console,
    console,
    check_internet_connection,
    is_youtube_video_id,
    validate_link,
    handle_video_link,
)
from .downloader import download


# Create CLI app
app = typer.Typer(
    name="pyutube",
    add_completion=False,
    help="Awesome CLI to download YouTube videos \
    (as video or audio)/shorts/playlists from the terminal",
    rich_markup_mode="rich",
)


# Define the variables for the arguments and options
url_arg = typer.Argument(
    None,
    help="YouTube URL [red]required[/red]",
    show_default=False
)
path_arg = typer.Argument(
    os.getcwd(),
    help="Path to save video [cyan]default: <current directory>[/cyan]",
    show_default=False
)
audio_option = typer.Option(
    False, "-a", "--audio", help="Download only audio"
)
video_option = typer.Option(
    False, "-f", "--footage", help="Download only video"
)
version_option = typer.Option(
    False, "-v", "--version", help="Show the version number"
)


@app.command(
    name="download",
    help="""
Download a [red]YouTube[/red] [green]videos[/green] [blue](as 
video or audio)[/blue], [green]shorts[/green], and [green]playlists[/green].
    """,
    epilog="""
Made with ❤️  By Ebraheem. Find me on GitHub: [link=https://github.com/Hetari]@Hetari[/link].

The project lives on [link=https://github.com/Hetari/pyutube]@Hetari/pyutube[/link].\n\nThank you for using Pyutube! and your support :star:
    """,
)
def pyutube(
    url: str = url_arg,
    path: str = path_arg,
    audio: bool = audio_option,
    video: bool = video_option,
    version: bool = version_option
) -> None:
    """
    Downloads a YouTube video.

    Args:
        url (str): The URL of the YouTube video.
        path (str): The path to save the video. Defaults to the current working directory.

    """
    if version:
        console.print(f"Pyutube {__version__}")
        sys.exit()

    if url is None:
        error_console.print("❗ Missing argument 'URL'.")
        sys.exit()

    clear()

    if not check_internet_connection():
        sys.exit()

    if is_youtube_video_id(url):
        url = f"https://www.youtube.com/watch?v={url}"

    is_valid_link, link_type = validate_link(url)

    if not is_valid_link:
        sys.exit()

    if audio:
        download(url, path, is_audio=True)

    elif video or link_type == "short":
        download(url, path, is_audio=False)

    elif link_type == "video":
        handle_video(url, path)

    elif link_type == "playlist":
        handle_playlist(url, path)

    else:
        error_console.print("❗ Unsupported link type.")
        sys.exit()

    sys.exit()


def handle_video(url, path):
    """
    Downloads a video from the given URL and saves it to the specified path.

    Args:
        url (str): The URL of the video.
        path (str): The path to save the video.

    Returns:
        None
    """
    # ask if the user wants to download audio, or video?
    try:
        is_audio = handle_video_link()
    except TypeError:
        return
    download(url, path, is_audio)


def handle_playlist(url: str, path: str):
    """
    Downloads a playlist of videos from the given URL and saves them to the specified path.

    Args:
        url (str): The URL of the playlist.
        path (str): The path to save the downloaded videos.

    Returns:
        None
    """
    try:
        is_audio = handle_video_link()
    except TypeError:
        return
    playlist = download(url, path, is_audio, is_playlist=True)
    links = playlist.video_urls
    title = playlist.title

    if not links:
        error_console.print("❗ There are no videos in the playlist.")
        return

    console.print(f"\nPlaylist title: {title}", style="info")
    console.print(f"Total videos: {len(links)}\n", style="info")
    console.print("")

    for index, link in enumerate(links):
        if index == 0:
            quality = download(links[0], path, is_audio)
        download(link, path, is_audio, quality_choice=quality)
        clear()
