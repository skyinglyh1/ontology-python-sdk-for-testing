import binascii
import csv
import json
import os
import sys, getopt
from time import time
import time as time2
from collections import namedtuple

from ontology.account.account import Account
from ontology.common.address import Address
from ontology.core.transaction import Transaction
from ontology.ont_sdk import OntologySdk
from ontology.smart_contract.neo_contract.abi.abi_info import AbiInfo
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from ontology.smart_contract.neo_vm import NeoVm
import requests
import re
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction
# http://polaris3.ont.io:20336
# http://127.0.0.1:20336
def main(argv):
   try:
      opts, args = getopt.getopt(argv, "hm:i:c:f:", ["migrate=", "invoke=", "compile", "function"])
   except getopt.GetoptError:
      print('demo.py [-m|--migrate] [-i|--invoke] [-c|--compile]')
      sys.exit(2)
   m = {}
   for opt, arg in opts:
      if opt == '-h':
         print('test.py [-m|--migrate] [-i|--invoke invoke.json -f function] [-c swap.cs] ')
         sys.exit()
      elif opt in ("-m", "--migrate"):
          m["func"] = "migrate"
          deploy_cmd(m, str(arg))
      elif opt in ("-i", "--invoke"):
         m["func"] = "invoke"
         invoke_cmd(m, str(arg))
      elif opt in ("-c", "--compile"):
          compile_cmd(m, str(arg))
          return
      elif opt in ("-f", "--function"):
          funcs = str(arg).split(",")
          funcs2 = funcs.copy()
          for func in dict(m["function"]).values():
              if func["function_name"] in funcs2:
                  funcs2.remove(func["function_name"])
          if len(funcs2) == 0:
              execute(m, funcs)
          else:
              print("there is not the function:", funcs2)
          sys.exit()
   execute(m)


def compile_cmd(m: [], arg: str):
    url = ""
    payload = {"type": "", "code": ""}
    if arg == "":
        print("there is not contract")
        return
    elif "cs" in arg:
        payload["type"] = "CSharp"
        # url = "http://42.159.94.234:8080/api/v1.0/compile"
        url = "https://smartxcompiler.ont.io/api/v1.0/csharp/compile"
        with open(arg, "r") as f:
            contract = f.read()
            if str == "":
                print("contract is null")
            payload["code"] = contract
    elif "py" in arg:
        payload["type"] = "Python"
        # url = "http://42.159.92.140:8080/api/v1.0/compile"
        url = "https://smartxcompiler.ont.io/api/beta/python/compile"
        with open(arg, "r") as f:
            contract = f.read()
            type(contract)
            if str == "":
                print("contract is null")
            payload["code"] = contract

    header = {'Content-type': 'application/json'}
    timeout = 10
    path = os.path.dirname(arg)
    file_name = os.path.basename(arg).split(".")
    print("compiling, please wait a monment...")
    session = requests.session()
    res = session.post(url, json=payload, headers=header, timeout=timeout, verify=False)
    # res = requests.post(url, json=payload, headers=header, timeout=timeout)
    result = json.loads(res.content.decode())
    if result["errcode"] == 0:
        with open(path+"/"+(file_name[0])+".avm", "w", encoding='utf-8') as f:
            avm = result["avm"].lstrip('b\'')
            temp = avm.rstrip('\'')
            f.write(temp)
        with open(path+"/"+file_name[0]+"_abi.json", "w", encoding='utf-8') as f2:
            r = re.sub('\\\\n', '', str(result["abi"]))
            abi = str(r.lstrip('b\''))
            temp = abi.rstrip('\'')
            f2.write(temp.replace(' ', ''))
        print("compiled, Thank you")
    else:
        print("compile failed")
        print(result)


def deploy_cmd(m: [], arg: str):
    if "json" in str(arg):
        with open(arg, "r") as f:
            r = json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            m["No"] = 1
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
            m["contract_address"] = Address.address_from_vm_code(m["code"]).to_reverse_hex_str()
    else:
        temp = str(arg).split(",")
        m["No"] = 1
        for i in temp:
            t = str(i).split("=")
            m[t[0]] = t[1]


