from flask import Blueprint, Response, request, abort

from app.renderVideo import video_capture_local
import app.data.db as db

router = Blueprint("apiRoutes",__name__)

#* Streming video
@router.route('/video_stream_local')
def video_stream_local():
    return Response(video_capture_local(), mimetype='multipart/x-mixed-replace; boundary=frame')



@router.route('/set_operation', methods=['POST'])
def nameRouter():
    data = request.get_json() 
    print(data)
    setOperation = data.get('operation')
    if not setOperation:
        abort(400, "No operation provided")
    
    db.operation = setOperation
    return "Operation set successfully", 200