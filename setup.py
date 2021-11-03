#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'mycroft-hello-world.mycroftai=ovos_skill_hello_world:HelloWorldSkill'
# in this case the skill_id is defined to purposefully replace the mycroft version of the skill,
# or rather to be replaced by it in case it is present. all skill directories take precedence over plugin skills

setup(
    # this is the package name that goes on pip
    name='ovos-skill-hello-world',
    version='0.0.1',
    description='OVOS hello world skill plugin',
    url='https://github.com/OpenVoiceOS/ovos-skill-hello-world',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"ovos_skill_hello_world": ""},
    package_data={'ovos_skill_hello_world': ['locale/*', 'vocab/*', "dialog/*"]},
    packages=['ovos_skill_hello_world'],
    include_package_data=True,
    install_requires=["ovos-plugin-manager>=0.0.1a3"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
