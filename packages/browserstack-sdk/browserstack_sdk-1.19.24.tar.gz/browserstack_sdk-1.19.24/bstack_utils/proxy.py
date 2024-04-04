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
from urllib.parse import urlparse
from bstack_utils.messages import bstack111l1111l1_opy_
def bstack1lllllllll1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lllllll1ll_opy_(bstack1llllllll1l_opy_, bstack1lllllll111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1llllllll1l_opy_):
        with open(bstack1llllllll1l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lllllllll1_opy_(bstack1llllllll1l_opy_):
        pac = get_pac(url=bstack1llllllll1l_opy_)
    else:
        raise Exception(bstack11l1l11_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬᐥ").format(bstack1llllllll1l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11l1l11_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢᐦ"), 80))
        bstack1lllllll1l1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lllllll1l1_opy_ = bstack11l1l11_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨᐧ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lllllll111_opy_, bstack1lllllll1l1_opy_)
    return proxy_url
def bstack1lll111l1_opy_(config):
    return bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᐨ") in config or bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᐩ") in config
def bstack1lll1l11ll_opy_(config):
    if not bstack1lll111l1_opy_(config):
        return
    if config.get(bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᐪ")):
        return config.get(bstack11l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᐫ"))
    if config.get(bstack11l1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᐬ")):
        return config.get(bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᐭ"))
def bstack1ll11l111_opy_(config, bstack1lllllll111_opy_):
    proxy = bstack1lll1l11ll_opy_(config)
    proxies = {}
    if config.get(bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᐮ")) or config.get(bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᐯ")):
        if proxy.endswith(bstack11l1l11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᐰ")):
            proxies = bstack1l1l1ll1_opy_(proxy, bstack1lllllll111_opy_)
        else:
            proxies = {
                bstack11l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᐱ"): proxy
            }
    return proxies
def bstack1l1l1ll1_opy_(bstack1llllllll1l_opy_, bstack1lllllll111_opy_):
    proxies = {}
    global bstack1lllllll11l_opy_
    if bstack11l1l11_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧᐲ") in globals():
        return bstack1lllllll11l_opy_
    try:
        proxy = bstack1lllllll1ll_opy_(bstack1llllllll1l_opy_, bstack1lllllll111_opy_)
        if bstack11l1l11_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧᐳ") in proxy:
            proxies = {}
        elif bstack11l1l11_opy_ (u"ࠨࡈࡕࡖࡓࠦᐴ") in proxy or bstack11l1l11_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨᐵ") in proxy or bstack11l1l11_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢᐶ") in proxy:
            bstack1llllllll11_opy_ = proxy.split(bstack11l1l11_opy_ (u"ࠤࠣࠦᐷ"))
            if bstack11l1l11_opy_ (u"ࠥ࠾࠴࠵ࠢᐸ") in bstack11l1l11_opy_ (u"ࠦࠧᐹ").join(bstack1llllllll11_opy_[1:]):
                proxies = {
                    bstack11l1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᐺ"): bstack11l1l11_opy_ (u"ࠨࠢᐻ").join(bstack1llllllll11_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᐼ"): str(bstack1llllllll11_opy_[0]).lower() + bstack11l1l11_opy_ (u"ࠣ࠼࠲࠳ࠧᐽ") + bstack11l1l11_opy_ (u"ࠤࠥᐾ").join(bstack1llllllll11_opy_[1:])
                }
        elif bstack11l1l11_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤᐿ") in proxy:
            bstack1llllllll11_opy_ = proxy.split(bstack11l1l11_opy_ (u"ࠦࠥࠨᑀ"))
            if bstack11l1l11_opy_ (u"ࠧࡀ࠯࠰ࠤᑁ") in bstack11l1l11_opy_ (u"ࠨࠢᑂ").join(bstack1llllllll11_opy_[1:]):
                proxies = {
                    bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᑃ"): bstack11l1l11_opy_ (u"ࠣࠤᑄ").join(bstack1llllllll11_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᑅ"): bstack11l1l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᑆ") + bstack11l1l11_opy_ (u"ࠦࠧᑇ").join(bstack1llllllll11_opy_[1:])
                }
        else:
            proxies = {
                bstack11l1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᑈ"): proxy
            }
    except Exception as e:
        print(bstack11l1l11_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥᑉ"), bstack111l1111l1_opy_.format(bstack1llllllll1l_opy_, str(e)))
    bstack1lllllll11l_opy_ = proxies
    return proxies