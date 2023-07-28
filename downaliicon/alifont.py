import requests, os, time, datetime, platform


# @ctoken    xhr接口获取
# @cid       https://www.iconfont.cn/collections/detail?&cid=45417

CTOKEN = "VgSZj3K7VhsTXC3LAkvFPNqN"
Cookie = "cna=DAgsHeUClT8CAXrncHD9+Q8R; locale=zh-cn; u=5894601; u.sig=eakV0Mcm4a_4u3ffvWC78ZuGN7KnmwV08aTIrJ4xweo; xlly_s=1; ctoken=VgSZj3K7VhsTXC3LAkvFPNqN; EGG_SESS_ICONFONT=Hu68kBY7XO7C6Udp3T99M1asKmUZ0gxjps8xjTrjx4ZtNCIR_nFu9Li15nxoPAWLXfFm3FTK5uTUW_7F7i0Y0KZBFkAwajV2DddSsyWipXFLnPrdkfPQRXupQef3gppMY-oMxKoNdCebauGYz5Xpr2OAudXaOYi3g2poPBMBNXE7XInBPXpXaUNnk5HAbjbUQqSrWmPMiWJZlG2u7BtKntYQDhEP2lOYIwO3BvHJRgkWcUKiVUX3s725J9BonVmm9KQXV-uOFE6Zeoag85mc54q7Ddx6MjxkM_8DYGclpug=; isg=BMLCu33IEl7mZAhDBO4atoe3E84kk8atoFkBuQzbXzXnX2PZ9SIGvARZD1sjDz5F"
headers = {"Referer": "https://www.iconfont.cn/", "Cookie": Cookie}


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
    return datetime.datetime.now().timestamp()


def down_file(source_url):
    res = requests.get(source_url, headers=headers)
    return res.content


# @param type
# 默认 空为 icon


def list_by_cid(id: str, kind_type: str):
    response = requests.get(
        f"https://www.iconfont.cn/api/collection/detail.json?id={id}&type={kind_type}&t={now()}&ctoken={CTOKEN}",
        headers=headers,
    )
    res = response.json()["data"]
    collection = res["collection"]
    return (collection["name"] or collection["description"], res["icons"])


# 下载icon
def down_icon_file(
    dir: str,  # 文件夹
    file_name: str,  # 文件名
    id: str,  # id
):
    url = f"https://www.iconfont.cn/api/icon/iconInfo.json?id={id}&t={now()}&ctoken={CTOKEN}"
    response = requests.get(url, headers=headers)
    time.sleep(2)
    os.makedirs(f"./down/Icon/{dir}", exist_ok=True)
    with open(f"./down/Icon/{dir}/{file_name}.svg", "w", encoding="utf-8") as f:
        res = response.json()["data"]
        f.write(res["origin_file"])


def down_lottie_mp4(dir: str, file_name: str, id: str, cid: str):
    url = f"https://www.iconfont.cn/api/svg/svgInfo.json?id={id}&cid={cid}&t={now()}&ctoken={CTOKEN}"
    response = requests.get(url, headers=headers)
    time.sleep(2)
    os.makedirs(f"./down/Lottie/{dir}", exist_ok=True)
    with open(f"./down/Lottie/{dir}/{file_name}.mp4", "wb") as f:
        res = response.json()["data"]
        mp4_url = res["preview_video"]
        f.write(down_file(f"https:{mp4_url}"))


def down_矢量插画库_svg(dir: str, file_name: str, id: str, cid: str):
    url = f"https://www.iconfont.cn/api/svg/svgInfo.json?id={id}&cid={cid}&t={now()}&ctoken={CTOKEN}"
    response = requests.get(url, headers=headers)
    time.sleep(2)
    os.makedirs(f"./down/矢量插画库/{dir}", exist_ok=True)
    with open(f"./down/矢量插画库/{dir}/{file_name}.svg", "wb") as f:
        res = response.json()["data"]
        svg_url = res["origin_file"]
        f.write(down_file(f"https:{svg_url}"))


def get_down_icon_by_cid(cids: list[str]):
    print(f"---- Icon下载... -----")
    for cid in cids:
        (dir, icons) = list_by_cid(cid, "icon")
        for icon in icons:
            down_icon_file(dir, icon["name"], icon["id"])

    show_notification("icons down", "下载完成")


def get_down_lottie_by_cid(cids: list[str]):
    print(f"---- Lottie下载... -----")
    for cid in cids:
        (dir, icons) = list_by_cid(cid, "illustration")
        for icon in icons:
            down_lottie_mp4(dir, icon["name"], icon["id"], cid)

    show_notification("Lottie down", "下载完成")


def get_down_矢量插画库_by_cid(cids: list[str]):
    print(f"---- 矢量插画库下载... -----")
    for cid in cids:
        (dir, icons) = list_by_cid(cid, "illustration")
        for icon in icons:
            down_矢量插画库_svg(dir, icon["name"], icon["id"], cid)

    show_notification("矢量插画库 down", "下载完成")


# 下载购物车 使用 控制台console 获取Icon Id
# JSON.parse(localStorage.__iconfont_car_icons__).map(t=>({id:String(t.id),name:t.name}))
# icons = [{"id": "36096095", "name": "大雨"}, {"id": "36622621", "name": "add"}]
# for icon in icons:
#     down_icon_file("test", icon["name"], icon["id"])
###


if __name__ == "__main__":
    # get_down_icon_by_cid(["45596"])
    # get_down_lottie_by_cid(["44475"])
    # get_down_矢量插画库_by_cid(["45786"])

    icons = [{"id": "36096095", "name": "大雨"}, {"id": "36622621", "name": "add"}]
    ##
    for icon in icons:
        down_icon_file("test", icon["name"], icon["id"])
