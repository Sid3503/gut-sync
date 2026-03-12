"use client"

import { useState, useCallback, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { FileText, Upload, X, Check, File } from "lucide-react"
import { useDropzone } from "react-dropzone"
import { cn } from "@/lib/utils"

interface PdfUploadCardProps {
  onFileSelect: (file: File | null) => void
  disabled?: boolean
  className?: string
}

export function PdfUploadCard({ onFileSelect, disabled = false, className }: PdfUploadCardProps) {
  const [file, setFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [pendingFile, setPendingFile] = useState<File | null>(null)
  
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const selectedFile = acceptedFiles[0]
      setPendingFile(selectedFile)
      setIsUploading(true)
      setProgress(0)

      // Simulate upload progress
      const interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 100) {
            clearInterval(interval)
            return 100
          }
          return prev + 10 
        })
      }, 50)
    }
  }, [])

  // Handle upload completion side-effects
  useEffect(() => {
    if (progress >= 100 && isUploading && pendingFile) {
        setFile(pendingFile)
        onFileSelect(pendingFile)
        setIsUploading(false)
        setPendingFile(null)
    }
  }, [progress, isUploading, pendingFile, onFileSelect])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    disabled: disabled || isUploading
  })

  // Silent update of parent state if file removed (though parent handles setFile from prop, we want to clear local too)
  const removeFile = (e: React.MouseEvent) => {
    e.stopPropagation()
    setFile(null)
    onFileSelect(null)
    setProgress(0)
  }

  return (
    <div className="inline-block">
      <AnimatePresence mode="wait">
        {!file ? (
           <motion.div
            key="upload"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            {...(getRootProps() as any)}
            className={cn(
              "relative inline-flex items-center gap-2 px-4 py-2 rounded-full border border-healthcare-border bg-healthcare-surface hover:bg-healthcare-surface/80 hover:border-healthcare-accent cursor-pointer transition-all duration-200 shadow-sm overflow-hidden",
              isDragActive && "border-healthcare-accent ring-2 ring-healthcare-accent/20",
              (disabled || isUploading) && "cursor-not-allowed",
              disabled && "opacity-50 pointer-events-none",
              className
            )}
          >
            {/* Progress Bar Background */}
            {isUploading && (
              <motion.div 
                className="absolute inset-0 bg-healthcare-accent/20 z-0"
                initial={{ width: "0%" }}
                animate={{ width: `${progress}%` }}
                transition={{ ease: "linear", duration: 0.05 }}
              />
            )}

            <input {...getInputProps()} />
            <div className="relative z-10 flex items-center gap-2 text-healthcare-text">
               {isUploading ? (
                 <>
                    <motion.div animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity, ease: "linear" }}>
                       <Upload className="w-4 h-4 text-healthcare-accent" />
                    </motion.div>
                    <span className="text-sm font-medium">Attaching... {progress}%</span>
                 </>
               ) : (
                 <>
                   <svg 
                     width="16" 
                     height="16" 
                     viewBox="0 0 24 24" 
                     fill="none" 
                     stroke="currentColor" 
                     strokeWidth="2" 
                     strokeLinecap="round" 
                     strokeLinejoin="round"
                     className="w-4 h-4 text-healthcare-muted"
                   >
                      <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48" />
                   </svg>
                   <span className="text-sm font-medium">Attach PDF</span>
                 </>
               )}
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="file"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-healthcare-accent/30 bg-healthcare-accent/10 pr-2"
          >
            <div className="flex items-center gap-2">
               <File className="w-3.5 h-3.5 text-healthcare-accent" />
               <span className="text-sm font-medium text-healthcare-heading max-w-[150px] truncate">
                 {file.name}
               </span>
            </div>

            <button
               onClick={removeFile}
               className="p-1 rounded-full hover:bg-healthcare-accent/20 text-healthcare-muted hover:text-red-500 transition-colors"
               disabled={disabled}
            >
               <X className="w-3.5 h-3.5" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
