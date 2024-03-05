import re

mime_types=['application','audio','text','image','video','etc']

def get_header_authentication(headers):
    pattern=r'^Bearer\s.*'
    if len(headers['authorization']) > 7 and bool(re.match(pattern=pattern,string=headers['authorization'])):
        bearer_token=headers['authorization'][7:]
    else:
        raise AttributeError('No bearer token found')
    return bearer_token
def get_origin_ip_address(headers):
    if 'X-Forwarded-For' in headers: #if the packet already passed through a NGINX reverse proxy server
        origin=headers['X-Forwarded-For']
    elif 'origin' in headers: 
        origin=headers['origin']
    else:
        raise KeyError('No origin IP address found')
    return origin
def get_header_mime_type(headers):
    mime_type=headers.get('content-type')
    if '/' in mime_type:
        mime_type = mime_type.split('/')[0]
        if mime_type not in mime_types:
            mime_type='etc'
    else:
        raise ValueError(f'MIME format invalid :{mime_type}')
def get_header_data(headers):
    bearer_token=get_header_authentication(headers)
    origin=get_origin_ip_address(headers)
    mime_type=get_header_mime_type
    referer = headers.get('referer')
    method = headers.get('method')
    return {
        'bearer_token': bearer_token,
        'origin': origin,
        'mime_type' : mime_type,
        'referer' : referer,
        'method' : method
        }

