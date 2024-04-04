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
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l11l1l1l1_opy_, bstack1l1lll1l11_opy_, update, bstack1l111lll_opy_,
                                       bstack1ll11ll1_opy_, bstack11ll1ll1_opy_, bstack1lll11ll1l_opy_, bstack111l1ll1_opy_,
                                       bstack1l1ll11111_opy_, bstack11l1l111l_opy_, bstack1llll11ll_opy_, bstack1ll1ll1l11_opy_,
                                       bstack1ll1l11lll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1lll11111_opy_)
from browserstack_sdk.bstack11llll1l1_opy_ import bstack1ll1ll11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1ll1ll1lll_opy_
from bstack_utils.capture import bstack1l111l1l1l_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack11l1ll1l1_opy_, bstack1l11ll11ll_opy_, bstack1ll1lllll_opy_, \
    bstack1lll1111l_opy_
from bstack_utils.helper import bstack1111lll1l_opy_, bstack1l1l1llll_opy_, bstack111lllll1l_opy_, bstack1l1lll111_opy_, \
    bstack11l11ll111_opy_, \
    bstack11l11lll1l_opy_, bstack11l111ll_opy_, bstack1l1l11l111_opy_, bstack11l11ll11l_opy_, bstack1l1l11l11l_opy_, Notset, \
    bstack1l1l1l1l1l_opy_, bstack11l1111l1l_opy_, bstack111ll1lll1_opy_, Result, bstack111ll1l1ll_opy_, bstack11l111ll11_opy_, bstack1l11l11l11_opy_, \
    bstack1ll11l111l_opy_, bstack1l11ll11l_opy_, bstack1l1lllll1l_opy_, bstack111ll11l1l_opy_
from bstack_utils.bstack111l1llll1_opy_ import bstack111ll1111l_opy_
from bstack_utils.messages import bstack1llll1l1l_opy_, bstack1l1ll11l_opy_, bstack11ll111ll_opy_, bstack1l1l11l1l_opy_, bstack1l1l11111l_opy_, \
    bstack11ll111l1_opy_, bstack1lll111ll_opy_, bstack1ll1ll1111_opy_, bstack1l1l11l1ll_opy_, bstack111lll1l1_opy_, \
    bstack1l1l1ll11_opy_, bstack1l1ll1ll11_opy_
from bstack_utils.proxy import bstack1lll1l11ll_opy_, bstack1l1l1ll1_opy_
from bstack_utils.bstack1l111111l_opy_ import bstack1lllll1lll1_opy_, bstack1lllll1ll1l_opy_, bstack1lllll1l1ll_opy_, bstack1llllll1ll1_opy_, \
    bstack1llllll11l1_opy_, bstack1llllll1l11_opy_, bstack1lllll1ll11_opy_, bstack11l11111l_opy_, bstack1llllll11ll_opy_
from bstack_utils.bstack1l1l1111l1_opy_ import bstack1l1l111l11_opy_
from bstack_utils.bstack1l1l111ll1_opy_ import bstack111lll1ll_opy_, bstack1l1ll11lll_opy_, bstack1111l1l1l_opy_, \
    bstack1l111l111_opy_, bstack1ll1ll11l_opy_
