from unittest.mock import Mock, patch

import pytest

from nba_miner.api import NBAApi


class TestNBAApi(object):
    @classmethod
    def setup_class(self):
        self.mock_get_patcher = patch("nba_warehouse.api.requests.get")
        self.mock_get = self.mock_get_patcher.start()

        self.url = "http://someurl.com"
        self.nba_api = NBAApi(self.url)

    @classmethod
    def teardown_class(self):
        self.mock_get_patcher.stop()

    def test_nba_api_url_is_correct(self):
        assert self.nba_api.url == self.url

    def test_nba_api_no_url_provided_raises_exception(self):
        with pytest.raises(TypeError):
            NBAApi()

    def test_get_data_from_nba_api_is_ok(self):
        self.mock_get.return_value = Mock(ok=True)

        response = self.nba_api.get()

        assert self.mock_get.called == True
        assert response.ok is True

    def test_get_data_from_nba_api_is_not_ok(self):
        self.mock_get.return_value = Mock(ok=False)

        response = self.nba_api.get()

        assert self.mock_get.called == True
        assert response is None
