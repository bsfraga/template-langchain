#!/bin/bash

# Cores para mensagens (funcionam em todos os sistemas)
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    RED='\033[0;31m'
    YELLOW='\033[1;33m'
    NC='\033[0m' # No Color
else
    GREEN=''
    RED=''
    YELLOW=''
    NC=''
fi

# Variáveis para controle de execução
USE_DOCKER=true
CLEAN_FLAG=false

# Processa parâmetros da linha de comando
for arg in "$@"; do
    case $arg in
        --clean)
            CLEAN_FLAG=true
            ;;
        --no-docker)
            USE_DOCKER=false
            ;;
        *)
            # Ignora outros parâmetros
            ;;
    esac
done

# Detecta o sistema operacional
detect_os() {
    case "$(uname -s)" in
        Linux*)     OS="Linux";;
        Darwin*)    OS="MacOS";;
        CYGWIN*)    OS="Windows";;
        MINGW*)     OS="Windows";;
        MSYS*)      OS="Windows";;
        *)          OS="UNKNOWN";;
    esac
    echo $OS
}

# Define variáveis específicas do SO
OS=$(detect_os)
case "$OS" in
    "Windows")
        PYTHON_CMD="py"
        VENV_ACTIVATE=".venv/Scripts/activate"
        ;;
    *)
        PYTHON_CMD="python3"
        VENV_ACTIVATE=".venv/bin/activate"
        ;;
esac

# Função para exibir mensagens de erro e sair
error_exit() {
    echo -e "${RED}Erro: $1${NC}" >&2
    exit 1
}

# Função para exibir mensagens informativas
info() {
    echo -e "${GREEN}$1${NC}"
}

# Função para exibir avisos
warning() {
    echo -e "${YELLOW}Aviso: $1${NC}"
}

# Verifica se Docker e Docker Compose estão instalados
check_docker() {
    if ! command -v docker &> /dev/null; then
        warning "Docker não encontrado. Executando em modo local."
        return 1
    fi
    
    if ! docker compose version &> /dev/null && ! docker-compose version &> /dev/null; then
        warning "Docker Compose não encontrado. Executando em modo local."
        return 1
    fi
    
    return 0
}

