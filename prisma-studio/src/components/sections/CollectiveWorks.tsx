"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Play, Film, Award, ExternalLink } from "lucide-react";

interface Project {
  id: string;
  title: string;
  category: "Film & Cinema" | "Spatial Audio" | "Generative AV" | "Music Video";
  director: string;
  year: string;
  duration: string;
  award?: string;
  image: string;
  description: string;
}

export const CollectiveWorks = () => {
  const [activeCategory, setActiveCategory] = useState<string>("All");
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  const categories = ["All", "Film & Cinema", "Spatial Audio", "Generative AV", "Music Video"];

  const projects: Project[] = [
    {
      id: "1",
      title: "Solstice in Monochrome",
      category: "Film & Cinema",
      director: "Elena Vance & Kenji Sato",
      year: "2025",
      duration: "18m 42s",
      award: "Vimeo Staff Pick · Best Experimental",
      image: "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=1200&q=80",
      description: "Shot on expired 35mm Kodak Double-X stock during the midnight sun in Svalbard, examining isolation through high-contrast chiaroscuro.",
    },
    {
      id: "2",
      title: "Aura // Resonator",
      category: "Spatial Audio",
      director: "Marcus Lindqvist",
      year: "2025",
      duration: "32m",
      award: "Cannes Lions Bronze (Sound Design)",
      image: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=1200&q=80",
      description: "An immersive 64-channel spatial sound dome experience sculpting sub-bass frequencies and granular water recordings.",
    },
    {
      id: "3",
      title: "Chromasphere 0.9",
      category: "Generative AV",
      director: "Talia Ramos",
      year: "2026",
      duration: "Live Performance",
      award: "Ars Electronica Honorary Mention",
      image: "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?auto=format&fit=crop&w=1200&q=80",
      description: "Custom TouchDesigner audio-reactive light architecture projecting optical prisms onto curved mist curtains.",
    },
    {
      id: "4",
      title: "Echoes of the Caldera",
      category: "Music Video",
      director: "Dmitri Volkov",
      year: "2026",
      duration: "4m 15s",
      award: "UKMVA Nominee 2026",
      image: "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1200&q=80",
      description: "A surreal, dreamscape audiovisual composition featuring volcanic ash choreography and live Buchla modular synthesis.",
    },
    {
      id: "5",
      title: "The Velocity of Stillness",
      category: "Film & Cinema",
      director: "Sora Takahashi",
      year: "2025",
      duration: "24m",
      award: "Rotterdam Film Festival Official Selection",
      image: "https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?auto=format&fit=crop&w=1200&q=80",
      description: "Exploring urban stillness at 4:00 AM across Tokyo, Seoul, and Taipei using custom anamorphic cine glass.",
    },
    {
      id: "6",
      title: "Bioluminescent Drift",
      category: "Generative AV",
      director: "Prisma Core Ensemble",
      year: "2026",
      duration: "Installation",
      award: "Sonar+D Featured Project",
      image: "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1200&q=80",
      description: "Simulating deep-sea hydrothermal organism luminescence through neural cellular automata and hydrophone field audio.",
    },
  ];

  const filteredProjects =
    activeCategory === "All"
      ? projects
      : projects.filter((p) => p.category === activeCategory);

  return (
    <section id="collective" className="w-full px-4 py-24 sm:px-6 md:px-12 lg:px-20 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-8 border-b border-white/10">
        <div>
          <span className="inline-flex items-center gap-2 text-xs uppercase tracking-widest text-[#E1E0CC]/60 font-mono mb-3">
            <Film className="w-3.5 h-3.5 text-[#E1E0CC]" />
            Selected Works / 02
          </span>
          <h2 className="text-3xl sm:text-4xl md:text-6xl font-bold tracking-tight text-[#E1E0CC] font-['Syne']">
            Collective Archive
          </h2>
        </div>
        <p className="max-w-md text-sm sm:text-base text-[#E1E0CC]/70 font-light leading-relaxed">
          Commissioned pieces, laboratory experiments, and award-winning festival selections
          crafted by Prisma resident artists and fellows.
        </p>
      </div>

      {/* Category Pills */}
      <div className="flex flex-wrap items-center gap-2 pt-8 pb-12">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-4 py-1.5 rounded-full text-xs sm:text-sm font-medium transition-all duration-200 cursor-pointer ${
              activeCategory === cat
                ? "bg-[#E1E0CC] text-[#0A0A0A] shadow-md"
                : "bg-white/[0.04] text-[#E1E0CC]/70 hover:bg-white/[0.1] hover:text-[#E1E0CC] border border-white/5"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Projects Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <AnimatePresence mode="popLayout">
          {filteredProjects.map((project) => (
            <motion.div
              layout
              key={project.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.4 }}
              onClick={() => setSelectedProject(project)}
              className="group cursor-pointer rounded-2xl overflow-hidden bg-white/[0.02] border border-white/10 hover:border-[#E1E0CC]/50 transition-all duration-300 flex flex-col"
            >
              {/* Media Thumbnail */}
              <div className="relative h-64 w-full overflow-hidden bg-black/40">
                <img
                  src={project.image}
                  alt={project.title}
                  className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105 filter brightness-90 group-hover:brightness-100"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/20" />
                
                {/* Play Button Overlay */}
                <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <div className="w-14 h-14 rounded-full bg-[#E1E0CC] text-[#0A0A0A] flex items-center justify-center shadow-xl transform group-hover:scale-110 transition-transform">
                    <Play className="w-6 h-6 fill-current translate-x-0.5" />
                  </div>
                </div>

                {/* Duration / Tag Badges */}
                <div className="absolute top-3 left-3 flex gap-2">
                  <span className="px-2.5 py-1 rounded-full text-[11px] font-mono bg-black/70 backdrop-blur-md text-[#E1E0CC] border border-white/10">
                    {project.duration}
                  </span>
                </div>

                {project.award && (
                  <div className="absolute bottom-3 left-3 right-3 flex items-center gap-1.5 text-[11px] font-mono text-[#E1E0CC]/90 bg-black/60 backdrop-blur-sm px-2.5 py-1 rounded-md border border-white/10">
                    <Award className="w-3.5 h-3.5 text-amber-300 shrink-0" />
                    <span className="truncate">{project.award}</span>
                  </div>
                )}
              </div>

              {/* Details */}
              <div className="p-6 flex-1 flex flex-col justify-between">
                <div>
                  <span className="text-xs uppercase tracking-wider text-[#E1E0CC]/50 font-mono">
                    {project.category} · {project.year}
                  </span>
                  <h3 className="text-xl font-bold text-[#E1E0CC] mt-1 group-hover:text-white transition-colors font-['Syne']">
                    {project.title}
                  </h3>
                  <p className="text-xs text-[#E1E0CC]/70 mt-2 font-light line-clamp-2">
                    {project.description}
                  </p>
                </div>
                <div className="mt-4 pt-4 border-t border-white/5 flex items-center justify-between text-xs text-[#E1E0CC]/60 font-mono">
                  <span>Dir. {project.director}</span>
                  <ExternalLink className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Project Detail Modal */}
      <AnimatePresence>
        {selectedProject && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="relative w-full max-w-2xl bg-[#0F0F0F] border border-white/15 rounded-3xl overflow-hidden shadow-2xl"
            >
              <div className="relative h-72 w-full">
                <img
                  src={selectedProject.image}
                  alt={selectedProject.title}
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-[#0F0F0F] via-[#0F0F0F]/30 to-transparent" />
                <button
                  onClick={() => setSelectedProject(null)}
                  className="absolute top-4 right-4 w-9 h-9 rounded-full bg-black/60 text-[#E1E0CC] flex items-center justify-center border border-white/10 hover:bg-black/90 cursor-pointer"
                >
                  ✕
                </button>
              </div>

              <div className="p-8">
                <span className="px-3 py-1 rounded-full text-xs font-mono bg-[#E1E0CC]/10 text-[#E1E0CC] border border-[#E1E0CC]/20">
                  {selectedProject.category} · {selectedProject.year}
                </span>
                <h3 className="text-2xl sm:text-3xl font-bold text-[#E1E0CC] font-['Syne'] mt-3">
                  {selectedProject.title}
                </h3>
                <p className="text-sm text-[#E1E0CC]/80 font-light mt-3 leading-relaxed">
                  {selectedProject.description}
                </p>
                
                <div className="mt-6 pt-6 border-t border-white/10 grid grid-cols-2 gap-4 text-xs font-mono text-[#E1E0CC]/70">
                  <div>
                    <span className="text-[#E1E0CC]/40 block">DIRECTOR</span>
                    {selectedProject.director}
                  </div>
                  <div>
                    <span className="text-[#E1E0CC]/40 block">DURATION</span>
                    {selectedProject.duration}
                  </div>
                </div>

                <div className="mt-6 flex justify-end">
                  <button
                    onClick={() => setSelectedProject(null)}
                    className="px-6 py-2.5 rounded-full bg-[#E1E0CC] text-[#0A0A0A] font-medium text-sm hover:bg-white transition-colors cursor-pointer"
                  >
                    Close Preview
                  </button>
                </div>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </section>
  );
};
