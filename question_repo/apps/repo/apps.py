from django.apps import AppConfig


class RepoConfig(AppConfig):
    name = 'apps.repo'
    verbose_name = '题库'

    def ready(self):
        # handler里面写了信号调用及处理回调函数
        from .signal import handler