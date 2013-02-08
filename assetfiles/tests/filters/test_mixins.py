import unittest

from assetfiles.filters import BaseFilter, MultiInputMixin, ExtensionMixin
from assetfiles.tests.base import is_glob2_available, AssetfilesTestCase


class MultiInputFilter(MultiInputMixin, BaseFilter):
    pass


class TestMultiInputMixin(AssetfilesTestCase):
    def mk_project_files(self):
        self.mkfile('static/file1.in')
        self.mkfile('static/dir1/file2.in')
        self.mkfile('static/dir1/file3.out')
        self.mkfile('static/dir2/file4.in')
        self.mkfile('app-1/static/file5.out')
        self.mkfile('app-1/static/file6.in')
        self.mkfile('app-1/static/dir1/file7.in')
        self.mkfile('app-1/static/dir3/file8.in')
        self.mkfile('app-2/static/file10.in')
        self.mkfile('app-2/static/dir4/subdir/file9.in')

    def test_matches_input_set_with_list(self):
        filter = MultiInputFilter(input_paths=(
            'dir/file1.in',
            'dir/file2.in',
            'dir/file3.in',
        ))
        self.assertFalse(filter.matches_input('file1.in'))
        self.assertFalse(filter.matches_input('dir/file1.out'))
        self.assertFalse(filter.matches_input('dir/file4.in'))
        self.assertFalse(filter.matches_input('dir/dir/file1.in'))
        self.assertTrue(filter.matches_input('dir/file1.in'))
        self.assertTrue(filter.matches_input('dir/file2.in'))
        self.assertTrue(filter.matches_input('dir/file3.in'))

    def test_matches_input_set_with_glob(self):
        filter = MultiInputFilter(input_paths='*.in')
        self.assertTrue(filter.matches_input('file1.in'))
        self.assertFalse(filter.matches_input('file1.out'))
        self.assertFalse(filter.matches_input('dir/file1.out'))
        self.assertTrue(filter.matches_input('dir/file4.in'))
        self.assertTrue(filter.matches_input('dir/dir/file1.in'))
        self.assertTrue(filter.matches_input('dir/file1.in'))
        self.assertTrue(filter.matches_input('dir/file2.in'))
        self.assertTrue(filter.matches_input('dir/file3.in'))

    def test_derives_input_paths_set_with_list(self):
        filter = MultiInputFilter(input_paths=(
            'dir/file1.in',
            'dir/file2.in',
            'dir/file3.in',
        ))
        self.assertEqual(filter.derive_input_paths('dir/file1.out'), [
            'dir/file1.in',
            'dir/file2.in',
            'dir/file3.in',
        ])

    def test_derives_input_paths_set_with_glob(self):
        filter1 = MultiInputFilter(input_paths='*.in')
        filter2 = MultiInputFilter(input_paths='dir1/*.in')
        self.mk_project_files()
        self.assertEqual(filter1.derive_input_paths('file.out'), [
            'file1.in',
            'file6.in',
            'file10.in',
        ])
        self.assertEqual(filter2.derive_input_paths('file.out'), [
            'dir1/file2.in',
            'dir1/file7.in',
        ])

    @unittest.skipUnless(is_glob2_available(), 'glob2 is not Python 3 compatible')
    def test_derives_input_paths_set_with_glob2(self):
        filter = MultiInputFilter(input_paths='**/*.in')
        self.mk_project_files()
        self.assertEqual(filter.derive_input_paths('file.out'), [
            'file1.in',
            'dir1/file2.in',
            'dir2/file4.in',
            'file6.in',
            'dir1/file7.in',
            'dir3/file8.in',
            'file10.in',
            'dir4/subdir/file9.in',
        ])

    def test_matches_set_input_path(self):
        filter = MultiInputFilter(input_path='dir/main.in')
        self.assertFalse(filter.matches_input('main.in'))
        self.assertFalse(filter.matches_input('dir/main.out'))
        self.assertFalse(filter.matches_input('dir/main'))
        self.assertFalse(filter.matches_input('dir/dir/main.in'))
        self.assertTrue(filter.matches_input('dir/main.in'))

    def test_derives_set_input_path(self):
        filter = MultiInputFilter(input_path='dir/main.in')
        self.assertEqual(filter.derive_input_paths('dir/main.in'),
            ['dir/main.in'])


