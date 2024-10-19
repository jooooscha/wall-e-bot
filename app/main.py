import json
import os, errno
from random import uniform, shuffle, choice
import itertools
import tempfile
from collections import defaultdict
import asyncio

import app.bot


def main():
    app.bot.start_bot()

if __name__ == "__main__":
    main()
