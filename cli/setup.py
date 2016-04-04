from setuptools import setup, find_packages
from pip.req import parse_requirements
import uuid

install_requires_pip = [str(ir.req) for ir in parse_requirements('requirements.txt', session=uuid.uuid1())]

setup(
    name='vm mgr cli',
    version='0.1',
    description='vm mgr cli iface',
    author='oleksii.iaroshenko',
    author_email='',
    setup_requires=[
        'setuptools_git >= 0.3'],
    install_requires=install_requires_pip,
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vm_mgr_cli = cli:parse_cmd_line',
        ]
    }
)