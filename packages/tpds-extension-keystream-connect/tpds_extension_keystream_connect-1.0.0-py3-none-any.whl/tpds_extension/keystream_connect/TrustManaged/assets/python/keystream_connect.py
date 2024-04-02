# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
import yaml
import time
import glob
import platform
import subprocess
import zipfile
import re
from contextlib import contextmanager
import sys, os
import tpds.tp_utils
from tpds.tp_utils.tp_settings import TPSettings
import tpds.tp_utils.tp_input_dialog as tp_userinput
from tpds.tp_utils.tp_print import print
from tpds.devices import TpdsBoards
from tpds.flash_program import FlashProgram
from pykitinfo import pykitinfo
from tpds.secure_element import ECC608A
import cryptoauthlib as cal

boardName = "DM320118"

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

class keySTREAM_AWS_Cert_Mgmt():
    def __init__(self, ks_config_path, hfile_path):
        self.ks_config_path = ks_config_path
        self.hfile_path = hfile_path

    def resetBoard(self):
            """
                Get the board info for DM320118 and Do a factory reset
            """
            msg_box_info = f'<font color=#0000ff><b>To Generate Manifest Lite the device should be factory reset.<br> Click "OK" to factory reset.<br><font color="green">This action may take few minutes.<br>Please wait until you see a status pop-up.</font></b></font><br>'
            modify_input_diag = tp_userinput.TPMessageBox(
                title="Flash Programming",
                info=msg_box_info,
                option_list=['OK','Cancel'])
            modify_input_diag.invoke_dialog()
            if modify_input_diag.user_select == 'OK':
                boardInfo = TpdsBoards().get_board_info(boardName)
                flash_program = FlashProgram(boardName, boardInfo)
                assert flash_program.is_board_connected(), "Check the Kit parser board connections"
                board_status = flash_program.check_board_status()
                print("\033[0;31mPLEASE WAIT\033[0m")
                print("\033[1;31mTHIS ACTION MAY TAKE A FEW MINUTES..\033[0m")
                with suppress_stdout():
                    if board_status != "factory_programmed":
                        factory_hex_path = os.path.join(boardInfo.board_path, boardName, f"{boardName}.hex")
                        assert factory_hex_path, "Factory hex is unavailable to program"
                        status = flash_program.load_hex_image_with_ipe(factory_hex_path)
                    else:
                            status = "success"

            elif modify_input_diag.user_select == 'Cancel':
                raise Exception("Factory reset failed.")

            elif isinstance(e, TypeError):
                status = f"An unexpected error occurred: {e}"
                raise Exception("Please check the device connection.")

            return status


    def manifest_lite(self, b=None):
        try:
            print('Executing Step-1.....')
            status = self.resetBoard()
            if status != "success":
                print("Error : ", status)
            else:
                msg_box_info = f'<font color=#0000ff><b>Factory Reset Completed.</b></font><br><font color="green"><b>STEP 1: Disconnect and Connect the Device.<br>STEP 2: Click "OK" to generate the Manifest Lite.</font></b></font><br>'
                modify_input_diag = tp_userinput.TPMessageBox(
                title="Factory Reset",
                info=msg_box_info,
                option_list=['OK','Cancel'])
                modify_input_diag.invoke_dialog()

            if modify_input_diag.user_select == 'OK':
                sys_shell = True if sys.platform == 'win32' else False
                lite_manifest_path = os.path.join(
                                TPSettings().get_base_folder(),
                                'keystream_connect', 'lite_manifest')

                os.chdir(lite_manifest_path)
                subProcessOut = tpds.tp_utils.run_subprocess_cmd(
                    cmd=["python", "tmng_manifest_lite_generation.py"],
                    sys_shell=sys_shell)
                if subProcessOut[0]:
                    raise ValueError("Manifest_lite generation failed!\nPlease check the device connection.")
                else:
                    zip_file_path = lite_manifest_path + "\\"
                    zip_file_path_1 = subProcessOut[1].strip() + "\\" + subProcessOut[1].strip() + ".zip"
                    msg_box_info = f'<font color=#0000ff><b>Manifest File generated in following path:</b></font><br>{zip_file_path}<br>{ zip_file_path_1}'
                    modify_input_diag = tp_userinput.TPMessageBox(
                    title="Manifest_lite Generated Sucessfully",
                    info=msg_box_info,
                    option_list=['OK','Cancel'])
                    modify_input_diag.invoke_dialog()
            elif modify_input_diag.user_select == 'Cancel':
                raise Exception("Manifest generation failed")
        except ValueError as e:
            raise e

    def get_inputs(self, b=None):
        print('Executing Step-2...')
        msg_box_info = (
                '<font color=#0000ff><b>Do you want to Enter/Modify any Pre-Config ?'
                '</b></font><br>')
        modify_input_diag = tp_userinput.TPMessageBox(
            title="Edit Configuration?",
            info=msg_box_info)
        modify_input_diag.invoke_dialog()

        print(f'Selected option is: {modify_input_diag.user_select}', canvas=b)

        # Get Multiple User Inputs Until User select Cancel.
        while modify_input_diag.user_select == 'OK':

            ks_creds_file = os.path.join(
                        TPSettings().get_base_folder(),
                        'keystream_config.yaml')

            with open(ks_creds_file, 'r+') as ks_file:
                ks_data = yaml.safe_load(ks_file)

            aws_creds_file = os.path.join(
                        TPSettings().get_base_folder(),
                        'aws_credentials.yaml')

            with open(aws_creds_file, 'r+') as aws_file:
                aws_cred_data = yaml.safe_load(aws_file)


            item_list = ['Fleet Profile Public UID', 'WiFi SSID', 'WiFi Password', 'keySTREAM Authorization Token', 'AWS Access Key ID', 'AWS Secret Access Key', 'Region','Apply All Settings']
            dropdown_desc = (
            '''<font color=#0000ff><b>Pre-config Input Selection</b>
            </font><br>
            <br>Fleet Profile Public UID - Enter the Fleet Profile Public UID Created in keySTREAM UI.
            <br>WiFi SSID - Provide WiFi SSID to which device needs to connect.
            <br>WiFi Password - Provide Wifi Password for device to connect.
            <br>keySTREAM Authorization Token - Provide Authorization Token.
            <br>AWS Access Key ID - Provide AWS Key ID.
            <br>AWS Secret Access Key - Provide AWS Secret Access Key.
            <br>Region - Provide AWS Region (eg:us-east-2)
            <br>Apply All Settings - Select this Option if All Inputs are Provided''')

            user_input = tp_userinput.TPInputDropdown(
                                        item_list=item_list,
                                        desc=dropdown_desc,
                                        dialog_title='Pre-Config Input Selection')
            user_input.invoke_dialog()
            print(f'Selected option is: {user_input.user_option}', canvas=b)
     

            if user_input.user_option == None:
                raise Exception ("Please select appropriate option.")
        
            if user_input.user_option == 'Fleet Profile Public UID':
                text_box_desc = (
                    '''<font color=#0000ff><b>Enter Fleet Profile Public UID</b></font><br>
                    <br>Please follow the instructions in Pre-Configure Steps to create Fleet Profile Public UID<br>''')
                pub_profile_uid = tp_userinput.TPInputTextBox(
                                                    desc=text_box_desc,
                                                    dialog_title='Fleet Profile Public UID')
                pub_profile_uid.invoke_dialog()
                print("Entry Done: Fleet Profile Public UID")
                ks_data['pub_uid'] = pub_profile_uid.user_text

            elif user_input.user_option == 'WiFi SSID':
                text_box_desc = (
                    '''<font color=#0000ff><b>Enter Wifi SSID</b></font><br>
                    ''')
                wifi_ssid = tp_userinput.TPInputTextBox(
                                                    desc=text_box_desc,
                                                    dialog_title='Wifi SSID')
                wifi_ssid.invoke_dialog()
                print("Entry Done: Wifi SSID")
                ks_data['ssid'] = wifi_ssid.user_text

            elif user_input.user_option == 'WiFi Password':
                text_box_desc = (
                    '''<font color=#0000ff><b>Enter Wifi Password</b></font><br>
                    ''')
                wifi_password = tp_userinput.TPInputTextBox(
                                                    desc=text_box_desc,
                                                    dialog_title='Wifi Password')
                wifi_password.invoke_dialog()
                print("Entry Done: Wifi Password")
                ks_data['password'] = wifi_password.user_text

            elif user_input.user_option == 'keySTREAM Authorization Token':
                text_box_desc = (
                    '''<font color=#0000ff><b>Enter keySTREAM Authorization Token</b></font><br>
                    ''')
                keystream_authorization_token = tp_userinput.TPInputTextBox(
                                                    desc=text_box_desc,
                                                    dialog_title='keySTREAM Authorization Token')
                keystream_authorization_token.invoke_dialog()
                print("Entry Done: keySTREAM Authorization Token")
                ks_data['keystream_auth_token'] = "Basic " + keystream_authorization_token.user_text

            elif user_input.user_option == 'AWS Access Key ID':
                text_box_desc = (
                    '''<font color=#0000ff><b>Enter AWS Access Key ID</b></font><br>
                    <br>Please follow the instructions in Pre-Configure Steps to create AWS Account if don't have one <br>''')
                aws_access_key_id = tp_userinput.TPInputTextBox(
                                                    desc=text_box_desc,
                                                    dialog_title='AWS Access Key ID')
                aws_access_key_id.invoke_dialog()
                print("Entry Done: AWS Access Key ID")
                aws_cred_data['access_key_id'] = aws_access_key_id.user_text

            elif user_input.user_option == 'AWS Secret Access Key':
                text_box_desc = (
                    '''<font color=#0000ff><b>Enter AWS Secret Access Key</b></font><br>
                    ''')
                aws_secret_access_key = tp_userinput.TPInputTextBox(
                                                    desc=text_box_desc,
                                                    dialog_title='AWS Secret Access Key')
                aws_secret_access_key.invoke_dialog()
                print("Entry Done: AWS Secret Access Key")
                aws_cred_data['secret_access_key'] = aws_secret_access_key.user_text

            elif user_input.user_option == 'Region':
                text_box_desc = (
                    '''<font color=#0000ff><b>Enter Region</b></font><br>
                    ''')
                region = tp_userinput.TPInputTextBox(
                                                    desc=text_box_desc,
                                                    dialog_title='Region')
                region.invoke_dialog()
                print("Entry Done: Region")
                aws_cred_data['region'] = region.user_text
            
            elif user_input.user_option == 'Apply All Settings':
                break
                

            with open(ks_creds_file, 'w') as ks_file:
                ks_file.write( yaml.dump(ks_data, sort_keys=False))

            with open(aws_creds_file, 'w') as aws_file:
                aws_file.write( yaml.dump(aws_cred_data, sort_keys=False))

        # End of while loop

        # Check if all data available
        creds_file = os.path.join(
                        TPSettings().get_base_folder(),
                        'keystream_config.yaml')

        with open(creds_file) as ks_file:
            data = yaml.safe_load(ks_file)

        data_not_available = []
        if data['ssid'] == '' or data['ssid'] == None:
            data_not_available.append('Wifi SSID')

        if data['password'] == '' or data['password'] == None:
            data_not_available.append('Wifi Password')


        if data['pub_uid'] == '' or data['pub_uid'] == None:
            data_not_available.append('Fleet Profile Public UID')

        if data['keystream_auth_token'] == '' or data['keystream_auth_token'] == None:
            data_not_available.append('keySTREAM Authorization Token')

        aws_creds_file = os.path.join(
                        TPSettings().get_base_folder(),
                        'aws_credentials.yaml')

        with open(aws_creds_file) as aws_file:
            aws_data = yaml.safe_load(aws_file)

        if aws_data['access_key_id'] == '' or aws_data['access_key_id'] == None:
            data_not_available.append('Aws Access Key ID')

        if aws_data['secret_access_key'] == '' or aws_data['secret_access_key'] == None:
            data_not_available.append('AWS Secret Access Key')

        if aws_data['region'] == '' or aws_data['region'] == None:
            data_not_available.append('Region')

        if bool(data_not_available):
            data_not_available = '\n'.join(data_not_available)
            raise Exception(f'Following Data are Not Available:\n{data_not_available}.\nPlease Select Step -2 and Provide the Data')

    def get_cacert(self, b=None):

        print('Executing Step-3...')
        creds_file = os.path.join(
                        self.ks_config_path,
                        'keystream_config.yaml')

        with open(creds_file) as f:
            data = yaml.safe_load(f)

        aws_creds_file = os.path.join(
                        self.ks_config_path,
                        'aws_credentials.yaml')

        with open(aws_creds_file) as aws_file:
            aws_data = yaml.safe_load(aws_file)

        global headers
        headers = {
            'accept' : 'application/json',
            'x-correlation-id' : 'ISEPDMUI-4d1cff76-7ace-4fda-0811-488fb8d99cbf',
            'Authorization' : data['keystream_auth_token']
        }

        ssid = data['ssid']
        password = data['password']
        pub_uid = data['pub_uid']
        global keystream_coap_endpoint
        global keystream_http_endpoint
        global keystream_endpoint
        
        keystream_coap_endpoint = data['keystream_coap_endpoint']
        keystream_http_endpoint = data['keystream_http_endpoint']
        # Only coap url could be accessed from outside via Rest API
        keystream_endpoint = data['keystream_coap_endpoint']
        # Setting AWS Credentials
        sys_shell = True if sys.platform == 'win32' else False
        subProcessOut = tpds.tp_utils.run_subprocess_cmd(
            cmd=[
                "aws", "configure", "set",
                "default.aws_access_key_id", aws_data['access_key_id']],
            sys_shell=sys_shell)

        if subProcessOut[0] != 0:
                raise Exception(f'Setting AWS Access key ID Failed!!!\nError:{subProcessOut[2]}.\n')

        subProcessOut = tpds.tp_utils.run_subprocess_cmd(
            cmd=[
                "aws", "configure", "set",
                "default.aws_secret_access_key", aws_data['secret_access_key']],
            sys_shell=sys_shell)

        if subProcessOut[0] != 0:
                raise Exception(f'Setting AWS Secret Access Key Failed!!!\nError:{subProcessOut[2]}.\n')

        subProcessOut = tpds.tp_utils.run_subprocess_cmd(
            cmd=[
                "aws", "configure", "set",
                "default.region", aws_data['region']],
            sys_shell=sys_shell)

        if subProcessOut[0] != 0:
                raise Exception(f'Setting AWS Region Failed!!!\nError:{subProcessOut[2]}.\n')

        #Getting AWS Endpoint
        subProcessOut = tpds.tp_utils.run_subprocess_cmd(
            cmd=[
                "aws", "iot", "describe-endpoint",
                "--endpoint-type", "iot:Data", "--output=text"],
            sys_shell=sys_shell)

        if subProcessOut[0] != 0:
                raise Exception(f'Getting AWS Endpoint Failed!!!\nError:{subProcessOut[2]}.\n')

        global aws_endpoint
        aws_endpoint = subProcessOut[1]
        aws_endpoint = aws_endpoint.replace('\n', '')
        # Writing config to header file
        ks_coap_url = "icpp." + keystream_coap_endpoint
        ks_http_url = "icph." + keystream_http_endpoint
        hfile_path = os.path.join(self.hfile_path, 'tmg_conf.h')
        with open(hfile_path, 'w') as fh:
            fh.write('/******************************************************************************\n')
            fh.write('*************************keySTREAM Trusted Agent ("KTA")***********************\n')
            fh.write('* (c) 2023-2024 Nagravision Sarl\n')
            fh.write('\n')
            fh.write('* Subject to your compliance with these terms, you may use the Nagravision Sarl\n')
            fh.write('* Software and any derivatives exclusively with Nagravision’s products. It is your\n')
            fh.write('* responsibility to comply with third party license terms applicable to your\n') 
            fh.write('* use of third party software (including open source software) that may accompany\n') 
            fh.write('* Nagravision Software.\n')
            fh.write('\n')
            fh.write('* Redistribution of this Nagravision Software in source or binary form is allowed\n') 
            fh.write('* and must include the above terms of use and the following disclaimer with the\n') 
            fh.write('* distribution and accompanying materials.\n')
            fh.write('\n')
            fh.write('* THIS SOFTWARE IS SUPPLIED BY NAGRAVISION "AS IS". NO WARRANTIES, WHETHER EXPRESS,\n') 
            fh.write('* IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED WARRANTIES OF\n') 
            fh.write('* NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE. IN NO\n') 
            fh.write('* EVENT WILL NAGRAVISION BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE, INCIDENTAL\n') 
            fh.write('* OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND WHATSOEVER RELATED TO\n') 
            fh.write('* THE SOFTWARE, HOWEVER CAUSED, EVEN IF NAGRAVISION HAS BEEN ADVISED OF THE\n') 
            fh.write('* POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE FULLEST EXTENT ALLOWED BY LAW,\n') 
            fh.write('* NAGRAVISION S TOTAL LIABILITY ON ALL CLAIMS IN ANY WAY RELATED TO THIS\n') 
            fh.write('* SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY, THAT YOU HAVE PAID DIRECTLY\n') 
            fh.write('* TO NAGRAVISION FOR THIS SOFTWARE. \n')
            fh.write('******************************************************************************/\n')
            fh.write('/** \\brief  Configuration file for environment setup.\n')
            fh.write('*\n')
            fh.write('*  \\author Kudelski IoT\n')
            fh.write('*\n')
            fh.write('*  \date 2023/06/12\n')
            fh.write('*\n')
            fh.write('*  \\file tmg_conf.h\n')
            fh.write('******************************************************************************/\n\n')
            fh.write('/**\n')
            fh.write(' * @brief Configuration file for environment setup.\n')
            fh.write(' */\n\n')
            fh.write('#ifndef TMG_CONF_H\n')
            fh.write('#define TMG_CONF_H\n\n')
            fh.write('#ifdef __cplusplus\n')
            fh.write('extern "C" {\n')
            fh.write('#endif /* C++ */\n\n')
            fh.write('/* This header file generated from one of the TPDS steps */\n')
            fh.write('/* Please do NOT make any changes to this file */\n\n')
            fh.write('/* -------------------------------------------------------------------------- */\n')
            fh.write('/* IMPORTS                                                                    */\n')
            fh.write('/* -------------------------------------------------------------------------- */\n\n')
            fh.write('/* -------------------------------------------------------------------------- */\n')
            fh.write('/* CONSTANTS, TYPES, ENUM                                                     */\n')
            fh.write('/* -------------------------------------------------------------------------- */\n\n')
            fh.write('/** @brief Wifi SSID for TrustManaged device */\n')
            fh.write(f'#define WIFI_SSID                           "{ssid}"\n\n')
            fh.write('/** @brief Wifi password for TrustManaged device */\n')
            fh.write(f'#define WIFI_PWD                            "{password}"\n\n')
            fh.write('/** @brief TrustManaged Device Public UID */\n')
            fh.write(f'#define KEYSTREAM_DEVICE_PUBLIC_PROFILE_UID "{pub_uid}"\n\n')
            fh.write('/** @brief keySTREAM COAP Endpoint */\n')
            fh.write(f'#define KEYSTREAM_COAP_URL                  (const uint8_t*)"{ks_coap_url}"\n\n')
            fh.write('/** @brief keySTREAM HTTP Endpoint */\n')
            fh.write(f'#define KEYSTREAM_HTTP_URL                  (const uint8_t*)"{ks_http_url}"\n\n')
            fh.write('/** @brief AWS Endpoint */\n')
            fh.write(f'#define AWS_ENDPOINT                        "{aws_endpoint}"\n\n')
            fh.write('/* -------------------------------------------------------------------------- */\n')
            fh.write('/* VARIABLES                                                                  */\n')
            fh.write('/* -------------------------------------------------------------------------- */\n\n')
            fh.write('/* -------------------------------------------------------------------------- */\n')
            fh.write('/* FUNCTIONS                                                                  */\n')
            fh.write('/* -------------------------------------------------------------------------- */\n\n')
            fh.write('#ifdef __cplusplus\n')
            fh.write('}\n')
            fh.write('#endif /* C++ */\n\n')
            fh.write('#endif // TMG_CONF_H\n\n')
            fh.write('/* -------------------------------------------------------------------------- */\n')
            fh.write('/* END OF FILE                                                                */\n')
            fh.write('/* -------------------------------------------------------------------------- */\n')

        fh.close()
        #Getting the dmuid from public profile uid
        keystream_endpoint = "https://" + keystream_endpoint
        url = f"{keystream_endpoint}/dm?dpPublicUid={pub_uid}"
        response = requests.get(url, headers=headers)
        dm = response.json()
        if 'totalRecords' in dm and dm['totalRecords'] == 0:
            raise Exception('Invalid public Profile UID!!!\n Please Provide Valid Device Fleet Profile Public UID in Step-2\n')
        if response.status_code != 200:
            check_inputs = ['Device Public UID', 'KeySTREAM Authorization Token and its Validity']
            if bool(check_inputs):
                check_inputs = '\n'.join(check_inputs)
                raise Exception(f'Request Failed!!!\nPlease check the following input parameters and retry:\n{check_inputs}.\n')
        
        dm = response.json()

        global dmuid
        dmuid = dm['deviceManagers'][0]['uuid']

        #Getting the Operational CA Name
        url = f"{keystream_endpoint}/dm/{dmuid}/business/deviceprofiles/desired?publicUid={pub_uid}&fields=zerotouch"

        response = requests.get(url, headers=headers)
        ca = response.json()
        global ca_name
        ca_name = ca['desiredProperties'][0]['zerotouch']['certificateAuthorityName']

        #Downloading CA Certificate

        print('Downloading CA Cert.....')

        url = f"{keystream_endpoint}/cm/dm/{dmuid}/certificateauthorities/{ca_name}"

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f'Downloading CA Cert Failed, Please provide valid input paramters in step 2.\n')
        ca_cert = response.json()
        print(ca_cert['certificate'])

        with open(f'{ca_name}_ca.pem', 'w') as f: 
            f.write("-----BEGIN CERTIFICATE-----\n")
            f.write(ca_cert['certificate'])
            f.write("\n-----END CERTIFICATE-----\n")

        print('Downloading CA certificate Done')
        
    def get_aws_code(self, b=None):

        print('Executing Step-4...')

        sys_shell = True if sys.platform == 'win32' else False
        print("Getting AWS Registration Code")
        subProcessOut = tpds.tp_utils.run_subprocess_cmd(
            cmd=[
                "aws", "iot", "get-registration-code",
                "--region", "us-east-2","--output=text"],
            sys_shell=sys_shell)

        if subProcessOut[0] != 0:
                raise Exception(f'Getting AWS Registration code Failed!!!\nError:{subProcessOut[2]}.\n')

        print("Registration Code: ", subProcessOut[1])
        if subProcessOut[1] == None:
            raise Exception(subProcessOut[1])

        #AWS registration Code
        global reg_code
        reg_code = subProcessOut[1]

    
    def get_pop(self, b=None):
        #Downloading Verification Certificate Certificate
        print('Executing Step-5...')

        print('Downloading PoP Cert from keySTREAM')

        url = f"{keystream_endpoint}/cm/dm/{dmuid}/certificateauthorities/{ca_name}/popcertificate/{reg_code}"

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f'Downloading PoP Cert Failed, Please provide valid input paramters in step 2.\n')
        pop_cert = response.json()
        print(pop_cert['popCertificate'])

        with open(f'{ca_name}_pop.pem', 'w') as f: 
            f.write(pop_cert['popCertificate'])

        print('Downloading PoP Certificate Done')


    def register_cert_to_aws(self, b=None):
        #Uploading Certificates to AWS
        print('Executing Step-6...')

        print("Uploading Signer Cert and Verification Cert To AWS")

        curr_path = os.getcwd()

        sys_shell = True if sys.platform == 'win32' else False
        subProcessOut = tpds.tp_utils.run_subprocess_cmd(
            cmd=[
                "aws", "iot", "register-ca-certificate",
                "--ca-certificate", f"file://{curr_path}\{ca_name}_ca.pem",
                "--verification-cert", f"file://{curr_path}\{ca_name}_pop.pem",
                "--set-as-active", "--allow-auto-registration", "--region",
                "us-east-2"],
            sys_shell=sys_shell)

        if "ResourceAlreadyExistsException" in subProcessOut[2]:
            print("Resource Already Exist!!!")

        if subProcessOut[0] != 0 and "ResourceAlreadyExistsException" not in subProcessOut[2]:
            raise Exception(subProcessOut[2])

        # Removing downloaded certificates
        os.remove(f"{ca_name}_ca.pem")
        os.remove(f"{ca_name}_pop.pem")
