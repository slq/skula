// Run with Node.js; requires sharp. Set NODE_PATH to an existing package bundle if needed.
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require('sharp');
const root = path.resolve(__dirname, '..');
async function render(source, destination, width, height) {
  await sharp(path.join(root, source), { density: 288 }).resize(width, height).png().toFile(path.join(root, destination));
}
async function main() {
  for (const name of ['logo', 'logo-light']) await render(`brand/${name}.svg`, `brand/${name}.png`, 1620);
  await render('brand/mark.svg', 'brand/mark.png', 512, 512);
  await render('brand/app-icon.svg', 'brand/app-icon.png', 1024, 1024);
  await render('brand/preview.svg', 'brand/preview.png', 1280, 850);
  for (const size of [192, 512]) {
    await render('brand/app-icon.svg', `public/icon-${size}.png`, size, size);
    await render('brand/app-icon-maskable.svg', `public/icon-maskable-${size}.png`, size, size);
  }
  await render('brand/apple-touch-icon.svg', 'public/apple-touch-icon.png', 180, 180);
  for (const size of [16, 32, 48]) await render('public/favicon.svg', `public/favicon-${size}x${size}.png`, size, size);
  // PNG frames in the ICO container are supported by modern browsers and Windows.
  const frames = [];
  for (const size of [16, 24, 32, 48, 64, 128, 256]) {
    frames.push({ size, png: await sharp(path.join(root, 'public/favicon.svg'), { density: 768 }).resize(size, size).png().toBuffer() });
  }
  const header = Buffer.alloc(6 + 16 * frames.length);
  header.writeUInt16LE(1, 2);
  header.writeUInt16LE(frames.length, 4);
  let offset = header.length;
  frames.forEach(({ size, png }, index) => {
    const pos = 6 + 16 * index;
    header[pos] = size === 256 ? 0 : size;
    header[pos + 1] = size === 256 ? 0 : size;
    header.writeUInt16LE(1, pos + 4);
    header.writeUInt16LE(32, pos + 6);
    header.writeUInt32LE(png.length, pos + 8);
    header.writeUInt32LE(offset, pos + 12);
    offset += png.length;
  });
  await fs.writeFile(path.join(root, 'public/favicon.ico'), Buffer.concat([header, ...frames.map(frame => frame.png)]));
  const appFrames = [];
  for (const { size } of frames) {
    const source = size <= 48 ? 'public/favicon.svg' : 'brand/app-icon.svg';
    appFrames.push(await sharp(path.join(root, source), { density: 768 }).resize(size, size).png().toBuffer());
  }
  const appHeader = Buffer.from(header);
  let appOffset = appHeader.length;
  appFrames.forEach((png, index) => {
    appHeader.writeUInt32LE(png.length, 6 + 16 * index + 8);
    appHeader.writeUInt32LE(appOffset, 6 + 16 * index + 12);
    appOffset += png.length;
  });
  await fs.writeFile(path.join(root, 'brand/app-icon.ico'), Buffer.concat([appHeader, ...appFrames]));
  console.log('Wyeksportowano PNG oraz ICO.');
}
main().catch(error => { console.error(error); process.exitCode = 1; });