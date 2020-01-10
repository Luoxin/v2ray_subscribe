from datetime import time

from orm import subscribe_crawl, session

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


session.query(subscribe_crawl).filter(subscribe_crawl.id == 1571721122).update(
    {subscribe_crawl.rule: {"need_proxy": True}}
)

session.commit()
