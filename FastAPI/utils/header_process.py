import re

mime_types=['application','audio','text','image','video','etc']
#####################################
##Handle requests from the user######
#####################################
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
def get_request_header_data(headers):

    bearer_token=get_header_authentication(headers)
    origin=get_origin_ip_address(headers)
    referer = headers.get('referer')
    user_id = headers.get('user_id')
    return {
        'bearer_token': bearer_token,
        'origin': origin,
        'referer' : referer,
        'user_id' : user_id
        }
#####################################
##Handle response from the database##
#####################################
def get_header_mime_type(headers):
    mime_type={key.decode('utf-8'): value.decode('utf-8') for key, value in headers}.get('content-type')
    if '/' in mime_type:
        mime_type = mime_type.split('/')[0]
        if mime_type not in mime_types:
            mime_type='etc'
    else:
        raise ValueError(f'MIME format invalid :{mime_type}')
    return mime_type
def get_response_length(headers):
    response_length=int({key.decode('utf-8'): value.decode('utf-8') for key, value in headers}.get('content-length'))
    return response_length
def get_response_header_data(headers):
    mime_type=get_header_mime_type(headers)
    response_length=get_response_length(headers)
    return {
        'mime_type' : mime_type,
        'response_length' : response_length
    }
    

