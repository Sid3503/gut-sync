"use client"

import { motion } from "framer-motion"

interface TextBlurLoaderProps {
  text?: string
  className?: string
}

export function TextBlurLoader({ text = "LOADING", className = "" }: TextBlurLoaderProps) {
  return (
    <div className={`flex items-center justify-center gap-[2px] ${className}`}>
      {text.split("").map((char, index) => (
        <motion.span
          key={index}
          className="font-bold inline-block"
          animate={{
            opacity: [0.3, 1, 0.3],
            filter: [
              "blur(2px)",
              "blur(0px)",
              "blur(2px)"
            ],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            delay: index * 0.1,
            ease: "easeInOut"
          }}
        >
          {char === " " ? "\u00A0" : char}
        </motion.span>
      ))}
    </div>
  )
}
