const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
export function remainingSurfaces(surfaces,draft){
 return surfaces.filter(s=>!same(draft.approvedItems?.[s.id],draft.items.find(i=>i.id===s.id)));
}
export function acceptDelivered(draft,result){
 if(result.delivery?.status!=='sent')return;
 draft.approvedItems??={};
 for(const item of result.feedback||[]){
  if(item.decision==='agree'&&same(item,draft.items.find(i=>i.id===item.id)))draft.approvedItems[item.id]=JSON.parse(JSON.stringify(item));
 }
}
