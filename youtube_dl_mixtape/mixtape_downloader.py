from pytube import YouTube
import re
import os
import subprocess


# e.g. parse_time("1:30") => 90
def parse_time(time_str):
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(time_str.split(':'))))


# returns a list of dictionary, each containing:
# "startTimeSec" => int
# "endTimeSec" => int
# "name" => string
def track_labels(video_url):
    video = YouTube(video_url)
    description = video.description
    section_strs = re.findall(r"\[*(\d+:\d+:?\d+)\]* (.*)", description)
    sections = list(map(lambda s: {"startTimeSec": parse_time(s[0]), "name": s[1]}, section_strs))
    sections = sorted(sections, key=lambda s: s["startTimeSec"])
    for i in range(len(sections)):
        sections[i]["endTimeSec"] = sections[i + 1]["startTimeSec"] if i + 1 < len(sections) else video.length
    return sections


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
        section = sections[i]
        start_time = section["startTimeSec"]
        section_name = section["name"]
        output_name = os.path.join(os.path.dirname(file), section_name)
        args = ["ffmpeg", "-y", "-i", file, "-ss", str(start_time)]
        if i + 1 < len(sections):  # if next section, add end time argument
            next_start_time = sections[i + 1]["startTimeSec"]
            args = args + ["-t", str(next_start_time - start_time)]
        args.append(f"{output_name}.mp4")
        workers.append(subprocess.Popen(args))
    for w in workers:
        w.wait()


'''
video = 'https://www.youtube.com/watch?v=-FlxM_0S2lA'
path = os.path.join("../", "test")
labels = track_labels(video)
print("labels: " + str(labels))
download_audio(video, path, "test")
section_file(os.path.join(path, "test.mp4"), labels)
'''