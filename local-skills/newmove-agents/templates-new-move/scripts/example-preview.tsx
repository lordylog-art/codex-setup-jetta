import React, { useState, useRef, useEffect } from 'react';
import { ModalCenario, AjustesModalCenario } from '@/app/templates/modal-cenario';
import { IconeErro } from '@/features/global-cadastros/driver-modal-error';
import { ModalResultado } from '@/app/templates/modal-resultado';
import { AcoesModal } from '@/app/templates/acoes-modal';
import styles from '@/app/templates/modal-cenario.module.css';
import '@/app/programacao-confirmation-dialogs.css';
import { IMAGENS_JOTINHA } from '@/app/templates/catalogo-recursos';
import { useReviewControls } from './review-controls';
import { useReviewScenarios, type ReviewScenario } from './review-scenarios';
const scenarios:ReviewScenario[]=[
 {id:'sucesso',title:'Cadastrar motorista · sucesso',steps:[
  {label:'Digitar o nome do motorista',action:'fill',selector:'[data-review="name"]',value:'Marcos Silva — demonstração'},
  {label:'Selecionar o perfil Motorista',action:'select',selector:'[data-review="profile"]',value:'Motorista'},
  {label:'Clicar em cadastrar',action:'click',selector:'[data-review="submit"]'},
  {label:'Conferir confirmação de sucesso',action:'assert',selector:'dialog[data-tone="sucesso"] h3',text:'Cadastro revisado'}]},
 {id:'erro',title:'Cadastrar motorista · falha e correção',steps:[
  {label:'Preencher o cadastro',action:'fill',selector:'[data-review="name"]',value:'Marcos Silva — demonstração'},
  {label:'Enviar e aguardar falha simulada',action:'click',selector:'[data-review="submit"]'},
  {label:'Conferir mensagem de falha',action:'assert',selector:'[data-review="retry"]',text:'Voltar ao cadastro'},
  {label:'Voltar para corrigir',action:'click',selector:'[data-review="retry"]'},
  {label:'Verificar que o nome foi preservado',action:'assert',selector:'[data-review="name"]',value:'Marcos Silva — demonstração'},
  {label:'Corrigir o nome',action:'fill',selector:'[data-review="name"]',value:'Marcos Silva Santos — demonstração'},
  {label:'Simular serviço recuperado',action:'select',selector:'[data-review="outcome"]',value:'sucesso'},
  {label:'Tentar cadastrar novamente',action:'click',selector:'[data-review="submit"]'},
  {label:'Conferir sucesso após a correção',action:'assert',selector:'dialog[data-tone="sucesso"] h3',text:'Cadastro revisado'}]}
];


