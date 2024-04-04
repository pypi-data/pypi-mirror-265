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
class bstack11l1ll1111_opy_(object):
  bstack1ll1l1ll_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"࠭ࡾࠨ໑")), bstack11l1l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ໒"))
  bstack11l1ll1l1l_opy_ = os.path.join(bstack1ll1l1ll_opy_, bstack11l1l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨ໓"))
  bstack11l1ll1l11_opy_ = None
  perform_scan = None
  bstack1ll1111lll_opy_ = None
  bstack11l11lll1_opy_ = None
  bstack11ll11l1ll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11l1l11_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫ໔")):
      cls.instance = super(bstack11l1ll1111_opy_, cls).__new__(cls)
      cls.instance.bstack11l1ll11ll_opy_()
    return cls.instance
  def bstack11l1ll11ll_opy_(self):
    try:
      with open(self.bstack11l1ll1l1l_opy_, bstack11l1l11_opy_ (u"ࠪࡶࠬ໕")) as bstack1ll1llll1_opy_:
        bstack11l1ll111l_opy_ = bstack1ll1llll1_opy_.read()
        data = json.loads(bstack11l1ll111l_opy_)
        if bstack11l1l11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭໖") in data:
          self.bstack11l1ll1ll1_opy_(data[bstack11l1l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ໗")])
        if bstack11l1l11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ໘") in data:
          self.bstack11ll11l1l1_opy_(data[bstack11l1l11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ໙")])
    except:
      pass
  def bstack11ll11l1l1_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack11l1l11_opy_ (u"ࠨࡵࡦࡥࡳ࠭໚")]
      self.bstack1ll1111lll_opy_ = scripts[bstack11l1l11_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭໛")]
      self.bstack11l11lll1_opy_ = scripts[bstack11l1l11_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧໜ")]
      self.bstack11ll11l1ll_opy_ = scripts[bstack11l1l11_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩໝ")]
  def bstack11l1ll1ll1_opy_(self, bstack11l1ll1l11_opy_):
    if bstack11l1ll1l11_opy_ != None and len(bstack11l1ll1l11_opy_) != 0:
      self.bstack11l1ll1l11_opy_ = bstack11l1ll1l11_opy_
  def store(self):
    try:
      with open(self.bstack11l1ll1l1l_opy_, bstack11l1l11_opy_ (u"ࠬࡽࠧໞ")) as file:
        json.dump({
          bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣໟ"): self.bstack11l1ll1l11_opy_,
          bstack11l1l11_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣ໠"): {
            bstack11l1l11_opy_ (u"ࠣࡵࡦࡥࡳࠨ໡"): self.perform_scan,
            bstack11l1l11_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨ໢"): self.bstack1ll1111lll_opy_,
            bstack11l1l11_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢ໣"): self.bstack11l11lll1_opy_,
            bstack11l1l11_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤ໤"): self.bstack11ll11l1ll_opy_
          }
        }, file)
    except:
      pass
  def bstack1lll11ll1_opy_(self, bstack11l1ll11l1_opy_):
    try:
      return any(command.get(bstack11l1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ໥")) == bstack11l1ll11l1_opy_ for command in self.bstack11l1ll1l11_opy_)
    except:
      return False
bstack1l1ll111ll_opy_ = bstack11l1ll1111_opy_()