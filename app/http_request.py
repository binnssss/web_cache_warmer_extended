import requests
import app

from requests.exceptions import RequestException

class HttpClient:
    def get(self, url, headers=None):
        return requests.get(url, headers=headers)
    
    def error_handler(response):
        return requests.exceptions.HTTPError(f"Error [{response.status_code}]")
    
    def get_error_status(error):
        return type(error).__name__
    
    def http_request(url, counter):
        response = None
        try:
            headers = {'User-Agent': app.user_agent} if app.user_agent else None
            response = HttpClient.get(url, headers=headers)
            print(url)
            if response.status_code == 200:
                message = "OK"
                print(f"{counter} Status {message} [{response.status_code}]: {url}")
            else:
                raise HttpClient.error_handler(response)
        except RequestException as e:
            message = "FAILED"
            status = response.status_code if response is not None else HttpClient.get_error_status(e)
            print(f"{counter} Status {message} [{status}]: {url} {e}")
            result = {'url': url, 'status': status, 'error': f"{e}"}
            return result