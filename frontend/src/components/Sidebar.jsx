import { useState } from "react";
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  BookOpen,
  FileText,
  Landmark,
  Wallet,
  TrendingUp,
  Calculator,
  BarChart3,
  Bot,
  Settings,
  ChevronDown,
  ChevronRight,
  X,
} from "lucide-react";

function Sidebar({
  sidebarOpen,
  setSidebarOpen,
}) {
  return (
    <>
      {/* Desktop Sidebar */}

      <aside className="hidden lg:flex w-80 bg-slate-950 text-white border-r border-slate-800 flex-col">

        {/* Logo */}

        <div className="px-8 py-7 border-b border-slate-800">

          <h1 className="text-3xl font-bold tracking-tight">
            FinSight AI
          </h1>

          <p className="text-sm text-slate-400 mt-2">
            Enterprise Financial Planning & Analysis
          </p>

        </div>

        <div className="flex-1 overflow-y-auto py-4">

          <SidebarContent
            setSidebarOpen={setSidebarOpen}
          />

        </div>

        <div className="border-t border-slate-800 p-6">

          <div className="rounded-xl bg-slate-900 p-4">

            <p className="text-sm font-semibold">
              FinSight AI
            </p>

            <p className="text-xs text-slate-400 mt-1">
              Version 1.0
            </p>

          </div>

        </div>

      </aside>

      {/* Mobile Sidebar */}

      <aside
        className={`fixed top-0 left-0 z-40 h-full w-80 bg-slate-950 text-white border-r border-slate-800 transform transition-transform duration-300 lg:hidden ${sidebarOpen
            ? "translate-x-0"
            : "-translate-x-full"
          }`}
      >

        <div className="flex items-center justify-between px-6 py-6 border-b border-slate-800">

          <div>

            <h1 className="text-2xl font-bold">
              FinSight AI
            </h1>

            <p className="text-xs text-slate-400 mt-1">
              Enterprise FP&A
            </p>

          </div>

          <button
            onClick={() => setSidebarOpen(false)}
            className="text-slate-300 hover:text-white"
          >
            <X size={24} />
          </button>

        </div>

        <div className="flex-1 overflow-y-auto py-4">

          <SidebarContent
            setSidebarOpen={setSidebarOpen}
          />

        </div>

      </aside>

    </>
  );
}
function SidebarContent({
  setSidebarOpen,
}) {
  return (
    <>

      <SidebarSection
        title="Executive"
        setSidebarOpen={setSidebarOpen}
        items={[
          {
            icon: LayoutDashboard,
            title: "Executive Dashboard",
            path: "/",
          },
        ]}
      />

      <SidebarSection
        title="Financial Reporting"
        setSidebarOpen={setSidebarOpen}
        items={[
          {
            icon: BookOpen,
            title: "Trial Balance",
            path: "/trial-balance",
          },
          {
            icon: FileText,
            title: "Income Statement",
            path: "/income-statement",
          },
          {
            icon: Landmark,
            title: "Balance Sheet",
            path: "/balance-sheet",
          },
          {
            icon: Wallet,
            title: "Cash Flow",
            path: "/cash-flow",
          },
          {
            icon: FileText,
            title: "Statement of Equity",
            path: "/statement-equity",
          },
        ]}
      />

      <SidebarSection
        title="Planning & Analysis"
        setSidebarOpen={setSidebarOpen}
        items={[
          {
            icon: TrendingUp,
            title: "Budget",
            path: "/budget",
          },
          {
            icon: TrendingUp,
            title: "Forecast",
            path: "/forecast",
          },
          {
            icon: BarChart3,
            title: "Variance Analysis",
            path: "/variance",
          },
          {
            icon: BarChart3,
            title: "Scenario Planning",
            path: "/scenario",
          },
        ]}
      />
      <SidebarSection
        title="Analytics"
        setSidebarOpen={setSidebarOpen}
        items={[
          {
            icon: Calculator,
            title: "Financial Ratios",
            path: "/ratios",
          },
          {
            icon: BarChart3,
            title: "Reports",
            path: "/reports",
          },
        ]}
      />

      <SidebarSection
        title="Artificial Intelligence"
        setSidebarOpen={setSidebarOpen}
        items={[
          {
            icon: Bot,
            title: "AI Copilot",
            path: "/ai-copilot",
          },
        ]}
      />

      <SidebarSection
        title="Administration"
        setSidebarOpen={setSidebarOpen}
        items={[
          {
            icon: Settings,
            title: "Settings",
            path: "/settings",
          },
        ]}
      />

    </>
  );
}

function SidebarSection({
  title,
  items,
  setSidebarOpen,
}) {
  const [open, setOpen] = useState(true);

  return (
    <div className="mb-3">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-5 py-2 text-xs uppercase tracking-widest text-slate-500 hover:text-white transition"
      >
        <span>{title}</span>

        {open ? (
          <ChevronDown size={15} />
        ) : (
          <ChevronRight size={15} />
        )}
      </button>

      {open && (
        <div className="mt-1 space-y-1">
          {items.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.title}
                to={item.path}
                onClick={() => {
                  // Close sidebar automatically on phones
                  if (window.innerWidth < 1024) {
                    setSidebarOpen(false);
                  }
                }}
                className={({ isActive }) =>
                  `flex items-center gap-3 mx-3 px-4 py-3 rounded-xl transition-all duration-200 ${isActive
                    ? "bg-blue-600 text-white shadow-lg"
                    : "text-slate-300 hover:bg-slate-900 hover:text-white"
                  }`
                }
              >
                <Icon size={18} />

                <span className="text-sm font-medium">
                  {item.title}
                </span>
              </NavLink>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default Sidebar;