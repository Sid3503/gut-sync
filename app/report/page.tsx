"use client"

import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import { ArrowLeft, AlertCircle, CheckCircle2, Info, BookOpen, FileDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

export default function ReportPage() {
  const [report, setReport] = useState<string>("")
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const storedReport = sessionStorage.getItem("symptomReport")
    if (storedReport) {
      setReport(storedReport)
    } else {
      // Redirect if no report available
      window.location.href = "/"
    }
    setIsLoading(false)
  }, [])

  const handleDownload = () => {
    const blob = new Blob([report], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `gutsync-report-${new Date().toISOString().split("T")[0]}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const handleNewAnalysis = () => {
    sessionStorage.removeItem("symptomReport")
    window.location.href = "/"
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-healthcare-bg via-healthcare-surface to-healthcare-bg">
        <div className="text-healthcare-muted">Loading your report...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-healthcare-bg via-healthcare-surface to-healthcare-bg">
      {/* Header */}
      <header className="sticky top-0 z-10 border-b border-healthcare-border/50 bg-healthcare-card/80 backdrop-blur-sm">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 py-3 sm:py-4">
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-2 sm:gap-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleNewAnalysis}
                className="text-healthcare-muted hover:text-healthcare-text hover:bg-healthcare-surface text-xs sm:text-sm"
              >
                <ArrowLeft className="mr-1 sm:mr-2 h-3 w-3 sm:h-4 sm:w-4" />
                <span className="hidden sm:inline">New Analysis</span>
                <span className="sm:hidden">New</span>
              </Button>
              <div className="flex items-center gap-2">
                <span className="text-xl sm:text-2xl">🔍</span>
                <span className="text-sm sm:text-base lg:text-lg font-semibold text-healthcare-text">
                  <span className="hidden sm:inline">Your Analysis Report</span>
                  <span className="sm:hidden">Report</span>
                </span>
              </div>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={handleDownload}
              className="border-healthcare-border text-healthcare-text hover:bg-healthcare-surface bg-transparent text-xs sm:text-sm"
            >
              <FileDown className="mr-1 sm:mr-2 h-3 w-3 sm:h-4 sm:w-4" />
              <span className="hidden sm:inline">Download</span>
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-5xl px-4 sm:px-6 py-8 sm:py-10 lg:py-12">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
          {/* Success Banner */}
          <div className="mb-6 sm:mb-8 flex items-start gap-3 sm:gap-4 rounded-2xl border border-healthcare-accent/20 bg-healthcare-accent/5 p-5 sm:p-6">
            <CheckCircle2 className="mt-0.5 h-5 w-5 sm:h-6 sm:w-6 flex-shrink-0 text-healthcare-accent" />
            <div>
              <h2 className="mb-1 text-base sm:text-lg font-semibold text-healthcare-heading">Analysis Complete</h2>
              <p className="text-sm sm:text-base leading-relaxed text-healthcare-muted text-pretty">
                We&apos;ve analyzed your symptoms based on current medical research. Please review the insights below
                and consult with a healthcare professional for proper diagnosis and treatment.
              </p>
            </div>
          </div>

          {/* Report Content */}
          <div className="space-y-4 sm:space-y-6">
            <div className="rounded-2xl border border-healthcare-border bg-healthcare-card p-5 sm:p-6 lg:p-8 shadow-sm">
              <div className="prose prose-healthcare max-w-none prose-headings:text-healthcare-heading prose-p:text-healthcare-text prose-strong:text-healthcare-text prose-li:text-healthcare-text">
                <ReactMarkdown 
                  remarkPlugins={[remarkGfm]}
                  components={{
                    a: ({ node, ...props }) => (
                      <a 
                        {...props} 
                        className="text-healthcare-accent hover:text-healthcare-accent-hover underline decoration-healthcare-accent/50 hover:decoration-healthcare-accent font-medium transition-colors"
                        target="_blank"
                        rel="noopener noreferrer"
                      />
                    ),
                    ul: ({ node, ...props }) => (
                      <ul {...props} className="list-disc list-inside space-y-2 my-4" />
                    ),
                    ol: ({ node, ...props }) => (
                      <ol {...props} className="list-decimal list-inside space-y-2 my-4" />
                    ),
                    li: ({ node, ...props }) => (
                      <li {...props} className="text-healthcare-text" />
                    ),
                    h1: ({ node, ...props }) => (
                      <h1 {...props} className="text-2xl sm:text-3xl font-bold text-healthcare-heading mt-8 mb-4" />
                    ),
                    h2: ({ node, ...props }) => (
                      <h2 {...props} className="text-xl sm:text-2xl font-bold text-healthcare-heading mt-6 mb-3 flex items-center gap-2" />
                    ),
                    h3: ({ node, ...props }) => (
                      <h3 {...props} className="text-lg sm:text-xl font-semibold text-healthcare-heading mt-5 mb-2" />
                    ),
                    p: ({ node, ...props }) => (
                      <p {...props} className="text-healthcare-text leading-relaxed my-3" />
                    ),
                    strong: ({ node, ...props }) => (
                      <strong {...props} className="font-semibold text-healthcare-heading" />
                    ),
                    blockquote: ({ node, ...props }) => (
                      <blockquote {...props} className="border-l-4 border-healthcare-accent/30 pl-4 italic text-healthcare-muted my-4" />
                    ),
                  }}
                >
                  {report}
                </ReactMarkdown>
              </div>
            </div>

            {/* Important Notice */}
            <div className="flex items-start gap-3 sm:gap-4 rounded-2xl border border-healthcare-warning/20 bg-healthcare-warning/5 p-5 sm:p-6">
              <AlertCircle className="mt-0.5 h-5 w-5 sm:h-6 sm:w-6 flex-shrink-0 text-healthcare-warning" />
              <div>
                <h3 className="mb-2 text-sm sm:text-base font-semibold text-healthcare-heading">
                  When to Seek Immediate Medical Attention
                </h3>
                <ul className="space-y-1.5 text-xs sm:text-sm leading-relaxed text-healthcare-muted">
                  <li className="flex items-start gap-2">
                    <span className="mt-0.5 text-healthcare-warning">•</span>
                    <span>Severe abdominal pain that doesn&apos;t improve</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-0.5 text-healthcare-warning">•</span>
                    <span>Blood in stool or vomit</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-0.5 text-healthcare-warning">•</span>
                    <span>Persistent vomiting or inability to keep fluids down</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-0.5 text-healthcare-warning">•</span>
                    <span>Signs of dehydration (dizziness, dark urine, dry mouth)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-0.5 text-healthcare-warning">•</span>
                    <span>Unexplained weight loss or fever</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Next Steps */}
            <div className="rounded-2xl border border-healthcare-border bg-healthcare-surface p-5 sm:p-6 lg:p-8">
              <div className="mb-4 sm:mb-6 flex items-center gap-3">
                <div className="flex h-8 w-8 sm:h-10 sm:w-10 items-center justify-center rounded-xl bg-healthcare-card">
                  <Info className="h-4 w-4 sm:h-5 sm:w-5 text-healthcare-accent" />
                </div>
                <h3 className="text-lg sm:text-xl font-semibold text-healthcare-heading">Recommended Next Steps</h3>
              </div>

              <div className="space-y-3 sm:space-y-4">
                <div className="flex gap-3 sm:gap-4">
                  <div className="flex h-7 w-7 sm:h-8 sm:w-8 flex-shrink-0 items-center justify-center rounded-full bg-healthcare-accent/10 text-xs sm:text-sm font-semibold text-healthcare-accent">
                    1
                  </div>
                  <div>
                    <h4 className="mb-1 text-sm sm:text-base font-semibold text-healthcare-heading">
                      Consult a Healthcare Provider
                    </h4>
                    <p className="text-xs sm:text-sm leading-relaxed text-healthcare-muted text-pretty">
                      Schedule an appointment with your doctor or a gastroenterologist to discuss your symptoms and get
                      a proper diagnosis.
                    </p>
                  </div>
                </div>

                <div className="flex gap-3 sm:gap-4">
                  <div className="flex h-7 w-7 sm:h-8 sm:w-8 flex-shrink-0 items-center justify-center rounded-full bg-healthcare-accent/10 text-xs sm:text-sm font-semibold text-healthcare-accent">
                    2
                  </div>
                  <div>
                    <h4 className="mb-1 text-sm sm:text-base font-semibold text-healthcare-heading">
                      Keep a Symptom Diary
                    </h4>
                    <p className="text-xs sm:text-sm leading-relaxed text-healthcare-muted text-pretty">
                      Track your symptoms, meals, and activities to identify patterns that can help your healthcare
                      provider make an accurate diagnosis.
                    </p>
                  </div>
                </div>

                <div className="flex gap-3 sm:gap-4">
                  <div className="flex h-7 w-7 sm:h-8 sm:w-8 flex-shrink-0 items-center justify-center rounded-full bg-healthcare-accent/10 text-xs sm:text-sm font-semibold text-healthcare-accent">
                    3
                  </div>
                  <div>
                    <h4 className="mb-1 text-sm sm:text-base font-semibold text-healthcare-heading">
                      Review Lifestyle Factors
                    </h4>
                    <p className="text-xs sm:text-sm leading-relaxed text-healthcare-muted text-pretty">
                      Consider diet, stress, sleep, and exercise patterns that may be contributing to your symptoms.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Research Context */}
            <div className="rounded-2xl border border-healthcare-border bg-healthcare-card p-5 sm:p-6 lg:p-8">
              <div className="mb-4 sm:mb-6 flex items-center gap-3">
                <div className="flex h-8 w-8 sm:h-10 sm:w-10 items-center justify-center rounded-xl bg-healthcare-surface">
                  <BookOpen className="h-4 w-4 sm:h-5 sm:w-5 text-healthcare-accent" />
                </div>
                <h3 className="text-lg sm:text-xl font-semibold text-healthcare-heading">About This Analysis</h3>
              </div>

              <p className="mb-3 sm:mb-4 text-sm sm:text-base leading-relaxed text-healthcare-muted text-pretty">
                This analysis is generated using artificial intelligence trained on medical literature and
                evidence-based guidelines. It provides educational information to help you understand potential causes
                and factors related to your symptoms.
              </p>

              <p className="text-sm sm:text-base leading-relaxed text-healthcare-muted text-pretty">
                <strong className="font-semibold text-healthcare-text">Important:</strong> This is not a medical
                diagnosis. Only a qualified healthcare professional can diagnose your condition through proper
                examination and testing. Always consult with your doctor before making any healthcare decisions.
              </p>
            </div>
          </div>

          {/* Action Button */}
          <div className="mt-8 sm:mt-12 text-center">
            <Button
              onClick={handleNewAnalysis}
              size="lg"
              variant="outline"
              className="h-11 sm:h-12 rounded-xl border-healthcare-border px-6 sm:px-8 text-sm sm:text-base font-medium hover:bg-healthcare-surface bg-transparent text-healthcare-text"
            >
              Analyze New Symptoms
            </Button>
          </div>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="border-t border-healthcare-border/50 bg-healthcare-card/50 py-6 sm:py-8">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 text-center text-xs text-healthcare-muted">
          <p className="leading-relaxed">
            Medical Disclaimer: This tool is for informational purposes only and does not provide medical advice,
            diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with
            any questions regarding a medical condition. Never disregard professional medical advice or delay seeking it
            because of something you have read on this website.
          </p>
        </div>
      </footer>
    </div>
  )
}
