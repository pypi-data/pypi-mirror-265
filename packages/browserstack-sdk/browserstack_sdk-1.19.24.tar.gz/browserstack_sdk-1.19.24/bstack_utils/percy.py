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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack11ll1111_opy_, bstack1llll11lll_opy_
class bstack1l1l11lll1_opy_:
  working_dir = os.getcwd()
  bstack1llll11111_opy_ = False
  config = {}
  binary_path = bstack11l1l11_opy_ (u"ࠩࠪᏀ")
  bstack1111lll1ll_opy_ = bstack11l1l11_opy_ (u"ࠪࠫᏁ")
  bstack1ll111l11_opy_ = False
  bstack1111llll1l_opy_ = None
  bstack1111ll11l1_opy_ = {}
  bstack11111l1ll1_opy_ = 300
  bstack1111lll1l1_opy_ = False
  logger = None
  bstack11111llll1_opy_ = False
  bstack11111l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠫࠬᏂ")
  bstack1111ll11ll_opy_ = {
    bstack11l1l11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᏃ") : 1,
    bstack11l1l11_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧᏄ") : 2,
    bstack11l1l11_opy_ (u"ࠧࡦࡦࡪࡩࠬᏅ") : 3,
    bstack11l1l11_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨᏆ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1111llll11_opy_(self):
    bstack11111ll11l_opy_ = bstack11l1l11_opy_ (u"ࠩࠪᏇ")
    bstack1111l1111l_opy_ = sys.platform
    bstack1111l111l1_opy_ = bstack11l1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᏈ")
    if re.match(bstack11l1l11_opy_ (u"ࠦࡩࡧࡲࡸ࡫ࡱࢀࡲࡧࡣࠡࡱࡶࠦᏉ"), bstack1111l1111l_opy_) != None:
      bstack11111ll11l_opy_ = bstack11l1l11ll1_opy_ + bstack11l1l11_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡵࡳࡹ࠰ࡽ࡭ࡵࠨᏊ")
      self.bstack11111l1l1l_opy_ = bstack11l1l11_opy_ (u"࠭࡭ࡢࡥࠪᏋ")
    elif re.match(bstack11l1l11_opy_ (u"ࠢ࡮ࡵࡺ࡭ࡳࢂ࡭ࡴࡻࡶࢀࡲ࡯࡮ࡨࡹࡿࡧࡾ࡭ࡷࡪࡰࡿࡦࡨࡩࡷࡪࡰࡿࡻ࡮ࡴࡣࡦࡾࡨࡱࡨࢂࡷࡪࡰ࠶࠶ࠧᏌ"), bstack1111l1111l_opy_) != None:
      bstack11111ll11l_opy_ = bstack11l1l11ll1_opy_ + bstack11l1l11_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡹ࡬ࡲ࠳ࢀࡩࡱࠤᏍ")
      bstack1111l111l1_opy_ = bstack11l1l11_opy_ (u"ࠤࡳࡩࡷࡩࡹ࠯ࡧࡻࡩࠧᏎ")
      self.bstack11111l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠪࡻ࡮ࡴࠧᏏ")
    else:
      bstack11111ll11l_opy_ = bstack11l1l11ll1_opy_ + bstack11l1l11_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡱ࡯࡮ࡶࡺ࠱ࡾ࡮ࡶࠢᏐ")
      self.bstack11111l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫᏑ")
    return bstack11111ll11l_opy_, bstack1111l111l1_opy_
  def bstack1111ll1111_opy_(self):
    try:
      bstack1111l1l11l_opy_ = [os.path.join(expanduser(bstack11l1l11_opy_ (u"ࠨࡾࠣᏒ")), bstack11l1l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᏓ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1111l1l11l_opy_:
        if(self.bstack11111l1lll_opy_(path)):
          return path
      raise bstack11l1l11_opy_ (u"ࠣࡗࡱࡥࡱࡨࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᏔ")
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠭ࠡࡽࢀࠦᏕ").format(e))
  def bstack11111l1lll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111ll1l1l_opy_(self, bstack11111ll11l_opy_, bstack1111l111l1_opy_):
    try:
      bstack1111ll1lll_opy_ = self.bstack1111ll1111_opy_()
      bstack11111lll1l_opy_ = os.path.join(bstack1111ll1lll_opy_, bstack11l1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰ࡽ࡭ࡵ࠭Ꮦ"))
      bstack1111ll1l11_opy_ = os.path.join(bstack1111ll1lll_opy_, bstack1111l111l1_opy_)
      if os.path.exists(bstack1111ll1l11_opy_):
        self.logger.info(bstack11l1l11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᏗ").format(bstack1111ll1l11_opy_))
        return bstack1111ll1l11_opy_
      if os.path.exists(bstack11111lll1l_opy_):
        self.logger.info(bstack11l1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡿ࡯ࡰࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡶࡰࡽ࡭ࡵࡶࡩ࡯ࡩࠥᏘ").format(bstack11111lll1l_opy_))
        return self.bstack1111l1llll_opy_(bstack11111lll1l_opy_, bstack1111l111l1_opy_)
      self.logger.info(bstack11l1l11_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭ࠡࡽࢀࠦᏙ").format(bstack11111ll11l_opy_))
      response = bstack1llll11lll_opy_(bstack11l1l11_opy_ (u"ࠧࡈࡇࡗࠫᏚ"), bstack11111ll11l_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack11111lll1l_opy_, bstack11l1l11_opy_ (u"ࠨࡹࡥࠫᏛ")) as file:
          file.write(response.content)
        self.logger.info(bstack11l1l11_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡧ࡮ࡥࠢࡶࡥࡻ࡫ࡤࠡࡣࡷࠤࢀࢃࠢᏜ").format(bstack11111lll1l_opy_))
        return self.bstack1111l1llll_opy_(bstack11111lll1l_opy_, bstack1111l111l1_opy_)
      else:
        raise(bstack11l1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠤࡘࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠼ࠣࡿࢂࠨᏝ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧᏞ").format(e))
  def bstack1111l1l1ll_opy_(self, bstack11111ll11l_opy_, bstack1111l111l1_opy_):
    try:
      retry = 2
      bstack1111ll1l11_opy_ = None
      bstack1111l1l1l1_opy_ = False
      while retry > 0:
        bstack1111ll1l11_opy_ = self.bstack1111ll1l1l_opy_(bstack11111ll11l_opy_, bstack1111l111l1_opy_)
        bstack1111l1l1l1_opy_ = self.bstack11111l11l1_opy_(bstack11111ll11l_opy_, bstack1111l111l1_opy_, bstack1111ll1l11_opy_)
        if bstack1111l1l1l1_opy_:
          break
        retry -= 1
      return bstack1111ll1l11_opy_, bstack1111l1l1l1_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡵࡧࡴࡩࠤᏟ").format(e))
    return bstack1111ll1l11_opy_, False
  def bstack11111l11l1_opy_(self, bstack11111ll11l_opy_, bstack1111l111l1_opy_, bstack1111ll1l11_opy_, bstack11111l111l_opy_ = 0):
    if bstack11111l111l_opy_ > 1:
      return False
    if bstack1111ll1l11_opy_ == None or os.path.exists(bstack1111ll1l11_opy_) == False:
      self.logger.warn(bstack11l1l11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡳࡧࡷࡶࡾ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦᏠ"))
      return False
    bstack1111l1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠢ࡟࠰࠭ࡄࡵ࡫ࡲࡤࡻ࡟࠳ࡨࡲࡩࠡ࡞ࡧ࠲ࡡࡪࠫ࠯࡞ࡧ࠯ࠧᏡ")
    command = bstack11l1l11_opy_ (u"ࠨࡽࢀࠤ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧᏢ").format(bstack1111ll1l11_opy_)
    bstack1111l111ll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1111l1ll1l_opy_, bstack1111l111ll_opy_) != None:
      return True
    else:
      self.logger.error(bstack11l1l11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡤ࡭ࡱ࡫ࡤࠣᏣ"))
      return False
  def bstack1111l1llll_opy_(self, bstack11111lll1l_opy_, bstack1111l111l1_opy_):
    try:
      working_dir = os.path.dirname(bstack11111lll1l_opy_)
      shutil.unpack_archive(bstack11111lll1l_opy_, working_dir)
      bstack1111ll1l11_opy_ = os.path.join(working_dir, bstack1111l111l1_opy_)
      os.chmod(bstack1111ll1l11_opy_, 0o755)
      return bstack1111ll1l11_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡵ࡯ࡼ࡬ࡴࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦᏤ"))
  def bstack11111l11ll_opy_(self):
    try:
      percy = str(self.config.get(bstack11l1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᏥ"), bstack11l1l11_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦᏦ"))).lower()
      if percy != bstack11l1l11_opy_ (u"ࠨࡴࡳࡷࡨࠦᏧ"):
        return False
      self.bstack1ll111l11_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᏨ").format(e))
  def bstack1111l11111_opy_(self):
    try:
      bstack1111l11111_opy_ = str(self.config.get(bstack11l1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᏩ"), bstack11l1l11_opy_ (u"ࠤࡤࡹࡹࡵࠢᏪ"))).lower()
      return bstack1111l11111_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᏫ").format(e))
  def init(self, bstack1llll11111_opy_, config, logger):
    self.bstack1llll11111_opy_ = bstack1llll11111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11111l11ll_opy_():
      return
    self.bstack1111ll11l1_opy_ = config.get(bstack11l1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᏬ"), {})
    self.bstack1111lll11l_opy_ = config.get(bstack11l1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᏭ"), bstack11l1l11_opy_ (u"ࠨࡡࡶࡶࡲࠦᏮ"))
    try:
      bstack11111ll11l_opy_, bstack1111l111l1_opy_ = self.bstack1111llll11_opy_()
      bstack1111ll1l11_opy_, bstack1111l1l1l1_opy_ = self.bstack1111l1l1ll_opy_(bstack11111ll11l_opy_, bstack1111l111l1_opy_)
      if bstack1111l1l1l1_opy_:
        self.binary_path = bstack1111ll1l11_opy_
        thread = Thread(target=self.bstack11111ll1ll_opy_)
        thread.start()
      else:
        self.bstack11111llll1_opy_ = True
        self.logger.error(bstack11l1l11_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾ࠮࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡖࡥࡳࡥࡼࠦᏯ").format(bstack1111ll1l11_opy_))
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᏰ").format(e))
  def bstack1111llllll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11l1l11_opy_ (u"ࠩ࡯ࡳ࡬࠭Ᏹ"), bstack11l1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰࡯ࡳ࡬࠭Ᏺ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡕࡻࡳࡩ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࡴࠢࡤࡸࠥࢁࡽࠣᏳ").format(logfile))
      self.bstack1111lll1ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࠡࡲࡤࡸ࡭࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᏴ").format(e))
  def bstack11111ll1ll_opy_(self):
    bstack1111l11l11_opy_ = self.bstack11111lllll_opy_()
    if bstack1111l11l11_opy_ == None:
      self.bstack11111llll1_opy_ = True
      self.logger.error(bstack11l1l11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠤᏵ"))
      return False
    command_args = [bstack11l1l11_opy_ (u"ࠢࡢࡲࡳ࠾ࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠣ᏶") if self.bstack1llll11111_opy_ else bstack11l1l11_opy_ (u"ࠨࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠬ᏷")]
    bstack111111lll1_opy_ = self.bstack1111l11ll1_opy_()
    if bstack111111lll1_opy_ != None:
      command_args.append(bstack11l1l11_opy_ (u"ࠤ࠰ࡧࠥࢁࡽࠣᏸ").format(bstack111111lll1_opy_))
    env = os.environ.copy()
    env[bstack11l1l11_opy_ (u"ࠥࡔࡊࡘࡃ࡚ࡡࡗࡓࡐࡋࡎࠣᏹ")] = bstack1111l11l11_opy_
    bstack1111l11l1l_opy_ = [self.binary_path]
    self.bstack1111llllll_opy_()
    self.bstack1111llll1l_opy_ = self.bstack111l111111_opy_(bstack1111l11l1l_opy_ + command_args, env)
    self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠧᏺ"))
    bstack11111l111l_opy_ = 0
    while self.bstack1111llll1l_opy_.poll() == None:
      bstack1111l11lll_opy_ = self.bstack1111l1ll11_opy_()
      if bstack1111l11lll_opy_:
        self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠣᏻ"))
        self.bstack1111lll1l1_opy_ = True
        return True
      bstack11111l111l_opy_ += 1
      self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡘࡥࡵࡴࡼࠤ࠲ࠦࡻࡾࠤᏼ").format(bstack11111l111l_opy_))
      time.sleep(2)
    self.logger.error(bstack11l1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡼࡿࠣࡥࡹࡺࡥ࡮ࡲࡷࡷࠧᏽ").format(bstack11111l111l_opy_))
    self.bstack11111llll1_opy_ = True
    return False
  def bstack1111l1ll11_opy_(self, bstack11111l111l_opy_ = 0):
    try:
      if bstack11111l111l_opy_ > 10:
        return False
      bstack11111ll1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࠨ᏾"), bstack11l1l11_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸ࠿࠻࠳࠴࠺ࠪ᏿"))
      bstack111l11111l_opy_ = bstack11111ll1l1_opy_ + bstack11l1l11lll_opy_
      response = requests.get(bstack111l11111l_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack11111lllll_opy_(self):
    bstack1111l1l111_opy_ = bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࠧ᐀") if self.bstack1llll11111_opy_ else bstack11l1l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᐁ")
    bstack11l11l111l_opy_ = bstack11l1l11_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠦᐂ").format(self.config[bstack11l1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᐃ")], bstack1111l1l111_opy_)
    uri = bstack11ll1111_opy_(bstack11l11l111l_opy_)
    try:
      response = bstack1llll11lll_opy_(bstack11l1l11_opy_ (u"ࠧࡈࡇࡗࠫᐄ"), uri, {}, {bstack11l1l11_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᐅ"): (self.config[bstack11l1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᐆ")], self.config[bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᐇ")])})
      if response.status_code == 200:
        bstack1111l1lll1_opy_ = response.json()
        if bstack11l1l11_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥᐈ") in bstack1111l1lll1_opy_:
          return bstack1111l1lll1_opy_[bstack11l1l11_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦᐉ")]
        else:
          raise bstack11l1l11_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠭ᐊ").format(bstack1111l1lll1_opy_)
      else:
        raise bstack11l1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃࠢᐋ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤᐌ").format(e))
  def bstack1111l11ll1_opy_(self):
    bstack11111ll111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧᐍ"))
    try:
      if bstack11l1l11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᐎ") not in self.bstack1111ll11l1_opy_:
        self.bstack1111ll11l1_opy_[bstack11l1l11_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᐏ")] = 2
      with open(bstack11111ll111_opy_, bstack11l1l11_opy_ (u"ࠬࡽࠧᐐ")) as fp:
        json.dump(self.bstack1111ll11l1_opy_, fp)
      return bstack11111ll111_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᐑ").format(e))
  def bstack111l111111_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11111l1l1l_opy_ == bstack11l1l11_opy_ (u"ࠧࡸ࡫ࡱࠫᐒ"):
        bstack11111lll11_opy_ = [bstack11l1l11_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩᐓ"), bstack11l1l11_opy_ (u"ࠩ࠲ࡧࠬᐔ")]
        cmd = bstack11111lll11_opy_ + cmd
      cmd = bstack11l1l11_opy_ (u"ࠪࠤࠬᐕ").join(cmd)
      self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽࠣᐖ").format(cmd))
      with open(self.bstack1111lll1ll_opy_, bstack11l1l11_opy_ (u"ࠧࡧࠢᐗ")) as bstack11111l1111_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11111l1111_opy_, text=True, stderr=bstack11111l1111_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack11111llll1_opy_ = True
      self.logger.error(bstack11l1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᐘ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1111lll1l1_opy_:
        self.logger.info(bstack11l1l11_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹࠣᐙ"))
        cmd = [self.binary_path, bstack11l1l11_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦᐚ")]
        self.bstack111l111111_opy_(cmd)
        self.bstack1111lll1l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᐛ").format(cmd, e))
  def bstack1lllll11ll_opy_(self):
    if not self.bstack1ll111l11_opy_:
      return
    try:
      bstack1111lll111_opy_ = 0
      while not self.bstack1111lll1l1_opy_ and bstack1111lll111_opy_ < self.bstack11111l1ll1_opy_:
        if self.bstack11111llll1_opy_:
          self.logger.info(bstack11l1l11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤࠣᐜ"))
          return
        time.sleep(1)
        bstack1111lll111_opy_ += 1
      os.environ[bstack11l1l11_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪᐝ")] = str(self.bstack1111ll1ll1_opy_())
      self.logger.info(bstack11l1l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨᐞ"))
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᐟ").format(e))
  def bstack1111ll1ll1_opy_(self):
    if self.bstack1llll11111_opy_:
      return
    try:
      bstack11111l1l11_opy_ = [platform[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᐠ")].lower() for platform in self.config.get(bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᐡ"), [])]
      bstack1111lllll1_opy_ = sys.maxsize
      bstack111111llll_opy_ = bstack11l1l11_opy_ (u"ࠩࠪᐢ")
      for browser in bstack11111l1l11_opy_:
        if browser in self.bstack1111ll11ll_opy_:
          bstack1111ll111l_opy_ = self.bstack1111ll11ll_opy_[browser]
        if bstack1111ll111l_opy_ < bstack1111lllll1_opy_:
          bstack1111lllll1_opy_ = bstack1111ll111l_opy_
          bstack111111llll_opy_ = browser
      return bstack111111llll_opy_
    except Exception as e:
      self.logger.error(bstack11l1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᐣ").format(e))