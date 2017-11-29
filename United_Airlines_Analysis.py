
def tokenize_tweet(text):
    """
    This function returns a list of lowercase words in the input string which contain more than 1 letters
    Input: A string
    Returns: List of words

    """
    words = re.split('\W+', text.lower())   #Split using regex
    words_gt_two = [word for word in words if len(word) > 1]    #Consider words with more than 1 character
    #print(words_gt_two)
    return words_gt_two


def filter_by_emotion(words,emotion):
    """
    Filters a list of the words to get only those words that contain a specific emotion
    Input: A list of words and a word which is an emotion in EMOTIONS
    Return Value: A list of words
    """
    default=-1
    #Use list comprehension if a word has any emotion in SENTIMENTS
    filtered_by_emotion = [word for word in words if SENTIMENTS.get(word,default) != -1 if SENTIMENTS.get(word,default).get(emotion,default) == 1 ]
    return(filtered_by_emotion)
    

def emotion_words(words):
    """
    Determines which words from a list have each emotion from a given list of EMOTIONS
    Input: A list of words
    Return Value: A dictionary in which emotions are keys and values are correponding words
    """
    emo_words_dict = {}
    for emotion in EMOTIONS:
        words_for_emotion = filter_by_emotion(words,emotion)    #Call filter_by_emotion() function for each emotion
        emo_words_dict[emotion] = words_for_emotion             #Create a dictionary for each emotion and words

    return(emo_words_dict)

def get_common_words(words):
    """
    Returns a list of the "most common" words in a list: each individual word in the input list ordered by how many times it appears in that list
    Input: A list of words
    Return Value: A list of unique most common words
    """
    words_lower = [word.lower() for word in words]      #Lowercase all words
    words_occr_dict = {word: 0 for word in words_lower} #Initialize a dictionary

    #Count  number of each word
    for word in words_lower:
        words_occr_dict[word]+=1

    #Sort the dictionary based on value in descending order and build a corresponding tuple
    words_occr_sorted_list = sorted(words_occr_dict.items(), key=lambda n: n[1], reverse=True)

    for i in range(len(words_occr_sorted_list)):
        words_occr_sorted_list[i] = words_occr_sorted_list[i][0]    #Build a list
        
    return(words_occr_sorted_list)



def analysze_tweets(tweetlist):
    """
    For each of the 10 emotions in EMOTION, this function calculates following things:
        1. The percentage of words across all tweets that have that emotion
        2. The most common words across all tweets that have that emotion (in order!)
        3. The most common hashtags across all tweets associated with that emotion by calling hashtags_for_emotion() function
    
    Input: A list of tweet data
    Return values: Sum of all words in tweet texts as a number, dictionary of emotions and corresponding word counts sorted in descending order,
                   dictionary of emotions and corresponding hashtags as values  
    """
    sum_all=0
    sum_emotion=0
    hashtags_list = []
    
    emotion_wordcount_dict = dict(zip(EMOTIONS,[0]*10))         #Create a dictionary for each emotion
    
    for i in range(len(tweetlist)):
        tweet_word_list = []
        emotion_words_dict = {}

        tweettext = tweetlist[i]['text']                        #Get text of i'th tweet
        tweet_word_list =  tokenize_tweet(tweettext)            #Get words in that tweet
        tweetlist[i]['words'] = tweet_word_list                 #Insert new key in each dictionary for words in that tweet
        emotion_words_dict = emotion_words(tweet_word_list)     #Find emotional words in that tweet
        tweetlist[i]['emotional_words'] = emotion_words_dict    #Insert new key in each dictionary for emotional words in that tweet
        
    #Count total words and words of each emotion
    for tweetdata in tweetlist:
        sum_all += reduce(lambda x,y: x+1, tweetdata['words'], 0)
        emotion_wordcount_dict['positive'] += reduce(lambda x,y: x+1, tweetdata['emotional_words']['positive'], 0)
        emotion_wordcount_dict['negative'] += reduce(lambda x,y: x+1, tweetdata['emotional_words']['negative'], 0)
        emotion_wordcount_dict['anger'] += reduce(lambda x,y: x+1, tweetdata['emotional_words']['anger'], 0)
        emotion_wordcount_dict['anticipation'] += reduce(lambda x,y: x+1, tweetdata['emotional_words']['anticipation'], 0)
        emotion_wordcount_dict['disgust'] += reduce(lambda x,y: x+1, tweetdata['emotional_words']['disgust'], 0)
        emotion_wordcount_dict['fear'] += reduce(lambda x,y: x+1, tweetdata['emotional_words']['fear'], 0)
        emotion_wordcount_dict['joy'] += reduce(lambda x,y: x+1, tweetdata['emotional_words']['joy'], 0)
        emotion_wordcount_dict['sadness'] += reduce(lambda x,y: x+1, tweetdata['emotional_words']['sadness'], 0)
        emotion_wordcount_dict['surprise'] += reduce(lambda x,y: x+1, tweetdata['emotional_words']['surprise'], 0)
        emotion_wordcount_dict['trust'] += reduce(lambda x,y: x+1, tweetdata['emotional_words']['trust'], 0)

    #Sort the dictionary of count of words for each emotion    
    #emotion_wordcount_dict_sorted = sorted(emotion_wordcount_dict.items(), key=lambda x: x[1], reverse = True)
    
    #Call hashtags_for_emotion() function to get hashtags for each emotion in a dictionary
    #emotion_hashtag_dict = hashtags_for_emotion(tweetlist)
    
    #return(sum_all,emotion_wordcount_dict_sorted,emotion_hashtag_dict)
    return(sum_all,emotion_wordcount_dict)      
    
    
