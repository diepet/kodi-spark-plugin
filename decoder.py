import json
import urllib2

class Decoder:
    
    def __init__(self, ip):
        self.ip = ip

    def __get_json_url(self, service):
        if self.ip:
            return 'http://' + self.ip + "/json/" + service
        else:
            return ''

    def __get_ok_list_url(self):
        json_url = self.__get_json_url('get_ok_list')
        if (json_url):
            return json_url + '?'
        else:
            return ''
    def __get_channel_stream_url(self):
        json_url = self.__get_json_url('get_channel_stream')
        if (json_url):
            return json_url + '?'
        else:
            return ''

    def __get_video_html_url(self):
        if self.ip:
            return 'http://' + self.ip + "/webstv/video.html?"

    def get_first_group(self):
        url = self.__get_ok_list_url()
        try:
            data = json.load(urllib2.urlopen(url))
            return data['firstgroup']['name']
        except:
            return []
    
    def get_second_group(self, first_group_index):
        url = self.__get_ok_list_url()
        url = url + "group1=" + str(first_group_index)
        try:
            data = json.load(urllib2.urlopen(url))
            return data['secondgroup']['name']
        except:
            return []

    def get_channels(self, first_group_index, second_group_index):
        url = self.__get_ok_list_url()
        url = url + "group1=" + str(first_group_index) + "&group2=" + str(second_group_index)
        try:
            data = json.load(urllib2.urlopen(url))
            return data['program']['channels']
        except:
            return []

    def get_channel_stream(self, channel_group_id):
        url = self.__get_video_html_url()
        url = url + "op=1&channelIndex=" + str(channel_group_id)
        urllib2.urlopen(url)
        url = self.__get_channel_stream_url()
        url = url + "gid=" + str(channel_group_id)
        try:
            data = json.load(urllib2.urlopen(url))
            return data
        except:
            return     