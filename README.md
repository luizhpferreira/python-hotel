# Este é um projeto pessoal que criei do zero!

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
Nele eu crio um CRUD de um hotel com (GET, POST, PUT E DELETE).

Também usei o banco de dados SQLAlchemy que recebe os valores dos hoteis e também do login de usuários.

Os usuários logados tem a senha mascarada, sendo gerado um hash seguro da senha usando bcrypt.

Na lógica do negócio só é possivel adicionar um novoHotel se o usuário tiver uma conta e estiver logado nela.

Também é possível rodar a aplicação em um container Docker.

Para criar um hotel eu criei um token de autenticação, só é possível criar um novoHotel se o token estiver atualizado!

OBS: Também criei um front-end simples usando React que recebe as informações do back-end está localizado no [Python-front-end](https://github.com/luizhpferreira/front-end)
- Crie um ambiente virtual
- Necessário instalar pip install Flask==2.2.5
- Para rodar a API em um container digite "docker-compose build e docker-compose up"
- É necessário instalar pip install Flask-SQLAlchemy
- O SQLite já vem por default no python
