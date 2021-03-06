import os
from unittest.mock import MagicMock

from imagekitio.client import ImageKit
from tests.dummy_data.file import (
    FAILED_DELETE_RESP,
    FAILED_GENERIC_RESP,
    SERVER_ERR_MSG,
    SUCCESS_DETAIL_MSG,
    SUCCESS_LIST_RESP_MESSAGE,
    SUCCESS_PURGE_CACHE_MSG,
    SUCCESS_PURGE_CACHE_STATUS_MSG,
)
from tests.helpers import (
    ClientTestCase,
    get_mocked_failed_resp,
    get_mocked_success_resp,
)

imagekit_obj = ImageKit(
    private_key="private_fake:", public_key="public_fake123:", url_endpoint="fake.com",
)


class TestUpload(ClientTestCase):
    """
    TestUpload class used to test upload method
    """

    image = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "dummy_data/image.png"
    )
    filename = "test"

    def test_upload_fails_on_unauthenticated_request(self):
        """
        Tests if the unauthenticated request restricted

        """

        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp()
        )
        resp = self.client.upload(file=self.image, file_name=self.filename)
        self.assertIsNotNone(resp["error"])
        self.assertIsNone(resp["response"])

    def test_upload_succeeds(self):
        """
        Tests if  upload succeeds
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_success_resp()
        )
        resp = self.client.upload(file=self.image, file_name=self.filename)
        self.assertIsNone(resp["error"])
        self.assertIsNotNone(resp["response"])

    def test_upload_fails_without_file_or_file_name(self) -> None:
        """Test upload raises error on missing required params
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp()
        )
        self.assertRaises(TypeError, self.client.upload, file_name=self.filename)
        self.assertRaises(TypeError, self.client.upload, file=self.image)


class TestListFiles(ClientTestCase):
    """
    TestListFiles class used to test list_files method
    """

    def test_list_files_fails_on_unauthenticated_request(self) -> None:
        """ Tests unauthenticated request restricted for list_files method

        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp()
        )
        resp = self.client.list_files(self.options)
        self.assertIsNotNone(resp["error"])
        self.assertIsNone(resp["response"])

    def test_list_files_succeeds_with_basic_request(self) -> None:
        """
        Tests if list_files work with skip and limit
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_success_resp(message=SUCCESS_LIST_RESP_MESSAGE)
        )

        resp = self.client.list_files(self.options)

        self.assertIsNone(resp["error"])
        self.assertIsNotNone(resp["response"])


class TestGetFileDetails(ClientTestCase):
    """
    TestGetFileDetails class used to test get_file_details method
    """

    file_id = "fake_file_id1234"
    file_url = "https://example.com/default.jpg"

    def test_get_file_details_fails_on_unauthenticated_request(self) -> None:
        """Tests if get_file_details raise error on unauthenticated request
        """

        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp()
        )
        resp = self.client.get_file_details(self.file_id)
        self.assertIsNotNone(resp["error"])
        self.assertIsNone(resp["response"])

    def test_file_details_succeeds_with_id(self) -> None:
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_success_resp(message=SUCCESS_DETAIL_MSG)
        )
        resp = self.client.get_file_details(self.file_id)
        self.assertIsNone(resp["error"])
        self.assertIsNotNone(resp["response"])

    def test_file_details_succeeds_with_url(self) -> None:
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_success_resp(message=SUCCESS_DETAIL_MSG)
        )
        resp = self.client.get_file_details(self.file_url)
        self.assertIsNone(resp["error"])
        self.assertIsNotNone(resp["response"])


