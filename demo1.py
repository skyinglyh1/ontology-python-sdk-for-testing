import csv
import json
import os
import sys, getopt
import time
from collections import namedtuple
from ontology.common.address import Address
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "-h-m:-i:-p", ["migrate=", "invoke=",])
    except getopt.GetoptError:
        print('test.py [-m|--migrate] [-i|--invoke] ')
        sys.exit(2)
    m = {}
    invoke_func_name = ""
    pre_exec = False
    for opt, arg in opts:
        if opt == '-h':
            print('test.py [-m|--migrate] [-i|--invoke] ')
            sys.exit()
        elif opt in ("-m", "--migrate"):
            m["func"] = "migrate"
            if "json" in str(arg):
                with open(arg, "r") as f:
                    r = json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
                    #print("r_json_content is ", r)
                    m["rpc_address"] = r.rpc_address
                    m["need_storage"] = r.need_storage
                    m["name"] = r.name
                    m["code_version"] = r.code_version
                    m["author"] = r.author
                    m["email"] = r.email
                    m["desp"] = r.desp
                    m["payer_address"] = r.payer_address
                    m["payer_password"] = r.payer_password
                    m["wallet_file_path"] = r.wallet_file_path
                    m["gas_limit"] = r.gas_limit
                    m["gas_price"] = r.gas_price
                    m["save_file"] = r.save_file
                    if ".avm" in r.code:
                        with open(r.code, "r") as f2:
                            m["code"] = f2.read()
                    else:
                        m["code"] = r.code
                    m["contract_address"] = Address.address_from_vm_code(m["code"]).to_hex_str()
            else:
                temp = str(arg).split(",")
                for i in temp:
                    t = str(i).split("=")
                    m[t[0]] = t[1]
        elif opt in ("-i", "--invoke"):
            invoke_func_name = arg
            print('invoke_function is ', invoke_func_name)
            m["func"] = "invoke"
            invoke_json_path = './invoke.json'
            if "json" in str(invoke_json_path):
                with open(invoke_json_path, "r") as f:
                    r = json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
                    m["rpc_address"] = r.rpc_address
                    m["acct_address"] = r.acct_address
                    m["acct_password"] = r.acct_password
                    m["payer_address"] = r.payer_address
                    m["payer_password"] = r.payer_password
                    m["wallet_file_path"] = r.wallet_file_path
                    m["gas_limit"] = r.gas_limit
                    m["gas_price"] = r.gas_price
                    #m["abi_path"] = r.abi_path
                    m["save_file"] = r.save_file
                    print('m_save_file is ', m["save_file"])
                    #m["function"] = r.function
                    if "abi.json" in r.abi:
                        with open(r.abi, "r") as f:
                            m["abi"] = f.read()
                    else:
                        m["abi"] = r.abi
            else:
                temp = str(invoke_json_path).split(",")
                for i in temp:
                    t = str(i).split("=")
                    m[t[0]] = t[1]
        elif opt in ("-p", "--pre"):
            pre_exec = True
            print('pre_exec is True')
        else:
            print('test.py [-m|--migrate] [-i|--invoke] ')
            sys.exit()
    sdk = OntologySdk()
    sdk.set_rpc(m["rpc_address"])
    if m["func"] is "migrate":
        need_storage = False
        if m["need_storage"] is 'true':
            need_storage = True
        tx = sdk.neo_vm().make_deploy_transaction(m["code"], need_storage, m["name"], m["code_version"], m["author"]
                                                  , m["email"], m["desp"], m["payer_address"], m["gas_limit"],
                                                  m["gas_price"])
        sdk.wallet_manager.open_wallet(m["wallet_file_path"])
        acct = sdk.wallet_manager.get_account(m["payer_address"], m["payer_password"])

        print('acct.address', acct.get_address_base58())

        sdk.sign_transaction(tx, acct)
        sdk.set_rpc(m["rpc_address"])
        try:
            print("deploying，please waiting ...")
            r = sdk.rpc.send_raw_transaction(tx)
            print("txhash:", r)
            for i in range(10):
                time.sleep(1)
                r = sdk.rpc.get_smart_contract(m["contract_address"])
                if r == "":
                    continue
                else:
                    print("deploy success")
                    break
            save_file(m, "success")
        except Exception as e:
            print(e)
            save_file(m, e)
    elif m["func"] is "invoke":
        res_abi = json.loads(m["abi"], object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        abi_info = AbiInfo(res_abi.hash, res_abi.entrypoint, res_abi.functions, res_abi.events)
        contract_address = bytearray.fromhex(str(res_abi.hash)[2:])
        contract_address.reverse()
        #print("contract_address is ", contract_address)
        sdk.wallet_manager.open_wallet(m["wallet_file_path"])
        acct = sdk.wallet_manager.get_account(m["acct_address"], m["acct_password"])
        payer = sdk.wallet_manager.get_account(m["payer_address"], m["payer_password"])
        print('res_abi.hash is ', res_abi.hash)
        #print('res_abi.entrypoint is ', res_abi.entrypoint)
        #print('res_abi.function is ', res_abi.functions, type(res_abi.functions), len(res_abi.functions))
        invoke_func = abi_info.get_function(invoke_func_name)
        func_params = {}

        for function in res_abi.functions:
            if function.name == invoke_func_name:
                func_params = function.parameters
        func_params_map ={}
        for param in func_params:
            hinter = 'Pls input ' + param.name + ' ('+ param.type + ')' + ': '
            raw_input = input(hinter)
            if param.type == 'String':
                invoke_func.parameters.append(str(raw_input))
            if param.type == 'ByteArray':
                invoke_func.parameters.append(bytearray(raw_input))
            if param.type == 'Integer':
                invoke_func.parameters.append(int(raw_input))
        try:
            print("")
            print("invoking '" + invoke_func_name + "', please waiting ...")
            #print("method: " + invoke_func_name)
            res = sdk.neo_vm().send_transaction(contract_address, acct, payer, m["gas_limit"], m["gas_price"], invoke_func, pre_exec)
            if not pre_exec:
                time.sleep(6)
                print("txhash:", res)
                print("Event:", sdk.rpc.get_smart_contract_event_by_tx_hash(res))
            else:
                print(res)
                print("res:", (bytearray.fromhex(res)).decode('utf-8'))
                #l.append((bytearray.fromhex(res)).decode('utf-8'))
        except Exception as e:
            print("Error:", e)
            #l.append(e)
        #func_l.append(l)
    else:
        print('only support migrate and invoke')










def save_file(m: [], res: str, func_l = None):
    ishasheader = False
    if os.path.exists(m["save_file"]):
        ishasheader = True
    if m["func"] == "migrate":
        with open(m["save_file"], "a") as csvfile:
            writer = csv.writer(csvfile)
            if not ishasheader:
                writer.writerow(
                    ["need_storage", "name", "code_version", "author", "email", "desp", "payer_address", "gas_limit",
                     "gas_price"])
            writer.writerow([m["need_storage"], m["name"], m["code_version"], m["author"], m["email"], m["desp"],
                             m["payer_address"], m["gas_limit"], m["gas_price"], res])
    elif m["func"] == "invoke":
        with open(m["save_file"], "a") as csvfile:
            writer = csv.writer(csvfile)
            if not ishasheader:
                writer.writerow(["contract_address", "acct_address", "payer_address", "gas_limit", "gas_price","function_name","pre_exec","params", "result"])
            for i in func_l:
                writer.writerow([m["contract_address"], m["acct_address"], m["payer_address"], m["gas_limit"], m["gas_price"], i[0],i[1], i[2], i[3]])


if __name__ == "__main__":
   main(sys.argv[1:])