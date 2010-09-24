from dynts.bench.suite import maketest

makebench(name,
          stmt = "handle=%s()\nhandle.request('%s')" % (name,DEFAULT_URL),
          setup = "from unuk.http import %s" % name)