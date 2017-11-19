import decoder

dec = decoder.Decoder("192.168.1.15")

print 'First Group'
first_group = dec.get_first_group()
print first_group

print 'Second Group'
second_group = dec.get_second_group(1)
print second_group

print 'Channels'
channels = dec.get_channels(1, 10)
print channels

stream = dec.get_channel_stream(53)
print stream
