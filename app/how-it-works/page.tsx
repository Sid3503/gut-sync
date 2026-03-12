"use client"

import { motion } from "framer-motion"
import { ArrowLeft, GitGraph, BookOpen, Activity, Search, FileText, AlertTriangle, ShieldCheck } from "lucide-react"
import { Button } from "@/components/ui/button"

import { Navbar } from "@/components/ui/Navbar"

export default function HowItWorksPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-healthcare-bg via-healthcare-surface to-healthcare-bg overflow-x-hidden">
      {/* Consistent Navbar */}
      <Navbar />

      {/* Main Content */}
      <main className="mx-auto max-w-5xl px-4 sm:px-6 pt-28 pb-24 sm:pt-32 lg:pt-36">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h1 className="mb-6 text-4xl sm:text-5xl font-bold text-healthcare-heading leading-tight">
            Under the Hood: <br />
            <span className="text-healthcare-accent">Agentic Architecture</span>
          </h1>
          <p className="mx-auto max-w-2xl text-lg text-healthcare-muted leading-relaxed">
            See how our 7+ specialized AI agents collaborate in a <strong>LangGraph</strong> workflow to analyze, research, and report on your gut health.
          </p>
        </motion.div>

        {/* 1. Architecture Diagram - EXACT from graph.py */}
        <section className="mb-20">
          <h2 className="mb-8 text-center text-3xl font-bold text-healthcare-heading flex items-center justify-center gap-3">
            <GitGraph className="w-8 h-8 text-healthcare-accent" />
            GutSyncGraph Topology
          </h2>
          <p className="text-center text-sm text-healthcare-muted mb-8">Exact representation from <code className="bg-healthcare-surface px-2 py-0.5 rounded">graph.py</code></p>
          
          <div className="relative rounded-3xl border border-healthcare-border bg-white p-4 sm:p-8 shadow-md">
             {/* Background Grid */}
             <div className="absolute inset-0 bg-[linear-gradient(to_right,#f0f0f0_1px,transparent_1px),linear-gradient(to_bottom,#f0f0f0_1px,transparent_1px)] bg-[size:24px_24px] opacity-30 pointer-events-none" />

             {/* MOBILE / TABLET VIEW (Vertical Stack) */}
             <div className="lg:hidden flex flex-col items-center gap-4 py-8 w-full">
                <GraphNode label="START" color="gray" />
                <Arrow vertical />
                <GraphNode label="intake_node" color="blue" icon="📥" />
                <Arrow vertical />
                
                {/* Branch Indicator */}
                <div className="w-full max-w-[260px] p-3 bg-slate-50/80 rounded-xl border border-dashed border-slate-300 flex flex-col gap-2 items-center">
                   <div className="text-[10px] text-slate-500 font-mono uppercase tracking-wider text-center">Multi-Modal Ingestion</div>
                   <div className="flex gap-2">
                      <GraphNode label="PDF" color="blue" icon="📄" />
                      <GraphNode label="Image" color="purple" icon="📸" />
                   </div>
                </div>
                <Arrow vertical />
                
                <GraphNode label="symptom_analysis_node" color="blue" icon="🔬" />
                <Arrow vertical />
                <GraphNode label="root_cause_node" color="yellow" icon="🔍" />
                <Arrow vertical />
                <GraphNode label="severity_node" color="green" icon="📊" />
                
                <div className="flex items-center gap-2 my-2">
                   <div className="h-4 w-px bg-slate-300" />
                   <span className="text-[10px] text-slate-400 font-mono">FAN-OUT</span>
                   <div className="h-4 w-px bg-slate-300" />
                </div>

                {/* Parallel Group */}
                <div className="p-3 bg-emerald-50/50 rounded-xl border border-emerald-100 flex flex-col gap-3 items-center w-full max-w-[280px]">
                   <GraphNode label="research_node" color="green-light" icon="📚" />
                   <Arrow vertical />
                   <GraphNode label="guideline_node" color="green-light" icon="🏥" />
                   <Arrow vertical />
                   <GraphNode label="nutrition_node" color="green-light" icon="🥗" />
                </div>
                
                <div className="flex items-center gap-2 my-2">
                   <div className="h-4 w-px bg-slate-300" />
                   <span className="text-[10px] text-slate-400 font-mono">FAN-IN</span>
                   <div className="h-4 w-px bg-slate-300" />
                </div>

                <GraphNode label="relief_node" color="blue" icon="💊" />
                <Arrow vertical />
                <GraphNode label="red_flag_node" color="yellow" icon="🚩" />
                <Arrow vertical />
                <GraphNode label="report_node" color="dark" icon="📝" />
                <Arrow vertical />
                <GraphNode label="END" color="gray" />
             </div>

             {/* DESKTOP VIEW (Original Horizontal Flow) */}
             <div className="hidden lg:block relative min-w-full overflow-x-auto pb-4">
               <div className="min-w-[1100px] py-8">
               
               {/* Row 1: START → intake_node */}
               <div className="flex items-center justify-start gap-2 mb-8">
                 <GraphNode label="START" color="gray" />
                 <Arrow />
                 <GraphNode label="intake_node" color="blue" icon="📥" />
               </div>

               {/* Row 2: Conditional PDF/Image Processing */}
               <div className="flex items-start gap-8 ml-[200px] mb-8">
                 {/* PDF Branch */}
                 <div className="flex flex-col items-center gap-2">
                   <div className="text-xs text-blue-600 font-semibold mb-1">if PDF uploaded</div>
                   <Arrow vertical />
                   <GraphNode label="pdf_analysis_node" color="blue" icon="📄" />
                   <Arrow vertical />
                   <GraphNode label="pdf_enrichment_node" color="blue" icon="📋" />
                   <Arrow vertical />
                   <div className="flex flex-col items-center gap-2">
                     <div className="text-xs text-purple-600 font-semibold">if Images uploaded</div>
                     <Arrow vertical />
                     <GraphNode label="image_analysis_node" color="purple" icon="📸" />
                     <Arrow vertical />
                     <GraphNode label="image_enrichment_node" color="purple" icon="🖼️" />
                   </div>
                 </div>

                 {/* Direct to Images Branch */}
                 <div className="flex flex-col items-center gap-2">
                   <div className="text-xs text-purple-600 font-semibold mb-1">if only Images</div>
                   <Arrow vertical />
                   <GraphNode label="image_analysis_node" color="purple" icon="📸" />
                   <Arrow vertical />
                   <GraphNode label="image_enrichment_node" color="purple" icon="🖼️" />
                 </div>

                 {/* Direct Path */}
                 <div className="flex flex-col items-center gap-2">
                   <div className="text-xs text-gray-600 font-semibold mb-1">if no files</div>
                   <Arrow vertical />
                   <div className="text-xs text-healthcare-muted">(direct to symptoms)</div>
                 </div>
               </div>

               {/* Convergence Indicator */}
               <div className="flex items-center gap-2 ml-[200px] mb-4">
                 <div className="text-xs text-healthcare-muted font-mono">↓ ALL PATHS CONVERGE</div>
               </div>

               {/* Row 3: Core Analysis Flow */}
               <div className="flex items-center justify-start gap-2 mb-8 ml-[100px]">
                 <GraphNode label="symptom_analysis_node" color="blue" icon="🔬" />
                 <Arrow />
                 <GraphNode label="root_cause_node" color="yellow" icon="🔍" />
                 <Arrow />
                 <GraphNode label="severity_node" color="green" icon="📊" />
               </div>

               {/* Fan-Out Indicator */}
               <div className="flex items-center gap-2 ml-[520px] mb-4">
                 <div className="text-xs text-healthcare-muted font-mono">↓ PARALLEL FAN-OUT</div>
               </div>

               {/* Row 4: Research Nodes (Parallel) */}
               <div className="flex items-center justify-center gap-4 mb-4 ml-[300px]">
                 <GraphNode label="research_node" color="green-light" icon="📚" />
                 <GraphNode label="guideline_node" color="green-light" icon="🏥" />
                 <GraphNode label="nutrition_node" color="green-light" icon="🥗" />
               </div>

               {/* Fan-In Indicator */}
               <div className="flex items-center gap-2 ml-[450px] mb-4">
                 <div className="text-xs text-healthcare-muted font-mono">↓ FAN-IN (research_sync)</div>
               </div>

               {/* Row 5: Conditional Router */}
               <div className="flex items-center gap-2 ml-[400px] mb-8">
                 <div className="px-4 py-2 rounded-lg border-2 border-dashed border-purple-300 bg-purple-50 text-purple-700 font-mono text-xs">
                   route_by_severity(state)
                 </div>
               </div>

               {/* Conditional Paths */}
               <div className="flex items-start gap-12 ml-[350px] mb-8">
                 {/* Mild Path */}
                 <div className="flex flex-col items-center gap-2">
                   <div className="text-xs text-green-600 font-semibold">if severity == "mild"</div>
                   <Arrow vertical />
                   <GraphNode label="relief_node" color="blue" icon="💊" />
                   <Arrow vertical />
                 </div>
                 
                 {/* Severe Path */}
                 <div className="flex flex-col items-center gap-2">
                   <div className="text-xs text-red-600 font-semibold">if severity == "severe"</div>
                   <Arrow vertical />
                   <div className="text-xs text-healthcare-muted">(skip relief)</div>
                 </div>
               </div>

               {/* Row 6: Convergence → red_flag_node → report_node → END */}
               <div className="flex items-center justify-center gap-2">
                 <GraphNode label="red_flag_node" color="yellow" icon="🚩" />
                 <Arrow />
                 <GraphNode label="report_node" color="dark" icon="📝" />
                 <Arrow />
                 <GraphNode label="END" color="gray" />
               </div>

             </div>
             </div>
          </div>

          {/* Code Reference */}
          <div className="mt-6 p-4 rounded-xl bg-slate-900 text-slate-100 font-mono text-xs overflow-x-auto">
            <pre>{`# From graph.py - Edge Definitions
workflow.add_edge(START, "intake_node")

# PDF & Image Routing (Conditional)
workflow.add_conditional_edges("intake_node", route_for_pdf, {
    "pdf_analysis_node": "pdf_analysis_node",
    "image_analysis_node": "image_analysis_node",
    "symptom_analysis_node": "symptom_analysis_node"
})
workflow.add_edge("pdf_analysis_node", "pdf_enrichment_node")

# Image Routing (after PDF enrichment)
workflow.add_conditional_edges("pdf_enrichment_node", route_for_images, {
    "image_analysis_node": "image_analysis_node",
    "symptom_analysis_node": "symptom_analysis_node"
})
workflow.add_edge("image_analysis_node", "image_enrichment_node")
workflow.add_edge("image_enrichment_node", "symptom_analysis_node")

# Core Analysis Flow
workflow.add_edge("symptom_analysis_node", "root_cause_node")
workflow.add_edge("root_cause_node", "severity_node")

# Fan-Out (Parallel Research)
workflow.add_edge("severity_node", "research_node")
workflow.add_edge("severity_node", "guideline_node")
workflow.add_edge("severity_node", "nutrition_node")

# Fan-In
workflow.add_edge("research_node", "research_sync")
workflow.add_edge("guideline_node", "research_sync")
workflow.add_edge("nutrition_node", "research_sync")

# Conditional Router
workflow.add_conditional_edges("research_sync", route_by_severity)

# Convergence
workflow.add_edge("relief_node", "red_flag_node")
workflow.add_edge("red_flag_node", "report_node")
workflow.add_edge("report_node", END)`}</pre>
          </div>
        </section>

        {/* 2. Dry Run Example */}
        <section className="mb-20">
           <h2 className="mb-8 text-center text-2xl font-bold text-healthcare-heading flex items-center justify-center gap-2">
            <Activity className="w-6 h-6 text-healthcare-accent" />
            Live Processing Example
          </h2>
          
          <div className="rounded-2xl border border-healthcare-border bg-healthcare-surface p-6 sm:p-8">
            <div className="mb-6 bg-white p-4 rounded-lg shadow-sm border border-healthcare-border/50 max-w-xl mx-auto">
              <span className="text-xs font-semibold text-healthcare-muted uppercase tracking-wider">User Input</span>
              <p className="text-healthcare-text italic mt-2">"I feel bloated and gassy about 30 minutes after eating ice cream or cheese. It's uncomfortable but not painful."</p>
              <div className="mt-3 flex items-center gap-2 text-xs text-healthcare-muted flex-wrap">
                <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded">📄 Lab Report.pdf</span>
                <span className="px-2 py-1 bg-purple-50 text-purple-700 rounded">📸 Symptom Photo.jpg</span>
              </div>
            </div>

            <div className="space-y-4">
               <Step 
                 num="01" 
                 title="Intake & Normalization" 
                 desc="IntakeAgent normalizes input and detects uploaded files."
                 data={{ symptoms: ["bloating", "gas"], onset: "30 mins", triggers: ["dairy", "ice cream", "cheese"], files: { pdf: true, images: 1 } }}
               />
               <Step 
                 num="02" 
                 title="Document & Image Analysis" 
                 desc="PDF and Image agents extract clinical context from uploaded files."
                 data={{ 
                   pdf_findings: "Previous lactose breath test: positive", 
                   image_findings: "Visible abdominal distension, no alarming features"
                 }}
               />
               <Step 
                 num="03" 
                 title="Root Cause Analysis" 
                 desc="RootCauseNode identifies potential link with enriched context."
                 data={{ potential_cause: "Lactose Intolerance", confidence: "Very High", supporting_evidence: ["breath test", "symptom pattern", "visual confirmation"] }}
               />
               <Step 
                 num="04" 
                 title="Research Activation" 
                 desc="Agents query external databases in parallel."
                 data={{ 
                     PubMed: "Search: 'lactose intolerance bloating mechanism'", 
                     Guidelines: "Fetch: 'ACG Guidelines Lactose Intolerance Management'",
                     Nutrition: "Query: 'Low FODMAP dairy alternatives'"
                 }}
               />
               <Step 
                 num="05" 
                 title="Report Synthesis" 
                 desc="LLM compiles findings into comprehensive Markdown report."
                 data={{ section: "Research-Backed Relief", content: "Based on your positive breath test and symptom pattern, consider lactase supplements and lactose-free alternatives..." }}
               />
            </div>
          </div>
        </section>

        {/* 3. Detailed Agent Nodes */}
        <section>
          <h2 className="mb-8 text-center text-2xl font-bold text-healthcare-heading flex items-center justify-center gap-2">
            <ShieldCheck className="w-6 h-6 text-healthcare-accent" />
            Agent Roster
          </h2>
          
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
             <AgentCard 
               title="Intake Agent" 
               icon="📥"
               role="Data Normalizer"
               details="Converts messy natural language into structured JSON state."
             />
             <AgentCard 
               title="PDF Agent" 
               icon="📄"
               role="Document Analyst"
               details="Extracts and summarizes clinical context from uploaded medical reports."
             />
             <AgentCard 
               title="Image Agent" 
               icon="📸"
               role="Visual Analyzer"
               details="Processes medical images including lab results, endoscopy reports, and symptom photos to extract clinical insights."
             />
             <AgentCard 
               title="Research Agent" 
               icon="📚"
               role="Academic Scout"
               details="Uses `DuckDuckGoSearch` to scan PubMed & NIH for mechanism-of-action papers."
             />
             <AgentCard 
               title="Guideline Agent" 
               icon="🏥"
               role="Protocol Checker"
               details="Fetches official protocols from CDC, ACG, and WGO."
             />
             <AgentCard 
               title="Nutrition Agent" 
               icon="🥗"
               role="Dietary Expert"
               details="Identifies trigger foods and suggests nutritional alternatives."
             />
             <AgentCard 
               title="Red Flag Agent" 
               icon="🚩"
               role="Safety Guardian"
               details="Scans strictly for emergency indicators (blood, severe pain, fever)."
             />
             <AgentCard 
               title="Report Agent" 
               icon="📝"
               role="Synthesizer"
               details="Compiles all parallel streams into a empathetic, cited final report."
             />
          </div>
        </section>

      </main>
    </div>
  )
}

