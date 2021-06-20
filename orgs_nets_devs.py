import requests
import json
from merakiCredentials import MerakiKey


def get_orgs():
	"""function for retrieving a list of organizations managed by Merarki
	"""
	global hdr
	url = "https://api.meraki.com/api/v0/organizations"
	hdr = {'X-Cisco-Meraki-API-Key': MerakiKey, 'content-type' : 'application/json'}
	resp = requests.get(url, headers=hdr)
	print(resp)
	org_list = resp.json()
	get_networks(org_list)



def get_networks(org_list):
	"""Print out the list of networks for each organization
	"""
	global org
	for org in org_list:
		#print('Collecting network list for {}'.format(org['name']))
		url = 'https://api.meraki.com/api/v0/organizations/{}/networks'.format(org['id'])
		resp = requests.get(url, headers=hdr)
		net_list = resp.json()
		get_devices(net_list)


def get_devices(net_list):
	"""Collect the devices in a network
	"""
	for net in net_list:
		try:
			print("Collecting Devices for the {} network which is part of the {} organization".format(net['name'], org['name']))
			url = 'https://api.meraki.com/api/v0/organizations/{}/networks/{}/devices'.format(org['id'], net['id'])
			resp = requests.get(url, headers=hdr)
			dev_list = resp.json()
			print_dev_info(dev_list)
		except:
			print('{} organization either has not networks or the networka have no devices'.format(org['name']))
			pass
		print('\n')


#Functions to Print Nice tables
def print_orgs_info(org_list):
	"""Print list of organizations
	"""
	print("{0:30}{1:30}".format("Organization ID", "Organization Name"))
	for org in orgs_list:
		print("{0:30}{1:30}".format(org['id'], org['name']))

def print_net_info(net_list):
	"""Print the list of networks in each organization
	"""
	print("{0:30}{1:30}{2:30}".format("Organization ID", "Network ID", "Network Name"))
	for net in net_list:
		print("{0:30}{1:30}{2:30}".format(net['organizationId'], net['id'], net['name']))


def print_dev_info(dev_list):
	"""print the list of devices in each network
	"""
	print('{0:30}{1:30}{2:30}'.format('Network ID', 'Device Name', 'Device Model'))
	for dev in dev_list:
		print('{0:30}{1:30}{2:30}'.format(dev['networkId'], dev['name'], dev['model']))

if __name__ == "__main__":
	get_orgs()