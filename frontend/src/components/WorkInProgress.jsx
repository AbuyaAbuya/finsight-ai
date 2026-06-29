import {
  Construction,
  Clock3,
  Sparkles,
} from "lucide-react";

function WorkInProgress({
  title,
  description,
}) {
  return (
    <div className="flex justify-center items-center min-h-[70vh]">

      <div className="bg-white rounded-2xl shadow-xl border border-slate-200 max-w-3xl w-full p-12 text-center">

        <div className="flex justify-center mb-6">

          <div className="w-24 h-24 rounded-full bg-blue-50 flex items-center justify-center">

            <Construction
              size={48}
              className="text-blue-600"
            />

          </div>

        </div>

        <h1 className="text-4xl font-bold text-slate-800">

          {title}

        </h1>

        <p className="text-blue-600 font-semibold mt-3 flex items-center justify-center gap-2">

          <Clock3 size={18} />

          Work in Progress

        </p>

        <p className="text-slate-500 mt-6 leading-8 text-lg">

          {description}

        </p>

        <div className="mt-10 rounded-xl bg-slate-50 border border-slate-200 p-6">

          <div className="flex justify-center mb-3">

            <Sparkles
              className="text-amber-500"
              size={22}
            />

          </div>

          <h3 className="font-semibold text-xl">

            Coming Soon

          </h3>

          <p className="text-slate-500 mt-2">

            We are building enterprise-grade financial reporting
            with interactive analysis, filters, drill-down,
            exports, and AI-powered insights.

          </p>

        </div>

      </div>

    </div>
  );
}

export default WorkInProgress;