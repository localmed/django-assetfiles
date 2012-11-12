from django.contrib.staticfiles.handlers import StaticFilesHandler
from assetfiles.views import serve

class AssetFilesHandler(StaticFilesHandler):
    def serve(self, request):
        """
        Actually serves the request path.
        """
        return serve(request, self.file_path(request.path), insecure=True)
