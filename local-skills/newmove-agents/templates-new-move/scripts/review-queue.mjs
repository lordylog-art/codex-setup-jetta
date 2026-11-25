const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
export function reviewGroups(surfaces){
 const groups=new Map(),result=[],ids=new Set(surfaces.map(s=>s.variantGroup).filter(Boolean));
 for(const surface of surfaces){
  if(!surface.variantGroup){
   let id=surface.id;while(ids.has(id))id='surface:'+id;ids.add(id);
   result.push({id,title:surface.title,surfaces:[surface]});
   continue;
  }
  const id=surface.variantGroup;
  if(!groups.has(id)){const group={id,title:surface.variantGroupTitle||surface.title,surfaces:[]};groups.set(id,group);result.push(group)}
  groups.get(id).surfaces.push(surface);
 }
 return result;
}
export function restoreDraft(manifest,read){
 const parse=key=>{try{return JSON.parse(read('template-review:'+JSON.stringify(key)))}catch{return null}};
 const pristine=draft=>!Object.keys(draft?.variantChoices||{}).length&&draft?.items?.every(item=>item.decision==='pending'&&!item.text);
 const seeded=local=>{
  const seed={items:structuredClone(manifest.deliveredReview.feedback),...(manifest.deliveredReview.variantChoices?{variantChoices:structuredClone(manifest.deliveredReview.variantChoices)}:{})};
  acceptDelivered(seed,manifest.deliveredReview);
  for(const item of local?.items||[]){
   const sent=seed.items.find(sent=>sent.id===item.id);
   if(sent&&item.configuration&&!Object.entries(item.configuration).every(([key,value])=>same(value,sent.configuration?.[key]))){
    Object.assign(sent,item,{configuration:{...sent.configuration,...item.configuration}});
   }
  }
  return seed;
 };
 let draft=parse(manifest);
 if(draft&&(!pristine(draft)||manifest.deliveredReview?.delivery?.status!=='sent'))return draft;
 if(!draft&&manifest.previousManifest?.grooming===manifest.grooming){
  draft=parse(manifest.previousManifest);
  if(draft&&(!pristine(draft)||manifest.deliveredReview?.delivery?.status!=='sent')){
   draft=structuredClone(draft);
   for(const [id,configuration] of Object.entries(manifest.configurationOverrides||{})){
    const item=draft.items?.find(item=>item.id===id);
    if(item)item.configuration={...item.configuration,...configuration};
   }
   return draft;
  }
 }
 if(manifest.deliveredReview?.delivery?.status==='sent'){
  draft=seeded(draft);
  for(const [id,configuration] of Object.entries(manifest.configurationOverrides||{})){
   const item=draft.items.find(item=>item.id===id);
   if(item)item.configuration={...item.configuration,...configuration};
  }
  return draft;
 }
 return null;
}
export function remainingSurfaces(surfaces,draft){
 return reviewGroups(surfaces).flatMap(group=>{
  if(group.surfaces[0].variantGroup){
   const approved=draft.approvedGroups?.[group.id];
   return approved&&approved.choice===draft.variantChoices?.[group.id]&&same(approved.items,group.surfaces.map(s=>draft.items.find(i=>i.id===s.id)))?[]:group.surfaces;
  }
  return group.surfaces.filter(s=>!same(draft.approvedItems?.[s.id],draft.items.find(i=>i.id===s.id)));
 });
}
export function acceptDelivered(draft,result){
 if(result.delivery?.status!=='sent')return;
 draft.approvedItems??={};
 for(const group of reviewGroups(result.surfaces||[]).filter(group=>group.surfaces[0].variantGroup)){
  const choice=result.variantChoices?.[group.id];
  const items=group.surfaces.map(s=>result.feedback?.find(i=>i.id===s.id));
  if(choice&&group.surfaces.some(s=>s.id===choice)&&choice===draft.variantChoices?.[group.id]&&items.every(Boolean)&&items.find(i=>i.id===choice)?.decision==='agree'&&same(items,group.surfaces.map(s=>draft.items.find(i=>i.id===s.id)))){
   draft.approvedGroups??={};
   draft.approvedGroups[group.id]=structuredClone({choice,items});
  }
 }
 for(const item of result.feedback||[]){
  if(item.decision==='agree'&&same(item,draft.items.find(i=>i.id===item.id)))draft.approvedItems[item.id]=JSON.parse(JSON.stringify(item));
 }
}
