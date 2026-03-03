"use client";

import ReactMarkdown from "react-markdown";

interface MessageBubbleProps {
  role: "user" | "assistant";
  content: string;
  isRedFlag?: boolean;
}

export default function MessageBubble({
  role,
  content,
  isRedFlag,
}: MessageBubbleProps) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      {!isUser && (
        <div className="mr-2 mt-1 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-silverio text-white text-sm">
          🩺
        </div>
      )}
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-silverio text-white rounded-br-md"
            : isRedFlag
              ? "bg-red-50 border border-red-200 text-gray-800 rounded-bl-md"
              : "bg-white border border-gray-200 text-gray-800 rounded-bl-md shadow-sm"
        }`}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap">{content}</p>
        ) : (
          <div className="markdown-body prose prose-sm max-w-none">
            <ReactMarkdown>{content}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}
