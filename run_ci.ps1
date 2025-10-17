param(
    [switch]$SkipAudit
)

function Resolve-Python {
    # Intenta 'py' (Windows Launcher) y luego 'python'
    $py = (Get-Command py -ErrorAction SilentlyContinue)
    if ($py) { return "py -3" }
    $python = (Get-Command python -ErrorAction SilentlyContinue)
    if ($python) { return "python" }
    Write-Error "No se encontró Python. Instala Python 3.11+ y vuelve a intentar."
    exit 1
}

$PY = Resolve-Python

Write-Host ">> Creando entorno virtual (.venv) si no existe..."
if (!(Test-Path ".\.venv")) {
    iex "$PY -m venv .venv"
}

$PIP = ".\.venv\Scripts\pip.exe"
$PYEXE = ".\.venv\Scripts\python.exe"

if (!(Test-Path $PIP)) {
    Write-Error "No se creó correctamente el venv. Revisa instalación de Python."
    exit 1
}

Write-Host ">> Actualizando pip e instalando dependencias..."
& $PYEXE -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { exit 1 }

& $PIP install -r requirements.txt
if ($LASTEXITCODE -ne 0) { exit 1 }

function Run-Step($name, $cmd) {
    Write-Host ">> $name"
    iex $cmd
    if ($LASTEXITCODE -ne 0) {
        Write-Error "$name falló (EXIT $LASTEXITCODE)."
        exit $LASTEXITCODE
    }
}

Run-Step "Ruff (lint)" ".\.venv\Scripts\ruff.exe check app"
Run-Step "Bandit (SAST)" ".\.venv\Scripts\bandit.exe -q -r app -x tests"

if (-not $SkipAudit) {
    Run-Step "pip-audit (dependencias)" ".\.venv\Scripts\pip-audit.exe --strict"
} else {
    Write-Host ">> Saltando pip-audit por --SkipAudit"
}

Run-Step "Pytest + cobertura (>=80%)" ".\.venv\Scripts\pytest.exe"

Write-Host ">> Listo. Cobertura HTML en coverage_html\index.html"
exit 0
