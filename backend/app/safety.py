import re

RED_FLAG_PATTERNS = [
    # Cardiovascular emergencies
    r"dor\s+(forte\s+)?(no|do)\s+peito",
    r"aperto\s+no\s+peito",
    r"dor\s+peitoral",
    r"enfarte",
    r"ataque\s+card[ií]aco",
    # Stroke
    r"dormência\s+(de\s+um\s+lado|unilateral|no\s+braço\s+e\s+perna)",
    r"confusão\s+s[úu]bita",
    r"perda\s+de\s+fala",
    r"avc",
    r"derrame\s+cerebral",
    r"paralisia\s+facial",
    # Respiratory
    r"falta\s+de\s+ar\s+(intensa|grave|severa|s[úu]bita)",
    r"não\s+consigo\s+respirar",
    r"dificuldade\s+(grave\s+)?em\s+respirar",
    r"sufocamento",
    # Allergic reaction
    r"anafilax",
    r"alergia\s+grave",
    r"inchaço\s+(da|na)\s+(garganta|l[ií]ngua|face)",
    # Mental health
    r"suic[ií]d",
    r"matar[-\s]me",
    r"acabar\s+com\s+(a\s+)?(minha\s+)?vida",
    r"auto[-\s]?les[ãa]o",
    r"quero\s+morrer",
    # Severe injury
    r"hemorragia\s+(grave|intensa|incontrol[áa]vel)",
    r"perda\s+de\s+consci[êe]ncia",
    r"desmai(o|ar|ei)",
    r"convuls",
    # Poisoning
    r"envenenamento",
    r"ingest[ãa]o\s+de\s+(produto|substância)",
    r"overdose",
]

_compiled_patterns = [re.compile(p, re.IGNORECASE) for p in RED_FLAG_PATTERNS]

RED_FLAG_MESSAGE = (
    "⚠️ **ATENÇÃO — POSSÍVEL EMERGÊNCIA MÉDICA**\n\n"
    "Os sintomas que descreves podem indicar uma situação que requer "
    "avaliação médica urgente.\n\n"
    "**Liga imediatamente para:**\n"
    "- 🇵🇹 **112** (Portugal — INEM)\n"
    "- 🇧🇷 **192** (Brasil — SAMU)\n"
    "- Ou dirige-te às urgências do hospital mais próximo\n\n"
    "O Dr. Silvério é um assistente educativo e **não substitui** "
    "atendimento médico de emergência. A tua segurança é a prioridade."
)

MENTAL_HEALTH_MESSAGE = (
    "💙 **Estou aqui para ti.**\n\n"
    "Se estás a passar por um momento difícil, por favor contacta:\n"
    "- 🇵🇹 **SOS Voz Amiga**: 213 544 545 (16h-24h)\n"
    "- 🇵🇹 **SNS 24**: 808 24 24 24\n"
    "- 🇧🇷 **CVV**: 188 (24h)\n"
    "- **Linha de emergência**: 112\n\n"
    "Não estás sozinho/a. Procura ajuda profissional."
)

MENTAL_HEALTH_PATTERNS = [
    r"suic[ií]d",
    r"matar[-\s]me",
    r"acabar\s+com\s+(a\s+)?(minha\s+)?vida",
    r"auto[-\s]?les[ãa]o",
    r"quero\s+morrer",
]
_mental_patterns = [re.compile(p, re.IGNORECASE) for p in MENTAL_HEALTH_PATTERNS]


def check_red_flags(text: str) -> tuple[bool, str | None]:
    """Check user message for red flags. Returns (is_red_flag, message)."""
    for pattern in _mental_patterns:
        if pattern.search(text):
            return True, MENTAL_HEALTH_MESSAGE

    for pattern in _compiled_patterns:
        if pattern.search(text):
            return True, RED_FLAG_MESSAGE

    return False, None
