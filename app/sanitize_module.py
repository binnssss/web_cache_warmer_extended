import app

class SanitizeModule:

    def result_sanitizer(url, status, response, original_data, e=''):
        if app.sanitize:
            result = original_data.copy()
            redirect_urls = response.url
            new_url = (original_data['New URL'] if original_data['New URL'].startswith('http://') or original_data['New URL'].startswith('https://') 
                       else (app.base_url + original_data['New URL'] if original_data['New URL'] != '/' else app.base_url))
            if redirect_urls != new_url:
                result.update({'from': url, 'to': new_url, 'final': redirect_urls})
        else:
            result = {'url': url, 'status': status, 'error': f"{e}"}
        return result