from flask import Blueprint, Response

from app.renderVideo import video_capture_local

router = Blueprint("apiRoutes",__name__)


@router.route('/video_stream_local')
def video_stream_local():
    return Response(video_capture_local(), mimetype='multipart/x-mixed-replace; boundary=frame')