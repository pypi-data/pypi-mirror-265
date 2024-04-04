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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111lllllll_opy_
from browserstack_sdk.bstack11llll1l1_opy_ import bstack1ll1ll11_opy_
def _111ll11l11_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111ll1111l_opy_:
    def __init__(self, handler):
        self._111l1ll1ll_opy_ = {}
        self._111l1l1lll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1ll1ll11_opy_.version()
        if bstack111lllllll_opy_(pytest_version, bstack11l1l11_opy_ (u"ࠣ࠺࠱࠵࠳࠷ࠢጞ")) >= 0:
            self._111l1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬጟ")] = Module._register_setup_function_fixture
            self._111l1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫጠ")] = Module._register_setup_module_fixture
            self._111l1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫጡ")] = Class._register_setup_class_fixture
            self._111l1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ጢ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111ll11111_opy_(bstack11l1l11_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩጣ"))
            Module._register_setup_module_fixture = self.bstack111ll11111_opy_(bstack11l1l11_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨጤ"))
            Class._register_setup_class_fixture = self.bstack111ll11111_opy_(bstack11l1l11_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨጥ"))
            Class._register_setup_method_fixture = self.bstack111ll11111_opy_(bstack11l1l11_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪጦ"))
        else:
            self._111l1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ጧ")] = Module._inject_setup_function_fixture
            self._111l1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬጨ")] = Module._inject_setup_module_fixture
            self._111l1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬጩ")] = Class._inject_setup_class_fixture
            self._111l1ll1ll_opy_[bstack11l1l11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧጪ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111ll11111_opy_(bstack11l1l11_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪጫ"))
            Module._inject_setup_module_fixture = self.bstack111ll11111_opy_(bstack11l1l11_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩጬ"))
            Class._inject_setup_class_fixture = self.bstack111ll11111_opy_(bstack11l1l11_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩጭ"))
            Class._inject_setup_method_fixture = self.bstack111ll11111_opy_(bstack11l1l11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫጮ"))
    def bstack111l1lll1l_opy_(self, bstack111l1lllll_opy_, hook_type):
        meth = getattr(bstack111l1lllll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111l1l1lll_opy_[hook_type] = meth
            setattr(bstack111l1lllll_opy_, hook_type, self.bstack111ll111ll_opy_(hook_type))
    def bstack111l1ll11l_opy_(self, instance, bstack111l1ll1l1_opy_):
        if bstack111l1ll1l1_opy_ == bstack11l1l11_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢጯ"):
            self.bstack111l1lll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨጰ"))
            self.bstack111l1lll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥጱ"))
        if bstack111l1ll1l1_opy_ == bstack11l1l11_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣጲ"):
            self.bstack111l1lll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢጳ"))
            self.bstack111l1lll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦጴ"))
        if bstack111l1ll1l1_opy_ == bstack11l1l11_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥጵ"):
            self.bstack111l1lll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤጶ"))
            self.bstack111l1lll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨጷ"))
        if bstack111l1ll1l1_opy_ == bstack11l1l11_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢጸ"):
            self.bstack111l1lll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨጹ"))
            self.bstack111l1lll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥጺ"))
    @staticmethod
    def bstack111l1lll11_opy_(hook_type, func, args):
        if hook_type in [bstack11l1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨጻ"), bstack11l1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬጼ")]:
            _111ll11l11_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111ll111ll_opy_(self, hook_type):
        def bstack111ll111l1_opy_(arg=None):
            self.handler(hook_type, bstack11l1l11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫጽ"))
            result = None
            exception = None
            try:
                self.bstack111l1lll11_opy_(hook_type, self._111l1l1lll_opy_[hook_type], (arg,))
                result = Result(result=bstack11l1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬጾ"))
            except Exception as e:
                result = Result(result=bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ጿ"), exception=e)
                self.handler(hook_type, bstack11l1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ፀ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1l11_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧፁ"), result)
        def bstack111l1l1ll1_opy_(this, arg=None):
            self.handler(hook_type, bstack11l1l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩፂ"))
            result = None
            exception = None
            try:
                self.bstack111l1lll11_opy_(hook_type, self._111l1l1lll_opy_[hook_type], (this, arg))
                result = Result(result=bstack11l1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪፃ"))
            except Exception as e:
                result = Result(result=bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫፄ"), exception=e)
                self.handler(hook_type, bstack11l1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫፅ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬፆ"), result)
        if hook_type in [bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ፇ"), bstack11l1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪፈ")]:
            return bstack111l1l1ll1_opy_
        return bstack111ll111l1_opy_
    def bstack111ll11111_opy_(self, bstack111l1ll1l1_opy_):
        def bstack111l1ll111_opy_(this, *args, **kwargs):
            self.bstack111l1ll11l_opy_(this, bstack111l1ll1l1_opy_)
            self._111l1ll1ll_opy_[bstack111l1ll1l1_opy_](this, *args, **kwargs)
        return bstack111l1ll111_opy_