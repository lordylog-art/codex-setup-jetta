'use client';

import {useEffect, useId, useLayoutEffect, useRef, useState, type RefObject} from 'react';
import './chatbot-send-prototype-studio.css';

export type ChatbotSendDemoContext = {
  signal: AbortSignal;
  wait: (ms: number) => Promise<void>;
  type: (text: string, onType: (value: string) => void) => Promise<void>;
};
export type ChatbotSendDemoStep = {
  id: string;
  label: string;
  target: string;
  action?: (context: ChatbotSendDemoContext & {target: HTMLElement}) => void | Promise<void>;
};
type DemoStatus = 'ready' | 'playing' | 'paused' | 'complete' | 'failed';
type DemoSnapshot = {status: DemoStatus; index: number; error: string};
type RunnerStep = {label: string; execute: (context: ChatbotSendDemoContext) => Promise<void>};

// Runner is independent of React so cancellation, pauses and single-step execution can be tested.
export class ChatbotSendDemoRunner {
  private controller = new AbortController();
  private active = false;
  private allowed = false;
  private single = false;
  private state: DemoSnapshot = {status: 'ready', index: 0, error: ''};
  speed = 1;
  constructor(private readonly publish: (state: DemoSnapshot) => void) {}

  private update(patch: Partial<DemoSnapshot>) {
    this.state = {...this.state, ...patch};
    this.publish(this.state);
  }
  reset() {
    this.controller.abort();
    this.controller = new AbortController();
    this.active = false;
    this.allowed = false;
    this.single = false;
    this.update({status: 'ready', index: 0, error: ''});
  }
  pause() {
    if (this.state.status !== 'playing') return;
    this.allowed = false;
    this.update({status: 'paused'});
  }
  async start(steps: RunnerStep[], oneStep = false) {
    if (this.state.status === 'complete' || this.state.status === 'failed') return;
    this.allowed = true;
    this.single = oneStep;
    this.update({status: 'playing'});
    if (this.active) return;
    this.active = true;
    const signal = this.controller.signal;
    const check = () => {if (signal.aborted) throw new DOMException('Canceled', 'AbortError');};
    const tick = () => new Promise<void>((resolve, reject) => {
      const cancel = () => {clearTimeout(timer); reject(new DOMException('Canceled', 'AbortError'));};
      const timer = setTimeout(() => {signal.removeEventListener('abort', cancel); resolve();}, 16);
      signal.addEventListener('abort', cancel, {once: true});
    });
    const wait = async (ms: number, done?: () => boolean) => {
      let remaining = ms;
      do {
        check();
        const before = performance.now();
        const wasAllowed = this.allowed;
        await tick();
        check();
        if (done?.()) return;
        if (wasAllowed && this.allowed) remaining -= (performance.now() - before) * this.speed;
      } while (remaining > 0 || !this.allowed);
    };
    const context: ChatbotSendDemoContext = {
      signal, wait,
      type: async (text, onType) => {
        let value = '';
        for (const character of text) {
          await wait(45);
          check();
          value += character;
          onType(value);
        }
      },
    };
    try {
      while (this.state.index < steps.length) {
        await wait(0);
        const step = steps[this.state.index];
        let finished = false;
        const action = Promise.resolve().then(() => step.execute(context)).finally(() => {finished = true;});
        const deadline = (async () => {
          for (let elapsed = 0; elapsed < 15000 && !finished; elapsed += 100) await wait(100, () => finished);
          if (!finished) throw new Error('A interação não respondeu em 15 segundos. Reinicie para tentar novamente.');
        })();
        await Promise.race([action, deadline]);
        check();
        this.update({index: this.state.index + 1});
        if (this.single) this.allowed = false;
        if (this.state.index === steps.length) {
          this.allowed = false;
          this.update({status: 'complete'});
          break;
        }
        if (!this.allowed) this.update({status: 'paused'});
        await wait(400);
      }
    } catch (error) {
      if (!signal.aborted) {
        this.allowed = false;
        this.update({status: 'failed', error: error instanceof Error ? error.message : 'Não foi possível executar este passo.'});
        this.controller.abort();
      }
    } finally {
      if (signal === this.controller.signal) this.active = false;
    }
  }
}

