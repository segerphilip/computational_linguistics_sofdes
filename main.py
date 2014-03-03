from pattern.web import *
from pattern.vector import *
from pattern.en import sentiment

def parse_facebook(fb):
	status_dict = {}
	profile = fb.profile(id = None)

	for post in fb.search(profile[0],type = NEWS, count=50):
		status = repr(post.text)
		comments = ()
 
		for comment in fb.search(post.id, type=COMMENTS):
			comments = comments + (comment.text,)

		reactions = (comments,post.likes)
		status_dict.update({status:reactions})

	return status_dict
	for status, reactions in (status_dict.iteritems()):
	
		print status
		print reactions

def parse_facebook_unit_test():
	test_license = "CAAEuAis8fUgBAGZBa7tSoTRZCIEfE7vzDVDTweZBEkufbhUPsnW7v2KuY27OeJDvZBoa4CDg8Bm6ZAsCnlAhFUlw8SUdMcM3yKAXtVqOd0cgpsYkB5MpRH2vP97W5NWkOWvJ8VknnfIpe7HE0vUE7uxJRJG7M1gRrXf5fjuRWLYW0GLyDv2Lg"
	test_name = "Austin Greene"
	fb = Facebook(test_license)

	status_dict = parse_facebook(fb)

	for status, reactions in status_dict.iteritems():
		print status
		print reactions


def sentiment_training(learning_data, fb):
	popularity_data = {}
	profile = fb.profile(id = None)
	friends = len(fb.search(profile[0], type=FRIENDS, count=10000))
	print friends
	for status, reaction in (learning_data.iteritems()):
		feeling = 0.0
		comments = reaction[0]
		for comment in comments:
			feeling += sentiment(comment)[0]
		#Add real popularity metric
		if len(comments) > 0:
			feeling /= len(comments)	
		print reaction [1]
		print len(comments)
		likePercentage = float(reaction[1])/float(friends)*100
		commentPercentage = float(len(comments))/float(friends)*100

		print likePercentage
		print commentPercentage
		#like formula
		likeMetric = 5*likePercentage**2 + .283*likePercentage -.084
		#comment formula
		commentMetric = 5*commentPercentage**2+.283*commentPercentage -.084

		if likeMetric > 1:
			likeMetric = 1

		if commentMetric > 1:
			commentMetric = 1

		feeling = (feeling + likeMetric + commentMetric)/3
		print feeling
		if feeling > .6 :
			popularity = "Yo dog, you will be so popular"
		elif feeling > .1:
			popularity = "good"
		elif feeling > -.09:
			popularity = "fine"
		elif feeling >  -.59:
			popularity = "bad"
		else:
			popularity = "BAD"

		popularity_data.update({status:popularity})

	print popularity_data
	training_data = [Document(status, type= popularity, stopwords=True) for status, popularity in popularity_data.items()]

	nb = NB(train=training_data)

	return nb

def sentiment_training_unit_test():
	test_license = "CAAEuAis8fUgBAGZBa7tSoTRZCIEfE7vzDVDTweZBEkufbhUPsnW7v2KuY27OeJDvZBoa4CDg8Bm6ZAsCnlAhFUlw8SUdMcM3yKAXtVqOd0cgpsYkB5MpRH2vP97W5NWkOWvJ8VknnfIpe7HE0vUE7uxJRJG7M1gRrXf5fjuRWLYW0GLyDv2Lg"
	test_name = "Austin Funkhouser"
	fb = Facebook(test_license)

	data = parse_facebook(fb)

	classifier = sentiment_training(data,fb)

	print classifier.classes
	print classifier.classify("I heart Joe Biden #yolo")

sentiment_training_unit_test()