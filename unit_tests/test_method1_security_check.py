from nose.tools import raises

from integration_tests.files import require_empty_dir
from integration_tests.files import touch
from integration_tests.files import unset_sticky_bit
from integration_tests.files import set_sticky_bit
from integration_tests.files import having_file

from trashcli.trash import mkdirs
from trashcli.trash import TopDirIsSymLink
from trashcli.trash import TopDirNotPresent
from trashcli.trash import TopDirWithoutStickyBit
from trashcli.trash import Method1VolumeTrashDirectory

import os

class TestMethod1VolumeTrashDirectory:
    def setUp(self):
        require_empty_dir('sandbox')
        self.checker = Method1VolumeTrashDirectory()

    @raises(TopDirWithoutStickyBit)
    def test_check_when_no_sticky_bit(self):
        mkdirs("sandbox/trash-dir")
        unset_sticky_bit('sandbox/trash-dir')

        self.checker.check('sandbox/trash-dir/123')

    @raises(TopDirNotPresent)
    def test_check_when_no_dir(self):
        touch('sandbox/trash-dir')
        set_sticky_bit('sandbox/trash-dir')

        self.checker.check('sandbox/trash-dir/123')

    @raises(TopDirIsSymLink)
    def test_check_when_is_symlink(self):
        mkdirs('sandbox/trash-dir-dest')
        set_sticky_bit('sandbox/trash-dir-dest')
        os.symlink('trash-dir-dest', 'sandbox/trash-dir')

        self.checker.check('sandbox/trash-dir/123')

    def test_check_pass(self):
        mkdirs('sandbox/trash-dir')
        set_sticky_bit('sandbox/trash-dir')

        self.checker.check('sandbox/trash-dir/123')

