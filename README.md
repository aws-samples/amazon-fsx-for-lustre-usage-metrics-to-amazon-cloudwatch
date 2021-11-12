# Publishing quota utilization on FSxL storage to Amazon CloudWatch
The fsxlcw software sends Amazon FSxL (FileSystem for Lustre) quota/limit and usage metrics to Amazon CloudWatch.  
**Metrics:**
- Per every user/group read from the system database (i.e.: /etc/passwd, /etc/groups):  
  - Kilobytes: disk space used
  - Files: number of i-nodes (number of files/directories)
  - Percentage over the soft (quota) limit: kilobytes/soft-quota-limit
  - Percentage over the hard (quota) limit: kilobytes/hard-quota-limit
  - Percentage over the soft i-node (quota) limit: files/soft-inode-quota-limit
  - Percentage over the hard i-node (quota) limit: files/hard-inode-quota-limit  

More info about FSxL quota settings at
[this documentation page](https://docs.aws.amazon.com/fsx/latest/LustreGuide/lustre-quotas.html)  


## Introduction
Amazon FSxL can manage user/group quota and can enforce limits on user/group quota usage.  

The metric data about user/group quota usage and limit are not collected automatically by AWS. There can be cases in 
which a customer might want:
- to monitor FSxL usage, 
- to compare the usage to the quota-limit assigned to a user/group (usage percent over quota-limit)
- to notify storage service administrators about the service usage (occupied disk space, percent over quota-limit)
- trigger other actions (i.e. Amazon EventBridge actions)
The fsxlcw software enables Amazon FSxL customers to do all the above, by making available to Amazon CloudWatch, metric 
data about Amazon FSxL usage.


## Common Use-Case
### Problem
An Amazon FSxL customer want to have metric data about the service usage in Amazon CloudWatch.
### Solution
1. Install fsxlcw on the EC2 instance where the Amazon FSxL is mounted (see *Prerequisites*).
2. Set a crontab-job that run the command every 5 minutes:
  ```
  crontab -e
  */5 * * * *     sudo /usr/local/bin/fsxl-2cw  # Run every 5 minutes
  ```
The metric data about Amazon FSxL usage will be sent to Amazon CloudWatch every 5 minutes.  
Then, it will also be possible to build Amazon CloudWatch dashboards and visualize the data and trigger Amazon EventBridge 
actions based on the available Amazon CloudWatch metrics.


## Disclaimer
fsxlcw exposes EC2 users and groups names in Amazon CloudWatch, in the metric's dimension names.

## Install
### Prerequisites
- EC2 instance with: 
  - the Lustre Client installed  
    [Here you can find a guide about how-to install the Lustre client](https://docs.aws.amazon.com/fsx/latest/LustreGuide/install-lustre-client.html)
  - An attached IAM Role with the following permission:
  ```
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Sid": "mysid",
              "Effect": "Allow",
              "Action": "cloudwatch:PutMetricData",
              "Resource": "*"
          }
      ]
  }
  ```
  - Python 3
  - A mounted Amazon FSxL disk
  

From source code:
```
$ git clone repourl
$ cd repodir
$ sudo python3 setup.py install
```

## Configure
Once installed, the configuration can be found in: 
```<path-to-package>/fsxlcw/conf/conf.yaml```.  
To locate the <path-to-package>, run 
```pip show fsxlcw```

Settings:  
```
log_level: DEBUG|INFO|WARNING|ERROR|CRITICAL
log_to_file: False|/absolute/path/to/log/file  # if not false, it will attempt to write into the specified file.
```


## Run
```
$ sudo /usr/local/bin/fsxl-2cw
```
The package should run on a EC2 instance, with at least one mounted FSxL filesystem.

### Test
1. Launch an EC2 instance using *Amazon Linux 2 AMI*.
2. Create a IAM role with the following permission:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "sid0",
            "Effect": "Allow",
            "Action": "cloudwatch:PutMetricData",
            "Resource": "*"
        }
    ]
}
```
3. Attach the role to the EC2 instance.
4. Create an FSxL filesystem.
5. Attach (mount) the FSxL filesystem to the EC2 instance.
6. Install the python package fsxlcw.
7. Set some quota limits for the mounted FSxL filesystem
   Example: ```sudo lfs setquota -u ec2-user -b 5000000 /mounted/directory```
8. Fill some disk space 
```
$ sudo /usr/local/bin/fsxl-diskfill /mounted/directory -n 35  # Utility from fsxlcw package
```
9. Run fsxlcw
```
$ sudo /usr/local/bin/fsxl-2cw
```
10. Verify the metrics are received in Amazon CloudWatch (in the same EC2 region).


## Changelog
Version 1.0.0
- All users/groups metrics are sent to Amazon CloudWatch


## License
[Apache License 2.0](LICENSE.txt)

## Contribute
See the [contributing note](CONTRIBUTING.md).
