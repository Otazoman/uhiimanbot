import flickrapi

API_KEY = "" 
API_SECRET = ""  

flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET)
flickr.get_request_token(oauth_callback='oob')

authorize_url = flickr.auth_url(perms='write')
print('Please visit the following URL and authorize the application:')
print(authorize_url)
verifier = input('Enter the verification code: ')

flickr.get_access_token(verifier)
print('Authentication successful')


