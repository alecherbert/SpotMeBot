import praw
from requests.exceptions import ConnectionError, HTTPError

def handle(f):
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except praw.exceptions.APIException:
            print("### praw failure")
            return None
        except ConnectionError:
            print("### praw failure")
        except HTTPError:
            print("### HTTPError")
            return None
    return wrapped