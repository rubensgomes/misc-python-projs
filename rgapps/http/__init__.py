"""rgapps.http subpackage

This package contains code that is dependent upon HTTP.  Things
like routes, HTTP exception handlers, REST resources.

Modules:
-------
errors: a module to place error handlers
routes: a module to define the HTTP routes
wsgi: a module that implements the Apache WSGI code.

Sub-Packages:
------------
resources: a sub-package where REST Resources are defined
"""
from functools import wraps
import logging

from flask.globals import request
from werkzeug.exceptions import Unauthorized

from rgapps.config import ini_config


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["errors", "routes", "wsgi", "http_basic_authenticate"]

def __basicAuthentication():
    """This is a private helper method used by the http_basic_authenticate.
    """
    auth = request.authorization
    logging.debug("Authenticating HTTP Basic Authentication "
                  "using Authorization [{0}]"
                  .format(auth))

    valid_username = ini_config.get("Sensor", "SENSOR_REST_API_USERNAME")
    valid_password = ini_config.get("Sensor", "SENSOR_REST_API_PASSWORD")

    if not auth:
        logging.debug("HTTP Basic Authentication header not found.")
        return False
    elif (auth.username != valid_username):
        logging.debug("user [{0}] is not valid. Authentication failed"
                       .format(auth.username))
        return False
    elif (auth.password != valid_password):
        logging.debug("Password not valid. user [{0}] failed authentication."
                       .format(auth.username))
        return False


    logging.debug("user [{0}] has been authenticated."
                   .format(auth.username))
    return True


def http_basic_authenticate(func):
    """ This is a decorator function used to replace the flask-restful
    method-decorator property inside flask-restful Resource classes.
    It authenticates the user using the HTTP Basic Authentication protocol.

    Parameters:
    ----------
    func: python function
        The function being decorated.

    Returns:
    -------
    The decorator function used in the method_decorators declared inside
    the flask-restful Resources classes.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        authenticated = __basicAuthentication()

        if authenticated:
            return func(*args, **kwargs)

        logging.info("Aborting request with 401 status code.")
        resource_url = request.base_url
        raise Unauthorized(
            "The REST resource [{0}] requires a valid username/passsord."
            .format(resource_url))

    return wrapper

if __name__ == '__main__':
    pass
