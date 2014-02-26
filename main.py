from pattern.web import *
from pattern.vector import *

def parse_facebook(facebook_id = None):
	status_dict = {}
	fb = Facebook(license = "CAAEuAis8fUgBAGZBa7tSoTRZCIEfE7vzDVDTweZBEkufbhUPsnW7v2KuY27OeJDvZBoa4CDg8Bm6ZAsCnlAhFUlw8SUdMcM3yKAXtVqOd0cgpsYkB5MpRH2vP97W5NWkOWvJ8VknnfIpe7HE0vUE7uxJRJG7M1gRrXf5fjuRWLYW0GLyDv2Lg" )
	profile = fb.profile(id = None)

	for post in fb.search(profile[0],type = NEWS, count=10):
		status = repr(post.text)
		comments = ()

		for comment in fb.search(post.id, type=COMMENTS):
			comments = comments + (comment.text,)

		status_dict.update({status:comments})

	for status, comments in (sorted(status_dict.iteritems())):
	
		print status
		print comments

def parse_facebook_unit_test():
	test_id = "CAAEuAis8fUgBAGZBa7tSoTRZCIEfE7vzDVDTweZBEkufbhUPsnW7v2KuY27OeJDvZBoa4CDg8Bm6ZAsCnlAhFUlw8SUdMcM3yKAXtVqOd0cgpsYkB5MpRH2vP97W5NWkOWvJ8VknnfIpe7HE0vUE7uxJRJG7M1gRrXf5fjuRWLYW0GLyDv2Lg"
	test_name = "Austin Greene"

	facebook_id = (test_id,test_name)

	parse_facebook(facebook_id)

parse_facebook_unit_test()
