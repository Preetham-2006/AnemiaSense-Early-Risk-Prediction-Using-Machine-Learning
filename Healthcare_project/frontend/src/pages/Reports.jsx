import { useEffect,useState } from "react";
import { Eye, RefreshCw } from "lucide-react";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import API from "../api";

export default function Reports(){
 const [reports,setReports]=useState([]),[loading,setLoading]=useState(true),[error,setError]=useState(""),[selected,setSelected]=useState(null);
 const load=async()=>{try{setLoading(true);setError("");const {data}=await API.get("/reports");setReports(Array.isArray(data)?data:[]);}catch(e){setError(e.response?.data?.message||"Unable to load reports.");}finally{setLoading(false);}};
 useEffect(()=>{load();},[]);
 return <div className="app-shell"><Sidebar/><main className="main"><Topbar/><div className="content"><div className="page-heading"><div><span className="eyebrow">HISTORY</span><h1>My Reports</h1><p>Every screening report is saved to your account.</p></div><button className="secondary-button" onClick={load}><RefreshCw size={17}/>Refresh</button></div>
 <div className="card"><div className="report-summary"><strong>{reports.length}</strong><span>saved reports</span></div>{loading?<div className="empty-state">Loading your reports...</div>:error?<div className="error-box">{error}</div>:reports.length===0?<div className="empty-state"><h3>No reports available yet</h3><p>Analyze your first blood report to see it here.</p></div>:<div className="table-wrapper"><table><thead><tr><th>Date</th><th>Result</th><th>Risk</th><th>Hemoglobin</th><th>MCV</th><th>Action</th></tr></thead><tbody>{reports.map(r=><tr key={r.id}><td>{new Date(r.created_at).toLocaleString()}</td><td><strong>{r.prediction}</strong></td><td><span className={`status-pill ${r.risk_level==="Low"?"green":"orange"}`}>{r.risk_level}</span></td><td>{r.hemoglobin}</td><td>{r.mcv}</td><td><button className="text-button" onClick={()=>setSelected(r)}><Eye size={16}/>View</button></td></tr>)}</tbody></table></div>}</div>
 {selected&&<div className="modal-backdrop" onClick={()=>setSelected(null)}><div className="card report-modal" onClick={e=>e.stopPropagation()}><div className="section-heading"><div><span className="eyebrow">REPORT #{selected.id}</span><h2>{selected.prediction}</h2></div><button className="icon-button" onClick={()=>setSelected(null)}>×</button></div><p>{new Date(selected.created_at).toLocaleString()} · {selected.risk_level} risk</p><div className="cbc-grid modal-grid">{[["Hemoglobin",selected.hemoglobin,"g/dL"],["RBC",selected.rbc,"×10⁶/µL"],["Hematocrit",selected.hematocrit,"%"],["WBC",selected.wbc,"×10³/µL"],["Platelets",selected.platelets,"×10³/µL"],["MCV",selected.mcv,"fL"],["MCHC",selected.mchc,"g/dL"],["MCH",selected.mch,"pg"],["RDW",selected.rdw,"%"]].map(([n,v,u])=><div className="metric" key={n}><span>{n}</span><strong>{v}</strong><small>{u}</small></div>)}</div><h3>Recommendations</h3><ul className="recommendation-list">{(selected.recommendations||[]).map((x,i)=><li key={i}>{x}</li>)}</ul></div></div>}
 </div></main></div>;
}
