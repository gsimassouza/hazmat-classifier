
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

NON_HAZMAT_PRODUCTS = """
# Non-Hazmat Products List
*Safe for Regular Shipping and Transport*

## Food & Beverages | Alimentos e Bebidas | Alimentos y Bebidas

**English** | **Portuguese** | **Spanish**
---|---|---
Canned vegetables | Vegetais enlatados | Vegetales enlatados
Dried fruits | Frutas secas | Frutas secas
Pasta | Massa | Pasta
Rice | Arroz | Arroz
Bread | Pão | Pan
Cookies | Biscoitos | Galletas
Chocolate | Chocolate | Chocolate
Coffee beans | Grãos de café | Granos de café
Tea bags | Sachês de chá | Bolsitas de té
Honey | Mel | Miel
Olive oil | Azeite de oliva | Aceite de oliva
Vinegar | Vinagre | Vinagre
Salt | Sal | Sal
Sugar | Açúcar | Azúcar
Flour | Farinha | Harina
Spices | Especiarias | Especias
Nuts | Nozes | Nueces
Cereal | Cereal | Cereal
Juice (non-alcoholic) | Suco (não alcoólico) | Jugo (sin alcohol)
Bottled water | Água engarrafada | Agua embotellada

## Clothing & Textiles | Roupas e Têxteis | Ropa y Textiles

**English** | **Portuguese** | **Spanish**
---|---|---
T-shirts | Camisetas | Camisetas
Jeans | Jeans | Vaqueros
Sweaters | Suéteres | Suéteres
Dresses | Vestidos | Vestidos
Underwear | Roupa íntima | Ropa interior
Socks | Meias | Calcetines
Shoes | Sapatos | Zapatos
Hats | Chapéus | Sombreros
Jackets | Jaquetas | Chaquetas
Scarves | Cachecóis | Bufandas
Gloves | Luvas | Guantes
Belts | Cintos | Cinturones
Handbags | Bolsas | Bolsos
Backpacks | Mochilas | Mochilas
Towels | Toalhas | Toallas
Bed sheets | Lençóis | Sábanas
Blankets | Cobertores | Mantas
Pillows | Travesseiros | Almohadas
Curtains | Cortinas | Cortinas
Rugs | Tapetes | Alfombras

## Electronics & Technology | Eletrônicos e Tecnologia | Electrónicos y Tecnología

**English** | **Portuguese** | **Spanish**
---|---|---
Smartphones | Smartphones | Teléfonos inteligentes
Laptops | Laptops | Laptops
Tablets | Tablets | Tabletas
Headphones | Fones de ouvido | Auriculares
Speakers | Alto-falantes | Altavoces
Keyboards | Teclados | Teclados
Computer mice | Mouses | Ratones de computadora
USB cables | Cabos USB | Cables USB
Phone chargers | Carregadores de telefone | Cargadores de teléfono
Power banks | Baterias portáteis | Baterías portátiles
Memory cards | Cartões de memória | Tarjetas de memoria
Hard drives | Discos rígidos | Discos duros
Digital cameras | Câmeras digitais | Cámaras digitales
E-readers | Leitores eletrônicos | Lectores electrónicos
Gaming controllers | Controles de jogos | Controles de videojuegos
Television | Televisão | Televisión
DVD players | Reprodutores de DVD | Reproductores de DVD
Radios | Rádios | Radios
Calculators | Calculadoras | Calculadoras
Watches | Relógios | Relojes

## Books & Stationery | Livros e Papelaria | Libros y Papelería

**English** | **Portuguese** | **Spanish**
---|---|---
Novels | Romances | Novelas
Textbooks | Livros didáticos | Libros de texto
Magazines | Revistas | Revistas
Newspapers | Jornais | Periódicos
Notebooks | Cadernos | Cuadernos
Pens | Canetas | Bolígrafos
Pencils | Lápis | Lápices
Erasers | Borrachas | Gomas de borrar
Rulers | Réguas | Reglas
Markers | Marcadores | Marcadores
Crayons | Giz de cera | Crayones
Paper | Papel | Papel
Envelopes | Envelopes | Sobres
Stamps | Selos | Sellos
Staplers | Grampeadores | Grapadoras
Paper clips | Clipes de papel | Clips
Folders | Pastas | Carpetas
Binders | Fichários | Carpetas de argollas
Calendars | Calendários | Calendarios
Diaries | Diários | Diarios

## Home & Garden | Casa e Jardim | Casa y Jardín

**English** | **Portuguese** | **Spanish**
---|---|---
Furniture | Móveis | Muebles
Lamps | Lâmpadas | Lámparas
Mirrors | Espelhos | Espejos
Picture frames | Molduras | Marcos de fotos
Vases | Vasos | Jarrones
Candles | Velas | Velas
Kitchenware | Utensílios de cozinha | Utensilios de cocina
Plates | Pratos | Platos
Cups | Xícaras | Tazas
Glasses | Copos | Vasos
Cutlery | Talheres | Cubiertos
Pots and pans | Panelas e frigideiras | Ollas y sartenes
Cleaning cloths | Panos de limpeza | Paños de limpieza
Brooms | Vassouras | Escobas
Mops | Esfregões | Trapeadores
Vacuum cleaners | Aspiradores | Aspiradoras
Garden tools | Ferramentas de jardim | Herramientas de jardín
Flower pots | Vasos de flores | Macetas
Seeds | Sementes | Semillas
Fertilizer (organic) | Fertilizante (orgânico) | Fertilizante (orgánico)
Watering cans | Regadores | Regaderas

## Personal Care | Cuidados Pessoais | Cuidado Personal

**English** | **Portuguese** | **Spanish**
---|---|---
Soap | Sabonete | Jabón
Shampoo | Xampu | Champú
Conditioner | Condicionador | Acondicionador
Toothbrush | Escova de dentes | Cepillo de dientes
Toothpaste | Pasta de dentes | Pasta de dientes
Deodorant | Desodorante | Desodorante
Lotion | Loção | Loción
Sunscreen | Protetor solar | Protector solar
Lip balm | Bálsamo labial | Bálsamo labial
Tissues | Lenços de papel | Pañuelos de papel
Cotton swabs | Cotonetes | Hisopos de algodón
Hair brushes | Escovas de cabelo | Cepillos para el cabello
Combs | Pentes | Peines
Nail clippers | Cortadores de unha | Cortauñas
Tweezers | Pinças | Pinzas
Razors | Barbeadores | Navajas de afeitar
Makeup | Maquiagem | Maquillaje
Perfume | Perfume | Perfume
Hair ties | Elásticos de cabelo | Ligas para el cabello
Bandages | Curativos | Vendajes
Vitamins | Vitaminas | Vitaminas

## Sports & Recreation | Esportes e Recreação | Deportes y Recreación

**English** | **Portuguese** | **Spanish**
---|---|---
Basketballs | Bolas de basquete | Pelotas de baloncesto
Soccer balls | Bolas de futebol | Pelotas de fútbol
Tennis balls | Bolas de tênis | Pelotas de tenis
Golf balls | Bolas de golfe | Pelotas de golf
Baseball bats | Tacos de beisebol | Bates de béisbol
Tennis rackets | Raquetes de tênis | Raquetas de tenis
Bicycles | Bicicletas | Bicicletas
Helmets | Capacetes | Cascos
Skateboards | Skates | Patinetas
Rollerblades | Patins inline | Patines en línea
Swimming goggles | Óculos de natação | Gafas de natación
Swimsuits | Maiôs | Trajes de baño
Yoga mats | Tapetes de yoga | Esterillas de yoga
Dumbbells | Halteres | Mancuernas
Jump ropes | Cordas de pular | Cuerdas de saltar
Frisbees | Frisbees | Frisbees
Playing cards | Cartas de jogar | Cartas de jugar
Board games | Jogos de tabuleiro | Juegos de mesa
Puzzles | Quebra-cabeças | Rompecabezas
Fishing rods | Varas de pescar | Cañas de pescar
Camping gear | Equipamentos de camping | Equipo de camping

## Arts & Crafts | Artes e Artesanato | Artes y Manualidades

**English** | **Portuguese** | **Spanish**
---|---|---
Paints | Tintas | Pinturas
Brushes | Pincéis | Pinceles
Canvas | Tela | Lienzo
Colored pencils | Lápis de cor | Lápices de colores
Watercolors | Aquarelas | Acuarelas
Clay | Argila | Arcilla
Glue | Cola | Pegamento
Scissors | Tesouras | Tijeras
Craft paper | Papel de artesanato | Papel de manualidades
Fabric | Tecido | Tela
Thread | Linha | Hilo
Needles | Agulhas | Agujas
Yarn | Fio | Hilo
Knitting needles | Agulhas de tricô | Agujas de tejer
Beads | Contas | Cuentas
Ribbon | Fita | Cinta
Stickers | Adesivos | Pegatinas
Stamps (craft) | Carimbos (artesanato) | Sellos (manualidades)
Ink pads | Almofadas de tinta | Almohadillas de tinta
Embroidery hoops | Bastidores de bordado | Bastidores de bordado

## Toys & Games | Brinquedos e Jogos | Juguetes y Juegos

**English** | **Portuguese** | **Spanish**
---|---|---
Dolls | Bonecas | Muñecas
Action figures | Bonecos de ação | Figuras de acción
Toy cars | Carrinhos de brinquedo | Coches de juguete
Building blocks | Blocos de construção | Bloques de construcción
Lego sets | Conjuntos de Lego | Sets de Lego
Stuffed animals | Bichos de pelúcia | Animales de peluche
Balls | Bolas | Pelotas
Kites | Pipas | Cometas
Coloring books | Livros de colorir | Libros para colorear
Crayons | Giz de cera | Crayones
Toy trains | Trens de brinquedo | Trenes de juguete
Marbles | Bolinhas de gude | Canicas
Spinning tops | Piões | Trompos
Yo-yos | Ioiôs | Yoyós
Jigsaw puzzles | Quebra-cabeças | Rompecabezas
Chess sets | Jogos de xadrez | Juegos de ajedrez
Checkers | Damas | Damas
Monopoly | Banco Imobiliário | Monopolio
Scrabble | Scrabble | Scrabble
Video games | Videogames | Videojuegos

## Musical Instruments | Instrumentos Musicais | Instrumentos Musicales

**English** | **Portuguese** | **Spanish**
---|---|---
Guitars | Violões | Guitarras
Keyboards | Teclados | Teclados
Drums | Baterias | Baterías
Flutes | Flautas | Flautas
Violins | Violinos | Violines
Trumpets | Trombetas | Trompetas
Harmonicas | Gaitas | Armónicas
Tambourines | Pandeiros | Panderetas
Recorders | Flautas doces | Flautas dulces
Maracas | Maracas | Maracas
Cymbals | Pratos | Platillos
Bells | Sinos | Campanas
Xylophones | Xilofones | Xilófonos
Banjos | Banjos | Banjos
Ukuleles | Ukuleles | Ukeleles
Saxophones | Saxofones | Saxofones
Clarinets | Clarinetes | Clarinetes
Pianos | Pianos | Pianos
Accordions | Sanfonas | Acordeones
Bongos | Bongôs | Bongos

## Office Supplies | Material de Escritório | Suministros de Oficina

**English** | **Portuguese** | **Spanish**
---|---|---
Printers | Impressoras | Impresoras
Scanners | Scanners | Escáneres
Photocopiers | Fotocopiadoras | Fotocopiadoras
Shredders | Trituradores | Trituradoras
Desk organizers | Organizadores de mesa | Organizadores de escritorio
Filing cabinets | Arquivos | Archivadores
Whiteboards | Quadros brancos | Pizarras blancas
Markers | Marcadores | Marcadores
Sticky notes | Notas adesivas | Notas adhesivas
Tape dispensers | Dispensadores de fita | Dispensadores de cinta
Hole punchers | Furadeiras | Perforadoras
Laminators | Laminadoras | Laminadoras
Label makers | Etiquetadoras | Etiquetadoras
Desk lamps | Lâmpadas de mesa | Lámparas de escritorio
Chairs | Cadeiras | Sillas
Desks | Mesas | Escritorios
Bookcases | Estantes | Estanterías
Bulletin boards | Quadros de avisos | Tableros de anuncios
Calendars | Calendários | Calendarios
Planners | Agendas | Planificadores
"""

# Classification
DEFAULT_MODEL = "gemini/gemini-2.5-flash"
INFO_EXTRACTOR_MODEL = "gemini/gemini-2.5-flash"
SEARCH_AGENT_MODEL = "gemini-2.5-flash" # Not using LiteLlm yet for SDS search agent due to reported issues in github


# File Paths
DATA_DIR = "data"
HAZMAT_DEFINITION_WITH_EXAMPLES_FILE = "data/hazmat-definition-with-examples.md"
HAZMAT_DEFINITION_FILE = "data/hazmat-definition.md"
