#!/usr/bin/env python3

import rethinkdb as r
import main
from pprint import pprint

if __name__ == "__main__":
    c = r.connect(*main.DB)
    pprint(r.db_drop('totp').run(c))
