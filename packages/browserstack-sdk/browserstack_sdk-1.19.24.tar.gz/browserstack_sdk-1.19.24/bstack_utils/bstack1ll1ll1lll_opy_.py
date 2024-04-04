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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l1l11111_opy_
import tempfile
import json
bstack111l11l111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫፉ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11l1l11_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨፊ"),
      datefmt=bstack11l1l11_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ፋ"),
      stream=sys.stdout
    )
  return logger
def bstack111l11llll_opy_():
  global bstack111l11l111_opy_
  if os.path.exists(bstack111l11l111_opy_):
    os.remove(bstack111l11l111_opy_)
def bstack1l1l111l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11l1llll1_opy_(config, log_level):
  bstack111l1l11ll_opy_ = log_level
  if bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧፌ") in config:
    bstack111l1l11ll_opy_ = bstack11l1l11111_opy_[config[bstack11l1l11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨፍ")]]
  if config.get(bstack11l1l11_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩፎ"), False):
    logging.getLogger().setLevel(bstack111l1l11ll_opy_)
    return bstack111l1l11ll_opy_
  global bstack111l11l111_opy_
  bstack1l1l111l_opy_()
  bstack111l1l1l11_opy_ = logging.Formatter(
    fmt=bstack11l1l11_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ፏ"),
    datefmt=bstack11l1l11_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫፐ")
  )
  bstack111l1l11l1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111l11l111_opy_)
  file_handler.setFormatter(bstack111l1l1l11_opy_)
  bstack111l1l11l1_opy_.setFormatter(bstack111l1l1l11_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111l1l11l1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11l1l11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬፑ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111l1l11l1_opy_.setLevel(bstack111l1l11ll_opy_)
  logging.getLogger().addHandler(bstack111l1l11l1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111l1l11ll_opy_
def bstack111l11l1ll_opy_(config):
  try:
    bstack111l11ll1l_opy_ = set([
      bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ፒ"), bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨፓ"), bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩፔ"), bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫፕ"), bstack11l1l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪፖ"),
      bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬፗ"), bstack11l1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ፘ"), bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬፙ"), bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ፚ")
    ])
    bstack111l1l1111_opy_ = bstack11l1l11_opy_ (u"࠭ࠧ፛")
    with open(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ፜")) as bstack111l11lll1_opy_:
      bstack111l1l1l1l_opy_ = bstack111l11lll1_opy_.read()
      bstack111l1l1111_opy_ = re.sub(bstack11l1l11_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩ፝"), bstack11l1l11_opy_ (u"ࠩࠪ፞"), bstack111l1l1l1l_opy_, flags=re.M)
      bstack111l1l1111_opy_ = re.sub(
        bstack11l1l11_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭፟") + bstack11l1l11_opy_ (u"ࠫࢁ࠭፠").join(bstack111l11ll1l_opy_) + bstack11l1l11_opy_ (u"ࠬ࠯࠮ࠫࠦࠪ፡"),
        bstack11l1l11_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨ።"),
        bstack111l1l1111_opy_, flags=re.M | re.I
      )
    def bstack111l11ll11_opy_(dic):
      bstack111l1l111l_opy_ = {}
      for key, value in dic.items():
        if key in bstack111l11ll1l_opy_:
          bstack111l1l111l_opy_[key] = bstack11l1l11_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ፣")
        else:
          if isinstance(value, dict):
            bstack111l1l111l_opy_[key] = bstack111l11ll11_opy_(value)
          else:
            bstack111l1l111l_opy_[key] = value
      return bstack111l1l111l_opy_
    bstack111l1l111l_opy_ = bstack111l11ll11_opy_(config)
    return {
      bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫ፤"): bstack111l1l1111_opy_,
      bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬ፥"): json.dumps(bstack111l1l111l_opy_)
    }
  except Exception as e:
    return {}
def bstack1ll1l1l11l_opy_(config):
  global bstack111l11l111_opy_
  try:
    if config.get(bstack11l1l11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬ፦"), False):
      return
    uuid = os.getenv(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ፧"))
    if not uuid or uuid == bstack11l1l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ፨"):
      return
    bstack111l11l11l_opy_ = [bstack11l1l11_opy_ (u"࠭ࡲࡦࡳࡸ࡭ࡷ࡫࡭ࡦࡰࡷࡷ࠳ࡺࡸࡵࠩ፩"), bstack11l1l11_opy_ (u"ࠧࡑ࡫ࡳࡪ࡮ࡲࡥࠨ፪"), bstack11l1l11_opy_ (u"ࠨࡲࡼࡴࡷࡵࡪࡦࡥࡷ࠲ࡹࡵ࡭࡭ࠩ፫"), bstack111l11l111_opy_]
    bstack1l1l111l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯࡯ࡳ࡬ࡹ࠭ࠨ፬") + uuid + bstack11l1l11_opy_ (u"ࠪ࠲ࡹࡧࡲ࠯ࡩࡽࠫ፭"))
    with tarfile.open(output_file, bstack11l1l11_opy_ (u"ࠦࡼࡀࡧࡻࠤ፮")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111l11l11l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111l11l1ll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111l11l1l1_opy_ = data.encode()
        tarinfo.size = len(bstack111l11l1l1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111l11l1l1_opy_))
    bstack11l1l111_opy_ = MultipartEncoder(
      fields= {
        bstack11l1l11_opy_ (u"ࠬࡪࡡࡵࡣࠪ፯"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11l1l11_opy_ (u"࠭ࡲࡣࠩ፰")), bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡾ࠭ࡨࡼ࡬ࡴࠬ፱")),
        bstack11l1l11_opy_ (u"ࠨࡥ࡯࡭ࡪࡴࡴࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ፲"): uuid
      }
    )
    response = requests.post(
      bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡹࡵࡲ࡯ࡢࡦ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡣ࡭࡫ࡨࡲࡹ࠳࡬ࡰࡩࡶ࠳ࡺࡶ࡬ࡰࡣࡧࠦ፳"),
      data=bstack11l1l111_opy_,
      headers={bstack11l1l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ፴"): bstack11l1l111_opy_.content_type},
      auth=(config[bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭፵")], config[bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ፶")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11l1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰ࡭ࡱࡤࡨࠥࡲ࡯ࡨࡵ࠽ࠤࠬ፷") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11l1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷ࠿࠭፸") + str(e))
  finally:
    try:
      bstack111l11llll_opy_()
    except:
      pass