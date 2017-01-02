import praw
from praw_test import getSubreddit, getPRAW
from handle import handle

def main():
    domains = ['youtube.com','m.youtube.com','youtu.be']
    r = getPRAW();
    r_posthardcore = getSubreddit(r,'posthardcore')
    r_spotmebot = getSubreddit(r,'spotmebot')
    for s in r_posthardcore.stream.submissions():
        if s.domain in domains:
            post_url = s.url
            post_title = s.title
            post = submitLinkPost(post_title,post_url,r_spotmebot)

def submitLinkPost(title,link,subreddit):
    submission = subreddit.submit(title=title,url=link)
    return submission


if __name__ == '__main__':
    main()
