// Local preview only: actions exercise the rendered controls and their handlers.
export async function playScenario(doc, steps, {signal, paused=()=>false, report=()=>{}, delay=650, timeout=5000}={}) {
  const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
  const checkpoint=async()=>{while(paused()&&!signal?.aborted)await sleep(60);if(signal?.aborted)throw new DOMException('Execução interrompida','AbortError')};
  const wait=async ms=>{for(let elapsed=0;elapsed<ms;elapsed+=50){await checkpoint();await sleep(Math.min(50,ms-elapsed))}};
  let marked;
  try {
    for(let index=0;index<steps.length;index++){
      await checkpoint();const step=steps[index];report({index,label:step.label,status:'running'});
      let target;let elapsed=0;
      while(elapsed<=timeout){
        await checkpoint();target=doc.querySelector(step.selector);
        const visible=target&&target.getClientRects().length>0;
        const matches=visible&&(step.text===undefined||target.textContent.includes(step.text))&&(step.value===undefined||step.action!=='assert'||target.value===step.value);
        if(matches)break;
        if(elapsed===timeout)throw Error('Etapa não encontrou o resultado esperado: '+step.label);
        await wait(100);elapsed=Math.min(timeout,elapsed+100);
      }
      if(marked)marked.removeAttribute('data-replay-active');marked=target;target.setAttribute('data-replay-active','true');target.scrollIntoView({block:'nearest'});
      await wait(delay);
      if(step.action==='click'){
        if(target.disabled)throw Error('Ação indisponível: '+step.label);
        target.click();
      }else if(step.action==='fill'||step.action==='select'){
        if(target.disabled||target.readOnly)throw Error('Campo indisponível: '+step.label);
        target.focus();const view=doc.defaultView;
        const prototype=step.action==='select'?view.HTMLSelectElement.prototype:view.HTMLInputElement.prototype;
        const setter=Object.getOwnPropertyDescriptor(prototype,'value').set;
        const values=step.action==='fill'?Array.from(step.value).map((_,i)=>Array.from(step.value).slice(0,i+1).join('')):[step.value];
        if(!values.length)values.push('');
        for(const value of values){await checkpoint();setter.call(target,value);target.dispatchEvent(new view.Event(step.action==='select'?'change':'input',{bubbles:true}));await wait(step.action==='fill'?40:0)}
      }else if(step.action!=='assert')throw Error('Ação de cenário não suportada');
      await wait(delay);report({index,label:step.label,status:'passed'});
    }
  } finally {marked?.removeAttribute('data-replay-active')}
}
