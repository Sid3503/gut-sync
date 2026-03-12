"use client"

import { motion } from "framer-motion"

export function SkeletonLoader() {
  return (
    <div className="w-full max-w-2xl mx-auto space-y-6 p-6">
      {/* Header Skeleton */}
      <div className="space-y-3">
        <motion.div
          className="h-8 bg-gradient-to-r from-healthcare-border via-healthcare-surface to-healthcare-border rounded-lg"
          animate={{
            backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "linear"
          }}
          style={{
            backgroundSize: "200% 100%"
          }}
        />
        <motion.div
          className="h-4 w-3/4 bg-gradient-to-r from-healthcare-border via-healthcare-surface to-healthcare-border rounded-lg"
          animate={{
            backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "linear",
            delay: 0.1
          }}
          style={{
            backgroundSize: "200% 100%"
          }}
        />
      </div>

      {/* Content Blocks */}
      {[1, 2, 3].map((block, blockIndex) => (
        <div key={block} className="space-y-3">
          {/* Section Title */}
          <motion.div
            className="h-6 w-1/3 bg-gradient-to-r from-healthcare-border via-healthcare-surface to-healthcare-border rounded-lg"
            animate={{
              backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "linear",
              delay: blockIndex * 0.2
            }}
            style={{
              backgroundSize: "200% 100%"
            }}
          />
          
          {/* Content Lines */}
          <div className="space-y-2">
            {[1, 2, 3].map((line, lineIndex) => (
              <motion.div
                key={line}
                className={`h-4 bg-gradient-to-r from-healthcare-border via-healthcare-surface to-healthcare-border rounded-lg ${
                  lineIndex === 2 ? 'w-5/6' : 'w-full'
                }`}
                animate={{
                  backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "linear",
                  delay: blockIndex * 0.2 + lineIndex * 0.1
                }}
                style={{
                  backgroundSize: "200% 100%"
                }}
              />
            ))}
          </div>
        </div>
      ))}

      {/* Image Placeholder */}
      <motion.div
        className="h-48 bg-gradient-to-r from-healthcare-border via-healthcare-surface to-healthcare-border rounded-xl"
        animate={{
          backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "linear",
          delay: 0.6
        }}
        style={{
          backgroundSize: "200% 100%"
        }}
      />
    </div>
  )
}
