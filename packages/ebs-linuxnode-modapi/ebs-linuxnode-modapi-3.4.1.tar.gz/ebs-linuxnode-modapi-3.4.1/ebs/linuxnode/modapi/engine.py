
import os
from copy import copy
from twisted import logger
from twisted.internet.defer import succeed
from twisted.internet.task import LoopingCall

from ebs.linuxnode.core.http import HTTPError
from .primitives import ApiPersistentActionQueue


class ServerReportsNotReady(Exception):
    def __init__(self, msg, data=None):
        self.msg = msg
        self.data = data or {}


class ConnectionRequirementsNotReady(Exception):
    def __init__(self, msg, data=None):
        self.msg = msg
        self.data = data or {}


class PrimaryAuthenticationFailure(Exception):
    pass


class TokenAuthenticationFailure(Exception):
    pass


class ModularApiEngineBase(object):
    _prefix = ""
    _api_probe = None
    _api_announce = None
    _api_tasks = []
    _api_reconnect_frequency = 30

    def __init__(self, actual, config=None):
        self._log = None
        self._config = config
        self._actual = actual
        self._api_reconnect_task = None
        self._api_engine_active = False
        self._api_endpoint_connected = None
        self._api_queue = ApiPersistentActionQueue(self)

    @property
    def name(self):
        return self._prefix

    """ Proxy to Core Engine """

    @property
    def cache_dir(self):
        return os.path.join(self._actual.cache_dir, self._prefix)

    @property
    def log(self):
        if not self._log:
            self._log = logger.Logger(namespace="modapi.{0}".format(self._prefix), source=self)
        return self._log

    @property
    def config(self):
        if self._config:
            return self._config
        else:
            return self._actual.config

    """ API Connection Status Primitives """
    @property
    def api_endpoint_connected(self):
        return self._api_endpoint_connected

    @api_endpoint_connected.setter
    def api_endpoint_connected(self, value):
        self._actual.modapi_signal_api_connected(value, self._prefix)
        self._api_endpoint_connected = value

    """ API Task Management """
    @property
    def api_tasks(self):
        return self._api_tasks

    def install_task(self, task, period):
        self._api_tasks.append((task, period))

    def _api_start_all_tasks(self, _):
        for task, period in self.api_tasks:
            t = getattr(self, task)
            if not t.running:
                self.log.info("Starting {task} with period {period}",
                              task=task, period=period)
                t.start(period)
        return succeed(True)

    def _api_stop_all_tasks(self, _):
        for task, _ in self._api_tasks:
            t = getattr(self, task)
            if t.running:
                self.log.info("Stopping {task}", task=task)
                t.stop()
        return succeed(True)

    """ API Connection Management """
    @property
    def api_reconnect_task(self):
        if self._api_reconnect_task is None:
            self._api_reconnect_task = LoopingCall(self.api_engine_activate)
        return self._api_reconnect_task

    def api_engine_activate(self):
        self.log.debug("Attempting to activate {0} API engine.".format(self._prefix))

        def _enter_reconnection_cycle(failure):
            self.log.error("Can't connect to {0} API endpoint".format(self._prefix))

            # TODO Should this be a HTTP API Engine check function or is here fine?
            if failure.check(ServerReportsNotReady):
                self._actual.modapi_signal_api_server_not_ready(failure.value, self._prefix)
            elif failure.check(ConnectionRequirementsNotReady):
                self._actual.modapi_signal_api_params_not_ready(failure.value, self._prefix)
                pass
            else:
                self.log.failure("Connection Failure : ", failure=failure)

            self.api_endpoint_connected = False
            if not self.api_reconnect_task.running:
                self.api_engine_reconnect()
            return failure

        if self._api_announce:
            d = getattr(self, self._api_announce)()
            d.addErrback(_enter_reconnection_cycle)
        else:
            d = succeed(True)

        d.addCallback(getattr(self, self._api_probe))

        def _made_connection(_):
            self.log.debug("Made connection")
            self.api_endpoint_connected = True
            self._api_engine_active = True
            if self.api_reconnect_task.running:
                self.api_reconnect_task.stop()
            self.log.info("Triggering process of {0} API persistent queue".format(self._prefix))
            self._api_queue.process()
            return

        d.addCallbacks(
            _made_connection,
            _enter_reconnection_cycle
        )

        def _error_handler(failure):
            if self.api_reconnect_task.running:
                return
            else:
                return failure

        d.addCallbacks(
            self._api_start_all_tasks,
            _error_handler
        )
        return d

    def api_engine_reconnect(self):
        if self._api_engine_active:
            self.api_endpoint_connected = False
            self.log.info("Lost connection to {0} API server. Attempting to reconnect."
                          "".format(self._prefix))
        self._api_engine_active = False
        if not self.api_reconnect_task.running:
            self._api_stop_all_tasks(True)
            self.api_reconnect_task.start(self._api_reconnect_frequency)

    def api_engine_stop(self):
        self._api_engine_active = False
        for task, _ in self._api_tasks:
            if getattr(self, task).running:
                getattr(self, task).stop()
        if self.api_reconnect_task.running:
            self.api_reconnect_task.stop()

    @property
    def api_engine_active(self):
        return self._api_engine_active

    def start(self):
        self.api_engine_activate()

    def stop(self):
        self.api_engine_stop()