// Sub-components for cleaner code
function GraphNode({ label, color, icon }: { label: string, color: string, icon?: string }) {
  const styles: Record<string, string> = {
     gray: "bg-gray-100 border-gray-300 text-gray-700",
     blue: "bg-blue-50 border-blue-200 text-blue-700",
     yellow: "bg-amber-50 border-amber-200 text-amber-700",
     green: "bg-green-100 border-green-300 text-green-800 shadow-lg",
     "green-light": "bg-green-50/80 border-green-200 text-green-700",
     purple: "bg-purple-50 border-purple-200 text-purple-700",
     dark: "bg-slate-800 border-slate-900 text-white",
  }

  return (
    <div className={`
       flex items-center gap-2 px-4 py-3 rounded-xl border-2 font-mono text-xs sm:text-sm font-semibold transition-all hover:scale-105 cursor-default relative
       ${styles[color] || styles.gray}
    `}>
       {icon && <span className="text-base">{icon}</span>}
       {label}
       {/* Dot Connector */}
       <div className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-2 h-2 bg-current rounded-full opacity-50" />
       <div className="absolute -top-1 left-1/2 -translate-x-1/2 w-2 h-2 bg-current rounded-full opacity-50" />
    </div>
  )
}

function Arrow({ vertical }: { vertical?: boolean }) {
  if (vertical) {
    return (
      <div className="flex flex-col items-center">
        <div className="w-px h-6 bg-slate-400" />
        <div className="w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-slate-400" />
      </div>
    )
  }
  return (
    <div className="flex items-center">
      <div className="w-6 h-px bg-slate-400" />
      <div className="w-0 h-0 border-t-4 border-b-4 border-l-4 border-t-transparent border-b-transparent border-l-slate-400" />
    </div>
  )
}