from bstack_utils.bstack11llll1111_opy_ import bstack1l111llll1_opy_
from bstack_utils.bstack1l1lllll_opy_ import bstack1l11ll1l11_opy_
import bstack_utils.bstack1111ll11_opy_ as bstack111lllll_opy_
from bstack_utils.bstack1l1ll111ll_opy_ import bstack1l1ll111ll_opy_
bstack1lll11llll_opy_ = None
bstack1l1l11llll_opy_ = None
bstack1lllll1l1l_opy_ = None
bstack1ll11111l1_opy_ = None
bstack11111lll1_opy_ = None
bstack1ll111111_opy_ = None
bstack1l1l111111_opy_ = None
bstack1l11lll1ll_opy_ = None
bstack11ll1llll_opy_ = None
bstack1lll1ll11l_opy_ = None
bstack11llll1ll_opy_ = None
bstack1l1ll1l111_opy_ = None
bstack11lll11l_opy_ = None
bstack1lll1ll1_opy_ = bstack11l1l11_opy_ (u"ࠪࠫᗕ")
CONFIG = {}
bstack1111l111_opy_ = False
bstack1ll11ll11_opy_ = bstack11l1l11_opy_ (u"ࠫࠬᗖ")
bstack1111l1ll_opy_ = bstack11l1l11_opy_ (u"ࠬ࠭ᗗ")
bstack111111ll1_opy_ = False
bstack1lll1l111l_opy_ = []
bstack1ll1lll111_opy_ = bstack11l1ll1l1_opy_
bstack1lll111llll_opy_ = bstack11l1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᗘ")
bstack1lll11lll11_opy_ = False
bstack111l1l111_opy_ = {}
bstack111lllll1_opy_ = False
logger = bstack1ll1ll1lll_opy_.get_logger(__name__, bstack1ll1lll111_opy_)
store = {
    bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᗙ"): []
}
bstack1lll1l11lll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l1111lll1_opy_ = {}
current_test_uuid = None
def bstack1l1l11l1_opy_(page, bstack1l111lll1_opy_):
    try:
        page.evaluate(bstack11l1l11_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᗚ"),
                      bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ᗛ") + json.dumps(
                          bstack1l111lll1_opy_) + bstack11l1l11_opy_ (u"ࠥࢁࢂࠨᗜ"))
    except Exception as e:
        print(bstack11l1l11_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤᗝ"), e)
def bstack1ll1lll1ll_opy_(page, message, level):
    try:
        page.evaluate(bstack11l1l11_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᗞ"), bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫᗟ") + json.dumps(
            message) + bstack11l1l11_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪᗠ") + json.dumps(level) + bstack11l1l11_opy_ (u"ࠨࡿࢀࠫᗡ"))
    except Exception as e:
        print(bstack11l1l11_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧᗢ"), e)
def pytest_configure(config):
    bstack1ll1l11l1l_opy_ = Config.bstack1l1l1l1ll_opy_()
    config.args = bstack1l11ll1l11_opy_.bstack1lll1lll1ll_opy_(config.args)
    bstack1ll1l11l1l_opy_.bstack11111l1l1_opy_(bstack1l1lllll1l_opy_(config.getoption(bstack11l1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᗣ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1lll111lll1_opy_ = item.config.getoption(bstack11l1l11_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᗤ"))
    plugins = item.config.getoption(bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨᗥ"))
    report = outcome.get_result()
    bstack1lll1l111l1_opy_(item, call, report)
    if bstack11l1l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦᗦ") not in plugins or bstack1l1l11l11l_opy_():
        return
    summary = []
    driver = getattr(item, bstack11l1l11_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣᗧ"), None)
    page = getattr(item, bstack11l1l11_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢᗨ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1lll11ll111_opy_(item, report, summary, bstack1lll111lll1_opy_)
    if (page is not None):
        bstack1lll1l1l11l_opy_(item, report, summary, bstack1lll111lll1_opy_)
def bstack1lll11ll111_opy_(item, report, summary, bstack1lll111lll1_opy_):
    if report.when == bstack11l1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᗩ") and report.skipped:
        bstack1llllll11ll_opy_(report)
    if report.when in [bstack11l1l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᗪ"), bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᗫ")]:
        return
    if not bstack111lllll1l_opy_():
        return
    try:
        if (str(bstack1lll111lll1_opy_).lower() != bstack11l1l11_opy_ (u"ࠬࡺࡲࡶࡧࠪᗬ")):
            item._driver.execute_script(
                bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫᗭ") + json.dumps(
                    report.nodeid) + bstack11l1l11_opy_ (u"ࠧࡾࡿࠪᗮ"))
        os.environ[bstack11l1l11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫᗯ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11l1l11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤᗰ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1l11_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᗱ")))
    bstack1ll1ll111l_opy_ = bstack11l1l11_opy_ (u"ࠦࠧᗲ")
    bstack1llllll11ll_opy_(report)
    if not passed:
        try:
            bstack1ll1ll111l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11l1l11_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᗳ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1ll111l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11l1l11_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᗴ")))
        bstack1ll1ll111l_opy_ = bstack11l1l11_opy_ (u"ࠢࠣᗵ")
        if not passed:
            try:
                bstack1ll1ll111l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1l11_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᗶ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll1ll111l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ᗷ")
                    + json.dumps(bstack11l1l11_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦᗸ"))
                    + bstack11l1l11_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢᗹ")
                )
            else:
                item._driver.execute_script(
                    bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪᗺ")
                    + json.dumps(str(bstack1ll1ll111l_opy_))
                    + bstack11l1l11_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤᗻ")
                )
        except Exception as e:
            summary.append(bstack11l1l11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧᗼ").format(e))
def bstack1lll11l1111_opy_(test_name, error_message):
    try:
        bstack1lll1l111ll_opy_ = []
        bstack1111lll1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᗽ"), bstack11l1l11_opy_ (u"ࠩ࠳ࠫᗾ"))
        bstack1111l1l11_opy_ = {bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᗿ"): test_name, bstack11l1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᘀ"): error_message, bstack11l1l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᘁ"): bstack1111lll1_opy_}
        bstack1lll11l1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫᘂ"))
        if os.path.exists(bstack1lll11l1l1l_opy_):
            with open(bstack1lll11l1l1l_opy_) as f:
                bstack1lll1l111ll_opy_ = json.load(f)
        bstack1lll1l111ll_opy_.append(bstack1111l1l11_opy_)
        with open(bstack1lll11l1l1l_opy_, bstack11l1l11_opy_ (u"ࠧࡸࠩᘃ")) as f:
            json.dump(bstack1lll1l111ll_opy_, f)
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭ᘄ") + str(e))
def bstack1lll1l1l11l_opy_(item, report, summary, bstack1lll111lll1_opy_):
    if report.when in [bstack11l1l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᘅ"), bstack11l1l11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᘆ")]:
        return
    if (str(bstack1lll111lll1_opy_).lower() != bstack11l1l11_opy_ (u"ࠫࡹࡸࡵࡦࠩᘇ")):
        bstack1l1l11l1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l1l11_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᘈ")))
    bstack1ll1ll111l_opy_ = bstack11l1l11_opy_ (u"ࠨࠢᘉ")
    bstack1llllll11ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll1ll111l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l1l11_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᘊ").format(e)
                )
        try:
            if passed:
                bstack1ll1ll11l_opy_(getattr(item, bstack11l1l11_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᘋ"), None), bstack11l1l11_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᘌ"))
            else:
                error_message = bstack11l1l11_opy_ (u"ࠪࠫᘍ")
                if bstack1ll1ll111l_opy_:
                    bstack1ll1lll1ll_opy_(item._page, str(bstack1ll1ll111l_opy_), bstack11l1l11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥᘎ"))
                    bstack1ll1ll11l_opy_(getattr(item, bstack11l1l11_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᘏ"), None), bstack11l1l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᘐ"), str(bstack1ll1ll111l_opy_))
                    error_message = str(bstack1ll1ll111l_opy_)
                else:
                    bstack1ll1ll11l_opy_(getattr(item, bstack11l1l11_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᘑ"), None), bstack11l1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᘒ"))
                bstack1lll11l1111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11l1l11_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨᘓ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack11l1l11_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢᘔ"), default=bstack11l1l11_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᘕ"), help=bstack11l1l11_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦᘖ"))
    parser.addoption(bstack11l1l11_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧᘗ"), default=bstack11l1l11_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨᘘ"), help=bstack11l1l11_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢᘙ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11l1l11_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦᘚ"), action=bstack11l1l11_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤᘛ"), default=bstack11l1l11_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦᘜ"),
                         help=bstack11l1l11_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦᘝ"))
def bstack1l111lll1l_opy_(log):
    if not (log[bstack11l1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᘞ")] and log[bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᘟ")].strip()):
        return
    active = bstack11lll1l1l1_opy_()
    log = {
        bstack11l1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᘠ"): log[bstack11l1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᘡ")],
        bstack11l1l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᘢ"): datetime.datetime.utcnow().isoformat() + bstack11l1l11_opy_ (u"ࠫ࡟࠭ᘣ"),
        bstack11l1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᘤ"): log[bstack11l1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᘥ")],
    }
    if active:
        if active[bstack11l1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬᘦ")] == bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᘧ"):
            log[bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᘨ")] = active[bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᘩ")]
        elif active[bstack11l1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩᘪ")] == bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࠪᘫ"):
            log[bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᘬ")] = active[bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᘭ")]
    bstack1l11ll1l11_opy_.bstack1ll1l1l11l_opy_([log])
def bstack11lll1l1l1_opy_():
    if len(store[bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᘮ")]) > 0 and store[bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᘯ")][-1]:
        return {
            bstack11l1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨᘰ"): bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᘱ"),
            bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᘲ"): store[bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᘳ")][-1]
        }
    if store.get(bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᘴ"), None):
        return {
            bstack11l1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᘵ"): bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺࠧᘶ"),
            bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᘷ"): store[bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᘸ")]
        }
    return None
