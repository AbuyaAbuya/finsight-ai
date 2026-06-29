import { Bot, Sparkles, Brain, MessageSquare } from "lucide-react";

function AICopilot() {
  return (
    <div className="max-w-6xl mx-auto py-10">

      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-3xl text-white p-10 shadow-xl">

        <div className="flex items-center gap-4">

          <div className="w-20 h-20 rounded-2xl bg-white/20 flex items-center justify-center">
            <Bot size={42} />
          </div>

          <div>
            <h1 className="text-4xl font-bold">
              AI Financial Copilot
            </h1>

            <p className="mt-2 text-blue-100 text-lg">
              Your intelligent FP&A assistant for financial analysis,
              forecasting and executive decision support.
            </p>
          </div>

        </div>

      </div>

      <div className="grid md:grid-cols-3 gap-6 mt-10">

        <div className="bg-white rounded-2xl shadow p-8 border">
          <Brain className="text-blue-600 mb-4" size={40} />

          <h2 className="text-xl font-semibold">
            Ask Financial Questions
          </h2>

          <p className="mt-3 text-slate-500">
            Ask questions such as:
          </p>

          <ul className="mt-4 space-y-2 text-slate-600">
            <li>• Why did profit decline?</li>
            <li>• Show revenue growth.</li>
            <li>• Compare this year vs last year.</li>
            <li>• Explain cash flow changes.</li>
          </ul>

        </div>

        <div className="bg-white rounded-2xl shadow p-8 border">

          <Sparkles className="text-amber-500 mb-4" size={40} />

          <h2 className="text-xl font-semibold">
            AI Insights
          </h2>

          <p className="mt-3 text-slate-500">
            Receive automated commentary,
            anomaly detection,
            financial summaries,
            and executive recommendations.
          </p>

        </div>

        <div className="bg-white rounded-2xl shadow p-8 border">

          <MessageSquare className="text-green-600 mb-4" size={40} />

          <h2 className="text-xl font-semibold">
            Coming Soon
          </h2>

          <p className="mt-3 text-slate-500">
            Chat with your financial data using natural language.
            FinSight AI will answer questions,
            generate reports,
            and explain trends instantly.
          </p>

        </div>

      </div>

      <div className="mt-10 bg-white rounded-2xl border shadow p-8">

        <h2 className="text-2xl font-semibold mb-4">
          Preview
        </h2>

        <div className="rounded-xl border-2 border-dashed border-slate-300 p-10 text-center">

          <Bot
            size={56}
            className="mx-auto text-blue-600 mb-5"
          />

          <h3 className="text-2xl font-semibold">
            AI Copilot is under active development
          </h3>

          <p className="text-slate-500 mt-4 max-w-2xl mx-auto">
            Soon you'll be able to ask questions like
            <strong> "Why did expenses increase?"</strong>,
            <strong> "Forecast next quarter revenue"</strong>,
            or
            <strong> "Summarize this financial statement"</strong>
            and receive instant AI-powered insights.
          </p>

        </div>

      </div>

    </div>
  );
}

export default AICopilot;