from typing import List
from http_injector import TypeInjector, HTTPInjector

from .response import ProxyResponse
from .database import Proxys

class Webshare:
    
    def __init__(self, Authorization: str) -> None:
        self.Authorization = Authorization
        self.client = HTTPInjector(typeInjector=TypeInjector.httpx, headers=dict(Authorization = self.Authorization))
        if Proxys.Count() <= 0:
            self.__search__
    
    @property
    def __plan__(self):
        Result  = self.client.get('https://proxy.webshare.io/api/v2/subscription/plan/').json()
        if type(Result) == dict:
            results = Result.get('results')
            if type(results) == list:
                return int(int(results[0].get('proxy_count')) / 100) + 1
        return 10
    
    @property
    def __search__(self):
        Proxys.DeleteAll()
        print('Searching Proxy', end='\r')
        responses: List[ProxyResponse] = list()
        for I in range(1, self.__plan__):
            URL     = f'https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page={I}&page_size=100'
            for results in self.client.get(URL).json().get('results'): 
                responses.append(ProxyResponse(results))
        Proxys.InsertMassal(responses)
    
    def build(self, Search: bool = False):
        while True:
            if Search:
                self.__search__
            rand = Proxys.Random()
            if rand is not None:
                return rand
            else:
                self.__search__