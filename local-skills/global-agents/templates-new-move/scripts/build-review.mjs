// Compile the task's real React consumers, retaining CSS modules and local assets.
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const [checkout, entry, manifestPath, destination] = process.argv.slice(2).map(x => path.resolve(x));
if (!destination) throw new Error('Uso: node build-review.mjs CHECKOUT ENTRY.tsx REVIEW.json DESTINO_NOVO');
const manifest = JSON.parse(await fs.readFile(manifestPath, 'utf8'));
if (!manifest.grooming || !Array.isArray(manifest.surfaces) || !manifest.surfaces.length) throw new Error('Grooming e superfícies obrigatórios.');
const ids = new Set();
for (const surface of manifest.surfaces) {
  if (!surface.id || ids.has(surface.id) || !surface.title || !surface.grooming || (!surface.template && !surface.gap)) throw new Error('Referência ausente ou ID duplicado.');
  ids.add(surface.id);
}
await fs.mkdir(destination); // Never replace another review or its drafts.
const require = createRequire(path.join(checkout, 'package.json'));
const { build } = await import(pathToFileURL(require.resolve('vite')));
const source = path.join(destination, '.source');
await fs.mkdir(source);
await fs.writeFile(path.join(source, 'index.html'), '<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Validação de templates</title><div id="root"></div><script type="module" src="/entry.tsx"></script></html>');
await fs.writeFile(path.join(source, 'entry.tsx'), `import React from 'react';import{createRoot}from'react-dom/client';import Preview from ${JSON.stringify(entry.replaceAll('\\','/'))};createRoot(document.getElementById('root')).render(<Preview/>);`);
// Only Next's image delivery is adapted; the template, layout and interactions are imported unchanged.
await fs.writeFile(path.join(source, 'image.tsx'), `import React from 'react';export default function Image({fill,priority,unoptimized,loader,quality,placeholder,blurDataURL,style,src,...props}){return <img {...props} src={typeof src==='string'?src:src.src} style={{...(fill?{position:'absolute',inset:0,width:'100%',height:'100%'}:{}),...style}}/>}`);
const postcss=require('postcss');
const globalCss=postcss.parse(await fs.readFile(path.join(checkout,'apps/web/src/app/globals.css'),'utf8'));
const iconCss=globalCss.nodes.filter(n=>(n.type==='rule'&&n.selector.startsWith('.document-submission-confirmation-icon'))||(n.type==='atrule'&&n.name==='keyframes'&&/^document-confirmation-(pop|ring|check|halo|sparks)$/.test(n.params))).map(n=>n.toString()).join('\n');
if(!iconCss.includes('__check'))throw Error('CSS canônico do check de sucesso não encontrado.');
await fs.writeFile(path.join(source,'confirmation.css'),iconCss+'\n[data-replay-active]{outline:3px solid #2558d6!important;outline-offset:5px!important} @media(prefers-reduced-motion:reduce){.document-submission-confirmation-icon,.document-submission-confirmation-icon *{animation:none!important}}');
await fs.appendFile(path.join(source,'entry.tsx'),"import './confirmation.css';");
await build({configFile:false,root:source,base:'./',publicDir:false,oxc:{jsx:{runtime:'automatic'}},
  resolve:{alias:{'@':path.join(checkout,'apps/web/src'),'next/image':path.join(source,'image.tsx'),react:path.dirname(require.resolve('react/package.json')),'react-dom':path.dirname(require.resolve('react-dom/package.json'))}},
  build:{outDir:path.join(destination,'preview'),emptyOutDir:false},
});
const scripts = path.dirname(fileURLToPath(import.meta.url));
await fs.copyFile(path.join(scripts,'review-client.html'),path.join(destination,'index.html'));
await fs.copyFile(path.join(scripts,'scenario-player.mjs'),path.join(destination,'scenario-player.js'));
await fs.copyFile(path.join(scripts,'review-queue.mjs'),path.join(destination,'review-queue.js'));
await fs.copyFile(manifestPath,path.join(destination,'review.json'));
await fs.cp(path.join(checkout,'apps/web/public/templates'),path.join(destination,'templates'),{recursive:true});
await fs.mkdir(path.join(destination,'fonts'));
for (const name of ['InterVariable.woff2','Inter-LICENSE.txt']) await fs.copyFile(path.join(checkout,'apps/web/public/fonts',name),path.join(destination,'fonts',name));
console.log(destination);
