class Language:
    def __init__(self, name: str, iso2: str):
        self.name = name
        self.iso2 = iso2


Language.ENGLISH = Language('English', 'en')
Language.SINHALA = Language('Sinhala', 'si')
Language.TAMIL = Language('Tamil', 'ta')
Language.SPANISH = Language('Spanish', 'es')
