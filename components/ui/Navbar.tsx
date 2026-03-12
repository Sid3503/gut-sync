"use client"

import { Button } from "@/components/ui/button"
import Link from "next/link"
import { usePathname } from "next/navigation"

export function Navbar() {
  const pathname = usePathname()

  const isActive = (path: string) => pathname === path

  return (
    <header className="fixed top-4 left-0 right-0 z-50 flex justify-center px-4">
      <div className="flex items-center gap-1 rounded-full border border-healthcare-border/50 bg-healthcare-card/80 px-2 py-2 shadow-lg backdrop-blur-md sm:gap-2">
        <Link href="/">
          <Button
            variant="ghost"
            className={`rounded-full px-3 sm:px-4 transition-all duration-300 hover:scale-105 hover:shadow-sm ${
              isActive("/") 
                ? "text-healthcare-text bg-healthcare-surface/50 font-medium shadow-sm" 
                : "text-healthcare-muted hover:text-healthcare-text hover:bg-healthcare-surface"
            }`}
          >
            <span className="text-lg">🏠</span>
            <span className="hidden sm:inline ml-2">Home</span>
          </Button>
        </Link>
        
        <Link href="/analyze">
          <Button
            variant="ghost"
            className={`rounded-full px-3 sm:px-4 transition-all duration-300 hover:scale-105 hover:shadow-sm ${
              isActive("/analyze") 
                ? "text-healthcare-text bg-healthcare-surface/50 font-medium shadow-sm" 
                : "text-healthcare-muted hover:text-healthcare-text hover:bg-healthcare-surface"
            }`}
          >
            <span className="text-lg">🩺</span>
            <span className="hidden sm:inline ml-2">Analyze</span>
          </Button>
        </Link>
        
        <Link href="/how-it-works">
          <Button
            variant="ghost"
            className={`rounded-full px-3 sm:px-4 transition-all duration-300 hover:scale-105 hover:shadow-sm ${
              isActive("/how-it-works") 
                ? "text-healthcare-text bg-healthcare-surface/50 font-medium shadow-sm" 
                : "text-healthcare-muted hover:text-healthcare-text hover:bg-healthcare-surface"
            }`}
          >
            <span className="text-lg">ℹ️</span>
            <span className="hidden sm:inline ml-2">How It Works</span>
          </Button>
        </Link>
      </div>
    </header>
  )
}
