# -*- coding: utf-8 -*-
from vcr_unittest import VCRTestCase


class VCRMixin:
    def _get_vcr_kwargs(self, **kwargs):
        kwargs['record_mode'] = 'new_episodes'
        return kwargs


class BaseTest(VCRMixin, VCRTestCase):
    def assertEqualPersons(self, persons, names):
        return self.assertEqual([person.__repr__() for person in persons], names)
