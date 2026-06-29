import { MapContainer, TileLayer, CircleMarker, Polyline, Polygon, Tooltip, useMap } from 'react-leaflet';
import { AudioEvent, Incident } from '../api/client';
import Legend from './Legend';
const q=(x:string)=>x==='good'?'#42f58d':x==='medium'?'#ffd166':'#ff5b6e';
function Fit({pts}:{pts:[number,number][]}){const map=useMap(); if(pts.length>1) setTimeout(()=>map.fitBounds(pts,{padding:[80,80]}),0); return null}
export default function MapView({events,incident}:{events:AudioEvent[];incident?:Incident}){const pts=(incident?.trajectory_points||[]).map(p=>[p.lat,p.lon] as [number,number]); const heat=pts.length?[pts.map(p=>[p[0]+.002,p[1]-.004] as [number,number]),pts.map(p=>[p[0]-.002,p[1]+.004] as [number,number]).reverse()].flat():[]; return <div className="mapWrap"><MapContainer center={[56.846,60.607]} zoom={13} attributionControl>
<TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="&copy; OpenStreetMap contributors" />
{heat.length>2&&<Polygon positions={heat} pathOptions={{color:'#9b5cff',fillColor:'#9b5cff',fillOpacity:.16,weight:1}}/>}
{events.map(e=><CircleMarker key={e.id} center={[e.lat,e.lon]} radius={8+e.signal_level/18} pathOptions={{color:q(e.noise_quality),fillColor:q(e.noise_quality),fillOpacity:.45}}><Tooltip>Сообщение #{e.id}<br/>{e.predicted_class} {Math.round(e.confidence*100)}%</Tooltip></CircleMarker>)}
{pts.length>1&&<Polyline positions={pts} pathOptions={{color:'#ffcc00',weight:4,dashArray:'8 8'}}/>}<Fit pts={pts}/>
</MapContainer><Legend /></div>}
