import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

for(const scenario of ['disabled connection','disabled connection with comment','disabled tool','multiline disabled tool','existing output'])test(`helper rejects ${scenario} before launching MCP`,async()=>{
 const root=await fs.mkdtemp(path.join(os.tmpdir(),'ponte-helper-'));
 const sentinel=path.join(root,'sentinel.mjs'),started=path.join(root,'started');
 await fs.writeFile(sentinel,`import fs from 'node:fs';fs.writeFileSync(${JSON.stringify(started)},'unexpected');`);
 const entry='C:/Users/caila/AppData/Roaming/npm/node_modules/@agentify/desktop/mcp-server.mjs';
 const extra=scenario==='disabled connection'?'enabled = false':scenario==='disabled connection with comment'?'enabled = false # disabled':scenario==='disabled tool'?"disabled_tools = ['agentify_query']":scenario==='multiline disabled tool'?"disabled_tools = [\n  'agentify_query', # keep disabled\n]":'';
 await fs.writeFile(path.join(root,'config.toml'),`[mcp_servers.agentify-desktop]\ncommand = '${process.execPath}'\nargs = ['${sentinel}', '${entry}']\nenabled_tools = ['agentify_query']\n${extra}\n`);
 const input=path.join(root,'request.json'),output=path.join(root,'response.json');
 await fs.writeFile(input,JSON.stringify({name:'agentify_query',arguments:{prompt:'not sent'}}));
 if(scenario==='existing output')await fs.writeFile(output,'PRESERVED');
 const result=spawnSync(process.execPath,[fileURLToPath(new URL('./query-mcp.mjs',import.meta.url)),input,output],{env:{...process.env,CODEX_HOME:root},encoding:'utf8',timeout:5000});
 assert.notEqual(result.status,0);assert.match(result.stderr,scenario==='existing output'?/EEXIST/:/disabled/i);
 await assert.rejects(fs.stat(started),{code:'ENOENT'});
 if(scenario==='existing output')assert.equal(await fs.readFile(output,'utf8'),'PRESERVED');
});
