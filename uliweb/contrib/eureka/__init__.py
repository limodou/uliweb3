from uliweb import settings

#settings.LOGIN.token_timeout
def startup_installed(sender):
    import py_eureka_client.eureka_client as eureka_client

    # 提供给py_eureka_client使用
    eureka_client.init(eureka_server=settings.EUREKA.eureka_server,
                       app_name=settings.EUREKA.app_name,
                       # 当前组件的主机名，可选参数，如果不填写会自动计算一个，如果服务和 eureka 服务器部署在同一台机器，请必须填写，否则会计算出 127.0.0.1
                       instance_host=settings.EUREKA.server_host,
                       instance_port=settings.EUREKA.server_port,
                       # 调用其他服务时的高可用策略，可选，默认为随机
                       ha_strategy=settings.EUREKA.ha_strategy)

