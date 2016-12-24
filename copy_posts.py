import praw



def main():
    fp = open("required_copyposts.txt","r")
    info = fp.read().split("\n")
    fp.close()
    user_agent = info[0]
    client_id = info[1]
    client_secret = info[2]
    password = info[3]
    username = info[4]
    r = praw.Reddit(client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent,
                    username=username,
                    password=password)
    domains = ['youtube.com','m.youtube.com','youtu.be']
    r_posthardcore = r.subreddit('posthardcore')
    r_spotmebot = r.subreddit('spotmebot')
    for s in r_posthardcore.stream.submissions():
    	if s.domain in domains:
    		post_url = s.url
    		post_title = s.title
    		post = r_spotmebot.submit(title=post_title,url=post_url)



if __name__ == '__main__':
	main()
