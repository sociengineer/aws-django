import boto3
import json
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords  

# # Create SQS client
# sqs = boto3.client('sqs')

# queue_url = 'https://sqs.ap-northeast-2.amazonaws.com/687651457542/s3-sqs-standard-que'

# # Receive message from SQS queue
# response = sqs.receive_message(
#     QueueUrl=queue_url,
#     AttributeNames=[
#         'SentTimestamp'
#     ],
#     MaxNumberOfMessages=1,
#     MessageAttributeNames=[
#         'All'
#     ],
#     VisibilityTimeout=0,
#     WaitTimeSeconds=0
# )

# # message = json.loads(response['Messages'][0]['Body'])['Records'][0]['s3']
# bucket_name = json.loads(response['Messages'][0]['Body'])['Records'][0]['s3']['bucket']['name']
# file_name = json.loads(response['Messages'][0]['Body'])['Records'][0]['s3']['object']['key']
# # receipt_handle = message['ReceiptHandle']


# # print(bucket_name, file_name)

# s3 = boto3.client('s3')
# s3.download_file(bucket_name, file_name, file_name)


translate = boto3.client(service_name='translate', 
                        region_name='ap-northeast-2', 
                        use_ssl=True)


comprehend = boto3.client(service_name='comprehend',
                          region_name='ap-northeast-2')


df = pd.read_csv('review_test.csv', encoding='utf-8')
# df = df[:3]
# print(df.iloc[0]['reviews.text'])
review_text_title= ''
wordcloud_texts = ''
# for index, review in df.iterrows():
#     review_text_title = str(review['reviews.text']) + ' ' + str(review['reviews.title'])
#     detected_source_language_code = json.dumps(comprehend.detect_dominant_language(Text = review_text_title).get('Languages')[0].get('LanguageCode'))
#     result = translate.translate_text(Text=review_text_title, 
#             SourceLanguageCode=detected_source_language_code.replace("\"",""), TargetLanguageCode="en")
#     translated_text = result.get('TranslatedText')
#     for key_phrase in comprehend.detect_key_phrases(Text=translated_text, LanguageCode='en').get("KeyPhrases"):
#         # for token in key_phrase.get('Text').split():
#         #     if token in stopwords:
#         wordcloud_texts += key_phrase.get('Text').replace(' ','_') + ' '
                
# wordcloud_texts = wordcloud_texts.lower().replace('the_', '').replace('a_', '')

for index, review in df.iterrows():
    review_text_title = str(review['reviews.text']) + ' ' + str(review['reviews.title'])
    detected_source_language_code = json.dumps(comprehend.detect_dominant_language(Text = review_text_title).get('Languages')[0].get('LanguageCode'))
    result = translate.translate_text(Text=review_text_title, 
            SourceLanguageCode=detected_source_language_code.replace("\"",""), TargetLanguageCode="en")
    translated_text = result.get('TranslatedText')
    for tokens in comprehend.detect_syntax(Text=translated_text, LanguageCode='en').get('SyntaxTokens'):
        if tokens.get('PartOfSpeech').get('Tag') in ['NOUN', 'ADV', 'ADJ']:
            wordcloud_texts += str(tokens.get('Text')) + ' '


# review['reviews.text'].decode('utf-8'))
# text = df.iloc[0]['reviews.text']

# detected_source_language_code = json.dumps(comprehend.detect_dominant_language(Text = text).get('Languages')[0].get('LanguageCode'))
# print(json.dumps(comprehend.detect_dominant_language(Text = text), sort_keys=True, indent=4))
# print("End of DetectDominantLanguage\n")
# print(SourceLanguageCode)



# result = translate.translate_text(Text=text, 
#             SourceLanguageCode=detected_source_language_code.replace("\"",""), TargetLanguageCode="en")
# print(result.get('TranslatedText'))
# translated_text = result.get('TranslatedText')

# print(comprehend.detect_syntax(Text=translated_text, LanguageCode='en').get('SyntaxTokens'))
# for tokens in comprehend.detect_syntax(Text=translated_text, LanguageCode='en').get('SyntaxTokens'):
#     if tokens.get('PartOfSpeech').get('Tag') == 'NOUN':
#         print(tokens.get('Text'), tokens.get('PartOfSpeech').get('Tag'))

# print(json.dumps(comprehend.detect_key_phrases(Text=translated_text, LanguageCode='en'), sort_keys=True, indent=4))
# print(comprehend.detect_key_phrases(Text=translated_text, LanguageCode='en').get("KeyPhrases")[0])

# wordcloud_texts = ''
# for key_phrase in comprehend.detect_key_phrases(Text=translated_text, LanguageCode='en').get("KeyPhrases"):
#     print(key_phrase.get('Text').replace(' ','_'))
#     wordcloud_texts += key_phrase.get('Text').replace(' ','_') + ' '

# print(wordcloud_texts)



word_cloud = WordCloud(collocations = False, background_color = 'white').generate(wordcloud_texts)
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
plt.show()
plt.savefig('wordcloud.png')


# print(json.dumps(comprehend.detect_syntax(Text=translated_text, LanguageCode='en'), sort_keys=True, indent=4).get('SyntaxTokens'))



# print('TranslatedText: ' + result.get('TranslatedText'))
# print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
# print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))


# Delete received message from queue
# sqs.delete_message(
#     QueueUrl=queue_url,
#     ReceiptHandle=receipt_handle
# )
# print('Received and deleted message: %s' % message)
