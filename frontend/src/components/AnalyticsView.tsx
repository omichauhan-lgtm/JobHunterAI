import React from "react";

export default function AnalyticsView() {
  const funnelStages = [
    { label: "🔍 Discovered", count: 362, width: "w-full", color: "bg-[#4F46E5] text-white" },
    { label: "📄 Applied", count: 18, width: "w-3/4", color: "bg-black text-white" },
    { label: "⚙️ Assessments", count: 4, width: "w-1/2", color: "bg-yellow-400 text-black border-2 border-black" },
    { label: "📞 Interviews", count: 2, width: "w-1/3", color: "bg-blue-400 text-black border-2 border-black" },
    { label: "🏆 Offers", count: 0, width: "w-1/12", color: "bg-emerald-400 text-black border-2 border-black" },
  ];

  return (
    <section className="bg-white border-4 border-black p-6 md:p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] flex-1">
      <div className="border-b-4 border-black pb-6 mb-6">
        <h2 className="text-2xl font-black uppercase">Funnel Analytics</h2>
        <p className="text-sm font-semibold text-gray-600 mt-1">
          Conversion rates across the recruitment lifecycle stages.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Funnel chart */}
        <div className="flex flex-col gap-3">
          <h3 className="text-lg font-black uppercase mb-4">Pipeline Conversion</h3>
          {funnelStages.map((stage, idx) => (
            <div key={idx} className="flex items-center gap-4">
              <div className="w-28 text-xs font-black uppercase text-gray-600">{stage.label}</div>
              <div className="flex-1 bg-gray-100 border-2 border-black h-10 relative overflow-hidden">
                <div
                  className={`h-full ${stage.width} ${stage.color} flex items-center px-4 font-bold text-xs border-r-2 border-black transition-all`}
                >
                  {stage.count}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Stats card and resume metrics */}
        <div className="border-4 border-black p-6 bg-[#FAF9F6] shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
          <h3 className="text-lg font-black uppercase mb-4">Resume Efficiency</h3>
          <div className="flex flex-col gap-4">
            <div className="flex justify-between items-center border-b-2 border-black pb-2">
              <span className="text-xs font-black uppercase text-gray-500">Resume Variant</span>
              <span className="text-xs font-black uppercase text-gray-500">Applications</span>
            </div>
            <div className="flex justify-between items-center text-sm font-bold">
              <span>ai.tex (AI Systems)</span>
              <span>12</span>
            </div>
            <div className="flex justify-between items-center text-sm font-bold">
              <span>backend.tex (Backend/Docker)</span>
              <span>6</span>
            </div>
            <div className="flex justify-between items-center text-sm font-bold text-gray-400">
              <span>frontend.tex (React/Next)</span>
              <span>0</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
