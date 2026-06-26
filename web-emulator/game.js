const canvas = document.querySelector("#game");
const ctx = canvas.getContext("2d");
const overlay = document.querySelector("#overlay");
const startBtn = document.querySelector("#startBtn");
const continueBtn = document.querySelector("#continueBtn");
const optionsBtn = document.querySelector("#optionsBtn");
const creditsBtn = document.querySelector("#creditsBtn");
const exitBtn = document.querySelector("#exitBtn");
const levelNameEl = document.querySelector("#levelName");
const itemsEl = document.querySelector("#items");
const livesEl = document.querySelector("#lives");
const timeEl = document.querySelector("#time");
const itemIconsEl = document.querySelector("#itemIcons");
const objectiveEl = document.querySelector("#objective");
document.body.classList.add("menu-mode");

const W = 1024;
const H = 576;
const SAVE_KEY = "moonParcelSaveV1";
const keys = new Set();
const images = new Map();
const missingAssets = new Set();
const ASSET_VERSION = new URLSearchParams(window.location.search).get("assetVersion") || `external-${Date.now()}`;
const asset = (path) => `./assets/${path}?v=${ASSET_VERSION}`;
const PLACEHOLDER_ASSET = asset("ui/PENDIENTE_ASSET.png");

const externalAssets = {
  rooms: {
    menu: asset("rooms/menu_main.png"),
    bedroom: asset("rooms/bedroom_initial.png"),
    hallway: asset("rooms/hallway_strange.png"),
    library: asset("rooms/library_enchanted.png"),
    mirror: asset("rooms/mirror_room.png"),
    garden: asset("rooms/garden_night.png"),
    cemetery: asset("rooms/cemetery.png"),
    party: asset("rooms/halloween_salon.png"),
  },
  characters: {
    idleDown: asset("characters/charlotte_idle_down.png"),
    idleUp: asset("characters/charlotte_idle_up.png"),
    idleSide: asset("characters/charlotte_idle_side.png"),
    walkDown1: asset("characters/charlotte_walk_down_1.png"),
    walkDown2: asset("characters/charlotte_walk_down_2.png"),
    walkUp1: asset("characters/charlotte_walk_up_1.png"),
    walkUp2: asset("characters/charlotte_walk_up_2.png"),
    walkSide1: asset("characters/charlotte_walk_side_1.png"),
    walkSide2: asset("characters/charlotte_walk_side_2.png"),
    interact: asset("characters/charlotte_interact.png"),
    surprise: asset("characters/charlotte_surprise.png"),
    holdPackage: asset("characters/charlotte_hold_package.png"),
    celebrate: asset("characters/charlotte_celebrate.png"),
  },
  portraits: {
    neutral: asset("portraits/charlotte_neutral.png"),
    surprise: asset("portraits/charlotte_surprise.png"),
  },
  objects: {
    bed: asset("objects/bed.png"),
    bookshelf: asset("objects/bookshelf.png"),
    books: asset("objects/open_spellbook.png"),
    cemeteryGate: asset("objects/cemetery_gate.png"),
    chair: asset("objects/chair.png"),
    clothesRack: asset("objects/clothes_hanging.png"),
    desk: asset("objects/desk.png"),
    doll: asset("objects/doll.png"),
    door: asset("objects/door.png"),
    finalTable: asset("objects/final_table.png"),
    ghost: asset("objects/ghost.png"),
    lamp: asset("objects/lamp.png"),
    makeup: asset("objects/makeup.png"),
    mirror: asset("objects/mirror_full.png"),
    moonFlowers: asset("objects/moon_flowers.png"),
    package: asset("objects/package_glow.png"),
    painting: asset("objects/haunted_painting.png"),
    photoCluster: asset("objects/photo_cluster.png"),
    plant: asset("objects/plant.png"),
    posterSet: asset("objects/poster_set.png"),
    plushes: asset("objects/plushes.png"),
    roundRug: asset("objects/round_rug.png"),
    shelves: asset("objects/wall_shelves.png"),
    shadow: asset("objects/shadow.png"),
    window: asset("objects/window_rain.png"),
  },
  ui: {
    dialogBox: asset("ui/dialog_box.png"),
    heartEmpty: asset("ui/heart_empty.png"),
    heartFull: asset("ui/heart_full.png"),
    inventoryPanel: asset("ui/inventory_panel.png"),
    inventorySlot: asset("ui/inventory_slot.png"),
    panel: asset("ui/panel.png"),
    selector: asset("ui/selector.png"),
    iconAccessory: asset("ui/icon_accessory.png"),
    iconBoots: asset("ui/icon_boots.png"),
    iconCape: asset("ui/icon_cape.png"),
    iconHat: asset("ui/icon_hat.png"),
    iconInvitation: asset("ui/icon_invitation.png"),
    iconKey: asset("ui/icon_key.png"),
    iconPackage: asset("ui/icon_package.png"),
    iconWand: asset("ui/icon_wand.png"),
  },
  tilesets: {
    interior: asset("tilesets/interior_room_tileset.png"),
  },
};

const sceneAssets = {
  menu: externalAssets.rooms.menu,
  bedroom: externalAssets.rooms.bedroom,
  hallway: externalAssets.rooms.hallway,
  library: externalAssets.rooms.library,
  mirror: externalAssets.rooms.mirror,
  garden: externalAssets.rooms.garden,
  cemetery: externalAssets.rooms.cemetery,
  party: externalAssets.rooms.party,
  bed: externalAssets.objects.bed,
  painting: externalAssets.objects.painting,
  books: externalAssets.objects.books,
  mirrorObject: externalAssets.objects.mirror,
  moonFlowers: externalAssets.objects.moonFlowers,
  finalTable: externalAssets.objects.finalTable,
  door: externalAssets.objects.door,
};

function collectAssetPaths(value, paths = []) {
  if (typeof value === "string") paths.push(value);
  else if (Array.isArray(value)) value.forEach((item) => collectAssetPaths(item, paths));
  else if (value && typeof value === "object") Object.values(value).forEach((item) => collectAssetPaths(item, paths));
  return paths;
}

const costumeOrder = ["hat", "cape", "boots", "wand", "accessory"];
const inventoryDefs = {
  invitation: {
    name: "Invitacion",
    icon: externalAssets.ui.iconInvitation,
    description: "Dice: Te esperamos esta noche. La tinta parece moverse sola.",
  },
  key: {
    name: "Llave antigua",
    icon: externalAssets.ui.iconKey,
    description: "Una llave fria con una luna grabada. No pertenece a tu casa.",
  },
  hat: {
    name: "Sombrero",
    icon: externalAssets.ui.iconHat,
    description: "Un sombrero de bruja ligero, como si recordara a su dueña.",
  },
  cape: {
    name: "Capa",
    icon: externalAssets.ui.iconCape,
    description: "La tela brilla cuando una puerta cambia de lugar.",
  },
  boots: {
    name: "Botas",
    icon: externalAssets.ui.iconBoots,
    description: "Botines encantados. Perfectos para correr si algo te sigue.",
  },
  wand: {
    name: "Varita",
    icon: externalAssets.ui.iconWand,
    description: "Una varita tibia. En la punta hay polvo de estrellas.",
  },
  accessory: {
    name: "Accesorio final",
    icon: externalAssets.ui.iconAccessory,
    description: "El broche final del disfraz. Late como un pequeño corazon.",
  },
};

const heroSprites = {
  pajama: externalAssets.characters.idleDown,
  idle: externalAssets.characters.idleDown,
  idleUp: externalAssets.characters.idleUp,
  idleSide: externalAssets.characters.idleSide,
  walkDown1: externalAssets.characters.walkDown1,
  walkDown2: externalAssets.characters.walkDown2,
  walkUp1: externalAssets.characters.walkUp1,
  walkUp2: externalAssets.characters.walkUp2,
  walkSide1: externalAssets.characters.walkSide1,
  walkSide2: externalAssets.characters.walkSide2,
  interact: externalAssets.characters.interact,
  surprise: externalAssets.characters.surprise,
  holdPackage: externalAssets.characters.holdPackage,
  portrait: externalAssets.portraits.neutral,
  portraitSurprise: externalAssets.portraits.surprise,
  pickup: externalAssets.characters.interact,
  celebrate: externalAssets.characters.celebrate,
  progress: Array.from({ length: 6 }, () => externalAssets.characters.idleDown),
};

