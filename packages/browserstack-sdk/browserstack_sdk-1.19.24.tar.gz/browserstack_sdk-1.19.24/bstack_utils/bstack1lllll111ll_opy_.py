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
import threading
bstack1lllll11ll1_opy_ = 1000
bstack1lllll11l11_opy_ = 5
bstack1lllll11111_opy_ = 30
bstack1lllll11lll_opy_ = 2
class bstack1lllll1l111_opy_:
    def __init__(self, handler, bstack1lllll11l1l_opy_=bstack1lllll11ll1_opy_, bstack1lllll1111l_opy_=bstack1lllll11l11_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lllll11l1l_opy_ = bstack1lllll11l1l_opy_
        self.bstack1lllll1111l_opy_ = bstack1lllll1111l_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1lllll1l11l_opy_()
    def bstack1lllll1l11l_opy_(self):
        self.timer = threading.Timer(self.bstack1lllll1111l_opy_, self.bstack1llll1llll1_opy_)
        self.timer.start()
    def bstack1lllll111l1_opy_(self):
        self.timer.cancel()
    def bstack1llll1lllll_opy_(self):
        self.bstack1lllll111l1_opy_()
        self.bstack1lllll1l11l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lllll11l1l_opy_:
                t = threading.Thread(target=self.bstack1llll1llll1_opy_)
                t.start()
                self.bstack1llll1lllll_opy_()
    def bstack1llll1llll1_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1lllll11l1l_opy_]
        del self.queue[:self.bstack1lllll11l1l_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1lllll111l1_opy_()
        while len(self.queue) > 0:
            self.bstack1llll1llll1_opy_()