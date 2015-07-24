"""dirLister, Unittests

"""

__author__ = 'Josh Windsor'
__contact__ = 'ging.sor@gmail.com'


import unittest
from dirLister import DirectoryLister


class TestDirLister(unittest.TestCase):

    def setUp(self):
        self.pretty_dirs = DirectoryLister()

    def tearDown(self):
        self.pretty_dirs = None


    def test_parse_dir(self):

        #bad dir test
        with self.assertRaises(IOError):
            self.pretty_dirs.parse_dirs('/Non-existant/dir')

        #good dir test
        self.pretty_dirs.parse_dirs()
        self.assertListEqual(self.pretty_dirs.filter_dirs(), ['/', '|____/DirLister'] )

    def test_show_hidden(self):

        expected_dir_show_hidden_on = ['/',
                        '|____/DirLister',
                        '      |____/.git',
                        '            |____/branches',
                        '            |____/hooks',
                        '            |____/info',
                        '            |____/objects',
                        '                  |____/info',
                        '                  |____/pack',
                        '            |____/refs',
                        '                  |____/heads',
                        '                  |____/tags',
                        '      |____/.idea',
                        '            |____/inspectionProfiles'
                        ]
        #good dir test
        self.pretty_dirs.parse_dirs()
        self.pretty_dirs.show_hidden_on()
        self.assertListEqual(self.pretty_dirs.filter_dirs(), expected_dir_show_hidden_on )

        expected_dir_show_hidden_off = ['/',
                                       '|____/DirLister'
                                       ]

        #good dir test
        self.pretty_dirs.parse_dirs()
        self.pretty_dirs.show_hidden_off()
        self.assertListEqual(self.pretty_dirs.filter_dirs(), expected_dir_show_hidden_off)

    def test_filter(self):

        expected_dir_show_hidden_off_filter_on = ['/',
                                        '|____/DirLister'
                                        ]

        #good dir test
        self.pretty_dirs.parse_dirs()
        self.pretty_dirs.show_hidden_off()
        self.pretty_dirs.filter_on(['objects'])
        self.assertListEqual(self.pretty_dirs.filter_dirs(), expected_dir_show_hidden_off_filter_on)

        expected_dir_show_hidden_on_filter_on = ['/',
                                       '|____/DirLister',
                                       '      |____/.git',
                                       '            |____/branches',
                                       '            |____/hooks',
                                       '            |____/info',
                                       '            |____/refs',
                                       '                  |____/heads',
                                       '                  |____/tags',
                                       '      |____/.idea',
                                       '            |____/inspectionProfiles'
                                       ]
        #good dir test
        self.pretty_dirs.parse_dirs()
        self.pretty_dirs.show_hidden_on()
        self.pretty_dirs.filter_on(['objects'])
        self.assertListEqual(self.pretty_dirs.filter_dirs(), expected_dir_show_hidden_on_filter_on)

        expected_dir_show_hidden_on_filter_on_more = ['/',
                                                 '|____/DirLister',
                                                 '      |____/.git',
                                                 '            |____/branches',
                                                 '            |____/hooks',
                                                 '            |____/info',
                                                 '      |____/.idea',
                                                 '            |____/inspectionProfiles'
                                                 ]

        #good dir test
        self.pretty_dirs.parse_dirs()
        self.pretty_dirs.show_hidden_on()
        self.pretty_dirs.filter_on(['objects', 'refs', 'origin'])
        self.assertListEqual(self.pretty_dirs.filter_dirs(), expected_dir_show_hidden_on_filter_on_more)

if __name__ == '__main__':
    unittest.main()