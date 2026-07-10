import React from "react";
import { signOut } from "firebase/auth";
import { auth } from "@/lib/firebase";
import { useRouter } from "next/navigation";

interface SidebarProps {
  selectedTab: string;
  setSelectedTab: (tab: string) => void;
  pendingCount: number;
}

export default function Sidebar({ selectedTab, setSelectedTab, pendingCount }: SidebarProps) {
  const router = useRouter();
  
  const tabs = [
    { id: "queue", label: "📋 Match Queue", count: pendingCount },
    { id: "analytics", label: "📊 Analytics", count: 0 },
    { id: "crm", label: "✉️ Recruiter CRM", count: 0 },
    { id: "graph", label: "🕸️ Knowledge Graph", count: 0 },
    { id: "settings", label: "⚙️ Settings", count: 0 }
  ];

  const handleSignOut = async () => {
    try {
      await signOut(auth);
      router.push("/login");
    } catch (err) {
      console.warn("Firebase sign out failed, routing to login directly:", err);
      // Ensure development mode bypass fallback
      router.push("/login");
    }
  };

  return (
    <aside className="w-full md:w-80 bg-white border-4 border-black p-6 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] flex flex-col justify-between">
      <div>
        <div className="flex items-center gap-3 mb-8">
          <span className="text-3xl">🤖</span>
          <h1 className="text-2xl font-black tracking-tight uppercase">JobHunterAI</h1>
        </div>
        <nav className="flex flex-col gap-3">
          {tabs.map((tab) => (
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
              {tab.count > 0 && (
                <span className="bg-red-500 text-white text-xs px-2 py-0.5 rounded-full font-black">
                  {tab.count}
                </span>
              )}
            </button>
          ))}
        </nav>
        
        <button
          onClick={handleSignOut}
          className="mt-6 flex items-center justify-center gap-2 w-full p-2.5 font-bold border-2 border-black text-red-600 bg-red-50 hover:bg-red-100 shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] active:translate-x-[1px] active:translate-y-[1px] active:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all text-xs uppercase"
        >
          🚪 Sign Out
        </button>
      </div>
      <div className="mt-8 pt-6 border-t-2 border-black text-xs font-semibold text-gray-600">
        V11 Cloud Active &bull; omichauhan427@gmail.com
      </div>
    </aside>
  );
}
