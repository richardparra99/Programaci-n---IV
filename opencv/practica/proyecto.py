print("Consulta1")
alquiler = abrir_tabla(tablas,"alquiler")
cliente = abrir_tabla(tablas,"cliente")
pais = abrir_tabla(tablas,"pais")
print(pais)
VC = pd.merge (alquiler,cliente,left_on ='id_cliente',right_on='id_cliente',how='inner')
VC = pd.merge (VC,pais,left_on ='id_pais',right_on='id',how='inner')


df= pd.read_excel(tablas)
print(df.head())

resultado1 = df[['fecha_compra','monto','id_cliente','nombre_cliente','nombre_pais']]
print(VC[resultado1].to_string(index = False))

ax = resultado1.plot.bar(x ="id_cliente",y="nombre_pais", rot=0)
plt.show()

#df= pd.read_excel(tablas)

#print(df.head())

#valores = df[["id_cliente","edad"]]
#print(valores)

#ax = 
valores.plot.bar(x="id_cliente", y="edad",rot = 0)
#
plt.show
()
#print("tabla 2")
#df1 = pd.read_excel(tablas, sheet_name='anime')
#print(df) 