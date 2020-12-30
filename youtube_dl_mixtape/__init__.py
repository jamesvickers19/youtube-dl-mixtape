from flask import Flask, request, Response
from youtube_dl_mixtape.mixtape_downloader import track_labels

'''
Env vars:
- FLASK_APP=youtube-dl-mixtape
- FLASK_ENV=development
'''


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/tracks')
    def tracks():
        video_id = request.args.get('v')
        if video_id is None:
            return Response("Missing required 'v' parameter (Youtube video id)", status=400)
        # TODO return as json array of tuples
        return str(track_labels(f"https://youtube.com/watch?v={video_id}"))

    # takes video_id and sections, returns zip (?) of mp4 files
    def download():
        pass

    return app