export class ChatbotSendScenarioQueue {
  private ids:string[]=[];
  private index=-1;
  get current(){return this.ids[this.index]??null;}
  get progress(){return {current:Math.min(this.index+1,this.ids.length),total:this.ids.length};}
  start(ids:string[]){this.ids=[...ids];this.index=ids.length?0:-1;return this.current;}
  advance(){if(this.current!==null)this.index++;return this.current;}
  cancel(){this.ids=[];this.index=-1;}
}

export type ChatbotSendPrototypeStudioProps = {
  variant: 'A' | 'B' | 'C' | 'D' | 'E';
  onVariantChange: (variant: 'A' | 'B' | 'C' | 'D' | 'E') => void;
  scenario: string;
  onScenarioChange: (scenario: string) => void;
  scenarios: {id: string; label: string; note: string}[];
  steps: ChatbotSendDemoStep[];
  scope: RefObject<HTMLElement | null>;
  onReset: () => void;
  onStatusChange?: (status: DemoStatus) => void;
  theme?: 'light'|'dark';
  onThemeChange?: () => void;
  onSpeedChange?: (speed:number) => void;
};

export function ChatbotSendPrototypeStudio(props: ChatbotSendPrototypeStudioProps) {
  const latest = useRef(props);
  latest.current = props;
  const [snapshot, setSnapshot] = useState<DemoSnapshot>({status: 'ready', index: 0, error: ''});
  const [cursor, setCursor] = useState<{x: number; y: number; click: boolean} | null>(null);
  const [speed, setSpeed] = useState(1);
  const [replayRequested,setReplayRequested]=useState(false);
  const [allScenarios,setAllScenarios]=useState(false),[batchSummary,setBatchSummary]=useState('');
  const queue=useRef(new ChatbotSendScenarioQueue());
  const activeVariant=useRef(props.variant);
  const [position,setPosition]=useState<{x:number;y:number}|null>(null);
  const drag=useRef<{x:number;y:number;left:number;top:number}|null>(null),bar=useRef<HTMLElement>(null),menu=useRef<HTMLDivElement>(null),menuId=useId();
  const runner = useRef<ChatbotSendDemoRunner | null>(null);
  if (!runner.current) runner.current = new ChatbotSendDemoRunner(setSnapshot);

  useEffect(() => {latest.current.onStatusChange?.(snapshot.status);}, [snapshot.status]);
  useEffect(() => {latest.current.onSpeedChange?.(speed);}, [speed]);
  useLayoutEffect(() => {
    if(activeVariant.current!==props.variant){queue.current.cancel();setBatchSummary('');activeVariant.current=props.variant;}
    runner.current!.reset();
    setCursor(null);
    return () => {runner.current!.reset();};
  }, [props.variant, props.scenario]);

  useEffect(() => {
    const scope = props.scope.current;
    if (!scope) return;
    const pause = (event: Event) => {
      if (event.isTrusted && event.target instanceof Element && !event.target.closest('[data-demo-studio]')) runner.current!.pause();
    };
    scope.addEventListener('pointerdown', pause, true);
    scope.addEventListener('keydown', pause, true);
    return () => {
      scope.removeEventListener('pointerdown', pause, true);
      scope.removeEventListener('keydown', pause, true);
    };
  }, [props.scope]);

  function reset() {
    queue.current.cancel();setBatchSummary('');
    setReplayRequested(false);
    runner.current!.reset();
    setCursor(null);
    latest.current.onReset();
  }
  function play(oneStep = false) {
    const steps = latest.current.steps.map(step => ({label: step.label, execute: async (context: ChatbotSendDemoContext) => {
      let target: HTMLElement | null = null;
      for (let elapsed = 0; elapsed <= 4000; elapsed += 80) {
        if (context.signal.aborted) return;
        const candidate = latest.current.scope.current?.querySelector<HTMLElement>(step.target);
        if (candidate && candidate.getClientRects().length && !candidate.matches(':disabled')) {target = candidate; break;}
        await context.wait(80);
      }
      if (!target) throw new Error(`“${step.label}”: controle indisponível. Reinicie a demonstração.`);
      target.scrollIntoView({block: 'nearest', inline: 'nearest', behavior: 'instant'});
      await context.wait(80);
      const bounds = target.getBoundingClientRect();
      const scope = latest.current.scope.current!;
      const area = scope.getBoundingClientRect();
      setCursor({x: bounds.left - area.left + scope.scrollLeft + bounds.width / 2, y: bounds.top - area.top + scope.scrollTop + bounds.height / 2, click: false});
      await context.wait(window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 60 : 420);
      if (!target.isConnected || !scope.contains(target)) throw new Error(`“${step.label}”: o controle mudou. Reinicie a demonstração.`);
      setCursor(position => position && {...position, click: true});
      target.focus({preventScroll: true});
      if (step.action) await step.action({...context, target});
      else target.click();
      await context.wait(180);
      setCursor(position => position && {...position, click: false});
    }}));
    void runner.current!.start(steps, oneStep);
  }
  useEffect(()=>{if(replayRequested){setReplayRequested(false);play();}},[replayRequested]);
  useEffect(()=>{
    if(snapshot.status==='failed'&&queue.current.current!==null){queue.current.cancel();setBatchSummary('Sequência interrompida');return;}
    if(snapshot.status!=='complete'||queue.current.current===null)return;
    const next=queue.current.advance(),progress=queue.current.progress;
    if(next===null){setBatchSummary(`${progress.total} cenários concluídos`);return;}
    setBatchSummary(`Cenário ${progress.current}/${progress.total}`);
    runner.current!.reset();setCursor(null);latest.current.onScenarioChange(next);setReplayRequested(true);
  },[snapshot.status]);
  function begin(){
    reset();
    if(allScenarios){const first=queue.current.start(latest.current.scenarios.map(item=>item.id));if(first){setBatchSummary(`Cenário 1/${latest.current.scenarios.length}`);latest.current.onScenarioChange(first);}}
    setReplayRequested(true);
  }
  const activeScenario = props.scenarios.find(item => item.id === props.scenario);
  const variants = ['A', 'B', 'C', 'D', 'E'] as const;
  const variantNames = {A: 'Lista direta', B: 'Lista e prévia', C: 'Por finalidade', D: 'Seleção compacta', E: 'Detalhes na lista'};
  const current = props.steps[snapshot.index];
  const status = {ready: 'Pronto para explorar', playing: 'Em reprodução', paused: 'Pausado', complete: 'Demonstração concluída', failed: 'Falha na demonstração'}[snapshot.status];
  function move(x:number,y:number){const r=bar.current?.getBoundingClientRect();if(r)setPosition({x:Math.max(8,Math.min(x,window.innerWidth-r.width-8)),y:Math.max(8,Math.min(y,window.innerHeight-r.height-8))});}
  useEffect(()=>{const clamp=()=>{const r=bar.current?.getBoundingClientRect();if(r)move(r.x,r.y);};window.addEventListener('resize',clamp);return()=>window.removeEventListener('resize',clamp);},[]);
  return <>
    {cursor && <div className={`chatbot-send-demo-cursor${cursor.click ? ' is-clicking' : ''}${snapshot.status === 'paused' ? ' is-paused' : ''}`} style={{left: cursor.x, top: cursor.y}} aria-hidden="true"><svg viewBox="0 0 24 30"><path d="M3 2v23l6-6 5 9 4-2-5-9h9Z" fill="#fff" stroke="#142c28" strokeWidth="1.6"/></svg><span/></div>}
    <aside ref={bar} className="chatbot-send-demo-studio" data-demo-studio="true" aria-label="Estúdio flutuante de demonstração" style={position?{left:position.x,top:position.y,right:'auto'}:undefined} title={'Protótipos · Simulação · '+(batchSummary||status)}
      onPointerDown={event=>{if((event.target as HTMLElement).closest('button,select'))return;const r=event.currentTarget.getBoundingClientRect();drag.current={x:event.clientX,y:event.clientY,left:r.x,top:r.y};menu.current?.hidePopover();event.currentTarget.setPointerCapture(event.pointerId);}}
      onPointerMove={event=>{if(drag.current)move(drag.current.left+event.clientX-drag.current.x,drag.current.top+event.clientY-drag.current.y);}}
      onPointerUp={()=>{drag.current=null;}} onPointerCancel={()=>{drag.current=null;}}>
      <span className="chatbot-send-demo-grip" tabIndex={0} role="button" aria-label="Mover estúdio com as setas" title="Arraste para mover" onKeyDown={event=>{if(!['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(event.key))return;event.preventDefault();event.stopPropagation();const r=bar.current!.getBoundingClientRect();move(r.x+(event.key==='ArrowLeft'?-16:event.key==='ArrowRight'?16:0),r.y+(event.key==='ArrowUp'?-16:event.key==='ArrowDown'?16:0));}}>⠿</span>
      <button type="button" className="chatbot-send-demo-play" aria-label={snapshot.status==='playing'?'Pausar':snapshot.status==='paused'?'Continuar':'Iniciar'} title={batchSummary||status} disabled={!props.steps.length} onClick={()=>{if(snapshot.status==='playing')runner.current!.pause();else if(snapshot.status==='paused')play();else begin();}}><svg viewBox="0 0 20 20" aria-hidden="true">{snapshot.status==='playing'?<path d="M6 4h3v12H6zm5 0h3v12h-3Z"/>:<path d="m6 3 11 7-11 7Z"/>}</svg></button>
      <span className="chatbot-send-demo-divider" aria-hidden="true"/>
      <select className="chatbot-send-demo-variant-picker" aria-label="Protótipo" title="Escolher uma das cinco versões" value={props.variant} onChange={event=>{reset();props.onVariantChange(event.target.value as typeof props.variant);}}>{variants.map((variant,index)=><option key={variant} value={variant}>{index+1} · {variantNames[variant]}</option>)}</select>
      <span className="chatbot-send-demo-divider" aria-hidden="true"/>
      <button type="button" className="chatbot-send-demo-scenario" popoverTarget={menuId} aria-haspopup="menu" aria-label="Cenário" title={activeScenario?.label}><svg viewBox="0 0 20 20" aria-hidden="true"><path d="m7 3 10 7-10 7M3 3v14"/></svg><span>Cenário</span></button>
      <select aria-label="Velocidade" title="Velocidade da demonstração" value={speed} onChange={event=>{const value=Number(event.target.value);setSpeed(value);runner.current!.speed=value;}}><option value={0.5}>0,5×</option><option value={1}>1×</option><option value={2}>2×</option></select>
      <button type="button" className="chatbot-send-demo-theme" aria-label={props.theme==='light'?'Ativar tema escuro':'Ativar tema claro'} title={props.theme==='light'?'Tema escuro':'Tema claro'} onClick={props.onThemeChange}>{props.theme==='light'?<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 15A9 9 0 0 1 9 4a9 9 0 1 0 11 11Z"/></svg>:<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/></svg>}</button>
      <div className="chatbot-send-demo-status" role="status" aria-live="polite">{batchSummary?batchSummary+' · ':''}{status} · {snapshot.index}/{props.steps.length} · {snapshot.error||current?.label}</div>
      <progress value={snapshot.index} max={Math.max(1,props.steps.length)} aria-label="Progresso da demonstração"/>
    </aside>
    <div ref={menu} id={menuId} popover="auto" className="chatbot-send-demo-menu" data-demo-studio="true" onToggle={event=>{if(event.newState!=='open')return;const r=bar.current!.getBoundingClientRect(),m=event.currentTarget; m.style.left=Math.max(8,Math.min(r.x,innerWidth-m.offsetWidth-8))+'px';m.style.top=(r.bottom+m.offsetHeight+8<innerHeight?r.bottom+8:Math.max(8,r.top-m.offsetHeight-8))+'px';}}>
      <strong>Cenários · Simulação</strong>
      <label>Situação<select aria-label="Situação da demonstração" value={props.scenario} onChange={event=>{reset();props.onScenarioChange(event.target.value);}}>{props.scenarios.map(item=><option key={item.id} value={item.id}>{item.label}</option>)}</select></label>
      <label className="chatbot-send-demo-all"><input type="checkbox" checked={allScenarios} onChange={event=>{setAllScenarios(event.target.checked);queue.current.cancel();setBatchSummary('');if(!event.target.checked)runner.current!.pause();}}/>Executar todos os cenários</label>
      <div><button type="button" onClick={()=>{play(true);menu.current?.hidePopover();}} disabled={snapshot.status==='playing'||snapshot.status==='complete'||snapshot.status==='failed'}>Próximo passo</button><button type="button" onClick={()=>{reset();menu.current?.hidePopover();}}>Reiniciar</button></div>
      {snapshot.error&&<p role="alert">{snapshot.error}</p>}
    </div>
  </>;
}
