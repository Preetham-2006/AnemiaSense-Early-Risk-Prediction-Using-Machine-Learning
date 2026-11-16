import { useEffect,useState } from "react";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import API from "../api";

const metrics=[
 ["Hemoglobin","g/dL","hemoglobin",18],
 ["RBC","×10⁶/µL","rbc",8],
 ["Hematocrit","%","hematocrit",50],
 ["WBC","×10³/µL","wbc",15],
 ["Platelets","×10³/µL","platelets",500],
 ["MCV","fL","mcv",120],
 ["MCHC","g/dL","mchc",40],
 ["MCH","pg","mch",40],
 ["RDW","%","rdw",25],
];
export default function Trends(){const [reports,setReports]=useState([]),[error,setError]=useState("");useEffect(()=>{API.get("/reports").then(r=>setReports(Array.isArray(r.data)?[...r.data].reverse():[])).catch(e=>setError(e.response?.data?.message||"Unable to load health trends."));},[]);return <div className="app-shell"><Sidebar/><main className="main"><Topbar/><div className="content"><div className="page-heading"><span className="eyebrow">MONITORING</span><h1>Health Trends</h1><p>Track your CBC values across all saved reports.</p></div>{error&&<div className="error-box">{error}</div>}<div className="trend-grid">{metrics.map(([title,unit,field,max])=><TrendCard key={field} title={title} unit={unit} field={field} max={max} reports={reports}/>)}</div>{reports.length===0&&<div className="empty-card"><h2>No trend data yet</h2><p>Submit at least one report to start tracking your CBC values.</p></div>}</div></main></div>}
function TrendCard({title,unit,field,max,reports}){return <div className="card trend-card"><div className="section-heading"><div><h3>{title}</h3><p>{unit}</p></div><span>{reports.length} points</span></div>{reports.length<1?<p>Submit reports to see trends.</p>:<div className="trend-bars">{reports.slice(-12).map((r,i)=>{const value=Number(r[field])||0;const h=Math.min(100,Math.max(5,(value/max)*100));return <div className="trend-item" key={r.id}><div className="trend-bar" style={{height:`${h}%`}}/><span>{value}</span><small>{i+1}</small></div>})}</div>}</div>}
