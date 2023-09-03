import flickrapi

from .configreader import Configreader


class GetOauth:
    def __init__(self, mode: str = "prod"):
        self.mode = mode
        config = Configreader(mode)
        self.flickrauth = config.get_snsauth("flickr")

    def get_flickr_oauth(self):
        API_KEY = self.flickrauth["api_key"]
        API_SECRET = self.flickrauth["secret"]

        flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET)
        authorize_url = flickr.auth_url(perms="write")
        print("Please visit the following URL and authorize the application:")
        print(authorize_url)
        verifier = input("Enter the verification code: ")

        flickr.get_access_token(verifier)
        print("Access Token:", flickr.token_cache.token.access_token)
        print("Access Token Secret:", flickr.token_cache.token.access_token_secret)
