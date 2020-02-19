import os


def get_conf_file_path() -> str:
    return find_file("conf.yaml")


def get_project_root_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))


def find_file(file_name):
    conf_path_list = [
        os.path.join(get_project_root_path(), file_name).replace("\\", "/"),
        os.path.join(get_project_root_path(), "conf", file_name).replace("\\", "/"),
        str(os.path.abspath(os.getcwd() + file_name)).replace("\\", "/"),
        str(os.path.join(os.getcwd(), "conf", file_name)).replace("\\", "/"),
    ]

    for conf_path in conf_path_list:
        if os.path.exists(conf_path):
            return conf_path

    print("无法找到配置文件 {}".format(conf_path_list))
