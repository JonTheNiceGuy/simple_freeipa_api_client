from freeipa_api import IpaApi, ApiError

def main():
  try:
    IPA = IpaApi('freeipa.example.org', 'dns_record_service_account', 'THIS_IS_A_BAD_IDEA...Do_NOT_store_plain_text_passwords')
    result = IPA.post('dnsrecord_show', ['example.org.', 'this_host_exists'])
    if 'result' in result and result['result']:
      ApiResult = result['result']
      if 'result' in ApiResult and ApiResult['result']:
        data = ApiResult['result']
        if 'arecord' in data and len(data['arecord']) > 0:
          print(f"A Record: {data['arecord']}")
        if 'aaaarecord' in data and len(data['aaaarecord']) > 0:
          print(f"AAAA Record: {data['aaaarecord']}")
        if 'cnamerecord' in data and len(data['cnamerecord']) > 0:
          print(f"CNAME Record: {data['cnamerecord']}")
  except ApiError as e:
        if 'DNS resource record not found' in e.args[0]:
            logging.debug('No record found, carrying on')
            method = 'dnsrecord_add'
        else:
            raise e

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(e)
        exit(1)
