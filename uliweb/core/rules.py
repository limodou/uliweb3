from __future__ import print_function, absolute_import, unicode_literals
import os
import re
import inspect
from uliweb.utils.common import log
from uliweb.utils.sorteddict import SortedDict
import copy
from ..utils._compat import string_types, iterkeys, get_class, ismethod

class ReservedKeyError(Exception):pass

__exposes__ = SortedDict()
__no_need_exposed__ = []
__class_methods__ = {}
__app_rules__ = {}
__url_route_rules__ = []
__url_names__ = {}
static_views = []

reserved_keys = ['settings', 'redirect', 'application', 'request', 'response', 'error',
    'json']

def add_rule(map, url, endpoint=None, **kwargs):
    from werkzeug.routing import Rule
    kwargs['endpoint'] = endpoint
    try:
        map.add(Rule(url, **kwargs))
    except ValueError as e:
        log.info("Wrong url is %s, endpoint=%s" % (url, endpoint))
        raise
            
def merge_rules():
    from itertools import chain
    
    s = []
    index = {}
    for v in sorted(__no_need_exposed__ + list(chain(*__exposes__.values())), key=lambda x:x[4]):
        appname, endpoint, url, kw, timestamp = v
        if 'name' in kw:
            url_name = kw.pop('name')
        else:
            url_name = endpoint
        __url_names__[url_name] = endpoint
        methods = [y.upper() for y in kw.get('methods', [])]
        methods.sort()

        key = url, tuple(methods), kw.get('subdomain')
        i = index.get(key, None)
        if i is not None:
            s[i] = appname, endpoint, url, kw
        else:
            s.append((appname, endpoint, url, kw))
            index[key] = len(s)-1
            
    return s


def get_func(f):
    if inspect.ismethod(f):
        return f.__func__
    else:
        return f


def get_function_path(f):
    if hasattr(f, '__qualname__'):
        return f.__module__ + '.' + f.__qualname__
    elif getattr(f, '__self__', None):
        return f.__module__ + '.' + f.__self__.__name__ + '.' + f.__name__
    elif getattr(f, 'im_class', None):
        return f.__module__ + '.' + f.im_class.__name__ + '.' + f.__name__
    else:
        return f.__module__ + '.' + f.__name__


def get_classname(f):
    if hasattr(f, '__qualname__'):
        return f.__qualname__.rsplit('.', 1)[0]
    elif getattr(f, '__self__', None):
        return f.__self__.__name__
    elif getattr(f, 'im_class', None):
        return f.im_class.__name__


def clear_rules():
    global __exposes__, __no_need_exposed__, __url_names__
    __exposes__ = {}
    __no_need_exposed__ = []
    __url_names__ = {}

def set_app_rules(rules=None):
    global __app_rules__
    __app_rules__ = {}
    __app_rules__.update(rules or {})
    
def set_urlroute_rules(rules=None):
    """
    rules should be (pattern, replace)

    e.g.: ('/admin', '/demo')
    """
    global __url_route_rules__
    __url_route_rules__ = []
    for k, v in (rules or {}).values():
        __url_route_rules__.append((re.compile(k), v))

def get_endpoint(f):
    if ismethod(f):
        _class = get_class(f)
        endpoint = '.'.join([_class.__module__, _class.__name__, f.__name__])
    elif inspect.isfunction(f):
        endpoint = '.'.join([f.__module__, f.__name__])
    else:
        endpoint = f
    return endpoint

def get_template_args(appname, f):
    viewname, clsname = '', ''
    if ismethod(f):
        _class = get_class(f)
        clsname = _class.__name__
        viewname = f.__name__
    else:
        viewname = f.__name__
    return {'appname':appname, 'view_class':clsname, 'function':viewname} 
    
def expose(rule=None, **kwargs):
    e = Expose(rule, **kwargs)
    if e.parse_level == 1:
        return rule
    else:
        return e
    