def invoke_cmd(m: [], arg: str):
    if "json" in str(arg):
        with open(arg, "r") as f:
            r = json.load(f)
            m["rpc_address"] = r["rpc_address"]
            m["payer_address"] = r["payer_address"]
            m["payer_password"] = r["payer_password"]
            m["wallet_file_path"] = r["wallet_file_path"]
            m["gas_limit"] = r["gas_limit"]
            m["gas_price"] = r["gas_price"]
            m["abi_path"] = r["abi_path"]
            m["save_file"] = r["save_file"]
            m["function"] = r["function"]
    else:
        temp = str(arg).split(",")
        for i in temp:
            t = str(i).split("=")
            m[t[0]] = t[1]


def execute(m:[], function_name=None):
    sdk = OntologySdk()
    sdk.set_rpc(m["rpc_address"])
    if m["func"] is "migrate":
        deploy(sdk, m)
    elif m["func"] is "invoke":
        invoke(sdk, m, function_name)
    else:
        print("only support migrate and invoke")


def invoke(sdk, m, function_name=None):
    func_maps = {}
    for i in dict(m["function"]).values():
        if function_name is not None:
            if i["function_name"] not in function_name:
                continue
        func_map = {}
        param_list = []
        func_map["function_name"] = i["function_name"]
        func_map["pre_exec"] = i["pre_exec"]
        try:
            if type(i["function_param"]) is dict:
                for value in dict(i["function_param"]).values():
                    if type(value) is list:
                        p_temp = []
                        for v in list(value):
                            p_temp.append(v)
                        param_list.append(p_temp)
                    else:
                        param_list.append(value)
            elif type(i["function_param"]) is list:
                temp_list = []
                for para in list(i["function_param"]):
                    if type(para) is dict:
                        temp_list2 = []
                        for para2 in dict(para).values():
                            temp_list2.append(para2)
                        temp_list.append(temp_list2)
                    # if type(para) is :
                    else:
                        temp_list.append(para)
                param_list.append(temp_list)
            func_map["param_list"] = param_list
        except Exception as e:
            pass
        if not i["pre_exec"]:
            try:
                func_map["signers"] = i["signers"]
            except AttributeError as e:
                func_map["signers"] = None
        func_maps[i["function_name"]] = func_map
    with open(str(m["abi_path"]), "r") as f:
        abi = json.loads(f.read(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        abi_info = AbiInfo(abi.hash, abi.entrypoint, abi.functions, abi.events)
        # print("abi_info is ", abi_info.hash, abi_info.entrypoint, abi_info.events, abi_info.functions)
        tmp = str(abi.hash)[2:]
        # print("tmp is ", tmp, type(tmp))
        contract_address = bytearray.fromhex(tmp)
        # print("contract_address is ", contract_address, type(contract_address))
        m["contract_address"] = contract_address.hex()
        contract_address.reverse()
        sdk.wallet_manager.open_wallet(m["wallet_file_path"])
        payer = sdk.wallet_manager.get_account(m["payer_address"], m["payer_password"])
        func_l = []
        no = 0
        for func_map in func_maps.values():
            if function_name is not None:
                if func_map["function_name"] not in function_name:
                    # params = BuildParams.create_code_params_script(function_name)
                    continue

            func = abi_info.get_function(func_map["function_name"])
            # print('func is ', func)
            if func is not None:
                func_map["return_type"] = func.return_type
            else:
                func_map["return_type"] = ""
                func = AbiFunction(func_map["function_name"], func_map["return_type"], func_map["param_list"])
                #print("func_map is ", func_map)
                #print("func is ", func)
            # print("func = "+str(func.name)+" -- "+str(func.parameters[0:])+" -- " +str(func.return_type))
            no = no + 1
            l = []
            l.append(no)
            l.append(func_map["function_name"])
            l.append(func_map["pre_exec"])
            # 用来放参数
            # print("func_map is ", func_map)
            # print("func is ", func)
            temp_l, params = convert_params(func, func_map)
            print("********", params)

            l.append(temp_l[:len(temp_l) - 1])

            if params is None:
                l.append("failed")
                func_l.append(l)
                continue
            try:
                print("")
                print("invoking, please waiting ...")
                print("method: " + func_map["function_name"])
                if func_map["pre_exec"]:
                    res = send_transaction(sdk, contract_address, None, None, 0, 0, params, True)
                    # print("res in pre_exec part :", res)
                    if res["error"] != 0:
                        print(res["desc"])
                        l.append(res["desc"])
                    else:
                        # print('**** res **** is ', res)
                        # print("######## res[result][Result] is ",res["result"]["Result"], type(res["result"]["Result"]))
                        if res["result"]["Result"] is None or res["result"]["Result"] == "":
                            # print("res:", res["result"]["Result"])
                            l.append("")
                        else:

                            if func_map["return_type"] == "Integer":
                                value = bytearray.fromhex(res["result"]["Result"])
                                value.reverse()
                                print("res:", int(value.hex(), 16))
                                l.append(int(value.hex(), 16))
                            elif func_map["return_type"] == "ByteArray":
                                # print("res:", (bytearray.fromhex(res["result"]["Result"])))
                                print("res:", res["result"]["Result"])
                                l.append(res["result"]["Result"])
                            elif func_map["return_type"] == "":
                                print("res:", res["result"]["Result"])
                                l.append(res["result"]["Result"])
                            elif func_map["return_type"] == "IntegerArray":
                                # print(" returntype = IntegerArray ")
                                print("res For IntegerArray is ", res["result"]["Result"])
                                returnedList = res["result"]["Result"]
                                intReturnList = []
                                for element in returnedList:
                                    if not element:
                                        element = "00"
                                    value = bytearray.fromhex(element)
                                    value.reverse()
                                    intValue = int(value.hex(), 16)
                                    intReturnList.append(intValue)

                                print("res: ", intReturnList)
                                l.append(intReturnList)
                            elif func_map["return_type"] == "ByetArrayArray":
                                print(" returntype = ByteArrayArray ")
                                print("res For ByetArrayArray is ", res["result"]["Result"])
                                returnedList = res["result"]["Result"]
                                ByteArrayReturnList = []
                                for element in returnedList:
                                    # Address.b58decode(func_map["param_list"][i], False).to_array()
                                    # ByteArrayValue = (bytearray.fromhex(element))
                                    # str1 = "7575526bc066a3acc6abb134119cd6d4a9041969"
                                    # address1=Address(binascii.a2b_hex(str1))
                                    address1 = Address(binascii.a2b_hex(element))
                                    ByteArrayValue = address1.b58encode()
                                    ByteArrayReturnList.append(ByteArrayValue)
                                print("res: ", ByteArrayReturnList)
                                l.append(ByteArrayReturnList)
                            else:
                                print("res:", (bytearray.fromhex(res["result"]["Result"])).decode('utf-8'))
                                l.append((bytearray.fromhex(res["result"]["Result"])).decode('utf-8'))
                else:

                    txhash, err = handle_tx(contract_address, func_map, params, payer, m, sdk)
                    if txhash == "":
                        l.append(err)
                    else:
                        for i in range(10):
                            time2.sleep(1)
                            event = sdk.rpc.get_smart_contract_event_by_tx_hash(txhash)
                            if event is not None:
                                print("txhash:", txhash)
                                print("event:", event)
                                break
                        l.append(txhash)
            except Exception as e:
                print("Error:", e)
                l.append(e)
            func_l.append(l)
        save_file(m, "", func_l)


def send_transaction(sdk, contract_address: bytearray, acct: Account, payer_acct: Account, gas_limit: int,
                         gas_price: int, param_list:[], pre_exec: bool):
    params = BuildParams.create_code_params_script(param_list)
    if pre_exec:
        tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 0, 0)
        if acct is not None:
            sdk.sign_transaction(tx, acct)
        return sdk.rpc.send_raw_transaction_pre_exec(tx)
    unix_time_now = int(time())
    params.append(0x67)
    for i in contract_address:
        params.append(i)
    tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer_acct.get_address().to_array(),
                     params, bytearray(), [], bytearray())
    if acct is not None:
        sdk.sign_transaction(tx, acct)
    if payer_acct is not None and acct is not None and acct.get_address_base58() != payer_acct.get_address_base58():
        sdk.add_sign_transaction(tx, payer_acct)
    return sdk.rpc.send_raw_transaction(tx)


