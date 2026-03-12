"use client"

import { useState, useCallback, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Image, Upload, X, Camera } from "lucide-react"
import { useDropzone } from "react-dropzone"
import { cn } from "@/lib/utils"

interface ImageUploadCardProps {
  onFilesSelect: (files: File[]) => void
  disabled?: boolean
  maxFiles?: number
  className?: string
}

export function ImageUploadCard({ onFilesSelect, disabled = false, maxFiles = 5, className }: ImageUploadCardProps) {
  const [files, setFiles] = useState<File[]>([])
  const [isUploading, setIsUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [pendingFiles, setPendingFiles] = useState<File[]>([])
  
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const newFiles = acceptedFiles.slice(0, maxFiles - files.length)
      setPendingFiles(newFiles)
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
  }, [files.length, maxFiles])

  // Handle upload completion side-effects
  useEffect(() => {
    if (progress >= 100 && isUploading && pendingFiles.length > 0) {
        const updatedFiles = [...files, ...pendingFiles]
        setFiles(updatedFiles)
        onFilesSelect(updatedFiles)
        setIsUploading(false)
        setPendingFiles([])
    }
  }, [progress, isUploading, pendingFiles, files, onFilesSelect])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'image/webp': ['.webp'],
      'image/heic': ['.heic']
    },
    maxFiles: maxFiles - files.length,
    disabled: disabled || isUploading || files.length >= maxFiles,
    multiple: true
  })

  const removeFile = (index: number, e: React.MouseEvent) => {
    e.stopPropagation()
    const updatedFiles = files.filter((_, i) => i !== index)
    setFiles(updatedFiles)
    onFilesSelect(updatedFiles)
  }

  return (
    <div className="inline-flex flex-wrap items-center gap-2">
      <AnimatePresence mode="wait">
        {files.length < maxFiles && (
           <motion.div
            key="upload"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            {...(getRootProps() as any)}
            className={cn(
              "relative inline-flex items-center gap-2 px-4 py-2 rounded-full border border-healthcare-border bg-healthcare-surface hover:bg-healthcare-surface/80 hover:border-healthcare-accent cursor-pointer transition-all duration-200 shadow-sm overflow-hidden",
              isDragActive && "border-healthcare-accent ring-2 ring-healthcare-accent/20",
              (disabled || isUploading || files.length >= maxFiles) && "cursor-not-allowed",
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
                    <span className="text-sm font-medium">Uploading... {progress}%</span>
                 </>
               ) : (
                 <>
                   <Camera className="w-4 h-4 text-healthcare-muted" />
                   <span className="text-sm font-medium">
                     {files.length === 0 ? "Add Images (optional)" : `Add more (${files.length}/${maxFiles})`}
                   </span>
                 </>
               )}
            </div>
          </motion.div>
        )}

        {/* Display uploaded files as small badges */}
        {files.map((file, index) => (
          <motion.div
            key={`${file.name}-${index}`}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-healthcare-accent/30 bg-healthcare-accent/10 pr-2"
          >
            <div className="flex items-center gap-2">
               <Image className="w-3.5 h-3.5 text-healthcare-accent" />
               <span className="text-xs font-medium text-healthcare-heading max-w-[80px] truncate">
                 {file.name}
               </span>
            </div>

            <button
               onClick={(e) => removeFile(index, e)}
               className="p-1 rounded-full hover:bg-healthcare-accent/20 text-healthcare-muted hover:text-red-500 transition-colors"
               disabled={disabled}
            >
               <X className="w-3.5 h-3.5" />
            </button>
          </motion.div>
        ))}
      </AnimatePresence>
      
      {/* Privacy reassurance (shown when files exist) */}
      {files.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="w-full mt-1 flex items-center gap-1.5 text-xs text-healthcare-muted/70"
        >
          <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          <span>Images processed securely and never stored</span>
        </motion.div>
      )}
    </div>
  )
}
