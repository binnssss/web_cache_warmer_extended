import app

class SanitizeModule:

    def result_sanitizer(url, status, e, response, original_data):
        if app.sanitize:
            result = original_data.copy()
            redirect_urls = response.url
            if redirect_urls != url:
                result.update({'from': url, 'to': redirect_urls})
        else:
            result = {'url': url, 'status': status, 'error': f"{e}"}
        return result