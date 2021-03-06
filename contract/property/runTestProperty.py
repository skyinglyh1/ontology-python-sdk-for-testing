import binascii
from binascii import b2a_hex, a2b_hex
import csv
import json
import os
import sys, getopt
from time import time
import time
import xlrd
from collections import namedtuple
import time
import unittest
from ontology.smart_contract.native_contract.asset import Asset
from ontology.account.account import Account
from ontology.common.address import Address
from ontology.core.transaction import Transaction
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.smart_contract.neo_vm import NeoVm
import requests
import re
import random
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction
from multiprocess import *
from ontology.crypto.digest import Digest
from ontology.utils.util import bigint_to_neo_bytes

# rpc_address = "http://127.0.0.1:20336"
rpc_address = "http://polaris1.ont.io:20336"
# rpc_address = "http://139.219.139.170:20336"
# rpc_address = "http://dappnode1.ont.io:20336"
sdk = OntologySdk()
sdk.set_rpc((rpc_address))
from datetime import datetime

ContractAddress = "1b51b2693c6da3ac61c6287cd0bfabe9af9f4f39"

contract_address_str = ContractAddress
contract_address_bytearray = bytearray.fromhex(contract_address_str)
contract_address = contract_address_bytearray
contract_address.reverse()

wallet_path = "C:\\Go_WorkSpace\\src\\github.com\\ontio\\ontology\\_Wallet_\\wallet.dat"
# wallet_path1 = "D:\\SmartX_accounts\\Cyano Wallet\\lucknumberAccount\\wallet1.dat"
# wallet_path10000 = "C:\\Go_WorkSpace\\src\\github.com\\ontio\\ontology\\_Wallet_\\wallet10000.dat"

sdk.wallet_manager.open_wallet(wallet_path)


admin_addr = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
admin_pwd = "password"
pwd = admin_pwd
adminAcct = sdk.wallet_manager.get_account(admin_addr, admin_pwd)

admin_addr1 = "ASUwFccvYFrrWR6vsZhhNszLFNvCLA5qS6"
admin_pwd1 = "password"
pwd1 = admin_pwd
adminAcct1 = sdk.wallet_manager.get_account(admin_addr1, admin_pwd1)

