import filecmp
import os
import unittest
from shutil import rmtree

from pharmcat_runner import haplotype

PATH = os.path.dirname(os.path.abspath(__file__))


class TestFiles(unittest.TestCase):
    def setUp(self):
        haplotype.call_haplotypes(
            dir_=os.path.join(PATH, "test_files, *.vcf"),
            output_dir=os.path.join(PATH, "test_files", "test_output"),
        )

    def tearDown(self):
        rmtree(os.path.join(PATH, "test_files", "test_output"))

    def test_pipeline(self):
        variant_call_rate = 0.95
        sample_call_rate = 0.95
        hwe = 0.001
        f1 = os.path.join(PATH, "test_files", "something.vcf.gz")
        f2 = os.path.join(PATH, "test_files", "test_output", "something.vcf.gz")
        self.assertTrue(filecmp.cmp(f1, f2, shallow=False))

    def test_pharmcat(self):
        f1 = os.path.join(PATH, "test_files", "something.vcf.gz")
        f2 = os.path.join(PATH, "test_files", "test_output", "something.vcf.gz")
        self.assertTrue(filecmp.cmp(f1, f2, shallow=False))
