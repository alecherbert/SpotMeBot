import praw
import threading
from praw_test import getSubreddit, getPRAW
from handle import handle

domains = ['youtube.com','m.youtube.com','youtu.be']
subs_to_copy = ['posthardcore','metalcore','listentothis']

def main():
    r = getPRAW();
    r_spotmebot = getSubreddit(r,'spotmebot')
    threads = []
    for sub in subs_to_copy:
        t = threading.Thread(target=copyFromSubreddit, args=(sub,r_spotmebot))
        threads.append(t)
        t.start()

def copyFromSubreddit(from_sub_name,to_sub):
    r = getPRAW();
    from_sub = getSubreddit(r,from_sub_name)
    for s in from_sub.stream.submissions():
        if s.domain in domains:
            post_url = s.url
            post_title = s.title
            post = submitLinkPost(post_title,post_url,to_sub,from_sub_name)

def submitLinkPost(title,link,subreddit,from_text):
    title += " - from /r/"+from_text
    submission = subreddit.submit(title=title,url=link)
    return submission


if __name__ == '__main__':
    main()
