import React from "react";

interface StatsGridProps {
  totalJobs: number;
  matchedCount: number;
  pendingCount: number;
  conversionRate: string;
}

export default function StatsGrid({ totalJobs, matchedCount, pendingCount, conversionRate }: StatsGridProps) {
  const stats = [
    { label: "Jobs Discovered", value: totalJobs.toString(), color: "bg-[#EEF2F6]" },
    { label: "Matches Found", value: matchedCount.toString(), color: "bg-[#EEF2F6]" },
    { label: "Awaiting Approval", value: pendingCount.toString(), color: "bg-[#FEF3C7]" },
    { label: "Interview Conversion", value: conversionRate, color: "bg-[#D1FAE5]" }
  ];

  return (
    <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {stats.map((stat, i) => (
        <div
          key={i}
          className={`p-6 border-4 border-black ${stat.color} shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] flex flex-col justify-between`}
        >
          <span className="text-sm font-bold text-gray-700 uppercase">{stat.label}</span>
          <span className="text-3xl font-black mt-2">{stat.value}</span>
        </div>
      ))}
    </section>
  );
}
