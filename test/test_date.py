from __future__ import print_function, absolute_import, unicode_literals
from uliweb.utils import date
from datetime import datetime

def test():
    """
    >>> set(["Asia/Shanghai","America/Chicago","Etc/GMT+8"]) < set(date.get_timezones())
    True
    >>> date.timezone('Asia/Shanghai') # doctest:+ELLIPSIS
    Timezone('Asia/Shanghai')
    >>> AsiaShanghai = date.timezone('Asia/Shanghai')
    >>> d = datetime(2011, 9, 13, 20, 14, 15, tzinfo=AsiaShanghai)
    >>> date.to_timezone(d, date.UTC).isoformat() 
    '2011-09-13T12:14:15+00:00'
    >>> date.to_datetime('2011-9-13 20:14:15', tzinfo=date.UTC)
    DateTime(2011, 9, 13, 20, 14, 15, tzinfo=Timezone('UTC'))
    >>> d = date.to_datetime('2011-9-13 20:14:15', tzinfo=AsiaShanghai)
    >>> d
    DateTime(2011, 9, 13, 20, 14, 15, tzinfo=Timezone('Asia/Shanghai'))
    >>> c = datetime(2011, 9, 13, 20, 14, 15)
    >>> date.to_datetime(c, tzinfo=AsiaShanghai)
    datetime.datetime(2011, 9, 13, 20, 14, 15, tzinfo=Timezone('Asia/Shanghai'))
    >>> date.to_datetime(d, tzinfo=date.UTC)
    datetime.datetime(2011, 9, 13, 12, 14, 15, tzinfo=Timezone('UTC'))
    >>> date.set_server_timezone(date.UTC)
    >>> date.to_datetime(d)
    datetime.datetime(2011, 9, 13, 12, 14, 15, tzinfo=Timezone('UTC'))
    >>> date.to_date('2011-9-13 20:14:15')
    datetime.date(2011, 9, 13)
    >>> date.to_datetime('2011-9-13 20:14:15')
    DateTime(2011, 9, 13, 20, 14, 15, tzinfo=Timezone('UTC'))
    >>> date.to_datetime('2011-9-13 20:14:15',tzinfo=AsiaShanghai)
    DateTime(2011, 9, 13, 20, 14, 15, tzinfo=Timezone('Asia/Shanghai'))
    >>> date.to_date('2011-9-13 20:14:15', tzinfo=date.UTC)
    datetime.date(2011, 9, 13)
    >>> date.to_time('2011-9-13 20:14:15')
    datetime.time(20, 14, 15, tzinfo=Timezone('UTC'))
    >>> date.to_time('2011-9-13 20:14:15', tzinfo=date.UTC)
    datetime.time(20, 14, 15, tzinfo=Timezone('UTC'))
    >>> date.to_string(date.to_date('2011-9-13 20:14:15'))
    '2011-09-13'
    >>> date.to_string(date.to_datetime('2011-9-13 20:14:15'))
    '2011-09-13 20:14:15 UTC'
    >>> date.to_string(date.to_time('2011-9-13 20:14:15'))
    '20:14:15'
    >>> date.to_timezone(None)
    >>> date.to_datetime(None)
    >>> date.to_date(None)
    >>> date.to_time(None)
    >>> date.set_local_timezone('Asia/Shanghai')
    >>> date.to_local(d)
    datetime.datetime(2011, 9, 13, 20, 14, 15, tzinfo=Timezone('Asia/Shanghai'))
    >>> date.timezone('Asia/Shanghai')
    Timezone('Asia/Shanghai')
    """
    
def test_microsecond():
    """
    >>> date.to_datetime('2012-08-01 16:41:12.5200')
    DateTime(2012, 8, 1, 16, 41, 12, 520000, tzinfo=Timezone('UTC'))
    >>> a = datetime(2012,8,1,16,41,12,5200)
    >>> print(a)
    2012-08-01 16:41:12.005200
    >>> b = date.to_datetime(a)
    >>> b
    datetime.datetime(2012, 8, 1, 16, 41, 12, 5200, tzinfo=Timezone('UTC'))
    >>> date.to_string(b, microsecond=True)
    '2012-08-01 16:41:12.005200 UTC'
    >>> date.to_string(b, timezone=False)
    '2012-08-01 16:41:12'
    """