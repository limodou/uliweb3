#! /usr/bin/env python
#coding=utf-8

from uliweb import Middleware, settings
from pendulum import timezone
from pendulum.tz.zoneinfo.exceptions import InvalidTimezone

class TimezoneMiddleware(Middleware):
    def __init__(self, application, settings):
        self._time_zone = settings.GLOBAL.TIME_ZONE
        self._local_time_zone = settings.GLOBAL.LOCAL_TIME_ZONE
        if self._time_zone and not self._local_time_zone:
            self._local_time_zone = self._time_zone
        self._cookie_key = settings.TIMEZONE.cookie_key

    def process_request(self, request):
        if self._time_zone:
            tz = None
            tzinfo = None
            if request.user:
                tz = request.user.timezone
            if not tz and request.cookies:
                v = request.cookies.get(self._cookie_key)
                if v:
                    tz = v
            if not tz:
                tz = self._local_time_zone
            if tz:
                try:
                    tzinfo = timezone(tz)
                except InvalidTimezone as e:
                    tz = settings.GLOBAL.LOCAL_TIME_ZONE
                    tzinfo = timezone(tz)
            request.tz = tz
            request.tzinfo = tzinfo
