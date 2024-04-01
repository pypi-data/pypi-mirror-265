from typing import Dict

class ProxyResponse:
    username: str = str()
    password: str = str()
    proxy_address: str = str()
    port: int = int()
    
    def __init__(self, result: Dict[str, any]) -> None:
        
        self.username = result.get('username')
        self.password = result.get('password')
        self.proxy_address = result.get('proxy_address')
        self.port = result.get('port')
        self.IpPort = result.get('proxy_address') + ':' + str(result.get('port'))
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(username={self.username}, password={self.password}, proxy_address={self.proxy_address}, port={self.port}, IpPort={self.IpPort})'