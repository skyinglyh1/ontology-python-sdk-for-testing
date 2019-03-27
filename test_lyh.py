import base64
import unittest

from ontology.utils import util
from ontology.account.account import Account
from ontology.wallet.wallet import WalletData
from ontology.wallet.account import AccountData
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.common.address import Address

private_key = "8b6bb2bebb27f3e2c24cc8a3febb413c1ef98bd2481e2292ada6d90f9a5f5ec9"
if __name__ == '__main__':
    account = Account(private_key)
    publickey = account.serialize_public_key()
    wif = account.export_wif()
    privatekey = account.get_privatekey_from_wif(wif)
    print("public key is ", publickey, type(publickey))
    print("private key is ", privatekey)
    print("...", account.serialize_private_key())
    address = Address(publickey)
    addr = address.b58decode()
    print("address is ", addr)
