#===============================================================================
# uploads.py
#===============================================================================

from flask import Blueprint, abort, current_app, send_from_directory
from flask_uploads import UploadSet, IMAGES

documents = UploadSet('documents', ('pdf',))
images = UploadSet('images', IMAGES)

uploads_mod = Blueprint('_uploads', __name__, url_prefix='/_uploads')

@uploads_mod.route('/<setname>/<path:filename>')
def uploaded_file(setname: UploadSet, filename: str) -> Any:
    config = current_app.upload_set_config.get(setname)  # type: ignore
    if config is None:
        abort(404)
    return send_from_directory(config.destination, filename)
