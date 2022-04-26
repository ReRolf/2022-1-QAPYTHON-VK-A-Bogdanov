import pytest


@pytest.mark.API
class TestApi:
    @pytest.fixture(scope='function', autouse=True)
    def login(self, api_client):
        self.client = api_client

    @pytest.mark.API
    def test_segment(self):
        segment_id = self.client.post_segment_create()
        assert self.client.segment_checker(segment_id)
        assert self.client.post_segment_delete(segment_id)

    @pytest.mark.API
    def test_campaign(self):
        campaign_id = self.client.post_campaign_create()
        assert self.client.post_campaign(campaign_id, "GET")
        assert self.client.post_campaign(campaign_id, "POST")
