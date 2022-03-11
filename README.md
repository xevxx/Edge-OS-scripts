# Edge-OS-scripts
Scripts for edgerouter manipulation

edgeosMonitorDNS.py
Inspired by https://community.ui.com/questions/Python-script-I-made-to-update-dynamic-ip-address-in-firewall/ad178566-1cab-453b-8e2a-1f75fd0c0477 and https://gist.github.com/m-hume/9e882d83e084ebf08f9f
This script monitors my Adguard and Pihole vms, all dns traffic is routed through them for my network using NAT rules, no matter the local dns setting; 
for whatever reasons the server might go down but this was causing the internet not to work on home network, 
big problem if i wasnt at home to reboot server or reconfigure edgerouter.

The script will ping the ip address configured.
it matches against address group i had created matched to the nat rules

if monitor is up and nat rules disabled, they are then enabled
if monitor is down and nat rules enabled, they are disabled

It is run every min using task scheduler.