const imagePaths = [
  PLACEHOLDER_ASSET,
  ...collectAssetPaths(externalAssets),
  ...Object.values(heroSprites).flat(),
  ...Object.values(inventoryDefs).map((item) => item.icon),
  ...Object.values(sceneAssets),
];

const rooms = [
  {
    id: "bedroom",
    name: "Habitacion inicial",
    bg: sceneAssets.bedroom,
    spawn: { x: 548, y: 392 },
    tint: "rgba(45, 22, 64, 0.08)",
    walls: [
      { x: 0, y: 0, w: 1024, h: 86 },
      { x: 0, y: 0, w: 34, h: 576 },
      { x: 990, y: 0, w: 34, h: 576 },
      { x: 0, y: 520, w: 1024, h: 56 },
    ],
    objects: [
      {
        id: "bedroomWindow",
        label: "mirar ventana",
        x: 396, y: 78, w: 170, h: 166,
        sprite: externalAssets.objects.window,
        action: () => say("Charlotte", "La lluvia golpea suave. Desde aqui la ciudad parece una postal violeta."),
      },
      {
        id: "posterSet",
        label: "mirar posters",
        x: 72, y: 94, w: 154, h: 118,
        sprite: externalAssets.objects.posterSet,
        action: () => say("Charlotte", "Mis posters favoritos: brujas, estrellas y una banda que Mama dice que suena triste."),
      },
      {
        id: "photoCluster",
        label: "mirar fotografias",
        x: 232, y: 88, w: 132, h: 112,
        sprite: externalAssets.objects.photoCluster,
        action: () => say("Charlotte", "Fotos con mis amigas, mi primer disfraz y una Polaroid donde salgo tapandome la cara."),
      },
      {
        id: "wallShelves",
        label: "examinar estanterias",
        x: 592, y: 72, w: 190, h: 132,
        sprite: externalAssets.objects.shelves,
        action: () => say("Charlotte", "Aqui guardo libretas, stickers, mini calabazas y cosas que no se botar."),
      },
      {
        id: "clothesRack",
        label: "revisar ropa colgada",
        x: 800, y: 96, w: 150, h: 176,
        sprite: externalAssets.objects.clothesRack,
        solid: true,
        collision: { x: 12, y: 120, w: 126, h: 42 },
        action: () => say("Charlotte", "Vestidos, chaquetas suaves y demasiados lazos morados para una sola persona."),
      },
      {
        id: "bookshelf",
        label: "examinar librero",
        x: 70, y: 222, w: 170, h: 194,
        sprite: externalAssets.objects.bookshelf,
        solid: true,
        collision: { x: 16, y: 96, w: 138, h: 82 },
        action: () => say("Charlotte", "Novelas de misterio, manga, diarios viejos y un libro que no recuerdo comprar."),
      },
      {
        id: "bed",
        label: "examinar cama",
        x: 250, y: 274, w: 260, h: 136,
        sprite: externalAssets.objects.bed,
        solid: true,
        collision: { x: 10, y: 72, w: 238, h: 56 },
        action: () => say("Charlotte", "Almohadas por todos lados. La manta todavia tiene forma de siesta interrumpida."),
      },
      {
        id: "roundRug",
        label: "mirar alfombra",
        x: 376, y: 388, w: 250, h: 106,
        sprite: externalAssets.objects.roundRug,
        action: () => say("Charlotte", "La alfombra redonda siempre queda torcida, aunque la acomode todos los dias."),
      },
      {
        id: "desk",
        label: "examinar escritorio",
        x: 590, y: 234, w: 224, h: 150,
        sprite: externalAssets.objects.desk,
        solid: true,
        collision: { x: 8, y: 86, w: 208, h: 54 },
        action: () => say("Charlotte", "Tareas sin terminar, cartas dobladas y una libreta llena de ideas para disfraces."),
      },
      {
        id: "chair",
        label: "mover silla",
        x: 650, y: 360, w: 86, h: 100,
        sprite: externalAssets.objects.chair,
        solid: true,
        collision: { x: 12, y: 48, w: 62, h: 40 },
        action: () => say("Charlotte", "La silla esta ocupada por mi chaqueta. Otra vez."),
      },
      {
        id: "makeup",
        label: "mirar maquillaje",
        x: 744, y: 322, w: 94, h: 62,
        sprite: externalAssets.objects.makeup,
        action: () => say("Charlotte", "Brillos, rubor rosa y un delineador que solo uso cuando quiero verme valiente."),
      },
      {
        id: "mirror",
        label: "mirar espejo",
        x: 836, y: 248, w: 118, h: 172,
        sprite: externalAssets.objects.mirror,
        solid: true,
        collision: { x: 18, y: 118, w: 82, h: 42 },
        action: () => say("Charlotte", "El espejo devuelve mi reflejo con un segundo de retraso. Eso es nuevo."),
      },
      {
        id: "plantDesk",
        label: "regar planta",
        x: 912, y: 390, w: 78, h: 88,
        sprite: externalAssets.objects.plant,
        solid: true,
        collision: { x: 18, y: 52, w: 46, h: 32 },
        action: () => say("Charlotte", "Se llama Luna. Sobrevivio a mis examenes, asi que es fuerte."),
      },
      {
        id: "plushes",
        label: "mirar peluches",
        x: 744, y: 418, w: 118, h: 86,
        sprite: externalAssets.objects.plushes,
        action: () => say("Charlotte", "Mis peluches hacen guardia. El conejo de la izquierda sabe demasiadas cosas."),
      },
      {
        id: "package",
        label: "abrir paquete",
        x: 478, y: 302, w: 126, h: 102,
        sprite: externalAssets.objects.package,
        solid: true,
        collision: { x: 20, y: 58, w: 86, h: 34 },
        action: openPackage,
      },
      {
        id: "floorLamp",
        label: "encender lampara",
        x: 142, y: 386, w: 82, h: 118,
        sprite: externalAssets.objects.lamp,
        solid: true,
        collision: { x: 24, y: 80, w: 34, h: 24 },
        action: () => say("Charlotte", "La luz calida hace que todo parezca menos raro. Casi."),
      },
      {
        id: "toHallway",
        label: "usar puerta",
        x: 904, y: 170, w: 96, h: 172,
        sprite: externalAssets.objects.door,
        action: () => {
          if (!has("key")) {
            say("Charlotte", "La puerta no tiene cerradura... pero pide una llave.");
            return;
          }
          changeRoom("hallway", 112, 390);
          queueDialogue([
            lineOf("Charlotte", "Esta puerta no estaba aqui hace unos minutos..."),
            lineOf("Charlotte", "La casa cambio por dentro."),
          ]);
        },
      },
    ],
  },
  {
    id: "hallway",
    name: "Pasillo extraño",
    bg: sceneAssets.hallway,
    spawn: { x: 120, y: 392 },
    walls: [
      { x: 0, y: 0, w: 1024, h: 124 },
      { x: 0, y: 0, w: 28, h: 576 },
      { x: 996, y: 0, w: 28, h: 576 },
      { x: 0, y: 520, w: 1024, h: 56 },
      { x: 360, y: 250, w: 116, h: 170 },
      { x: 710, y: 250, w: 120, h: 168 },
    ],
    objects: [
      door("toBedroom", "volver a la habitacion", 58, 246, "bedroom", 860, 392),
      door("toLibrary", "entrar a biblioteca", 368, 240, "library", 130, 392),
      door("toMirror", "abrir cuarto de espejos", 715, 240, "mirror", 152, 392),
      {
        id: "gardenDoor",
        label: "abrir puerta del jardin",
        x: 900, y: 236, w: 72, h: 150,
        sprite: sceneAssets.door,
        action: () => {
          if (!has("wand")) {
            say("Charlotte", "La puerta esta cubierta por polvo brillante. Necesito algo magico.");
            return;
          }
          changeRoom("garden", 128, 390);
        },
      },
      {
        id: "painting",
        label: "examinar cuadro",
        x: 518, y: 178, w: 100, h: 106,
        sprite: sceneAssets.painting,
        action: () => {
          flags.paintingChanged = true;
          queueDialogue([
            lineOf("Charlotte", "El retrato esta sonriendo distinto."),
            lineOf("Charlotte", "Creo que alguien me esta observando..."),
          ]);
        },
      },
    ],
  },
  {
    id: "library",
    name: "Biblioteca encantada",
    bg: sceneAssets.library,
    spawn: { x: 130, y: 392 },
    walls: [
      { x: 0, y: 0, w: 1024, h: 120 },
      { x: 0, y: 0, w: 32, h: 576 },
      { x: 992, y: 0, w: 32, h: 576 },
      { x: 0, y: 520, w: 1024, h: 56 },
      { x: 74, y: 150, w: 250, h: 212 },
      { x: 672, y: 150, w: 250, h: 212 },
      { x: 426, y: 330, w: 190, h: 80 },
    ],
    objects: [
      door("libraryExit", "salir al pasillo", 52, 242, "hallway", 420, 392),
      {
        id: "books",
        label: "leer libro abierto",
        x: 420, y: 318, w: 200, h: 92,
        sprite: sceneAssets.books,
        action: () => {
          if (!has("hat")) {
            giveItem("hat");
            queueDialogue([
              lineOf("Charlotte", "El libro dice: Una bruja siempre empieza por su sombrero."),
              lineOf("Charlotte", "¡Encontré el sombrero de bruja!"),
            ]);
          } else {
            say("Charlotte", "Las paginas ahora estan en blanco.");
          }
        },
      },
      {
        id: "doll",
        label: "hablar con muñeco",
        x: 748, y: 366, w: 90, h: 92,
        sprite: externalAssets.objects.doll,
        action: () => {
          if (!has("hat")) {
            say("Muñeco", "La casa solo presta ropa a quien sabe leer sus pistas.");
            return;
          }
          if (!has("cape")) {
            giveItem("cape");
            queueDialogue([
              lineOf("Muñeco", "No corras todavia. Primero aprende a esconderte en la noche."),
              lineOf("Charlotte", "¡Esta capa combina perfecto!"),
            ]);
          } else {
            say("Muñeco", "Las paredes escuchan menos si caminas despacio.");
          }
        },
      },
    ],
  },
  {
    id: "mirror",
    name: "Cuarto de espejos",
    bg: sceneAssets.mirror,
    spawn: { x: 150, y: 392 },
    tint: "rgba(110, 52, 144, 0.18)",
    walls: [
      { x: 0, y: 0, w: 1024, h: 122 },
      { x: 0, y: 0, w: 34, h: 576 },
      { x: 990, y: 0, w: 34, h: 576 },
      { x: 0, y: 520, w: 1024, h: 56 },
      { x: 420, y: 136, w: 184, h: 250 },
    ],
    objects: [
      door("mirrorExit", "volver al pasillo", 64, 244, "hallway", 760, 392),
      {
        id: "mirror",
        label: "examinar espejo",
        x: 424, y: 136, w: 176, h: 248,
        sprite: sceneAssets.mirrorObject,
        action: () => {
          if (!has("cape")) {
            say("Charlotte", "El espejo no refleja mi habitacion. Refleja un jardin bajo la lluvia.");
            return;
          }
          if (!has("wand")) {
            giveItem("wand");
            flags.mirrorFlash = true;
            queueDialogue([
              lineOf("Charlotte", "Mi reflejo me entrego una varita..."),
              lineOf("Charlotte", "¡Ahora tengo magia!"),
            ]);
          } else {
            say("Charlotte", "Mi reflejo saluda un segundo tarde.");
          }
        },
      },
    ],
  },
  {
    id: "garden",
    name: "Jardin nocturno",
    bg: sceneAssets.garden,
    spawn: { x: 128, y: 390 },
    walls: [
      { x: 0, y: 0, w: 1024, h: 114 },
      { x: 0, y: 0, w: 28, h: 576 },
      { x: 996, y: 0, w: 28, h: 576 },
      { x: 0, y: 518, w: 1024, h: 58 },
      { x: 120, y: 350, w: 120, h: 104 },
      { x: 720, y: 340, w: 130, h: 110 },
    ],
    objects: [
      door("gardenExit", "volver al pasillo", 60, 252, "hallway", 920, 392),
      {
        id: "sunflowers",
        label: "activar flores lunares",
        x: 716, y: 330, w: 150, h: 130,
        sprite: sceneAssets.moonFlowers,
        action: () => {
          if (!has("wand")) {
            say("Charlotte", "Las flores siguen mi mirada. Tal vez reaccionen a magia.");
            return;
          }
          if (!has("boots")) {
            giveItem("boots");
            queueDialogue([
              lineOf("Charlotte", "Las flores abrieron un compartimiento secreto."),
              lineOf("Charlotte", "¡Lista para correr por Halloween!"),
            ]);
          } else {
            say("Charlotte", "Las flores susurran: corre solo cuando la sombra despierte.");
          }
        },
      },
      {
        id: "cemeteryGate",
        label: "cruzar reja",
        x: 912, y: 248, w: 72, h: 150,
        sprite: sceneAssets.door,
        action: () => {
          if (!has("boots")) {
            say("Charlotte", "El camino esta hundido. Necesito algo para moverme rapido.");
            return;
          }
          changeRoom("cemetery", 126, 390);
        },
      },
    ],
  },
  {
    id: "cemetery",
    name: "Cementerio",
    bg: sceneAssets.cemetery,
    spawn: { x: 126, y: 390 },
    walls: [
      { x: 0, y: 0, w: 1024, h: 112 },
      { x: 0, y: 0, w: 26, h: 576 },
      { x: 998, y: 0, w: 26, h: 576 },
      { x: 0, y: 518, w: 1024, h: 58 },
      { x: 160, y: 292, w: 120, h: 92 },
      { x: 590, y: 292, w: 130, h: 98 },
    ],
    objects: [
      door("cemeteryBack", "volver al jardin", 54, 248, "garden", 870, 390),
      {
        id: "ghost",
        label: "hablar con fantasma",
        x: 448, y: 338, w: 92, h: 96,
        sprite: externalAssets.objects.ghost,
        action: () => {
          if (!has("accessory")) {
            giveItem("accessory");
            flags.chaseStarted = true;
            startChase();
            queueDialogue([
              lineOf("Fantasma", "Yo solo cuidaba el broche hasta que llegaras."),
              lineOf("Charlotte", "¡Mi disfraz esta casi completo!"),
              lineOf("Fantasma", "Ahora corre. La casa tambien lo sabe."),
            ]);
          } else {
            say("Fantasma", "La salida esta al este. No mires atras si la sombra respira.");
          }
        },
      },
      {
        id: "partyGate",
        label: "abrir salida a la fiesta",
        x: 912, y: 246, w: 76, h: 154,
        sprite: sceneAssets.door,
        action: () => {
          if (costumeCount() < 5) {
            say("Charlotte", "La puerta espera el disfraz completo.");
            return;
          }
          changeRoom("party", 492, 392);
          startEnding();
        },
      },
    ],
  },
  {
    id: "party",
    name: "Salon de Halloween",
    bg: sceneAssets.party,
    spawn: { x: 492, y: 392 },
    walls: [
      { x: 0, y: 0, w: 1024, h: 116 },
      { x: 0, y: 0, w: 28, h: 576 },
      { x: 996, y: 0, w: 28, h: 576 },
      { x: 0, y: 520, w: 1024, h: 56 },
    ],
    objects: [
      {
        id: "finalTable",
        label: "leer tarjeta",
        x: 430, y: 290, w: 180, h: 118,
        sprite: sceneAssets.finalTable,
        action: () => say("Moon Parcel", "Gracias por completar la entrega. La fiesta empieza cuando encuentras tu propia luz."),
      },
    ],
  },
];

