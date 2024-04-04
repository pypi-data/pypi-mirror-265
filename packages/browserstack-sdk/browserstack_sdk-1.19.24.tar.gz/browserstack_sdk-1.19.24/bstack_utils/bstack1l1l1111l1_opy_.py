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
class bstack1l1l111l11_opy_:
    def __init__(self, handler):
        self._1llll1lll1l_opy_ = None
        self.handler = handler
        self._1llll1ll1ll_opy_ = self.bstack1llll1lll11_opy_()
        self.patch()
    def patch(self):
        self._1llll1lll1l_opy_ = self._1llll1ll1ll_opy_.execute
        self._1llll1ll1ll_opy_.execute = self.bstack1llll1ll1l1_opy_()
    def bstack1llll1ll1l1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11l1l11_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࠤᑽ"), driver_command, None, this, args)
            response = self._1llll1lll1l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11l1l11_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࠤᑾ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llll1ll1ll_opy_.execute = self._1llll1lll1l_opy_
    @staticmethod
    def bstack1llll1lll11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver