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
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11l1l111ll_opy_, bstack1ll1l11ll1_opy_, bstack1l1l1l1l1_opy_, bstack1llll11l_opy_
from bstack_utils.messages import bstack1lll1lll_opy_, bstack11ll111l1_opy_
from bstack_utils.proxy import bstack1ll11l111_opy_, bstack1lll1l11ll_opy_
bstack1ll1l11l1l_opy_ = Config.bstack1l1l1l1ll_opy_()
def bstack11l1lll1l1_opy_(config):
    return config[bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᆄ")]
def bstack11l1llll1l_opy_(config):
    return config[bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᆅ")]
def bstack1l1111l11_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111lll1l1l_opy_(obj):
    values = []
    bstack111ll1ll1l_opy_ = re.compile(bstack11l1l11_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥᆆ"), re.I)
    for key in obj.keys():
        if bstack111ll1ll1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111ll11ll1_opy_(config):
    tags = []
    tags.extend(bstack111lll1l1l_opy_(os.environ))
    tags.extend(bstack111lll1l1l_opy_(config))
    return tags
def bstack11l11lll1l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1111lll_opy_(bstack111ll1l11l_opy_):
    if not bstack111ll1l11l_opy_:
        return bstack11l1l11_opy_ (u"ࠧࠨᆇ")
    return bstack11l1l11_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤᆈ").format(bstack111ll1l11l_opy_.name, bstack111ll1l11l_opy_.email)
def bstack11ll111111_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l111l111_opy_ = repo.common_dir
        info = {
            bstack11l1l11_opy_ (u"ࠤࡶ࡬ࡦࠨᆉ"): repo.head.commit.hexsha,
            bstack11l1l11_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨᆊ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l1l11_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦᆋ"): repo.active_branch.name,
            bstack11l1l11_opy_ (u"ࠧࡺࡡࡨࠤᆌ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤᆍ"): bstack11l1111lll_opy_(repo.head.commit.committer),
            bstack11l1l11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣᆎ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l1l11_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣᆏ"): bstack11l1111lll_opy_(repo.head.commit.author),
            bstack11l1l11_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢᆐ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l1l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᆑ"): repo.head.commit.message,
            bstack11l1l11_opy_ (u"ࠦࡷࡵ࡯ࡵࠤᆒ"): repo.git.rev_parse(bstack11l1l11_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢᆓ")),
            bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᆔ"): bstack11l111l111_opy_,
            bstack11l1l11_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥᆕ"): subprocess.check_output([bstack11l1l11_opy_ (u"ࠣࡩ࡬ࡸࠧᆖ"), bstack11l1l11_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧᆗ"), bstack11l1l11_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨᆘ")]).strip().decode(
                bstack11l1l11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᆙ")),
            bstack11l1l11_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᆚ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᆛ"): repo.git.rev_list(
                bstack11l1l11_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢᆜ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111ll1ll11_opy_ = []
        for remote in remotes:
            bstack111lll1l11_opy_ = {
                bstack11l1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᆝ"): remote.name,
                bstack11l1l11_opy_ (u"ࠤࡸࡶࡱࠨᆞ"): remote.url,
            }
            bstack111ll1ll11_opy_.append(bstack111lll1l11_opy_)
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᆟ"): bstack11l1l11_opy_ (u"ࠦ࡬࡯ࡴࠣᆠ"),
            **info,
            bstack11l1l11_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨᆡ"): bstack111ll1ll11_opy_
        }
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᆢ").format(err))
        return {}
def bstack1lll111111_opy_():
    env = os.environ
    if (bstack11l1l11_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᆣ") in env and len(env[bstack11l1l11_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᆤ")]) > 0) or (
            bstack11l1l11_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᆥ") in env and len(env[bstack11l1l11_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᆦ")]) > 0):
        return {
            bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆧ"): bstack11l1l11_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨᆨ"),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᆩ"): env.get(bstack11l1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᆪ")),
            bstack11l1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆫ"): env.get(bstack11l1l11_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦᆬ")),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᆭ"): env.get(bstack11l1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᆮ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠧࡉࡉࠣᆯ")) == bstack11l1l11_opy_ (u"ࠨࡴࡳࡷࡨࠦᆰ") and bstack1l1lllll1l_opy_(env.get(bstack11l1l11_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤᆱ"))):
        return {
            bstack11l1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᆲ"): bstack11l1l11_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦᆳ"),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᆴ"): env.get(bstack11l1l11_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᆵ")),
            bstack11l1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᆶ"): env.get(bstack11l1l11_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥᆷ")),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆸ"): env.get(bstack11l1l11_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦᆹ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠤࡆࡍࠧᆺ")) == bstack11l1l11_opy_ (u"ࠥࡸࡷࡻࡥࠣᆻ") and bstack1l1lllll1l_opy_(env.get(bstack11l1l11_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦᆼ"))):
        return {
            bstack11l1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆽ"): bstack11l1l11_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤᆾ"),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᆿ"): env.get(bstack11l1l11_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣᇀ")),
            bstack11l1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᇁ"): env.get(bstack11l1l11_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᇂ")),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇃ"): env.get(bstack11l1l11_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᇄ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠨࡃࡊࠤᇅ")) == bstack11l1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧᇆ") and env.get(bstack11l1l11_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᇇ")) == bstack11l1l11_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦᇈ"):
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᇉ"): bstack11l1l11_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨᇊ"),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇋ"): None,
            bstack11l1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇌ"): None,
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇍ"): None
        }
    if env.get(bstack11l1l11_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦᇎ")) and env.get(bstack11l1l11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧᇏ")):
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᇐ"): bstack11l1l11_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢᇑ"),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇒ"): env.get(bstack11l1l11_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦᇓ")),
            bstack11l1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇔ"): None,
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇕ"): env.get(bstack11l1l11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᇖ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠥࡇࡎࠨᇗ")) == bstack11l1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᇘ") and bstack1l1lllll1l_opy_(env.get(bstack11l1l11_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦᇙ"))):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇚ"): bstack11l1l11_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨᇛ"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇜ"): env.get(bstack11l1l11_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧᇝ")),
            bstack11l1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇞ"): None,
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇟ"): env.get(bstack11l1l11_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᇠ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠨࡃࡊࠤᇡ")) == bstack11l1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧᇢ") and bstack1l1lllll1l_opy_(env.get(bstack11l1l11_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦᇣ"))):
        return {
            bstack11l1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇤ"): bstack11l1l11_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨᇥ"),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇦ"): env.get(bstack11l1l11_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦᇧ")),
            bstack11l1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇨ"): env.get(bstack11l1l11_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᇩ")),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇪ"): env.get(bstack11l1l11_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧᇫ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠥࡇࡎࠨᇬ")) == bstack11l1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᇭ") and bstack1l1lllll1l_opy_(env.get(bstack11l1l11_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣᇮ"))):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇯ"): bstack11l1l11_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢᇰ"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇱ"): env.get(bstack11l1l11_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨᇲ")),
            bstack11l1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇳ"): env.get(bstack11l1l11_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᇴ")),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇵ"): env.get(bstack11l1l11_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤᇶ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠢࡄࡋࠥᇷ")) == bstack11l1l11_opy_ (u"ࠣࡶࡵࡹࡪࠨᇸ") and bstack1l1lllll1l_opy_(env.get(bstack11l1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᇹ"))):
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᇺ"): bstack11l1l11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᇻ"),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇼ"): env.get(bstack11l1l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᇽ")),
            bstack11l1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇾ"): env.get(bstack11l1l11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᇿ")) or env.get(bstack11l1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧሀ")),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤሁ"): env.get(bstack11l1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨሂ"))
        }
    if bstack1l1lllll1l_opy_(env.get(bstack11l1l11_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢሃ"))):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሄ"): bstack11l1l11_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢህ"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሆ"): bstack11l1l11_opy_ (u"ࠤࡾࢁࢀࢃࠢሇ").format(env.get(bstack11l1l11_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ለ")), env.get(bstack11l1l11_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫሉ"))),
            bstack11l1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢሊ"): env.get(bstack11l1l11_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧላ")),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨሌ"): env.get(bstack11l1l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣል"))
        }
    if bstack1l1lllll1l_opy_(env.get(bstack11l1l11_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦሎ"))):
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣሏ"): bstack11l1l11_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨሐ"),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሑ"): bstack11l1l11_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧሒ").format(env.get(bstack11l1l11_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭ሓ")), env.get(bstack11l1l11_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩሔ")), env.get(bstack11l1l11_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪሕ")), env.get(bstack11l1l11_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧሖ"))),
            bstack11l1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨሗ"): env.get(bstack11l1l11_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤመ")),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧሙ"): env.get(bstack11l1l11_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣሚ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤማ")) and env.get(bstack11l1l11_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦሜ")):
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣም"): bstack11l1l11_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨሞ"),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሟ"): bstack11l1l11_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤሠ").format(env.get(bstack11l1l11_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪሡ")), env.get(bstack11l1l11_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭ሢ")), env.get(bstack11l1l11_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩሣ"))),
            bstack11l1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧሤ"): env.get(bstack11l1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦሥ")),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦሦ"): env.get(bstack11l1l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨሧ"))
        }
    if any([env.get(bstack11l1l11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧረ")), env.get(bstack11l1l11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢሩ")), env.get(bstack11l1l11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨሪ"))]):
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣራ"): bstack11l1l11_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦሬ"),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣር"): env.get(bstack11l1l11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧሮ")),
            bstack11l1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሯ"): env.get(bstack11l1l11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨሰ")),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሱ"): env.get(bstack11l1l11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣሲ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤሳ")):
        return {
            bstack11l1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥሴ"): bstack11l1l11_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨስ"),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሶ"): env.get(bstack11l1l11_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥሷ")),
            bstack11l1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሸ"): env.get(bstack11l1l11_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤሹ")),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሺ"): env.get(bstack11l1l11_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥሻ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢሼ")) or env.get(bstack11l1l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤሽ")):
        return {
            bstack11l1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨሾ"): bstack11l1l11_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥሿ"),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨቀ"): env.get(bstack11l1l11_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣቁ")),
            bstack11l1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢቂ"): bstack11l1l11_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨቃ") if env.get(bstack11l1l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤቄ")) else None,
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢቅ"): env.get(bstack11l1l11_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢቆ"))
        }
    if any([env.get(bstack11l1l11_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣቇ")), env.get(bstack11l1l11_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧቈ")), env.get(bstack11l1l11_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧ቉"))]):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦቊ"): bstack11l1l11_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨቋ"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦቌ"): None,
            bstack11l1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦቍ"): env.get(bstack11l1l11_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢ቎")),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ቏"): env.get(bstack11l1l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢቐ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤቑ")):
        return {
            bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧቒ"): bstack11l1l11_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦቓ"),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧቔ"): env.get(bstack11l1l11_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤቕ")),
            bstack11l1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨቖ"): bstack11l1l11_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨ቗").format(env.get(bstack11l1l11_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩቘ"))) if env.get(bstack11l1l11_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥ቙")) else None,
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢቚ"): env.get(bstack11l1l11_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦቛ"))
        }
    if bstack1l1lllll1l_opy_(env.get(bstack11l1l11_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦቜ"))):
        return {
            bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤቝ"): bstack11l1l11_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨ቞"),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ቟"): env.get(bstack11l1l11_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦበ")),
            bstack11l1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥቡ"): env.get(bstack11l1l11_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧቢ")),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤባ"): env.get(bstack11l1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨቤ"))
        }
    if bstack1l1lllll1l_opy_(env.get(bstack11l1l11_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨብ"))):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦቦ"): bstack11l1l11_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣቧ"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦቨ"): bstack11l1l11_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥቩ").format(env.get(bstack11l1l11_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧቪ")), env.get(bstack11l1l11_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨቫ")), env.get(bstack11l1l11_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬቬ"))),
            bstack11l1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣቭ"): env.get(bstack11l1l11_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤቮ")),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢቯ"): env.get(bstack11l1l11_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤተ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠥࡇࡎࠨቱ")) == bstack11l1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤቲ") and env.get(bstack11l1l11_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧታ")) == bstack11l1l11_opy_ (u"ࠨ࠱ࠣቴ"):
        return {
            bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧት"): bstack11l1l11_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣቶ"),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧቷ"): bstack11l1l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨቸ").format(env.get(bstack11l1l11_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨቹ"))),
            bstack11l1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢቺ"): None,
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧቻ"): None,
        }
    if env.get(bstack11l1l11_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥቼ")):
        return {
            bstack11l1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨች"): bstack11l1l11_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦቾ"),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨቿ"): None,
            bstack11l1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨኀ"): env.get(bstack11l1l11_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨኁ")),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧኂ"): env.get(bstack11l1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨኃ"))
        }
    if any([env.get(bstack11l1l11_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦኄ")), env.get(bstack11l1l11_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤኅ")), env.get(bstack11l1l11_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣኆ")), env.get(bstack11l1l11_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧኇ"))]):
        return {
            bstack11l1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥኈ"): bstack11l1l11_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤ኉"),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥኊ"): None,
            bstack11l1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥኋ"): env.get(bstack11l1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥኌ")) or None,
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤኍ"): env.get(bstack11l1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ኎"), 0)
        }
    if env.get(bstack11l1l11_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ኏")):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦነ"): bstack11l1l11_opy_ (u"ࠢࡈࡱࡆࡈࠧኑ"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦኒ"): None,
            bstack11l1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦና"): env.get(bstack11l1l11_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣኔ")),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥን"): env.get(bstack11l1l11_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦኖ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦኗ")):
        return {
            bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧኘ"): bstack11l1l11_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦኙ"),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧኚ"): env.get(bstack11l1l11_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤኛ")),
            bstack11l1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨኜ"): env.get(bstack11l1l11_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣኝ")),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧኞ"): env.get(bstack11l1l11_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧኟ"))
        }
    return {bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢአ"): None}
def get_host_info():
    return {
        bstack11l1l11_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦኡ"): platform.node(),
        bstack11l1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧኢ"): platform.system(),
        bstack11l1l11_opy_ (u"ࠦࡹࡿࡰࡦࠤኣ"): platform.machine(),
        bstack11l1l11_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨኤ"): platform.version(),
        bstack11l1l11_opy_ (u"ࠨࡡࡳࡥ࡫ࠦእ"): platform.architecture()[0]
    }
def bstack1l1l1llll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111lllll11_opy_():
    if bstack1ll1l11l1l_opy_.get_property(bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨኦ")):
        return bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧኧ")
    return bstack11l1l11_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨከ")
def bstack11l11l1l1l_opy_(driver):
    info = {
        bstack11l1l11_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩኩ"): driver.capabilities,
        bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨኪ"): driver.session_id,
        bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ካ"): driver.capabilities.get(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫኬ"), None),
        bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩክ"): driver.capabilities.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩኮ"), None),
        bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫኯ"): driver.capabilities.get(bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩኰ"), None),
    }
    if bstack111lllll11_opy_() == bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ኱"):
        info[bstack11l1l11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ኲ")] = bstack11l1l11_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬኳ") if bstack1llll11111_opy_() else bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩኴ")
    return info
def bstack1llll11111_opy_():
    if bstack1ll1l11l1l_opy_.get_property(bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧኵ")):
        return True
    if bstack1l1lllll1l_opy_(os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ኶"), None)):
        return True
    return False
def bstack1llll11lll_opy_(bstack111lll1lll_opy_, url, data, config):
    headers = config.get(bstack11l1l11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ኷"), None)
    proxies = bstack1ll11l111_opy_(config, url)
    auth = config.get(bstack11l1l11_opy_ (u"ࠫࡦࡻࡴࡩࠩኸ"), None)
    response = requests.request(
            bstack111lll1lll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1lll111l_opy_(bstack1l1l11lll_opy_, size):
    bstack1l1l1ll1l_opy_ = []
    while len(bstack1l1l11lll_opy_) > size:
        bstack1l11ll1ll_opy_ = bstack1l1l11lll_opy_[:size]
        bstack1l1l1ll1l_opy_.append(bstack1l11ll1ll_opy_)
        bstack1l1l11lll_opy_ = bstack1l1l11lll_opy_[size:]
    bstack1l1l1ll1l_opy_.append(bstack1l1l11lll_opy_)
    return bstack1l1l1ll1l_opy_
def bstack11l1111ll1_opy_(message, bstack11l11l1lll_opy_=False):
    os.write(1, bytes(message, bstack11l1l11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫኹ")))
    os.write(1, bytes(bstack11l1l11_opy_ (u"࠭࡜࡯ࠩኺ"), bstack11l1l11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ኻ")))
    if bstack11l11l1lll_opy_:
        with open(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧኼ") + os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨኽ")] + bstack11l1l11_opy_ (u"ࠪ࠲ࡱࡵࡧࠨኾ"), bstack11l1l11_opy_ (u"ࠫࡦ࠭኿")) as f:
            f.write(message + bstack11l1l11_opy_ (u"ࠬࡢ࡮ࠨዀ"))
def bstack111lllll1l_opy_():
    return os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ዁")].lower() == bstack11l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬዂ")
def bstack11ll1111_opy_(bstack11l11l111l_opy_):
    return bstack11l1l11_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧዃ").format(bstack11l1l111ll_opy_, bstack11l11l111l_opy_)
def bstack1l1lll111_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack11l1l11_opy_ (u"ࠩ࡝ࠫዄ")
def bstack11l1111l1l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l1l11_opy_ (u"ࠪ࡞ࠬዅ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l1l11_opy_ (u"ࠫ࡟࠭዆")))).total_seconds() * 1000
def bstack111ll1l1ll_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack11l1l11_opy_ (u"ࠬࡠࠧ዇")
def bstack111lll111l_opy_(bstack111llll1l1_opy_):
    date_format = bstack11l1l11_opy_ (u"࡚࠭ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠫወ")
    bstack111lll11ll_opy_ = datetime.datetime.strptime(bstack111llll1l1_opy_, date_format)
    return bstack111lll11ll_opy_.isoformat() + bstack11l1l11_opy_ (u"࡛ࠧࠩዉ")
def bstack11l11ll111_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨዊ")
    else:
        return bstack11l1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩዋ")
def bstack1l1lllll1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨዌ")
def bstack111llllll1_opy_(val):
    return val.__str__().lower() == bstack11l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪው")
def bstack1l11l11l11_opy_(bstack11l111llll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l111llll_opy_ as e:
                print(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧዎ").format(func.__name__, bstack11l111llll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l11lll11_opy_(bstack111llll11l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111llll11l_opy_(cls, *args, **kwargs)
            except bstack11l111llll_opy_ as e:
                print(bstack11l1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨዏ").format(bstack111llll11l_opy_.__name__, bstack11l111llll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l11lll11_opy_
    else:
        return decorator
def bstack1l111ll11_opy_(bstack11ll1ll1ll_opy_):
    if bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫዐ") in bstack11ll1ll1ll_opy_ and bstack111llllll1_opy_(bstack11ll1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬዑ")]):
        return False
    if bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫዒ") in bstack11ll1ll1ll_opy_ and bstack111llllll1_opy_(bstack11ll1ll1ll_opy_[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬዓ")]):
        return False
    return True
def bstack1l1l11l11l_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l1l11l111_opy_(hub_url):
    if bstack11l111ll_opy_() <= version.parse(bstack11l1l11_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫዔ")):
        if hub_url != bstack11l1l11_opy_ (u"ࠬ࠭ዕ"):
            return bstack11l1l11_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢዖ") + hub_url + bstack11l1l11_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ዗")
        return bstack1l1l1l1l1_opy_
    if hub_url != bstack11l1l11_opy_ (u"ࠨࠩዘ"):
        return bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦዙ") + hub_url + bstack11l1l11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦዚ")
    return bstack1llll11l_opy_
def bstack11l11ll11l_opy_():
    return isinstance(os.getenv(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪዛ")), str)
def bstack1llllll1ll_opy_(url):
    return urlparse(url).hostname
def bstack1llll111l_opy_(hostname):
    for bstack1lll11ll11_opy_ in bstack1ll1l11ll1_opy_:
        regex = re.compile(bstack1lll11ll11_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111lll1ll1_opy_(bstack111ll1l1l1_opy_, file_name, logger):
    bstack1ll1l1ll_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠬࢄࠧዜ")), bstack111ll1l1l1_opy_)
    try:
        if not os.path.exists(bstack1ll1l1ll_opy_):
            os.makedirs(bstack1ll1l1ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"࠭ࡾࠨዝ")), bstack111ll1l1l1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l1l11_opy_ (u"ࠧࡸࠩዞ")):
                pass
            with open(file_path, bstack11l1l11_opy_ (u"ࠣࡹ࠮ࠦዟ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1lll1lll_opy_.format(str(e)))
def bstack11l11l1l11_opy_(file_name, key, value, logger):
    file_path = bstack111lll1ll1_opy_(bstack11l1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩዠ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l11l1l1l_opy_ = json.load(open(file_path, bstack11l1l11_opy_ (u"ࠪࡶࡧ࠭ዡ")))
        else:
            bstack1l11l1l1l_opy_ = {}
        bstack1l11l1l1l_opy_[key] = value
        with open(file_path, bstack11l1l11_opy_ (u"ࠦࡼ࠱ࠢዢ")) as outfile:
            json.dump(bstack1l11l1l1l_opy_, outfile)
def bstack1ll11l1ll1_opy_(file_name, logger):
    file_path = bstack111lll1ll1_opy_(bstack11l1l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬዣ"), file_name, logger)
    bstack1l11l1l1l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l1l11_opy_ (u"࠭ࡲࠨዤ")) as bstack1ll1llll1_opy_:
            bstack1l11l1l1l_opy_ = json.load(bstack1ll1llll1_opy_)
    return bstack1l11l1l1l_opy_
def bstack1l11l1ll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫዥ") + file_path + bstack11l1l11_opy_ (u"ࠨࠢࠪዦ") + str(e))
def bstack11l111ll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l1l11_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦዧ")
def bstack1l1l1l1l1l_opy_(config):
    if bstack11l1l11_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩየ") in config:
        del (config[bstack11l1l11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪዩ")])
        return False
    if bstack11l111ll_opy_() < version.parse(bstack11l1l11_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫዪ")):
        return False
    if bstack11l111ll_opy_() >= version.parse(bstack11l1l11_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬያ")):
        return True
    if bstack11l1l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧዬ") in config and config[bstack11l1l11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨይ")] is False:
        return False
    else:
        return True
def bstack1l1l111l1l_opy_(args_list, bstack11l11ll1ll_opy_):
    index = -1
    for value in bstack11l11ll1ll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11lll1ll11_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11lll1ll11_opy_ = bstack11lll1ll11_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩዮ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪዯ"), exception=exception)
    def bstack11ll1l11l1_opy_(self):
        if self.result != bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫደ"):
            return None
        if bstack11l1l11_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣዱ") in self.exception_type:
            return bstack11l1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢዲ")
        return bstack11l1l11_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣዳ")
    def bstack111llll111_opy_(self):
        if self.result != bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨዴ"):
            return None
        if self.bstack11lll1ll11_opy_:
            return self.bstack11lll1ll11_opy_
        return bstack111ll1lll1_opy_(self.exception)
def bstack111ll1lll1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l111ll11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1111lll1l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l11ll11_opy_(config, logger):
    try:
        import playwright
        bstack11l1111111_opy_ = playwright.__file__
        bstack11l111111l_opy_ = os.path.split(bstack11l1111111_opy_)
        bstack111ll1l111_opy_ = bstack11l111111l_opy_[0] + bstack11l1l11_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬድ")
        os.environ[bstack11l1l11_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭ዶ")] = bstack1lll1l11ll_opy_(config)
        with open(bstack111ll1l111_opy_, bstack11l1l11_opy_ (u"ࠫࡷ࠭ዷ")) as f:
            bstack1lll11l11l_opy_ = f.read()
            bstack11l11ll1l1_opy_ = bstack11l1l11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫዸ")
            bstack11l11llll1_opy_ = bstack1lll11l11l_opy_.find(bstack11l11ll1l1_opy_)
            if bstack11l11llll1_opy_ == -1:
              process = subprocess.Popen(bstack11l1l11_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥዹ"), shell=True, cwd=bstack11l111111l_opy_[0])
              process.wait()
              bstack11l11l1ll1_opy_ = bstack11l1l11_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧዺ")
              bstack111lll11l1_opy_ = bstack11l1l11_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧዻ")
              bstack111lll1111_opy_ = bstack1lll11l11l_opy_.replace(bstack11l11l1ll1_opy_, bstack111lll11l1_opy_)
              with open(bstack111ll1l111_opy_, bstack11l1l11_opy_ (u"ࠩࡺࠫዼ")) as f:
                f.write(bstack111lll1111_opy_)
    except Exception as e:
        logger.error(bstack11ll111l1_opy_.format(str(e)))
def bstack1l1l1ll1l1_opy_():
  try:
    bstack11l111l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪዽ"))
    bstack11l11l1111_opy_ = []
    if os.path.exists(bstack11l111l11l_opy_):
      with open(bstack11l111l11l_opy_) as f:
        bstack11l11l1111_opy_ = json.load(f)
      os.remove(bstack11l111l11l_opy_)
    return bstack11l11l1111_opy_
  except:
    pass
  return []
def bstack1ll11l111l_opy_(bstack1ll1ll1ll1_opy_):
  try:
    bstack11l11l1111_opy_ = []
    bstack11l111l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫዾ"))
    if os.path.exists(bstack11l111l11l_opy_):
      with open(bstack11l111l11l_opy_) as f:
        bstack11l11l1111_opy_ = json.load(f)
    bstack11l11l1111_opy_.append(bstack1ll1ll1ll1_opy_)
    with open(bstack11l111l11l_opy_, bstack11l1l11_opy_ (u"ࠬࡽࠧዿ")) as f:
        json.dump(bstack11l11l1111_opy_, f)
  except:
    pass
def bstack1l11ll11l_opy_(logger, bstack11l11111l1_opy_ = False):
  try:
    test_name = os.environ.get(bstack11l1l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩጀ"), bstack11l1l11_opy_ (u"ࠧࠨጁ"))
    if test_name == bstack11l1l11_opy_ (u"ࠨࠩጂ"):
        test_name = threading.current_thread().__dict__.get(bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨጃ"), bstack11l1l11_opy_ (u"ࠪࠫጄ"))
    bstack11l111lll1_opy_ = bstack11l1l11_opy_ (u"ࠫ࠱ࠦࠧጅ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l11111l1_opy_:
        bstack1111lll1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬጆ"), bstack11l1l11_opy_ (u"࠭࠰ࠨጇ"))
        bstack1111l1l11_opy_ = {bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬገ"): test_name, bstack11l1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧጉ"): bstack11l111lll1_opy_, bstack11l1l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨጊ"): bstack1111lll1_opy_}
        bstack111llll1ll_opy_ = []
        bstack11l11111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩጋ"))
        if os.path.exists(bstack11l11111ll_opy_):
            with open(bstack11l11111ll_opy_) as f:
                bstack111llll1ll_opy_ = json.load(f)
        bstack111llll1ll_opy_.append(bstack1111l1l11_opy_)
        with open(bstack11l11111ll_opy_, bstack11l1l11_opy_ (u"ࠫࡼ࠭ጌ")) as f:
            json.dump(bstack111llll1ll_opy_, f)
    else:
        bstack1111l1l11_opy_ = {bstack11l1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪግ"): test_name, bstack11l1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬጎ"): bstack11l111lll1_opy_, bstack11l1l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ጏ"): str(multiprocessing.current_process().name)}
        if bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬጐ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1111l1l11_opy_)
  except Exception as e:
      logger.warn(bstack11l1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ጑").format(e))
def bstack1ll111ll1l_opy_(error_message, test_name, index, logger):
  try:
    bstack11l111l1l1_opy_ = []
    bstack1111l1l11_opy_ = {bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨጒ"): test_name, bstack11l1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪጓ"): error_message, bstack11l1l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫጔ"): index}
    bstack111ll11lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧጕ"))
    if os.path.exists(bstack111ll11lll_opy_):
        with open(bstack111ll11lll_opy_) as f:
            bstack11l111l1l1_opy_ = json.load(f)
    bstack11l111l1l1_opy_.append(bstack1111l1l11_opy_)
    with open(bstack111ll11lll_opy_, bstack11l1l11_opy_ (u"ࠧࡸࠩ጖")) as f:
        json.dump(bstack11l111l1l1_opy_, f)
  except Exception as e:
    logger.warn(bstack11l1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ጗").format(e))
def bstack1ll1llll_opy_(bstack1ll11l11l_opy_, name, logger):
  try:
    bstack1111l1l11_opy_ = {bstack11l1l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧጘ"): name, bstack11l1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩጙ"): bstack1ll11l11l_opy_, bstack11l1l11_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪጚ"): str(threading.current_thread()._name)}
    return bstack1111l1l11_opy_
  except Exception as e:
    logger.warn(bstack11l1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤጛ").format(e))
  return
def bstack111ll11l1l_opy_():
    return platform.system() == bstack11l1l11_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹࠧጜ")
def bstack1lll1lll11_opy_(bstack11l111l1ll_opy_, config, logger):
    bstack11l111ll1l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l111l1ll_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡲࡴࡦࡴࠣࡧࡴࡴࡦࡪࡩࠣ࡯ࡪࡿࡳࠡࡤࡼࠤࡷ࡫ࡧࡦࡺࠣࡱࡦࡺࡣࡩ࠼ࠣࡿࢂࠨጝ").format(e))
    return bstack11l111ll1l_opy_
def bstack111lllllll_opy_(bstack11l11l11ll_opy_, bstack11l11l11l1_opy_):
    bstack11l1111l11_opy_ = version.parse(bstack11l11l11ll_opy_)
    bstack111ll1llll_opy_ = version.parse(bstack11l11l11l1_opy_)
    if bstack11l1111l11_opy_ > bstack111ll1llll_opy_:
        return 1
    elif bstack11l1111l11_opy_ < bstack111ll1llll_opy_:
        return -1
    else:
        return 0