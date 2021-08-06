import json
import requests
import urllib.parse # Py3
import urllib.request # Py

#read the Webhose API key
def read_webhose_key():
    
    #  Get the Webhose API key from the search.key file, return API OR None
    webhose_api_key = None
    try:
        with open ('search.key','r') as f:
            webhose_api_key = f.readline().strip()
    except:
        try:
            with open('../search.key') as f:
                webhose_api_key = f.readline().strip()

        except:
            raise IOError('search.key file not found')
    if not webhose_api_key:
        raise KeyError('search key not found')
    return webhose_api_key
# run query

def run_query(search_terms):
    # """set search terms, store the results returned by the Webhose API in list"""
    webhose_api_key = read_webhose_key()
    if not webhose_api_key:
        raise KeyError('Webhose key not found')
    root_url ='http://webhose.io/search'
    
    query_string = urllib.parse.quote(search_terms)
    search_url = ('{root_url}?token={key}&format=json&q={query}').format(
                    root_url=root_url,
                    key=webhose_api_key,
                    query=query_string)
  
    
    results = []
    try:
        response = urllib.request.urlopen(search_url).read().decode('utf-8')
        json_response = json.loads(response)
        for post in json_response['posts']:
            results.append({'title': post['title'],
                            'link': post['url'],
                            'summary': post['text'][:200]})
    except:
        print("Error when querying the Webhose API")

    return results


def main():
    search_terms = input("Enter your query terms: ")
    results = run_query(search_terms)

    for result in results:
        print(result['title'])
        print(result['link'])
        print(result['summary'])
        print('===============')


# run from here
if __name__ == '__main__':
    main()



