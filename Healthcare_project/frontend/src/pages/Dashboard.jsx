import { useEffect, useState } from "react";
import { Activity, FileText, ShieldCheck, TrendingUp, ArrowRight, AlertCircle } from "lucide-react";
import { useNavigate } from "react-router-dom";
import API from "../api";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import StatCard from "../components/StatCard";
import Chatbot from "../components/Chatbot";

export default function Dashboard() {
  const navigate=useNavigate(); const [data,setData]=useState(null); const [loading,setLoading]=useState(true); const [error,setError]=useState("");
  const user=JSON.parse(localStorage.getItem("user")||"{}");
  useEffect(()=>{API.get("/dashboard").then(r=>setData(r.data)).catch(e=>setError(e.response?.data?.message||"Unable to load dashboard.")).finally(()=>setLoading(false));},[]);
  const report=data?.latest_report; const recent=data?.reports||[];
  return <div className="app-shell"><Sidebar/><main className="main"><Topbar/><div className="content">
    <div className="page-heading"><div><span className="eyebrow">BLOOD HEALTH OVERVIEW</span><h1>Welcome, {user.name||"Patient"} 👋</h1><p>Your latest screening, report history and CBC trends in one place.</p></div><button className="primary-button" onClick={()=>navigate("/analyze")}><Activity size={18}/>Analyze New Report</button></div>
    {error&&<div className="error-box"><AlertCircle size={18}/>{error}</div>}
    {loading?<div className="card empty-state">Loading your health dashboard...</div>:<>
      <div className="stats-grid">
        <StatCard title="Anemia Screening" value={report?.prediction||"No Report"} subtitle="Latest screening result" icon={<ShieldCheck size={20}/>} type={report?.prediction==="Anemia Detected"?"warning":"success"}/>
        <StatCard title="Risk Level" value={report?.risk_level||"—"} subtitle="Project screening category" icon={<Activity size={20}/>}/>
        <StatCard title="Saved Reports" value={data?.report_count??0} subtitle="All reports in your account" icon={<FileText size={20}/>} onClick={()=>navigate("/reports")}/>
        <StatCard title="Health Trends" value={recent.length?"Active":"Start"} subtitle="Track CBC changes" icon={<TrendingUp size={20}/>} onClick={()=>navigate("/trends")}/>
      </div>
      {report?<section className="card"><div className="section-heading"><div><h2>Latest CBC Summary</h2><p>Report #{report.id} · {new Date(report.created_at).toLocaleString()}</p></div><span className={`status-pill ${report.risk_level==="Low"?"green":"orange"}`}>{report.risk_level} Risk</span></div><div className="cbc-grid">{[["Hemoglobin",report.hemoglobin,"g/dL"],["RBC",report.rbc,"×10⁶/µL"],["Hematocrit",report.hematocrit,"%"],["WBC",report.wbc,"×10³/µL"],["Platelets",report.platelets,"×10³/µL"],["MCV",report.mcv,"fL"],["MCHC",report.mchc,"g/dL"],["MCH",report.mch,"pg"],["RDW",report.rdw,"%"]].map(([n,v,u])=><Metric key={n} name={n} value={v} unit={u}/>)}</div></section>:<section className="empty-card"><div className="empty-icon"><Activity size={30}/></div><h2>No blood report yet</h2><p>Enter your CBC values to generate your first screening report.</p><button className="primary-button" onClick={()=>navigate("/analyze")}>Analyze Blood Report</button></section>}
      <section className="card"><div className="section-heading"><div><h2>Recent Activity</h2><p>Your latest saved screening reports.</p></div><button className="text-button" onClick={()=>navigate("/reports")}>View all <ArrowRight size={16}/></button></div>{recent.length?<div className="activity-list">{recent.slice(0,5).map(r=><div className="activity-row" key={r.id}><div><strong>Report #{r.id}</strong><span>{new Date(r.created_at).toLocaleString()}</span></div><span className={`status-pill ${r.prediction==="Anemia Detected"?"orange":"green"}`}>{r.prediction}</span><span>{r.risk_level} risk</span></div>)}</div>:<p>No saved reports yet.</p>}</section>
    </>}
  </div></main><Chatbot/></div>;
}
function Metric({name,value,unit}){return <div className="metric"><span>{name}</span><strong>{value}</strong><small>{unit}</small></div>}
