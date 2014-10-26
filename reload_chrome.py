import begin
import re
from remote_webkit_debug import ChromeShell, ChromeTab


def iterate_tabs():
    chromeShell = ChromeShell()
    for x in chromeShell.get_tabs():
        if ("chrome-extension:" in x["url"] or
            "chrome-devtools:" in x["url"]):
            break
        yield x


def listtabs():
    for x in iterate_tabs():
        print(x["url"])
        print(x["title"])


def find_tabs(pattern):
    ptn = re.compile(pattern)
    for tab in iterate_tabs():
        if ptn.search(tab["url"]) or ptn.search(tab["title"]):
            yield tab


def reload_tab(tabinfo):
    print("reload: {0}".format(tabinfo["title"]))
    chromeShell = ChromeShell()
    with chromeShell.pick_tab(tabinfo) as tab:
        tab.send_command("Page.reload")


def reload_tabs(pattern):
    for tab in find_tabs(pattern):
        reload_tab(tab)


@begin.start
def main(*args):
    if len(args) != 0:
        for pattern in args:
            reload_tabs(pattern)
    else:
        listtabs()
