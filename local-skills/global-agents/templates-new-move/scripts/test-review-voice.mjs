// Isolated browser capture and provider responses; no microphone or external requests.
import { createRequire } from 'node:module';
import assert from 'node:assert/strict';
const {chromium}=createRequire('D:/newmove/package.json')('playwright');
const browser=await chromium.launch();
const page=await browser.newPage({viewport:{width:1600,height:1200}});
try {
  await page.clock.install();
  await page.addInitScript(()=>{
    window.recordings=[];
    navigator.mediaDevices.getUserMedia=async()=>({getTracks:()=>[{stop(){}}]});
    window.MediaRecorder=class {
      state='inactive';mimeType='audio/webm';
      constructor(){window.recordings.push(this)}
      start(){this.state='recording';this.ondataavailable?.({data:new Blob(['inicio'])})}
      stop(){this.state='inactive';this.ondataavailable?.({data:new Blob(['fim'])});this.onstop?.()}
    };
  });
  await page.route('**/voice/health',route=>route.fulfill({json:{ready:true,maxSeconds:600}}));
  let calls=0;
  await page.route('**/voice/transcribe',async route=>{
    calls++;assert.equal(route.request().postDataBuffer().toString(),'iniciofim');
    await route.fulfill({json:calls===1?{text:'Texto revisado completo.'}:{text:'Texto original preservado.',warning:'Revisão indisponível; confira o texto.'}});
  });
  await page.goto(process.argv[2]||'http://127.0.0.1:43187/');
  await page.locator('textarea:visible').fill('Observação digitada.');
  const mic=page.getByRole('button',{name:/Ditar observação sobre/});
  await mic.click();await page.waitForFunction(()=>window.recordings[0]?.state==='recording');
  await page.clock.fastForward(121000);
  assert.equal(await page.evaluate(()=>window.recordings[0].state),'recording','O antigo corte de 120 s não pode retornar.');
  await page.getByRole('button',{name:/Parar gravação de/}).click();
  await page.waitForFunction(()=>document.querySelector('textarea').value.includes('Texto revisado completo.'));
  assert.equal(await page.locator('textarea:visible').inputValue(),'Observação digitada.\nTexto revisado completo.');
  assert.equal(await page.getByRole('link',{name:'Baixar áudio completo desta gravação'}).count(),1);
  await page.getByRole('button',{name:/Ditar observação sobre/}).click();
  await page.waitForFunction(()=>window.recordings[1]?.state==='recording');
  await page.clock.fastForward(601000);
  await page.waitForFunction(()=>document.querySelector('.voice-message').textContent.includes('Revisão indisponível'));
  assert.match(await page.locator('.voice-message').innerText(),/Limite configurado de 600 segundos/);
  assert.match(await page.locator('textarea:visible').inputValue(),/Texto original preservado/);
  assert.equal(calls,2);
  console.log('PASS: 600 s configured limit, explicit stop, complete audio chunks, append without loss, visible revision warning, retained audio.');
} finally {await browser.close()}
