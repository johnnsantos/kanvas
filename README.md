# ROTAS DA APLICAÇÃO
- ``POST /api/accounts/`` - cria usuários
- ``POST /api/login/`` - faz autenticação
- ``POST /api/courses/`` - cria curso (user: instrutor apenas)
- ``PUT /api/courses/registrations/`` - matricula estudantes num determinado curso (user: instrutor apenas)
- ``GET /api/courses/``- lista cursos e alunos matriculados (sem autenticação)
- ``POST /api/activities/`` - cria atividade do estudante (sem nota, user: estudante apenas)
- ``PUT /api/activities/`` - edita atividade - atribui nota - (user: facilitador e instrutor)
- ``GET /api/activities/`` - lista atividades do estudante (user: estudante)
- ``GET /api/activities/`` - lista todas as atividades de todos os estudantes (user: facilitador e instrutor)
- ``GET /api/activities/<int:user_id>/`` - filtra as atividades por user_id (user: facilitador e instrutor)

## Sobre Usuários:
Esta plataforma terá 3 tipos de usuário:

Estudante
Facilitador
Instrutor
Você deverá utilizar os campos que vêm no User padrão do Django, ou seja:

username
first_name
last_name
email
password
groups
user_permissions
is_staff
is_active
is_superuser
last_login
date_joined
Confira a documentação em:  (Links para um site externo.) https://docs.djangoproject.com/pt-br/3.1/ref/contrib/auth/ (Links para um site externo.) para mais detalhes, se necessário.

Para diferenciar entre os tipos de acesso, você deverá trabalhar com os campos is_staff e is_superuser, sendo que:

Estudante - terá ambos os campos is_staff e is_superuser com o valor False
Facilitador - terá os campos is_staff == True e is_superuser == False
Instrutor - terá ambos os campos is_staff e is_superuser com o valor True

## Sobre Criação de Usuários:
Para poder criar usuários de diferentes tipos, é necessário utilizar o seguinte endpoint:/api/accounts/.

Não implemente qualquer tipo de autenticação para este endpoint - ou seja, qualquer pessoa pode criar qualquer usuário.

````
POST /api/accounts/ - criando um estudante:
// REQUEST
{
  "username": "student",
  "password": "1234",
  "is_superuser": false,
  "is_staff": false
}
````

````
// RESPONSE STATUS -> HTTP 201
{
  "id": 1,
  "username": "student",
  "is_superuser": false,
  "is_staff": false
}
````
````
POST /api/accounts/ - criando um facilitador:
// REQUEST
{
  "username": "facilitator",
  "password": "1234",
  "is_superuser": false,
  "is_staff": true
}
````
````
// RESPONSE STATUS -> HTTP 201
{
  "id": 2,
  "username": "facilitator",
  "is_superuser": false,
  "is_staff": true
}
````
````
POST /api/accounts/ - criando um instrutor:
// REQUEST
{
  "username": "instructor",
  "password": "1234",
  "is_superuser": true,
  "is_staff": true
}
````
````
// RESPONSE STATUS -> HTTP 201
{
  "id": 3,
  "username": "instructor",
  "is_superuser": true,
  "is_staff": true
}
````

Caso haja a tentativa de criação de um usuário que já está cadastrado o sistema deverá responder com HTTP 409 - Conflict.

## Sobre Autenticação:
A API funcionará com autenticação baseada em token.

````
POST /api/login/ - fazendo login (serve para qualquer tipo de usuário):
// REQUEST
{
  "username": "student",
  "password": "1234"
}
````
````
// RESPONSE STATUS -> HTTP 200
{
  "token": "dfd384673e9127213de6116ca33257ce4aa203cf"
}
````
Esse token servirá para identificar o usuário em cada request. Na grande maioria dos endpoints seguintes, será necessário colocar essa informação nos Headers. O header específico para autenticação tem o formato Authorization: Token <colocar o token aqui>.

## Sobre Cursos:
Course é um model que representa um curso dentro da plataforma Kanvas. Apenas um User com acesso de instrutor (ou seja is_superuser == True) pode criar novos cursos e matricular usuários nos cursos.

Naturalmente, existe uma relação de N→ N entre Course e User. Um curso tem vários alunos. Simultaneamente, um estudante pode estar matriculado em diversos cursos.

