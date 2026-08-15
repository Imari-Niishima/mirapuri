#GNF.py
#これまで取得したミラプリスナップの点数ファイルから最新のものを取得する
#その内容を辞書構造で保持

import os
import datetime
import requests
import urllib
import re
import sys
from pathlib import Path
import pprint

#def get_new_file():
if __name__ == "__main__":

    p_temp = Path("scores")

    pprint.pprint(list(p_temp.iterdir()))