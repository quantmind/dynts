from dynts.utils import test
from dynts.lib import make_skiplist
from dynts.utils.populate import populate


class CythonSkiplistInsert(test.BenchMark):
    size = 10000
    number = 10

    def setUp(self):
        self.data = populate(size=self.size)

    def __str__(self):
        return '%s (%s elements, %s times)' % (
            self.__class__.__name__, self.size, self.number)

    def run(self):
        make_skiplist(self.data)


class CythonSkiplistIteration(CythonSkiplistInsert):
    data = None

    def setUp(self):
        self.data = make_skiplist(populate(size=self.size))

    def run(self):
        pass


class SkiplistInsert(CythonSkiplistInsert):

    def run(self):
        make_skiplist(self.data, use_fallback=True)


class SkiplistIteration(CythonSkiplistIteration):

    def setUp(self):
        self.data = make_skiplist(populate(size=self.size), use_fallback=True)
