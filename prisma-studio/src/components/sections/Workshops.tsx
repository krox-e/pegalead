"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Calendar, MapPin, Users, CheckCircle2, ArrowUpRight } from "lucide-react";

interface Workshop {
  id: string;
  title: string;
  instructor: string;
  dates: string;
  location: string;
  format: "In-Person" | "Hybrid" | "Remote Lab";
  spotsRemaining: number;
  description: string;
}

export const Workshops = () => {
  const [registeredId, setRegisteredId] = useState<string | null>(null);

  const workshops: Workshop[] = [
    {
      id: "ws-1",
      title: "Sculpting Shadow: 35mm & Monochromatic Lighting",
      instructor: "Kenji Sato (Director of Photography)",
      dates: "October 14 – 18, 2026",
      location: "Tokyo Studio (Shibuya)",
      format: "In-Person",
      spotsRemaining: 4,
      description: "Hands-on studio masterclass utilizing Arriflex 35mm cameras, custom tungsten fresnels, and photochemical darkroom chemical pushes.",
    },
    {
      id: "ws-2",
      title: "Granular Soundscapes & Foley Synthesis",
      instructor: "Marcus Lindqvist (Sound Artist)",
      dates: "November 03 – 07, 2026",
      location: "Berlin (Kreuzberg Lab)",
      format: "Hybrid",
      spotsRemaining: 2,
      description: "Crafting atmospheric film textures from hydrophone field captures, Serge modular synthesizers, and spatial multichannel mixing.",
    },
    {
      id: "ws-3",
      title: "Generative Motion: TouchDesigner to Film Print",
      instructor: "Talia Ramos & Prisma Tech Lab",
      dates: "November 21 – 25, 2026",
      location: "London & Global Stream",
      format: "Remote Lab",
      spotsRemaining: 8,
      description: "Bridging algorithmic shaders and GLSL generative patterns with physical optical printers and photochemical emulsion exposure.",
    },
    {
      id: "ws-4",
      title: "Color Science & Photochemical Film Emulation",
      instructor: "Elena Vance (Senior Colorist)",
      dates: "December 05 – 09, 2026",
      location: "São Paulo (Vila Madalena)",
      format: "In-Person",
      spotsRemaining: 5,
      description: "Mathematical look design, spectral film stock profiling, halation curves, and non-destructive print transfer pipelines in DaVinci Resolve.",
    },
  ];

  return (
    <section id="workshops" className="w-full px-4 py-24 sm:px-6 md:px-12 lg:px-20 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-8 border-b border-white/10">
        <div>
          <span className="inline-flex items-center gap-2 text-xs uppercase tracking-widest text-[#E1E0CC]/60 font-mono mb-3">
            <Users className="w-3.5 h-3.5 text-[#E1E0CC]" />
            Education & Craft / 03
          </span>
          <h2 className="text-3xl sm:text-4xl md:text-6xl font-bold tracking-tight text-[#E1E0CC] font-['Syne']">
            Masterclasses & Labs
          </h2>
        </div>
        <p className="max-w-md text-sm sm:text-base text-[#E1E0CC]/70 font-light leading-relaxed">
          Intensive cohorts led by working filmmakers and audio engineers. Small groups,
          pure practice, and direct access to rare production gear.
        </p>
      </div>

      {/* Workshop List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-12">
        {workshops.map((ws, idx) => {
          const isRegistered = registeredId === ws.id;
          return (
            <motion.div
              key={ws.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: idx * 0.1 }}
              className="p-8 rounded-3xl bg-white/[0.02] border border-white/10 hover:border-[#E1E0CC]/40 transition-all duration-300 flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-4">
                  <span className="px-3 py-1 rounded-full text-xs font-mono bg-white/[0.06] text-[#E1E0CC] border border-white/10">
                    {ws.format}
                  </span>
                  <span className="text-xs font-mono text-amber-300 bg-amber-400/10 px-2.5 py-0.5 rounded-full">
                    {ws.spotsRemaining} spots left
                  </span>
                </div>

                <h3 className="text-xl sm:text-2xl font-bold text-[#E1E0CC] font-['Syne'] group-hover:text-white transition-colors">
                  {ws.title}
                </h3>
                <p className="text-xs text-[#E1E0CC]/60 font-mono mt-1 mb-4">
                  Led by {ws.instructor}
                </p>
                <p className="text-sm text-[#E1E0CC]/75 font-light leading-relaxed mb-6">
                  {ws.description}
                </p>
              </div>

              <div className="pt-6 border-t border-white/5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="space-y-1.5 text-xs text-[#E1E0CC]/70 font-mono">
                  <div className="flex items-center gap-2">
                    <Calendar className="w-3.5 h-3.5 text-[#E1E0CC]/50" />
                    <span>{ws.dates}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="w-3.5 h-3.5 text-[#E1E0CC]/50" />
                    <span>{ws.location}</span>
                  </div>
                </div>

                <button
                  onClick={() => setRegisteredId(ws.id)}
                  disabled={isRegistered}
                  className={`px-5 py-2.5 rounded-full text-xs sm:text-sm font-semibold transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer ${
                    isRegistered
                      ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                      : "bg-[#E1E0CC] text-[#0A0A0A] hover:bg-white hover:scale-105"
                  }`}
                >
                  {isRegistered ? (
                    <>
                      <CheckCircle2 className="w-4 h-4" />
                      RSVP Confirmed
                    </>
                  ) : (
                    <>
                      Apply for Seat
                      <ArrowUpRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              </div>
            </motion.div>
          );
        })}
      </div>
    </section>
  );
};
