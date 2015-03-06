__author__ = 'Ramki Subramanian'

import re
import json

class messageDecode(object):


    def __int__(self,input_str):
        pass

    def decode(input_str):
        main={}
        #string = "Oncdadad@e httpe:SAASd (have) @Ramki asdasdasda @RajeshSubra8 98 sadasdasdsdadadas #(swaasd79des) accomplished small (adadasd) things, you may(123456 Mike Jack) attempt great ones."
        string = "(Happy)Did you @notic adadadfase!!! the tinyurls?? @Ramki!! adsas daasd(happy) @Rajeshh SD asdassdasdsa..They are awesome. http://tinyurl.com/mz4k345d @Ramki adadasdasd"
        emoticons = re.findall(r"(\([\w\s]{1,15}\).*?)", string)   # \s for whitespace ( to handle multiword names like Michael Jackson , \w for alphanumeric ( to handle usernames like mike999)
        emoticons = [em.strip('()')for em in emoticons]
        main['emoticons'] = emoticons
        print emoticons

        # Previous method
        # e = re.findall(r"(\B(?:\@)[\w\S]*.*?)", string) # \B to catch the @ in the start of the word \S- to handle only singleword values
        # \B to catch the @ in the start of the word
        # \S- to handle only singleword values

        mentions = re.findall(r"((?:\@)[\w.]+)", string)
        mentions = [i.strip('@') for i in mentions]
        main['mentions'] = mentions
        print mentions

        #URL
        url = re.findall(r"(http[^\s]+).*?",string)
        print url


        print json.dumps(main,sort_keys=True,indent=4)






if __name__ == '__main__':
    newObj = messageDecode()
    input_str="(sic)(spoiley)http://www.bing.com/permanent/?request=get-archive&isbn=0342-8244,@Ramki!!(Boo Yeah)(Happy)"
    newObj.decode(input_str)

