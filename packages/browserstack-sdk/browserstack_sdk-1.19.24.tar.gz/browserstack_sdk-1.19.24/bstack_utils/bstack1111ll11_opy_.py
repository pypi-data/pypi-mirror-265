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
import json
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack11ll1111ll_opy_ as bstack11ll11lll1_opy_
from bstack_utils.bstack1l1ll111ll_opy_ import bstack1l1ll111ll_opy_
from bstack_utils.helper import bstack1l1lll111_opy_, bstack1l111ll11_opy_, bstack11l1lll1l1_opy_, bstack11l1llll1l_opy_, bstack1lll111111_opy_, get_host_info, bstack11ll111111_opy_, bstack1llll11lll_opy_, bstack1l11l11l11_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l11l11l11_opy_(class_method=False)
def _11l1lll11l_opy_(driver, bstack1ll11lll11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11l1l11_opy_ (u"ࠨࡱࡶࡣࡳࡧ࡭ࡦࠩา"): caps.get(bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨำ"), None),
        bstack11l1l11_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧิ"): bstack1ll11lll11_opy_.get(bstack11l1l11_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧี"), None),
        bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫึ"): caps.get(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫื"), None),
        bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ุࠩ"): caps.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ูࠩ"), None)
    }
  except Exception as error:
    logger.debug(bstack11l1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ฺࠥ࠭") + str(error))
  return response
def bstack1l11ll1l1_opy_(config):
  return config.get(bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ฻"), False) or any([p.get(bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ฼"), False) == True for p in config.get(bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ฽"), [])])
def bstack11l11l1l1_opy_(config, bstack1111lll1_opy_):
  try:
    if not bstack1l111ll11_opy_(config):
      return False
    bstack11l1ll1lll_opy_ = config.get(bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭฾"), False)
    bstack11l1llllll_opy_ = config[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ฿")][bstack1111lll1_opy_].get(bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨเ"), None)
    if bstack11l1llllll_opy_ != None:
      bstack11l1ll1lll_opy_ = bstack11l1llllll_opy_
    bstack11ll11ll11_opy_ = os.getenv(bstack11l1l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧแ")) is not None and len(os.getenv(bstack11l1l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨโ"))) > 0 and os.getenv(bstack11l1l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩใ")) != bstack11l1l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪไ")
    return bstack11l1ll1lll_opy_ and bstack11ll11ll11_opy_
  except Exception as error:
    logger.debug(bstack11l1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ๅ") + str(error))
  return False
def bstack1l1llll11_opy_(bstack11ll11l111_opy_, test_tags):
  bstack11ll11l111_opy_ = os.getenv(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨๆ"))
  if bstack11ll11l111_opy_ is None:
    return True
  bstack11ll11l111_opy_ = json.loads(bstack11ll11l111_opy_)
  try:
    include_tags = bstack11ll11l111_opy_[bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭็")] if bstack11l1l11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫่ࠧ") in bstack11ll11l111_opy_ and isinstance(bstack11ll11l111_opy_[bstack11l1l11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ้")], list) else []
    exclude_tags = bstack11ll11l111_opy_[bstack11l1l11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦ๊ࠩ")] if bstack11l1l11_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧ๋ࠪ") in bstack11ll11l111_opy_ and isinstance(bstack11ll11l111_opy_[bstack11l1l11_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ์")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢํ") + str(error))
  return False
def bstack1llll11l11_opy_(config, bstack11l1lll111_opy_, bstack11ll1111l1_opy_, bstack11l1llll11_opy_):
  bstack11ll1l1111_opy_ = bstack11l1lll1l1_opy_(config)
  bstack11ll11111l_opy_ = bstack11l1llll1l_opy_(config)
  if bstack11ll1l1111_opy_ is None or bstack11ll11111l_opy_ is None:
    logger.error(bstack11l1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩ๎"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ๏"), bstack11l1l11_opy_ (u"ࠪࡿࢂ࠭๐")))
    data = {
        bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ๑"): config[bstack11l1l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ๒")],
        bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ๓"): config.get(bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ๔"), os.path.basename(os.getcwd())),
        bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨࠫ๕"): bstack1l1lll111_opy_(),
        bstack11l1l11_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ๖"): config.get(bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭๗"), bstack11l1l11_opy_ (u"ࠫࠬ๘")),
        bstack11l1l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ๙"): {
            bstack11l1l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭๚"): bstack11l1lll111_opy_,
            bstack11l1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ๛"): bstack11ll1111l1_opy_,
            bstack11l1l11_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ๜"): __version__,
            bstack11l1l11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ๝"): bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ๞"),
            bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ๟"): bstack11l1l11_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ๠"),
            bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭๡"): bstack11l1llll11_opy_
        },
        bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ๢"): settings,
        bstack11l1l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩ๣"): bstack11ll111111_opy_(),
        bstack11l1l11_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩ๤"): bstack1lll111111_opy_(),
        bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬ๥"): get_host_info(),
        bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭๦"): bstack1l111ll11_opy_(config)
    }
    headers = {
        bstack11l1l11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ๧"): bstack11l1l11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ๨"),
    }
    config = {
        bstack11l1l11_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ๩"): (bstack11ll1l1111_opy_, bstack11ll11111l_opy_),
        bstack11l1l11_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ๪"): headers
    }
    response = bstack1llll11lll_opy_(bstack11l1l11_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ๫"), bstack11ll11lll1_opy_ + bstack11l1l11_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵࠪ๬"), data, config)
    bstack11ll11l11l_opy_ = response.json()
    if bstack11ll11l11l_opy_[bstack11l1l11_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ๭")]:
      parsed = json.loads(os.getenv(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭๮"), bstack11l1l11_opy_ (u"࠭ࡻࡾࠩ๯")))
      parsed[bstack11l1l11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ๰")] = bstack11ll11l11l_opy_[bstack11l1l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭๱")][bstack11l1l11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ๲")]
      os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ๳")] = json.dumps(parsed)
      bstack1l1ll111ll_opy_.bstack11ll11l1l1_opy_(bstack11ll11l11l_opy_[bstack11l1l11_opy_ (u"ࠫࡩࡧࡴࡢࠩ๴")][bstack11l1l11_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭๵")])
      bstack1l1ll111ll_opy_.bstack11l1ll1ll1_opy_(bstack11ll11l11l_opy_[bstack11l1l11_opy_ (u"࠭ࡤࡢࡶࡤࠫ๶")][bstack11l1l11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ๷")])
      bstack1l1ll111ll_opy_.store()
      return bstack11ll11l11l_opy_[bstack11l1l11_opy_ (u"ࠨࡦࡤࡸࡦ࠭๸")][bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ๹")], bstack11ll11l11l_opy_[bstack11l1l11_opy_ (u"ࠪࡨࡦࡺࡡࠨ๺")][bstack11l1l11_opy_ (u"ࠫ࡮ࡪࠧ๻")]
    else:
      logger.error(bstack11l1l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭๼") + bstack11ll11l11l_opy_[bstack11l1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ๽")])
      if bstack11ll11l11l_opy_[bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ๾")] == bstack11l1l11_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪ๿"):
        for bstack11ll11llll_opy_ in bstack11ll11l11l_opy_[bstack11l1l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ຀")]:
          logger.error(bstack11ll11llll_opy_[bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫກ")])
      return None, None
  except Exception as error:
    logger.error(bstack11l1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧຂ") +  str(error))
    return None, None
def bstack11l11l111_opy_():
  if os.getenv(bstack11l1l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ຃")) is None:
    return {
        bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ຄ"): bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭຅"),
        bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩຆ"): bstack11l1l11_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨງ")
    }
  data = {bstack11l1l11_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫຈ"): bstack1l1lll111_opy_()}
  headers = {
      bstack11l1l11_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫຉ"): bstack11l1l11_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭ຊ") + os.getenv(bstack11l1l11_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦ຋")),
      bstack11l1l11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ຌ"): bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫຍ")
  }
  response = bstack1llll11lll_opy_(bstack11l1l11_opy_ (u"ࠩࡓ࡙࡙࠭ຎ"), bstack11ll11lll1_opy_ + bstack11l1l11_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬຏ"), data, { bstack11l1l11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬຐ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11l1l11_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨຑ") + datetime.utcnow().isoformat() + bstack11l1l11_opy_ (u"࡚࠭ࠨຒ"))
      return {bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧຓ"): bstack11l1l11_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩດ"), bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪຕ"): bstack11l1l11_opy_ (u"ࠪࠫຖ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11l1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢທ") + str(error))
    return {
        bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬຘ"): bstack11l1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬນ"),
        bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨບ"): str(error)
    }
def bstack11111ll1_opy_(caps, options):
  try:
    bstack11ll111ll1_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩປ"), {}).get(bstack11l1l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ຜ"), caps.get(bstack11l1l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪຝ"), bstack11l1l11_opy_ (u"ࠫࠬພ")))
    if bstack11ll111ll1_opy_:
      logger.warn(bstack11l1l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤຟ"))
      return False
    browser = caps.get(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫຠ"), bstack11l1l11_opy_ (u"ࠧࠨມ")).lower()
    if browser != bstack11l1l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨຢ"):
      logger.warn(bstack11l1l11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧຣ"))
      return False
    browser_version = caps.get(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ຤"), caps.get(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ລ")))
    if browser_version and browser_version != bstack11l1l11_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬ຦") and int(browser_version.split(bstack11l1l11_opy_ (u"࠭࠮ࠨວ"))[0]) <= 94:
      logger.warn(bstack11l1l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠷࠲ࠧຨ"))
      return False
    if not options is None:
      bstack11ll11ll1l_opy_ = options.to_capabilities().get(bstack11l1l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ຩ"), {})
      if bstack11l1l11_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ສ") in bstack11ll11ll1l_opy_.get(bstack11l1l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨຫ"), []):
        logger.warn(bstack11l1l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨຬ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢອ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11ll111lll_opy_ = config.get(bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ຮ"), {})
    bstack11ll111lll_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪຯ")] = os.getenv(bstack11l1l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ະ"))
    bstack11l1lllll1_opy_ = json.loads(os.getenv(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪັ"), bstack11l1l11_opy_ (u"ࠪࡿࢂ࠭າ"))).get(bstack11l1l11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬຳ"))
    caps[bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬິ")] = True
    if bstack11l1l11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧີ") in caps:
      caps[bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨຶ")][bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨື")] = bstack11ll111lll_opy_
      caps[bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵຸࠪ")][bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵູࠪ")][bstack11l1l11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ຺ࠬ")] = bstack11l1lllll1_opy_
    else:
      caps[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫົ")] = bstack11ll111lll_opy_
      caps[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬຼ")][bstack11l1l11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨຽ")] = bstack11l1lllll1_opy_
  except Exception as error:
    logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤ຾") +  str(error))
def bstack11l1ll1ll_opy_(driver, bstack11ll111l11_opy_):
  try:
    setattr(driver, bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ຿"), True)
    session = driver.session_id
    if session:
      bstack11ll111l1l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll111l1l_opy_ = False
      bstack11ll111l1l_opy_ = url.scheme in [bstack11l1l11_opy_ (u"ࠥ࡬ࡹࡺࡰࠣເ"), bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥແ")]
      if bstack11ll111l1l_opy_:
        if bstack11ll111l11_opy_:
          logger.info(bstack11l1l11_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧໂ"))
      return bstack11ll111l11_opy_
  except Exception as e:
    logger.error(bstack11l1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤໃ") + str(e))
    return False
def bstack1ll1l1llll_opy_(driver, class_name, name, module_name, path, bstack1ll11lll11_opy_):
  try:
    bstack11lll11l1l_opy_ = [class_name] if not class_name is None else []
    bstack11ll1l111l_opy_ = {
        bstack11l1l11_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧໄ"): True,
        bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡊࡥࡵࡣ࡬ࡰࡸࠨ໅"): {
            bstack11l1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢໆ"): name,
            bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡓࡷࡱࡍࡩࠨ໇"): os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤ࡚ࡅࡔࡖࡢࡖ࡚ࡔ࡟ࡊࡆ່ࠪ")),
            bstack11l1l11_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡓࡥࡹ࡮້ࠢ"): str(path),
            bstack11l1l11_opy_ (u"ࠨࡳࡤࡱࡳࡩࡑ࡯ࡳࡵࠤ໊"): [module_name, *bstack11lll11l1l_opy_, name],
        },
        bstack11l1l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ໋"): _11l1lll11l_opy_(driver, bstack1ll11lll11_opy_)
    }
    logger.debug(bstack11l1l11_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫ໌"))
    logger.debug(driver.execute_async_script(bstack1l1ll111ll_opy_.perform_scan, {bstack11l1l11_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤໍ"): name}))
    logger.debug(driver.execute_async_script(bstack1l1ll111ll_opy_.bstack11ll11l1ll_opy_, bstack11ll1l111l_opy_))
    logger.info(bstack11l1l11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨ໎"))
  except Exception as bstack11l1lll1ll_opy_:
    logger.error(bstack11l1l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨ໏") + str(path) + bstack11l1l11_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢ໐") + str(bstack11l1lll1ll_opy_))