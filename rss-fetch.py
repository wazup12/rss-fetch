import feedparser
from subprocess import check_output
import os

# OPTIONS -------------------------------- #
LIGHT_MODE = False
NUM_SPACES = 2
TITLE_COLOR = "RED"
# ---------------------------------------- #

COLOR_NAMES = ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE"]
COLORS = {}
BASE = "\033["


def create_color_list():
    for i in range(8):
        COLORS.update({f"DARK_{COLOR_NAMES[i]}": f"{BASE}3{i}m"})
        COLORS.update({f"LIGHT_{COLOR_NAMES[i]}": f"{BASE}9{i}m"})


def get_color(key):
    create_color_list()

    if key.startswith("DARK_") or key.startswith("LIGHT_"):
        pass
    elif LIGHT_MODE:
        key = "DARK_" + key
    else:
        key = "LIGHT_" + key

    return COLORS.get(key)


def get_date():
    date = check_output(["date", "-I"]).strip().decode("utf-8")
    return date


BOLD = "\033[1m"
UNDERLINE = "\033[4m"
ITALICS = "\033[3m"
RESET = "\033[0m"
TITLE_COLOR = get_color(TITLE_COLOR)
INDENT = " " * NUM_SPACES
DATE = get_date()
info = ""


def retrieve_urls():
    urls = []

    with open("feeds.txt", "r") as file:
        urls = file.read().split("\n")

    return urls


def process_urls(urls, out_dir="out", out_file=f"{DATE}.feed"):
    for url in urls:
        if not url:
            continue
        parse_url(url)

    out_file_path = os.path.join(out_dir, out_file)
    os.makedirs(out_dir, exist_ok=True)

    with open(out_file_path, "w") as file:
        file.write(info)


def parse_url(url):
    global info
    feed = feedparser.parse(url)

    title = feed.feed.title
    info += get_feed_info(title)

    for entry in feed.entries:
        # print(entry.keys())
        entry_title = entry.title
        entry_link = entry.link
        entry_summary = entry.summary

        info += get_entry_info(entry_title, entry_link, summary=entry_summary)


def get_feed_info(title):
    return f"{BOLD}{title.upper()}:{RESET}\n"


def get_entry_info(title, url, date="", summary=""):
    if not title:
        return ""

    string = f"{INDENT}{TITLE_COLOR}{title}{RESET}\n"

    if url:
        string += f"{INDENT} [{ITALICS}{url}{RESET}]\n"

    return string


def print_feed(out_dir="out"):
    feeds = os.listdir(out_dir)
    feeds.sort(reverse=True)

    # return latest feed
    print(f"Latest feed: {feeds[0]}")
    print()

    with open(os.path.join(out_dir, feeds[0]), "r") as file:
        print(file.read())


if __name__ == "__main__":
    urls = retrieve_urls()
    process_urls(urls)
    print_feed()
