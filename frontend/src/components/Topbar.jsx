import {
  Bell,
  Search,
  CalendarDays,
  ChevronDown,
  UserCircle2,
  Sparkles,
} from "lucide-react";

import { useFilterContext } from "../contexts/FilterContext";

function Topbar() {
  const {
    year,
    quarter,
    month,
  } = useFilterContext();

  function reportingPeriod() {
    if (year && month) return `${month} ${year}`;
    if (year && quarter) return `${quarter} ${year}`;
    if (year) return `${year}`;
    return "All Reporting Periods";
  }

  return (
    <header className="h-20 bg-white border-b border-slate-200 flex items-center justify-between px-10 shadow-sm">

      {/* LEFT */}

      <div className="flex items-center gap-6">

        <div className="flex items-center gap-3 bg-slate-100 rounded-xl px-5 py-3 w-[420px]">

          <Search
            size={18}
            className="text-slate-500"
          />

          <input
            type="text"
            placeholder="Search accounts, reports, journals..."
            className="bg-transparent outline-none w-full text-sm"
          />

        </div>

        <div className="hidden xl:flex items-center gap-3 border border-slate-200 rounded-xl px-4 py-3">

          <CalendarDays
            size={18}
            className="text-blue-600"
          />

          <div>

            <p className="text-xs text-slate-500">
              Reporting Period
            </p>

            <p className="font-semibold text-slate-700">
              {reportingPeriod()}
            </p>

          </div>

        </div>

      </div>

      {/* RIGHT */}

      <div className="flex items-center gap-6">

        <button className="hidden lg:flex items-center gap-2 bg-blue-600 hover:bg-blue-700 transition text-white rounded-xl px-5 py-3">

          <Sparkles size={17} />

          <span className="font-medium">
            Ask AI
          </span>

        </button>

        <button className="relative">

          <Bell
            size={22}
            className="text-slate-600"
          />

          <span className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-red-500"></span>

        </button>

        <button className="flex items-center gap-3 hover:bg-slate-100 rounded-xl px-3 py-2 transition">

          <UserCircle2
            size={40}
            className="text-blue-600"
          />

          <div className="text-left">

            <p className="font-semibold text-slate-800">
              Joseph Abuya
            </p>

            <p className="text-xs text-slate-500">
              Financial Analyst
            </p>

          </div>

          <ChevronDown
            size={16}
            className="text-slate-500"
          />

        </button>

      </div>

    </header>
  );
}

export default Topbar;