class TestAsset(unittest.TestCase):

    def test_check_hash(self):
        hash = "e94e67dea2f20ec5c9243a9e050ad3ffcb4166378c4df8a0c33a3c0f56a6654e"
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        print("Check-res is ", res)
        return True

    # def test_Deploy(self):
    #     payerAcct = adminAcct
    #     param_list = []
    #     param_list.append("DeployTEEContract".encode())
    #     param_list1 = []
    #     param_list1.append(payerAcct.get_address().to_array())
    #     param_list1.append(bytearray.fromhex("01"))
    #     avmCode = "013cc56b6a00527ac46a51527ac4681953797374656d2e53746f726167652e476574436f6e746578746a52527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a53527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a54527ac41400000000000000000000000000000000000000026a55527ac4084d455441444154416a56527ac40d434f4e54524143545f434f44456a57527ac40e434f4e54524143545f41444d494e6a58527ac4006a59527ac4516a5a527ac4526a5b527ac4536a5c527ac46a00c30e5265676973746572576f726b65727d9c7c75645e006a51c300c36a5d527ac46a51c351c36a5e527ac46a51c352c36a5f527ac46a51c353c36a60527ac46a51c354c36a0111527ac46a51c355c36a0112527ac46a0112c36a0111c36a60c36a5fc36a5ec36a5dc365bd056c75666203006a00c30c557064617465576f726b65727d9c7c75645e006a51c300c36a5d527ac46a51c351c36a5e527ac46a51c352c36a5f527ac46a51c353c36a60527ac46a51c354c36a0111527ac46a51c355c36a0113527ac46a0113c36a0111c36a60c36a5fc36a5ec36a5dc3653c086c75666203006a00c309476574576f726b65727d9c7c756419006a51c300c36a5d527ac46a5dc365e40a6c75666203006a00c3114465706c6f79544545436f6e74726163747d9c7c756439006a51c300c36a0114527ac46a51c351c36a0115527ac46a51c352c36a0116527ac46a0116c36a0115c36a0114c365bc0b6c75666203006a00c30e476574544545436f6e74726163747d9c7c75641b006a51c300c36a0117527ac46a0117c3657b0d6c75666203006a00c30a4372656174655461736b7d9c7c756475006a51c300c36a0118527ac46a51c351c36a0119527ac46a51c352c36a0117527ac46a51c353c36a011a527ac46a51c354c36a011b527ac46a51c355c36a011c527ac46a51c356c36a011d527ac46a011dc36a011cc36a011bc36a011ac36a0117c36a0119c36a0118c3658d0e6c75666203006a00c30953746172745461736b7d9c7c75641b006a51c300c36a0118527ac46a0118c36522126c75666203006a00c30a46696e6973685461736b7d9c7c756475006a51c300c36a0118527ac46a51c351c36a011e527ac46a51c352c36a011a527ac46a51c353c36a011f527ac46a51c354c36a0120527ac46a51c355c36a0121527ac46a51c356c36a0122527ac46a0122c36a0121c36a0120c36a011fc36a011ac36a011ec36a0118c36504146c75666203006a00c30c4765745461736b53746174657d9c7c75641b006a51c300c36a0118527ac46a0118c36585186c75666203006a00c30b4765745461736b496e666f7d9c7c75641b006a51c300c36a0118527ac46a0118c365c3196c75666203006a00c3094765744f75747075747d9c7c75642a006a51c300c36a0118527ac46a51c351c36a0123527ac46a0123c36a0118c365b21a6c75666203006c75660116c56b6a00527ac46a51527ac46a51c36a00c3946a52527ac46a52c3c56a53527ac4006a54527ac46a00c36a55527ac46a00c36a51c37d9f7c756433006a54c36a55c3936a56527ac46a56c36a53c36a54c37bc46a54c351936a54527ac46a55c36a54c3936a00527ac462c6ff6a53c36c75660114c56b6a00527ac4014e00806a51527ac46a00c3c0007da07c75f16a00c3a96a52527ac4006a53527ac4011500655eff76c96a54527ac46a54c3c06a55527ac46a53c36a55c39f644b006a54c36a53c3c36a56527ac46a53c351936a53527ac46a56c3517d9f7c756409006227006203006a51c36a52c36a56c36a56c351947b6b766b946c6c52727f7e6a51527ac462b1ff6a51c36c7566011cc56b6a00527ac46a51527ac46a00c3c06a52527ac46a51c3647c00c77601307c007bc47601317c517bc47601327c527bc47601337c537bc47601347c547bc47601357c557bc47601367c567bc47601377c577bc47601387c587bc47601397c597bc47601417c5a7bc47601427c5b7bc47601437c5c7bc47601447c5d7bc47601457c5e7bc47601467c5f7bc46a53527ac4627900c77601307c007bc47601317c517bc47601327c527bc47601337c537bc47601347c547bc47601357c557bc47601367c567bc47601377c577bc47601387c587bc47601397c597bc47601617c5a7bc47601627c5b7bc47601637c5c7bc47601647c5d7bc47601657c5e7bc47601667c5f7bc46a53527ac4006a54527ac4006a55527ac46a52c30065d7fd6a56527ac46a56c3c06a57527ac46a55c36a57c39f6479006a56c36a55c3c36a58527ac46a55c351936a55527ac46a00c36a58c351936a58c37b6b766b946c6c52727f6a59527ac46a59c301007e6a59527ac46a59c302f0008454996a5a527ac46a54c36a53c36a5ac3c37e6a54527ac46a59c35f846a5a527ac46a54c36a53c36a5ac3c37e6a54527ac46283ff6a54c36c75660114c56b6a00527ac46a51527ac46a52527ac46a53527ac46a54527ac46a55527ac4681953797374656d2e53746f726167652e476574436f6e746578746a56527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a57527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a58527ac41400000000000000000000000000000000000000026a59527ac4084d455441444154416a5a527ac40d434f4e54524143545f434f44456a5b527ac40e434f4e54524143545f41444d494e6a5c527ac4006a5d527ac4516a5e527ac4526a5f527ac4536a60527ac412696e76616c696420697020616464726573736a51c3007d9e7c756553187512696e76616c6964207075626c6963206b65796a52c3007d9e7c756534187511696e76616c69642066656520726174696f6a54c3007da07c756516187511696e76616c6964206761732070726963656a53c3007da07c7565f81775096e6f74206f776e65726a58c3681b53797374656d2e52756e74696d652e436865636b5769746e65737365ca177516696e76616c696420776f726b657220616464726573736a55c3655c1e65a917756a00c36a56c3681253797374656d2e53746f726167652e476574642f006a00c30665786973742e52c176c9681553797374656d2e52756e74696d652e4e6f74696679006c7566620300c7766a51c37c0269707bc4766a52c37c067075624b65797bc4766a53c37c0867617350726963657bc4766a54c37c08666565526174696f7bc4766a55c37c07616464726573737bc46a0111527ac46a0111c3681853797374656d2e52756e74696d652e53657269616c697a656a00c36a56c3681253797374656d2e53746f726167652e50757406776f726b65720872656769737465726a00c353c176c9681553797374656d2e52756e74696d652e4e6f74696679516c7566011ac56b6a00527ac46a51527ac46a52527ac46a53527ac46a54527ac46a55527ac4681953797374656d2e53746f726167652e476574436f6e746578746a56527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a57527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a58527ac41400000000000000000000000000000000000000026a59527ac4084d455441444154416a5a527ac40d434f4e54524143545f434f44456a5b527ac40e434f4e54524143545f41444d494e6a5c527ac4006a5d527ac4516a5e527ac4526a5f527ac4536a60527ac4096e6f74206f776e65726a58c3681b53797374656d2e52756e74696d652e436865636b5769746e657373655315756a00c36a56c3681253797374656d2e53746f726167652e4765746a0111527ac46a0111c3916433006a00c30a6e6f742065786973742e52c176c9681553797374656d2e52756e74696d652e4e6f74696679006c75666203006a0111c3681a53797374656d2e52756e74696d652e446573657269616c697a656a0112527ac46a51c3007d9e7c756412006a51c36a0112c30269707bc46203006a52c3007d9e7c756416006a52c36a0112c3067075624b65797bc46203006a53c3007d9e7c756418006a53c36a0112c30867617350726963657bc46203006a54c3007d9e7c756418006a54c36a0112c308666565526174696f7bc46203006a55c3007d9e7c756417006a55c36a0112c307616464726573737bc46203006a0112c3681853797374656d2e52756e74696d652e53657269616c697a656a00c36a56c3681253797374656d2e53746f726167652e50757406776f726b6572067570646174656a00c353c176c9681553797374656d2e52756e74696d652e4e6f74696679516c75665dc56b6a00527ac4681953797374656d2e53746f726167652e476574436f6e746578746a51527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a52527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a53527ac41400000000000000000000000000000000000000026a54527ac4084d455441444154416a55527ac40d434f4e54524143545f434f44456a56527ac40e434f4e54524143545f41444d494e6a57527ac4006a58527ac4516a59527ac4526a5a527ac4536a5b527ac46a00c36a51c3681253797374656d2e53746f726167652e4765746c756660c56b6a00527ac46a51527ac46a52527ac4681953797374656d2e53746f726167652e476574436f6e746578746a53527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a54527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a55527ac41400000000000000000000000000000000000000026a56527ac4084d455441444154416a57527ac40d434f4e54524143545f434f44456a58527ac40e434f4e54524143545f41444d494e6a59527ac4006a5a527ac4516a5b527ac4526a5c527ac4536a5d527ac46a52c365adf56a5e527ac40c696e76616c696420636f64656a5ec3652618657311756a51c36a57c36a5ec3658a126a53c3681253797374656d2e53746f726167652e5075746a52c36a58c36a5ec36567126a53c3681253797374656d2e53746f726167652e5075746a00c36a59c36a5ec36544126a53c3681253797374656d2e53746f726167652e507574114465706c6f79544545436f6e74726163746a5ec352c176c9681553797374656d2e52756e74696d652e4e6f746966796a5ec3681553797374656d2e52756e74696d652e4e6f74696679516c756660c56b6a00527ac4681953797374656d2e53746f726167652e476574436f6e746578746a51527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a52527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a53527ac41400000000000000000000000000000000000000026a54527ac4084d455441444154416a55527ac40d434f4e54524143545f434f44456a56527ac40e434f4e54524143545f41444d494e6a57527ac4006a58527ac4516a59527ac4526a5a527ac4536a5b527ac46a56c36a00c365c9106a51c3681253797374656d2e53746f726167652e4765746a5c527ac46a55c36a00c365a4106a51c3681253797374656d2e53746f726167652e4765746a5d527ac4c7766a5dc37c086d657461446174617bc4766a5cc37c04636f64657bc46a5e527ac46a5ec3681853797374656d2e52756e74696d652e53657269616c697a656c75660119c56b6a00527ac46a51527ac46a52527ac46a53527ac46a54527ac46a55527ac46a56527ac4681953797374656d2e53746f726167652e476574436f6e746578746a57527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a58527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a59527ac41400000000000000000000000000000000000000026a5a527ac4084d455441444154416a5b527ac40d434f4e54524143545f434f44456a5c527ac40e434f4e54524143545f41444d494e6a5d527ac4006a5e527ac4516a5f527ac4526a60527ac4536a0111527ac414696e76616c6964207072657061696420666565206a54c3007da07c7565d50d7510696e76616c69642070726f76696465726a55c3c0007da07c7565b70d7515696e76616c696420636f6e747261637420686173686a52c3c001147d9c7c7565930d7512696e76616c696420706172616d20686173686a53c3c0007da07c7565730d75096e6f74206f776e65726a51c3681b53797374656d2e52756e74696d652e436865636b5769746e65737365450d756a00c36a57c3681253797374656d2e53746f726167652e476574640a00006c75666203006a56c36548f96a0112527ac46a0112c3916433006a56c30a6e6f742065787369742e52c176c9681553797374656d2e52756e74696d652e4e6f74696679006c7566620300137472616e73666572206f6e67206661696c65646a54c36a58c36a51c365b21165b90c756a0112c3086761735072696365c36a0113527ac46a0112c308666565526174696fc36a0114527ac4c7766a00c37c067461736b49647bc4766a51c37c0763726561746f727bc4766a52c37c0c636f6e7472616374486173687bc4766a53c37c06706172616d737bc4766a54c37c0a707265706169644665657bc4766a55c37c0c6461746150726f76696465727bc4766a56c37c08776f726b657249647bc4766a0113c37c0867617350726963657bc4766a0114c37c08666565526174696f7bc4766a54c37c0a707265706169644665657bc47607637265617465647c067374617475737bc46a0115527ac46a0115c3681853797374656d2e52756e74696d652e53657269616c697a656a00c36a57c3681253797374656d2e53746f726167652e507574047461736b066372656174656a00c36a51c36a56c355c176c9681553797374656d2e52756e74696d652e4e6f74696679516c75660116c56b6a00527ac4681953797374656d2e53746f726167652e476574436f6e746578746a51527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a52527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a53527ac41400000000000000000000000000000000000000026a54527ac4084d455441444154416a55527ac40d434f4e54524143545f434f44456a56527ac40e434f4e54524143545f41444d494e6a57527ac4006a58527ac4516a59527ac4526a5a527ac4536a5b527ac46a00c36a51c3681253797374656d2e53746f726167652e4765746a5c527ac46a5cc391640a00006c75666203006a5cc3681a53797374656d2e52756e74696d652e446573657269616c697a656a5d527ac46a5dc308776f726b65724964c36a5e527ac46a5ec36518f66a5f527ac46a5fc391640a00006c75666203006a5fc30761646472657373c36a60527ac40a6e6f7420776f726b65726a60c3681b53797374656d2e52756e74696d652e436865636b5769746e6573736598097507737461727465646a5dc3067374617475737bc4681653797374656d2e52756e74696d652e47657454696d656a5dc309737461727454696d657bc46a5dc3681853797374656d2e52756e74696d652e53657269616c697a656a00c36a51c3681253797374656d2e53746f726167652e507574047461736b0573746172746a00c353c176c9681553797374656d2e52756e74696d652e4e6f74696679516c7566012ec56b6a00527ac46a51527ac46a52527ac46a53527ac46a54527ac46a55527ac46a56527ac4681953797374656d2e53746f726167652e476574436f6e746578746a57527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a58527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a59527ac41400000000000000000000000000000000000000026a5a527ac4084d455441444154416a5b527ac40d434f4e54524143545f434f44456a5c527ac40e434f4e54524143545f41444d494e6a5d527ac4006a5e527ac4516a5f527ac4526a60527ac4536a0111527ac46a00c36a57c3681253797374656d2e53746f726167652e4765746a0112527ac46a0112c391640a00006c75666203006a0112c3681a53797374656d2e52756e74696d652e446573657269616c697a656a0113527ac46a0113c308776f726b65724964c36a0114527ac46a0114c36589f36a0115527ac46a0115c391640a00006c75666203000a6e6f7420776f726b65726a0115c30761646472657373c3681b53797374656d2e52756e74696d652e436865636b5769746e657373650e07756a0113c306706172616d73c36a0116527ac412696e76616c696420706172616d20686173686a0116c36a52c37d9c7c7565da06756a0113c30c6461746150726f7669646572c365990e6a0117527ac46a53c3681a53797374656d2e52756e74696d652e446573657269616c697a656a0118527ac46a0117c3c06a0119527ac46a0119c36a53c3c07d9e7c75640a00006c7566620300006a011a527ac46a0119c3006514ea6a011b527ac46a011bc3c06a011c527ac46a011ac36a011cc39f6451006a011bc36a011ac3c36a011d527ac46a011ac351936a011a527ac411696e76616c6964206461746120686173686a0117c36a011dc3c36a5fc3c36a0118c36a011dc3c37d9c7c756502067562a9ff6a55c3681a53797374656d2e52756e74696d652e446573657269616c697a656a011e527ac46a011ec391640a00006c75666203006a0113c3086761735072696365c36a011ec300c3956a011f527ac46a0113c308776f726b65724964c365ccf16a0115527ac410696e73756666696369656e74206761736a011fc36a0115c30761646472657373c36a58c365660a656d0575006a0120527ac46a0117c36a0121527ac46a0121c3c06a0122527ac46a0120c36a0122c39f644d006a0121c36a0120c3c36a0123527ac46a0120c351936a0120527ac410696e73756666696369656e74206761736a0123c36a0111c3c36a0123c36a60c3c36a58c365f70965fe047562adff0866696e69736865646a0113c3067374617475737bc46a54c36a0113c30a6f7574707574486173687bc46a55c36a0113c3076f7574707574307bc46a56c36a0113c3076f7574707574317bc46a0113c3681853797374656d2e52756e74696d652e53657269616c697a656a00c36a57c3681253797374656d2e53746f726167652e507574047461736b0666696e6973686a00c353c176c9681553797374656d2e52756e74696d652e4e6f74696679516c756660c56b6a00527ac4681953797374656d2e53746f726167652e476574436f6e746578746a51527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a52527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a53527ac41400000000000000000000000000000000000000026a54527ac4084d455441444154416a55527ac40d434f4e54524143545f434f44456a56527ac40e434f4e54524143545f41444d494e6a57527ac4006a58527ac4516a59527ac4526a5a527ac4536a5b527ac46a00c36a51c3681253797374656d2e53746f726167652e4765746a5c527ac46a5cc391640a00006c75666203006a5cc3681a53797374656d2e52756e74696d652e446573657269616c697a656a5d527ac46a5dc306737461747573c36c75665dc56b6a00527ac4681953797374656d2e53746f726167652e476574436f6e746578746a51527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a52527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a53527ac41400000000000000000000000000000000000000026a54527ac4084d455441444154416a55527ac40d434f4e54524143545f434f44456a56527ac40e434f4e54524143545f41444d494e6a57527ac4006a58527ac4516a59527ac4526a5a527ac4536a5b527ac46a00c36a51c3681253797374656d2e53746f726167652e4765746c75660113c56b6a00527ac46a51527ac4681953797374656d2e53746f726167652e476574436f6e746578746a52527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a53527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a54527ac41400000000000000000000000000000000000000026a55527ac4084d455441444154416a56527ac40d434f4e54524143545f434f44456a57527ac40e434f4e54524143545f41444d494e6a58527ac4006a59527ac4516a5a527ac4526a5b527ac4536a5c527ac46a51c3007d9e7c7576640c00756a51c3517d9e7c75640a00006c75666203006a00c36a52c3681253797374656d2e53746f726167652e4765746a5d527ac46a5dc391640a00006c75666203006a5dc3681a53797374656d2e52756e74696d652e446573657269616c697a656a5e527ac46a51c3007d9c7c756415006a5ec3076f757470757430c36c75666203006a5ec3076f757470757431c36c75665ec56b6a00527ac46a51527ac4681953797374656d2e53746f726167652e476574436f6e746578746a52527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a53527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a54527ac41400000000000000000000000000000000000000026a55527ac4084d455441444154416a56527ac40d434f4e54524143545f434f44456a57527ac40e434f4e54524143545f41444d494e6a58527ac4006a59527ac4516a5a527ac4526a5b527ac4536a5c527ac46a00c391640a006a51c3f0620300516c75665ec56b6a00527ac46a51527ac4681953797374656d2e53746f726167652e476574436f6e746578746a52527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a53527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a54527ac41400000000000000000000000000000000000000026a55527ac4084d455441444154416a56527ac40d434f4e54524143545f434f44456a57527ac40e434f4e54524143545f41444d494e6a58527ac4006a59527ac4516a5a527ac4526a5b527ac4536a5c527ac46a00c3015f7e6a51c37e6c756660c56b6a00527ac46a51527ac4681953797374656d2e53746f726167652e476574436f6e746578746a52527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a53527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a54527ac41400000000000000000000000000000000000000026a55527ac4084d455441444154416a56527ac40d434f4e54524143545f434f44456a57527ac40e434f4e54524143545f41444d494e6a58527ac4006a59527ac4516a5a527ac4526a5b527ac4536a5c527ac46a00c3007d9c7c75640a00006c75666203006a00c36a51c3956a5d527ac4206d756c206f7065726174696f6e206661696c65642c2063202f206120213d20626a5dc36a00c3966a51c37d9c7c75655efc756a5dc36c75665fc56b6a00527ac46a51527ac4681953797374656d2e53746f726167652e476574436f6e746578746a52527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a53527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a54527ac41400000000000000000000000000000000000000026a55527ac4084d455441444154416a56527ac40d434f4e54524143545f434f44456a57527ac40e434f4e54524143545f41444d494e6a58527ac4006a59527ac4516a5a527ac4526a5b527ac4536a5c527ac41944656e6f6d696e61746f722063616e2774206265207a65726f6a51c3007da07c756520fb756a00c36a51c3966a5d527ac46a5dc36c75660112c56b6a00527ac46a51527ac46a52527ac4681953797374656d2e53746f726167652e476574436f6e746578746a53527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a54527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a55527ac41400000000000000000000000000000000000000026a56527ac4084d455441444154416a57527ac40d434f4e54524143545f434f44456a58527ac40e434f4e54524143545f41444d494e6a59527ac4006a5a527ac4516a5b527ac4526a5c527ac4536a5d527ac4096e6f74206f776e65726a00c3681b53797374656d2e52756e74696d652e436865636b5769746e65737365c8f9756a52c36a51c36a00c353c66b6a00527ac46a51527ac46a52527ac46c6a5e527ac46a5ec351c176c9087472616e736665726a56c30068164f6e746f6c6f67792e4e61746976652e496e766f6b656a5f527ac46a5fc376640d00756a5fc301017d9c7c75640a00516c7566620700006c75666c75665ec56b6a00527ac4681953797374656d2e53746f726167652e476574436f6e746578746a51527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a52527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a53527ac41400000000000000000000000000000000000000026a54527ac4084d455441444154416a55527ac40d434f4e54524143545f434f44456a56527ac40e434f4e54524143545f41444d494e6a57527ac4006a58527ac4516a59527ac4526a5a527ac4536a5b527ac46a00c3c001147d9e7c75640a00006c7566620300516c75665ec56b6a00527ac4681953797374656d2e53746f726167652e476574436f6e746578746a51527ac4682d53797374656d2e457865637574696f6e456e67696e652e476574457865637574696e67536372697074486173686a52527ac422415166344d7a7531594a72687a39663361526b6b77536d396e33716858475368347068204f6e746f6c6f67792e52756e74696d652e426173653538546f416464726573736a53527ac41400000000000000000000000000000000000000026a54527ac4084d455441444154416a55527ac40d434f4e54524143545f434f44456a56527ac40e434f4e54524143545f41444d494e6a57527ac4006a58527ac4516a59527ac4526a5a527ac4536a5b527ac46a00c3681a53797374656d2e52756e74696d652e446573657269616c697a656a5c527ac46a5cc36c7566"
    #     param_list1.append(bytearray.fromhex(avmCode))
    #     param_list.append(param_list1)
    #     hash = self.test_invoke(payerAcct, param_list)
    #     print("hash === test", hash)

    # def test_testAddress(self):
    #     payerAcct = adminAcct
    #     param_list = []
    #     param_list.append("testAddress".encode())
    #     param_list1 = []
    #     param_list.append(param_list1)
    #     # print("***** getExplodePoint", param_list)
    #     res = self.test_invokeRead(payerAcct, param_list)
    #     print("res === testAddress", res)
    #     account = Address(binascii.a2b_hex(res))
    #     account = account.b58encode()
    #     print("res === testAddress", account)

    # def test_Test(self):
    #     payerAcct = adminAcct
    #     param_list = []
    #     param_list.append("test".encode())
    #     args = []
    #     param_list1 = []
    #     param_list2 = []
    #     param_list2.append(21)
    #     param_list2.append(22)
    #     param_list1.append(param_list2)
    #     param_list3 = []
    #     param_list3.append(31)
    #     param_list3.append(32)
    #     param_list1.append(param_list3)
    #     args.append(param_list1)
    #     param_list.append(args)
    #     print("***** test", param_list)
    #     params = BuildParams.create_code_params_script(param_list)
    #     hash = self.test_invoke(payerAcct, param_list)
    #     print("hash === test", hash)
    #     return True


    # def test_init(self):
    #     param_list = []
    #     # when pre-execute, don't use 0x67
    #     abi_function = AbiFunction("init", "",param_list)
    #     hash = sdk.neo_vm().send_transaction(contract_address, adminAcct, adminAcct, 200000, 500, abi_function, False)
    #     # res = sdk.rpc.send_raw_transaction(tx)
    #     time.sleep(6)
    #     res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
    #     print("init-res is ", res)
    #     return True
    #
    def test_setGP(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("setGP".encode())

        userBase58Address1 = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
        acct = Address.b58decode(userBase58Address1).to_array()
        # print('acct is ', acct)
        # hash = "616f2a4a38396ff203ea01e6c070ae421bb8ce2d"
        # print("acct1 is ",  bytearray.fromhex(hash))
        # return True


        param_list1 = [124, 100, 100000000000,[[1001, 1], [1002, 1], [1003, 1]]]

        param_list.append(param_list1)
        print("***** setGP", param_list)
        hash = self.test_invoke(payerAcct, param_list)
        print("hash === setGP", hash)
        return True

    def test_multiCreateToken(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("multiCreateToken".encode())
        param_list1 = [[1001, "MyFirstToken", "MFT"], [1002, "MySecondToken", "MST"], [1003, "MyThirdToken", "MTT"], [1004, "MyForthToken", "MFT"]]
        param_list.append(param_list1)

        res = self.test_invoke(payerAcct, param_list)

        print("res === multiCreateToken ===", res)


    def test_multiMintToken(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("multiMintToken".encode())
        userBase58Address1 = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
        toAcct = Address.b58decode(userBase58Address1).to_array()
        param_list1 = [[toAcct, 1001, 5], [toAcct, 1002, 5], [toAcct, 1003, 5]]
        param_list.append(param_list1)
        print("***** multiMintToken", param_list)
        hash = self.test_invoke(payerAcct, param_list)
        print("hash === multiMintToken", hash)
        # time.sleep(6)
        return True

    def test_transferMulti(self):
        payerAcct = adminAcct1
        param_list = []
        param_list.append("transferMulti".encode())
        fromAcct = Address.b58decode("ASUwFccvYFrrWR6vsZhhNszLFNvCLA5qS6").to_array()
        toAcct = Address.b58decode("AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p").to_array()
        param_list1 = [[fromAcct, toAcct, 1001, 1], [fromAcct, toAcct, 1002, 1], [fromAcct, toAcct, 1003, 1]]
        param_list.append(param_list1)
        print("***** transferMulti", param_list)
        hash = self.test_invoke(payerAcct, param_list)
        print("hash === transferMulti", hash)
        # time.sleep(6)
        return True

    def test_multiBurnToken(self):
        payerAcct = adminAcct
        param_list = []
        param_list.append("multiBurnToken".encode())
        account = Address.b58decode("AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p").to_array()
        param_list1 = [[account, 1001, 5], [account, 1002, 1], [account, 1003, 1]]
        param_list.append(param_list1)
        print("***** multiBurnToken", param_list)
        hash = self.test_invoke(payerAcct, param_list)
        print("hash === multiBurnToken", hash)
        # time.sleep(6)
        return True








    def test_transferONG(self, fromAcct, toAcct, ongAmount):

        fromAddr = fromAcct.get_address_base58()
        toAddr = toAcct.get_address_base58()
        asset = "ong"
        ass = Asset(sdk)
        payerAddr = fromAddr
        gaslimit = 20000000
        gasprice = 500
        tx = ass.new_transfer_transaction(asset, fromAddr, toAddr, ongAmount, payerAddr, gaslimit, gasprice)
        sdk.sign_transaction(tx, fromAcct)
        hash = sdk.rpc.send_raw_transaction(tx)



    def test_invoke(self, payerAcct, param_list):
        params = BuildParams.create_code_params_script(param_list)
        #
        # tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 500)
        # sdk.sign_transaction(tx, payerAcct)
        # nil, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        #
        params.append(0x67)
        for i in contract_address:
            params.append(i)
        gaslimit = 20000000
        gaslimit = gaslimit * 2
        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, 500, gaslimit, payerAcct.get_address().to_array(), params, bytearray(), [], bytearray())
        sdk.sign_transaction(tx, payerAcct)
        loopFlag = True
        hash = None
        while loopFlag:
            try:
                hash = sdk.rpc.send_raw_transaction(tx)
            except requests.exceptions.ConnectTimeout or requests.exceptions.ConnectionError:
                loopFlag = True
            if hash != None:
                loopFlag = False
        print("hash is", hash)
        return hash

    def test_invokeRead(self, payerAcct, param_list):
        params = BuildParams.create_code_params_script(param_list)

        tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 500)
        sdk.sign_transaction(tx, payerAcct)
        res, gaslimit = sdk.rpc.send_raw_transaction_pre_exec(tx)
        return res




















    def test_handleEvent(self, action, hash):
        res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
        if action == "setOddsTable":
            events = res["Notify"]
            # print("buyPaper-res-events is ", events)
            notifyContents = []
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == ContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    notifyContents.append(notifyContent)
            print("setOddsTable-res-events is : ", notifyContents)
        elif action == "setLuckyToOngRate":
            events = res["Notify"]
            # print("buyPaper-res-events is ", events)
            notifyContents = []
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == ContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    if first == "setRate":
                        num = event["States"][1]
                        if not num:
                            num = "0"
                        num = bytearray.fromhex(num)
                        num.reverse()
                        num = int(num.hex(), 16)
                        notifyContent.append(num)
                        num = event["States"][2]
                        if not num:
                            num = "0"
                        num = bytearray.fromhex(num)
                        num.reverse()
                        num = int(num.hex(), 16)
                        notifyContent.append(num)
                    notifyContents.append(notifyContent)
            print("setLuckyToOngRate-res-events is : ", notifyContents)
        elif action == "startNewRound":
            events = res["Notify"]
            notifyContents = []
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == ContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    if first == "startNewRound":
                        roundNumber = event["States"][1]
                        if not roundNumber:
                            num = "0"
                        roundNumber = bytearray.fromhex(roundNumber)
                        roundNumber.reverse()
                        roundNumber = int(roundNumber.hex(), 16)
                        notifyContent.append(roundNumber)

                        timeStamp = str(event["States"][2])
                        if not timeStamp:
                            timeStamp = "0"
                        timeStamp = bytearray.fromhex(timeStamp)
                        timeStamp.reverse()
                        timeStamp = int(timeStamp.hex(), 16)
                        dateTime = datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
                        notifyContent.append(dateTime)

                        hashHexString = str(event["States"][3])
                        notifyContent.append(hashHexString)
                    notifyContents.append(notifyContent)
            print("startNewRound-res-events is : ", notifyContents)
        elif action == "bet":
            events = res["Notify"]
            notifyContents = []
            i = 1
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == ContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    notifyContent.append(first)
                    if first == "bet":
                        roundNumber = event["States"][1]
                        if not roundNumber:
                            num = "0"
                        roundNumber = bytearray.fromhex(roundNumber)
                        roundNumber.reverse()
                        roundNumber = int(roundNumber.hex(), 16)
                        notifyContent.append(roundNumber)

                        account = Address(binascii.a2b_hex(event["States"][2]))
                        account = account.b58encode()
                        notifyContent.append(account)

                        num = event["States"][3]
                        if not num:
                            num = "0"
                        num = bytearray.fromhex(num)
                        num.reverse()
                        num = int(num.hex(), 16)
                        notifyContent.append(num)
                    notifyContents.append(notifyContent)
            print("bet-res-events is : ", notifyContents)
        elif action == "endCurrentRound":
            res = sdk.rpc.get_smart_contract_event_by_tx_hash(hash)
            print("endCurrentRound-res is ", res)
            events = res["Notify"]
            notifyContents = []
            i = 1
            # print("events === ", events)
            for event in events:
                notifyContent = []
                if event["ContractAddress"] == ContractAddress:
                    first = (bytearray.fromhex(event["States"][0])).decode('utf-8')
                    if first == "endCurrentRound":
                        notifyContent.append(first)
                        roundNumber = event["States"][1]
                        if not roundNumber:
                            num = "0"
                        roundNumber = bytearray.fromhex(roundNumber)
                        roundNumber.reverse()
                        roundNumber = int(roundNumber.hex(), 16)
                        notifyContent.append(roundNumber)

                        explodePoint = event["States"][2]
                        if not explodePoint:
                            explodePoint = "0"
                        explodePoint = bytearray.fromhex(explodePoint)
                        explodePoint.reverse()
                        explodePoint = int(explodePoint.hex(), 16)
                        notifyContent.append(explodePoint)

                        salt = event["States"][3]
                        if not salt:
                            salt = "0"
                        salt = bytearray.fromhex(salt)
                        salt.reverse()
                        salt = int(salt.hex(), 16)
                        notifyContent.append(salt)

                        effectiveEscapeAcctPointOddsProfitList = event["States"][4]
                        notify1 = []
                        for effectiveEscapeAcctPointOddsProfit in effectiveEscapeAcctPointOddsProfitList:
                            notify2 = []
                            account = Address(binascii.a2b_hex(effectiveEscapeAcctPointOddsProfit[0]))
                            account = account.b58encode()
                            notify2.append(account)

                            escapePoint = effectiveEscapeAcctPointOddsProfit[1]
                            if not escapePoint:
                                escapePoint = "0"
                            escapePoint = bytearray.fromhex(escapePoint)
                            escapePoint.reverse()
                            escapePoint = int(escapePoint.hex(), 16)
                            notify2.append(escapePoint)

                            # odds = effectiveEscapeAcctPointOddsProfit[2]
                            # if not odds:
                            #     odds = "0"
                            # odds = bytearray.fromhex(odds)
                            # odds.reverse()
                            # odds = int(odds.hex(), 16)
                            # notify2.append(odds)

                            profit = effectiveEscapeAcctPointOddsProfit[2]
                            if not profit:
                                profit = "0"
                            profit = bytearray.fromhex(profit)
                            profit.reverse()
                            profit = int(profit.hex(), 16)
                            notify2.append(profit)

                            notify1.append(notify2)

                        notifyContent.append(notify1)
                        # print("endCurrentRound-res-event is : ", notifyContent)
                    elif first == "Error":
                        errorCode = event["States"][1]
                        if not errorCode:
                            errorCode = "0"
                        errorCode = bytearray.fromhex(errorCode)
                        errorCode.reverse()
                        errorCode = int(errorCode.hex(), 16)
                        notifyContent.append(errorCode)
                    notifyContents.append(notifyContent)
            print("endCurrentRound-res-events is : ", notifyContents)

        return True
