$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$unityProjectVersionFile = Join-Path $projectRoot "ProjectSettings\ProjectVersion.txt"
$buildOutput = Join-Path $projectRoot "dist\windows\Minijuego.exe"
$installerScript = Join-Path $projectRoot "installer\Minijuego.iss"

function Find-Unity {
    $versionLine = Get-Content $unityProjectVersionFile | Where-Object { $_ -like "m_EditorVersion:*" } | Select-Object -First 1
    $version = ($versionLine -replace "m_EditorVersion:\s*", "").Trim()

    $candidates = @(
        "C:\Program Files\Unity\Hub\Editor\$version\Editor\Unity.exe",
        "C:\Program Files\Unity\Editor\Unity.exe"
    )

    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            return $candidate
        }
    }

    $command = Get-Command Unity.exe -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    throw "No se encontro Unity. Instala Unity $version o agrega Unity.exe al PATH."
}

function Find-InnoSetup {
    $candidates = @(
        "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        "C:\Program Files\Inno Setup 6\ISCC.exe"
    )

    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            return $candidate
        }
    }

    $command = Get-Command ISCC.exe -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    return $null
}

$unityExe = Find-Unity

Write-Host "Compilando build de Windows con Unity..."
& $unityExe `
    -batchmode `
    -quit `
    -projectPath $projectRoot `
    -executeMethod BuildWindows.Build `
    -logFile (Join-Path $projectRoot "dist\unity-build.log")

if (-not (Test-Path $buildOutput)) {
    throw "Unity termino sin generar $buildOutput. Revisa dist\unity-build.log."
}

$iscc = Find-InnoSetup
if (-not $iscc) {
    Write-Host "Build generado en dist\windows, pero no se encontro Inno Setup para crear el instalador."
    Write-Host "Instala Inno Setup 6 y vuelve a ejecutar este script."
    exit 0
}

Write-Host "Generando instalador con Inno Setup..."
& $iscc $installerScript

Write-Host "Listo: dist\installer\Minijuego-Setup-1.0.exe"
