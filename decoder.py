import urllib2
import xml.etree.ElementTree as ET
import time

class Decoder:
    
    def __init__(self, ip):
        self.ip = ip

    def __get_xml_api_url(self, service):
        return 'http://' + self.ip + ":9090/api/xml/" + service

    def __get_channel_list_url(self):
        return self.__get_xml_api_url('get_channel_list')

    def __get_change_channel_url(self):
        return self.__get_xml_api_url('change_channel')

    def __get_channel_stream_url(self):
        return self.__get_xml_api_url('get_channel_stream')

    def __get_stream_status_url(self):
        return self.__get_xml_api_url('get_stream_status')

    def __get_stream_m3u_url(self):
        return 'http://' + self.ip + ':9090/api/stream.m3u'

    def get_first_group(self):
        url = self.__get_channel_list_url()
        xml_response = urllib2.urlopen(url).read()
        root = ET.fromstring(xml_response)
        nameElements = root.findall('./first_group/groups/item/name')
        names = [ ]
        for nameElem in nameElements:
            names.append(nameElem.text)
        return names
    
    def get_second_group(self, first_group_index):
        url = self.__get_channel_list_url()
        url = url + '?first_group=' + str(first_group_index)
        xml_response = urllib2.urlopen(url).read()
        root = ET.fromstring(xml_response)
        nameElements = root.findall('./second_group/groups/item/name')
        names = [ ]
        for nameElem in nameElements:
            names.append(nameElem.text)
        return names

    def get_channels(self, first_group_index, second_group_index):
        url = self.__get_channel_list_url()
        url = url + '?first_group=' + str(first_group_index) + '&second_group=' + str(second_group_index)
        xml_response = urllib2.urlopen(url).read()
        root = ET.fromstring(xml_response)
        itemElements = root.findall('./channel_list/channels/item')
        channels = [ ]
        for itemElem in itemElements:
            group_id = itemElem.find('group_id').text
            prog_id = itemElem.find('prog_id').text
            encrypt = itemElem.find('encrypt').text
            tp_num = itemElem.find('tp_num').text
            name = itemElem.find('name').text
            channels.append({'group_id': group_id, 'prog_id': prog_id, 'encrypt': encrypt, 'tp_num': tp_num, 'name': name})
        return channels

    def get_channel_stream(self, channel_group_id):
        # start changing channel
        url = self.__get_change_channel_url()
        url = url + '?gid=' + str(channel_group_id)
        xml_response = urllib2.urlopen(url).read()
        root = ET.fromstring(xml_response)
        errorCodeElement = root.find('./error/code')
        errorMessageElement = root.find('./error/message')
        if errorCodeElement.text != '0' or errorMessageElement.text != 'success':
            raise ValueError('Unable to change channel')
        # end changing channel
        # -----------
        # start get channel stream
        url = self.__get_channel_stream_url()
        url = url + '?gid=' + str(channel_group_id)
        xml_response = urllib2.urlopen(url).read()
        root = ET.fromstring(xml_response)
        udp_stream_port = root.find('./udp_stream_port').text
        udp_server_port = root.find('./udp_server_port').text
        # end get channel stream
        # -----------
        # start checking stream status url
        url = self.__get_stream_status_url()
        retry = 5
        sleep_time = 2
        xml_response = urllib2.urlopen(url).read()
        root = ET.fromstring(xml_response)
        status_code = root.find('./code').text
        # Start checking if stream status code is equals to 3
        # Status codes known are:
        #   2: Started, but have not get PMT.
        #   3: Got PMT and recording.
        while retry > 0 and status_code != '3':
            # if stream status code was not 3 and retry limit does not reached
            # then check again stream status code
            retry = retry - 1
            time.sleep(sleep_time)
            xml_response = urllib2.urlopen(url).read()
            root = ET.fromstring(xml_response)
            status_code = root.find('./code').text
        if status_code != '3':
            raise ValueError('Unable to initialize stream')
        # end checking stream url
        # -----------
        # start downloading m3u url
        url = self.__get_stream_m3u_url()
        m3u_content = urllib2.urlopen(url).read()
        return m3u_content
