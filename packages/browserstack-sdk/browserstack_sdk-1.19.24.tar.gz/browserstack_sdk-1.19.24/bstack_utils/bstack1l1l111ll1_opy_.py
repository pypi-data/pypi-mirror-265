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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111lll1ll1_opy_, bstack1llllll1ll_opy_, bstack1111lll1l_opy_, bstack1llll111l_opy_, \
    bstack11l11l1l11_opy_
def bstack1ll11111l_opy_(bstack1llll1ll111_opy_):
    for driver in bstack1llll1ll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l111l111_opy_(driver, status, reason=bstack11l1l11_opy_ (u"ࠫࠬᑿ")):
    bstack1ll1l11l1l_opy_ = Config.bstack1l1l1l1ll_opy_()
    if bstack1ll1l11l1l_opy_.bstack11lll111ll_opy_():
        return
    bstack1l11l1l11_opy_ = bstack111lll1ll_opy_(bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᒀ"), bstack11l1l11_opy_ (u"࠭ࠧᒁ"), status, reason, bstack11l1l11_opy_ (u"ࠧࠨᒂ"), bstack11l1l11_opy_ (u"ࠨࠩᒃ"))
    driver.execute_script(bstack1l11l1l11_opy_)
def bstack1ll1ll11l_opy_(page, status, reason=bstack11l1l11_opy_ (u"ࠩࠪᒄ")):
    try:
        if page is None:
            return
        bstack1ll1l11l1l_opy_ = Config.bstack1l1l1l1ll_opy_()
        if bstack1ll1l11l1l_opy_.bstack11lll111ll_opy_():
            return
        bstack1l11l1l11_opy_ = bstack111lll1ll_opy_(bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᒅ"), bstack11l1l11_opy_ (u"ࠫࠬᒆ"), status, reason, bstack11l1l11_opy_ (u"ࠬ࠭ᒇ"), bstack11l1l11_opy_ (u"࠭ࠧᒈ"))
        page.evaluate(bstack11l1l11_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᒉ"), bstack1l11l1l11_opy_)
    except Exception as e:
        print(bstack11l1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡿࢂࠨᒊ"), e)
def bstack111lll1ll_opy_(type, name, status, reason, bstack1llllll1l_opy_, bstack1ll1l11l_opy_):
    bstack1l111l11_opy_ = {
        bstack11l1l11_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩᒋ"): type,
        bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᒌ"): {}
    }
    if type == bstack11l1l11_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ᒍ"):
        bstack1l111l11_opy_[bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᒎ")][bstack11l1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᒏ")] = bstack1llllll1l_opy_
        bstack1l111l11_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᒐ")][bstack11l1l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᒑ")] = json.dumps(str(bstack1ll1l11l_opy_))
    if type == bstack11l1l11_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᒒ"):
        bstack1l111l11_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᒓ")][bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᒔ")] = name
    if type == bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᒕ"):
        bstack1l111l11_opy_[bstack11l1l11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᒖ")][bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᒗ")] = status
        if status == bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᒘ") and str(reason) != bstack11l1l11_opy_ (u"ࠤࠥᒙ"):
            bstack1l111l11_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᒚ")][bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫᒛ")] = json.dumps(str(reason))
    bstack1lll1ll1ll_opy_ = bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪᒜ").format(json.dumps(bstack1l111l11_opy_))
    return bstack1lll1ll1ll_opy_
def bstack1l1ll11lll_opy_(url, config, logger, bstack1ll1l111l1_opy_=False):
    hostname = bstack1llllll1ll_opy_(url)
    is_private = bstack1llll111l_opy_(hostname)
    try:
        if is_private or bstack1ll1l111l1_opy_:
            file_path = bstack111lll1ll1_opy_(bstack11l1l11_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᒝ"), bstack11l1l11_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ᒞ"), logger)
            if os.environ.get(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᒟ")) and eval(
                    os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᒠ"))):
                return
            if (bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᒡ") in config and not config[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᒢ")]):
                os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᒣ")] = str(True)
                bstack1llll1ll11l_opy_ = {bstack11l1l11_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨᒤ"): hostname}
                bstack11l11l1l11_opy_(bstack11l1l11_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ᒥ"), bstack11l1l11_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭ᒦ"), bstack1llll1ll11l_opy_, logger)
    except Exception as e:
        pass
def bstack1111l1l1l_opy_(caps, bstack1llll1l1lll_opy_):
    if bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᒧ") in caps:
        caps[bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᒨ")][bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪᒩ")] = True
        if bstack1llll1l1lll_opy_:
            caps[bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᒪ")][bstack11l1l11_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᒫ")] = bstack1llll1l1lll_opy_
    else:
        caps[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬᒬ")] = True
        if bstack1llll1l1lll_opy_:
            caps[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᒭ")] = bstack1llll1l1lll_opy_
def bstack1lllll1l1l1_opy_(bstack1l11l11l1l_opy_):
    bstack1llll1l1ll1_opy_ = bstack1111lll1l_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭ᒮ"), bstack11l1l11_opy_ (u"ࠪࠫᒯ"))
    if bstack1llll1l1ll1_opy_ == bstack11l1l11_opy_ (u"ࠫࠬᒰ") or bstack1llll1l1ll1_opy_ == bstack11l1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᒱ"):
        threading.current_thread().testStatus = bstack1l11l11l1l_opy_
    else:
        if bstack1l11l11l1l_opy_ == bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒲ"):
            threading.current_thread().testStatus = bstack1l11l11l1l_opy_