def hashtags_for_emotion(tweetdata):
    """
    Takes a list of tweet data and finds hashtags for each emotion
    Input: A list of tweet data
    Return value: A dictionary of emotions and corresponding hashtags as values
    """
    zero_list = [[] for i in range(1,11)]
    emotion_hashtag_dict = dict(zip(EMOTIONS,zero_list))
    for tweet in tweetdata:
        tweetwords = tokenize_tweet(tweet['text'])          #Get words in tweet text
        for emotion in EMOTIONS:
            if filter_by_emotion(tweetwords,emotion):       #Check if list of emotional words is empty of not, gives FALSE if list is empty
                if tweet['entities']['hashtags']:           #Check if list of hashtags in tweet data is empty of not, gives FALSE if list is empty
                    for i in range(len(tweet['entities']['hashtags'])):
                        hashtag = tweet['entities']['hashtags'][i]['text']      #Get each hashtag
                        emotion_hashtag_dict[emotion].append(hashtag)           #Append to the list of each emotion key in dictionary
    return(emotion_hashtag_dict)


def display_stats(tweetdata,sum_all,emotion_wordcount_dict_sorted):
    """
    Prints each emotion and correponding stats: percentage of words, example words and hashtags
    Input: A list of tweet data, Sum of all words in text of all tweets, dictionary of emotions and corresponding 
           word counts sorted in descending order, dictionary of emotions and corresponding hashtags as values
    Return value: None
    """
    each_tweet_text_list = [tweetdata[i]['text'] for i in range(len(tweetdata))]    
    tweet_text = tokenize_tweet(reduce(lambda x,y: x+y,each_tweet_text_list))
    print('\nTotal number of words in '+str(len(tweetdata))+ ' tweets was '+ str(sum_all)+'\n')

    print("Average polarity for "+whichdate+"th April 2017 is "+str(round(polarity_calc(tweetdata),4))+"\n\n")


    #Print headers
    print("{0:<15s}  {1:<5s}  {2:<30s}   ".format('EMOTION','% of WORDS','TOP 10 WORDS'))

    #Print dotted lines beneath each header for better visibility
    print("{0:<15s}  {1:<5s}  {2:<30s}   ".format('----------','----------','---------------------------------------------------'))
    for emotion in emotion_wordcount_dict_sorted:
        percentage = (emotion[1]/sum_all)*100
        common_words = ','.join(get_common_words(filter_by_emotion(tweet_text,emotion[0]))[:10])     #Get top 3 words
        #common_hashtags_words_list = get_common_words(emotion_hashtag_dict[emotion[0]])[:3]         #Get top 3 hashtags
        #common_hashtags = ','.join(['#'+tag for tag in common_hashtags_words_list])                 #Append # sign
        #print("{0:<15s} {1:5.2f}%       {2:<30s}   {3:30s}".format(emotion[0],percentage,common_words,common_hashtags))     #Print values
        print("{0:<15s} {1:5.2f}%       {2:<30s}   ".format(emotion[0],percentage,common_words))


