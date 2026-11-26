import {el} from './dom.js';
import {request} from './api.js';

const ns = 'http://www.w3.org/2000/svg';

function mark(kind, attrs, caption) {
  const item = document.createElementNS(ns, kind);
  for (const [attribute, value] of Object.entries(attrs)) item.setAttribute(attribute, value);
  if (caption) {
    const title = document.createElementNS(ns, 'title');
    title.textContent = caption;
    item.append(title);
  }
  return item;
}

function drawMask(item, slots) {
  const {width_mm: width, height_mm: height, frame_inset: margin} = item;
  const panel = mark('svg', {viewBox: '-5 -5 ' + (width+10) + ' ' + (height+10), role:'img',
    'aria-label':item.label+' 的边界、内保留区和试色位置'});
  panel.append(
    mark('rect',{x:0,y:0,width,height,class:'panel-outline'},'复制样张外圈'),
    mark('rect',{x:margin,y:margin,width:width-2*margin,height:height-2*margin,class:'working-area'},'可试色边界'),
    mark('rect',{x:item.hold_x1,y:item.hold_y1,width:item.hold_x2-item.hold_x1,height:item.hold_y2-item.hold_y1,
      class:'keepout'},'内保留区'));
  for (const slot of slots.filter((slot) => slot.panel === item.code)) {
    panel.append(mark('circle',{cx:slot.x_mm,cy:slot.y_mm,r:2.4,class:'registered'},
      slot.code + ' · ' + slot.state + ' · ' + slot.x_mm + ',' + slot.y_mm));
  }
  return panel;
}

export async function proofMap(root) {
  const [regions, slots] = await Promise.all([request('/proof_regions'), request('/patch_slots')]);
  if (!regions.length) return;
  const selector = el('select', {'aria-label':'绘图样张'}, regions.map((row) => el('option',{value:row.code},row.label)));
  const figure = el('figure',{class:'proof-map'},
    el('figcaption',{},'保护边界与已登记试色位'),selector);
  const plot = el('div',{});
  const label = el('small',{});
  function render() {
    const current = regions.find((row) => row.code === selector.value);
    plot.replaceChildren(drawMask(current, slots));
    label.textContent = '版次 '+current.revision+' · 深色为内保留区，圆点为试色位。';
  }
  selector.addEventListener('change',render);
  figure.append(plot,label);
  root.querySelector('.ledger')?.before(figure);
  render();
}
