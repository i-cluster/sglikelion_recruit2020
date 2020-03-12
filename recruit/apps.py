from django.apps import AppConfig


class RecruitConfig(AppConfig):
    name = 'recruit'
    verbose_name = '지원자 관리'


from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem

class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
    menu = (
        ParentItem('지원자 관리', children=[
            ChildItem(model='recruit.profile'),
            ChildItem(model='recruit.application'),
        ], icon='fa fa-users'),
    )