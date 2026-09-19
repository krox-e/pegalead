"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Mail, Send, CheckCircle2, Sparkles } from "lucide-react";

export const Inquiries = () => {
  const [topic, setTopic] = useState<string>("Join the Lab");
  const [submitted, setSubmitted] = useState<boolean>(false);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    portfolio: "",
    message: "",
  });

  const topics = [
    "Join the Lab",
    "Commission Project",
    "Workshop Enrollment",
    "Fellowship Application",
    "Screenings & Press",
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name || !formData.email) return;
    setSubmitted(true);
  };

  return (
    <section id="inquiries" className="w-full px-4 py-24 sm:px-6 md:px-12 lg:px-20 max-w-7xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 p-8 sm:p-12 md:p-16 rounded-3xl bg-gradient-to-b from-white/[0.03] to-transparent border border-white/10 relative overflow-hidden">
        {/* Background ambient glow */}
        <div className="pointer-events-none absolute -top-40 -right-40 w-96 h-96 rounded-full bg-[#E1E0CC]/5 blur-3xl" />
        
        {/* Left Column: Information */}
        <div className="lg:col-span-5 flex flex-col justify-between">
          <div>
            <span className="inline-flex items-center gap-2 text-xs uppercase tracking-widest text-[#E1E0CC]/60 font-mono mb-3">
              <Mail className="w-3.5 h-3.5 text-[#E1E0CC]" />
              Inquiries & Submissions / 05
            </span>
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-tight text-[#E1E0CC] font-['Syne']">
              Let's create something tactile.
            </h2>
            <p className="mt-4 text-sm sm:text-base text-[#E1E0CC]/75 font-light leading-relaxed">
              Whether you are an independent director seeking lab residency, a festival programmer,
              or a brand looking for authentic cinematic direction, we'd love to hear from you.
            </p>
          </div>

          <div className="mt-12 space-y-6">
            <div className="text-xs font-mono text-[#E1E0CC]/60">
              <p className="uppercase tracking-widest text-[#E1E0CC]/40 mb-1">DIRECT INBOX</p>
              <p className="text-sm sm:text-base text-[#E1E0CC] font-sans">contact@prisma-collective.org</p>
            </div>
            <div className="text-xs font-mono text-[#E1E0CC]/60">
              <p className="uppercase tracking-widest text-[#E1E0CC]/40 mb-1">PHYSICAL STUDIOS</p>
              <p className="text-sm text-[#E1E0CC]/80">Tokyo · Shibuya 2-chome</p>
              <p className="text-sm text-[#E1E0CC]/80">Berlin · Kreuzberg Oranienstraße</p>
            </div>
          </div>
        </div>

        {/* Right Column: Form */}
        <div className="lg:col-span-7">
          {submitted ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="h-full min-h-[400px] flex flex-col items-center justify-center text-center p-8 rounded-2xl bg-white/[0.02] border border-[#E1E0CC]/30"
            >
              <div className="w-16 h-16 rounded-full bg-[#E1E0CC]/15 text-[#E1E0CC] flex items-center justify-center mb-4">
                <CheckCircle2 className="w-8 h-8" />
              </div>
              <h3 className="text-2xl font-bold text-[#E1E0CC] font-['Syne']">
                Inquiry Received
              </h3>
              <p className="max-w-md text-sm text-[#E1E0CC]/70 font-light mt-2">
                Thank you, {formData.name}. A Prisma lab curator will review your transmission and get in touch within 48 hours.
              </p>
              <button
                onClick={() => {
                  setSubmitted(false);
                  setFormData({ name: "", email: "", portfolio: "", message: "" });
                }}
                className="mt-6 px-6 py-2 rounded-full text-xs font-mono bg-white/10 text-[#E1E0CC] hover:bg-white/20 transition-colors cursor-pointer"
              >
                Send Another Transmission
              </button>
            </motion.div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Topic Pills */}
              <div>
                <label className="block text-xs uppercase tracking-wider text-[#E1E0CC]/60 font-mono mb-2">
                  Select Focus Area
                </label>
                <div className="flex flex-wrap gap-2">
                  {topics.map((t) => (
                    <button
                      type="button"
                      key={t}
                      onClick={() => setTopic(t)}
                      className={`px-3.5 py-1.5 rounded-full text-xs font-medium transition-all cursor-pointer ${
                        topic === t
                          ? "bg-[#E1E0CC] text-[#0A0A0A] font-semibold"
                          : "bg-white/[0.04] text-[#E1E0CC]/70 hover:bg-white/[0.08] hover:text-[#E1E0CC] border border-white/5"
                      }`}
                    >
                      {t}
                    </button>
                  ))}
                </div>
              </div>

              {/* Input Fields */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs uppercase tracking-wider text-[#E1E0CC]/60 font-mono mb-1.5">
                    Your Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder="Kenji Sato"
                    className="w-full px-4 py-3 rounded-xl bg-white/[0.03] border border-white/10 text-[#E1E0CC] placeholder:text-[#E1E0CC]/30 text-sm focus:outline-none focus:border-[#E1E0CC] transition-colors"
                  />
                </div>

                <div>
                  <label className="block text-xs uppercase tracking-wider text-[#E1E0CC]/60 font-mono mb-1.5">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    placeholder="kenji@studio.com"
                    className="w-full px-4 py-3 rounded-xl bg-white/[0.03] border border-white/10 text-[#E1E0CC] placeholder:text-[#E1E0CC]/30 text-sm focus:outline-none focus:border-[#E1E0CC] transition-colors"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs uppercase tracking-wider text-[#E1E0CC]/60 font-mono mb-1.5">
                  Portfolio / Reel / Website
                </label>
                <input
                  type="url"
                  value={formData.portfolio}
                  onChange={(e) => setFormData({ ...formData, portfolio: e.target.value })}
                  placeholder="https://vimeo.com/your-reel"
                  className="w-full px-4 py-3 rounded-xl bg-white/[0.03] border border-white/10 text-[#E1E0CC] placeholder:text-[#E1E0CC]/30 text-sm focus:outline-none focus:border-[#E1E0CC] transition-colors"
                />
              </div>

              <div>
                <label className="block text-xs uppercase tracking-wider text-[#E1E0CC]/60 font-mono mb-1.5">
                  Your Transmission & Context
                </label>
                <textarea
                  rows={4}
                  value={formData.message}
                  onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  placeholder="Tell us about the project, concept, technical scope, or why you want to join our residency..."
                  className="w-full px-4 py-3 rounded-xl bg-white/[0.03] border border-white/10 text-[#E1E0CC] placeholder:text-[#E1E0CC]/30 text-sm focus:outline-none focus:border-[#E1E0CC] transition-colors resize-none"
                />
              </div>

              <button
                type="submit"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-full bg-[#E1E0CC] text-[#0A0A0A] font-semibold text-sm hover:bg-white hover:scale-[1.02] transition-all duration-200 cursor-pointer shadow-xl"
              >
                <span>Transmit Inquiry</span>
                <Send className="w-4 h-4" />
              </button>
            </form>
          )}
        </div>
      </div>
    </section>
  );
};
