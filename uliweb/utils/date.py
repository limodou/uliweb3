from __future__ import print_function, absolute_import, unicode_literals
import time, re
from datetime import tzinfo, timedelta, datetime, date, time as time_
from .sorteddict import SortedDict
from ._compat import string_types, PY2, integer_types
from pendulum import timezone, timezones, UTC, parse

__server_timezone__ = None
__local_timezone__ = None

class DateError(Exception):pass
class TimeFormatError(Exception):pass

ZERO = timedelta(0)

def set_server_timezone(tz):
    import os
    global __server_timezone__

    #handle FixedTimezone case
    if hasattr(tz,"name"):
        tz = tz.name

    if tz:
        #Set environ, similar with django: https://juejin.im/post/5848b301128fe1006907d5ed
        os.environ['TZ'] = tz
        __server_timezone__ = timezone(tz)
    else:
        __server_timezone__ = None

def get_server_timezone():
    return __server_timezone__

def set_local_timezone(tz):
    global __local_timezone__
    if tz:
        __local_timezone__ = timezone(tz)
    else:
        __local_timezone__ = None

def get_local_timezone():
    return __local_timezone__

def get_timezones():
    return timezones

def pick_timezone(*args):
    for x in args:
        if x:
            if isinstance(x,tzinfo):
                return x
            tz = timezone(x)
            if tz:
                return tz

def is_aware(value):
    return value.utcoffset() is not None

def is_naive(value):
    return value.utcoffset() is None

def now(tzinfo=None):
    global __server_timezone__
    tz = pick_timezone(tzinfo, __server_timezone__)
    return datetime.now(tz)

def utc_now():
    return datetime.now(UTC)

def today(tzinfo=None):
    d = now(tzinfo)
    return to_date(d, tzinfo)

def to_timezone(dt, tzinfo=None):
    """
    Convert a datetime to timezone
    """
    if not dt:
        return dt
    tz = pick_timezone(tzinfo, __server_timezone__)
    if not tz:
        return dt
    dttz = getattr(dt, 'tzinfo', None)
    if not dttz:
        return dt.replace(tzinfo=tz)
    else:
        return dt.astimezone(tz)

def to_date(dt, tzinfo=None, format=None):
    """
    Convert a datetime to date with tzinfo
    """
    d = to_datetime(dt, tzinfo, format)
    if not d:
        return d
    return date(d.year, d.month, d.day)

def to_time(dt, tzinfo=None, format=None):
    """
    Convert a datetime to time with tzinfo
    """
    d = to_datetime(dt, tzinfo, format)
    if not d:
        return d
    return time_(d.hour, d.minute, d.second, d.microsecond, tzinfo=d.tzinfo)

def to_datetime(dt, tzinfo=None, format=None):
    """
    Convert a date or time to datetime with tzinfo
    """
    if not dt:
        return dt

    tz = pick_timezone(tzinfo, __server_timezone__)

    if isinstance(dt, string_types):
        try:
            d = parse(dt, strict=False)
        except Exception:
            return None
        d = d.replace(tzinfo=tz)
        if not tz:
            d = datetime(d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond)
    else:
        d = datetime(getattr(dt, 'year', 1970), getattr(dt, 'month', 1),
            getattr(dt, 'day', 1), getattr(dt, 'hour', 0), getattr(dt, 'minute', 0),
            getattr(dt, 'second', 0), getattr(dt, 'microsecond', 0))
        if not getattr(dt, 'tzinfo', None):
            d = d.replace(tzinfo=tz)
            return d
        else:
            d = d.replace(tzinfo=dt.tzinfo)
    return to_timezone(d, tzinfo)

def to_local(dt, tzinfo=None):
    tz = pick_timezone(tzinfo, __local_timezone__)
    return to_datetime(dt, tzinfo=tz)

def to_string(dt, microsecond=False, timezone=True):
    if isinstance(dt, datetime):
        format = '%Y-%m-%d %H:%M:%S'
        if microsecond:
            format += '.%f'
        if timezone:
            format += ' %Z'
        return strftime(dt, format).rstrip()
    elif isinstance(dt, date):
        return strftime(dt, '%Y-%m-%d')
    elif isinstance(dt, time_):
        format = '%H:%M:%S'
        if microsecond:
            format += '.%f'
        return strftime(dt, format)

re_time = re.compile(r'(\d+)([s|ms|h|m])')
def parse_time(t):
    """
    Parse string time format to microsecond
    """
    if isinstance(t, (str, unicode)):
        b = re_time.match(t)
        if b:
            v, unit = int(b.group(1)), b.group(2)
            if unit == 's':
                return v*1000
            elif unit == 'm':
                return v*60*1000
            elif unit == 'h':
                return v*60*60*1000
            else:
                return v
        else:
            raise TimeFormatError(t)
    elif isinstance(t, integer_types):
        return t
    else:
        raise TimeFormatError(t)

def _findall(text, substr):
    # Also finds overlaps
    sites = []
    i = 0
    while 1:
        j = text.find(substr, i)
        if j == -1:
            break
        sites.append(j)
        i = j+1
    return sites

# I hope I did this math right. Every 28 years the
# calendar repeats, except through century leap years
# excepting the 400 year leap years. But only if
# you're using the Gregorian calendar.

if PY2:
    def strftime(dt, fmt):
        # WARNING: known bug with "%s", which is the number
        # of seconds since the epoch. This is too harsh
        # of a check. It should allow "%%s".
        import datetime

        fmt = fmt.replace("%s", "s")
        if isinstance(dt, datetime.time):
            return dt.strftime(fmt)

        if dt.year > 1900:
            return time.strftime(fmt, dt.timetuple())

        year = dt.year
        # For every non-leap year century, advance by
        # 6 years to get into the 28-year repeat cycle
        delta = 2000 - year
        off = 6*(delta // 100 + delta // 400)
        year = year + off

        # Move to around the year 2000
        year = year + ((2000 - year)//28)*28
        timetuple = dt.timetuple()
        s1 = time.strftime(fmt, (year,) + timetuple[1:])
        sites1 = _findall(s1, str(year))

        s2 = time.strftime(fmt, (year+28,) + timetuple[1:])
        sites2 = _findall(s2, str(year+28))

        sites = []
        for site in sites1:
            if site in sites2:
                sites.append(site)

        s = s1
        syear = "%4d" % (dt.year,)
        for site in sites:
            s = s[:site] + syear + s[site+4:]
        return s
else:
    def strftime(dt, fmt):
        return dt.strftime(fmt)


#if __name__ == '__main__':
#    GMT8 = timezone('GMT +8')
#    d = to_datetime('2011-9-13 20:14:15', tzinfo=GMT8)
#    print repr(d)
#    set_timezone(UTC)
#    print repr(to_datetime(d))
#    set_local_timezone('GMT +8')
#    print get_local_timezone()
#    print repr(to_local(d))