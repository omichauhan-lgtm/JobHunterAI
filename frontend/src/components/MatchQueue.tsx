import React from "react";

interface Job {
  id: number;
  company: string;
  title: string;
  score: number;
  salary: string;
  remote: string;
  template: string;
  source: string;
  link: string;
  status: string;
}

interface MatchQueueProps {
  jobs: Job[];
  onReview: (job: Job) => void;
}

export default function MatchQueue({ jobs, onReview }: MatchQueueProps) {
  return (
    <section className="bg-white border-4 border-black p-6 md:p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] flex-1">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b-4 border-black pb-6">
        <div>
          <h2 className="text-2xl font-black uppercase">Actionable Match Queue</h2>
          <p className="text-sm font-semibold text-gray-600 mt-1">
            Tailored packages compiled by background cloud workers. Awaiting final review.
          </p>
        </div>
        <button className="bg-[#4F46E5] text-white font-extrabold px-6 py-3 border-4 border-black rounded-full shadow-[inset_0_4px_4px_rgba(255,255,255,0.4),_4px_4px_0px_0px_rgba(0,0,0,1)] active:translate-x-[2px] active:translate-y-[2px] hover:bg-[#4338CA] transition-all">
          ⚡ Trigger Discovery Run
        </button>
      </div>

      <div className="flex flex-col gap-6">
        {jobs.map((job) => (
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
                onClick={() => onReview(job)}
                className="flex-1 md:flex-initial bg-[#10B981] hover:bg-[#059669] text-white font-black px-4 py-2 border-2 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] active:translate-x-0.5 active:translate-y-0.5 transition-all text-xs"
              >
                📋 Review & Approve
              </button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
