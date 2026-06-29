import { MapContainer, TileLayer, CircleMarker, Polyline, Polygon, Tooltip } from 'react-leaflet';
import L from 'leaflet';
import { Sensor, AudioEvent, Incident } from '../api/client';
import Legend from './Legend';
const q=(x:string)=>x==='good'?'#42f58d':x==='medium'?'#ffd166':'#ff5b6e';
export default function MapView({sensors,events,incident}:{sensors:Sensor[];events:AudioEvent[];incident?:Incident}){const pts=(incident?.trajectory_points||[]).map(p=>[p.lat,p.lon] as [number,number]); const last=pts.at(-1); const heat=pts.length?[pts.map(p=>[p[0]+.006,p[1]-.01] as [number,number]),pts.map(p=>[p[0]-.006,p[1]+.01] as [number,number]).reverse()].flat():[]; return <div className="mapWrap"><MapContainer center={[55.752,37.616]} zoom={12} zoomControl={false} attributionControl={false}>
<TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" eventHandlers={{tileerror:()=>document.querySelector('.mapWrap')?.classList.add('fallback')}} />
{heat.length>2&&<Polygon positions={heat} pathOptions={{color:'#9b5cff',fillColor:'#9b5cff',fillOpacity:.16,weight:1}}/>}
{sensors.map(s=><CircleMarker key={s.id} center={[s.lat,s.lon]} radius={7} pathOptions={{color:'#72ddf7',fillColor:'#72ddf7',fillOpacity:.85}}><Tooltip>{s.name}<br/>{s.device_type}</Tooltip></CircleMarker>)}
{events.map(e=><CircleMarker key={e.id} center={[e.lat,e.lon]} radius={8+e.signal_level/18} pathOptions={{color:q(e.noise_quality),fillColor:q(e.noise_quality),fillOpacity:.45}}><Tooltip>Событие #{e.id}<br/>{e.predicted_class} {Math.round(e.confidence*100)}%</Tooltip></CircleMarker>)}
{pts.length>1&&<Polyline positions={pts} pathOptions={{color:'#ffcc00',weight:4,dashArray:'8 8'}}/>}{last&&<CircleMarker center={last} radius={14} pathOptions={{color:'#ffcc00',fillColor:'#ffcc00',fillOpacity:.35}}><Tooltip>Направление-гипотеза: {incident?.direction_bearing}°</Tooltip></CircleMarker>}
</MapContainer><div className="localMap">Локальная имитация карты: сетка промзоны без внешних тайлов</div><Legend /></div>}
