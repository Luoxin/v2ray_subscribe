import sys

sys.path("..")
sys.path("../../")

from watchdog.observers import Observer
from watchdog.events import *
import time


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        pass
        # if event.is_directory:
        #     print(
        #         "directory moved from {0} to {1}".format(
        #             event.src_path, event.dest_path
        #         )
        #     )
        # else:
        #     print("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
        file_path = event.src_path

        # 如果不是文件夹并且以json结尾，那么认为这个是一个服务
        if not event.is_directory and event.src_path.endswith(".json"):
            # 把文件名的后缀 .json 去掉获取到一个节点名
            node_name_item = file_path.replace(".json", "").split(".")

            if len(node_name_item) > 1:
                category_name = node_name_item[0]
            else:
                return

            # 如果是服务类型的
            if node_name_item[0] == "service":
                server_name = node_name_item[1]
                with open(os.path.join())

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))


if __name__ == "__main__":
    path = "D:/迅雷啊在"
    observer = Observer()
    event_handler = FileEventHandler()
    # Windows
    observer.schedule(event_handler, path, False)
    # Linux、服务器
    #     observer.schedule(event_handler, path, False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
