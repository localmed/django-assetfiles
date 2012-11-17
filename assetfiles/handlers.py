from django.contrib.staticfiles.handlers import StaticFilesHandler

from assetfiles.views import serve


class AssetFilesHandler(StaticFilesHandler):
    """
    Overrides StaticFilesHandler to use Assetfiles' view for serving files.
    """

    def serve(self, request):
        return serve(request, self.file_path(request.path), insecure=True)
