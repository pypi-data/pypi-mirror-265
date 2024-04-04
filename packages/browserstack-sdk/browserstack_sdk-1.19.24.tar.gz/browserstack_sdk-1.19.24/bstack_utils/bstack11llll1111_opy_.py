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
from uuid import uuid4
from bstack_utils.helper import bstack1l1lll111_opy_, bstack11l1111l1l_opy_
from bstack_utils.bstack1l111111l_opy_ import bstack1llllll1lll_opy_
class bstack11lll1l1ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l111lll11_opy_=None, framework=None, tags=[], scope=[], bstack1llll111l1l_opy_=None, bstack1llll1l11ll_opy_=True, bstack1llll111lll_opy_=None, bstack111l111l1_opy_=None, result=None, duration=None, bstack1l11l111ll_opy_=None, meta={}):
        self.bstack1l11l111ll_opy_ = bstack1l11l111ll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llll1l11ll_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l111lll11_opy_ = bstack1l111lll11_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llll111l1l_opy_ = bstack1llll111l1l_opy_
        self.bstack1llll111lll_opy_ = bstack1llll111lll_opy_
        self.bstack111l111l1_opy_ = bstack111l111l1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l11l11111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll1l1111_opy_(self):
        bstack1llll1l1l1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11l1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᒳ"): bstack1llll1l1l1l_opy_,
            bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᒴ"): bstack1llll1l1l1l_opy_,
            bstack11l1l11_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᒵ"): bstack1llll1l1l1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11l1l11_opy_ (u"࡙ࠥࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡹࡲ࡫࡮ࡵ࠼ࠣࠦᒶ") + key)
            setattr(self, key, val)
    def bstack1llll11ll11_opy_(self):
        return {
            bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᒷ"): self.name,
            bstack11l1l11_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᒸ"): {
                bstack11l1l11_opy_ (u"࠭࡬ࡢࡰࡪࠫᒹ"): bstack11l1l11_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᒺ"),
                bstack11l1l11_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᒻ"): self.code
            },
            bstack11l1l11_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᒼ"): self.scope,
            bstack11l1l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᒽ"): self.tags,
            bstack11l1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᒾ"): self.framework,
            bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᒿ"): self.bstack1l111lll11_opy_
        }
    def bstack1llll11l1ll_opy_(self):
        return {
         bstack11l1l11_opy_ (u"࠭࡭ࡦࡶࡤࠫᓀ"): self.meta
        }
    def bstack1llll11l111_opy_(self):
        return {
            bstack11l1l11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᓁ"): {
                bstack11l1l11_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᓂ"): self.bstack1llll111l1l_opy_
            }
        }
    def bstack1llll11l1l1_opy_(self, bstack1llll11ll1l_opy_, details):
        step = next(filter(lambda st: st[bstack11l1l11_opy_ (u"ࠩ࡬ࡨࠬᓃ")] == bstack1llll11ll1l_opy_, self.meta[bstack11l1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᓄ")]), None)
        step.update(details)
    def bstack1llll11lll1_opy_(self, bstack1llll11ll1l_opy_):
        step = next(filter(lambda st: st[bstack11l1l11_opy_ (u"ࠫ࡮ࡪࠧᓅ")] == bstack1llll11ll1l_opy_, self.meta[bstack11l1l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᓆ")]), None)
        step.update({
            bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᓇ"): bstack1l1lll111_opy_()
        })
    def bstack1l11l1111l_opy_(self, bstack1llll11ll1l_opy_, result, duration=None):
        bstack1llll111lll_opy_ = bstack1l1lll111_opy_()
        if bstack1llll11ll1l_opy_ is not None and self.meta.get(bstack11l1l11_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᓈ")):
            step = next(filter(lambda st: st[bstack11l1l11_opy_ (u"ࠨ࡫ࡧࠫᓉ")] == bstack1llll11ll1l_opy_, self.meta[bstack11l1l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᓊ")]), None)
            step.update({
                bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᓋ"): bstack1llll111lll_opy_,
                bstack11l1l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᓌ"): duration if duration else bstack11l1111l1l_opy_(step[bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᓍ")], bstack1llll111lll_opy_),
                bstack11l1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᓎ"): result.result,
                bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᓏ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llll1l111l_opy_):
        if self.meta.get(bstack11l1l11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᓐ")):
            self.meta[bstack11l1l11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᓑ")].append(bstack1llll1l111l_opy_)
        else:
            self.meta[bstack11l1l11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᓒ")] = [ bstack1llll1l111l_opy_ ]
    def bstack1llll11l11l_opy_(self):
        return {
            bstack11l1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᓓ"): self.bstack1l11l11111_opy_(),
            **self.bstack1llll11ll11_opy_(),
            **self.bstack1llll1l1111_opy_(),
            **self.bstack1llll11l1ll_opy_()
        }
    def bstack1llll11llll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᓔ"): self.bstack1llll111lll_opy_,
            bstack11l1l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᓕ"): self.duration,
            bstack11l1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᓖ"): self.result.result
        }
        if data[bstack11l1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᓗ")] == bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᓘ"):
            data[bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᓙ")] = self.result.bstack11ll1l11l1_opy_()
            data[bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᓚ")] = [{bstack11l1l11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᓛ"): self.result.bstack111llll111_opy_()}]
        return data
    def bstack1llll1l1l11_opy_(self):
        return {
            bstack11l1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᓜ"): self.bstack1l11l11111_opy_(),
            **self.bstack1llll11ll11_opy_(),
            **self.bstack1llll1l1111_opy_(),
            **self.bstack1llll11llll_opy_(),
            **self.bstack1llll11l1ll_opy_()
        }
    def bstack11llll1lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11l1l11_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡫ࡤࠨᓝ") in event:
            return self.bstack1llll11l11l_opy_()
        elif bstack11l1l11_opy_ (u"ࠨࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᓞ") in event:
            return self.bstack1llll1l1l11_opy_()
    def bstack11lll11ll1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1llll111lll_opy_ = time if time else bstack1l1lll111_opy_()
        self.duration = duration if duration else bstack11l1111l1l_opy_(self.bstack1l111lll11_opy_, self.bstack1llll111lll_opy_)
        if result:
            self.result = result
class bstack1l111llll1_opy_(bstack11lll1l1ll_opy_):
    def __init__(self, hooks=[], bstack1l11111lll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l11111lll_opy_ = bstack1l11111lll_opy_
        super().__init__(*args, **kwargs, bstack111l111l1_opy_=bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺࠧᓟ"))
    @classmethod
    def bstack1llll1l11l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l1l11_opy_ (u"ࠪ࡭ࡩ࠭ᓠ"): id(step),
                bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡸࡵࠩᓡ"): step.name,
                bstack11l1l11_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ᓢ"): step.keyword,
            })
        return bstack1l111llll1_opy_(
            **kwargs,
            meta={
                bstack11l1l11_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧᓣ"): {
                    bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᓤ"): feature.name,
                    bstack11l1l11_opy_ (u"ࠨࡲࡤࡸ࡭࠭ᓥ"): feature.filename,
                    bstack11l1l11_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᓦ"): feature.description
                },
                bstack11l1l11_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬᓧ"): {
                    bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᓨ"): scenario.name
                },
                bstack11l1l11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᓩ"): steps,
                bstack11l1l11_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨᓪ"): bstack1llllll1lll_opy_(test)
            }
        )
    def bstack1llll111l11_opy_(self):
        return {
            bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᓫ"): self.hooks
        }
    def bstack1llll1111ll_opy_(self):
        if self.bstack1l11111lll_opy_:
            return {
                bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᓬ"): self.bstack1l11111lll_opy_
            }
        return {}
    def bstack1llll1l1l11_opy_(self):
        return {
            **super().bstack1llll1l1l11_opy_(),
            **self.bstack1llll111l11_opy_()
        }
    def bstack1llll11l11l_opy_(self):
        return {
            **super().bstack1llll11l11l_opy_(),
            **self.bstack1llll1111ll_opy_()
        }
    def bstack11lll11ll1_opy_(self):
        return bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᓭ")
class bstack1l1111111l_opy_(bstack11lll1l1ll_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack111l111l1_opy_=bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᓮ"))
    def bstack1l1111l11l_opy_(self):
        return self.hook_type
    def bstack1llll111ll1_opy_(self):
        return {
            bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᓯ"): self.hook_type
        }
    def bstack1llll1l1l11_opy_(self):
        return {
            **super().bstack1llll1l1l11_opy_(),
            **self.bstack1llll111ll1_opy_()
        }
    def bstack1llll11l11l_opy_(self):
        return {
            **super().bstack1llll11l11l_opy_(),
            **self.bstack1llll111ll1_opy_()
        }
    def bstack11lll11ll1_opy_(self):
        return bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧᓰ")