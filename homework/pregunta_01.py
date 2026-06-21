"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
import os
import glob

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    def normalizar(texto):
        texto=texto.strip()
        texto=texto.lower()
        return texto
    def espacios(texto):
        texto=texto.replace("_", " ")
        texto=texto.replace("-", " ")
        texto=texto.split()
        return (" ").join(texto)
    def plata(texto):
        texto=texto.replace(".00","")
        texto=texto.translate(str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"))
        return int(texto)
    
    df=pd.read_csv("files/input/solicitudes_de_credito.csv",sep=";",index_col=0)
    df=df.dropna()
    columnas=df.columns.to_list()
    
    for i in columnas:
        if i=="monto_del_credito":
            df[i]=df[i].apply(plata)

        if i=="fecha_de_beneficio":
            fecha_dm=pd.to_datetime(df[i], format="%d/%m/%Y", errors="coerce")
            fecha_am = pd.to_datetime(df[i], format="%Y/%m/%d", errors="coerce")
            df[i] = fecha_dm.fillna(fecha_am)
            
        if i in ["sexo", "tipo_de_emprendimiento", "idea_negocio", "línea_credito"]:
            df[i]=df[i].apply(normalizar)
        
        if i in ["idea_negocio", "línea_credito"]:
            df[i]=df[i].apply(espacios)
        
        if i=="barrio":
            df[i]=df[i].str.lower().str.replace("-", " ").str.replace("_", " ")
        
        if i in ["comuna_ciudadano", "estrato"]:
            df[i]=df[i].astype(int)

        
    df.drop_duplicates(inplace=True)
    
    if os.path.exists("files/output/"):
        for file in glob.glob(f"files/output/*"):
            os.remove(file)
    else:
        os.makedirs("files/output")
    
    df.to_csv(
        f"{"files/output"}/solicitudes_de_credito.csv",
        sep=";",
        index=False,
        header=True,
        )
    

if __name__ == "__main__":
    pregunta_01()