function Step({ num, title, desc, data }: { num: string, title: string, desc: string, data: any }) {
    return (
        <div className="flex flex-col sm:flex-row gap-2 sm:gap-4">
            <div className="flex-shrink-0 w-8 text-healthcare-accent font-bold text-lg pt-0 sm:pt-1">{num}</div>
            <div className="flex-grow min-w-0">
                <h4 className="font-semibold text-healthcare-heading">{title}</h4>
                <p className="text-sm text-healthcare-muted mb-2">{desc}</p>
                <div className="bg-healthcare-card border border-healthcare-border rounded-lg p-3 text-xs font-mono text-healthcare-text overflow-x-auto">
                    <pre>{JSON.stringify(data, null, 2)}</pre>
                </div>
            </div>
        </div>
    )
}

function AgentCard({ title, icon, role, details }: { title: string, icon: string, role: string, details: string }) {
    return (
        <div className="p-5 rounded-2xl border border-healthcare-border bg-healthcare-card shadow-sm hover:shadow-md transition-all group">
            <div className="flex items-center gap-3 mb-3">
                <div className="h-10 w-10 flex items-center justify-center rounded-full bg-healthcare-surface text-xl group-hover:scale-110 transition-transform">
                    {icon}
                </div>
                <div>
                    <h3 className="font-semibold text-healthcare-heading">{title}</h3>
                    <p className="text-xs text-healthcare-accent font-medium uppercase tracking-wide">{role}</p>
                </div>
            </div>
            <p className="text-sm text-healthcare-muted leading-relaxed">
                {details}
            </p>
        </div>
    )
}