````
POST /api/courses/ - criando um curso:
// REQUEST
// Header -> Authorization: Token <token-do-instrutor>
{
  "name": "Javascript 101"
}
// RESPONSE STATUS -> HTTP 201
{
  "id": 1,
  "name": "Javascript 101",
  "user_set": []
}
````
Se for fornecido um token de estudante ou facilitador, o sistema deverá responder da seguinte forma:

````
// REQUEST
// Header -> Authorization: Token <token-do-facilitador ou token-to-estudante>
{
  "name": "Javascript 101"
}
// RESPONSE STATUS -> HTTP 403
{
  "detail": "You do not have permission to perform this action."
}
````

Dica: para obter este comportamento, você precisará criar uma classe de permissões e utilizá-la adequadamente nas views. Dê uma olhada no material sobre esse assunto. 📖

````
PUT /api/courses/registrations/- atualizando a lista de estudantes matriculados em um curso:
// REQUEST
// Header -> Authorization: Token <token-do-instrutor>
{
  "course_id": 1,
  "user_ids": [1, 2, 7]
}
// RESPONSE STATUS -> HTTP 200
{
  "id": 1,
  "name": "Javascript 101",
  "user_set": [
    {
      "id": 1,
      "is_superuser": false,
      "is_staff": false,
      "username": "luiz"
    },
    {
      "id": 7,
      "is_superuser": false,
      "is_staff": false,
      "username": "isabela"
    },
    {
      "id": 2,
      "is_superuser": false,
      "is_staff": false,
      "username": "raphael"
    }
  ]
}
````
Desta forma é possível matricular vários alunos simultaneamente. Da mesma maneira, é possível remover vários estudantes ao mesmo tempo ao registrar novamente a lista de alunos.

````
// REQUEST
// Header -> Authorization: Token <token-do-instrutor>
{
  "course_id": 1,
  "user_ids": [1]
}
// RESPONSE STATUS -> HTTP 200
{
  "id": 1,
  "name": "Javascript 101",
  "user_set": [
    {
      "id": 1,
      "is_superuser": false,
      "is_staff": false,
      "username": "luiz"
    }
  ]
}
````

Toda requisição feita para esse endpoint deverá atualizar a lista de alunos matriculados no curso. No primeiro exemplo os alunos 1, 2 e 7 foram vinculados ao curso 1. Já na segunda requisição a lista de alunos foi atualizada, matriculando somente o aluno 1 e removendo os alunos 2 e 7 que não estavam na nova listagem.

Se for fornecido um token de estudante ou facilitador, o sistema deverá responder da seguinte forma:

````
// REQUEST
// Header -> Authorization: Token <token-do-facilitador ou token-to-estudante>
{
  "course_id": 1,
  "user_ids": [1]
}
// RESPONSE STATUS -> HTTP 403
{
  "detail": "You do not have permission to perform this action."
}
````

* Dica: para obter este comportamento, você precisará criar uma classe de permissões e utilizá-la adequadamente nas views. Dê uma olhada no material sobre esse assunto. 📖

GET /api/courses/ - obtendo a lista de cursos e alunos:
Este endpoint pode ser acessado por qualquer client (mesmo sem autenticação). A resposta do servidor deve trazer uma lista de cursos, mostrando cada aluno inscrito, no seguinte formato:

````
// RESPONSE STATUS -> HTTP 200
[
  {
    "id": 1,
    "name": "Javascript 101",
    "user_set": [
      {
        "id": 1,
        "is_superuser": false,
        "is_staff": false,
        "username": "luiz"
      }
    ]
  },
  {
    "id": 2,
    "name": "Python 101",
    "user_set": []
  }
]
````

## Sobre Atividades:
Activity representa uma atividade feita por um User. Existe uma relação de 1 → N entre User e Activity. Somente um usuário do tipo estudante pode criar uma Activity porém não pode atribuir uma nota. Apenas um User com no mínimo is_staff == True pode atribuir a nota (grade) à Activity.

Dica: Para simplificar, não crie associações entre Activity e Course.


````POST /api/activities/ - criando uma atividade (estudante)````
Mesmo que o User do tipo estudante faça um request que tem o campo grade, a nota não deve ser registrada no momento da criação.

````
// REQUEST
// Header -> Authorization: Token <token-do-estudante>
{
  "repo": "gitlab.com/cantina-kenzie",
  "grade": 10 // Esse campo é opcional
}
// RESPONSE STATUS -> HTTP 201
// Repare que o campo grade foi ignorado
{
  "id": 6,
  "user_id": 7,
  "repo": "gitlab.com/cantina-kenzie",
  "grade": null
}
````

