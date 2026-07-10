import React from "react";

export default function GraphExplorer() {
  const experiences = [
    {
      role: "BI Analytics Intern",
      company: "Rajputana Vehicles",
      bullets: [
        { text: "Optimized dashboard queries via PostgreSQL indexes.", evidence: "PR #205" }
      ]
    },
    {
      role: "Open Source Contributor",
      company: "ADEN Gateway",
      bullets: [
        { text: "Implemented secure OAuth2 authorization handlers.", evidence: "PR #12" }
      ]
    }
  ];

  return (
    <section className="bg-white border-4 border-black p-6 md:p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] flex-1">
      <div className="border-b-4 border-black pb-6 mb-6">
        <h2 className="text-2xl font-black uppercase">Knowledge Graph Explorer</h2>
        <p className="text-sm font-semibold text-gray-600 mt-1">
          Visualizing grounded credentials, project bullets, and verified code verification logs.
        </p>
      </div>

      <div className="flex flex-col gap-6">
        {experiences.map((exp, idx) => (
          <div key={idx} className="p-6 border-4 border-black bg-[#FAF9F6] shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
            <h3 className="text-lg font-black uppercase">{exp.role}</h3>
            <span className="text-xs font-bold text-[#4F46E5]">{exp.company}</span>
            <div className="mt-4 flex flex-col gap-3">
              {exp.bullets.map((bullet, i) => (
                <div key={i} className="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 bg-white p-3 border-2 border-black">
                  <span className="text-xs font-semibold text-gray-700">{bullet.text}</span>
                  <span className="bg-yellow-300 text-[10px] font-black uppercase px-2 py-0.5 border border-black shadow-[1px_1px_0px_0px_rgba(0,0,0,1)]">
                    🔑 {bullet.evidence}
                  </span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
