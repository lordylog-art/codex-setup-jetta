import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';

// A fresh MCP connection exposes updated optional fields to clients with a cached schema.
const [input,output]=process.argv.slice(2);
assert.ok(input&&output,'Usage: query-mcp.mjs request.json new-response.json');
const config=await fs.readFile(path.join(process.env.CODEX_HOME||path.join(os.homedir(),'.codex'),'config.toml'),'utf8');
const section=name=>config.match(new RegExp('\\[mcp_servers\\.agentify-desktop'+name+'\\]\\s*([\\s\\S]*?)(?=\\n\\[|$)'))?.[1]||'';
const quoted=text=>[...text.matchAll(/'([^']*)'|"((?:\\.|[^"\\])*)"/g)].map(m=>m[1]??JSON.parse(m[0]));
const uncomment=text=>text.split(/\r?\n/).map(line=>line.match(/^(?:'[^']*'|"(?:\\.|[^"\\])*"|[^'"#])*/)?.[0]||'').join('\n');
const server=uncomment(section('')),environment=uncomment(section('\\.env'));
const value=key=>server.match(new RegExp('^'+key+'\\s*=\\s*(\\[[\\s\\S]*?\\]|[^\\r\\n]*)','m'))?.[1]||'';
const command=quoted(value('command'))[0],args=quoted(value('args')),enabled=quoted(value('enabled_tools'));
assert.notEqual(value('enabled').trim(),'false','Configured Agentify connection is disabled');
const entry=args.find(arg=>arg.endsWith('mcp-server.mjs'));
assert.ok(command&&entry,'Configured Agentify MCP entry not found');
const request=JSON.parse(await fs.readFile(input,'utf8'));
assert.ok(enabled.includes(request.name),'Tool is not enabled in the configured Agentify connection');
assert.ok(!quoted(value('disabled_tools')).includes(request.name),'Tool is disabled in the configured Agentify connection');
const env={...process.env};
for(const line of environment.split(/\r?\n/)){
 const match=line.match(/^([A-Z_][A-Z_0-9]*)\s*=\s*(.+)$/);
 if(match){const values=quoted(match[2]);assert.equal(values.length,1,'Unsupported Agentify environment value');env[match[1]]=values[0]}
}
const require=createRequire(entry);
const {Client}=await import(pathToFileURL(require.resolve('@modelcontextprotocol/sdk/client/index.js')));
const {StdioClientTransport}=await import(pathToFileURL(require.resolve('@modelcontextprotocol/sdk/client/stdio.js')));
const client=new Client({name:'ponte-chatgpt',version:'1.0.0'},{capabilities:{}});
await fs.mkdir(path.dirname(path.resolve(output)),{recursive:true});
const outputFile=await fs.open(output,'wx');
let invoked=false,recorded=false;
try{
 await client.connect(new StdioClientTransport({command,args,env,stderr:'pipe'}));
 const tools=await client.listTools();
 if(request.arguments?.chatMode)assert.ok(tools.tools.find(t=>t.name===request.name)?.inputSchema.properties.chatMode,'MCP does not support chatMode');
 invoked=true;
 const result=await client.callTool(request,undefined,{timeout:Math.max(120000,(Number(request.arguments?.timeoutMs)||660000)+60000)});
 await outputFile.writeFile(JSON.stringify(result,null,2));recorded=true;
 console.log(JSON.stringify({isError:!!result.isError,tabId:result.structuredContent?.tabId,text:result.content?.filter(c=>c.type==='text').map(c=>c.text).join('\n').slice(0,1500),output}));
 if(result.isError)process.exitCode=1;
}catch(error){
 if(!recorded)await outputFile.writeFile(JSON.stringify({isError:true,error:error.message,requestMayHaveBeenSent:invoked}));
 throw error;
}finally{await outputFile.close();await client.close()}
