import pytest
from base import BaseCase
from ui.locators import basic_locators


class TestExample(BaseCase):

    @pytest.mark.UI
    def test_login(self):
        login_validation = self.login()
        assert 'dashboard' in self.driver.current_url
        assert login_validation

    @pytest.mark.UI
    def test_logout(self):
        logout_validation = self.logout()
        assert 'target.my.com' in self.driver.current_url
        assert logout_validation

    @pytest.mark.UI
    def test_edit(self):
        edit = self.edit()
        assert edit

    @pytest.mark.parametrize(
        'locator_button, locator, url',
        [
            pytest.param(
                basic_locators.AUDIENCE_BUTTON_LOCATOR,
                basic_locators.AUDIENCE_TEXT_LOCATOR,
                "segments/segments_list"
            ),
            pytest.param(
                basic_locators.TOOLS_BUTTON_LOCATOR,
                basic_locators.FEED_TEXT_LOCATOR,
                "tools/feeds"
            ),
        ],
    )
    def test_following(self, locator_button, locator, url):
        following = self.following(locator_button, locator)
        assert following
        assert url in self.driver.current_url
