import re
import requests
from PyBypass.Shortners import *
from PyBypass.Filehoster import *
from PyBypass.Constants import *
from PyBypass.GdriveSharer import *
from PyBypass.VideoServers import *

class BypasserNotFoundError(Exception):
	"""
	Raise when there is no bypasser script for the provided URL.
	"""
		

class UrlConnectionError(Exception):
	"""
	Raise when response code of given url is not equal to 200
	"""
	
	
class RequiredValueNotFoundError(Exception):
	"""
	Raise when user didn't provided required parameters.
	( Example: gdot_crypt, appdrive_email etc )
	"""

class UnableToBypassError(Exception):
	"""
	Raise when script is unable to bypass the given url. 
	( possible reason can be wrong link, wrong parameters, cloudfare protection or script is patched)
	"""

		
def _requiredvaluechecker(function):

	"""
	A decorator to check if required parameters is/are present or not  to bypass 
	the given links
	"""
	
	def wrapper_function(*args, **kwargs):
		
		func_name = args[-1]
		if func_name == "gdtot_bypass" and "gdtot_crypt" not in kwargs:
			raise RequiredValueNotFoundError("Missing required parameter 'gdtot_crypt'. please enter your GDOT crypt value")


		if func_name == "appdrive_bypass" and not all(
			[("appdrive_email" in kwargs), ("appdrive_password" in kwargs)]
		):
			raise RequiredValueNotFoundError("Missing required parameter 'appdrive_email' and 'appdrive_password. please enter yout appdrive credentials to bypass the given link.")


		if func_name == "hubdrive_bypass" and "hubdrive_crypt" not in kwargs:
			raise RequiredValueNotFoundError("Missing required parameter 'hubdrive_crypt'. please enter your hubdrive crypt value")


		if func_name == "sharerpw_bypass" and not all(
			[
				("sharerpw_xsrf_token" in kwargs),
				("sharerpw_larvel_session" in kwargs),
			]
		):
			raise RequiredValueNotFoundError("Missing required parameter 'sharerpw_xsrf_token' and 'sharerpw_larvel_session. please enter yout sharer.pw credential value to bypass the given link.")	

		value = function(*args, **kwargs)
		return value	

	return wrapper_function


		
class PyBypass:
		
	def _init__(self):
		pass

	@_requiredvaluechecker
	def redirect_function(self, url, bypasser_function, **kwargs):
		
		parameter = "".join(f" ,{key}='{values}' " for key, values in kwargs.items())
		parameter = parameter.strip()


		try:
			bypassed_value = eval(f"{bypasser_function}('{url}'{parameter})")
		except Exception as e:
			raise UnableToBypassError("Can not able to bypass this link. Possible reason can be cloudfare protection, wrong link, wrong parameters, expired  link or script is patched")


		if bypassed_value is None:
			raise UnableToBypassError("Can not able to bypass this link. Possible reason can be cloudfare protection, wrong link, wrong parameters, expired  link or script is patched")
		return bypassed_value
		 
		 
									
	def bypass(self, url, name=None, **kwargs):
		
		if "ouo.press" in url or "linkbnao.com" in url or "go.earnl.xyz" in url:
			pass
			
		else:
			try:
				response = requests.get(url)
				
			except Exception as e:
				raise UrlConnectionError("Not able to establish a successful connection with given URL. It is probably protected by cloudfare.")
			
			if response.status_code != 200:
				raise UrlConnectionError("Not able to establisha a successful connection with given URL. It is probably protected by cloudfare.")
	
	
		bypasser_function = None
		
		if name:
		    for (key,value) in MAIN_REGEX.items():
		    	if name.lower() == value[0]:
		    		bypasser_function = value[1] ; break

		else:
			for (key,value) in MAIN_REGEX.items():		
				if bool(re.search(FR"{key}", url)):
					bypasser_function = value[1]						
		
		if bypasser_function is not None:
			return self.redirect_function(url, bypasser_function, **kwargs)
		else:
			raise BypasserNotFoundError("can not find a bypasser script found for this URL.")


def bypass(url, name=None, **kwargs):
	bypasser = PyBypass()
	return bypasser.bypass(url , name=name, **kwargs)