def deploy(sdk, m):
    # 判断是否已经部署
    code = sdk.rpc.get_smart_contract(m["contract_address"])
    if code != "unknow contract":
        print("contract have been deployed")
        print("contract_address:", m["contract_address"])
        return
    need_storage = False
    if m["need_storage"] is 'true':
        need_storage = True
    tx = sdk.neo_vm().make_deploy_transaction(m["code"], need_storage, m["name"], m["code_version"], m["author"]
                                              , m["email"], m["desp"], m["payer_address"], m["gas_limit"],
                                              m["gas_price"])
    sdk.wallet_manager.open_wallet(m["wallet_file_path"])
    acct = sdk.wallet_manager.get_account(m["payer_address"], m["payer_password"])
    sdk.sign_transaction(tx, acct)
    sdk.set_rpc(m["rpc_address"])
    try:
        print("deploying，please waiting ...")
        res = sdk.rpc.send_raw_transaction(tx)
        print("txhash:", res)
        for i in range(10):
            time2.sleep(1)
            res = sdk.rpc.get_smart_contract(m["contract_address"])
            if res == "unknow contract" or res == "":
                continue
            else:
                print("deploy success")
                save_file(m, "success")
                return
        print("deployed failed")
        save_file(m, "deployed failed")
    except Exception as e:
        print(e)
        save_file(m, e)


