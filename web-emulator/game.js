const canvas = document.querySelector("#game");
const ctx = canvas.getContext("2d");
const overlay = document.querySelector("#overlay");
const startBtn = document.querySelector("#startBtn");
const creditsBtn = document.querySelector("#creditsBtn");
const levelNameEl = document.querySelector("#levelName");
const itemsEl = document.querySelector("#items");
const livesEl = document.querySelector("#lives");
const timeEl = document.querySelector("#time");
const itemIconsEl = document.querySelector("#itemIcons");

const W = 1024;
const H = 576;
const gravity = 1950;
const maxFallSpeed = 1350;
const keys = new Set();
const images = new Map();

const hd = (path) => `./hd/${path}`;
const asset = (path) => `../Assets/Images/MidnightCostumeQuest/${path}`;

const itemCatalog = [
  { name: "Sombrero", asset: hd("Collectibles/witch_hat.png"), message: "¡Encontré mi sombrero de bruja!" },
  { name: "Capa", asset: hd("Collectibles/magic_cape.png"), message: "¡Esta capa combina perfecto!" },
  { name: "Varita", asset: hd("Collectibles/magic_wand.png"), message: "¡Ahora tengo magia!" },
  { name: "Botas", asset: hd("Collectibles/boots.png"), message: "¡Lista para correr por Halloween!" },
  { name: "Accesorio", asset: hd("Collectibles/accessory.png"), message: "¡Mi disfraz está casi completo!" },
];

const platformThemes = ["tomb", "book", "branch", "pumpkin", "cloud"];

const levels = [
  createLevel("Cementerio Fashion", "cementerio_fashion", [
    platform("pumpkin", 0, 512, 1024, 64),
    platform("tomb", 280, 392, 190, 36),
    platform("book", 560, 300, 210, 34),
    platform("branch", 780, 420, 190, 34),
  ], [
    point(325, 350, 0), point(610, 258, 1), point(840, 378, 2), point(90, 460, 3), point(930, 360, 4),
  ], [
    enemy(520, 452, 350, 690), enemy(855, 360, 780, 970),
  ]),
  createLevel("Mercado de Halloween", "mercado_de_halloween", [
    platform("pumpkin", 0, 512, 1024, 64),
    platform("cloud", 175, 408, 160, 34),
    platform("book", 460, 330, 210, 34),
    platform("tomb", 760, 420, 190, 36),
  ], [
    point(210, 366, 0), point(520, 288, 1), point(820, 378, 2), point(620, 470, 3), point(910, 360, 4),
  ], [
    enemy(410, 452, 310, 620), enemy(810, 360, 760, 950),
  ]),
  createLevel("Bosque de la Luna", "bosque_de_la_luna", [
    platform("pumpkin", 0, 512, 1024, 64),
    platform("branch", 180, 405, 200, 32),
    platform("cloud", 470, 300, 190, 34),
    platform("tomb", 740, 390, 185, 36),
    platform("book", 580, 455, 145, 34),
  ], [
    point(225, 362, 0), point(530, 258, 1), point(790, 348, 2), point(620, 412, 3), point(910, 350, 4),
  ], [
    enemy(340, 452, 250, 520), enemy(825, 330, 740, 930),
  ]),
  createLevel("Mansion Encantada", "mansion_encantada", [
    platform("pumpkin", 0, 512, 1024, 64),
    platform("book", 230, 385, 190, 34),
    platform("tomb", 515, 442, 185, 36),
    platform("cloud", 720, 310, 210, 34),
  ], [
    point(270, 342, 0), point(565, 400, 1), point(780, 268, 2), point(890, 268, 3), point(90, 460, 4),
  ], [
    enemy(520, 452, 430, 710), enemy(790, 250, 710, 930),
  ]),
  createLevel("Plaza del Festival", "plaza_del_festival", [
    platform("pumpkin", 0, 512, 1024, 64),
    platform("cloud", 130, 380, 180, 34),
    platform("branch", 390, 310, 210, 32),
    platform("book", 650, 380, 170, 34),
    platform("tomb", 835, 454, 150, 36),
  ], [
    point(180, 338, 0), point(450, 268, 1), point(705, 338, 2), point(910, 410, 3), point(560, 470, 4),
  ], [
    enemy(320, 452, 210, 520), enemy(710, 320, 650, 825), enemy(900, 395, 835, 986),
  ]),
];

