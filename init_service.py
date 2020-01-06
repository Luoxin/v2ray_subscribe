"""
初始化基础的任务
"""
import multiprocessing
import threading

from api.time_info import keep_time_consistent
from conf.conf import NTP_SERVER_ENABLE

task_func_map = {
    keep_time_consistent: {
        "startup_mode": "thread",
    }
}


# process_pool = multiprocessing.Pool(3)


def start_task():
    for task, rule in task_func_map.items():
        startup_mode = "thread" if rule.get("startup_mode") is None else rule.get("startup_mode")
        enable = False if rule.get("enable") is not None else rule.get("enable")

        # 如果不开启这个任务，就直接查找下一个任务
        if not enable:
            continue

        if startup_mode == "thread":
            threading.Thread(target=task, daemon=True).start()

        # if startup_mode == "process":

        #     process_pool.apply_async(task)

    # process_pool.close()
    # process_pool.join()


def init_service():
    start_task()
