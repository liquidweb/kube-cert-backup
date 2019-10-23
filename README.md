# Cert Object Backup and Restore

This small script is to back up Kubernetes certificate objects that are used by the cert-manager.
The script will also restore by creating the backed-up certificate objects in the given Kubernetes
namespace.

## Installation

After cloning the repo you will need to add the yaml library

```bash
python setup.py install
```

This script uses the pyyaml library. If for some reason install fails you can always just install
pyyaml with pip

```bash
pip install pyyaml
```

You can find more information on this library at [PyYaml](https://pyyaml.org/wiki/PyYAMLDocumentation)

## Usage

For backing up cert objects you need to give 3 parameters: namespace, k8 config path, and the key word backup.

```bash
python backup.py <namespace> backup <k8_config_path>
```
example
```bash
sudo python backup.py liquid-web-cert-manager-staging backup /Users/myusername/.kube/config-dev
```

For restoring the cert object after a back up you need to give 3 parameters: namespace, k8 config path, and the key word restore.
<b>Note: If you have multiple backup files there is no guarantee it will restore from latest. Only one backup file should be kept
 in back up path.</b>

```bash
python backup.py <namespace> restore <k8_config_path>
```
example
```bash
sudo python backup.py liquid-web-cert-manager-staging restore /Users/myusername/.kube/config-dev
```

All certificate objects will be backed up to the following path in yaml form.

```bash
/var/lib/backup/<cert_manager_backup_timestamp>/certs
``` 

## Other

This script uses kubectl and it assumes that you have kubectl already installed and its context
configured to the kubernetes profile you wish to connect to.

More info can be found at [Setup kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
Change kubernetes kubectl context [Configure Access to Multiple Cluster](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)