class TestDeleteFile(ClientTestCase):
    file_id = "fax_abx1223"

    def test_file_delete_fails_on_unauthenticated_request(self) -> None:
        """Test delete_file on unauthenticated request
        this function checks if raises error on unauthenticated request
        to check if delete is only restricted to authenticated
        user
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp()
        )
        resp = self.client.delete_file(self.file_id)

        self.assertIsNotNone(resp["error"])
        self.assertIsNone(resp["response"])

    def test_file_delete_fails_on_item_not_found(self):
        """Test delete_file on unavailable content
        this function raising expected error if the file
        is not available
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp(message=FAILED_DELETE_RESP)
        )
        resp = self.client.delete_file(self.file_id)

        self.assertIsNotNone(resp["error"])
        self.assertIsNone(resp["response"])

    def test_file_delete_succeeds(self):
        """Test delete file on authenticated request
        this function tests if delete_file working properly
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_success_resp({"error": None, "response": None})
        )
        resp = self.client.delete_file(self.file_id)

        self.assertIsNone(resp["error"])
        self.assertIsNone(resp["response"])


class TestPurgeCache(ClientTestCase):
    fake_image_url = "https://example.com/fakeid/fakeimage.jpg"

    def test_purge_cache_fails_on_unauthenticated_request(self) -> None:
        """Test purge_cache unauthenticated request
        this function checks if raises error on unauthenticated request
        to check if purge_cache is only restricted to authenticated request
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp()
        )
        resp = self.client.purge_cache(self.fake_image_url)
        self.assertIsNotNone(resp["error"])
        self.assertIsNone(resp["response"])

    def test_purge_cache_fails_without_passing_file_url(self) -> None:
        """Test purge_cache raises error on invalid_body request
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp()
        )
        self.assertRaises(TypeError, self.client.purge_cache)

    def test_purge_cache_succeeds(self) -> None:
        """Test purge_cache working properly
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_success_resp(message=SUCCESS_PURGE_CACHE_MSG)
        )
        resp = self.client.purge_cache(self.fake_image_url)
        self.assertIsNone(resp["error"])
        self.assertIsNotNone(resp["response"])
        self.assertIn("request_id", resp["response"])


class TestPurgeCacheStatus(ClientTestCase):
    cache_request_id = "fake1234"

    def test_get_purge_cache_status_fails_on_unauthenticated_request(self) -> None:
        """Test get_purge_cache_status unauthenticated request
        this function checks if raises error on unauthenticated request
        to check if get_purge_cache_status is only restricted to authenticated
        user
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp()
        )
        resp = self.client.get_purge_cache_status(self.cache_request_id)
        self.assertIsNotNone(resp["error"])
        self.assertIsNone(resp["response"])

    def test_purge_cache_status_fails_without_passing_file_url(self) -> None:
        """Test purge_cache raises error on invalid_body request
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp()
        )
        self.assertRaises(TypeError, self.client.get_purge_cache_status)

    def test_purge_cache_status_succeeds(self) -> None:
        """Test delete file on authenticated request
        this function tests if delete_file working properly
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_success_resp(message=SUCCESS_PURGE_CACHE_STATUS_MSG)
        )
        resp = self.client.get_purge_cache_status(self.cache_request_id)
        self.assertIsNone(resp["error"])
        self.assertIsNotNone(resp["response"])


class TestGetMetaData(ClientTestCase):
    file_id = "fake_file_xbc"

    def test_get_metadata_fails_on_unauthenticated_request(self) -> None:
        """Tests get_metadata raise error on unauthenticated request
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp()
        )
        resp = self.client.get_metadata(file_id=self.file_id)
        self.assertIsNotNone(resp["error"])
        self.assertIsNone(resp["response"])

    def test_purge_cache_status_fails_without_passing_file_id(self) -> None:
        """Test purge_cache raises error on invalid_body request
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp()
        )
        self.assertRaises(TypeError, self.client.get_metadata())

    def test_get_metadata_succeeds(self):
        """Tests if get_metadata working properly
        """

        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_success_resp()
        )
        resp = self.client.get_metadata(file_id=self.file_id)
        self.assertIsNone(resp["error"])
        self.assertIsNotNone(resp["response"])


class TestUpdateFileDetails(ClientTestCase):
    """
    TestUpdateFileDetails class used to update file details method
    """

    file_id = "fake_123"

    valid_options = {"tags": ["tag1", "tag2"], "custom_coordinates": "10,10,100,100"}
    invalid_options = {"tags": "", "custom_coordinates": ""}

    def test_details_fails_on_unauthenticated_request(self):
        """
        Tests if the unauthenticated request restricted

        """

        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp()
        )
        resp = self.client.update_file_details(
            file_id=self.file_id, options=self.valid_options
        )
        self.assertIsNotNone(resp["error"])
        self.assertIsNone(resp["response"])

    def test_update_file_details_succeeds_with_id(self):
        """
        Tests if  update_file_details succeeds with file_url
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_success_resp()
        )
        resp = self.client.update_file_details(
            file_id=self.file_id, options=self.valid_options
        )
        self.assertIsNone(resp["error"])
        self.assertIsNotNone(resp["response"])

    def test_file_details_succeeds_with_url(self):
        self.client.ik_request = MagicMock(return_value=get_mocked_success_resp())

    def test_update_file_details_fails_without_file_or_file_name(self) -> None:
        """Test upload raises error on missing required params
        """
        self.client.ik_request.request = MagicMock(
            return_value=get_mocked_failed_resp()
        )
        self.assertRaises(
            ValueError,
            self.client.update_file_details,
            file_id=self.file_id,
            options=self.invalid_options,
        )
