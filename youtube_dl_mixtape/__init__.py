from flask import Flask, request, Response
from youtube_dl_mixtape.mixtape_downloader import video_sections
import json

'''
Env vars:
- FLASK_APP=youtube-dl-mixtape
- FLASK_ENV=development
'''


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/sections')
    def get_sections():
        video_id = request.args.get('v')
        if video_id is None:
            return Response("Missing required 'v' parameter (Youtube video id)", status=400)
        sections = video_sections(f"https://youtube.com/watch?v={video_id}")
        response = Response(json.dumps(sections), mimetype="application/json")
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    # takes video_id and sections, returns zip (?) of mp4 files
    def download():
        pass

    return app
