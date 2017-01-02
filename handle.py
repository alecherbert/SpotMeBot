import praw
from requests.exceptions import ConnectionError, HTTPError, Timeout

def handle(f):
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except praw.errors.APIException:
            print("### praw failure")
            return None
        except ConnectionError:
            print("### ConnectionError")
        except (Timeout, socket.timeout, socket.error):
            print("### timeout")
            return None
        except HTTPError:
            print("### HTTPError")
            return None
    return wrapped