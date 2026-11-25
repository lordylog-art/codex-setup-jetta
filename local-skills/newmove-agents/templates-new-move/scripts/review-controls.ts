import { useEffect } from 'react';

export type ReviewControl = {id:string; label:string; value:string; options:{value:string;label:string}[]; disabled?:boolean; hint?:string};

/** Publish only options actually supported by the active template. */
export function useReviewControls(surfaceId:string, controls:ReviewControl[], change:(id:string,value:string)=>void, scope?:string) {
  useEffect(()=>{
    const publish=()=>parent.postMessage({type:'template-review:controls',surfaceId,controls,scope},location.origin);
    const receive=(event:MessageEvent)=>{
      if(event.source!==parent||event.origin!==location.origin)return;
      if(event.data?.type==='template-review:request')return publish();
      if(event.data?.type!=='template-review:change')return;
      const control=controls.find(c=>c.id===event.data.id);
      if(control&&!control.disabled&&control.options.some(o=>o.value===event.data.value))change(control.id,event.data.value);
    };
    window.addEventListener('message',receive);publish();
    return()=>window.removeEventListener('message',receive);
  },[surfaceId,controls,change,scope]);
}