const player = {
  x: 72,
  y: 422,
  w: 54,
  h: 82,
  vx: 0,
  vy: 0,
  facing: 1,
  grounded: false,
  invulnerable: 0,
  walkTime: 0,
};

let levelIndex = 0;
let collected = new Set();
let lives = 3;
let elapsed = 0;
let started = false;
let gameMode = "menu";
let paused = false;
let won = false;
let lastTime = performance.now();
let introTime = 0;
let endingTime = 0;
let storyMessage = "";
let storyMessageTimer = 0;
let celebrateTimer = 0;
let particles = [];
let magicDust = Array.from({ length: 70 }, (_, i) => ({
  x: (i * 173) % W,
  y: 70 + ((i * 89) % 400),
  speed: 8 + (i % 7) * 2,
  phase: i * 0.7,
}));

function createLevel(name, bgName, platforms, items, enemies) {
  return { name, bg: hd(`Backgrounds/${bgName}.png`), platforms, items, enemies };
}

function platform(kind, x, y, w, h) {
  return { kind, x, y, w, h };
}

function point(x, y, itemType) {
  return { x, y, itemType };
}

function enemy(x, y, minX, maxX) {
  return { x, y, w: 56, h: 56, minX, maxX, vx: 70, phase: Math.random() * Math.PI * 2 };
}

const imagePaths = [
  hd("Character/idle.png"),
  hd("Character/run_1.png"),
  hd("Character/run_2.png"),
  hd("Character/jump.png"),
  hd("Character/fall.png"),
  asset("Enemies/ghost.png"),
  asset("Enemies/bat.png"),
  ...itemCatalog.map((item) => item.asset),
  ...levels.map((level) => level.bg),
];

function loadImages() {
  return Promise.all([...new Set(imagePaths)].map((path) => new Promise((resolve) => {
    const img = new Image();
    img.onload = resolve;
    img.onerror = resolve;
    img.src = encodeURI(path);
    images.set(path, img);
  })));
}

