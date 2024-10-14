import app
import app.http_request

class SanitizeModule:
    def remove_trailing_slash(url):
        if url.endswith('/'):
            return url.rstrip('/')
        return url

    def result_sanitizer(url, status, response, original_data, e=''):
        if app.sanitize:
            app.locale = app.http_request.HttpClient.get_locale().lower()
            redirect_urls = SanitizeModule.remove_trailing_slash(response.url)
            new_url = SanitizeModule.remove_trailing_slash((original_data[app.reference_column] if original_data[app.reference_column].startswith('http://') or 
                                                            original_data[app.reference_column].startswith('https://') 
                       else (app.base_url + original_data[app.reference_column] if original_data[app.reference_column] != '/' else app.base_url)))
            new_url_localized = SanitizeModule.remove_trailing_slash((original_data[app.reference_column] if original_data[app.reference_column].startswith('http://') or 
                                                                      original_data[app.reference_column].startswith('https://') 
                       else (app.base_url + '/' + app.locale + original_data[app.reference_column] if original_data[app.reference_column] != '/' else app.base_url)))
            if redirect_urls == new_url_localized:
                new_url = new_url_localized
            result = original_data.copy()
            if redirect_urls != new_url:
                result.update({'from': url, 'to': new_url, 'final': redirect_urls})
                return result
        else:
            result = {'url': url, 'status': status, 'error': f"{e}"}
            return result