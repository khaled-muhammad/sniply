import json


class Account:
    def __init__(self, platform, username, cookies):
        self.platform = platform
        self.username = username
        self.cookies  = cookies
    
    @staticmethod
    def from_path(platform, path):
        with open(path, 'r') as f:
            cookies = json.load(f)
        
        return Account(platform, path.split('/')[-1].removesuffix('.sc'), cookies)