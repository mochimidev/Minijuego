# Minijuego

Videojuego 2D desarrollado en Unity para el Taller de Desarrollo de Videojuegos. El proyecto presenta una experiencia de plataformas con escenarios progresivos, coleccionables, contador de tiempo, contador de intentos y sistema de finalizacion por nivel.

## Capturas del videojuego

Las siguientes capturas fueron generadas a partir de las escenas y assets reales incluidos en el proyecto.

| Menu principal | Nivel 1 |
| --- | --- |
| ![Menu principal](docs/screenshots/menu-principal.png) | ![Nivel 1](docs/screenshots/nivel-1.png) |

| Desafio con obstaculos | Nivel avanzado |
| --- | --- |
| ![Nivel 3](docs/screenshots/nivel-3.png) | ![Nivel 5](docs/screenshots/nivel-5.png) |

## Descripcion

Minijuego es una propuesta de plataformas 2D donde el jugador debe avanzar por distintos niveles, evitar peligros, recolectar diamantes y llegar al punto final de cada escena. La experiencia combina desplazamiento lateral, saltos, zonas de doble salto, enemigos, plataformas y una interfaz que registra el rendimiento durante la partida.

El juego incluye un menu principal, panel de creditos, menu de pausa y pantalla final de nivel con resumen de intentos, diamantes y tiempo.

## Caracteristicas principales

- Movimiento horizontal y salto mediante fisicas 2D.
- Sistema de doble salto en zonas especificas.
- Recoleccion de diamantes.
- Enemigos y zonas de muerte con reinicio del jugador.
- Contador de tiempo por intento y tiempo acumulado.
- Contador de intentos.
- Pantalla de finalizacion de nivel.
- Menu principal, creditos y menu de pausa.
- Cinco escenas de nivel incluidas en el build.

## Controles

| Accion | Tecla / Entrada |
| --- | --- |
| Mover al jugador | Flechas izquierda/derecha o eje horizontal configurado en Unity |
| Saltar | Barra espaciadora o boton `Jump` |
| Descender con impulso en el aire | Flecha abajo o eje vertical negativo |
| Pausar / reanudar | `Esc` o boton `Cancel` |

## Escenas incluidas

- `MenuPrincipal`
- `nivel1`
- `nivel2`
- `nivel3`
- `nivel4`
- `nivel5`

## Requisitos

- Unity `2021.3.11f1`
- TextMeshPro `3.0.6`
- Cinemachine `2.8.9`
- Soporte 2D de Unity

## Como ejecutar el proyecto

1. Clonar o descargar este repositorio.
2. Abrir la carpeta del proyecto desde Unity Hub.
3. Usar Unity `2021.3.11f1` o una version compatible de Unity 2021 LTS.
4. Abrir la escena `Assets/Scenes/MenuPrincipal.unity`.
5. Presionar `Play` en el editor.

## Estructura del proyecto

```text
Assets/
  Images/          Sprites, fondos e iconos del videojuego
  Prefabs/         Jugador, plataformas, enemigos, UI y elementos de nivel
  Scenes/          Menu principal y niveles jugables
  Scripts/         Logica de movimiento, menus, contadores y eventos
Packages/          Dependencias del proyecto Unity
ProjectSettings/   Configuracion general del proyecto
docs/screenshots/  Capturas usadas en este README
```

## Autores

- [Gabriel Barrientos](https://github.com/pinguin-frosch)
- [Charlotte Rodriguez](https://github.com/Thekawaiicokie)

## Contexto academico

Proyecto creado para el Taller de Desarrollo de Videojuegos.
