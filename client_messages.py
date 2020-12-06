# Author: Mikhail Goryunov <gormih78@yandex.ru>
from lxml import etree


def daisy_sub_element(base_elemet, sub_element_name, attrs={}):
    daisy_ns = {'do': "http://www.daisy.org/ns/daisy-online/"}
    return etree.SubElement(base_elemet,
                            '{%s}%s' % (daisy_ns['do'], sub_element_name), attrib=attrs,
                            nsmap=daisy_ns)


def daisy_element(element_name, attrs={}):
    daisy_ns = {'do': "http://www.daisy.org/ns/daisy-online/"}
    return etree.Element('{%s}%s' % (daisy_ns['do'], element_name), attrib=attrs,
                         nsmap=daisy_ns)


class SoapEnvelope(object):
    root_ns = {'SOAP-ENV': "http://schemas.xmlsoap.org/soap/envelope/"}

    def __init__(self, *args, **kwargs):
        self.root = etree.Element('{%s}Envelope' % self.root_ns["SOAP-ENV"], nsmap=self.root_ns)
        self.root.append(etree.Element('{%s}Header' % self.root_ns["SOAP-ENV"]))
        self.expand_envelope(*args, **kwargs)

    def expand_envelope(self, *args, **kwargs):
        pass

    def dump(self, pretty_print=False):
        return etree.tostring(self.root, pretty_print=pretty_print).decode()


class DaisyOnlineBase(SoapEnvelope):
    daisy_ns = {'do': "http://www.daisy.org/ns/daisy-online/"}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body = 0
        if not self.__class__.__name__.startswith('DaisyOnline'):
            raise ValueError('Chield method MUST have start name from "DaisyOnline"')

    def expand_envelope(self, *args, **kwargs):
        self.body = etree.Element('{%s}Body' % self.root_ns["SOAP-ENV"], nsmap=self.daisy_ns)
        self.expand_body(*args, **kwargs)
        self.root.append(self.body)

    def expand_body(self, *args, **kwargs):
        pass

    def ret_headers(self):
        action = self.__class__.__name__[len('DaisyOnline'):]
        action = action[0].lower() + action[1:]
        self.headers['SOAPAction'] = action
        return self.headers


class DaisyOnlineLogon(DaisyOnlineBase):

    def expand_body(self, *args, **kwargs):
        action = etree.SubElement(self.body, '{%s}logOn' % self.daisy_ns['do'], nsmap=self.daisy_ns)
        username = daisy_sub_element(action, 'username')
        password = daisy_sub_element(action, 'password')
        username.text = args[0]
        password.text = args[1]


class DaisyOnlineLogoff(DaisyOnlineBase):
    def expand_body(self, *args, **kwargs):
        self.body.append(daisy_element('logOff'))


class DaisyOnlineGetServiceAttributes(DaisyOnlineBase):

    def expand_body(self, *args, **kwargs):
        self.body.append(daisy_element('getServiceAttributes'))


class DaisyOnlineSetReadingSystemAttributes(DaisyOnlineBase):

    def expand_body(self, *args, **kwargs):
        action = daisy_sub_element(self.body, 'setReadingSystemAttributes')
        readingSystemAttributes = daisy_sub_element(action, 'readingSystemAttributes')
        manufacturer = daisy_sub_element(readingSystemAttributes, 'manufacturer')
        manufacturer.text = kwargs['manufacturer']
        model = daisy_sub_element(readingSystemAttributes, 'model')
        model.text = kwargs['model']
        version = daisy_sub_element(readingSystemAttributes, 'version')
        version.text = kwargs['version']
        config = daisy_sub_element(readingSystemAttributes, 'config')
        config_supportsMultipleSelections = daisy_sub_element(config, 'supportsMultipleSelections')
        config_supportsMultipleSelections.text = kwargs['supportsMultipleSelections']
        config_preferredUILanguage = daisy_sub_element(config, 'preferredUILanguage')
        config_preferredUILanguage.text = kwargs['preferredUILanguage']
        config_supportedContentFormats = daisy_sub_element(config, 'supportedContentFormats')
        for _contentFormat in kwargs['supportedContentFormats']:
            contentFormat = daisy_sub_element(config_supportedContentFormats, 'contentFormat')
            contentFormat.text = _contentFormat
        config_supportedContentProtectionFormats = daisy_sub_element(config, 'supportedContentProtectionFormats')
        for _contentProtectionFormat in kwargs['supportedContentProtectionFormats']:
            contentProtectionFormat = daisy_sub_element(config_supportedContentProtectionFormats, 'contentFormat')
            contentProtectionFormat.text = _contentProtectionFormat
        config_supportedMimeTypes = daisy_sub_element(config, 'supportedMimeTypes')
        for _supportedMimeType in kwargs['supportedMimeTypes']:
            config_supportedMimeTypes.append(daisy_element('mimeType', attrs={'type': _supportedMimeType}))
        config_supportedInputTypes = daisy_sub_element(config, 'supportedInputTypes')
        for _supportedInputType in kwargs['supportedInputTypes']:
            config_supportedInputTypes.append(daisy_element('input',
                                              attrs={'type': _supportedInputType}))
        config_requiresAudioLabels = daisy_sub_element(config, 'requiresAudioLabels')
        config_requiresAudioLabels.text = kwargs['requiresAudioLabels']


class DaisyOnlineGetQuestions(DaisyOnlineBase):

    def expand_body(self, *args, **kwargs):
        getQuestions = daisy_sub_element(self.body, 'getQuestions')
        userResponses = daisy_sub_element(getQuestions, 'userResponses')
        for _userResponse in kwargs['userResponses']:  # User Responses is list of dict
            userResponses.append(daisy_element('userResponse', attrs=_userResponse))  # User response is dict, example:
            # {'questionID':'root'
            #   'value':'genres'}


class DaisyOnlineGetContentList(DaisyOnlineBase):

    def expand_body(self, *args, **kwargs):
        getContentList = daisy_sub_element(self.body, 'getContentList')
        id = daisy_sub_element(getContentList, 'id')
        id.text = kwargs['id']
        firstItem = daisy_sub_element(getContentList, 'firstItem')
        firstItem.text = kwargs['firstItem']
        lastItem = daisy_sub_element(getContentList, 'lastItem')
        lastItem.text = kwargs['lastItem']


class DaisyOnlineGetContentResources(DaisyOnlineBase):

    def expand_body(self, *args, **kwargs):
        getContentResources = daisy_sub_element(self.body, 'getContentResources')
        contentID = daisy_sub_element(getContentResources, 'contentID')
        contentID.text = args[0]


class DaisyOnlineGetContentMetadata(DaisyOnlineBase):

    def expand_body(self, *args, **kwargs):
        getContentMetadata = daisy_sub_element(self.body, 'getContentMetadata')
        contentID = daisy_sub_element(getContentMetadata, 'contentID')
        contentID.text = args[0]


class DaisyOnlineReturnContent(DaisyOnlineBase):

    def expand_body(self, *args, **kwargs):
        returnContent = daisy_sub_element(self.body, 'returnContent')
        contentID = daisy_sub_element(returnContent, 'contentID')
        contentID.text = args[0]
