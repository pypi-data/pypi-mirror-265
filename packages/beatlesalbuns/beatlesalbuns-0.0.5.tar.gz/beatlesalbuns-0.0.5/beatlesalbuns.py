import pandas as pd

class BAlbuns:
    def __init__(self):
        #Criação de dicionário com a lista de Albuns dos Beatles
        self.balbums={'Name': ['1-Please Please Me',
                      '2-With The Beatles',
                      '3-A Hard Day\'s Night', 
                      '4-Beatles for Sale', 
                      '5-Help!', 
                      '6-Rubber Soul',
                      '7-Revolver',
                      '8-Sgt. Pepper\'s Lonely Hearts Club Band',
                      '9-Magical Mystery Tour',
                      '10-White Album',
                      '11-Yellow Submarine',
                      '12-Abbey Road',
                      '13-Let It Be'],
                    'Year': [1963, 1963, 1964, 1964, 1965, 1965, 1966, 1967, 1967, 1968, 1969, 1969, 1970]}
    # Método que mostra num dataframe os albuns do grupo The Beatles
    def show_albuns(self):
        #Converter dicionário numa Dataframe em Pandas
         print(f"=== Welcome! This is the list of The Beatles's albums ===".center(50))
         print(f"=== I love The Beatles!! ===\n".center(50))
         print(pd.DataFrame(self.balbums))
         return pd.DataFrame(self.balbums)
    # Método que mostra as estatísticas da lista de albuns, contam quanto albuns/ano
    def stats(self):
        print("Number of albuns per year")
        print(self.show_albuns().groupby("Year").count())
    # Método que apresenta os nome dos elementos da banda
    def band_members(self):
        print("""
            == Band Members ==
            Vocals and Bass - Paul McCartney
            Vocals and Guitar - John Lennon
            Guitar - George Harrison
            Drums - Ringo Starr
        \n""")
    # def info(self):
    #     print(self.show_albuns().info())

if __name__ == '__main__':
    #Instancia um objeto do tipo classe BAlbuns do módulo
    ls_albuns = BAlbuns()
    #invoca os métodos show_albuns(), stats(), band_members()
    ls_albuns.show_albuns()
    ls_albuns.band_members()
    ls_albuns.stats()
    #ls_albuns.info()

