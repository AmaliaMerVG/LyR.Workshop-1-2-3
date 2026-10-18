# LyR Workshop 1-2-3

Talleres de algoritmos aleatorizados, streaming y grafos aplicados al rastreo de equipaje aéreo.

| Carpeta | Contenido |
|---|---|
| `whorkshop1/` | Muestreo aleatorio, QuickSort, hashing universal, Power of Two Choices, desigualdad de Markov |
| `whorkshop2/` | Bloom Filter, muestreo por hash, HyperLogLog, AMS Sketch |
| `whorkshop3/` | Cadenas de Markov, distribución estacionaria, PageRank, caminata aleatoria, 2-SAT |

El proyecto usa **Python 3.11.8** y las librerías listadas en `requirements.txt`.

- [macOS / Linux](#macos--linux)
- [Windows](#windows)
- [Ejecutar los talleres](#ejecutar-los-talleres)

---

## macOS / Linux

### Requisitos previos

- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) (plugin de pyenv para crear entornos virtuales)

En macOS se pueden instalar con Homebrew:

```bash
brew install pyenv pyenv-virtualenv
```

Y agregar al final de `~/.zshrc` (luego abrir una terminal nueva o ejecutar `source ~/.zshrc`):

```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

### Crear el ambiente

Todos los comandos se ejecutan desde la raíz del repositorio.

1. Instalar Python 3.11.8 (si ya está instalado, este paso se puede omitir):

   ```bash
   pyenv install 3.11.8
   ```

2. Crear el entorno virtual del proyecto:

   ```bash
   pyenv virtualenv 3.11.8 lyr-workshop-env
   ```

3. Asociar el entorno a la carpeta del proyecto. Esto crea un archivo `.python-version` y activa el entorno automáticamente cada vez que se entra al repositorio:

   ```bash
   pyenv local lyr-workshop-env
   ```

4. Instalar las librerías:

   ```bash
   pip install -r requirements.txt
   ```

5. Verificar la instalación:

   ```bash
   python --version   # Python 3.11.8
   python -c "import numpy, pandas, matplotlib, seaborn; print('OK')"
   ```

### Eliminar el ambiente

```bash
pyenv uninstall lyr-workshop-env
rm .python-version
```

---

## Windows

En Windows se usa [pyenv-win](https://github.com/pyenv-win/pyenv-win), la versión de pyenv para Windows. Como pyenv-win no incluye el plugin de entornos virtuales, el entorno se crea con el módulo `venv` que ya trae Python.

Todos los comandos son para **PowerShell**.

### Requisitos previos

1. Desactivar los alias de Python de la Microsoft Store, que interfieren con pyenv-win:
   *Configuración → Aplicaciones → Configuración avanzada de aplicaciones → Alias de ejecución de aplicaciones* y desactivar **python.exe** y **python3.exe**.

2. Permitir la ejecución de scripts locales para el usuario actual (necesario para instalar pyenv-win y activar el entorno):

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. Instalar pyenv-win:

   ```powershell
   Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
   ```

4. Cerrar y volver a abrir PowerShell, y comprobar que funciona:

   ```powershell
   pyenv --version
   ```

### Crear el ambiente

Todos los comandos se ejecutan desde la raíz del repositorio.

1. Instalar Python 3.11.8 (si ya está instalado, este paso se puede omitir):

   ```powershell
   pyenv install 3.11.8
   ```

2. Fijar esa versión para la carpeta del proyecto (crea el archivo `.python-version`):

   ```powershell
   pyenv local 3.11.8
   ```

3. Crear el entorno virtual dentro del proyecto:

   ```powershell
   python -m venv .venv
   ```

4. Activar el entorno (hay que hacerlo cada vez que se abre una terminal nueva). Al activarse, el prompt muestra `(.venv)`:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   > Si se usa **CMD** en lugar de PowerShell: `.venv\Scripts\activate.bat`

5. Instalar las librerías:

   ```powershell
   pip install -r requirements.txt
   ```

6. Verificar la instalación:

   ```powershell
   python --version   # Python 3.11.8
   python -c "import numpy, pandas, matplotlib, seaborn; print('OK')"
   ```

### Eliminar el ambiente

```powershell
deactivate
Remove-Item -Recurse -Force .venv
Remove-Item .python-version
```

---

## Ejecutar los talleres

Con el ambiente activo, cada script se ejecuta desde dentro de su carpeta, porque lee los archivos `.json` que están ahí:

```bash
cd whorkshop1
python workshop1_task1.py
python workshop1_dashboard.py
```

Los dashboards y `workshop2_task4.py` guardan una imagen `.png` y además abren una ventana con la gráfica.
