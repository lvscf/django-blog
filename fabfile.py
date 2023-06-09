from fabric import task
from invoke import Responder
from _credentials import github_username, github_password
import logging
logging.basicConfig(level=logging.DEBUG)

def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username)
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(github_username),
        response='{}\n'.format(github_password)
    )
    return [username_responder, password_responder]


@task()
def deploy(c):
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'django-blog-tutorial'

    project_root_path = '~/apps/django-blog/'

    # 先停止应用
    with c.cd(supervisor_conf_path):
        cmd = '~/.local/bin/supervisorctl -c ~/etc/supervisord.conf stop {}'.format(supervisor_program_name)
        logging.debug('当前目录：{}，当前操作：{}'.format(supervisor_conf_path, cmd))
        c.run(cmd)
        logging.debug('操作完成')

    # 进入项目根目录，从 Git 拉取最新代码
    with c.cd(project_root_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        logging.debug('当前目录：{}，当前操作：{}'.format(project_root_path, cmd))
        c.run(cmd, watchers=responders)
        logging.debug('操作完成')

    # 安装依赖，迁移数据库，收集静态文件
    with c.cd(project_root_path):
        cmd = '安装依赖，迁移数据库，收集静态文件'
        logging.debug('当前目录：{}，当前操作：{}'.format(project_root_path, cmd))
        c.run('pipenv install --deploy --ignore-pipfile')
        c.run('pipenv run python manage.py migrate')
        c.run('pipenv run python manage.py collectstatic --noinput')
        logging.debug('操作完成')

    # 重新启动应用
    with c.cd(supervisor_conf_path):
        cmd = '~/.local/bin/supervisorctl -c ~/etc/supervisord.conf start {}'.format(supervisor_program_name)
        logging.debug('当前目录：{}，当前操作：{}'.format(project_root_path, cmd))
        c.run(cmd)
        logging.debug('操作完成')
