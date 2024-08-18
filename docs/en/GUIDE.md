## Overview

<img src="./GUIDE-img/nhn-cloud.svg" width="90%" height="60%">

To register an NHN Cloud service account in Cloudforet, you need the settings information below. There are four types of Schemas.

* NHN Cloud Access Key
	* `Tenant ID`
	* `Username`
	* `Password`

* NHN Cloud APP Key
	* `APP Key`
	* `Email Secret Key (optional)`
	* `Push Secret Key (optional)`
  	* `User Access Key ID (optional)`
	* `Secret Access Key (optional)`

* NHN Cloud Certificate Manager APP Key
	* `Certificate Manager APP Key`
  	* `User Access Key ID`
	* `Secret Access Key`

* NHN Cloud Object Storage Access Key
	* `Object Storage Tenant ID`
	* `Username`
	* `Object Storage Password`
    * `Storage Account`



>💡 Before starting the setup guide, please make sure **NHN Cloud User** has been created.

See the NHN Guides [NHN Documentation](https://docs.nhncloud.com/en/nhncloud/en/user-guide/)

To collect NHN Cloud resources, you have to create a NHN Cloud Service account in Cloudforet.

<img src="./GUIDE-img/account-info-1.png" width="90%" height="60%">

Go to Service Account and click [NHN Cloud] to create a NHN Cloud Service account.

<img src="./GUIDE-img/account-info-2.png" width="90%" height="60%">

<img src="./GUIDE-img/account-info-3.png" width="90%" height="60%">

Select a Project for the Service Account.

<img src="./GUIDE-img/account-info-4.png" width="70%" height="60%">

Choose Secret Type Schema and insert the Input Forms.

<img src="./GUIDE-img/account-info-5.png" width="70%" height="60%">


This setup guide will take a closer look at what the above-mentioned information means and where to obtain it.
<br>

### Username
**Username** is the ID you use when you login into NHN Console IAM.
<br>

### Tenant ID
**Tenant ID** is a **unique identifier** for your organization provided by NHN Cloud Services.
Tenant ID is a cloud-based identity and access management service that you use to manage users on an organizational basis. It is used to manage IaaS resources and issuing tokens to access resources.
<br>

### Password
**Password** is the password you use for login in default. But you can manage to set password for paticular services such as Compute Instance or Object Storage.
<br>

### APP Key
**APP Key** is the key that can be obtained through NHN Cloud project management settings. Integrated project Appkey is applied for authentication of NHN Cloud Service.
Required when using NHN Cloud's API of PaaS resources.
<br>

### User Access Key ID
This is the User ID that is required for user authentication to use the NHN Cloud service.
Required when using RDS and Certificate Manager resources.
<br>

### Secret Access Key
This is the Secret Key that is required for user authentication to use the NHN Cloud service.
Required when using RDS and Certificate Manager resources.
<br>

### Storage Account
This is the **Account** that can be obtained through Object Storage Service.
Required when using Object Storage resources.
<br>

### Email Secret Key
This is the Secret Key that is required for Email resources.
<br>

### Push Secret Key
This is the Secret Key that is required for Push resources.
<br>

We briefly discussed the concept of setup information required when registering a Cloudforet NHN Cloud service account.
Now, let's learn more about **how to actually obtain configuration information** in the next lesson.

<br>

## How to obtain the keys

Cloudforet supports the **[NHN_client_secret]** method through issuing authentication keys for integration with NHN Cloud.
The method using **[NHN_client_secret]** requires the following setting information.

1. NHN Cloud Access Key (for IaaS)
	* `Tenant ID`
	* `Username`
	* `Password`

2. NHN Cloud Object Storage Access Key (for Object Storage service)
	* `Object Storage Tenant ID (from Object Storage)`
	* `Username`
	* `Object Storage Password (from Object Storage)`
	* `Storage Account`

3. NHN Cloud APP Key (for PaaS)
	* `APP Key`
	* `Email Secret Key (optional key for Email service)`
	* `Push Secret Key (optional key for Push service)`
  	* `User Access Key ID (optional key for RDS service)`
	* `Secret Access Key (optional key for RDS service)`

4. NHN Cloud Certificate Manager APP Key (for Certificate Manager service)
	* `Certificate Manager APP Key (from Certificate Manager service)`
  	* `User Access Key ID`
	* `Secret Access Key`

Choose a schema or schemas you are willing to obtain, and proceed with the following order for the Schemas.

<br>
<br>

## 1. NHN Cloud Access Key

* `Tenant ID`
* `Username`
* `Password`

(1) Log in to [NHN Cloud Console](https://id.nhncloud.com/login).

(1-1) Choose the project you are using and go to [Compute - Instance].
And then click [Set API Endpoint] button.

<img src="./GUIDE-img/access-key-info-1.png" width="90%" height="80%">

(1-2) Then, you can find your 'Tenant ID' here. You can also click on the [Modify] button to Set API 'Password'.
'Username' is the ID you use when you login into NHN Console IAM.

<img src="./GUIDE-img/access-key-info-2.png" width="90%" height="80%">

<br>
<br>

## 2. NHN Cloud Object Storage Access Key

* `Object Storage Tenant ID (from Object Storage)`
* `Username`
* `Object Storage Password (from Object Storage)`
* `Storage Account`

(2) Log in to [NHN Cloud Console](https://id.nhncloud.com/login).

(2-1) Choose the project you are using and go to [Storage - Object Storage].
And then click [Set API Endpoint] button.

<img src="./GUIDE-img/storage-access-key-info-1.png" width="90%" height="80%">

(2-2) Then, you can find your 'Object Storage Tenant ID' and 'Storage Account' here. You can also click on the [Modify] button to Set API 'Object Storage Password'.
'Username' is the ID you use when you login into NHN Console IAM.

<img src="./GUIDE-img/storage-access-key-info-2.png" width="90%" height="80%">

<br>
<br>

## 3. NHN Cloud APP Key

* `APP Key`
* `Email Secret Key (optional key for Email service)`
* `Push Secret Key (optional key for Push service)`
* `User Access Key ID (optional key for RDS service)`
* `Secret Access Key (optional key for RDS service)`

(3) Log in to [NHN Cloud Console](https://id.nhncloud.com/login).

(3-1) Choose the project you are using and click on the [Project Management] section.

<img src="./GUIDE-img/app-key-info-1.png" width="90%" height="80%">

(3-2) Integrated project Appkey is applied for authentication of NHN Cloud Service. You can create your APP Key here. When your APP Key is created, you will see the APP Key below.

<img src="./GUIDE-img/app-key-info-2.png" width="90%" height="80%">

(3-3) Email Secret Key is an optional key for Email service. Choose the project you are using and go to [Notification - Email].
And then click [URL & Appkey] button.

<img src="./GUIDE-img/app-key-info-3.png" width="90%" height="80%">

(3-4) Then, you can find your 'Email Secret Key' here. Make sure to use Integrated Appkey that we created at (3-2) and not to use Appkey for specific resource.

<img src="./GUIDE-img/app-key-info-4.png" width="90%" height="80%">

(3-5) Push Secret Key is an optional key for Push service. Choose the project you are using and go to [Notification - Push].
And then click [URL & Appkey] button.

<img src="./GUIDE-img/app-key-info-5.png" width="90%" height="80%">

(3-6) Then, you can find your 'Push Secret Key' here. Make sure to use Integrated Appkey that we created at (3-2) and not to use Appkey for specific resource.

<img src="./GUIDE-img/app-key-info-6.png" width="90%" height="80%">

(3-7) Click your name and API Security Setting at the top right corner.

<img src="./GUIDE-img/app-key-info-7.png" width="90%" height="80%">

(3-8) You can create your User Access Key ID and Secret Access Key here. When your User Access Key ID and Secret Access Key is created, you will see the them below.

<img src="./GUIDE-img/app-key-info-8.png" width="90%" height="80%">

<br>
<br>

## 4. NHN Cloud Certificate Manager APP Key

* `Certificate Manager APP Key (from Certificate Manager service)`
* `User Access Key ID`
* `Secret Access Key`

(4) Log in to [NHN Cloud Console](https://id.nhncloud.com/login).

(4-1) Choose the project you are using and click [Management - Certificate Manager].
And then click [URL & Appkey] button.

<img src="./GUIDE-img/certificate-app-key-info-1.png" width="90%" height="80%">

(4-2) Then, you can find your 'Certificate Manager APP Key' here. Make sure to use Certificate Manager APP Key for this schema and not to use Integrated Appkey that we created at (3-2). This is because Certificate Manager resource can not be called with Integrated Appkey.

<img src="./GUIDE-img/certificate-app-key-info-2.png" width="90%" height="80%">


If you can't find the service, go to [Service] to activate the service.

<img src="./GUIDE-img/service-info.png" width="90%" height="80%">