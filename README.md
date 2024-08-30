<h1 align="center">NHN Cloud Plugin - Inventory</h1>  
  
<br/>  
<div align="center" style="display:flex;">  
  <img width="300" src="https://static.toastoven.net/toast/resources/img/logo_nhn_cloud_color.svg">  
<p> <br>  
<a  href="https://www.apache.org/licenses/LICENSE-2.0"  target="_blank">  
<img  alt="License: Apache 2.0"  src="https://img.shields.io/badge/License-Apache 2.0-yellow.svg"  />  
</a>
</p>  
  
</div> 

`plugin-nhncloud-inven-collector` is an NHN Cloud inventory collector plugin for Cloudforet.


#### Plugin to collect NHN Cloud Services


> Cloudforet's [plugin-nhncloud-inven-collector](https://github.com/cloudforet-io/plugin-nhncloud-inven-collector) is a convenient tool to 
get cloud service data from NHN Cloud Services. 


Find us also at [Dockerhub](https://hub.docker.com/r/cloudforet/plugin-nhncloud-inven-collector)

Please contact us if you need any further information. 
<admin@cloudforet.io>


---

## Service List

<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <table>
        <thead>
            <tr>
                <th>Group</th>
                <th>Category</th>
                <th>Service</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td rowspan="4">Compute</td>
                <td rowspan="3">Instance</td>
                <td>Instance</td>
            </tr>
            <tr>
                <td>Key Pair</td>
            </tr>
            <tr>
                <td>Availability Zone</td>
            </tr>
            <tr>
                <td>Image</td>
                <td>Image</td>
            </tr>
            <tr>
                <td rowspan="2">Container</td>
                <td rowspan="2">NHN Kubernetes Service(NKS)</td>
                <td>Cluster</td>
            </tr>
            <tr>
                <td>Node Group</td>
            </tr>
            <tr>
                <td rowspan="31">Network</td>
                <td rowspan="3">VPC</td>
                <td>VPC</td>
            </tr>
            <tr>
                <td>Subnet</td>
            </tr>
            <tr>
                <td>Routing Table</td>
            </tr>
            <tr>
                <td>Floating IP</td>
                <td>Floating IP</td>
            </tr>
            <tr>
                <td rowspan="3">Network ACL</td>
                <td>Network ACL</td>
            </tr>
            <tr>
                <td>Network ACL Binding</td>
            </tr>
            <tr>
                <td>Network ACL Rule</td>
            </tr>
            <tr>
                <td rowspan="2">Security Group</td>
                <td>Security Group</td>
            </tr>
            <tr>
                <td>Security Rule</td>
            </tr>
            <tr>
                <td rowspan="10">Load Balancer</td>
                <td>Load Balancer</td>
            </tr>
            <tr>
                <td>Health Monitor</td>
            </tr>
            <tr>
                <td>IP ACL</td>
            </tr>
            <tr>
                <td>IP ACL Target</td>
            </tr>
            <tr>
                <td>L7 Policy</td>
            </tr>
            <tr>
                <td>L7 Rule</td>
            </tr>
            <tr>
                <td>Listener</td>
            </tr>
            <tr>
                <td>Member</td>
            </tr>
            <tr>
                <td>Pool</td>
            </tr>
            <tr>
                <td>Secret</td>
            </tr>
            <tr>
                <td rowspan="6">Transit Hub</td>
                <td>Transit Hub</td>
            </tr>
            <tr>
                <td>Attachment</td>
            </tr>
            <tr>
                <td>Multicast Domain</td>
            </tr>
            <tr>
                <td>Routing Table</td>
            </tr>
            <tr>
                <td>Shared Multicast Domain</td>
            </tr>
            <tr>
                <td>Shared Transit Hub</td>
            </tr>
            <tr>
                <td rowspan="2">Service Gateway</td>
                <td>Service Gateway</td>
            </tr>
            <tr>
                <td>Service Endpoint</td>
            </tr>
            <tr>
                <td rowspan="4">DNS Plus</td>
                <td>DNS Zone</td>
            </tr>
            <tr>
                <td>Health Check</td>
            </tr>
            <tr>
                <td>GSLB</td>
            </tr>
            <tr>
                <td>Pool</td>
            </tr>
            <tr>
                <td rowspan="4">Storage</td>
                <td rowspan="3">Block Storage</td>
                <td>Block Storage</td>
            </tr>
            <tr>
                <td>Block Storage Snapshot</td>
            </tr>
            <tr>
                <td>Block Storage Type</td>
            </tr>
	    <tr>
                <td>Object Storage</td>
		<td>Container</td>
            </tr>
            <tr>
                <td rowspan="14">Database</td>
                <td rowspan="7">RDS For MySQL</td>
                <td>DB Instance</td>
            </tr>
            <tr>
                <td>DB Instance Group</td>
            </tr>
            <tr>
                <td>Backup</td>
            </tr>
            <tr>
                <td>DB Security Group</td>
            </tr>
            <tr>
                <td>Notification Group</td>
            </tr>
            <tr>
                <td>Parameter Group</td>
            </tr>
            <tr>
                <td>User Group</td>
            </tr>
            <tr>
                <td rowspan="7">RDS For MariaDB</td>
                <td>DB Instance</td>
            </tr>
            <tr>
                <td>DB Instance Group</td>
            </tr>
            <tr>
                <td>Backup</td>
            </tr>
            <tr>
                <td>DB Security Group</td>
            </tr>
            <tr>
                <td>Notification Group</td>
            </tr>
            <tr>
                <td>Parameter Group</td>
            </tr>
            <tr>
                <td>User Group</td>
            </tr>
            <tr>
                <td rowspan="5">Notification</td>
                <td rowspan="2">Push</td>
                <td>Tag</td>
            </tr>
            <tr>
                <td>Token</td>
            </tr>
            <tr>
                <td rowspan="3">Email</td>
                <td>Tag</td>
            </tr>
            <tr>
                <td>Category</td>
            </tr>
            <tr>
                <td>Template</td>
            </tr>
            <tr>
                <td rowspan="3">Application Service</td>
                <td rowspan="3">API Gateway</td>
                <td>Service</td>
            </tr>
            <tr>
                <td>API Key</td>
            </tr>
            <tr>
                <td>Usage Plan</td>
            </tr>
            <tr>
                <td>Management</td>
                <td>Certificate Manager</td>
                <td>Certificate</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
    
---

## SETTING
You should insert information about account in Cloudforet's **Service Account** initially. There are four Secret Type schemas.
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
   
---

## Comprehensive Guide on Utilizing the NHN Plugin
#### [English guide for NHN Plugin](./docs/en/README.md)
#### [Korean guide for NHN Plugin](./docs/ko/README.md)
