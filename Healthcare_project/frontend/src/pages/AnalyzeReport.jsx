import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Activity, AlertTriangle, CheckCircle2 } from "lucide-react";
import API from "../api";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

const fields = [
  ["ward_number", "Ward Number", "identifier"],
  ["hemoglobin", "Hemoglobin", "g/dL"],
  ["rbc", "RBC Count", "×10⁶/µL"],
  ["hematocrit", "Hematocrit", "%"],
  ["wbc", "WBC Count", "×10³/µL"],
  ["platelets", "Platelets", "×10³/µL"],
  ["mcv", "MCV", "fL"],
  ["mchc", "MCHC", "g/dL"],
  ["mch", "MCH", "pg"],
  ["rdw", "RDW", "%"],
];

const initial = Object.fromEntries(fields.map(([key]) => [key, ""]));

export default function AnalyzeReport() {
  const navigate = useNavigate();
  const [form, setForm] = useState(initial);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyze = async (e) => {
    e.preventDefault(); setError(""); setResult(null);
    if (Object.values(form).some(v => v === "" || !Number.isFinite(Number(v)))) {
      setError("Please enter all 10 CBC parameters."); return;
    }
    const data = Object.fromEntries(fields.map(([key]) => [key, Number(form[key])]));
    try {
      setLoading(true);
      const { data: response } = await API.post("/predict", data);
      if (!response?.success) throw new Error(response?.message || "Prediction failed.");
      setResult(response);
    } catch (err) {
      if (err.response?.status === 401) {
        setError("Your login session has expired. Please log in again.");
        return;
      }
      setError(err.response?.data?.message || err.message || "Prediction failed. Please make sure the backend is running.");
    } finally { setLoading(false); }
  };

  const detected = result?.prediction_value === 1 || result?.prediction === "Anemia Detected";
  const probability = result?.probability == null ? null : Number(result.probability);

  return <div className="app-shell"><Sidebar/><main className="main"><Topbar/><div className="content">
    <div className="page-heading"><div><span className="eyebrow">AI-POWERED SCREENING</span><h1>Analyze Blood Report</h1><p>Enter the same 10 features used by your trained LightGBM model.</p></div></div>
    <form className="card" onSubmit={analyze}>
      <div className="section-heading"><div><h2>CBC Parameters</h2><p>Use values exactly as shown on the laboratory report.</p></div><div className="model-badge">LightGBM</div></div>
      <div className="form-grid">{fields.map(([name,label,unit])=><div className="field" key={name}><label htmlFor={name}>{label}<span>{unit}</span></label><input id={name} name={name} type="number" min="0" step="any" value={form[name]} onChange={e=>setForm(v=>({...v,[name]:e.target.value}))} placeholder="Enter value" required/></div>)}</div>
      {error&&<div className="error-box"><AlertTriangle size={18}/><span>{error}</span></div>}
      <button className="primary-button analyze-button" disabled={loading}><Activity size={18}/>{loading?"Analyzing...":"Run LightGBM Analysis"}</button>
    </form>

    {result&&<section className="result-section">
      <div className={`result-banner ${detected?"warning":"success"}`}><div className="result-icon">{detected?<AlertTriangle/>:<CheckCircle2/>}</div><div><span>SCREENING RESULT</span><h2>{result.diagnosis || result.prediction}</h2><p>Model probability: {probability==null?"N/A":`${(probability*100).toFixed(2)}%`}</p></div></div>
      <div className="result-grid">
        <div className="card"><h3>Risk Level</h3><div className="big-result">{result.risk_level}</div><p>Project screening category, not a clinical diagnosis.</p></div>
        <div className="card"><h3>Abnormal Parameters</h3>{result.abnormal_parameters?.length?<div className="tag-list">{result.abnormal_parameters.map(x=><span key={x}>{x}</span>)}</div>:<p className="normal-text">No configured abnormalities detected.</p>}</div>
        <div className="card"><h3>Medical Review</h3><p>{result.doctor_message}</p>{["High","Moderate"].includes(result.risk_level)&&<button type="button" className="secondary-button" onClick={()=>navigate("/recommendations")}>View Recommendations</button>}</div>
      </div>
      <div className="card"><h2>Screening Guidance</h2><ul className="recommendation-list">{(result.recommendations||[]).map((x,i)=><li key={i}>{x}</li>)}</ul></div>
      <div className="success-box"><strong>Report #{result.report_id}</strong> saved successfully. You can view it in <button type="button" className="text-button" onClick={()=>navigate("/reports")}>My Reports</button>.</div>
      <div className="medical-disclaimer"><strong>Important:</strong> This application provides project-level screening and educational information. It does not replace professional medical diagnosis.</div>
    </section>}
  </div></main></div>;
}
