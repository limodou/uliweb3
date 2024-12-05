![LOGO](https://raw.github.com/limodou/uliweb3/master/logos/uliweb_logo_media.png)

Uliweb Introduction
=====================

Limodou <limodou@gmail.com>

## About Uliweb3

Uliweb3 is a project for transferring uliweb from Python 2 to Python 3. The goal is to make it as simple as possible.
Uliweb is a full-stacked Python based web framework with three main design goals: reusability, configurability, and replaceability. All functionalities revolve around these goals. This project was created and led by Limodou <mailto:limodou@gmail.com>.

### Differences between Uliweb and Uliweb3

- [X] Remove taglib
- [X] Remove uaml
- [X] Remove rcssmin
- [X] Remove rjsmin
- [X] Remove pysimplesoap
- [X] Remove utils/rst.py
- [X] Remove bae
- [X] Remove heroku
- [X] Remove sae
- [X] Remove soap
- [X] Remove xmlrpc
- [X] Remove dbupload
- [X] Remove generic command, remain MultiView
- [X] Remove objcache
- [X] Remove develop
- [X] Remove template combine support
- [X] Remove qqmail support

### Unfinished Modules

- [X] uliweb-ui
- [X] uliweb-layout
- [X] uliweb-apps
- [ ] Werkzeug upgrade

### Bugs

- [ ] Werkzeug Debug seems failed

### License

Uliweb3 is released under BSD license.

### Features

* **Organization**
  * MVT (Model View Template) development model.
  * Distributed development but unified management. Uliweb organizes a project with small apps. Each app can have its own configuration file (settings.ini), template directory, and static directory. Existing apps can be easily reused, but are treated as a compound web application project if configured as such. Developers can also reference static files and templates between apps, thus easing inter-application data exchange. All apps in a project are loaded by default if INSTALLED_APPS is not configured in the configuration file. All separate app configuration files are automatically processed at project startup.

* **URL Mapping**
  * Flexible and powerful URL mapping. Uliweb uses werkzeug's routing module. User can easily define a URL, which in turn can be easily bound with a view function. URLs can also be created reversely according to the view function name. It supports argument definitions in URLs and default URL mapping to a view function.

* **View and Template**
  * View templates can be automatically applied. If you return a dict variable from view function, Uliweb will automatically try to match and apply a template according to the view function name.
  * Environment execution mode. Each view function will be run in an environment, which eliminates the need to write many import statements. Plus there are already many objects that can be used directly, for example: request, response, etc. This is DRY and saves a lot of coding.
  * Developers can directly use Python code in a template; the Python code does not need to be indented as long as a pass statement is added at the end of each code block. Uliweb also supports child template inclusion and inheritance.

* **ORM**
  * Uliorm is based on SQLAlchemy package, so you can use Model layer and SQL expression layer both.
  * Uliorm integrates with alembic package, you can use it to migrate database automatically.

* **I18n**
  * Can be used in Python and template files.
  * Browser language and cookie settings are supported including automatic language switching.
  * Provides a command line tool that developers can use to extract .po files. This can happen either at the app level or project level process. It can automatically merge .pot files to existing .po files.

* **Extension**
  * Dispatch extension. This is a dispatch processing mechanism that utilizes different types of dispatch points. So you can write procedures to carry out special processes and bind them to these dispatch points. For example, database initialization, I18n process initialization, etc.
  * Middleware extension. It's similar to Django. You can configure it in configuration files. Each middleware can process the request and response objects.
  * Special function calls in the views module initial process. If you write a special function named __begin__, it'll be processed before any view function can be processed, this allows developers to do some module level processing at that point, for example: check the user authentication, etc.

* **Command Line Tools**
  * Creates project, creates apps, and include the basic essential directory structure, files and code.
  * Export static files, you can export all available apps' static files to a special directory. Also supports CSS and JS combination and compress process.
  * Startup a development web server that's supports debugging and auto reload.
  * Apps can also have its own command line tools. For example: orm, auth, etc.

* **Deployment**
  * Supports uwsgi.

* **Development**
  * Provide a development server, and can be automatically reload when some module files are modified.
  * Enhanced debugging, you can check the error traceback, template debugging is also supported.

### Community

* Mailing List: https://groups.google.com/g/uliweb

### Links

* **Uliweb** Project Homepage https://github.com/limodou/uliweb3
* **Uliweb-doc** Documentation Project http://github.com/limodou/uliweb-doc
* **Uliweb-doc Online** Document https://limodou.github.io/uliweb-doc/zh_CN/uliweb3/index.html
