"use client"

import { motion } from "framer-motion"
import { FileText, User, Activity, Search, Shield, FileCheck } from "lucide-react"

interface LiveReportBuilderProps {
  completedSteps: number[]
  totalSteps: number
  currentStep: number
}

export function LiveReportBuilder({ completedSteps, totalSteps, currentStep }: LiveReportBuilderProps) {
  // Define sections mapped to analysis steps
  const sections = [
    { id: 0, label: "Patient Profile", icon: <User className="w-4 h-4" />, lines: 3 },
    { id: 1, label: "Clinical Analysis", icon: <Activity className="w-4 h-4" />, lines: 4 },
    { id: 2, label: "Research Findings", icon: <Search className="w-4 h-4" />, lines: 3 },
    { id: 3, label: "Safety Check", icon: <Shield className="w-4 h-4" />, lines: 2 },
    { id: 4, label: "Recommendations", icon: <FileCheck className="w-4 h-4" />, lines: 4 },
  ]

  // Helper to determine section status
  const getSectionStatus = (index: number) => {
    // Map available sections to total steps roughly
    const progressPerSection = totalSteps / sections.length
    const threshold = index * progressPerSection
    
    if (completedSteps.length > threshold + 0.5) return "completed"
    if (currentStep >= threshold && currentStep < threshold + progressPerSection) return "active"
    return "pending"
  }

  return (
    <motion.div 
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="w-full h-full min-h-[500px] flex flex-col bg-white/50 backdrop-blur-sm rounded-3xl p-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-healthcare-accent/10 rounded-xl">
            <FileText className="w-5 h-5 text-healthcare-accent" />
          </div>
          <div>
            <span className="block text-sm font-bold text-healthcare-heading">LIVE REPORT</span>
            <span className="text-xs text-healthcare-muted">Real-time compilation</span>
          </div>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 bg-green-500/10 rounded-full border border-green-500/20">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
          </span>
          <span className="text-[10px] font-bold text-green-700 uppercase tracking-wide">Building</span>
        </div>
      </div>

      {/* Builder Canvas */}
      <div className="space-y-8 overflow-y-auto flex-1 custom-scrollbar pr-2">
        {sections.map((section, index) => {
          const status = getSectionStatus(index)
          
          return (
            <div key={section.id} className="space-y-3">
              {/* Section Header */}
              <div className="flex items-center gap-3">
                <div className={`p-1.5 rounded-lg transition-colors duration-500 shadow-sm ${
                  status === "completed" ? "bg-healthcare-accent/10 text-healthcare-accent" : 
                  status === "active" ? "bg-white text-slate-500 shadow-slate-200" : "bg-slate-50/50 text-slate-300"
                }`}>
                  {section.icon}
                </div>
                <span className={`text-sm font-semibold transition-colors duration-500 ${
                  status === "completed" ? "text-slate-800" : 
                  status === "active" ? "text-slate-700" : "text-slate-300"
                }`}>
                  {section.label}
                </span>
                {status === "completed" && (
                  <motion.div 
                    initial={{ scale: 0 }} 
                    animate={{ scale: 1 }}
                    className="ml-auto"
                  >
                    <div className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.4)]" />
                  </motion.div>
                )}
              </div>

              {/* Skeleton Lines */}
              <div className="space-y-2 pl-10">
                {Array.from({ length: section.lines }).map((_, i) => (
                  <div key={i} className="relative h-2 rounded-full overflow-hidden bg-slate-100/50">
                    <motion.div
                      className={`absolute inset-0 h-full rounded-full ${
                        status === "completed" ? "bg-slate-300" : 
                        status === "active" ? "bg-gradient-to-r from-slate-200 via-healthcare-accent/20 to-slate-200" : "bg-transparent"
                      }`}
                      animate={status === "active" ? {
                        x: ["-100%", "100%"]
                      } : {}}
                      transition={{
                        repeat: Infinity,
                        duration: 1.5,
                        ease: "linear"
                      }}
                      style={{ 
                        width: i === section.lines - 1 ? "60%" : "100%",
                      }}
                    />
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>
      
      {/* Footer Status */}
      <div className="mt-8 text-xs text-center text-healthcare-muted font-medium bg-white/40 py-3 rounded-xl border border-white/50">
        AI Agents are constructing your report...
      </div>
    </motion.div>
  )
}
