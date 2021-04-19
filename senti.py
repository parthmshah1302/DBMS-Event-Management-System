from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

def Sentiment(text):
    apikey='VzPPAGsigGV1Cb-Vp6S2Wu7kIj_B8ujevtnnGMK2bjMs'
    url='https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/05ffd3d4-ad08-4486-bc23-13bcaae327ff'

    authenticator = IAMAuthenticator(apikey)
    tone_analyzer = ToneAnalyzerV3(version='2017-09-21',authenticator=authenticator)
    tone_analyzer.set_service_url(url)

    result=tone_analyzer.tone(
        {'text':text},
        content_type='application/json'
    ).get_result()
    json_r=json.dumps(result, indent=2)
    a=json.loads(json_r)
    return(a['document_tone']['tones'][0]['tone_id'])

print(Sentiment('this is a good comment'))