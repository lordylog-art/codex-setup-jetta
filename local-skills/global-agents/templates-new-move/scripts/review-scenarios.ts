import { useEffect, useRef } from 'react';
export type ReviewScenario={id:string;title:string;steps:{label:string;action:'fill'|'select'|'click'|'assert';selector:string;value?:string;text?:string}[]};
export function useReviewScenarios(surfaceId:string,scenarios:ReviewScenario[],reset:(id:string)=>void){
 const resetRef=useRef(reset);resetRef.current=reset;
 useEffect(()=>{
  const publish=()=>parent.postMessage({type:'template-review:scenarios',surfaceId,scenarios},location.origin);
  const receive=(event:MessageEvent)=>{
   if(event.origin!==location.origin||event.source!==parent)return;
   if(event.data?.type==='template-review:request')publish();
   if(event.data?.type==='template-review:scenario-reset'&&scenarios.some(s=>s.id===event.data.id)){
    resetRef.current(event.data.id);
    requestAnimationFrame(()=>requestAnimationFrame(()=>parent.postMessage({type:'template-review:scenario-ready',surfaceId,id:event.data.id},location.origin)));
   }
  };
  window.addEventListener('message',receive);publish();return()=>window.removeEventListener('message',receive);
 },[surfaceId,scenarios]);
}
