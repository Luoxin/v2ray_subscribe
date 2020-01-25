import os


def get_file_list_by_file_path(
    root_dir_path: str = os.getcwd(),
    recursion: bool = False,
    show_file: bool = True,
    show_dir: bool = True,
    only_show_postfix: bool = False,
    sort_type: int = 0,
    sort_key=None,
) -> list:
    """ 获取文件列表
    :param root_dir_path 要搜索的路径
    :param recursion 是否需要查找下一级数据
    :param show_file 是否显示文件
    :param show_dir 是否显示目录
    :param only_show_postfix 是否仅展示后缀
    :param sort_type 排序类型
                    0 不排序
                    1 字母升序
                    2 字母降序
    :param sort_key 排序的比较元素，同sort函数的key
    :return: 文件列表
    """

    def add_with_path(root: str, sub_path: str):
        """ 添加找到的文件路径并保证路径不重复
        :param root: 
        :param sub_path: 
        :return: 
        """
        if only_show_postfix:
            if os.path.isfile(os.path.join(root, sub_path)):
                file = os.path.splitext(sub_path)[-1]
        else:
            file = os.path.join(root, sub_path)

        if root == "" or path == "" or file == "":
            return

        if file not in result_set:
            result_set.add(file)

    result_set = set()
    try:
        if not os.path.exists(root_dir_path) and os.path.isdir(root_dir_path):
            raise ValueError("can not find path or is not dir")
        for dir_path, dir_names, file_names in os.walk(root_dir_path):
            if show_file:
                for path in file_names:
                    add_with_path(dir_path, path)

            if show_dir and not only_show_postfix:
                for path in dir_names:
                    add_with_path(dir_path, path)

            if not recursion:
                break
    except Exception as e:
        print("\n".join(e.args))
    finally:
        result_list = list(result_set)
        if sort_type is 1:
            result_list.sort(key=sort_key)
        elif sort_type is 2:
            result_list.sort(key=sort_key, reverse=True)

        return result_list


def get_project_root_path():
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


if __name__ == "__main__":
    fl = get_file_list_by_file_path("C:/Program Files/JetBrains/IntelliJ IDEA 2018.3.6")
    print(fl)
