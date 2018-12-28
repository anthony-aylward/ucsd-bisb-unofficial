#===============================================================================
# uploads.py
#===============================================================================

from flask_uploads import UploadSet, IMAGES
documents = UploadSet('documents', ('pdf',))
images = UploadSet('images', IMAGES)
