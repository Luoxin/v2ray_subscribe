import multiprocessing
import threading

from api.time_info import keep_time_consistent

task_func_map = {
    keep_time_consistent: {
        # "startup_mode": "process"
    }
}

# process_pool = multiprocessing.Pool(3)


def start_task():
    for task, rule in task_func_map.items():
        print("启动一个任务")
        startup_mode = (
            "thread" if rule.get("startup_mode") is None else rule.get("startup_mode")
        )
        if startup_mode == "thread":
            threading.Thread(target=task, daemon=True).start()

        # if startup_mode == "process":

        #     process_pool.apply_async(task)

    # process_pool.close()
    # process_pool.join()