def handle_tx(contract_address, func_map, param_list, payer, m, sdk):
    #print("param_list:", param_list)
    #print('param_list is ', param_list)
    params = BuildParams.create_code_params_script(param_list)
    print("Second final params ------ ", param_list)

    unix_time_now = int(time())
    params.append(0x67)
    #print("final params ------ ",params)
    for i in contract_address:
        params.append(i)
    tx = Transaction(0, 0xd1, unix_time_now, m["gas_price"], m["gas_limit"],
                     payer.get_address().to_array(),
                     params, bytearray(), [], bytearray())
    sdk.add_sign_transaction(tx, payer)
    path_addr = []
    if type(func_map["signers"]) is dict:
        signers = func_map["signers"]
        if signers["m"] == 1:
            sdk.wallet_manager.open_wallet(signers["signer"]["walletpath"])
            acc = sdk.wallet_manager.get_account(signers["signer"]["address"], signers["signer"]["password"])
            if acc is not None:
                sdk.add_sign_transaction(tx, acc)
        else:
            print("not supported multi signature")
            return "", "not supported multi signature"
    elif type(func_map["signers"]) is list:
        for signer in list(func_map["signers"]):
            if signer["m"] == 1:
                if signer["signer"]["walletpath"] not in path_addr:
                    path_addr.append(signer["signer"]["walletpath"])
                    sdk.wallet_manager.open_wallet(signer["signer"]["walletpath"])
                acc = sdk.wallet_manager.get_account(signer["signer"]["address"], signer["signer"]["password"])
                if acc is not None:
                    sdk.add_sign_transaction(tx, acc)
            else:
                print("not support multi signature")
                return "", "not supported multi signature"
                # TODO
    res = sdk.rpc.send_raw_transaction(tx)
    return res, ""


def convert_params(func, func_map: {}):
    params_list = []
    params_list.append(func_map["function_name"].encode())
    params = []
    temp_l = ""
    # print("******* \n ", func_map["param_list"])
    for i in range(len(func_map["param_list"])):
        # print("type is ", func.parameters[i], type(func.parameters[i]))
        if func.parameters[i].type == "String":
            params.append(str(func_map["param_list"][i]))
            temp_l += str(func_map["param_list"][i]) + ":"
        elif func.parameters[i].type == "ByteArray":
            temp_l += str(func_map["param_list"][i]) + ":"
            try:
                addr = bytearray()
                if func_map["param_list"][i].startswith("A"):
                    addr = Address.b58decode(func_map["param_list"][i], False).to_array()
                    #print('address is *********** ', addr, type(addr))
                else:
                    addr = Address(bytearray.fromhex(func_map["param_list"][i])).to_array()
                params.append(addr)
            except Exception as e:
                params.append(bytearray(func_map["param_list"][i].encode()))
        elif func.parameters[i].type == "Integer":
            params.append(func_map["param_list"][i])
            temp_l += str(func_map["param_list"][i]) + ":"
        elif func.parameters[i].type == "Array":
            param_l = []
            for param in func_map["param_list"][i]:
                # print("type is ", type(param))
                if type(param) is dict:
                    temp = []
                    for p in dict(param).values():
                        if type(p) is str:
                            temp_l = str(p).split(":")[1] + ":"
                            if str(p).split(":")[0] == "String":
                                temp.append(str(p).split(":")[1])
                            elif str(p).split(":")[0] == "ByteArray":
                                try:
                                    temp.append(Address.b58decode(str(p).split(":")[1], False).to_array())
                                except Exception as e:
                                    # temp.append(str(p).split(":")[1].encode())
                                    temp.append(bytearray.fromhex(p.split(":")[1]))
                            # elif str(p).split(":")[0] == "Integer":
                            #     temp.append(int(str(p).split(":")[1]))
                        elif type(p) is bool:
                            temp.append(p)
                            if p:
                                temp_l += "false:"
                            else:
                                temp_l += "true:"
                        elif type(p) is int:
                            temp.append(p)
                            temp_l += str(p) + ":"
                        else:
                            print("not supported data type")
                            temp_l += "not supported data type" + ":"
                            return
                    param_l.append(temp)
                elif type(param) is list:
                    param_l.append(param)
                else:
                    temp_l += "not supported data type" + ":"
                    print("only support dict")
                    return temp_l, None
            print("22222", param_l)
            print("3333", params)
            if len(params) == 0 :
                # print("go here")
                params = param_l
            elif len(params) == 1 and len(param_l) == 1:
                params.append(param_l[0])
            else:
                params.append(param_l)
    params_list.append(params)
    return temp_l, params_list


def save_file(m: [], res: str, func_l = None):
    ishasheader = False
    no = 0
    if os.path.exists(m["save_file"]):
        with open(m["save_file"], "r") as f:
            lines = list(csv.reader(x.replace('\0', '') for x in f))
            # lines = list(csv.reader(f))
            if len(lines) <= 1:
                no = 0
            else:
                ishasheader = True
                line = list(lines)[len(list(lines)) - 1]
                no = int(line[0], 10) + 1
    if m["func"] == "migrate":
        with open(m["save_file"], "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not ishasheader:
                writer.writerow(
                    ["No", "need_storage", "name", "code_version", "author", "email", "desp", "payer_address", "gas_limit",
                     "gas_price", "result"])
            writer.writerow([m["No"]+no, m["need_storage"], m["name"], m["code_version"], m["author"], m["email"], m["desp"],
                             m["payer_address"], m["gas_limit"], m["gas_price"], res])
    elif m["func"] == "invoke":
        with open(m["save_file"], "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not ishasheader:
                writer.writerow(["No", "contract_address", "payer_address", "gas_limit", "gas_price","function_name","pre_exec","params", "result"])
            for i in func_l:
                writer.writerow([i[0]+no, m["contract_address"], m["payer_address"], m["gas_limit"], m["gas_price"],i[1], i[2], i[3],i[4]])


if __name__ == "__main__":
   main(sys.argv[1:])