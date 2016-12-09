import sys
from fabric.api import task
from fabric.context_managers import cd, hide
from fabric.operations import sudo, put, run


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def info(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()


def success(msg):
    sys.stdout.write(bcolors.OKGREEN + msg + bcolors.ENDC + "\n")


@task
def install_packages():
    info("Updating...")
    sudo('apt-get -y update')
    success("OK")

    packages = " ".join(["python-pip", "openssl"])
    info("Installing {}...".format(packages))
    sudo('apt-get -y install {}'.format(packages))
    success("OK")


@task
def create_app_user():
    info("Creating group 'webapps'...")
    resp = run('cat /etc/group')
    if 'webapps' not in resp:
        sudo('groupadd --system webapps')
        success("Created system group webapps.")
    else:
        success("Group 'webapps' already exists.")

    info("Creating user 'channels'...")
    resp = run('cat /etc/passwd')
    if 'channels' not in resp:
        sudo('useradd --system --gid webapps --shell /bin/bash --home /srv/channels channels')
        success("Created user 'channels'...")
    else:
        success("User 'channels' already exists.")

    sudo('mkdir -p /srv/channels')
    sudo('chown channels /srv/channels')


@task
def upload_code():
    info("Uploading code...")
    sudo('mkdir -p /srv/channels')
    for x in ['channel_lineup', 'lineup', 'manage.py', 'requirements.txt',
        'supervisord.conf']:
        put(x, '/srv/channels', use_sudo=True)
    success("Code successfully uploaded.")


@task
def install_app_dependencies():
    info("Installing app dependencies from requirements.txt...")
    with cd('/srv/channels'):
        sudo('pip install -r requirements.txt')
    success("Installed packages.")


@task
def collect_static_files():
    info("Collecting static files...")
    with cd('/srv/channels'):
        sudo('python manage.py collectstatic --noinput')
    success("Static files collected to /var/www/channels/static")


@task
def run_migrations():
    info("Running Migrations...")
    with cd('/srv/channels'):
        sudo('python manage.py makemigrations')
        sudo('python manage.py migrate')
    success("OK")

@task
def configure_supervisor():
    """
    Installs supervisor, uploads our configuration, and starts the service.
    """
    info("Installing Supervisor...")
    sudo("apt-get -y install supervisor")
    success("OK")

    info("Uploading Supervisor configuration...")
    put('supervisord.conf', '/etc/supervisor/conf.d/channels.conf', use_sudo=True)
    success("OK")

    info("Restarting Supervisor...")
    sudo('service supervisor restart')
    success("OK")


@task
def configure_nginx():
    """
    Installs Nginx, uploads our configuration, and starts the service.
    """
    info("Installing Nginx...")
    sudo("apt-get -y install nginx")
    success("OK")

    info("Uploading Nginx configuration...")
    put('channels.conf', '/etc/nginx/sites-enabled', use_sudo=True)
    success("OK")

    info("Removing default Nginx configuration...")
    sudo("rm -rf /etc/nginx/sites-enabled/default")
    success("OK")

    info("Reloading Nginx configuration...")
    sudo("service nginx reload")
    success("OK")

    info("Restarting Nginx...")
    sudo("service nginx restart")
    success("OK")


@task
def full_deploy():
    with hide('running', 'stdout'):
        install_packages()
        create_app_user()
        upload_code()
        install_app_dependencies()
        collect_static_files()
        run_migrations()
        configure_supervisor()
        configure_nginx()