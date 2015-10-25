Python Netconf abstraction layer for Cisco IOS XE devices
=======

This is a python library that makes it easy as pie to talk Netconf to any IOS
XE device that supports netconf.


# Install 

**Option 1**

```
sudo pip install pyskate
```

Using `pip` also installs `xmltodict` and `ncclient` that are required.

**Option 2**

Clone this repository, modify your PYTHONPATH, and do all that fun stuff!

# Connecting to device

```python
>>> 
>>> from pyskate import IOSXEDevice
>>> 
>>> router = IOSXEDevice('hostname','username','password')
>>> router.connect()
```

# Disconnecting from device

```python
>>> 
>>> router.disconnect()
```
# Retrieving running configuration
```python
>>> config = router.get_config()

```
# Editing running configuration 
```python
>>> router.edit_config("interface Gi1\ndescription spam")

```
# Saving running configuration to startup configuration
```python
>>> router.save_config()

```
# Executing command
```python
>>> cmd_output = router.exec_command("show interface")

```
