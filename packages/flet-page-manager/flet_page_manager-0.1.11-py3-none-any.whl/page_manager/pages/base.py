from __future__ import annotations

from typing import Generic, TypeVar, TYPE_CHECKING

import flet as ft

from ..state import StateBase

if TYPE_CHECKING:
    from ..manager import PageManager
__PageBase_StateT = TypeVar("__PageBase_StateT", bound = StateBase)


class PageBase(Generic[__PageBase_StateT]):
    async def init(self, page: ft.Page, pm: PageManager[__PageBase_StateT]):
        pm.state.running_pages.append(page)
        await page.window_center_async()

    async def build(self, page: ft.Page, pm: PageManager[__PageBase_StateT]):
        raise NotImplementedError

    async def __call__(self, page: ft.Page, pm: PageManager[__PageBase_StateT]):
        await self.init(page, pm)
        await self.build(page, pm)
