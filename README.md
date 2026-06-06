# Midnight Costume Quest

Videojuego 2D de plataformas desarrollado en Unity. La base jugable conserva movimiento lateral, salto, doble salto, obstaculos, coleccionables, cronometro, intentos y progresion de niveles.

Este rediseño propone una nueva identidad visual y narrativa: Mara Midnight, una chica pastel goth, debe recuperar las piezas de su disfraz antes de la Competencia de Halloween.

## Estado de assets

No se incluyen assets placeholder. Los PNG ilustrados finales deben producirse como arte 2D original antes de reemplazar los sprites actuales.

Carpeta objetivo para la produccion final:

```text
Assets/Images/MidnightCostumeQuest/
```

## Concepto

La noche anterior a la competencia, una tormenta magica dispersa las piezas del disfraz de Mara por distintos escenarios de Halloween. El jugador debe atravesar niveles, evitar peligros, recolectar piezas y llegar a la meta antes del evento.

## Progresion

- Nivel 1: Cementerio Fashion, sombrero de bruja.
- Nivel 2: Mercado de Halloween, collar de murcielago.
- Nivel 3: Bosque de la Luna, botines encantados.
- Nivel 4: Mansion Encantada, capa magica.
- Nivel 5: Plaza del Festival, maquillaje especial.

Coleccionables secundarios:

- Dulces.
- Calabazas.
- Estrellas.
- Murcielagos magicos.

## Direccion artistica

- Pastel goth.
- Spooky cute.
- Halloween fashion.
- Chibi detallado.
- Paleta: lavanda, morado oscuro, negro suave, rosa empolvado, naranja otonal y dorado.
- Estilo indie comercial para Itch.io o Steam.

Restricciones visuales:

- No copiar Monster High, Disney, Sanrio, Tamagotchi ni personajes existentes.
- No reutilizar ni simplificar PNG actuales.
- No usar fondos planos, rectangulos basicos ni composiciones vacias.

## Lista de produccion visual

Personaje:

- Sprite sheet 2D de Mara Midnight.
- Idle, walk, jump, fall, hurt y victory.
- Cabello negro con mechas moradas.
- Ropa alternativa, botines, medias rayadas y accesorios Halloween fashion.

Fondos parallax:

- Cementerio Fashion.
- Mercado de Halloween.
- Bosque de la Luna.
- Mansion Encantada.
- Plaza del Festival.

Tilesets:

- Plataformas de piedra gotica.
- Rejas.
- Tumbas decorativas.
- Faroles.
- Escaleras.
- Puentes.
- Suelo con detalles.
- Bordes y esquinas.

Coleccionables:

- Sombrero de bruja.
- Collar murcielago.
- Botines encantados.
- Capa magica.
- Maquillaje especial.
- Dulces.
- Calabazas.
- Estrellas.

Enemigos:

- Fantasma kawaii.
- Murcielago.
- Calabaza viviente.
- Muneca espeluznante cute.

UI:

- Menu principal.
- Botones.
- HUD con vidas, tiempo y coleccionables.
- Pantalla de pausa.
- Pantalla final de nivel.
- Pantalla de victoria.

## Caracteristicas jugables conservadas

- Movimiento horizontal y salto mediante fisicas 2D.
- Sistema de doble salto en zonas especificas.
- Recoleccion de objetos.
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

## Requisitos

- Unity `2021.3.11f1`
- TextMeshPro `3.0.6`
- Cinemachine `2.8.9`
- Soporte 2D de Unity

## Como ejecutar desde Unity

1. Abrir la carpeta del proyecto desde Unity Hub.
2. Usar Unity `2021.3.11f1` o una version compatible de Unity 2021 LTS.
3. Abrir la escena `Assets/Scenes/MenuPrincipal.unity`.
4. Presionar `Play` en el editor.

## Creditos

- Estructura base: Charlotte y Gabriel Barrientos.
- Rediseño visual y narrativo propuesto: Midnight Costume Quest.
- [Gabriel Barrientos](https://github.com/pinguin-frosch)
- [Charlotte Rodriguez](https://github.com/Thekawaiicokie)
