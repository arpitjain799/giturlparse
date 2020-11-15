# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import unittest

from giturlparse import parse

# Test data
VALID_PARSE_URLS = (
    # Valid SSH, HTTPS, GIT
    ('SSH', ('git@github.com:Org/Repo.git', {
        'host': 'github.com',
        'resource': 'github.com',
        'user': 'git',
        'port': '',
        'owner': 'Org',
        'repo': 'Repo',
        'name': 'Repo',
        'groups': [],
        'path': '',
        'path_raw': '',
        'pathname': 'Org/Repo.git',
        'branch': '',
        'protocol': 'ssh',
        'protocols': [],
        'github': True,
        'bitbucket': False,
        'assembla': False
    })),
    ('HTTPS', ('git+https://github.com/Org/Repo.git', {
        'host': 'github.com',
        'resource': 'github.com',
        'user': 'git',
        'port': '',
        'owner': 'Org',
        'repo': 'Repo',
        'name': 'Repo',
        'groups': [],
        'path': '',
        'path_raw': '',
        'pathname': '/Org/Repo.git',
        'branch': '',
        'protocol': 'https',
        'protocols': ['git', 'https'],
        'github': True,
        'bitbucket': False,
        'assembla': False
    })),
    ('HTTPS', ('https://github.com/foo-bar/xpwn', {
        'host': 'github.com',
        'resource': 'github.com',
        'user': 'git',
        'port': '',
        'owner': 'foo-bar',
        'repo': 'xpwn',
        'name': 'xpwn',
        'groups': [],
        'path': '',
        'path_raw': '',
        'pathname': '/foo-bar/xpwn',
        'branch': '',
        'protocol': 'https',
        'protocols': ['https'],
        'github': True,
    })),
    ('GIT', ('git://github.com/Org/Repo.git', {
        'host': 'github.com',
        'resource': 'github.com',
        'user': 'git',
        'port': '',
        'owner': 'Org',
        'repo': 'Repo',
        'name': 'Repo',
        'groups': [],
        'path': '',
        'path_raw': '',
        'pathname': '/Org/Repo.git',
        'branch': '',
        'protocol': 'git',
        'protocols': ['git'],
        'github': True,
    })),
    ('GIT', ('git://github.com/foo-bar/xpwn', {
        'host': 'github.com',
        'resource': 'github.com',
        'user': 'git',
        'port': '',
        'owner': 'foo-bar',
        'repo': 'xpwn',
        'name': 'xpwn',
        'groups': [],
        'path': '',
        'path_raw': '',
        'pathname': '/foo-bar/xpwn',
        'branch': '',
        'protocol': 'git',
        'protocols': ['git'],
        'github': True,
    })),

    # BitBucket
    ('SSH', ('git@bitbucket.org:Org/Repo.git', {
        'host': 'bitbucket.org',
        'resource': 'bitbucket.org',
        'user': 'git',
        'port': '',
        'owner': 'Org',
        'repo': 'Repo',
        'name': 'Repo',
        'groups': [],
        'path': '',
        'path_raw': '',
        'pathname': 'Org/Repo.git',
        'branch': '',
        'protocol': 'ssh',
        'protocols': [],
        'platform': 'bitbucket'
    })),

    # Gitlab
    ('SSH', ('git@host.org:9999/Org/Repo.git', {
        'host': 'host.org',
        'resource': 'host.org',
        'user': 'git',
        'port': '9999',
        'owner': 'Org',
        'repo': 'Repo',
        'name': 'Repo',
        'groups': [],
        'path': '',
        'path_raw': '',
        'pathname': '/Org/Repo.git',
        'branch': '',
        'protocol': 'ssh',
        'protocols': [],
        'platform': 'gitlab'
    })),
    ('SSH', ('git@host.org:9999/Org-hyphen/Repo.git', {
        'host': 'host.org',
        'resource': 'host.org',
        'user': 'git',
        'port': '9999',
        'owner': 'Org-hyphen',
        'repo': 'Repo',
        'name': 'Repo',
        'groups': [],
        'path': '',
        'path_raw': '',
        'pathname': '/Org-hyphen/Repo.git',
        'branch': '',
        'protocol': 'ssh',
        'protocols': [],
        'platform': 'gitlab'
    })),
    ('SSH', ('git@host.org:Org/Repo.git', {
        'host': 'host.org',
        'resource': 'host.org',
        'user': 'git',
        'port': '',
        'owner': 'Org',
        'repo': 'Repo',
        'name': 'Repo',
        'groups': [],
        'path': '',
        'path_raw': '',
        'pathname': 'Org/Repo.git',
        'branch': '',
        'protocol': 'ssh',
        'protocols': [],
        'platform': 'gitlab'
    })),
    ('SSH', ('ssh://git@host.org:9999/Org/Repo.git', {
        'host': 'host.org',
        'resource': 'host.org',
        'user': 'git',
        'port': '9999',
        'owner': 'Org',
        'repo': 'Repo',
        'name': 'Repo',
        'groups': [],
        'path': '',
        'path_raw': '',
        'pathname': '/Org/Repo.git',
        'branch': '',
        'protocol': 'ssh',
        'protocols': ['ssh'],
        'platform': 'gitlab'
    })),
    ('HTTPS', ('https://host.org/Org/Repo.git', {
        'host': 'host.org',
        'resource': 'host.org',
        'user': 'git',
        'port': '',
        'owner': 'Org',
        'repo': 'Repo',
        'name': 'Repo',
        'groups': [],
        'path': '',
        'path_raw': '',
        'pathname': '/Org/Repo.git',
        'branch': '',
        'protocol': 'https',
        'protocols': ['https'],
        'platform': 'gitlab'
    })),
    ('HTTPS', ('https://github.com/nephila/giturlparse/blob/master/giturlparse/github.py', {
        'host': 'github.com',
        'resource': 'github.com',
        'port': '',
        'user': 'git',
        'owner': 'nephila',
        'repo': 'giturlparse',
        'name': 'giturlparse',
        'groups': [],
        'path': 'master/giturlparse/github.py',
        'path_raw': '/blob/master/giturlparse/github.py',
        'pathname': '/nephila/giturlparse/blob/master/giturlparse/github.py',
        'branch': '',
        'protocol': 'https',
        'protocols': ['https'],
        'platform': 'github'
    })),
    ('HTTPS', ('https://github.com/nephila/giturlparse/tree/feature/py37', {
        'host': 'github.com',
        'resource': 'github.com',
        'user': 'git',
        'port': '',
        'owner': 'nephila',
        'repo': 'giturlparse',
        'name': 'giturlparse',
        'groups': [],
        'path': '',
        'path_raw': '/tree/feature/py37',
        'pathname': '/nephila/giturlparse/tree/feature/py37',
        'branch': 'feature/py37',
        'protocol': 'https',
        'protocols': ['https'],
        'platform': 'github'
    })),
    ('HTTPS', ('https://gitlab.com/nephila/giturlparse/blob/master/giturlparse/github.py', {
        'host': 'gitlab.com',
        'resource': 'gitlab.com',
        'user': 'git',
        'port': '',
        'owner': 'nephila',
        'repo': 'giturlparse',
        'name': 'giturlparse',
        'groups': [],
        'path': 'master/giturlparse/github.py',
        'path_raw': '/blob/master/giturlparse/github.py',
        'pathname': '/nephila/giturlparse/blob/master/giturlparse/github.py',
        'branch': '',
        'protocol': 'https',
        'protocols': ['https'],
        'platform': 'gitlab'
    })),
    ('HTTPS',
     ('https://gitlab.com/nephila/group2/third-group/giturlparse/blob/master/'
      'giturlparse/platforms/github.py', {
        'host': 'gitlab.com',
        'resource': 'gitlab.com',
        'user': 'git',
        'port': '',
        'owner': 'nephila',
        'repo': 'giturlparse',
        'name': 'giturlparse',
        'groups': ['group2', 'third-group'],
        'path': 'master/giturlparse/platforms/github.py',
        'path_raw': '/blob/master/giturlparse/platforms/github.py',
        'pathname': '/nephila/group2/third-group/giturlparse/blob/master/'
      'giturlparse/platforms/github.py',
        'branch': '',
        'protocol': 'https',
        'protocols': ['https'],
        'platform': 'gitlab'
      })),
    ('SSH', ('git@host.org:9999/Org/Group/subGroup/Repo.git/blob/master/giturlparse/github.py', {
        'host': 'host.org',
        'resource': 'host.org',
        'user': 'git',
        'port': '9999',
        'owner': 'Org',
        'repo': 'Repo',
        'name': 'Repo',
        'groups': ['Group', 'subGroup'],
        'path': 'master/giturlparse/github.py',
        'path_raw': '/blob/master/giturlparse/github.py',
        'pathname': '/Org/Group/subGroup/Repo.git/blob/master/giturlparse/github.py',
        'branch': '',
        'protocol': 'ssh',
        'protocols': [],
        'platform': 'gitlab'
    })),
    ('GIT', ('git://host.org:9999/Org/Group/subGroup/Repo.git/blob/master/giturlparse/github.py', {
        'host': 'host.org',
        'resource': 'host.org',
        'user': 'git',
        'port': '9999',
        'owner': 'Org',
        'repo': 'Repo',
        'name': 'Repo',
        'groups': ['Group', 'subGroup'],
        'path': 'master/giturlparse/github.py',
        'path_raw': '/blob/master/giturlparse/github.py',
        'pathname': '/Org/Group/subGroup/Repo.git/blob/master/giturlparse/github.py',
        'branch': '',
        'protocol': 'git',
        'protocols': ['git'],
        'platform': 'gitlab'
    })),
    ('GIT', ('git://host.org:9999/Org/Group/subGroup/Repo.git/-/tree/feature/custom-branch', {
        'host': 'host.org',
        'resource': 'host.org',
        'user': 'git',
        'port': '9999',
        'owner': 'Org',
        'repo': 'Repo',
        'name': 'Repo',
        'groups': ['Group', 'subGroup'],
        'path': '',
        'path_raw': '/-/tree/feature/custom-branch',
        'pathname': '/Org/Group/subGroup/Repo.git/-/tree/feature/custom-branch',
        'branch': 'feature/custom-branch',
        'protocol': 'git',
        'protocols': ['git'],
        'platform': 'gitlab'
    })),
)

INVALID_PARSE_URLS = (
    ('SSH No Username', '@github.com:Org/Repo.git'),
    ('SSH No Repo', 'git@github.com:Org'),
    ('HTTPS No Repo', 'https://github.com/Org'),
    ('GIT No Repo', 'git://github.com/Org'),
)


# Here's our "unit tests".
class UrlParseTestCase(unittest.TestCase):
    def _test_valid(self, url, expected):
        p = parse(url)
        self.assertTrue(p.valid, "%s is not a valid URL" % url)
        for k, v in expected.items():
            attr_v = getattr(p, k)
            self.assertEqual(
                attr_v, v, "[%s] Property '%s' should be '%s' but is '%s'" % (
                    url, k, v, attr_v
                )
            )

    def testValidUrls(self):
        for test_type, data in VALID_PARSE_URLS:
            self._test_valid(*data)

    def _test_invalid(self, url):
        p = parse(url)
        self.assertFalse(p.valid)

    def testInvalidUrls(self):
        for problem, url in INVALID_PARSE_URLS:
            self._test_invalid(url)


# Test Suite
suite = unittest.TestLoader().loadTestsFromTestCase(UrlParseTestCase)
