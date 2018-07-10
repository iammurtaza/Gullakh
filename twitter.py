import json
import sys
import datetime
import re
import unicodedata

def main():
	#accnt=sys.argv[1]
	#args=sys.argv[2:]
	accnt="twitter"
	args='{"token":"935426607220629504-YMpxqgZv5EViljATeuU3Xwuj875nvrM","tokenSecret":"tw5YPyEXLqduUFFTCn67vH2TyFGj0mH0wUoaAp3iH9oM1","id":"935426607220629504","nickname":"mhzTweets","name":"Murtaza Hasan","email":"murtaza.hasan.zaidi@gmail.com","avatar":"http:\/\/abs.twimg.com\/sticky\/default_profile_images\/default_profile_normal.png","user":{"id_str":"935426607220629504","entities":{"description":{"urls":[]}},"protected":false,"followers_count":5,"friends_count":71,"listed_count":0,"created_at":"Tue Nov 28 08:34:17 +0000 2017","favourites_count":0,"utc_offset":null,"time_zone":null,"geo_enabled":false,"verified":false,"statuses_count":0,"lang":"en","contributors_enabled":false,"is_translator":false,"is_translation_enabled":false,"profile_background_color":"F5F8FA","profile_background_tile":false,"profile_link_color":"1DA1F2","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":true,"has_extended_profile":false,"default_profile":true,"default_profile_image":true,"following":false,"follow_request_sent":false,"notifications":false,"translator_type":"none","suspended":false,"needs_phone_verification":false,"url":null,"profile_background_image_url":null,"profile_background_image_url_https":null,"profile_image_url":"http:\/\/abs.twimg.com\/sticky\/default_profile_images\/default_profile_normal.png","profile_image_url_https":"https:\/\/abs.twimg.com\/sticky\/default_profile_images\/default_profile_normal.png","location":"","description":""},"avatar_original":"http:\/\/abs.twimg.com\/sticky\/default_profile_images\/default_profile.png"}'
	

	
	args=args.replace("\'","")

	testTrue=re.compile(r"true")
	testFalse=re.compile(r"false")
	testlink=re.compile("(\\u003Ca)(.*)()(\\u003E)")


	replacement="html"
	replacementTrue="\"true\""
	replacementFalse="\"false\""

	args=re.sub(testlink,replacement,args)
	args=re.sub(testTrue,replacementTrue,args)
	args=re.sub(testFalse,replacementFalse,args)


	value=json.loads(args,strict=False)
	print("******************************************************************************\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	#print(args)

	if(accnt == "twitter"):print(twitterScore(value))
	#elwse:print("NO")


def twitterScore(value):

	total_score=0

	if(value['user']['statuses_count']):tweets=value['user']['statuses_count']
	else:tweets=0

	if(value['user']['followers_count']):followers=value['user']['followers_count']
	else:followers=0
	
	if(value['user']['friends_count']):following=value['user']['friends_count']
	else:following=0
	
	if(value['user']['favourites_count']):likes=value['user']['favourites_count']
	else:likes=0
	
	score1=tweets+0.5*following+1.2*followers+0.8*likes

	if(score1>250):total_score+=250
	else:total_score+=score1

	#print("%%%%%%",total_score)


	if(value['user']['created_at']):
		year_created=value['user']['created_at'][-4:]
		now=datetime.datetime.now()
		life_time_of_accnt=now.year-int(year_created)
		time_score=dict([(14,30),(13,30),(12,30),(11,30),(10,30),(9,30),(8,30),(7,30),(6,30),(5,30),(4,20),(3,20),(2,10),(1,10),(0,0)])

		total_score+=time_score[life_time_of_accnt]

	else:pass

	#print("&&&&&&&&&",total_score)
	


	if(value['name'] and value['email']):
		first_name=value['name'].split()[0]
		last_name=value['name'].split()[1]
		email=value['email'].lower()
		contains_first=re.compile(first_name.lower())
		contains_last=re.compile(last_name.lower())

		if(contains_first.search(email)):total_score+=2.5
		if(contains_last.search(email)):total_score+=2.5
	else:pass	

	#print("###################",total_score)



	if(value['user']['statuses_count']):
		if(value['user']['status']):
			months={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
			last_tweet_year=int(value['user']['status']['created_at'][-4:])
			last_tweet_month=value['user']['status']['created_at'].split()[1]
			if(now.year-last_tweet_year is 0):
				difference_month=now.month-months[last_tweet_month]
				if(difference_month <= 2):
					total_score+=60
				elif(difference_month<=3 and difference_month>2):
					total_score+=50	
				elif(difference_month<=4 and difference_month>3):
					total_score+=40
				elif(difference_month<=5 and difference_month>4):
					total_score+=30
				else:total_score+=20		
			else:
				total_score+=10
		else:pass			

	else:pass
	#print("###################",total_score)

	if(value['user']['verified']):
		if(value['user']['verified']=='true'):total_score+=50
		else:pass
	else:pass
	#print("###################",total_score)


	if(value['user']['suspended']):
		if(value['user']['suspended']=='false'):total_score+=50
		else:pass
	else:pass
	#print("###################",total_score)

	return(total_score)




if __name__ == '__main__':
	main()




#total score=510



