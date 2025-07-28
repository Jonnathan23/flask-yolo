from flask import Blueprint, Response, request, abort

from app.renderVideo import video_capture_local, video_capture_mobile
import app.data.db as db

router = Blueprint("apiRoutes",__name__)

#* Streming video
@router.route('/video_stream_local')
def video_stream_local():
    return Response(video_capture_local(), mimetype='multipart/x-mixed-replace; boundary=frame')


@router.route('/video_stream_mobile')
def video_stream_mobile():
    return Response(video_capture_mobile(), mimetype='multipart/x-mixed-replace; boundary=frame')


@router.route('/set_operation', methods=['POST'])
def setOperation():
    data = request.get_json()     
    print(data)
    setOperation = data.get('operation')
    if not setOperation:
        abort(400, "No operation provided")
    
    db.operation = setOperation
    print(f"Operation set to: {db.operation}")
    return "Operation set successfully", 200