import unittest
import filecmp
import difflib
import os

env_dir = os.path.join(os.path.dirname(__file__), "..", "environments")


class ConditionUtilsTest(unittest.TestCase):
    @staticmethod
    def _diff_file(first, second):
        with open(first) as f1, open(second) as f2:
            for diff in difflib.context_diff(
                    f1.readlines(), f2.readlines(), fromfile=first, tofile=second):
                print(diff)

    def _same_files(self, env1, env2):
        dircmp = filecmp.dircmp(os.path.join(env_dir, env1), os.path.join(env_dir, env2))
        self.assertFalse(dircmp.left_only, "{} contains unique files: {}"
                         .format(env1, dircmp.left_only))
        self.assertFalse(dircmp.right_only, "{} contains unique files: {}"
                         .format(env2, dircmp.right_only))

        type_mappings = dircmp.subdirs['typemappings']
        self.assertFalse(type_mappings.left_only, "{} typemapings contains unique files: {}"
                         .format(env1, type_mappings.left_only))
        self.assertFalse(type_mappings.right_only, "{} typemapings contains unique files: {}"
                         .format(env2, type_mappings.right_only))

        types = dircmp.subdirs['types']
        self.assertFalse(types.left_only, "{} types contains unique files: {}"
                         .format(env1, types.left_only))
        self.assertFalse(types.right_only, "{} types contains unique files: {}"
                         .format(env2, types.right_only))
        for diff_file in types.diff_files:
            self._diff_file(os.path.join(types.left, diff_file),
                            os.path.join(types.right, diff_file))
        self.assertFalse(types.diff_files)

    def test_same_files_in_prod_and_appdev(self):
        self._same_files('prod', 'appdev')

    def test_same_files_in_prod_and_next(self):
        self._same_files('prod', 'next')
