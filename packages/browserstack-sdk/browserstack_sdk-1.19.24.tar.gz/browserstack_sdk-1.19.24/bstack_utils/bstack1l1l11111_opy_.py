# coding: UTF-8
import sys
bstack1lllll1l_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1l1111_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack1l111_opy_
    bstack1_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1lll111_opy_ = bstack11lllll_opy_ [:-1]
    bstack1l1l11l_opy_ = bstack1_opy_ % len (bstack1lll111_opy_)
    bstack1llll1l_opy_ = bstack1lll111_opy_ [:bstack1l1l11l_opy_] + bstack1lll111_opy_ [bstack1l1l11l_opy_:]
    if bstack1lllll1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack1ll1l1_opy_ + bstack1_opy_) % bstack1l1111_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack1llll1l_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack1ll1l1_opy_ + bstack1_opy_) % bstack1l1111_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack1llll1l_opy_)])
    return eval (bstack11llll_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack1lllllll1l_opy_:
    def __init__(self):
        self._1111111ll1_opy_ = deque()
        self._1llllllllll_opy_ = {}
        self._111111ll1l_opy_ = False
    def bstack111111l111_opy_(self, test_name, bstack1111111l1l_opy_):
        bstack111111l1ll_opy_ = self._1llllllllll_opy_.get(test_name, {})
        return bstack111111l1ll_opy_.get(bstack1111111l1l_opy_, 0)
    def bstack11111111l1_opy_(self, test_name, bstack1111111l1l_opy_):
        bstack111111l11l_opy_ = self.bstack111111l111_opy_(test_name, bstack1111111l1l_opy_)
        self.bstack1111111l11_opy_(test_name, bstack1111111l1l_opy_)
        return bstack111111l11l_opy_
    def bstack1111111l11_opy_(self, test_name, bstack1111111l1l_opy_):
        if test_name not in self._1llllllllll_opy_:
            self._1llllllllll_opy_[test_name] = {}
        bstack111111l1ll_opy_ = self._1llllllllll_opy_[test_name]
        bstack111111l11l_opy_ = bstack111111l1ll_opy_.get(bstack1111111l1l_opy_, 0)
        bstack111111l1ll_opy_[bstack1111111l1l_opy_] = bstack111111l11l_opy_ + 1
    def bstack11ll1l1l1_opy_(self, bstack111111ll11_opy_, bstack111111l1l1_opy_):
        bstack1111111111_opy_ = self.bstack11111111l1_opy_(bstack111111ll11_opy_, bstack111111l1l1_opy_)
        bstack1111111lll_opy_ = bstack11l1l1l111_opy_[bstack111111l1l1_opy_]
        bstack111111111l_opy_ = bstack11l1l11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨᐤ").format(bstack111111ll11_opy_, bstack1111111lll_opy_, bstack1111111111_opy_)
        self._1111111ll1_opy_.append(bstack111111111l_opy_)
    def bstack11llll11_opy_(self):
        return len(self._1111111ll1_opy_) == 0
    def bstack11l1ll11_opy_(self):
        bstack11111111ll_opy_ = self._1111111ll1_opy_.popleft()
        return bstack11111111ll_opy_
    def capturing(self):
        return self._111111ll1l_opy_
    def bstack1lllll1111_opy_(self):
        self._111111ll1l_opy_ = True
    def bstack111l1ll11_opy_(self):
        self._111111ll1l_opy_ = False