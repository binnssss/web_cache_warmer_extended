import requests
import app

from app.sanitize_module import SanitizeModule

class HttpClient:
    def get(url, headers=None):
        return requests.get(url, headers=headers, verify=app.cert)
    
    def get_locale():
        response = requests.get('https://ipinfo.io', verify=False)
        data = response.json()
        country_code = data['country']
        return country_code
    
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
            else: 
                raise requests.exceptions.HTTPError(response)
        except requests.exceptions.RequestException as e:    
            print(e)
            if response is not None:
                message = "FAILED"
                status = response.status_code if response is not None else HttpClient.get_error_status(e)
                print(f"{counter} Status {message} [{status}]: {url} {e}")
                result = SanitizeModule.result_sanitizer(url, status, response, original_data, e)
                return result