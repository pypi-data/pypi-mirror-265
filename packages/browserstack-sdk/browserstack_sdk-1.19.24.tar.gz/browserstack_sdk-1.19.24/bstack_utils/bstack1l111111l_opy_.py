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
import re
from bstack_utils.bstack1l1l111ll1_opy_ import bstack1lllll1l1l1_opy_
def bstack1llllll1111_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1l11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑊ")):
        return bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᑋ")
    elif fixture_name.startswith(bstack11l1l11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑌ")):
        return bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩᑍ")
    elif fixture_name.startswith(bstack11l1l11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑎ")):
        return bstack11l1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᑏ")
    elif fixture_name.startswith(bstack11l1l11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᑐ")):
        return bstack11l1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩᑑ")
def bstack1lllll1llll_opy_(fixture_name):
    return bool(re.match(bstack11l1l11_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡽ࡯ࡲࡨࡺࡲࡥࠪࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᑒ"), fixture_name))
def bstack1llllll1ll1_opy_(fixture_name):
    return bool(re.match(bstack11l1l11_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪᑓ"), fixture_name))
def bstack1llllll11l1_opy_(fixture_name):
    return bool(re.match(bstack11l1l11_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫࡟࠯ࠬࠪᑔ"), fixture_name))
def bstack1llllll1l1l_opy_(fixture_name):
    if fixture_name.startswith(bstack11l1l11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᑕ")):
        return bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᑖ"), bstack11l1l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᑗ")
    elif fixture_name.startswith(bstack11l1l11_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑘ")):
        return bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᑙ"), bstack11l1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ᑚ")
    elif fixture_name.startswith(bstack11l1l11_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᑛ")):
        return bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᑜ"), bstack11l1l11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᑝ")
    elif fixture_name.startswith(bstack11l1l11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑞ")):
        return bstack11l1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡰࡳࡩࡻ࡬ࡦࠩᑟ"), bstack11l1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫᑠ")
    return None, None
def bstack1lllll1ll1l_opy_(hook_name):
    if hook_name in [bstack11l1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᑡ"), bstack11l1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᑢ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lllll1l1ll_opy_(hook_name):
    if hook_name in [bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᑣ"), bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᑤ")]:
        return bstack11l1l11_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᑥ")
    elif hook_name in [bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᑦ"), bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ᑧ")]:
        return bstack11l1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ᑨ")
    elif hook_name in [bstack11l1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᑩ"), bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᑪ")]:
        return bstack11l1l11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᑫ")
    elif hook_name in [bstack11l1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨᑬ"), bstack11l1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᑭ")]:
        return bstack11l1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫᑮ")
    return hook_name
def bstack1llllll1l11_opy_(node, scenario):
    if hasattr(node, bstack11l1l11_opy_ (u"ࠩࡦࡥࡱࡲࡳࡱࡧࡦࠫᑯ")):
        parts = node.nodeid.rsplit(bstack11l1l11_opy_ (u"ࠥ࡟ࠧᑰ"))
        params = parts[-1]
        return bstack11l1l11_opy_ (u"ࠦࢀࢃࠠ࡜ࡽࢀࠦᑱ").format(scenario.name, params)
    return scenario.name
def bstack1llllll1lll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11l1l11_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᑲ")):
            examples = list(node.callspec.params[bstack11l1l11_opy_ (u"࠭࡟ࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡪࡾࡡ࡮ࡲ࡯ࡩࠬᑳ")].values())
        return examples
    except:
        return []
def bstack1lllll1ll11_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llllll11ll_opy_(report):
    try:
        status = bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᑴ")
        if report.passed or (report.failed and hasattr(report, bstack11l1l11_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᑵ"))):
            status = bstack11l1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᑶ")
        elif report.skipped:
            status = bstack11l1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᑷ")
        bstack1lllll1l1l1_opy_(status)
    except:
        pass
def bstack11l11111l_opy_(status):
    try:
        bstack1llllll111l_opy_ = bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᑸ")
        if status == bstack11l1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᑹ"):
            bstack1llllll111l_opy_ = bstack11l1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᑺ")
        elif status == bstack11l1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᑻ"):
            bstack1llllll111l_opy_ = bstack11l1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᑼ")
        bstack1lllll1l1l1_opy_(bstack1llllll111l_opy_)
    except:
        pass
def bstack1lllll1lll1_opy_(item=None, report=None, summary=None, extra=None):
    return