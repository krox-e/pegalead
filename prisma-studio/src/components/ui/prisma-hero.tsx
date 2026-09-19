"use client";

import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import { useState } from "react";

const WordsPullUp = ({
  text,
  className = "",
}: {
  text: string;
  className?: string;
}) => {
  const words = text.split(" ");

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
      },
    },
  };

  const item = {
    hidden: { y: 20, opacity: 0 },
    show: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.8,
        ease: [0.16, 1, 0.3, 1] as [number, number, number, number],
      },
    },
  };

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className={className}
    >
      {words.map((word, i) => (
        <motion.span
          key={i}
          variants={item}
          style={{ display: "inline-block", marginRight: "0.25em" }}
        >
          {word}
        </motion.span>
      ))}
    </motion.div>
  );
};

export const PrismaHero = () => {
  const [activeTab, setActiveTab] = useState("Our story");

  const navItems = [
    { label: "Our story", href: "#story" },
    { label: "Collective", href: "#collective" },
    { label: "Workshops", href: "#workshops" },
    { label: "Programs", href: "#programs" },
    { label: "Inquiries", href: "#inquiries" },
  ];

  return (
    <section className="h-screen w-full p-2 sm:p-3 md:p-4">
      <div className="relative h-full w-full overflow-hidden rounded-2xl md:rounded-[2rem] border border-white/10 shadow-2xl">
        {/* Background Video */}
        <video
          autoPlay
          loop
          muted
          playsInline
          className="absolute inset-0 h-full w-full object-cover"
        >
          <source
            src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260405_170732_8a9ccda6-5cff-4628-b164-059c500a2b41.mp4"
            type="video/mp4"
          />
        </video>

        {/* Noise overlay */}
        <div className="noise-overlay pointer-events-none absolute inset-0 opacity-[0.7] mix-blend-overlay" />

        {/* Cinematic gradient overlay */}
        <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/85 via-black/25 to-black/45" />

        <div className="relative z-10 flex h-full flex-col justify-between p-4 sm:p-6 md:p-8">
          {/* Floating pill navigation */}
          <div className="flex justify-center pt-2">
            <nav className="flex items-center gap-1 rounded-full bg-black/80 px-2 py-1.5 backdrop-blur-md border border-white/10 shadow-xl">
              {navItems.map((item) => (
                <a
                  key={item.label}
                  href={item.href}
                  onClick={() => setActiveTab(item.label)}
                  className={`relative rounded-full px-3 py-1 text-xs transition-colors sm:px-4 sm:text-sm font-medium ${
                    activeTab === item.label
                      ? "text-black"
                      : "text-white/70 hover:text-white"
                  }`}
                >
                  {activeTab === item.label && (
                    <motion.div
                      layoutId="active-pill"
                      className="absolute inset-0 rounded-full bg-[#E1E0CC]"
                      transition={{
                        type: "spring",
                        stiffness: 380,
                        damping: 30,
                      }}
                    />
                  )}
                  <span className="relative z-10">{item.label}</span>
                </a>
              ))}
            </nav>
          </div>

          {/* Bottom content */}
          <div className="grid grid-cols-12 gap-4 pb-2 sm:pb-4">
            <div className="col-span-12 md:col-span-8">
              <h1
                style={{ color: "#E1E0CC", fontFamily: "'Syne', sans-serif" }}
                className="font-bold leading-[0.82] tracking-[-0.07em] text-[26vw] sm:text-[24vw] md:text-[22vw] lg:text-[20vw] xl:text-[19vw] 2xl:text-[20vw] select-none"
              >
                <WordsPullUp text="Prisma*" />
              </h1>
            </div>

            <div className="col-span-12 flex flex-col justify-end gap-3 md:col-span-4 md:items-start md:pb-3">
              <motion.p
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.4 }}
                className="text-xs sm:text-sm md:text-base leading-relaxed text-[#E1E0CC]/80 max-w-md font-light"
              >
                A non-profit studio exploring creative storytelling through sound, light, and movement.
              </motion.p>
              <motion.a
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.6 }}
                href="#inquiries"
                className="group inline-flex items-center gap-2 self-start rounded-full bg-[#E1E0CC] py-1.5 pl-5 pr-1.5 text-sm font-semibold text-[#0A0A0A] transition-all hover:gap-3 hover:bg-white sm:text-base shadow-lg cursor-pointer"
              >
                <span className="tracking-tight">Join the lab</span>
                <span className="flex h-7 w-7 items-center justify-center rounded-full bg-[#0A0A0A] text-[#E1E0CC] transition-transform group-hover:rotate-45 sm:h-8 sm:w-8">
                  <ArrowRight className="h-3.5 w-3.5 sm:h-4 sm:w-4" />
                </span>
              </motion.a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default PrismaHero;
