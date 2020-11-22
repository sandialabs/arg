import argparse
import os
import subprocess


class PdfComparatorCli:
    """ Class responsible for comparison two pdf files having the same name in different directories.
        Can be run as script from console when all optional arguments are passed.
        Can be imported and used in another Python script when all optional parameters are passes to class Constructor.
        Class uses external tools `diff` and `ImageMagick` which needs to installed in the system.
        :param page_range: Pages to comparison, starts from 0, e.g. '0-15', '1-1'
        :param exp_dir: Path to template DIRECTORY where file is located
        :param exp_dir: Path to generated DIRECTORY where file is located
        :param file_name: File name for comparison with .pdf extension, e.g. 'report.pdf' (same in both directories)
    """

    def __init__(self, page_range: str = None, exp_dir: str = None, gen_dir: str = None, file_name: str = None):
        self.cur_dir = os.path.abspath('')
        self.exp_png = 'exp.png'
        self.gen_png = 'gen.png'
        if page_range is not None and exp_dir is not None and gen_dir is not None and file_name is not None:
            self.first_page = int(page_range.split('-')[0])
            self.last_page = int(page_range.split('-')[1])
            self.exp_file_name = os.path.join(exp_dir, file_name)
            self.gen_file_name = os.path.join(gen_dir, file_name)
        else:
            self.first_page = None
            self.last_page = None
            self.exp_file_name = None
            self.gen_file_name = None

    def __cli(self):
        """ Method responsible for parsing command line arguments, when run directly from console.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-r", "--range", help="Pages to comparison, starts from 0, e.g. '0-15', '1-1'")
        parser.add_argument("-e", "--expected", help="Path to template file (directory)")
        parser.add_argument("-g", "--generated", help="Path to generated file (directory)")
        parser.add_argument("-f", "--file_name", help="File name for comparison with .pdf extension, e.g. 'report.pdf'")
        args = parser.parse_args()

        if not args.range or not args.expected or not args.generated or not args.file_name:
            raise RuntimeError('Provide all parameters!')
        else:
            self.first_page = int(args.range.split('-')[0])
            self.last_page = int(args.range.split('-')[1])
            self.exp_file_name = os.path.join(args.expected, args.file_name)
            self.gen_file_name = os.path.join(args.generated, args.file_name)

    def __check_parameters(self):
        """ Checks if all parameters were passed. If not raise error.
        """
        if self.first_page is None or self.last_page is None or self.exp_file_name is None \
                or self.gen_file_name is None:
            raise RuntimeError('Provide all parameters!')

    def check_files(self):
        """ Checks if pdf files exist. Checks extension.
        """
        self.__check_parameters()
        print(f"==========================================================================================")
        print(f"Checking if files exists...")
        for file in [self.exp_file_name, self.gen_file_name]:
            if not os.path.isfile(file):
                raise FileNotFoundError(f"File: {file} not found")
            else:
                print(f"File: \n{file} \nFOUND!")
            if os.path.splitext(file)[-1] != '.pdf':
                raise NameError(f"Provide file: {file} with .pdf extension")

    def generate_png(self, input_file: str, output_file: str):
        """ Generates .png file of each page of .pdf document with ImageMagick.
        """
        self.__check_parameters()
        print(f"==========================================================================================")
        print(f"Converting pdf file: \n{input_file}\n=> png files: \n{output_file}")
        cmds = ["convert", input_file, "-strip", output_file]
        script = subprocess.run(cmds, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if script.stdout or script.stderr:
            raise RuntimeError(f"ImageMagic Error! STDOUT: {script.stdout}, STDERR: {script.stderr}")

    def compare_png(self, expected_png: str, generated_png: str):
        """ Compares .png files with use of 'diff' tool.
            Raise error when something appears on stdout or stderr.
        """
        self.__check_parameters()
        page_nr = os.path.splitext(expected_png)[0].split("-")[-1]
        print(f"==========================================================================================")
        print(f"Comparing page number: {page_nr}")
        cmds = ["diff", expected_png, generated_png]
        script = subprocess.run(cmds, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if script.stdout or script.stderr:
            raise RuntimeError(f"STDOUT: {script.stdout}, STDERR: {script.stderr}")
        else:
            print(f"Page number: {page_nr} are the same!")

    def get_pngs_to_compare(self) -> map:
        """ Returns iterator of .png tuples for comparison, sorted by page numbers.
            Raise error when number of pages differs.
        """
        self.__check_parameters()
        def page_num(elem):
            """ Function returns page number for sorting purposes.
            """
            return int(os.path.splitext(elem)[0].split("-")[-1])

        exp_files = list()
        gen_files = list()
        for file in os.listdir(self.cur_dir):
            file_split_ext = os.path.splitext(file)
            minus_sep = file_split_ext[0].split("-")
            if file_split_ext[-1] == '.png' and int(minus_sep[-1]) in range(self.first_page, self.last_page + 1):
                if minus_sep[0][-3:] == os.path.splitext(self.exp_png)[0]:
                    exp_files.append(file)
                elif minus_sep[0][-3:] == os.path.splitext(self.gen_png)[0]:
                    gen_files.append(file)
        exp_files.sort(key=page_num)
        gen_files.sort(key=page_num)
        if len(exp_files) != len(gen_files):
            raise AssertionError(
                f"Number of pages differs!\nEXPECTED NUM OF PAGES: {len(exp_files)}\n"
                f"GENERATED NUM OF PAGES: {len(gen_files)}")
        print(f"==========================================================================================")
        print(f"FOUND: {len(exp_files)} PAGES!")

        return zip(exp_files, gen_files)

    def main(self):
        self.__cli()
        self.check_files()
        self.generate_png(input_file=self.exp_file_name, output_file=os.path.join(self.cur_dir, self.exp_png))
        self.generate_png(input_file=self.gen_file_name, output_file=os.path.join(self.cur_dir, self.gen_png))
        pages_to_compare = self.get_pngs_to_compare()
        for page in pages_to_compare:
            self.compare_png(expected_png=page[0], generated_png=page[1])
        print(f"======================================= SUCCEEDED ========================================")


if __name__ == "__main__":
    PdfComparatorCli().main()
