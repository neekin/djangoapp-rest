import xadmin
from xadmin import views
# from xadmin.plugins.auth import UserAdmin
# from .models import UserProfile


class BaseSetting:
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    site_title = '后台管理系统'
    site_footer = '在线管理'
    menu_style = 'accordion'


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
