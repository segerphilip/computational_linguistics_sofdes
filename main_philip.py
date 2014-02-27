from pattern.web import *
from pattern.vector import *
from pattern.en import *

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
	test_license = "CAAEuAis8fUgBAKJgumD8nBusvZBoeNSdKFivZA2mlhv5aP5Cs9FeN1SWJQAq4v0lt8T27t4o0XiQRCq7mMi0h1POJZAacLljF0fdGaTK70rn9tZC7CPTZAZCacGIkOLzPgLBjtbIEKcVNHrAXnhpB425OZAZBzR3UH8WGw9I1FL8AlhNAB4yzTmw"
	test_name = "Philip Seger"	
	fb = Facebook(test_license)

	parse_facebook(fb)

parse_facebook_unit_test()

def sentiment_training(learning_data, fb):
	setiment_data = {}
	for status, reactions in (learning_data.iteritems()):
		sentiment = 0
		for comments in comments:
			sentiment += sentiment(comment)
			sentiment = sentiment / 2

