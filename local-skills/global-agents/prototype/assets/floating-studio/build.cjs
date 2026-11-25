const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const {createRequire} = require('node:module');
const {createHash} = require('node:crypto');

// Uses an existing toolchain; never installs or downloads dependencies.
async function build() {
  const project = path.resolve(process.argv[2] || process.cwd());
  const local = createRequire(path.join(project,'package.json'));
  const ts = local('typescript');
  const {webpack} = local('next/dist/compiled/webpack/webpack');
  const temp = fs.mkdtempSync(path.join(os.tmpdir(),'prototype-floating-studio-'));
  try {
    const source = fs.readFileSync(path.join(__dirname,'chatbot-send-prototype-studio.tsx'),'utf8');
    const output = ts.transpileModule(source, {compilerOptions:{target:ts.ScriptTarget.ES2020,module:ts.ModuleKind.ESNext,jsx:ts.JsxEmit.ReactJSX}}).outputText;
    fs.writeFileSync(path.join(temp,'component.js'),output.replace(/^import ['"]\.\/chatbot-send-prototype-studio\.css['"];?\s*$/m,''));
    fs.copyFileSync(path.join(__dirname,'adapter.mjs'),path.join(temp,'adapter.mjs'));
    await new Promise((resolve,reject) => {
      const compiler = webpack({mode:'production',entry:path.join(temp,'adapter.mjs'),output:{path:__dirname,filename:'floating-studio.js',library:{name:'PrototypeFloatingStudio',type:'var'}},resolve:{modules:[path.join(project,'node_modules'),'node_modules']},optimization:{minimize:false},devtool:false,performance:{hints:false}});
      compiler.run((error,stats) => compiler.close(() => error || stats.hasErrors() ? reject(error || new Error(stats.toString({all:false,errors:true}))) : resolve()));
    });
    const css = fs.readFileSync(path.join(__dirname,'chatbot-send-prototype-studio.css'),'utf8');
    const bundle = fs.readFileSync(path.join(__dirname,'floating-studio.js'),'utf8');
    const preview = fs.readFileSync(path.join(__dirname,'preview.js'),'utf8');
    const html = `<!doctype html><html lang="pt-BR" data-theme="dark"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Estúdio flutuante aprovado · demonstração local</title><style>
html{--wa-menu:#232728;--wa-text:#e9edef;--wa-muted:#8696a0;--wa-hover:#ffffff14;--wa-selected:#ffffff20;--wa-input:#2a3942;background:#101415;color:var(--wa-text);font:14px Arial,sans-serif}html[data-theme=light]{--wa-menu:#fff;--wa-text:#172320;--wa-muted:#65736e;--wa-hover:#0000000a;--wa-selected:#00000014;--wa-input:#f0f3f1;background:#f7f9f8}body{margin:0}#stage{position:relative;box-sizing:border-box;min-height:100vh;padding:104px 24px 32px}main{max-width:560px;margin:auto}h1{font-size:22px}main input,main button{box-sizing:border-box;font:inherit;padding:12px;border:1px solid var(--wa-muted);border-radius:8px;background:var(--wa-input);color:inherit}main input{width:100%;margin:12px 0}main button{cursor:pointer}#result{overflow-wrap:anywhere}button:focus-visible,select:focus-visible,input:focus-visible,[role=button]:focus-visible{outline:0;background:var(--wa-selected)}
${css}</style><div id="stage"><main><h1>Estúdio de protótipos</h1><p>Exemplo local em memória para conferir os controles aprovados.</p><label for="demo-input">Texto de exemplo</label><input id="demo-input" autocomplete="off"><button id="demo-apply" type="button">Aplicar exemplo</button><p id="result" role="status">Pronto para explorar</p></main></div><div id="studio"></div><script>${bundle.replace(/<\/script/gi,'<\\/script')}</script><script>${preview}</script></html>`;
    fs.writeFileSync(path.join(__dirname,'floating-studio.html'),html);
    const files=['chatbot-send-prototype-studio.tsx','chatbot-send-prototype-studio.css','floating-studio.js','floating-studio.html'];
    fs.writeFileSync(path.join(__dirname,'SHA256SUMS'),files.map(file=>createHash('sha256').update(fs.readFileSync(path.join(__dirname,file))).digest('hex')+'  '+file).join('\n')+'\n');
    console.log('Built offline HTML and reusable bundle from the canonical TSX/CSS.');
  } finally {fs.rmSync(temp,{recursive:true,force:true});}
}
build().catch(error=>{console.error(error);process.exitCode=1;});
