from pytube import YouTube
import re
import os
import subprocess


# e.g. parse_time("1:30") => 90
def parse_time(time_str):
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(time_str.split(':'))))


# returns list of tuple (start_time_sec, name)
def track_labels(video_url):
    description = YouTube(video_url).description
    matches = re.findall(r"\[*(\d+:\d+:?\d+)\]* (.*)", description)
    return list(map(lambda match: (parse_time(match[0]), match[1]), matches))


def download_audio(video_url, target_folder, filename):
    YouTube(video_url).streams\
        .filter(only_audio=True)\
        .filter(mime_type="audio/mp4")\
        .order_by('abr').desc().first()\
        .download(output_path=target_folder, filename=filename)


# splits file into tracks
def section_file(file, sections):
    workers = []
    for i in range(len(sections)):
        start_time, section_name = sections[i]
        output_name = os.path.join(os.path.dirname(file), section_name)
        args = ["ffmpeg", "-y", "-i", file, "-ss", str(start_time)]
        if i + 1 < len(sections):
            args = args + ["-t", str(sections[i + 1][0] - start_time)]
        args.append(f"{output_name}.mp4")
        workers.append(subprocess.Popen(args))
    for w in workers:
        w.wait()


video = 'https://www.youtube.com/watch?v=-FlxM_0S2lA'
path = os.path.join("../", "test")
print("track_labels: " + str(track_labels(video)))
download_audio(video, path, "test")
section_file(os.path.join(path, "test.mp4"), track_labels(video))


# TODO make this an extension / MR of pytube library?