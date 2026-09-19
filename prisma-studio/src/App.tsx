import { PrismaHero } from "@/components/ui/prisma-hero";
import { OurStory } from "@/components/sections/OurStory";
import { CollectiveWorks } from "@/components/sections/CollectiveWorks";
import { Workshops } from "@/components/sections/Workshops";
import { Programs } from "@/components/sections/Programs";
import { Inquiries } from "@/components/sections/Inquiries";
import { Footer } from "@/components/sections/Footer";

export default function App() {
  return (
    <main className="min-h-screen bg-[#0A0A0A] text-[#E1E0CC] selection:bg-[#E1E0CC] selection:text-[#0A0A0A]">
      {/* 1. Cinematic Hero Section (PrismaHero) */}
      <PrismaHero />

      {/* 2. Our Story / Manifesto */}
      <OurStory />

      {/* 3. Selected Collective Works */}
      <CollectiveWorks />

      {/* 4. Masterclasses & Workshops */}
      <Workshops />

      {/* 5. Residencies & Programs */}
      <Programs />

      {/* 6. Inquiries & Submissions */}
      <Inquiries />

      {/* 7. Footer & Live World Clocks */}
      <Footer />
    </main>
  );
}
