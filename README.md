# Plusplan - Sistema de Planejamento - PMOC

Bem-vindo ao **Plusplan**, um sistema de planejamento voltado para a gestão de Planos de Manutenção, Operação e Controle (PMOC). Este projeto está em **desenvolvimento** e foi criado como um recurso educacional para quem está estudando desenvolvimento web com Python e Django.

## Sobre o Projeto

O Plusplan é um sistema web em construção, desenvolvido em Python e Django, idealizado para ajudar estudantes a aprender sobre a criação de aplicações web, autenticação de usuários e gestão de planos de manutenção. Ele serve como um exemplo prático para explorar conceitos como MVC, bancos de dados e design de interfaces.

### Funcionalidades (em Desenvolvimento)

- **Autenticação de Usuários**: Login seguro com interface personalizada ("Plusplan").
- **Cadastro de Usuários**: Registro básico de novos usuários.
- **Gestão de Planos**: Estrutura inicial para criar e monitorar planos de manutenção (em progresso).
- **Interface Intuitiva**: Design simples para estudo e personalização.

**Nota**: Este é um projeto educacional. As funcionalidades estão sendo implementadas gradualmente e podem não estar completas.

## Público-Alvo

Este repositório é voltado para:
- Estudantes de desenvolvimento web ou ciência da computação.
- Profissionais iniciantes em Python e Django ou gestão de PMOC.
- Qualquer pessoa interessada em aprender contribuindo com código aberto.

## Pré-requisitos

Antes de instalar e rodar o Plusplan, certifique-se de ter o seguinte instalado:

- Python 3.10 ou superior
- Git
- Um ambiente virtual (recomendado)
- Banco de dados SQLite (padrão) ou PostgreSQL (para prática avançada)

## Instalação

Siga os passos abaixo para configurar o projeto localmente e usá-lo como material de estudo:

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/lourival2021/plusplan.git
   cd plusplan
   ```

2. **Crie e Ative um Ambiente Virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o Banco de Dados**:
   Execute as migrações para criar o banco de dados:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crie um Superusuário** (para explorar o admin):
   ```bash
   python manage.py createsuperuser
   ```

6. **Inicie o Servidor**:
   ```bash
   python manage.py runserver
   ```
   Acesse o sistema em `http://127.0.0.1:8000/login/` para explorar.

## Uso Educacional

- **Login**: Experimente a página de login em `http://127.0.0.1:8000/login/` com as credenciais do superusuário.
- **Admin**: Explore o painel em `http://127.0.0.1:8000/admin/` para gerenciar dados.
- **Personalização**: Modifique o código (ex.: `usuarios/views.py` ou `templates/`) para aprender.

## Estrutura do Projeto

- `plusplan/`: Configurações principais do projeto Django.
- `usuarios/`: App para autenticação e gerenciamento de usuários (base para estudos).
- `cadastros/`: App para cadastros de clientes, empresas, contrato e outros (base para estudos).
- `financeiros/`: App para controle financeiro (base para estudos).
- `planejamentos/`: App para planejamento do PMOC (base para estudos).
- `static/`: Arquivos estáticos (personalizáveis).
- `templates/`: Templates HTML para prática de design.

## Progresso

- **Última Atualização**: 30 de maio de 2025, 09:47 AM -03.
- **Tarefas Pendentes**: Implementação completa da gestão de planos e relatórios.

## Para Produção (Futuro)

Este projeto ainda não está pronto para produção. Para fins educacionais, use o ambiente local. Quando concluído, será necessário:
- Configurar `ALLOWED_HOSTS` em `plusplan/settings.py`.
- Usar um banco de dados como PostgreSQL.
- Coletar arquivos estáticos:
  ```bash
  python manage.py collectstatic
  ```

## Contribuição

Como projeto educacional, incentivamos contribuições de estudantes e aprendizes! Siga os passos:

1. Faça um fork do repositório.
2. Crie um branch para sua ideia:
   ```bash
   git checkout -b minha-ideia
   ```
3. Faça suas alterações e commit:
   ```bash
   git commit -m "Adiciona minha ideia"
   ```
4. Envie para o repositório:
   ```bash
   git push origin minha-ideia
   ```
5. Abra um Pull Request no GitHub para discutir e aprender.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes (opcional para estudantes).

## Contato

Se tiver dúvidas ou ideias para o aprendizado, entre em contato: lourival_silva@msn.com

---

Desenvolvido por Lourival da Silva Júnior - 2025

---

Lembre-se "Aprender, construir e evoluir todos os dias."