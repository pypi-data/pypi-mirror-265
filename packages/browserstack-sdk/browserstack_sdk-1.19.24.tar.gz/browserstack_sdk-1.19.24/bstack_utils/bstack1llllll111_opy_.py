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
from browserstack_sdk.bstack11llll1l1_opy_ import bstack1ll1ll11_opy_
from browserstack_sdk.bstack1l111l1lll_opy_ import RobotHandler
def bstack1llllll11_opy_(framework):
    if framework.lower() == bstack11l1l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᆀ"):
        return bstack1ll1ll11_opy_.version()
    elif framework.lower() == bstack11l1l11_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᆁ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11l1l11_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᆂ"):
        import behave
        return behave.__version__
    else:
        return bstack11l1l11_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫᆃ")