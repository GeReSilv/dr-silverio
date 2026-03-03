"use client";

import Link from "next/link";

export default function Header() {
  return (
    <header className="sticky top-0 z-10 border-b border-gray-200 bg-white/80 backdrop-blur-sm">
      <div className="mx-auto flex max-w-4xl items-center gap-3 px-4 py-3">
        <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-silverio text-white text-xl">
            🩺
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900 leading-tight">
              Dr. Silvério
            </h1>
            <p className="text-xs text-gray-500">
              Assistente de Fisiologia
            </p>
          </div>
        </Link>
        <div className="ml-auto">
          <span className="inline-flex items-center gap-1 rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-700">
            <span className="h-1.5 w-1.5 rounded-full bg-green-500" />
            Online
          </span>
        </div>
      </div>
    </header>
  );
}
