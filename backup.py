#!/usr/bin/python
import os
import subprocess
import datetime
import yaml
import sys


namespace = sys.argv[1]
action = sys.argv[2]
k8_config = sys.argv[3]
backup_dir = '/var/lib/backup/'
backup_now = 'cert_manager_backup_%s' % datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
backup_path = os.path.join(backup_dir, backup_now)


def get_cert_obj():
    my_env = os.environ.copy()
    my_env['KUBECONFIG'] = k8_config
    command = 'kubectl get certs -n {0} --no-headers' \
              ' -o custom-columns=name:.metadata.name'.format(namespace).split()
    return subprocess.check_output(command, env=my_env).split()


def get_secret_obj():
    my_env = os.environ.copy()
    my_env['KUBECONFIG'] = k8_config
    command = 'kubectl get secrets -n {0} --no-headers' \
              ' -o custom-columns=name:.metadata.name'.format(namespace).split()
    return subprocess.check_output(command, env=my_env).split()


def write_yaml_objs(certs, obj_type):
    my_env = os.environ.copy()
    my_env['KUBECONFIG'] = k8_config
    if obj_type == 'certs':
        path = backup_path + '/certs'
    if obj_type == 'secrets':
        path = backup_path + '/secrets'
    for cert_obj in certs:
        command = 'kubectl get cert {0} -n {1} -o yaml'.format(cert_obj, namespace).split()
        yaml_stream = yaml.load(subprocess.check_output(command, env=my_env), Loader=yaml.FullLoader)
        '''Clean up the yaml file and remove generated data from k8'''
        del yaml_stream['status']
        del yaml_stream['metadata']['creationTimestamp']
        del yaml_stream['metadata']['generation']
        del yaml_stream['metadata']['resourceVersion']
        del yaml_stream['metadata']['selfLink']
        del yaml_stream['metadata']['uid']
        if not os.path.isdir(path):
            os.makedirs(path)
        with open(os.path.join(path,
                               "%s.yaml" % cert_obj), 'w') as fh:
            yaml.dump(yaml_stream, fh)


def restore_from_backup(certs, path):
    my_env = os.environ.copy()
    my_env['KUBECONFIG'] = k8_config
    os.chdir(path)
    for cert in certs:
        print 'Creating cert object for {0}'.format(cert)
        command = 'kubectl create -f {0} -n {1}'.format(cert, namespace).split()
        subprocess.check_output(command, env=my_env).split()


def read_cert_obj_from_backup(obj_type):
    print('Reading cert objects from back up file')
    backup_file_names = os.listdir(backup_dir)
    latest_backup = backup_file_names[len(backup_file_names)-1:]
    path = backup_dir + latest_backup[0]
    if obj_type == 'certs':
        path = path + '/certs'
    if obj_type == 'secrets':
        path = path + '/secrets'
    return os.listdir(path), path


if action == 'backup':
    print('Backing up cert objects... namespace {0} -- k8 config {1}'.format(namespace, k8_config))
    cert_objs = get_cert_obj()
    write_yaml_objs(cert_objs, 'certs')
    #secrets = get_secret_obj()
    #write_yaml_objs(secrets, 'secrets')
    print('Backup complete')
if action == 'restore':
    print('Restoring cert objects...')
    args = read_cert_obj_from_backup('certs')
    restore_from_backup(args[0], args[1])
    #args = read_cert_obj_from_backup('secrets')
    #restore_from_backup(args[0], args[1])
    print('Restore complete')
