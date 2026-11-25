const stage = document.querySelector('#stage');
const field = document.querySelector('#demo-input');
const result = document.querySelector('#result');
const scenarios = [
  {id:'baseline', label:'Caminho completo', note:'Fixture sintética local.'},
  {id:'long', label:'Texto longo', note:'Fixture sintética local.'},
  {id:'recovery', label:'Recuperação', note:'Fixture sintética local.'},
];
let variant = 'A', scenario = 'baseline', theme = 'dark';
const reset = () => {field.value = ''; result.textContent = 'Pronto para explorar';};
function steps() {
  const text = scenario === 'long' ? 'Texto sintético com acentos e detalhes para testar a demonstração.' : scenario === 'recovery' ? 'Dados corrigidos' : 'Olá, demonstração';
  return [
    {id:'type', label:'Preencher exemplo', target:'#demo-input', action:({type,target}) => type(text, value => {target.value=value; target.dispatchEvent(new Event('input',{bubbles:true}));})},
    {id:'apply', label:'Aplicar exemplo', target:'#demo-apply'},
  ];
}
document.querySelector('#demo-apply').addEventListener('click', () => {result.textContent=field.value || 'Preencha o exemplo para continuar.';});
const studio = PrototypeFloatingStudio.mount(document.querySelector('#studio'), {
  variant, scenario, scenarios, steps:steps(), scope:{current:stage}, theme,
  onReset:reset,
  onVariantChange(value) {variant=value; reset(); studio.update({variant,steps:steps()});},
  onScenarioChange(value) {scenario=value; reset(); studio.update({scenario,steps:steps()});},
  onThemeChange() {theme=theme==='dark'?'light':'dark'; document.documentElement.dataset.theme=theme; studio.update({theme});},
});
