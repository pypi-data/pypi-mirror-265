"""Ithaca SDK."""
import requests
import logging

from eth_account import Account

from .analytics import Analytics
from .auth import Auth
from .calculation import Calculation
from .client import Client
from .constants import ENVS
from .fundlock import Fundlock
from .market import Market
from .orders import Orders  # type: ignore  # noqa: F401
from .protocol import Protocol
from .socket import Socket


class IthacaSDK:
    """
    Ithaca SDK Class

    Properties:
        auth (Auth): Authentication
        protocol (Protocol): Protocol
        market (Market): Market
        client (Client): Client
        orders (Orders): Orders
        calculation (Calculation): Calculation
        socket (Socket): Socket
        fundlock (Fundlock): Fundlock
        analytics (Analytics): Analytics
    """

    def __init__(
            self, 
            private_key, 
            api_endpoint,
            ws_endpoint,
            graphql_endpoint,
            rpc_endpoint,
            env_name="CANARY"):
        """
        Ithaca SDK Constructor. By default, one should specify a private_key for on-chain and backend authentication followed by the environment one wishes to access.
        
        Args:
          private_key (str): Private Key
          api_endpoint (str): API Endpoint
          ws_endpoint (str): Websocket Endpoint
          graphql_endpoint (str): Graphql Endpoint
          rpc_endpoint (str): RPC Endpoint
          env_name (str): (Depreciated) Environment Name
        """
        if api_endpoint, ws_endpoint, graphql_endpoint, rpc_endpoint not None:
          logging.warning("Endpoint specifications not found, defaulting to 'env_name: {0}".format(env_name))
          self.env = ENVS.get(env_name)
        else:
          self.env = {
            "base_url": api_endpoint,
            "ws_url": ws_endpoint,
            "subgraph": graphql_endpoint,
            "rpc_url": rpc_endpoint
          }
        self.account = Account.from_key(private_key)
        self.session = requests.Session()
        self.base_url = self.env.get("base_url")
        self.subgraph_url = self.env.get("subgraph")
        self.ws_url = self.env.get("ws_url")
        self.rpc_url = self.env.get("rpc_url")

        self.auth = Auth(self)
        self.protocol = Protocol(self)
        self.market = Market(self)
        self.client = Client(self)
        self.orders = Orders(self)
        self.calculation = Calculation(self)
        self.socket = Socket(self)
        self.fundlock = Fundlock(self)
        self.analytics = Analytics(self)

    def post(self, endpoint, json=None):
        """Make Post Request.

        Args:
            endpoint (_type_): _description_
            json (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        verify = False if "localhost" in self.base_url else True
        res = self.session.post(self.base_url + endpoint, json=json, verify=verify)
        try:
            return res.json()
        except requests.JSONDecodeError:
            return res

    def get(self, endpoint):
        """Make GET request.

        Args:
            endpoint (_type_): _description_

        Returns:
            _type_: _description_
        """
        headers = {"Content type": "application/json"}
        verify = True if self.base_url.startswith("https") else False
        res = self.session.get(self.base_url + endpoint, params=headers, verify=verify)
        return res.json()
