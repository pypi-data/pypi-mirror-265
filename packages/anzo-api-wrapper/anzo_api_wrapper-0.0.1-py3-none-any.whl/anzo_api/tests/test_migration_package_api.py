from unittest import TestCase
from typing import List
from anzo_api.migration_package_api import MigrationPackageApi
from anzo_api.tests.test_utils.test_common import *
from io import BytesIO


class TestMigrationPackageApi(TestCase):

    def setUp(self):
        self.anzo = MigrationPackageApi(DOMAIN, port=PORT, username=USERNAME, password=PASSWORD)
        self.migration_uri = "http://cambridgesemantics.com/MigrationPackage/6f27007afef546d1b5fbba9062bc1d9c"

    def test_import_migration_package(self):
        result = self.anzo.import_migration_package(migration_package="./test_utils/ExamplePackage_20240320181221.zip")
        self.assertTrue(result)

    def test_export_migration_package(self):
        self.anzo.import_migration_package(migration_package="./test_utils/ExamplePackage_20240320181221.zip")
        result = self.anzo.export_migration_package(migration_package_uri=self.migration_uri)
        self.assertIsInstance(result, BytesIO)
