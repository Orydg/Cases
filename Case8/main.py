import os

DIRECTORY = r'test'


class RenameFiles:

    def __init__(self, find_directory):

        self.Num = 0
        self.load(find_directory)

    def reset(self):
        """
        Сброс счетчика.

        """
        self.Num = 0

    def get_valid_name(self, name):
        valid_name = name.replace(name, str(self.Num) + '.png')
        self.Num += 1
        return valid_name

    def rename_file(self, root, name):
        valid_name = self.get_valid_name(name)
        old_file = os.path.join(root, name)
        new_file = os.path.join(root, valid_name)
        os.rename(old_file, new_file)

    def load(self, find_directory):

        for root, dirs, files in os.walk(find_directory):
            for name in files:
                self.rename_file(root, name)


if __name__ == '__main__':
    rename = RenameFiles(DIRECTORY)
