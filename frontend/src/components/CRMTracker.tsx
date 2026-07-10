import React from "react";

export default function CRMTracker() {
  const contacts = [
    {
      id: 1,
      name: "Harrison Chase",
      company: "LangChain",
      status: "Initial Outreach",
      lastContact: "2026-07-10",
      notes: "Sent LinkedIn note referencing their fastapi gateway repository contribution."
    },
    {
      id: 2,
      name: "Elwood",
      company: "Supabase",
      status: "Technical Assessment",
      lastContact: "2026-07-09",
      notes: "PostgreSQL pgvector clustering query optimization task."
    }
  ];

  return (
    <section className="bg-white border-4 border-black p-6 md:p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] flex-1">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b-4 border-black pb-6">
        <div>
          <h2 className="text-2xl font-black uppercase">Recruiter CRM Ledger</h2>
          <p className="text-sm font-semibold text-gray-600 mt-1">
            Track communication history and scheduling stages with talent acquisition partners.
          </p>
        </div>
        <button className="bg-black text-white font-extrabold px-6 py-3 border-2 border-black hover:translate-x-0.5 hover:translate-y-0.5 shadow-[4px_4px_0px_0px_rgba(79,70,229,1)] transition-all text-xs">
          ➕ Log New Interaction
        </button>
      </div>

      <div className="flex flex-col gap-6">
        {contacts.map((contact) => (
          <div
            key={contact.id}
            className="p-6 border-4 border-black bg-[#FAF9F6] shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
          >
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-lg font-black">{contact.name}</h3>
                <span className="text-xs font-bold text-gray-500">{contact.company}</span>
              </div>
              <span className="bg-[#4F46E5] text-white text-xs font-black uppercase px-2.5 py-1 border-2 border-black shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
                {contact.status}
              </span>
            </div>
            <div className="mt-4 text-xs font-bold text-gray-600 border-t border-black pt-4">
              <span className="block text-gray-400 mb-1">NOTES</span>
              {contact.notes}
            </div>
            <div className="mt-3 text-[10px] font-black text-gray-400">
              LAST CORRESPONDENCE: {contact.lastContact}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
