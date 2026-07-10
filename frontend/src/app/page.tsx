"use client";

import React from "react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#F0EBE1] text-black font-sans flex flex-col justify-between selection:bg-[#4F46E5] selection:text-white">
      {/* Navbar */}
      <header className="border-b-4 border-black bg-white py-4 px-6 md:px-12 flex justify-between items-center sticky top-0 z-40">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🤖</span>
          <span className="text-xl font-black uppercase tracking-wider">JobHunterAI</span>
        </div>
        <Link
          href="/dashboard"
          className="bg-black text-white font-black px-6 py-2 border-2 border-black hover:translate-x-0.5 hover:translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0px_0px_rgba(79,70,229,1)] transition-all text-sm"
        >
          Open App 🚀
        </Link>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-6 md:px-12 max-w-5xl mx-auto text-center flex flex-col items-center">
        <span className="bg-yellow-300 text-xs font-black uppercase px-3 py-1 border-2 border-black shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] mb-6">
          V11 Cloud-Native Release
        </span>
        <h1 className="text-4xl md:text-6xl font-black tracking-tight uppercase leading-none max-w-4xl">
          Autonomously Land Your Next <span className="text-[#4F46E5]">Remote Engineering</span> Role
        </h1>
        <p className="text-lg md:text-xl font-bold text-gray-700 mt-6 max-w-2xl leading-relaxed">
          JobHunterAI runs 24/7 in the cloud. It discovers high-fit remote positions, tailors evidence-grounded resumes, and delivers a spreadsheet report directly to your Gmail inbox every morning.
        </p>
        
        {/* Claymorphic Button */}
        <Link
          href="/dashboard"
          className="mt-10 bg-[#4F46E5] text-white font-black text-lg px-8 py-4 border-4 border-black rounded-full shadow-[inset_0_4px_4px_rgba(255,255,255,0.4),_6px_6px_0px_0px_rgba(0,0,0,1)] active:translate-x-[2px] active:translate-y-[2px] hover:bg-[#4338CA] transition-all"
        >
          Get Started &bull; Launch Dashboard
        </Link>
      </section>

      {/* Product Comparisons: The Problem */}
      <section className="bg-white border-y-4 border-black py-16 px-6 md:px-12">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-black text-center uppercase mb-12">The Job Hunting Problem</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 border-4 border-black bg-[#FAF9F6] shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
              <span className="text-3xl">🐌</span>
              <h3 className="text-xl font-black uppercase mt-4">Manual Tailoring</h3>
              <p className="text-sm font-semibold text-gray-600 mt-2 leading-relaxed">
                Adapting cover letters and bullets manually for dozens of positions is slow, exhausting, and prone to fatigue.
              </p>
            </div>
            <div className="p-6 border-4 border-black bg-[#FAF9F6] shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
              <span className="text-3xl">⚠️</span>
              <h3 className="text-xl font-black uppercase mt-4">Auto-Apply Bots</h3>
              <p className="text-sm font-semibold text-gray-600 mt-2 leading-relaxed">
                Spamming generic applications without tailoring gets your resume immediately filtered by ATS systems or ignored by recruiters.
              </p>
            </div>
            <div className="p-6 border-4 border-black bg-[#D1FAE5] shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]">
              <span className="text-3xl">🌟</span>
              <h3 className="text-xl font-black uppercase mt-4 text-emerald-950">JobHunterAI Platform</h3>
              <p className="text-sm font-bold text-emerald-900 mt-2 leading-relaxed">
                Programmatic ATS matching, evidence-backed bullet point verification, and human-in-the-loop approval before anything is sent.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-16 px-6 md:px-12 max-w-5xl mx-auto w-full">
        <h2 className="text-3xl font-black text-center uppercase mb-12">How it works</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            { step: "01", title: "Continuous Scan", desc: "Background cloud workers scrape remote portals for matching profiles." },
            { step: "02", title: "Evidence Scoring", desc: "Scores are computed using career knowledge graph and skill datasets." },
            { step: "03", title: "Compile Package", desc: "Generates grounded LaTeX resumes, cover letters, and outreach files." },
            { step: "04", title: "Inbox Briefing", desc: "A spreadsheet listing and HTML report arrives in your email at 08:00 AM." }
          ].map((item, index) => (
            <div key={index} className="bg-white border-4 border-black p-6 shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
              <span className="text-2xl font-black text-[#4F46E5] block mb-2">{item.step}</span>
              <h4 className="text-lg font-black uppercase mb-1">{item.title}</h4>
              <p className="text-xs font-semibold text-gray-600 leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Pricing Section (Beta Special) */}
      <section className="bg-white border-t-4 border-black py-16 px-6 md:px-12 text-center">
        <div className="max-w-xl mx-auto border-4 border-black p-8 bg-[#FAF9F6] shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
          <h3 className="text-2xl font-black uppercase">Candidate Beta Program</h3>
          <p className="text-sm font-bold text-gray-600 mt-2">
            Free high-precision tracking for remote software & AI engineers.
          </p>
          <div className="text-5xl font-black my-6">$0</div>
          <Link
            href="/dashboard"
            className="block bg-black text-white font-black py-3 border-2 border-black hover:translate-x-0.5 hover:translate-y-0.5 active:translate-x-1 active:translate-y-1 shadow-[4px_4px_0px_0px_rgba(79,70,229,1)] transition-all text-sm uppercase"
          >
            Launch Free Account
          </Link>
        </div>
      </section>

      {/* FAQ Accordion */}
      <section className="py-16 px-6 md:px-12 max-w-4xl mx-auto w-full">
        <h2 className="text-3xl font-black text-center uppercase mb-12">Frequently Asked Questions</h2>
        <div className="flex flex-col gap-4">
          {[
            {
              q: "Is this an auto-apply bot?",
              a: "Absolutely not. JobHunterAI does all the discovery, scoring, and tailoring in the background, but human-in-the-loop approval is strictly required before any application is sent out."
            },
            {
              q: "How does the platform guarantee resume truthfulness?",
              a: "We model your credentials as a relational Knowledge Graph. Every bullet point compiled into your resume must trace back to concrete evidence tags (such as pull request numbers or commit IDs) logged in the database."
            },
            {
              q: "Does this require my laptop to be on?",
              a: "No. Because it runs cloud services, background discovery workers, databases, and cron schedulers operate 24/7. Your daily brief and matching spreadsheet arrive in your inbox even when your PC is offline."
            }
          ].map((faq, index) => (
            <div key={index} className="bg-white border-2 border-black p-6 shadow-[3px_3px_0px_0px_rgba(0,0,0,1)]">
              <h4 className="text-md font-black uppercase">{faq.q}</h4>
              <p className="text-sm font-semibold text-gray-600 mt-2 leading-relaxed">{faq.a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t-4 border-black bg-white py-8 px-6 text-center text-xs font-bold text-gray-600">
        &copy; {new Date().getFullYear()} JobHunterAI. All rights reserved. Deployed Cloud-Native.
      </footer>
    </div>
  );
}
