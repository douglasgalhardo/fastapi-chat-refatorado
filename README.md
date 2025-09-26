# Chat em Tempo Real com FastAPI, MongoDB e WebSockets

Este projeto é uma aplicação de chat em tempo real construída com FastAPI, MongoDB Atlas e WebSockets. O código foi completamente refatorado a partir de uma base funcional para seguir as melhores práticas de desenvolvimento, como modularidade, separação de responsabilidades e o uso de Pydantic para validação de dados.

## ✨ Principais Funcionalidades

- **Comunicação em Tempo Real**: Envio e recebimento de mensagens instantaneamente via WebSockets.
- **Salas de Chat Múltiplas**: Suporte para diferentes salas, isolando as conversas.
- **Persistência de Mensagens**: As mensagens são salvas em um banco de dados NoSQL (MongoDB Atlas).
- **Histórico de Mensagens**: Ao entrar em uma sala, o usuário recebe o histórico recente de mensagens.
- **API REST Documentada**: Endpoints REST para interagir com as mensagens, com documentação automática via Swagger UI.
- **Código Modular e Organizado**: A estrutura do projeto foi refatorada para facilitar a manutenção e escalabilidade.

## 📂 Estrutura do Projeto

A arquitetura do projeto foi organizada para separar as responsabilidades:

```
/
├── app/
│   ├── __init__.py
│   ├── config.py             # Carrega as variáveis de ambiente
│   ├── database.py           # Gerencia a conexão com o MongoDB
│   ├── main.py               # Ponto de entrada da aplicação FastAPI
│   ├── models.py             # Define os modelos de dados com Pydantic
│   ├── ws_manager.py         # Gerencia as conexões WebSocket
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── messages.py       # Rotas REST para mensagens
│   │   └── websocket.py      # Rota do WebSocket
│   └── static/
│       └── index.html        # Frontend simples para testes
├── .env                      # Arquivo para as variáveis de ambiente (local)
├── README.md                 # Esta documentação
└── requirements.txt          # Dependências do projeto
```

## 🛠️ Pré-requisitos

Antes de começar, garanta que você tenha:

- **Python 3.8+** instalado.
- Uma conta no **MongoDB Atlas** com um cluster gratuito criado.

## ⚙️ Instalação e Configuração (Passo a Passo)

Siga os passos abaixo para configurar e rodar o projeto localmente.

**1. Clonar o Repositório**

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA_DO_PROJETO>
```

**2. Criar e Ativar o Ambiente Virtual**

É uma boa prática isolar as dependências do projeto.

- No Windows:
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```
- No macOS/Linux:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

**3. Instalar as Dependências**

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

**4. Configurar as Variáveis de Ambiente**

Este passo é crucial para a conexão com o banco de dados.

- Crie uma cópia do arquivo `.env.example` (se houver) ou crie um novo arquivo chamado `.env` na raiz do projeto.
- Adicione a sua **Connection String** do MongoDB Atlas a este arquivo:

  ```env
  # Substitua pela sua string de conexão do MongoDB Atlas
  # Lembre-se de substituir <password> pela sua senha e, se necessário, o nome do banco.
  MONGO_URL="mongodb+srv://<user>:<password>@<cluster-url>/<db-name>?retryWrites=true&w=majority"
  ```

## ▶️ Executando a Aplicação

Após a instalação e configuração, inicie o servidor com o Uvicorn:

```bash
uvicorn app.main:app --reload
```

- O servidor estará rodando em `http://localhost:8000/`.
- A documentação interativa da API (Swagger) estará disponível em `http://localhost:8000/docs`.

## 🚀 Como Usar e Testar

1.  Abra seu navegador e acesse `http://localhost:8000/`.
2.  Digite um nome para a **sala** (ex: `geral`), seu **nome** (ex: `Ana`) e clique em **Conectar**.
3.  Abra uma **nova janela anônima** do navegador e acesse `http://localhost:8000/` novamente.
4.  Conecte-se à **mesma sala** (`geral`), mas com um nome diferente (ex: `Beto`).
5.  Envie mensagens em uma janela e veja-as aparecerem em tempo real na outra!

## Endpoints da API

| Método | Endpoint                 | Descrição                                         |
| :----- | :----------------------- | :------------------------------------------------ |
| `GET`  | `/rooms/{room}/messages` | Retorna o histórico de mensagens de uma sala.     |
| `POST` | `/rooms/{room}/messages` | Envia uma nova mensagem para uma sala (via REST). |
| `WS`   | `/ws/{room}`             | Estabelece a conexão WebSocket para uma sala.     |
