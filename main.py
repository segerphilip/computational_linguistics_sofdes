"""
Devs: Austin Greene
Sub-Dev/comments for days: Philip Seger
Date: 2/26/14

This program takes a users Facebook key and a possible new post.
From there, it finds the success rate from previous posts, depending on:
	# of likes
	# of comments
Then, it gives the user an estimate of how well the post will do.
"""
#also, we used all the patter :)
from pattern.web import *
from pattern.vector import *
from pattern.en import sentiment

#this whole function is used to find data from fb and then store it for later use
def parse_facebook(fb):
	#dictionary for statuses, will include comments and likes
	status_dict = {}
	profile = fb.profile(id = None)
	#go through a user's news feed for a certain amount
	for post in fb.search(profile[0],type = NEWS, count=100):
		status = repr(post.text)
		comments = ()
 		#add comments to the comments string
		for comment in fb.search(post.id, type=COMMENTS):
			comments = comments + (comment.text,)
		#include data from both comments and number of likes
		reactions = (comments,post.likes)
		status_dict.update({status:reactions})
	#this data is used by other functions
	return status_dict
	#this is just for testing
	for status, reactions in (status_dict.iteritems()):
	
		print status
		print reactions

#super fun handy unit test, using Austin as the guinea pig
def parse_facebook_unit_test():
	test_license = "CAAEuAis8fUgBAGZBa7tSoTRZCIEfE7vzDVDTweZBEkufbhUPsnW7v2KuY27OeJDvZBoa4CDg8Bm6ZAsCnlAhFUlw8SUdMcM3yKAXtVqOd0cgpsYkB5MpRH2vP97W5NWkOWvJ8VknnfIpe7HE0vUE7uxJRJG7M1gRrXf5fjuRWLYW0GLyDv2Lg"
	test_name = "Austin Greene"
	fb = Facebook(test_license)
	#get the proper fb data
	status_dict = parse_facebook(fb)
	#check the data for accuracy
	for status, reactions in status_dict.iteritems():
		print status
		print reactions

#main function that analyzes with machine learning from pattern
def sentiment_training(learning_data, fb):
	popularity_data = {}
	profile = fb.profile(id = None)
	#store friends as a metric, used to calculate percentage of likes/comments
	friends = len(fb.search(profile[0], type=FRIENDS, count=10000))
	for status, reaction in (learning_data.iteritems()):
		feeling = 0.0
		#comments are stored in the first area for reaction, unpack it
		comments = reaction[0]
		for comment in comments:
			feeling += sentiment(comment)[0]
		#Add real popularity metric
		if len(comments) > 0:
			feeling /= len(comments)
		#number of likes compared to number of friends and then same with comments
		likePercentage = float(reaction[1])/float(friends)*100
		commentPercentage = float(len(comments))/float(friends)*100

		#like formula to have a more smooth approach, rather than abrupt
		likeMetric = -.025*likePercentage**2 + .374*likePercentage -.227
		#comment formula similar to likeMetric
		commentMetric =-.54*commentPercentage**2+1.639*commentPercentage -.33

		#using a scale from -1 to 1, so make sure it is in the bounds
		if likeMetric > 1:
			likeMetric = 1

		if commentMetric > 1:
			commentMetric = 1

		#take average of the likes, comments, and sentiment
		feeling = (feeling + likeMetric + commentMetric)/3
		#bounds used to decide whether a post was successful or not
		if feeling > .6 :
			popularity = "very popular"
		elif feeling > .1:
			popularity = "popular"
		elif feeling > -.09:
			popularity = "meh"
		elif feeling >  -.59:
			popularity = "not popular"
		else:
			popularity = "bad"

		popularity_data.update({status:popularity})
	#format the data nicely for the machine learning portion
	training_data = [Document(status, type= popularity, stopwords=True) for status, popularity in popularity_data.items()]
	#we used the slp module from pattern as it resulted in more accurate results for bad/good comparisons
	slp = SLP(train=training_data)

	return slp

#more unit testing woo!
def sentiment_training_unit_test():
	test_license = "CAAEuAis8fUgBAGZBa7tSoTRZCIEfE7vzDVDTweZBEkufbhUPsnW7v2KuY27OeJDvZBoa4CDg8Bm6ZAsCnlAhFUlw8SUdMcM3yKAXtVqOd0cgpsYkB5MpRH2vP97W5NWkOWvJ8VknnfIpe7HE0vUE7uxJRJG7M1gRrXf5fjuRWLYW0GLyDv2Lg"
	#austin funkhouser, woah. That's strange :)
	test_name = "Austin Funkhouser"
	fb = Facebook(test_license)
	#get all the fb data
	data = parse_facebook(fb)
	#figure out the previous posts
	classifier = sentiment_training(data,fb)
	#test with a new post, whether it is good or bad
	print classifier.classes
	print classifier.classify("I'm so excited for the next party")

#main program for use, run it by doing "pythong main.py" in terminal
if __name__ == '__main__':
	#get the license from keyboard input, probably want to crtl-v :)
	license = raw_input("What is your Facebook license key?: ")
	# Philip : CAAEuAis8fUgBAL68FHHC3QZAxBlrUPLc8PKqP8qvbedGbLFtgA4w3E8EZBxFRvDifZARY0rv1lxCDipwwT7b21X0j9M4aM3tsmxyYogJ53PevOBvZCvQa4ZBOmZCFxpZC4RSFbl8yN0flqZBUJXO2qczm3gOZBwCZCc4bzXHFiZBejNcAnsgkSiStWL
	# Austin : CAAEuAis8fUgBAGZBa7tSoTRZCIEfE7vzDVDTweZBEkufbhUPsnW7v2KuY27OeJDvZBoa4CDg8Bm6ZAsCnlAhFUlw8SUdMcM3yKAXtVqOd0cgpsYkB5MpRH2vP97W5NWkOWvJ8VknnfIpe7HE0vUE7uxJRJG7M1gRrXf5fjuRWLYW0GLyDv2Lg
	#input a possible post to be evaluated
	status = raw_input("What is your next status: ")
	# I hate everyone ==> Not popular
	# I love everyone ==> Very popular

	fb = Facebook(license)
	#get fb data
	data = parse_facebook(fb)
	#get previous comment sentiment and use machine learning
	classifier = sentiment_training(data,fb)

	classification=classifier.classify(status)

	#print classification
	#this is for if the post is really bad, then even with great previous history it will still do poorly
	if sentiment(status)[0] <-.5 and classification is ("popular" or "very popular"):
		classification = "not popular"
	elif sentiment(status)[0] <-.5 and classification is ("meh" or "not popular"):
		classification = "bad"
	#print the final result
	print "This post will be " + classification