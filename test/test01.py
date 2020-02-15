import psutil

for pid in psutil.pids():
    try:
        p = psutil.Process(pid)
        if pid == 0 or len(p.cmdline()) == 0:
            continue
        for connection in p.connections():
            if (
                connection.type == 1
                and (connection.laddr.port == 1086 if connection.laddr != () else False)
                or (connection.raddr.port != 1086 if connection.laddr == () else False)
            ):
                print(pid)
    except (PermissionError, psutil.AccessDenied, psutil.NoSuchProcess):
        pass
