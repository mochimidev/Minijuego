# Minijuego

Videojuego 2D desarrollado originalmente en Unity para el Taller de Desarrollo de Videojuegos. El proyecto presenta una experiencia de plataformas con escenarios progresivos, coleccionables, contador de tiempo, contador de intentos y sistema de finalización por nivel.

## Evolución del proyecto

Este repositorio conserva la estructura base desarrollada durante el proyecto académico original por Gabriel Barrientos y Charlotte Rodriguez.

Actualmente el proyecto se encuentra en proceso de rediseño visual y conceptual por Charlotte Rodriguez, incorporando una nueva dirección artística, mejoras de experiencia de usuario, modernización de la interfaz y una temática completamente renovada orientada al coleccionismo, exploración y personalización.

### Créditos de desarrollo

**Estructura base y desarrollo académico**

* Gabriel Barrientos
* Charlotte Rodriguez

**Rediseño visual, dirección artística y evolución del proyecto**

* Charlotte Rodriguez

## Nueva temática

La nueva versión transforma el juego de plataformas tradicional en una experiencia de exploración con estética cozy, spooky cute y pastel goth.

La protagonista debe recorrer distintos escenarios inspirados en otoño y Halloween para encontrar objetos decorativos que permitirán personalizar y mejorar su habitación.

Los coleccionables incluyen:

* Labiales alternativos
* Delineadores
* Peluches
* Decoraciones de Halloween
* Vinilos
* Posters
* Lámparas de luna
* Velas aromáticas
* Accesorios decorativos

Cada objeto desbloqueado aparece visualmente dentro de la habitación del jugador, permitiendo observar su progreso a medida que avanza por los niveles.

## Objetivos de la actualización

* Modernizar la estética general.
* Mejorar la interfaz de usuario.
* Incorporar progresión visual.
* Añadir coleccionables con utilidad real.
* Crear una identidad artística propia.
* Convertir el proyecto en una pieza de portafolio profesional.

## Características principales

* Movimiento horizontal y salto mediante físicas 2D.
* Sistema de doble salto.
* Recolección de objetos especiales.
* Enemigos y obstáculos.
* Contador de tiempo.
* Contador de intentos.
* Pantalla de finalización de nivel.
* Sistema de progreso de habitación.
* Menú principal y menú de pausa.
* Múltiples niveles explorables.


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
