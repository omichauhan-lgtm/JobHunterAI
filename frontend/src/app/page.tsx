"use client";

import React, { useState } from "react";
import Sidebar from "@/components/Sidebar";
import StatsGrid from "@/components/StatsGrid";
import MatchQueue from "@/components/MatchQueue";

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

  const handleReview = (job: any) => {
    setSelectedJob(job);
    setShowApprovalModal(true);
  };

  return (
    <div className="min-h-screen bg-[#F0EBE1] text-black font-sans p-6 md:p-12 flex flex-col md:flex-row gap-8">
      {/* Sidebar navigation */}
      <Sidebar
        selectedTab={selectedTab}
        setSelectedTab={setSelectedTab}
        pendingCount={matchedJobs.length}
      />

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col gap-8">
        {/* Top Header Grid */}
        <StatsGrid
          totalJobs={362}
          matchedCount={3}
          pendingCount={matchedJobs.length}
          conversionRate="0.0%"
        />

        {/* Content Tab Box */}
        {selectedTab === "queue" && (
          <MatchQueue
            jobs={matchedJobs}
            onReview={handleReview}
          />
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
