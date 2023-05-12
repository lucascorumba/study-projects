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


def nan_targets(val, cols):
	"""
	Recebe um pandas.Series (val) e uma lista com colunas (cols).
	Retorna uma lista contendo valores que serão substituidos.
	"""
	to_replace = list()
	for col in cols:
		to_replace.append(val[col])
	return to_replace