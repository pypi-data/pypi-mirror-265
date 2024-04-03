# standard imports
import logging
import time

# external imports
from chainlib.eth.unittest.ethtester import EthTesterCase
from chainlib.connection import RPCConnection
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt
from chainlib.eth.address import to_checksum_address

# local imports
from giftable_erc20_token import GiftableToken

logg = logging.getLogger(__name__)


class TestGiftableToken(EthTesterCase):

    expire = 0

    def setUp(self):
        super(TestGiftableToken, self).setUp()
        self.conn = RPCConnection.connect(self.chain_spec, 'default')
       
        address = self.publish_giftable_token('Foo Token', 'FOO', 16, expire=self.expire)
        self.address = to_checksum_address(address)
        nonce_oracle = RPCNonceOracle(self.accounts[0], conn=self.conn)
        c = GiftableToken(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        self.initial_supply = 1 << 40
        (tx_hash, o) = c.mint_to(self.address, self.accounts[0], self.accounts[0], self.initial_supply)
        r = self.conn.do(o)
        o = receipt(tx_hash)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)


    def publish_giftable_token(self, name, symbol, decimals=16, expire=None):
        nonce_oracle = RPCNonceOracle(self.accounts[0], conn=self.conn)
        c = GiftableToken(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        self.symbol = name
        self.name = symbol
        self.decimals = decimals
        (tx_hash, o) = c.constructor(self.accounts[0], self.name, self.symbol, self.decimals, expire=expire)
        self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)
        address = r['contract_address'] 
        logg.debug('published on address {} with hash {}'.format(address, tx_hash))
        return address


class TestGiftableExpireToken(TestGiftableToken):

    expire = int(time.time()) + 100000

    def setUp(self):
        super(TestGiftableExpireToken, self).setUp()