Podemos observar que nesse request o campo grade não foi passado, e a resposta do sistema foi um grade: null.

````
// REQUEST
// Header -> Authorization: Token <token-do-estudante>
{
  "repo": "gitlab.com/cantina-kenzie",
}
// RESPONSE STATUS -> HTTP 201
// Repare que o campo grade foi ignorado
{
  "id": 6,
  "user_id": 7,
  "repo": "gitlab.com/cantina-kenzie",
  "grade": null
}
````

Não deve ser possível criar duas ou mais atividades com o mesmo repo, ou seja, caso tenha sido criada uma atividade com o "repo: gitlab.com/cantina-kenzie (Links para um site externo.)", ao cadastrar uma nova atividade com o "repo: gitlab.com/cantina-kenzie (Links para um site externo.)" o sistema não deverá criar uma nova atividade.

Se for fornecido um token de facilitador ou instrutor, o sistema deverá responder com HTTP 401 - Unauthorized.

````
PUT /api/activities/ - editando a nota de uma atividade (facilitador ou instrutor)
//REQUEST
//Header -> Authorization: Token <token-do-facilitador ou instrutor>
{
  "id": 6,
  "grade": 10
}
//RESPONSE STATUS -> HTTP 201
{
  "id": 6,
  "user_id": 7,
  "repo": "gitlab.com/cantina-kenzie",
  "grade": 10
}
````

Se for fornecido um token de estudante o sistema deverá responder com HTTP 401 - Unauthorized.

Caso seja informado o id de uma atividade inválido o sistema deverá responder com HTTP 404 - Not Found.

Além disso, um User do tipo estudante pode apenas visualizar uma lista com as suas próprias atividades. Já os usuários do tipo instrutor e facilitador podem visualizar todas as atividades de todos os estudantes e filtrar as atividades por usuários.

````
GET /api/activities/ - listando atividades (estudante)
//REQUEST
//Header -> Authorization: Token <token-do-estudante>
[
  {
    "id": 1,
    "user_id": 1,
    "repo": "github.com/luiz/cantina",
    "grade": null
  },
  {
    "id": 6,
    "user_id": 1,
    "repo": "github.com/hanoi",
    "grade": null
  },
  {
    "id": 15,
    "user_id": 1,
    "repo": "github.com/foodlabs",
    "grade": null
  },
]
````

Reparem que todas as atividades têm o mesmo user_id.

````
GET /api/activities/ - listando atividades (facilitador ou instrutor)
//REQUEST
//Header -> Authorization: Token <token-do-facilitador ou token-do-instrutor>
[
  {
    "id": 1,
    "user_id": 1,
    "repo": "github.com/luiz/cantina",
    "grade": null
  },
  {
    "id": 6,
    "user_id": 1,
    "repo": "github.com/hanoi",
    "grade": null
  },
  {
    "id": 10,
    "user_id": 2,
    "repo": "github.com/foodlabs",
    "grade": null
  },
  {
    "id": 35,
    "user_id": 3,
    "repo": "github.com/kanvas",
    "grade": null
  },
]
````

Reparem que agora listamos atividades com user_id diferentes.

GET /api/activities/<int:user_id>/ - filtrando atividades fornecendo um user_id opcional (facilitador ou instrutor)
Como os instrutores e facilitadores podem ver as atividades de todos os alunos, precisamos dar a eles a opção de filtrar esses dados através do user_id. Se o id enviado for 1, o retorno deve ser a lista de todas as atividades do usuário (estudante) que possui user_id = 1.

````
//REQUEST (/api/activities/1/)
//Header -> Authorization: Token <token-do-facilitador ou token-do-instrutor>
[
  {
    "id": 1,
    "user_id": 1,
    "repo": "github.com/luiz/cantina",
    "grade": null
  },
  {
    "id": 6,
    "user_id": 1,
    "repo": "github.com/hanoi",
    "grade": null
  },
  {
    "id": 15,
    "user_id": 1,
    "repo": "github.com/foodlabs",
    "grade": null
  },
]
````

Caso o user_id enviado seja inválido, você deverá retornar um status HTTP 404 NOT FOUND.

````
//REQUEST (/api/activities/x/)
//Header -> Authorization: Token <token-do-facilitador ou instrutor>
// RESPONSE STATUS -> HTTP 404 NOT FOUND
{ 
  "detail": "Invalid user_id." 
}
````