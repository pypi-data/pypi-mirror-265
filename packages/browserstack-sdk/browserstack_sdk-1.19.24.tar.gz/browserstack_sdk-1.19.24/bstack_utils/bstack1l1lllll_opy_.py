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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11ll111111_opy_, bstack1lll111111_opy_, get_host_info, bstack11l1lll1l1_opy_, bstack11l1llll1l_opy_, bstack111ll11ll1_opy_, \
    bstack11l11l1l1l_opy_, bstack111lllll11_opy_, bstack1llll11lll_opy_, bstack11l1111ll1_opy_, bstack1l1lllll1l_opy_, bstack1l11l11l11_opy_
from bstack_utils.bstack1lllll111ll_opy_ import bstack1lllll1l111_opy_
from bstack_utils.bstack11llll1111_opy_ import bstack11lll1l1ll_opy_
import bstack_utils.bstack1111ll11_opy_ as bstack111lllll_opy_
from bstack_utils.constants import bstack11l1l1l11l_opy_
bstack1lll1ll11l1_opy_ = [
    bstack11l1l11_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᓱ"), bstack11l1l11_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᓲ"), bstack11l1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᓳ"), bstack11l1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᓴ"),
    bstack11l1l11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᓵ"), bstack11l1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᓶ"), bstack11l1l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᓷ")
]
bstack1lll1ll11ll_opy_ = bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᓸ")
logger = logging.getLogger(__name__)
class bstack1l11ll1l11_opy_:
    bstack1lllll111ll_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def launch(cls, bs_config, bstack1lll1llll11_opy_):
        cls.bs_config = bs_config
        cls.bstack1lll1llllll_opy_()
        bstack11ll1l1111_opy_ = bstack11l1lll1l1_opy_(bs_config)
        bstack11ll11111l_opy_ = bstack11l1llll1l_opy_(bs_config)
        bstack1ll111l1ll_opy_ = False
        bstack11llllll_opy_ = False
        if bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࠫᓹ") in bs_config:
            bstack1ll111l1ll_opy_ = True
        else:
            bstack11llllll_opy_ = True
        bstack1ll1l1lll1_opy_ = {
            bstack11l1l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᓺ"): cls.bstack11111ll11_opy_() and cls.bstack1lll1lll1l1_opy_(bstack1lll1llll11_opy_.get(bstack11l1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪᓻ"), bstack11l1l11_opy_ (u"ࠪࠫᓼ"))),
            bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᓽ"): bstack111lllll_opy_.bstack1l11ll1l1_opy_(bs_config),
            bstack11l1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᓾ"): bs_config.get(bstack11l1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᓿ"), False),
            bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᔀ"): bstack11llllll_opy_,
            bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᔁ"): bstack1ll111l1ll_opy_
        }
        data = {
            bstack11l1l11_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩᔂ"): bstack11l1l11_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨᔃ"),
            bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧࠪᔄ"): bs_config.get(bstack11l1l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᔅ"), bstack11l1l11_opy_ (u"࠭ࠧᔆ")),
            bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᔇ"): bs_config.get(bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᔈ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᔉ"): bs_config.get(bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᔊ")),
            bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᔋ"): bs_config.get(bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᔌ"), bstack11l1l11_opy_ (u"࠭ࠧᔍ")),
            bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹࡥࡴࡪ࡯ࡨࠫᔎ"): datetime.datetime.now().isoformat(),
            bstack11l1l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᔏ"): bstack111ll11ll1_opy_(bs_config),
            bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬᔐ"): get_host_info(),
            bstack11l1l11_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫᔑ"): bstack1lll111111_opy_(),
            bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᔒ"): os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫᔓ")),
            bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫᔔ"): os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬᔕ"), False),
            bstack11l1l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪᔖ"): bstack11ll111111_opy_(),
            bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧᔗ"): bstack1ll1l1lll1_opy_,
            bstack11l1l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡢࡺࡪࡸࡳࡪࡱࡱࠫᔘ"): {
                bstack11l1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᔙ"): bstack1lll1llll11_opy_.get(bstack11l1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ᔚ"), bstack11l1l11_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᔛ")),
                bstack11l1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᔜ"): bstack1lll1llll11_opy_.get(bstack11l1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᔝ")),
                bstack11l1l11_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᔞ"): bstack1lll1llll11_opy_.get(bstack11l1l11_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᔟ"))
            }
        }
        config = {
            bstack11l1l11_opy_ (u"ࠫࡦࡻࡴࡩࠩᔠ"): (bstack11ll1l1111_opy_, bstack11ll11111l_opy_),
            bstack11l1l11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᔡ"): cls.default_headers()
        }
        response = bstack1llll11lll_opy_(bstack11l1l11_opy_ (u"࠭ࡐࡐࡕࡗࠫᔢ"), cls.request_url(bstack11l1l11_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹࠧᔣ")), data, config)
        if response.status_code != 200:
            os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᔤ")] = bstack11l1l11_opy_ (u"ࠩࡱࡹࡱࡲࠧᔥ")
            os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᔦ")] = bstack11l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᔧ")
            os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᔨ")] = bstack11l1l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᔩ")
            os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᔪ")] = bstack11l1l11_opy_ (u"ࠣࡰࡸࡰࡱࠨᔫ")
            os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᔬ")] = bstack11l1l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᔭ")
            bstack1llll1111l1_opy_ = response.json()
            if bstack1llll1111l1_opy_ and bstack1llll1111l1_opy_[bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᔮ")]:
                error_message = bstack1llll1111l1_opy_[bstack11l1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᔯ")]
                if bstack1llll1111l1_opy_[bstack11l1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᔰ")] == bstack11l1l11_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡉࡏࡘࡄࡐࡎࡊ࡟ࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࠬᔱ"):
                    logger.error(error_message)
                elif bstack1llll1111l1_opy_[bstack11l1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᔲ")] == bstack11l1l11_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠨᔳ"):
                    logger.info(error_message)
                elif bstack1llll1111l1_opy_[bstack11l1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ᔴ")] == bstack11l1l11_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡗࡉࡑ࡟ࡅࡇࡓࡖࡊࡉࡁࡕࡇࡇࠫᔵ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11l1l11_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡚ࠥࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᔶ"))
            return [None, None, None]
        bstack1llll1111l1_opy_ = response.json()
        os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᔷ")] = bstack1llll1111l1_opy_[bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᔸ")]
        if cls.bstack11111ll11_opy_() is True and cls.bstack1lll1lll1l1_opy_(bstack1lll1llll11_opy_.get(bstack11l1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩᔹ"), bstack11l1l11_opy_ (u"ࠩࠪᔺ"))):
            logger.debug(bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧᔻ"))
            os.environ[bstack11l1l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪᔼ")] = bstack11l1l11_opy_ (u"ࠬࡺࡲࡶࡧࠪᔽ")
            if bstack1llll1111l1_opy_.get(bstack11l1l11_opy_ (u"࠭ࡪࡸࡶࠪᔾ")):
                os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᔿ")] = bstack1llll1111l1_opy_[bstack11l1l11_opy_ (u"ࠨ࡬ࡺࡸࠬᕀ")]
                os.environ[bstack11l1l11_opy_ (u"ࠩࡆࡖࡊࡊࡅࡏࡖࡌࡅࡑ࡙࡟ࡇࡑࡕࡣࡈࡘࡁࡔࡊࡢࡖࡊࡖࡏࡓࡖࡌࡒࡌ࠭ᕁ")] = json.dumps({
                    bstack11l1l11_opy_ (u"ࠪࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬᕂ"): bstack11ll1l1111_opy_,
                    bstack11l1l11_opy_ (u"ࠫࡵࡧࡳࡴࡹࡲࡶࡩ࠭ᕃ"): bstack11ll11111l_opy_
                })
            if bstack1llll1111l1_opy_.get(bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᕄ")):
                os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᕅ")] = bstack1llll1111l1_opy_[bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᕆ")]
            if bstack1llll1111l1_opy_.get(bstack11l1l11_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᕇ")):
                os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᕈ")] = str(bstack1llll1111l1_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᕉ")])
        return [bstack1llll1111l1_opy_[bstack11l1l11_opy_ (u"ࠫ࡯ࡽࡴࠨᕊ")], bstack1llll1111l1_opy_[bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᕋ")], bstack1llll1111l1_opy_[bstack11l1l11_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᕌ")]]
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᕍ")] == bstack11l1l11_opy_ (u"ࠣࡰࡸࡰࡱࠨᕎ") or os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᕏ")] == bstack11l1l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᕐ"):
            print(bstack11l1l11_opy_ (u"ࠫࡊ࡞ࡃࡆࡒࡗࡍࡔࡔࠠࡊࡐࠣࡷࡹࡵࡰࡃࡷ࡬ࡰࡩ࡛ࡰࡴࡶࡵࡩࡦࡳࠠࡓࡇࡔ࡙ࡊ࡙ࡔࠡࡖࡒࠤ࡙ࡋࡓࡕࠢࡒࡆࡘࡋࡒࡗࡃࡅࡍࡑࡏࡔ࡚ࠢ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬᕑ"))
            return {
                bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᕒ"): bstack11l1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᕓ"),
                bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᕔ"): bstack11l1l11_opy_ (u"ࠨࡖࡲ࡯ࡪࡴ࠯ࡣࡷ࡬ࡰࡩࡏࡄࠡ࡫ࡶࠤࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠬࠡࡤࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡰ࡭࡬࡮ࡴࠡࡪࡤࡺࡪࠦࡦࡢ࡫࡯ࡩࡩ࠭ᕕ")
            }
        else:
            cls.bstack1lllll111ll_opy_.shutdown()
            data = {
                bstack11l1l11_opy_ (u"ࠩࡶࡸࡴࡶ࡟ࡵ࡫ࡰࡩࠬᕖ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack11l1l11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᕗ"): cls.default_headers()
            }
            bstack11l11l111l_opy_ = bstack11l1l11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡶࡲࡴࠬᕘ").format(os.environ[bstack11l1l11_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠦᕙ")])
            bstack1lll1ll1lll_opy_ = cls.request_url(bstack11l11l111l_opy_)
            response = bstack1llll11lll_opy_(bstack11l1l11_opy_ (u"࠭ࡐࡖࡖࠪᕚ"), bstack1lll1ll1lll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l1l11_opy_ (u"ࠢࡔࡶࡲࡴࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡮ࡰࡶࠣࡳࡰࠨᕛ"))
    @classmethod
    def bstack1l11111l11_opy_(cls):
        if cls.bstack1lllll111ll_opy_ is None:
            return
        cls.bstack1lllll111ll_opy_.shutdown()
    @classmethod
    def bstack1l11llll11_opy_(cls):
        if cls.on():
            print(
                bstack11l1l11_opy_ (u"ࠨࡘ࡬ࡷ࡮ࡺࠠࡩࡶࡷࡴࡸࡀ࠯࠰ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠠࡵࡱࠣࡺ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡳࡳࡷࡺࠬࠡ࡫ࡱࡷ࡮࡭ࡨࡵࡵ࠯ࠤࡦࡴࡤࠡ࡯ࡤࡲࡾࠦ࡭ࡰࡴࡨࠤࡩ࡫ࡢࡶࡩࡪ࡭ࡳ࡭ࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧ࡬࡭ࠢࡤࡸࠥࡵ࡮ࡦࠢࡳࡰࡦࡩࡥࠢ࡞ࡱࠫᕜ").format(os.environ[bstack11l1l11_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠣᕝ")]))
    @classmethod
    def bstack1lll1llllll_opy_(cls):
        if cls.bstack1lllll111ll_opy_ is not None:
            return
        cls.bstack1lllll111ll_opy_ = bstack1lllll1l111_opy_(cls.bstack1lll1lllll1_opy_)
        cls.bstack1lllll111ll_opy_.start()
    @classmethod
    def bstack1l111l11ll_opy_(cls, bstack11lllll1l1_opy_, bstack1lll1llll1l_opy_=bstack11l1l11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᕞ")):
        if not cls.on():
            return
        bstack111l111l1_opy_ = bstack11lllll1l1_opy_[bstack11l1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᕟ")]
        bstack1lll1l1llll_opy_ = {
            bstack11l1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᕠ"): bstack11l1l11_opy_ (u"࠭ࡔࡦࡵࡷࡣࡘࡺࡡࡳࡶࡢ࡙ࡵࡲ࡯ࡢࡦࠪᕡ"),
            bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᕢ"): bstack11l1l11_opy_ (u"ࠨࡖࡨࡷࡹࡥࡅ࡯ࡦࡢ࡙ࡵࡲ࡯ࡢࡦࠪᕣ"),
            bstack11l1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᕤ"): bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࡠࡕ࡮࡭ࡵࡶࡥࡥࡡࡘࡴࡱࡵࡡࡥࠩᕥ"),
            bstack11l1l11_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᕦ"): bstack11l1l11_opy_ (u"ࠬࡒ࡯ࡨࡡࡘࡴࡱࡵࡡࡥࠩᕧ"),
            bstack11l1l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᕨ"): bstack11l1l11_opy_ (u"ࠧࡉࡱࡲ࡯ࡤ࡙ࡴࡢࡴࡷࡣ࡚ࡶ࡬ࡰࡣࡧࠫᕩ"),
            bstack11l1l11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᕪ"): bstack11l1l11_opy_ (u"ࠩࡋࡳࡴࡱ࡟ࡆࡰࡧࡣ࡚ࡶ࡬ࡰࡣࡧࠫᕫ"),
            bstack11l1l11_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᕬ"): bstack11l1l11_opy_ (u"ࠫࡈࡈࡔࡠࡗࡳࡰࡴࡧࡤࠨᕭ")
        }.get(bstack111l111l1_opy_)
        if bstack1lll1llll1l_opy_ == bstack11l1l11_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫᕮ"):
            cls.bstack1lll1llllll_opy_()
            cls.bstack1lllll111ll_opy_.add(bstack11lllll1l1_opy_)
        elif bstack1lll1llll1l_opy_ == bstack11l1l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᕯ"):
            cls.bstack1lll1lllll1_opy_([bstack11lllll1l1_opy_], bstack1lll1llll1l_opy_)
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1lll1lllll1_opy_(cls, bstack11lllll1l1_opy_, bstack1lll1llll1l_opy_=bstack11l1l11_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᕰ")):
        config = {
            bstack11l1l11_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᕱ"): cls.default_headers()
        }
        response = bstack1llll11lll_opy_(bstack11l1l11_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᕲ"), cls.request_url(bstack1lll1llll1l_opy_), bstack11lllll1l1_opy_, config)
        bstack11ll11l11l_opy_ = response.json()
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1ll1l1l11l_opy_(cls, bstack11llllll1l_opy_):
        bstack1lll1lll111_opy_ = []
        for log in bstack11llllll1l_opy_:
            bstack1lll1ll111l_opy_ = {
                bstack11l1l11_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᕳ"): bstack11l1l11_opy_ (u"࡙ࠫࡋࡓࡕࡡࡏࡓࡌ࠭ᕴ"),
                bstack11l1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᕵ"): log[bstack11l1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᕶ")],
                bstack11l1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᕷ"): log[bstack11l1l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᕸ")],
                bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶ࡟ࡳࡧࡶࡴࡴࡴࡳࡦࠩᕹ"): {},
                bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᕺ"): log[bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᕻ")],
            }
            if bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᕼ") in log:
                bstack1lll1ll111l_opy_[bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᕽ")] = log[bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᕾ")]
            elif bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᕿ") in log:
                bstack1lll1ll111l_opy_[bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖀ")] = log[bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖁ")]
            bstack1lll1lll111_opy_.append(bstack1lll1ll111l_opy_)
        cls.bstack1l111l11ll_opy_({
            bstack11l1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᖂ"): bstack11l1l11_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᖃ"),
            bstack11l1l11_opy_ (u"࠭࡬ࡰࡩࡶࠫᖄ"): bstack1lll1lll111_opy_
        })
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1lll1ll1l11_opy_(cls, steps):
        bstack1lll1ll1111_opy_ = []
        for step in steps:
            bstack1lll1ll1ll1_opy_ = {
                bstack11l1l11_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᖅ"): bstack11l1l11_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡕࡇࡓࠫᖆ"),
                bstack11l1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᖇ"): step[bstack11l1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᖈ")],
                bstack11l1l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᖉ"): step[bstack11l1l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᖊ")],
                bstack11l1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᖋ"): step[bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᖌ")],
                bstack11l1l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᖍ"): step[bstack11l1l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᖎ")]
            }
            if bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖏ") in step:
                bstack1lll1ll1ll1_opy_[bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖐ")] = step[bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖑ")]
            elif bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖒ") in step:
                bstack1lll1ll1ll1_opy_[bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᖓ")] = step[bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖔ")]
            bstack1lll1ll1111_opy_.append(bstack1lll1ll1ll1_opy_)
        cls.bstack1l111l11ll_opy_({
            bstack11l1l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᖕ"): bstack11l1l11_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᖖ"),
            bstack11l1l11_opy_ (u"ࠫࡱࡵࡧࡴࠩᖗ"): bstack1lll1ll1111_opy_
        })
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1lll1111l1_opy_(cls, screenshot):
        cls.bstack1l111l11ll_opy_({
            bstack11l1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᖘ"): bstack11l1l11_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᖙ"),
            bstack11l1l11_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᖚ"): [{
                bstack11l1l11_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ᖛ"): bstack11l1l11_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠫᖜ"),
                bstack11l1l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᖝ"): datetime.datetime.utcnow().isoformat() + bstack11l1l11_opy_ (u"ࠫ࡟࠭ᖞ"),
                bstack11l1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖟ"): screenshot[bstack11l1l11_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬᖠ")],
                bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᖡ"): screenshot[bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖢ")]
            }]
        }, bstack1lll1llll1l_opy_=bstack11l1l11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᖣ"))
    @classmethod
    @bstack1l11l11l11_opy_(class_method=True)
    def bstack1ll111l1l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l111l11ll_opy_({
            bstack11l1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᖤ"): bstack11l1l11_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨᖥ"),
            bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᖦ"): {
                bstack11l1l11_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᖧ"): cls.current_test_uuid(),
                bstack11l1l11_opy_ (u"ࠢࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸࠨᖨ"): cls.bstack11llll1l11_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack11l1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᖩ"), None) is None or os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᖪ")] == bstack11l1l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᖫ"):
            return False
        return True
    @classmethod
    def bstack11111ll11_opy_(cls):
        return bstack1l1lllll1l_opy_(cls.bs_config.get(bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᖬ"), False))
    @classmethod
    def bstack1lll1lll1l1_opy_(cls, framework):
        return framework in bstack11l1l1l11l_opy_
    @staticmethod
    def request_url(url):
        return bstack11l1l11_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫᖭ").format(bstack1lll1ll11ll_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack11l1l11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᖮ"): bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᖯ"),
            bstack11l1l11_opy_ (u"ࠨ࡚࠰ࡆࡘ࡚ࡁࡄࡍ࠰ࡘࡊ࡙ࡔࡐࡒࡖࠫᖰ"): bstack11l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᖱ")
        }
        if os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᖲ"), None):
            headers[bstack11l1l11_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫᖳ")] = bstack11l1l11_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨᖴ").format(os.environ[bstack11l1l11_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠢᖵ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᖶ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᖷ"), None)
    @staticmethod
    def bstack11lll1l1l1_opy_():
        if getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᖸ"), None):
            return {
                bstack11l1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨᖹ"): bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᖺ"),
                bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖻ"): getattr(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᖼ"), None)
            }
        if getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᖽ"), None):
            return {
                bstack11l1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᖾ"): bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᖿ"),
                bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᗀ"): getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᗁ"), None)
            }
        return None
    @staticmethod
    def bstack11llll1l11_opy_(driver):
        return {
            bstack111lllll11_opy_(): bstack11l11l1l1l_opy_(driver)
        }
    @staticmethod
    def bstack1lll1ll1l1l_opy_(exception_info, report):
        return [{bstack11l1l11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᗂ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11ll1l11l1_opy_(typename):
        if bstack11l1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᗃ") in typename:
            return bstack11l1l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᗄ")
        return bstack11l1l11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᗅ")
    @staticmethod
    def bstack1llll11111l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11ll1l11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l1111l1ll_opy_(test, hook_name=None):
        bstack1lll1lll11l_opy_ = test.parent
        if hook_name in [bstack11l1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᗆ"), bstack11l1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᗇ"), bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪᗈ"), bstack11l1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᗉ")]:
            bstack1lll1lll11l_opy_ = test
        scope = []
        while bstack1lll1lll11l_opy_ is not None:
            scope.append(bstack1lll1lll11l_opy_.name)
            bstack1lll1lll11l_opy_ = bstack1lll1lll11l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1llll111111_opy_(hook_type):
        if hook_type == bstack11l1l11_opy_ (u"ࠨࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠦᗊ"):
            return bstack11l1l11_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡨࡰࡱ࡮ࠦᗋ")
        elif hook_type == bstack11l1l11_opy_ (u"ࠣࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠧᗌ"):
            return bstack11l1l11_opy_ (u"ࠤࡗࡩࡦࡸࡤࡰࡹࡱࠤ࡭ࡵ࡯࡬ࠤᗍ")
    @staticmethod
    def bstack1lll1lll1ll_opy_(bstack1ll11lll1_opy_):
        try:
            if not bstack1l11ll1l11_opy_.on():
                return bstack1ll11lll1_opy_
            if os.environ.get(bstack11l1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠣᗎ"), None) == bstack11l1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᗏ"):
                tests = os.environ.get(bstack11l1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠤᗐ"), None)
                if tests is None or tests == bstack11l1l11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᗑ"):
                    return bstack1ll11lll1_opy_
                bstack1ll11lll1_opy_ = tests.split(bstack11l1l11_opy_ (u"ࠧ࠭ࠩᗒ"))
                return bstack1ll11lll1_opy_
        except Exception as exc:
            print(bstack11l1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡳࡧࡵࡹࡳࠦࡨࡢࡰࡧࡰࡪࡸ࠺ࠡࠤᗓ"), str(exc))
        return bstack1ll11lll1_opy_
    @classmethod
    def bstack1l1111ll1l_opy_(cls, event: str, bstack11lllll1l1_opy_: bstack11lll1l1ll_opy_):
        bstack11llllll11_opy_ = {
            bstack11l1l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᗔ"): event,
            bstack11lllll1l1_opy_.bstack11lll11ll1_opy_(): bstack11lllll1l1_opy_.bstack11llll1lll_opy_(event)
        }
        bstack1l11ll1l11_opy_.bstack1l111l11ll_opy_(bstack11llllll11_opy_)