bstack11lll1l111_opy_ = bstack1l111l1l1l_opy_(bstack1l111lll1l_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lll11lll11_opy_
        item._1lll1l11111_opy_ = True
        bstack1l1l1ll1ll_opy_ = bstack111lllll_opy_.bstack1l1llll11_opy_(CONFIG, bstack11l11lll1l_opy_(item.own_markers))
        item._a11y_test_case = bstack1l1l1ll1ll_opy_
        if bstack1lll11lll11_opy_:
            driver = getattr(item, bstack11l1l11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᘹ"), None)
            item._a11y_started = bstack111lllll_opy_.bstack11l1ll1ll_opy_(driver, bstack1l1l1ll1ll_opy_)
        if not bstack1l11ll1l11_opy_.on() or bstack1lll111llll_opy_ != bstack11l1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᘺ"):
            return
        global current_test_uuid, bstack11lll1l111_opy_
        bstack11lll1l111_opy_.start()
        bstack1l111ll1ll_opy_ = {
            bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᘻ"): uuid4().__str__(),
            bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᘼ"): datetime.datetime.utcnow().isoformat() + bstack11l1l11_opy_ (u"ࠩ࡝ࠫᘽ")
        }
        current_test_uuid = bstack1l111ll1ll_opy_[bstack11l1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᘾ")]
        store[bstack11l1l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᘿ")] = bstack1l111ll1ll_opy_[bstack11l1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪᙀ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l1111lll1_opy_[item.nodeid] = {**_1l1111lll1_opy_[item.nodeid], **bstack1l111ll1ll_opy_}
        bstack1lll11ll1ll_opy_(item, _1l1111lll1_opy_[item.nodeid], bstack11l1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᙁ"))
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩᙂ"), str(err))
def pytest_runtest_setup(item):
    global bstack1lll1l11lll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l11ll11l_opy_():
        atexit.register(bstack1ll11111l_opy_)
        if not bstack1lll1l11lll_opy_:
            try:
                bstack1lll1l11l11_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111ll11l1l_opy_():
                    bstack1lll1l11l11_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lll1l11l11_opy_:
                    signal.signal(s, bstack1lll1l1111l_opy_)
                bstack1lll1l11lll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11l1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤᙃ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lllll1lll1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11l1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᙄ")
    try:
        if not bstack1l11ll1l11_opy_.on():
            return
        bstack11lll1l111_opy_.start()
        uuid = uuid4().__str__()
        bstack1l111ll1ll_opy_ = {
            bstack11l1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᙅ"): uuid,
            bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᙆ"): datetime.datetime.utcnow().isoformat() + bstack11l1l11_opy_ (u"ࠬࡠࠧᙇ"),
            bstack11l1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫᙈ"): bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᙉ"),
            bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᙊ"): bstack11l1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᙋ"),
            bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᙌ"): bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᙍ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᙎ")] = item
        store[bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᙏ")] = [uuid]
        if not _1l1111lll1_opy_.get(item.nodeid, None):
            _1l1111lll1_opy_[item.nodeid] = {bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᙐ"): [], bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᙑ"): []}
        _1l1111lll1_opy_[item.nodeid][bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᙒ")].append(bstack1l111ll1ll_opy_[bstack11l1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᙓ")])
        _1l1111lll1_opy_[item.nodeid + bstack11l1l11_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫᙔ")] = bstack1l111ll1ll_opy_
        bstack1lll11llll1_opy_(item, bstack1l111ll1ll_opy_, bstack11l1l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᙕ"))
    except Exception as err:
        print(bstack11l1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩᙖ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack111l1l111_opy_
        if CONFIG.get(bstack11l1l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᙗ"), False):
            if CONFIG.get(bstack11l1l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᙘ"), bstack11l1l11_opy_ (u"ࠤࡤࡹࡹࡵࠢᙙ")) == bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᙚ"):
                bstack1lll1l1ll11_opy_ = bstack1111lll1l_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᙛ"), None)
                bstack1l11l1l111_opy_ = bstack1lll1l1ll11_opy_ + bstack11l1l11_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣᙜ")
                driver = getattr(item, bstack11l1l11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᙝ"), None)
                PercySDK.screenshot(driver, bstack1l11l1l111_opy_)
        if getattr(item, bstack11l1l11_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡣࡵࡸࡪࡪࠧᙞ"), False):
            bstack1ll1ll11_opy_.bstack1l11llll1_opy_(getattr(item, bstack11l1l11_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᙟ"), None), bstack111l1l111_opy_, logger, item)
        if not bstack1l11ll1l11_opy_.on():
            return
        bstack1l111ll1ll_opy_ = {
            bstack11l1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᙠ"): uuid4().__str__(),
            bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᙡ"): datetime.datetime.utcnow().isoformat() + bstack11l1l11_opy_ (u"ࠫ࡟࠭ᙢ"),
            bstack11l1l11_opy_ (u"ࠬࡺࡹࡱࡧࠪᙣ"): bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᙤ"),
            bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᙥ"): bstack11l1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᙦ"),
            bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬᙧ"): bstack11l1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᙨ")
        }
        _1l1111lll1_opy_[item.nodeid + bstack11l1l11_opy_ (u"ࠫ࠲ࡺࡥࡢࡴࡧࡳࡼࡴࠧᙩ")] = bstack1l111ll1ll_opy_
        bstack1lll11llll1_opy_(item, bstack1l111ll1ll_opy_, bstack11l1l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᙪ"))
    except Exception as err:
        print(bstack11l1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮࠻ࠢࡾࢁࠬᙫ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l11ll1l11_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1llllll1ll1_opy_(fixturedef.argname):
        store[bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭ᙬ")] = request.node
    elif bstack1llllll11l1_opy_(fixturedef.argname):
        store[bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭᙭")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11l1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᙮"): fixturedef.argname,
            bstack11l1l11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᙯ"): bstack11l11ll111_opy_(outcome),
            bstack11l1l11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᙰ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᙱ")]
        if not _1l1111lll1_opy_.get(current_test_item.nodeid, None):
            _1l1111lll1_opy_[current_test_item.nodeid] = {bstack11l1l11_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᙲ"): []}
        _1l1111lll1_opy_[current_test_item.nodeid][bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᙳ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11l1l11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫᙴ"), str(err))
if bstack1l1l11l11l_opy_() and bstack1l11ll1l11_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l1111lll1_opy_[request.node.nodeid][bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᙵ")].bstack1llll11lll1_opy_(id(step))
        except Exception as err:
            print(bstack11l1l11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳ࠾ࠥࢁࡽࠨᙶ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l1111lll1_opy_[request.node.nodeid][bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᙷ")].bstack1l11l1111l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11l1l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩᙸ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11llll1111_opy_: bstack1l111llll1_opy_ = _1l1111lll1_opy_[request.node.nodeid][bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᙹ")]
            bstack11llll1111_opy_.bstack1l11l1111l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11l1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡷࡹ࡫ࡰࡠࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫᙺ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lll111llll_opy_
        try:
            if not bstack1l11ll1l11_opy_.on() or bstack1lll111llll_opy_ != bstack11l1l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᙻ"):
                return
            global bstack11lll1l111_opy_
            bstack11lll1l111_opy_.start()
            driver = bstack1111lll1l_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨᙼ"), None)
            if not _1l1111lll1_opy_.get(request.node.nodeid, None):
                _1l1111lll1_opy_[request.node.nodeid] = {}
            bstack11llll1111_opy_ = bstack1l111llll1_opy_.bstack1llll1l11l1_opy_(
                scenario, feature, request.node,
                name=bstack1llllll1l11_opy_(request.node, scenario),
                bstack1l111lll11_opy_=bstack1l1lll111_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11l1l11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᙽ"),
                tags=bstack1lllll1ll11_opy_(feature, scenario),
                bstack1l11111lll_opy_=bstack1l11ll1l11_opy_.bstack11llll1l11_opy_(driver) if driver and driver.session_id else {}
            )
            _1l1111lll1_opy_[request.node.nodeid][bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᙾ")] = bstack11llll1111_opy_
            bstack1lll1l11l1l_opy_(bstack11llll1111_opy_.uuid)
            bstack1l11ll1l11_opy_.bstack1l1111ll1l_opy_(bstack11l1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᙿ"), bstack11llll1111_opy_)
        except Exception as err:
            print(bstack11l1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨ "), str(err))
def bstack1lll111ll11_opy_(bstack1lll1l1l1ll_opy_):
    if bstack1lll1l1l1ll_opy_ in store[bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᚁ")]:
        store[bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᚂ")].remove(bstack1lll1l1l1ll_opy_)
def bstack1lll1l11l1l_opy_(bstack1lll11l1l11_opy_):
    store[bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᚃ")] = bstack1lll11l1l11_opy_
    threading.current_thread().current_test_uuid = bstack1lll11l1l11_opy_
@bstack1l11ll1l11_opy_.bstack1llll11111l_opy_
def bstack1lll1l111l1_opy_(item, call, report):
    global bstack1lll111llll_opy_
    bstack1ll1l111l_opy_ = bstack1l1lll111_opy_()
    if hasattr(report, bstack11l1l11_opy_ (u"ࠪࡷࡹࡵࡰࠨᚄ")):
        bstack1ll1l111l_opy_ = bstack111ll1l1ll_opy_(report.stop)
    elif hasattr(report, bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࠪᚅ")):
        bstack1ll1l111l_opy_ = bstack111ll1l1ll_opy_(report.start)
    try:
        if getattr(report, bstack11l1l11_opy_ (u"ࠬࡽࡨࡦࡰࠪᚆ"), bstack11l1l11_opy_ (u"࠭ࠧᚇ")) == bstack11l1l11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᚈ"):
            bstack11lll1l111_opy_.reset()
        if getattr(report, bstack11l1l11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᚉ"), bstack11l1l11_opy_ (u"ࠩࠪᚊ")) == bstack11l1l11_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᚋ"):
            if bstack1lll111llll_opy_ == bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᚌ"):
                _1l1111lll1_opy_[item.nodeid][bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᚍ")] = bstack1ll1l111l_opy_
                bstack1lll11ll1ll_opy_(item, _1l1111lll1_opy_[item.nodeid], bstack11l1l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᚎ"), report, call)
                store[bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᚏ")] = None
            elif bstack1lll111llll_opy_ == bstack11l1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᚐ"):
                bstack11llll1111_opy_ = _1l1111lll1_opy_[item.nodeid][bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᚑ")]
                bstack11llll1111_opy_.set(hooks=_1l1111lll1_opy_[item.nodeid].get(bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᚒ"), []))
                exception, bstack11lll1ll11_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11lll1ll11_opy_ = [call.excinfo.exconly(), getattr(report, bstack11l1l11_opy_ (u"ࠫࡱࡵ࡮ࡨࡴࡨࡴࡷࡺࡥࡹࡶࠪᚓ"), bstack11l1l11_opy_ (u"ࠬ࠭ᚔ"))]
                bstack11llll1111_opy_.stop(time=bstack1ll1l111l_opy_, result=Result(result=getattr(report, bstack11l1l11_opy_ (u"࠭࡯ࡶࡶࡦࡳࡲ࡫ࠧᚕ"), bstack11l1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᚖ")), exception=exception, bstack11lll1ll11_opy_=bstack11lll1ll11_opy_))
                bstack1l11ll1l11_opy_.bstack1l1111ll1l_opy_(bstack11l1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᚗ"), _1l1111lll1_opy_[item.nodeid][bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᚘ")])
        elif getattr(report, bstack11l1l11_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᚙ"), bstack11l1l11_opy_ (u"ࠫࠬᚚ")) in [bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ᚛"), bstack11l1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ᚜")]:
            bstack11llll11l1_opy_ = item.nodeid + bstack11l1l11_opy_ (u"ࠧ࠮ࠩ᚝") + getattr(report, bstack11l1l11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭᚞"), bstack11l1l11_opy_ (u"ࠩࠪ᚟"))
            if getattr(report, bstack11l1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᚠ"), False):
                hook_type = bstack11l1l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᚡ") if getattr(report, bstack11l1l11_opy_ (u"ࠬࡽࡨࡦࡰࠪᚢ"), bstack11l1l11_opy_ (u"࠭ࠧᚣ")) == bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᚤ") else bstack11l1l11_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᚥ")
                _1l1111lll1_opy_[bstack11llll11l1_opy_] = {
                    bstack11l1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᚦ"): uuid4().__str__(),
                    bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᚧ"): bstack1ll1l111l_opy_,
                    bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᚨ"): hook_type
                }
            _1l1111lll1_opy_[bstack11llll11l1_opy_][bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᚩ")] = bstack1ll1l111l_opy_
            bstack1lll111ll11_opy_(_1l1111lll1_opy_[bstack11llll11l1_opy_][bstack11l1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᚪ")])
            bstack1lll11llll1_opy_(item, _1l1111lll1_opy_[bstack11llll11l1_opy_], bstack11l1l11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᚫ"), report, call)
            if getattr(report, bstack11l1l11_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᚬ"), bstack11l1l11_opy_ (u"ࠩࠪᚭ")) == bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᚮ"):
                if getattr(report, bstack11l1l11_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬᚯ"), bstack11l1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᚰ")) == bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᚱ"):
                    bstack1l111ll1ll_opy_ = {
                        bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᚲ"): uuid4().__str__(),
                        bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᚳ"): bstack1l1lll111_opy_(),
                        bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᚴ"): bstack1l1lll111_opy_()
                    }
                    _1l1111lll1_opy_[item.nodeid] = {**_1l1111lll1_opy_[item.nodeid], **bstack1l111ll1ll_opy_}
                    bstack1lll11ll1ll_opy_(item, _1l1111lll1_opy_[item.nodeid], bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᚵ"))
                    bstack1lll11ll1ll_opy_(item, _1l1111lll1_opy_[item.nodeid], bstack11l1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᚶ"), report, call)
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪᚷ"), str(err))
def bstack1lll11ll1l1_opy_(test, bstack1l111ll1ll_opy_, result=None, call=None, bstack111l111l1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11llll1111_opy_ = {
        bstack11l1l11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᚸ"): bstack1l111ll1ll_opy_[bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᚹ")],
        bstack11l1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᚺ"): bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺࠧᚻ"),
        bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᚼ"): test.name,
        bstack11l1l11_opy_ (u"ࠫࡧࡵࡤࡺࠩᚽ"): {
            bstack11l1l11_opy_ (u"ࠬࡲࡡ࡯ࡩࠪᚾ"): bstack11l1l11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᚿ"),
            bstack11l1l11_opy_ (u"ࠧࡤࡱࡧࡩࠬᛀ"): inspect.getsource(test.obj)
        },
        bstack11l1l11_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᛁ"): test.name,
        bstack11l1l11_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨᛂ"): test.name,
        bstack11l1l11_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᛃ"): bstack1l11ll1l11_opy_.bstack1l1111l1ll_opy_(test),
        bstack11l1l11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᛄ"): file_path,
        bstack11l1l11_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᛅ"): file_path,
        bstack11l1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᛆ"): bstack11l1l11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᛇ"),
        bstack11l1l11_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᛈ"): file_path,
        bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᛉ"): bstack1l111ll1ll_opy_[bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᛊ")],
        bstack11l1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᛋ"): bstack11l1l11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬᛌ"),
        bstack11l1l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩᛍ"): {
            bstack11l1l11_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫᛎ"): test.nodeid
        },
        bstack11l1l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᛏ"): bstack11l11lll1l_opy_(test.own_markers)
    }
    if bstack111l111l1_opy_ in [bstack11l1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᛐ"), bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᛑ")]:
        bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᛒ")] = {
            bstack11l1l11_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᛓ"): bstack1l111ll1ll_opy_.get(bstack11l1l11_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᛔ"), [])
        }
    if bstack111l111l1_opy_ == bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᛕ"):
        bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᛖ")] = bstack11l1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᛗ")
        bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᛘ")] = bstack1l111ll1ll_opy_[bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᛙ")]
        bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᛚ")] = bstack1l111ll1ll_opy_[bstack11l1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᛛ")]
    if result:
        bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᛜ")] = result.outcome
        bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᛝ")] = result.duration * 1000
        bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᛞ")] = bstack1l111ll1ll_opy_[bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᛟ")]
        if result.failed:
            bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᛠ")] = bstack1l11ll1l11_opy_.bstack11ll1l11l1_opy_(call.excinfo.typename)
            bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᛡ")] = bstack1l11ll1l11_opy_.bstack1lll1ll1l1l_opy_(call.excinfo, result)
        bstack11llll1111_opy_[bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᛢ")] = bstack1l111ll1ll_opy_[bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᛣ")]
    if outcome:
        bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᛤ")] = bstack11l11ll111_opy_(outcome)
        bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᛥ")] = 0
        bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᛦ")] = bstack1l111ll1ll_opy_[bstack11l1l11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᛧ")]
        if bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᛨ")] == bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᛩ"):
            bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᛪ")] = bstack11l1l11_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩ᛫")  # bstack1lll1l1l111_opy_
            bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ᛬")] = [{bstack11l1l11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭᛭"): [bstack11l1l11_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨᛮ")]}]
        bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᛯ")] = bstack1l111ll1ll_opy_[bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᛰ")]
    return bstack11llll1111_opy_
def bstack1lll11l111l_opy_(test, bstack11lll11lll_opy_, bstack111l111l1_opy_, result, call, outcome, bstack1lll1l1lll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11lll11lll_opy_[bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᛱ")]
    hook_name = bstack11lll11lll_opy_[bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᛲ")]
    hook_data = {
        bstack11l1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᛳ"): bstack11lll11lll_opy_[bstack11l1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᛴ")],
        bstack11l1l11_opy_ (u"ࠫࡹࡿࡰࡦࠩᛵ"): bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᛶ"),
        bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᛷ"): bstack11l1l11_opy_ (u"ࠧࡼࡿࠪᛸ").format(bstack1lllll1ll1l_opy_(hook_name)),
        bstack11l1l11_opy_ (u"ࠨࡤࡲࡨࡾ࠭᛹"): {
            bstack11l1l11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧ᛺"): bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ᛻"),
            bstack11l1l11_opy_ (u"ࠫࡨࡵࡤࡦࠩ᛼"): None
        },
        bstack11l1l11_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫ᛽"): test.name,
        bstack11l1l11_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭᛾"): bstack1l11ll1l11_opy_.bstack1l1111l1ll_opy_(test, hook_name),
        bstack11l1l11_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ᛿"): file_path,
        bstack11l1l11_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᜀ"): file_path,
        bstack11l1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᜁ"): bstack11l1l11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᜂ"),
        bstack11l1l11_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᜃ"): file_path,
        bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᜄ"): bstack11lll11lll_opy_[bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᜅ")],
        bstack11l1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᜆ"): bstack11l1l11_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᜇ") if bstack1lll111llll_opy_ == bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᜈ") else bstack11l1l11_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᜉ"),
        bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᜊ"): hook_type
    }
    bstack1lll11l11ll_opy_ = bstack1l11111ll1_opy_(_1l1111lll1_opy_.get(test.nodeid, None))
    if bstack1lll11l11ll_opy_:
        hook_data[bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪᜋ")] = bstack1lll11l11ll_opy_
    if result:
        hook_data[bstack11l1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᜌ")] = result.outcome
        hook_data[bstack11l1l11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᜍ")] = result.duration * 1000
        hook_data[bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᜎ")] = bstack11lll11lll_opy_[bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᜏ")]
        if result.failed:
            hook_data[bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᜐ")] = bstack1l11ll1l11_opy_.bstack11ll1l11l1_opy_(call.excinfo.typename)
            hook_data[bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᜑ")] = bstack1l11ll1l11_opy_.bstack1lll1ll1l1l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11l1l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᜒ")] = bstack11l11ll111_opy_(outcome)
        hook_data[bstack11l1l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᜓ")] = 100
        hook_data[bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸ᜔ࠬ")] = bstack11lll11lll_opy_[bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ᜕࠭")]
        if hook_data[bstack11l1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᜖")] == bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᜗"):
            hook_data[bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ᜘")] = bstack11l1l11_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭᜙")  # bstack1lll1l1l111_opy_
            hook_data[bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧ᜚")] = [{bstack11l1l11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ᜛"): [bstack11l1l11_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬ᜜")]}]
    if bstack1lll1l1lll1_opy_:
        hook_data[bstack11l1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᜝")] = bstack1lll1l1lll1_opy_.result
        hook_data[bstack11l1l11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ᜞")] = bstack11l1111l1l_opy_(bstack11lll11lll_opy_[bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᜟ")], bstack11lll11lll_opy_[bstack11l1l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᜠ")])
        hook_data[bstack11l1l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᜡ")] = bstack11lll11lll_opy_[bstack11l1l11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᜢ")]
        if hook_data[bstack11l1l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᜣ")] == bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᜤ"):
            hook_data[bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᜥ")] = bstack1l11ll1l11_opy_.bstack11ll1l11l1_opy_(bstack1lll1l1lll1_opy_.exception_type)
            hook_data[bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᜦ")] = [{bstack11l1l11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᜧ"): bstack111ll1lll1_opy_(bstack1lll1l1lll1_opy_.exception)}]
    return hook_data
def bstack1lll11ll1ll_opy_(test, bstack1l111ll1ll_opy_, bstack111l111l1_opy_, result=None, call=None, outcome=None):
    bstack11llll1111_opy_ = bstack1lll11ll1l1_opy_(test, bstack1l111ll1ll_opy_, result, call, bstack111l111l1_opy_, outcome)
    driver = getattr(test, bstack11l1l11_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᜨ"), None)
    if bstack111l111l1_opy_ == bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᜩ") and driver:
        bstack11llll1111_opy_[bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᜪ")] = bstack1l11ll1l11_opy_.bstack11llll1l11_opy_(driver)
    if bstack111l111l1_opy_ == bstack11l1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᜫ"):
        bstack111l111l1_opy_ = bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᜬ")
    bstack11llllll11_opy_ = {
        bstack11l1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᜭ"): bstack111l111l1_opy_,
        bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᜮ"): bstack11llll1111_opy_
    }
    bstack1l11ll1l11_opy_.bstack1l111l11ll_opy_(bstack11llllll11_opy_)
def bstack1lll11llll1_opy_(test, bstack1l111ll1ll_opy_, bstack111l111l1_opy_, result=None, call=None, outcome=None, bstack1lll1l1lll1_opy_=None):
    hook_data = bstack1lll11l111l_opy_(test, bstack1l111ll1ll_opy_, bstack111l111l1_opy_, result, call, outcome, bstack1lll1l1lll1_opy_)
    bstack11llllll11_opy_ = {
        bstack11l1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᜯ"): bstack111l111l1_opy_,
        bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩᜰ"): hook_data
    }
    bstack1l11ll1l11_opy_.bstack1l111l11ll_opy_(bstack11llllll11_opy_)
def bstack1l11111ll1_opy_(bstack1l111ll1ll_opy_):
    if not bstack1l111ll1ll_opy_:
        return None
    if bstack1l111ll1ll_opy_.get(bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᜱ"), None):
        return getattr(bstack1l111ll1ll_opy_[bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᜲ")], bstack11l1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᜳ"), None)
    return bstack1l111ll1ll_opy_.get(bstack11l1l11_opy_ (u"ࠫࡺࡻࡩࡥ᜴ࠩ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l11ll1l11_opy_.on():
            return
        places = [bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ᜵"), bstack11l1l11_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ᜶"), bstack11l1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ᜷")]
        bstack11llllll1l_opy_ = []
        for bstack1lll1l1l1l1_opy_ in places:
            records = caplog.get_records(bstack1lll1l1l1l1_opy_)
            bstack1lll11lllll_opy_ = bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᜸") if bstack1lll1l1l1l1_opy_ == bstack11l1l11_opy_ (u"ࠩࡦࡥࡱࡲࠧ᜹") else bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᜺")
            bstack1lll11l11l1_opy_ = request.node.nodeid + (bstack11l1l11_opy_ (u"ࠫࠬ᜻") if bstack1lll1l1l1l1_opy_ == bstack11l1l11_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ᜼") else bstack11l1l11_opy_ (u"࠭࠭ࠨ᜽") + bstack1lll1l1l1l1_opy_)
            bstack1lll11l1l11_opy_ = bstack1l11111ll1_opy_(_1l1111lll1_opy_.get(bstack1lll11l11l1_opy_, None))
            if not bstack1lll11l1l11_opy_:
                continue
            for record in records:
                if bstack11l111ll11_opy_(record.message):
                    continue
                bstack11llllll1l_opy_.append({
                    bstack11l1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ᜾"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack11l1l11_opy_ (u"ࠨ࡜ࠪ᜿"),
                    bstack11l1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᝀ"): record.levelname,
                    bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᝁ"): record.message,
                    bstack1lll11lllll_opy_: bstack1lll11l1l11_opy_
                })
        if len(bstack11llllll1l_opy_) > 0:
            bstack1l11ll1l11_opy_.bstack1ll1l1l11l_opy_(bstack11llllll1l_opy_)
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡩ࡯࡯ࡦࡢࡪ࡮ࡾࡴࡶࡴࡨ࠾ࠥࢁࡽࠨᝂ"), str(err))
def bstack1l11ll11l1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack111lllll1_opy_
    bstack1ll11llll_opy_ = bstack1111lll1l_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᝃ"), None) and bstack1111lll1l_opy_(
            threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᝄ"), None)
    bstack1ll1l1l1_opy_ = getattr(driver, bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧᝅ"), None) != None and getattr(driver, bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨᝆ"), None) == True
    if sequence == bstack11l1l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᝇ") and driver != None:
      if not bstack111lllll1_opy_ and bstack111lllll1l_opy_() and bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᝈ") in CONFIG and CONFIG[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᝉ")] == True and bstack1l1ll111ll_opy_.bstack1lll11ll1_opy_(driver_command) and (bstack1ll1l1l1_opy_ or bstack1ll11llll_opy_) and not bstack1lll11111_opy_(args):
        try:
          bstack111lllll1_opy_ = True
          logger.debug(bstack11l1l11_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧᝊ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11l1l11_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫᝋ").format(str(err)))
        bstack111lllll1_opy_ = False
    if sequence == bstack11l1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᝌ"):
        if driver_command == bstack11l1l11_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬᝍ"):
            bstack1l11ll1l11_opy_.bstack1lll1111l1_opy_({
                bstack11l1l11_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨᝎ"): response[bstack11l1l11_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩᝏ")],
                bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᝐ"): store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᝑ")]
            })
def bstack1ll11111l_opy_():
    global bstack1lll1l111l_opy_
    bstack1ll1ll1lll_opy_.bstack1l1l111l_opy_()
    logging.shutdown()
    bstack1l11ll1l11_opy_.bstack1l11111l11_opy_()
    for driver in bstack1lll1l111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1l1111l_opy_(*args):
    global bstack1lll1l111l_opy_
    bstack1l11ll1l11_opy_.bstack1l11111l11_opy_()
    for driver in bstack1lll1l111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1111llll1_opy_(self, *args, **kwargs):
    bstack1l1l1lllll_opy_ = bstack1lll11llll_opy_(self, *args, **kwargs)
    bstack1l11ll1l11_opy_.bstack1ll111l1l_opy_(self)
    return bstack1l1l1lllll_opy_
def bstack11ll11l1_opy_(framework_name):
    global bstack1lll1ll1_opy_
    global bstack11llll11l_opy_
    bstack1lll1ll1_opy_ = framework_name
    logger.info(bstack1l1ll1ll11_opy_.format(bstack1lll1ll1_opy_.split(bstack11l1l11_opy_ (u"࠭࠭ࠨᝒ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack111lllll1l_opy_():
            Service.start = bstack1lll11ll1l_opy_
            Service.stop = bstack111l1ll1_opy_
            webdriver.Remote.__init__ = bstack1lllllll11_opy_
            webdriver.Remote.get = bstack11ll1l111_opy_
            if not isinstance(os.getenv(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨᝓ")), str):
                return
            WebDriver.close = bstack1l1ll11111_opy_
            WebDriver.quit = bstack1l1ll11l11_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack111lllll1l_opy_() and bstack1l11ll1l11_opy_.on():
            webdriver.Remote.__init__ = bstack1111llll1_opy_
        bstack11llll11l_opy_ = True
    except Exception as e:
        pass
    bstack1llll1ll1_opy_()
    if os.environ.get(bstack11l1l11_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭᝔")):
        bstack11llll11l_opy_ = eval(os.environ.get(bstack11l1l11_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧ᝕")))
    if not bstack11llll11l_opy_:
        bstack1llll11ll_opy_(bstack11l1l11_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧ᝖"), bstack1l1l1ll11_opy_)
    if bstack1ll111l11l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1llll1l11l_opy_
        except Exception as e:
            logger.error(bstack11ll111l1_opy_.format(str(e)))
    if bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᝗") in str(framework_name).lower():
        if not bstack111lllll1l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll11ll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11ll1ll1_opy_
            Config.getoption = bstack1111lll11_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack111l1l1l1_opy_
        except Exception as e:
            pass
def bstack1l1ll11l11_opy_(self):
    global bstack1lll1ll1_opy_
    global bstack1l11lllll1_opy_
    global bstack1l1l11llll_opy_
    try:
        if bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᝘") in bstack1lll1ll1_opy_ and self.session_id != None and bstack1111lll1l_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪ᝙"), bstack11l1l11_opy_ (u"ࠧࠨ᝚")) != bstack11l1l11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ᝛"):
            bstack1l1lll1lll_opy_ = bstack11l1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ᝜") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᝝")
            bstack1l11ll11l_opy_(logger, True)
            if self != None:
                bstack1l111l111_opy_(self, bstack1l1lll1lll_opy_, bstack11l1l11_opy_ (u"ࠫ࠱ࠦࠧ᝞").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ᝟"), None)
        if item is not None and bstack1lll11lll11_opy_:
            bstack1ll1ll11_opy_.bstack1l11llll1_opy_(self, bstack111l1l111_opy_, logger, item)
        threading.current_thread().testStatus = bstack11l1l11_opy_ (u"࠭ࠧᝠ")
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣᝡ") + str(e))
    bstack1l1l11llll_opy_(self)
    self.session_id = None
def bstack1lllllll11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l11lllll1_opy_
    global bstack1l1lll1l1_opy_
    global bstack111111ll1_opy_
    global bstack1lll1ll1_opy_
    global bstack1lll11llll_opy_
    global bstack1lll1l111l_opy_
    global bstack1ll11ll11_opy_
    global bstack1111l1ll_opy_
    global bstack1lll11lll11_opy_
    global bstack111l1l111_opy_
    CONFIG[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᝢ")] = str(bstack1lll1ll1_opy_) + str(__version__)
    command_executor = bstack1l1l11l111_opy_(bstack1ll11ll11_opy_)
    logger.debug(bstack1l1l11l1l_opy_.format(command_executor))
    proxy = bstack1ll1l11lll_opy_(CONFIG, proxy)
    bstack1111lll1_opy_ = 0
    try:
        if bstack111111ll1_opy_ is True:
            bstack1111lll1_opy_ = int(os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᝣ")))
    except:
        bstack1111lll1_opy_ = 0
    bstack1ll1lll11l_opy_ = bstack1l11l1l1l1_opy_(CONFIG, bstack1111lll1_opy_)
    logger.debug(bstack1ll1ll1111_opy_.format(str(bstack1ll1lll11l_opy_)))
    bstack111l1l111_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᝤ"))[bstack1111lll1_opy_]
    if bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᝥ") in CONFIG and CONFIG[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᝦ")]:
        bstack1111l1l1l_opy_(bstack1ll1lll11l_opy_, bstack1111l1ll_opy_)
    if bstack111lllll_opy_.bstack11l11l1l1_opy_(CONFIG, bstack1111lll1_opy_) and bstack111lllll_opy_.bstack11111ll1_opy_(bstack1ll1lll11l_opy_, options):
        bstack1lll11lll11_opy_ = True
        bstack111lllll_opy_.set_capabilities(bstack1ll1lll11l_opy_, CONFIG)
    if desired_capabilities:
        bstack1l1llll1_opy_ = bstack1l1lll1l11_opy_(desired_capabilities)
        bstack1l1llll1_opy_[bstack11l1l11_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᝧ")] = bstack1l1l1l1l1l_opy_(CONFIG)
        bstack1111l1l1_opy_ = bstack1l11l1l1l1_opy_(bstack1l1llll1_opy_)
        if bstack1111l1l1_opy_:
            bstack1ll1lll11l_opy_ = update(bstack1111l1l1_opy_, bstack1ll1lll11l_opy_)
        desired_capabilities = None
    if options:
        bstack11l1l111l_opy_(options, bstack1ll1lll11l_opy_)
    if not options:
        options = bstack1l111lll_opy_(bstack1ll1lll11l_opy_)
    if proxy and bstack11l111ll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᝨ")):
        options.proxy(proxy)
    if options and bstack11l111ll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᝩ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11l111ll_opy_() < version.parse(bstack11l1l11_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᝪ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll1lll11l_opy_)
    logger.info(bstack11ll111ll_opy_)
    if bstack11l111ll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪᝫ")):
        bstack1lll11llll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l111ll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᝬ")):
        bstack1lll11llll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l111ll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬ᝭")):
        bstack1lll11llll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1lll11llll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1ll1ll1ll1_opy_ = bstack11l1l11_opy_ (u"࠭ࠧᝮ")
        if bstack11l111ll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨᝯ")):
            bstack1ll1ll1ll1_opy_ = self.caps.get(bstack11l1l11_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣᝰ"))
        else:
            bstack1ll1ll1ll1_opy_ = self.capabilities.get(bstack11l1l11_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤ᝱"))
        if bstack1ll1ll1ll1_opy_:
            bstack1ll11l111l_opy_(bstack1ll1ll1ll1_opy_)
            if bstack11l111ll_opy_() <= version.parse(bstack11l1l11_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪᝲ")):
                self.command_executor._url = bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᝳ") + bstack1ll11ll11_opy_ + bstack11l1l11_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤ᝴")
            else:
                self.command_executor._url = bstack11l1l11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣ᝵") + bstack1ll1ll1ll1_opy_ + bstack11l1l11_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣ᝶")
            logger.debug(bstack1l1ll11l_opy_.format(bstack1ll1ll1ll1_opy_))
        else:
            logger.debug(bstack1llll1l1l_opy_.format(bstack11l1l11_opy_ (u"ࠣࡑࡳࡸ࡮ࡳࡡ࡭ࠢࡋࡹࡧࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤ᝷")))
    except Exception as e:
        logger.debug(bstack1llll1l1l_opy_.format(e))
    bstack1l11lllll1_opy_ = self.session_id
    if bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᝸") in bstack1lll1ll1_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11l1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ᝹"), None)
        if item:
            bstack1lll11lll1l_opy_ = getattr(item, bstack11l1l11_opy_ (u"ࠫࡤࡺࡥࡴࡶࡢࡧࡦࡹࡥࡠࡵࡷࡥࡷࡺࡥࡥࠩ᝺"), False)
            if not getattr(item, bstack11l1l11_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭᝻"), None) and bstack1lll11lll1l_opy_:
                setattr(store[bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ᝼")], bstack11l1l11_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ᝽"), self)
        bstack1l11ll1l11_opy_.bstack1ll111l1l_opy_(self)
    bstack1lll1l111l_opy_.append(self)
    if bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᝾") in CONFIG and bstack11l1l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᝿") in CONFIG[bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ក")][bstack1111lll1_opy_]:
        bstack1l1lll1l1_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧខ")][bstack1111lll1_opy_][bstack11l1l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪគ")]
    logger.debug(bstack111lll1l1_opy_.format(bstack1l11lllll1_opy_))
def bstack11ll1l111_opy_(self, url):
    global bstack11ll1llll_opy_
    global CONFIG
    try:
        bstack1l1ll11lll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1l11l1ll_opy_.format(str(err)))
    try:
        bstack11ll1llll_opy_(self, url)
    except Exception as e:
        try:
            bstack1lll1l11_opy_ = str(e)
            if any(err_msg in bstack1lll1l11_opy_ for err_msg in bstack1ll1lllll_opy_):
                bstack1l1ll11lll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1l11l1ll_opy_.format(str(err)))
        raise e
def bstack111l111ll_opy_(item, when):
    global bstack1l1ll1l111_opy_
    try:
        bstack1l1ll1l111_opy_(item, when)
    except Exception as e:
        pass
def bstack111l1l1l1_opy_(item, call, rep):
    global bstack11lll11l_opy_
    global bstack1lll1l111l_opy_
    name = bstack11l1l11_opy_ (u"࠭ࠧឃ")
    try:
        if rep.when == bstack11l1l11_opy_ (u"ࠧࡤࡣ࡯ࡰࠬង"):
            bstack1l11lllll1_opy_ = threading.current_thread().bstackSessionId
            bstack1lll111lll1_opy_ = item.config.getoption(bstack11l1l11_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪច"))
            try:
                if (str(bstack1lll111lll1_opy_).lower() != bstack11l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧឆ")):
                    name = str(rep.nodeid)
                    bstack1l11l1l11_opy_ = bstack111lll1ll_opy_(bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫជ"), name, bstack11l1l11_opy_ (u"ࠫࠬឈ"), bstack11l1l11_opy_ (u"ࠬ࠭ញ"), bstack11l1l11_opy_ (u"࠭ࠧដ"), bstack11l1l11_opy_ (u"ࠧࠨឋ"))
                    os.environ[bstack11l1l11_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫឌ")] = name
                    for driver in bstack1lll1l111l_opy_:
                        if bstack1l11lllll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l11l1l11_opy_)
            except Exception as e:
                logger.debug(bstack11l1l11_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩឍ").format(str(e)))
            try:
                bstack11l11111l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11l1l11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫណ"):
                    status = bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫត") if rep.outcome.lower() == bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬថ") else bstack11l1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ទ")
                    reason = bstack11l1l11_opy_ (u"ࠧࠨធ")
                    if status == bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨន"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11l1l11_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧប") if status == bstack11l1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪផ") else bstack11l1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪព")
                    data = name + bstack11l1l11_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧភ") if status == bstack11l1l11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ម") else name + bstack11l1l11_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪយ") + reason
                    bstack1lll111l1l_opy_ = bstack111lll1ll_opy_(bstack11l1l11_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪរ"), bstack11l1l11_opy_ (u"ࠩࠪល"), bstack11l1l11_opy_ (u"ࠪࠫវ"), bstack11l1l11_opy_ (u"ࠫࠬឝ"), level, data)
                    for driver in bstack1lll1l111l_opy_:
                        if bstack1l11lllll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll111l1l_opy_)
            except Exception as e:
                logger.debug(bstack11l1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩឞ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪស").format(str(e)))
    bstack11lll11l_opy_(item, call, rep)
notset = Notset()
def bstack1111lll11_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11llll1ll_opy_
    if str(name).lower() == bstack11l1l11_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧហ"):
        return bstack11l1l11_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢឡ")
    else:
        return bstack11llll1ll_opy_(self, name, default, skip)
def bstack1llll1l11l_opy_(self):
    global CONFIG
    global bstack1l1l111111_opy_
    try:
        proxy = bstack1lll1l11ll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11l1l11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧអ")):
                proxies = bstack1l1l1ll1_opy_(proxy, bstack1l1l11l111_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll1lll1l_opy_ = proxies.popitem()
                    if bstack11l1l11_opy_ (u"ࠥ࠾࠴࠵ࠢឣ") in bstack1ll1lll1l_opy_:
                        return bstack1ll1lll1l_opy_
                    else:
                        return bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧឤ") + bstack1ll1lll1l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11l1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤឥ").format(str(e)))
    return bstack1l1l111111_opy_(self)
def bstack1ll111l11l_opy_():
    return (bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩឦ") in CONFIG or bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫឧ") in CONFIG) and bstack1l1l1llll_opy_() and bstack11l111ll_opy_() >= version.parse(
        bstack1l11ll11ll_opy_)
def bstack11l11ll1_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l1lll1l1_opy_
    global bstack111111ll1_opy_
    global bstack1lll1ll1_opy_
    CONFIG[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪឨ")] = str(bstack1lll1ll1_opy_) + str(__version__)
    bstack1111lll1_opy_ = 0
    try:
        if bstack111111ll1_opy_ is True:
            bstack1111lll1_opy_ = int(os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩឩ")))
    except:
        bstack1111lll1_opy_ = 0
    CONFIG[bstack11l1l11_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤឪ")] = True
    bstack1ll1lll11l_opy_ = bstack1l11l1l1l1_opy_(CONFIG, bstack1111lll1_opy_)
    logger.debug(bstack1ll1ll1111_opy_.format(str(bstack1ll1lll11l_opy_)))
    if CONFIG.get(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨឫ")):
        bstack1111l1l1l_opy_(bstack1ll1lll11l_opy_, bstack1111l1ll_opy_)
    if bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨឬ") in CONFIG and bstack11l1l11_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫឭ") in CONFIG[bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪឮ")][bstack1111lll1_opy_]:
        bstack1l1lll1l1_opy_ = CONFIG[bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫឯ")][bstack1111lll1_opy_][bstack11l1l11_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧឰ")]
    import urllib
    import json
    bstack1l11lll1l_opy_ = bstack11l1l11_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬឱ") + urllib.parse.quote(json.dumps(bstack1ll1lll11l_opy_))
    browser = self.connect(bstack1l11lll1l_opy_)
    return browser
def bstack1llll1ll1_opy_():
    global bstack11llll11l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11l11ll1_opy_
        bstack11llll11l_opy_ = True
    except Exception as e:
        pass
def bstack1lll11l1ll1_opy_():
    global CONFIG
    global bstack1111l111_opy_
    global bstack1ll11ll11_opy_
    global bstack1111l1ll_opy_
    global bstack111111ll1_opy_
    global bstack1ll1lll111_opy_
    CONFIG = json.loads(os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪឲ")))
    bstack1111l111_opy_ = eval(os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ឳ")))
    bstack1ll11ll11_opy_ = os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭឴"))
    bstack1ll1ll1l11_opy_(CONFIG, bstack1111l111_opy_)
    bstack1ll1lll111_opy_ = bstack1ll1ll1lll_opy_.bstack11l1llll1_opy_(CONFIG, bstack1ll1lll111_opy_)
    global bstack1lll11llll_opy_
    global bstack1l1l11llll_opy_
    global bstack1lllll1l1l_opy_
    global bstack1ll11111l1_opy_
    global bstack11111lll1_opy_
    global bstack1ll111111_opy_
    global bstack1l11lll1ll_opy_
    global bstack11ll1llll_opy_
    global bstack1l1l111111_opy_
    global bstack11llll1ll_opy_
    global bstack1l1ll1l111_opy_
    global bstack11lll11l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lll11llll_opy_ = webdriver.Remote.__init__
        bstack1l1l11llll_opy_ = WebDriver.quit
        bstack1l11lll1ll_opy_ = WebDriver.close
        bstack11ll1llll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11l1l11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ឵") in CONFIG or bstack11l1l11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬា") in CONFIG) and bstack1l1l1llll_opy_():
        if bstack11l111ll_opy_() < version.parse(bstack1l11ll11ll_opy_):
            logger.error(bstack1lll111ll_opy_.format(bstack11l111ll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l1l111111_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack11ll111l1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11llll1ll_opy_ = Config.getoption
        from _pytest import runner
        bstack1l1ll1l111_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l1l11111l_opy_)
    try:
        from pytest_bdd import reporting
        bstack11lll11l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪិ"))
    bstack1111l1ll_opy_ = CONFIG.get(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧី"), {}).get(bstack11l1l11_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ឹ"))
    bstack111111ll1_opy_ = True
    bstack11ll11l1_opy_(bstack1lll1111l_opy_)
if (bstack11l11ll11l_opy_()):
    bstack1lll11l1ll1_opy_()
@bstack1l11l11l11_opy_(class_method=False)
def bstack1lll11ll11l_opy_(hook_name, event, bstack1lll1l1ll1l_opy_=None):
    if hook_name not in [bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ឺ"), bstack11l1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪុ"), bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ូ"), bstack11l1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪួ"), bstack11l1l11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧើ"), bstack11l1l11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫឿ"), bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪៀ"), bstack11l1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧេ")]:
        return
    node = store[bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪែ")]
    if hook_name in [bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ៃ"), bstack11l1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪោ")]:
        node = store[bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡱࡴࡪࡵ࡭ࡧࡢ࡭ࡹ࡫࡭ࠨៅ")]
    elif hook_name in [bstack11l1l11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨំ"), bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬះ")]:
        node = store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪៈ")]
    if event == bstack11l1l11_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭៉"):
        hook_type = bstack1lllll1l1ll_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11lll11lll_opy_ = {
            bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ៊"): uuid,
            bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ់"): bstack1l1lll111_opy_(),
            bstack11l1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ៌"): bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ៍"),
            bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ៎"): hook_type,
            bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨ៏"): hook_name
        }
        store[bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ័")].append(uuid)
        bstack1lll1l11ll1_opy_ = node.nodeid
        if hook_type == bstack11l1l11_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ៑"):
            if not _1l1111lll1_opy_.get(bstack1lll1l11ll1_opy_, None):
                _1l1111lll1_opy_[bstack1lll1l11ll1_opy_] = {bstack11l1l11_opy_ (u"ࠨࡪࡲࡳࡰࡹ្ࠧ"): []}
            _1l1111lll1_opy_[bstack1lll1l11ll1_opy_][bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ៓")].append(bstack11lll11lll_opy_[bstack11l1l11_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ។")])
        _1l1111lll1_opy_[bstack1lll1l11ll1_opy_ + bstack11l1l11_opy_ (u"ࠫ࠲࠭៕") + hook_name] = bstack11lll11lll_opy_
        bstack1lll11llll1_opy_(node, bstack11lll11lll_opy_, bstack11l1l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭៖"))
    elif event == bstack11l1l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬៗ"):
        bstack11llll11l1_opy_ = node.nodeid + bstack11l1l11_opy_ (u"ࠧ࠮ࠩ៘") + hook_name
        _1l1111lll1_opy_[bstack11llll11l1_opy_][bstack11l1l11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭៙")] = bstack1l1lll111_opy_()
        bstack1lll111ll11_opy_(_1l1111lll1_opy_[bstack11llll11l1_opy_][bstack11l1l11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ៚")])
        bstack1lll11llll1_opy_(node, _1l1111lll1_opy_[bstack11llll11l1_opy_], bstack11l1l11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ៛"), bstack1lll1l1lll1_opy_=bstack1lll1l1ll1l_opy_)
def bstack1lll11l1lll_opy_():
    global bstack1lll111llll_opy_
    if bstack1l1l11l11l_opy_():
        bstack1lll111llll_opy_ = bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨៜ")
    else:
        bstack1lll111llll_opy_ = bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ៝")
@bstack1l11ll1l11_opy_.bstack1llll11111l_opy_
def bstack1lll111ll1l_opy_():
    bstack1lll11l1lll_opy_()
    if bstack1l1l1llll_opy_():
        bstack1l1l111l11_opy_(bstack1l11ll11l1_opy_)
    try:
        bstack111ll1111l_opy_(bstack1lll11ll11l_opy_)
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮࡯ࡰ࡭ࡶࠤࡵࡧࡴࡤࡪ࠽ࠤࢀࢃࠢ៞").format(e))
bstack1lll111ll1l_opy_()