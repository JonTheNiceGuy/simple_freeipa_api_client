# simple_freeipa_api_client

This simple python class will help you build interactions with the FreeIPA service and RedHat IdM service.

There is an example.py file which gives you an idea of how to call the IpaApi function.

__Note that you SHOULD NOT store credentials in your source code. I recommend and endorse [SOPS](https://github.com/getsops/sops) but that is outside the scope of this document.__

Something to note; if you're making an JSON-RPC API call against FreeIPA/IDM, there is a great web interface which describes all the API calls. Note that any of the arguments you see must all be provided in a list, in the order provided, while options can be passed in any order

![image](https://github.com/JonTheNiceGuy/simple_freeipa_api_client/assets/228671/4d5c739c-083c-41f3-9f05-f48791f5b842)

For example, using the above record, you need to call:

```
method = 'dnsrecord_add'
arguments = [
  'dns.zone.example.org.', # dnszoneidnsname
  'dnsname'                # idnsname
]
options = {
  'arecord': '192.0.2.1',
  'dnsttl': '3600'
}
IPA.post(method, arguments, options)
```

## Security Notifications

Please feel free to raise any issues via [issues](https://github.com/JonTheNiceGuy/simple_freeipa_api_client/issues), raising a pull request with a fix, or, alternatively, [contact me directly](mailto:jon@sprig.gs). Be aware, however, this is a small library to help you make simple scripts, and there is no support offered here, either implied or explicit.
