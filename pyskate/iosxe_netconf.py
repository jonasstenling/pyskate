'''Netconf implementation for IOSXE devices'''

from ncclient import manager
from ncclient.transport.errors import TransportError
import xmltodict

def reconnect_device(func):
    '''When a method is using this decorator and self.reconnect == True, try
       to reconnect to the device if a TransportError exception is thrown by
       ncclient. This typically happens if the router has disconnected the
       connection due to inactivity.'''
    def inner(self, *args, **kwargs):
        '''Wrap decorated function and reconnect as wanted.'''
        if self.reconnect == True:
            try:
                return func(self, *args, **kwargs)
            except TransportError:
                self.connect()
                return func(self, *args, **kwargs)
        else:
            return func(self, *args, **kwargs)
    return inner

class IOSXEDevice(object):
    '''Implements methods for configuration retrieval and update'''
    def __init__(self, hostname, username, password, reconnect=True, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.reconnect = reconnect
        self.port = port
        self.handle = None

    def connect(self):
        '''Returns True if connect to device is successful.'''
        self.handle = manager.connect_ssh(self.hostname,
                                          username=self.username,
                                          password=self.password,
                                          port=self.port,
                                          hostkey_verify=False)

    def disconnect(self):
        '''Returns True if disconnect from device is successful.'''
        try:
            self.handle.close_session()
        except TransportError:
            return True # already disconnected

#
# This function doesn't work as expected, filtered configuration
# is returned truncated at the top. Troubleshooting ongoing.
#
    @reconnect_device
    def get_config_with_filter(self, netconf_filter):
        '''Returns filtered running config in device as list
           Filter is specified as "| ?
               exclude
               include
               section"
           E.g. "| section ^interface" for all interface configuration'''
        netconf_filter = """
<filter>
<config-format-text-cmd>
<text-filter-spec>{netconf_filter}</text-filter-spec>
</config-format-text-cmd>
</filter>""".format(netconf_filter=netconf_filter)
        response = xmltodict.parse(self.handle.get(netconf_filter).xml)
        return response['rpc-reply']['data']['cli-config-data']['cmd']

    @reconnect_device
    def get_config(self):
        '''Returns running config in device as list.'''
        response = xmltodict.parse(self.handle.get().xml)
        return response['rpc-reply']['data']['cli-config-data-block'].split('\n')


    @reconnect_device
    def exec_command(self, command):
        '''Returns output of executed command as list.'''
        netconf_filter = """
<filter>
<config-format-text-block>
<text-filter-spec>| begin ^end </text-filter-spec>
</config-format-text-block>
<oper-data-format-text-block>
<exec>{command}</exec>
</oper-data-format-text-block>
</filter>""".format(command=command)
        response = xmltodict.parse(self.handle.get(netconf_filter).xml)
        return response['rpc-reply'] \
                       ['data']['cli-oper-data-block']['item']['response'].split('\n')

    @reconnect_device
    def edit_config(self, commands):
        '''Returns True if commit of *commands* to running configuration is
        successful.'''
        config = """
<config>
<cli-config-data-block>
{commands}
</cli-config-data-block>
</config>""".format(commands=commands)
        response = xmltodict.parse(
            self.handle.edit_config(target='running', config=config).xml)
        return 'ok' in response['rpc-reply'] # Got <ok /> tag

    @reconnect_device
    def save_config(self):
        '''Returns true if save of running configuration is successful.'''
        return '[OK]' in self.exec_command('copy running startup')