def download_twitter_data(screen_name,count=200):
  """
  Gets live data from twitter for a particular twitter screen name and number of tweets specified
  Input: A screen name and count of tweets(defaults to 200)
  Return value: twitter data in json format
  """
  parameters={'screen_name':screen_name,'count':count}      #Set parameters
  myreq = requests.get(url='https://faculty.washington.edu/joelross/proxy/twitter/timeline/',params=parameters)     #Get data
  tweet_data = json.loads(myreq.text)   #Load json file
  return tweet_data


def polarity_calc(tweetdata):
    from textblob import TextBlob
    tweettext = ''
    polarity = []
    import numpy as np
    for tweet in tweetdata:
        tweettext = tweettext + tweet['text']

    blob = TextBlob(tweettext)
    for sentence in blob.sentences:
        polarity.append(sentence.sentiment.polarity)

    return(np.sum(polarity))

if __name__ == "__main__":
    

    from data.sentiments_nrc import SENTIMENTS
    from data.sentiments_nrc import EMOTIONS
    from functools import reduce
    import re
    import json
    import requests
    from bokeh.resources import CDN
    from bokeh.embed import file_html

    final_list = []

    mode = input("\n\nPlease enter mode as follows:\n\n Enter '1' for a line graph of positive and negative sentiments from 8th April to 28th April 2017.\n Enter '2' for datewise sentiment percentage and top words.\n Enter '3' for sentiment percentage and top words for tweets downloaded from Twitter's Streaming API.\n\n Your choice: ")
    
    if mode == '1':

        for i in range(8,29):
            filename = 'data/tweets_UA_'+str(i)+'Apr_10k.json'
            json_data=open(filename).read()
            data_UA = json.loads(json_data)
        

        
            sum_all,emotion_wordcount_dict = analysze_tweets(data_UA)          #Call function

            positive_sum = emotion_wordcount_dict['positive'] + emotion_wordcount_dict['anticipation'] + emotion_wordcount_dict['trust'] + emotion_wordcount_dict['surprise']+ emotion_wordcount_dict['joy']

            negative_sum = emotion_wordcount_dict['negative'] + emotion_wordcount_dict['fear'] + emotion_wordcount_dict['anger'] + emotion_wordcount_dict['sadness']+ emotion_wordcount_dict['disgust']


            temp_dict = {}
            day = str(i) if len(str(i)) > 1 else '0'+str(i)
            temp_dict['date'] = '2017-04-'+day
            temp_dict['total_sum'] = sum_all
            #temp_dict['positive_sum'] = positive_sum
            #temp_dict['negative_sum'] = negative_sum
            #temp_dict['positive_%'] = round(positive_sum*100/(positive_sum+negative_sum), 4)
            #temp_dict['negative_%'] = round(negative_sum*100/(positive_sum+negative_sum), 4)
            temp_dict['positive_%'] = round(positive_sum*100/(sum_all), 4)
            temp_dict['negative_%'] = round(negative_sum*100/(sum_all), 4)
            temp_dict['avg_polarity'] = round(polarity_calc(data_UA),4)
            final_list.append(temp_dict)
            
        print(final_list)
        #Begin plotting Bokeh plot
        from datetime import datetime
        eachdate = []
        positive_perc = []
        negative_perc = []
        avg_polarity = []
        for eachday in final_list:
            eachdate.append(datetime.strptime(eachday['date'], '%Y-%m-%d').date().day)
            positive_perc.append(eachday['positive_%']/100)
            negative_perc.append(eachday['negative_%']/100)
            avg_polarity.append(eachday['avg_polarity'])
            
        #print(eachdate)
        #print(positive_perc)
        #print(negative_perc)
        from bokeh.plotting import figure, output_file, show
        from bokeh.models import HoverTool,NumeralTickFormatter,PrintfTickFormatter
        output_file("UA_posneg_senti.html")
        p = figure(title="Sentiment over time", x_axis_label='Date', y_axis_label='Sentiment Percentage (%)')
        p.background_fill_color = "#f2f1ef"
        p.background_fill_alpha = 0.5

        p.line(x=eachdate, y=positive_perc, line_width=2, line_color="#6fef47",legend="Positive Sentiment")
        p.line(x=eachdate, y=negative_perc, line_width=2, line_color="#ed071e",legend="Negative Sentiment")


        #p.xaxis.minor_tick_line_color = None
        p.yaxis[0].formatter = NumeralTickFormatter(format="0%")
        #p.yaxis[0].formatter = PrintfTickFormatter(format="%2i %")
        p.legend.location = "top_right"
        p.legend.border_line_width = 1
        p.legend.border_line_color = "black"
        p.legend.border_line_alpha = 0.3
        TOOLS = 'box_zoom,box_select,crosshair,resize,reset,hover'



        pos_hov = p.circle(eachdate, positive_perc, size=20,
                        fill_color="grey", hover_fill_color="#6fef47",
                        fill_alpha=0.05, hover_alpha=0.3,
                        line_color=None, hover_line_color="white")



        neg_hov = p.circle(eachdate, negative_perc, size=20,
                        fill_color="grey", hover_fill_color="#ed071e",
                        fill_alpha=0.05, hover_alpha=0.3,
                        line_color=None, hover_line_color="white")


        p.add_tools(HoverTool(tooltips=None, renderers=[pos_hov,neg_hov], mode='vline'))
        html = file_html(p, CDN, "senti")
        Html_file= open("html_senti","w")
        Html_file.write(html)
        Html_file.close()
        
        show(p)


        output_file("UA_polarity.html")
        p1 = figure(title="Polarity over time", x_axis_label='Date', y_axis_label='Polarity')
        
        p1.background_fill_color = "#f2f1ef"
        p1.background_fill_alpha = 0.5
        p1.line(x=eachdate, y=avg_polarity, line_width=2, line_color="blue",legend="Polarity")
        hov = p1.circle(eachdate, avg_polarity, size=20,
                        fill_color="grey", hover_fill_color="blue",
                        fill_alpha=0.05, hover_alpha=0.3,
                        line_color=None, hover_line_color="white")
        p1.add_tools(HoverTool(tooltips=None, renderers=[hov], mode='hline'))
        show(p1)

    ####################################################################################################################
    #For mode 2, get a date from user between 8th April and 28th April and display sentiment percentage and top 10 words
    if mode == '2':
        whichdate = input("\n\n Enter the date for which you want sentiment percentages and top 10 words. For example, enter '12' for 12th April 2017.\n\n Your Choice: ")
        filename = 'data/tweets_UA_'+str(whichdate)+'Apr_10k.json'
        json_data_whichdate=open(filename).read()
        data_whichdate = json.loads(json_data_whichdate)

        sum_all,emotion_wordcount_dict = analysze_tweets(data_whichdate)
        emotion_wordcount_dict_sorted = sorted(emotion_wordcount_dict.items(), key=lambda x: x[1], reverse = True)
        
        display_stats(data_whichdate,sum_all,emotion_wordcount_dict_sorted)

    if mode == '3':
        filename = 'data/tweets_UA_Current_29May_10k.json'
        json_data_live=open(filename).read()
        data_live = json.loads(json_data_live)

        sum_all,emotion_wordcount_dict = analysze_tweets(data_live)
        emotion_wordcount_dict_sorted = sorted(emotion_wordcount_dict.items(), key=lambda x: x[1], reverse = True)
        display_stats(data_live,sum_all,emotion_wordcount_dict_sorted)
