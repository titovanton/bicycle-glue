# coding: UTF-8


import os
import shutil
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


class Command(BaseCommand):

    def handle(self, *args, **options):
        conf = settings.GLUE_CONFIG
        command = ['glue', conf['source'], conf['output'], '--recursive', '--project', ]
        ext = '.css'


        if conf.get('less', False):
            command += ['--less']
            ext = '.less'

        if conf.get('scss', False):
            command += ['--scss']
            ext = '.scss'

        if conf.get('css_url', False):
            command += ['--url=%s' % conf['css_url']]

        if conf.get('crop', False):
            command += ['--crop']

        if conf.get('margin', False):
            command += ['--margin=%d' % conf['margin']]


        try:
            subprocess.call(command)
        except OSError:
            raise Exception('glue does not exists on your os')
        else:

            if not os.path.exists(conf['move_styles_to']):
                os.makedirs(conf['move_styles_to'])

            for basename in os.listdir(conf['output']):

                if basename.endswith(ext):
                    pathname = os.path.join(conf['output'], basename)
                    dstdir = os.path.join(conf['move_styles_to'], basename)

                    if os.path.isfile(pathname):
                        shutil.move(pathname, dstdir)

                        if conf['csscomb']:

                            try:
                                subprocess.call(['csscomb', dstdir])
                            except OSError:
                                raise Exception('csscomb does not exists on your os')
