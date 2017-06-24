from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        input = self.browser.find_element_by_id('id-input-todo')
        self.assertAlmostEqual(
            input.location['x'] + input.size['width'] / 2,
            512,
            delta=5
        )
        # see if it keeps center after post
        input.send_keys('testing for center\n')
        input = self.browser.find_element_by_id('id-input-todo')
        self.assertAlmostEqual(
            input.location['x'] + input.size['width'] / 2,
            512,
            delta=5
        )
