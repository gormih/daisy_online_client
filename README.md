# daisy_online_client

**Usage:**
```python
>>from client_messages import *

>>logon = DaisyOnlineLogon('userlogin', 'userpassword')
>>getserviceAttr = DaisyOnlineGetServiceAttributes()
>>attributes = {'manufacturer': 'gormihale',
          'model': 'is_test_system',
          'version': '1.0',
          'supportsMultipleSelections': 'false',
          'preferredUILanguage': 'en',
          'supportedContentFormats': ['ANSI/NISO Z39.86-2002', 'ANSI/NISO Z39.86-2005', 'DAISY 2.0', 	   'Daisy 2.02'],
          'supportedContentProtectionFormats': ['PDTB2'],
          'supportedMimeTypes': ['audio/mpeg',  'application/smil', 'text/plain',
                                 'text/xml', 'text/html'],
          'supportedInputTypes': ['TEXT_ALPHANUMERIC', 'AUDIO'],
          'requiresAudioLabels': 'false'
          }
  >>setservAttr = DaisyOnlineSetReadingSystemAttributes([], **attributes)
  >>print(msg.headers(), msg.dump() for msg in [logon, getserviceAttr, setservAttr]) 
```