const state = {
  room: "bedroom",
  player: { x: 548, y: 392, w: 44, h: 62, facing: "down", walk: 0 },
  lives: 3,
  elapsed: 0,
  started: false,
  paused: false,
  inventoryOpen: false,
  selectedInventory: 0,
  dialogue: [],
  currentLine: null,
  inventory: new Set(),
  flags: {},
  chase: null,
  ending: false,
  eventFlash: 0,
  saveFlash: 0,
};

const flags = state.flags;
let lastTime = performance.now();
let menuTime = 0;
let particles = [];
const rain = Array.from({ length: 58 }, (_, i) => ({ x: (i * 87) % W, y: (i * 43) % H, s: 160 + (i % 4) * 28 }));
const motes = Array.from({ length: 70 }, (_, i) => ({ x: (i * 137) % W, y: 60 + ((i * 71) % 430), phase: i * 0.73 }));

function lineOf(speaker, text) {
  return { speaker, text };
}

function room() {
  return rooms.find((r) => r.id === state.room);
}

function has(item) {
  return state.inventory.has(item);
}

function costumeCount() {
  return costumeOrder.filter((item) => has(item)).length;
}

function giveItem(item) {
  state.inventory.add(item);
  burst(state.player.x + 24, state.player.y - 28, "#ffd36b", 16);
  updateHud();
  saveGame();
}

