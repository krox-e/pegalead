"use client";

import { motion } from "framer-motion";
import { Sparkles, Eye, Radio, Flame } from "lucide-react";

export const OurStory = () => {
  const pillars = [
    {
      icon: Eye,
      title: "Optical Experimentation",
      description:
        "Pushing the boundaries of 16mm/35mm photochemical emulsions combined with real-time generative light manipulation.",
    },
    {
      icon: Radio,
      title: "Foley & Granular Sound",
      description:
        "Building acoustic worlds through modular synthesis, tactile foley, and microtonal spatial audio environments.",
    },
    {
      icon: Flame,
      title: "Radical Storytelling",
      description:
        "Dismantling conventional narrative arcs in favor of sensorial rhythms, poetic pacing, and uninhibited emotional resonance.",
    },
  ];

  const stats = [
    { value: "48+", label: "Global Film Screenings" },
    { value: "14", label: "International Fellowships" },
    { value: "3.2M", label: "Audiovisual Streams" },
    { value: "100%", label: "Creative Autonomy" },
  ];

  return (
    <section id="story" className="w-full px-4 py-24 sm:px-6 md:px-12 lg:px-20 max-w-7xl mx-auto">
      {/* Editorial Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-12 border-b border-white/10">
        <div>
          <span className="inline-flex items-center gap-2 text-xs uppercase tracking-widest text-[#E1E0CC]/60 font-mono mb-3">
            <Sparkles className="w-3.5 h-3.5 text-[#E1E0CC]" />
            Manifesto / 01
          </span>
          <h2 className="text-3xl sm:text-4xl md:text-6xl font-bold tracking-tight text-[#E1E0CC] font-['Syne']">
            Light bends. <br />
            Stories refract.
          </h2>
        </div>
        <p className="max-w-md text-sm sm:text-base text-[#E1E0CC]/70 font-light leading-relaxed">
          Prisma is an independent creative laboratory and collective founded in 2021.
          We gather cinematographers, sonic sculptors, and creative technologists to produce
          works that defy algorithms and celebrate analog friction.
        </p>
      </div>

      {/* Pillars Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 py-16">
        {pillars.map((pillar, idx) => {
          const Icon = pillar.icon;
          return (
            <motion.div
              key={pillar.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: idx * 0.15 }}
              className="p-8 rounded-2xl bg-white/[0.02] border border-white/10 hover:border-[#E1E0CC]/40 transition-all duration-300 group hover:-translate-y-1 backdrop-blur-sm"
            >
              <div className="w-12 h-12 rounded-xl bg-[#E1E0CC]/10 flex items-center justify-center text-[#E1E0CC] mb-6 group-hover:scale-110 transition-transform">
                <Icon className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-semibold text-[#E1E0CC] mb-3 font-['Syne']">
                {pillar.title}
              </h3>
              <p className="text-sm text-[#E1E0CC]/65 leading-relaxed font-light">
                {pillar.description}
              </p>
            </motion.div>
          );
        })}
      </div>

      {/* Stats Counter Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 p-8 rounded-2xl bg-gradient-to-r from-white/[0.03] via-white/[0.01] to-white/[0.03] border border-white/10">
        {stats.map((stat) => (
          <div key={stat.label} className="text-center md:text-left">
            <p className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-[#E1E0CC] font-['Syne'] tracking-tight">
              {stat.value}
            </p>
            <p className="text-xs uppercase tracking-wider text-[#E1E0CC]/60 font-mono mt-1">
              {stat.label}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
};
