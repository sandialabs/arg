import os
import time


class StringSwapper:
    """ Swap strings in files with given extension in given directory.
    """
    def __init__(self, files_dir: str, extension: str, strings_to_swap: dict):
        self.files = None
        self.extension = extension.lower()
        self.files_dir = os.path.abspath(files_dir)
        self.strings_to_swap = strings_to_swap

    def find_files(self):
        """ Finds files to change.
        """
        if self.files is None:
            print(f"==========================================================================================")
            print('Finding files ...')
            self.files = [f"{self.files_dir}/{file}" for file in os.listdir(self.files_dir) if
                          os.path.isfile(f"{self.files_dir}/{file}") and os.path.splitext(f"{self.files_dir}/{file}")[
                              -1].lower() == self.extension]
            if self.files:
                print(f"Found {len(self.files)} files:")
                for file in self.files:
                    print(f"=> {file}")
            else:
                raise FileNotFoundError('No files were found!')

    def swap_strings(self):
        """ Swaps strings.
        """
        for file in self.files:
            print(f"==========================================================================================")
            print(f"=> Swapping in file {file}")
            with open(file, 'r') as read_file:
                s = read_file.read()
                for key, value in self.strings_to_swap.items():
                    print(f"==> Replacing {key} with {value}")
                    s = s.replace(key, value)
            with open(file, 'w') as write_file:
                print(f"===> Writing file {file}")
                write_file.write(s)

    def main(self):
        t0 = time.monotonic()
        self.find_files()
        self.swap_strings()
        print(f"==========================================================================================")
        print(f"All strings were swapped in {(time.monotonic() - t0):.3f} s")


if __name__ == "__main__":
    str_to_swap = {'<a href="index.html" class="icon icon-home"': '<a href="../index.html" class="icon icon-home"',
                   '<a href="#" class="icon icon-home"': '<a href="../index.html" class="icon icon-home"'}
    StringSwapper(files_dir='../docs/_sphinx/_build/html', extension='.html', strings_to_swap=str_to_swap).main()
