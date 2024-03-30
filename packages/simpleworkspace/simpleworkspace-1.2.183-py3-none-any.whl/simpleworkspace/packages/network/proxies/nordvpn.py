import requests
from functools import cached_property


class _ProxyServerDTO:
    def __init__(self, hostname:str, port:int, protocol:str) -> None:
        self.hostname = hostname
        self.port = port
        self.protocol = protocol

class NordVPNProxy():
    #https://api.nordvpn.com/v1/servers?limit=100000
    #https://api.nordvpn.com/v1/servers/recommendations?limit=10&offset=0


    class Proxies_SOCKS5():
        """SOCKS5 supports alot of protocols but not recommended for simple requests since it transmits data unencrypted to the proxy server which contains auth token"""
        IE = _ProxyServerDTO("ie.socks.nordhold.net", 1080, "socks5") 
        IE_DUBLIN = _ProxyServerDTO("dublin.ie.socks.nordhold.net", 1080, "socks5") 
        NL = _ProxyServerDTO("nl.socks.nordhold.net", 1080, "socks5") 
        NL_AMSTERDAM = _ProxyServerDTO("amsterdam.nl.socks.nordhold.net", 1080, "socks5") 
        SE = _ProxyServerDTO("se.socks.nordhold.net", 1080, "socks5") 
        SE_STOCKHOLM = _ProxyServerDTO("stockholm.se.socks.nordhold.net", 1080, "socks5") 
        US = _ProxyServerDTO("us.socks.nordhold.net", 1080, "socks5") 
        US_ATLANTA = _ProxyServerDTO("atlanta.us.socks.nordhold.net", 1080, "socks5") 
        US_DALLAS = _ProxyServerDTO("dallas.us.socks.nordhold.net", 1080, "socks5") 
        US_LOSANGELES = _ProxyServerDTO("los-angeles.us.socks.nordhold.net", 1080, "socks5")
    
    class Proxies_HTTPS():
        SE_1 = _ProxyServerDTO("se530.nordvpn.com", 89, "https")
        SE_2 = _ProxyServerDTO("se560.nordvpn.com", 89, "https")
        SE_3 = _ProxyServerDTO("se534.nordvpn.com", 89, "https")
        SE_4 = _ProxyServerDTO("se563.nordvpn.com", 89, "https")
        SE_5 = _ProxyServerDTO("se546.nordvpn.com", 89, "https")
        NL_1 = _ProxyServerDTO("nl897.nordvpn.com", 89, "https")
        NL_2 = _ProxyServerDTO("nl880.nordvpn.com", 89, "https")
        NL_3 = _ProxyServerDTO("nl996.nordvpn.com", 89, "https")
        NL_4 = _ProxyServerDTO("nl914.nordvpn.com", 89, "https")
        NL_5 = _ProxyServerDTO("nl866.nordvpn.com", 89, "https")
        US_1 = _ProxyServerDTO("us6784.nordvpn.com", 89, "https")
        US_2 = _ProxyServerDTO("us9338.nordvpn.com", 89, "https")
        US_3 = _ProxyServerDTO("us9340.nordvpn.com", 89, "https")
        US_4 = _ProxyServerDTO("us8371.nordvpn.com", 89, "https")
        US_5 = _ProxyServerDTO("us5835.nordvpn.com", 89, "https")

    
    @cached_property
    def _CountriesLookup(self):
        listOfCountries = requests.get("https://api.nordvpn.com/v1/servers/countries").json()

        lookup = {}
        for country in listOfCountries:
            lookup[country['name'].upper()] = country['id']
            lookup[country['code'].upper()] = country['id']

        return lookup

    def GetServers_Recommendations_HTTPS(self, limit=1, offset=0, country:str=None):
        '''
        gets recommended HTTPS proxy servers from online api (proxy_ssl = HTTPS proxy)

        :param country: filters recommendation based on country by name or code eg "Sweden" or "SE" (case insensitive)
        '''
        params = {
            "limit":limit,
            "offset": offset,
            "filters[servers_technologies][identifier]": 'proxy_ssl'
        }
        if(country is not None):
            country = country.upper()
            if(country not in self._CountriesLookup):
                raise NameError(f"Country '{country}' was not found")
            params["filters[country_id]"] = self._CountriesLookup[country]

        listOfServers = requests.get("https://api.nordvpn.com/v1/servers/recommendations",params=params, timeout=60).json()
        
        hostnames = [_ProxyServerDTO(server['hostname'], 89, "https") for server in listOfServers]
        return hostnames

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        
    def CreateClient(self, server: _ProxyServerDTO=Proxies_HTTPS.SE_1):
        '''
        Creates a wrapped requests client session with proxy tunnel.

        :param proxyServer: the desired proxy server to use, if none specified then a recommended server is chosen 

        The protocol used dictates wheter encryption is used while communicating over to proxy server.
        socks5 sends unencrypted data to proxy server. https proxies sends the data encrypted over to the proxy.
        From proxy to final destination encryption is used based on if the requested address was https or not.
        '''
        
        session = requests.Session()
        session.proxies = {
            'http': f'{server.protocol}://{self.username}:{self.password}@{server.hostname}:{server.port}',
            'https': f'{server.protocol}://{self.username}:{self.password}@{server.hostname}:{server.port}',
        }
        return session


# def __Compiler_ProxyList_HTTPS__():
#     nordvpn = NordVPNProxy(None, None)
#     databuilder = []
#     for country in ['SE', 'NL', 'US']:
#         servers = nordvpn.GetServers_Recommendations_HTTPS(limit=5, country=country)
#         for i, server in enumerate(servers):
#             databuilder.append(f'{country}_{i+1} = _ProxyServerDTO("{server.hostname}", 89, "https")')

#     res = "\n".join(databuilder)
#     return res