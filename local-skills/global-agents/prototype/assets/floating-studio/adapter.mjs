import {createElement} from 'react';
import {createRoot} from 'react-dom/client';
import {ChatbotSendPrototypeStudio} from './component.js';

// Keep the approved component unchanged; the host owns fixtures and product actions.
export function mount(container, initialProps) {
  const root = createRoot(container);
  let props = initialProps;
  const render = () => root.render(createElement(ChatbotSendPrototypeStudio, props));
  render();
  return {
    update(patch) {props = {...props, ...patch}; render();},
    unmount() {root.unmount();},
  };
}
