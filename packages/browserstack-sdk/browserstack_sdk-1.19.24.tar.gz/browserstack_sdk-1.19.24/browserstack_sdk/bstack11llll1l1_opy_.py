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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1111ll11_opy_ as bstack111lllll_opy_
from browserstack_sdk.bstack1l1l111ll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1l11111l_opy_
class bstack1ll1ll11_opy_:
    def __init__(self, args, logger, bstack11ll1ll1ll_opy_, bstack11lll111l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll1ll1ll_opy_ = bstack11ll1ll1ll_opy_
        self.bstack11lll111l1_opy_ = bstack11lll111l1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1ll11lll1_opy_ = []
        self.bstack11lll1111l_opy_ = None
        self.bstack1ll11lllll_opy_ = []
        self.bstack11ll1lllll_opy_ = self.bstack1ll1l11ll_opy_()
        self.bstack11l111l11_opy_ = -1
    def bstack1llll11l1_opy_(self, bstack11ll1l1lll_opy_):
        self.parse_args()
        self.bstack11ll1lll11_opy_()
        self.bstack11ll1ll11l_opy_(bstack11ll1l1lll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11lll11111_opy_():
        import importlib
        if getattr(importlib, bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡲ࡯ࡢࡦࡨࡶࠬฎ"), False):
            bstack11ll1l1ll1_opy_ = importlib.find_loader(bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪฏ"))
        else:
            bstack11ll1l1ll1_opy_ = importlib.util.find_spec(bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫฐ"))
    def bstack11ll1ll1l1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l111l11_opy_ = -1
        if bstack11l1l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪฑ") in self.bstack11ll1ll1ll_opy_:
            self.bstack11l111l11_opy_ = int(self.bstack11ll1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫฒ")])
        try:
            bstack11ll1llll1_opy_ = [bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧณ"), bstack11l1l11_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩด"), bstack11l1l11_opy_ (u"ࠧ࠮ࡲࠪต")]
            if self.bstack11l111l11_opy_ >= 0:
                bstack11ll1llll1_opy_.extend([bstack11l1l11_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩถ"), bstack11l1l11_opy_ (u"ࠩ࠰ࡲࠬท")])
            for arg in bstack11ll1llll1_opy_:
                self.bstack11ll1ll1l1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11ll1lll11_opy_(self):
        bstack11lll1111l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11lll1111l_opy_ = bstack11lll1111l_opy_
        return bstack11lll1111l_opy_
    def bstack1l1ll1l11l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11lll11111_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1l11111l_opy_)
    def bstack11ll1ll11l_opy_(self, bstack11ll1l1lll_opy_):
        bstack1ll1l11l1l_opy_ = Config.bstack1l1l1l1ll_opy_()
        if bstack11ll1l1lll_opy_:
            self.bstack11lll1111l_opy_.append(bstack11l1l11_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧธ"))
            self.bstack11lll1111l_opy_.append(bstack11l1l11_opy_ (u"࡙ࠫࡸࡵࡦࠩน"))
        if bstack1ll1l11l1l_opy_.bstack11lll111ll_opy_():
            self.bstack11lll1111l_opy_.append(bstack11l1l11_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫบ"))
            self.bstack11lll1111l_opy_.append(bstack11l1l11_opy_ (u"࠭ࡔࡳࡷࡨࠫป"))
        self.bstack11lll1111l_opy_.append(bstack11l1l11_opy_ (u"ࠧ࠮ࡲࠪผ"))
        self.bstack11lll1111l_opy_.append(bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭ฝ"))
        self.bstack11lll1111l_opy_.append(bstack11l1l11_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫพ"))
        self.bstack11lll1111l_opy_.append(bstack11l1l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪฟ"))
        if self.bstack11l111l11_opy_ > 1:
            self.bstack11lll1111l_opy_.append(bstack11l1l11_opy_ (u"ࠫ࠲ࡴࠧภ"))
            self.bstack11lll1111l_opy_.append(str(self.bstack11l111l11_opy_))
    def bstack11ll1ll111_opy_(self):
        bstack1ll11lllll_opy_ = []
        for spec in self.bstack1ll11lll1_opy_:
            bstack1l1lll1ll1_opy_ = [spec]
            bstack1l1lll1ll1_opy_ += self.bstack11lll1111l_opy_
            bstack1ll11lllll_opy_.append(bstack1l1lll1ll1_opy_)
        self.bstack1ll11lllll_opy_ = bstack1ll11lllll_opy_
        return bstack1ll11lllll_opy_
    def bstack1ll1l11ll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11ll1lllll_opy_ = True
            return True
        except Exception as e:
            self.bstack11ll1lllll_opy_ = False
        return self.bstack11ll1lllll_opy_
    def bstack1lll1l1lll_opy_(self, bstack11lll11l11_opy_, bstack1llll11l1_opy_):
        bstack1llll11l1_opy_[bstack11l1l11_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬม")] = self.bstack11ll1ll1ll_opy_
        multiprocessing.set_start_method(bstack11l1l11_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬย"))
        if bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪร") in self.bstack11ll1ll1ll_opy_:
            bstack111ll1lll_opy_ = []
            manager = multiprocessing.Manager()
            bstack1ll11ll111_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11ll1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫฤ")]):
                bstack111ll1lll_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack11lll11l11_opy_,
                                                           args=(self.bstack11lll1111l_opy_, bstack1llll11l1_opy_, bstack1ll11ll111_opy_)))
            i = 0
            bstack11ll1lll1l_opy_ = len(self.bstack11ll1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬล")])
            for t in bstack111ll1lll_opy_:
                os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪฦ")] = str(i)
                os.environ[bstack11l1l11_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬว")] = json.dumps(self.bstack11ll1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨศ")][i % bstack11ll1lll1l_opy_])
                i += 1
                t.start()
            for t in bstack111ll1lll_opy_:
                t.join()
            return list(bstack1ll11ll111_opy_)
    @staticmethod
    def bstack1l11llll1_opy_(driver, bstack1ll11lll11_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪษ"), None)
        if item and getattr(item, bstack11l1l11_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࠩส"), None) and not getattr(item, bstack11l1l11_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࡤࡪ࡯࡯ࡧࠪห"), False):
            logger.info(
                bstack11l1l11_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠣฬ"))
            bstack11lll11l1l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack111lllll_opy_.bstack1ll1l1llll_opy_(driver, bstack11lll11l1l_opy_, item.name, item.module.__name__, item.path, bstack1ll11lll11_opy_)
            item._a11y_stop_done = True
            if wait:
                sleep(2)