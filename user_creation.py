#####   NOME:            user_creation.py
#####   VERSÃO:          1.0
#####   DESCRIÇÃO:       Cria usuario kubernetes
#####   DATA DA CRIAÇÃO: 10/05/2023
#####   ESCRITO POR:     Thiago Gama da Silva
#####   E-MAIL:          t.gama.silva@gmail.com

import sys
import os
import subprocess
from os import system

def verify_parameters():
    if len(sys.argv) != 3:
        print("Devem ser passado 2 parametros: usuario e nome do cluster")
        exit();

def cert_creation():
    # 1 - cert creation
    global user
    user=sys.argv[1]
    #user=input("Nome do usuário: ")
    print('criando certificados...')
    os.system("sleep 1")
    user_key = "openssl genrsa -out {0}.key 2048".format(user)
    os.system(user_key)
    user_csr = "openssl req -new -key {0}.key -out {0}.csr -subj '/CN={0}'".format(user)
    os.system(user_csr)
    print('Certificados criados listados abaixo')
    os.system('ls {0}*'.format(user))

def object_create_csr():
    # 2 - object creation 
    global request 
    global file_object
    command="cat {0}.csr | base64 | tr -d '\n'".format(user)
    request=subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    sed_file="sed -e 's/name:/name: {0}/g' -e 's/request:/request: {1}/g' csr_sample.yaml > csr_{0}.yaml".format(user,request.decode('utf-8'))
    os.system(sed_file)
    command_apply="kubectl apply -f csr_{0}.yaml".format(user)
    os.system(command_apply)

def kube_cert_approve():
    # 3 - kubernetes approve
    command_approve="kubectl certificate approve {0}".format(user)
    approve=subprocess.check_output(command_approve, shell=True)
    
    command_export=f"kubectl get csr {user} -o jsonpath='{{.status.certificate}}' | base64 -d > {user}.crt"
    export=subprocess.check_output(command_export, shell=True)

def kube_add_user():
    # 4 - add user to kubeconfig
    command_add_user="kubectl config set-credentials {0} --client-key={0}.key --client-certificate={0}.crt --embed-certs=true".format(user)
    add_user=subprocess.check_output(command_add_user, shell=True)

def kube_add_context():
    # 5 - add context to kubeconfig
    global cluster
    cluster=sys.argv[2]
    command_add_context="kubectl config set-context {1} --cluster={0} --user={1}".format(cluster, user)
    add_context=subprocess.check_output(command_add_context, shell=True)
    print(' ')
    print('Sucesso. Verifique abaixo o certificado criado e o usuário setado no contexto escolhido;')
    print(' ')
    command_get_context="kubectl config get-contexts"
    os.system(command_get_context)
    print(' ')
    command_get_csr="kubectl get csr"
    os.system(command_get_csr)


verify_parameters()
cert_creation()
object_create_csr()
kube_cert_approve()
kube_add_user()
kube_add_context()

