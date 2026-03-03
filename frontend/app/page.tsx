import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-blue-50 to-white px-4">
      <div className="max-w-2xl text-center">
        {/* Avatar */}
        <div className="mx-auto mb-6 flex h-28 w-28 items-center justify-center rounded-full bg-silverio text-white text-5xl shadow-lg">
          🩺
        </div>

        <h1 className="mb-2 text-4xl font-bold text-gray-900">
          Dr. Silvério
        </h1>
        <p className="mb-1 text-xl text-silverio font-medium">
          Assistente de Fisiologia e Saúde
        </p>
        <p className="mb-8 text-gray-500">
          Baseado no Tortora — Principles of Anatomy and Physiology
        </p>

        <div className="mb-8 space-y-3 text-left bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h2 className="text-lg font-semibold text-gray-800 text-center mb-4">
            O que posso fazer por ti?
          </h2>
          <div className="grid gap-3 sm:grid-cols-2">
            <div className="flex items-start gap-3 p-3 rounded-lg bg-blue-50">
              <span className="text-2xl">🔬</span>
              <div>
                <p className="font-medium text-gray-800">Explicar Fisiologia</p>
                <p className="text-sm text-gray-600">
                  Mecanismos do corpo humano de forma acessível
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 rounded-lg bg-blue-50">
              <span className="text-2xl">💡</span>
              <div>
                <p className="font-medium text-gray-800">Tirar Dúvidas</p>
                <p className="text-sm text-gray-600">
                  Sobre sintomas, anatomia, e bem-estar
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 rounded-lg bg-blue-50">
              <span className="text-2xl">📚</span>
              <div>
                <p className="font-medium text-gray-800">Base Científica</p>
                <p className="text-sm text-gray-600">
                  Referências do Tortora e evidência científica
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 rounded-lg bg-blue-50">
              <span className="text-2xl">⚠️</span>
              <div>
                <p className="font-medium text-gray-800">Sinais de Alerta</p>
                <p className="text-sm text-gray-600">
                  Identificar quando procurar ajuda médica
                </p>
              </div>
            </div>
          </div>
        </div>

        <Link
          href="/chat"
          className="inline-flex items-center gap-2 rounded-full bg-silverio px-8 py-4 text-lg font-semibold text-white shadow-lg transition hover:bg-silverio-dark hover:shadow-xl active:scale-95"
        >
          Iniciar Consulta
          <svg
            className="h-5 w-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 7l5 5m0 0l-5 5m5-5H6"
            />
          </svg>
        </Link>

        {/* Disclaimer */}
        <p className="mt-8 text-xs text-gray-400 max-w-lg mx-auto">
          O Dr. Silvério é um assistente educativo. As informações fornecidas
          são de carácter educativo e informativo. Não substituem diagnóstico,
          tratamento ou aconselhamento médico profissional. Em caso de
          emergência, contacte o 112.
        </p>
      </div>
    </main>
  );
}
