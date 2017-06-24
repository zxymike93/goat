from unittest import skip

from functional_tests.base import FunctionalTest


class ValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty(self):
        # you post an empty input

        # refresh the page
        # warning: no empty input

        # enter something
        # ok

        # post another empty input
        # warning again

        self.fail('Write me!')
