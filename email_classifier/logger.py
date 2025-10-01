import logging

# Configuração básica do logger
logging.basicConfig(
    level=logging.INFO,  # nível mínimo de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Criando loggers específicos para diferentes módulos
logger_nlp = logging.getLogger("nlp_logger")
logger_views = logging.getLogger("views_logger")
logger_utils = logging.getLogger("utils_logger")
logger_api = logging.getLogger("api_logger")