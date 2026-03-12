"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { ArrowRight, Star, Activity, Shield, Users, ArrowUpRight, FileText, Brain, Microscope, Check } from "lucide-react"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { Navbar } from "@/components/ui/Navbar"

export default function LandingPage() {
  const [isNavigating, setIsNavigating] = useState(false)

  const handleStart = () => {
    setIsNavigating(true)
    setTimeout(() => {
      window.location.href = "/analyze"
    }, 600)
  }

  return (
    <div className="min-h-screen bg-white text-slate-900 overflow-x-hidden font-sans selection:bg-healthcare-accent/20">
      
      {/* Consistent Navbar */}
      <Navbar />

      {/* Main Grid Layout */}
      <main className="max-w-[1400px] mx-auto px-6 pt-28 pb-20">
        <div className="grid lg:grid-cols-12 gap-8 lg:gap-16 items-center">
          
          {/* Left Column: Text (Span 4) */}
          <div className="lg:col-span-4 relative z-10 space-y-8">
            {/* Decorative Star - Animated */}
            <motion.div 
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1, rotate: 360 }}
              transition={{ 
                delay: 0.2,
                rotate: { duration: 20, repeat: Infinity, ease: "linear" }
              }}
              className="absolute -top-16 -right-10 lg:right-0 lg:-top-20 text-healthcare-accent/20"
            >
              <svg width="120" height="120" viewBox="0 0 100 100" fill="currentColor">
                <path d="M50 0 C50 0 70 30 100 50 C70 70 50 100 50 100 C50 100 30 70 0 50 C30 30 50 0 50 0 Z" />
              </svg>
            </motion.div>

            <div className="relative">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: "40px" }}
                className="h-[2px] bg-slate-900 mb-6"
              />
              <motion.p 
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="text-sm font-semibold tracking-widest uppercase text-slate-500 mb-4"
              >
                AI-Powered • Health • Balance
              </motion.p>
              <motion.h1 
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-serif font-medium leading-[1.1] text-slate-900"
              >
                Find perfect <span className="italic text-healthcare-accent">balance</span> for your digestive health
                <span className="inline-block w-3 h-3 bg-red-500 rounded-full ml-2 mb-2"></span>
              </motion.h1>
            </div>

            <motion.p 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="text-slate-600 text-lg leading-relaxed max-w-md"
            >
              8 specialized AI agents collaborate to analyze your symptoms, process medical documents, and provide personalized relief strategies.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
            >
              <Button 
                onClick={handleStart}
                className="h-14 px-8 rounded-full bg-slate-900 text-white text-lg font-medium hover:bg-slate-800 transition-all hover:scale-105 shadow-xl shadow-slate-900/20"
              >
                Start Analysis <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </motion.div>
          </div>

          {/* Center Column: Arch Visual (Span 5) */}
          <div className="lg:col-span-12 xl:col-span-5 relative h-[500px] lg:h-[600px] flex items-end justify-center lg:justify-start">
            <div className="relative w-full h-full flex items-end justify-center">
              {/* Outer Glow Ring */}
              <motion.div 
                className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[115%] h-[85%] rounded-full -z-10"
                style={{
                  background: "radial-gradient(ellipse at center, rgba(99,102,241,0.15) 0%, rgba(168,85,247,0.08) 40%, transparent 70%)"
                }}
                animate={{ scale: [1, 1.02, 1], opacity: [0.6, 1, 0.6] }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
              />

              {/* Main Arch Image - Central Intelligence Hub */}
              <motion.div 
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "100%", opacity: 1 }}
                transition={{ duration: 1.2, ease: "easeOut" }}
                className="relative w-full max-w-md h-full rounded-t-full overflow-hidden"
                style={{
                  background: "linear-gradient(180deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%)"
                }}
              >
                {/* Aurora Gradient Overlay */}
                <motion.div 
                  className="absolute inset-0 opacity-40"
                  style={{
                    background: "radial-gradient(ellipse at 30% 20%, rgba(56,189,248,0.3) 0%, transparent 50%), radial-gradient(ellipse at 70% 80%, rgba(168,85,247,0.25) 0%, transparent 50%), radial-gradient(ellipse at 50% 50%, rgba(34,197,94,0.15) 0%, transparent 60%)"
                  }}
                  animate={{ 
                    opacity: [0.3, 0.5, 0.3],
                  }}
                  transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
                />
                
                {/* Mesh Grid Background */}
                <div className="absolute inset-0 opacity-[0.07]" style={{
                  backgroundImage: `linear-gradient(rgba(255,255,255,0.4) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.4) 1px, transparent 1px)`,
                  backgroundSize: "32px 32px"
                }} />
                
                {/* Floating Particles */}
                {[...Array(6)].map((_, i) => (
                  <motion.div
                    key={i}
                    className="absolute w-1 h-1 rounded-full bg-white/40"
                    style={{
                      left: `${20 + i * 12}%`,
                      top: `${30 + (i % 3) * 20}%`,
                    }}
                    animate={{
                      y: [0, -20, 0],
                      opacity: [0.2, 0.6, 0.2],
                      scale: [1, 1.5, 1],
                    }}
                    transition={{
                      duration: 3 + i * 0.5,
                      repeat: Infinity,
                      delay: i * 0.4,
                      ease: "easeInOut",
                    }}
                  />
                ))}

                {/* Inner Content Container */}
                <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-white/90">
                    
                    {/* Workflow Diagram */}
                    <div className="relative z-10 w-full h-full flex flex-col items-center justify-between py-10 max-w-[300px]">
                       
                       {/* Step 1: Input - Glassmorphic Card */}
                       <motion.div 
                         className="flex flex-col items-center gap-3"
                         initial={{ scale: 0, y: 20 }} 
                         animate={{ scale: 1, y: 0 }} 
                         transition={{ delay: 0.8, type: "spring", stiffness: 200 }}
                       >
                          <div className="relative">
                            {/* Glow Effect */}
                            <div className="absolute inset-0 w-14 h-14 rounded-2xl bg-cyan-400/30 blur-xl" />
                            <div className="relative w-14 h-14 rounded-2xl bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-xl border border-cyan-400/30 flex items-center justify-center shadow-[0_0_30px_rgba(34,211,238,0.2)]">
                               <FileText className="w-6 h-6 text-cyan-300" />
                            </div>
                          </div>
                          <span className="text-[11px] uppercase tracking-[0.2em] text-cyan-300/70 font-medium">Input</span>
                       </motion.div>

                       {/* Connector 1 - Animated Energy Line */}
                       <div className="flex-1 w-[3px] rounded-full bg-gradient-to-b from-cyan-500/20 via-transparent to-transparent relative overflow-hidden my-1">
                          <motion.div 
                            className="absolute top-0 left-0 w-full h-8 rounded-full"
                            style={{
                              background: "linear-gradient(180deg, transparent, rgba(34,211,238,0.8), rgba(34,211,238,0.4), transparent)"
                            }}
                            animate={{ y: ["-100%", "400%"] }}
                            transition={{ duration: 1.8, repeat: Infinity, ease: "easeInOut" }}
                          />
                          {/* Static glow dots */}
                          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-1.5 h-1.5 rounded-full bg-cyan-400/50" />
                          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 w-1 h-1 rounded-full bg-purple-400/40" />
                       </div>

                       {/* Step 2: Central AI Hub - Premium Orbital Design */}
                       <div className="relative w-52 h-52 flex items-center justify-center">
                          
                          {/* Outer Orbital Ring */}
                          <motion.div 
                             className="absolute inset-0 rounded-full"
                             style={{
                               border: "1px dashed rgba(168,85,247,0.3)",
                             }}
                             animate={{ rotate: 360 }}
                             transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
                          />
                          
                          {/* Middle Orbital Ring with Gradient */}
                          <motion.div 
                             className="absolute inset-4 rounded-full"
                             style={{
                               background: "conic-gradient(from 0deg, transparent, rgba(99,102,241,0.2), transparent, rgba(168,85,247,0.2), transparent)",
                               border: "1px solid rgba(99,102,241,0.15)",
                             }}
                             animate={{ rotate: -360 }}
                             transition={{ duration: 18, repeat: Infinity, ease: "linear" }}
                          />
                          
                          {/* Inner Glow Ring */}
                          <motion.div 
                             className="absolute inset-8 rounded-full bg-gradient-to-br from-indigo-500/10 to-purple-500/10"
                             animate={{ scale: [1, 1.05, 1] }}
                             transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                          />

                          {/* Center Node - Glass Brain Hub */}
                          <motion.div 
                            className="relative w-20 h-20 rounded-full flex items-center justify-center z-10"
                            animate={{ scale: [1, 1.02, 1] }}
                            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                          >
                            {/* Multi-layer glow */}
                            <div className="absolute inset-0 rounded-full bg-indigo-500/20 blur-xl" />
                            <div className="absolute inset-1 rounded-full bg-gradient-to-br from-slate-800 via-indigo-950 to-slate-900 border border-indigo-400/30" />
                            <div className="absolute inset-3 rounded-full bg-gradient-to-br from-indigo-900/50 to-purple-900/50 border border-white/10" />
                            <motion.div 
                              className="absolute inset-0 rounded-full"
                              style={{
                                background: "conic-gradient(from 0deg, transparent 0%, rgba(99,102,241,0.3) 25%, transparent 50%, rgba(168,85,247,0.3) 75%, transparent 100%)"
                              }}
                              animate={{ rotate: 360 }}
                              transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
                            />
                            <Brain className="w-8 h-8 text-white relative z-10 drop-shadow-[0_0_8px_rgba(255,255,255,0.5)]" />
                          </motion.div>

                          {/* Satellite Nodes - Premium Floating Orbs */}
                          {/* Node 1: Activity - Top Right */}
                          <motion.div 
                              className="absolute -top-1 right-6"
                              animate={{ y: [0, -6, 0], x: [0, 2, 0] }} 
                              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                          >
                            <div className="relative">
                              <div className="absolute inset-0 w-12 h-12 rounded-full bg-amber-400/20 blur-lg" />
                              <div className="relative w-12 h-12 rounded-full bg-gradient-to-br from-slate-800/95 to-slate-900/95 backdrop-blur-sm border border-amber-400/40 flex items-center justify-center shadow-[0_0_20px_rgba(251,191,36,0.2)]">
                                <Activity className="w-5 h-5 text-amber-400" />
                              </div>
                            </div>
                          </motion.div>
                          
                          {/* Node 2: Shield - Bottom Left */}
                          <motion.div 
                              className="absolute bottom-2 -left-2"
                              animate={{ y: [0, 5, 0], x: [0, -2, 0] }} 
                              transition={{ duration: 3.5, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
                          >
                            <div className="relative">
                              <div className="absolute inset-0 w-12 h-12 rounded-full bg-emerald-400/20 blur-lg" />
                              <div className="relative w-12 h-12 rounded-full bg-gradient-to-br from-slate-800/95 to-slate-900/95 backdrop-blur-sm border border-emerald-400/40 flex items-center justify-center shadow-[0_0_20px_rgba(52,211,153,0.2)]">
                                <Shield className="w-5 h-5 text-emerald-400" />
                              </div>
                            </div>
                          </motion.div>
                          
                          {/* Node 3: Microscope - Bottom Right */}
                          <motion.div 
                              className="absolute bottom-2 -right-2"
                              animate={{ y: [0, -4, 0], x: [0, 3, 0] }} 
                              transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", delay: 1 }}
                          >
                            <div className="relative">
                              <div className="absolute inset-0 w-12 h-12 rounded-full bg-purple-400/20 blur-lg" />
                              <div className="relative w-12 h-12 rounded-full bg-gradient-to-br from-slate-800/95 to-slate-900/95 backdrop-blur-sm border border-purple-400/40 flex items-center justify-center shadow-[0_0_20px_rgba(192,132,252,0.2)]">
                                <Microscope className="w-5 h-5 text-purple-400" />
                              </div>
                            </div>
                          </motion.div>
                          
                          {/* Connection Lines to Satellites */}
                          <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ zIndex: 5 }}>
                            <motion.line x1="50%" y1="40%" x2="75%" y2="15%" stroke="url(#amberGrad)" strokeWidth="1" strokeDasharray="4 4"
                              initial={{ pathLength: 0, opacity: 0 }}
                              animate={{ pathLength: 1, opacity: 0.5 }}
                              transition={{ delay: 1.5, duration: 0.8 }}
                            />
                            <motion.line x1="40%" y1="60%" x2="15%" y2="85%" stroke="url(#greenGrad)" strokeWidth="1" strokeDasharray="4 4"
                              initial={{ pathLength: 0, opacity: 0 }}
                              animate={{ pathLength: 1, opacity: 0.5 }}
                              transition={{ delay: 1.7, duration: 0.8 }}
                            />
                            <motion.line x1="60%" y1="60%" x2="85%" y2="85%" stroke="url(#purpleGrad)" strokeWidth="1" strokeDasharray="4 4"
                              initial={{ pathLength: 0, opacity: 0 }}
                              animate={{ pathLength: 1, opacity: 0.5 }}
                              transition={{ delay: 1.9, duration: 0.8 }}
                            />
                            <defs>
                              <linearGradient id="amberGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stopColor="rgba(251,191,36,0.5)" />
                                <stop offset="100%" stopColor="rgba(251,191,36,0.1)" />
                              </linearGradient>
                              <linearGradient id="greenGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stopColor="rgba(52,211,153,0.5)" />
                                <stop offset="100%" stopColor="rgba(52,211,153,0.1)" />
                              </linearGradient>
                              <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stopColor="rgba(192,132,252,0.5)" />
                                <stop offset="100%" stopColor="rgba(192,132,252,0.1)" />
                              </linearGradient>
                            </defs>
                          </svg>
                       </div>

                       {/* Connector 2 - Animated Energy Line */}
                       <div className="flex-1 w-[3px] rounded-full bg-gradient-to-b from-transparent via-transparent to-emerald-500/20 relative overflow-hidden my-1">
                          <motion.div 
                            className="absolute top-0 left-0 w-full h-8 rounded-full"
                            style={{
                              background: "linear-gradient(180deg, transparent, rgba(52,211,153,0.8), rgba(52,211,153,0.4), transparent)"
                            }}
                            animate={{ y: ["-100%", "400%"] }}
                            transition={{ duration: 1.8, repeat: Infinity, ease: "easeInOut", delay: 0.9 }}
                          />
                          <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-1 h-1 rounded-full bg-purple-400/40" />
                          <div className="absolute top-2/3 left-1/2 -translate-x-1/2 w-1.5 h-1.5 rounded-full bg-emerald-400/50" />
                       </div>

                       {/* Step 3: Result - Premium Success Badge */}
                       <motion.div 
                         className="flex flex-col items-center gap-3"
                         initial={{ scale: 0, y: -20 }} 
                         animate={{ scale: 1, y: 0 }} 
                         transition={{ delay: 1.2, type: "spring", stiffness: 200 }}
                       >
                          <div className="relative">
                            {/* Multi-layer glow */}
                            <div className="absolute inset-0 w-14 h-14 rounded-2xl bg-emerald-400/30 blur-xl" />
                            <motion.div 
                              className="absolute -inset-1 rounded-2xl opacity-60"
                              style={{
                                background: "linear-gradient(135deg, rgba(52,211,153,0.5) 0%, rgba(16,185,129,0.3) 50%, rgba(5,150,105,0.5) 100%)"
                              }}
                              animate={{ opacity: [0.4, 0.7, 0.4] }}
                              transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                            />
                            <div className="relative w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-500 via-green-500 to-teal-600 flex items-center justify-center shadow-[0_0_30px_rgba(52,211,153,0.4),0_4px_20px_rgba(0,0,0,0.3)]">
                               <Check className="w-7 h-7 text-white drop-shadow-lg" />
                            </div>
                          </div>
                          <span className="text-[11px] uppercase tracking-[0.2em] text-emerald-300/70 font-medium">Report</span>
                       </motion.div>
                    </div>
                </div>

                {/* Bottom Gradient Fade */}
                <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-slate-900/80 to-transparent pointer-events-none" />
                
                {/* Inner Border Glow */}
                <div className="absolute inset-0 rounded-t-full border border-white/[0.08] pointer-events-none" />

              </motion.div>
            </div>
          </div>

          {/* Right Column: Stacked Images (Span 3) */}
          <div className="hidden xl:flex lg:col-span-3 flex-col gap-6 h-full justify-center">
             {[
               { color: "bg-orange-50", icon: <FileText className="w-8 h-8 text-orange-600" />, label: "Document Intake" },
               { color: "bg-blue-50", icon: <Microscope className="w-8 h-8 text-blue-600" />, label: "Deep Analysis" },
               { color: "bg-purple-50", icon: <Activity className="w-8 h-8 text-purple-600" />, label: "Smart Relief" }
             ].map((item, i) => (
               <motion.div
                key={i}
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 1.2 + (i * 0.1) }}
                className={`flex-1 min-h-[160px] rounded-[2rem] ${item.color} flex items-center justify-center relative group overflow-hidden cursor-pointer hover:shadow-lg transition-all`}
               >
                 <div className="text-center">
                    <span className="mb-3 block group-hover:scale-110 transition-transform duration-300 inline-block">{item.icon}</span>
                    <span className="block text-sm font-medium text-slate-600">{item.label}</span>
                 </div>
                 {/* Hover Overlay */}
                 <div className="absolute inset-0 bg-black/0 group-hover:bg-black/5 transition-colors absolute inset-0" />
               </motion.div>
             ))}
          </div>
        </div>

        {/* Bottom Stats Row - Updated with Factual Info */}
        <div className="mt-16 grid md:grid-cols-3 gap-6 lg:gap-8">
          {[
            { 
              value: "8 Agents", 
              label: "Multi-agent architecture working in parallel",
              bg: "bg-blue-100",
              text: "text-blue-900"
            },
            { 
              value: "Clinical Logic", 
              label: "Follows standard diagnostic protocols",
              bg: "bg-amber-100", 
              text: "text-amber-900"
            },
            { 
              value: "Multi-Modal", 
              label: "Analyzes symptoms, PDF reports & images",
              bg: "bg-rose-100",
              text: "text-rose-900"
            }
          ].map((stat, i) => (
             <motion.div
               key={i}
               initial={{ opacity: 0, y: 30 }}
               animate={{ opacity: 1, y: 0 }}
               transition={{ delay: 1.5 + (i * 0.1) }}
               className={`${stat.bg} rounded-2xl p-6 lg:p-8 flex flex-col justify-between min-h-[140px] relative overflow-hidden group`}
             >
                <div className="relative z-10">
                   <h3 className={`text-3xl lg:text-3xl font-bold ${stat.text} mb-2`}>{stat.value}</h3>
                   <p className={`${stat.text}/80 text-sm lg:text-base`}>{stat.label}</p>
                </div>
                <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
                   <div className="w-8 h-8 rounded-full bg-white/30 flex items-center justify-center">
                      <ArrowUpRight className={`w-4 h-4 ${stat.text}`} />
                   </div>
                </div>
             </motion.div>
          ))}
        </div>
      </main>
    </div>
  )
}
