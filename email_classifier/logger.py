import logging

# Configuração básica do logger
logging.basicConfig(
    level=logging.INFO,  # nível mínimo de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Criando um logger para o NLP
logger = logging.getLogger("nlp_logger")