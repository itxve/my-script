import requests, os, time, datetime, platform

# @ctoken    xhr接口获取
# @cid       https://www.iconfont.cn/collections/detail?&cid=45417

CTOKEN = "xxxx"


# Mac 声音文件在 /System/Library/Sounds/ 目录。


def show_notification(title, text):
    if platform.system() == "Darwin":
        os.system(
            """
                osascript -e 'display notification "{}" with title "{}" sound name "Glass"'
                """.format(
                text, title
            )
        )
    else:
        print(f"{text} :::::: {title}")


def now():
    return datetime.datetime.now()


def list_by_cid(id: str):
    response = requests.get(
        f"https://www.iconfont.cn/api/collection/detail.json?id={id}&t={now()}&ctoken={CTOKEN}"
    )
    res = response.json()["data"]
    collection = res["collection"]
    return (collection["description"] or collection["name"], res["icons"])


# 下载icon
def down_icon(
    dir: str,
    file_name: str,
    id: str,
):
    url = f"https://www.iconfont.cn/api/icon/iconInfo.json?id={id}&t={now()}&ctoken={CTOKEN}"
    response = requests.get(url)
    time.sleep(2)
    os.makedirs(f"./icons/{dir}", exist_ok=True)
    with open(f"./icons/{dir}/{file_name}.svg", "w", encoding="utf-8") as f:
        res = response.json()["data"]
        f.write(res["origin_file"])


def get_down(cids: list[str]):
    for cid in cids:
        print(f"---- start down cid {cid} -----")
        (dir, icons) = list_by_cid(cid)
        for icon in icons:
            down_icon(dir, icon["name"], icon["id"])
        print(f"---- end down cid {cid} -----")

    show_notification("icons down", "下载完成")


if __name__ == "__main__":
    get_down(["1912"])
