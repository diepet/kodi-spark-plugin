# -*- coding: utf-8 -*-
# Module: default
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
import xbmcaddon
import decoder

DECODER_IP_ADDRESS = xbmcaddon.Addon().getSetting('spark.video.decoderIPAddress');

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])
# Get addon instance
_addon = xbmcaddon.Addon()

def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def list_first_group():
    """
    Create the list of decoder first group of channels in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, _addon.getLocalizedString(30903))
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    # Create Decoder instance
    dec = decoder.Decoder(DECODER_IP_ADDRESS)
    # Get First Group
    first_group = dec.get_first_group()
    i = 0
    # Iterate through items group
    for item in first_group:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=item)
        list_item.setInfo('video', {'title': item, 'genre': item})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='get_second_group', first_group_title=item, first_group_index=i)
        i = i + 1
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)

def list_second_group(first_group_title, first_group_index):
    """
    Create the list of decoder second group of channels in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, _addon.getLocalizedString(30904))
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    # Create Decoder instance
    dec = decoder.Decoder(DECODER_IP_ADDRESS)
    # Get Second Group
    second_group = dec.get_second_group(int(first_group_index))
    i = 0
    # Iterate through items group
    for item in second_group:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=item)
        list_item.setInfo('video', {'title': item, 'genre': item})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='get_channels', first_group_title=first_group_title, first_group_index=first_group_index, second_group_title=item, second_group_index=i)
        i = i + 1
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)

def list_channels(first_group_title, first_group_index, second_group_title, second_group_index):
    """
    Create the list of decoder channels in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, _addon.getLocalizedString(30907))
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    # Create Decoder instance
    dec = decoder.Decoder(DECODER_IP_ADDRESS)
    # Get Second Group
    channels = dec.get_channels(int(first_group_index), int(second_group_index))
    # Iterate through items group
    for chan in channels:
        channel_name = chan['name']
        channel_group_id = chan['group_id']
        list_item = xbmcgui.ListItem(label=channel_name)
        list_item.setInfo('video', {'title': channel_name, 'genre': channel_name})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='play_channel', channel_group_id=channel_group_id)
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_channel(channel_group_id):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create Decoder instance
    dec = decoder.Decoder(DECODER_IP_ADDRESS)
    # Get Channel Stream
    # TODO to fix - 1
    channel_stream_url = dec.get_channel_stream(int(channel_group_id) - 1)
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=channel_stream_url)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'get_second_group':
            # Display the list of second group
            list_second_group(params['first_group_title'], params['first_group_index'])
        elif params['action'] == 'get_channels':
            # Display channels list
            list_channels(params['first_group_title'], params['first_group_index'], params['second_group_title'], params['second_group_index'])
        elif params['action'] == 'play_channel':
            # Play a video from a provided URL.
            play_channel(params['channel_group_id'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        #list_categories()
        list_first_group()

if __name__ == '__main__':

    if not DECODER_IP_ADDRESS:
        xbmcgui.Dialog().ok(_addon.getLocalizedString(30905), _addon.getLocalizedString(30906))
    else:
        # Call the router function and pass the plugin call parameters to it.
        # We use string slicing to trim the leading '?' from the plugin call paramstring
        router(sys.argv[2][1:])
