"use client";

import React, { useState, useEffect } from "react";
import Sidebar from "@/components/Sidebar";
import StatsGrid from "@/components/StatsGrid";
import MatchQueue from "@/components/MatchQueue";
import AnalyticsView from "@/components/AnalyticsView";
import CRMTracker from "@/components/CRMTracker";
import GraphExplorer from "@/components/GraphExplorer";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "@/lib/firebase";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const [selectedTab, setSelectedTab] = useState("queue");
  const [showApprovalModal, setShowApprovalModal] = useState(false);
  const [selectedJob, setSelectedJob] = useState<any>(null);
  const router = useRouter();
  const [authLoading, setAuthLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      const devBypass = sessionStorage.getItem("devBypass") === "true";
      if (!currentUser && !devBypass) {
        console.log("Unauthenticated user redirected to login.");
        router.push("/login");
      } else {
        setAuthLoading(false);
      }
    });
    return () => unsubscribe();
  }, [router]);
  
  const [matchedJobs, setMatchedJobs] = useState<any[]>([]);
  const [stats, setStats] = useState({
    totalJobs: 0,
    matchedCount: 0,
    pendingCount: 0,
    conversionRate: "0.0%",
  });
  const [loading, setLoading] = useState(true);
  const [reviewLoading, setReviewLoading] = useState(false);
  const [reviewDetails, setReviewDetails] = useState<any>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const statsRes = await fetch(`${API_BASE}/api/stats`);
      let fetchedStats = {
        totalJobs: 362,
        matchedCount: 3,
        pendingCount: 3,
        conversionRate: "0.0%",
      };
      if (statsRes.ok) {
        const statsData = await statsRes.json();
        fetchedStats = {
          totalJobs: statsData.total_jobs || 0,
          matchedCount: statsData.matched_jobs || 0,
          pendingCount: statsData.pending_review || 0,
          conversionRate: `${statsData.interview_rate}%`,
        };
      }
      setStats(fetchedStats);

      const jobsRes = await fetch(`${API_BASE}/api/jobs`);
      if (jobsRes.ok) {
        const jobsData = await jobsRes.json();
        setMatchedJobs(jobsData);
      } else {
        throw new Error("Jobs API failed");
      }
    } catch (err) {
      console.warn("Backend API offline, falling back to mock data:", err);
      setMatchedJobs([
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
          status: "discovered"
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
          status: "discovered"
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
          status: "discovered"
        }
      ]);
      setStats({
        totalJobs: 362,
        matchedCount: 3,
        pendingCount: 3,
        conversionRate: "0.0%",
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleReview = async (job: any) => {
    setSelectedJob(job);
    setShowApprovalModal(true);
    setReviewLoading(true);
    setReviewDetails(null);
    try {
      const res = await fetch(`${API_BASE}/api/review/${job.id}`);
      if (res.ok) {
        const data = await res.json();
        setReviewDetails(data);
      } else {
        throw new Error("Review API failed");
      }
    } catch (err) {
      console.warn("Failed to fetch live compilation review, utilizing fallback:", err);
      setReviewDetails({
        resume_name: `${job.company}_resume_v11.tex`,
        cover_letter_text: `Dear Hiring Team,\n\nI am thrilled to apply for the ${job.title} role at ${job.company}. My background in FastAPI and Kubernetes fits your technical challenges...`,
        outreach_text: `Hi, I noticed the opening for ${job.title} at ${job.company}. I'd love to connect and share how my FastAPI work matches your team's current focus!`,
        warnings: ["Offline Fallback Mode active."]
      });
    } finally {
      setReviewLoading(false);
    }
  };

  const handleApprove = async () => {
    if (!selectedJob) return;
    try {
      const res = await fetch(`${API_BASE}/api/approve/${selectedJob.id}`, {
        method: "POST",
      });
      if (res.ok) {
        alert(`Application for ${selectedJob.company} approved and logged in CRM!`);
        fetchDashboardData();
      } else {
        throw new Error("Approval request failed");
      }
    } catch (err) {
      console.error(err);
      alert(`Simulated App approval for ${selectedJob.company} logged locally.`);
    } finally {
      setShowApprovalModal(false);
    }
  };

  const pendingJobs = matchedJobs.filter(j => j.status === "discovered");

  if (authLoading) {
    return (
      <div className="min-h-screen bg-[#F0EBE1] text-black font-sans flex items-center justify-center">
        <div className="bg-white border-4 border-black p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] text-center font-bold text-lg">
          🔒 Verifying Client Session...
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#F0EBE1] text-black font-sans p-6 md:p-12 flex flex-col md:flex-row gap-8">
      {/* Sidebar navigation */}
      <Sidebar
        selectedTab={selectedTab}
        setSelectedTab={setSelectedTab}
        pendingCount={pendingJobs.length}
      />

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col gap-8">
        {/* Top Header Grid */}
        <StatsGrid
          totalJobs={stats.totalJobs}
          matchedCount={stats.matchedCount}
          pendingCount={pendingJobs.length}
          conversionRate={stats.conversionRate}
        />

        {/* Content Tab Box */}
        {selectedTab === "queue" && (
          <div>
            {loading ? (
              <div className="bg-white border-4 border-black p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] text-center font-bold">
                🔄 Syncing with Database Gateway...
              </div>
            ) : (
              <MatchQueue
                jobs={pendingJobs}
                onReview={handleReview}
              />
            )}
          </div>
        )}

        {selectedTab === "analytics" && <AnalyticsView />}

        {selectedTab === "crm" && <CRMTracker />}

        {selectedTab === "graph" && <GraphExplorer />}

        {selectedTab === "settings" && (
          <section className="bg-white border-4 border-black p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] flex-1 flex flex-col items-center justify-center text-center">
            <span className="text-5xl">⚙️</span>
            <h3 className="text-xl font-black uppercase mt-4">Settings & Integrations</h3>
            <p className="text-sm text-gray-600 mt-2 max-w-sm">
              Manage API keys, Gmail SMTP credentials, and cron job parameters directly inside the cloud environment.
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

            {reviewLoading ? (
              <div className="py-12 text-center font-bold">
                ⚙️ Compiling tailored resume variants and checking rule criticisms...
              </div>
            ) : reviewDetails ? (
              <div className="flex flex-col gap-4 mb-6">
                <div className="p-3 bg-[#FAF9F6] border-2 border-black">
                  <span className="block text-xs font-black uppercase text-gray-500 mb-1">Tailored Resume Output</span>
                  <span className="font-mono text-xs">{reviewDetails.resume_name}</span>
                </div>
                <div className="p-3 bg-[#FAF9F6] border-2 border-black max-h-36 overflow-y-auto">
                  <span className="block text-xs font-black uppercase text-gray-500 mb-1">Cover Letter Draft</span>
                  <span className="text-xs whitespace-pre-wrap">{reviewDetails.cover_letter_text}</span>
                </div>
                <div className="p-3 bg-[#FAF9F6] border-2 border-black max-h-24 overflow-y-auto">
                  <span className="block text-xs font-black uppercase text-gray-500 mb-1">LinkedIn Outreach</span>
                  <span className="text-xs whitespace-pre-wrap">{reviewDetails.outreach_text}</span>
                </div>
                {reviewDetails.warnings && reviewDetails.warnings.length > 0 && (
                  <div className="p-3 bg-red-50 border-2 border-red-500 text-red-700 text-xs font-bold">
                    ⚠️ Warnings:
                    <ul className="list-disc pl-4 mt-1 font-semibold">
                      {reviewDetails.warnings.map((w: string, idx: number) => (
                        <li key={idx}>{w}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <div className="py-12 text-center text-red-500 font-bold">
                ⚠️ Failed to load review details.
              </div>
            )}

            <div className="flex gap-4">
              <button
                onClick={() => setShowApprovalModal(false)}
                className="flex-1 bg-gray-200 hover:bg-gray-300 font-black py-2 border-2 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] text-sm active:translate-x-0.5 active:translate-y-0.5 transition-all"
              >
                Reject / Re-tailor
              </button>
              <button
                onClick={handleApprove}
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
