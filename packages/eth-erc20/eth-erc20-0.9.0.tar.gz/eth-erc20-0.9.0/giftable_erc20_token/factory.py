# standard imports
import os
import logging

# external imports
from chainlib.eth.tx import (
        TxFactory,
        TxFormat,
        )
from chainlib.hash import keccak256_string_to_hex
from chainlib.eth.contract import (
        ABIContractEncoder,
        ABIContractType,
        )
from chainlib.eth.constant import ZERO_ADDRESS
from chainlib.jsonrpc import JSONRPCRequest
from hexathon import add_0x

# local imports
from giftable_erc20_token.data import data_dir
from eth_erc20 import ERC20

logg = logging.getLogger(__name__)


class GiftableToken(ERC20):

    __abi = None
    __bytecode = None

    def constructor(self, sender_address, name, symbol, decimals, expire=0, tx_format=TxFormat.JSONRPC, version=None):
        code = self.cargs(name, symbol, decimals, expire=expire)
        tx = self.template(sender_address, None, use_nonce=True)
        tx = self.set_code(tx, code)
        return self.finalize(tx, tx_format)


    @staticmethod
    def cargs(name, symbol, decimals, expire=0, version=None):
        if expire == None:
            expire = 0
        code = GiftableToken.bytecode(version=version)
        enc = ABIContractEncoder()
        enc.string(name)
        enc.string(symbol)
        enc.uint256(decimals)
        enc.uint256(expire)
        args = enc.get()
        code += args
        logg.debug('constructor code: ' + args)
        return code


    @staticmethod
    def gas(code=None):
        return 2000000


    @staticmethod
    def abi():
        if GiftableToken.__abi == None:
            f = open(os.path.join(data_dir, 'GiftableToken.json'), 'r')
            GiftableToken.__abi = json.load(f)
            f.close()
        return GiftableToken.__abi


    @staticmethod
    def bytecode(version=None):
        if GiftableToken.__bytecode == None:
            f = open(os.path.join(data_dir, 'GiftableToken.bin'))
            GiftableToken.__bytecode = f.read()
            f.close()
        return GiftableToken.__bytecode


    def add_minter(self, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        enc = ABIContractEncoder()
        enc.method('addMinter')
        enc.typ(ABIContractType.ADDRESS)
        enc.address(address)
        data = enc.get()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format)
        return tx


    def remove_minter(self, contract_address, sender_address, address, tx_format=TxFormat.JSONRPC):
        enc = ABIContractEncoder()
        enc.method('removeMinter')
        enc.typ(ABIContractType.ADDRESS)
        enc.address(address)
        data = enc.get()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format)
        return tx


    def mint_to(self, contract_address, sender_address, address, value, tx_format=TxFormat.JSONRPC):
        enc = ABIContractEncoder()
        enc.method('mintTo')
        enc.typ(ABIContractType.ADDRESS)
        enc.typ(ABIContractType.UINT256)
        enc.address(address)
        enc.uint256(value)
        data = enc.get()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format)
        return tx


    def burn(self, contract_address, sender_address, value, tx_format=TxFormat.JSONRPC):
        enc = ABIContractEncoder()
        enc.method('burn')
        enc.typ(ABIContractType.UINT256)
        enc.uint256(value)
        data = enc.get()
        tx = self.template(sender_address, contract_address, use_nonce=True)
        tx = self.set_code(tx, data)
        tx = self.finalize(tx, tx_format)
        return tx


    def burned(self, contract_address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('totalBurned')
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o['params'].append('latest')
        o = j.finalize(o)
        return o


    def total_minted(self, contract_address, sender_address=ZERO_ADDRESS, id_generator=None):
        j = JSONRPCRequest(id_generator)
        o = j.template()
        o['method'] = 'eth_call'
        enc = ABIContractEncoder()
        enc.method('totalMinted')
        data = add_0x(enc.get())
        tx = self.template(sender_address, contract_address)
        tx = self.set_code(tx, data)
        o['params'].append(self.normalize(tx))
        o['params'].append('latest')
        o = j.finalize(o)
        return o


def bytecode(**kwargs):
    return GiftableToken.bytecode(version=kwargs.get('version'))


def create(**kwargs):
    return GiftableToken.cargs(kwargs['name'], kwargs['symbol'], kwargs['decimals'], expire=kwargs.get('expire'), version=kwargs.get('version'))


def args(v):
    if v == 'create':
        return (['name', 'symbol', 'decimals'], ['expire', 'version'],)
    elif v == 'default' or v == 'bytecode':
        return ([], ['version'],)
    raise ValueError('unknown command: ' + v)