# Executa a aplicação usando Docker Compose
run_with_docker() {
    info "Executando com Docker Compose..."
    
    # Verifica se o arquivo .env existe
    if [ ! -f .env ]; then
        warning "Arquivo .env não encontrado. Criando um modelo básico..."
        cat > .env << EOF
OPENAI_API_KEY=seu_api_key_aqui
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
DEBUG=False
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=1
MAX_TOKENS=2000
RESPONSE_FORMAT=json
EOF
        info "Arquivo .env criado. Por favor, edite-o com suas configurações."
        exit 1
    fi
    
    # Carrega variáveis de ambiente do .env
    if [ "$OS" = "Windows" ]; then
        # No Windows, usamos o comando 'set' para carregar variáveis de ambiente
        while IFS= read -r line || [ -n "$line" ]; do
            if [[ $line != \#* ]] && [[ ! -z "$line" ]]; then
                export "$line"
            fi
        done < .env
    else
        # No Linux/MacOS, podemos usar source
        source .env
    fi
    
    # Verifica se a OPENAI_API_KEY está configurada
    if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "seu_api_key_aqui" ]; then
        error_exit "OPENAI_API_KEY não configurada no arquivo .env"
    fi
    
    # Determina o comando Docker Compose correto
    if docker compose version &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker compose"
    else
        DOCKER_COMPOSE_CMD="docker-compose"
    fi
    
    # Executa o Docker Compose com ou sem a flag --clean
    if [ "$CLEAN_FLAG" = true ]; then
        info "Recriando toda a stack..."
        $DOCKER_COMPOSE_CMD down -v
        $DOCKER_COMPOSE_CMD build --no-cache
        $DOCKER_COMPOSE_CMD up -d
    else
        $DOCKER_COMPOSE_CMD up -d
    fi
    
    info "Aplicação iniciada em http://localhost:${API_PORT:-8000}"
}

# Executa a aplicação localmente (sem Docker)
run_locally() {
    # Verifica se Python está instalado
    if ! command -v $PYTHON_CMD &> /dev/null; then
        if [ "$OS" = "Windows" ] && command -v python &> /dev/null; then
            PYTHON_CMD="python"
        else
            error_exit "Python não encontrado. Por favor, instale o Python 3.9 ou superior."
        fi
    fi

    # Verifica a versão do Python
    PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if [ "$(echo $PYTHON_VERSION | cut -d. -f1)" -lt 3 ] || [ "$(echo $PYTHON_VERSION | cut -d. -f2)" -lt 9 ]; then
        error_exit "Python 3.9 ou superior é necessário. Versão atual: $PYTHON_VERSION"
    fi

    # Verifica se o arquivo .env existe
    if [ ! -f .env ]; then
        warning "Arquivo .env não encontrado. Criando um modelo básico..."
        cat > .env << EOF
OPENAI_API_KEY=seu_api_key_aqui
MODEL_NAME=gpt-3.5-turbo
TEMPERATURE=0.7
DEBUG=False
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=1
MAX_TOKENS=2000
RESPONSE_FORMAT=json
EOF
        info "Arquivo .env criado. Por favor, edite-o com suas configurações."
        exit 1
    fi

    # Verifica se o ambiente virtual existe, se não, cria
    if [ ! -d ".venv" ] || [ "$CLEAN_FLAG" = true ]; then
        if [ "$CLEAN_FLAG" = true ] && [ -d ".venv" ]; then
            info "Removendo ambiente virtual existente..."
            rm -rf .venv
        fi
        info "Criando ambiente virtual..."
        $PYTHON_CMD -m venv .venv || error_exit "Falha ao criar ambiente virtual"
    fi

    # Ativa o ambiente virtual
    info "Ativando ambiente virtual..."
    if [ "$OS" = "Windows" ]; then
        source $VENV_ACTIVATE || . $VENV_ACTIVATE || error_exit "Falha ao ativar ambiente virtual"
    else
        . $VENV_ACTIVATE || error_exit "Falha ao ativar ambiente virtual"
    fi

    # Atualiza pip
    info "Atualizando pip..."
    python -m pip install --upgrade pip || error_exit "Falha ao atualizar pip"

    # Instala dependências
    info "Instalando dependências..."
    pip install -e . || error_exit "Falha ao instalar dependências"

    # Garante que dependências específicas estão instaladas
    info "Verificando dependências específicas..."
    pip install "pydantic-settings>=2.1.0" \
        "langchain-community>=0.0.13" \
        "langchain-core>=0.1.15" \
        "langchain-openai>=0.0.5" \
        "instructor>=0.4.5" || error_exit "Falha ao instalar dependências específicas"

    # Carrega variáveis de ambiente do .env
    if [ "$OS" = "Windows" ]; then
        # No Windows, usamos o comando 'set' para carregar variáveis de ambiente
        while IFS= read -r line || [ -n "$line" ]; do
            if [[ $line != \#* ]] && [[ ! -z "$line" ]]; then
                export "$line"
            fi
        done < .env
    else
        # No Linux/MacOS, podemos usar source
        source .env
    fi

    # Verifica se a OPENAI_API_KEY está configurada
    if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "seu_api_key_aqui" ]; then
        error_exit "OPENAI_API_KEY não configurada no arquivo .env"
    fi

    # Define permissões do arquivo (apenas Unix-like)
    if [ "$OS" != "Windows" ]; then
        chmod +x run.sh 2>/dev/null || true
    fi

    # Inicia o servidor
    info "Iniciando o servidor..."
    python -m uvicorn src.langchain_template.api:app \
        --host ${API_HOST:-0.0.0.0} \
        --port ${API_PORT:-8000} \
        --workers ${API_WORKERS:-1} \
        --reload
}

# Executa a aplicação com Docker ou localmente
if [ "$USE_DOCKER" = true ] && check_docker; then
    run_with_docker
else
    run_locally
fi 