// Demonstration only; each grooming must supply its own complete consumer and manifest.
export default function Preview() {
  const surfaceId=new URLSearchParams(location.search).get('surface')||'cadastro';
  const title=surfaceId==='cadastro-2'?'Cadastro — exemplo 2':surfaceId==='cadastro-3'?'Cadastro — exemplo 3':'Revisar cadastro';
  const [open, setOpen] = useState(true), [configure, setConfigure] = useState(false);
  const [state, setState] = useState('padrao'), [result, setResult] = useState('');
  type Layout={tamanho:'compacto'|'padrao'|'amplo';apresentacao:'ilustrado'|'conteudo';posicao:'esquerda'|'direita';escala:'menor'|'padrao'|'maior';altura:'padrao'|'alta'};
  const defaultLayout:Layout={tamanho:'padrao',apresentacao:'ilustrado',posicao:'esquerda',escala:'padrao',altura:'padrao'};
  const [layouts,setLayouts]=useState<Record<string,Layout>>({});
  const scope=result||'padrao';
  const layoutFor=(id:string)=>layouts[id]||defaultLayout;
  const layout=layoutFor(scope);
  const {tamanho:size,apresentacao:presentation,posicao:position,escala:scale,altura:height}=layout;
  const updateLayout=<K extends keyof Layout>(key:K,value:Layout[K])=>setLayouts(current=>({...current,[scope]:{...(current[scope]||defaultLayout),[key]:value}}));
  const setSize=(value:Layout['tamanho'])=>updateLayout('tamanho',value);
  const setPresentation=(value:Layout['apresentacao'])=>updateLayout('apresentacao',value);
  const setPosition=(value:Layout['posicao'])=>updateLayout('posicao',value);
  const setScale=(value:Layout['escala'])=>updateLayout('escala',value);
  const setHeight=(value:Layout['altura'])=>updateLayout('altura',value);
  const [name,setName]=useState('Pessoa de demonstração');
  const [submitting,setSubmitting]=useState(false);
  const submitTimer=useRef<ReturnType<typeof setTimeout>|undefined>(undefined);
  useEffect(()=>()=>clearTimeout(submitTimer.current),[]);
  useReviewScenarios(surfaceId,scenarios,id=>{clearTimeout(submitTimer.current);setSubmitting(false);setOpen(true);setConfigure(false);setResult('');setName('');setProfile('Motorista');setState(id==='erro'?'erro':'sucesso')});
  const submit=()=>{if(submitting)return;setSubmitting(true);submitTimer.current=setTimeout(()=>{setSubmitting(false);setResult(state==='padrao'?'sucesso':state)},800)};
  const [profile, setProfile] = useState('Motorista');
  const [image, setImage] = useState('cadastro');
  const options=(values:string[][])=>values.map(([value,label])=>({value,label}));
  const controls=[
    {id:'tamanho',label:'Tamanho',value:size,options:options([['compacto','Compacto'],['padrao','Padrão'],['amplo','Amplo']])},
    {id:'apresentacao',label:'Apresentação',value:presentation,options:options([['ilustrado','Ilustrado'],['conteudo','Conteúdo expandido']])},
    {id:'altura',label:'Altura',value:height,options:options([['padrao','Padrão'],['alta','Alta']])},
    {id:'posicao',label:'Lado do Jotinha',value:position,options:options([['esquerda','Esquerda'],['direita','Direita']])},
    {id:'escala',label:'Escala do Jotinha',value:presentation==='conteudo'?'menor':scale,disabled:presentation==='conteudo',hint:presentation==='conteudo'?'Menor fixo no conteúdo expandido':'',options:options([['menor','Menor'],['padrao','Padrão'],['maior','Maior']])},
    {id:'imagem',label:'Imagem do Jotinha',value:image,disabled:Boolean(result),hint:result?'O resultado usa a imagem do seu estado':'',options:IMAGENS_JOTINHA.map(i=>({value:i.id,label:i.titulo}))},
    {id:'perfil',label:'Perfil demonstrativo',value:profile,disabled:Boolean(result),options:options([['Motorista','Motorista'],['Ajudante','Ajudante']])},
    {id:'estado',label:'Estado da prévia',value:result||'padrao',options:options([['padrao','Cadastro'],['sucesso','Sucesso'],['erro','Falha'],['aviso','Alerta']])},
  ];
  useReviewControls(surfaceId,controls,(id,value)=>{
    if(id==='tamanho')setSize(value as typeof size);
    if(id==='apresentacao')setPresentation(value as typeof presentation);
    if(id==='altura')setHeight(value as typeof height);
    if(id==='posicao')setPosition(value as typeof position);
    if(id==='escala')setScale(value as typeof scale);
    if(id==='imagem')setImage(value);
    if(id==='perfil')setProfile(value);
    if(id==='estado'){setOpen(true);setResult(value==='padrao'?'':value)}
  },scope);
  const close = () => {setOpen(false);setResult('')};
  return <main style={{fontFamily:'Segoe UI',padding:24}}>
    <h1>Revisar cadastro demonstrativo</h1><p>Componentes reais do catálogo. Os dados e resultados desta demonstração são fictícios.</p>
    <button onClick={()=>setOpen(true)}>Abrir demonstração</button>
    <ModalCenario {...layoutFor('padrao')} imagem={`/templates/avatar-${image}.png`} aberto={open&&!result} onFechar={close} tipo="cadastro" titulo={title} descricao="Confira os dados fictícios antes de simular a conclusão.">
      {configure&&<><AjustesModalCenario tamanho={size} onTamanho={setSize} apresentacao={presentation} onApresentacao={setPresentation} posicao={position} onPosicao={setPosition} escala={scale} onEscala={setScale}/>
      <label className={styles.campo}>Altura<select value={height} onChange={e=>setHeight(e.target.value as typeof height)}><option value="padrao">Padrão</option><option value="alta">Alta</option></select></label></>}
      <div className={styles.formulario}><label className={styles.campo}>Nome<input data-review="name" value={name} onChange={e=>setName(e.target.value)}/></label><label className={styles.campo}>Perfil<select data-review="profile" value={profile} onChange={e=>setProfile(e.target.value)}><option>Motorista</option><option>Ajudante</option></select></label>
      <label className={styles.campo}>Resultado simulado<select data-review="outcome" value={state} onChange={e=>setState(e.target.value)}><option value="padrao">Padrão — sucesso</option><option value="sucesso">Sucesso</option><option value="erro">Falha</option><option value="aviso">Alerta</option></select></label></div>
      <AcoesModal className={styles.acoes}><button onClick={()=>setConfigure(!configure)} aria-expanded={configure}>Configurar</button><button className={styles.secundario} onClick={close}>Cancelar</button><button data-review="submit" disabled={submitting} className={styles.primario} onClick={submit}>{submitting?'Cadastrando…':'Simular cadastro'}</button></AcoesModal>
    </ModalCenario>
    <ModalResultado {...layoutFor(result||'sucesso')} aberto={result==='sucesso'||result==='aviso'} onFechar={close} estado={result==='sucesso'?'sucesso':'aviso'} titulo={result==='sucesso'?'Cadastro revisado':'Confira os dados'} mensagem={result==='sucesso'?'A simulação foi concluída. Nenhum cadastro real foi alterado.':'Há dados que precisam de revisão nesta simulação.'}/>
    <ModalCenario {...layoutFor('erro')} aberto={result==='erro'} onFechar={()=>setResult('')} tipo="erro" titulo="Falha" descricao="Os dados foram preservados. Volte ao cadastro para corrigir."><div className={styles.status}><div className={styles.iconeResultado} style={{width:132,height:132}}><IconeErro/></div><h3>Cadastro não concluído</h3></div><AcoesModal className={styles.acoes}><button data-review="retry" className={styles.primario} onClick={()=>setResult('')}>Voltar ao cadastro</button></AcoesModal></ModalCenario>
  </main>;
}
