from django import template
import re

register = template.Library()

BROWSERS = (
    (re.compile('Edg'), 'Edge'),
    (re.compile('OPR'), 'Opera'),
    (re.compile('Chrome'), 'Chrome'),
    (re.compile('Safari'), 'Safari'),
    (re.compile('Firefox'), 'Firefox'),
    (re.compile('IE'), 'Internet Explorer'),
)

DEVICES = (
    (re.compile('Windows Mobile'), 'Windows Mobile'),
    (re.compile('Android'), 'Android'),
    (re.compile('Linux'), 'Linux'),
    (re.compile('iPhone'), 'iPhone'),
    (re.compile('iPad'), 'iPad'),
    (re.compile('Mac OS X 10[._]9'), 'OS X Mavericks'),
    (re.compile('Mac OS X 10[._]10'), 'OS X Yosemite'),
    (re.compile('Mac OS X 10[._]11'), 'OS X El Capitan'),
    (re.compile('Mac OS X 10[._]12'), 'macOS Sierra'),
    (re.compile('Mac OS X 10[._]13'), 'macOS High Sierra'),
    (re.compile('Mac OS X 10[._]14'), 'macOS Mojave'),
    (re.compile('Mac OS X 10[._]15'), 'macOS Catalina'),
    (re.compile('Mac OS X 11'), 'macOS Big Sur'),
    (re.compile('Mac OS X 12'), 'macOS Monterey'),
    (re.compile('Mac OS X'), 'macOS'),
    (re.compile('NT 5.1'), 'Windows XP'),
    (re.compile('NT 6.0'), 'Windows Vista'),
    (re.compile('NT 6.1'), 'Windows 7'),
    (re.compile('NT 6.2'), 'Windows 8'),
    (re.compile('NT 6.3'), 'Windows 8.1'),
    (re.compile('NT 10.0'), 'Windows 10'),
    (re.compile('Windows'), 'Windows'),
)


@register.filter
def get_device(value):

    browser = None
    for regex, name in BROWSERS:
        if regex.search(value):
            browser = name
            break

    device = None
    for regex, name in DEVICES:
        if regex.search(value):
            device = name
            break

    if browser and device:
        return '%(browser)s on %(device)s' % {'browser': browser, 'device': device}

    if browser:
        return browser

    if device:
        return device

    return None
