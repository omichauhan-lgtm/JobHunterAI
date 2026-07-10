"use client";

import React, { useState } from "react";

export default function Home() {
  const [selectedTab, setSelectedTab] = useState("queue");
  const [showApprovalModal, setShowApprovalModal] = useState(false);
  const [selectedJob, setSelectedJob] = useState<any>(null);

  const matchedJobs = [
    {
      id: 1,
      company: "LangChain",
      title: "AI Integration Engineer",
      score: 90,
      salary: "$140,000 - $180,000",
      remote: "Remote",
      template: "ai.tex",
      source: "Lever",
      link: "https://boards.lever.co/langchain/ai-engineer",
      status: "Awaiting Approval"
    },
    {
      id: 2,
      company: "LiteLLM",
      title: "Founding AI Platform Engineer",
      score: 80,
      salary: "$120,000 - $160,000",
      remote: "Remote",
      template: "backend.tex",
      source: "YC Jobs",
      link: "https://www.workatastartup.com/companies/litellm/jobs",
      status: "Awaiting Approval"
    },
    {
      id: 3,
      company: "Supabase",
      title: "Backend Systems Engineer",
      score: 80,
      salary: "$130,000 - $170,000",
      remote: "Remote",
      template: "backend.tex",
      source: "Greenhouse",
      link: "https://boards.greenhouse.io/supabase/backend-engineer",
      status: "Awaiting Approval"
    }
  ];

  return (
    <div className="min-h-screen bg-[#F0EBE1] text-black font-sans p-6 md:p-12 flex flex-col md:flex-row gap-8">
      {/* Sidebar: Brutalist Border + Shadow */}
      <aside className="w-full md:w-80 bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] flex flex-col justify-between">
        <div>
          <div className="flex items-center gap-3 mb-8">
            <span className="text-3xl">🤖</span>
            <h1 className="text-2xl font-black tracking-tight uppercase">JobHunterAI</h1>
          </div>
          <nav className="flex flex-col gap-3">
            {[
              { id: "queue", label: "📋 Match Queue", count: 3 },
              { id: "analytics", label: "📊 Analytics", count: null },
              { id: "crm", label: "✉️ Recruiter CRM", count: null },
              { id: "graph", label: "🕸️ Knowledge Graph", count: null },
              { id: "settings", label: "⚙️ Settings", count: null }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setSelectedTab(tab.id)}
                className={`flex items-center justify-between w-full p-3 font-bold border-2 border-black text-left transition-all ${
                  selectedTab === tab.id
                    ? "bg-[#4F46E5] text-white translate-x-[2px] translate-y-[2px] shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
                    : "bg-[#EEF2F6] hover:bg-[#E2E8F0] shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
                }`}
              >
                <span>{tab.label}</span>
                {tab.count !== null && (
                  <span className="bg-red-500 text-white text-xs px-2 py-0.5 rounded-full font-black">
                    {tab.count}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>
        <div className="mt-8 pt-6 border-t-2 border-black text-xs font-semibold text-gray-600">
          V11 Cloud Active &bull; omichauhan427@gmail.com
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col gap-8">
        {/* Top Header Grid with Claymorphic Accents */}
        <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Jobs Discovered", value: "362", color: "bg-[#EEF2F6]" },
            { label: "Matches Found", value: "3", color: "bg-[#EEF2F6]" },
            { label: "Awaiting Approval", value: "3", color: "bg-[#FEF3C7]" },
            { label: "Interview Conversion", value: "0.0%", color: "bg-[#D1FAE5]" }
          ].map((stat, i) => (
            <div
              key={i}
              className={`p-6 border-4 border-black ${stat.color} shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] flex flex-col justify-between`}
            >
              <span className="text-sm font-bold text-gray-700 uppercase">{stat.label}</span>
              <span className="text-3xl font-black mt-2">{stat.value}</span>
            </div>
          ))}
        </section>

        {/* Content Tab Box */}
        {selectedTab === "queue" && (
          <section className="bg-white border-4 border-black p-6 md:p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] flex-1">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b-4 border-black pb-6">
              <div>
                <h2 className="text-2xl font-black uppercase">Actionable Match Queue</h2>
                <p className="text-sm font-semibold text-gray-600 mt-1">
                  Tailored packages compiled by background cloud workers. Awaiting final review.
                </p>
              </div>
              {/* Claymorphic Button */}
              <button className="bg-[#4F46E5] text-white font-extrabold px-6 py-3 border-4 border-black rounded-full shadow-[inset_0_4px_4px_rgba(255,255,255,0.4),_4px_4px_0px_0px_rgba(0,0,0,1)] active:translate-x-[2px] active:translate-y-[2px] hover:bg-[#4338CA] transition-all">
                ⚡ Trigger Discovery Run
              </button>
            </div>

            <div className="flex flex-col gap-6">
              {matchedJobs.map((job) => (
                <div
                  key={job.id}
                  className="p-6 border-4 border-black bg-[#FAF9F6] shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] transition-all flex flex-col md:flex-row justify-between items-start md:items-center gap-4"
                >
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="bg-yellow-400 text-xs font-black uppercase px-2 py-0.5 border-2 border-black shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
                        Fit Score: {job.score}%
                      </span>
                      <span className="text-sm font-bold text-gray-500">Source: {job.source}</span>
                    </div>
                    <h3 className="text-xl font-black mt-2">
                      {job.title} at <span className="text-[#4F46E5]">{job.company}</span>
                    </h3>
                    <div className="flex flex-wrap gap-4 text-xs font-bold text-gray-600 mt-2">
                      <span>💰 {job.salary}</span>
                      <span>🌍 {job.remote}</span>
                      <span>📄 Template: {job.template}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 w-full md:w-auto">
                    <a
                      href={job.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 md:flex-initial text-center bg-[#EEF2F6] hover:bg-[#E2E8F0] font-black px-4 py-2 border-2 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] active:translate-x-0.5 active:translate-y-0.5 transition-all text-xs"
                    >
                      🔗 Direct Link
                    </a>
                    <button
                      onClick={() => {
                        setSelectedJob(job);
                        setShowApprovalModal(true);
                      }}
                      className="flex-1 md:flex-initial bg-[#10B981] hover:bg-[#059669] text-white font-black px-4 py-2 border-2 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] active:translate-x-0.5 active:translate-y-0.5 transition-all text-xs"
                    >
                      📋 Review & Approve
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {selectedTab !== "queue" && (
          <section className="bg-white border-4 border-black p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] flex-1 flex flex-col items-center justify-center text-center">
            <span className="text-5xl">🚧</span>
            <h3 className="text-xl font-black uppercase mt-4">Module under active construction</h3>
            <p className="text-sm text-gray-600 mt-2 max-w-sm">
              The presentation pages are being integrated into Next.js. Expose existing APIs to render this data.
            </p>
          </section>
        )}
      </main>

      {/* Brutalist Modal */}
      {showApprovalModal && selectedJob && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white border-4 border-black p-6 md:p-8 max-w-lg w-full shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] relative">
            <button
              onClick={() => setShowApprovalModal(false)}
              className="absolute top-4 right-4 bg-red-500 hover:bg-red-600 text-white font-black w-8 h-8 rounded-full border-2 border-black flex items-center justify-center shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] text-sm"
            >
              ✕
            </button>
            <h3 className="text-xl font-black uppercase mb-2">Review Application Package</h3>
            <p className="text-sm text-gray-500 font-bold mb-4">
              {selectedJob.title} — {selectedJob.company}
            </p>
            <div className="flex flex-col gap-4 mb-6">
              <div className="p-3 bg-[#FAF9F6] border-2 border-black">
                <span className="block text-xs font-black uppercase text-gray-500 mb-1">Tailored Resume Output</span>
                <span className="font-mono text-xs">{selectedJob.company}_resume_v11.tex</span>
              </div>
              <div className="p-3 bg-[#FAF9F6] border-2 border-black">
                <span className="block text-xs font-black uppercase text-gray-500 mb-1">Cover Letter Draft</span>
                <span className="font-mono text-xs">{selectedJob.company}_cover_letter.md</span>
              </div>
              <div className="p-3 bg-[#FAF9F6] border-2 border-black">
                <span className="block text-xs font-black uppercase text-gray-500 mb-1">LinkedIn Outreach</span>
                <span className="font-mono text-xs">{selectedJob.company}_outreach.txt</span>
              </div>
            </div>
            <div className="flex gap-4">
              <button
                onClick={() => setShowApprovalModal(false)}
                className="flex-1 bg-gray-200 hover:bg-gray-300 font-black py-2 border-2 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] text-sm active:translate-x-0.5 active:translate-y-0.5 transition-all"
              >
                Reject / Re-tailor
              </button>
              <button
                onClick={() => {
                  alert("Application approved and logged in CRM!");
                  setShowApprovalModal(false);
                }}
                className="flex-1 bg-[#10B981] hover:bg-[#059669] text-white font-black py-2 border-2 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] text-sm active:translate-x-0.5 active:translate-y-0.5 transition-all"
              >
                Approve & Mark Applied
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