class Expose(object):
    def __init__(self, rule=None, restful=False, replace=False, template=None,
                 layout=None, **kwargs):
        self.restful = restful
        self.replace = replace
        self.template = template
        self.layout = layout
        if inspect.isfunction(rule) or inspect.isclass(rule):
            self.parse_level = 1
            self.rule = None
            self.kwargs = {}
            self.parse(rule)
        else:
            self.parse_level = 2
            self.rule = rule
            self.kwargs = kwargs

    def _get_app_prefix(self, appname):
        if appname in __app_rules__:
            d = __app_rules__[appname]
            if not d:
                return
            if isinstance(d, str):
                return d
            else:
                return d.get('prefix')

    def _get_app_subdomin(self, appname):
        if appname in __app_rules__:
            d = __app_rules__[appname]
            if not d:
                return
            if isinstance(d, str):
                return
            else:
                return d.get('subdomain')

    def _fix_url(self, appname, rule):
        app_prefix = self._get_app_prefix(appname)
        if rule.startswith('/') and app_prefix:
            url = os.path.normcase(os.path.join(app_prefix, rule.lstrip('/'))).replace('\\', '/')
        else:
            if rule.startswith('!'):
                url = rule[1:]
            else:
                url = rule

        if len(url) > 1:
            url = url.rstrip('/')
        return url

    def _fix_route(self, rule):
        for k, v in __url_route_rules__:
            if k.match(rule):
                return k.sub(v, rule)
        return rule

    def _fix_kwargs(self, appname, v):
        _subdomain = self._get_app_subdomin(appname)
        if _subdomain is None:
            _subdomain = self.kwargs.get('subdomain')
        if _subdomain is None:
            return
        if _subdomain:
            v['subdomain'] = _subdomain
        else:
            v.pop('subdomain', None)
            
    def _get_path(self, f):
        m = f.__module__.split('.')
        s = []
        for i in m:
            if not i.startswith('views'):
                s.append(i)
        appname = '.'.join(s)
        return appname, '/'.join(s)
    
    def parse(self, f):
        if inspect.isfunction(f) or ismethod(f):
            func, result = self.parse_function(f)
            a = __exposes__.setdefault(func, [])
            a.append(result)
        else:
            self.parse_class(f)
            
    def parse_class(self, f):
        from uliweb.utils.date import now
        appname, path = self._get_path(f)
        clsname = f.__name__
        if self.rule:
            prefix = self.rule
        else:
            prefix = '/' + '/'.join([path, clsname])
        f.__exposed_url__ = prefix
        for name in dir(f):
            func = getattr(f, name)
            if (ismethod(func) or inspect.isfunction(func)) and not name.startswith('_'):
                if hasattr(func, '__exposed__') and func.__exposed__:
                    new_endpoint = '.'.join([func.__module__, f.__name__, name])
                    f_func = get_func(func)
                    if f_func in __exposes__:
                        for v in __exposes__.pop(f_func):
                            #__no_rule__ used to distinct if the view function has used
                            #expose to decorator, if not then __no_rule__ will be True
                            #then it'll use default url route regular to make url
                            if func.__no_rule__:
                                rule = self._get_url(appname, prefix, func)
                            else:
                                #check if the func has already rule
                                _old = func.__old_rule__.get(v[2])
                                #if keep, then it'll skip app prefix
                                if _old.startswith('!'):
                                    rule = _old[1:]
                                    if not rule.startswith('/'):
                                        raise ValueError("The rule of <!rule> definition should be start with '!/'")

                                else:
                                    rule = os.path.join(prefix, _old).replace('\\', '/')
                                    rule = self._fix_url(appname, rule)

                                func.__old_rule__['clsname'] = clsname
                                #save processed data
                                x = list(v)
                                x[1] = new_endpoint
                                x[2] = rule
                                setattr(func, '__saved_rule__', x)

                                #add subdomain process
                                self._fix_kwargs(appname, v[3])

                            rule = self._fix_route(rule)
                            __no_need_exposed__.append((v[0], new_endpoint, rule, v[3], now()))
                    else:
                        #maybe is subclass
                        v = copy.deepcopy(func.func_dict.get('__saved_rule__'))
                        if getattr(func, '__fixed_url__'):
                            rule = v[2]
                        else:
                            rule = self._get_url(appname, prefix, func)
                        rule = self._fix_route(rule)
                        if v and new_endpoint != v[1]:
                            if self.replace:
                                v[3]['name'] = v[3].get('name') or v[1]
                                setattr(func, '__template__', {'function':func.__name__, 'view_class':func.__old_rule__['clsname'], 'appname':appname})
                            else:
                                v[2] = rule
                            v[1] = new_endpoint
                            v[4] = now()
                            setattr(func, '__saved_rule__', v)

                            #add subdomain process
                            self._fix_kwargs(appname, v[3])
                            __no_need_exposed__.append(v)
                else:
                    rule = self._get_url(appname, prefix, func)
                    rule = self._fix_route(rule)
                    endpoint = '.'.join([f.__module__, clsname, func.__name__])
                    #process inherit kwargs from class
                    #add subdomain process
                    kw = {}
                    self._fix_kwargs(appname, kw)
                    x = appname, endpoint, rule, kw, now()
                    __no_need_exposed__.append(x)
                    setattr(func, '__exposed__', True)
                    setattr(func, '__saved_rule__', list(x))
                    setattr(func, '__old_rule__', {'rule':rule, 'clsname':clsname})
                    setattr(func, '__template__', None)
                    setattr(func, '__layout__', None)
                    setattr(func, '__fixed_url__', False)
    
    def _get_url(self, appname, prefix, f):
        args = inspect.signature(f).parameters
        if args:
            if ismethod(f):
                args = args[1:]
            args = ['<%s>' % x for x in args]
        if f.__name__ in reserved_keys:
            raise ReservedKeyError('The name "%s" is a reversed key, so please change another one' % f.__name__)
        prefix = prefix.rstrip('/')
        if self.restful:
            rule = self._fix_url(appname, '/'.join([prefix] + args[:1] + [f.__name__] +args[1:]))
        else:
            rule = self._fix_url(appname, '/'.join([prefix, f.__name__] +args))
        return rule
    
    def parse_function(self, f):
        from uliweb.utils.date import now
        args = inspect.signature(f).parameters
        if args:
            args = ['<%s>' % x for x in args]
        if f.__name__ in reserved_keys:
            raise ReservedKeyError('The name "%s" is a reversed key, so please change another one' % f.__name__)
        appname, path = self._get_path(f)
        if self.rule is None:
            if self.restful:
                rule = '/' + '/'.join([path] + args[:1] + [f.__name__] + args[1:])
            else:
                rule = '/' + '/'.join([path, f.__name__] + args)
        else:
            self.rule = self._fix_route(self.rule)
            rule = self.rule
        fixed_url = rule.startswith('!')
        rule = self._fix_url(appname, rule)
        endpoint = get_function_path(f)
        clsname = get_classname(f)
        setattr(f, '__exposed__', True)
        setattr(f, '__no_rule__', (self.parse_level == 1) or (self.parse_level == 2 and (self.rule is None)))
        if not hasattr(f, '__old_rule__'):
            setattr(f, '__old_rule__', {})

        getattr(f, '__old_rule__')[rule] = self.rule
        getattr(f, '__old_rule__')['clsname'] = clsname
        setattr(f, '__template__', self.template)
        setattr(f, '__layout__', self.layout)
        setattr(f, '__fixed_url__', fixed_url)

        kw = self.kwargs.copy()
        self._fix_kwargs(appname, kw)
        return f, (appname, endpoint, rule, kw, now())
    
    def __call__(self, f):
        from uliweb.utils.common import safe_import
        
        if isinstance(f, string_types):
            try:
                _, f = safe_import(f)
            except:
                log.error('Import error: rule=%s' % f)
                raise
        self.parse(f)
        return f
