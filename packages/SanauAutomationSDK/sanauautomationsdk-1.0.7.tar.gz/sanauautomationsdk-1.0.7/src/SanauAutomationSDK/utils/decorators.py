import json
import time
import requests


def catch(retries=10, delay=10):
    def decorator(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            headers = kwargs.get('headers', {})
            kwargs['headers'] = {**{'Access-Key': self.access_key}, **headers}

            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (requests.ConnectionError, requests.Timeout, json.JSONDecodeError) as e:
                    if attempt >= retries-1:
                        if isinstance(e, json.JSONDecodeError):
                            raise json.JSONDecodeError('JSONDecoderError! The server may be down', e.doc, e.pos) from None
                        raise e from None
                    time.sleep(delay)
                except Exception as e:
                    raise e from None

        return wrapper

    return decorator
