Release notes
=======

# 0.1.2 (2015-01-15)

* Catch RPCError from ncclient when configuration fails and raise ConfigDeployError.
* Add IfMissingError, BGPMissingError and VRFMissingError exception.
* Remove broken get_config_with_filter() function.
* Add get_interface_config() function.
* Add get_bgp_config() function.
* Add get_vrf_definition_config() function.

# 0.1
* Initial public release.
