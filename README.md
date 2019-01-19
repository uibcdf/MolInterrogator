# TargetInterrogator

# What will be this?

- La entrada debe poder ser un termino general o un pdb. Si el pdb tiene ligando... la información
  que saca esta librería se circunscribe a ese ligando, o no.
- Interacciones protein-proteina:
	- Interfases
	- protein con las que forma complejo
	- Posible structura terciaria y cuaternaria
- La lista de ligandos reportados:
	- información de inhibición, reglas lipinski, propiedades físicas, etc..
	- posiblidad de sacar analogos del conjunto de ligandos reportados
	- que pudieran sacar farmacóforos de estos ligandos
	- que estos farmacóforos puedan cribar quimiotecas
- Ruta metabólica o porcesos metabolicos en los que está implicado
- 


TargetInterrogator is the python wrapper or platform to get information of a given target from
databases and servers. This information should be realted with:

- Set of reported compounds: IC50, Binding affinity, etc.
- Set of Protein-Protein interactions.
- ...