function queueDialogue(lines) {
  state.dialogue.push(...lines);
  if (!state.currentLine) nextDialogue();
}

function say(speaker, text) {
  queueDialogue([lineOf(speaker, text)]);
}

function nextDialogue() {
  state.currentLine = state.dialogue.shift() || null;
}

function openPackage() {
  if (flags.packageOpen) {
    say("Charlotte", "La caja sigue tibia. Dentro solo queda polvo dorado.");
    return;
  }
  flags.packageOpen = true;
  giveItem("invitation");
  giveItem("key");
  saveGame();
  queueDialogue([
    lineOf("Charlotte", "Mi paquete Moon Parcel llego... ¿por que la caja esta brillando?"),
    lineOf("Charlotte", "Hay una invitacion: Te esperamos esta noche."),
    lineOf("Charlotte", "Y una llave antigua. No recuerdo haber pedido esto."),
  ]);
}

function door(id, label, x, y, target, spawnX, spawnY) {
  return {
    id,
    label,
    x, y, w: 82, h: 150,
    sprite: sceneAssets.door,
    action: () => changeRoom(target, spawnX, spawnY),
  };
}

function changeRoom(id, x, y) {
  state.room = id;
  state.player.x = x;
  state.player.y = y;
  state.player.walk = 0;
  state.inventoryOpen = false;
  updateHud();
  saveGame();
}

function saveGame({ flash = true } = {}) {
  if (!state.started) return;
  const payload = {
    room: state.room,
    player: {
      x: state.player.x,
      y: state.player.y,
      facing: state.player.facing,
    },
    lives: state.lives,
    elapsed: state.elapsed,
    inventory: [...state.inventory],
    flags: { ...state.flags },
    chase: state.chase ? { ...state.chase } : null,
    ending: state.ending,
    savedAt: Date.now(),
  };
  try {
    localStorage.setItem(SAVE_KEY, JSON.stringify(payload));
    if (flash) state.saveFlash = 1.8;
    refreshContinueButton();
  } catch {
    state.saveFlash = 0;
  }
}

function readSave() {
  try {
    const raw = localStorage.getItem(SAVE_KEY);
    if (!raw) return null;
    const save = JSON.parse(raw);
    if (!rooms.some((r) => r.id === save.room)) return null;
    return save;
  } catch {
    return null;
  }
}

function loadGame() {
  const save = readSave();
  if (!save) {
    setMenuCopy("Guardado", "Halloween Delivery", "Aun no hay partida guardada. La casa espera que abras el paquete por primera vez.");
    refreshContinueButton();
    return;
  }

  state.started = true;
  document.body.classList.remove("menu-mode");
  overlay.hidden = true;
  state.paused = false;
  state.inventoryOpen = false;
  state.dialogue = [];
  state.currentLine = null;
  state.room = save.room;
  state.player.x = Number(save.player?.x) || room().spawn.x;
  state.player.y = Number(save.player?.y) || room().spawn.y;
  state.player.facing = save.player?.facing || "down";
  state.player.walk = 0;
  state.lives = Math.max(1, Math.min(3, Number(save.lives) || 3));
  state.elapsed = Math.max(0, Number(save.elapsed) || 0);
  state.inventory = new Set((save.inventory || []).filter((item) => inventoryDefs[item]));
  Object.keys(flags).forEach((key) => delete flags[key]);
  Object.assign(flags, save.flags || {});
  state.chase = save.chase || (flags.chaseStarted && state.room === "cemetery" ? { x: 220, y: 180, speed: 92, active: true } : null);
  state.ending = Boolean(save.ending);
  state.saveFlash = 1.8;
  updateHud();
}

function clearSave() {
  try {
    localStorage.removeItem(SAVE_KEY);
  } catch {
    // Ignored: some embedded browsers can block storage.
  }
  refreshContinueButton();
}

function refreshContinueButton() {
  continueBtn.disabled = !readSave();
}

function setMenuCopy(badge, title, text) {
  overlay.querySelector(".moon-badge").textContent = badge;
  overlay.querySelector("h1").textContent = title;
  overlay.querySelector("p").textContent = text;
}

function startChase() {
  state.chase = { x: 220, y: 180, speed: 92, active: true };
  saveGame();
}

function startEnding() {
  state.ending = true;
  state.chase = null;
  saveGame();
  queueDialogue([
    lineOf("Charlotte", "El disfraz esta completo..."),
    lineOf("Moon Parcel", "La casa nunca quiso atraparte. Queria asegurarse de que llegaras lista."),
    lineOf("Charlotte", "Entonces... ¿esta era mi invitacion a la fiesta?"),
    lineOf("Moon Parcel", "Feliz Halloween, Charlotte."),
  ]);
}

function loadImages() {
  return Promise.all([...new Set(imagePaths)].map((path) => new Promise((resolve) => {
    const img = new Image();
    img.onload = () => resolve();
    img.onerror = () => {
      missingAssets.add(path);
      resolve();
    };
    img.src = encodeURI(path);
    images.set(path, img);
  })));
}

function resizeCanvas() {
  const dpr = Math.max(1, Math.min(2, window.devicePixelRatio || 1));
  canvas.width = W * dpr;
  canvas.height = H * dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.imageSmoothingEnabled = false;
}

function update(dt) {
  if (!state.started) {
    menuTime += dt;
    updateAtmosphere(dt);
    updateParticles(dt);
    return;
  }
  if (!state.started || state.paused || state.currentLine || state.inventoryOpen || state.ending) {
    updateAtmosphere(dt);
    updateParticles(dt);
    return;
  }
  state.elapsed += dt;
  const p = state.player;
  const speed = state.chase ? 216 : 172;
  const dx = (keys.has("ArrowRight") || keys.has("KeyD") ? 1 : 0) - (keys.has("ArrowLeft") || keys.has("KeyA") ? 1 : 0);
  const dy = (keys.has("ArrowDown") || keys.has("KeyS") ? 1 : 0) - (keys.has("ArrowUp") || keys.has("KeyW") ? 1 : 0);
  if (dx || dy) {
    const len = Math.hypot(dx, dy);
    movePlayer((dx / len) * speed * dt, 0);
    movePlayer(0, (dy / len) * speed * dt);
    p.facing = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "right" : "left") : (dy > 0 ? "down" : "up");
    p.walk += dt;
  }

  if (state.chase?.active) updateChase(dt);
  updateAtmosphere(dt);
  updateParticles(dt);
  updateHud();
}

