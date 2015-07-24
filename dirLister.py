"""dirLister, Directory Lister is pretty print module for listing
   directories and its sub-directories. It allows for some simple filtering
   including filtering out direcotory based on name or for filtering to a
   certain node depth.

"""

__author__ = 'Josh Windsor'
__contact__ = 'ging.sor@gmail.com'
__copyright__ = "Copyright 2015"
__license__ = "TBD"
__version__ = '2015.07'
__status__ = "Prototype"


import os
from copy import deepcopy


class DirectoryLister(object):
    """This class is use to pretty print directories"""

    def __init__(self, show_hidden=False, indent_size=4):
        """Constructor for DirectoryStructure"""

        #core
        self.pretty_dirs_structure = []
        self.base_dir = None
        self.dir_dict = {}
        self.pretty_marker = '|____/'
        self.indent_size = len(self.pretty_marker)

        #hidden
        self.show_hidden = show_hidden

        #filter
        self.filter_state = False
        self.filter_names = []
        self.max_levels = None

        # recursive helpers
        self.tmp_dir_dict = None

    def filter_on(self, names=None):
        """"""

        if not names:
            names = []

        self.filter_state = True
        self.filter_names = names

    def filter_off(self):
        """"""

        self.filter_state = False
        self.filter_names = []

    def is_filter_on(self):
        """"""

        return self.filter_state

    def show_hidden_on(self):
        """"""

        self.show_hidden = True

    def show_hidden_off(self):
        """"""

        self.show_hidden = False

    def is_show_hidden(self):
        """"""

        return self.show_hidden


    def parse_dirs(self, startpath=os.getcwd()):
        """Parses directory and all subdirecoties from supplied location"""

        if os.path.exists(startpath):

            self.base_dir = startpath.rsplit(os.sep, 1)[1]
            self.pretty_dirs_structure = []

            for root, dirs, files in os.walk(startpath):

                        dir_key = ''
                        dirs.reverse()
                        path = root.replace(startpath, '')
                        if path == '':
                            dir_key = self.base_dir
                            path = self.base_dir
                        else:
                            dir_key = root.rsplit(os.sep, 1)[1]
                            path = os.path.join(self.base_dir,path[1:])

                        dir_dict_bucket = {path: dirs}

                        if dir_key in self.dir_dict:
                            self.dir_dict[dir_key].update(dir_dict_bucket)
                        else:
                            self.dir_dict[dir_key] = dir_dict_bucket
        else:
            raise IOError("Directory supplied does not exist: {}".format(startpath))


        #build pretty dirs
        self.build_dirs()


    def build_dirs(self):
        """"""
        # Recursively build directories

        self.tmp_dir_dict = deepcopy(self.dir_dict)
        self.build_pretty_dir(self.base_dir, self.base_dir, 0)
        self.pretty_dirs_structure.insert(0, os.sep)


    def build_pretty_dir(self, dir_name, dir_path, level):
        """"""

        while len(self.tmp_dir_dict[dir_name][dir_path]) > 0:
            sub_dir_name = self.tmp_dir_dict[dir_name][dir_path][0]
            self.build_pretty_dir(sub_dir_name, os.path.join(dir_path,sub_dir_name) ,  level + 1)
            self.tmp_dir_dict[dir_name][dir_path].remove(sub_dir_name)

        # no more levels create pretty dir string
        intent = ' ' * self.indent_size * level
        pretty = intent + self.pretty_marker + dir_name
        self.pretty_dirs_structure.insert(0, pretty)


    def filter_dirs(self):
        """TODO - Need descp"""

        pretty_dirs_printout = []

        # create tuple list that has line_num and line.
        line_num = 0
        filter_dirs = []
        for line in self.pretty_dirs_structure:
            filter_dirs.append((line_num, line))
            line_num += 1

        # add any hidden directories to the filter_names
        if self.show_hidden is False:
            for line_num, line in filter_dirs:
                if '/.' in line:
                    self.filter_state = True
                    self.filter_names.append(line.rsplit(os.sep, 1)[1])

        i = 0
        while i < len(filter_dirs):
            line_num, line = filter_dirs[i]
            dir_name = line.rsplit(os.sep,1)[1]
            if dir_name in self.filter_names:
                j = line_num + 1
                indent_level = self.level(line.rsplit(os.sep, 1)[0] + os.sep)
                filter_indent_level = self.level(filter_dirs[j][1].rsplit(os.sep,1)[0] + os.sep)
                while indent_level < filter_indent_level:
                    j += 1
                    try:
                        filter_indent_level = self.level(filter_dirs[j][1].rsplit(os.sep,1)[0] + os.sep)
                    except IndexError:
                        i = j
                        break
                i = j
            else:
                pretty_dirs_printout.append(line)
                i += 1

        return pretty_dirs_printout


    def print_dirs(self):
        """Prints directories structure"""

        pretty_dirs_printout = self.filter_dirs()

        for line in pretty_dirs_printout:
            print(line)

    def level(self, indent):

        return len(indent.split(self.pretty_marker, 1)[0]) / self.indent_size


def main(argc, argv):

    start_path = os.getcwd()
    if argc == 2:
        start_path = argv[1]

    pretty_dir = DirectoryLister()
    pretty_dir.parse_dirs(start_path)
    pretty_dir.show_hidden_on()
    #pretty_dir.filter_on(['objects', 'refs', 'origin'])
    #pretty_dir.filter_on(['objects'])
    pretty_dir.print_dirs()


if __name__ == '__main__':
    import sys

    main(len(sys.argv), sys.argv)