function resizeCanvas() {
  const dpr = Math.max(1, Math.min(2, window.devicePixelRatio || 1));
  canvas.width = Math.round(W * dpr);
  canvas.height = Math.round(H * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.imageSmoothingEnabled = false;
}

function resetPlayer() {
  player.x = 72;
  player.y = 422;
  player.vx = 0;
  player.vy = 0;
  player.grounded = false;
  player.invulnerable = 1.0;
}

function resetLevel(keepLives = false) {
  const level = levels[levelIndex];
  collected = new Set();
  lives = keepLives ? lives : 3;
  elapsed = 0;
  won = false;
  paused = false;
  level.enemies.forEach((e, i) => {
    e.x = e.minX + (i + 1) * 30;
    e.vx = Math.abs(e.vx);
  });
  resetPlayer();
  updateHud();
}

function updateHud() {
  const level = levels[levelIndex];
  levelNameEl.textContent = `${levelIndex + 1}. ${level.name}`;
  itemsEl.textContent = `${collected.size}/${level.items.length}`;
  livesEl.textContent = "♥".repeat(lives) + "♡".repeat(Math.max(0, 3 - lives));
  timeEl.textContent = String(Math.floor(elapsed));
  itemIconsEl.innerHTML = itemCatalog.map((item, index) => `
    <span class="item-icon ${hasCollectedType(index) ? "collected" : ""}" title="${item.name}">
      <img src="${item.asset}" alt="${item.name}">
    </span>
  `).join("");
}

function hasCollectedType(type) {
  return [...collected].some((itemIndex) => levels[levelIndex].items[itemIndex]?.itemType === type);
}

function rectsOverlap(a, b) {
  return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

function horizontalOverlap(a, b, padding = 0) {
  return a.x + a.w > b.x + padding && a.x < b.x + b.w - padding;
}

function findLandingPlatform(previousBottom, currentBottom) {
  let best = null;
  for (const p of levels[levelIndex].platforms) {
    if (!horizontalOverlap(player, p, 4)) continue;
    if (previousBottom <= p.y + 16 && currentBottom >= p.y) {
      if (!best || p.y < best.y) best = p;
    }
  }
  return best;
}

function step(dt) {
  if (gameMode === "intro") {
    introTime += dt;
    particles = particles
      .map((p) => ({ ...p, life: p.life - dt, x: p.x + p.vx * dt, y: p.y + p.vy * dt }))
      .filter((p) => p.life > 0);
    if (introTime > 7.2 || keys.has("Enter") || keys.has("Space")) beginGameplay();
    return;
  }

  if (gameMode === "ending") {
    endingTime += dt;
    if (Math.floor(endingTime * 10) % 5 === 0) {
      burst(500 + Math.sin(endingTime * 2) * 130, 260 + Math.cos(endingTime * 3) * 55, "#ffd36b", 2);
    }
    particles = particles
      .map((p) => ({ ...p, life: p.life - dt, x: p.x + p.vx * dt, y: p.y + p.vy * dt, vy: p.vy + 90 * dt }))
      .filter((p) => p.life > 0);
    return;
  }

  if (!started || paused || won || gameMode !== "play") return;
  elapsed += dt;
  player.invulnerable = Math.max(0, player.invulnerable - dt);
  storyMessageTimer = Math.max(0, storyMessageTimer - dt);
  celebrateTimer = Math.max(0, celebrateTimer - dt);

  const left = keys.has("ArrowLeft") || keys.has("KeyA");
  const right = keys.has("ArrowRight") || keys.has("KeyD");
  const fastFall = keys.has("ArrowDown") || keys.has("KeyS");
  const speed = 310;
  player.vx = (right ? speed : 0) - (left ? speed : 0);
  if (player.vx !== 0) player.facing = Math.sign(player.vx);

  const previousBottom = player.y + player.h;
  if (fastFall && !player.grounded) player.vy += 900 * dt;
  player.vy = Math.min(maxFallSpeed, player.vy + gravity * dt);
  player.x += player.vx * dt;
  player.y += player.vy * dt;
  player.x = Math.max(0, Math.min(W - player.w, player.x));
  player.grounded = false;

  const platform = player.vy >= 0 ? findLandingPlatform(previousBottom, player.y + player.h) : null;
  if (platform) {
    player.y = platform.y - player.h;
    player.vy = 0;
    player.grounded = true;
  }

  if (player.y > H + 80) damagePlayer();

  const level = levels[levelIndex];
  level.enemies.forEach((enemy) => {
    enemy.phase += dt * 4;
    enemy.x += enemy.vx * dt;
    if (enemy.x < enemy.minX || enemy.x > enemy.maxX) {
      enemy.vx *= -1;
      enemy.x = Math.max(enemy.minX, Math.min(enemy.maxX, enemy.x));
    }
    const hitbox = { x: enemy.x + 8, y: enemy.y + 8, w: enemy.w - 16, h: enemy.h - 14 };
    if (rectsOverlap(player, hitbox) && player.invulnerable <= 0) damagePlayer();
  });

  level.items.forEach((item, index) => {
    if (collected.has(index)) return;
    const itemBox = { x: item.x - 24, y: item.y - 24, w: 48, h: 48 };
    if (rectsOverlap(player, itemBox)) {
      collected.add(index);
      burst(item.x, item.y, "#ffd36b", 18);
      storyMessage = itemCatalog[item.itemType].message;
      storyMessageTimer = 2.8;
      celebrateTimer = 0.65;
      updateHud();
    }
  });

  particles = particles
    .map((p) => ({ ...p, life: p.life - dt, x: p.x + p.vx * dt, y: p.y + p.vy * dt, vy: p.vy + 220 * dt }))
    .filter((p) => p.life > 0);

  if (collected.size === level.items.length) completeLevel();
  player.walkTime += dt;
  updateHud();
}

function damagePlayer() {
  lives -= 1;
  burst(player.x + player.w / 2, player.y + player.h / 2, "#ff7aa8", 14);
  if (lives <= 0) {
    resetLevel(false);
  } else {
    resetPlayer();
    updateHud();
  }
}

function completeLevel() {
  won = true;
  overlay.hidden = false;
  overlay.querySelector("h1").textContent = "Felicidades";
  overlay.querySelector("p").textContent = "¡Felicidades! Has conseguido todos los items para tu disfraz. ¡Feliz Halloween!";
  startBtn.textContent = levelIndex === levels.length - 1 ? "Volver a jugar" : "Siguiente nivel";
  creditsBtn.hidden = true;
}

function burst(x, y, color, count) {
  for (let i = 0; i < count; i++) {
    const angle = (Math.PI * 2 * i) / count;
    particles.push({
      x, y,
      vx: Math.cos(angle) * (70 + (i % 4) * 30),
      vy: Math.sin(angle) * (70 + (i % 3) * 26),
      color,
      life: 0.55 + (i % 4) * 0.08,
    });
  }
}

function drawImage(path, x, y, w, h, flip = false) {
  const img = images.get(path);
  if (!img || !img.complete || img.naturalWidth === 0) return false;
  ctx.save();
  if (flip) {
    ctx.translate(x + w, y);
    ctx.scale(-1, 1);
    ctx.drawImage(img, 0, 0, w, h);
  } else {
    ctx.drawImage(img, x, y, w, h);
  }
  ctx.restore();
  return true;
}

function drawCoverImage(path, x, y, w, h, focusY = 0.5) {
  const img = images.get(path);
  if (!img || !img.complete || img.naturalWidth === 0) return false;
  const sourceRatio = img.naturalWidth / img.naturalHeight;
  const targetRatio = w / h;
  let sx = 0, sy = 0, sw = img.naturalWidth, sh = img.naturalHeight;
  if (sourceRatio > targetRatio) {
    sw = img.naturalHeight * targetRatio;
    sx = (img.naturalWidth - sw) / 2;
  } else {
    sh = img.naturalWidth / targetRatio;
    sy = Math.max(0, Math.min(img.naturalHeight - sh, (img.naturalHeight - sh) * focusY));
  }
  ctx.drawImage(img, sx, sy, sw, sh, x, y, w, h);
  return true;
}

function render() {
  const level = levels[levelIndex];
  ctx.clearRect(0, 0, W, H);
  drawCoverImage(level.bg, 0, 0, W, H, 0.47);
  drawParallaxAndAtmosphere();

  level.platforms.forEach(drawPlatform);
  level.items.forEach((item, index) => {
    if (!collected.has(index)) drawCollectible(item, index);
  });
  level.enemies.forEach(drawEnemy);
  drawGate();
  drawMara();
  drawParticles();
  drawCanvasHud();

  if (paused) {
    ctx.fillStyle = "rgba(8, 5, 14, 0.72)";
    ctx.fillRect(0, 0, W, H);
    drawPixelText("PAUSA", W / 2 - 78, H / 2, 42, "#ffd36b");
  }
}

function drawParallaxAndAtmosphere() {
  const t = performance.now() / 1000;
  ctx.save();
  ctx.globalAlpha = 0.22;
  const fog = ctx.createLinearGradient(0, 360, 0, 545);
  fog.addColorStop(0, "rgba(255, 190, 245, 0)");
  fog.addColorStop(1, "rgba(244, 178, 255, 0.42)");
  ctx.fillStyle = fog;
  for (let i = 0; i < 4; i++) {
    ctx.beginPath();
    ctx.ellipse(((t * 18 + i * 310) % 1320) - 120, 430 + i * 18, 210, 34, 0, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;

  magicDust.forEach((p, i) => {
    const x = (p.x + t * p.speed) % W;
    const y = p.y + Math.sin(t * 1.6 + p.phase) * 8;
    ctx.fillStyle = i % 3 === 0 ? "#ffd36b" : "#f7a6ff";
    ctx.globalAlpha = 0.45 + Math.sin(t * 3 + p.phase) * 0.18;
    ctx.fillRect(x, y, 3, 3);
  });
  ctx.globalAlpha = 1;

  ctx.fillStyle = "rgba(20, 10, 32, 0.9)";
  for (let i = 0; i < 6; i++) {
    const x = ((t * (24 + i * 3) + i * 210) % 1200) - 80;
    const y = 72 + Math.sin(t * 2 + i) * 20 + i * 15;
    drawBat(x, y, 0.7 + (i % 3) * 0.15);
  }
  ctx.globalAlpha = 1;
  ctx.restore();
}

function drawBat(x, y, s) {
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.quadraticCurveTo(x + 12 * s, y - 12 * s, x + 24 * s, y);
  ctx.quadraticCurveTo(x + 34 * s, y - 12 * s, x + 44 * s, y);
  ctx.quadraticCurveTo(x + 30 * s, y + 8 * s, x + 22 * s, y + 2 * s);
  ctx.quadraticCurveTo(x + 14 * s, y + 8 * s, x, y);
  ctx.fill();
}

function drawPlatform(p) {
  ctx.save();
  ctx.shadowColor = "rgba(0, 0, 0, 0.38)";
  ctx.shadowBlur = 12;
  ctx.shadowOffsetY = 8;
  if (p.kind === "tomb") drawTombPlatform(p);
  if (p.kind === "book") drawBookPlatform(p);
  if (p.kind === "branch") drawBranchPlatform(p);
  if (p.kind === "pumpkin") drawGroundPlatform(p);
  if (p.kind === "cloud") drawCloudPlatform(p);
  ctx.restore();
}

function drawTombPlatform(p) {
  ctx.fillStyle = "#4a365f";
  ctx.beginPath();
  ctx.roundRect(p.x, p.y + 8, p.w, p.h, 7);
  ctx.fill();
  ctx.fillStyle = "#75528b";
  for (let x = p.x + 10; x < p.x + p.w - 12; x += 34) {
    ctx.beginPath();
    ctx.roundRect(x, p.y - 12, 24, p.h + 12, 9);
    ctx.fill();
  }
  drawPlatformTop(p);
}

function drawBookPlatform(p) {
  ctx.fillStyle = "#3b214d";
  ctx.beginPath();
  ctx.roundRect(p.x, p.y, p.w, p.h, 6);
  ctx.fill();
  ctx.fillStyle = "#9b5bc3";
  ctx.fillRect(p.x + 8, p.y + 7, p.w - 16, 6);
  ctx.fillStyle = "#ffd36b";
  ctx.fillRect(p.x + 20, p.y + p.h - 8, p.w - 40, 4);
  drawPlatformTop(p);
}

function drawBranchPlatform(p) {
  ctx.strokeStyle = "#281323";
  ctx.lineWidth = p.h;
  ctx.lineCap = "round";
  ctx.beginPath();
  ctx.moveTo(p.x + 12, p.y + p.h / 2);
  ctx.quadraticCurveTo(p.x + p.w * 0.48, p.y - 8, p.x + p.w - 10, p.y + p.h / 2);
  ctx.stroke();
  ctx.strokeStyle = "#7b3b65";
  ctx.lineWidth = 4;
  ctx.stroke();
  ctx.fillStyle = "#d774bd";
  ctx.fillRect(p.x + 15, p.y + 6, p.w - 30, 4);
}

function drawGroundPlatform(p) {
  const fill = ctx.createLinearGradient(0, p.y, 0, p.y + p.h);
  fill.addColorStop(0, "#d96ac5");
  fill.addColorStop(0.18, "#5b316e");
  fill.addColorStop(1, "#25152d");
  ctx.fillStyle = fill;
  ctx.beginPath();
  ctx.roundRect(p.x, p.y, p.w, p.h, 6);
  ctx.fill();
  ctx.fillStyle = "rgba(255, 222, 250, 0.55)";
  ctx.fillRect(p.x, p.y + 4, p.w, 4);
  for (let x = p.x + 20; x < p.w; x += 72) drawTinyPumpkin(x, p.y - 11);
}

function drawCloudPlatform(p) {
  ctx.fillStyle = "#f2d8ff";
  ctx.beginPath();
  ctx.roundRect(p.x + 8, p.y + 10, p.w - 16, p.h - 8, 12);
  ctx.fill();
  ctx.fillStyle = "#9b62bc";
  ctx.fillRect(p.x + 16, p.y + p.h - 8, p.w - 32, 5);
  drawPlatformTop(p);
}

function drawPlatformTop(p) {
  ctx.fillStyle = "#ffb8f4";
  ctx.fillRect(p.x + 8, p.y + 4, p.w - 16, 4);
  ctx.fillStyle = "rgba(24, 10, 30, 0.36)";
  ctx.fillRect(p.x + 10, p.y + p.h - 7, p.w - 20, 4);
}

function drawTinyPumpkin(x, y) {
  ctx.fillStyle = "#f08a32";
  ctx.beginPath();
  ctx.ellipse(x, y, 10, 8, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#30131f";
  ctx.fillRect(x - 4, y - 1, 2, 2);
  ctx.fillRect(x + 3, y - 1, 2, 2);
}

function drawCollectible(item, index) {
  const catalog = itemCatalog[item.itemType];
  const bob = Math.sin(performance.now() / 260 + index) * 7;
  const x = item.x;
  const y = item.y + bob;
  ctx.save();
  ctx.shadowColor = "#ffd36b";
  ctx.shadowBlur = 18;
  ctx.globalAlpha = 0.75;
  ctx.beginPath();
  ctx.arc(x, y, 27, 0, Math.PI * 2);
  ctx.fillStyle = "rgba(255, 215, 113, 0.22)";
  ctx.fill();
  ctx.globalAlpha = 1;
  drawImage(catalog.asset, x - 31, y - 31, 62, 62);
  ctx.restore();
}

function drawEnemy(enemy) {
  const bob = Math.sin(enemy.phase) * 6;
  ctx.save();
  ctx.fillStyle = "rgba(255, 92, 142, 0.18)";
  ctx.beginPath();
  ctx.arc(enemy.x + enemy.w / 2, enemy.y + enemy.h / 2 + bob, 38, 0, Math.PI * 2);
  ctx.fill();
  drawImage(asset("Enemies/ghost.png"), enemy.x - 6, enemy.y + bob - 8, enemy.w + 12, enemy.h + 12, enemy.vx < 0);
  ctx.fillStyle = "#ff5c8e";
  ctx.fillRect(enemy.minX, enemy.y + enemy.h + 8, enemy.maxX - enemy.minX + enemy.w, 3);
  ctx.restore();
}

function drawGate() {
  const ready = collected.size === levels[levelIndex].items.length;
  ctx.save();
  ctx.shadowColor = ready ? "#ffd36b" : "rgba(0, 0, 0, 0.35)";
  ctx.shadowBlur = ready ? 20 : 8;
  ctx.fillStyle = ready ? "#ffd36b" : "#796883";
  ctx.fillRect(966, 434, 42, 78);
  ctx.fillStyle = "#24172b";
  ctx.fillRect(978, 450, 18, 62);
  ctx.restore();
}

function drawMara() {
  let sprite = hd("Character/idle.png");
  if (!player.grounded) sprite = player.vy < 0 ? hd("Character/jump.png") : hd("Character/fall.png");
  else if (Math.abs(player.vx) > 1) sprite = Math.floor(player.walkTime * 8) % 2 ? hd("Character/run_1.png") : hd("Character/run_2.png");

  const img = images.get(sprite);
  const targetH = Math.abs(player.vx) > 1 ? 176 : 160;
  const targetW = img?.naturalHeight ? targetH * (img.naturalWidth / img.naturalHeight) : 118;
  const drawX = player.x + player.w / 2 - targetW / 2;
  const drawY = player.y + player.h - targetH + 12;
  ctx.save();
  ctx.globalAlpha = player.invulnerable > 0 && Math.floor(performance.now() / 90) % 2 === 0 ? 0.55 : 1;
  ctx.shadowColor = "rgba(0, 0, 0, 0.48)";
  ctx.shadowBlur = 14;
  ctx.shadowOffsetY = 6;
  drawImage(sprite, drawX, drawY, targetW, targetH, player.facing < 0);
  ctx.restore();
}

function drawParticles() {
  particles.forEach((p) => {
    ctx.globalAlpha = Math.max(0, p.life * 1.6);
    ctx.fillStyle = p.color;
    ctx.fillRect(p.x, p.y, 5, 5);
  });
  ctx.globalAlpha = 1;
}

function drawCanvasHud() {
  drawPixelText(`Disfraz: ${collected.size}/${levels[levelIndex].items.length}`, 22, 28, 20, "#fff2b8");
}

function drawPixelText(text, x, y, size, color) {
  ctx.save();
  ctx.font = `800 ${size}px "Trebuchet MS", sans-serif`;
  ctx.fillStyle = "#4a1d5d";
  ctx.fillText(text, x + 3, y + 3);
  ctx.fillStyle = color;
  ctx.fillText(text, x, y);
  ctx.restore();
}

function loop(now) {
  const dt = Math.min(0.033, (now - lastTime) / 1000);
  lastTime = now;
  step(dt);
  render();
  requestAnimationFrame(loop);
}

function jump() {
  if (player.grounded && !paused && started) {
    player.vy = -780;
    player.grounded = false;
  }
}

window.addEventListener("keydown", (event) => {
  keys.add(event.code);
  if (["Space", "KeyW", "ArrowUp"].includes(event.code)) {
    event.preventDefault();
    jump();
  }
  if (event.code === "Escape" && started && !won) paused = !paused;
});

window.addEventListener("keyup", (event) => keys.delete(event.code));

startBtn.addEventListener("click", () => {
  if (won && levelIndex < levels.length - 1) levelIndex += 1;
  else if (won && levelIndex === levels.length - 1) levelIndex = 0;
  started = true;
  overlay.hidden = true;
  startBtn.textContent = "Jugar";
  creditsBtn.hidden = false;
  resetLevel(false);
});

creditsBtn.addEventListener("click", () => {
  overlay.querySelector("h1").textContent = "Creditos";
  overlay.querySelector("p").textContent = "Rediseño visual inspirado en Halloween kawaii pixel art. Base jugable: minijuego Unity original.";
});

document.querySelector("#restart").addEventListener("click", () => resetLevel(false));
document.querySelector("#prevLevel").addEventListener("click", () => {
  levelIndex = (levelIndex + levels.length - 1) % levels.length;
  started = true;
  overlay.hidden = true;
  resetLevel(false);
});
document.querySelector("#nextLevel").addEventListener("click", () => {
  levelIndex = (levelIndex + 1) % levels.length;
  started = true;
  overlay.hidden = true;
  resetLevel(false);
});

window.addEventListener("resize", resizeCanvas);
resizeCanvas();
loadImages().then(() => {
  resetLevel(false);
  requestAnimationFrame(loop);
});
