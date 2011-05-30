#!/usr/bin/env python
from migrate.versioning.shell import main
main(url='postgresql://tnz_layer:c0ns0le@localhost:5432/tnz', debug='False', repository='database')
