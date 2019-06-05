def startup_installed(sender):
    from uliweb import functions
    
    server_timezone = sender.settings.GLOBAL.TIME_ZONE
    functions.set_server_timezone(server_timezone)
    
    local_timezone = sender.settings.GLOBAL.LOCAL_TIME_ZONE
    #if use timezone, default value of local_timezone is same as server_timezone
    if server_timezone and not local_timezone:
        local_timezone = server_timezone
    functions.set_local_timezone(local_timezone)

def to_ltimezone(dt):
    from uliweb import request, settings
    if settings.GLOBAL.TIME_ZONE:
        tzinfo = getattr(request,"tzinfo",None)
        if tzinfo:
            dt = tzinfo.convert(dt)
    return dt
