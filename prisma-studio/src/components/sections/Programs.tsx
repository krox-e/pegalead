"use client";

import { motion } from "framer-motion";
import { Compass, Sparkles, Check, ArrowRight } from "lucide-react";

export const Programs = () => {
  const programs = [
    {
      title: "Autumn Darkroom Residency",
      term: "Sept – Nov 2026",
      location: "Kyoto / Tokyo",
      stipend: "$8,500 + Full Lab & Camera Access",
      highlights: [
        "Dedicated photochemical wet-lab and 35mm scanner access",
        "Round-trip travel and studio living quarters covered",
        "Solo exhibition at Prisma Tokyo Gallery in December",
      ],
      deadline: "Applications close August 30",
    },
    {
      title: "Emerging Director Fellowship",
      term: "12-Month Cohort",
      location: "Global / Hybrid",
      stipend: "$25,000 Production Grant",
      highlights: [
        "One-on-one mentorship with Cannes & Sundance selected directors",
        "Access to Prisma's cinema camera package (Arri Alexa 35 & anamorphic glass)",
        "Guaranteed festival submission and premiere packaging strategy",
      ],
      deadline: "Applications open for 2027",
    },
    {
      title: "Sonic & Generative Media Fellowship",
      term: "Spring 2027",
      location: "Berlin Lab",
      stipend: "$10,000 + Modular Synth Archive",
      highlights: [
        "Unrestricted access to 24-channel spatial sound dome",
        "Collaboration with Prisma's GLSL and creative coding team",
        "Live performance residency at CTM / Transmediale partner venues",
      ],
      deadline: "Applications close October 15",
    },
  ];

  return (
    <section id="programs" className="w-full px-4 py-24 sm:px-6 md:px-12 lg:px-20 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-8 border-b border-white/10">
        <div>
          <span className="inline-flex items-center gap-2 text-xs uppercase tracking-widest text-[#E1E0CC]/60 font-mono mb-3">
            <Compass className="w-3.5 h-3.5 text-[#E1E0CC]" />
            Residencies & Fellowships / 04
          </span>
          <h2 className="text-3xl sm:text-4xl md:text-6xl font-bold tracking-tight text-[#E1E0CC] font-['Syne']">
            Programs & Support
          </h2>
        </div>
        <p className="max-w-md text-sm sm:text-base text-[#E1E0CC]/70 font-light leading-relaxed">
          We reinvest 100% of commercial revenue into non-profit creative fellowships,
          grants, and physical lab spaces for visionary creators.
        </p>
      </div>

      {/* Program Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 pt-12">
        {programs.map((prog, idx) => (
          <motion.div
            key={prog.title}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: idx * 0.15 }}
            className="p-8 rounded-3xl bg-gradient-to-b from-white/[0.04] to-white/[0.01] border border-white/10 hover:border-[#E1E0CC]/50 transition-all duration-300 flex flex-col justify-between group"
          >
            <div>
              <div className="flex items-center justify-between text-xs font-mono text-[#E1E0CC]/60 mb-3">
                <span>{prog.term}</span>
                <span className="text-[#E1E0CC]">{prog.location}</span>
              </div>

              <h3 className="text-2xl font-bold text-[#E1E0CC] font-['Syne'] mb-2 group-hover:text-white">
                {prog.title}
              </h3>

              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono bg-[#E1E0CC]/10 text-[#E1E0CC] border border-[#E1E0CC]/20 mb-6">
                <Sparkles className="w-3.5 h-3.5" />
                <span>{prog.stipend}</span>
              </div>

              <div className="space-y-3 pt-4 border-t border-white/10 mb-8">
                {prog.highlights.map((item) => (
                  <div key={item} className="flex items-start gap-3 text-xs sm:text-sm text-[#E1E0CC]/75 font-light">
                    <Check className="w-4 h-4 text-[#E1E0CC] shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="pt-6 border-t border-white/5 flex items-center justify-between">
              <span className="text-xs font-mono text-[#E1E0CC]/50">
                {prog.deadline}
              </span>
              <a
                href="#inquiries"
                className="inline-flex items-center gap-2 text-xs sm:text-sm font-semibold text-[#E1E0CC] hover:text-white group/btn"
              >
                <span>Apply</span>
                <ArrowRight className="w-4 h-4 group-hover/btn:translate-x-1 transition-transform" />
              </a>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
};
