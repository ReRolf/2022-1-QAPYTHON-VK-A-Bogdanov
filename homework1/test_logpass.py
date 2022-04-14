import pytest
from base import BaseCase
from ui.locators import basic_locators


class TestExample(BaseCase):

    @pytest.mark.UI
    def test_login(self):
        self.login()

    @pytest.mark.UI
    def test_logout(self):
        self.logout()

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
                basic_locators.FEEDS_TITLE_LOCATOR,
                "tools/feeds"
            ),
        ],
    )
    def test_following(self, locator_button, locator, url):
        self.following(locator_button, locator)

