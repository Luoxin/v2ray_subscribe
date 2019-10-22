from datetime import time

from orm import SubscribeCrawl, session

url = ""

# new_data = SubscribeCrawl(
#     id=int(time.time()),
#     url=url.replace(" ", ""),
#     type=1,
#     is_closed=False,
#     interval=3600,
#     next_time=0,
# )
# session.add(new_data)


session.query(SubscribeCrawl).filter(SubscribeCrawl.id == 1571721122).update({
    SubscribeCrawl.rule: {"need_proxy": True}
})

session.commit()
