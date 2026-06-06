estructura base charlotte y gabirel barrientos estructura visual y tematica neuva charlotte rodriguez

# Minijuego

Videojuego 2D desarrollado en Unity como proyecto academico del Taller de Desarrollo de Videojuegos. La version actual presenta una experiencia de plataformas con menu principal, niveles progresivos, coleccionables, enemigos, zonas de muerte, contador de tiempo, contador de intentos y pantalla final de nivel.

El proyecto tambien funciona como base para una futura reinterpretacion visual y tematica con identidad cozy, alternativa, pastel goth y Halloween adorable.

## Interfaz actual

Las siguientes capturas muestran la interfaz y los escenarios reales incluidos actualmente en el proyecto.

### Menu principal

<img src="docs/screenshots/menu-principal.png" alt="Menu principal actual del videojuego" width="100%">

### Nivel 1

<img src="docs/screenshots/nivel-1.png" alt="Primer nivel jugable" width="100%">

### Nivel con obstaculos

<img src="docs/screenshots/nivel-3.png" alt="Nivel con plataformas, obstaculos y contador de progreso" width="100%">

### Nivel avanzado

<img src="docs/screenshots/nivel-5.png" alt="Nivel avanzado del videojuego" width="100%">

## Descripcion del juego actual

Minijuego es una propuesta de plataformas 2D donde el jugador debe avanzar por distintos niveles, evitar peligros, recolectar diamantes y llegar al punto final de cada escena. La experiencia combina desplazamiento lateral, saltos, zonas de doble salto, enemigos, plataformas y una interfaz que registra el rendimiento durante la partida.

El juego incluye menu principal, panel de creditos, menu de pausa y pantalla final de nivel con resumen de intentos, diamantes y tiempo.

## Caracteristicas principales

- Movimiento horizontal y salto mediante fisicas 2D.
- Sistema de doble salto en zonas especificas.
- Recoleccion de diamantes.
- Enemigos y zonas de muerte con reinicio del jugador.
- Contador de tiempo por intento y tiempo acumulado.
- Contador de intentos.
- Pantalla de finalizacion de nivel.
- Menu principal, creditos y menu de pausa.
- Cinco escenas de nivel incluidas en la configuracion de build.

## Controles

- **Mover al jugador:** flechas izquierda/derecha o eje horizontal configurado en Unity.
- **Saltar:** barra espaciadora o boton `Jump`.
- **Descender con impulso en el aire:** flecha abajo o eje vertical negativo.
- **Pausar / reanudar:** `Esc` o boton `Cancel`.

## Escenas incluidas

- `MenuPrincipal`
- `nivel1`
- `nivel2`
- `nivel3`
- `nivel4`
- `nivel5`

## Requisitos del proyecto

- Unity `2021.3.11f1`
- TextMeshPro `3.0.6`
- Cinemachine `2.8.9`
- Soporte 2D de Unity

## Como ejecutar desde Unity

1. Clonar o descargar este repositorio.
2. Abrir la carpeta del proyecto desde Unity Hub.
3. Usar Unity `2021.3.11f1` o una version compatible de Unity 2021 LTS.
4. Abrir la escena `Assets/Scenes/MenuPrincipal.unity`.
5. Presionar `Play` en el editor.

## Build e instalador para Windows

Este repositorio incluye archivos preparados para generar una version instalable para Windows:

- `Assets/Editor/BuildWindows.cs`: compila el juego para Windows desde Unity en modo batch.
- `tools/BuildWindows.ps1`: ejecuta Unity, genera el build y, si Inno Setup esta instalado, crea el instalador.
- `installer/Minijuego.iss`: configuracion del instalador para Inno Setup.

Para generar el build y el instalador:

```powershell
powershell -ExecutionPolicy Bypass -File tools/BuildWindows.ps1
```

El instalador final se genera en:

```text
dist/installer/Minijuego-Setup-1.0.exe
```

Nota: para crear el instalador es necesario tener Unity instalado con soporte Windows y tener Inno Setup disponible en el equipo. Si Unity o Inno Setup no estan instalados, el script mostrara el paso que falta.

## Estructura del proyecto

```text
Assets/
  Editor/          Script de build para Windows
  Images/          Sprites, fondos e iconos del videojuego
  Prefabs/         Jugador, plataformas, enemigos, UI y elementos de nivel
  Scenes/          Menu principal y niveles jugables
  Scripts/         Logica de movimiento, menus, contadores y eventos
Packages/          Dependencias del proyecto Unity
ProjectSettings/   Configuracion general del proyecto
docs/screenshots/  Capturas usadas en este README
installer/         Script para generar el instalador de Windows
tools/             Automatizacion de build
```

## Creditos

- Estructura base: Charlotte y Gabriel Barrientos.
- Estructura visual y tematica nueva: Charlotte Rodriguez.
- [Gabriel Barrientos](https://github.com/pinguin-frosch)
- [Charlotte Rodriguez](https://github.com/Thekawaiicokie)

## Contexto academico

Proyecto creado para el Taller de Desarrollo de Videojuegos.
