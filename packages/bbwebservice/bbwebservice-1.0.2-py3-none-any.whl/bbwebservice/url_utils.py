
HEX_CHARS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
import re

def unescape_url(url:str) -> str:
    unescaped = ''
    escape_sequence = ''
    index = 0
    url_len = len(url)
    
    while index < url_len:
        if url[index] == '%' and index + 3 <= url_len and url[index+1] in HEX_CHARS and url[index+2] in HEX_CHARS and len(escape_sequence) <= 6:
            escape_sequence += url[index:index+3]
            index += 3
        elif escape_sequence:
            unescaped += decode_url_encoded_string(escape_sequence)
            unescaped += url[index]
            escape_sequence = ''
            index += 1
        else:
            unescaped += url[index]
            index += 1
    return unescaped
            

def decode_url_encoded_string(url_encoded_string:str) ->str:
    try:
        encoded_parts = url_encoded_string.split('%')[1:]
        decoded_bytes = bytes([int(part[:2], 16) for part in encoded_parts])
        unicode_char = decoded_bytes.decode('utf-8')
        return unicode_char
    except UnicodeDecodeError:
        return None


#TODO: native URL matching withoug re for better performance 
#TODO: special hashing were string gets hash of matching template 
class UrlTemplate:
    
    def __init__(self, template_string):
        self.template = template_string
        self.regex_pattern = re.sub(r'\{(\w+):(\w+)\}', self._repl, template_string)
        self.handler = None
        self.type = None
    
    def _repl(self, match):
        type_ = match.group(2)
        if type_ == 'int':
            return r'(\d+)'
        elif type_ == 'str':
            return r'(\w+)'
        elif type_ == 'float':
            return r'(\d+\.\d+)'
        elif type_ == 'bool':
            return r'(True|False)'
        else:
            raise ValueError(f"Unknown type: {type_}")
        
    def convert(self, value, type_):
        if type_ == 'int':
            return int(value)
        elif type_ == 'float':
            return float(value)
        elif type_ == 'float':
            return bool(value)
        else:
            return value
        
    def extract(self, url):
        match = re.match(self.regex_pattern, url)
        if match:
           return {k: self.convert(v, t) for (k, t), v in zip(re.findall(r'\{(\w+):(\w+)\}', self.template), match.groups())}
        else:
            return None
        
    def __eq__(self, url):
        
        if isinstance(url, str):
            return re.match(self.regex_pattern, url)
        if isinstance(url,self.__class__):
            return self.template == url.template
        
        return False
