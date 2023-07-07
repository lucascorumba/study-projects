from numpy import NaN

# dict {Estado: UF}
uf_dict = {
	'Acre': 'AC',
	'Alagoas': 'AL',
	'Amapá': 'AP',
	'Amazonas': 'AM',
	'Bahia': 'BA',
	'Ceará': 'CE',
	'Distrito Federal': 'DF',
	'Espírito Santo': 'ES',
	'Goiás': 'GO',
	'Maranhão': 'MA',
	'Mato Grosso': 'MT',
	'Mato Grosso do Sul': 'MS',
	'Minas Gerais': 'MG',
	'Pará': 'PA',
	'Paraíba': 'PB',
	'Paraná': 'PR',
	'Pernambuco': 'PE',
	'Piauí': 'PI',
	'Rio de Janeiro': 'RJ',
	'Rio Grande do Norte': 'RN',
	'Rio Grande do Sul': 'RS',
	'Rondônia': 'RO',
	'Roraima': 'RR',
	'Santa Catarina': 'SC',
	'São Paulo': 'SP',
	'Sergipe': 'SE',
	'Tocantins': 'TO',
	'GOIAS': 'GO'
}

# dict {UF: Região}
region_dict =  {
	'AC': 'Norte', 'AM': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'AP': 'Norte', 'PA': 'Norte', 'TO': 'Norte',
	'MA': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'CE': 'Nordeste', 'PB': 'Nordeste', 'BA': 'Nordeste',
	'PE': 'Nordeste', 'AL': 'Nordeste', 'SE': 'Nordeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste',
	'MS': 'Centro-Oeste', 'DF': 'Centro-Oeste',	'MG': 'Sudeste', 'SP': 'Sudeste', 'ES': 'Sudeste', 'RJ': 'Sudeste',
	'PR': 'Sul', 'SC': 'Sul', 'RS': 'Sul'
}

# df.apply(lambda x: utils.get_region(x, utils.region_dict))
def get_region(uf, dict):
	"""
	Retorna a região à qual a UF fornecida pertence
	"""
	if uf in dict:
		return dict[uf]
	return uf

# df.apply(lambda x: utils.get_uf(x, utils.uf_dict))
def get_uf(state, dict):
	"""
	Retorna UF de acordo com nome do estado.
	"""
	if state in dict:
		return dict[state]
	return state


def check_int(val):
	"""
	Recebe um valor numérico.
	Caso seja contínuo: retorna NaN
	Caso seja discreto: retorna o valor recebido
	"""
	try:
		temp = int(val)
	# Lida com casos onde val = NaN
	except ValueError:
		return NaN
	if val != temp:
		return NaN
	return temp


def check_negative(val):
	"""
	Recebe um valor numérico.
	Para valores menores que "0", retorna NaN.
	Caso contrário, retorna o valor recebido.
	"""
	if val < 0:
		return NaN
	return val


def big_small(a, b):
	"""
	Recebe dois valores numéricos.
	Retorna uma tupla com os mesmos valores
	ordenados em (maior, menor).
	"""
	if a > b:
		return a, b
	return b, a

def clear_lists(*args):
	"""
	Recebe uma quantidade variável de listas.
	Apaga os dados de todas elas.
	"""
	for arg in args:
		arg.clear()