#!/usr/bin/env python

'''
python utils too small for a package
'''

import json
import shutil
import socket
import subprocess

import psutil

from khnum.khnum import hnum


def ago(dstr):
    '''
    returns relative time string from ISO date string

    >>> utils.ago('2020-01-01')
    '2.86 months ago'

    >>> utils.ago('2020-03-26T12:00:00Z')
    '9.72 hours ago'
    '''
    now = datetime.utcnow()

    then = datetime(
        int(dstr[:4]),  # year
        int(dstr[5:7] if dstr[5:7] else 0),  # month
        int(dstr[8:10] if dstr[8:10] else 0),  # day
        int(dstr[11:13] if dstr[11:13] else 0),  # hours
        int(dstr[14:16] if dstr[14:16] else 0),  # minutes
        int(dstr[17:19] if dstr[17:19] else 0))  # seconds

    seconds = int((now - then).total_seconds())

    sec_in_hour = 60 * 60
    sec_in_day = sec_in_hour * 24
    sec_in_week = sec_in_day * 7
    sec_in_month = sec_in_day * 30

    if seconds > sec_in_month:
        return '{} months ago'.format(round(seconds / sec_in_month, 2))

    if seconds > sec_in_week:
        return '{} weeks ago'.format(round(seconds / sec_in_week, 2))

    if seconds > sec_in_day:
        return '{} days ago'.format(round(seconds / sec_in_day, 2))

    if seconds > sec_in_hour:
        return '{} hours ago'.format(round(seconds / sec_in_hour, 2))

    return '{} sec ago'.format(seconds)


def mbps(_bytes, seconds):
    '''
    returns megabits per second from bytes and seconds
    '''
    megabits = _bytes / 125000.0
    return round(megabits / seconds, 2)


def pretty(data):
    '''
    returns data as a pretty string
    '''
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


def shell(cmd):
    '''
    returns stdout, stdin from shell command
    raises IOError on command failure
    '''
    job = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if job.returncode != 0:
        raise IOError(
            'command failed: {} stdout: {} stderr: {}'.format(
                cmd, job.stdout, job.stderr))

    return job.stdout, job.stderr


def system(basepath):
    '''
    returns system info string: <host> <%cpu> <%vmem> <space>
    '''
    space = hnum(shutil.disk_usage(basepath).free, 'bytes')
    host = socket.gethostname().split('.')[0]
    cpu = psutil.cpu_percent()
    vmem = dict(psutil.virtual_memory()._asdict())

    return '{} {} %cpu {} %vmem {}'.format(host, cpu, vmem['percent'], space)
