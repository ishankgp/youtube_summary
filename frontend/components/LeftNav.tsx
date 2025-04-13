"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { ChevronLeft, ChevronRight } from "lucide-react"

type HistoryItem = {
  id: string
  title: string
  timestamp: string
  description: string
}

type LeftNavProps = {
  history: HistoryItem[]
  onSelectHistory: (id: string) => void
}

export default function LeftNav({ history, onSelectHistory }: LeftNavProps) {
  const [isOpen, setIsOpen] = useState(true)

  return (
    <div
      className={`fixed top-0 left-0 h-full bg-white shadow-lg transition-all duration-300 ${isOpen ? "w-64" : "w-16"}`}
    >
      <Button variant="ghost" size="icon" className="absolute top-4 right-4" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? <ChevronLeft /> : <ChevronRight />}
      </Button>
      {isOpen && (
        <div className="p-4 mt-12">
          <h2 className="text-lg font-semibold mb-4">History</h2>
          <ScrollArea className="h-[calc(100vh-8rem)]">
            {history.map((item) => (
              <Button
                key={item.id}
                variant="ghost"
                className="w-full justify-start text-left mb-2"
                onClick={() => onSelectHistory(item.id)}
              >
                <div>
                  <div className="font-medium">{item.title}</div>
                  <div className="text-xs text-gray-500">{item.timestamp}</div>
                </div>
              </Button>
            ))}
          </ScrollArea>
        </div>
      )}
    </div>
  )
}

