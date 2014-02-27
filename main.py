from pattern.web import *
from pattern.vector import *
from pattern.en import sentiment

def parse_facebook(fb):
	status_dict = {}
	profile = fb.profile(id = None)

	for post in fb.search(profile[0],type = NEWS, count=10):
		status = repr(post.text)
		comments = ()

		for comment in fb.search(post.id, type=COMMENTS):
			comments = comments + (comment.text,)

		reactions = (comments,post.likes)
		status_dict.update({status:reactions})

	for status, reactions in (status_dict.iteritems()):
	
		print status
		print reactions

def parse_facebook_unit_test():
	test_license = "CAAEuAis8fUgBAGZBa7tSoTRZCIEfE7vzDVDTweZBEkufbhUPsnW7v2KuY27OeJDvZBoa4CDg8Bm6ZAsCnlAhFUlw8SUdMcM3yKAXtVqOd0cgpsYkB5MpRH2vP97W5NWkOWvJ8VknnfIpe7HE0vUE7uxJRJG7M1gRrXf5fjuRWLYW0GLyDv2Lg"
	test_name = "Austin Greene"
	fb = Facebook(test_license)

	parse_facebook(fb)

parse_facebook_unit_test()

def sentiment_training(learing_data, fb):
	sentiment_data = {}
	profile = fb.profile(id = None)

	for status, reactions in (learning_data.iteritems()):
		sentiment = 0
		for comment in comments:
			sentiment += sentiment(comment)
			sentiment =  sentiment/2
		sentiment_data.update({status:sentiment})