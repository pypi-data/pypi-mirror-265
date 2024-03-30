
# started from original 0.0.6. 
# I don't see any CVE as the original author had declared. keep using.
import sys
import requests

IS_PY3 = sys.version_info[0] == 3

if not IS_PY3:
  raise ValueError("This package only supports python3")


class ApiError(Exception):

  def __init__(self, http_response):
    content = http_response.json()
    self.status_code = http_response.status_code
    self.status_desc = content['error']['statusdesc']
    self.error_message = content['error']['errormessage']
    super(ApiError, self).__init__(self.__str__())

  def __repr__(self):
    return 'pingdomv3.ApiError: HTTP `%s - %s` returned with message, "%s"' % \
           (self.status_code, self.status_desc, self.error_message)

  def __str__(self):
    return self.__repr__()


class Api(object):

  def __init__(self, token):
    self.base_url = "https://api.pingdom.com/api/3.1/"
    self.headers = {'Authorization': 'Bearer %s' % token}

  def send(self, method, resource, resource_id=None, data=None, params=None):
    if data is None:
      data = {}
    if params is None:
      params = {}
    if resource_id is not None:
      resource = "%s/%s" % (resource, resource_id)
    response = requests.request(method, self.base_url + resource,
                                headers=self.headers,
                                data=data,
                                params=params
                                )
    if response.status_code != 200:
      raise ApiError(response)
    else:
      return response.json()


class Client(object):
  """
  Pingdom client
  """

  def __init__(self, token):
    """
    Initializer.

    :param token: Pingdom V3 API Token. Generate from https://my.pingdom.com/3/api-tokens
    """
    self.token = token
    self.api = Api(token)

  def get_checks(self, limit: int = None,
                 offset: int = None,
                 showencryption: bool = None,
                 include_tags: bool = None,
                 include_severity: bool = None,
                 tags: str = None
                 ):
    """
    https://docs.pingdom.com/api/#tag/Checks/paths/~1checks/get
    """
    params = {}
    if limit is not None:
      params['limit'] = limit
    if offset is not None:
      params['offset'] = offset
    if showencryption is not None:
      params['showencryption'] = showencryption
    if include_tags is not None:
      params['include_tags'] = include_tags
    if include_severity is not None:
      params['include_severity'] = include_severity
    if tags:
      params['tags'] = tags
    return self.api.send('get', "checks", params=params)['checks']

  def get_check(self, check_id):
    return self.api.send('get', "checks/%s" % check_id)['check']

  def create_check(self, check_detail):
    return self.api.send('POST', "checks", data=check_detail)['check']

  def update_check(self, check_id, check_detail):
    return self.api.send('PUT', f"checks/{check_id}", data=check_detail)

  def duplicate_check(self, check_id):
    detail = self.get_check(check_id)
    detail['host'] = str(detail.get('hostname'))
    detail['name'] = 'Copy Of %s' % detail.get('name')
    for unused_key in ('id', 'created', 'hostname', 'lasttesttime', 'lastresponsetime', 'status', 'lasterrortime'):
      detail.pop(unused_key, None)
    if 'tags' in detail:
      detail['tags'] = ','.join([t['name'] for t in detail['tags']])

    return self.create_check(detail)

  def delete_check(self, check_id):
    return self.api.send('delete', 'checks/%s' % check_id)
