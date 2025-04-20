import yt_dlp
import sys
import os
from youtube_links_to_download import all_links


def list_formats(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        print(f"\nAvailable formats for: {info.get('title')}")
        for f in formats:
            print(f"{f['format_id']:>6} | {str(f.get('height') or 'N/A'):>5}p | {f.get('ext', ''):<4} | {f.get('format_note', '')}")
        print("\nYou can re-run the command with `--quality <format_id>` or `--quality 720p`\n")


def is_ffmpeg_installed():
    return os.system("ffmpeg -version >nul 2>&1") == 0


def download_video(url, quality=None, save_path='./YouTubeDownloads/'):
    format_str = "bestvideo+bestaudio/best"  # fallback

    if quality:
        print(f"[+] Using specified quality: {quality}")
        if quality.endswith("p") and quality[:-1].isdigit():
            height = quality.replace("p", "")
            format_str = f"bestvideo[height={height}]+bestaudio/best[height={height}]"
        else:
            # assume it's a format_id
            format_str = quality

    ydl_opts = {
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'format': format_str,
        'merge_output_format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        print("[!] Download failed. Listing available formats instead...\n")
        list_formats(url)


# ========= Main Logic =========

filename = "youtube-downloader"
quality = None

# Defaults
links = all_links

# CLI flags
if len(sys.argv) == 1:
    print("[+] Downloading all default links:")
    for link in all_links:
        download_video(link)
    exit()

if "--help" in sys.argv or "-h" in sys.argv:
    print("\nCommands\n==========")
    print("-h | --help\t=> show help info")
    print("-u | --url\t=> download a single YouTube URL")
    print("-q | --quality\t=> choose quality (360p / 720p / 1080p or format_id)")
    print("--list-formats\t=> list all available formats for a specific URL")
    print("\nExamples:")
    print(f"python {filename}.py --url <url>")
    print(f"python {filename}.py --url <url> --quality 720p")
    print(f"python {filename}.py --url <url> --list-formats\n")
    exit()

if "--url" in sys.argv or "-u" in sys.argv:
    try:
        u_index = sys.argv.index("--url") if "--url" in sys.argv else sys.argv.index("-u")
        url = sys.argv[u_index + 1]
        links = [url]

        # Just list formats
        if "--list-formats" in sys.argv:
            list_formats(url)
            exit()

    except IndexError:
        print("[!] URL missing after -u / --url")
        exit()

if "--quality" in sys.argv or "-q" in sys.argv:
    try:
        q_index = sys.argv.index("--quality") if "--quality" in sys.argv else sys.argv.index("-q")
        quality = sys.argv[q_index + 1]
    except IndexError:
        print("[!] You must specify a quality level (e.g., 360p, 720p, 1080p or format_id)")
        exit()

# Do downloads
for link in links:
    print(f"[+] Downloading: {link}")
    download_video(link, quality=quality)