function movePlayer(dx, dy) {
  const p = state.player;
  p.x += dx;
  p.y += dy;
  const bounds = playerHitbox();
  const blockers = [
    ...room().walls,
    ...room().objects.filter((obj) => obj.solid && !obj.hidden?.()).map(objectCollisionBox),
  ];
  for (const wall of blockers) {
    if (overlap(bounds, wall)) {
      p.x -= dx;
      p.y -= dy;
      return;
    }
  }
}

function playerHitbox() {
  const p = state.player;
  return { x: p.x + 11, y: p.y + 34, w: p.w - 22, h: p.h - 8 };
}

function objectBox(obj) {
  return { x: obj.x, y: obj.y, w: obj.w, h: obj.h };
}

function objectCollisionBox(obj) {
  if (!obj.collision) return objectBox(obj);
  return {
    x: obj.x + obj.collision.x,
    y: obj.y + obj.collision.y,
    w: obj.collision.w,
    h: obj.collision.h,
  };
}

function overlap(a, b) {
  return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

function nearestObject() {
  const p = state.player;
  const center = { x: p.x + p.w / 2, y: p.y + p.h / 2 };
  let best = null;
  for (const obj of room().objects) {
    if (obj.hidden?.()) continue;
    const ox = obj.x + obj.w / 2;
    const oy = obj.y + obj.h / 2;
    const dist = Math.hypot(center.x - ox, center.y - oy);
    if (dist < 112 && (!best || dist < best.dist)) best = { obj, dist };
  }
  return best?.obj || null;
}

function updateChase(dt) {
  if (state.room !== "cemetery") return;
  const c = state.chase;
  const p = state.player;
  const targetX = p.x + p.w / 2;
  const targetY = p.y + p.h / 2;
  const dx = targetX - c.x;
  const dy = targetY - c.y;
  const len = Math.hypot(dx, dy) || 1;
  c.x += (dx / len) * c.speed * dt;
  c.y += (dy / len) * c.speed * dt;
  if (Math.hypot(targetX - c.x, targetY - c.y) < 34) {
    state.lives -= 1;
    burst(p.x + 22, p.y + 18, "#ff5f8d", 18);
    if (state.lives <= 0) {
      state.lives = 3;
      state.inventory.delete("accessory");
      flags.chaseStarted = false;
      state.chase = null;
      changeRoom("cemetery", 126, 390);
      say("Charlotte", "Desperte junto a la reja... el broche volvio a esconderse.");
    } else {
      changeRoom("cemetery", 126, 390);
      c.x = 220;
      c.y = 180;
      say("Charlotte", "La sombra me alcanzo. Tengo que llegar a la salida.");
    }
  }
}

function updateAtmosphere(dt) {
  for (const drop of rain) drop.y = (drop.y + drop.s * dt) % (H + 30);
  state.eventFlash = Math.max(0, state.eventFlash - dt);
  state.saveFlash = Math.max(0, state.saveFlash - dt);
}

function updateParticles(dt) {
  particles = particles
    .map((p) => ({ ...p, life: p.life - dt, x: p.x + p.vx * dt, y: p.y + p.vy * dt }))
    .filter((p) => p.life > 0);
}

function burst(x, y, color, count) {
  for (let i = 0; i < count; i++) {
    const a = (Math.PI * 2 * i) / count;
    particles.push({ x, y, vx: Math.cos(a) * (50 + (i % 3) * 28), vy: Math.sin(a) * (50 + (i % 4) * 20), color, life: 0.45 + (i % 3) * 0.12 });
  }
}

function interact() {
  if (state.currentLine) {
    nextDialogue();
    return;
  }
  if (state.inventoryOpen) {
    examineSelectedItem();
    return;
  }
  const obj = nearestObject();
  if (obj) obj.action();
  else say("Charlotte", "No hay nada especial aqui... salvo que la casa respira bajito.");
}

function examineSelectedItem() {
  const items = [...state.inventory];
  if (!items.length) {
    say("Charlotte", "Mi inventario esta vacio.");
    state.inventoryOpen = false;
    return;
  }
  const item = items[state.selectedInventory % items.length];
  state.inventoryOpen = false;
  say(inventoryDefs[item].name, inventoryDefs[item].description);
}

function updateHud() {
  levelNameEl.textContent = room().name;
  itemsEl.textContent = `${costumeCount()}/5`;
  livesEl.innerHTML = Array.from({ length: 3 }, (_, i) => {
    const src = i < state.lives ? externalAssets.ui.heartFull : externalAssets.ui.heartEmpty;
    return `<img class="heart" src="${src}" alt="${i < state.lives ? "vida" : "sin vida"}" onerror="this.src='${PLACEHOLDER_ASSET}'">`;
  }).join("");
  timeEl.textContent = String(Math.floor(state.elapsed));
  objectiveEl.textContent = currentObjective();
  itemIconsEl.innerHTML = Object.entries(inventoryDefs)
    .map(([id, item]) => `<span class="item-icon ${has(id) ? "collected" : ""}" title="${item.name}"><img src="${item.icon}" alt="${item.name}" onerror="this.src='${PLACEHOLDER_ASSET}'"></span>`)
    .join("");
}

function currentObjective() {
  if (!state.started) return "Explora la casa viva, examina objetos con E y descubre por que Moon Parcel te eligio.";
  if (state.ending) return "Llegaste a la fiesta. Habla con Moon Parcel y disfruta tu disfraz completo.";
  if (!flags.packageOpen) return "Abre el paquete brillante en tu habitacion.";
  if (!has("hat")) return "Busca una pista en la biblioteca. El sombrero es la primera pieza.";
  if (!has("cape")) return "Habla con el muneco de la biblioteca para conseguir la capa.";
  if (!has("wand")) return "Ve al cuarto de espejos y examina el reflejo.";
  if (!has("boots")) return "Usa la varita en las flores lunares del jardin.";
  if (!has("accessory")) return "Cruza al cementerio y habla con el fantasma que cuida el broche.";
  if (state.chase?.active) return "Corre a la puerta este del cementerio antes de que la sombra te alcance.";
  return "Abre la salida hacia el salon de Halloween.";
}

function render() {
  ctx.clearRect(0, 0, W, H);
  if (!state.started) {
    drawMainMenuScene();
    drawParticles();
    return;
  }
  drawRoom();
  drawObjects();
  drawChase();
  drawPlayer();
  drawAtmosphere();
  drawParticles();
  drawMiniMap();
  drawSaveNotice();
  drawInteractionPrompt();
  drawInventory();
  drawDialogue();
  drawPause();
  drawEndingSparkles();
}

function drawMainMenuScene() {
  const t = menuTime;
  ctx.save();
  drawImage(sceneAssets.menu, 0, 0, W, H, false, "cover");
  drawMenuCharlotte(t);
  drawMenuWeather(t);
  ctx.restore();
}

function drawMenuMoon(t) {
  ctx.save();
  ctx.fillStyle = "#ffd36b";
  ctx.globalAlpha = 0.9;
  ctx.beginPath();
  ctx.arc(764, 86, 56, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#09071a";
  ctx.beginPath();
  ctx.arc(788, 70, 55, 0, Math.PI * 2);
  ctx.fill();
  ctx.globalAlpha = 0.16;
  ctx.fillStyle = "#fff2c7";
  ctx.beginPath();
  ctx.arc(760, 90, 88 + Math.sin(t) * 4, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function drawMenuForest(t) {
  ctx.save();
  for (let i = 0; i < 12; i++) {
    const x = i * 94 - 34;
    const sway = Math.sin(t * 0.8 + i) * 5;
    ctx.strokeStyle = i % 2 ? "#10091f" : "#160d27";
    ctx.lineWidth = 14 + (i % 3) * 4;
    ctx.beginPath();
    ctx.moveTo(x, H);
    ctx.quadraticCurveTo(x + 34 + sway, 300, x + 12, 140);
    ctx.stroke();
    ctx.lineWidth = 5;
    for (let j = 0; j < 3; j++) {
      ctx.beginPath();
      ctx.moveTo(x + 14 + sway, 220 + j * 42);
      ctx.lineTo(x + (j % 2 ? -42 : 52) + sway, 164 + j * 28);
      ctx.stroke();
    }
  }
  ctx.restore();
}

function drawMenuHouse(t) {
  ctx.save();
  const x = 540;
  const y = 150;
  ctx.fillStyle = "#120815";
  ctx.fillRect(x + 20, y + 158, 314, 220);
  ctx.fillStyle = "#241336";
  ctx.fillRect(x + 44, y + 120, 268, 258);
  ctx.strokeStyle = "#a86cf1";
  ctx.lineWidth = 4;
  ctx.strokeRect(x + 44, y + 120, 268, 258);
  ctx.fillStyle = "#1a102b";
  ctx.fillRect(x + 106, y + 48, 144, 108);
  ctx.strokeRect(x + 106, y + 48, 144, 108);
  ctx.fillStyle = "#120815";
  triangle(x + 24, y + 122, x + 178, y + 20, x + 334, y + 122);
  triangle(x + 82, y + 48, x + 178, y - 12, x + 276, y + 48);
  ctx.strokeStyle = "#f29ad7";
  ctx.lineWidth = 3;
  linePath([[x + 24, y + 122], [x + 178, y + 20], [x + 334, y + 122]]);
  linePath([[x + 82, y + 48], [x + 178, y - 12], [x + 276, y + 48]]);

  drawMenuWindow(x + 74, y + 158, t, 0);
  drawMenuWindow(x + 224, y + 158, t, 1);
  drawMenuWindow(x + 148, y + 82, t, 2);
  drawMenuDoor(x + 146, y + 282);
  ctx.restore();
}

function drawMenuWindow(x, y, t, id) {
  const phase = (t + id * 2.4) % 9;
  const lit = phase < 4.8 || (id === 1 && t > 7 && t < 10);
  ctx.fillStyle = "#120815";
  ctx.fillRect(x, y, 52, 72);
  ctx.strokeStyle = "#f29ad7";
  ctx.lineWidth = 3;
  ctx.strokeRect(x, y, 52, 72);
  ctx.fillStyle = lit ? "#d68a52" : "#202f66";
  ctx.globalAlpha = lit ? 0.92 + Math.sin(t * 5 + id) * 0.07 : 0.55;
  ctx.fillRect(x + 8, y + 10, 36, 52);
  ctx.globalAlpha = 1;
  ctx.strokeStyle = "#ffc0dc";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(x + 26, y + 10);
  ctx.lineTo(x + 26, y + 62);
  ctx.moveTo(x + 8, y + 36);
  ctx.lineTo(x + 44, y + 36);
  ctx.stroke();
}

function drawMenuDoor(x, y) {
  ctx.fillStyle = "#170d27";
  ctx.fillRect(x, y, 74, 96);
  ctx.strokeStyle = "#f29ad7";
  ctx.lineWidth = 4;
  ctx.strokeRect(x, y, 74, 96);
  ctx.fillStyle = "#ffd36b";
  ctx.fillRect(x + 54, y + 48, 6, 6);
}

function drawMenuFenceAndLamps(t) {
  ctx.save();
  ctx.strokeStyle = "#120815";
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.moveTo(0, 400);
  ctx.lineTo(W, 382);
  ctx.stroke();
  for (let x = -10; x < W + 20; x += 48) {
    ctx.fillStyle = "#120815";
    ctx.fillRect(x, 360, 8, 96);
    triangle(x - 5, 360, x + 4, 344, x + 13, 360);
  }
  [130, 430, 884].forEach((x, i) => drawMenuLamp(x, 316 + Math.sin(t + i) * 3, t + i));
  ctx.restore();
}

function drawMenuLamp(x, y, t) {
  ctx.fillStyle = "#120815";
  ctx.fillRect(x - 5, y + 52, 10, 100);
  ctx.fillRect(x - 22, y + 40, 44, 12);
  ctx.strokeStyle = "#ffd36b";
  ctx.lineWidth = 3;
  ctx.strokeRect(x - 16, y, 32, 42);
  ctx.fillStyle = "#d68a52";
  ctx.globalAlpha = 0.65 + Math.sin(t * 6) * 0.15;
  ctx.fillRect(x - 9, y + 8, 18, 26);
  ctx.globalAlpha = 0.18;
  ctx.beginPath();
  ctx.arc(x, y + 22, 48, 0, Math.PI * 2);
  ctx.fill();
  ctx.globalAlpha = 1;
}

function drawMenuForeground(t) {
  ctx.save();
  ctx.fillStyle = "#151020";
  ctx.fillRect(0, 448, W, 128);
  ctx.fillStyle = "rgba(247, 191, 210, 0.16)";
  for (let i = 0; i < 5; i++) {
    ctx.beginPath();
    ctx.ellipse(((t * 18 + i * 260) % 1200) - 80, 472 + i * 12, 170, 22, 0, 0, Math.PI * 2);
    ctx.fill();
  }
  for (let i = 0; i < 22; i++) {
    const x = (i * 57 + Math.sin(t + i) * 4) % W;
    const y = 488 + (i % 4) * 20;
    ctx.fillStyle = i % 3 ? "#3d2063" : "#4b263a";
    ctx.fillRect(x, y, 28, 10);
    if (i % 7 === 0) {
      ctx.fillStyle = "#b06451";
      ctx.fillRect(x + 4, y - 18, 22, 18);
      ctx.fillStyle = "#d68a52";
      ctx.fillRect(x + 10, y - 10, 6, 5);
    }
  }
  ctx.restore();
}

function drawMenuCharlotte(t) {
  const breathe = Math.sin(t * 2) * 3;
  const lookDown = Math.floor(t % 7) === 5;
  const blink = Math.floor((t * 2.6) % 9) === 0;
  drawImage(heroSprites.holdPackage, 390, 344 + breathe, 118, 146);
  drawImage(externalAssets.objects.package, 482, 394 + breathe, 78, 78);
  ctx.fillStyle = "#ffd36b";
  ctx.fillRect(524, 414 + breathe, 5, 5);
  ctx.fillRect(534, 424 + breathe, 4, 4);
  if (lookDown) drawPixelText("?", 460, 346 + breathe, 22, "#ffd36b");
  if (blink) {
    ctx.fillStyle = "#ffd36b";
    ctx.globalAlpha = 0.35;
    ctx.fillRect(412, 400 + breathe, 70, 6);
    ctx.globalAlpha = 1;
  }
}

function drawMenuWeather(t) {
  ctx.save();
  ctx.strokeStyle = "#a86cf1";
  ctx.lineWidth = 2;
  ctx.globalAlpha = 0.28;
  for (const drop of rain) {
    const x = (drop.x + Math.sin(t * 0.6) * 8) % W;
    ctx.beginPath();
    ctx.moveTo(x, drop.y);
    ctx.lineTo(x - 7, drop.y + 18);
    ctx.stroke();
  }
  ctx.globalAlpha = 1;
  for (let i = 0; i < 36; i++) {
    const x = (i * 83 + t * (12 + i % 4)) % W;
    const y = 118 + ((i * 47) % 330) + Math.sin(t + i) * 8;
    ctx.fillStyle = i % 4 ? "#f29ad7" : "#ffd36b";
    ctx.globalAlpha = 0.25 + Math.sin(t * 2 + i) * 0.15;
    ctx.fillRect(x, y, 3, 3);
  }
  ctx.globalAlpha = 1;
  ctx.restore();
}

function drawMenuMysteryEvents(t) {
  if (t > 5.5 && t < 7.5) {
    ctx.fillStyle = "#120815";
    const x = 772 + (t - 5.5) * 32;
    ctx.fillRect(x, 316, 24, 58);
  }
  if (t > 10.5 && t < 13.5) {
    drawPixelText("...", 690, 280 + Math.sin(t * 4) * 2, 22, "#ffd36b");
  }
  if (t > 15 && t < 17.5) {
    ctx.fillStyle = "#ffd36b";
    ctx.globalAlpha = 0.75 + Math.sin(t * 12) * 0.15;
    ctx.fillRect(686, 311, 8, 8);
    ctx.fillRect(709, 311, 8, 8);
    ctx.globalAlpha = 1;
  }
}

function triangle(x1, y1, x2, y2, x3, y3) {
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.lineTo(x3, y3);
  ctx.closePath();
  ctx.fill();
}

function linePath(points) {
  ctx.beginPath();
  ctx.moveTo(points[0][0], points[0][1]);
  for (const [x, y] of points.slice(1)) ctx.lineTo(x, y);
  ctx.stroke();
}

function drawRoom() {
  const r = room();
  drawImage(r.bg, 0, 0, W, H, false, "cover");
  ctx.fillStyle = r.tint || "rgba(20, 8, 28, 0.12)";
  ctx.fillRect(0, 0, W, H);
  drawRoomDecor(r.id);
}

function drawRoomDecor(id) {
  if (flags.paintingChanged && id === "hallway") {
    drawPixelText("?", 560, 208, 36, "#ffd36b");
  }
}

function drawObjects() {
  const objects = [...room().objects].sort((a, b) => (a.y + a.h) - (b.y + b.h));
  for (const obj of objects) {
    if (obj.hidden?.()) continue;
    if (obj.sprite) {
      drawImage(obj.sprite, obj.x, obj.y, obj.w, obj.h);
    } else {
      drawPropBox(obj);
    }
    if (nearestObject() === obj && !state.currentLine && !state.inventoryOpen) {
      ctx.strokeStyle = "#ffd36b";
      ctx.lineWidth = 3;
      ctx.strokeRect(obj.x - 4, obj.y - 4, obj.w + 8, obj.h + 8);
    }
  }
}

function drawPropBox(obj) {
  drawPendingAsset(`objects/${obj.id}.png`, obj.x, obj.y, obj.w, obj.h);
}

function drawPlayer() {
  const p = state.player;
  const walking = keys.has("ArrowRight") || keys.has("KeyD") || keys.has("ArrowLeft") || keys.has("KeyA") || keys.has("ArrowDown") || keys.has("KeyS") || keys.has("ArrowUp") || keys.has("KeyW");
  const frame = Math.floor(p.walk * 8) % 2;
  let sprite = heroSprites.idle;
  if (p.facing === "up") sprite = walking ? (frame ? heroSprites.walkUp1 : heroSprites.walkUp2) : heroSprites.idleUp;
  else if (p.facing === "left" || p.facing === "right") sprite = walking ? (frame ? heroSprites.walkSide1 : heroSprites.walkSide2) : heroSprites.idleSide;
  else sprite = walking ? (frame ? heroSprites.walkDown1 : heroSprites.walkDown2) : heroSprites.idle;
  const flip = p.facing === "left";
  drawImage(sprite, p.x - 32, p.y - 58, 108, 132, flip);
}

function drawChase() {
  if (!state.chase?.active || state.room !== "cemetery") return;
  const c = state.chase;
  drawImage(externalAssets.objects.shadow, c.x - 48, c.y - 58, 96, 96);
  drawPixelText("!", c.x - 7, c.y - 68, 24, "#ffd36b");
}

function drawAtmosphere() {
  const t = performance.now() / 1000;
  ctx.save();
  ctx.globalAlpha = 0.2;
  ctx.strokeStyle = "#a86cf1";
  ctx.lineWidth = 2;
  for (const drop of rain) {
    ctx.beginPath();
    ctx.moveTo(drop.x, drop.y);
    ctx.lineTo(drop.x - 8, drop.y + 16);
    ctx.stroke();
  }
  ctx.globalAlpha = 1;
  for (let i = 0; i < motes.length; i++) {
    const m = motes[i];
    const x = (m.x + t * (8 + (i % 5))) % W;
    const y = m.y + Math.sin(t * 1.4 + m.phase) * 8;
    ctx.fillStyle = i % 3 ? "#f29ad7" : "#ffd36b";
    ctx.globalAlpha = 0.38 + Math.sin(t * 2 + m.phase) * 0.16;
    ctx.fillRect(x, y, 3, 3);
  }
  ctx.globalAlpha = 1;
  for (let i = 0; i < 3; i++) {
    ctx.fillStyle = "rgba(255, 192, 220, 0.13)";
    ctx.beginPath();
    ctx.ellipse(((t * 18 + i * 330) % 1240) - 80, 430 + i * 18, 180, 28, 0, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();
}

function drawParticles() {
  for (const p of particles) {
    ctx.globalAlpha = Math.max(0, p.life * 1.8);
    ctx.fillStyle = p.color;
    ctx.fillRect(p.x, p.y, 5, 5);
  }
  ctx.globalAlpha = 1;
}

function drawMiniMap() {
  drawPanel(850, 18, 154, 108);
  const map = {
    bedroom: [876, 74],
    hallway: [914, 74],
    library: [914, 40],
    mirror: [952, 74],
    garden: [952, 108],
    cemetery: [990, 108],
    party: [990, 74],
  };
  Object.entries(map).forEach(([id, [x, y]]) => {
    ctx.fillStyle = id === state.room ? "#ffd36b" : "#3d2063";
    ctx.fillRect(x, y, 24, 18);
    ctx.strokeStyle = "#f29ad7";
    ctx.strokeRect(x, y, 24, 18);
  });
  ctx.fillStyle = "#ffc0dc";
  ctx.fillText("MAPA", 894, 48);
}

function drawSaveNotice() {
  if (state.saveFlash <= 0 || state.currentLine || state.inventoryOpen) return;
  ctx.save();
  ctx.globalAlpha = Math.min(1, state.saveFlash);
  drawPanel(38, 20, 190, 46);
  drawPixelText("Guardado", 66, 52, 18, "#ffd36b");
  ctx.restore();
}

function drawInteractionPrompt() {
  if (state.currentLine || state.inventoryOpen || state.ending) return;
  const obj = nearestObject();
  if (!obj) return;
  drawPanel(312, 18, 400, 50);
  drawPixelText(`E  ${obj.label}`, 334, 52, 19, "#fff2c7");
}

function drawInventory() {
  if (!state.inventoryOpen) return;
  const items = [...state.inventory];
  drawImage(externalAssets.ui.inventoryPanel, 172, 90, 680, 370, false, "stretch");
  drawPixelText("Inventario", 208, 132, 28, "#ffd36b");
  drawPixelText("Tab cambia objeto - E examina - I cierra", 208, 426, 18, "#f7bfd2");
  if (!items.length) {
    drawPixelText("Aun no tienes objetos.", 208, 210, 24, "#fff2c7");
    return;
  }
  items.forEach((id, i) => {
    const x = 220 + (i % 4) * 140;
    const y = 166 + Math.floor(i / 4) * 118;
    drawImage(externalAssets.ui.inventorySlot, x, y, 88, 88);
    if (i === state.selectedInventory % items.length) drawImage(externalAssets.ui.selector, x - 7, y - 7, 102, 102);
    drawImage(inventoryDefs[id].icon, x + 14, y + 14, 60, 60);
    drawPixelText(inventoryDefs[id].name, x - 10, y + 112, 15, "#fff2c7");
  });
}

function drawDialogue() {
  if (!state.currentLine) return;
  drawImage(externalAssets.ui.dialogBox, 48, 386, 928, 164);
  drawPanel(70, 404, 142, 126);
  const portrait = state.currentLine.text.includes("?") ? heroSprites.portraitSurprise : heroSprites.portrait;
  drawImage(portrait, 78, 394, 126, 126);
  drawPixelText(`${state.currentLine.speaker}:`, 236, 430, 22, "#ffd36b");
  wrapText(state.currentLine.text, 690, 22).forEach((text, i) => {
    drawPixelText(text, 236, 468 + i * 28, 22, "#fff6ff");
  });
  drawPixelText("E", 936, 526, 18, "#ffd36b");
}

function drawPause() {
  if (!state.paused) return;
  ctx.fillStyle = "rgba(8, 5, 14, 0.72)";
  ctx.fillRect(0, 0, W, H);
  drawPanel(348, 184, 328, 160);
  drawPixelText("PAUSA", 438, 244, 36, "#ffd36b");
  drawPixelText("Esc para continuar", 390, 292, 20, "#fff6ff");
}

function drawEndingSparkles() {
  if (!state.ending) return;
  const t = performance.now() / 1000;
  for (let i = 0; i < 18; i++) {
    star(110 + i * 48, 112 + Math.sin(t * 2 + i) * 44, i % 2 ? "#f29ad7" : "#ffd36b", 5);
  }
  drawImage(heroSprites.celebrate, 430, 254 + Math.sin(t * 6) * 7, 156, 190);
}

function drawImage(path, x, y, w, h, flip = false, fit = "contain") {
  const img = images.get(path);
  if (!img || !img.complete || img.naturalWidth === 0 || missingAssets.has(path)) {
    drawPendingAsset(path, x, y, w, h);
    return false;
  }
  ctx.save();
  ctx.imageSmoothingEnabled = false;
  let dx = x;
  let dy = y;
  let dw = w;
  let dh = h;
  if (fit !== "stretch" && img.naturalWidth && img.naturalHeight) {
    const scale = fit === "cover"
      ? Math.max(w / img.naturalWidth, h / img.naturalHeight)
      : Math.min(w / img.naturalWidth, h / img.naturalHeight);
    dw = Math.max(1, Math.round(img.naturalWidth * scale));
    dh = Math.max(1, Math.round(img.naturalHeight * scale));
    dx = Math.round(x + (w - dw) / 2);
    dy = Math.round(y + (h - dh) / 2);
    if (fit === "cover") {
      ctx.beginPath();
      ctx.rect(x, y, w, h);
      ctx.clip();
    }
  }
  if (flip) {
    ctx.translate(dx + dw, dy);
    ctx.scale(-1, 1);
    ctx.drawImage(img, 0, 0, dw, dh);
  } else {
    ctx.drawImage(img, dx, dy, dw, dh);
  }
  ctx.restore();
  return true;
}

function drawPanel(x, y, w, h) {
  drawImage(externalAssets.ui.panel, x, y, w, h, false, "stretch");
}

function drawPendingAsset(path, x, y, w, h) {
  const placeholder = images.get(PLACEHOLDER_ASSET);
  ctx.save();
  ctx.imageSmoothingEnabled = false;
  if (placeholder?.complete && placeholder.naturalWidth > 0 && path !== PLACEHOLDER_ASSET) {
    const scale = Math.min(w / placeholder.naturalWidth, h / placeholder.naturalHeight);
    const dw = Math.max(1, Math.round(placeholder.naturalWidth * scale));
    const dh = Math.max(1, Math.round(placeholder.naturalHeight * scale));
    const dx = Math.round(x + (w - dw) / 2);
    const dy = Math.round(y + (h - dh) / 2);
    ctx.drawImage(placeholder, dx, dy, dw, dh);
  } else {
    ctx.fillStyle = "#14081c";
    ctx.fillRect(x, y, w, h);
    ctx.strokeStyle = "#ffd36b";
    ctx.lineWidth = 2;
    ctx.strokeRect(x + 1, y + 1, Math.max(1, w - 2), Math.max(1, h - 2));
  }
  if (w >= 120 && h >= 72) {
    ctx.font = "900 13px monospace";
    ctx.fillStyle = "#fff1c7";
    ctx.textAlign = "center";
    ctx.fillText("PENDIENTE_ASSET", x + w / 2, y + h / 2 + 36);
  }
  ctx.restore();
}

function drawPixelText(text, x, y, size, color) {
  ctx.save();
  ctx.font = `900 ${size}px "Trebuchet MS", sans-serif`;
  ctx.fillStyle = "#120815";
  ctx.fillText(text, x + 3, y + 3);
  ctx.fillStyle = color;
  ctx.fillText(text, x, y);
  ctx.restore();
}

function wrapText(text, maxWidth, size) {
  ctx.save();
  ctx.font = `900 ${size}px "Trebuchet MS", sans-serif`;
  const words = text.split(" ");
  const lines = [];
  let line = "";
  for (const word of words) {
    const test = line ? `${line} ${word}` : word;
    if (ctx.measureText(test).width > maxWidth && line) {
      lines.push(line);
      line = word;
    } else {
      line = test;
    }
  }
  if (line) lines.push(line);
  ctx.restore();
  return lines;
}

function star(x, y, color, size = 4) {
  ctx.fillStyle = color;
  ctx.fillRect(x - 1, y - size, 3, size * 2);
  ctx.fillRect(x - size, y - 1, size * 2, 3);
  ctx.fillStyle = "#fff2c7";
  ctx.fillRect(x, y, 2, 2);
}

function loop(now) {
  const dt = Math.min(0.033, (now - lastTime) / 1000);
  lastTime = now;
  update(dt);
  render();
  requestAnimationFrame(loop);
}

function startGame() {
  clearSave();
  state.started = true;
  document.body.classList.remove("menu-mode");
  state.paused = false;
  state.ending = false;
  state.room = "bedroom";
  state.player.x = room().spawn.x;
  state.player.y = room().spawn.y;
  state.inventory.clear();
  state.selectedInventory = 0;
  Object.keys(flags).forEach((key) => delete flags[key]);
  state.chase = null;
  state.lives = 3;
  state.elapsed = 0;
  state.saveFlash = 0;
  overlay.hidden = true;
  queueDialogue([
    lineOf("Charlotte", "Es Halloween... y mi paquete Moon Parcel acaba de llegar."),
    lineOf("Charlotte", "La caja esta brillando. Eso no venia en la descripcion."),
  ]);
  updateHud();
  saveGame({ flash: false });
}

window.addEventListener("keydown", (event) => {
  keys.add(event.code);
  if (event.code === "KeyE" || event.code === "Enter") {
    event.preventDefault();
    interact();
  }
  if (event.code === "KeyI") {
    event.preventDefault();
    if (!state.currentLine) state.inventoryOpen = !state.inventoryOpen;
  }
  if (event.code === "Tab") {
    event.preventDefault();
    const size = Math.max(1, state.inventory.size);
    state.selectedInventory = (state.selectedInventory + 1) % size;
  }
  if (event.code === "Escape" && state.started && !state.currentLine) {
    state.paused = !state.paused;
    state.inventoryOpen = false;
  }
});

window.addEventListener("keyup", (event) => keys.delete(event.code));

startBtn.addEventListener("click", startGame);

continueBtn.addEventListener("click", () => {
  loadGame();
});

optionsBtn.addEventListener("click", () => {
  setMenuCopy("Opciones", "Ambiente", "Lluvia, niebla, luces parpadeantes, particulas magicas y guardado automatico activados.");
});

creditsBtn.addEventListener("click", () => {
  setMenuCopy("Creditos", "Halloween Delivery", "Aventura narrativa pixel art creada para explorar una casa viva, resolver pistas y completar el disfraz de Charlotte.");
});

exitBtn.addEventListener("click", () => {
  setMenuCopy("Moon Parcel", "Halloween Delivery", "La casa magica queda esperando otra entrega.");
});

document.querySelector("#restart").addEventListener("click", () => {
  const r = room();
  state.player.x = r.spawn.x;
  state.player.y = r.spawn.y;
  state.currentLine = null;
  state.dialogue = [];
  state.inventoryOpen = false;
});

document.querySelector("#prevLevel").addEventListener("click", () => {
  const i = rooms.findIndex((r) => r.id === state.room);
  const next = rooms[(i + rooms.length - 1) % rooms.length];
  changeRoom(next.id, next.spawn.x, next.spawn.y);
});

document.querySelector("#nextLevel").addEventListener("click", () => {
  const i = rooms.findIndex((r) => r.id === state.room);
  const next = rooms[(i + 1) % rooms.length];
  changeRoom(next.id, next.spawn.x, next.spawn.y);
});

window.addEventListener("resize", resizeCanvas);
resizeCanvas();
loadImages().then(() => {
  updateHud();
  refreshContinueButton();
  requestAnimationFrame(loop);
});