class ExtensionFilter(ExtensionMixin, BaseFilter):
    input_exts = ('foo', 'baz')
    output_ext = 'bar'


class TessExtensionMixin(AssetfilesTestCase):
    def test_matches_input_file_by_ext(self):
        filter = ExtensionFilter()
        self.assertTrue(filter.matches_input('main.foo'))
        self.assertTrue(filter.matches_input('main.baz'))
        self.assertTrue(filter.matches_input('main.plugin.foo'))
        self.assertFalse(filter.matches_input('main.css'))

    def test_does_not_match_input_file_without_input_exts(self):
        filter = ExtensionFilter()
        filter.input_exts = ()
        self.assertFalse(filter.matches_input('main.foo'))
        self.assertFalse(filter.matches_input('main.baz'))

    def test_set_single_input_ext(self):
        filter = ExtensionFilter()
        filter.input_ext = 'foo'
        self.assertEqual(('foo',), filter.input_exts)

    def test_matches_output_file_by_ext(self):
        filter = ExtensionFilter()
        self.assertTrue(filter.matches_output('main.bar'))
        self.assertTrue(filter.matches_output('main.plugin.bar'))
        self.assertFalse(filter.matches_output('main.foo'))

    def test_does_not_match_output_file_without_output_ext(self):
        filter = ExtensionFilter()
        filter.output_ext = None
        self.assertFalse(filter.matches_output('main.bar'))

    def test_derive_input_paths(self):
        filter = ExtensionFilter()
        self.assertEqual([
            'dir/main.bar.foo',
            'dir/main.foo',
            'dir/main.bar.baz',
            'dir/main.baz',
        ], filter.derive_input_paths('dir/main.bar'))
        self.assertEqual([
            'dir/main.plugin.bar.foo',
            'dir/main.plugin.foo',
            'dir/main.plugin.bar.baz',
            'dir/main.plugin.baz',
        ], filter.derive_input_paths('dir/main.plugin.bar'))

    def test_derive_output_path(self):
        filter = ExtensionFilter()
        self.assertEqual('dir/main.bar',
            filter.derive_output_path('dir/main.foo'))
        self.assertEqual('dir/main.bar',
            filter.derive_output_path('dir/main.bar.foo'))
        self.assertEqual('dir/main.plugin.bar',
            filter.derive_output_path('dir/main.plugin.foo'))

    def test_matches_set_input_path(self):
        filter = ExtensionFilter(input_path='dir/main.in')
        self.assertFalse(filter.matches_input('main.in'))
        self.assertFalse(filter.matches_input('dir/main.out'))
        self.assertFalse(filter.matches_input('dir/main'))
        self.assertFalse(filter.matches_input('dir/dir/main.in'))
        self.assertTrue(filter.matches_input('dir/main.in'))

    def test_derives_set_input_path(self):
        filter = ExtensionFilter(input_path='dir/main.in')
        self.assertEqual(filter.derive_input_paths('dir/main.in'),
            ['dir/main.in'])

    def test_matches_set_output_path(self):
        filter = ExtensionFilter(output_path='dir/main.out')
        self.assertFalse(filter.matches_output('main.out'))
        self.assertFalse(filter.matches_output('dir/main.in'))
        self.assertFalse(filter.matches_output('dir/main'))
        self.assertFalse(filter.matches_output('dir/dir/main.out'))
        self.assertTrue(filter.matches_output('dir/main.out'))

    def test_derives_set_output_path(self):
        filter = ExtensionFilter(output_path='dir/main.out')
        self.assertEqual(filter.derive_output_path('main.in'), 'dir/main.out')
        self.assertEqual(filter.derive_output_path('dir/main.in'), 'dir/main.out')
