
# Configuration for the Hazmat Classifier pipeline

# Data Collection
ML_BASE_URL = "https://lista.mercadolivre.com.br"
ML_API_BASE_URL = "https://api.mercadolibre.com"
SITE_ID = "MLB"

QUERIES = [
    "limpeza", "beleza", "ferramentas", "eletrônicos", "saúde", "automotivo", "casa", "cozinha", "banheiro", "escritório",
    "escola", "celular", "informática", "roupas", "calçados", "acessórios", "bebê", "brinquedos", "esporte", "academia",
    "iluminação", "elétrica", "jardim", "construção", "decoração", "climatização", "som", "vídeo", "câmeras", "vigilância",
    "perfumes", "cuidados pessoais", "higiene", "cosméticos", "maquiagem", "dermocosméticos", "ferramentas elétricas",
    "parafusos", "pintura", "automação", "segurança", "autopeças", "pneus", "som automotivo", "faróis", "escapamento",
    "bateria", "moto", "bicicleta", "pescaria", "camping", "churrasco", "limpeza pesada", "desinfetantes", "inseticidas",
    "papelaria", "mochilas", "malas", "relógios", "óculos", "calças", "camisetas", "jaquetas", "tênis", "sandálias", "meias",
    "lingerie", "fraldas", "mamadeiras", "carrinho de bebê", "berço", "livros", "livros infantis", "livros técnicos", "pets",
    "ração", "gatos", "cães", "aquário", "energia solar", "placas solares", "carregador portátil", "pilhas", "extintores",
    "tinta spray", "epóxi", "adesivo", "colas", "verniz", "solvente", "álcool", "baterias", "pilhas recarregáveis",
    "produtos de limpeza", "cuidados com o carro", "climatizador", "ventilador", "umidificador", "ar-condicionado", "energia elétrica"
]

# Classification
JSON_EXTRACTOR_MODEL = "gemini/gemini-2.5-flash"
HAZMAT_CLASSIFIER_MODEL = "gemini/gemini-2.5-flash"

# File Paths
DATA_DIR = "data"
HAZMAT_DEFINITION_FILE = "data/hazmat-definition.md"
