from uliweb import settings, functions
import logging
from pendulum import timezone

log = logging.getLogger(__name__)

def startup_installed(sender):
    server_timezone = sender.settings.GLOBAL.TIME_ZONE
    functions.set_server_timezone(server_timezone)

    local_timezone = sender.settings.GLOBAL.LOCAL_TIME_ZONE
    #if use timezone, default value of local_timezone is same as server_timezone
    if server_timezone and not local_timezone:
        local_timezone = server_timezone
    functions.set_local_timezone(local_timezone)

def to_ltimezone(dt):
    from uliweb import request
    if settings.GLOBAL.TIME_ZONE:
        tzinfo = getattr(request,"tzinfo",None)
        if not tzinfo:
            tz = settings.GLOBAL.LOCAL_TIME_ZONE
            if tz:
                tzinfo = timezone(tz)
        if tzinfo:
            dt = tzinfo.convert(dt)
    return dt

# refer contrib.orm.after_init_apps
def after_init_orm(sender):
    from uliweb import orm
    from uliweb.utils.common import import_attr

    def get_func(var_path):
        func_path = settings.get_var(var_path)
        return import_attr(func_path) if func_path else None

    orm.set_timezone_support(get_func('ORM/TIMEZONE_SUPPORT'))
    orm.set_now(get_func('ORM/NOW'))
    orm.set_to_datetime(get_func('ORM/TO_DATETIME'))
    orm.set_to_timezone(get_func('ORM/TO_TIMEZONE'))
    orm.set_to_ltimezone(get_func('ORM/TO_LTIMEZONE'))

def orm_now():
    server_timezone = functions.get_server_timezone()
    if server_timezone == None:
        return functions.now()
    else:
        #return UTC datetime for auto_now_add
        return functions.utc_now()

def orm_to_datetime(*args, **kwargs):
    dt = functions.to_datetime(*args, **kwargs)
    server_timezone = functions.get_server_timezone()
    if not server_timezone:
        if functions.is_aware(dt):
            log.error("receive a timezone-aware datetime (%s) when settings.GLOBAL.TIME_ZONE is None"%(dt))
            raise ValueError("Timezone-aware datetimes are not accepted, when settings.GLOBAL.TIME_ZONE is None")
    else:
        if functions.is_naive(dt):
            log.warn("received a naive datetime (%s) while settings.GLOBAL.TIME_ZONE not None"%(dt))
            dt = server_timezone.convert(dt)
    return dt

def timezone_support():
    return bool(functions.get_server_timezone())
