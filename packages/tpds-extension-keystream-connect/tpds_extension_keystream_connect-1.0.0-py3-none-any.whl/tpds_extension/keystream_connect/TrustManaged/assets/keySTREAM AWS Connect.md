# Trust Platform Design Suite - Use Case Help - Trust MANAGER and keySTREAM SaaS

This guide provides a clear step-by-step process for onboarding an ECC608 Trust Manager with the KeySTREAM SaaS from Kudelski IoT ("keySTREAM"), operating on AWS. It's important to note that manual secure exchange processes are not required with this onboarding methodology. The customized PKI is preconfigured in KeySTREAM, and the device certificate is linked a posteriori, when the device is deployed in the field.

### During the evaluation of the ECC608 TrustMANAGER and keySTREAM from Kudelski IOT, you will be guided through
 - Creating a microchip e-commerce account
 - Creating a keySTREAM account
 - Registering the microchip e-commerce email account to keySTREAM
 - Creating an AWS IoT account
 - Creating your root CA within keySTREAM 
 - Using Trust Platform Design Suite to onboard the development kit from Microchip into keySTREAM
 - Completing the in-field provisioning of the ECC608Trust MANAGER
 - Operating certificate management operations remotely from keySTREAM

## Setup Requirements
1. Acquire the [DM320118](https://www.microchip.com/developmenttools/ProductDetails/DM320118) CryptoAuth Trust Platform development kit.
2. Purchase the [WIFI 7 CLICK](https://www.mikroe.com/wifi-7-click) (WINC1500 or WINC1510 Wifi module) from mikroe.com.
3. Download and Install [MPLAB X IDE](https://www.microchip.com/en-us/development-tools-tools-and-software/mplab-x-ide) version 6.15 or above.
4. Connect DM320118 board to PC running Trust Platform Design Suite. 
5. Connect WIFI7 clickboard onto DM320118 by making sure the chamfer is aligned with the silkscreen indicator of the DM320118.

## Configuration Steps
1. Ensure **MPLAB X Path** is set in TPDS under **File** -> **Preference** -> **System Settings**. <br>
This setup facilitates:
    - Programming the Use Case prototyping kit to factory reset application by TPDS.
    - Opening the embedded project of the use case.
    - Note: Microchip/Atmel Studio must be installed on the system, and this tool is compatible only with MS Windows.
2. Additional Notes:<br>
     Some versions of DM320118 nEDBG firmware may fail to upgrade WINC software. In such cases, follow these steps
    - From the Microchip Studio Command Prompt, 
    - Navigate to the ~/.trustplatform/winc_firmware_upgrade folder, as shown in figure #001
    <figure style="text-align: center;"><img src="images/winc_firmware_update.png" style="width: 35%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 35%;">Figure 001</figcaption></figure>
    - Upgrade the firmware to version 1.18.528 ; run the following command:<br>
			**atfw -t nedbg -a nedbg_fw-1.18.528.zip**, as shown in figure #002.
    <figure style="text-align: center;"><img src="images/winc_firmware_upgrade.png" style="width: 55%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 55%;">Figure 002</figcaption></figure>
    - Note: The WINC firmware upgrade process may take a few minutes; please wait for it to complete.
----------------------------------------------  --------------------------------------------------------------------------------------------

## Pre Use Case Transaction Steps

- Before proceeding with the use case transaction diagram, certain pre-setup steps must be completed.
 
### keySTREAM Account Setup and Requirements

  - You must have an account on Kudelski's keySTREAM portal to proceed with the use case. Registration is free and can be completed via [this link](https://mc.obp.iot.kudelski.com)
  - Upon completing the registration process, you will gain access to your own tenant on the keySTREAM SaaS platform from Kudelski IoT.

### Signing in on keySTREAM portal

To sign in to the keySTREAM portal, please locate the link provided in the email from "Kudelski IoT Onboarding Portal" confirming the creation of your keySTREAM tenant. This email includes comprehensive instructions, so ensure you review it carefully.

For the upcoming steps, it's essential to be signed in to the keySTREAM portal.

### Obtaining an API key

From keySTREAM portal, you can generate an APIkey that you'll need later on. Here is how to obtain it:
  - On the left panel, click on "System", then on the tab "API KEYS".
  - On the right hand side, click on **CREATE**.
  - The Create API Key popup window appears :
      <figure style="text-align: center;"><img src="images/create_api_key.png" style="width: 65%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 65%;">Figure 003</figcaption></figure>
  - The Name field can be freely chosen.
  - The Role to be selected here is **Devices Administrator** (aka **dmAdmin**)
  - The Validity can be specified in hours or left empty, in which case the API key will never expire.<br>
  - Click **Commit** to create the API key, which will appear in the list of API keys.<br>

Locate the API key that you just created, in the list, and on the Action column, click the pencil icon (tooltip: **Edit**):
      <figure style="text-align: center;"><img src="images/list_api_keys.png" style="width: 65%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 65%;">Figure 004</figcaption></figure>
A popup window appears, **Edit Api Key**:
      <figure style="text-align: center;"><img src="images/edit_api_key.png" style="width: 65%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 65%;">Figure 005</figcaption></figure>

The API key that is expected in this use case is the value in the field "Basic Credentials". Unmask it by clicking on the eye button on the right, then copy/paste it somewhere for later use. You can also click the **DOWNLOAD CREDENTIALS** button; the downloaded file contains the same "BasicCredentials" field, among other metadata.

Do NOT initiate the TPDS use case before obtaining the token from Kudelski IoT; it is a mandatory entry in the TPDS use case.

### Creating a Fleet Profile

A Fleet profile
  - Is a label attached to a set of devices sharing the same configuration.<br>
  - Serves as a link between you, the device manufacturer, and the device you’ll have in the field.<br>
  - Will be referenced both on keySTREAM and in your device’s firmware.<br>
  - Is identified by a Fleet Profile Public UID that is easily readable by a human, as further explained below.<br>

The keySTREAM UI allows to create a Fleet Profile and attach a configuration to it:

- Click on **Fleet Management** from left panel as shown in below figure #006.<br>
    <figure style="text-align: center;"><img src="images/fleet_mgmt.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 006</figcaption></figure>

- Click on **CREATE** as shown in figure #007.
    <figure style="text-align: center;"><img src="images/create_profile.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 007</figcaption></figure>
- A popup window appears :
    <figure style="text-align: center;"><img src="images/profile_details.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 008</figcaption></figure>

  -  The following fields can be configured :
     - **Fleet Profile Public Uid (required) :** 
        A unique URI string, identifying the Fleet Profile. It is advised to avoid creating two Fleet Profiles with the same name. The final Fleet Profile Public Uid would be a concatenation of an auto-generated prefix (e.g. 9S4F:) and the Fleet Profile Public Uid (example.org:dp:network:device) that has been defined. The final Fleet Profile Public Uid would look like 9S4F:example.org:dp:network:device.
     - **Model, Brand and Manufacturer:** they’re optional and purely informational, for your own use.
     - **Usage of non sealed fleet profile public uid is authorized (optional):** By default this option is 'disabled'. For more information on **non sealed fleet profile public uid** Navigate to Documentation page from left panel on keySTREAM UI and Click on keySTREAM microchip documentation.Then navigate to Workflows tab and then click on Multi Fleet Profiles.

- Upon clicking on **NEXT**, you can create your own Root Certificate Authority (CA) associated with this new Fleet Profile:
    <figure style="text-align: center;"><img src="images/configure_ca.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 009</figcaption></figure>
  
  - The following fields can be configured :
     - **Root CA Common Name (CN):** This field is restricted to a fixed length of 16 Bytes. In case your input is shorter, it will be right-padded with spaces; a longer input will be truncated.

     - **Root CA Organization (O):** This field is restricted to a fixed length of 16 Bytes. In case your input is shorter, it will be right-padded with spaces; a longer input will be truncated. Notice that the Organization Unit will be hardcoded to TrustMANAGER.

     - **Root CA Certificate Validity(Years):** Number of Year(s) of validity of the Root CA.
   
     - **Device Operational Certificate validity (Years):** The number of Year(s) of validity of the Device Operational Certificate. It shall be shorter than the RooT CA Certificate validity.
   
  - After you click on **COMMIT**, a newly configured Fleet Profile with its freshly created Root CA appears in the list below: 
    <figure style="text-align: center;"><img src="images/device_profile_list.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 010</figcaption></figure>

  - All devices that are configured with this Fleet Profile will be provisioned with a unique device certificate signed by the certificate authority (CA) associated to this Fleet Profile when they register on keySTREAM.

------------------------------------------------------------------------------------------------------------------------------------------

### AWS Setup Requirements

**AWS Account Setup Instructions:**

In order to run the AWS Cloud Connect Use Cases, an AWS account is required. This document describes the steps required to obtain and configure an AWS account for the demo.

[Amazon Web Services (AWS)](https://aws.amazon.com/) provides computing services for a fee. Some are offered for free on a trial or small-scale basis. <br>
By signing up for your own AWS account, you are establishing an account to gain access to a wide range of computing services.

Think of your AWS account as your root account to AWS services. It is very powerful and gives you complete access. Be sure to protect your username and password.You control access to your AWS account by creating individual users and groups using the Identity and Access Management (IAM) Console. From the IAM Console, you also assign policies (permissions) to the group.

**Create your own AWS account**

 1. Create AWS account
  
    - Go to [AWS account](https://aws.amazon.com/) and follow instructions to create your own AWS account.<br>
    
    - Additional details can be found at [AWS Account Creation and Activation Guide](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/).

 1. Secure root account with MFA (multi-factor authentication)

    This is an important step to better secure your root account against attackers. <br>
    Anyone logging in not only needs to know the password, but also a constantly changing code generated by an MFA device.

    AWS recommends a number of MFA device options at the following link: [MFA device options](https://aws.amazon.com/iam/details/mfa/)

    The quickest solution is a virtual MFA device running on a phone. These apps provide the ability to scan the QR code AWS will generate to set up the MFA device.

    1. Return to [AWS account](https://aws.amazon.com/) and click the **Sign In to the Console**
    2. If it asks for an IAM user name and password, select the **Sign-in using root account credentials** link.
    3. Enter the email and password for your AWS account.
    4. Under **Find Services** search for **IAM** and select it to bring up the Identity and Access Management options.
    5. Click on **Activate MFA (Multi-factor Authentication) on your root account**

 1. Create an admin IAM user AWS best practices recommend not using your root account for standard administrative tasks, <br>
 but to create a special admin user for those tasks. See [Best Practices for Securing AWS IAM Credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#lock-away-credentials)

 1. Follow the instructions at [Creating an AWS IAM Admin Group](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html) for creating an admin user.

 2. Enable MFA (multi-factor authentication) for the admin user. <br>
 See [AWS IAM Best Practices: Enable MFA for Privileged Users](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#enable-mfa-for-privileged-users)

**AWS CLI**

  - AWS CLI is already installed during the TPDS installation.

**Get AWS Access Key and AWS Secret Access Key**

  - Follow this link and get the AWS Access Key and Secret Key [**AWS Access Keys**](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html)

**Configuring the account using CloudFormation Templates**

The usage of a custom PKI with TrustFLEX devices uses the Just-In-Time Registration (JITR) feature of AWS IoT Core. <br>
This feature requires a number of resources setup with an AWS account to work. The creation of these resources is automated through the AWS CloudFormation service.

1. Sign into the [AWS console](https://aws.amazon.com/) using the admin user created in the previous section.
2. Change to region to **US East (Ohio)** (a.k.a. us-east-2). This is done from a dropdown in the top right of the console webpage after logging in.
3. Under **Find Services** search for **CloudFormation** and select it to bring up that service.
4. Click **Create Stack** button.
5. Select **Upload a template file** from the page of the stack creation.
6. Click **Choose file** and upload the **aws-zero-touch-full-setup.yaml** file. Note, if running from a China region, you'll need to select the <br> 
    **aws-zero-touch-full-setup-cn.yaml** instead. These files are available in ~/.trustplatform folder.
7. Click **Next** to move on to the stack details.
8. Enter **TrustFLEX** as the stack name. Actual name isn't important, just has to be unique.
9. Enter a password for the user that will be created to run the demo under **UserPassword**. It's important the password has small characters, <br>
   capitals, numbers and at least 1 special character.
10. Click **Next** to move on to the stack options. Nothing needs to be changed here.
11. Click **Next** to move on to the stack review.
12. Check the acknowledgement box regarding IAM resources at the bottom of the page.
13. Click **Create Stack** to start the resource creation.
14. Wait until the stack creation completes. This can take a few minutes. Once done, the stack your created will show as CREATE_COMPLETE.
15. Save demo credentials. Click the **Outputs** tab for the stack to see the credentials to be saved.

------------------------------------------------------------------------------------------------------------------------------------------
### Use Case Transaction Steps

- While providing inputs in the following steps, ensure that you do not introduce any spaces.

- **Providing Pre Config Inputs:**

      - To proceed, click on step-1, to generate manifest lite the device should be factory reset,Click **OK** to factory reset, This action may take few minutes. Please wait until you see a status pop. as shown in Figure #011.1
  <figure style="text-align: center;"><img src="images/factory_completed.png" style="width: 65%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 65%;">Figure 011.1</figcaption></figure>

      - Factory Reset completed, follow the steps, as shown in Figure #011.2.
  <figure style="text-align: center;"><img src="images/disconnect_connect.png" style="width: 65%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 65%;">Figure 011.2</figcaption></figure>

      - A Manifest Lite will be generated, displaying its path, then click "OK", as shown in Figure #011.3.
  <figure style="text-align: center;"><img src="images/generated_path.png" style="width: 65%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 65%;">Figure 011.3</figcaption></figure>
  
      - Uploading a Manifest File which is generated in keySTREAM, Click on **Device Ownership** from left panel, as shown in Figure #011.4.
  <figure style="text-align: center;"><img src="images/device_Ownership.png" style="width: 65%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 65%;">Figure 011.4</figcaption></figure>

     - Click on **DEVICE CLAIMING**, You can claim devices by importing a Manifest File containing a list of devices (identified by their ChipUid). As shown above, click on **Choose File** under the  Manifest option and then click on **IMPORT**, as shown in Figure #011.5.
  <figure style="text-align: center;"><img src="images/claim_devices.png" style="width: 65%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 65%;">Figure 11.5</figcaption></figure>

    - Then click on step-2, as shown in Figure #012.
  <figure style="text-align: center;"><img src="images/tpds_steps_config.png" style="width: 65%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 65%;">Figure 012</figcaption></figure>

    - The following dialog box will open, as shown in Figure #013.
  <figure style="text-align: center;"><img src="images/edit_configuration.png" style="width: 65%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 65%;">Figure 013</figcaption></figure>

    - If clicked OK the following window opens, as shown in Figure #014.
  <figure style="text-align: center;"><img src="images/pre_config_input_selection.png" style="width: 50%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 50%;">Figure 014</figcaption></figure>

    - Select "Fleet Profile Public UID", as shown in Figure #015.
  <figure style="text-align: center;"><img src="images/drop_down.png" style="width: 50%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 50%;">Figure 015</figcaption></figure>

    - Refer the  keySTREAM UI, go to **Fleet Management** as shown in figure #016.
  <figure style="text-align: center;"><img src="images/fleet_mgmt.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 016</figcaption></figure>

    - Locate the "Fleeet Profile Public UID" you previously created as shown in figure #017.
  <figure style="text-align: center;"><img src="images/device_profile_list.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 017</figcaption></figure>

    - Populate the "Fleet Profile Public UID in TPDS", click OK as shown in figure #018.
  <figure style="text-align: center;"><img src="images/provide_uid_tpds.png" style="width: 50%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 50%;">Figure 018</figcaption></figure>

    - Then select "WiFi SSID". This the name of the WiFi hotspot/gateway you will connect to. Note that in a corporate network port 443 is blocked and messages from the demo will not go through, as shown in figure #019.
  <figure style="text-align: center;"><img src="images/wifi_ssid.png" style="width: 50%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 50%;">Figure 019</figcaption></figure>

    - Then give Wi-Fi passowrd, as shown in figure #020.
  <figure style="text-align: center; "><img src="images/WIFI_Password.png" style="width: 50%; display: block;" /><figcaption style="font-weight: bold; text-align: center;clear: both; width: 50%;">Figure 020</figcaption> </figure>

    - Then, enter the keySTREAM authorization token. To obtain a keySTREAM token, send another email to iot.ops@nagra.com requesting your "keySTREAM token" as shown in figure #021.
  <figure style="text-align: center;"><img src="images/authorization_token.png" style="width: 50%; display: block;" /><figcaption style="font-weight: bold; text-align: center;clear: both; width: 50%;">Figure 021</figcaption> </figure>

      - Then, enter Aws Access Key ID, as shown in figure #022.
  <figure style="text-align: center;"><img src="images/aws_access_key_id.png" style="width: 50%; display: block;" /><figcaption style="font-weight: bold; text-align: center;clear: both; width: 50%;">Figure 022</figcaption> </figure>

    - Then enter your AWS access key, which you will find in the stack created in CloudFormation in the OUTPUTS tab, as shown in the figure #023.
  <figure style="text-align: center;"><img src="images/aws_secret_access_key_id.png" style="width: 50%; display: block;" /><figcaption style="font-weight: bold; text-align: center;clear: both; width: 50%;">Figure 023</figcaption> </figure>

    - Do the same for the AWS Secret Access Key (suggestion change ID by key), as shown in figure 024.
  <figure style="text-align: center;"><img src="images/aws_secret_access_key.png" style="width: 50%; display: block;" /><figcaption style="font-weight: bold; text-align: center;clear: both; width: 50%;">Figure 024</figcaption> </figure>

    - Enter the region of your AWS server, as shown in figure #025.
  <figure style="text-align: center;"><img src="images/region.png" style="width: 50%; display: block;" /><figcaption style="font-weight: bold; text-align: center;clear: both; width: 50%;">Figure 025</figcaption> </figure>

     - Select this Option if All Inputs are Provided and Click on **OK**, as shown in figure #026.
  <figure style="text-align: center;"><img src="images/apply_all_settings.png" style="width: 50%; display: block;" /><figcaption style="font-weight: bold; text-align: center;clear: both; width: 50%;">Figure 026</figcaption> </figure>
     - If any changes are made to the pre-configuration later, select **Apply All Settings** and proceed. 
     - Then click on each step from step 3 - 6. 
     
     - Once all the tpds steps are done, Click on the **MPLAB X Project** to load the project in MPLAB X IDE as shown in figure #027.
  <figure style="text-align: center;"><img src="images/mplab.png" style="width: 65%; display: block;" /><figcaption style="font-weight: bold; text-align: center;clear: both; width: 65%;">Figure 027</figcaption> </figure>

 - **Possible Errors**

   - If "CANCEL" is clicked at the beginning step without filling in the configuration details, the window below will pop up as shown in figure #028.
  <figure style="text-align: center;"><img src="images/input_error.png" style="width: 60%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 60%;">Figure 028</figcaption></figure>

   - After clicking STEP2, this error comes up, there is a problem with how the AWS account was setup, An error occurred (UnrecognizedClientException). when calling the DescribeEndpoint operation: The security token.<br> included in the request is invalid. as shown in figure #029.
  <figure style="text-align: center;"><img src="images/aws_failed.png" style="width: 60%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 60%;">Figure 029</figcaption></figure>

    - Go to the "IAM" service, as shown in figure #030.
    <figure style="text-align: center;"><img src="images/iam_dashboard.png" style="width: 55%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 55%;">Figure 030</figcaption></figure>
    - Click on Users and verify your are not ALREADY using a user name identical to the  as a user name Cloudformation is tryting to  create. If it's identical, change the new user name or delete the old one. You might have this user name setup from the AWS IoT TPDS  use case already.It's possible you tested the AWS IoT Trust&GO orTrustFLEX use case in the past and this user was created.cloudformation is trying to create a new user which conflicts with the old user name and associated parameters,
    best is to delete the old user name.

------------------------------------------------------------------------------------------------------------------------------------------
## Enabling KTA Debug Logs.
- While Excuting these steps mentioned below, will enable Kta Debug Logs.
    - STEP 1: Navigate to Projects tabs, Right click on the project you want to excute, and set as main project, as shown in figure #031.
  <figure style="text-align: center;"><img src="images/project_tab.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 031</figcaption></figure>
    - STEP 2: Navigate to the menu bar, Click on the Files and Navigate and click on the **Project Properties**, as shown in figure #0032.
  <figure style="text-align: center;"><img src="images/project_properties.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 032</figcaption></figure>
    - Step 3: Under Categories, Navigate to the XC32(Global Options) and select the **xc32-gcc**, as shown in figure #0033.
  <figure style="text-align: center;"><img src="images/categories.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 033</figcaption></figure>
    - STEP 4: Select the Option catergories, in the dropdown select the **processing and message**, as shown in figure #0034.
  <figure style="text-align: center;"><img src="images/categories_options.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 034</figcaption></figure>
    - STEP 5: After selecting the Preprocessing and messages, Navigate to the **Preprocessor macros** and click as shown in figure, as shown in figure #0035.
  <figure style="text-align: center;"><img src="images/macros.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 035</figcaption></figure>
    - STEP 6: After selecting the **Preprocessor macros** options, Slect the **Enter string here** and type **LOG_KTA_ENABLE=1** and Select **ok**, as shown in figure #036.
  <figure style="text-align: center;"><img src="images/macros_options.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 036</figcaption></figure>
    - STEP 7: Under Categories tab, Naviagate to **Files Inclusion/Exclusion**, click on **>** to Included Files to Excluded Files and select **Apply** and click **OK**, Log will be enabled, as shown in figure #0037.
  <figure style="text-align: center;"><img src="images/Files_properties.png" style="width: 75%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 75%;">Figure 037</figcaption></figure>
    - STEP 8: KTA has moduleLevel Logs which can be enabled by the User as per their requirements.
        - Navigate to **KTALog.c**.
        - change the moduleLevelConfig as per the requirements for the required module as shown in figure #038.
        - **E_KTALOG_LEVEL_DEBUG** -> Enables the Debug Log Info.
        - **E_KTALOG_LEVEL_ERROR** -> Enables the Error Log Info.
  <figure style="text-align: center;"><img src="images/kta_log.png" style="width: 60%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 60%;">Figure 038</figcaption></figure>
------------------------------------------------------------------------------------------------------------------------------------------

## Post Use Case Transaction Steps
On completing Use Case steps execution on TPDS, it is possible to either run the embedded project or view C source files by clicking *MPLAB X Project* or *C Source Folder* button.

- Once the Usecase project is loaded on MPLAB X IDE,
    - Set the project as Main -> right click on Project and select **Set as Main Project**
    - Set the configuration -> right click on Project, expand **Set Configuration** to select **keySTREAM_AWS_CONNECT_COAP** or **keySTREAM_AWS_CONNECT_HTTP**
    - Build and Program the project -> right click on Project and select **Make and Program Device**
- Log from the embedded project can be viewed using applications like TeraTerm. Select the COM port and set baud rate as 115200-8-N-1

**Example TeraTerm Logs after successfully executing embedded project:**

 - **keySTREAM log During Embedded run (figure #039).**
  <figure style="text-align: center;"><img src="images/activated_message.png" style="width: 60%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 60%;">Figure 039</figcaption></figure>

 - **AWS log During Embedded run (figure #040).**
  <figure style="text-align: center;"><img src="images/provisioned_message.png" style="width: 60%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 60%;">Figure 040</figcaption></figure>

 - **Connecting to Cloud messages appear along with the led state (figure #041).**
  <figure style="text-align: center;"><img src="images/aws_ttlog.png" style="width: 60%; display: block;" /><figcaption style="font-weight: bold; text-align: center; clear: both; width: 60%;">Figure 041</figcaption></figure>

