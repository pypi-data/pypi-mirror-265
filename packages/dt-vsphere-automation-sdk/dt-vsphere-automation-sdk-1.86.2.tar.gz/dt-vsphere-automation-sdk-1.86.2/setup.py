#!/usr/bin/env python

from setuptools import setup

setup(name='dt-vsphere-automation-sdk',
      version='1.86.2',
      description='VMware vSphere Automation SDK for Python',
      url='https://github.com/vmware/vsphere-automation-sdk-python',
      author='VMware, Inc.',
      license='MIT',
      packages=[],
      install_requires=[
        'lxml >= 4.3.0',
        'pyvmomi',
        'vapi-runtime==2.44.0',
        'vcenter-bindings==4.2.0',
        'vapi-common-client==2.44.0',
        'vmwarecloud-aws==1.64.0',
        'nsx-python-sdk==4.1.2.0.0',
        'nsx-policy-python-sdk==4.1.2.0.0',
        'nsx-vmc-policy-python-sdk==4.1.2.0.0',
        'nsx-vmc-aws-integration-python-sdk==4.1.2.0.0',
        'vmwarecloud-draas==1.23.0',
      ]
)
