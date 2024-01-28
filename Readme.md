# Drive Monitor

## Overview

The purpose of this script is to monitor your Google Drive account for any publicly visible folders and make them private.

## Usage:

In order to run the script you need to create a Google Cloud application token, here is how to do it:

* Create a project at this URL: https://console.cloud.google.com/projectcreate
* Once the project is created, enable these APIs:
  * Google Drive API: https://console.cloud.google.com/marketplace/product/google/drive.googleapis.com
  * Google Drive Activity API: https://console.cloud.google.com/marketplace/product/google/driveactivity.googleapis.com
  * First we need to configure the consent screen:
    * Go to this page: https://console.cloud.google.com/apis/credentials/consent
    * Select "External" (That's what I had available)
    * Click: "Create"
    * Enter "App Name" and "User support email" as well as "Developer contact information"
    * Click: "Save and continue"
    * Click: "ADD OR REMOVE SCOPES"
      * add these scopes: https://www.googleapis.com/auth/drive.activity.readonly, https://www.googleapis.com/auth/drive
    * Click "Save and continue"
    * Again Click "Save and continue"
    * Now click "Publish App" so that it can be used
  * Now create an OAuth token:
    * Go to: https://console.cloud.google.com/apis/credentials
    * Click: "+ Create Credentials" > "Oauth Client ID"
    * In "Application Type" select "Desktop App" and give it a name
  * Now download the credential secrets file and save it as credentials.json

Install the requirements

```bash
python3 -m pip install -r requirements.txt
```


Run the script:

```bash
usage: main.py [-h] [-p]

A script that monitors and protect public folders in google drive.

optional arguments:
  -h, --help       show this help message and exit
  -p, --use_proxy  Use a proxy (default: 127.0.0.1:8080)
```

Next log into your Google account when the screen pops up. Note: you'll need to do this twice, because we use 2 different APIs.

### Sample Output:
```
[+] No new files
[-] File 1VMKIeQLN1uQAYVO1bjYhnsJUFVtaHnce -> File created but not public yet
[-] File 1VMKIeQLN1uQAYVO1bjYhnsJUFVtaHnce -> Now It's public
[-] File is a public folder - making private! -> Try to make it private
[-] Folder is now private -> Success!
[-] File 1oE2qr4aIsuYWDGX0uIefZenjjbZ2eQKp
[-] File is a public folder - making private!
[-] Folder is now private
[-] File 1oE2qr4aIsuYWDGX0uIefZenjjbZ2eQKp
```

## Use Notes

### Scopes

I tried using the most minimal scopes that I could, this came out to:

https://www.googleapis.com/auth/drive.activity.readonly - used to read the users drive activity
https://www.googleapis.com/auth/drive - used to change file permissions (this is a pretty privileged scope)

### Functionality

Finding created files can be done in a few ways, for example we can list all the files in the drive, however this would take way to long.
Therefor this script utilizes the Google Drive activity monitor.

I chose to protect every file that popped up in the activity monitor, I found this was more effective than filtering for created files.
This is because files can become public in many ways (shared, moved etc.)

I tried to figure out how to get the user's default sharing settings, but I could only find mentions of this for enterprise accounts.
So I checked my account's settings page and found that I don't have a setting like this.

This is weird because according to this forum answer https://support.google.com/drive/thread/236878577/default-share-setting?hl=en the setting should exist. Maybe it's depricated?

If this did exist than any app that can change the file can set the default share setting to public and leak files.

## Additional Thoughts

### Token Security

An obvious problem with API's is stolen / leaked tokens, if someone steals the token (or it is accidentally committed to a public git repo) a malicious party can misuse it.

### Folder Permissions

When creating a file in a folder owned by another user. The owner immediately gets Editor permissions. This means a root folder owned by a compromised user account can compromise all the child items.

### Sharing Permissions

When sharing a file or folder the default behaviour is to allow Editors to share the file, this means they can make the file public.

### Ideas For Future Research

* Enterprise accounts support search across the whole domain, this can probably be used to find public files.
  * I couldn't find a way to get a users public files using the search function
  * Even though you can get a user's share id using this endpoint https://developers.google.com/drive/api/reference/rest/v2/permissions/getIdForEmail
* To add permissions to a file, you either need the https://www.googleapis.com/auth/drive scope that I use in this script, or the  https://www.googleapis.com/auth/docs
scope. Maybe this scope is easier to obtain...
* Look into expiry for sharing, you can probably abuse it
* Try to create interesting capability situations... (tried a bit and couldn't think of anything)
