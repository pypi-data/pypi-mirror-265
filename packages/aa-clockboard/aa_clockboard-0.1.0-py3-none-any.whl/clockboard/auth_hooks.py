from allianceauth import hooks
from allianceauth.services.hooks import UrlHook, MenuItemHook

from . import urls
from .views import dashboard_clocks


class AAClockboardHook(MenuItemHook):
    def __init__(self):
        super().__init__("Clock Board", "fa-regular fa-clock", "clockboard:index", navactive=['clockboard:'])

    def render(self, request):
        if request.user.has_perm('clockboard.can_see_clocks'):
            return super().render(request)
        return ''


class AAClockboardDashboardHook(hooks.DashboardItemHook):
    def __init__(self):
        super().__init__(
            dashboard_clocks,
            3
        )

    def render(self, request):
        if request.user.has_perm('clockboard.can_see_clocks'):
            return super().render(request)
        return ''


@hooks.register('menu_item_hook')
def register_menu():
    return AAClockboardHook()


@hooks.register('url_hook')
def register_urls():
    return UrlHook(urls, 'clockboard', 'clockboard/')


@hooks.register('dashboard_hook')
def register_dashboard_hook():
    return AAClockboardDashboardHook()
