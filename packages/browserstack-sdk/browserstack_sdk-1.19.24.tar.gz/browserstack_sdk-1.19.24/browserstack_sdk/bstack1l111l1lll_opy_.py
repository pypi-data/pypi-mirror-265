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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11ll1ll1ll_opy_, bstack11lll111l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll1ll1ll_opy_ = bstack11ll1ll1ll_opy_
        self.bstack11lll111l1_opy_ = bstack11lll111l1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l1111l1ll_opy_(bstack11ll1l1l1l_opy_):
        bstack11ll1l1l11_opy_ = []
        if bstack11ll1l1l1l_opy_:
            tokens = str(os.path.basename(bstack11ll1l1l1l_opy_)).split(bstack11l1l11_opy_ (u"ࠥࡣࠧอ"))
            camelcase_name = bstack11l1l11_opy_ (u"ࠦࠥࠨฮ").join(t.title() for t in tokens)
            suite_name, bstack11ll1l11ll_opy_ = os.path.splitext(camelcase_name)
            bstack11ll1l1l11_opy_.append(suite_name)
        return bstack11ll1l1l11_opy_
    @staticmethod
    def bstack11ll1l11l1_opy_(typename):
        if bstack11l1l11_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣฯ") in typename:
            return bstack11l1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢะ")
        return bstack11l1l11_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣั")