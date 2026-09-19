"use client";

import { useEffect, useState } from "react";
import { ArrowUp, Disc3 } from "lucide-react";

export const Footer = () => {
  const [times, setTimes] = useState({
    tokyo: "",
    berlin: "",
    london: "",
    newYork: "",
    saoPaulo: "",
  });

  useEffect(() => {
    const updateClocks = () => {
      const now = new Date();
      const format = (tz: string) =>
        new Intl.DateTimeFormat("en-US", {
          timeZone: tz,
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
          hour12: false,
        }).format(now);

      setTimes({
        tokyo: format("Asia/Tokyo"),
        berlin: format("Europe/Berlin"),
        london: format("Europe/London"),
        newYork: format("America/New_York"),
        saoPaulo: format("America/Sao_Paulo"),
      });
    };

    updateClocks();
    const interval = setInterval(updateClocks, 1000);
    return () => clearInterval(interval);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <footer className="w-full border-t border-white/10 bg-[#070707] text-[#E1E0CC] pt-16 pb-12 px-4 sm:px-6 md:px-12 lg:px-20">
      <div className="max-w-7xl mx-auto space-y-16">
        {/* World Time Hubs */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6 pb-12 border-b border-white/5 text-xs font-mono">
          <div>
            <span className="text-[#E1E0CC]/40 block mb-1">TOKYO (JST)</span>
            <span className="text-sm text-[#E1E0CC] font-semibold">{times.tokyo || "--:--:--"}</span>
          </div>
          <div>
            <span className="text-[#E1E0CC]/40 block mb-1">BERLIN (CET)</span>
            <span className="text-sm text-[#E1E0CC] font-semibold">{times.berlin || "--:--:--"}</span>
          </div>
          <div>
            <span className="text-[#E1E0CC]/40 block mb-1">LONDON (GMT)</span>
            <span className="text-sm text-[#E1E0CC] font-semibold">{times.london || "--:--:--"}</span>
          </div>
          <div>
            <span className="text-[#E1E0CC]/40 block mb-1">NEW YORK (EST)</span>
            <span className="text-sm text-[#E1E0CC] font-semibold">{times.newYork || "--:--:--"}</span>
          </div>
          <div>
            <span className="text-[#E1E0CC]/40 block mb-1">SÃO PAULO (BRT)</span>
            <span className="text-sm text-[#E1E0CC] font-semibold">{times.saoPaulo || "--:--:--"}</span>
          </div>
        </div>

        {/* Main Footer Row */}
        <div className="flex flex-col md:flex-row items-start md:items-end justify-between gap-8">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Disc3 className="w-5 h-5 text-[#E1E0CC] animate-spin" style={{ animationDuration: "12s" }} />
              <span className="font-bold text-xl tracking-tight font-['Syne']">Prisma*</span>
            </div>
            <p className="text-xs text-[#E1E0CC]/60 max-w-sm font-light leading-relaxed">
              An international non-profit audiovisual laboratory exploring light, analog emulsion,
              granular synthesis, and physical cinema.
            </p>
          </div>

          {/* Social Links */}
          <div className="flex flex-wrap items-center gap-6 text-xs font-mono uppercase tracking-wider text-[#E1E0CC]/70">
            <a href="https://vimeo.com" target="_blank" rel="noreferrer" className="hover:text-white transition-colors">
              Vimeo
            </a>
            <a href="https://instagram.com" target="_blank" rel="noreferrer" className="hover:text-white transition-colors">
              Instagram
            </a>
            <a href="https://are.na" target="_blank" rel="noreferrer" className="hover:text-white transition-colors">
              Are.na
            </a>
            <a href="https://discord.com" target="_blank" rel="noreferrer" className="hover:text-white transition-colors">
              Discord
            </a>
            <button
              onClick={scrollToTop}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/15 text-[#E1E0CC] transition-colors cursor-pointer ml-auto"
            >
              <span>Top</span>
              <ArrowUp className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Bottom Legal / Credits */}
        <div className="pt-8 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between text-[11px] font-mono text-[#E1E0CC]/40 gap-4">
          <p>© {new Date().getFullYear()} Prisma Collective & Creative Lab. All rights reserved.</p>
          <p>Cinematic Hero Section based on 21st.dev / Rahil Vahora</p>
        </div>
      </div>
    </footer>
  );
};
