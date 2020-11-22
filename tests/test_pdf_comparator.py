import os
import random
import shutil
import subprocess
from unittest import TestCase
from unittest.mock import patch, Mock

from utils.pdf_comparison import PdfComparatorCli


class TestPdfComparatorCli(TestCase):
    def setUp(self) -> None:
        self.page_range = '2-5'
        self.last_page = int(self.page_range.split('-')[1])
        self.cur_dir = os.path.abspath('')
        self.exp_dir = os.path.join(self.cur_dir, 'exp')
        self.gen_dir = os.path.join(self.cur_dir, 'gen')
        self.build_tests_templates = list()
        self.__initialize_test()

    def __initialize_test(self) -> None:
        os.mkdir(self.exp_dir)
        os.mkdir(self.gen_dir)
        self.__test_case_finder()

    def __test_case_finder(self) -> None:
        test_names = list()
        for directory in os.listdir(os.path.join(self.cur_dir, 'build_tests')):
            test_names.append(directory)
        for test in test_names:
            file_path = os.path.join(self.cur_dir, 'build_tests', test, 'expected',
                                     f'build_tests-{test}-Report-LaTeX.pdf')
            if os.path.isfile(file_path):
                self.build_tests_templates.append(file_path)

    def tearDown(self) -> None:
        shutil.rmtree(self.exp_dir)
        shutil.rmtree(self.gen_dir)
        for file in os.listdir(self.cur_dir):
            if os.path.splitext(file)[-1] == '.png':
                os.remove(file)

    @staticmethod
    def sub_run(stdout: str = '', stderr: str = ''):
        ret_val = Mock()
        ret_val.stdout = stdout
        ret_val.stderr = stderr
        return ret_val

    @patch.object(subprocess, 'run')
    def test_comparison_should_succeded(self, sub_mock):
        for page in range(self.last_page + 1):
            exp = os.path.join(self.cur_dir, f"exp-{page}.png")
            gen = os.path.join(self.cur_dir, f"gen-{page}.png")
            with open(exp, 'w') as f_exp:
                f_exp.write('png')
            with open(gen, 'w') as f_gen:
                f_gen.write('png')
        sub_mock.return_value = self.sub_run()
        random_report = random.choice(self.build_tests_templates)
        random_report_name = os.path.split(random_report)[-1]
        expected_report = os.path.join(self.exp_dir, random_report_name)
        generated_report = os.path.join(self.gen_dir, random_report_name)
        shutil.copy(random_report, expected_report)
        shutil.copy(random_report, generated_report)
        pcc = PdfComparatorCli(page_range=self.page_range, exp_dir=self.exp_dir, gen_dir=self.gen_dir,
                               file_name=random_report_name)
        pcc.check_files()
        pcc.generate_png(input_file=expected_report, output_file=os.path.join(self.cur_dir, 'exp.png'))
        pcc.generate_png(input_file=generated_report, output_file=os.path.join(self.cur_dir, 'gen.png'))
        pages_to_compare = pcc.get_pngs_to_compare()
        for page in pages_to_compare:
            pcc.compare_png(expected_png=page[0], generated_png=page[1])

    def test_comparison_not_all_params(self):
        pcc = PdfComparatorCli(page_range=self.page_range, exp_dir=self.exp_dir, gen_dir=self.gen_dir)
        with self.assertRaises(RuntimeError) as e:
            pcc.check_files()
        self.assertEqual(e.exception.args[0], 'Provide all parameters!')

    def test_comparison_no_files(self):
        file_name = os.path.join(self.exp_dir, 'testname')
        pcc = PdfComparatorCli(page_range=self.page_range, exp_dir=self.exp_dir, gen_dir=self.gen_dir,
                               file_name=file_name)
        with self.assertRaises(FileNotFoundError) as e:
            pcc.check_files()
        self.assertEqual(e.exception.args[0], f'File: {file_name} not found')

    def test_comparison_wrong_types(self):
        file_name = 'testfile.png'
        exp_png_file = os.path.join(self.exp_dir, file_name)
        gen_png_file = os.path.join(self.gen_dir, file_name)
        with open(exp_png_file, 'w') as exp:
            exp.write('test')
        with open(gen_png_file, 'w') as gen:
            gen.write('test')
        pcc = PdfComparatorCli(page_range=self.page_range, exp_dir=self.exp_dir, gen_dir=self.gen_dir,
                               file_name=file_name)
        with self.assertRaises(NameError) as e:
            pcc.check_files()
        self.assertEqual(e.exception.args[0], f'Provide file: {exp_png_file} with .pdf extension')

    @patch.object(subprocess, 'run')
    def test_comparison_image_magic_stdout(self, sub_mock):
        for page in range(self.last_page + 1):
            exp = os.path.join(self.cur_dir, f"exp-{page}.png")
            gen = os.path.join(self.cur_dir, f"gen-{page}.png")
            with open(exp, 'w') as f_exp:
                f_exp.write('png')
            with open(gen, 'w') as f_gen:
                f_gen.write('png')
        stdout = 'TESTERROR'
        sub_mock.return_value = self.sub_run(stdout=stdout)
        random_report = random.choice(self.build_tests_templates)
        random_report_name = os.path.split(random_report)[-1]
        expected_report = os.path.join(self.exp_dir, random_report_name)
        generated_report = os.path.join(self.gen_dir, random_report_name)
        shutil.copy(random_report, expected_report)
        shutil.copy(random_report, generated_report)
        pcc = PdfComparatorCli(page_range=self.page_range, exp_dir=self.exp_dir, gen_dir=self.gen_dir,
                               file_name=random_report_name)
        pcc.check_files()
        with self.assertRaises(RuntimeError) as e:
            pcc.generate_png(input_file=expected_report, output_file=os.path.join(self.cur_dir, 'exp.png'))
            pcc.generate_png(input_file=generated_report, output_file=os.path.join(self.cur_dir, 'gen.png'))
        self.assertEqual(e.exception.args[0], f"ImageMagic Error! STDOUT: {stdout}, STDERR: ")

    @patch.object(subprocess, 'run')
    def test_comparison_image_magic_stderr(self, sub_mock):
        for page in range(self.last_page + 1):
            exp = os.path.join(self.cur_dir, f"exp-{page}.png")
            gen = os.path.join(self.cur_dir, f"gen-{page}.png")
            with open(exp, 'w') as f_exp:
                f_exp.write('png')
            with open(gen, 'w') as f_gen:
                f_gen.write('png')
        stderr = 'TESTERROR'
        sub_mock.return_value = self.sub_run(stderr=stderr)
        random_report = random.choice(self.build_tests_templates)
        random_report_name = os.path.split(random_report)[-1]
        expected_report = os.path.join(self.exp_dir, random_report_name)
        generated_report = os.path.join(self.gen_dir, random_report_name)
        shutil.copy(random_report, expected_report)
        shutil.copy(random_report, generated_report)
        pcc = PdfComparatorCli(page_range='2-5', exp_dir=self.exp_dir, gen_dir=self.gen_dir,
                               file_name=random_report_name)
        pcc.check_files()
        with self.assertRaises(RuntimeError) as e:
            pcc.generate_png(input_file=expected_report, output_file=os.path.join(self.cur_dir, 'exp.png'))
            pcc.generate_png(input_file=generated_report, output_file=os.path.join(self.cur_dir, 'gen.png'))
        self.assertEqual(e.exception.args[0], f"ImageMagic Error! STDOUT: , STDERR: {stderr}")

    @patch.object(subprocess, 'run')
    def test_comparison_page_number_differs(self, sub_mock):
        for page in range(self.last_page + 1):
            exp = os.path.join(self.cur_dir, f"exp-{page}.png")
            with open(exp, 'w') as f_exp:
                f_exp.write('png')
        for page in range(self.last_page):
            gen = os.path.join(self.cur_dir, f"gen-{page}.png")
            with open(gen, 'w') as f_gen:
                f_gen.write('png')
        sub_mock.return_value = self.sub_run()
        lp_ran_len = len(list(range(int(self.page_range.split('-')[1]))))
        fp_ran_len = len(list(range(int(self.page_range.split('-')[0]))))
        exp_num_pages = lp_ran_len - fp_ran_len + 1
        gen_num_pages = lp_ran_len - fp_ran_len
        random_report = random.choice(self.build_tests_templates)
        random_report_name = os.path.split(random_report)[-1]
        expected_report = os.path.join(self.exp_dir, random_report_name)
        generated_report = os.path.join(self.gen_dir, random_report_name)
        shutil.copy(random_report, expected_report)
        shutil.copy(random_report, generated_report)
        pcc = PdfComparatorCli(page_range=self.page_range, exp_dir=self.exp_dir, gen_dir=self.gen_dir,
                               file_name=random_report_name)
        pcc.check_files()
        pcc.generate_png(input_file=expected_report, output_file=os.path.join(self.cur_dir, 'exp.png'))
        pcc.generate_png(input_file=generated_report, output_file=os.path.join(self.cur_dir, 'gen.png'))
        with self.assertRaises(AssertionError) as e:
            pages_to_compare = pcc.get_pngs_to_compare()
        self.assertEqual(e.exception.args[0],
                         f"Number of pages differs!\nEXPECTED NUM OF PAGES: {exp_num_pages}"
                         f"\nGENERATED NUM OF PAGES: {gen_num_pages}")

    @patch.object(subprocess, 'run')
    def test_compare_png_dif_stdout(self, sub_mock):
        for page in range(self.last_page + 1):
            exp = os.path.join(self.cur_dir, f"exp-{page}.png")
            gen = os.path.join(self.cur_dir, f"gen-{page}.png")
            with open(exp, 'w') as f_exp:
                f_exp.write('png')
            with open(gen, 'w') as f_gen:
                f_gen.write('png1')
        stdout = 'TESTERROR'
        sub_mock.side_effect = [self.sub_run(), self.sub_run(), self.sub_run(stdout=stdout)]
        random_report = random.choice(self.build_tests_templates)
        random_report_name = os.path.split(random_report)[-1]
        expected_report = os.path.join(self.exp_dir, random_report_name)
        generated_report = os.path.join(self.gen_dir, random_report_name)
        shutil.copy(random_report, expected_report)
        shutil.copy(random_report, generated_report)
        pcc = PdfComparatorCli(page_range=self.page_range, exp_dir=self.exp_dir, gen_dir=self.gen_dir,
                               file_name=random_report_name)
        pcc.check_files()
        pcc.generate_png(input_file=expected_report, output_file=os.path.join(self.cur_dir, 'exp.png'))
        pcc.generate_png(input_file=generated_report, output_file=os.path.join(self.cur_dir, 'gen.png'))
        pages_to_compare = pcc.get_pngs_to_compare()
        with self.assertRaises(RuntimeError) as e:
            for page in pages_to_compare:
                pcc.compare_png(expected_png=page[0], generated_png=page[1])
        self.assertEqual(e.exception.args[0], f"STDOUT: {stdout}, STDERR: ")

    @patch.object(subprocess, 'run')
    def test_compare_png_dif_stderr(self, sub_mock):
        for page in range(self.last_page + 1):
            exp = os.path.join(self.cur_dir, f"exp-{page}.png")
            gen = os.path.join(self.cur_dir, f"gen-{page}.png")
            with open(exp, 'w') as f_exp:
                f_exp.write('png')
            with open(gen, 'w') as f_gen:
                f_gen.write('png1')
        stderr = 'TESTERROR'
        sub_mock.side_effect = [self.sub_run(), self.sub_run(), self.sub_run(stderr=stderr)]
        random_report = random.choice(self.build_tests_templates)
        random_report_name = os.path.split(random_report)[-1]
        expected_report = os.path.join(self.exp_dir, random_report_name)
        generated_report = os.path.join(self.gen_dir, random_report_name)
        shutil.copy(random_report, expected_report)
        shutil.copy(random_report, generated_report)
        pcc = PdfComparatorCli(page_range=self.page_range, exp_dir=self.exp_dir, gen_dir=self.gen_dir,
                               file_name=random_report_name)
        pcc.check_files()
        pcc.generate_png(input_file=expected_report, output_file=os.path.join(self.cur_dir, 'exp.png'))
        pcc.generate_png(input_file=generated_report, output_file=os.path.join(self.cur_dir, 'gen.png'))
        pages_to_compare = pcc.get_pngs_to_compare()
        with self.assertRaises(RuntimeError) as e:
            for page in pages_to_compare:
                pcc.compare_png(expected_png=page[0], generated_png=page[1])
        self.assertEqual(e.exception.args[0], f"STDOUT: , STDERR: {stderr}")