class ModularHttpApiEngine(ModularApiEngineBase):
    _api_baseurl = ''
    _api_headers = {}

    _auth_url = ''
    _auth_headers = {}

    def __init__(self, actual, config=None):
        super(ModularHttpApiEngine, self).__init__(actual, config)
        self._api_token = None
        self._internet_connected = False
        self._internet_link = None

    """ Proxy to Core Engine """
    @property
    def http_get(self):
        return self._actual.http_get

    @property
    def http_post(self):
        return self._actual.http_post

    @property
    def network_info(self):
        return self._actual.network_info

    """ Network Status Primitives """

    # TODO Consider moving the core network status primitives
    #  entirely into the manager instead

    @property
    def internet_connected(self):
        return self._internet_connected

    @internet_connected.setter
    def internet_connected(self, value):
        self._actual.modapi_signal_internet_connected(value, self._prefix)
        self._internet_connected = value

    @property
    def internet_link(self):
        return self._internet_link

    @internet_link.setter
    def internet_link(self, value):
        self._actual.modapi_signal_internet_link(value, self._prefix)
        self._internet_link = value

    """ API Engine Management """
    def api_engine_activate(self):
        # Probe for internet
        d = self.http_get('https://www.google.com')

        def _get_internet_info(maybe_failure):
            ld = self.network_info

            def _set_internet_link(l):
                if l:
                    if isinstance(l, str):
                        self.internet_link = l
                    else:
                        self.internet_link = l.decode('utf-8')
            ld.addCallback(_set_internet_link)
            return maybe_failure
        d.addBoth(_get_internet_info)

        def _made_connection(_):
            self.log.debug("Have Internet Connection")
            self.internet_connected = True

        def _enter_reconnection_cycle(failure):
            self.log.error("No Internet!")
            self.internet_connected = False
            if not self.api_reconnect_task.running:
                self.api_engine_reconnect()
            return failure

        d.addCallbacks(
            _made_connection,
            _enter_reconnection_cycle
        )

        def _error_handler(failure):
            if self.api_reconnect_task.running:
                return
            else:
                return failure

        d.addCallbacks(
            lambda _: ModularApiEngineBase.api_engine_activate(self),
            _error_handler
        )
        return d

    @property
    def api_token(self):
        raise NotImplementedError

    def api_token_reset(self):
        raise NotImplementedError

    def _strip_auth(self, headers):
        if b'Authorization' in headers.keys():
            rv = copy(headers)
            rv[b'Authorization'] = rv[b'Authorization'][:10] + b'...'
            return rv
        return headers

    """ Core HTTP API Executor """
    def _api_execute(self, ep, request_builder, response_handler):
        url = "{0}/{1}".format(self.api_url, ep)

        d = request_builder()

        def _get_response(req: dict):
            language = req.pop('_language', 'JSON')
            language = language.upper()
            method = req.pop('_method', 'POST')
            method = method.upper()
            headers = copy(self._api_headers)
            bearer_token = req.pop('_token', None)
            if bearer_token:
                headers[b'Authorization'] = b'Bearer ' + bearer_token.encode('ascii')
            self.log.debug("Executing {language} API {method} Request to {url} \n"
                           "   with content '{content}'\n"
                           "   and headers '{headers}'", 
                           url=url, content=req, headers=self._strip_auth(headers),
                           method=method, language=language)
            params = req.pop('_query', [])
            request_structure = {
                'json': req,
                'params': params,
            }
            request_structure = {k: v for k, v in request_structure.items() if v}
            if method == 'POST':
                r = self.http_post(url, timeout=120, headers=headers,
                                   **request_structure)
            elif method == 'GET':
                r = self.http_get(url, timeout=120, headers=headers,
                                  **request_structure)
            else:
                raise ValueError("Method {} not recognized".format(method))
            if language == 'JSON':
                r.addCallbacks(
                    self._parse_json_response
                )
            return r
        d.addCallback(_get_response)

        def _error_handler(failure):
            self.log.failure("Attempting to handle API Error for API request to "
                             "endpoint '{endpoint}'", failure=failure, endpoint=ep)
            if isinstance(failure.value, HTTPError) and \
                    failure.value.response.code in [401, 403]:
                self.log.info(f"Encountered {failure.value.response.code} Error. "
                              f"Attempting API Token Reset.")
                self.api_token_reset()
            if not self.api_reconnect_task.running:
                self.log.debug("Starting API Reconnect Task")
                self.api_engine_reconnect()
            return failure
        d.addCallbacks(response_handler, _error_handler)
        return d

    @property
    def api_url(self):
        if self._api_baseurl.startswith('config'):
            cft = self._api_baseurl.split(':')[1]
            return getattr(self.config, cft)
        return self._api_baseurl

    @property
    def auth_url(self):
        if self._auth_url.startswith('config'):
            cft = self._auth_url.split(':')[1]
            return getattr(self.config, cft)
        return self._auth_url

    def start(self):
        super(ModularHttpApiEngine, self).start()

    def stop(self):
        super(ModularHttpApiEngine, self).stop()

    # API Language Support Infrastructure

    # JSON
    def _parse_json_response(self, response):
        self.log.debug("Attempting to extract JSON from response {r}", r=response)
        return response.json()
