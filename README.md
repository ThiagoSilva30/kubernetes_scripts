#Kubernetes scripts 

# user_creation.py

O script user_creation.py foi projetado para automatizar a criação de usuario no kubernetes.

Para isso, ele cria os certificados, aprova a solicitacao e seta o usuario no cluster que o usuario desejar.

É necessário passar 2 parametros para que o script seja executado corretamente, um nome para o usuario e o context/cluster que voce deseja setar o usuário criado.

É adcionado um arquivo csr.yaml para que o script tambem seja executado. Voce pode configurar este arquivo como desejar, só é necessário deixar em branco os campos "name" e "request"

Exemplo:

python3 user_creation.py devops cluster