import os.path
from urllib.parse import quote_plus
from io import BytesIO

from anzo_api.rest_adapter import RestAdapter


class MigrationPackageApi(object):
    """A class for interacting with an Anzo Server.

    This wraps the Anzo API endpoints to simplify building Anzo workflows that require interactions among many
    system assets.

    The general patterns in this class are:
    - AnzoRestApiException is raised if any errors are returned from the API endpoint
    - A TimeoutError is raised if the operation times out
    - API responses are returned as an object representing the Anzo asset (i.e. Graphmart, Layer, Model, etc.)
    """
    def __init__(self,
                 hostname,
                 port,
                 path="",
                 username="",
                 password="",
                 auth_token="",
                 ssl_verify=False):
        self._rest_adapter = RestAdapter(hostname, port, username, password, auth_token, ssl_verify)

    def import_migration_package(self, migration_package, new_version_label=None, new_version_comment=None,
                                 current_state_version_label=None, current_state_version_comment=None,
                                 apply_import=False, force=False) -> bool:
        with open(migration_package, 'rb') as f:
            multipart_files = {
                "migrationPackage": (os.path.basename(migration_package), f),
                "newVersionLabel": (None, new_version_label),
                "newVersionComment": (None, new_version_comment),
                "currentStateVersionLabel": (None, current_state_version_label),
                "currentStateVersionComment": (None, current_state_version_comment),
                "applyImport": (None, apply_import)
            }
            params = {"force": force}
            self._rest_adapter.post(endpoint=f"migration/import", ep_params=params, files=multipart_files)
        return True

    def export_migration_package(self, migration_package_uri) -> BytesIO:
        """

        Args:
            migration_package_uri: URI of the migration package

        Returns:
            Native Python ZipFile object (zipfile.ZipFile)
        """
        uri = quote_plus(migration_package_uri)
        result = self._rest_adapter.post(endpoint=f"migration/{uri}/export")
        result_in_bytes = BytesIO(result.content)
        return result_in_bytes
