"use client"

import { useState, useEffect, useRef } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { ArrowUp, Check, Sparkles, Zap, Activity, Microscope, ArrowRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { PdfUploadCard } from "@/components/ui/PdfUploadCard"
import { ImageUploadCard } from "@/components/ui/ImageUploadCard"
import { TextBlurLoader } from "@/components/ui/TextBlurLoader"
import { SkeletonLoader } from "@/components/ui/SkeletonLoader"
import { LiveReportBuilder } from "@/components/ui/LiveReportBuilder"
import { Navbar } from "@/components/ui/Navbar"
import { cn } from "@/lib/utils"

// Suggestions focusing on capabilities with rich examples
const suggestions = [
  {
    icon: <Zap className="w-5 h-5 text-amber-500" />,
    title: "Analyze Symptoms",
    description: "Describe what you're feeling for an instant assessment",
    prompt: "I've been experiencing a sharp pain in my lower right abdomen for about 2 days. It gets worse when I walk or cough. I also feel a bit nauseous and haven't had much appetite."
  },
  {
    icon: <Activity className="w-5 h-5 text-emerald-500" />,
    title: "Check Food Sensitivities",
    description: "Find correlations between your diet and discomfort",
    prompt: "Every time I drink milk or eat ice cream, I get bloated and gassy within 30 minutes. It's really uncomfortable and sometimes gives me cramps. I think I might be lactose intolerant."
  },
  {
    icon: <Microscope className="w-5 h-5 text-blue-500" />,
    title: "Interpret Lab Results",
    description: "Upload your medical reports for a simplified explanation",
    prompt: "I just got my blood work back and my Vitamin D levels are low (18 ng/mL). Can you explain what this means and what supplements I should take? I'm also feeling tired lately.",
    action: "upload" 
  }
]

function generateUUID() {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

// Analysis steps that match ACTUAL backend node execution
const analysisSteps = [
  { 
    id: 1, 
    label: "Intake & Normalization", 
    description: "Parsing your description into structured clinical data",
    icon: "📥",
    color: "from-gray-500/20 to-neutral-500/20",
    minDuration: 4000 
  },
  { 
    id: 2, 
    label: "Symptom Analysis", 
    description: "Identifying patterns, correlations, and body systems involved",
    icon: "🔬",
    color: "from-zinc-500/20 to-stone-500/20",
    minDuration: 5000 
  },
  { 
    id: 3, 
    label: "Root Cause Investigation", 
    description: "Exploring possible physiological explanations for your symptoms",
    icon: "🔍",
    color: "from-slate-500/20 to-gray-500/20",
    minDuration: 6000 
  },
  { 
    id: 4, 
    label: "Severity Assessment", 
    description: "Evaluating urgency and impact on your daily life",
    icon: "📊",
    color: "from-neutral-500/20 to-zinc-500/20",
    minDuration: 3000 
  },
  { 
    id: 5, 
    label: "Research Lookup", 
    description: "Querying PubMed, NIH, CDC and clinical databases",
    icon: "📚",
    color: "from-stone-500/20 to-slate-500/20",
    minDuration: 8000 
  },
  { 
    id: 6, 
    label: "Relief Strategies", 
    description: "Formulating personalized recommendations based on your profile",
    icon: "💊",
    color: "from-gray-600/20 to-neutral-600/20",
    minDuration: 5000 
  },
  { 
    id: 7, 
    label: "Safety Check", 
    description: "Scanning for warning signs that may require medical attention",
    icon: "🚩",
    color: "from-zinc-600/20 to-stone-600/20",
    minDuration: 4000 
  },
  { 
    id: 8, 
    label: "Report Generation", 
    description: "Synthesizing all findings into your personalized health report",
    icon: "📝",
    color: "from-slate-600/20 to-gray-600/20",
    minDuration: 8000 
  },
]

export default function AnalyzePage() {
  const [symptoms, setSymptoms] = useState("")
  const [pdfFile, setPdfFile] = useState<File | null>(null)
  const [imageFiles, setImageFiles] = useState<File[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [completedSteps, setCompletedSteps] = useState<number[]>([])
  const [isTransitioning, setIsTransitioning] = useState(false)
  const [apiComplete, setApiComplete] = useState(false)
  const [showFinalLoading, setShowFinalLoading] = useState(false)
  const [elapsedTime, setElapsedTime] = useState(0)
  const apiResultRef = useRef<any>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Focus textarea on mount
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.focus()
    }
  }, [])

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
        textareaRef.current.style.height = 'inherit';
        textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 400)}px`;
    }
  }, [symptoms]);

  // Timer to show elapsed time
  useEffect(() => {
    if (!isAnalyzing) return
    const interval = setInterval(() => {
      setElapsedTime(prev => prev + 1)
    }, 1000)
    return () => clearInterval(interval)
  }, [isAnalyzing])

  // Step progression during analysis
  useEffect(() => {
    if (!isAnalyzing || apiComplete) return
    
    // Calculate total steps dynamically
    let totalSteps = analysisSteps.length
    if (pdfFile) totalSteps++
    if (imageFiles.length > 0) totalSteps++
    
    if (currentStep >= totalSteps) return

    const timer = setTimeout(() => {
      setCompletedSteps(prev => [...prev, currentStep])
      if (currentStep < totalSteps - 1) {
        setCurrentStep(prev => prev + 1)
      }
    }, 4000) // Generic duration for smoothness

    return () => clearTimeout(timer)
  }, [isAnalyzing, currentStep, apiComplete, pdfFile, imageFiles.length])

  // When API completes, finish all steps and transition
  useEffect(() => {
    if (apiComplete && apiResultRef.current) {
      let totalSteps = analysisSteps.length
      if (pdfFile) totalSteps++
      if (imageFiles.length > 0) totalSteps++
      const allSteps = Array.from({ length: totalSteps }, (_, i) => i)
      setCompletedSteps(allSteps)
      setCurrentStep(totalSteps)

      setTimeout(async () => {
        setShowFinalLoading(true)
        await new Promise(resolve => setTimeout(resolve, 3000)) // Show loaders for 3 seconds
        setIsTransitioning(true)
        await new Promise(resolve => setTimeout(resolve, 600))
        sessionStorage.setItem("symptomReport", apiResultRef.current)
        window.location.href = "/report"
      }, 800)
    }
  }, [apiComplete, pdfFile, imageFiles.length])

  const handleSubmit = async () => {
    if (symptoms.trim().length < 5) return

    setIsAnalyzing(true)
    setCurrentStep(0)
    setCompletedSteps([])
    setApiComplete(false)
    setElapsedTime(0)

    try {
      const formData = new FormData()
      formData.append("user_id", generateUUID())
      formData.append("message", symptoms)
      formData.append("source", "web")
      if (pdfFile) {
        formData.append("file", pdfFile)
      }
      // Add image files
      if (imageFiles.length > 0) {
        imageFiles.forEach((file) => {
          formData.append("image_files", file)
        })
      }

      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error("Analysis failed")
      }

      const data = await response.json()
      apiResultRef.current = data.report
      setApiComplete(true)

    } catch (error) {
      console.error("Analysis error:", error)
      alert("Unable to complete analysis. Please try again.")
      setIsAnalyzing(false)
      setCurrentStep(0)
      setCompletedSteps([])
    }
  }

  const handleSuggestionClick = (suggestion: any) => {
    if (suggestion.action === 'upload') {
       // Ideally we would trigger the file input here, but for now let's just prompt text
       setSymptoms(suggestion.prompt)
    } else {
       setSymptoms(suggestion.prompt)
    }
    textareaRef.current?.focus()
  }

  // Analysis Screen - Card-based Animation
  if (isAnalyzing) {
    // Dynamic steps based on PDF and Image presence
    const activeSteps = [...analysisSteps]
    let insertIndex = 1 // Start after Intake (index 0)
    
    if (pdfFile) {
       // Insert after Intake (index 0)
       activeSteps.splice(insertIndex, 0, {
          id: 99,
          label: "Document Review",
          description: "Carefully reviewing the information you shared",
          icon: "📄",
          color: "from-blue-600/20 to-indigo-600/20",
          minDuration: 4000
       })
       insertIndex++ // Move insert position for next step
    }
    
    if (imageFiles.length > 0) {
       // Insert after Document Review (if exists) or after Intake
       activeSteps.splice(insertIndex, 0, {
          id: 98,
          label: "Image Analysis",
          description: "Processing and analyzing your medical images",
          icon: "📸",
          color: "from-purple-600/20 to-pink-600/20",
          minDuration: 4000
       })
    }
    
    const currentStepData = activeSteps[Math.min(currentStep, activeSteps.length - 1)]
    
    // Final Loading Screen - Show after all steps complete
    if (showFinalLoading) {
      return (
        <>
        <Navbar />
        <motion.div 
          className="flex min-h-screen flex-col items-center justify-center pt-24 pb-8 bg-gradient-to-br from-healthcare-bg via-healthcare-surface to-healthcare-bg px-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: isTransitioning ? 0 : 1 }}
          transition={{ duration: 0.6 }}
        >
          {/* Animated Background */}
          <div className="fixed inset-0 overflow-hidden pointer-events-none">
            <motion.div
              className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-gradient-to-br from-healthcare-accent/10 via-primary-200/15 to-transparent blur-3xl"
              animate={{
                scale: [1, 1.2, 1],
                rotate: [0, 180, 360],
              }}
              transition={{
                duration: 20,
                repeat: Infinity,
                ease: "linear",
              }}
            />
          </div>

          <div className="relative z-10 w-full max-w-4xl">
            {/* Header */}
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-12 text-center"
            >
              <h1 className="text-2xl sm:text-3xl font-bold text-healthcare-heading mb-2">
                Compiling Your Report
              </h1>
              <p className="text-healthcare-muted text-sm sm:text-base">
                Synthesizing all findings into your personalized health analysis
              </p>
            </motion.div>

            {/* Text Blur Loader - Shows first */}
            <AnimatePresence mode="wait">
              <motion.div
                key="text-blur"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.5 }}
                className="mb-12 flex justify-center"
              >
                <TextBlurLoader />
              </motion.div>
            </AnimatePresence>

            {/* Skeleton Loader - Shows after text blur */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5, duration: 0.6 }}
              className="rounded-3xl border border-healthcare-border bg-healthcare-card/80 backdrop-blur-sm shadow-xl overflow-hidden"
            >
              <SkeletonLoader />
            </motion.div>

            {/* Progress Indicator */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
              className="mt-8 flex items-center justify-center gap-2"
            >
              <motion.div 
                className="w-2 h-2 rounded-full bg-healthcare-accent"
                animate={{ opacity: [1, 0.3, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
              />
              <span className="text-sm text-healthcare-muted">
                Finalizing your personalized health report...
              </span>
            </motion.div>
          </div>
        </motion.div>
        </>
      )
    }
    
    return (
      <>
      <Navbar />
      <motion.div 
        className="flex min-h-screen flex-col items-center justify-center pt-24 pb-8 bg-gradient-to-br from-healthcare-bg via-healthcare-surface to-healthcare-bg px-4"
        animate={{ opacity: isTransitioning ? 0 : 1 }}
        transition={{ duration: 0.6 }}
      >
        {/* Animated Background */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <motion.div
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-gradient-to-br from-healthcare-accent/10 via-primary-200/15 to-transparent blur-3xl"
            animate={{
              scale: [1, 1.2, 1],
              rotate: [0, 180, 360],
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "linear",
            }}
          />
        </div>

        <div className="relative z-10 w-full max-w-7xl grid lg:grid-cols-2 gap-12 lg:gap-24 px-4 sm:px-8 items-start">
          <div className="w-full flex flex-col items-center">
            {/* Header */}
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-8"
            >
              <h1 className="text-2xl sm:text-3xl font-bold text-healthcare-heading mb-2">
                Analyzing Your Symptoms
              </h1>
              <p className="text-healthcare-muted text-sm sm:text-base">
                Our AI agents are working together
              </p>
            </motion.div>

          {/* Progress Indicator */}
          <div className="mb-6 flex items-center justify-center gap-2">
            {activeSteps.map((_, index) => (
              <motion.div
                key={index}
                className={`h-2 rounded-full transition-all duration-500 ${
                  completedSteps.includes(index)
                    ? "w-8 bg-status-success"
                    : index === currentStep
                      ? "w-8 bg-healthcare-accent"
                      : "w-2 bg-healthcare-border"
                }`}
                initial={{ scale: 0.8 }}
                animate={{ 
                  scale: index === currentStep ? [1, 1.1, 1] : 1,
                }}
                transition={{ 
                  duration: 1, 
                  repeat: index === currentStep ? Infinity : 0 
                }}
              />
            ))}
          </div>

          {/* Current Step Card */}
          <AnimatePresence mode="wait">
            <motion.div
              key={currentStep}
              initial={{ opacity: 0, y: 30, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -30, scale: 0.95 }}
              transition={{ duration: 0.4, ease: "easeOut" }}
              className={`relative rounded-3xl border border-healthcare-border/50 bg-gradient-to-br ${currentStepData.color} backdrop-blur-sm p-8 sm:p-10 shadow-xl overflow-hidden w-full`}
            >
              {/* Background Pattern */}
              <div className="absolute inset-0 opacity-30">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(255,255,255,0.8),transparent_70%)]" />
              </div>

              {/* Card Content */}
              <div className="relative z-10">
                {/* Icon */}
                <motion.div
                  className="mx-auto mb-6 w-20 h-20 rounded-2xl bg-white/80 backdrop-blur-sm shadow-lg flex items-center justify-center text-4xl"
                  animate={{ 
                    rotate: [0, 5, -5, 0],
                    scale: [1, 1.05, 1],
                  }}
                  transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                >
                  {currentStepData.icon}
                </motion.div>

                {/* Step Counter */}
                <div className="mb-4 text-sm font-medium text-healthcare-muted">
                  Step {currentStep + 1} of {activeSteps.length}
                </div>

                {/* Title */}
                <h2 className="text-xl sm:text-2xl font-bold text-healthcare-heading mb-3">
                  {currentStepData.label}
                </h2>

                {/* Description */}
                <p className="text-healthcare-muted text-sm sm:text-base leading-relaxed mb-6">
                  {currentStepData.description}
                </p>

                {/* Loading Indicator */}
                <div className="flex items-center justify-center gap-3">
                  <TextBlurLoader text="PROCESSING" className="text-sm font-bold text-healthcare-accent" />
                </div>
              </div>

              {/* Animated Border Glow */}
              <motion.div
                className="absolute inset-0 rounded-3xl border-2 border-healthcare-accent/30"
                animate={{ opacity: [0.3, 0.6, 0.3] }}
                transition={{ duration: 2, repeat: Infinity }}
              />
            </motion.div>
          </AnimatePresence>

          {/* Timer & Status */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="mt-8 flex items-center justify-center gap-4 text-sm text-healthcare-muted"
          >
            <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-healthcare-surface/50 border border-healthcare-border/30">
              <motion.div 
                className="w-2 h-2 rounded-full bg-healthcare-accent"
                animate={{ opacity: [1, 0.3, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
              />
              <span className="font-mono">
                {Math.floor(elapsedTime / 60).toString().padStart(2, '0')}:{(elapsedTime % 60).toString().padStart(2, '0')}
              </span>
            </div>
            <span className="text-healthcare-muted/60">•</span>
            <span>{completedSteps.length} of {activeSteps.length} complete</span>
          </motion.div>

          {/* Completed Steps Pills */}
          {completedSteps.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-6 flex flex-wrap justify-center gap-2"
            >
              {completedSteps.map((stepIndex) => (
                <motion.div
                  key={stepIndex}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-status-success-bg border border-status-success-border text-xs"
                >
                  <Check className="w-3 h-3 text-status-success" />
                  <span className="text-status-success font-medium">{activeSteps[stepIndex]?.label}</span>
                </motion.div>
              ))}
            </motion.div>
          )}
        </div>

        {/* Live Report Builder Widget - Desktop */}
        <div className="hidden lg:flex w-full h-full items-start pt-8">
          <LiveReportBuilder 
            completedSteps={completedSteps} 
            totalSteps={activeSteps.length} 
            currentStep={currentStep} 
          />
        </div>
        
        {/* Live Report Builder Widget - Mobile */}
        <div className="block lg:hidden w-full max-w-[340px] mx-auto">
          <LiveReportBuilder 
            completedSteps={completedSteps} 
            totalSteps={activeSteps.length} 
            currentStep={currentStep} 
          />
        </div>
      </div>
      </motion.div>
      </>
    )
  }

  // Input Screen (New Design)
  return (
    <div className="min-h-screen bg-healthcare-bg flex flex-col">
      <Navbar />
      
      <main className="flex-1 flex flex-col items-center justify-start pt-24 px-4 md:px-6 relative overflow-hidden pb-12">
        {/* Background Gradients */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
            <div className="absolute top-[20%] right-[10%] w-[500px] h-[500px] bg-healthcare-accent/5 rounded-full blur-3xl opacity-50" />
            <div className="absolute bottom-[10%] left-[10%] w-[400px] h-[400px] bg-blue-500/5 rounded-full blur-3xl opacity-50" />
        </div>

        <div className="w-full max-w-5xl relative z-10 flex flex-col items-center gap-8 md:gap-10">
            
            {/* Header Section */}
            <motion.div 
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="text-center space-y-4"
            >
                {/* Badge removed as requested */}
                <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-healthcare-heading to-healthcare-heading/70 tracking-tight">
                    How can I help you today?
                </h1>
                <p className="text-lg text-healthcare-muted max-w-2xl mx-auto leading-relaxed">
                    Describe your symptoms, upload medical records, or analyze recent health patterns.
                </p>
            </motion.div>

            {/* Main Input Area (Expanded) */}
            <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2, duration: 0.5 }}
                className="w-full"
            >
                <div className="relative rounded-3xl bg-healthcare-surface border border-healthcare-border/60 shadow-xl shadow-healthcare-accent/5 overflow-hidden transition-all focus-within:ring-2 focus-within:ring-healthcare-accent/20 focus-within:border-healthcare-accent/40 min-h-[550px] flex flex-col justify-between">
                    <Textarea
                        ref={textareaRef}
                        value={symptoms}
                        onChange={(e) => setSymptoms(e.target.value)}
                        placeholder="Describe your symptoms deeply..."
                        className="w-full flex-1 p-8 text-xl bg-transparent border-0 focus-visible:ring-0 resize-none data-[placeholder]:text-healthcare-muted/50 min-h-[200px]"
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSubmit();
                            }
                        }}
                    />

                    {/* Suggestion Cards (Inside Input Area) - Restyled */}
                     <AnimatePresence>
                        {symptoms.length === 0 && (
                            <motion.div 
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                className="px-6 pb-6 grid grid-cols-1 md:grid-cols-3 gap-4"
                            >
                                {suggestions.map((item, i) => (
                                    <button
                                        key={i}
                                        onClick={() => handleSuggestionClick(item)}
                                        className="flex flex-col items-start text-left p-4 rounded-xl border border-healthcare-border bg-healthcare-bg/30 hover:bg-healthcare-card hover:border-healthcare-accent/50 hover:shadow-md transition-all duration-300 group"
                                    >
                                        <div className="flex items-center gap-3 mb-2 w-full">
                                            <div className="p-2 rounded-full bg-white shadow-sm ring-1 ring-black/5 group-hover:scale-110 transition-transform">
                                                {item.icon}
                                            </div>
                                            <span className="font-semibold text-healthcare-heading text-sm group-hover:text-healthcare-accent transition-colors">
                                                {item.title}
                                            </span>
                                        </div>
                                        <p className="text-xs text-healthcare-muted leading-relaxed line-clamp-3 pl-1">
                                            {item.description}
                                        </p>
                                    </button>
                                ))}
                            </motion.div>
                        )}
                    </AnimatePresence>
                    
                    {/* Action Bar */}
                    <div className="flex items-center justify-between px-6 py-4 bg-healthcare-surface/50 border-t border-healthcare-border/40 backdrop-blur-sm mt-auto">
                        <div className="flex items-center gap-3">
                           <PdfUploadCard 
                                onFileSelect={setPdfFile} 
                                className="h-10 px-4 text-sm bg-healthcare-bg hover:bg-healthcare-card active:scale-95 transition-all shadow-sm border-healthcare-border/50"
                            />
                           <ImageUploadCard 
                                onFilesSelect={setImageFiles} 
                                maxFiles={5}
                                className="h-10 px-4 text-sm bg-healthcare-bg hover:bg-healthcare-card active:scale-95 transition-all shadow-sm border-healthcare-border/50"
                            />
                        </div>

                        <Button
                            onClick={handleSubmit}
                            disabled={!symptoms.trim() && !pdfFile && imageFiles.length === 0}
                            size="icon"
                            className={cn(
                                "h-12 w-12 rounded-2xl transition-all duration-300 shadow-sm",
                                symptoms.trim().length > 0 || pdfFile || imageFiles.length > 0
                                  ? "bg-healthcare-accent text-white hover:bg-healthcare-accent-hover hover:scale-105 hover:shadow-md" 
                                  : "bg-healthcare-border/50 text-healthcare-muted cursor-not-allowed"
                            )}
                        >
                            <ArrowUp className="w-6 h-6" />
                        </Button>
                    </div>
                </div>
                
                {/* File Previews (Below Input) */}
                <AnimatePresence>
                    {(pdfFile || imageFiles.length > 0) && (
                        <motion.div 
                            initial={{ opacity: 0, height: 0 }} 
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="mt-4 flex flex-wrap gap-2 px-1"
                        >
                            {/* Handled mostly by component internal state display, but we can add summary here if needed */}
                        </motion.div>
                    )}
                </AnimatePresence>
            </motion.div>

            {/* Footer */}
            <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 }} 
                className="text-xs text-healthcare-muted/60 text-center mt-8 max-w-md"
            >
                GutSync AI can make mistakes. Please double check important information.
            </motion.p>
        </div>
      </main>
    </div>
  )
}
