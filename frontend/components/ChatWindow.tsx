"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import MessageBubble from "./MessageBubble";
import InputBar from "./InputBar";
import { sendMessageStream, type ChatMessage, type StreamEvent } from "@/lib/api";

interface DisplayMessage {
  role: "user" | "assistant";
  content: string;
  isRedFlag?: boolean;
}

const WELCOME_MESSAGE: DisplayMessage = {
  role: "assistant",
  content:
    "Olá! Sou o **Dr. Silvério**, o teu assistente de fisiologia e saúde. 🩺\n\n" +
    "Posso ajudar-te a compreender como o teu corpo funciona, explicar sintomas " +
    "de forma educativa, e indicar quando deves procurar ajuda médica.\n\n" +
    "Em que posso ajudar-te hoje?",
};

export default function ChatWindow() {
  const [messages, setMessages] = useState<DisplayMessage[]>([WELCOME_MESSAGE]);
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Load history from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("dr-silverio-history");
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          setMessages([WELCOME_MESSAGE, ...parsed]);
        }
      } catch {
        // ignore
      }
    }
  }, []);

  // Save history to localStorage
  useEffect(() => {
    const toSave = messages.slice(1); // skip welcome
    if (toSave.length > 0) {
      localStorage.setItem("dr-silverio-history", JSON.stringify(toSave));
    }
  }, [messages]);

  const handleSend = async (text: string) => {
    const userMsg: DisplayMessage = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    // Build history for API (skip welcome, skip red flag meta)
    const apiHistory: ChatMessage[] = messages
      .slice(1)
      .filter((m) => !m.isRedFlag)
      .map((m) => ({ role: m.role, content: m.content }));

    let assistantContent = "";
    let redFlagContent = "";

    try {
      await sendMessageStream(text, apiHistory, (event: StreamEvent) => {
        if (event.type === "red_flag" && event.content) {
          redFlagContent = event.content;
          setMessages((prev) => [
            ...prev,
            { role: "assistant", content: event.content!, isRedFlag: true },
          ]);
        } else if (event.type === "content" && event.content) {
          assistantContent += event.content;
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last?.role === "assistant" && !last.isRedFlag) {
              return [
                ...prev.slice(0, -1),
                { role: "assistant", content: assistantContent },
              ];
            }
            return [...prev, { role: "assistant", content: assistantContent }];
          });
        } else if (event.type === "error" && event.content) {
          setMessages((prev) => [
            ...prev,
            { role: "assistant", content: `Erro: ${event.content}` },
          ]);
        }
      });
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Peço desculpa, houve um erro de ligação. Verifica se o backend está a correr e tenta novamente.",
        },
      ]);
    }

    setIsLoading(false);
  };

  const handleClear = () => {
    setMessages([WELCOME_MESSAGE]);
    localStorage.removeItem("dr-silverio-history");
  };

  return (
    <div className="flex h-full flex-col">
      {/* Clear button */}
      <div className="flex justify-end px-4 py-1">
        <button
          onClick={handleClear}
          className="text-xs text-gray-400 hover:text-gray-600 transition"
        >
          Limpar conversa
        </button>
      </div>

      {/* Messages */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto chat-scroll px-4 py-4"
      >
        <div className="mx-auto max-w-4xl">
          {messages.map((msg, i) => (
            <MessageBubble
              key={i}
              role={msg.role}
              content={msg.content}
              isRedFlag={msg.isRedFlag}
            />
          ))}
          {isLoading && messages[messages.length - 1]?.role === "user" && (
            <div className="flex items-center gap-2 mb-4">
              <div className="mr-2 flex h-8 w-8 items-center justify-center rounded-full bg-silverio text-white text-sm">
                🩺
              </div>
              <div className="flex gap-1 rounded-2xl bg-white border border-gray-200 px-4 py-3 shadow-sm">
                <span className="typing-dot h-2 w-2 rounded-full bg-gray-400" />
                <span className="typing-dot h-2 w-2 rounded-full bg-gray-400" />
                <span className="typing-dot h-2 w-2 rounded-full bg-gray-400" />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input */}
      <InputBar onSend={handleSend} disabled={isLoading} />
    </div>
  );
}
