# Requisitos
É recomendado utilizar ambientes virtuais para instalação de pacotes requeridos pelo projeto.

Utilizando `venv`:
```
python3 -m venv venv-name

# Windows
venv-name\Scripts\activate.bat    # cmd
venv-name\Scripts\activate.ps1    # Power Shell

# Unix
source venv-name/bin/activate
```
*Necessita `pip>=19.3` para instalação via [PyPl](https://pypi.org/project/pandas/)*
```
pip install pandas
```

```
pip install notebook
```

```
pip install matplotlib
pip install seaborn
```

```
# Para utilização do venv como kernel do Jupyter Notebook
pip install ipykernel

# Para instalar o novo kernel
ipython kernel install --user --name=venv-name
```