"use client";
import { useState } from "react";

export default function Dashboard() {
  const [jdText, setJdText] = useState("");
  const [jobId, setJobId] = useState<string | null>(null);
  const [candidatesInput, setCandidatesInput] = useState("");
  const [rankings, setRankings] = useState<any[]>([]);
  const [weights, setWeights] = useState({ technical: 0.4, career: 0.2, behavior: 0.2, culture: 0.2, risk_penalty: 0.1 });

  const [status, setStatus] = useState("");

  const analyzeJD = async () => {
    setStatus("Analyzing Job Description (Engine 1)...");
    const res = await fetch("http://localhost:8000/job/analyze", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description: jdText })
    });
    const data = await res.json();
    setJobId(data.job_id);
    setStatus(`JD Analyzed! Job ID: ${data.job_id}`);
  };

  const analyzeCandidates = async () => {
    setStatus("Processing Candidates (Engines 2, 3, 4)...");
    let cands = [];
    try {
      cands = JSON.parse(candidatesInput);
    } catch(e) {
      alert("Invalid JSON for candidates"); return;
    }
    await fetch("http://localhost:8000/candidate/analyze", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ candidates: cands })
    });
    setStatus("Candidates processed and saved!");
  };

  const rankCandidates = async () => {
    if (!jobId) return;
    setStatus("Ranking Committee in session (Engines 5-9, 11, 12)...");
    const res = await fetch(`http://localhost:8000/rank/${jobId}`, { method: "POST" });
    const data = await res.json();
    setRankings(data.rankings);
    setStatus("Ranking Complete!");
  };

  const applyCounterfactual = async () => {
    if (!jobId) return;
    setStatus("Applying Counterfactual Weights (Engine 10)...");
    const res = await fetch("http://localhost:8000/rankings/re-rank", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_id: jobId, weights })
    });
    const data = await res.json();
    setRankings(data.rankings);
    setStatus("Re-Ranking Complete!");
  };

  const handleWeightChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setWeights({ ...weights, [e.target.name]: parseFloat(e.target.value) });
  };

  const exportCSV = () => {
    if (!rankings.length) return;
    let csv = "Name,Overall Score,Tech Fit,Behavior Fit,Missing Skills\n";
    rankings.forEach(r => {
      csv += `Cand_${r.candidate_id.substring(0,6)},${r.overall_score.toFixed(2)},${r.technical_fit.toFixed(2)},${r.behavior_fit.toFixed(2)},"${r.missing_skills.join(", ")}"\n`;
    });
    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.setAttribute("hidden", "");
    a.setAttribute("href", url);
    a.setAttribute("download", "hermes_rankings.csv");
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 p-8 font-sans">
      <header className="mb-8 border-b pb-4">
        <h1 className="text-3xl font-bold tracking-tight text-indigo-700">HERMES AI</h1>
        <p className="text-slate-500">Recruiter Decision Dashboard & AI Hiring Committee</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold mb-4">1. Job Intelligence</h2>
            <textarea className="w-full h-32 p-3 border rounded text-sm mb-2" placeholder="Paste Job Description here..." value={jdText} onChange={(e)=>setJdText(e.target.value)} />
            <button onClick={analyzeJD} className="w-full bg-indigo-600 text-white py-2 rounded font-medium hover:bg-indigo-700">Analyze JD</button>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold mb-4">2. Candidate Data</h2>
            <textarea className="w-full h-32 p-3 border rounded text-sm mb-2 font-mono" placeholder='[{"name": "Alice", "skills": ["Python", "Docker"]}]' value={candidatesInput} onChange={(e)=>setCandidatesInput(e.target.value)} />
            <button onClick={analyzeCandidates} className="w-full bg-indigo-600 text-white py-2 rounded font-medium hover:bg-indigo-700">Load Candidates</button>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
            <h2 className="text-xl font-semibold mb-4">3. The Committee</h2>
            <button onClick={rankCandidates} disabled={!jobId} className="w-full bg-emerald-600 text-white py-2 rounded font-medium hover:bg-emerald-700 disabled:opacity-50">Generate Rankings</button>
          </div>

          <div className="bg-slate-100 p-4 rounded text-sm text-slate-700 font-mono">Status: {status || "Idle"}</div>
        </div>

        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Counterfactual Strategist</h2>
              <button onClick={applyCounterfactual} className="bg-indigo-100 text-indigo-700 px-4 py-1 rounded text-sm font-medium hover:bg-indigo-200">Re-Rank</button>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              {Object.keys(weights).map((w) => (
                <div key={w}>
                  <label className="block text-slate-500 capitalize mb-1">{w.replace("_", " ")}</label>
                  <input type="number" step="0.1" name={w} value={(weights as any)[w]} onChange={handleWeightChange} className="w-full border p-1 rounded" />
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Ranked Shortlist</h2>
              <button onClick={exportCSV} className="text-sm border border-slate-300 px-3 py-1 rounded hover:bg-slate-50">Export CSV</button>
            </div>

            <div className="space-y-4">
              {rankings.length === 0 && <p className="text-slate-500 text-sm">No candidates ranked yet.</p>}
              {rankings.map((r, i) => (
                <div key={i} className="border border-slate-200 rounded p-4 flex flex-col md:flex-row gap-4">
                  <div className="flex-shrink-0 flex flex-col items-center justify-center w-20 bg-indigo-50 rounded p-2">
                    <span className="text-2xl font-bold text-indigo-700">{(r.overall_score * 100).toFixed(0)}</span>
                    <span className="text-xs text-indigo-500">Score</span>
                  </div>
                  <div className="flex-grow space-y-2">
                    <div className="flex justify-between">
                      <span className="font-semibold text-lg">Candidate {r.candidate_id.substring(0, 6)}</span>
                      <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded-full">Risk: {(r.risk_score * 100).toFixed(0)}</span>
                    </div>

                    <div className="text-sm grid grid-cols-2 gap-2 text-slate-600">
                      <div><span className="font-medium text-slate-900">Tech Fit:</span> {(r.technical_fit * 100).toFixed(0)}%</div>
                      <div><span className="font-medium text-slate-900">Behavior Fit:</span> {(r.behavior_fit * 100).toFixed(0)}%</div>
                    </div>

                    <div className="text-sm bg-slate-50 p-2 rounded">
                      <div className="text-emerald-700 font-medium mb-1">Strengths</div>
                      <ul className="list-disc pl-5 text-slate-600">{r.strengths.map((s: string, idx: number) => <li key={idx}>{s}</li>)}</ul>
                    </div>

                    {r.missing_skills.length > 0 && (
                      <div className="text-sm text-red-600">
                        <span className="font-medium">Missing:</span> {r.missing_skills.join(", ")}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
