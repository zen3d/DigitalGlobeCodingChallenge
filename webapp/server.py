"""
Digital Globe interview challenge solution

    * Create a URL shortening service
    * Put it behind a cherrypy Rest API in a meaningful way
    * The service must be built as a Docker image
    * Put the code in Github in a way that makes sense: Readme file, etc
    * Make it pretty as if someone's going to use it
    * Deploy to a cloud provider of your choice
    * Rate limit the service to 2 requests per second
    * Bonus: for any kind of GUI

"""
from time import time
import cherrypy


_url_form = """
<!DOCTYPE html>
<html>
    <body>
	<form action="new_url" method="post">
          URL:<br>
          <input type="text" name="url" value="">
          <br>
          <input type="submit" value="Submit">
        </form>
    </body>
</html>
"""

_url_report = """
<!DOCTYPE html>
<html>
    <body>
	To access the URL:
        <br>
	%s
	<br>
	use the key:
        <br>
	%s
    </body>
</html>
"""

_invalid_key = """
<!DOCTYPE html>
<html>
    <body>
	Invalid key was specified:
        <br>
	%s
    </body>
</html>
"""

_unknown_key = """
<!DOCTYPE html>
<html>
    <body>
        An unknown key was specified: 
        <br>
        %s
    </body>
</html>
"""

keys_dict = {}

time_last = time()

def rate_limit():
    time_next = time()
    if (time_next - time_last < 0.5):
        raise cherrypy.HTTPError(403) # raise a Forbidden Error
    time_last = time_next
    
def hash_str(str):
    """Create a 6 character string that acts as a URL hash key"""
    hash_value = hash(str)
    hash_str = ""
    for idx in range(0, 6):
        hash_mod = hash_value % 64
        hash_value = hash_value / 64
        if (0 <= hash_mod) and (hash_mod < 26):
            hash_str += chr(ord('A') + hash_mod)
        elif (26 <= hash_mod) and (hash_mod < 52):
            hash_str += chr(ord('a') + hash_mod - 26)
        else:
            hash_str += chr(ord('0') + hash_mod - 52)
    return hash_str

class Root(object):
    def __init__(self):
        self.keys_dict = {}
        self.time_last = time()

    def rate_limit(self):
        """Limit the rate at which the server responds"""
        time_next = time()
        if time_next - self.time_last < 0.5:
            raise cherrypy.HTTPError(403) # raise a Forbidden Error
        self.time_last = time_next

    def index(self):
        """Handler for base URL"""
        self.rate_limit();
        return _url_form
    index.exposed = True

    def new_url(self, url = None):
        """Handler to indicate hash key for a URL"""
        if url == None:
            return _url_form
        else:
            self.rate_limit()
            url_hash = hash_str(hash(url))
            self.keys_dict[url_hash] = url
            return (_url_report % (url, url_hash))
    new_url.exposed = True

    def default(self, *args, **kwargs):
        """Handler to respond to hash keys"""
        self.rate_limit()
        if len(args) > 1:
            return (_invalid_key % ('/'.join(args)))
        elif args[0] in self.keys_dict:
            print(self.keys_dict[args[0]])
            raise cherrypy.HTTPRedirect("http://%s" % (self.keys_dict[args[0]]))
        else:
            return (_unknown_key % args[0])
        print(len(args))
        return "in default"
    default.exposed = True

root = Root()

cherrypy.config.update({'server.socket_host': '0.0.0.0'})

cherrypy.tree.mount(root)
