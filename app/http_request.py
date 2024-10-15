import requests
import app

from app.sanitize_module import SanitizeModule

class HttpClient:
    def get(url, headers=None):
        if not app.cert:
            app.cert = False
        return requests.get(url, headers=headers, verify=app.cert)
    
    def get_locale():
        if not app.cert or not app.IPINFO_TOKEN:
            app.cert = False
        
        url = f"http://ipinfo.io/{HttpClient.get_public_ip()}/json"
        
        if app.IPINFO_TOKEN:
            headers = {
                'Authorization': f'Bearer {app.IPINFO_TOKEN}'
            }
        try: 
            response = requests.get(url, headers=headers, verify=app.cert)
            if response.status_code == 200:
                data = response.json()
                country_code = data['country']
                return country_code
            else:
                raise requests.exceptions.HTTPError(response)
        except requests.exceptions.RequestException as e:
            print('Error obtaining locale...')
            print(e)

    def get_public_ip():
        try:
            response = requests.get('https://api.ipify.org?format=json', verify=app.cert)
            if response.status_code == 200:
                return response.json()['ip']
            else:
                raise requests.exceptions.HTTPError(response)
        except requests.exceptions.RequestException as e:
            print('Error fetching IP...')
            print(e)    
    
    def error_handler(response):
        return requests.exceptions.HTTPError(response)
    
    def get_error_status(error):
        return type(error).__name__
    
    def http_request(url, counter, original_data=None):
        response = None
        try:
            headers = {'User-Agent': app.user_agent,} if app.user_agent else None
            response = HttpClient.get(url, headers=headers)
            if response.status_code == 200:
                message = "OK"
                print(f"{counter} Status {message} [{response.status_code}]: {url}")
                if app.sanitize:
                    result = SanitizeModule.result_sanitizer(url, response.status_code, response, original_data)
                    return result
            else: 
                raise requests.exceptions.HTTPError(response)
        except requests.exceptions.RequestException as e:    
            if response is not None:
                message = "FAILED"
                status = response.status_code if response is not None else HttpClient.get_error_status(e)
                print(f"{counter} Status {message} [{status}]: {url} {e}") 
                result = SanitizeModule.result_sanitizer(url, status, response, original_data, e)
                return result